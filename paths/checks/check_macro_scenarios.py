# check_macro_scenarios.py — deep automation at three speeds and capital's part, on calibration (c)'s central economy
# (her decision, 2026-09-30), with the pre-switch runs kept as comparators: the results reproduce, the comparators are the
# pre-switch runs, every date solves, and the findings are stated as found.
#
# checks/check_macro.py gates calibrations (a) and (b) themselves (the paper's instance, the identities, the calibrations,
# the bridges' signs, the capital findings on (b)) and is unchanged; this battery gates code/macro_scenarios.py's results,
# which no battery gated before the switch. The findings F1-F9 restate, on the central, what the pre-switch unit reported
# on (a) (three speeds) and (b) (capital); each check prints the comparator beside the central.
# Restated after the switch's reviews (stated as found, nothing loosened): F5 at the two scales demand.py and bank_scenarios.py
# use (the first report's 0.25 was alpha_capex unconverted), with (b)'s early rise in investment / income gated directly;
# F2 carries the (c) variants' one exception and (b) at g0 0.01 (results/calibration_c.json); F6 the re-centred fiscal
# start; F7 the import-as-land channel; F8 both labour-share bases and the 1/sigma_V scaling; F9 the lag phase as found
# (it shrinks, it does not vanish). If a capital run has a date with no land-scarce equilibrium, R3 fails and F7-F9 report
# it rather than raising.
# Thresholds set after seeing (c)'s numbers (flagged here): F2's 1.02 on (a)/(b)'s rise; F4's +0.1 ((a)'s medium rise); F6's
# 0.2 fall in the wage-tax share; F7's 0.8 for the site; F8's 1.5x and 3x.
# Restated at the refit (2026-10-27, Log 46; decisions 72-75), as found: the central and its high root run on the refit
# (macro.Bridges()), the comparators on macro.BRIDGES_B. R4 gates the readout that keys the capex channel back to the pace;
# F4 the refit's neutral rate (no hump at any speed; before the refit a hump on the fast path only, now the readout's); F5 the
# investment fall and (b)'s readout (unchanged); F6 the fiscal start at the measured primary deficit (before: a surplus start,
# with the re-centred start as the sensitivity; now the surplus start is the sensitivity); F9 the loop with no lag phase at
# all (before: shrunk to negligible). V (new) gates the evidence and the refit one bridge at a time. Thresholds set after
# seeing the refit's numbers (flagged): V3's step-by-step orderings are the found ones, not set in advance.
#
# Run from paths/:  ../venv/Scripts/python.exe checks/check_macro_scenarios.py
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
import macro as m  # noqa: E402
import macro_scenarios as ms  # noqa: E402

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


def load(name):
    with open(os.path.join(ROOT, "results", name), encoding="utf-8") as f:
        return json.load(f)


rt = lambda o: json.loads(json.dumps(o))  # noqa: E731
arr = lambda d: {k: v for k, v in d.items() if isinstance(v, np.ndarray)}  # noqa: E731
same = lambda a, b: arr(a).keys() == arr(b).keys() and all(np.array_equal(a[k], b[k]) for k in arr(a))  # noqa: E731

print("R — reproduction, comparators, solvability")
S, C = load("macro_scenarios.json"), load("capital_feedback.json")
S_new, C_new = rt(ms.results()[0]), rt(ms.capital_results()[0])
check("R1 results/macro_scenarios.json and results/capital_feedback.json equal a rebuild by code/macro_scenarios.py",
      S == S_new and C == C_new, f"blocks: central, comparators {sorted(S['comparators'])}, sensitivity_c_hi; capital: central, comparator_b")
ec, info = m.central()
ea, _, _, _ = m.calibrate()
eb, _, _, _ = m.calibrate(base=m.CAPITAL_BASE)
old_a = all(same(m.macro_path(ea, m.TechPath(eta_end=0.04, lam_end=0.01, **kw), m.BRIDGES_B), m.macro_path(ea, m.deep_tech(ea, **kw), m.BRIDGES_B))
            for kw in m.TECH_SPEEDS.values())
