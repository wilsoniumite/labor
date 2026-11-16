# appendix_b.py — the economy of the paper's Appendix B, solved: task assignment on [0, 1], durable machines priced at
# Appendix A.4's user cost, household participation, and support funded by a provider who owns the land and the machines.
# Plain functions on a parameter dict; numpy and scipy only. The paper's numerical instance (Appendix B and Figure 3) is
# PRINTED below: illustrative, with durable machines, its parameters set from U.S.-like shares and a measured elasticity
# of substitution (how, below; set_from_targets() redoes it in closed form). TEST_ECONOMIES exercise the checks beyond
# it: the SSRN version's instance, in the flow benchmark, and a binding ceiling; the paper prints no number from them.
#
# THE MODEL (rent r = 1, the numeraire; v = w/r). gamma(x) = eta (g0 + g1 x^k), J(x) = the integral of gamma over [0, x].
# A machine costs V_m = a p_m + lambda v + b to build (machine services, hours, land), supplies one unit of service a
# period, and depreciates at delta; its owner requires the return rho, so a service unit rents at p_m = (rho + delta) V_m.
# At a threshold x (machines below, people above) the task condition v = gamma(x) p_m gives
#     D(x) = 1 - (rho + delta)(a + lambda gamma(x)),  p_m = (rho + delta) b / D,  V_m = b / D,  v = gamma p_m,
#     p = v (1 - x) + p_m J,  P_s = p + h.
# In a stationary state the stock X supplies X services: Y J to final tasks and a delta X to rebuilding delta X machines.
#     Y = T / (h + b delta J / (1 - a delta)),  X = Y J / (1 - a delta),
#     n_D = Y (1 - x) + lambda delta X,  n_S = N F(log(1 + v / P_s)),  F uniform on [0, chi_max].
# The basket's total requirements of hours and land (the replacement coefficients) are L_s = n_D / Y and B_s = T / Y, and
# P_s = v L_s + B_s + rho V_m X / Y; income = v n + T + rho V_m X (wages, rent, interest) = P_s Y. Tasks where D(x) <= 0
# are closed to machines at every wage (the machine services that would replace an hour embody more than the hour): the
# ceiling x_c is the first such task (1 if none), and the equilibrium n_D(x*) = n_S(x*) is sought on (0, x_c). At x_c,
# v and P_s are unbounded but v / P_s is not; it is computed in the form
# (rho+delta) b gamma / [(rho+delta) b (gamma (1 - x) + J) + h D], finite at D = 0.
#
# CAPABILITY GAINS ON A SET OF TASKS. P["gain"] = (lo, hi, f): machines become 1/f times as productive at the tasks
# [lo, hi) of the schedule, so their gamma is multiplied by f, and the schedule is relabeled so gamma increases (Section
# 3.1). gamma at position u of the relabeled schedule is the u-quantile of the task gammas: with G the base schedule's
# inverse (clipped to [0, 1]), the measure of tasks at or below y is min(G(y), lo) + max(G(y) - hi, 0)
# + max(min(G(y/f), hi) - lo, 0); J sums gamma over that set. Figure 3's task automation is the gain f = 1/2 on the tasks
# people perform at baseline, [x*, 1): the relabeled schedule is continuous and strictly increasing, with two kinks.
#
# A HARD WALL. P["H"] = |H| closes the tasks [1 - |H|, 1] to machines outright (Appendix E). If labor demand still
# exceeds supply with the margin at 1 - |H|, below the ceiling, labor holds only H: the margin no longer prices the hour,
# the rental is the user cost on the wage, p_m = (rho + delta)(lambda v + b)/(1 - (rho + delta) a), and v clears n_S.
#
# Run from pinning/:  python3 code/appendix_b.py      (prints the paper's Appendix B and Figure 3 numbers)

import numpy as np
from scipy.optimize import brentq

KEYS = ("N", "T", "h", "a", "b", "lam", "g0", "g1", "k", "eta", "chi_max", "rho", "delta")

