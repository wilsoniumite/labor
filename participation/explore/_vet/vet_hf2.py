# vet_hf2.py — adversarial checks on E-HF2 (explore half only). No logging into the explorer's files.
import os, sys, json
import numpy as np, pandas as pd
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "explore")); sys.path.insert(0, os.path.join(ROOT, "code"))
import data, build, specs, inference as inf

raw = data.manifest_raw()
cy = build.country_year("explore", raw=raw)
cl = build.country_level("explore", raw=raw)
out = cy.copy()
for name, age in (("U", "Y25-74"), ("U2554", "Y25-54"), ("U1529", "Y15-29")):
    s, b = build.cell(raw["une_lfs"], age=age)
    out[name] = s.reindex(out.index).to_numpy(float)
    out[name + "__breaks"] = [list(b.get(g, [])) for g in out.index.get_level_values(0)]
cyl = out
geos = sorted(set(cy.index.get_level_values(0)))
fstd = specs.f_constants(cl, geos)
ctx = specs.Ctx(cl, fstd)
print("F_raw / F_years:"); print(cl[["F_raw", "F_years"]].to_string())
spec = dict(specs.TESTS["C1"]); spec.update(x="Q*F", z=["Q"], side=1)
B = int(os.environ.get("B", 1999))
res = {}

def fr_design(spec, cyx=cyl, geos_=geos, years=None):
    s = dict(spec)
    if years: s["years"] = years
    fr = specs.frame(cyx, s, ctx, geos_, None)
    return fr

def est(label, spec, cyx=cyl, geos_=geos, years=None, extra=None, trends=True, drop_rows=None):
    fr = fr_design(spec, cyx, geos_, years)
    y, x, Z, g, M = specs.design(fr, spec["fe"], trends=trends)
    if drop_rows is not None:
        keep = ~drop_rows(M)
        y, x, Z, g, M = y[keep], x[keep], Z[keep], g[keep], M[keep].reset_index(drop=True)
        Z = Z[:, np.abs(Z).sum(0) > 0]
    if extra is not None:
        Z = np.column_stack([Z, extra(M)])
    r = inf.wcr(y, x, Z, g, side=1, B=B)
    res[label] = dict(beta=r["beta"], se=r["se"], p=r["p"], n=r["n"], G=r["G"])
    print(f"{label:60s} b={r['beta']:+7.2f} se={r['se']:5.2f} p={r['p']:.3f} n={r['n']} G={r['G']}")
    return r, (y, x, Z, g, M)

r0, (y, x, Z, g, M) = est("HF2 as proposed", spec)
geo_used = sorted(set(M.geo))
Fm = M.geo.map(ctx.F).to_numpy(float)

# 1. windows
est("drop 2022-2025", spec, years=(2005, 2019))
est("2008-2025", spec, years=(2008, 2025))
est("2010-2025", spec, years=(2010, 2025))
est("2005-2023", spec, years=(2005, 2023))
# drop each country's own F-construction years from the outcome sample
Fy = cl["F_years"]
def own_F_years(M):
    return np.array([yr in (Fy.get(gg) or []) for gg, yr in zip(M.geo, M.year)])
est("drop each country's own F years from outcome", spec, drop_rows=own_F_years)

# 2. F x year effects: identification only off country-specific q deviations
def Fyear(M):
    yrs = sorted(set(M.year))[1:]
    return np.column_stack([(M.year.to_numpy() == t) * M.geo.map(ctx.F).to_numpy(float) for t in yrs])
est("+ F x year dummies", spec, extra=Fyear)
# F x quadratic trend
def Fq(M):
    t = (M.year.to_numpy(float) - 2015) / 10
    return np.column_stack([M.geo.map(ctx.F).to_numpy(float) * t**2])
est("+ F x t^2", spec, extra=Fq)
# country quadratic trends
def cq(M):
    t = (M.year.to_numpy(float) - 2015) / 10
    return np.column_stack([(M.geo.to_numpy() == gg) * t**2 for gg in sorted(set(M.geo))])
est("+ country quadratic trends", spec, extra=cq)
# U x F (the cycle response differs with floor)
def UF(M):
    return np.column_stack([M["c0"].to_numpy(float) * M.geo.map(ctx.F).to_numpy(float)])
est("+ U x F", spec, extra=UF)
# youth unemployment control (C-1 secondary)
s2 = dict(spec); s2["controls"] = ["U", "U1529"]
est("+ U15-29", s2)
# no break dummies? (check how many)
fr = fr_design(spec)
print("break dummies:", len(fr["breaks"]), fr["breaks"])

# 3. lead: q_{t+1} x F
s3 = dict(spec); 
def lead(M):
    d = cyl.reset_index().set_index(["geo", "year"])
    lf = d["logq_f1"].reindex(list(zip(M.geo, M.year))).to_numpy(float)
    return np.column_stack([lf * M.geo.map(ctx.F).to_numpy(float), lf])
