# check_dynamics.py — sympy checks for the v2 dynamics ("capital is time",
# rewrite brief v2 §3, structure memo STATE log 32; 2026-08-28).
#
# House rule: no proposition enters the draft before its check passes. The
# structure memo requires the u_K derivation and the steady-state equivalence
# lemma checked BEFORE any Phase 2/3 drafting; this file is that gate, plus
# the brief §6 sympy list and the T4 entry-margin algebra.
#
# Timing conventions (caution iv of the memo, pinned here once):
#   * build cost p_K is paid at the START of period t (dated t);
#   * the unit's first service period is t+J, its rental π_{t+J} dated t+J;
#   * wear is post-install: the first service is undepreciated, mass decays
#     by (1−δ) each service period thereafter.
# Ownership/financing convention (caution i, pinned here once):
#   * builds are 100%-externally financed at the world rate ρ (domestic
#     ownership with full-value debt, per the memo's suggestion — or foreign
#     equity; check L3 proves the two coincide in steady state, where free
#     entry makes the machine sector's net cash to households identically 0).
#   * households are hand-to-mouth: Inc = wN_a + rT in SS; goods clearing
#     carries an explicit net-export term NX = πK − p_K I (rentals out minus
#     build inflows), and Walras is verified WITH it.
#
# Run: ../venv/Scripts/python.exe checks/check_dynamics.py  (from the-link-revision/)

import json
import os
import sympy as sp

GREEN = []
def ok(name, cond):
    assert cond, f"CHECK FAILED: {name}"
    GREEN.append(name)
    print(f"  ok  {name}")

# v2 symbols. Operating recipe (a, λ, b) per unit of service; build recipe
# (a_I, λ_I, b_I) per unit started; ρ interest, δ wear, J build lag.
a, lam, gamma, b, r, w, c = sp.symbols("a lambda gamma b r w c", positive=True)
aI, lamI, bI = sp.symbols("a_I lambda_I b_I", nonnegative=True)
rho = sp.symbols("rho", positive=True)
delta = sp.symbols("delta", positive=True)   # 0 < δ < 1 imposed where needed
J = sp.symbols("J", integer=True, positive=True)
piK, pK = sp.symbols("pi p_K", positive=True)
alpha, T, N, Lbar, gamL, gambar = sp.symbols("alpha T N Lbar gamma_L gammabar", positive=True)

uK = (rho + delta) * (1 + rho) ** (J - 1)

# ================================================================ U: u_K
# The user cost is DERIVED from the free-entry PV condition, not asserted.
# A unit started at 0 costs p_K (dated 0) and yields π at J, J+1, … with
# survival (1−δ)^{s−J}:  p_K = Σ_{s≥J} (1+ρ)^{−s} (1−δ)^{s−J} π.
# Tail ratio qq = (1−δ)/(1+ρ) < 1 always on δ, ρ > 0, so the sum converges
# with no extra assumption: 1 − qq = (ρ+δ)/(1+ρ) > 0.
m, M = sp.symbols("m M", integer=True, nonnegative=True)
qq = (1 - delta) / (1 + rho)
ok("U1: geometric convergence is automatic — 1 − (1−δ)/(1+ρ) = (ρ+δ)/(1+ρ)",
   sp.simplify(1 - qq - (rho + delta) / (1 + rho)) == 0)
# partial-sum identity (algebra, no convergence needed), then the tail limit
partial = (1 - qq ** M) / (1 - qq)
ok("U2: partial-sum identity (1−qq)·Σ_{m<M} qq^m = 1 − qq^M",
   sp.simplify((1 - qq) * partial - (1 - qq ** M)) == 0)
PV = piK * (1 + rho) ** (-J) * (1 / (1 - qq))     # tail qq^M → 0
pi_solved = sp.solve(sp.Eq(pK, PV), piK)
ok("U3: free entry p_K = PV(π) delivers π = (ρ+δ)(1+ρ)^{J−1} p_K — u_K derived",
   len(pi_solved) == 1 and sp.simplify(pi_solved[0] - uK * pK) == 0)
ok("U4: J = 1 corner is the wear user cost ρ+δ; J = 1, δ = 1 is 1+ρ "
   "(Appendix A's two λ=0 carrying factors are u_K corners)",
   sp.simplify(uK.subs(J, 1) - (rho + delta)) == 0
   and sp.simplify(uK.subs([(J, 1), (delta, 1)]) - (1 + rho)) == 0)
