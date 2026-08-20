# compute_century.py — λ unit 3: benchmark-year λ̂_US 1947–1992 (SIC era) and
# the splice onto the 1997–2023 NAICS series (unit 2).
#
# BEA's own caveat, carried on every output: the historical benchmark tables
# "should not be used as a time series" (classification changes, no
# comprehensive back-revision). They are used here as benchmark POINTS, with
# the splice step reported and within-segment directions preserved.
#
# Self-identifying parsing (no hand-keyed row meanings):
#   - Rows/cols with numeric prefix 1–85 are industries/commodities; prefix
#     ≥86 (VA rows 86–90, final-demand columns 90–99) are specials, per the
#     85-order convention that also carries into the two-digit vintages.
#   - The VA block is the greedy subset of positive special rows whose
#     economy-wide total best matches revised GDP (HIST file), trying unit
#     scales {1e-3, 1, 1e3} — scale cancels everywhere else (v_w is a ratio,
#     f is normalized), so the anchor alone needs it. Gap reported.
#   - Compensation = the largest VA-block row, share of block in [0.45, 0.72]
#     (compensation has always dominated VA). Vintages whose table carries
#     only a total-VA row (no split) emit the VA-content series λ̂_VA only,
#     and the ledger says so — no imputation backward.
#   - Final-demand columns: special columns with positive totals (imports —
#     negative-total columns — drop out); f_c = Σ max(cell, 0), normalized
#     on the machine set (committed cell-clip rule).
#   - Published total requirements used everywhere: in-file TR (1947, 1963,
#     1967), the separate 1958 TR workbook, in-file IxC TR (1972, 1977), the
#     trailing ×1e7 fields (1982), TBL5 (1987), IXCTR.TXT (1992). For
#     1987/1992 the make+use reconstruction (unit-2 algebra) is compared to
#     the published TR as a check.
#
# Machine set, SIC 85-order: 43–58 (nonelectrical machinery 43–52 incl.
# office & computing 51; electrical 53–58). Variant "+i" adds 62
# (scientific instruments — NAICS 334 ancestry). Two-digit letter splits
# (26A, 51A, …) map by leading digits. Software/computer services are not
# separable before the NAICS era at these levels; the century set is
# narrow-only and says so.

import io, os, re, zipfile
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "..", "data", "cache")
OUT = os.path.join(HERE, "..", "data")
FIG = os.path.join(HERE, "..", "figures")

GDP_TOL = 0.15
COMP_BAND = (0.45, 0.72)
SET_MAIN = set(range(43, 59))
SET_INSTR = SET_MAIN | {62}
SCALES = (1e-3, 1e-1, 1.0, 1e3)   # 1982 ships in $100K units (0.1×$M)

def zopen(zname, fname):
    return zipfile.ZipFile(os.path.join(CACHE, zname)).read(fname)

def num(x):
    return pd.to_numeric(x, errors="coerce")

def norm_code(s):
    s = str(s).strip().strip('"')
    m = re.match(r"^0*(\d+)", s)
    return m.group(1) + s[m.end():].strip() if m else s

def prefix(code):
    m = re.match(r"^(\d+)", str(code))
    return int(m.group(1)) if m else None

def is_industry(code):
    p = prefix(code)
    return p is not None and 1 <= p <= 85

def hist_anchors():
    xl = pd.ExcelFile(io.BytesIO(zopen("AllTablesHIST.zip", "GDPbyInd_VA_1947-1997.xlsx")))
    va = xl.parse("VA", header=None)
    years = [str(y) for y in va.iloc[5, 2:].tolist()]
    gdp_row = va[va[1].astype(str).str.strip() == "Gross domestic product"].index[0]
    gdp = {y: float(v) for y, v in zip(years, va.iloc[gdp_row, 2:].tolist())
           if str(v) not in ("...", "nan")}
    comp = xl.parse("Components", header=None)
    crow = comp[comp[1].astype(str).str.strip() == "Compensation of employees"].index[0]
    cyears = [str(y) for y in comp.iloc[5, 2:].tolist()]
    ccomp = {y: float(v) for y, v in zip(cyears, comp.iloc[crow, 2:].tolist())
             if str(v) not in ("...", "nan")}
    return gdp, ccomp

def long_to_mat(df, rcol, ccol, vcol):
    M = df.pivot_table(index=rcol, columns=ccol, values=vcol, aggfunc="sum")
    M.index = [str(x) for x in M.index]
    M.columns = [str(x) for x in M.columns]
    return M

