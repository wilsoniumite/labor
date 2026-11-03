# fig_labor_market_clearing.py — Figure 3 of the paper: labor-market clearing in the numerical economy of Appendix B
# (the SSRN version's instance, in the flow benchmark; solved by code/appendix_b.py). It redraws the SSRN figure
# (paper/figures/ssrn/fig_labor_market_clearing.png) from the model: the participation curve N_a/N = F(log(1 + w/P_s)),
# F uniform on [0, 1], with support and preferences fixed; and labor demand n_D/N against w/P_s as the task margin moves
# over [0, 1], at baseline, under recursive automation (lambda = 0: no labor in the machine chain) and under task
# automation (gamma halved at every task), each equilibrium marked.
# Run from pinning/:  python3 code/fig_labor_market_clearing.py
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rcParams

sys.path.insert(0, str(Path(__file__).resolve().parent))
import appendix_b as B  # noqa: E402

# Typography as Figures 1 and 2 after the 2026-11-02 pass (code/fig_schedule.py, code/fig_replacement_closure.py): the
# model figures' DejaVu Serif, TrueType embedded; drawn at the width it prints, 0.88\textwidth of the 16 cm text width,
# so sizes here are printed sizes: ticks, legend and annotation 8 pt, axis labels 8.5 pt. Line widths, markers and the
# arrow are the SSRN figure's (an 8.7 in canvas) times 0.634, the scale they print at.
rcParams["font.family"] = "serif"
rcParams["font.serif"] = ["DejaVu Serif", "Georgia"]
rcParams["mathtext.fontset"] = "dejavuserif"
rcParams["pdf.fonttype"] = 42          # TrueType in the PDF: fonts embedded
PRINT_W = 0.88 * 16 / 2.54             # inches
rcParams["font.size"] = 8.5
rcParams["xtick.labelsize"] = rcParams["ytick.labelsize"] = 8
rcParams["axes.linewidth"] = 0.52
for _ax in ("xtick", "ytick"):
    rcParams[f"{_ax}.major.width"] = 0.52
    rcParams[f"{_ax}.major.size"] = 2.3

NAVY, BLUE, RED, LIGHT, GRAY = "#1a1a3d", "#4878b8", "#8b2020", "#8fa9d4", "#555555"
XMAX, YTOP = 0.8, 0.6                  # the SSRN figure's frame

P = B.PRINTED
eq = B.figure3(P)
curves = {name: B.demand_curve(B.scenario(P, name)) for name, _ in B.SCENARIOS}
na, rw = B.participation_curve(P, upto=XMAX)

# the picture's claims, checked before drawing: each marked point is on its demand curve and on the participation curve;
# demand falls as w/P_s rises along each curve; both automation channels lower w/P_s and N_a/N; every demand curve
# stays below the frame's top
for name, (nd, w, xs) in curves.items():
    e = eq[name]
    assert np.all(np.diff(nd) < 0) and np.all(np.diff(w) > 0), name
    assert abs(np.interp(e["real_wage"], w, nd) - e["participation"]) < 1e-4, name
    assert abs(np.expm1(P["chi_max"] * e["participation"]) - e["real_wage"]) < 1e-12, name
    assert w.max() < YTOP, name
for name in ("recursive", "task"):
    assert eq[name]["real_wage"] < eq["baseline"]["real_wage"] and eq[name]["participation"] < eq["baseline"]["participation"]
low = min(("recursive", "task"), key=lambda k: eq[k]["real_wage"])

# a little taller than the SSRN canvas (aspect 1.70 for its 1.894): at its printed 8 pt the legend no longer fits in the
# upper right beside the participation curve, so it sits in the lower right, under the task-automation curve
fig, ax = plt.subplots(figsize=(PRINT_W, PRINT_W / 1.70), layout="constrained")
ax.plot(na, rw, color=RED, lw=1.55, label="Participation (support and preferences fixed)", zorder=3)
style = {"baseline": dict(color=NAVY, lw=1.65, ls="-", label="Labor demand, baseline (Appendix B)"),
         "recursive": dict(color=BLUE, lw=1.4, ls=(0, (3.7, 1.6)), label=r"Labor demand, recursive automation: $\lambda=0$"),
         "task": dict(color=LIGHT, lw=1.4, ls=(0, (5.2, 1.6, 1.0, 1.6)), label=r"Labor demand, task automation: $\gamma$ halved")}
for name, (nd, w, xs) in curves.items():
    ax.plot(nd, w, zorder=2, **style[name])
for name, e in eq.items():
    ax.plot(e["participation"], e["real_wage"], "o", ms=5, mfc=style[name]["color"], mec="white", mew=0.8, zorder=6)
b, lo = eq["baseline"], eq[low]
ax.annotate("", xy=(lo["participation"] - 0.006, lo["real_wage"] + 0.020),
            xytext=(b["participation"] - 0.026, b["real_wage"] + 0.006),
            arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=0.76, connectionstyle="arc3,rad=0.25",
                            shrinkA=0, shrinkB=0, mutation_scale=7.5), zorder=5)
ax.text(0.190, 0.33, "Automation moves the\nequilibrium down the\nparticipation curve", ha="right", va="center",
        fontsize=8, color=GRAY, linespacing=1.1)
ax.set_xlim(0, XMAX)
ax.set_ylim(0, YTOP)
ax.set_yticks(np.arange(0, YTOP + 0.001, 0.1))
ax.set_xlabel(r"Participation $N_a/N$")
ax.set_ylabel(r"Real wage in baskets $w/P_s$")
ax.grid(alpha=0.25, lw=0.33)
ax.spines[["top", "right"]].set_visible(False)
ax.legend(loc="lower right", frameon=False, fontsize=8, handlelength=2.6, labelspacing=0.35)
OUT = Path(__file__).resolve().parents[1] / "paper" / "figures" / "fig_labor_market_clearing.png"
fig.savefig(OUT, dpi=300)
fig.savefig(OUT.with_suffix(".pdf"), metadata={"CreationDate": None})
print(f"wrote {OUT} and {OUT.with_suffix('.pdf').name}")
for name, e in eq.items():
    print(f"  {name:9s} w/P_s {e['real_wage']:.4f}  N_a/N {e['participation']:.4f}  x* {e['x']:.5f}")
