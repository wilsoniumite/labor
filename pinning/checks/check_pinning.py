# check_pinning.py — algebra + numeric checks for the rewrite's new spine
# ("Pinning the Wage to Scarcity and Technology", 2026-08-13).
#
# Everything NEW relative to checks/corner/ (the lambda=0 corner spine) is here: the λ-recursion
# (labor inside the machine recipe), the replacement closure, the fork
# displays with λ, the comparative statics the text states in words, the
# welfare-pair sums with multiple terminal factors, and the priced-exit
# floor. The λ=0 corner spine is already covered by checks/corner/ and
# lean/ — checks 1 and 6 confirm the limits agree.
#
# House rule: no proposition enters the draft before its check passes.
# Run: ../venv/Scripts/python.exe checks/check_pinning.py  (from pinning/)

import sympy as sp

GREEN = []
def ok(name, cond):
    assert cond, f"CHECK FAILED: {name}"
    GREEN.append(name)
    print(f"  ok  {name}")

a, lam, gamma, b, r, w, c = sp.symbols("a lambda gamma b r w c", positive=True)
Lbar, alpha, q = sp.symbols("Lbar alpha q", positive=True)

# ---------------------------------------------------------------- Prop 2
# Replacement closure: solve {w = c*gamma, c = a*c + lam*w + b*r}.
sol = sp.solve([sp.Eq(w, c*gamma), sp.Eq(c, a*c + lam*w + b*r)], [w, c], dict=True)
assert len(sol) == 1
c_star = sp.simplify(sol[0][c])
w_star = sp.simplify(sol[0][w])
D = 1 - a - lam*gamma  # viability denominator

ok("P2 closure: c = b*r/(1-a-lam*gamma)",
   sp.simplify(c_star - b*r/D) == 0)
ok("P2 closure: w = gamma*b*r/(1-a-lam*gamma)",
   sp.simplify(w_star - gamma*b*r/D) == 0)

# λ→0 limit recovers the corner recursion c = b*r/(1-a) (old Prop 3).
ok("P2 limit: lam->0 gives c = b*r/(1-a)",
   sp.simplify(c_star.subs(lam, 0) - b*r/(1 - a)) == 0)

# Comparative statics ON THE VIABLE SET D>0 (signs the text states in words):
# both closures rise in lam and in gamma; so recursive automation (lam down)
# and task automation (gamma down) each lower w; lam down lowers c; and with
# lam>0 task automation ALSO cheapens the machine (cross-effect).
dw_dlam = sp.simplify(sp.diff(w_star, lam))
dw_dgamma = sp.simplify(sp.diff(w_star, gamma))
dc_dlam = sp.simplify(sp.diff(c_star, lam))
dc_dgamma = sp.simplify(sp.diff(c_star, gamma))
ok("P2 statics: dw/dlam = gamma^2*b*r/D^2 > 0",
   sp.simplify(dw_dlam - gamma**2*b*r/D**2) == 0)
ok("P2 statics: dw/dgamma = b*r*(1-a)/D^2 > 0",
   sp.simplify(dw_dgamma - b*r*(1 - a)/D**2) == 0)
ok("P2 statics: dc/dlam = gamma*b*r/D^2 > 0",
   sp.simplify(dc_dlam - gamma*b*r/D**2) == 0)
ok("P2 statics: dc/dgamma = lam*b*r/D^2 > 0 (cross-effect needs lam>0)",
   sp.simplify(dc_dgamma - lam*b*r/D**2) == 0)

# Numeric instantiation (the paper's worked instance): a=0.5, lam=0.1,
# gamma*=3, b=0.2, r=1  ->  c=1, w=3; recursive automation to lam=0
# gives c=0.4, w=1.2 (a 60% cut at fixed gamma*, r).
inst = {a: sp.Rational(1, 2), lam: sp.Rational(1, 10), gamma: 3,
        b: sp.Rational(1, 5), r: 1}
ok("P2 instance: (a,lam,gamma,b,r)=(0.5,0.1,3,0.2,1) -> c=1",
   c_star.subs(inst) == 1)
ok("P2 instance: -> w=3",  w_star.subs(inst) == 3)
ok("P2 instance: recursion balances 1 = 0.5*1 + 0.1*3 + 0.2*1",
   sp.Rational(1, 2)*1 + sp.Rational(1, 10)*3 + sp.Rational(1, 5)*1 == 1)
