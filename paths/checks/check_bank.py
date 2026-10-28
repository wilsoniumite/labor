# check_bank.py — the stylised bank: accounting, behaviour, valuation, distributions; findings as found; and the export
# (results/paths_for_banks.csv) built on the same paths.
#
# Since 2026-09-30 (her decision) the paths run on calibration (c)'s central economy (macro.central(): the open reading,
# the low root), with bridges set on (b) and not retuned until the refit of 2026-10-27. Findings F1-F4 were re-run on it and hold as stated; their
# numbers moved (old -> new: paths/STATE.md, the switch entry, "The switch to (c)", and the stylised bank's entry below it,
# each (c) number with (b)'s beside it); F5-F6 are new; R and X gate the switch, the sensitivity
# runs and the export. Thresholds set after seeing (c)'s numbers: F5's 0.3, F6's 0.9, R4's one-half, R5's and X4's bands
# (each is the found value with room, flagged here as set after seeing the data).
# Restated after the switch's reviews: F5 is a central-root result (on the high root the share over the line stays at its
# start, as on (b)) and says so; F6 states the high root's owners'-saving branch (most of the book, not all of it) and gates
# it below the central's (its 0.5, "most", set after seeing the high root's 58%: flagged); X4 computes (b)'s year-10 numbers
# from the (b) export it builds instead of quoting them.
# Restated at the refit (2026-10-27, Log 46; the central on the bridges refit on (c), its two branches macro.BRANCHES; (b) on its
# own, macro.BRIDGES_B and SCEN_B), as found: F5 now holds on the high root too (smaller); R5 is the readout keyed back to the pace
# (the investment key's readout before); F1-F4, F6 hold as stated, numbers moved (STATE Log 46). F5's 0.5 and R5's +1.0 / +0.3 set
# after seeing the refit's numbers (flagged). Corrected at the revision (checks:L1, B1, N2): F1, F3 and F6 held as stated at the
# refit; F2 and F4 were restated (the deficits branch no longer raised rates; F4's label changed without the tag, its gate kept, its
# margin 1.23 -> 0.61); R6 was restated after two of its high-root clauses failed — F2's borrowers clause inverted (8% over the
# line, gated < 0.1) and F4's half-point margin dropped (0.46) — not a narrow pass; X4's bands were all re-set at the refit to its
# values (households' income floor 0.95 -> 0.90, status quo year 5 0.80-0.83 -> 0.78-0.81, the year-10 bands), unflagged.
# Restated at the revision (2026-10-28, Log 54; decisions 93-96: the investment key at Rachel and Smith's coefficient times its
# pass-through, every coefficient per point of income, the start net of the state's asset income, the debt's rate floored, the
# bridges at the start's required return), as found; flagged where set or restated after seeing (the revision's planning runs count
# as seeing; old -> new): F5's high-root clause (18% against its start 7.6% + 5 points -> 10.6%, gated 2 points over its start); R5's
# owners'-saving NII clause (equal under both keys, 0.88 -> 0.90 against 0.89, now within 0.05); R6 restated back to F2-F4's own
# clauses on the high root (its deficits branch 11.6% over the line, F2's 10% met again; F4's half point met, 0.82); X4's bands
# re-set (the deficits branch's site x10 -> x6.75 at year 10, band 9.5-10.5 -> 6.5-7.0; owners' saving's wage bill 0.12 -> 0.143,
# 0.10-0.14 -> 0.12-0.16; its employment 0.43 -> 0.464, 0.41-0.45 -> 0.44-0.48); R7 new (the deficits branch at the investment
# key's pass-through 1 / 0.6 / 0.4 / 0: planning values policy at year 15 1.75 / 2.75 / 3.0 / 4.0%, high root 1.5 / 2.5 / 2.75 /
# 3.5). F2 and F4 carry the moved numbers in their labels. Narrow passes: R5's pace-keyed deficits peak 4.0% against its start +
# 1.0 (one 25 bp step) and NII high 2.54 against 2.41; R6's high-root borrowers clause, 11.6% against 10%. R4 holds vacuously on the
# refit (no world's required return rises: 0.00 pp; (b) 1.80), a regression guard (checks:V1). Narrow passes named later
# (2026-10-28, the record's corrections against the final results, checks:N2 recomputed): F5's high root, 10.6% against its start
# + 2 points (9.6%); F6's high root, 90.8% of the book against the central's 100% ("not all of it"; at the refit 97%); R7's "flat
# at 0.6 (low root) / 0.4 (high root)", equalities on the 25 bp policy grid; X4's bands, set around the found values, closest
# the status quo's site price 0.800 against < 0.81, the deficits branch's employment 0.569 against < 0.58 and households' income
# 0.944 against > 0.90. F4's margin is 0.92 against its half point (at the refit 0.61: checks:L1), no longer narrow.
# Restated at the verification (2026-10-28, Log 54's last bullet; the verifiers' findings, flagged): R1 extended to rebuild every
# stored block the R checks read — the pass-through readout on both roots (R7), the readout keyed to the pace (R5) and the high
# root's runs, calibration and rate rises (R4, R6, F5, F6) — where it rebuilt the central's main runs only (the blocks were equal to
# the code before the extension: a coverage gap, not stale data); R7's label says policy rates (its 0.6 / 0.4 are the policy rate's)
# and R7 gains a clause set after seeing, read off the export (X2 gates it against a fresh build): at the gross reading the deficits
# branch's 10Y falls (to 2.22% at year 8.5 from 2.93%) but is back above its start by year 15 (3.03%; 4.84% by year 25) as the term
# premium rises with debt (150% of income at year 15, the premium 2.09 against 0.30), so "both branches fall" is the policy rate's.
#
# Run from paths/:  ../venv/Scripts/python.exe checks/check_bank.py
# Exit status 0 only if every check passes; prints "ALL GREEN (n)" or the failures.

