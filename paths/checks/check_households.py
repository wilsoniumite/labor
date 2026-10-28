# check_households.py — the household layer (code/households.py): the bookkeeping is what it says, and the findings,
# stated as found.
#
# Since 2026-09-30 (her decision) the worlds run on calibration (c)'s central economy (macro.central(): the open reading, the
# low root), with bank_scenarios' bridges set on (b) and not retuned. (c)'s wage fall is far larger than (b)'s, and it
# exposes two artefacts of the layer, gated in A: benefits on the start's real wage exceed the collapsing wage from year
# 8-9, and the rigid-wage rule takes employment to the layer's 5% floor from year 10.5. F1, F2, F5, F6 and G1 (deficits)
# hold as stated (numbers moved); F3, F4, G1 (owners' saving), G2-G4 are restated as found; B5 gates the benefits-at-exit
# sensitivity's bookkeeping and S1 reads it; A discloses the artefacts; X gates the switch.
# Thresholds set after seeing (c)'s numbers: F3's -1.5 and (-0.3, -0.01), G1's owners'-saving band [0.1, 0.2), G4's -8,
# A1's years 8-10 and 150, A2's years 10-11, S1's bands (flagged here). G1's 0.2 and G2's 9.99 (the cap, 10% of income) are
# the pre-switch claims' own.
# Restated after the switch's reviews (as found, nothing loosened): G1 (owners' saving) attributes its positive demand levels
# to A1 and reads the benefits-at-exit runs; G2 states the third clause the first restatement dropped (networks still at
# their cap at year 15), which disappears too; A1 and A2 are gated directly on (b) and the high root, not by year-15
# proxies — A1 appears on the high root and, when owners' saving dominates, on (b); A2 (the employment floor) is a
# central-root result.
#
# Restated at the refit (2026-10-27, Log 46; decisions 78-79), as found. The worlds run on the bridges refit on (c) (macro.BRANCHES;
# (b) on its own, macro.BRIDGES_B and SCEN_B); the layer's two rules are redesigned for money wages that fall 60-80%: benefits follow
# the current money wage (the start's real wage and each cohort's real wage at exit are sensitivities), and rigid money wages fall
# at most 4% a year with the log excess costing a share of the jobs left. A1 and A2, which disclosed the two artefacts, now gate the
# redesign (the artefacts gone, and back under the old rules); B4 gates the new rigidity, S1 the exit rule as a sensitivity; F1-F3,
# G1-G4 and X3 are restated (the constrained households now deepen the downturn; the old G1-G2 clauses the artefact removed hold
# again). Thresholds set after seeing the refit's numbers (flagged): F1's bands, F3's -1.5 / -0.5, G2's 40, G3's 20 and 0.2, A1's
# 50-90 and 200 / 100, X3's bands. Corrected at the revision (households:H1, H2, H5, H6): the refit's money wages fell 73-87% by year
# 15, not 60-80% (the pre-refit size); "the constrained households now deepen the downturn" held under the wage rule only, the exit
# and start rules cushioning both branches; A1's 50-90 band followed from the wage rule's own parameters (55-84.25%: bookkeeping);
# A1 had stopped gating (b) and the high root (their onsets were computed and not used); X2's "pre-switch layer" was (b)'s
# pre-switch worlds through the redesigned layer (decisions 78-79 applied to (b) too: 10 of its 12 runs moved at the refit).
# Restated at the revision (2026-10-28, Log 54; her call "Sweden's rules", decision 94, and the rigid-wage excess in logs, decision
# 79 corrected; the worlds on the revised refit, decisions 93 and 95-96). Public support follows Sweden's rules in the central run:
# the first year on the person's own net money wage at exit, fixed for the spell (the a-kassa), then a floor of 0.36 of the start's
# mean net wage indexed to prices (the riksnorm plus a one-room rent); the 'wage' rule (benefits follow the current money wage, the
# default of 27-28 Oct) is the named alternative, stored; the family-based regime is pinned to 'wage' until her call. These rules
# apply to (b)'s runs too: its central rows moved again (deficits 0.00 [-0.10], owners' saving -1.49 [-1.67]). Money wages fall
# 71-84% by year 15. Set in advance: B5 restated (mechanical: it compares the 'wage' rule, which it was built for, with 'exit'), B6
# new (with no unemployment response and no inflation, and the floor at the later rate, the four rules pay the same), B7 new (the
# rigid runs' excess is log(W / W_market) at every date). Restated after seeing the revision's results (its planning runs count as
# seeing; flagged, old -> new): A1 (coverage 55-84% at every date in both branches, the drag never zero -> under Sweden's rules
# coverage passes 100% by the floor: on the central from year 10.75 / 9.75, 163 / 294% at year 15; on the high root when owners'
# saving dominates, 133%, not when deficits do, 96%; on (b) in neither, 68 / 87%; the wage alternative's 55-84% kept as its
# bookkeeping clause); F2 (households deepen both branches, -7.49 / -1.14 against -7.23 / -0.65 pooled -> they cushion the
# owners'-saving branch, -4.02 against -4.65, and deepen the deficits branch a little, -0.60 against -0.35); F3 (state support
# halves the drag, -0.93 against -1.98 -> under Sweden's rules the drag is zero by year 12, the wage alternative halves it, -0.95
# against -2.02; the no-support run sets the floor to zero too, floor_share 0, and asserts it pays nothing: built as before, with
# only the two rates at zero, it still paid the floor, its drag -0.00 at year 12); G1 owners' saving
# (both levels negative, cost 0.42 at the refit -> the state's level positive, +0.49, the family's -0.98, cost 1.47); X3 (the high
# root deepened the falling branch -> cushions it, -3.46 against -4.08); S1's label (on the wage rule, the default, the artefact never
# comes back -> on the wage alternative; under Sweden's rules coverage passes 100% too); S2 new (the wage alternative deepens both
# branches: planning values -0.96 against -0.35, -4.95 against -4.65). A2's label carries its margin (households:H6). X2 relabelled.
# G2, G3 and G4 hold on the pinned family rule. Narrow pass: G3's demand move, 0.164 / 0.177% of GDP against < 0.2. Named later
# (2026-10-28, the record's corrections against the final results, checks:N3 and households:H6 recomputed): A1's "on the high root
# not when deficits dominate", coverage 95.75% at year 15 against 100 (96.9 at 16: rising slowly). Of the two checks:N3 named at
# the refit (F2 0.26 against a pooled -7.23; F4 one 0.25-year step), F2 now differs from pooling by 0.63 / 0.25 points against
# pooled gaps of -4.65 / -0.35, and F4 is 6.5 years at the floor against 6.0 (two steps): no longer narrow. A1's
# wage-alternative clauses are bookkeeping, both the band and the drag that never goes to zero (coverage under 100% leaves a loss);
# A2's floor is a result that rests on the elasticity (its label gives the margin). The high-elasticity sensitivity households:H6
# suggests is not stored: A2 reads the elasticity that would reach the floor off the stored rigid runs (1.02; 0.69 with no cut).
#
# Run from paths/:  ../venv/Scripts/python.exe checks/check_households.py
# Exit status 0 only if every check passes; prints "ALL GREEN (n)" or the failures.

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
import macro as m  # noqa: E402

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


