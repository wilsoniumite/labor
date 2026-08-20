# compute_family_b.py — λ unit 4: the world referee (WIOD).
#
# World λ̂ = labor compensation embodied — all countries — per $1 of machinery
# final output, through the GLOBAL Leontief inverse of the world IO table.
#
# Legs:
#   WIOD 2016: 2000–2014, 44 areas × 56 sectors (ISIC4). SEA16: COMP and LAB
#     (self-employment axis free) and H_EMPE hours. Currency via shares —
#     (COMP/GO)_SEA is dimensionless; hours use WIOT USD output.
#   WIOD 2013: 1995–2011, 41 areas × 35 sectors (ISIC3), wiot_full.dta long
#     format; SEA13 labor layer; 2000–2011 overlap vs 2016 = vintage check.
#   Long-run WIOD: DOWNGRADED, recorded — its SEA has no labor variables
#     (GO/II/VA/EXP only; verified 2026-08-20), so no world λ̂ before 1995.
#   ICIO: data zips 403 every scriptable client — extension parked as the
#     documented manual download.
#
# Grid per year: {COMP, LAB} × {ROW=0 lower bound, ROW=mean} × sector set.
# Views: world ($1 of world machinery final demand) and USpurch ($1 of US
# machinery final purchases), the latter split into US vs foreign labor.
# H leg: hours embodied × world average hourly compensation = H_rel
# (dimensionless quantity leg); w̄_rel = λ̂ / H_rel.
# FD: all categories except inventories (detected as the signed category),
# cell-clip ≥ 0 — the committed rule.
#
# Exact global identity: v_resid′(I−A)⁻¹ ≡ 1 for the closed world table —
# machine precision, gates every year. UNREAD; the gate read is unit 6.

import io, os, re, sys, zipfile
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "..", "data", "cache")
OUT = os.path.join(HERE, "..", "data")
FIG = os.path.join(HERE, "..", "figures")

SETS16 = {"narrow": ["C26", "C27", "C28"], "medium": ["C26", "C27", "C28", "J62_J63"]}
# WIOD13 item numbers: 13 = Machinery Nec ('29'), 14 = Electrical and Optical
# ('30t33') — verified at build via USA gross output vs SEA (both USD).
SETS13 = {"narrow13": [13, 14]}
SEA13_OF_ITEM = {13: "29", 14: "30t33"}
Y16 = list(range(2000, 2015))
Y13 = list(range(1995, 2012))

def engine(Z, GO, FD, keys, v_w_map, v_h_map, us_mask, set_keys, fd_us_cols, ledger, tag):
    """Z: n×n ndarray; GO: n; FD: n×(kept fd cols) DataFrame (clipped);
    keys: list of (country, item) row identities; v_w_map/v_h_map: dicts
    variant→n-vector; us_mask: bool n; set_keys: dict set→bool n (supplier
    rows in the machinery set); fd_us_cols: columns of FD belonging to USA.
    Zero-GO sectors (empty WIOD sectors, stray flows) are dropped from the
    system — the identity is algebraically exact only on GO > 0 — and the
    dropped mass is reported."""
    K = GO > 0
    dropped_flow = float(Z[~K, :].sum() + Z[:, ~K].sum())
    Z = Z[np.ix_(K, K)]
    GOk = GO[K]
    FD = FD.loc[K.nonzero()[0]] if isinstance(FD, pd.DataFrame) else FD[K]
    v_w_map = {k: v[K] for k, v in v_w_map.items()}
    v_h_map = {k: v[K] for k, v in v_h_map.items()}
    us_mask = us_mask[K]
    set_keys = {s: m[K] for s, m in set_keys.items()}
    n = K.sum()
    A = Z / GOk[None, :]
    X = np.linalg.inv(np.eye(n) - A)
    v_resid = (GOk - Z.sum(axis=0)) / GOk
    ident = float(np.abs(v_resid @ X - 1.0).max())
    out = {"ident_err": ident, "n_dropped": int((~K).sum()), "dropped_flow": dropped_flow}
    fd_world = FD.sum(axis=1).values.clip(0)
    fd_us = FD[fd_us_cols].sum(axis=1).values.clip(0)
    for sname, smask in set_keys.items():
        for view, fd_all in (("world", fd_world), ("uspurch", fd_us)):
            f = fd_all * smask
            tot = f.sum()
            if tot <= 0:
                continue
            f = f / tot
            Xf = X @ f
            for vname, v in v_w_map.items():
                lam = float(v @ Xf)
                out[f"lam_{sname}_{view}_{vname}"] = lam
                if view == "uspurch":
                    out[f"lamUS_{sname}_{vname}"] = float((v * us_mask) @ Xf)
            for hname, vh in v_h_map.items():
                out[f"hours_{sname}_{view}_{hname}"] = float(vh @ Xf)   # hours per $M
    ledger.append((tag, f"ident {ident:.1e}",
                   " ".join(f"{k.split('lam_')[-1]}={v:.3f}" for k, v in out.items()
                            if k.startswith("lam_narrow"))))
    return out

