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
# A lead (2026-11-06, while she flew): a value-share rent phi in a machine's cost (cmp["phi"], 0 by default), beside its
# land: imported content and IP rents priced with the machine, as BEA's cost split shows them (imported content 18-21%
# of the machine bundle, 1997-2023). Vm = (a p_m + lambda v + b) / (1 - phi); the rent on each machine built, phi Vm
# delta K a year, is the owners' income. Land's share of a machine's cost is still b / Vm.
# The skill split (her idea and go, 2026-11-08): services in two goods, low-skill and high-skill, each with its own clock
# (eta_s a pair), nested with nondurables Cobb-Douglas at the record's shares (rest_skill). A worker for each good (her
# go, the same day): each good's tasks are done at its own pay, r_s times the production wage v (cmp["r_d"], "r_n",
# "r_s", "r_l", "r_h"; 1 by default, one wage). A task of good s goes to a machine when gamma_s(x) <= r_s m, so dearer
# workers lose more tasks; p_s = r_s v (1 - x_s) + p_m J_s. Machines are built at v, people choose to work at v, and the
# hours of every good clear one labour market (the pay gaps are set, as compensating differences); final labour's pay is
# v * final_w, which buys the baskets with the land rent, interest and the rent on machines (income = consumption). With
# every r_s = 1 each number is the one-wage economy's, bit for bit.

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


def rest(pn, ps, cmp):
    """Services apart (her go, 2026-11-08): the other goods as nondurables and services, Cobb-Douglas with services'
    spending share omega_s set each year from the record (a constant-taste CES cannot follow the record: services' share
    rose fourfold against nondurables' while their relative price only doubled), the unit cost normalised to nondurables'
    price at the reference prices (1950's). Returns the nest's unit cost and its demands per unit (nondurables, services).
    In 1950 (mode "ref") the nest is read at its reference point: unit cost = nondurables' price."""
    w = cmp["omega_s"]
    if cmp.get("mode") == "ref":
        c = pn
    else:
        rn, rs = cmp["pref_n"], cmp["pref_s"]
        c = rn * (pn / rn) ** (1.0 - w) * (ps / rs) ** w
    return c, (1.0 - w) * c / pn, w * c / ps


def rest_skill(pn, pl, ph, cmp):
    """The skill split (her idea, 2026-11-08): the other goods as nondurables (with the goods-like services), low-skill
    and high-skill services, Cobb-Douglas with the services groups' shares omega_l, omega_h set each year from the record
    (nondurables the rest), the unit cost normalised to nondurables' price at the reference prices (1950's). Returns the
    unit cost and the demands per unit (nondurables, low, high). In 1950 (mode "ref") the unit cost is nondurables' price."""
    wl, wh = cmp["omega_l"], cmp["omega_h"]
    wn = 1.0 - wl - wh
    if cmp.get("mode") == "ref":
        c = pn
    else:
        rn, rl, rh = cmp["pref_n"], cmp["pref_l"], cmp["pref_h"]
        c = rn * (pn / rn) ** wn * (pl / rl) ** wl * (ph / rh) ** wh
    return c, wn * c / pn, wl * c / pl, wh * c / ph


