# check_outlook.py — the case (code/outlook.py): the engine untouched, every input as measured or stated, the stored
# results reproduced, and the case's findings as found.
#
# Run from outlook/:  python checks/check_outlook.py
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
import outlook as ol  # noqa: E402

gc = ol.gc
RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


R = json.load(open(os.path.join(ROOT, "results", "outlook.json"), encoding="utf-8"))
cm, stored_regs = ol.stored()
regs = ol.regions()
C = ol.run(None, regs, cm)
case = R["case"]

print("The engine")
# E1: the case's input to the engine is off unless given: the stored central scenario, bit for bit
G = ol.load("global_crash.json")
dates = {r: None if d is None else d["years"] for r, d in G["preset_dates"]["modern rules"].items()}
n = gc.months(24)
a = gc.simulate(stored_regs, gc.dated(gc.MODERN, dates), gc.ai_shock(n), cm, n, waves=gc.CENTRAL_WAVES)
sh = gc.ai_shock(n)
sh.push = {}
b = gc.simulate(stored_regs, gc.dated(gc.MODERN, dates), sh, cm, n, waves=gc.CENTRAL_WAVES)
same = all(np.array_equal(a[r][k], b[r][k]) for r in gc.R for k in a[r])
key = "modern rules | bust + displacement | two waves, robotics in 2 years, care absorbs"
ref = G["scenarios"][key]["year4"]["US"]
got = gc.summary(a, stored_regs, 16)["US"]
check("E1 with no inflation input the engine is the stored one, bit for bit, and reproduces its stored central run",
      same and abs(got["unemployment_max"] - ref["unemployment_max"]) <= 0.011,
      f"US unemployment's year-4 high {got['unemployment_max']} (stored {ref['unemployment_max']})")
# E2: the input adds to core inflation and to nothing else directly: in the first step inflation is the start's
first = {r: float(C["out"][r]["pi"][1]) for r in ("US", "EA")}
check("E2 where inflation starts above target it starts the run where it was measured",
      all(abs(first[r] - regs[r].pi0) < 0.08 for r in first),
      ", ".join(f"{r} {first[r]:.2f} against {regs[r].pi0:.2f} at the start" for r in first))
check("E3 where it starts at or below target there is no input", sorted(C["shock"].push) == ["EA", "US"],
      f"input for {sorted(C['shock'].push)}; core inflation at the start "
      + ", ".join(f"{r} {regs[r].pi0:.2f}" for r in ("FR", "SE", "CN")))

print("The inputs")
sn = ol.seen()
p = ol.us_pace("central", ol.N)
check("I1 the pace starts at the most the jobs data allow and doubles every two years, up to a point a year",
      abs(p[0] - sn["bound"]) < 1e-12 and abs(p[24] - 2 * sn["bound"]) < 1e-12 and p.max() == ol.CEILING
      and np.all(np.diff(p) >= 0), f"{p[0]:.3f} at the start, {p[24]:.3f} two years on, {p[48]:.3f} four years on; the "
      f"trend itself reads {sn['trend']:.2f}, the endpoints {sn['endpoints']:.2f}")
check("I2 the share of the displaced that leaves the workforce is the middle of its three bases",
      regs["US"].exit_share == sorted(sn["exit_share_by_base"].values())[1] and stored_regs["US"].exit_share == max(sn["exit_share_by_base"].values()),
      f"{regs['US'].exit_share} (the bases: {sorted(sn['exit_share_by_base'].values())}; the stored model used the highest)")
push = R["inputs"]["inflation_in_the_pipeline"]
check("I3 the excess fades at each region's measured pace", 1.5 < push["US"]["half_life_years"] < 2.0 and 0.8 < push["EA"]["half_life_years"] < 1.1,
      f"half-lives: US {push['US']['half_life_years']} years ({push['US']['measured']['peak']} to {push['US']['measured']['low']}), "
      f"euro area outside France {push['EA']['half_life_years']}")
check("I4 the bust is dated from the day of this year's high", abs(ol.delay_of(ol.PEAK) - (-0.7118412046543463)) < 1e-12
      and ol.delay_of("2026-12-10") == 0 and ol.delay_of("2026-10-06", "ramp") == 0,
      f"ai_shock's delay {ol.delay_of(ol.PEAK):.3f} quarters for {ol.PEAK}; 0 for 10 December 2026")
# I5: the levers start the month after the region's unemployment has risen by the trigger, in this run
bare = gc.simulate(C["regions"], gc.dated(gc.MODERN, {r: None for r in gc.R}), C["shock"], cm, C["n"], waves=C["waves"])
k_first = min(k for r in gc.R for k in range(1, C["n"]) if bare[r]["u"][k - 1] - regs[r].u0 >= gc.MODERN.trigger)
d_first = min(d for d in C["dates"].values() if d is not None)
check("I5 the first lever starts the month after unemployment there has risen two points in the run",
      abs(d_first - (k_first - 1) * ol.DT) < 1e-12, f"{case['policy_lever_from']}")

