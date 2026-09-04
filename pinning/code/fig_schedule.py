# fig_schedule.py — Figure 1 of the paper: the task-assignment schedule with the
# set H of tasks closed to machines drawn as a wall (Section 3). Pure schematic,
# no data. Carved from the three-schematic script fig_model_schematics.py on
# 2026-09-04 (the other two schematics belong to the dynamics thread).
# Run from pinning/:  ../venv/Scripts/python.exe code/fig_schedule.py
from pathlib import Path


import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams["font.family"] = "serif"
rcParams["font.serif"] = ["DejaVu Serif", "Georgia"]
rcParams["font.size"] = 11
rcParams["mathtext.fontset"] = "dejavuserif"

NAVY, BLUE, RED, GRAY = "#1a1a3d", "#4878b8", "#8b2020", "#c8c8c8"

# ---------------------------------------------------------------- schedule
# 2026-09-02 (her call): the industrial configuration is the template — a
# steep schedule over the tasks machines can reach, then the set H of tasks
# closed to machines (γ_M = 0, γ unbounded), relabeled last and drawn as a
# wall at the right edge. Labor holds H at any wage; the margin lies among
# the reachable tasks. The pre-wall version is in git history.
M_CLOSED = 0.70                      # [M_CLOSED, 1] is H
xo = np.linspace(0, M_CLOSED, 400, endpoint=False)
rho = 0.4 + 3.6 * (xo / M_CLOSED) ** 1.8
wc = 2.0
xstar = M_CLOSED * ((wc - 0.4) / 3.6) ** (1 / 1.8)
YTOP = 5.2

fig, ax = plt.subplots(figsize=(8.6, 4.6), dpi=150)
ax.plot(xo, rho, color=NAVY, lw=2.6, label="relative human productivity γ(x)")
ax.annotate("", xy=(M_CLOSED, YTOP), xytext=(M_CLOSED, float(rho[-1])),
            arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.6, ls="--",
                            shrinkA=0, shrinkB=0, mutation_scale=12))
ax.axhline(wc, color=RED, lw=1.6, ls="--")
ax.axvline(xstar, color="#666666", lw=1.0, ls=":")
ax.fill_between(xo, 0, rho, where=xo <= xstar, color=GRAY, alpha=0.35)
ax.fill_between(xo, 0, rho, where=xo >= xstar, color=BLUE, alpha=0.18)
ax.axvspan(M_CLOSED, 1.0, color=BLUE, alpha=0.10, lw=0)
# labels per her 2026-09-02 ruling on the editorial sheet: short, sentence
# case, mathtext; the argument lives in the caption, not the plot
ax.annotate("$w/c$", xy=(0.025, wc + 0.12), color=RED, fontsize=10.5)
ax.annotate("$x^*$", xy=(xstar + 0.008, 0.18), color="#444444", fontsize=10.5)
ax.annotate(r"Machines: $\gamma(x) < w/c$",
            xy=(0.215, 0.16), ha="center", fontsize=9.5, color="#555555")
ax.annotate(r"Labor: $\gamma(x) > w/c$",
            xy=(0.575, 0.95), ha="center", fontsize=9.5, color=NAVY)
ax.annotate("$H$: tasks closed to machines",
            xy=(0.85, 2.55), ha="center", fontsize=9.5, color="#555555")
ax.set_xlabel(r"Tasks $x$, ordered by increasing $\gamma$; closed tasks last")
ax.set_ylabel(r"Relative human productivity $\gamma(x)$")
ax.set_xlim(0, 1.0); ax.set_ylim(0, YTOP)
ax.grid(alpha=0.25, lw=0.5)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
OUT = Path(__file__).resolve().parents[1] / "paper" / "figures" / "fig_schedule.png"
fig.savefig(OUT, bbox_inches="tight")
print(f"wrote {OUT}")

