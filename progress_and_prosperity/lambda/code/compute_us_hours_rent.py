# compute_us_hours_rent.py — λ unit 5: the US hours leg (H_rel, w̄_rel) and
# the rent layer (S&S purge; A&R level anchor recorded).
#
# Hours architecture (no re-inversion, no invented levels):
#   r_vec(t) = TR·f from the unit-2 build (published IxC TR + verified
#   domestic variant) — industry output required per $1 machinery final
#   output, 71 BEA industries. Hours enter only as a row vector, so they are
#   applied at BLOCK level: each BEA industry maps to one of ~24 blocks that
#   also have an ISIC-56 counterpart. Levels 2000–2014 from WIOD16 SEA USA
#   hours (H_EMPE, unit-4 member); the 1997–1999 and 2015–2023 tails extend
#   each block by the BEA-BLS KLEMS hours index (2017=100), weighted within
#   block by KLEMS labor compensation — a labeled mechanical extension,
#   continuous at 2014 by construction.
#   H(t) = Σ_b hours_b/GO_b · r_b ;  H_rel = H × w̄_US (economy average
#   hourly compensation, unit-2 comp levels / block hours total);
#   w̄_rel = λ̂ / H_rel.
#
# Rent layer (published values only, per the data rule):
#   Stansbury–Summers BPEA 2020 replication (Brookings-hosted, public):
#   industry panel 1987–2016, implied labor rents by industry.
#   ρ_i(t) = implabrents_i / compensation_i (both in the panel) mapped onto
#   the 71 BEA industries by name (machinery industries map 1:1); unmapped
#   industries carry the corporate-business aggregate ratio.
#   λ̂_purged(t) = Σ_i (1−ρ_i(t)) · v_w_i · r_vec_i, 1987–2016 window
#   (here: 1997–2016 ∩ unit-2 years).
#   A&R 2026 §3.3 level anchor (rents ≈35% [19–44.5%] on automated jobs)
#   recorded in DATA_NOTES — a different object (displaced-job level, not
#   an industry×year series), used as a magnitude benchmark at the read.
#
# UNREAD discipline: outputs only; the gate read is unit 6.

import io, os, sys, zipfile
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "..", "data", "cache")
OUT = os.path.join(HERE, "..", "data")
FIG = os.path.join(HERE, "..", "figures")
sys.path.insert(0, HERE)
from compute_family_a import parse, open_xl, SETS, FD_EXCLUDE

YEARS = list(range(1997, 2024))

