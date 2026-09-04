"""
build_fullband_df_figures.py — pinning/effort (Figure 5 of the paper)

Proposed replacements for two frozen figures, fixing a guardrail violation.

The archive's own strong/weak memo (source_manifests/LONGRUN_STRONG_WEAK_MEMO.md,
"Guardrail") says a weak historical estimate becomes unacceptable if "the
uncertainty band is omitted". The frozen FIG_DF and FIG_DFQ draw the
partial-identification band over the strong 2004-2023 window only, while
DF21 carries lower/upper bounds for every year — so the weakest stretch of
the series (1950-2003 bounds reach 63-92%) is the one stretch drawn as a
bare line. These variants draw the weak-year bounds too, at a lighter tint
so weak stays visually distinct from strong.

Reads only frozen inputs (archive_v28/expected). The D-F figure is written to
figures/; the D-F/Q synthesis is the paper's Figure 5 and is written to
paper/figures/fig_consumption_financing_and_human_effort.png. Neither carries
an in-figure title (the captions do, 2026-09-04). The frozen originals are untouched.

Run from the repo root:
    ./venv/Scripts/python.exe pinning/effort/code/build_fullband_df_figures.py
"""

import csv
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
E = ROOT / "archive_v28" / "expected"
OUT = ROOT / "figures"


def rcsv(p):
    with open(p, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


df21 = {int(r["year"]): r for r in rcsv(E / "DF21_FINAL_longrun_labor_origin_financing_1950_2025.csv")}
dq = {int(r["year"]): r for r in rcsv(E / "LR_Q1_fullchain_factor_content_strong_weak_1950_2025.csv")}

yrs = np.arange(1950, 2026)
cen = np.array([100 * float(df21[y]["labor_origin_financing_central"]) for y in yrs])
lo = np.array([100 * float(df21[y]["lower"]) for y in yrs])
hi = np.array([100 * float(df21[y]["upper"]) for y in yrs])
strong = np.array([df21[y]["tier"].startswith("STRONG") for y in yrs])

# Band segments: weak years at a lighter tint than the strong window, so the
# strong/weak boundary stays visible in the band itself, not only in the line
# style. Segments overlap by one year so the band is drawn without gaps.
pre = yrs <= 2004
mid = (yrs >= 2004) & (yrs <= 2023)
post = yrs >= 2023

# --- Figure 1: D-F alone, full-band variant of FIG_DF_FINAL -----------------
fig, ax = plt.subplots(figsize=(12.2, 6.5))
ax.fill_between(yrs[pre], lo[pre], hi[pre], color="tab:blue", alpha=0.07,
                label="Weak-extension interval (aggregate method)")
ax.fill_between(yrs[post], lo[post], hi[post], color="tab:blue", alpha=0.07)
ax.fill_between(yrs[mid], lo[mid], hi[mid], color="tab:blue", alpha=0.16,
                label="Modern partial-identification interval")
ax.plot(yrs[pre], cen[pre], linestyle="--", linewidth=2, color="tab:blue",
        label="Weak long-run extension")
ax.plot(yrs[mid], cen[mid], linewidth=2.7, color="tab:orange",
        label="Annual BEA DPI-ranked source-profile central")
ax.plot(yrs[post], cen[post], linestyle="--", linewidth=2, color="tab:green")
ax.set_xlim(1950, 2025)
ax.set_ylim(40, 100)
ax.set_xlabel("Year")
ax.set_ylabel("Labor-origin financing share of PCE (%)")
ax.grid(True, alpha=0.25)
ax.legend(frameon=False)
fig.tight_layout()
fig.savefig(OUT / "FIG_DF_fullband_labor_origin_financing_1950_2025.png",
            dpi=250, bbox_inches="tight")
plt.close(fig)

# --- Figure 2: D-F/Q synthesis, full-band variant of FIG_DFQ_FINAL ----------
qc = np.array([100 * float(dq[y]["human_effort_share_headline"]) for y in yrs])
qlo = np.array([100 * float(dq[y]["human_effort_weak_lower"]) for y in yrs])
qhi = np.array([100 * float(dq[y]["human_effort_weak_upper"]) for y in yrs])
qpre = yrs <= 1997
qs = (yrs >= 1997) & (yrs <= 2023)
qpost = yrs >= 2023

fig, ax = plt.subplots(figsize=(12.2, 6.6))
ax.fill_between(yrs[pre], lo[pre], hi[pre], color="tab:blue", alpha=0.05,
                label="D-F weak-extension interval")
ax.fill_between(yrs[post], lo[post], hi[post], color="tab:blue", alpha=0.05)
ax.fill_between(yrs[mid], lo[mid], hi[mid], color="tab:blue", alpha=0.11,
                label="D-F partial-identification interval")
ax.fill_between(yrs, qlo, qhi, color="tab:orange", alpha=0.09,
                label="D-Q weak-extension band")
ax.plot(yrs[pre], cen[pre], linestyle="--", linewidth=2, color="tab:blue",
        label="D-F financing — weak extension")
ax.plot(yrs[mid], cen[mid], linewidth=2.5, color="tab:orange",
        label="D-F financing — annual source profiles")
ax.plot(yrs[post], cen[post], linestyle="--", linewidth=2, color="tab:green")
ax.plot(yrs[qpre], qc[qpre], linestyle="--", linewidth=2, color="tab:red",
        label="D-Q production labor — weak extension")
ax.plot(yrs[qs], qc[qs], linewidth=2.7, color="tab:purple",
        label="D-Q production labor — BEA full-chain benchmark")
ax.plot(yrs[qpost], qc[qpost], linestyle="--", linewidth=2, color="tab:brown")
ax.set_xlim(1950, 2025)
ax.set_ylim(35, 100)
ax.set_xlabel("Year")
ax.set_ylabel("Percent of PCE")
ax.grid(True, alpha=0.25)
ax.legend(frameon=False, fontsize=8.2, loc="upper right")
fig.tight_layout()
fig.savefig(ROOT.parent / "paper" / "figures" / "fig_consumption_financing_and_human_effort.png",
            dpi=250, bbox_inches="tight")
plt.close(fig)

print("wrote 2 full-band variant figures to", OUT)
