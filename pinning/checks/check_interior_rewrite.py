# check_interior.py — the battery for Appendix B and Figure 3 (2026-11-03): Lemma B.1 in its durable-machine form and its
# illustrative instance, set from U.S.-like shares. The economies are solved by code/appendix_b.py; every check
# recomputes its object from the paper's equations, written here, and prints PASS or FAIL. Economies: the printed
# instance (durable machines, a binding ceiling); Figure 3's recursive- and task-automation economies; and two test
# economies (appendix_b.TEST_ECONOMIES: the SSRN version's instance, in the flow benchmark, and a labor-heavy chain whose
# ceiling binds; the paper prints no number from them). Groups:
#   E  the equilibrium conditions, per economy: the task margin and task costs, the user-cost machine price, labor-market
#      clearing, the goods, machine and land markets, participation from utility, funding, the standing assumptions,
#      Lemma B.1's conditions (25) and its proof's monotonicity and derivative claims
#   I  income accounting, per economy: wages + rent + interest = income; the three-row network, prices on the user-cost
#      coefficients and quantities on the replacement coefficients; (4) on the replacement coefficients gives L_s and
#      B_s, with Y = T/B_s, N_a = T L_s/B_s ((11)) and P_s = w L_s + r B_s + rho V_m X/Y
#   L  an independently specified linear production program with 2,048 task cells (primitives only; nothing from the
#      solver): per economy it finds the equilibrium by itself — hours worked from participation at its own dual wage,
#      and with durable machines the charge per machine from the required return at its own dual machine cost — and its
#      output, threshold, hours and prices match the solver's within a priori discretization bounds
#   F  the flow special case: (21)-(24) at rho = 0, delta = 1 are the SSRN version's flow equations; its instance solves
#      to the numbers printed there; income without interest
#   S  the automation path of Appendix B's last paragraph (lambda = 0, gamma scaled by eta)
#   Q  every number quoted in Appendix B, the Figure 3 caption and Section 6.1, recomputed and found in paper/main.tex,
#      each anchored to the words around it; no decimal there left unchecked; the shares the instance's paragraph states;
#      Section 5's and D.3's flow-benchmark statements; the data note's cell count; the AI line in every figure caption;
#      no residue of calibration (c)'s wording; Figure 3's file
# Tolerances are set a priori: 1e-12 relative for identities; the program's from the midpoint rule's error bound and one
# cell's variation in gamma at the margin, carried through the crossing of demand and supply (group L says how).
# Run from pinning/:  python3 checks/check_interior_rewrite.py      Exit 0 only if every check passes.
#
# RE-POINTED COPY (2026-11-05) of check_interior.py for the Lucas-style rewrite, paper/main_rewrite.tex. Changed, and
# only these: ROOT is the repository (code/ and data/ are imported from it, read-only); the text read is the rewrite,
# its LaTeX comments (the build's provenance notes, which do not print) stripped unless RAW_TEX=1; the region anchors
# (Appendix B's material is now Section 3.1's flow-benchmark paragraph and Section 7, without Figure 3's caption; old
# Section 5 is Section 4.2, Corollary 1, Section 7's statics and 9.1's heterogeneity paragraph; old 6.1 is 5.1); the
# templates whose sentence survives with new words ("flow benchmark", "instance" now Table 2's parameter rows,
# "shares", "support"); Q4's anchor (the rewrite's D.3 sentence); Q8's figure path (the file the rewrite includes).
# Expected values, tolerances, computations and the set of checks are the repository's. Q3's two flow-benchmark
# sentences were replaced in the rewrite and are left as they were (unmatched), as instructed. Diagnostic lines that
# start with "   ." are not checks.

import math
import os
import re
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq, linprog
from scipy.sparse import coo_matrix

ROOT = Path(__file__).resolve().parents[1]
REWRITE = ROOT / "paper" / "main_rewrite.tex"
sys.path.insert(0, str(ROOT / "code"))
import appendix_b as B  # noqa: E402

RESULTS = []
CELLS = 2048


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok)))
    print(f"{'PASS' if ok else 'FAIL'} {name}" + (f" — {detail}" if detail else ""))


def rel(a, b):
    return abs(a - b) / max(abs(b), 1e-300)


PR = B.PRINTED
ECON = {"printed": PR, "recursive": B.scenario(PR, "recursive"), "task": B.scenario(PR, "task"), **B.TEST_ECONOMIES}
SOL = {k: B.solve(P) for k, P in ECON.items()}


# ---------------------------------------------------------------- primitives, written here from the paper's equations
def g_(P, x):
    """gamma(x) = eta (g0 + g1 x^k): the schedule, from the parameters."""
    return P["eta"] * (P["g0"] + P["g1"] * x ** P["k"])


def J_quad(P, x):
    """J(x) = the integral of gamma over [0, x], by adaptive quadrature."""
    return quad(lambda t: g_(P, t), 0.0, x, epsabs=1e-15, epsrel=1e-13, limit=200)[0]


def J_(P, x):
    """J(x) in closed form (E1 checks it against the quadrature)."""
    return P["eta"] * (P["g0"] * x + P["g1"] * x ** (P["k"] + 1.0) / (P["k"] + 1.0))


def F_(P, z):
    return min(max(z / P["chi_max"], 0.0), 1.0)


def model_at(P, x, j=None):
    """(21)-(24) at threshold x, with J(x) replaced by j if given: v, p_m, P_s, w/P_s, Y, X, final and chain hours, n_D."""
    cpt, ad = P["rho"] + P["delta"], P["a"] * P["delta"]
    j = J_(P, x) if j is None else j
    D = 1.0 - cpt * (P["a"] + P["lam"] * g_(P, x))
    pm = cpt * P["b"] / D
    v = g_(P, x) * pm
    Ps = v * (1.0 - x) + pm * j + P["h"]
    Y = P["T"] / (P["h"] + P["b"] * P["delta"] * j / (1.0 - ad))
    X = Y * j / (1.0 - ad)
    final, chain = Y * (1.0 - x), P["lam"] * P["delta"] * X
    return dict(v=v, pm=pm, Ps=Ps, w=v / Ps, Y=Y, X=X, final=final, chain=chain, nD=final + chain)


