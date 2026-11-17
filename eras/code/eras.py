# eras.py — the synthesis: the schedule's shape below the margin traced from the long record, and the sizes of its
# regions by era. Reads the other scripts' outputs (run pull.py, machines_region.py, skeleton.py, modern_schedule.py first).
#
# (a) The margin's path traces the schedule. The task condition makes the margin's relative human productivity equal
#     the wage over the machine rental, gamma(x*_t) = (w/p_m)_t. If the schedule held still in units of machine
#     services, each year's margin would be a point on it, and the record would draw the schedule below today's margin.
#     x*_t: power accounting to 1870, the model's reading from output per hour after (machines_region.py, central case,
#     band low-high). (w/p_m)_t: average weekly earnings over the implied investment deflator (BoE A47, UK, from 1830),
#     a coarse stand-in for machine prices: it prices structures with machines and catches little of machines' quality
#     gains, so it understates how far machine services cheapened. Both axes scale with output per hour under balanced
#     growth, so part of the shape is built in; the slope is the statement, not the curvature.
# (b) Sizes by era, as shares of the tasks people perform: contestable (skeleton.py; for 2025 also the envelope estimate,
#     modern_schedule.py), behind the ceiling and H (2025 only, from LLM exposure), the rest unsplit where no
#     capability measure exists. The machines' share x* of hand-equivalent work is printed beside each bar.
# Run from eras/:  ../venv/Scripts/python.exe code/eras.py
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

ROOT = Path(__file__).resolve().parents[1]
mr = pd.read_csv(ROOT / "data" / "machines_region.csv")
wp = pd.read_csv(ROOT / "data" / "boe_uk_wages_prices.csv").set_index("year")
theta = pd.read_csv(ROOT / "data" / "theta.csv")
split = pd.read_csv(ROOT / "data" / "split_2025.csv")
S_M, SIGMA = dict(low=0.35, central=0.45, high=0.55), dict(low=0.3, central=0.6, high=0.9)


def xstar(year, case):
    """x* by year: power accounting to 1870, the model reading after (the two agree at 1870 by construction)."""
    kind = "power accounting" if year <= 1870 else "model reading from output per hour"
    q = mr[(mr.kind == kind) & (mr.case == case) & (mr.year == year)]
    return float(q.x_all.iloc[0])


def contestable(t):
    lt = np.log(1 / t)
    return {k: S_M[k] * SIGMA[k] * lt for k in S_M}


# %% (a) the traced schedule
W = (wp.weekly_earnings / wp.investment_deflator).dropna()
yrs = [y for y in W.index if 1830 <= y <= 2016]
pts = pd.DataFrame({"year": yrs, "W": [W[y] / W[2016] for y in yrs],
                    **{f"u_{c}": [1 - xstar(y, c) for y in yrs] for c in ("low", "central", "high")}})
pts.to_csv(ROOT / "data" / "traced_schedule.csv", index=False)
fit = np.polyfit(np.log(pts.u_central), np.log(pts.W), 1)
late = pts[pts.year >= 1870]
fit_late = np.polyfit(np.log(late.u_central), np.log(late.W), 1)
print(f"traced schedule: ln W = {fit[0]:.2f} ln(1 - x*) + c over 1830-2016 ({fit_late[0]:.2f} over 1870-2016); a "
      f"slope of -1 is gamma proportional to 1/(1 - x)")
print(f"W 2016/1830 = {W[2016] / W[1830]:.1f}, W 2016/1870 = {W[2016] / W[1870]:.1f}")

# %% (b) region sizes by era
th_uk = theta[theta.country == "UK"].set_index("year").theta
th_us = theta[theta.country == "US"].groupby("year").theta.median()
eras = [("c. 1700, England & Wales", 1700, None, "power accounting"),
        ("c. 1870, UK", 1870, float(th_uk[1870]), "UK proxy theta"),
        ("c. 1970, UK x*, US theta (1967)", 1970, float(th_us[1967]), "US machinery theta"),
        ("2016-2025, UK x* (2016), US theta (2023)", 2016, float(th_us[2023]), "US machinery theta")]
rows = []
for label, y, t, src in eras:
    xs = {c: xstar(y, c) for c in ("low", "central", "high")}
    con = contestable(t) if t else None
    rows.append(dict(era=label, x_low=xs["low"], x_central=xs["central"], x_high=xs["high"], theta=t,
                     contest_low=con["low"] if con else np.nan, contest_central=con["central"] if con else np.nan,
                     contest_high=con["high"] if con else np.nan))
sizes = pd.DataFrame(rows)
sizes.to_csv(ROOT / "data" / "region_sizes.csv", index=False)
print(sizes.round(3).to_string(index=False))

