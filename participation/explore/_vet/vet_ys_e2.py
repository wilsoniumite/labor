# vet_ys_e2.py — adversarial checks on youth_school E2 (D1's equation with E 20-24 as outcome). Explore half only.
# Uses the frozen specs machinery (specs.estimate) with D1's outcome swapped; logs nothing into the explorer's files.
import os, sys, json
import numpy as np, pandas as pd
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "explore")); sys.path.insert(0, os.path.join(ROOT, "code"))
import data, build, specs, inference as inf

raw = data.manifest_raw()
cy = build.country_year("explore", raw=raw)
cl = build.country_level("explore", raw=raw)
geos = sorted(set(cy.index.get_level_values(0)))
ctx = specs.Ctx(cl, specs.f_constants(cl, geos))
B = int(os.environ.get("B", 1999))
res = {}
E2 = dict(specs.TESTS["D1"]); E2["outcome"] = [(1, "E2024")]

def run(label, spec, variant=None, g=geos, b=B, ci=False):
    r = specs.estimate(cy, cl, spec, ctx, g, variant=variant, B=b, with_ci=ci)
    res[label] = {k: r.get(k) for k in ("beta", "se", "p", "p_opposite", "n", "G", "G_star", "mde", "lead_coefficient")}
    print(f"{label:55s} b={r['beta']:+7.2f} se={r['se']:5.2f} p(-)={r['p']:.3f} n={r['n']} G={r['G']} "
          f"G*={r['G_star']:.1f} mde={r['mde']:.1f}" + (f" lead={r['lead_coefficient']}" if r.get('lead_coefficient') else ""))
    return r

r0 = run("E2 as proposed (B=9999)", E2, b=9999, ci=True)
print("  geos", r0["geos_used"], "years", r0["years_used"][0], "-", r0["years_used"][-1], "ci", r0["ci"])
print("  MDE on 15 clusters from this se:", inf.mde(r0["se"], 15))
run("D1 frozen (A2534) for comparison", specs.TESTS["D1"])
for v in ["country_trends", "excl_2008_2013", "lead", "all_residents", "q_hpi", "q_cp00", "q_comp", "long_differences"]:
    try:
        run(f"E2 variant {v}", E2, v)
    except Exception as e:
        print(v, "failed", e)
# the main effect and the top-quartile slope
sl = dict(specs.SECONDARY["D1.slope_top_quartile"]) if hasattr(specs, "SECONDARY") else None
# leave one out
loo = {}
for g in r0["geos_used"]:
    r = specs.estimate(cy, cl, E2, ctx, [x for x in geos if x != g], B=B, with_ci=False)
    loo[g] = (round(r["beta"], 2), round(r["p"], 3))
print("LOO:", loo); res["loo"] = loo
# leave two out: the worst pair for the hypothesis
worst = []
gs = r0["geos_used"]
for i in range(len(gs)):
    for j in range(i + 1, len(gs)):
        r = specs.estimate(cy, cl, E2, ctx, [x for x in geos if x not in (gs[i], gs[j])], B=499, with_ci=False)
        worst.append((r["p"], r["beta"], gs[i], gs[j]))
worst.sort(reverse=True)
print("leave-two-out, five weakest:", [(round(p, 3), round(b, 2), a, c) for p, b, a, c in worst[:5]])
print("leave-two-out share with p>0.10:", np.mean([w[0] > 0.10 for w in worst]))
res["l2o_share_p_gt_010"] = float(np.mean([w[0] > 0.10 for w in worst]))

# F x year fixed effects: absorbs any common shock loading on F (e.g. 2009-2013 crisis, post-2013 recovery in high-F)
fr = specs.frame(cy, E2, ctx, geos)
y, x, Z, g, M = specs.design(fr, E2["fe"])
F = M.geo.map(ctx.F).to_numpy(float)
yrs = sorted(set(M.year))
FY = np.column_stack([F * (M.year.to_numpy() == t) for t in yrs[1:]])
r = inf.wcr(y, x, np.column_stack([Z, FY]), g, side=-1, B=B)
print(f"{'E2 + F x year FE':55s} b={r['beta']:+7.2f} se={r['se']:5.2f} p(-)={r['p']:.3f}")
res["FxYear"] = dict(beta=r["beta"], se=r["se"], p=r["p"])
# F x linear trend only
FT = (F * (M.year.to_numpy() - 2010) / 10)[:, None]
r = inf.wcr(y, x, np.column_stack([Z, FT]), g, side=-1, B=B)
print(f"{'E2 + F x linear trend':55s} b={r['beta']:+7.2f} se={r['se']:5.2f} p(-)={r['p']:.3f}")
res["FxTrend"] = dict(beta=r["beta"], se=r["se"], p=r["p"])
# the main-effect coefficient b1 and implied slopes
from numpy.linalg import lstsq
Xf = np.column_stack([x, Z])
coef = lstsq(Xf, y, rcond=None)[0]
b2, b1 = coef[0], coef[1 + list(range(Z.shape[1])).index(Z.shape[1] - Z.shape[1]) + 0] if False else (coef[0], None)
# z0 (Q) sits after the FE block: find its column
nfe = inf.fe_matrix(M, ["geo", "year"]).shape[1]
b1 = coef[1 + nfe]
F75 = np.percentile(ctx.F.reindex(sorted(set(M.geo))).to_numpy(float), 75)
F25 = np.percentile(ctx.F.reindex(sorted(set(M.geo))).to_numpy(float), 25)
print(f"b1 (q at F=0) = {b1:.2f}; slope at F25 = {b1 + coef[0]*F25:.2f}; at F75 = {b1 + coef[0]*F75:.2f}")
res["b1"] = b1; res["slope_F25"] = b1 + coef[0]*F25; res["slope_F75"] = b1 + coef[0]*F75
print("F by country:", ctx.F.reindex(sorted(set(M.geo))).round(2).to_dict())

# per-country slope of E2024 on q (FE-only within, year FE common): understanding
dd = M.copy(); dd["y"] = y; dd["q"] = M["z0"]
# residualise y and q on year FE + U + breaks except country-specific slope: simple: country-by-country OLS of y on q, U, year trend
sl = {}
for gg, s in dd.groupby("geo"):
    if len(s) > 5:
        A = np.column_stack([np.ones(len(s)), s.q, s.c0])
        c = lstsq(A, s.y, rcond=None)[0]
        sl[gg] = round(c[1], 1)
print("country slope dE2024/dlogq (with U, no year FE):", sl)
res["country_slopes"] = sl
json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "vet_ys_e2.json"), "w"), indent=1,
          default=lambda o: o if not isinstance(o, np.generic) else o.item())
