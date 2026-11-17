# machines_region.py — how much of the hand-equivalent work non-human power did in England & Wales, 1700-1870, and the
# model's reading of that share from output per hour, 1870-2016. This is the left region of the schedule, [0, x*).
#
# The model's task measure: with gamma_L = 1, each task takes one human-hour per unit of output by hand, so x* is the
# share of hand-hours that non-human inputs perform. A draught animal, a mill or an engine performing a task replaces
# the human-hours that task would take; for power tasks that is its applied mechanical energy over a person's
# sustained power. So, year by year:
#     M = sum over sources of (energy input x conversion efficiency) / (human power x 1 h)     [hand-hours]
#     H = employment x weekly hours x 52                                                         [hours actually worked]
#     x* = M / (M + H)
# Sources (data/): Warde (2007) appendix table 1, energy inputs in PJ (draught-animal feed, wind on sails and windmills,
# water through mill wheels); Warde (2007) table 8, fixed steam horsepower in England & Wales (c.1800 30,000, c.1838
# 140,000, 1870 1,100,000; locomotives and steamships excluded); Bank of England millennium dataset, sheet A1
# (employment from 1760, weekly hours from 1700, population, real GDP, GDP per hour).
# Assumptions (not data; each a band, low/central/high, chosen so x* is monotone in each):
#     human sustained mechanical power      100 / 75 / 50 W           (lower power: more hand-hours per joule)
#     draught animals, feed to work         0.07 / 0.10 / 0.13        (Warde's note 59 and p. 76: about 10 percent)
#     water wheels, input to work           0.15 / 0.25 / 0.40 in 1700, rising linearly to 0.30 / 0.50 / 0.75 in 1870
#                                           (Warde p. 49: undershot wheels 15 percent early, iron wheels 85 percent late)
#     wind, input at the sails to work      0.25 / 0.40 / 0.50        (Warde p. 47: about half lost between sails and motion)
#     steam engines, hours run a year       1,500 / 2,500 / 3,500
#     Wales, relative to England's population: 1.07 (1801 and 1871 censuses: 0.071 and 0.066)
# Before 1760 employment is unknown; it is taken as the 1760 ratio of employment to population.
# After 1870 the model's own accounting takes over: output per final-task hour is 1/(1 - x*), so if every hour saved
# per unit of output came from a task passing to non-human inputs, 1 - x*_t = (1 - x*_1870) P_1870 / P_t, with P GDP
# per hour. That overstates x*, since division of labour, skills and better inputs also raise output per hour.
# The 1760-1870 overlap tests the reading: the power-based and productivity-based paths should move together.
# Run from eras/:  ../venv/Scripts/python.exe code/machines_region.py
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
w = pd.read_csv(ROOT / "data" / "warde_energy_1560_1870.csv").set_index("year")
b = pd.read_csv(ROOT / "data" / "boe_uk_1700_2016.csv").set_index("year")
PJ = 1e15
CASES = ("low", "central", "high")
P_HUMAN = dict(low=100.0, central=75.0, high=50.0)                 # W
ETA_ANIMAL = dict(low=0.07, central=0.10, high=0.13)
ETA_WATER_1700 = dict(low=0.15, central=0.25, high=0.40)
ETA_WATER_1870 = dict(low=0.30, central=0.50, high=0.75)
ETA_WIND = dict(low=0.25, central=0.40, high=0.50)
STEAM_HOURS = dict(low=1500.0, central=2500.0, high=3500.0)
WALES = 1.07
STEAM_HP = {1712: 0.0, 1800: 30_000.0, 1838: 140_000.0, 1870: 1_100_000.0}   # Warde table 8 (Newcomen's first, 1712)


def steam_hp(year):
    """Fixed steam horsepower in England & Wales: linear from 1712 to 1800, log-linear between Warde's later points."""
    if year <= 1712:
        return 0.0
    if year <= 1800:
        return STEAM_HP[1800] * (year - 1712) / (1800 - 1712)
    for (y0, h0), (y1, h1) in zip(list(STEAM_HP.items())[1:], list(STEAM_HP.items())[2:]):
        if year <= y1:
            return h0 * (h1 / h0) ** ((year - y0) / (y1 - y0))
    return STEAM_HP[1870]


