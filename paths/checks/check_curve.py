# check_curve.py — the curve layer's battery: computer algebra for the identities, numerics for the code.
#
# Run from paths/:  ../venv/Scripts/python.exe checks/check_curve.py
# Exit status 0 only if every check passes. Checks gate: nothing downstream uses curve.py until green.

from __future__ import annotations

import os
import sys

import numpy as np
import sympy as sp
from scipy.integrate import quad
from scipy.optimize import brentq

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "code"))
import curve as cv  # noqa: E402
import cycle as cy  # noqa: E402

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


# ------------------------------------------------------------------ S: identities, symbolically
print("S — identities (sympy)")
s, T, x, u = sp.symbols("s T x u", positive=True)
r0, m0, rb, tp = sp.symbols("r0 m0 rbar tp", real=True)
k, k1, k2, ktp = sp.symbols("k k1 k2 ktp", positive=True)
Ls = lambda y: (1 - sp.exp(-y)) / y  # noqa: E731
path = rb + (r0 - rb) * sp.exp(-k1 * s) + (m0 - rb) * k1 / (k1 - k2) * (sp.exp(-k2 * s) - sp.exp(-k1 * s))
zc = rb + (r0 - rb) * Ls(k1 * T) + (m0 - rb) * k1 / (k1 - k2) * (Ls(k2 * T) - Ls(k1 * T))
m_s = rb + (m0 - rb) * sp.exp(-k2 * s)

check("S1 the cascade path solves dr/ds = k1 (m - r) with r(0) = r0",
      sp.simplify(sp.diff(path, s) - k1 * (m_s - path)) == 0 and sp.simplify(path.subs(s, 0) - r0) == 0)
check("S2 the zero curve is the path's average: d(T z)/dT = E[r(T)]",
      sp.simplify(sp.diff(T * zc, T) - path.subs(s, T)) == 0)
check("S3 ... and T z -> 0 as T -> 0 (so z is the average from 0, not up to a constant)",
      sp.limit(T * zc, T, 0) == 0)
z1 = rb + (r0 - rb) * Ls(k * T)
check("S4 timing: in the one-speed curve dz/dk = (rbar - r0)/k * (L(kT) - e^{-kT})",
      sp.simplify(sp.diff(z1, k) - (rb - r0) / k * (Ls(k * T) - sp.exp(-k * T))) == 0)
w = k1 / (k1 - k2) * (Ls(k2 * T) - Ls(k1 * T))
lim = sp.limit(w, k2, k1)
check("S5 equal speeds give Nelson–Siegel: the cascade weight -> L(kT) - e^{-kT} as k2 -> k1",
      sp.simplify(lim - (Ls(k1 * T) - sp.exp(-k1 * T))) == 0)
check("S6 m0 = rbar reduces the cascade to the one-speed curve",
      sp.simplify(zc.subs(m0, rb) - z1.subs(k, k1)) == 0)
tp_T = tp * (1 - Ls(ktp * T))
check("S7 term premium: d(T tp(T))/dT = tp (1 - e^{-ktp T})",
      sp.simplify(sp.diff(T * tp_T, T) - tp * (1 - sp.exp(-ktp * T))) == 0)
xstar_eq = sp.diff(Ls(x) - sp.exp(-x), x)
check("S8 the curvature loading's stationary point satisfies (1 + x) e^{-x} = L(x)",
      sp.simplify(xstar_eq * x - ((1 + x) * sp.exp(-x) - Ls(x))) == 0)

# ------------------------------------------------------------------ N: the code against the algebra
print("N — the code (numpy)")
rng = np.random.default_rng(20260924)


def rand_state(delay=True):
    return cv.CurveState(r0=rng.uniform(-0.5, 5), m0=rng.uniform(-0.5, 6), rbar=rng.uniform(0, 5),
                         k1=rng.uniform(0.05, 5), k2=rng.uniform(0.01, 2), tp=rng.uniform(-0.5, 1.5),
                         ktp=rng.uniform(0.05, 1), delay=rng.uniform(0, 1) if delay else 0.0)


