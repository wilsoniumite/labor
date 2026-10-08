# s06_young_men.py — is the fall in men's 25-29 activity schooling, or inactivity outside school (the parental floor)?
# Uses edat_lfse_19 25-29 FE by sex and edat_lfse_20 NEET inactive 25-29 by sex (X: understanding only).
# Out: s06_young_men.txt
from __future__ import annotations
import os, sys
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as cm  # noqa: E402

df = cm.panel()
for s in "MF":
    df[f"educ2529_{s}"] = cm.series_x("educ", sex=s, age="Y25-29").reindex(df.index).to_numpy(float)
    df[f"inac2529_{s}"] = cm.series_x("neet", sex=s, age="Y25-29", wstatus="INAC").reindex(df.index).to_numpy(float)
    df[f"cores2529_{s}"] = cm.series_x("cores", sex=s, age="Y25-29").reindex(df.index).to_numpy(float)
d = df.reset_index()
out = []
def say(s):
    out.append(str(s)); print(s)
p1, p2 = d[d.year.between(2005, 2008)].groupby("geo").mean(numeric_only=True), d[d.year.between(2022, 2025)].groupby("geo").mean(numeric_only=True)
ch = pd.DataFrame({"dAM2529": p2["AM25-29"] - p1["AM25-29"], "dEduc_M": p2.educ2529_M - p1.educ2529_M,
                   "dInacNEET_M": p2.inac2529_M - p1.inac2529_M, "dCores_M": p2.cores2529_M - p1.cores2529_M,
                   "dAF2529": p2["AF25-29"] - p1["AF25-29"], "dEduc_F": p2.educ2529_F - p1.educ2529_F,
                   "dInacNEET_F": p2.inac2529_F - p1.inac2529_F, "dCores_F": p2.cores2529_F - p1.cores2529_F})
say("changes 2005-08 -> 2022-25 (pp), 25-29 (activity: nationals; education/NEET/coresidence: all, X):")
say(ch.round(1).to_string())
say("means: " + ch.mean().round(2).to_string())
say("corr(dAM2529, dEduc_M) %.2f; corr(dAM2529, dInacNEET_M) %.2f; corr(dAM2529, dCores_M) %.2f" % (
    ch.corr().loc["dAM2529", "dEduc_M"], ch.corr().loc["dAM2529", "dInacNEET_M"], ch.corr().loc["dAM2529", "dCores_M"]))
open(os.path.join(cm.HERE, "s06_young_men.txt"), "w").write("\n".join(out) + "\n")
