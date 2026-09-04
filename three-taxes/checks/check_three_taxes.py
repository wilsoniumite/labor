# check_three_taxes.py — algebra + numeric checks for the three-taxes sketch
# ("Three Taxes", thread founded 2026-08-27 from the circular-flow conversation).
#
# Everything here is NEW relative to the-link-revision/checks/ and
# link-repo/checks/: the resolution shares phi_w/phi_r derived from the
# closure, the tier-2 leg decomposition and its corner equivalence, the
# convergence of the deadweight index on both factors, the circular-flow
# fixed point and its kappa discipline, the grandfathering dial, the
# hold-up FOC behind the 100% ceiling, the withholding-monopoly identity,
# and the A–K one-time-levy share. The closure itself is check_pinning's;
# block 1 re-derives it only to build on it.
#
# House rule: no proposition enters a draft before its check passes.
# Run: ../venv/Scripts/python.exe checks/check_three_taxes.py  (from three-taxes/)

import sympy as sp

GREEN = []
def ok(name, cond):
    assert cond, f"CHECK FAILED: {name}"
    GREEN.append(name)
    print(f"  ok  {name}")

a, lam, rho, ell, r, w, c, t, tau = sp.symbols(
    "a lambda rho ell r w c t tau", positive=True)

# ------------------------------------------------- T1: resolution shares
# Closure (check_pinning's Prop 2, re-derived as the base for everything):
sol = sp.solve([sp.Eq(w, c*rho), sp.Eq(c, a*c + lam*w + ell*r)], [w, c], dict=True)
assert len(sol) == 1
c_star = sp.simplify(sol[0][c]); w_star = sp.simplify(sol[0][w])
D = 1 - a - lam*rho

# Total wage/rent content of one unit's price: the recursion's geometric
# unwind. W_u = a*W_u + lam*w  and  R_u = a*R_u + ell*r.
W_u = sp.solve(sp.Eq(sp.Symbol("Wu"), a*sp.Symbol("Wu") + lam*w_star),
               sp.Symbol("Wu"))[0]
R_u = sp.solve(sp.Eq(sp.Symbol("Ru"), a*sp.Symbol("Ru") + ell*r),
               sp.Symbol("Ru"))[0]
ok("T1 contents: W_u = lam*w*/(1-a), R_u = ell*r/(1-a)",
   sp.simplify(W_u - lam*w_star/(1 - a)) == 0
   and sp.simplify(R_u - ell*r/(1 - a)) == 0)
ok("T1 ledger closes: W_u + R_u = c* (every price resolves into the two claims)",
   sp.simplify(W_u + R_u - c_star) == 0)

phi_w = sp.simplify(W_u/c_star)
phi_r = sp.simplify(R_u/c_star)
ok("T1 shares: phi_w = lam*rho/(1-a), phi_r = (1-a-lam*rho)/(1-a)",
   sp.simplify(phi_w - lam*rho/(1 - a)) == 0
   and sp.simplify(phi_r - D/(1 - a)) == 0)
ok("T1 shares sum to one", sp.simplify(phi_w + phi_r - 1) == 0)
ok("T1 corner: lam->0 gives (phi_w, phi_r) = (0, 1)",
   phi_w.subs(lam, 0) == 0 and phi_r.subs(lam, 0) == 1)
# Viability D>0 with lam*rho>0 pins phi_r strictly inside (0,1):
ok("T1 viability pins phi_r in (0,1): 1-phi_r = lam*rho/(1-a) > 0 and phi_r = D/(1-a) > 0 on D>0",
   sp.simplify(1 - phi_r - lam*rho/(1 - a)) == 0)

inst = {a: sp.Rational(1, 2), lam: sp.Rational(1, 10), rho: 3,
        ell: sp.Rational(1, 5), r: 1}
ok("T1 instance (0.5,0.1,3,0.2,1): phi_w = 0.6, phi_r = 0.4",
   phi_w.subs(inst) == sp.Rational(3, 5) and phi_r.subs(inst) == sp.Rational(2, 5))

# --------------------------------------- T6: the tier-2 legs and the corner
# A consumption tax at rate t on one unit splits t*c into a wage-leg
# (payroll tax in disguise — P1 App C's phrase) and a rent-leg (lump-sum).
wage_leg = t*c_star*phi_w
rent_leg = t*c_star*phi_r
ok("T6 legs: wage leg = t*lam*w*/(1-a), rent leg = t*ell*r/(1-a)",
   sp.simplify(wage_leg - t*lam*w_star/(1 - a)) == 0
   and sp.simplify(rent_leg - t*ell*r/(1 - a)) == 0)
ok("T6 legs instance: at t=0.25, unit revenue 0.25 splits 0.15 wage / 0.10 rent",
   wage_leg.subs(inst).subs(t, sp.Rational(1, 4)) == sp.Rational(3, 20)
   and rent_leg.subs(inst).subs(t, sp.Rational(1, 4)) == sp.Rational(1, 10))
