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
# Thresholds set after seeing (c)'s numbers (flagged here): F2's 1.02 on (a)/(b)'s rise; F4's +0.3 (fast hump) and +0.1
# ((a)'s medium rise); F6's 0.2 fall in the wage-tax share; F7's 0.8 for the site; F8's 1.5x and 3x; F9's tenfold.
#
# Run from paths/:  ../venv/Scripts/python.exe checks/check_macro_scenarios.py
# Exit status 0 only if every check passes.

from __future__ import annotations

import json
import os
import sys

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
old_a = all(same(m.macro_path(ea, m.TechPath(eta_end=0.04, lam_end=0.01, **kw)), m.macro_path(ea, m.deep_tech(ea, **kw)))
            for kw in m.TECH_SPEEDS.values())
tb = m.TechPath(eta_end=0.04, lam_end=0.01, t_mid=6, width=6)
old_b = (same(m.macro_path(eb, tb, m.Bridges(capital_premium=5.0)), m.macro_path(eb, m.deep_tech(eb), m.feedback_bridges(eb)))
         and same(m.macro_path(eb, tb, m.Bridges(capital_premium=5.0, rho_shift=2.0)),
                  m.macro_path(eb, m.deep_tech(eb), m.feedback_bridges(eb, rho_shift=2.0))))
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
err4 = max(float(np.max(np.abs((ms.r_star_capex_on_investment(ec, mp, a) - mp["r_star"])
                               - (a * (inv - inv[0]) * 100 - br.alpha_capex * mp["automation_pace"])))) for a in SC.values())
check("R4 the investment-keyed readout differs from the default r* only in the capex channel (alpha_inv x the change in investment / "
      "income in place of alpha_capex x the pace), at the two scales demand.py and bank_scenarios.py use (demand.alpha_inv_bridge, "
      "demand.alpha_inv_is: one source), and its investment is solve's inv_income at every date",
      err4 < 1e-12 and np.max(np.abs(inv - q_inv)) < 1e-12 and S["capex_on_investment"]["alpha_inv"] == SC,
      f"max error {err4:.1e} / {np.max(np.abs(inv - q_inv)):.1e}; scales {SC['bridge scale']:.4f} (bridge) and "
      f"{SC['demand-layer scale']:.2f} (demand layer)")

print("F — findings (the central against the pre-switch runs; bridges set on (a)/(b), not retuned; stated as found)")
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
check("F4 the neutral rate (the default bridge, capex keyed to the pace of tasks moving): up then down only on the fast path, a smaller "
      "hump than (a)'s; on the medium and slow paths it never rises above its start (in (a) the medium path rose too)",
      rc_["fast"][1] > rc_["fast"][0] + 0.3 and rc_["fast"][2] < rc_["fast"][0] and rc_["fast"][1] - rc_["fast"][0] < ra_["fast"][1] - ra_["fast"][0]
      and all(c[k]["r_star_peak_year"] == 0.0 for k in ("slow", "medium")) and ra_["medium"][1] > ra_["medium"][0] + 0.1,
      "start/peak/end: fast " + "/".join(f"{v:+.2f}" for v in rc_["fast"]) + " ((a) " + "/".join(f"{v:+.2f}" for v in ra_["fast"])
      + "), medium " + "/".join(f"{v:+.2f}" for v in rc_["medium"]) + " ((a) " + "/".join(f"{v:+.2f}" for v in ra_["medium"]) + ")")