r, (yy, xx, ZZ, gg_, MM) = est("+ lead q_{t+1} and q_{t+1} x F (rows with lead)", spec, extra=lead,
                                 drop_rows=lambda M: ~np.isfinite(cyl.reset_index().set_index(['geo','year'])['logq_f1'].reindex(list(zip(M.geo, M.year))).to_numpy(float)))
# lead coefficient itself
mask = np.isfinite(cyl.reset_index().set_index(['geo','year'])['logq_f1'].reindex(list(zip(M.geo, M.year))).to_numpy(float))
Ml = M[mask].reset_index(drop=True)
lf = cyl.reset_index().set_index(["geo", "year"])["logq_f1"].reindex(list(zip(Ml.geo, Ml.year))).to_numpy(float)
Zl = np.column_stack([Z[mask], x[mask], lf]); Zl = Zl[:, np.abs(Zl).sum(0) > 0]
rl = inf.wcr(y[mask], lf * Ml.geo.map(ctx.F).to_numpy(float), Zl, g[mask], side=0, B=B)
print(f"   lead coefficient q_(t+1) x F: b={rl['beta']:+.2f} se={rl['se']:.2f} two-sided p={rl['p']:.3f}")
res["lead coef"] = dict(beta=rl["beta"], se=rl["se"], p2=rl["p"])

# 4. randomisation inference over F's assignment across the 15 countries (design-based, few clusters)
rng = np.random.default_rng(7)
Fvals = ctx.F.reindex(geo_used).to_numpy(float)
q = M["z0"].to_numpy(float)
Zb = Z.copy()
def tstat(xv):
    rr = inf.wcr(y, xv, Zb, g, side=1, B=9)
    return rr["beta"] / rr["se"], rr["beta"]
t0, b0 = tstat(x)
ts, bs = [], []
for _ in range(int(os.environ.get("R", 999))):
    perm = dict(zip(geo_used, rng.permutation(Fvals)))
    xv = q * M.geo.map(perm).to_numpy(float)
    t, b = tstat(xv); ts.append(t); bs.append(b)
ts = np.array(ts); bs = np.array(bs)
p_ri_t = (1 + (ts >= t0).sum()) / (1 + len(ts)); p_ri_b = (1 + (bs >= b0).sum()) / (1 + len(bs))
print(f"RI over F permutations: t0={t0:.2f} p(t)={p_ri_t:.3f} p(b)={p_ri_b:.3f}; sd of b under perm={bs.std():.2f}")
res["RI F perm"] = dict(t0=t0, p_t=p_ri_t, p_b=p_ri_b, sd_b=bs.std())

# 5. FWL: partial out and show country contributions to the slope
P = np.column_stack([np.ones(len(y)), Z])
bet = np.linalg.lstsq(P, x, rcond=None)[0]; xr = x - P @ bet
bet = np.linalg.lstsq(P, y, rcond=None)[0]; yr = y - P @ bet
contrib = pd.DataFrame({"geo": g, "xy": xr * yr, "xx": xr * xr}).groupby("geo").sum()
contrib["share_num"] = contrib.xy / contrib.xy.sum(); contrib["share_var"] = contrib.xx / contrib.xx.sum()
contrib["F"] = ctx.F.reindex(contrib.index)
print("beta check", (xr @ yr) / (xr @ xr)); print(contrib.round(3).to_string())
yearc = pd.DataFrame({"year": M.year, "xy": xr * yr, "xx": xr * xr}).groupby("year").sum()
yearc["share_num"] = yearc.xy / (xr @ yr); yearc["share_var"] = yearc.xx / (xr @ xr)
print(yearc.round(3).to_string())
# leave-two-out worst
loo2 = []
import itertools
for a, b_ in itertools.combinations(geo_used, 2):
    keep = (g != a) & (g != b_)
    Zk = Z[keep]; Zk = Zk[:, np.abs(Zk).sum(0) > 0]
    Pk = np.column_stack([np.ones(keep.sum()), Zk])
    xk = x[keep] - Pk @ np.linalg.lstsq(Pk, x[keep], rcond=None)[0]
    loo2.append((a, b_, float(xk @ y[keep] / (xk @ xk))))
loo2.sort(key=lambda t: t[2]); print("leave-two-out lowest betas:", loo2[:6])
res["loo2_min"] = loo2[:6]
# data peek
d = cyl.reset_index(); d = d[d.geo.isin(geo_used)]
print(d.pivot(index="year", columns="geo", values="coresid2534").round(1).to_string())
print(d.pivot(index="year", columns="geo", values="logq_l1").round(3).to_string())
json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "vet_hf2.json"), "w"), indent=1, default=float)
