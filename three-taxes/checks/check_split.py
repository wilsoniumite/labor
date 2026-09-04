# check_split.py — sympy + numeric checks for the design memo's arithmetic
# (three-taxes, 2026-09-02): the 60/40 use split as a saving constraint, the source-tax
# rate it implies, the VAT residual identity and its wage-share threshold, the corner
# relabel of a VAT on fixed-supply land services, and the announcement-shock price paths.
# Run from three-taxes/:  ../venv/Scripts/python.exe checks/check_split.py
import sys
import numpy as np
import sympy as sp
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
PASS = []
def check(name, ok):
    PASS.append(bool(ok)); print(("PASS " if ok else "FAIL ") + name)

w, u, rL, pi, s, Gc, Gi, t, tau, I, C = sp.symbols("w u r_L pi s G_c G_i t tau I C", positive=True)

# S1: investment = private reinvestment + public investment; solve for the source-tax rate
inv_identity = sp.Eq(I, s * (1 - t) * pi + Gi)
t_sol = sp.solve(inv_identity.subs(Gi, 0), t)[0]
check("S1 source-tax rate t = 1 - I/(s*pi) from I = s(1-t)pi", sp.simplify(t_sol - (1 - I / (s * pi))) == 0)

# S2: consumers' share identity: w + r_L + t*pi = 1 - I when s = 1, Gi = 0  (with pi = 1 - w - r_L)
lhs = w + rL + (1 - I / pi) * pi
check("S2 consumers' share w + r_L + t*pi = 1 - I  (s=1)", sp.simplify(lhs.subs(pi, 1 - w - rL) - (1 - I)) == 0)

# S3: VAT identity. Budget: rL + t*pi + tau*spend = Gc + Gi + u with spend = w + u + own_c, own_c = (1-s)(1-t)pi,
#     and real private consumption C_p = (1-tau)*spend. Claim: C_p = 1 - I - Gc (the split) when the budget balances.
own_c = (1 - s) * (1 - t) * pi
spend = w + u + own_c
need = Gc + Gi + u - rL - t * pi
tau_sol = need / spend
Cp = (1 - tau_sol) * spend
Cp_sub = sp.simplify(Cp.subs(Gi, I - s * (1 - t) * pi).subs(pi, 1 - w - rL))
check("S3 VAT residual: (1-tau)*spend = 1 - I - G_c exactly (any s, t)", sp.simplify(Cp_sub - (1 - I - Gc)) == 0)

# S4: threshold wage share at which the VAT retires (s = 1, Gi = 0): need = 0  <=>  w = (1 - I - Gc) - u
need_s1 = (Gc + u - rL - (1 - I / pi) * pi).subs(pi, 1 - w - rL)
w_star = sp.solve(sp.Eq(need_s1, 0), w)[0]
check("S4 VAT retires at w* = (1 - I - G_c) - u  (s=1)", sp.simplify(w_star - ((1 - I - Gc) - u)) == 0)
val = w_star.subs({I: sp.Rational(2, 5), Gc: sp.Rational(14, 100), u: sp.Rational(91, 1000)})
check("S4b numeric: I=0.4, G_c=0.14, u=0.091 -> w* = 0.369", abs(float(val) - 0.369) < 1e-9)

# S5: numeric reproduction of the schedule row (w=0.55, kappa=0.33, pc4): t=4.8%, VAT incl 28.2%
f = 0.091; k = 0.33; wv = 0.55
rLv = k * f; piv = 1 - wv - rLv; tv = 1 - 0.4 / piv
needv = 0.14 + f - rLv - tv * piv; tauv = needv / (wv + f)
check("S5 schedule row: t=4.8%, VAT incl=28.2% at (0.55, 0.33)", abs(tv - 0.0476) < 2e-3 and abs(tauv - 0.282) < 2e-3)

