# curve.py — the curve layer of paths/: policy, cycle target, destination, speed, term premium, basis.
#
# The market's expected policy path is a two-stage cascade (a central-tendency model):
#     dr/ds = k1 (m - r),    dm/ds = k2 (rbar - m)
# policy r moves toward the cycle target m at speed k1; m drifts toward the long-run destination
# rbar at speed k2. Solving from (r0, m0):
#     E[r(s)] = rbar + (r0 - rbar) e^{-k1 s} + (m0 - rbar) k1/(k1 - k2) (e^{-k2 s} - e^{-k1 s})
# Averaging over [0, T] gives the expectations part of the zero curve:
#     z(T) = rbar + (r0 - rbar) L(k1 T) + (m0 - rbar) k1/(k1 - k2) (L(k2 T) - L(k1 T)),
#     L(x) = (1 - e^{-x}) / x.
# Two special cases carry the argument (both machine-checked in checks/check_curve.py):
#   m0 = rbar      -> the one-speed curve  z = rbar + (r0 - rbar) L(kT);
#   k1 = k2 = lam  -> Nelson–Siegel: level rbar, slope r0 - rbar, curvature m0 - rbar, the cascade
#                     behind the arbitrage-free Nelson–Siegel model of Christensen, Diebold and
#                     Rudebusch (2011).
# The timing result: in the one-speed curve, dz/dk = (rbar - r0)/k * (L(kT) - e^{-kT}) — the
# Nelson–Siegel curvature loading scaled by the gap. A revision of *when* policy arrives moves the
# curve in a hump whose size is the slope; on a flat curve it cannot occur.
#
# The front is pinned: policy only changes at meetings, so the market expects r0 to hold for a delay d
# (time to the next move it prices) and the cascade to start from there. With d > 0,
#     z(T) = r0 for T <= d,   z(T) = [d r0 + (T - d) zc(T - d)] / T for T > d   (zc: the cascade above).
#
# Units: rates in percent, maturities in years. Convexity is ignored (expectations + an additive term
# premium); the term premium and the basis are add-ons, not derived from a pricing kernel.

from __future__ import annotations

from dataclasses import dataclass, replace

import numpy as np


def L(x):
    """(1 - e^{-x}) / x, with the x -> 0 limit 1 (series below 1e-6)."""
    x = np.asarray(x, dtype=float)
    small = np.abs(x) < 1e-6
    xs = np.where(small, 1.0, x)
    return np.where(small, 1.0 - x / 2.0 + x * x / 6.0, (1.0 - np.exp(-xs)) / xs)


def curvature_loading(x):
    """Nelson–Siegel curvature loading L(x) - e^{-x}: zero at 0 and at infinity, peak at x* ~ 1.793."""
    return L(x) - np.exp(-np.asarray(x, dtype=float))


@dataclass(frozen=True)
class CurveState:
    """One date's curve state. r0: policy now. m0: the cycle target the market expects policy to reach.
    rbar: the long-run destination. k1: speed toward the cycle target (/yr) — the timing belief.
    k2: speed at which the cycle target itself returns to rbar (/yr). tp: term premium at the long end;
    ktp: how fast it builds with maturity. basis: flat interbank-over-OIS spread (e.g. STIBOR vs OIS).
    delay: years for which the market expects policy to hold at r0 before the cascade starts (the
    meeting calendar, forward guidance)."""
    r0: float
    m0: float
    rbar: float
    k1: float = 1.0
    k2: float = 0.2
    tp: float = 0.0
    ktp: float = 0.25
    basis: float = 0.0
    delay: float = 0.0

    @classmethod
    def one_speed(cls, r0, rbar, k, **kw):
        """The one-speed curve: the cycle target is the destination."""
        return cls(r0=r0, m0=rbar, rbar=rbar, k1=k, **kw)


def _cascade_weight(k1, k2, T):
    """k1/(k1 - k2) (L(k2 T) - L(k1 T)), continuous through k1 = k2 (the Nelson–Siegel curvature)."""
    T = np.asarray(T, dtype=float)
    if abs(k1 - k2) < 1e-9 * max(1.0, k1):
        return curvature_loading(k1 * T)
    return k1 / (k1 - k2) * (L(k2 * T) - L(k1 * T))


