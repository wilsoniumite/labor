# s05_aging.py - aging against the routine decline (C-5): what the cross-section holds, a panel version, and a
# shift-share split of the 2011-2019 routine change into within-age and between-age (15-24 vs 25-64) parts.
import sys, json
sys.path.insert(0, "explore"); sys.path.insert(0, "code")
import data
import numpy as np, pandas as pd
import specs, inference as inf
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
pd.set_option("display.width", 220)
es = data.es
prev = json.load(open("explore/occupations_ai/s04_specs.json"))["specs"]
SPECS = list(prev)
def rec(name, r):
    d = dict(name=name, beta=r["beta"], se=r["se"], p=r["p"], G=r["G"], n=r["n"], G_star=r.get("G_star"), mde=inf.mde(r["se"], r["G"]))
    SPECS[:] = [z for z in SPECS if z["name"] != name]; SPECS.append(d); print(f"  [{len(SPECS)}] {name}: b={d['beta']:.4f} se={d['se']:.4f} p={d['p']:.4f} G={d['G']} n={d['n']} G*={d['G_star']:.2f} mde={d['mde']:.3f}")
raw = data.manifest_raw()
cy, cl = data.panel()
# C-4 leave CH out (which country dominates)
spec = specs.TESTS["C4"]; ctx = specs.Ctx(cl, (cl["F_raw"].mean(), cl["F_raw"].std(ddof=0)))
fr = specs.frame(cy, spec, ctx, [g for g in data.GEOS if g != "CH"])
y, x, Z, g, M = specs.design(fr, spec["fe"])
r = inf.wcr(y, x, Z, g, side=-1, B=9999); rec("C4 frozen, CH left out", r)
f = inf._Fit(y, x, Z, g)
print("    leverage without CH:", pd.Series(np.bincount(f.g, f.xt * f.xt) / f.xx, index=f.labels).sort_values(ascending=False).head(3).round(3).to_dict())

# population ratios per year (actual), 56+ / 21-55
pop = es.clean(raw["pop"])
pop = pd.concat([pop[pop.age != "Y_OPEN"].assign(a=lambda d: d.age.str[1:].astype(int)),
                 pop[pop.age == "Y_OPEN"].assign(a=100)])
pv = pop.pivot_table(index=["geo", "year"], columns="a", values="value")
old = pv[[c for c in pv.columns if c >= 56]].sum(1, min_count=1); wk = pv[[c for c in pv.columns if 21 <= c <= 55]].sum(1, min_count=1)
ratio = (old / wk).rename("old_ratio")
young_pop = (pv[[c for c in pv.columns if 15 <= c <= 24]].sum(1) / pv[[c for c in pv.columns if 25 <= c <= 64]].sum(1)).rename("young_pop_ratio")
rt = ratio.unstack("geo")
print("\nactual 56+/21-55, 2011 and 2019 and 2025, and change 2011-19:")
print(pd.DataFrame({"2011": rt.loc[2011], "2019": rt.loc[2019], "2025": rt.loc[2025], "d1119": rt.loc[2019] - rt.loc[2011]}).round(3).T.to_string())
_c = pd.DataFrame({"a": rt.loc[2019] - rt.loc[2011], "p": cl["aging_pred"]}).dropna()
print("corr(actual d1119, aging_pred):", round(_c.corr().iloc[0, 1], 3))

