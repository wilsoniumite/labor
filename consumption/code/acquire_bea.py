# acquire_bea.py — vendor BEA national accounts (PCE by type of product incl. underlying detail, monthly and
# annual; personal income and its disposition) and BEA's distributional statistics (distribution of personal
# income, 2025 nowcast, income-stratified PCE price index, joint DPI/PCE distribution); then build tidy long
# files from the raw files only.
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
from common import fetch, RAW, TIDY

import csv
import datetime as dt

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
     "bea_pce_u_long.csv, bea_pi_long.csv, bea_pce_published_long.csv (values, series codes, hierarchy via "
     "SeriesCodeParents); Table 2.10 decile shares cross-check"),
    # --- NIPA workbooks (route b): table layout (line order, indentation, labels) and release stamps -------
    ("nipa/xls_underlying/Section2All_xls.xlsx", APPS + "/national/Release/XLS/Underlying/Section2All_xls.xlsx",
     "BEA NIPA underlying-detail workbook, Section 2 (Tables 2.3.4U-2.3.6U, 2.4.3U-2.4.6U; annual, "
     "quarterly and monthly sheets), release of 2026-10-29",
     "bea_pce_u_long.csv: line layout, indentation (level), labels, release/last-revised stamps; "
     "cell-by-cell cross-check of flat-file values"),
    ("nipa/xls_survey/Section2All_xls.xlsx", APPS + "/national/Release/XLS/Survey/Section2All_xls.xlsx",
     "BEA NIPA published-tables workbook, Section 2 (Tables 2.1-2.10 incl. 2.3.x, 2.6, 2.8.x; annual, "
     "quarterly and monthly sheets), release of 2026-10-29",
     "bea_pi_long.csv and bea_pce_published_long.csv: line layout, indentation, labels, release stamps; "
     "cross-check of flat-file values"),
    # --- the September 2026 Personal Income and Outlays release: headline numbers for cross-checks --------
    ("release/pi0926.pdf", WWW + "/sites/default/files/2026-10/pi0926.pdf",
     "BEA news release 'Personal Income and Outlays, September 2026' (BEA 26-46, 2026-10-29), full PDF "
     "with release tables", "headline cross-checks (README_bea.md)"),
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
    # --- joint distribution of DPI and PCE (distribution of personal saving), BEA-BLS, 2004-2023 ----------
    ("distribution/joint_dpi_pce/joint_dist_summary.xlsx", WWW + "/sites/default/files/2026-05/joint_dist_summary.xlsx",
     "BEA distribution of personal saving based on a joint distribution of DPI and PCE: summary workbook, "
     "all available years (2004-2023) and metrics", "bea_joint_dpi_pce_by_decile.csv"),
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
     "cross-check of bea_pi_long.csv (Table 2.6 real PI excluding transfers)"),
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


FAILS = fetch_all(DOWNLOADS)
