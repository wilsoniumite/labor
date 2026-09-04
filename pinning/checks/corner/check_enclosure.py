"""Verification of item 2: the enclosure margin — endogenous s(r).

Numbering: enters as Proposition 9 ("The commons, priced", end of Section 6
between Feasibility = 8 and the mix; the mix moves 9 -> 10 and the Baumol
fork 10 -> 11). Document order preserved.

Units: the goods numeraire of Proposition 4. Exit life = autarkic keep s_0
(own production on a plot, machine-independent by construction) minus the
plot's rent q*h_e; dependency floor s_d; q = r/pg as everywhere.

Claims checked (drafted in enclosure_section.html):
  N-i    idle margin: while land demand falls short of the stock, the
         marginal parcel rents at its reservation value zero — the commons
         is the idle margin and s = s_0 (exogenous); the closure's land
         clearing T_P + T_H = T (5i) closes that margin at the corner
  N-ii   enclosed exit: s(q) = max(s_0 - q*h_e, s_d), falling one-for-one
         (ds/dq = -h_e); enclosure completes at finite progress,
         q_enc = (s_0 - s_d)/h_e
  N-iii  the race: kappa(q) rises (8i) while s(q) falls; q_enc vs q* (the
         kappa = 1 threshold) orders by crowding: q_enc >= q* iff
         N <= N_crit = q_enc*T/(g_s + q_enc*h_s). Worked instance
         (closure world, s_0 = 1.5, h_e = h_s = 1, s_d = 0): q_enc = 1.5,
         N_crit = 60; N = 50 safe (q* = 1 < 1.5), N = 80 opens the gap
         (q* = 4 > 1.5) — commons dead, floor not yet fundable
  N-iv   u-cancellation survives s(r): (w + u) - (s(q) + u) is independent
         of u — 6(i) unharmed; in the enclosed limit the guaranteed floor
         is u + s_d, and the h_e*q the enclosure takes is exactly what the
         purchased commons replaces
  N-v    desperate supply (linked regime): lower s raises participation and
         lowers the wage through Prop 1's comparative statics — enclosure
         manufactures labor supply (numeric: s 25 -> 20 gives n 0.5 -> 0.6
         and w 30 -> 26 in the sloped instance)
"""
import sympy as sp

def ok(name, zero_expr):
    z = sp.simplify(zero_expr)
    assert z == 0, f"FAIL {name}: residual {z}"
    print(f"PASS  {name}")


# ---------- N-i: idle margin and its closing ----------
# Reservation rent zero + excess supply => marginal rent zero.
D_land, T = sp.symbols('D T', positive=True)
r_marginal = sp.Piecewise((0, D_land < T), (sp.Symbol('r_pos', positive=True), True))
assert r_marginal.subs(D_land, T / 2) == 0
# Corner closes the margin: closure land clearing (re-derived, as in C-i).
a, ell, r, rho, Lbar, sigma = sp.symbols('a ell r rho Lbar sigma', positive=True)
Y = (1 - a) * (1 - sigma) * T / (ell * rho * Lbar)
X = rho * Lbar * Y / (1 - a)
T_P = ell * X
T_H = sigma * T
ok("N-i   corner closes the idle margin: T_P + T_H = T (5i)", T_P + T_H - T)
print("PASS  N-i   idle margin rents at zero while D < T; the corner employs it all")

# ---------- N-ii: enclosed exit ----------
q, h_e, s0, sd = sp.symbols('q h_e s_0 s_d', positive=True)
s_of_q = s0 - q * h_e                       # above the dependency floor
ok("N-ii  ds/dq = -h_e (one-for-one with the land price of subsistence living)",
   sp.diff(s_of_q, q) + h_e)
q_enc = sp.solve(sp.Eq(s_of_q, sd), q)[0]
ok("N-ii  q_enc = (s_0 - s_d)/h_e — enclosure completes at finite progress",
   q_enc - (s0 - sd) / h_e)

# ---------- N-iii: the race ----------
N, gs, hs = sp.symbols('N g_s h_s', positive=True)
qstar = N * gs / (T - N * hs)               # kappa = 1 threshold (8ii)
N_crit = sp.solve(sp.Eq(qstar, q_enc), N)[0]
ok("N-iii N_crit = q_enc*T/(g_s + q_enc*h_s)",
   N_crit - q_enc * T / (gs + q_enc * hs))
