# fig_eras_workers.py — Figure 4 of the paper: the task schedule in four eras, in
# one panel, with the wage ratio of a young entrant with no training (filled dots)
# and of a worker with years of training or experience (open dots) marked in each
# era. The caption identifies the markers.
# Smooth convex power curves illustrate relative capability across tasks.
# Conventions:
# * the wall is the set H of tasks closed to machines (by capability, preference or
#   law; γ unbounded), ranked last and drawn as a dashed vertical arrow off the
#   chart. Which tasks are closed does not depend on the worker, and each worker's
#   ranking of the tasks by γ rearranges the same [0, 1] with H last, so an era's
#   wall is at x = 1 − |H| for every worker: training moves a worker's schedule and
#   wage, never the wall. (Until 2026-11-04 the figure had two panels, one per
#   worker, with the walls in different places, read as worker-specific task mixes.)
# * the solid curves are the entrant's schedules, each that era's quantile function
#   of the entrant's γ on the open tasks [0, 1 − |H|);
# * machines never lose capability, so each era's schedule lies weakly below the
#   previous one and its wall further right (enforced numerically below; task
#   creation could break it only at the top);
# * a dot's height is an illustrative wage/machine-rental ratio w/p_m, not wage
#   purchasing power over goods or non-produced services. A dot on a schedule is an
#   interior margin, w/p_m = γ(x*); a dot on the wall is employment confined to
#   human-required tasks, where the wage is not a machine price (and a wall does not
#   imply that the participation constraint binds). Both workers in an era face the
#   same p_m, so the ratio of their dots' heights is the era's illustrative training
#   premium w_T/w_E;
# * one schedule cannot carry two interior dots at different wages: where two
#   workers share relative productivity, the cheaper one takes every open task and
#   the dearer one is at the wall. A trained worker with a contestable margin needs a
#   schedule of their own, drawn dashed where it holds one (candidate AI) and lying
#   weakly above the entrant's (training lowers productivity at no task; enforced).
#   Elsewhere the trained worker is at the wall, which needs their wage ratio above
#   their own schedule at every open task, so above the top of the entrant's
#   (enforced);
# * the AI schedules retain slope and a positive illustrative training premium;
# * the curvatures and wage ratios are schematic illustrations. The premia they
#   imply (printed when the script runs) are 1.27, 1.90, 2.15 and 1.38: rising into
#   computing, as the U.S. college premium did after 1980, and narrowing under
#   candidate AI.
# Pure schematic; the curves are not fitted to data.

import argparse
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.lines import Line2D

rcParams["font.family"] = "serif"
rcParams["font.serif"] = ["DejaVu Serif", "Georgia"]
rcParams["mathtext.fontset"] = "dejavuserif"
rcParams["pdf.fonttype"] = 42          # TrueType in the PDF: fonts embedded
# The figure is drawn at the width it prints, 0.88\textwidth in main.tex (16 cm text
# width), so sizes here are printed sizes: ticks 8 pt, axis labels 8.5 pt, the notes
# and the legend 7.5 pt (the legend's three columns fit the width at 7.5, not 8).
# Line widths, marker, tick and arrow sizes are those of the 2026-11-02 typography
# pass; the dots are a little larger so that the open ones read at print size.
PRINT_W = 0.88 * 16 / 2.54             # inches
rcParams["font.size"] = 8.5
rcParams["xtick.labelsize"] = rcParams["ytick.labelsize"] = 8
rcParams["axes.linewidth"] = 0.53
rcParams["patch.linewidth"] = 0.66     # the legend frame
for _ax in ("xtick", "ytick"):
    rcParams[f"{_ax}.major.width"] = 0.53
    rcParams[f"{_ax}.major.size"] = 2.3

BROWN, NAVY, BLUE, RED = "#8a6d3b", "#1a1a3d", "#4878b8", "#8b2020"
YTOP = 3.4
TRAINED_DASH = (0, (4, 1.6))           # the trained worker's own schedule
DOT = dict(marker="o", ls="none", ms=4.3)
OPEN_DOT = dict(marker="o", ls="none", ms=4.6, mfc="white", mew=1.1)

LEGEND = {
    "pre":  "pre-industrial (to about 1780)",
    "ind":  "industrial (1780–1950)",
    "comp": "computing (1970–2020)",
    "ai":   "candidate AI",
}
COLOR = {"pre": BROWN, "ind": NAVY, "comp": BLUE, "ai": RED}