with open(os.path.join(ROOT, "results", "households.json"), encoding="utf-8") as f:
    R = json.load(f)
s0 = R["sweden_start"]
with open(os.path.join(ROOT, "results", "demand.json"), encoding="utf-8") as f:
    cyc = json.load(f)["sweden_cycle"]
dmp = dm.Demand(kappa=cyc["kappa_per_pp_output_gap"], okun=cyc["okun"])
W = {name: dm.world(br, truth) for name, (br, truth) in bs.SCEN.items()}
C = hh.Support()
S = R["scenarios"]
DDN, OSN = "deficits dominate", "owners' saving dominates"
HI, CB = R["sensitivity: the high root"]["scenarios"], R["comparator: calibration (b)"]["scenarios"]
EX = R["sensitivity: benefits on the wage at exit"]["scenarios"]
ST = R["sensitivity: benefits on the start's real wage"]["scenarios"]
NC = R["sensitivity: rigid wages, no money-wage cut"]["scenarios"]

print("D — the Swedish start (Statistics Sweden)")
check("D1 household debt 1.6-1.9 x disposable income, floating share 0.7-0.85, mortgage margin 0.8-1.4 points",
      1.6 < s0["debt"] / s0["disposable"] < 1.9 and 0.7 < s0["floating_share"] < 0.85 and 0.8 < s0["mortgage_margin"] < 1.4,
      f"{s0['debt'] / s0['disposable']:.2f}, {s0['floating_share']:.3f}, {s0['mortgage_margin']:.2f}")

print("B — the bookkeeping")
r = hh.run(W["status quo"], dmp, C, s0)
check("B1 the status quo stays put: no extra demand, no gap, debt service a constant share of income",
      np.abs(r["households"]["level"]).max() < 1e-9 and np.abs(r["gap"]).max() < 1e-9 and np.ptp(r["dsr"][1:]) < 1e-9,
      f"debt service {r['dsr'][5]:.2f}% of income")
r = hh.run(W[DDN], dmp, C, s0)
h = r["households"]
dstep = h["debt"][1:] / h["debt"][:-1]
check("B2 money debts never fall faster than amortisation", dstep.min() >= 1 - C.amort / 100 * 0.25 - 1e-12, f"smallest quarterly ratio {dstep.min():.5f}")
tot = h["d_out"] + h["d_sup"] + h["d_debt"] + h["d_check"]
check("B3 the demand level is the sum of its channels", np.allclose(tot, h["level"]))
rr = hh.run(W[OSN], dmp, replace(C, rigid_wages=True), s0)
rr0 = hh.run(W[OSN], dmp, replace(C, rigid_wages=True, wage_fall_max=0.0), s0)
fall_ = (1 - rr["households"]["W"][1:] / rr["households"]["W"][:-1]) / 0.25 * 100       # % a year, as the layer compounds it
check("B4 [restated at the refit] rigid money wages fall no faster than wage_fall_max (4% a year), and with it at zero never fall",
      fall_.max() <= C.wage_fall_max * (1 + 1e-9) and fall_.max() > 0.5 * C.wage_fall_max and np.all(np.diff(rr0["households"]["W"]) >= -1e-12),
      f"fastest fall {fall_.max():.3f}% a year (limit {C.wage_fall_max:g})")
syn = dict(W["status quo"])
syn["participation"] = syn["participation"] * (1 - 0.3 * np.clip(syn["t"] / 10, 0, 1))
d0 = replace(dmp, okun=0.0)
a_, b_ = hh.run(syn, d0, replace(C, benefit_base="wage"), s0), hh.run(syn, d0, replace(C, benefit_base="exit"), s0)
check("B5 [restated at the revision; mechanical] the benefits-at-exit sensitivity is the 'wage' rule (benefits following the current money "
      "wage, the rule B5 was built for and the default until the revision; now the named alternative) when the real wage never moves (a "
      "world with exits and a flat real wage, no cyclical re-employment)",
      np.ptp(a_["households"]["W"] / a_["households"]["P"]) < 1e-12 and a_["households"]["out_new"][-1] > 0.25
      and np.max(np.abs(a_["households"]["public_new"] - b_["households"]["public_new"])) < 1e-9 * np.max(a_["households"]["public_new"]),
      f"largest difference {np.max(np.abs(a_['households']['public_new'] - b_['households']['public_new'])):.1e} SEK bn a year")
