# check_righttail.py — gate for unit 3 (build_righttail.py outputs). Verifies
# the exposure mapping's structure, the right-tail join's accounting, the
# capability clock's construction (doubling time re-derived from the written
# CSV), the raw-vs-published METR validation, and the stats table's
# consistency with the underlying rows. Green before anything feeds the paper.
import os

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
FIGS = os.path.normpath(os.path.join(HERE, "..", "figures"))

exp = pd.read_csv(os.path.join(DATA, "exposure_occ1990dd.csv"))
tail = pd.read_csv(os.path.join(DATA, "right_tail.csv"))
stats = pd.read_csv(os.path.join(DATA, "right_tail_stats.csv"))
clock = pd.read_csv(os.path.join(DATA, "capability_clock.csv"),
                    parse_dates=["date"])
val = pd.read_csv(os.path.join(DATA, "metr_raw_validation.csv"))
panel = pd.read_csv(os.path.join(DATA, "oews_occ1990dd_panel.csv"))

VARIANTS = ["dv_rating_alpha", "dv_rating_beta", "dv_rating_gamma",
            "human_rating_alpha", "human_rating_beta", "human_rating_gamma"]
ok = 0


def check(name, cond):
    global ok
    assert cond, f"FAIL: {name}"
    ok += 1
    print(f"  ok  {name}")


print("== exposure layer ==")
check(">= 300 occ1990dd rows", len(exp) >= 300)
check("all six variants inside [0, 1]",
      ((exp[VARIANTS] >= -1e-9) & (exp[VARIANTS] <= 1 + 1e-9)).all().all())
for rater in ["dv_rating", "human_rating"]:
    check(f"{rater}: alpha <= beta <= gamma rowwise (Eloundou nesting)",
          ((exp[f"{rater}_alpha"] <= exp[f"{rater}_beta"] + 1e-9)
           & (exp[f"{rater}_beta"] <= exp[f"{rater}_gamma"] + 1e-9)).all())

print("== right-tail join ==")
p25 = panel[panel["year"] == 2025]
check("2025 employment total matches the panel",
      np.isclose(tail["emp_2025"].sum(), p25["emp"].sum()))
for rule in ["d30", "d40", "d50"]:
    f = pd.read_csv(os.path.join(DATA, f"flips_{rule}.csv"))
    check(f"{rule}: flipped count matches the flips file",
          int((tail[f"flipped_{rule}"] == True).sum())      # noqa: E712
          == int(f["flipped"].sum()))
cov = tail.dropna(subset=["dv_rating_beta"])["emp_2025"].sum() / tail["emp_2025"].sum()
check("exposure covers >= 0.85 of 2025 employment", cov >= 0.85)

print("== the clock ==")
check("four sources present",
      set(clock["source"].unique()) == {"eci", "gpqa_diamond",
                                        "swe_bench_verified", "metr_horizon_min"})
check("dates inside 2019-2027",
      clock["date"].between("2019-01-01", "2027-01-01").all())
for s in clock["source"].unique():
    d = clock[clock["source"] == s].sort_values(["date", "model", "value"])
    check(f"{s}: frontier is a running max",
          (d["frontier"].diff().dropna() >= -1e-12).all()
          and np.allclose(d["frontier"], d["value"].cummax()))
h = clock[(clock["source"] == "metr_horizon_min") & (clock["value"] > 0)]
check("horizon frontier ends above one workday-scale task (> 500 min)",
      h["frontier"].max() > 500)
yrs = (h["date"] - h["date"].min()).dt.days / 365.25
dbl = 12.0 / np.polyfit(yrs, np.log2(h["value"]), 1)[0]
check(f"doubling time re-derived from CSV inside [4, 12] months ({dbl:.1f})",
      4.0 <= dbl <= 12.0)

print("== raw-vs-published validation ==")
check(">= 10 models matched", len(val) >= 10)
check("all matched horizons positive",
      (val["h50_raw"] > 0).all() and (val["h50_epoch"] > 0).all())
corr = np.corrcoef(np.log(val["h50_raw"]), np.log(val["h50_epoch"]))[0, 1]
check(f"log-space correlation >= 0.9 ({corr:.3f})", corr >= 0.9)

print("== stats-table consistency (spot re-derivation) ==")
a = tail[tail["flipped_d40"] != True].dropna(subset=["human_rating_beta"])  # noqa: E712
share = (a[a["human_rating_beta"] >= 0.5]["emp_2025"].sum()
         / a["emp_2025"].sum())
cell = stats[(stats["rule"] == "d40")
             & (stats["variant"] == "human_rating_beta")]["surv_share_ge50"].iloc[0]
check("d40 x human-beta survivor share recomputes exactly",
      np.isclose(share, cell))
# guards the reported sentence: under stricter rules the surviving mass is
# MORE exposed than the flipped mass (pre-LLM flips were low-exposure work)
d50 = stats[(stats["rule"] == "d50") & (stats["variant"] == "human_rating_beta")]
check("d50 x human-beta: survivors more exposed than the flipped",
      float(d50["surv_emp_wmean"].iloc[0]) > float(d50["dead_emp_wmean"].iloc[0]))

fp = os.path.join(FIGS, "right_tail.png")
check("figure exists and is substantive",
      os.path.exists(fp) and os.path.getsize(fp) > 30_000)

print(f"\nALL GREEN — {ok} checks passed.")
