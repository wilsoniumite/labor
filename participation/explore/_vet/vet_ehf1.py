# vet_ehf1.py — adversarial checks of candidate E-HF1 (explore half only; data via explore/data.py).
import json, os, sys
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "explore")); sys.path.insert(0, os.path.join(ROOT, "code"))
import data, build, specs, inference as inf

raw = data.manifest_raw()
cy = build.country_year("explore", raw=raw); cl = build.country_level("explore", raw=raw)
cyl = cy.copy()
for name, age in (("U", "Y25-74"), ("U2554", "Y25-54"), ("U1529", "Y15-29")):
    s, b = build.cell(raw["une_lfs"], age=age)
    cyl[name] = s.reindex(cyl.index).to_numpy(float)
    cyl[name + "__breaks"] = [list(b.get(g, [])) for g in cyl.index.get_level_values(0)]
geos = sorted(set(cy.index.get_level_values(0)))
fstd = specs.f_constants(cl, geos); ctx = specs.Ctx(cl, fstd)
B = int(os.environ.get("B", 9999))
N = [0]; OUT = {}

def est(label, frame_cy=cyl, over=None, geos_=None, trends=True, quad=False, extra_cols=None, variant=None, perm=None):
    spec = dict(specs.TESTS["D1"]); spec.update(over or {})
    c = specs.Ctx(cl, fstd)
    if perm is not None:
        c.F = pd.Series(perm, index=c.F.index)
    fr = specs.frame(frame_cy, spec, c, geos_ or geos, variant)
    y, x, Z, g, M = specs.design(fr, spec["fe"], trends=trends)
    if quad:
        t = ((M["year"].to_numpy(float) - 2010) / 10) ** 2
        Z = np.column_stack([Z] + [(M["geo"].to_numpy() == gg) * t for gg in sorted(set(M["geo"]))])
    if extra_cols is not None:
        Z = np.column_stack([Z, extra_cols(M)])
    r = inf.wcr(y, x, Z, g, side=-1, B=B)
    N[0] += 1
    rec = dict(beta=r["beta"], se=r["se"], p=r["p"], p_opp=r["p_opposite"], n=r["n"], G=r["G"],
               yrs=[int(M.year.min()), int(M.year.max())])
    if perm is None:
        OUT[label] = rec
        print(f"{label:55s} b={r['beta']:+7.2f} se={r['se']:5.2f} p={r['p']:.3f} n={r['n']} G={r['G']} yrs={rec['yrs']}")
    return r, M

base, M0 = est("E-HF1 as proposed")
est("no trends (same frame)", trends=False)
est("quadratic country trends", quad=True)
est("trends, all residents", variant="all_residents")
est("trends, frozen U (une_rt_a)", frame_cy=cy)
est("trends, 2003+", over=dict(years=(2003, 2025)))
est("trends, 2005+", over=dict(years=(2005, 2025)))
est("trends, 1997-2012", over=dict(years=(1997, 2012)))
est("trends, 2013-2025", over=dict(years=(2013, 2025)))
est("trends, excl 2008-2013", variant="excl_2008_2013")
CEE = ["BG", "EE", "HR", "HU", "LV", "PL"]; SOUTH = ["IT", "MT", "PT"]
est("trends, drop CEE", geos_=[g for g in geos if g not in CEE])
est("trends, drop South", geos_=[g for g in geos if g not in SOUTH])
est("trends, drop CEE+South", geos_=[g for g in geos if g not in CEE + SOUTH])
# leave-two-out worst
worst = []
import itertools
loo2 = {}
for a, b2 in itertools.combinations([g for g in geos if g != "HR"], 2):
    spec = dict(specs.TESTS["D1"])
    fr = specs.frame(cyl, spec, ctx, [g for g in geos if g not in (a, b2)])
    y, x, Z, g, M = specs.design(fr, spec["fe"], trends=True)
    r = inf.wcr(y, x, Z, g, side=-1, B=999); N[0] += 1
    loo2[a + "-" + b2] = (r["beta"], r["p"])
srt = sorted(loo2.items(), key=lambda kv: -kv[1][1])[:8]
print("leave-two-out worst (B=999):", [(k, round(v[0], 2), round(v[1], 3)) for k, v in srt])
print("share of 105 leave-two-out with p>0.10:", np.mean([v[1] > 0.10 for v in loo2.values()]))
OUT["loo2_worst"] = srt; OUT["loo2_share_p_gt_010"] = float(np.mean([v[1] > 0.10 for v in loo2.values()]))

# lead placebo: add log q_{t+1} and log q_{t+1} x F with trends
def lead_cols(M):
    d = cyl.reset_index().set_index(["geo", "year"])
    f1 = d["logq_f1"].reindex(pd.MultiIndex.from_arrays([M.geo, M.year])).to_numpy(float)
    F = M.geo.map(ctx.F).to_numpy(float)
    return np.column_stack([f1, f1 * F])
