# s03_young_gap.py - do the young hold more of the contestable (routine/clerical) tasks?
# Computed the manifest way: 25-64 = 15-64 minus 15-24 (lfsa_egais THS_PER, sex T); C4 (u/c cells missing).
# Checked against the direct 25-54 cells of the EXTRA series.
import sys, json
sys.path.insert(0, "explore")
import data
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
pd.set_option("display.width", 220)
es = data.es
raw = data.manifest_raw()
occ = es.clean(raw["occ"])
w = occ.pivot_table(index=["geo", "year"], columns=["age", "isco08"], values="value")
y = w["Y15-24"]; a = w["Y15-64"]; p = a - y                # 25-64
def shares(t):
    s = pd.DataFrame({"OC4": t["OC4"], "OC7": t["OC7"], "OC8": t["OC8"]}).div(t["TOTAL"], axis=0) * 100
    s["OC48"] = s["OC4"] + s["OC8"]; s["ROUT"] = s["OC4"] + s["OC7"] + s["OC8"]
    return s
sy, sp = shares(y), shares(p)
gap = sy - sp
gap.to_csv("explore/occupations_ai/gap_young_minus_2564.csv")
out = {}
for c in ["OC4", "OC8", "OC48", "ROUT", "OC7"]:
    g = gap[c].unstack("geo")
    m1, m2 = g.loc[2011:2019].mean(), g.loc[2022:2025].mean()
    out[c] = dict(m1119=m1.round(2).to_dict(), m2225=m2.round(2).to_dict())
    print(f"\n{c}: young (15-24) minus 25-64 share, pp. mean 2011-19 / 2022-25")
    print(pd.DataFrame({"2011-19": m1, "2022-25": m2}).round(2).T.to_string())
    v = m1.dropna()
    print(f"  across countries 2011-19: mean {v.mean():.2f}, sd {v.std():.2f}, n {len(v)}, positive {int((v>0).sum())}")
# direct 25-54 check
ex = data.extra("occ"); ex = ex[ex.sex == "T"]
d54 = ex.pivot_table(index=["geo", "year"], columns=["age", "isco08"], values="value")["Y25-54"]
s54 = shares(d54)
print("\nOC4 share 25-64 (manifest) vs 25-54 (direct), 2015:")
print(pd.DataFrame({"25-64": sp["OC4"].xs(2015, level="year"), "25-54": s54["OC4"].xs(2015, level="year")}).round(2).T.to_string())
# figure: young vs prime clerical share, 2011-19 mean
fig, axs = plt.subplots(1, 3, figsize=(13, 4.3))
for ax, c, lab in zip(axs, ["OC4", "OC48", "ROUT"], ["Clerical (OC4)", "Clerical + operators (OC4+OC8)", "Routine (OC4+OC7+OC8)"]):
    a1 = sp[c].unstack("geo").loc[2011:2019].mean(); b1 = sy[c].unstack("geo").loc[2011:2019].mean()
    ax.scatter(a1, b1, s=14, color="#3b6ea8")
    for gname in a1.index:
        if np.isfinite(a1[gname]) and np.isfinite(b1[gname]):
            ax.annotate(gname, (a1[gname], b1[gname]), fontsize=8, xytext=(3, 2), textcoords="offset points")
    lo = np.nanmin([a1.min(), b1.min()]) - 1; hi = np.nanmax([a1.max(), b1.max()]) + 1
    ax.plot([lo, hi], [lo, hi], color="#999", lw=0.8)
    ax.set_title(lab, fontsize=10); ax.set_xlabel("share at 25-64, % (2011-19 mean)"); ax.set_ylabel("share at 15-24, %")
fig.tight_layout(); fig.savefig("explore/occupations_ai/fig1_young_vs_prime_shares.png", dpi=130)
json.dump(out, open("explore/occupations_ai/young_gap.json", "w"), indent=1)
