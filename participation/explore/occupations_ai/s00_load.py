# s00_load.py - look at what lfsa_egais and the manifest frames hold for the explore half.
import os, sys
sys.path.insert(0, "explore")
import data
import pandas as pd
occ = data.extra("occ")
print(occ.columns.tolist(), len(occ))
print(occ["isco08"].unique())
print(occ["age"].unique(), occ["sex"].unique(), occ["year"].min(), occ["year"].max())
print(occ.groupby("geo")["year"].agg(["min", "max"]))
print("flags:", occ["flag"].value_counts(dropna=False).head(20) if "flag" in occ else "no flag col")
raw = data.manifest_raw()
for k, v in raw.items():
    print(k, v.shape, list(v.columns))
cy, cl = data.panel()
print(cl)
print(cy.columns.tolist())
