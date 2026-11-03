# check_cost_system.py — the cost system of Sections 3, 4 and 6 and Appendices A and C, checked numerically (2026-11-03;
# the data note names this file). On random productive networks and on Appendix B's economies (the printed instance, with
# durable machines, and code/appendix_b.py's TEST_ECONOMIES: the SSRN version's flow instance and a binding ceiling):
#   N  network prices p = (I - A)^(-1)(lambda w + B r) against production rounds, p = c + Ac + A^2 c + ..., truncated
#      independently of the inverse (when a round adds less than 1e-16 of the price); total requirements likewise ((4))
#   F  factor-income cancellation (Appendix C): p'f = w lambda'y + r'B'y for f = (I - A')y; with durable machines the
#      cancellation leaves wages, rent and interest
#   M  the feasible-method bounds of Section 6 ((12), (13), (19)): with a menu of methods per good, the cost-minimizing
#      selection prices every good at most at the all-human chain's w Lbar + r bbar and at least at its own rent bill
#      r btilde, every unused method costs at least the price, and the purchasing-power bounds hold; the task-level price
#      (20) and its flat case
#   P  participation from utility (Proposition 3, (9), (10), Appendix D.1): each person's choice from u = log(1 + w n/P_s)
#      - chi n against the reservation wage, the aggregate N F(log(1 + w/P_s)) against a count, conditional payments
#   C  Appendix B's three-row system, per economy: production rounds price it on the user-cost coefficients; factor income
#      on the replacement coefficients leaves wages, rent and interest; the feasible-method bounds and participation from
#      utility at its equilibrium
# Tolerances: 1e-12 relative for identities; counts to their grid. Every random draw is seeded.
# Run from pinning/:  python3 checks/check_cost_system.py      Exit 0 only if every check passes.

import math
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import quad

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
import appendix_b as B  # noqa: E402

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok)))
    print(f"{'PASS' if ok else 'FAIL'} {name}" + (f" — {detail}" if detail else ""))


