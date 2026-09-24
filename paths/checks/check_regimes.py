# check_regimes.py — the regime-mixture layer's battery.
#
# Run from paths/:  ../venv/Scripts/python.exe checks/check_regimes.py
# Exit status 0 only if every check passes.

from __future__ import annotations

import os
import sys
from dataclasses import replace

import numpy as np
import sympy as sp
from scipy.integrate import quad

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "code"))
import curve as cv  # noqa: E402
import regimes as rg  # noqa: E402

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


rng = np.random.default_rng(19921119)
Tg = np.array([1 / 12, 0.25, 0.5, 1, 2, 3, 5, 7, 10, 20, 30])


def rand_state():
    return cv.CurveState(r0=rng.uniform(0, 6), m0=rng.uniform(-1, 8), rbar=rng.uniform(0, 6), k1=rng.uniform(0.1, 6),
                         k2=rng.uniform(0.02, 2), tp=rng.uniform(-0.5, 1.5), ktp=rng.uniform(0.05, 1),
                         delay=rng.uniform(0, 0.8))


print("S — identities (sympy)")
s, T, h, p = sp.symbols("s T h p", positive=True)
fA, fB = sp.Function("fA"), sp.Function("fB")
wB = p * (1 - sp.exp(-h * s))
mixed = (1 - wB) * fA(s) + wB * fB(s)
check("S1 the arrival weights sum to one and the mixed forward is f_A + w_B (f_B - f_A)",
      sp.simplify(mixed - (fA(s) + wB * (fB(s) - fA(s)))) == 0)
check("S2 recognition: d/dp of the mixed forward is (1 - e^{-hs}) (f_B - f_A), free of p",
      sp.simplify(sp.diff(mixed, p) - (1 - sp.exp(-h * s)) * (fB(s) - fA(s))) == 0)
piB, zA, zB = sp.symbols("pi_B z_A z_B", real=True)
check("S3 resolution, static: z_B - [(1 - pi_B) z_A + pi_B z_B] = (1 - pi_B)(z_B - z_A)",
      sp.simplify(zB - ((1 - piB) * zA + piB * zB) - (1 - piB) * (zB - zA)) == 0)

print("N — the code")
errs = []
for _ in range(60):
    a, b = rand_state(), rand_state()
    pi = rng.uniform(0, 1)
    m = rg.StaticMixture((a, b), (1 - pi, pi))
    num = [quad(lambda q: float(rg.forward(q, m)), 0, t, points=[x for x in (a.delay, b.delay) if x < t] or None, limit=200)[0] / t
           for t in (0.3, 2.0, 10.0)]
    errs.append(np.max(np.abs(rg.zero(np.array([0.3, 2.0, 10.0]), m) - num)))
check("N1 a static mixture's zero curve is the probability-weighted sum of the regimes' zeros (and their forwards' average)",
      max(errs) < 1e-8, f"max err {max(errs):.1e}")

errs = []
for _ in range(60):
    a, b = rand_state(), rand_state()
    m = rg.Arrival(a, b, p=rng.uniform(0, 1), h=rng.uniform(0.05, 5))
    num = [quad(lambda q: float(rg.forward(q, m)), 0, t, points=[x for x in (a.delay, b.delay) if x < t] or None, limit=200)[0] / t
           for t in (0.1, 1.5, 7.0, 30.0)]
    errs.append(np.max(np.abs(rg.zero(np.array([0.1, 1.5, 7.0, 30.0]), m) - num)))
check("N2 an arrival mixture's zero curve is the average of its mixed forward (quadrature, delays included)",
      max(errs) < 1e-9, f"max err {max(errs):.1e}")

a, b = rand_state(), rand_state()
z0 = rg.zero(Tg, rg.Arrival(a, b, p=0.0, h=1.0))
zslow = rg.zero(Tg[:6], rg.Arrival(a, b, p=1.0, h=1e-7))
zfast = rg.zero(Tg, rg.Arrival(a, b, p=1.0, h=1e6))
check("N3 limits: p = 0 is the status quo; an arrival never expected in the horizon is the status quo; "
      "a certain, immediate arrival is the new regime",
      np.max(np.abs(z0 - cv.zero(Tg, a))) < 1e-12 and np.max(np.abs(zslow - cv.zero(Tg[:6], a))) < 1e-5
      and np.max(np.abs(zfast[3:] - cv.zero(Tg[3:], b))) < 1e-4)

