"""
vendor_legacy_inputs.py — pinning/effort

Extracts the legacy-archive files that the DF9/DF10 consolidated rebuild
(build_df9_df10_longrun.py) needs, from the zips shipped inside
archive_v28/legacy_archives/, into data/legacy_inputs/ with a provenance
manifest. Also derives three slim tables from archive_v28 inputs for the
pieces whose generating pass predates the export (the 1950s weak backcasts
and the transfer-exposure scenario bounds) — extracted, never edited.

Rerunnable: output is a pure function of the shipped archive.

Run from the repo root:
    ./venv/Scripts/python.exe pinning/effort/code/vendor_legacy_inputs.py
"""

import csv
import io
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEGZ = ROOT / "archive_v28" / "legacy_archives"
V28DF = ROOT / "archive_v28" / "inputs" / "df"
OUT = ROOT / "data" / "legacy_inputs"

V19_ZIP = "effort_accounting_DF_full_pce_2026-08-27_v19.zip"
V2_ZIP = "effort_accounting_v2_bundle(1).zip"

# (zip, member path inside zip, output name)
PULLS = [
    (V19_ZIP, "DF_full_pce/DF8_minimum_intertemporal_strong_weak_1950_2025.csv",
     "DF8_minimum_intertemporal_strong_weak_1950_2025.csv"),
    (V19_ZIP, "DF_full_pce/DF8_timing_floor_model_validation.csv",
     "DF8_timing_floor_model_validation.csv"),
    (V19_ZIP, "prior/ea_DF_strong_weak_pass/DF_3_program_funding_lookthrough_detail_1960_2025.csv",
     "DF_3_program_funding_lookthrough_detail_1960_2025.csv"),
    (V19_ZIP, "prior/ea_DF_strong_weak_pass/DF_1_recursive_funding_assumptions.csv",
     "DF_1_recursive_funding_assumptions.csv"),
    (V2_ZIP, "proprietor_effort_proxy_v1.csv", "proprietor_effort_proxy_v1.csv"),
]


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = []
    for zname, member, outname in PULLS:
        with zipfile.ZipFile(LEGZ / zname) as z:
            data = z.read(member)
        (OUT / outname).write_bytes(data)
        manifest.append({"file": outname, "source": f"archive_v28/legacy_archives/{zname}",
                         "member": member,
                         "role": "archived intermediate consumed by build_df9_df10_longrun.py"})

    # Slim extracts from the v28 inputs themselves: archived weak backcasts
    # whose generating pass predates the export. Extracted verbatim by column.
    df9 = list(csv.DictReader(open(V28DF / "DF9_current_resource_origin_strong_weak_1950_2025.csv",
                                   encoding="utf-8-sig")))
    df10 = list(csv.DictReader(open(V28DF / "DF10_full_pce_financing_ledger_strong_weak_1950_2025.csv",
                                    encoding="utf-8-sig")))

    comp_cols = ["employee_comp", "proprietors", "rental", "interest", "dividends", "transfers"]
    with open(OUT / "DF9_1950s_composition_backcast.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["year"] + [c + "_share_resources" for c in comp_cols])
        for r in df9:
            if 1950 <= int(r["year"]) <= 1959:
                w.writerow([r["year"]] + [r[c + "_share_resources"] for c in comp_cols])
    manifest.append({"file": "DF9_1950s_composition_backcast.csv",
                     "source": "archive_v28/inputs/df/DF9_current_resource_origin_strong_weak_1950_2025.csv",
                     "member": "rows 1950-1959, composition-share columns",
                     "role": "archived WEAK_COMPOSITION_BACKCAST (generating pass not in the export; "
                             "see DF10_QA row: '1950-1959 claimed observed: NO')"})

    with open(OUT / "DF10_1950s_pce_dpi_backcast.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["year", "pce_b", "dpi_b"])
        for r in df10:
            if 1950 <= int(r["year"]) <= 1959:
                w.writerow([r["year"], r["pce_b"], r["dpi_b"]])
    manifest.append({"file": "DF10_1950s_pce_dpi_backcast.csv",
                     "source": "archive_v28/inputs/df/DF10_full_pce_financing_ledger_strong_weak_1950_2025.csv",
                     "member": "rows 1950-1959, pce_b/dpi_b",
                     "role": "PCE is NIPA-observed; the DPI column is the archived WEAK_BACKCAST "
                             "(DPI/resources-consistent construction, generating pass not in the export)"})

    with open(OUT / "transfer_wage_exposure_bounds_1960_2025.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["year", "transfer_wage_exposure_low", "transfer_wage_exposure_high"])
        for r in df9:
            if int(r["year"]) >= 1960:
                w.writerow([r["year"], r["transfer_wage_exposure_low"], r["transfer_wage_exposure_high"]])
    manifest.append({"file": "transfer_wage_exposure_bounds_1960_2025.csv",
                     "source": "archive_v28/inputs/df/DF9_current_resource_origin_strong_weak_1950_2025.csv",
                     "member": "transfer_wage_exposure_low/high, 1960-2025",
                     "role": "archived scenario bounds (DF_1 low/high scenarios applied to program funding "
                             "histories; per-program scenario recomputation is the remaining frontier — "
                             "the MID path is generated from DF_3, these bounds are not)"})

    with open(OUT / "PROVENANCE_legacy_inputs.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["file", "source", "member", "role"])
        w.writeheader()
        w.writerows(manifest)
    print(f"vendored {len(manifest)} files to {OUT}")


if __name__ == "__main__":
    main()
