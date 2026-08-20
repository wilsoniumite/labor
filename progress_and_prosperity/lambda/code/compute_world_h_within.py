# compute_world_h_within.py — unit 6a: the repaired world quantity leg
# (Stella's Option A, spec amendment 2026-08-20 — committed before this ran).
#
# Object: per release, countries' embodied hours per $1 of WORLD machinery
# final demand (narrow set, world view — same f as the read), split by the
# country where the hours are worked:
#     h_c(t) = Σ_{i ∈ country c} v_h[i] · (X f)[i]
#     comp_c(t) = Σ_{i ∈ country c} v_w[i] · (X f)[i]
# over SEA-covered countries only (uncovered/ROW contribute no hours under
# row0 and are excluded from the index; stated).
#
# Indices (the two grid members per release):
#   Törnqvist (chained):  Δln H_within = Σ_c ½(s_c(t−1)+s_c(t))·Δln h_c
#                         with s_c = comp_c / Σ comp_c, over countries with
#                         h_c > 0 in both adjacent years.
#   Laspeyres (fixed base = release's first sourced year):
#                         H_L(t) = Σ_c s_c(base)·h_c(t)/h_c(base).
# Between (relocation) component, reported not gated:
#   Δln(H_raw) − Δln(H_within), H_raw = Σ_c h_c.
#
# Loaders duplicate the verified constructions of compute_family_b.py /
# compute_icio.py (same matrices, same FD rule); ICIO frozen-2014 years are
# computed but flagged supporting-only, as everywhere.

import io, os, sys, zipfile
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "..", "data", "cache")
OUT = os.path.join(HERE, "..", "data")
sys.path.insert(0, HERE)
from compute_icio import A16, A13, ZIPS, FD_CATS, sea_tables, share_maps

NARROW16 = ["C26", "C27", "C28"]
NARROW13_ITEMS = [13, 14]
NARROW_ICIO = ["C26", "C27", "C28"]

def percountry(Z, GO, FD_kept, keys, v_w, v_h, smask):
    K = GO > 0
    Z = Z[np.ix_(K, K)]; GOk = GO[K]
    keys = [k for k, kk in zip(keys, K) if kk]
    v_w = v_w[K]; v_h = v_h[K]; smask = smask[K]
    fd = FD_kept[K]
    A = Z / GOk[None, :]
    X = np.linalg.inv(np.eye(K.sum()) - A)
    f = fd * smask
    f = f / f.sum()
    r = X @ f
    hw = v_h * r
    cw = v_w * r
    out = {}
    for j, (c, i) in enumerate(keys):
        if hw[j] > 0 or cw[j] > 0:
            h0, c0 = out.get(c, (0.0, 0.0))
            out[c] = (h0 + hw[j], c0 + cw[j])
    return out

def run_wiod16():
    names = [nm for nm in zipfile.ZipFile(os.path.join(CACHE, "WIOTS_in_STATA.zip")).namelist()
             if nm.lower().endswith(".dta")]
    sea = pd.ExcelFile(os.path.join(CACHE, "wiod16_sea.xlsx")).parse("DATA")
    sea_v = {var: sea[sea["variable"] == var].set_index(["country", "code"])
             for var in ("COMP", "GO", "H_EMPE")}
    import re
    rows = []
    for yr in range(2000, 2015):
        nm = [x for x in names if str(yr) in x][0]
        with zipfile.ZipFile(os.path.join(CACHE, "WIOTS_in_STATA.zip")) as z:
            d = pd.read_stata(io.BytesIO(z.read(nm)))
        val_cols = [c for c in d.columns if re.match(r"^v[A-Z]{3}\d+$", str(c))]
        ctry = d["Country"].astype(str); rnr = d["RNr"].astype(int)
        ind_rows = (rnr <= 56) & (ctry != "TOT")
        keys = list(zip(ctry[ind_rows], rnr[ind_rows]))
        code_of = dict(zip(rnr[ind_rows], d.loc[ind_rows, "IndustryCode"].astype(str)))
        col_ind = [c for c in val_cols if 1 <= int(c[4:]) <= 56]
        col_fd = [c for c in val_cols if int(c[4:]) > 56]
        Z = d.loc[ind_rows, col_ind].fillna(0).values
        col_keys = [(c[1:4], int(c[4:])) for c in col_ind]
        order = [col_keys.index(k) for k in keys]
        Z = Z[:, order]
        GO = d[d["IndustryCode"].astype(str) == "GO"][col_ind].fillna(0).values[0][order]
        pre = d.loc[ind_rows, col_fd].fillna(0)
        negshare = {k: (pre[[c for c in col_fd if int(c[4:]) == k]] < 0).values.mean()
                    for k in sorted({int(c[4:]) for c in col_fd})}
        inv_cat = max(negshare, key=negshare.get)
        FD = pre[[c for c in col_fd if int(c[4:]) != inv_cat]].clip(lower=0).sum(axis=1).values
        ycol = yr
        n = len(keys)
        v_w = np.zeros(n); v_h = np.zeros(n)
        for j, (c, k) in enumerate(keys):
            code = code_of.get(k)
            try:
                go = float(sea_v["GO"].loc[(c, code), ycol])
                if go > 0:
                    v_w[j] = float(sea_v["COMP"].loc[(c, code), ycol]) / go
                    v_h[j] = float(sea_v["H_EMPE"].loc[(c, code), ycol]) / GO[j] if GO[j] > 0 else 0.0
            except KeyError:
                pass
        smask = np.array([code_of.get(k) in NARROW16 for c, k in keys], dtype=float)
        pc = percountry(Z, GO, FD, keys, v_w, v_h, smask)
        for c, (h, cm) in pc.items():
            rows.append({"release": "wiod16", "year": yr, "country": c, "h": h, "comp": cm})
        print(f"  w16 {yr}: {len(pc)} countries", flush=True)
    return rows

