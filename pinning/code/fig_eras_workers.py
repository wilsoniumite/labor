# fig_eras_workers.py — Figure 2 of the paper: the
# schedule across four eras, drawn twice — for a young entrant with no
# training (top) and for a worker with years of training or experience
# (bottom). The caption identifies the panels.
# Smooth convex power curves illustrate relative capability across tasks.
# Conventions:
# * panels use different worker-specific task mixes, fixed across eras within
#   each panel. Different wall locations reflect those mixes, not a change in
#   machine capability caused by training;
# * each curve is that era's quantile function of γ for that task mix, tasks
#   ranked by γ with the tasks closed to machines (the set H, γ unbounded)
#   last, drawn as a dashed vertical arrow off the chart — the wall;
# * machines never lose capability, so within a panel each era's curve lies
#   weakly below the previous one and its wall further right (enforced
#   numerically below; task creation could break it only at the top);
# * a dot's height is an illustrative wage/machine-rental ratio w/c, not wage
#   purchasing power over goods or non-produced services. It marks the era's margin:
#   on the schedule where the wage line
#   crosses it, or at the wall when the wage exceeds the machine cost at
#   every reachable task — there the wage is not a machine price.
# * a wall does not imply that the participation constraint binds;
# * the AI schedules retain slope and a positive illustrative training premium.
# * the curvatures and wage ratios are schematic illustrations.
# Pure schematic; the curves are not fitted to data.

import argparse
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


LEGEND = {
    "pre":  "pre-industrial (to about 1780)",
    "ind":  "industrial (1780–1950)",
    "comp": "computing (1970–2020)",
    "ai":   "Candidate AI",
}
COLOR = {"pre": BROWN, "ind": NAVY, "comp": BLUE, "ai": RED}

# (open-set measure m = 1 − |H|, quantile function on [0, m), w/c,
#  margin x*, None to solve the intersection, or "wall")
ENTRANT = [
    ("pre",  0.06, lambda x: 0.03 + 0.5 * (x / 0.06) ** 3,        1.5,  "wall"),
    ("ind",  0.45, lambda x: 0.02 + 2.5 * (x / 0.45) ** 2.5,      1.0,  None),
    ("comp", 0.75, lambda x: 0.008 + 1.70 * (x / 0.75) ** 1.65, 0.93, None),
    ("ai",   0.94, lambda x: 0.004 + 1.25 * (x / 0.94) ** 1.50, 0.80, None),
]
TRAINED = [
    ("pre",  0.06, lambda x: 0.03 + 0.5 * (x / 0.06) ** 3,        1.9,  "wall"),
    ("ind",  0.25, lambda x: 0.02 + 1.2 * (x / 0.25) ** 2.5,      2.4,  "wall"),
    ("comp", 0.50, lambda x: 0.008 + 1.50 * (x / 0.50) ** 1.70, 2.0,  "wall"),
    ("ai",   0.92, lambda x: 0.004 + 1.45 * (x / 0.92) ** 1.55, 1.00, None),
]

# Suggested paper caption. Retain the type-specific task-mix qualification
# whenever this figure is reused.
FIGURE_CAPTION = r"""Four schematic configurations of the task schedule, shown for
an untrained entrant (top) and a worker with accumulated training or experience
(bottom). Each panel uses a different worker-specific task mix, held fixed
across eras within that panel; differences in wall location reflect these
mixes, not an effect of training on machine capability. Closed tasks appear as
a wall at the right edge. Dot heights are illustrative wage--machine-rental
ratios $w/c$, not purchasing power over goods or non-produced services. A dot on the
contestable schedule marks an interior margin satisfying $w/c=\gamma(x^*)$;
a dot on the wall marks the absence of such a margin and does not imply a
binding participation constraint. Industrialization opens physical tasks;
computing extends competition into cognitive tasks while many trained tasks
remain closed. Relative human advantage continues to vary across the open
task range. In the candidate AI configuration, machine competition extends
across more tasks, while the schedules keep rising and retain an illustrative
positive training premium. The chosen curvatures illustrate differences in
relative capability across tasks."""


def build(spec):
    out = []
    for key, m, g, wc, xst in spec:
        xs = np.linspace(0, m, 600, endpoint=False)
        ys = g(xs)
        at_wall = xst == "wall"
        if at_wall:
            assert wc > ys[-1], f"wall wage reaches contestable tasks: {key}"
            xst = m
        else:
            assert ys[0] <= wc <= ys[-1], f"no interior intersection: {key}"
            if xst is None:
                xst = float(np.interp(wc, ys, xs))
            assert 0 <= xst < m and np.isclose(
                np.interp(xst, xs, ys), wc, rtol=0, atol=1e-9
            ), f"wage marker is off the schedule: {key}"
        assert np.all(np.diff(ys) >= -1e-9), f"unsorted schedule: {key}"
        out.append(dict(key=key, m=m, xs=xs, ys=ys, wc=wc,
                        xstar=xst, at_wall=at_wall))
    for a, b in zip(out, out[1:]):                        # nesting asserted
        assert b["m"] >= a["m"], f"wall moved left: {b['key']}"
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
        if e["at_wall"]:
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


def margin_point(era):
    return era["xstar"], era["wc"]


def main():
    default_output = (Path(__file__).resolve().parents[1] / "paper"
                      / "figures" / "fig_eras_workers.png")
    parser = argparse.ArgumentParser(description="Draw the schematic eras figure.")
    parser.add_argument("--output", type=Path, default=default_output,
                        help="Output image path (default: ../paper/figures/fig_eras_workers.png).")
    args = parser.parse_args()

    entrant = build(ENTRANT)
    trained = build(TRAINED)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.6, 8.4), dpi=150, sharex=True)

    draw_panel(ax1, entrant, [
        ("Wage shaped by land access\nand labor scarcity",
         margin_point(entrant[0]), (0.10, 2.95), "pre", "left"),
        ("Steep task margin:\nmachine substitution\nprices the wage",
         margin_point(entrant[1]), (0.60, 2.35), "ind", "center"),
        ("Computing:\nuneven task\ncompetition",
         margin_point(entrant[2]), (0.845, 2.65), "comp", "center"),
        ("Machine competition extends\nacross more tasks",
         margin_point(entrant[3]), (0.80, 0.43), "ai", "center"),
    ])
    draw_panel(ax2, trained, [
        ("Wage shaped by\nland access and\nlabor scarcity",
         margin_point(trained[0]), (0.075, 3.2), "pre", "left"),
        ("Wall boundary:\nskilled tasks\nclosed to engines",
         margin_point(trained[1]), (0.28, 3.2), "ind", "left"),
        ("Wall boundary: skilled tasks\nremain closed to computers",
         margin_point(trained[2]), (0.65, 2.45), "comp", "center"),
        ("Retreating wall: training\npremium may narrow",
         margin_point(trained[3]), (0.80, 0.45), "ai", "center"),
    ])
    fig.text(0.535, 0.985, r"Dots: illustrative wage ratios $w/c$",
             ha="center", va="top", fontsize=9)
    ax2.set_xlabel(r"Tasks $x$, ordered by this worker's $\gamma$; closed tasks last")
    ax2.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=4, fontsize=8.8,
               framealpha=0.95, handlelength=1.8, columnspacing=1.0)
    fig.subplots_adjust(left=0.09, right=0.98, top=0.94, bottom=0.12, hspace=0.22)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()