# The durability line: u = (ρ+δ)(1+ρ)^{J−1} prices the flow-to-stock ratio
# of EVERY produced object by its (J, δ) coordinates. The consumable corner
# extends the formula below its declared J ≥ 1 domain (build lag zero, total
# wear): pay p_K now, receive the single service now — price equals rental.
# Land is the unproducible limit (J = ∞: no entry condition ever binds).
ok("U4b: the consumable corner — J = 0, δ = 1 gives u = 1 (price = rental: "
   "a good consumed on delivery); the PV condition itself degenerates to "
   "p_K = π there",
   sp.simplify(uK.subs([(J, 0), (delta, 1)]) - 1) == 0
   and sp.simplify((piK * (1 + rho) ** (1 - J) / (rho + delta))
                   .subs([(J, 0), (delta, 1)]) - piK) == 0)
# off-by-one guard: the end-of-period-discounting misread gives (ρ+δ)(1+ρ)^J,
# which differs from the derived form for every ρ > 0 — the convention bites.
ok("U5: the (ρ+δ)(1+ρ)^J misread differs from the derived u_K whenever ρ > 0",
   sp.simplify((rho + delta) * (1 + rho) ** J - uK) != 0)
# numeric tail check of the infinite sum itself (house style: symbolic + numeric)
import mpmath as mp
for (r0, d0, J0) in [(0.05, 0.10, 3), (0.12, 0.04, 7)]:
    lhs = mp.nsum(lambda s: (1 + r0) ** (-s) * (1 - d0) ** (s - J0), [J0, mp.inf])
    rhs = (1 + r0) ** (1 - J0) / (r0 + d0)
    assert abs(lhs - rhs) < 1e-12
ok("U6: infinite-sum PV matches the closed form numerically at two (ρ, δ, J)", True)

# ================================================== R: the SS recursion
# c = a c + λ w + b r + u_K p_K,  p_K = a_I c + λ_I w + b_I r,  w = γ* c.
rec = sp.solve([sp.Eq(w, c * gamma),
                sp.Eq(c, a * c + lam * w + b * r + uK * (aI * c + lamI * w + bI * r))],
               [w, c], dict=True)
assert len(rec) == 1
Den = 1 - a - lam * gamma - uK * (aI + lamI * gamma)
theta_c = (b + uK * bI) / Den
theta_w = gamma * theta_c
ok("R1: θ_c = (b + u_K b_I)/(1 − a − λγ* − u_K(a_I + λ_I γ*)) — the brief's display",
   sp.simplify(rec[0][c] - theta_c * r) == 0)
ok("R2: θ_w = γ* θ_c", sp.simplify(rec[0][w] - theta_w * r) == 0)
pK_form = aI * theta_c + lamI * theta_w + bI
ok("R3: p_K/r = a_I θ_c + λ_I θ_w + b_I",
   sp.simplify((aI * rec[0][c] + lamI * rec[0][w] + bI * r) - pK_form * r) == 0)
ok("R4: zero build recipe recovers v1's static closure c = br/(1−a−λγ*)",
   sp.simplify(rec[0][c].subs([(aI, 0), (lamI, 0), (bI, 0)])
               - b * r / (1 - a - lam * gamma)) == 0)
# capitalize-the-whole-recipe corner: no operating inputs, build recipe
# (a', λ', b') — reproduces the carrying-factor closed form with s = u_K.
ap, lp, bp, s_c = sp.symbols("a' lambda' b' s_carry", positive=True)
cap = sp.solve([sp.Eq(w, c * gamma),
                sp.Eq(c, uK * (ap * c + lp * w + bp * r))], [w, c], dict=True)
ok("R5: operating-recipe-free corner is the carrying-factor form with s = u_K "
   "(c = u_K b'r/(1 − u_K(a' + λ'γ*)))",
   len(cap) == 1 and
   sp.simplify(cap[0][c] - uK * bp * r / (1 - uK * (ap + lp * gamma))) == 0)
# uniqueness of the price block on the viable set: the linear system's
# determinant in (c, w) is the denominator, nonzero when Den > 0.
Mat = sp.Matrix([[1 - a - uK * aI, -(lam + uK * lamI)], [-gamma, 1]])
ok("R6: price block determinant = Den — unique solution on the viable set",
   sp.simplify(Mat.det() - Den) == 0)

# ==================================================== S: comparative statics
ok("S1: dθ_c/dγ* = θ_c(λ + u_K λ_I)/Den > 0 — task automation (γ*↓) cheapens "
   "the machine service in land units (the cross-effect, both channels)",
   sp.simplify(sp.diff(theta_c, gamma) - theta_c * (lam + uK * lamI) / Den) == 0)
ok("S2: dθ_w/dγ* > 0 on the viable set — automation lowers the wage's land claim",
   sp.simplify(sp.diff(theta_w, gamma)
               - theta_c * (1 + gamma * (lam + uK * lamI) / Den)) == 0)
