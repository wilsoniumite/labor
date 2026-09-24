# regime_digestion.py — how slowly do markets and forecasters digest news about the regime?
#
# The speed results (speed_scenarios.py) rest on one assumption: that people digest judgements about
# the regime slowly. Three public tests, at three layers:
#   1. Expectations of the next year. The Coibion–Gorodnichenko regression of forecast error on
#      forecast revision: with full, instant digestion the slope is 0; a positive slope b means
#      revisions are too small, and lambda = b / (1 + b) is the share of news not yet in the forecast
#      after one revision period (half-life ln 0.5 / ln lambda periods). Run on the Survey of
#      Professional Forecasters' 3-month bill forecasts (1–3 quarters ahead) and on market forwards
#      (Gürkaynak–Sack–Wright zero curve; 1-year rates 1, 2 and 4 years ahead, net of the Kim–Wright
#      term premium from 1990, raw from 1972).
#   2. The regime anchor. The survey's forecast of the 10-year average bill rate (1992–) and the
#      market's expected 1-year rate 9 years ahead (forward net of Kim–Wright): how fast they moved
#      toward realized rates (a constant-gain fit; part of any slowness is prudence, since a
#      forecaster should not read the cycle as a regime), the record of their errors, and whether
#      they beat naive rules.
#   3. What it means in the model: if people digest regime news over years while AI digests it in
#      weeks, adopting AI can itself reprice the curve — a catch-up with no news at all.
# Layer 0 — prices of quantified news, days since 1995 — is digestion_history.py.
#
# Run from paths/:  ../venv/Scripts/python.exe code/regime_digestion.py
# Out: results/regime_digestion.json, figures/fig_regime_digestion.png

from __future__ import annotations

import io
import json
import os
import sys
import warnings
from dataclasses import replace

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy.optimize import minimize_scalar  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "..", "pinning", "code"))
import lambda_compute2 as _lc  # noqa: E402
import macro as m  # noqa: E402
import recognition as rc  # noqa: E402
import regimes as rg  # noqa: E402

_lc.CACHE = os.path.join(ROOT, "cache")
NL = chr(10)
PRICE_HL_TRADING_DAYS = 9.8          # digestion_history.py: US 10Y 1982-94, the drifting quarter of each move
warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")


# ------------------------------------------------------------------ data
def gsw_monthly():
    """Gürkaynak–Sack–Wright zero yields, month-end (cache/fed: a trimmed vintage of the Board's file)."""
    txt = open(os.path.join(ROOT, "cache", "fed", "gsw_feds200628_trimmed.csv"), encoding="utf-8").read().splitlines()
    g = pd.read_csv(io.StringIO(NL.join(ln for ln in txt if not ln.startswith("#"))), parse_dates=["Date"]).set_index("Date")
    return g.resample("ME").last()


def kw_monthly():
    return {n: _lc.pull_fred(f"THREEFYTP{n}").resample("ME").last() for n in range(1, 11)}


def spf(name):
    df = pd.read_excel(os.path.join(ROOT, "cache", "spf", f"median_{name}_level.xlsx"))
    df["q"] = pd.PeriodIndex.from_fields(year=df.YEAR, quarter=df.QUARTER, freq="Q")
    return df.set_index("q")


def bill():
    tb = _lc.pull_fred("TB3MS")
    q = tb.groupby(tb.index.to_period("Q")).mean()
    a = tb.resample("YE").mean()
    a.index = a.index.year
    return q, a


# ------------------------------------------------------------------ statistics
def ols_hac(y, x, lags):
    """OLS of y on a constant and x with Newey–West (Bartlett) standard errors."""
    X = np.column_stack([np.ones(len(x)), x])
    XtX = np.linalg.inv(X.T @ X)
    b = XtX @ X.T @ y
    Xu = X * (y - X @ b)[:, None]
    S = Xu.T @ Xu
    for lag in range(1, lags + 1):
        G = Xu[lag:].T @ Xu[:-lag]
        S += (1.0 - lag / (lags + 1.0)) * (G + G.T)
    return b, np.sqrt(np.diag(XtX @ S @ XtX))


