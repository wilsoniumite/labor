"""
build_fig3_realwage_fork.py — pinning/effort

Figure 3 (the real-wage fork), rebuilt from live FRED pulls. Replaces the
broken placeholder PNG shipped in archive_v28/expected/BASELINE_FIG3_*.png.

Construction is the house-established one (the long draft's deflator_fork.py (git history, tag pre-cleanup-2026-09-04);
the 2026-08-26 talk data briefing (same tag) §1): AHETPI monthly average
hourly earnings, deflated separately by CPI durables (CUSR0000SAD) and CPI
shelter (CUSR0000SAH1), annual means over complete years only, both legs
indexed 1964 = 100 (AHETPI's first full year).

Data rule (house): live public data only, no substitution. The pull step
vendors each series to data/raw/ with a provenance manifest; reruns rebuild
from the vendored snapshot with zero downloads. --refresh re-pulls live.

The series end at 2024: October 2025 CPI was never published (the cancelled
shutdown-era release leaves CUSR0000SAD and CUSR0000SAH1 permanently blank
for 2025-10), so 2025 can never satisfy the complete-year rule. Reported,
not patched.
Validation gates: level sanity anchors at 2023, plus the fork's documented
endpoints (talk_data_briefing.md, built 2026-08: 2024 durables leg 376.8,
shelter leg 78.6, 1983 seam-year ratio 1.46) within revision tolerance.
Any gate failure stops the build rather than approximating.

Run from the repo root:
    ./venv/Scripts/python.exe pinning/effort/code/build_fig3_realwage_fork.py [--refresh]
"""

import csv
import sys
import urllib.request
from datetime import date
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
OUT_CSV = ROOT / "data" / "fig3_realwage_fork.csv"
OUT_PNG = ROOT / "figures" / "FIG3_realwage_fork.png"

SERIES = {
    "wage": "AHETPI",        # avg hourly earnings, production & nonsupervisory, $/hr, monthly SA
    "durables": "CUSR0000SAD",  # CPI durables, monthly SA
    "shelter": "CUSR0000SAH1",  # CPI shelter, monthly SA
}
BASE_YEAR = 1964
# Level sanity anchors at 2023 annual means (from the long draft's deflator_fork.py (git history, tag pre-cleanup-2026-09-04)).
SANITY_2023 = {"wage": (26, 32), "durables": (105, 140), "shelter": (350, 420)}
# Fork anchors documented in the 2026-08-26 talk data briefing (same tag)
# (series built 2026-08-05); tolerances allow ordinary source revisions.
FORK_ANCHORS = [
    ("durables leg 2024", 2024, "durables", 376.8, 3.0),
    ("shelter leg 2024", 2024, "shelter", 78.6, 1.5),
]
SEAM_RATIO_1983 = (1.46, 0.05)


def pull(sid: str) -> Path:
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}"
    with urllib.request.urlopen(url, timeout=60) as r:
        txt = r.read().decode("utf-8")
    p = RAW / f"{sid}.csv"
    p.write_text(txt, encoding="utf-8")
    return p


def load_annual(sid: str) -> dict[int, float]:
    """Annual means over complete years only — a partial vintage year must
    not masquerade as an annual observation."""
    months: dict[int, list[float]] = {}
    with open(RAW / f"{sid}.csv", newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            val = row[sid]
            if val in ("", "."):
                continue
            months.setdefault(int(row["observation_date"][:4]), []).append(float(val))
    return {y: sum(v) / len(v) for y, v in months.items() if len(v) >= 12}


def main() -> int:
    refresh = "--refresh" in sys.argv
    RAW.mkdir(parents=True, exist_ok=True)
    manifest = []
    for concept, sid in SERIES.items():
        f = RAW / f"{sid}.csv"
        if refresh or not f.exists():
            pull(sid)
            manifest.append({"series": sid, "concept": concept,
                             "url": f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}",
                             "pulled": date.today().isoformat()})
    if manifest:
        mf = RAW / "fig3_pull_manifest.csv"
        rows = list(csv.DictReader(open(mf, encoding="utf-8"))) if mf.exists() else []
        rows.extend(manifest)
        with open(mf, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["series", "concept", "url", "pulled"])
            w.writeheader()
            w.writerows(rows)

    annual = {c: load_annual(sid) for c, sid in SERIES.items()}

    failures = []
    for concept, (lo, hi) in SANITY_2023.items():
        v = annual[concept].get(2023)
        if v is None or not (lo <= v <= hi):
            failures.append(f"sanity {concept} 2023={v} not in [{lo},{hi}]")

    years = sorted(set(annual["wage"]) & set(annual["durables"]) & set(annual["shelter"]))
    years = [y for y in years if y >= BASE_YEAR]
    legs = {}
    for d in ("durables", "shelter"):
        real = {y: annual["wage"][y] / annual[d][y] for y in years}
        legs[d] = {y: 100 * real[y] / real[BASE_YEAR] for y in years}

    for name, y, leg, target, tol in FORK_ANCHORS:
        v = legs[leg].get(y)
        if v is None or abs(v - target) > tol:
            failures.append(f"fork anchor {name}: {v} vs {target}±{tol}")
    seam = legs["durables"][1983] / legs["shelter"][1983]
    if abs(seam - SEAM_RATIO_1983[0]) > SEAM_RATIO_1983[1]:
        failures.append(f"1983 seam ratio {seam:.3f} vs {SEAM_RATIO_1983[0]}±{SEAM_RATIO_1983[1]}")

    print("=== validation ledger ===")
    print(f"years {years[0]}–{years[-1]} | 1983 seam ratio {seam:.2f} | "
          f"2024 legs {legs['durables'].get(2024, float('nan')):.1f} / "
          f"{legs['shelter'].get(2024, float('nan')):.1f} | "
          f"last-year fork ratio {legs['durables'][years[-1]] / legs['shelter'][years[-1]]:.2f}x")
    if failures:
        for msg in failures:
            print("FAIL", msg)
        print("BLOCKED: validation failed — stopping rather than approximating.")
        return 1
    print("all gates PASS")

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["year", "real_wage_durables_1964_100", "real_wage_shelter_1964_100"])
        for y in years:
            w.writerow([y, legs["durables"][y], legs["shelter"][y]])

    yrs = np.array(years)
    fig, ax = plt.subplots(figsize=(12.2, 6.5))
    ax.plot(yrs, [legs["durables"][y] for y in years], linewidth=2.5, color="tab:blue",
            label="wage deflated by durables CPI (machine-made goods)")
    ax.plot(yrs, [legs["shelter"][y] for y in years], linewidth=2.5, color="tab:red",
            label="wage deflated by shelter CPI (land-priced)")
    ax.axhline(100, color="k", linewidth=0.8, linestyle=":")
    ax.set_xlim(BASE_YEAR, yrs.max())
    ax.set_xlabel("Year")
    ax.set_ylabel(f"Real average hourly earnings, {BASE_YEAR} = 100")
    ax.set_title("The deflator fork: the same U.S. paycheck against machine-made goods and against land-priced shelter")
    ax.grid(True, alpha=0.25)
    ax.legend(frameon=False, loc="upper left")
    fig.tight_layout()
    fig.savefig(OUT_PNG, dpi=250, bbox_inches="tight")
    plt.close(fig)
    print("wrote", OUT_CSV.name, "and", OUT_PNG.name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