# ---------------------------------------------------------------- E: the equilibrium conditions
for r, P in ECON.items():
    q = SOL[r]
    x, v, pm, Vm, Ps, Y, X, n = (q[k] for k in ("x", "v", "pm", "Vm", "Ps", "Y", "X", "n"))
    cpt = P["rho"] + P["delta"]
    Jq = J_quad(P, x)
    check(f"E1[{r}] J(x*) by quadrature equals the closed form used by the solver (1e-10 relative)", rel(q["J"], Jq) <= 1e-10,
          f"{Jq:.12g}")
    check(f"E2[{r}] the task margin: w/p_m = gamma(x*) (1e-12)", rel(v / pm, g_(P, x)) <= 1e-12, f"gamma(x*) {g_(P, x):.6f}")
    check(f"E3[{r}] the user-cost machine price: V_m = a p_m + lambda w + b r and p_m = (rho + delta) V_m (1e-12)",
          rel(Vm, P["a"] * pm + P["lam"] * v + P["b"]) <= 1e-12 and rel(pm, cpt * Vm) <= 1e-12,
          f"V_m {Vm:.6g}, p_m {pm:.6g}")
    xs = np.linspace(0.0, 1.0, 20001)
    mc, lc = g_(P, xs) * pm, v
    below, above = xs < x - 1e-9, xs > x + 1e-9
    xc = q["x_ceiling"]
    ws = np.logspace(-6, 3, 400) * v
    closed = xs[xs >= xc] if xc < 1.0 else xs[:0]
    any_wage = all(np.all(g_(P, xx) * cpt * (P["lam"] * ws + P["b"]) / (1.0 - cpt * P["a"]) > ws) for xx in closed[::50])
    check(f"E4[{r}] task costs: at the equilibrium prices machines are cheaper on every task below x* and labor on every task "
          f"above it (20,001 tasks), and above any ceiling x_c < 1 a machine costs more than the hour at every wage tried "
          f"(400 wages, 1e-6 to 1e3 times w)",
          np.all(mc[below] < lc) and np.all(mc[above] > lc) and (xc < 1.0) == bool(len(closed)) and any_wage,
          f"x* {x:.6f}, x_c {xc:.6f}")
    p_task = v * quad(lambda t: min(1.0, g_(P, t) / g_(P, x)), 0.0, 1.0, points=[x], epsabs=1e-15, limit=200)[0]
    check(f"E5[{r}] the final good's price from its task costs, w times the integral of min(1, gamma/gamma(x*)) ((20)), "
          f"equals (22) (1e-10)", rel(p_task, q["p"]) <= 1e-10, f"p {q['p']:.6g}")
    nS = P["N"] * F_(P, math.log1p(v / Ps))
    check(f"E6[{r}] labor-market clearing: final-task plus machine-sector hours, Y(1 - x*) + lambda delta X, equal "
          f"N F(log(1 + w/P_s)) (1e-12)", rel(Y * (1 - x) + P["lam"] * P["delta"] * X, nS) <= 1e-12 and rel(n, nS) <= 1e-12,
          f"N_a {n:.6f}")
    workers = P["N"] + v * n / Ps
    provider = (P["T"] + P["rho"] * Vm * X) / Ps - P["N"]
    check(f"E7[{r}] goods, machine and land markets: X = Y J + a delta X, hY + b delta X = T, and workers' N + w N_a/P_s "
          f"baskets plus the provider's (T + rho V_m X)/P_s - N sum to Y (1e-12)",
          rel(X, Y * Jq + P["a"] * P["delta"] * X) <= 1e-10 and rel(P["h"] * Y + P["b"] * P["delta"] * X, P["T"]) <= 1e-12
          and rel(workers + provider, Y) <= 1e-12, f"provider {provider:.4f} baskets beyond support")
    chis = (np.arange(200000) + 0.5) / 200000 * P["chi_max"]
    work = np.log1p(v / Ps) - chis >= 0.0
    check(f"E8[{r}] participation from utility: on 200,000 work costs spread evenly over [0, chi_max], the share for whom "
          f"log(1 + w/P_s) - chi >= 0 is N_a/N (to the grid's 1/200,000)", abs(work.mean() - n / P["N"]) <= 1.0 / 200000,
          f"{work.mean():.6f} vs {n / P['N']:.6f}")
    check(f"E9[{r}] funded support: the provider's rent and interest cover N P_s at x*", P["T"] + P["rho"] * Vm * X >= P["N"] * Ps,
          f"N P_s / (T + rho V_m X) = {P['N'] * Ps / (P['T'] + P['rho'] * Vm * X):.4f}")
    gam_c, J_c = g_(P, xc), J_quad(P, xc)
    if xc < 1.0:
        lim = gam_c / (gam_c * (1 - xc) + J_c)
        ceiling_ok = abs(cpt * (P["a"] + P["lam"] * gam_c) - 1.0) <= 1e-12
    else:
        lim = model_at(P, 1.0)["w"]
        ceiling_ok = cpt * (P["a"] + P["lam"] * gam_c) < 1.0
    nS_c = P["N"] * F_(P, math.log1p(lim))
    ad = P["a"] * P["delta"]
    Yc = P["T"] / (P["h"] + P["b"] * P["delta"] * J_c / (1 - ad))
    nD_c = Yc * (1 - xc + P["lam"] * P["delta"] * J_c / (1 - ad))
    check(f"E10[{r}] standing assumptions: (rho + delta)(a + lambda gamma(0)) < 1, delta in (0, 1], rho >= 0, gamma' > 0 on "
          f"(0, 1]; the ceiling solves (rho + delta)(a + lambda gamma(x_c)) = 1 if x_c < 1, else no task is closed (1e-12)",
          cpt * (P["a"] + P["lam"] * g_(P, 0.0)) < 1 and 0 < P["delta"] <= 1 and P["rho"] >= 0
          and P["eta"] > 0 and P["g1"] > 0 and P["k"] > 0 and P["g0"] > 0 and ceiling_ok,
          f"(rho+delta)(a+lambda gamma(0)) {cpt * (P['a'] + P['lam'] * g_(P, 0.0)):.4f}, x_c {xc:.6f}")
    check(f"E11[{r}] Lemma B.1's conditions (25): T > N h, and n_S(x_c) > n_D(x_c), with n_S(x_c) at the limit "
          f"v/P_s -> gamma(x_c)/[gamma(x_c)(1 - x_c) + J(x_c)] when x_c < 1", P["T"] > P["N"] * P["h"] and nS_c > nD_c
          and rel(nS_c, q["nS_ceiling"]) <= 1e-10, f"T/h {P['T'] / P['h']:.4f}; n_S(x_c) {nS_c:.4f} > n_D(x_c) {nD_c:.4f}")
    grid = np.linspace(1e-9, xc * (1 - 1e-9), 20001)
    nd = np.array([model_at(P, t)["nD"] for t in grid])
    ws_ = np.array([model_at(P, t)["w"] for t in grid])
    ns = np.array([P["N"] * F_(P, math.log1p(w_)) for w_ in ws_])
    pts = np.linspace(0.5 * xc, 0.95 * xc, 100)
    hh = 1e-5

    def d4(fun, t):
        return (-fun(t + 2 * hh) + 8 * fun(t + hh) - 8 * fun(t - hh) + fun(t - 2 * hh)) / (12 * hh)
    errs = []
    for t in pts:
        a_ = model_at(P, t)
        dv = d4(lambda u: model_at(P, u)["v"], t)
        dp = d4(lambda u: model_at(P, u)["Ps"], t)        # P_s - p = h, a constant
        dvP = d4(lambda u: model_at(P, u)["w"], t)
        Jt = J_(P, t)
        errs.append(max(rel(dp, dv * (1 - t + cpt * P["lam"] * Jt / (1 - cpt * P["a"]))),
                        rel(dvP, dv * (P["h"] + cpt * P["b"] * Jt / (1 - cpt * P["a"])) / a_["Ps"] ** 2)))
    check(f"E12[{r}] the proof's claims: n_D strictly decreasing and v/P_s nondecreasing (to 4 ulps) on 20,001 points of (0, x_c), "
          f"n_D - n_S changes sign once; p'(x) and d(v/P_s)/dx match the displayed formulas at 100 points of [x_c/2, 0.95 x_c] (1e-6)",
          np.all(np.diff(nd) < 0) and np.all(np.diff(ws_) >= -4 * np.finfo(float).eps * ws_[1:])   # flat where gamma' ~ 0: ulps
          and int(np.sum(np.diff(np.sign(nd - ns)) != 0)) == 1
          and max(errs) < 1e-6, f"largest derivative gap {max(errs):.1e}")

