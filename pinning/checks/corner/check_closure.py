"""Verification of the new closure section (Proposition C) for 'The Link'.

Proposition C entered the draft as Proposition 5 (splice of 2026-08-05;
Conditionality -> 6, Funding -> 7). C-labels below kept for continuity.

Corner regime, machines perform all tasks, delta = 0. Households are
Cobb-Douglas, U = g^(1-sigma) * h^sigma, over the machine-made good g and
direct land services h (housing, siting, space). Land stock T splits into
production land T_P and housing land T_H.

Claims checked:
  (C-i)   unique real allocation: T_H = sigma*T,  Y = (1-a)(1-sigma)T/(l rho Lbar)
  (C-ii)  goods bill = production-land rent, pg*Y = r*T_P; and GDP = rT identically
  (C-iii) market clearing reproduces Prop 4(ii): r/pg = (1-a)/(l rho Lbar)
  gross-up consistency: X = rho*Lbar*Y/(1-a) solves X = rho*Lbar*Y + a*X; l*X = T_P
  CES remark: land expenditure share s_h -> 1 | sigma | 0 as r/pg -> oo,
              for eta < 1 | eta = 1 | eta > 1
"""
import sympy as sp

a, ell, r, rho, Lbar, sigma, T = sp.symbols('a ell r rho Lbar sigma T',
                                            positive=True)

c = ell * r / (1 - a)      # Prop 3
pg = c * rho * Lbar        # corner goods price


def ok(name, zero_expr):
    z = sp.simplify(zero_expr)
    assert z == 0, f"FAIL {name}: residual {z}"
    print(f"PASS  {name}")


# Demand side: Cobb-Douglas shares of income rT.
T_H = sigma * T
G = (1 - sigma) * r * T / pg                       # goods demand
Y = (1 - a) * (1 - sigma) * T / (ell * rho * Lbar)  # claimed output
ok("C-i    goods demand equals claimed Y", G - Y)

# Supply side: machine-services gross-up and land clearing.
X = rho * Lbar * Y / (1 - a)
ok("gross-up  X solves X = rho*Lbar*Y + a*X", X - (rho * Lbar * Y + a * X))
T_P = ell * X
ok("land clearing  T_P + T_H = T", T_P + T_H - T)

# (C-ii) incidence identities.
ok("C-ii   goods bill is production-land rent:  pg*Y = r*T_P", pg * Y - r * T_P)
ok("C-ii   GDP identity:  pg*Y + r*T_H = r*T", pg * Y + r * T_H - r * T)

# (C-iii) demand-side relative price matches the cost-side Prop 4(ii).
ok("C-iii  r/pg = (1-a)/(l rho Lbar)", r / pg - (1 - a) / (ell * rho * Lbar))

# Numeric instance (a=0.6, l=0.2, rho=1.8, Lbar=1, T=100, sigma=0.3, r=1):
vals = {a: sp.Rational(3, 5), ell: sp.Rational(1, 5), rho: sp.Rational(9, 5),
        Lbar: 1, T: 100, sigma: sp.Rational(3, 10), r: 1}
inst = {'c': float(c.subs(vals)), 'pg': float(pg.subs(vals)),
        'Y': float(Y.subs(vals)), 'T_H': float(T_H.subs(vals)),
        'T_P': float(T_P.subs(vals)),
        'GDP': float((pg * Y + r * T_H).subs(vals)),
        'rT': float((r * T).subs(vals))}
assert abs(inst['GDP'] - inst['rT']) < 1e-12
print(f"PASS  numeric instance: {inst}")

# CES remark: s_h(q) = sigma*q^(1-eta) / (sigma*q^(1-eta) + 1 - sigma), q = r/pg.
q, eta = sp.symbols('q eta', positive=True)
s_h = sigma * q ** (1 - eta) / (sigma * q ** (1 - eta) + (1 - sigma))
sig_val = sp.Rational(3, 10)
cases = [(sp.Rational(1, 2), 1, "eta<1 -> 1 (complements: immiseration sharpens)"),
         (1, sig_val, "eta=1 -> sigma (Cobb-Douglas)"),
         (2, 0, "eta>1 -> 0 (substitution bounds the squeeze)")]
for eta_val, expected, label in cases:
    lim = sp.limit(s_h.subs({eta: eta_val, sigma: sig_val}), q, sp.oo)
    assert sp.simplify(lim - expected) == 0, (eta_val, lim)
print("PASS  CES remark: land expenditure share limits 1 | sigma | 0 as q -> oo")

print()
print("All closure checks passed.")