def eta_water(case, year):
    f = (year - 1700) / 170
    return ETA_WATER_1700[case] + f * (ETA_WATER_1870[case] - ETA_WATER_1700[case])


# %% human hours, England & Wales: GB+NI employment scaled by the E&W share of population; before 1760 the 1760 ratio
# of employment to population
ew_pop = WALES * b.pop_england
emp_rate_1760 = b.employment[1760] / b.pop_gbni[1760]
emp_ew = (b.employment / b.pop_gbni).fillna(emp_rate_1760) * ew_pop * 1e3          # thousands to people
hours_ew = emp_ew * b.weekly_hours * 52

# %% non-human work in hand-hours, 1700-1870, from Warde's carriers and his steam horsepower
years = np.arange(1700, 1871)
rows = []
for y in years:
    src = w.loc[y]
    for case in CASES:
        joule_per_hand_hour = P_HUMAN[case] * 3600.0
        hh = dict(animals=src.draught_feed * PJ * ETA_ANIMAL[case] / joule_per_hand_hour,
                  water=src.water * PJ * eta_water(case, y) / joule_per_hand_hour,
                  wind=src.wind * PJ * ETA_WIND[case] / joule_per_hand_hour,
                  steam=steam_hp(y) * 746.0 * 3600.0 * STEAM_HOURS[case] / joule_per_hand_hour)
        H = hours_ew[y]
        rows.append(dict(year=y, case=case, human_hours=H, **{f"hh_{k}": v for k, v in hh.items()},
                         x_all=sum(hh.values()) / (sum(hh.values()) + H),
                         x_inanimate=(hh["water"] + hh["wind"] + hh["steam"]) / (hh["water"] + hh["wind"] + hh["steam"] + H),
                         x_no_sails=(hh["animals"] + hh["water"] + hh["steam"]) / (hh["animals"] + hh["water"]
                                                                                    + hh["steam"] + H)))
pw = pd.DataFrame(rows)

# %% output per hour: the A1 series from 1856; before it, real GDP over employment x hours x 52, spliced on the 1856-1870
# overlap (the A1 series is the authority where it exists)
own = b.gdp_real / (b.employment * b.weekly_hours * 52)
ov = b.loc[1856:1870]
scale = float((ov.gdp_per_hour / own.loc[1856:1870]).median())
spread = float((ov.gdp_per_hour / own.loc[1856:1870]).std() / scale)
P = b.gdp_per_hour.where(b.gdp_per_hour.notna(), own * scale)
print(f"output per hour: own construction spliced to A1 at scale {scale:.4g} (1856-70 dispersion {spread:.1%}); "
      f"P_1870/P_1760 = {P[1870] / P[1760]:.2f}, P_2016/P_1870 = {P[2016] / P[1870]:.2f}, P_2016/P_1760 = "
      f"{P[2016] / P[1760]:.1f}")

# %% the overlap test, 1760-1870: does 1 - x* (power-based) fall as output per hour rises?
for case in CASES:
    q = pw[pw.case == case].set_index("year")
    print(f"{case:8s} x* (all non-human power)  1700 {q.x_all[1700]:.2f}  1760 {q.x_all[1760]:.2f}  1800 {q.x_all[1800]:.2f}"
          f"  1838 {q.x_all[1838]:.2f}  1870 {q.x_all[1870]:.2f} | inanimate only 1700 {q.x_inanimate[1700]:.3f}"
          f"  1800 {q.x_inanimate[1800]:.3f}  1870 {q.x_inanimate[1870]:.3f}"
          f" | (1-x*) 1870/1760 {(1 - q.x_all[1870]) / (1 - q.x_all[1760]):.2f} vs P_1760/P_1870 {P[1760] / P[1870]:.2f}")

