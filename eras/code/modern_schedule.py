# modern_schedule.py — the US schedule around the margin, 1999-2025, from the companion thread's revealed adoption, and
# the 2025 split of the tasks people perform into contestable, behind the ceiling and H.
#
# Revealed adoption (../companion, Lemma 1 inverted): a task passes to machines when the waterline w/c (wage over a
# quality-adjusted machine price) reaches its relative human productivity, so an occupation that switched in year t sits
# on the schedule at rho = (w/c)_t / (w/c)_1999. The companion detects switches from falls in an occupation's share of
# employment under three rules (d30, d40, d50: 30, 40, 50 percent declines), which also catch demand shifts; its spec
# says so. Members: data/envelope.csv (median of six w/c members), data/flips_*.csv (1999 employment), wc_grid.csv.
# In those units the margin in year t sits at (w/c)_t / (w/c)_1999 and the ceiling at that level over theta_t, theta from
# the lambda thread's machinery series (data/theta.csv, US members, median).
# The 2025 split (shares of the tasks people perform):
#   contestable: two estimates, (i) s_M sigma ln(1/theta) at s_M 0.45, sigma 0.6 (skeleton.py's central case), and
#     (ii) the envelope's own slope: switches covered a share F of 1999 employment while the waterline rose by the
#     factor W = (w/c)_2025/(w/c)_1999, so the log-slope is ln W / F and the band is ln(1/theta) F / ln W.
#   machine-capable: the employment-weighted mean LLM exposure of the occupations still standing in 2025
#     (Eloundou et al., the companion's right tail: data/right_tail_stats.csv), alpha, beta and gamma aggregations,
#     GPT-4 and human raters averaged. Exposure is technical feasibility for LLMs only, so this understates what
#     machines can do (robots and other software add to it).
#   behind the ceiling = capable - contestable; H = 1 - capable.
# Run from eras/:  ../venv/Scripts/python.exe code/modern_schedule.py
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

ROOT = Path(__file__).resolve().parents[1]
COMP = ROOT.parent / "companion" / "data"
RULES = ("d30", "d40", "d50")
S_M, SIGMA = 0.45, 0.6

wc = pd.read_csv(COMP / "wc_grid.csv").set_index("year").wc_median
env = pd.read_csv(COMP / "envelope.csv")
env = env[env.wc_member == "wc_median"]
theta = pd.read_csv(ROOT / "data" / "theta.csv")
theta_us = theta[theta.country == "US"].groupby("year").theta.median()
th = lambda y: float(theta_us[theta_us.index <= y].iloc[-1])          # latest available year at or before y
W = float(wc[2025] / wc[1999])
print(f"waterline 2025/1999: {W:.2f}; theta 1997 {th(1999):.3f}, 2023 {th(2025):.3f}")

# %% the traversed stretch of the schedule, per rule: cumulative 1999-employment share against rho
curves, F = {}, {}
for rule in RULES:
    fl = pd.read_csv(COMP / f"flips_{rule}.csv")
    base = fl.emp_base.sum()
    e = env[env.rule == rule].sort_values("rho_wc")
    curves[rule] = (np.concatenate([[0.0], e.emp_base.cumsum().to_numpy() / base]),
                    np.concatenate([[1.0], e.rho_wc.to_numpy()]))
    F[rule] = float(fl.loc[fl.flipped, "emp_base"].sum() / base)
    print(f"{rule}: {F[rule]:.1%} of 1999 employment switched; envelope log-slope ln W / F = {np.log(W) / F[rule]:.1f} "
          f"(sigma 0.6, s_M 0.45 would give {1 / (S_M * SIGMA):.1f}); implied s_M sigma {F[rule] / np.log(W):.3f}")

# the 1999 view: of the occupations that switched by 2025, how many sat below the 1999 ceiling (contestable then) and how
# many above it (behind the ceiling in 1999, opened as recursive automation lifted it)
c99 = 1 / th(1999)
for rule in RULES:
    e = env[env.rule == rule]
    below = e.loc[e.rho_wc <= c99, "emp_base"].sum() / e.emp_base.sum()
    print(f"{rule}: of the 1999-2025 switches, {below:.0%} (by 1999 employment) sat below the 1999 ceiling "
          f"({c99:.2f}), {1 - below:.0%} above it")