def _path_weight(k1, k2, s):
    """k1/(k1 - k2) (e^{-k2 s} - e^{-k1 s}), continuous through k1 = k2 (k s e^{-k s})."""
    s = np.asarray(s, dtype=float)
    if abs(k1 - k2) < 1e-9 * max(1.0, k1):
        return k1 * s * np.exp(-k1 * s)
    return k1 / (k1 - k2) * (np.exp(-k2 * s) - np.exp(-k1 * s))


def _cascade_path(u, c: CurveState):
    return c.rbar + (c.r0 - c.rbar) * np.exp(-c.k1 * u) + (c.m0 - c.rbar) * _path_weight(c.k1, c.k2, u)


def _cascade_zero(u, c: CurveState):
    return c.rbar + (c.r0 - c.rbar) * L(c.k1 * u) + (c.m0 - c.rbar) * _cascade_weight(c.k1, c.k2, u)


def expected_path(s, c: CurveState):
    """E[r(s)]: the market's expected policy rate s years ahead (no term premium): r0 until the delay,
    then the cascade."""
    s = np.asarray(s, dtype=float)
    u = np.maximum(s - c.delay, 0.0)
    return np.where(s <= c.delay, c.r0, _cascade_path(u, c))


def term_premium(T, c: CurveState):
    """Additive term premium tp (1 - L(ktp T)): zero at the front, tp at the long end."""
    return c.tp * (1.0 - L(c.ktp * np.asarray(T, dtype=float)))


def zero(T, c: CurveState):
    """Zero rate at maturity T (OIS): the average expected policy rate over [0, T] plus the term premium."""
    T = np.asarray(T, dtype=float)
    if c.delay <= 0.0:
        ez = _cascade_zero(T, c)
    else:
        u = np.maximum(T - c.delay, 0.0)
        Ts = np.maximum(T, 1e-12)
        ez = np.where(T <= c.delay, c.r0, (c.delay * c.r0 + u * _cascade_zero(u, c)) / Ts)
    return ez + term_premium(T, c)


def zero_projection(T, c: CurveState):
    """Zero rate on the interbank projection curve (e.g. STIBOR-3M): OIS plus the basis."""
    return zero(T, c) + c.basis


def forward(T, c: CurveState):
    """Instantaneous forward d(T z)/dT = E[r(T)] + tp (1 - e^{-ktp T})."""
    T = np.asarray(T, dtype=float)
    return expected_path(T, c) + c.tp * (1.0 - np.exp(-c.ktp * T))


def forward_between(a, b, c: CurveState):
    """Simple-average forward rate between maturities a < b, from the zero curve."""
    return (b * zero(b, c) - a * zero(a, c)) / (b - a)


def timing_share(c: CurveState, front=1 / 12):
    """tau = (f(1,2) - z(front)) / (f(5,10) - z(front)): the share of the policy-to-destination gap
    priced to close within one to two years. The empirical statistic of the SEK and US measurements."""
    r_front = zero(front, c)
    return (forward_between(1, 2, c) - r_front) / (forward_between(5, 10, c) - r_front)


# ---------------------------------------------------------------- modes: what each state moves
MODES = ("policy", "cycle target", "destination", "timing", "term premium")


def loadings(T, c: CurveState, h=1e-6):
    """The curve's response to a unit move in each state (percentage points per unit; timing per
    unit of log k1). Central differences on the closed form — exact up to O(h^2)."""
    T = np.asarray(T, dtype=float)
    out = {}
    for name, field, scale in (("policy", "r0", 1.0), ("cycle target", "m0", 1.0),
                               ("destination", "rbar", 1.0), ("term premium", "tp", 1.0)):
        up = replace(c, **{field: getattr(c, field) + h})
        dn = replace(c, **{field: getattr(c, field) - h})
        out[name] = (zero(T, up) - zero(T, dn)) / (2 * h) * scale
    up, dn = replace(c, k1=c.k1 * np.exp(h)), replace(c, k1=c.k1 * np.exp(-h))
    out["timing"] = (zero(T, up) - zero(T, dn)) / (2 * h)
    return out