syn0 = dict(syn, pi_star=0.0, pi_wage=np.zeros_like(syn["t"]))       # no inflation: money and real wages flat
d00 = replace(dmp, okun=0.0, kappa=0.0)                               # no cyclical job loss, no Phillips curve: prices flat
C6 = replace(C, floor_share=C.replacement_later)                      # the floor at the later rate, so the four rules can agree
runs6 = {b: hh.run(syn0, d00, replace(C6, benefit_base=b), s0) for b in ("sweden", "wage", "exit", "start")}
pn6 = {b: r6["households"]["public_new"] for b, r6 in runs6.items()}
gap6 = max(float(np.max(np.abs(pn6[b] - pn6["wage"]))) for b in pn6) / float(np.max(np.abs(pn6["wage"])))
h6 = runs6["sweden"]["households"]
check("B6 [new at the revision; set in advance] Sweden's rules are bookkeeping-consistent with the others: in a world with exits, no "
      "inflation and no cyclical job loss or Phillips curve (money and real wages flat, prices flat), and the floor at the later rate, the "
      "four rules — Sweden's, the current money wage, the real wage at exit, the start's real wage — pay the same public support at every "
      "date (within 1e-12 of its largest value); the world exercises both the first year and the years after it",
      gap6 < 1e-12 and np.ptp(h6["P"]) < 1e-15 and np.ptp(h6["W"]) < 1e-15 and np.all(np.diff(h6["out_new"]) >= -1e-15)
      and h6["out_new"][-1] > 0.25,
      f"largest relative gap {gap6:.1e}; out of work at the end {h6['out_new'][-1]:.3f} of the start's employment")
rig_runs = {(n, lab): hh.run(W[n], dmp, sp_, s0) for n in (DDN, OSN)
            for lab, sp_ in (("central", replace(C, rigid_wages=True)), ("family-based", replace(C, **hh.FAMILY, rigid_wages=True)))}
b7 = max(float(np.max(np.abs(x["households"]["wage_excess"] - np.log(x["households"]["W"] / x["households"]["W_market"]))))
         for x in rig_runs.values())
x7 = rig_runs[(OSN, "central")]["households"]
check("B7 [new at the revision; set in advance] rigid money wages' excess is tracked in logs (decision 79 corrected): at every date of the "
      "rigid runs (central and family-based, both branches) the excess the job loss is charged on is log(W / W_market), the money wage "
      "over the market money wage (until the revision it was summed linearly, a first-order approximation that understated job loss)",
      b7 < 1e-12 and float(np.max(x7["wage_excess"])) > 1.0,
      f"largest gap {b7:.1e}; owners' saving's largest log excess {float(np.max(x7['wage_excess'])):.3f} (W / W_market at year 15 "
      f"{float(np.interp(15, rig_runs[(OSN, 'central')]['t'], x7['W'] / x7['W_market'])):.2f})")

print("F — the findings (calibration (c), the central; stated as found)")
dd, os_ = S[f"{DDN} | central"]["y5_y8_y10_y12_y15"], S[f"{OSN} | central"]["y5_y8_y10_y12_y15"]
check("F1 [restated at the refit] floating-rate mortgages move with policy, and on the refit policy falls in both branches: debt service "
      "falls most when owners' saving takes rates to the floor; with deficits dominating it rises a little to year 10, as money incomes "
      "fall faster than rates, then falls (before the refit it rose by more than a point there)",
      os_["debt_service_pct_income"][4] < os_["debt_service_pct_income"][0] - 2
      and dd["debt_service_pct_income"][2] > dd["debt_service_pct_income"][0] and dd["debt_service_pct_income"][4] < dd["debt_service_pct_income"][0],
      f"deficits {dd['debt_service_pct_income']}; owners' saving {os_['debt_service_pct_income']}")
g_full = S[f"{OSN} | demand layer alone (full pooling)"]["gap_min_and_year"][0]
g_hh = S[f"{OSN} | central"]["gap_min_max"][0]
g_hd, g_fd = S[f"{DDN} | central"]["gap_min_max"][0], S[f"{DDN} | demand layer alone (full pooling)"]["gap_min_and_year"][0]
check("F2 [restated at the refit and at the revision] the sign is set by the benefit rule: under Sweden's rules (decision 94) Swedish "
      "households cushion the falling branch (a smaller gap than full pooling when owners' saving dominates: the price-indexed floor "
      "outruns the collapsing wage, and falling rates ease debt service) and deepen the deficits branch a little; under the wage "
      "alternative they deepen both (S2; at the refit, on that rule, -7.49 / -1.14 against -7.23 / -0.65 pooled); before the refit they "
      "cushioned the falling branch too, on the start's real wage (A1)", g_hh > g_full and g_hd < g_fd,
      f"owners' saving {g_hh} against {g_full} pooled; deficits {g_hd} against {g_fd}")
r0 = hh.run(W[DDN], dmp, replace(C, replacement_first=0.0, replacement_later=0.0, floor_share=0.0), s0)
rw = hh.run(W[DDN], dmp, replace(C, benefit_base="wage"), s0)
rx = hh.run(W[DDN], dmp, replace(C, benefit_base="exit"), s0)
rs = hh.run(W[DDN], dmp, replace(C, benefit_base="start"), s0)
d12 = {k: float(np.interp(12, x["t"], x["households"]["d_out"]))
       for k, x in (("none", r0), ("state", r), ("wage", rw), ("exit", rx), ("start", rs))}
