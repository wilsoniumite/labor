# pinning_model.py — the pinning model: the economy of the paper's Appendix B, solved, and calibrated from shares.
# One implementation. The paper's instance and Figure 3 (code/appendix_b.py) solve with it, and so does the complex model
# in ../paths/ (paths/code/macro.py runs this economy along a technology path and re-exports every name below).
#
# THE ECONOMY. N potential workers; a provider owns T units of land and the machines, gives each person one basket in
# work and in exit, and spends the rest in the basket's proportions. A basket is one unit of the final good and h units
# of space. Rent r = 1 (the numeraire), v = w/r. The final good needs one unit of each task on [0, 1]; a machine does
# task x with gamma(x) = eta (g0 + g1 x^k) service units, gamma increasing, J(x) its integral over [0, x]. A machine
# costs Vm = a p_m + lambda v + b to build (machine services, hours, land), supplies one service unit a year and
# depreciates at delta; its owner requires the return rho, so a service unit rents at p_m = (rho + delta) Vm
# (Appendix A.4; (rho, delta) = (0, 1) is the flow benchmark). At an interior threshold x (machines below, people above),
# with the task condition v = gamma(x) p_m:
#     Vm = b / (1 - (rho + delta)(a + lambda gamma)),  p(x) = v (1 - x) + p_m J,  P_s = p + h,
#     Y = T / (h + b delta J / (1 - a delta)),  K = Y J / (1 - a delta),  n_D = Y (1 - x) + lambda delta K,
#     n_S = N F(log(1 + v / P_s)),  F uniform on [0, chi_max] (CappedEconomy: at most a share cap).
# Equilibrium: n_D(x*) = n_S(x*). Income = v n + T + rho Vm K (wages, land rent, interest).
#
# THE CEILING. Tasks where (rho + delta)(a + lambda gamma(x)) >= 1 are closed to machines at every wage: the machine
# services that would replace an hour embody more than the hour (Appendix A.1 lets tasks be closed to machines by
# capability, preference or law; A.4: "each expression requires a positive denominator"). The equilibrium is sought on
# (0, x_ceiling), which is (0, 1) exactly whenever x_ceiling = 1. Beyond a rate headroom (rate_headroom) the ceiling
# falls below the tasks the labour force can staff and there is no land-scarce equilibrium: solve raises
# NoEquilibrium. Per unit of build cost Vm: theta_V = lambda v / Vm (labour), kappa_V = a p_m / Vm (machine services),
# sigma_V = b / Vm (fixed rents); they sum to 1; multiplier = 1 + theta_V / sigma_V = d ln v / d ln gamma at a fixed
# return; labour_share_bea = v final_hours / income (the paper's Figure 7 object); chain_share = machine hours / n.
#
# THE CALIBRATION. calibrate_c solves seven shares (ChainTargets) in closed form and returns every root in the
# schedule's convexity k: the targets pin x*, and one equation in k (_chain_ratio) has two roots, between which the data
# cannot choose. The low root is the main reading everywhere (the paper's instance, k 4.36; calibration (c), k 5.66).
#
# Run from pinning/:  python3 code/pinning_model.py    (the paper's instance from its shares, both roots)

from __future__ import annotations

from dataclasses import dataclass, replace

import numpy as np
from scipy.optimize import brentq


@dataclass(frozen=True)
class Economy:
    N: float = 4.0
    T: float = 10.0
    h: float = 1.0
    a: float = 0.3
    b: float = 0.4
    lam: float = 0.05
    g0: float = 0.2          # gamma(x) = eta * (g0 + g1 x^k); k = 1 is the paper's schedule, k > 1 the
    g1: float = 0.8          # convex schedules of its eras figure (human advantage concentrated near the wall)
    k: float = 1.0
    eta: float = 1.0
    chi_max: float = 1.0     # work cost chi ~ U[0, chi_max]
    rho: float = 0.0         # required return on machine capital (a year) — Appendix A.4's interest
    delta: float = 1.0       # depreciation (a year). (rho, delta) = (0, 1) is Appendix B's flow benchmark exactly

    def gamma(self, x):
        return self.eta * (self.g0 + self.g1 * x ** self.k)

    def J(self, x):
        return self.eta * (self.g0 * x + self.g1 * x ** (self.k + 1.0) / (self.k + 1.0))