def rel(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    return float(np.max(np.abs(a - b) / np.maximum(np.abs(b), 1e-300)))


def rounds(A, c, tol=1e-16, cap=100000):
    """Production rounds: c + Ac + A^2 c + ..., stopped when a round adds less than tol of the running total."""
    total, term, t = c.copy(), c.copy(), 0
    while t < cap:
        term = A @ term
        total = total + term
        t += 1
        if np.max(np.abs(term)) <= tol * np.max(np.abs(total)):
            return total, t
    raise RuntimeError("production rounds did not settle")


def network(rng, n=None, K=None, radius=None):
    """A random productive network: A >= 0 with spectral radius `radius` < 1, labor lambda >= 0, non-produced inputs B >= 0."""
    n = n or int(rng.integers(2, 41))
    K = K or int(rng.integers(1, 5))
    A = rng.uniform(0, 1, (n, n)) * (rng.uniform(0, 1, (n, n)) < rng.uniform(0.1, 0.8))
    rad = max(abs(np.linalg.eigvals(A)))
    A = A * ((radius or rng.uniform(0.1, 0.97)) / rad) if rad > 0 else A
    lam = rng.uniform(0, 2, n) * (rng.uniform(0, 1, n) < 0.85)
    Bm = rng.uniform(0, 1, (n, K)) * (rng.uniform(0, 1, (n, K)) < 0.6)
    lam[lam.sum() == 0] = 1.0
    return A, lam, Bm


rng = np.random.default_rng(20261103)
NETS = [network(rng) for _ in range(200)]

# ---------------------------------------------------------------- N: network prices against production rounds
gapN, gapT, maxr, nrounds = 0.0, 0.0, 0.0, []
for A, lam, Bm in NETS:
    n, K = Bm.shape
    w, r = rng.uniform(0.1, 5), rng.uniform(0.1, 3, K)
    c = lam * w + Bm @ r
    p_inv = np.linalg.solve(np.eye(n) - A, c)
    p_rnd, t = rounds(A, c)
    lt, _ = rounds(A, lam)
    Bt = np.column_stack([rounds(A, Bm[:, j])[0] if Bm[:, j].any() else np.zeros(n) for j in range(K)])
    gapN = max(gapN, rel(p_rnd, p_inv))
    gapT = max(gapT, rel(lt * w + Bt @ r, p_inv))
    maxr = max(maxr, max(abs(np.linalg.eigvals(A))))
    nrounds.append(t)
check("N1 on 200 random productive networks (2-40 goods, 1-4 non-produced inputs, spectral radius up to 0.97), prices from "
      "independently truncated production rounds equal (I - A)^(-1)(lambda w + B r) (1e-12)", gapN <= 1e-12,
      f"max relative gap {gapN:.1e}; rounds {min(nrounds)}-{max(nrounds)}")
check("N2 ... and total requirements from rounds, lambdatilde = sum A^k lambda and Btilde = sum A^k B, price every good: "
      "p = w lambdatilde + Btilde r ((4), (12)) (1e-12)", gapT <= 1e-12, f"max relative gap {gapT:.1e}")
# a directly rented non-produced service as a pass-through row: p_h = r, b_h = 1, no other inputs (Section 3.2)
A, lam, Bm = NETS[0]
n = len(lam)
Ah = np.zeros((n + 1, n + 1))
Ah[:n, :n] = A
lamh, bh = np.r_[lam, 0.0], np.r_[Bm[:, 0], 1.0]
ph = np.linalg.solve(np.eye(n + 1) - Ah, lamh * 1.3 + bh * 0.7)
check("N3 a directly rented non-produced service entered as a pass-through row (p_h = r, b_h = 1) is priced at the rent",
      abs(ph[-1] - 0.7) <= 1e-15)

# ---------------------------------------------------------------- F: factor-income cancellation
gapF, gapH = 0.0, 0.0
for A, lam, Bm in NETS:
    n, K = Bm.shape
    w, r = rng.uniform(0.1, 5), rng.uniform(0.1, 3, K)
    p = np.linalg.solve(np.eye(n) - A, lam * w + Bm @ r)
    f = rng.uniform(0, 2, n) * (rng.uniform(0, 1, n) < 0.7)
    y = np.linalg.solve(np.eye(n) - A.T, f)
    I_ = p @ f
    gapF = max(gapF, abs(I_ - (w * (lam @ y) + r @ (Bm.T @ y))) / I_ if I_ > 0 else 0.0)
    gapH = max(gapH, abs(p @ y - p @ (A.T @ y) - I_) / max(I_, 1e-300) if I_ > 0 else 0.0)
check("F1 on the same networks, final expenditure p'f with f = (I - A')y equals w lambda'y + r'B'y: intermediate payments "
      "cancel and every hour and non-produced service is paid once (Appendix C; 1e-12)", gapF <= 1e-12 and gapH <= 1e-12,
      f"max relative gap {gapF:.1e}")

# ---------------------------------------------------------------- M: the feasible-method bounds of Section 6
viol = dict(upper=0.0, lower=0.0, unused=0.0, pp_low=0.0, pp_high=0.0, ident=0.0)
switched = 0
for k in range(150):
    n = int(rng.integers(2, 25))
    w, r = rng.uniform(0.1, 5), rng.uniform(0.1, 3)
    menus = []                        # per good: list of (row of A, lambda, b)
    AH, lamH, bH = network(rng, n=n, K=1, radius=rng.uniform(0.05, 0.6))   # the all-human chain: every good by hand
    lamH = lamH + rng.uniform(0.05, 1, n)
    A0, lam0, b0 = network(rng, n=n, K=1)
    A1, lam1, b1 = network(rng, n=n, K=1)
    lam0, lam1 = lam0 + rng.uniform(0.01, 0.5, n), lam1 + rng.uniform(0.01, 0.5, n)   # every method uses some labor: p > 0
    for i in range(n):
        menus.append([(A0[i], lam0[i], b0[i, 0]), (A1[i], lam1[i], b1[i, 0]), (AH[i], lamH[i], bH[i, 0])])
    choice = np.zeros(n, int)
    for _ in range(200):              # policy iteration: price the selected rows, let each good take its cheapest method
        As = np.array([menus[i][choice[i]][0] for i in range(n)])
        ls = np.array([menus[i][choice[i]][1] for i in range(n)])
        bs = np.array([menus[i][choice[i]][2] for i in range(n)])
        if max(abs(np.linalg.eigvals(As))) >= 1:
            choice = np.full(n, 2)
            continue
        p = np.linalg.solve(np.eye(n) - As, ls * w + bs * r)
        cost = np.array([[m[0] @ p + m[1] * w + m[2] * r for m in menus[i]] for i in range(n)])
        new = np.where(cost[np.arange(n), choice] <= cost.min(axis=1) * (1 + 1e-13), choice, cost.argmin(axis=1))
        if np.array_equal(new, choice):
            break
        choice = new
    switched += int(np.any(choice != 0))
    Lbar = np.linalg.solve(np.eye(n) - AH, lamH)
    bbar = np.linalg.solve(np.eye(n) - AH, bH[:, 0])
    lt = np.linalg.solve(np.eye(n) - As, ls)
    bt = np.linalg.solve(np.eye(n) - As, bs)
    if not np.all(p > 0):
        viol["nonpositive"] = viol.get("nonpositive", 0) + 1
        continue
    pos = bt > 0
    new_v = dict(upper=np.max((p - (w * Lbar + r * bbar)) / p), lower=np.max((r * bt - p) / p),
                 unused=np.max((p[:, None] - cost) / p[:, None]), ident=rel(w / p, 1.0 / (lt + bt * r / w)),
                 pp_low=np.max((1.0 / (Lbar + bbar * r / w) - w / p) / (w / p)),
                 pp_high=np.max((w / p[pos] - (w / r) / bt[pos]) / (w / p[pos])) if pos.any() else -np.inf)
    for key, val in new_v.items():
        if not np.isfinite(val) and not (key == "pp_high" and val == -np.inf):
            viol["nonfinite"] = viol.get("nonfinite", 0) + 1
        viol[key] = max(viol[key], float(val))
tolm = 1e-12
check("M1 on 150 random economies with three methods per good (two machine-using, one all-human), the cost-minimizing "
      "selection prices every good between its rent bill and the all-human chain: r btilde_i <= p_i <= w Lbar_i + r bbar_i "
      "((19)), and every unused method costs at least the price (Appendix A.1)",
      viol["upper"] <= tolm and viol["lower"] <= tolm and viol["unused"] <= tolm and not viol.get("nonpositive")
      and not viol.get("nonfinite"),
      f"worst: upper {viol['upper']:.1e}, lower {viol['lower']:.1e}, unused {viol['unused']:.1e}; selections that left the first "
      f"method {switched}/150")
check("M2 ... w/p_i = 1/(lambdatilde_i + btilde_i r/w) ((12)), and the purchasing-power bounds "
      "1/(Lbar_i + bbar_i r/w) <= w/p_i <= (w/r)/btilde_i ((13)) (1e-12)",
      viol["ident"] <= tolm and viol["pp_low"] <= tolm and viol["pp_high"] <= tolm,
      f"worst: identity {viol['ident']:.1e}, lower {viol['pp_low']:.1e}, upper {viol['pp_high']:.1e}")
gap20, gapflat = 0.0, 0.0
for k in range(100):                  # the task-level price (20): a task list with human-required tasks, an active margin
    m = 257
    gL = rng.lognormal(0, 0.5, m)
    gam = rng.lognormal(0, 0.8, m)
    gam[rng.uniform(0, 1, m) < 0.1] = np.inf                       # human-required: gamma_M = 0
    gstar, w, r, bdir = rng.uniform(0.2, 1.5), rng.uniform(0.3, 3), rng.uniform(0.2, 2), rng.uniform(0, 1)
    pm = w / gstar                                                  # the margin: w = p_m gamma(x*)
    gM = np.where(np.isfinite(gam), gL / np.where(np.isfinite(gam), gam, 1.0), 0.0)
    mach = np.full(m, np.inf)
    np.divide(pm, gM, out=mach, where=gM > 0)
    price = r * bdir + np.mean(np.minimum(w / gL, mach))           # each task at its cheaper input, tasks in equal amounts
    eff = np.mean(np.minimum(1.0, gam / gstar) / gL)
    Lbar = np.mean(1.0 / gL)
    gap20 = max(gap20, abs(price - (r * bdir + w * eff)) / price, max(price - (w * Lbar + r * bdir), 0.0) / price,
                max(1.0 / (Lbar + bdir * r / w) - w / price, 0.0) / (w / price))
    flat = np.full(m, gstar)                                         # uniform relative capability: every task at parity
    pflat = r * bdir + np.mean(np.minimum(w / gL, pm / (gL / flat)))
    gapflat = max(gapflat, abs(pflat - (w * Lbar + r * bdir)) / pflat)
check("M3 the task-level price (20): with tasks at their cheaper input and an active margin w = p_m gamma(x*), "
      "p = r b + w mean(min(1, gamma/gamma(x*))/gamma_L), at most w Lbar + r b, so w/p >= 1/(Lbar + b r/w); with uniform "
      "capability p = w Lbar + r b exactly (100 task lists of 257 tasks, a tenth human-required; 1e-12)",
      gap20 <= 1e-12 and gapflat <= 1e-12, f"worst {gap20:.1e}, flat {gapflat:.1e}")

# ---------------------------------------------------------------- P: participation from utility
Nd = 200000
w = rng.lognormal(0, 1, Nd)
Ps = rng.lognormal(0, 1, Nd)
chi = rng.exponential(1.0, Nd)
by_u = np.log1p(w / Ps) - chi >= 0.0                                 # u_1 >= u_0 = log(1) - 0
by_s = w >= np.expm1(chi) * Ps                                       # (9): w >= s = (e^chi - 1) P_s
tie = np.abs(np.log1p(w / Ps) - chi) < 1e-12
scale = rng.lognormal(0, 2, Nd)
by_scaled = np.log1p((w * scale) / (Ps * scale)) - chi >= 0.0
check("P1 200,000 people choose by comparing log(1 + w/P_s) - chi with exit's 0, exactly as the reservation wage "
      "s = (e^chi - 1) P_s says (Proposition 3, (9)), and rescaling w and P_s together changes no choice",
      np.array_equal(by_u[~tie], by_s[~tie]) and np.array_equal(by_u, by_scaled), f"{int(tie.sum())} ties set aside")
Mq = 1_000_000
agg = []
for name, Finv, Fc, ratio in (("uniform on [0, 2.2]", lambda u: 2.2 * u, lambda z: min(z / 2.2, 1.0), 1.7),
                              ("exponential, mean 0.8", lambda u: -0.8 * np.log1p(-u), lambda z: 1 - math.exp(-z / 0.8), 0.9),
                              ("uniform on [0, 1]", lambda u: u, lambda z: min(z, 1.0), 3.5)):
    chis = Finv((np.arange(Mq) + 0.5) / Mq)                          # a quantile grid of work costs
    share = np.mean(np.log1p(ratio) - chis >= 0.0)
    agg.append((name, share, Fc(math.log1p(ratio))))
check("P2 the aggregate N_a/N = F(log(1 + w/P_s)) ((10)) equals the share of a 1,000,000-point quantile grid of work costs "
      "for whom working beats exit, for three distributions F (to the grid's 1e-6)",
      all(abs(s - f_) <= 1.0 / Mq for _, s, f_ in agg), "; ".join(f"{n_}: {s:.6f} vs {f_:.6f}" for n_, s, f_ in agg))
mw, me = rng.uniform(0, 2, Nd), rng.uniform(0, 2, Nd)
lhs = np.log((Ps + w + mw) / (Ps + me)) >= chi
rhs = w >= np.expm1(chi) * (Ps + me) - (mw - me)
tie2 = np.abs(np.log((Ps + w + mw) / (Ps + me)) - chi) < 1e-12
d = rng.uniform(0, 2, Nd)
unc = np.log((Ps + w + d) / (Ps + d)) >= chi
unc_s = w >= np.expm1(chi) * (Ps + d)
tie3 = np.abs(np.log((Ps + w + d) / (Ps + d)) - chi) < 1e-12
check("P3 with payments (m_w, m_e) in work and exit, the utility comparison is w >= (e^chi - 1)(P_s + m_e) - Delta ((27)); "
      "an unconditional payment d gives the reservation wage (e^chi - 1)(P_s + d) (Appendix D.1)",
      np.array_equal(lhs[~tie2], rhs[~tie2]) and np.array_equal(unc[~tie3], unc_s[~tie3]))

# ---------------------------------------------------------------- C: Appendix B's economies, flow and durable
for name, P in (("printed", B.PRINTED), *B.TEST_ECONOMIES.items()):
    q = B.solve(P)
    x, v, pm, Vm, Ps_, Y, X, n_ = (q[k] for k in ("x", "v", "pm", "Vm", "Ps", "Y", "X", "n"))
    cpt, Jx = P["rho"] + P["delta"], q["J"]
    Ap = np.array([[0, Jx, 0], [0, cpt * P["a"], 0], [0, 0, 0]])
    lp_, bp_ = np.array([1 - x, cpt * P["lam"], 0.0]), np.array([0.0, cpt * P["b"], 1.0])
    p_r, t = rounds(Ap, lp_ * v + bp_)
    lt, _ = rounds(Ap, lp_)
    bt, _ = rounds(Ap, bp_)
    z = np.array([1.0, 0.0, P["h"]])
    check(f"C1[{name}] Appendix B's three-row system on the user-cost coefficients: production rounds price the final good, "
          f"machine services and space as the solver does, and the basket at P_s = w z'lambdatilde + r z'btilde (1e-12)",
          rel(p_r, [q["p"], pm, 1.0]) <= 1e-12 and rel(z @ p_r, Ps_) <= 1e-12 and rel(v * (z @ lt) + z @ bt, Ps_) <= 1e-12,
          f"{t} rounds")
    Aq = np.array([[0, Jx, 0], [0, P["a"] * P["delta"], 0], [0, 0, 0]])
    lq, bq = np.array([1 - x, P["lam"] * P["delta"], 0.0]), np.array([0.0, P["b"] * P["delta"], 1.0])
    y = np.array([Y, X, P["h"] * Y])
    f = (np.eye(3) - Aq.T) @ y
    interest = P["rho"] * Vm * X
    check(f"C2[{name}] factor-income cancellation with durable machines: p'f = w lambda'y + r b'y + rho V_m X, the quantity "
          f"coefficients (replacement at delta) giving lambda'y = N_a and b'y = T (1e-12)",
          rel(p_r @ f, v * (lq @ y) + bq @ y + interest) <= 1e-12 and rel(lq @ y, n_) <= 1e-12 and rel(bq @ y, P["T"]) <= 1e-12,
          f"interest {interest / (p_r @ f):.4f} of income")
    # the all-human method: every task by hand, Lbar = integral of 1/gamma_L = 1, no land in the final good
    Lbar = quad(lambda s: 1.0, 0.0, 1.0)[0]
    check(f"C3[{name}] the feasible-method bounds: the final good costs at most its all-human chain (p <= w Lbar, Lbar = 1), "
          f"the basket at most w + r h and at least its rent bill r z'btilde, so 1/(1 + h r/w) <= w/P_s <= (w/r)/z'btilde",
          q["p"] <= v * Lbar and Ps_ <= v * Lbar + P["h"] and Ps_ >= z @ bt and 1.0 / (1.0 + P["h"] / v) <= v / Ps_ <= v / (z @ bt),
          f"w/P_s {v / Ps_:.4f} in [{1.0 / (1.0 + P['h'] / v):.4f}, {v / (z @ bt):.4f}]")
    chis = (np.arange(Mq) + 0.5) / Mq * P["chi_max"]
    share = np.mean(np.log1p(v / Ps_) - chis >= 0.0)
    check(f"C4[{name}] participation from utility at the equilibrium: the share of a 1,000,000-point grid of work costs on "
          f"[0, chi_max] for whom log(1 + w/P_s) - chi >= 0 is N_a/N (to 1e-6)", abs(share - n_ / P["N"]) <= 1.0 / Mq,
          f"{share:.6f} vs {n_ / P['N']:.6f}")

n_fail = sum(not ok for _, ok in RESULTS)
print(f"\n{'ALL GREEN' if not n_fail else f'{n_fail} FAILED'} ({len(RESULTS)} checks)")
sys.exit(1 if n_fail else 0)
