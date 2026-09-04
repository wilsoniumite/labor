"""Verification of item 6: Proposition 9 (the mix frontier) — LVT/VAT
weights on the way to the corner.

Numbering: entered as Proposition 9, now Proposition 10 — the enclosure
margin (item 2) took 9 the same day, and the Baumol fork sits at 11.
Document order of propositions is preserved. The paper writes aggregate consumption
spending as E (bare C is the fork's unit cost); this check's internal C is
the same object.

Claims checked (drafted in mix_section.html):
  M-i    corner coincidence: at the pure corner (closure world), aggregate
         consumption spending E = pg*Y + r*T_H equals rT identically, so a
         uniform VAT and a proportional LVT share one base; the instruments
         merge
  M-ii   transition blind spots: LVT reaches saved rents that VAT misses;
         VAT reaches dynamic + institutional rents that LVT misses; neither
         base contains the other (numeric instance)
  M-iii  the frontier: minimizing VAT deadweight D = (h/2)*lam_C*C*t_V^2
         subject to t_L*rT + t_V*C = N*P_s with t_L <= 1 gives
         t_V = 0 when kappa >= 1, else t_L = 1 and
         t_V = N*P_s*(1-kappa)/C, with minimized deadweight proportional
         to lam_C*(1-kappa)^2 at given floor-to-consumption ratio;
         monotone: rising in lam_C, falling in kappa
  M-iv   convergence: lam_C -> 0 sends the transition deadweight to zero;
         with today's measured pair (lam_C = 0.72, kappa = 0.33) the cost
         index is 0.323; at (0.50, 0.60) it is 0.080 -- a fourfold fall
"""
import sympy as sp

def ok(name, zero_expr):
    z = sp.simplify(zero_expr)
    assert z == 0, f"FAIL {name}: residual {z}"
    print(f"PASS  {name}")


# ---------- M-i: corner coincidence (closure world) ----------
a, ell, r, rho, Lbar, sigma, T = sp.symbols('a ell r rho Lbar sigma T', positive=True)
c = ell * r / (1 - a)
pg = c * rho * Lbar
Y = (1 - a) * (1 - sigma) * T / (ell * rho * Lbar)   # closure output
T_H = sigma * T
E = pg * Y + r * T_H                                  # all consumption spending
ok("M-i   corner: consumption spending E = rT identically (one base)", E - r * T)

# ---------- M-ii: transition blind spots (numeric) ----------
rT, saved = 100, 20            # land rents, of which 20 saved (VAT-blind)
O = 50                          # dynamic + institutional rents, consumed (LVT-blind)
W = 200                         # wage-financed consumption
C_num = (rT - saved) + O + W    # consumption = 330
B_lvt = rT                      # reaches saved rents too
B_vat_clean = (rT - saved) + O  # non-wage consumption slice = 130
assert O > 0 and saved > 0
assert B_lvt - (rT - saved) == saved          # LVT-only reach: saved rents
assert B_vat_clean - (rT - saved) == O        # VAT-only clean reach: other rents
print("PASS  M-ii  blind spots: LVT-only reaches saved rents (20), VAT-only "
      "reaches non-site rents (50); neither base contains the other")

# ---------- M-iii: the frontier ----------
h, lamC, Cc, NPs, rT_s, tV = sp.symbols('h lambda_C C NP_s rT t_V', positive=True)
kappa = rT_s / NPs
# revenue: t_L*rT + t_V*C = NPs; deadweight D = (h/2)*lamC*C*t_V^2, dD/dt_L = 0,
# so minimize t_V: t_L = min(1, NPs/rT). Case kappa >= 1: t_V = 0. Case kappa < 1:
tV_star = (NPs - rT_s) / Cc
ok("M-iii t_V* = N*P_s*(1-kappa)/C", tV_star - NPs * (1 - kappa) / Cc)
D_star = (h / 2) * lamC * Cc * tV_star ** 2
ok("M-iii D* = (h/2)*lambda_C*(N*P_s)^2*(1-kappa)^2/C  — the display",
   D_star - (h / 2) * lamC * NPs ** 2 * (1 - kappa) ** 2 / Cc)
ok("M-iii dD*/dlambda_C > 0 (falls as wage-linkage falls)",
   sp.diff(D_star, lamC) - D_star / lamC)
kap = sp.symbols('kap', positive=True)
D_in_kappa = (h / 2) * lamC * NPs ** 2 * (1 - kap) ** 2 / Cc
ok("M-iii dD*/dkappa = -h*lambda_C*(N*P_s)^2*(1-kappa)/C < 0 (falls as coverage climbs)",
   sp.diff(D_in_kappa, kap) + h * lamC * NPs ** 2 * (1 - kap) / Cc)
# t_L = 1 is optimal: any t_L < 1 forces higher t_V at zero deadweight saving.
tL_alt = sp.Rational(9, 10)
tV_alt = (NPs - tL_alt * rT_s) / Cc
D_alt = (h / 2) * lamC * Cc * tV_alt ** 2
gap = sp.simplify((D_alt - D_star).subs([(NPs, 200), (rT_s, 66), (Cc, 300)]))
assert sp.simplify(gap) > 0
print("PASS  M-iii t_L = 1 dominates t_L = 0.9 (deadweight strictly larger at any "
      "lambda_C > 0): rent base fills first")

# ---------- M-iv: convergence and today's numbers ----------
index = lamC * (1 - kappa) ** 2
assert sp.limit(D_star, lamC, 0, '+') == 0
today = float(index.subs([(lamC, sp.Rational(72, 100)), (rT_s, 33), (NPs, 100)]))
future = float(index.subs([(lamC, sp.Rational(50, 100)), (rT_s, 60), (NPs, 100)]))
assert abs(today - 0.72 * 0.67 ** 2) < 1e-12 and abs(today - 0.323208) < 1e-6
assert abs(future - 0.08) < 1e-12
assert today / future > 4
print("PASS  M-iv  cost index lambda_C*(1-kappa)^2: today (0.72, 0.33) = 0.323; "
      "at (0.50, 0.60) = 0.080 — fourfold fall; -> 0 at the corner")

print()
print("All mix-frontier checks passed.")
