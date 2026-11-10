# essay_figures.py — the figures of essay/essay.md, each from a table or a script that a battery holds.
#
#   fig_hours     what a forty-hour week made in 1973, in hours of 2024, to make and to buy     ../paths/cache/OPHNFB.csv, HOANBS.csv; the panel
#   fig_dollar    where a dollar of consumer spending ends up, 2023                         data/one_basis.csv
#   fig_tenths    what each tenth of households lives on, 2023                              code/exposure.py
#   fig_pay       output per hour and the production worker's hourly pay since 1950         ../paths/cache/OPHNFB.csv; the panel
#   fig_band      a sketch of the argument about the worth of an hour: no data              (none)
#   fig_time      what people given $1,000 a month did with it: transcribed figures         Vivalt and others, as cited
#   fig_split     who is paid as machines improve, in the model economy                     code/paper_path.py
#   fig_buys      what incomes and an hour's pay amount to at the hundredfold point         code/paper_path.py
#   fig_tax       taxing the return on machines against owning a fifth of them              code/paper_path.py
#   fig_dividend  what a holding in common would pay a person, against the poverty line     code/program.py
#   fig_door      what ownership costs in years of wages, and how long saving for it takes  code/paper_path.py, code/program.py
#   fig_shares    each group's share of market income: now, after a large shift, with a fifth in common   code/exposure.py
#   fig_floor     what a poverty-line income for everyone would cost, share of GDP          code/rent_base.py
#   fig_common    who is paid for what along the model's path, under the program            code/program.py
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
import figures as fg  # noqa: E402
import one_basis_tables as obt  # noqa: E402
import paper_path as pp  # noqa: E402
import program as pg  # noqa: E402
import rent_base as rb  # noqa: E402
import wage_shortfall as ws  # noqa: E402
from figures import AQUA, BLUE, CONTEXT, GRID, INK, INK2, MUTED, ORANGE, RED, dot  # noqa: E402

OUT = os.path.join(ROOT, "essay", "figures")
LW = 2.0
PALE_ORANGE = "#f5b89f"                                               # the orange at a lighter step: the public's part of it
plt.rcParams.update({"font.size": 9.5, "legend.fontsize": 9.5, "axes.titlesize": 10})
BOUGHT_FROM = "Source: author's calculations from the national accounts of the U.S. Bureau of Economic Analysis."
MODEL = "Source: author's calculations in a model economy fitted to the United States."
GROUPS = [("bottom half", "Poorer half of households"), ("next four tenths", "Next four tenths"), ("top tenth", "Richest tenth")]


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


