# check_macro.py — the macro block's battery: the paper's Appendix B (SSRN version) reproduced, its
# identities, the calibration, and the bridges' signs.
#
# Run from paths/:  ../venv/Scripts/python.exe checks/check_macro.py
# Exit status 0 only if every check passes.

from __future__ import annotations

import os
import sys
from dataclasses import replace

import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "code"))
import curve as cv  # noqa: E402
import macro as m  # noqa: E402

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


print("P — the paper's Appendix B (SSRN version of 2026-09-23)")
q = m.solve(m.Economy())
paper = dict(x=0.86315, v=0.54344, Y=7.88061, n=1.34338, final_hours=1.07846, machine_hours=0.26492, support_cost=5.44630)
dev = {k: abs(q[k] - val) for k, val in paper.items()}
check("P1 the numerical instance reproduces every published figure to five decimals",
      max(dev.values()) < 5e-6, " ".join(f"{k} {q[k]:.5f}" for k in paper))
seq = []
for eta in (1.0, 0.3, 0.1, 0.03, 0.01):
    e = m.Economy(lam=0.0, g0=eta, g1=eta)                       # gamma_eta(x) = eta (1 + x)
    s = m.solve(e)
    q1 = m._parts(e, 1.0)
    seq.append((eta, s["v"], s["participation"], q1["nS"] > q1["nD"] and e.T > e.N * q1["Ps"]))
check("P2 the paper's automation sequence: v <= 2 b eta / (1 - a), Lemma B.1 holding, participation falling toward 0",
      all(v <= 2 * 0.4 * eta / 0.7 + 1e-12 and ok for eta, v, _, ok in seq) and all(np.diff([p for _, _, p, _ in seq]) < 0),
      "participation " + " ".join(f"{p:.3f}" for _, _, p, _ in seq))

print("I — identities")
rng = np.random.default_rng(923)
errs, land_errs, n_ok = [], [], 0
while n_ok < 60:
    e = m.Economy(N=rng.uniform(1, 5), T=rng.uniform(2, 20), h=rng.uniform(0.1, 2), a=rng.uniform(0.05, 0.5),
                  b=rng.uniform(0.1, 1), lam=rng.uniform(0, 0.1), g0=rng.uniform(0.01, 0.5), g1=rng.uniform(0.2, 1.5),
                  k=rng.uniform(0.5, 6), chi_max=rng.uniform(0.5, 3))
    try:
        s = m.solve(e)
    except (ValueError, AssertionError):
        continue
    n_ok += 1
    errs.append(abs(s["Y"] * s["Ps"] - s["income"]) / s["income"])
    land_errs.append(abs(e.h * s["Y"] + e.b * s["X"] - e.T) / e.T)
check("I1 income: Y Ps = v n + T (Appendix C) at 60 random interior economies", max(errs) < 1e-12, f"max rel err {max(errs):.1e}")
check("I2 land clears: h Y + b X = T", max(land_errs) < 1e-12, f"max rel err {max(land_errs):.1e}")

print("C — the calibrated normal case")
e0, s0, tg, err = m.calibrate()
q1 = m._parts(e0, 1.0)
split = m.income_split(e0, s0)
check("C1 the calibration hits all four targets and Lemma B.1 holds at the start",
      err < 1e-8 and q1["nS"] > q1["nD"] and e0.T > e0.N * q1["Ps"],
      f"labour {s0['labor_share']:.3f}, participation {s0['participation']:.3f}, baskets/person {s0['Y']:.3f}, "
      f"site share {e0.h / s0['Ps']:.3f}; k = {e0.k:.2f}")
check("C2 income splits into labour, the housing site and the machine chains (scarce inputs plus capital income)",
      abs(sum(split.values()) - 1) < 1e-12, " ".join(f"{k} {v:.2f}" for k, v in split.items()))
etas = (1.0, 0.5, 0.3, 0.15, 0.08, 0.04, 0.02)
deep = [m.solve(replace(e0, eta=eta, lam=0.01)) for eta in etas]
rw = np.array([d["real_wage"] for d in deep])
site = np.array([e0.h / d["Ps"] for d in deep])
bound = np.array([d["v"] / (e0.h + e0.b * d["J"] / (1 - e0.a)) for d in deep])
check("C3 deep automation: the basket's site share rises throughout, the real wage in baskets ends far below its start, "
      "and it never exceeds the rent bound (v/r over land per basket, Proposition 4)",
      np.all(np.diff(site) > 0) and rw[-1] < 0.5 * rw[0] and np.all(rw <= bound + 1e-12),
      "real wage " + " ".join(f"{v:.2f}" for v in rw))