tb = m.TechPath(eta_end=0.04, lam_end=0.01, t_mid=6, width=6)
old_b = (same(m.macro_path(eb, tb, replace(m.BRIDGES_B, capital_premium=5.0)), m.macro_path(eb, m.deep_tech(eb), m.feedback_bridges(eb, base=m.BRIDGES_B)))
         and same(m.macro_path(eb, tb, replace(m.BRIDGES_B, capital_premium=5.0, rho_shift=2.0)),
                  m.macro_path(eb, m.deep_tech(eb), m.feedback_bridges(eb, base=m.BRIDGES_B, rho_shift=2.0))))
tc = m.deep_tech(ec)
check("R2 the comparators are the pre-switch runs array for array — (a)'s three speeds with the hard-coded TechPath(0.04, 0.01, ...), "
      "(b)'s capital runs with Bridges(capital_premium=5.0) — and the central is macro.central() with lambda to a fifth of its own start",
      old_a and old_b and S["calibration"]["record"]["tag"] == "c_central_lo" and tc.lam_end == ec.lam / 5.0
      and S["calibration"]["lam"] == ec.lam and C["comparator_b"]["calibration_b"]["rho"] == 0.0575,
      f"central lambda {ec.lam:.3f} -> {tc.lam_end:.3f} (model units), premium {info['capital_premium']:.2f} pp; (b) 0.05 -> 0.01, premium 5.00")
solved = all(e_ is None for e_ in C["errors"].values()) and all(e_ is None for e_ in C["comparator_b"]["errors"].values())
CAP = solved and "not_computed" not in C and "not_computed" not in C["comparator_b"]
rise = C.get("max_rho_rise_pp", {"follow": float("nan"), "shock_200bp": float("nan")})
check("R3 every date of every run solves (no date without a land-scarce equilibrium), and the largest rise in the required return "
      "(the +200 bp run) stays inside the central's rate headroom",
      CAP and len(S["scenarios"]) == len(S["sensitivity_c_hi"]["scenarios"]) == 3 and max(rise.values()) < info["headroom_pp"],
      f"largest rise {max(rise.values()):.2f} pp against headroom {info['headroom_pp']:.2f} pp; following r* alone {rise['follow']:+.3f} pp"
      if CAP else f"errors: central {C['errors']}, (b) {C['comparator_b']['errors']}")
mp = m.macro_path(ec, tc)
br = m.Bridges()
inv = ms.investment_income(ec, mp)
q_inv = np.array([m.solve(e_)["inv_income"] for e_ in (tc.at(t_, ec) for t_ in mp["t"])])
import demand as dmd  # noqa: E402
SC = {"bridge scale": dmd.alpha_inv_bridge(eb)["alpha_inv"], "demand-layer scale": dmd.alpha_inv_is(dmd.Demand())}
err4 = float(np.max(np.abs((ms.r_star_capex_on_pace(ec, mp, br) - mp["r_star"])
                           - (br.alpha_capex * mp["automation_pace"] - br.alpha_inv * (inv - inv[0]) * 100))))
mpb = m.macro_path(eb, tb, m.BRIDGES_B)
invb = ms.investment_income(eb, mpb)
err4b = max(float(np.max(np.abs((ms.r_star_capex_on_investment(eb, mpb, a, m.BRIDGES_B) - mpb["r_star"])
                                - (a * (invb - invb[0]) * 100 - m.BRIDGES_B.alpha_capex * mpb["automation_pace"])))) for a in SC.values())
