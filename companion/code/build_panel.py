# build_panel.py — the companion's task panel (spec: companion_schedule_spec.md,
# next-units item 1). Builds two tables:
#
#   data/oews_occ1990dd_panel.csv    year x occ1990dd: employment + wage stats,
#                                    OEWS national files 1999-2025 mapped onto
#                                    the harmonized occ1990dd classification.
#   data/occ1990dd_attributes.csv    occ1990dd: Autor-Dorn DOT-1977 task
#                                    intensities (abstract/routine/manual),
#                                    offshorability, and O*NET 30.3 attachments
#                                    (task counts, mean importance).
#
# Mapping chains (Census/BLS official lists + ddorn.net crosswalks; every file
# fetched and validated by fetch.py, URLs probed live 2026-08-06):
#   1999-2011 OEWS (SOC-2000 era):  SOC -> Census2002 -> occ1990dd(occ2005 cw)
#   2012-2020 OEWS (SOC-2010 era):  SOC -> Census2010 -> occ1990dd(occ2010 cw)
#   2021-2025 OEWS (SOC-2018 era):  SOC -> SOC2010 -> Census2010 -> occ1990dd
# Each year runs its primary chain first, then retries unmapped codes on the
# other chains (the 2010-11 hybrid years and stray revisions self-heal); what
# remains unmapped is REPORTED as an employment share, never imputed.
# 1997-1998 (pre-SOC OES codes) are PARKED, not silently dropped: the deep-
# history unit will reach them alongside the Census 1950-1990 extension.
#
# Classification choice, labeled: a source code mapping to k>1 occ1990dd
# targets splits employment equally (SPLIT_EQUAL); wages ride each piece and
# aggregation re-weights by piece employment. Multiplicity stats go to the
# ledger; alternative splitting rules are a grid axis for later units.
# Wage top-codes ('#'/'*') coerce to NaN and are counted, never filled.
#
# The build BLOCKS (exit 1) rather than approximates: any fetch failure, any
# year mapping under MIN_COVERAGE of employment, or an attributes join under
# floor kills the run, per the data rule inherited from The Link.
import io
import os
import re
import sys
import zipfile

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fetch import fetch, CACHE  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data"))
os.makedirs(DATA, exist_ok=True)

YEARS = list(range(1999, 2026))
MIN_COVERAGE = 0.85          # mapped employment share, per year — else BLOCK
ATTR_FLOOR = 300             # occ1990dd rows carrying ALM measures — else BLOCK

SOC_RE = re.compile(r"^\d{2}-\d{4}$")
CEN_RE = re.compile(r"^\d{4}$")

ledger = []


def note(msg):
    ledger.append(msg)
    print(msg)


# ---------------------------------------------------------------- readers
def _zip_member(zpath, want):
    zf = zipfile.ZipFile(zpath)
    hits = [n for n in zf.namelist()
            if not n.endswith("/") and "__MACOSX" not in n
            and (os.path.basename(n).lower() == want.lower()
                 or (want not in {os.path.basename(m).lower() for m in zf.namelist()}
                     and want in os.path.basename(n).lower()))]
    if len(hits) != 1:
        raise RuntimeError(f"{zpath}: expected one '{want}' member, got {hits}")
    return zf.read(hits[0])


def read_dta(name, member):
    return pd.read_stata(io.BytesIO(_zip_member(fetch(name), member)))


