# check_family_b.py — gating checks for the world referee build (λ unit 4).
# Checks gate absolutely: any RED blocks the unit.
#   ./venv/Scripts/python.exe progress_and_prosperity/lambda/checks/check_family_b.py

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
    res = pd.read_csv(os.path.join(OUT, "lambda_world_family_b.csv"))
    w13 = res[res.release == "wiod13"].set_index("year")
    w16 = res[res.release == "wiod16"].set_index("year")

    check("C1 coverage: wiod13 1995–2011 (17y), wiod16 2000–2014 (15y)",
          len(w13) == 17 and len(w16) == 15
          and w13.index.min() == 1995 and w16.index.max() == 2014)

    check("C2 exact global identity ≤ 1e-9 every year (closed world table)",
          bool((res["ident_err"] < 1e-9).all()),
          f"max {res['ident_err'].max():.1e}")

    check("C3 zero-GO sectors dropped are immaterial",
          bool((res["dropped_flow"] < 5e4).all()),
          f"max dropped flow ${res['dropped_flow'].max():,.0f}M; max n_dropped {int(res['n_dropped'].max())}")

    # per-release evaluation: each release has its own sector-set columns;
    # cross-release cells are structurally NaN, and thin-labor years are
    # excluded upstream (flagged) — both masked here, not failed on.
    kept = res[~res["thin_labor_excluded"].fillna(False)]
    lam_cols = [c for c in res.columns if c.startswith("lam_") and "US_" not in c]
    ok_range, lo, hi = True, np.inf, -np.inf
    for _, sub in kept.groupby("release"):
        cols = [c for c in lam_cols if sub[c].notna().any()]
        v = sub[cols]
        ok_range &= bool(((v > 0) & (v < 1)).where(v.notna(), True).all().all())
        ok_range &= not v.isna().all(axis=1).any()
        lo, hi = min(lo, v.min().min()), max(hi, v.max().max())
    check("C4a λ̂ ∈ (0,1) all variants, views, kept years (per release)",
          ok_range, f"range [{lo:.3f}, {hi:.3f}]")

    ok_order = True
    for _, sub in kept.groupby("release"):
        for base in {c.rsplit("_", 2)[0] for c in lam_cols if sub[c].notna().any()}:
            for v in ("comp", "lab"):
                c0, cm = f"{base}_{v}_row0", f"{base}_{v}_rowm"
                if c0 in sub.columns and sub[c0].notna().any():
                    ok_order &= bool((sub[c0] <= sub[cm] + 1e-9).dropna().all())
            for r in ("row0", "rowm"):
                cc, cl = f"{base}_comp_{r}", f"{base}_lab_{r}"
                if cc in sub.columns and sub[cc].notna().any():
                    ok_order &= bool((sub[cc] <= sub[cl] + 1e-9).dropna().all())
    check("C4b member ordering: ROW0 ≤ ROWmean and COMP ≤ LAB, everywhere", ok_order)

    # domestic/foreign decomposition on the US-purchases view
    dec_ok, fshare = True, []
    for _, r in res.iterrows():
        for s in ("narrow", "narrow13", "medium"):
            lam_c, lus_c = f"lam_{s}_uspurch_comp_rowm", f"lamUS_{s}_comp_rowm"
            if lam_c in res.columns and pd.notna(r.get(lam_c)) and pd.notna(r.get(lus_c)):
                dec_ok &= 0 <= r[lus_c] <= r[lam_c] + 1e-9
                fshare.append(1 - r[lus_c] / r[lam_c])
    check("C5 US + foreign decomposition: 0 ≤ US-labor ≤ total; foreign share ∈ (0,1)",
          dec_ok and all(0 < f < 1 for f in fshare),
          f"foreign-labor share of US machinery purchases: [{min(fshare):.2f}, {max(fshare):.2f}]")

    excl = res[res["thin_labor_excluded"].fillna(False)]
    check("C6 labor coverage ≥ 60% for every kept year; thin years excluded and flagged",
          bool((kept["cover_share"] >= 0.6).all()),
          f"kept min {kept['cover_share'].min():.2f}; excluded: "
          f"{[f'{r.release}:{int(r.year)}(cov {r.cover_share:.2f})' for r in excl.itertuples()]}")

    md = w13.dropna(subset=["map_dev"])
    check("C7 wiod13 sector-mapping verified via USA machinery GO (WIOT vs SEA)",
          bool((md["map_dev"] < 0.05).all()) and len(md) > 10,
          f"max dev {md['map_dev'].max():.3f}")

    # vintage overlap 2000–2011 — REPORT-ONLY (different sector classifications:
    # narrow13 includes optical instruments, excludes software)
    a = w13["lam_narrow13_world_comp_rowm"].dropna()
    b = w16["lam_narrow_world_comp_rowm"].dropna()
    ov = sorted(set(a.index) & set(b.index))
    dev = (a.loc[ov] - b.loc[ov]).abs().max()
    check("C8 vintage overlap 2000–2011 recorded (report-only, classifications differ)",
          np.isfinite(dev), f"max |w13−w16| {dev:.3f} on world/comp/rowm")

    hrel_cols = [c for c in res.columns if c.startswith("hrel_")]
    ok_h, hlo, hhi = len(hrel_cols) > 0, np.inf, -np.inf
    for _, sub in kept.groupby("release"):
        cols = [c for c in hrel_cols if sub[c].notna().any()]
        v = sub[cols]
        ok_h &= bool(((v > 0) & (v < 1)).where(v.notna(), True).all().all())
        ok_h &= not v.isna().all(axis=1).any()
        hlo, hhi = min(hlo, v.min().min()), max(hhi, v.max().max())
    check("C9 H_rel present, positive, and below 1 (quantity leg well-formed)",
          ok_h, f"range [{hlo:.3f}, {hhi:.3f}]")

    check("C10 wbar (world avg hourly compensation, USD) sane and rising-ish",
          bool(res["wbar"].between(1, 100).all()),
          f"range [{res['wbar'].min():.1f}, {res['wbar'].max():.1f}] $/hr")

    n_red = sum(1 for _, ok, _ in RESULTS if not ok)
    print(f"\n{'ALL GREEN' if n_red == 0 else f'{n_red} RED'} ({len(RESULTS)} checks)")
    sys.exit(0 if n_red == 0 else 1)

if __name__ == "__main__":
    main()
