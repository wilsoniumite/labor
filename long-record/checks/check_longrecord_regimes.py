# check_longrecord_regimes.py — Phase-0 algebra for the long-record thread.
#
# House rule: no claim enters a spec or paper before its algebra passes a
# computer-algebra check and equilibrium claims a numeric instance. This file
# gates the "discriminating predictions" section of ../docs/spec.md.
#
# It also RECORDS A REFUTATION: the founding discussion proposed a raw
# sign-flip in wage-rent comovement at the regime switch. R3 and R4 below
# show that claim does not survive: nominal comovement is numeraire content
# (the price system is homogeneous of degree one in the terminal rent), and
# the population-response of the wage is negative in BOTH regimes. What
# survives, and is sharper, is R2e: WHAT DETERMINES q flips at the switch —
# scarcity-side (N against T) in the floor regime, cost-side (the machine
# recipe) in the flat-capability limit.
#
# Objects follow paper/pinning.html notation (the-link-revision).

import sympy as sp
import numpy as np

GREEN = []

def ok(name, cond):
    assert cond, f"FAILED: {name}"
    GREEN.append(name)
    print(f"  PASS  {name}")

# ---------------------------------------------------------------- R1: floor
print("R1  floor regime (goods numeraire; sloped branch of s(q))")
q, s0, sd, he, gs, hs = sp.symbols('q s0 sd he gs hs', positive=True)

w_floor = s0 - q*he            # wage pinned at the outside option, Prop 3(ii)
Ps = gs + q*hs                 # subsistence bundle price / p_g  (F.3's bundle)
WR = w_floor / Ps              # the welfare ratio: Allen's object, our floor

num = sp.simplify(sp.together(sp.diff(WR, q)) * Ps**2)
ok("R1a dWR/dq < 0: numerator is -(he*gs + hs*s0)",
   sp.simplify(num + (he*gs + hs*s0)) == 0)

w_over_r = w_floor / q         # wage in land units (r/p_g = q, p_g = 1 here)
ok("R1b d(w/r)/dq = -s0/q^2 < 0",
   sp.simplify(sp.diff(w_over_r, q) + s0/q**2) == 0)
# Reading: in the floor regime the wage responds to the land margin, and the
# welfare ratio falls one-for-one-ish with q. Population is the driver of q.

# ------------------------------------------------- R2: ceiling, flat limit
print("R2  ceiling regime, flat-capability limit (Props 2, 4, D.1)")
a, lam, rho, ell, r, Lbar = sp.symbols('a lam rho ell r Lbar', positive=True)
D = 1 - a - lam*rho            # viability margin, assumed > 0

c = ell*r/D                    # Prop 2 closure
w = rho*c
pg = c*rho*Lbar                # flat-limit goods price

ok("R2a w/pg = 1/Lbar (Prop 4(i): goods-wage pinned by absolute productivity)",
   sp.simplify(w/pg - 1/Lbar) == 0)

wr = sp.simplify(w/r)
ok("R2b w/r = rho*ell/(1-a-lam*rho), and r-free",
   sp.simplify(wr - rho*ell/D) == 0 and not wr.has(r))
ok("R2c d(w/r)/drho = ell*(1-a)/D^2 > 0",
   sp.simplify(sp.diff(wr, rho) - ell*(1-a)/D**2) == 0)
ok("R2d d(w/r)/dlam = rho^2*ell/D^2 > 0",
   sp.simplify(sp.diff(wr, lam) - rho**2*ell/D**2) == 0)

qflat = sp.simplify(r/pg)
ok("R2e q = (1-a-lam*rho)/(ell*rho*Lbar): TECHNOLOGY-ONLY (no N, no T)",
   sp.simplify(qflat - D/(ell*rho*Lbar)) == 0
   and not any(qflat.has(s) for s in (q,)))
# Reading: in the flat limit q is pinned from the COST side (Prop 4(ii),
# D.1(iii)); land supply moves quantities, not the relative price. In the
# floor regime q is pinned from the SCARCITY side (N against T). This is the
# surviving discriminator D1: q's determinant flips at the switch.

