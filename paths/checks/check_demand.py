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
    g = [abs(S[f"{name} | {v}"]["gap_min_and_year" if "owners" in name else "gap_max_and_year"][0]) for v in
         ("fast learning (1 year)", C, "slow learning (8 years, pre-2021 anchors)")]
    check(f"M3 {name}: the slower the central bank learns r*, the larger the gap (1, 3, 8 years)", g[0] < g[1] < g[2], str(g))
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
check("F2 deficits dominate: policy too loose on the way up — a positive gap and inflation above target",
      dd_c["gap_max_and_year"][0] > 0.3 and dd_c["inflation_min_max"][1] > 2.0, f"gap {dd_c['gap_max_and_year']}, inflation {dd_c['inflation_min_max']}")
cyc_runs = {k: v for k, v in S.items() if "2009-size" not in k}
cyc_max = max(abs(v["gap_min_and_year"][0]) for v in cyc_runs.values())
weak = {k: v for k, v in cyc_runs.items() if "weak anchor" in k}
firm = {k: v for k, v in cyc_runs.items() if "weak anchor" not in k}
lo_weak = min(v["inflation_min_max"][0] for v in weak.values())
eb_, _ = bs.economy("b")                      # (b)'s cycle runs, the same variants as demand.main, for the comparison the claim makes
VAR = {C: base, "fast learning (1 year)": replace(base, h=1.0), "slow learning (8 years, pre-2021 anchors)": replace(base, h=8.0),
       "weak anchor (expectations follow inflation)": replace(base, anchor=0.5), "no floor (counterfactual)": replace(base, elb=-99.0),
       "steeper IS (a_r 0.15)": replace(base, a_r=0.15), "flatter IS (a_r 0.05)": replace(base, a_r=0.05)}
Wb_ = {name: dm.world(br, truth, e=eb_) for name, (br, truth) in bs.SCEN.items()}
cyc_b = {f"{n} | {vn}": dm.summary(dm.run(mp_, dv)) for n, mp_ in Wb_.items() for vn, dv in VAR.items()}
for n in (DDN, OSN):
    mpf_ = dm.world(bs.SCEN[n][0], "new", fast=True, e=eb_)
    cyc_b |= {f"{n}, fast automation | {vn}": dm.summary(dm.run(mpf_, VAR[vn])) for vn in (C, "slow learning (8 years, pre-2021 anchors)",
                                                                                         "weak anchor (expectations follow inflation)")}
infl_b = (min(v["inflation_min_max"][0] for v in cyc_b.values()), max(v["inflation_min_max"][1] for v in cyc_b.values()))
check("F3 [restated] on the paper's paths, even fast automation with slow learning keeps the cycle normal-sized: gaps within 3%, headline "
      "inflation 1.5-2.5% — except with a weak anchor, where it falls below 1.5% (to 1.28; the check's 1.25 under it is a regression "
      "guard, not the claim); on (b) every run, the weak-anchor runs included, stayed within 1.5-2.5%",
      cyc_max < 3.0 and all(1.5 <= v["inflation_min_max"][0] and v["inflation_min_max"][1] <= 2.5 for v in firm.values())
      and all(1.25 <= v["inflation_min_max"][0] and v["inflation_min_max"][1] <= 2.5 for v in weak.values()) and lo_weak < 1.5
      and set(cyc_b) == set(cyc_runs) and 1.5 <= infl_b[0] and infl_b[1] <= 2.5 and max(abs(v["gap_min_and_year"][0]) for v in cyc_b.values()) < 3.0,
      f"largest gap {cyc_max:.2f}%; inflation {min(v['inflation_min_max'][0] for v in firm.values())}-"
      f"{max(v['inflation_min_max'][1] for v in firm.values())}% with a firm anchor, {lo_weak}-"
      f"{max(v['inflation_min_max'][1] for v in weak.values())}% with a weak one; (b), "
      f"{len(cyc_b)} runs: inflation {infl_b[0]}-{infl_b[1]}%, largest gap {max(abs(v['gap_min_and_year'][0]) for v in cyc_b.values()):.2f}%")
