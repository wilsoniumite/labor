# pace.py — the pace of displacement against what has been seen. Her question (2026-09-25): is the model calibrated to
# the participation, output and hours changes already seen? Before this unit two measures were in (the US exit share and
# the build-out net of imports, decoupling.py); the pace was not: `global_crash.py`'s US drift, a point of the labour force
# a year, is the paper's slow channel, set by hand. Questions, stated before the data were fitted:
#   1. what the US prime-age data show since the employment peak (September 2024), measured two ways: the endpoints
#      (3-month averages at the peak and the latest month, as decoupling.py) and the trends (least squares on the monthly
#      rates, with standard errors robust to autocorrelation), from the peak and from January 2024; in points of the
#      labour force: non-employment (the fall in the employment rate), exits (the fall in participation) and unemployment;
#   2. how robust the exit share is — the share of lost employment that leaves the labour force — to the base and the
#      method (the crash model uses the endpoint measure from the peak);
#   3. the pace: the multiple of the paper's pace at which the model's own US non-employment over the window (today's
#      rules, no bust, robotics not arrived, care at its trend) matches the data: the trend, its upper bound (+2 s.e.) and
#      the endpoint. All of the observed change is attributed to displacement, so each is an upper bound on AI's;
#   4. the loop: whether the output gap can separate the model's spending loop from other forces on this window;
#   5. what the measured paces do to the crash model's main rows;
#   6. two sensitivities (her questions): care hired well above its trend over the window, holding employment up. The model
#      already hires into care at its trend, so the like-for-like adjustment adds back only the hiring above it, and only
#      if that hiring absorbed people AI displaced (care hires mostly women and new entrants, so it is an upper bound on
#      what care hides); counting all care hiring as non-employment would double count real jobs. And the build-out's own
#      jobs: construction's gain over the window, all of it counted as data centres (an upper bound), against
#      manufacturing's change.
#
# Run from paths/:  ../venv/Scripts/python.exe code/pace.py
# Out: results/pace.json, figures/fig_pace.png

from __future__ import annotations

import json
import os
import sys
from dataclasses import replace

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import decoupling as dc  # noqa: E402
import global_crash as gc  # noqa: E402

N = 24                                                            # quarters, as the crash model's runs
WAVES_NOW = gc.Waves(split=True, robot_lag=99.0, absorb=True)     # the window: robotics not arrived, care at its trend
WAVES_ROWS = gc.Waves(split=True, robot_lag=2.0, absorb=True)     # the model's rows: robotics two years out


def stored():
    j = json.load(open(os.path.join(ROOT, "results", "global_crash.json"), encoding="utf-8"))
    return gc.Common(**j["common"]), {r: gc.Region(**j["regions"][r]) for r in gc.R}, j


def prime_age() -> pd.DataFrame:
    return pd.DataFrame({"emp": dc.fred("LNS12300060"), "part": dc.fred("LNS11300060"), "unemp": dc.fred("LNS14000060")}).dropna()


def ols_nw(t: np.ndarray, y: np.ndarray, lags: int = 3) -> tuple[float, float]:
    """Slope and its Newey-West standard error."""
    X = np.column_stack([np.ones_like(t), t])
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    e = y - X @ b
    xtx = np.linalg.inv(X.T @ X)
    S = (X * e[:, None]).T @ (X * e[:, None])
    for L in range(1, lags + 1):
        w = 1 - L / (lags + 1)
        G = (X[L:] * e[L:, None]).T @ (X[:-L] * e[:-L, None])
        S += w * (G + G.T)
    V = xtx @ S @ xtx
    return float(b[1]), float(np.sqrt(V[1, 1]))


def measure(d: pd.DataFrame, base: pd.Timestamp, part_base: float) -> dict:
    """Trends since `base`, in points of the labour force a year: non-employment, exits, unemployment."""
    s = d.loc[base:]
    t = np.array([(i - s.index[0]).days / 365.25 for i in s.index])
    out = {}
    for k, y in (("non_employment", -s.emp.values / part_base * 100), ("exits", -s.part.values / part_base * 100),
                 ("unemployment", s.unemp.values)):
        b, se = ols_nw(t, y)
        out[k] = {"pts_a_year": round(b, 3), "se": round(se, 3)}
    return out


