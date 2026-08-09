"""Baseline verification of the algebra in 'The Link' (Aug 2026 working draft).

Run top-to-bottom (notebook-cell friendly). Every block prints PASS or raises
AssertionError with the offending residual. Symbolic checks via sympy; the
running example of Sections 3-4 is re-done numerically at the end.

Status: everything passes. The one genuine erratum (Prop 4(ii), a -> 1 margin)
is documented in check_prop4ii_margins() below and PATCHED in the draft as of
2026-08-05. Labels follow post-splice numbering: closure = Prop 5,
Conditionality = Prop 6, Funding = Prop 7 (pre-splice: 5 and 6).
"""
import sympy as sp

# Symbols. All positive by declaration; a < 1 where the recursion needs it.
a, ell, r, delta = sp.symbols('a ell r delta', positive=True)
rho, Lbar, sigma, t = sp.symbols('rho Lbar sigma t', positive=True)
n_share = sp.symbols('n_share', positive=True)   # participation share n/N


def ok(name, zero_expr):
    z = sp.simplify(zero_expr)
    assert z == 0, f"FAIL {name}: residual {z}"
    print(f"PASS  {name}")


# ---------- Prop 3: machine rental recursion ----------
c_sym = sp.symbols('c', positive=True)
c_static = sp.solve(sp.Eq(c_sym, a * c_sym + ell * r), c_sym)[0]
ok("Prop 3          c = lr/(1-a)", c_static - ell * r / (1 - a))

c_disc = sp.solve(sp.Eq(c_sym, (a * c_sym + ell * r) * (1 + delta)), c_sym)[0]
ok("Prop 3 (delta)  c = lr(1+d)/(1-a(1+d))",
   c_disc - ell * r * (1 + delta) / (1 - a * (1 + delta)))

# Corner-regime objects used everywhere below (delta = 0)
c = ell * r / (1 - a)      # machine rental
w = c * rho                # corner base wage
pg = c * rho * Lbar        # final-good price on the flat schedule

# ---------- Prop 4(i): real wage in machine-made goods ----------
ok("Prop 4(i)       w/pg = 1/Lbar (machine quality cancels)", w / pg - 1 / Lbar)

# ---------- Prop 4(ii): relative price of non-produced services ----------
ok("Prop 4(ii)      r/pg = (1-a)/(l rho Lbar)",
   r / pg - (1 - a) / (ell * rho * Lbar))


def check_prop4ii_margins():
    target = (1 - a) / (ell * rho * Lbar)
    # the patch's substitution bound, asserted (not just printed): l = l0*(1-a)
    ell0 = sp.symbols('ell0', positive=True)
    ok("Prop 4(ii)      substitution bound: l = l0*(1-a) leaves r/pg = 1/(l0 rho Lbar)",
       target.subs(ell, ell0 * (1 - a)) - 1 / (ell0 * rho * Lbar))
    # sympy can't sign (1-a) from positivity alone; pin the bystander symbols.
    half = sp.Rational(1, 2)
    assert sp.limit(target.subs({a: half, ell: 1, Lbar: 1}), rho, 0, '+') == sp.oo
    assert sp.limit(target.subs({a: half, rho: 1, Lbar: 1}), ell, 0, '+') == sp.oo
    lim_a = sp.limit(target.subs({ell: 1, rho: 1, Lbar: 1}), a, 1, '-')
    # The paper claims divergence as a -> 1. The limit is in fact ZERO:
    assert lim_a == 0, lim_a
    print("PASS  Prop 4(ii) margins: rho->0 and l->0 diverge as claimed")
    print("ERRATUM Prop 4(ii): a->1 gives r/pg -> 0, not infinity. a->1 sends the")
    print("        machine rental c = lr/(1-a) to infinity (regress, not progress);")
    print("        improvement is a DOWN, which raises r/pg only boundedly, toward")
    print("        1/(l rho Lbar). Correct divergence margins: rho->0 and l->0 only.")
    print("        (Even joint substitution of machines for land in the recipe,")
    print("        l = l0*(1-a), leaves r/pg = 1/(l0 rho Lbar): bounded.)")


check_prop4ii_margins()

# ---------- Prop 4(iii): collapse against a land-content bundle ----------
P = pg ** (1 - sigma) * r ** sigma
ok("Prop 4(iii)     w/P = (1/Lbar)*(pg/r)^sigma",
   sp.simplify(w / P - (1 / Lbar) * (pg / r) ** sigma))

