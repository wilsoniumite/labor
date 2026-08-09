"""Verification of the feasibility theorem (queue item 3, theorem half):
Proposition 8, the coverage ratio of the rent-funded floor.

Post-splice numbering: closure = Prop 5, Conditionality = 6, Funding = 7;
this enters as Prop 8 (end of Section 6 — nothing downstream renumbers).

Setup: corner regime with the closure machinery. Per-person subsistence is a
bundle (g_s, h_s) of the machine-made good and direct land services, costing
P_s = pg*g_s + r*h_s. Coverage ratio at full rent capture:
    kappa = rT / (N * P_s).

Claims checked (drafted in feasibility_section.html):
  F-i    kappa = q*T / (N*(g_s + q*h_s)) with q = r/pg = (1-a)/(l rho Lbar);
         strictly increasing in q; limits 0 (q -> 0) and T/(N*h_s)
         (q -> oo), the sup unattained at any finite q
  F-ii   kappa = 1 exactly at q* = N*g_s/(T - N*h_s), which exists iff
         T > N*h_s; if T <= N*h_s no finite q funds the floor
  F-iii  the land constraint in disguise: kappa >= 1 iff
         N*(g_s/q + h_s) <= T (direct plus embodied land content of N
         subsistence bundles fits in T); fiscal = physical because national
         income is rT identically (5ii)
  F-iv   machine-improvement margins: every margin raises kappa (a down,
         l down, rho down all raise q); the a-margin is bounded (q -> 1/(l
         rho Lbar) as a -> 0), echoing the patched 4(ii)
  numeric: the closure check's world (a=3/5, l=1/5, rho=9/5, Lbar=1, T=100,
         r=1, so pg=0.9, q=10/9, rT=GDP=100): N=50 feasible (kappa=20/19,
         N*P_s=95<=100, q*=1), N=80 not yet (kappa=25/38, q*=4), N=120
         never (T - N*h_s < 0, sup kappa = 5/6 < 1)
"""
import sympy as sp

def ok(name, zero_expr):
    z = sp.simplify(zero_expr)
    assert z == 0, f"FAIL {name}: residual {z}"
    print(f"PASS  {name}")


q, T, N, gs, hs = sp.symbols('q T N g_s h_s', positive=True)
a, ell, rho, Lbar, r = sp.symbols('a ell rho Lbar r', positive=True)

kappa = q * T / (N * (gs + q * hs))

# ---------- F-i: from primitives, monotone, limits ----------
pg = ell * r * rho * Lbar / (1 - a)          # closure: pg = c*rho*Lbar
q_val = (1 - a) / (ell * rho * Lbar)         # Prop 4(ii)
Ps = pg * gs + r * hs
ok("F-i   kappa from primitives: rT/(N*P_s) = qT/(N(g_s + q h_s))",
   r * T / (N * Ps) - kappa.subs(q, q_val))
ok("F-i   dkappa/dq = T*g_s / (N*(g_s + q*h_s)^2) > 0",
   sp.diff(kappa, q) - T * gs / (N * (gs + q * hs) ** 2))
assert sp.limit(kappa, q, 0, '+') == 0
assert sp.simplify(sp.limit(kappa, q, sp.oo) - T / (N * hs)) == 0
ok("F-i   sup unattained: T/(N h_s) - kappa = T g_s/(N h_s (g_s + q h_s))",
   T / (N * hs) - kappa - T * gs / (N * hs * (gs + q * hs)))
print("PASS  F-i   limits: kappa -> 0 as q -> 0+, kappa -> T/(N*h_s) as q -> oo")

# ---------- F-ii: the threshold ----------
D = sp.symbols('D', positive=True)           # T = N*h_s + D, D > 0
qstar = N * gs / D
ok("F-ii  kappa(q*) = 1 at q* = N g_s/(T - N h_s), when T > N h_s",
   kappa.subs([(q, qstar), (T, N * hs + D)]) - 1)
# T <= N*h_s: sup kappa = T/(N h_s) <= 1 and unattained -> infeasible at all q.
ok("F-ii  at T = N h_s the sup is exactly 1 (and unattained)",
   (T / (N * hs)).subs(T, N * hs) - 1)

# ---------- F-iii: the land constraint in disguise ----------
land_slack = T - N * (gs / q + hs)           # land left after N bundles
ok("F-iii kappa - 1 = q * land_slack / (N*(g_s + q*h_s)) -- same sign",
   kappa - 1 - q * land_slack / (N * (gs + q * hs)))

# ---------- F-iv: margins ----------
ok("F-iv  dq/da = -1/(l rho Lbar) < 0  (a down raises q: improvement)",
   sp.diff(q_val, a) + 1 / (ell * rho * Lbar))
ok("F-iv  a -> 0 bound: q -> 1/(l rho Lbar), the 4(ii) echo",
   sp.limit(q_val, a, 0, '+') - 1 / (ell * rho * Lbar))
ok("F-iv  dq/dl = -q/l < 0  (l down raises q)",
   sp.diff(q_val, ell) + q_val / ell)
ok("F-iv  dq/drho = -q/rho < 0  (rho down raises q)",
   sp.diff(q_val, rho) + q_val / rho)
print("PASS  F-iv  all machine margins raise q hence kappa; a-margin bounded")

# ---------- numeric instances (closure check's world) ----------
base = {a: sp.Rational(3, 5), ell: sp.Rational(1, 5), rho: sp.Rational(9, 5),
        Lbar: 1, r: 1, T: 100, gs: 1, hs: 1}
q_num = q_val.subs(base)
assert q_num == sp.Rational(10, 9)
Ps_num = Ps.subs(base)
assert Ps_num == sp.Rational(19, 10)                    # P_s = 1.9
k50 = kappa.subs(base).subs([(q, q_num), (N, 50)])
assert k50 == sp.Rational(20, 19) and k50 >= 1          # feasible
assert (50 * Ps_num <= 100) is not False                # N*P_s = 95 <= rT
assert qstar.subs(base).subs([(N, 50), (D, 50)]) == 1   # q* = 1 <= 10/9
k80 = kappa.subs(base).subs([(q, q_num), (N, 80)])
assert k80 == sp.Rational(25, 38) and k80 < 1           # not yet: q* = 4
assert qstar.subs(base).subs([(N, 80), (D, 20)]) == 4
k120sup = (T / (N * hs)).subs(base).subs(N, 120)
assert k120sup == sp.Rational(5, 6) < 1                 # never feasible
print("PASS  numeric: N=50 kappa=20/19 (feasible, q*=1), N=80 kappa=25/38 "
      "(q*=4, not yet), N=120 sup=5/6 (never)")

print()
print("All feasibility checks passed.")