def observed() -> dict:
    d = prime_age()
    m = d.rolling(3).mean().dropna()
    peak = m.emp.loc["2022":].idxmax()
    end = m.index[-1]
    years = (end - peak).days / 365.25
    A, B = m.loc[peak], m.loc[end]
    ends = {}
    for name, base in (("the peak (3-month average)", m.loc[peak]), ("2024 average", d.loc["2024"].mean()),
                       ("2023-24 average", d.loc["2023":"2024"].mean())):
        ne = float(base.emp - B.emp) / float(base.part) * 100
        ex = float(base.part - B.part) / float(base.part) * 100
        ends[name] = {"non_employment_lf_pts": round(ne, 2), "exits_lf_pts": round(ex, 2),
                      "exit_share": round(ex / ne, 2) if ne > 0.05 else None}
    trends = {"since the peak": measure(d, peak, float(A.part)), "since January 2024": measure(d, pd.Timestamp("2024-01-01"), float(A.part))}
    for v in trends.values():
        ne, ex = v["non_employment"]["pts_a_year"], v["exits"]["pts_a_year"]
        v["exit_share"] = round(ex / ne, 2) if ne > 0.02 else None
    gdp, pot = dc.fred("GDPC1"), dc.fred("GDPPOT")
    gap = ((gdp / pot.reindex(gdp.index) - 1) * 100).dropna()
    q0 = gap.index[gap.index <= peak][-1]
    ur = dc.fred("UNRATE")
    part = d.part
    return {"window": f"{peak:%Y-%m} to {end:%Y-%m}", "years": round(years, 2),
            "endpoints_from": ends, "trends": trends,
            "prime_age_participation_range_2023_to_may_2026": [float(part.loc["2023-02":"2026-05"].min()), float(part.loc["2023-02":"2026-05"].max())],
            "prime_age_participation_june_2026_change": round(float(part.loc["2026-06-01"] - part.loc["2026-05-01"]), 2),
            "unemployment_rate_all_ages": [float(ur.loc[peak]), float(ur.iloc[-1])],
            "cbo_output_gap": {"from": [f"{q0:%Y-%m}", round(float(gap[q0]), 2)], "to": [f"{gap.index[-1]:%Y-%m}", round(float(gap.iloc[-1]), 2)]},
            "_d": d, "_m": m, "_peak": peak, "_gap": gap}


def at(x: np.ndarray, q: float) -> float:
    return float(np.interp(q, np.arange(len(x)), x))


def run(regs, cm, mult: float, rules=gc.MODERN, shock=None, waves=WAVES_NOW, n=N):
    rg = {r: replace(g, drift=g.drift * mult) for r, g in regs.items()}
    return rg, gc.simulate(rg, {r: rules for r in gc.R}, shock or gc.Shock(), cm, n, waves=waves)


def nonemp(o: dict, u0: float, q: float) -> float:
    us = o["US"]
    return at(us["u"], q) - u0 + at(us["out"], q)


def pace_for(regs, cm, target: float, q: float) -> float:
    """The multiple of the paper's pace at which the model's US non-employment rise after q quarters equals the target."""
    u0 = regs["US"].u0
    f = lambda m: nonemp(run(regs, cm, m)[1], u0, q) - target  # noqa: E731
    lo, hi = 0.0, 3.0
    if f(lo) >= 0:
        return 0.0
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if f(mid) < 0 else (lo, mid)
    return (lo + hi) / 2


def window_reading(o: dict, u0: float, q: float) -> dict:
    us = o["US"]
    return {"non_employment_lf_pts": round(nonemp(o, u0, q), 2), "exits_lf_pts": round(at(us["out"], q), 2),
            "unemployment_change": round(at(us["u"], q) - u0, 2), "output_gap_change": round(at(us["y"], q), 2)}


