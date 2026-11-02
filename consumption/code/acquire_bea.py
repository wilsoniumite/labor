# acquire_bea.py — vendor BEA national accounts (PCE by type of product incl. underlying detail, monthly and
# annual; personal income and its disposition) and BEA's distributional statistics (distribution of personal
# income with the 2025 nowcast, income-stratified PCE price index, joint DPI/PCE distribution); then build tidy
# long files from the raw files only, with every cross-check written to tidy/bea_checks.csv.
#
# Run from the repo root:  venv/bin/python -I consumption/code/acquire_bea.py
#   --offline       never touch the network (build from what is vendored)
#   --retry-failed  retry downloads recorded in raw/bea/FETCH_FAILURES.csv (default: a recorded failure is not
#                   retried, per the stop-and-report rule)
# Downloads skip files already vendored, so a rerun is offline and rebuilds every tidy file from raw.
# Plain functions and top-level code (notebook-cell friendly). No modelling here.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import fetch, manifest_row, sha256_of, RAW, TIDY

import csv
import datetime as dt
import re
import zipfile

import numpy as np
import openpyxl
import pandas as pd
import pdfplumber
from bs4 import BeautifulSoup
from tqdm.auto import tqdm

SRC = "bea"
RAWB = RAW / SRC
TIDY.mkdir(parents=True, exist_ok=True)
OFFLINE = "--offline" in sys.argv
RETRY_FAILED = "--retry-failed" in sys.argv

# ---------------------------------------------------------------------------------------------------------
# 1. Download list. (rel_file, url, what_it_is, used_for)
# ---------------------------------------------------------------------------------------------------------
APPS = "https://apps.bea.gov"
WWW = "https://www.bea.gov"
DPI_NAT = APPS + "/data/special-topics/distribution-of-personal-income/national"
DPI_ISP = APPS + "/data/special-topics/distribution-of-personal-income/ispcepx"

DOWNLOADS = [
    # --- NIPA flat files (route a): every published and underlying-detail NIPA series, A/Q/M --------------
    ("nipa/FlatFiles.zip", APPS + "/national/Release/TXT/FlatFiles.zip",
     "BEA NIPA flat files (zip of nipadataA.txt, nipadataQ.txt, nipadataM.txt, SeriesRegister.txt, "
     "TablesRegister.txt; same files as posted individually under /national/Release/TXT/), release of "
     "2026-10-29 (Personal Income and Outlays, September 2026; GDP 2026Q3 advance)",
     "values of bea_pce_u_long, bea_pce_major_long, bea_pi_long (series codes, A and M data); register "
     "parents check the hierarchy; Table 2.10 decile shares cross-check"),
    # --- NIPA workbooks (route b): table layout (line order, indentation, labels) and release stamps -------
    ("nipa/xls_underlying/Section2All_xls.xlsx", APPS + "/national/Release/XLS/Underlying/Section2All_xls.xlsx",
     "BEA NIPA underlying-detail workbook, Section 2 (Tables 2.3.4U-2.3.6U, 2.4.3U-2.4.6U; annual, "
     "quarterly and monthly sheets), release of 2026-10-29",
     "bea_pce_u_long / bea_pce_u_lines: line layout, indentation (level), labels, release stamps; "
     "cell-by-cell cross-check of flat-file values"),
    ("nipa/xls_survey/Section2All_xls.xlsx", APPS + "/national/Release/XLS/Survey/Section2All_xls.xlsx",
     "BEA NIPA published-tables workbook, Section 2 (Tables 2.1-2.10 incl. 2.3.x, 2.6, 2.8.x; annual, "
     "quarterly and monthly sheets), release of 2026-10-29",
     "bea_pi_long and bea_pce_major_long: line layout, indentation, labels, release stamps; cell-by-cell "
     "cross-check of flat-file values; Table 2.10"),
    # --- PCE methodology: NIPA Handbook chapter 5 (definitions, imputations, NPISHs, quality of the detail) -
    ("nipa/nipa-handbook-chapter-05.pdf", WWW + "/resources/methodologies/nipa-handbook/pdf/chapter-05.pdf",
     "BEA NIPA Handbook, Chapter 5: Personal Consumption Expenditures (updated December 2024)",
     "definitions and the quality caveat on underlying detail (README_bea.md)"),
    ("nipa/faq-84-pce-detail-beyond-2-4-5U.html", WWW + "/help/faq/84",
     "BEA FAQ 84: 'Are more detailed estimates available for PCE beyond what is presented in the underlying "
     "detail Table 2.4.5U?' (HTML as of the pull date)", "README_bea.md (scope of the U detail)"),
    # --- the September 2026 Personal Income and Outlays release: headline numbers for cross-checks --------
    ("release/pi0926.pdf", WWW + "/sites/default/files/2026-10/pi0926.pdf",
     "BEA news release 'Personal Income and Outlays, September 2026' (BEA 26-46, 2026-10-29), full PDF "
     "with release tables", "headline cross-checks (bea_checks.csv)"),
    ("release/personal-income-and-outlays-september-2026.html",
     WWW + "/news/2026/personal-income-and-outlays-september-2026",
     "BEA news release 'Personal Income and Outlays, September 2026', HTML page as of the pull date",
     "headline cross-checks (README_bea.md)"),
    # --- distribution of personal income (national), June 2026 release ------------------------------------
    ("distribution/national/summary-file.csv", DPI_NAT + "/summary-file.csv",
     "BEA distribution of personal income, national summary file: all available years and metrics "
     "(2000-2023 final, 2024 provisional), release of 2026-06-16", "bea_dpi_distribution.csv"),
    ("distribution/national/distribution-of-personal-income-inequality-metrics-summary-2023.xlsx",
     DPI_NAT + "/distribution-of-personal-income-inequality-metrics-summary-2023.xlsx",
     "BEA distribution of personal income: inequality-metrics summary workbook, data for 2023",
     "cross-check of bea_dpi_distribution.csv"),
    ("distribution/national/distribution-of-personal-income-inequality-metrics-summary-2024.xlsx",
     DPI_NAT + "/distribution-of-personal-income-inequality-metrics-summary-2024.xlsx",
     "BEA distribution of personal income: inequality-metrics summary workbook, provisional data for 2024",
     "cross-check of bea_dpi_distribution.csv; 2024 top-share interval ranges"),
    ("distribution/national/technical-document.pdf", DPI_NAT + "/technical-document.pdf",
     "BEA technical document: An Updated Methodology for Distributing Personal Income",
     "definitions (README_bea.md)"),
    ("distribution/national/readme-for-summary-file.pdf", DPI_NAT + "/readme-for-summary-file.pdf",
     "BEA read-me for the national summary file (variable definitions)", "definitions (README_bea.md)"),
    ("distribution/national/summary-methodological-update.pdf", DPI_NAT + "/summary-methodological-update.pdf",
     "BEA summary of methodological updates, distribution of personal income (June 2026 release)",
     "definitions and revisions (README_bea.md)"),
    ("distribution/distribution-of-personal-income.html",
     WWW + "/data/special-topics/distribution-of-personal-income",
     "BEA 'Distribution of Personal Income' special-topics page as of the pull date; carries the "
     "experimental 2025 nowcast table (quintile shares 2024 published / 2025 nowcast, 2025 nominal growth)",
     "bea_dpi_distribution.csv (2025 nowcast rows); file links and release notes"),
    ("distribution/blog_2026-06-16_innovations-distribution-income-statistics.html",
     WWW + "/news/blog/2026-06-16/innovations-distribution-income-statistics-new-data-and-new-tool",
     "BEA blog 2026-06-16 'Innovations in Distribution of Income Statistics: New Data and a New Tool'",
     "release context (README_bea.md)"),
    # --- income-stratified PCE price index (ISPCEPX), June 2026 -------------------------------------------
    ("distribution/ispcepx/ispecpx_table.xlsx", DPI_ISP + "/ispecpx_table.xlsx",
     "BEA income-stratified PCE price index (ISPCEPX) by income decile, workbook (file name as published)",
     "bea_pce_price_by_income_decile.csv"),
    ("distribution/ispcepx/readme_ISPCEPX.pdf", DPI_ISP + "/readme_ISPCEPX.pdf",
     "BEA read-me / method note for the income-stratified PCE price index", "definitions (README_bea.md)"),
    ("distribution/ispcepx/BEA-WP2025-9.pdf", "https://www.bea.gov/system/files/papers/BEA-WP2025-9.pdf",
     "BEA Working Paper 2025-9, Gindelsky and Martin, 'Rethinking Inflation Heterogeneity: Evidence From "
     "National Accounts' (the ISPCEPX method paper)", "method reference (README_bea.md)"),
    # --- joint distribution of DPI and PCE (distribution of personal saving), BEA-BLS ---------------------
    ("distribution/joint_dpi_pce/joint_dist_summary.xlsx", WWW + "/sites/default/files/2026-05/joint_dist_summary.xlsx",
     "BEA distribution of personal saving based on a joint distribution of DPI and PCE: summary workbook, "
     "all available years and metrics (page text says 2004-2023; the workbook holds 2000-2023)",
     "bea_joint_dpi_pce_by_decile.csv, bea_joint_dpi_pce_joint_shares.csv"),
    ("distribution/joint_dpi_pce/technical_document_personal_saving.pdf",
     WWW + "/sites/default/files/2026-04/technical_document_personal_saving.pdf",
     "BEA technical document: The Methodology for Distributing Personal Saving via a Joint Distribution of "
     "DPI and PCE", "definitions (README_bea.md)"),
    ("distribution/joint_dpi_pce/readme_for_summary_file.pdf",
     WWW + "/sites/default/files/2026-04/readme_for_summary_file.pdf",
     "BEA read-me for the joint DPI/PCE (personal saving) summary file", "definitions (README_bea.md)"),
    # --- FRED cross-check of real personal income excluding current transfer receipts ---------------------
    ("fred/W875RX1.csv", "https://fred.stlouisfed.org/graph/fredgraph.csv?id=W875RX1",
     "FRED series W875RX1, real personal income excluding current transfer receipts (billions of chained "
     "2017 dollars, SAAR), CSV from fredgraph.csv",
     "cross-check of bea_pi_long.csv (Table 2.6 line 36, W875RX)"),
]