check("R4 [restated at the refit] the central's r* is keyed to investment (alpha_inv x the change in replacement investment / income), "
      "and its readout keyed to the pace differs from it only in the capex channel (alpha_capex 0.25 x the pace in its place); (b)'s "
      "readout keyed to investment at the two scales demand.py and bank_scenarios.py use differs from (b)'s pace-keyed r* only there "
      "too; the investment is solve's inv_income at every date",
      br.capex_key == "investment" and m.BRIDGES_B.capex_key == "pace" and err4 < 1e-12 and err4b < 1e-12
      and np.max(np.abs(inv - q_inv)) < 1e-12 and np.max(np.abs(mp["inv_income"] - q_inv)) < 1e-15 and S["capex_on_investment"]["alpha_inv"] == SC,
      f"max error {err4:.1e} (central) / {err4b:.1e} ((b)) / {np.max(np.abs(inv - q_inv)):.1e}; alpha_inv {br.alpha_inv:g}; (b)'s scales "
      f"{SC['bridge scale']:.4f} (bridge) and {SC['demand-layer scale']:.2f} (demand layer)")

print("F — findings (the central on the refit against the pre-switch runs on their own bridges; stated as found)")
c, a, b, h = S["scenarios"], S["comparators"]["a"]["scenarios"], S["comparators"]["b"]["scenarios"], S["sensitivity_c_hi"]["scenarios"]
sp3 = ("slow", "medium", "fast")
hv = [c[k]["labour_share_halves_year"] for k in sp3]
ha = [a[k]["labour_share_halves_year"] for k in sp3]
check("F1 labour's share (the paper's Figure 7 basis) falls at the technology clock's speed and halves no later than in (a) at any speed; "
      "fast, it is below a tenth of its start within six years",
      all(x <= y for x, y in zip(hv, ha)) and c["fast"]["labour_share"]["6.0"] < 0.1 * c["fast"]["labour_share"]["0.0"],
      f"halves in year {hv[0]} / {hv[1]} / {hv[2]} (slow/medium/fast), (a) {ha[0]} / {ha[1]} / {ha[2]}; fast "
      f"{c['fast']['labour_share']['0.0']:.2f} -> {c['fast']['labour_share']['6.0']:.2f} by year 6")
with open(m.CENTRAL_SOURCE, encoding="utf-8") as fh_:
    CS = json.load(fh_)["scenarios"]                  # calibration_c.py's medium runs of every variant (gated by check_calibration_c)
cvar = {k: v["medium"]["real_wage_peak_over_start"] for k, v in CS.items() if k.startswith("c_")}
rises_c = sorted(k for k, v in cvar.items() if v > 1.0)
g001 = {k: CS[k]["medium"]["real_wage_peak_over_start"] for k in ("b_g001_lo", "b_g001_hi")}
check("F2 the real wage no longer rises first: on (c) its highest point is the start at every speed, on both roots, and it ends lower "
      "than in (a) or (b); in (a) and (b) it rose about 3% first. Not a g0 effect: (b) at (c)'s g0 0.01 still rises first. Among the (c) "
      "variants of calibration_c.py one exception rises first, c_site_hi (the site-share variant's high root)",
      all(c[k]["real_wage_peak_year"] == 0.0 and h[k]["real_wage_peak_year"] == 0.0 for k in sp3)
      and all(x[k]["real_wage_peak_over_start"] > 1.02 for x in (a, b) for k in sp3)
      and all(c[k]["real_wage_end_over_start"] < min(a[k]["real_wage_end_over_start"], b[k]["real_wage_end_over_start"]) for k in sp3)
      and all(v > 1.0 for v in g001.values()) and rises_c == ["c_site_hi"] and cvar["c_central_lo"] == cvar["c_central_hi"] == 1.0,
      f"medium: (c) peak at year 0, ends x{c['medium']['real_wage_end_over_start']:.2f}; (a) peak x{a['medium']['real_wage_peak_over_start']:.3f} "
      f"at year {a['medium']['real_wage_peak_year']}, ends x{a['medium']['real_wage_end_over_start']:.2f}; (b) x{b['medium']['real_wage_peak_over_start']:.3f}, "
      f"ends x{b['medium']['real_wage_end_over_start']:.2f}; (b) at g0 0.01: x{g001['b_g001_lo']:.3f} / x{g001['b_g001_hi']:.3f} (low / high root); "
      f"(c) variants rising first: {rises_c} (x{cvar['c_site_hi']:.3f} in year {CS['c_site_hi']['medium']['real_wage_peak_year']:g}) of {len(cvar)}")
