# check_theory.py — the battery for Sections 3-4 and Appendix A of "Understanding the Great Stagnation".
# Every check recomputes its object from the paper's equations, written here, and prints PASS or FAIL.
# Groups:
#   A  the algebra, in sympy: the derivatives of L_s and B_s and their signs; output per hour = 1/L_s; Lemma 1's
#      elasticity; w/P_s rising in the margin (the formula of the proof); the income identity; Proposition 3's
#      elasticities and D as land's share of build cost; Lemma 2; the pay-productivity identity; Lemma 3's limit
#   X  the funded-exit case (theta = Delta = 0) against the companion paper's independent solver
#      (../pinning/code/appendix_b.py), on its printed instance and its two test economies
#   E  the equilibrium conditions from primitives, per economy: cost-minimizing assignment on a task grid, the final
#      good's price by quadrature of task costs, the user cost, the machine, land and labor markets, participation
#      counted from utility on a grid of work costs, funding, goods clearing
#   L  Lemma 1: output per hour, the signs, the elasticity against finite differences
#   P1 Proposition 1: absorption along theta and Delta
#   P2 Proposition 2: machine progress, the limits of hours and output per hour, the growth rates, interiority
#   P3 Proposition 3: the required return, enclosed and funded
#   W  Lemma 2 on random cost systems
#   C  Lemma 3 along a simulated path
#   R  random economies: Lemma 1, Proposition 1, Proposition 3(ii), the income identity
#   Q  every model number quoted in paper/main.tex, recomputed and found next to its words; no decimal in the theory
#      sections left unchecked
# Tolerances are set a priori: 1e-12 relative for identities and the cross-check; finite differences at their
# truncation order. Run from stagnation/:  ../venv/bin/python checks/check_theory.py     Exit 0 only if all pass.

import re
import sys
from pathlib import Path

import numpy as np
import sympy as sp
from scipy.integrate import quad
from tqdm.auto import tqdm

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
import model as M  # noqa: E402

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok)))
    print(f"{'PASS' if ok else 'FAIL'} {name}" + (f" — {detail}" if detail else ""))


def rel(a, b):
    return abs(a - b) / max(abs(b), 1e-300)


B0 = M.BASE
REG = {k: M.with_(B0, **kw) for k, kw in M.REGIMES.items()}
SOL = {k: M.solve(P) for k, P in REG.items()}

# ------------------------------------------------------------------------------------------------- A: the algebra
x, t, a, b, lam, d, rho, h, T, g, gp, Jx = sp.symbols("x t a b lambda delta rho h T gamma gamma_p J", real=True)
c = rho + d
G = sp.Function("gamma")
Jf = sp.Integral(G(t), (t, 0, x))
Ls_sym = 1 - x + lam * d * Jf / (1 - a * d)
Bs_sym = h + b * d * Jf / (1 - a * d)
check("A1 L_s' = -1 + lambda delta gamma/(1 - a delta)",
      sp.simplify(sp.diff(Ls_sym, x) - (-1 + lam * d * G(x) / (1 - a * d))) == 0)
check("A1 B_s' = b delta gamma/(1 - a delta)", sp.simplify(sp.diff(Bs_sym, x) - b * d * G(x) / (1 - a * d)) == 0)
# sign: (1 - a delta) - lambda delta gamma = D + rho (a + lambda gamma), so L_s' < 0 wherever D > 0
Dg = 1 - c * (a + lam * g)
check("A2 1 - a delta - lambda delta gamma = D + rho(a + lambda gamma) (L_s' < 0 where D > 0)",
      sp.expand((1 - a * d - lam * d * g) - (Dg + rho * (a + lam * g))) == 0)
# output per hour
Lq, Bq, Lp, Bp = sp.symbols("L B L_p B_p", positive=True)
check("A3 Y / n_D = (T/B_s) / (T L_s/B_s) = 1/L_s", sp.simplify((T / Bq) / (T * Lq / Bq) - 1 / Lq) == 0)
# Lemma 1's elasticity: (dlog pi/dx) / (dlog N_a/dx) with pi = 1/L, N_a = T L/B, L' < 0 < B'
u_, w_ = -Lp / Lq, Bp / Bq
eps_sym = (-Lp / Lq) / (Lp / Lq - Bp / Bq)
check("A4 dlog pi / dlog N_a = -1/(1 + psi), psi = (B'/B)/(-L'/L)",
      sp.simplify(eps_sym - (-1 / (1 + w_ / u_))) == 0)