# %% figure
NAVY, BLUE, RED, GRAY, GOLD, LIGHT = "#1a1a3d", "#4878b8", "#8b2020", "#777777", "#a07a2a", "#c9d6ea"
fig, (a, c) = plt.subplots(1, 2, figsize=(12, 4.8), layout="constrained", gridspec_kw=dict(width_ratios=[1, 1.15]))
a.fill_betweenx(pts.W, pts.u_high, pts.u_low, color=NAVY, alpha=0.12, lw=0)
sc = a.scatter(pts.u_central, pts.W, c=pts.year, cmap="viridis", s=9, zorder=3)
for y in (1830, 1870, 1913, 1950, 1970, 2000, 2016):
    r = pts[pts.year == y].iloc[0]
    a.annotate(str(y), (r.u_central, r.W), textcoords="offset points", xytext=(6, -2), fontsize=7.5)
uu = np.geomspace(0.012, 0.5, 50)
a.plot(uu, np.exp(fit[1]) * uu ** fit[0], color=RED, lw=0.9, ls="--",
       label=rf"fit: $\gamma \propto (1-x)^{{{fit[0]:.2f}}}$")
a.plot(uu, (uu / float(pts.u_central.iloc[-1])) ** -1.0, color=GRAY, lw=0.8, ls=":", label=r"$\gamma \propto 1/(1-x)$")
a.set_xscale("log"); a.set_yscale("log")
a.invert_xaxis()
a.set(xlabel=r"People's share of hand-equivalent work, $1-x^*$ (log, reversed)",
      ylabel="Wage over investment-goods prices, 2016 = 1 (log)",
      title="(a) The margin's path traces the schedule below it, UK 1830-2016\n"
            "(each year's margin is a point; band: low-high cases of $x^*$)")
a.legend(loc="upper left", fontsize=7.5, frameon=False)
fig.colorbar(sc, ax=a, label="year", shrink=0.8)
for i, r in sizes.iterrows():
    y0 = len(sizes) - 1 - i
    if r.era.startswith("2016"):
        b = split[(split.capable_measure == "beta") & (split.contestable_estimate == "formula")].iloc[0]
        segs = [(b.contestable, BLUE, None), (b.behind_ceiling, LIGHT, None), (b.H, "#e8e8e8", None)]
        env_est = split[(split.capable_measure == "beta") & split.contestable_estimate.str.startswith("envelope")]
        c.plot(env_est.contestable, [y0 - 0.36] * len(env_est), "D", color=GOLD, ms=4, zorder=5)
    elif np.isnan(r.contest_central):
        segs = [(1.0, "white", "//")]
        c.text(0.5, y0, "no input-output data: theta, and so the contestable band, not measured", ha="center",
               va="center", fontsize=7.3, color=GRAY, bbox=dict(facecolor="white", edgecolor="none", pad=1.5))
    else:
        segs = [(r.contest_central, BLUE, None), (1 - r.contest_central, "white", "//")]
    left = 0.0
    for wdt, colr, hatch in segs:
        c.barh(y0, wdt, left=left, color=colr, hatch=hatch, edgecolor="#bbbbbb" if hatch else "white", height=0.62)
        if wdt > 0.07 and not hatch:
            c.text(left + wdt / 2, y0, f"{wdt:.0%}", ha="center", va="center", fontsize=7.5)
        left += wdt
    if not np.isnan(r.contest_central):
        c.errorbar(r.contest_central, y0 + 0.36, xerr=[[r.contest_central - r.contest_low],
                                                       [r.contest_high - r.contest_central]],
                   fmt="none", ecolor=NAVY, elinewidth=0.8, capsize=2)
    c.text(-0.02, y0 + 0.02, f"{r.era}\nmachines do {r.x_central:.0%} ({r.x_low:.0%}-{r.x_high:.0%})\n"
           "of hand-equivalent work", ha="right", va="center", fontsize=7.3)
c.set_yticks([])
c.set(xlim=(0, 1), ylim=(-0.6, len(sizes) - 0.4), xlabel="Share of the tasks people perform",
      title="(b) Sizes of the regions by era\n(whisker: contestable band at the low and high assumptions)")
c.plot([], [], "D", color=GOLD, ms=4, label="2025 contestable, envelope estimates (d50, d40, d30)")
c.legend(handles=[Patch(color=BLUE, label=r"contestable, $s_M\sigma\ln(1/\theta)$ central"),
                  c.get_lines()[-1],
                  Patch(color=LIGHT, label="behind the ceiling, LLM-capable (2025)"),
                  Patch(color="#e8e8e8", label="H for LLMs (2025)"),
                  Patch(facecolor="white", hatch="//", edgecolor="#bbbbbb", label="behind the ceiling or H: not split")],
         loc="upper center", bbox_to_anchor=(0.45, -0.12), ncol=2, fontsize=6.8, frameon=False)
for ax in (a, c):
    ax.title.set_fontsize(9)
    ax.grid(alpha=0.25, lw=0.33)
    ax.spines[["top", "right"]].set_visible(False)
c.spines[["left"]].set_visible(False)
fig.savefig(ROOT / "figures" / "eras.png", dpi=200)
print("wrote figures/eras.png, data/traced_schedule.csv, data/region_sizes.csv")
