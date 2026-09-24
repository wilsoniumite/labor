# check_global_crash.py — the four-region crash model (code/global_crash.py): the mechanics are what they say, the
# history is reproduced (and where it is not, the bias is stated), and the findings, stated as found.
#
# Run from paths/:  ../venv/Scripts/python.exe checks/check_global_crash.py
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
import global_crash as gc  # noqa: E402

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


J = json.load(open(os.path.join(ROOT, "results", "global_crash.json"), encoding="utf-8"))
V, S = J["validation"], J["scenarios"]
fp = V["fitted"]
cm = replace(gc.Common(), sigma=fp["sigma"], money=fp["money"], debt_deflation=fp["debt_deflation"], kappa_1930=fp["kappa_1930"], a_r=fp["a_r"])
regs = gc.regions_today()
regs.pop("_notes")
regs = {r: (replace(g, okun=fp["okun_us"]) if r == "US" else g) for r, g in regs.items()}

print("V — history, one parameter set")
m1, t1 = V["model"]["1929-33"], V["targets"]["1929-33"]
check("V1 1929-33 with the 1930s' rules: 1933 output, prices within 5% of the data, unemployment within 5 points; the 1930-32 path within 7%",
      abs(m1["output_over_1929"][3] - t1["output_over_1929"][3]) < 0.05 and abs(m1["prices_over_1929"][3] - t1["prices_over_1929"][3]) < 0.05
      and abs(m1["unemployment"][3] - t1["unemployment"][3]) < 5 and max(abs(a - b) for a, b in zip(m1["output_over_1929"], t1["output_over_1929"])) < 0.07,
      f"output {m1['output_over_1929']} against {t1['output_over_1929']}; unemployment {m1['unemployment']} against {t1['unemployment']}")
m2, t2 = V["model"]["2007-09"], V["targets"]["2007-09"]
check("V2 2007-09 with today's rules: the trough within 1.5 points, the unemployment peak within 1.5 points",
      abs(min(m2["gap_change"]) - min(t2["gap_change"])) < 1.5 and abs(max(m2["unemployment"]) - max(t2["unemployment"])) < 1.5,
      f"trough {min(m2['gap_change'])} against {min(t2['gap_change'])}; peak {max(m2['unemployment'])} against {max(t2['unemployment'])}")
check("V3 the stated bias: the model recovers from 2009 faster than the US did (end-2010 gap closer to zero) — so it is optimistic about how long a crisis lasts",
      m2["gap_change"][-1] > t2["gap_change"][-1] + 1.0, f"end-2010 gap {m2['gap_change'][-1]} against {t2['gap_change'][-1]}")

print("M — the mechanics")
n = 16
calm = {r: replace(g, eta=0.0, drift=0.0, pi0=2.0, i0=cm.r_star + 2.0) for r, g in regs.items()}
o = gc.simulate(calm, {r: gc.MODERN for r in gc.R}, gc.Shock(), cm, n)
check("M1 no shock, no drift, policy at neutral and inflation on target: every region stays at capacity",
      all(np.abs(o[r]["y"]).max() < 1e-9 and np.ptp(o[r]["u"]) < 1e-9 for r in gc.R))
us_only = gc.Shock(demand={"US": gc.ramp(-5.0, 1, 2, n)})
o = gc.simulate(calm, {r: gc.MODERN for r in gc.R}, us_only, cm, n)
check("M2 trade carries a US slump abroad: every other region's gap falls, Sweden's (exports half of GDP) the most of the three",
      all(o[r]["y"].min() < -0.05 for r in ("EA", "SE", "CN")) and o["SE"]["y"].min() < min(o["EA"]["y"].min(), o["CN"]["y"].min()),
      {r: round(float(o[r]["y"].min()), 2) for r in gc.R})
o = gc.simulate(regs, {r: gc.MODERN for r in gc.R}, gc.ai_shock(24), cm, 24)
check("M3 under the backstop, spreads stay under each region's cap and capital above the recapitalisation floor",
      all(o[r]["s"].max() <= regs[r].spread_cap + 1e-9 and o[r]["k"].min() >= gc.MODERN.capital_floor * regs[r].bank_capital - 1e-9 for r in gc.R))