ok("S3: dθ_c/dλ = γ*θ_c/Den > 0 and dθ_c/dλ_I = u_K γ*θ_c/Den > 0 — recursive "
   "automation through either recipe lowers c/r",
   sp.simplify(sp.diff(theta_c, lam) - gamma * theta_c / Den) == 0
   and sp.simplify(sp.diff(theta_c, lamI) - uK * gamma * theta_c / Den) == 0)
ok("S4: du_K/dJ = u_K·ln(1+ρ) > 0 — build time is dear time",
   sp.simplify(sp.diff(uK, J) - uK * sp.log(1 + rho)) == 0)
dtheta_duK = sp.simplify(sp.diff((b + s_c * bI) / (1 - a - lam * gamma - s_c * (aI + lamI * gamma)), s_c))
num_duK = bI * (1 - a - lam * gamma) + b * (aI + lamI * gamma)
ok("S5: dθ_c/du_K has sign of b_I(1−a−λγ*) + b(a_I+λ_Iγ*) > 0 on the viable "
   "set — longer J raises the land content of machine services",
   sp.simplify(dtheta_duK
               - num_duK / (1 - a - lam * gamma - s_c * (aI + lamI * gamma)) ** 2) == 0)
ok("S6: at λ = 0 the cross-effect survives through the build recipe alone "
   "(dθ_c/dγ*|_{λ=0} = θ_c u_K λ_I/Den > 0)",
   sp.simplify(sp.diff(theta_c, gamma).subs(lam, 0)
               - (theta_c * uK * lamI / Den).subs(lam, 0)) == 0)

# =================================== L: vintage ledger and the interest identity
# Stationary stock K, I = δK (K' = (1−δ)K + I). All values dated end-of-period
# (equivalently start-of-next before time passes); flows land end-of-period.
K, I = sp.symbols("K I", positive=True)
k = sp.symbols("k", integer=True, nonnegative=True)
CF = uK * pK * K - pK * (delta * K)               # rentals in, builds out
ok("L1: SS machine-sector cash = p_K K[(ρ+δ)(1+ρ)^{J−1} − δ] = ρp_K K + "
   "(ρ+δ)[(1+ρ)^{J−1} − 1]p_K K — the J = 1 corner is exactly ρp_K K",
   sp.simplify(CF - (rho * pK * K + (rho + delta) * ((1 + rho) ** (J - 1) - 1) * pK * K)) == 0
   and sp.simplify(CF.subs(J, 1) - rho * pK * K) == 0)
# ledger: installed value = π/(ρ+δ) per unit of surviving mass (first flow
# discounted once); WIP cohorts j = 0..J−2 at compounded cost p_K(1+ρ)^j.
V_inst = (uK * pK) * K / (rho + delta)
V_wip = pK * (delta * K) * sp.summation((1 + rho) ** k, (k, 0, J - 2))
W_K = sp.simplify(V_inst + V_wip)
ok("L2: the interest identity — SS machine cash = ρ·W_K with machine wealth "
   "W_K = installed PV + work in progress at compounded cost "
   "(W_K = p_K K[(1+ρ)^{J−1} + δ((1+ρ)^{J−1}−1)/ρ])",
   sp.simplify(CF - rho * W_K) == 0
   and sp.simplify(W_K - pK * K * ((1 + rho) ** (J - 1)
                                   + delta * ((1 + rho) ** (J - 1) - 1) / rho)) == 0)
ok("L3: zero NPV in the ledger — a vintage's PV of rentals at install equals "
   "its compounded build cost, so 100%-external finance at ρ leaves exactly "
   "zero SS machine cash to households (the two conventions coincide at rest)",
   sp.simplify(uK * pK * (1 + rho) / (rho + delta) - pK * (1 + rho) ** J) == 0)
ok("L4: W_K ≥ p_K K with equality iff J = 1 — the gestation float is the "
   "excess (W_K/p_K K − 1 vanishes at J = 1, is positive at J = 2 and J = 4)",
   sp.simplify(W_K.subs(J, 1) - pK * K) == 0
   and all(sp.simplify(sp.factor(W_K / (pK * K) - 1).subs(
       [(rho, sp.Rational(1, 20)), (delta, sp.Rational(1, 10)), (J, jv)])) > 0
       for jv in (2, 4)))

# ======================================= V: the land-viability named condition
# Land clearing T = bX + b_I I + α·Inc/r with Inc = wN_a + rT solves to
# r[(1−α)T − (bX + b_I I)] = α w N_a  —  r > 0  iff  (1−α)T > bX + b_I I.
X, Y, Na, Inc = sp.symbols("X Y N_a Inc", positive=True)
r_land = sp.solve(sp.Eq(T, b * X + bI * I + alpha * (w * Na + r * T) / r), r)
ok("V1: r = α w N_a / [(1−α)T − (bX + b_I I)] — caution (ii)'s condition "
   "(1−α)T > bX + b_I I is exactly the r > 0 requirement",
   len(r_land) == 1
   and sp.simplify(r_land[0] - alpha * w * Na / ((1 - alpha) * T - b * X - bI * I)) == 0)

