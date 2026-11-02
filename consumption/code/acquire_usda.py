# acquire_usda.py — vendor USDA ERS Technical Bulletin 1929 (Muhammad, Seale, Meade and Regmi, "International
# Evidence on Food Consumption Patterns: An Update Using 2005 International Comparison Program Data", 2011, revised
# 2013) and the data files ERS publishes with it (the "International Food Consumption Patterns" data product, 2005
# ICP round: budget shares, marginal shares, income and price elasticities for 144 countries), then build tidy files
# from the raw files only.
#
# Run from the repo root:  venv/bin/python -I consumption/code/acquire_usda.py
#   --offline       never touch the network (build from what is vendored)
#   --retry-failed  retry downloads recorded in raw/usda/FETCH_FAILURES.csv (default: a recorded failure is not
#                   retried, per the stop-and-report rule)
# Downloads skip files already vendored, so a rerun is offline and rebuilds every tidy file from raw.
# Plain functions and top-level code (notebook-cell friendly). No modelling here: the elasticity recomputation
# below only verifies the transcription against the bulletin's own published elasticities.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import fetch, manifest_row, RAW, TIDY, REPO

import csv
import datetime as dt
import re

import numpy as np
import pandas as pd
from tqdm.auto import tqdm

SRC = "usda"
RAWU = RAW / SRC
RAWU.mkdir(parents=True, exist_ok=True)
TIDY.mkdir(parents=True, exist_ok=True)
OFFLINE = "--offline" in sys.argv
RETRY_FAILED = "--retry-failed" in sys.argv

# ---------------------------------------------------------------------------------------------------------
# 1. Download list. (rel_file, url, what_it_is, used_for)
#    Every URL is the link exactly as published on the ERS pages (the ?v= query is ERS's own cache key).
# ---------------------------------------------------------------------------------------------------------
ERS = "https://www.ers.usda.gov"
DP = ERS + "/data-products/international-food-consumption-patterns"

DOWNLOADS = [
    # --- the publication page and its three downloads ---------------------------------------------------------
    ("report/pub-details_47581.html", ERS + "/publications/pub-details?pubid=47581",
     "ERS publication page for TB-1929 as of the pull date (redirects to /publications/47581): authors, date "
     "3/22/2011, the three downloads (report summary PDF, full report PDF, TB1929.zip)", "provenance (README_usda.md)"),
    ("report/tb-1929.pdf", ERS + "/media/8559/tb-1929.pdf?v=21006",
     "TB-1929 full report PDF ('Full Report', 2.02 MB on the publication page): Muhammad, Seale, Meade and Regmi, "
     "International Evidence on Food Consumption Patterns: An Update Using 2005 ICP Data",
     "usda_tb1929_params.csv (model equations, parameter tables), budget shares and elasticity tables for the "
     "verification, README_usda.md (equations, category definitions)"),
    ("report/tb-1929-report-summary.pdf", ERS + "/media/7267/tb-1929-report-summary.pdf?v=48253",
     "TB-1929 report summary PDF ('Report Summary', 209 KB on the publication page; 2 pages, modified 2013-02-13)",
     "category list cross-check (usda_tb1929_checks.csv)"),
    ("report/download-tb1929.zip", ERS + "/media/14891/download-tb1929.zip?v=99965",
     "TB1929.zip ('Download TB1929.zip', 455 KB on the publication page): readme.txt and the report's four "
     "figures as PNG (Fig01-Fig04, March 2011); no tables or data",
     "provenance only (inventoried in usda_tb1929_checks.csv; nothing parsed)"),
    # --- the data product the bulletin's estimates are published in -------------------------------------------
    ("dataproduct/international-food-consumption-patterns.html", DP,
     "ERS data product page 'International Food Consumption Patterns' as of the pull date (Updated 12/31/2025; "
     "file list with last-updated dates; 'no longer being updated')", "provenance (README_usda.md)"),
    ("dataproduct/documentation.html", DP + "/documentation",
     "ERS data product documentation page as of the pull date (Updated 1/8/2025): scope, category coverage, "
     "estimation procedure, data-item definitions", "category definitions (README_usda.md)"),
    ("dataproduct/budget-shares-broad-aggregates-conditional-food.xls",
     ERS + "/media/5659/budget-shares-for-broad-aggregates-and-conditional-budget-shares-for-food-categories.xls"
     "?v=79564",
     "ERS data product file 'Budget Shares for Broad Aggregates and Conditional Budget Shares for Food Categories' "
     "(XLS, sheet Table9, last updated 2/11/2011): the bulletin's Table 2, income-group averages",
     "cross-check of Table 2 (usda_tb1929_checks.csv)"),
    ("dataproduct/income-elasticities-broad-categories.xls",
     ERS + "/media/5656/income-elasticities-for-broad-consumption-categories-144-countries-2005.xls?v=30940",
     "ERS data product file 'Income Elasticities for Broad Consumption Categories, 144 Countries, 2005' (XLS, sheet "
     "Table1, last updated 9/4/2013): appendix table 1, with per capita income relative to the US to 14 digits",
     "usda_tb1929_country_long.csv, usda_tb1929_countries.csv, usda_tb1929_recompute.csv"),
    ("dataproduct/income-elasticities-food-subcategories.xls",
     ERS + "/media/5661/income-elasticities-for-food-subcategories-144-countries-2005.xls?v=94803",
     "ERS data product file 'Income Elasticities for Food Subcategories, 144 Countries, 2005' (XLS, sheet Table5, "
     "last updated 9/4/2013): appendix table 5 to 6 decimals, with per capita food spending relative to the US",
     "usda_tb1929_country_long.csv, usda_tb1929_countries.csv, usda_tb1929_recompute.csv"),
    ("dataproduct/marginal-shares-broad-categories.xls",
     ERS + "/media/5658/distribution-of-additional-1-income-across-broad-expenditure-categories-144-countries-"
     "2005.xls?v=10203",
     "ERS data product file 'Distribution of Additional $1 Income Across Broad Expenditure Categories, 144 "
     "Countries, 2005' (XLS, sheet Table7, last updated 9/4/2013): appendix table 7, marginal shares",
     "usda_tb1929_country_long.csv, usda_tb1929_recompute.csv, usda_tb1929_backsolved.csv"),
    ("dataproduct/marginal-shares-food-subgroups.xls",
     ERS + "/media/5660/distribution-of-additional-1-income-across-food-subgroups-144-countries-2005.xls?v=71083",
     "ERS data product file 'Distribution of Additional $1 Income Across Food Subgroups, 144 Countries, 2005' (XLS, "
     "sheet Table8, last updated 9/4/2013): appendix table 8, conditional marginal shares to 6 decimals",
     "usda_tb1929_country_long.csv, usda_tb1929_recompute.csv, usda_tb1929_backsolved.csv"),
    ("dataproduct/compensated-own-price-broad-real-income-constant.xls",
     ERS + "/media/5654/compensated-own-price-elasticity-for-broad-consumption-groups-144-countries-2005-real-"
     "income-held-constant.xls?v=18425",
     "ERS data product file 'Compensated Own-price Elasticity for Broad Consumption Groups, 144 Countries, 2005 "
     "(real income held constant)' (XLS, sheet Table3, last updated 9/4/2013): appendix table 3, Slutsky",
     "usda_tb1929_country_long.csv, usda_tb1929_recompute.csv"),
    ("dataproduct/compensated-own-price-broad-mui-constant.xls",
     ERS + "/media/5653/compensated-own-price-elasticity-for-broad-consumption-groups-144-countries-2005-marginal-"
     "utility-of-income-held-constant.xls?v=16078",
     "ERS data product file 'Compensated Own-price Elasticity for Broad Consumption Groups, 144 Countries, 2005 "
     "(marginal utility of income held constant)' (XLS, sheet Table2, last updated 9/4/2013): appendix table 2, Frisch",
     "usda_tb1929_country_long.csv, usda_tb1929_recompute.csv"),
    ("dataproduct/uncompensated-own-price-broad.xls",
     ERS + "/media/5655/uncompensated-own-price-elasticity-for-broad-consumption-groups-144-countries-2005.xls"
     "?v=51774",
     "ERS data product file 'Uncompensated Own-price Elasticity for Broad Consumption Groups, 144 Countries, 2005' "
     "(XLS, sheet Table4, last updated 9/4/2013): appendix table 4, Cournot",
     "usda_tb1929_country_long.csv, usda_tb1929_recompute.csv"),
    ("dataproduct/unconditional-own-price-food-subcategories-mui-constant.xls",
     ERS + "/media/5657/unconditional-own-price-elasticity-for-for-subcategories-144-countries-2005-marginal-"
     "utility-of-income-held-constant.xls?v=69790",
     "ERS data product file 'Unconditional Own-price Elasticity for For Subcategories, 144 Countries, 2005 (marginal "
     "utility of income held constant)' [sic] (XLS, sheet Table6, last updated 9/4/2013): appendix table 6, Frisch "
     "for the food subgroups to 6 decimals", "usda_tb1929_country_long.csv, usda_tb1929_recompute.csv"),
    # --- definitions supplement: ERS's companion report on the same 2005 ICP data (same four authors) ------------
    #     TB-1929 never lists what each of its nine groups contains beyond one sentence; the data product's
    #     documentation page cites TB-1937 as a source report. Used for category definitions ONLY: TB-1937 reuses
    #     TB-1929's Table 3 parameters and none of its numbers enter the tidy parameter file.
    ("supplement/pub-details_47611.html", ERS + "/publications/47611",
     "ERS publication page for TB-1937 (Meade, Regmi, Seale and Muhammad, 'New International Evidence on Food "
     "Consumption Patterns: A Focus on Cross-Price Effects Based on 2005 ICP Data', 1/16/2014) as of the pull date",
     "provenance of the definitions supplement (README_usda.md)"),
    ("supplement/tb-1937.pdf", ERS + "/media/8678/tb-1937.pdf?v=54375",
     "TB-1937 full report PDF (January 2014): ERS's companion report on the same 2005 ICP data; states that its "
     "elasticities use TB-1929's Table 3 parameters and defines the nine groups more fully (housing = gross rent, "
     "fuel and power; 'other' = grooming services, jewelry and other miscellaneous; food away from home sat in "
     "recreation in earlier ICP rounds)",
     "usda_tb1929_categories.csv and README_usda.md (category definitions only; no parameters taken from it)"),
]

# ---------------------------------------------------------------------------------------------------------
# 2. Download (skip vendored files; a failure is recorded and not retried unless --retry-failed).
#    After one failure on a host in a run, the remaining files on that host are not attempted in that run.
# ---------------------------------------------------------------------------------------------------------
FAIL_PATH = RAWU / "FETCH_FAILURES.csv"
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


def host_of(url):
    return re.sub(r"^https?://([^/]+)/.*$", r"\1", url)


def fetch_all(downloads):
    fails = read_failures()
    dead_hosts = {}
    for rel, url, what, used in tqdm(downloads, desc="USDA ERS downloads"):
        if (RAWU / rel).exists():
            fails.pop(rel, None)
            continue
        if OFFLINE:
            print("  offline, not vendored:", rel)
            continue
        if rel in fails and not RETRY_FAILED:
            print("  not retried (recorded failure; use --retry-failed):", rel, "|", fails[rel]["error"][:160])
            continue
        host = host_of(url)
        if host in dead_hosts:
            fails[rel] = {"file": rel, "url": url, "date_tried": dt.date.today().isoformat(),
                          "error": f"not attempted: {host} failed earlier in this run ({dead_hosts[host]})"}
            continue
        try:
            fetch(SRC, rel, url, what, used)
            fails.pop(rel, None)
        except Exception as e:
            print("  FAILED:", rel, url, repr(e)[:300])
            fails[rel] = {"file": rel, "url": url, "date_tried": dt.date.today().isoformat(), "error": repr(e)}
            dead_hosts[host] = f"first failure on {rel}"
    write_failures(fails)
    return fails


def sync_manifest(downloads):
    """Keep MANIFEST.csv descriptions in step with DOWNLOADS (date_pulled and hashes come from the file)."""
    mpath = RAWU / "MANIFEST.csv"
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
print("vendored files:", sum((RAWU / d[0]).exists() for d in DOWNLOADS), "of", len(DOWNLOADS),
      "| recorded failures:", len(FAILS))

# ---------------------------------------------------------------------------------------------------------
# 3. Helpers: the checks log, CSV writer, number tokens
#    Every check has a kind: 'consistency' (my parsing and transcription: two extractors agree, PDF and data
#    product agree, counts and orders; the script stops if one fails), 'verification' (recomputing the bulletin's
#    published numbers from the transcribed parameters; a failure is a finding about the source, reported in the
#    README), 'source_finding' (a feature of the source as printed, recorded, never corrected) and 'info'.
# ---------------------------------------------------------------------------------------------------------
import itertools

