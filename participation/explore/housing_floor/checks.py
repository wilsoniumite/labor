# checks.py — what drives the D1/D2 estimates: leave-one-out, trends x q measure, moderators other than F,
# CP041 informativeness (small rental markets), and what D2's square actually measures when q trends.
# Out: checks.json; every estimate logged to specs_log.jsonl.

import json
import os

import numpy as np
import pandas as pd

import common as C

raw, cy, cl = C.load()
cyl = C.with_lfs_cycle(raw, cy)
geos = sorted(set(cy.index.get_level_values(0)))
out = {}
B = 9999


def go(label, frame, base, cl_=None, B=B, **over):
    r = C.run(label, frame, cl if cl_ is None else cl_, base=base, B=B, **over)
    out[label] = {k: r.get(k) for k in ("beta", "se", "p", "p_opposite", "n", "G", "G_star", "geos_used")}
    out[label]["years"] = [min(r["years_used"]), max(r["years_used"])]
    print(f"{label:58s} {C.fmt(r)}")
    return r


def swap_q(frame, col):
    f = frame.copy()
    f["logq_l1"] = f[col]
    f["logq_l1__breaks"] = f[col + "__breaks"]
    return f


# 1. D1 with country trends: the q measure, the window, and leave-one-out
print("--- D1 with country trends")
for qc in ("logq_cp00_l1", "logq_comp_l1", "logq_hpi_l1"):
    go(f"D1 long trends, {qc}", swap_q(cyl, qc), "D1", variant="country_trends")
go("D1 trends, lfsa_urgan U, 2009+", cyl, "D1", variant="country_trends", years=(2009, 2025))
go("D1 trends, lfsa_urgan U, 1997-2019", cyl, "D1", variant="country_trends", years=(1997, 2019))
go("D1 trends, no cycle control, 1997+", cy, "D1", variant="country_trends", controls=[])
loo = {}
for g in geos:
    if not np.isfinite(cl.loc[g, "F_raw"]):
        continue
    r = C.run(f"D1 long trends LOO -{g}", cyl, cl, base="D1", B=B, variant="country_trends",
              geos=[c for c in geos if c != g])
    loo[g] = dict(beta=r["beta"], se=r["se"], p=r["p"])
    print(f"   leave out {g}: b={r['beta']:+.2f} se={r['se']:.2f} p={r['p']:.3f}")
out["D1 long trends LOO"] = loo

# 2. D1 without CEE (CP041 in small, regulated rental markets) and on large-rental-market countries
ten = C.data.extra("tenure")                       # understanding only
rent = (ten[(ten.age == "Y25-34") & (ten.tenure == "RENT_MKT") & ten.year.between(2015, 2017)]
        .groupby("geo")["value"].mean())
print("--- D1 by rental-market size / region")
nocee = [g for g in geos if g not in C.CEE]
for lab, gs in (("no CEE", nocee), ("RENT_MKT 25-34 >= 15%", [g for g in geos if rent.get(g, 0) >= 15])):
    print("   ", lab, gs)
    go(f"D1 long, {lab}", cyl, "D1", geos=gs)
    go(f"D1 long trends, {lab}", cyl, "D1", geos=gs, variant="country_trends")

# 3. other moderators in F's place (all standardised over the countries used)
ob = C.data.extra("overburden")                    # understanding only
ob_y = ob[(ob.age == "Y25-29") & ob.year.between(2005, 2010)].groupby("geo")["value"].mean()
mods = {"outright owners 55-64 (manifest)": cl["owner_outright_5564"],
        "overburden 25-29 2005-2010 (not manifest)": ob_y,
        "market renters 25-34 (not manifest)": rent}
print("--- D1 with other moderators")
for lab, m in mods.items():
    cl2 = cl.copy()
    cl2["F_raw"] = m.reindex(cl2.index)
    go(f"D1 long, moderator = {lab}", cyl, "D1", cl_=cl2)
    go(f"D1 long trends, moderator = {lab}", cyl, "D1", cl_=cl2, variant="country_trends")
print("    moderators:", pd.DataFrame({k: v.reindex(geos) for k, v in mods.items()} | {"F_raw": cl["F_raw"]}).round(1))

# 4. D2: what the square measures when q trends
d = cyl.reset_index()
d = d[(d.year >= 1997) & d.logq_l1.notna() & d.A2534.notna()].copy()
d["dev"] = d.logq_l1 - d.groupby("geo").logq_l1.transform("mean")
d["sq"] = d.dev ** 2
d["tc"] = d.year - d.groupby("geo").year.transform("mean")
cors = {}
for g, x in d.groupby("geo"):
    cors[g] = float(np.corrcoef(x.sq, x.tc ** 2)[0, 1]) if len(x) > 3 else np.nan
print("--- D2: within-country corr of (log q - m_c)^2 with (t - tbar_c)^2:", {k: round(v, 2) for k, v in cors.items()})
out["D2 corr sq with quadratic time"] = cors
fr = C.specs.frame(cyl, C.specs.TESTS["D2"], C.specs.Ctx(cl, C.specs.f_constants(cl, geos)), geos)
M = fr["M"]
Q = C.inf._basis(C.inf.fe_matrix(M, ["geo", "year"]))
xt = M.x.to_numpy() - Q @ (Q.T @ M.x.to_numpy())
share = pd.Series(xt ** 2, index=M.geo).groupby(level=0).sum()
share = (share / share.sum()).sort_values(ascending=False)
print("    share of D2's identifying variation (sum of squared partialled x) by country:", share.round(3).to_dict())
out["D2 leverage share"] = share.to_dict()

# D2 with country-specific quadratic time trends (the square of a trending q is close to a quadratic trend)
def d2_quad(frame, years=(1997, 2025), label=""):
    s = dict(C.specs.TESTS["D2"]); s["years"] = years
    fr = C.specs.frame(frame, s, C.specs.Ctx(cl, C.specs.f_constants(cl, geos)), geos)
    M = fr["M"]
    t = (M.year.to_numpy(float) - 2010) / 10
    G = sorted(set(M.geo))
    Z = np.column_stack([C.inf.fe_matrix(M, ["geo", "year"]), M[fr["names"]].to_numpy(float),
                         C.specs.break_dummies(M, fr["breaks"]),
                         np.column_stack([(M.geo.to_numpy() == g) * t for g in G]),
                         np.column_stack([(M.geo.to_numpy() == g) * t ** 2 for g in G])])
    r = C.inf.wcr(M.y.to_numpy(float), M.x.to_numpy(float), Z, M.geo.to_numpy(), side=-1, B=B)
    r["years_used"] = list(M.year); r["geos_used"] = G
    C.log_spec(label, r)
    out[label] = {k: r[k] for k in ("beta", "se", "p", "p_opposite", "n", "G", "G_star")}
    print(f"{label:58s} {C.fmt(r)}")


d2_quad(cyl, label="D2 long, country quadratic trends")
go("D2 long, no CEE", cyl, "D2", geos=nocee)
loo2 = {}
for g in geos:
    r = C.run(f"D2 long LOO -{g}", cyl, cl, base="D2", B=B, geos=[c for c in geos if c != g])
    loo2[g] = dict(beta=r["beta"], se=r["se"], p=r["p"])
    print(f"   D2 long leave out {g}: b={r['beta']:+.2f} se={r['se']:.2f} p={r['p']:.3f}")
out["D2 long LOO"] = loo2

json.dump(C.specs.clean_json(out), open(os.path.join(C.HERE, "checks.json"), "w"), indent=1)