check("F3 [restated at the refit and at the revision] state support takes out the surge in dependence's cut to demand by year 12: without "
      "it (no public support at all, the floor included) the job losers' drag at year 12 is 2.0% of GDP; under Sweden's rules it is zero — "
      "the price-indexed floor exceeds the wage lost once money wages have fallen far enough — as under the rules that hold benefits in "
      "real terms (the start's real wage, the rule before the refit, or each cohort's wage at exit); under the wage alternative state "
      "support halves it (0.9%; at the refit's default, the same rule, 0.93 against 1.98)",
      np.max(np.abs(r0["households"]["public_new"])) == 0.0 and d12["none"] < -1.5 and abs(d12["state"]) < 1e-9
      and -1.5 < d12["wage"] < -0.5 and d12["none"] < 1.5 * d12["wage"] and abs(d12["start"]) < 1e-9 and abs(d12["exit"]) < 1e-9,
      f"{d12['none']:.2f} without state support; {d12['state']:.2f} under Sweden's rules; {d12['wage']:.2f} under the wage alternative; "
      f"{d12['start']:.2f} / {d12['exit']:.2f} on the start's real wage / at exit (% of GDP)")
rig = S[f"{OSN} | rigid money wages"]
check("F4 [restated at the refit] rigid money wages turn the adjustment into job loss: more people out of work and a deeper gap, longer "
      "at the floor (the layer's employment floor no longer reached: A2)",
      rig["y5_y8_y10_y12_y15"]["out_of_work_pp"][2] > os_["out_of_work_pp"][2] + 5 and rig["gap_min_max"][0] < g_hh - 1 and rig["years_at_floor"] > S[f"{OSN} | central"]["years_at_floor"],
      f"out of work at year 10 {rig['y5_y8_y10_y12_y15']['out_of_work_pp'][2]}% against {os_['out_of_work_pp'][2]}%; gap {rig['gap_min_max'][0]} against {g_hh}; "
      f"{rig['years_at_floor']} years at the floor against {S[OSN + ' | central']['years_at_floor']}")
ck = hh.run(W[DDN], dmp, replace(C, check_size=4.0), s0)
on = ck["households"]["check"] > 0
check("F5 emergency checks lift output only while they are paid", on.any() and (ck["gap"][on] - r["gap"][on]).min() > 0.1
      and abs(np.interp(14, ck["t"], ck["gap"]) - np.interp(14, r["t"], r["gap"])) < 0.05,
      f"while paid +{(ck['gap'][on] - r['gap'][on]).mean():.2f} points (from year {ck['t'][on][0]}); at year 14 {np.interp(14, ck['t'], ck['gap']) - np.interp(14, r['t'], r['gap']):+.3f}")
np_ = S[f"{DDN} | no private support"]["y5_y8_y10_y12_y15"]["demand_level"][2]
check("F6 under today's Swedish state support, family and friends change little (the demand level within 0.05% of GDP without them)",
      abs(np_ - dd["demand_level"][2]) < 0.05, f"{np_} against {dd['demand_level'][2]}")

print("G — family-based support against today's Swedish state support")
FAM = replace(C, **hh.FAMILY)
g1 = {}
for name in (DDN, OSN):
    st, fa = S[f"{name} | central"], S[f"{name} | family-based support"]
    ys, yf = st["y5_y8_y10_y12_y15"], fa["y5_y8_y10_y12_y15"]
    g1[name] = (ys["demand_level"][3] - yf["demand_level"][3], fa["gap_min_max"][0] <= st["gap_min_max"][0], yf["support_cost_pct_gdp"][3] < ys["support_cost_pct_gdp"][3],
                yf["demand_level"][3], ys["demand_level"][3], yf["support_cost_pct_gdp"][3], ys["support_cost_pct_gdp"][3])
g1b = {n: CB[f"{n} | central"]["y5_y8_y10_y12_y15"]["demand_level"][3] - CB[f"{n} | family-based support"]["y5_y8_y10_y12_y15"]["demand_level"][3]
       for n in (DDN, OSN)}
g1d = lambda n: f"level {g1[n][3]} against {g1[n][4]} (cost {g1[n][0]:.2f}; (b) {g1b[n]:.2f}), state bill {g1[n][5]} against {g1[n][6]} % of GDP"  # noqa: E731
check(f"G1 {DDN}: leaning on families costs demand — a larger drag from constrained households at year 12 and a lower gap trough, for a "
      "smaller state bill",
      g1[DDN][0] > 0.2 and g1[DDN][1] and g1[DDN][2], g1d(DDN))
gx = {v: EX[f"{OSN} | {v}"]["y5_y8_y10_y12_y15"]["demand_level"][3] for v in ("central", "family-based support")}
check(f"G1 [restated at the refit and at the revision] {OSN}: leaning on families costs demand — a lower demand level at year 12 and a "
      "lower gap trough, for a smaller state bill — by more than the 0.2% of GDP the claim had (as on (b)); the family-based level is "
      "negative, while under Sweden's rules the state's is positive (the job losers' drag zero by then, the floor above the wage lost, and "
      "falling rates easing debt service; at the refit, benefits following wages, both were negative, cost 0.42; before it both positive, "
      "cost 0.17, through the benefit artefact)",
      g1[OSN][0] > 0.2 and g1[OSN][1] and g1[OSN][2] and g1[OSN][3] < 0 < g1[OSN][4] and g1b[OSN] > 0.2,
      g1d(OSN) + f"; with benefits at exit: level {gx['family-based support']} against {gx['central']}")