import pdfplumber
import xlrd
from bs4 import BeautifulSoup
from pypdf import PdfReader

CHECKS = []


def check(name, computed, published, tol, unit, note="", source="", kind="verification"):
    """Log one numeric check. tol is an absolute tolerance in `unit`; published=None records a value, untested."""
    ok, diff = None, None
    if published is not None and computed is not None and not (pd.isna(computed) or pd.isna(published)):
        diff = float(computed) - float(published)
        ok = bool(abs(diff) <= tol + 1e-12)
    CHECKS.append({"kind": kind if ok is not None else "info", "check": name, "computed": computed,
                   "published": published, "diff": diff, "tolerance": tol, "unit": unit, "pass": ok,
                   "source": source, "note": note})
    flag = {True: "ok  ", False: "FAIL", None: "info"}[ok]
    print(f"  [{flag}] {name}: computed={computed} published={published} {unit} {note}"[:260])
    return ok


def check_bool(name, ok, computed="", note="", source="", kind="consistency"):
    """Log a yes/no check (e.g. two lists are identical)."""
    CHECKS.append({"kind": kind, "check": name, "computed": computed, "published": None, "diff": None,
                   "tolerance": None, "unit": "", "pass": bool(ok), "source": source, "note": note})
    print(f"  [{'ok  ' if ok else 'FAIL'}] {name}: {computed} {note}"[:260])
    return ok


def finding(name, detail, source=""):
    """Record a feature of the source as printed (not a test; nothing is corrected)."""
    CHECKS.append({"kind": "source_finding", "check": name, "computed": detail, "published": None, "diff": None,
                   "tolerance": None, "unit": "", "pass": None, "source": source,
                   "note": "as published (recorded, not corrected)"})
    print(f"  [find] {name}: {detail}"[:260])


def write_csv(df, name):
    path = TIDY / name
    df.to_csv(path, index=False, lineterminator="\n")
    print(f"  wrote {path.relative_to(REPO)}: {len(df):,} rows x {df.shape[1]} cols")
    return path


NUM = r"-?\d*\.\d+"
H = 0.0005                     # half a unit in the third decimal: the printed precision of every parameter


def norm(s):
    """Unicode minus/dashes and non-breaking spaces to ASCII, so number tokens parse the same from every extractor."""
    return s.replace("−", "-").replace("–", "-").replace("\xa0", " ")


def squash(s):
    """Letters and digits only, lower case: for matching names and quotes across line breaks and hyphenation."""
    return re.sub(r"[^a-z0-9]", "", s.lower())


def printed_page(text, footer):
    """The publication's own page label: the line just above its running footer (arabic in the body, roman in front)."""
    lines = [ln.strip() for ln in text.splitlines()]
    for k in range(1, len(lines)):
        if lines[k].startswith(footer) and re.fullmatch(r"\d+|[ivx]+", lines[k - 1]):
            return lines[k - 1]
    return ""


# ---------------------------------------------------------------------------------------------------------
# 4. The bulletin PDF: page text from two independent extractors (pdfplumber, pypdf), printed page labels
#    (printed page = PDF page - 6 in the body), the revision note
# ---------------------------------------------------------------------------------------------------------
PDF = RAWU / "report/tb-1929.pdf"
FOOTER = "International Evidence on Food Consumption Patterns: An Update Using 2005 International Comparison"
with pdfplumber.open(PDF) as pdf:
    META = dict(pdf.metadata)
    PAGES = [norm(p.extract_text() or "") for p in tqdm(pdf.pages, desc="TB-1929 pages (pdfplumber)")]
    # body column only (x < 400 pt; side notes sit in the right margin and interleave with body lines in PAGES)
    PAGES_BODY = [norm(p.crop((0, 0, 400, p.height)).extract_text() or "") for p in tqdm(pdf.pages, desc="TB-1929 body column")]
    # right-hand margin of PDF p. 17 (printed p. 11): footnote 11, the list of outlier countries
    p17 = pdf.pages[16]
    MARGIN_P17 = norm(p17.crop((400, 0, p17.width, p17.height)).extract_text() or "")
PAGES_PYPDF = [norm(pg.extract_text() or "") for pg in PdfReader(PDF).pages]
PRINTED = {i + 1: printed_page(t, FOOTER) for i, t in enumerate(PAGES)}
print("TB-1929 PDF:", len(PAGES), "pages | created", META.get("CreationDate"), "| modified", META.get("ModDate"))


def pdf_page_of(pattern, pages=PAGES):
    hits = [i + 1 for i, t in enumerate(pages) if re.search(pattern, t, flags=re.M)]
    if len(hits) != 1:
        raise RuntimeError(f"pattern {pattern!r} found on PDF pages {hits}, expected exactly one")
    return hits[0]


check_bool("printed page labels: body pages are PDF page - 6 (pp. 1-53)",
           all(PRINTED[i] == str(i - 6) for i in range(7, 60)), f"PDF 7 -> '{PRINTED[7]}', PDF 59 -> '{PRINTED[59]}'")
REVISION = re.search(r"This report, originally released in March 2011, was revised in February 2013[^.]*\.[^.]*\.",
                     " ".join(PAGES[2].split()))
check_bool("bulletin carries the February 2013 revision note", REVISION is not None,
           REVISION.group(0) if REVISION else "", source="tb-1929.pdf abstract (PDF p. 3, printed p. i)")
check_bool("PDF metadata creation date is the 2013 revision", str(META.get("CreationDate", "")).startswith("D:2013"),
           META.get("CreationDate"), source="tb-1929.pdf metadata")

# ---------------------------------------------------------------------------------------------------------
# 5. Tables 3 and 4: the estimated parameters. Stage one: Florida-PI model over nine broad groups (Table 3,
#    printed p. 12). Stage two: conditional Florida-Slutsky model over eight food subgroups (Table 4, printed
#    p. 16). Parsed from both extractors; they must agree exactly (and were compared with the page images).
# ---------------------------------------------------------------------------------------------------------
STAGE1_CATS = ["Food, beverage, and tobacco", "Clothing and footwear", "Housing and utilities",
               "Furnishing, household equipment, and maintenance", "Medical and health",
               "Transportation and communication", "Recreation and culture", "Education", "Other"]
STAGE2_CATS = ["Cereals", "Meat", "Fish", "Dairy and eggs", "Oils and fat", "Fruit and vegetables", "Food other",
               "Beverages and tobacco"]
STARS = {"": "no significance marker", "*": "* = significant at the 0.01 level (table note)",
         "**": "** = significant at the 0.05 level (table note)"}


def parse_param_table(text, table_no):
    lines = [ln.strip() for ln in text.splitlines()]
    i0 = lines.index(f"Table {table_no}")
    rows, section = [], None
    names = {3: {"beta": "beta", "alpha": "alpha"}, 4: {"beta": "beta_star", "alpha": "alpha_star"}}[table_no]
    for ln in lines[i0 + 2:]:
        if re.match(r"^[1a]Comoros", ln):
            break
        if ln.startswith("Beta"):
            section = names["beta"]
            continue
        if ln.startswith("Alpha"):
            section = names["alpha"]
            continue
        if ln.startswith("Slutsky own-price effects"):
            section = "pi_star_ii"
            continue
        if ln.startswith("Heteroskedasticity"):
            section = "hetero"
            continue
        m = re.match(rf"^(?P<label>.+?)\s+(?P<val>{NUM})\s+(?P<se>{NUM})(?P<stars>\**)$", ln)
        if not m:
            continue
        label = m["label"].strip()
        if label.startswith("Income flexibility"):
            cat, par = "(all)", "phi"
        elif section == "hetero":
            cat, par = "(all)", label
        else:
            cat, par = label, section
        rows.append({"category": cat, "parameter": par, "value": m["val"], "se": m["se"], "stars": m["stars"]})
    return lines[i0 + 1], rows


P_T3 = pdf_page_of(r"^Table 3\s*$")
P_T4 = pdf_page_of(r"^Table 4\s*$")
T3_TITLE, T3 = parse_param_table(PAGES[P_T3 - 1], 3)
T4_TITLE, T4 = parse_param_table(PAGES[P_T4 - 1], 4)
for tno, rows_a, pno in [(3, T3, P_T3), (4, T4, P_T4)]:
    _, rows_b = parse_param_table(PAGES_PYPDF[pno - 1], tno)
    check_bool(f"Table {tno}: pdfplumber and pypdf transcriptions identical", rows_a == rows_b,
               f"{len(rows_a)} rows (pdfplumber) vs {len(rows_b)} rows (pypdf)", source=f"tb-1929.pdf PDF p. {pno}")
check_bool("Table 3 rows: phi + 9 beta + 9 alpha + K2 + K3", len(T3) == 21 and
           [r["category"] for r in T3 if r["parameter"] == "beta"] == STAGE1_CATS and
           [r["category"] for r in T3 if r["parameter"] == "alpha"] == STAGE1_CATS, f"{len(T3)} rows; '{T3_TITLE}'")
check_bool("Table 4 rows: 8 beta* + 8 alpha* + 8 pi*_ii + K2 + K3", len(T4) == 26 and
           all([r["category"] for r in T4 if r["parameter"] == p] == STAGE2_CATS
               for p in ["beta_star", "alpha_star", "pi_star_ii"]), f"{len(T4)} rows; '{T4_TITLE}'")


def pval(rows, par, cat="(all)"):
    return float(next(r["value"] for r in rows if r["parameter"] == par and r["category"] == cat))


PHI = pval(T3, "phi")
A1 = np.array([pval(T3, "alpha", c) for c in STAGE1_CATS])
B1 = np.array([pval(T3, "beta", c) for c in STAGE1_CATS])
A2 = np.array([pval(T4, "alpha_star", c) for c in STAGE2_CATS])
B2 = np.array([pval(T4, "beta_star", c) for c in STAGE2_CATS])
check("Table 3: sum of alpha (adding-up, eq. 2: = 1)", round(A1.sum(), 6), 1.0, 4.5 * H * 2, "share",
      "nine printed alphas, 3 decimals each", f"Table 3, PDF p. {P_T3}")
check("Table 3: sum of beta (adding-up, eq. 2: = 0)", round(B1.sum(), 6), 0.0, 4.5 * H * 2, "share",
      "nine printed betas", f"Table 3, PDF p. {P_T3}")
check("Table 4: sum of alpha* (adding-up: = 1)", round(A2.sum(), 6), 1.0, 4 * H * 2, "share",
      "eight printed alpha*: they sum to 1.001 (rounding)", f"Table 4, PDF p. {P_T4}")
check("Table 4: sum of beta* (adding-up: = 0)", round(B2.sum(), 6), 0.0, 4 * H * 2, "share",
      "eight printed beta*: they sum to +0.001 (rounding)", f"Table 4, PDF p. {P_T4}")
for rows, tno in [(T3, 3), (T4, 4)]:
    for r in rows:
        v, s = abs(float(r["value"])), float(r["se"])
        t = v / s if s else np.inf
        if (r["stars"] == "*" and t < 2.576) or (r["stars"] == "**" and t < 1.96) or (r["stars"] == "" and t >= 2.576):
            finding(f"Table {tno}: significance marker inconsistent with |value/se|, {r['parameter']} {r['category']}",
                    f"value {r['value']}, se {r['se']}, marker '{r['stars']}', |t| = {t:.2f} at printed precision",
                    f"Table {tno}")
finding("Table 4 note cites 'equations 10a-10c'", "the bulletin numbers the conditional model as a single equation "
        "(10); there are no equations 10a-10c", f"Table 4 note, PDF p. {P_T4}")

# Outlier countries (footnote 11, printed p. 11): estimated without them (125 countries), elasticities for all 144.
OUT_TXT = " ".join(MARGIN_P17.split()).replace("Gam- bia", "Gambia")
m = re.search(r"Outlier countries include (.+?)\.", OUT_TXT)
OUTLIERS_RAW = [x.strip() for x in re.split(r",\s*|\s+and\s+", m.group(1))] if m else []
OUTLIER_NAME = {"Democratic Republic of Congo": "Congo, Dem. Rep.", "Gambia": "Gambia, The",
                "Syria": "Syrian Arab Republic"}
OUTLIERS = [OUTLIER_NAME.get(x, x) for x in OUTLIERS_RAW]
check_bool("footnote 11: 19 outlier countries listed (text: 'This procedure resulted in 19 outlier countries')",
           len(OUTLIERS) == 19 and "resulted in 19 outlier" in " ".join(PAGES[16].split()), "; ".join(OUTLIERS_RAW),
           source="tb-1929.pdf printed p. 11, margin")

