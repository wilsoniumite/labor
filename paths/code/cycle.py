# cycle.py — a rate cycle as three clocks driving the curve layer.
#
# A fundamental change arrives at t_news: the central bank's desired rate moves (the cycle) and the
# long-run destination moves (the macro). Three clocks turn that into curve states over time:
#   institutions — the central bank acts only after a lag, at meetings, in steps (curve.PolicyRule);
#   recognition  — the market learns the new cycle target and the new destination with half-lives,
#                  and comes to expect the bank's speed of adjustment;
#   technology   — enters here only through the destination path, supplied from outside (the macro
#                  block that paths/ will add; this file takes it as a driver).
# Everything the market prices is a CurveState; the policy rate r0 is the bank's actual rate.

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from curve import CurveState, PolicyRule


@dataclass(frozen=True)
class CycleDrivers:
    t_news: float = 0.25          # years: when the fundamental change arrives
    desired_before: float = 0.0   # the bank's desired rate before the news (%)
    desired_after: float = 4.0    # ... after it: the cycle target
    rbar_before: float = 1.0      # long-run destination before the news (%)
    rbar_after: float = 2.5       # ... after it
    cb_lag: float = 0.5           # institutions clock: years from news to the first move
    h_cycle: float = 0.15         # recognition clock: half-life of the market's learning of the cycle target
    h_dest: float = 0.75          # ... of the destination (slower)
    k1_before: float = 0.2        # timing belief before the news (/yr): a slow drift
    k2: float = 0.5               # speed at which the cycle target returns to the destination (/yr)
    tp: float = 0.3               # term premium at the long end (%)


def _learn(before, after, t, t0, half_life):
    if t < t0:
        return before
    return before + (after - before) * (1.0 - 0.5 ** ((t - t0) / half_life))


def simulate(d: CycleDrivers, rule: PolicyRule = PolicyRule(), years: float = 4.0, dt: float = 1 / 52):
    """Weekly curve states over `years`. Returns (times, states, policy rates, first-move time)."""
    M = rule.meetings_per_year
    meet = np.arange(1, int(years * M) + 1) / M
    t_first = d.t_news + d.cb_lag
    r, k_rule = d.desired_before, rule.implied_speed()
    times = np.arange(0.0, years + 1e-12, dt)
    states, rates, mi = [], [], 0
    for t in times:
        while mi < len(meet) and meet[mi] <= t + 1e-12:
            desired = d.desired_after if meet[mi] >= t_first - 1e-12 else d.desired_before
            r = rule.decide(r, desired)
            mi += 1
        m_mkt = _learn(d.desired_before, d.desired_after, t, d.t_news, d.h_cycle)
        rbar_mkt = _learn(d.rbar_before, d.rbar_after, t, d.t_news, d.h_dest)
        k1_mkt = _learn(d.k1_before, k_rule, t, d.t_news, d.h_cycle)
        next_meet = meet[mi] - t if mi < len(meet) else 1.0 / M
        # the market knows the lag: before the first move it expects policy to hold until then
        delay = max(t_first - t, next_meet) if t >= d.t_news else next_meet
        states.append(CurveState(r0=r, m0=m_mkt, rbar=rbar_mkt, k1=k1_mkt, k2=d.k2, tp=d.tp, delay=delay))
        rates.append(r)
    return times, states, np.array(rates), t_first