# occupation shares
occ = es.clean(raw["occ"])
w = occ.pivot_table(index=["geo", "year"], columns=["age", "isco08"], values="value")
yg, al = w["Y15-24"], w["Y15-64"]; pr = al - yg
rout = lambda t: (t["OC4"] + t["OC7"] + t["OC8"]) / t["TOTAL"] * 100
R_all = rout(al).unstack("geo")
# shift-share 2011 -> 2019: aggregate routine share = sum_a e_a * s_a; between = sum (e_a19 - e_a11) * s_a11
rows = []
for gname in data.GEOS:
    try:
        e11y = yg.loc[(gname, 2011), "TOTAL"] / al.loc[(gname, 2011), "TOTAL"]; e19y = yg.loc[(gname, 2019), "TOTAL"] / al.loc[(gname, 2019), "TOTAL"]
        sy11, sy19 = rout(yg).loc[(gname, 2011)], rout(yg).loc[(gname, 2019)]
        sp11, sp19 = rout(pr).loc[(gname, 2011)], rout(pr).loc[(gname, 2019)]
    except KeyError:
        continue
    tot = (e19y * sy19 + (1 - e19y) * sp19) - (e11y * sy11 + (1 - e11y) * sp11)
    between = (e19y - e11y) * (sy11 - sp11)
    rows.append(dict(geo=gname, total=tot, between_age=between, within_young=e11y * (sy19 - sy11), within_2564=(1 - e11y) * (sp19 - sp11),
                     young_emp_share_11=e11y * 100, young_emp_share_19=e19y * 100))
ss = pd.DataFrame(rows).set_index("geo")
print("\nshift-share of the 2011-2019 routine-share change (pp):"); print(ss.round(2).to_string())

# panel: routine share 15-64 on actual old ratio, country+year FE, break dummies from the occ cells, 2011-2025 excl 2020-21
br = {}
for i in ["OC4", "OC7", "OC8", "TOTAL"]:
    for gname, ys in es.break_years(raw["occ"][(raw["occ"].age == "Y15-64") & (raw["occ"].isco08 == i)]).items():
        br.setdefault(gname, set()).update(ys)
d = pd.DataFrame({"rout": rout(al), "old": ratio, "U": cy["U"]}).reset_index()
d = d[(d.year >= 2011) & ~d.year.isin([2020, 2021])].dropna()
bd = [((d.geo == gname) & (d.year >= t)).astype(float).to_numpy() for gname, ys in br.items() for t in ys if 2011 < t <= 2025]
bd = [b for b in bd if b[(d.geo == d.geo.iloc[0]).to_numpy()].std() >= 0 and b.std() > 0]
for nm, Zx in [("panel rout~old_ratio FE+breaks", np.column_stack([inf.fe_matrix(d, ["geo", "year"])] + bd)),
               ("panel rout~old_ratio FE+breaks+U", np.column_stack([inf.fe_matrix(d, ["geo", "year"]), d[["U"]].to_numpy()] + bd))]:
    r = inf.wcr(d["rout"].to_numpy(), d["old"].to_numpy(), Zx, d["geo"].to_numpy(), side=-1, B=9999); rec(nm, r)
# figure: C-5 scatter
fig, axs = plt.subplots(1, 2, figsize=(10, 4.2))
ax = axs[0]
ax.scatter(cl["aging_pred"], cl["routine_change"], s=14, color="#3b6ea8")
for gname in cl.index:
    if np.isfinite(cl.loc[gname, "aging_pred"]): ax.annotate(gname, (cl.loc[gname, "aging_pred"], cl.loc[gname, "routine_change"]), fontsize=8, xytext=(3, 2), textcoords="offset points")
ax.set_xlabel("predicted aging 2011-19 (C-5 regressor)"); ax.set_ylabel("routine share change 2011-19, pp"); ax.set_title("C-5 cross-section, explore half", fontsize=10)
ax = axs[1]
ax.bar(ss.index, ss["total"], color="#bbb", label="total")
ax.bar(ss.index, ss["between_age"], color="#a33", label="between ages (fewer young)")
ax.set_ylabel("pp, 2011-19"); ax.legend(fontsize=8); ax.set_title("Routine-share change and its age-composition part", fontsize=10)
fig.tight_layout(); fig.savefig("explore/occupations_ai/fig3_aging_routine.png", dpi=130)
json.dump(dict(specs=SPECS, shift_share=ss.to_dict()), open("explore/occupations_ai/s05_specs.json", "w"), indent=1, default=str)