# ---------------------------------------------------------------------------------------------------------
# 2. Download (skip vendored files; a failure is recorded and not retried unless --retry-failed)
# ---------------------------------------------------------------------------------------------------------
FAIL_PATH = RAWB / "FETCH_FAILURES.csv"
FAIL_COLS = ["file", "url", "date_tried", "error"]


def read_failures():
    if not FAIL_PATH.exists():
        return {}
    with open(FAIL_PATH, newline="", encoding="utf-8") as fh:
        return {r["file"]: r for r in csv.DictReader(fh)}


def write_failures(fails):
    if not fails:
        if FAIL_PATH.exists():
            FAIL_PATH.unlink()
        return
    with open(FAIL_PATH, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FAIL_COLS)
        w.writeheader()
        w.writerows(sorted(fails.values(), key=lambda r: r["file"]))


def fetch_all(downloads):
    fails = read_failures()
    for rel, url, what, used in tqdm(downloads, desc="BEA downloads"):
        if (RAWB / rel).exists():
            fails.pop(rel, None)
            continue
        if OFFLINE:
            print("  offline, not vendored:", rel)
            continue
        if rel in fails and not RETRY_FAILED:
            print("  not retried (recorded failure; use --retry-failed):", rel, "|", fails[rel]["error"][:200])
            continue
        try:
            fetch(SRC, rel, url, what, used)
            fails.pop(rel, None)
        except Exception as e:
            print("  FAILED:", rel, url, repr(e))
            fails[rel] = {"file": rel, "url": url, "date_tried": dt.date.today().isoformat(), "error": repr(e)}
    write_failures(fails)
    return fails


def sync_manifest(downloads):
    """Keep MANIFEST.csv descriptions in step with DOWNLOADS (date_pulled and hashes come from the file)."""
    mpath = RAWB / "MANIFEST.csv"
    if not mpath.exists():
        return
    with open(mpath, newline="", encoding="utf-8") as fh:
        rows = {r["file"]: r for r in csv.DictReader(fh)}
    for rel, url, what, used in downloads:
        r = rows.get(rel)
        if r and (r["what_it_is"] != what or r["used_for"] != used or r["url"] != url):
            manifest_row(SRC, rel, url, what, used, date_pulled=r["date_pulled"])


FAILS = fetch_all(DOWNLOADS)
sync_manifest(DOWNLOADS)

# ---------------------------------------------------------------------------------------------------------
# 3. Helpers: checks log, flat files, workbook sheets, labels and hierarchy
# ---------------------------------------------------------------------------------------------------------
CHECKS = []


def check(name, ok, value="", detail=""):
    """Record one cross-check. ok: True/False, or None for an informational line."""
    status = "info" if ok is None else ("pass" if ok else "FAIL")
    CHECKS.append({"check": name, "status": status, "value": str(value), "detail": detail})
    print(f"  [{status}] {name}: {value}  {detail}")


FLAT = RAWB / "nipa" / "FlatFiles.zip"
XLS_U = RAWB / "nipa" / "xls_underlying" / "Section2All_xls.xlsx"
XLS_S = RAWB / "nipa" / "xls_survey" / "Section2All_xls.xlsx"


def read_flat_data(member):
    """nipadataA/M.txt: SeriesCode, Period (1959 or 1959M01), Value (thousands separators) -> float."""
    with zipfile.ZipFile(FLAT) as z, z.open(member) as fh:
        df = pd.read_csv(fh, dtype=str, keep_default_na=False)
    df.columns = ["series_code", "period", "value"]
    df["value"] = pd.to_numeric(df["value"].str.replace(",", "", regex=False), errors="raise")
    return df


def read_flat_register():
    with zipfile.ZipFile(FLAT) as z, z.open("SeriesRegister.txt") as fh:
        reg = pd.read_csv(fh, dtype=str, keep_default_na=False)
    reg.columns = ["series_code", "series_label", "metric", "calc_type", "default_scale", "table_lines", "parents"]
    return reg


def read_flat_tables():
    with zipfile.ZipFile(FLAT) as z, z.open("TablesRegister.txt") as fh:
        return pd.read_csv(fh, dtype=str, keep_default_na=False)


def read_sheet(wb, sheet):
    """One BEA table sheet -> (meta, periods, layout rows, numeric cells, footnotes).
    Layout rows keep the raw label (leading spaces = indentation) and the section it sits in: 'main' until the
    first unnumbered header row ('Addenda:', 'Additional aggregates:'), 'addenda' after it."""
    rows = list(wb[sheet].iter_rows(values_only=True))
    meta = {"sheet": sheet, "title": rows[0][0]}
    for r in rows[:8]:
        v = r[0]
        if isinstance(v, str):
            if v.startswith("["):
                meta["unit_note"] = v
            elif v.startswith(("Annual data", "Monthly data", "Quarterly data")):
                meta["coverage"] = v
            elif v.startswith("Data published"):
                meta["published"] = v
            elif v.startswith("File created"):
                meta["file_created"] = " ".join(v.split())
    hi = next(i for i, r in enumerate(rows) if r[0] == "Line")
    periods = [p for p in rows[hi][3:] if p is not None]
    lay, cells, notes, headers, section = [], [], [], [], "main"
    for r in rows[hi + 1:]:
        if r[0] is not None and str(r[0]).strip().isdigit():
            ln = int(r[0])
            d = indent_of(r[1])[0]
            lay.append({"line": ln, "label_raw": r[1], "series_code": r[2], "section": section,
                        "context": " ".join(t for k, t in headers if k < d)})
            for p, v in zip(periods, r[3:3 + len(periods)]):
                if isinstance(v, (int, float)) and not isinstance(v, bool):
                    cells.append((ln, p, float(v)))
                elif v not in (".....", None):
                    raise ValueError(f"{sheet} line {ln} {p}: unexpected cell {v!r}")
        elif r[0] is None and isinstance(r[1], str) and r[1].strip():
            section = "addenda"          # unnumbered header rows: 'Addenda:', 'Additional aggregates:', 'Per capita:'
            d = indent_of(r[1])[0]
            headers = [(k, t) for k, t in headers if k < d] + [(d, r[1].strip())]
        elif isinstance(r[0], str) and r[0].strip():
            notes.append(r[0].strip())
    return (meta, periods, pd.DataFrame(lay), pd.DataFrame(cells, columns=["line", "period", "value_xls"]), notes)


FOOT = re.compile(r"\\\d+\\")                       # footnote markers such as \1\ in BEA labels
XREF = re.compile(r"\s*\(((?:parts? of )?\d+(?:(?:,? and |, )(?:parts? of )?\d+)*)\)\s*$")  # '(55)', '(parts of 31 and 32)'


def clean_label(raw):
    return FOOT.sub("", raw).strip()


def indent_of(raw):
    n = len(raw) - len(raw.lstrip(" "))
    return n // 2, n % 2


def period_to_date(p):
    p = str(p)
    return p[:4] + "-" + p[5:7] if "M" in p else p


def add_hierarchy(lay, reg, pce_root):
    """level = display indent depth; parent_line = nearest earlier line one level up (main section only, and
    only when parent and child are the same kind of quantity); sign = -1 for 'Less:' lines."""
    lay = lay.sort_values("line").reset_index(drop=True)
    odd = []
    lev = []
    for ln, raw in zip(lay["line"], lay["label_raw"]):
        d, r = indent_of(raw)
        if r:
            odd.append(ln)
        if pce_root:   # PCE tables print line 1 indented (4-6 spaces) above Goods/Services at indent 0
            lev.append(0 if ln == 1 else d + 1)
        else:
            lev.append(d)
    lay["level"] = lev
    lay["label"] = [clean_label(x) for x in lay["label_raw"]]
    lay["sign"] = [-1 if x.startswith("Less:") else 1 for x in lay["label"]]
    lay.loc[lay["label"] == "Residual", "section"] = "residual"
    kind = reg.set_index("series_code")[["metric", "calc_type"]].apply(tuple, axis=1).to_dict()
    parents, stack = [], {}
    for ln, lv, sec, code in zip(lay["line"], lay["level"], lay["section"], lay["series_code"]):
        p = pd.NA
        if sec == "main":
            if lv > 0 and (lv - 1) in stack:
                cand = stack[lv - 1]
                if kind.get(code) == kind.get(cand[1]) or code not in kind or cand[1] not in kind:
                    p = cand[0]
            stack[lv] = (ln, code)
            for k in [k for k in stack if k > lv]:
                del stack[k]
        parents.append(p)
    lay["parent_line"] = pd.array(parents, dtype="Int64")
    return lay, odd


