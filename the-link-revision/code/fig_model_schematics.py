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
rcParams["mathtext.fontset"] = "dejavuserif"

NAVY, BLUE, RED, GRAY = "#1a1a3d", "#4878b8", "#8b2020", "#c8c8c8"

# ---------------------------------------------------------------- schedule
# 2026-09-02 (her call): the industrial configuration is the template — a
# steep schedule over the tasks machines can reach, then the set H of tasks
# closed to machines (γ_M = 0, γ unbounded), relabeled last and drawn as a
# wall at the right edge. Labor holds H at any wage; the margin lies among
# the reachable tasks. The pre-wall version is in git history.
M_CLOSED = 0.70                      # [M_CLOSED, 1] is H
xo = np.linspace(0, M_CLOSED, 400, endpoint=False)
rho = 0.4 + 3.6 * (xo / M_CLOSED) ** 1.8
wc = 2.0
xstar = M_CLOSED * ((wc - 0.4) / 3.6) ** (1 / 1.8)
YTOP = 5.2

fig, ax = plt.subplots(figsize=(8.6, 4.6), dpi=150)
ax.plot(xo, rho, color=NAVY, lw=2.6, label="relative human productivity γ(x)")
ax.annotate("", xy=(M_CLOSED, YTOP), xytext=(M_CLOSED, float(rho[-1])),
            arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.6, ls="--",
                            shrinkA=0, shrinkB=0, mutation_scale=12))
ax.axhline(wc, color=RED, lw=1.6, ls="--")
ax.axvline(xstar, color="#666666", lw=1.0, ls=":")
ax.fill_between(xo, 0, rho, where=xo <= xstar, color=GRAY, alpha=0.35)
ax.fill_between(xo, 0, rho, where=xo >= xstar, color=BLUE, alpha=0.18)
ax.axvspan(M_CLOSED, 1.0, color=BLUE, alpha=0.10, lw=0)
# labels per her 2026-09-02 ruling on the editorial sheet: short, sentence
# case, mathtext; the argument lives in the caption, not the plot
ax.annotate("$w/c$", xy=(0.025, wc + 0.12), color=RED, fontsize=10.5)
ax.annotate("$x^*$", xy=(xstar + 0.008, 0.18), color="#444444", fontsize=10.5)
ax.annotate(r"Machines: $\gamma(x) < w/c$",
            xy=(0.215, 0.16), ha="center", fontsize=9.5, color="#555555")
ax.annotate(r"Labor: $\gamma(x) > w/c$",
            xy=(0.575, 0.95), ha="center", fontsize=9.5, color=NAVY)
ax.annotate("$H$: tasks closed to machines",
            xy=(0.85, 2.55), ha="center", fontsize=9.5, color="#555555")
ax.set_xlabel(r"Tasks $x$, ordered by increasing $\gamma$; closed tasks last")
ax.set_ylabel(r"Relative human productivity $\gamma(x)$")
ax.set_xlim(0, 1.0); ax.set_ylim(0, YTOP)
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