# ---------------------------------------------------------------- I: income accounting
for r, P in ECON.items():
    q = SOL[r]
    x, v, pm, Vm, Ps, Y, X, n = (q[k] for k in ("x", "v", "pm", "Vm", "Ps", "Y", "X", "n"))
    cpt, Jx = P["rho"] + P["delta"], q["J"]
    wages, rent, interest = v * n, P["T"], P["rho"] * Vm * X
    check(f"I1[{r}] wages + rent + interest = income = P_s Y (1e-12)", rel(wages + rent + interest, Ps * Y) <= 1e-12,
          f"shares {wages / (Ps * Y):.4f} / {rent / (Ps * Y):.4f} / {interest / (Ps * Y):.4f}")
    Ap = np.array([[0, Jx, 0], [0, cpt * P["a"], 0], [0, 0, 0]])
    lp_, bp_ = np.array([1 - x, cpt * P["lam"], 0.0]), np.array([0.0, cpt * P["b"], 1.0])
    p_net = np.linalg.solve(np.eye(3) - Ap, lp_ * v + bp_ * 1.0)
    Aq = np.array([[0, Jx, 0], [0, P["a"] * P["delta"], 0], [0, 0, 0]])
    lq, bq = np.array([1 - x, P["lam"] * P["delta"], 0.0]), np.array([0.0, P["b"] * P["delta"], 1.0])
    y = np.array([Y, X, P["h"] * Y])
    f = (np.eye(3) - Aq.T) @ y
    check(f"I2[{r}] the three-row network: (3) on the user-cost coefficients prices (p, p_m, r) as the solver does; the "
          f"replacement coefficients take gross output (Y, X, hY) to final use (Y, 0, hY), with lambda'y = N_a and b'y = T; "
          f"p'f = w lambda'y + r b'y + rho V_m X (1e-12)",
          max(rel(p_net[0], q["p"]), rel(p_net[1], pm), rel(p_net[2], 1.0)) <= 1e-12 and abs(f[1]) <= 1e-12 * X
          and rel(f[0], Y) <= 1e-12 and rel(f[2], P["h"] * Y) <= 1e-12 and rel(lq @ y, n) <= 1e-12 and rel(bq @ y, P["T"]) <= 1e-12
          and rel(p_net @ f, v * (lq @ y) + bq @ y + interest) <= 1e-12)
    z = np.array([1.0, 0.0, P["h"]])
    Ls = z @ np.linalg.solve(np.eye(3) - Aq, lq)          # (4) on the replacement coefficients
    Bs = z @ np.linalg.solve(np.eye(3) - Aq, bq)
    check(f"I3[{r}] (4) on the replacement coefficients gives the printed L_s = 1 - x + lambda delta J/(1 - a delta) and "
          f"B_s = h + b delta J/(1 - a delta); Y = T/B_s, N_a = T L_s/B_s ((11)) and P_s = w L_s + r B_s + rho V_m X/Y (1e-12)",
          rel(Ls, 1 - x + P["lam"] * P["delta"] * Jx / (1 - P["a"] * P["delta"])) <= 1e-12
          and rel(Bs, P["h"] + P["b"] * P["delta"] * Jx / (1 - P["a"] * P["delta"])) <= 1e-12
          and rel(Ls, q["L_s"]) <= 1e-12 and rel(Bs, q["B_s"]) <= 1e-12
          and rel(Y, P["T"] / Bs) <= 1e-12 and rel(n, P["T"] * Ls / Bs) <= 1e-12 and rel(Ps, v * Ls + Bs + interest / Y) <= 1e-12,
          f"L_s {Ls:.6g}, B_s {Bs:.6g}")
    flow = P["rho"] == 0.0 and P["delta"] == 1.0
    check(f"I4[{r}] the two sets of coefficients coincide exactly in the flow benchmark, where P_s = w L_s + r B_s; with "
          f"durable machines the flow formula misses P_s by the interest per basket (1e-10)",
          (np.allclose(Ap, Aq, rtol=0, atol=0) and rel(Ps, v * Ls + Bs) <= 1e-12) if flow
          else (not np.allclose(Ap, Aq) and rel(Ps - (v * Ls + Bs), interest / Y) <= 1e-10),
          "flow" if flow else f"interest per basket {interest / Y:.6g}")


