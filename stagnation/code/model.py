# model.py — the stationary task economy of "Understanding the Great Stagnation", Sections 3-4.
# Plain functions on a parameter dict (numpy and scipy only), written to be pasted into a notebook cell and tinkered
# with. This is the paper's own implementation; checks/check_theory.py compares its funded-exit case with the
# independent solver of the companion paper (../pinning/code/appendix_b.py) and checks every result on it.
#
# THE MODEL (land rent r = 1 is the numeraire; v = w/r; omega = w/P_s, the wage in baskets).
#   Tasks x in [0, 1], one unit each per unit of the final good. An hour completes one unit of any task; a machine-hour
#   completes 1/gamma(x) units of task x, gamma(x) = eta (g0 + g1 x^k): eta scales machine capability (lower eta =
#   better machines at every task). J(x) = integral of gamma over [0, x].
#   A machine costs V_m = a p_m + lambda v + b (machine services, hours, land) to build, supplies one unit of service a
#   period and depreciates at delta; its owner requires the return rho: p_m = (rho + delta) V_m. At a margin x
#   (machines below, people above):
#       D(x) = 1 - (rho + delta)(a + lambda gamma(x))   [= land's share of a machine's build cost, b / V_m]
#       p_m = (rho + delta) b / D,  V_m = b / D,  v = gamma(x) p_m,  p = v (1 - x) + p_m J,  P_s = p + h.
#   Stationary quantities (the stock X supplies Y J to final tasks and a delta X to rebuilding):
#       B_s = h + b delta J / (1 - a delta)        full-chain land per basket
#       L_s = 1 - x + lambda delta J / (1 - a delta) full-chain hours per basket
#       Y = T / B_s,  X = Y J / (1 - a delta),  n_D = T L_s / B_s,  output per hour pi = Y / n_D = 1 / L_s.
#   People: N persons. A share theta has no support outside work and always works. The rest have funded exit: one
#   basket of support in work and out, and work iff log(1 + omega + Delta) >= chi, chi uniform on [0, chi_max]; Delta
#   is a payment of Delta baskets to every worker (support conditioned on work). Labor supply at margin x:
#       n_S = N [theta + (1 - theta) F(log(1 + omega(x) + Delta))].
#   A provider owning the land and the machines pays support and Delta from rent and interest:
#       funded iff T + rho V_m X >= P_s [(1 - theta) N + Delta n].
#   The equilibrium is the margin x* in (0, x_c) where n_D = n_S; x_c is the first task with D = 0 (1 if none).
#
# Run from stagnation/:  ../venv/bin/python code/model.py     (prints the instance, the illustrations, the paths)

import numpy as np
from scipy.optimize import brentq

# The instance: Bage and Wilson (2026), Appendix B, set there from U.S.-like shares, with funded exit (theta = 0) and
# no conditioning (Delta = 0). theta and Delta are this paper's additions.
BASE = dict(N=1.0, T=0.01, h=0.0017, a=1.4, b=0.4, lam=7.3, g0=0.01, g1=0.99, k=4.4, eta=1.0, chi_max=2.2,
            rho=0.09, delta=0.05, theta=0.0, Delta=0.0)

# The illustrations the paper reports: who can leave work.
REGIMES = {
    "funded": dict(theta=0.0, Delta=0.0),        # every person has funded, unconditional exit
    "quarter": dict(theta=0.25, Delta=0.0),      # a quarter have no support outside work
    "enclosed": dict(theta=1.0, Delta=0.0),      # nobody has support outside work
    "conditioned": dict(theta=0.0, Delta=0.3),   # support for everyone, plus 0.3 baskets for working
}

ETAS = np.logspace(0.0, -6.0, 121)   # the path of machine progress: capability at every task up a millionfold
RHOS = np.linspace(0.01, 0.10, 91)   # the required return


# ---------------------------------------------------------------------------------------------------- the schedule
def gamma(P, x):
    return P["eta"] * (P["g0"] + P["g1"] * x ** P["k"])


