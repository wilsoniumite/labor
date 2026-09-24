# check_recognition.py — the recognition clock as a mixture: Bayes, the market curve, resolution, narrative.
#
# Run from paths/:  ../venv/Scripts/python.exe checks/check_recognition.py
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
import recognition as rc  # noqa: E402
import regimes as rg  # noqa: E402

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


e, old, new = rc.worlds()
t = old["t"]
logit = lambda p: np.log(p / (1 - p))  # noqa: E731

print("L — learning")
p_same = rc.learn(old, old, rc.Learning(sigma=1.0, p0=0.05))
check("L1 two worlds with the same signal teach nothing: the probability stays at the prior", np.allclose(p_same, 0.05))
lr = rc.Learning(sigma=1.0, p0=0.05)
p = rc.learn(old, new, lr)
d = (new["labor_share"] - old["labor_share"]) * 100
closed = logit(0.05) + np.concatenate([[0.0], np.cumsum(d[1:] ** 2 / 2.0)])
_, lo = rc.learn(old, new, lr, return_logodds=True)
check("L2 noiseless learning is the closed form: log odds = logit(p0) + sum (s_new - s_old)^2 / (2 sigma^2)",
      np.max(np.abs(lo - closed)) < 1e-9 * max(1.0, np.max(np.abs(closed))), f"final log odds {lo[-1]:.1f}")
p_old = rc.learn(old, new, replace(lr, truth="old"))
check("L3 if the data come from the status quo, the probability of the new world only falls",
      np.all(np.diff(p_old) <= 1e-15) and p_old[-1] < 1e-6)
cross = [rc.crossing(t, rc.learn(old, new, replace(lr, sigma=s)), 0.5) for s in (0.5, 1.0, 2.0, 4.0)]
check("L4 noisier data mean later recognition: the date the probability crosses one half rises with sigma",
      all(c is not None for c in cross) and np.all(np.diff(cross) > 0), "sigma 0.5/1/2/4 pp: " + " ".join(f"{c:.2f}" for c in cross))
pj = rc.learn(old, old, rc.Learning(sigma=1.0, p0=0.05, jumps=((2.0, 3.0),)))
i2 = int(np.argmin(np.abs(t - 2.0)))
check("L5 a narrative shock moves the log odds by exactly its size, with no new data",
      abs((logit(pj[i2]) - logit(pj[i2 - 1])) - 3.0) < 1e-12 and np.allclose(pj[:i2], 0.05))

print("M — the market curve")
mixes, olds, news, pol = rc.market_curves(old, new, p)
T = np.array([1 / 12, 0.25, 1, 2, 5, 10, 30])
err = max(np.max(np.abs(rg.zero(T, mx) - ((1 - p[i]) * cv.zero(T, olds[i]) + p[i] * cv.zero(T, news[i]))))
          for i, mx in enumerate(mixes))
check("M1 the market curve is the probability-weighted mix of the two worlds' curves", err < 1e-12, f"max err {err:.1e}")
i = int(np.argmin(np.abs(t - 3.0)))
jump = cv.zero(T, news[i]) - rg.zero(T, mixes[i])
check("M2 revealing the truth jumps the curve by (1 - p)(z_new - z_old)",
      np.max(np.abs(jump - (1 - p[i]) * (cv.zero(T, news[i]) - cv.zero(T, olds[i])))) < 1e-12,
      f"at year 3 (p {p[i]:.2f}): 2Y {jump[3]*100:+.1f}, 10Y {jump[5]*100:+.1f}, 30Y {jump[6]*100:+.1f} bp")
desired = (1 - p) * old["desired"] + p * new["desired"]
check("M3 the policy rate is common to both worlds' curves, sits on the 25 bp grid, and tracks the probability-weighted desired rate",
      all(o.r0 == n.r0 for o, n in zip(olds, news)) and np.allclose(pol / 0.25, np.round(pol / 0.25))
      and np.max(np.abs(pol - desired)) < 0.5, f"max gap to desired {np.max(np.abs(pol - desired)):.2f} pp")

print("S — the baseline scenario (default bridges; scenario-dependent, stated as found)")
ls_done = (new["labor_share"][0] - np.interp(cross[1], t, new["labor_share"])) / (new["labor_share"][0] - new["labor_share"][-1])
check("S1 with noiseless data and sigma 1 pp, the market is past one half before a tenth of the labour-share fall has happened",
      ls_done < 0.1, f"crosses 1/2 at year {cross[1]:.2f}, with {ls_done*100:.1f}% of the fall done")
iy0, iy5 = 0, int(np.argmin(np.abs(t - 5.0)))
z0, z5 = rg.zero(T, mixes[iy0]), rg.zero(T, mixes[iy5])
check("S2 under the default bridges, waking up lowers the long end (the new world's future neutral rate averages lower)",
      z5[-1] < z0[-1] and z5[-2] < z0[-2], f"year 0 -> 5: 2Y {(z5[3]-z0[3])*100:+.0f}, 10Y {(z5[5]-z0[5])*100:+.0f}, 30Y {(z5[6]-z0[6])*100:+.0f} bp")

n_ok = sum(ok for _, ok, _ in RESULTS)
print(f"\n{n_ok}/{len(RESULTS)} checks passed")
sys.exit(0 if n_ok == len(RESULTS) else 1)
