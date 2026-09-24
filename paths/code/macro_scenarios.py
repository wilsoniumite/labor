# macro_scenarios.py — the macro block run through to curves: deep automation at three speeds.
#
# The calibrated normal case (macro.calibrate) along a technology path that takes capability eta from
# 1 to 0.04 and the labour in a machine-service hour from 0.05 to 0.01, over 15 years, at three speeds
# of the technology clock: slow (centred year 10, 12 years wide), medium (year 6, 6 wide), fast (year 3,
# 2 wide). Bridges at their defaults — illustrative coefficients, not estimates. The curves come from
# macro.curve_path: a stepwise central bank, a market learning the destination with a one-year half-life.
#
# Run from paths/:  ../venv/Scripts/python.exe code/macro_scenarios.py
# Out: results/macro_scenarios.json, figures/fig_macro_scenarios.png

from __future__ import annotations

import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import curve as cv  # noqa: E402
import macro as m  # noqa: E402
import sovereign as sv  # noqa: E402

SPEEDS = {"slow": m.TechPath(eta_end=0.04, lam_end=0.01, t_mid=10, width=12),
          "medium": m.TechPath(eta_end=0.04, lam_end=0.01, t_mid=6, width=6),
          "fast": m.TechPath(eta_end=0.04, lam_end=0.01, t_mid=3, width=2)}
T = np.array([1 / 12, 0.25, 0.5, 1, 2, 3, 5, 7, 10, 20, 30])
DATES = (0.0, 3.0, 6.0, 10.0)
NL = chr(10)


def main():
    e0, _, _, _ = m.calibrate()
    runs = {k: m.macro_path(e0, tp) for k, tp in SPEEDS.items()}
    out = {"calibration": {k: float(getattr(e0, k)) for k in ("T", "h", "chi_max", "k", "g0", "g1", "a", "b", "lam")}, "scenarios": {}}
    for k, mp in runs.items():
        states, sovs, pol = m.curve_path(mp)
        at = {d: int(np.argmin(np.abs(mp["t"] - d))) for d in DATES}
        out["scenarios"][k] = {
            "labour_share": {d: round(float(mp["labor_share"][i]), 3) for d, i in at.items()},
            "real_wage": {d: round(float(mp["real_wage"][i]), 3) for d, i in at.items()},
            "participation": {d: round(float(mp["participation"][i]), 3) for d, i in at.items()},
            "r_star": {d: round(float(mp["r_star"][i]), 2) for d, i in at.items()},
            "policy": {d: round(float(pol[i]), 2) for d, i in at.items()},
            "debt": {d: round(float(mp["debt"][i]), 1) for d, i in at.items()},
            "ois_curve": {d: [round(float(z), 3) for z in cv.zero(T, states[i])] for d, i in at.items()},
            "gov_spread": {d: [round(float(z), 3) for z in sv.spread(T, sovs[i])] for d, i in at.items()}}
        runs[k]["_states"], runs[k]["_policy"] = states, pol
        print(f"{k:7s} labour share " + " ".join(f"{v:.2f}" for v in out['scenarios'][k]['labour_share'].values())
              + " | real wage " + " ".join(f"{v:.2f}" for v in out['scenarios'][k]['real_wage'].values())
              + " | r* " + " ".join(f"{v:+.2f}" for v in out['scenarios'][k]['r_star'].values())
              + " | policy " + " ".join(f"{v:.2f}" for v in out['scenarios'][k]['policy'].values())
              + " | debt " + " ".join(f"{v:.0f}" for v in out['scenarios'][k]['debt'].values()))
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, "results", "macro_scenarios.json"), "w", encoding="utf-8"), indent=1)
    figure(runs)


