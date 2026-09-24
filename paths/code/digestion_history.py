# digestion_history.py — has the speed at which bond markets price news changed with technology?
#
# Her conjecture (2026-09-24): internet adoption and the like may have changed digestion speed before.
# A public test on US Treasury yields (FRED, daily constant-maturity 10Y from 1962, 2Y from 1976). If
# news is priced at once, daily yield changes are uncorrelated and the variance ratio
#     VR(q) = Var(q-day change) / (q Var(1-day change))
# is 1 at every horizon; if part of each move drifts in over the following weeks, VR(q) rises above 1
# with q; if prices overshoot and come back, it falls below 1. Estimated in rolling four-year windows
# and by era: wire services and telephones (1962–81); screens and futures (1982–94: Bloomberg's
# terminal 1982, Treasury note futures 1982); the internet and electronic interdealer trading
# (1995–2008: BrokerTec and eSpeed 1999–2000); algorithmic trading (2009–26).
#
# The partial-digestion reading used by the learner (recognition.Learning.digest, digest_share): a share
# f of each piece of news is priced at once, the rest drifts in with half-life h; VR(q) then rises
# from 1 toward about 1/f^2 over a few half-lives. Fitted for the 10Y by era.
#
# Confounds, stated: the Federal Reserve began announcing its decisions in February 1994 (before that
# the market inferred them, with delays); early constant-maturity quotes were staler; policy smoothing
# makes short-maturity changes persistent at horizons of months (so the 2Y at 3–6 months measures the
# Fed, not the market); 2009–15 sat at the lower bound. A second test — the 10Y's response over the
# weeks after the days the Fed's target moved — was run and is recorded as inconclusive: with the
# target change and the 3M bill standing in for the surprise, 31–99 events an era do not separate drift
# from noise.
#
# Run from paths/:  ../venv/Scripts/python.exe code/digestion_history.py
# Out: results/digestion_history.json, figures/fig_digestion_history.png

from __future__ import annotations

import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy.optimize import least_squares  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "..", "pinning", "code"))
import lambda_compute2 as _lc  # noqa: E402

_lc.CACHE = os.path.join(ROOT, "cache")
NL = chr(10)
ERAS = (("1962–81 wire and telephone", "1962", "1981"), ("1982–94 screens and futures", "1982", "1994"),
        ("1995–2008 internet, electronic trading", "1995", "2008"), ("2009–26 algorithmic", "2009", "2026"))
Q = (2, 3, 5, 10, 21, 42, 63, 126)
MILESTONES = ((1982.5, "Bloomberg terminal;" + NL + "note futures"), (1994.1, "Fed announces" + NL + "decisions"),
              (1999.5, "electronic" + NL + "Treasury trading"), (2023.0, "LLMs"))


def variance_ratio(x, q):
    """Lo–MacKinlay variance ratio with overlapping q-period sums."""
    x = np.asarray(x, float)
    x = x - x.mean()
    s1 = np.sum(x ** 2) / len(x)
    cs = np.concatenate([[0.0], np.cumsum(x)])
    sq = cs[q:] - cs[:-q]
    return float(np.sum(sq ** 2) / (len(sq) * q * s1))


def variance_ratio_z(x, q):
    """Heteroskedasticity-robust z statistic for VR(q) = 1 (Lo and MacKinlay 1988)."""
    x = np.asarray(x, float)
    x = x - x.mean()
    n = len(x)
    den = np.sum(x ** 2)
    theta = sum((2.0 * (q - j) / q) ** 2 * (np.sum(x[j:] ** 2 * x[:-j] ** 2) / den ** 2 * n) for j in range(1, q))
    return float((variance_ratio(x, q) - 1.0) / np.sqrt(theta / n))


def vr_partial(qs, f, h, J=3000):
    """VR(q) when a share f of each shock is priced at once and the rest drifts in with half-life h."""
    lam = 1.0 - 0.5 ** (1.0 / h)
    c = (1.0 - f) * lam * (1.0 - lam) ** np.arange(J)
    c[0] += f
    g = np.array([np.dot(c[:J - k], c[k:]) for k in range(max(qs))])
    return np.array([(q * g[0] + 2.0 * np.sum((q - np.arange(1, q)) * g[1:q])) / (q * g[0]) for q in qs])


