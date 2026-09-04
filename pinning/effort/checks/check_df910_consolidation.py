"""
check_df910_consolidation.py — pinning/effort

Gates the consolidated DF9/DF10 rebuild (code/build_df9_df10_longrun.py)
against the archived v28 ledgers:

1. DF9: every numeric column reproduces the archived file to <= 1e-12 for
   all 76 years (composition shares, proprietor and transfer parameters,
   and all origin-share tiers). The proprietor parameters and the transfer
   MID path are generated, not copied - this is the consolidation claim.
2. DF10: centrals, timing slice, PCE/DPI, and the capacity LOWER bound
   reproduce exactly for all years; the capacity UPPER bound reproduces
   exactly for every year OUTSIDE 1958-1979.
3. The 1958-1979 upper values differ only inside the documented window,
   only upward (rebuilt wider/more conservative), and by <= 3.3pp - the
   KNOWN DISCREPANCY surfaced in the 2026-08-31 consolidation session
   (see the build script's header). GREEN does not bless those 22 archived
   values; adopting the rebuilt ones in DF21/figures is Stella's call.
4. DF21 cross-check: for weak years the expected DF21 central/lower match
   the rebuilt DF10 exactly; DF21 upper matches outside the window.

Run from the repo root:
    ./venv/Scripts/python.exe pinning/effort/checks/check_df910_consolidation.py
"""

import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
V28DF = ROOT / "archive_v28" / "inputs" / "df"
V28EXP = ROOT / "archive_v28" / "expected"
REB = ROOT / "data" / "rebuilt"

WINDOW = set(range(1958, 1980))
TOL = 1e-12
GREEN, RED = 0, 0


def report(ok, msg):
    global GREEN, RED
    print(("PASS" if ok else "FAIL"), msg)
    GREEN += ok
    RED += not ok


def load(p, key="year"):
    return {int(r[key]): r for r in csv.DictReader(open(p, encoding="utf-8-sig"))}


def maxdiff(a, b, cols, years):
    return max(abs(float(a[y][c]) - float(b[y][c])) for y in years for c in cols)


def main() -> int:
    for script in ("vendor_legacy_inputs.py", "build_df9_df10_longrun.py"):
        r = subprocess.run([sys.executable, str(ROOT / "code" / script)],
                           capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stdout, r.stderr)
            print(f"RED — {script} failed")
            return 1

    years = list(range(1950, 2026))
    reb9 = load(REB / "DF9_rebuilt_1950_2025.csv")
    arc9 = load(V28DF / "DF9_current_resource_origin_strong_weak_1950_2025.csv")
    reb10 = load(REB / "DF10_rebuilt_1950_2025.csv")
    arc10 = load(V28DF / "DF10_full_pce_financing_ledger_strong_weak_1950_2025.csv")
    df21 = load(V28EXP / "DF21_FINAL_longrun_labor_origin_financing_1950_2025.csv")

    cols9 = ([c + "_share_resources" for c in
              ["employee_comp", "proprietors", "rental", "interest", "dividends", "transfers"]]
             + [f"{p}_{t}" for p in ("proprietor_effort_share", "transfer_wage_exposure",
                                     "labor_origin_current_resource_share")
                for t in ("low", "mid", "high")]
             + ["ownership_origin_current_resource_share_mid",
                "fiscal_nonlabor_or_unresolved_current_resource_share_mid"])
    report(maxdiff(reb9, arc9, cols9, years) <= TOL,
           f"DF9 all {len(cols9)} numeric columns reproduce archived (76 years)")

    cols10 = ["pce_b", "dpi_b", "minimum_intertemporal_share_pce",
              "current_labor_origin_share_pce_central",
              "current_ownership_property_origin_share_pce_central",
              "current_fiscal_nonlabor_unresolved_share_pce_central",
              "labor_financing_capacity_lower_share_pce"]
    report(maxdiff(reb10, arc10, cols10, years) <= TOL,
           "DF10 centrals, timing, PCE/DPI, capacity LOWER reproduce archived (76 years)")

    out_win = [y for y in years if y not in WINDOW]
    report(maxdiff(reb10, arc10, ["labor_financing_capacity_upper_share_pce"], out_win) <= TOL,
           "DF10 capacity UPPER reproduces archived outside 1958-1979 (54 years)")

    diffs = {y: (float(reb10[y]["labor_financing_capacity_upper_share_pce"])
                 - float(arc10[y]["labor_financing_capacity_upper_share_pce"]))
             for y in WINDOW}
    report(all(0 < d <= 0.033 for d in diffs.values()),
           f"1958-1979 upper discrepancy confined, upward, <= 3.3pp "
           f"(max {max(diffs.values()) * 100:.2f}pp in {max(diffs, key=diffs.get)})")

    weak = [y for y in years if df21[y]["tier"] == "WEAK_LONGRUN_EXTENSION"]
    e_cl = max(abs(float(df21[y]["labor_origin_financing_central"])
                   - float(reb10[y]["current_labor_origin_share_pce_central"])) for y in weak)
    e_lo = max(abs(float(df21[y]["lower"])
                   - float(reb10[y]["labor_financing_capacity_lower_share_pce"])) for y in weak)
    e_hi = max(abs(float(df21[y]["upper"])
                   - float(reb10[y]["labor_financing_capacity_upper_share_pce"]))
               for y in weak if y not in WINDOW)
    report(max(e_cl, e_lo, e_hi) <= TOL,
           "DF21 weak years match rebuilt DF10 (central/lower all, upper outside window)")

    if RED:
        print(f"RED — {RED} of {GREEN + RED} checks failed")
        return 1
    print(f"GREEN — consolidation verified ({GREEN} checks; "
          "22 archived 1958-1979 uppers remain the documented discrepancy, her call)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
