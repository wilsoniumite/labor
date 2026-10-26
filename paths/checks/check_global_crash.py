# check_global_crash.py — the crash model (code/global_crash.py: four economies, the euro area as France and the rest of
# the union since 2026-10-27): the mechanics are what they say, the
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
check("V3 the stated bias: unemployment recovers from 2009 faster than the US's did (end-2010 more than a point below the data) "
      "while the output gap does not (end-2010 within a point) — optimistic about how long joblessness lasts. Restated after the "
      "sign fix of 2026-10-26: before it, the gap recovered too fast as well (end-2010 -1.27 against -4.2)",
      m2["unemployment"][-1] < t2["unemployment"][-1] - 1.0 and abs(m2["gap_change"][-1] - t2["gap_change"][-1]) < 1.0,
      f"end-2010 unemployment {m2['unemployment'][-1]} against {t2['unemployment'][-1]}; gap {m2['gap_change'][-1]} against {t2['gap_change'][-1]}")

r00, t00 = gc.run_2000(cm, fp["okun_us"]), gc.targets_2000()
eu00 = r00["u"][1:16] - np.array(t00["unemployment"])
check("V4 out of sample, the dot-com bust (2000-03, today's rules, measured equity, all equipment and exports; not in the "
      "fit): the unemployment peak and the output trough within 1.5 points of the data, as V2 asks of 2008-10, and "
      "quarterly unemployment's RMS error under 0.75. Stated as found on 2026-10-26: RMS 0.66 (0.94 on the fit before the "
      "sign fix), the gap's 1.11 (0.74 before). The timing misses: the model's unemployment peaks in 2001Q3, seven "
      "quarters before the data's (2003Q2), and it recovers after 2001 faster than the US did, as V3 says of 2009",
      abs(r00["u"].max() - max(t00["unemployment"])) < 1.5 and abs(r00["y"].min() - min(t00["gap_change"])) < 1.5
      and float(np.sqrt(np.mean(eu00 ** 2))) < 0.75,
      f"peak {r00['u'].max():.2f} (k={int(np.argmax(r00['u']))}) against {max(t00['unemployment'])} (k={1 + int(np.argmax(t00['unemployment']))}); "
      f"trough {r00['y'].min():.2f} against {min(t00['gap_change'])}; RMS unemployment {np.sqrt(np.mean(eu00 ** 2)):.2f}; "
      f"2003Q4 {r00['u'][15]:.2f} against {t00['unemployment'][-1]}")

print("B — the 2000-02 bust, measured")
import pandas as pd  # noqa: E402
qd = lambda sid, end=False: (lambda x: x.groupby(x.index.to_period("Q")).last() if end else x.groupby(x.index.to_period("Q")).mean())(gc.fred(sid))  # noqa: E731
qs = [pd.Period("2000Q1", "Q") + k for k in range(24)]
z = qd("BOGZ1LM153064475Q", True)
eqm = np.array([max(0.0, 1 - z[q] / z[qs[0]]) for q in qs])
g = qd("GDP")
net = (qd("Y034RC1Q027SBEA") + qd("B985RC1Q027SBEA") + qd("W003RC1Q027SBEA") - qd("B852RC1Q027SBEA")) / g * 100
yr = net.dropna().groupby(net.dropna().index.year).mean().loc[1990:1994]
sl, ic = np.polyfit(yr.index.values.astype(float), yr.values, 1)
gp = np.array([net[q] - (sl * (q.year + (q.quarter - 1) / 4 + 0.125) + ic) for q in qs])
ci = qd("CORBLACBS")
base = ci[(ci.index >= pd.Period("1997Q1", "Q")) & (ci.index <= pd.Period("1999Q4", "Q"))].mean()
ex = np.array([max(0.0, ci[q] - base) for q in qs])
b2 = gc.bust_2000()
hist = json.load(open(os.path.join(ROOT, "cache", "HISTORY_SOURCES.json"), encoding="utf-8"))
import hashlib  # noqa: E402
hashes = all(hashlib.sha256(open(os.path.join(ROOT, "cache", f"{sid}.csv"), encoding="utf-8").read().encode()).hexdigest() == v["sha256"]
             for sid, v in hist.items())
