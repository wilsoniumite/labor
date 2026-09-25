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

print("F — the findings (year 4, stated as found; 'non-employment' is unemployment plus those who left the labour force)")
NW = lambda x, r="US": x[r]["not_working_rise_max"]  # noqa: E731
y4 = lambda k: S[k]["year4"]  # noqa: E731
bo = y4("modern rules | bust only")
check("F1 today's rules, the bust alone: a world recession about 2008's size or larger (the four together at least 5% below capacity)",
      bo["four_weighted_gap_min"] <= -5.0, f"four together {bo['four_weighted_gap_min']}%; US {bo['US']['gap_min']}%")
lab = y4("modern rules | bust + displacement, recessions trigger adoption x3")
check("F2 today's rules with displacement and recessions triggering adoption: a jobs depression without an output one — US "
      "non-employment up 20 points or more while output stays within 15% of capacity; measured unemployment shows under half of it",
      NW(lab) >= 20 and lab["US"]["gap_min"] > -15 and lab["US"]["unemployment_max"] - regs["US"].u0 < NW(lab) / 2,
      f"US non-employment +{NW(lab)} (unemployment {lab['US']['unemployment_max']}%, {lab['US']['out_of_labour_force_end']} points out of the labour force), gap {lab['US']['gap_min']}%")
er = y4("rules erode under pressure | bust + displacement")
check("F3 when the rules erode (austerity, no backstop, tariffs, looser anchoring): Great Depression scale — the four together 20%+ "
      "below capacity, US non-employment up 25 points or more, US banks' capital gone",
      er["four_weighted_gap_min"] <= -20 and NW(er) >= 25 and er["US"]["bank_capital_lost_max"] >= 0.99,
      f"four together {er['four_weighted_gap_min']}%, US non-employment +{NW(er)}, capital lost {er['US']['bank_capital_lost_max']}")
ex = y4("rules expand under pressure | bust + displacement")
check("F4 when the rules expand (an income guarantee): output held within 10% everywhere, at no more than 6% of US GDP a year — but "
      "US non-employment still up more than 10 points: the guarantee holds demand, not jobs",
      all(ex[r]["gap_min"] > -10 for r in gc.R) and ex["US"]["guarantee_cost_max_pct_gdp"] <= 6 and NW(ex) > 10,
      f"gaps {[ex[r]['gap_min'] for r in gc.R]}; US guarantee {ex['US']['guarantee_cost_max_pct_gdp']}% of GDP; US non-employment +{NW(ex)}")
th = y4("the 1930s' rules | bust + displacement")
check("F5 the 1930s' rules on today's economy are worse still than eroded rules", th["four_weighted_gap_min"] < er["four_weighted_gap_min"],
      f"{th['four_weighted_gap_min']} against {er['four_weighted_gap_min']}")
md = y4("modern rules | bust + displacement")
check("F6 the US leads: the largest rise in non-employment of the four under today's rules",
      max(gc.R, key=lambda r: NW(md, r)) == "US", {r: NW(md, r) for r in gc.R})

print("X — the participation margin and the measured build-out (decoupling.py), stated as found")
dec = json.load(open(os.path.join(ROOT, "results", "decoupling.json"), encoding="utf-8"))
check("X1 the inputs are the measured ones: the US build-out net of computer imports above its 2015-22 trend, and the US exit share "
      "since the prime-age employment peak; the other regions keep the displaced in the labour force (not measured)",
      abs(regs["US"].ai_capex - dec["ai_build_out"]["net_above_2015_22_trend_pts"]) < 1e-9
      and abs(regs["US"].exit_share - dec["where_the_displaced_go"]["prime_age_25_54"]["since_the_employment_peak"]["exit_share"]) < 1e-9
      and all(regs[r].exit_share == 0 for r in ("EA", "SE", "CN")),
      f"US build-out {regs['US'].ai_capex}% of GDP (assumed 1.5 before), exit share {regs['US'].exit_share}")