# ---------------------------------------------------------------------------------------------------------
# 6. Table 2 (printed p. 5): average budget shares by income group (broad groups; food subgroups as shares of food)
# ---------------------------------------------------------------------------------------------------------
P_T2 = pdf_page_of(r"^Table 2\s*$")
T2_LINES = [ln.strip() for ln in PAGES[P_T2 - 1].splitlines()]
T2_ROWS = [ln for ln in T2_LINES[T2_LINES.index("Table 2"):] if re.match(rf"^income(\s+{NUM})+$", ln)]
check_bool("Table 2: six income-group rows parsed (3 broad, 3 food)", len(T2_ROWS) == 6,
           f"{len(T2_ROWS)} rows", source=f"Table 2, PDF p. {P_T2}")
GROUPS = ["low", "middle", "high"]
T2 = []
for k, ln in enumerate(T2_ROWS):
    vals = [float(x) for x in ln.split()[1:]]
    cats = STAGE1_CATS if k < 3 else STAGE2_CATS
    assert len(vals) == len(cats), ln
    for c, v in zip(cats, vals):
        T2.append({"source_table": "Table 2", "printed_page": PRINTED[P_T2], "income_group": GROUPS[k % 3],
                   "stage": 1 if k < 3 else 2, "category": c,
                   "measure": "budget_share" if k < 3 else "conditional_budget_share", "value": v})
T2 = pd.DataFrame(T2)
for g in GROUPS:
    for st in (1, 2):
        s = T2[(T2.income_group == g) & (T2.stage == st)].value.sum()
        check(f"Table 2: {g}-income {'broad' if st == 1 else 'food-subgroup'} shares sum to 1", round(s, 6), 1.0,
              (9 if st == 1 else 8) * H, "share", "printed shares, 3 decimals each", f"Table 2, PDF p. {P_T2}",
              kind="consistency")
X9 = xlrd.open_workbook(RAWU / "dataproduct/budget-shares-broad-aggregates-conditional-food.xls").sheet_by_index(0)
X9_VALS = [float(X9.cell_value(r, c)) for r in (2, 3, 4) for c in range(1, 10)] + \
          [float(X9.cell_value(r, c)) for r in (7, 8, 9) for c in range(1, 9)]
check_bool("Table 2 = data product 'Budget Shares for Broad Aggregates and Conditional Budget Shares' (all 51 cells)",
           X9_VALS == T2.value.tolist(), f"sheet '{X9.name}'", source="budget-shares-broad-aggregates-conditional-food.xls")

# ---------------------------------------------------------------------------------------------------------
# 7. Appendix tables 1-8 (country by country) from the PDF, and the same tables from the data product XLS
# ---------------------------------------------------------------------------------------------------------
APPX = {  # appendix table -> (stage, measure, leading per-capita columns, equation, data product file)
    1: (1, "income_elasticity", [], "5", "dataproduct/income-elasticities-broad-categories.xls"),
    2: (1, "frisch_own_price_elasticity", [], "6", "dataproduct/compensated-own-price-broad-mui-constant.xls"),
    3: (1, "slutsky_own_price_elasticity", [], "7", "dataproduct/compensated-own-price-broad-real-income-constant.xls"),
    4: (1, "cournot_own_price_elasticity", [], "8", "dataproduct/uncompensated-own-price-broad.xls"),
    5: (2, "unconditional_income_elasticity", ["per_capita_food"], "11",
        "dataproduct/income-elasticities-food-subcategories.xls"),
    6: (2, "unconditional_frisch_own_price_elasticity", ["per_capita_food"], "12",
        "dataproduct/unconditional-own-price-food-subcategories-mui-constant.xls"),
    7: (1, "marginal_share", ["per_capita_income"], "3", "dataproduct/marginal-shares-broad-categories.xls"),
    8: (2, "conditional_marginal_share", ["per_capita_income", "per_capita_food"], "3, conditional form",
        "dataproduct/marginal-shares-food-subgroups.xls"),
}
TITLE_KEY = {1: "Income elasticities for aggregate", 2: "Frisch own-price elasticities for aggregate",
             3: "Slutsky own-price elasticities for aggregate", 4: "Cournot own-price elasticities for aggregate",
             5: "Unconditional expenditure elasticities of demand for food", 6: "Unconditional Frisch own-price",
             7: "Marginal shares for aggregate", 8: "Conditional marginal shares for food"}


def parse_appendix(pages):
    rows, titles, group = [], {}, {}
    for pno, text in enumerate(pages, start=1):
        lines = [ln.strip() for ln in text.splitlines()]
        hdr = [k for k, ln in enumerate(lines) if re.fullmatch(r"Appendix table \d+", ln)]
        if not hdr:
            continue
        k0 = hdr[0]
        tno = int(lines[k0].split()[-1])
        titles.setdefault(tno, lines[k0 + 1])
        # the column header's last line ends with "Other" (broad groups) or "& tobacco" (food subgroups)
        kh = next(k for k in range(k0 + 2, len(lines)) if re.search(r"(Other|& tobacco)$", lines[k]))
        pending = ""
        for ln in lines[kh + 1:]:
            if ln.startswith("Countries are reported") or ln.startswith("---continued"):
                break
            g = re.fullmatch(r"(Low|Middle|High)-income countries:", ln)
            if g:
                group[tno], pending = g.group(1).lower(), ""
                continue
            toks = ln.split()
            j = len(toks)
            while j > 0 and re.fullmatch(NUM + r"[ab]?", toks[j - 1]):
                j -= 1
            if j == len(toks):
                pending = (pending + " " + ln).strip()
                continue
            name = (pending + " " + " ".join(toks[:j])).strip()
            pending = ""
            kind = "average" if re.search(r"average$", name, flags=re.I) else "country"
            rows.append({"table": tno, "pdf_page": pno, "printed_page": PRINTED[pno], "income_group": group[tno],
                         "name": name, "kind": kind, "tokens": toks[j:]})
    return rows, titles


APPX_PDF_ROWS, APPX_TITLES = parse_appendix(PAGES)
for t, (st, meas, lead, eq, xls) in APPX.items():
    check_bool(f"appendix table {t} title", APPX_TITLES.get(t, "").startswith(TITLE_KEY[t]),
               APPX_TITLES.get(t, "(missing)"), source="tb-1929.pdf")
    rs = [r for r in APPX_PDF_ROWS if r["table"] == t]
    ncol = len(lead) + (9 if st == 1 else 8)
    check_bool(f"appendix table {t}: 144 countries + 3 group averages, {ncol} numbers per row",
               sum(r["kind"] == "country" for r in rs) == 144 and sum(r["kind"] == "average" for r in rs) == 3
               and all(len(r["tokens"]) == ncol for r in rs),
               f"{sum(r['kind'] == 'country' for r in rs)} countries, {sum(r['kind'] == 'average' for r in rs)} "
               f"averages, PDF pp. {min(r['pdf_page'] for r in rs)}-{max(r['pdf_page'] for r in rs)}")


def name_match(raw, canon):
    """'exact' (after joining a hyphenated line break), 'wrapped' (the PDF line holds only the head of the name, or
    the tail of the previous row's name in front of this one: a layout artifact), or '' (no match)."""
    r, c = squash(re.sub(r"(\w)- (\w)", r"\1\2", raw)), squash(canon)
    if r == c:
        return "exact"
    if r and (c.startswith(r) or r.endswith(c)):
        return "wrapped"
    return ""


# Appendix table 1 is the reference list; its names come out of the PDF whole. Every other table is matched to it by
# position, and each row's name must match exactly or as one of the wrapped layouts listed in the checks.
COUNTRIES = [r["name"] for r in APPX_PDF_ROWS if r["table"] == 1 and r["kind"] == "country"]
for t in range(1, 9):
    rs = [r for r in APPX_PDF_ROWS if r["table"] == t and r["kind"] == "country"]
    kinds = [name_match(r["name"], c) for r, c in zip(rs, COUNTRIES)]
    wrapped = [f"'{r['name']}' = {c}" for r, c, k in zip(rs, COUNTRIES, kinds) if k == "wrapped"]
    check_bool(f"appendix table {t}: same 144 countries in the same order as appendix table 1",
               len(rs) == 144 and all(kinds) and len(wrapped) <= 2,
               f"{kinds.count('exact')} exact, {len(wrapped)} wrapped by the layout"
               + (f": {'; '.join(wrapped)}" if wrapped else ""), source=f"appendix table {t}")
    for r, c in zip(rs, COUNTRIES):
        r["name_pdf"], r["name"] = r["name"], c
GROUP_OF = {r["name"]: r["income_group"] for r in APPX_PDF_ROWS if r["table"] == 1 and r["kind"] == "country"}
for t in range(2, 9):
    check_bool(f"appendix table {t}: same income-group assignment as appendix table 1",
               all(GROUP_OF[r["name"]] == r["income_group"] for r in APPX_PDF_ROWS
                   if r["table"] == t and r["kind"] == "country"))
check_bool("every outlier in footnote 11 is one of the 144 countries", all(c in COUNTRIES for c in OUTLIERS),
           f"{sum(c in COUNTRIES for c in OUTLIERS)} of {len(OUTLIERS)}")


def read_xls(rel):
    sh = xlrd.open_workbook(RAWU / rel).sheet_by_index(0)
    header = [str(sh.cell_value(1, c)).strip() for c in range(sh.ncols)]
    rows, notes = [], []
    for r in range(2, sh.nrows):
        vals = [sh.cell_value(r, c) for c in range(sh.ncols)]
        if all(str(v).strip() == "" for v in vals):
            continue
        if all(str(v).strip() == "" for v in vals[1:]):
            notes.append(str(vals[0]).strip())
            continue
        rows.append(vals)
    return {"sheet": sh.name, "title": str(sh.cell_value(0, 0)).strip(), "header": header, "rows": rows,
            "notes": notes}


def xls_num(v):
    """A numeric cell, or a text cell such as '1.573a' / ' -0.000b' (value plus the table's footnote letter)."""
    if isinstance(v, float):
        return v, ""
    m = re.fullmatch(r"(-?\d*\.\d+)([ab]?)", str(v).strip())
    if not m:
        raise ValueError(f"unparseable cell {v!r}")
    return float(m.group(1)), m.group(2)


XLS = {t: read_xls(APPX[t][4]) for t in APPX}
for t, x in XLS.items():
    names = [str(r[0]).strip() for r in x["rows"]]
    check_bool(f"data product {x['sheet']} (appendix table {t}): same 144 countries in the same order as the PDF",
               names == COUNTRIES, f"{len(names)} rows; title '{x['title']}'", source=APPX[t][4])

# Long table of every published country cell: the data product value (full precision) beside the PDF value.
LONG = []
for t, (st, meas, lead, eq, rel) in APPX.items():
    cats = STAGE1_CATS if st == 1 else STAGE2_CATS
    pdf_rows = [r for r in APPX_PDF_ROWS if r["table"] == t and r["kind"] == "country"]
    xlead = 2 if t == 8 else 1                             # data product: country, one or two per-capita columns
    for k, (prow, xrow) in enumerate(zip(pdf_rows, XLS[t]["rows"])):
        xvals = [xls_num(v) for v in xrow[1 + xlead:]]
        pvals = [(float(re.sub("[ab]$", "", s)), s[-1] if s[-1] in "ab" else "") for s in prow["tokens"][len(lead):]]
        assert len(xvals) == len(cats) == len(pvals), (t, prow["name"])
        for c, (xv, xf), (pv, pf) in zip(cats, xvals, pvals):
            LONG.append({"appendix_table": t, "measure": meas, "equation": eq, "stage": st, "category": c,
                         "country": prow["name"], "country_order": k + 1, "income_group": prow["income_group"],
                         "value": xv, "flag": xf, "value_pdf": pv, "flag_pdf": pf, "pdf_page": prow["pdf_page"],
                         "printed_page": prow["printed_page"], "xls_file": rel})
LONG = pd.DataFrame(LONG)

# Per-capita columns: real per capita income and real per capita food spending, both relative to the US (= 1).
PCI = {str(r[0]).strip(): float(r[1]) for r in XLS[1]["rows"]}
PCF = {str(r[0]).strip(): float(r[1]) for r in XLS[5]["rows"]}
for t in (2, 3, 4):
    check_bool(f"per capita income identical in data product tables 1 and {t} (14 significant digits)",
               all(float(r[1]) == PCI[str(r[0]).strip()] for r in XLS[t]["rows"]))
check_bool("per capita food spending identical in data product tables 5, 6 and 8",
           all(float(r[1]) == PCF[str(r[0]).strip()] for r in XLS[6]["rows"]) and
           all(float(r[2]) == PCF[str(r[0]).strip()] for r in XLS[8]["rows"]))
gap7 = max(abs(float(r[1]) - PCI[str(r[0]).strip()]) for r in XLS[7]["rows"])
gap8 = max(abs(float(r[1]) - PCI[str(r[0]).strip()]) for r in XLS[8]["rows"])
check("per capita income: data product table 7 (3 dec.) vs tables 1-4 (14 digits), max abs gap", gap7, 0.0, H,
      "ratio to US", "table 7 rounds the same numbers", "data product", kind="consistency")
