# fig_model_schematics.py — three schematics for the rewrite, in its register.
# 1. fig_schedule.png  — the task-assignment margin, WITHOUT wedges (main §3).
# 2. fig_strata.png    — the pay-layer bars in running-example dollars (App B;
#                        uses the wedge vocabulary legitimately, coined terms out).
# 3. fig_ushape.png    — the within-group U-shape, trough now at the 70th–95th
#                        percentiles (fixes the old fig4 defect flagged in the
#                        long draft's handoff list).
# Pure schematics, no data.

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams["font.family"] = "serif"
rcParams["font.serif"] = ["DejaVu Serif", "Georgia"]
rcParams["font.size"] = 11

NAVY, BLUE, RED, GRAY = "#1a1a3d", "#4878b8", "#8b2020", "#c8c8c8"

# ---------------------------------------------------------------- schedule
x = np.linspace(0, 1, 400)
rho = 0.5 + 4.5 * x**1.6
wc = 2.0
xstar = (1.5 / 4.5) ** (1 / 1.6)

fig, ax = plt.subplots(figsize=(8.6, 4.6), dpi=150)
ax.plot(x, rho, color=NAVY, lw=2.6, label="relative human productivity γ(x)")
ax.axhline(wc, color=RED, lw=1.6, ls="--")
ax.axvline(xstar, color="#666666", lw=1.0, ls=":")
ax.fill_between(x, 0, rho, where=x <= xstar, color=GRAY, alpha=0.35)
ax.fill_between(x, 0, rho, where=x >= xstar, color=BLUE, alpha=0.18)
ax.annotate("w/c", xy=(0.025, wc + 0.12), color=RED, fontsize=10.5)
ax.annotate("x*", xy=(xstar + 0.008, 0.18), color="#444444", fontsize=10.5)
ax.annotate("machines hold [0, x*):\nγ(x) < w/c — labor too dear",
            xy=(0.245, 0.16), ha="center", fontsize=9.5, color="#555555")
ax.annotate("labor holds [x*, 1]:\nγ(x) > w/c — the human hour\nreplaces more machine service",
            xy=(0.795, 0.95), ha="center", fontsize=9.5, color=NAVY)
ax.set_xlabel("tasks x, relabeled so γ increases")
ax.set_ylabel("relative human productivity γ(x)")
ax.set_xlim(0, 1.0); ax.set_ylim(0, 5.2)
ax.grid(alpha=0.25, lw=0.5)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig("figures/fig_schedule.png", bbox_inches="tight")
print("wrote figures/fig_schedule.png")

# ------------------------------------------------------------------ strata
# Running-example dollars (main §3 + App B): c=$10, γ(x*)=4 → w=$40; the
# wedged task pays µ·w=$50 at µ=1.25; s=$25; terminal parity c·γ̄=18.
fig, ax = plt.subplots(figsize=(8.6, 4.8), dpi=150)
stages = ["steep schedule,\nwedged task", "wedge rent gone\n(targeted adoption)",
          "schedule flattens\n(premium erodes)", "parity below s:\nrational exit"]
pos = np.arange(4)
floor = [25, 25, 25, 0]
premium = [15, 15, 3, 0]
wedge = [10, 0, 0, 0]
ax.bar(pos[:3], floor[:3], 0.52, color=GRAY, label="exit floor s")
ax.bar(pos[:3], premium[:3], 0.52, bottom=floor[:3], color=BLUE,
       label="task premium c·γ̃(x*) − s")
ax.bar(pos[:1], wedge[:1], 0.52, bottom=[floor[0] + premium[0]], color=RED,
       label="wedge rent (µ−1)·w")
ax.bar(pos[3:], [25], 0.52, facecolor="none", edgecolor="#555555",
       hatch="//", lw=1.2, label="outside option (the exit life)")
ax.axhline(18, color=RED, lw=1.3, ls=":")
ax.annotate("machine parity c·γ̄ = 10 × 1.8 = 18 < s = 25",
            xy=(1.62, 18), xytext=(1.32, 33.5), fontsize=9.5, color=RED,
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.0))
ax.set_xticks(pos); ax.set_xticklabels(stages, fontsize=9.5)
ax.set_ylabel("$ per hour (running example)")
ax.set_ylim(0, 60)
ax.grid(alpha=0.25, lw=0.5, axis="y")
ax.spines[["top", "right"]].set_visible(False)
ax.legend(loc="upper right", framealpha=0.95, fontsize=9.5)
fig.tight_layout()
fig.savefig("figures/fig_strata.png", bbox_inches="tight")
print("wrote figures/fig_strata.png")

# ------------------------------------------------------------------ ushape
xp = np.linspace(0, 100, 500)
dip = -12.0 * np.exp(-((xp - 84.0) / 7.5) ** 2)
fig, ax = plt.subplots(figsize=(8.6, 4.6), dpi=150)
ax.plot(xp, dip, color=NAVY, lw=2.6)
ax.axhline(0, color="#999999", lw=1.0)
for band in (70, 95):
    ax.axvline(band, color="#aaaaaa", lw=0.9, ls=":")
ax.annotate("no-rent jobs:\nonly the base wage moves",
            xy=(22, -2.6), ha="center", fontsize=9.5, color="#555555")
ax.annotate("rent-holding jobs, 70th–95th:\nwedge rents lost with full incidence",
            xy=(56, -9.6), ha="center", fontsize=9.5, color=RED)
ax.annotate("top jobs: protection\nholds the adoption\ndecision, or no wedge",
            xy=(97.5, -4.6), ha="center", fontsize=9.0, color="#555555")
ax.set_xlabel("within-group wage percentile")
ax.set_ylabel("Δ log wage within group (schematic)")
ax.set_xlim(0, 103); ax.set_ylim(-14, 2)
ax.grid(alpha=0.25, lw=0.5)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig("figures/fig_ushape.png", bbox_inches="tight")
print("wrote figures/fig_ushape.png")