# ---------------- WIOD13 ----------------
def run_wiod13(ledger, rows):
    p = os.path.join(CACHE, "wiot_full.dta")
    cols = ["year", "row_country", "col_country", "row_item", "col_item", "value"]
    parts = []
    for chunk in pd.read_stata(p, chunksize=2_000_000, columns=cols):
        chunk["value"] = chunk["value"].astype("float64")
        chunk["year"] = chunk["year"].astype("int16")
        chunk["row_item"] = chunk["row_item"].astype("int16")
        chunk["col_item"] = chunk["col_item"].astype("int16")
        parts.append(chunk)
    full = pd.concat(parts, ignore_index=True)
    del parts
    print(f"wiot_full loaded: {len(full):,} rows; years {full.year.min()}–{full.year.max()}; "
          f"row_item ≤ {full.row_item.max()}, col_item ≤ {full.col_item.max()}", flush=True)

    sea = pd.ExcelFile(os.path.join(CACHE, "wiod13_sea_jul14.xlsx")).parse("DATA")
    ycols13 = {y: f"_{y}" for y in Y13}
    sea_v = {}
    for var in ("COMP", "LAB", "GO", "VA", "H_EMP"):
        d = sea[sea["Variable"] == var].set_index(["Country", "Code"])
        sea_v[var] = d

    for yr in Y13:
        d = full[full.year == yr]
        zmask = (d.row_item <= 35) & (d.col_item <= 35)
        Zl = d[zmask]
        rc = sorted(set(zip(Zl.row_country, Zl.row_item)))
        idx = {k: i for i, k in enumerate(rc)}
        n = len(rc)
        Z = np.zeros((n, n))
        ri = Zl.row_country.astype(str) + "|" + Zl.row_item.astype(str)
        ci = Zl.col_country.astype(str) + "|" + Zl.col_item.astype(str)
        km = {f"{c}|{i}": idx[(c, i)] for (c, i) in rc}
        np.add.at(Z, (ri.map(km).values, ci.map(km).values), Zl.value.values)

        # specials: identify the GO row among row_item > 35. The intermediate-
        # total row has median(v/colsum) ≈ 1.000; gross output sits well above
        # (colsum + the whole VA block). Take the LARGEST median ratio in a
        # sane band; block if none qualifies.
        spec = d[(d.row_item > 35) & (d.col_item <= 35)]
        colsum = Z.sum(axis=0)
        cand = {}
        for it in sorted(spec.row_item.unique()):
            s = spec[spec.row_item == it]
            v = np.zeros(n)
            np.add.at(v, (s.col_country.astype(str) + "|" + s.col_item.astype(str)).map(km).values, s.value.values)
            with np.errstate(invalid="ignore", divide="ignore"):
                ratio = float(np.nanmedian(np.where(colsum > 0, v / np.maximum(colsum, 1e-9), np.nan)))
            if v.min() >= -1e-6 and 1.05 < ratio < 10:
                cand[it] = (ratio, v)
        if not cand:
            raise RuntimeError(f"{yr}: no GO row candidate (ratios rejected)")
        go_item = max(cand, key=lambda it: cand[it][0])
        GO = cand[go_item][1]

        # final demand: col_item > 35; inventories = the category with negatives
        fdl = d[(d.row_item <= 35) & (d.col_item > 35)]
        fd_cats = sorted(fdl.col_item.unique())
        neg_share = {c: (fdl[fdl.col_item == c].value < 0).mean() for c in fd_cats}
        inv_cat = max(neg_share, key=neg_share.get)
        keep = [c for c in fd_cats if c != inv_cat]
        FD = pd.DataFrame(0.0, index=range(n),
                          columns=[f"{cc}|{c}" for cc in sorted(fdl.col_country.unique()) for c in keep])
        for (cc, c), gg in fdl[fdl.col_item.isin(keep)].groupby(["col_country", "col_item"]):
            col = f"{cc}|{c}"
            v = np.zeros(n)
            np.add.at(v, (gg.row_country.astype(str) + "|" + gg.row_item.astype(str)).map(km).values,
                      gg.value.clip(lower=0).values)
            FD[col] = v
        fd_us_cols = [c for c in FD.columns if c.startswith("USA|")]

        # SEA shares mapped onto rows; countries absent in SEA → ROW variants
        def share(var):
            v = np.full(n, np.nan)
            num, den = sea_v[var], sea_v["GO"]
            for (c, i), j in idx.items():
                code = SEA13_OF_ITEM.get(i)
                key = (c, code) if code else None
                if code is None:
                    # only machinery codes hard-mapped; others via full code list
                    pass
            return v
        # full mapping: WIOD13 item order ↔ SEA13 code order (both 35 long)
        sea_codes = [c for c in sea[sea["Country"] == "USA"].Code.unique() if c != "TOT"]
        item_of = {i + 1: sea_codes[i] for i in range(len(sea_codes))}
        def share_full(var, den_var="GO"):
            v = np.full(n, np.nan)
            for (c, i), j in idx.items():
                code = item_of.get(i)
                try:
                    num = float(sea_v[var].loc[(c, code), ycols13[yr]])
                    den = float(sea_v[den_var].loc[(c, code), ycols13[yr]])
                    v[j] = num / den if den > 0 else np.nan
                except KeyError:
                    v[j] = np.nan
            return v
        vw_comp = share_full("COMP"); vw_lab = share_full("LAB")
        cover = ~np.isnan(vw_comp)
        w_mean = np.nansum(vw_comp * GO) / np.nansum(np.where(cover, GO, np.nan))
        l_mean = np.nansum(vw_lab * GO) / np.nansum(np.where(cover, GO, np.nan))
        v_w_map = {
            "comp_row0": np.where(cover, vw_comp, 0.0),
            "comp_rowm": np.where(cover, vw_comp, w_mean),
            "lab_row0": np.where(cover, vw_lab, 0.0),
            "lab_rowm": np.where(cover, vw_lab, l_mean),
        }
        # hours per $M USD of output (SEA hours: thousands of hours? — units
        # cancel in H_rel; kept raw and labeled)
        vh = np.full(n, np.nan)
        for (c, i), j in idx.items():
            code = item_of.get(i)
            try:
                h = float(sea_v["H_EMP"].loc[(c, code), ycols13[yr]])
                vh[j] = h / GO[j] if GO[j] > 0 else np.nan
            except KeyError:
                vh[j] = np.nan
        hcover = ~np.isnan(vh)
        h_mean = np.nansum(vh * GO) / np.nansum(np.where(hcover, GO, np.nan))
        v_h_map = {"h_row0": np.where(hcover, vh, 0.0), "h_rowm": np.where(hcover, vh, h_mean)}
        comp_usd = np.nansum(np.where(cover, vw_comp, 0.0) * GO)
        hours_tot = np.nansum(np.where(hcover, vh, 0.0) * GO)
        wbar = comp_usd / hours_tot if hours_tot > 0 else np.nan

        us_mask = np.array([c == "USA" for (c, i) in rc], dtype=float)
        set_keys = {s: np.array([i in items for (c, i) in rc], dtype=float)
                    for s, items in SETS13.items()}
        # sector-mapping check: USA machinery GO, WIOT vs SEA (both USD)
        map_dev = np.nan
        try:
            wiot_go = sum(GO[idx[("USA", i)]] for i in SETS13["narrow13"])
            sea_go = sum(float(sea_v["GO"].loc[("USA", SEA13_OF_ITEM[i]), ycols13[yr]])
                         for i in SETS13["narrow13"])
            map_dev = abs(wiot_go - sea_go) / sea_go
        except Exception:
            pass

        out = engine(Z, GO, FD, rc, v_w_map, v_h_map, us_mask, set_keys, fd_us_cols,
                     ledger, f"w13 {yr}")
        out.update({"year": yr, "release": "wiod13", "go_item": int(go_item),
                    "inv_cat": int(inv_cat), "map_dev": map_dev, "wbar": wbar,
                    "cover_share": float(np.nansum(np.where(cover, GO, 0)) / GO.sum())})
        rows.append(out)
        print(f"  w13 {yr} done (ident {out['ident_err']:.1e})", flush=True)

