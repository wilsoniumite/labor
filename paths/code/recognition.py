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
# SPEED (her point, 2026-09-24: markets run on cognitive labour at a human speed; if AI comes to be
# trusted to guide investment decisions, that bottleneck lifts). The market's capacity — information
# processed per quarter, relative to today's market — rises from 1 toward `capacity_end` as trust in AI
# grows. By default trust follows the true world's own technology (the capability being recognised is
# the capability doing the recognising: in the status quo it never arrives); `trust_lead` lets finance
# adopt early, and a (t_mid, width) logistic or a constant sets trust independently of the world.
# Capacity c means the market reads c times as many independent observations: per step of length dt,
# the noise variance is sigma^2 (0.25/dt) / c. Part of the noise, `common`, is shared by all the
# market's AI readings (one model family, one misreading) and does not average away: variance
# common^2 (0.25/dt) + (sigma^2 - common^2)(0.25/dt)/c. A market that is `aware` of the shared part
# weighs its readings correctly; one that is not treats them all as independent and over-updates —
# faster, and more easily fooled.
# Capacity also sets how fast evidence is digested into prices: today's market closes the gap between
# its belief and the belief the evidence supports with half-life `digest` (years; 0 = at once, the pure
# Bayesian learner), and that half-life shortens in proportion to capacity; `digest_share` is the part
# of each change digested that way (the rest is priced at once). Digestion acts on the probability —
# a level, like a forecast, since the market's expected rate is linear in it — which is what the
# evidence measures (yield changes, survey and forward revisions, long-run anchors); in log odds, a
# sliver of overwhelming evidence would already mean certainty. More reading makes recognition earlier; faster
# digestion makes it abrupt — news that a human market prices over weeks gaps in days. (US Treasuries
# measured this once already for rate news: in 1982–94 about a quarter of each 10Y move came over the
# following weeks, half-life about two weeks; since 1995 none — code/digestion_history.py.)
# `refine` puts the macro paths on a finer grid so that moves inside a quarter can be seen.
#
# The curve the market shows is the static mixture (regimes.StaticMixture) of the two worlds' curves,
# weights 1 - p and p. The central bank learns alongside the market: its desired rate is the
# probability-weighted desired rate, delivered by the curve layer's stepwise rule; the policy rate is
# common to both worlds' curves (it is observed). A world's curve at date t, as if that world were
# known: policy now; a cycle target at that world's desired rate a year ahead; a destination at that
# world's average neutral rate over the next ten years plus the target inflation (past the end of the
# simulated path its last value holds — simulate beyond the dates you report); its term premium.
# Resolution — the truth revealed — jumps the curve to the true world's curve: (1 - p)(z_new - z_old).
#
# CALIBRATION (her decision, 2026-09-30). worlds() runs on calibration (c)'s central economy, macro.central() — the open
# (domp) reading, the low root in k — with the required return following r* from that economy's own rho
# (macro.feedback_bridges) and deep automation relative to its own lambda (macro.deep_tech); (b) and (c)'s high root are
# kept by name (calibration="b", "c_hi"), and capital=False stays the flow benchmark (a), which (c) has no analogue of. (c)
# runs on the bridges refit on (c) (macro.Bridges(); Log 46), (a) and (b) on the bridges as tuned on (b) (macro.BRIDGES_B).
# The market's signal stays solve's labor_share — all wages over
# income, the machine chain's labour included (0.554 at (c)'s start, against labour_share_bea's 0.47, the consumption
# chain only, which is (c)'s target; in (b) the two coincide to 0.001). The basis matters on (c): the machine chain's
# labour is the part deep automation removes fastest, so the all-wages signal falls faster early and the market wakes up
# earlier than on the Figure 7 basis (Learning(signal="labour_share_bea"); recognition_scenarios.py stores it as a
# sensitivity). The central economy is read from results/calibration_c.json (BEA; code/calibration_c.py, gated by
# checks/check_calibration_c.py) by macro.central().
#
# Gated by checks/check_recognition.py (and, through the runs built on it, check_speed, check_reverse, check_bank).

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
    capacity_end: float = 1.0        # information per quarter once AI is fully trusted (1: today's human-speed market)
    trust: object = "technology"     # "technology": follows the true world's automation; (t_mid, width) in years; or a constant
    trust_lead: float = 0.0          # years by which trust in AI for investment leads the economy's automation
    common: float = 0.0              # pp: the part of sigma shared by all the market's readings (does not average away)
    aware: bool = True               # the market knows its readings share that error (False: it over-updates)
    digest: float = 0.0              # years: half-life with which today's market prices the evidence (0: at once)
    digest_share: float = 1.0        # the part of each change in the evidence digested at that pace (the rest at once)


def trust_path(old: dict, new: dict, lr: Learning = Learning()):
    """Trust in AI for investment decisions, 0 -> 1, at each date of the paths."""
    t = old["t"]
    if lr.trust == "technology":
        if lr.truth != "new":
            return np.zeros_like(t)
        eta = new["eta"]
        if eta[0] == eta[-1]:
            return np.zeros_like(t)
        prog = (eta[0] - eta) / (eta[0] - eta[-1])
        return np.clip(np.interp(t + lr.trust_lead, t, prog), 0.0, 1.0)
    if isinstance(lr.trust, (int, float)):
        return np.full_like(t, float(lr.trust))
    mid, width = lr.trust
    s = 1.0 / (1.0 + np.exp(-(t - mid) / (width / 4.0)))
    s0 = 1.0 / (1.0 + np.exp(mid / (width / 4.0)))
    return (s - s0) / (1.0 - s0)


def capacity_path(old: dict, new: dict, lr: Learning = Learning()):
    """Information the market processes per quarter, relative to today's market."""
    return 1.0 + (lr.capacity_end - 1.0) * trust_path(old, new, lr)