BSC, DSC = "bridge scale", "demand-layer scale"
gapk = {sc: [c[k]["r_star_capex_on_investment_end_below_pace_keyed_pp"][sc] for k in sp3] for sc in (BSC, DSC)}
ri = {sc: {k: c[k]["r_star_capex_on_investment_start_peak_end"][sc] for k in sp3} for sc in (BSC, DSC)}
mps = {k: m.macro_path(ec, m.deep_tech(ec, **kw)) for k, kw in m.TECH_SPEEDS.items()}
gap_u = [float(mps[k]["r_star"][-1] - ms.r_star_capex_on_investment(ec, mps[k], ms.ALPHA_UNCONVERTED)[-1]) for k in sp3]  # the first report's 0.25
check("F5 a sensitivity, the capex channel keyed to investment / income at the two scales demand.py and bank_scenarios.py use: (c)'s "
      "investment / income falls from the start at every speed, and the investment-keyed neutral rate then never rises above its start, "
      "at either scale, on either root; how far it ends below the pace-keyed r* depends on the scale — about half a point at the "
      "bridge's, several points at the demand layer's (the first report's 'at least a point' held only at alpha_capex's 0.25 used "
      "unconverted). On (b), at a fixed return, investment / income first rises, and the readout rises at the demand layer's scale "
      "but not at the bridge's — the same split as demand R3's (b) with the return following r*",
      all(c[k]["investment_income"]["15.0"] < c[k]["investment_income"]["3.0"] < c[k]["investment_income"]["0.0"] for k in sp3)
      and all(x[k]["investment_income_peak_and_year"][1] == 0.0 for x in (c, h) for k in sp3)
      and all(x[k]["r_star_capex_on_investment_peak_year"][sc] == 0.0 for x in (c, h) for k in sp3 for sc in (BSC, DSC))
      and all(0.0 < g < 1.0 for g in gapk[BSC]) and all(g > 1.0 for g in gapk[DSC]) and all(g > 1.0 for g in gap_u)
      and all(b[k]["investment_income"]["3.0"] > b[k]["investment_income"]["0.0"] and b[k]["investment_income_peak_and_year"][1] > 0.0 for k in sp3)
      and all(b[k]["r_star_capex_on_investment_rise_bp"][DSC] > 0.0 and b[k]["r_star_capex_on_investment_rise_bp"][BSC] == 0.0 for k in sp3),
      "investment / income, medium: " + " ".join(f"{v:.3f}" for v in c["medium"]["investment_income"].values())
      + f"; end below the pace-keyed r*, slow/medium/fast: bridge scale ({SC[BSC]:.4f}) " + " / ".join(f"{g:.2f}" for g in gapk[BSC])
      + f" pp, demand-layer scale ({SC[DSC]:.2f}) " + " / ".join(f"{g:.2f}" for g in gapk[DSC]) + " pp, at 0.25 unconverted "
      + " / ".join(f"{g:.2f}" for g in gap_u) + " pp; ends " + ", ".join(f"{ri[BSC][k][2]:+.2f} / {ri[DSC][k][2]:+.2f}" for k in sp3)
      + f" (pace-keyed {rc_['slow'][2]:+.2f} / {rc_['medium'][2]:+.2f} / {rc_['fast'][2]:+.2f}); (b): investment / income medium "
      + f"{b['medium']['investment_income']['0.0']:.4f} -> {b['medium']['investment_income_peak_and_year'][0]:.4f} at year "
      + f"{b['medium']['investment_income_peak_and_year'][1]:g}, readout rise " + "/".join(f"{b[k]['r_star_capex_on_investment_rise_bp'][DSC]:.1f}" for k in sp3)
      + " bp at the demand layer's scale, " + "/".join(f"{b[k]['r_star_capex_on_investment_rise_bp'][BSC]:.1f}" for k in sp3) + " at the bridge's")
