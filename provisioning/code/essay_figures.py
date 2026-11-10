# essay_figures.py — the figures of essay/essay.md, each from a table or a script that a battery holds.
#
#   fig_hours     where a forty-hour week of 1973 went: hours to make and to buy it in 2024     ../paths/cache/OPHNFB.csv; the panel
#   fig_tenths    what each tenth of households lives on, 2023                              code/exposure.py
#   fig_pay       output per hour and the production worker's hourly pay since 1950         ../paths/cache/OPHNFB.csv; the panel
#   fig_band      a sketch of the argument about the worth of an hour: no data              (none)
#   fig_split     who is paid as machines improve, in the model economy                     code/paper_path.py
#   fig_buys      what incomes and an hour's pay amount to at the hundredfold point         code/paper_path.py
#   fig_tax       taxing the return on machines against owning a fifth of them              code/paper_path.py
#   fig_floor     what a poverty-line income for everyone would cost, share of GDP          code/rent_base.py
#
# The style, the colours and their validation are figures.py's. One colour means one thing throughout: blue is pay for
# work, orange is income from owning what was built, aqua is income from owning land. Each figure carries its finding as
# a title, since a figure in an essay is often seen without the text around it. Static, for a web page.
#
# fig_pay and the third bar of fig_hours need the backward model's panel, which is on another branch (see
# wage_shortfall.py); give its path:
# Run from provisioning/:  python3 code/essay_figures.py [PATH/TO/us-record/data/panel.csv]      writes essay/figures/*.png

import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import exposure as ex  # noqa: E402
import paper_path as pp  # noqa: E402
import rent_base as rb  # noqa: E402
import wage_shortfall as ws  # noqa: E402
from figures import AQUA, BLUE, CONTEXT, GRID, INK, INK2, MUTED, ORANGE, RED, dot  # noqa: E402

OUT = os.path.join(ROOT, "essay", "figures")
LW = 2.0
PALE_ORANGE = "#f5b89f"                                               # the orange at a lighter step: the public's part of it
plt.rcParams.update({"font.size": 9.5, "legend.fontsize": 9.5, "axes.titlesize": 10})
BOUGHT_FROM = "Source: author's calculations from the national accounts of the U.S. Bureau of Economic Analysis."
MODEL = "Source: author's calculations in a model economy fitted to the United States."


def finish(fig, ax, name, title, sub=None, source=None, lift=6, drop=34):
    """The finding as a title above the axes, a line under it saying what is drawn, the source at the foot; then save.
    `lift` is the room, in points, that a legend above the axes needs; `drop` the room the tick labels and axis label need."""
    up = lift
    if sub:
        ax.annotate(sub, (0, 1), xycoords="axes fraction", xytext=(0, up), textcoords="offset points", ha="left", va="bottom",
                    fontsize=9.5, color=INK2, linespacing=1.25, annotation_clip=False)
        up += 12.5 * (sub.count("\n") + 1) + 4
    ax.annotate(title, (0, 1), xycoords="axes fraction", xytext=(0, up), textcoords="offset points", ha="left", va="bottom",
                fontsize=11.5, fontweight="bold", color=INK, linespacing=1.2, annotation_clip=False)
    if source:
        ax.annotate(source, (0, 0), xycoords="axes fraction", xytext=(0, -drop), textcoords="offset points", ha="left", va="top",
                    fontsize=8, color=MUTED, linespacing=1.25, annotation_clip=False)
    os.makedirs(OUT, exist_ok=True)
    fig.savefig(os.path.join(OUT, name + ".png"), bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)


def segments(ax, y, parts, height=0.5, gap=0.004, size=9.5):
    """One horizontal bar divided into labelled parts of a whole, the page showing between them."""
    left = 0.0
    for value, colour, label in parts:
        ax.barh(y, value - gap, left=left + gap / 2, height=height, color=colour, zorder=3)
        if label:
            ax.text(left + value / 2, y, label, ha="center", va="center", color="white" if colour != CONTEXT else INK, fontsize=size,
                    fontweight="bold", zorder=4)
        left += value


