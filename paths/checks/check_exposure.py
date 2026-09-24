# check_exposure.py — the two waves' inputs (code/exposure.py) and Baumol concentration (code/baumol.py): the
# measurements are what they say, and the findings, stated as found.
#
# Run from paths/:  ../venv/Scripts/python.exe checks/check_exposure.py
# Exit status 0 only if every check passes.

from __future__ import annotations

import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "code"))
import global_crash as gc  # noqa: E402

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


E = json.load(open(os.path.join(ROOT, "results", "exposure.json"), encoding="utf-8"))
B = json.load(open(os.path.join(ROOT, "results", "baumol.json"), encoding="utf-8"))
X, C = E["regions"], E["cyclicality"]

print("E — who is exposed to which wave (ILOSTAT)")
check("E1 each region's shares of employment by group sum to one",
      all(abs(sum(X[r]["share"].values()) - 1) < 1e-3 for r in X), {r: X[r]["share"] for r in X})
check("E2 the first wave's reach: cognitive work is 56-65% of employment in the US, the euro area and Sweden, 20% in China; "
      "physical work 70% in China",
      all(0.55 <= X[r]["share"]["cognitive"] <= 0.66 for r in ("US", "EA", "SE")) and X["CN"]["share"]["cognitive"] < 0.25
      and X["CN"]["share"]["physical"] > 0.65, {r: X[r]["share"]["cognitive"] for r in X})
check("E3 pay: cognitive work pays above the average and physical and in-person work below it, in every measured region",
      all(X[r]["premium"]["cognitive"] > 1 > X[r]["premium"]["physical"] > X[r]["premium"]["in_person"] for r in ("US", "EA", "SE")),
      {r: X[r]["premium"] for r in ("US", "EA", "SE")})
check("E4 recessions cut physical work at least twice as fast as all employment, and cognitive work more slowly — the US "
      "2007-10, Spain 2007-10, Sweden 2008-10",
      all(C[c]["physical"]["beta"] >= 2 and C[c]["cognitive"]["beta"] < 1 for c in C),
      {c: (C[c]["cognitive"]["beta"], C[c]["physical"]["beta"]) for c in C})
check("E5 before robotics, the automatable share of a recession's job loss: under half in the US, euro area and Sweden, under "
      "10% in China",
      all(X[r]["recession_loss_share"]["cognitive"] < 0.5 for r in ("US", "EA", "SE")) and X["CN"]["recession_loss_share"]["cognitive"] < 0.1,
      {r: X[r]["recession_loss_share"]["cognitive"] for r in X})
check("E6 the crash model's recession betas are the measured US ones",
      all(abs(gc.Common().beta[g] - E["beta_used"][g]) < 0.005 for g in gc.GROUPS), E["beta_used"])

K = E["care"]
check("E7 the ceiling: the largest care share any rich economy measured employs is Norway's, above every region's today, and it "
      "is the crash model's",
      K["ceiling_country"] == "NOR" and all(K["regions"][r]["care_share_pct"] < K["ceiling_pct"] for r in K["regions"])
      and abs(gc.Common().care_ceiling - K["ceiling_pct"]) < 1e-9,
      f"{K['ceiling_pct']}% ({K['ceiling_country']}); room {({r: v['headroom_pts'] for r, v in K['regions'].items()})}")
check("E8 the gate: in every region men work in care at a fifth to a third of women's rate, so displaced physical workers "
      "(mostly men) enter more slowly than cognitive ones",
      all(0.2 <= K["regions"][r]["men_vs_women_in_care"] <= 0.34 and K["regions"][r]["gate"]["physical"] < K["regions"][r]["gate"]["cognitive"] for r in K["regions"]),
      {r: (v["men_vs_women_in_care"], v["gate"]["cognitive"], v["gate"]["physical"]) for r, v in K["regions"].items()})
check("E9 need or financing? Care's share rises with the public sector's share of employment across rich economies — a first "
      "look only (employer type is not financing: the Netherlands runs care privately with public money)",
      K["care_vs_public_employment"]["correlation"] > 0.4 and K["care_vs_public_employment"]["countries"] >= 12, K["care_vs_public_employment"])

print("B — Baumol concentration, stated as found")
U = B["us_payrolls"]
w24, w12 = U["windows"]["24 months"], U["windows"]["12 months"]
check("B1 US payrolls, the last two years: health care and social assistance added at least 90% of net job growth, women "
      "at least 70%",
      w24["health_and_social_pct_of_net"] >= 90 and w24["women_pct_of_net"] >= 70,
      f"{w24['from']} to {w24['to']}: care {w24['health_and_social_thousands']}k of {w24['net_thousands']}k "
      f"({w24['health_and_social_pct_of_net']}%), women {w24['women_pct_of_net']}%; last 12 months care {w12['health_and_social_pct_of_net']}%")
