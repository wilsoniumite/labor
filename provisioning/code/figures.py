# figures.py — the draft's figures, each from a table a battery holds.
#
#   fig_accounts      three accounts of labour's part in consumption, 1997-2023              data/one_basis.csv, the financing panel
#   fig_exposure      each income decile's exposure, 2023                                    data/exposure_deciles.csv
#   fig_holdings      who holds each claim and who does the consuming, 2023                  data/exposure_groups.csv
#   fig_shift         each group's share of market income as labour's share falls            code/exposure.py's identity
#   fig_path          who is paid along the companion's path, and what the claims cost       code/paper_path.py
#   fig_bases         the site-rent base and the cost of a floor, 1947-2024                  code/rent_base.py
#   fig_program       each group's income from capital and land per dollar of labour income  code/program.py
#
# Colour: three categorical slots (blue, orange, aqua) and a blue/red pair for above and below zero, validated on a white
# page with the dataviz skill's validator (all checks pass; aqua is under 3:1 against the page, so every aqua mark has a
# label, and every figure's numbers are in a table in the paper). Text is never in a series colour. Static, for print.
#
# Run from provisioning/:  python3 code/figures.py      writes paper/figures/*.png

import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from matplotlib.patches import FancyBboxPatch, Rectangle  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import exposure as ex  # noqa: E402
import one_basis_tables as obt  # noqa: E402
import paper_path as pp  # noqa: E402
import program as pg  # noqa: E402
import rent_base as rb  # noqa: E402

OUT = os.path.join(ROOT, "paper", "figures")
BLUE, ORANGE, AQUA, RED = "#2a78d6", "#eb6834", "#1baf7a", "#e34948"
INK, INK2, MUTED, GRID, AXIS, CONTEXT = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7", "#b5b3ab"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.5, "axes.edgecolor": AXIS, "axes.linewidth": 0.8,
                     "axes.labelcolor": INK2, "xtick.color": MUTED, "ytick.color": MUTED, "xtick.labelcolor": INK2,
                     "ytick.labelcolor": INK2, "text.color": INK, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "axes.grid.axis": "y", "grid.color": GRID, "grid.linewidth": 0.8, "grid.linestyle": "-",
                     "axes.axisbelow": True, "legend.frameon": False, "legend.fontsize": 8.5, "figure.dpi": 100,
                     "savefig.dpi": 220, "savefig.facecolor": "white", "axes.titlesize": 9, "axes.titleweight": "bold",
                     "axes.titlelocation": "left", "axes.titlepad": 8})
LW = 1.7


def save(fig, name):
    os.makedirs(OUT, exist_ok=True)
    fig.savefig(os.path.join(OUT, name + ".png"), bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)


def dot(ax, x, y, colour):
    """An end marker: the series colour with a ring of the page's colour."""
    ax.plot([x], [y], marker="o", ms=6.5, mfc=colour, mec="white", mew=1.6, zorder=5)


def column(ax, x, height, width, colour, radius_in=0.045):
    """A column that grows from zero with its data end rounded (by radius_in inches on the page) and its base square.
    Call it after the axes' limits are set."""
    if height == 0:
        return
    box = ax.get_window_extent().transformed(ax.figure.dpi_scale_trans.inverted())
    per_in_x = (ax.get_xlim()[1] - ax.get_xlim()[0]) / box.width
    per_in_y = (ax.get_ylim()[1] - ax.get_ylim()[0]) / box.height
    rx, ry = radius_in * per_in_x, min(radius_in * per_in_y, abs(height) / 2)
    y0, y1 = (0.0, height) if height > 0 else (height, 0.0)
    ax.add_patch(FancyBboxPatch((x - width / 2, y0), width, y1 - y0, boxstyle=f"round,pad=0,rounding_size={rx}",
                                mutation_aspect=per_in_y / per_in_x, fc=colour, ec="none", zorder=3))
    base = 0.0 if height > 0 else -ry                                   # a square patch over the rounded corners at the base
    ax.add_patch(Rectangle((x - width / 2, base), width, ry, fc=colour, ec="none", zorder=3))