part10 = float(np.interp(10, mp["t"], mp["participation"] / mp["participation"][0]))
mpb_ = Wb_[OSN]
part10_b = float(np.interp(10, mpb_["t"], mpb_["participation"] / mpb_["participation"][0]))
check("F4 [restated to the size found] the structural exit dwarfs the cycle: participation about half its start by year 10 (on (b) 10%+ "
      "lower, the pre-switch claim), the cyclical unemployment rise under 1 point",
      0.4 < part10 < 0.6 and os_c["unemployment_up_max"] < 1.0 and part10 < part10_b < 0.9,
      f"participation {part10:.3f} of the start ((b) {part10_b:.3f}); cyclical +{os_c['unemployment_up_max']} pp")
k_now = "status quo + a 2009-size demand shock, today's room (2.25 points) | the Riksbank's 2008 strength, weak anchor"
k_then = "status quo + a 2009-size demand shock, 2008's room (5.25 points) | the Riksbank's 2008 strength, weak anchor"
check("F5 a 2009-size shock takes today's Riksbank to the floor (not 2008's), and the gap three years on is deeper",
      S[k_now]["years_at_floor"] > 0 and S[k_then]["years_at_floor"] == 0 and S[k_now]["y3_y5_y8_y10_y12_y15"]["gap"][0] < S[k_then]["y3_y5_y8_y10_y12_y15"]["gap"][0],
      f"floor {S[k_now]['years_at_floor']} years; gap at year 3 {S[k_now]['y3_y5_y8_y10_y12_y15']['gap'][0]} against {S[k_then]['y3_y5_y8_y10_y12_y15']['gap'][0]}")
HI, CB = R["sensitivity: the high root"]["scenarios"], R["comparator: calibration (b)"]["scenarios"]
ob = CB[f"{OSN} | {C}"]
check("F6 [new on (c)] when owners' saving dominates the floor binds for years, and sooner: 4 years from year 11.25 within the 15 "
      "(on (b) 1.25 from year 14)",
      os_c["years_at_floor"] >= 3.5 and os_c["first_year_at_floor"] < 12 and ob["years_at_floor"] < 2 and ob["first_year_at_floor"] > 13,
      f"{os_c['years_at_floor']} years from {os_c['first_year_at_floor']}; (b) {ob['years_at_floor']} from {ob['first_year_at_floor']}; "
      f"fast automation {S[OSN + ', fast automation | ' + C]['years_at_floor']} from {S[OSN + ', fast automation | ' + C]['first_year_at_floor']} "
      f"((b) {CB[OSN + ', fast automation | ' + C]['years_at_floor']})")

print("R — the neutral rate: the bridge and its readout keyed to investment spending (a sensitivity, not a finding)")
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
check("R1 the readout's pieces are the macro block's: r* = r0 + capex_term - alpha_rent (non-wage share) + alpha_fiscal (deficit) on every "
      "(c) world, medium and fast, and investment / income at the start is solve's inv_income",
      worst < 1e-12 and abs(inv0 / 100 - m.solve(e)["inv_income"]) < 1e-15, f"largest gap {worst:.1e}; investment {inv0:.3f}% of income")
ab = dm.alpha_inv_bridge(eb)
qb = m.solve(eb)
x_, a_ = qb["x"], eb.a * eb.delta
Jx, gx = eb.J(x_), eb.gamma(x_)
den = eb.h + eb.b * eb.delta * Jx / (1 - a_)
Yp = -eb.T * eb.b * eb.delta * gx / (1 - a_) / den ** 2
dKdx = (Yp * Jx + (eb.T / den) * gx) / (1 - a_)
per_pp = qb["Vm"] * dKdx * 0.01 / qb["income"] * 100
check("R2 the two scales: the bridge's (alpha_capex 0.25 over the net investment that moving 1 pp of tasks a year needs at (b)'s start — "
      "recomputed in closed form, dK/dx = (Y' J + Y gamma)/(1 - a delta)) and the demand layer's ((1 - a1)/a_r)",
      abs(ab["net_investment_pct_income_per_pp_tasks_a_year"] / per_pp - 1) < 1e-6 and abs(ab["alpha_inv"] - 0.25 / per_pp) < 1e-8
      and abs(dm.alpha_inv_is(dm.Demand()) - 0.6) < 1e-12 and R["neutral_rate_invest_keyed"]["alpha_inv"]["bridge scale"] == ab,
      f"{per_pp:.4f}% of income per pp of tasks a year -> {ab['alpha_inv']:.4f}; demand layer {dm.alpha_inv_is(dm.Demand()):.2f}")