# ---------------------------------------------------------------- L: the linear production program
def production_program(P, hours, charge=0.0, cells=CELLS):
    """Maximize baskets, less `charge` baskets per machine held, over task assignments on `cells` equal task cells,
    without imposing a threshold. Primitives only: a basket is one unit of every task on [0, 1] and h units of land; an
    hour completes one unit of a task, a unit of machine service 1/gamma(x) units (gamma at the cell's midpoint); a stock
    of X machines supplies X units of service a period, of which a delta X rebuild the delta X machines that wear out,
    each built with a units of service, lambda hours and b land. Resources: `hours` and the land T. Variables: Y, human
    hours H_i and machine services M_i in each cell, and X. Duals are in baskets: w an hour, r land, p_m a unit of
    service."""
    n = cells
    g = g_(P, (np.arange(n) + 0.5) / n)
    iY, iX, H, M = 0, 2 * n + 1, 1 + np.arange(n), 1 + n + np.arange(n)
    rs, rh, rl = n, n + 1, n + 2
    rows = np.concatenate([np.arange(n), np.arange(n), np.arange(n), np.full(n, rs), [rs], np.full(n, rh), [rh], [rl, rl]])
    cols = np.concatenate([np.full(n, iY), H, M, M, [iX], H, [iX], [iY, iX]])
    vals = np.concatenate([np.ones(n), -n * np.ones(n), -n / g,          # Y/n units of task i, by hours or by services
                           np.ones(n), [-(1.0 - P["a"] * P["delta"])],   # services in tasks <= the stock's, net of rebuilding
                           np.ones(n) / hours, [P["lam"] * P["delta"] / hours],   # hours, scaled by their total
                           [P["h"] / P["T"], P["b"] * P["delta"] / P["T"]]])      # land, scaled by T
    A = coo_matrix((vals, (rows, cols)), shape=(n + 3, 2 * n + 2)).tocsr()
    rhs = np.zeros(n + 3)
    rhs[rh] = rhs[rl] = 1.0
    obj = np.zeros(2 * n + 2)
    obj[iY], obj[iX] = -1.0, charge
    res = linprog(obj, A_ub=A, b_ub=rhs, bounds=(0, None), method="highs-ipm",
                  options=dict(primal_feasibility_tolerance=1e-10, dual_feasibility_tolerance=1e-10))
    if not res.success:
        raise RuntimeError(res.message)
    xv, du = res.x, -res.ineqlin.marginals
    Y, X = xv[iY], xv[iX]
    share = xv[M] / g / (Y / n)                         # each cell's share done by machines
    return dict(Y=Y, X=X, threshold=float(np.sum(share) / n), final_hours=float(np.sum(xv[H])),
                chain_hours=P["lam"] * P["delta"] * X, w=du[rh] / hours, r=du[rl] / P["T"], pm=du[rs], share=share)


def program_equilibrium(P, cells=CELLS):
    """The equilibrium the program finds by itself: hours worked N_a such that its dual wage (w/P_s, in baskets) makes
    N F(log(1 + w/P_s)) = N_a (Brent's method on N_a in (0, N]); with durable machines, for each N_a, the charge per
    machine c such that c = rho (a p_m + lambda w + b r) at its dual prices (Brent's method on c), Appendix A.4's
    required return in baskets."""
    def at_hours(hours):
        if P["rho"] == 0.0:
            return production_program(P, hours, 0.0, cells), 0.0

        def gap(c):
            pr = production_program(P, hours, c, cells)
            return P["rho"] * (P["a"] * pr["pm"] + P["lam"] * pr["w"] + P["b"] * pr["r"]) - c
        hi = 1e-3
        while gap(hi) > 0.0:
            hi *= 4.0
        c = brentq(gap, 0.0, hi, xtol=1e-13, rtol=1e-12)
        return production_program(P, hours, c, cells), c
    supply_gap = lambda h_: P["N"] * F_(P, math.log1p(at_hours(h_)[0]["w"])) - h_
    na = brentq(supply_gap, 1e-6 * P["N"], P["N"], xtol=1e-12, rtol=1e-11)
    pr, c = at_hours(na)
    return dict(pr, n=na, charge=c)


def program_tolerances(P, q, cells=CELLS):
    """A priori bounds. The program is the economy with gamma replaced by its value at each cell's midpoint. At a given
    threshold its J is in error by at most E = x d^2/24 max|gamma''| + max gamma' d^2/8 (the midpoint rule over the whole
    cells below, plus the split cell; d the cell width); its margin prices a task at a midpoint within one cell of x*, so
    its w/r is off by at most the closure multiplier times max gamma' d/gamma(x*) relatively, and with durable machines
    the charge, a share rho/(rho + delta) of p_m, adds as much again: call the sum tau. Demand then shifts by at most
    |dn_D/dJ| E hours and supply by N/chi_max (w/P_s)/(1 + w/P_s) tau; the crossing of the decreasing demand and the
    increasing supply moves vertically by at most the larger shift, and horizontally by at most their sum over the sum of
    the curves' slopes at x*. A quantity Q moves by |dQ/dx| times that plus |dQ/dJ| E; a price by tau plus its slope times
    that. Every bound is doubled for second-order terms."""
    d, x = 1.0 / cells, q["x"]
    cpt, ad = P["rho"] + P["delta"], P["a"] * P["delta"]
    near = np.linspace(max(x - d, 0.0), min(x + d, 1.0), 101)
    g1 = float(np.max(P["eta"] * P["g1"] * P["k"] * near ** (P["k"] - 1.0)))
    xs = np.linspace(0.0, min(x + d, 1.0), 4001)
    g2 = float(np.max(np.abs(P["eta"] * P["g1"] * P["k"] * (P["k"] - 1.0) * xs ** max(P["k"] - 2.0, 0.0)))) if P["k"] != 1.0 else 0.0
    E = x * d * d / 24.0 * g2 + g1 * d * d / 8.0
    tau = q["multiplier"] * g1 * d / g_(P, x) * (1.0 + P["rho"] / cpt) + 1e-9
    m = model_at(P, x)
    om = m["w"]
    Bq = P["h"] + P["b"] * P["delta"] * J_(P, x) / (1 - ad)
    dnD_dJ = abs(m["Y"] * P["lam"] * P["delta"] / (1 - ad) - m["nD"] * (P["b"] * P["delta"] / (1 - ad)) / Bq)
    aD, bS = dnD_dJ * E, P["N"] / P["chi_max"] * om / (1.0 + om) * tau
    e = 1e-6

    def slope(key, along=True):
        if along:
            return (model_at(P, x + e)[key] - model_at(P, x - e)[key]) / (2 * e)
        j = J_(P, x)
        return (model_at(P, x, j + e)[key] - model_at(P, x, j - e)[key]) / (2 * e)
    nS_slope = P["N"] / P["chi_max"] * slope("w") / (1.0 + om)
    dx = 2.0 * (aD + bS) / (abs(slope("nD")) + nS_slope)
    out = dict(x=dx, n=2.0 * max(aD, bS) / q["n"])
    for key in ("Y", "X", "final", "chain"):
        val = model_at(P, x)[key]
        out[key] = 2.0 * (abs(slope(key)) * dx + abs(slope(key, along=False)) * E) / val + 1e-9 if val > 0 else 1e-9
    for key in ("w", "v", "Ps", "pm"):
        out[key] = 2.0 * (tau + abs(slope(key)) / model_at(P, x)[key] * dx)
    return out


