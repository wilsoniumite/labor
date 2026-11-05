# check_basket.py — the basket held at constant utility (pinning_model.BasketEconomy), checked before anything is fitted
# with it. It reads no variant's fit: its economies are the base fit's (results/fit_base.json, seen at breakpoint B) and
# the fit's 1950 starts.
#   N  nesting: with sigma 0 the basket is the fixed one, and the economy is the pinning model's, bit for bit to 1e-12;
#      at p_ref the basket is one unit of goods and h of site, whatever sigma; utility scales the whole basket
#   U  the basket is the cheapest way to the same utility: its CES utility (calibrated share form) equals the reference
#      bundle's at every price, and its goods equal the derivative of its cost in the goods price (Shephard)
#   C  sigma 1 (Cobb-Douglas, a formula of its own) is the limit of the general formula
#   D  as goods cheapen below p_ref, a basket holds more goods and less site
#   L  in equilibrium, at the elasticity set from the data: land adds up (site in baskets plus the machines' land is T),
#      income equals spending on baskets, and labour demand equals supply
# Tolerances set before the first run. N2 failed at the first run (1.9e-11): the site's share was computed as one minus
# the goods' share, which loses digits where h is tiny; the basket now computes each share directly [fixed at its cause].
# Run from us-record/:  python3 checks/check_basket.py      Exit 0 only if every check passes.

import json
import os
import sys
from dataclasses import asdict

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "code"))
import fit_base as F  # noqa: E402

pm = F.pm
RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok)))
    print(f"{'PASS' if ok else 'FAIL'} {name}" + (f" — {detail}" if detail else ""))


def rel(a, b):
    return abs(a - b) / max(abs(b), 1e-300)


base = json.load(open(os.path.join(ROOT, "results", "fit_base.json")))
ECON = F.economies(base["best"]["par"])
for s in F.starts():
    ECON.append(F.economies(s)[0])


def basket_of(e, sigma, p_ref):
    return pm.BasketEconomy(**asdict(e), sigma=sigma, p_ref=p_ref)


# ---- N: nesting
KEYS = ["x", "v", "p", "Ps", "Y", "K", "participation", "labour_share_bea", "theta_V", "income", "n"]
worst = 0.0
for e in ECON:
    q1 = pm.solve(e)
    for p_ref in (0.5 * q1["p"], q1["p"], 3.0 * q1["p"]):
        q2 = pm.solve(basket_of(e, 0.0, p_ref))
        worst = max(worst, max(rel(q2[k], q1[k]) for k in KEYS))
check(f"N1 with sigma 0 the economy is the pinning model's (relative 1e-12), on {len(ECON)} economies at three p_ref",
      worst < 1e-12, f"worst {worst:.1e}")
SIGMAS = (0.3, F.SIGMA_SET, 1.0, 1.5)
worst = 0.0
for e in ECON[::5]:
    for sg in SIGMAS:
        g, s = basket_of(e, sg, 0.7).basket(0.7)
        worst = max(worst, rel(g, 1.0), rel(s, e.h))
check("N2 at p_ref the basket is one unit of goods and h of site, at every sigma (relative 1e-12)", worst < 1e-12,
      f"worst {worst:.1e}")

worst = 0.0
for e in ECON[::5]:
    for sg in SIGMAS:
        for p in (0.1, 0.7, 4.0):
            g1, s1 = basket_of(e, sg, 0.7).basket(p)
            for u in (0.5, 1.52, 3.0):
                g, s = pm.BasketEconomy(**asdict(e), sigma=sg, p_ref=0.7, utility=u).basket(p)
                worst = max(worst, rel(g, u * g1), rel(s, u * s1))
check("N3 utility scales the whole basket: at utility u it is u times the basket at 1 (relative 1e-12) [added with "
      "her note on utility, before its run]", worst < 1e-12, f"worst {worst:.1e}")