def run_wiod13():
    p = os.path.join(CACHE, "wiot_full.dta")
    full = pd.concat(list(pd.read_stata(p, chunksize=2_000_000,
                     columns=["year", "row_country", "col_country", "row_item", "col_item", "value"])),
                     ignore_index=True)
    sea = pd.ExcelFile(os.path.join(CACHE, "wiod13_sea_jul14.xlsx")).parse("DATA")
    sea_v = {var: sea[sea["Variable"] == var].set_index(["Country", "Code"])
             for var in ("COMP", "GO", "H_EMP")}
    sea_codes = [c for c in sea[sea["Country"] == "USA"].Code.unique() if c != "TOT"]
    item_of = {i + 1: sea_codes[i] for i in range(len(sea_codes))}
    rows = []
    for yr in list(range(1995, 2010)):
        d = full[full.year == yr]
        zmask = (d.row_item <= 35) & (d.col_item <= 35)
        Zl = d[zmask]
        rc = sorted(set(zip(Zl.row_country.astype(str), Zl.row_item.astype(int))))
        idx = {k: i for i, k in enumerate(rc)}
        km = {f"{c}|{i}": idx[(c, i)] for (c, i) in rc}
        n = len(rc)
        Z = np.zeros((n, n))
        np.add.at(Z, ((Zl.row_country.astype(str) + "|" + Zl.row_item.astype(str)).map(km).values,
                      (Zl.col_country.astype(str) + "|" + Zl.col_item.astype(str)).map(km).values),
                  Zl.value.values)
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
        go_item = max(cand, key=lambda it: cand[it][0])
        GO = cand[go_item][1]
        fdl = d[(d.row_item <= 35) & (d.col_item > 35)]
        fd_cats = sorted(fdl.col_item.unique())
        neg = {c: (fdl[fdl.col_item == c].value < 0).mean() for c in fd_cats}
        keep = [c for c in fd_cats if c != max(neg, key=neg.get)]
        FD = np.zeros(n)
        kk = fdl[fdl.col_item.isin(keep)]
        np.add.at(FD, (kk.row_country.astype(str) + "|" + kk.row_item.astype(str)).map(km).values,
                  kk.value.clip(lower=0).values)
        ycol = f"_{yr}"
        v_w = np.zeros(n); v_h = np.zeros(n)
        for (c, i), j in idx.items():
            code = item_of.get(i)
            try:
                go = float(sea_v["GO"].loc[(c, code), ycol])
                if go > 0:
                    v_w[j] = float(sea_v["COMP"].loc[(c, code), ycol]) / go
                    v_h[j] = float(sea_v["H_EMP"].loc[(c, code), ycol]) / GO[j] if GO[j] > 0 else 0.0
            except KeyError:
                pass
        smask = np.array([i in NARROW13_ITEMS for (c, i) in rc], dtype=float)
        pc = percountry(Z, GO, FD, rc, np.nan_to_num(v_w), np.nan_to_num(v_h), smask)
        for c, (h, cm) in pc.items():
            rows.append({"release": "wiod13", "year": yr, "country": c, "h": h, "comp": cm})
        print(f"  w13 {yr}: {len(pc)} countries", flush=True)
    return rows

