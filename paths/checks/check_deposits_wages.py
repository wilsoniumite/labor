# check_deposits_wages.py — Swedish household deposits against wages, income, saving and rates
# (code/deposits_wages.py): the data are what they say, and the findings, stated as found.
#
# Run from paths/:  ../venv/Scripts/python.exe checks/check_deposits_wages.py
# Exit status 0 only if every check passes.

from __future__ import annotations

import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "code"))
import deposits_wages as dw  # noqa: E402

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


d = dw.data()
R = json.load(open(os.path.join(ROOT, "results", "deposits_wages.json"), encoding="utf-8"))

print("D — the data")
w = d.loc["1996Q4":"2026Q2", ["deposits", "wages", "disposable", "consumption", "policy", "dep_demand"]]
check("D1 every series is complete, quarterly, 1996Q4 to 2026Q2", w.notna().all().all() and len(w) == 119, f"{len(w)} quarters")
last = d.loc["2026Q2"]
check("D2 levels are the size Sweden's are: household deposits 2.5-3.5 trn, disposable income 3.0-3.5 trn a year",
      2500 < last.deposits < 3500 and 3000 < last.disposable < 3500, f"{last.deposits:.0f} and {last.disposable:.0f} SEK bn")
check("D3 wages are 0.8-0.95 of household disposable income throughout (the narrow range the wage test works in)",
      0.8 < R["wage_share_of_disposable_range"][0] and R["wage_share_of_disposable_range"][1] < 0.95, str(R["wage_share_of_disposable_range"]))

print("F — the findings (stated as found)")
g1, g1b = R["1_growth_on_wage_growth"], R["1b_growth_on_income_growth"]
check("F1 a year's deposit growth does not follow its wage growth: slope within 2 s.e. of zero, R² below 0.05",
      abs(g1["wage growth"]["coef"]) < 2 * g1["wage growth"]["se"] and g1["r2"] < 0.05,
      f"slope {g1['wage growth']['coef']} (s.e. {g1['wage growth']['se']}), R² {g1['r2']}")
check("F2 it does follow disposable income growth: slope more than 2 s.e. from zero, R² at least 5x the wage fit's",
      g1b["income growth"]["coef"] > 2 * g1b["income growth"]["se"] and g1b["r2"] > 5 * g1["r2"],
      f"slope {g1b['income growth']['coef']} (s.e. {g1b['income growth']['se']}), R² {g1b['r2']}")
sf = R["2_stock_flow"]
check("F3 deposits accumulate saving (0.2-0.5 of each krona saved, t > 2); wage change adds nothing significant once saving is in",
      0.2 < sf["saving"]["coef"] < 0.5 and sf["saving"]["coef"] > 2 * sf["saving"]["se"] and abs(sf["wage change"]["coef"]) < 2 * sf["wage change"]["se"],
      f"saving {sf['saving']['coef']} (s.e. {sf['saving']['se']}), wage change {sf['wage change']['coef']} (s.e. {sf['wage change']['se']})")
ws, ws_b = R["3_wage_share_levels"], R["3b_wage_share_no_trend"]
check("F4 relative to income, deposits are LOWER when wages are a larger share of it — the sign against a wage franchise, with and without a trend",
      ws["log wage share"]["coef"] + 2 * ws["log wage share"]["se"] < 0 and ws_b["log wage share"]["coef"] + 2 * ws_b["log wage share"]["se"] < 0,
      f"{ws['log wage share']['coef']} (s.e. {ws['log wage share']['se']}); no trend {ws_b['log wage share']['coef']}")
ep = R["4c_hikes_2021Q4_2024Q2"]
check("F5 through the 2022-24 hikes deposits fell relative to income, 1-5% per point of the cost of holding them",
      -0.05 < ep["semi_elasticity_per_pp"] < -0.01, f"{ep['semi_elasticity_per_pp']} per pp; ratio {ep['deposits_over_disposable']}")
th = R["5_nonwage_share_to_households"]
check("F6 households receive about half of the economy's non-wage income (0.4-0.75, long-run mean)", 0.4 < th["mean_1996_2025"] < 0.75, str(th))

n_ok = sum(ok for _, ok, _ in RESULTS)
print(f"\n{n_ok}/{len(RESULTS)} checks passed")
sys.exit(0 if n_ok == len(RESULTS) else 1)