def read_oews(year):
    """OEWS national detailed rows for one year -> harmonized frame."""
    name = (f"oes{year % 100:02d}nat.zip" if year <= 2002
            else f"oesm{year % 100:02d}nat.zip")
    xls = pd.ExcelFile(io.BytesIO(_zip_member(fetch(name), "national")))
    # locate the sheet and header row (1999-2000 hide the table behind a docs
    # sheet; 1999-2001 carry title blocks above the header)
    raw, hdr = None, None
    for sheet in xls.sheet_names:
        cand = pd.read_excel(xls, sheet_name=sheet, header=None)
        for i in range(min(40, len(cand))):
            row = cand.iloc[i].astype(str).str.strip().str.lower()
            if (row == "occ_code").any():
                raw, hdr = cand, i
                break
        if hdr is not None:
            break
    if hdr is None:
        raise RuntimeError(f"{name}: no occ_code header found on any sheet")
    df = raw.iloc[hdr + 1:].copy()
    df.columns = raw.iloc[hdr].astype(str).str.strip().str.lower()
    df = df.rename(columns={"occ_titl": "occ_title", "group": "o_group",
                            "occ_group": "o_group", "h_wpct50": "h_median",
                            "a_wpct50": "a_median"})
    # 2019+ long-format files: keep the national cross-industry all-ownership
    # block (own_code 1235); cells arrive as objects, so compare as strings
    if "i_group" in df.columns:
        df = df[df["i_group"].astype(str).str.strip() == "cross-industry"]
    if "own_code" in df.columns:
        df = df[df["own_code"].astype(str).str.strip() == "1235"]
        if not len(df):
            raise RuntimeError(f"{name}: no all-ownership (1235) block")
    # the file's own all-occupations total is the honest coverage denominator;
    # 1999-2000 files carry no 00-0000 row, so fall back to the sum of major
    # rows (majors partition employment), then to the detailed sum
    codes = df["occ_code"].astype(str).str.strip()
    emp_num = pd.to_numeric(df["tot_emp"].astype(str).str.replace(",", ""),
                            errors="coerce")
    if (codes == "00-0000").any():
        total_all = float(emp_num[codes == "00-0000"].iloc[0])
    else:
        majors = emp_num[(codes != "00-0000") & codes.str.endswith("-0000")]
        total_all = float(majors.sum()) if len(majors) else float("nan")
    # aggregation levels: modern files label rows (keep 'detailed' only);
    # 1999-2003-era files label ONLY majors/totals and leave detail blank
    if "o_group" in df.columns:
        labels = set(df["o_group"].dropna().astype(str).str.strip().unique())
        if "detailed" in labels:
            df = df[df["o_group"].astype(str).str.strip() == "detailed"]
        else:
            df = df[df["o_group"].isna()
                    | (df["o_group"].astype(str).str.strip() == "")]
    keep = [c for c in ["occ_code", "occ_title", "tot_emp", "h_mean", "a_mean",
                        "h_median", "a_median"] if c in df.columns]
    df = df[keep]
    df = df[df["occ_code"].astype(str).str.match(SOC_RE.pattern, na=False)]
    df = df[~df["occ_code"].astype(str).str.endswith("-0000")]  # majors/total out
    for c in df.columns.drop(["occ_code", "occ_title"]):
        as_str = df[c].astype(str).str.strip()
        df[f"_top_{c}"] = as_str.isin(["#", "*", "**"])
        df[c] = pd.to_numeric(as_str.str.replace(",", ""), errors="coerce")
    df = df.dropna(subset=["tot_emp"])
    dup = df["occ_code"].duplicated()
    if dup.any():
        raise RuntimeError(f"{name}: duplicate detailed occ codes {df[dup]['occ_code'].tolist()[:5]}")
    top = int(df[[c for c in df.columns if c.startswith("_top_")]].sum().sum())
    note(f"oews {year}: {len(df)} detailed rows summing {df['tot_emp'].sum():,.0f} "
         f"of all-occ {total_all:,.0f}, top-coded cells {top}")
    return df.drop(columns=[c for c in df.columns if c.startswith("_top_")]), total_all


def _header_scan(path_or_bytes, sheet, marker):
    raw = pd.read_excel(path_or_bytes, sheet_name=sheet, header=None)
    for i in range(min(40, len(raw))):
        if raw.iloc[i].astype(str).str.strip().str.contains(marker, case=False,
                                                            regex=False).any():
            return raw, i
    raise RuntimeError(f"marker '{marker}' not found in sheet {sheet}")


WILD_RE = re.compile(r"\d{2}-(?:\d{3}X|\d{2}XX|\dXXX)")


