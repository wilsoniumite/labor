# two_goods.py — durables apart (her go, 2026-11-06): the pinning model with two final goods, durables and everything
# else (the rest of consumption but shelter), made by one kind of machine.
#
# THE ECONOMY. As ../pinning/code/pinning_model.py, with the final good split in two. Each good s has its own continuum of
# tasks and its own capability clock: a machine does task x of good s with gamma_s(x) = eta_s (g0 + g1 x^k) service
# units; the schedules' shape (g0, g1, k) is common. There is one machine (Vm = a p_m + lambda v + b, p_m = (rho +
# delta) Vm), one wage and one land market. At the common margin m = v / p_m each good automates its tasks below x_s,
# where gamma_s(x_s) = m (x_s = 0 below the schedule, 1 above it). Prices: p_s = v (1 - x_s) + p_m J_s(x_s).
# The basket holds a composite of the two goods and site, at constant utility: the composite is CES with elasticity
# sigma_dg and durables' spending share omega_d at the reference prices (the model's own 1950 prices), its unit cost
# normalised to the other goods' 1950 price; the outer basket is pinning_model.BasketEconomy's, read at the composite's
# price. Land: T = B (s + g b delta J_mix / (1 - a delta)), J_mix = d_d J_d + d_g J_g per unit of composite. Labour:
# n_D = B g (d_d (1 - x_d) + d_g (1 - x_g)) + lambda delta K. One equation in m: n_D = n_S, on (0, the machine chain's
# ceiling), the ceiling being the margin where (rho + delta)(a + lambda m) = 1.
# In 1950 the composite is read at its reference point (reference mode: unit cost = the other goods' price, demands
# omega_d c / p_d and 1 - omega_d), which is what fixes the reference prices; every CES composite agrees there.
# With eta_d = eta_g the two goods are one, and every number is the one-good model's (checks/check_two_goods.py).

import numpy as np
from scipy.optimize import brentq

import pinning_model as pm


def x_of(m, eta, e):
    """The last task a machine takes at margin m under clock eta: gamma(x) = m, held to [0, 1]."""
    r = (m / eta - e.g0) / e.g1
    if r <= 0.0:
        return 0.0
    if r >= 1.0:
        return 1.0
    return float(r ** (1.0 / e.k))


def J_of(x, eta, e):
    return eta * (e.g0 * x + e.g1 * x ** (e.k + 1.0) / (e.k + 1.0))


def composite(pd, pg, cmp):
    """The composite's unit cost and its demands per unit (durables, other goods). cmp: dict(omega_d, and either
    mode="ref", or sigma_dg with the reference prices pref_d, pref_g)."""
    w = cmp["omega_d"]
    if cmp.get("mode") == "ref":                       # the reference point: unit cost the other goods' price
        c = pg
        return c, w * c / pd, (1.0 - w) * c / pg
    s, rd, rg = cmp["sigma_dg"], cmp["pref_d"], cmp["pref_g"]
    if abs(s - 1.0) < 1e-12:                            # Cobb-Douglas
        c = rg * (pd / rd) ** w * (pg / rg) ** (1.0 - w)
        return c, w * c / pd, (1.0 - w) * c / pg
    ad, ag = w * (rg / rd) ** (1.0 - s), (1.0 - w)       # shares omega at the reference, unit cost pref_g there
    c = (ad * pd ** (1.0 - s) + ag * pg ** (1.0 - s)) ** (1.0 / (1.0 - s))
    return c, ad * (pd / c) ** (-s), ag * (pg / c) ** (-s)


def parts(e, m, eta_d, cmp):
    """Every price and quantity at margin m (e: a pinning_model economy whose eta is the other goods' clock)."""
    cpt = e.rho + e.delta
    den = 1.0 - cpt * (e.a + e.lam * m)
    Vm = e.b / den
    pm_ = cpt * Vm
    v = m * pm_
    xg, xd = x_of(m, e.eta, e), x_of(m, eta_d, e)
    Jg, Jd = J_of(xg, e.eta, e), J_of(xd, eta_d, e)
    pg, pd = v * (1.0 - xg) + pm_ * Jg, v * (1.0 - xd) + pm_ * Jd
    c, dd, dg = composite(pd, pg, cmp)
    gb, sb = e.basket(c)                                # the outer basket, read at the composite's price
    Ps = c * gb + sb
    Jmix = dd * Jd + dg * Jg
    B = e.T / (sb + gb * e.b * e.delta * Jmix / (1.0 - e.a * e.delta))
    K = B * gb * Jmix / (1.0 - e.a * e.delta)
    final = B * gb * (dd * (1.0 - xd) + dg * (1.0 - xg))
    mh = e.lam * e.delta * K
    z = np.log1p(v / Ps)
    nS = e.N * min(max(z / e.chi_max, 0.0), getattr(e, "cap", 1.0))
    return dict(m=m, xg=xg, xd=xd, Jg=Jg, Jd=Jd, v=v, pm=pm_, Vm=Vm, pg=pg, pd=pd, c=c, dd=dd, dg=dg, gb=gb, sb=sb, Ps=Ps,
                B=B, K=K, final=final, mh=mh, nD=final + mh, nS=nS)


def m_ceiling(e):
    """The margin at the machine chain's ceiling: (rho + delta)(a + lambda m) = 1 (inf if lambda is zero)."""
    cpt = e.rho + e.delta
    if cpt * e.a >= 1.0:
        raise pm.NoEquilibrium("machine-service cost undefined even with no labour in the chain")
    return np.inf if e.lam <= 0 else (1.0 / cpt - e.a) / e.lam


def solve(e, eta_d, cmp):
    """The interior equilibrium n_D(m) = n_S(m) on (0, the ceiling); NoEquilibrium where there is none."""
    mbar = m_ceiling(e)
    top = max(e.eta, eta_d) * (e.g0 + e.g1)              # every task of both goods automated above this
    hi = min(mbar * (1.0 - 1e-13), top) if np.isfinite(mbar) else top
    lo = 1e-12 * hi
    f = lambda m: (lambda q: q["nD"] - q["nS"])(parts(e, m, eta_d, cmp))  # noqa: E731
    flo, fhi = f(lo), f(hi)
    if not (flo > 0 and fhi < 0):
        raise pm.NoEquilibrium(f"no interior equilibrium: nD - nS = {flo:.4g} at the bottom, {fhi:.4g} at the top")
    m = brentq(f, lo, hi, xtol=1e-15 * hi, rtol=1e-15)
    q = parts(e, m, eta_d, cmp)
    n = q["nD"]
    interest = e.rho * q["Vm"] * q["K"]
    income = q["v"] * n + e.T + interest
    q.update(n=n, participation=n / e.N, income=income, labour_share_bea=q["v"] * q["final"] / income,
             theta_V=e.lam * q["v"] / q["Vm"], kappa_V=e.a * q["pm"] / q["Vm"], sigma_V=e.b / q["Vm"],
             chain_share=q["mh"] / n, inv_income=e.delta * q["Vm"] * q["K"] / income, m_ceiling=mbar,
             xg_ceiling=x_of(mbar, e.eta, e) if np.isfinite(mbar) else 1.0,
             xd_ceiling=x_of(mbar, eta_d, e) if np.isfinite(mbar) else 1.0,
             dur_share=q["pd"] * q["dd"] / q["c"])        # durables' share of the composite's cost
    return q