def table_values(lay, flat, periods):
    """Values for every line from the flat file (by series code), restricted to the periods the sheet shows."""
    codes = lay.loc[lay["series_code"].ne("ZZZZZZ"), ["line", "series_code"]]
    f = flat[flat["series_code"].isin(set(codes["series_code"])) & flat["period"].isin(set(periods))]
    return codes.merge(f, on="series_code", how="inner")[["line", "series_code", "period", "value"]]


def compare_flat_xls(name, vals, cells):
    m = vals.merge(cells, on=["line", "period"], how="outer", indicator=True)
    only_flat = int((m["_merge"] == "left_only").sum())
    only_xls = int((m["_merge"] == "right_only").sum())
    both = m[m["_merge"] == "both"]
    diff = (both["value"] - both["value_xls"]).abs()
    mx = float(diff.max()) if len(diff) else 0.0
    ok = only_flat == 0 and only_xls == 0 and mx <= 1e-9 * max(1.0, float(both["value"].abs().max()))
    check(f"flat file = workbook, {name}", ok, f"{len(both)} cells",
          f"only in flat file: {only_flat}; only in workbook: {only_xls}; max abs diff {mx:g}")
    return ok


def child_gaps(vals, lay):
    """Per parent and period: parent value minus signed sum of its children's values (children with data)."""
    rel = lay.loc[lay["parent_line"].notna(), ["line", "parent_line", "sign"]].copy()
    rel["parent_line"] = rel["parent_line"].astype(int)
    ch = vals.merge(rel, on="line")
    ch["sv"] = ch["sign"] * ch["value"]
    s = ch.groupby(["parent_line", "period"], as_index=False).agg(child_sum=("sv", "sum"), n_child=("sv", "size"))
    par = vals.rename(columns={"line": "parent_line", "value": "parent_value"})[["parent_line", "period", "parent_value"]]
    g = s.merge(par, on=["parent_line", "period"], how="inner")
    g["n_expected"] = g["parent_line"].map(rel["parent_line"].value_counts())
    g["gap"] = g["parent_value"] - g["child_sum"]
    g["rel_gap"] = g["gap"].abs() / g["parent_value"].abs().where(g["parent_value"].ne(0))
    g["beyond_rounding"] = g["gap"].abs() > (g["n_child"] + 1) / 2     # values are rounded to 1 million $
    return g


def report_gaps(name, g, unit="million $"):
    """Pass if every gap beyond rounding sits in a period where some child line is unpublished ('.....')."""
    i = g["gap"].abs().idxmax()
    hard = g[g["beyond_rounding"] & (g["n_child"] == g["n_expected"])]
    soft = g[g["beyond_rounding"] & (g["n_child"] < g["n_expected"])]
    check(f"{name} children sum to parents (signed; 'Less:' lines subtracted)", len(hard) == 0,
          f"largest gap {g.at[i, 'gap']:.0f} {unit} (parent line {g.at[i, 'parent_line']}, {g.at[i, 'period']}; "
          f"{g.at[i, 'n_child']} of {g.at[i, 'n_expected']} children published)",
          f"{len(g)} parent-periods; beyond rounding with all children published: {len(hard)}; "
          f"max relative gap {g['rel_gap'].max():.2e}")
    if len(hard):
        check(f"{name} gaps beyond rounding (all children published)", None, len(hard),
              "; ".join(f"line {a} {b}: {c:.0f}" for a, b, c in hard.head(10)[["parent_line", "period", "gap"]].values))
    if len(soft):
        check(f"{name} gaps where some children are unpublished", None, len(soft),
              "; ".join(f"line {a} {b}: {c:.0f} ({d} of {e} children)" for a, b, c, d, e in
                        soft.head(12)[["parent_line", "period", "gap", "n_child", "n_expected"]].values))
    return g


def unit_of(metric, calc, scale, freq, code=""):
    sa = ", SAAR" if freq == "M" else ""
    if code == "A072RC":
        return "percent of disposable personal income"
    if code == "A229RC":
        return "dollars per person" + sa
    if code == "A229RX":
        return "chained 2017 dollars per person" + sa
    if calc == "Level" and metric == "Current Dollars":
        assert scale == "-6", (code, scale)
        return "millions of dollars" + sa
    if calc == "Level" and metric == "Chained Dollars":
        assert scale == "-6", (code, scale)
        return "millions of chained 2017 dollars" + sa
    if calc == "Level" and metric in ("Fisher Price Index", "Fisher Quantity Index"):
        return "index 2017=100" + (", SA" if freq == "M" else "")
    if calc == "Level" and metric == "Persons":
        assert scale == "-3", (code, scale)
        return "thousands of persons"
    if calc.startswith("Percent change"):
        return ("percent change from preceding month (monthly rate, not annualized)" if freq == "M"
                else "percent change from preceding year")
    raise ValueError((metric, calc, scale, code))


TABLE_UNIT = {"U20405": ("Current Dollars", "Level", "-6"), "U20406": ("Chained Dollars", "Level", "-6"),
              "U20404": ("Fisher Price Index", "Level", "0"), "U20403": ("Fisher Quantity Index", "Level", "0"),
              "T20305": ("Current Dollars", "Level", "-6"), "T20306": ("Chained Dollars", "Level", "-6"),
              "T20805": ("Current Dollars", "Level", "-6"), "T20806": ("Chained Dollars", "Level", "-6")}


def table_name(tid):
    """'U20405' -> '2.4.5U', 'T20600' -> '2.6', 'T20805' -> '2.8.5'."""
    s, a, b, c = tid[1], tid[2:4].lstrip("0"), tid[4:6], tid[0] == "U"
    name = f"{s}.{a}" if b == "00" else f"{s}.{a}.{int(b)}"
    return name + ("U" if c else "")


def build_table(wb, tid, freq, flat, reg, pce_root):
    """Tidy long rows for one table and frequency, plus its layout; values from the flat file, checked
    cell by cell against the workbook sheet."""
    meta, periods, lay, cells, notes = read_sheet(wb, f"{tid}-{freq}")
    lay, odd = add_hierarchy(lay, reg, pce_root)
    if odd:
        check(f"even indentation, {tid}-{freq}", False, f"odd indent on lines {odd}")
    vals = table_values(lay, flat, periods)
    compare_flat_xls(f"{tid}-{freq}", vals, cells)
    if tid in TABLE_UNIT:
        u = unit_of(*TABLE_UNIT[tid], freq)
        units = {ln: u for ln in lay["line"]}
    else:
        r = reg.set_index("series_code")
        units = {ln: unit_of(r.at[c, "metric"], r.at[c, "calc_type"], r.at[c, "default_scale"], freq, c)
                 for ln, c in zip(lay["line"], lay["series_code"]) if c in r.index}
    out = vals.merge(lay[["line", "label", "level", "parent_line", "sign", "section", "context"]], on="line")
    out["table"] = table_name(tid)
    out["table_id"] = tid
    out["freq"] = freq
    out["date"] = [period_to_date(p) for p in out["period"]]
    out["unit"] = out["line"].map(units)
    cols = ["table", "freq", "line", "series_code", "label", "level", "parent_line", "date", "value", "unit",
            "sign", "section", "context", "table_id"]
    out = out[cols].sort_values(["line", "date"]).reset_index(drop=True)
    return out, lay, meta, notes, vals


# ---------------------------------------------------------------------------------------------------------
# 4. Raw-file integrity, then load the NIPA flat files and workbooks
# ---------------------------------------------------------------------------------------------------------
with open(RAWB / "MANIFEST.csv", newline="", encoding="utf-8") as fh:
    MAN = list(csv.DictReader(fh))
bad = [r["file"] for r in MAN if sha256_of(RAWB / r["file"]) != r["sha256"]]
missing = [rel for rel, *_ in DOWNLOADS if not (RAWB / rel).exists()]
check("raw files unchanged since download (sha256 = MANIFEST.csv)", not bad, f"{len(MAN) - len(bad)}/{len(MAN)} match",
      f"changed: {bad}; not vendored: {missing}")
print("Reading NIPA flat files ...")
FM = read_flat_data("nipadataM.txt")
FA = read_flat_data("nipadataA.txt")
REG = read_flat_register()
TREG = read_flat_tables()
check("SeriesRegister series codes unique", REG["series_code"].is_unique, len(REG))
check("flat files: latest month", None, FM["period"].max(), f"latest year {FA['period'].max()}")
for t in ["U20402", "U20802", "U20401"]:
    check(f"TablesRegister lists {t} (contributions/percent change for U detail)", None,
          bool((TREG["TableId"] == t).any()))
WB_U = openpyxl.load_workbook(XLS_U, read_only=True)
WB_S = openpyxl.load_workbook(XLS_S, read_only=True)
check("underlying workbook sheets", None, " ".join(WB_U.sheetnames[1:]),
      "no 2.4.1U/2.4.2U (percent change / contributions) sheets are published for the U detail")

# ---------------------------------------------------------------------------------------------------------
# 5. bea_pce_u_long: Tables 2.4.5U, 2.4.6U, 2.4.4U, 2.4.3U, monthly and annual
# ---------------------------------------------------------------------------------------------------------
print("Building bea_pce_u_long ...")
U_TABLES = ["U20405", "U20406", "U20404", "U20403"]
parts, lays, metas, vals_u = [], {}, [], {}
for tid in tqdm(U_TABLES, desc="U tables"):
    for freq, flat in [("A", FA), ("M", FM)]:
        out, lay, meta, notes, vals = build_table(WB_U, tid, freq, flat, REG, pce_root=True)
        parts.append(out)
        lays[(tid, freq)] = lay
        vals_u[(tid, freq)] = vals
        metas.append({**meta, "notes": " | ".join(notes)})