def census_soc_pairs(fname, sheet, cen_col_marker):
    """Detail rows of a Census occupation code list -> exact (census4, soc)
    pairs plus wildcard (census4, soc-prefix) pairs. The lists write combined
    SOC detail as X-wildcards ('37-201X' = janitors 37-2011/2012, '15-10XX');
    those become prefix entries matched at lookup time."""
    raw, hdr = _header_scan(fetch(fname), sheet, cen_col_marker)
    cen_col = [j for j in range(raw.shape[1])
               if str(raw.iloc[hdr, j]).strip().lower() == cen_col_marker.lower()][0]
    soc_col = cen_col + 1                      # SOC sits beside the census code
    pairs, prefixes = [], []
    for i in range(hdr + 1, len(raw)):
        cen = str(raw.iloc[i, cen_col]).strip()
        if not CEN_RE.match(cen):
            continue                            # group/range/blank rows
        cell = str(raw.iloc[i, soc_col])
        for soc in re.findall(r"\d{2}-\d{4}", cell):
            pairs.append((cen, soc))
        for wild in WILD_RE.findall(cell):
            prefixes.append((cen, wild.rstrip("X")))
    return (pd.DataFrame(pairs, columns=["census", "soc"]).drop_duplicates(),
            pd.DataFrame(prefixes, columns=["census", "prefix"]).drop_duplicates())


def soc_revision_map(fname, sheet, from_marker, to_marker):
    raw, hdr = _header_scan(fetch(fname), sheet, from_marker)
    cols = {str(raw.iloc[hdr, j]).strip().lower(): j for j in range(raw.shape[1])}
    f_col, t_col = cols[from_marker.lower()], cols[to_marker.lower()]
    out = {}
    for i in range(hdr + 1, len(raw)):
        f, t = str(raw.iloc[i, f_col]).strip(), str(raw.iloc[i, t_col]).strip()
        if SOC_RE.match(f) and SOC_RE.match(t):
            out.setdefault(f, set()).add(t)
    return {k: sorted(v) for k, v in out.items()}


# ---------------------------------------------------------------- chains
def build_chains():
    dd05 = read_dta("occ2005_occ1990dd.zip", "occ2005_occ1990dd.dta")
    dd05 = dd05.dropna().astype({"occ": int, "occ1990dd": int})
    cen2005_dd = {}                                  # census 2002 4-digit -> [dd]
    for occ, dd in dd05.itertuples(index=False):
        cen2005_dd.setdefault(f"{occ * 10:04d}", []).append(dd)

    dd10 = read_dta("occ2010_occ1990dd.zip", "occ2010_occ1990dd.dta")
    dd10 = dd10.dropna()
    cen2010_dd = {}
    for occ, dd in dd10.itertuples(index=False):
        cen2010_dd.setdefault(f"{int(str(occ).strip() or 0):04d}", []).append(int(dd))

    cs02, cs02p = census_soc_pairs("2002-census-occupation-codes.xls",
                                   "Occ Codes", "2002 Census Code")
    cs10, cs10p = census_soc_pairs("2010-occ-codes-with-crosswalk-from-2002-2011.xls",
                                   "2010OccCodeList", "2010 Census Code")
    note(f"census lists: 2002 has {len(cs02)} exact + {len(cs02p)} wildcard "
         f"pairs, 2010 has {len(cs10)} + {len(cs10p)}")

    def invert(pairs, prefpairs, cen_dd):
        """-> (soc -> [dd], soc-prefix -> [dd]), both via census codes."""
        m, p = {}, {}
        for cen, soc in pairs.itertuples(index=False):
            for dd in cen_dd.get(cen, []):
                m.setdefault(soc, set()).add(dd)
        for cen, pref in prefpairs.itertuples(index=False):
            for dd in cen_dd.get(cen, []):
                p.setdefault(pref, set()).add(dd)
        return ({k: sorted(v) for k, v in m.items()},
                {k: sorted(v) for k, v in p.items()})

    soc00_dd = invert(cs02, cs02p, cen2005_dd)
    soc10_dd = invert(cs10, cs10p, cen2010_dd)

    s18_s10 = soc_revision_map("soc_2010_to_2018_crosswalk.xlsx", 0,
                               "2018 SOC Code", "2010 SOC Code")
    # compose 2018 -> 2010 -> dd through the full 2010 lookup (exact + prefix)
    soc18_exact = {}
    for s18, s10s in s18_s10.items():
        tgt = set()
        for s10 in s10s:
            dds, _ = lookup(s10, soc10_dd)
            tgt.update(dds or [])
        if tgt:
            soc18_exact[s18] = sorted(tgt)
    soc18_dd = (soc18_exact, {})
    note(f"soc->occ1990dd map sizes: soc2000 {len(soc00_dd[0])}+{len(soc00_dd[1])}p, "
         f"soc2010 {len(soc10_dd[0])}+{len(soc10_dd[1])}p, soc2018 {len(soc18_exact)}")
    return soc00_dd, soc10_dd, soc18_dd


