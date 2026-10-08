# describe.py — the picture: q and its alternatives, coresidence, overburden, rental-market size, per explore country.
# Out: fig/q_measures.png, fig/cores_act.png, fig/overburden.png, describe.json (tables), printed summary.

import json
import os

import numpy as np
import pandas as pd

import common as C

raw, cy, cl = C.load()
plt = C.style()
geos = sorted(set(cy.index.get_level_values(0)))
d = cy.reset_index()
# un-lagged versions for the picture
h = raw["hicp"]
hic = {c: build_s for c, build_s in ((c, C.build.cell(h, coicop=c)[0]) for c in ("CP041", "IGD_NNRG", "CP00"))}
comp = C.build.cell(raw["comp"])[0]
hpi = C.build._per_country_unit(raw["hpi"], ["I15_A_AVG", "I25_A_AVG"])[0]
P = pd.DataFrame({"cp041": hic["CP041"], "nnrg": hic["IGD_NNRG"], "cp00": hic["CP00"]})
P = P.join(comp.rename("comp"), how="left").join(hpi.rename("hpi"), how="left")
P["lq"] = np.log(P.cp041 / P.nnrg)
P["lq_cp00"] = np.log(P.cp041 / P.cp00)
P["lq_comp"] = np.log(P.cp041 / P.comp)
P["lq_hpi"] = np.log(P.hpi / P.cp00)
P = P.reset_index()
P = P[(P.year >= 1996) & (P.year <= 2025)]

# extra series (understanding only)
ten = C.data.extra("tenure")
ob = C.data.extra("overburden")
cores_x = C.data.extra("cores")

rows = []
for g in geos:
    p = P[P.geo == g].set_index("year")
    r = dict(geo=g)
    for v in ("lq", "lq_cp00", "lq_comp", "lq_hpi"):
        s = p[v].dropna()
        r[v + "_first"] = int(s.index.min()) if len(s) else None
        r[v + "_change"] = float(s.iloc[-1] - s.iloc[0]) if len(s) > 1 else np.nan
        r[v + "_sd"] = float(s.std()) if len(s) > 1 else np.nan
        # sd of the detrended (linear) series: how much movement is left after a country trend
        if len(s) > 4:
            t = s.index.to_numpy(float)
            res = s.to_numpy() - np.polyval(np.polyfit(t, s.to_numpy(), 1), t)
            r[v + "_sd_detr"] = float(res.std())
    # CP041 behaviour: sd of annual log changes, largest jump, correlation of rent growth with HPI and comp growth
    dl = np.log(p["cp041"]).diff()
    r["cp041_dlog_sd"] = float(dl.std())
    r["cp041_dlog_max"] = float(dl.abs().max())
    r["cp041_dlog_max_year"] = int(dl.abs().idxmax()) if dl.notna().any() else None
    r["cp041_growth_pa"] = float(np.log(p.cp041.dropna().iloc[-1] / p.cp041.dropna().iloc[0]) /
                                 (p.cp041.dropna().index[-1] - p.cp041.dropna().index[0]))
    for other in ("hpi", "comp", "cp00"):
        x = pd.concat([dl, np.log(p[other]).diff()], axis=1).dropna()
        r[f"corr_drent_d{other}"] = float(x.corr().iloc[0, 1]) if len(x) > 4 else np.nan
    # rental market size (ilc_lvps05, 2015-2017 means), 25-34 and all ages
    for age in ("Y25-34", "TOTAL"):
        for tn in ("RENT_MKT", "RENT_FR", "OWN_NL", "OWN_L"):
            s = ten[(ten.geo == g) & (ten.age == age) & (ten.tenure == tn) & ten.year.between(2015, 2017)]["value"]
            r[f"{tn}_{age}"] = float(s.mean()) if len(s) else np.nan
    # overburden of the young (25-29) and of all, 2010-2019 mean and first available
    for age in ("Y25-29", "TOTAL"):
        s = ob[(ob.geo == g) & (ob.age == age)].set_index("year")["value"].dropna()
        r[f"overb_{age}_1019"] = float(s.loc[2010:2019].mean()) if len(s.loc[2010:2019]) else np.nan
        r[f"overb_{age}_first"] = (int(s.index.min()), float(s.iloc[0])) if len(s) else None
    c = cy.loc[g]
    r["F_raw"] = float(cl.loc[g, "F_raw"])
    r["cores_mean"] = float(c["coresid2534"].mean())
    s = c["coresid2534"].dropna()
    r["cores_change"] = float(s.iloc[-1] - s.iloc[0]) if len(s) > 1 else np.nan
    a = c["A2534"].dropna()
    r["A2534_first"] = (int(a.index.min()), float(a.iloc[0])) if len(a) else None
    r["A2534_last"] = (int(a.index.max()), float(a.iloc[-1])) if len(a) else None
    rows.append(r)
T = pd.DataFrame(rows).set_index("geo")
pd.set_option("display.width", 250, "display.max_columns", 40)
print(T[["lq_first", "lq_change", "lq_sd", "lq_sd_detr", "lq_cp00_change", "lq_comp_change", "lq_hpi_first",
         "lq_hpi_change", "lq_hpi_sd_detr"]].round(3))