# ============================== E: the equivalence lemma, flat case (symbolic)
# Sequence economy of brief §3.5 at constants, flat schedule γ(x) = γ̄ with
# γ_L constant (L̄ = 1/γ_L), machine-task measure m_x interior. Direction 1:
# constants ⇒ the §4 recursion. Direction 2: the recursion's solution extends
# to a full constant sequence (quantities positive, PV free entry, Walras).
m_x = sp.symbols("m_x", positive=True)
cF = gamL / gambar                                  # from 1 = c·γ̄L̄, L̄ = 1/γ_L
wF = gambar * cF
ok("E1: flat unit-cost condition pins c = 1/(γ̄L̄) for EVERY interior split "
   "(the split drops out: CM at rest), and w = γ̄c = 1/L̄",
   sp.simplify(cF * (m_x * gambar / gamL) + wF * (1 - m_x) / gamL - 1) == 0
   and sp.simplify(wF - gamL) == 0)
DenF = Den.subs(gamma, gambar)
theta_cF = theta_c.subs(gamma, gambar)
rF = sp.simplify(cF / theta_cF)
ok("E2: free entry at constants forces r = c/θ_c(γ̄) — the sequence economy's "
   "constant prices ARE the §4 recursion's (the lemma's price half)",
   sp.simplify(cF - a * cF - lam * wF - b * rF
               - uK * (aI * cF + lamI * wF + bI * rF)) == 0)
# quantity half: X(1−a−a_Iδ) = (m_xY)γ̄/γ_L; N = (Y−m_xY)/γ_L + (λ+λ_Iδ)X;
# land clearing pins X; all solved in closed form, Walras then verified.
XF = ((1 - alpha) * T - alpha * wF * N / rF) / (b + bI * delta)
MYF = XF * (1 - a - aI * delta) * gamL / gambar
YF = gamL * (N - (lam + lamI * delta) * XF) + MYF
mF = sp.simplify(MYF / YF)
IncF = wF * N + rF * T
NXF = uK * (aI * cF + lamI * wF + bI * rF) * XF - (aI * cF + lamI * wF + bI * rF) * delta * XF
ok("E3: Walras closes at constants WITH net exports — Y = (1−α)Inc + NX "
   "identically in all parameters (caution (i) resolved: goods clearing "
   "holds with Inc = wN + rT and NX = πK − p_K I)",
   sp.simplify(YF - (1 - alpha) * IncF - NXF) == 0)
# named interior conditions (the lemma's existence clause), verified to be
# exactly what positivity of the closed forms requires at a numeric point
# INSIDE the region and violated OUTSIDE it:
flatpt = {a: sp.Rational(1, 2), lam: sp.Rational(1, 10), b: sp.Rational(1, 5),
          aI: sp.Rational(1, 10), lamI: sp.Rational(1, 5), bI: sp.Rational(1, 50),
          rho: sp.Rational(1, 20), delta: sp.Rational(1, 10), J: 3,
          gambar: 3, gamL: 1, alpha: sp.Rational(3, 10), N: 1}
# The interior region is NARROW: the worked dials use T = 3.8, chosen so that
# every experiment endpoint (γ̄ ∈ {3, 2.8} × J ∈ {1, 2, 3, 4}) stays interior.
vals_int = {T: sp.Rational(19, 5)}
XF5, MYF5, YF5, mF5 = [sp.simplify(e.subs({**flatpt, **vals_int})) for e in (XF, MYF, YF, mF)]
ok("E4: interior flat SS exists at the worked dials (T = 3.8): X > 0, "
   "0 < m < 1, labor not exhausted by operation ((λ+λ_Iδ)X < N)",
   XF5 > 0 and 0 < mF5 < 1
   and (lam + lamI * delta).subs(flatpt) * XF5 < 1)
ok("E4b: the experiment endpoints stay interior at T = 3.8 — γ̄ = 2.8 at "
   "J ∈ {1, 2, 3, 4} all keep 0 < m < 1 and (λ+λ_Iδ)X < N",
   all(0 < sp.simplify(mF.subs({**flatpt, **vals_int, gambar: sp.Rational(14, 5), J: Jv})) < 1
       and (lam + lamI * delta).subs(flatpt)
       * sp.simplify(XF.subs({**flatpt, **vals_int, gambar: sp.Rational(14, 5), J: Jv})) < 1
       for Jv in (1, 2, 3, 4)))