check("per capita income: data product table 8 (6 dec.) vs tables 1-4, max abs gap", gap8, 0.0, 5e-7,
      "ratio to US", "table 8 rounds the same numbers", "data product", kind="consistency")
check("per capita income of the United States (the normalisation, Q = 1)", PCI["United States"], 1.0, 0.0,
      "ratio to US", "TB-1937 p. 12: real per capita income 'relative to that of the United States normalized to "
      "equal 1'", "data product table 1", kind="consistency")
for t, col in [(7, 0), (8, 0), (8, 1), (5, 0), (6, 0)]:
    lead = APPX[t][2]
    pdf_pc = {r["name"]: float(r["tokens"][col]) for r in APPX_PDF_ROWS if r["table"] == t and r["kind"] == "country"}
    full = PCI if lead[col] == "per_capita_income" else PCF
    g = max(abs(pdf_pc[c] - full[c]) for c in COUNTRIES)
    check(f"PDF appendix table {t} column '{lead[col]}' vs data product (rounded to 3 dec.), max abs gap", round(g, 9),
          0.0, H + 1e-9, "ratio to US", "", f"appendix table {t}", kind="consistency")
bad_rank = [c for a, c in zip(COUNTRIES, COUNTRIES[1:]) if PCI[c] < PCI[a]]
check_bool("countries are listed in ascending per capita income (as the tables state)", not bad_rank,
           f"{len(bad_rank)} out of order: {bad_rank[:5]}")
thr = {c: ("low" if PCI[c] < 0.15 else "middle" if PCI[c] < 0.45 else "high") for c in COUNTRIES}
mis = [c for c in COUNTRIES if thr[c] != GROUP_OF[c]]
check_bool("income groups match the stated thresholds (<15%, 15-45%, >=45% of US per capita income)", not mis,
           f"{len(mis)} mismatches: {[(c, round(PCI[c], 4), GROUP_OF[c]) for c in mis]}",
           source="text p. 4; appendix group headers")

# PDF (3 decimals) vs data product (3 or 6 decimals): every cell and every footnote letter. The two ERS releases
# differ in exactly the cells listed here (found 2026-11-02); the check fails if any other cell differs or these
# stop differing. Both values are kept in the tidy file; section 8 shows which one the model gives.
KNOWN_DIFFS = {
    (5, "Zambia", "Food other"): "flag only: the data product marks 1.672 'a' (computed from the actual share); the "
                                 "PDF prints 1.672 without a mark",
    (6, "Spain", "Cereals"): "the data product keeps the raw positive Frisch value; the PDF prints 0.000b (set to zero)",
    (6, "Spain", "Oils and fat"): "the data product keeps the raw positive Frisch value; the PDF prints 0.000b",
    (6, "Italy", "Cereals"): "the data product keeps the raw positive Frisch value; the PDF prints 0.000b",
}
LONG["pdf_minus_xls"] = LONG.value_pdf - LONG.value
LONG["release_note"] = [KNOWN_DIFFS.get((t, c, g), "") for t, c, g in
                        zip(LONG.appendix_table, LONG.country, LONG.category)]
for t in APPX:
    d = LONG[LONG.appendix_table == t]
    six = t in (5, 6, 8)
    tol = (H + 1e-9) if six else 0.0
    bad = d[(d.pdf_minus_xls.abs() > tol) | (d.flag != d.flag_pdf)]
    known = {k for k in KNOWN_DIFFS if k[0] == t}
    found = set(zip(bad.appendix_table, bad.country, bad.category))
    rest = d[d.release_note == ""]
    check(f"appendix table {t}: PDF vs data product, max abs gap over the {len(rest)} cells not listed as release "
          f"differences", round(rest.pdf_minus_xls.abs().max(), 9), 0.0, tol, "elasticity or share",
          "data product carries 6 decimals; PDF rounds to 3" if six else "both carry 3 decimals",
          f"appendix table {t} vs {APPX[t][4]}", kind="consistency")
    check_bool(f"appendix table {t}: cells where PDF and data product differ are exactly the listed ones",
               found == known, f"{len(found)} differing: {sorted(found)}; flagged cells: data product "
               f"{(d.flag != '').sum()}, PDF {(d.flag_pdf != '').sum()}")
    for k in sorted(known):
        r = d[(d.country == k[1]) & (d.category == k[2])].iloc[0]
        finding(f"release difference, appendix table {t}, {k[1]}, {k[2]}",
                f"data product {r.value} '{r.flag}' vs PDF {r.value_pdf} '{r.flag_pdf}': {KNOWN_DIFFS[k]}",
                f"{APPX[t][4]} vs tb-1929.pdf PDF p. {r.pdf_page}")

# ---------------------------------------------------------------------------------------------------------
# 8. Verification: recompute every published country cell from the transcribed parameters (Tables 3 and 4) and
#    the per capita incomes ERS reports (data product: income to 14 significant digits, food spending to 6).
#    Stage one at geometric mean prices: w = alpha + beta q (eq. 4b), theta = w + beta (eq. 3), eta = 1 + beta/w
#    (eq. 5), F = phi eta (eq. 6), S = F (1 - w - beta) (eq. 7), C = S - (w + beta) (eq. 8), with
#    q = ln(per capita income relative to the US). Stage two: w* = alpha* + beta* qF, theta* = w* + beta*,
#    eta* = 1 + beta*/w*, eta_U = eta_F eta* (eq. 11), F_u = phi eta_F eta* (eq. 12), qF = ln(per capita food
#    spending relative to the US), eta_F = the stage-one food elasticity (eq. 5).
#    Rounding band: each parameter is printed to 3 decimals, so the recomputation is repeated with every parameter
#    at its printed value and +-0.0005 (3 points each); the published cell must lie in [min, max] widened by its
#    own half unit of rounding. phi is run twice: as printed in Table 3, and as implied by the published Frisch
#    tables (phi_hat = F/eta, which is constant across cells; see the checks), because the two differ.
# ---------------------------------------------------------------------------------------------------------
Q = np.array([PCI[c] for c in COUNTRIES])
QF = np.array([PCF[c] for c in COUNTRIES])
q, qf = np.log(Q), np.log(QF)


def stage1(alpha, beta, phi, qv):
    w = alpha + beta * qv
    th = w + beta
    eta = th / w
    F = phi * eta
    S = F * (1 - th)
    return {"w": w, 7: th, 1: eta, 2: F, 3: S, 4: S - th}


def stage2(aF, bF, a, b, phi, qv, qfv):
    wF = aF + bF * qv
    etaF = 1 + bF / wF
    w = a + b * qfv
    eta_c = 1 + b / w
    return {"w": w, "etaF": etaF, "eta_c": eta_c, 8: w + b, 5: etaF * eta_c, 6: phi * etaF * eta_c}


def pub(t, cat):
    """Published cells of one table and category in country order: data product value and flag, PDF value and flag."""
    d = LONG[(LONG.appendix_table == t) & (LONG.category == cat)].sort_values("country_order")
    assert list(d.country) == COUNTRIES
    return d.value.to_numpy(), d.flag.to_numpy(), d.value_pdf.to_numpy(), d.flag_pdf.to_numpy()


# phi implied by the published tables: F_u / eta_U cell by cell in the 6-decimal stage-two tables (eq. 12)
_F6 = LONG[(LONG.appendix_table == 6) & (LONG.flag_pdf != "b") & (LONG.release_note == "")].set_index(
    ["country", "category"]).value
_E5 = LONG[LONG.appendix_table == 5].set_index(["country", "category"]).value.reindex(_F6.index)
PHI_RATIOS = (_F6 / _E5)[_E5.abs() > 0.05]
PHI_HAT = round(float(PHI_RATIOS.median()), 5)
HPHI = 0.0001                  # band for phi_hat (the 6-decimal ratios scatter by less than +-0.0004)

G3 = np.array(list(itertools.product([-H, 0.0, H], repeat=3)))
G5 = np.array(list(itertools.product([-H, 0.0, H], repeat=5)))
G3h = G3 * np.array([1, 1, HPHI / H])
G5h = G5 * np.array([1, 1, 1, 1, HPHI / H])
REC = []


def rec_rows(t, stage, cat, point, band, pointh, bandh, w_impl):
    v, f, vp, fp = pub(t, cat)
    for k, c in enumerate(COUNTRIES):
        REC.append({"appendix_table": t, "measure": APPX[t][1], "stage": stage, "category": cat, "country": c,
                    "country_order": k + 1, "income_group": GROUP_OF[c], "per_capita_income_rel_us": Q[k],
                    "per_capita_food_rel_us": QF[k] if stage == 2 else np.nan, "w_fitted": point["w"][k],
                    "published": v[k], "flag": f[k], "published_pdf": vp[k], "flag_pdf": fp[k],
                    "recomputed": point[t][k], "band_lo": band[t][:, k].min(), "band_hi": band[t][:, k].max(),
                    "recomputed_phi_hat": pointh[t][k], "band_lo_phi_hat": bandh[t][:, k].min(),
                    "band_hi_phi_hat": bandh[t][:, k].max(), "w_implied_actual": w_impl[k]})


for i, cat in enumerate(tqdm(STAGE1_CATS, desc="recompute stage one")):
    args = (A1[i] + G3[:, [0]], B1[i] + G3[:, [1]])
    point, band = stage1(A1[i], B1[i], PHI, q), stage1(*args, PHI + G3[:, [2]], q[None, :])
    pointh, bandh = stage1(A1[i], B1[i], PHI_HAT, q), stage1(A1[i] + G3h[:, [0]], B1[i] + G3h[:, [1]],
                                                             PHI_HAT + G3h[:, [2]], q[None, :])
    eta_pub, eta_flag = pub(1, cat)[0], pub(1, cat)[1]
    w_impl = np.where(eta_flag == "a", B1[i] / (eta_pub - 1), np.nan)   # actual share behind an 'a' cell
    for t in (1, 2, 3, 4, 7):
        rec_rows(t, 1, cat, point, band, pointh, bandh, w_impl)
for i, cat in enumerate(tqdm(STAGE2_CATS, desc="recompute stage two")):
    point = stage2(A1[0], B1[0], A2[i], B2[i], PHI, q, qf)
    band = stage2(A1[0] + G5[:, [0]], B1[0] + G5[:, [1]], A2[i] + G5[:, [2]], B2[i] + G5[:, [3]], PHI + G5[:, [4]],
                  q[None, :], qf[None, :])
    pointh = stage2(A1[0], B1[0], A2[i], B2[i], PHI_HAT, q, qf)
    bandh = stage2(A1[0] + G5h[:, [0]], B1[0] + G5h[:, [1]], A2[i] + G5h[:, [2]], B2[i] + G5h[:, [3]],
                   PHI_HAT + G5h[:, [4]], q[None, :], qf[None, :])
    v5, f5, _, fp5 = pub(5, cat)
    w_impl = np.where((f5 == "a") | (fp5 == "a"), B2[i] / (v5 / point["etaF"] - 1), np.nan)
    for t in (5, 6, 8):
        rec_rows(t, 2, cat, point, band, pointh, bandh, w_impl)
REC = pd.DataFrame(REC)
REC["half_unit_published"] = np.where(REC.appendix_table.isin([5, 6, 8]), 5e-7, H)
REC["gap"] = REC.recomputed - REC.published
REC["gap_phi_hat"] = REC.recomputed_phi_hat - REC.published
REC["within_band"] = ((REC.published >= REC.band_lo - REC.half_unit_published - 1e-12) &
                      (REC.published <= REC.band_hi + REC.half_unit_published + 1e-12))
REC["within_band_phi_hat"] = ((REC.published >= REC.band_lo_phi_hat - REC.half_unit_published - 1e-12) &
                              (REC.published <= REC.band_hi_phi_hat + REC.half_unit_published + 1e-12))
REC["status"] = np.select(
    [(REC.flag == "a") | (REC.flag_pdf == "a"), REC.flag_pdf == "b"],
    ["actual-share cell ('a'): not recomputable from TB-1929, which does not publish actual country shares",
     "set to zero by ERS ('b'): recomputed is the positive Frisch value it replaced"],
    "recomputed from the transcribed parameters")
TESTED = REC[REC.status == "recomputed from the transcribed parameters"]
print("verification: recomputed", len(TESTED), "of", len(REC), "published cells")
check("phi implied by the published Frisch tables: median of F_u / eta_U over the 6-decimal stage-two cells",
      PHI_HAT, PHI, H, "", f"{len(PHI_RATIOS)} cells, range {PHI_RATIOS.min():.5f} to {PHI_RATIOS.max():.5f}; "
      f"Table 3 prints {PHI} (se 0.034)", "appendix tables 5-6 (data product)")
_r1 = (TESTED[TESTED.appendix_table == 2].set_index(["country", "category"]).published /
       TESTED[TESTED.appendix_table == 1].set_index(["country", "category"]).published).dropna()