NR = R["neutral_rate_invest_keyed"]
TK, BSC, DSC = "task keyed (the bridge as set)", "investment keyed, bridge scale", "investment keyed, demand-layer scale"
cc, bb = NR["central (c)"], NR["comparator: calibration (b)"]
DEF = "default bridges (the macro block's own r*)"
lower15 = all(w[s_]["15"] < w[TK]["15"] for w in (v["r_star"] for v in cc.values()) for s_ in (BSC, DSC))
inv_falls = all(v["inv_income_pct"]["15"] < v["inv_income_pct"]["0"] - 10 for v in cc.values())
check("R3 [readout] keyed to investment spending — which on (c) falls by about 13 points of income by year 15 on every path — r* is lower at year "
      "15 in every (c) world at both scales; the default bridges' rise disappears (fast: +0.54 pp at year 3.75 -> none); deficits still "
      "lift r* at the bridge's scale (3.3 against 3.9 at year 15) and lower it at the demand layer's (-4.2); on (b) the hump survives only "
      "at the demand layer's scale",
      lower15 and inv_falls and all(cc[k]["r_star_rise_above_start_to_15_pp"][s_] <= 1e-12 for k in (DEF, DEF + ", fast automation") for s_ in (BSC, DSC))
      and cc[DEF + ", fast automation"]["r_star_rise_above_start_to_15_pp"][TK] > 0.5
      and 3.0 < cc[DDN]["r_star"][BSC]["15"] < cc[DDN]["r_star"][TK]["15"] and cc[DDN]["r_star"][DSC]["15"] < -4.0
      and bb[DEF]["r_star_rise_above_start_to_15_pp"][BSC] <= 1e-12 and bb[DEF]["r_star_rise_above_start_to_15_pp"][DSC] > 0.0,
      f"inv/income {cc[DDN]['inv_income_pct']['0']:.1f} -> {cc[DDN]['inv_income_pct']['15']:.1f}% (deficits); default fast rise "
      f"{cc[DEF + ', fast automation']['r_star_rise_above_start_to_15_pp'][TK]:.2f} -> {cc[DEF + ', fast automation']['r_star_rise_above_start_to_15_pp'][BSC]:.2f} / "
      f"{cc[DEF + ', fast automation']['r_star_rise_above_start_to_15_pp'][DSC]:.2f}; deficits y15 {cc[DDN]['r_star'][TK]['15']:.2f} / "
      f"{cc[DDN]['r_star'][BSC]['15']:.2f} / {cc[DDN]['r_star'][DSC]['15']:.2f}; owners y15 {cc[OSN]['r_star'][TK]['15']:.2f} / "
      f"{cc[OSN]['r_star'][BSC]['15']:.2f} / {cc[OSN]['r_star'][DSC]['15']:.2f}; (b) default max {[round(x, 2) for x in bb[DEF]['r_star_max_and_year_to_15'][TK]]} / "
      f"{[round(x, 2) for x in bb[DEF]['r_star_max_and_year_to_15'][BSC]]} / {[round(x, 2) for x in bb[DEF]['r_star_max_and_year_to_15'][DSC]]}")
dl = lambda w, s_: cc[w]["demand_layer"][s_]  # noqa: E731
check("R4 [readout] the demand layer on those r* paths: at the bridge's scale the findings keep their signs (owners' saving deeper, "
      "-2.7%; deficits +0.8%); at the demand layer's scale the deficits branch turns to a slump at the floor and the owners'-saving "
      "gap leaves the normal range (-12%, inflation 0.3%) — the cycle's size rests on the capex key",
      dl(OSN, BSC)["gap_min_and_year"][0] < dl(OSN, TK)["gap_min_and_year"][0] and dl(DDN, BSC)["gap_max_and_year"][0] > 0.3
      and dl(DDN, DSC)["gap_min_and_year"][0] < -2.0 and dl(DDN, DSC)["years_at_floor"] > 3.0 and dl(DDN, DSC)["gap_max_and_year"][0] == 0.0
      and dl(OSN, DSC)["gap_min_and_year"][0] < -10.0 and dl(OSN, DSC)["inflation_min_max"][0] < 0.5,
      f"owners' saving gap {dl(OSN, TK)['gap_min_and_year'][0]} / {dl(OSN, BSC)['gap_min_and_year'][0]} / {dl(OSN, DSC)['gap_min_and_year'][0]}, "
      f"inflation low {dl(OSN, DSC)['inflation_min_max'][0]}, floor {dl(OSN, TK)['years_at_floor']} / {dl(OSN, BSC)['years_at_floor']} / "
      f"{dl(OSN, DSC)['years_at_floor']} years; deficits gap {dl(DDN, TK)['gap_max_and_year'][0]} / {dl(DDN, BSC)['gap_max_and_year'][0]} / "
      f"{dl(DDN, DSC)['gap_min_and_year'][0]} (floor {dl(DDN, DSC)['years_at_floor']} years)")
