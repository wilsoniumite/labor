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
# refit's numbers (flagged): F2's -0.3 / -1.0, F3's -3.5 and 1.5 / 1.75, F4's 1.5, F6's 6 and 9, R3's and R4's bands. Narrow at the
# refit and unnamed then (checks:N1): F3's no-floor gap -2.90 against the pre-refit 3% (a pre-refit claim surviving by 0.10); F3's
# deficits inflation low 1.78 against 1.75; F4's participation at year 10 0.428 against 0.4; F6's first floor year 8.5 against 9;
# R3's deficits pace-keyed rise 2.15 against 2.0; R4's pace-keyed deficits inflation high 2.11 against 2.0.
# Restated at the revision (2026-10-28, Log 54; decisions 93-96: the investment key at Rachel and Smith's coefficient times its
# pass-through, every coefficient per point of income, the start net of the state's asset income, the debt's rate floored, and on
# these feedback worlds the bridges read at the start's required return). Set in advance: R1 (r* is r0 plus the three terms the
# bridge added, stored by macro_path, and on the refit's feedback worlds the fixed-return r* at the start's return — the old rebuild
# from the path's own series no longer applies, off by up to 0.33 pp) and R2 (alpha_inv is macro.Bridges()'s, the investment key,
# no longer macro.NEUTRAL_SCALE). Restated after seeing the revision's results (its planning runs count as seeing; flagged, old ->
# new): F3 (with the floor the owners'-saving gap passed -3.5% in every run, inflation fell below 1.5% in every run and below zero
# with a weak anchor -> the flatter IS curve's gap is -2.35% with inflation down to 1.66%, so: every run past -2%, all but the flatter
# IS curve past -3.5%, inflation below 1.7% in every run and below 1.5% in all but that one, below 1% with a weak anchor, 0.66%; 0.21%
# on the fast path); F6's first year (8.5 against < 9 -> 9.25 against < 9.5); R3 (the deficits branch's pace-keyed rise 2.15 against
# > 2.0 -> 1.37 against > 1.25; its pace-keyed r* at year 15 2.9 against > 2.5 -> 2.07 against > 1.75; its investment-keyed r* at year
# 15 -1.1 against < -1.0 -> -0.28 against < 0); F4's cyclical rise tightened with its label (about a point, 1.2 against < 1.5 -> under
# a point, 0.78 against < 1.0). R4's label carries the moved numbers, its gate unchanged. Narrow passes: F2's deficits gap -0.35
# inside (-1.0, -0.3); F3's floor clause, slow learning 5.0 years against >= 5.0 (zero margin); F6's years, 6.0 against >= 6.0 (zero
# margin). Narrow passes named later (2026-10-28, the record's corrections against the final results, checks:N1 recomputed):
# F3's "inflation below 1.7% in every run", the flatter IS curve's 1.66 against 1.7 (set after seeing); F3's deficits inflation low
# 1.88 against 1.75; F6's first year 9.25 against < 9.5 (one quarter); R3's pace-keyed deficits rise 1.37 against > 1.25; R4's
# pace-keyed deficits inflation high 2.07 against > 2.0. Of the six checks:N1 named at the refit, F3's no-floor gap (-2.23 against
# 3%) and F4's participation (0.464 against 0.4) are no longer narrow.
# Restated at the verification (2026-10-28, Log 54's last bullet; the verifiers' findings, flagged): M3's and F2's labels say "at the
# gross reading of the investment key (the central)", their gates unchanged (her call (1) wants claims that rest on the pass-through
# stated conditionally); R7 new, set after seeing, a readout as bank R7 is: the deficits branch at a pass-through of 1 / 0.6 / 0.4 /
# 0, its gap's low -0.35 / -0.05 / 0.00 / 0.00 and high 0.00 / +0.02 / +0.11 / +0.42%, a slump at gross turning to a mild boom netted;
# the owners'-saving branch a slump at the floor at both ends (netted -1.77%, 4.5 years at the floor); gated on the found direction.
# X1 extended to every stored scenario (43, where it rebuilt the 5 central-learning runs) and to the high-root block, which F3 and X3
# gate (the stored blocks were equal to the code before the extension: a coverage gap, not stale data).
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
    check(f"M3 {name}: the slower the central bank learns r*, the larger the gap (1, 3, 8 years; at the gross reading of the investment key, "
          f"the central, r* falls in both branches, so both gaps are troughs; below a pass-through of about 0.6 the deficits branch's r* "
          f"rises: R7)", g[0] < g[1] < g[2], str(g))
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
check("F2 [restated at the refit; its label at the verification] deficits dominate: at the gross reading of the investment key (the "
      "central) r* falls in this branch too (keyed to investment), so policy is a little too tight on the way down — a small negative gap "
      "and inflation just below target (before the refit, too loose on the way up: a positive gap of 1.1% and inflation to 2.16%; below a "
      "pass-through of about 0.6 a mild boom again: R7)",
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
FLAT = f"{OSN} | flatter IS (a_r 0.05)"
check("F3 [restated at the refit and at the revision] the cycle is no longer normal-sized when owners' saving dominates: with the floor "
      "the gap passes -2% in every run and -3.5% in all but the flatter IS curve's (-4.65% with central learning, -5.75% with fast "
      "automation, -6.9% with a steeper IS curve, -2.35% with a flatter one; at the refit -7.2 / -9.0 / -10.9 / -3.6), the floor binds for "
      "five years or more, inflation falls below 1.7% in every run and below 1.5% in all but the flatter IS curve's, below 1% with a weak "
      "anchor (at the refit below zero); without the floor the gap stays under 3%. When deficits dominate the gap stays within 1.5% and "
      "inflation within 1.75-2.0%. Before the refit every (c) run stayed within 3% (inflation 1.5-2.5% with a firm anchor); on (b) every "
      "run, the weak-anchor runs included, still stays within 3% and 1.5-2.5%",
      all(v["gap_min_and_year"][0] < -2.0 and v["years_at_floor"] >= 5.0 and v["inflation_min_max"][0] < 1.7 for v in own_floor.values())
      and all(v["gap_min_and_year"][0] < -3.5 and v["inflation_min_max"][0] < 1.5 for k, v in own_floor.items() if k != FLAT)
      and max(v["inflation_min_max"][0] for k, v in own.items() if "weak anchor" in k) < 1.0
      and abs(S[f"{OSN} | no floor (counterfactual)"]["gap_min_and_year"][0]) < 3.0
      and all(abs(v["gap_min_and_year"][0]) < 1.5 and v["gap_max_and_year"][0] < 1.5 and 1.75 <= v["inflation_min_max"][0]
              and v["inflation_min_max"][1] <= 2.0 for v in dfc.values())
      and set(cyc_b) == set(cyc_runs) and 1.5 <= infl_b[0] and infl_b[1] <= 2.5 and max(abs(v["gap_min_and_year"][0]) for v in cyc_b.values()) < 3.0,
      f"largest gap {cyc_max:.2f}%; owners' saving, with the floor: gaps {min(v['gap_min_and_year'][0] for v in own_floor.values())} to "
      f"{max(v['gap_min_and_year'][0] for v in own_floor.values())}%, floor {min(v['years_at_floor'] for v in own_floor.values())}-"
      f"{max(v['years_at_floor'] for v in own_floor.values())} years, inflation lows {min(v['inflation_min_max'][0] for v in own.values())} to "
      f"{max(v['inflation_min_max'][0] for v in own_floor.values())}% (the flatter IS curve {S[FLAT]['inflation_min_max'][0]}%), with a weak anchor "
      + " / ".join(str(v["inflation_min_max"][0]) for k, v in own.items() if "weak anchor" in k) + f"%; the next largest gap "
      f"{max(v['gap_min_and_year'][0] for k, v in own_floor.items() if k != FLAT)}%; without the floor "
      f"{S[OSN + ' | no floor (counterfactual)']['gap_min_and_year'][0]}%; all runs' weak-anchor low {lo_weak}; deficits: gaps within "
      f"{max(abs(v['gap_min_and_year'][0]) for v in dfc.values()):.2f}%, inflation low {min(v['inflation_min_max'][0] for v in dfc.values())}%; (b), "
      f"{len(cyc_b)} runs: inflation {infl_b[0]}-{infl_b[1]}%, largest gap {max(abs(v['gap_min_and_year'][0]) for v in cyc_b.values()):.2f}%")
part10 = float(np.interp(10, mp["t"], mp["participation"] / mp["participation"][0]))
mpb_ = Wb_[OSN]
part10_b = float(np.interp(10, mpb_["t"], mpb_["participation"] / mpb_["participation"][0]))
check("F4 [restated to the size found; at the refit and at the revision] the structural exit dwarfs the cycle: participation about half "
      "its start by year 10 (on (b) 10%+ lower, the pre-switch claim), the cyclical unemployment rise under a point (0.78; at the refit "
      "about a point, 1.2; before it under 1)",
      0.4 < part10 < 0.6 and os_c["unemployment_up_max"] < 1.0 and part10 < part10_b < 0.9,
      f"participation {part10:.3f} of the start ((b) {part10_b:.3f}); cyclical +{os_c['unemployment_up_max']} pp")
k_now = "status quo + a 2009-size demand shock, today's room (2.25 points) | the Riksbank's 2008 strength, weak anchor"
k_then = "status quo + a 2009-size demand shock, 2008's room (5.25 points) | the Riksbank's 2008 strength, weak anchor"
check("F5 a 2009-size shock takes today's Riksbank to the floor (not 2008's), and the gap three years on is deeper",
      S[k_now]["years_at_floor"] > 0 and S[k_then]["years_at_floor"] == 0 and S[k_now]["y3_y5_y8_y10_y12_y15"]["gap"][0] < S[k_then]["y3_y5_y8_y10_y12_y15"]["gap"][0],
      f"floor {S[k_now]['years_at_floor']} years; gap at year 3 {S[k_now]['y3_y5_y8_y10_y12_y15']['gap'][0]} against {S[k_then]['y3_y5_y8_y10_y12_y15']['gap'][0]}")
HI, CB = R["sensitivity: the high root"]["scenarios"], R["comparator: calibration (b)"]["scenarios"]
ob = CB[f"{OSN} | {C}"]
check("F6 [new on (c); restated at the refit and at the revision] when owners' saving dominates the floor binds for years, and sooner: "
      "6.0 years from year 9.25 within the 15 (at the refit 6.75 from 8.5; before it 4 from 11.25; on (b) 1.25 from year 14)",
      os_c["years_at_floor"] >= 6.0 and os_c["first_year_at_floor"] < 9.5 and ob["years_at_floor"] < 2 and ob["first_year_at_floor"] > 13,
      f"{os_c['years_at_floor']} years from {os_c['first_year_at_floor']}; (b) {ob['years_at_floor']} from {ob['first_year_at_floor']}; "
      f"fast automation {S[OSN + ', fast automation | ' + C]['years_at_floor']} from {S[OSN + ', fast automation | ' + C]['first_year_at_floor']} "
      f"((b) {CB[OSN + ', fast automation | ' + C]['years_at_floor']})")

print("R — the neutral rate: the refit's bridge and its readout keyed back to the pace of tasks (a readout, not a finding)")
e, cal = bs.economy("lo")
eb, _ = bs.economy("b")
worst, worst_fix, worst_term, n_w = 0.0, 0.0, 0.0, 0
for name, (bridges, truth) in list(bs.SCEN.items()) + [("default bridges", ({}, "new"))]:
    for fast in (False, True):
        mp_ = dm.world(bridges, truth, fast=fast, e=e)
        br = m.feedback_bridges(e, **bridges)
        rebuilt = br.r0_star + dm.capex_term(mp_, br) + mp_["r_star_owners"] + mp_["r_star_fiscal"]
        worst = max(worst, float(np.max(np.abs(rebuilt - mp_["r_star"]))))
        tech_ = (m.deep_tech(e, **m.TECH_SPEEDS["fast"]) if fast else m.deep_tech(e)) if truth == "new" else m.hold_tech(e)
        fx = m.macro_path(m.start_economy(e, br), tech_, replace(br, capital_premium=None, rho_shift=0.0), 25.0, 0.25)
        inv_fx, ns_fx = fx["inv_income"] * 100, fx["nonwage_share"]
        worst_fix = max(worst_fix, float(np.max(np.abs(fx["r_star"] - mp_["r_star"]))))
        worst_term = max(worst_term, float(np.max(np.abs(dm.capex_term(mp_, br) - br.alpha_inv * (inv_fx - inv_fx[0])))),
                         float(np.max(np.abs(mp_["r_star_owners"] + br.alpha_rent * (ns_fx - ns_fx[0])))),
                         float(np.max(np.abs(mp_["r_star_fiscal"] - br.alpha_fiscal * (fx["deficit"] - fx["deficit"][0])))))
        n_w += 1
inv0 = dm.investment_income(W[DDN], e)[0]
check("R1 [restated at the revision; set in advance] the readout's pieces are the macro block's: r* = r0 + the three terms the bridge added, "
      "as macro_path stores them — capex_term (on the refit alpha_inv x the change in investment / income), owners' saving (-alpha_rent x "
      "the change in the non-wage share), deficits (+alpha_fiscal x the change in the deficit) — on every (c) world, medium and fast; on "
      "these feedback worlds the bridges read at the start's required return (decision 96), so each term is the fixed-return path's on the "
      "economy the world starts at, and r* is that path's r* exactly (until the revision the terms were read along the path itself, and "
      "R1 rebuilt them from the path's own series); investment / income at the start is solve's inv_income",
      worst < 1e-12 and worst_fix <= 1e-12 and worst_term < 1e-12 and abs(inv0 / 100 - m.solve(e)["inv_income"]) < 1e-15,
      f"{n_w} worlds: largest gap {worst:.1e} (sum of the terms), {worst_fix:.1e} (against the fixed-return r* at the start's return), "
      f"{worst_term:.1e} (each term rebuilt on that path); investment {inv0:.3f}% of income")
ab = dm.alpha_inv_bridge(eb)
qb = m.solve(eb)
x_, a_ = qb["x"], eb.a * eb.delta
Jx, gx = eb.J(x_), eb.gamma(x_)
den = eb.h + eb.b * eb.delta * Jx / (1 - a_)
Yp = -eb.T * eb.b * eb.delta * gx / (1 - a_) / den ** 2
dKdx = (Yp * Jx + (eb.T / den) * gx) / (1 - a_)
per_pp = qb["Vm"] * dKdx * 0.01 / qb["income"] * 100
check("R2 [restated at the revision; set in advance] the scales: the refit's (alpha_inv = macro.Bridges()'s, the investment key: Rachel "
      "and Smith's 0.2 per point of GDP at the central pass-through, per point of income; until the revision macro.NEUTRAL_SCALE) and, for "
      "(b)'s readout, the bridge's (alpha_capex 0.25 over the net investment that moving 1 pp of tasks a year needs at (b)'s start — "
      "recomputed in closed form, dK/dx = (Y' J + Y gamma)/(1 - a delta)) and the demand layer's ((1 - a1)/a_r)",
      abs(ab["net_investment_pct_income_per_pp_tasks_a_year"] / per_pp - 1) < 1e-6 and abs(ab["alpha_inv"] - 0.25 / per_pp) < 1e-8
      and abs(dm.alpha_inv_is(dm.Demand()) - 0.6) < 1e-12 and R["neutral_rate_rekeyed"]["alpha_inv"]["bridge scale"] == ab
      and R["neutral_rate_rekeyed"]["alpha_inv"]["central (c)"] == m.Bridges().alpha_inv == m.INVESTMENT_KEY,
      f"{per_pp:.4f}% of income per pp of tasks a year -> {ab['alpha_inv']:.4f}; demand layer {dm.alpha_inv_is(dm.Demand()):.2f}; the refit's "
      f"{R['neutral_rate_rekeyed']['alpha_inv']['central (c)']:.4f}")
NR = R["neutral_rate_rekeyed"]
TK, BSC, DSC = "task keyed (the bridge as set)", "investment keyed, bridge scale", "investment keyed, demand-layer scale"
IV, PK = "investment keyed (the refit)", "pace keyed (as tuned on (b))"
cc, bb = NR["central (c)"], NR["comparator: calibration (b)"]
DEF = "default bridges (the macro block's own r*)"
lower15 = all(v["r_star"][IV]["15"] < v["r_star"][PK]["15"] for v in cc.values())
inv_falls = all(v["inv_income_pct"]["15"] < v["inv_income_pct"]["0"] - 10 for v in cc.values())
check("R3 [restated at the refit and at the revision] keyed to investment spending (the refit) — which on (c) falls by about 13 points of "
      "income by year 15 on every path — r* never rises above its start in any (c) world and is lower at year 15 in every one than keyed "
      "back to the pace of tasks; keyed to the pace, the deficits branch rises again (by 1.4 points, to about 2.1% at year 15, against "
      "-0.3% on the refit; at the refit by 2.15 points, to 2.9% against -1.1%) and the default world barely rises; on (b) the readout as "
      "before the refit: the hump survives only at the demand layer's scale",
      lower15 and inv_falls and all(v["r_star_rise_above_start_to_15_pp"][IV] <= 1e-12 for v in cc.values())
      and cc[DDN]["r_star_rise_above_start_to_15_pp"][PK] > 1.25 and 1.75 < cc[DDN]["r_star"][PK]["15"] and cc[DDN]["r_star"][IV]["15"] < 0.0
      and cc[DEF]["r_star_rise_above_start_to_15_pp"][PK] < 0.1
      and bb[DEF]["r_star_rise_above_start_to_15_pp"][BSC] <= 1e-12 and bb[DEF]["r_star_rise_above_start_to_15_pp"][DSC] > 0.0,
      f"inv/income {cc[DDN]['inv_income_pct']['0']:.1f} -> {cc[DDN]['inv_income_pct']['15']:.1f}% (deficits); r* at year 15, investment / "
      f"pace keyed: default {cc[DEF]['r_star'][IV]['15']:.2f} / {cc[DEF]['r_star'][PK]['15']:.2f}, deficits {cc[DDN]['r_star'][IV]['15']:.2f} / "
      f"{cc[DDN]['r_star'][PK]['15']:.2f}, owners {cc[OSN]['r_star'][IV]['15']:.2f} / {cc[OSN]['r_star'][PK]['15']:.2f}; deficits' rise keyed to "
      f"the pace {cc[DDN]['r_star_rise_above_start_to_15_pp'][PK]:.2f} pp; (b) default max {[round(x, 2) for x in bb[DEF]['r_star_max_and_year_to_15'][TK]]} / "
      f"{[round(x, 2) for x in bb[DEF]['r_star_max_and_year_to_15'][BSC]]} / {[round(x, 2) for x in bb[DEF]['r_star_max_and_year_to_15'][DSC]]}")
dl = lambda w, s_: cc[w]["demand_layer"][s_]  # noqa: E731
check("R4 [restated at the refit; numbers updated at the revision] the demand layer on those r* paths: keyed back to the pace, the deficits "
      "branch is a mild boom again (+0.5%, inflation above target; at the refit +0.8%) and the owners'-saving gap a third the size (-1.6%; "
      "-2.3%); keyed to investment (the refit) the deficits branch is a small slump and the owners'-saving gap -4.65%, at the floor for 6.0 "
      "years (at the refit -7.2%, 6.75 years) — the cycle's size and the branches' split rest on the capex key",
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

PTS = (1.0, 0.6, 0.4, 0.0)            # the investment key's pass-through (decision 93): 1 gross (the central) to 0 netted
dpt = {p_: dm.summary(dm.run(dm.world({**bs.SCEN[DDN][0], "alpha_inv": m.investment_key(p_)}, bs.SCEN[DDN][1], e=e), base)) for p_ in PTS}
opt = {p_: dm.summary(dm.run(dm.world({**bs.SCEN[OSN][0], "alpha_inv": m.investment_key(p_)}, bs.SCEN[OSN][1], e=e), base)) for p_ in (1.0, 0.0)}
gmax = [dpt[p_]["gap_max_and_year"][0] for p_ in PTS]
gmin = [dpt[p_]["gap_min_and_year"][0] for p_ in PTS]
check("R7 [new at the verification, set after seeing] readout, the investment key's pass-through (decision 93; as bank R7): the deficits "
      "branch is a small slump at the gross reading (the central, F2, equal to the stored run) and turns as less of the investment fall "
      "counts — its gap's high rising and its low no longer negative, a mild boom with the fall netted against capital consumption; the "
      "owners'-saving branch stays a slump at the floor at both ends",
      json.loads(json.dumps(dpt[1.0])) == dd_c and json.loads(json.dumps(opt[1.0])) == os_c
      and np.all(np.diff(gmax) > 0) and np.all(np.diff(gmin) >= 0) and gmax[0] == 0.0 and gmin[0] < -0.3 and gmin[-1] == 0.0 and gmax[-1] > 0.3
      and all(v["gap_min_and_year"][0] < -1.0 and v["years_at_floor"] > 0 for v in opt.values()),
      "the deficits branch at a pass-through of 1 / 0.6 / 0.4 / 0: gap low " + " / ".join(f"{x:+.2f}" for x in gmin) + ", high "
      + " / ".join(f"{x:+.2f}" for x in gmax) + "%, inflation " + " / ".join(f"{dpt[p_]['inflation_min_max'][0]}-{dpt[p_]['inflation_min_max'][1]}"
                                                                              for p_ in PTS)
      + "%; owners' saving gross / netted " + " / ".join(f"{opt[p_]['gap_min_and_year'][0]}% ({opt[p_]['years_at_floor']} years at the floor)"
                                                         for p_ in (1.0, 0.0)))

print("X — the switch: (c)'s runs, the (b) comparator, the high root")
fresh = {}
for name, mp_ in W.items():
    for vn, dv in VAR.items():
        fresh[f"{name} | {vn}"] = dm.summary(dm.run(mp_, dv))
for name in (DDN, OSN):
    mpf_ = dm.world(bs.SCEN[name][0], "new", fast=True)
    for vn in (C, "slow learning (8 years, pre-2021 anchors)", "weak anchor (expectations follow inflation)"):
        fresh[f"{name}, fast automation | {vn}"] = dm.summary(dm.run(mpf_, VAR[vn]))
RESP = {"textbook rule": base, "the Riksbank's 2008 strength": replace(base, phi_y=1.0, smooth=0.5)}
for name in ("status quo", OSN):
    mp_ = W[name]
    neutral = float(mp_["r_star"][0] + mp_["pi_star"])
    for room_name, room in (("2008's room (5.25 points)", 5.25), ("today's room (2.25 points)", 2.25)):
        for resp, d0_ in RESP.items():
            for anch, a_ in (("anchored", d0_.anchor), ("weak anchor", 0.5)):
                fresh[f"{name} + a 2009-size demand shock, {room_name} | {resp}, {anch}"] = dm.summary(
                    dm.run(mp_, replace(d0_, elb=neutral - room, anchor=a_), shock=dm.crash(mp_["t"])), horizon=6.0)
eh_, calh_ = bs.economy("hi")
bbh_, sch_ = bs.base_bridges("hi")
fresh_hi = {f"{name} | {C}": dm.summary(dm.run(dm.world(br_, tr_, e=eh_, base=bbh_), base)) for name, (br_, tr_) in sch_.items()}
fresh_hi |= {f"{name}, fast automation | {C}": dm.summary(dm.run(dm.world(sch_[name][0], sch_[name][1], fast=True, e=eh_, base=bbh_), base))
             for name in (DDN, OSN)}
check("X1 [extended at the verification] demand.json's runs equal a fresh rebuild on macro.central() — every stored scenario (the three "
      "worlds under every variant, fast automation, the 2009-size shocks; until the verification only the five central-learning runs) and "
      "the high-root block F3 and X3 read (its calibration record too) — and its calibration record is the central's",
      json.loads(json.dumps(fresh)) == S and R["calibration"] == json.loads(json.dumps(cal))
      and json.loads(json.dumps(fresh_hi)) == HI and R["sensitivity: the high root"]["calibration"] == json.loads(json.dumps(calh_)),
      f"{len(fresh)} of {len(S)} runs; the high root {len(fresh_hi)} of {len(HI)}; {cal['tag']} / {calh_['tag']}")


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