fam_run = {n: hh.run(W[n], dmp, FAM, s0) for n in (DDN, OSN)}
nc_run = {n: hh.run(W[n], dmp, replace(FAM, private_cap=1.0), s0) for n in (DDN, OSN)}
for name in (DDN, OSN):
    fa = S[f"{name} | family-based support"]
    yf = fa["y5_y8_y10_y12_y15"]
    fx = EX[f"{name} | family-based support"]["y5_y8_y10_y12_y15"]
    t_ = fam_run[name]["t"]
    binds = (fam_run[name]["households"]["cap_binds"] > 0.5) & (t_ <= 15 + 1e-9)
    fb_ = CB[f"{name} | family-based support"]["y5_y8_y10_y12_y15"]
    check(f"G2 [restated at the refit] {name}: networks run out — the cap on what family and friends give binds from the deep phase to "
          "year 15, less and less of the lost wage is covered (under 40% by year 15), and the supporters' burden sits at the 10% cap at year "
          "15, as on (b) — the clauses the benefit artefact had removed before the refit hold again",
          fa["years_network_cap_binds"] > 0 and binds.any() and t_[binds][-1] >= 15.0 - 1e-9 and yf["lost_wage_covered_pct"][4] < 40
          and yf["supporters_burden_pct"][4] >= 9.99 and fb_["supporters_burden_pct"][4] >= 9.99,
          f"cap binds {fa['years_network_cap_binds']} years (years {t_[binds][0]}-{t_[binds][-1]}); covered {yf['lost_wage_covered_pct']}; at exit "
          f"{fx['lost_wage_covered_pct']}; supporters' burden at year 15 {yf['supporters_burden_pct'][4]}% of income (at exit "
          f"{fx['supporters_burden_pct'][4]}; (b) {fb_['supporters_burden_pct'][4]})")
    w_ = t_ <= 15 + 1e-9
    gain = (nc_run[name]["households"]["covered"] - fam_run[name]["households"]["covered"])[binds]
    dlev = np.abs(nc_run[name]["households"]["level"] - fam_run[name]["households"]["level"])[w_]
    check(f"G3 [restated at the refit] {name}: while the cap binds it moves who bears the loss far more than it moves demand — lifting it "
          "covers up to about 30 points more of the lost wage and moves the demand level by under 0.2% of GDP (before the refit under 0.05)",
          gain.max() > 20 and dlev.max() < 0.2,
          f"coverage up to +{gain.max():.2f} points without the cap; demand level within {dlev.max():.3f}% of GDP")
tail = S[f"{OSN} | family-based, rigid money wages"]
check("G4 [restated at the refit] the tail is family-based support with rigid money wages: the deepest downturn of every run, more than "
      "twice 2009's, and the longest at the floor",
      tail["gap_min_max"][0] == min(v["gap_min_max"][0] for k, v in S.items() if "gap_min_max" in v) and tail["gap_min_max"][0] < -8.0
      and tail["years_at_floor"] == max(v["years_at_floor"] for k, v in S.items() if "years_at_floor" in v),
      f"gap {tail['gap_min_max'][0]}, inflation {tail['inflation_min_max'][0]}, {tail['years_at_floor']} years at the floor; covered "
      f"{tail['y5_y8_y10_y12_y15']['lost_wage_covered_pct'][4]}% by year 15; (b) {CB[OSN + ' | family-based, rigid money wages']['gap_min_max'][0]}")

print("A — the artefacts (c) exposes, disclosed")


def artefact_onset(x, horizon=15.0):
    """The first date after year 3 and within the horizon from which coverage is over 100% and the job losers' drag is zero
    for good (to the run's end), and coverage at the horizon; (None, ...) if there is none."""
    t_, cov, d_ = x["t"], x["households"]["covered"], x["households"]["d_out"]
    w = t_ <= horizon + 1e-9
    k15 = int(np.argmin(np.abs(t_ - horizon)))
    for k0 in np.nonzero((cov > 100) & (t_ > 3) & w)[0]:
        if np.all(np.abs(d_[k0:]) < 1e-12):
            return float(t_[k0]), float(cov[k15])
    return None, float(cov[k15])


def floor_year(x):
    """The first date employment reaches the layer's floor (5% of the start's), or None."""
    at_floor = x["households"]["employed"] <= 0.05 + 1e-12
    return float(x["t"][at_floor][0]) if at_floor.any() else None


eb_, _ = bs.economy("b")
eh_, _ = bs.economy("hi")
Wo = {"b": {n: dm.world(*bs.SCEN_B[n], e=eb_, base=m.BRIDGES_B) for n in (DDN, OSN)}, "hi": {n: dm.world(*bs.SCEN[n], e=eh_) for n in (DDN, OSN)}}
onset = {n: artefact_onset(r if n == DDN else hh.run(W[OSN], dmp, C, s0)) for n in (DDN, OSN)}      # Sweden's rules
on_o = {(k, n): artefact_onset(hh.run(Wo[k][n], dmp, C, s0)) for k in Wo for n in (DDN, OSN)}
CW = replace(C, benefit_base="wage")                                                                   # the named alternative
cov = {}
for n in (DDN, OSN):
    x = hh.run(W[n], dmp, CW, s0)
    w_ = (x["t"] > 0.5) & (x["t"] <= 15 + 1e-9)
    cov[n] = (float(x["households"]["covered"][w_].min()), float(x["households"]["covered"][w_].max()),
              float(np.interp(15, x["t"], x["households"]["d_out"])), artefact_onset(x)[0])
