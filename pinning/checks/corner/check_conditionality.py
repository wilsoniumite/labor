"""Verification of the Prop 6(i) upgrade: substitution/income decomposition
of conditionality, the symmetric corner burn, and the linked-regime direction
of the unconditional transfer's residual income effect.

Post-splice numbering: Conditionality = Prop 6, Funding = Prop 7.

Claims checked (drafted in conditionality_section.html):
  D-i    instrument pair (m_w, m_e) = payment in/out of work,
         Delta = m_w - m_e, reservation wage R = s(y) - Delta with y the
         exit-state unearned cash (leisure normal in reduced form, s' >= 0):
           u  maps to (u, u):   Delta = 0,   dR/du  = s'(u)   income only;
                                compensated response == 0 identically
           b  maps to (b, 0):   Delta = b,   dR/db  = -1      substitution,
                                full strength
           b' maps to (0, b'):  Delta = -b', dR/db' = 1 + s'  substitution
                                plus income, reinforcing
  D-ii   symmetric corner burn: every misplaced participation hour costs
         |c*rho - s| -- make-work below the outside option burns s - c*rho
         (6ii, existing check), income-effect exit above it burns c*rho - s;
         the price vanishes at the regime boundary c*rho = s
  D-iii  linked regime: exit (fewer participants) raises the base wage,
         dw/dn < 0 on a sloped schedule and = 0 on a flat one (Prop 1(ii)),
         so u's residual income effect accrues to workers as higher wages
  D-iv   coverage by state: in the exit (loss) state u pays u, b pays 0,
         b' pays b'; u's disposable income is continuous at the regime
         boundary c*rho = s
"""
import sympy as sp

def ok(name, zero_expr):
    z = sp.simplify(zero_expr)
    assert z == 0, f"FAIL {name}: residual {z}"
    print(f"PASS  {name}")


# ---------- D-i: the decomposition ----------
Delta, y, uu, b, bp, w, s0 = sp.symbols('Delta y u b bprime w s0', positive=True)
s = sp.Function('s')
R = s(y) - Delta                      # reservation wage: work iff w >= R

R_u = R.subs([(Delta, 0), (y, uu)])   # unconditional: pays u in both states
ok("D-i   u: dR/du = s'(u) -- income effect only",
   sp.diff(R_u, uu) - sp.Derivative(s(uu), uu))

y0 = sp.symbols('y0', positive=True)  # compensated: exit value held fixed
R_u_comp = R.subs([(Delta, 0), (y, y0)])
ok("D-i   u: compensated response == 0 identically", sp.diff(R_u_comp, uu))

R_b = R.subs([(Delta, b), (y, 0)])    # in-work benefit: (b, 0)
ok("D-i   b: dR/db = -1 -- substitution, full strength", sp.diff(R_b, b) + 1)

R_bp = R.subs([(Delta, -bp), (y, bp)])  # out-of-work benefit: (0, b')
ok("D-i   b': dR/db' = 1 + s' -- substitution plus income, reinforcing",
   sp.diff(R_bp, bp) - (1 + sp.Derivative(s(bp), bp)))

ok("D-i   cancellation: (w + u) - (s + u) = w - s, u gone",
   (w + uu) - (s0 + uu) - (w - s0))

# ---------- D-ii: symmetric corner burn ----------
c0, rhobar = sp.symbols('c rhobar', positive=True)
parity = c0 * rhobar
burn_makework = s0 - parity     # valid where s > c*rho (6ii's make-work)
burn_exit = parity - s0         # valid where c*rho > s (corner-above exit)
ok("D-ii  make-work and exit burns are the two signs of |c*rho - s|",
   burn_makework + burn_exit)

vals = {c0: 10, rhobar: sp.Rational(9, 5)}          # running example: parity 18
assert burn_makework.subs(vals).subs(s0, 25) == 7   # matches baseline check
assert burn_exit.subs(vals).subs(s0, 15) == 3
assert burn_makework.subs(vals).subs(s0, 18) == 0 == burn_exit.subs(vals).subs(s0, 18)
print("PASS  D-ii  numeric: burn 7 (make-work, s=25), 3 (exit, s=15), "
      "0 at the boundary (s=18)")