def fig_accounts():
    made, fin, pub = obt.made(), obt.financing(), obt.published()
    fig, ax = plt.subplots(figsize=(6.6, 3.5))
    ax.fill_between(fin.index, fin.fin_lower, fin.fin_upper, color=ORANGE, alpha=0.10, lw=0, zorder=1)
    ax.plot(pub.index, pub.human_effort_share, color=CONTEXT, lw=LW, zorder=2, label="Made by labor, as the production account counts it")
    ax.plot(fin.index, fin.fin_labour, color=ORANGE, lw=LW, zorder=3, label="Paid for by labor income (its bounds shaded)")
    ax.plot(made.index, made.labour_factor_psi38, color=BLUE, lw=LW, zorder=4, label="Made by labor, with wear traced back and taxes and imports set aside")
    for s, c in ((pub.human_effort_share, CONTEXT), (fin.fin_labour, ORANGE), (made.labour_factor_psi38, BLUE)):
        dot(ax, s.index[-1], s.iloc[-1], c)
    ax.annotate("0.66 made and 0.66 paid for", (2023, made.labour_factor_psi38[2023]), xytext=(6, 0), textcoords="offset points",
                va="center", color=INK2)
    ax.annotate("0.47", (2023, pub.human_effort_share[2023]), xytext=(6, 0), textcoords="offset points", va="center", color=INK2)
    ax.annotate("wear, taxes\nand imports", (2012.5, 0.565), ha="center", va="center", color=MUTED, fontsize=8)
    ax.set_xlim(1996.5, 2023.5)
    ax.set_ylim(0.40, 0.86)
    ax.set_yticks([0.4, 0.5, 0.6, 0.7, 0.8])
    ax.set_ylabel("Labor's share")
    ax.legend(loc="upper left", bbox_to_anchor=(0.0, 1.20), ncol=1, handlelength=1.6, borderaxespad=0)
    fig.subplots_adjust(right=0.74)
    save(fig, "fig_accounts")


def fig_exposure():
    d = pd.read_csv(os.path.join(ROOT, "data", "exposure_deciles.csv"))
    d = d[d.year == 2023].set_index("decile").loc[ex.DECILES]
    fig, ax = plt.subplots(figsize=(6.6, 3.1))
    names = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th"]
    ax.set_xticks(range(10), names)
    ax.set_xlim(-0.6, 9.6)
    ax.set_ylim(-0.19, 0.17)
    for i, v in enumerate(d.exposure.values):
        column(ax, i, v, 0.46, BLUE if v > 0 else RED)
    ax.axhline(0, color=AXIS, lw=0.8, zorder=4)
    for i in (0, 6, 9):
        v = d.exposure.values[i]
        ax.annotate(f"{v:+.2f}".replace("-", "\u2212"), (i, v), xytext=(0, 4 if v > 0 else -4), textcoords="offset points",
                    ha="center", va="bottom" if v > 0 else "top", color=INK2)
    ax.set_yticks([-0.15, -0.10, -0.05, 0, 0.05, 0.10, 0.15], ["−0.15", "−0.10", "−0.05", "0", "+0.05", "+0.10", "+0.15"])
    ax.set_xlabel("Tenth of households by equivalized disposable income, poorest to richest")
    ax.set_ylabel("Labor's share of income less\nlabor's share of what it buys")
    ax.tick_params(axis="x", length=0)
    ax.plot([], [], color=BLUE, lw=6, label="Paid more by labor than its purchases are made by it")
    ax.plot([], [], color=RED, lw=6, label="Paid less")
    ax.legend(loc="upper left", bbox_to_anchor=(0.0, 1.16), ncol=2, handlelength=0.9, borderaxespad=0, columnspacing=1.6)
    save(fig, "fig_exposure")


