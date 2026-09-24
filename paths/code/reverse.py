# reverse.py — reverse stress testing, part 1: the envelope of outcomes across the model's dials.
#
# The openness principle keeps structure fixed and makes behaviour swappable; the behaviour lives in
# named coefficients. This file turns them — with the technology path and the market's learning — over
# broad stated ranges (not estimates), runs the two-world recognition model for each draw, and asks:
# how large can the curve's moves get, which dials drive them, and what is the smallest departure from
# the defaults that produces a given move? Part 2 — a bank's exposure profile applied to these paths —
# belongs where the bank's numbers are, not in this public repository.

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
    capital_premium: float = 5.0
    sigma: float = 1.0
    p0: float = 0.05


RANGES = {"eta_end": (0.02, 0.5), "width": (1.0, 12.0), "t_mid": (2.0, 8.0), "alpha_capex": (0.0, 1.0),
          "alpha_rent": (0.0, 0.2), "alpha_fiscal": (0.0, 0.4), "tp_per_debt": (0.0, 0.05),
          "debt_threshold": (40.0, 90.0), "public_support": (0.1, 0.6), "capital_premium": (3.0, 7.0),
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


def run(econ: m.Economy, d: Dials, years: float = 15.0, dt: float = 0.25, keep_paths: bool = False, lookahead: float = 10.0):
    """Both worlds under the dials, recognition, the market curve; the outcomes the envelope reports over
    `years` (and, if asked, the time paths behind them). The worlds are simulated `lookahead` years
    further, so the curve's ten-year average neutral rate never runs off the end of the path."""
    br = m.Bridges(capital_premium=d.capital_premium, alpha_capex=d.alpha_capex, alpha_rent=d.alpha_rent,
                   alpha_fiscal=d.alpha_fiscal, tp_per_debt=d.tp_per_debt, debt_threshold=d.debt_threshold,
                   public_support=d.public_support, r0_star=0.75)
    old = m.macro_path(econ, m.TechPath(eta_end=1.0, lam_end=econ.lam), br, years + lookahead, dt)
    new = m.macro_path(econ, m.TechPath(eta_end=d.eta_end, lam_end=0.01, t_mid=d.t_mid, width=d.width), br, years + lookahead, dt)
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