def gamma_prime(P, x):
    return P["eta"] * P["g1"] * P["k"] * x ** (P["k"] - 1.0)


def J(P, x):
    return P["eta"] * (P["g0"] * x + P["g1"] * x ** (P["k"] + 1.0) / (P["k"] + 1.0))


def D(P, x):
    """1 - (rho + delta)(a + lambda gamma(x)): land's share of a machine's build cost; positive where machines can
    take task x."""
    return 1.0 - (P["rho"] + P["delta"]) * (P["a"] + P["lam"] * gamma(P, x))


def ceiling(P):
    """x_c: the first task closed to machines at every wage (D = 0), or 1 if D(1) > 0."""
    if (P["rho"] + P["delta"]) * P["a"] >= 1.0 or P["a"] * P["delta"] >= 1.0:
        raise ValueError("machine services cannot be produced at a finite price")
    if D(P, 0.0) <= 0.0:
        raise ValueError("no task is open to machines")
    if D(P, 1.0) > 0.0:
        return 1.0
    return brentq(lambda x: D(P, x), 0.0, 1.0, xtol=1e-16, rtol=4 * np.finfo(float).eps)


# ---------------------------------------------------------------------------------------------- prices at a margin
def p_m(P, x):
    return (P["rho"] + P["delta"]) * P["b"] / D(P, x)


def v(P, x):
    """w/r at margin x: the task condition w = p_m gamma(x*)."""
    return gamma(P, x) * p_m(P, x)


def P_s(P, x):
    return v(P, x) * (1.0 - x) + p_m(P, x) * J(P, x) + P["h"]


def omega(P, x):
    """w/P_s at margin x, in a form that stays finite at the ceiling (D = 0)."""
    c, g = P["rho"] + P["delta"], gamma(P, x)
    return c * P["b"] * g / (c * P["b"] * (g * (1.0 - x) + J(P, x)) + P["h"] * D(P, x))


# ------------------------------------------------------------------------------------------ quantities at a margin
def B_s(P, x):
    return P["h"] + P["b"] * P["delta"] * J(P, x) / (1.0 - P["a"] * P["delta"])


def L_s(P, x):
    return 1.0 - x + P["lam"] * P["delta"] * J(P, x) / (1.0 - P["a"] * P["delta"])


def B_s_prime(P, x):
    return P["b"] * P["delta"] * gamma(P, x) / (1.0 - P["a"] * P["delta"])


def L_s_prime(P, x):
    return -1.0 + P["lam"] * P["delta"] * gamma(P, x) / (1.0 - P["a"] * P["delta"])


def n_D(P, x):
    return P["T"] * L_s(P, x) / B_s(P, x)


def F(P, z):
    """The work-cost distribution: chi uniform on [0, chi_max]."""
    return min(max(z / P["chi_max"], 0.0), 1.0)


def n_S(P, x):
    return P["N"] * (P["theta"] + (1.0 - P["theta"]) * F(P, np.log1p(omega(P, x) + P["Delta"])))


def N_inf(P):
    """The hours that remain when the wage buys nothing: N [theta + (1 - theta) F(log(1 + Delta))]."""
    return P["N"] * (P["theta"] + (1.0 - P["theta"]) * F(P, np.log1p(P["Delta"])))


def pi_ceiling(P):
    """Output per hour's limit along machine progress: T / (h N_inf), infinite if no hours remain."""
    n = N_inf(P)
    return P["T"] / (P["h"] * n) if n > 0.0 else np.inf


def psi(P, x):
    """(B_s'/B_s) / (-L_s'/L_s): land freed per unit of labor added when the margin moves."""
    return (B_s_prime(P, x) / B_s(P, x)) / (-L_s_prime(P, x) / L_s(P, x))


def elasticity(P, x):
    """d log(output per hour) / d log(hours) across equilibria with the same technology (Lemma 1)."""
    return -1.0 / (1.0 + psi(P, x))


# -------------------------------------------------------------------------------------------------- the equilibrium
def excess(P, x):
    return n_D(P, x) - n_S(P, x)