# %% the model's reading after 1870, anchored at each case's power-based x*_1870
read = []
for case in CASES:
    x1870 = float(pw[(pw.case == case) & (pw.year == 1870)].x_all.iloc[0])
    for y in range(1870, 2017):
        read.append(dict(year=y, case=case, x_star=1 - (1 - x1870) * P[1870] / P[y]))
rd = pd.DataFrame(read)
out = pd.concat([pw.assign(kind="power accounting")[["year", "case", "kind", "x_all", "x_inanimate", "x_no_sails"]],
                 rd.assign(kind="model reading from output per hour").rename(columns={"x_star": "x_all"})])
out.to_csv(ROOT / "data" / "machines_region.csv", index=False)
for y in (1900, 1950, 1970, 2000, 2016):
    v = {c: float(rd[(rd.case == c) & (rd.year == y)].x_star.iloc[0]) for c in CASES}
    print(f"model reading {y}: x* {v['low']:.3f} / {v['central']:.3f} / {v['high']:.3f};  people do "
          f"{1 - v['high']:.1%}-{1 - v['low']:.1%} of the hand-equivalent work")

# %% figure: the share of hand-equivalent work people still do, 1 - x*, on a log scale
NAVY, BLUE, RED, GRAY, GOLD = "#1a1a3d", "#4878b8", "#8b2020", "#777777", "#a07a2a"
fig, (a, c) = plt.subplots(1, 2, figsize=(11, 4.4), layout="constrained", gridspec_kw=dict(width_ratios=[1, 1.35]))
for col, lab, colr in (("x_all", "all non-human power (animals, water, wind, steam)", NAVY),
                       ("x_no_sails", "without sails", BLUE), ("x_inanimate", "inanimate only (water, wind, steam)", GOLD)):
    lo, ce, hi = (pw[pw.case == k].set_index("year")[col] for k in CASES)
    a.fill_between(years, lo, hi, color=colr, alpha=0.18, lw=0)
    a.plot(years, ce, color=colr, lw=1.6, label=lab)
a.set(xlim=(1700, 1870), ylim=(0, 1), xlabel="Year", ylabel="Share of hand-equivalent work, $x^*$",
      title="(a) Non-human power's share, England & Wales\n(Warde's energy series; bands: conversion assumptions)")
a.title.set_fontsize(9)
a.legend(loc="upper left", fontsize=7.5, frameon=False)
for k, ls in zip(CASES, (":", "-", "--")):
    q = pw[pw.case == k].set_index("year")
    c.plot(years, 1 - q.x_all, color=NAVY, lw=1.2 if k == "central" else 0.8, ls=ls)
    r = rd[rd.case == k].set_index("year")
    c.plot(r.index, 1 - r.x_star, color=RED, lw=1.2 if k == "central" else 0.8, ls=ls)
c.plot([], [], color=NAVY, label="power accounting (panel a, all non-human power)")
c.plot([], [], color=RED, label="model reading: $1-x^*\\propto$ 1/(GDP per hour), anchored in 1870")
c.plot(1895, 0.14, "o", color=GOLD, ms=6, mec="white", label="US manufactures c.1895: machine/hand time 0.14\n"
       "(Hand and Machine Labor; Atack, Margo, Rhode 2019)")
c.set_yscale("log")
c.set(xlim=(1700, 2016), ylim=(0.004, 1), xlabel="Year", ylabel="Share people still do, $1-x^*$ (log)",
      title="(b) The machines' region grows toward the whole schedule\n(dotted, solid, dashed: low, central, high cases)")
c.title.set_fontsize(9)
c.legend(loc="lower left", fontsize=7.5, frameon=False)
for ax in (a, c):
    ax.grid(alpha=0.25, lw=0.33)
    ax.spines[["top", "right"]].set_visible(False)
fig.savefig(ROOT / "figures" / "machines_region.png", dpi=200)
print("wrote figures/machines_region.png and data/machines_region.csv")
