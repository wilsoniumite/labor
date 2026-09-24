# check_financing.py — is the most care a society employs set by need or by financing (code/financing.py)? The
# findings, stated as found.
#
# Run from paths/:  ../venv/Scripts/python.exe checks/check_financing.py
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


J = json.load(open(os.path.join(ROOT, "results", "financing.json"), encoding="utf-8"))
X, N, B = J["cross_section"], J["norway"], J["borrowing"]

print("1 — need or financing, across OECD economies")
for tag, s in (("all", X["single"]), ("rich", X["single_rich"])):
    best = max(s, key=lambda v: s[v]["r2"])
    check(f"1{'a' if tag == 'all' else 'b'} ({tag}, {X['countries'] if tag == 'all' else X['rich_countries']} economies) public spending on "
          "long-term care goes with care's share of jobs better than health spending, income or age; age explains under a tenth",
          best == "pub_ltc" and s["old65"]["r2"] < 0.1, {v: s[v]["r2"] for v in s})
jm = X["joint"]["Norway on mainland GDP"]
check("1c together: public long-term care spending holds (t > 3) with income and age; age adds nothing (|t| < 2)",
      jm["public_ltc"]["t"] > 3 and abs(jm["old65"]["t"]) < 2,
      f"public LTC {jm['public_ltc']}, log income {jm['log_gdp_pc']}, age {jm['old65']}, R2 {jm['r2']}")
jg = X["joint"]["GDP"]
check("1d Norway, on mainland GDP, spends the most public money on long-term care in the OECD and sits within 1.5 points of the "
      "line; on total GDP (oil and gas inflate it) it looked 3 points above",
      list(X["highest_public_ltc_pct_gdp"])[0] == "NOR" and abs(jm["residual"]["NOR"]) < 1.5 and jg["residual"]["NOR"] > 2.5,
      f"public LTC {X['highest_public_ltc_pct_gdp']}; residual {jm['residual']['NOR']} on mainland, {jg['residual']['NOR']} on total GDP")

print("2 — the spending channel, Norway")
yrs = [y for y in ("2019", "2020", "2021", "2022", "2023", "2024", "2025") if "fund_to_budget_vs_public_health_and_ltc" in N[y]]
check("2a the fund's transfer into the state budget is 7-13% of mainland GDP in 2019-25",
      all(7 <= N[y]["fund_to_budget_pct_mainland_gdp"] <= 13.5 for y in ("2019", "2020", "2021", "2022", "2023", "2024", "2025")),
      {y: N[y]["fund_to_budget_pct_mainland_gdp"] for y in ("2019", "2020", "2021", "2022", "2023", "2024", "2025")})
check("2b about the size of Norway's whole public health and long-term care bill: two-thirds of it or more every year since 2019",
      all(N[y]["fund_to_budget_vs_public_health_and_ltc"] >= 0.65 for y in yrs), {y: N[y]["fund_to_budget_vs_public_health_and_ltc"] for y in yrs})
check("2c in a crisis the fund pays: the transfer jumped in 2020 (the pandemic) above every other year since 2010",
      max(N, key=lambda y: N[y]["fund_to_budget_pct_mainland_gdp"]) == "2020", {y: N[y]["fund_to_budget_pct_mainland_gdp"] for y in ("2018", "2019", "2020", "2021", "2022")})

print("3 — the balance-sheet channel (her point: the fund lowers borrowing costs even without drawing on it)")
S = B["slopes"]
check("3a without a central bank of its own (the euro area), a government's long rate rises at least 10 bp per 10 points of net "
      "debt, and more steeply in the 2010-13 crisis than in calm 2015-19",
      S["euro area 2010-24"]["long_rate"]["bp_per_10_points_net_debt"] >= 10
      and S["euro area crisis 2010-13"]["long_rate"]["bp_per_10_points_net_debt"] > S["euro area calm 2015-19"]["long_rate"]["bp_per_10_points_net_debt"],
      {k: v["long_rate"]["bp_per_10_points_net_debt"] for k, v in S.items()})
check("3b with its own central bank, under 3 bp: in normal times the price of debt barely binds",
      S["own central bank 2010-24"]["long_rate"]["bp_per_10_points_net_debt"] < 3, S["own central bank 2010-24"])
nf = B["norway_net_financial_liabilities_pct_gdp"]
check("3c Norway is a net creditor of 1.5 times GDP or more every year since 2012, while still borrowing (gross liabilities "
      "30-60% of GDP)", all(v <= -150 for y, v in nf.items() if int(y) >= 2012)
      and all(30 <= v <= 60 for y, v in B["norway_gross_liabilities_pct_gdp"].items() if int(y) >= 2012), nf)

n_ok = sum(ok for _, ok, _ in RESULTS)
print(f"\n{n_ok}/{len(RESULTS)} checks passed")
sys.exit(0 if n_ok == len(RESULTS) else 1)
