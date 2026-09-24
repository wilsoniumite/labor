# check_households.py — the household layer (code/households.py): the bookkeeping is what it says, and the findings,
# stated as found.
#
# Run from paths/:  ../venv/Scripts/python.exe checks/check_households.py
# Exit status 0 only if every check passes.

from __future__ import annotations

import json
import os
import sys
from dataclasses import replace

import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "code"))
import bank_scenarios as bs  # noqa: E402
import demand as dm  # noqa: E402
import households as hh  # noqa: E402

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


R = json.load(open(os.path.join(ROOT, "results", "households.json"), encoding="utf-8"))
s0 = R["sweden_start"]
cyc = json.load(open(os.path.join(ROOT, "results", "demand.json"), encoding="utf-8"))["sweden_cycle"]
dmp = dm.Demand(kappa=cyc["kappa_per_pp_output_gap"], okun=cyc["okun"])
W = {name: dm.world(br, truth) for name, (br, truth) in bs.SCEN.items()}
C = hh.Support()
S = R["scenarios"]

print("D — the Swedish start (Statistics Sweden)")
check("D1 household debt 1.6-1.9 x disposable income, floating share 0.7-0.85, mortgage margin 0.8-1.4 points",
      1.6 < s0["debt"] / s0["disposable"] < 1.9 and 0.7 < s0["floating_share"] < 0.85 and 0.8 < s0["mortgage_margin"] < 1.4,
      f"{s0['debt'] / s0['disposable']:.2f}, {s0['floating_share']:.3f}, {s0['mortgage_margin']:.2f}")

print("B — the bookkeeping")
r = hh.run(W["status quo"], dmp, C, s0)
check("B1 the status quo stays put: no extra demand, no gap, debt service a constant share of income",
      np.abs(r["households"]["level"]).max() < 1e-9 and np.abs(r["gap"]).max() < 1e-9 and np.ptp(r["dsr"][1:]) < 1e-9,
      f"debt service {r['dsr'][5]:.2f}% of income")
r = hh.run(W["deficits dominate"], dmp, C, s0)
h = r["households"]
dstep = h["debt"][1:] / h["debt"][:-1]
check("B2 money debts never fall faster than amortisation", dstep.min() >= 1 - C.amort / 100 * 0.25 - 1e-12, f"smallest quarterly ratio {dstep.min():.5f}")
tot = h["d_out"] + h["d_sup"] + h["d_debt"] + h["d_check"]
check("B3 the demand level is the sum of its channels", np.allclose(tot, h["level"]))
rr = hh.run(W["owners' saving dominates"], dmp, replace(C, rigid_wages=True), s0)
check("B4 rigid money wages never fall", np.all(np.diff(rr["households"]["W"]) >= -1e-12))

print("F — the findings (stated as found)")
dd, os_ = S["deficits dominate | central"]["y5_y8_y10_y12_y15"], S["owners' saving dominates | central"]["y5_y8_y10_y12_y15"]
check("F1 floating-rate mortgages move with the branch: debt service rises when deficits dominate, falls when owners' saving does",
      dd["debt_service_pct_income"][3] > dd["debt_service_pct_income"][0] + 1 and os_["debt_service_pct_income"][4] < os_["debt_service_pct_income"][0] - 2,
      f"deficits {dd['debt_service_pct_income']}; owners' saving {os_['debt_service_pct_income']}")
g_full = S["owners' saving dominates | demand layer alone (full pooling)"]["gap_min_and_year"][0]
g_hh = S["owners' saving dominates | central"]["gap_min_max"][0]
check("F2 so in the falling-rate branch Swedish households cushion the downturn (a smaller gap than full pooling)", g_hh > g_full,
      f"{g_hh} against {g_full}")
r0 = hh.run(W["deficits dominate"], dmp, replace(C, replacement_first=0.0, replacement_later=0.0), s0)
check("F3 state support is what keeps the surge in dependence from cutting demand: without it the job-loser drag at year 12 is several times larger",
      np.interp(12, r0["t"], r0["households"]["d_out"]) < 3 * np.interp(12, r["t"], h["d_out"]),
      f"{np.interp(12, r0['t'], r0['households']['d_out']):.2f} against {np.interp(12, r['t'], h['d_out']):.2f} % of GDP")