def figure(runs):
    SPEED_C = {"slow": "#1baf7a", "medium": "#2a78d6", "fast": "#eb6834"}
    FORK_C = {"goods": "#008300", "shelter": "#e87ba4", "wages": "#eda100"}
    RAMP = ("#b7d3f6", "#6da7ec", "#2a78d6", "#104281")
    INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9.5, "axes.edgecolor": GRID,
                         "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
                         "axes.titlesize": 10.5, "axes.titleweight": "bold", "axes.titlecolor": INK,
                         "axes.titlelocation": "left"})
    fig, ax = plt.subplots(2, 3, figsize=(15, 8.6), facecolor=SURF)
    for a in ax.flat:
        a.set_facecolor(SURF); a.grid(True, color=GRID, lw=0.8); a.set_axisbelow(True)
        for s in ("top", "right"):
            a.spines[s].set_visible(False)
    panels = ((ax[0, 0], "labor_share", 100, "1. Labour's share of income", "%"),
              (ax[0, 1], "real_wage", 1, "2. What an hour's wage buys\nsupport baskets per hour", "baskets"),
              (ax[1, 0], "r_star", 1, "4. The neutral real rate\nbuild-out up, owners' saving down, deficits up", "%"),
              (ax[1, 1], "debt", 1, "5. Public debt", "% of income"))
    for a, key, scale, title, unit in panels:
        for k, mp in runs.items():
            a.plot(mp["t"], mp[key] * scale, color=SPEED_C[k], lw=2, label=f"{k} automation")
        a.set_title(title); a.set_ylabel(unit); a.set_xlabel("years")
        if key == "labor_share":                         # one legend: the speed colours are the same in panels 1, 2, 4, 5
            a.legend(frameon=False, fontsize=8.5, labelcolor=INK)
    ax[1, 0].axhline(0, color=INK2, lw=0.8)
    a = ax[0, 2]
    mp = runs["medium"]
    for key, lab in (("pi_goods", "goods"), ("pi_shelter", "shelter"), ("pi_wage", "wages")):
        a.plot(mp["t"], mp[key], color=FORK_C[lab], lw=2, label=lab)
    a.axhline(mp["pi_star"], color=INK2, lw=1, ls="--")
    a.text(14.8, mp["pi_star"] + 0.6, "the basket, on target", ha="right", fontsize=8.5, color=INK2)
    a.set_title("3. The fork, medium speed\ninflation with the basket held on target"); a.set_ylabel("% a year"); a.set_xlabel("years")
    a.legend(frameon=False, fontsize=8.5, labelcolor=INK, loc="upper right")
    a = ax[1, 2]
    for d, c in zip(DATES, RAMP):
        i = int(np.argmin(np.abs(mp["t"] - d)))
        a.plot(T, cv.zero(T, mp["_states"][i]), color=c, lw=2, marker="o", ms=3.5, label=f"year {d:g}: policy {mp['_policy'][i]:.2f}%")
    a.set_xscale("log"); a.set_xticks([1 / 12, 1, 2, 5, 10, 30]); a.set_xticklabels(["1M", "1Y", "2Y", "5Y", "10Y", "30Y"])
    a.set_title("6. The OIS curve along the medium path"); a.set_ylabel("zero rate, %")
    a.legend(frameon=False, fontsize=8.5, labelcolor=INK)
    fig.text(0.01, 0.005, "Calibrated normal case (labour 0.47, employment 0.60, 3 baskets per person, site 13% of the basket); capability 1 → 0.04, "
             "labour per machine-service hour 0.05 → 0.01. Bridge coefficients are illustrative defaults, not estimates.", fontsize=8, color=INK2)
    fig.tight_layout(rect=(0, 0.02, 1, 1))
    p = os.path.join(ROOT, "figures", "fig_macro_scenarios.png"); fig.savefig(p, dpi=150, facecolor=SURF); print(p)