check("B1 the 2000-02 bust's three legs, recomputed here from the cached files (Z.1 household equity; BEA's information "
      "processing equipment, software and power structures less computer imports, over GDP, against their 1990-94 trend; "
      "the Fed Board's C&I charge-offs over their 1997-99 mean), equal bust_2000's; the history files written from the "
      "publishers carry the hashes their record names (cache/HISTORY_SOURCES.json); household equity -44.7% at the trough "
      "ten quarters after the peak, the build-out's excess 76% lost at most, the losses peaking ten quarters after",
      np.allclose(eqm, b2["measured"]["equity_fall"], atol=1e-12) and np.allclose(1 - gp / gp[0], b2["measured"]["capex_share_lost"], atol=1e-12)
      and np.allclose(ex / ex.sum(), b2["losses"], atol=1e-12) and hashes
      and round(eqm.max(), 3) == 0.447 and int(np.argmax(eqm)) == 10 and round((1 - gp / gp[0]).max(), 3) == 0.762
      and int(np.argmax(ex)) == 10,
      f"equity trough {eqm.max():.3f} at k={int(np.argmax(eqm))}; build-out lost at most {(1 - gp / gp[0]).max():.3f}; losses peak k={int(np.argmax(ex))}")

print("S — the measured shocks enter with the sign of their own change (a fall is a drag)")
d07 = gc.demand_2007()
res = gc.fred("PRFI") / gc.fred("GDP").reindex(gc.fred("PRFI").index) * 100
dres = res.loc["2007-10-01":].values[:13] - float(res.loc["2007-10-01"])
xq = gc.fred("EXPGSC1")
dex = ((xq - xq.loc["2007-10-01"]) / gc.fred("GDPC1").loc["2007-10-01"] * 100).loc["2007-10-01":].values[:13]
check("S1 2008-10: housebuilding enters as residential investment's change in share of GDP (it fell, so a drag every quarter), exports "
      "as their own change, housing wealth as a fall; each with the sign of the measured change, quarter by quarter",
      np.array_equal(np.sign(d07["housebuilding"]), np.sign(dres)) and (d07["housebuilding"][1:] < 0).all()
      and np.array_equal(np.sign(d07["exports"]), np.sign(dex)) and (d07["housing wealth"] <= 0).all(),
      {k: [round(float(x), 2) for x in v[[1, 4, 8, 12]]] for k, v in d07.items()})
full, nob, noh = (gc.run_2007(cm, fp["okun_us"], drop=dr) for dr in ((), ("housebuilding",), ("housing wealth",)))
check("S2 and in the run: leaving out the housebuilding collapse or the fall in housing wealth makes 2008-10 milder (a higher trough)",
      nob["y"].min() > full["y"].min() and noh["y"].min() > full["y"].min(),
      f"trough {full['y'].min():.2f}; without housebuilding {nob['y'].min():.2f}; without housing wealth {noh['y'].min():.2f}")

print("M — the mechanics")
n = 16
calm = {r: replace(g, eta=0.0, drift=0.0, pi0=2.0, i0=cm.r_star + 2.0, sov0=g.sov_calm) for r, g in regs.items()}
o = gc.simulate(calm, {r: gc.MODERN for r in gc.R}, gc.Shock(), cm, n)
check("M1 no shock, no drift, policy at neutral and inflation on target: every region stays at capacity",
      all(np.abs(o[r]["y"]).max() < 1e-9 and np.ptp(o[r]["u"]) < 1e-9 for r in gc.R))
us_only = gc.Shock(demand={"US": gc.ramp(-5.0, 1, 2, n)})
o = gc.simulate(calm, {r: gc.MODERN for r in gc.R}, us_only, cm, n)
check("M2 trade carries a US slump abroad: every other region's gap falls, Sweden's (exports half of GDP) the most",
      all(o[r]["y"].min() < -0.05 for r in ("EA", "FR", "SE", "CN"))
      and o["SE"]["y"].min() < min(o["EA"]["y"].min(), o["FR"]["y"].min(), o["CN"]["y"].min()),
      {r: round(float(o[r]["y"].min()), 2) for r in gc.R})
o = gc.simulate(regs, {r: gc.MODERN for r in gc.R}, gc.ai_shock(24), cm, 24)
outside = {r: (regs[r].sov_pass * (o[r]["sov"] - regs[r].sov_calm) if regs[r].sov_debt > 0 else o[r]["premium"]) for r in gc.R}
check("M3 under the backstop, the banks' part of spreads stays under each region's cap (the price of debt and France's "
      "sovereign spread are added outside it), and capital above the recapitalisation floor",
      all((o[r]["s"] - outside[r]).max() <= regs[r].spread_cap + 1e-9
          and o[r]["k"].min() >= gc.MODERN.capital_floor * regs[r].bank_capital - 1e-9 for r in gc.R))
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
check("F1 today's rules, the bust alone (dot-com size): a world recession, smaller than 2008's — the four together 2-4% below "
      "capacity, the US 3% or more, about 2001's depth. Restated after the sign fix of 2026-10-26: before it, about 2008's size "
      "(the four -5.9%, the US -7.58%)",
      -4.0 < bo["four_weighted_gap_min"] <= -2.0 and bo["US"]["gap_min"] <= -3.0, f"four together {bo['four_weighted_gap_min']}%; US {bo['US']['gap_min']}%")