errs = []
for _ in range(40):
    a, b = rand_state(), rand_state()
    m = rg.Arrival(a, b, p=rng.uniform(0.1, 0.9), h=rng.uniform(0.1, 3))
    d = 1e-6
    fd = (rg.zero(Tg, replace(m, p=m.p + d)) - rg.zero(Tg, replace(m, p=m.p - d))) / (2 * d)
    errs.append(np.max(np.abs(fd - rg.recognition_mode(Tg, m))))
check("N4 the recognition mode equals dz/dp by finite differences", max(errs) < 1e-6, f"max err {max(errs):.1e}")

A = cv.CurveState(r0=2.0, m0=3.0, rbar=3.0, k1=1.0, k2=0.3, tp=0.3)
B = replace(A, rbar=5.0, m0=4.0, tp=1.0)                      # same policy now, a higher anchor and premium
rm = rg.recognition_mode(np.concatenate([[1e-4], Tg]), rg.Arrival(A, B, p=0.3, h=0.5))
check("N5 recognition bites from the back: ~0 at the front, rising along the curve when the new regime "
      "differs in destination", abs(rm[0]) < 1e-3 and np.all(np.diff(rm) > 0), " ".join(f"{v:.2f}" for v in rm[1::2]))
h_peaks = []
for hh in (0.2, 1.0, 5.0):
    r = rg.recognition_mode(Tg, rg.Arrival(A, B, p=0.3, h=hh))
    h_peaks.append(float(r[Tg.tolist().index(2)] / r[-1]))
check("N6 the hazard sets how far out recognition bites: a sooner expected arrival moves the 2Y more, relative to 30Y",
      h_peaks[0] < h_peaks[1] < h_peaks[2], "2Y/30Y at h = 0.2, 1, 5: " + " ".join(f"{v:.2f}" for v in h_peaks))

shift = 1.75
Bp = replace(A, r0=A.r0 + shift, m0=A.m0 + shift, rbar=A.rbar + shift)   # the same world, re-anchored by +175 bp
jump = rg.resolution_jumps(Tg, rg.StaticMixture((A, Bp), (0.4, 0.6)))[1]
check("N7 resolution to a re-anchored regime is exactly parallel: (1 - pi_B) x the anchor shift at every maturity",
      np.max(np.abs(jump - 0.4 * shift)) < 1e-12, f"jump {jump[0]*100:.0f} bp at 1M and {jump[-1]*100:.0f} bp at 30Y")
Bt = replace(A, k1=4.0)                                                # same anchor, faster timing
Tw = np.concatenate([[1e-5], Tg, [300.0]])
jt = rg.resolution_jumps(Tw, rg.StaticMixture((A, Bt), (0.4, 0.6)))[1]
check("N8 ... while resolution to a regime that differs only in timing is a hump: -> 0 at both ends, peak inside",
      abs(jt[0]) < 1e-3 * np.max(np.abs(jt)) and abs(jt[-1]) < 0.02 * np.max(np.abs(jt)) and 0 < int(np.argmax(np.abs(jt))) < len(Tw) - 1,
      f"1M {jt[1]*100:+.1f}, peak {np.max(jt)*100:+.1f} at {Tw[np.argmax(jt)]:g}y, 30Y {jt[-2]*100:+.1f}, 300Y {jt[-1]*100:+.2f} bp")

lo = cv.CurveState(r0=1.0, m0=1.0, rbar=1.0, tp=0.0)
hi = cv.CurveState(r0=5.0, m0=5.0, rbar=5.0, tp=0.0)
calm = rg.StaticMixture((lo, hi), (0.5, 0.5))
zc = rg.zero(Tg, calm)
jl, jh = rg.resolution_jumps(Tg, calm)
check("N9 two distant worlds can show a perfectly flat curve: 3% everywhere, with ±200 bp waiting in either resolution",
      np.max(np.abs(zc - 3.0)) < 1e-12 and np.allclose(jl, -2.0) and np.allclose(jh, 2.0))

n_ok = sum(ok for _, ok, _ in RESULTS)
print(f"\n{n_ok}/{len(RESULTS)} checks passed")
sys.exit(0 if n_ok == len(RESULTS) else 1)