def learn(old: dict, new: dict, lr: Learning = Learning(), return_logodds: bool = False):
    """The market's probability of the new world at each date of the two (equal-grid) macro paths
    (and, if asked, the log odds, which keep their precision where the probability rounds to 0 or 1).
    Steps may be any length; sigma is per quarterly observation at today's capacity."""
    from scipy.special import expit
    assert 0.0 <= lr.common <= lr.sigma
    t = old["t"]
    s_old, s_new = old[lr.signal] * lr.scale, new[lr.signal] * lr.scale
    truth = s_new if lr.truth == "new" else s_old
    cap = capacity_path(old, new, lr)
    rng = np.random.default_rng(lr.seed) if lr.seed is not None else None
    lo = np.log(lr.p0 / (1.0 - lr.p0))                           # the evidence's log odds
    p_s = lr.p0                                                  # the slowly digested belief (a level, like a forecast)
    out = np.empty_like(t)
    los = np.empty_like(t)
    for i, ti in enumerate(t):
        if i > 0:
            q = 0.25 / (ti - t[i - 1])                           # steps per quarter
            var_c = lr.common ** 2 * q
            var_i = (lr.sigma ** 2 - lr.common ** 2) * q / cap[i]
            var_seen = var_c + var_i if lr.aware else lr.sigma ** 2 * q / cap[i]
            if rng is None:
                s = truth[i]
            elif lr.common == 0.0:
                s = truth[i] + rng.normal(0.0, np.sqrt(var_i))
            else:
                s = truth[i] + rng.normal(0.0, np.sqrt(var_c)) + rng.normal(0.0, np.sqrt(var_i))
            lo += ((s - s_old[i]) ** 2 - (s - s_new[i]) ** 2) / (2.0 * var_seen)
            for when, d in lr.jumps:
                if t[i - 1] < when <= ti:
                    lo += d
            if lr.digest > 0.0:
                p_s += (expit(lo) - p_s) * (1.0 - 0.5 ** ((ti - t[i - 1]) * cap[i] / lr.digest))
        if lr.digest == 0.0:
            los[i], out[i] = lo, expit(lo)
        else:
            out[i] = (1.0 - lr.digest_share) * expit(lo) + lr.digest_share * p_s
            with np.errstate(divide="ignore"):
                los[i] = np.log(out[i]) - np.log1p(-out[i])        # +inf once the belief is exactly 1
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


def refine(mp: dict, dt: float):
    """A macro path on a finer grid (linear between its dates), so moves inside a quarter show."""
    t = mp["t"]
    tf = np.arange(0.0, t[-1] + 1e-9, dt)
    return {k: (np.interp(tf, t, v) if isinstance(v, np.ndarray) and v.shape == t.shape and k != "t" else v)
            for k, v in mp.items()} | {"t": tf}


def crossing(t, p, level):
    """The first date p reaches `level` (linear interpolation), or None."""
    idx = np.nonzero(p >= level)[0]
    if len(idx) == 0:
        return None
    i = int(idx[0])
    if i == 0:
        return float(t[0])
    return float(t[i - 1] + (level - p[i - 1]) / (p[i] - p[i - 1]) * (t[i] - t[i - 1]))


CALIBRATIONS = ("c", "c_hi", "b", "a")


def economy(calibration: str = "c"):
    """(Economy, Bridges) for a two-world run on one calibration (see worlds)."""
    if calibration in ("c", "c_hi"):
        e, _ = m.central("hi" if calibration == "c_hi" else "lo")
        return e, m.feedback_bridges(e)
    if calibration == "b":
        e, _, _, _ = m.calibrate(base=m.CAPITAL_BASE)
        return e, m.feedback_bridges(e, base=m.BRIDGES_B)   # == the pre-switch Bridges(capital_premium=5.0), bit for bit
    if calibration == "a":
        e, _, _, _ = m.calibrate(base=m.CALIBRATION_BASE)
        return e, m.BRIDGES_B
    raise ValueError(f"calibration {calibration!r}: one of {CALIBRATIONS}")


def worlds(years: float = 15.0, dt: float = 0.25, capital: bool = True, tech_new: m.TechPath | None = None,
           calibration: str | None = None):
    """The two worlds — the status quo (technology held at the economy's own start, macro.hold_tech) and a new world
    (medium deep automation relative to the economy's own start, macro.deep_tech, by default) — on one calibration:
      "c"    (the default; her decision, 2026-09-30) calibration (c)'s central economy, macro.central("lo") — the open
             (domp) reading, the low root in k — with the required return following r* from its own rho
             (macro.feedback_bridges: premium rho x 100 - 0.75 = 6.80 pp);
      "c_hi" its high root in k, the sensitivity, the same way;
      "b"    calibration (b), the pre-switch default, kept as the comparator: bit-identical to the pre-switch worlds (the
             helpers give (b)'s hard-coded Bridges(capital_premium=5.0) and TechPath(0.04, 0.01, 6, 6) exactly);
      "a"    the flow benchmark (a) with a fixed return, no feedback — what capital=False has always meant. (c) has no flow
             analogue (its measured machine chain needs A.4's capital), so capital=False stays the (a) comparator.
    capital=False selects "a"; `calibration`, if given, overrides `capital`. Raises macro.NoEquilibrium if a date has no
    land-scarce equilibrium (not at the default bridges on any calibration here)."""
    calibration = calibration or ("c" if capital else "a")
    e, br = economy(calibration)
    tech_new = tech_new or m.deep_tech(e)
    old = m.macro_path(e, m.hold_tech(e), br, years, dt)
    new = m.macro_path(e, tech_new, br, years, dt)
    return e, old, new