from __future__ import annotations

import json
import os
import sys
from dataclasses import replace

import numpy as np
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "code"))
import bank as bk  # noqa: E402
import bank_scenarios as bs  # noqa: E402
import export_paths as ex  # noqa: E402
import macro as m  # noqa: E402
import recognition as rc  # noqa: E402
import regimes as rg  # noqa: E402

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


b = bk.Bank()
t = np.arange(0.0, 20.0 + 1e-9, 0.25)
rng = np.random.default_rng(3)

print("A — accounting and behaviour")
pol = np.cumsum(rng.normal(0, 0.3, len(t))) + 2.0
z2 = pol + rng.normal(0, 0.2, len(t))
total, lines, rates = bk.nii(pol, z2, t, b)
check("A1 the NII lines add up exactly to income on assets less cost of liabilities (any path)",
      np.max(np.abs(sum(lines.values()) - total)) < 1e-12)
flat = np.full_like(t, 3.0)
tot_f, lines_f, rates_f = bk.nii(flat, flat + 0.3, t, b)
check("A2 at a constant policy rate everything is settled from the start: NII, deposit mix and margins constant",
      np.ptp(tot_f) < 1e-12 and np.ptp(rates_f["tx_share"]) < 1e-12 and abs(lines_f["mortgage margin"][0] - b.mortgages * b.mortgage_margin) < 1e-12)
step = np.where(t < 2.0, 2.0, 4.5)
_, lines_s, rates_s = bk.nii(step, step, t, b)
beta = (rates_s["deposit_rate"] - rates_s["deposit_rate"][0]) / 2.5
after = t >= 2.0
check("A3 after a rise the deposit pass-through climbs with time held (the windfall decays), and the mortgage margin is squeezed then restored",
      np.all(np.diff(beta[after]) >= -1e-12) and beta[after][1] < beta[after][-1]
      and lines_s["mortgage margin"][after][0] < lines_s["mortgage margin"][0] and abs(lines_s["mortgage margin"][-1] - lines_s["mortgage margin"][0]) < 1e-6,
      f"pass-through {beta[after][1]:.2f} a quarter after, {beta[after][8]:.2f} two years after, {beta[after][-1]:.2f} long after")
low = np.full_like(t, -0.5)
_, lines_l, rates_l = bk.nii(low, low, t, b)
check("A4 below zero, deposit rates stop at zero and lending margins widen by margin_comp per pp",
      np.all(rates_l["deposit_rate"] >= 0) and abs(lines_l["mortgage margin"][-1] / b.mortgages - (b.mortgage_margin + b.margin_comp * (b.margin_from + 0.5))) < 1e-9)

print("V — valuation and distributions")
rent = np.ones_like(t)
z10 = np.full_like(t, 3.0)
hp = bk.house_price(t, np.zeros_like(t), rent, rent, z10, 2.0, b)
z10b = np.where(t < 5, 3.0, 4.0)
hpb = bk.house_price(t, np.zeros_like(t), rent, rent, z10b, 2.0, b)
u0, u1 = (3.0 - 2.0 + b.house_premium) / 100, (4.0 - 2.0 + b.house_premium) / 100
check("V1 flat rents at a constant rate keep the price constant; a permanent rise in the real rate scales it by u0/u1",
      np.ptp(hp) < 1e-9 and abs(hpb[-1] - u0 / u1) < 2e-3, f"{hpb[-1]:.4f} vs {u0 / u1:.4f}")
