# vet_eocc2.py - adversarial checks of candidate E-OCC2 (explore half only; data via explore/data.py, manifest occ only).
import os, sys, json
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "explore")); sys.path.insert(0, os.path.join(ROOT, "code"))
import data, inference as inf
from scipy import stats
es = data.es
B = int(os.environ.get("B", 9999))
raw = data.manifest_raw(); occr = raw["occ"]
print("occ columns:", list(occr.columns), "units:", occr.get("unit", pd.Series()).unique()[:5])
occ = es.clean(occr)
w = occ.pivot_table(index=["geo", "year"], columns=["age", "isco08"], values="value")
yg, al = w["Y15-24"], w["Y15-64"]; pr = al - yg
geos = data.GEOS
N = [0]; OUT = {}

def Rser(groups=("OC4",), young=yg, old=pr):
    return np.log((sum(young[c] for c in groups) / young["TOTAL"]) / (sum(old[c] for c in groups) / old["TOTAL"]))

def brk(groups):
    b = {}
    for a in ["Y15-24", "Y15-64"]:
        for i in list(groups) + ["TOTAL"]:
            for g, ys in es.break_years(occr[(occr.age == a) & (occr.isco08 == i)]).items():
                b.setdefault(g, set()).update(int(t) for t in ys)
    return b

def bdum(d, b, lo):
    cols, seen = [], set()
    for g, ys in b.items():
        m = (d.geo == g).to_numpy()
        for t in sorted(ys):
            if t <= lo: continue
            c = (m & (d.year >= t).to_numpy()).astype(float)
            if not m.any() or c[m].min() == c[m].max() or c.tobytes() in seen: continue
            seen.add(c.tobytes()); cols.append(c)
    return np.column_stack(cols) if cols else np.zeros((len(d), 0))

def run(label, groups=("OC4",), base=(2022,), post=(2023, 2024, 2025), gs=None, trend_pre=None, side=-1, quiet=False,
        breaks=True):
    Rm = Rser(groups)
    yrs = list(base) + list(post) + (list(trend_pre) if trend_pre else [])
    d = Rm.rename("R").reset_index()
    d = d[d.geo.isin(gs or geos) & d.year.isin(yrs)].dropna().reset_index(drop=True)
    d = d[d.groupby("geo").year.transform(lambda s: s.isin(base).any() and s.isin(post).any())].reset_index(drop=True)
    d["post"] = d.year.isin(post).astype(float)
    Zl = [inf.fe_matrix(d, "geo")]
    if breaks: Zl.append(bdum(d, brk(groups), min(yrs)))
    if trend_pre:  # country-specific linear trends identified off the pre years + base
        for g in sorted(set(d.geo))[1:] if False else sorted(set(d.geo)):
            Zl.append(((d.geo == g) * (d.year - 2015)).to_numpy(float)[:, None])
    Z = np.column_stack(Zl)
    r = inf.wcr(d["R"].to_numpy(), d["post"].to_numpy(), Z, d.geo.to_numpy(), side=side, B=B)
    N[0] += 1
    rec = dict(beta=r["beta"], se=r["se"], p=r["p"], p_opp=r["p_opposite"], n=r["n"], G=r["G"], Gs=r.get("G_star"))
    OUT[label] = rec
    if not quiet:
        print(f"[{N[0]:2d}] {label:58s} b={r['beta']:+.4f} se={r['se']:.4f} p={r['p']:.3f} n={r['n']} G={r['G']} G*={r.get('G_star', 0):.1f}")
    return r, d

