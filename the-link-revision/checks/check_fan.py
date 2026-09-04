# check_fan.py — the land-intensity composites (v5 unit, 2026-09-01).
# Verifies every algebraic claim of the composite-pricing display and
# Proposition fork(iv) in latex/v5_land_intensity.tex, and the measured
# numbers its Section 9 fork paragraph quotes (from the fan CSV built by
# effort-accounting/code/build_fig3_realwage_fan.py). House rule: sympy
# for the algebra, exact anchors for the data, fail loudly.
#
# Claims:
#  F1  cost parity alone prices any category p = w*Lbar_cat + r*b_cat —
#      for ANY machine rental c (only w = gbar*c is used), so the display
#      is closure-free and the build-time/interest closures cannot move it.
#  F2  w/p_cat = 1/(Lbar_cat + b_cat*(r/w)).
#  F3  r/w = (1-a-lam*gbar)/(gbar*b) from the replacement closure; it
#      rises as lam falls and as gbar falls, and diverges as gbar -> 0.
#  F4  b_cat = 0: w/p_cat = 1/Lbar_cat invariant to gbar and lam jointly,
#      and under the interest-augmented closures of Appendix A
#      (c = br(1+rho)/(1-(1+rho)(a+lam*gbar)), same with rho+delta) the
#      display and the invariance hold unchanged, and r/w still diverges.
#  F5  b_cat > 0: w/p_cat strictly falls as r/w rises, to 0 in the limit;
#      the land term overtakes the hours term exactly at r/w = Lbar_cat/b_cat,
#      so lower intensity b/Lbar means a later crossover (the ordering claim).
#  F6  Nesting: (Lbar, 0) reproduces fork(i) w/p = 1/Lbar; multiplying
#      fork(ii)'s r/p by Lbar reproduces F3's r/w (parts consistent).
#  D1  Fan CSV anchors, 1964 base: 2024 legs durables 376.8 / food 113.2 /
#      shelter 78.6 (±0.1), and the Section 9 roundings +277% / +13% / -21%.

import csv
from pathlib import Path

import sympy as sp

a, lam, b, r, gbar = sp.symbols("a lam b r gbar", positive=True)
Lc, bc = sp.symbols("Lc bc", positive=True)          # a category's two constants
rho, delta = sp.symbols("rho delta", positive=True)

fails = []


def chk(name, cond):
    ok = bool(cond)
    print(("PASS " if ok else "FAIL ") + name)
    if not ok:
        fails.append(name)


# F1 — parity alone: any c, machine-hours per unit of hours content = gbar.
c_any = sp.symbols("c_any", positive=True)
p_cat = gbar * Lc * c_any + bc * r                    # machine-done tasks + land
w_par = gbar * c_any
chk("F1 p_cat = w*Lc + r*bc under parity, any c",
    sp.simplify(p_cat - (w_par * Lc + r * bc)) == 0)

# F2/F3 — with the replacement closure.
c_cl = sp.solve(sp.Eq(sp.Symbol("c"), a * sp.Symbol("c") + lam * gbar * sp.Symbol("c") + b * r),
                sp.Symbol("c"), dict=True)[0][sp.Symbol("c")]
w_cl = gbar * c_cl
rw = sp.simplify(r / w_cl)
chk("F3 r/w = (1-a-lam*gbar)/(gbar*b)",
    sp.simplify(rw - (1 - a - lam * gbar) / (gbar * b)) == 0)
chk("F3 r/w rises as lam falls", sp.simplify(sp.diff(rw, lam) + 1 / b) == 0)
chk("F3 r/w rises as gbar falls",
    sp.simplify(sp.diff(rw, gbar) + (1 - a) / (gbar**2 * b)) == 0)
chk("F3 r/w diverges as gbar->0",
    sp.limit(rw.subs({a: sp.Rational(1, 2), lam: sp.Rational(1, 10), b: sp.Rational(1, 5)}),
             gbar, 0, "+") == sp.oo)
wp = sp.simplify(w_cl / (gbar * Lc * c_cl + bc * r))
chk("F2 w/p_cat = 1/(Lc + bc*(r/w))", sp.simplify(wp - 1 / (Lc + bc * rw)) == 0)

