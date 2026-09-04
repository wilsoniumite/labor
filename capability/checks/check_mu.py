"""Verification of Block D (the anatomy of mu) — sketch link-sketch-blocks-B0-C-D.md.

Claims checked (the [check] flag of D1):
  (D1-CS) Formal statement of the three comparative statics of the displacement-
          loss decomposition L = wedge + stranded specific practice +
          compensating differential:
            (1) wedge component: discrete at the event, scales with the base
                wage and (mu-1), tenure-free;
            (2) stranded practice: dL/dtenure = (r+dP)*sigma_spec*C'(tenure) > 0
                — the tenure gradient identifies the stranded share;
            (3) compensating differential: appears in the MEASURED wage loss,
                cancels in welfare (amenity regained), so it concentrates where
                disamenities were high and adds zero to both welfare and
                allocative columns.
          Ledger inequalities: welfare loss <= measured loss (equality iff
          d = 0); allocative (negative-sum) component = wedge only, so the
          wedge-share reading of the imported 60-90% offset is an UPPER bound,
          and the offset restates as (imported figure) x (wedge weight).
"""
import sys

import sympy as sp

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

b, mu, r, dP, sig, d_ = sp.symbols('b mu r delta_P sigma_spec d', positive=True)
ten = sp.symbols('tenure', positive=True)
C_s = sp.Function('C')(ten)                      # accumulated specific-practice cost

w_pre = b * mu + (r + dP) * sig * C_s + d_       # wedge + specific premium + differential
w_post = b                                       # transferable base elsewhere
L = sp.simplify(w_pre - w_post)                  # measured displacement loss

# (1) wedge component
wedge = b * (mu - 1)
assert sp.simplify(L - (wedge + (r + dP) * sig * C_s + d_)) == 0
assert sp.diff(wedge, ten) == 0
print("PASS  D1-CS ledger: L = b(mu-1) + (r+dP)*sigma*C(tenure) + d; wedge term tenure-free")

# (2) stranded practice: the tenure gradient belongs to it alone
dL_dten = sp.simplify(sp.diff(L, ten))
assert sp.simplify(dL_dten - (r + dP) * sig * sp.diff(C_s, ten)) == 0
print("PASS  D1-CS dL/dtenure = (r+dP)*sigma*C'(tenure) — the tenure gradient identifies"
      " the stranded-practice share (Jacobson-LaLonde-Sullivan gradient, in the model)")

# (3) compensating differential: measured vs welfare vs allocative columns
welfare = sp.simplify(L - d_)                    # amenity regained on displacement
alloc = wedge                                    # stranded practice was paid = product
assert sp.simplify(L - welfare - d_) == 0
assert sp.simplify(welfare - alloc - (r + dP) * sig * C_s) == 0
print("PASS  D1-CS columns: measured L >= welfare loss (gap = d, concentrating where"
      " disamenities were high) >= allocative loss (wedge only)")

# the upper-bound restatement of the imported 60-90% figure
share = sp.simplify(alloc / L)
w_wedge = sp.symbols('omega_wedge', positive=True)
one = sp.simplify(share.subs({sig: sp.Rational(0), d_: sp.Rational(0, 1)}))
# with sigma=0 and d=0, share = 1: wedge-share reading exact only in the pure-wedge corner
assert sp.simplify(one - 1) == 0
inst = share.subs({b: 1, mu: sp.Rational(3, 2), sig: sp.Rational(1, 2),
                   C_s: sp.Rational(1, 2), r: sp.Rational(5, 100),
                   dP: sp.Rational(6, 100), d_: sp.Rational(1, 10)})
inst = float(sp.simplify(inst))
assert inst < 1
print(f"PASS  D1-CS wedge-share reading is an upper bound (numeric instance: allocative"
      f" share {inst:.2f} of measured loss); the imported 60-90%% offset restates as"
      " 60-90%% x omega_wedge, indexed by the decomposition weights")

# U-shape incidence, minimal form: wedge losses live only where mu > 1 (the paper's
# upper-middle stratum); base-wage movement hits everyone. Three-position instance:
positions = {"bottom (no rents)": (1, 0), "upper-middle (wedge)": (sp.Rational(3, 2), 0),
             "top (unautomatable rent)": (1, 0)}
losses = {k: float(sp.simplify((b * (m - 1) + dd).subs({b: 1, d_: 0})))
          for k, (m, dd) in positions.items()}
assert losses["upper-middle (wedge)"] > losses["bottom (no rents)"] == losses["top (unautomatable rent)"]
print("PASS  D1-CS incidence: the wedge component concentrates in the upper-middle"
      f" stratum ({losses}) — the U-shape's mechanism, restated")

print()
print("All Block D checks passed (flag D1-CS).")