# w/P_s rising in x: d(v/P_s)/dx = v'(x) [h + c b J/(1 - c a)] / P_s^2
A_ = a + lam * G(x)
pm_x = c * b / (1 - c * A_)
v_x = G(x) * pm_x
Ps_x = v_x * (1 - x) + pm_x * Jf + h
lhs = sp.diff(v_x / Ps_x, x)
rhs = sp.diff(v_x, x) * (h + c * b * Jf / (1 - c * a)) / Ps_x ** 2
check("A5 d(w/P_s)/dx = v'(x)[h + (rho+delta) b J/(1 - (rho+delta) a)]/P_s^2 (so w/P_s rises with x)",
      sp.simplify(sp.together(lhs - rhs)) == 0)
# the income identity: P_s Y = v n_D + T + rho V_m X
pm_s = c * b / Dg
v_s, Vm_s = g * pm_s, b / Dg
Y_s = T / (h + b * d * Jx / (1 - a * d))
X_s = Y_s * Jx / (1 - a * d)
nD_s = Y_s * (1 - x + lam * d * Jx / (1 - a * d))
Ps_s = v_s * (1 - x) + pm_s * Jx + h
check("A6 income = wages + rent + interest: P_s Y = v n_D + T + rho V_m X",
      sp.simplify(Ps_s * Y_s - (v_s * nD_s + T + rho * Vm_s * X_s)) == 0)
check("A6 the user cost: p_m = (rho + delta)(a p_m + lambda v + b) at v = gamma p_m",
      sp.simplify(pm_s - c * (a * pm_s + lam * v_s + b)) == 0)
check("A6 D = b / V_m: land's share of a machine's build cost", sp.simplify(Dg - b / Vm_s) == 0)
# Proposition 3: dlog v/dlog(rho+delta) = 1/D at a fixed margin; w/P_s rising in rho; land price in hours
cc = sp.symbols("c", positive=True)
v_c = g * cc * b / (1 - cc * (a + lam * g))
check("A7 dlog(w/r)/dlog(rho + delta) = 1/D at a fixed margin",
      sp.simplify(sp.diff(sp.log(v_c), cc) * cc - 1 / (1 - cc * (a + lam * g))) == 0)
om_c = g / (g * (1 - x) + Jx + h / (cc * b / (1 - cc * (a + lam * g))))
dom = sp.simplify(sp.diff(om_c, cc))
dom_expected = g * h / b / (g * (1 - x) + Jx + h * (1 - cc * (a + lam * g)) / (cc * b)) ** 2 / cc ** 2
check("A7 d(w/P_s)/d(rho + delta) = gamma (h/b) / [c^2 (gamma(1-x) + J + h D/(c b))^2] > 0 at a fixed margin",
      sp.simplify(dom - dom_expected) == 0)
v_rho = g * (rho + d) * b / (1 - (rho + d) * (a + lam * g))
land_hours = 1 / (rho * v_rho)
el_land = sp.simplify(sp.diff(sp.log(land_hours), rho) * rho)
check("A8 dlog(price of land in hours)/dlog rho = -1 - rho/((rho+delta) D)",
      sp.simplify(el_land - (-1 - rho / ((rho + d) * (1 - (rho + d) * (a + lam * g))))) == 0)
# Lemma 2
LC, BC, LY, BY, s_ = sp.symbols("L_C B_C L_Y B_Y s", positive=True)
wedge = sp.log(LC + s_ * BC) - sp.log(LY + s_ * BY)
betaC, betaY = s_ * BC / (LC + s_ * BC), s_ * BY / (LY + s_ * BY)
check("A9 dlog(P_C/P_Y)/dlog(r/w) = beta_C - beta_Y", sp.simplify(sp.diff(wedge, s_) * s_ - (betaC - betaY)) == 0)
w_, PC, PY, Yn, Na = sp.symbols("w P_C P_Y Y_n N_a", positive=True)
check("A10 (w/P_C)/((Y_n/P_Y)/N_a) = (w N_a/Y_n)(P_Y/P_C): real pay over productivity = labor's share x price ratio",
      sp.simplify((w_ / PC) / ((Yn / PY) / Na) - (w_ * Na / Yn) * (PY / PC)) == 0)