U_LONG = pd.concat(parts, ignore_index=True)
order_t = {table_name(t): i for i, t in enumerate(U_TABLES)}
U_LONG = U_LONG.sort_values(["table", "freq", "line", "date"], key=lambda s: s.map(order_t) if s.name == "table"
                            else s).reset_index(drop=True)

# layout must be identical across the four tables and both frequencies (same lines, labels, levels, parents)
LAYCOLS = ["line", "label", "level", "parent_line", "sign", "section", "context"]
base = lays[("U20405", "A")][LAYCOLS]
same = all(base.equals(l[LAYCOLS]) for l in lays.values())
check("U tables share one line layout (lines, labels, levels, parents)", same, f"{len(base)} lines")
for m in metas:
    check(f"vintage stamp {m['sheet']}", None, m.get("published", ""), f"{m.get('coverage', '')}; {m.get('file_created', '')}")

# hierarchy vs SeriesRegister parents: the display parent's code must be among the register's parents
lay5 = lays[("U20405", "A")]
code_of = dict(zip(lay5["line"], lay5["series_code"]))
regpar = dict(zip(REG["series_code"], REG["parents"]))
bad = []
for ln, p, c in zip(lay5["line"], lay5["parent_line"], lay5["series_code"]):
    if pd.notna(p) and code_of[int(p)] not in regpar.get(c, "").split("|"):
        bad.append((ln, c, int(p), code_of[int(p)], regpar.get(c, "")))
check("2.4.5U display parents agree with SeriesRegister parents", not bad, f"{len(bad)} disagreements",
      "; ".join(f"line {b[0]} {b[1]}: display parent line {b[2]} {b[3]}, register {b[4]}" for b in bad[:10]))
main = lay5[lay5["section"] == "main"]
check("2.4.5U numbered lines", None, len(lay5), f"main hierarchy lines {len(main)} (1-{main['line'].max()}); "
      f"addenda lines {int((lay5['section'] == 'addenda').sum())}; deepest level {int(main['level'].max())} "
      f"(PCE = level 0)")
deep = main[main["level"] == main["level"].max()]
check("2.4.5U deepest lines", None, "; ".join(f"{a} {b}" for a, b in zip(deep["line"], deep["label"])))

# children-sum check on nominal 2.4.5U (both frequencies); rounding bound = (children + 1) / 2 millions
for freq in ["A", "M"]:
    g = report_gaps(f"2.4.5U-{freq}", child_gaps(vals_u[("U20405", freq)], lays[("U20405", freq)]))
    recent = g[g["period"] >= ("2022" if freq == "A" else "2022M01")]
    j = recent["gap"].abs().idxmax()
    check(f"2.4.5U-{freq} largest children-sum gap since 2022", None, f"{recent.at[j, 'gap']:.0f} million $",
          f"parent line {recent.at[j, 'parent_line']}, {recent.at[j, 'period']}")

# addenda identity: PCE excluding food and energy (374) = PCE (1) - PCE food and energy (370)
v5 = vals_u[("U20405", "M")].pivot(index="period", columns="line", values="value")
d = (v5[1] - v5[370] - v5[374]).abs().max()
check("2.4.5U-M addenda identity line 374 = line 1 - line 370", d <= 1, f"max abs diff {d:.0f} million $")

# chained-dollar detail is not additive: same children-sum on 2.4.6U
for freq in ["A", "M"]:
    g = child_gaps(vals_u[("U20406", freq)], lays[("U20406", freq)])
    i = g["gap"].abs().idxmax()
    last = g["period"].max()
    top = g[(g["parent_line"] == 1) & (g["period"] == last)]
    check(f"2.4.6U-{freq} chained-dollar children do NOT sum to parents", None,
          f"PCE line 1 minus (Goods + Services) in {last}: {float(top['gap'].iloc[0]):.0f} million chained 2017 $",
          f"largest gap anywhere {g.at[i, 'gap']:.0f} (parent line {g.at[i, 'parent_line']}, {g.at[i, 'period']}); "
          f"median |rel gap| {g['rel_gap'].median():.2e}")

U_LONG["parent_line"] = U_LONG["parent_line"].astype("Int64")
u_path = TIDY / "bea_pce_u_long.csv.gz"
U_LONG.to_csv(u_path, index=False, compression={"method": "gzip", "compresslevel": 6, "mtime": 0})
check("wrote bea_pce_u_long.csv.gz", None, f"{len(U_LONG)} rows",
      "; ".join(f"{t}-{f}: {g['date'].min()}..{g['date'].max()} ({g['line'].nunique()} lines)"
                for (t, f), g in U_LONG.groupby(["table", "freq"], sort=False)))

# line dictionary: one row per line with each table's series code, leaf flag and xref to Table 2.5.5
L = lay5[["line", "label", "level", "parent_line", "sign", "section", "context"]].copy()
L["label_short"] = [XREF.sub("", x) for x in L["label"]]
L["xref_table_2_5_5"] = [m.group(1) if (m := XREF.search(x)) else "" for x in L["label"]]
kids = L.loc[L["parent_line"].notna(), "parent_line"].astype(int).value_counts()
L["n_children"] = L["line"].map(kids).fillna(0).astype(int)
L["is_leaf"] = (L["section"] == "main") & (L["n_children"] == 0)
par_of = {a: (int(b) if pd.notna(b) else None) for a, b in zip(L["line"], L["parent_line"])}
sgn_of = dict(zip(L["line"], L["sign"]))
paths, sroot = [], []
for ln, sec in zip(L["line"], L["section"]):
    p, s, x = [ln], 1, ln
    while par_of[x] is not None:
        s *= sgn_of[x]
        x = par_of[x]
        p.append(x)
    paths.append(">".join(str(v) for v in reversed(p)) if sec == "main" else "")
    sroot.append(s if sec == "main" else pd.NA)
L["path_lines"] = paths                      # e.g. 1>150>342>356>357>358
L["sign_to_root"] = pd.array(sroot, dtype="Int64")   # product of signs up to PCE (line 1): how the line enters PCE
vm = vals_u[("U20405", "M")].pivot(index="period", columns="line", values="value")
leaves = L[L["is_leaf"]]
active = [ln for ln in leaves["line"] if vm[ln].last_valid_index() == vm.index[-1]]     # drops 157/158 (end 2001)
start = max(vm[ln].first_valid_index() for ln in active)
late = [f"{ln} ({vm[ln].first_valid_index()})" for ln in active if vm[ln].first_valid_index() > vm.index[0]]
v = vm.loc[start:]
lv = sum(v[ln] * s for ln, s in zip(leaves["line"], leaves["sign_to_root"]) if ln in active)
dd = (v[1] - lv).abs()
check(f"2.4.5U-M: PCE = signed sum of the {len(active)} current leaf lines (sign_to_root), {start} onward",
      bool(v[active].notna().all().all()) and float(dd.max()) <= 0.5 * len(active),
      f"max abs diff {dd.max():.0f} million $ over {len(dd)} months",
      f"rounding bound {0.5 * len(active):.0f}; leaves published later than 1959M01 (their parent is the finest level "
      f"before that): {', '.join(late)}")
for tid in U_TABLES:
    L["code_" + table_name(tid).replace(".", "_")] = L["line"].map(dict(zip(lays[(tid, "A")]["line"],
                                                                             lays[(tid, "A")]["series_code"])))
for tid in U_TABLES:
    for freq in ["A", "M"]:
        v = vals_u[(tid, freq)].groupby("line")["period"].agg(["min", "max"])
        nm = table_name(tid).replace(".", "_")
        L[f"first_{freq}_{nm}"] = L["line"].map(v["min"]).map(lambda p: period_to_date(p) if pd.notna(p) else "")
        L[f"last_{freq}_{nm}"] = L["line"].map(v["max"]).map(lambda p: period_to_date(p) if pd.notna(p) else "")
L.to_csv(TIDY / "bea_pce_u_lines.csv", index=False)
check("wrote bea_pce_u_lines.csv", None, f"{len(L)} lines", f"{int(L['is_leaf'].sum())} leaf lines in the main hierarchy")

# ---------------------------------------------------------------------------------------------------------
# 6. bea_pce_major_long: published Tables 2.3.5 / 2.3.6 (annual) and 2.8.5 / 2.8.6 (monthly)
# ---------------------------------------------------------------------------------------------------------
print("Building bea_pce_major_long ...")
parts, lays_s, vals_s = [], {}, {}
for tid, freq, flat in [("T20305", "A", FA), ("T20306", "A", FA), ("T20805", "M", FM), ("T20806", "M", FM)]:
    out, lay, meta, notes, vals = build_table(WB_S, tid, freq, flat, REG, pce_root=True)
    parts.append(out)
    lays_s[tid], vals_s[tid] = lay, vals
    check(f"vintage stamp {meta['sheet']}", None, meta.get("published", ""), f"{meta.get('coverage', '')}")
    if tid == "T20306":
        check("Table 2.3.6 note on chained dollars", None, next((n for n in notes if n.startswith("Note.")), ""))
MAJ = pd.concat(parts, ignore_index=True)
MAJ["parent_line"] = MAJ["parent_line"].astype("Int64")
MAJ.to_csv(TIDY / "bea_pce_major_long.csv", index=False)
check("wrote bea_pce_major_long.csv", None, f"{len(MAJ)} rows",
      "; ".join(f"{t}: {g['date'].min()}..{g['date'].max()}" for t, g in MAJ.groupby("table", sort=False)))

