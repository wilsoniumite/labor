# compute_icio.py — λ unit 5b: the ICIO extension of the world referee
# (unlocked by Stella's manual download of the 2025-edition SML zips,
# 2026-08-20 — the five-click vendored step; 2006-2010_SML.zip not supplied
# yet, and 2006–2010 is fully covered by WIOD anyway).
#
# Same object and engine as unit 4 (compute_family_b.engine): world λ̂ and
# hours through the global inverse of the closed world table; views world /
# US-purchases with the US/foreign decomposition; {COMP, LAB} × {ROW=0,
# ROW=mean} bands.
#
# Labor layer, honestly labeled per year (labor_vintage column):
#   1995–1999: SEA13 shares (ISIC3, coarser map)      → "sea13"
#   2000–2014: SEA16 shares (ISIC4, near-1:1 map)     → "sea16"
#   2015–2022: SEA16 shares FROZEN at 2014            → "frozen2014"
# The frozen member attributes ALL post-2014 λ̂ movement to structure
# (A, trade, final demand) and NONE to within-industry share drift — a
# transparent conservative assumption, flagged in every output; the gate
# read weights it accordingly.
#
# ICIO areas without SEA labor data (incl. ROW) ride the {0, mean} band, as
# in unit 4. GO = the published OUT row (verified > column intermediate
# sum); FD excludes INVNT (committed rule); DPABR kept (consumption).

import os, sys, zipfile
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "..", "data", "cache")
OUT = os.path.join(HERE, "..", "data")
FIG = os.path.join(HERE, "..", "figures")
sys.path.insert(0, HERE)
from compute_family_b import engine

ZIPS = {  # year → zip
    **{y: "1995-2000_SML.zip" for y in range(1995, 2001)},
    **{y: "2001-2005_SML.zip" for y in range(2001, 2006)},
    **{y: "2011-2015_SML.zip" for y in range(2011, 2016)},
    **{y: "2016-2022_SML.zip" for y in range(2016, 2023)},
}
FD_CATS = {"HFCE", "NPISH", "GGFC", "GFCF", "INVNT", "DPABR"}
SETS_ICIO = {"narrow": ["C26", "C27", "C28"], "medium": ["C26", "C27", "C28", "J62_63"]}

# ICIO activity → SEA16 codes (shares pooled over the listed codes)
A16 = {
    "A01": ["A01"], "A02": ["A02"], "A03": ["A03"],
    "B05": ["B"], "B06": ["B"], "B07": ["B"], "B08": ["B"], "B09": ["B"],
    "C10T12": ["C10-C12"], "C13T15": ["C13-C15"], "C16": ["C16"],
    "C17_18": ["C17", "C18"], "C19": ["C19"], "C20": ["C20"], "C21": ["C21"],
    "C22": ["C22"], "C23": ["C23"], "C24A": ["C24"], "C24B": ["C24"],
    "C25": ["C25"], "C26": ["C26"], "C27": ["C27"], "C28": ["C28"],
    "C29": ["C29"], "C301": ["C30"], "C302T309": ["C30"],
    "C31T33": ["C31_C32", "C33"], "D": ["D35"], "E": ["E36", "E37-E39"],
    "F": ["F"], "G": ["G45", "G46", "G47"],
    "H49": ["H49"], "H50": ["H50"], "H51": ["H51"], "H52": ["H52"], "H53": ["H53"],
    "I": ["I"], "J58T60": ["J58", "J59_J60"], "J61": ["J61"], "J62_63": ["J62_J63"],
    "K": ["K64", "K65", "K66"], "L": ["L68"],
    "M": ["M69_M70", "M71", "M72", "M73", "M74_M75"], "N": ["N"],
    "O": ["O84"], "P": ["P85"], "Q": ["Q"], "R": ["R_S"], "S": ["R_S"], "T": ["T"],
}
# ICIO activity → SEA13 code (ISIC3; coarser — machinery block honesty:
# C26/C27 → 30t33 (electrical AND optical), C28 → 29)
A13 = {
    "A01": "AtB", "A02": "AtB", "A03": "AtB",
    "B05": "C", "B06": "C", "B07": "C", "B08": "C", "B09": "C",
    "C10T12": "15t16", "C13T15": "17t18", "C16": "20",
    "C17_18": "21t22", "C19": "23", "C20": "24", "C21": "24",
    "C22": "25", "C23": "26", "C24A": "27t28", "C24B": "27t28", "C25": "27t28",
    "C26": "30t33", "C27": "30t33", "C28": "29",
    "C29": "34t35", "C301": "34t35", "C302T309": "34t35",
    "C31T33": "36t37", "D": "E", "E": "E", "F": "F",
    "G": "51", "H49": "60", "H50": "61", "H51": "62", "H52": "63", "H53": "64",
    "I": "H", "J58T60": "71t74", "J61": "64", "J62_63": "71t74",
    "K": "J", "L": "70", "M": "71t74", "N": "71t74",
    "O": "L", "P": "M", "Q": "N", "R": "O", "S": "O", "T": "P",
}