rig = S["owners' saving dominates | rigid money wages"]
check("F4 rigid money wages turn the adjustment into job loss: more people out of work and a deeper gap, longer at the floor",
      rig["y5_y8_y10_y12_y15"]["out_of_work_pp"][2] > os_["out_of_work_pp"][2] + 5 and rig["gap_min_max"][0] < g_hh - 1 and rig["years_at_floor"] > S["owners' saving dominates | central"]["years_at_floor"],
      f"out of work at year 10 {rig['y5_y8_y10_y12_y15']['out_of_work_pp'][2]}% against {os_['out_of_work_pp'][2]}%; gap {rig['gap_min_max'][0]} against {g_hh}")
ck = hh.run(W["deficits dominate"], dmp, replace(C, check_size=4.0), s0)
on = ck["households"]["check"] > 0
check("F5 emergency checks lift output only while they are paid", on.any() and (ck["gap"][on] - r["gap"][on]).min() > 0.1
      and abs(np.interp(14, ck["t"], ck["gap"]) - np.interp(14, r["t"], r["gap"])) < 0.05,
      f"while paid +{(ck['gap'][on] - r['gap'][on]).mean():.2f} points; at year 14 {np.interp(14, ck['t'], ck['gap']) - np.interp(14, r['t'], r['gap']):+.3f}")
np_ = S["deficits dominate | no private support"]["y5_y8_y10_y12_y15"]["demand_level"][2]
check("F6 under today's Swedish state support, family and friends change little (the demand level within 0.05% of GDP without them)",
      abs(np_ - dd["demand_level"][2]) < 0.05, f"{np_} against {dd['demand_level'][2]}")

print("G — family-based support against today's Swedish state support")
for name in ("deficits dominate", "owners' saving dominates"):
    st, fa = S[f"{name} | central"], S[f"{name} | family-based support"]
    ys, yf = st["y5_y8_y10_y12_y15"], fa["y5_y8_y10_y12_y15"]
    check(f"G1 {name}: leaning on families costs demand — a larger drag from constrained households at year 12 and a lower gap trough, for a smaller state bill",
          yf["demand_level"][3] < ys["demand_level"][3] - 0.2 and fa["gap_min_max"][0] <= st["gap_min_max"][0] and yf["support_cost_pct_gdp"][3] < ys["support_cost_pct_gdp"][3],
          f"drag {yf['demand_level'][3]} against {ys['demand_level'][3]}; state cost {yf['support_cost_pct_gdp'][3]} against {ys['support_cost_pct_gdp'][3]} % of GDP")
    check(f"G2 {name}: networks run out — the cap on what family and friends give binds in the deep phase, and less of the lost wage is covered by year 15",
          fa["years_network_cap_binds"] > 0 and yf["lost_wage_covered_pct"][4] < 80 and yf["supporters_burden_pct"][4] >= 9.99,
          f"cap binds {fa['years_network_cap_binds']} years; covered {yf['lost_wage_covered_pct']}")
    nc = S[f"{name} | family-based, no cap on what networks give"]["y5_y8_y10_y12_y15"]
    check(f"G3 {name}: the cap moves who bears the loss more than it moves demand (the drag within 0.05% of GDP without it)",
          abs(nc["demand_level"][4] - yf["demand_level"][4]) < 0.05 and nc["lost_wage_covered_pct"][4] > yf["lost_wage_covered_pct"][4],
          f"drag {nc['demand_level'][4]} against {yf['demand_level'][4]}; covered {nc['lost_wage_covered_pct'][4]} against {yf['lost_wage_covered_pct'][4]}")
tail = S["owners' saving dominates | family-based, rigid money wages"]
check("G4 the tail is family-based support with rigid money wages: the deepest downturn of every run, 2009-sized, and the longest at the floor",
      tail["gap_min_max"][0] == min(v["gap_min_max"][0] for k, v in S.items() if "gap_min_max" in v) and tail["gap_min_max"][0] < -4.0
      and tail["years_at_floor"] == max(v["years_at_floor"] for k, v in S.items() if "years_at_floor" in v),
      f"gap {tail['gap_min_max'][0]}, {tail['years_at_floor']} years at the floor")

n_ok = sum(ok for _, ok, _ in RESULTS)
print(f"\n{n_ok}/{len(RESULTS)} checks passed")
sys.exit(0 if n_ok == len(RESULTS) else 1)