spec = dict(specs.TESTS["D1"]); fr = specs.frame(cyl, spec, ctx, geos)
y, x, Z, g, M = specs.design(fr, spec["fe"], trends=True)
L = lead_cols(M); ok = np.isfinite(L).all(1)
r = inf.wcr(y[ok], x[ok], np.column_stack([Z[ok], L[ok]]), g[ok], side=-1, B=B); N[0] += 1
rl = inf.wcr(y[ok], L[ok, 1], np.column_stack([Z[ok], L[ok, 0], x[ok]]), g[ok], side=0, B=B); N[0] += 1
print(f"lead check: b2 (lag) {r['beta']:+.2f} se {r['se']:.2f} p {r['p']:.3f}; lead q_f1 x F {rl['beta']:+.2f} se {rl['se']:.2f} p2 {rl['p']:.3f} n {r['n']}")
OUT["lead"] = dict(b_lag=r["beta"], p_lag=r["p"], b_lead=rl["beta"], se_lead=rl["se"], p2_lead=rl["p"])
# contemporaneous q instead of lag
d = cyl.copy(); d["logq_l1"] = d["logq"]; d["logq_l1__breaks"] = d["logq__breaks"] if "logq__breaks" in d else d["logq_l1__breaks"]
est("trends, q contemporaneous", frame_cy=d)

# components of q: CP041 x F vs IGD_NNRG x F
hicp = raw["hicp"]
def comp_series(coicop):
    s, b = build.cell(hicp, coicop=coicop)
    return np.log(s)
try:
    rows = {}
    for cc in ("CP041", "IGD_NNRG", "CP00"):
        s = comp_series(cc)
        s1 = s.copy(); s1.index = pd.MultiIndex.from_arrays([s.index.get_level_values(0), s.index.get_level_values(1) + 1])
        rows[cc] = s1
    for cc in ("CP041", "IGD_NNRG"):
        dd = cyl.copy(); dd["logq_l1"] = rows[cc].reindex(dd.index).to_numpy(float) * (1 if cc == "CP041" else -1)
        est(f"trends, component: {'+log CP041' if cc=='CP041' else '-log IGD_NNRG'} (x F)", frame_cy=dd)
except Exception as e:
    print("components failed", e)

# outcome pieces
for lab, cols in (("men", [("M", "Y25-29"), ("M", "Y30-34")]), ("women", [("F", "Y25-29"), ("F", "Y30-34")]),
                  ("25-29", [("M", "Y25-29"), ("F", "Y25-29")]), ("30-34", [("M", "Y30-34"), ("F", "Y30-34")])):
    s = build.band(raw["act"], [dict(sex=a, age=b_, citizen="NAT") for a, b_ in cols])
    dd = cyl.copy(); dd["A2534"] = (s[0] if isinstance(s, tuple) else s).reindex(dd.index).to_numpy(float)
    est(f"trends, outcome {lab}", frame_cy=dd)

# randomisation inference: permute F across the 15 countries (all permutations sampled)
rng = np.random.default_rng(1)
Fv = ctx.F.copy(); idx = [g for g in Fv.index if np.isfinite(Fv[g])]
tobs = base["t"]; ts = []
for k in range(2000):
    p = Fv.copy(); p[idx] = rng.permutation(Fv[idx].to_numpy())
    spec = dict(specs.TESTS["D1"]); c = specs.Ctx(cl, fstd); c.F = p
    fr = specs.frame(cyl, spec, c, geos); y, x, Z, g, M = specs.design(fr, spec["fe"], trends=True)
    f = inf._Fit(y, x, Z, g); ts.append(f.t(0.0))
ts = np.array(ts)
print(f"RI (F permuted across countries, 2000 draws, studentised): p one-sided = {np.mean(ts <= tobs):.3f}; t_obs {tobs:.2f}")
OUT["ri_perm_F"] = dict(p=float(np.mean(ts <= tobs)), t_obs=float(tobs))
# MDEs
se = base["se"]
for a in (0.05, 0.01, 0.0125, 0.025):
    print(f"MDE (G=15, alpha={a}): {inf.mde(se, 15, alpha=a):.2f}")
from scipy import stats
for true in (6.09, 4.5, 3.0):
    pw = 1 - stats.t.cdf(stats.t.ppf(0.95, 14) - true / se, 14)
    pw1 = 1 - stats.t.cdf(stats.t.ppf(0.99, 14) - true / se, 14)
    print(f"power if true b2={true}: alpha .05 {pw:.2f}, alpha .01 {pw1:.2f}")
print("specs estimated in this vet:", N[0], "(+2000 permutation fits)")
json.dump(specs.clean_json(OUT), open(os.path.join(HERE, "vet_ehf1.json"), "w"), indent=1)
