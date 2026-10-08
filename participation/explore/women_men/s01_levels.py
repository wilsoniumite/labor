# s01_levels.py — levels, gap, trends and convergence of prime-age participation by sex (manifest data, nationals).
# Out: fig01_prime_age_by_country.png, fig02_gap_convergence.png, fig03_age_profile_gap.png, s01_levels.csv
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as cm  # noqa: E402

W, M, GREY, INK, MUTED = "#eb6834", "#2a78d6", "#8a8984", "#0b0b0b", "#52514e"
plt.rcParams.update({"font.size": 9, "axes.edgecolor": "#c9c8c2", "axes.labelcolor": MUTED,
                     "xtick.color": MUTED, "ytick.color": MUTED, "axes.spines.top": False,
                     "axes.spines.right": False})
OUT = cm.HERE

df = cm.panel()
d = df.reset_index()
d["gap"] = d["AW2554"] - d["AM2554"]

# --- table: levels in selected years
rows = []
for g in cm.GEOS:
    x = d[d.geo == g].set_index("year")
    def at(c, y):
        return x[c].get(y, np.nan)
    first = x["gap"].dropna()
    rows.append(dict(geo=g, first_year=int(first.index.min()) if len(first) else None,
                     AW_first=at("AW2554", first.index.min()) if len(first) else np.nan,
                     AM_first=at("AM2554", first.index.min()) if len(first) else np.nan,
                     AW2005=at("AW2554", 2005), AM2005=at("AM2554", 2005),
                     AW2019=at("AW2554", 2019), AM2019=at("AM2554", 2019),
                     AW2025=at("AW2554", 2025), AM2025=at("AM2554", 2025),
                     gap2005=at("gap", 2005), gap2019=at("gap", 2019), gap2025=at("gap", 2025)))
T = pd.DataFrame(rows).set_index("geo")
T.round(1).to_csv(os.path.join(OUT, "s01_levels.csv"))
print(T.round(1).to_string())
print("\nmeans:", T[["AW2005", "AM2005", "AW2019", "AM2019", "AW2025", "AM2025", "gap2005", "gap2025"]].mean().round(1).to_dict())

# --- trend of men's prime-age participation per country 2005-2025 (pp per decade, OLS on years, no breaks)
tr = {}
for g in cm.GEOS:
    x = d[(d.geo == g) & d.year.between(2005, 2025)].dropna(subset=["AM2554", "AW2554"])
    if len(x) > 5:
        tr[g] = dict(men=10 * np.polyfit(x.year, x.AM2554, 1)[0], women=10 * np.polyfit(x.year, x.AW2554, 1)[0],
                     n=len(x))
tr = pd.DataFrame(tr).T
print("\ntrend 2005-2025, pp per decade (no break adjustment):\n", tr.round(2).to_string())
print("mean men", tr.men.mean().round(2), "median men", tr.men.median().round(2), "#neg", (tr.men < 0).sum())
print("mean women", tr.women.mean().round(2))

# --- convergence: change in gap 2005->2025 (or 2024 if missing) on gap 2005
c = T[["gap2005", "gap2025"]].dropna()
s = stats.linregress(c.gap2005, c.gap2025 - c.gap2005)
print(f"\nconvergence (gap change 2005-2025 on gap 2005): slope {s.slope:.3f} se {s.stderr:.3f} r {s.rvalue:.2f} n {len(c)}")
sig = d.groupby("year")["gap"].std()
print("cross-country sd of gap by year:", sig.loc[[1998, 2005, 2010, 2015, 2019, 2025]].round(2).to_dict())

# --- figure 1: small multiples, women and men 25-54 by country
fig, axs = plt.subplots(4, 4, figsize=(10, 8.5), sharex=True, sharey=True)
for ax, g in zip(axs.flat, cm.GEOS):
    x = d[d.geo == g].sort_values("year")
    ax.plot(x.year, x.AM2554, color=M, lw=2)
    ax.plot(x.year, x.AW2554, color=W, lw=2)
    ax.set_title(g, fontsize=9, color=INK, loc="left")
    ax.set_ylim(55, 100)
    ax.grid(axis="y", color="#e8e7e2", lw=0.6)
