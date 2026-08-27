# check_pinning.py — algebra + numeric checks for the rewrite's new spine
# ("Pinning the Wage to Scarcity and Technology", 2026-08-13).
#
# Everything NEW relative to link-repo/checks/ is here: the λ-recursion
# (labor inside the machine recipe), the replacement closure, the fork
# displays with λ, the comparative statics the text states in words, the
# welfare-pair sums with multiple terminal factors, and the priced-exit
# floor. The λ=0 corner spine is already covered by link-repo/checks/ and
# lean/ — checks 1 and 6 confirm the limits agree.
#
# House rule: no proposition enters the draft before its check passes.
# Run: ../venv/Scripts/python.exe checks/check_pinning.py  (from the-link-revision/)

import sympy as sp

GREEN = []
def ok(name, cond):
    assert cond, f"CHECK FAILED: {name}"
    GREEN.append(name)
    print(f"  ok  {name}")

a, lam, rho, ell, r, w, c = sp.symbols("a lambda rho ell r w c", positive=True)
Lbar, sigma, q = sp.symbols("Lbar sigma q", positive=True)

# ---------------------------------------------------------------- Prop 2
# Replacement closure: solve {w = c*rho, c = a*c + lam*w + ell*r}.
sol = sp.solve([sp.Eq(w, c*rho), sp.Eq(c, a*c + lam*w + ell*r)], [w, c], dict=True)
assert len(sol) == 1
c_star = sp.simplify(sol[0][c])
w_star = sp.simplify(sol[0][w])
D = 1 - a - lam*rho  # viability denominator

ok("P2 closure: c = ell*r/(1-a-lam*rho)",
   sp.simplify(c_star - ell*r/D) == 0)
ok("P2 closure: w = rho*ell*r/(1-a-lam*rho)",
   sp.simplify(w_star - rho*ell*r/D) == 0)

# λ→0 limit recovers the corner recursion c = ell*r/(1-a) (old Prop 3).
ok("P2 limit: lam->0 gives c = ell*r/(1-a)",
   sp.simplify(c_star.subs(lam, 0) - ell*r/(1 - a)) == 0)

# Comparative statics ON THE VIABLE SET D>0 (signs the text states in words):
# both closures rise in lam and in rho; so recursive automation (lam down)
# and task automation (rho down) each lower w; lam down lowers c; and with
# lam>0 task automation ALSO cheapens the machine (cross-effect).
dw_dlam = sp.simplify(sp.diff(w_star, lam))
dw_drho = sp.simplify(sp.diff(w_star, rho))
dc_dlam = sp.simplify(sp.diff(c_star, lam))
dc_drho = sp.simplify(sp.diff(c_star, rho))
ok("P2 statics: dw/dlam = rho^2*ell*r/D^2 > 0",
   sp.simplify(dw_dlam - rho**2*ell*r/D**2) == 0)
ok("P2 statics: dw/drho = ell*r*(1-a)/D^2 > 0",
   sp.simplify(dw_drho - ell*r*(1 - a)/D**2) == 0)
ok("P2 statics: dc/dlam = rho*ell*r/D^2 > 0",
   sp.simplify(dc_dlam - rho*ell*r/D**2) == 0)
ok("P2 statics: dc/drho = lam*ell*r/D^2 > 0 (cross-effect needs lam>0)",
   sp.simplify(dc_drho - lam*ell*r/D**2) == 0)

# Numeric instantiation (the paper's worked instance): a=0.5, lam=0.1,
# rho*=3, ell=0.2, r=1  ->  c=1, w=3; recursive automation to lam=0
# gives c=0.4, w=1.2 (a 60% cut at fixed rho*, r).
inst = {a: sp.Rational(1, 2), lam: sp.Rational(1, 10), rho: 3,
        ell: sp.Rational(1, 5), r: 1}
ok("P2 instance: (a,lam,rho,ell,r)=(0.5,0.1,3,0.2,1) -> c=1",
   c_star.subs(inst) == 1)
