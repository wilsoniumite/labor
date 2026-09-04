# fig_three_drivers.py — the two napkin figures.
#   Figure 1  figures/fig_drivers_scatter.png : crisis value vs market pull, bubble = people pull.
#   Figure 2  figures/fig_majors_underemployment.png : who works in the field they trained for.
#
# Colors are the dataviz reference palette, slots 1-2 (validated order documented in the skill's
# palette.md: adjacent CVD dE 9.1 light; first three slots pass all-pairs). Single-hue where the
# marks are one set; two hues only where the chart encodes a real two-way identity.

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE, ORANGE = "#2a78d6", "#eb6834"
SURFACE, INK, INK2, MUTED, GRID, BASE = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
plt.rcParams.update({
    "font.family": ["Segoe UI", "DejaVu Sans"], "figure.facecolor": SURFACE,
    "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "axes.edgecolor": BASE, "axes.labelcolor": INK2, "xtick.color": MUTED, "ytick.color": MUTED,
    "text.color": INK, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6,
})

NICE = {
    "food_agriculture": "Food & agriculture", "energy": "Energy", "water": "Water",
    "health_social_care": "Health & care", "transport_logistics": "Transport & logistics",
    "communications_it": "IT & communications", "finance_insurance": "Finance & insurance",
    "construction_housing": "Construction & housing", "manufacturing": "Manufacturing",
    "defense_public_safety": "Defense & public safety", "education_research": "Education & research",
    "media_arts_culture": "Media & arts", "government_admin": "Government admin",
    "professional_business": "Professional services", "retail_leisure": "Retail & leisure",
}

# ---------------------------------------------------------------- Figure 1: the three drivers
d = pd.read_csv("data/three_drivers.csv").set_index("sector")
x = d.wagebill_share * 100
y = d.crisis_sources
size = (d.degrees_share.clip(lower=0.004)) * 26000  # area ~ degree share, floored so Water is visible

fig, ax = plt.subplots(figsize=(9.2, 6.0), dpi=200)
ax.set_xscale("log")
ax.scatter(x, y, s=size, color=BLUE, alpha=0.78, edgecolors=SURFACE, linewidths=2, zorder=3)

# label placement tuned by hand after rendering; (dx, dy, ha) in offset points
OFF = {
    "energy": (0, 14, "center"), "government_admin": (0, 14, "center"),
    "defense_public_safety": (0, -22, "center"),
    "transport_logistics": (-14, 4, "right"), "food_agriculture": (0, -22, "center"),
    "water": (0, 13, "center"), "communications_it": (6, 24, "center"),
    "finance_insurance": (-40, -4, "right"),
    "manufacturing": (16, 6, "left"), "construction_housing": (0, -22, "center"),
    "media_arts_culture": (0, -28, "center"),
    "education_research": (-46, -4, "right"), "professional_business": (-56, 6, "right"),
    "retail_leisure": (10, -30, "center"),
}
for s in d.index:
    if s == "health_social_care":  # bubble is large enough to carry its label inside
        ax.annotate(NICE[s], (x[s], y[s]), ha="center", va="center",
                    fontsize=8.6, color=SURFACE, zorder=4)
        continue
    dx, dy, ha = OFF[s]
    ax.annotate(NICE[s], (x[s], y[s]), textcoords="offset points", xytext=(dx, dy),
                ha=ha, fontsize=8.3, color=INK2, zorder=4)

ax.set_yticks(range(0, 8))
ax.set_ylim(-0.6, 8.1)
ax.set_xticks([0.2, 0.5, 1, 2, 5, 10, 20])
ax.set_xticklabels(["0.2%", "0.5%", "1%", "2%", "5%", "10%", "20%"])
ax.set_xlim(0.13, 30)
ax.set_xlabel("share of the 2024 US wage bill  (QCEW, log scale)  —  what the market pays for")
ax.set_ylabel("standing crisis / essential-service lists naming the sector  (of 7)")
ax.set_title("Where the three drivers point: crisis planners vs the market vs students",
             fontsize=12.5, color=INK, loc="left", pad=14)
ax.text(0.155, 7.75, "everyone's crisis lists,\nalmost nobody's paycheck",
        fontsize=8.6, color=MUTED, style="italic", va="top")
ax.text(27, 2.5, "big paycheck,\nno crisis list", fontsize=8.6, color=MUTED,
        style="italic", ha="right")
ax.text(0.155, -0.45,
        "bubble area = share of bachelor's degrees conferred, 2021-22 (NCES; smallest bubbles floored)  ·  "
        "lists: NSM-22, NATO, Finland, UK NRR 2025, MSB NRSB 2025, Lloyd's RDS 2026, WEF GRR 2026",
        fontsize=7.0, color=MUTED)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig("figures/fig_drivers_scatter.png", bbox_inches="tight")
plt.close(fig)
print("wrote figures/fig_drivers_scatter.png")

# ---------------------------------------------------------------- Figure 2: majors vs field jobs
ny = pd.read_csv("data/majors_match_nyfed.csv")

# majors that mainly feed the crisis-heavy sectors (6-7 lists): judgment call, kept coarse
ESSENTIAL = {
    "Agriculture", "Animal and Plant Sciences", "Nursing", "Medical Technicians",
    "Civil Engineering", "Electrical Engineering", "Mechanical Engineering",
    "General Engineering", "Aerospace Engineering", "Computer Engineering",
    "Computer Science", "Nutrition Sciences", "Health Services", "Pharmacy",
    "Environmental Studies", "Miscellaneous Engineering", "Industrial Engineering",
    "Chemical Engineering", "Construction Services", "Public Policy and Law",
}
sel = pd.concat([ny.head(12), ny.tail(12)]).drop_duplicates("major")
sel = sel.sort_values("underemployment_rate")

fig, ax = plt.subplots(figsize=(8.6, 7.4), dpi=200)
ypos = range(len(sel))
colors = [ORANGE if m in ESSENTIAL else BLUE for m in sel.major]
ax.hlines(ypos, 0, sel.underemployment_rate * 100, color=GRID, linewidth=1.2, zorder=2)
ax.scatter(sel.underemployment_rate * 100, ypos, s=64, color=colors,
           edgecolors=SURFACE, linewidths=1.5, zorder=3)
for i, (m, v) in enumerate(zip(sel.major, sel.underemployment_rate * 100)):
    ax.text(v + 1.2, i, f"{v:.0f}%", va="center", fontsize=7.6, color=INK2)
ax.set_yticks(list(ypos))
ax.set_yticklabels(sel.major, fontsize=8.6, color=INK)
ax.set_xlabel("share of employed graduates in jobs not requiring a college degree\n"
              "(NY Fed College Labor Market, outcomes by major; accessed Aug 2026)")
ax.set_title("The twelve best- and worst-matched majors — and where food lands",
             fontsize=12.5, color=INK, loc="left", pad=14)
ax.scatter([], [], s=64, color=ORANGE, label="feeds a sector on 6-7 crisis lists")
ax.scatter([], [], s=64, color=BLUE, label="other majors")
ax.legend(loc="lower right", frameon=False, fontsize=8.6)
ax.set_xlim(0, 78)
ax.grid(axis="y", visible=False)
ax.spines[["top", "right", "left"]].set_visible(False)
fig.tight_layout()
fig.savefig("figures/fig_majors_underemployment.png", bbox_inches="tight")
plt.close(fig)
print("wrote figures/fig_majors_underemployment.png")
