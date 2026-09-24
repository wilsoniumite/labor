# sovereign.py — the anchor-failure state: a sovereign spread over the common curve.
#
# The curve layer prices the common (risk-free, OIS) curve: the average expected policy path plus a
# term premium. A government's own curve adds a spread for the risk that it does not pay in full:
#     z_gov(T) = z_common(T) + spread(T),   spread(T) = (1/T) ∫_0^T E[λ(s) · LGD] ds + c,
# the average expected loss rate (default intensity times loss given default) plus a convenience
# term c — negative for a safe haven whose bonds trade through the common curve, positive for an
# illiquid or distrusted one. The expected loss path reuses the curve layer's cascade: a loss rate
# now, a stress level it heads toward, a long-run level, two speeds, a delay. Fiscal regimes reuse
# regimes.py: stress arrives or not, is recognised, resolves.
#
# What the shapes mean. A stress expected soon and expected to pass gives a humped or inverted spread
# curve (the front pays most — a liquidity crisis). A slow erosion of the tax base — the paper's
# fiscal channel, wage income shrinking as a share of income while transfer needs rise — raises the
# long-run loss level and so lifts the spread from the back: the long end moves first and the front
# barely at all, the same signature as recognition. None of it touches the common curve, so the six
# supervisory rate shocks, defined on the risk-free curve, cannot see it; it is credit-spread risk.
#
# Units: percent and years, as curve.py. The spread's term premium is folded into the loss path;
# convexity ignored.

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

import curve as cv
import regimes as rg


@dataclass(frozen=True)
class SovereignState:
    """The market's expected loss-rate path (a CurveState in loss-rate units: r0 = loss rate now,
    m0 = the stress level it heads toward, rbar = the long-run level) plus a convenience term."""
    loss: cv.CurveState
    convenience: float = 0.0

    @classmethod
    def flat(cls, level, convenience=0.0):
        return cls(cv.CurveState(r0=level, m0=level, rbar=level, tp=0.0), convenience)


def spread(T, sov):
    """Sovereign spread over the common curve at maturity T. `sov` is a SovereignState, or a regime
    mixture (regimes.StaticMixture / regimes.Arrival) whose states are loss paths, with its own
    convenience term given as `sov.convenience` if present (else 0)."""
    T = np.asarray(T, dtype=float)
    if isinstance(sov, SovereignState):
        return cv.zero(T, sov.loss) + sov.convenience
    return rg.zero(T, sov) + getattr(sov, "convenience", 0.0)


def gov_zero(T, common, sov):
    """The government's zero curve: the common curve (a CurveState or a regime mixture) plus the spread."""
    base = cv.zero(T, common) if isinstance(common, cv.CurveState) else rg.zero(T, common)
    return base + spread(T, sov)


def spread_slope(sov, short=2.0, long=10.0):
    """Long minus short spread: positive when the risk sits in the future (erosion), negative when it
    is near and expected to pass (a crunch)."""
    s = spread(np.array([short, long]), sov)
    return float(s[1] - s[0])