def fit_partial(vr_obs, qs=Q):
    best = None
    for h0 in (1.0, 5.0, 15.0, 40.0):
        for f0 in (0.6, 0.9):
            r = least_squares(lambda th: vr_partial(qs, th[0], th[1]) - vr_obs, x0=[f0, h0], bounds=([0.3, 0.2], [1.0, 250.0]))
            if best is None or r.cost < best.cost:
                best = r
    return float(best.x[0]), float(best.x[1]), float(np.sqrt(2 * best.cost / len(qs)))


def event_test():
    """The 10Y's cumulative response h trading days after the days the Fed's target moved, regressed on
    that day's change in the 3M bill (a stand-in for the surprise), by era. Recorded, not relied on."""
    tar = pd.concat([_lc.pull_fred("DFEDTAR"), _lc.pull_fred("DFEDTARU")]).sort_index()
    ch = tar.diff()
    events = ch[ch.abs() > 1e-9].index
    y10, s3 = _lc.pull_fred("DGS10"), _lc.pull_fred("DGS3MO")
    idx = y10.index
    out = {}
    for name, a, b in ERAS[1:]:
        rows = []
        for ev in events:
            if not (pd.Timestamp(a) <= ev <= pd.Timestamp(b + "-12-31")):
                continue
            i = idx.searchsorted(ev)
            if i < 1 or i + 60 >= len(idx) or idx[i] != ev or ev not in s3.index or idx[i - 1] not in s3.index:
                continue
            rows.append([(s3[ev] - s3[idx[i - 1]]) * 100] + [(y10.iloc[i + h] - y10.iloc[i - 1]) * 100 for h in (0, 5, 20, 40, 60)])
        R = np.array(rows)
        out[name] = {"events": len(R), "slope_by_days_after_0_5_20_40_60":
                     [round(float(np.sum(R[:, 0] * R[:, k]) / np.sum(R[:, 0] ** 2)), 2) for k in range(1, 6)]}
    return out


def main():
    y = {s: _lc.pull_fred(s) for s in ("DGS10", "DGS2")}
    dy = {s: v.diff().dropna() * 100 for s, v in y.items()}
    out = {"source": "FRED DGS10 (1962-), DGS2 (1976-), daily; changes in bp", "eras": {}, "rolling_4y": {}}
    for s in ("DGS10", "DGS2"):
        out["eras"][s] = {}
        for name, a, b in ERAS:
            x = dy[s][a:b].values
            if len(x) < 1000:
                continue
            vr_obs = np.array([variance_ratio(x, q) for q in Q])
            row = {"n": len(x), "sd_bp": round(float(x.std()), 2),
                   "VR": {str(q): round(float(v), 3) for q, v in zip(Q, vr_obs)},
                   "z": {str(q): round(variance_ratio_z(x, q), 2) for q in (5, 21, 63)}}
            if s == "DGS10":
                f, h, rmse = fit_partial(vr_obs)
                row["partial_digestion_fit"] = {"priced_at_once": round(f, 2), "rest_half_life_days": round(h, 1),
                                                "rmse": round(rmse, 3),
                                                "usable": bool(rmse < 0.06 and f < 0.98)}
            out["eras"][s][name] = row
        rows = []
        first = int(dy[s].index[0].year) + 1
        for y0 in range(first, 2023):
            x = dy[s][str(y0):str(y0 + 3)].values
            if len(x) > 700:
                rows.append([y0 + 2.0, variance_ratio(x, 5), variance_ratio(x, 21), variance_ratio(x, 63)])
        out["rolling_4y"][s] = rows
    out["event_test"] = {"verdict": "inconclusive: no stable drift pattern across eras at these sample sizes",
                         "by_era": event_test()}
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, "results", "digestion_history.json"), "w", encoding="utf-8"), indent=1)
    for s, eras in out["eras"].items():
        for name, row in eras.items():
            print(s, name, row["VR"], row["z"], row.get("partial_digestion_fit", ""))
    figure(out, dy)