band = (100 * (C.replacement_later + C.private * (1 - C.replacement_later)),              # the wage rule's own bounds: no first year,
        100 * (C.replacement_first + C.private * (1 - C.replacement_first)            # savings gone; all first year, savings drawn
               + C.draw * (1 - C.private) * (1 - C.replacement_first)))
st15 = {n: ST[f"{n} | central"]["y5_y8_y10_y12_y15"]["lost_wage_covered_pct"][4] for n in (DDN, OSN)}
ex15 = {n: EX[f"{n} | central"]["y5_y8_y10_y12_y15"]["lost_wage_covered_pct"][4] for n in (DDN, OSN)}
check("A1 [restated at the refit and at the revision, decision 94] under Sweden's rules coverage of the lost wage passes 100% once money "
      "wages fall below the price-indexed floor — a consequence of the floor, not an artefact — and the job losers' drag goes to zero for "
      "good: on the central in both branches, on the high root when owners' saving dominates (not when deficits do), on (b) in neither "
      "within 15 years. Under the wage alternative (the rule from the refit to the revision) coverage stays between 50% and 90% at every "
      "date — bookkeeping: the rule's own rates bound it, 55-84.25% — and the drag never goes to zero (bookkeeping too: coverage under "
      "100% leaves a loss). The old rule and the wage at exit, "
      "kept as sensitivities, still outrun the collapsing wage: coverage by year 15 over 200% on the start's real wage and over 100% at exit "
      "(before the refit, on the start's real wage, the drag was zero from year 9.25 / 8.25, coverage 176% / 315% by year 15)",
      all(onset[n][0] is not None and onset[n][1] > 100 for n in (DDN, OSN))
      and on_o[("hi", OSN)][0] is not None and on_o[("hi", DDN)][0] is None and on_o[("hi", DDN)][1] < 100
      and all(on_o[("b", n)][0] is None and on_o[("b", n)][1] < 100 for n in (DDN, OSN))
      and all(band[0] <= c_[0] and c_[1] <= band[1] + 1e-9 and 50 < c_[0] and c_[1] < 90 and c_[2] < -0.3 and c_[3] is None for c_ in cov.values())
      and all(v > 200 for v in st15.values()) and all(v > 100 for v in ex15.values()),
      "Sweden's rules: " + "; ".join(f"{n} from year {onset[n][0]}, {onset[n][1]:.0f}% at 15" for n in (DDN, OSN))
      + "; high root " + " / ".join(f"{on_o[('hi', n)][0]} ({on_o[('hi', n)][1]:.0f}%)" for n in (DDN, OSN))
      + "; (b) " + " / ".join(f"{on_o[('b', n)][0]} ({on_o[('b', n)][1]:.0f}%)" for n in (DDN, OSN))
      + "; the wage alternative: " + "; ".join(f"{n} covered {cov[n][0]:.2f}-{cov[n][1]:.2f}% (bounds {band[0]:.0f}-{band[1]:.2f}), drag at 15 "
                                               f"{cov[n][2]:.2f}% of GDP" for n in cov)
      + "; at 15 on the start's real wage " + " / ".join(f"{st15[n]:.0f}" for n in (DDN, OSN)) + "%, at exit "
      + " / ".join(f"{ex15[n]:.0f}" for n in (DDN, OSN)) + "% (deficits / owners' saving)")
flo = {}
for name, sp in ((OSN, replace(C, rigid_wages=True)), (DDN, replace(C, rigid_wages=True)), (OSN + ", family", replace(FAM, rigid_wages=True)),
                 (OSN + ", no cut", replace(C, rigid_wages=True, wage_fall_max=0.0)), (OSN + ", family, no cut", replace(FAM, rigid_wages=True, wage_fall_max=0.0))):
    flo[name] = floor_year(hh.run(W[name.split(",")[0]], dmp, sp, s0))
flo_o = {(k, n): floor_year(hh.run(Wo[k][n], dmp, replace(C, rigid_wages=True), s0)) for k in Wo for n in (DDN, OSN)}
emp_low = float(rr["households"]["employed"].min())


def eps_to_floor(x):
    """The labour-demand elasticity at which a rigid run would first reach the layer's floor (the smallest over dates of
    log(employment before the excess / 0.05) / the log excess), and the run's largest log excess."""
    h_ = x["households"]
    base_ = h_["employed"] + h_["extra_job_loss"]
    on_ = h_["wage_excess"] > 1e-9
    return float(np.min(np.log(base_[on_] / 0.05) / h_["wage_excess"][on_])), float(np.max(h_["wage_excess"]))


eps_c, xmax_c = eps_to_floor(rr)
eps_0, xmax_0 = eps_to_floor(rr0)
check("A2 [the redesign, decision 79; its label at the revision] rigid money wages fall at most 4% a year and the log excess over the market "
      "wage (tracked in logs since the revision, B7) costs a share of the jobs still there (the labour-demand elasticity 0.4): no rigid-wage "
      "run reaches the layer's floor (5% of the start's employment) on the central, the high root or (b), nor with no money-wage cut at all "
      "(before the refit the central's owners'-saving run reached it from year 10.5). The margin rests on the elasticity, estimated on "
      "small wage changes and applied here to log excesses up to about 1.4 (2.0 with no cut): an elasticity of about 1.0 (0.7 with no "
      "cut) would reach the floor",
      all(v is None for v in flo.values()) and all(v is None for v in flo_o.values()) and emp_low > 0.05,
      f"floors reached: {[k for k, v in {**flo, **{str(k): v for k, v in flo_o.items()}}.items() if v is not None]}; lowest employment "
      f"{emp_low:.3f} of the start's (owners' saving, rigid wages; at the refit, the excess summed linearly, 0.096); largest log excess "
      f"{xmax_c:.2f} ({xmax_0:.2f} with no cut); the elasticity that would reach the floor {eps_c:.2f} ({eps_0:.2f} with no cut)")