ok("E5: at T = 10 the SAME dials violate interiority (m > 1: labor scarcer "
   "than the land bound wants) — the interior conditions are real, not "
   "decorative; the flat case has corner regimes the solver must detect",
   sp.simplify(mF.subs({**flatpt, T: 10})) > 1)

# ------------------- T1 (early): the b_I = 0 flat transition in closed form
# With b_I = 0 and the external-finance convention, the perfect-foresight
# path after an unanticipated permanent γ̄_0 → γ̄_1 is EXACT:
#   r_t = r_old for t < J (the old pipeline holds K at K_old and land
#   clearing does not move — w is γ̄-invariant), r_t = r_new for t ≥ J;
#   K_t = K_old for t < J, K_new from t = J on (I_0 = K_new − (1−δ)K_old ≥ 0
#   is a named condition); π is a rectangle: π_win = c_1(1−a) − λw − b r_old
#   on the window, u_K p_K,new after. Q_0 has the closed form below.
g0_, g1_ = sp.symbols("gammabar_0 gammabar_1", positive=True)
bI0 = {bI: 0}
cS = gamL / gambar
wS = gamL
rS = sp.simplify((cS / theta_c.subs(gamma, gambar)).subs(bI0))
XS = sp.simplify((((1 - alpha) * T - alpha * wS * N / rS) / (b + bI * delta)).subs(bI0))
r0_, r1_ = rS.subs(gambar, g0_), rS.subs(gambar, g1_)
K0_, K1_ = XS.subs(gambar, g0_), XS.subs(gambar, g1_)
ok("T1a: window land clearing is the OLD steady state's — w is γ̄-invariant "
   "and K is pipeline-frozen, so T − bK_old − αw N/r_old = 0 survives the "
   "shock unchanged (the rent is frozen for exactly J periods)",
   sp.simplify((1 - alpha) * T - b * K0_ - alpha * wS * N / r0_) == 0)
pK1 = (aI * cS + lamI * wS).subs(gambar, g1_)
pi_win = sp.simplify(cS.subs(gambar, g1_) * (1 - a) - lam * wS - b * r0_)
pi_new = sp.simplify(uK * pK1)
ok("T1b: the window rentals exceed the new steady-state rental exactly when "
   "the rent rises across the transition (π_win − π_new = b(r_new − r_old))",
   sp.simplify((pi_win - pi_new) - b * (r1_ - r0_)) == 0)
qqJ = ((1 - delta) / (1 + rho)) ** J
Q0_closed = sp.simplify((pi_win * (1 - qqJ) + pi_new * qqJ) / ((rho + delta) * pK1))
kk = sp.symbols("kk", integer=True, nonnegative=True)


def conv_branch(e):
    """Select Piecewise branches whose condition holds on the model domain
    (0 < δ < 1, ρ > 0 — the geometric-tail condition of U1). The condition is
    verified, not assumed: it must evaluate True at the sample rationals."""
    e = sp.piecewise_fold(e)
    while isinstance(e, sp.Piecewise):
        cond = e.args[0][1]
        assert cond == True or bool(cond.subs({delta: sp.Rational(1, 10),
                                               rho: sp.Rational(1, 20)}))
        e = e.args[0][0]
    return e


V0_win = sp.summation((1 + rho) ** (-(kk + 1)) * (1 - delta) ** kk * pi_win, (kk, 0, J - 1))
V0_tail = conv_branch(sp.summation((1 + rho) ** (-(kk + 1)) * (1 - delta) ** kk * pi_new,
                                   (kk, J, sp.oo)))
V0_sum = V0_win + V0_tail
# (sympy cannot normalize (−1)^J(δ−1)^J → (1−δ)^J at symbolic integer J, so
# the sum identity is verified at explicit J, symbolic in everything else.)
ok("T1c: Q_0 closed form — the PV of the rectangle over replacement cost is "
   "Q_0 = [π_win(1−qq^J) + π_new qq^J]/((ρ+δ)p_K), qq = (1−δ)/(1+ρ) "
   "(verified at J ∈ {1, 2, 3, 5, 8}, symbolic in all other parameters)",
   all(sp.simplify(conv_branch(sp.simplify((V0_sum / pK1 - Q0_closed).subs(J, jv)))) == 0
       for jv in (1, 2, 3, 5, 8)))
ok("T1d: steady-state Q is NOT 1 — installed capacity carries the gestation "
   "float, Q̄ = π_new/((ρ+δ)p_K) = (1+ρ)^{J−1} (Hayashi's Q = 1 is the J = 1 "
   "corner); the windfall is the excess over THAT: "
   "Q_0 − (1+ρ)^{J−1} = (1−qq^J)·b·(r_new − r_old)/((ρ+δ)p_K)",
   sp.simplify(pi_new / ((rho + delta) * pK1) - (1 + rho) ** (J - 1)) == 0
   and sp.simplify((Q0_closed - (1 + rho) ** (J - 1)) * (rho + delta) * pK1
                   - (1 - qqJ) * b * (r1_ - r0_)) == 0)