check("phi implied by the published stage-one Frisch table: median of F / eta (3-decimal cells)",
      round(float(_r1.median()), 5), PHI, H, "", f"{len(_r1)} cells, interquartile range {_r1.quantile(.25):.5f} to "
      f"{_r1.quantile(.75):.5f}", "appendix tables 1-2 (data product)")
for (t, cat), d in TESTED.groupby(["appendix_table", "category"], sort=False):
    j = d.gap.abs().idxmax()
    uses_phi = t in (2, 3, 4, 6)
    check_bool(f"recompute appendix table {t} ({APPX[t][1]}), {cat}"
               + (f": inside the rounding band with Table 3's phi = {PHI}" if uses_phi else ": inside the rounding band"),
               d.within_band.all(), f"{int(d.within_band.sum())}/{len(d)} inside; max |gap| {abs(d.gap[j]):.6f} at "
               f"{d.country[j]} (published {d.published[j]}, recomputed {d.recomputed[j]:.6f})",
               source=f"Table 3{' and 4' if APPX[t][0] == 2 else ''}; appendix table {t}", kind="verification")
    if uses_phi:
        jh = d.gap_phi_hat.abs().idxmax()
        check_bool(f"recompute appendix table {t} ({APPX[t][1]}), {cat}: inside the rounding band with phi_hat = "
                   f"{PHI_HAT}", d.within_band_phi_hat.all(), f"{int(d.within_band_phi_hat.sum())}/{len(d)} inside; "
                   f"max |gap| {abs(d.gap_phi_hat[jh]):.6f} at {d.country[jh]}",
                   source=f"appendix table {t}" + (" (phi_hat is taken from tables 5-6, so this one is circular)"
                                                   if t == 6 else " (phi_hat from tables 5-6: an out-of-sample test)"),
                   kind="verification")
NOPHI = TESTED[TESTED.appendix_table.isin([1, 5, 7, 8])]
j = NOPHI.gap.abs().idxmax()
check(f"largest gap, cells that do not involve phi (income elasticities, marginal shares; {len(NOPHI):,} cells)",
      round(float(NOPHI.gap[j]), 6), None, 0, "elasticity or share",
      f"appendix table {NOPHI.appendix_table[j]}, {NOPHI.country[j]}, {NOPHI.category[j]}: published "
      f"{NOPHI.published[j]}, recomputed {NOPHI.recomputed[j]:.4f}, band [{NOPHI.band_lo[j]:.4f}, "
      f"{NOPHI.band_hi[j]:.4f}] (fitted share {NOPHI.w_fitted[j]:.4f}, so the elasticity is extremely sensitive)",
      "usda_tb1929_recompute.csv")
FOODE = NOPHI[(NOPHI.appendix_table == 1) & (NOPHI.category == STAGE1_CATS[0])]
j = FOODE.gap.abs().idxmax()
check("largest gap, food income elasticity (appendix table 1, all 144 countries)", round(float(FOODE.gap[j]), 6),
      None, 0, "elasticity", f"{FOODE.country[j]}: published {FOODE.published[j]}, recomputed {FOODE.recomputed[j]:.6f}"
      f"; all {int(FOODE.within_band.sum())}/{len(FOODE)} inside the rounding band", "usda_tb1929_recompute.csv")
for t, cat in [(5, "Food other"), (5, "Beverages and tobacco")]:
    dd = NOPHI[(NOPHI.appendix_table == t) & (NOPHI.category == cat)]
    j = dd.gap.abs().idxmax()
    check(f"largest gap, appendix table {t} {cat} ({len(dd)} cells; eq. 11)", round(float(dd.gap[j]), 6), None, 0,
          "elasticity", f"{dd.country[j]}: published {dd.published[j]}, recomputed {dd.recomputed[j]:.6f}; "
          f"{int(dd.within_band.sum())}/{len(dd)} inside the rounding band", "usda_tb1929_recompute.csv")
NOPHI_WELL = NOPHI[NOPHI.w_fitted.abs() >= 0.02]
j = NOPHI_WELL.gap.abs().idxmax()
check("largest gap, same cells where the fitted share is at least 0.02",
      round(float(NOPHI_WELL.gap[j]), 6), None, 0, "elasticity or share",
      f"appendix table {NOPHI_WELL.appendix_table[j]}, {NOPHI_WELL.country[j]}, {NOPHI_WELL.category[j]}: published "
      f"{NOPHI_WELL.published[j]}, recomputed {NOPHI_WELL.recomputed[j]:.4f}", "usda_tb1929_recompute.csv")
for lab, d in [("income elasticities and marginal shares (tables 1, 5, 7, 8)", NOPHI),
               ("price elasticities with Table 3's phi (tables 2, 3, 4, 6)", TESTED[TESTED.appendix_table.isin([2, 3, 4, 6])])]:
    check_bool(f"every recomputed cell inside its rounding band: {lab}", d.within_band.all(),
               f"{int(d.within_band.sum())}/{len(d)}", kind="verification")
d = TESTED[TESTED.appendix_table.isin([2, 3, 4])]
check_bool("every recomputed cell inside its rounding band: stage-one price elasticities with phi_hat (tables 2-4)",
           d.within_band_phi_hat.all(), f"{int(d.within_band_phi_hat.sum())}/{len(d)}", kind="verification")
d = TESTED[TESTED.appendix_table.isin([2, 3, 4, 6])]
OUTB = d[~d.within_band]
j = OUTB.gap.abs().idxmax()
check("largest gap among the price-elasticity cells that fall outside the band with Table 3's phi",
      round(float(OUTB.gap[j]), 6), None, 0, "elasticity", f"{len(OUTB)} cells outside (table 2 food "
      f"{len(OUTB[(OUTB.appendix_table == 2)])}, table 4 food {len(OUTB[(OUTB.appendix_table == 4)])}, table 6 cereals "
      f"{len(OUTB[(OUTB.appendix_table == 6)])}); worst: appendix table {OUTB.appendix_table[j]}, {OUTB.country[j]}, "
      f"{OUTB.category[j]}: published {OUTB.published[j]}, recomputed {OUTB.recomputed[j]:.6f}, with phi_hat "
      f"{OUTB.recomputed_phi_hat[j]:.6f}", "usda_tb1929_recompute.csv")
finding("Table 3's phi does not reproduce the published price elasticities",
        f"Table 3 prints phi = {PHI} (se 0.034). Every Frisch elasticity ERS publishes divides by its income "
        f"elasticity to {PHI_HAT} (stage two, {len(PHI_RATIOS)} six-decimal cells, range {PHI_RATIOS.min():.4f} to "
        f"{PHI_RATIOS.max():.4f}), which would print as {round(PHI_HAT, 3)}. With {PHI}, {len(OUTB)} of {len(d)} "
        f"recomputed Frisch, Slutsky and Cournot cells fall outside their rounding band, by up to "
        f"{OUTB.gap.abs().max():.4f}; with {PHI_HAT} all {len(d)} fall inside. "
        f"The income elasticities and marginal shares (alpha, beta) are unaffected.", "Table 3; appendix tables 2-4, 6")

# Spot checks requested for this step: Finland, the United States and three low-income countries.
for c in ["Finland", "United States", "Tanzania", "India", "Kenya"]:
    for t, cat in [(1, STAGE1_CATS[0]), (7, STAGE1_CATS[0]), (1, "Medical and health"), (1, "Recreation and culture"),
                   (1, "Housing and utilities"), (5, "Food other"), (5, "Beverages and tobacco"), (5, "Cereals"),
                   (8, "Food other"), (2, STAGE1_CATS[0]), (6, "Food other")]:
        r = REC[(REC.appendix_table == t) & (REC.country == c) & (REC.category == cat)].iloc[0]
        if t in (2, 6):    # price elasticities: phi_hat (Table 3's phi is tested on its own above)
            val, half = r.recomputed_phi_hat, max(r.recomputed_phi_hat - r.band_lo_phi_hat,
                                                  r.band_hi_phi_hat - r.recomputed_phi_hat)
            extra = f"; phi_hat = {PHI_HAT}; with Table 3's phi {PHI}: {r.recomputed:.6f}"
        else:
            val, half, extra = r.recomputed, max(r.recomputed - r.band_lo, r.band_hi - r.recomputed), ""
        check(f"spot check {c}: appendix table {t} {APPX[t][1]}, {cat}", round(val, 6), r.published,
              round(half + r.half_unit_published, 6), "elasticity or share", f"tolerance = rounding band half-width; "
              f"fitted share {r.w_fitted:.4f}; per capita income {r.per_capita_income_rel_us:.4f}{extra}",
              f"appendix table {t}")

# 'a' cells: ERS used actual budget shares, which TB-1929 does not report. Their internal consistency: the actual
# share implied by the published income elasticity must reproduce the published Slutsky and Cournot values (eqs. 7,
# 8), and F = phi eta must hold whatever share was used (eqs. 6, 12).
A1C = REC[(REC.appendix_table == 1) & (REC.flag == "a")]
for _, r in A1C.iterrows():
    i = STAGE1_CATS.index(r.category)
    w = r.w_implied_actual
    th = w + B1[i]
    for t, val in [(2, PHI_HAT * th / w), (3, PHI_HAT * th / w * (1 - th)), (4, PHI_HAT * th / w * (1 - th) - th)]:
        o = REC[(REC.appendix_table == t) & (REC.country == r.country) & (REC.category == r.category)].iloc[0]
        if o.flag == "a":
            check(f"'a' cell {r.country}, {r.category}: appendix table {t} from the actual share implied by table 1",
                  round(val, 4), o.published, 0.003 * max(1, abs(val)), "elasticity",
                  f"implied actual share {w:.4f} (fitted {r.w_fitted:.4f}); phi_hat {PHI_HAT}", f"appendix table {t}")
        else:
            finding(f"'a' cell in appendix table 1 but not in table {t}: {r.country}, {r.category}",
                    f"table 1 uses an actual share ({r.published}a, implied share {w:.4f}); table {t} prints "
                    f"{o.published} unmarked, the fitted-share value (fitted share {r.w_fitted:.4f}; recomputed with "
                    f"phi_hat {o.recomputed_phi_hat:.3f})", f"appendix tables 1 and {t}")
A5C = REC[(REC.appendix_table == 5) & ((REC.flag == "a") | (REC.flag_pdf == "a"))]
for _, r in A5C.iterrows():
    o = REC[(REC.appendix_table == 6) & (REC.country == r.country) & (REC.category == r.category)].iloc[0]
    check(f"'a' cell {r.country}, {r.category}: Frisch = phi_hat x income elasticity (eq. 12)",
          round(PHI_HAT * r.published, 6), o.published, 2 * H + abs(r.published) * HPHI, "elasticity",
          f"fitted conditional share {r.w_fitted:.4f} (negative); implied actual share {r.w_implied_actual:.4f}; "
          f"flags: data product '{r.flag}', PDF '{r.flag_pdf}'", "appendix tables 5-6")
z = REC[(REC.appendix_table == 5) & (REC.country == "Zambia") & (REC.category == "Food other")].iloc[0]
finding("Zambia, Food other: which release is right about the 'a' mark",
        f"the fitted conditional share is {z.w_fitted:.4f}, negative, so the fitted-share elasticity would be "
        f"{z.recomputed:.3f}; the published {z.published} was computed from an actual share (implied "
        f"{z.w_implied_actual:.4f}): the data product's 'a' is right and the PDF omits it",
        "appendix table 5 vs data product Table5")
NEG_FITTED = sorted(REC[(REC.appendix_table == 5) & (REC.w_fitted < 0)].country.unique())
check_bool("stage two: the 'a' cells (either release) are exactly the cells with a negative fitted conditional share",
           set(A5C.country) == set(NEG_FITTED) and set(A5C.category) == {"Food other"},
           f"negative fitted share: {NEG_FITTED}", kind="verification")

# 'b' cells: ERS set positive (Giffen) unconditional Frisch values to zero. Since phi < 0 and F_u = phi eta_U, they
# must be exactly the cells (outside the 'a' cells) whose published income elasticity in appendix table 5 is < 0.
E5 = LONG[(LONG.appendix_table == 5) & (LONG.flag == "") & (LONG.flag_pdf == "")]
neg = set(E5[E5.value < 0][["country", "category"]].itertuples(index=False, name=None))
B6 = REC[REC.appendix_table == 6]
bset = set(B6[B6.flag_pdf == "b"][["country", "category"]].itertuples(index=False, name=None))
check_bool("table 6 'b' cells (PDF) = cells whose published table-5 income elasticity is negative", neg == bset,
           f"{len(bset)} 'b' cells; only in one set: {sorted(neg ^ bset)}", kind="verification")
