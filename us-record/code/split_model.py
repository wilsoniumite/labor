# split_model.py — the pinning model with people split in two (her calls, 2026-11-05): the production and nonsupervisory
# group (AHETPI's; everyone but managers and supervisors) and managers and supervisors, each working its own block of
# tasks against machines, so each has its own task margin and its own wage. Computing (from 1970) makes machines better
# at the first group's block only.
#
# THE ECONOMY. As ../../pinning/code/pinning_model.py, with: block R (the production and nonsupervisory group's tasks, a
# share s_R = 1 - s_N of the final good's tasks) and block N (managers' and supervisors', s_N), each ordered by machine
# difficulty on [0, 1] with the same schedule; machines need comp * gamma(x) service units at block R's tasks and
# gamma(x) at block N's (comp = 1 before computing). Each type is s_i of the population and supplies the machine chain's
# labour in that proportion, so a machine costs Vm = a p_m + lambda (s_R v_R + s_N v_N) + b. At margins x_R, x_N:
#     v_R = gamma_R(x_R) p_m,  v_N = gamma_N(x_N) p_m,  p_m = (rho + delta) b / D,  D = 1 - (rho + delta)(a + lambda gbar),
#     gbar = s_R gamma_R(x_R) + s_N gamma_N(x_N),
#     p = s_R [v_R (1 - x_R) + p_m J_R(x_R)] + s_N [v_N (1 - x_N) + p_m J_N(x_N)],  P_s = p + h,
#     J = s_R J_R + s_N J_N,  Y = T / (h + b delta J / (1 - a delta)),  K = Y J / (1 - a delta),
#     n_i^D = Y s_i (1 - x_i) + s_i lambda delta K,  n_i^S = N s_i F(log(1 + v_i / P_s)).
# With comp = 1 both blocks clear at the one-type margin, and this IS the pinning model (checks/check_split_model.py).
#
# Solved as two equations in the margins' logits (scipy's hybr), from a given guess and then from the one-type solution;
# refused (pinning_model.NoEquilibrium) unless both markets clear to a relative 1e-10 with D > 0. Read as the data read
# them: pay_gap is all employees' average wage over the first group's; routine_share is that group's share of employment.

import os
import sys

import numpy as np
from scipy.optimize import root

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                                "pinning", "code"))
import pinning_model as pm  # noqa: E402


def gam(e, comp, x):
    return e.eta * comp * (e.g0 + e.g1 * x ** e.k)


def jint(e, comp, x):
    return e.eta * comp * (e.g0 * x + e.g1 * x ** (e.k + 1.0) / (e.k + 1.0))


def parts(e, s_n, comp, xr, xn):
    """Prices and quantities at margins (xr, xn)."""
    s_r = 1.0 - s_n
    gr, gn = gam(e, comp, xr), gam(e, 1.0, xn)
    jr, jn = jint(e, comp, xr), jint(e, 1.0, xn)
    cpt = e.rho + e.delta
    D = 1.0 - cpt * (e.a + e.lam * (s_r * gr + s_n * gn))
    Vm = e.b / D
    pm_ = cpt * Vm
    vr, vn = gr * pm_, gn * pm_
    p = s_r * (vr * (1.0 - xr) + pm_ * jr) + s_n * (vn * (1.0 - xn) + pm_ * jn)
    gb, sb = e.basket(p)                          # the pinning model's basket: (1, h) but in BasketEconomy
    Ps = p * gb + sb
    J = s_r * jr + s_n * jn
    Y = gb * e.T / (sb + gb * e.b * e.delta * J / (1.0 - e.a * e.delta))
    K = Y * J / (1.0 - e.a * e.delta)
    mh = e.lam * e.delta * K
    ndr, ndn = Y * s_r * (1.0 - xr) + s_r * mh, Y * s_n * (1.0 - xn) + s_n * mh
    F = lambda z: min(max(z / e.chi_max, 0.0), getattr(e, "cap", 1.0))  # noqa: E731   the pinning model's supply
    nsr, nsn = e.N * s_r * F(np.log1p(vr / Ps)), e.N * s_n * F(np.log1p(vn / Ps))
    return dict(xr=xr, xn=xn, gr=gr, gn=gn, D=D, Vm=Vm, pm=pm_, vr=vr, vn=vn, p=p, Ps=Ps, J=J, Y=Y, K=K,
                machine_hours=mh, ndr=ndr, ndn=ndn, nsr=nsr, nsn=nsn)


def solve(e, s_n, comp, guess=None):
    """The equilibrium (xr, xn), from guess (margins; the previous year's in a fit) and, failing that, from the one-type
    solution of the same economy. Every number solve(e) reports in the one-type model is computed the same way here."""
    logit = lambda x: np.log(x / (1.0 - x))  # noqa: E731
    expit = lambda u: 1.0 / (1.0 + np.exp(-u))  # noqa: E731

    def res(u):
        q = parts(e, s_n, comp, expit(u[0]), expit(u[1]))
        if not (q["D"] > 0 and np.isfinite(q["Ps"]) and q["nsr"] > 0 and q["nsn"] > 0):
            return [1e3, 1e3]
        return [q["ndr"] / q["nsr"] - 1.0, q["ndn"] / q["nsn"] - 1.0]

    def attempt(g):
        with np.errstate(all="ignore"):
            r = root(res, [logit(g[0]), logit(g[1])], method="hybr", options=dict(xtol=1e-14))
            q = parts(e, s_n, comp, expit(r.x[0]), expit(r.x[1]))
        ok = q["D"] > 0 and q["nsr"] > 0 and q["nsn"] > 0
        worst = max(abs(q["ndr"] / q["nsr"] - 1.0), abs(q["ndn"] / q["nsn"] - 1.0)) if ok else np.inf
        return q, worst

    q, worst = attempt(guess) if guess is not None else (None, np.inf)
    if not worst < 1e-10:
        x0 = pm.solve(e)["x"]                     # raises NoEquilibrium if even the one-type economy has none
        q, worst = attempt((x0, x0))
    if not worst < 1e-10:
        raise pm.NoEquilibrium(f"split economy: no equilibrium found (worst market gap {worst:.2e})")
    s_r = 1.0 - s_n
    xr, xn = q["xr"], q["xn"]
    nr, nn = q["ndr"], q["ndn"]
    final_r, final_n = q["Y"] * s_r * (1.0 - xr), q["Y"] * s_n * (1.0 - xn)
    interest = e.rho * q["Vm"] * q["K"]
    income = q["vr"] * nr + q["vn"] * nn + e.T + interest
    q.update(nr=nr, nn=nn, n=nr + nn, participation=(nr + nn) / e.N, income=income, worst_gap=worst,
             labour_share_bea=(q["vr"] * final_r + q["vn"] * final_n) / income,
             theta_V=e.lam * (s_r * q["vr"] + s_n * q["vn"]) / q["Vm"],
             pay_gap=((nr * q["vr"] + nn * q["vn"]) / (nr + nn)) / q["vr"],
             routine_share=nr / (nr + nn),
             income_identity=income / (q["Ps"] * q["Y"]) - 1.0)
    return q
