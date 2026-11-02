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
rcParams["mathtext.fontset"] = "dejavuserif"
rcParams["pdf.fonttype"] = 42          # TrueType in the PDF: fonts embedded
# 2026-11-02, typography pass: the figure is drawn at the width it prints,
# 0.88\textwidth in main.tex (16 cm text width), so sizes here are printed sizes:
# ticks and annotations 8 pt, axis labels 8.5 pt. Line widths, tick lengths and
# arrow heads are the earlier values (an 8.5 in canvas) times 0.654, the scale
# they printed at, so the plot keeps its weight on the page.
PRINT_W = 0.88 * 16 / 2.54             # inches
rcParams["font.size"] = 8.5
rcParams["xtick.labelsize"] = rcParams["ytick.labelsize"] = 8
rcParams["axes.linewidth"] = 0.52
for _ax in ("xtick", "ytick"):
    rcParams[f"{_ax}.major.width"] = 0.52
    rcParams[f"{_ax}.major.size"] = 2.3

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

# the earlier 8.6 x 4.6 in canvas saved at 8.48 x 4.48 in; the aspect is kept
fig, ax = plt.subplots(figsize=(PRINT_W, PRINT_W / 1.894), layout="constrained")
ax.plot(xo, rho, color=NAVY, lw=1.7, label="relative human productivity γ(x)")
ax.annotate("", xy=(M_CLOSED, YTOP), xytext=(M_CLOSED, float(rho[-1])),
            arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.05, ls="--",
                            shrinkA=0, shrinkB=0, mutation_scale=7.8))
ax.axhline(wc, color=RED, lw=1.05, ls="--")
ax.axvline(xstar, color="#666666", lw=0.65, ls=":")
ax.fill_between(xo, 0, rho, where=xo <= xstar, color=GRAY, alpha=0.35)
ax.fill_between(xo, 0, rho, where=xo >= xstar, color=BLUE, alpha=0.18)
ax.axvspan(M_CLOSED, 1.0, color=BLUE, alpha=0.10, lw=0)
# labels per her 2026-09-02 ruling on the editorial sheet: short, sentence
# case, mathtext; the argument lives in the caption, not the plot. The ratio is
# w/p_m, the paper's notation for the machine rental (was w/c); label positions
# as in the SSRN figure (2026-09-23), paper/figures/ssrn/fig_schedule.png, sizes
# from the typography pass, which breaks the H label over two lines to stay
# in H and centers the Labor label between x* and the wall (was x = 0.59)
ax.annotate("$w/p_m$", xy=(0.025, wc + 0.12), color=RED, fontsize=8)
ax.annotate("$x^*$", xy=(xstar + 0.008, 0.18), color="#444444", fontsize=8)
ax.annotate(r"Machines: $\gamma(x) < w/p_m$",
            xy=(0.235, 0.16), ha="center", fontsize=8, color="#555555")
ax.annotate(r"Labor: $\gamma(x) > w/p_m$",
            xy=(0.575, 0.95), ha="center", fontsize=8, color=NAVY)
ax.annotate("$H$: tasks closed\nto machines",
            xy=(0.85, 2.55), ha="center", fontsize=8, color="#555555")
ax.set_xlabel(r"Tasks $x$, ordered by increasing $\gamma$; closed tasks last")
ax.set_ylabel(r"Relative human productivity $\gamma(x)$")
ax.set_xlim(0, 1.0); ax.set_ylim(0, YTOP)
ax.grid(alpha=0.25, lw=0.33)
ax.spines[["top", "right"]].set_visible(False)
OUT = Path(__file__).resolve().parents[1] / "paper" / "figures" / "fig_schedule.png"
fig.savefig(OUT, dpi=300)
fig.savefig(OUT.with_suffix(".pdf"), metadata={"CreationDate": None})
print(f"wrote {OUT} and {OUT.with_suffix('.pdf').name}")