def parts(e, m, eta_d, cmp, eta_s=None):
    """Every price and quantity at margin m (e: a pinning_model economy whose eta is the other goods' clock; with eta_s,
    services' clock, the other goods are nondurables (on e's clock) and services, nested as rest() says; with eta_s a pair
    (low, high), the skill split, nested as rest_skill() says). Each good's pay over the production wage from cmp (r_d,
    r_n, r_s, r_l, r_h; 1 by default)."""
    cpt = e.rho + e.delta
    phi = cmp.get("phi", 0.0)
    den = 1.0 - phi - cpt * (e.a + e.lam * m)
    Vm = e.b / den
    pm_ = cpt * Vm
    v = m * pm_
    rd, rg = cmp.get("r_d", 1.0), cmp.get("r_n", 1.0)  # each good's pay over the production wage (1: one wage)
    xg, xd = x_of(rg * m, e.eta, e), x_of(rd * m, eta_d, e)
    Jg, Jd = J_of(xg, e.eta, e), J_of(xd, eta_d, e)
    pg, pd = rg * v * (1.0 - xg) + pm_ * Jg, rd * v * (1.0 - xd) + pm_ * Jd
    if eta_s is None:                                   # two goods: the other goods are one good
        prest, Jrest, Lrest, Wrest, extra = pg, Jg, 1.0 - xg, rg * (1.0 - xg), {}
    elif np.ndim(eta_s) == 0:                           # three goods: the other goods are nondurables and services
        rs = cmp.get("r_s", 1.0)
        xs = x_of(rs * m, eta_s, e)
        Js = J_of(xs, eta_s, e)
        ps = rs * v * (1.0 - xs) + pm_ * Js
        prest, dn, ds = rest(pg, ps, cmp)
        Jrest, Lrest = dn * Jg + ds * Js, dn * (1.0 - xg) + ds * (1.0 - xs)
        Wrest = dn * rg * (1.0 - xg) + ds * rs * (1.0 - xs)
        extra = dict(xs=xs, Js=Js, ps=ps, dn=dn, ds=ds, prest=prest)
    else:                                               # four goods: nondurables, low- and high-skill services
        eta_l, eta_h = eta_s
        rl, rh = cmp.get("r_l", 1.0), cmp.get("r_h", 1.0)
        xl, xh = x_of(rl * m, eta_l, e), x_of(rh * m, eta_h, e)
        Jl, Jh = J_of(xl, eta_l, e), J_of(xh, eta_h, e)
        pl, ph = rl * v * (1.0 - xl) + pm_ * Jl, rh * v * (1.0 - xh) + pm_ * Jh
        prest, dn, dl, dh = rest_skill(pg, pl, ph, cmp)
        Jrest = dn * Jg + dl * Jl + dh * Jh
        Lrest = dn * (1.0 - xg) + dl * (1.0 - xl) + dh * (1.0 - xh)
        Wrest = dn * rg * (1.0 - xg) + dl * rl * (1.0 - xl) + dh * rh * (1.0 - xh)
        extra = dict(xl=xl, xh=xh, Jl=Jl, Jh=Jh, pl=pl, ph=ph, dn=dn, dl=dl, dh=dh, prest=prest)
    c, dd, dg = composite(pd, prest, cmp)
    gb, sb = e.basket(c)                                # the outer basket, read at the composite's price
    Ps = c * gb + sb
    Jmix = dd * Jd + dg * Jrest
    B = e.T / (sb + gb * e.b * e.delta * Jmix / (1.0 - e.a * e.delta))
    K = B * gb * Jmix / (1.0 - e.a * e.delta)
    final = B * gb * (dd * (1.0 - xd) + dg * Lrest)
    final_w = B * gb * (dd * rd * (1.0 - xd) + dg * Wrest)   # final labour's pay, in production wages (final at one wage)
    mh = e.lam * e.delta * K
    z = np.log1p(v / Ps)
    nS = e.N * min(max(z / e.chi_max, 0.0), getattr(e, "cap", 1.0))
    return dict(m=m, xg=xg, xd=xd, Jg=Jg, Jd=Jd, v=v, pm=pm_, Vm=Vm, pg=pg, pd=pd, c=c, dd=dd, dg=dg, gb=gb, sb=sb, Ps=Ps,
                B=B, K=K, final=final, final_w=final_w, mh=mh, nD=final + mh, nS=nS, rd=rd, rg=rg, **extra)


def m_ceiling(e, phi=0.0):
    """The margin at the machine chain's ceiling: phi + (rho + delta)(a + lambda m) = 1 (inf if lambda is zero)."""
    cpt = e.rho + e.delta
    if phi + cpt * e.a >= 1.0:
        raise pm.NoEquilibrium("machine-service cost undefined even with no labour in the chain")
    return np.inf if e.lam <= 0 else ((1.0 - phi) / cpt - e.a) / e.lam


