# s01_shares.py - ISCO-08 major-group shares by age (sex T), explore half: coverage, routine shares, young vs prime.
import sys
sys.path.insert(0, "explore")
import data
import numpy as np
import pandas as pd
pd.set_option("display.width", 220); pd.set_option("display.max_columns", 30)
occ = data.extra("occ")
occ = occ[(occ.sex == "T")]
print("non-null by year (TOTAL, Y15-64):")
t = occ[(occ.isco08 == "TOTAL") & (occ.age == "Y15-64")].pivot(index="year", columns="geo", values="value")
print(t.notna().sum(1).to_string())
w = occ.pivot_table(index=["geo", "year", "age"], columns="isco08", values="value")
sh = 100 * w.div(w["TOTAL"], axis=0)
sh["ROUT"] = sh[["OC4", "OC7", "OC8"]].sum(1, min_count=3)
sh.to_csv("explore/occupations_ai/shares_T.csv")
for a in ["Y15-24", "Y25-54", "Y55-64", "Y15-64"]:
    s = sh.xs(a, level="age")
    for c in ["OC4", "ROUT"]:
        p = s[c].unstack("geo")
        print(f"\n{c} share at {a}")
        print(p.loc[2008:2025].round(1).to_string())
# flags on occ cells 15-24
f = occ[(occ.age == "Y15-24") & occ.isco08.isin(["OC4", "TOTAL"]) & (occ.year >= 2011)]
print("\nflags 15-24 OC4/TOTAL since 2011:")
print(f[f.flag.str.len() > 0].groupby(["geo", "isco08", "flag"]).year.apply(list).to_string())