L = np.exp(rng.normal(np.log(0.7) - 0.35 ** 2 / 2, 0.35, 400_000))
mc = np.mean(np.maximum(0, 1 - 0.8 / L))
out = bk.borrowers(np.array([0.0]), np.array([3.0]), np.array([1.0]), np.array([1.0]), np.array([0.55 / 0.7]), b)
check("V2 loss given default matches a Monte Carlo over lognormal loan-to-values", abs(out["lgd"][0] - mc) < 2e-3, f"{out['lgd'][0]:.4f} vs {mc:.4f}")
D = np.exp(rng.normal(np.log(b.dti_mean) - b.dti_logsd ** 2 / 2, b.dti_logsd, 400_000))
mc2 = np.mean((0.05 + 0.02) * D > b.dsr_line)
out2 = bk.borrowers(np.array([0.0]), np.array([5.0]), np.array([1.0]), np.array([1.0]), np.array([1.0]), b)
check("V3 the share over the debt-service line matches a Monte Carlo over lognormal debt-to-income", abs(out2["share_over_line"][0] - mc2) < 2e-3,
      f"{out2['share_over_line'][0]:.4f} vs {mc2:.4f}")
z3 = np.where(t < 5, 2.0, 5.0)
c = bk.commercial(t, z3, np.ones_like(t), b)
i_pre, i_mid, i_post = (int(np.searchsorted(t, x)) for x in (4.75, 6.5, 8.0))
check("V4 property companies' funding cost moves from the old to the new rate over the refinancing years, and cover falls in proportion",
      abs(c["funding_rate"][i_pre] - (2.0 + b.cre_spread)) < 1e-9 and abs(c["funding_rate"][i_mid] - (1.25 * 4.0 + 0.25 * 5.5 + 1.5 * 7.0) / 3.0) < 0.02   # the grid ramps the step over 4.75-5.0
      and abs(c["funding_rate"][i_post] - (5.0 + b.cre_spread)) < 1e-9
      and abs(c["icr_mean"][i_post] - b.icr_mean * (2.0 + b.cre_spread) / (5.0 + b.cre_spread)) < 1e-9,
      f"funding {c['funding_rate'][i_pre]:.2f} -> {c['funding_rate'][i_mid]:.2f} halfway -> {c['funding_rate'][i_post]:.2f}")

print("F — the findings (results/bank.json, rebuilt by code/bank_scenarios.py; calibration (c), the central; stated as found)")
with open(os.path.join(ROOT, "results", "bank.json"), encoding="utf-8") as f:
    R = json.load(f)
HI, CB = R["sensitivity: the high root"], R["comparator: calibration (b)"]
pt, dd, dw, os_ = R["a pure tightening"], R["deficits dominate"], R["deficits dominate, office rents follow the wage bill"], R["owners' saving dominates"]
OSN, OSW = "owners' saving dominates", "owners' saving dominates, office rents follow the wage bill"
ow, sq = R[OSW], R["status quo"]
check("F1 a pure tightening: NII rises first, the deposit windfall decays while rates are held, house prices fall, then losses peak after NII",
      pt["nii_max"] > pt["nii_start"] + 0.5 and pt["deposit_beta_year_after"] > pt["deposit_beta_at_policy_extreme"]
      and pt["house_real_min_and_year"][0] < 0.9 and pt["losses_max_year"] > pt["nii_max_year"],
      f"NII {pt['nii_start']} -> {pt['nii_max']} (year {pt['nii_max_year']}); pass-through {pt['deposit_beta_at_policy_extreme']} -> {pt['deposit_beta_year_after']}; "
      f"houses {pt['house_real_min_and_year'][0]}; losses peak year {pt['losses_max_year']}")
