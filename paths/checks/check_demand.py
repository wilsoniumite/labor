# check_demand.py — the demand layer (code/demand.py): the mechanics are what they say, and the findings, stated
# as found.
#
# Since 2026-09-30 (her decision) the worlds run on calibration (c)'s central economy (macro.central(): the open reading, the
# low root), with bank_scenarios' bridges set on (b) and not retuned. F1, F2 and F5 hold as stated (numbers moved); F3 is
# restated (its inflation band no longer holds with a weak anchor); F4 is restated to the size found; F6 is new. R gates the
# neutral-rate readout (r* with the capex channel keyed to investment spending: a sensitivity, not a finding; R6 the net-
# investment diagnostic beside it); X the switch.
# Thresholds set after seeing (c)'s numbers: F3's 1.25, F4's 0.4-0.6, F6's 3.5 and 12, R3's and R4's bands, R6's -40 and
# one-half (flagged here). F3's 1.25 is a regression guard on the weak-anchor low, set 3 bp under the 1.28 found so that a
# change in the runs shows: it is not part of the claim, whose content is the exception itself (the low below 1.5).
# The (b) numbers quoted in F3 and F4 are computed here from (b)'s worlds (bs.economy("b"), the comparator X2 gates as the
# pre-switch layer), not copied from the pre-switch report.
# Restated at the refit (2026-10-27, Log 46; the central on the bridges refit on (c) in macro.BRANCHES, (b) on its own), as found:
# M3 reads both branches' gaps as troughs (r* now falls in both); F2 (the deficits branch is now a small slump, not a boom), F3
# (the owners'-saving cycle is no longer normal-sized), F4 (the cyclical rise is about a point) and F6 (the floor binds longer and
# sooner) restated; R reads the readout keyed back to the pace (before: keyed to investment). Thresholds set after seeing the
# refit's numbers (flagged): F2's -0.3 / -1.0, F3's -3.5 and 1.5 / 1.75, F4's 1.5, F6's 6 and 9, R3's and R4's bands.
#
# Run from paths/:  ../venv/Scripts/python.exe checks/check_demand.py
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
import macro as m  # noqa: E402

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


with open(os.path.join(ROOT, "results", "demand.json"), encoding="utf-8") as f:
    R = json.load(f)
cyc = R["sweden_cycle"]
base = dm.Demand(kappa=cyc["kappa_per_pp_output_gap"], okun=cyc["okun"])
W = {name: dm.world(br, truth) for name, (br, truth) in bs.SCEN.items()}
S = R["scenarios"]
C = "central (r* learned with a 3-year half-life)"
OSN, DDN = "owners' saving dominates", "deficits dominate"

print("M — the mechanics")
r = dm.run(W["status quo"], base)
check("M1 the status quo is a steady state: no gap, inflation on target, policy at neutral throughout",
      np.abs(r["gap"]).max() < 1e-12 and np.abs(r["inflation"] - 2.0).max() < 1e-12 and np.ptp(r["policy"]) < 1e-12)
r = dm.run(W[OSN], replace(base, h=1e-6, smooth=0.0, elb=-99.0))
check("M2 a central bank that knows r* at once, without smoothing or a floor, keeps the gap near zero as r* falls",
      np.abs(r["gap"]).max() < 0.3, f"largest gap {np.abs(r['gap']).max():.3f}%")
for name in (DDN, OSN):
    g = [abs(S[f"{name} | {v}"]["gap_min_and_year"][0]) for v in ("fast learning (1 year)", C, "slow learning (8 years, pre-2021 anchors)")]
    check(f"M3 {name}: the slower the central bank learns r*, the larger the gap (1, 3, 8 years; on the refit r* falls in both branches, "
          f"so both gaps are troughs)", g[0] < g[1] < g[2], str(g))