old_us = {r: (replace(g, ai_capex=1.5, drift=0.0) if r == "US" else replace(g, drift=0.0)) for r, g in regs.items()}
new_us = {r: replace(g, drift=0.0) for r, g in regs.items()}
a = gc.summary(gc.simulate(old_us, {r: gc.MODERN for r in gc.R}, gc.ai_shock(24), cm, 24), regs, 16)
b = gc.summary(gc.simulate(new_us, {r: gc.MODERN for r in gc.R}, gc.ai_shock(24), cm, 24), regs, 16)
check("X2 measured, the build-out makes the US bust milder: the bust alone takes US output at worst over a point less below capacity "
      "than with the 1.5% of GDP assumed before — the imported servers' collapse lands abroad",
      b["US"]["gap_min"] - a["US"]["gap_min"] >= 1, f"US gap {a['US']['gap_min']} assumed -> {b['US']['gap_min']} measured")
dep6 = S["modern rules | bust + displacement, recessions trigger adoption x3 | two waves, robotics in 2 years"]["year6"]["US"]
check("X3 exits hide a jobs depression from the unemployment rate: by year 6 (robotics two years out) US unemployment reads under "
      "20% while more than 20 points have left the labour force",
      dep6["unemployment_max"] < 20 and dep6["out_of_labour_force_end"] > 20,
      f"unemployment {dep6['unemployment_max']}%, out of the labour force {dep6['out_of_labour_force_end']}, non-employment +{dep6['not_working_rise_max']}")
nb = lambda rn, h: S[f"{rn} | displacement without a bust"][h]["US"]  # noqa: E731
check("X4 displacement without a bust (where the US is): fiscal triggers keyed to unemployment fire late — by year 4 output is "
      "1.5 points or more further below capacity than with triggers keyed to non-employment; a temporary stimulus then runs out, "
      "and by year 6 both are near -7% while an income guarantee holds output within 4%",
      nb("modern rules", "year4")["gap_min"] <= nb("modern rules, triggers on non-employment", "year4")["gap_min"] - 1.5
      and abs(nb("modern rules", "year6")["gap_min"] - nb("modern rules, triggers on non-employment", "year6")["gap_min"]) < 1.5
      and nb("rules expand under pressure", "year6")["gap_min"] > -4,
      {k: (nb(k, "year4")["gap_min"], nb(k, "year6")["gap_min"]) for k in ("modern rules", "modern rules, triggers on non-employment", "rules expand under pressure")})
t0 = S["modern rules | bust + displacement, recessions trigger adoption x3"]["year6"]
t1 = S["modern rules, triggers on non-employment | bust + displacement, recessions trigger adoption x3"]["year6"]
check("X5 in a bust the cyclical rise in unemployment fires the triggers either way: keying them to non-employment changes nothing",
      all(abs(t0[r]["gap_min"] - t1[r]["gap_min"]) < 1e-9 for r in gc.R), {r: (t0[r]["gap_min"], t1[r]["gap_min"]) for r in gc.R})

print("W — two waves (cognitive now, physical once robotics arrives), stated as found")
row = "modern rules | bust + displacement, recessions trigger adoption x3"
wv = lambda L, h="year4": S[f"{row} | two waves, robotics in {L} years"][h]  # noqa: E731
u4 = [NW(lab)] + [NW(wv(L)) for L in (1, 2, 3)]
check("W1 the robotics lag holds the jobs depression back: US year-4 non-employment falls with every year of lag, and with robotics "
      "three years out it is at least 5 points below the uniform case",
      all(a_ >= b_ for a_, b_ in zip(u4, u4[1:])) and u4[0] - u4[3] >= 5, f"uniform, 1, 2, 3 years: {u4}")
