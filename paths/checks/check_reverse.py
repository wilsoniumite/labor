# check_reverse.py — reverse stress testing, part 1: the dial space, the sampler, the statistics, the run.
#
# Run from paths/:  ../venv/Scripts/python.exe checks/check_reverse.py
# Exit status 0 only if every check passes.

from __future__ import annotations

import os
import sys
from dataclasses import replace

import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "code"))
import macro as m  # noqa: E402
import recognition as rc  # noqa: E402
import regimes as rg  # noqa: E402
import reverse as rv  # noqa: E402

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


e, _, _, _ = m.calibrate(base=m.CAPITAL_BASE)
D0 = rv.Dials()

print("U — the dial space and the sampler")
u0 = rv.to_unit(D0)
back = rv.from_unit(u0)
check("U1 the defaults sit inside the ranges, and unit -> dials -> unit is the identity (log dials included)",
      np.all((u0 > 0) & (u0 < 1)) and all(abs(getattr(back, k) - getattr(D0, k)) < 1e-12 for k in rv.NAMES),
      "defaults in the unit cube: " + " ".join(f"{k} {x:.2f}" for k, x in zip(rv.NAMES, u0)))
mid = rv.from_unit(np.full(len(rv.NAMES), 0.5))
check("U2 a log dial's midpoint is the geometric mean of its range, a linear dial's the arithmetic mean",
      all(abs(getattr(mid, k) - (np.sqrt(lo * hi) if k in rv.LOG else (lo + hi) / 2)) < 1e-12 for k, (lo, hi) in rv.RANGES.items()))
n = 500
U = rv.sample(n)
strata = np.floor(U * n).astype(int)
check("U3 the Latin hypercube puts exactly one draw in each 1/n stratum of every dial",
      all(np.array_equal(np.sort(strata[:, j]), np.arange(n)) for j in range(U.shape[1])))

print("S — the statistics")
rng = np.random.default_rng(1)
x = rng.normal(size=2000)
check("S1 rank correlation is +1 under any increasing transform, -1 under a decreasing one, near 0 for independent draws",
      abs(rv.rank_corr(x, np.exp(3 * x)) - 1) < 1e-12 and abs(rv.rank_corr(x, -x ** 3) + 1) < 1e-12
      and abs(rv.rank_corr(x, rng.normal(size=2000))) < 0.1)
Us = np.array([[0.5, 0.5], [0.9, 0.9], [0.6, 0.5], [0.1, 0.1], [0.45, 0.2]])
vals = np.array([0.0, 150.0, 120.0, -200.0, -90.0])
j_up, d_up = rv.nearest_breach(Us, vals, 100.0, np.array([0.5, 0.5]))
j_dn, d_dn = rv.nearest_breach(Us, vals, -100.0, np.array([0.5, 0.5]))
j_no, _ = rv.nearest_breach(Us, vals, 500.0, np.array([0.5, 0.5]))
check("S2 nearest breach: the closest draw among those reaching the threshold, by sign; none if nothing reaches it",
      j_up == 2 and abs(d_up - 0.1) < 1e-12 and j_dn == 3 and j_no is None)

print("R — the run")
o0 = rv.run(e, D0, lookahead=0.0)
_, old, new = rc.worlds()
p = rc.learn(old, new, rc.Learning(sigma=D0.sigma, p0=D0.p0))
mixes, _, _, _ = rc.market_curves(old, new, p)
z = np.array([rg.zero(np.array([10.0]), mx)[0] for mx in mixes])
t = old["t"]
i10, i90 = max(int(np.searchsorted(t, rc.crossing(t, p, 0.1))) - 1, 0), int(np.searchsorted(t, rc.crossing(t, p, 0.9)))
check("R1 at the default dials (no look-ahead) the run is the recognition model: the same 10Y move over the window",
      abs(o0["recog_10Y"] - (z[i90] - z[i10]) * 100) < 1e-9, f"{o0['recog_10Y']:+.2f} bp")
