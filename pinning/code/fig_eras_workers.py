# fig_eras_workers.py — Figure 2 of the paper (her call, 2026-09-02): the
# schedule across four eras, drawn twice — for a young entrant with no
# training (top) and for a worker with years of training or experience
# (bottom). Supersedes the single-panel era figure (dynamics/code/fig_eras.py).
# No in-figure panel titles (2026-09-04): the caption says which panel is which.
#
# Conventions (see the 2026-09-02 review, STATE logs 42–44):
# * each curve is that era's quantile function of γ for that person, tasks
#   ranked by γ with the tasks closed to machines (the set H, γ unbounded)
#   last, drawn as a dashed vertical arrow off the chart — the wall;
# * machines never lose capability, so within a panel each era's curve lies
#   weakly below the previous one and its wall further right (enforced
#   numerically below; task creation could break it only at the top);
# * the dot marks the era's margin: on the schedule where the wage line
#   crosses it, or at the wall when the wage exceeds the machine cost at
#   every reachable task — there the wage is not a machine price.
# Pure schematic, no data; wall positions and levels are illustrative.

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams["font.family"] = "serif"
rcParams["font.serif"] = ["DejaVu Serif", "Georgia"]
rcParams["font.size"] = 11
rcParams["mathtext.fontset"] = "dejavuserif"

BROWN, NAVY, BLUE, RED, GRAY = "#8a6d3b", "#1a1a3d", "#4878b8", "#8b2020", "#c8c8c8"
YTOP = 3.4


def logistic(x, mid, width):
    return 1.0 / (1.0 + np.exp(-(x - mid) / width))


LEGEND = {
    "pre":  "pre-industrial (to about 1780)",
    "ind":  "industrial (1780–1950)",
    "comp": "computing (1970–2020)",
    "ai":   "Candidate AI",
}
COLOR = {"pre": BROWN, "ind": NAVY, "comp": BLUE, "ai": RED}

# (open-set measure m = 1 − |H|, quantile function on [0, m), w/c, margin x*
#  or "wall")
ENTRANT = [
    ("pre",  0.06, lambda x: 0.03 + 0.5 * (x / 0.06) ** 3,        1.5,  "wall"),
    ("ind",  0.45, lambda x: 0.02 + 2.5 * (x / 0.45) ** 2.5,      1.0,  None),
    ("comp", 0.75, lambda x: 0.95 * logistic(x, 0.42, 0.05),      0.95, 0.62),
    ("ai",   0.94, lambda x: 0.85 * logistic(x, 0.43, 0.05),      0.85, 0.78),
]
TRAINED = [
    ("pre",  0.06, lambda x: 0.03 + 0.5 * (x / 0.06) ** 3,        1.9,  "wall"),
    ("ind",  0.25, lambda x: 0.02 + 1.2 * (x / 0.25) ** 2.5,      2.4,  "wall"),
    ("comp", 0.50, lambda x: 0.95 * logistic(x, 0.30, 0.045),     2.0,  "wall"),
    ("ai",   0.92, lambda x: 0.85 * logistic(x, 0.34, 0.05),      0.85, 0.72),
]


def build(spec):
    out, prev = [], None
    for key, m, g, wc, xst in spec:
        xs = np.linspace(0, m, 600, endpoint=False)
        ys = g(xs)
        if prev is not None:
            ys = np.minimum(ys, np.interp(xs, prev[0], prev[1], right=np.inf))
        if xst is None:                                   # margin on the schedule
            xst = float(xs[np.argmin(np.abs(ys - wc))])
        elif xst == "wall":
            xst = m
        out.append(dict(key=key, m=m, xs=xs, ys=ys, wc=wc, xstar=xst))
        prev = (xs, ys)
    for a, b in zip(out, out[1:]):                        # nesting asserted
        common = b["xs"][b["xs"] < a["m"]]
        assert np.all(np.interp(common, b["xs"], b["ys"])
                      <= np.interp(common, a["xs"], a["ys"]) + 1e-9), \
            f"nesting violated: {b['key']} above {a['key']}"
    return out


def draw_panel(ax, eras, notes):
    for e in eras:
        col = COLOR[e["key"]]
        ax.plot(e["xs"], e["ys"], color=col, lw=2.4, label=LEGEND[e["key"]])
        ax.annotate("", xy=(e["m"], YTOP), xytext=(e["m"], float(e["ys"][-1])),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=1.4, ls="--",
                                    shrinkA=0, shrinkB=0, mutation_scale=12))
        if e["xstar"] == e["m"]:                          # margin at the wall
            ax.plot([0, e["m"]], [e["wc"], e["wc"]], color=col, lw=1.0, ls=":")
        ax.plot(e["xstar"], e["wc"], "o", color=col, ms=6, zorder=5)
    for (text, xy, xytext, key, ha) in notes:
        ax.annotate(text, xy=xy, xytext=xytext, fontsize=8.8, color=COLOR[key],
                    ha=ha, va="top",
                    arrowprops=dict(arrowstyle="->", color=COLOR[key], lw=0.9))
    ax.set_xlim(-0.02, 1.04)
    ax.set_ylim(0, YTOP)
    ax.set_ylabel(r"Relative human productivity $\gamma(x)$")
    ax.grid(alpha=0.25, lw=0.5)
    ax.spines[["top", "right"]].set_visible(False)


entrant = build(ENTRANT)
trained = build(TRAINED)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.6, 8.4), dpi=150, sharex=True)

# annotations per her 2026-09-02 ruling on the editorial sheet (its tables)
draw_panel(ax1, entrant, [
    ("Wall boundary:\nparticipation floor binds", (0.06, 1.5), (0.10, 2.95), "pre", "left"),
    ("Steep task margin:\nmachine substitution\nprices the wage",
     (entrant[1]["xstar"], 1.0), (0.60, 2.35), "ind", "center"),
    ("Flat task margin:\nwage locally pinned", (0.62, 0.95), (0.845, 1.85), "comp", "center"),
    ("Contestable schedule\nnearly flat", (0.78, 0.85), (0.86, 0.50), "ai", "center"),
])
draw_panel(ax2, trained, [
    ("Wall boundary:\nfloor and skill\nscarcity", (0.06, 1.9), (0.075, 3.2), "pre", "left"),
    ("Wall boundary: skilled\ntasks remain closed\nto engines",
     (0.25, 2.4), (0.28, 3.2), "ind", "left"),
    ("Wall boundary: skilled tasks\nremain closed to computers", (0.50, 2.0), (0.62, 2.45), "comp", "center"),
    ("Retreating wall: training\npremium may narrow", (0.72, 0.85), (0.80, 0.45), "ai", "center"),
])
ax2.set_xlabel(r"Tasks $x$, ordered by this worker's $\gamma$; closed tasks last")
ax2.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=4, fontsize=8.8,
           framealpha=0.95, handlelength=1.8, columnspacing=1.0)
fig.subplots_adjust(left=0.09, right=0.98, top=0.96, bottom=0.12, hspace=0.22)
OUT = Path(__file__).resolve().parents[1] / "paper" / "figures" / "fig_eras_workers.png"
fig.savefig(OUT, bbox_inches="tight")
print(f"wrote {OUT}")