# The paper's instance. Set: N 1, b 0.4, delta 0.05, and T 0.01, which fixes the units of gamma and lambda. Eight
# parameters (h, a, lambda, chi_max, rho and the schedule's g0, g1, k) solve eight targets of the order of U.S. data:
# labor 0.47 of a machine's build cost, machine services 0.20 of it, labor 0.47 of consumption on the full chain, site
# 0.06 of the basket, the machine chain 0.15 of hours, participation 0.60, 3 baskets a person, and an elasticity of
# substitution between machine services and labor at the margin of 0.6 (the range of estimates of the aggregate
# capital-labor elasticity: 0.40-0.60, Chirinko 2008; 0.5-0.7 for U.S. manufacturing, Oberfield and Raval 2021). The
# return is an outcome (0.093). set_from_targets() gives the solution in closed form; then two significant figures.
# The rounded instance has labor 0.471 of build cost, machine services 0.196, labor 0.476 of consumption, site 0.061,
# chain 0.150 of hours, participation 0.602, 2.97 baskets a person, and sigma 0.61 at its margin.
PRINTED = dict(N=1.0, T=0.01, h=0.0017, a=1.4, b=0.4, lam=7.3, g0=0.074, g1=14.0, k=19.0, eta=1.0, chi_max=2.2,
               rho=0.09, delta=0.05)

TARGETS = dict(theta_V=0.47, machines=0.20, labor=0.47, site=0.06, chain=0.15, participation=0.60, baskets=3.0,
               sigma=0.6)

# The SSRN version's instance (Appendix B as printed 2026-09-23), in the flow benchmark rho = 0, delta = 1.
SSRN_INSTANCE = dict(N=4.0, T=10.0, h=1.0, a=0.3, b=0.4, lam=0.05, g0=0.2, g1=0.8, k=1.0, eta=1.0, chi_max=1.0,
                     rho=0.0, delta=1.0)

# Figure 3's three economies: baseline; recursive automation (no labor in the machine chain); task automation (machines
# twice as productive at every task people perform at baseline, the schedule relabeled).
SCENARIOS = (("baseline", None), ("recursive", {"lam": 0.0}), ("task", "gain at people's tasks"))

# Appendix B's illustrative automation path: retain the instance, set lambda = 0 and scale its schedule by eta,
# gamma_eta(x) = eta (0.074 + 14 x^19); at eta = 1 it is Figure 3's recursive-automation economy.
SEQUENCE = dict(lam=0.0)

# For the checks beyond the printed instance: the SSRN version's flow instance, and a labor-heavy machine chain with a
# convex schedule whose ceiling binds (x_c < 1), its margin well below the ceiling, where the program's discretization
# bounds stay useful.
TEST_ECONOMIES = {
    "ssrn_flow": SSRN_INSTANCE,
    "ceiling": {**SSRN_INSTANCE, "rho": 0.04, "delta": 0.2, "lam": 4.0, "g0": 0.05, "g1": 0.95, "k": 2.0, "T": 6.0},
}


# ---------------------------------------------------------------- the schedule
def _g(P, x):
    return P["eta"] * (P["g0"] + P["g1"] * x ** P["k"])


def _J(P, x):
    return P["eta"] * (P["g0"] * x + P["g1"] * x ** (P["k"] + 1.0) / (P["k"] + 1.0))


def _dg(P, x):
    return P["eta"] * P["g1"] * P["k"] * x ** (P["k"] - 1.0)


def _ginv(P, y):
    """The task of the base schedule whose gamma is y, clipped to [0, 1]."""
    t = (y / P["eta"] - P["g0"]) / P["g1"]
    return 0.0 if t <= 0.0 else min(t ** (1.0 / P["k"]), 1.0)


def _pieces(P):
    """With a gain: the base schedule's three stretches [start, end) with the factor on their gamma."""
    lo, hi, f = P["gain"]
    return [(s, e, m) for s, e, m in ((0.0, lo, 1.0), (lo, hi, f), (hi, 1.0, 1.0)) if e > s]


def _held(P, y):
    """For each stretch, the base position up to which its tasks have gamma at most y (its start if none, its end if
    all): the stretches' tasks at or below the level y."""
    out = []
    for s, e, m in _pieces(P):
        if y >= m * _g(P, e):
            out.append(e)
        elif y <= m * _g(P, s):
            out.append(s)
        else:
            out.append(min(max(_ginv(P, y / m), s), e))
    return out