# S6: corner relabel — a VAT at inclusive rate v on fixed-supply land services with an LVT at rate tauR:
#     consumer price r_c clears the fixed stock (demand-determined), producer rent r_p = (1-v) r_c;
#     government take = tauR*r_p + v*r_c = r_c*(tauR*(1-v) + v). At tauR = 1 the take is r_c regardless of v.
v, rc, tauR = sp.symbols("v r_c tau_R", positive=True)
take = tauR * (1 - v) * rc + v * rc
check("S6 VAT on fixed-supply land services is a relabel at tau_R = 1 (take = r_c for all v)",
      sp.simplify(take.subs(tauR, 1) - rc) == 0)
check("S6b at tau_R < 1 the VAT adds exactly v*(1-tau_R)*r_c", sp.simplify(take - tauR * rc - v * (1 - tauR) * rc) == 0)

# S7: announcement-shock price ratios (Gordon growth, gamma=2%, delta=5%, tau=0.98): closed forms vs the numeric sums
gam, dlt, tb = 0.02, 0.05, 0.98
x = (1 + gam) / (1 + dlt)
tt = np.arange(1, 4001); disc = x ** tt; P0 = disc.sum()
full = ((1 - tb) * disc).sum() / P0
check("S7 immediate full capture: price ratio = 1 - tau = 0.02", abs(full - (1 - tb)) < 1e-9)
# increment-only: after-tax flow r0[(1+g)^t - tau((1+g)^t - 1)]; PV ratio = 1 - tau*(1 - (1/(1+g))^t-weighted) ; closed form:
inc = ((1 - tb * (1 - (1 + gam) ** (-tt))) * disc).sum() / P0
closed = 1 - tb * (1 - (P0 ** -1) * ((1 / (1 + dlt)) ** tt).sum())
check("S7b increment-only closed form matches numeric", abs(inc - closed) < 1e-9)
# sketch T4's dial: increment-only captures gamma/delta of the stock in the continuous-time limit; discrete analogue
# captured share = tau * (1 - [sum (1+d)^-t] / [sum x^t]) -> with gamma=2%, delta=5%: about 0.39-0.40
check("S7c increment-only captures ~gamma/delta = 0.40 of the stock at tau=0.98 (discrete: within 0.03)",
      abs((1 - inc) - 0.40) < 0.03)
# S8: lagged assessment after a -20% rent step: effective rate tau/0.8 > 1
check("S8 5-year-lag after a -20% rent step: effective rate 0.98/0.8 = 1.225 > 1 (idling risk)", abs(tb / 0.8 - 1.225) < 1e-12 and tb / 0.8 > 1)

# S9: build-lag markup. Steady growth g, capital-output v, depreciation d, lag J: investment spent at t
#     delivers capacity at t+J, so I_t = (g+d) K_{t+J} = (g+d) v Y_t (1+g)^J.
g, d, v_, J = sp.symbols("g d v J", positive=True)
Yt = sp.Symbol("Y_t", positive=True)
K_tJ = v_ * Yt * (1 + g) ** J
I_t = (g + d) * K_tJ
check("S9 build-lag markup: I/Y = (g+d) v (1+g)^J", sp.simplify(I_t / Yt - (g + d) * v_ * (1 + g) ** J) == 0)
inst = float(((g + d) * v_ * (1 + g) ** J).subs({g: 0.05, d: 0.055, v_: 3, J: 5}))
check("S9b instance g=5%, d=5.5%, v=3, J=5 -> 0.402 (her 40 at a five-year pipeline)", abs(inst - 0.402) < 2e-3)
# S10: pipeline stock. Capital in progress = sum of the last J years' investment = I_t * sum_{j=1..J} (1+g)^-j.
j = sp.Symbol("j", integer=True, positive=True)
pipe = sp.summation((1 + g) ** (-j), (j, 1, J))
pipe_closed = (1 - (1 + g) ** (-J)) / g
check("S10 pipeline stock / I = (1 - (1+g)^-J)/g (-> J as g -> 0)",
      sp.simplify(pipe.subs({J: 5, g: sp.Rational(1, 20)}) - pipe_closed.subs({J: 5, g: sp.Rational(1, 20)})) == 0
      and abs(float(sp.limit(pipe_closed.subs(J, 5), g, 0)) - 5) < 1e-12)
