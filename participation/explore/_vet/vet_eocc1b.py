import sys
sys.path.insert(0, "explore"); sys.path.insert(0, "code")
import data, numpy as np, pandas as pd
from scipy import stats
es = data.es
occ = es.clean(data.manifest_raw()["occ"])
w = occ.pivot_table(index=["geo","year"], columns=["age","isco08"], values="value")
yg, al = w["Y15-24"], w["Y15-64"]; pr = al - yg
sy = 100*yg["OC4"]/yg["TOTAL"]; sp = 100*pr["OC4"]/pr["TOTAL"]
lr = np.log(sy/sp).rename("lr").reset_index(); lr = lr[lr.year.between(2011,2019)].dropna()
m = lr.groupby("geo").lr.mean(); n = lr.groupby("geo").lr.count()
print(m.round(3).to_string())
print(f"log ratio: mean {m.mean():.3f} sd {m.std():.3f} t {m.mean()/(m.std()/4):.2f}; MDE15 a.05 {(stats.t.ppf(.95,14)+stats.t.ppf(.8,14))*m.std()/np.sqrt(15):.3f}, a.01 {(stats.t.ppf(.99,14)+stats.t.ppf(.8,14))*m.std()/np.sqrt(15):.3f}")
m5 = m[n>=5]; print(f"log ratio, >=5 yrs: mean {m5.mean():.3f} t {m5.mean()/(m5.std()/np.sqrt(len(m5))):.2f} n {len(m5)}")
g = (sy-sp).rename("g").reset_index(); g = g[g.year.between(2011,2019)].dropna()
gm = g.groupby("geo").g.mean(); gn = g.groupby("geo").g.count(); g5 = gm[gn>=5]
print(f"pp gap, >=5 yrs: mean {g5.mean():.3f} sd {g5.std():.3f} t {g5.mean()/(g5.std()/np.sqrt(len(g5))):.2f} n {len(g5)}")
# level of OC4 at 25-64 vs gap: is gap proportional to the level?
lv = sp.rename("lv").reset_index(); lv = lv[lv.year.between(2011,2019)].groupby("geo").lv.mean()
print("corr(prime OC4 level, pp gap):", np.corrcoef(lv[gm.index], gm)[0,1].round(2))
