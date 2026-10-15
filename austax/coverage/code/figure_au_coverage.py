"""Blog figure: Australian land-rent coverage of a basic living standard, 1990-91 to 2024-25.

Reads out/coverage.csv (from build_coverage.py). Styled like the US blog figure
(scratchpad drafts/figure/blog_fig_paycheck_plain.py): no title or notes in the image, direct end labels,
plain legend words, reference palette in fixed order, thin lines, white background, 200 dpi.
"""
import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "out"

with open(OUT / "coverage.csv", newline="") as f:
    rows = list(csv.DictReader(f))
x = [int(r["fy_end"]) for r in rows]
col = lambda k: [float(r[k]) for r in rows]
lo, med, hi = col("coverage_min"), col("coverage_median"), col("coverage_max")
land, rent = col("coverage_median_landvalue_family"), col("coverage_median_rentshare_family")

BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"     # reference categorical slots 1-3, fixed order
INK, MUTED = "#0b0b0b", "#52514e"

fig, ax = plt.subplots(figsize=(10, 5.6))
ax.fill_between(x, lo, hi, color=BLUE, alpha=0.13, linewidth=0, label="Range across 18 estimates")
ax.plot(x, med, color=BLUE, linewidth=2.4, label="All estimates, middle value", solid_capstyle="round")
ax.plot(x, land, color=ORANGE, linewidth=1.5, label="Land values at the bond rate")
ax.plot(x, rent, color=AQUA, linewidth=1.5, label="30 to 50 per cent of housing rents")
for series, name in ((med, "Middle value"), (land, "Land values"), (rent, "Housing rents")):
    ax.annotate(f"{name} {series[-1]:.0%}", (x[-1], series[-1]), xytext=(8, 0), textcoords="offset points",
                va="center", fontsize=10.5, color=INK)
ax.set_xlim(x[0], x[-1])
ax.set_ylim(0, 1.0)
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:.0%}"))
ax.set_xticks([1991, 1995, 2000, 2005, 2010, 2015, 2020, 2025])
ax.set_xlabel("Financial year ending 30 June", color=INK, fontsize=10.5)
ax.set_ylabel("Share of a basic living standard for every resident", color=INK, fontsize=10.5)
ax.tick_params(colors=MUTED, labelsize=10)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
for side in ("left", "bottom"):
    ax.spines[side].set_color("#c9c8c3")
ax.grid(True, axis="y", color="#e6e5e0", linewidth=0.8)
ax.legend(frameon=False, loc="upper left", fontsize=10)
fig.tight_layout()
fig.savefig(OUT / "figure_au_coverage.png", dpi=200, bbox_inches="tight", facecolor="white")
print("wrote", OUT / "figure_au_coverage.png")
