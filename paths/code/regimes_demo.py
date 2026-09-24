# regimes_demo.py — what "the world waking up" looks like on a curve, with stylised numbers.
#
# Illustrative only: every state below is chosen, not calibrated. A status quo (policy 2%, heading
# for 2.75%) against two candidate new worlds the paper's mechanism points to — a higher-rate world
# (capex demand and fiscal strain raise the destination and the term premium) and a lower-rate world
# (wage-financed demand shrinks, policy is cut). Four panels: recognition toward each world (the
# market's eventual probability p rises; arrival hazard h = 0.5/yr), two worlds hidden in one calm
# curve, and where recognition bites along the curve for different hazards.
#
# Run from paths/:  ../venv/Scripts/python.exe code/regimes_demo.py
# Out: figures/fig_regimes_demo.png

from __future__ import annotations

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
import regimes as rg  # noqa: E402

STATUS_QUO = cv.CurveState(r0=2.0, m0=2.5, rbar=2.75, k1=1.0, k2=0.3, tp=0.4, delay=1 / 12)
HIGHER = replace(STATUS_QUO, m0=4.0, rbar=4.5, tp=1.3)                 # capex demand, fiscal strain
LOWER = replace(STATUS_QUO, m0=0.5, rbar=1.0, k1=1.5)                  # wage-financed demand shrinks
H = 0.5
T = np.geomspace(1 / 12, 30, 80)


def main():
    MARKET, HIGH_C, LOW_C = "#2a78d6", "#eb6834", "#1baf7a"     # colour follows the entity in every panel
    INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
    SQ = INK2                                                     # the status quo: a neutral reference line
    RAMP = ("#86b6ef", "#2a78d6", "#104281")                      # ordered hazards: one hue, light to dark
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9.5, "axes.edgecolor": GRID,
                         "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
                         "axes.titlesize": 10.5, "axes.titleweight": "bold", "axes.titlecolor": INK,
                         "axes.titlelocation": "left"})
    fig, ax = plt.subplots(2, 2, figsize=(13, 8.6), facecolor=SURF)
    for a in ax.flat:
        a.set_facecolor(SURF); a.grid(True, color=GRID, lw=0.8); a.set_axisbelow(True)
        for s in ("top", "right"):
            a.spines[s].set_visible(False)
        a.set_xscale("log"); a.set_xticks([1 / 12, 1, 2, 5, 10, 30]); a.set_xticklabels(["1M", "1Y", "2Y", "5Y", "10Y", "30Y"])

    for a, new, name, letter, col in ((ax[0, 0], HIGHER, "a higher-rate world", "1", HIGH_C),
                                      (ax[0, 1], LOWER, "a lower-rate world", "2", LOW_C)):
        a.plot(T, cv.zero(T, STATUS_QUO), color=SQ, lw=1.6, label="status quo")
        a.plot(T, cv.zero(T, new), color=col, lw=2, label=f"{name}, if it comes now")
        for pp, ls in ((0.3, "-"), (0.6, "--")):
            a.plot(T, rg.zero(T, rg.Arrival(STATUS_QUO, new, p=pp, h=H)), color=MARKET, lw=2, ls=ls,
                   label=f"market curve, p = {pp:.1f}")
        a.set_title(f"{letter}. Waking up to {name}\nthe market's probability p rises; arrival hazard 0.5/yr")
        a.set_ylabel("Zero rate, %")
        a.legend(frameon=False, fontsize=8.5, labelcolor=INK, loc="upper left" if new is HIGHER else "lower left")

    a = ax[1, 0]
    calm = rg.StaticMixture((HIGHER, LOWER), (0.5, 0.5))
    zc = rg.zero(T, calm)
    a.plot(T, cv.zero(T, HIGHER), color=HIGH_C, lw=2, label="a higher-rate world")
    a.plot(T, cv.zero(T, LOWER), color=LOW_C, lw=2, label="a lower-rate world")
    a.plot(T, zc, color=MARKET, lw=2.4, label="the curve the market shows (50/50)")
    for t_ in (2.0, 10.0):
        i = int(np.argmin(np.abs(T - t_)))
        up, dn = cv.zero(T[i], HIGHER) - zc[i], cv.zero(T[i], LOWER) - zc[i]
        a.annotate(f"{up*100:+.0f} / {dn*100:+.0f} bp", (T[i], zc[i]), (8, -4), textcoords="offset points",
                   fontsize=8.5, color=INK)
    a.set_title("3. Two worlds, one calm curve\nthe jump waiting in each resolution, at 2Y and 10Y")
    a.set_ylabel("Zero rate, %")
    a.legend(frameon=False, fontsize=8.5, labelcolor=INK, loc="upper left")

    a = ax[1, 1]
    for hh, c in zip((0.2, 1.0, 5.0), RAMP):
        rm = rg.recognition_mode(T, rg.Arrival(STATUS_QUO, HIGHER, p=0.3, h=hh))
        a.plot(T, rm * 10, color=c, lw=2, label=f"arrival hazard {hh:g}/yr (half-life {np.log(2)/hh:.1g} yr)")
    a.axhline(0, color=INK2, lw=0.8)
    a.set_title("4. Where recognition bites\ncurve move for a 10-point rise in p, toward the higher-rate world")
    a.set_ylabel("Change in zero rate, bp")
    a.legend(frameon=False, fontsize=8.5, labelcolor=INK, loc="upper left")

    fig.text(0.01, 0.005, "Illustrative: every state is chosen, not calibrated. Status quo: policy 2%, destination 2.75%, term premium 0.4%. "
             "Higher-rate world: destination 4.5%, term premium 1.3%. Lower-rate world: destination 1%, faster cuts.",
             fontsize=8, color=INK2)
    fig.tight_layout(rect=(0, 0.02, 1, 1))
    p = os.path.join(ROOT, "figures", "fig_regimes_demo.png")
    fig.savefig(p, dpi=150, facecolor=SURF)
    print(p)


if __name__ == "__main__":
    main()