# Lemma 3 (the paper's normalization, C = [alpha^(1/s) c_M^((s-1)/s) + (1-alpha)^(1/s) c_S^((s-1)/s)]^(s/(s-1))):
# demand c_M/c_S = (alpha/(1-alpha)) q^(-s), so the share is alpha q^(1-s)/(alpha q^(1-s) + 1 - alpha), -> 0 for s < 1
qq, al, cs_, mm = sp.symbols("q alpha c_S m", positive=True)
ok, worst_mrs = True, 0.0
rng_a = np.random.default_rng(11)
for sig in (sp.Rational(1, 10), sp.Rational(1, 2), sp.Rational(9, 10)):
    cM_ = cs_ * al / (1 - al) * qq ** (-sig)
    share_q = qq * cM_ / (qq * cM_ + cs_)
    share_f = al * qq ** (1 - sig) / (al * qq ** (1 - sig) + 1 - al)
    ok &= sp.limit(share_f, qq, 0, "+") == 0
    # demand from the first-order conditions of C at prices (q, 1): the MRS equals the price ratio; and the share of
    # the demanded quantities is the formula. Fractional powers defeat symbolic simplification, so both are evaluated
    # at random points.
    C_ = (al ** (1 / sig) * mm ** ((sig - 1) / sig) + (1 - al) ** (1 / sig) * cs_ ** ((sig - 1) / sig)) \
        ** (sig / (sig - 1))
    mrs = (sp.diff(C_, mm) / sp.diff(C_, cs_)).subs(mm, cM_)
    f_mrs = sp.lambdify((al, qq, cs_), mrs - qq)
    f_sh = sp.lambdify((al, qq, cs_), share_q - share_f)
    for _ in range(200):
        a_, q_, c_ = rng_a.uniform(0.05, 0.95), 10 ** rng_a.uniform(-3, 2), 10 ** rng_a.uniform(-2, 2)
        worst_mrs = max(worst_mrs, abs(f_mrs(a_, q_, c_)) / q_, abs(f_sh(a_, q_, c_)))
check("A11 Lemma 3: CES demand c_M/c_S = (alpha/(1-alpha)) q^-sigma (MRS = q), share alpha q^(1-sigma)/(...) -> 0 "
      "(sigma = 0.1, 0.5, 0.9; 600 random points)", ok and worst_mrs < 1e-10, f"worst {worst_mrs:.1e}")

# ------------------------------------------------------------------- X: against the companion paper's solver
sys.path.insert(0, str(ROOT.parent / "pinning" / "code"))
try:
    import appendix_b as AB  # noqa: E402
    for name, P in (("printed", AB.PRINTED), *AB.TEST_ECONOMIES.items()):
        q_ab, q_us = AB.solve(P), M.solve({**P, "theta": 0.0, "Delta": 0.0})
        worst = max(rel(q_us[k1], q_ab[k2]) for k1, k2 in
                    (("x", "x"), ("v", "v"), ("Ps", "Ps"), ("Y", "Y"), ("X", "X"), ("n", "n"), ("pm", "pm"),
                     ("interest", "interest"), ("L_s", "L_s"), ("B_s", "B_s")))
        check(f"X1 funded exit reproduces the companion solver ({name})", worst < 1e-12, f"worst rel. gap {worst:.1e}")
except ImportError as e:
    check("X1 companion solver importable", False, str(e))