r = dm.run(W[OSN], base)
r0 = dm.run(W[OSN], replace(base, elb=-99.0))
check("M4 the floor holds, and where it binds the gap is no smaller than without it",
      r["policy"].min() >= base.elb - 1e-12 and r0["policy"].min() < base.elb and np.all(r["gap"] <= r0["gap"] + 1e-9),
      f"policy min {r['policy'].min():.2f} (without the floor {r0['policy'].min():.2f})")
mp = W[OSN]
check("M5 the equilibrium's relative prices ride through unchanged (goods less housing inflation is the macro block's)",
      np.allclose(r["pi_goods"] - r["pi_shelter"], mp["pi_goods"] - mp["pi_shelter"]))

print("C — the calibration (Swedish data)")
check("C1 Okun: unemployment rises when growth falls, more than 3 standard errors from zero",
      cyc["okun_du_per_pp_growth"]["coef"] < 0 and abs(cyc["okun_du_per_pp_growth"]["coef"]) > 3 * cyc["okun_du_per_pp_growth"]["se"],
      str(cyc["okun_du_per_pp_growth"]))
check("C2 Phillips: core inflation falls when unemployment is above trend; kappa between 0.02 and 0.5",
      cyc["phillips_per_pp_unemployment_gap"]["coef"] < 0 and 0.02 < cyc["kappa_per_pp_output_gap"] < 0.5,
      f"{cyc['phillips_per_pp_unemployment_gap']}, kappa {cyc['kappa_per_pp_output_gap']}")

print("F — the findings (calibration (c), the central; stated as found)")
os_c, dd_c = S[f"{OSN} | {C}"], S[f"{DDN} | {C}"]
check("F1 owners' saving dominates: policy too tight on the way down — a negative gap and inflation below target",
      os_c["gap_min_and_year"][0] < -0.5 and os_c["inflation_min_max"][0] < 2.0, f"gap {os_c['gap_min_and_year']}, inflation {os_c['inflation_min_max']}")
check("F2 [restated at the refit] deficits dominate: on the refit r* falls in this branch too (keyed to investment), so policy is a "
      "little too tight on the way down — a small negative gap and inflation just below target (before the refit, too loose on the way "
      "up: a positive gap of 1.1% and inflation to 2.16%)",
      -1.0 < dd_c["gap_min_and_year"][0] < -0.3 and dd_c["gap_max_and_year"][0] == 0.0 and dd_c["inflation_min_max"][1] == 2.0
      and dd_c["inflation_min_max"][0] < 2.0, f"gap {dd_c['gap_min_and_year']}, inflation {dd_c['inflation_min_max']}")
cyc_runs = {k: v for k, v in S.items() if "2009-size" not in k}
cyc_max = max(abs(v["gap_min_and_year"][0]) for v in cyc_runs.values())
weak = {k: v for k, v in cyc_runs.items() if "weak anchor" in k}
firm = {k: v for k, v in cyc_runs.items() if "weak anchor" not in k}
lo_weak = min(v["inflation_min_max"][0] for v in weak.values())
eb_, _ = bs.economy("b")                      # (b)'s cycle runs, the same variants as demand.main, for the comparison the claim makes
VAR = {C: base, "fast learning (1 year)": replace(base, h=1.0), "slow learning (8 years, pre-2021 anchors)": replace(base, h=8.0),
       "weak anchor (expectations follow inflation)": replace(base, anchor=0.5), "no floor (counterfactual)": replace(base, elb=-99.0),
       "steeper IS (a_r 0.15)": replace(base, a_r=0.15), "flatter IS (a_r 0.05)": replace(base, a_r=0.05)}