def run_icio():
    v16, v13 = sea_tables()
    rows = []
    for yr in sorted(ZIPS):
        zf = zipfile.ZipFile(os.path.join(CACHE, ZIPS[yr]))
        with zf.open(f"{yr}_SML.csv") as f:
            d = pd.read_csv(f, index_col=0)
        cols = list(d.columns)
        ind_cols = [c for c in cols if "_" in c and c.split("_", 1)[1] not in FD_CATS and c != "OUT"]
        fd_cols = [c for c in cols if "_" in c and c.split("_", 1)[1] in FD_CATS]
        ind_rows = [r for r in d.index if r in set(ind_cols)]
        Z = d.loc[ind_rows, ind_rows].fillna(0.0).values
        GO = d.loc["OUT", ind_rows].fillna(0.0).values
        keep_fd = [c for c in fd_cols if c.split("_", 1)[1] != "INVNT"]
        FD = d.loc[ind_rows, keep_fd].fillna(0.0).clip(lower=0).sum(axis=1).values
        keys = [(r.split("_", 1)[0], r.split("_", 1)[1]) for r in ind_rows]
        vintage, get = share_maps(v16, v13, yr)
        n = len(keys)
        v_w = np.zeros(n); v_h = np.zeros(n)
        for j, (c, a) in enumerate(keys):
            w = get(c, a, "COMP")
            if np.isfinite(w):
                v_w[j] = w
                hrs = get(c, a, "HRS")
                v_h[j] = hrs / GO[j] if np.isfinite(hrs) and GO[j] > 0 else 0.0
        smask = np.array([a in NARROW_ICIO for c, a in keys], dtype=float)
        pc = percountry(Z, GO, FD, keys, v_w, v_h, smask)
        for c, (h, cm) in pc.items():
            rows.append({"release": "icio25", "year": yr, "country": c, "h": h, "comp": cm,
                         "vintage": vintage})
        print(f"  icio {yr}: {len(pc)} countries ({vintage})", flush=True)
    return rows

def indices(df):
    """Per release: chained Törnqvist + fixed-base Laspeyres over countries."""
    out = []
    for rel, sub in df.groupby("release"):
        piv_h = sub.pivot_table(index="year", columns="country", values="h")
        piv_c = sub.pivot_table(index="year", columns="country", values="comp")
        years = sorted(piv_h.index)
        base = years[0]
        # Törnqvist chained
        lnH = {base: 0.0}
        for y0, y1 in zip(years[:-1], years[1:]):
            common = [c for c in piv_h.columns
                      if piv_h.loc[y0, c] > 0 and piv_h.loc[y1, c] > 0
                      and pd.notna(piv_h.loc[y0, c]) and pd.notna(piv_h.loc[y1, c])]
            s0 = piv_c.loc[y0, common] / piv_c.loc[y0, common].sum()
            s1 = piv_c.loc[y1, common] / piv_c.loc[y1, common].sum()
            dln = float((0.5 * (s0 + s1) * np.log(piv_h.loc[y1, common] / piv_h.loc[y0, common])).sum())
            lnH[y1] = lnH[y0] + dln
        # Laspeyres fixed base
        bcommon = [c for c in piv_h.columns if piv_h.loc[base, c] > 0 and pd.notna(piv_h.loc[base, c])]
        sb = piv_c.loc[base, bcommon] / piv_c.loc[base, bcommon].sum()
        for y in years:
            rel_h = piv_h.loc[y, bcommon] / piv_h.loc[base, bcommon]
            lasp = float((sb * rel_h).dropna().sum() / sb[rel_h.notna()].sum())
            raw = float(piv_h.loc[y].sum() / piv_h.loc[base].sum())
            row = {"release": rel, "year": y, "H_within_tornqvist": float(np.exp(lnH[y])),
                   "H_within_laspeyres": lasp, "H_raw": raw}
            if "vintage" in sub.columns:
                v = sub[sub.year == y]["vintage"].iloc[0]
                row["vintage"] = v
            out.append(row)
    return pd.DataFrame(out)

def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    rows = []
    if which in ("all", "wiod"):
        rows += run_wiod13()
        rows += run_wiod16()
    if which in ("all", "icio"):
        rows += run_icio()
    df = pd.DataFrame(rows)
    fp = os.path.join(OUT, "world_h_within_countries.csv")
    if which != "all" and os.path.exists(fp):
        old = pd.read_csv(fp)
        df = pd.concat([old[~old.release.isin(df.release.unique())], df], ignore_index=True)
    df.to_csv(fp, index=False)
    idx = indices(df)
    idx.to_csv(os.path.join(OUT, "world_h_within_index.csv"), index=False)
    print("\n=== within-country hours indices ===")
    print(idx.round(4).to_string(index=False))

if __name__ == "__main__":
    main()
