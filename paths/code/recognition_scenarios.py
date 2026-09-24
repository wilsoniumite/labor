# recognition_scenarios.py — when does the market wake up, what does the curve do, and a false dawn.
#
# The two worlds of recognition.worlds() (calibration (b), the return following r*): the status quo and
# medium deep automation. The market watches labour's share each quarter with noise sigma (pp).
# Outputs: recognition dates by noise and prior; a Monte Carlo over noise draws (sigma 1 pp, 500 seeds)
# for both truths — how late recognition can be, and how often noise alone makes the market believe in
# a new world that is not coming; the market curve through recognition; the jump still waiting; and a
# narrative shock (+3 log odds at year 1.5) under each truth.
#
# Run from paths/:  ../venv/Scripts/python.exe code/recognition_scenarios.py
# Out: results/recognition.json, figures/fig_recognition.png

from __future__ import annotations

import json
import os
import sys
from dataclasses import replace

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import curve as cv  # noqa: E402
import recognition as rc  # noqa: E402
import regimes as rg  # noqa: E402

T = np.array([1 / 12, 0.25, 0.5, 1, 2, 3, 5, 7, 10, 20, 30])
NL = chr(10)


def main():
    e, old, new = rc.worlds()
    t = old["t"]
    base = rc.Learning(sigma=1.0, p0=0.05)
    out = {"worlds": "calibration (b), return following r*; status quo vs medium deep automation (eta 1 -> 0.04)",
           "labour_share_pp": {str(y): [round(float(old['labor_share'][i] * 100), 1), round(float(new['labor_share'][i] * 100), 1)]
                               for y, i in ((y, int(np.argmin(np.abs(t - y)))) for y in (0, 2, 3, 4, 5, 6, 8))}}
    # 1. recognition dates, noiseless, by noise and prior
    table = {}
    for sig in (0.5, 1.0, 2.0, 4.0):
        for p0 in (0.01, 0.05, 0.2):
            p = rc.learn(old, new, replace(base, sigma=sig, p0=p0))
            c = [rc.crossing(t, p, L) for L in (0.1, 0.5, 0.9)]
            done = None if c[1] is None else float((new["labor_share"][0] - np.interp(c[1], t, new["labor_share"]))
                                                   / (new["labor_share"][0] - new["labor_share"][-1]))
            table[f"sigma {sig}, p0 {p0}"] = {"p_0.1": c[0], "p_0.5": c[1], "p_0.9": c[2], "fall_done_at_0.5": done}
    out["recognition_noiseless"] = table
    # 2. Monte Carlo over noise draws
    cross_new, false_dawn = [], 0
    for seed in range(500):
        pn = rc.learn(old, new, replace(base, seed=seed))
        cross_new.append(rc.crossing(t, pn, 0.5))
        po = rc.learn(old, new, replace(base, seed=10_000 + seed, truth="old"))
        false_dawn += bool(np.max(po) >= 0.5)
    cn = np.array([c for c in cross_new if c is not None])
    out["monte_carlo_sigma1"] = {"new_world_p50_date_percentiles_10_50_90": [round(float(q), 2) for q in np.percentile(cn, [10, 50, 90])],
                                 "never_crossed": 500 - len(cn),
                                 "status_quo_false_dawn_share": false_dawn / 500}
    # 3. the market curve through recognition
    p = rc.learn(old, new, base)
    mixes, olds, news, pol = rc.market_curves(old, new, p)
    zmix = np.array([rg.zero(T, mx) for mx in mixes])
    znew = np.array([cv.zero(T, s) for s in news])
    c10, c90 = rc.crossing(t, p, 0.1), rc.crossing(t, p, 0.9)
    i10, i90 = int(np.searchsorted(t, c10)), int(np.searchsorted(t, c90))
    out["recognition_window"] = {"from_year": round(c10, 2), "to_year": round(c90, 2),
                                 "curve_move_bp": {lab: round(float((zmix[i90, k] - zmix[max(i10 - 1, 0), k]) * 100), 1)
                                                   for lab, k in (("3M", 1), ("2Y", 4), ("10Y", 8), ("30Y", 10))}}
    jump = (znew - zmix) * 100
    out["jump_waiting_bp_max"] = {lab: round(float(jump[:, k][np.argmax(np.abs(jump[:, k]))]), 1) for lab, k in (("2Y", 4), ("10Y", 8), ("30Y", 10))}
    # 4. a narrative shock under each truth
    nar = {}
    for truth in ("new", "old"):
        pj = rc.learn(old, new, replace(base, truth=truth, jumps=((1.5, 3.0),)))
        mj, _, _, _ = rc.market_curves(old, new, pj)
        z10 = np.array([rg.zero(np.array([10.0]), mx)[0] for mx in mj])
        nar[truth] = {"p": pj, "z10": z10}
    i15 = int(np.argmin(np.abs(t - 1.5)))
    pk = int(np.argmax(nar["old"]["p"][i15:])) + i15
    back = rc.crossing(t[pk:], 1 - nar["old"]["p"][pk:], 0.9)
    out["narrative_shock"] = {"p_after_jump": round(float(nar["old"]["p"][i15]), 3),
                              "status_quo_10Y_move_at_peak_bp": round(float((nar["old"]["z10"][pk] - nar["old"]["z10"][i15 - 1]) * 100), 1),
                              "status_quo_p_back_below_0.1_year": back}
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, "results", "recognition.json"), "w", encoding="utf-8"), indent=1, default=str)
    for k, v in out.items():
        if k != "recognition_noiseless":
            print(k, v)
    figure(t, old, new, base, zmix, jump, p, cn, nar)