inst0 = dict(inst); inst0[lam] = 0
ok("P2 instance: lam->0 gives c=0.4, w=1.2 (60% wage cut)",
   c_star.subs(inst0) == sp.Rational(2, 5) and w_star.subs(inst0) == sp.Rational(6, 5))
ok("P2 viability: instance denominator D=0.2>0; D<=0 kills positivity",
   D.subs(inst) == sp.Rational(1, 5) and D.subs({a: sp.Rational(1, 2), lam: sp.Rational(1, 5), gamma: 3}) < 0)

# ---------------------------------------------------------------- Prop 4
# Flat-capability limit. p = c*gammabar*Lbar; w = c*gammabar.
p_num = c_star.subs(gamma, gamma) * gamma * Lbar     # with gamma now read as gammabar
w_flat = c_star * gamma

ok("P4(i): w/p = 1/Lbar (machine quality cancels)",
   sp.simplify(w_flat/p_num - 1/Lbar) == 0)

r_over_p = sp.simplify(r/p_num)
ok("P4(ii): r/p = (1-a-lam*gamma)/(b*gamma*Lbar)",
   sp.simplify(r_over_p - D/(b*gamma*Lbar)) == 0)
ok("P4(ii) statics: d(r/p)/dlam = -1/(b*Lbar) < 0 (lam down raises it)",
   sp.simplify(sp.diff(r_over_p, lam) + 1/(b*Lbar)) == 0)
ok("P4(ii) statics: d(r/p)/dgamma = -(1-a)/(b*gamma^2*Lbar) < 0 (gamma down raises it)",
   sp.simplify(sp.diff(r_over_p, gamma) + (1 - a)/(b*gamma**2*Lbar)) == 0)
# For the limits sympy needs the viability domain made explicit: write
# 1-a = anet > 0 (for gamma->0) and 1-a-lam*gamma = Dpos > 0 (for b->0).
anet, Dpos = sp.symbols("anet Dpos", positive=True)
ok("P4(ii) divergence: gamma->0+ sends r/p to +oo (given a<1)",
   sp.limit(r_over_p.subs(a, 1 - anet), gamma, 0, "+") == sp.oo)
ok("P4(ii) divergence: b->0+ sends r/p to +oo (given D>0)",
   sp.limit(r_over_p.subs(a, 1 - lam*gamma - Dpos), b, 0, "+") == sp.oo)
# Bounded-substitution remark (stated at lam=0, as in the prior draft):
b0 = sp.symbols("b0", positive=True)
ok("P4(ii) bound: at lam=0, b=b0*(1-a) gives r/p = 1/(b0*gamma*Lbar)",
   sp.simplify(r_over_p.subs({lam: 0, b: b0*(1 - a)}) - 1/(b0*gamma*Lbar)) == 0)

# P4(iii): geometric index P = p_num^(1-alpha)*r^alpha.
P = p_num**(1 - alpha) * r**alpha
ok("P4(iii): w/P = (1/Lbar)*(p/r)^alpha",
   sp.simplify(w_flat/P - (1/Lbar)*(p_num/r)**alpha) == 0)

# ---------------------------------------------------------------- Prop 5
# Welfare pair with J=2 terminal factors, N=3 people.
tau_R = sp.symbols("tau_R", nonnegative=True)
r1, r2, T1, T2 = sp.symbols("r1 r2 T1 T2", positive=True)
om = sp.Matrix(3, 2, sp.symbols("om11 om12 om21 om22 om31 om32", nonnegative=True))
R = r1*T1 + r2*T2
N_people = 3
d = tau_R*R/N_people
incomes = [(1 - tau_R)*(om[i, 0]*r1*T1 + om[i, 1]*r2*T2) + d for i in range(3)]
total = sp.simplify(sp.expand(sum(incomes)))
share_constraint = [(om[0, j] + om[1, j] + om[2, j], 1) for j in range(2)]
total_c = total
for expr, val in share_constraint:
    total_c = total_c.subs(om[2, 0], 1 - om[0, 0] - om[1, 0]).subs(om[2, 1], 1 - om[0, 1] - om[1, 1])
ok("P5: incomes sum to R for every tau_R (shares sum to 1)",
   sp.simplify(total_c - R) == 0)
ok("P5: tau_R=0 gives inherited shares; tau_R=1 gives R/N each",
   sp.simplify(incomes[0].subs(tau_R, 1) - R/3) == 0
   and sp.simplify(incomes[0].subs(tau_R, 0) - (om[0, 0]*r1*T1 + om[0, 1]*r2*T2)) == 0)