ok("P2 instance: -> w=3",  w_star.subs(inst) == 3)
ok("P2 instance: recursion balances 1 = 0.5*1 + 0.1*3 + 0.2*1",
   sp.Rational(1, 2)*1 + sp.Rational(1, 10)*3 + sp.Rational(1, 5)*1 == 1)
inst0 = dict(inst); inst0[lam] = 0
ok("P2 instance: lam->0 gives c=0.4, w=1.2 (60% wage cut)",
   c_star.subs(inst0) == sp.Rational(2, 5) and w_star.subs(inst0) == sp.Rational(6, 5))
ok("P2 viability: instance denominator D=0.2>0; D<=0 kills positivity",
   D.subs(inst) == sp.Rational(1, 5) and D.subs({a: sp.Rational(1, 2), lam: sp.Rational(1, 5), rho: 3}) < 0)

# ---------------------------------------------------------------- Prop 4
# Flat-capability limit. p_g = c*rhobar*Lbar; w = c*rhobar.
pg = c_star.subs(rho, rho) * rho * Lbar     # with rho now read as rhobar
w_flat = c_star * rho

ok("P4(i): w/p_g = 1/Lbar (machine quality cancels)",
   sp.simplify(w_flat/pg - 1/Lbar) == 0)

r_over_pg = sp.simplify(r/pg)
ok("P4(ii): r/p_g = (1-a-lam*rho)/(ell*rho*Lbar)",
   sp.simplify(r_over_pg - D/(ell*rho*Lbar)) == 0)
ok("P4(ii) statics: d(r/p_g)/dlam = -1/(ell*Lbar) < 0 (lam down raises it)",
   sp.simplify(sp.diff(r_over_pg, lam) + 1/(ell*Lbar)) == 0)
ok("P4(ii) statics: d(r/p_g)/drho = -(1-a)/(ell*rho^2*Lbar) < 0 (rho down raises it)",
   sp.simplify(sp.diff(r_over_pg, rho) + (1 - a)/(ell*rho**2*Lbar)) == 0)
# For the limits sympy needs the viability domain made explicit: write
# 1-a = anet > 0 (for rho->0) and 1-a-lam*rho = Dpos > 0 (for ell->0).
anet, Dpos = sp.symbols("anet Dpos", positive=True)
ok("P4(ii) divergence: rho->0+ sends r/p_g to +oo (given a<1)",
   sp.limit(r_over_pg.subs(a, 1 - anet), rho, 0, "+") == sp.oo)
ok("P4(ii) divergence: ell->0+ sends r/p_g to +oo (given D>0)",
   sp.limit(r_over_pg.subs(a, 1 - lam*rho - Dpos), ell, 0, "+") == sp.oo)
# Bounded-substitution remark (stated at lam=0, as in the prior draft):
ell0 = sp.symbols("ell0", positive=True)
ok("P4(ii) bound: at lam=0, ell=ell0*(1-a) gives r/p_g = 1/(ell0*rho*Lbar)",
   sp.simplify(r_over_pg.subs({lam: 0, ell: ell0*(1 - a)}) - 1/(ell0*rho*Lbar)) == 0)

# P4(iii): geometric index P = pg^(1-sigma)*r^sigma.
P = pg**(1 - sigma) * r**sigma
ok("P4(iii): w/P = (1/Lbar)*(p_g/r)^sigma",
   sp.simplify(w_flat/P - (1/Lbar)*(pg/r)**sigma) == 0)

# ---------------------------------------------------------------- Prop 5
# Welfare pair with J=2 terminal factors, N=3 people.
tau = sp.symbols("tau", nonnegative=True)
r1, r2, T1, T2 = sp.symbols("r1 r2 T1 T2", positive=True)
om = sp.Matrix(3, 2, sp.symbols("om11 om12 om21 om22 om31 om32", nonnegative=True))
R = r1*T1 + r2*T2
N_people = 3
u = tau*R/N_people
incomes = [(1 - tau)*(om[i, 0]*r1*T1 + om[i, 1]*r2*T2) + u for i in range(3)]
total = sp.simplify(sp.expand(sum(incomes)))
share_constraint = [(om[0, j] + om[1, j] + om[2, j], 1) for j in range(2)]
total_c = total
for expr, val in share_constraint:
    total_c = total_c.subs(om[2, 0], 1 - om[0, 0] - om[1, 0]).subs(om[2, 1], 1 - om[0, 1] - om[1, 1])
