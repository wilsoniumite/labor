# m1_eras.py — M1 of docs/spec.md: the eras, from the dated FRED pull (code/fred.py, cache/fred/).
# Annual averages of each series (complete years), then: output per hour by era (code/eras.py); hours per person 16
# and over (nonfarm business hours index over the civilian noninstitutional population) by era; labor's share (index);
# the 10-year real interest rate (Cleveland Fed, from 1982; TIPS from 2003); land's share of households' owner-
# occupied real estate, 1 - structures at current cost / real estate at market value (the pairing of the companion
# paper's coverage ratio). Writes data/m1_eras.json (every number the text quotes) and data/m1_annual.csv, and draws
# Figure 3 (paper/figures/fig_eras.pdf, .png). Descriptive: no prediction is scored on M1.
# Run from stagnation/:  ../venv/bin/python code/m1_eras.py
import json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams

import eras
import fred
import model

EPS = model.numbers()["eps_base"]          # Lemma 1's elasticity in the instance

ROOT = Path(__file__).resolve().parents[1]
ERAS = eras.ERAS


# Periods the statistical agencies did not collect: a year missing only these is averaged over the rest.
KNOWN_GAPS = {"2025-10": "not collected during the federal government shutdown of October-November 2025 "
                         "(household survey and CPI)"}


def annual(sid):
    """Calendar-year means over complete years; a year missing only a KNOWN_GAPS period is averaged over the periods
    published. Daily series need 240 trading days (a complete year)."""
    s = fred.fetch(sid)
    g = s.groupby(s.index.year)
    n = g.count()
    if sid == "DFII10":
        return g.mean()[n >= 240]
    full = n.max()
    gaps = pd.Series({y: sum(1 for k in KNOWN_GAPS if k.startswith(str(y))) for y in n.index})
    keep = (n == full) | ((n == full - gaps) & (gaps > 0) & (full == 12))
    return g.mean()[keep]


def population_smoothed():
    """CNP16OV with each January's log change replaced by the mean log change of the other months of its year, as
    annual means over the same months annual() keeps (a sensitivity: BLS's January population-control steps)."""
    s = fred.fetch("CNP16OV")
    d = np.log(s).diff()
    jan = d.index.month == 1
    yr = d.index.year
    d[jan] = d[~jan].groupby(yr[~jan]).mean().reindex(yr[jan]).values
    d.iloc[0] = 0.0
    sm = np.exp(np.log(s.iloc[0]) + d.cumsum())
    keep = annual("CNP16OV").index
    return sm.groupby(sm.index.year).mean().loc[keep]


def build():
    a = pd.DataFrame({sid: annual(sid) for sid in ("OPHNFB", "HOANBS", "PRS85006173", "REAINTRATREARAT10Y", "DFII10",
                                                   "HOOREVLMHMV", "BOGZ1LM155012665Q", "CNP16OV")})
    a["hours_per_person"] = a.HOANBS / a.CNP16OV
    a["land_share"] = 1 - a.BOGZ1LM155012665Q / a.HOOREVLMHMV
    return a


def growth(s, y0, y1):
    return 100 * (np.log(s[y1]) - np.log(s[y0])) / (y1 - y0)


def numbers(a):
    out = {"output_per_hour": {f"{y0}-{y1}": growth(a.OPHNFB, y0, y1) for y0, y1 in ERAS},
           "hours_per_person": {f"{y0}-{y1}": growth(a.hours_per_person, y0, y1) for y0, y1 in ERAS if y0 >= 1948}}
    base = out["output_per_hour"]["1948-1973"]
    out["slowdown"] = {f"{y0}-{y1}": base - out["output_per_hour"][f"{y0}-{y1}"] for y0, y1 in ERAS[1:]}
    # Lemma 1 at given technology, land and basket: the elasticity of output per hour with respect to hours lies in
    # (-1, 0), so a swing in the growth of hours per person of g points a year between two eras moves the growth of
    # output per hour by at most g, and by |eps| g at the instance's elasticity (code/model.py). The swing from
    # 1948-73 to 1973-95 is the rise in 1973-95 plus the fall in 1948-73.
    g = out["hours_per_person"]["1973-1995"] - out["hours_per_person"]["1948-1973"]
    out["lemma1_swing_1948_1973_to_1973_1995"] = dict(swing=g, at_most=g, instance=-EPS * g)
    # sensitivity, added after the data were seen: BLS introduces new population controls each January without
    # revising earlier months, so CNP16OV steps each January; with each January's change set to the mean change of the
    # other months of its year, hours per person by era
    hpp_s = a.HOANBS / population_smoothed()
    out["hours_per_person_smoothed"] = {f"{y0}-{y1}": growth(hpp_s, y0, y1) for y0, y1 in ERAS}
    s = np.log(fred.fetch("CNP16OV")).diff().dropna()
    jan = s[s.index.month == 1]
    rest = s[s.index.month != 1]
    step = (jan.groupby(jan.index.year).first() - rest.groupby(rest.index.year).mean()).dropna()
    out["population_january_step"] = dict(max_year=int(step.idxmax()), max_pct=100 * float(step.max()),
                                          y2025_pct=100 * float(step[2025]))
    ls = a.PRS85006173
    out["labor_share"] = dict(level_1948=ls[1948], level_2000=ls[2000], level_2025=ls[2025],
                              pct_1948_2000=100 * (ls[2000] / ls[1948] - 1), pct_2000_2025=100 * (ls[2025] / ls[2000] - 1),
                              min_year=int(ls.idxmin()), min_level=ls.min())
    rr = a.REAINTRATREARAT10Y.dropna()
    out["real_rate"] = dict(avg_1982_1984=rr.loc[1982:1984].mean(), min_year=int(rr.idxmin()), min_value=rr.min(),
                            avg_2023_2025=rr.loc[2023:2025].mean(), tips_2020=a.DFII10[2020],
                            tips_2025=a.DFII10[2025], tips_min_year=int(a.DFII10.dropna().idxmin()))
    land = a.land_share.dropna()
    out["land_share"] = dict(first_year=int(land.index.min()), first=100 * land.iloc[0],
                             avg_1952_1972=100 * land.loc[1952:1972].mean(), avg_2004_2019=100 * land.loc[2004:2019].mean(),
                             peak_year=int(land.idxmax()), peak=100 * land.max(), y2025=100 * land[2025],
                             y1995=100 * land[1995])
    return out