def _locate(P, x):
    """With a gain: the level y = gamma at position x of the relabeled schedule, and each stretch's held position there.
    Between consecutive stretch-end levels the set of stretches being filled is fixed; where only one is, its position
    follows from x directly (no inversion, so flat stretches stay exact); where two are, the level is found numerically,
    on a part of the schedule that is not flat."""
    pcs = _pieces(P)
    levels = sorted({m * _g(P, s) for s, e, m in pcs} | {m * _g(P, e) for s, e, m in pcs})
    cum = [sum(p - s for p, (s, e, m) in zip(_held(P, y), pcs)) for y in levels]
    i = max(0, min(int(np.searchsorted(cum, x, side="left")), len(levels) - 1))
    if i == 0:
        return levels[0], [s for s, e, m in pcs]
    ya, yb = levels[i - 1], levels[i]
    ha = _held(P, ya)
    filling = [j for j, (s, e, m) in enumerate(pcs) if m * _g(P, s) <= ya and m * _g(P, e) >= yb]
    if len(filling) == 1:
        j = filling[0]
        held = list(ha)
        held[j] = ha[j] + (x - cum[i - 1])
        s, e, m = pcs[j]
        return m * _g(P, held[j]), held
    y = brentq(lambda t: sum(p - s for p, (s, e, m) in zip(_held(P, t), pcs)) - x, ya, yb, xtol=1e-16,
               rtol=4 * np.finfo(float).eps, maxiter=400)
    return y, _held(P, y)


def gamma(P, x):
    if "gain" not in P:
        return _g(P, x)
    if np.ndim(x):
        return np.array([gamma(P, float(t)) for t in np.ravel(x)]).reshape(np.shape(x))
    return _locate(P, min(max(float(x), 0.0), 1.0))[0]


def J(P, x):
    if "gain" not in P:
        return _J(P, x)
    if np.ndim(x):
        return np.array([J(P, float(t)) for t in np.ravel(x)]).reshape(np.shape(x))
    if x <= 0.0:
        return 0.0
    y, held = _locate(P, min(float(x), 1.0))
    return sum(m * (_J(P, p) - _J(P, s)) for p, (s, e, m) in zip(held, _pieces(P)))


def dgamma(P, x):
    """gamma'(x): with a gain, one over the density of task gammas at gamma(x), summed over the stretches being filled
    there."""
    if "gain" not in P:
        return _dg(P, x)
    y, held = _locate(P, float(x))
    dens = 0.0
    for p, (s, e, m) in zip(held, _pieces(P)):
        lo_y, hi_y = m * _g(P, s), m * _g(P, e)
        if lo_y <= y and (y < hi_y or (e == 1.0 and y == hi_y)):     # the level is inside the stretch's range
            slope = m * _dg(P, p)
            dens += np.inf if slope == 0.0 else 1.0 / slope            # a flat start: gamma' = 0, as gamma'(0) = 0
    return 0.0 if dens == np.inf else 1.0 / dens


def kinks(P):
    """With a gain: the positions of the relabeled schedule where a stretch starts or stops being filled (gamma' jumps,
    or gamma jumps where no tasks lie between two levels)."""
    pcs = _pieces(P)
    levels = sorted({m * _g(P, s) for s, e, m in pcs} | {m * _g(P, e) for s, e, m in pcs})
    pos = [sum(p - s for p, (s, e, m) in zip(_held(P, y), pcs)) for y in levels]
    return sorted({round(u, 15) for u in pos if 1e-12 < u < 1.0 - 1e-12})


def capability_gain(P, lo, hi, f):
    """Machines 1/f times as productive at the tasks [lo, hi) of P's schedule; the schedule relabeled."""
    if "gain" in P:
        raise ValueError("one gain at a time")
    return {**P, "gain": (float(lo), float(hi), float(f))}


def task_automation(P, f=0.5):
    """Section 3.4's task automation as Figure 3 draws it: machines twice as productive at every task people perform in
    P's equilibrium, [x*, 1)."""
    return capability_gain(P, solve(P)["x"], 1.0, f)


def machine_task_gain(P, f=0.5):
    """Capability gains at the tasks machines already perform in P's equilibrium, [0, x*)."""
    return capability_gain(P, 0.0, solve(P)["x"], f)