# Collapse on the two true margins, concrete sigma to keep sympy honest:
wP_c = (w / P).subs({sigma: sp.Rational(1, 3), a: sp.Rational(1, 2),
                     Lbar: 1, r: 1, rho: 2})
assert sp.limit(wP_c, ell, 0, '+') == 0
wP_c2 = (w / P).subs({sigma: sp.Rational(1, 3), a: sp.Rational(1, 2),
                      Lbar: 1, r: 1, ell: sp.Rational(1, 5)})
assert sp.limit(wP_c2, rho, 0, '+') == 0
print("PASS  Prop 4(iii)     w/P -> 0 as l->0 and as rho->0 (sigma > 0)")

# ---------- Prop 7(i): wage-funded transfer in the corner ----------
disposable_full = (1 - t) * c * rho + t * c * rho
ok("Prop 7(i)       full participation: disposable = c*rho for ALL t",
   disposable_full - c * rho)

# Partial participation: tax collected from workers only, transfer spread over N.
disp_partial = (1 - t) * c * rho + t * c * rho * n_share
ok("Prop 7(i)       partial participation: d(disposable)/dt = -c*rho*(1 - n/N) < 0",
   sp.diff(disp_partial, t) + c * rho * (1 - n_share))

# ---------- Lemma 1: wedge deflation ----------
mu, gL, gM, w_free = sp.symbols('mu gamma_L gamma_M w', positive=True)
cost_gap = mu * w_free / gL - c_sym / gM          # labor holds task iff <= 0
deflated = w_free - c_sym * (gL / gM) / mu        # iff w <= c * rho/mu
ok("Lemma 1         cost comparison == (w <= c*rhotilde), positive rescale",
   sp.simplify(cost_gap * gL / mu - deflated))


# ---------- Running example, Sections 3-4, numeric ----------
def running_example():
    c0, s = 10.0, 25.0
    raw = {'A': 1.0, 'B': 5.0, 'C': 4.5}
    mu_ = {'A': 1.0, 'B': 1.25, 'C': 1.0}
    eff = {k: raw[k] / mu_[k] for k in raw}            # A:1, B:4, C:4.5
    assert eff['B'] == 4.0 and eff['C'] == 4.5

    # Machines hold A; marginal labor task = lowest effective edge among {B, C}.
    w0 = c0 * min(eff['B'], eff['C'])
    assert w0 == 40.0                                   # base wage
    assert mu_['B'] * w0 == 50.0                        # wedge job pays 50

    # Machines improve uniformly 25%: every human edge divides by 1.25.
    raw1 = {k: v / 1.25 for k, v in raw.items()}        # B:4, C:3.6
    eff1 = {k: raw1[k] / mu_[k] for k in raw}           # B:3.2, C:3.6
    assert abs(eff1['B'] - 3.2) < 1e-12 and abs(eff1['C'] - 3.6) < 1e-12
    assert c0 * eff1['B'] == 32.0     # "if nothing else changed" wage at B-margin
    assert eff1['B'] < eff1['C']      # Prop 2 targeting: wedged B floods first,
    #                                   though humans are objectively better at it
    assert raw1['B'] > raw1['C']      # (4 > 3.6 -- the paper's point, verified)
    assert c0 * eff1['C'] == 36.0     # post-flood base wage at the C-margin

    # Displaced B-worker loses 50 -> 36: 10 of wedge rent (full incidence)
    # plus 4 of base-wage decline (spread economy-wide).
    assert (50 - 36) == (10 + 4)

    # Fig 3 terminal stage: c=10, rhobar=1.8 -> parity wage 18 < s=25 -> exit.
    assert c0 * 1.8 == 18.0 and 18.0 < s

    # Prop 6(ii) corner make-work: b=8 gives s-b=17 <= 18 < 25 ->
    # benefit summons work; society burns s - c*rhobar = 7 per hour.
    b = 8.0
    assert s - b <= 18.0 < s and (s - c0 * 1.8) == 7.0

    print("PASS  Running example (Sections 3-4), Prop 2 ordering, Fig 3 terminal, "
          "Prop 6(ii) burn rate")


running_example()

print()
print("All baseline checks passed. (Prop 4(ii) erratum: documented above, "
      "patched in the draft 2026-08-05.)")
