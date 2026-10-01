# reverse.py — reverse stress testing, part 1: the envelope of outcomes across the model's dials.
#
# The openness principle keeps structure fixed and makes behaviour swappable; the behaviour lives in
# named coefficients. This file turns them — with the technology path and the market's learning — over
# broad stated ranges (not estimates), runs the two-world recognition model for each draw, and asks:
# how large can the curve's moves get, which dials drive them, and what is the smallest departure from
# the defaults that produces a given move? Part 2 — a bank's exposure profile applied to these paths —
# belongs where the bank's numbers are, not in this public repository.
#
# CALIBRATION (her decision, 2026-09-30). run() takes the economy as an argument; reverse_envelope.py passes calibration
# (c)'s central economy (macro.central()) and, as the comparator, (b). The dials are relative to the economy where they
# must be: the new world's lambda falls to a fifth of the economy's own start (macro.deep_tech; (b)'s 0.05 -> 0.01), the
# status quo holds it (macro.hold_tech), and the capital premium is a shift from the economy's own premium
# (macro.capital_premium: rho x 100 - r0*, 5.0 on (b), 6.80 on the central), so its range, +-2 pp, is centred on each
# economy's own required return — on (b) the pre-switch 3-7 pp. Beyond the central's rate headroom (7.18 pp) a date has
# no land-scarce equilibrium and macro.solve raises NoEquilibrium; run() lets it propagate and first_failure() finds the
# date, so the envelope counts and reports such draws rather than dropping them. The central economy is read from
# results/calibration_c.json (BEA; code/calibration_c.py, gated by checks/check_calibration_c.py) by macro.central().
#
# WHAT A PICK NEEDS (attribute). Which dials a draw departs from the defaults by much (a listing, 0.15 of a dial's range in
# reverse_envelope.py) is not what causes its outcome: a dial moved a little can carry it. attribute() finds the cause by
# re-running the draw with dial subsets — only the two direction bridges moved from the defaults, those two reset in the
# draw, only the listed dials moved, and each dial reset alone — and names the dials whose reset alone loses the breach.
#
# Gated by checks/check_reverse.py.

from __future__ import annotations

from dataclasses import dataclass, fields, replace

import numpy as np

import curve as cv
import macro as m
import recognition as rc
import regimes as rg

T = np.array([0.25, 2.0, 10.0, 30.0])
LABELS = ("3M", "2Y", "10Y", "30Y")


@dataclass(frozen=True)
class Dials:
    """One point in the scenario space; each field carries (default, low, high) in RANGES."""
    eta_end: float = 0.04
    width: float = 6.0
    t_mid: float = 6.0
    alpha_capex: float = 0.25
    alpha_rent: float = 0.05
    alpha_fiscal: float = 0.10
    tp_per_debt: float = 0.02
    debt_threshold: float = 60.0
    public_support: float = 0.30
    premium_shift: float = 0.0       # pp added to the economy's own capital premium (macro.capital_premium)
    sigma: float = 1.0
    p0: float = 0.05


RANGES = {"eta_end": (0.02, 0.5), "width": (1.0, 12.0), "t_mid": (2.0, 8.0), "alpha_capex": (0.0, 1.0),
          "alpha_rent": (0.0, 0.2), "alpha_fiscal": (0.0, 0.4), "tp_per_debt": (0.0, 0.05),
          "debt_threshold": (40.0, 90.0), "public_support": (0.1, 0.6), "premium_shift": (-2.0, 2.0),
          "sigma": (0.5, 4.0), "p0": (0.01, 0.3)}
LOG = {"eta_end", "sigma", "p0"}          # scale parameters: drawn uniform in logs, so each factor of two gets equal weight
NAMES = tuple(f.name for f in fields(Dials))


def _fwd(k, v):
    return np.log(v) if k in LOG else v


def to_unit(d: Dials):
    return np.array([(_fwd(k, getattr(d, k)) - _fwd(k, RANGES[k][0])) / (_fwd(k, RANGES[k][1]) - _fwd(k, RANGES[k][0]))
                     for k in NAMES])


def from_unit(u):
    out = {}
    for k, x in zip(NAMES, u):
        lo, hi = _fwd(k, RANGES[k][0]), _fwd(k, RANGES[k][1])
        v = lo + float(x) * (hi - lo)
        out[k] = float(np.exp(v)) if k in LOG else v
    return Dials(**out)