def identify(M, gdp_y, ledger, tag):
    """Returns comp_row (or None), va_rows, fd_cols, diagnostics."""
    ind_cols = [c for c in M.columns if is_industry(c)]
    special_rows = [r for r in M.index if not is_industry(r)]
    special_cols = [c for c in M.columns if not is_industry(c)]
    totals = {r: float(M.loc[r, ind_cols].fillna(0).sum()) for r in special_rows}
    pos = {r: t for r, t in totals.items() if t > 0}
    best = (None, np.inf, 1.0)          # (rows, gap, scale)
    for sc in SCALES:
        acc, s = [], 0.0
        for r in sorted(pos, key=lambda r: -pos[r]):
            acc, s = acc + [r], s + pos[r] * sc
            gap = abs(s - gdp_y) / gdp_y
            if gap < best[1]:
                best = (list(acc), gap, sc)
    va_rows, gap, scale = best
    if va_rows is None:
        ledger.append((tag, "no positive special rows")); return None, [], [], gap, np.nan, scale
    comp_row = max(va_rows, key=lambda r: pos[r])
    cshare = pos[comp_row] / sum(pos[r] for r in va_rows)
    fd_cols = [c for c in special_cols
               if float(M[c].reindex([r for r in M.index if is_industry(r)]).fillna(0).sum()) > 0]
    split_ok = gap < GDP_TOL and COMP_BAND[0] <= cshare <= COMP_BAND[1] and len(va_rows) >= 2
    ledger.append((tag, f"VA rows {va_rows} gap {gap:.1%} scale {scale:g}",
                   f"comp {comp_row} share {cshare:.2f} split_ok={split_ok}",
                   f"FD {fd_cols}"))
    return (comp_row if split_ok else None), va_rows, fd_cols, gap, cshare, scale

def machine_targets(codes, with_instr):
    tgt = SET_INSTR if with_instr else SET_MAIN
    return [c for c in codes if prefix(c) in tgt]

def point(M_use, TR, comp_row, va_rows, fd_cols, ledger, tag):
    """λ̂ (if comp available) and λ̂_VA for both set variants."""
    ind = [i for i in TR.index if i in M_use.columns and is_industry(i)]
    g = M_use[ind].fillna(0).sum(axis=0)
    ind = [i for i in ind if g[i] > 0]
    g = g[ind]
    v_all = (M_use.loc[va_rows, ind].fillna(0).sum(axis=0) / g).astype(float)
    v_w = (M_use.loc[comp_row, ind].fillna(0) / g).astype(float) if comp_row else None
    out = {}
    target_rows = [r for r in M_use.index if is_industry(r)]
    fd = M_use.loc[target_rows, [c for c in fd_cols if c in M_use.columns]].clip(lower=0).sum(axis=1)
    for suffix, wi in (("", False), ("i", True)):
        tset = [c for c in machine_targets(TR.columns, wi) if c in fd.index and fd[c] > 0]
        f = fd.loc[tset]; f = f / f.sum()
        TRs = TR.loc[ind, f.index].fillna(0)
        # full-VA resolution ≈ 1 (minus import leakage): the parse CHECK,
        # not a series — near-1 by construction for published TRs
        out[f"res_va{suffix}"] = float(v_all.values @ TRs.values @ f.values)
        if v_w is not None:
            out[f"lam{suffix}"] = float(v_w.values @ TRs.values @ f.values)
        if suffix == "":
            out["n_set"] = len(f)
    ledger.append((tag, f"λ̂={out.get('lam', float('nan')):.4f}",
                   f"res_VA={out['res_va']:.4f}", f"n_set={out['n_set']}"))
    return out

def parse_xls(zname, fname, cmap, skip=1):
    raw = pd.ExcelFile(io.BytesIO(zopen(zname, fname))).parse(0, header=None, skiprows=skip)
    df = pd.DataFrame({k: raw[v] for k, v in cmap.items()})
    df["r"] = df["r"].map(norm_code); df["c"] = df["c"].map(norm_code)
    for k in cmap:
        if k not in ("r", "c"):
            df[k] = num(df[k])
    return df

def rd_csvish(zname, fname):
    rows = []
    for l in zopen(zname, fname).decode("latin-1").splitlines():
        if l.strip():
            rows.append([p.strip().strip('"') for p in l.split(",")])
    return rows

def rd_ws(zname, fname):
    rows = []
    for l in zopen(zname, fname).decode("latin-1").splitlines():
        p = l.split()
        if len(p) >= 4:
            rows.append(p)
    return rows

