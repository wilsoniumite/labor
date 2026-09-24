# regimes.py — expectations as a mixture of regimes: the curve the market shows is an average over worlds.
#
# The market can hold more than one future at once — the peg holds or breaks; wages keep carrying
# consumption or they do not. Each regime j carries its own expected policy path and term premium (a
# curve.CurveState, whose instantaneous forward is f_j(s)). The market's weight on regime j at horizon
# s is w_j(s), summing to one. A zero rate is the average forward, and expectations are linear, so
#     z(T) = (1/T) ∫_0^T  Σ_j w_j(s) f_j(s) ds.
# Two weightings:
#   static   w_j(s) = π_j                     — the regime is decided, only unknown;
#   arrival  the status quo A holds until a new regime B arrives, with eventual probability p and,
#            given that it comes, hazard h:   w_B(s) = p (1 - e^{-h s}),  w_A(s) = 1 - w_B(s).
# Two events then move the curve with no policy move at all:
#   recognition — the market's p rises:  dz/dp = (1/T) ∫ (1 - e^{-hs}) (f_B - f_A) ds, zero at the front
#                 and growing along the curve; h sets how far out it bites;
#   resolution  — uncertainty ends and the curve jumps to one regime's own curve. For two static
#                 regimes the jump to B is (1 - π_B)(z_B - z_A): if the regimes differ by the same
#                 amount at every horizon — a different anchor, policy included — the jump is exactly
#                 parallel. The largest one-day moves of Sweden's 1990–95 record (19 November 1992, the
#                 float: 2Y −210, 5Y −178, 10Y −101 bp, the policy rate unchanged) are such a jump.
# A corollary with teeth for risk: a mixture of distant regimes can show an ordinary, even flat curve.
# The curve then says nothing about the size of the move waiting in either world.

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

import curve as cv

_GL_X, _GL_W = np.polynomial.legendre.leggauss(96)


def _average(fn, T, breaks=()):
    """(1/T) ∫_0^T fn(s) ds by Gauss–Legendre on pieces split at the breakpoints (the delays, where
    forwards kink). Accurate to ~1e-12 for the sums of exponentials used here."""
    T = float(T)
    if T <= 0:
        return float(fn(np.array([0.0]))[0])
    cuts = sorted({0.0, T, *[b for b in breaks if 0.0 < b < T]})
    total = 0.0
    for a, b in zip(cuts[:-1], cuts[1:]):
        s = 0.5 * (b - a) * _GL_X + 0.5 * (b + a)
        total += 0.5 * (b - a) * float(np.dot(_GL_W, fn(s)))
    return total / T


@dataclass(frozen=True)
class StaticMixture:
    """Regimes decided but unknown: weight π_j on regime j at every horizon."""
    states: tuple
    probs: tuple
    names: tuple = ()

    def weights(self, s):
        return [np.full_like(np.asarray(s, dtype=float), p) for p in self.probs]


@dataclass(frozen=True)
class Arrival:
    """A status quo that holds until a new regime arrives: eventual probability p, hazard h (/yr) given
    that it comes. states = (status quo, new regime)."""
    status_quo: cv.CurveState
    new: cv.CurveState
    p: float
    h: float
    names: tuple = ("status quo", "new regime")

    @property
    def states(self):
        return (self.status_quo, self.new)

    def weights(self, s):
        wb = self.p * (1.0 - np.exp(-self.h * np.asarray(s, dtype=float)))
        return [1.0 - wb, wb]


def forward(s, mix):
    """The mixture's instantaneous forward Σ w_j(s) f_j(s)."""
    s = np.asarray(s, dtype=float)
    return sum(w * cv.forward(s, st) for w, st in zip(mix.weights(s), mix.states))


def zero(T, mix):
    """The mixture's zero curve. Static mixtures are exact weighted sums of the regimes' zeros; arrival
    mixtures are averaged numerically."""
    T = np.atleast_1d(np.asarray(T, dtype=float))
    if isinstance(mix, StaticMixture):
        return sum(p * cv.zero(T, st) for p, st in zip(mix.probs, mix.states))
    breaks = [st.delay for st in mix.states]
    return np.array([_average(lambda s: forward(s, mix), t, breaks) for t in T])


def components(T, mix):
    """Each regime's own zero curve: where the curve goes if that regime is the one that happens."""
    return [cv.zero(T, st) for st in mix.states]


def resolution_jumps(T, mix):
    """The jump to each regime's curve if the uncertainty resolved now: z_j(T) - z(T)."""
    z = zero(T, mix)
    return [zj - z for zj in components(T, mix)]


def recognition_mode(T, mix: Arrival):
    """dz/dp for an arrival mixture: (1/T) ∫ (1 - e^{-hs}) (f_new - f_status quo) ds, per unit of p."""
    T = np.atleast_1d(np.asarray(T, dtype=float))
    breaks = [st.delay for st in mix.states]
    g = lambda s: (1.0 - np.exp(-mix.h * s)) * (cv.forward(s, mix.new) - cv.forward(s, mix.status_quo))  # noqa: E731
    return np.array([_average(g, t, breaks) for t in T])