# %% the 2025 split
rt = pd.read_csv(COMP / "right_tail_stats.csv")
cap = {agg: float(rt[rt.variant.str.endswith(agg)].surv_emp_wmean.mean()) for agg in ("alpha", "beta", "gamma")}
lt = np.log(1 / th(2025))
contest = {"formula": S_M * SIGMA * lt, **{f"envelope {r}": lt * F[r] / np.log(W) for r in RULES}}
rows = []
for agg, k in cap.items():
    for name, c in contest.items():
        cc = min(c, k)
        rows.append(dict(capable_measure=agg, contestable_estimate=name, contestable=cc, behind_ceiling=k - cc, H=1 - k))
split = pd.DataFrame(rows)
split.to_csv(ROOT / "data" / "split_2025.csv", index=False)
print(split.round(3).to_string(index=False))

# %% figure
NAVY, BLUE, RED, GRAY, GOLD, LIGHT = "#1a1a3d", "#4878b8", "#8b2020", "#777777", "#a07a2a", "#c9d6ea"
fig, (a, c) = plt.subplots(1, 2, figsize=(11.5, 4.6), layout="constrained", gridspec_kw=dict(width_ratios=[1.25, 1]))
for rule, colr in zip(RULES, (NAVY, BLUE, GOLD)):
    x, y = curves[rule]
    a.step(x, y, where="post", color=colr, lw=1.3, label=f"switched, rule {rule} ({F[rule]:.0%} of 1999 employment)")
for yr, ls in ((1999, ":"), (2005, "--"), (2015, "-."), (2025, "-")):
    m = float(wc[yr] / wc[1999])
    a.axhline(m, color=RED, lw=0.8, ls=ls)
    a.axhline(m / th(yr), color=NAVY, lw=0.8, ls=ls)
    a.text(0.465, m * 1.03, f"margin {yr}", color=RED, fontsize=7, ha="right")
    a.text(0.465, m / th(yr) * 1.03, f"ceiling {yr}", color=NAVY, fontsize=7, ha="right")
a.axvspan(max(F.values()), 0.47, color=GRAY, alpha=0.08, lw=0)
a.text(0.40, 3.2, "still with people\nin 2025: above\nthe 2025 margin", fontsize=7.5, color=GRAY, ha="center")
a.set_yscale("log")
a.set(xlim=(0, 0.47), ylim=(0.9, 20), xlabel="Cumulative share of 1999 employment, ordered by where it sits",
      ylabel="Relative human productivity, 1999 margin = 1 (log)",
      title="(a) The stretch of the schedule the margin crossed, 1999-2025\n"
            "(revealed adoption; margin and ceiling move up it together)")
a.legend(loc="upper left", fontsize=7.2, frameon=False)
labels, lefts = [], []
for i, r in split.iterrows():
    y0 = len(split) - 1 - i
    left = 0.0
    for col, colr in (("contestable", BLUE), ("behind_ceiling", LIGHT), ("H", "#e8e8e8")):
        c.barh(y0, r[col], left=left, color=colr, edgecolor="white", height=0.8)
        if r[col] > 0.06:
            c.text(left + r[col] / 2, y0, f"{r[col]:.0%}", ha="center", va="center", fontsize=7)
        left += r[col]
    labels.append(f"{r.capable_measure}, {r.contestable_estimate}")
c.set_yticks(range(len(split))[::-1], labels, fontsize=7)
c.set(xlim=(0, 1), xlabel="Share of the tasks people perform, 2025",
      title="(b) 2025: where the tasks people perform sit\n(capable: LLM exposure; contestable: two estimates)")
c.legend(handles=[Patch(color=BLUE, label="contestable"), Patch(color=LIGHT, label="behind the ceiling (LLM-capable)"),
                  Patch(color="#e8e8e8", label="H for LLMs (not exposed)")],
         loc="upper center", bbox_to_anchor=(0.5, -0.13), ncol=3, fontsize=7, frameon=False)
for ax in (a, c):
    ax.title.set_fontsize(9)
    ax.grid(alpha=0.25, lw=0.33)
    ax.spines[["top", "right"]].set_visible(False)
fig.savefig(ROOT / "figures" / "modern_schedule.png", dpi=200)
print("wrote figures/modern_schedule.png and data/split_2025.csv")