# ---------------------------------------------------------------- the economy
def denominator(P, x):
    """D(x) = 1 - (rho + delta)(a + lambda gamma(x)): positive exactly where machines can take task x."""
    return 1.0 - (P["rho"] + P["delta"]) * (P["a"] + P["lam"] * gamma(P, x))


def ceiling(P):
    """x_c: the first task closed to machines at every wage (D = 0), or 1 if D(1) > 0."""
    if (P["rho"] + P["delta"]) * P["a"] >= 1.0 or P["a"] * P["delta"] >= 1.0:
        raise ValueError("(rho + delta) a < 1 fails: machine services cannot be produced at a finite price")
    if denominator(P, 0.0) <= 0.0:
        raise ValueError("D(0) <= 0: no task is open to machines")
    if denominator(P, 1.0) > 0.0:
        return 1.0
    return brentq(lambda x: denominator(P, x), 0.0, 1.0, xtol=1e-16, rtol=4 * np.finfo(float).eps)


def real_wage(P, x):
    """v / P_s at threshold x, in a form that stays finite at the ceiling (D = 0)."""
    cpt, g, j = P["rho"] + P["delta"], gamma(P, x), J(P, x)
    return cpt * P["b"] * g / (cpt * P["b"] * (g * (1.0 - x) + j) + P["h"] * denominator(P, x))


def F(P, z):
    """The work-cost distribution: chi uniform on [0, chi_max]."""
    return min(max(z / P["chi_max"], 0.0), 1.0)


def demand(P, x):
    """(Y, X, final-task hours, machine-sector hours, n_D) at threshold x."""
    ad = P["a"] * P["delta"]
    j = J(P, x)
    Y = P["T"] / (P["h"] + P["b"] * P["delta"] * j / (1.0 - ad))
    X = Y * j / (1.0 - ad)
    final, chain = Y * (1.0 - x), P["lam"] * P["delta"] * X
    return Y, X, final, chain, final + chain


def supply(P, x):
    return P["N"] * F(P, np.log1p(real_wage(P, x)))


def excess_demand(P, x):
    return demand(P, x)[4] - supply(P, x)


def at(P, x):
    """Prices and quantities at threshold x < x_c."""
    cpt, D = P["rho"] + P["delta"], denominator(P, x)
    if D <= 0.0:
        raise ValueError(f"x = {x} is at or above the machine chain's ceiling")
    g, j = gamma(P, x), J(P, x)
    pm = cpt * P["b"] / D
    Vm, v = pm / cpt, g * pm
    p = v * (1.0 - x) + pm * j
    Ps = p + P["h"]
    Y, X, final, chain, nD = demand(P, x)
    return dict(x=x, gamma=g, J=j, D=D, pm=pm, Vm=Vm, v=v, p=p, Ps=Ps, Y=Y, X=X, final_hours=final,
                chain_hours=chain, nD=nD, nS=supply(P, x), real_wage=real_wage(P, x), regime="interior")


def at_wall(P, xH):
    """Labor holds only the hard wall [xH, 1]: quantities at the threshold xH, the wage that clears participation, and
    the rental at the user cost on that wage."""
    cpt = P["rho"] + P["delta"]
    Y, X, final, chain, nD = demand(P, xH)
    j = J(P, xH)
    need = np.expm1(P["chi_max"] * nD / P["N"])            # the w/P_s at which n_S = n_D

    def real(v):
        pm = cpt * (P["lam"] * v + P["b"]) / (1.0 - cpt * P["a"])
        return v / (v * (1.0 - xH) + pm * j + P["h"])
    v0 = gamma(P, xH) * cpt * P["b"] / denominator(P, xH)  # the wage that puts the margin at xH
    if not real(v0) <= need < 1.0 / ((1.0 - xH) + cpt * P["lam"] * j / (1.0 - cpt * P["a"])):
        raise ValueError("no equilibrium with labor holding only the wall")
    v = brentq(lambda t: real(t) - need, v0, v0 * 1e15, xtol=1e-300, rtol=4 * np.finfo(float).eps, maxiter=500)
    pm = cpt * (P["lam"] * v + P["b"]) / (1.0 - cpt * P["a"])
    p = v * (1.0 - xH) + pm * j
    return dict(x=xH, gamma=gamma(P, xH), J=j, D=None, pm=pm, Vm=pm / cpt, v=v, p=p, Ps=p + P["h"], Y=Y, X=X,
                final_hours=final, chain_hours=chain, nD=nD, nS=nD, real_wage=v / (p + P["h"]), regime="only H")


