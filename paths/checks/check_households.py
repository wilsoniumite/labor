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
check("B4 rigid money wages never fall", np.all(np.diff(rr["households"]["W"]) >= -1e-12))
syn = dict(W["status quo"])
syn["participation"] = syn["participation"] * (1 - 0.3 * np.clip(syn["t"] / 10, 0, 1))
d0 = replace(dmp, okun=0.0)
a_, b_ = hh.run(syn, d0, C, s0), hh.run(syn, d0, replace(C, benefit_base="exit"), s0)
check("B5 the benefits-at-exit sensitivity is the layer's rule when the real wage never moves (a world with exits and a flat real wage, "
      "no cyclical re-employment)",
      np.ptp(a_["households"]["W"] / a_["households"]["P"]) < 1e-12 and a_["households"]["out_new"][-1] > 0.25
      and np.max(np.abs(a_["households"]["public_new"] - b_["households"]["public_new"])) < 1e-9 * np.max(a_["households"]["public_new"]),
      f"largest difference {np.max(np.abs(a_['households']['public_new'] - b_['households']['public_new'])):.1e} SEK bn a year")

print("F — the findings (calibration (c), the central; stated as found)")
dd, os_ = S[f"{DDN} | central"]["y5_y8_y10_y12_y15"], S[f"{OSN} | central"]["y5_y8_y10_y12_y15"]
check("F1 floating-rate mortgages move with the branch: debt service rises when deficits dominate, falls when owners' saving does",
      dd["debt_service_pct_income"][3] > dd["debt_service_pct_income"][0] + 1 and os_["debt_service_pct_income"][4] < os_["debt_service_pct_income"][0] - 2,
      f"deficits {dd['debt_service_pct_income']}; owners' saving {os_['debt_service_pct_income']}")
g_full = S[f"{OSN} | demand layer alone (full pooling)"]["gap_min_and_year"][0]
g_hh = S[f"{OSN} | central"]["gap_min_max"][0]
check("F2 so in the falling-rate branch Swedish households cushion the downturn (a smaller gap than full pooling)", g_hh > g_full,
      f"{g_hh} against {g_full}")
r0 = hh.run(W[DDN], dmp, replace(C, replacement_first=0.0, replacement_later=0.0), s0)
rx = hh.run(W[DDN], dmp, replace(C, benefit_base="exit"), s0)
d12 = {k: float(np.interp(12, x["t"], x["households"]["d_out"])) for k, x in (("none", r0), ("state", r), ("exit", rx))}
check("F3 [restated] state support is what keeps the surge in dependence from cutting demand: without it the job losers' drag at year 12 "
      "is 2.2% of GDP; with it zero — the benefit artefact (A1) — or 0.1% with benefits on the wage at exit",
      d12["none"] < -1.5 and d12["state"] >= -1e-9 and -0.3 < d12["exit"] < -0.01 and d12["none"] < 3 * d12["exit"],
      f"{d12['none']:.2f} without state support; {d12['state']:.2f} with it; {d12['exit']:.2f} with benefits on the wage at exit (% of GDP)")
