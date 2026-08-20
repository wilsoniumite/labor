# compute_family_a.py — λ̂_US from BEA make-use framework (after redefinitions,
# producers' prices), summary level, 1997–2023.
#
# Object (lambda_spec.md): λ̂(t) = v_w′ (I−A)⁻¹ f_M — the vertically integrated
# labor-compensation share of one dollar of machinery final output.
#
# Construction verified against the published tables (diag_reconstruction.py,
# 2026-08-20): with B = published CxI_DR (direct requirements, after redef,
# incl. V001/V002/V003 coefficient rows) and W = Make/q (market shares, all 73
# commodities incl. Used/Other), W(I − B_c W)⁻¹ reproduces the published
# IxC_TR to max|err| ≈ 7e-05 (DR rounding). The earlier SUT-framework attempt
# missed by ~0.3 — the published TR's basis is the MU after-redef framework,
# not the SUT presentation. The reconstruction is gated per year (C4) and the
# run BLOCKS if it degrades; only then does the domestic variant (proportional
# import purge on the same B, W) earn trust.
#
#   v_w[i]  = DR row V001 (compensation of employees per $ industry output)
#   v_nw[i] = DR rows V002+V003 (taxes less subsidies + gross operating surplus)
#   B_c     = DR commodity rows (73 × 71)
#   W       = Make[i,c]/q_c, q = Make column sums (71 × 73)
#   TR_tot  = published IxC_TR (import-comparable total requirements)
#   TR_dom  = W(I − diag(φ) B_c W)⁻¹, φ_c = q_c/(q_c + M_c), M_c = −Use[c,F050]
#             (proportional import purge; import-matrix variant queued)
#   f_set   = final uses of member commodities from the MU Use table
#             (all F-columns except F030 inventories and F050 imports),
#             clipped at 0, normalized to $1
#
# Variants (grid v1): {narrow, medium, broad} × {tot, dom}; plus dom_purch
# (final-layer purge, reported not banded); direct compensation share of the
# member industries; the non-wage resolution through both inverses.
# Deferred axes, recorded in STATE: self-employment imputation; the
# import-matrix (non-proportional) purge; before-redefinitions variant.
#
# No reading here: outputs + checks only. The gate read is unit 4.

import io, os, zipfile
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "..", "data", "cache")
OUT = os.path.join(HERE, "..", "data")
FIG = os.path.join(HERE, "..", "figures")
YEARS = [str(y) for y in range(1997, 2024)]
RECON_TOL = 5e-4  # vs published TR; observed ~7e-05 (DR rounding)

SETS = {
    "narrow": ["333", "334", "335"],
    "medium": ["333", "334", "335", "511", "514", "5415"],
    "broad":  ["333", "334", "335", "511", "514", "5415", "532RL"],
}
FD_EXCLUDE = {"F030", "F050"}

def parse(df):
    col_codes = [str(c) for c in df.iloc[5, 2:]]
    row_codes = [str(c) for c in df.iloc[7:, 0]]
    body = df.iloc[7:, 2:]
    body = pd.DataFrame(pd.to_numeric(body.stack(), errors="coerce").unstack().values,
                        index=row_codes, columns=col_codes)
    ok = lambda c: c != "nan" and " " not in c and len(c) <= 8
    return body.loc[[c for c in body.index if ok(c)],
                    [c for c in body.columns if ok(c)]]

def open_xl(zname, fname):
    z = zipfile.ZipFile(os.path.join(CACHE, zname))
    return pd.ExcelFile(io.BytesIO(z.read(fname)))