def solve(P):
    """The interior equilibrium of Lemma B.1: n_D(x*) = n_S(x*) on (0, x_c), and what the paper reads off it; with a
    hard wall that the margin would pass, labor holding only H."""
    xc = ceiling(P)
    xH = 1.0 - P.get("H", 0.0)
    if xH < xc and excess_demand(P, xH) >= 0.0:
        q = at_wall(P, xH)
    else:
        up = min(xc, xH)
        f0, fc = excess_demand(P, 0.0), excess_demand(P, up)
        if not (f0 > 0.0 > fc):
            raise ValueError(f"Lemma B.1's crossing fails: n_D - n_S = {f0:.4g} at 0 and {fc:.4g} at x_c = {xc:.6f}")
        x = brentq(lambda t: excess_demand(P, t), 0.0, up, xtol=1e-16, rtol=4 * np.finfo(float).eps, maxiter=500)
        q = at(P, x)
    x = q["x"]
    n = q["nD"]
    interest = P["rho"] * q["Vm"] * q["X"]
    income = q["v"] * n + P["T"] + interest
    theta, sigma = P["lam"] * q["v"] / q["Vm"], P["b"] / q["Vm"]
    j, ad = q["J"], P["a"] * P["delta"]
    q.update(x_ceiling=xc, n=n, participation=n / P["N"], income=income, wages=q["v"] * n, rent=P["T"],
             interest=interest, interest_share=interest / income, replacement=P["delta"] * q["Vm"] * q["X"],
             theta_V=theta, sigma_V=sigma,
             multiplier=1.0 + theta / sigma,                     # d ln(w/r) / d ln gamma(x*), margin and return fixed
             L_s=1.0 - x + P["lam"] * P["delta"] * j / (1.0 - ad),
             B_s=P["h"] + P["b"] * P["delta"] * j / (1.0 - ad),
             provider_income=P["T"] + interest, support=P["N"] * q["Ps"],
             provider_baskets=(P["T"] + interest) / q["Ps"] - P["N"],
             funded=P["T"] + interest >= P["N"] * q["Ps"],
             nS_ceiling=supply(P, xc), nD_ceiling=demand(P, xc)[4])
    return q


def scenario(P, name):
    if name == "task":
        return task_automation(P)
    return {**P, **(dict(SCENARIOS)[name] or {})}


def figure3(P=PRINTED):
    """The equilibria Figure 3 marks: name -> solve()."""
    return {name: solve(scenario(P, name)) for name, _ in SCENARIOS}


def demand_curve(P, n=3000):
    """Labor demand n_D/N against w/P_s as the threshold moves over [0, x_c], points packed toward x_c."""
    xc = ceiling(P)
    s = np.linspace(0.0, 1.0, n)
    xs = xc * (1.0 - (1.0 - s) ** 2)
    return (np.array([demand(P, x)[4] for x in xs]) / P["N"], np.array([real_wage(P, x) for x in xs]), xs)


def participation_curve(P, upto=1.0, n=800):
    """N_a/N from 0 to upto and the w/P_s at which it is supplied: w/P_s = exp(chi_max N_a/N) - 1 (N_a/N <= 1)."""
    na = np.linspace(0.0, min(upto, 1.0), n)
    return na, np.expm1(P["chi_max"] * na)


def sequence(P, eta):
    """The automation path's economy at eta: lambda = 0, gamma_eta(x) = eta (g0 + g1 x^k)."""
    return {**P, **SEQUENCE, "eta": float(eta)}


def sequence_bound(P):
    """The path's wage bound per unit of eta: v = (rho + delta) b gamma_eta(x) / (1 - (rho + delta) a) with lambda = 0,
    and gamma_eta(x) <= eta gamma(1) = eta (g0 + g1), so v <= eta gamma(1) (rho + delta) b / (1 - (rho + delta) a)."""
    cpt = P["rho"] + P["delta"]
    return cpt * P["b"] * (P["g0"] + P["g1"]) / (1.0 - cpt * P["a"])