print(T[["cp041_growth_pa", "cp041_dlog_sd", "cp041_dlog_max", "cp041_dlog_max_year", "corr_drent_dhpi",
         "corr_drent_dcomp", "corr_drent_dcp00"]].round(3))
print(T[["RENT_MKT_Y25-34", "RENT_FR_Y25-34", "RENT_MKT_TOTAL", "OWN_NL_TOTAL", "overb_Y25-29_1019",
         "overb_TOTAL_1019", "F_raw", "cores_mean", "cores_change", "A2534_first", "A2534_last"]].round(1))

# within-country variation left after country and year FE (what D1/D2 identify from)
for v in ("logq_l1", "logq_hpi_l1", "logq_comp_l1", "logq_cp00_l1"):
    for lo in (1997, 2009):
        x = d[(d.year >= lo) & d[v].notna()][["geo", "year", v]]
        Z = C.inf.fe_matrix(x, ["geo", "year"])
        Q = C.inf._basis(Z)
        e = x[v].to_numpy() - Q @ (Q.T @ x[v].to_numpy())
        x = x.assign(res=e)
        print(f"{v} from {lo}: n={len(x)} sd(raw)={x[v].std():.3f} sd(two-way FE residual)={e.std():.3f}; "
              f"by country:", x.groupby("geo")["res"].std().round(3).to_dict())

# square term in D2: how much curvature support is there? range of (lq - m_c) within each country
x = d[(d.year >= 1997) & d.logq_l1.notna()].copy()
x["dev"] = x.logq_l1 - x.groupby("geo").logq_l1.transform("mean")
print("range of log q deviation (1997+):", x.groupby("geo").dev.agg(lambda s: s.max() - s.min()).round(3).to_dict())
x9 = d[(d.year >= 2009) & d.logq_l1.notna()].copy()
x9["dev"] = x9.logq_l1 - x9.groupby("geo").logq_l1.transform("mean")
print("range of log q deviation (2009+):", x9.groupby("geo").dev.agg(lambda s: s.max() - s.min()).round(3).to_dict())
T.to_json(os.path.join(C.HERE, "describe.json"), orient="index", indent=1)

# ---------------------------------------------------------------- figures
fig, axs = plt.subplots(4, 4, figsize=(11, 9), sharex=True)
for ax, g in zip(axs.flat, geos):
    p = P[P.geo == g].set_index("year")
    for v, col, lab in (("lq", C.BLUE, "rent / non-energy goods (q)"), ("lq_comp", C.ORANGE,
                                                                         "rent / compensation per employee"),
                        ("lq_hpi", C.AQUA, "house prices / all items")):
        s = p[v].dropna()
        if len(s):
            base = s.loc[2015] if 2015 in s.index else s.iloc[0]
            ax.plot(s.index, s - base, color=col, label=lab)
    ax.axhline(0, color=C.GRAY, lw=0.6)
    ax.set_title(g + (" (CEE)" if g in C.CEE else ""), loc="left")
fig.legend(*axs.flat[0].get_legend_handles_labels(), loc="lower center", ncol=3)
fig.suptitle("Log relative prices, 0 = 2015, explore half", x=0.01, ha="left", color=C.INK)
fig.tight_layout(rect=(0, 0.04, 1, 0.97))
fig.savefig(os.path.join(C.FIG, "q_measures.png"), dpi=130)

fig, axs = plt.subplots(4, 4, figsize=(11, 9), sharex=True)
for ax, g in zip(axs.flat, geos):
    c = cy.loc[g]
    ax.plot(c.index, c["A2534"], color=C.BLUE, label="activity rate 25-34 (nationals, %)")
    ax.plot(c.index, c["coresid2534"], color=C.ORANGE, label="25-34 living with parents (%)")
    ax.plot(c.index, c["U"], color=C.AQUA, label="unemployment 25-74 (frozen C7 source, %)")
    ax.set_ylim(0, 100)
    ax.set_title(f"{g}  F_raw={cl.loc[g, 'F_raw']:.0f}", loc="left")
fig.legend(*axs.flat[0].get_legend_handles_labels(), loc="lower center", ncol=3)
fig.suptitle("Participation, coresidence and the cycle, explore half (2020-21 dropped)", x=0.01, ha="left",
             color=C.INK)
fig.tight_layout(rect=(0, 0.04, 1, 0.97))
fig.savefig(os.path.join(C.FIG, "cores_act.png"), dpi=130)

fig, axs = plt.subplots(4, 4, figsize=(11, 9), sharex=True)
for ax, g in zip(axs.flat, geos):
    for age, col, lab in (("Y25-29", C.BLUE, "25-29"), ("TOTAL", C.ORANGE, "all ages")):
        s = ob[(ob.geo == g) & (ob.age == age)].set_index("year")["value"].dropna().sort_index()
        ax.plot(s.index, s, color=col, label=lab)
    ax.set_title(g, loc="left")
fig.legend(*axs.flat[0].get_legend_handles_labels(), loc="lower center", ncol=2)
fig.suptitle("Housing cost overburden rate (%), ilc_lvho07a, explore half", x=0.01, ha="left", color=C.INK)
fig.tight_layout(rect=(0, 0.04, 1, 0.97))
fig.savefig(os.path.join(C.FIG, "overburden.png"), dpi=130)
print("figures written")