def main():
    tr_xl = open_xl("AllTablesSUP.zip", "IxC_TR_1997-2023_Summary.xlsx")
    dr_xl = open_xl("AllTablesIO.zip", "CxI_DR_1997-2023_Summary.xlsx")
    mk_xl = open_xl("AllTablesIO.zip", "IOMake_After_Redefinitions_PRO_1997-2023_Summary.xlsx")
    us_xl = open_xl("AllTablesIO.zip", "IOUse_After_Redefinitions_PRO_1997-2023_Summary.xlsx")

    rows, ledger, blocked = [], [], []
    for yr in YEARS:
        tr, dr, mk, us = (parse(x.parse(yr, header=None)) for x in (tr_xl, dr_xl, mk_xl, us_xl))

        inds = [i for i in tr.index if i in mk.index]                 # 71 industries
        coms = [c for c in tr.columns if c in mk.columns]             # 73 commodities
        V = mk.loc[inds, coms].fillna(0.0)                            # make: i×c
        q = V.sum(axis=0)
        W = (V.values / np.where(q.values[None, :] == 0, np.nan, q.values[None, :]))
        W = np.nan_to_num(W)
        Bc = dr.loc[coms, inds].fillna(0.0).values                    # c×i
        v_w = dr.loc["V001", inds].fillna(0.0).values
        v_nw = (dr.loc["V002", inds].fillna(0.0) + dr.loc["V003", inds].fillna(0.0)).values

        TRpub = tr.loc[inds, coms].fillna(0.0).values
        Ic = np.eye(len(coms))
        TRcon = W @ np.linalg.inv(Ic - Bc @ W)
        recon_err = float(np.max(np.abs(TRcon - TRpub)))
        if recon_err > RECON_TOL:
            blocked.append((yr, recon_err))

        # imports and domestic purge (proportional)
        M_c = (-us.loc[coms, "F050"].fillna(0.0)).clip(lower=0.0)
        phi = (q / (q + M_c)).clip(0.0, 1.0).fillna(0.0).values
        TRdom = W @ np.linalg.inv(Ic - (phi[:, None] * Bc) @ W)

        # final-use weights
        fd_cols = [c for c in us.columns if c.startswith("F") and c not in FD_EXCLUDE]
        FD = us.loc[coms, fd_cols].fillna(0.0).sum(axis=1)

        g = V.sum(axis=1)                                             # industry output
        comp_i = v_w * g.values                                       # compensation levels

        row = {"year": int(yr), "recon_err": recon_err}
        for sname, members in SETS.items():
            mem = [m for m in members if m in coms]
            f = FD.loc[mem].clip(lower=0.0)
            f = (f / f.sum()).values
            idx = [coms.index(m) for m in mem]
            for tag, Mx in (("tot", TRpub), ("dom", TRdom)):
                row[f"lam_{sname}_{tag}"] = float(v_w @ Mx[:, idx] @ f)
                row[f"res_nw_{sname}_{tag}"] = float(v_nw @ Mx[:, idx] @ f)
            row[f"lam_{sname}_domp"] = float(v_w @ TRdom[:, idx] @ (phi[idx] * f))
            mi = [i for i in mem if i in inds]
            gi = g.loc[mi].sum()
            row[f"direct_{sname}"] = float(comp_i[[inds.index(i) for i in mi]].sum() / gi)
        rows.append(row)
        ledger.append((yr, f"recon_err={recon_err:.2e}", f"inds={len(inds)}", f"coms={len(coms)}"))

    print("=== build ledger ===")
    for e in ledger:
        print("  ", *e)
    if blocked:
        print(f"\nBLOCKED: reconstruction gate C4 failed (tol {RECON_TOL:g}): {blocked}")
        raise SystemExit(1)

    res = pd.DataFrame(rows).set_index("year")
    os.makedirs(OUT, exist_ok=True)
    res.to_csv(os.path.join(OUT, "lambda_us_family_a.csv"))

    lam_cols = [c for c in res.columns if c.startswith("lam_") and not c.endswith("domp")]
    band = res[lam_cols]
    print("\n=== snapshots (λ̂ members) ===")
    print(res.loc[[1997, 2005, 2015, 2023], lam_cols + ["direct_narrow"]].round(4).to_string())

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    os.makedirs(FIG, exist_ok=True)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.fill_between(res.index, band.min(axis=1), band.max(axis=1), alpha=0.25,
                    label="λ̂_US band (3 sector sets × {tot, dom})")
    ax.plot(res.index, band.median(axis=1), lw=2, label="median member")
    ax.plot(res.index, res["lam_narrow_tot"], lw=1.2, ls="--", label="narrow, total-requirements")
    ax.plot(res.index, res["direct_narrow"], lw=1.2, ls=":", label="direct share, narrow (no inverse)")
    ax.set_ylabel("compensation share of $1 machinery final output")
    ax.set_title("λ̂_US — vertically integrated labor-compensation share of machinery final output\n"
                 "Family A, BEA MU summary 1997–2023 · tier: accounting · UNREAD (gate read = unit 4)")
    ax.legend(loc="best", fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "lambda_us_family_a.png"), dpi=150)
    print("\nwrote data/lambda_us_family_a.csv and figures/lambda_us_family_a.png")

if __name__ == "__main__":
    main()