ok("P5: incomes sum to R for every tau (shares sum to 1)",
   sp.simplify(total_c - R) == 0)
ok("P5: tau=0 gives inherited shares; tau=1 gives R/N each",
   sp.simplify(incomes[0].subs(tau, 1) - R/3) == 0
   and sp.simplify(incomes[0].subs(tau, 0) - (om[0, 0]*r1*T1 + om[0, 1]*r2*T2)) == 0)
# No participation wedge: (w+u >= s+u) <-> (w >= s) — u cancels identically.
s_ = sp.symbols("s", positive=True)
ok("P5: participation comparison unchanged by u ((w+u)-(s+u) = w-s)",
   sp.simplify((w + u) - (s_ + u) - (w - s_)) == 0)

# ---------------------------------------------------------------- Prop 3
# Priced exit: s(q) = max(s0 - q*h_e, s_d).
s0, sd, he = sp.symbols("s0 s_d h_e", positive=True)
s_of_q = sp.Max(s0 - q*he, sd)
q_enc = (s0 - sd)/he
ok("P3 floor: s(q) hits the dependency floor exactly at q_enc = (s0-s_d)/h_e",
   sp.simplify(s_of_q.subs(q, q_enc) - sd) == 0
   and sp.simplify((s0 - q*he).subs(q, q_enc) - sd) == 0)
qa, qb = sp.Rational(1, 3), sp.Rational(2, 3)
inst_e = {s0: 10, sd: 4, he: 6}  # q_enc = 1
ok("P3 floor: s(q) weakly decreasing in q (numeric grid)",
   all(float(s_of_q.subs(inst_e).subs(q, x1)) >= float(s_of_q.subs(inst_e).subs(q, x2))
       for x1, x2 in [(qa, qb), (qb, 1), (1, 2)]))
ok("P3 floor: above q_enc the floor is s_d (constant)",
   s_of_q.subs(inst_e).subs(q, 2) == 4 and s_of_q.subs(inst_e).subs(q, 5) == 4)

# ------------------------------------------------- Appendix G (rho-form)
# G.1 restated 2026-08-19 on rho -> 0 outside K (the per-task symbol m is
# gone; link-repo/checks/check_kset.py holds the old m-form record). The
# new claim chain: c stays pinned by the recursion while per-task machine
# cost c*rho/gamma_L vanishes, so a K-holding good's unit cost tends to
# its K-labor cost. CES share limits double as Appendix E's display
# (G.1(ii) now cites it), previously unchecked in THIS repo.
k_, wK, gL = sp.symbols("k w_K gamma_L", positive=True)
c_of_rho = ell*r/(1 - a - lam*rho)          # worst case: margin at the vanishing rho
unit_cost = k_*wK/gL + (1 - k_)*c_of_rho*rho/gL
anet2 = sp.symbols("anet2", positive=True)
ok("G1(i): c pinned at rho->0: c -> ell*r/(1-a) > 0, not zero",
   sp.limit(c_of_rho.subs(a, 1 - anet2), rho, 0, "+") == ell*r/anet2)
ok("G1(i): unit cost -> k*w_K/gamma_L as rho->0 outside K",
   sp.limit(unit_cost.subs(a, 1 - anet2), rho, 0, "+") == k_*wK/gL)
ok("G1(i): labor's share of cost -> 1",
   sp.limit((k_*wK/gL)/unit_cost.subs(a, 1 - anet2), rho, 0, "+") == 1)
ok("G1(iii): K-free good's price -> 0 (k=0 case of (i))",
   sp.limit(unit_cost.subs({a: 1 - anet2, k_: 0}), rho, 0, "+") == 0)
