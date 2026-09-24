# check_sovereign.py — the anchor-failure (sovereign spread) battery.
#
# Run from paths/:  ../venv/Scripts/python.exe checks/check_sovereign.py
# Exit status 0 only if every check passes.

from __future__ import annotations

import os
import sys
from dataclasses import replace

import numpy as np
from scipy.integrate import quad

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "code"))
import curve as cv  # noqa: E402
import regimes as rg  # noqa: E402
import sovereign as sv  # noqa: E402

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


rng = np.random.default_rng(1994)
Tg = np.array([1 / 12, 0.25, 0.5, 1, 2, 3, 5, 7, 10, 20, 30])
common = cv.CurveState(r0=2.0, m0=2.5, rbar=2.75, k1=1.0, k2=0.3, tp=0.4, delay=1 / 12)

print("N — the spread and the government curve")
errs = []
for _ in range(80):
    loss = cv.CurveState(r0=rng.uniform(0, 1), m0=rng.uniform(0, 4), rbar=rng.uniform(0, 2), k1=rng.uniform(0.1, 5),
                         k2=rng.uniform(0.02, 2), tp=0.0, delay=rng.uniform(0, 0.5))
    sov = sv.SovereignState(loss, convenience=rng.uniform(-0.5, 0.5))
    for t in (0.5, 3.0, 10.0):
        avg = quad(lambda q: float(cv.expected_path(q, loss)), 0, t, points=[loss.delay] if loss.delay < t else None,
                   limit=200)[0] / t
        errs.append(abs(float(sv.spread(t, sov)) - (avg + sov.convenience)))
check("N1 the spread is the average expected loss rate plus the convenience term", max(errs) < 1e-9, f"max err {max(errs):.1e}")

sov = sv.SovereignState.flat(0.8, convenience=-0.2)
check("N2 the government curve is the common curve plus the spread; a flat loss rate gives a flat spread",
      np.max(np.abs(sv.gov_zero(Tg, common, sov) - cv.zero(Tg, common) - 0.6)) < 1e-12)

T_sh = np.array([1 / 12, 2.0, 10.0])
before = cv.zero(T_sh, common)
widen = sv.SovereignState.flat(2.0)
after_common = cv.zero(T_sh, common)
check("N3 the spread never moves the common curve: a sovereign widening is invisible to shocks defined on it",
      np.array_equal(before, after_common) and np.all(sv.gov_zero(T_sh, common, widen) - before > 1.99))

crunch = sv.SovereignState(cv.CurveState(r0=0.5, m0=6.0, rbar=0.5, k1=8.0, k2=1.5, tp=0.0))   # stress now, expected to pass
erosion = sv.SovereignState(cv.CurveState(r0=0.3, m0=0.3, rbar=3.0, k1=0.15, k2=0.15, tp=0.0))  # a long-run loss level rising slowly
sc, se = sv.spread(Tg, crunch), sv.spread(Tg, erosion)
check("N4 a crunch expected to pass humps or inverts the spread curve; a slow erosion slopes it up",
      sv.spread_slope(crunch) < 0 and 0 < int(np.argmax(sc)) < len(Tg) - 1 and sv.spread_slope(erosion) > 0 and np.all(np.diff(se) > 0),
      f"crunch 2Y {sc[4]:.2f} / 10Y {sc[8]:.2f}; erosion 2Y {se[4]:.2f} / 10Y {se[8]:.2f}")

calm = cv.CurveState(r0=0.2, m0=0.2, rbar=0.2, tp=0.0)
stressed = replace(calm, m0=1.0, rbar=2.5, k1=0.5)          # the fiscal base erodes: a higher long-run loss
fis = rg.Arrival(calm, stressed, p=0.2, h=0.4)
rec = rg.recognition_mode(np.concatenate([[1e-4], Tg]), fis)
check("N5 recognising a fiscal regime moves the spread from the back: ~0 at the front, rising along the curve",
      abs(rec[0]) < 1e-3 and np.all(np.diff(rec) > 0),
      f"per 10 points of p: 2Y {rec[5]*0.1*100:.1f} bp, 10Y {rec[9]*0.1*100:.1f} bp, 30Y {rec[-1]*0.1*100:.1f} bp")

conv_flip = sv.SovereignState.flat(0.0, convenience=0.5)
haven = sv.SovereignState.flat(0.0, convenience=-0.3)
jump = sv.gov_zero(Tg, common, conv_flip) - sv.gov_zero(Tg, common, haven)
check("N6 a safe haven losing its convenience value moves the whole government curve in parallel, with no default risk at all",
      np.allclose(jump, 0.8), f"{jump[0]*100:.0f} bp at every maturity")

n_ok = sum(ok for _, ok, _ in RESULTS)
print(f"\n{n_ok}/{len(RESULTS)} checks passed")
sys.exit(0 if n_ok == len(RESULTS) else 1)