Wb_ = {name: dm.world(br, truth, e=eb_, base=m.BRIDGES_B) for name, (br, truth) in bs.SCEN_B.items()}
cyc_b = {f"{n} | {vn}": dm.summary(dm.run(mp_, dv)) for n, mp_ in Wb_.items() for vn, dv in VAR.items()}
for n in (DDN, OSN):
    mpf_ = dm.world(bs.SCEN_B[n][0], "new", fast=True, e=eb_, base=m.BRIDGES_B)
    cyc_b |= {f"{n}, fast automation | {vn}": dm.summary(dm.run(mpf_, VAR[vn])) for vn in (C, "slow learning (8 years, pre-2021 anchors)",
                                                                                         "weak anchor (expectations follow inflation)")}
infl_b = (min(v["inflation_min_max"][0] for v in cyc_b.values()), max(v["inflation_min_max"][1] for v in cyc_b.values()))
own = {k: v for k, v in cyc_runs.items() if k.startswith(OSN)}
dfc = {k: v for k, v in cyc_runs.items() if k.startswith(DDN)}
own_floor = {k: v for k, v in own.items() if "no floor" not in k}
check("F3 [restated at the refit] the cycle is no longer normal-sized when owners' saving dominates: the gap passes -3.5% in every run "
      "with the floor (-7.2% with central learning, -9.0% with fast automation, -10.9% with a steeper IS curve, -3.6% with a flatter one), "
      "the floor binds for five years or more, inflation falls below 1.5% (below zero with a weak anchor); without the floor the gap stays under 3%. When deficits "
      "dominate the gap stays within 1.5% and inflation within 1.75-2.0%. Before the refit every (c) run stayed within 3% (inflation "
      "1.5-2.5% with a firm anchor); on (b) every run, the weak-anchor runs included, still stays within 3% and 1.5-2.5%",
      all(v["gap_min_and_year"][0] < -3.5 and v["years_at_floor"] >= 5.0 and v["inflation_min_max"][0] < 1.5 for v in own_floor.values())
      and min(v["inflation_min_max"][0] for k, v in own.items() if "weak anchor" in k) < 0.0
      and abs(S[f"{OSN} | no floor (counterfactual)"]["gap_min_and_year"][0]) < 3.0
      and all(abs(v["gap_min_and_year"][0]) < 1.5 and v["gap_max_and_year"][0] < 1.5 and 1.75 <= v["inflation_min_max"][0]
              and v["inflation_min_max"][1] <= 2.0 for v in dfc.values())
      and set(cyc_b) == set(cyc_runs) and 1.5 <= infl_b[0] and infl_b[1] <= 2.5 and max(abs(v["gap_min_and_year"][0]) for v in cyc_b.values()) < 3.0,
      f"largest gap {cyc_max:.2f}%; owners' saving, with the floor: gaps {min(v['gap_min_and_year'][0] for v in own_floor.values())} to "
      f"{max(v['gap_min_and_year'][0] for v in own_floor.values())}%, floor {min(v['years_at_floor'] for v in own_floor.values())}-"
      f"{max(v['years_at_floor'] for v in own_floor.values())} years, inflation low {min(v['inflation_min_max'][0] for v in own.values())}% "
      f"(weak anchor), {lo_weak}; deficits: gaps within {max(abs(v['gap_min_and_year'][0]) for v in dfc.values()):.2f}%; (b), "
      f"{len(cyc_b)} runs: inflation {infl_b[0]}-{infl_b[1]}%, largest gap {max(abs(v['gap_min_and_year'][0]) for v in cyc_b.values()):.2f}%")
part10 = float(np.interp(10, mp["t"], mp["participation"] / mp["participation"][0]))
mpb_ = Wb_[OSN]
part10_b = float(np.interp(10, mpb_["t"], mpb_["participation"] / mpb_["participation"][0]))
check("F4 [restated to the size found; at the refit] the structural exit dwarfs the cycle: participation about half its start by year 10 "
      "(on (b) 10%+ lower, the pre-switch claim), the cyclical unemployment rise about a point (1.2; before the refit under 1)",
      0.4 < part10 < 0.6 and os_c["unemployment_up_max"] < 1.5 and part10 < part10_b < 0.9,
      f"participation {part10:.3f} of the start ((b) {part10_b:.3f}); cyclical +{os_c['unemployment_up_max']} pp")