d2 = S["modern rules | bust + displacement | two waves, robotics in 2 years"]["year6"]
check("W2 it delays, it does not prevent: with robotics two years out, US non-employment by year 6 is above the uniform case's at "
      "year 4, in this row and with displacement alone",
      NW(wv(2, "year6")) > NW(lab) and NW(d2) > NW(md), f"{NW(wv(2, 'year6'))} against {NW(lab)}; displacement alone {NW(d2)} against {NW(md)}")
per = lambda x: x["US"]["gap_min"] / NW(x)  # noqa: E731
check("W3 the first wave costs more per job: with robotics three years out, US output falls further per point of non-employment "
      "than in the uniform case (the displaced earn 1.2 times the average, with support capped)",
      per(wv(3)) < per(lab), f"{per(wv(3)):.3f} against {per(lab):.3f} points of output per point of non-employment")
cn = [NW(lab, "CN"), NW(wv(3), "CN")]
check("W4 China waits for robotics: with robotics three years out, its year-4 non-employment rise is at least 1 point below the uniform "
      "case and its displaced are mostly in physical work once robotics arrives",
      cn[0] - cn[1] >= 1 and wv(3, "year6")["CN"]["displaced_physical_end"] > wv(3, "year6")["CN"]["displaced_cognitive_end"],
      f"{cn}; year 6 displaced cognitive {wv(3, 'year6')['CN']['displaced_cognitive_end']}, physical {wv(3, 'year6')['CN']['displaced_physical_end']}")
# the fiscal response starts when unemployment is 2 points up, so a split that raises unemployment more slowly also
# delays the stimulus (China's output is a little worse with the lag in the rows above, for that reason alone)
nofisc = {r: replace(gc.MODERN, fiscal="none") for r in gc.R}
rg3 = {r: replace(g, eta=3 * g.eta) for r, g in regs.items()}
a = gc.summary(gc.simulate(rg3, nofisc, gc.ai_shock(24), cm, 24), regs, 16)
b = gc.summary(gc.simulate(rg3, nofisc, gc.ai_shock(24), cm, 24, waves=lag3), regs, 16)
check("W5 not the fiscal trigger's timing: with no discretionary fiscal response, the lag still cuts US non-employment, the first "
      "wave still costs more output per point of it, and China's output is better with the lag, not worse",
      NW(b) < NW(a) and per(b) < per(a) and b["CN"]["gap_min"] > a["CN"]["gap_min"],
      f"US non-employment +{NW(a)} -> +{NW(b)}; per point {per(a):.3f} -> {per(b):.3f}; China gap {a['CN']['gap_min']} -> {b['CN']['gap_min']}")

print("C — care as the absorber (robotics two years out), stated as found")
ab = gc.Waves(split=True, robot_lag=2.0, absorb=True)
nab = gc.Waves(split=True, robot_lag=2.0)
diffs = []
for rl in (gc.ERODED, replace(gc.MODERN, care="cut")):
    a = gc.simulate(rg3, {r: rl for r in gc.R}, gc.ai_shock(24), cm, 24, waves=nab)
    b = gc.simulate(rg3, {r: rl for r in gc.R}, gc.ai_shock(24), cm, 24, waves=ab)
    diffs.append(max(float(np.abs(a[r][k] - b[r][k]).max()) for r in gc.R for k in ("y", "u", "u_star", "k", "out")))
check("C1 the absorber nests the split: when the rules hire none of the displaced into care, the runs are the split's exactly",
      max(diffs) < 1e-9, f"largest difference {max(diffs):.1e}")
runs_c = {lab_: gc.simulate(rg3, {r: rl for r in gc.R}, gc.ai_shock(24), c, 24, waves=ab) for lab_, rl, c in
          (("build", gc.CARE, cm), ("fast", replace(gc.CARE, care_pace=3.0), cm), ("fast, no ceiling", replace(gc.CARE, care_pace=3.0), replace(cm, care_ceiling=100.0)),
           ("trend", gc.MODERN, cm))}