lab = y4("modern rules | bust + displacement, recessions trigger adoption x3")
check("F2 today's rules with displacement and recessions triggering adoption: a jobs crisis without an output one — US "
      "non-employment up 10 points or more while output stays within 10% of capacity; measured unemployment shows under half of "
      "it. Restated after the sign fix of 2026-10-26: before it, +21.03 with the gap at -11.08% (20 points, within 15%)",
      NW(lab) >= 10 and lab["US"]["gap_min"] > -10 and lab["US"]["unemployment_max"] - regs["US"].u0 < NW(lab) / 2,
      f"US non-employment +{NW(lab)} (unemployment {lab['US']['unemployment_max']}%, {lab['US']['out_of_labour_force_end']} points out of the labour force), gap {lab['US']['gap_min']}%")
er = y4("rules erode under pressure | bust + displacement")
check("F3 when the rules erode (austerity, no backstop, tariffs, looser anchoring): a deep world recession, about twice "
      "2008's — the four together 8% or more below capacity, US non-employment up 12 points or more, most of US banks' "
      "capital gone. Restated 2026-10-26 after the bust moved to the 2000-02 bust's measured path and the start to the dated vintage (Log 42): before it -10.59%, +16.32, 0.874; before the sign fix, Great Depression scale (-24.66%, "
      "+34.36, all capital)",
      er["four_weighted_gap_min"] <= -8.0 and NW(er) >= 12 and er["US"]["bank_capital_lost_max"] >= 0.6,
      f"four together {er['four_weighted_gap_min']}%, US non-employment +{NW(er)}, capital lost {er['US']['bank_capital_lost_max']}")
ex = y4("rules expand under pressure | bust + displacement")
check("F4 when the rules expand (an income guarantee): output held within 5% everywhere, at no more than 3% of US GDP a year — "
      "but US non-employment still up more than 7 points: the guarantee holds demand, not jobs. Restated 2026-10-26 after the bust moved to the 2000-02 bust's measured path and the start to the dated vintage (Log 42): before it "
      "within 6%, 2.74% of GDP, +8.71; before the sign fix within 10%, 3.67%, +11.6",
      all(ex[r]["gap_min"] > -5 for r in gc.R) and ex["US"]["guarantee_cost_max_pct_gdp"] <= 3 and NW(ex) > 7,
      f"gaps {[ex[r]['gap_min'] for r in gc.R]}; US guarantee {ex['US']['guarantee_cost_max_pct_gdp']}% of GDP; US non-employment +{NW(ex)}")
th = y4("the 1930s' rules | bust + displacement")
check("F5 the 1930s' rules on today's economy are worse still than eroded rules", th["four_weighted_gap_min"] < er["four_weighted_gap_min"],
      f"{th['four_weighted_gap_min']} against {er['four_weighted_gap_min']}")
md = y4("modern rules | bust + displacement")
check("F6 the US leads: the largest rise in non-employment of the four under today's rules",
      max(gc.R, key=lambda r: NW(md, r)) == "US", {r: NW(md, r) for r in gc.R})

print("X — the participation margin and the measured build-out (decoupling.py), stated as found")
dec = json.load(open(os.path.join(ROOT, "results", "decoupling.json"), encoding="utf-8"))
check("X1 the inputs are the measured ones: the US build-out net of computer imports above its 2015-22 trend (floored at zero: "
      "it sits below its trend, -0.42 points, since decoupling.py reads information processing equipment, not all "
      "equipment; Log 42), and the US exit share since the prime-age employment peak; the other regions keep the "
      "displaced in the labour force (not measured)",
      abs(regs["US"].ai_capex - max(dec["ai_build_out"]["net_above_2015_22_trend_pts"], 0.0)) < 1e-9
      and abs(regs["US"].exit_share - dec["where_the_displaced_go"]["prime_age_25_54"]["since_the_employment_peak"]["exit_share"]) < 1e-9
      and all(regs[r].exit_share == 0 for r in ("EA", "FR", "SE", "CN")),
      f"US build-out {regs['US'].ai_capex}% of GDP (measured {dec['ai_build_out']['net_above_2015_22_trend_pts']}; assumed 1.5 before), "
      f"exit share {regs['US'].exit_share}")
