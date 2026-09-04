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
code/feasibility_kappa.py). Writes paper/figures/fig_kappa_measurement.png.
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

ROOT = Path(__file__).resolve().parent.parent
GRID = ROOT / "data" / "kappa_results.csv"
OUT = ROOT / "paper" / "figures" / "fig_kappa_measurement.png"

# Frozen from the built grid, 2026-09-01 (guards column drift on rebuilds).
ANCHORS_2025 = {"kappa_med": (0.326, 0.02), "flow_med": (0.326, 0.02),
                "stock_med": (0.303, 0.02)}

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

fig, ax = plt.subplots(figsize=(9, 5))
ax.fill_between(years, kmin, kmax, alpha=0.25,
                label="Min–max range across specifications")
ax.plot(years, kmed, lw=2, label="Median across specifications")
ax.plot(years, stock_med, lw=1.4, linestyle="--", color="C0", alpha=0.8,
        label="Real-estate residual × Treasury yield (median)")
ax.plot(years, flow_med, lw=2.4, color="tab:red",
        label="Share of BEA housing services (median)")
ax.axhline(1.0, color="k", lw=1, ls=":", label=r"$\kappa = 1$ (full coverage)")
ax.set_ylabel(r"Coverage ratio $\kappa = rT/(N \cdot P_s)$")
ax.legend(loc="upper left", fontsize=8, framealpha=1.0)
fig.tight_layout()
fig.savefig(OUT, dpi=150)
print(f"anchors OK (2025: med {built['kappa_med']:.3f}, flow {built['flow_med']:.3f}, "
      f"stock {built['stock_med']:.3f}); wrote {OUT.relative_to(ROOT)}")