alphas = {"bridge scale": ab["alpha_inv"], "demand-layer scale": dm.alpha_inv_is(dm.Demand())}
fresh_c = json.loads(json.dumps(dm.neutral_rate_readout(e, base, alphas)))
fresh_b = json.loads(json.dumps(dm.neutral_rate_readout(eb, base, alphas)))
check("R5 the stored readout equals a fresh rebuild, on (c) and (b)", fresh_c == cc and fresh_b == bb, f"{len(cc)} + {len(bb)} worlds")
NI = "net_investment_pct_income_diagnostic"
mp_d = dm.world(*bs.SCEN[DDN], e=e)
ni_gap = float(np.max(np.abs(dm.net_investment_income(mp_d) - mp_d["Vm"] * np.gradient(mp_d["K"], mp_d["t"]) / mp_d["income"] * 100)))
k_falls = all(K_[int(round(10 / 0.25))] < 0.5 * K_[0] for K_ in (dm.world(*wd, fast=f_, e=ec)["K"]
              for wd in (({}, "new"), bs.SCEN[DDN], bs.SCEN[OSN]) for f_ in (False, True) for ec in (e, eb)))
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
    br = m.Bridges(capital_premium=5.0, **bridges)
    if truth != "new":
        tech = m.TechPath(eta_end=1.0, lam_end=eb.lam)
    else:
        tech = m.TechPath(eta_end=0.04, lam_end=0.01, t_mid=3, width=2) if fast else m.TechPath(eta_end=0.04, lam_end=0.01, t_mid=6, width=6)
    return m.macro_path(eb, tech, br, 25.0, 0.25)


old_b = {f"{name} | {C}": dm.summary(dm.run(world_b_old(br, truth), base)) for name, (br, truth) in bs.SCEN.items()}
old_b |= {f"{name}, fast automation | {C}": dm.summary(dm.run(world_b_old(bs.SCEN[name][0], "new", fast=True), base)) for name in (DDN, OSN)}
check("X2 the (b) comparator is the pre-switch layer: rebuilt with (b)'s hard-coded Bridges(capital_premium=5.0) and TechPaths it equals the "
      "stored comparator run for run", all(json.loads(json.dumps(v)) == CB[k] for k, v in old_b.items()) and len(old_b) == len(CB) == 5,
      f"{len(old_b)} runs; owners' saving gap {CB[OSN + ' | ' + C]['gap_min_and_year']} (b)")
ho, hd = HI[f"{OSN} | {C}"], HI[f"{DDN} | {C}"]
check("X3 sensitivity, the high root: F1, F2 and F6's floor hold there too",
      ho["gap_min_and_year"][0] < -0.5 and ho["inflation_min_max"][0] < 2.0 and hd["gap_max_and_year"][0] > 0.3 and hd["inflation_min_max"][1] > 2.0
      and ho["years_at_floor"] > ob["years_at_floor"],
      f"owners' saving gap {ho['gap_min_and_year']}, inflation {ho['inflation_min_max']}, floor {ho['years_at_floor']} years; deficits gap "
      f"{hd['gap_max_and_year']}, inflation {hd['inflation_min_max']}")

n_ok = sum(ok for _, ok, _ in RESULTS)
fails = [n for n, ok, _ in RESULTS if not ok]
print(f"\n{n_ok}/{len(RESULTS)} checks passed")
print(f"ALL GREEN ({len(RESULTS)})" if not fails else "FAILURES: " + "; ".join(n.split(" ")[0] for n in fails))
sys.exit(0 if n_ok == len(RESULTS) else 1)