for name, P in ECON.items():
    q = SOL[name]
    pe = program_equilibrium(P)
    tol = program_tolerances(P, q)
    s = pe["share"]
    split = np.flatnonzero((s > 1e-5) & (s < 1 - 1e-5))
    check(f"L1[{name}] the program's optimal assignment is a threshold, found and not imposed: machines take every cell "
          f"below one split cell and none above it (2,048 cells; shares to the interior-point solver's 1e-5)",
          len(split) <= 1 and np.all(np.diff(s) <= 1e-5) and s[0] > 1 - 1e-5 and s[-1] < 1e-5,
          f"split cell {split.tolist()}, threshold {pe['threshold']:.6f}")
    gaps = dict(n=rel(pe["n"], q["n"]), Y=rel(pe["Y"], q["Y"]), X=rel(pe["X"], q["X"]),
                final=rel(pe["final_hours"], q["final_hours"]),
                chain=rel(pe["chain_hours"], q["chain_hours"]) if q["chain_hours"] > 0 else abs(pe["chain_hours"]))
    check(f"L2[{name}] the program's own equilibrium — participation from its dual wage"
          + (", the charge per machine from the required return at its dual machine cost" if P["rho"] > 0 else "")
          + " — matches the solver's hours worked, output, machine stock and hours split, and its threshold the solver's x*, "
          f"within a priori discretization bounds",
          all(gaps[k] <= tol[k] for k in gaps) and abs(pe["threshold"] - q["x"]) <= tol["x"],
          ", ".join(f"{k} {gaps[k]:.1e}/{tol[k]:.0e}" for k in gaps) + f", x {abs(pe['threshold'] - q['x']):.1e}/{tol['x']:.0e}")
    Vm_dual = P["a"] * pe["pm"] + P["lam"] * pe["w"] + P["b"] * pe["r"]
    pg = dict(w=rel(pe["w"], q["real_wage"]), v=rel(pe["w"] / pe["r"], q["v"]), Ps=rel(1.0 / pe["r"], q["Ps"]),
              pm=rel(pe["pm"] / pe["r"], q["pm"]))
    check(f"L3[{name}] its dual prices are the equilibrium's within the same bounds: w/P_s (an hour's dual, in baskets), "
          f"w/r = v, P_s/r and p_m/r; and its machine service rents at the user cost, p_m = c + delta V_m with "
          f"V_m = a p_m + lambda w + b r (1e-8)",
          all(pg[k] <= tol[k] for k in pg) and rel(pe["pm"], pe["charge"] + P["delta"] * Vm_dual) <= 1e-8,
          ", ".join(f"{k} {pg[k]:.1e}/{tol[k]:.0e}" for k in pg))

# ---------------------------------------------------------------- F: the flow special case
SS = B.SSRN_INSTANCE
qp = SOL["ssrn_flow"]
# the SSRN version (paper/ssrn-7226858.pdf, Appendix B and the Figure 3 caption), as printed
RECORD = dict(x=0.86315, v=0.54344, Y=7.88061, n=1.34338, final_hours=1.07846, chain_hours=0.26492, support=5.44630)
FIG3_RECORD = {"baseline": (0.40, 0.34), "recursive": (0.37, 0.32), "task": (0.24, 0.21)}
f3p = B.figure3(SS)
check("F1 the SSRN version's instance (rho 0, delta 1; N 4, T 10, h 1, a 0.3, b 0.4, lambda 0.05, gamma 0.2 + 0.8x, chi "
      "uniform on [0, 1]) solves to its printed x*, v, Y, N_a and its split, and N P_s to five decimals, and its Figure 3 "
      "equilibria to two: 0.40/0.34, 0.37/0.32, 0.24/0.21",
      SS["rho"] == 0.0 and SS["delta"] == 1.0 and all(abs(qp[k] - v) <= 0.5e-5 for k, v in RECORD.items())
      and all(round(f3p[s]["real_wage"], 2) == w and round(f3p[s]["participation"], 2) == na for s, (w, na) in FIG3_RECORD.items()),
      ", ".join(f"{k} {qp[k]:.5f}" for k in RECORD))
f2 = []
FLOW_SETS = (SS, {**SS, "g0": 0.05, "g1": 0.95, "k": 3.0, "lam": 0.9})    # the second: convex, its ceiling binds (x_c < 1)
for P in FLOW_SETS:
    for t in np.linspace(0.01, 0.99 * B.ceiling(P), 50):
        a_ = B.at(P, t)
        gg, JJ = g_(P, t), J_quad(P, t)
        D0 = 1 - P["a"] - P["lam"] * gg
        Yp = P["T"] / (P["h"] + P["b"] * JJ / (1 - P["a"]))
        f2.append(max(rel(a_["v"], P["b"] * gg / D0), rel(a_["pm"], P["b"] / D0), rel(a_["Y"], Yp),
                      rel(a_["X"], Yp * JJ / (1 - P["a"])), rel(a_["nD"], Yp * (1 - t + P["lam"] * JJ / (1 - P["a"])))))
check("F2 at rho = 0 and delta = 1, (21)-(24) are the SSRN version's flow equations v = b gamma/(1 - a - lambda gamma), "
      "p_m = b/(1 - a - lambda gamma), Y = T/(h + bJ/(1 - a)), X = YJ/(1 - a), n_D = Y[1 - x + lambda J/(1 - a)] (1e-10, "
      "50 thresholds each on the SSRN instance and on a convex flow set whose ceiling binds)",
      max(f2) <= 1e-10 and B.ceiling(FLOW_SETS[1]) < 1.0 and len(f2) == 100, f"largest gap {max(f2):.1e} over {len(f2)} points")