old_us = {r: (replace(g, ai_capex=1.5, drift=0.0) if r == "US" else replace(g, drift=0.0)) for r, g in regs.items()}
new_us = {r: replace(g, drift=0.0) for r, g in regs.items()}
a = gc.summary(gc.simulate(old_us, {r: gc.MODERN for r in gc.R}, gc.ai_shock(24), cm, 24), regs, 16)
b = gc.summary(gc.simulate(new_us, {r: gc.MODERN for r in gc.R}, gc.ai_shock(24), cm, 24), regs, 16)
nof = {r: replace(gc.MODERN, fiscal="none") for r in gc.R}
a0 = gc.summary(gc.simulate(old_us, nof, gc.ai_shock(24), cm, 24), regs, 16)
b0 = gc.summary(gc.simulate(new_us, nof, gc.ai_shock(24), cm, 24), regs, 16)
check("X2 measured, the US build-out has nothing above its trend, so the bust's capex leg is zero in the US. Had it been "
      "the 1.5% of GDP assumed before, the bust would cut deeper: by over a point at year 4 without discretionary fiscal "
      "policy, and by less with today's triggers, since the faster rise in unemployment fires the stimulus earlier. "
      "Restated 2026-10-26 after the bust moved to the 2000-02 bust's measured sizes, dated from the peak (Log 44): before it the gate read the year-4 trough with the triggers on (-3.09 against -3.24), which the "
      "trigger's timing confounds (the review of 2026-10-26)",
      regs["US"].ai_capex == 0.0 and a0["US"]["gap_min"] <= b0["US"]["gap_min"] - 1.0 and a["US"]["gap_min"] < b["US"]["gap_min"],
      f"US gap, no fiscal response: {a0['US']['gap_min']} assumed -> {b0['US']['gap_min']} measured; with the triggers "
      f"{a['US']['gap_min']} -> {b['US']['gap_min']}")
dep6 = S["modern rules | bust + displacement, recessions trigger adoption x3 | two waves, robotics in 2 years"]["year6"]["US"]
check("X3 exits hide a jobs depression from the unemployment rate: by year 6 (robotics two years out) US unemployment reads under "
      "15% while more points have left the labour force than unemployment has risen. Restated after the sign fix of 2026-10-26: "
      "before it, under 20% with more than 20 points out (19.71%, 22.96)",
      dep6["unemployment_max"] < 15 and dep6["out_of_labour_force_end"] > dep6["unemployment_max"] - regs["US"].u0,
      f"unemployment {dep6['unemployment_max']}%, out of the labour force {dep6['out_of_labour_force_end']}, non-employment +{dep6['not_working_rise_max']}")
nb = lambda rn, h: S[f"{rn} | displacement without a bust"][h]["US"]  # noqa: E731
check("X4 displacement without a bust (where the US is): fiscal triggers keyed to unemployment fire late — by year 4 output is "
      "1.5 points or more further below capacity than with triggers keyed to non-employment; by year 6 the order flips (the "
      "earlier stimulus has run out), and every rule set stays within 5%. Restated after the sign fix of 2026-10-26: before it, "
      "both triggers near -7% by year 6 and the guarantee within 4% (-6.69, -7.26, -3.65)",
      nb("modern rules", "year4")["gap_min"] <= nb("modern rules, triggers on non-employment", "year4")["gap_min"] - 1.5
      and nb("modern rules, triggers on non-employment", "year6")["gap_min"] < nb("modern rules", "year6")["gap_min"]
      and all(nb(k, "year6")["gap_min"] > -5 for k in ("modern rules", "modern rules, triggers on non-employment", "rules expand under pressure")),
      {k: (nb(k, "year4")["gap_min"], nb(k, "year6")["gap_min"]) for k in ("modern rules", "modern rules, triggers on non-employment", "rules expand under pressure")})
t0 = S["modern rules | bust + displacement, recessions trigger adoption x3"]["year6"]
t1 = S["modern rules, triggers on non-employment | bust + displacement, recessions trigger adoption x3"]["year6"]
check("X5 in a bust the cyclical rise in unemployment fires the triggers either way: keying them to non-employment moves no "
      "region's worst output by half a point. Restated after the sign fix of 2026-10-26: before it, it changed nothing (to 1e-9)",
      all(abs(t0[r]["gap_min"] - t1[r]["gap_min"]) < 0.5 for r in gc.R), {r: (t0[r]["gap_min"], t1[r]["gap_min"]) for r in gc.R})

