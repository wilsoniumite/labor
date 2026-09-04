# fig_eras_v2_draft.py — CANDIDATE redraw of Figure 2 (the era schematic),
# built for the 2026-09-02 review of the task schedules. Not referenced by
# the paper; fig_eras.py / fig_eras.png are untouched. Her call.
#
# What changes against fig_eras.py, and why (each is a model statement):
#
# 1. FOUR configurations, the pre-industrial one drawn. Appendix A's set H
#    (tasks closed to machines) is the object: pre-industrial H covers nearly
#    every task, so the schedule is a sliver (mills, draft animals) and then a
#    WALL — relative human productivity is off-chart because no machine
#    holds the task at any price. The margin sits at the wall, labor demand
#    in the task dimension is perfectly inelastic there, and the wage is set
#    on the other side: the land floor s(q) (Prop 3; long-record R1).
#    So "off-chart" was right and "compressed"/"flat" was the wrong word:
#    the pre-industrial schedule is the VERTICAL case, the AI limit the FLAT
#    case — opposite labor-demand elasticities, both pinning the wage to
#    land (the floor, then the recursion c ∝ r).
#
# 2. NESTING. Each curve is that era's quantile function of γ (tasks ranked
#    by that era's γ, H counted as γ = ∞). Machines do not lose capability,
#    so in rank space each era's curve lies weakly BELOW the previous one and
#    its wall lies further RIGHT; only task creation at the top can break it.
#    fig_eras.py violates this at the bottom (computing 0.9 > industrial 0.3
#    at x = 0; AI above both below x ≈ 0.41) and has no wall in any era.
#
# 3. EVERY ERA KEEPS A WALL. Industrial: engines "useless at cognitive
#    tasks" — those tasks are in H, not at γ = 8. Computing: non-routine
#    manual and cognitive tasks stay closed (ALM 2003). AI: H is the residue
#    (co-presence, law, capability) — Appendix D.
#
# 4. THE MARGIN IS MARKED, because flatness matters only AT the margin
#    (Lemma A.1: a flat stretch pins the wage only if x* sits on it).
#    Industrial: x* on a steep stretch inside the physical tasks. Computing:
#    x* on a short plateau — the routine block, coded at similar cost, the
#    polarization trace. AI: the plateau is nearly the whole open set.
#
# 5. λ (labor inside the machine sector) is NOT a γ-object and cannot be
#    drawn on this chart; the panel version carries it as one line per era
#    (high / high / high — "barely touched": the developers / falling).
#    Reinstatement (new tasks at the wall: developers, IT) is the paper's
#    new-task margin; in rank space it enters at the top.
#
# Pure schematic, no data. Wall positions and levels are illustrative.

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams["font.family"] = "serif"
rcParams["font.serif"] = ["DejaVu Serif", "Georgia"]
rcParams["font.size"] = 11

BROWN, NAVY, BLUE, RED, GRAY = "#8a6d3b", "#1a1a3d", "#4878b8", "#8b2020", "#c8c8c8"


def logistic(x, mid, width):
    return 1.0 / (1.0 + np.exp(-(x - mid) / width))


# ------------------------------------------------------------ the four eras
# Each era: (open-set measure m = 1 − |H|, quantile function on [0, m)).
# Curves are enforced nested numerically below.
ERAS = [
    dict(key="pre",  name="pre-industrial", color=BROWN, m=0.06,
         g=lambda x: 0.03 + 0.5 * (x / 0.06) ** 3,
         wc=1.5, xstar=0.06),                                   # margin AT the wall
    dict(key="ind",  name="industrial",     color=NAVY,  m=0.40,
         g=lambda x: 0.02 + 2.5 * (x / 0.40) ** 2.5,
         wc=1.0, xstar=None),                                   # solved below
    dict(key="comp", name="computing",      color=BLUE,  m=0.62,
         g=lambda x: 0.95 * logistic(x, 0.36, 0.045),
         wc=0.95, xstar=0.55),                                  # on the plateau
    dict(key="ai",   name="AI",             color=RED,   m=0.94,
         g=lambda x: 0.85 * logistic(x, 0.37, 0.05),
         wc=0.85, xstar=0.70),                                  # on the plateau
]