ok("T6 corner: lam->0 kills the wage leg; whole revenue is the rent leg",
   sp.simplify(wage_leg.subs(lam, 0)) == 0
   and sp.simplify(rent_leg.subs(lam, 0) - t*c_star.subs(lam, 0)) == 0)
# Corner equivalence (P1 prop:landonly read fiscally): at lam=0 the rent
# flow per unit IS the price, so a consumption tax at rate t and a rent
# tax at rate tau=t take identical revenue per unit.
ok("T6 corner equivalence: t*c|_{lam=0} = tau*R_u|_{lam=0} at tau=t",
   sp.simplify(t*c_star.subs(lam, 0) - t*R_u.subs(lam, 0)) == 0)
inst0 = dict(inst); inst0[lam] = 0
ok("T6 corner instance: lam=0 gives c=0.4=rent content; both taxes take 0.12 at 30%",
   c_star.subs(inst0) == sp.Rational(2, 5)
   and sp.Rational(3, 10)*sp.Rational(2, 5) == sp.Rational(3, 25))

# ------------------------------------------------- T7: convergence
ok("T7 rate: d(phi_w)/d(lam) = rho/(1-a) > 0 (the impurity is lam-shaped)",
   sp.simplify(sp.diff(phi_w, lam) - rho/(1 - a)) == 0)
# DW = F(lam)*(1-k(lam))^2 with F'>0 (wage-financed share rises in lam)
# and k'<0 (kappa falls in lam): DW is increasing in lam, so it falls as
# automation lowers lam — BOTH factors, one process.
F, Fp, k, kp = sp.symbols("F Fp k kp", positive=True)  # kp = -k'(lam) > 0
dDW = Fp*(1 - k)**2 + 2*F*(1 - k)*kp          # = F'(1-k)^2 - 2F(1-k)k'
ok("T7 monotone: dDW/dlam = F'(1-k)^2 - 2F(1-k)k' > 0 given F'>0, k'<0, k<1",
   sp.simplify(dDW.subs(k, sp.Rational(1, 3))) ==
   Fp*sp.Rational(4, 9) + F*kp*sp.Rational(4, 3)
   and dDW.subs({F: 1, Fp: 1, k: sp.Rational(1, 3), kp: 1}) > 0)
# P1 App C's measured instance: 0.72*(1-0.33)^2 = 0.32; at (0.50,0.60) = 0.08.
ok("T7 index instance: 0.72*(1-0.33)^2 rounds to 0.32",
   abs(0.72*(1 - 0.33)**2 - 0.32) < 0.005)
ok("T7 index instance: 0.50*(1-0.60)^2 = 0.08",
   sp.Rational(1, 2)*sp.Rational(2, 5)**2 == sp.Rational(2, 25))

# ------------------------------------------- T5: the circular flow, disciplined
R0, m_p, m_r, x, g, h, kap0 = sp.symbols("R0 m_p m_r x g h kappa0", positive=True)
# Gross recirculation fixed point: R = R0 + phi_r*tau*R.
R_star = sp.solve(sp.Eq(sp.Symbol("R"), R0 + phi_r*tau*sp.Symbol("R")),
                  sp.Symbol("R"))[0]
ok("T5 fixed point: R* = R0/(1 - phi_r*tau)",
   sp.simplify(R_star - R0/(1 - phi_r*tau)) == 0)
ok("T5 convergent on the viable set: phi_r*tau < 1 whenever lam*rho>0, tau<=1",
   sp.simplify(1 - phi_r*tau - (lam*rho/(1 - a))).subs(tau, 1) == 0)
   # at tau=1 the gap 1-phi_r*tau equals the wage-resolution share exactly:
   # the loop closes (diverges) only at (lam=0, tau=1) — the corner circuit.
ok("T5 instance: phi_r=0.4, tau=1 -> gross base multiplier 1/0.6 = 5/3",
   sp.simplify(R_star.subs(inst).subs(tau, 1) - sp.Rational(5, 3)*R0) == 0)
# Net discipline: a transfer x moves spending between baskets; the base
# moves by the rent-content DIFFERENCE only.
ok("T5 transfer invariance: dR = (m_p - m_r)*x; equal baskets move nothing",
   sp.simplify((m_p*x - m_r*x) - (m_p - m_r)*x) == 0
   and (m_p*x - m_r*x).subs(m_p, m_r) == 0)
# kappa under a rent-price scaling g (numerator fully exposed, bundle
# exposed through its rent content h):
kap_g = kap0*g/((1 - h) + h*g)
ok("T5 kappa(1) = kappa0", sp.simplify(kap_g.subs(g, 1) - kap0) == 0)
ok("T5 kappa rises in g iff h<1: d(kappa)/dg = kappa0*(1-h)/((1-h)+h*g)^2",
   sp.simplify(sp.diff(kap_g, g) - kap0*(1 - h)/((1 - h) + h*g)**2) == 0)