for tid in ["T20305", "T20805"]:
    report_gaps(table_name(tid), child_gaps(vals_s[tid], lays_s[tid]))

# published lines = U lines with the same series code, period by period (major types are U lines)
for tid, utid, freq in [("T20805", "U20405", "M"), ("T20806", "U20406", "M"), ("T20305", "U20405", "A"),
                        ("T20306", "U20406", "A")]:
    a = vals_s[tid][["series_code", "period", "value"]]
    b = vals_u[(utid, freq)][["series_code", "period", "value"]].drop_duplicates(["series_code", "period"])
    m = a.merge(b, on=["series_code", "period"], suffixes=("_pub", "_u"))
    codes_missing = sorted(set(a["series_code"]) - set(b["series_code"]))
    check(f"{table_name(tid)} = {table_name(utid)} for shared series codes", bool((m["value_pub"] == m["value_u"]).all()),
          f"{len(m)} cells, {m['series_code'].nunique()} series",
          f"published series not in the U table: {codes_missing}")

# Table 2.3.6 residual = line 1 minus the sum of the most detailed lines
lay = lays_s["T20306"]
v = vals_s["T20306"].pivot(index="period", columns="line", values="value")
leaf = [ln for ln in lay.loc[lay["section"] == "main", "line"]
        if ln not in set(lay["parent_line"].dropna().astype(int))]
sgn = dict(zip(lay["line"], lay["sign"]))
resid = v[1] - sum(sgn[ln] * v[ln] for ln in leaf)
d = (resid - v[25]).abs().max()
check("Table 2.3.6 residual line 25 = line 1 - sum of most detailed lines", d <= len(leaf), f"max abs diff {d:.0f}",
      f"most detailed lines {leaf}; residual 2025 = {v.loc['2025', 25]:.0f} million chained 2017 $")

# ---------------------------------------------------------------------------------------------------------
# 7. bea_pi_long: Table 2.6 (monthly) and Table 2.1 (annual)
# ---------------------------------------------------------------------------------------------------------
print("Building bea_pi_long ...")
parts, lays_p, vals_p = [], {}, {}
for tid, freq, flat in [("T20600", "M", FM), ("T20100", "A", FA)]:
    out, lay, meta, notes, vals = build_table(WB_S, tid, freq, flat, REG, pce_root=False)
    parts.append(out)
    lays_p[tid], vals_p[tid] = lay, vals
    check(f"vintage stamp {meta['sheet']}", None, meta.get("published", ""), f"{meta.get('coverage', '')}")
PI = pd.concat(parts, ignore_index=True)
PI["parent_line"] = PI["parent_line"].astype("Int64")
PI.to_csv(TIDY / "bea_pi_long.csv", index=False)
check("wrote bea_pi_long.csv", None, f"{len(PI)} rows",
      "; ".join(f"{t}: {g['date'].min()}..{g['date'].max()} ({g['line'].nunique()} lines)" for t, g in PI.groupby("table", sort=False)))
for tid in ["T20600", "T20100"]:
    g = report_gaps(table_name(tid), child_gaps(vals_p[tid], lays_p[tid]))
    check(f"{table_name(tid)} parents checked", None, sorted(g["parent_line"].unique().tolist()))
    v = vals_p[tid].pivot(index="period", columns="line", values="value")
    d1 = (v[27] - (v[1] - v[26])).abs().max()
    d2 = (v[34] - (v[27] - v[28])).abs().max()
    d3 = (v[35] - (100 * v[34] / v[27]).round(1)).abs().max()
    check(f"{table_name(tid)} identities DPI = PI - taxes, saving = DPI - outlays, rate = saving/DPI",
          d1 <= 1 and d2 <= 1 and d3 <= 0.1 + 1e-9, f"max abs diffs {d1:.0f}, {d2:.0f} million $; {d3:.2f} pp")
    # BEA: real PI excluding transfers (line 36) = (PI - current transfer receipts) deflated by the PCE implicit deflator
    pce = vals_u[("U20405", "M" if tid == "T20600" else "A")].query("line == 1").set_index("period")["value"]
    rpce = (FM if tid == "T20600" else FA).query("series_code == 'DPCERX'").set_index("period")["value"]
    implied = (v[1] - v[16]) * rpce / pce
    rd = ((implied - v[36]) / v[36]).abs().dropna()
    check(f"{table_name(tid)} line 36 = (line 1 - line 16) / PCE implicit deflator (DPCERC/DPCERX)",
          float(rd.max()) < 5e-5, f"max relative diff {rd.max():.2e} over {len(rd)} periods",
          f"{rd.index.min()}..{rd.index.max()}" + (" (monthly chained-dollar PCE starts 2007M01)" if tid == "T20600" else ""))

fred = RAWB / "fred" / "W875RX1.csv"
if fred.exists():
    f = pd.read_csv(fred)
    f.columns = ["date", "fred"]
    f["date"] = f["date"].str[:7]
    w = PI.query("table == '2.6' and line == 36")[["date", "value"]]
    m = f.merge(w, on="date")
    d = (m["fred"] - (m["value"] / 1000).round(3)).abs().max()
    check("FRED W875RX1 (billions) = Table 2.6 line 36 / 1000", d <= 0.051, f"max abs diff {d:.3f} billion",
          f"{len(m)} months")
else:
    check("FRED W875RX1 cross-check", False, "NOT RUN (download failed)",
          "fred/W875RX1.csv not vendored: see raw/bea/FETCH_FAILURES.csv; the internal line-36 check above stands in")

# ---------------------------------------------------------------------------------------------------------
# 8. Headline cross-checks against the September 2026 release (numbers parsed from the PDF text)
# ---------------------------------------------------------------------------------------------------------
print("Release headline cross-checks ...")
with pdfplumber.open(RAWB / "release" / "pi0926.pdf") as pdf:
    REL_PDF = " ".join("\n".join((p.extract_text() or "") for p in pdf.pages).split())
_s = BeautifulSoup((RAWB / "release" / "personal-income-and-outlays-september-2026.html").read_text(encoding="utf-8"), "lxml")
REL_HTML = " ".join((_s.find("main") or _s).get_text(" ", strip=True).split())
check("release stamp (HTML)", None, re.search(r"EMBARGOED UNTIL RELEASE AT [^,]+, \w+, \w+ \d+, \d{4}", REL_HTML).group(0),
      re.search(r"BEA \d+.\d+", REL_HTML).group(0))
v6 = vals_p["T20600"].pivot(index="period", columns="line", values="value")
v5 = vals_u[("U20405", "M")].pivot(index="period", columns="line", values="value")
v4 = vals_u[("U20404", "M")].pivot(index="period", columns="line", values="value")
v6r = vals_u[("U20406", "M")].pivot(index="period", columns="line", values="value")
LAST = FM["period"].max()
PREV = v6.index[v6.index.get_loc(LAST) - 1]
YAGO = f"{int(LAST[:4]) - 1}{LAST[4:]}"


def num(s):
    return float(s.replace(",", "").replace("–", "-").replace("−", "-"))


def rel_check(name, pattern, computed, tol, text="html"):
    m = re.search(pattern, REL_HTML if text == "html" else REL_PDF)
    if not m:
        check(f"release: {name}", False, f"pattern not found in {text} text", pattern)
        return
    pub = [num(x) for x in m.groups()]
    ok = all(abs(a - b) <= tol + 1e-9 for a, b in zip(pub, computed))
    check(f"release: {name}", ok, f"published {pub}", f"from data {[round(c, 3) for c in computed]}")


def dchg(v, ln):
    return (v.at[LAST, ln] - v.at[PREV, ln]) / 1000


def pchg(v, ln, base=None):
    base = base or PREV
    return 100 * (v.at[LAST, ln] / v.at[base, ln] - 1)


rel_check("personal income change", r"Personal income increased \$([\d.]+) billion \(([\d.]+) percent",
          [dchg(v6, 1), round(pchg(v6, 1), 1)], 0.05)
rel_check("DPI change", r"increased \$([\d.]+) billion \(([\d.]+) percent\), and personal",
          [dchg(v6, 27), round(pchg(v6, 27), 1)], 0.05)
rel_check("PCE change", r"\(PCE\) increased \$([\d.]+) billion \(([\d.]+) percent\)",
          [dchg(v6, 29), round(pchg(v6, 29), 1)], 0.05)
rel_check("personal outlays change", r"Personal outlays.{0,120}?increased \$([\d.]+) billion", [dchg(v6, 28)], 0.05)
rel_check("personal saving level and rate", r"Personal saving was \$([\d.,]+) billion, and the personal saving rate.{0,80}?was ([\d.]+) percent",
          [v6.at[LAST, 34] / 1000, v6.at[LAST, 35]], 0.05)
rel_check("goods and services changes", r"increases of \$([\d.]+) billion in spending on goods and \$([\d.]+) billion in spending on services",
          [dchg(v5, 2), dchg(v5, 150)], 0.05)
rel_check("real PCE change", r"Real PCE increased \$([\d.]+) billion", [(v6r.at[LAST, 1] - v6r.at[PREV, 1]) / 1000], 0.05)
rel_check("PCE price index m/m and core m/m", r"From the preceding month, the PCE price index for September increased ([\d.]+) percent\s*\.\s*Excluding food and energy, the PCE price index increased ([\d.]+) percent",
          [round(pchg(v4, 1), 1), round(pchg(v4, 374), 1)], 0.05)
