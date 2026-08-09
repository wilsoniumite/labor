# make_figs.py — five figures for the standalone Link document
import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os
os.makedirs("figures", exist_ok=True)
plt.rcParams.update({"font.family": "DejaVu Serif", "font.size": 10.5,
                     "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.alpha": 0.22})
FS = (6.9, 3.9)

# ---- Fig 1: the effective schedule, wedges as negative altitude, two waterlines
x = np.linspace(0, 1, 600)
rho = 0.8 + 4.2 * x**1.35
mu = np.ones_like(x)
mu[(x > 0.52) & (x < 0.66)] = 1.28
mu[(x > 0.80) & (x < 0.88)] = 1.15
rho_eff = rho / mu
w1, w2 = 1.818, 2.00
fig, ax = plt.subplots(figsize=FS)
ax.plot(x, rho, ls="--", lw=1.2, color="#999", label="raw edge ρ(x)")
ax.plot(x, rho_eff, lw=2.0, color="#1a1a3d", label="effective edge ρ̃(x) = ρ(x)/µ(x)")
ax.axhline(w1, color="#8c2d2d", lw=1.3, ls=":", label="waterline w/c (today)")
ax.axhline(w2, color="#8c2d2d", lw=1.3, ls="-.", alpha=0.7, label="waterline after an automation advance")
ax.fill_between(x, 0, 5.2, where=(rho_eff <= w1), color="#c9c9c9", alpha=0.45)
ax.annotate("machines", (0.13, 0.55), fontsize=10, color="#444")
ax.annotate("labor", (0.75, 0.55), fontsize=10, color="#444")
ax.annotate("wedge pocket:\nartificially low altitude,\nflooded first", (0.585, 2.12), fontsize=8.6,
            ha="center", va="bottom", color="#8c2d2d",
            xytext=(0.62, 3.55), arrowprops=dict(arrowstyle="->", color="#8c2d2d", lw=1))
ax.annotate("marginal task x*", (0.35, w1), xytext=(0.16, 2.6), fontsize=8.6,
            arrowprops=dict(arrowstyle="->", color="#333", lw=0.9))
ax.set_xlabel("tasks x, ordered by raw human edge ρ(x)"); ax.set_ylabel("human edge over machines")
ax.set_ylim(0, 5.2); ax.set_xlim(0, 1); ax.legend(fontsize=8, loc="upper left", framealpha=0.9)
fig.tight_layout(); fig.savefig("figures/fig1_schedule.png", dpi=170); plt.close(fig)

# ---- Fig 2: three schedules (the arcs)
fig, ax = plt.subplots(figsize=FS)
ax.plot(x, 0.3 + 8.0 * x**2.0, lw=2.0, color="#1a1a3d", label="industrial era: dispersed, steep")
ax.plot(x, 0.9 + 5.5 * x**2.4, lw=2.0, color="#4c72b0", label="computing: flattened at the simple end")
ax.plot(x, 0.85 + 1.2 * x**2.2, lw=2.0, color="#8c2d2d", label="AI: flattening becomes general")
ax.annotate("level falls and slope falls —\ntwo separate injuries", (0.99, 2.25), fontsize=9,
            ha="right", va="bottom", color="#8c2d2d")
ax.set_xlabel("tasks x"); ax.set_ylabel("effective human edge ρ̃(x)")
ax.set_ylim(0, 8.6); ax.legend(fontsize=8.5, loc="upper left")
fig.tight_layout(); fig.savefig("figures/fig2_arcs.png", dpi=170); plt.close(fig)

# ---- Fig 3: stratigraphy demolition
stages = ["industrial era", "wedges\ndemolished", "link\neroded", "corner-below:\nexit"]
floor_, link_, wedge_ = [25, 25, 25, 0], [15, 15, 3, 0], [10, 0, 0, 0]
fig, ax = plt.subplots(figsize=(6.9, 4.3))
idx = np.arange(4)
ax.bar(idx, floor_, 0.55, color="#c9c9c9", label="exit floor s")
ax.bar(idx, link_, 0.55, bottom=floor_, color="#4c72b0", label="link premium c·ρ̃(x*) − s")
ax.bar(idx, wedge_, 0.55, bottom=np.array(floor_) + np.array(link_), color="#8c2d2d", label="wedge rent (µ−1)·w")
ax.bar([3], [25], 0.55, color="none", edgecolor="#777", hatch="//", label="outside option (the woods, the family)")
ax.axhline(18, color="#8c2d2d", lw=1.1, ls=":")
ax.annotate("machine parity\nc·ρ̄ = 10 × 1.8 = 18 < s = 25", (2.55, 18.8), fontsize=8.4,
            color="#8c2d2d", ha="center", va="bottom", xytext=(2.75, 29.5),
            arrowprops=dict(arrowstyle="->", color="#8c2d2d", lw=0.8))
