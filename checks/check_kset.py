"""Verification of item 5: Proposition 9 (the Baumol fork), the
verifiability/credence result, and the superstar bifurcation.

Post-splice numbering: closure = 5, Conditionality = 6, Funding = 7,
Feasibility = 8, enclosure = 9, mix frontier = 10; this is Proposition 11
(subsection at the end of Section 9). It entered as 9 and renumbered twice
the same day (mix took 9, then enclosure took 9; 2026-08-05).

Claims checked (drafted in kset_section.html):
  P9-i    Leontief cost concentration: a good whose checklist meets K
          (measure k, wage w_K) has unit cost C(m) = k*w_K/gamma_L +
          (1-k)*m; as per-task machine cost m -> 0, C -> k*w_K/gamma_L and
          labor's share of cost -> 1 (Baumol derived, not assumed)
  P9-ii   the consumption fork: CES share of K-content as the machine
          price p_g -> 0 tends to 1 | theta | 0 for eta < 1 | = 1 | > 1
  P9-iii  three-way terminal split (machine good, land services, K-labor;
          common eta < 1): machine share -> 0; land and K split the limit
          by weights x price terms; corner of Props 3-8 = the K-empty
          boundary
  P9-iv   credence bound: sustainable provenance premium pi_H <=
          min(phi_H, v*f/(1-v)) — no-entry condition for fakers who pass
          w.p. (1-v) and pay penalty f when caught; f -> 0 kills the
          premium for every v < 1; v -> 1 (co-presence) unbounds it
  P9-v    superstar/barbell: top K-performer's income share beta +
          (1-beta)/n, rising in reach beta; median-to-mean K-income =
          (1-beta) -> 0; aggregate labor share can be high while the
          median wage sits at the corner floor
  kappa   consequence for Prop 8: a K-service component in the
          subsistence bundle raises P_s, so kappa falls at every q
"""
import sympy as sp

def ok(name, zero_expr):
    z = sp.simplify(zero_expr)
    assert z == 0, f"FAIL {name}: residual {z}"
    print(f"PASS  {name}")


# ---------- P9-i: cost concentration ----------
k, wK, gL, m = sp.symbols('k w_K gamma_L m', positive=True)
C = k * wK / gL + (1 - k) * m
labor_share = (k * wK / gL) / C
assert sp.limit(C, m, 0, '+') == k * wK / gL
assert sp.limit(labor_share, m, 0, '+') == 1
ok("P9-i   d(labor cost share)/dm < 0 (share rises as machines cheapen)",
   sp.diff(labor_share, m) + (k * wK / gL) * (1 - k) / C ** 2)
print("PASS  P9-i   C -> k*w_K/gamma_L and labor share of cost -> 1 as m -> 0")

# ---------- P9-ii: the consumption fork ----------
pg, eta, theta = sp.symbols('p_g eta theta', positive=True)
th = sp.Rational(1, 4)
sK = theta * wK ** (1 - eta) / (theta * wK ** (1 - eta) + (1 - theta) * pg ** (1 - eta))
for eta_val, expected, label in [(sp.Rational(1, 2), 1, "eta<1 -> 1"),
                                 (1, th, "eta=1 -> theta"),
                                 (2, 0, "eta>1 -> 0")]:
    lim = sp.limit(sK.subs([(eta, eta_val), (theta, th), (wK, 3)]), pg, 0, '+')
    assert sp.simplify(lim - expected) == 0, (label, lim)
print("PASS  P9-ii  s_K -> 1 | theta | 0 as p_g -> 0 for eta < 1 | = 1 | > 1")

# ---------- P9-iii: three-way terminal split ----------
r, thg, thT, thK = sp.symbols('r theta_g theta_T theta_K', positive=True)
e = sp.Rational(1, 2)                        # common eta < 1
terms = {"g": thg * pg ** (1 - e), "T": thT * r ** (1 - e), "K": thK * wK ** (1 - e)}
tot = sum(terms.values())
share_g = terms["g"] / tot
share_T = terms["T"] / tot
lim_g = sp.limit(share_g, pg, 0, '+')
lim_T = sp.limit(share_T, pg, 0, '+')
assert lim_g == 0
ok("P9-iii land's terminal share = theta_T*r^(1-eta) / (theta_T*r^(1-eta) + theta_K*w_K^(1-eta))",
   lim_T - thT * r ** (1 - e) / (thT * r ** (1 - e) + thK * wK ** (1 - e)))
