# check_panel.py — gate for the companion's task panel (build_panel.py outputs).
# House rule: no result enters the paper before its check passes. This file
# asserts structural invariants, coverage floors, and known-world anchors
# against the WRITTEN outputs (plus the build ledger), independently of the
# builder's own in-run gates.
import os
import re

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))

panel = pd.read_csv(os.path.join(DATA, "oews_occ1990dd_panel.csv"))
attrs = pd.read_csv(os.path.join(DATA, "occ1990dd_attributes.csv"))
cov = pd.read_csv(os.path.join(DATA, "panel_coverage.csv"))
ledger = open(os.path.join(DATA, "build_ledger.txt"), encoding="utf8").read()

ok = 0


def check(name, cond):
    global ok
    assert cond, f"FAIL: {name}"
    ok += 1
    print(f"  ok  {name}")


print("== structure ==")
check("panel columns", {"year", "occ1990dd", "emp", "h_mean", "a_mean",
                        "h_median", "a_median", "n_source_codes",
                        "top_source_title"} <= set(panel.columns))
check("years are exactly 1999-2025",
      sorted(panel["year"].unique()) == list(range(1999, 2026)))
check("no duplicate (year, occ1990dd)",
      not panel.duplicated(["year", "occ1990dd"]).any())
check(">= 300 occupations every year",
      (panel.groupby("year")["occ1990dd"].nunique() >= 300).all())
check("attributes: one row per occ1990dd, 330 of them",
      len(attrs) == 330 and attrs["occ1990dd"].is_unique)

print("== coverage (vs each file's own all-occupations total) ==")
check("every year >= 0.85", (cov["coverage"] >= 0.85).all())
check("median year >= 0.93", cov["coverage"].median() >= 0.93)
totals = {int(y): float(t.replace(",", "")) for y, t in
          re.findall(r"oews (\d{4}): .* of all-occ ([\d,]+)", ledger)}
check("ledger carries all 27 totals", len(totals) == 27)
emp_year = panel.groupby("year")["emp"].sum()
check("mapped employment never exceeds the source total",
      all(emp_year[y] <= totals[y] * 1.0001 for y in totals))
check("mapped employment within [100M, 170M] each year",
      emp_year.between(100e6, 170e6).all())
check("the 2020 covid dip is visible", emp_year[2020] < emp_year[2019])

print("== wages ==")
m = panel.dropna(subset=["h_mean", "h_median"])
check("wage skew: h_median <= h_mean on >= 90% of rows",
      (m["h_median"] <= m["h_mean"]).mean() >= 0.90)
wmean = panel.dropna(subset=["h_mean"]).groupby("year").apply(
    lambda g: np.average(g["h_mean"], weights=g["emp"]), include_groups=False)
check("nominal emp-weighted mean wage rises 1999 -> 2025 by > 1.5x",
      wmean[2025] > 1.5 * wmean[1999])
check("1999 emp-weighted mean wage in a sane band ($12-$22)",
      12 <= wmean[1999] <= 22)

print("== worked-instance anchor: telephone operators (occ1990dd 348) ==")
tel = panel[panel["occ1990dd"] == 348].set_index("year")
check("present in every year", len(tel) == 27)
check("collapse: emp(1999) > 5x emp(2025)",
      tel.loc[1999, "emp"] > 5 * tel.loc[2025, "emp"])
check("monotone through era slices: 1999 > 2010 > 2020",
      tel.loc[1999, "emp"] > tel.loc[2010, "emp"] > tel.loc[2020, "emp"])
check("label says operator",
      "operator" in str(tel.loc[2025, "top_source_title"]).lower())

print("== task attributes ==")
a = attrs.set_index("occ1990dd")
check("ALM measures complete on all 330 rows",
      attrs[["task_abstract", "task_routine", "task_manual"]].notna().all().all())
check("routine intensity: operators (348) > managers (4)",
      a.loc[348, "task_routine"] > a.loc[4, "task_routine"])
check("abstract intensity: managers (4) > operators (348)",
      a.loc[4, "task_abstract"] > a.loc[348, "task_abstract"])
check("offshorability present on >= 300 rows",
      attrs["task_offshorability"].notna().sum() >= 300)
check("O*NET attachments on >= 300 rows, task counts >= 3 where present",
      (attrs["onet_n_tasks"].notna().sum() >= 300)
      and (attrs["onet_n_tasks"].dropna() >= 3).all())
check("latest labels attached on >= 300 rows",
      attrs["label_latest"].notna().sum() >= 300)

print(f"\nALL GREEN — {ok} checks passed.")