# ---- blocks: BEA summary codes → block; ISIC-56 (SEA) codes → block
BEA_BLOCK = {
    "111CA": "agri", "113FF": "agri",
    "211": "mining", "212": "mining", "213": "mining",
    "22": "utilities", "23": "construction",
    "311FT": "food", "313TT": "textiles", "315AL": "textiles",
    "321": "wood_paper", "322": "wood_paper", "323": "wood_paper",
    "324": "petro_chem", "325": "petro_chem", "326": "petro_chem",
    "327": "nonmetal", "331": "metals", "332": "metals",
    "333": "machinery", "334": "computers", "335": "electrical",
    "3361MV": "transp_eq", "3364OT": "transp_eq",
    "337": "furn_misc", "339": "furn_misc",
    "42": "trade", "441": "trade", "445": "trade", "452": "trade", "4A0": "trade",
    "481": "transport", "482": "transport", "483": "transport", "484": "transport",
    "485": "transport", "486": "transport", "487OS": "transport", "493": "transport",
    "511": "publishing", "512": "publishing", "513": "telecom", "514": "it_services",
    "521CI": "finance", "523": "finance", "524": "finance", "525": "finance",
    "HS": "real_estate", "ORE": "real_estate", "532RL": "real_estate",
    "5411": "prof_serv", "5415": "it_services", "5412OP": "prof_serv",
    "55": "mgmt", "561": "admin", "562": "admin",
    "61": "edu_health", "621": "edu_health", "622": "edu_health", "623": "edu_health",
    "624": "edu_health", "711AS": "arts_accom", "713": "arts_accom",
    "721": "arts_accom", "722": "arts_accom", "81": "other_serv",
    "GFGD": "gov", "GFGN": "gov", "GFE": "gov", "GSLG": "gov", "GSLE": "gov",
}
ISIC_BLOCK = {
    "A01": "agri", "A02": "agri", "A03": "agri",
    "B": "mining", "D35": "utilities", "E36": "utilities", "E37-E39": "utilities",
    "F": "construction",
    "C10-C12": "food", "C13-C15": "textiles",
    "C16": "wood_paper", "C17": "wood_paper", "C18": "wood_paper",
    "C19": "petro_chem", "C20": "petro_chem", "C21": "petro_chem", "C22": "petro_chem",
    "C23": "nonmetal", "C24": "metals", "C25": "metals",
    "C26": "computers", "C27": "electrical", "C28": "machinery",
    "C29": "transp_eq", "C30": "transp_eq",
    "C31_C32": "furn_misc", "C33": "furn_misc",
    "G45": "trade", "G46": "trade", "G47": "trade",
    "H49": "transport", "H50": "transport", "H51": "transport", "H52": "transport",
    "H53": "transport",
    "J58": "publishing", "J59_J60": "publishing", "J61": "telecom",
    "J62_J63": "it_services",
    "K64": "finance", "K65": "finance", "K66": "finance",
    "L68": "real_estate",
    "M69_M70": "prof_serv", "M71": "prof_serv", "M72": "prof_serv",
    "M73": "prof_serv", "M74_M75": "prof_serv",
    "N": "admin",
    "P85": "edu_health", "Q": "edu_health",
    "R_S": "arts_accom", "T": "other_serv", "U": "other_serv",
    "I": "arts_accom", "O84": "gov",
}
# S&S indcode → BEA codes (unmapped BEA industries take the aggregate ratio)
SS_BEA = {
    "Dur_machinery": ["333"], "Dur_computer": ["334"], "Dur_electrical": ["335"],
    "Computer_serv": ["5415", "514"], "Inf_data": ["514"],
    "Dur_fab_metal": ["332"], "Dur_prim_metal": ["331"], "Dur_wood": ["321"],
    "Dur_furniture": ["337"], "Dur_misc": ["339"], "Dur_nonmetal": ["327"],
    "Dur_transp": ["3361MV", "3364OT"],
    "Construction": ["23"], "Utilities": ["22"],
}

def klems_frames():
    xl = pd.ExcelFile(os.path.join(CACHE, "klems_ilpa_1997_2024.xlsx"))
    def grid(sheet):
        d = xl.parse(sheet, header=None)
        hdr = d.iloc[1]
        years = {j: int(hdr[j]) for j in range(1, d.shape[1]) if pd.notna(hdr[j])}
        rows = d.iloc[2:].dropna(subset=[0])
        out = pd.DataFrame({yr: pd.to_numeric(rows[j], errors="coerce").values
                            for j, yr in years.items()},
                           index=rows[0].astype(str).str.strip().values)
        return out
    return grid("Labor Hours_Quantity"), grid("Labor_Col Compensation") + grid("Labor_NoCol Compensation")

