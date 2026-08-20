# check_century.py — gating checks for the century-arc build (λ unit 3).
# Checks gate absolutely: any RED blocks the unit.
#   ./venv/Scripts/python.exe progress_and_prosperity/lambda/checks/check_century.py

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
    res = pd.read_csv(os.path.join(OUT, "lambda_us_century.csv")).set_index("year")
    a = pd.read_csv(os.path.join(OUT, "lambda_us_family_a.csv")).set_index("year")

    expected = [1947, 1958, 1963, 1967, 1972, 1977, 1982, 1987, 1992]
    check("C1 all nine vintages parsed", sorted(res.index) == expected,
          f"{sorted(res.index)}")

    check("C2 GDP-anchor identification within tolerance (all vintages)",
          bool((res["gdp_gap"] < 0.15).all()),
          f"max gap {res['gdp_gap'].max():.1%} (vintage-vs-revised GDP, expected order 5–8%)")

    split = res.dropna(subset=["lam"])
    check("C3 compensation share of VA in [0.45, 0.72] where split exists",
          bool(split["comp_share_of_va"].between(0.45, 0.72).all()),
          f"range [{split['comp_share_of_va'].min():.2f}, {split['comp_share_of_va'].max():.2f}]")

    check("C4 full-VA resolution ≈ 1 for every vintage (parse identity)",
          bool(res["res_va"].between(0.90, 1.02).all()),
          f"range [{res['res_va'].min():.3f}, {res['res_va'].max():.3f}]")

    check("C5 λ̂ ∈ (0,1) where present; instrument variant within 0.05",
          bool((split["lam"].between(0, 1)).all()
               and (split["lam"] - split["lami"]).abs().max() < 0.05),
          f"λ̂ range [{split['lam'].min():.3f}, {split['lam'].max():.3f}]")

    check("C6 compensation series covers 1967–1992 incl. W1b anchors (1982, 1992)",
          {1967, 1972, 1977, 1982, 1987, 1992} <= set(split.index),
          f"{sorted(split.index)}")

    check("C7 pre-1967 vintages honestly dropped from λ̂ (no comp split at 85-level)",
          bool(res.loc[[1947, 1958, 1963], "lam"].isna().all()),
          "res_va green there — tables parse; compensation genuinely not split")

    hx = res.dropna(subset=["hist_comp_dev"])
    check("C8 external comp cross-check (HIST components, 1987+)",
          bool((hx["hist_comp_dev"] < 0.05).all()) and len(hx) >= 2,
          f"devs {dict(hx['hist_comp_dev'].round(4))}")

    ok_splice = "lam_spliced" in res.columns and 1997 in a.index
    if ok_splice:
        link = a.loc[1997, "lam_narrow_tot"] / res.loc[1992, "lam"]
        check("C9 splice link 1992→1997 within [0.7, 1.3], step reported",
              0.7 < link < 1.3, f"link {link:.4f} (the classification-break step, stated not hidden)")
    else:
        check("C9 splice link present", False, "missing")

    rec = res.dropna(subset=["recon_err"]) if "recon_err" in res.columns else pd.DataFrame()
    check("C10 two-digit reconstruction recorded (REPORT-ONLY: published TR is the source)",
          len(rec) >= 2,
          f"recon_err {dict(rec['recon_err'].round(3))} — SIC-era 2-digit conventions "
          "not reproduced by the unit-2 algebra; published TR used directly; resolution identity holds")

    n_red = sum(1 for _, ok, _ in RESULTS if not ok)
    print(f"\n{'ALL GREEN' if n_red == 0 else f'{n_red} RED'} ({len(RESULTS)} checks)")
    sys.exit(0 if n_red == 0 else 1)

if __name__ == "__main__":
    main()