def main():
    gdp, hist_comp = hist_anchors()
    ledger, rows, failures = [], [], []

    def add_row(yr, era, ident, pt, extra=None):
        comp_row, va_rows, fd_cols, gap, cshare, scale = ident
        row = {"year": yr, "era": era, **pt, "gdp_gap": gap,
               "comp_share_of_va": cshare, "scale": scale}
        if extra:
            row.update(extra)
        rows.append(row)

    # ---- square 85-order eras (industry×industry, published TR)
    SQ = {1947: ("47IOexcel.zip", "1947 Transactions 85-level Data.xls", {"r": 0, "c": 1, "flow": 2, "tr": 4}),
          1963: ("63IO85-levelexcel.zip", "1963 Transactions 85-level Data.xls", {"r": 0, "c": 1, "flow": 2, "tr": 3}),
          1967: ("67IO85-levelexcel.zip", "1967 Transactions 85-level Data.xls", {"r": 0, "c": 1, "flow": 2, "tr": 4})}
    for yr, (zn, fn, cmap) in SQ.items():
        try:
            df = parse_xls(zn, fn, cmap)
            M = long_to_mat(df, "r", "c", "flow")
            TR = long_to_mat(df.dropna(subset=["tr"]), "r", "c", "tr")
            TR = TR.loc[[i for i in TR.index if is_industry(i)],
                        [c for c in TR.columns if is_industry(c)]].fillna(0)
            ident = identify(M, gdp[str(yr)], ledger, str(yr))
            pt = point(M, TR, ident[0], ident[1], ident[2], ledger, str(yr))
            add_row(yr, "sq85", ident, pt)
        except Exception as e:
            failures.append((yr, f"{type(e).__name__}: {e}"))

    # 1958: transactions + separate TR workbook
    try:
        df = parse_xls("58IOexcel.zip", "1958 Transactions 85-level Data.xls", {"r": 0, "c": 1, "flow": 2})
        M = long_to_mat(df, "r", "c", "flow")
        tr = parse_xls("58IOTRexcel.zip", "1958 Total Requirements 85-level Data.xls", {"r": 0, "c": 1, "tr": 2})
        TR = long_to_mat(tr, "r", "c", "tr")
        TR = TR.loc[[i for i in TR.index if is_industry(i)],
                    [c for c in TR.columns if is_industry(c)]].fillna(0)
        ident = identify(M, gdp["1958"], ledger, "1958")
        pt = point(M, TR, ident[0], ident[1], ident[2], ledger, "1958")
        add_row(1958, "sq85", ident, pt)
    except Exception as e:
        failures.append((1958, f"{type(e).__name__}: {e}"))

    # ---- make-use 85-order: 1972, 1977 (published IxC TR in-file)
    MU = {1972: ("72IO85-levelexcel.zip", "1972 Transactions 85-level Data.xls", {"r": 0, "c": 1, "use": 2, "ictr": 5}),
          1977: ("77IO85-levelexcel.zip", "1977 Transactions 85-level Data.xls", {"r": 0, "c": 1, "use": 2, "ictr": 6})}
    for yr, (zn, fn, cmap) in MU.items():
        try:
            df = parse_xls(zn, fn, cmap)
            U = long_to_mat(df, "r", "c", "use")
            TR = long_to_mat(df.dropna(subset=["ictr"]), "r", "c", "ictr")
            TR = TR.loc[[i for i in TR.index if is_industry(i)],
                        [c for c in TR.columns if is_industry(c)]].fillna(0)
            ident = identify(U, gdp[str(yr)], ledger, str(yr))
            pt = point(U, TR, ident[0], ident[1], ident[2], ledger, str(yr))
            add_row(yr, "mu85", ident, pt)
        except Exception as e:
            failures.append((yr, f"{type(e).__name__}: {e}"))

    # ---- two-digit text vintages
    # 1992: comma files; published IxC TR; reconstruction check
    try:
        u = rd_csvish("ndn0180.zip", "IOUSE.TXT")
        use = pd.DataFrame({"r": [norm_code(x[0]) for x in u], "c": [norm_code(x[1]) for x in u],
                            "v": num([x[3] for x in u])})
        m = rd_csvish("ndn0180.zip", "IOMAKE.TXT")
        mk = pd.DataFrame({"r": [norm_code(x[0]) for x in m], "c": [norm_code(x[1]) for x in m],
                           "v": num([x[3] for x in m])})
        t = rd_csvish("ndn0180.zip", "IXCTR.TXT")
        trp = pd.DataFrame({"r": [norm_code(x[0]) for x in t], "c": [norm_code(x[1]) for x in t],
                            "v": num([x[3] for x in t])})
        U = long_to_mat(use, "r", "c", "v")
        V = long_to_mat(mk, "r", "c", "v")          # industries × commodities
        TRpub = long_to_mat(trp, "r", "c", "v").fillna(0)
        inds = [i for i in V.index if is_industry(i)]
        coms = [c for c in V.columns if is_industry(c)]
        q = V.loc[inds, coms].fillna(0).sum(axis=0)
        W = np.nan_to_num(V.loc[inds, coms].fillna(0).values / np.where(q.values[None, :] == 0, np.nan, q.values[None, :]))
        g = U[inds].fillna(0).sum(axis=0)
        Bc = U.reindex(index=coms)[inds].fillna(0).values / np.where(g.values[None, :] == 0, np.nan, g.values[None, :])
        Bc = np.nan_to_num(Bc)
        TRcon = pd.DataFrame(W @ np.linalg.inv(np.eye(len(coms)) - Bc @ W), index=inds, columns=coms)
        cr = [i for i in inds if i in TRpub.index]; cc = [c for c in coms if c in TRpub.columns]
        recon = float((TRcon.loc[cr, cc] - TRpub.loc[cr, cc]).abs().max().max())
        ident = identify(U, gdp["1992"], ledger, "1992")
        pt = point(U, TRpub.loc[cr, cc], ident[0], ident[1], ident[2], ledger, "1992")
        comp_total = float(U.loc[ident[0], [c for c in U.columns if is_industry(c)]].fillna(0).sum()) * ident[5] if ident[0] else np.nan
        extra = {"recon_err": recon}
        if "1992" in hist_comp and ident[0]:
            extra["hist_comp_dev"] = abs(comp_total - hist_comp["1992"]) / hist_comp["1992"]
        add_row(1992, "2dig", ident, pt, extra)
    except Exception as e:
        failures.append((1992, f"{type(e).__name__}: {e}"))

    # 1987: whitespace DAT files; TBL2 use, TBL1 make, TBL5 published IxC TR
    try:
        d2 = rd_ws("ndn0019.zip", "TBL2-87.DAT")
        use = pd.DataFrame({"r": [norm_code(x[0]) for x in d2], "c": [norm_code(x[1]) for x in d2],
                            "v": num([x[3] for x in d2])})
        d1 = rd_ws("ndn0019.zip", "TBL1-87.DAT")
        mk = pd.DataFrame({"r": [norm_code(x[0]) for x in d1], "c": [norm_code(x[1]) for x in d1],
                           "v": num([x[3] for x in d1])})
        d5 = rd_ws("ndn0019.zip", "TBL5-87.DAT")
        trp = pd.DataFrame({"r": [norm_code(x[0]) for x in d5], "c": [norm_code(x[1]) for x in d5],
                            "v": num([x[3] for x in d5])})
        U = long_to_mat(use, "r", "c", "v")
        V = long_to_mat(mk, "r", "c", "v")
        TRpub = long_to_mat(trp, "r", "c", "v").fillna(0)
        inds = [i for i in V.index if is_industry(i)]
        coms = [c for c in V.columns if is_industry(c)]
        q = V.loc[inds, coms].fillna(0).sum(axis=0)
        W = np.nan_to_num(V.loc[inds, coms].fillna(0).values / np.where(q.values[None, :] == 0, np.nan, q.values[None, :]))
        g = U[inds].fillna(0).sum(axis=0)
        Bc = np.nan_to_num(U.reindex(index=coms)[inds].fillna(0).values / np.where(g.values[None, :] == 0, np.nan, g.values[None, :]))
        TRcon = pd.DataFrame(W @ np.linalg.inv(np.eye(len(coms)) - Bc @ W), index=inds, columns=coms)
        cr = [i for i in inds if i in TRpub.index]; cc = [c for c in coms if c in TRpub.columns]
        recon = float((TRcon.loc[cr, cc] - TRpub.loc[cr, cc]).abs().max().max())
        ident = identify(U, gdp["1987"], ledger, "1987")
        pt = point(U, TRpub.loc[cr, cc], ident[0], ident[1], ident[2], ledger, "1987")
        extra = {"recon_err": recon}
        if "1987" in hist_comp and ident[0]:
            comp_total = float(U.loc[ident[0], [c for c in U.columns if is_industry(c)]].fillna(0).sum()) * ident[5]
            extra["hist_comp_dev"] = abs(comp_total - hist_comp["1987"]) / hist_comp["1987"]
        add_row(1987, "2dig", ident, pt, extra)
    except Exception as e:
        failures.append((1987, f"{type(e).__name__}: {e}"))

    # 1982: fixed-width multi-table lines; use = field C, IxC TR = last field ×1e-7
    try:
        lines = [l for l in zopen("ndn0125.zip", "82-2dall.txt").decode("latin-1").splitlines() if l.strip()]
        width = max(len(l) for l in lines)
        nf = (width - 4) // 10
        recs = []
        for l in lines:
            l = l.ljust(4 + 10 * nf)
            r, c = norm_code(l[0:2]), norm_code(l[2:4])
            vals = [l[4 + 10 * k: 14 + 10 * k].strip() for k in range(nf)]
            recs.append((r, c, vals[0], vals[-1]))
        df = pd.DataFrame(recs, columns=["r", "c", "use", "ictr"])
        df["use"] = num(df["use"]); df["ictr"] = num(df["ictr"]) / 1e7
        U = long_to_mat(df, "r", "c", "use")
        TRpub = long_to_mat(df.dropna(subset=["ictr"]), "r", "c", "ictr")
        TRpub = TRpub.loc[[i for i in TRpub.index if is_industry(i)],
                          [c for c in TRpub.columns if is_industry(c)]].fillna(0)
        ident = identify(U, gdp["1982"], ledger, "1982")
        pt = point(U, TRpub, ident[0], ident[1], ident[2], ledger, "1982")
        add_row(1982, "2dig", ident, pt)
    except Exception as e:
        failures.append((1982, f"{type(e).__name__}: {e}"))

    res = pd.DataFrame(rows).sort_values("year").set_index("year")
    print("=== build ledger ===")
    for e in ledger:
        print("  ", " | ".join(str(x) for x in e))
    if failures:
        print("\n=== failures (reported, not substituted) ===")
        for yr, msg in failures:
            print(f"  {yr}: {msg}")

    # ---- splice onto unit 2 (NAICS narrow, total-requirements)
    a = pd.read_csv(os.path.join(OUT, "lambda_us_family_a.csv")).set_index("year")
    if 1992 in res.index and pd.notna(res.loc[1992].get("lam", np.nan)) and res.loc[1992, "lam"] > 0:
        link = float(a.loc[1997, "lam_narrow_tot"]) / float(res.loc[1992, "lam"])
        res["lam_spliced"] = res["lam"] * link
        print(f"\nsplice link 1992→1997 (ratio): {link:.4f} "
              f"(SIC λ̂ 1992 {res.loc[1992, 'lam']:.4f} → NAICS 1997 {a.loc[1997, 'lam_narrow_tot']:.4f})")
    res.to_csv(os.path.join(OUT, "lambda_us_century.csv"))
    print("\n=== century points ===")
    show = [c for c in ("era", "lam", "lami", "res_va", "lam_spliced", "gdp_gap",
                        "comp_share_of_va", "recon_err", "hist_comp_dev", "n_set") if c in res.columns]
    print(res[show].round(4).to_string())

    # ---- figure
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(10, 5.5))
    lam_cols = [c for c in a.columns if c.startswith("lam_") and not c.endswith("domp")]
    ax.fill_between(a.index, a[lam_cols].min(axis=1), a[lam_cols].max(axis=1),
                    alpha=0.25, label="1997–2023 λ̂ band (unit 2 grid)")
    ax.plot(a.index, a[lam_cols].median(axis=1), lw=2)
    if "lam_spliced" in res.columns:
        s = res.dropna(subset=["lam_spliced"])
        ax.plot(s.index, s["lam_spliced"], "o--", lw=1.4,
                label="benchmark λ̂ (compensation), spliced at 1992→1997")
        ax.plot(s.index, s["lam"], "s", ms=4, alpha=0.5, label="benchmark λ̂, unspliced (SIC 43–58)")
    ax.set_ylabel("compensation share of $1 machinery final output")
    ax.set_title("λ̂_US, the century arc — benchmark points 1947–1992 + annual 1997–2023\n"
                 "tier: accounting · UNREAD (gate read = unit 6) · BEA: historical benchmarks "
                 "\"should not be used as a time series\" — shown as points, splice stated")
    ax.legend(loc="best", fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "lambda_us_century.png"), dpi=150)
    print("\nwrote data/lambda_us_century.csv and figures/lambda_us_century.png")

if __name__ == "__main__":
    main()