YTOP = 3.4
prev = None
for e in ERAS:
    xs = np.linspace(0, e["m"], 600, endpoint=False)
    ys = e["g"](xs)
    if prev is not None:                      # nesting: weakly below the previous era
        ys = np.minimum(ys, np.interp(xs, prev[0], prev[1], right=np.inf))
    e["xs"], e["ys"] = xs, ys
    prev = (xs, ys)
# industrial margin: γ(x*) = w/c on the sloped stretch
e = ERAS[1]
e["xstar"] = float(e["xs"][np.argmin(np.abs(e["ys"] - e["wc"]))])

# sanity: nesting holds at every drawn point
for a, b in zip(ERAS, ERAS[1:]):
    common = b["xs"][b["xs"] < a["m"]]
    assert np.all(np.interp(common, b["xs"], b["ys"]) <= np.interp(common, a["xs"], a["ys"]) + 1e-9), \
        f"nesting violated: {b['key']} above {a['key']}"


def draw_wall(ax, e, ytop, lw=1.4, label=None, fontsize=9):
    x0 = e["m"]
    y0 = float(e["ys"][-1])
    ax.annotate("", xy=(x0, ytop), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=e["color"], lw=lw, ls="--",
                                shrinkA=0, shrinkB=0, mutation_scale=12))
    if label:
        ax.text(x0 + 0.008, ytop - 0.06, label, color=e["color"], fontsize=fontsize,
                ha="left", va="top", rotation=90)


# =============================================================== single panel
fig, ax = plt.subplots(figsize=(8.6, 4.8), dpi=150)
LEG = {
    "pre":  "pre-industrial: mills and draft animals; everything else closed",
    "ind":  "industrial: physical tasks open, steep at the margin; cognitive closed",
    "comp": "computing: routine tasks open; a flat stretch at the margin",
    "ai":   "AI: flat nearly everywhere; H is what remains",
}
for e in ERAS:
    ax.plot(e["xs"], e["ys"], color=e["color"], lw=2.4, label=LEG[e["key"]])
    draw_wall(ax, e, YTOP)
    # the margin
    if e["key"] == "pre":
        ax.plot([0, e["m"]], [e["wc"], e["wc"]], color=e["color"], lw=1.1, ls=":")
        ax.plot(e["m"], e["wc"], "o", color=e["color"], ms=5.5, zorder=5)
    else:
        ax.plot(e["xstar"], e["wc"], "o", color=e["color"], ms=5.5, zorder=5)

ax.text(0.075, YTOP - 0.05, "off-chart: no machine holds\nthe task (the set H)",
        color="#555555", fontsize=9, ha="left", va="top")
ax.annotate("the margin sits at the wall:\nthe wage is the land floor s(q)",
            xy=(0.06, 1.5), xytext=(0.075, 2.98), fontsize=8.6, color=BROWN, va="top",
            arrowprops=dict(arrowstyle="->", color=BROWN, lw=0.9))
ax.annotate("x* on a steep stretch:\nthe ceiling rises off the floor",
            xy=(ERAS[1]["xstar"], 1.0), xytext=(0.515, 1.95), fontsize=8.5, color=NAVY,
            ha="center",
            arrowprops=dict(arrowstyle="->", color=NAVY, lw=0.9))
ax.annotate("x* on a flat stretch:\nthe wage is pinned where it sits",
            xy=(0.55, 0.95), xytext=(0.78, 1.55), fontsize=8.8, color=BLUE, ha="center",
            arrowprops=dict(arrowstyle="->", color=BLUE, lw=0.9))
ax.annotate("the level at the margin falls,\nand the slope falls with it",
            xy=(0.70, 0.85), xytext=(0.80, 0.30), fontsize=9, color=RED, ha="center",
            arrowprops=dict(arrowstyle="->", color=RED, lw=0.9))
ax.text(0.955, 0.12, "H", color=RED, fontsize=10, ha="left")

ax.set_xlabel("tasks x, each era ranked by its own γ (closed tasks last)")
ax.set_ylabel("relative human productivity γ(x)")
ax.set_xlim(-0.02, 1.04)
ax.set_ylim(0, YTOP)
ax.grid(alpha=0.25, lw=0.5)
ax.spines[["top", "right"]].set_visible(False)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=2, fontsize=8.6,
          framealpha=0.95, handlelength=1.8, columnspacing=1.2)