# (era, wall at 1 − |H|, the entrant's schedule on [0, 1 − |H|), the entrant's w/p_m
#  and where it sits, the trained worker's w/p_m and where it sits). Where: "schedule",
#  an interior margin solved on the entrant's schedule; "wall", employment confined
#  to human-required tasks; "own", an interior margin on the trained worker's own
#  schedule TRAINED[era]. The entrant's industrial ratio was 1.0 in the two-panel
#  figure; the trained dot has to clear the schedule's top (2.52), and at 1.5 the
#  industrial premium (1.90) sits below computing's (2.15).
ERAS = [
    ("pre",  0.06, lambda x: 0.03 + 0.5 * (x / 0.06) ** 3,       1.5,  "wall",     1.9,  "wall"),
    ("ind",  0.45, lambda x: 0.02 + 2.5 * (x / 0.45) ** 2.5,     1.5,  "schedule", 2.85, "wall"),
    ("comp", 0.75, lambda x: 0.008 + 1.70 * (x / 0.75) ** 1.65,  0.93, "schedule", 2.0,  "wall"),
    ("ai",   0.94, lambda x: 0.004 + 1.25 * (x / 0.94) ** 1.50,  0.80, "schedule", 1.10, "own"),
]
TRAINED = {"ai": lambda x: 0.004 + 1.60 * (x / 0.94) ** 1.45}

# The paper's caption (main.tex, Figure 4). Retain the common-wall sentence and the
# reading of the open dots whenever this figure is reused.
FIGURE_CAPTION = r"""Four schematic configurations of the task schedule, shown for
an untrained entrant (filled dots) and a worker with accumulated training or
experience (open dots). Solid curves are the entrant's schedules; the trained
worker's own schedule is drawn (dashed) only in the candidate AI configuration, and
in the others lies below that worker's wage ratio at every open task. Closed tasks
appear as a wall at the right edge, common to both workers. Dot heights are
illustrative wage--machine-rental ratios $w/p_m$; within a configuration both dots
share $p_m$, so their ratio is the illustrative training premium. A dot on a
schedule marks an interior margin satisfying $w/p_m=\gamma(x^*)$; a dot on the wall
marks employment confined to human-required tasks, whose wage also depends on
demand, labor supply, and institutions. Industrialization opens physical tasks;
computing extends competition into cognitive tasks while many trained tasks remain
closed. Relative human advantage continues to vary across the open task range. In
the candidate AI configuration, machine competition extends across more tasks,
including trained ones, and the trained worker acquires an interior margin; the
schedules keep rising and retain an illustrative positive training premium. The
chosen curvatures illustrate differences in relative capability across tasks.
Drawn by code written with Claude (Anthropic)."""


def margin(xs, ys, top, w, where, what):
    """x of a dot at height w: solved on the schedule (xs, ys) with top value `top`,
    or None for the wall, where the wage must exceed the schedule at every open task."""
    if where == "wall":
        assert w > top, f"wall wage reaches open tasks: {what}"
        return None
    assert ys[0] <= w <= ys[-1], f"no interior intersection: {what}"
    x = float(np.interp(w, ys, xs))
    assert 0 <= x < xs[-1] and np.isclose(np.interp(x, xs, ys), w, rtol=0, atol=1e-9), \
        f"dot is off the schedule: {what}"
    return x


def build(spec):
    out = []
    for key, m, g, we, e_at, wt, t_at in spec:
        xs = np.linspace(0, m, 600, endpoint=False)
        ys, top = g(xs), float(g(m))
        assert np.all(np.diff(ys) > 0), f"unsorted schedule: {key}"
        xe = margin(xs, ys, top, we, e_at, f"entrant, {key}")
        yt = None
        if t_at == "own":
            yt = TRAINED[key](xs)
            assert np.all(np.diff(yt) > 0), f"unsorted trained schedule: {key}"
            assert np.all(yt >= ys), f"trained schedule below the entrant's: {key}"
            xt = margin(xs, yt, float(TRAINED[key](m)), wt, "schedule", f"trained, {key}")
        else:
            assert t_at == "wall"
            xt = margin(xs, ys, top, wt, "wall", f"trained, {key}")
        assert wt > we, f"no training premium: {key}"
        out.append(dict(key=key, m=m, xs=xs, ys=ys, top=top, yt=yt,
                        we=we, xe=m if xe is None else xe,
                        wt=wt, xt=m if xt is None else xt))
    for a, b in zip(out, out[1:]):                        # nesting asserted
        assert b["m"] >= a["m"], f"wall moved left: {b['key']}"
        common = b["xs"][b["xs"] < a["m"]]
        assert np.all(np.interp(common, b["xs"], b["ys"])
                      <= np.interp(common, a["xs"], a["ys"]) + 1e-9), \
            f"nesting violated: {b['key']} above {a['key']}"
    return out