o1 = rv.run(e, D0)
check("R2 simulating ten years past the horizon changes the default run little (its new world has settled by year 15)",
      abs(o1["recog_10Y"] - o0["recog_10Y"]) < 1.0 and abs(o1["ten_year_10Y"] - o0["ten_year_10Y"]) < 10.0,
      f"10Y over ten years {o0['ten_year_10Y']:+.1f} -> {o1['ten_year_10Y']:+.1f} bp")
lo_rent, hi_rent = rv.run(e, replace(D0, alpha_rent=0.02)), rv.run(e, replace(D0, alpha_rent=0.15))
lo_fis, hi_fis = rv.run(e, replace(D0, alpha_fiscal=0.0)), rv.run(e, replace(D0, alpha_fiscal=0.3))
check("R3 the two bridges that decide direction move the 10Y as their sign says: owners' saving down, deficits up",
      hi_rent["ten_year_10Y"] < lo_rent["ten_year_10Y"] and hi_fis["ten_year_10Y"] > lo_fis["ten_year_10Y"],
      f"alpha_rent .02 -> .15: {lo_rent['ten_year_10Y']:+.0f} -> {hi_rent['ten_year_10Y']:+.0f} bp; "
      f"alpha_fiscal 0 -> .3: {lo_fis['ten_year_10Y']:+.0f} -> {hi_fis['ten_year_10Y']:+.0f} bp")
check("R4 more public support means more public debt; shallower automation means a higher real-wage low point",
      rv.run(e, replace(D0, public_support=0.5))["debt_max"] > o1["debt_max"]
      and rv.run(e, replace(D0, eta_end=0.3))["real_wage_min_rel"] > o1["real_wage_min_rel"])
deep = rv.Dials(eta_end=0.037, width=1.42, t_mid=7.83, alpha_capex=0.985, alpha_rent=0.192, alpha_fiscal=0.367,
                tp_per_debt=0.004, debt_threshold=83.0, public_support=0.515, capital_premium=3.98, sigma=1.79, p0=0.107)
od = rv.run(e, deep, keep_paths=True)
check("R5 in a draw that drives the neutral rate far below zero, policy stops at the lower bound and the 10Y stops falling",
      od["policy_min"] >= -0.5 - 1e-12 and od["r_star_min"] + 2.0 < -0.5
      and np.ptp(od["_paths"]["z"][-12:, 2]) * 100 < 10.0,
      f"r* low {od['r_star_min']:+.1f}%, policy low {od['policy_min']:+.2f}%, 10Y range over the last 3 years "
      f"{np.ptp(od['_paths']['z'][-12:, 2]) * 100:.1f} bp")


def flips(rs, thr=0.25):
    d = np.diff(rs)
    return int(np.sum((d[1:] * d[:-1] < 0) & (np.minimum(np.abs(d[1:]), np.abs(d[:-1])) > thr)))


def rstar(d, hl):
    br = m.Bridges(capital_premium=d.capital_premium, alpha_capex=d.alpha_capex, alpha_rent=d.alpha_rent,
                   alpha_fiscal=d.alpha_fiscal, tp_per_debt=d.tp_per_debt, debt_threshold=d.debt_threshold,
                   public_support=d.public_support, rho_halflife=hl)
    return m.macro_path(e, m.TechPath(eta_end=d.eta_end, lam_end=0.01, t_mid=d.t_mid, width=d.width), br, 25, 0.25)["r_star"]


f1 = np.array([flips(rstar(rv.from_unit(u), 1.0)) for u in U[:300]])
f0 = flips(rstar(deep, 0.0))
check("R6 with the required return adjusting (half-life 1 year) no draw cycles quarter to quarter; following last quarter's r* at once can",
      f1.max() <= 1 and f0 >= 10, f"300 draws: at most {f1.max()} reversal(s) of more than 25 bp; the deep draw undamped: {f0}")

n_ok = sum(ok for _, ok, _ in RESULTS)
print(f"\n{n_ok}/{len(RESULTS)} checks passed")
sys.exit(0 if n_ok == len(RESULTS) else 1)