fig.tight_layout()
fig.savefig("figures/fig_eras_v2_draft.png", bbox_inches="tight")
print("wrote figures/fig_eras_v2_draft.png")

# ================================================================ four panels
NOTES = {
    "pre":  ("to ~1780", "machines: mills, draft animals, sail",
             "wage: the land floor s(q) — the margin cannot move",
             "λ high: every machine hand-made and hand-run"),
    "ind":  ("1780–1950", "machines: power and physical tasks",
             "wage: the ceiling c·γ(x*), steep at the margin",
             "λ high: operators, mechanics, builders"),
    "comp": ("1970–2020", "machines: + routine cognitive and manual tasks",
             "wage: pinned on the plateau (the polarization trace)",
             "λ high: developers; new tasks enter at the wall"),
    "ai":   ("candidate", "machines: everything but H",
             "wage: c·γ̄ everywhere, and c ∝ r — land again",
             "λ falling: the machine sector sheds its own labor"),
}
TITLE_X = {"pre": 0.10, "ind": 0.44, "comp": 0.02, "ai": 0.02}
fig, axes = plt.subplots(2, 2, figsize=(10.4, 8.6), dpi=150, sharey=True)
for ax, e in zip(axes.ravel(), ERAS):
    t, l1, l2, l3 = NOTES[e["key"]]
    ax.plot(e["xs"], e["ys"], color=e["color"], lw=2.6)
    draw_wall(ax, e, YTOP, lw=1.6)
    ax.axvspan(e["m"], 1.0, color=GRAY, alpha=0.22, lw=0)
    # w/c line and the two shadings of Figure 1
    line_col = NAVY if e["key"] == "ai" else RED
    ax.axhline(e["wc"], color=line_col, lw=1.3, ls="--")
    if e["key"] == "pre":
        ax.text(0.985, e["wc"] + 0.06, "s/c (the floor)", color=line_col, fontsize=9.5, ha="right")
    elif e["key"] == "ai":
        ax.text(0.30, e["wc"] + 0.06, "w/c = γ̄", color=line_col, fontsize=9.5, ha="left")
    else:
        ax.text(0.985, e["wc"] + 0.06, "w/c", color=line_col, fontsize=9.5, ha="right")
    xs, ys = e["xs"], e["ys"]
    xst = e["xstar"]
    ax.fill_between(xs, 0, ys, where=xs <= xst, color=GRAY, alpha=0.5, lw=0)
    ax.fill_between(xs, 0, ys, where=xs >= xst, color=BLUE, alpha=0.18, lw=0)
    ax.axvline(xst, color="#666666", lw=1.0, ls=":")
    ax.text(xst + 0.008, 0.1, "x*", color="#444444", fontsize=10)
    ax.text(TITLE_X[e["key"]], YTOP - 0.08, f"{e['name']} ({t})", color=e["color"],
            fontsize=11.5, fontweight="bold", ha="left", va="top")
    ax.text(0.0, -0.30, f"{l1}\n{l2}\n{l3}", color="#444444", fontsize=9,
            ha="left", va="top", linespacing=1.4, transform=ax.transAxes)
    if e["key"] == "ai":
        ax.text(0.97, 0.45, "H", color="#666666", fontsize=10, ha="center", va="center")
    else:
        ax.text(e["m"] + 0.5 * (1 - e["m"]), 0.55, "closed to\nmachines (H)",
                color="#666666", fontsize=9, ha="center", va="center")
    ax.grid(alpha=0.25, lw=0.5)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_xlim(-0.01, 1.01)
    ax.set_ylim(0, YTOP)
    ax.set_xlabel("tasks x, ranked by the era's γ (closed tasks last)")
for ax in axes[:, 0]:
    ax.set_ylabel("relative human productivity γ(x)")
fig.subplots_adjust(left=0.07, right=0.98, top=0.97, bottom=0.14, hspace=0.75, wspace=0.10)
fig.savefig("figures/fig_eras_v2_draft_panels.png", bbox_inches="tight")
print("wrote figures/fig_eras_v2_draft_panels.png")