def fig_holdings():
    g = pd.read_csv(os.path.join(ROOT, "data", "exposure_groups.csv"))
    g = g[g.year == 2023].set_index("group")
    rows = [("Labor income", "share_of_labour_income"), ("Income of capital and land", "share_of_capital_and_land"),
            ("Transfers", "share_of_transfers"), ("Consumption", "share_of_consumption")]
    groups = [("bottom half", "Poorer half", BLUE), ("next four tenths", "Next four tenths", ORANGE), ("top tenth", "Richest tenth", AQUA)]
    fig, ax = plt.subplots(figsize=(6.6, 2.5))
    gap = 0.004                                                        # the page showing between segments
    for j, (label, col) in enumerate(rows):
        y, left = len(rows) - 1 - j, 0.0
        for key, name, colour in groups:
            v = float(g.loc[key, col])
            ax.add_patch(FancyBboxPatch((left + gap / 2, y - 0.2), v - gap, 0.4, boxstyle="round,pad=0,rounding_size=0.008",
                                        mutation_aspect=12.0, fc=colour, ec="none", zorder=3))
            ax.text(left + gap / 2 + 0.008, y, f"{100 * v:.0f}%", va="center", ha="left", color="white", fontsize=8.5,
                    fontweight="bold", zorder=4)
            left += v
    ax.set_yticks(range(len(rows)), [r[0] for r in rows][::-1])
    ax.tick_params(axis="y", length=0)
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.5, len(rows) - 0.5)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0], ["0", "25%", "50%", "75%", "100%"])
    ax.grid(False)
    ax.spines["left"].set_visible(False)
    for key, name, colour in groups:
        ax.plot([], [], color=colour, lw=6, label=name)
    ax.legend(loc="upper left", bbox_to_anchor=(0.0, 1.17), ncol=3, handlelength=0.9, borderaxespad=0, columnspacing=1.6)
    save(fig, "fig_holdings")


def fig_shift():
    tabs = ex.inputs()
    held, s_now = ex.market_shares(tabs, 2023)
    s = np.linspace(s_now, 0.0, 200)
    fig, axes = plt.subplots(1, 3, figsize=(6.6, 2.7), sharey=True)
    titles = {"bottom half": "Poorer half", "next four tenths": "Next four tenths", "top tenth": "Richest tenth"}
    for ax, (g, h) in zip(axes, held.items()):
        as_now = [ex.income_share(h, x) for x in s]
        common = [ex.income_share(h, x, 0.2) for x in s]
        ax.plot(s, as_now, color=BLUE, lw=LW, zorder=4, label="Holdings as they were in 2023")
        ax.plot(s, common, color=ORANGE, lw=LW, zorder=3, label="A fifth of capital and land held in common")
        ax.axvline(0.17, color=GRID, lw=0.8, zorder=1)
        dot(ax, s_now, as_now[0], BLUE)
        dot(ax, 0.17, ex.income_share(h, 0.17), BLUE)
        dot(ax, 0.17, ex.income_share(h, 0.17, 0.2), ORANGE)
        pct = lambda v: f"{100 * v:.1f}%"
        up = ex.income_share(h, 0.17) > ex.income_share(h, 0.17, 0.2)
        ax.annotate(pct(ex.income_share(h, 0.17)), (0.17, ex.income_share(h, 0.17)), xytext=(0, 7 if up else -7),
                    textcoords="offset points", ha="center", va="bottom" if up else "top", color=INK2)
        ax.annotate(pct(ex.income_share(h, 0.17, 0.2)), (0.17, ex.income_share(h, 0.17, 0.2)), xytext=(0, -7 if up else 7),
                    textcoords="offset points", ha="center", va="top" if up else "bottom", color=INK2)
        above = as_now[0] > common[0]
        ax.annotate(pct(as_now[0]), (s_now, as_now[0]), xytext=(0, 12 if above else -10), textcoords="offset points", ha="center",
                    va="bottom" if above else "top", color=INK2)
        ax.set_title(titles[g], fontweight="normal", color=INK)
        ax.set_xlim(0.80, -0.03)
        ax.set_xticks([0.66, 0.4, 0.17, 0.0], ["0.66\nin 2023", "0.40", "0.17", "0"])
        ax.set_ylim(0, 0.75)
        ax.set_yticks([0, 0.25, 0.5, 0.75], ["0", "25%", "50%", "75%"])
    axes[0].set_ylabel("Share of market income")
    axes[1].set_xlabel("Labor's share of market income, falling to the right")
    axes[0].legend(loc="upper left", bbox_to_anchor=(0.0, 1.36), ncol=2, handlelength=1.6, borderaxespad=0, columnspacing=1.8)
    fig.subplots_adjust(wspace=0.12)
    save(fig, "fig_shift")


