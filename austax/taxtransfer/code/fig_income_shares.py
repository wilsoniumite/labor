"""Blog figure: employees' share and home-ownership share of Australia's total factor income, 1959-60 to 2025-26.

Reads out/income_shares.csv (written by build_facts.py) and writes out/fig_income_shares.png.
No title or notes inside the image (the article supplies them); direct end labels; reference palette slots 1-2.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

HERE = Path(__file__).resolve().parent.parent
d = pd.read_csv(HERE / "out" / "income_shares.csv", index_col=0)
x = [int(fy[:4]) + 1 for fy in d.index]          # financial year ending June, plotted at its end year
assert x[0] == 1960 and x[-1] == 2026, (x[0], x[-1])

LINES = [("Employees' pay", "coe_share_tfi", "#2a78d6"),
         ("Housing owned by households (rents and imputed rents, net of running costs)", "gos_dwellings_share_tfi", "#eb6834")]
INK, MUTED = "#0b0b0b", "#52514e"

fig, ax = plt.subplots(figsize=(10, 5.6))
for name, colname, color in LINES:
    ys = 100 * d[colname].values
    ax.plot(x, ys, color=color, linewidth=1.8, label=name, solid_capstyle="round")
    ax.annotate(f"{ys[-1]:.0f}%", (x[-1], ys[-1]), xytext=(8, 0), textcoords="offset points", va="center",
                fontsize=10.5, color=INK)
peak_i = int(d["coe_share_tfi"].values.argmax())
ax.annotate(f"{100 * d['coe_share_tfi'].values[peak_i]:.0f}% in {d.index[peak_i]}", (x[peak_i], 100 * d["coe_share_tfi"].values[peak_i]),
            xytext=(8, 6), textcoords="offset points", fontsize=10, color=MUTED)
ax.set_xlim(1960, 2026)
ax.set_ylim(0, 70)
ax.set_ylabel("Share of total factor income, per cent (years ending June)", color=INK, fontsize=10.5)
ax.tick_params(colors=MUTED, labelsize=10)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
for side in ("left", "bottom"):
    ax.spines[side].set_color("#c9c8c3")
ax.grid(True, axis="y", color="#e6e5e0", linewidth=0.8)
ax.legend(frameon=False, loc="center left", fontsize=10)
fig.tight_layout()
out = HERE / "out" / "fig_income_shares.png"
fig.savefig(out, dpi=200, bbox_inches="tight", facecolor="white")
print("wrote", out)