# ------------------------------------------------------- R3: homogeneity
print("R3  homogeneity: nominal (w,r) comovement is numeraire content")
kap = sp.symbols('kap', positive=True)
scale = lambda e: e.subs(r, kap*r)
ok("R3a c, w, pg all scale linearly in r",
   all(sp.simplify(scale(e)/e - kap) == 0 for e in (c, w, pg)))
ok("R3b w/pg and w/r invariant to r-scaling",
   sp.simplify(scale(w/pg) - w/pg) == 0
   and sp.simplify(scale(wr) - wr) == 0)
# Reading: "rents up => nominal wages up" in the ceiling regime is a change
# of numeraire, not a prediction. Any fit must run on deflated objects
# (welfare ratio, w/r, q), never on nominal comovements.

# ------------------------------------- R4: refutation record (sign of dw/dN)
print("R4  REFUTATION RECORD: the naive sign-flip in the N-response")
# floor channel: N up -> land margin tightens -> q up -> w down.
w_at = lambda qv: 25.0 - qv*10.0            # s0 = 25, he = 10 (toy dollars)
ok("R4a floor: w falls as q(N) rises", w_at(0.8) < w_at(0.5))
# ceiling channel: N up -> x* down -> rho* down -> w down.
# paper's worked instance (a, lam, ell, r) = (0.5, 0.1, 0.2, 1):
wc = lambda rh: rh*0.2*1.0/(1 - 0.5 - 0.1*rh)
ok("R4b ceiling: w falls as rho*(N) falls (3.0 -> 2.8 gives 3.00 -> ~2.55)",
   wc(2.8) < wc(3.0) and abs(wc(3.0) - 3.0) < 1e-12)
print("  RECORDED: dw/dN < 0 in BOTH regimes. The sign of the population")
print("  response does NOT discriminate. Discrimination lives in q's")
print("  determinant (R2e) and the switch event (R5), plus the channel:")
print("  floor-era wage moves are MEDIATED by rents; ceiling-era moves are")
print("  mediated by the task margin with the land market dropping out of")
print("  the wage equation conditional on technology.")

# ---------------------------------------------------- R5: the switch (toy)
print("R5  the switch object exists along a plausible technology path (TOY)")
ts = np.linspace(0.0, 1.0, 101)
rho_t = 0.5 + 2.5*ts        # margin rho* rising through industrialisation
q_t = 0.3 + 0.9*ts          # land tightening as the margin closes
s_t = 25.0 - 10.0*q_t       # floor falling 22 -> 13
wc_t = rho_t*0.2*30.0/(1 - 0.5 - 0.1*rho_t)   # ceiling candidate, toy scale
assert np.all(1 - 0.5 - 0.1*rho_t > 0), "viability violated in toy"
cross = np.argmax(wc_t > s_t)
ok("R5a binding boundary switches at an interior date",
   0 < cross < len(ts) - 1 and wc_t[0] < s_t[0] and wc_t[-1] > s_t[-1])
print(f"        toy crossing at t = {ts[cross]:.2f} "
      f"(wc = {wc_t[cross]:.1f}, s = {s_t[cross]:.1f}) — illustrates the")
print("        object the fit must DATE, not a calibration.")

# ----------------------------------------------------------------- summary
print()
print(f"ALL GREEN ({len(GREEN)} checks)")
print("VERDICTS for the spec:")
print("  D1  q's determinant flips at the switch: scarcity-side (N/T) in the")
print("      floor regime [R1], cost-side (machine recipe) in the flat limit")
print("      [R2e]. OPEN ALGEBRA: the sloped machine era (lam > 0, land in")
print("      production AND housing) needs the joint system of App A before")
print("      D1 can be asserted along the transition path, not just at the")
print("      endpoint configurations.")
print("  D2  the switch is a joint event (wage escape = land-share exit):")
print("      stated in Sec 9 of the paper; the fit dates it two ways [R5].")
print("  D3  floor-era welfare-ratio variance should be explained by (N, T)")
print("      alone with he-consistent magnitudes [R1]; refuted-claim record")
print("      [R3, R4] bans nominal-comovement and sign-flip 'tests'.")