k_now = "status quo + a 2009-size demand shock, today's room (2.25 points) | the Riksbank's 2008 strength, weak anchor"
k_then = "status quo + a 2009-size demand shock, 2008's room (5.25 points) | the Riksbank's 2008 strength, weak anchor"
check("F5 a 2009-size shock takes today's Riksbank to the floor (not 2008's), and the gap three years on is deeper",
      S[k_now]["years_at_floor"] > 0 and S[k_then]["years_at_floor"] == 0 and S[k_now]["y3_y5_y8_y10_y12_y15"]["gap"][0] < S[k_then]["y3_y5_y8_y10_y12_y15"]["gap"][0],
      f"floor {S[k_now]['years_at_floor']} years; gap at year 3 {S[k_now]['y3_y5_y8_y10_y12_y15']['gap'][0]} against {S[k_then]['y3_y5_y8_y10_y12_y15']['gap'][0]}")
HI, CB = R["sensitivity: the high root"]["scenarios"], R["comparator: calibration (b)"]["scenarios"]
ob = CB[f"{OSN} | {C}"]
check("F6 [new on (c); restated at the refit] when owners' saving dominates the floor binds for years, and sooner: 6.75 years from year "
      "8.5 within the 15 (before the refit 4 from 11.25; on (b) 1.25 from year 14)",
      os_c["years_at_floor"] >= 6.0 and os_c["first_year_at_floor"] < 9 and ob["years_at_floor"] < 2 and ob["first_year_at_floor"] > 13,
      f"{os_c['years_at_floor']} years from {os_c['first_year_at_floor']}; (b) {ob['years_at_floor']} from {ob['first_year_at_floor']}; "
      f"fast automation {S[OSN + ', fast automation | ' + C]['years_at_floor']} from {S[OSN + ', fast automation | ' + C]['first_year_at_floor']} "
      f"((b) {CB[OSN + ', fast automation | ' + C]['years_at_floor']})")

print("R — the neutral rate: the refit's bridge and its readout keyed back to the pace of tasks (a readout, not a finding)")
e, cal = bs.economy("lo")
eb, _ = bs.economy("b")
worst = 0.0
for name, (bridges, truth) in list(bs.SCEN.items()) + [("default bridges", ({}, "new"))]:
    for fast in (False, True):
        mp_ = dm.world(bridges, truth, fast=fast, e=e)
        br = m.feedback_bridges(e, **bridges)
        rebuilt = (br.r0_star + dm.capex_term(mp_, br) - br.alpha_rent * (mp_["nonwage_share"] - mp_["nonwage_share"][0])
                   + br.alpha_fiscal * (mp_["deficit"] - mp_["deficit"][0]))
        worst = max(worst, float(np.max(np.abs(rebuilt - mp_["r_star"]))))
inv0 = dm.investment_income(W[DDN], e)[0]
check("R1 the readout's pieces are the macro block's: r* = r0 + capex_term (on the refit alpha_inv x the change in investment / income) "
      "- alpha_rent (non-wage share) + alpha_fiscal (deficit) on every (c) world, medium and fast, and investment / income at the start is "
      "solve's inv_income",
      worst < 1e-12 and abs(inv0 / 100 - m.solve(e)["inv_income"]) < 1e-15, f"largest gap {worst:.1e}; investment {inv0:.3f}% of income")
