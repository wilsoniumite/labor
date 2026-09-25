# check_decoupling.py — output rising while work does not (code/decoupling.py): the findings, stated as found.
#
# Run from paths/:  ../venv/Scripts/python.exe checks/check_decoupling.py
# Exit status 0 only if every check passes.

from __future__ import annotations

import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


J = json.load(open(os.path.join(ROOT, "results", "decoupling.json"), encoding="utf-8"))
OW, NC, MF, BO, WG = J["output_and_work"], J["nowcast"], J["manufacturing"], J["ai_build_out"], J["where_the_displaced_go"]
w = OW["windows"]
recent = next(v for k, v in w.items() if k.startswith("2023-04"))
before = w["2015-01 to 2019-10"]
check("D1 output without hours: since 2023Q2 US business output has grown over 2% a year while hours grew under 0.5%; output per "
      "hour faster than in 2015-19",
      recent["output_pct_a_year"] > 2 and recent["hours_pct_a_year"] < 0.5 and recent["output_per_hour_pct_a_year"] > before["output_per_hour_pct_a_year"] + 0.5,
      f"since 2023Q2 {recent}; 2015-19 {before}")
ls = OW["labour_share"]
check("D2 labour's share of business output at its lowest since 1947, down 3 points or more in a year — a fall that since 1990 "
      "only recessions and their recoveries matched",
      ls["is_record_low"] and ls["four_quarter_change"] <= -3 and all(k[:4] in ("2002", "2009", "2013", "2021") for k in ls["larger_four_quarter_falls_since_1990"]),
      f"index {ls['index_2017_100']} (previous low {ls['previous_record_low']}); four quarters {ls['four_quarter_change']}; larger falls {ls['larger_four_quarter_falls_since_1990']}")
check("D3 the nowcast is strong and noisy: GDPNow puts the quarter in progress at 4% or more; its final nowcasts have missed "
      "published growth by more than a point on average",
      NC["gdpnow_current_quarter"]["pct_saar"] >= 4 and NC["gdpnow_error"]["mean_abs"] > 1,
      f"{NC['gdpnow_current_quarter']}; mean absolute miss {NC['gdpnow_error']['mean_abs']} (largest recent {NC['gdpnow_error']['largest_recent_miss']})")
m = MF["changes_pct"]["since 2019-12"]
check("D4 AI lifts a narrow slice of manufacturing: semiconductors up over 50% since 2019, all manufacturing within 3%, "
      "manufacturing jobs down", m["semiconductors"] > 50 and abs(m["all manufacturing"]) < 3 and m["manufacturing jobs"] < 0, m)
ch = BO["change_since_2022_pts"]
check("D5 the build-out leaks abroad: since 2022 computer imports rose more (% of GDP) than investment in information processing "
      "equipment; net of them the build-out is below its 2022 level and within half a point of its 2015-22 trend — the crash "
      "model's assumed 1.5% of GDP is over three times the measure",
      -ch["less: imports of computers, peripherals and parts"] > ch["information processing equipment"] and BO["net_above_2022_pts"] < 0
      and abs(BO["net_above_2015_22_trend_pts"]) < 0.5 and BO["crash_model_assumed_pct_gdp"] > 3 * BO["net_above_2015_22_trend_pts"],
      f"since 2022 {ch}; net above trend {BO['net_above_2015_22_trend_pts']}, above 2022 {BO['net_above_2022_pts']}")
p = WG["prime_age_25_54"]
now = p["since_the_employment_peak"]
check("D6 the displaced leave the labour force: since the prime-age employment peak at least three-quarters of the fall in the "
      "employment rate is participation, against under 0.4 in 2000-03 and 2007-10 (small changes: survey noise is a few tenths)",
      now["exit_share"] >= 0.75 and p["2007-10 (recession)"]["exit_share"] < 0.4 and p["2000-03 (recession and the China shock)"]["exit_share"] < 0.4,
      {k: (v["window"], v["employment_rate_change"], v["exit_share"]) for k, v in p.items()})

n_ok = sum(ok for _, ok, _ in RESULTS)
print(f"\n{n_ok}/{len(RESULTS)} checks passed")
sys.exit(0 if n_ok == len(RESULTS) else 1)