flat = {r: replace(g, groups=g.groups, premium={q: 1.0 for q in gc.GROUPS}, benefit_cap=99.0) for r, g in regs.items()}
now = gc.Waves(split=True, robot_lag=0.0, robot_ramp=0.0)
worst = {r: replace(g, eta=3 * g.eta) for r, g in flat.items()}
diffs = []
for rl in (gc.MODERN, gc.EXPANDED, gc.ERODED):
    a = gc.simulate(worst, {r: rl for r in gc.R}, gc.ai_shock(24), cm, 24)
    b = gc.simulate(worst, {r: rl for r in gc.R}, gc.ai_shock(24), cm, 24, waves=now)
    diffs.append(max(float(np.abs(a[r][k] - b[r][k]).max()) for r in gc.R for k in ("y", "u", "u_star", "k", "deficit_extra")))
check("M4 the split nests the uniform case: every group paid the average, support uncapped and robotics from the start reproduce "
      "the uniform runs exactly (today's, expanding and eroding rules)", max(diffs) < 1e-9, f"largest difference {max(diffs):.1e}")
lag3 = gc.Waves(split=True, robot_lag=3.0)
o = gc.simulate({r: replace(g, eta=3 * g.eta) for r, g in regs.items()}, {r: gc.MODERN for r in gc.R}, gc.ai_shock(24), cm, 24, waves=lag3)
before = int(3.0 / gc.DT)
check("M5 before robotics arrives, nobody in physical work is displaced; after it, they are",
      all(o[r]["s_phys"][:before + 1].max() == 0 and o[r]["s_phys"][-1] > 0 for r in gc.R),
      {r: (float(o[r]["s_phys"][before]), round(float(o[r]["s_phys"][-1]), 2)) for r in gc.R})
w = {r: gc.wave_weights(regs[r], gc.MODERN, cm, lag3) for r in gc.R}
check("M6 a recession's usual mix of job losers weighs what the fit assumed (lost net pay per point = 1 - replacement); a "
      "displaced cognitive worker weighs more",
      all(abs(sum(w[r]["mix"][q] * w[r]["spend"][q] for q in gc.GROUPS) - (1 - regs[r].replacement)) < 1e-9
          and w[r]["spend"]["cognitive"] > 1 - regs[r].replacement for r in gc.R),
      {r: {q: round(w[r]["spend"][q] / (1 - regs[r].replacement), 2) for q in gc.GROUPS} for r in gc.R})

print("F — the findings (year 4, stated as found)")
y4 = lambda k: S[k]["year4"]  # noqa: E731
bo = y4("modern rules | bust only")
check("F1 today's rules, the bust alone: a world recession about 2008's size or larger (the four together at least 5% below capacity)",
      bo["four_weighted_gap_min"] <= -5.0, f"four together {bo['four_weighted_gap_min']}%; US {bo['US']['gap_min']}%")
lab = y4("modern rules | bust + displacement, recessions trigger adoption x3")
check("F2 today's rules with displacement and recessions triggering adoption: a labour depression without an output one — US unemployment above 20% while US output stays within 15% of capacity",
      lab["US"]["unemployment_max"] > 20 and lab["US"]["gap_min"] > -15, f"US unemployment {lab['US']['unemployment_max']}%, gap {lab['US']['gap_min']}%")
er = y4("rules erode under pressure | bust + displacement")
check("F3 when the rules erode (austerity, no backstop, tariffs, looser anchoring): Great Depression scale — the four together 20%+ below capacity, US unemployment 25%+, US banks' capital gone",
      er["four_weighted_gap_min"] <= -20 and er["US"]["unemployment_max"] >= 25 and er["US"]["bank_capital_lost_max"] >= 0.99,
      f"four together {er['four_weighted_gap_min']}%, US unemployment {er['US']['unemployment_max']}%, capital lost {er['US']['bank_capital_lost_max']}")
ex = y4("rules expand under pressure | bust + displacement")
check("F4 when the rules expand (an income guarantee): output held within 10% everywhere, at no more than 6% of US GDP a year — but US unemployment still above 15%: the guarantee holds demand, not jobs",
      all(ex[r]["gap_min"] > -10 for r in gc.R) and ex["US"]["guarantee_cost_max_pct_gdp"] <= 6 and ex["US"]["unemployment_max"] > 15,
      f"gaps {[ex[r]['gap_min'] for r in gc.R]}; US guarantee {ex['US']['guarantee_cost_max_pct_gdp']}% of GDP; US unemployment {ex['US']['unemployment_max']}%")
th = y4("the 1930s' rules | bust + displacement")
check("F5 the 1930s' rules on today's economy are worse still than eroded rules", th["four_weighted_gap_min"] < er["four_weighted_gap_min"],
      f"{th['four_weighted_gap_min']} against {er['four_weighted_gap_min']}")