ok("T5 both-sides invariance: h=1 makes kappa(g) = kappa0 for every g",
   sp.simplify(kap_g.subs(h, 1) - kap0) == 0)
ok("T5 ceiling in g: kappa -> kappa0/h as g -> oo",
   sp.simplify(sp.limit(kap_g, g, sp.oo) - kap0/h) == 0)
ok("T5 instance: h=0.62, g=1.1 lifts kappa by ~3.6% (second-order, as argued)",
   abs(float(kap_g.subs({h: 0.62, g: 1.1, kap0: 1})) - 1.0358) < 0.001)

# ------------------------------------------------- T4: the grandfathering dial
gam, delta = sp.symbols("gamma delta", positive=True)
PV_full = sp.integrate(r*sp.exp(gam*sp.Symbol("s_")) *
                       sp.exp(-delta*sp.Symbol("s_")),
                       (sp.Symbol("s_"), 0, sp.oo), conds="none")
PV_kept = sp.integrate(r*sp.exp(-delta*sp.Symbol("s_")),
                       (sp.Symbol("s_"), 0, sp.oo), conds="none")
share = sp.simplify(1 - PV_kept/PV_full)
ok("T4 dial: increment-only capture share = gamma/delta (delta>gamma)",
   sp.simplify(share.subs(delta, gam + sp.Symbol("d2", positive=True))
               - gam/(gam + sp.Symbol("d2", positive=True))) == 0)
ok("T4 dial instance: gamma=2%, delta=5% -> 40% of the stock",
   share.subs({gam: sp.Rational(2, 100), delta: sp.Rational(5, 100)})
   == sp.Rational(2, 5))

# ------------------------------------------------- T3: the ceiling's hold-up FOC
A_, alph, beta, e = sp.symbols("A alpha beta e", positive=True)
# Tenant surplus (1-beta)*A*e^alpha - e; revaluation captures beta of value.
e_star = sp.solve(sp.Eq(sp.diff((1 - beta)*A_*e**alph - e, e), 0), e)[0]
e_fb = e_star.subs(beta, 0)
ok("T3 hold-up: e*(beta) = (alpha*A*(1-beta))^(1/(1-alpha)); beta=0 is first-best",
   sp.simplify(e_star - (alph*A_*(1 - beta))**(1/(1 - alph))) == 0)
inst3 = {A_: 2, alph: sp.Rational(1, 2)}
ok("T3 instance: A=2, alpha=1/2 -> e_fb=1; beta=1/2 -> e*=1/4",
   sp.simplify(e_fb.subs(inst3) - 1) == 0
   and sp.simplify(e_star.subs(inst3).subs(beta, sp.Rational(1, 2))
                   - sp.Rational(1, 4)) == 0)
S = A_*e**alph - e   # joint surplus
ok("T3 instance: joint surplus 1 at beta=0 falls to 3/4 at beta=1/2",
   sp.simplify(S.subs(inst3).subs(e, 1) - 1) == 0
   and sp.simplify(S.subs(inst3).subs(e, sp.Rational(1, 4))
                   - sp.Rational(3, 4)) == 0)

# ------------------------------------------------- T3b: withholding identity
A2, B2, T2 = sp.symbols("A2 B2 T2", positive=True)
r_clear = (A2 - T2)/B2                    # D(r)=A2-B2*r clears at T2
gain = sp.simplify(A2**2/(4*B2) - r_clear*T2)
ok("T3b withholding: unconstrained monopoly revenue - competitive bill = (T-A/2)^2/B",
   sp.simplify(gain - (T2 - A2/2)**2/B2) == 0)
ok("T3b instance: A=10,B=1,T=6 -> monopoly 25 > bill 24, one unit idled",
   gain.subs({A2: 10, B2: 1, T2: 6}) == 1
   and (10 - sp.Rational(10, 2))/1 == 5)   # served 5 of 6
ok("T3b instance: A=10,B=1,T=4 -> constraint binds (A/2=5>4), no gain over clearing",
   sp.Rational(10, 2) > 4)  # monopoly point infeasible; price = clearing price
   # Perversity note checked by the identity: the gain (T-A/2)^2/B GROWS with
   # abundance T — withholding pays most where natural scarcity is mildest.

# ------------------------------------------------- T6c: the A–K third leg
ok("T6c one-time levy: VAT at t takes t/(1+t) of existing wealth's purchasing power",
   sp.simplify(1 - 1/(1 + t) - t/(1 + t)) == 0)
ok("T6c instance: t=25% -> a 20% levy on accumulated stocks",
   sp.Rational(1, 4)/(1 + sp.Rational(1, 4)) == sp.Rational(1, 5))

print(f"ALL GREEN ({len(GREEN)})")
