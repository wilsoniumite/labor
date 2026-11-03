# appendix_b.py — the economy of the paper's Appendix B, solved: task assignment on [0, 1], durable machines priced at
# Appendix A.4's user cost, household participation, and support funded by a provider who owns the land and the machines.
# Plain functions on a parameter dict; numpy and scipy only. The paper's numerical instance (Appendix B and Figure 3) is
# the SSRN version's (2026-09-23), in the flow benchmark rho = 0, delta = 1: PRINTED below. The durable-machine economies
# in TEST_ECONOMIES exercise Lemma B.1's general form in the checks; the paper prints no number from them.
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
# are closed to machines at every wage (the machine services that would replace an hour cost more than the hour): the
# ceiling x_c is the first such task (1 if none), and the equilibrium n_D(x*) = n_S(x*) is sought on (0, x_c). At x_c,
# v and P_s are unbounded but v / P_s is not; it is computed in the form
# (rho+delta) b gamma / [(rho+delta) b (gamma (1 - x) + J) + h D], finite at D = 0.
#
# Run from pinning/:  python3 code/appendix_b.py      (prints the paper's Appendix B and Figure 3 numbers)

import numpy as np
from scipy.optimize import brentq

KEYS = ("N", "T", "h", "a", "b", "lam", "g0", "g1", "k", "eta", "chi_max", "rho", "delta")

# The paper's instance (Appendix B as printed in the SSRN version, 2026-09-23): the flow benchmark.
PRINTED = dict(N=4.0, T=10.0, h=1.0, a=0.3, b=0.4, lam=0.05, g0=0.2, g1=0.8, k=1.0, eta=1.0, chi_max=1.0,
               rho=0.0, delta=1.0)

# Figure 3's three economies: baseline; recursive automation (no labor in the machine chain); task automation (gamma
# halved at every task).
SCENARIOS = (("baseline", {}), ("recursive", {"lam": 0.0}), ("task", {"eta": 0.5}))

# Appendix B's illustrative automation path: retain the instance, set lambda = 0 and gamma_eta(x) = eta (1 + x).
SEQUENCE = dict(lam=0.0, g0=1.0, g1=1.0, k=1.0)

# Durable machines (rho > 0, delta < 1), for the checks of Lemma B.1's general form: the instance with a ten-year
# machine and a 5 percent return (no ceiling binds), and a labor-heavy machine chain with a convex schedule whose ceiling
# binds (x_c < 1), its margin chosen well below the ceiling, where the program's discretization bounds stay useful.
TEST_ECONOMIES = {
    "durable": {**PRINTED, "rho": 0.05, "delta": 0.1},
    "ceiling": {**PRINTED, "rho": 0.04, "delta": 0.2, "lam": 4.0, "g0": 0.05, "g1": 0.95, "k": 2.0, "T": 6.0},
}


def gamma(P, x):
    return P["eta"] * (P["g0"] + P["g1"] * x ** P["k"])


def J(P, x):
    return P["eta"] * (P["g0"] * x + P["g1"] * x ** (P["k"] + 1.0) / (P["k"] + 1.0))


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
                chain_hours=chain, nD=nD, nS=supply(P, x), real_wage=real_wage(P, x))


def solve(P):
    """The interior equilibrium of Lemma B.1: n_D(x*) = n_S(x*) on (0, x_c), and what the paper reads off it."""
    xc = ceiling(P)
    f0, fc = excess_demand(P, 0.0), excess_demand(P, xc)
    if not (f0 > 0.0 > fc):
        raise ValueError(f"Lemma B.1's crossing fails: n_D - n_S = {f0:.4g} at 0 and {fc:.4g} at x_c = {xc:.6f}")
    x = brentq(lambda t: excess_demand(P, t), 0.0, xc, xtol=1e-16, rtol=4 * np.finfo(float).eps, maxiter=500)
    q = at(P, x)
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
    return {**P, **dict(SCENARIOS)[name]}


def figure3(P=PRINTED):
    """The equilibria Figure 3 marks: name -> solve()."""
    return {name: solve({**P, **kw}) for name, kw in SCENARIOS}


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
    """The automation path's economy at eta: lambda = 0, gamma_eta(x) = eta (1 + x)."""
    return {**P, **SEQUENCE, "eta": float(eta)}


def sequence_bound(P):
    """The path's wage bound per unit of eta: v = (rho + delta) b gamma_eta(x) / (1 - (rho + delta) a) with lambda = 0,
    and gamma_eta <= 2 eta, so v <= 2 b eta / (1 - a) in the flow benchmark."""
    cpt = P["rho"] + P["delta"]
    return cpt * P["b"] * (SEQUENCE["g0"] + SEQUENCE["g1"]) / (1.0 - cpt * P["a"])


def paper_numbers(P=PRINTED):
    """Every number Appendix B and the Figure 3 caption quote, unrounded, by name (checks/check_interior.py formats each
    and finds it in paper/main.tex, anchored to the words around it)."""
    q = solve(P)
    f3 = figure3(P)
    return {
        "x_star": q["x"], "v": q["v"], "Y": q["Y"], "N_a": q["n"], "final_hours": q["final_hours"],
        "chain_hours": q["chain_hours"], "support": q["support"], "provider_income": q["provider_income"],
        **{f"fig3_{s}_{k}": f3[s][key] for s in ("baseline", "recursive", "task")
           for k, key in (("w", "real_wage"), ("n", "participation"))},
        "capability_ratio": (SEQUENCE["g0"] + SEQUENCE["g1"]) / SEQUENCE["g0"],   # gamma_eta(1) / gamma_eta(0)
    }


if __name__ == "__main__":
    for name, P in (("the paper's instance (flow benchmark)", PRINTED), *TEST_ECONOMIES.items()):
        print(f"--- {name}")
        q = solve(P)
        print(f"  x* {q['x']:.6f}  x_c {q['x_ceiling']:.6f}  v {q['v']:.6f}  w/P_s {q['real_wage']:.6f}  N_a/N {q['participation']:.6f}"
              f"  Y {q['Y']:.6f}  N_a {q['n']:.6f} = {q['final_hours']:.6f} final + {q['chain_hours']:.6f} chain")
        print(f"  income {q['income']:.6g} = wages {q['wages']:.6g} + rent {q['rent']:.6g} + interest {q['interest']:.6g};"
              f"  N P_s {q['support']:.6g} of provider income {q['provider_income']:.6g} (funded: {q['funded']})")
    print("--- Figure 3 (the paper's instance)")
    for s, e in figure3().items():
        print(f"  {s:9s}: w/P_s {e['real_wage']:.4f}  N_a/N {e['participation']:.4f}  x* {e['x']:.5f}")
    print("--- the automation path (lambda 0, gamma = eta (1 + x))")
    for eta in (1.0, 0.1, 0.01):
        q = solve(sequence(PRINTED, eta))
        print(f"  eta {eta:<5}: v {q['v']:.6f} <= {sequence_bound(PRINTED) * eta:.6f}  N_a/N {q['participation']:.5f}"
              f"  funded {q['funded']}")
    print("--- the paper's numbers (paper_numbers())")
    for k, v in paper_numbers().items():
        print(f"  {k:22s} {v:.10g}")