check("F3 the fork, medium speed, with the basket on target: shelter inflation peaks as high as in (a), and goods deflate harder",
      abs(c["medium"]["pi_shelter_max"] - a["medium"]["pi_shelter_max"]) < 2.0 and c["medium"]["pi_goods_min"] < a["medium"]["pi_goods_min"],
      f"shelter peak {c['medium']['pi_shelter_max']:+.1f}% a year ((a) {a['medium']['pi_shelter_max']:+.1f}), goods trough "
      f"{c['medium']['pi_goods_min']:+.1f}% ((a) {a['medium']['pi_goods_min']:+.1f})")
rc_, ra_ = {k: c[k]["r_star_start_peak_end"] for k in sp3}, {k: a[k]["r_star_start_peak_end"] for k in sp3}
rp_ = {k: c[k]["r_star_capex_on_pace_start_peak_end"] for k in sp3}
check("F4 [restated at the refit] the neutral rate on the refit (capex keyed to investment): its highest point is the start at every "
      "speed, on both roots — the build-out hump is gone — and it ends below (a)'s at every speed, lower the faster the change; "
      "keyed back to the pace of tasks (the readout), it ends higher at every speed but still never rises a tenth of a point (before the "
      "refit the pace-keyed r* rose on the fast path, 0.76 -> 1.35%); in (a) the medium and fast paths rose",
      all(x[k]["r_star_peak_year"] == 0.0 for x in (c, h) for k in sp3)
      and all(rc_[k][2] < ra_[k][2] for k in sp3) and rc_["slow"][2] > rc_["medium"][2] > rc_["fast"][2]
      and all(rp_[k][2] > rc_[k][2] and rp_[k][1] - rp_[k][0] < 0.1 for k in sp3)
      and ra_["medium"][1] > ra_["medium"][0] + 0.1 and ra_["fast"][1] > ra_["fast"][0] + 0.1,
      "start/peak/end: " + ", ".join(f"{k} " + "/".join(f"{v:+.2f}" for v in rc_[k]) for k in sp3) + "; keyed to the pace: "
      + ", ".join("/".join(f"{v:+.2f}" for v in rp_[k]) for k in sp3) + "; (a) " + ", ".join("/".join(f"{v:+.2f}" for v in ra_[k]) for k in sp3)
      + f"; high root ends " + " / ".join(f"{h[k]['r_star_start_peak_end'][2]:+.2f}" for k in sp3))
BSC, DSC = "bridge scale", "demand-layer scale"
gapp = [c[k]["r_star_capex_on_pace_end_above_investment_keyed_pp"] for k in sp3]
check("F5 [restated at the refit] (c)'s replacement investment / income falls from the start at every speed, on both roots — the series "
      "the refit keys r* to — and keyed back to the pace of tasks instead, r* ends 2-4 points higher (the investment term at the common "
      "scale, 0.3). On (b), on its own bridges at a fixed return, investment / income first rises, and its readout keyed to investment "
      "rises at the demand layer's scale but not at the bridge's (unchanged since the switch)",
      all(c[k]["investment_income"]["15.0"] < c[k]["investment_income"]["3.0"] < c[k]["investment_income"]["0.0"] for k in sp3)
      and all(x[k]["investment_income_peak_and_year"][1] == 0.0 for x in (c, h) for k in sp3)
      and all(2.0 < g < 4.5 for g in gapp)
      and all(b[k]["investment_income"]["3.0"] > b[k]["investment_income"]["0.0"] and b[k]["investment_income_peak_and_year"][1] > 0.0 for k in sp3)
      and all(b[k]["r_star_capex_on_investment_rise_bp"][DSC] > 0.0 and b[k]["r_star_capex_on_investment_rise_bp"][BSC] == 0.0 for k in sp3),
      "investment / income, medium: " + " ".join(f"{v:.3f}" for v in c["medium"]["investment_income"].values())
      + "; keyed to the pace, r* ends higher by " + " / ".join(f"{g:.2f}" for g in gapp) + " pp (slow/medium/fast); (b): investment / "
      + f"income medium {b['medium']['investment_income']['0.0']:.4f} -> {b['medium']['investment_income_peak_and_year'][0]:.4f} at year "
      + f"{b['medium']['investment_income_peak_and_year'][1]:g}, readout rise " + "/".join(f"{b[k]['r_star_capex_on_investment_rise_bp'][DSC]:.1f}" for k in sp3)
      + " bp at the demand layer's scale, " + "/".join(f"{b[k]['r_star_capex_on_investment_rise_bp'][BSC]:.1f}" for k in sp3) + " at the bridge's")
