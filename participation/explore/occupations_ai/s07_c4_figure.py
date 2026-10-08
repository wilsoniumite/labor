# s07_c4_figure.py - figure for why C-4 cannot see much: each country's share of the identifying variation
# (gamma_g, nationals and all residents) and the raw 2022 -> 2023-25 change in E2024 - E2554 against X_c.
# No new specification: the leverages are those of the frozen design (s02, s04).
import sys, json
sys.path.insert(0, "explore"); sys.path.insert(0, "code")
import data
import numpy as np, pandas as pd
import specs, inference as inf
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
cy, cl = data.panel()
ctx = specs.Ctx(cl, (cl["F_raw"].mean(), cl["F_raw"].std(ddof=0)))
lev = {}
for v in [None, "all_residents"]:
    fr = specs.frame(cy, specs.TESTS["C4"], ctx, data.GEOS, v)
    y, x, Z, g, M = specs.design(fr, ["geo", "year"])
    f = inf._Fit(y, x, Z, g)
    lev[v or "nationals"] = pd.Series(np.bincount(f.g, f.xt * f.xt) / f.xx, index=f.labels)
L = pd.DataFrame(lev).fillna(0).sort_values("nationals", ascending=False)
d = cy.reset_index(); 
fig, axs = plt.subplots(1, 2, figsize=(11, 4.2))
ax = axs[0]; i = np.arange(len(L))
ax.bar(i - 0.2, L["nationals"], 0.4, label="nationals (frozen)", color="#3b6ea8")
ax.bar(i + 0.2, L["all_residents"], 0.4, label="all residents", color="#c98a2b")
ax.set_xticks(i); ax.set_xticklabels(L.index, fontsize=8); ax.set_ylabel("share of identifying variation")
ax.legend(fontsize=8); ax.set_title("C-4: each country's weight in X_c x post-2023 (after FE and breaks)", fontsize=9)
ax = axs[1]
for col, mk, lab in [("", "o", "nationals"), ("_all", "^", "all residents")]:
    gp = (d["E2024" + col] - d["E2554" + col]).groupby([d.geo, d.year]).first().unstack("geo")
    ch = gp.loc[2023:2025].mean() - gp.loc[2022]
    ax.scatter(cl["X_c"].reindex(ch.index), ch, marker=mk, s=16, label=lab)
    if col == "_all":
        for gname in ch.index:
            if np.isfinite(ch[gname]): ax.annotate(gname, (cl.loc[gname, "X_c"], ch[gname]), fontsize=7, xytext=(3, 2), textcoords="offset points")
ax.axhline(0, color="#777", lw=.7); ax.set_xlabel("X_c: clerical share at 15-24, 2018-19 (%)")
ax.set_ylabel("change in E(20-24) - E(25-54), 2022 to 2023-25 mean, pp"); ax.legend(fontsize=8)
ax.set_title("The variation C-4 actually uses", fontsize=9)
fig.tight_layout(); fig.savefig("explore/occupations_ai/fig5_c4_anatomy.png", dpi=130)
print(L.round(3).to_string())