rel_check("PCE price index y/y and core y/y", r"From the same month one year ago, the PCE price index for September increased ([\d.]+) percent\s*\.\s*Excluding food and energy, the PCE price index increased ([\d.]+) percent from one year ago",
          [round(pchg(v4, 1, YAGO), 1), round(pchg(v4, 374, YAGO), 1)], 0.05)
# 'Personal Income and Related Measures' table (August, September percent changes)
TWO = v6.index[v6.index.get_loc(LAST) - 2]
v6x = vals_p["T20600"].pivot(index="period", columns="line", values="value")
for lab, ser in [("Current-dollar personal income", ("pi", 1)), ("Current-dollar DPI", ("pi", 27)),
                 ("Real DPI", ("pi", 37)), ("Current-dollar PCE", ("pi", 29)), ("Real PCE", ("r", 1)),
                 ("PCE price index", ("p", 1)), ("PCE price index, excluding food and energy", ("p", 374))]:
    vv = {"pi": v6x, "r": v6r, "p": v4}[ser[0]]
    comp = [round(100 * (vv.at[PREV, ser[1]] / vv.at[TWO, ser[1]] - 1), 1),
            round(100 * (vv.at[LAST, ser[1]] / vv.at[PREV, ser[1]] - 1), 1)]
    rel_check(f"related measures table: {lab}", re.escape(lab) + r" ([–\-]?[\d.]+) ([–\-]?[\d.]+)", comp, 0.05,
              text="pdf")
# 'Changes in Monthly Consumer Spending' chart values (billions of dollars, SAAR), by major type
CAT = {"Gasoline and other energy goods": 113, "Transportation services": 190, "Housing and utilities": 152,
       "Food services and accommodations": 234, "Health care": 172, "Financial services and insurance": 252,
       "Other services": 280, "Food and beverages": 73, "Other nondurable goods": 120,
       "Clothing and footwear": 104, "Furnishings and durable household equipment": 23,
       "Recreational goods and vehicles": 38, "Other durable goods": 62,
       "Final expenditures of nonprofit institutions": 342, "Recreation services": 209,
       "Motor vehicles and parts": 4}
for lab, ln in CAT.items():
    rel_check(f"spending-change chart: {lab}", r"(?:^| )" + re.escape(lab) + r" ([–\-]?[\d.]+)(?: |$)",
              [round(dchg(v5, ln), 1)], 0.051, text="pdf")

# ---------------------------------------------------------------------------------------------------------
# 9. bea_dpi_distribution: national distribution of personal income (2000-2024) + 2025 nowcast
# ---------------------------------------------------------------------------------------------------------
print("Building bea_dpi_distribution ...")
DN = RAWB / "distribution" / "national"
sf = pd.read_csv(DN / "summary-file.csv", dtype=str, keep_default_na=False)
sf.columns = ["year", "ranking", "income_concept", "nipa_t29_line", "quantile_or_metric", "value_raw"]

METRICS = {  # summary-metric label -> (metric, unit)
    "Equivalized Gini": ("gini_equivalized", "Gini index (0-1) of equivalized income"),
    "Equivalized 50/10 Ratio": ("ratio_p50_p10_equivalized", "ratio of percentiles of equivalized income"),
    "Equivalized 80/20 Ratio": ("ratio_p80_p20_equivalized", "ratio of percentiles of equivalized income"),
    "Equivalized 90/10 Ratio": ("ratio_p90_p10_equivalized", "ratio of percentiles of equivalized income"),
    "Equivalized 90/50 Ratio": ("ratio_p90_p50_equivalized", "ratio of percentiles of equivalized income"),
    "Mean (Nominal)": ("mean_nominal", "current dollars per household (total, unequivalized income)"),
    "Mean ($2017)": ("mean_2017usd", "2017 dollars per household (total, unequivalized income)"),
    "Median (Nominal)": ("median_nominal", "current dollars per household"),
    "Median ($2017)": ("median_2017usd", "2017 dollars per household"),
    "Total ($Billions)": ("total", "billions of current dollars"),
}


def parse_group(q):
    m = re.fullmatch(r"(\d+)-(\d+)%", q)
    if m:
        lo, hi = int(m.group(1)), int(m.group(2))
        if hi - lo == 10:
            return f"D{hi // 10:02d}", lo, hi
        if hi - lo == 20:
            return f"Q{hi // 20}", lo, hi
        raise ValueError(q)
    return {"Bottom 5%": ("B05", 0, 5), "Top 5%": ("T05", 95, 100), "Top 1%": ("T01", 99, 100)}.get(q, ("ALL", np.nan, np.nan))


rows = []
for r in sf.itertuples(index=False):
    grp, lo, hi = parse_group(r.quantile_or_metric)
    if grp != "ALL":
        metric, unit = "share", "fraction of the income concept's total over all households"
    elif r.income_concept in ("Unweighted Observations", "Weighted Observations"):
        metric = "obs_unweighted" if r.income_concept.startswith("Unweighted") else "obs_weighted"
        unit = "CPS household records" if metric == "obs_unweighted" else "households (weighted count)"
    else:
        metric, unit = METRICS[r.quantile_or_metric]
    val, vlo, vhi = np.nan, np.nan, np.nan
    m = re.fullmatch(r"\[(-?[\d.]+)-(-?[\d.]+)\]", r.value_raw)
    if m:
        vlo, vhi = float(m.group(1)), float(m.group(2))
    elif r.value_raw in ("N/A", ""):
        pass
    else:
        val = float(r.value_raw)
    y = int(r.year)
    rows.append({"year": y, "status": "provisional" if y == 2024 else "final",
                 "ranking": {"Equivalized Personal Income": "equivalized_pi",
                             "Equivalized Disposable Personal Income": "equivalized_dpi", "": "none"}[r.ranking],
                 "income_concept": r.income_concept,
                 "nipa_t29_line": int(float(r.nipa_t29_line)) if r.nipa_t29_line else pd.NA,
                 "group": grp, "pct_lo": lo, "pct_hi": hi, "metric": metric, "value": val,
                 "value_lo": vlo, "value_hi": vhi, "unit": unit, "source": "summary-file.csv",
                 "quantile_or_metric_raw": r.quantile_or_metric})

# 2025 experimental nowcast (quintile shares of personal income and their nominal growth), from the page table
soup = BeautifulSoup((RAWB / "distribution" / "distribution-of-personal-income.html").read_text(encoding="utf-8"), "lxml")
tables = [t for t in soup.find_all("table") if "Nowcast" in t.get_text()]
assert len(tables) == 1, "nowcast table not found (or ambiguous) on the distribution page"
nc_rows = []
for tr in tables[0].find_all("tr"):
    cells = [c.get_text(" ", strip=True) for c in tr.find_all(["td", "th"])]
    if cells and re.match(r"Q\d: \d+-\d+%", cells[0]):
        nc_rows.append(cells)
hdr = [" ".join(c.get_text(" ", strip=True).split()) for c in tables[0].find_all("tr")[0].find_all(["td", "th"])]
check("nowcast table header", None, " | ".join(hdr))
assert len(nc_rows) == 5 and all(len(c) == 4 for c in nc_rows), nc_rows
nowcast_2024 = {}
for q, s24, s25, g25 in nc_rows:
    grp, lo, hi = parse_group(q.split(": ")[1])
    nowcast_2024[grp] = float(s24)
    base = {"year": 2025, "status": "nowcast_experimental", "ranking": "not_stated",
            "income_concept": "Personal income", "nipa_t29_line": pd.NA, "group": grp, "pct_lo": lo, "pct_hi": hi,
            "value_lo": np.nan, "value_hi": np.nan, "source": "distribution-of-personal-income.html (nowcast table)",
            "quantile_or_metric_raw": q}
    rows.append({**base, "metric": "share", "value": round(float(s25) / 100, 6),
                 "unit": "fraction of the income concept's total over all households"})
    rows.append({**base, "metric": "growth_nominal_2024_2025", "value": float(g25.rstrip("%")),
                 "unit": "percent change 2024-2025 in the group's nominal personal income"})
DPI = pd.DataFrame(rows)
DPI["nipa_t29_line"] = DPI["nipa_t29_line"].astype("Int64")
DPI = DPI.sort_values(["year", "ranking", "nipa_t29_line", "income_concept", "metric", "group"],
                      na_position="last").reset_index(drop=True)
DPI.to_csv(TIDY / "bea_dpi_distribution.csv", index=False)
check("wrote bea_dpi_distribution.csv", None, f"{len(DPI)} rows", f"years {DPI['year'].min()}-{DPI['year'].max()}")

# checks: decile and quintile shares sum to 1; 2024 nowcast-page column = summary file; xlsx 2023/2024 = summary file;
# NIPA Table 2.10 (flat file) = summary file deciles
sh = DPI[(DPI["metric"] == "share") & DPI["group"].str.match(r"^[DQ]")].copy()
sh["kind"] = sh["group"].str[0]
tot = sh.groupby(["year", "ranking", "income_concept", "kind"])["value"].sum()
check("decile/quintile shares sum to 1 (by year, ranking, concept)", bool(((tot - 1).abs() <= 0.006).all()),
      f"max |sum - 1| = {(tot - 1).abs().max():.3f}", f"{len(tot)} groups; published to 3 decimals")