print("S — the sensitivity: benefits on each cohort's real wage at exit (not a default)")
ex_os, ex_dd = EX[f"{OSN} | central"], EX[f"{DDN} | central"]["y5_y8_y10_y12_y15"]
onset_x = {}
for name in (DDN, OSN):
    x = rx if name == DDN else hh.run(W[OSN], dmp, replace(C, benefit_base="exit"), s0)
    d_, t_ = x["households"]["d_out"], x["t"]
    k0 = next((k for k in range(len(t_)) if t_[k] > 3 and np.all(np.abs(d_[k:]) < 1e-12)), None)
    onset_x[name] = (float(t_[k0]), float(x["households"]["covered"][k0]) > 100) if k0 is not None else (None, False)
check("S1 [restated at the refit; its label at the revision] with benefits on each cohort's real wage at exit (a sensitivity) the job "
      "losers' drag goes to zero for good within 15 years in both branches, coverage passing 100% (early cohorts' benefits rest on higher "
      "wages than the ones now lost) — on the wage alternative it never does (A1); under Sweden's rules (the default) coverage passes 100% "
      "too, by the price-indexed floor (A1)",
      all(v[0] is not None and v[0] <= 15.0 and v[1] for v in onset_x.values()),
      f"drag zero from year {onset_x[DDN][0]} (deficits) / {onset_x[OSN][0]} (owners' saving); owners' saving covered "
      f"{ex_os['y5_y8_y10_y12_y15']['lost_wage_covered_pct']}; deficits job losers {ex_dd['from_job_losers']} (years 5/8/10/12/15)")
ALT = R["alternative: benefits follow the current money wage"]["scenarios"]
ga = {n: ALT[f"{n} | central"]["gap_min_max"][0] for n in (DDN, OSN)}
gp = {n: S[f"{n} | demand layer alone (full pooling)"]["gap_min_and_year"][0] for n in (DDN, OSN)}
gs = {n: S[f"{n} | central"]["gap_min_max"][0] for n in (DDN, OSN)}
check("S2 [new at the revision, set after seeing] the named alternative, benefits following the current money wage (the rule from the refit "
      "to the revision; stored beside Sweden's rules): under it the constrained households deepen both branches (a larger gap than full "
      "pooling), deeper than under Sweden's rules in both — so F2's sign, and the cushion in the falling branch, are the benefit rule's",
      all(ga[n] < gp[n] and ga[n] < gs[n] for n in (DDN, OSN)),
      "; ".join(f"{n}: {ga[n]} against {gp[n]} pooled ({gs[n]} under Sweden's rules)" for n in (DDN, OSN)))

print("X — the switch: (c)'s runs, the (b) comparator, the high root")
variants = {"central": C, "rigid money wages": replace(C, rigid_wages=True), "emergency checks (4% of income for a year)": replace(C, check_size=4.0),
            "rigid wages and checks": replace(C, rigid_wages=True, check_size=4.0), "no private support": replace(C, private=0.0),
            "family-based support": FAM, "family-based, no cap on what networks give": replace(C, **(hh.FAMILY | {"private_cap": 1.0})),
            "family-based, rigid money wages": replace(C, **hh.FAMILY, rigid_wages=True),
            "family-based, with emergency checks": replace(C, **hh.FAMILY, check_size=4.0)}
fresh = {f"{n} | {vn}": hh.summary(hh.run(mp, dmp, sp, s0)) for n, mp in W.items() for vn, sp in variants.items()}
AUT = (DDN, OSN)
blocks = {"alternative: benefits follow the current money wage":
          {f"{n} | {vn}": replace(variants[vn], benefit_base="wage") for n in AUT for vn in ("central", "rigid money wages", "no private support")},
          "sensitivity: the floor's level":
          {f"{n} | {vn} | floor_share {fs:g}": replace(variants[vn], floor_share=fs) for n in AUT for vn in ("central", "rigid money wages")
           for fs in (0.27, 0.43)},
          "sensitivity: the first year at the aggregate a-kassa rate": {f"{n} | central": replace(C, replacement_first=0.51) for n in AUT},
          "sensitivity: the family-based regime on Sweden's structure":
          {f"{n} | {vn}": replace(variants[vn], benefit_base="sweden", floor_share=0.25) for n in AUT
           for vn in ("family-based support", "family-based, no cap on what networks give", "family-based, rigid money wages")},
          "sensitivity: benefits on the wage at exit": {f"{n} | {vn}": replace(variants[vn], benefit_base="exit") for n in AUT for vn in hh.EXIT_COMPARED},
          "sensitivity: benefits on the start's real wage": {f"{n} | {vn}": replace(variants[vn], benefit_base="start") for n in AUT for vn in hh.EXIT_COMPARED},
          "sensitivity: rigid wages, no money-wage cut":
          {f"{n} | {vn}": replace(variants[vn], wage_fall_max=0.0) for n in AUT for vn in ("rigid money wages", "family-based, rigid money wages")}}
same_blocks = all(json.loads(json.dumps({k: hh.summary(hh.run(W[k.split(" | ")[0]], dmp, sp_, s0)) for k, sp_ in bl.items()})) == R[key]["scenarios"]
                  for key, bl in blocks.items())