# ------------------------------------------------------------------------- E: equilibrium conditions, primitives
def equilibrium_checks(tag, P, q):
    xs, pm, vv = q["x"], q["pm"], q["v"]
    grid = np.linspace(0.0, 1.0, 4001)
    cost_m = pm * M.gamma(P, grid)
    below, above = grid < xs - 1e-9, grid > xs + 1e-9
    ok_assign = np.all(cost_m[below] < vv) and np.all(cost_m[above] > vv)
    check(f"E1 {tag}: machines cheaper below x*, labor above; indifferent at x*",
          ok_assign and rel(pm * M.gamma(P, xs), vv) < 1e-12)
    p_quad = quad(lambda s: min(vv, pm * M.gamma(P, s)), 0.0, 1.0, points=[xs], epsabs=1e-15, epsrel=1e-12,
                  limit=200)[0]
    check(f"E2 {tag}: final-good price = integral of least task costs", rel(p_quad, q["p"]) < 1e-9,
          f"{p_quad:.12g} vs {q['p']:.12g}")
    Vm = P["a"] * pm + P["lam"] * vv + P["b"]
    check(f"E3 {tag}: user cost p_m = (rho + delta) V_m", rel(pm, (P["rho"] + P["delta"]) * Vm) < 1e-12)
    J_q = quad(lambda s: M.gamma(P, s), 0.0, xs, epsabs=1e-15, epsrel=1e-13)[0]
    Y, X, n = q["Y"], q["X"], q["n"]
    check(f"E4 {tag}: machine services clear, X = Y J + a delta X", rel(X, Y * J_q + P["a"] * P["delta"] * X) < 1e-9)
    check(f"E4 {tag}: land clears, h Y + b delta X = T", rel(P["h"] * Y + P["b"] * P["delta"] * X, P["T"]) < 1e-12)
    check(f"E4 {tag}: labor clears, Y(1 - x*) + lambda delta X = n_S",
          rel(Y * (1 - xs) + P["lam"] * P["delta"] * X, M.n_S(P, xs)) < 1e-10)
    chis = (np.arange(200000) + 0.5) / 200000 * P["chi_max"]
    work = np.log1p(q["omega"] + P["Delta"]) >= chis
    n_util = P["N"] * (P["theta"] + (1 - P["theta"]) * work.mean())
    check(f"E5 {tag}: participation counted from utility on a work-cost grid", abs(n_util - n) < 2e-5 * P["N"],
          f"{n_util:.6f} vs {n:.6f}")
    check(f"E6 {tag}: support funded from rent and interest", q["funded"],
          f"{q['support']:.6f} of {q['provider_income']:.6f}")
    provider = q["provider_income"] / q["Ps"] - (1 - P["theta"]) * P["N"] - P["Delta"] * n
    consumed = (1 - P["theta"]) * P["N"] + n * (q["omega"] + P["Delta"]) + provider
    check(f"E7 {tag}: baskets consumed = baskets produced", rel(consumed, Y) < 1e-12)
    check(f"E8 {tag}: interior, 0 < x* < x_c and T > N h", 0 < xs < q["x_c"] and P["T"] > P["N"] * P["h"])


for k, P in REG.items():
    equilibrium_checks(k, P, SOL[k])

# ---------------------------------------------------------------------------------------------------- L: Lemma 1
for k, P in REG.items():
    q = SOL[k]
    grid = np.linspace(1e-6, q["x_c"] - 1e-6, 2001)
    sgn = np.all(np.array([M.L_s_prime(P, s) for s in grid]) < 0) and np.all(
        np.array([M.B_s_prime(P, s) for s in grid]) > 0)
    check(f"L1 {k}: output per hour = Y/N_a = 1/L_s(x*); L_s falls and B_s rises on (0, x_c)",
          rel(q["pi"], 1 / q["L_s"]) < 1e-12 and sgn)
    # a small supply shift: theta up (or N up when theta = 1) moves x* with technology fixed
    Pd = M.with_(P, theta=P["theta"] + 1e-6) if P["theta"] < 1 else M.with_(P, N=P["N"] * (1 + 1e-6))
    q2 = M.solve(Pd)
    fd = (np.log(q2["pi"]) - np.log(q["pi"])) / (np.log(q2["n"]) - np.log(q["n"]))
    check(f"L2 {k}: dlog pi/dlog N_a = -1/(1 + psi) against a finite supply shift",
          abs(fd - q["elasticity"]) < 1e-4 and -1 < q["elasticity"] < 0,
          f"{fd:.6f} vs {q['elasticity']:.6f}")

# ----------------------------------------------------------------------------------------------- P1: absorption
for key, vals in (("theta", (0.0, 0.1, 0.25, 0.5, 0.75, 1.0)), ("Delta", (0.0, 0.1, 0.2, 0.3))):
    qs = [M.solve(M.with_(B0, **{key: val})) for val in vals]
    dec = lambda f: all(f(qs[i + 1]) < f(qs[i]) for i in range(len(qs) - 1))  # noqa: E731
    inc = lambda f: all(f(qs[i + 1]) > f(qs[i]) for i in range(len(qs) - 1))  # noqa: E731
    check(f"P1 {key} up: x* falls, hours and output rise, output per hour, w/r and w/P_s fall",
          dec(lambda q: q["x"]) and inc(lambda q: q["n"]) and inc(lambda q: q["Y"]) and dec(lambda q: q["pi"])
          and dec(lambda q: q["v"]) and dec(lambda q: q["omega"]),
          ", ".join(f"{q['pi']:.4f}" for q in qs))
    check(f"P1 {key} up: labor's share rises in the instance (Remark d)", inc(lambda q: q["labor_share"]),
          ", ".join(f"{q['labor_share']:.4f}" for q in qs))