check("F3 in the flow benchmark income is wages plus rent (Proposition 5's I = w N_a + r T), interest is zero, and support "
      "N P_s is paid out of the rent T",
      rel(qp["wages"] + SS["T"], qp["Ps"] * qp["Y"]) <= 1e-12 and qp["interest"] == 0.0 and qp["provider_income"] == SS["T"]
      and qp["funded"])

# ---------------------------------------------------------------- S: the automation path (Appendix B's last paragraph)
etas = np.exp(np.linspace(np.log(1e-4), 0.0, 2001))
rows = []
for e in etas:
    Pe = B.sequence(PR, e)
    q = B.solve(Pe)
    rows.append((e, q["participation"], q["v"], q["x_ceiling"], q["nS_ceiling"], q["nD_ceiling"], q["funded"], q["Ps"]))
rows = np.array(rows, dtype=float)
check("S1 along lambda = 0 with the instance's schedule scaled by eta, eta from 1e-4 to 1 (2,001 points): (25) holds "
      "throughout (x_c = 1, T > Nh, n_S(1) > n_D(1) = 0), the provider's rent and interest fund the support, and at eta = 1 "
      "the path is Figure 3's recursive-automation economy",
      np.all(rows[:, 3] == 1.0) and PR["T"] > PR["N"] * PR["h"] and np.all(rows[:, 4] > rows[:, 5]) and np.all(rows[:, 5] == 0.0)
      and np.all(rows[:, 6] == 1.0) and B.SEQUENCE == dict(lam=0.0)
      and rel(rows[-1, 1], B.figure3(PR)["recursive"]["participation"]) <= 1e-12)
cpt_ = PR["rho"] + PR["delta"]
bound = cpt_ * PR["b"] / (1.0 - cpt_ * PR["a"])
low_eta = rows[:, 0] <= 0.01
check("S2 ... 0 < v <= eta (rho + delta) b/[1 - (rho + delta) a], so v -> 0; participation falls toward zero (below its "
      "eta = 1 value for every eta <= 0.01, and under 0.002 at eta = 1e-4), with P_s >= h; relative capability "
      "gamma_eta(1)/gamma_eta(0) is 100 at every eta",
      np.all(rows[:, 2] > 0) and np.all(rows[:, 2] <= rows[:, 0] * bound * (1 + 1e-12))
      and np.all(rows[low_eta, 1] < rows[-1, 1]) and np.all(np.diff(rows[low_eta, 1]) > 0)
      and rows[0, 1] < 0.002 and np.all(rows[:, 7] >= PR["h"]) and rel(B.sequence_bound(PR), bound) <= 1e-15
      and all(abs(g_(B.sequence(PR, e), 1.0) / g_(B.sequence(PR, e), 0.0) - 100.0) < 1e-9 for e in etas[::100]),
      f"bound {bound:.5f} eta; participation {rows[-1, 1]:.4f} at eta 1, {rows[0, 1]:.6f} at eta 1e-4")

# ---------------------------------------------------------------- Q: the numbers quoted in the text
RAW = REWRITE.read_text(encoding="utf-8")


def strip_comments(s):
    """Drop LaTeX comments as TeX does: a line holding only a comment goes whole (newline included); an inline comment
    goes from its unescaped % to the end of the line. (The rewrite has no inline comments; its full-line comments are
    the build's provenance notes.)"""
    s = re.sub(r"(?m)^[ \t]*(?<!\\)%.*\n", "", s)
    return re.sub(r"(?<!\\)%.*", "", s)


TEX = RAW if os.environ.get("RAW_TEX") == "1" else strip_comments(RAW)
print(f"   . text read: {REWRITE.name}, {'raw' if TEX is RAW else 'LaTeX comments stripped'} ({len(TEX):,} characters)")


def region(start, end):
    i = TEX.index(start)
    return TEX[i:TEX.index(end, i)]


# Re-pointed regions. Appendix B's numerical economy is now Section 7 (with Figure 3 inside it, so its caption is taken
# out, as R_B never held it); its flow-benchmark sentence is now Section 3.1's paragraph after Assumption 2.
R_SEC7 = region(r"\section{A numerical economy and an automation path}", r"\section{Measurement}")
R_CAP = region(r"\caption{Labor-market clearing", r"\label{fig:3}")
R_FLOW = region(r"The last condition has two parts", r"\begin{assumption}[land]")  # review: the run-in head "Land." was dropped (R24)
R_B = R_FLOW + "\n" + R_SEC7.replace(R_CAP, "")
# Old Section 5 (Replacement meets participation) now lives in Section 4.2 (eq. (10)-(11)), Corollary 1 and its remark
# (L324 S1-2, L743), Section 7's statics (L324 S3-7) and 9.1's heterogeneity paragraph (L326).
R_S5 = "\n".join([
    region(r"\subsection{Participation and the labor market}", r"\subsection{Existence and uniqueness}"),
    region(r"\begin{corollary}[labor supply and the margin]", r"\section{Purchasing power and income}"),
    region(r"Workers occupy tasks at which their relative productivity is higher.", r"Of the two curvatures"),
    region(r"\textbf{Heterogeneity and skill premia.}", r"The model can be applied to the long record"),
])
R_61 = region(r"\subsection{What an hour's wage buys}", r"\subsection{Factor income while labor remains employed}")
R_D3 = region(r"\subsection{Feasibility: the coverage ratio}", r"\subsection{Dependence and fiscal coverage}")
WORDS = {100: "hundred"}               # n-to-one, a n times as high


def fill(template, *vals):
    """Replace <.Nf>, <d>, <pct> (a share as whole percent), <pct1> (to one decimal) and <word> placeholders in order."""
    it = iter(vals)

    def sub(m):
        v = next(it)
        spec = m.group(1)
        if spec == "word":
            return WORDS[int(round(v))]
        if spec == "pct":
            return f"{round(100 * v):d}"
        if spec == "pct1":
            return f"{100 * v:.1f}"
        if spec == "d":
            if abs(v - round(v)) > 1e-12:
                raise ValueError(f"{v} is not an integer")
            return f"{int(round(v)):d}"
        return format(v, spec)
    return re.sub(r"<(\.\d+f|d|word|pct1|pct)>", sub, template)