check("B2 far above care's share of jobs, and above its share of growth in any expansion since 1991",
      w24["health_and_social_pct_of_net"] > 5 * U["level"]["health_and_social_share_pct"]
      and all(v["health_and_social_pct_of_net"] < 40 for v in U["expansions"].values()),
      {k: v["health_and_social_pct_of_net"] for k, v in U["expansions"].items()})
R = U["recessions"]
check("B3 care holds in an ordinary recession and fell only in the in-person shock: it grew through 2001 and 2008-10 while "
      "payrolls fell, and fell in 2020",
      R["2001"]["health_and_social_pct"] > 0 > R["2001"]["payrolls_pct"] and R["2008-10"]["health_and_social_pct"] > 0 > R["2008-10"]["payrolls_pct"]
      and R["2020"]["health_and_social_pct"] < 0, R)
check("B4 austerity reached the public side: US state and local government shed jobs through 2008-13",
      B["us_payrolls"]["austerity_2008_13"]["state_and_local_thousands"] < -500, B["us_payrolls"]["austerity_2008_13"])
L = B["labour_force_surveys"]
check("B5 Germany concentrates like the US: health and social work at least 70% of net employment growth 2022-25, "
      "manufacturing shrinking",
      L["DEU"]["2022-2025"]["health_and_social_pct_of_net"] >= 70 and L["DEU"]["2022-2025"]["manufacturing_thousands"] < 0,
      {k: L["DEU"]["2022-2025"][k] for k in ("health_and_social_pct_of_net", "care_and_teaching_pct_of_net", "manufacturing_thousands")})
se = L["SE"]
check("B6 Sweden does not: care's share of employment unchanged 2019-25 within half a point; yet women took at least 90% "
      "of net growth in 2022-25",
      abs(se["2019-2025"]["health_and_social_share_of_employment_pct"]["2025"] - se["2019-2025"]["health_and_social_share_of_employment_pct"]["2019"]) <= 0.5
      and se["2022-2025"]["women_pct_of_net"] >= 90,
      {"care share": se["2019-2025"]["health_and_social_share_of_employment_pct"], "women 2022-25": se["2022-2025"]["women_pct_of_net"]})
check("B7 care is three-quarters women everywhere measured (72-81%)",
      all(72 <= L[a]["2022-2025"]["health_and_social_women_pct"] <= 82 for a in ("US", "SE", "EA5", "DEU", "FRA", "ITA", "ESP", "NLD")),
      {a: L[a]["2022-2025"]["health_and_social_women_pct"] for a in L})
P = B["premise_us"]
check("B8 Baumol's premise, US: health care's price about doubled against goods since 1990, and its spending share rose "
      "13% to 17%",
      P["by_year"]["2026"]["price_vs_goods_1990_1"] >= 1.8 and P["by_year"]["1990"]["health_care_share_of_consumer_spending_pct"] < 14
      and P["by_year"]["2026"]["health_care_share_of_consumer_spending_pct"] > 16, P["by_year"])
check("B9 but since 2008 the share rose while health care's price fell against all consumer prices — a volume shift (ageing, "
      "coverage), not the price-driven concentration of the paper's proposition; 1990-2008 was consistent with it (sigma < 1)",
      P["implied_sigma"]["2008-2026"]["relative_price_log_points"] < 0 < P["implied_sigma"]["2008-2026"]["share_odds_log_points"]
      and P["implied_sigma"]["1990-2008"]["implied_sigma"] < 1, P["implied_sigma"])
Y = B["pay"]
check("B10 the absorbing sector pays below the average in Sweden, Germany, France and the Netherlands (0.83-0.87), and US "
      "education and health pay has slipped against all private pay since 2010",
      all(Y["health_and_social_by_country"][a]["health_and_social_vs_average"] < 0.9 for a in ("SWE", "DEU", "FRA", "NLD"))
      and list(Y["us_education_and_health_vs_private_hourly"].values())[-1] < Y["us_education_and_health_vs_private_hourly"]["2010"],
      {**{a: v["health_and_social_vs_average"] for a, v in Y["health_and_social_by_country"].items()}, "US hourly": Y["us_education_and_health_vs_private_hourly"]})
check("B11 the state pays for most of it: US Medicare and Medicaid benefits come to at least half of consumer spending on "
      "health care", B["who_pays"]["us_medicare_medicaid_vs_health_care_spending"] >= 0.5, B["who_pays"])

n_ok = sum(ok for _, ok, _ in RESULTS)
print(f"\n{n_ok}/{len(RESULTS)} checks passed")
sys.exit(0 if n_ok == len(RESULTS) else 1)