# ----------------------------------------------------------------------------------------- P2: machine progress
for k, P in REG.items():
    qs = M.path(P)
    check(f"P2 {k}: interior equilibrium at every eta on the path (1 to 1e-6)", len(qs) == len(M.ETAS))
    last = qs[-1]
    ninf = M.N_inf(P)
    if ninf > 0:
        # linear convergence in eta: the gap at 1e-6 is a tenth of the gap at 1e-5 (within a factor of two)
        q5 = M.solve(M.with_(P, eta=1e-5))
        gap_n6, gap_n5 = abs(last["n"] - ninf), abs(q5["n"] - ninf)
        gap_p6, gap_p5 = abs(last["pi"] - M.pi_ceiling(P)), abs(q5["pi"] - M.pi_ceiling(P))
        lin = lambda g6, g5: g6 < 1e-12 or 0.05 < g6 / g5 < 0.2  # noqa: E731  (exact up to root-finding noise)
        check(f"P2 {k}: hours -> N_inf = {ninf:.6f}, the gap shrinking in proportion to eta",
              gap_n6 < 1e-3 * ninf and lin(gap_n6, gap_n5), f"{last['n']:.8f}")
        check(f"P2 {k}: output per hour -> T/(h N_inf) = {M.pi_ceiling(P):.6f} from below, the gap in proportion to eta",
              gap_p6 < 1e-3 * M.pi_ceiling(P) and lin(gap_p6, gap_p5)
              and all(q["pi"] <= M.pi_ceiling(P) * (1 + 1e-12) for q in qs), f"{last['pi']:.8f}")
        gr = M.growth_per_log_capability(P, 1e-6)
        check(f"P2 {k}: growth of output per hour per unit of log capability -> 0", abs(gr) < 1e-3, f"{gr:.2e}")
    else:
        check(f"P2 {k}: hours -> 0", last["n"] < 1e-4, f"{last['n']:.3e}")
        gr = M.growth_per_log_capability(P, 1e-6)
        check(f"P2 {k}: growth of output per hour per unit of log capability -> 1", abs(gr - 1) < 1e-3, f"{gr:.6f}")
        lhs_, rhs_ = M.small_eta_interior(P)
        check(f"P2 {k}: the small-eta interior condition holds", lhs_ > rhs_, f"{lhs_:.5f} > {rhs_:.6f}")
    check(f"P2 {k}: output -> T/h", rel(last["Y"], P["T"] / P["h"]) < 1e-4, f"{last['Y']:.6f}")
    check(f"P2 {k}: output per hour rises along the path",
          all(qs[i + 1]["pi"] > qs[i]["pi"] for i in range(len(qs) - 1)))
    # once no task is closed to machines (D(1) > 0), w/r <= eta (rho+delta) b gamma_hat(1) / D_min, D_min = D(1)
    cpt, g1 = P["rho"] + P["delta"], P["g0"] + P["g1"]
    dmin = lambda e: 1 - cpt * (P["a"] + P["lam"] * e * g1)  # noqa: E731
    open_all = [(q, e) for q, e in zip(qs, M.ETAS) if dmin(e) > 0]
    check(f"P2 {k}: w/r <= eta (rho+delta) b gamma_hat(1)/D(1) once every task is open -> 0; w/P_s, labor's share -> 0",
          len(open_all) > 50 and all(q["v"] <= e * cpt * P["b"] * g1 / dmin(e) * (1 + 1e-12) for q, e in open_all)
          and last["omega"] < 1e-4 and last["labor_share"] < 1e-4,
          f"{len(open_all)} points open; w/P_s {last['omega']:.2e}, share {last['labor_share']:.2e}")
qs0 = M.path(M.with_(B0, lam=0.0))
check("P2 lambda = 0 (no labor in the machine chain): interior along the whole path, growth -> 1",
      len(qs0) == len(M.ETAS) and abs(M.growth_per_log_capability(M.with_(B0, lam=0.0), 1e-6) - 1) < 1e-3)

# --------------------------------------------------------------------------------------- P3: the required return
qe = M.rates(REG["enclosed"])
xs_e = np.array([q["x"] for q in qe])
check("P3 enclosed: the margin does not depend on rho", np.max(np.abs(xs_e - xs_e[0])) < 1e-12,
      f"spread {np.max(np.abs(xs_e - xs_e[0])):.1e}")
inc_r = lambda qs, f: all(f(qs[i + 1]) > f(qs[i]) for i in range(len(qs) - 1))  # noqa: E731
check("P3 enclosed: w/r and w/P_s rise with rho; output per hour and hours do not move; land in hours falls",
      inc_r(qe, lambda q: q["v"]) and inc_r(qe, lambda q: q["omega"])
      and max(abs(q["pi"] - qe[0]["pi"]) for q in qe) < 1e-12 * qe[0]["pi"]
      and inc_r(qe[::-1], lambda q: q["land_price_hours"]))