print("The results")
again = ol.build()
check("R1 the stored results are the code's", json.dumps(again, sort_keys=True) == json.dumps(R, sort_keys=True))
u = case["us_unemployment"]
check("R2 US unemployment rises about a point by the end of 2027 and about two by early 2029, then falls back with the response",
      0.8 <= u["2027Q4"] - 4.2 <= 1.3 and 1.7 <= case["us_unemployment_first_high"][1] - 4.2 <= 2.3
      and case["us_unemployment_low_after"][1] < case["us_unemployment_first_high"][1] - 1.0,
      f"{u['2027Q4']}% in 2027Q4, a high of {case['us_unemployment_first_high'][1]}% in {case['us_unemployment_first_high'][0]}, "
      f"{case['us_unemployment_low_after'][1]}% in {case['us_unemployment_low_after'][0]}; the Sahm rule in {case['us_sahm_rule_month']}")
i = case["us_policy_rate"]
check("R3 the Fed raises a little further, then cuts", case["us_policy_rate_high"][1] > regs["US"].i0 + 0.15 and case["us_policy_rate_high"][0] <= "2027Q2"
      and i["2028Q4"] < regs["US"].i0 - 0.8,
      f"a high of {case['us_policy_rate_high'][1]}% in {case['us_policy_rate_high'][0]} from {regs['US'].i0}%, {i['2028Q4']}% in 2028Q4; "
      f"without the inflation input {R['without_the_inflation_input']['us_policy_rate']['2027Q2']}% in 2027Q2")
o = case["us_out_of_work"]
check("R4 the share out of work is still rising at the end, above the first high", case["still_rising_at_the_end"] and o["2032Q2"] > o["2028Q4"] + 1.5,
      f"{o['2028Q4']}% in 2028Q4, {o['2032Q2']}% in 2032Q2 ({case['us_left_the_workforce_2032Q2']} points of it out of the workforce)")
ar = R["around"]
by_pace = [ar[k]["us_out_of_work_2032Q2"] for k in ("no AI job losses", "the pace stays as seen")] + [o["2032Q2"], ar["the pace doubles every year"]["us_out_of_work_2032Q2"]]
by_bust = [ar["funding holds"]["us_out_of_work_2032Q2"], o["2032Q2"], ar["a dot-com-sized bust"]["us_out_of_work_2032Q2"], ar["a severe bust"]["us_out_of_work_2032Q2"]]
check("R5 by 2032 the share out of work rises with the pace and with the bust's size", by_pace == sorted(by_pace) and by_bust == sorted(by_bust),
      f"by pace (none, as seen, the case, doubling yearly) {by_pace}; by bust (none, the case, dot-com, severe) {by_bust}")
check("R6 by 2032 the pace matters more than the bust's size",
      by_pace[-1] - by_pace[1] > by_bust[2] - by_bust[0]
      and abs(ar["a dot-com-sized bust"]["us_out_of_work_2028Q4"] - ar["funding holds"]["us_out_of_work_2028Q4"]) <
      abs(o["2028Q4"] - ar["funding holds"]["us_out_of_work_2028Q4"]) + 1.5, f"spread by pace {by_pace[-1] - by_pace[1]:.2f} points, by bust {by_bust[2] - by_bust[0]:.2f}")
w, e = ar["the worse case"], ar["spending cuts and tariffs"]
check("R7 the case's downturn is a recession and its end a deep one; eroding rules turn it into a labour depression, and with a dot-com-sized bust a depression",
      e["verdict"] in ("labour", "labour-held") and w["verdict"] == "depression" and case["verdict"] == "deep"
      and -4 < case["four_output_worst_in_the_downturn"][1] <= -2 and case["four_output_worst_month"][0] == R["inputs"]["ends"],
      f"the case: {case['four_output_worst_in_the_downturn'][1]}% at worst in the downturn, {case['four_output_worst_month'][1]}% in its last month ({case['verdict']}); cuts and tariffs: {e['verdict']} ({e['us_out_of_work_2032Q2']}% out of work, "
      f"output {e['four_output_worst'][1]}%); with a dot-com-sized bust: {w['verdict']} ({w['us_out_of_work_2032Q2']}%, {w['four_output_worst'][1]}%)")
