# s06_candidates.py - explore-half estimates of the candidate E-hypotheses, from the frozen manifest's raw frames only
# (lfsa_egais sex T, Y15-24 and Y15-64, OC4/OC7/OC8/TOTAL; 25-64 = 15-64 minus 15-24), with C3 break dummies from
# the cells used, C4 (u/c missing), C2 (2020-21 dropped), clusters = country (16 on the explore half).
#   E-OCC1  entrants hold the clerical stretch: OC4 share at 15-24 minus at 25-64 > 0 (stacked, young dummy,
#           country x year FE), 2011-2025.
#   E-OCC2  entrants first in the AI window: R = log(OC4 share 15-24 / OC4 share 25-64) falls from 2022 to 2023-25
#           (country FE, 2022-2025, post dummy).
# Leave-one-out and the MDE on 15 clusters (explore se scaled by sqrt(16/15)).
import sys, json
sys.path.insert(0, "explore"); sys.path.insert(0, "code")
import data
import numpy as np, pandas as pd
import inference as inf
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
es = data.es
prev = json.load(open("explore/occupations_ai/s05_specs.json"))["specs"]
SPECS = list(prev)
def rec(name, r, **kw):
    d = dict(name=name, beta=r["beta"], se=r["se"], p=r["p"], p_opposite=r["p_opposite"], G=r["G"], n=r["n"],
             G_star=r.get("G_star"), mde16=inf.mde(r["se"], r["G"]), mde15=inf.mde(r["se"] * np.sqrt(r["G"] / 15), 15), **kw)
    SPECS[:] = [z for z in SPECS if z["name"] != name]; SPECS.append(d)
    print(f"  [{len(SPECS)}] {name}: b={d['beta']:.4f} se={d['se']:.4f} p={d['p']:.4f} G={d['G']} n={d['n']} "
          f"G*={d['G_star']:.2f} mde15={d['mde15']:.3f}")
    return d
raw = data.manifest_raw()
occr = raw["occ"]
occ = es.clean(occr)
w = occ.pivot_table(index=["geo", "year"], columns=["age", "isco08"], values="value")
yg, al = w["Y15-24"], w["Y15-64"]; pr = al - yg
def cells_breaks(groups):
    b = {}
    for a in ["Y15-24", "Y15-64"]:
        for i in groups + ["TOTAL"]:
            for gname, ys in es.break_years(occr[(occr.age == a) & (occr.isco08 == i)]).items():
                b.setdefault(gname, set()).update(int(t) for t in ys)
    return b
def bdum(d, b, lo):
    cols, seen = [], set()
    for gname, ys in b.items():
        m = (d.geo == gname).to_numpy()
        for t in sorted(ys):
            if t <= lo: continue
            c = (m & (d.year >= t).to_numpy()).astype(float)
            if not m.any() or c[m].min() == c[m].max() or c.tobytes() in seen: continue
            seen.add(c.tobytes()); cols.append(c)
    return np.column_stack(cols) if cols else np.zeros((len(d), 0))
def loo(fn, geos):
    out = {}
    for gname in geos:
        r = fn([x for x in geos if x != gname]); out[gname] = round(r["p"], 4)
    return out
RES = {}
# ---- E-OCC1
def e1(geos, groups=("OC4",), years=(2011, 2025), ret_d=False):
    sy = sum(yg[c] for c in groups) / yg["TOTAL"] * 100; sp = sum(pr[c] for c in groups) / pr["TOTAL"] * 100
    d = pd.concat([sy.rename("s").reset_index().assign(young=1.0), sp.rename("s").reset_index().assign(young=0.0)])
    d = d[d.geo.isin(geos) & d.year.between(*years) & ~d.year.isin([2020, 2021])].dropna().reset_index(drop=True)
    d["cy"] = d.geo + "_" + d.year.astype(str)
    # breaks: a break in a young cell shifts the young row; C3 would put 1[geo=c, year>=t] -- absorbed by cy FE, so
    # the age-specific version 1[geo=c, year>=t] x young is the one that bites
    b = cells_breaks(list(groups))
    B = bdum(d, b, years[0]) * d["young"].to_numpy()[:, None]
    Z = np.column_stack([inf.fe_matrix(d, "cy"), B])
    r = inf.wcr(d["s"].to_numpy(), d["young"].to_numpy(), Z, d.geo.to_numpy(), side=+1, B=9999)
    return (r, d) if ret_d else r
