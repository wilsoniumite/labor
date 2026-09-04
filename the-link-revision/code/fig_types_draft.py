# fig_types_draft.py — CANDIDATE companion to the Figure 2 redraw, for the
# 2026-09-02 review: the schedule is person-specific (§6 "Heterogeneity";
# App A "Heterogeneous workers": type-specific schedules, every proposition
# type by type). Not referenced by the paper. Her call.
#
# The question it answers: can "being a good developer is a capability that
# cannot be trained, or takes years to train" be a differently shaped
# schedule? Reading in the model's objects:
#
# * A type i has γ_i(x) = γ_L,i(x)/γ_M(x): the machine side is common, the
#   human side is the person's. A type's task list also has its own closed
#   set (tasks machines cannot hold, App A's H, seen from that type).
# * An ORDINARY type in the computing era: routine tasks open, a plateau
#   near parity at its margin, a small wall (care, non-routine manual). Its
#   wage is pinned on the plateau (Lemma A.1).
# * A DEVELOPER type: the same routine region, but its specialty tasks are
#   closed to machines, so its wall comes early and its margin sits AT the
#   wall. Its wage is then not a machine price: at w_D it loses every open
#   task on cost (comparative advantage) and holds only wall tasks. w_D is a
#   price on the scarcity of the type against demand for its tasks — the
#   pre-industrial configuration, one person at a time.
# * Untrainable vs trainable is NOT a shape difference; it is the supply
#   side of the type. Fixed capability = no human entry ever: the type is a
#   terminal factor (J_H = ∞) and w_D carries a rent, like land. Trainable
#   with lag J_H = entrants arrive after the lag and the premium decays to
#   the training user cost over J_H — the ladder-of-lags logic of App E,
#   applied to a human build.
# * Either way the premium survives only while the type's tasks stay closed
#   to MACHINES. Untrainability protects against human entry, not machine
#   entry. Under AI the developer's wall moves right, the schedule flattens
#   to the same plateau as everyone's, and both wages sit at c·γ̄:
#   "flattening becomes general" across tasks AND across people.
# * The aggregate curve the paper draws for the computing era (flat bottom,
#   steep top) is what the envelope of these two types looks like — but the
#   envelope must be taken in cost units, γ_i divided by w_i/c, not raw γ_i,
#   or a high-wage type is assigned tasks it loses on cost.
#
# Pure schematic, no data.

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams["font.family"] = "serif"
rcParams["font.serif"] = ["DejaVu Serif", "Georgia"]
rcParams["font.size"] = 11

NAVY, BLUE, RED, GRAY = "#1a1a3d", "#4878b8", "#8b2020", "#c8c8c8"
YTOP = 3.4


def logistic(x, mid, width):
    return 1.0 / (1.0 + np.exp(-(x - mid) / width))


def curve(m, g):
    xs = np.linspace(0, m, 600, endpoint=False)
    return xs, g(xs)


def draw_wall(ax, x0, y0, color, lw=1.6):
    ax.annotate("", xy=(x0, YTOP), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, ls="--",
                                shrinkA=0, shrinkB=0, mutation_scale=12))


fig, axes = plt.subplots(1, 3, figsize=(13.2, 4.6), dpi=150, sharey=True)

# (a) ordinary type, computing era ------------------------------------------
ax = axes[0]
m, wc, xst = 0.85, 0.95, 0.70
xs, ys = curve(m, lambda x: 0.95 * logistic(x, 0.45, 0.06))
ax.plot(xs, ys, color=BLUE, lw=2.6)
draw_wall(ax, m, float(ys[-1]), BLUE)
ax.axvspan(m, 1.0, color=GRAY, alpha=0.22, lw=0)
ax.axhline(wc, color=RED, lw=1.3, ls="--")
ax.text(0.985, wc + 0.06, "w/c", color=RED, fontsize=9.5, ha="right")
ax.fill_between(xs, 0, ys, where=xs <= xst, color=GRAY, alpha=0.5, lw=0)
ax.fill_between(xs, 0, ys, where=xs >= xst, color=BLUE, alpha=0.18, lw=0)
ax.axvline(xst, color="#666666", lw=1.0, ls=":")
ax.text(xst + 0.008, 0.1, "x*", color="#444444", fontsize=10)
ax.text(0.02, YTOP - 0.08, "ordinary type", color=BLUE,
        fontsize=10.5, fontweight="bold", ha="left", va="top")
