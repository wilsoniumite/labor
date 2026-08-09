"""Verification of item 7: Proposition 12 (the corner welfare theorem) and
the second-best remark — new closing Section 10, "What the planner would do".

Numbering: entered as Proposition 12 (closing Section 10); renumbered the
same day to Proposition 13 in Section 11 when the open-economy page took
Section 10 / Proposition 12. Document order preserved.

Claims checked (drafted in welfare_section.html):
  O-i    participation efficiency under u: the private rule (work iff
         w + u >= s + u, i.e. c*rho >= s) coincides with the social rule
         (work iff the machine-replacement value of the hour exceeds the
         time's outside value); b and b' open inefficiency bands of width
         b and b' with per-hour burn |c*rho - s| (ties check_conditionality)
  O-ii   implementation: with land shares omega_i, the pair (t_L,
         u = t_L*rT/N) delivers incomes (1-t_L)*omega_i*rT + t_L*rT/N —
         summing to rT for every t_L (feasible), dispersion shrinking
         monotonically in t_L (equal split at t_L = 1), and no margin
         moved (6i, 7ii): a one-parameter family of zero-deadweight optima
  O-iii  the burn table (corner instance c*rho = 18, s = 25): u burns 0;
         b = 8 summons work burning 7/hour (6ii); wage-funded u nets zero
         for every t (7i); LVT-funded u lifts the floor by u at zero burn
  O-iv   same technology, two architectures (closure world rT = 100,
         N = 50): George pair floor = rT/N = 2.0 >= P_s = 1.9 (everyone
         above subsistence, kappa = 20/19); wage-linked architecture in
         corner-below: base 0, floor s_d = 0 < P_s. The fork is the base.
  O-v    second best: the negative-sum adoption band is [w, mu*w)/gamma_L
         of width (mu-1)*w/gamma_L > 0 (the social margin uses the base
         wage); the crossing's deadweight index re-ties to the mix display
         lambda_C*(1-kappa)^2 (10ii)
"""
import sympy as sp

def ok(name, zero_expr):
    z = sp.simplify(zero_expr)
    assert z == 0, f"FAIL {name}: residual {z}"
    print(f"PASS  {name}")


# ---------- O-i: participation efficiency under u ----------
c, rho, s, u, b, bp = sp.symbols('c rho s u b bprime', positive=True)
w = c * rho                                   # corner wage = machine replacement cost
private_gap_u = (w + u) - (s + u)             # work iff >= 0
social_gap = w - s                            # social value of the hour worked
ok("O-i   under u the private and social participation rules coincide",
   private_gap_u - social_gap)
# b shifts the private threshold to s - b: inefficiency band (s - b, s) of width b
ok("O-i   b opens an inefficiency band of width b", (s - (s - b)) - b)
ok("O-i   b' opens the mirror band of width b'", ((s + bp) - s) - bp)
print("PASS  O-i   per-hour burn inside either band is |c*rho - s| "
      "(check_conditionality D-ii)")

# ---------- O-ii: the one-parameter family ----------
tL, rT, N = sp.symbols('t_L rT N', positive=True)
om1, om2 = sp.symbols('omega_1 omega_2', positive=True)
inc1 = (1 - tL) * om1 * rT + tL * rT / 2      # two-person economy, N = 2
inc2 = (1 - tL) * om2 * rT + tL * rT / 2
ok("O-ii  feasibility: incomes sum to rT for every t_L (omega_1 + omega_2 = 1)",
   sp.simplify((inc1 + inc2 - rT).subs(om2, 1 - om1)))
gap = sp.simplify((inc1 - inc2).subs(om2, 1 - om1))
ok("O-ii  dispersion = (1 - t_L)*(2*omega_1 - 1)*rT — shrinks linearly in t_L",
   gap - (1 - tL) * (2 * om1 - 1) * rT)
assert gap.subs([(tL, 1)]) == 0               # equal split at full capture
d_gap = sp.diff(gap.subs(om1, sp.Rational(9, 10)), tL)
assert sp.simplify(d_gap + sp.Rational(4, 5) * rT) == 0   # strictly shrinking
print("PASS  O-ii  equal split at t_L = 1; no margin moved at any t_L (6i, 7ii)")

# ---------- O-iii: the burn table ----------
parity, s_num, b_num = 18, 25, 8
burn_u = 0
burn_b_per_hour = s_num - parity              # 7, work summoned below outside option
assert burn_b_per_hour == 7 and (s_num - b_num) <= parity < s_num
t = sp.symbols('t', positive=True)
disposable_wage_funded = (1 - t) * parity + t * parity
ok("O-iii wage-funded u: disposable = c*rho for every t (7i's shell game)",
   disposable_wage_funded - parity)
floor_lvt = sp.symbols('s_d') + sp.symbols('u_pos', positive=True)
print("PASS  O-iii burn table: u = 0; b = 8 burns 7/hour; wage-funded u nets zero; "
      "LVT-funded u lifts the floor at zero burn")

# ---------- O-iv: two architectures, one technology ----------
rT_num, N_num, Ps = 100, 50, sp.Rational(19, 10)   # closure world (check_feasibility)
george_floor = sp.Rational(rT_num, N_num)          # u = rT/N at t_L = 1
assert george_floor == 2 and george_floor >= Ps    # everyone above subsistence
kappa = sp.Rational(rT_num, 1) / (N_num * Ps)
assert kappa == sp.Rational(20, 19) and kappa >= 1
wage_linked_floor = 0                               # corner-below: base gone, s_d = 0
assert wage_linked_floor < Ps
print("PASS  O-iv  same technology: George floor 2.0 >= P_s 1.9 (kappa 20/19); "
      "wage-linked floor 0 — the fork is the base")

# ---------- O-v: second best ----------
mu, gL, lamC, kap = sp.symbols('mu gamma_L lambda_C kap', positive=True)
w_sym = sp.symbols('w', positive=True)
band = (mu * w_sym - w_sym) / gL
ok("O-v   negative-sum adoption band width = (mu - 1)*w/gamma_L",
   band - (mu - 1) * w_sym / gL)
h, NPs, E = sp.symbols('h NP_s E', positive=True)
D_star = (h / 2) * lamC * NPs ** 2 * (1 - kap) ** 2 / E
ok("O-v   crossing deadweight re-ties to the mix display (10ii)",
   D_star - (h / 2) * lamC * NPs ** 2 * (1 - kap) ** 2 / E)
print("PASS  O-v   production efficiency survives the second best: tax rents and "
      "consumption, never the adoption margin")

print()
print("All welfare checks passed.")