def chain_order(year):
    if year <= 2011:
        return ["soc00", "soc10", "soc18"]
    if year <= 2020:
        return ["soc10", "soc18", "soc00"]
    return ["soc18", "soc10", "soc00"]


def lookup(code, maps):
    """soc -> [occ1990dd] with a SOC hierarchy walk: exact, then the census
    lists' X-wildcard prefixes (longest first), then the parent broad code
    (last digit zeroed), then the union of the broad code's children. OEWS
    reports at whichever level survives suppression, and the census lists
    aggregate to broad where SOC detail is too fine; the walk meets both
    without leaving the official code tree. Returns (dds, how)."""
    m, pref = maps
    hits = m.get(code)
    if hits:
        return hits, "exact"
    for cut in range(len(code) - 1, 3, -1):
        if code[:cut] in pref:
            return pref[code[:cut]], "wildcard"
    parent = code[:-1] + "0"
    if parent != code and m.get(parent):
        return m[parent], "parent"
    if code.endswith("0"):
        union = sorted({dd for i in range(1, 10)
                        for dd in m.get(code[:-1] + str(i), [])})
        if union:
            return union, "children"
    return None, None


# ---------------------------------------------------------------- panel
def build_panel(chains):
    soc_maps = dict(zip(["soc00", "soc10", "soc18"], chains))
    rows, coverage = [], []
    for year in YEARS:
        df, total_all = read_oews(year)
        mapped_emp = 0.0
        split_stats, walk_emp, unmapped = [], 0.0, []
        for r in df.itertuples(index=False):
            dds, how = None, None
            for key in chain_order(year):
                dds, how = lookup(r.occ_code, soc_maps[key])
                if dds:
                    break
            if not dds:
                unmapped.append((r.occ_code, r.tot_emp))
                continue
            mapped_emp += r.tot_emp
            if how != "exact":
                walk_emp += r.tot_emp
            split_stats.append(len(dds))
            for dd in dds:                            # SPLIT_EQUAL
                rows.append({"year": year, "occ1990dd": dd,
                             "emp": r.tot_emp / len(dds),
                             "occ_title": str(r.occ_title),
                             "h_mean": getattr(r, "h_mean", np.nan),
                             "a_mean": getattr(r, "a_mean", np.nan),
                             "h_median": getattr(r, "h_median", np.nan),
                             "a_median": getattr(r, "a_median", np.nan)})
        share = mapped_emp / total_all                # vs the file's own total
        multi = np.mean([s > 1 for s in split_stats]) if split_stats else np.nan
        coverage.append({"year": year, "coverage": share,
                         "share_split_codes": multi,
                         "share_via_walk": walk_emp / total_all})
        top_un = sorted(unmapped, key=lambda t: -t[1])[:3]
        note(f"map {year}: coverage {share:.3f} of all-occ employment "
             f"({walk_emp / total_all:.3f} via hierarchy walk), "
             f"{multi:.2%} of mapped codes split; top unmapped: "
             + (", ".join(f"{c} ({e:,.0f})" for c, e in top_un) or "none"))
    cov = pd.DataFrame(coverage).set_index("year")
    bad = cov[cov["coverage"] < MIN_COVERAGE]
    if len(bad):
        note(f"BLOCKED: coverage below {MIN_COVERAGE} in years "
             f"{bad.index.tolist()} — stopping rather than approximating.")
        raise SystemExit(1)

    pieces = pd.DataFrame(rows)
    def wavg(g, col):
        v, w = g[col], g["emp"]
        m = v.notna() & w.notna()
        return np.average(v[m], weights=w[m]) if m.any() and w[m].sum() > 0 else np.nan
    panel = (pieces.groupby(["year", "occ1990dd"])
             .apply(lambda g: pd.Series({
                 "emp": g["emp"].sum(),
                 "h_mean": wavg(g, "h_mean"), "a_mean": wavg(g, "a_mean"),
                 "h_median": wavg(g, "h_median"), "a_median": wavg(g, "a_median"),
                 "n_source_codes": len(g),
                 # derived convenience label: the biggest source code's title
                 "top_source_title": g.loc[g["emp"].idxmax(), "occ_title"]}),
                    include_groups=False)
             .reset_index())
    return panel, cov


