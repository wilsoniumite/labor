# s05_care_cores.py — care-related inactivity by sex (lfsa_igar, X) and coresidence by sex (ilc_lvps08, X):
# levels, trends, and how they move with q and with participation. Understanding only (neither series is in the
# frozen manifest by sex). Men's prime-age non-participation by age band: trend, and the link to living with parents.
# Out: s05_care_cores.txt, fig07_care.png, fig08_men_young_cores.png
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as cm  # noqa: E402

W, M, GREY, INK, MUTED = "#eb6834", "#2a78d6", "#8a8984", "#0b0b0b", "#52514e"
df = cm.panel()
out = []


def say(s):
    out.append(str(s))
    print(s)


for s in "FM":
    df[f"care_{s}"] = cm.series_x("igar", sex=s, age="Y25-54", reason="FAM_CARE").reindex(df.index).to_numpy(float)
    df[f"carepo_{s}"] = cm.series_x("igar", sex=s, age="Y25-54", reason="FAM_CARE_PER_OTH").reindex(df.index).to_numpy(float)
    df[f"ill_{s}"] = cm.series_x("igar", sex=s, age="Y25-54", reason="ILL_DIS_OWN").reindex(df.index).to_numpy(float)
    df[f"cores2534_{s}"] = cm.series_x("cores", sex=s, age="Y25-34").reindex(df.index).to_numpy(float)
    df[f"cores2529_{s}"] = cm.series_x("cores", sex=s, age="Y25-29").reindex(df.index).to_numpy(float)
    df[f"neet_inac2529_{s}"] = cm.series_x("neet", sex=s, age="Y25-29", wstatus="INAC").reindex(df.index).to_numpy(float)
d = df.reset_index()

# --- care inactivity: levels and trends
say("care-related inactivity 25-54 (% of population), FAM_CARE / FAM_CARE_PER_OTH:")
t = d[d.year.isin([2008, 2014, 2019, 2024])].pivot_table(index="geo", columns="year",
                                                         values=["care_F", "carepo_F", "care_M"])
say(t.round(1).to_string())
# share of the women's participation gap accounted for by care-related inactivity (2019)
x = d[d.year == 2019].set_index("geo")
x["inact_gap"] = (100 - x.AW2554) - (100 - x.AM2554)
x["care_gap"] = x.carepo_F - x.carepo_M
say("\n2019: inactivity gap W-M 25-54 vs care-related (FAM_CARE_PER_OTH) gap:\n" +
    x[["inact_gap", "care_gap"]].round(1).to_string())
say("mean share of the gap that is care/family/personal: %.2f" % (x.care_gap.sum() / x.inact_gap.sum()))

# care inactivity within country on q and U (FE, X data: understanding only)
for y, lab in (("care_F", "women's care inactivity 25-54 (X) on q"),
               ("carepo_F", "women's care+personal inactivity (X) on q")):
    r = cm.reg(df, y, "logq_l1", ["U_lfs"], side=-1, label=lab)
    say(cm.fmt(r))
r = cm.reg(df, "carepo_F", "U2554_lfs", side=-1, label="women's care+personal inactivity (X) on U25-54")
say(cm.fmt(r))
r = cm.reg(df, "AW2554", "carepo_F", side=-1, label="AW2554 on care+personal inactivity (X), mechanical check")
say(cm.fmt(r))

# --- men's prime-age non-participation by band, trend
say("\nmen's inactivity by band (100 - activity), mean over countries with data in both periods:")
for b in ("25-29", "30-34", "35-39", "40-44", "45-49", "50-54"):
    c = f"AM{b}"
    a1 = d[d.year.between(2005, 2008)].groupby("geo")[c].mean()
    a2 = d[d.year.between(2022, 2025)].groupby("geo")[c].mean()
    k = a1.dropna().index.intersection(a2.dropna().index)
    say(f"  {b}: 2005-08 {100 - a1[k].mean():.1f}  2022-25 {100 - a2[k].mean():.1f}  change {-(a2[k] - a1[k]).mean():+.1f} "
        f"(n={len(k)}; rising in {int(((a2[k] - a1[k]) < 0).sum())})")