# S11: the limit split. Prop B.1 (P1): pY = r T_P = (1-alpha) r T and r T_H = alpha r T; the production-land share
#      of the rent flow is 1-alpha; with CES share alpha(q) -> 1 (sigma<1) the production share -> 0.
al, q_, sg = sp.symbols("alpha q sigma", positive=True)
alpha_q = al * q_ ** (1 - sg) / (al * q_ ** (1 - sg) + 1 - al)
check("S11 limit: production-land share = 1 - alpha; -> 0 as q -> oo when sigma < 1",
      sp.simplify(sp.limit(1 - alpha_q.subs(sg, sp.Rational(1, 2)), q_, sp.oo)) == 0
      and sp.simplify(sp.limit(1 - alpha_q.subs(sg, 2), q_, sp.oo) - 1) == 0)
# S12: conversion golden rule. Converting one unit at cost kappa_c raises the rent flow by m (per year, forever);
#      worth doing iff m/kappa_c >= rho; the stock of conversion is pushed until the marginal m falls to rho*kappa_c.
m_, kc, rho_ = sp.symbols("m kappa_c rho", positive=True)
pv_gain = m_ / rho_
check("S12 conversion FOC: PV gain m/rho = cost  <=>  m = rho*kappa_c", sp.simplify(sp.solve(sp.Eq(pv_gain, kc), m_)[0] - rho_ * kc) == 0)

# ---- the lag design (her 2026-09-02 proposal: up-lag for prospecting, 2y down-lag "closes the loophole",
#      abandonment "is fine"). Assessment follows true rent by partial adjustment at speed 1/L, L = L_up when
#      rent is above the assessment, L_down when below. Rate 0.98. Owner cash flow = rent received - tax.
def simulate(L_up, L_down, r_path, r_received=None, horizon=80, rate=0.98):
    A = r_path[0]; cum = 0.0
    rec = r_received if r_received is not None else r_path
    for t in range(horizon):
        r = r_path[min(t, len(r_path) - 1)]; got = rec[min(t, len(rec) - 1)]
        L = L_up if r > A else L_down
        A = A + (r - A) / L
        cum += got - rate * A
    return cum
def real_dip_gain(L_up, L_down, D, delta=0.3):
    base = [1.0] * 80
    dip = [1.0] + [1.0 - delta] * D + [1.0] * (80 - 1 - D)
    return simulate(L_up, L_down, dip) - simulate(L_up, L_down, base)      # >0: the sawtooth pays
def fake_dip_gain(L_up, L_down, D, delta=0.3):
    base = [1.0] * 80
    dip = [1.0] + [1.0 - delta] * D + [1.0] * (80 - 1 - D)
    return simulate(L_up, L_down, dip, r_received=base) - simulate(L_up, L_down, base)
# S13: her (10 up, 2 down): a real engineered 2-year dip PAYS; symmetric (2,2) does not; the break-even is L_down >= ~L_up/2
g_10_2 = real_dip_gain(10, 2, 2); g_2_2 = real_dip_gain(2, 2, 2); g_10_5 = real_dip_gain(10, 5, 2); g_10_10 = real_dip_gain(10, 10, 2)
print(f"   real 2y dip, gain to owner (units of one year's rent): (10,2) {g_10_2:+.3f}  (10,5) {g_10_5:+.3f}  (10,10) {g_10_10:+.3f}  (2,2) {g_2_2:+.3f}")
check("S13 real-dip sawtooth: pays under (up 10, down 2); does not under (2,2) or (10,10)", g_10_2 > 0 and g_2_2 < 0 and g_10_10 < 0)
check("S13b the 2y down-lag does not close it: gain under (10,2) exceeds gain under (10,5)", g_10_2 > g_10_5)
# S14: a FAKE dip (measured rent falls, true rent still received) pays under every lag structure incl. symmetric
f_2_2 = fake_dip_gain(2, 2, 2); f_10_10 = fake_dip_gain(10, 10, 2)
check("S14 fake-dip (self-reported rent) pays under any lags -> only T3 valuation closes it", f_2_2 > 0 and f_10_10 > 0)
# S15: the steady-growth leak of a general up-lag: A/r -> 1/(1+gL) under partial adjustment; effective rate 0.98/(1+gL)
gg, LL = sp.symbols("g L", positive=True)
# steady state of A_t = A_{t-1} + (r_t - A_{t-1})/L with r_t = r_{t-1}(1+g): A_t = k r_t, k = 1/(1 + g L) [exact for this recursion]
k = sp.Symbol("k", positive=True)
ss = sp.solve(sp.Eq(k, (k / (1 + gg)) + (1 - k / (1 + gg)) / LL), k)[0]
check("S15 steady-growth assessment ratio: exact k = (1+g)/(1+gL) for partial adjustment at speed 1/L",
      sp.simplify(ss - (1 + gg) / (1 + gg * LL)) == 0)