check("F2 [restated at the refit; numbers at the revision] in the paper's world with deficits dominating (on the refit real rates no "
      "longer rise there: policy falls to 1.75%, at the refit's first run 1.0%), house prices rise while wages fall: the collateral boom "
      "protects the bank, not the borrowers",
      dd["house_real_y5_y10_y15"][1] > 2 and dd["wage_real_y5_y10_y15"][2] < 0.7 and dd["mortgage_loss_rate_max_pct"] < 0.05
      and dd["share_over_dsr_line_max"] > 0.1,
      f"houses x{dd['house_real_y5_y10_y15'][1]} real by year 10; real wage {dd['wage_real_y5_y10_y15'][2]} by 15; "
      f"{dd['share_over_dsr_line_max']:.0%} over the line; mortgage losses {dd['mortgage_loss_rate_max_pct']}% a year")
check("F3 commercial property hangs on one assumption: rents following the wage bill put most of the book below 1.5x cover, following the site almost none",
      dw["cre_share_below_line_max"] > 0.5 and dd["cre_share_below_line_max"] < 0.15,
      f"{dw['cre_share_below_line_max']:.0%} against {dd['cre_share_below_line_max']:.0%}")
check("F4 [restated at the refit] the bank's worst path is the one where owners' saving pulls rates to the floor, not the deficits branch "
      "(where rates rose before the refit and now fall less)",
      os_["nii_min"] < min(dd["nii_min"], pt["nii_min"]) - 0.5, f"NII low {os_['nii_min']} (year {os_['nii_min_year']}) against {dd['nii_min']} and {pt['nii_min']}")
check("F5 [new on (c); restated at the refit and at the revision] the falling-rate branch squeezes borrowers too: money wages fall faster "
      "than mortgage rates, so the share over the debt-service line rises from its start (7.6%) to 60% on the central root and about 11% "
      "on the high root (at the refit 72% and 18%; before it 40% and, on the high root, its start); on (b) it stays at its start",
      os_["share_over_dsr_line_max"] > 0.5 and sq["share_over_dsr_line_max"] < 0.1
      and CB["owners' saving dominates"]["share_over_dsr_line_max"] == CB["status quo"]["share_over_dsr_line_max"]
      and HI["owners' saving dominates"]["share_over_dsr_line_max"] > HI["status quo"]["share_over_dsr_line_max"] + 0.02,
      f"{os_['share_over_dsr_line_max']:.1%} over the line at most against {sq['share_over_dsr_line_max']:.1%} at the start; debt service "
      f"{os_['dsr_mean_max']:.3f} of income at most; (b) {CB[OSN]['share_over_dsr_line_max']:.1%}; "
      f"high root {HI[OSN]['share_over_dsr_line_max']:.1%}")
check("F6 [new on (c)] with office rents following the wage bill, commercial property breaks in both branches: the whole book below 1.5x "
      "cover when owners' saving dominates too on the central root (10% on (b), whose wage bill fell more slowly than funding costs); "
      "on the high root most of the book but not all of it (the share is root-dependent)",
      ow["cre_share_below_line_max"] > 0.9 and dw["cre_share_below_line_max"] > 0.9
      and CB["owners' saving dominates, office rents follow the wage bill"]["cre_share_below_line_max"] < 0.15
      and 0.5 < HI[OSW]["cre_share_below_line_max"] < ow["cre_share_below_line_max"],
      f"{ow['cre_share_below_line_max']:.0%} and {dw['cre_share_below_line_max']:.0%}; (b) "
      f"{CB[OSW]['cre_share_below_line_max']:.0%}; high root "
      f"{HI[OSW]['cre_share_below_line_max']:.0%}")

print("R — the switch to (c), the sensitivities and the readouts")
e, cal = bs.economy("lo")
res, _, rise = bs.bank_runs(e)
rt = lambda o: json.loads(json.dumps(o))  # noqa: E731
eh, calh = bs.economy("hi")
res_h, _, rise_h = bs.bank_runs(eh, "hi")
pace_ = rt(bs.pace_keyed(e))
ptr_ = {"central (c)": rt(bs.pass_through_readout(e, "lo")), "high root": rt(bs.pass_through_readout(eh, "hi"))}
HB = R["sensitivity: the high root"]
check("R1 [extended at the verification] results/bank.json equals a fresh rebuild on macro.central(): the (c) runs (every summary; the "
      "calibration record and rate rises), and every stored block the R checks read — the readout keyed to the pace (R5), the "
      "pass-through readout on both roots (R7), and the high root's runs, calibration and rate rises (R4, R6; F5, F6); until the "
      "verification only the (c) runs were rebuilt",
      all(R[k] == rt(v) for k, v in res.items()) and R["calibration"] == rt(cal)
      and all(R["required_return_rise_pp"][k] == v for k, v in rise.items())
      and R["sensitivity: r* keyed to the pace of tasks"] == pace_
      and all(R["sensitivity: the investment key's pass-through"][r_] == ptr_[r_] for r_ in ptr_)
      and R["sensitivity: the investment key's pass-through"]["pass_throughs"] == list(bs.PASS_THROUGHS)
      and HB == rt({"calibration": calh, "required_return_rise_pp": rise_h, **res_h}),
      f"{len(res)} paths; {cal['tag']}, rho {cal['rho']:.6f}; the pace-keyed readout, the pass-through readout on {len(ptr_)} roots, the "
      f"high root's {len(res_h)} paths ({calh['tag']})")