# =============== EJ: the equivalence lemma, sloped case (A-joint instantiated)
# check_pinning's Appendix-A joint system extended with the build recipe:
# γ(x) = 1+4x, γ_L = 1, a = 0.5, λ = 0.1, b = 0.2, T = 10, α = 0.3, N = 1,
# s0 = 1, h_e = 0.5, s̲ = 0.2  +  (a_I, λ_I, b_I) = (0.1, 0.2, 0.02),
# (ρ, δ, J) = (0.05, 0.10, 3). Free entry replaces flow zero-profit:
# π = u_K p_K. Build → 0 must reproduce check_pinning's root exactly.
aJ_, lamJ_, bJ_, TJ_, alJ_, NJ_ = 0.5, 0.1, 0.2, 10.0, 0.3, 1.0
s0J_, heJ_, sdJ_ = 1.0, 0.5, 0.2
uKn = float((rho + delta).subs(flatpt) * (1 + rho).subs(flatpt) ** 2)  # (ρ+δ)(1+ρ)^{J−1}

def joint_dyn(xs, aI_=0.1, lamI_=0.2, bI_=0.02, dl=0.10, uk=uKn):
    g = 1 + 4 * xs
    Ig = xs + 2 * xs * xs                          # ∫γ on [0, xs]
    cJ = 1.0 / (g * (1 - xs) + Ig)                 # unit cost = 1
    wJ = g * cJ                                    # the margin
    DenJ = 1 - aJ_ - lamJ_ * g - uk * (aI_ + lamI_ * g)
    rJ = cJ * DenJ / (bJ_ + uk * bI_)              # free entry π = u_K p_K
    Y = NJ_ / ((1 - xs) + (lamJ_ + lamI_ * dl) * Ig / (1 - aJ_ - aI_ * dl))
    Xs = Y * Ig / (1 - aJ_ - aI_ * dl)             # services incl. build use
    land = (bJ_ + bI_ * dl) * Xs + alJ_ * (wJ * NJ_ + rJ * TJ_) / rJ
    return land - TJ_, wJ, cJ, rJ, Y, Xs, DenJ

# The build recipe shrinks the viable set: Den(γ(x)) > 0 now dies at
# x ≈ 0.658 (statically it died at x = 1). Uniqueness is claimed and checked
# ON THE VIABLE SET — beyond it r < 0 and the residual's sign is meaningless.
grid = [i / 1000.0 for i in range(1, 990)]
vgrid = [x for x in grid if joint_dyn(x)[6] > 0]
signs = [joint_dyn(x)[0] > 0 for x in vgrid]
flips = sum(1 for i in range(1, len(vgrid)) if signs[i] != signs[i - 1])
ok("EJ1: extended joint system — land residual has exactly one sign change "
   "on the viable set (Den > 0, which now binds at x ≈ 0.658, not 1)",
   flips == 1 and vgrid[-1] < 0.67)
lo, hi = vgrid[0], vgrid[-1]
for _ in range(200):
    mid = (lo + hi) / 2
    if (joint_dyn(lo)[0] > 0) == (joint_dyn(mid)[0] > 0):
        lo = mid
    else:
        hi = mid
xsJ = (lo + hi) / 2
residJ, wJn, cJn, rJn, YJn, XJn, DenJn = joint_dyn(xsJ)
ok("EJ2: land market clears at the root", abs(residJ) < 1e-9)
ok("EJ3: dynamic viability Den > 0 at the root", DenJn > 0)
pKn = 0.1 * cJn + 0.2 * wJn + 0.02 * rJn
IncJn = wJn * NJ_ + rJn * TJ_
NXJn = uKn * pKn * XJn - pKn * 0.10 * XJn
ok("EJ4: goods clear by Walras WITH net exports at the root "
   "(Y = (1−α)Inc + πK − p_K I)",
   abs(YJn - (1 - alJ_) * IncJn - NXJn) < 1e-8)
ok("EJ5: full participation consistent at the root (w > max(s0 − q h_e, s̲))",
   wJn > max(s0J_ - rJn * heJ_, sdJ_))
ok("EJ6: the recursion holds at the root — c/r = θ_c(γ(x*)) with the build "
   "recipe (the lemma's price half, sloped)",
   abs(cJn / rJn - float(theta_c.subs({**flatpt, gamma: 1 + 4 * xsJ}))) < 1e-9)