errs = []
for _ in range(200):
    c = rand_state()
    for Tm in (0.05, 0.5, 2.0, 7.0, 30.0):
        avg = quad(lambda q: float(cv.expected_path(q, c)), 0, Tm, points=[c.delay] if c.delay < Tm else None, limit=200)[0] / Tm
        errs.append(abs(float(cv.zero(Tm, c)) - (avg + float(cv.term_premium(Tm, c)))))
check("N1 zero() equals the numerical average of expected_path() plus the term premium (200 states, delay incl.)",
      max(errs) < 1e-8, f"max err {max(errs):.1e}")

errs = []
for _ in range(200):
    c = rand_state()
    for Tm in (0.3, 1.7, 6.0, 25.0):
        if abs(Tm - c.delay) < 1e-3:
            continue
        h = 1e-5
        fd = ((Tm + h) * cv.zero(Tm + h, c) - (Tm - h) * cv.zero(Tm - h, c)) / (2 * h)
        errs.append(abs(float(fd) - float(cv.forward(Tm, c))))
check("N2 forward() equals d(T z)/dT by finite differences", max(errs) < 1e-6, f"max err {max(errs):.1e}")

Tg = np.array([1 / 12, 0.25, 0.5, 1, 2, 3, 5, 7, 10, 20, 30])
errs = []
for _ in range(100):
    c = cv.CurveState.one_speed(rng.uniform(0, 4), rng.uniform(0, 5), rng.uniform(0.05, 5))
    num = cv.loadings(Tg, c)["timing"]                                    # per unit of log k
    ana = c.k1 * cv.timing_loading_one_speed(Tg, c.r0, c.rbar, c.k1)       # per unit of k, times k
    errs.append(np.max(np.abs(num - ana)))
check("N3 the code's timing mode equals the closed form (one speed, no delay)", max(errs) < 1e-5, f"max err {max(errs):.1e}")

flat = cv.CurveState(r0=2.5, m0=2.5, rbar=2.5, k1=0.8, k2=0.3, tp=0.4, delay=0.1)
check("N4 on a flat curve (r0 = m0 = rbar) a timing revision moves nothing",
      np.max(np.abs(cv.loadings(Tg, flat)["timing"])) < 1e-9)
c = cv.CurveState.one_speed(1.8, 3.2, 1.0)
tl = cv.loadings(np.array([1e-6, 1e4]), c)["timing"]
inner = cv.loadings(Tg, c)["timing"]
check("N5 the timing mode is a hump: ~0 at both ends, positive inside when the destination is above policy",
      np.max(np.abs(tl)) < 1e-3 and np.all(inner > 0))

xstar = brentq(lambda y: (1 + y) * np.exp(-y) - cv.L(y), 0.5, 5.0)
xs = np.linspace(0.01, 10, 200001)
check("N6 the curvature loading peaks at x* ~ 1.7933 (timing hump peaks at maturity 1.79/k)",
      abs(xs[np.argmax(cv.curvature_loading(xs))] - xstar) < 1e-3 and abs(xstar - 1.7933) < 1e-3, f"x* = {xstar:.4f}")

ks = np.geomspace(1e-4, 200, 60)
taus = np.array([cv.timing_share(cv.CurveState.one_speed(1.0, 3.0, kk)) for kk in ks])
floor = (1.5 - 1 / 24) / (7.5 - 1 / 24)   # k -> 0: the path drifts linearly, forwards sit at interval midpoints
check("N7 the timing share rises with speed, from the slow-drift floor (1.5 - 1/24)/(7.5 - 1/24) ~ 0.196 toward 1",
      np.all(np.diff(taus) > -1e-12) and abs(taus[0] - floor) < 1e-3 and taus[-1] > 0.98, f"tau {taus[0]:.4f} .. {taus[-1]:.4f}")
td = [cv.timing_share(cv.CurveState.one_speed(1.0, 3.0, 0.5, delay=dd)) for dd in (0.0, 1.0, 2.0, 3.0)]
check("N7b a timing share below the floor needs a delay: holding policy for >= 2 years gives exactly 0",
      td[0] > td[1] > td[2] and abs(td[2]) < 1e-12 and abs(td[3]) < 1e-12, "tau at delay 0/1/2/3y: " + " ".join(f"{v:.3f}" for v in td))