def path_b_old(e_, bridges, truth, lr=rc.Learning(sigma=1.0, p0=0.05)):
    """The pre-switch bank_scenarios.path, with (b)'s hard-coded objects."""
    br = replace(m.BRIDGES_B, capital_premium=5.0, **bridges)
    old = m.macro_path(e_, m.TechPath(eta_end=1.0, lam_end=e_.lam), br, 25.0, 0.25)
    new = m.macro_path(e_, m.TechPath(eta_end=0.04, lam_end=0.01, t_mid=6, width=6), br, 25.0, 0.25)
    p = rc.learn(old, new, replace(lr, truth=truth))
    mixes, _, _, pol_ = rc.market_curves(old, new, p)
    z = np.array([rg.zero(bs.T, mx) for mx in mixes])
    return old, new, p, pol_, {"2Y": z[:, 0], "3Y": z[:, 1], "10Y": z[:, 2]}


eb, _ = bs.economy("b")
same = []
for name, (bridges, truth) in bs.SCEN_B.items():
    old, new, p, pol_, zeros = path_b_old(eb, bridges, truth)
    for inc in ("site", "employment"):
        if name == "status quo" and inc == "employment":
            continue
        key = name if inc == "site" else f"{name}, office rents follow the wage bill"
        same.append(bs.summary(old["t"], bk.run(old["t"], pol_, zeros, p, old, new, truth=truth, b=bk.Bank(cre_income=inc))) == CB[key])
check("R2 the (b) comparator is the pre-switch bank: rebuilt with (b)'s hard-coded Bridges(capital_premium=5.0) and TechPath(0.04, 0.01) it "
      "equals the stored comparator summary for summary", all(same) and len(same) == 5, f"{sum(same)}/{len(same)} paths identical")
check("R3 the pure tightening is the same on every calibration (its world is the status quo, steady on any economy)",
      pt == HI["a pure tightening"] == CB["a pure tightening"], f"NII peak {pt['nii_max']} on (c), the high root and (b)")
rr = R["required_return_rise_pp"]
check("R4 [its label at the revision] no world's required return leaves the central's rate headroom (beyond it solve raises "
      "NoEquilibrium): the largest rise, deficits dominating, uses under half of it — on the refit no world's required return rises at "
      "all (0.00 pp; (b) 1.80), so the check is a regression guard against leaving the headroom",
      max(rr[k] for k in bs.SCEN) < 0.5 * rr["headroom_pp"] and max(HI["required_return_rise_pp"].values()) < 0.5 * HI["calibration"]["headroom_pp"],
      f"{rr['deficits dominate']:.2f} pp of {rr['headroom_pp']:.2f} (high root {HI['required_return_rise_pp']['deficits dominate']:.2f} of "
      f"{HI['calibration']['headroom_pp']:.2f}; (b) {CB['required_return_rise_pp']['deficits dominate']:.2f})")