def timing_loading_one_speed(T, r0, rbar, k):
    """Closed form dz/dk for the one-speed curve with no delay: (rbar - r0)/k * (L(kT) - e^{-kT})."""
    return (rbar - r0) / k * curvature_loading(k * np.asarray(T, dtype=float))


# ---------------------------------------------------------------- the policy rule (institutions clock)
@dataclass(frozen=True)
class PolicyRule:
    """A central bank that meets `meetings_per_year` times and closes a fraction `inertia` of the gap
    to its desired rate per meeting, in multiples of `step`, at most `max_steps` steps per meeting."""
    meetings_per_year: int = 8
    step: float = 0.25
    max_steps: int = 4
    inertia: float = 0.5

    def decide(self, r, desired):
        """Close `inertia` of the gap, rounded half away from zero to whole steps; a gap of at least
        one step always gets at least one step (otherwise the last step would never be taken)."""
        gap = desired - r
        n = int(np.sign(gap) * np.floor(abs(self.inertia * gap / self.step) + 0.5))
        if n == 0 and abs(gap) >= self.step - 1e-12:
            n = int(np.sign(gap))
        n = max(-self.max_steps, min(self.max_steps, n))
        return r + n * self.step

    def implied_speed(self):
        """The continuous speed k with the same per-meeting gap closure: -M ln(1 - inertia)."""
        return -self.meetings_per_year * np.log(1.0 - self.inertia)

    def simulate(self, r0, desired_fn, years, start=0.0):
        """Policy path on the meeting calendar: returns (meeting times, rate after each meeting)."""
        dt = 1.0 / self.meetings_per_year
        t = start + dt * np.arange(1, int(round(years * self.meetings_per_year)) + 1)
        r, out = r0, []
        for ti in t:
            r = self.decide(r, desired_fn(ti))
            out.append(r)
        return t, np.array(out)


# ---------------------------------------------------------------- the supervisory shapes, for comparison
def sot_shapes(T):
    """The six BCBS d368 §132 shapes as unit loadings (parallel, short, steepener, flattener;
    down-shocks are the negatives). S_short = e^{-T/4}, S_long = 1 - e^{-T/4}."""
    T = np.asarray(T, dtype=float)
    s, l = np.exp(-T / 4.0), 1.0 - np.exp(-T / 4.0)
    return {"parallel": np.ones_like(T), "short": s, "steepener": -0.65 * s + 0.90 * l,
            "flattener": 0.80 * s - 0.60 * l, "S_short": s, "S_long": l}


def sot_label(shape, coef):
    """Name a fitted single shape with its direction. The SOT set has parallel and short shocks in both
    directions but steepener and flattener in one direction only; a negative fit on those is named as
    the reversed shape and flagged as outside the SOT set."""
    if shape in ("parallel", "short"):
        return f"{shape} {'up' if coef >= 0 else 'down'}"
    return shape if coef >= 0 else f"reverse {shape} (not an SOT shock)"


def best_sot(y, T):
    """The single SOT shape (either sign) that best fits a move y at maturities T: (label, R^2, scale)."""
    sh = sot_shapes(T)
    fits = {k: fit_share(y, sh[k][:, None]) for k in ("parallel", "short", "steepener", "flattener")}
    k = max(fits, key=lambda q: fits[q][1])
    b, r2 = fits[k]
    return sot_label(k, float(b[0])), float(r2), float(b[0])


def fit_share(y, X):
    """Least squares y ~ X b (no intercept); uncentred R^2 = share of the squared move explained."""
    y = np.asarray(y, dtype=float)
    X = np.atleast_2d(np.asarray(X, dtype=float))
    if X.shape[0] != y.shape[0]:
        X = X.T
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    r = y - X @ b
    return b, 1.0 - (r @ r) / (y @ y)