def fig_path():
    t = np.linspace(0, 2, 201)
    m = [pp.mix(x) for x in t]
    labour, interest, rent = (np.array([r[k] for r in m]) for k in ("labour", "interest", "rent"))
    cost = np.array([pp.claims(x)["both"] for x in t])
    fig, (a, b) = plt.subplots(1, 2, figsize=(6.6, 2.9), gridspec_kw={"wspace": 0.34})
    edge = dict(lw=1.2, color="white")
    a.fill_between(t, 0, labour, color=BLUE, lw=0, zorder=2)
    a.fill_between(t, labour, labour + interest, color=ORANGE, lw=0, zorder=2)
    a.fill_between(t, labour + interest, 1, color=AQUA, lw=0, zorder=2)
    a.plot(t, labour, zorder=3, **edge)
    a.plot(t, labour + interest, zorder=3, **edge)
    a.text(0.12, 0.28, "Labor", color="white", fontweight="bold", va="center")
    a.text(1.15, 0.36, "Interest", color="white", fontweight="bold", va="center")
    a.text(1.15, 0.83, "Rent", color="white", fontweight="bold", va="center")
    a.axvline(0.77, color=INK2, lw=0.8, zorder=4)
    a.text(0.80, 0.955, "t = 0.77", color="white", fontsize=8, va="center", ha="left")
    a.set_xlim(0, 2)
    a.set_ylim(0, 1)
    a.set_yticks([0, 0.25, 0.5, 0.75, 1.0], ["0", "25%", "50%", "75%", "100%"])
    a.set_xlabel("Technology index t")
    a.set_ylabel("Share of income")
    a.grid(False)
    b.plot(t[t <= 1.5], cost[t <= 1.5], color=BLUE, lw=LW, zorder=3)
    for x in (0.0, 0.77, 1.0):
        y = pp.claims(x)["both"]
        dot(b, x, y, BLUE)
        side = dict(xytext=(7, 6), ha="left", va="bottom") if x == 0.0 else dict(xytext=(-5, 5), ha="right", va="bottom")
        b.annotate(f"{y:.1f}" if y < 10 else f"{y:.0f}", (x, y), textcoords="offset points", color=INK2, **side)
    b.set_yscale("log")
    b.set_yticks([5, 10, 20, 50, 100, 200], ["5", "10", "20", "50", "100", "200"])
    b.minorticks_off()
    b.set_xlim(0, 1.5)
    b.set_ylim(5, 400)
    b.set_xlabel("Technology index t")
    b.set_ylabel("Years of the whole wage bill")
    a.set_title("Who is paid", fontweight="normal")
    b.set_title("What the claims on interest and rent cost", fontweight="normal")
    save(fig, "fig_path")


