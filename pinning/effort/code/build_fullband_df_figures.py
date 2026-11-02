"""
build_fullband_df_figures.py — pinning/effort (Figure 7 of the paper)

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
figures/; the D-F/Q synthesis is the paper's Figure 7 and is written to
paper/figures/fig_consumption_financing_and_human_effort.png, with a vector copy
(.pdf) next to it. Neither carries an in-figure title (the captions do,
2026-09-04). The frozen originals are untouched. The paper figure's legend uses
plain names (her call, 2026-11-02, after the SSRN figure's legend) in place of
the archive's D-F/D-Q labels; each extension entry also shows the 2024-2025
tail drawn in its own color.

Run from the repo root:
    ./venv/Scripts/python.exe pinning/effort/code/build_fullband_df_figures.py
"""

import csv
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerTuple

# matplotlib's stock default face, pinned so every machine draws the same figure
# (some installations default to another face); TrueType embedding in the PDF
plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["pdf.fonttype"] = 42

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

# Extension years by the tier columns: D-F weak 1950-2003 and 2024-2025 (DF21
# "tier"), D-Q weak 1950-1996 and 2024-2025 (LR_Q1 "evidence_tier"); the labels
# below state them, so they are checked here.
fin_ext = [int(y) for y in yrs[~strong]]
q_ext = [int(y) for y in yrs if dq[y]["evidence_tier"] == "WEAK"]
assert fin_ext == list(range(1950, 2004)) + [2024, 2025], "D-F extension years moved"
assert q_ext == list(range(1950, 1997)) + [2024, 2025], "D-Q extension years moved"
assert list(yrs[strong]) == list(range(2004, 2024)), "D-F data window moved"

FIN = "Consumption financed from labor-origin resources"
PROD = "Human effort in consumed production"
# 2026-11-02, typography pass (the paper figure only; the D-F figure above is
# untouched): drawn at the width it prints, 0.92\textwidth in main.tex (16 cm text
# width), so sizes here are printed sizes: ticks 8 pt, axis labels 8.5 pt, legend
# 7.5 pt. Line widths and tick sizes are the earlier values (a 12.1 in canvas)
# times 0.479, the scale they printed at, so the plot keeps its weight on the page.
# At a legible size the legend no longer fits inside the axes (its longest entry
# is wider than the plot), and two columns do not fit the page width, so it sits
# below the axes in one column; the figure is taller by the legend (4.24 in, was
# 3.11 in as printed), the plot keeping its shape (width/height 1.93). Wording and
# order of the entries are unchanged.
PRINT_W = 0.92 * 16 / 2.54             # inches
PRINT_RC = {"font.size": 8.5, "xtick.labelsize": 8, "ytick.labelsize": 8,
            "axes.linewidth": 0.38, "grid.linewidth": 0.38,
            "xtick.major.width": 0.38, "ytick.major.width": 0.38,
            "xtick.major.size": 1.7, "ytick.major.size": 1.7}
with plt.rc_context(PRINT_RC):
    fig, ax = plt.subplots(figsize=(PRINT_W, 4.24), layout="constrained")
    fin_band_ext = ax.fill_between(yrs[pre], lo[pre], hi[pre], color="tab:blue", alpha=0.05)
    ax.fill_between(yrs[post], lo[post], hi[post], color="tab:blue", alpha=0.05)
    fin_band_id = ax.fill_between(yrs[mid], lo[mid], hi[mid], color="tab:blue", alpha=0.11)
    prod_band = ax.fill_between(yrs, qlo, qhi, color="tab:orange", alpha=0.09)
    fin_ext_pre, = ax.plot(yrs[pre], cen[pre], linestyle="--", linewidth=0.96, color="tab:blue")
    fin_data, = ax.plot(yrs[mid], cen[mid], linewidth=1.2, color="tab:orange")
    fin_ext_post, = ax.plot(yrs[post], cen[post], linestyle="--", linewidth=0.96,
                            color="tab:green")
    prod_ext_pre, = ax.plot(yrs[qpre], qc[qpre], linestyle="--", linewidth=0.96,
                            color="tab:red")
    prod_bench, = ax.plot(yrs[qs], qc[qs], linewidth=1.29, color="tab:purple")
    prod_ext_post, = ax.plot(yrs[qpost], qc[qpost], linestyle="--", linewidth=0.96,
                             color="tab:brown")
    ax.set_xlim(1950, 2025)
    ax.set_ylim(35, 100)
    ax.set_xlabel("Year")
    ax.set_ylabel("Percent of PCE")
    ax.grid(True, alpha=0.25)
    fig.legend(
        [fin_band_ext, fin_band_id, prod_band,
         (fin_ext_pre, fin_ext_post), fin_data, (prod_ext_pre, prod_ext_post), prod_bench],
        ["Financing: long-run extension interval (1950–2003, 2024–2025)",
         "Financing: identification interval (2004–2023)",
         "Production: long-run extension interval (all years)",
         FIN + ": long-run extension (1950–2003, 2024–2025)",
         FIN + ": annual income-source data (2004–2023)",
         PROD + ": long-run extension (1950–1996, 2024–2025)",
         PROD + ": BEA full-chain benchmark (1997–2023)"],
        handler_map={tuple: HandlerTuple(ndivide=None, pad=0.3)}, handlelength=3.2,
        frameon=False, fontsize=7.5, loc="outside lower center", ncol=1,
        labelspacing=0.3, borderpad=0.2)
    PAPER_FIG = ROOT.parent / "paper" / "figures" / "fig_consumption_financing_and_human_effort.png"
    fig.savefig(PAPER_FIG, dpi=300)
    fig.savefig(PAPER_FIG.with_suffix(".pdf"), metadata={"CreationDate": None})
    plt.close(fig)

print("wrote the D-F full-band figure to", OUT, "and the paper figure to", PAPER_FIG.parent,
      f"({PAPER_FIG.name}, {PAPER_FIG.with_suffix('.pdf').name})")