IK = R["sensitivity: r* keyed to the pace of tasks"]
ikd, iko = IK["deficits dominate"], IK["owners' saving dominates"]
IV, PK = "investment keyed (the refit)", "pace keyed (as tuned on (b))"
check("R5 [restated at the refit and at the revision] readout (the capex channel keyed back to the pace of tasks, alpha_capex 0.25, not "
      "a finding): the investment-keyed rows are the main runs; keyed to the pace, deficits lift rates again (policy to 4.0%, the bank's "
      "NII up; at the refit 4.75%) where on the refit they fall (to 1.75%; at the refit 1.0%); the owners'-saving branch goes to the floor "
      "either way, its NII low within a twentieth of a point (0.90 against 0.89; at the refit equal) — the two branches' split rests on "
      "the capex key",
      all(ikd[IV][k] == dd[k] for k in bs.IK_FIELDS) and all(iko[IV][k] == os_[k] for k in bs.IK_FIELDS)
      and ikd[PK]["policy_start_peak_end"][1] > ikd[PK]["policy_start_peak_end"][0] + 1.0 > ikd[IV]["policy_start_peak_end"][1] + 1.0
      and ikd[PK]["nii_max"] > ikd[IV]["nii_max"] + 0.3
      and iko[PK]["policy_start_peak_end"][2] == iko[IV]["policy_start_peak_end"][2] == -0.5 and abs(iko[PK]["nii_min"] - os_["nii_min"]) < 0.05,
      f"deficits: policy peak {ikd[IV]['policy_start_peak_end'][1]} (investment) / {ikd[PK]['policy_start_peak_end'][1]} (pace); NII high "
      f"{ikd[IV]['nii_max']} / {ikd[PK]['nii_max']}, low {ikd[IV]['nii_min']} / {ikd[PK]['nii_min']}; 10Y at year 10 "
      f"{ikd[IV]['z10_y5_y10_y15'][1]} / {ikd[PK]['z10_y5_y10_y15'][1]}; owners' saving NII low {iko[IV]['nii_min']} / {iko[PK]['nii_min']}")
check("R6 [restated at the refit and at the revision] sensitivity, the high root: F2-F4 hold there too, as gated on the central — the "
      "deficits branch's borrowers over the debt-service line more than one in ten (12%; at the refit 8%, its start, the clause inverted), "
      "and the owners'-saving branch the worst path by more than half a point (at the refit by 0.46, the margin dropped) — and F5 holds, "
      "smaller",
      HI["deficits dominate"]["house_real_y5_y10_y15"][1] > 2 and HI["deficits dominate"]["wage_real_y5_y10_y15"][2] < 0.7
      and HI["deficits dominate"]["mortgage_loss_rate_max_pct"] < 0.05
      and HI["deficits dominate"]["share_over_dsr_line_max"] > 0.1 and HI["deficits dominate, office rents follow the wage bill"]["cre_share_below_line_max"] > 0.5
      and HI["deficits dominate"]["cre_share_below_line_max"] < 0.15
      and HI["owners' saving dominates"]["nii_min"] < min(HI["deficits dominate"]["nii_min"], pt["nii_min"]) - 0.5,
      f"houses x{HI['deficits dominate']['house_real_y5_y10_y15'][1]}; real wage {HI['deficits dominate']['wage_real_y5_y10_y15'][2]}; "
      f"{HI['deficits dominate']['share_over_dsr_line_max']:.0%} over the line; wage-bill offices "
      f"{HI['deficits dominate, office rents follow the wage bill']['cre_share_below_line_max']:.0%}; NII low {HI[OSN]['nii_min']} against "
      f"{HI['deficits dominate']['nii_min']} (deficits) and {pt['nii_min']}")