md = y4("modern rules | bust + displacement")
check("F6 the US leads: the largest unemployment rise of the four under today's rules",
      max(gc.R, key=lambda r: md[r]["unemployment_max"] - regs[r].u0) == "US", {r: round(md[r]["unemployment_max"] - regs[r].u0, 1) for r in gc.R})

print("W — two waves (cognitive now, physical once robotics arrives), stated as found")
row = "modern rules | bust + displacement, recessions trigger adoption x3"
wv = lambda L, h="year4": S[f"{row} | two waves, robotics in {L} years"][h]  # noqa: E731
u4 = [lab["US"]["unemployment_max"]] + [wv(L)["US"]["unemployment_max"] for L in (1, 2, 3)]
check("W1 the robotics lag holds the labour depression back: US year-4 unemployment falls with every year of lag, and with "
      "robotics three years out it is at least 5 points below the uniform case",
      all(a >= b for a, b in zip(u4, u4[1:])) and u4[0] - u4[3] >= 5, f"uniform, 1, 2, 3 years: {u4}")
check("W2 it delays, it does not prevent: with robotics two years out, US unemployment by year 6 is above the uniform case's "
      "at year 4, in this row and with displacement alone",
      wv(2, "year6")["US"]["unemployment_max"] > lab["US"]["unemployment_max"]
      and S["modern rules | bust + displacement | two waves, robotics in 2 years"]["year6"]["US"]["unemployment_max"] > md["US"]["unemployment_max"],
      f"{wv(2, 'year6')['US']['unemployment_max']} against {lab['US']['unemployment_max']}; displacement alone "
      f"{S['modern rules | bust + displacement | two waves, robotics in 2 years']['year6']['US']['unemployment_max']} against {md['US']['unemployment_max']}")
per = lambda x: x["US"]["gap_min"] / (x["US"]["unemployment_max"] - regs["US"].u0)  # noqa: E731
check("W3 the first wave costs more per job: with robotics three years out, US output falls further per point of unemployment "
      "than in the uniform case (the displaced earn 1.2 times the average, with support capped)",
      per(wv(3)) < per(lab), f"{per(wv(3)):.3f} against {per(lab):.3f} points of output per point of unemployment")
cn = [lab["CN"]["unemployment_max"], wv(3)["CN"]["unemployment_max"]]
check("W4 China waits for robotics: with robotics three years out, its year-4 unemployment is at least 1 point below the uniform "
      "case and its displaced are mostly in physical work once robotics arrives",
      cn[0] - cn[1] >= 1 and wv(3, "year6")["CN"]["displaced_physical_end"] > wv(3, "year6")["CN"]["displaced_cognitive_end"],
      f"{cn}; year 6 displaced cognitive {wv(3, 'year6')['CN']['displaced_cognitive_end']}, physical {wv(3, 'year6')['CN']['displaced_physical_end']}")
# the fiscal response starts when unemployment is 2 points up, so a split that raises unemployment more slowly also
# delays the stimulus (China's output is a little worse with the lag in the rows above, for that reason alone)
nofisc = {r: replace(gc.MODERN, fiscal="none") for r in gc.R}
rg3 = {r: replace(g, eta=3 * g.eta) for r, g in regs.items()}
a = gc.summary(gc.simulate(rg3, nofisc, gc.ai_shock(24), cm, 24), regs, 16)
b = gc.summary(gc.simulate(rg3, nofisc, gc.ai_shock(24), cm, 24, waves=lag3), regs, 16)
check("W5 not the fiscal trigger's timing: with no discretionary fiscal response, the lag still cuts US unemployment, the first "
      "wave still costs more output per point of it, and China's output is better with the lag, not worse",
      b["US"]["unemployment_max"] < a["US"]["unemployment_max"] and per(b) < per(a) and b["CN"]["gap_min"] > a["CN"]["gap_min"],
      f"US unemployment {a['US']['unemployment_max']} -> {b['US']['unemployment_max']}; per point {per(a):.3f} -> {per(b):.3f}; "
      f"China gap {a['CN']['gap_min']} -> {b['CN']['gap_min']}")

n_ok = sum(ok for _, ok, _ in RESULTS)
print(f"\n{n_ok}/{len(RESULTS)} checks passed")
sys.exit(0 if n_ok == len(RESULTS) else 1)