# ---------------- WIOD16 ----------------
def run_wiod16(ledger, rows):
    names = [nm for nm in zipfile.ZipFile(os.path.join(CACHE, "WIOTS_in_STATA.zip")).namelist()
             if nm.lower().endswith(".dta")]
    sea = pd.ExcelFile(os.path.join(CACHE, "wiod16_sea.xlsx")).parse("DATA")
    sea_v = {var: sea[sea["variable"] == var].set_index(["country", "code"])
             for var in ("COMP", "LAB", "GO", "VA", "H_EMPE")}
    for yr in Y16:
        nm = [x for x in names if str(yr) in x]
        if not nm:
            continue
        d = pd.read_stata(io.BytesIO(zread_big("WIOTS_in_STATA.zip", nm[0])))
        # columns: meta (IndustryCode/…/Year) + one value col per
        # (country, number): vAUS1..vROW61, numbers 1–56 industries, 57–61 FD
        val_cols = [c for c in d.columns if re.match(r"^v[A-Z]{3}\d+$", str(c))]
        ctry = d["Country"].astype(str)
        rnr = d["RNr"].astype(int)
        ind_rows = (rnr <= 56) & (ctry != "TOT")
        keys = list(zip(ctry[ind_rows], rnr[ind_rows]))
        code_of = dict(zip(rnr[ind_rows], d.loc[ind_rows, "IndustryCode"].astype(str)))
        n = len(keys)
        col_ind = [c for c in val_cols if 1 <= int(c[4:]) <= 56]
        col_fd = [c for c in val_cols if int(c[4:]) > 56]
        Z = d.loc[ind_rows, col_ind].fillna(0).values
        col_keys = [(c[1:4], int(c[4:])) for c in col_ind]
        order = [col_keys.index(k) for k in keys]
        Z = Z[:, order]
        go_row = d[(d["IndustryCode"].astype(str) == "GO")]
        GO = go_row[col_ind].fillna(0).values[0][order]
        # inventories = the FD category with negatives, detected pre-clip
        pre = d.loc[ind_rows, col_fd].fillna(0)
        negshare = {k: (pre[[c for c in col_fd if int(c[4:]) == k]] < 0).values.mean()
                    for k in sorted({int(c[4:]) for c in col_fd})}
        inv_cat = max(negshare, key=negshare.get)
        keep_fd = [c for c in col_fd if int(c[4:]) != inv_cat]
        FD = pre[keep_fd].clip(lower=0)
        FD.index = range(n)
        fd_us_cols = [c for c in keep_fd if c.startswith("vUSA")]
        ycol = yr if yr in sea_v["GO"].columns else str(yr)   # SEA16 headers are ints

        def share_full(var):
            v = np.full(n, np.nan)
            for j, (c, k) in enumerate(keys):
                code = code_of.get(k)
                try:
                    num = float(sea_v[var].loc[(c, code), ycol])
                    den = float(sea_v["GO"].loc[(c, code), ycol])
                    v[j] = num / den if den > 0 else np.nan
                except KeyError:
                    v[j] = np.nan
            return v
        vw_comp = share_full("COMP"); vw_lab = share_full("LAB")
        cover = ~np.isnan(vw_comp)
        w_mean = np.nansum(vw_comp * GO) / np.nansum(np.where(cover, GO, np.nan))
        l_mean = np.nansum(vw_lab * GO) / np.nansum(np.where(cover, GO, np.nan))
        v_w_map = {"comp_row0": np.where(cover, vw_comp, 0.0),
                   "comp_rowm": np.where(cover, vw_comp, w_mean),
                   "lab_row0": np.where(cover, vw_lab, 0.0),
                   "lab_rowm": np.where(cover, vw_lab, l_mean)}
        vh = np.full(n, np.nan)
        for j, (c, k) in enumerate(keys):
            code = code_of.get(k)
            try:
                h = float(sea_v["H_EMPE"].loc[(c, code), ycol])
                vh[j] = h / GO[j] if GO[j] > 0 else np.nan
            except KeyError:
                vh[j] = np.nan
        hcover = ~np.isnan(vh)
        h_mean = np.nansum(vh * GO) / np.nansum(np.where(hcover, GO, np.nan))
        v_h_map = {"h_row0": np.where(hcover, vh, 0.0), "h_rowm": np.where(hcover, vh, h_mean)}
        comp_usd = np.nansum(np.where(cover, vw_comp, 0.0) * GO)
        hours_tot = np.nansum(np.where(hcover, vh, 0.0) * GO)
        wbar = comp_usd / hours_tot if hours_tot > 0 else np.nan

        us_mask = np.array([c == "USA" for (c, k) in keys], dtype=float)
        set_keys = {s: np.array([code_of.get(k) in codes for (c, k) in keys], dtype=float)
                    for s, codes in SETS16.items()}
        out = engine(Z, GO, FD, keys, v_w_map, v_h_map, us_mask, set_keys, fd_us_cols,
                     ledger, f"w16 {yr}")
        out.update({"year": yr, "release": "wiod16", "inv_cat": int(inv_cat), "wbar": wbar,
                    "cover_share": float(np.nansum(np.where(cover, GO, 0)) / GO.sum())})
        rows.append(out)
        print(f"  w16 {yr} done (ident {out['ident_err']:.1e})", flush=True)