# KLEMS industry name → block (63 rows; names match GDPxInd naming)
def klems_block(name):
    s = name.lower()
    rules = [
        ("machinery", "machinery"), ("computer and electronic", "computers"),
        ("electrical equipment", "electrical"),
        ("motor vehicles", "transp_eq"), ("other transportation equipment", "transp_eq"),
        ("furniture", "furn_misc"), ("miscellaneous manufacturing", "furn_misc"),
        ("farms", "agri"), ("forestry", "agri"),
        ("oil and gas", "mining"), ("mining", "mining"), ("support activities for mining", "mining"),
        ("utilities", "utilities"), ("construction", "construction"),
        ("food and beverage and tobacco", "food"),
        ("textile", "textiles"), ("apparel", "textiles"),
        ("wood products", "wood_paper"), ("paper products", "wood_paper"), ("printing", "wood_paper"),
        ("petroleum and coal", "petro_chem"), ("chemical products", "petro_chem"),
        ("plastics and rubber", "petro_chem"), ("nonmetallic mineral", "nonmetal"),
        ("primary metals", "metals"), ("fabricated metal", "metals"),
        ("wholesale trade", "trade"), ("retail trade", "trade"),
        ("motor vehicle and parts dealers", "trade"), ("food and beverage stores", "trade"),
        ("general merchandise", "trade"), ("other retail", "trade"),
        ("air transportation", "transport"), ("rail transportation", "transport"),
        ("water transportation", "transport"), ("truck transportation", "transport"),
        ("transit", "transport"), ("pipeline", "transport"),
        ("other transportation and support", "transport"), ("warehousing", "transport"),
        ("publishing industries", "publishing"), ("motion picture", "publishing"),
        ("broadcasting and telecommunications", "telecom"),
        ("data processing", "it_services"),
        ("computer systems design", "it_services"),
        ("federal reserve banks", "finance"), ("credit intermediation", "finance"),
        ("securities", "finance"), ("insurance", "finance"), ("funds", "finance"),
        ("housing", "real_estate"), ("other real estate", "real_estate"),
        ("real estate", "real_estate"), ("rental and leasing", "real_estate"),
        ("legal services", "prof_serv"),
        ("miscellaneous professional, scientific, and technical", "prof_serv"),
        ("management of companies", "mgmt"),
        ("administrative and support", "admin"), ("waste management", "admin"),
        ("educational services", "edu_health"), ("ambulatory", "edu_health"),
        ("hospitals", "edu_health"), ("nursing", "edu_health"), ("social assistance", "edu_health"),
        ("performing arts", "arts_accom"), ("amusements", "arts_accom"),
        ("accommodation", "arts_accom"), ("food services", "arts_accom"),
        ("other services", "other_serv"),
        ("federal", "gov"), ("state and local", "gov"), ("government", "gov"),
    ]
    for key, b in rules:
        if key in s:
            return b
    return None

def sea_usa_hours():
    d = pd.ExcelFile(os.path.join(CACHE, "wiod16_sea.xlsx")).parse("DATA")
    h = d[(d["country"] == "USA") & (d["variable"] == "H_EMPE")].set_index("code")
    ycols = [c for c in h.columns if isinstance(c, (int, float)) and 2000 <= int(c) <= 2014]
    return h[ycols]