def draw(ax, eras):
    for e in eras:
        col = COLOR[e["key"]]
        ax.plot(e["xs"], e["ys"], color=col, lw=1.58)
        if e["yt"] is not None:
            ax.plot(e["xs"], e["yt"], color=col, lw=1.1, ls=TRAINED_DASH)
        ax.annotate("", xy=(e["m"], YTOP), xytext=(e["m"], e["top"]),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=0.92, ls="--",
                                    shrinkA=0, shrinkB=0, mutation_scale=7.9))
        ax.plot(e["xe"], e["we"], color=col, zorder=5, **DOT)
        ax.plot(e["xt"], e["wt"], mec=col, zorder=5, **OPEN_DOT)
    ax.set_xlim(-0.02, 1.04)
    ax.set_ylim(0, YTOP)
    ax.set_xlabel(r"Tasks $x$, each schedule ordered by its worker's $\gamma$; closed tasks last")
    ax.set_ylabel(r"Relative human productivity $\gamma(x)$")
    ax.grid(alpha=0.25, lw=0.33)
    ax.spines[["top", "right"]].set_visible(False)


def note(ax, text, targets, xytext, key, ha):
    """A note in the era's color with an arrow to each target; every arrow leaves the
    same text box (copies after the first are invisible)."""
    for i, xy in enumerate(targets):
        ax.annotate(text, xy=xy, xytext=xytext, fontsize=7.5, ha=ha, va="top",
                    color=COLOR[key] if i == 0 else "none",
                    arrowprops=dict(arrowstyle="->", color=COLOR[key], lw=0.59,
                                    mutation_scale=5.8, shrinkB=3))


def legend(fig):
    era = {k: Line2D([], [], color=COLOR[k], lw=1.58) for k in COLOR}
    blank = Line2D([], [], ls="none")
    keys = [Line2D([], [], color="0.3", **DOT),
            Line2D([], [], mec="0.3", **OPEN_DOT),
            Line2D([], [], color="0.3", lw=1.1, ls=TRAINED_DASH)]
    # matplotlib fills legend columns first: the eras read across two rows on the
    # left, the markers down the right column
    handles = [era["pre"], era["comp"], blank, era["ind"], era["ai"], blank] + keys
    labels = [LEGEND["pre"], LEGEND["comp"], "", LEGEND["ind"], LEGEND["ai"], "",
              "entrant", "trained worker", "trained worker's schedule"]
    return fig.legend(handles, labels, loc="outside lower center", ncol=3, fontsize=7.5,
                      framealpha=0.95, handlelength=1.8, handletextpad=0.5,
                      columnspacing=1.2)


def main():
    default_output = (Path(__file__).resolve().parents[1] / "paper"
                      / "figures" / "fig_eras_workers.png")
    parser = argparse.ArgumentParser(description="Draw the schematic eras figure.")
    parser.add_argument("--output", type=Path, default=default_output,
                        help="Output image path (default: ../paper/figures/fig_eras_workers.png); "
                             "a PDF with the same basename is written next to it.")
    args = parser.parse_args()

    eras = build(ERAS)
    print("training premia w_T/w_E:",
          ", ".join(f"{e['key']} {e['wt'] / e['we']:.2f}" for e in eras))
    at = {e["key"]: e for e in eras}

    def dot(key, who):
        return at[key]["x" + who], at[key]["w" + who]

    # one panel replaces the two of 2026-11-02 (8.42 x 5.35 in printed): 3.6 in tall
    fig, ax = plt.subplots(figsize=(PRINT_W, 3.6), layout="constrained")
    draw(ax, eras)
    # note positions at the printed size: the pre-industrial note sits between its
    # wall and the industrial schedule, the industrial and computing notes above their
    # schedules, the AI note below the AI schedules
    note(ax, "Both at the wall:\nwages shaped by\nland access and\nlabor scarcity",
         [dot("pre", "t"), dot("pre", "e")], (0.10, 1.98), "pre", "left")
    note(ax, "Engines price the entrant;\nthe trained worker is\nbehind the wall",
         [dot("ind", "t")], (0.415, 3.33), "ind", "right")
    note(ax, "Computers price\nthe entrant; the\ntrained worker is\nbehind the wall",
         [dot("comp", "t")], (0.60, 3.33), "comp", "center")
    note(ax, "The wall reaches trained tasks:\nboth margins contestable",
         [dot("ai", "t")], (0.80, 0.55), "ai", "center")
    leg = legend(fig)
    fig.canvas.draw()
    box = leg.get_window_extent()
    assert box.x0 >= 0 and box.x1 <= fig.bbox.width, "legend wider than the printed figure"

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, dpi=300)
    pdf = args.output.with_suffix(".pdf")
    fig.savefig(pdf, metadata={"CreationDate": None})
    plt.close(fig)
    print(f"wrote {args.output} and {pdf.name}")


if __name__ == "__main__":
    main()