def zread_big(zname, fname):
    with zipfile.ZipFile(os.path.join(CACHE, zname)) as z:
        return z.read(fname)

def main():
    ledger, rows = [], []
    which = sys.argv[1] if len(sys.argv) > 1 else "both"
    if which in ("both", "w13"):
        run_wiod13(ledger, rows)
    if which in ("both", "w16"):
        run_wiod16(ledger, rows)
    res = pd.DataFrame(rows).set_index(["release", "year"]).sort_index()
    os.makedirs(OUT, exist_ok=True)
    mode = "a" if which in ("w16",) and os.path.exists(os.path.join(OUT, "lambda_world_family_b.csv")) else "w"
    if mode == "a":
        old = pd.read_csv(os.path.join(OUT, "lambda_world_family_b.csv")).set_index(["release", "year"])
        res = pd.concat([old[~old.index.isin(res.index)], res]).sort_index()
    # H_rel = hours embodied × world average hourly compensation (USD):
    # dimensionless quantity leg of the amended criteria; w̄_rel = λ̂/H_rel.
    for c in [c for c in res.columns if c.startswith("hours_")]:
        res[c.replace("hours_", "hrel_")] = res[c] * res["wbar"]
    # thin-labor exclusion: years whose SEA labor layer covers < 60% of world
    # output produce bands too wide to mean anything — excluded from the λ̂
    # series, flagged, never silently kept (SEA13 thins in 2010–11).
    thin = res["cover_share"] < 0.6
    res["thin_labor_excluded"] = thin
    drop_cols = [c for c in res.columns if c.startswith(("lam", "hours_", "hrel_"))]
    res.loc[thin, drop_cols] = np.nan
    if thin.any():
        print(f"thin-labor exclusion: {[f'{r}:{y}' for (r, y) in res.index[thin]]}")
    res.to_csv(os.path.join(OUT, "lambda_world_family_b.csv"))
    print("\n=== ledger ===")
    for e in ledger:
        print("  ", " | ".join(str(x) for x in e))
    lamcols = [c for c in res.columns if c.startswith("lam_narrow")]
    print("\n=== snapshots ===")
    print(res[lamcols].round(4).to_string())

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(9.5, 5.5))
    for rel, style in (("wiod13", "--"), ("wiod16", "-")):
        if rel not in res.index.get_level_values(0):
            continue
        sub = res.loc[rel]
        band_cols = [c for c in sub.columns if c.startswith("lam_narrow_world_")]
        ax.fill_between(sub.index, sub[band_cols].min(axis=1), sub[band_cols].max(axis=1),
                        alpha=0.2)
        ax.plot(sub.index, sub[band_cols].median(axis=1), style, lw=2,
                label=f"world λ̂ narrow, {rel} (band: COMP/LAB × ROW variants)")
        us_cols = [c for c in sub.columns if c.startswith("lam_narrow_uspurch_")]
        ax.plot(sub.index, sub[us_cols].median(axis=1), style, lw=1.1, alpha=0.6,
                label=f"US-purchases view, {rel} (median)")
    ax.set_ylabel("labor compensation embodied per $1 machinery final output")
    ax.set_title("λ̂ world — Family B (WIOD releases; global inverse, all-country labor)\n"
                 "tier: accounting · UNREAD (gate read = unit 6) · LR-WIOD leg downgraded: no labor layer")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "lambda_world_family_b.png"), dpi=150)
    print("\nwrote data/lambda_world_family_b.csv and figures/lambda_world_family_b.png")

if __name__ == "__main__":
    main()