NUM = B.paper_numbers()
assert dict(B.SCENARIOS)["task"] == {"eta": 0.5} and dict(B.SCENARIOS)["recursive"] == {"lam": 0.0}
SEQ = B.SEQUENCE
EXPECT = {  # region -> [(label, template, values)]; every template carries the words around its numbers
    "B": [
        # re-pointed: the sentence is now Section 3.1's (after Assumption 2), in new words; same values
        ("flow benchmark", r"With $\rho=<d>$ and $\delta=<d>$ a machine lasts one period and earns no return, so machine "
                           r"services are priced at their current cost; we call this case the flow benchmark.", (0, 1)),
        # re-pointed: the parameter list is now Table 2's parameter rows, each value beside its symbol and row label (the
        # table lists a, lambda, b in that order, so the values follow it); same values and formats
        ("instance", "\n".join([
            r"workers; land & $N$; $T$ & $<d>$; $<.2f>$ \\",
            r"space per basket & $h$ & $<.4f>$ \\",
            r"machine-hours, hours, and land to build a machine & $a$, $\lambda$, $b$ & $<.1f>$, $<.1f>$, $<.1f>$ \\",
            r"depreciation; rate of time preference & $\delta$; $\rho$ & $<.2f>$; $<.2f>$ \\",
            r"relative human productivity & $\gamma(x)$ & $<.2f>+<.2f>x^{<.1f>}$ \\",
            r"cost of work & $\chi$ & uniform on $[0,<.1f>]$ \\"]),
         (PR["N"], PR["T"], PR["h"], PR["a"], PR["lam"], PR["b"], PR["delta"], PR["rho"], PR["g0"], PR["g1"], PR["k"],
          PR["chi_max"])),
        # re-pointed: "the full-chain cost of consumption" is now "the cost of a basket at final tasks" (the share the code
        # computes, shares()["labor"] = v(1 - x)/P_s); same values
        ("shares", r"labor is about half of a machine's build cost and of the cost of a basket at final tasks, machine services "
                   r"are about a fifth of a machine's build cost, and site rent is <pct1> percent of the basket; participation "
                   r"is <pct> percent.", (NUM["site"], NUM["participation"])),
        ("solution", r"The solution has $x^*\simeq<.5f>$, below the ceiling $x_c\simeq<.5f>$, $v\simeq<.5f>$, $Y\simeq<.5f>$, "
                     r"and $N_a\simeq<.5f>$: about $<.5f>$ hours at final tasks and $<.5f>$ in machine production.",
         (NUM["x_star"], NUM["x_c"], NUM["v"], NUM["Y"], NUM["N_a"], NUM["final_hours"], NUM["chain_hours"])),
        # re-pointed: "provider's" is now "owner's"; same values
        ("support", r"Support costs $NP_s\simeq<.5f>$ out of the owner's rent and interest of $<.5f>$.",
         (NUM["support"], NUM["provider_income"])),
        ("path", r"retain these parameters and set $\lambda=<d>$ and $\gamma_\eta(x)=\eta(<.2f>+<.2f>x^{<.1f>})$, with "
                 r"$0<\eta\le1$; at $\eta=1$ this is the recursive-automation economy of Figure~\ref{fig:3}.",
         (SEQ["lam"], PR["g0"], PR["g1"], PR["k"])),
        ("path bound", r"$0<v\le\eta(\rho+\delta)b/[1-(\rho+\delta)a]\to0$", ()),
        ("path ratio", r"Relative capability remains a <word> times as high at the last task as at the first.",
         (NUM["capability_ratio"],)),
        ("path participation", r"it is $<.2f>$ at $\eta=1$ and $<.2f>$ at $\eta=0.01$.", (NUM["seq_n_eta1"], NUM["seq_n_eta001"])),
    ],
    "CAP": [
        ("parameters", r"($N=<d>$, $T=<.2f>$, $h=<.4f>$, $a=<.1f>$, $b=<.1f>$, $\delta=<.2f>$, $\rho=<.2f>$, $\chi$ uniform on "
                       r"$[0,<.1f>]$)", (PR["N"], PR["T"], PR["h"], PR["a"], PR["b"], PR["delta"], PR["rho"], PR["chi_max"])),
        ("participation curve", r"The participation curve $N_a/N=\log(1+w/P_s)/<.1f>$ holds support and preferences fixed.",
         (PR["chi_max"],)),
        ("baseline", r"At baseline ($\lambda=<.1f>$, $\gamma(x)=<.2f>+<.2f>x^{<.1f>}$), the equilibrium has $w/P_s\simeq<.2f>$ "
                     r"and $N_a/N\simeq<.2f>$.",
         (PR["lam"], PR["g0"], PR["g1"], PR["k"], NUM["fig3_baseline_w"], NUM["fig3_baseline_n"])),
        ("recursive", r"Recursive automation ($\lambda=<d>$) moves it to about $<.2f>$ and $<.2f>$;",
         (0, NUM["fig3_recursive_w"], NUM["fig3_recursive_n"])),
        ("task", r"task automation, which halves $\gamma$ at every task, moves it to about $<.2f>$ and $<.2f>$.",
         (NUM["fig3_task_w"], NUM["fig3_task_n"])),
    ],
    "61": [("hundred-to-one", r"a sequence with a persistent <word>-to-one capability ratio across tasks", (NUM["capability_ratio"],))],
}
REGIONS = {"B": R_B, "CAP": R_CAP, "61": R_61}
DEC = re.compile(r"(?<![\d.])\d+\.\d+(?![\d.])(?!\s*(?:cm|pt|mm|em|ex|in\b|\\textwidth|\\linewidth))")


def blank(text):
    """Labels, references and graphics options blanked to spaces (positions kept): they are not quoted numbers."""
    return re.sub(r"\\(?:label|ref|eqref)\{[^}]*\}|\\includegraphics\[[^\]]*\]", lambda m: " " * len(m.group(0)), text)