check("C2 care never passes the ceiling (Norway's 20.1% of employment), trend and build-out together",
      all(runs_c[k][r]["care"].max() <= cm.care_ceiling + 1e-9 for k in ("build", "fast", "trend") for r in gc.R),
      {r: round(float(runs_c["fast"][r]["care"].max()), 2) for r in gc.R})
o = runs_c["build"]
phys_pool = {r: float((o[r]["s_phys"][-1] + o[r]["at_phys"][-1] + o[r]["ax_phys"][-1])
                      / (o[r]["s_cog"][-1] + o[r]["s_phys"][-1] + o[r]["at_cog"][-1] + o[r]["at_phys"][-1] + o[r]["ax_cog"][-1] + o[r]["ax_phys"][-1])) for r in gc.R}
phys_abs = {r: float((o[r]["at_phys"][-1] + o[r]["ax_phys"][-1]) / (o[r]["at_cog"][-1] + o[r]["at_phys"][-1] + o[r]["ax_cog"][-1] + o[r]["ax_phys"][-1])) for r in gc.R}
check("C3 the gate: the physical wave, mostly men, is under-represented among those care takes in",
      all(phys_abs[r] < phys_pool[r] for r in gc.R), {r: (round(phys_abs[r], 2), round(phys_pool[r], 2)) for r in gc.R})
y6 = lambda rn, dial, wl: S[f"{rn} | {dial} | two waves, robotics in 2 years{wl}"]["year6"]  # noqa: E731
row3 = "bust + displacement, recessions trigger adoption x3"
row1 = "bust + displacement"
none_, trend_, build_ = y6("modern rules", row3, ""), y6("modern rules", row3, ", care absorbs"), y6("rules expand into care", row3, ", care absorbs")
check("C4 care's trend jobs exist anyway: taking them lowers US non-employment a little but does not raise output (the displaced "
      "take them from people who would have entered work)",
      NW(trend_) < NW(none_) and trend_["US"]["gap_min"] <= none_["US"]["gap_min"],
      f"non-employment +{NW(none_)} -> +{NW(trend_)}; gap {none_['US']['gap_min']} -> {trend_['US']['gap_min']}")
check("C5 a funded build-out, a point of employment a year: in the labour-depression row, US year-6 non-employment at least 5 points "
      "lower, at no more than 1.5% of GDP a year, with US care at the ceiling",
      NW(none_) - NW(build_) >= 5 and build_["US"]["care_cost_max_pct_gdp"] <= 1.5 and build_["US"]["care_share_end"] >= cm.care_ceiling - 0.05,
      f"+{NW(none_)} -> +{NW(build_)}; cost {build_['US']['care_cost_max_pct_gdp']}% of GDP; care {build_['US']['care_share_end']}%")
fast_, open_ = y6("rules expand into care", row3, ", care absorbs, three points a year"), y6("rules expand into care", row3, ", care absorbs, three points a year, no ceiling")
check("C6 in the US the ceiling is the limit, not the pace: three points a year gains under a point by year 6; without the "
      "ceiling it gains more than five",
      NW(build_) - NW(fast_) < 1 and NW(fast_) - NW(open_) > 5,
      f"a point a year +{NW(build_)}, three +{NW(fast_)}, three without the ceiling +{NW(open_)} (care {open_['US']['care_share_end']}%)")
struct = build_["US"]["displaced_cognitive_end"] + build_["US"]["displaced_physical_end"]
room = cm.care_ceiling - regs["US"].care_share
check("C7 care cannot rescue the jobs depression: the US displaced still out of work at year 6 are several times the room care had "
      "(Norway's share less today's), and US non-employment stays up more than 20 points even without a ceiling",
      struct >= 3 * room and NW(open_) > 20, f"still displaced {struct:.1f} points against room {room:.1f}; without a ceiling +{NW(open_)}")