@dataclass(frozen=True)
class CappedEconomy(Economy):
    """The economy with participation capped: a share 1 - cap of people never works at any wage, and below the cap
    participation follows the wage as in Economy (the backward model's cap, her idea of 2026-11-05:
    ../../us-record/STATE.md). A subclass, so Economy's fields, and every stored parameter set, stay the paper's."""
    cap: float = 1.0


def _parts(e: Economy, x):
    """Prices and quantities at threshold x. Machines are a stock K, one service unit a year each; a new
    machine costs Vm = a p_m + lambda v + b (machine services, hours, land), so the user cost is
    p_m = (rho + delta) Vm (Appendix A.4) and, at the margin v = p_m gamma(x*),
        Vm = b / (1 - (rho + delta)(a + lambda gamma)),   p_m = (rho + delta) Vm.
    Replacement of delta K a year uses a delta K services, lambda delta K hours and b delta K land:
        K = Y J / (1 - a delta),  Y = T / (h + b delta J / (1 - a delta)),  n = Y (1 - x) + lambda delta K.
    Income: I = v n + T + rho Vm K (wages, land rent, interest). At (0, 1) all of this is Appendix B."""
    g, J = e.gamma(x), e.J(x)
    cpt = e.rho + e.delta
    den = 1.0 - cpt * (e.a + e.lam * g)
    Vm = e.b / den
    pm = cpt * Vm
    v = g * pm
    p = v * (1.0 - x) + pm * J
    Ps = p + e.h
    Y = e.T / (e.h + e.b * e.delta * J / (1.0 - e.a * e.delta))
    K = Y * J / (1.0 - e.a * e.delta)
    final_hours = Y * (1.0 - x)
    machine_hours = e.lam * e.delta * K
    nD = final_hours + machine_hours
    z = np.log1p(v / Ps)
    nS = e.N * min(max(z / e.chi_max, 0.0), getattr(e, "cap", 1.0))      # 1: everyone can work (CappedEconomy: less)
    return dict(x=x, gamma=g, J=J, v=v, pm=pm, Vm=Vm, p=p, Ps=Ps, Y=Y, X=K, K=K, final_hours=final_hours,
                machine_hours=machine_hours, nD=nD, nS=nS)


class NoEquilibrium(ValueError):
    """No interior land-scarce equilibrium on (0, x_ceiling)."""


def x_ceiling(e: Economy):
    """The last task machines can take at any wage: where (rho + delta)(a + lambda gamma(x)) = 1 the machine
    services that replace an hour embody (with interest, traced through the machines that build machines) the
    whole hour, and the machine-service cost is unbounded in rent units. Tasks beyond it are closed to machines by
    capability (A.1). 1.0 when the cost stays finite on the whole task list — Appendix B's standing assumption,
    which holds for the paper's instance and calibrations (a) and (b). On the knife edge g(1) = 0 exactly the cost is
    unbounded only at x = 1 itself; the ceiling returned is then the interior point where the cost's denominator is 1e-9
    of its value at x = 0, so solve never divides by zero there (it solves below it or raises NoEquilibrium)."""
    cpt = e.rho + e.delta
    g = lambda x: 1.0 - cpt * (e.a + e.lam * e.gamma(x))  # noqa: E731
    g1 = g(1.0)
    if g1 > 0:
        return 1.0
    g0 = g(0.0)
    if g0 <= 0:
        raise NoEquilibrium("machine-service cost undefined even at x = 0")
    if g1 == 0:
        return brentq(lambda x: g(x) - 1e-9 * g0, 0.0, 1.0, xtol=1e-15)
    return brentq(g, 0.0, 1.0, xtol=1e-15)


