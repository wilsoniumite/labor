# vet_eocc1.py - adversarial checks on E-OCC1 (explore half only, manifest raw frames only)
import sys, itertools
sys.path.insert(0, "explore"); sys.path.insert(0, "code")
import data, numpy as np, pandas as pd
import inference as inf
es = data.es
raw = data.manifest_raw(); occr = raw["occ"]
print(occr.columns.tolist()); print(occr.head(3).to_string())
occ = es.clean(occr)
# 1. missingness from C4: which OC4/TOTAL cells are blanked at 15-24 / 15-64, 2011-2025
r = occr[occr.isco08.isin(["OC4","TOTAL"]) & occr.year.between(2011,2025)]
fl = r[r.flag.fillna("").str.contains("u|c")]
print("\nu/c flagged cells (OC4/TOTAL), 2011-25:"); print(fl.groupby(["geo","age","isco08"]).year.apply(list).to_string())
bf = r[r.flag.fillna("").str.contains("b")]
print("\nb flags:"); print(bf.groupby(["geo","age","isco08"]).year.apply(list).to_string())
w = occ.pivot_table(index=["geo","year"], columns=["age","isco08"], values="value")
yg, al = w["Y15-24"], w["Y15-64"]; pr = al - yg
sy = 100*yg["OC4"]/yg["TOTAL"]; sp = 100*pr["OC4"]/pr["TOTAL"]
gap = (sy-sp).rename("gap").reset_index()
gap = gap[gap.year.between(2011,2025) & ~gap.year.isin([2020,2021])]
# raw (uncleaned) values for flagged young cells: what are they?
rv = occr.pivot_table(index=["geo","year"], columns=["age","isco08"], values="value")
rsy = 100*rv["Y15-24"]["OC4"]/rv["Y15-24"]["TOTAL"]; rsp = 100*(rv["Y15-64"]["OC4"]-rv["Y15-24"]["OC4"])/(rv["Y15-64"]["TOTAL"]-rv["Y15-24"]["TOTAL"])
rg = (rsy-rsp).rename("rawgap").reset_index()
mm = gap.merge(rg, on=["geo","year"], how="right")
mm = mm[mm.year.between(2011,2025) & ~mm.year.isin([2020,2021])]
miss = mm[mm.gap.isna() & mm.rawgap.notna()]
print("\ncells blanked by C4 but with a raw value (gap if kept):"); print(miss.to_string())
print("young OC4 thousands, min by country 2011-19:"); print(yg["OC4"].unstack("geo").loc[2011:2019].min().round(1).to_string())
# 2. country means and year-by-year signs, 2011-19
g1 = gap[gap.year<=2019].dropna()
cm = g1.groupby("geo").gap.agg(["mean","min","max","count"])
cm["npos"] = g1.groupby("geo").gap.apply(lambda s:(s>0).sum())
print("\ncountry gaps 2011-19:"); print(cm.round(2).to_string())
m = cm["mean"]; print(f"mean {m.mean():.3f} sd {m.std():.3f} t {m.mean()/(m.std()/np.sqrt(len(m))):.2f} n {len(m)} npos {(m>0).sum()}")
# exact sign-flip test on country means
vals = m.to_numpy(); obs = vals.mean(); cnt=0; tot=0
for s in itertools.product([1,-1], repeat=len(vals)):
    tot+=1; cnt += (np.mean(vals*np.array(s)) >= obs-1e-12)
print("exact sign-flip one-sided p (country means):", cnt/tot)
# median / trimmed
print("median", np.median(vals), "mean without CH,MT", m.drop(["CH","MT"]).mean(), "t", m.drop(["CH","MT"]).mean()/(m.drop(["CH","MT"]).std()/np.sqrt(14)))
# drop-two worst-case: drop the 2 largest
for k in [1,2,3]:
    v = np.sort(vals)[:-k]; print(f"drop top {k}: mean {v.mean():.2f} t {v.mean()/(v.std(ddof=1)/np.sqrt(len(v))):.2f}")
# 3. 2022-25 era alone (post-2021 break), country means
g2 = gap[gap.year>=2022].dropna(); m2 = g2.groupby("geo").gap.mean()
print(f"\n2022-25: mean {m2.mean():.2f} sd {m2.std():.2f} t {m2.mean()/(m2.std()/np.sqrt(len(m2))):.2f} n {len(m2)} npos {(m2>0).sum()}")
# 4. WCR on the gap with country FE? (gap on const via stacked spec, no breaks), and with log ratio outcome
def stacked(outy, outp, years, logratio=False):
    d = pd.concat([outy.rename("s").reset_index().assign(young=1.0), outp.rename("s").reset_index().assign(young=0.0)])
    d = d[d.year.between(*years) & ~d.year.isin([2020,2021])].dropna().reset_index(drop=True)
    d = d[d.groupby(["geo","year"]).s.transform("count")==2].reset_index(drop=True)
    if logratio: d["s"]=np.log(d.s)
    d["cy"]=d.geo+"_"+d.year.astype(str)
    return inf.wcr(d.s.to_numpy(), d.young.to_numpy(), inf.fe_matrix(d,"cy"), d.geo.to_numpy(), side=+1, B=9999), d
r1,d1 = stacked(sy,sp,(2011,2019)); print("\nstacked 2011-19 no breaks:", {k:r1[k] for k in ["beta","se","p","G","n"]})
r2,_ = stacked(sy,sp,(2011,2019),True); print("log ratio 2011-19:", {k:r2[k] for k in ["beta","se","p","G","n"]})
r3,_ = stacked(sy,sp,(2022,2025)); print("stacked 2022-25:", {k:r3[k] for k in ["beta","se","p","G","n"]})
# country-mean weighting: weight each country equally (C8) - compare to country-year weighting
print("country-year weighted mean of gap 2011-19:", g1.gap.mean(), " country-equal:", m.mean())
# 5. MDE on 15 clusters from country-mean sd, Holm worst-case alpha 0.01, power .8, t_14
from scipy import stats
for a in [0.05, 0.0125, 0.01]:
    mde = (stats.t.ppf(1-a,14)+stats.t.ppf(0.8,14))*m.std()/np.sqrt(15)
    print(f"MDE15 alpha {a}: {mde:.2f}")
se15 = m.std()/np.sqrt(15)
for a in [0.05,0.01]:
    crit = stats.t.ppf(1-a,14); print(f"power at true {m.mean():.2f}, alpha {a}: {1-stats.nct.cdf(crit,14,m.mean()/se15):.2f}; at half: {1-stats.nct.cdf(crit,14,0.5*m.mean()/se15):.2f}")