def solve(e, eta_d, cmp, eta_s=None):
    """The interior equilibrium n_D(m) = n_S(m) on (0, the ceiling); NoEquilibrium where there is none. With eta_s,
    services apart, or with a pair the skill split (parts)."""
    phi = cmp.get("phi", 0.0)
    mbar = m_ceiling(e, phi)
    rd, rg = cmp.get("r_d", 1.0), cmp.get("r_n", 1.0)
    top = max(e.eta / rg, eta_d / rd) * (e.g0 + e.g1)    # every task of both goods automated above this
    if eta_s is not None and np.ndim(eta_s) == 0:
        top = max(top, eta_s / cmp.get("r_s", 1.0) * (e.g0 + e.g1))
    elif eta_s is not None:
        top = max(top, eta_s[0] / cmp.get("r_l", 1.0) * (e.g0 + e.g1), eta_s[1] / cmp.get("r_h", 1.0) * (e.g0 + e.g1))
    hi = min(mbar * (1.0 - 1e-13), top) if np.isfinite(mbar) else top
    lo = 1e-12 * hi
    f = lambda m: (lambda q: q["nD"] - q["nS"])(parts(e, m, eta_d, cmp, eta_s))  # noqa: E731
    flo, fhi = f(lo), f(hi)
    if not (flo > 0 and fhi < 0):
        raise pm.NoEquilibrium(f"no interior equilibrium: nD - nS = {flo:.4g} at the bottom, {fhi:.4g} at the top")
    m = brentq(f, lo, hi, xtol=1e-15 * hi, rtol=1e-15)
    q = parts(e, m, eta_d, cmp, eta_s)
    n = q["nD"]
    interest = e.rho * q["Vm"] * q["K"]
    rent = phi * q["Vm"] * e.delta * q["K"]               # the value-share rent on each machine built (0 by default)
    income = q["v"] * (q["final_w"] + q["mh"]) + e.T + interest + rent   # each good's workers at their own pay
    q.update(n=n, participation=n / e.N, income=income, labour_share_bea=q["v"] * q["final_w"] / income,
             theta_V=e.lam * q["v"] / q["Vm"], kappa_V=e.a * q["pm"] / q["Vm"], sigma_V=e.b / q["Vm"], phi=phi,
             fixed_rents=phi + e.b / q["Vm"], rent_income=rent / income,
             chain_share=q["mh"] / n, inv_income=e.delta * q["Vm"] * q["K"] / income, m_ceiling=mbar,
             xg_ceiling=x_of(rg * mbar, e.eta, e) if np.isfinite(mbar) else 1.0,
             xd_ceiling=x_of(rd * mbar, eta_d, e) if np.isfinite(mbar) else 1.0,
             dur_share=q["pd"] * q["dd"] / q["c"])        # durables' share of the composite's cost
    if eta_s is not None and np.ndim(eta_s) == 0:         # services apart: their task line and spending share
        q.update(xs_ceiling=x_of(cmp.get("r_s", 1.0) * mbar, eta_s, e) if np.isfinite(mbar) else 1.0,
                 srv_share=q["ps"] * q["ds"] * q["dg"] / q["c"], nd_share=q["pg"] * q["dn"] * q["dg"] / q["c"])
    elif eta_s is not None:                               # the skill split: both services groups' task lines and shares
        rl, rh = cmp.get("r_l", 1.0), cmp.get("r_h", 1.0)
        q.update(xl_ceiling=x_of(rl * mbar, eta_s[0], e) if np.isfinite(mbar) else 1.0,
                 xh_ceiling=x_of(rh * mbar, eta_s[1], e) if np.isfinite(mbar) else 1.0,
                 low_share=q["pl"] * q["dl"] * q["dg"] / q["c"], high_share=q["ph"] * q["dh"] * q["dg"] / q["c"],
                 nd_share=q["pg"] * q["dn"] * q["dg"] / q["c"], rl=rl, rh=rh)
    return q