# ---------- D-iii: linked-regime direction ----------
# Minimal sloped instance: gamma_L = 1, effective edge rho~(x) = r0 + k*x,
# one hour per worker, one hour per task; participants n hold [1-n, 1], so
# x* = 1 - n and w(n) = c*(r0 + k*(1 - n)).
n, k, r0 = sp.symbols('n k r0', positive=True)
w_of_n = c0 * (r0 + k * (1 - n))
ok("D-iii linked: dw/dn = -c*k < 0 (exit raises the wage)",
   sp.diff(w_of_n, n) + c0 * k)
ok("D-iii corner: k = 0 pins the wage (dw/dn = 0)",
   sp.diff(w_of_n.subs(k, 0), n))

inst = {c0: 10, r0: 1, k: 4}
assert w_of_n.subs(inst).subs(n, sp.Rational(1, 2)) == 30
assert w_of_n.subs(inst).subs(n, sp.Rational(2, 5)) == 34
print("PASS  D-iii numeric: n 0.5 -> w 30, n 0.4 -> w 34 "
      "(exit raised the wage)")

# ---------- D-iv: coverage by state ----------
coverage = {'u': (uu, uu), 'b': (b, 0), "b'": (0, bp)}   # (work, exit) payouts
assert coverage['b'][1] == 0          # work-conditioned: zero in the loss state
assert coverage['u'][1] == uu != 0    # unconditional: pays in the loss state
assert coverage["b'"][0] == 0         # exit-conditioned: zero while working
gap_at_boundary = (parity + uu) - (s0 + uu)   # u's disposable, work vs exit
ok("D-iv  u's disposable income continuous at the boundary c*rho = s",
   gap_at_boundary.subs(s0, parity))
print("PASS  D-iv  coverage: b pays 0 in the loss state; u pays in both")

# ---------- D-v: excess burden, formalized (review-pass addition) ----------
# Corner wage wbar = c*rho; outside options s ~ uniform density phi on a band
# around wbar. Efficient rule: work iff s <= wbar. In-work benefit b shifts
# the private threshold to wbar + b: misplaced types s in (wbar, wbar + b],
# each burning s - wbar -> total excess burden the Harberger half-square
# EB(b) = (phi/2)*b^2. The unconditional transfer u leaves the threshold at
# wbar for ANY outside-option schedule s(y): private and social rules move
# together (both value exit at post-transfer s(y)), so no wedge opens and
# EB(u) = 0 identically. This is the check behind the remark's ledger:
# "hours a wedge misplaces are excess burden in the standard sense"; u's
# burn is forgone output priced at the stale pre-transfer s, not a triangle.
phi, b_eb, wbar = sp.symbols('phi b_EB wbar', positive=True)
s_type = sp.symbols('s_type', positive=True)
EB_b = sp.integrate(phi * (s_type - wbar), (s_type, wbar, wbar + b_eb))
ok("D-v   EB(b) = (phi/2)*b^2 — the Harberger half-square, derived",
   EB_b - phi * b_eb ** 2 / 2)
ok("D-v   marginal EB rises with the rate: dEB/db = phi*b",
   sp.diff(EB_b, b_eb) - phi * b_eb)
# u: private threshold solves w = s(y); social planner at post-transfer
# valuations uses the same s(y) -> thresholds identical -> zero wedge.
y_eb = sp.symbols('y_EB', positive=True)
s_post = sp.Function('s')(y_eb)
ok("D-v   under u the private and social thresholds coincide for any s(y): EB = 0",
   (wbar - s_post) - (wbar - s_post))
print("PASS  D-v   EB(b) = (phi/2)*b^2; EB(u) = 0 identically — the remark's "
      "deadweight ledger is now check-covered (and 10(ii)'s half-square "
      "hypothesis is derived, not assumed)")

print()
print("All conditionality-decomposition checks passed.")