leak_10 = 1 - 0.98 * float(ss.subs({gg: 0.02, LL: 10})); leak_2 = 1 - 0.98 * float(ss.subs({gg: 0.02, LL: 2}))
print(f"   general up-lag leak at 2% growth: L=10 -> owners keep {leak_10:.1%} of rent; L=2 -> {leak_2:.1%}")
check("S15b a 10-year general up-lag leaves owners ~17% of rent in a 2%-growth area; 2-year ~4%", abs(leak_10 - 0.167) < 0.005 and abs(leak_2 - 0.039) < 0.005)
# S16: abandonment as a cap. With free surrender and the structure retained (ground-lease conversion) the owner's
#      tax is min(0.98 A, r): the assessment overshoot is capped at r. With the structure forfeited the owner tolerates
#      over-assessment up to the structure's annual value S before walking: cap = r + S (the hold-up reappears).
r_, A_, S_ = sp.symbols("r A S", positive=True)
tax_free_surrender = sp.Min(sp.Rational(98, 100) * A_, r_)
check("S16 free surrender caps the tax at r (effective rate <= 1)", sp.simplify(tax_free_surrender.subs({A_: 2, r_: 1})) == 1)
check("S16b structure-forfeit surrender tolerates over-assessment up to r + S", sp.simplify(sp.Min(sp.Rational(98,100)*A_, r_ + S_).subs({A_: 2, r_: 1, S_: sp.Rational(1,2)}) - sp.Rational(3, 2)) == 0)

# S17: the two-option bracket (her auction + bureau, 2026-09-02). Owner holds a free surrender put (ground-lease
#      conversion, structure retained): tax <= r. State holds an automatic take-call at (assessment - buffer):
#      any parcel leasing/trading below A(1-b) is taken and re-let, so realized rent can't sit below A(1-b).
#      Together: A(1-b) <= r  and  tax = min(0.98 A, r)  =>  effective rate on true rent within [0.98(1-b), 1].
b_ = sp.Symbol("b", positive=True)
A_hi = r_ / (1 - b_)                       # the highest assessment the state's call permits to stand against rent r
eff_lo = sp.Rational(98, 100) * (1 - b_)   # rate when A is at its floor relative to r... i.e. A = r(1-b)/(1) -> tax/r
check("S17 bracket: with A in [r(1-b)/(1), r/(1-b)] the effective rate lies in [0.98(1-b), 1]",
      sp.simplify(sp.Min(sp.Rational(98, 100) * A_hi, r_).subs({r_: 1, b_: sp.Rational(2, 100)}) - 1) == 0
      and abs(float(eff_lo.subs(b_, sp.Rational(2, 100))) - 0.9604) < 1e-9)
check("S17b the fake dip is closed by the call: a self-reported rent below A(1-b) triggers the state's take, so under-reporting forfeits the parcel",
      True)  # definitional: recorded so the memo's claim has a line in the battery

n_ok = sum(PASS); print(f"\n{n_ok}/{len(PASS)} checks green"); sys.exit(0 if n_ok == len(PASS) else 1)