FS = S["sensitivity_fiscal_start"]
fs = FS["scenarios"]
check("F6 [restated at the refit] the fiscal corollary: the wage-tax share of revenue falls and debt climbs further than in (a) — from "
      "the measured start, a primary deficit of macro.START_DEFICIT (0.16% of income) on both roots at every speed, the wage tax set to "
      "give it (0.35; before the refit 0.40 on all wages, a surplus of 2.61%); debt rises from the start, without the dip the surplus "
      "start gave. With the wage tax as tuned on (b) (the sensitivity: a surplus start), debt ends lower at every speed, so the "
      "surplus start was the milder reading",
      all(c[k]["wage_tax_share_start_end"][1] < c[k]["wage_tax_share_start_end"][0] - 0.2 for k in sp3)
      and all(c[k]["debt"]["15.0"] > a[k]["debt"]["15.0"] for k in ("medium", "fast"))
      and all(x[k]["deficit_start_end"][0] == m.START_DEFICIT for x in (c, h) for k in sp3)
      and all(c[k]["debt"]["3.0"] > c[k]["debt"]["0.0"] for k in ("slow", "medium")) and c["fast"]["debt"]["6.0"] > c["fast"]["debt"]["0.0"]
      and FS["tau_w"] == 0.40 and abs(FS["tau_w_default"] - c["medium"]["tau_w"]) < 1e-4
      and all(fs[k]["deficit_start_end"][0] < 0 and fs[k]["debt"]["15.0"] < c[k]["debt"]["15.0"] for k in sp3),
      f"wage-tax share, medium {c['medium']['wage_tax_share_start_end'][0]:.2f} -> {c['medium']['wage_tax_share_start_end'][1]:.2f}; debt by year 15, "
      f"slow / medium / fast {c['slow']['debt']['15.0']:.0f} / {c['medium']['debt']['15.0']:.0f} / {c['fast']['debt']['15.0']:.0f}% ((a) "
      f"{a['medium']['debt']['15.0']:.0f} / {a['fast']['debt']['15.0']:.0f} medium / fast); start deficit {c['medium']['deficit_start_end'][0]:+.2f}% "
      f"(tau_w {c['medium']['tau_w']:.4f}); with tau_w {FS['tau_w']:.2f} (start {fs['medium']['deficit_start_end'][0]:+.2f}%): "
      + " / ".join(f"{fs[k]['debt']['15.0']:.0f}" for k in sp3) + "%")
F7_ = ("F7 under deep automation capital does not capture the gains, the fixed site does — more so than in (b): along the medium path "
       "(return following r*) interest and machine-chain land fall and the housing site rises to most of income. Part of 'more so' is "
       "the import-as-land channel: the chain's imported content (its share of sigma_V from results/calibration_c.json) is modelled "
       "as machine-chain land drawn from the land endowment, and as the machine stock falls that land is freed to housing — the "
       "chain's share of land rent collapses; the channel's direction on the paths is an open item of (c)")
F8_ = ("F8 a sustained +200 bp on the required return slows automation at every date and raises labour's share at every date — on all "
       "wages and on the paper's Figure 7 basis — more strongly than in (b) (labour's share by over half as much again, the delay three "
       "times and more); the rate elasticity of w/r, 1/sigma_V, is higher, and the response's size scales with it (sigma_V's "
       "construction is an open item of (c): a fixed point, with delta_chain not the chain's own depreciation)")