# No participation wedge: (w+d >= s+d) <-> (w >= s) — d cancels identically.
s_ = sp.symbols("s", positive=True)
ok("P5: participation comparison unchanged by d ((w+d)-(s+d) = w-s)",
   sp.simplify((w + d) - (s_ + d) - (w - s_)) == 0)

# ---------------------------------------------------------------- Prop 3
# Priced exit: s(q) = max(s0 - q*h_e, s_d).
s0, s_lb, he = sp.symbols("s0 s_lb h_e", positive=True)
s_of_q = sp.Max(s0 - q*he, s_lb)
q_enc = (s0 - s_lb)/he
ok("P3 floor: s(q) hits the dependency floor exactly at q_enc = (s0-s_lb)/h_e",
   sp.simplify(s_of_q.subs(q, q_enc) - s_lb) == 0
   and sp.simplify((s0 - q*he).subs(q, q_enc) - s_lb) == 0)
qa, qb = sp.Rational(1, 3), sp.Rational(2, 3)
inst_e = {s0: 10, s_lb: 4, he: 6}  # q_enc = 1
ok("P3 floor: s(q) weakly decreasing in q (numeric grid)",
   all(float(s_of_q.subs(inst_e).subs(q, x1)) >= float(s_of_q.subs(inst_e).subs(q, x2))
       for x1, x2 in [(qa, qb), (qb, 1), (1, 2)]))
ok("P3 floor: above q_enc the floor is s_lb (constant)",
   s_of_q.subs(inst_e).subs(q, 2) == 4 and s_of_q.subs(inst_e).subs(q, 5) == 4)

# ------------------------------------------------- Appendix D (gamma-form)
# G.1 restated 2026-08-19 on gamma -> 0 outside H (the per-task symbol m is
# gone; checks/corner/check_kset.py holds the old m-form record). The
# new claim chain: c stays pinned by the recursion while per-task machine
# cost c*gamma/gamma_L vanishes, so an H-holding good's unit cost tends to
# its H-labor cost. CES share limits double as Appendix B's display
# (G.1(ii) now cites it), previously unchecked in THIS repo.
Habs, wH, gL = sp.symbols("Habs w_H gamma_L", positive=True)
c_of_gamma = b*r/(1 - a - lam*gamma)          # worst case: margin at the vanishing gamma
unit_cost = Habs*wH/gL + (1 - Habs)*c_of_gamma*gamma/gL
anet2 = sp.symbols("anet2", positive=True)
ok("D1(i): c pinned at gamma->0: c -> b*r/(1-a) > 0, not zero",
   sp.limit(c_of_gamma.subs(a, 1 - anet2), gamma, 0, "+") == b*r/anet2)
ok("D1(i): unit cost -> |H|*w_H/gamma_L as gamma->0 outside H",
   sp.limit(unit_cost.subs(a, 1 - anet2), gamma, 0, "+") == Habs*wH/gL)
ok("D1(i): labor's share of cost -> 1",
   sp.limit((Habs*wH/gL)/unit_cost.subs(a, 1 - anet2), gamma, 0, "+") == 1)
ok("D1(iii): H-free good's price -> 0 (|H|=0 case of (i))",
   sp.limit(unit_cost.subs({a: 1 - anet2, Habs: 0}), gamma, 0, "+") == 0)
ok("D1(ii): relative price of H-content over H-free diverges",
   sp.limit((wH/gL)/(c_of_gamma.subs(a, 1 - anet2)*gamma/gL), gamma, 0, "+") == sp.oo)
# Appendix B's share display alpha(q) = alpha*q^(1-sigma)/(alpha*q^(1-sigma)+1-alpha),
# limits as the dear category's relative price q -> oo, at alpha = 1/4:
sigma_ = sp.symbols("sigma", positive=True)
alph4 = sp.Rational(1, 4)
alpha_q = alph4*q**(1 - sigma_) / (alph4*q**(1 - sigma_) + 1 - alph4)
ok("B/D1(ii): CES share -> 1 for sigma<1 (complements: the dear category eats the budget)",
   sp.limit(alpha_q.subs(sigma_, sp.Rational(1, 2)), q, sp.oo) == 1)
ok("B/D1(ii): CES share = taste weight for sigma=1 (Cobb-Douglas)",
   sp.simplify(alpha_q.subs(sigma_, 1) - alph4) == 0)