for key, items in EXPECT.items():
    text = REGIONS[key]
    covered, missing = [], []
    for label, tmpl, vals in items:
        s = fill(tmpl, *vals)
        spans = [(m.start(), m.end()) for m in re.finditer(re.escape(s), text)]
        if len(spans) != 1:
            missing.append(f"{label}: {s!r} ({len(spans)} matches)")
        covered += spans
    loose = [m.group(0) for m in DEC.finditer(blank(text)) if not any(a <= m.start() < b for a, b in covered)]
    where = {"B": "Appendix B", "CAP": "the Figure 3 caption", "61": "Section 6.1's pointer to Appendix B"}[key]
    check(f"Q1[{key}] every quoted number in {where} is recomputed and found once as printed, with its words "
          f"({len(items)} passages)", not missing, "; ".join(missing[:4]) if missing else f"{len(covered)} matches")
    check(f"Q2[{key}] no decimal in {where} is left unchecked", not loose, f"unchecked: {loose[:10]}" if loose else "")
    if missing or loose:
        print(f"   . Q[{key}] all unmatched templates: {missing}")
        print(f"   . Q[{key}] all unchecked decimals ({len(loose)}): {loose}")
s5_body = R_S5.replace(R_CAP, "")
f3 = B.figure3(PR)
both_lower = all(f3[s]["real_wage"] < f3["baseline"]["real_wage"] and f3[s]["participation"] < f3["baseline"]["participation"]
                 for s in ("recursive", "task"))
check("Q3 Section 5 outside the caption quotes no number; it states P_s = wL_s + rB_s for the flow benchmark, pointing to "
      "Appendix B for the interest; and its claim that both automation channels lower the real wage and participation in "
      "the example holds",
      not DEC.search(blank(s5_body)) and both_lower
      and (r"In the flow benchmark, the production network prices the basket through its total human hours" in s5_body)
      and (r"so $P_s=wL_s+rB_s$. With durable machines, $P_s$ also pays interest on the machines that supply the basket "
           r"(Appendix~\ref{app:B})." in s5_body)
      and "In that example, both automation channels lower the real wage and participation together." in s5_body)
for _lbl, _ok in (("no decimal in old Section 5's text", not DEC.search(blank(s5_body))),
                  ("both channels lower w/P_s and N_a/N in the example (computed)", both_lower),
                  ("anchor 'In the flow benchmark, the production network prices the basket ...' present",
                   r"In the flow benchmark, the production network prices the basket through its total human hours" in s5_body),
                  (r"anchor 'so $P_s=wL_s+rB_s$. With durable machines, ... (Appendix~\ref{app:B}).' present",
                   r"so $P_s=wL_s+rB_s$. With durable machines, $P_s$ also pays interest on the machines that supply the basket "
                   r"(Appendix~\ref{app:B})." in s5_body),
                  ("anchor 'In that example, both automation channels lower ... together.' present",
                   "In that example, both automation channels lower the real wage and participation together." in s5_body),
                  ("(anywhere in the text) 'production network prices the basket'", "production network prices the basket" in TEX)):
    print(f"   . Q3 part: {_lbl}: {_ok}")
check("Q4 Appendix D.3 states P_s = wL_s + rB_s in the flow benchmark; the data note's linear program has the battery's "
      f"{CELLS:,} task cells",
      # re-pointed: the rewrite's D.3 sentence (on the price coefficients of Lemma 1(i))
      r"With one non-produced input, the basket's price coefficients in Lemma~\ref{lem:prices}(i) give" in R_D3
      and f"an independently specified linear production program with {CELLS:,} task cells" in TEX)
check("Q5 the shares the instance's paragraph states hold: labor 'about half' of a machine's build cost and of the "
      "full-chain cost of consumption (0.4-0.6), machine services 'about a fifth' of build cost (0.15-0.25); the site share "
      "and participation are checked as printed in Q1",
      0.4 <= NUM["theta_V"] <= 0.6 and 0.4 <= NUM["labor"] <= 0.6 and 0.15 <= NUM["machines"] <= 0.25,
      f"labor {NUM['theta_V']:.3f} of build cost, {NUM['labor']:.3f} of consumption; machine services {NUM['machines']:.3f}")
CAPTIONS = re.findall(r"\\begin\{figure\}.*?\\end\{figure\}", TEX, flags=re.S)
TAG = "Drawn by code written with Claude (Anthropic).}"
check("Q6 every figure caption (8) ends with the AI line the journal asks for in captions: 'Drawn by code written with "
      "Claude (Anthropic).'", len(CAPTIONS) == 8 and all(TAG in c for c in CAPTIONS), f"{sum(TAG in c for c in CAPTIONS)} of {len(CAPTIONS)}")
RESIDUE = ("calibrated to U.S. data", "calibrated economy", r"\theta_V", r"\sigma_V", "2.77", "0.0755", "0.0522", "5.66",
           "13.65", "WP2026-01, read from", "figures/ssrn/fig_labor_market")
found = [s for s in RESIDUE if s in TEX]
check("Q7 no residue of calibration (c)'s wording, notation or numbers, or of the SSRN image of Figure 3, in main.tex",
      not found, f"found: {found}" if found else "")
pdf = REWRITE.parent / "figures" / "fig_labor_market_clearing.pdf"     # re-pointed: the file the rewrite includes
raw = pdf.read_bytes() if pdf.exists() else b""
_repo_pdf = ROOT / "paper" / "figures" / "fig_labor_market_clearing.pdf"
print(f"   . Q8 the rewrite's Figure 3 file is byte-identical to the repository's: "
      f"{_repo_pdf.exists() and raw == _repo_pdf.read_bytes()}")
mb = re.search(rb"/MediaBox\s*\[\s*0\s+0\s+([\d.]+)\s+([\d.]+)\s*\]", raw)
check("Q8 Figure 3 is the script-built vector file: main.tex includes figures/fig_labor_market_clearing.pdf at "
      "0.88\\textwidth, the PDF is 0.88 x 16 cm wide (as Figures 1 and 2), carries no CreationDate, and embeds its fonts "
      "(FontFile2); the PNG beside it exists",
      r"\includegraphics[width=0.88\textwidth]{figures/fig_labor_market_clearing.pdf}" in TEX and mb is not None
      and abs(float(mb.group(1)) - 0.88 * 16 / 2.54 * 72) < 0.01 and b"/CreationDate" not in raw and b"/FontFile2" in raw
      and pdf.with_suffix(".png").exists(), f"width {float(mb.group(1)):.3f} pt" if mb else "no MediaBox")

n_fail = sum(not ok for _, ok in RESULTS)
print(f"\n{'ALL GREEN' if not n_fail else f'{n_fail} FAILED'} ({len(RESULTS)} checks)")
sys.exit(1 if n_fail else 0)