print("W — two waves (cognitive now, physical once robotics arrives), stated as found")
row = "modern rules | bust + displacement, recessions trigger adoption x3"
wv = lambda L, h="year4": S[f"{row} | two waves, robotics in {L} years"][h]  # noqa: E731
u4 = [NW(lab)] + [NW(wv(L)) for L in (1, 2, 3)]
check("W1 the robotics lag holds the jobs crisis back: US year-4 non-employment falls with every year of lag, and with robotics "
      "three years out it is at least 2.5 points below the uniform case. Restated 2026-10-26 after the bust moved to the 2000-02 bust's measured path and the start to the dated vintage (Log 42): before it at least 3.5 (13.2 -> "
      "9.26); before the sign fix at least 5 (21.03 -> 14.71)",
      all(a_ >= b_ for a_, b_ in zip(u4, u4[1:])) and u4[0] - u4[3] >= 2.5, f"uniform, 1, 2, 3 years: {u4}")
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
check("C5 a funded build-out, a point of employment a year: in the labour-depression row, US year-6 non-employment at least 4 "
      "points lower, at no more than 1% of GDP a year; US care short of the ceiling by year 6 (the pace binds; C6). "
      "Restated 2026-10-26 after the bust moved to the 2000-02 bust's measured path and the start to the dated vintage (Log 42): before it at least 5 points lower with care within 0.1 of the ceiling (+24.44 -> +18.08, 20.02%)",
      NW(none_) - NW(build_) >= 4 and build_["US"]["care_cost_max_pct_gdp"] <= 1.0 and build_["US"]["care_share_end"] < cm.care_ceiling - 0.5,
      f"+{NW(none_)} -> +{NW(build_)}; cost {build_['US']['care_cost_max_pct_gdp']}% of GDP; care {build_['US']['care_share_end']}%")
fast_, open_ = y6("rules expand into care", row3, ", care absorbs, three points a year"), y6("rules expand into care", row3, ", care absorbs, three points a year, no ceiling")
check("C6 in the US both the pace and the ceiling bind: three points a year gains over a point by year 6, and without the "
      "ceiling it gains over a point more. Restated 2026-10-26 after the bust moved to the 2000-02 bust's measured sizes, dated from the peak (Log 44): before it the pace bound and the ceiling barely did (a point a "
      "year +12.21, three +10.64, three without the ceiling +8.79); before Log 42 the ceiling was the limit, not the pace",
      NW(build_) - NW(fast_) > 1 and NW(fast_) - NW(open_) > 1,
      f"a point a year +{NW(build_)}, three +{NW(fast_)}, three without the ceiling +{NW(open_)} (care {open_['US']['care_share_end']}%)")
struct = build_["US"]["displaced_cognitive_end"] + build_["US"]["displaced_physical_end"]
room = cm.care_ceiling - regs["US"].care_share
check("C7 care cannot rescue the jobs crisis: the US displaced still out of work at year 6 exceed the room care had (Norway's "
      "share less today's), and US non-employment stays up more than 8 points even without a ceiling. Restated 2026-10-26 after the bust moved to the 2000-02 bust's measured path and the start to the dated vintage (Log 42): "
      "before it about twice the room and more than 12 points (10.4 against 5.3; +13.65)",
      struct >= room and NW(open_) > 8, f"still displaced {struct:.1f} points against room {room:.1f}; without a ceiling +{NW(open_)}")
se1, se0 = y6("rules expand into care", row1, ", care absorbs")["SE"], y6("modern rules", row1, "")["SE"]
check("C8 Sweden, displacement alone: the build-out takes year-6 unemployment down at least 2 points and care stays under the "
      "ceiling — there the gate and the pace of training bind, not the ceiling. Restated 2026-10-26 after the bust moved to the 2000-02 bust's measured path and the start to the dated vintage (Log 42): before it at least 2.5",
      se0["unemployment_max"] - se1["unemployment_max"] >= 2.0 and se1["care_share_end"] < cm.care_ceiling - 1,
      f"{se0['unemployment_max']} -> {se1['unemployment_max']}; care {se1['care_share_end']}%")