for c, cat in sorted(k[1:] for k in KNOWN_DIFFS if k[0] == 6):
    r = B6[(B6.country == c) & (B6.category == cat)].iloc[0]
    check(f"table 6 release difference {c} {cat}: the data product's value is the positive Frisch value (phi_hat)",
          round(r.recomputed_phi_hat, 6), r.published, max(r.recomputed_phi_hat - r.band_lo_phi_hat,
                                                           r.band_hi_phi_hat - r.recomputed_phi_hat) + 5e-7,
          "elasticity", "the PDF replaced it with 0.000b", "data product Table6")

# ---------------------------------------------------------------------------------------------------------
# 9. Back-solve alpha and beta from the published country tables: a second, independent test of the transcription,
#    and the unrounded values behind ERS's own tables. Marginal shares are linear in log income, theta = alpha +
#    beta (1 + q) (eq. 3 with eq. 4b; the conditional form for stage two), so a least-squares line through the 144
#    published marginal shares returns alpha and beta.
# ---------------------------------------------------------------------------------------------------------
BACK = []
for stage, cats, t, xv, unit_half, A, B in [(1, STAGE1_CATS, 7, q, H, A1, B1), (2, STAGE2_CATS, 8, qf, 5e-7, A2, B2)]:
    X = np.column_stack([np.ones_like(xv), 1 + xv])
    names = ("alpha", "beta") if stage == 1 else ("alpha_star", "beta_star")
    for i, cat in enumerate(cats):
        y = pub(t, cat)[0]
        coef = np.linalg.lstsq(X, y, rcond=None)[0]
        rmax = float(np.abs(y - X @ coef).max())
        for par, printed, hat in [(names[0], A[i], coef[0]), (names[1], B[i], coef[1])]:
            BACK.append({"stage": stage, "category": cat, "parameter": par, "value_printed": printed,
                         "value_backsolved": round(float(hat), 6), "rounds_to_printed": bool(abs(hat - printed) <= H),
                         "n_cells": len(y), "max_abs_residual": round(rmax, 9),
                         "method": f"least squares of the 144 published marginal shares (appendix table {t}; the "
                                   f"data product carries {'3' if stage == 1 else '6'} decimals) on 1 + ln(per capita "
                                   f"{'income' if stage == 1 else 'food spending'} relative to the US)"})
            check(f"back-solve {par} {cat} from appendix table {t}", round(float(hat), 6), printed, H, "share",
                  f"max |residual| of the line {rmax:.1e} (published rounding {unit_half:g})", f"appendix table {t}")
BACK.append({"stage": 1, "category": "(all)", "parameter": "phi", "value_printed": PHI, "value_backsolved": PHI_HAT,
             "rounds_to_printed": bool(abs(PHI_HAT - PHI) <= H), "n_cells": len(PHI_RATIOS),
             "max_abs_residual": round(float((PHI_RATIOS - PHI_HAT).abs().max()), 9),
             "method": "median of F_u / eta_U over the 6-decimal stage-two cells (appendix tables 6 and 5; eq. 12)"})
BACK = pd.DataFrame(BACK)
for stage, pa, pb in [(1, "alpha", "beta"), (2, "alpha_star", "beta_star")]:
    sa = BACK[(BACK.stage == stage) & (BACK.parameter == pa)].value_backsolved.sum()
    sb = BACK[(BACK.stage == stage) & (BACK.parameter == pb)].value_backsolved.sum()
    check(f"back-solved stage-{stage} {pa}: sum to 1 (adding-up)", round(sa, 6), 1.0, 2e-4 if stage == 1 else 1e-5,
          "share", "", "back-solve")
    check(f"back-solved stage-{stage} {pb}: sum to 0 (adding-up)", round(sb, 6), 0.0, 2e-4 if stage == 1 else 1e-5,
          "share", "", "back-solve")
# The log and its normalisation: 1/(eta - 1) = alpha/beta + q, so the slope on q is 1 for a natural log with US = 1.
E = pub(1, STAGE1_CATS[0])[0]
slope, icept = np.polyfit(q, 1.0 / (E - 1.0), 1)
check("food income elasticity: slope of 1/(eta - 1) on ln(per capita income) (1 for a natural log, US = 1)",
      round(float(slope), 4), 1.0, 0.01, "", f"intercept {icept:.4f} vs alpha/beta = {A1[0] / B1[0]:.4f} (Table 3)",
      "appendix table 1 (data product)")

# ---------------------------------------------------------------------------------------------------------
# 10. Headline numbers in the bulletin's text against its own (printed, 3-decimal) tables; group averages
# ---------------------------------------------------------------------------------------------------------
def cell(t, country, cat):
    return float(LONG[(LONG.appendix_table == t) & (LONG.country == country) & (LONG.category == cat)].value_pdf.iloc[0])


FOODC, RECC, MEDC = STAGE1_CATS[0], "Recreation and culture", "Medical and health"
AVG = {(r["table"], r["name"].split("-")[0].lower()): r["tokens"] for r in APPX_PDF_ROWS if r["kind"] == "average"}
TEXT_CLAIMS = [  # (claim as printed, printed page, value from the printed tables, number in the text, tolerance)
    ("$1 more income raises food spending 63 cents in the DR Congo", "12", cell(7, "Congo, Dem. Rep.", FOODC), .63, .005),
    ("... but only 6 cents in the United States", "12", cell(7, "United States", FOODC), .06, .005),
    ("US health marginal share 12 cents", "12", cell(7, "United States", MEDC), .12, .005),
    ("US recreation marginal share 13 cents", "12", cell(7, "United States", RECC), .13, .005),
    ("DR Congo recreation 'would not increase at all'", "12", cell(7, "Congo, Dem. Rep.", RECC), 0.0, .01),
    ("food income elasticity 0.85 for the DR Congo", "13-14", cell(1, "Congo, Dem. Rep.", FOODC), .85, .005),
    ("food income elasticity 0.71 for Armenia", "14", cell(1, "Armenia", FOODC), .71, .005),
    ("food income elasticity of middle-income countries from 0.71 (Venezuela)", "14", cell(1, "Venezuela, RB", FOODC), .71, .005),
    ("food income elasticity of middle-income countries to 0.57 (Israel)", "14", cell(1, "Israel", FOODC), .57, .005),
    ("food income elasticity of high-income countries from 0.56 (Portugal)", "14", cell(1, "Portugal", FOODC), .56, .005),
    ("food income elasticity of high-income countries to 0.35 (United States)", "14", cell(1, "United States", FOODC), .35, .005),
    ("average food income elasticity, low-income countries, 0.78", "14", float(AVG[(1, "low")][0]), .78, .005),
    ("average food income elasticity, high-income countries, 0.50", "14", float(AVG[(1, "high")][0]), .50, .005),
    ("education income elasticity, low-income average 0.93", "14", float(AVG[(1, "low")][7]), .93, .005),
    ("education income elasticity, high-income average 0.91", "14", float(AVG[(1, "high")][7]), .91, .005),
    ("recreation income elasticity 13.1 for Angola", "14", cell(1, "Angola", RECC), 13.1, .05),
    ("recreation income elasticity 1.25 for the United States", "14", cell(1, "United States", RECC), 1.25, .005),
    ("medical/health income elasticity 8.6 for Liberia", "14", cell(1, "Liberia", MEDC), 8.6, .05),
    ("medical/health income elasticity 1.21 for the United States", "14", cell(1, "United States", MEDC), 1.21, .005),
    ("Slutsky food elasticity -0.23 for the DR Congo", "14", cell(3, "Congo, Dem. Rep.", FOODC), -.23, .005),
    ("Slutsky food elasticity peaks at -0.384", "14", float(LONG[(LONG.appendix_table == 3) & (LONG.category == FOODC)].value_pdf.min()), -.384, 0),
    ("Slutsky food elasticity -0.24 for the United States", "14", cell(3, "United States", FOODC), -.24, .005),
    ("turning point at Argentina, 22 percent of US per capita income", "15", PCI["Argentina"], .22, .005),
    ("$1 more food spending: cereals +31 cents in the DR Congo", "17", cell(8, "Congo, Dem. Rep.", "Cereals"), .31, .005),
    ("... cereals -1.5 cents in the United States", "17", cell(8, "United States", "Cereals"), -.015, .0005),
    ("'other' food +5 cents in the DR Congo", "17", cell(8, "Congo, Dem. Rep.", "Food other"), .05, .005),
    ("'other' food +42 cents in the United States", "17", cell(8, "United States", "Food other"), .42, .005),
    ("cereals income elasticity 0.69 in the DR Congo", "18", cell(5, "Congo, Dem. Rep.", "Cereals"), .69, .005),
    ("cereals income elasticity -0.09 in the United States", "18", cell(5, "United States", "Cereals"), -.09, .005),
    ("beverages/tobacco income elasticity 7.1 in Liberia", "18", cell(5, "Liberia", "Beverages and tobacco"), 7.1, .05),
    ("beverages/tobacco income elasticity 0.42 in the United States", "18", cell(5, "United States", "Beverages and tobacco"), .42, .005),
    ("Frisch elasticity of breads and cereals 0.50 (absolute) in the DR Congo", "18", -cell(6, "Congo, Dem. Rep.", "Cereals"), .50, .005),
    ("'other' food: price +1% cuts consumption by more than 1% (low-income average)", "18", -float(AVG[(6, "low")][7]), 1.0, 0.05),
    ("... and by less than 0.5% (high-income average)", "18", -float(AVG[(6, "high")][7]), 0.47, 0.03),
]
for claim, page, comp, txt, tol in TEXT_CLAIMS:
    check(f"text p. {page}: {claim}", round(comp, 6), txt, tol, "", "", f"tb-1929.pdf printed p. {page}")
us_cer = REC[(REC.appendix_table == 6) & (REC.country == "United States") & (REC.category == "Cereals")].iloc[0]
finding("text p. 18: the cereals Frisch elasticity is quoted as 0.06 for the United States; appendix table 6 prints "
        "0.000b", f"recomputed before ERS's zeroing: {us_cer.recomputed_phi_hat:.4f}; the text quotes the positive "
        "value the table replaced with zero (footnote b), without its sign", "tb-1929.pdf printed p. 18")
peak = LONG[(LONG.appendix_table == 3) & (LONG.category == FOODC) & (LONG.value_pdf == -0.384)].country.tolist()
check_bool("text p. 14: the Slutsky food peak -0.384 runs 'Ukraine to Argentina'",
           peak[0] == "Ukraine" and peak[-1] == "Argentina", f"{peak[0]} ... {peak[-1]} ({len(peak)} countries)",
           kind="verification")

# Group averages printed under every appendix table: simple means of the group's printed country values?
GA = []
for r in [r for r in APPX_PDF_ROWS if r["kind"] == "average"]:
    t = r["table"]
    st, meas, lead = APPX[t][0], APPX[t][1], APPX[t][2]
    g = r["name"].split("-")[0].lower()
    members = [c for c in COUNTRIES if GROUP_OF[c] == g]
    for col, tok in zip(lead + (STAGE1_CATS if st == 1 else STAGE2_CATS), r["tokens"]):
        if col in ("per_capita_income", "per_capita_food"):
            vals = [PCI[c] if col == "per_capita_income" else PCF[c] for c in members]
            measure, stg, cat = col + "_rel_us", 0, "(all)"
        else:
            dd = LONG[(LONG.appendix_table == t) & (LONG.category == col) & LONG.country.isin(members)]
            vals, measure, stg, cat = dd.value_pdf.tolist(), meas, st, col
        GA.append({"source_table": f"appendix table {t}", "printed_page": r["printed_page"], "income_group": g,
                   "stage": stg, "category": cat, "measure": measure, "value": float(re.sub("[ab]$", "", tok)),
                   "mean_of_countries": round(float(np.mean(vals)), 6), "n_countries": len(vals)})
GA = pd.DataFrame(GA)
GA["diff"] = (GA.value - GA.mean_of_countries).round(6)
worst = GA.loc[GA["diff"].abs().idxmax()]
check("appendix group averages = simple (unweighted) means of the printed country values, largest |diff|, all tables",
      float(worst["diff"]), 0.0, 0.0015, "", f"{worst.source_table}, {worst.income_group}, {worst.category}: printed "
      f"{worst.value}, mean {worst.mean_of_countries}; 'a' and 'b' cells enter as printed", "appendix tables")
for g, v in [("low", .045), ("high", .089)]:
    check(f"Table 2: health budget share, {g}-income ({v:.1%} in the summary)",
          float(T2[(T2.income_group == g) & (T2.category == MEDC)].value.iloc[0]), v, 0, "share", "",
          "Table 2; summary p. iii")
for g in GROUPS:
    members = [c for c in COUNTRIES if GROUP_OF[c] == g]
    fitted = np.mean([A1[0] + B1[0] * np.log(PCI[c]) for c in members])
    check(f"Table 2 {g}-income food budget share (actual, ICP data) beside the mean fitted share", round(fitted, 4),
          None, 0, "share", f"Table 2 prints {float(T2[(T2.income_group == g) & (T2.category == FOODC)].value.iloc[0])}"
          ": actual shares, while the elasticities use fitted shares at geometric mean prices", "Table 2; Table 3")

