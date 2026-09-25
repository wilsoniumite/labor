# decoupling.py — output rising while work does not: the US national accounts against the paper's mechanism. Her question
# (2026-09-25): output and GDPNow nowcasts are rising while the US sheds labour — does that fit the model; is AI pushing
# manufacturing? Questions, stated before the data were fitted:
#   1. output against work: nonfarm business output, hours and output per hour, window by window; labour's share of
#      business output against its whole history (BLS via FRED, 1947-);
#   2. the nowcast: real GDP growth quarter by quarter and the Atlanta Fed's GDPNow for the quarter in progress; how far
#      GDPNow's final nowcasts have missed published (revised) growth, 2011-;
#   3. manufacturing: output by industry (Federal Reserve industrial production) against manufacturing jobs;
#   4. the AI build-out's size, for the crash model (which assumed 1.5% of US GDP): investment in information processing
#      equipment and software and in power and communication structures, less imports of computers, peripherals and
#      parts, % of GDP (BEA via FRED) — against 2022 (before ChatGPT) and against its 2015-22 trend. Data-centre buildings
#      sit inside office structures, published only annually, and are left out: the measure is a lower bound;
#   5. where the displaced go: prime-age (25-54) employment, participation and unemployment from the prime-age employment
#      peak to the latest month (3-month averages), against 2007-10 and 2000-03 — the share of lost employment that shows
#      up as people leaving the labour force rather than as unemployment (the "exit share").
#
# Run from paths/:  ../venv/Scripts/python.exe code/decoupling.py
# Out: results/decoupling.json, figures/fig_decoupling.png

from __future__ import annotations

import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(os.path.dirname(ROOT), "pinning", "code"))
import lambda_compute2 as _lc  # noqa: E402

_lc.CACHE = os.path.join(ROOT, "cache")
IP = {"IPMAN": "all manufacturing", "IPG3344S": "semiconductors", "IPG334S": "computers and electronics",
      "IPG335S": "electrical equipment", "IPG2211S": "electric power generation"}
BUILD = {"Y033RC1Q027SBEA": "information processing equipment", "B985RC1Q027SBEA": "software",
         "W003RC1Q027SBEA": "power and communication structures", "B852RC1Q027SBEA": "less: imports of computers, peripherals and parts"}


def fred(sid: str) -> pd.Series:
    s = _lc.pull_fred(sid)
    if s is None:
        raise SystemExit(f"FRED {sid}: not available")
    return s


def label(t) -> str:
    return str(pd.Timestamp(t).date())[:7]


def output_and_work() -> dict:
    out, hrs, prod, ls = fred("OUTNFB"), fred("HOANBS"), fred("OPHNFB"), fred("PRS85006173")
    end = out.index[-1]
    windows = {}
    for a in ("2015-01-01", "2019-10-01", "2023-04-01"):
        a_, b_ = pd.Timestamp(a), end
        yrs = (b_ - a_).days / 365.25 if a != "2015-01-01" else (pd.Timestamp("2019-10-01") - a_).days / 365.25
        b_ = end if a != "2015-01-01" else pd.Timestamp("2019-10-01")
        ann = lambda s: round(100 * ((s[b_] / s[a_]) ** (1 / yrs) - 1), 2)  # noqa: E731
        windows[f"{label(a_)} to {label(b_)}"] = {"output_pct_a_year": ann(out), "hours_pct_a_year": ann(hrs), "output_per_hour_pct_a_year": ann(prod),
                                                  "labour_share_change_pts": round(float(ls[b_] - ls[a_]), 1)}
    ch4 = ls.diff(4)
    return {"latest": label(end), "four_quarters": {"output_pct": round(100 * float(out.iloc[-1] / out.iloc[-5] - 1), 2),
                                                     "hours_pct": round(100 * float(hrs.iloc[-1] / hrs.iloc[-5] - 1), 2),
                                                     "output_per_hour_pct": round(100 * float(prod.iloc[-1] / prod.iloc[-5] - 1), 2)},
            "windows": windows,
            "labour_share": {"index_2017_100": round(float(ls.iloc[-1]), 1), "lowest_since": label(ls.index[0]),
                             "is_record_low": bool(ls.iloc[-1] <= ls.min()), "previous_record_low": round(float(ls.iloc[:-1].min()), 1),
                             "four_quarter_change": round(float(ch4.iloc[-1]), 1),
                             "larger_four_quarter_falls_since_1990": {label(k): round(float(v), 1) for k, v in ch4.loc["1990":].iloc[:-1].nsmallest(8).items() if v < ch4.iloc[-1]}},
            "_series": (out, hrs, ls)}