def cg(err, rev, lags):
    d = pd.concat([err.rename("e"), rev.rename("r")], axis=1).dropna()
    b, se = ols_hac(d["e"].values, d["r"].values, lags)
    return float(b[1]), float(se[1]), len(d)


def half_life(b, period):
    """Half-life of undigested news implied by a CG slope b, in the units of `period`."""
    if b <= 0:
        return None
    lam = b / (1.0 + b)
    return float(np.log(0.5) / np.log(lam) * period)


def gain_fit(anchor: pd.Series, realized: pd.Series):
    """Constant gain g: anchor_t = anchor_{t-1} + g (realized_{t-1} - anchor_{t-1}), fitted from the first value."""
    yrs = anchor.index

    def path(g):
        a = [anchor.iloc[0]]
        for y in yrs[1:]:
            a.append(a[-1] + g * (realized.loc[y - 1] - a[-1]))
        return np.array(a)
    r = minimize_scalar(lambda g: np.sum((path(g) - anchor.values) ** 2), bounds=(0.0, 1.0), method="bounded")
    return float(r.x), float(np.sqrt(r.fun / len(yrs)))


# ------------------------------------------------------------------ the tests
def layer1(g, kw, sp, bq):
    out = {"survey": {}, "market_kw": {}, "market_raw": {}}
    for a, b_ in (("1981Q3", "2026Q2"), ("1981Q3", "1994Q4"), ("1995Q1", "2007Q4"), ("2008Q1", "2026Q2")):
        row = {}
        for h in (1, 2, 3):
            F, Fprev = sp[f"TBILL{2 + h}"], sp[f"TBILL{3 + h}"].shift(1)
            err = pd.Series(bq.reindex(sp.index + h).values, index=sp.index) - F
            bb, se, n = cg(err[a:b_], (F - Fprev)[a:b_], h + 1)
            hl = half_life(bb, 3.0)
            row[f"{h}q ahead"] = {"b": round(bb, 2), "se": round(se, 2), "n": n, "half_life_months": None if hl is None else round(hl, 1)}
        out["survey"][f"{a[:4]}-{b_[:4]}"] = row
    y = {n: g[f"SVENY{n:02d}"] for n in range(1, 11)}
    f = {k: (k + 1) * y[k + 1] - k * y[k] for k in range(1, 9)}
    ftp = {k: (k + 1) * kw[k + 1] - k * kw[k] for k in range(1, 9)}
    for label, fk, eras in (("market_kw", {k: f[k] - ftp[k] for k in range(1, 9)}, (("1990", "2025"), ("1990", "2007"), ("2008", "2025"))),
                            ("market_raw", f, (("1972", "2025"), ("1972", "1994"), ("1995", "2025")))):
        for a, b_ in eras:
            row = {}
            for k in (1, 2, 4):
                err = y[1].shift(-12 * k) - fk[k]
                bb, se, n = cg(err[a:b_], (fk[k] - fk[k + 1].shift(12))[a:b_], 12 * (k + 1))
                hl = half_life(bb, 12.0)
                row[f"{k}y ahead"] = {"b": round(bb, 2), "se": round(se, 2), "n": n, "half_life_months": None if hl is None else round(hl, 1)}
            out[label][f"{a}-{b_}"] = row
    return out, y, f


