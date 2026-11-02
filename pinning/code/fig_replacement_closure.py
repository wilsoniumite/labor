# fig_replacement_closure.py — Figure 2 of the paper: the replacement closure,
# Proposition 2, equation (5): w/r = gamma(x*) b_m / (1 - gamma(x*) lambda_m),
# with b_m and lambda_m the full-chain (tilde) requirements of a machine-hour.
# Drawn against gamma(x*) with b_m = 1 at two fixed values of lambda_m, 0.3 and
# 0 (the line w/r = gamma(x*) b_m). From A, task automation moves the economy
# along its curve (gamma(x*) falls); recursive automation moves it down to the
# line (lambda_m falls). Pure schematic, no data: the curves are the formula,
# the values illustrative. Written 2026-11-02 to reproduce the SSRN figure
# (paper/figures/ssrn/fig_replacement_closure.png), which had no script here.
# Run from pinning/:  ../venv/Scripts/python.exe code/fig_replacement_closure.py
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
# ticks, legend and annotations 8 pt, axis labels and the point label 8.5 pt. Line
# widths, marker, tick and arrow sizes are the earlier values (an 8.4 in canvas)
# times 0.663, the scale they printed at, so the plot keeps its weight on the page.
PRINT_W = 0.88 * 16 / 2.54             # inches
rcParams["font.size"] = 8.5
rcParams["xtick.labelsize"] = rcParams["ytick.labelsize"] = 8
rcParams["axes.linewidth"] = 0.53
for _ax in ("xtick", "ytick"):
    rcParams[f"{_ax}.major.width"] = 0.53
    rcParams[f"{_ax}.major.size"] = 2.3

NAVY, BLUE, RED, GRAY = "#1a1a3d", "#4878b8", "#8b2020", "#c8c8c8"

B_M = 1.0                              # full-chain non-produced input per machine-hour
LAM_M = 0.3                            # full-chain labor in a machine-hour, the upper curve
G_A = 1.5                              # gamma(x*) at A
G_TASK = 0.95                          # gamma(x*) after task automation
XMAX, YTOP = 2.0, 4.5


def closure(g, lam):
    """Equation (5): w/r at the margin, under 1 - gamma(x*) lambda_m > 0."""
    g = np.asarray(g, dtype=float)
    assert np.all(1 - g * lam > 0), "closure undefined: gamma * lambda_m >= 1"
    return g * B_M / (1 - g * lam)


g = np.linspace(0, XMAX, 400)
wr_a = float(closure(G_A, LAM_M))
wr_task = float(closure(G_TASK, LAM_M))
wr_rec = float(closure(G_A, 0.0))
# the picture's claims, checked on the formula: w/r rises with gamma(x*) and
# with lambda_m, and lambda_m = 0 is the line w/r = gamma(x*) b_m
assert np.all(np.diff(closure(g, LAM_M)) > 0)
assert np.all(closure(g[1:], LAM_M) > closure(g[1:], 0.0))
assert np.allclose(closure(g, 0.0), g * B_M)
assert wr_task < wr_a and wr_rec < wr_a

# the earlier 8.6 x 4.6 in canvas saved at 8.36 x 4.48 in; the aspect is kept
fig, ax = plt.subplots(figsize=(PRINT_W, PRINT_W / 1.866), layout="constrained")
ax.plot(g, closure(g, LAM_M), color=NAVY, lw=1.73,
        label=r"$\widetilde{\lambda}_m = 0.3$")
ax.plot(g, closure(g, 0.0), color=BLUE, lw=1.46,
        label=r"$\widetilde{\lambda}_m = 0$ (machines made by machines)")
ax.annotate("", xy=(G_TASK, wr_task), xytext=(G_A, wr_a),
            arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=0.93,
                            connectionstyle="arc3,rad=0.2",
                            shrinkA=4, shrinkB=0, mutation_scale=9.3))
ax.annotate("", xy=(G_A, wr_rec), xytext=(G_A, wr_a),
            arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=0.93,
                            shrinkA=4, shrinkB=0, mutation_scale=9.3))
ax.plot(G_A, wr_a, "o", color=NAVY, ms=5, mec="white", mew=1.0, zorder=5)
ax.annotate("A", xy=(G_A - 0.055, wr_a + 0.21), ha="center", va="center",
            fontsize=8.5, fontweight="bold", color=NAVY)
# labels short, sentence case, mathtext; the argument lives in the caption
ax.annotate("Task automation:\n" r"$\gamma(x^*)$ falls",
            xy=(0.99, 2.37), ha="right", va="center", fontsize=8, color=NAVY)
ax.annotate("Recursive automation:\n" r"$\widetilde{\lambda}_m$ falls",
            xy=(1.55, 2.13), ha="left", va="center", fontsize=8, color=NAVY)
ax.annotate(r"$w/r = \gamma(x^*)\,\widetilde{b}_m$", xy=(1.97, 1.31),
            ha="right", va="center", fontsize=8, color="#555555")
leg = ax.legend(loc="upper left", frameon=False, fontsize=8,
                title="Full-chain labor in a machine-hour", title_fontsize=8,
                alignment="left")
leg.get_title().set_color("#555555")
ax.set_xlabel(r"Relative human productivity at the marginal task, $\gamma(x^*)$")
ax.set_ylabel(r"Wage–rent ratio $w/r$")
ax.set_xlim(0, XMAX); ax.set_ylim(0, YTOP)
ax.set_xticks([0.0, 0.5, 1.0, 1.5, 2.0])
ax.set_yticks([0, 1, 2, 3, 4])
ax.grid(alpha=0.25, lw=0.33)
ax.spines[["top", "right"]].set_visible(False)
OUT = Path(__file__).resolve().parents[1] / "paper" / "figures" / "fig_replacement_closure.png"
fig.savefig(OUT, dpi=300)
fig.savefig(OUT.with_suffix(".pdf"), metadata={"CreationDate": None})
print(f"wrote {OUT} and {OUT.with_suffix('.pdf').name}")