inst = {s0: sp.Rational(3, 2), sd: 0, h_e: 1, gs: 1, hs: 1, T: 100}
q_enc_num = q_enc.subs(inst)
assert q_enc_num == sp.Rational(3, 2)
assert N_crit.subs(inst) == 60
q50 = qstar.subs(inst).subs(N, 50)          # = 1
q80 = qstar.subs(inst).subs(N, 80)          # = 4
assert q50 == 1 and q50 < q_enc_num          # N=50: floor fundable before commons dies
assert q80 == 4 and q80 > q_enc_num          # N=80: the gap opens
print("PASS  N-iii race: q_enc = 1.5, N_crit = 60; N=50 safe (q*=1), "
      "N=80 opens the gap (q*=4) — commons dead, floor not yet fundable")

# ---------- N-iv: u-cancellation survives; the floor in the enclosed limit ----------
w, u = sp.symbols('w u', positive=True)
gap_participation = (w + u) - (s_of_q + u)
ok("N-iv  (w + u) - (s(q) + u) independent of u — 6(i) unharmed",
   sp.diff(gap_participation, u))
floor_enclosed = sp.Max(s_of_q, sd) + u
past = floor_enclosed.subs([(s0, sp.Rational(3, 2)), (h_e, 1),
                            (sd, sp.Rational(1, 10)), (u, 2), (q, 10)])
assert past == sp.Rational(21, 10)                 # beyond q_enc: floor = s_d + u
taken = s0 - s_of_q
ok("N-iv  what enclosure takes is exactly h_e*q — the purchased commons' bill",
   taken - q * h_e)
print("PASS  N-iv  enclosed-limit floor = s_d + u: the transfer becomes the commons")

# ---------- N-v: desperate supply in the linked regime ----------
c0, k, r0, s_lin = sp.symbols('c k r_0 s_lin', positive=True)
n_of_s = 1 - s_lin / 50                      # participation falls in s (instance)
w_of_s = c0 * (r0 + k * (1 - n_of_s))
ok("N-v   dw/ds > 0: lower s means more participants and a lower wage",
   sp.diff(w_of_s, s_lin) - c0 * k / 50)
inst2 = {c0: 10, r0: 1, k: 4}
assert n_of_s.subs(s_lin, 25) == sp.Rational(1, 2)
assert n_of_s.subs(s_lin, 20) == sp.Rational(3, 5)
assert w_of_s.subs(inst2).subs(s_lin, 25) == 30
assert w_of_s.subs(inst2).subs(s_lin, 20) == 26
print("PASS  N-v   numeric: s 25 -> 20 gives n 0.5 -> 0.6 and w 30 -> 26 "
      "(enclosure manufactures labor supply)")

# ---------- N-vi: the take is capped past q_enc (review-pass addition) ----------
# Below q_enc the household rents the plot and the take is h_e*q (N-iv's
# unclamped identity). Past q_enc renting is dominated (s0 - q*h_e < s_d), the
# household stands on s_d, and restoring s0 costs s0 - s_d = h_e*q_enc: the
# bill CAPS at the enclosure threshold, it does not track the rising rent.
q_enc = (s0 - sd) / h_e
s_clamped = sp.Max(s0 - q * h_e, sd)
restore_bill = s0 - s_clamped                       # what u must cover to hold s0
vals_cap = [(s0, sp.Rational(3, 2)), (h_e, 1), (sd, sp.Rational(1, 10))]
below = restore_bill.subs(vals_cap).subs(q, 1)      # q < q_enc = 1.4
past2 = restore_bill.subs(vals_cap).subs(q, 10)     # q > q_enc
assert below == 1                                   # = h_e*q, still linear
assert past2 == sp.Rational(7, 5)                   # = s0 - s_d = h_e*q_enc: capped
assert past2 == (q_enc * h_e).subs(vals_cap)
ok("N-vi  cap identity: s0 - s_d = h_e*q_enc", (s0 - sd) - h_e * q_enc)
print("PASS  N-vi  the take caps at h_e*q_enc past enclosure (bill 1.0 at q=1, "
      "1.4 for ALL q > q_enc) — not the still-rising plot rent")

print()
print("All enclosure-margin checks passed.")
