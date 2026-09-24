# check_floor_margins.py — the floor-margin evidence (code/floor_margins.py): the data are what they say,
# and the findings, stated as found.
#
# Run from paths/:  ../venv/Scripts/python.exe checks/check_floor_margins.py
# Exit status 0 only if every check passes.

from __future__ import annotations

import json
import os
import sys

import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "code"))
import floor_margins as fm  # noqa: E402

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


df = fm.data()
R = json.load(open(os.path.join(ROOT, "results", "floor_margins.json"), encoding="utf-8"))

print("D — the data")
need = ["mortgage_float_new", "dep_hh_demand_stock", "dep_nfc_demand_stock", "nfc_float_new", "policy"]
w = df.loc["2015-01":"2026-07", need]
check("D1 every series is complete, monthly, 2015-01 to 2026-07", w.notna().all().all() and len(w) == 139, f"{len(w)} months")
neg = df.loc["2016-03":"2018-12"]
check("D2 the negative-rate window is what it says: policy at -0.50% throughout 2016-03..2018-12",
      np.allclose(neg.policy.values, -0.5, atol=0.02))

print("F — the findings (stated as found)")
fl = R["floor"]
check("F1 below zero, floating mortgage margins widened about one-for-one: contrast and regression agree, 0.7 to 1.3 per point",
      0.7 < fl["regression_2015_2021_per_point_below_zero"] < 1.3 and abs(fl["contrast_per_point_below_zero"] - fl["regression_2015_2021_per_point_below_zero"]) < 0.2,
      f"regression {fl['regression_2015_2021_per_point_below_zero']}, contrast {fl['contrast_per_point_below_zero']}, over STIBOR {fl['over_stibor_per_point_below_zero']}")
nm = (neg.mortgage_float_new.mean(), df.loc["2020-04":"2021-12"].mortgage_float_new.mean())
check("F2 so the new floating mortgage rate itself held its level whether policy was -0.5% or 0%", abs(nm[0] - nm[1]) < 0.15,
      f"{nm[0]:.2f}% at -0.5, {nm[1]:.2f}% at 0")
ep = R["episodes"]
check("F3 corporate floating margins did not widen: negative rates passed through to corporate loans",
      abs(ep["negative, 2016-18"]["nfc_float_new_over_policy"] - ep["zero, 2020-21"]["nfc_float_new_over_policy"]) < 0.15,
      f"{ep['negative, 2016-18']['nfc_float_new_over_policy']} against {ep['zero, 2020-21']['nfc_float_new_over_policy']}")
check("F4 deposit rates stopped at zero, not below: household and corporate on-demand rates never negative at -0.5%",
      fl["deposit_floor"]["hh_demand_min"] >= 0 and fl["deposit_floor"]["nfc_demand_min"] >= 0,
      f"minima {fl['deposit_floor']}")
asy = R["asymmetry"]
check("F5 household deposit rates rise more slowly than they fall (2022-23 against 2024-26)",
      asy["dep_hh_demand_stock"]["up_over_down"] < 0.85 and asy["dep_hh_all_stock"]["up_over_down"] < 0.85,
      f"up/down: on demand {asy['dep_hh_demand_stock']['up_over_down']}, all {asy['dep_hh_all_stock']['up_over_down']}")

n_ok = sum(ok for _, ok, _ in RESULTS)
print(f"\n{n_ok}/{len(RESULTS)} checks passed")
sys.exit(0 if n_ok == len(RESULTS) else 1)