q24 = DPI.query("year == 2024 and ranking == 'equivalized_pi' and income_concept == 'Personal income' and metric == 'share'")
q24 = dict(zip(q24["group"], q24["value"]))
d = max(abs(nowcast_2024[g] - round(100 * q24[g], 1)) for g in nowcast_2024)
check("nowcast page '2024 share (published)' = summary file 2024 quintile shares of PI", d < 1e-9, f"max diff {d:.2f} pp")
nc = DPI.query("year == 2025")
g25 = dict(zip(nc.query("metric == 'growth_nominal_2024_2025'")["group"], nc.query("metric == 'growth_nominal_2024_2025'")["value"]))
s25 = dict(zip(nc.query("metric == 'share'")["group"], nc.query("metric == 'share'")["value"]))
agg = sum(q24[g] * (1 + g25[g] / 100) for g in g25)
impl = {g: q24[g] * (1 + g25[g] / 100) / agg for g in g25}
check("nowcast internal consistency (2024 shares x group growth -> 2025 shares)", None,
      f"implied aggregate PI growth {100 * (agg - 1):.2f}%",
      "implied 2025 shares " + ", ".join(f"{g} {100 * impl[g]:.2f} (pub {100 * s25[g]:.1f})" for g in sorted(impl)))

for yr in [2023, 2024]:
    wbx = openpyxl.load_workbook(DN / f"distribution-of-personal-income-inequality-metrics-summary-{yr}.xlsx",
                                 read_only=True, data_only=True)
    t1 = [r for r in wbx["Table 1"].iter_rows(values_only=True) if r and isinstance(r[0], int)]
    t2 = [r for r in wbx["Table 2"].iter_rows(values_only=True) if r and isinstance(r[0], int) and isinstance(r[1], str)]
    nd, nm = 0, 0
    sub = DPI[(DPI["year"] == yr) & (DPI["metric"] == "share")]
    for r in t1:
        if r[1] not in set(sub["income_concept"]) and r[1] not in ("From business (net)", "From nonprofit institutions",
                                                                   "Less: Contributions for government social insurance, domestic", "Less: Taxes"):
            continue
        concept = {"From business (net)": "Household current transfer receipts from business (net)",
                   "From nonprofit institutions": "Household current transfer receipts from nonprofit institutions",
                   "Less: Contributions for government social insurance, domestic": "Contributions for government social insurance, domestic",
                   "Less: Taxes": "Taxes"}.get(r[1], r[1])
        for k, rk in [(0, "equivalized_pi"), (1, "equivalized_dpi")]:
            for i in range(10):
                x = sub[(sub["ranking"] == rk) & (sub["income_concept"] == concept) & (sub["group"] == f"D{i + 1:02d}")]["value"]
                nm += 1
                if len(x) != 1 or abs(float(x.iloc[0]) - float(r[3 + 10 * k + i])) > 1e-9:
                    nd += 1
    check(f"inequality-metrics workbook {yr} Table 1 decile shares = summary file", nd == 0, f"{nm - nd}/{nm} match")
    # Table 2 metrics: PI column under PI ranking, DPI column under DPI ranking
    nd, nm = 0, 0
    lab2 = {"0-20% share": "Q1", "20-40% share": "Q2", "40-60% share": "Q3", "60-80% share": "Q4", "80-100% share": "Q5",
            "Top 1% share": "T01", "Top 5% share": "T05", "Bottom 5%": "B05"}
    for r in t2:
        for col, concept, rk in [(2, "Personal income", "equivalized_pi"), (3, "Disposable personal income", "equivalized_dpi")]:
            q = DPI[(DPI["year"] == yr) & (DPI["ranking"] == rk) & (DPI["income_concept"] == concept)]
            if r[1] in lab2:
                x = q[(q["metric"] == "share") & (q["group"] == lab2[r[1]])]
            elif r[1].startswith("Mean ($2017)"):
                x = q[q["metric"] == "mean_2017usd"]
            elif r[1].startswith("Mean ("):
                x = q[q["metric"] == "mean_nominal"]
            elif r[1].startswith("Median ($2017)"):
                x = q[q["metric"] == "median_2017usd"]
            elif r[1].startswith("Median ("):
                x = q[q["metric"] == "median_nominal"]
            else:
                x = q[q["metric"] == {"Eq. 90/10 Ratio": "ratio_p90_p10_equivalized", "Eq. 80/20 Ratio": "ratio_p80_p20_equivalized",
                                      "Eq. Gini": "gini_equivalized"}[r[1]]]
            nm += 1
            if len(x) != 1:
                nd += 1
                continue
            cell = r[col]
            if isinstance(cell, str):
                lo_, hi_ = [float(s) for s in cell.strip("[]").split("-")]
                okc = abs(lo_ - x["value_lo"].iloc[0]) < 1e-9 and abs(hi_ - x["value_hi"].iloc[0]) < 1e-9
            else:
                okc = abs(float(cell) - float(x["value"].iloc[0])) <= 0.5 + 1e-9 * abs(float(cell))  # means/medians rounded to $1
            nd += 0 if okc else 1
    check(f"inequality-metrics workbook {yr} Table 2 metrics = summary file", nd == 0, f"{nm - nd}/{nm} match")

t210 = FA[FA["series_code"].str.match(r"^DP0012[67]\d$")].copy()
t210["n"] = t210["series_code"].str[-2:].astype(int)
t210["concept"] = np.where(t210["n"] < 70, "Personal income", "Disposable personal income")
t210["group"] = [f"D{(n % 10) + 1:02d}" for n in t210["n"]]
t210["year"] = t210["period"].astype(int)
cmp = []
for concept, rk in [("Personal income", "equivalized_pi"), ("Disposable personal income", "equivalized_dpi")]:
    q = DPI[(DPI["metric"] == "share") & (DPI["ranking"] == rk) & (DPI["income_concept"] == concept)
            & DPI["group"].str.startswith("D")][["year", "group", "value"]]
    m = t210[t210["concept"] == concept].merge(q, on=["year", "group"])
    m["d"] = (m["value_x"] - 100 * m["value_y"]).abs()
    cmp.append((concept, rk, len(m), int((m["d"] > 0.051).sum()), float(m["d"].max())))
check("NIPA Table 2.10 (flat file, % to 1 decimal) = summary-file decile shares, each concept ranked by its own "
      "equivalized income", all(c[3] == 0 and c[2] == 250 for c in cmp),
      "; ".join(f"{a} ({b}): {c} cells, {d} differ by >0.05pp (max {e:.2f})" for a, b, c, d, e in cmp))

# summary-file totals vs current NIPA vintage (the distribution was released 2026-06-16, before the 2026 annual update)
pi_now = PI.query("table == '2.1' and line == 1").set_index("date")["value"] / 1000
tt = DPI.query("metric == 'total' and income_concept == 'Personal income'").set_index("year")["value"]
dd = {y: tt[y] - pi_now[str(y)] for y in tt.index}
check("summary-file personal income totals vs current NIPA Table 2.1 line 1", None,
      ", ".join(f"{y}: {tt[y]:.0f} vs {pi_now[str(y)]:.0f}" for y in [2019, 2021, 2022, 2023, 2024]),
      f"max |diff| {max(abs(x) for x in dd.values()):.0f} billion $; 2000-2020 max |diff| "
      f"{max(abs(dd[y]) for y in dd if y <= 2020):.1f} (totals are rounded to $1bn)")

# ---------------------------------------------------------------------------------------------------------
# 10. bea_pce_price_by_income_decile: income-stratified PCE price index (ISPCEPX)
# ---------------------------------------------------------------------------------------------------------
print("Building bea_pce_price_by_income_decile ...")
wbx = openpyxl.load_workbook(RAWB / "distribution" / "ispcepx" / "ispecpx_table.xlsx", read_only=True, data_only=True)
xr = [r for r in wbx[wbx.sheetnames[0]].iter_rows(values_only=True) if r and r[0] is not None]
hdr, data = list(xr[0]), [r for r in xr[1:] if isinstance(r[0], int)]
rows = []
for r in data:
    for col, v in zip(hdr[1:], r[1:]):
        if col == "Published PCE PI":
            grp, lo, hi, base, grouping = "ALL", np.nan, np.nan, "2017=100", "all (published aggregate PCE price index)"
        elif col == "Indexed Published PCE PI":
            grp, lo, hi, base, grouping = "ALL", np.nan, np.nan, "2000=100", "all (published aggregate PCE price index)"
        else:
            grp, lo, hi = parse_group(col.replace("ISPCEPX: ", ""))
            base = "2000=100"
            grouping = "decile of equivalized DPI" if grp.startswith("D") else "quintile of equivalized DPI"
        rows.append({"year": int(r[0]), "group": grp, "grouping": grouping, "pct_lo": lo, "pct_hi": hi,
                     "index_base": base, "value": float(v), "imputed_weights": int(r[0]) == 2024 and grp != "ALL",
                     "source_column": col})
ISP = pd.DataFrame(rows)
ISP.to_csv(TIDY / "bea_pce_price_by_income_decile.csv", index=False)
check("wrote bea_pce_price_by_income_decile.csv", None, f"{len(ISP)} rows",
      f"years {ISP['year'].min()}-{ISP['year'].max()}; columns: {', '.join(hdr)}")
