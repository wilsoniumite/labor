# complete_schedule.py — a candidate Figure 1 with every category the session arrived at, on Figure 1's printed
# schedule (gamma = 0.4 + 3.6 (x/0.7)^1.8, w/p_m = 2, H = [0.7, 1]):
#   machines (gamma < w/p_m); labor, contestable (w/p_m < gamma < 1/lam_m); labor behind the soft wall (gamma above
#   1/lam_m: machines could do it, but the machines would embody more labor than the task takes, so no wage makes them
#   cheaper); H (closed by law, preference or capability; a jump); and, beside the schedule on the same gamma axis, the
#   latent reservoir: tasks of goods nobody buys at cost, which would switch on with people above w/p_m and with
#   machines below it.
# The soft wall is drawn where Appendix B's shares put it, 1/theta = 1.70 times the margin's gamma (w/p_m can never
# rise above it), so here at 3.40.
# Run from walls/:  python code/complete_schedule.py
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import model as m  # noqa: E402

rcParams["font.family"] = "serif"
rcParams["font.serif"] = ["DejaVu Serif", "Georgia"]
rcParams["mathtext.fontset"] = "dejavuserif"
rcParams["font.size"] = 8.5
rcParams["xtick.labelsize"] = rcParams["ytick.labelsize"] = 8
NAVY, BLUE, RED, GRAY, BROWN = "#1a1a3d", "#4878b8", "#8b2020", "#c8c8c8", "#8a6d3b"

M, WC, YTOP = 0.70, 2.0, 5.2
CAP = WC * m.soft_wall_multiple()                         # 3.40
g = lambda x: 0.4 + 3.6 * (x / M) ** 1.8                    # noqa: E731
inv = lambda y: M * ((y - 0.4) / 3.6) ** (1 / 1.8)          # noqa: E731
xstar, xc = inv(WC), inv(CAP)
xs = np.linspace(0, M, 600, endpoint=False)
ys = g(xs)

fig, (ax, axr) = plt.subplots(1, 2, figsize=(0.88 * 16 / 2.54 * 1.15, 3.2), layout="constrained",
                              gridspec_kw=dict(width_ratios=[4.2, 1.0], wspace=0.02), sharey=True)
ax.plot(xs, ys, color=NAVY, lw=1.7, zorder=3)
ax.annotate("", xy=(M, YTOP), xytext=(M, float(g(M))),
            arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.05, ls="--", shrinkA=0, shrinkB=0, mutation_scale=7.8))
ax.axhline(WC, color=RED, lw=1.05, ls="--")
ax.axhline(CAP, color=BROWN, lw=0.9, ls=(0, (2, 1.5)))
for xv in (xstar, xc):
    ax.axvline(xv, color="#666666", lw=0.6, ls=":")
ax.fill_between(xs, 0, ys, where=xs <= xstar, color=GRAY, alpha=0.35, lw=0)
ax.fill_between(xs, 0, ys, where=(xs >= xstar) & (xs <= xc), color=BLUE, alpha=0.20, lw=0)
ax.fill_between(xs, 0, ys, where=xs >= xc, color=BROWN, alpha=0.16, lw=0)
ax.axvspan(M, 1.0, color=BLUE, alpha=0.10, lw=0)
ax.annotate("$w/p_m$", xy=(0.02, WC + 0.12), color=RED, fontsize=8)
ax.annotate(r"$1/\widetilde\lambda_m$: $w/p_m$ cannot rise above this", xy=(0.02, CAP + 0.12), color=BROWN, fontsize=7.5)
ax.annotate("$x^*$", xy=(xstar + 0.006, 0.12), color="#444444", fontsize=8)
ax.annotate("$x_c$", xy=(xc + 0.006, 0.12), color="#444444", fontsize=8)
ax.annotate("Machines", xy=(0.22, 0.55), ha="center", fontsize=8, color="#555555")
ax.annotate("Labor:\ncontestable", xy=(0.54, 0.55), ha="center", fontsize=7.5, color=NAVY)
ax.annotate("Labor: machines\ncould, at no wage", xy=(0.668, 2.55), ha="center", fontsize=7, color=BROWN,
            rotation=90, va="center")
ax.annotate("$H$: law,\npreference,\ncapability", xy=(0.85, 2.3), ha="center", fontsize=8, color="#555555")
ax.set_xlabel(r"Tasks of produced goods $x$, ordered by $\gamma$; closed tasks last")
ax.set_ylabel(r"Relative human productivity $\gamma$")
ax.set_xlim(0, 1.0)
ax.set_ylim(0, YTOP)
ax.grid(alpha=0.25, lw=0.33)
ax.spines[["top", "right"]].set_visible(False)
# the latent reservoir, on the same gamma axis: an illustrative density (lognormal around the margin)
yy = np.linspace(0.02, YTOP, 400)
dens = np.exp(-0.5 * ((np.log(yy) - np.log(2.6)) / 0.55) ** 2) / yy
dens /= dens.max()
axr.fill_betweenx(yy, 0, dens, where=yy <= WC, color=GRAY, alpha=0.55, lw=0)
axr.fill_betweenx(yy, 0, dens, where=yy >= WC, color=BLUE, alpha=0.35, lw=0)
axr.plot(dens, yy, color="#555555", lw=0.8)
axr.axhline(WC, color=RED, lw=1.05, ls="--")
axr.axhline(CAP, color=BROWN, lw=0.9, ls=(0, (2, 1.5)))
axr.annotate("would switch\non with\npeople", xy=(0.55, 3.0), ha="center", fontsize=7, color=NAVY)
axr.annotate("would switch\non with\nmachines", xy=(0.55, 0.75), ha="center", fontsize=7, color="#555555")
axr.set_xlim(0, 1.25)
axr.set_xticks([])
axr.set_xlabel("latent tasks\n(goods not bought)", fontsize=7.5)
axr.spines[["top", "right"]].set_visible(False)
fig.savefig(HERE.parent / "figures" / "complete_schedule.png", dpi=200)
print(f"x* {xstar:.3f}, soft wall at gamma {CAP:.2f} -> x_c {xc:.3f}, H from {M}; wrote figures/complete_schedule.png")