def bridges(econ: m.Economy, d: Dials, **extra) -> m.Bridges:
    """The dials' bridges, the required return following r* from the economy's own rho shifted by d.premium_shift."""
    br = m.Bridges(alpha_capex=d.alpha_capex, alpha_rent=d.alpha_rent, alpha_fiscal=d.alpha_fiscal, tp_per_debt=d.tp_per_debt,
                   debt_threshold=d.debt_threshold, public_support=d.public_support, r0_star=0.75, **extra)
    return replace(br, capital_premium=m.capital_premium(econ, br) + d.premium_shift)


def techs(econ: m.Economy, d: Dials):
    """(status quo, new world): capability and lambda held; deep automation relative to the economy's own start."""
    return m.hold_tech(econ), m.deep_tech(econ, t_mid=d.t_mid, width=d.width, eta_end=d.eta_end)


def failure_year(econ: m.Economy, tech: m.TechPath, br: m.Bridges, years: float, dt: float = 0.25):
    """None if macro_path(econ, tech, br, years, dt) solves at every date; otherwise (the first date with no land-scarce
    equilibrium, the error). Each date depends only on the past, so a prefix of the path solves exactly when it stops
    before that date: bisection on the prefix's length (the start is tested alone, since macro_path needs two dates)."""
    n = int(round(years / dt))
    try:
        m.macro_path(econ, tech, br, n * dt, dt)
        return None
    except m.NoEquilibrium as ex:
        err = str(ex)
    rho0 = (max(br.r0_star + br.capital_premium + br.rho_shift, 0.0) / 100 if br.capital_premium is not None
            else econ.rho + br.rho_shift / 100)
    try:
        m.solve(replace(tech.at(0.0, econ), rho=rho0))
    except m.NoEquilibrium:
        return 0.0, err
    lo, hi = 0, n                                       # a prefix of lo steps solves, one of hi steps does not
    while hi - lo > 1:
        mid = (lo + hi) // 2
        try:
            m.macro_path(econ, tech, br, mid * dt, dt)
            lo = mid
        except m.NoEquilibrium:
            hi = mid
    return hi * dt, err


def first_failure(econ: m.Economy, d: Dials, years: float = 15.0, dt: float = 0.25, lookahead: float = 10.0):
    """None if both worlds of a run solve at every date; otherwise {world, year, error} for the first date with no
    land-scarce equilibrium (failure_year), the status quo checked first."""
    br = bridges(econ, d)
    for world, tech in zip(("status quo", "new world"), techs(econ, d)):
        f = failure_year(econ, tech, br, years + lookahead, dt)
        if f is not None:
            return {"world": world, "year": f[0], "error": f[1]}
    return None