def layer2(g, kw, ba):
    b10 = spf("bill10").dropna()
    b10 = b10[b10.QUARTER == 1].set_index("YEAR")["BILL10"]
    f9 = (10 * g["SVENY10"] - 9 * g["SVENY09"]) - (10 * kw[10] - 9 * kw[9])
    f9y = f9.resample("YE").mean()
    f9y.index = f9y.index.year
    out = {"gain_fits": {}}
    for name, series, spans in (("survey 10-year bill average", b10, ((1992, 2026), (1992, 2007), (2008, 2021), (2021, 2026))),
                                ("market 1y rate 9y ahead, net of KW", f9y.dropna(), ((1990, 2025), (1990, 2007), (2008, 2021), (2021, 2025)))):
        out["gain_fits"][name] = {}
        for a, b_ in spans:
            gg, rmse = gain_fit(series.loc[a:b_], ba)
            out["gain_fits"][name][f"{a}-{b_}"] = {"gain_per_year": round(gg, 3),
                                                   "half_life_years": round(float(np.log(0.5) / np.log(1 - gg)), 1) if gg > 0 else None,
                                                   "rmse": round(rmse, 2)}
    real10 = pd.Series({yr: ba.loc[yr:yr + 9].mean() for yr in b10.index if yr + 9 <= 2025})
    errs = real10 - b10.loc[real10.index]
    bench = {"survey anchor": b10.loc[real10.index], "no change (last year's rate)": pd.Series({yr: ba.loc[yr - 1] for yr in real10.index}),
             "trailing 5-year average": pd.Series({yr: ba.loc[yr - 5:yr - 1].mean() for yr in real10.index})}
    out["survey_anchor_record"] = {
        "surveys": f"{real10.index[0]}-{real10.index[-1]} (realized 10-year averages overlap: about {len(real10) / 10:.1f} independent decades)",
        "too_high_share": round(float(np.mean(errs < 0)), 2), "mean_error_pp": round(float(errs.mean()), 2),
        "rmse_pp": {k: round(float(np.sqrt(np.mean((real10 - v) ** 2))), 2) for k, v in bench.items()}}
    return out, b10, f9y, real10


def layer3(e):
    """The model's consequence: slow human regime digestion, then AI adoption."""
    br = m.Bridges(capital_premium=5.0, alpha_fiscal=0.25, alpha_rent=0.02)
    old = rc.refine(m.macro_path(e, m.TechPath(eta_end=1.0, lam_end=e.lam), br, 25.0, 0.25), 1 / 52)
    new = rc.refine(m.macro_path(e, m.TechPath(eta_end=0.04, lam_end=0.01, t_mid=6, width=6), br, 25.0, 0.25), 1 / 52)
    t = old["t"]
    T10 = np.array([10.0])
    base = rc.Learning(sigma=1.0, p0=0.05)
    w = t <= 15.0 + 1e-9

    def run(lr):
        p = rc.learn(old, new, lr)
        z = np.array([rg.zero(T10, mx)[0] for mx in rc.market_curves(old, new, p)[0]]) * 100
        month = float(np.max(np.abs(z[4:][w[4:]] - z[:-4][w[4:]])))
        return p, z, {"p_0.5": rc.crossing(t, p, 0.5), "max_10Y_move_in_a_month_bp": round(month, 1),
                      "max_10Y_move_in_a_quarter_bp": round(float(np.max(np.abs(z[13:][w[13:]] - z[:-13][w[13:]]))), 1)}
    out, paths = {}, {}
    p, z, row = run(base)
    out["instant (the evidence)"], paths["instant (the evidence)"] = row, (p, z)
    for hl in (1.0, 3.0, 5.0):
        for ai in (False, True):
            lr = replace(base, digest=hl) if not ai else replace(base, digest=hl, trust=(5.0, 1.0), capacity_end=30.0)
            key = f"human regime digestion {hl:g}y" + (", AI adopted around year 5 (x30)" if ai else "")
            p, z, row = run(lr)
            out[key], paths[key] = row, (p, z)
    i0, i1 = int(np.searchsorted(t, 4.5)), int(np.searchsorted(t, 5.5))
    ev = paths["instant (the evidence)"][1]
    out["instant (the evidence)"]["10Y_move_years_4.5_to_5.5_bp"] = round(float(ev[i1] - ev[i0]), 1)
    for hl in (1.0, 3.0, 5.0):
        k0 = f"human regime digestion {hl:g}y"
        k1 = k0 + ", AI adopted around year 5 (x30)"
        out[k1]["10Y_move_years_4.5_to_5.5_bp"] = round(float(paths[k1][1][i1] - paths[k1][1][i0]), 1)
        out[k0]["10Y_move_years_4.5_to_5.5_bp"] = round(float(paths[k0][1][i1] - paths[k0][1][i0]), 1)
    return out, t, paths