def fig_bases():
    t = rb.table()
    fig, (a, b) = plt.subplots(1, 2, figsize=(6.6, 2.7), gridspec_kw={"wspace": 0.30})
    a.fill_between(t.index, t.share_dpi_30, t.share_dpi_50, color=BLUE, alpha=0.14, lw=0, zorder=2)
    a.plot(t.index, t.share_dpi_30, color=BLUE, lw=LW, zorder=3)
    a.plot(t.index, t.share_dpi_50, color=BLUE, lw=LW, zorder=3)
    a.text(1986, 0.090, "if land is half of housing", ha="center", va="center", color=INK2, fontsize=8)
    a.text(1986, 0.027, "if it is three tenths", ha="center", va="center", color=INK2, fontsize=8)
    a.set_ylim(0, 0.10)
    a.set_yticks([0, 0.02, 0.04, 0.06, 0.08, 0.10], ["0", "2%", "4%", "6%", "8%", "10%"])
    a.set_title("Site rent, share of disposable income", fontweight="normal")
    b.fill_between(t.index, t.floor_gdp_family4, t.floor_gdp_single, color=BLUE, alpha=0.14, lw=0, zorder=2)
    b.plot(t.index, t.floor_gdp_family4, color=BLUE, lw=LW, zorder=3)
    b.plot(t.index, t.floor_gdp_single, color=BLUE, lw=LW, zorder=3)
    b.text(1976, 0.47, "for a person living alone", ha="left", va="center", color=INK2, fontsize=8)
    b.text(1950, 0.075, "for one of a family of four", ha="left", va="center", color=INK2, fontsize=8)
    for key in ("floor_gdp_family4", "floor_gdp_single"):
        dot(b, 2024, float(t.loc[2024, key]), BLUE)
        b.annotate(f"{100 * float(t.loc[2024, key]):.0f}%", (2024, float(t.loc[2024, key])), xytext=(8, 0), textcoords="offset points",
                   va="center", color=INK2)
    b.set_ylim(0, 0.7)
    b.set_yticks([0, 0.2, 0.4, 0.6], ["0", "20%", "40%", "60%"])
    b.set_title("A poverty-line bundle for everyone, share of GDP", fontweight="normal")
    for ax in (a, b):
        ax.set_xlim(1947, 2030)
        ax.set_xticks([1950, 1975, 2000, 2024])
    save(fig, "fig_bases")


def fig_program():
    tabs = ex.inputs()
    now, matched = pg.gaps(tabs, 2023)
    common, _ = pg.gaps(tabs, 2023, pg.THETA)
    groups = [("bottom half", "Poorer half"), ("next four tenths", "Next four tenths"), ("top tenth", "Richest tenth")]
    fig, ax = plt.subplots(figsize=(6.6, 2.2))
    ax.axvline(100 * matched, color=INK2, lw=0.8, zorder=1)
    ax.text(100 * matched + 1.5, len(groups) - 0.48, f"a matched group: {100 * matched:.0f}", ha="left", va="bottom", color=INK2, fontsize=8)
    for j, (key, name) in enumerate(groups):
        y = len(groups) - 1 - j
        a, b = 100 * now[key]["per_dollar"], 100 * common[key]["per_dollar"]
        ax.plot([a, b], [y, y], color=CONTEXT, lw=2.0, zorder=2, solid_capstyle="round")
        ax.plot([a], [y], marker="o", ms=7.5, mfc=BLUE, mec="white", mew=1.6, zorder=4)
        ax.plot([b], [y], marker="o", ms=7.5, mfc=ORANGE, mec="white", mew=1.6, zorder=4)
        ax.annotate(f"{min(a, b):.0f}", (min(a, b), y), xytext=(-8, 0), textcoords="offset points", ha="right", va="center", color=INK2)
        near = 0 < 100 * matched - max(a, b) < 6                        # a label to the right would sit on the matched line
        ax.annotate(f"{max(a, b):.0f}", (max(a, b), y), xytext=(0, 7) if near else (8, 0), textcoords="offset points",
                    ha="center" if near else "left", va="bottom" if near else "center", color=INK2)
    ax.set_yticks(range(len(groups)), [name for _, name in groups][::-1])
    ax.tick_params(axis="y", length=0)
    ax.set_xlim(0, 106)
    ax.set_ylim(-0.55, len(groups) - 0.15)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xlabel("Cents of income from capital and land for every dollar of labor income")
    ax.grid(False)
    ax.grid(True, axis="x")
    ax.spines["left"].set_visible(False)
    ax.plot([], [], marker="o", ls="", ms=7, mfc=BLUE, mec="white", mew=1.4, label="In 2023")
    ax.plot([], [], marker="o", ls="", ms=7, mfc=ORANGE, mec="white", mew=1.4, label="With a fifth of the claims held in common")
    ax.legend(loc="upper left", bbox_to_anchor=(0.0, 1.24), ncol=2, handletextpad=0.3, borderaxespad=0, columnspacing=1.8)
    save(fig, "fig_program")


if __name__ == "__main__":
    for f in (fig_accounts, fig_exposure, fig_holdings, fig_shift, fig_path, fig_bases, fig_program):
        f()
        print("drew", f.__name__)
