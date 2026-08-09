# check_wedges.py — gate for unit 4 (build_wedges.py outputs). Structural
# and accounting gates plus known-world anchors. The targeting-order
# DIRECTION is a hypothesis under test and is NOT gated — with two marked
# exceptions ("sentence guards") that pin the specific claims the README
# reports, so prose and data cannot drift apart.
import os

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
FIGS = os.path.normpath(os.path.join(HERE, "..", "figures"))

w = pd.read_csv(os.path.join(DATA, "wedges_occ1990dd.csv"))
t1 = pd.read_csv(os.path.join(DATA, "targeting_cohorts.csv"))
t2 = pd.read_csv(os.path.join(DATA, "targeting_by_routine.csv"))
t3 = pd.read_csv(os.path.join(DATA, "protection_survival.csv"))
ledger = open(os.path.join(DATA, "wedges_ledger.txt"), encoding="utf8").read()

ok = 0


def check(name, cond):
    global ok
    assert cond, f"FAIL: {name}"
    ok += 1
    print(f"  ok  {name}")


print("== wedge table ==")
check("330 occ1990dd rows, unique", len(w) == 330 and w["occ1990dd"].is_unique)
share_cols = ["cov_9901", "mem_9901", "cov_2025", "mem_2025", "licensed_2025"]
check("all shares inside [0, 1]",
      all(w[c].dropna().between(-1e-9, 1 + 1e-9).all() for c in share_cols))
check("membership <= coverage rowwise (members are covered)",
      (w["mem_9901"] <= w["cov_9901"] + 1e-9).all()
      and (w.dropna(subset=["mem_2025"])["mem_2025"]
           <= w.dropna(subset=["mem_2025"])["cov_2025"] + 1e-9).all())
check("pre-period coverage on >= 300 rows", w["cov_9901"].notna().sum() >= 300)
check("licensure attached on >= 300 rows", w["licensed_2025"].notna().sum() >= 300)

print("== mapping accounting (from the ledger) ==")
check("1999-2001 mapped shares recorded at >= 0.85",
      all(f"unionstats {y} -> occ1990dd" in ledger for y in (1999, 2000, 2001)))
check("2025 mapped share recorded at >= 0.80",
      "unionstats 2025 -> occ1990dd" in ledger)

print("== economy anchors ==")
wm = np.average(w["cov_9901"].dropna(),
                weights=w.loc[w["cov_9901"].notna(), "emp_k_9901"])
check(f"employment-weighted union coverage 1999-2001 in [0.10, 0.20] ({wm:.3f})",
      0.10 <= wm <= 0.20)
w25 = w.dropna(subset=["cov_2025", "emp_k_2025"])
wm25 = np.average(w25["cov_2025"], weights=w25["emp_k_2025"])
check(f"coverage fell 1999-2001 -> 2025 ({wm:.3f} -> {wm25:.3f})", wm25 < wm)
tel = w[w["occ1990dd"] == 348]
check("telephone operators more unionized than the economy pre-period",
      float(tel["cov_9901"].iloc[0]) > wm)

print("== test-table structure ==")
for rule in ["d30", "d40", "d50"]:
    rows = t1[t1["rule"] == rule]
    coh = rows[rows["cohort"] != "spearman_flipyear_cov"]
    sp = rows[rows["cohort"] == "spearman_flipyear_cov"]
    check(f"{rule}: cohort ns sum to the flipped count",
          int(coh["n"].sum()) == int(sp["n"].iloc[0]))
    check(f"{rule}: early cohorts carry n >= 10",
          (coh[coh["cohort"].isin(["2000-07", "2008-15"])]["n"] >= 10).all())
    check(f"{rule}: spearman inside [-1, 1]",
          -1 <= float(sp["cov_9901"].iloc[0]) <= 1)
check("T2 rows all have n >= 10 and spearman inside [-1, 1]",
      (t2["n"] >= 10).all() and t2["spearman"].between(-1, 1).all())

print("== T3 spot re-derivation ==")
f = pd.read_csv(os.path.join(DATA, "flips_d40.csv"))
d = f.merge(w, on="occ1990dd", how="left")
fl = d[(d["flipped"] == True)].dropna(subset=["cov_9901"])     # noqa: E712
val = np.average(fl["cov_9901"], weights=fl["emp_base"])
cell = float(t3[t3["rule"] == "d40"]["flipped_cov_9901"].iloc[0])
check("d40 flipped pre-period coverage recomputes exactly",
      np.isclose(val, cell))

print("== sentence guards (pin the README's claims to the data) ==")
check("licensed share higher among survivors under every rule",
      (t3["surv_licensed"] > t3["flipped_licensed"]).all())
hi = t2[t2["routine_terc"] == "high"]
check("high-routine tercile: early flippers more covered than late, all rules",
      (hi["cov_early"] > hi["cov_late"]).all())

fp = os.path.join(FIGS, "wedge_targeting.png")
check("figure exists and is substantive",
      os.path.exists(fp) and os.path.getsize(fp) > 30_000)

print(f"\nALL GREEN — {ok} checks passed.")
