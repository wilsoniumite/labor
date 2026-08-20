# check_us_hours_rent.py — gating checks for the US hours + rent layer (λ unit 5).
# Checks gate absolutely: any RED blocks the unit.
#   ./venv/Scripts/python.exe progress_and_prosperity/lambda/checks/check_us_hours_rent.py

import os, sys
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "data")

RESULTS = []
def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(f"[{'GREEN' if ok else 'RED  '}] {name}" + (f" — {detail}" if detail else ""))

def main():
    res = pd.read_csv(os.path.join(OUT, "lambda_us_hours_rent.csv")).set_index("year")
    lamA = pd.read_csv(os.path.join(OUT, "lambda_us_family_a.csv")).set_index("year")
    variants = [(s, t) for s in ("narrow", "medium", "broad") for t in ("tot", "dom")]

    hrel = res[[f"Hrel_{s}_{t}" for s, t in variants]]
    check("C1 panel complete 1997–2023; H_rel finite for every variant",
          len(res) == 27 and np.isfinite(hrel.values).all(),
          f"27 years × {hrel.shape[1]} variants")

    cov = res[[f"bridge_cover_{s}_{t}" for s, t in variants]]
    check("C2 block bridge covers all requirement mass",
          bool((cov > 0.999).all().all()), f"min {cov.min().min():.4f}")

    wrel = res[[f"wrel_{s}_{t}" for s, t in variants]]
    check("C3 H_rel ∈ (0,1); w̄_rel ∈ (0.8, 2.0)",
          bool(((hrel > 0) & (hrel < 1)).all().all())
          and bool(((wrel > 0.8) & (wrel < 2.0)).all().all()),
          f"H_rel [{hrel.min().min():.3f}, {hrel.max().max():.3f}]; "
          f"w̄_rel [{wrel.min().min():.3f}, {wrel.max().max():.3f}]")

    dev = 0.0
    for s, t in variants:
        lam = lamA[f"lam_{s}_{t}"].loc[res.index]
        dev = max(dev, float((lam - res[f"Hrel_{s}_{t}"] * res[f"wrel_{s}_{t}"]).abs().max()))
    check("C4 exact decomposition λ̂ = H_rel × w̄_rel", dev < 1e-9, f"max dev {dev:.1e}")

    check("C5 no seam artifacts: year-on-year H_rel steps within ±20%",
          bool((hrel.pct_change().abs().dropna() < 0.20).all().all()),
          f"max |yoy| {hrel.pct_change().abs().max().max():.1%} "
          "(SEA 2000–2014 core; KLEMS-index tails 1997–99, 2015–23)")

    ok_p, pmax = True, 0.0
    for s, t in variants:
        lp = res[f"lampurged_{s}_{t}"].dropna()
        lam = lamA[f"lam_{s}_{t}"].loc[lp.index]
        ok_p &= bool((lp <= lam + 1e-9).all()) and set(lp.index) == set(range(1997, 2017))
        pmax = max(pmax, float((lam - lp).max()))
    check("C6 rent purge: populated exactly 1997–2016, λ̂_purged ≤ λ̂, magnitude sane",
          ok_p and pmax < 0.2, f"max purge {pmax:.3f}")

    rho = res[["rho_machinery_direct", "rho_aggregate"]].dropna()
    check("C7 S&S rent shares populated 1997–2016, ∈ (0, 0.3)",
          len(rho) == 20 and bool(((rho > 0) & (rho < 0.3)).all().all()),
          f"machinery ρ [{rho['rho_machinery_direct'].min():.3f}, {rho['rho_machinery_direct'].max():.3f}]; "
          f"aggregate ρ [{rho['rho_aggregate'].min():.3f}, {rho['rho_aggregate'].max():.3f}]")

    ok_dom = all(bool((res[f"H_{s}_dom"] <= res[f"H_{s}_tot"] + 1e-12).all())
                 for s in ("narrow", "medium", "broad"))
    check("C8 H_dom ≤ H_tot member-wise (import purge removes requirements)", ok_dom)

    check("C9 economy average hourly compensation sane (pins hours units)",
          bool(res["wbar_us"].between(15, 70).all()),
          f"wbar [{res['wbar_us'].min():.1f}, {res['wbar_us'].max():.1f}] $/hr")

    n_red = sum(1 for _, ok, _ in RESULTS if not ok)
    print(f"\n{'ALL GREEN' if n_red == 0 else f'{n_red} RED'} ({len(RESULTS)} checks)")
    sys.exit(0 if n_red == 0 else 1)

if __name__ == "__main__":
    main()