def sea_tables():
    s16 = pd.ExcelFile(os.path.join(CACHE, "wiod16_sea.xlsx")).parse("DATA")
    s13 = pd.ExcelFile(os.path.join(CACHE, "wiod13_sea_jul14.xlsx")).parse("DATA")
    v16 = {v: s16[s16["variable"] == v].set_index(["country", "code"])
           for v in ("COMP", "LAB", "GO", "H_EMPE")}
    v13 = {v: s13[s13["Variable"] == v].set_index(["Country", "Code"])
           for v in ("COMP", "LAB", "GO", "H_EMP")}
    return v16, v13

def share_maps(v16, v13, yr):
    """Return (vintage, getter): getter(country, act, var) → share or nan.
    var ∈ {COMP, LAB, HRS} (HRS returns hours LEVEL, pooled)."""
    if yr >= 2000:
        y = min(yr, 2014); vintage = "sea16" if yr <= 2014 else "frozen2014"
        def get(c, act, var):
            codes = A16.get(act)
            if not codes:
                return np.nan
            try:
                if var == "HRS":
                    return sum(float(v16["H_EMPE"].loc[(c, k), y]) for k in codes)
                num = sum(float(v16[var].loc[(c, k), y]) for k in codes)
                den = sum(float(v16["GO"].loc[(c, k), y]) for k in codes)
                return num / den if den > 0 else np.nan
            except KeyError:
                return np.nan
        return vintage, get
    else:
        ycol = f"_{yr}"; vintage = "sea13"
        def get(c, act, var):
            k = A13.get(act)
            if not k:
                return np.nan
            try:
                if var == "HRS":
                    return float(v13["H_EMP"].loc[(c, k), ycol])
                num = float(v13[var].loc[(c, k), ycol])
                den = float(v13["GO"].loc[(c, k), ycol])
                return num / den if den > 0 else np.nan
            except KeyError:
                return np.nan
        return vintage, get