def capital_figure():
    """(b): the capital-split calibration along the medium path; what a sustained +200 bp on the required
    return does; and the loop between the economy's real rate and automation."""
    from dataclasses import replace  # noqa: F401
    eb, sb, _, _ = m.calibrate(base=m.CAPITAL_BASE)
    tech = SPEEDS["medium"]
    fixed = m.macro_path(eb, tech)
    follow = m.macro_path(eb, tech, m.Bridges(capital_premium=5.0))
    shock = m.macro_path(eb, tech, m.Bridges(capital_premium=5.0, rho_shift=2.0))
    t = follow["t"]
    x_mid = float(np.interp(6.0, t, follow["x"]))
    delay_weeks = (float(np.interp(x_mid, shock["x"], t)) - 6.0) * 52
    split = {"labour": follow["labor_share"], "housing site": eb.h * follow["Y"] / follow["income"],
             "machine-chain land": eb.b * eb.delta * follow["X"] / follow["income"], "interest": follow["capital_share"]}
    res = {"calibration_b": {k: float(getattr(eb, k)) for k in ("T", "h", "chi_max", "k", "rho", "delta", "b")},
           "split_start": {k: round(float(v[0]), 3) for k, v in split.items()},
           "split_year15": {k: round(float(v[-1]), 3) for k, v in split.items()},
           "capital_output_start": round(float(sb["capital_output"]), 2),
           "shock_200bp": {"max_labour_share_pp": round(float(np.max(shock["labor_share"] - follow["labor_share"]) * 100), 2),
                           "max_tasks_pp": round(float(np.min(shock["x"] - follow["x"]) * 100), 2),
                           "delay_at_year6_weeks": round(delay_weeks, 1)},
           "loop_year15_tasks_ahead_pp": round(float((follow["x"] - fixed["x"])[-1] * 100), 2)}
    json.dump(res, open(os.path.join(ROOT, "results", "capital_feedback.json"), "w", encoding="utf-8"), indent=1)
    print("capital (b):", res["split_start"], "->", res["split_year15"], "| +200bp:", res["shock_200bp"], "| loop:", res["loop_year15_tasks_ahead_pp"])

    C = {"labour": "#2a78d6", "housing site": "#1baf7a", "machine-chain land": "#eb6834", "interest": "#e87ba4",
         "tasks": "#008300", "return": "#e87ba4"}
    INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.6), facecolor=SURF)
    for a in ax:
        a.set_facecolor(SURF); a.grid(True, color=GRID, lw=0.8); a.set_axisbelow(True); a.set_xlabel("years")
        for sp in ("top", "right"):
            a.spines[sp].set_visible(False)
    a = ax[0]
    nudge = {"interest": 6, "labour": -6}                 # the two end values sit a point apart
    for k, v in split.items():
        a.plot(t, v * 100, color=C[k], lw=2)
        a.annotate(k, (t[-1], v[-1] * 100), (4, nudge.get(k, 0)), textcoords="offset points", fontsize=8.5, color=INK, va="center")
    a.set_xlim(0, 19); a.set_xticks([0, 5, 10, 15])
    a.set_title("1. Who is paid, medium automation" + NL + "capital split out (b)"); a.set_ylabel("% of income")
    a = ax[1]
    a.plot(t, (shock["labor_share"] - follow["labor_share"]) * 100, color=C["labour"], lw=2, label="labour's share")
    a.plot(t, (shock["x"] - follow["x"]) * 100, color=C["tasks"], lw=2, label="tasks done by machines")
    a.axhline(0, color=INK2, lw=0.8)
    a.set_title("2. A sustained +200 bp on the required return" + NL
                + f"difference from no shock; delays automation ~{delay_weeks:.0f} weeks")
    a.set_ylabel("percentage points"); a.legend(frameon=False, fontsize=8.5, labelcolor=INK)
    a = ax[2]
    a.plot(t, follow["rho"] - fixed["rho"], color=C["return"], lw=2, label="required return, vs fixed")
    a.plot(t, (follow["x"] - fixed["x"]) * 100, color=C["tasks"], lw=2, label="tasks done by machines, vs fixed")
    a.axhline(0, color=INK2, lw=0.8)
    a.set_title("3. The loop: the return follows r*" + NL + "up in the build-out, down after")
    a.set_ylabel("percentage points"); a.legend(frameon=False, fontsize=8.5, labelcolor=INK)
    fig.text(0.01, 0.01, "Calibration (b): required return 5.75% (0.75% real + 5% premium), depreciation 8%; labour 0.47, employment 0.60, 3 baskets per person, "
             "site 13%; capital/income 2.98 (implied). Illustrative bridge defaults.", fontsize=8, color=INK2)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    p = os.path.join(ROOT, "figures", "fig_capital_feedback.png"); fig.savefig(p, dpi=150, facecolor=SURF); print(p)


if __name__ == "__main__":
    main()
    capital_figure()