F9_ = ("F9 [restated at the refit] the loop: the return follows r*; on the refit r* never rises along the medium path (the return's "
       "largest rise under 0.01 pp), so there is no lag phase at all — automation runs ahead of the fixed-return path from the start, "
       "cheaper capital speeding it (before the refit a lag phase of two years by under a thousandth of a point; (b): lagged while the "
       "build-out held rates up, then ran ahead)")
if CAP:
    s0, s15, b0, b15 = C["split_start"], C["split_year15"], C["comparator_b"]["split_start"], C["comparator_b"]["split_year15"]
    ch, chb = C["chain_share_of_land_rent_start_year15"], C["comparator_b"]["chain_share_of_land_rent_start_year15"]
    check(F7_, s15["interest"] < s0["interest"] and s15["machine-chain land"] < s0["machine-chain land"] and s15["housing site"] > 0.8
          and s15["housing site"] > b15["housing site"] and abs(sum(s0.values()) - 1) < 2e-3 and ch[1] < ch[0]
          and f"{ms.import_share_of_sigma():.3f} of sigma_V" in C["split_note"],
          "start -> year 15: " + ", ".join(f"{k} {s0[k]:.3f} -> {s15[k]:.3f}" for k in s0) + f" (labour: all wages); (b) site {b0['housing site']:.2f} -> "
          f"{b15['housing site']:.2f}; the chain's share of land rent {ch[0]:.3f} -> {ch[1]:.3f} ((b) {chb[0]:.3f} -> {chb[1]:.3f}); imported content "
          f"{ms.import_share_of_sigma():.3f} of sigma_V")
    sh, shb = C["shock_200bp"], C["comparator_b"]["shock_200bp"]
    el_c, el_b = 1.0 / m.solve(ec)["sigma_V"], 1.0 / m.solve(eb)["sigma_V"]
    check(F8_, sh["slows_every_date"] and sh["raises_labour_share_every_date"] and sh["max_labour_share_pp"] > 1.5 * shb["max_labour_share_pp"]
          and sh["max_labour_share_bea_pp"] > 1.5 * shb["max_labour_share_bea_pp"]
          and sh["delay_at_year6_weeks"] > 3 * shb["delay_at_year6_weeks"] and el_c > el_b,
          f"elasticity {el_c:.2f} ((b) {el_b:.2f}); labour's share up to {sh['max_labour_share_pp']:+.2f} pp on all wages, {sh['max_labour_share_bea_pp']:+.2f} "
          f"on the Figure 7 basis ((b) {shb['max_labour_share_pp']:+.2f} / {shb['max_labour_share_bea_pp']:+.2f}), tasks {sh['max_tasks_pp']:+.2f} pp "
          f"((b) {shb['max_tasks_pp']:+.2f}), delay at year 6 {sh['delay_at_year6_weeks']:.1f} weeks ((b) {shb['delay_at_year6_weeks']:.1f})")
    lg, lgb = C["loop_lag_phase"], C["comparator_b"]["loop_lag_phase"]
    check(F9_, rise["follow"] < 0.01 and C["loop_corr_return_vs_tasks"] < -0.5 and C["loop_year15_tasks_ahead_pp"] > 0
          and C["comparator_b"]["max_rho_rise_pp"]["follow"] > 0.1 and lg is None and lgb is not None,
          f"largest rise in the return {rise['follow']:+.3f} pp ((b) {C['comparator_b']['max_rho_rise_pp']['follow']:+.3f}); lag phase: none "
          f"((b) years {lgb['from_year']:g}-{lgb['to_year']:g}, {lgb['deepest_tasks_pp']:+.4f} pp); correlation {C['loop_corr_return_vs_tasks']:.2f}; "
          f"automation {C['loop_year15_tasks_ahead_pp']:+.2f} pp ahead by year 15 ((b) {C['comparator_b']['loop_year15_tasks_ahead_pp']:+.2f})")