FS = S["sensitivity_fiscal_start"]
fs = FS["scenarios"]
check("F6 the fiscal corollary: the wage-tax share of revenue falls and debt climbs further than in (a) — from a start in surplus (the "
      "bridges' wage tax on all wages); with the wage tax re-centred so the central starts at (b)'s deficit, debt climbs further still, "
      "so the surplus start makes the finding milder, not harsher",
      all(c[k]["wage_tax_share_start_end"][1] < c[k]["wage_tax_share_start_end"][0] - 0.2 for k in sp3)
      and all(c[k]["debt"]["15.0"] > a[k]["debt"]["15.0"] for k in ("medium", "fast"))
      and c["medium"]["deficit_start_end"][0] < 0 and all(abs(fs[k]["deficit_start_end"][0] - FS["target_start_deficit_pct"]) < 0.01 for k in sp3)
      and FS["target_start_deficit_pct"] == round(b["medium"]["deficit_start_end"][0], 4)
      and all(fs[k]["debt"]["15.0"] > c[k]["debt"]["15.0"] for k in sp3),
      f"wage-tax share, medium {c['medium']['wage_tax_share_start_end'][0]:.2f} -> {c['medium']['wage_tax_share_start_end'][1]:.2f}; debt by year 15, "
      f"medium {c['medium']['debt']['15.0']:.0f}% ((a) {a['medium']['debt']['15.0']:.0f}), fast {c['fast']['debt']['15.0']:.0f}% ((a) {a['fast']['debt']['15.0']:.0f}); "
      f"start deficit {c['medium']['deficit_start_end'][0]:+.2f}% ((b) {b['medium']['deficit_start_end'][0]:+.2f}); re-centred (tau_w {FS['tau_w']:.4f} "
      f"for {FS['tau_w_default']:.2f}): medium {fs['medium']['debt']['15.0']:.0f}%, fast {fs['fast']['debt']['15.0']:.0f}%")
F7_ = ("F7 under deep automation capital does not capture the gains, the fixed site does — more so than in (b): along the medium path "
       "(return following r*) interest and machine-chain land fall and the housing site rises to most of income. Part of 'more so' is "
       "the import-as-land channel: the chain's imported content (its share of sigma_V from results/calibration_c.json) is modelled "
       "as machine-chain land drawn from the land endowment, and as the machine stock falls that land is freed to housing — the "
       "chain's share of land rent collapses; the channel's direction on the paths is an open item of (c)")
F8_ = ("F8 a sustained +200 bp on the required return slows automation at every date and raises labour's share at every date — on all "
       "wages and on the paper's Figure 7 basis — more strongly than in (b) (labour's share by over half as much again, the delay three "
       "times and more); the rate elasticity of w/r, 1/sigma_V, is higher, and the response's size scales with it (sigma_V's "
       "construction is an open item of (c): a fixed point, with delta_chain not the chain's own depreciation)")
F9_ = ("F9 the loop: the return follows r*; on the central r* barely rises along the medium path (the gate: the return's largest rise "
       "under 0.01 pp, a threshold, not zero), so the lag phase shrinks to negligible — automation runs behind the fixed-return path "
       "for about two years by under a thousandth of a point of tasks, against (b)'s eight years and a hundredth of a point — and then "
       "runs ahead ((b): lagged while the build-out held rates up, then ran ahead)")
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
          and C["comparator_b"]["max_rho_rise_pp"]["follow"] > 0.1 and lg is not None and lgb is not None
          and lg["deepest_tasks_pp"] < 0 and abs(lg["deepest_tasks_pp"]) * 10 < abs(lgb["deepest_tasks_pp"]) and lg["to_year"] < lgb["to_year"],
          f"largest rise in the return {rise['follow']:+.3f} pp ((b) {C['comparator_b']['max_rho_rise_pp']['follow']:+.3f}); lag phase years "
          f"{lg['from_year']:g}-{lg['to_year']:g}, at most {lg['deepest_tasks_pp']:+.5f} pp of tasks (year {lg['deepest_year']:g}) against (b)'s "
          f"{lgb['from_year']:g}-{lgb['to_year']:g}, {lgb['deepest_tasks_pp']:+.4f} pp; correlation {C['loop_corr_return_vs_tasks']:.2f}; automation "
          f"{C['loop_year15_tasks_ahead_pp']:+.2f} pp ahead by year 15 ((b) {C['comparator_b']['loop_year15_tasks_ahead_pp']:+.2f})")
else:
    for name_ in (F7_, F8_, F9_):
        check(name_, False, f"not computed: a capital run has a date with no land-scarce equilibrium — central {C['errors']}, (b) "
                            f"{C['comparator_b']['errors']}")

fails = [n for n, ok, _ in RESULTS if not ok]
print(f"\n{len(RESULTS) - len(fails)}/{len(RESULTS)} checks passed")
print(f"ALL GREEN ({len(RESULTS)})" if not fails else "FAILURES: " + "; ".join(n.split(' ')[0] for n in fails))
sys.exit(0 if not fails else 1)
