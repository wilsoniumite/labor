# s03_tenure.py — the second-earner enclosure signature: does women's participation respond more (more positively) to
# q where renting households dominate? The theory critic's reading of App B: the second earner's exit is housed by
# the household, so q reaches her only through the household's net housing position: positive where renters
# dominate, zero or negative where (outright) owners dominate.
# Moderators: renter share by age from ilc_lvps05 (X, 2015-2017 mean, understanding only) and the manifest's
# outright-owner share 55-64 (M, same years, flagged not predetermined).
# Out: s03_tenure.txt, fig05_tenure_slopes.png
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as cm  # noqa: E402

W, M, GREY, INK, MUTED = "#eb6834", "#2a78d6", "#8a8984", "#0b0b0b", "#52514e"
df = cm.panel()
out = []


def say(s):
    out.append(s)
    print(s)


# --- moderators (country level)
ten = cm.data.extra("tenure")
ten = ten[ten.year.isin([2015, 2016, 2017])]
mod = {}
for t in ("RENT", "RENT_MKT", "OWN_NL", "OWN_L"):
    for a in ("Y25-34", "Y35-44", "Y45-54", "Y18-64", "Y55-64"):
        mod[f"{t}_{a}"] = ten[(ten.tenure == t) & (ten.age == a)].groupby("geo").value.mean()
mod = pd.DataFrame(mod)
mod["RENT_2554"] = mod[["RENT_Y25-34", "RENT_Y35-44", "RENT_Y45-54"]].mean(1)
mod["OWNNL_2554"] = mod[["OWN_NL_Y25-34", "OWN_NL_Y35-44", "OWN_NL_Y45-54"]].mean(1)
mod["OWNL_2554"] = mod[["OWN_L_Y25-34", "OWN_L_Y35-44", "OWN_L_Y45-54"]].mean(1)
cl = cm.data.panel()[1]
mod["OWNNL5564_M"] = cl["owner_outright_5564"]
mod["F_raw"] = cl["F_raw"]
say(mod[["RENT_2554", "RENT_MKT_Y25-34", "OWNNL_2554", "OWNL_2554", "OWNNL5564_M", "F_raw"]].round(1).to_string())
say("corr: " + mod[["RENT_2554", "OWNNL_2554", "OWNNL5564_M", "F_raw"]].corr().round(2).to_string())

# --- country-by-country slopes (descriptive): AW2554 on q_l1 and U_lfs and a linear trend, 1997-2025
d = df.reset_index()
sl = {}
for g in cm.GEOS:
    x = d[(d.geo == g) & ~d.year.isin([2020, 2021])].dropna(subset=["AW2554", "AM2554", "logq_l1", "U_lfs"])
    X = np.column_stack([np.ones(len(x)), x.logq_l1, x.U_lfs, x.year - 2010])
    bw = np.linalg.lstsq(X, x.AW2554, rcond=None)[0][1]
    bm = np.linalg.lstsq(X, x.AM2554, rcond=None)[0][1]
    sl[g] = dict(bW=bw, bM=bm, n=len(x))
sl = pd.DataFrame(sl).T.join(mod[["RENT_2554", "OWNNL_2554", "OWNNL5564_M"]])
say("\ncountry slopes of AW2554 / AM2554 on q (with U_lfs and own linear trend), no breaks:\n" + sl.round(2).to_string())
s = sl.dropna()
say("corr(bW, RENT_2554) %.2f  corr(bW, OWNNL_2554) %.2f  corr(bW, OWNNL5564_M) %.2f" % (
    np.corrcoef(s.bW, s.RENT_2554)[0, 1], np.corrcoef(s.bW, s.OWNNL_2554)[0, 1], np.corrcoef(s.bW, s.OWNNL5564_M)[0, 1]))
cm.count(0, "country-by-country slopes (descriptive, not counted as specs)")


# --- pooled interactions (FE, breaks, WCR)
def inter(mname, y, side, label, controls=("U_lfs",), years=(1997, 2025), trends=False):
    m = mod[mname]
    z = (m - m.mean()) / m.std(ddof=0)
    dd = df.copy()
    geo = dd.index.get_level_values(0)
    dd["QxR"] = dd["logq_l1"].to_numpy() * geo.map(z).to_numpy(float)
    r = cm.reg(dd, y, ["QxR", "logq_l1"], list(controls), years=years, side=side, label=label, trends=trends,
               extra_breaks=())
    say(cm.fmt(r))
    return r


say("")
inter("RENT_2554", "AW2554", +1, "W 25-54: q x renter share 25-54 (X), sd units")
inter("RENT_2554", [(1, "AW2554"), (-1, "AM2554")], +1, "W-M 25-54: q x renter share 25-54 (X)")
inter("OWNNL5564_M", "AW2554", -1, "W 25-54: q x outright owners 55-64 (M)")
inter("OWNNL5564_M", [(1, "AW2554"), (-1, "AM2554")], -1, "W-M 25-54: q x outright owners 55-64 (M)")
inter("OWNNL_2554", "AW2554", -1, "W 25-54: q x outright owners 25-54 (X)")
inter("RENT_2554", "AW2554", +1, "W 25-54: q x renter share, country trends", trends=True)
inter("OWNNL5564_M", "AW2554", -1, "W 25-54: q x outright owners 55-64 (M), trends", trends=True)
open(os.path.join(cm.HERE, "s03_tenure.txt"), "w").write("\n".join(out) + "\n")

fig, ax = plt.subplots(1, 2, figsize=(10, 4))
for a, mname, lab in ((ax[0], "RENT_2554", "renter share 25-54, 2015-17 (%)"),
                      (ax[1], "OWNNL5564_M", "outright owners 55-64, 2015-17 (%)")):
    a.axhline(0, color="#c9c8c2", lw=0.8)
    a.scatter(s[mname], s.bW, color=W, s=30, edgecolor="white", label="women")
    a.scatter(s[mname], s.bM, color=M, s=30, edgecolor="white", label="men")
    for g, r in s.iterrows():
        a.annotate(g, (r[mname], r.bW), fontsize=6.5, color=MUTED, xytext=(3, 2), textcoords="offset points")
    a.set_xlabel(lab)
    a.set_ylabel("country slope of activity 25-54 on log q (pp)")
    a.set_ylim(-60, 60)
ax[0].legend(frameon=False, fontsize=8)
ax[0].set_title("Women's q-slope against renting (country by country)", fontsize=9, loc="left", color=INK)
ax[1].set_title("... and against outright ownership of the old", fontsize=9, loc="left", color=INK)
fig.tight_layout()
fig.savefig(os.path.join(cm.HERE, "fig05_tenure_slopes.png"), dpi=150)