# F4 — zero content: joint invariance, and under the interest closures.
wp0 = wp.subs(bc, 0)
chk("F4 b=0 invariant in gbar", sp.simplify(sp.diff(wp0, gbar)) == 0)
chk("F4 b=0 invariant in lam", sp.simplify(sp.diff(wp0, lam)) == 0)
chk("F4 b=0 value 1/Lc", sp.simplify(wp0 - 1 / Lc) == 0)
for tag, fac in (("1+rho", 1 + rho), ("rho+delta", rho + delta)):
    c_i = b * r * fac / (1 - fac * (a + lam * gbar))  # Appendix A user-cost closures
    w_i = gbar * c_i
    wp_i = sp.simplify(w_i / (gbar * Lc * c_i + bc * r))
    rw_i = sp.simplify(r / w_i)
    chk(f"F4 display holds under {tag} closure",
        sp.simplify(wp_i - 1 / (Lc + bc * rw_i)) == 0)
    chk(f"F4 b=0 invariant under {tag} closure",
        sp.simplify(sp.diff(wp_i.subs(bc, 0), gbar)) == 0
        and sp.simplify(sp.diff(wp_i.subs(bc, 0), lam)) == 0)
    chk(f"F4 r/w diverges as gbar->0 under {tag} closure",
        sp.limit(rw_i.subs({a: sp.Rational(1, 2), lam: sp.Rational(1, 10),
                            b: sp.Rational(1, 5), rho: sp.Rational(1, 20),
                            delta: sp.Rational(1, 10)}), gbar, 0, "+") == sp.oo)

# F5 — monotone fall, limit, crossover, ordering.
x = sp.symbols("x", positive=True)                    # x stands for r/w
wp_x = 1 / (Lc + bc * x)
chk("F5 w/p falls in r/w when bc>0",
    sp.simplify(sp.diff(wp_x, x) + bc / (Lc + bc * x) ** 2) == 0)
chk("F5 w/p -> 0 as r/w -> oo", sp.limit(wp_x, x, sp.oo) == 0)
chk("F5 crossover: land term = hours term at r/w = Lc/bc",
    sp.simplify((bc * x - Lc).subs(x, Lc / bc)) == 0)
L1, b1, L2, b2 = sp.symbols("L1 b1 L2 b2", positive=True)
chk("F5 ordering: lower b/L means later crossover",
    sp.simplify(sp.together(L1 / b1 - L2 / b2)
                - sp.together((b2 / L2 - b1 / L1) * (L1 * L2) / (b1 * b2))) == 0)

# F6 — nesting against fork(i)/(ii).
chk("F6 (Lbar,0) reproduces fork(i)",
    sp.simplify(wp.subs({Lc: sp.Symbol("Lbar", positive=True), bc: 0})
                - 1 / sp.Symbol("Lbar", positive=True)) == 0)
Lbar = sp.Symbol("Lbar", positive=True)
rp_forkii = (1 - a - lam * gbar) / (b * gbar * Lbar)  # fork(ii) display
chk("F6 fork(ii) * Lbar = r/w", sp.simplify(rp_forkii * Lbar - rw) == 0)

# D1 — the fan CSV anchors and the Section 9 roundings.
csv_path = Path(__file__).resolve().parent.parent.parent / "effort-accounting" / "data" / "fig3_realwage_fan.csv"
if not csv_path.exists():
    chk(f"D1 fan CSV present at {csv_path}", False)
else:
    rows = {int(r_["year"]): r_ for r_ in csv.DictReader(open(csv_path, encoding="utf-8"))}
    legs64 = {}
    for name in ("durables", "food", "shelter"):
        col = f"real_wage_{name}_1950_100"
        legs64[name] = 100 * float(rows[2024][col]) / float(rows[1964][col])
    for name, target in (("durables", 376.8), ("food", 113.2), ("shelter", 78.6)):
        chk(f"D1 {name} leg 2024 (1964 base) = {target}",
            abs(legs64[name] - target) <= 0.1)
    for name, pct in (("durables", 277), ("food", 13), ("shelter", -21)):
        chk(f"D1 {name} rounding {pct:+d}%", round(legs64[name] - 100) == pct)

print()
print("ALL GREEN" if not fails else f"{len(fails)} FAILURES: {fails}")
raise SystemExit(1 if fails else 0)