# ---------------------------------------------------------------- what the paper reads off the instance
def shares(P, q):
    """The shares the instance was set from: labor's and machine services' shares of a machine's build cost, labor's
    full-chain share of consumption, the site's share of the basket, the chain's share of hours."""
    cpt = P["rho"] + P["delta"]
    return dict(theta_V=P["lam"] * q["v"] / q["Vm"], machines=cpt * P["a"], labor=q["v"] * (1.0 - q["x"]) / q["Ps"],
                site=P["h"] / q["Ps"], chain=q["chain_hours"] / q["n"])


def sigma_margin(P, x):
    """The elasticity of substitution between machine services and labor in final tasks at the margin x: the elasticity
    of machine-hours per human-hour there, J(x)/(1 - x), with respect to w/p_m = gamma(x)."""
    g = gamma(P, x)
    return (g / J(P, x) + 1.0 / (1.0 - x)) * g / dgamma(P, x)


def ceiling_reading(P, q):
    """Section 3.3's ceiling at an interior equilibrium: theta = gamma(x*) lambda-tilde_m, the labor share of
    machine-service cost at the margin; gamma(x_c)/gamma(x*) = 1/theta; the contestable share of the tasks labor performs,
    (x_c - x*)/(1 - x*); and its first-order value s_M sigma ln(1/theta), s_M the machines' share of final-task cost."""
    cpt = P["rho"] + P["delta"]
    theta = q["gamma"] * cpt * P["lam"] / (1.0 - cpt * P["a"])
    sM = q["pm"] * q["J"] / (q["pm"] * q["J"] + q["v"] * (1.0 - q["x"]))
    sig = sigma_margin(P, q["x"])
    return dict(theta=theta, wall_multiple=gamma(P, q["x_ceiling"]) / q["gamma"],
                contestable=(q["x_ceiling"] - q["x"]) / (1.0 - q["x"]), s_M=sM, sigma=sig,
                first_order=sM * sig * np.log(1.0 / theta))


def set_from_targets(tg=TARGETS, N=1.0, b=0.4, delta=0.05, T=0.01):
    """The instance before rounding, in closed form. Participation, the chain's share of hours and baskets a person give
    the margin, 1 - x* = participation (1 - chain) N / baskets; the machine-cost shares and the chain's share give the
    return; labor's and the site's shares of the basket leave the schedule one condition, J(x*) = R gamma(x*)(1 - x*)
    with R = (1 - labor - site)/labor; sigma at the margin fixes its exponent; T fixes the units of gamma and lambda."""
    x = 1.0 - tg["participation"] * N * (1.0 - tg["chain"]) / (tg["baskets"] * N)
    R = (1.0 - tg["labor"] - tg["site"]) / tg["labor"]
    cpt = tg["machines"] * delta + tg["theta_V"] * delta * R * (1.0 - tg["chain"]) / tg["chain"]

    def shape(k):                                          # gamma = c + x^k meeting the condition at x
        return (R * x ** k * (1.0 - x) - x ** (k + 1.0) / (k + 1.0)) / (x - R * (1.0 - x))

    def sig(k):
        c = shape(k)
        g, j = c + x ** k, c * x + x ** (k + 1.0) / (k + 1.0)
        return (g / j + 1.0 / (1.0 - x)) * g / (k * x ** (k - 1.0))
    k_lo = brentq(shape, 1.0 + 1e-9, 60.0) if shape(1.0 + 1e-9) * shape(60.0) < 0 else 1.0
    k = brentq(lambda kk: sig(kk) - tg["sigma"], k_lo + 1e-6, 400.0, xtol=1e-14)
    c = shape(k)
    a = tg["machines"] / cpt
    D = 1.0 - tg["machines"] - tg["theta_V"]

    def scaled(s):                                         # gamma = s (c + x^k); everything else follows
        g, j = s * (c + x ** k), s * (c * x + x ** (k + 1.0) / (k + 1.0))
        pm = cpt * b / D
        v = g * pm
        Ps = v * (1.0 - x) / tg["labor"]
        h = tg["site"] * Ps
        return dict(g=g, h=h, T=tg["baskets"] * N * (h + b * delta * j / (1.0 - a * delta)), v=v, Ps=Ps)
    s = T / scaled(1.0)["T"]                               # T is linear in the scale of gamma
    q = scaled(s)
    return dict(N=N, T=T, h=q["h"], a=a, b=b, lam=tg["theta_V"] / (cpt * q["g"]), g0=s * c, g1=s, k=k, eta=1.0,
                chi_max=np.log1p(q["v"] / q["Ps"]) / tg["participation"], rho=cpt - delta, delta=delta)