def solve(e: Economy):
    """The interior equilibrium n_D(x*) = n_S(x*) on the tasks machines can take, (0, x_ceiling). Raises
    NoEquilibrium (a ValueError) if Lemma B.1's conditions fail there. [(c): the search stops at the machine
    chain's ceiling instead of asserting Appendix B's assumption at x = 1; identical whenever x_ceiling = 1.]"""
    xb = x_ceiling(e)
    f = lambda x: _parts(e, x)["nD"] - _parts(e, x)["nS"]  # noqa: E731
    lo, hi = 1e-12, (1.0 if xb >= 1.0 else xb * (1.0 - 1e-13))
    if hi < 1.0:          # where the cost is very flat at the ceiling, step back until its denominator is positive in floating point
        den = lambda x: 1.0 - (e.rho + e.delta) * (e.a + e.lam * e.gamma(x))  # noqa: E731
        j = 0
        while den(hi) <= 0.0:
            j += 1
            if j > 40:
                raise NoEquilibrium(f"machine-service cost not finite below the machine chain's ceiling x = {xb:.5f}")
            hi = xb * (1.0 - 1e-13 * 2.0 ** j)
    if f(lo) <= 0 or f(hi) >= 0:
        raise NoEquilibrium(f"no interior equilibrium: nD - nS = {f(lo):.4g} at 0, {f(hi):.4g} at "
                            + ("1" if hi == 1.0 else f"the machine chain's ceiling x = {xb:.5f}"))
    x = brentq(f, lo, hi, xtol=1e-15)
    q = _parts(e, x)
    n = q["nD"]
    interest = e.rho * q["Vm"] * q["K"]
    income = q["v"] * n + e.T + interest
    q.update(n=n, participation=n / e.N, income=income, labor_share=q["v"] * n / income,
             capital_share=interest / income, capital_output=q["Vm"] * q["K"] / income,
             real_wage=q["v"] / q["Ps"], goods_to_space=q["p"] / 1.0,
             support_cost=e.N * q["Ps"], funded=e.T + interest > e.N * q["Ps"])
    # (c) additions — the machine chain on BEA's basis (per unit of build cost Vm); every key above is unchanged
    Vm = q["Vm"]
    theta_V = e.lam * q["v"] / Vm if Vm > 0 else float("nan")
    sigma_V = e.b / Vm if Vm > 0 else float("nan")
    q.update(x_ceiling=xb, theta_V=theta_V, kappa_V=e.a * q["pm"] / Vm if Vm > 0 else float("nan"), sigma_V=sigma_V,
             multiplier=1.0 + theta_V / sigma_V if sigma_V > 0 else float("inf"),
             chain_share=q["machine_hours"] / n, labour_share_bea=q["v"] * q["final_hours"] / income,
             inv_income=e.delta * Vm * q["K"] / income)
    return q