def nowcast() -> dict:
    gn, g = fred("GDPNOW"), fred("A191RL1Q225SBEA")
    e = (gn - g.reindex(gn.index)).dropna()
    current = gn.index[-1]
    return {"gdpnow_current_quarter": {"quarter": label(current), "pct_saar": round(float(gn.iloc[-1]), 1)},
            "gdp_growth_last_8_quarters_pct_saar": {label(k): float(v) for k, v in g.iloc[-8:].items()},
            "gdpnow_error": {"quarters": len(e), "mean": round(float(e.mean()), 2), "mean_abs": round(float(e.abs().mean()), 2),
                             "mean_abs_excluding_2020": round(float(e[e.index.year != 2020].abs().mean()), 2),
                             "largest_recent_miss": {label(e.iloc[-8:].abs().idxmax()): round(float(e.loc[e.iloc[-8:].abs().idxmax()]), 1)}}}


def manufacturing() -> dict:
    ip = {k: fred(k) for k in IP}
    man = fred("MANEMP")
    end = man.index[-1]
    out = {}
    for lab, a in (("12 months", end - pd.DateOffset(months=12)), ("24 months", end - pd.DateOffset(months=24)), ("since 2019-12", pd.Timestamp("2019-12-01"))):
        out[lab] = {**{IP[k]: round(100 * float(v[end] / v[a] - 1), 1) for k, v in ip.items()}, "manufacturing jobs": round(100 * float(man[end] / man[a] - 1), 1)}
    return {"latest": label(end), "changes_pct": out, "_series": (ip, man)}


def build_out() -> dict:
    gdp = fred("GDP")
    sh = pd.DataFrame({BUILD[k]: (-1 if k == "B852RC1Q027SBEA" else 1) * 100 * fred(k) / gdp.reindex(fred(k).index) for k in BUILD}).dropna()
    sh["net"] = sh.sum(axis=1)
    yr = sh.groupby(sh.index.year).mean()
    t = yr.loc[2015:2022, "net"]
    slope, icpt = np.polyfit(t.index, t.values, 1)
    last = sh.index[-1]
    tt = last.year + (last.month - 1) / 12
    trend_now = float(slope * tt + icpt)
    latest = sh.iloc[-1]
    return {"latest": label(last), "pct_gdp_latest": {k: round(float(v), 2) for k, v in latest.items()},
            "pct_gdp_by_year": {int(y): {k: round(float(v), 2) for k, v in r.items()} for y, r in yr.loc[2015:].iterrows()},
            "change_since_2022_pts": {k: round(float(latest[k] - yr.loc[2022, k]), 2) for k in sh.columns},
            "trend_2015_22_pts_a_year": round(float(slope), 3),
            "net_above_2015_22_trend_pts": round(float(latest["net"] - trend_now), 2),
            "net_above_2022_pts": round(float(latest["net"] - yr.loc[2022, "net"]), 2),
            "crash_model_assumed_pct_gdp": 1.5, "_sh": sh}


def where_they_go() -> dict:
    d = pd.DataFrame({"employment_rate": fred("LNS12300060"), "participation": fred("LNS11300060"), "unemployment": fred("LNS14000060")}).dropna()
    m = d.rolling(3).mean().dropna()
    peak = m.employment_rate.loc["2022":].idxmax()
    end = m.index[-1]

    def episode(a, b):
        A, B = m.loc[a], m.loc[b]
        de, dl = float(B.employment_rate - A.employment_rate), float(B.participation - A.participation)
        return {"window": f"{label(a)} to {label(b)}", "employment_rate_change": round(de, 2), "participation_change": round(dl, 2),
                "unemployment_change": round(float(B.unemployment - A.unemployment), 2), "exit_share": round(dl / de, 2) if abs(de) > 1e-9 else None}
    return {"prime_age_25_54": {"since_the_employment_peak": episode(peak, end),
                                "2007-10 (recession)": episode(pd.Timestamp("2007-12-01"), pd.Timestamp("2010-06-01")),
                                "2000-03 (recession and the China shock)": episode(pd.Timestamp("2000-12-01"), pd.Timestamp("2003-12-01"))},
            "all_ages_24_months": {"unemployment_rate": [float(fred("UNRATE").iloc[-25]), float(fred("UNRATE").iloc[-1])],
                                   "participation": [float(fred("CIVPART").iloc[-25]), float(fred("CIVPART").iloc[-1])],
                                   "employment_rate": [float(fred("EMRATIO").iloc[-25]), float(fred("EMRATIO").iloc[-1])]},
            "_m": m, "_peak": peak}