for i, t in enumerate(["", "targeted\nautomation", "schedule\nflattens", "parity < s:\nrational exit"]):
    ax.annotate(t, (i, 53), ha="center", fontsize=8.2, color="#333")
ax.set_xticks(idx); ax.set_xticklabels(stages, fontsize=9)
ax.set_ylabel("$ per hour (running example)"); ax.set_ylim(0, 60)
ax.legend(fontsize=8, loc="lower center", bbox_to_anchor=(0.5, 1.01), ncol=2,
          framealpha=0.95, borderaxespad=0.0)
fig.tight_layout(); fig.savefig("figures/fig3_strata.png", dpi=170); plt.close(fig)

# ---- Fig 4: U-shape within-group prediction (schematic)
p = np.linspace(0, 1, 400); M = 0.30
t = np.clip((p - M) / (0.99 - M), 0, 1)
shape = t**2.2 * (1 - t)**0.4
y = np.where(p <= M, 0.0, -12 * shape / shape.max())
fig, ax = plt.subplots(figsize=FS)
ax.plot(p * 100, y, lw=2.0, color="#1a1a3d")
ax.axhline(0, color="#999", lw=0.9)
ax.axvline(30, color="#999", lw=0.8, ls=":")
ax.annotate("no-rent jobs:\nonly the base wage moves", (-0.5, -3.4), fontsize=8.6, color="#444")
ax.annotate("wedge-job holders:\nrents demolished,\nfull incidence", (47, -11.4), fontsize=8.6, color="#8c2d2d")
ax.annotate("unautomatable\nrent jobs", (88, -2.6), fontsize=8.6, color="#444", ha="center")
ax.set_xlabel("within-group wage percentile"); ax.set_ylabel("Δ log wage relative to 30th pctile (schematic)")
ax.set_ylim(-14, 2)
fig.tight_layout(); fig.savefig("figures/fig4_ushape.png", dpi=170); plt.close(fig)

# ---- Fig 5: real data — deficit-aware financing split
r = pd.read_csv("data/four_way_split.csv", index_col=0)
m = r[["wage_direct_med", "wagetax_med", "ownertax_med", "borrowed_med"]] * 100
fig, ax = plt.subplots(figsize=(6.9, 4.1))
labels = ["direct wages", "transfers from wage taxes", "transfers from ownership taxes", "transfers from borrowing"]
colors = ["#1a1a3d", "#4c72b0", "#8c2d2d", "#b0803c"]
for c, lab, col in zip(m.columns, labels, colors):
    ax.plot(m.index, m[c], lw=1.9, label=lab, color=col)
ax.fill_between(r.index, r["borrowed_min"] * 100, r["borrowed_max"] * 100, alpha=0.13, color="#b0803c")
ax.axvspan(1998, 2000, color="#4c9c6b", alpha=0.13)
ax.annotate("1998–2000: the only\nfully tax-financed years", (2000.6, 46), fontsize=8.2, color="#2c6b47")
for yr in (2009, 2021):
    ax.annotate("", (yr, m.loc[yr, "borrowed_med"] + 1.2), xytext=(yr, m.loc[yr, "borrowed_med"] + 4.5),
                arrowprops=dict(arrowstyle="->", color="#b0803c", lw=1.1))
ax.annotate("crisis borrowing", (2001, 20.3), fontsize=8.2, color="#7a5a2a")
ax.set_ylabel("% of non-owner-loop consumption financing")
ax.set_xlabel("year"); ax.set_ylim(0, 100)
ax.legend(fontsize=8, loc="center left", framealpha=0.95)
fig.tight_layout(); fig.savefig("figures/fig5_fourway.png", dpi=170); plt.close(fig)
print("figures written:", sorted(os.listdir("figures")))