def wall_floor(P, H):
    """Appendix E's bound in this economy: as gamma_eta -> 0 outside H along the path, output tends to T/h baskets and
    labor demand to |H| T/h, so participation tends to |H| T/(N h) when that is below one."""
    return H * P["T"] / (P["N"] * P["h"])


def paper_numbers(P=PRINTED):
    """Every number Appendix B, the Figure 3 caption, Sections 3.3 and 6.1 and Appendix E quote, unrounded, by name
    (checks/check_interior.py formats each and finds it in paper/main.tex, anchored to the words around it)."""
    q = solve(P)
    f3 = figure3(P)
    cr = ceiling_reading(P, q)
    path = {eta: solve(sequence(P, eta))["participation"] for eta in (1.0, 0.01, 0.001)}
    peak_eta = np.exp(np.linspace(np.log(0.01), 0.0, 401))
    peak = max((solve(sequence(P, e))["participation"], e) for e in peak_eta)
    return {
        "x_star": q["x"], "x_c": q["x_ceiling"], "v": q["v"], "Y": q["Y"], "N_a": q["n"], "final_hours": q["final_hours"],
        "chain_hours": q["chain_hours"], "support": q["support"], "provider_income": q["provider_income"],
        **shares(P, q), "participation": q["participation"],
        **cr,
        **{f"fig3_{s}_{k}": f3[s][key] for s in ("baseline", "recursive", "task")
           for k, key in (("w", "real_wage"), ("n", "participation"))},
        "machine_gain_w": solve(machine_task_gain(P))["real_wage"] / q["real_wage"] - 1.0,
        "seq_bound": sequence_bound(P), "seq_n_eta1": path[1.0], "seq_n_eta001": path[0.01], "seq_n_eta0001": path[0.001],
        "seq_peak_n": peak[0], "seq_peak_eta": peak[1],
        "capability_ratio": (P["g0"] + P["g1"]) / P["g0"],                       # gamma_eta(1) / gamma_eta(0)
        "land_baskets": P["T"] / (P["N"] * P["h"]), "wall_floor_5pct": wall_floor(P, 0.05),
    }


if __name__ == "__main__":
    for name, P in (("the paper's instance", PRINTED), *TEST_ECONOMIES.items()):
        print(f"--- {name}")
        q = solve(P)
        print(f"  x* {q['x']:.6f}  x_c {q['x_ceiling']:.6f}  v {q['v']:.6f}  w/P_s {q['real_wage']:.6f}  N_a/N {q['participation']:.6f}"
              f"  Y {q['Y']:.6f}  N_a {q['n']:.6f} = {q['final_hours']:.6f} final + {q['chain_hours']:.6f} chain")
        print(f"  income {q['income']:.6g} = wages {q['wages']:.6g} + rent {q['rent']:.6g} + interest {q['interest']:.6g};"
              f"  N P_s {q['support']:.6g} of provider income {q['provider_income']:.6g} (funded: {q['funded']})")
    print("--- the instance before rounding (set_from_targets())")
    print("  " + ", ".join(f"{k} {v:.6g}" for k, v in set_from_targets().items()))
    print("--- Figure 3 (the paper's instance)")
    for s, e in figure3().items():
        print(f"  {s:9s}: w/P_s {e['real_wage']:.4f}  N_a/N {e['participation']:.4f}  x* {e['x']:.5f}")
    print("--- the automation path (lambda 0, gamma scaled by eta)")
    for eta in (1.0, 0.3, 0.1, 0.01, 0.001):
        q = solve(sequence(PRINTED, eta))
        print(f"  eta {eta:<5}: v {q['v']:.6f} <= {sequence_bound(PRINTED) * eta:.6f}  N_a/N {q['participation']:.5f}"
              f"  funded {q['funded']}")
    print("--- the paper's numbers (paper_numbers())")
    for k, v in paper_numbers().items():
        print(f"  {k:22s} {v:.10g}")