dm = (d[d.year.between(2022, 2025)].groupby("geo")["AM25-29"].mean() - d[d.year.between(2005, 2008)].groupby("geo")["AM25-29"].mean())
say("change in men's 25-29 activity, 2005-08 to 2022-25, by country:\n" + dm.round(1).to_string())

# men's coresidence 25-29 vs their participation: within country (X)
for y, x_, sd, lab in (("AM25-29", "cores2529_M", -1, "men 25-29 activity on men's coresidence 25-29 (X)"),
                       ("AF25-29", "cores2529_F", -1, "women 25-29 activity on women's coresidence 25-29 (X)"),
                       ("AM2534", "cores2534_M", -1, "men 25-34 activity on men's coresidence 25-34 (X)")):
    r = cm.reg(df, y, x_, ["U_lfs"], years=(2005, 2025), side=sd, label=lab)
    say(cm.fmt(r))
# coresidence by sex on q (X)
for s in "MF":
    r = cm.reg(df, f"cores2534_{s}", "logq_l1", ["U_lfs"], years=(2005, 2025), side=+1,
               label=f"coresidence 25-34 sex {s} (X) on q")
    say(cm.fmt(r))
xs = d[d.year.between(2017, 2019)].groupby("geo")[["cores2534_M", "cores2534_F", "AM2534", "AF2534",
                                                   "neet_inac2529_M"]].mean()
say("\n2017-19 means:\n" + xs.round(1).to_string())
say("cross-country corr(cores2534_M, AM2534) %.2f; corr(cores2534_M, neet_inac2529_M) %.2f" % (
    xs.corr().loc["cores2534_M", "AM2534"], xs.corr().loc["cores2534_M", "neet_inac2529_M"]))
open(os.path.join(cm.HERE, "s05_care_cores.txt"), "w").write("\n".join(out) + "\n")

# figures
fig, ax = plt.subplots(4, 4, figsize=(10, 8), sharex=True, sharey=True)
for a, g in zip(ax.flat, cm.GEOS):
    z = d[d.geo == g].sort_values("year")
    a.plot(z.year, 100 - z.AW2554, color=W, lw=2)
    a.plot(z.year, z.carepo_F, color=W, lw=1.2, ls="--")
    a.plot(z.year, 100 - z.AM2554, color=M, lw=2)
    a.set_title(g, fontsize=9, loc="left", color=INK)
    a.grid(axis="y", color="#e8e7e2", lw=0.6)
    a.set_ylim(0, 45)
from matplotlib.lines import Line2D
fig.legend([Line2D([], [], color=W, lw=2), Line2D([], [], color=W, lw=1.2, ls="--"), Line2D([], [], color=M, lw=2)],
           ["women inactive 25-54", "women inactive for care/family/personal reasons", "men inactive 25-54"],
           loc="upper right", frameon=False, ncol=3, fontsize=8)
fig.suptitle("Inactivity 25-54 (% of population) and its care-related part", x=0.01, ha="left", color=INK)
fig.tight_layout(rect=(0, 0, 1, 0.95))
fig.savefig(os.path.join(cm.HERE, "fig07_care.png"), dpi=150)

fig, ax = plt.subplots(1, 2, figsize=(10, 4))
ax[0].bar(dm.index, dm.values, color=[M if v >= 0 else GREY for v in dm.values], width=0.6)
ax[0].axhline(0, color="#c9c8c2", lw=0.8)
ax[0].set_title("Men 25-29: change in activity, 2005-08 to 2022-25 (pp)", fontsize=9, loc="left", color=INK)
ax[0].tick_params(axis="x", labelsize=7)
ax[1].scatter(xs.cores2534_M, xs.AM2534, color=M, s=30, edgecolor="white")
for g, r in xs.iterrows():
    ax[1].annotate(g, (r.cores2534_M, r.AM2534), fontsize=6.5, color=MUTED, xytext=(3, 2), textcoords="offset points")
ax[1].set_xlabel("men 25-34 living with parents, 2017-19 (%)")
ax[1].set_ylabel("men's activity 25-34, 2017-19 (%)")
ax[1].set_title("Across countries: coresidence and young men's activity", fontsize=9, loc="left", color=INK)
fig.tight_layout()
fig.savefig(os.path.join(cm.HERE, "fig08_men_young_cores.png"), dpi=150)