def main():
    v16, v13 = sea_tables()
    only = [int(a) for a in sys.argv[1:]] or sorted(ZIPS)
    ledger, rows = [], []
    for yr in only:
        zf = zipfile.ZipFile(os.path.join(CACHE, ZIPS[yr]))
        with zf.open(f"{yr}_SML.csv") as f:
            d = pd.read_csv(f, index_col=0)
        cols = list(d.columns)
        ind_cols = [c for c in cols if "_" in c and c.split("_", 1)[1] not in FD_CATS and c != "OUT"]
        fd_cols = [c for c in cols if "_" in c and c.split("_", 1)[1] in FD_CATS]
        ind_rows = [r for r in d.index if r in set(ind_cols)]
        assert len(ind_rows) == len(ind_cols), f"{yr}: row/col industry mismatch"
        Z = d.loc[ind_rows, ind_rows].fillna(0.0).values
        GO = d.loc["OUT", ind_rows].fillna(0.0).values
        ratio = np.nanmedian(np.where(Z.sum(axis=0) > 0, GO / np.maximum(Z.sum(axis=0), 1e-9), np.nan))
        assert ratio > 1.05, f"{yr}: OUT row fails the gross-output ratio test ({ratio:.3f})"
        pre = d.loc[ind_rows, fd_cols].fillna(0.0)
        keep_fd = [c for c in fd_cols if c.split("_", 1)[1] != "INVNT"]
        FD = pre[keep_fd].clip(lower=0.0)
        FD.index = range(len(ind_rows))
        fd_us_cols = [c for c in keep_fd if c.startswith("USA_")]

        keys = [(r.split("_", 1)[0], r.split("_", 1)[1]) for r in ind_rows]
        vintage, get = share_maps(v16, v13, yr)
        n = len(keys)
        vw_comp = np.array([get(c, a, "COMP") for c, a in keys])
        vw_lab = np.array([get(c, a, "LAB") for c, a in keys])
        hrs = np.array([get(c, a, "HRS") for c, a in keys])
        vh = np.where((hrs > 0) & (GO > 0), hrs / np.maximum(GO, 1e-9), np.nan)
        cover = ~np.isnan(vw_comp)
        w_mean = np.nansum(vw_comp * GO) / np.nansum(np.where(cover, GO, np.nan))
        l_mean = np.nansum(vw_lab * GO) / np.nansum(np.where(cover, GO, np.nan))
        v_w_map = {"comp_row0": np.where(cover, vw_comp, 0.0),
                   "comp_rowm": np.where(cover, vw_comp, w_mean),
                   "lab_row0": np.where(cover, np.nan_to_num(vw_lab), 0.0),
                   "lab_rowm": np.where(cover, np.nan_to_num(vw_lab), l_mean)}
        hcover = ~np.isnan(vh)
        h_mean = np.nansum(np.where(hcover, vh, 0.0) * GO) / np.nansum(np.where(hcover, GO, np.nan))
        v_h_map = {"h_row0": np.where(hcover, vh, 0.0), "h_rowm": np.where(hcover, vh, h_mean)}
        comp_usd = np.nansum(np.where(cover, vw_comp, 0.0) * GO)
        hours_tot = np.nansum(np.where(hcover, vh, 0.0) * GO)
        wbar = comp_usd / hours_tot if hours_tot > 0 else np.nan
        us_mask = np.array([c == "USA" for c, a in keys], dtype=float)
        set_keys = {s: np.array([a in acts for c, a in keys], dtype=float)
                    for s, acts in SETS_ICIO.items()}

        out = engine(Z, GO, FD, keys, v_w_map, v_h_map, us_mask, set_keys, fd_us_cols,
                     ledger, f"icio {yr}")
        out.update({"year": yr, "release": "icio25", "labor_vintage": vintage,
                    "wbar": wbar,
                    "cover_share": float(np.nansum(np.where(cover, GO, 0)) / GO.sum())})
        rows.append(out)
        print(f"  icio {yr} done ({vintage}, ident {out['ident_err']:.1e})", flush=True)

    res = pd.DataFrame(rows).set_index(["release", "year"]).sort_index()
    for c in [c for c in res.columns if c.startswith("hours_")]:
        res[c.replace("hours_", "hrel_")] = res[c] * res["wbar"]
    fp = os.path.join(OUT, "lambda_world_family_b.csv")
    old = pd.read_csv(fp).set_index(["release", "year"])
    res = pd.concat([old[~old.index.isin(res.index)], res]).sort_index()
    res.to_csv(fp)
    print("\n=== ledger ===")
    for e in ledger:
        print("  ", " | ".join(str(x) for x in e))
    icio = res.loc["icio25"]
    show = [c for c in icio.columns if c.startswith("lam_narrow_world_")] + ["labor_vintage", "cover_share"]
    print(icio[show].round(4).to_string())

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(9.5, 5.5))
    for rel, style in (("wiod13", ":"), ("wiod16", "--"), ("icio25", "-")):
        if rel not in res.index.get_level_values(0):
            continue
        sub = res.loc[rel]
        band_cols = [c for c in sub.columns if c.startswith("lam_narrow_world_")
                     or (rel == "wiod13" and c.startswith("lam_narrow13_world_"))]
        band = sub[band_cols].dropna(how="all")
        ax.fill_between(band.index, band.min(axis=1), band.max(axis=1), alpha=0.15)
        ax.plot(band.index, band.median(axis=1), style, lw=2, label=f"world λ̂ narrow, {rel}")
    frozen = res.loc["icio25"].query("labor_vintage == 'frozen2014'")
    if len(frozen):
        ax.axvspan(frozen.index.min() - 0.5, frozen.index.max() + 0.5, alpha=0.08, color="gray")
        ax.text(frozen.index.min() + 0.2, ax.get_ylim()[0] + 0.01,
                "shares frozen at 2014\n(structure-only)", fontsize=7)
    ax.set_ylabel("labor compensation embodied per $1 machinery final output")
    ax.set_title("λ̂ world — three releases (WIOD 13/16 + ICIO 2025 via manual download)\n"
                 "tier: accounting · UNREAD (gate read = unit 6) · 2006–2010 ICIO zip not yet supplied")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "lambda_world_family_b.png"), dpi=150)
    print("\nwrote lambda_world_family_b.csv (+icio25) and refreshed the figure")

if __name__ == "__main__":
    main()