def main():
    ledger = []
    # ---- unit-2 matrices per year (reuse the verified construction)
    tr_xl = open_xl("AllTablesSUP.zip", "IxC_TR_1997-2023_Summary.xlsx")
    dr_xl = open_xl("AllTablesIO.zip", "CxI_DR_1997-2023_Summary.xlsx")
    mk_xl = open_xl("AllTablesIO.zip", "IOMake_After_Redefinitions_PRO_1997-2023_Summary.xlsx")
    us_xl = open_xl("AllTablesIO.zip", "IOUse_After_Redefinitions_PRO_1997-2023_Summary.xlsx")
    lamA = pd.read_csv(os.path.join(OUT, "lambda_us_family_a.csv")).set_index("year")

    # ---- hours levels by block: SEA (2000–2014) + KLEMS-index tails
    hidx, kcomp = klems_frames()
    kblocks = {name: klems_block(name) for name in hidx.index}
    unmapped_k = [n for n, b in kblocks.items() if b is None and "all industries" not in n.lower()]
    sea_h = sea_usa_hours()
    sea_blocks = {}
    for code, row in sea_h.iterrows():
        b = ISIC_BLOCK.get(str(code))
        if b:
            sea_blocks.setdefault(b, np.zeros(15))
            sea_blocks[b] += row.values.astype(float)
    blocks = sorted(sea_blocks)
    hours_b = pd.DataFrame(index=blocks, columns=YEARS, dtype=float)
    for b in blocks:
        for i, yr in enumerate(range(2000, 2015)):
            hours_b.loc[b, yr] = sea_blocks[b][i]
        members = [n for n, bb in kblocks.items() if bb == b and n in hidx.index]
        if members:
            w = kcomp.loc[members, 2014].astype(float).clip(lower=0)
            w = w / w.sum() if w.sum() > 0 else pd.Series(1 / len(members), index=members)
            for yr in YEARS:
                if yr < 2000 or yr > 2014:
                    ratio = float((hidx.loc[members, yr] / hidx.loc[members, 2014] * w).sum())
                    hours_b.loc[b, yr] = sea_blocks[b][14] * ratio
    ledger.append(("hours", f"{len(blocks)} blocks; KLEMS-unmapped rows: {unmapped_k[:4]}",
                   f"tail extension 1997–99 + 2015–23 by KLEMS index"))

    # ---- S&S rent shares → per-BEA-industry ρ(t)
    z = zipfile.ZipFile(os.path.join(CACHE, "stansum_replication.zip"))
    ss = pd.read_stata(io.BytesIO(z.read("Replication - Figs and Tables/Data/data_industry_figs_tables.dta")))
    ss = ss.dropna(subset=["implabrents", "compensation"])
    ss["rho_comp"] = (ss["implabrents"] / ss["compensation"]).clip(0, 0.6)
    agg = pd.read_stata(io.BytesIO(z.read("Replication - Figs and Tables/Data/data_aggregate_figs_table1.dta")))
    agg = agg[agg["industry"].str.startswith("Corporate")]
    rho_agg = (agg.set_index("year")["implabrentshare"] / agg.set_index("year")["laborshare"]).clip(0, 0.6)
    rho_bea = {}   # (bea_code, year) → rho
    for ind, rows_ in ss.groupby("indcode"):
        for code in SS_BEA.get(str(ind), []):
            for _, r in rows_.iterrows():
                rho_bea[(code, int(r["year"]))] = float(r["rho_comp"])

    # ---- per-year assembly
    out_rows = []
    for yr in YEARS:
        tr, dr, mk, us = (parse(x.parse(str(yr), header=None)) for x in (tr_xl, dr_xl, mk_xl, us_xl))
        inds = [i for i in tr.index if i in mk.index]
        coms = [c for c in tr.columns if c in mk.columns]
        V = mk.loc[inds, coms].fillna(0.0)
        q = V.sum(axis=0)
        W = np.nan_to_num(V.values / np.where(q.values[None, :] == 0, np.nan, q.values[None, :]))
        Bc = dr.loc[coms, inds].fillna(0.0).values
        v_w = dr.loc["V001", inds].fillna(0.0).values
        TRpub = tr.loc[inds, coms].fillna(0.0).values
        Ic = np.eye(len(coms))
        M_c = (-us.loc[coms, "F050"].fillna(0.0)).clip(lower=0.0)
        phi = (q / (q + M_c)).clip(0.0, 1.0).fillna(0.0).values
        TRdom = W @ np.linalg.inv(Ic - (phi[:, None] * Bc) @ W)
        fd_cols = [c for c in us.columns if c.startswith("F") and c not in FD_EXCLUDE]
        FD = us.loc[coms, fd_cols].fillna(0.0).sum(axis=1)
        g = V.sum(axis=1)
        comp_lvl = v_w * g.values
        blk_of = [BEA_BLOCK.get(i) for i in inds]
        go_b = {}
        for i, b in zip(inds, blk_of):
            if b:
                go_b[b] = go_b.get(b, 0.0) + float(g[i])
        vh_b = {b: (hours_b.loc[b, yr] / go_b[b] if b in go_b and go_b[b] > 0 else np.nan)
                for b in blocks}
        wbar = comp_lvl.sum() / hours_b[yr].sum()

        row = {"year": yr, "wbar_us": wbar}
        for sname, members in SETS.items():
            mem = [m for m in members if m in coms]
            f = FD.loc[mem].clip(lower=0.0)
            f = (f / f.sum()).values
            idx_m = [coms.index(m) for m in mem]
            for tag, Mx in (("tot", TRpub), ("dom", TRdom)):
                r_vec = Mx[:, idx_m] @ f
                r_b = {}
                mapped = 0.0
                for val, b in zip(r_vec, blk_of):
                    if b:
                        r_b[b] = r_b.get(b, 0.0) + val
                        mapped += val
                H = float(sum(vh_b[b] * r_b[b] for b in r_b if not np.isnan(vh_b.get(b, np.nan))))
                row[f"H_{sname}_{tag}"] = H                       # hours per $1 (SEA hour units per $M — scale cancels in H_rel)
                row[f"Hrel_{sname}_{tag}"] = H * wbar
                lam = float(lamA.loc[yr, f"lam_{sname}_{tag}"])
                row[f"wrel_{sname}_{tag}"] = lam / (H * wbar) if H > 0 else np.nan
                row[f"bridge_cover_{sname}_{tag}"] = mapped / r_vec.sum()
                # rent purge (populated 1997–2016)
                if yr <= 2016:
                    rho_vec = np.array([rho_bea.get((i, yr), float(rho_agg.get(yr, np.nan)))
                                        for i in inds])
                    row[f"lampurged_{sname}_{tag}"] = float(((1 - rho_vec) * v_w) @ (Mx[:, idx_m] @ f))
        rho_mac = np.nanmean([rho_bea.get((c, yr), np.nan) for c in ("333", "334", "335")])
        row["rho_machinery_direct"] = rho_mac if yr <= 2016 else np.nan
        row["rho_aggregate"] = float(rho_agg.get(yr, np.nan))
        out_rows.append(row)
        print(f"  {yr} done", flush=True)

    res = pd.DataFrame(out_rows).set_index("year")
    res.to_csv(os.path.join(OUT, "lambda_us_hours_rent.csv"))
    print("\n=== ledger ===")
    for e in ledger:
        print("  ", " | ".join(str(x) for x in e))
    show = ["Hrel_narrow_tot", "wrel_narrow_tot", "lampurged_narrow_tot",
            "rho_machinery_direct", "rho_aggregate", "bridge_cover_narrow_tot"]
    print(res[show].round(4).to_string())

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    ax = axes[0]
    ax.plot(res.index, lamA.loc[res.index, "lam_narrow_tot"], lw=2, label="λ̂ (unit 2, narrow tot)")
    ax.plot(res.index, res["Hrel_narrow_tot"], lw=2, ls="--", label="H_rel (quantity leg)")
    ax.plot(res.index, res["lampurged_narrow_tot"], lw=1.5, ls=":",
            label="λ̂ rent-purged (S&S industry ρ, 1997–2016)")
    ax.set_title("λ̂ and its quantity leg — US narrow, total-requirements")
    ax.legend(fontsize=8)
    ax = axes[1]
    ax.plot(res.index, res["wrel_narrow_tot"], lw=2, label="w̄_rel = λ̂ / H_rel (price leg)")
    ax.plot(res.index, res["rho_machinery_direct"], lw=1.5, ls="--",
            label="S&S rent share, machinery direct (ρ)")
    ax.plot(res.index, res["rho_aggregate"], lw=1, ls=":", label="S&S rent share, corporate aggregate")
    ax.set_title("The rent-sensitive leg and the S&S anchors")
    ax.legend(fontsize=8)
    fig.suptitle("λ unit 5 — hours + rent layer · tier: accounting · UNREAD (gate read = unit 6)",
                 fontsize=10)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "lambda_us_hours_rent.png"), dpi=150)
    print("\nwrote data/lambda_us_hours_rent.csv and figures/lambda_us_hours_rent.png")

if __name__ == "__main__":
    main()