print("B — the bridges")
tech = m.TechPath(eta_end=0.04, lam_end=0.01, t_mid=6, width=6)
mp = m.macro_path(e0, tech)
basket = mp["pi_star"] + np.gradient(np.log(mp["Ps"] / mp["Ps"]), mp["t"]) * 100
check("B1 the fork: with the basket on target, goods inflation sits below it and shelter above it while automation runs",
      np.allclose(basket, 2.0) and np.mean(mp["pi_goods"][8:40]) < 2.0 < np.mean(mp["pi_shelter"][8:40]),
      f"mean years 2-10: goods {np.mean(mp['pi_goods'][8:40]):.2f}%, shelter {np.mean(mp['pi_shelter'][8:40]):.2f}%")
check("B2 the fiscal corollary: the wage-tax share of revenue falls and the deficit rises",
      mp["wage_tax_share"][-1] < mp["wage_tax_share"][0] - 0.2 and mp["deficit"][-1] > mp["deficit"][0] + 2,
      f"wage-tax share {mp['wage_tax_share'][0]:.2f} -> {mp['wage_tax_share'][-1]:.2f}; deficit {mp['deficit'][0]:+.1f} -> {mp['deficit'][-1]:+.1f}% of income")
base_br = m.Bridges()
r_cap = m.macro_path(e0, tech, replace(base_br, alpha_rent=0, alpha_fiscal=0))["r_star"]
r_rent = m.macro_path(e0, tech, replace(base_br, alpha_capex=0, alpha_fiscal=0))["r_star"]
r_fis = m.macro_path(e0, tech, replace(base_br, alpha_capex=0, alpha_rent=0))["r_star"]
check("B3 the neutral rate's channels have their stated signs: the build-out raises it, the shift to owners lowers it, "
      "deficits raise it", r_cap.max() > base_br.r0_star + 0.1 and r_rent[-1] < base_br.r0_star - 0.1 and r_fis[-1] > base_br.r0_star + 0.1,
      f"build-out peak +{r_cap.max() - base_br.r0_star:.2f}, owners {r_rent[-1] - base_br.r0_star:+.2f}, fiscal {r_fis[-1] - base_br.r0_star:+.2f} pp")
fast = m.macro_path(e0, m.TechPath(eta_end=0.04, lam_end=0.01, t_mid=3, width=2))
check("B4 on a fast path the neutral rate rises during the build-out and ends below where it started: up now, down later",
      fast["r_star"].max() > fast["r_star"][0] + 0.3 and fast["r_star"][-1] < fast["r_star"][0],
      f"start {fast['r_star'][0]:.2f}, peak {fast['r_star'].max():.2f}, end {fast['r_star'][-1]:.2f}%")
goods = m.macro_path(e0, tech, replace(base_br, mandate="goods"))
check("B5 a mandate that leaves out shelter sets a lower desired rate while goods deflate",
      np.mean(goods["desired"][8:40]) < np.mean(mp["desired"][8:40]),
      f"mean years 2-10: headline {np.mean(mp['desired'][8:40]):.2f}%, goods-only {np.mean(goods['desired'][8:40]):.2f}%")

print("K — into the curve layer")
states, sovs, pol = m.curve_path(mp)
steps = np.diff(pol)
check("K1 policy sits on the 25 bp grid and moves in whole steps; each curve's expected path starts at the policy rate until the next meeting",
      np.allclose(pol / 0.25, np.round(pol / 0.25)) and np.allclose(steps / 0.25, np.round(steps / 0.25))
      and all(abs(float(cv.zero(st.delay * 0.999, st) - cv.term_premium(st.delay * 0.999, st)) - st.r0) < 1e-9 for st in states[1:]),
      f"policy {pol[0]:.2f} -> {pol[-1]:.2f}%")
dest = np.array([st.rbar for st in states])
target = mp["r_star"] + mp["pi_star"]
check("K2 the market's destination learns the macro destination: it closes on r* + pi* by the end",
      abs(dest[-1] - target[-1]) < 0.1, f"destination {dest[-1]:.2f} vs r* + pi* {target[-1]:.2f}%")

n_ok = sum(ok for _, ok, _ in RESULTS)
print(f"\n{n_ok}/{len(RESULTS)} checks passed")
sys.exit(0 if n_ok == len(RESULTS) else 1)
