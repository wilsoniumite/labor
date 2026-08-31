"""
crosscheck_s1_fred.py — effort-accounting thread

Closes the v28 audit caveat that the S1 owner-housing input snapshot was
"recovered from the prior D2 output rather than freshly downloaded": pulls
the two Z.1 series live from FRED and compares them, year by year, against
archive_v28/inputs/scarcity/owner_housing_stock_source_snapshot_1945_2025.csv.

Report-only by design: the archived snapshot stays the canonical
reproduction input (the frozen figures were built from it); this script
documents how far the current vintage has drifted. Ordinary Z.1 revisions
concentrate in recent years. Raw pulls are vendored to data/raw/ with the
Fig-3 manifest.

Run from the repo root:
    ./venv/Scripts/python.exe effort-accounting/code/crosscheck_s1_fred.py [--refresh]
"""

import csv
import sys
import urllib.request
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
SNAP = ROOT / "archive_v28" / "inputs" / "scarcity" / "owner_housing_stock_source_snapshot_1945_2025.csv"
OUT = ROOT / "data" / "s1_fred_crosscheck.csv"

SERIES = {
    "owner_occupied_real_estate_market_value_b": "BOGZ1FL155035013A",
    "owner_occupied_residential_structures_current_cost_b": "BOGZ1LM155012665A",
}
MILLIONS_TO_BILLIONS = 1e-3  # Z.1 annual series post in millions of dollars


def pull(sid: str) -> None:
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}"
    with urllib.request.urlopen(url, timeout=60) as r:
        (RAW / f"{sid}.csv").write_text(r.read().decode("utf-8"), encoding="utf-8")


def load_fred(sid: str) -> dict[int, float]:
    out = {}
    with open(RAW / f"{sid}.csv", newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            if row[sid] not in ("", "."):
                out[int(row["observation_date"][:4])] = float(row[sid]) * MILLIONS_TO_BILLIONS
    return out


def main() -> int:
    refresh = "--refresh" in sys.argv
    RAW.mkdir(parents=True, exist_ok=True)
    manifest_rows = []
    for sid in SERIES.values():
        if refresh or not (RAW / f"{sid}.csv").exists():
            pull(sid)
            manifest_rows.append({"series": sid, "concept": "S1 cross-check",
                                  "url": f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}",
                                  "pulled": date.today().isoformat()})
    if manifest_rows:
        mf = RAW / "fig3_pull_manifest.csv"
        rows = list(csv.DictReader(open(mf, encoding="utf-8"))) if mf.exists() else []
        rows.extend(manifest_rows)
        with open(mf, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["series", "concept", "url", "pulled"])
            w.writeheader()
            w.writerows(rows)

    snap = {int(r["year"]): r for r in csv.DictReader(open(SNAP, encoding="utf-8-sig"))}
    live = {col: load_fred(sid) for col, sid in SERIES.items()}

    rows, worst = [], (0.0, None, None)
    for y in sorted(snap):
        for col in SERIES:
            a = float(snap[y][col])
            b = live[col].get(y)
            if b is None:
                continue
            rel = abs(b - a) / max(abs(a), 1e-9)
            rows.append({"year": y, "concept": col, "snapshot_b": a, "live_b": b,
                         "rel_diff_pct": 100 * rel})
            if rel > worst[0]:
                worst = (rel, y, col)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["year", "concept", "snapshot_b", "live_b", "rel_diff_pct"])
        w.writeheader()
        w.writerows(rows)

    exact = sum(1 for r in rows if r["rel_diff_pct"] == 0.0)
    under_01 = sum(1 for r in rows if r["rel_diff_pct"] < 0.1)
    print(f"=== S1 cross-check: {len(rows)} year-series cells ===")
    print(f"identical: {exact} | within 0.1%: {under_01} | "
          f"worst: {100 * worst[0]:.3f}% ({worst[1]}, {worst[2] and worst[2].split('_')[2]})")
    recent = [r for r in rows if r["year"] >= 2020]
    if recent:
        print("2020+ max rel diff: "
              f"{max(r['rel_diff_pct'] for r in recent):.3f}%")
    print("wrote", OUT.name, "— archived snapshot remains the canonical repro input")
    return 0


if __name__ == "__main__":
    sys.exit(main())
