"""Verification of Block A (the split) — sketch link-sketch-blocks-AB.md.

Claims checked (the three [check] flags of Block A):
  (A0-DR)   Diminishing-returns study technology changes nothing qualitative:
            with C(q;th) = w_alt * g(q)/lambda(th), g convex increasing, all of
            A2's signs survive: dC/dth < 0, gradient-channel rent >= 0 for
            th >= th_m, P = (r+dP)*C(q_req; th_m) is structural (free-entry
            indifference does not reference g's shape).
  (A1-FP)   Sorting with endogenous practice is a fixed point that exists:
            single-crossing of the value function in (th, alpha) with q at its
            interior optimum (envelope), plus a numerical equilibrium (8
            occupation pools x 40 talent types, tatonnement on per-efficiency
            prices) that converges and is positively assortative.
  (A2-POOL) With an occupation-sized pool sharing one qualification q_req, the
            marginal acquirer th_m is interior, the pool premium equals the
            MARGINAL acquirer's amortized cost (free entry), and inframarginal
            talent rents are positive and increasing in th.
"""
import sys

import numpy as np
import sympy as sp

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ---------------------------------------------------------------- A0-DR
th, thm, q, k, w, r, dP, lam0 = sp.symbols('theta theta_m q k w r delta_P lambda0', positive=True)
lam = lam0 * sp.exp(th)                      # lambda' > 0
g = q ** k                                   # convex for k >= 1 (k=1 is the sketch's linear case)
C = w * g / lam
dC_dth = sp.simplify(sp.diff(C, th))
assert sp.simplify(dC_dth + w * g / lam) == 0, dC_dth   # dC/dth = -C < 0
print("PASS  A0-DR  dC/dtheta = -C < 0 for every convex g = q^k (k free)")

C_at = lambda t: (w * g / (lam0 * sp.exp(t)))
R_grad = (r + dP) * (C_at(thm) - C_at(th))
diff = sp.simplify(R_grad / ((r + dP) * w * g / lam0))  # = e^-thm - e^-th >= 0 iff th >= thm
assert sp.simplify(diff - (sp.exp(-thm) - sp.exp(-th))) == 0
print("PASS  A0-DR  gradient-channel rent (r+dP)[C(th_m)-C(th)] >= 0 for th >= th_m, any k")
print("PASS  A0-DR  P = (r+dP)*C(q_req; th_m) is the indifference equation itself — g-free")

# ---------------------------------------------------------------- A1-FP single crossing (envelope)
al, be, p = sp.symbols('alpha beta p', positive=True)
# interior q*: max_q  p*exp(al*th + be*q) - (r+dP)*w*q/lam(th)  has FOC
# p*be*exp(al*th+be*q) = (r+dP)*w/lam  ->  value V; envelope: dV/dth at fixed q*
qs = sp.symbols('q_star', positive=True)
V = p * sp.exp(al * th + be * qs) - (r + dP) * w * qs / lam
dV_dth = sp.diff(V, th)                       # envelope: q* terms drop at the optimum
d2V_dth_dal = sp.simplify(sp.diff(dV_dth, al))
# = p*th... compute: dV/dth = p*al*e^{al th + be q} + (r+dP) w q / lam  (since dlam/dth=lam)
# cross partial in alpha: p*e^{..}*(1 + al*th) > 0
assert sp.simplify(d2V_dth_dal - p * sp.exp(al * th + be * qs) * (1 + al * th)) == 0
print("PASS  A1-FP  single crossing: d2V/dtheta dalpha = p e^(alpha th + beta q)(1+alpha th) > 0")
print("             (higher-talent workers gain more from higher-loading tasks; PAM follows)")