for tag, P in (("enclosed", REG["enclosed"]), ("funded", REG["funded"])):
    q = M.solve(P)
    xf = q["x"]
    e1 = M.with_(P, rho=P["rho"] * (1 + 1e-6))
    fd_v = (np.log(M.v(e1, xf)) - np.log(M.v(P, xf))) / (np.log(e1["rho"] + e1["delta"]) - np.log(P["rho"] + P["delta"]))
    check(f"P3 {tag}: dlog(w/r)/dlog(rho+delta) = 1/D at the fixed margin", abs(fd_v - 1 / q["D"]) < 1e-5,
          f"{fd_v:.6f} vs {1 / q['D']:.6f}")
    lh = lambda PP: 1 / (PP["rho"] * M.v(PP, xf))  # noqa: E731
    fd_l = (np.log(lh(e1)) - np.log(lh(P))) / (np.log(e1["rho"]) - np.log(P["rho"]))
    an_l = -1 - P["rho"] / ((P["rho"] + P["delta"]) * q["D"])
    check(f"P3 {tag}: dlog(land in hours)/dlog rho = -1 - rho/((rho+delta) D) at the fixed margin",
          abs(fd_l - an_l) < 1e-5, f"{fd_l:.6f} vs {an_l:.6f}")
qf = M.rates(REG["funded"])
check("P3 funded: as rho falls the margin rises, hours fall, output per hour rises",
      inc_r(qf[::-1], lambda q: q["x"]) and inc_r(qf, lambda q: q["n"]) and inc_r(qf[::-1], lambda q: q["pi"]))

# ------------------------------------------------------------------------------------------------- W: Lemma 2
rng = np.random.default_rng(20261116)
worst = 0.0
for _ in range(500):
    Lc, Bc, Ly, By, s0 = rng.uniform(0.05, 3.0, 5)
    f = lambda s: np.log((Lc + s * Bc) / (Ly + s * By))  # noqa: E731
    fd = (f(s0 * np.exp(1e-6)) - f(s0 * np.exp(-1e-6))) / 2e-6
    an = s0 * Bc / (Lc + s0 * Bc) - s0 * By / (Ly + s0 * By)
    worst = max(worst, abs(fd - an))
check("W1 Lemma 2 on 500 random cost systems", worst < 1e-8, f"worst gap {worst:.1e}")

# ------------------------------------------------------------------------------------------------- C: Lemma 3
ok_c, details = True, []
for sig in (0.3, 0.6, 0.9):
    al_, gq, gS = 0.6, 0.03, 0.005            # relative price of the machine-made good falls 3%/yr; c_S grows 0.5%
    ts = np.arange(0, 20001)
    q_t = np.exp(-gq * ts)                     # p_M / p_S
    cS = np.exp(gS * ts)
    cM = cS * (al_ / (1 - al_)) * q_t ** (-sig)
    share_M = al_ * q_t ** (1 - sig) / (al_ * q_t ** (1 - sig) + 1 - al_)
    excess_ok_share = np.max(np.abs(share_M - q_t * cM / (q_t * cM + cS))) < 1e-12   # share from quantities
    div = share_M[1:] * np.diff(np.log(cM)) + (1 - share_M[1:]) * np.diff(np.log(cS))
    # measured growth exceeds the bound good's by exactly s_M sigma g_q (each period, at the period's share)
    excess_ok = np.max(np.abs(div - gS - share_M[1:] * sig * gq)) < 1e-12
    rho_ces = (sig - 1) / sig
    with np.errstate(over="ignore"):
        C = (al_ ** (1 / sig) * cM ** rho_ces + (1 - al_) ** (1 / sig) * cS ** rho_ces) ** (1 / rho_ces)
    bound = (1 - al_) ** (1 / (sig - 1)) * cS
    ok_c &= (excess_ok and excess_ok_share and abs(div[-1] - gS) < 1e-6 and np.all(np.diff(share_M) < 0)
             and share_M[-1] < 1e-6
             and np.all(C[np.isfinite(C)] <= bound[np.isfinite(C)] * (1 + 1e-12)))
    details.append(f"sigma {sig}: growth {div[-1]:.6f}, share {share_M[-1]:.1e}")
check("C1 Lemma 3: measured growth = g_S + s_M sigma g_q -> g_S, s_M falls to 0, the level below "
      "(1-alpha)^(1/(sigma-1)) c_S", ok_c, "; ".join(details))

