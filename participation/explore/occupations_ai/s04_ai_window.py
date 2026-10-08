# s04_ai_window.py - the post-2023 window: (A) C-4 with the exposure GAP (young minus 25-64 clerical share) instead of the
# young's clerical share; (B) within-occupation: the young's clerical share relative to 25-64's, R = log(s4_y / s4_p),
# 2022 -> 2023-25 against its own pre-2019 path. Every estimated specification is counted in SPECS.
import sys, json
sys.path.insert(0, "explore"); sys.path.insert(0, "code")
import data
import numpy as np, pandas as pd
import specs, inference as inf
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
pd.set_option("display.width", 220)
es = data.es
SPECS = []
def rec(name, r, extra=None):
    d = dict(name=name, beta=r["beta"], se=r["se"], p=r["p"], G=r["G"], n=r["n"], G_star=r.get("G_star"),
             mde=inf.mde(r["se"], r["G"]))
    if extra: d.update(extra)
    SPECS.append(d); print(f"  [{len(SPECS)}] {name}: b={d['beta']:.4f} se={d['se']:.4f} p={d['p']:.4f} G={d['G']} n={d['n']} G*={d['G_star']:.2f} mde={d['mde']:.3f}")

raw = data.manifest_raw()
occ = es.clean(raw["occ"])
w = occ.pivot_table(index=["geo", "year"], columns=["age", "isco08"], values="value")
yg, al = w["Y15-24"], w["Y15-64"]; pr = al - yg
s4y = yg["OC4"] / yg["TOTAL"] * 100; s4p = pr["OC4"] / pr["TOTAL"] * 100
gap = (s4y - s4p).unstack("geo")
Xgap = gap.loc[2018:2019].mean()
cy, cl = data.panel()
print("exposure gap 2018-19:", Xgap.round(2).sort_values().to_dict())
print("corr with X_c:", round(np.corrcoef(Xgap.reindex(cl.index), cl["X_c"])[0, 1], 3))

# (A) the C-4 frame with X replaced by the gap
spec = specs.TESTS["C4"]
for nm, X in [("C4 frozen X_c", cl["X_c"]), ("C4 exposure gap", Xgap.reindex(cl.index))]:
    for variant in [None, "all_residents"]:
        ctx = specs.Ctx(cl, (cl["F_raw"].mean(), cl["F_raw"].std(ddof=0)))
        ctx.X = X
        fr = specs.frame(cy, spec, ctx, data.GEOS, variant)
        y, x, Z, g, M = specs.design(fr, spec["fe"])
        r = inf.wcr(y, x, Z, g, side=-1, B=9999)
        f = inf._Fit(y, x, Z, g)
        gam = pd.Series(np.bincount(f.g, f.xt * f.xt) / f.xx, index=f.labels).sort_values(ascending=False)
        if nm != "C4 frozen X_c" or variant:
            rec(f"{nm} [{variant or 'nationals'}]", r, dict(top_leverage=gam.head(3).round(3).to_dict()))
        else:
            print("  (frozen C-4 reproduced, not counted)", round(r["beta"], 4), round(r["p"], 4))
        print("     top leverage:", gam.head(3).round(3).to_dict(), "geos:", sorted(set(M.geo)))

# (B) R = log(s4_y/s4_p) and the same for OC8 and routine
def R(code_list):
    ny = sum(yg[c] for c in code_list) / yg["TOTAL"]; npr = sum(pr[c] for c in code_list) / pr["TOTAL"]
    return np.log(ny / npr).unstack("geo")
res = {}
for lab, cl_ in [("OC4", ["OC4"]), ("OC48", ["OC4", "OC8"]), ("ROUT", ["OC4", "OC7", "OC8"])]:
    Rm = R(cl_)
    print(f"\nR = log(young share / 25-64 share), {lab}")
    print(Rm.loc[2011:2025].round(2).to_string())
    res[lab] = Rm
    # change 2022 -> mean(2023-25), country by country
    post = Rm.loc[2023:2025].mean() - Rm.loc[2022]
    pre = (Rm.loc[2016:2019].mean() - Rm.loc[2011:2014].mean()) / 5 * 2   # pre-trend per 2 years (comparable span)
    print(f"  change 2022->2023-25 mean: {post.mean():.3f} (sd {post.std():.3f}, n {post.notna().sum()}); "
          f"pre slope over a 2-yr span: {pre.mean():.3f}")
    # panel test: R on post2023 dummy, country FE, years 2022-2025, clusters = country (no year FE possible)
    d = Rm.loc[2022:2025].stack().rename("R").reset_index()
    d["post"] = (d["year"] >= 2023).astype(float)
    Z = inf.fe_matrix(d, "geo")
    r = inf.wcr(d["R"].to_numpy(), d["post"].to_numpy(), Z, d["geo"].to_numpy(), side=-1, B=9999)
    rec(f"R_{lab} post2023 vs 2022, country FE, 2022-25", r)
# figure: R_OC4 by country
fig, ax = plt.subplots(figsize=(8, 4.5)); ax.set_prop_cycle(color=plt.cm.tab20(np.linspace(0, 1, 16)))
for gname in res["OC4"].columns:
    s = res["OC4"][gname].loc[2011:2025]
    ax.plot(s.index, s.values, lw=1, alpha=.8, label=gname)
ax.axvspan(2019.5, 2021.5, color="#ddd", alpha=.6); ax.axvline(2022.5, color="#a33", lw=.8, ls="--")
ax.set_ylabel("log(clerical share at 15-24 / at 25-64)"); ax.legend(ncol=8, fontsize=7, loc="lower center")
ax.set_title("Young relative clerical share by country, explore half", fontsize=10)
fig.tight_layout(); fig.savefig("explore/occupations_ai/fig2_relative_clerical_share.png", dpi=130)
json.dump(dict(specs=SPECS, Xgap=Xgap.to_dict()), open("explore/occupations_ai/s04_specs.json", "w"), indent=1, default=str)