rig = S[f"{OSN} | rigid money wages"]
check("F4 [restated] rigid money wages turn the adjustment into job loss: more people out of work and a deeper gap, longer at the floor — "
      "until employment reaches the layer's floor (A2)",
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
check(f"G1 [restated] {OSN}: leaning on families costs demand — a lower demand level at year 12 and a lower gap trough, for a smaller "
      "state bill — but by 0.17% of GDP, under the 0.2 the claim had (on (b) 0.58). Both levels at year 12 are positive (the constrained "
      "households add demand there) because of the benefit artefact (A1): with benefits on the wage at exit the family-based level is "
      "negative and the cost is above 0.2 again",
      0.1 <= g1[OSN][0] < 0.2 and g1[OSN][1] and g1[OSN][2] and g1[OSN][3] > 0 and g1[OSN][4] > 0 and g1b[OSN] > 0.2
      and gx["family-based support"] < 0 and gx["central"] - gx["family-based support"] > 0.2,
      g1d(OSN) + f"; with benefits at exit: level {gx['family-based support']} against {gx['central']} (cost {gx['central'] - gx['family-based support']:.2f})")
fam_run = {n: hh.run(W[n], dmp, FAM, s0) for n in (DDN, OSN)}
nc_run = {n: hh.run(W[n], dmp, replace(FAM, private_cap=1.0), s0) for n in (DDN, OSN)}
for name in (DDN, OSN):
    fa = S[f"{name} | family-based support"]
    yf = fa["y5_y8_y10_y12_y15"]
    fx = EX[f"{name} | family-based support"]["y5_y8_y10_y12_y15"]
    t_ = fam_run[name]["t"]
    binds = (fam_run[name]["households"]["cap_binds"] > 0.5) & (t_ <= 15 + 1e-9)
    fb_ = CB[f"{name} | family-based support"]["y5_y8_y10_y12_y15"]
    check(f"G2 [restated] {name}: networks run out — the cap on what family and friends give binds in the deep phase; the old second half "
          "(less of the lost wage covered by year 15) disappears with the benefit artefact (A1), and holds with benefits on the wage at exit "
          "only when deficits dominate; the old third clause (networks still at their cap at year 15: supporters' burden at the 10% cap) "
          "disappears too — the burden at year 15 is below the cap — and holds with benefits at exit, as it did on (b)",
          fa["years_network_cap_binds"] > 0 and binds.any() and yf["lost_wage_covered_pct"][4] > 80
          and ((fx["lost_wage_covered_pct"][4] < 80) if name == DDN else (80 <= fx["lost_wage_covered_pct"][4] < 85))
          and yf["supporters_burden_pct"][4] < 9.99 and fx["supporters_burden_pct"][4] >= 9.99 and fb_["supporters_burden_pct"][4] >= 9.99,
          f"cap binds {fa['years_network_cap_binds']} years (years {t_[binds][0]}-{t_[binds][-1]}); covered {yf['lost_wage_covered_pct']}; at exit "
          f"{fx['lost_wage_covered_pct']}; supporters' burden at year 15 {yf['supporters_burden_pct'][4]}% of income (at exit "
          f"{fx['supporters_burden_pct'][4]}; (b) {fb_['supporters_burden_pct'][4]})")
    w_ = t_ <= 15 + 1e-9
    gain = (nc_run[name]["households"]["covered"] - fam_run[name]["households"]["covered"])[binds]
    dlev = np.abs(nc_run[name]["households"]["level"] - fam_run[name]["households"]["level"])[w_]
    check(f"G3 [restated] {name}: while the cap binds it moves who bears the loss more than it moves demand — lifting it covers more of the "
          "lost wage, the demand level moves under 0.05% of GDP (by year 15 the cap no longer binds, so the old year-15 reading is empty)",
          gain.max() > 0.5 and dlev.max() < 0.05,
          f"coverage up to +{gain.max():.2f} points without the cap; demand level within {dlev.max():.3f}% of GDP")
tail = S[f"{OSN} | family-based, rigid money wages"]
check("G4 [restated] the tail is family-based support with rigid money wages: the deepest downturn of every run, about twice 2009's, and the "
      "longest at the floor (its depth set partly by the employment floor, A2)",
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
Wo = {"b": {n: dm.world(*bs.SCEN[n], e=eb_) for n in (DDN, OSN)}, "hi": {n: dm.world(*bs.SCEN[n], e=eh_) for n in (DDN, OSN)}}
onset = {n: artefact_onset(r if n == DDN else hh.run(W[OSN], dmp, C, s0)) for n in (DDN, OSN)}
on_o = {(k, n): artefact_onset(hh.run(Wo[k][n], dmp, C, s0)) for k in Wo for n in (DDN, OSN)}
check("A1 benefits: public support is the replacement rate on the START's real net wage, so once money wages fall far enough it exceeds the "
      "wage lost — from year 9.25 (deficits) and 8.25 (owners' saving) the job losers' drag is zero for good and coverage reaches 176% / "
      "315% by year 15. Not the central root's alone: on the high root it comes later in both branches; on (b) it comes only when "
      "owners' saving dominates, later still, and never within 15 years when deficits do",
      all(o_[0] is not None and 8.0 <= o_[0] <= 10.0 and o_[1] > 150 for o_ in onset.values())
      and all(on_o[("hi", n)][0] is not None and on_o[("hi", n)][0] > onset[n][0] for n in (DDN, OSN))
      and on_o[("b", DDN)][0] is None and on_o[("b", OSN)][0] is not None and on_o[("b", OSN)][0] > onset[OSN][0],
      "; ".join(f"{n}: from year {onset[n][0]}, covered {onset[n][1]:.0f}% at 15" for n in onset) + "; high root: "
      + ", ".join(f"{on_o[('hi', n)][0]} ({on_o[('hi', n)][1]:.0f}%)" for n in (DDN, OSN)) + "; (b): "
      + ", ".join(f"{on_o[('b', n)][0]} ({on_o[('b', n)][1]:.0f}%)" for n in (DDN, OSN)) + " (deficits, owners' saving)")
flo = {}
for name, sp in ((OSN, replace(C, rigid_wages=True)), (DDN, replace(C, rigid_wages=True)), (OSN + ", family", replace(FAM, rigid_wages=True))):
    flo[name] = floor_year(hh.run(W[name.split(",")[0]], dmp, sp, s0))
flo_o = {(k, n): floor_year(hh.run(Wo[k][n], dmp, replace(C, rigid_wages=True), s0)) for k in Wo for n in (DDN, OSN)}
check("A2 [central root only] rigid wages: job loss from rigidity is linear in the accumulated refused cut, and with money wages that would "
      "fall 60-80% it takes employment to the layer's floor (5% of the start's) from year 10.5 when owners' saving dominates (15.5 when "
      "deficits do) — on the central root only: on the high root and on (b) no rigid-wage run reaches the floor within 15 years",
      10.0 <= flo[OSN] <= 11.0 and 10.0 <= flo[OSN + ", family"] <= 11.0 and flo[DDN] > 15.0
      and all(v is None or v > 15.0 for v in flo_o.values()),
      f"floor from year {flo[OSN]} (family-based {flo[OSN + ', family']}; deficits {flo[DDN]}); high root "
      f"{flo_o[('hi', DDN)]} / {flo_o[('hi', OSN)]}, (b) {flo_o[('b', DDN)]} / {flo_o[('b', OSN)]} (deficits / owners' saving; None: never in the run)")

print("S — the sensitivity: benefits on each cohort's real wage at exit (not a default)")
ex_os, ex_dd = EX[f"{OSN} | central"], EX[f"{DDN} | central"]["y5_y8_y10_y12_y15"]
onset_x = {}
for name in (DDN, OSN):
    x = rx if name == DDN else hh.run(W[OSN], dmp, replace(C, benefit_base="exit"), s0)
    d_, t_ = x["households"]["d_out"], x["t"]
    k0 = next(k for k in range(len(t_)) if t_[k] > 3 and np.all(np.abs(d_[k:]) < 1e-12))
    onset_x[name] = (float(t_[k0]), float(x["households"]["covered"][k0]) > 100)
check("S1 with benefits on the wage at exit, F2 survives (households still cushion the falling branch), and the benefit artefact is delayed, "
      "not removed: the job losers' drag is zero for good from year 14 rather than 9.25 when deficits dominate, and from 10.25 rather than "
      "8.25 when owners' saving does — coverage passes 100% then (early cohorts' benefits rest on higher wages than the ones now lost)",
      ex_os["gap_min_max"][0] > g_full and ex_dd["from_job_losers"][2] < -0.3
      and 13.5 <= onset_x[DDN][0] <= 14.5 and 10.0 <= onset_x[OSN][0] <= 10.5 and all(onset_x[n][0] > onset[n][0] and onset_x[n][1] for n in onset_x),
      f"owners' saving gap {ex_os['gap_min_max'][0]} against {g_full} pooled; deficits job losers {ex_dd['from_job_losers']} (years 5/8/10/12/15); drag "
      f"zero from year {onset_x[DDN][0]} / {onset_x[OSN][0]} at exit against {onset[DDN][0]} / {onset[OSN][0]} on the start's wage; owners' saving "
      f"covered {ex_os['y5_y8_y10_y12_y15']['lost_wage_covered_pct']}")

print("X — the switch: (c)'s runs, the (b) comparator, the high root")
variants = {"central": C, "rigid money wages": replace(C, rigid_wages=True), "emergency checks (4% of income for a year)": replace(C, check_size=4.0),
            "rigid wages and checks": replace(C, rigid_wages=True, check_size=4.0), "no private support": replace(C, private=0.0),
            "family-based support": FAM, "family-based, no cap on what networks give": replace(C, **(hh.FAMILY | {"private_cap": 1.0})),
            "family-based, rigid money wages": replace(C, **hh.FAMILY, rigid_wages=True),
            "family-based, with emergency checks": replace(C, **hh.FAMILY, check_size=4.0)}
fresh = {f"{n} | {vn}": hh.summary(hh.run(mp, dmp, sp, s0)) for n, mp in W.items() for vn, sp in variants.items()}
check("X1 households.json's (c) runs equal a fresh rebuild on macro.central(), and its calibration record is the central's",
      all(json.loads(json.dumps(v)) == S[k] for k, v in fresh.items()) and R["calibration"] == json.loads(json.dumps(bs.economy("lo")[1])),
      f"{len(fresh)} runs; {R['calibration']['tag']}")
eb, _ = bs.economy("b")


def world_b_old(bridges, truth):
    """The pre-switch demand.world (medium), with (b)'s hard-coded objects."""
    br = m.Bridges(capital_premium=5.0, **bridges)
    tech = m.TechPath(eta_end=0.04, lam_end=0.01, t_mid=6, width=6) if truth == "new" else m.TechPath(eta_end=1.0, lam_end=eb.lam)
    return m.macro_path(eb, tech, br, 25.0, 0.25)


old_b = {}
for n in (DDN, OSN):
    mpb = world_b_old(*bs.SCEN[n])
    old_b |= {f"{n} | {vn}": hh.summary(hh.run(mpb, dmp, variants[vn], s0)) for vn in hh.COMPARED}
    old_b[f"{n} | demand layer alone (full pooling)"] = dm.summary(dm.run(mpb, dmp))
check("X2 the (b) comparator is the pre-switch layer: rebuilt with (b)'s hard-coded Bridges(capital_premium=5.0) and TechPaths it equals the "
      "stored comparator run for run", all(json.loads(json.dumps(v)) == CB[k] for k, v in old_b.items()) and len(old_b) == len(CB) == 12,
      f"{len(old_b)} runs; the tail {CB[OSN + ' | family-based, rigid money wages']['gap_min_max'][0]} on (b)")
hd, ho = HI[f"{DDN} | central"]["y5_y8_y10_y12_y15"], HI[f"{OSN} | central"]
htail = HI[f"{OSN} | family-based, rigid money wages"]
check("X3 sensitivity, the high root: F1, F2 and G4 hold there too; its rigid-wage runs stay off the employment floor within 15 years",
      hd["debt_service_pct_income"][3] > hd["debt_service_pct_income"][0] + 1 and ho["y5_y8_y10_y12_y15"]["debt_service_pct_income"][4] < ho["y5_y8_y10_y12_y15"]["debt_service_pct_income"][0] - 2
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