ok("B/D1(ii): CES share -> 0 for sigma>1 (substitution defuses)",
   sp.limit(alpha_q.subs(sigma_, 2), q, sp.oo) == 0)

# --------------------------------------------- Appendix D x C.3 (2026-08-19)
# The cross-module display added with the environment appendix: a H-service
# component in the subsistence bundle lowers coverage at every q, further
# the dearer the H-hour. (Algebra first verified in checks/corner's
# check_kset.py; restated here on this paper's own display.)
ns, wHg = sp.symbols("n_s w_H_over_p", positive=True)
gs, hs, T_, N_ = sp.symbols("g_s h_s T N", positive=True)
kappa_free = q*T_/(N_*(gs + q*hs))
kappa_H = q*T_/(N_*(gs + ns*wHg + q*hs))
ok("DxC: H-component lowers coverage at every q (positive gap identity)",
   sp.simplify(kappa_free - kappa_H
               - q*T_*ns*wHg/(N_*(gs + q*hs)*(gs + ns*wHg + q*hs))) == 0)
ok("DxC: the gap grows as the K-hour gets dearer (d kappa_H / d(w_H/p) < 0)",
   sp.simplify(sp.diff(kappa_H, wHg)
               + q*T_*ns/(N_*(gs + ns*wHg + q*hs)**2)) == 0)

# ------------------------------------------------------- Appendix A hook
# Market-clearing wage decreasing in participation, given r: w(gamma*) rises
# in gamma*, and gamma(x*) falls as more tasks must be held — composite falls.
ok("A: dw/dgamma > 0 on D>0 => w(N_a) inherits monotonicity of gamma(x*(N_a))",
   sp.simplify(dw_dgamma*D**2 - b*r*(1 - a)) == 0)

# --------------------------------------------- Appendix D lemmas (2026-08-26)
# D.2 the fraud bound: a false provenance claim is caught w.p. v and pays f;
# a premium p is sustainable iff expected fake profit (1-v)p - v*f <= 0.
v_, f_, p_ = sp.symbols("v f p", positive=True)
bound = v_*f_/(1 - v_)
ok("D.2: fraud bound solves the incentive condition exactly",
   sp.simplify(sp.solve(sp.Eq((1 - v_)*p_, v_*f_), p_)[0] - bound) == 0)
ok("D.2: bound rises in v and in f",
   sp.simplify(sp.diff(bound, v_) - f_/(1 - v_)**2) == 0
   and sp.simplify(sp.diff(bound, f_) - v_/(1 - v_)) == 0)
ok("D.2: diverges as v -> 1, collapses as f -> 0 for every v < 1",
   sp.limit(bound, v_, 1, '-') == sp.oo and sp.limit(bound, f_, 0, '+') == 0)

# D.3 superstar concentration: a measure-zero top carries psi of
# H-expenditure, the co-present remainder is uniform. Discrete stand-in:
# one star among N workers, total expenditure 1; median/mean -> 1 - psi.
Nw, psi_n = 100001, 0.6
others = (1 - psi_n)/(Nw - 1)      # uniform non-star income
mean_i = 1.0/Nw                     # mean unchanged: total/N
ok("D.3: median = non-star income; median/mean -> (1-psi) as the top's measure -> 0",
   abs(others/mean_i - (1 - psi_n)*Nw/(Nw - 1)) < 1e-12
   and abs(others/mean_i - (1 - psi_n)) < 1e-4)

# ------------------------------ Appendix A: joint-system instantiation
# Sloped regime with r endogenous. Config: gamma(x) = 1 + 4x (gamma_L = 1),
# a=0.5, lam=0.1, b=0.2, land T=10, unit labor N=1, Cobb-Douglas land
# share alpha=0.3, exit s0=1, h_e=0.5, s_d=0.2; numeraire p = 1. Given
# x*, free entry + the margin + the unit-cost condition pin (w, c, r); Y
# comes from labor clearing; land clearing is one residual in x*. Verified:
# exactly one sign change on the grid (a unique crossing), the land market
# clears at the root, goods clearing follows (the Walras cross-check of the
# accounting), viability holds, and w > s(q) so full participation is
# consistent with the posited equilibrium.
aJ, lamJ, bJ, TJ, alphJ, NJ = 0.5, 0.1, 0.2, 10.0, 0.3, 1.0
s0J, heJ, sdJ = 1.0, 0.5, 0.2

