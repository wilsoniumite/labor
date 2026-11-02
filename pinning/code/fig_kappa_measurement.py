"""
fig_kappa_measurement.py — pinning/code

Paper artwork for the coverage-ratio figure (fig:kappa), v5 lineage: the
published 12-member grid (band + median, as in feasibility_kappa.py's
kappa_coverage.png) with the grid's two rent measurements drawn separately —
the eight valuation members (Z.1 land residual x Treasury cap rate, median)
and the four rent-bill members (BEA PCE housing services x land share,
median). Sourcing lives in the LaTeX caption, not on the figure (her call,
2026-09-01); legend wording is the plain register she approved the same day.

Reads the built grid (data/kappa_results.csv — regenerate with
code/feasibility_kappa.py). Writes paper/figures/fig_kappa_measurement.png and,
the same figure in vector form, fig_kappa_measurement.pdf.
No in-figure title: the caption carries it (2026-09-04).

Run from the repo root:
    ./venv/Scripts/python.exe pinning/code/fig_kappa_measurement.py
"""

import csv
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# matplotlib's stock default face, pinned so every machine draws the same figure
# (some installations default to another face); TrueType embedding in the PDF
plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["pdf.fonttype"] = 42
# 2026-11-02, typography pass: the figure is drawn at the width it prints,
# 0.88\textwidth in main.tex (16 cm text width), so sizes here are printed sizes:
# ticks 8 pt, axis label 8.5 pt, legend 7.5 pt. Line widths and tick sizes are the
# earlier values (a 9 in canvas) times 0.616, the scale they printed at, so the
# plot keeps its weight on the page.
PRINT_W = 0.88 * 16 / 2.54             # inches
plt.rcParams["font.size"] = 8.5
plt.rcParams["xtick.labelsize"] = plt.rcParams["ytick.labelsize"] = 8
plt.rcParams["axes.linewidth"] = 0.49
for _ax in ("xtick", "ytick"):
    plt.rcParams[f"{_ax}.major.width"] = 0.49
    plt.rcParams[f"{_ax}.major.size"] = 2.15

ROOT = Path(__file__).resolve().parent.parent
GRID = ROOT / "data" / "kappa_results.csv"
OUT = ROOT / "paper" / "figures" / "fig_kappa_measurement.png"

# Frozen from the built grid, 2026-09-01 (guards column drift on rebuilds).
# 2026-11-02: kappa_med and stock_med re-anchored after the Z.1 land residual was matched to households
# (HOOREVLMHMV in place of HNOREMV; STATE Open 10). Before: kappa_med 0.326, stock_med 0.303.
ANCHORS_2025 = {"kappa_med": (0.298, 0.02), "flow_med": (0.326, 0.02),
                "stock_med": (0.250, 0.02)}

years, kmin, kmed, kmax, flow_med, stock_med = [], [], [], [], [], []
with open(GRID, newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        years.append(int(r["year"]))
        kmin.append(float(r["kappa_min"]))
        kmed.append(float(r["kappa_med"]))
        kmax.append(float(r["kappa_max"]))
        flow_med.append(float(np.median([float(r[c]) for c in r
                                         if c.startswith("k_flow_") and r[c]])))
        stock_med.append(float(np.median([float(r[c]) for c in r
                                          if c.startswith("k_z1_") and r[c]])))

i25 = years.index(2025)
built = {"kappa_med": kmed[i25], "flow_med": flow_med[i25], "stock_med": stock_med[i25]}
bad = [f"{k} {v:.3f} vs {t}±{tol}" for k, (t, tol) in ANCHORS_2025.items()
       if abs((v := built[k]) - t) > tol]
if bad:
    raise SystemExit("BLOCKED — grid anchors failed: " + "; ".join(bad))

# the earlier 9 x 5 in canvas (3.08 in tall as printed) had its legend inside the
# axes; at a legible size it would cover the 1980s peak of the band, so it sits
# below the axes in two columns. The figure is 0.19 in taller and the plot a
# little flatter (width/height 2.02, was 1.82): the most height that keeps this
# figure on the same page as Figure 5 in main.tex as of 2026-11-02 (3.29 in)
fig, ax = plt.subplots(figsize=(PRINT_W, 3.27), layout="constrained")
ax.fill_between(years, kmin, kmax, alpha=0.25,
                label="Min–max range across specifications")
ax.plot(years, kmed, lw=1.23, label="Median across specifications")
ax.plot(years, stock_med, lw=0.86, linestyle="--", color="C0", alpha=0.8,
        label="Real-estate residual × Treasury yield (median)")
ax.plot(years, flow_med, lw=1.48, color="tab:red",
        label="Share of BEA housing services (median)")
ax.axhline(1.0, color="k", lw=0.62, ls=":", label=r"$\kappa = 1$ (full coverage)")
ax.set_ylabel(r"Coverage ratio $\kappa = rT/(N \cdot P_s)$")
handles, labels = ax.get_legend_handles_labels()
order = [0, 2, 4, 1, 3]                 # rows read in the earlier legend's order
fig.legend([handles[i] for i in order], [labels[i] for i in order],
           loc="outside lower center", ncol=2, fontsize=7.5, frameon=False,
           columnspacing=1.5, labelspacing=0.3, borderpad=0.2)
fig.savefig(OUT, dpi=300)
fig.savefig(OUT.with_suffix(".pdf"), metadata={"CreationDate": None})
print(f"anchors OK (2025: med {built['kappa_med']:.3f}, flow {built['flow_med']:.3f}, "
      f"stock {built['stock_med']:.3f}); wrote {OUT.relative_to(ROOT)} and {OUT.with_suffix('.pdf').name}")
