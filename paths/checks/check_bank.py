# check_bank.py — the stylised bank: accounting, behaviour, valuation, distributions; findings as found.
#
# Run from paths/:  ../venv/Scripts/python.exe checks/check_bank.py
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
import bank as bk  # noqa: E402

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

print("F — the findings (results/bank.json, rebuilt by code/bank_scenarios.py; stated as found)")
R = json.load(open(os.path.join(ROOT, "results", "bank.json"), encoding="utf-8"))
pt, dd, dw, os_ = R["a pure tightening"], R["deficits dominate"], R["deficits dominate, office rents follow the wage bill"], R["owners' saving dominates"]
check("F1 a pure tightening: NII rises first, the deposit windfall decays while rates are held, house prices fall, then losses peak after NII",
      pt["nii_max"] > pt["nii_start"] + 0.5 and pt["deposit_beta_year_after"] > pt["deposit_beta_at_policy_extreme"]
      and pt["house_real_min_and_year"][0] < 0.9 and pt["losses_max_year"] > pt["nii_max_year"],
      f"NII {pt['nii_start']} -> {pt['nii_max']} (year {pt['nii_max_year']}); pass-through {pt['deposit_beta_at_policy_extreme']} -> {pt['deposit_beta_year_after']}; "
      f"houses {pt['house_real_min_and_year'][0]}; losses peak year {pt['losses_max_year']}")
check("F2 in the paper's world with real rates rising, house prices rise while wages fall: the collateral boom protects the bank, not the borrowers",
      dd["house_real_y5_y10_y15"][1] > 2 and dd["wage_real_y5_y10_y15"][2] < 0.7 and dd["mortgage_loss_rate_max_pct"] < 0.05
      and dd["share_over_dsr_line_max"] > 0.1,
      f"houses x{dd['house_real_y5_y10_y15'][1]} real by year 10; real wage {dd['wage_real_y5_y10_y15'][2]} by 15; "
      f"{dd['share_over_dsr_line_max']:.0%} over the line; mortgage losses {dd['mortgage_loss_rate_max_pct']}% a year")
check("F3 commercial property hangs on one assumption: rents following the wage bill put most of the book below 1.5x cover, following the site almost none",
      dw["cre_share_below_line_max"] > 0.5 and dd["cre_share_below_line_max"] < 0.15,
      f"{dw['cre_share_below_line_max']:.0%} against {dd['cre_share_below_line_max']:.0%}")
check("F4 the bank's worst path is the one where owners' saving pulls rates to the floor, not the one where they rise",
      os_["nii_min"] < min(dd["nii_min"], pt["nii_min"]) - 0.5, f"NII low {os_['nii_min']} against {dd['nii_min']} and {pt['nii_min']}")

n_ok = sum(ok for _, ok, _ in RESULTS)
print(f"\n{n_ok}/{len(RESULTS)} checks passed")
sys.exit(0 if n_ok == len(RESULTS) else 1)