# 0. reproduce
r0, d0 = run("E-OCC2 as proposed")
print("countries:", sorted(set(d0.geo)), "years per country:", d0.groupby("geo").year.apply(list).to_dict())
# 1. which cells exist: u/c in OC4 Y15-24
f = occr[(occr.isco08 == "OC4") & (occr.age == "Y15-24") & occr.year.between(2016, 2025)]
print("\nOC4 Y15-24 flags 2016-25:\n", f.pivot_table(index="geo", columns="year", values="flag", aggfunc="first").fillna("").to_string())
print("\nOC4 Y15-24 levels (THS) 2022-25:\n", w["Y15-24"]["OC4"].unstack("geo").loc[2016:2025].round(1).T.to_string())
# 2. the per-country change and pre-period behaviour of R
Rm = Rser().unstack("geo")
print("\nR_OC4 by year:\n", Rm.loc[2011:2025].round(3).T.to_string())
ch = (Rm.loc[2023:2025].mean() - Rm.loc[2022])
print("\nchange 2022 -> mean 2023-25:", ch.round(3).sort_values().to_dict(), "mean", round(ch.mean(), 4), "median", round(ch.median(), 4))
# 3. placebo windows: same contrast with base year b and post b+1..b+3, all pre-AI
plac = {}
for b0 in range(2011, 2017):
    r, _ = run(f"placebo base {b0}, post {b0+1}-{b0+3}", base=(b0,), post=(b0 + 1, b0 + 2, b0 + 3), quiet=True)
    plac[b0] = (round(r["beta"], 4), round(r["se"], 4), round(r["p"], 3))
print("\nplacebo windows (beta, se, p one-sided neg):", plac)
betas = np.array([v[0] for v in plac.values()])
print("placebo beta mean", betas.mean().round(4), "sd", betas.std(ddof=1).round(4))
# 4. pre-trend: slope of R on year within country 2011-2019
dd = Rm.loc[2011:2019].stack().rename("R").reset_index()
slopes = dd.groupby("geo").apply(lambda z: np.polyfit(z.year, z.R, 1)[0] if len(z) > 3 else np.nan)
print("\nwithin-country slope of R 2011-19 per year:", slopes.round(4).to_dict(), "mean", round(slopes.mean(), 4))
# pooled pre-trend via WCR: R on year with country FE 2011-2019
dpre = dd[dd.geo.isin(geos)].dropna().reset_index(drop=True)
rpt = inf.wcr(dpre.R.to_numpy(), (dpre.year - 2015).to_numpy(float), inf.fe_matrix(dpre, "geo"), dpre.geo.to_numpy(), side=-1, B=B)
N[0] += 1
print(f"pooled pre-trend 2011-19: slope {rpt['beta']:+.4f}/yr se {rpt['se']:.4f} p(neg) {rpt['p']:.3f} p(pos) {rpt['p_opposite']:.3f}")
# 5. alternatives
run("base 2019+2022 (pre = both)", base=(2019, 2022))
run("base 2016-19+2022", base=(2016, 2017, 2018, 2019, 2022))
run("trend-adjusted: pre 2015-19 + 2022 base, country trends", trend_pre=(2015, 2016, 2017, 2018, 2019))
run("no break dummies", breaks=False)
run("post 2024-25 only", post=(2024, 2025))
run("placebo occupation OC7", groups=("OC7",), side=-1)
run("placebo occupation OC8", groups=("OC8",), side=-1)
# 6. leave-two-out worst
import itertools
G0 = sorted(set(d0.geo)); l2 = {}
for a, b2 in itertools.combinations(G0, 2):
    r, _ = run(f"L2O {a},{b2}", gs=[g for g in G0 if g not in (a, b2)], quiet=True)
    l2[(a, b2)] = r["p"]
srt = sorted(l2.items(), key=lambda kv: kv[1])
print("\nleave-two-out lowest p:", srt[:5], " highest p:", srt[-3:])
# 7. MDE on 15 clusters, at alpha 0.05 and at Holm's first step 0.01 (5 E)
se15 = r0["se"] * np.sqrt(r0["G"] / 15)
for a in (0.05, 0.025, 0.0125, 0.01):
    print(f"MDE15 alpha={a}: {inf.mde(se15, 15, alpha=a):.3f}")
# what fraction of confirm countries would have data: G of explore = 14/16 -> scale to ~13 of 15
se13 = r0["se"] * np.sqrt(r0["G"] / 13)
print(f"MDE13 alpha=0.05: {inf.mde(se13, 13):.3f}; alpha=0.01: {inf.mde(se13, 13, alpha=0.01):.3f}")
print("\nN specs estimated here (incl. 15 placebo/L2O quiet):", N[0])
json.dump(dict(OUT={k: v for k, v in OUT.items() if not k.startswith("L2O") and not k.startswith("placebo")},
               placebo=plac, l2o_low=[(list(k), v) for k, v in srt[:5]], n_specs=N[0]),
          open(os.path.join(HERE, "vet_eocc2.json"), "w"), indent=1, default=float)