def solve(P):
    """The interior equilibrium n_D(x*) = n_S(x*) on (0, x_c), and everything the paper reads off it."""
    xc = ceiling(P)
    f0, fc = excess(P, 0.0), excess(P, xc)
    if not (f0 > 0.0 > fc):
        raise ValueError(f"no interior crossing: n_D - n_S = {f0:.4g} at 0 and {fc:.4g} at x_c = {xc:.6f}")
    x = brentq(lambda t: excess(P, t), 0.0, xc, xtol=1e-16, rtol=4 * np.finfo(float).eps, maxiter=500)
    pm, vv, Ps = p_m(P, x), v(P, x), P_s(P, x)
    Vm = pm / (P["rho"] + P["delta"])
    Y = P["T"] / B_s(P, x)
    X = Y * J(P, x) / (1.0 - P["a"] * P["delta"])
    n = n_D(P, x)
    interest = P["rho"] * Vm * X
    income = vv * n + P["T"] + interest
    support = Ps * ((1.0 - P["theta"]) * P["N"] + P["Delta"] * n)
    return dict(x=x, x_c=xc, gamma=gamma(P, x), J=J(P, x), D=D(P, x), pm=pm, Vm=Vm, v=vv, p=Ps - P["h"], Ps=Ps,
                omega=omega(P, x), Y=Y, X=X, n=n, nS=n_S(P, x), pi=Y / n, L_s=L_s(P, x), B_s=B_s(P, x),
                final_hours=Y * (1.0 - x), chain_hours=P["lam"] * P["delta"] * X,
                income=income, wages=vv * n, interest=interest, labor_share=vv * n / income,
                participation=n / P["N"], psi=psi(P, x), elasticity=elasticity(P, x),
                land_price_hours=1.0 / (P["rho"] * vv) if P["rho"] > 0 else np.inf,
                provider_income=P["T"] + interest, support=support, funded=P["T"] + interest >= support)


def with_(P, **kw):
    return {**P, **kw}


def path(P, etas=ETAS):
    """Equilibria along machine progress gamma_eta = eta (g0 + g1 x^k)."""
    return [solve(with_(P, eta=float(e))) for e in etas]


def rates(P, rhos=RHOS):
    """Equilibria along the required return."""
    return [solve(with_(P, rho=float(r))) for r in rhos]


def small_eta_interior(P):
    """Proposition 2's sufficient condition for interior equilibria at small eta when no hours remain (N_inf = 0):
    N F'(0) (rho + delta) b gamma_hat(1) (1 - a delta) > T lambda delta J_hat(1) (1 - (rho + delta) a), with
    gamma_hat, J_hat the schedule at eta = 1. Returns (lhs, rhs)."""
    c, g1, j1 = P["rho"] + P["delta"], P["g0"] + P["g1"], P["g0"] + P["g1"] / (P["k"] + 1.0)
    lhs = P["N"] / P["chi_max"] * c * P["b"] * g1 * (1.0 - P["a"] * P["delta"])
    rhs = P["T"] * P["lam"] * P["delta"] * j1 * (1.0 - c * P["a"])
    return lhs, rhs


def growth_per_log_capability(P, eta, step=1e-3):
    """d log(output per hour) / d log(1/eta) at eta: the growth of output per hour per unit of growth in machine
    capability (Proposition 2(iv))."""
    a, b = solve(with_(P, eta=eta)), solve(with_(P, eta=eta * np.exp(-step)))
    return (np.log(b["pi"]) - np.log(a["pi"])) / step