def improvement(ax, upto=2.0):
    """The model's technology index as what it is: how many times better machines are than today's."""
    marks = [(0.0, "today"), (0.5, "10 times"), (1.0, "100 times"), (1.5, "1,000 times"), (2.0, "10,000 times")]
    marks = [m for m in marks if m[0] <= upto + 1e-9]
    ax.set_xlim(0, upto)
    ax.set_xticks([m[0] for m in marks], [m[1] for m in marks])
    ax.set_xlabel("How much better machines are than today's, at every task")


def fig_tenths():
    tabs = ex.inputs()
    a = ex.amounts(tabs, 2023)
    work = a.comp + ex.PSI * a.prop
    owning = (1.0 - ex.PSI) * a.prop + a.rent + a.interest + a.dividends + a.accrued
    total = work + owning + a.benefits
    names = ["Poorest tenth", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "Richest tenth"]
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    for i in range(10):
        y = 9 - i
        w, o, b = work.iloc[i] / total.iloc[i], owning.iloc[i] / total.iloc[i], a.benefits.iloc[i] / total.iloc[i]
        segments(ax, y, [(w, BLUE, f"{100 * w:.0f}%"), (o, ORANGE, f"{100 * o:.0f}%"), (b, CONTEXT, f"{100 * b:.0f}%" if b > 0.06 else "")],
                 height=0.64, size=9)
    ax.set_yticks(range(10), names[::-1])
    ax.tick_params(axis="y", length=0)
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.6, 9.6)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0], ["0", "25%", "50%", "75%", "100%"])
    ax.grid(False)
    ax.spines["left"].set_visible(False)
    ax.plot([], [], color=BLUE, lw=7, label="Pay for work")
    ax.plot([], [], color=ORANGE, lw=7, label="Income from owning")
    ax.plot([], [], color=CONTEXT, lw=7, label="Government benefits")
    ax.legend(loc="lower left", bbox_to_anchor=(0.0, 1.0), ncol=3, handlelength=0.9, borderaxespad=0.3, columnspacing=1.8)
    finish(fig, ax, "fig_tenths", "Nine households in ten live on pay and benefits.\nOne in ten lives half on ownership",
           "Where each tenth of American households gets its income, 2023. Income from owning includes\nthe profits that companies keep",
           BOUGHT_FROM, lift=26)


def fig_hours(panel_path=None):
    """Where a forty-hour week of 1973 went: the hours it takes in 2024 to make what it made (from output per hour, held
    here) and, with the backward model's panel, the hours of ordinary pay it takes to buy what its pay bought."""
    oph = ws.annual("paths/cache/OPHNFB.csv")
    make = 40.0 / (oph[2024] / oph[1973])
    buy = None
    if panel_path:
        w = pd.read_csv(panel_path).set_index("year")["wage_exshelter"]
        buy = 40.0 / (w[2024] / w[1973])
    parts = [(0.0, make, INK, "white", "still needed to make\nwhat the week made", "center")]
    if buy is None:
        parts.append((make, 40.0, CONTEXT, INK, "freed since 1973", "center"))
    else:
        parts.append((make, buy, CONTEXT, INK, "freed, and never reached\nordinary paychecks", "left"))
        parts.append((buy, 40.0, BLUE, "white", "reached ordinary\npay, and was taken\nas more things", "right"))
    fig, ax = plt.subplots(figsize=(7.2, 2.2))
    gap = 0.12
    for left, right, colour, ink, note, align in parts:
        ax.barh(0, right - left - gap, left=left + gap / 2, height=0.62, color=colour, zorder=3)
        ax.text((left + right) / 2, 0, f"{right - left:.0f} hours", ha="center", va="center", color=ink, fontsize=10, fontweight="bold", zorder=4)
        ax.text({"right": right, "left": left + 0.3, "center": (left + right) / 2}[align], -0.46, note, ha=align, va="top", color=INK2,
                fontsize=9, linespacing=1.25)
    ax.plot([make + 0.1, 39.9], [0.52, 0.52], color=INK2, lw=0.9, zorder=3)
    for x in (make + 0.1, 39.9):
        ax.plot([x, x], [0.44, 0.52], color=INK2, lw=0.9, zorder=3)
    ax.text((make + 40.0) / 2, 0.58, f"{40.0 - make:.0f} hours freed since 1973", ha="center", va="bottom", color=INK2, fontsize=9)
    ax.set_xlim(0, 40)
    ax.set_ylim(-1.6, 0.95)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_visible(False)
    finish(fig, ax, "fig_hours", "Where a forty-hour week went",
           "What forty hours of work made in the United States in 1973 takes sixteen hours to make in 2024.\n"
           "Ordinary pay is measured against prices other than housing",
           "Source: author's calculations from Bureau of Labor Statistics series.", drop=4)