g_ = y6("rules expand under pressure", row3, "")
per_c = (NW(none_) - NW(build_)) / build_["US"]["care_cost_max_pct_gdp"]
per_g = (NW(none_) - NW(g_)) / g_["US"]["guarantee_cost_max_pct_gdp"]
check("C9 care buys jobs, the guarantee buys demand: per point of GDP a year, the build-out takes more off US non-employment than "
      "the income guarantee, and the guarantee holds output closer to capacity. Restated 2026-10-26 after the bust moved to the 2000-02 bust's measured path and the start to the dated vintage (Log 42): before it over 4 points "
      "closer (-9.1 against -4.44)",
      per_c > per_g and g_["US"]["gap_min"] > build_["US"]["gap_min"],
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
      "10 points with the build-out either way; Sweden's result moves with it (there it binds). Restated 2026-10-26 after the bust moved to the 2000-02 bust's measured path and the start to the dated vintage (Log 42): before it "
      "more than 15 (19.84, 17.65)",
      all(v[0] > 10 for v in sens.values()) and abs(sens[0.10][2] - sens[0.50][2]) > 1, sens)

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
check("K3 taxes on labour lose room as displacement shrinks the wage base: the US room falls by over a quarter by year 6; "
      "Sweden's, already near the top, by over two-fifths, and its build-out ends level with the levy's. Restated 2026-10-26 after the bust moved to the 2000-02 bust's measured path and the start to the dated vintage (Log 42): "
      "before it the US room fell by over two-fifths (11.58 -> 6.32) and Sweden's to under a point (0.75)",
      tx["US"]["financing_room_end_pct_gdp"] < tx["US"]["financing_room_start_pct_gdp"] * 0.75
      and tx["SE"]["financing_room_end_pct_gdp"] < tx["SE"]["financing_room_start_pct_gdp"] * 0.6
      and abs(lv["SE"]["care_share_end"] - tx["SE"]["care_share_end"]) < 0.2,
      f"US room {tx['US']['financing_room_start_pct_gdp']} -> {tx['US']['financing_room_end_pct_gdp']}; Sweden {tx['SE']['financing_room_start_pct_gdp']} -> "
      f"{tx['SE']['financing_room_end_pct_gdp']}; Swedish care {tx['SE']['care_share_end']}% against {lv['SE']['care_share_end']}% with the levy")
check("K4 a levy on AI income gains room as displacement grows, and in the US, the euro area and Sweden it never binds: the same "
      "jobs as borrowing, with no debt for the build-out (France's debt carries its banks' recapitalisation as well, "
      "decision 70: the levy adds none to it)",
      all(lv[r]["financing_room_end_pct_gdp"] > lv[r]["financing_room_start_pct_gdp"] for r in ("US", "EA", "SE"))
      and all(abs(NW(lv, r) - NW(bo, r)) < 0.05 for r in ("US", "EA", "SE"))
      and all(lv[r]["debt_added_end_pct_gdp"] == 0 for r in gc.R if regs[r].sov_debt == 0)
      and lv["FR"]["debt_added_end_pct_gdp"] <= bo["FR"]["debt_added_end_pct_gdp"],
      {r: (lv[r]["financing_room_start_pct_gdp"], lv[r]["financing_room_end_pct_gdp"], NW(lv, r), NW(bo, r)) for r in ("US", "EA", "SE")})
check("K5 taxing workers to pay for it costs jobs: financed by labour taxes, US year-6 non-employment is at least a point above "
      "the levy's, and Sweden's at least 0.2. Restated 2026-10-26 after the bust moved to the 2000-02 bust's measured path and the start to the dated vintage (Log 42): before it at least 1.5 and 0.3 (15.33 against 13.65; 4.71 "
      "against 4.37)",
      NW(tx) - NW(lv) >= 1.0 and NW(tx, "SE") - NW(lv, "SE") >= 0.2, {r: (NW(tx, r), NW(lv, r)) for r in gc.R})
check("K6 the price of debt does not bind at a build-out's size: under 5 bp in every region, the euro area included, with at most "
      "5% of GDP added over six years",
      all(bo[r]["debt_premium_max_bp"] < 5 and bo[r]["debt_added_end_pct_gdp"] <= 5 for r in gc.R),
      {r: (bo[r]["debt_premium_max_bp"], bo[r]["debt_added_end_pct_gdp"]) for r in gc.R})
slow = fl("care financed by borrowing", row3, fast=False)
check("K7 with a point a year the pace binds before any financing limit (borrowing without a cap within half a point of the capped "
      "build-out); with three points a year, financing decides: taxes on labour leave US non-employment's rise at least a "
      "point above the levy's and borrowing's. Restated 2026-10-26 after the bust moved to the 2000-02 bust's measured path and the start to the dated vintage (Log 42): before it at least 1.5 (15.33 against 13.65)",
      abs(NW(slow) - NW(build_)) < 0.5 and NW(tx) - max(NW(lv), NW(bo)) >= 1.0,
      f"a point a year +{NW(slow)} (capped +{NW(build_)}); three: levy +{NW(lv)}, borrowing +{NW(bo)}, labour taxes +{NW(tx)}")