w = ISP.pivot_table(index="year", columns="source_column", values="value")
check("ISPCEPX: every group index = 100 in 2000", bool((ISP.query("year == 2000 and index_base == '2000=100'")["value"] == 100).all()))
d = (w["Indexed Published PCE PI"] - (100 * w["Published PCE PI"] / w.at[2000, "Published PCE PI"]).round(2)).abs().max()
check("ISPCEPX: 'Indexed Published PCE PI' = Published PCE PI rebased to 2000", d <= 0.011, f"max abs diff {d:.3f}")
cur = FA.query("series_code == 'DPCERG'").assign(year=lambda x: x["period"].astype(int)).set_index("year")["value"]
dd = (w["Published PCE PI"] - cur.reindex(w.index).round(2))
check("ISPCEPX 'Published PCE PI' vs current-vintage 2.4.4U line 1 (DPCERG)", None,
      f"max |diff| {dd.abs().max():.3f} index points",
      "differences by year (ISPCEPX minus current): " + ", ".join(f"{y}: {x:+.2f}" for y, x in dd.items() if abs(x) > 0.005))
dec = w[[c for c in w.columns if c.startswith("ISPCEPX") and int(re.findall(r"(\d+)-(\d+)", c)[0][1]) - int(re.findall(r"(\d+)-(\d+)", c)[0][0]) == 10]]
infl = 100 * (dec.iloc[-1] / dec.loc[2019] - 1)
check("ISPCEPX cumulative inflation 2019-2024 by decile (info)", None,
      ", ".join(f"{c.replace('ISPCEPX: ', '')} {x:.1f}%" for c, x in infl.items()),
      f"aggregate {100 * (w.at[2024, 'Indexed Published PCE PI'] / w.at[2019, 'Indexed Published PCE PI'] - 1):.1f}%")

# ---------------------------------------------------------------------------------------------------------
# 11. Joint distribution of DPI and PCE (distribution of personal saving), 2000-2023
# ---------------------------------------------------------------------------------------------------------
print("Building joint DPI/PCE files ...")
wbj = openpyxl.load_workbook(RAWB / "distribution" / "joint_dpi_pce" / "joint_dist_summary.xlsx", read_only=True, data_only=True)


def sheet_rows(ws):
    return [r for r in ws.iter_rows(values_only=True) if any(v is not None for v in r)]


s1 = sheet_rows(wbj["shares of NIPA totals"])
METJ = {"Total ($ Billions)": ("total", "billions of current dollars"),
        "Mean (Nominal)": ("mean_nominal", "current dollars per household"),
        "Mean ($2017)": ("mean_2017usd", "2017 dollars per household"),
        "Median (Nominal)": ("median_nominal", "current dollars per household"),
        "Median ($2017)": ("median_2017usd", "2017 dollars per household")}
rows = []
for r in s1[1:]:
    y, rk, ser, line, q, v = r[:6]
    grp, lo, hi = parse_group(q)
    if grp == "ALL":
        metric, unit = METJ[q]
    else:
        metric, unit = "share", "fraction of the NIPA total of the series"
    rows.append({"year": int(y), "ranking": "equivalized_dpi", "series": ser, "nipa_t21_line": int(line), "group": grp,
                 "pct_lo": lo, "pct_hi": hi, "metric": metric, "value": float(v), "unit": unit,
                 "source_sheet": "shares of NIPA totals", "quantile_or_metric_raw": q})
check("joint workbook 'shares of NIPA totals' ranking field", None, sorted({r[1] for r in s1[1:]}))
s3 = sheet_rows(wbj["savings rates"])
for r in s3[1:]:
    for col, v in zip(s3[0][1:], r[1:]):
        grp, lo, hi = parse_group(col)
        rows.append({"year": int(r[0]), "ranking": "equivalized_dpi", "series": "Personal saving rate", "nipa_t21_line": pd.NA,
                     "group": grp, "pct_lo": lo, "pct_hi": hi, "metric": "saving_rate", "value": float(v),
                     "unit": "personal saving / DPI of the group (fraction)", "source_sheet": "savings rates",
                     "quantile_or_metric_raw": col})
JD = pd.DataFrame(rows)
JD["nipa_t21_line"] = JD["nipa_t21_line"].astype("Int64")
JD = JD.sort_values(["year", "series", "metric", "pct_lo", "pct_hi"], na_position="first").reset_index(drop=True)
JD.to_csv(TIDY / "bea_joint_dpi_pce_by_decile.csv", index=False)
check("wrote bea_joint_dpi_pce_by_decile.csv", None, f"{len(JD)} rows", f"years {JD['year'].min()}-{JD['year'].max()}")

s2 = sheet_rows(wbj["joint shares"])
JS = pd.DataFrame(s2[1:], columns=["year", "dpi_group_raw", "pce_group_raw", "share_households", "share_dpi", "share_pce"])
JS["year"] = JS["year"].astype(int)
for side in ["dpi", "pce"]:
    g = [parse_group(x) for x in JS[f"{side}_group_raw"]]
    JS[f"{side}_group"] = [x[0] for x in g]
JS = JS[["year", "dpi_group", "pce_group", "share_households", "share_dpi", "share_pce", "dpi_group_raw", "pce_group_raw"]]
JS.to_csv(TIDY / "bea_joint_dpi_pce_joint_shares.csv", index=False)
check("wrote bea_joint_dpi_pce_joint_shares.csv", None, f"{len(JS)} rows", f"years {JS['year'].min()}-{JS['year'].max()}")

dsh = JD[(JD["metric"] == "share") & JD["group"].str.startswith("D")].groupby(["year", "series"])["value"].sum()
check("joint file: decile shares of DPI and PCE sum to 1", bool(((dsh.xs("Disposable Personal Income", level=1) - 1).abs() <= 0.006).all()
                                                               and ((dsh.xs("Personal Consumption Expenditures", level=1) - 1).abs() <= 0.006).all()),
      f"max |sum-1| DPI {(dsh.xs('Disposable Personal Income', level=1) - 1).abs().max():.3f}, "
      f"PCE {(dsh.xs('Personal Consumption Expenditures', level=1) - 1).abs().max():.3f}, "
      f"saving {(dsh.xs('Personal Saving', level=1) - 1).abs().max():.3f}")
jsd = JS[JS["dpi_group"].str.startswith("D") & JS["pce_group"].str.startswith("D")].groupby("year")[["share_households", "share_dpi", "share_pce"]].sum()
check("joint shares over the 10x10 decile grid sum to 1", bool(((jsd - 1).abs() <= 0.03).all().all()),
      f"max |sum-1| {(jsd - 1).abs().max().max():.3f}", "Top 1%/Top 5% rows overlap 90-100% and are excluded from the sum")
T = JD[JD["metric"] == "total"].pivot(index="year", columns="series", values="value")
S = JD[(JD["metric"] == "share") & JD["group"].str.startswith("D")].pivot_table(index=["year", "group"], columns="series", values="value")
R = JD[(JD["metric"] == "saving_rate") & JD["group"].str.startswith("D")].set_index(["year", "group"])["value"]
impl = S["Personal Saving"] * T["Personal Saving"].reindex(S.index.get_level_values(0)).values / (
    S["Disposable Personal Income"] * T["Disposable Personal Income"].reindex(S.index.get_level_values(0)).values)
dr = (impl - R).abs()
check("joint file: decile saving rate = saving share x total / (DPI share x total)", None,
      f"max abs diff {dr.max():.3f}; median {dr.median():.4f}", "shares are rounded to 3 decimals, so only approximate")
cur21 = PI.query("table == '2.1'").pivot(index="date", columns="line", values="value") / 1000
dd = [(y, T.at[y, "Disposable Personal Income"] - cur21.at[str(y), 27], T.at[y, "Personal Consumption Expenditures"] - cur21.at[str(y), 29])
      for y in T.index]
check("joint file totals vs current NIPA Table 2.1 (DPI line 27, PCE line 29)", None,
      "; ".join(f"{y}: DPI {a:+.0f}, PCE {b:+.0f} bn" for y, a, b in dd if y >= 2019),
      f"2000-2020 max |diff| DPI {max(abs(a) for y, a, b in dd if y <= 2020):.1f}, PCE {max(abs(b) for y, a, b in dd if y <= 2020):.1f} bn")

# ---------------------------------------------------------------------------------------------------------
# 12. Headline facts for the report
# ---------------------------------------------------------------------------------------------------------
print("Headline facts ...")
M6 = v6.index[v6.index.get_loc(LAST) - 6]
for nm_, ser in [("real PCE (2.4.6U/2.8.6 line 1, DPCERX)", v6r[1]),
                 ("real PI excluding current transfer receipts (2.6 line 36, W875RX)", v6x[36]),
                 ("real DPI (2.6 line 37, A067RX)", v6x[37]),
                 ("nominal PCE (2.6 line 29)", v6x[29]),
                 ("nominal PI excluding current transfer receipts (2.6 line 1 - line 16, derived)", v6x[1] - v6x[16])]:
    c6 = 100 * (ser[LAST] / ser[M6] - 1)
    c12 = 100 * (ser[LAST] / ser[YAGO] - 1)
    check(f"latest: {nm_}", None, f"{LAST}: {ser[LAST] / 1e6:.4f} trillion",
          f"6-month change ({M6}->{LAST}) {c6:.2f}% ({100 * ((1 + c6 / 100) ** 2 - 1):.2f}% annualized); "
          f"12-month change ({YAGO}->{LAST}) {c12:.2f}%")

pd.DataFrame(CHECKS).to_csv(TIDY / "bea_checks.csv", index=False)
nfail = sum(c["status"] == "FAIL" for c in CHECKS)
print(f"Done. {len(CHECKS)} checks, {nfail} FAIL (see consumption/data/tidy/bea_checks.csv).")