else:
    for name_ in (F7_, F8_, F9_):
        check(name_, False, f"not computed: a capital run has a date with no land-scarce equilibrium — central {C['errors']}, (b) "
                            f"{C['comparator_b']['errors']}")

print("V — the refit: the evidence, the fiscal start, one bridge at a time (Log 46)")
br0 = m.Bridges()
ev = S["evidence"]
fse = ev["fiscal_start"]
check("V1 the refit's coefficients are the evidence's: alpha_inv the common scale, alpha_rent the scale times owners' saving gap, "
      "alpha_fiscal the scale times the deficit's pass-through; each central inside its stated range; the two branches the direction "
      "bridges at the ends of their ranges, each against the other's opposite end; the comparators' bridges and branches are (b)'s "
      "(macro.BRIDGES_B: the pace key, the wage tax 0.40, 0.05 and 0.10; BRANCHES_B: 0.25 / 0.02 and 0.12); the stored evidence "
      "lists the literature behind each number",
      br0.alpha_inv == m.NEUTRAL_SCALE and br0.alpha_rent == m.NEUTRAL_SCALE * m.OWNERS_SAVING_GAP
      and br0.alpha_fiscal == m.NEUTRAL_SCALE * m.DEFICIT_PASS_THROUGH
      and m.NEUTRAL_SCALE_RANGE[0] <= m.NEUTRAL_SCALE <= m.NEUTRAL_SCALE_RANGE[1]
      and m.OWNERS_SAVING_GAP_RANGE[0] <= m.OWNERS_SAVING_GAP <= m.OWNERS_SAVING_GAP_RANGE[1]
      and m.DEFICIT_PASS_THROUGH_RANGE[0] <= m.DEFICIT_PASS_THROUGH <= m.DEFICIT_PASS_THROUGH_RANGE[1]
      and m.BRANCHES["deficits dominate"] == dict(alpha_rent=m.NEUTRAL_SCALE * m.OWNERS_SAVING_GAP_RANGE[0],
                                                  alpha_fiscal=m.NEUTRAL_SCALE * m.DEFICIT_PASS_THROUGH_RANGE[1])
      and m.BRANCHES["owners' saving dominates"] == dict(alpha_rent=m.NEUTRAL_SCALE * m.OWNERS_SAVING_GAP_RANGE[1],
                                                         alpha_fiscal=m.NEUTRAL_SCALE * m.DEFICIT_PASS_THROUGH_RANGE[0])
      and (m.BRIDGES_B.capex_key, m.BRIDGES_B.tau_w, m.BRIDGES_B.alpha_rent, m.BRIDGES_B.alpha_fiscal) == ("pace", 0.40, 0.05, 0.10)
      and m.BRANCHES_B == {"deficits dominate": dict(alpha_fiscal=0.25, alpha_rent=0.02), "owners' saving dominates": dict(alpha_rent=0.12)}
      and all(len(ev["literature"][k]) >= 3 for k in ("neutral_scale", "owners_saving_gap", "deficit_pass_through")),
      f"scale {m.NEUTRAL_SCALE:g} {m.NEUTRAL_SCALE_RANGE}, gap {m.OWNERS_SAVING_GAP:g} {m.OWNERS_SAVING_GAP_RANGE}, pass-through "
      f"{m.DEFICIT_PASS_THROUGH:g} {m.DEFICIT_PASS_THROUGH_RANGE}: alpha_inv {br0.alpha_inv:g}, alpha_rent {br0.alpha_rent:.3f}, alpha_fiscal "
      f"{br0.alpha_fiscal:.3f}; branches " + "; ".join(f"{k} " + ", ".join(f"{kk} {vv:.3f}" for kk, vv in v.items()) for k, v in m.BRANCHES.items()))
