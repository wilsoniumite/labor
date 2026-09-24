# recognition.py — the recognition clock as a mixture: the market learns which world it is in.
#
# Two worlds, each a full macro path (macro.macro_path): the status quo, and a new world in which
# automation proceeds. The market does not know which it is in. Each quarter it observes a signal — by
# default labour's share of income, measured with noise sigma — and updates the log odds of the new
# world by Bayes' rule with Gaussian likelihoods:
#     d log odds = [(s - s_old)^2 - (s - s_new)^2] / (2 sigma^2).
# Observing the truth without noise, the expected increment is (s_new - s_old)^2 / (2 sigma^2): the
# market learns only as fast as the two worlds' signals separate relative to the noise, so a gradual
# change can be recognised late and then quickly. A narrative shock — a jump in the odds with no new
# data — can be added as `jumps`.
#
# The curve the market shows is the static mixture (regimes.StaticMixture) of the two worlds' curves,
# weights 1 - p and p. The central bank learns alongside the market: its desired rate is the
# probability-weighted desired rate, delivered by the curve layer's stepwise rule; the policy rate is
# common to both worlds' curves (it is observed). A world's curve at date t, as if that world were
# known: policy now; a cycle target at that world's desired rate a year ahead; a destination at that
# world's average neutral rate over the next ten years plus the target inflation (past the end of the
# simulated path its last value holds — simulate beyond the dates you report); its term premium.
# Resolution — the truth revealed — jumps the curve to the true world's curve: (1 - p)(z_new - z_old).

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

import curve as cv
import macro as m
import regimes as rg


@dataclass(frozen=True)
class Learning:
    signal: str = "labor_share"      # the statistic the market watches (a key of the macro path)
    scale: float = 100.0             # converts the signal to the units of sigma (labour share to pp)
    sigma: float = 1.0               # measurement noise, in those units, per quarterly observation
    p0: float = 0.05                 # the market's prior probability of the new world
    truth: str = "new"               # which world the data come from
    seed: int | None = None          # None: noiseless observations (the expected learning path)
    jumps: tuple = ()                # ((year, change in log odds), ...): narrative shocks


def learn(old: dict, new: dict, lr: Learning = Learning(), return_logodds: bool = False):
    """The market's probability of the new world at each date of the two (equal-grid) macro paths
    (and, if asked, the log odds, which keep their precision where the probability rounds to 0 or 1)."""
    from scipy.special import expit
    t = old["t"]
    s_old, s_new = old[lr.signal] * lr.scale, new[lr.signal] * lr.scale
    truth = s_new if lr.truth == "new" else s_old
    rng = np.random.default_rng(lr.seed) if lr.seed is not None else None
    lo = np.log(lr.p0 / (1.0 - lr.p0))
    out = np.empty_like(t)
    los = np.empty_like(t)
    for i, ti in enumerate(t):
        if i > 0:
            s = truth[i] + (rng.normal(0.0, lr.sigma) if rng is not None else 0.0)
            lo += ((s - s_old[i]) ** 2 - (s - s_new[i]) ** 2) / (2.0 * lr.sigma ** 2)
            for when, d in lr.jumps:
                if t[i - 1] < when <= ti:
                    lo += d
        los[i] = lo
        out[i] = expit(lo)
    return (out, los) if return_logodds else out


def _world_state(mp: dict, i: int, r0: float, delay: float, rule: cv.PolicyRule, horizon: float = 10.0,
                 k2: float = 0.3, elb: float = -0.5):
    t = mp["t"]
    ahead = np.linspace(t[i], t[i] + horizon, 81)          # a full window always; past the path's end, its last value holds
    rbar = max(float(np.mean(np.interp(ahead, t, mp["r_star"]))) + mp["pi_star"], elb)   # expectations respect the lower bound
    m0 = max(float(np.interp(t[i] + 1.0, t, mp["desired"])), elb)
    return cv.CurveState(r0=r0, m0=m0, rbar=rbar, k1=rule.implied_speed(), k2=k2, tp=float(mp["tp"][i]), delay=delay)


def market_curves(old: dict, new: dict, p: np.ndarray, rule: cv.PolicyRule | None = None, elb: float = -0.5):
    """Per date: the market's mixture, the two worlds' own curves, and the common policy rate."""
    rule = rule or cv.PolicyRule()
    t = old["t"]
    desired = (1.0 - p) * old["desired"] + p * new["desired"]
    M = rule.meetings_per_year
    r = max(round(float(desired[0]) / rule.step) * rule.step, elb)
    next_meet = 1.0 / M
    mixes, olds, news, policy = [], [], [], []
    for i, ti in enumerate(t):
        while ti + 1e-12 >= next_meet:
            r = max(rule.decide(r, max(float(np.interp(next_meet, t, desired)), elb)), elb)
            next_meet += 1.0 / M
        so = _world_state(old, i, r, next_meet - ti, rule, elb=elb)
        sn = _world_state(new, i, r, next_meet - ti, rule, elb=elb)
        olds.append(so); news.append(sn)
        mixes.append(rg.StaticMixture((so, sn), (1.0 - float(p[i]), float(p[i]))))
        policy.append(r)
    return mixes, olds, news, np.array(policy)


def crossing(t, p, level):
    """The first date p reaches `level` (linear interpolation), or None."""
    idx = np.nonzero(p >= level)[0]
    if len(idx) == 0:
        return None
    i = int(idx[0])
    if i == 0:
        return float(t[0])
    return float(t[i - 1] + (level - p[i - 1]) / (p[i] - p[i - 1]) * (t[i] - t[i - 1]))


def worlds(years: float = 15.0, dt: float = 0.25, capital: bool = True, tech_new: m.TechPath | None = None):
    """The two worlds on the calibrated economy — (b) with the return following r* by default: the status
    quo (technology fixed) and a new world (medium deep automation by default)."""
    e, _, _, _ = m.calibrate(base=m.CAPITAL_BASE if capital else m.CALIBRATION_BASE)
    br = m.Bridges(capital_premium=5.0) if capital else m.Bridges()
    tech_new = tech_new or m.TechPath(eta_end=0.04, lam_end=0.01, t_mid=6, width=6)
    old = m.macro_path(e, m.TechPath(eta_end=1.0, lam_end=e.lam), br, years, dt)
    new = m.macro_path(e, tech_new, br, years, dt)
    return e, old, new