print("E — the euro area in two: France and the rest of the union (decision 70)")
import vintage  # noqa: E402
import pandas as pd  # noqa: E402
end = pd.Period(gc.START, "Q").end_time
at = lambda sid: vintage.read(sid).loc[:end]  # noqa: E731
fu, eu, fn, en = (at(x) for x in ("FR_UNEMPLOYMENT", "EA21_UNEMPLOYMENT", "FR_UNEMPLOYED", "EA21_UNEMPLOYED"))
lf_fr, lf_ea = fn.iloc[-1] / fu.iloc[-1], en.iloc[-1] / eu.iloc[-1]
merged_u = (regs["EA"].u0 * (lf_ea - lf_fr) + regs["FR"].u0 * lf_fr) / lf_ea
w_fr = float(at("FR_HICP_WEIGHT").iloc[-1]) / 1000
merged_pi = (1 - w_fr) * regs["EA"].pi0 + w_fr * regs["FR"].pi0
spr = (at("FRGVB10Y") - at("DEGVB10Y")).dropna()
check("E1 the start measured: the two halves' unemployment recombine, on Eurostat's labour forces, into the euro area's; "
      "their core inflation, at France's HICP weight, into the euro area's; their sizes into the euro area's quarter, split "
      "by GDP; France's spread over Germany at 30 Sep against its mean from July 2025 to June 2026; its debt (Eurostat) "
      "and its banks' holdings of euro-area government debt (the ECB) over GDP",
      abs(merged_u - float(eu.iloc[-1])) < 1e-9 and abs(merged_pi - vintage.yoy(at("00XEFDEZ19M086NEST"))) < 1e-9
      and abs(regs["EA"].size + regs["FR"].size - 0.25) < 1e-3 and regs["EA"].union == regs["FR"].union == "EA"
      and abs(regs["FR"].sov0 - float(spr.iloc[-1])) < 1e-12 and f"{spr.index[-1]:%Y-%m-%d}" == "2026-09-30"
      and regs["FR"].sov0 > regs["FR"].sov_calm and regs["FR"].sov_debt > 100 and 10 < regs["FR"].sov_banks < 20,
      f"u: France {regs['FR'].u0}, the rest {regs['EA'].u0:.2f} -> {merged_u:.2f} (the euro area {float(eu.iloc[-1])}); "
      f"core: France {regs['FR'].pi0:.2f}, the rest {regs['EA'].pi0:.2f}; sizes {regs['FR'].size} + {regs['EA'].size}; "
      f"France's spread {regs['FR'].sov0:.2f} (calm {regs['FR'].sov_calm:.2f}), debt {regs['FR'].sov_debt}% of GDP, "
      f"its banks' holdings {regs['FR'].sov_banks:.1f}%")
# two identical halves in a union, trading with the world as the whole did, reproduce the one region exactly
whole = {r: g for r, g in regs.items() if r != "FR"}
whole["EA"] = replace(whole["EA"], size=0.25, union="", trade={q: v for q, v in regs["EA"].trade.items() if q != "FR"})
whole = {r: (replace(g, trade={**{q: v for q, v in g.trade.items() if q != "FR"}, "EA": g.trade.get("EA", 0) + g.trade.get("FR", 0)})
             if r != "EA" else g) for r, g in whole.items()}
tw = sum(whole["EA"].trade.values())
whole["EA"] = replace(whole["EA"], trade={q: v / tw for q, v in whole["EA"].trade.items()})
mutual = 0.3                                       # each half sends 30% of its exports to the other, tariff-free
half_trade = lambda other: {**{q: v * (1 - mutual) for q, v in whole["EA"].trade.items()}, other: mutual}  # noqa: E731
halves = {**{r: replace(g, trade={**{q: v for q, v in g.trade.items() if q != "EA"}, "EA": g.trade["EA"] / 2, "FR": g.trade["EA"] / 2})
             for r, g in whole.items() if r != "EA"},
          "EA": replace(whole["EA"], size=0.125, union="EA", exports=whole["EA"].exports / (1 - mutual), trade=half_trade("FR")),
          "FR": replace(whole["EA"], name="FR", size=0.125, union="EA", exports=whole["EA"].exports / (1 - mutual), trade=half_trade("EA"))}
wr = {r: gc.MODERN for r in whole}
a_ = gc.simulate(whole, wr, gc.ai_shock(24), cm, 24)
b_ = gc.simulate(halves, {r: gc.MODERN for r in halves}, gc.ai_shock(24), cm, 24)
d = max(float(np.abs(a_[r][k] - b_[q][k]).max()) for r, q in (("US", "US"), ("SE", "SE"), ("CN", "CN"), ("EA", "EA"), ("EA", "FR"))
        for k in ("y", "u", "i", "k", "s"))