none = ol.readings(ol.run({"size": 0.0, "pace": "none"}, regs, cm))
check("R8 the engine does not return to where it started on its own: with no bust and no AI job losses unemployment still drifts up",
      0.2 < none["us_unemployment"]["2032Q2"] - 4.2 < 0.8,
      f"US {none['us_unemployment']['2032Q2']}% in 2032Q2 from 4.2% (France {none['regions']['FR']['out_of_work']['2032Q2']}%, Sweden "
      f"{none['regions']['SE']['out_of_work']['2032Q2']}%): a limit, stated")

oow = ol.quarters(C["out"]["US"]["u"]) + ol.quarters(C["out"]["US"]["out"])
hi = ol.q_of(case["us_unemployment_first_high"][0])
check("R9 after the downturn the share out of work never returns to where it started",
      oow[hi:].min() > oow[0] + 0.8, f"its lowest after the first high {oow[hi:].min():.2f}% against {oow[0]:.2f}% at the start")

print("The switches and the inflation setting")
# L1: the engine's presets are bundles of switches, reproduced exactly (their names apart), and so are the two that
# pay for a care build-out another way
pairs = [(k, {"policy": k}, gc.PRESETS[v]) for k, v in ol.POLICIES.items()]
pairs += [("care, taxed on wages", {"policy": "care", "paid": "wages"}, gc.PRESETS["care financed by labour taxes"]),
          ("care, a levy on AI's income", {"policy": "care", "paid": "levy"}, gc.PRESETS["care financed by a levy on AI income"])]
off = []
for name, pick, preset in pairs:
    st = ol.settings_of(pick)
    rules = ol.rules_of(st, regs)
    if any(replace(rl, name=preset.name) != preset for rl in rules.values()) or cm.ai_levy != ol.TODAY["levy"]:
        off.append(name)
check("L1 each of the engine's presets is a bundle of switches, rule for rule", not off,
      f"{len(pairs)} presets" + (f"; not reproduced: {off}" if off else ""))
# L2: one run has one naming: a switch that does not apply is put back, and switches that make a bundle name it
same = [ol.settings_of({"share": 0.6}) == ol.settings_of(), ol.settings_of({"levy": 1.0, "care_pace": 2.0}) == ol.settings_of(),
        ol.settings_of({"tariff_by": "us", "tariff_from": "2029"}) == ol.settings_of(),
        ol.settings_of({"response": "guarantee", "trigger": 1.5}) == ol.settings_of({"policy": "guarantee"}),
        ol.settings_of({"policy": "erode", "expect": "anchored", "rescues": "on", "response": "stimulus", "tariff": 0.0,
                        "care": "trend"}) == ol.settings_of(),
        ol.settings_of({"policy": "erode", "tariff": 10.0})["policy"] == "erode",
        ol.settings_of({"policy": "guarantee"})["policy"] == "guarantee"]
refused = 0
for bad_pick in ({"benefits": 2.0}, {"tariff": -1.0}, {"expect": "firm"}, {"policy": "care-tax"}, {"inflation": "falls"},
                 {"weather": "fine"}):
    try:
        ol.settings_of(bad_pick)
    except ValueError:
        refused += 1
check("L2 one run has one naming, and a setting or value the model does not have is refused", all(same) and refused == 6,
      f"{sum(same)} of {len(same)} namings settle alike; {refused} of 6 refused")
# L3: what each switch does, on the case (the share of the US workforce out of work in 2032Q2)
sw = {k: v["us_out_of_work_2032Q2"] for k, v in R["switches"].items()}
mid = case["us_out_of_work"]["2032Q2"]
worse = ["central banks hold their rates", "expectations slipping", "no deposit insurance", "no unemployment benefits",
         "no response", "spending cuts", "tariffs of 20 points by everyone", "tariffs of 20 points by the US",
         "care stops hiring"]
better = ["benefits half as high again", "a response after one point", "an income guarantee, borrowed",
          "an income guarantee, a levy on AI's income", "care built out, borrowed", "care built out, taxed on wages",
          "care built out, a levy on AI's income"]
check("L3 each switch moves the outcome the way it should: fewer out of work with more support, more with less",
      all(sw[k] > mid for k in worse) and all(sw[k] < mid for k in better)
      and sw["tariffs of 20 points by the US"] < sw["tariffs of 20 points by everyone"]
      and sw["spending cuts"] > sw["no response"] and abs(sw["no bank rescues"] - mid) < 0.5,
      f"the case {mid}%; worse: {min(sw[k] for k in worse)}-{max(sw[k] for k in worse)}%; better: "
      f"{min(sw[k] for k in better)}-{max(sw[k] for k in better)}%; without bank rescues {sw['no bank rescues']}% "
      f"(the rescues' floor does not bind in the US in the case)")