ab = dm.alpha_inv_bridge(eb)
qb = m.solve(eb)
x_, a_ = qb["x"], eb.a * eb.delta
Jx, gx = eb.J(x_), eb.gamma(x_)
den = eb.h + eb.b * eb.delta * Jx / (1 - a_)
Yp = -eb.T * eb.b * eb.delta * gx / (1 - a_) / den ** 2
dKdx = (Yp * Jx + (eb.T / den) * gx) / (1 - a_)
per_pp = qb["Vm"] * dKdx * 0.01 / qb["income"] * 100
check("R2 the scales: the refit's (alpha_inv = macro.NEUTRAL_SCALE) and, for (b)'s readout, the bridge's (alpha_capex 0.25 over the net "
      "investment that moving 1 pp of tasks a year needs at (b)'s start — recomputed in closed form, dK/dx = (Y' J + Y gamma)/(1 - a delta)) "
      "and the demand layer's ((1 - a1)/a_r)",
      abs(ab["net_investment_pct_income_per_pp_tasks_a_year"] / per_pp - 1) < 1e-6 and abs(ab["alpha_inv"] - 0.25 / per_pp) < 1e-8
      and abs(dm.alpha_inv_is(dm.Demand()) - 0.6) < 1e-12 and R["neutral_rate_rekeyed"]["alpha_inv"]["bridge scale"] == ab
      and R["neutral_rate_rekeyed"]["alpha_inv"]["central (c)"] == m.NEUTRAL_SCALE,
      f"{per_pp:.4f}% of income per pp of tasks a year -> {ab['alpha_inv']:.4f}; demand layer {dm.alpha_inv_is(dm.Demand()):.2f}")
NR = R["neutral_rate_rekeyed"]
TK, BSC, DSC = "task keyed (the bridge as set)", "investment keyed, bridge scale", "investment keyed, demand-layer scale"
IV, PK = "investment keyed (the refit)", "pace keyed (as tuned on (b))"
cc, bb = NR["central (c)"], NR["comparator: calibration (b)"]
DEF = "default bridges (the macro block's own r*)"
lower15 = all(v["r_star"][IV]["15"] < v["r_star"][PK]["15"] for v in cc.values())
inv_falls = all(v["inv_income_pct"]["15"] < v["inv_income_pct"]["0"] - 10 for v in cc.values())
check("R3 [restated at the refit] keyed to investment spending (the refit) — which on (c) falls by about 13 points of income by year 15 on "
      "every path — r* never rises above its start in any (c) world and is lower at year 15 in every one than keyed back to the pace of "
      "tasks; keyed to the pace, the deficits branch rises again (to about 2.9% at year 15, against -1.1% on the refit) and the default "
      "world barely rises; on (b) the readout as before the refit: the hump survives only at the demand layer's scale",
      lower15 and inv_falls and all(v["r_star_rise_above_start_to_15_pp"][IV] <= 1e-12 for v in cc.values())
      and cc[DDN]["r_star_rise_above_start_to_15_pp"][PK] > 2.0 and 2.5 < cc[DDN]["r_star"][PK]["15"] and cc[DDN]["r_star"][IV]["15"] < -1.0
      and cc[DEF]["r_star_rise_above_start_to_15_pp"][PK] < 0.1
      and bb[DEF]["r_star_rise_above_start_to_15_pp"][BSC] <= 1e-12 and bb[DEF]["r_star_rise_above_start_to_15_pp"][DSC] > 0.0,
      f"inv/income {cc[DDN]['inv_income_pct']['0']:.1f} -> {cc[DDN]['inv_income_pct']['15']:.1f}% (deficits); r* at year 15, investment / "
      f"pace keyed: default {cc[DEF]['r_star'][IV]['15']:.2f} / {cc[DEF]['r_star'][PK]['15']:.2f}, deficits {cc[DDN]['r_star'][IV]['15']:.2f} / "
      f"{cc[DDN]['r_star'][PK]['15']:.2f}, owners {cc[OSN]['r_star'][IV]['15']:.2f} / {cc[OSN]['r_star'][PK]['15']:.2f}; deficits' rise keyed to "
      f"the pace {cc[DDN]['r_star_rise_above_start_to_15_pp'][PK]:.2f} pp; (b) default max {[round(x, 2) for x in bb[DEF]['r_star_max_and_year_to_15'][TK]]} / "
      f"{[round(x, 2) for x in bb[DEF]['r_star_max_and_year_to_15'][BSC]]} / {[round(x, 2) for x in bb[DEF]['r_star_max_and_year_to_15'][DSC]]}")