# --------------------------------------------------------------------------------------- R: random economies
def draw(r):
    P = dict(N=r.uniform(0.5, 2.0), a=r.uniform(0.0, 3.0), b=r.uniform(0.1, 1.0), lam=r.uniform(0.0, 10.0),
             g0=r.uniform(0.005, 0.2), k=r.uniform(0.5, 6.0), eta=1.0, chi_max=r.uniform(0.5, 4.0),
             rho=r.uniform(0.0, 0.1), delta=r.uniform(0.03, 0.3), theta=r.uniform(0.0, 0.9), Delta=r.uniform(0.0, 0.5))
    P["g1"] = 1.0 - P["g0"]
    P["h"] = r.uniform(0.0005, 0.01)
    P["T"] = P["N"] * P["h"] * r.uniform(1.5, 20.0)
    return P


rng = np.random.default_rng(7)
kept, bad = 0, []
for _ in tqdm(range(3000), desc="random economies", leave=False):
    P = draw(rng)
    try:
        q = M.solve(P)
    except ValueError:
        continue
    kept += 1
    # Lemma 1 against a small supply shift (N scaled up: strict at every margin; n_D does not depend on N)
    q2 = M.solve(M.with_(P, N=P["N"] * (1 + 1e-6)))
    fd = (np.log(q2["pi"]) - np.log(q["pi"])) / (np.log(q2["n"]) - np.log(q["n"]))
    if not (abs(fd - q["elasticity"]) < 1e-3 and -1 < q["elasticity"] < 0):
        bad.append(("L", P))
    # Proposition 1: a larger shift in N, and a rise in theta where it shifts supply (the supported not all working)
    prop1 = lambda q3: (q3["x"] < q["x"] and q3["n"] > q["n"] and q3["Y"] > q["Y"] and q3["pi"] < q["pi"]  # noqa
                        and q3["v"] < q["v"] and q3["omega"] < q["omega"])
    if not prop1(M.solve(M.with_(P, N=P["N"] * 1.05))):
        bad.append(("P1-N", P))
    if M.F(P, np.log1p(q["omega"] + P["Delta"])) < 1.0 and not prop1(
            M.solve(M.with_(P, theta=min(P["theta"] + 0.05, 1.0)))):
        bad.append(("P1-theta", P))
    # income identity
    if rel(q["Ps"] * q["Y"], q["income"]) > 1e-12:
        bad.append(("I", P))
    # Proposition 3(ii): enclosed, the margin does not move with rho
    try:
        e1, e2 = M.solve(M.with_(P, theta=1.0)), M.solve(M.with_(P, theta=1.0, rho=P["rho"] * 0.5))
        if not (abs(e1["x"] - e2["x"]) < 1e-12 and e2["v"] < e1["v"] and e2["omega"] < e1["omega"]):
            bad.append(("P3", P))
    except ValueError:
        pass
    if kept >= 300:
        break
check("R1 300 random interior economies: Lemma 1, Proposition 1, the income identity, Proposition 3(ii)",
      kept >= 300 and not bad, f"kept {kept}, failures {len(bad)}" + (f" first {bad[0][0]}" if bad else ""))

# ------------------------------------------------------------------------------- Q: the numbers in paper/main.tex
TEX = ROOT / "paper" / "main.tex"
NUM = M.numbers()
# (key, how it prints, words it must sit near). "pct" prints "N percent"; "abs2" prints |value| to two decimals
# (the text carries the sign in math mode).
QUOTES = [
    ("x_base", "{:.3f}", r"x\^\*"), ("n_base", "{:.2f}", r"participation"),
    ("psi_base", "{:.2f}", r"psi"), ("eps_base", "abs2", r"elasticity"),
    ("pi_base", "{:.2f}", r"output per hour"), ("pi_conditioned", "{:.2f}", r"conditioned"),
    ("n_conditioned", "{:.2f}", r"participation"), ("pi_quarter", "{:.2f}", r"quarter"),
    ("n_quarter", "{:.2f}", r"quarter"), ("pi_enclosed", "{:.2f}", r"nobody has support"),
    ("pi_drop_enclosed", "pct", r"lower than with funded exit"),
    ("ls_base", "{:.2f}", r"labor's share"), ("ls_enclosed", "{:.2f}", r"labor's share"),
    ("ceil_conditioned", "{:.1f}", r"conditioned support it levels off"),
    ("ceil_quarter", "{:.1f}", r"quarter of people unsupported"), ("ceil_enclosed", "{:.2f}", r"nobody supported"),
    ("Ninf_conditioned", "{:.2f}", r"hours tend to"),
    ("D_base", "pct", r"land is"), ("invD_base", "{:.2f}", r"elasticity in \(i\)"),
    ("invD_enclosed", "{:.2f}", r"nobody supported"),
    ("rate_v_drop_enclosed", "pct", r"lowers \$w/r\$ by"), ("rate_omega_drop_enclosed", "pct", r"w/P_s"),
    ("rate_land_mult_enclosed", "{:.1f}", r"price of land in hours of work by"),
    ("rate_v_drop_funded", "pct", r"funded exit the same fall"), ("rate_n_funded_low", "{:.2f}", r"participation"),
    ("rate_pi_rise_funded", "pct", r"output per hour rises"),
]
# the instance's parameters and the illustrations' settings (inputs, not results), and the fork, cited from the
# companion paper
ALLOWED = {"0.01", "0.0017", "1.4", "0.4", "7.3", "0.05", "0.09", "0.99", "4.4", "2.2", "0.3", "0.25", "0.04",
           "4.8"}