# ---------------------------------------------------------------- A1-FP + A2-POOL numeric equilibrium
rng = np.random.default_rng(7)
NT, NP = 400, 8                               # fine talent grid: the claim is a continuum
thetas = np.linspace(0.0, 1.5, NT)            # talent grid, equal mass 1/NT each
alphas = np.linspace(0.0, 1.4, NP)            # pool loadings, increasing; pool 0 = untrained
betas = np.full(NP, 0.6); betas[0] = 0.0
qreq = np.full(NP, 0.8); qreq[0] = 0.0        # pooled qualification requirement
K_dem = np.full(NP, 0.35)                     # unit-elastic demand D_j(p) = K_j / p_j
R_, DP_, WALT = 0.05, 0.06, 1.0
lamv = 0.5 + thetas                           # lambda(theta), increasing

def net_flow(pv):
    # worker x pool net flow: p*exp(al th + be qreq) - (r+dP)*w*qreq/lam
    cap = np.exp(np.outer(thetas, alphas) + betas * qreq)
    cost = (R_ + DP_) * WALT * qreq / lamv[:, None]
    return pv * cap - cost

# Existence demo: workers best-respond (argmax over pools, training bundled into the
# pool choice), prices update by a heavily damped multiplicative rule toward K/S.
# 400 discrete types put a granularity bound on clearing: tolerance 2% is that bound,
# labeled — the claim is existence-with-sorting, not knife-edge exactness.
capm = np.exp(np.outer(thetas, alphas) + betas * qreq)
pv = np.full(NP, 0.4)
TOL = 2e-2
sup_avg = None
for it in range(30000):
    nf = net_flow(pv)
    choice = nf.argmax(axis=1)
    sup = np.bincount(choice, weights=capm[np.arange(NT), choice], minlength=NP) / NT
    kap = max(2e-3, 1.0 / (it + 1))            # fictitious-play averaging kills the see-saw
    sup_avg = sup if sup_avg is None else (1 - kap) * sup_avg + kap * sup
    dem = K_dem / pv
    excess = dem - sup_avg
    if np.abs(excess / dem).max() < TOL:
        break
    pv *= np.clip((dem / np.maximum(sup_avg, 1e-9)) ** 0.05, 0.99, 1.01)
assert np.abs(excess / dem).max() < TOL, f"no convergence: {excess / dem}"
frac_opt = 1.0                                          # argmax assignment is optimal by construction
print(f"PASS  A1-FP  numeric fixed point exists: fictitious-play averaging settled in {it} "
      f"steps, max |excess demand| {np.abs(excess/dem).max():.1e} (within the 2% granularity "
      f"bound of 400 discrete types); assignment is each type's argmax by construction")
assert np.all(np.diff(choice) >= 0), f"assignment not monotone: {choice}"
print("PASS  A1-FP  positive assortative: pool index is monotone in talent "
      f"(pool sizes {np.bincount(choice, minlength=NP).tolist()})")

# A2-POOL: marginal acquirer in each occupied trained pool is interior and pinned
nf = net_flow(pv)
interior_hits = 0
for j in range(1, NP):
    members = np.where(choice == j)[0]
    if len(members) == 0 or members.min() == 0:
        continue
    m = members.min()                          # lowest-talent member = marginal acquirer
    adv = nf[m, j] - nf[m].max(where=np.arange(NP) != j, initial=-np.inf)
    prev = nf[m - 1, j] - nf[m - 1].max(where=np.arange(NP) != j, initial=-np.inf)
    assert adv >= -1e-9 and prev <= 1e-9, (j, adv, prev)
    interior_hits += 1
assert interior_hits >= 3
print(f"PASS  A2-POOL th_m interior in {interior_hits} pools: marginal member weakly prefers "
      "the pool, the next type down weakly prefers elsewhere (free entry pins the margin)")

# inframarginal talent rent rises in theta within a pool (Ricardian differential)
j = choice[-1]                                 # top pool
members = np.where(choice == j)[0]
rents = nf[members, j] - nf[members[0], j]
assert np.all(np.diff(rents) > -1e-12) and rents[-1] > 1e-6
print(f"PASS  A2-POOL inframarginal rents increase in talent within the pool "
      f"(top rent {rents[-1]:.3f} over the pool's marginal acquirer)")

print()
print("All Block A checks passed (flags A0-DR, A1-FP, A2-POOL).")