# nesting gate: build recipe → 0 reproduces check_pinning's A-joint root.
def joint_static(xs):
    g = 1 + 4 * xs
    Ig = xs + 2 * xs * xs
    cJ = 1.0 / (g * (1 - xs) + Ig)
    wJ = g * cJ
    rJ = cJ * (1 - aJ_ - lamJ_ * g) / bJ_
    Y = NJ_ / ((1 - xs) + lamJ_ * Ig / (1 - aJ_))
    Xs = Y * Ig / (1 - aJ_)
    return (bJ_ * Xs + alJ_ * (wJ * NJ_ + rJ * TJ_) / rJ - TJ_, wJ, cJ, rJ, Y, Xs)
lo, hi = 0.001, 0.989
for _ in range(200):
    mid = (lo + hi) / 2
    if (joint_static(lo)[0] > 0) == (joint_static(mid)[0] > 0):
        lo = mid
    else:
        hi = mid
xs0 = (lo + hi) / 2
lo, hi = 0.001, 0.989
for _ in range(200):
    mid = (lo + hi) / 2
    if (joint_dyn(lo, 0, 0, 0, 0.10)[0] > 0) == (joint_dyn(mid, 0, 0, 0, 0.10)[0] > 0):
        lo = mid
    else:
        hi = mid
xs00 = (lo + hi) / 2
st0, dyn0 = joint_static(xs0), joint_dyn(xs00, 0, 0, 0, 0.10)
ok("EJ7: build recipe → 0 reproduces check_pinning's A-joint root "
   "(x*, w, c, r, Y, X all within 1e-9)",
   abs(xs0 - xs00) < 1e-9
   and all(abs(s - d) < 1e-9 for s, d in zip(st0[1:6], dyn0[1:6])))

# ============================================== P: participation invariance
q_, hw, he, s0, sund = sp.symbols("q h_w h_e s_0 s_under", positive=True)
ok("P1: with h_w = h_e the exit comparison is q-free on the s0 branch — "
   "(w − q h) − (s0 − q h) = w − s0 identically",
   sp.simplify((w - q_ * hw) - (s0 - q_ * hw) - (w - s0)) == 0)
# NOTE (drafting caveat, carried to the veto list): on the dependency-floor
# branch the cancellation needs the floor life to occupy the same land; if s̲
# is land-free the work side still carries q h_w. §6 must state the branch.
Pidx = 1 ** (1 - alpha) * q_ ** alpha              # P = p^{1−α} r^α at p = 1
ok("P2: rigidity half — the working life's real value degrades smoothly as "
   "q^{−α} while a rigid-h_e exit hits zero at finite q = s0/h_e",
   sp.simplify(sp.diff(w / Pidx, q_) + alpha * w * q_ ** (-alpha - 1)) == 0
   and sp.solve(sp.Eq(s0 - q_ * he, 0), q_) == [s0 / he])
theta_e = sp.symbols("theta_e", positive=True)
ok("P3: funding source — a rent-funded exit s0 = θ_e r holds its land claim "
   "(s0/r constant in γ*); a wage-funded one inherits θ_w and shrinks",
   sp.diff(theta_e, gamma) == 0
   and sp.simplify(sp.diff(theta_w, gamma)) != 0)
tauR, dd = sp.symbols("tau_R d", positive=True)
ok("P4: the dividend d = τ_R R/N cancels from the participation comparison "
   "and is itself a land claim (d/r = τ_R T/N, γ*-invariant)",
   sp.simplify((w + dd) - (s0 + dd) - (w - s0)) == 0
   and sp.diff(tauR * T / N, gamma) == 0)

# ========================================= F: the fork as coefficient ratios
mj, lj, bj = sp.symbols("m_j l_j b_j", nonnegative=True)
theta_j = mj * theta_c + lj * theta_w + bj
ok("F1: the real wage in good j is the pure coefficient ratio θ_w/θ_j — "
   "r cancels from w/p_j identically",
   sp.simplify(theta_w * r / (theta_j * r) - theta_w / theta_j) == 0)
kprop = sp.symbols("k_prop", positive=True)
ok("F2: Caselli–Manning is θ_j ∝ θ_w — the ratio is invariant to γ*, λ, J",
   sp.simplify(theta_w / (kprop * theta_w) - 1 / kprop) == 0)
theta_c_at0 = theta_c.subs(gamma, 0)
ok("F3: the fork — θ_c stays finite as γ* → 0 (given viability at γ* = 0), "
   "so θ_w → 0 and w/p_j ≤ θ_w/b_j → 0 for any good with b_j > 0; "
   "the θ = 1 endpoint (pure location) is the worst case",
   sp.simplify(theta_c_at0 - (b + uK * bI) / (1 - a - uK * aI)) == 0
   and sp.limit(theta_w.subs({aI: 0, lamI: 0, bI: 0}), gamma, 0) == 0)