PTR = R["sensitivity: the investment key's pass-through"]
PTS = ("1", "0.6", "0.4", "0")
pol15 = {r_: [PTR[r_][p_]["policy_start_peak_end"][2] for p_ in PTS] for r_ in ("central (c)", "high root")}
st0 = {r_: PTR[r_]["1"]["policy_start_peak_end"][0] for r_ in pol15}
main_dd = {"central (c)": dd, "high root": HI["deficits dominate"]}
main_os = {"central (c)": os_, "high root": HI["owners' saving dominates"]}
XP = pd.read_csv(os.path.join(ROOT, "results", "paths_for_banks.csv"))
xd = XP[XP.scenario == "deficits dominate"]
z10, tz = xd["z10Y"].to_numpy(), xd["t_years"].to_numpy()
i_lo = int(np.argmin(z10[tz <= 15 + 1e-9]))
z10_15, z10_25 = float(z10[np.abs(tz - 15) < 1e-9][0]), float(z10[np.abs(tz - 25) < 1e-9][0])
check("R7 [new at the revision, set after seeing; its label and its 10Y clause at the verification] readout, the investment key's "
      "pass-through (decision 93: the share of the investment fall counted as excess saving, 1 gross to 0 netted against capital "
      "consumption), the deficits branch on both roots: at the gross reading (the central, the main runs) both branches' policy rates "
      "fall — the deficits branch's 10Y falls too, but only for a time: it is back above its start by year 15 as the term premium rises "
      "with debt (the export, set after seeing); the deficits branch's policy rate at year 15 rises as less of the fall counts — flat at "
      "a pass-through of 0.6 on the low root and 0.4 on the high root — and stands at or above its start from 0.4 down; with the fall "
      "netted it rises (to 4.0% on the low root, 3.5% on the high root). The bank's two-branch split rests on the pass-through, which "
      "the evidence does not pin",
      PTR["pass_throughs"] == [1.0, 0.6, 0.4, 0.0] and all(PTR[r_][p_]["alpha_inv"] == m.investment_key(float(p_)) for r_ in pol15 for p_ in PTS)
      and all(PTR[r_]["1"][k] == main_dd[r_][k] for r_ in pol15 for k in ("policy_start_peak_end", "nii_min", "nii_max"))
      and all(pol15[r_][0] < st0[r_] and main_os[r_]["policy_start_peak_end"][2] == -0.5 for r_ in pol15)
      and all(np.all(np.diff(pol15[r_]) >= 0) and pol15[r_][2] >= st0[r_] and pol15[r_][3] > st0[r_] for r_ in pol15)
      and pol15["central (c)"][1] == st0["central (c)"] and pol15["high root"][2] == st0["high root"]
      and all(np.all(np.diff([PTR[r_][p_]["r_star_y15"] for p_ in PTS]) > 0) for r_ in pol15)
      and z10[i_lo] < z10[0] < z10_15 < z10_25 and 5 < tz[i_lo] < 15,
      "policy at year 15 at pass-through 1 / 0.6 / 0.4 / 0: " + "; ".join(f"{r_} " + " / ".join(f"{v:g}" for v in pol15[r_]) + f" (start {st0[r_]:g})"
                                                                     for r_ in pol15)
      + f"; the deficits branch's 10Y at the gross reading {z10[0]:.2f}% at the start, {z10[i_lo]:.2f}% at its low (year {tz[i_lo]:g}), "
      f"{z10_15:.2f}% at year 15, {z10_25:.2f}% at 25"
      + "; r* at year 15 " + "; ".join(" / ".join(f"{PTR[r_][p_]['r_star_y15']:+.2f}" for p_ in PTS) for r_ in pol15)
      + "; NII high " + "; ".join(" / ".join(f"{PTR[r_][p_]['nii_max']:.2f}" for p_ in PTS) for r_ in pol15))

print("X — the export (results/paths_for_banks.csv, code/export_paths.py)")
X = pd.read_csv(os.path.join(ROOT, "results", "paths_for_banks.csv"))
COLS = ["scenario", "t_years", "policy", "z3M", "z1Y", "z2Y", "z3Y", "z5Y", "z7Y", "z10Y", "wage_bill_real", "real_wage", "employed",
        "site_rent_real", "site_price_real", "price_level", "income_real", "labor_share"]
n_sc = X.groupby("scenario").size().to_dict()
check("X1 the export keeps its 18 columns, names and order, and adds one last column, the calibration's tag, on every row",
      list(X.columns) == COLS + ["calibration"] and set(X["calibration"]) == {cal["tag"]} and len(X) == 705
      and n_sc == {"status quo": 101, "a pure tightening": 101, "deficits dominate": 101, "owners' saving dominates": 101,
                   "deficits dominate, slow digestion then AI adoption": 301},
      f"{len(X.columns)} columns, last {X.columns[-1]!r} = {cal['tag']!r}; {len(X)} rows")
Xc = ex.build(e, cal["tag"])
check("X2 the export equals a fresh build on the central economy (every cell)", Xc.equals(X), f"{Xc.shape}")
Xb = ex.build(eb, "b", "b")
ptc, ptb = Xc[Xc.scenario == "a pure tightening"].reset_index(drop=True), Xb[Xb.scenario == "a pure tightening"].reset_index(drop=True)
differ = [k for k in COLS if not ptc[k].equals(ptb[k])]
check("X3 the pure tightening's rows are calibration-free but for labor_share (the start's level: 0.554 on (c), 0.47 on (b))",
      differ == ["labor_share"] and abs(ptc["labor_share"][0] - 0.55368) < 5e-6 and abs(ptb["labor_share"][0] - 0.47) < 5e-6, f"differ: {differ}")
with open(os.path.join(ROOT, "results", "deposits_wages.json"), encoding="utf-8") as f:
    hs = json.load(f)["5_nonwage_share_to_households"]


def at(scen, col, y, df=X):
    r_ = df[(df.scenario == scen) & (np.abs(df.t_years - y) < 1e-9)]
    return float(r_[col].iloc[0])