# L4: how a guarantee is paid for: a tax on wages costs the spending of those who pay it; a levy on AI's income costs
# none and borrows less than borrowing all of it
g_b, g_w, g_l = (ol.run({"response": "guarantee", "paid": k}, regs, cm) for k in ("borrowing", "wages", "levy"))
debt = [float(x["out"]["US"]["debt_extra"][-1]) for x in (g_b, g_w, g_l)]
fin = float(np.min(g_w["out"]["US"]["d_fin"]))
check("L4 a guarantee paid for by a tax on wages or a levy borrows less; the tax costs demand, the levy none",
      debt[1] < debt[0] and debt[2] < debt[0] and fin < 0 and float(np.min(g_l["out"]["US"]["d_fin"])) == 0.0
      and sw["an income guarantee, taxed on wages"] > sw["an income guarantee, borrowed"],
      f"US debt added by the end, % of GDP: borrowed {debt[0]:.2f}, wage tax {debt[1]:.2f}, levy {debt[2]:.2f}; the tax's "
      f"drag on spending at most {fin:.2f}% of GDP")
# L5: benefits at their level: the replacement rate scales and is never above 1
lv = {b: gc.support_rate(regs["US"], ol.rules_of(ol.settings_of({"benefits": b}), regs)["US"]) for b in (0.0, 0.5, 1.0, 1.5)}
check("L5 the benefits' level scales the replacement rate", lv[0.0] == 0.0 and lv[1.0] == regs["US"].replacement
      and abs(lv[0.5] - 0.5 * lv[1.0]) < 1e-12 and lv[1.5] == min(1.5 * lv[1.0], 1.0),
      f"US replacement rate {lv[1.0]:.2f} today; {lv[0.5]:.2f} at half, {lv[1.5]:.2f} at one and a half times")
# L6: tariffs by the US alone: its own in full, the others' by their sales to it
tu = ol.rules_of(ol.settings_of({"tariff": 20.0, "tariff_by": "us"}), regs)
check("L6 tariffs raised by the US fall on the others by what they sell to it", tu["US"].tariff == 20.0
      and all(0 < tu[r].tariff < 20.0 for r in ("EA", "FR", "SE", "CN")),
      ", ".join(f"{r} {tu[r].tariff}" for r in gc.R))
# I6: the inflation options
n_ = ol.N
fades, stays, wv = (ol.push_paths(regs, n_, cm, k)[0] for k in ol.INFLATIONS)
check("I6 inflation's options: staying holds the start's excess; the second wave adds three points in every economy "
      "through 2028 and is gone by 2030",
      all(np.allclose(stays[r], fades[r][0]) for r in fades) and sorted(wv) == sorted(gc.R)
      and abs(float(wv["SE"][24]) - ol.WAVE["points"]) < 1e-9 and float(wv["SE"][40]) == 0.0
      and abs(float(wv["US"][24] - fades["US"][24]) - ol.WAVE["points"]) < 1e-9,
      f"US excess {float(fades['US'][0]):.2f} at the start; the wave {float(wv['SE'][12]):.2f} points at the end of September "
      f"2027, {float(wv['SE'][24]):.2f} a year later")
# R10: stagflation is in the model only when expectations come loose
ar_ = R["around"]
st_, w0, w1, w2 = (ar_[k] for k in ("inflation stays where it is", "a second wave of inflation",
                                    "a second wave, expectations slipping", "a second wave, expectations loose"))
check("R10 inflation that stays costs little; a second wave with expectations loose sends the Fed's rate past 15% and "
      "leaves more out of work than any pace does",
      st_["us_out_of_work_2032Q2"] - mid < 1.0 and st_["us_policy_rate_high"][1] < 5
      and w0["us_policy_rate_high"][1] < w1["us_policy_rate_high"][1] < w2["us_policy_rate_high"][1]
      and w2["us_policy_rate_high"][1] > 15 and w2["us_out_of_work_2032Q2"] > ar_["the pace doubles every year"]["us_out_of_work_2032Q2"],
      f"out of work in 2032Q2: stays {st_['us_out_of_work_2032Q2']}%, wave {w0['us_out_of_work_2032Q2']}%, slipping "
      f"{w1['us_out_of_work_2032Q2']}%, loose {w2['us_out_of_work_2032Q2']}% (the case {mid}%); the Fed's high "
      f"{st_['us_policy_rate_high'][1]}, {w0['us_policy_rate_high'][1]}, {w1['us_policy_rate_high'][1]}, "
      f"{w2['us_policy_rate_high'][1]}%")

bad = [n_ for n_, ok, _ in RESULTS if not ok]
print(f"\n{len(RESULTS) - len(bad)}/{len(RESULTS)} checks pass")
sys.exit(1 if bad else 0)