def fig_dollar():
    r = obt.made().loc[2023]
    work, owning = r.labour_dollar_psi38, r.comp + r.nos - r.labour_dollar_psi38
    fig, ax = plt.subplots(figsize=(7.2, 2.2))
    segments(ax, 1, [(work, BLUE, f"{100 * work:.0f}¢ pay for work"), (owning, ORANGE, f"{100 * owning:.1f}¢ to owners"),
                     (r.tax, CONTEXT, f"{100 * r.tax:.0f}¢"), (r.imports, CONTEXT, f"{100 * r.imports:.0f}¢")])
    ax.text(work + owning + r.tax / 2, 1.29, "taxes on\nthe product", ha="center", va="bottom", color=INK2, fontsize=8.5, linespacing=1.1)
    ax.text(1.0, 1.29, "imports", ha="right", va="bottom", color=INK2, fontsize=8.5)
    share = work / (work + owning)
    segments(ax, 0, [(share, BLUE, f"{100 * share:.0f}% for work"), (1 - share, ORANGE, f"{100 * (1 - share):.0f}% for owning")])
    ax.set_yticks([1, 0], ["One dollar spent\nby a household", "The part paid to\nAmericans for making it"])
    ax.tick_params(axis="y", length=0)
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.4, 1.78)
    ax.set_xticks([])
    ax.grid(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_visible(False)
    finish(fig, ax, "fig_dollar", "Two-thirds of what we buy is paid for by work, one-third by ownership",
           "Where a dollar of American consumer spending ends up once every stage of production\nis followed back, 2023",
           BOUGHT_FROM, drop=8)


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
    """What a forty-hour week made in 1973, in hours of 2024: the hours it takes to make it (from output per hour, held
    here) and, with the backward model's panel, the hours of ordinary pay it takes to buy it."""
    oph, hours, people = ws.annual("paths/cache/OPHNFB.csv"), ws.annual("paths/cache/HOANBS.csv"), rb.annual(pg.POPULATION)
    make = 40.0 / (oph[2024] / oph[1973])
    a_head = (hours[2024] / hours[1973]) / (people[2024] / people[1973]) - 1.0
    rows = [("A week of work in 1973", 40.0, CONTEXT), ("The hours it takes in 2024\nto make what that week made", make, INK)]
    if panel_path:
        w = pd.read_csv(panel_path).set_index("year")["wage_exshelter"]
        rows.append(("The hours of ordinary pay it takes in 2024\nto buy what that week's pay bought", 40.0 / (w[2024] / w[1973]), BLUE))
    fig, ax = plt.subplots(figsize=(7.2, 2.5))
    for j, (name, v, colour) in enumerate(rows):
        y = len(rows) - 1 - j
        ax.barh(y, v, height=0.56, color=colour, zorder=3)
        ax.annotate(f"{v:.0f} hours", (v, y), xytext=(6, 0), textcoords="offset points", ha="left", va="center", color=INK2)
    ax.set_yticks(range(len(rows)), [r[0] for r in rows][::-1])
    ax.tick_params(axis="y", length=0)
    ax.set_xlim(0, 46)
    ax.set_ylim(-0.55, len(rows) - 0.45)
    ax.set_xticks([0, 10, 20, 30, 40])
    ax.set_xlabel("Hours a week")
    ax.grid(False)
    ax.grid(True, axis="x")
    ax.spines["left"].set_visible(False)
    finish(fig, ax, "fig_hours", "What forty hours made in 1973 takes sixteen hours to make now",
           f"United States. Over the same years the hours worked in business, for each head of population,\nrose by {100 * a_head:.0f} percent. "
           "Ordinary pay is measured against prices other than housing",
           "Source: author's calculations from Bureau of Labor Statistics and Bureau of Economic Analysis series.", drop=48)


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


def fig_door():
    tabs = ex.inputs()
    t = np.linspace(0, 1, 101)
    cost = np.array([pp.claims(x)["both"] for x in t])
    now = pg.gaps(tabs, 2023, pg.THETA)[0]["next four tenths"]["short"]
    later = pg.gaps(tabs, 2023, pg.THETA, pp.mix(1.0)["labour"])[0]["next four tenths"]["short"]
    fig, (a, b) = plt.subplots(1, 2, figsize=(7.2, 3.1), gridspec_kw={"wspace": 0.36, "width_ratios": [1.45, 1]})
    a.plot(t, cost, color=BLUE, lw=LW, zorder=3, clip_on=False)
    for x, off, ha in ((0.0, (8, 8), "left"), (0.77, (-8, 6), "right"), (1.0, (-10, 0), "right")):
        y = pp.claims(x)["both"]
        a.plot([x], [y], marker="o", ms=6.5, mfc=BLUE, mec="white", mew=1.6, zorder=5, clip_on=False)
        a.annotate(f"{y:.1f} years" if y < 10 else f"{y:.0f} years", (x, y), xytext=off, textcoords="offset points", ha=ha,
                   va="bottom" if off[1] else "center", color=INK2)
    improvement(a, 1.0)
    a.set_xlabel("How much better machines are than today's")
    a.set_ylim(0, 52)
    a.set_yticks([0, 10, 20, 30, 40, 50])
    a.set_ylabel("Years of the whole country's wages")
    a.set_title("What all the machines and land cost", fontweight="normal", fontsize=9.5, color=INK2)
    years = [pg.years_to_match(now, 0.05, 0.05), pg.years_to_match(later, 0.05, 0.05)]
    b.set_xlim(-0.6, 1.6)
    b.set_ylim(0, 90)
    for i, v in enumerate(years):
        fg.column(b, i, v, 0.5, BLUE)
        b.annotate(f"{v:.0f} years", (i, v), xytext=(0, 4), textcoords="offset points", ha="center", va="bottom", color=INK2)
    b.set_xticks([0, 1], ["today", "at 100 times"])
    b.tick_params(axis="x", length=0)
    b.set_yticks([0, 25, 50, 75])
    b.set_ylabel("Years of saving 5% of pay")
    b.set_title("How long a household saves\nto buy its share", fontweight="normal", fontsize=9.5, color=INK2)
    finish(fig, a, "fig_door", "Ownership gets harder to buy out of wages the further the shift goes", None,
           MODEL + " The saving is that of the four tenths of\nhouseholds above the middle, with its returns reinvested at 5% a year.", lift=34, drop=48)


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


def fig_dividend():
    tabs = ex.inputs()
    d, p = pg.dividend(tabs, 2023), pg.public_claims(tabs, 2023)
    people = rb.annual(pg.POPULATION)[2023] * 1e3
    k = pg.incomes(tabs, 2023)[1].sum() * 1e9 / people
    growth = [x * k for x in p["growth_share"]]
    social_security = pg.benefits(2023)["social_security_bn"] * 1e9 / people
    line4, line1 = d["a_person"] / d["family4"], d["a_person"] / d["single"]
    rows = [("A fifth of all machines and land,\nheld in common", d["a_person"], ORANGE, None),
            ("of which: today's tax on company\nprofits, turned into a stake", p["corporate_a_person"], PALE_ORANGE, None),
            ("of which: the growth of land rent,\nafter 25 years", growth[1], PALE_ORANGE, growth[0]),
            ("Social Security, for each person\nin the country", social_security, CONTEXT, None),
            ("Poverty line, one member of\na family of four", line4, CONTEXT, None),
            ("Poverty line, a person living alone", line1, CONTEXT, None)]
    fig, ax = plt.subplots(figsize=(7.2, 3.9))
    for j, (name, v, colour, low) in enumerate(rows):
        y = len(rows) - 1 - j
        if low is None:
            ax.barh(y, v, height=0.56, color=colour, zorder=3)
            label = f"\\${v:,.0f}"
        else:
            ax.barh(y, low, height=0.56, color=colour, zorder=3)
            ax.barh(y, v - low, left=low, height=0.56, color=colour, alpha=0.5, zorder=3)
            label = f"\\${low:,.0f} to \\${v:,.0f}"
        ax.annotate(label, (v, y), xytext=(6, 0), textcoords="offset points", ha="left", va="center", color=INK2)
    ax.set_yticks(range(len(rows)), [r[0] for r in rows][::-1])
    ax.tick_params(axis="y", length=0)
    ax.set_xlim(0, 18500)
    ax.set_xticks([0, 5000, 10000, 15000], ["0", "\\$5,000", "\\$10,000", "\\$15,000"])
    ax.set_xlabel("Dollars a person a year, 2023")
    ax.grid(False)
    ax.grid(True, axis="x")
    ax.spines["left"].set_visible(False)
    ax.plot([], [], color=ORANGE, lw=7, label="The dividend")
    ax.plot([], [], color=PALE_ORANGE, lw=7, label="Where most of it could come from")
    ax.plot([], [], color=CONTEXT, lw=7, label="For comparison")
    ax.legend(loc="lower left", bbox_to_anchor=(0.0, 1.0), ncol=3, handlelength=0.9, borderaxespad=0.3, columnspacing=1.6)
    finish(fig, ax, "fig_dividend", "A common fifth would pay every American about \\$4,500 a year",
           "What an equal dividend from a fifth of the income of machines and land would have paid in 2023", BOUGHT_FROM, lift=26, drop=48)


def fig_shares():
    tabs = ex.inputs()
    held, s_now = ex.market_shares(tabs, 2023)
    fig, ax = plt.subplots(figsize=(7.2, 3.0))
    for j, (key, name) in enumerate(GROUPS):
        y = 2 - j
        h = held[key]
        now, shifted, common = (100 * ex.income_share(h, s_now), 100 * ex.income_share(h, 0.17), 100 * ex.income_share(h, 0.17, 0.2))
        ax.plot([shifted, common], [y, y], color=CONTEXT, lw=2.0, zorder=2, solid_capstyle="round")
        ax.plot([now, now], [y - 0.2, y + 0.2], color=INK2, lw=2.2, zorder=3, solid_capstyle="butt")
        ax.plot([shifted], [y], marker="o", ms=9, mfc=RED, mec="white", mew=1.6, zorder=4)
        ax.plot([common], [y], marker="o", ms=9, mfc=INK, mec="white", mew=1.6, zorder=4)
        ax.annotate(f"{now:.0f}%", (now, y + 0.2), xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", color=INK2, fontsize=9)
        ax.annotate(f"{shifted:.0f}%", (shifted, y), xytext=(0, -9), textcoords="offset points", ha="center", va="top", color=INK2, fontsize=9)
        near = abs(common - now) < 4.5
        ax.annotate(f"{common:.0f}%", (common, y), xytext=(0, -9 if near else 9), textcoords="offset points", ha="center",
                    va="top" if near else "bottom", color=INK2, fontsize=9)
    ax.set_yticks(range(3), [name for _, name in GROUPS][::-1])
    ax.tick_params(axis="y", length=0)
    ax.set_xlim(0, 70)
    ax.set_ylim(-0.6, 2.6)
    ax.set_xticks([0, 20, 40, 60], ["0", "20%", "40%", "60%"])
    ax.set_xlabel("Share of all income earned in the market")
    ax.grid(False)
    ax.grid(True, axis="x")
    ax.spines["left"].set_visible(False)
    ax.plot([], [], marker="|", ls="", ms=11, mew=2.2, color=INK2, label="In 2023")
    ax.plot([], [], marker="o", ls="", ms=8, mfc=RED, mec="white", mew=1.4, label="If work were paid 17% of income, with ownership as it is today")
    ax.plot([], [], marker="o", ls="", ms=8, mfc=INK, mec="white", mew=1.4, label="The same, with a fifth of machines and land held in common")
    ax.legend(loc="lower left", bbox_to_anchor=(0.0, 1.0), ncol=1, handletextpad=0.3, borderaxespad=0.3)
    finish(fig, ax, "fig_shares", "A large shift would take most from the middle.\nA common fifth protects the poorer half", None, BOUGHT_FROM, lift=58, drop=48)


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


def fig_common():
    t = np.linspace(0, 2, 201)
    c = [pg.common_income(x) for x in t]
    work, saving, owners, stake, rent = (np.array([r[k] for r in c]) for k in ("work", "saving", "owners_rent", "stake", "rent"))
    fig, ax = plt.subplots(figsize=(7.2, 3.8))
    edge = dict(lw=1.3, color="white")
    levels = np.cumsum([work, saving, owners, stake, rent], axis=0)
    for low, high, colour in ((0 * work, levels[0], BLUE), (levels[0], levels[1], ORANGE), (levels[1], levels[2], CONTEXT),
                              (levels[2], levels[3], PALE_ORANGE), (levels[3], levels[4], AQUA)):
        ax.fill_between(t, low, high, color=colour, lw=0, zorder=2)
    for line in levels[:4]:
        ax.plot(t, line, zorder=3, **edge)
    ax.plot(t, levels[2], color=INK, lw=1.8, zorder=4)
    ax.text(0.06, 0.28, "Pay for work", color="white", fontweight="bold", va="center")
    ax.text(0.98, 0.31, "Income of those who saved\nand own machines", color="white", fontweight="bold", va="center")
    ax.text(1.02, 0.86, "The growth of land rent", color="white", fontweight="bold", va="center")
    ax.text(1.24, 0.603, "The public's fifth of the machines", color=INK, fontweight="bold", va="center", fontsize=9)
    ax.annotate("rent left to those\nwho own land today", (0.13, float(np.interp(0.13, t, levels[1] + owners / 2))), xytext=(0.05, 0.725),
                ha="left", va="center", color="white", fontsize=8.5, fontweight="bold",
                arrowprops=dict(arrowstyle="-", color="white", lw=0.9, shrinkA=1, shrinkB=0), zorder=6)
    improvement(ax)
    ax.set_ylim(0, 1)
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0], ["0", "25%", "50%", "75%", "100%"])
    ax.set_ylabel("Share of all income")
    ax.grid(False)
    held = [100 * pg.common_income(x)["common"] for x in (0.0, 1.0, 2.0)]
    finish(fig, ax, "fig_common", "Under the program, the part held in common grows as work becomes scarce",
           f"Who is paid for what in the model economy. Everything above the dark line is held in common:\n{held[0]:.0f}% of all income today, "
           f"{held[1]:.0f}% when machines are 100 times better, {held[2]:.0f}% at 10,000 times", MODEL, drop=48)


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


