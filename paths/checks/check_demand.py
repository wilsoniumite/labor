# check_demand.py — the demand layer (code/demand.py): the mechanics are what they say, and the findings, stated
# as found.
#
# Run from paths/:  ../venv/Scripts/python.exe checks/check_demand.py
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

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


R = json.load(open(os.path.join(ROOT, "results", "demand.json"), encoding="utf-8"))
cyc = R["sweden_cycle"]
base = dm.Demand(kappa=cyc["kappa_per_pp_output_gap"], okun=cyc["okun"])
W = {name: dm.world(br, truth) for name, (br, truth) in bs.SCEN.items()}
S = R["scenarios"]
C = "central (r* learned with a 3-year half-life)"

print("M — the mechanics")
r = dm.run(W["status quo"], base)
check("M1 the status quo is a steady state: no gap, inflation on target, policy at neutral throughout",
      np.abs(r["gap"]).max() < 1e-12 and np.abs(r["inflation"] - 2.0).max() < 1e-12 and np.ptp(r["policy"]) < 1e-12)
r = dm.run(W["owners' saving dominates"], replace(base, h=1e-6, smooth=0.0, elb=-99.0))
check("M2 a central bank that knows r* at once, without smoothing or a floor, keeps the gap near zero as r* falls",
      np.abs(r["gap"]).max() < 0.3, f"largest gap {np.abs(r['gap']).max():.3f}%")
for name in ("deficits dominate", "owners' saving dominates"):
    g = [abs(S[f"{name} | {v}"]["gap_min_and_year" if "owners" in name else "gap_max_and_year"][0]) for v in
         ("fast learning (1 year)", C, "slow learning (8 years, pre-2021 anchors)")]
    check(f"M3 {name}: the slower the central bank learns r*, the larger the gap (1, 3, 8 years)", g[0] < g[1] < g[2], str(g))
r = dm.run(W["owners' saving dominates"], base)
r0 = dm.run(W["owners' saving dominates"], replace(base, elb=-99.0))
check("M4 the floor holds, and where it binds the gap is no smaller than without it",
      r["policy"].min() >= base.elb - 1e-12 and r0["policy"].min() < base.elb and np.all(r["gap"] <= r0["gap"] + 1e-9),
      f"policy min {r['policy'].min():.2f} (without the floor {r0['policy'].min():.2f})")
mp = W["owners' saving dominates"]
check("M5 the equilibrium's relative prices ride through unchanged (goods less housing inflation is the macro block's)",
      np.allclose(r["pi_goods"] - r["pi_shelter"], mp["pi_goods"] - mp["pi_shelter"]))

print("C — the calibration (Swedish data)")
check("C1 Okun: unemployment rises when growth falls, more than 3 standard errors from zero",
      cyc["okun_du_per_pp_growth"]["coef"] < 0 and abs(cyc["okun_du_per_pp_growth"]["coef"]) > 3 * cyc["okun_du_per_pp_growth"]["se"],
      str(cyc["okun_du_per_pp_growth"]))
check("C2 Phillips: core inflation falls when unemployment is above trend; kappa between 0.02 and 0.5",
      cyc["phillips_per_pp_unemployment_gap"]["coef"] < 0 and 0.02 < cyc["kappa_per_pp_output_gap"] < 0.5,
      f"{cyc['phillips_per_pp_unemployment_gap']}, kappa {cyc['kappa_per_pp_output_gap']}")

print("F — the findings (stated as found)")
os_c, dd_c = S[f"owners' saving dominates | {C}"], S[f"deficits dominate | {C}"]
check("F1 owners' saving dominates: policy too tight on the way down — a negative gap and inflation below target",
      os_c["gap_min_and_year"][0] < -0.5 and os_c["inflation_min_max"][0] < 2.0, f"gap {os_c['gap_min_and_year']}, inflation {os_c['inflation_min_max']}")
check("F2 deficits dominate: policy too loose on the way up — a positive gap and inflation above target",
      dd_c["gap_max_and_year"][0] > 0.3 and dd_c["inflation_min_max"][1] > 2.0, f"gap {dd_c['gap_max_and_year']}, inflation {dd_c['inflation_min_max']}")
cyc_max = max(abs(v["gap_min_and_year"][0]) for k, v in S.items() if "2009-size" not in k)
check("F3 on the paper's paths, even fast automation with slow learning keeps the cycle normal-sized: gaps within 3%, headline inflation 1.5-2.5%",
      cyc_max < 3.0 and all(1.5 <= v["inflation_min_max"][0] and v["inflation_min_max"][1] <= 2.5 for k, v in S.items() if "2009-size" not in k),
      f"largest gap {cyc_max:.2f}%")
part10 = float(np.interp(10, mp["t"], mp["participation"] / mp["participation"][0]))
check("F4 the structural exit dwarfs the cycle: participation 10%+ lower by year 10, the cyclical unemployment rise under 1 point",
      part10 < 0.9 and os_c["unemployment_up_max"] < 1.0, f"participation {part10:.2f} of the start; cyclical +{os_c['unemployment_up_max']} pp")
k_now = "status quo + a 2009-size demand shock, today's room (2.25 points) | the Riksbank's 2008 strength, weak anchor"
k_then = "status quo + a 2009-size demand shock, 2008's room (5.25 points) | the Riksbank's 2008 strength, weak anchor"
check("F5 a 2009-size shock takes today's Riksbank to the floor (not 2008's), and the gap three years on is deeper",
      S[k_now]["years_at_floor"] > 0 and S[k_then]["years_at_floor"] == 0 and S[k_now]["y3_y5_y8_y10_y12_y15"]["gap"][0] < S[k_then]["y3_y5_y8_y10_y12_y15"]["gap"][0],
      f"floor {S[k_now]['years_at_floor']} years; gap at year 3 {S[k_now]['y3_y5_y8_y10_y12_y15']['gap'][0]} against {S[k_then]['y3_y5_y8_y10_y12_y15']['gap'][0]}")

n_ok = sum(ok for _, ok, _ in RESULTS)
print(f"\n{n_ok}/{len(RESULTS)} checks passed")
sys.exit(0 if n_ok == len(RESULTS) else 1)