ok("G1(ii): relative price of K-content over K-free diverges",
   sp.limit((wK/gL)/(c_of_rho.subs(a, 1 - anet2)*rho/gL), rho, 0, "+") == sp.oo)
# Appendix E's share display s_h(q) = sigma*q^(1-eta)/(sigma*q^(1-eta)+1-sigma),
# limits as the dear category's relative price q -> oo, at sigma = 1/4:
eta_ = sp.symbols("eta", positive=True)
sig4 = sp.Rational(1, 4)
s_h = sig4*q**(1 - eta_) / (sig4*q**(1 - eta_) + 1 - sig4)
ok("E/G1(ii): CES share -> 1 for eta<1 (complements: the dear category eats the budget)",
   sp.limit(s_h.subs(eta_, sp.Rational(1, 2)), q, sp.oo) == 1)
ok("E/G1(ii): CES share = taste weight for eta=1 (Cobb-Douglas)",
   sp.simplify(s_h.subs(eta_, 1) - sig4) == 0)
ok("E/G1(ii): CES share -> 0 for eta>1 (substitution defuses)",
   sp.limit(s_h.subs(eta_, 2), q, sp.oo) == 0)

# --------------------------------------------- Appendix G x F.3 (2026-08-19)
# The cross-module display added with the environment appendix: a K-service
# component in the subsistence bundle lowers coverage at every q, further
# the dearer the K-hour. (Algebra first verified in link-repo's
# check_kset.py; restated here on this paper's own display.)
ks, wKg = sp.symbols("k_s w_K_over_pg", positive=True)
gs, hs, T_, N_ = sp.symbols("g_s h_s T N", positive=True)
kappa_free = q*T_/(N_*(gs + q*hs))
kappa_K = q*T_/(N_*(gs + ks*wKg + q*hs))
ok("GxF: K-component lowers coverage at every q (positive gap identity)",
   sp.simplify(kappa_free - kappa_K
               - q*T_*ks*wKg/(N_*(gs + q*hs)*(gs + ks*wKg + q*hs))) == 0)
ok("GxF: the gap grows as the K-hour gets dearer (d kappa_K / d(w_K/p_g) < 0)",
   sp.simplify(sp.diff(kappa_K, wKg)
               + q*T_*ks/(N_*(gs + ks*wKg + q*hs)**2)) == 0)

# ------------------------------------------------------- Appendix A hook
# Market-clearing wage decreasing in participation, given r: w(rho*) rises
# in rho*, and rho(x*) falls as more tasks must be held — composite falls.
ok("A: dw/drho > 0 on D>0 => w(n) inherits monotonicity of rho(x*(n))",
   sp.simplify(dw_drho*D**2 - ell*r*(1 - a)) == 0)

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

# D.3 superstar concentration: a measure-zero top carries beta of
# K-expenditure, the co-present remainder is uniform. Discrete stand-in:
# one star among N workers, total expenditure 1; median/mean -> 1 - beta.
Nw, beta_n = 100001, 0.6
others = (1 - beta_n)/(Nw - 1)      # uniform non-star income
mean_i = 1.0/Nw                     # mean unchanged: total/N
ok("D.3: median = non-star income; median/mean -> (1-beta) as the top's measure -> 0",
   abs(others/mean_i - (1 - beta_n)*Nw/(Nw - 1)) < 1e-12
   and abs(others/mean_i - (1 - beta_n)) < 1e-4)

# ------------------------------ Appendix A: joint-system instantiation
# Sloped regime with r endogenous. Config: rho(x) = 1 + 4x (gamma_L = 1),
# a=0.5, lam=0.1, ell=0.2, land T=10, unit labor N=1, Cobb-Douglas land
# share sigma=0.3, exit s0=1, h_e=0.5, s_d=0.2; numeraire p_g = 1. Given
# x*, free entry + the margin + the unit-cost condition pin (w, c, r); Y
# comes from labor clearing; land clearing is one residual in x*. Verified:
# exactly one sign change on the grid (a unique crossing), the land market
# clears at the root, goods clearing follows (the Walras cross-check of the
# accounting), viability holds, and w > s(q) so full participation is
# consistent with the posited equilibrium.
aJ, lamJ, ellJ, TJ, sigJ, NJ = 0.5, 0.1, 0.2, 10.0, 0.3, 1.0
s0J, heJ, sdJ = 1.0, 0.5, 0.2