geos = data.GEOS
r = e1(geos); RES["E-OCC1"] = rec("E-OCC1 OC4 young-minus-25-64, 2011-25, cy FE + young x breaks", r, loo=loo(e1, geos))
print("    LOO p:", RES["E-OCC1"]["loo"])
r = e1(geos, years=(2011, 2019)); rec("E-OCC1 variant OC4, 2011-19", r)
r = e1(geos, groups=("OC4", "OC7", "OC8")); rec("E-OCC1 variant routine 4+7+8, 2011-25", r)
def e1nb(geos):
    sy = yg["OC4"] / yg["TOTAL"] * 100; sp = pr["OC4"] / pr["TOTAL"] * 100
    d = pd.concat([sy.rename("s").reset_index().assign(young=1.0), sp.rename("s").reset_index().assign(young=0.0)])
    d = d[d.geo.isin(geos) & d.year.between(2011, 2025) & ~d.year.isin([2020, 2021])].dropna().reset_index(drop=True)
    d["cy"] = d.geo + "_" + d.year.astype(str)
    return inf.wcr(d["s"].to_numpy(), d["young"].to_numpy(), inf.fe_matrix(d, "cy"), d.geo.to_numpy(), side=+1, B=9999)
rec("E-OCC1 variant OC4, no break dummies", e1nb(geos))
# ---- E-OCC2
def e2(geos, groups=("OC4",), base=(2022,), post=(2023, 2024, 2025)):
    Rm = np.log((sum(yg[c] for c in groups) / yg["TOTAL"]) / (sum(pr[c] for c in groups) / pr["TOTAL"]))
    d = Rm.rename("R").reset_index()
    d = d[d.geo.isin(geos) & d.year.isin(list(base) + list(post))].dropna().reset_index(drop=True)
    d = d[d.groupby("geo").year.transform(lambda s: s.isin(base).any() and s.isin(post).any())].reset_index(drop=True)
    d["post"] = d.year.isin(post).astype(float)
    Z = np.column_stack([inf.fe_matrix(d, "geo"), bdum(d, cells_breaks(list(groups)), min(base))])
    return inf.wcr(d["R"].to_numpy(), d["post"].to_numpy(), Z, d.geo.to_numpy(), side=-1, B=9999)
r = e2(geos); RES["E-OCC2"] = rec("E-OCC2 R_OC4 2023-25 vs 2022, country FE + breaks", r, loo=loo(e2, geos))
print("    LOO p:", RES["E-OCC2"]["loo"])
# within-explore what effect could have been seen? a 10% relative fall is -0.105 log points
json.dump(dict(specs=SPECS, n_specs=len(SPECS), candidates=RES), open("explore/occupations_ai/s06_specs.json", "w"), indent=1, default=str)
# figure: the stacked E-OCC1 gap by country (2011-25 mean, OC4) with LOO-sensitive countries marked
sy = yg["OC4"] / yg["TOTAL"] * 100; sp = pr["OC4"] / pr["TOTAL"] * 100
gp = (sy - sp).unstack("geo"); gp = gp.loc[[y for y in gp.index if 2011 <= y <= 2025 and y not in (2020, 2021)]]
m = gp.mean().sort_values()
fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(m.index, m.values, color=["#a33" if v < 0 else "#3b6ea8" for v in m.values])
ax.axhline(0, color="#555", lw=.8); ax.set_ylabel("pp")
ax.set_title("Clerical (OC4) share at 15-24 minus at 25-64, mean 2011-2025 (excl. 2020-21), explore half", fontsize=9)
fig.tight_layout(); fig.savefig("explore/occupations_ai/fig4_clerical_gap_by_country.png", dpi=130)