check("X1 [extended at the revision] households.json's (c) runs equal a fresh rebuild on macro.central() — the scenarios and every "
      "sensitivity block (the wage alternative, the floor's level, the first year at the aggregate a-kassa rate, the family-based regime on "
      "Sweden's structure, benefits at exit and on the start's real wage, rigid wages with no cut) — its calibration record is the "
      "central's, and its stored evidence and support are the code's (benefit_evidence; the central's floor 0.36 is the evidence's 0.3616 "
      "to two decimals)",
      all(json.loads(json.dumps(v)) == S[k] for k, v in fresh.items()) and R["calibration"] == json.loads(json.dumps(bs.economy("lo")[1]))
      and same_blocks and R["evidence"] == json.loads(json.dumps(hh.benefit_evidence(s0))) and R["support"] == json.loads(json.dumps(C.__dict__))
      and round(R["evidence"]["floor_share"]["derived"], 2) == C.floor_share,
      f"{len(fresh)} runs and {sum(len(b_) for b_ in blocks.values())} sensitivity runs; {R['calibration']['tag']}; the floor "
      f"{R['evidence']['floor_share']['derived']} (cross-checks " + " / ".join(f"{v:.3f}" for v in R["evidence"]["floor_share"]
      ["cross_checks_on_the_layer_s_wage_bill"].values()) + f"), the a-kassa's aggregate first-year rate "
      f"{R['evidence']['replacement_first']['aggregate_gross_rate_under_the_ceiling']}")
eb, _ = bs.economy("b")


def world_b_old(bridges, truth):
    """The pre-switch demand.world (medium), with (b)'s hard-coded objects."""
    br = replace(m.BRIDGES_B, capital_premium=5.0, **bridges)
    tech = m.TechPath(eta_end=0.04, lam_end=0.01, t_mid=6, width=6) if truth == "new" else m.TechPath(eta_end=1.0, lam_end=eb.lam)
    return m.macro_path(eb, tech, br, 25.0, 0.25)


old_b = {}
for n in (DDN, OSN):
    mpb = world_b_old(*bs.SCEN_B[n])
    old_b |= {f"{n} | {vn}": hh.summary(hh.run(mpb, dmp, variants[vn], s0)) for vn in hh.COMPARED}
    old_b[f"{n} | demand layer alone (full pooling)"] = dm.summary(dm.run(mpb, dmp))
check("X2 [relabelled at the revision] the (b) comparator is (b)'s pre-switch macro worlds through today's household layer: rebuilt with "
      "(b)'s hard-coded Bridges(capital_premium=5.0) and TechPaths, under the layer's current rules (decisions 78-79 and 94 apply to (b)'s "
      "runs too, so 10 of its 12 runs moved at the refit and its central rows again at the revision; the two pooled runs are the macro "
      "worlds alone), it equals the stored comparator run for run", all(json.loads(json.dumps(v)) == CB[k] for k, v in old_b.items()) and len(old_b) == len(CB) == 12,
      f"{len(old_b)} runs; the tail {CB[OSN + ' | family-based, rigid money wages']['gap_min_max'][0]} on (b); its central rows: deficits "
      f"{CB[DDN + ' | central']['gap_min_max'][0]}, owners' saving {CB[OSN + ' | central']['gap_min_max'][0]} (pooled "
      f"{CB[OSN + ' | demand layer alone (full pooling)']['gap_min_and_year'][0]})")
hd, ho = HI[f"{DDN} | central"]["y5_y8_y10_y12_y15"], HI[f"{OSN} | central"]
htail = HI[f"{OSN} | family-based, rigid money wages"]
check("X3 [restated at the refit and at the revision] sensitivity, the high root: F1's owners'-saving branch, F2 (restated: under Sweden's "
      "rules households cushion the falling branch there too; at the refit, on the wage rule, they deepened it) and G4 hold there too; its "
      "rigid-wage runs stay off the employment floor",
      ho["y5_y8_y10_y12_y15"]["debt_service_pct_income"][4] < ho["y5_y8_y10_y12_y15"]["debt_service_pct_income"][0] - 2
      and ho["gap_min_max"][0] > HI[f"{OSN} | demand layer alone (full pooling)"]["gap_min_and_year"][0]
      and htail["gap_min_max"][0] == min(v["gap_min_max"][0] for v in HI.values() if "gap_min_max" in v)
      and htail["years_at_floor"] == max(v["years_at_floor"] for v in HI.values() if "years_at_floor" in v)
      and max(v["y5_y8_y10_y12_y15"]["out_of_work_pp"][4] for v in HI.values() if "gap_min_max" in v) < 95.0,
      f"debt service {hd['debt_service_pct_income']} / {ho['y5_y8_y10_y12_y15']['debt_service_pct_income']}; owners' saving gap {ho['gap_min_max'][0]} against "
      f"{HI[OSN + ' | demand layer alone (full pooling)']['gap_min_and_year'][0]} pooled; tail {htail['gap_min_max'][0]}, {htail['years_at_floor']} years at the floor; "
      f"out of work at 15 at most {max(v['y5_y8_y10_y12_y15']['out_of_work_pp'][4] for v in HI.values() if 'gap_min_max' in v)}%")

n_ok = sum(ok for _, ok, _ in RESULTS)
fails = [n for n, ok, _ in RESULTS if not ok]
print(f"\n{n_ok}/{len(RESULTS)} checks passed")
print(f"ALL GREEN ({len(RESULTS)})" if not fails else "FAILURES: " + "; ".join(n.split(" ")[0] for n in fails))
sys.exit(0 if n_ok == len(RESULTS) else 1)