def run(econ: m.Economy, d: Dials, years: float = 15.0, dt: float = 0.25, keep_paths: bool = False, lookahead: float = 10.0):
    """Both worlds under the dials, recognition, the market curve; the outcomes the envelope reports over
    `years` (and, if asked, the time paths behind them). The worlds are simulated `lookahead` years
    further, so the curve's ten-year average neutral rate never runs off the end of the path. Raises
    macro.NoEquilibrium if a date of either world has no land-scarce equilibrium (first_failure finds it)."""
    br = bridges(econ, d)
    tech_old, tech_new = techs(econ, d)
    old = m.macro_path(econ, tech_old, br, years + lookahead, dt)
    new = m.macro_path(econ, tech_new, br, years + lookahead, dt)
    p = rc.learn(old, new, rc.Learning(sigma=d.sigma, p0=d.p0))
    mixes, olds, news, pol = rc.market_curves(old, new, p)
    keep = old["t"] <= years + 1e-9
    t, p, pol = old["t"][keep], p[keep], pol[keep]
    mixes, news = mixes[:len(t)], news[:len(t)]
    new = {k: (v[keep] if isinstance(v, np.ndarray) and v.shape[:1] == keep.shape else v) for k, v in new.items()}
    z = np.array([rg.zero(T, mx) for mx in mixes])
    zn = np.array([cv.zero(T, s) for s in news])
    c10, c50, c90 = (rc.crossing(t, p, L) for L in (0.1, 0.5, 0.9))
    out = {"c10": c10, "c50": c50, "c90": c90}
    if c10 is not None and c90 is not None:
        i10, i90 = max(int(np.searchsorted(t, c10)) - 1, 0), int(np.searchsorted(t, c90))
        for k, lab in enumerate(LABELS):
            out[f"recog_{lab}"] = float((z[i90, k] - z[i10, k]) * 100)
    else:
        for lab in LABELS:
            out[f"recog_{lab}"] = 0.0
    i10y = int(np.argmin(np.abs(t - 10.0)))
    for k, lab in enumerate(LABELS):
        out[f"ten_year_{lab}"] = float((z[i10y, k] - z[0, k]) * 100)
        dev = (z[:, k] - z[0, k]) * 100
        out[f"max_up_{lab}"] = float(dev.max())
        out[f"max_down_{lab}"] = float(dev.min())
    out["max_jump_10Y"] = float(np.max(np.abs(zn[:, 2] - z[:, 2])) * 100)
    out["policy_min"], out["policy_max"] = float(pol.min()), float(pol.max())
    out["real_wage_min_rel"] = float(new["real_wage"].min() / new["real_wage"][0])
    out["debt_max"] = float(new["debt"].max())
    out["shelter_infl_max"] = float(new["pi_shelter"].max())
    out["r_star_min"], out["r_star_max"] = float(new["r_star"].min()), float(new["r_star"].max())
    out["rho_rise_max_pp"] = float(new["rho"].max() - new["rho"][0])
    if keep_paths:
        out["_paths"] = {"t": t, "p": p, "z": z, "policy": pol, "real_wage": new["real_wage"], "debt": new["debt"]}
    return out


def sample(n: int, seed: int = 20260924):
    from scipy.stats import qmc
    return qmc.LatinHypercube(d=len(NAMES), seed=seed).random(n)


def rank_corr(x, y):
    """Spearman rank correlation."""
    rx = np.argsort(np.argsort(x)).astype(float)
    ry = np.argsort(np.argsort(y)).astype(float)
    rx -= rx.mean(); ry -= ry.mean()
    return float((rx @ ry) / np.sqrt((rx @ rx) * (ry @ ry)))


def nearest_breach(U, values, threshold, default_u):
    """Among the draws whose outcome reaches the threshold (same sign), the one closest to the defaults
    in the unit cube — the most plausible way to get there, within the sample."""
    hit = values >= threshold if threshold >= 0 else values <= threshold
    if not np.any(hit):
        return None, None
    dist = np.linalg.norm(U - default_u, axis=1)
    idx = np.nonzero(hit)[0]
    j = int(idx[np.argmin(dist[idx])])
    return j, float(dist[j])


DIRECTION = ("alpha_rent", "alpha_fiscal")     # the two neutral-rate bridges that decide the curve's direction (owners' saving, deficits)


def attribute(econ: m.Economy, d: Dials, key: str, threshold: float, listed=()):
    """What a draw's breach of `threshold` in outcome `key` needs, found by re-running it with dial subsets (not by which
    dials moved far): the outcome at the draw; with only the direction bridges moved from the defaults (every other dial at
    its default); with the direction bridges reset to their defaults in the draw; with only the `listed` dials moved; and
    with each dial reset alone. `needed`: the dials whose reset alone loses the breach. Outcomes in bp, rounded to 0.1."""
    d0 = Dials()
    hit = (lambda v: v >= threshold) if threshold >= 0 else (lambda v: v <= threshold)
    val = lambda dd: round(float(run(econ, dd)[key]), 1)  # noqa: E731
    only = lambda ks: replace(d0, **{k: getattr(d, k) for k in ks})  # noqa: E731
    reset = lambda ks: replace(d, **{k: getattr(d0, k) for k in ks})  # noqa: E731
    each = {k: val(reset([k])) for k in NAMES}
    return {"outcome": key, "threshold": threshold, "at_draw": val(d),
            "direction_bridges": {k: [getattr(d0, k), round(getattr(d, k), 4)] for k in DIRECTION},
            "direction_bridges_only": val(only(DIRECTION)), "direction_bridges_reset": val(reset(DIRECTION)),
            "listed_dials_only": val(only(listed)) if listed else None, "each_dial_reset": each,
            "needed": [k for k in NAMES if not hit(each[k])]}
