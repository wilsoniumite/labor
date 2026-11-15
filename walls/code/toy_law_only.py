# law_only_toy.py — scratch mock-up (not part of the paper): H set only by law, machines technically able to do every
# other task, technology changing only the schedule's shape. Three snapshots of the schedule under one legal wall:
# (a) in gamma units, with the machine chain's cap w/p_m < 1/lam_m; (b) in rent units through equation (5),
# v = gamma b_m / (1 - gamma lam_m), where the chain's wall is an asymptote at x_c (gamma(x_c) lam_m = 1).
# Run from walls/:  python code/toy_law_only.py
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

HERE = Path(__file__).resolve().parent
rcParams["font.family"] = "serif"
rcParams["font.serif"] = ["DejaVu Serif", "Georgia"]
rcParams["mathtext.fontset"] = "dejavuserif"
rcParams["font.size"] = 8.5
rcParams["xtick.labelsize"] = rcParams["ytick.labelsize"] = 8
rcParams["axes.linewidth"] = 0.52
for _ax in ("xtick", "ytick"):
    rcParams[f"{_ax}.major.width"] = 0.52
    rcParams[f"{_ax}.major.size"] = 2.3
PRINT_W = 0.88 * 16 / 2.54
NAVY, BLUE, RED, GRAY = "#1a1a3d", "#4878b8", "#8b2020", "#c8c8c8"

M = 0.85                     # the legal wall: H = [0.85, 1], closed by law in every snapshot
LAM, B = 0.3, 1.0            # Figure 2's full-chain labor and land in a machine-hour
CAP = 1 / LAM                # w/p_m stays below this at any wage
G_HI = 30.0                  # beyond the capability frontier machines are 30x worse than people, not useless
# (label, frontier f, gamma below the frontier, colour): machines improve, the frontier moves right and past the wall
SNAPS = [("early", 0.25, 0.30, "#9fb6d6"), ("later", 0.60, 0.25, BLUE), ("late", 1.30, 0.15, NAVY)]
S = 0.06                     # width of the frontier's climb


def gamma(x, f, glo):
    """A smooth climb in log gamma from glo to G_HI around the frontier f: finite everywhere."""
    return glo * (G_HI / glo) ** (1 / (1 + np.exp(-(x - f) / S)))


xs = np.linspace(0, M, 3000, endpoint=False)
fig, axs = plt.subplots(2, 1, figsize=(PRINT_W, 2 * (PRINT_W / 1.894 + 0.32)), layout="constrained")

ax = axs[0]
YT = 6.0
for lab, f, glo, col in SNAPS:
    g = gamma(xs, f, glo)
    assert np.all(np.diff(g) > 0) and np.all(np.isfinite(g))
    ax.plot(xs, np.minimum(g, YT + 1), color=col, lw=1.6, label=lab)
    if g.max() >= CAP:
        xc = float(np.interp(CAP, g, xs))
        ax.plot(xc, CAP, "o", ms=4, color=col, zorder=5)
    else:
        top = float(gamma(M, f, glo))
        ax.annotate("", xy=(M, YT), xytext=(M, top),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=1.0, ls="--", shrinkA=0, shrinkB=0, mutation_scale=7.8))
ax.axhline(CAP, color=RED, lw=0.9, ls=(0, (5, 2)))
ax.annotate(r"$1/\widetilde{\lambda}_m$: $w/p_m$ stays" "\nbelow this at any wage", xy=(0.30, CAP - 0.12), va="top", color=RED, fontsize=7.5)
ax.annotate("above the line: machines\ncan do the task, but not\nat any wage", xy=(0.31, 5.75), va="top", fontsize=7.5,
            color="#555555", ha="left")
ax.plot(M, 1.5, "o", ms=4.6, mfc="white", mec=NAVY, mew=1.1, zorder=6)
ax.annotate("late: once $w/p_m$ clears\nthe top, labor holds only $H$", xy=(M, 1.5), xytext=(0.835, 2.45), ha="right",
            va="center", fontsize=7.5, color=NAVY,
            arrowprops=dict(arrowstyle="->", color=NAVY, lw=0.59, mutation_scale=5.8, shrinkB=3))
ax.axvspan(M, 1.0, color=BLUE, alpha=0.10, lw=0)
ax.annotate("$H$: closed\nby law", xy=(0.925, 2.2), ha="center", fontsize=8, color="#555555")
ax.set_title("(a) H set only by law; machines can do every other task; only the schedule changes",
             loc="left", fontsize=8.5, color="#333333")
ax.set_ylabel(r"Relative human productivity $\gamma(x)$")
ax.set_xlabel(r"Tasks $x$, ordered by increasing $\gamma$; legally closed tasks last")
ax.legend(loc="upper left", frameon=False, fontsize=7.5, title="machines:", title_fontsize=7.5, alignment="left")
ax.set_xlim(0, 1.0)
ax.set_ylim(0, YT)
ax.grid(alpha=0.25, lw=0.33)
ax.spines[["top", "right"]].set_visible(False)

ax = axs[1]
VT = 12.0
for lab, f, glo, col in SNAPS:
    g = gamma(xs, f, glo)
    open_ = g < CAP
    xo, go = xs[open_], g[open_]
    if not open_.all():   # the chain's wall: dense points toward x_c so the asymptote draws
        xc = float(np.interp(CAP, g, xs))
        xo = xc * (1 - (1 - np.linspace(0, 1, 3000, endpoint=False)) ** 3)
        go = gamma(xo, f, glo)
        ax.plot([xc, xc], [0, VT], color=col, lw=0.8, ls=(0, (4, 2.5)))
        ax.annotate("$x_c$", xy=(xc + 0.008, 0.35), fontsize=8, color=col)
    v = go * B / (1 - go * LAM)
    ax.plot(xo, np.minimum(v, VT + 1), color=col, lw=1.6)
    if open_.all():
        ax.annotate("", xy=(M, VT), xytext=(M, float(v[-1])),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=1.0, ls="--", shrinkA=0, shrinkB=0, mutation_scale=7.8))
ax.axvspan(M, 1.0, color=BLUE, alpha=0.10, lw=0)
ax.annotate("$H$: closed\nby law", xy=(0.925, 5.5), ha="center", fontsize=8, color="#555555")
ax.annotate("the chain's wall:\nan asymptote that\nmoves right as\nmachines improve", xy=(0.40, 9.0), fontsize=7.5,
            color="#555555", ha="center", va="center")
ax.annotate("the legal\nwall: a jump", xy=(0.84, 3.0), fontsize=7.5, color=NAVY, ha="right")
ax.set_title("(b) The same schedules in rent units, through equation (5)", loc="left", fontsize=8.5, color="#333333")
ax.set_ylabel(r"$w/r$ at which labor and machines tie")
ax.set_xlabel(r"Tasks $x$, ordered by increasing $\gamma$; legally closed tasks last")
ax.set_xlim(0, 1.0)
ax.set_ylim(0, VT)
ax.grid(alpha=0.25, lw=0.33)
ax.spines[["top", "right"]].set_visible(False)
fig.savefig(HERE.parent / "figures" / "toy_law_only.png", dpi=200)
plt.close(fig)
for lab, f, glo, col in SNAPS:
    g = gamma(xs, f, glo)
    print(f"{lab[:5]}: top of the open schedule {g.max():.2f}; x_c = "
          f"{float(np.interp(CAP, g, xs)) if g.max() >= CAP else 'none (top below the cap)'}")
print("wrote toy_law_only.png")
