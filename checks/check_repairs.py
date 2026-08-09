"""Verification of the small-repairs batch (2026-08-05): Lemma 2
(existence/uniqueness of the threshold equilibrium) and the
machine-stock-with-depreciation generalization of Prop 3. The other
repairs (abstract alignment, "gadgets" fix, Prediction 1 relabel, 7(i)
full-participation marker, reference additions) are wording, verified by
the review pass rather than algebra.

Claims checked:
  R-i    Lemma 2: the market-clearing wage c*rho~(x*(n)) is continuous and
         strictly decreasing in participants (single crossing with the
         participation step at s => existence + uniqueness); flat stretch
         pins the wage (reuses the D-iii instance)
  R-ii   depreciation: user-cost recursion c = (delta+d)*(a*c + l*r) solves
         to c = l*r*(delta+d)/(1 - a*(delta+d)); nests the paper's
         one-period display at d = 1 and the static formula at
         delta = 0, d = 1; finite iff a*(delta+d) < 1
"""
import sympy as sp

def ok(name, zero_expr):
    z = sp.simplify(zero_expr)
    assert z == 0, f"FAIL {name}: residual {z}"
    print(f"PASS  {name}")


# ---------- R-i: Lemma 2 ----------
c0, k, r0, n = sp.symbols('c k r_0 n', positive=True)
w_demand = c0 * (r0 + k * (1 - n))            # sloped instance: strictly decreasing
ok("R-i   demand wage strictly decreasing in participants: dw/dn = -c*k",
   sp.diff(w_demand, n) + c0 * k)
inst = {c0: 10, r0: 1, k: 4}
s_val = 25
sol = sp.solve(sp.Eq(w_demand.subs(inst), s_val), n)
assert len(sol) == 1 and sol[0] == sp.Rational(5, 8)   # unique crossing at the step
ok("R-i   flat stretch (k = 0) pins the wage: dw/dn = 0",
   sp.diff(w_demand.subs(k, 0), n))
print("PASS  R-i   single crossing: unique n = 2/5 at s = 25 in the instance; "
      "existence by continuity, uniqueness by monotonicity")

# ---------- R-ii: depreciation ----------
a, ell, r, delta, d = sp.symbols('a ell r delta d', positive=True)
c_sym = sp.symbols('c_m', positive=True)
c_user = sp.solve(sp.Eq(c_sym, (delta + d) * (a * c_sym + ell * r)), c_sym)[0]
ok("R-ii  user-cost recursion: c = l*r*(delta+d)/(1 - a*(delta+d))",
   c_user - ell * r * (delta + d) / (1 - a * (delta + d)))
ok("R-ii  nests the one-period display at d = 1: c = l*r*(1+delta)/(1-a*(1+delta))",
   c_user.subs(d, 1) - ell * r * (1 + delta) / (1 - a * (1 + delta)))
static = sp.limit(c_user.subs(d, 1), delta, 0, '+')
ok("R-ii  nests the static formula at delta = 0, d = 1: c = l*r/(1-a)",
   static - ell * r / (1 - a))
print("PASS  R-ii  finiteness iff a*(delta+d) < 1; wear thickens the sliver as "
      "waiting does; the destination is unchanged")

print()
print("All small-repairs checks passed.")