axs[0, 0].text(1997, 92, "men", color=MUTED, fontsize=8)
axs[0, 0].text(1997, 62, "women", color=MUTED, fontsize=8)
fig.suptitle("Activity rate 25-54, nationals (%), 1995-2025 (2020-21 dropped)", x=0.01, ha="left", color=INK)
from matplotlib.lines import Line2D
fig.legend([Line2D([], [], color=M, lw=2), Line2D([], [], color=W, lw=2)], ["men", "women"], loc="upper right",
           frameon=False, ncol=2)
fig.tight_layout(rect=(0, 0, 1, 0.96))
fig.savefig(os.path.join(OUT, "fig01_prime_age_by_country.png"), dpi=150)

# --- figure 2: convergence
fig, ax = plt.subplots(1, 2, figsize=(10, 4))
ax[0].axhline(0, color="#c9c8c2", lw=0.8)
ax[0].scatter(c.gap2005, c.gap2025 - c.gap2005, color=W, s=30, edgecolor="white", lw=1)
for g, r in c.iterrows():
    ax[0].annotate(g, (r.gap2005, r.gap2025 - r.gap2005), fontsize=7, color=MUTED, xytext=(3, 2),
                   textcoords="offset points")
xx = np.linspace(c.gap2005.min(), c.gap2005.max(), 2)
ax[0].plot(xx, s.intercept + s.slope * xx, color=GREY, lw=1)
ax[0].set_xlabel("women minus men, 25-54, 2005 (pp)")
ax[0].set_ylabel("change in the gap 2005-2025 (pp)")
ax[0].set_title(f"Gap closes most where it was widest (slope {s.slope:.2f})", fontsize=9, loc="left", color=INK)
for g in cm.GEOS:
    x = d[d.geo == g].sort_values("year")
    ax[1].plot(x.year, x.gap, color=GREY, lw=0.8, alpha=0.6)
mg = d.groupby("year").gap.mean()
ax[1].plot(mg.index, mg.values, color=W, lw=2.2)
ax[1].set_title("Gap by country (grey) and the equal-weight mean", fontsize=9, loc="left", color=INK)
ax[1].set_ylabel("women minus men, 25-54 (pp)")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "fig02_gap_convergence.png"), dpi=150)

# --- figure 3: age profile of the gap, mean over countries, by period
bands = ["2529", "3034", "3539", "4044", "4549", "5054", "5559", "6064"]
per = {"2005-2008": (2005, 2008), "2014-2017": (2014, 2017), "2022-2025": (2022, 2025)}
prof = {}
for lab, (a, b) in per.items():
    x = d[d.year.between(a, b)]
    prof[lab] = {
        "W": [x.groupby("geo")[f"AF{k[:2]}-{k[2:]}"].mean().mean() for k in bands],
        "M": [x.groupby("geo")[f"AM{k[:2]}-{k[2:]}"].mean().mean() for k in bands]}
print("\nage profile (mean over countries of country means):")
for lab in per:
    print(lab, "W", np.round(prof[lab]["W"], 1), "\n          M", np.round(prof[lab]["M"], 1))
fig, ax = plt.subplots(1, 2, figsize=(10, 3.8))
shade = {"2005-2008": 0.35, "2014-2017": 0.65, "2022-2025": 1.0}
lab_x = [b[:2] + "-" + b[2:] for b in bands]
for lab in per:
    ax[0].plot(lab_x, prof[lab]["W"], color=W, alpha=shade[lab], lw=2, marker="o", ms=4, label=f"women {lab}")
    ax[0].plot(lab_x, prof[lab]["M"], color=M, alpha=shade[lab], lw=2, marker="o", ms=4, label=f"men {lab}")
    ax[1].plot(lab_x, np.array(prof[lab]["W"]) - np.array(prof[lab]["M"]), color=W, alpha=shade[lab], lw=2,
               marker="o", ms=4, label=lab)
ax[0].set_title("Activity rate by age (%), mean of 16 countries", fontsize=9, loc="left", color=INK)
ax[1].set_title("Women minus men by age (pp)", fontsize=9, loc="left", color=INK)
ax[0].legend(fontsize=6.5, frameon=False, ncol=2)
ax[1].legend(fontsize=7, frameon=False)
ax[1].axhline(0, color="#c9c8c2", lw=0.8)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "fig03_age_profile_gap.png"), dpi=150)
