# check_envelope.py — gate for unit 2 (build_envelope.py outputs). Verifies
# the w/c grid's construction, the envelope's defining identity (rho equals
# the waterline at the flip year — re-derived from the CSVs, not trusted),
# rule-grid orderings, era monotonicity, the density integral, and the
# worked-instance anchor. House rule: green before anything feeds the paper.
import os

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
FIGS = os.path.normpath(os.path.join(HERE, "..", "figures"))

grid = pd.read_csv(os.path.join(DATA, "wc_grid.csv")).set_index("year")
env = pd.read_csv(os.path.join(DATA, "envelope.csv"))
stats = pd.read_csv(os.path.join(DATA, "envelope_stats.csv"))
dens = pd.read_csv(os.path.join(DATA, "waterline_density.csv"))
flips = {r: pd.read_csv(os.path.join(DATA, f"flips_{r}.csv"))
         for r in ["d30", "d40", "d50"]}
RULE_CEIL = {"d30": 0.70, "d40": 0.60, "d50": 0.50}

ok = 0


def check(name, cond):
    global ok
    assert cond, f"FAIL: {name}"
    ok += 1
    print(f"  ok  {name}")


print("== the w/c grid ==")
members = [c for c in grid.columns if c != "wc_median"]
check("six members plus median", len(members) == 6)
check("normalized: every member = 1.0 at 1999",
      np.allclose(grid.loc[1999, members], 1.0))
check("median is the row median of the members",
      np.allclose(grid["wc_median"], grid[members].median(axis=1)))
check("the waterline rose: median 2025 > 5x 1999",
      grid.loc[2025, "wc_median"] > 5.0)
check("member ordering 2025: computer-cost members above broad equipment",
      min(grid.loc[2025, ["ahetpi_x_pc_hedonic", "ahetpi_x_ppi_computer",
                          "oews_x_pc_hedonic", "oews_x_ppi_computer"]])
      > max(grid.loc[2025, ["ahetpi_x_equip_broad", "oews_x_equip_broad"]]))

print("== the envelope identity (re-derived) ==")
rho_check = [np.isclose(r.rho_wc, grid.loc[int(r.flip_year), r.wc_member])
             for r in env.itertuples(index=False)]
check(f"rho equals the waterline at the flip year on all {len(env)} rows",
      all(rho_check))
check("flip years inside (1999, 2025]",
      env["flip_year"].between(2000, 2025).all())
check("base employment positive on all envelope rows",
      (env["emp_base"] > 0).all())

print("== rule grid ==")
for rule, df in flips.items():
    f = df[df["flipped"]]
    check(f"{rule}: flipped implies end/peak <= {RULE_CEIL[rule]}",
          (f["end_over_peak"] <= RULE_CEIL[rule] + 1e-12).all())
    check(f"{rule}: peaks leave >= 3 post-peak years",
          (f["peak_year"] <= 2022).all())
mass = {r: flips[r][flips[r]["flipped"]]["emp_base"].sum()
        / flips[r]["emp_base"].sum() for r in flips}
check("stricter rules flip less mass: d50 <= d40 <= d30",
      mass["d50"] <= mass["d40"] <= mass["d30"])

print("== era slices ==")
for rule in flips:
    s = stats[stats["rule"] == rule].sort_values("era")
    check(f"{rule}: flipped mass nondecreasing across eras",
          s["mass_flipped"].is_monotonic_increasing)
    check(f"{rule}: median rho nondecreasing across eras",
          s["rho_p50"].is_monotonic_increasing)
    check(f"{rule}: era-2025 count matches the flips file",
          int(s[s["era"] == 2025]["n_flipped"].iloc[0])
          == int(flips[rule]["flipped"].sum()))

print("== density integral ==")
for rule in flips:
    d = dens[dens["rule"] == rule]
    total = d["dmass"].sum()
    check(f"{rule}: flip-mass increments integrate to the 2025 mass",
          np.isclose(total, mass[rule], atol=1e-9))
check("density nonnegative wherever defined",
      (dens["density"].dropna() >= 0).all())

print("== worked-instance anchor: telephone operators (348) ==")
for rule, df in flips.items():
    t = df[df["occ1990dd"] == 348].iloc[0]
    check(f"{rule}: operators flipped, by 2008", bool(t["flipped"])
          and int(t["flip_year"]) <= 2008)
    # rho is discrete (one value per flip year), so ties at the median are
    # structural; the anchor is rank position — bottom half of the flipped set
    med = env[(env["rule"] == rule) & (env["wc_member"] == "wc_median")]
    tel_rho = float(med[med["occ1990dd"] == 348]["rho_wc"].iloc[0])
    check(f"{rule}: operators in the bottom half of flipped rho ranks",
          (med["rho_wc"] < tel_rho).mean() <= 0.5)

fp = os.path.join(FIGS, "schedule_envelope.png")
check("figure exists and is substantive",
      os.path.exists(fp) and os.path.getsize(fp) > 30_000)

print(f"\nALL GREEN — {ok} checks passed.")