def fmt(key, how):
    val = NUM[key]
    if how == "pct":
        return f"{100 * val:.0f} percent"
    if how == "abs2":
        return f"{abs(val):.2f}"
    return how.format(val)


if not TEX.exists():
    check("Q0 paper/main.tex exists", False)
else:
    tex = TEX.read_text()
    regions = re.findall(r"% THEORY-NUMBERS-BEGIN(.*?)% THEORY-NUMBERS-END", tex, flags=re.S)
    body = "\n".join(regions)
    check("Q0 the theory sections are marked for the number audit (two regions: Sections 3-4, the appendices)",
          len(regions) == 2 and len(body) > 10000, f"{len(regions)} regions, {len(body)} characters")
    found_strings = set()
    for key, how, anchor in QUOTES:
        s = fmt(key, how)
        hits = [m.start() for m in re.finditer(r"(?<![\d.])" + re.escape(s) + r"(?![\d])", body)]
        near = any(re.search(anchor, body[max(0, p - 300):p + 300]) for p in hits)
        check(f"Q1 {key} = '{s}' printed near /{anchor}/", bool(hits) and near, f"{len(hits)} hit(s)")
        found_strings.add(s.split(" ")[0])
    prose = re.sub(r"\\(label|ref|eqref|input)\{[^}]*\}|\\includegraphics\[[^\]]*\]\{[^}]*\}", "", body)
    decimals = set(re.findall(r"(?<![\w.])\d+\.\d+", prose))
    unchecked = sorted(dd for dd in decimals if dd not in found_strings and dd not in ALLOWED)
    check("Q2 no decimal in the theory sections left unchecked", not unchecked, ", ".join(unchecked[:12]))
    # the introduction's eras, from code/eras.py (FRED OPHNFB, the cached vintage)
    import eras as E  # noqa: E402
    ok_e, det = True, []
    for (y0, y1), gr in E.eras().items():
        if y1 == 2025:
            continue
        s = f"{gr:.1f} percent"
        hit = [m.start() for m in re.finditer(re.escape(s), tex)]
        ok_e &= any(str(y0) in tex[p:p + 80] or str(y0) in tex[max(0, p - 120):p] for p in hit)
        det.append(f"{y0}-{y1} {s}")
    check("Q3 the introduction's eras of output per hour match code/eras.py", ok_e, "; ".join(det))
    # Table B.1 is the model's, as written by code/table_regimes.py
    import table_regimes as TR  # noqa: E402
    tab = ROOT / "paper" / "tables" / "tab_regimes.tex"
    check("Q4 Table B.1 (paper/tables/tab_regimes.tex) equals a fresh rebuild from the model",
          tab.exists() and tab.read_text() == TR.table_text())
    for fig in ("fig_paths.pdf", "fig_rates.pdf"):
        check(f"Q5 {fig} exists and is included", (ROOT / "paper" / "figures" / fig).exists()
              and f"figures/{fig}" in tex)
    caps = re.findall(r"\\caption\{(.*?)\}\s*\\label\{fig", tex, flags=re.S)
    check("Q5 every figure caption ends with the AI line", len(caps) == 2 and all(
        c.rstrip().endswith("Drawn by code written with Claude (Anthropic).") for c in caps))

n_fail = sum(1 for _, okk in RESULTS if not okk)
print(f"\n{len(RESULTS) - n_fail}/{len(RESULTS)} checks passed")
sys.exit(1 if n_fail else 0)