apart = gc.simulate(halves, {r: gc.MODERN for r in halves}, gc.Shock(demand={"FR": gc.ramp(-3.0, 1, 2, 24)}), cm, 24)
check("E2 the split nests the one euro area: two identical halves in a union, each half the size and trading with each "
      "other tariff-free, reproduce the single region and every other region's path exactly (a union partner's slump "
      "reaches a member only as far as it differs from its own); a shock to one half alone spills over to the other",
      d < 1e-9 and apart["EA"]["y"].min() < -0.01, f"largest difference {d:.1e}; a French-only shock moves the rest "
      f"{apart['EA']['y'].min():.2f} (France {apart['FR']['y'].min():.2f})")
o = gc.simulate(regs, {r: gc.MODERN for r in gc.R}, gc.ai_shock(24), cm, 24)
oe = gc.simulate(regs, {r: gc.ERODED for r in gc.R}, gc.ai_shock(24), cm, 24)
check("E3 one policy rate: in the union the rest of the euro area and France have the same rate every quarter, under "
      "today's rules and eroding ones",
      np.allclose(o["EA"]["i"], o["FR"]["i"], atol=0) and np.allclose(oe["EA"]["i"], oe["FR"]["i"], atol=0))
# the doom loop: extra French bank losses, with and without the two links (the recapitalisation's debt, the holdings)
hit = gc.ai_shock(24)
hit.losses["FR"] = hit.losses["FR"] + gc.pulse(4.0, 2, 4, 24)
loop = gc.simulate(regs, {r: gc.MODERN for r in gc.R}, hit, cm, 24)
cut = gc.simulate({**regs, "FR": replace(regs["FR"], sov_banks=0.0, debt_slope=0.0, debt_slope_crisis=0.0)},
                  {r: gc.MODERN for r in gc.R}, hit, cm, 24)
rise_loop = float(loop["FR"]["sov"].max() - regs["FR"].sov0)
check("E4 the doom loop, at the measured price of debt: with French banks losing 4% of their loans more, the state's "
      "recapitalisation raises France's spread and French output falls further than without the loop; stated as found "
      "(the loop is weak at these sizes: what moves France's spread is a premium, not its banks)",
      rise_loop > 0 and loop["FR"]["y"].min() < cut["FR"]["y"].min() and rise_loop < 0.5,
      f"France's spread +{rise_loop:.3f} at most; French output {loop['FR']['y'].min():.2f} against {cut['FR']['y'].min():.2f} "
      f"without the loop; capital lost {loop['FR']['stress'].max():.2f}")
prem = gc.ai_shock(24)
prem.spread = {"FR": np.minimum(np.arange(24) / 4, 1.0) * 2.0}
free = gc.simulate(regs, {r: gc.MODERN for r in gc.R}, prem, cm, 24)
capped = gc.simulate(regs, {r: (replace(gc.MODERN, tpi=0.5) if r == "FR" else gc.MODERN) for r in gc.R}, prem, cm, 24)
nw = lambda o_, r: float((o_[r]["u"] + o_[r]["out"]).max())  # noqa: E731
check("E5 the ECB's backstop for France (TPI): capped half a point above its start, France's spread never passes the cap, "
      "and with a two-point premium France's output falls less and fewer are out of work than uncapped",
      capped["FR"]["sov"].max() <= regs["FR"].sov0 + 0.5 + 1e-12 and free["FR"]["sov"].max() > regs["FR"].sov0 + 1.9
      and capped["FR"]["y"].min() > free["FR"]["y"].min() and nw(capped, "FR") < nw(free, "FR"),
      f"spread {free['FR']['sov'].max():.2f} uncapped, {capped['FR']['sov'].max():.2f} capped; French output "
      f"{free['FR']['y'].min():.2f} -> {capped['FR']['y'].min():.2f}; out of work {nw(free, 'FR'):.2f} -> {nw(capped, 'FR'):.2f}")
check("E6 France's spread already present at the start reaches its borrowers: the private spread at index 0 is half of "
      "its excess over the calm level, and nowhere else in the union",
      abs(o["FR"]["s"][0] - regs["FR"].sov_pass * (regs["FR"].sov0 - regs["FR"].sov_calm)) < 1e-12 and o["EA"]["s"][0] == 0,
      f"France {o['FR']['s'][0]:.3f}, the rest {o['EA']['s'][0]}")

n_ok = sum(ok for _, ok, _ in RESULTS)
print(f"\n{n_ok}/{len(RESULTS)} checks passed")
sys.exit(0 if n_ok == len(RESULTS) else 1)