def fig_pay(panel_path):
    oph = ws.annual("paths/cache/OPHNFB.csv")
    w = pd.read_csv(panel_path).set_index("year")["wage_exshelter"].dropna()
    years = [y for y in w.index if y in oph.index and y >= 1950]
    made, pay = 100 * oph.loc[years] / oph[1950], 100 * w.loc[years] / w[1950]
    fig, ax = plt.subplots(figsize=(7.2, 3.5))
    ax.axvline(1973, color=GRID, lw=1.0, zorder=1)
    ax.plot(years, made.values, color=INK2, lw=LW, zorder=3)
    ax.plot(years, pay.values, color=BLUE, lw=LW, zorder=4)
    for series, colour, label in ((made, INK2, "what an hour of\nwork produces"), (pay, BLUE, "what an hour of\nordinary pay buys")):
        dot(ax, 2024, series[2024], colour)
        ax.annotate(f"{label}:\n{series[2024] / 100:.1f} times 1950", (2024, series[2024]), xytext=(8, 0), textcoords="offset points", ha="left",
                    va="center", color=INK2, fontsize=9, linespacing=1.2)
    ax.text(1972, 440, "1973", ha="right", va="center", color=MUTED, fontsize=9)
    ax.set_xlim(1950, 2024.5)
    ax.set_ylim(80, 480)
    ax.set_xticks([1950, 1973, 1995, 2024])
    ax.set_yticks([100, 200, 300, 400])
    ax.set_ylabel("1950 = 100")
    fig.subplots_adjust(right=0.76)
    finish(fig, ax, "fig_pay", "Until 1973, ordinary pay kept pace with what an hour produced",
           "Output per hour in American business, and the hourly pay of production and nonsupervisory workers\nafter consumer prices other than shelter",
           "Source: author's calculations from Bureau of Labor Statistics series.")


def fig_split():
    t = np.linspace(0, 2, 201)
    m = [pp.mix(x) for x in t]
    work, machines = (np.array([r[k] for r in m]) for k in ("labour", "interest"))
    fig, ax = plt.subplots(figsize=(7.2, 3.6))
    edge = dict(lw=1.3, color="white")
    ax.fill_between(t, 0, work, color=BLUE, lw=0, zorder=2)
    ax.fill_between(t, work, work + machines, color=ORANGE, lw=0, zorder=2)
    ax.fill_between(t, work + machines, 1, color=AQUA, lw=0, zorder=2)
    ax.plot(t, work, zorder=3, **edge)
    ax.plot(t, work + machines, zorder=3, **edge)
    ax.text(0.06, 0.28, "Pay for work", color="white", fontweight="bold", va="center")
    ax.text(1.02, 0.42, "Income of those who own machines", color="white", fontweight="bold", va="center")
    ax.text(1.02, 0.84, "Income of those who own land", color="white", fontweight="bold", va="center")
    ax.annotate(f"{100 * pp.mix(0.0)['labour']:.0f}%", (0.0, pp.mix(0.0)["labour"]), xytext=(6, -7), textcoords="offset points", ha="left",
                va="top", color="white", fontweight="bold", fontsize=9, zorder=5)
    ax.annotate(f"{100 * pp.mix(1.0)['labour']:.0f}%", (1.0, pp.mix(1.0)["labour"]), xytext=(-5, -9), textcoords="offset points", ha="right",
                va="top", color="white", fontweight="bold", fontsize=9, zorder=5)
    improvement(ax)
    ax.set_ylim(0, 1)
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0], ["0", "25%", "50%", "75%", "100%"])
    ax.set_ylabel("Share of all income")
    ax.grid(False)
    finish(fig, ax, "fig_split", "As machines improve, pay for work becomes a small part of income",
           "Who is paid in a model economy as machines get better at every task and learn to build one another", MODEL, drop=48)