# ------------------------------------------------------------------------------------------------------------ figure
rcParams["font.family"] = "serif"
rcParams["font.serif"] = ["DejaVu Serif"]
rcParams["mathtext.fontset"] = "dejavuserif"
rcParams["pdf.fonttype"] = 42
PRINT_W = 0.88 * 16 / 2.54
rcParams["font.size"] = 8.5
rcParams["xtick.labelsize"] = rcParams["ytick.labelsize"] = 7.5
rcParams["axes.linewidth"] = 0.53
for _ax in ("xtick", "ytick"):
    rcParams[f"{_ax}.major.width"] = rcParams[f"{_ax}.minor.width"] = 0.45
    rcParams[f"{_ax}.major.size"] = 2.3
    rcParams[f"{_ax}.minor.size"] = 1.3
BLUE, ORANGE, INK, MUTED, GRID = "#2a78d6", "#eb6834", "#0b0b0b", "#52514e", "#e4e3df"


def draw(a, nums):
    fig, axs = plt.subplots(2, 2, figsize=(PRINT_W, PRINT_W / 1.45), layout="constrained")
    (a1, a2), (a3, a4) = axs
    yrs = a.index
    a1.plot(yrs, a.OPHNFB, color=BLUE, lw=1.4)
    a1.set_yscale("log")
    a1.set_yticks([25, 50, 100])
    a1.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{y:g}"))
    a1.yaxis.set_minor_formatter(plt.NullFormatter())
    for y0, y1 in eras.ERAS:
        a1.axvline(y0, color=GRID, lw=0.8, zorder=0)
        g = nums["output_per_hour"][f"{y0}-{y1}"]
        a1.text((y0 + y1) / 2, 132, f"{g:.1f}", ha="center", va="bottom", fontsize=6.5, color=MUTED)
    a1.set_ylim(18, 165)
    a1.set_ylabel("Output per hour\n(2017 = 100, log scale)", fontsize=7.5)
    a2.plot(yrs, a.PRS85006173, color=BLUE, lw=1.4)
    a2.set_ylabel("Labor's share\n(2017 = 100)", fontsize=7.5)
    rr, tips = a.REAINTRATREARAT10Y.dropna(), a.DFII10.dropna()
    a3.plot(rr.index, rr, color=BLUE, lw=1.4, label="Cleveland Fed")
    a3.plot(tips.index, tips, color=ORANGE, lw=1.4, label="TIPS yield")
    a3.axhline(0, color=MUTED, lw=0.6, zorder=0)
    a3.set_ylabel("10-year real interest\nrate (percent)", fontsize=7.5)
    a3.legend(frameon=False, fontsize=6.5, loc="upper left", handlelength=1.4)
    a3.set_ylim(-1.3, 8.8)
    land = a.land_share.dropna() * 100
    a4.plot(land.index, land, color=BLUE, lw=1.4)
    a4.set_ylabel("Land's share of household\nreal estate (percent)", fontsize=7.5)
    for ax, tag in ((a1, "(a)"), (a2, "(b)"), (a3, "(c)"), (a4, "(d)")):
        ax.set_xlim(1945, 2027)
        ax.grid(True, which="major", color=GRID, lw=0.5)
        ax.spines[["top", "right"]].set_visible(False)
        ax.tick_params(colors=MUTED, labelcolor=INK)
        ax.text(0.0, 1.02, tag, transform=ax.transAxes, ha="left", va="bottom", fontsize=8.5, color=INK)
    out = ROOT / "paper" / "figures" / "fig_eras.png"
    fig.savefig(out, dpi=300)
    fig.savefig(out.with_suffix(".pdf"), metadata={"CreationDate": None})
    return out


if __name__ == "__main__":
    a = build()
    nums = numbers(a)
    (ROOT / "data").mkdir(exist_ok=True)
    a.to_csv(ROOT / "data" / "m1_annual.csv")
    (ROOT / "data" / "m1_eras.json").write_text(json.dumps(nums, indent=2, default=float))
    print(json.dumps(nums, indent=1, default=lambda v: round(float(v), 3)))
    print("wrote", draw(a, nums))