def rows(regs, cm, mult: float) -> dict:
    out = {}
    for name, rl, shock in (("modern rules | bust + displacement", gc.MODERN, gc.ai_shock(N)),
                            ("rules expand under pressure | bust + displacement", gc.EXPANDED, gc.ai_shock(N)),
                            ("rules erode under pressure | bust + displacement", gc.ERODED, gc.ai_shock(N)),
                            ("modern rules | displacement without a bust", gc.MODERN, None)):
        rg, o = run(regs, cm, mult, rl, shock, WAVES_ROWS)
        s4 = gc.summary(o, rg, 16)
        us = o["US"]
        k = int(np.argmax(us["u"] + us["out"]))
        out[name] = {"us_out_of_work_peak": round(float((us["u"] + us["out"])[k]), 1), "us_unemployment_at_peak": round(float(us["u"][k]), 1),
                     "year4_us_gap_min": s4["US"]["gap_min"], "year4_four_gap_min": s4["four_weighted_gap_min"]}
    return out


def main():
    cm, regs, stored_json = stored()
    ob = observed()
    q = ob["years"] * 4
    u0 = regs["US"].u0
    tr = ob["trends"]["since the peak"]["non_employment"]
    targets = {"trend": tr["pts_a_year"] * ob["years"],
               "trend + 2 s.e.": (tr["pts_a_year"] + 2 * tr["se"]) * ob["years"],
               "endpoint": ob["endpoints_from"]["the peak (3-month average)"]["non_employment_lf_pts"]}
    paces = {k: round(pace_for(regs, cm, v, q), 3) for k, v in targets.items()}
    _, o_paper = run(regs, cm, 1.0)
    peak, yrs = ob["_peak"], ob["years"]
    lf0 = float(dc.fred("CLF16OV").loc[peak])
    added = lambda sid: float(dc.fred(sid).iloc[-1] - dc.fred(sid).loc[peak]) / lf0 * 100  # noqa: E731
    trend = json.load(open(os.path.join(ROOT, "results", "exposure.json"), encoding="utf-8"))["care"]["regions"]["US"]["care_trend_pts_a_year"]
    care = added("CES6562000001")
    excess = care / yrs - trend
    with_care = {k: v + excess * yrs for k, v in targets.items()}
    sensitivity = {
        "care": {"added_lf_pts": round(care, 2), "added_lf_pts_a_year": round(care / yrs, 2), "model_trend_pts_a_year": trend,
                 "above_trend_pts_a_year": round(excess, 2),
                 "targets_with_above_trend_care_lf_pts": {k: round(v, 2) for k, v in with_care.items()},
                 "paces_with_above_trend_care": {k: round(pace_for(regs, cm, v, q), 3) for k, v in with_care.items()},
                 "note": "an upper bound on what care hides: the hiring above its trend counted as displaced people it took in"},
        "build_out": {"construction_added_lf_pts": round(added("USCONS"), 3), "manufacturing_added_lf_pts": round(added("MANEMP"), 3),
                      "note": "all of construction's gain counted as data centres (an upper bound); against manufacturing's change"}}
    res = {"observed": {k: v for k, v in ob.items() if not k.startswith("_")},
           "non_employment_targets_lf_pts": {k: round(v, 2) for k, v in targets.items()},
           "paces": {"multiples_of_the_papers": paces, "us_drift_papers_pts_a_year": regs["US"].drift,
                     "note": "the multiple of the paper's pace at which the model's own US non-employment over the window "
                             "(today's rules, no bust, robotics not arrived, care at its trend, the exit share as stored) "
                             "matches each measure of the data; all of the observed change attributed to displacement, so each "
                             "is an upper bound on AI's"},
           "window_model_at_the_papers_pace": window_reading(o_paper, u0, q),
           "window_model_at_each_pace": {k: window_reading(run(regs, cm, v)[1], u0, q) for k, v in paces.items()},
           "loop": {"note": "not identifiable on this window: at the paces the trends allow, the model's own output gap barely "
                            "moves, while the CBO gap fell from an overheated start; the fall is other forces"},
           "sensitivity": sensitivity,
           "rows": {"papers_pace": rows(regs, cm, 1.0), **{f"pace: {k}": rows(regs, cm, v) for k, v in paces.items()}}}
    mine = gc.summary(gc.simulate(regs, {r: gc.MODERN for r in gc.R}, gc.Shock(), cm, N), regs, 16)["US"]
    theirs = stored_json["scenarios"]["modern rules | displacement without a bust"]["year4"]["US"]
    res["reproduces_stored"] = {f: [mine[f], theirs[f]] for f in ("gap_min", "unemployment_max", "not_working_rise_max")}
    json.dump(res, open(os.path.join(ROOT, "results", "pace.json"), "w", encoding="utf-8"), indent=1)
    print(json.dumps(res, indent=1))
    figure(ob, regs, cm, paces, u0)