dl = lambda w, s_: cc[w]["demand_layer"][s_]  # noqa: E731
check("R4 [restated at the refit] the demand layer on those r* paths: keyed back to the pace, the deficits branch is a mild boom again "
      "(+0.8%, inflation above target) and the owners'-saving gap a third the size (-2.3%); keyed to investment (the refit) the deficits "
      "branch is a small slump and the owners'-saving gap -7.2%, at the floor for 6.75 years — the cycle's size and the branches' split "
      "rest on the capex key",
      dl(DDN, PK)["gap_max_and_year"][0] > 0.3 and dl(DDN, PK)["inflation_min_max"][1] > 2.0 and dl(DDN, IV)["gap_max_and_year"][0] == 0.0
      and dl(DDN, IV)["gap_min_and_year"][0] < 0.0 and dl(OSN, IV)["gap_min_and_year"][0] < 2.5 * dl(OSN, PK)["gap_min_and_year"][0] < 0.0
      and dl(OSN, IV)["years_at_floor"] > dl(OSN, PK)["years_at_floor"],
      f"deficits gap {dl(DDN, IV)['gap_min_and_year'][0]} (investment) / +{dl(DDN, PK)['gap_max_and_year'][0]} (pace), inflation high "
      f"{dl(DDN, PK)['inflation_min_max'][1]}; owners' saving gap {dl(OSN, IV)['gap_min_and_year'][0]} / {dl(OSN, PK)['gap_min_and_year'][0]}, "
      f"floor {dl(OSN, IV)['years_at_floor']} / {dl(OSN, PK)['years_at_floor']} years")
alphas = {"bridge scale": ab["alpha_inv"], "demand-layer scale": dm.alpha_inv_is(dm.Demand())}
fresh_c = json.loads(json.dumps(dm.neutral_rate_readout(e, base, None, "lo")))
fresh_b = json.loads(json.dumps(dm.neutral_rate_readout(eb, base, alphas, "b")))
check("R5 the stored readout equals a fresh rebuild, on (c) and (b)", fresh_c == cc and fresh_b == bb, f"{len(cc)} + {len(bb)} worlds")
NI = "net_investment_pct_income_diagnostic"
mp_d = dm.world(*bs.SCEN[DDN], e=e)
ni_gap = float(np.max(np.abs(dm.net_investment_income(mp_d) - mp_d["Vm"] * np.gradient(mp_d["K"], mp_d["t"]) / mp_d["income"] * 100)))
k_falls = all(K_[int(round(10 / 0.25))] < 0.5 * K_[0] for K_ in (dm.world(*wd, fast=f_, e=ec, base=bb_)["K"]
              for ec, bb_, sc_ in ((e, None, bs.SCEN), (eb, m.BRIDGES_B, bs.SCEN_B))
              for wd in (({}, "new"), sc_[DDN], sc_[OSN]) for f_ in (False, True)))
troughs = [v["net_investment_min_and_year_to_15"][0] for v in list(cc.values()) + list(bb.values())]
check("R6 [readout] the series keyed to is replacement investment; net investment (Vm dK/dt / income, a diagnostic outside the quasi-static "
      "accounts) is negative through every deep build-out on (c) and on (b) — the machine stock K falls by more than half by year 10 as "
      "capability makes each machine do more — so keying to investment including it would lower r* further, not less",
      ni_gap < 1e-12 and k_falls and all(v[NI][str(y)] < 0 for v in list(cc.values()) + list(bb.values()) for y in (3, 5))
      and max(troughs) < -40.0,
      f"troughs {min(troughs):.0f} to {max(troughs):.0f}% of income a year; (c) deficits medium {cc[DDN][NI]['3']:.1f} / {cc[DDN][NI]['5']:.1f} / "
      f"{cc[DDN][NI]['8']:.1f}% at years 3 / 5 / 8 against replacement {cc[DDN]['inv_income_pct']['3']:.1f} / {cc[DDN]['inv_income_pct']['5']:.1f} / "
      f"{cc[DDN]['inv_income_pct']['8']:.1f}%")