# ------------------------------------------------------------------ calibration from shares
@dataclass(frozen=True)
class ChainTargets:
    """The seven targets calibrate_c solves in closed form: labour's share of consumption, participation, baskets a
    person and the site's share of the basket, and the machine chain: labour's and fixed rents' shares of a machine's
    build cost and the chain's share of hours; with a depreciation rate. The defaults are calibration (c) of ../paths/
    (the machine chain as BEA's accounts measure it, ../paths/code/chains.py); the paper's instance sets the same seven
    from U.S.-like shares (appendix_b.SHARES: the site 0.06 of the basket). b stays the land unit ((b, h, T) scale together and leave
    every real quantity unchanged); the return rho is an outcome (the adding-up pins rho/delta).
    IMPORT BASIS (calibration (c)). labour, theta_V, chain_share and sigma_V must be read on one import basis
    (../paths/code/calibration_c.py records a tag for each and ../paths/checks/check_calibration_c.py gates it). Central, 'domp' (US labour only; imported
    content outside the labour share, as a fixed-quantity cost — in the model it is part of the chain's land b, paid as
    domestic rent and drawn from T, not an elastic import at a world price): labour 0.47 is BEA WP2026-01's human-effort share
    of PCE (foreign content in its own bucket), theta_V 0.470 and chain_share 0.151 the equipment + IPP + private
    structures bundle on chains.py's domp basis, sigma_V its imported content plus its domestic fixed rent. 'tot'
    (imports priced at US cost shares): theta_V 0.569, chain_share 0.183, labour 0.47 grossed up for PCE's foreign
    content (0.519). Pairing 0.47 with the tot theta_V and chain_share mixes the two (the 'mixed basis' variant)."""
    theta_V: float                 # lambda v / Vm: full-chain compensation share of a machine's build cost
    chain_share: float             # lambda delta K / n: the machine chain's share of all labour (compensation: one wage)
    sigma_V: float                 # b / Vm: fixed-quantity rents' share of build cost (open basis: incl. imported content)
    delta: float                   # depreciation a year (BEA Fixed Assets)
    labour: float = 0.47           # her labour share, read on `basis` (and on the import basis of theta_V; see above)
    basis: str = "bea"             # "bea": v (1 - x) / Ps, the consumption chain with capital services in surplus (the
                                   # paper's Figure 7 object under A.4); "traced": v n / income (solve's labor_share)
    participation: float = 0.60
    baskets_per_person: float = 3.0
    site: float = 0.13             # read on `site_basis`
    site_basis: str = "basket"     # "basket": h / Ps (her target); "gdp": h Y / (income + delta Vm K), the measured flow
    b: float = 0.4
    g0: float = 0.01               # gamma(0)/gamma(1) at eta = 1; her 0.02 has no root on the BEA basis at measured values
    N: float = 1.0


def _chain_ratio(x, k, g0, g1):
    """J(x) / (gamma(x)(1 - x)) at eta = 1: capital services over direct labour in the consumption chain. It tends to
    x/(1 - x) as k -> 0 and as k -> infinity and dips between (J <= x gamma), so a target below x/(1 - x) and above
    the dip has exactly two roots in k (../paths/checks/check_calibration_c.py M3)."""
    return (g0 * x + g1 * x ** (k + 1.0) / (k + 1.0)) / ((g0 + g1 * x ** k) * (1.0 - x))