# ---------------------------------------------------------------------------------------------------------
# 11. Category definitions in the publishers' words (every quote is checked against the vendored text and its page
#     located), and the mapping to COICOP divisions and BLS CE top-level items (judgment calls spelled out)
# ---------------------------------------------------------------------------------------------------------
TB1937_PAGES = [norm(pg.extract_text() or "") for pg in
                tqdm(PdfReader(RAWU / "supplement/tb-1937.pdf").pages, desc="TB-1937 pages (pypdf)")]
TB1937_PRINTED = {i + 1: printed_page(t, "New International Evidence on Food Consumption Patterns, TB-1937")
                  for i, t in enumerate(TB1937_PAGES)}
DOC_TEXT = norm(BeautifulSoup((RAWU / "dataproduct/documentation.html").read_text(encoding="utf-8"),
                              "lxml").get_text(" "))
SOURCE_TEXT = {
    "TB-1929": [(PRINTED[i + 1] or f"PDF {i + 1}", squash(t)) for pages in (PAGES, PAGES_BODY, PAGES_PYPDF)
                for i, t in enumerate(pages)],
    "TB-1937": [(TB1937_PRINTED[i + 1] or f"PDF {i + 1}", squash(t)) for i, t in enumerate(TB1937_PAGES)],
    "ERS documentation page": [("web page", squash(DOC_TEXT))],
}


def cite(source, quote):
    """The quote with its source and page(s); a quote not found verbatim (letters and digits) fails a check."""
    pages = list(dict.fromkeys(lab for lab, txt in SOURCE_TEXT[source] if squash(quote) in txt))
    check_bool(f"quote found in {source}: '{quote[:70]}...'", bool(pages), f"pages {pages}", source=source)
    labels = [lab.replace("PDF ", "PDF p. ") + " (unnumbered page)" if lab.startswith("PDF") else "p. " + lab
              for lab in pages]
    where = source if source == "ERS documentation page" else f"{source} {', '.join(labels)}"
    return f"\"{quote}\" ({where})"


Q_LIST1 = ("clothing and footwear, education, housing, house furnishings and operations, medical care, transport and "
           "communications, recreation, and other expenditures")
Q_LIST2 = ("eight food subcategories: bread and cereals, meat, fish, dairy products, fruits and vegetables, oils and "
           "fats, beverages and tobacco, and other food products")
Q37_LIST = ("food, beverages, and tobacco (for the first time includes food consumed away from home); clothing and "
            "footwear; gross rent, fuel, and power; house furnishings and operations (includes spending on household "
            "equipment and maintenance); medical and health; transport and communications; recreation; education; "
            "and other.")
Q37_OTHER = "(“Other” includes expenditures for grooming services, jewelry, and other miscellaneous expenditures.)"
QDOC_SUB = ("Food subcategories Bread and cereals Meat Fish Dairy products Fruits and vegetables Oils and fats "
            "Beverages and tobacco Other food products")
L2 = {1: ["Food, beverages, & tobacco", "Clothing & footwear", "Housing", "House furnishings", "Medical & health",
          "Transport & communications", "Recreation", "Education", "Other"],
      2: ["Cereals", "Meats", "Fish", "Dairy", "Oils & fats", "Fruits & vegetables", "Food other",
          "Beverages & tobacco"]}
LDP = {1: XLS[1]["header"][2:], 2: XLS[8]["header"][3:]}
CATEGORIES = [
    # ---- stage one: the nine broad groups of the Florida-PI model --------------------------------------------
    dict(stage=1, category="Food, beverage, and tobacco", label_text="food",
         short_def="food at home + food away from home (restaurants and catering) + beverages and tobacco",
         definition_tb1929=[("TB-1929", "food—which includes food prepared and consumed at home, food away from "
                                        "home, and beverages and tobacco"),
                            ("TB-1929", "Unlike previous ICP data, restaurant and catering expenditures are included "
                                        "among food in the 2005 data."),
                            ("TB-1929", "In the 2005 ICP round, food for the first time includes food consumed away "
                                        "from home, captured under the “other food” category.")],
         definition_other=[("ERS documentation page", "Food, which includes food prepared and consumed at home, food "
                                                     "away from home, and beverages and tobacco"),
                           ("TB-1937", "“Food away from home” was included under “recreation” "
                                       "expenditure in the previous rounds of ICP.")],
         coicop_1999="01 Food and non-alcoholic beverages; 02 Alcoholic beverages, tobacco and narcotics; 11.1 Catering "
                     "services",
         coicop_2018="01 Food and non-alcoholic beverages; 02 Alcoholic beverages, tobacco and narcotics; 11.1 Food and "
                     "beverage serving services",
         bls_ce="Food at home; Food away from home; Alcoholic beverages; Tobacco products and smoking supplies",
         judgment="ERS names restaurant and catering spending but never lists ICP headings, so 'COICOP 11.1 in full' "
                  "(canteens, take-away) is a judgment; accommodation (11.2) is not in food (see Other); narcotics "
                  "presumably sit here with alcohol and tobacco (not stated). CE food away from home and on-premise "
                  "alcohol are inside this group either way."),
    dict(stage=1, category="Clothing and footwear", label_text="clothing and footwear",
         short_def="clothing and footwear",
         definition_tb1929=[("TB-1929", Q_LIST1)], definition_other=[("TB-1937", Q37_LIST)],
         coicop_1999="03 Clothing and footwear", coicop_2018="03 Clothing and footwear",
         bls_ce="Apparel and services",
         judgment="CE 'Other apparel products and services' holds watches and jewelry, which COICOP puts in personal "
                  "effects (12.3 in 1999, 13.2 in 2018) and TB-1937 in 'Other'; small."),
    dict(stage=1, category="Housing and utilities", label_text="housing",
         short_def="housing: actual and imputed rent, water, fuel and power (TB-1937: gross rent, fuel, and power)",
         definition_tb1929=[("TB-1929", Q_LIST1)], definition_other=[("TB-1937", Q37_LIST)],
         coicop_1999="04 Housing, water, electricity, gas and other fuels",
         coicop_2018="04 Housing, water, electricity, gas and other fuels",
         bls_ce="Housing > Shelter (Owned dwellings, Rented dwellings, Other lodging); Housing > Utilities, fuels, and "
                "public services, less Telephone services",
         judgment="ICP and COICOP housing include owner-occupiers' imputed rent (COICOP 04.2, 15.2% of Finnish HBS "
                  "2022 spending); CE records none: its 'Owned dwellings' is cash outlay (mortgage interest, property "
                  "taxes, insurance, maintenance and repairs). CE 'Other lodging' mixes second homes with lodging on "
                  "trips (COICOP 11.2, see Other). CE 'Telephone services' sits under CE utilities but is "
                  "communication."),
    dict(stage=1, category="Furnishing, household equipment, and maintenance", label_text="house furnishings and operations",
         short_def="furnishings, household equipment, and routine household maintenance and operations",
         definition_tb1929=[("TB-1929", Q_LIST1)], definition_other=[("TB-1937", Q37_LIST)],
         coicop_1999="05 Furnishings, household equipment and routine maintenance of the house",
         coicop_2018="05 Furnishings, household equipment and routine household maintenance",
         bls_ce="Housing > Household furnishings and equipment; Housing > Housekeeping supplies, less Postage and "
                "stationery; Housing > Household operations > Other household expenses",
         judgment="CE 'Household operations > Personal services' is mostly child and adult care (COICOP social "
                  "protection, 12.4 in 1999 and 13.3 in 2018: Other). CE 'Postage and stationery' is postal services "
                  "(communication) and stationery (recreation)."),
    dict(stage=1, category="Medical and health", label_text="medical care",
         short_def="medical care and health", definition_tb1929=[("TB-1929", Q_LIST1)],
         definition_other=[("TB-1937", Q37_LIST)], coicop_1999="06 Health", coicop_2018="06 Health",
         bls_ce="Healthcare (Health insurance, Medical services, Drugs, Medical supplies)",
         judgment="CE 'Health insurance' is premiums, which COICOP books as insurance connected with health (12.5.3 "
                  "in 1999, 12.1.3 in 2018: Other) unless netted. ERS does not say whether its ICP aggregate is "
                  "household expenditure only or includes government-provided health and education."),
    dict(stage=1, category="Transportation and communication", label_text="transport and communications",
         short_def="transport and communications", definition_tb1929=[("TB-1929", Q_LIST1)],
         definition_other=[("TB-1937", Q37_LIST)], coicop_1999="07 Transport; 08 Communication",
         coicop_2018="07 Transport; 08 Information and communication",
         bls_ce="Transportation; Housing > Utilities, fuels, and public services > Telephone services; postage (in "
                "Housing > Housekeeping supplies > Postage and stationery)",
         judgment="CE 'Vehicle finance charges' are interest (outside COICOP consumption); CE 'Vehicle insurance' is "
                  "insurance connected with transport (12.5.4 / 12.1.4: Other); CE vehicle purchases are net of "
                  "trade-ins. COICOP 2018 08.1 'Information and communication equipment' merges telephones (1999 08.2, "
                  "here) with computers and audio-visual equipment (1999 09.1, recreation); no clean division-level "
                  "split."),
    dict(stage=1, category="Recreation and culture", label_text="recreation",
         short_def="recreation and culture", definition_tb1929=[("TB-1929", Q_LIST1)],
         definition_other=[("TB-1937", Q37_LIST)], coicop_1999="09 Recreation and culture",
         coicop_2018="09 Recreation, sport and culture",
         bls_ce="Entertainment; Reading",
         judgment="Package holidays are COICOP 09.6 (1999) / 09.8 (2018); CE spreads trips over lodging, transport and "
                  "food away. Computers and audio-visual equipment: see Transportation and communication."),
    dict(stage=1, category="Education", label_text="education",
         short_def="education", definition_tb1929=[("TB-1929", Q_LIST1)], definition_other=[("TB-1937", Q37_LIST)],
         coicop_1999="10 Education", coicop_2018="10 Education services", bls_ce="Education",
         judgment="CE education includes school books and supplies (COICOP 09.5 in 1999, 09.7 in 2018); small. "
                  "Coverage of government-provided education not stated (see Medical and health)."),
    dict(stage=1, category="Other", label_text="other expenditures",
         short_def="everything else: personal care, personal effects, insurance, financial and other services",
         definition_tb1929=[("TB-1929", Q_LIST1)], definition_other=[("TB-1937", Q37_LIST), ("TB-1937", Q37_OTHER)],
         coicop_1999="12 Miscellaneous goods and services; 11.2 Accommodation services (judgment)",
         coicop_2018="12 Insurance and financial services; 13 Personal care, social protection and miscellaneous goods "
                     "and services; 11.2 Accommodation services (judgment)",
         bls_ce="Personal care products and services; Miscellaneous; by the judgments above also jewelry and watches, "
                "child and adult care, vehicle and health insurance premiums, lodging on trips. Outside consumption: "
                "Cash contributions; Personal insurance and pensions",
         judgment="TB-1929 places catering in food but never says where accommodation (COICOP 11.2) or net purchases "
                  "abroad went; treating Other as the residual is a judgment."),
    # ---- stage two: the eight food subgroups of the conditional Florida-Slutsky model ----------------------------
    dict(stage=2, category="Cereals", label_text="bread and cereals", short_def="bread and cereals",
         definition_tb1929=[("TB-1929", Q_LIST2)], definition_other=[("ERS documentation page", QDOC_SUB)],
         coicop_1999="01.1.1 Bread and cereals", coicop_2018="01.1.1 Cereals and cereal products",
         bls_ce="Food at home > Cereals and bakery products", judgment=""),
    dict(stage=2, category="Meat", label_text="meat", short_def="meat", definition_tb1929=[("TB-1929", Q_LIST2)],
         definition_other=[("ERS documentation page", QDOC_SUB)], coicop_1999="01.1.2 Meat", coicop_2018="01.1.2 Meat",
         bls_ce="Food at home > Meats, poultry, fish, and eggs > Beef, Pork, Other meats, Poultry", judgment=""),
    dict(stage=2, category="Fish", label_text="fish", short_def="fish", definition_tb1929=[("TB-1929", Q_LIST2)],
         definition_other=[("ERS documentation page", QDOC_SUB)], coicop_1999="01.1.3 Fish and seafood", coicop_2018="01.1.3 Fish and other seafood",
         bls_ce="Food at home > Meats, poultry, fish, and eggs > Fish and seafood", judgment=""),
    dict(stage=2, category="Dairy and eggs", label_text="dairy products", short_def="dairy products and eggs",
         definition_tb1929=[("TB-1929", Q_LIST2)], definition_other=[("ERS documentation page", QDOC_SUB)],
         coicop_1999="01.1.4 Milk, cheese and eggs", coicop_2018="01.1.4 Milk, other dairy products and eggs",
         bls_ce="Food at home > Dairy products; Food at home > Meats, poultry, fish, and eggs > Eggs",
         judgment="Table 4 says 'Dairy and eggs'; the text says 'dairy products' and Table 2 'Dairy'."),
    dict(stage=2, category="Oils and fat", label_text="oils and fats", short_def="oils and fats",
         definition_tb1929=[("TB-1929", Q_LIST2)], definition_other=[("ERS documentation page", QDOC_SUB)],
         coicop_1999="01.1.5 Oils and fats", coicop_2018="01.1.5 Oils and fats",
         bls_ce="Food at home > Other food at home > Fats and oils", judgment=""),
    dict(stage=2, category="Fruit and vegetables", label_text="fruits and vegetables",
         short_def="fruits and vegetables, including roots and tubers",
         definition_tb1929=[("TB-1929", Q_LIST2), ("TB-1929", "The fruits and vegetable category includes roots and "
                                                              "tubers, a cheap source of calories in many poor countries.")],
         definition_other=[("ERS documentation page", QDOC_SUB)], coicop_1999="01.1.6 Fruit; 01.1.7 Vegetables",
         coicop_2018="01.1.6 Fruit and nuts; 01.1.7 Vegetables, tubers, plantains, cooking bananas and pulses",
         bls_ce="Food at home > Fruits and vegetables", judgment=""),
    dict(stage=2, category="Food other", label_text="other food products",
         short_def="food away from home (restaurants, catering) and every other food item: not restaurants alone",
         definition_tb1929=[("TB-1929", Q_LIST2),
                            ("TB-1929", "In the 2005 ICP round, food for the first time includes food consumed away "
                                        "from home, captured under the “other food” category."),
                            ("TB-1929", "the budget share for the other food category—which includes "
                                        "away-from-home food purchases—is highest in high-income countries"),
                            ("TB-1929", "“other” food expenditures, which includes restaurant expenditures "
                                        "and high-end purchases")],
         definition_other=[("ERS documentation page", QDOC_SUB)],
         coicop_1999="11.1 Catering services (stated); by elimination 01.1.8 Sugar, jam, honey, chocolate and "
                     "confectionery and 01.1.9 Food products n.e.c.; 01.2 Non-alcoholic beverages here or in Beverages "
                     "and tobacco (not stated)",
         coicop_2018="11.1 Food and beverage serving services (stated); by elimination 01.1.8 and 01.1.9; 01.2 not "
                     "stated",
         bls_ce="Food away from home; Food at home > Other food at home > Sugar and other sweets, Miscellaneous foods, "
                "Food prepared by consumer unit on out of town trips",
         judgment="The only subgroup that holds restaurant spending, and it is not restaurants alone. TB-1929 has no "
                  "restaurant subgroup."),
    dict(stage=2, category="Beverages and tobacco", label_text="beverages and tobacco",
         short_def="beverages and tobacco ('beverages' not qualified: alcoholic for sure, non-alcoholic not stated)",
         definition_tb1929=[("TB-1929", Q_LIST2)], definition_other=[("ERS documentation page", QDOC_SUB)],
         coicop_1999="02 Alcoholic beverages, tobacco and narcotics; probably 01.2 Non-alcoholic beverages (not stated)",
         coicop_2018="02 Alcoholic beverages, tobacco and narcotics; probably 01.2 Non-alcoholic beverages (not stated)",
         bls_ce="Alcoholic beverages; Tobacco products and smoking supplies; Food at home > Other food at home > "
                "Nonalcoholic beverages if non-alcoholic beverages belong here",
         judgment="TB-1929 never qualifies 'beverages'. The subgroup is 'alcohol and tobacco' only if non-alcoholic "
                  "beverages sit in Food other; ERS's documents do not settle it."),
]
SUMMARY_TXT = squash(" ".join(norm(pg.extract_text() or "") for pg in
                               PdfReader(RAWU / "report/tb-1929-report-summary.pdf").pages))
