# s02_c4_anatomy.py - why C-4 finds nothing on the explore half, and which country carries G* = 1.8.
# Reproduces the frozen C-4 design (specs.frame/design, read-only import), then decomposes it.
import sys, json
sys.path.insert(0, "explore"); sys.path.insert(0, "code")
import data
import numpy as np, pandas as pd
import specs, inference as inf
pd.set_option("display.width", 200)
cy, cl = data.panel()
ctx = specs.Ctx(cl, (cl["F_raw"].mean(), cl["F_raw"].std(ddof=0)))
spec = specs.TESTS["C4"]
geos = data.GEOS
fr = specs.frame(cy, spec, ctx, geos)
y, x, Z, g, M = specs.design(fr, spec["fe"])
print("n", len(y), "Z cols", Z.shape[1], "break pairs", len(fr["breaks"]))
br = pd.DataFrame(fr["breaks"], columns=["geo", "year"])
print("break years by country (E2024, E2554, U):")
print(br.groupby("geo").year.apply(list).to_string())
r = inf.wcr(y, x, Z, g, side=-1, B=9999)
print("reproduced:", {k: round(r[k], 4) for k in ["beta", "se", "p", "G_star"]})
f = inf._Fit(y, x, Z, g)
gam = pd.Series(np.bincount(f.g, f.xt * f.xt) / f.xx, index=f.labels)
print("\nleverage share gamma_g of each country in xt'xt (G* = G/(1+cv^2)):")
print(gam.sort_values(ascending=False).round(3).to_string())
print("X_c:", cl["X_c"].round(2).sort_values().to_dict())
# per-country contribution to beta: sum_g xt_g'yt_g / xt'xt
contrib = pd.Series(np.bincount(f.g, f.xt * f.yt) / f.xx, index=f.labels)
print("\ncontribution to beta by country (sums to beta):")
print(contrib.sort_values().round(4).to_string(), " total", round(contrib.sum(), 4))
# how much of x is left after the break dummies: share of within-variation absorbed
Z0 = np.column_stack([inf.fe_matrix(M, ["geo", "year"]), M[fr["names"]].to_numpy(float)])
f0 = inf._Fit(y, x, Z0, g)
print("\nxt'xt with breaks / without breaks:", round(f.xx / f0.xx, 3))
r0 = inf.wcr(y, x, Z0, g, side=-1, B=9999)
print("no break dummies:", {k: round(r0[k], 4) for k in ["beta", "se", "p", "G_star"]})
gam0 = pd.Series(np.bincount(f0.g, f0.xt * f0.xt) / f0.xx, index=f0.labels)
print(gam0.sort_values(ascending=False).round(3).head(5).to_string())
# raw outcome: E2024 - E2554 by country, 2016-2025
d = cy.reset_index()
d["gap"] = d["E2024"] - d["E2554"]
print("\nE2024 - E2554 (nationals):")
print(d[d.year >= 2014].pivot(index="year", columns="geo", values="gap").round(1).to_string())
json.dump(dict(gamma=gam.to_dict(), contrib=contrib.to_dict(), gamma_nobreaks=gam0.to_dict(),
               beta=r["beta"], se=r["se"], p=r["p"], G_star=r["G_star"],
               nobreaks=dict(beta=r0["beta"], se=r0["se"], p=r0["p"], G_star=r0["G_star"]),
               breaks=br.groupby("geo").year.apply(list).to_dict(), xx_ratio=f.xx / f0.xx),
          open("explore/occupations_ai/c4_anatomy.json", "w"), indent=1)