def fig_buys():
    start, one = pp.point(0.0), pp.point(1.0)
    owners = (one["real_income"] * (1 - one["labour"])) / (start["real_income"] * (1 - start["labour"]))
    rows = [("All income in the economy", one["real_income"] / start["real_income"]),
            ("Income of those who own machines and land", owners),
            ("An hour's pay, in goods", one["wage_good"] / start["wage_good"]),
            ("An hour's pay, in everything a household buys", one["real_wage"] / start["real_wage"]),
            ("An hour's pay, in land", one["wage_rent"] / start["wage_rent"])]
    fig, ax = plt.subplots(figsize=(7.2, 3.0))
    ax.axvline(0, color=INK2, lw=0.9, zorder=1)
    for j, (name, v) in enumerate(rows):
        y = len(rows) - 1 - j
        x = np.log10(v)
        ax.barh(y, x, height=0.56, color=(CONTEXT, ORANGE, BLUE, BLUE, BLUE)[j], zorder=3)
        label = f"{v:.0f} times as much" if v > 1 else f"one-{'twelfth' if round(1 / v) == 12 else str(round(1 / v)) + 'th'} as much"
        ax.annotate(label, (max(x, 0.0), y), xytext=(6, 0), textcoords="offset points", ha="left", va="center", color=INK2)
    ax.set_yticks(range(len(rows)), [r[0] for r in rows][::-1])
    ax.tick_params(axis="y", length=0)
    ax.set_xlim(-1.35, 2.75)
    ax.set_xticks([-1, 0, 1, 2], ["a tenth", "as today", "10 times", "100 times"])
    ax.set_ylim(-0.55, len(rows) - 0.4)
    ax.grid(False)
    ax.grid(True, axis="x")
    ax.spines["left"].set_visible(False)
    finish(fig, ax, "fig_buys", "Everyone is richer in goods. What an hour of work no longer buys is land",
           "The model economy when machines are 100 times better than today's, compared with today", MODEL)


def fig_tax():
    tax = pp.interest_tax(0.20)
    fifth = 0.2 * pp.mix(0.0)["interest"]
    rows = [("What the public receives", tax["revenue"], fifth, PALE_ORANGE), ("What happens to all wages", tax["wages"], 0.0, BLUE),
            ("What happens to the size\nof the economy", tax["real_income"] - 1.0, 0.0, CONTEXT)]
    fig, ax = plt.subplots(figsize=(7.2, 3.1))
    ax.axvline(0, color=INK2, lw=0.9, zorder=1)
    h = 0.32
    for j, (name, a, b, colour) in enumerate(rows):
        y = len(rows) - 1 - j
        for value, dy, route in ((a, h / 2 + 0.02, "with the tax"), (b, -h / 2 - 0.02, "with the share")):
            ax.barh(y + dy, 100 * value, height=h, color=colour, zorder=3)
            amount = "no change" if value == 0 else ("+" if value > 0 else "−") + f"{100 * abs(value):.1f}%"
            ax.annotate(f"{amount} {route}", (100 * max(value, 0.0), y + dy), xytext=(5, 0), textcoords="offset points", ha="left",
                        va="center", color=INK2)
    ax.set_yticks(range(len(rows)), [r[0] for r in rows][::-1])
    ax.tick_params(axis="y", length=0)
    ax.set_xlim(-11.5, 11.5)
    ax.set_xticks([-8, -4, 0, 4, 8], ["−8%", "−4%", "0", "+4%", "+8%"])
    ax.set_xlabel("Percent of national income")
    ax.set_ylim(-0.6, len(rows) - 0.4)
    ax.grid(False)
    ax.grid(True, axis="x")
    ax.spines["left"].set_visible(False)
    finish(fig, ax, "fig_tax", "A tax on what machines earn comes out of wages.\nA share in the machines does not",
           "Two ways to give the public a fifth of the income from machines, in the model economy, once\neverything has adjusted: "
           "a 20% tax on what machines earn, and owning a fifth of the machines", MODEL, drop=48)


