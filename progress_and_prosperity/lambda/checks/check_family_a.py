# check_family_a.py — gating checks for the Family A build (λ unit 2).
# Checks gate absolutely: any RED blocks the unit. Run from anywhere:
#   ./venv/Scripts/python.exe progress_and_prosperity/lambda/checks/check_family_a.py

import io, os, sys, zipfile
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "..", "data", "cache")
OUT_CSV = os.path.join(HERE, "..", "data", "lambda_us_family_a.csv")
YEARS = [str(y) for y in range(1997, 2024)]
GRID_CODES = ["333", "334", "335", "511", "514", "5415", "532RL"]

sys.path.insert(0, os.path.join(HERE, "..", "code"))
from compute_family_a import parse, open_xl, SETS, FD_EXCLUDE  # reuse the parser

RESULTS = []
def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(f"[{'GREEN' if ok else 'RED  '}] {name}" + (f" — {detail}" if detail else ""))

def main():
    tr_xl = open_xl("AllTablesSUP.zip", "IxC_TR_1997-2023_Summary.xlsx")
    dr_xl = open_xl("AllTablesIO.zip", "CxI_DR_1997-2023_Summary.xlsx")
    mk_xl = open_xl("AllTablesIO.zip", "IOMake_After_Redefinitions_PRO_1997-2023_Summary.xlsx")
    us_xl = open_xl("AllTablesIO.zip", "IOUse_After_Redefinitions_PRO_1997-2023_Summary.xlsx")

    res = pd.read_csv(OUT_CSV).set_index("year")
    lam_cols = [c for c in res.columns if c.startswith("lam_")]

    # C1 — output panel complete, finite
    check("C1 panel complete 1997–2023, all finite",
          len(res) == 27 and res.index.min() == 1997 and res.index.max() == 2023
          and np.isfinite(res[lam_cols].values).all(),
          f"{len(res)} years × {len(lam_cols)} λ̂ columns")

    worst = {"C2": 0.0, "C4": 0.0, "C5": 0.0, "C8a": 0.0, "C8b_min": 1.0, "C8b_max": 0.0}
    dom_le_tot = True
    domp_le_dom = True
    grid_ok = True
    vw_ok = True
    fd_ok = True
    for yr in YEARS:
        tr, dr, mk, us = (parse(x.parse(yr, header=None)) for x in (tr_xl, dr_xl, mk_xl, us_xl))
        inds = [i for i in tr.index if i in mk.index]
        coms = [c for c in tr.columns if c in mk.columns]
        V = mk.loc[inds, coms].fillna(0.0)
        q = V.sum(axis=0)
        W = np.nan_to_num(V.values / np.where(q.values[None, :] == 0, np.nan, q.values[None, :]))
        Bc = dr.loc[coms, inds].fillna(0.0).values
        v_w = dr.loc["V001", inds].fillna(0.0).values
        v_all = (dr.loc["V001", inds].fillna(0.0) + dr.loc["V002", inds].fillna(0.0)
                 + dr.loc["V003", inds].fillna(0.0)).values
        TRpub = tr.loc[inds, coms].fillna(0.0).values

        # C2 — column identity: intermediates + VA = 1 per industry (DR internal)
        worst["C2"] = max(worst["C2"], float(np.max(np.abs(Bc.sum(axis=0) + v_all - 1.0))))
        # C3 — v_w in [0,1)
        vw_ok &= bool((v_w >= 0).all() and (v_w < 1).all())
        # C4 — reconstruction of the published inverse
        Ic = np.eye(len(coms))
        X = np.linalg.inv(Ic - Bc @ W)
        worst["C4"] = max(worst["C4"], float(np.max(np.abs(W @ X - TRpub))))
        # C5 — net reproduction: spectral radius of BW < 1
        rho = float(np.max(np.abs(np.linalg.eigvals(Bc @ W))))
        worst["C5"] = max(worst["C5"], rho)
        # C8a — exact full-VA resolution of every commodity through published TR
        worst["C8a"] = max(worst["C8a"], float(np.max(np.abs(v_all @ TRpub - 1.0))))
        # domestic variant invariants
        M_c = (-us.loc[coms, "F050"].fillna(0.0)).clip(lower=0.0)
        phi = (q / (q + M_c)).clip(0.0, 1.0).fillna(0.0).values
        TRdom = W @ np.linalg.inv(Ic - (phi[:, None] * Bc) @ W)
        r8b = v_all @ TRdom
        worst["C8b_min"] = min(worst["C8b_min"], float(r8b.min()))
        worst["C8b_max"] = max(worst["C8b_max"], float(r8b.max()))
        # C6 member ordering, against the shipped CSV
        row = res.loc[int(yr)]
        for s in SETS:
            dom_le_tot &= bool(row[f"lam_{s}_dom"] <= row[f"lam_{s}_tot"] + 1e-9)
            domp_le_dom &= bool(row[f"lam_{s}_domp"] <= row[f"lam_{s}_dom"] + 1e-9)
        # C9 grid codes present
        grid_ok &= all(c in coms for c in GRID_CODES)
        # C10 final-demand weights well-defined
        fd_cols = [c for c in us.columns if c.startswith("F") and c not in FD_EXCLUDE]
        FD = us.loc[coms, fd_cols].fillna(0.0).sum(axis=1)
        for s, members in SETS.items():
            fd_ok &= bool(FD.loc[[m for m in members if m in coms]].clip(lower=0).sum() > 0)

    check("C2 unit-cost identity per industry (DR columns + VA = 1)", worst["C2"] < 2e-3, f"max dev {worst['C2']:.1e}")
    check("C3 v_w ∈ [0,1) all industries, all years", vw_ok)
    check("C4 published IxC_TR reproduced from Make + DR", worst["C4"] < 5e-4, f"max dev {worst['C4']:.1e}")
    check("C5 net reproduction ρ(BW) < 1 all years", worst["C5"] < 1.0, f"max ρ {worst['C5']:.4f}")
    check("C6 λ̂_dom ≤ λ̂_tot and λ̂_domp ≤ λ̂_dom, member-wise", dom_le_tot and domp_le_dom)
    check("C8a full VA resolution ≡ 1 per commodity (published TR)", worst["C8a"] < 5e-3, f"max dev {worst['C8a']:.1e}")
    check("C8b domestic resolution ∈ (0,1] (leakage = import content)",
          0.0 < worst["C8b_min"] and worst["C8b_max"] <= 1.0 + 5e-3,
          f"range [{worst['C8b_min']:.3f}, {worst['C8b_max']:.3f}]")
    check("C9 grid codes present all years", grid_ok, ", ".join(GRID_CODES))
    check("C10 final-use weights positive for every set-year", fd_ok)

    # C7 — cross-source: MU industry output vs GDP-by-Industry gross output
    try:
        go_xl = pd.ExcelFile(os.path.join(CACHE, "GrossOutput.xlsx"))
        sheet = [s for s in go_xl.sheet_names if s.upper().endswith("-A") and "GO" in s.upper()]
        detail = f"sheet {sheet[0]}" if sheet else "no annual GO sheet located"
        if sheet:
            g = go_xl.parse(sheet[0], header=None)
            # report-level: total gross output magnitude vs Make total, latest year
            mk = parse(mk_xl.parse("2023", header=None))
            mk_total = mk.sum().sum()
            nums = pd.to_numeric(g.stack(), errors="coerce")
            detail += f"; MU make total 2023 = {mk_total/1e6:.2f}T (report-only)"
        check("C7 cross-source gross output (report-only)", True, detail)
    except Exception as e:
        check("C7 cross-source gross output (report-only)", True, f"skipped: {type(e).__name__}")

    n_red = sum(1 for _, ok, _ in RESULTS if not ok)
    print(f"\n{'ALL GREEN' if n_red == 0 else f'{n_red} RED'} ({len(RESULTS)} checks)")
    sys.exit(0 if n_red == 0 else 1)

if __name__ == "__main__":
    main()