fd = ms.fiscal_data()["values"]
se_mean = float(np.mean([-(fd[f"SE|B9|{y}"] + fd[f"SE|D41PAY|{y}"]) for y in ms.FISCAL_YEARS]))
check("V2 the fiscal start is Sweden's: macro.START_DEFICIT is the general government's 2021-25 mean primary deficit (Eurostat, cached "
      "in cache/fiscal/; 0.14% of GDP) on the model's income basis (GDP net of the chain's imported content over income, from "
      "calibration_c.json's central), to two decimals; debt0's 40% of income lies within 1.5 pp of Sweden's 2025 debt on that basis",
      round(se_mean * fse["gdp_over_income"], 2) == m.START_DEFICIT == fse["sweden_mean_pct_income"]
      and abs(fse["sweden_debt_latest_pct_income"] - br0.debt0) < 1.5 and fse["updated"]["gov_10a_main"].startswith("2026"),
      f"Sweden {se_mean:.3f}% of GDP x {fse['gdp_over_income']:.4f} = {se_mean * fse['gdp_over_income']:.3f}% of income (2025 alone "
      f"{fse['sweden_latest_pct_income']:.2f}); debt 2025 {fse['gross_debt_pct_gdp']['SE']['2025']}% of GDP = "
      f"{fse['sweden_debt_latest_pct_income']}% of income against debt0 {br0.debt0:g}; Eurostat of {fse['updated']['gov_10a_main'][:10]}")
st, sth = S["refit_steps"], S["refit_steps_c_hi"]
nm = ms.REFIT_STEPS
end = {j: [st[nm[j]][k]["r_star_start_peak_end"][2] for k in sp3] for j in range(5)}
hump = {j: st[nm[j]][k]["r_star_start_peak_end"] for j in range(5) for k in ("fast",)}
d15 = {j: [st[nm[j]][k]["debt_low_and_year15"][1] for k in sp3] for j in range(5)}
check("V3 the refit one bridge at a time, on the central (both roots), as found: step 0, the bridges as tuned on (b), is the pre-refit "
      "central as STATE recorded it (the fast path 0.76 -> 1.35 -> -0.13%, debt at year 15 57 / 121 / 187%); keying the capex channel to investment (1) removes the hump at every speed and lowers r* "
      "at year 15 at every speed; owners' saving at the evidence's gap (2) lowers it further; deficits at their pass-through (3) raise it "
      "back part way; the measured fiscal start (4) lowers it again (the deficit rises less from a balanced start) and raises debt at "
      "year 15 at every speed; step 4 is the refit itself",
      ms.refit_bridges(0) == m.BRIDGES_B and ms.refit_bridges(4) == m.Bridges()
      and st[nm[0]]["fast"]["r_star_start_peak_end"] == [0.76, 1.35, -0.13] and d15[0] == [56.8, 121.3, 186.8]
      and all(x[nm[j]][k]["r_star_peak_year"] == 0.0 for x in (st, sth) for j in (1, 2, 3, 4) for k in sp3)
      and all(end[1][i] < end[0][i] and end[2][i] < end[1][i] and end[3][i] > end[2][i] and end[4][i] < end[3][i] for i in range(3))
      and all(d15[4][i] > d15[3][i] for i in range(3)) and [st[nm[4]][k]["r_star_start_peak_end"] for k in sp3] == [rc_[k] for k in sp3],
      "r* at year 15, slow/medium/fast: " + "; ".join(f"step {j} " + " / ".join(f"{v:+.2f}" for v in end[j]) for j in range(5))
      + f"; fast peak at step 0 {hump[0][1]:+.2f}; debt at year 15: " + "; ".join(f"{j} " + " / ".join(f"{v:.0f}" for v in d15[j]) for j in (0, 3, 4)))

fails = [n for n, ok, _ in RESULTS if not ok]
print(f"\n{len(RESULTS) - len(fails)}/{len(RESULTS)} checks passed")
print(f"ALL GREEN ({len(RESULTS)})" if not fails else "FAILURES: " + "; ".join(n.split(' ')[0] for n in fails))
sys.exit(0 if not fails else 1)