def figure(ob, regs, cm, paces, u0):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams["axes.titlesize"] = 10
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.6), layout="constrained")
    fig.get_layout_engine().set(rect=(0, 0.05, 1, 0.95))
    d, m, peak = ob["_d"], ob["_m"], ob["_peak"]
    a = ax[0]
    s = d.loc["2023":]
    a.plot(s.index, s.part, color="C0", lw=1, alpha=0.6, label="participation, monthly")
    a.plot(m.loc["2023":].index, m.loc["2023":].part, color="C0", lw=2, label="participation, 3-month average")
    b = a.twinx()
    b.plot(s.index, s.unemp, color="C3", lw=1, alpha=0.6)
    b.plot(m.loc["2023":].index, m.loc["2023":].unemp, color="C3", lw=2, label="unemployment (right)")
    a.axvline(peak, color="grey", lw=0.8, ls=":")
    import matplotlib.dates as mdates
    a.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 7)))
    a.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    a.set_title("1. US prime-age (25-54) participation and unemployment, %")
    h1, l1 = a.get_legend_handles_labels(); h2, l2 = b.get_legend_handles_labels()
    a.legend(h1 + h2, l1 + l2, fontsize=8, loc="lower left")
    a = ax[1]
    part0 = float(m.loc[peak].part)
    ne = (float(m.loc[peak].emp) - m.loc[peak:].emp) / part0 * 100
    t_obs = [(i - peak).days / 365.25 for i in ne.index]
    a.plot(t_obs, ne.values, color="k", lw=2, label="observed, 3-month average")
    tr = ob["trends"]["since the peak"]["non_employment"]
    tt = np.linspace(0, ob["years"], 20)
    a.plot(tt, tr["pts_a_year"] * tt, color="k", ls="--", lw=1, label=f"observed trend ({tr['pts_a_year']:+.2f} ± {tr['se']:.2f} a year)")
    tq = np.arange(N) / 4
    for (k, mult), c in zip((("the paper's pace", 1.0),) + tuple((f"pace: {k} (x{v:.2f})", v) for k, v in paces.items()),
                            ("C3", "C2", "C1", "C0")):
        _, o = run(regs, cm, mult)
        a.plot(tq, o["US"]["u"] - u0 + o["US"]["out"], color=c, label="model, " + k)
    a.axhline(0, color="grey", lw=0.8); a.set_xlim(0, 3)
    a.set_title("2. Non-employment since the 2024 peak (points of the labour force)"); a.set_xlabel("years from the peak")
    a.legend(fontsize=7.5)
    a = ax[2]
    rows_ = {"the paper's pace": (1.0, "C3")} | {f"{k} (x{v:.2f})": (v, c) for (k, v), c in zip(paces.items(), ("C2", "C1", "C0"))}
    for k, (mult, c) in rows_.items():
        _, o = run(regs, cm, mult, gc.MODERN, gc.ai_shock(N), WAVES_ROWS)
        a.plot(tq, o["US"]["u"] + o["US"]["out"], color=c, label=k)
    a.set_title("3. US out of work after a dot-com-sized bust, today's rules, %"); a.set_xlabel("years")
    a.legend(fontsize=8)
    fig.text(0.01, 0.01, f"Window {ob['window']}. Model: today's rules, no bust (panel 2), robotics not arrived, care hiring at its trend, "
             "the exit share as stored. All of the observed change attributed to displacement (upper bounds).", fontsize=8)
    p = os.path.join(ROOT, "figures", "fig_pace.png"); fig.savefig(p, dpi=150); print(p)


if __name__ == "__main__":
    main()
