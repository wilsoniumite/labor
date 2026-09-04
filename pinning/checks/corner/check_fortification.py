"""Verification of the fortification unit (Stella's critique, adopted
2026-08-05): Prop 2 proviso scope, the selection/distillation dynamic,
the growing blocked-task drag, Baumol compounding, punctuated adoption.

Post-splice numbering: closure = Prop 5, Conditionality = 6, Funding = 7,
Feasibility = 8. This unit adds NO numbered proposition — a proviso sentence
in Prop 2, a remark closing Section 4, an amended Prediction 2, and an
upgraded ledger sentence in Section 9.

Claims checked (drafted in fortification_section.html):
  W-i    selection/distillation: naked wedges flip in rho~-order as machine
         improvement g rises; fortified never flip; the fortified share of
         the SURVIVING wedge stock is weakly increasing in g (continuum
         version symbolic, discrete version numeric)
  W-ii   growing drag: a blocked task's forgone saving per task unit,
         w/gamma_L - c/gamma_M, is increasing in gamma_M and tends to the
         full labor cost w/gamma_L as machine cost -> 0
  W-iii  Baumol compounding: with fortified price fixed (labor cost) and
         machine prices collapsing, relative price z -> oo sends the
         fortified expenditure share to 1 | theta | 0 for eta < 1 | = 1 |
         > 1 (same CES structure as the closure's s_h check)
  W-iv   punctuated adoption: with confrontation cost F, the flip point
         g1(F) = m0/(mu*w - F) exceeds the naked flip point g0 = m0/(mu*w),
         is increasing in F, and adoption arrives with accumulated gap
         exactly F > 0 (naked tasks flip at gap 0: smooth)
"""
import sympy as sp

def ok(name, zero_expr):
    z = sp.simplify(zero_expr)
    assert z == 0, f"FAIL {name}: residual {z}"
    print(f"PASS  {name}")


# ---------- W-i: selection / distillation ----------
g, v, E, F0 = sp.symbols('g v E F0', positive=True)
# Naked effective edges uniform on [0, E]; waterline v; improvement divides
# edges by g, so a naked wedge survives iff its edge exceeds g*v.
M = (E - g * v) / E                       # surviving naked mass (g*v <= E)
share_F = F0 / (F0 + M)
ok("W-i   d(fortified share)/dg = F0*v/E / (F0 + M)^2 > 0",
   sp.diff(share_F, g) - F0 * (v / E) / (F0 + M) ** 2)

edges = [2, 3, 4, 5]                      # discrete naked wedges, v = 1
fort = 2
shares = []
for gg in [1, 2.5, 4.5, 6]:
    naked_alive = sum(1 for e in edges if e > gg * 1)
    shares.append(sp.Rational(fort, fort + naked_alive))
assert shares == [sp.Rational(1, 3), sp.Rational(2, 5),
                  sp.Rational(2, 3), sp.Rational(1, 1)]
assert all(shares[i] < shares[i + 1] for i in range(len(shares) - 1))
print("PASS  W-i   numeric: fortified share of surviving wedges "
      "1/3 -> 2/5 -> 2/3 -> 1 as improvement proceeds")

# ---------- W-ii: growing drag of a blocked task ----------
w, gL, gM, c = sp.symbols('w gamma_L gamma_M c', positive=True)
loss = w / gL - c / gM                    # forgone saving per task unit
ok("W-ii  d(loss)/d(gamma_M) = c/gamma_M^2 > 0",
   sp.diff(loss, gM) - c / gM ** 2)
assert sp.limit(loss, gM, sp.oo) == w / gL
print("PASS  W-ii  loss -> full labor cost w/gamma_L as machine cost -> 0")

# ---------- W-iii: Baumol compounding of the fortified share ----------
z, eta, theta = sp.symbols('z eta theta', positive=True)
share = theta * z ** (1 - eta) / (theta * z ** (1 - eta) + 1 - theta)
th = sp.Rational(1, 5)
cases = [(sp.Rational(1, 2), 1), (1, th), (2, 0)]
for eta_val, expected in cases:
    lim = sp.limit(share.subs([(eta, eta_val), (theta, th)]), z, sp.oo)
    assert sp.simplify(lim - expected) == 0, (eta_val, lim)
print("PASS  W-iii fortified expenditure share -> 1 | theta | 0 as z -> oo "
      "for eta < 1 | = 1 | > 1")

# ---------- W-iv: punctuated adoption ----------
mu, m0, Fc = sp.symbols('mu m0 F_c', positive=True)
muw = mu * w                              # wedge labor cost per task
gap = muw - m0 / g                        # saving from flipping, rises in g
g0 = sp.solve(sp.Eq(gap, 0), g)[0]        # naked flip point
g1 = sp.solve(sp.Eq(gap, Fc), g)[0]       # fortified flip point
ok("W-iv  naked flip at g0 = m0/(mu*w)", g0 - m0 / muw)
ok("W-iv  fortified flip at g1 = m0/(mu*w - F_c)", g1 - m0 / (muw - Fc))
ok("W-iv  delay dg1/dF_c = m0/(mu*w - F_c)^2 > 0",
   sp.diff(g1, Fc) - m0 / (muw - Fc) ** 2)
ok("W-iv  per-period gap at fortified adoption is exactly F_c (punctuated)",
   gap.subs(g, g1) - Fc)
# Numeric: mu*w = 50 (the wedged B-job), m0 = 45: g0 = 0.9; F = 5 -> g1 = 1;
# F = 25 -> g1 = 1.8 -- twice the machine progress before anything moves.
inst = {mu: sp.Rational(5, 4), w: 40, m0: 45}
assert g0.subs(inst) == sp.Rational(9, 10)
assert g1.subs(inst).subs(Fc, 5) == 1
assert g1.subs(inst).subs(Fc, 25) == sp.Rational(9, 5)
print("PASS  W-iv  numeric: g0 = 0.9; F=5 -> g1 = 1.0; F=25 -> g1 = 1.8")

print()
print("All fortification checks passed.")