for quote in [CATEGORIES[0]["definition_tb1929"][0][1], Q_LIST2]:
    check_bool(f"report summary PDF repeats the category list: '{quote[:70]}...'", squash(quote) in SUMMARY_TXT,
               source="tb-1929-report-summary.pdf")
import zipfile
with zipfile.ZipFile(RAWU / "report/download-tb1929.zip") as zf:      # names only; nothing is extracted
    ZIP_NAMES = sorted(zf.namelist())
check_bool("TB1929.zip holds a readme and the four figures only (no tables)",
           ZIP_NAMES == ["Fig01.png", "Fig02.png", "Fig03.png", "Fig04.png", "readme.txt"], ", ".join(ZIP_NAMES),
           source="report/download-tb1929.zip")
CAT_ROWS = []
for c in CATEGORIES:
    k = (STAGE1_CATS if c["stage"] == 1 else STAGE2_CATS).index(c["category"])
    CAT_ROWS.append({"stage": c["stage"], "order": k + 1, "category": c["category"],
                     "label_tb1929_text": c["label_text"], "label_tb1929_table2_appendix": L2[c["stage"]][k],
                     "label_data_product": LDP[c["stage"]][k], "short_definition": c["short_def"],
                     "definition_tb1929": " | ".join(cite(s, x) for s, x in c["definition_tb1929"]),
                     "definition_other_ers": " | ".join(cite(s, x) for s, x in c["definition_other"]),
                     "coicop_1999": c["coicop_1999"], "coicop_2018": c["coicop_2018"], "bls_ce": c["bls_ce"],
                     "judgment_calls": c["judgment"]})
CAT = pd.DataFrame(CAT_ROWS)
check_bool("category list complete: 9 stage-one groups and 8 stage-two subgroups, in table order",
           CAT[CAT.stage == 1].category.tolist() == STAGE1_CATS and CAT[CAT.stage == 2].category.tolist() == STAGE2_CATS)
for src, quote in [("TB-1937", "The parameters are those estimated by MSMR (2011; table 3, p. 12). All elasticities "
                               "are calculated at geometric mean prices."),
                   ("TB-1937", "real per capita income in all countries relative to that of the United States "
                               "normalized to equal 1")]:
    check_bool(f"TB-1937 says: {quote[:80]}", bool(cite(src, quote)), source="TB-1937")

# ---------------------------------------------------------------------------------------------------------
# 12. Tidy outputs
# ---------------------------------------------------------------------------------------------------------
print("writing tidy files")
BK = BACK.set_index(["stage", "category", "parameter"]).value_backsolved
SHORT = {(c["stage"], c["category"]): c["short_def"] for c in CATEGORIES}


def band_text(stage, cat, tables):
    d = TESTED[(TESTED.stage == stage) & (TESTED.category == cat) & TESTED.appendix_table.isin(tables)]
    return f"{int(d.within_band.sum())}/{len(d)} cells of appendix tables {', '.join(map(str, tables))}"


PAR = []
for rows, tno, stage, pno in [(T3, 3, 1, P_T3), (T4, 4, 2, P_T4)]:
    for r in rows:
        par, cat = r["parameter"], r["category"]
        if par in ("alpha", "beta"):
            ver = (f"verified: back-solved from the 144 marginal shares of appendix table 7 = {BK[(1, cat, par)]} "
                   f"(rounds to the printed value); recomputation inside the rounding band for "
                   f"{band_text(1, cat, [1, 7])}")
        elif par in ("alpha_star", "beta_star"):
            ver = (f"verified: back-solved from the 144 six-decimal marginal shares of appendix table 8 = "
                   f"{BK[(2, cat, par)]} (rounds to the printed value); recomputation inside the rounding band for "
                   f"{band_text(2, cat, [5, 8])}")
        elif par == "phi":
            dd = TESTED[TESTED.appendix_table.isin([2, 3, 4, 6])]
            ver = (f"NOT reproduced: the published Frisch, Slutsky and Cournot tables imply phi = {PHI_HAT} (F/eta, "
                   f"{len(PHI_RATIOS)} six-decimal cells), which would print as {round(PHI_HAT, 3)}; with "
                   f"{PHI}, {int((~dd.within_band).sum())} of {len(dd)} recomputed price-elasticity cells fall "
                   f"outside their rounding band (by up to {dd[~dd.within_band].gap.abs().max():.4f}); with {PHI_HAT}, "
                   f"{int(dd.within_band_phi_hat.sum())}/{len(dd)} inside; income elasticities do not use phi")
        else:
            ver = ("not verifiable by recomputation: no table in TB-1929 depends on it; two independent text "
                   "extractions agree and match the page image")
        note = f"{STARS[r['stars']]}; PDF p. {pno}; {ver}; se as printed (not recomputable)"
        if par in ("beta", "beta_star"):
            note = f"group: {SHORT[(stage, cat)]}; " + note
        PAR.append({"stage": stage, "category": cat, "parameter": par, "value": r["value"], "se": r["se"],
                    "table": f"Table {tno}", "page": int(PRINTED[pno]), "note": note})
PAR = pd.DataFrame(PAR)
write_csv(PAR, "usda_tb1929_params.csv")
write_csv(CAT, "usda_tb1929_categories.csv")

CTRY = pd.DataFrame({"country": COUNTRIES, "country_order": range(1, 145),
                     "income_group": [GROUP_OF[c] for c in COUNTRIES],
                     "per_capita_income_rel_us": [PCI[c] for c in COUNTRIES],
                     "per_capita_food_rel_us": [PCF[c] for c in COUNTRIES],
                     "outlier_in_estimation": [c in OUTLIERS for c in COUNTRIES]})
write_csv(CTRY, "usda_tb1929_countries.csv")

OUT_LONG = LONG.merge(CTRY[["country", "per_capita_income_rel_us", "per_capita_food_rel_us", "outlier_in_estimation"]],
                      on="country", how="left")
OUT_LONG = OUT_LONG[["appendix_table", "measure", "equation", "stage", "category", "country", "country_order",
                     "income_group", "outlier_in_estimation", "per_capita_income_rel_us", "per_capita_food_rel_us",
                     "value", "flag", "value_pdf", "flag_pdf", "release_note", "pdf_page", "printed_page", "xls_file"]]
CAT_ORDER = {c: i for i, c in enumerate(STAGE1_CATS + STAGE2_CATS)}
OUT_LONG = OUT_LONG.assign(_k=OUT_LONG.category.map(CAT_ORDER)).sort_values(
    ["appendix_table", "country_order", "_k"]).drop(columns="_k")
write_csv(OUT_LONG, "usda_tb1929_country_long.csv")

GA_OUT = pd.concat([T2.assign(mean_of_countries=np.nan, n_countries=np.nan, diff=np.nan), GA], ignore_index=True)
write_csv(GA_OUT[["source_table", "printed_page", "income_group", "stage", "category", "measure", "value",
                  "mean_of_countries", "n_countries", "diff"]], "usda_tb1929_group_averages.csv")

REC_OUT = REC[["appendix_table", "measure", "stage", "category", "country", "country_order", "income_group",
               "per_capita_income_rel_us", "per_capita_food_rel_us", "w_fitted", "published", "flag", "published_pdf",
               "flag_pdf", "status", "recomputed", "band_lo", "band_hi", "gap", "within_band", "recomputed_phi_hat",
               "band_lo_phi_hat", "band_hi_phi_hat", "gap_phi_hat", "within_band_phi_hat", "w_implied_actual",
               "half_unit_published"]].copy()
for col in ["w_fitted", "recomputed", "band_lo", "band_hi", "gap", "recomputed_phi_hat", "band_lo_phi_hat",
            "band_hi_phi_hat", "gap_phi_hat", "w_implied_actual"]:
    REC_OUT[col] = REC_OUT[col].round(9)
write_csv(REC_OUT, "usda_tb1929_recompute.csv")
write_csv(BACK, "usda_tb1929_backsolved.csv")

CHK = pd.DataFrame(CHECKS)[["kind", "check", "computed", "published", "diff", "tolerance", "unit", "pass", "source",
                            "note"]]
write_csv(CHK, "usda_tb1929_checks.csv")

# ---------------------------------------------------------------------------------------------------------
# 13. Summary; stop if any consistency check failed (a parsing or transcription problem on my side)
# ---------------------------------------------------------------------------------------------------------
summary = CHK.groupby(["kind", "pass"], dropna=False).size()
print("checks by kind and result:\n" + summary.to_string())
bad = CHK[(CHK.kind == "consistency") & (CHK["pass"] == False)]
vfail = CHK[(CHK.kind == "verification") & (CHK["pass"] == False)]
print(f"verification checks that fail ({len(vfail)}; findings about the source, see README_usda.md):")
for _, r in vfail.iterrows():
    print("   -", r.check[:200])
if len(bad):
    raise SystemExit(f"{len(bad)} consistency checks failed: " + "; ".join(bad.check.head(5)))
print("done:", len(CHK), "checks;", len(bad), "consistency failures")