theta_p = gambar * Lbar * theta_c.subs(gamma, gambar)
ok("F4: flat limit — θ_w/θ_p = 1/L̄ exactly (CM restated in coefficients)",
   sp.simplify(theta_w.subs(gamma, gambar) / theta_p - 1 / Lbar) == 0)

# ============================ T4 (early): entry-margin tax algebra, no solver
tK = sp.symbols("tau_K", positive=True)
rec_tax = sp.solve([sp.Eq(w, c * gamma),
                    sp.Eq(c, a * c + lam * w + b * r
                          + (uK / (1 - tK)) * (aI * c + lamI * w + bI * r))],
                   [w, c], dict=True)
theta_c_tax = sp.simplify(rec_tax[0][c] / r)
ok("T4a: an anticipated rental tax on NEW capacity scales the user cost by "
   "1/(1−τ_K) and raises θ_c — the entry margin is distorted",
   sp.simplify(theta_c_tax
               - ((b + uK / (1 - tK) * bI)
                  / (1 - a - lam * gamma - uK / (1 - tK) * (aI + lamI * gamma)))) == 0
   and sp.simplify(sp.diff(theta_c_tax, tK).subs(
       {**{k2: v for k2, v in flatpt.items() if k2 not in (gambar, gamL, alpha, N)},
        gamma: 3, tK: sp.Rational(1, 5)})) > 0)
ok("T4b: a one-time levy on stock in place enters no entry condition — the "
   "PV condition for new units is levy-free by construction (sunk windfall; "
   "the θ's carry no term in it)",
   sp.simplify(theta_c - theta_c_tax.subs(tK, 0)) == 0)
ok("T4c: the rent tax τ_R appears in NO production price — θ_c, θ_w, p_K/r "
   "are τ_R-free identically (land supply is the fixed factor)",
   all(tauR not in e.free_symbols for e in (theta_c, theta_w, pK_form)))

# ================================================= N: the new-task condition
t_, eta_, Del0 = sp.symbols("t eta Delta_0", positive=True)
gmax = gambar + Del0 * eta_ ** t_                   # support sup, collapsing
gth = gamma * theta_c                               # g(γ) = γθ_c(γ) = θ_w
ok("N1: θ_w is increasing in γ* (S2), so reinstatement at γ*_t = sup-support "
   "keeps w/r above the flat value at every finite t — a transitional "
   "stabilizer, not a rescue",
   sp.simplify(sp.diff(gth, gamma)
               - theta_c * (1 + gamma * (lam + uK * lamI) / Den)) == 0)
ok("N2: if the support sup collapses to γ̄ (here γ̄ + Δ0 η^t, 0 < η < 1), the "
   "flat limit still arrives: lim γ*_t = γ̄",
   sp.limit(gmax.subs(eta_, sp.Rational(1, 2)), t_, sp.oo) == gambar)

# ------------------------------------------------ solver targets (hard gate)
# The dynamics code (code/dynamics/) must reproduce these steady states
# before any transition experiment runs. Written by this check, read by the
# solver's gate — no import coupling.
targets = {
    "flat": {
        "params": {"a": 0.5, "lam": 0.1, "b": 0.2, "aI": 0.1, "lamI": 0.2,
                   "bI": 0.02, "rho": 0.05, "delta": 0.10, "J": 3,
                   "gambar": 3.0, "gamL": 1.0, "alpha": 0.3, "T": 3.8, "N": 1.0},
        "c": float(cF.subs(flatpt)), "w": float(wF.subs(flatpt)),
        "r": float(rF.subs(flatpt)), "X": float(XF5), "Y": float(YF5),
        "m": float(mF5), "uK": uKn,
    },
    "sloped": {
        "params": {"a": aJ_, "lam": lamJ_, "b": bJ_, "aI": 0.1, "lamI": 0.2,
                   "bI": 0.02, "rho": 0.05, "delta": 0.10, "J": 3,
                   "T": TJ_, "alpha": alJ_, "N": NJ_,
                   "schedule": "1+4x, gamma_L = 1",
                   "s0": s0J_, "he": heJ_, "sd": sdJ_},
        "xstar": xsJ, "c": cJn, "w": wJn, "r": rJn, "Y": YJn, "X": XJn,
        "pK": pKn, "uK": uKn,
    },
}
out = os.path.join(os.path.dirname(__file__), "dynamics_ss_targets.json")
with open(out, "w") as f:
    json.dump(targets, f, indent=2)
print(f"\n  targets written: {out}")

print(f"\nALL GREEN ({len(GREEN)} checks)")