def calibrate_c(tg: ChainTargets):
    """(c) in closed form: steady-state identities pin, in turn, investment over consumption (from the chain share
    and theta_V), capital services' share of consumption (labour and site), delta/(rho + delta) (the adding-up),
    the threshold x* (participation, output, chain share), the schedule's convexity k (capital services over
    labour at x*), lambda and a (theta_V, sigma_V) and the scale (h, T, chi_max). Returns [(Economy, info)] for
    every root in k, sorted by k (the low root is (a)/(b)'s branch); raises ValueError when a step has no solution."""
    s = tg.chain_share
    LB = tg.labour if tg.basis == "bea" else tg.labour * (1.0 - s)          # labour in the consumption chain / C
    iC = s * LB / (tg.theta_V * (1.0 - s))                                   # replacement investment / C
    site_C = tg.site if tg.site_basis == "basket" else tg.site * (1.0 + iC)
    cs = 1.0 - LB - site_C                                                   # capital services / C
    if cs <= 0:
        raise ValueError(f"labour {LB:.4f} + site {site_C:.4f} leave no capital services")
    u = iC / (cs + (1.0 - tg.theta_V - tg.sigma_V) * iC)                     # delta / (rho + delta)
    if u >= 1:
        raise ValueError(f"the adding-up needs a non-positive return (delta/(rho + delta) = {u:.4f})")
    rho = tg.delta * (1.0 / u - 1.0)
    x = 1.0 - tg.participation * (1.0 - s) / tg.baskets_per_person
    ratio = cs / LB
    g0, g1 = tg.g0, 1.0 - tg.g0
    ks = np.exp(np.linspace(np.log(0.05), np.log(400.0), 40001))
    r = _chain_ratio(x, ks, g0, g1) - ratio
    info = dict(LB=LB, iC=iC, site_C=site_C, cs=cs, u=u, rho=rho, x=x, ratio=ratio,
                ratio_min=float(np.min(_chain_ratio(x, ks, g0, g1))), ratio_limit=x / (1.0 - x))
    roots = [brentq(lambda k: _chain_ratio(x, k, g0, g1) - ratio, ks[i], ks[i + 1], xtol=1e-14)
             for i in range(len(ks) - 1) if r[i] * r[i + 1] < 0]
    if not roots:
        raise ValueError(f"no schedule convexity k fits: cs/LB {ratio:.4f} at x* {x:.4f} lies outside the schedule's "
                         f"range [{info['ratio_min']:.4f}, {info['ratio_limit']:.4f}) at g0 {g0}")
    cpt = rho + tg.delta
    out = []
    for k in roots:
        gam = g0 + g1 * x ** k
        J = g0 * x + g1 * x ** (k + 1.0) / (k + 1.0)
        lam = tg.theta_V / (gam * cpt)
        a = (1.0 - tg.theta_V - tg.sigma_V) / cpt
        Vm = tg.b / tg.sigma_V
        v = gam * cpt * Vm
        Ps = v * (1.0 - x) / LB
        h = site_C * Ps
        Y = tg.baskets_per_person * tg.N
        K = Y * J / (1.0 - a * tg.delta)
        T = h * Y + tg.b * tg.delta * K
        chi = float(np.log1p(v / Ps) / tg.participation)
        e = Economy(N=tg.N, T=T, h=h, a=a, b=tg.b, lam=lam, g0=g0, g1=g1, k=k, eta=1.0, chi_max=chi, rho=rho,
                    delta=tg.delta)
        out.append((e, dict(info, k=k, gamma=gam)))
    return sorted(out, key=lambda p: p[1]["k"])


def target_residuals(e: Economy, tg: ChainTargets):
    """Each of the seven targets missed at the solved equilibrium (relative for output, absolute shares otherwise)."""
    q = solve(e)
    lab = q["labour_share_bea"] if tg.basis == "bea" else q["labor_share"]
    site = e.h / q["Ps"] if tg.site_basis == "basket" else e.h * q["Y"] / (q["income"] + e.delta * q["Vm"] * q["K"])
    return dict(labour=lab - tg.labour, participation=q["participation"] - tg.participation,
                baskets=(q["Y"] / e.N - tg.baskets_per_person) / tg.baskets_per_person, site=site - tg.site,
                theta_V=q["theta_V"] - tg.theta_V, chain_share=q["chain_share"] - tg.chain_share,
                sigma_V=q["sigma_V"] - tg.sigma_V)


def rate_headroom(e: Economy, hi_pp: float = 20.0):
    """The largest sustained rise in the required return (pp, found to 60 bisections) at which a land-scarce
    interior equilibrium still exists. Beyond it the machine chain's ceiling falls below the tasks the labour force
    can staff (labour demand exceeds supply at the ceiling) and solve raises NoEquilibrium."""
    def ok(d):
        try:
            solve(replace(e, rho=e.rho + d / 100.0))
            return True
        except NoEquilibrium:
            return False
    if ok(hi_pp):
        return hi_pp
    lo, hi = 0.0, hi_pp
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if ok(mid) else (lo, mid)
    return lo


if __name__ == "__main__":
    import appendix_b
    for e, info in calibrate_c(appendix_b.SHARES):
        q = solve(e)
        print(f"k {e.k:.4f}: a {e.a:.4f}  lam {e.lam:.4f}  rho {e.rho:.5f}  h {e.h:.6f}  T {e.T:.6f}  chi_max {e.chi_max:.4f}"
              f"  x* {q['x']:.5f}  w/P_s {q['real_wage']:.4f}  N_a/N {q['participation']:.4f}")