se1, se0 = y6("rules expand into care", row1, ", care absorbs")["SE"], y6("modern rules", row1, "")["SE"]
check("C8 Sweden, displacement alone: the build-out takes year-6 unemployment down at least 2.5 points and care stays under the "
      "ceiling — there the gate and the pace of training bind, not the ceiling",
      se0["unemployment_max"] - se1["unemployment_max"] >= 2.5 and se1["care_share_end"] < cm.care_ceiling - 1,
      f"{se0['unemployment_max']} -> {se1['unemployment_max']}; care {se1['care_share_end']}%")
g_ = y6("rules expand under pressure", row3, "")
per_c = (NW(none_) - NW(build_)) / build_["US"]["care_cost_max_pct_gdp"]
per_g = (NW(none_) - NW(g_)) / g_["US"]["guarantee_cost_max_pct_gdp"]
check("C9 care buys jobs, the guarantee buys demand: per point of GDP a year, the build-out takes more off US non-employment than "
      "the income guarantee, but the guarantee holds output far closer to capacity",
      per_c > per_g and g_["US"]["gap_min"] > build_["US"]["gap_min"] + 5,
      f"points of non-employment per % of GDP: care {per_c:.1f}, guarantee {per_g:.1f}; gap: care {build_['US']['gap_min']}, guarantee {g_['US']['gap_min']}")
er_ = y6("rules erode under pressure", row3, ", care absorbs")
check("C10 when the rules erode, care takes in nobody and stops growing",
      all(er_[r]["absorbed_into_existing_care_jobs_end"] + er_[r]["absorbed_into_new_care_jobs_end"] == 0
          and abs(er_[r]["care_share_end"] - regs[r].care_share) < 1e-6 for r in gc.R), {r: er_[r]["care_share_end"] for r in gc.R})
sens = {}
for h in (0.10, 0.50):
    o = gc.summary(gc.simulate(rg3, {r: gc.CARE for r in gc.R}, gc.ai_shock(24), replace(cm, care_hire=h), 24, waves=ab), regs)
    sens[h] = (NW(o), o["US"]["care_share_end"], o["SE"]["unemployment_max"])
check("C11 how fast care trains and hires (0.10 or 0.50 of the willing a quarter, against 0.25): US non-employment stays up more than "
      "25 points with the build-out either way; Sweden's result moves with it (there it binds)",
      all(v[0] > 25 for v in sens.values()) and abs(sens[0.10][2] - sens[0.50][2]) > 1, sens)

print("K — the financing limit (what pays for the build-out), stated as found")
fin = json.load(open(os.path.join(ROOT, "results", "financing.json"), encoding="utf-8"))
check("K1 the inputs are the measured ones: taxes on labour and the highest take (Austria), and the price of debt with and without "
      "a central bank of one's own",
      abs(cm.tax_max - fin["labour_taxes"]["oecd_highest"]["labour_taxes_pct_gdp"]) < 1e-9
      and all(abs(regs[r].labour_tax - fin["labour_taxes"]["regions"][r]["labour_taxes_pct_gdp"]) < 1e-9 for r in gc.R)
      and regs["EA"].debt_slope_crisis > regs["EA"].debt_slope > 10 > 1 > regs["US"].debt_slope,
      {r: (regs[r].labour_tax, regs[r].debt_slope, regs[r].debt_slope_crisis) for r in gc.R})
flat_price = {r: replace(g, eta=3 * g.eta, debt_slope=0.0, debt_slope_crisis=0.0) for r, g in regs.items()}
nc = replace(cm, care_ceiling=100.0)
a = gc.simulate(flat_price, {r: gc.CARE for r in gc.R}, gc.ai_shock(24), nc, 24, waves=ab)
b = gc.simulate(flat_price, {r: gc.CARE_LEVY for r in gc.R}, gc.ai_shock(24), replace(nc, ai_levy=1e6), 24, waves=ab)
d = max(float(np.abs(a[r][k] - b[r][k]).max()) for r in gc.R for k in ("y", "u", "care", "out"))
check("K2 the source changes only the limit, the drag and the price: with debt free and the levy unlimited, borrowing and the levy "
      "give the same paths", d < 1e-9, f"largest difference {d:.1e}")