def joint_state(xs):
    rho_x = 1 + 4*xs
    den = 1 - aJ - lamJ*rho_x
    Irho = xs + 2*xs*xs                      # integral of gamma on [0, xs]
    cJ = 1.0/(rho_x*(1 - xs) + Irho)         # unit cost of the good = 1
    wJ = rho_x*cJ                            # the margin
    rJ = cJ*den/bJ                         # free entry
    Y = NJ/((1 - xs) + lamJ*Irho/(1 - aJ))   # labor clearing at N
    X = Y*Irho/(1 - aJ)                      # gross machine services
    land = bJ*X + alphJ*(wJ*NJ + rJ*TJ)/rJ  # machine + housing demand
    return land - TJ, wJ, cJ, rJ, Y, X, den

grid = [i/1000.0 for i in range(1, 990)]
signs = [joint_state(x)[0] > 0 for x in grid]
flips = sum(1 for k in range(1, len(grid)) if signs[k] != signs[k - 1])
ok("A-joint: land residual has exactly one sign change on the x* grid", flips == 1)
lo, hi = 0.001, 0.989
for _ in range(80):
    mid = (lo + hi)/2
    if (joint_state(lo)[0] > 0) == (joint_state(mid)[0] > 0):
        lo = mid
    else:
        hi = mid
residJ, wJ, cJ, rJ, YJ, XJ, denJ = joint_state((lo + hi)/2)
ok("A-joint: land market clears at the root", abs(residJ) < 1e-9)
ok("A-joint: viability 1 - a - lam*gamma(x*) > 0 at the root", denJ > 0)
ok("A-joint: goods market clears by Walras at the root",
   abs(YJ - (1 - alphJ)*(wJ*NJ + rJ*TJ)) < 1e-8)
ok("A-joint: full participation consistent (w > s(q), q = r at p = 1)",
   wJ > max(s0J - rJ*heJ, sdJ))

# ----------------------------- the λ>0 user-cost forms (2026-08-27)
# One unit of machine stock costs P = a·c + λ·w + b·r to build; services
# price by user cost c = s·P where s is the carrying factor — s = 1+ρ for
# one-period building under time preference alone, s = ρ+δ with wear.
# With the margin w = γ*·c the closed form is c = s·br/(1 − s(a+λγ*)),
# viability s(a+λγ*) < 1 — the λ>0 generalization of Appendix A's two
# displays, previously deliberately unstated because unchecked.
rho_, delta_w, s_c = sp.symbols("rho delta s_carry", positive=True)
uc = sp.solve([sp.Eq(w, c*gamma), sp.Eq(c, s_c*(a*c + lam*w + b*r))],
              [w, c], dict=True)
assert len(uc) == 1
c_uc = sp.simplify(uc[0][c])
c_uc_form = s_c*b*r/(1 - s_c*(a + lam*gamma))
ok("A-usercost: closed form c = s·br/(1 − s(a+λγ*)) for carrying factor s",
   sp.simplify(c_uc - c_uc_form) == 0)
ok("A-usercost: w = γ*·c at the solution",
   sp.simplify(sp.simplify(uc[0][w]) - gamma*c_uc_form) == 0)
ok("A-usercost: λ→0 recovers both stated λ=0 displays (s=1+ρ and s=ρ+δ)",
   sp.simplify(c_uc.subs([(lam, 0), (s_c, 1+rho_)])
               - b*r*(1+rho_)/(1 - a*(1+rho_))) == 0
   and sp.simplify(c_uc.subs([(lam, 0), (s_c, rho_+delta_w)])
                   - b*r*(rho_+delta_w)/(1 - a*(rho_+delta_w))) == 0)
ok("A-usercost: s = 1 recovers the static closure c = br/(1−a−λγ*)",
   sp.simplify(c_uc.subs(s_c, 1) - b*r/(1 - a - lam*gamma)) == 0)
D_uc = 1 - s_c*(a + lam*gamma)
ok("A-usercost: dc/ds = br/D² > 0 and dc/dλ = s²γbr/D² > 0 on the viable set",
   sp.simplify(sp.diff(c_uc_form, s_c) - b*r/D_uc**2) == 0
   and sp.simplify(sp.diff(c_uc_form, lam) - s_c**2*gamma*b*r/D_uc**2) == 0)

print(f"\nALL GREEN ({len(GREEN)} checks)")