print("X — the switch: (c)'s runs, the (b) comparator, the high root")
fresh = {}
for name, mp_ in W.items():
    fresh[f"{name} | {C}"] = dm.summary(dm.run(mp_, base))
for name in (DDN, OSN):
    fresh[f"{name}, fast automation | {C}"] = dm.summary(dm.run(dm.world(bs.SCEN[name][0], "new", fast=True), base))
check("X1 demand.json's central-learning runs equal a fresh rebuild on macro.central(), and its calibration record is the central's",
      all(json.loads(json.dumps(v)) == S[k] for k, v in fresh.items()) and R["calibration"] == json.loads(json.dumps(cal)),
      f"{len(fresh)} runs; {cal['tag']}")


def world_b_old(bridges, truth, fast=False):
    """The pre-switch demand.world, with (b)'s hard-coded objects."""
    br = replace(m.BRIDGES_B, capital_premium=5.0, **bridges)
    if truth != "new":
        tech = m.TechPath(eta_end=1.0, lam_end=eb.lam)
    else:
        tech = m.TechPath(eta_end=0.04, lam_end=0.01, t_mid=3, width=2) if fast else m.TechPath(eta_end=0.04, lam_end=0.01, t_mid=6, width=6)
    return m.macro_path(eb, tech, br, 25.0, 0.25)


old_b = {f"{name} | {C}": dm.summary(dm.run(world_b_old(br, truth), base)) for name, (br, truth) in bs.SCEN_B.items()}
old_b |= {f"{name}, fast automation | {C}": dm.summary(dm.run(world_b_old(bs.SCEN_B[name][0], "new", fast=True), base)) for name in (DDN, OSN)}
check("X2 the (b) comparator is the pre-switch layer: rebuilt with (b)'s hard-coded Bridges(capital_premium=5.0) and TechPaths it equals the "
      "stored comparator run for run", all(json.loads(json.dumps(v)) == CB[k] for k, v in old_b.items()) and len(old_b) == len(CB) == 5,
      f"{len(old_b)} runs; owners' saving gap {CB[OSN + ' | ' + C]['gap_min_and_year']} (b)")
ho, hd = HI[f"{OSN} | {C}"], HI[f"{DDN} | {C}"]
check("X3 [restated at the refit] sensitivity, the high root: F1, F2 (restated: the deficits branch a small slump) and F6's floor hold "
      "there too",
      ho["gap_min_and_year"][0] < -0.5 and ho["inflation_min_max"][0] < 2.0 and -1.0 < hd["gap_min_and_year"][0] < -0.3
      and hd["gap_max_and_year"][0] == 0.0 and hd["inflation_min_max"][0] < 2.0 and ho["years_at_floor"] > ob["years_at_floor"],
      f"owners' saving gap {ho['gap_min_and_year']}, inflation {ho['inflation_min_max']}, floor {ho['years_at_floor']} years; deficits gap "
      f"{hd['gap_min_and_year']}, inflation {hd['inflation_min_max']}")

n_ok = sum(ok for _, ok, _ in RESULTS)
fails = [n for n, ok, _ in RESULTS if not ok]
print(f"\n{n_ok}/{len(RESULTS)} checks passed")
print(f"ALL GREEN ({len(RESULTS)})" if not fails else "FAILURES: " + "; ".join(n.split(" ")[0] for n in fails))
sys.exit(0 if n_ok == len(RESULTS) else 1)