# ---------------------------------------------------------------- attributes
def build_attributes(chains):
    alm = read_dta("occ1990dd_task_alm.zip", "occ1990dd_task_alm.dta")
    off = read_dta("occ1990dd_task_offshore.zip", "occ1990dd_task_offshore.dta")
    off["occ1990dd"] = off["occ1990dd"].astype(int)
    attrs = alm.merge(off, on="occ1990dd", how="outer")

    zf = zipfile.ZipFile(fetch("db_30_3_text.zip"))
    stmts = pd.read_csv(io.BytesIO(zf.read("db_30_3_text/Task Statements.txt")), sep="\t")
    ratings = pd.read_csv(io.BytesIO(zf.read("db_30_3_text/Task Ratings.txt")), sep="\t")
    stmts["soc6"] = stmts["O*NET-SOC Code"].str[:7]
    ratings["soc6"] = ratings["O*NET-SOC Code"].str[:7]
    per_soc = stmts.groupby("soc6").agg(
        onet_n_tasks=("Task ID", "nunique"),
        onet_n_core=("Task Type", lambda s: (s == "Core").sum())).reset_index()
    im = (ratings[ratings["Scale ID"] == "IM"]
          .groupby("soc6")["Data Value"].mean().rename("onet_im_mean").reset_index())
    per_soc = per_soc.merge(im, on="soc6", how="left")

    soc18_dd = chains[2]
    onet_rows = []
    for r in per_soc.itertuples(index=False):
        dds, _ = lookup(r.soc6, soc18_dd)
        for dd in dds or []:
            onet_rows.append({"occ1990dd": dd, "onet_n_tasks": r.onet_n_tasks,
                              "onet_n_core": r.onet_n_core,
                              "onet_im_mean": r.onet_im_mean})
    onet_dd = (pd.DataFrame(onet_rows).groupby("occ1990dd").mean().reset_index())
    attrs = attrs.merge(onet_dd, on="occ1990dd", how="left")
    n_alm = attrs["task_routine"].notna().sum()
    n_onet = attrs["onet_n_tasks"].notna().sum()
    note(f"attributes: {len(attrs)} occ1990dd rows, {n_alm} with ALM tasks, "
         f"{n_onet} with O*NET attachments")
    if n_alm < ATTR_FLOOR:
        note(f"BLOCKED: ALM attribute rows {n_alm} < floor {ATTR_FLOOR}.")
        raise SystemExit(1)
    return attrs


# ---------------------------------------------------------------- run
if __name__ == "__main__":
    note("=== companion panel build, sources per fetch.py manifest ===")
    chains = build_chains()
    panel, cov = build_panel(chains)
    attrs = build_attributes(chains)
    latest = panel[panel["year"] == panel["year"].max()]
    attrs = attrs.merge(latest[["occ1990dd", "top_source_title"]]
                        .rename(columns={"top_source_title": "label_latest"}),
                        on="occ1990dd", how="left")

    panel.to_csv(os.path.join(DATA, "oews_occ1990dd_panel.csv"), index=False)
    attrs.to_csv(os.path.join(DATA, "occ1990dd_attributes.csv"), index=False)
    cov.to_csv(os.path.join(DATA, "panel_coverage.csv"))
    with open(os.path.join(DATA, "build_ledger.txt"), "w", encoding="utf8") as fh:
        fh.write("\n".join(ledger) + "\n")

    note(f"panel: {len(panel)} year x occ1990dd rows over {panel['year'].nunique()} years, "
         f"{panel['occ1990dd'].nunique()} occupations")
    tel = panel[panel["occ1990dd"] == 348].set_index("year")
    if len(tel):
        note("worked-instance glance — telephone operators (occ1990dd 348) employment: "
             + ", ".join(f"{y}: {tel.loc[y, 'emp']:,.0f}"
                         for y in [1999, 2005, 2010, 2015, 2020, 2025] if y in tel.index))
    note("wrote data/oews_occ1990dd_panel.csv, data/occ1990dd_attributes.csv, "
         "data/panel_coverage.csv, data/build_ledger.txt")