def main():
    e, _, _, _ = m.calibrate(base=m.CAPITAL_BASE)
    g, kw, sp = gsw_monthly(), kw_monthly(), spf("tbill")
    bq, ba = bill()
    out = {"sources": {"GSW": "Federal Reserve Board, feds200628 (staff research data), trimmed vintage in cache/fed",
                       "SPF": "Philadelphia Fed Survey of Professional Forecasters, median TBILL and BILL10 (cache/spf)",
                       "FRED": "TB3MS; THREEFYTP1-10 (Kim-Wright term premia)"}}
    out["layer1_next_year"], y, f = layer1(g, kw, sp, bq)
    out["layer2_regime_anchor"], b10, f9y, real10 = layer2(g, kw, ba)
    out["layer3_model_catch_up"], t, paths = layer3(e)
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, "results", "regime_digestion.json"), "w", encoding="utf-8"), indent=1, default=str)
    print(json.dumps(out, indent=1, default=str)[:6000])
    figure(y, f, b10, f9y, real10, ba, out, t, paths)


def figure(y, f, b10, f9y, real10, ba, out, t, paths):
    INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
    REAL, FWD, SURV, MKT = "#0b0b0b", "#6da7ec", "#eb6834", "#2a78d6"
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9.5, "axes.edgecolor": GRID,
                         "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
                         "axes.titlesize": 10.5, "axes.titleweight": "bold", "axes.titlecolor": INK,
                         "axes.titlelocation": "left"})
    fig, ax = plt.subplots(2, 2, figsize=(15, 10), facecolor=SURF, layout="constrained")
    fig.get_layout_engine().set(rect=(0, 0.03, 1, 0.97), h_pad=0.12, w_pad=0.1)
    for a in ax.flat:
        a.set_facecolor(SURF); a.grid(True, color=GRID, lw=0.8); a.set_axisbelow(True)
        for sp_ in ("top", "right"):
            a.spines[sp_].set_visible(False)
    # 1. what the curve priced, year by year
    a = ax[0, 0]
    y1 = y[1]["1988":]
    a.plot(y1.index, y1.values, color=REAL, lw=2, label="1-year rate, realized")
    first = True
    for yr in range(1990, 2026):
        d = pd.Timestamp(f"{yr}-12-31")
        if d not in f[1].index:
            continue
        fw = [y[1].loc[d]] + [f[k].loc[d] for k in range(1, 8)]
        a.plot([d + pd.DateOffset(years=k) for k in range(8)], fw, color=FWD, lw=1.1, alpha=0.9,
               label="what the curve priced at each year-end (1-year forwards)" if first else None)
        first = False
    a.set_xlim(pd.Timestamp("1989-01-01"), pd.Timestamp("2027-01-01")); a.set_ylim(-0.5, 9)
    a.set_title("1. What the curve priced against what came" + NL + "US Treasuries (Gürkaynak–Sack–Wright); forwards include term premia")
    a.set_ylabel("%"); a.legend(frameon=False, fontsize=8.5, labelcolor=INK, loc="upper right")
    # 2. the regime anchors
    a = ax[0, 1]
    a.plot(ba.loc[1988:2025].index, ba.loc[1988:2025].values, color=REAL, lw=1.2, alpha=0.6, label="3-month bill, annual average")
    a.plot(real10.index, real10.values, color=REAL, lw=2, label="the next 10 years' average, realized")
    a.plot(b10.index, b10.values, color=SURV, lw=2, marker="o", ms=3.5, label="survey: expected 10-year average")
    a.plot(f9y.loc[1990:].index, f9y.loc[1990:].values, color=MKT, lw=2, label="market: 1-year rate 9 years ahead, net of term premium")
    rec = out["layer2_regime_anchor"]["survey_anchor_record"]
    a.set_title("2. The regime anchor moved over years" + NL
                + f"survey too high in {rec['too_high_share']:.0%} of surveys; beaten by 'no change'")
    a.set_ylabel("%"); a.legend(frameon=False, fontsize=8, labelcolor=INK, loc="upper right")
    # 3. three layers, three speeds
    a = ax[1, 0]
    L1, L2 = out["layer1_next_year"], out["layer2_regime_anchor"]["gain_fits"]
    rows = [("prices: 10Y rate news, 1982–94" + NL + "(a quarter of each move; since 1995 none)", PRICE_HL_TRADING_DAYS * 365 / 252 / 30.4, "#b9b8b3"),
            ("survey: bill 1 quarter ahead", L1["survey"]["1981-2026"]["1q ahead"]["half_life_months"], SURV),
            ("survey: bill 3 quarters ahead", L1["survey"]["1981-2026"]["3q ahead"]["half_life_months"], SURV),
            ("market: 1-year rate 1 year ahead (net of KW)", L1["market_kw"]["1990-2025"]["1y ahead"]["half_life_months"], MKT),
            ("survey anchor: 10-year average, 2008–21", L2["survey 10-year bill average"]["2008-2021"]["half_life_years"] * 12, SURV),
            ("market anchor: 9 years ahead, 2008–21", L2["market 1y rate 9y ahead, net of KW"]["2008-2021"]["half_life_years"] * 12, MKT),
            ("survey anchor, 2021–26", L2["survey 10-year bill average"]["2021-2026"]["half_life_years"] * 12, SURV),
            ("market anchor, 2021–25", L2["market 1y rate 9y ahead, net of KW"]["2021-2025"]["half_life_years"] * 12, MKT)]
    for i, (lab, v, col) in enumerate(rows):
        a.barh(i, v, color=col, height=0.6)
        a.text(v * 1.08, i, (f"{v * 30.4:.0f} days" if v < 1 else f"{v:.1f} months" if v < 24 else f"{v / 12:.1f} years"),
               va="center", fontsize=8, color=INK2)
    a.set_xscale("log"); a.set_xlim(0.2, 400)
    a.set_yticks(range(len(rows))); a.set_yticklabels([r[0] for r in rows], fontsize=8.5); a.invert_yaxis()
    a.set_xticks([0.5, 1, 3, 12, 60, 120]); a.set_xticklabels(["2 wk", "1 mo", "1 qtr", "1 yr", "5 yrs", "10 yrs"])
    a.set_title("3. Three layers, three speeds" + NL + "half-life of news not yet in the price or the forecast")
    # 4. the model: catch-up
    a = ax[1, 1]
    w = t <= 10
    sty = {"instant (the evidence)": ("#104281", "-", "the evidence (instant digestion)"),
           "human regime digestion 3y": (SURV, "--", "people digesting regime news, half-life 3 years"),
           "human regime digestion 3y, AI adopted around year 5 (x30)": ("#e34948", "-", "the same, AI adopted around year 5")}
    for key, (col, ls, lab) in sty.items():
        p, z = paths[key]
        a.plot(t[w], z[w] - z[0], color=col, ls=ls, lw=2, label=lab)
    a.axvspan(4.5, 5.5, color=GRID, alpha=0.6, lw=0)
    a.text(4.55, a.get_ylim()[1] * 0.05 if a.get_ylim()[1] > 0 else 5, "adoption", fontsize=8, color=INK2)
    r3 = out["layer3_model_catch_up"]
    a.set_title("4. Adopting AI can itself reprice the curve" + NL
                + f"10Y; adoption year +{r3['human regime digestion 3y, AI adopted around year 5 (x30)']['10Y_move_years_4.5_to_5.5_bp']:.0f} bp, "
                  f"+{r3['human regime digestion 3y']['10Y_move_years_4.5_to_5.5_bp']:.0f} without AI, +{r3['instant (the evidence)']['10Y_move_years_4.5_to_5.5_bp']:.0f} in the evidence")
    a.set_xlabel("years (deficits dominate)"); a.set_ylabel("bp from the start"); a.legend(frameon=False, fontsize=8.5, labelcolor=INK, loc="upper left")
    fig.text(0.01, 0.005, "Coibion–Gorodnichenko slopes b -> share of news not yet absorbed per revision, b/(1+b) -> half-life. Anchors: constant-gain fits toward "
             "realized bill rates (part of any slowness is prudence). Sources: FRB (GSW), Philadelphia Fed (SPF), FRED.", fontsize=8, color=INK2)
    pth = os.path.join(ROOT, "figures", "fig_regime_digestion.png"); fig.savefig(pth, dpi=150, facecolor=SURF); print(pth)


if __name__ == "__main__":
    main()