# ---- U: the same utility, at least cost
worst_u, worst_d = 0.0, 0.0
for e in ECON[::5]:
    for sg in SIGMAS:
        be = basket_of(e, sg, 1.0)
        th = 1.0 / (1.0 + e.h)
        for p in np.exp(np.linspace(np.log(0.01), np.log(100.0), 21)):
            g, s = be.basket(p)
            if sg == 1.0:
                u = g ** th * (s / e.h) ** (1.0 - th)
            else:
                rr = (sg - 1.0) / sg
                u = (th * g ** rr + (1.0 - th) * (s / e.h) ** rr) ** (1.0 / rr)
            worst_u = max(worst_u, abs(u - 1.0))
            dp = 1e-6 * p
            cost = lambda q: (lambda gs: q * gs[0] + gs[1])(be.basket(q))  # noqa: E731
            worst_d = max(worst_d, rel((cost(p + dp) - cost(p - dp)) / (2.0 * dp), g))
check("U1 the basket's utility is the reference bundle's at every price from 1/100 to 100 times p_ref (1e-10)",
      worst_u < 1e-10, f"worst {worst_u:.1e}")
check("U2 its goods are the derivative of its cost in the goods price (Shephard; central difference, relative 1e-6)",
      worst_d < 1e-6, f"worst {worst_d:.1e}")

# ---- C: Cobb-Douglas as the limit
worst = 0.0
for e in ECON[::5]:
    for p in (0.05, 0.5, 5.0):
        g1, s1 = basket_of(e, 1.0, 1.0).basket(p)
        for sg in (1.0 - 1e-7, 1.0 + 1e-7):
            g2, s2 = basket_of(e, sg, 1.0).basket(p)
            worst = max(worst, rel(g2, g1), rel(s2, s1))
check("C1 sigma 1 agrees with the general formula at 1 -/+ 1e-7 (relative 1e-5)", worst < 1e-5, f"worst {worst:.1e}")

# ---- D: direction
ok = True
for e in ECON[::5]:
    for sg in SIGMAS:
        be = basket_of(e, sg, 1.0)
        prev = (1.0, e.h)
        for p in (0.8, 0.5, 0.2, 0.05):
            g, s = be.basket(p)
            ok &= g > prev[0] and s < prev[1]
            prev = (g, s)
check("D1 as goods cheapen below p_ref, each basket holds more goods and less site, at every sigma above 0", ok)

# ---- L: in equilibrium, at the set elasticity
land, ident, gap, solved = 0.0, 0.0, 0.0, 0
for e in ECON:
    p_ref = pm.solve(e)["p"]
    for f in (1.0, 0.3, 0.1):                             # the year's own price, and goods 3 and 10 times dearer then
        try:
            q = pm.solve(basket_of(e, F.SIGMA_SET, p_ref / f))
        except pm.NoEquilibrium:
            continue
        solved += 1
        land = max(land, rel(q["site_basket"] * q["baskets"] + e.b * e.delta * q["K"], e.T))
        ident = max(ident, rel(q["income"], q["Ps"] * q["baskets"]))
        gap = max(gap, abs(q["nD"] - q["nS"]) / q["nD"])
n_cases = 3 * len(ECON)
check(f"L1 at sigma {F.SIGMA_SET:.4f} (set from the data), land adds up: site in baskets plus the machines' land is T "
      "(relative 1e-12)", land < 1e-12, f"{solved} of {n_cases} solved; worst {land:.1e}")
check("L2 ... income equals spending on baskets (relative 1e-12)", ident < 1e-12, f"worst {ident:.1e}")
check("L3 ... labour demand equals supply (relative 1e-9)", gap < 1e-9, f"worst {gap:.1e}")
check("L4 ... in at least nine in ten of them", solved >= 0.9 * n_cases, f"{solved} of {n_cases}")

n_fail = sum(not ok for _, ok in RESULTS)
print(f"\n{'ALL GREEN' if not n_fail else f'{n_fail} FAILED'} ({len(RESULTS)} checks)")
sys.exit(1 if n_fail else 0)