def figure(out, dy):
    INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
    TEN, TWO = "#2a78d6", "#1baf7a"
    ERA_C = ("#b7d3f6", "#6da7ec", "#2a78d6", "#104281")
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9.5, "axes.edgecolor": GRID,
                         "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
                         "axes.titlesize": 10.5, "axes.titleweight": "bold", "axes.titlecolor": INK,
                         "axes.titlelocation": "left"})
    fig, ax = plt.subplots(1, 3, figsize=(16, 5.4), facecolor=SURF, layout="constrained",
                           gridspec_kw={"width_ratios": [1.5, 1, 1]})
    fig.get_layout_engine().set(rect=(0, 0.05, 1, 0.95), w_pad=0.1)
    for a in ax:
        a.set_facecolor(SURF); a.grid(True, color=GRID, lw=0.8); a.set_axisbelow(True)
        for sp in ("top", "right"):
            a.spines[sp].set_visible(False)
    a = ax[0]
    for s, col in (("DGS10", TEN), ("DGS2", TWO)):
        r = np.array(out["rolling_4y"][s])
        a.plot(r[:, 0], r[:, 2], color=col, lw=2, label=f"{s[3:]}Y, over a month")
    a.axhline(1.0, color=INK2, lw=0.8)
    for k, (yr, lab) in enumerate(MILESTONES):
        a.axvline(yr, color=INK2, lw=0.8, ls=":")
        a.text(yr + 0.3, 2.62 if k % 2 == 0 else 2.3, lab, fontsize=7.5, color=INK2, va="top")
    a.set_ylim(0.5, 2.7)
    a.set_title("1. News used to drift into bond prices; since the mid-1990s it does not" + NL
                + "21-day variance ratio, rolling four-year windows; 1 = priced at once")
    a.set_xlabel("centre of the window"); a.set_ylabel("variance ratio")
    a.legend(frameon=False, fontsize=8.5, labelcolor=INK, loc="lower left")
    a = ax[1]
    for (name, _, _), col in zip(ERAS, ERA_C):
        row = out["eras"]["DGS10"][name]
        a.plot(Q, [row["VR"][str(q)] for q in Q], color=col, lw=2, marker="o", ms=4, label=name)
    a.axhline(1.0, color=INK2, lw=0.8)
    a.set_xscale("log"); a.set_xticks(Q); a.set_xticklabels([str(q) for q in Q])
    a.set_title("2. How long the 10Y kept moving after news" + NL + "variance ratio by horizon, by era")
    a.set_xlabel("horizon, trading days"); a.set_ylabel("variance ratio")
    a.legend(frameon=False, fontsize=8, labelcolor=INK, loc="upper left")
    a = ax[2]
    names = [n for n, _, _ in ERAS]
    zs = [out["eras"]["DGS10"][n]["z"]["21"] for n in names]
    a.bar(range(4), zs, color=ERA_C)
    a.axhline(0, color=INK2, lw=0.8)
    for lvl in (-1.96, 1.96):
        a.axhline(lvl, color=INK2, lw=0.8, ls="--")
    a.set_xticks(range(4)); a.set_xticklabels([n.split(" ")[0] for n in names], fontsize=8.5)
    fit = out["eras"]["DGS10"]["1982–94 screens and futures"]["partial_digestion_fit"]
    a.set_title("3. Drift, then none, then a little overshoot" + NL + "10Y, z of the 21-day ratio; dashed ±1.96")
    a.text(1, zs[1] / 2, f"{fit['priced_at_once']:.0%} at once," + NL + "rest half-life" + NL + f"{fit['rest_half_life_days']:.0f} days",
           ha="center", va="center", fontsize=8, color="white")
    a.set_ylabel("z")
    fig.text(0.01, 0.01, "FRED DGS10, DGS2 (constant-maturity par yields, daily). Confounds: the Fed's announcements from Feb 1994; staler early quotes; "
             "policy smoothing (the 2Y at months measures the Fed); the lower bound 2009–15.", fontsize=8, color=INK2)
    pth = os.path.join(ROOT, "figures", "fig_digestion_history.png"); fig.savefig(pth, dpi=150, facecolor=SURF); print(pth)


if __name__ == "__main__":
    main()
