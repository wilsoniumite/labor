# fig_fourway.py — the composition of U.S. consumption financing, 1962–2025
# (Appendix C's figure). Reads data/four_way_split.csv, built by four_way.py.
# Carved verbatim from the long draft's make_figs.py (its Figure 5 block) on
# 2026-09-04; same fonts and grid settings, so the PNG is byte-identical.
# Run from pinning/:  ../venv/Scripts/python.exe code/fig_fourway.py
from pathlib import Path
import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os
ROOT = Path(__file__).resolve().parents[1]
plt.rcParams.update({"font.family": "DejaVu Serif", "font.size": 10.5,
                     "axes.spines.top": False, "axes.spines.right": False,
                     "axes.grid": True, "grid.alpha": 0.22})
FS = (6.9, 3.9)
# ---- Fig 5: real data — deficit-aware financing split
r = pd.read_csv(ROOT / "data" / "four_way_split.csv", index_col=0)
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
OUT = ROOT / "paper" / "figures" / "fig_fourway.png"
fig.tight_layout(); fig.savefig(OUT, dpi=170); plt.close(fig)
print(f"wrote {OUT}")