def hh_income(scen, y, share, df=X):
    """Households' real income, start = 1: wages plus `share` of non-wage income (deposits_wages.py's measured share)."""
    ls, ls0 = at(scen, "labor_share", y, df), at(scen, "labor_share", 0.0, df)
    return at(scen, "income_real", y, df) * (ls + share * (1 - ls)) / (ls0 + share * (1 - ls0))


DDn = "deficits dominate"
v = {k: (at(DDn, k, 10.0), at(OSN, k, 10.0)) for k in ("site_price_real", "wage_bill_real", "employed", "income_real")}
SH = ("mean_1996_2025", "mean_2015_2025")
hi_ = [hh_income(sc_, 10.0, hs[s_]) for s_ in SH for sc_ in (DDn, OSN)]
hib = [hh_income(sc_, 10.0, hs[s_], Xb) for s_ in SH for sc_ in (DDn, OSN)]
vb = {k: (at(DDn, k, 10.0, Xb), at(OSN, k, 10.0, Xb)) for k in v}           # (b), from the (b) export built in X3
check("X4 [restated at the refit and at the revision] what the export says at year 10, deficits / owners' saving (as found on the "
      "revised refit; (b)'s numbers, which STATE log 15-16 quoted, are computed from the (b) export beside them): site prices x6.75 / x20 "
      "(x19 by year 5 in the owners' branch; at the refit x10 / x20; before it x2.8 / x19); the wage bill 0.23 / 0.14 (at the refit 0.22 / "
      "0.12; before it 0.30 / 0.18); employment 0.57 / 0.46 (0.56 / 0.43; 0.63 / 0.51); real income x1.34 / x1.33 (x1.34 / x1.32; x1.35 / "
      "x1.33) — the wage bill, employment and income below (b)'s, both site prices above them — so households' income, wages plus the "
      "measured share of non-wage income, is about flat (0.94-1.07 of the start) where on (b) it rose by half or more",
      6.5 < v["site_price_real"][0] < 7.0 and 19.0 < v["site_price_real"][1] < 20.0 and at(OSN, "site_price_real", 5.0) > 18.5
      and 0.20 < v["wage_bill_real"][0] < 0.25 and 0.12 < v["wage_bill_real"][1] < 0.16
      and 0.54 < v["employed"][0] < 0.58 and 0.44 < v["employed"][1] < 0.48
      and 1.3 < v["income_real"][1] < v["income_real"][0] < 1.4 and all(0.90 < x < 1.10 for x in hi_) and all(x > 1.45 for x in hib)
      and 0.78 < at("status quo", "site_price_real", 5.0) < 0.81
      and all(v[k][j] < vb[k][j] for k in ("wage_bill_real", "employed", "income_real") for j in (0, 1))
      and all(v["site_price_real"][j] > vb["site_price_real"][j] for j in (0, 1)),
      f"site x{v['site_price_real'][0]:.2f} / x{v['site_price_real'][1]:.2f} ((b) x{vb['site_price_real'][0]:.2f} / x{vb['site_price_real'][1]:.2f}); "
      f"wage bill {v['wage_bill_real'][0]:.3f} / {v['wage_bill_real'][1]:.3f} ((b) {vb['wage_bill_real'][0]:.3f} / {vb['wage_bill_real'][1]:.3f}); "
      f"employed {v['employed'][0]:.3f} / {v['employed'][1]:.3f} ((b) {vb['employed'][0]:.3f} / {vb['employed'][1]:.3f}); income "
      f"x{v['income_real'][0]:.3f} / x{v['income_real'][1]:.3f} ((b) x{vb['income_real'][0]:.3f} / x{vb['income_real'][1]:.3f}); households' "
      f"income at share {hs[SH[0]]} {hi_[0]:.3f} / {hi_[1]:.3f} ((b) {hib[0]:.3f} / {hib[1]:.3f}), at {hs[SH[1]]} {hi_[2]:.3f} / {hi_[3]:.3f} "
      f"((b) {hib[2]:.3f} / {hib[3]:.3f}); status quo site price {at('status quo', 'site_price_real', 5.0):.3f} at year 5 ((b) "
      f"{at('status quo', 'site_price_real', 5.0, Xb):.3f})")

n_ok = sum(ok for _, ok, _ in RESULTS)
fails = [n for n, ok, _ in RESULTS if not ok]
print(f"\n{n_ok}/{len(RESULTS)} checks passed")
print(f"ALL GREEN ({len(RESULTS)})" if not fails else "FAILURES: " + "; ".join(n.split(" ")[0] for n in fails))
sys.exit(0 if n_ok == len(RESULTS) else 1)