def joint_state(xs):
    rho_x = 1 + 4*xs
    den = 1 - aJ - lamJ*rho_x
    Irho = xs + 2*xs*xs                      # integral of rho on [0, xs]
    cJ = 1.0/(rho_x*(1 - xs) + Irho)         # unit cost of the good = 1
    wJ = rho_x*cJ                            # the margin
    rJ = cJ*den/ellJ                         # free entry
    Y = NJ/((1 - xs) + lamJ*Irho/(1 - aJ))   # labor clearing at N
    X = Y*Irho/(1 - aJ)                      # gross machine services
    land = ellJ*X + sigJ*(wJ*NJ + rJ*TJ)/rJ  # machine + housing demand
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
ok("A-joint: viability 1 - a - lam*rho(x*) > 0 at the root", denJ > 0)
ok("A-joint: goods market clears by Walras at the root",
   abs(YJ - (1 - sigJ)*(wJ*NJ + rJ*TJ)) < 1e-8)
ok("A-joint: full participation consistent (w > s(q), q = r at p_g = 1)",
   wJ > max(s0J - rJ*heJ, sdJ))

# ----------------------------- the λ>0 user-cost forms (2026-08-27)
# One unit of machine stock costs P = a·c + λ·w + ℓ·r to build; services
# price by user cost c = s·P where s is the carrying factor — s = 1+δ for
# one-period building under time preference alone, s = δ+d with wear.
# With the margin w = ρ*·c the closed form is c = s·ℓr/(1 − s(a+λρ*)),
# viability s(a+λρ*) < 1 — the λ>0 generalization of Appendix A's two
# displays, previously deliberately unstated because unchecked.
delta_, d_w, s_c = sp.symbols("delta d_wear s_carry", positive=True)
uc = sp.solve([sp.Eq(w, c*rho), sp.Eq(c, s_c*(a*c + lam*w + ell*r))],
              [w, c], dict=True)
assert len(uc) == 1
c_uc = sp.simplify(uc[0][c])
c_uc_form = s_c*ell*r/(1 - s_c*(a + lam*rho))
ok("A-usercost: closed form c = s·ℓr/(1 − s(a+λρ*)) for carrying factor s",
   sp.simplify(c_uc - c_uc_form) == 0)
ok("A-usercost: w = ρ*·c at the solution",
   sp.simplify(sp.simplify(uc[0][w]) - rho*c_uc_form) == 0)
ok("A-usercost: λ→0 recovers both stated λ=0 displays (s=1+δ and s=δ+d)",
   sp.simplify(c_uc.subs([(lam, 0), (s_c, 1+delta_)])
               - ell*r*(1+delta_)/(1 - a*(1+delta_))) == 0
   and sp.simplify(c_uc.subs([(lam, 0), (s_c, delta_+d_w)])
                   - ell*r*(delta_+d_w)/(1 - a*(delta_+d_w))) == 0)
ok("A-usercost: s = 1 recovers the static closure c = ℓr/(1−a−λρ*)",
   sp.simplify(c_uc.subs(s_c, 1) - ell*r/(1 - a - lam*rho)) == 0)
D_uc = 1 - s_c*(a + lam*rho)
ok("A-usercost: dc/ds = ℓr/D² > 0 and dc/dλ = s²ρℓr/D² > 0 on the viable set",
   sp.simplify(sp.diff(c_uc_form, s_c) - ell*r/D_uc**2) == 0
   and sp.simplify(sp.diff(c_uc_form, lam) - s_c**2*rho*ell*r/D_uc**2) == 0)

print(f"\nALL GREEN ({len(GREEN)} checks)")