ax.text(0.925, 0.55, "H", color="#666666", fontsize=10, ha="center")
ax.text(0.0, -0.22, "routine tasks open; the margin sits on a plateau.\n"
        "Wage: pinned there at c·γ(x*) — the polarization trace",
        color="#444444", fontsize=8.6, ha="left", va="top", linespacing=1.4,
        transform=ax.transAxes)

# (b) developer type, computing era -----------------------------------------
ax = axes[1]
m, wd = 0.55, 2.4
xs, ys = curve(m, lambda x: 0.95 * logistic(x, 0.30, 0.05))
ax.plot(xs, ys, color=NAVY, lw=2.6)
draw_wall(ax, m, float(ys[-1]), NAVY)
ax.axvspan(m, 1.0, color=BLUE, alpha=0.14, lw=0)
ax.fill_between(xs, 0, ys, color=GRAY, alpha=0.5, lw=0)
ax.axhline(wd, color=RED, lw=1.3, ls="--")
ax.text(0.985, wd + 0.06, "w_D/c", color=RED, fontsize=9.5, ha="right")
ax.axvline(m, color="#666666", lw=1.0, ls=":")
ax.text(m + 0.008, 0.1, "x* = the wall", color="#444444", fontsize=10)
ax.text(0.02, YTOP - 0.08, "developer type", color=NAVY,
        fontsize=10.5, fontweight="bold", ha="left", va="top")
ax.text(0.775, 1.15, "the type's specialty:\nclosed to machines (H)",
        color="#555555", fontsize=9, ha="center", va="center")
ax.annotate("above every open task:\nholds only wall tasks", xy=(0.40, wd),
            xytext=(0.30, 1.75), fontsize=9, color=RED, ha="center",
            arrowprops=dict(arrowstyle="->", color=RED, lw=0.9))
ax.text(0.0, -0.22, "specialty tasks closed to machines; the margin\n"
        "sits at the wall. Wage: a scarcity price on the type —\n"
        "a rent if untrainable (J_H = ∞); a quasi-rent that\n"
        "decays over the training lag J_H if trainable",
        color="#444444", fontsize=8.6, ha="left", va="top", linespacing=1.4,
        transform=ax.transAxes)

# (c) both types, AI ----------------------------------------------------------
ax = axes[2]
m, wc = 0.94, 0.85
xo, yo = curve(m, lambda x: 0.85 * logistic(x, 0.40, 0.06))
xd, yd = curve(m, lambda x: 0.85 * logistic(x, 0.36, 0.05))
ax.plot(xo, yo, color=BLUE, lw=2.6, label="ordinary type")
ax.plot(xd, yd, color=NAVY, lw=2.0, ls=(0, (4, 2)), label="developer type")
draw_wall(ax, m, float(yo[-1]), RED)
ax.axvspan(m, 1.0, color=GRAY, alpha=0.22, lw=0)
ax.axhline(wc, color=RED, lw=1.3, ls="--")
ax.text(0.30, wc + 0.06, "w/c = γ̄, both types", color=RED, fontsize=9.5, ha="left")
ax.fill_between(xo, 0, yo, color=GRAY, alpha=0.5, lw=0)
ax.text(0.02, YTOP - 0.08, "both types, AI", color=RED,
        fontsize=10.5, fontweight="bold", ha="left", va="top")
ax.text(0.97, 0.45, "H", color="#666666", fontsize=10, ha="center", va="center")
ax.legend(loc="center right", bbox_to_anchor=(0.98, 0.62), fontsize=9, framealpha=0.95)
ax.text(0.0, -0.22, "the developer's wall moves right: machines reach\n"
        "the specialty. Wage: c·γ̄ for both types —\n"
        "untrainability protected against human entry, not\n"
        "machine entry; the premium goes either way",
        color="#444444", fontsize=8.6, ha="left", va="top", linespacing=1.4,
        transform=ax.transAxes)

for ax in axes:
    ax.grid(alpha=0.25, lw=0.5)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_xlim(-0.01, 1.01)
    ax.set_ylim(0, YTOP)
    ax.set_xlabel("tasks the type can do, ranked by its γ")
axes[0].set_ylabel("relative human productivity γ_i(x)")
fig.subplots_adjust(left=0.05, right=0.99, top=0.96, bottom=0.40, wspace=0.14)
fig.savefig("figures/fig_types_draft.png", bbox_inches="tight")
print("wrote figures/fig_types_draft.png")