VIVALT = dict(monthly=1000, comparison=50, less_income=1900)        # Vivalt and others (2024, 2026), as their summary prints them


def fig_time():
    more = 12 * (VIVALT["monthly"] - VIVALT["comparison"])
    less = VIVALT["less_income"]
    fig, ax = plt.subplots(figsize=(7.2, 1.7))
    segments(ax, 0, [(less / more, BLUE, ""), (1 - less / more, CONTEXT, f"about \\${more - less:,.0f} a year more to live on")], height=0.6)
    ax.text(less / more / 2, 0.36, f"about \\${less:,.0f} a year less\nfrom work and other income", ha="center", va="bottom", color=INK2,
            fontsize=9, linespacing=1.25)
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.4, 0.95)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.grid(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_visible(False)
    finish(fig, ax, "fig_time", "Given money with no conditions, people took about a sixth of it as time",
           f"What 1,000 low-income Americans did with \\$1,000 a month for three years: \\${more:,.0f} a year more than\na comparison group "
           "received, and what happened to their other income",
           "Source: Vivalt and others (2024, 2026); the division is the author's arithmetic on the figures in their summary.", drop=8)


if __name__ == "__main__":
    panel = sys.argv[1] if len(sys.argv) > 1 and os.path.exists(sys.argv[1]) else None
    for f in (fig_dollar, fig_tenths, fig_band, fig_time, fig_split, fig_buys, fig_tax, fig_dividend, fig_door, fig_shares, fig_floor, fig_common):
        f()
        print("drew", f.__name__)
    fig_hours(panel)
    print("drew fig_hours" + ("" if panel else " without its third bar: give the backward model's panel as an argument (see the header)"))
    if panel:
        fig_pay(panel)
        print("drew fig_pay")
    else:
        print("NOT DRAWN  fig_pay: give the backward model's panel as an argument (see the header)")
