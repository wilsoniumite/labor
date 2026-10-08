# vet_ehf1_decomp.py — E-HF1: rents vs goods prices in the joint regression; a real-income interaction control.
import os, sys
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "explore")); sys.path.insert(0, os.path.join(ROOT, "code"))
import data, build, specs, inference as inf
raw = data.manifest_raw()
cy = build.country_year("explore", raw=raw); cl = build.country_level("explore", raw=raw)
for name, age in (("U", "Y25-74"),):
    s, b = build.cell(raw["une_lfs"], age=age); cy[name] = s.reindex(cy.index).to_numpy(float)
    cy[name + "__breaks"] = [list(b.get(g, [])) for g in cy.index.get_level_values(0)]
geos = sorted(set(cy.index.get_level_values(0))); fstd = specs.f_constants(cl, geos); ctx = specs.Ctx(cl, fstd)
spec = dict(specs.TESTS["D1"]); fr = specs.frame(cy, spec, ctx, geos)
y, x, Z, g, M = specs.design(fr, spec["fe"], trends=True)
key = pd.MultiIndex.from_arrays([M.geo, M.year - 1])
def lg(coicop):
    s, _ = build.cell(raw["hicp"], coicop=coicop); return np.log(s).reindex(key).to_numpy(float)
def lcomp():
    s, _ = build.cell(raw["comp"]); return np.log(s).reindex(key).to_numpy(float)
F = M.geo.map(ctx.F).to_numpy(float)
r041, rig, r00, rc = lg("CP041"), lg("IGD_NNRG"), lg("CP00"), lcomp()
print("check q == r041 - rig:", np.nanmax(np.abs((r041 - rig) * F - x)))
n = 0
def go(lab, xv, extra, side=-1):
    global n
    ok = np.isfinite(xv) & np.isfinite(extra).all(1)
    r = inf.wcr(y[ok], xv[ok], np.column_stack([Z[ok], extra[ok]]), g[ok], side=side, B=9999); n += 1
    print(f"{lab:62s} b={r['beta']:+7.2f} se={r['se']:5.2f} p={r['p']:.3f} n={r['n']}")
# joint: CP041 x F and IGD x F with their main effects (q main effect sits in Z already: drop it by using raw cols)
base = Z  # Z holds log q main effect as z0; add components
go("joint: log CP041 x F  (| log IGD x F, mains)", r041 * F, np.column_stack([rig * F, r041, rig]))
go("joint: -log IGD x F   (| log CP041 x F, mains)", -rig * F, np.column_stack([r041 * F, r041, rig]))
# equality test: q x F with (log CP041 + log IGD) x F added — tests if rents and goods enter as a ratio
go("q x F | (log CP041 + log IGD) x F (homogeneity)", x, np.column_stack([(r041 + rig) * F, r041 + rig]))
go("q x F | log CP00 x F (general inflation x F)", x, np.column_stack([r00 * F, r00]))
rw = rc - r00
go("q x F | log real comp_{t-1} and x F", x, np.column_stack([rw, rw * F]))
go("log real comp_{t-1} x F alone (two-sided)", rw * F, np.column_stack([rw]), side=0)
go("q x F | log nominal comp x F and log IGD x F", x, np.column_stack([rc, rc * F, rig * F, rig]))
print("specs:", n)