# K-empty boundary: theta_K = 0 sends land's terminal share to 1 (the corner world)
assert sp.simplify(lim_T.subs(thK, 0) - 1) == 0
print("PASS  P9-iii machine share -> 0; K = 0 boundary returns the corner (land takes all)")

# ---------- P9-iv: credence bound ----------
v, f, phiH, piH = sp.symbols('v f phi_H pi_H', positive=True)
# faker expected profit per attempt: (1-v)*pi - v*f; no-entry iff pi <= v*f/(1-v)
pi_max = v * f / (1 - v)
ok("P9-iv  no-entry bound: (1-v)*pi_max - v*f = 0", (1 - v) * pi_max - v * f)
ok("P9-iv  d(pi_max)/dv = f/(1-v)^2 > 0", sp.diff(pi_max, v) - f / (1 - v) ** 2)
ok("P9-iv  d(pi_max)/df = v/(1-v) > 0", sp.diff(pi_max, f) - v / (1 - v))
assert sp.limit(pi_max, f, 0, '+') == 0            # price-only enforcement: premium dies, any v < 1
assert sp.limit(pi_max.subs(f, 1), v, 1, '-') == sp.oo   # co-presence: fraud impossible
print("PASS  P9-iv  f -> 0 kills the premium for every v < 1; v -> 1 unbounds it; "
      "effective premium min(phi_H, v*f/(1-v))")

# ---------- P9-v: superstars and the barbell ----------
beta, n = sp.symbols('beta n', positive=True)
top_share = beta + (1 - beta) / n
ok("P9-v   d(top share)/d(beta) = 1 - 1/n > 0 for n > 1",
   sp.diff(top_share, beta) - (1 - 1 / n))
# non-top performers split (1-beta) equally: median/mean = (1-beta) for n >= 3
median_over_mean = ((1 - beta) * 1 / n) / (1 / n)
ok("P9-v   median-to-mean K-income = 1 - beta", median_over_mean - (1 - beta))
assert sp.limit(median_over_mean, beta, 1, '-') == 0
# barbell instance: N = 100 workers, K holds 5 with s_K = 0.6 of income;
# 95 at the corner floor w = c*rhobar = 18 (running example's terminal stage).
N_, nK, s_K_num, floor = 100, 5, sp.Rational(3, 5), 18
Y = 100 * floor / (1 - s_K_num) * sp.Rational(95, 100)   # normalize: non-K wage bill = 95*18
nonK_bill = 95 * floor
total_income = nonK_bill / (1 - s_K_num)
agg_labor_share = 1                                       # all income is labor here by construction
median_wage = floor                                       # 95 of 100 workers at the floor
assert total_income * s_K_num == sp.Rational(2565)        # K's 60% = 2565 over 5 workers
assert (total_income * s_K_num / nK) / floor == sp.Rational(2565, 5) / 18  # K-wage 28.5x floor
print("PASS  P9-v   barbell instance: aggregate labor share 100%, median wage at the "
      "floor (18), K-wage 28.5x the floor across 5 of 100 workers")

# ---------- consequence for Prop 8's kappa ----------
q, T, N, gs, hs, ks = sp.symbols('q T N g_s h_s k_s', positive=True)
kappa_no_K = q * T / (N * (gs + q * hs))
# K-service component k_s*w_K in the bundle, priced in units of the good (w_K/pg fixed):
wK_units = sp.symbols('w_K_over_pg', positive=True)
kappa_K = q * T / (N * (gs + ks * wK_units + q * hs))
ok("kappa  K-term lowers coverage at every q",
   sp.simplify(kappa_no_K - kappa_K
               - q * T * ks * wK_units / (N * (gs + q * hs) * (gs + ks * wK_units + q * hs))))
print("PASS  kappa  a K-service component in P_s lowers kappa at every q "
      "(the reservation economy taxes its own remedy)")

print()
print("All K-set / Baumol-fork checks passed.")