def figure(t, old, new, base, zmix, jump, p, cn, nar):
    OLD_C, NEW_C, MARKET = "#52514e", "#eb6834", "#2a78d6"
    RAMP4 = ("#b7d3f6", "#6da7ec", "#2a78d6", "#104281")
    MAT = {"2Y": "#1baf7a", "10Y": "#2a78d6", "30Y": "#eb6834"}
    INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9.5, "axes.edgecolor": GRID,
                         "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
                         "axes.titlesize": 10.5, "axes.titleweight": "bold", "axes.titlecolor": INK,
                         "axes.titlelocation": "left"})
    fig, ax = plt.subplots(2, 3, figsize=(15.5, 8.8), facecolor=SURF)
    for a in ax.flat:
        a.set_facecolor(SURF); a.grid(True, color=GRID, lw=0.8); a.set_axisbelow(True)
        for sp in ("top", "right"):
            a.spines[sp].set_visible(False)
    w = t <= 8
    a = ax[0, 0]
    a.fill_between(t[w], new["labor_share"][w] * 100 - base.sigma, new["labor_share"][w] * 100 + base.sigma, color=NEW_C, alpha=0.15, lw=0)
    a.plot(t[w], old["labor_share"][w] * 100, color=OLD_C, lw=2, label="status quo")
    a.plot(t[w], new["labor_share"][w] * 100, color=NEW_C, lw=2, label="new world (the truth), ± 1 pp noise")
    a.set_title("1. What the market watches" + NL + "labour's share of income, two worlds"); a.set_ylabel("%"); a.set_xlabel("years")
    a.legend(frameon=False, fontsize=8.5, labelcolor=INK, loc="lower left")
    a = ax[0, 1]
    for sig, c in zip((0.5, 1.0, 2.0, 4.0), RAMP4):
        a.plot(t[w], rc.learn(old, new, replace(base, sigma=sig))[w], color=c, lw=2, label=f"noise {sig:g} pp")
    a.set_title("2. When the market wakes up" + NL + "probability of the new world, prior 5%, noiseless data"); a.set_ylabel("probability"); a.set_xlabel("years")
    a.legend(frameon=False, fontsize=8.5, labelcolor=INK, loc="lower right")
    a = ax[0, 2]
    a.hist(cn, bins=np.arange(0, 8.01, 0.25), color=MARKET, edgecolor=SURF, linewidth=1)
    q = np.percentile(cn, [10, 50, 90])
    a.set_title("3. With noisy data: the date belief crosses one half" + NL + f"500 draws, noise 1 pp; 10/50/90%: {q[0]:.1f} / {q[1]:.1f} / {q[2]:.1f} yrs")
    a.set_xlabel("years"); a.set_ylabel("draws")
    a = ax[1, 0]
    for yr, c in zip((0.0, 2.5, 3.5, 10.0), RAMP4):
        i = int(np.argmin(np.abs(t - yr)))
        a.plot(T, zmix[i], color=c, lw=2, marker="o", ms=3.5, label=f"year {yr:g}: p = {p[i]:.2f}")
    a.set_xscale("log"); a.set_xticks([1 / 12, 1, 2, 5, 10, 30]); a.set_xticklabels(["1M", "1Y", "2Y", "5Y", "10Y", "30Y"])
    a.set_title("4. The market's curve through recognition" + NL + "noise 1 pp, prior 5%"); a.set_ylabel("zero rate, %")
    a.legend(frameon=False, fontsize=8.5, labelcolor=INK)
    a = ax[1, 1]
    for lab, k in (("2Y", 4), ("10Y", 8), ("30Y", 10)):
        a.plot(t[w], jump[w, k], color=MAT[lab], lw=2, label=lab)
    a.axhline(0, color=INK2, lw=0.8)
    a.set_title("5. The jump still waiting" + NL + "if the truth were revealed that day"); a.set_ylabel("bp"); a.set_xlabel("years")
    a.legend(frameon=False, fontsize=8.5, labelcolor=INK)
    a = ax[1, 2]
    a.plot(t[w], nar["new"]["p"][w], color=NEW_C, lw=2, label="truth: new world")
    a.plot(t[w], nar["old"]["p"][w], color=OLD_C, lw=2, label="truth: status quo — a false dawn")
    a.axvline(1.5, color=INK2, lw=0.8, ls=":")
    a.set_title("6. A narrative shock at year 1.5 (+3 log odds)" + NL + "probability of the new world under each truth"); a.set_ylabel("probability"); a.set_xlabel("years")
    a.legend(frameon=False, fontsize=8.5, labelcolor=INK, loc="center right")
    fig.text(0.01, 0.005, "Worlds: calibration (b), required return following r*; new world = capability 1 → 0.04 at medium speed. Bayesian learning on "
             "quarterly labour-share data. Bridge coefficients are illustrative defaults.", fontsize=8, color=INK2)
    fig.tight_layout(rect=(0, 0.02, 1, 1))
    pth = os.path.join(ROOT, "figures", "fig_recognition.png"); fig.savefig(pth, dpi=150, facecolor=SURF); print(pth)


if __name__ == "__main__":
    main()