a = cv.CurveState(r0=1.0, m0=3.5, rbar=2.5, k1=1.3, k2=1.3, tp=0.0)
b = cv.CurveState(r0=1.0, m0=3.5, rbar=2.5, k1=1.3, k2=1.3 * (1 + 1e-6), tp=0.0)
ns = 2.5 + (1.0 - 2.5) * cv.L(1.3 * Tg) + (3.5 - 2.5) * cv.curvature_loading(1.3 * Tg)
check("N8 equal speeds reproduce Nelson–Siegel, continuously across the k1 = k2 branch",
      np.max(np.abs(cv.zero(Tg, a) - ns)) < 1e-12 and np.max(np.abs(cv.zero(Tg, b) - ns)) < 1e-5)

rule = cv.PolicyRule(meetings_per_year=8, step=0.25, max_steps=4, inertia=0.5)
t, rp = rule.simulate(0.0, lambda q: 4.0, 5.0)
moves = np.diff(np.concatenate([[0.0], rp]))
check("N9 the policy rule moves in whole steps, at most max_steps a meeting, and settles on target",
      np.allclose(moves / 0.25, np.round(moves / 0.25)) and np.max(np.abs(moves)) <= 1.0 + 1e-12 and abs(rp[-1] - 4.0) < 1e-12,
      "path " + " ".join(f"{v:.2f}" for v in rp[:6]))
phi = 0.3
gap = np.array([(1 - phi) ** n for n in range(1, 17)])
cont = np.exp(-cv.PolicyRule(meetings_per_year=8, inertia=phi).implied_speed() * np.arange(1, 17) / 8)
check("N10 the rule's implied speed -M ln(1 - inertia) matches its unrounded meeting path", np.max(np.abs(gap - cont)) < 1e-12)

# ------------------------------------------------------------------ C: the stylised cycle
print("C — a stylised cycle through the three clocks")
d = cy.CycleDrivers()
times, states, rates, t_first = cy.simulate(d)
Tc = np.array([1 / 12, 0.25, 0.5, 1, 2, 3, 4, 5, 7, 10, 15, 20, 30])


def at(tq):
    return states[int(np.argmin(np.abs(times - tq)))]


def dz(ta, tb):
    return (cv.zero(Tc, at(tb)) - cv.zero(Tc, at(ta))) * 100


A = dz(d.t_news - 0.02, t_first - 1 / 12 - 0.02)   # ends while the first move is still > 1 month away
B = dz(t_first - 0.02, t_first + 0.75)
W = dz(d.t_news - 0.02, 3.5)
pol = (rates[int(np.argmin(np.abs(times - 3.5)))] - rates[int(np.argmin(np.abs(times - (d.t_news - 0.02))))]) * 100
sh = cv.sot_shapes(Tc)
_, r2par = cv.fit_share(W, sh["parallel"][:, None])
check("C1 pricing phase (news -> a month before the first move): the 1M is pinned and the move is a hump",
      abs(A[0]) < 0.5 and 0 < int(np.argmax(A)) < len(Tc) - 1, f"1M {A[0]:+.3f}, peak {A.max():+.0f} bp at {Tc[np.argmax(A)]:.2g}y, 30Y {A[-1]:+.0f}")
check("C2 delivery phase: the front catches up — the largest move is at the short end",
      Tc[int(np.argmax(B))] <= 1.0 and B[0] > B[-1], f"1M {B[0]:+.0f}, 2Y {B[4]:+.0f}, 30Y {B[-1]:+.0f}")
check("C3 whole cycle: the front moves with policy and the cumulative move is close to parallel, front-heavy",
      abs(W[0] - pol) < 10 and np.all(np.diff(W[3:]) <= 1e-9) and r2par > 0.7,
      f"1M {W[0]:+.0f} vs policy {pol:+.0f}, 10Y {W[9]:+.0f}, 30Y {W[-1]:+.0f}, parallel R² {r2par:.2f}")

n_ok = sum(ok for _, ok, _ in RESULTS)
print(f"\n{n_ok}/{len(RESULTS)} checks passed")
sys.exit(0 if n_ok == len(RESULTS) else 1)