def numbers(P=BASE):
    """Every model number the paper quotes, unrounded, by name (checks/check_theory.py formats each and finds it in
    paper/main.tex next to the words it belongs to)."""
    q = {k: solve(with_(P, **kw)) for k, kw in REGIMES.items()}
    out = dict(
        x_base=q["funded"]["x"], pi_base=q["funded"]["pi"], n_base=q["funded"]["n"],
        eps_base=q["funded"]["elasticity"], psi_base=q["funded"]["psi"],
        pi_enclosed=q["enclosed"]["pi"], x_enclosed=q["enclosed"]["x"], Y_base=q["funded"]["Y"],
        Y_enclosed=q["enclosed"]["Y"],
        pi_drop_enclosed=1.0 - q["enclosed"]["pi"] / q["funded"]["pi"],
        pi_quarter=q["quarter"]["pi"], n_quarter=q["quarter"]["n"],
        pi_conditioned=q["conditioned"]["pi"], n_conditioned=q["conditioned"]["n"],
        ls_base=q["funded"]["labor_share"], ls_enclosed=q["enclosed"]["labor_share"],
        D_base=q["funded"]["D"], invD_base=1.0 / q["funded"]["D"], invD_enclosed=1.0 / q["enclosed"]["D"],
        ceil_enclosed=pi_ceiling(with_(P, **REGIMES["enclosed"])),
        ceil_quarter=pi_ceiling(with_(P, **REGIMES["quarter"])),
        ceil_conditioned=pi_ceiling(with_(P, **REGIMES["conditioned"])),
        Ninf_conditioned=N_inf(with_(P, **REGIMES["conditioned"])),
    )
    e1, e2 = solve(with_(P, **REGIMES["enclosed"])), solve(with_(P, **REGIMES["enclosed"], rho=0.04))
    f1, f2 = solve(with_(P, **REGIMES["funded"])), solve(with_(P, **REGIMES["funded"], rho=0.04))
    out.update(rate_v_drop_enclosed=1.0 - e2["v"] / e1["v"], rate_omega_drop_enclosed=1.0 - e2["omega"] / e1["omega"],
               rate_land_mult_enclosed=e2["land_price_hours"] / e1["land_price_hours"],
               rate_pi_rise_funded=f2["pi"] / f1["pi"] - 1.0, rate_n_funded_low=f2["n"],
               rate_v_drop_funded=1.0 - f2["v"] / f1["v"])
    return out


if __name__ == "__main__":
    print("--- the regimes at the instance's technology")
    for k, kw in REGIMES.items():
        q = solve(with_(BASE, **kw))
        print(f"  {k:12s} x* {q['x']:.5f}  hours {q['n']:.5f}  Y {q['Y']:.5f}  pi {q['pi']:.4f}  w/r {q['v']:.5f}"
              f"  w/P_s {q['omega']:.4f}  labor share {q['labor_share']:.4f}  eps {q['elasticity']:.4f}"
              f"  funded {q['funded']} ({q['support']:.5f} of {q['provider_income']:.5f})")
    print("--- machine progress: output per hour (hours) as capability rises 10x, 100x, ... 1e6x")
    for k, kw in REGIMES.items():
        P = with_(BASE, **kw)
        row = [solve(with_(P, eta=e)) for e in (1, 1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6)]
        print(f"  {k:12s} ceiling {pi_ceiling(P):8.4g}: " + "  ".join(f"{q['pi']:.4g} ({q['n']:.3g})" for q in row))
        print(f"  {'':12s} growth per log capability at 1e-2, 1e-4, 1e-6: "
              + ", ".join(f"{growth_per_log_capability(P, e):.5f}" for e in (1e-2, 1e-4, 1e-6)))
    print("--- the required return 0.09 -> 0.04")
    for k in ("enclosed", "funded"):
        a, b = solve(with_(BASE, **REGIMES[k])), solve(with_(BASE, **REGIMES[k], rho=0.04))
        print(f"  {k:9s} x* {a['x']:.5f} -> {b['x']:.5f}  w/r {a['v']:.5f} -> {b['v']:.5f}  w/P_s {a['omega']:.4f} ->"
              f" {b['omega']:.4f}  pi {a['pi']:.4f} -> {b['pi']:.4f}  land in hours {a['land_price_hours']:.1f} ->"
              f" {b['land_price_hours']:.1f}  1/D {1 / a['D']:.3f}")
    print("--- Proposition 2's small-eta condition (funded): lhs, rhs =", small_eta_interior(BASE))
    print("--- numbers()")
    for k, val in numbers().items():
        print(f"  {k:26s} {val:.10g}")