def fig_floor():
    t = rb.table()
    fig, ax = plt.subplots(figsize=(7.2, 3.3))
    ax.fill_between(t.index, 100 * t.floor_gdp_family4, 100 * t.floor_gdp_single, color=BLUE, alpha=0.14, lw=0, zorder=2)
    ax.plot(t.index, 100 * t.floor_gdp_family4, color=BLUE, lw=LW, zorder=3)
    ax.plot(t.index, 100 * t.floor_gdp_single, color=BLUE, lw=LW, zorder=3)
    ax.text(1962, 47, "at the poverty line for a person living alone", ha="left", va="bottom", color=INK2, fontsize=9)
    ax.text(1949, 12.5, "at the poverty line for one\nmember of a family of four", ha="left", va="top", color=INK2, fontsize=9)
    for key in ("floor_gdp_family4", "floor_gdp_single"):
        v = 100 * float(t.loc[2024, key])
        dot(ax, 2024, v, BLUE)
        ax.annotate(f"{v:.0f}%", (2024, v), xytext=(8, 0), textcoords="offset points", va="center", color=INK2)
    ax.set_xlim(1947, 2030)
    ax.set_xticks([1950, 1975, 2000, 2024])
    ax.set_ylim(0, 70)
    ax.set_yticks([0, 20, 40, 60], ["0", "20%", "40%", "60%"])
    ax.set_ylabel("Share of everything the country produces")
    finish(fig, ax, "fig_floor", "Keeping everyone out of poverty costs a third of what it did in 1955",
           "What it would cost to pay every American a poverty-line income, as a share of GDP", BOUGHT_FROM)


def fig_band():
    """A sketch, not data: jobs laid out by what an hour of them produces, against the wage and against what the hour is
    worth to the person doing it. The band between the two is the work that pays its way and is not worth the time."""
    wage, worth = 0.33, 0.67
    fig, ax = plt.subplots(figsize=(7.2, 2.3))
    segments(ax, 0, [(wage, CONTEXT, ""), (worth - wage, RED, ""), (1 - worth, BLUE, "")], height=0.62)
    ax.text(wage / 2, 0, "Can't pay the wage.\nNobody offers this job.", ha="center", va="center", color=INK, fontsize=9, linespacing=1.3)
    ax.text((wage + worth) / 2, 0, "Pays its way.\nNot worth the time.", ha="center", va="center", color="white", fontsize=9,
            fontweight="bold", linespacing=1.3)
    ax.text((1 + worth) / 2, 0, "Worth doing.", ha="center", va="center", color="white", fontsize=9, fontweight="bold")
    for x, label in ((wage, "the wage the\nworker has to accept"), (worth, "what the hour is worth\nto the person doing it")):
        ax.plot([x, x], [-0.48, 0.48], color=INK, lw=1.4, zorder=5)
        ax.text(x, -0.56, label, ha="center", va="top", color=INK2, fontsize=9, linespacing=1.25)
    ax.annotate("", (0.99, -1.22), xytext=(0.01, -1.22), arrowprops=dict(arrowstyle="->", color=INK2, lw=0.9))
    ax.text(0.5, -1.30, "what an hour of the job produces, from less to more", ha="center", va="top", color=INK2, fontsize=9)
    ax.set_xlim(0, 1)
    ax.set_ylim(-1.62, 0.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_visible(False)
    finish(fig, ax, "fig_band", "Some work pays its way and still isn't worth doing",
           "A sketch of the argument, not a measurement. When a worker cannot refuse, the wage sits below what\nthe hour is worth to them, "
           "and the jobs in between get done", None)


if __name__ == "__main__":
    panel = sys.argv[1] if len(sys.argv) > 1 and os.path.exists(sys.argv[1]) else None
    for f in (fig_tenths, fig_band, fig_split, fig_buys, fig_tax, fig_floor):
        f()
        print("drew", f.__name__)
    fig_hours(panel)
    print("drew fig_hours" + ("" if panel else " without the split of the freed hours: give the backward model's panel as an argument (see the header)"))
    if panel:
        fig_pay(panel)
        print("drew fig_pay")
    else:
        print("NOT DRAWN  fig_pay: give the backward model's panel as an argument (see the header)")