fl = lambda rn, dial, fast=True: S[f"{rn} | {dial} | two waves, robotics in 2 years, care absorbs, financing limit" + (", three points a year" if fast else "")]["year6"]  # noqa: E731
tx, lv, bo = fl("care financed by labour taxes", row3), fl("care financed by a levy on AI income", row3), fl("care financed by borrowing", row3)
check("K3 taxes on labour lose room as displacement shrinks the wage base: the US room falls by more than two-thirds by year 6; "
      "Sweden's, already near the top, runs out and its build-out stalls at least a point of employment short of the levy's",
      tx["US"]["financing_room_end_pct_gdp"] < tx["US"]["financing_room_start_pct_gdp"] / 3 and tx["SE"]["financing_room_end_pct_gdp"] <= 0
      and lv["SE"]["care_share_end"] - tx["SE"]["care_share_end"] >= 1,
      f"US room {tx['US']['financing_room_start_pct_gdp']} -> {tx['US']['financing_room_end_pct_gdp']}; Sweden {tx['SE']['financing_room_start_pct_gdp']} -> "
      f"{tx['SE']['financing_room_end_pct_gdp']}; Swedish care {tx['SE']['care_share_end']}% against {lv['SE']['care_share_end']}% with the levy")
check("K4 a levy on AI income gains room as displacement grows, and in the US, the euro area and Sweden it never binds: the same "
      "jobs as borrowing, with no debt",
      all(lv[r]["financing_room_end_pct_gdp"] > lv[r]["financing_room_start_pct_gdp"] for r in ("US", "EA", "SE"))
      and all(abs(NW(lv, r) - NW(bo, r)) < 0.05 for r in ("US", "EA", "SE"))
      and all(lv[r]["debt_added_end_pct_gdp"] == 0 for r in gc.R),
      {r: (lv[r]["financing_room_start_pct_gdp"], lv[r]["financing_room_end_pct_gdp"], NW(lv, r), NW(bo, r)) for r in ("US", "EA", "SE")})
check("K5 taxing workers to pay for it costs jobs: financed by labour taxes, US year-6 non-employment is at least 2 points above the "
      "levy's, and Sweden's at least 1",
      NW(tx) - NW(lv) >= 2 and NW(tx, "SE") - NW(lv, "SE") >= 1, {r: (NW(tx, r), NW(lv, r)) for r in gc.R})
check("K6 the price of debt does not bind at a build-out's size: under 5 bp in every region, the euro area included, with at most "
      "5% of GDP added over six years",
      all(bo[r]["debt_premium_max_bp"] < 5 and bo[r]["debt_added_end_pct_gdp"] <= 5 for r in gc.R),
      {r: (bo[r]["debt_premium_max_bp"], bo[r]["debt_added_end_pct_gdp"]) for r in gc.R})
slow = fl("care financed by borrowing", row3, fast=False)
check("K7 with a point a year the pace binds before any financing limit (borrowing without a cap within half a point of the capped "
      "build-out); with three points a year, financing decides: the levy and borrowing hold US non-employment's rise under 25 "
      "points, taxes on labour do not",
      abs(NW(slow) - NW(build_)) < 0.5 and NW(lv) < 25 and NW(bo) < 25 and NW(tx) > 25,
      f"a point a year +{NW(slow)} (capped +{NW(build_)}); three: levy +{NW(lv)}, borrowing +{NW(bo)}, labour taxes +{NW(tx)}")

n_ok = sum(ok for _, ok, _ in RESULTS)
print(f"\n{n_ok}/{len(RESULTS)} checks passed")
sys.exit(0 if n_ok == len(RESULTS) else 1)