def main():
    ow, nc, mf, bo, wg = output_and_work(), nowcast(), manufacturing(), build_out(), where_they_go()
    strip = lambda d: {k: v for k, v in d.items() if not k.startswith("_")}  # noqa: E731
    res = {"output_and_work": strip(ow), "nowcast": nc, "manufacturing": strip(mf), "ai_build_out": strip(bo), "where_the_displaced_go": strip(wg)}
    json.dump(res, open(os.path.join(ROOT, "results", "decoupling.json"), "w", encoding="utf-8"), indent=1)
    print(json.dumps(res, indent=1))
    figure(ow, mf, bo, wg)


def figure(ow, mf, bo, wg):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams["axes.titlesize"] = 10
    fig, ax = plt.subplots(2, 2, figsize=(14, 9.4), layout="constrained")
    fig.get_layout_engine().set(rect=(0, 0.03, 1, 0.97))
    out, hrs, ls = ow["_series"]
    base = pd.Timestamp("2019-10-01")
    a = ax[0, 0]
    a.plot(out.loc["2015":].index, 100 * out.loc["2015":] / out[base], color="C0", label="output, nonfarm business")
    a.plot(hrs.loc["2015":].index, 100 * hrs.loc["2015":] / hrs[base], color="C1", label="hours worked")
    b = a.twinx()
    b.plot(ls.loc["2015":].index, ls.loc["2015":], color="C3", ls="--", label="labour's share (right; 2017 = 100)")
    a.set_title("US output against hours (2019Q4 = 100), and labour's share of business output")
    h1, l1 = a.get_legend_handles_labels(); h2, l2 = b.get_legend_handles_labels()
    a.legend(h1 + h2, l1 + l2, fontsize=8, loc="upper left")
    ip, man = mf["_series"]
    a = ax[0, 1]
    base = pd.Timestamp("2019-12-01")
    for k, c in (("IPG3344S", "C0"), ("IPG334S", "C2"), ("IPG2211S", "C4"), ("IPMAN", "k")):
        s = ip[k].loc["2018":]
        a.plot(s.index, 100 * s / ip[k][base], color=c, label=IP[k] + ", output")
    s = man.loc["2018":]
    a.plot(s.index, 100 * s / man[base], color="C3", ls="--", label="manufacturing jobs")
    a.set_title("US manufacturing: output by industry and jobs (2019-12 = 100)"); a.legend(fontsize=8)
    sh = bo["_sh"]
    a = ax[1, 0]
    for k, c in zip(sh.columns, ("C0", "C2", "C4", "C3", "k")):
        a.plot(sh.index, sh[k], color=c, lw=2 if k == "net" else 1.2, label="net of imports" if k == "net" else k)
    a.axvline(pd.Timestamp("2022-11-30"), color="grey", lw=0.8, ls=":")
    a.set_xlim(pd.Timestamp("2015-01-01"), sh.index[-1])
    a.set_title("The AI build-out, % of GDP: investment less computer imports (ChatGPT dotted)"); a.legend(fontsize=7.5)
    m, peak = wg["_m"], wg["_peak"]
    a = ax[1, 1]
    mm = m.loc["2022":]
    for k, c in (("employment_rate", "C0"), ("participation", "C2"), ("unemployment", "C3")):
        a.plot(mm.index, mm[k] - m.loc[peak, k], color=c, label=k.replace("_", " ") + ", change since the peak")
    a.axvline(peak, color="grey", lw=0.8, ls=":"); a.axhline(0, color="grey", lw=0.8)
    a.set_title("US prime-age (25-54): where lost employment goes (points, 3-month averages)"); a.legend(fontsize=8)
    fig.text(0.01, 0.005, "BLS productivity and labour force, Federal Reserve industrial production, BEA investment and imports, Atlanta Fed GDPNow; all via FRED. "
             "Data-centre buildings are not in the build-out measure (annual office structures only).", fontsize=7.5)
    fig.savefig(os.path.join(ROOT, "figures", "fig_decoupling.png"), dpi=120)


if __name__ == "__main__":
    main()
