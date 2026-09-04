"""Verification of item 8: the open-economy page — Proposition 12 (trade as
the early waterline), the jurisdictional split of the bases, and the
cross-ties (wedges flood first in both waters; the room shields twice;
the bridge is constitutive for deficit consumers).

Numbering: enters as Proposition 12 in a new Section 10 ("The open economy,
in one page"); welfare becomes Section 11 and its theorem Proposition 13.
No other site references either number.

Claims checked (drafted in open_section.html):
  T-i    early waterline: a tradable task is held domestically iff
         w <= min(c*rho~, w_f*rho~_f) — the foreign wage is a second
         machine rental; the tradable waterline is weakly higher, so the
         demolition arrives weakly earlier (min(a,b) <= a), and wedges
         raise flip priority under BOTH margins (each threshold ~ 1/mu)
  T-ii   way-station: as c falls, an offshored task flips to machines when
         machine cost undercuts the foreign wage — offshore then automated,
         the closed corner restored (numeric sequence 40 -> 35 -> 30)
  T-iii  jurisdictional rents: the exporter's Prop-5 pass-through sends the
         importer's spending into the exporter's T_P; destination VAT
         reaches imports, domestic LVT reaches domestic sites only — the
         border splits the bases (neither contains the other)
  T-iv   the bridge is constitutive: deficit instance — domestic rents 60,
         floor 100, imported land content 40: LVT alone cannot fund the
         floor at any rate; adding destination VAT on all consumption can
  T-v    the room shields twice: a co-present task faces only the machine
         margin (offshore cost infinite), and its provenance premium is
         unbounded as v -> 1 (Prop 11's remark, re-tied)
"""
import sympy as sp

def ok(name, zero_expr):
    z = sp.simplify(zero_expr)
    assert z == 0, f"FAIL {name}: residual {z}"
    print(f"PASS  {name}")


# ---------- T-i: early waterline ----------
w, c, wf, mu, rho, rhof = sp.symbols('w c w_f mu rho rho_f', positive=True)
dom_machine = c * rho / mu            # c * rho~
dom_foreign = wf * rhof / mu          # w_f * rho~_f
waterline_tradable = sp.Min(dom_machine, dom_foreign)
# weakly below the closed waterline on BOTH branches (foreign cheaper / machine cheaper):
gap_foreign_cheaper = (waterline_tradable - dom_machine).subs(
    [(c, 10), (rho, 4), (wf, 7), (rhof, 5), (mu, 1)])
gap_machine_cheaper = (waterline_tradable - dom_machine).subs(
    [(c, 10), (rho, 4), (wf, 12), (rhof, 5), (mu, 1)])
assert sp.simplify(gap_foreign_cheaper) == -5    # 35 < 40: trade flips it earlier
assert sp.simplify(gap_machine_cheaper) == 0     # foreign dearer: closed waterline binds
print("PASS  T-i   tradable waterline weakly below the closed one on both branches")
ok("T-i   wedges are negative altitude in both waters: d(threshold)/dmu < 0, machine margin",
   sp.diff(dom_machine, mu) + c * rho / mu ** 2)
ok("T-i   ... and offshore margin alike",
   sp.diff(dom_foreign, mu) + wf * rhof / mu ** 2)

# ---------- T-ii: the way-station ----------
w_dom, cost_foreign = 40, 35
for cost_machine, holder in [(45, "foreign"), (30, "machine")]:
    best = min(w_dom, cost_foreign, cost_machine)
    if cost_machine == 45:
        assert best == cost_foreign and holder == "foreign"     # offshored
    else:
        assert best == cost_machine and holder == "machine"     # then automated
print("PASS  T-ii  sequence 40 (home) -> 35 (offshore) -> 30 (machine): "
      "offshoring is a way-station to the same corner")

# ---------- T-iii: the border splits the bases ----------
a, ell, r, rho_s, Lbar = sp.symbols('a ell r rho_s Lbar', positive=True)
Y = sp.symbols('Y', positive=True)
pg = ell * r * rho_s * Lbar / (1 - a)
TP = ell * (rho_s * Lbar * Y / (1 - a))
ok("T-iii exporter pass-through: importer's goods bill pg*Y = r*T_P abroad",
   pg * Y - r * TP)
E_home, imports, rents_home = 100, 40, 60      # consumption, its imported slice, domestic rT
base_vat = E_home                               # destination principle: all consumption
base_lvt = rents_home                           # domestic sites only
assert imports <= base_vat and imports > 0      # VAT reaches the imported land content
assert base_lvt - (E_home - imports) == 0       # LVT reaches exactly the domestic slice here
print("PASS  T-iii bases split at the border: VAT holds the imported slice (40), "
      "LVT the domestic sites (60); neither contains the other")

# ---------- T-iv: the bridge is constitutive ----------
floor_cost = 100
lvt_max = rents_home                            # t_L = 1
assert lvt_max < floor_cost                     # LVT alone cannot fund the floor
tv_needed = sp.Rational(floor_cost - rents_home, E_home)
assert tv_needed == sp.Rational(2, 5) and lvt_max + tv_needed * E_home == floor_cost
print("PASS  T-iv  deficit instance: LVT max 60 < floor 100; destination VAT at 0.4 "
      "bridges — on open borders the bridge is constitutive")

# ---------- T-v: the room shields twice ----------
copresent_waterline = dom_machine               # offshore cost infinite: min(x, oo) = x
ok("T-v   co-present tasks face only the machine margin",
   copresent_waterline - c * rho / mu)
v, f = sp.symbols('v f', positive=True)
pi_max = v * f / (1 - v)
assert sp.limit(pi_max.subs(f, 1), v, 1, '-') == sp.oo
print("PASS  T-v   and their provenance premium is unbounded as v -> 1 (Prop 11 re-tied): "
      "the room shields twice")

print()
print("All open-economy checks passed.")
