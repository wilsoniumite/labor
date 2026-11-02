# acquire_fed.py — vendor Federal Reserve Board data for the consumption thread:
#   * Survey of Consumer Finances: the 2022 summary extract (re-issued 2026-10-09 in 2025 dollars), the program that
#     defines its variables (bulletin.macro.txt), the 2022 codebook, the 2022 full public data (household roster and
#     a few KVW inputs only), the 2025 extract and codebook, the 2023 and 2026 Bulletin articles and the Fed's
#     historic tables used as cross-checks;
#   * Distributional Financial Accounts: the full CSV zip (2026:Q2) and the public code package (read as text for
#     the group definitions, never executed);
#   * Financial Accounts (Z.1): the Board's 2026:Q2 CSV package and the archived 2020:Q4 package (last release with
#     the NFC current-cost structures); the paper's FRED copies are attempted as specified and failures recorded.
# Then build tidy files from the raw files only, with every cross-check written to tidy/fed_checks.csv.
# Documentation of every output: consumption/data/tidy/README_fed.md and scf2022_variables.md.
#
# Run from the repo root:  venv/bin/python -I consumption/code/acquire_fed.py
#   --offline       never touch the network (build from what is vendored)
#   --retry-failed  retry downloads recorded in raw/fed/FETCH_FAILURES.csv (default: a recorded failure is not
#                   retried, per the stop-and-report rule)
# Downloads skip files already vendored, so a rerun is offline and rebuilds every tidy file from raw.
# Plain functions and top-level code (notebook-cell friendly). No modelling here.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import fetch, manifest_row, RAW, TIDY, REPO

import csv
import datetime as dt
import io
import re
import zipfile

import numpy as np
import openpyxl
import pandas as pd
import pdfplumber
from bs4 import BeautifulSoup
from tqdm.auto import tqdm

SRC = "fed"
RAWF = RAW / SRC
RAWF.mkdir(parents=True, exist_ok=True)
TIDY.mkdir(parents=True, exist_ok=True)
OFFLINE = "--offline" in sys.argv
RETRY_FAILED = "--retry-failed" in sys.argv

# ---------------------------------------------------------------------------------------------------------
# 1. Download list. (rel_file, url, what_it_is, used_for)
# ---------------------------------------------------------------------------------------------------------
FRB = "https://www.federalreserve.gov"
SCF_FILES = FRB + "/econres/files"
Z1_REL = FRB + "/releases/z1/20260911"            # the 2026:Q2 Z.1 release (2026-09-11), dated folder
FRED_CSV = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}"

DOWNLOADS = [
    # --- SCF 2022: summary extract public data and the program that defines its variables --------------------
    ("scf/scfp2022excel.zip", SCF_FILES + "/scfp2022excel.zip",
     "SCF 2022 Summary Extract Public Data, CSV version (zip of SCFP2022.csv; five implicates per family; page says "
     "'all dollar variables inflation-adjusted to 2025 dollars', last updated 10/9/2026)",
     "scf2022_summary.csv.gz"),
    ("scf/bulletin.macro.txt", SCF_FILES + "/bulletin.macro.txt",
     "SCF 'SAS macro - Variable Definitions' / 'Summary Extract Data Program' that creates every summary-extract "
     "variable (version posted with the 2025 survey release, last updated 10/9/2026; same URL on the 2022 page)",
     "scf2022_variables.md (definitions quoted from it); CPI adjustment factors for the 2022-dollar cross-checks"),
    ("scf/codebk2022.txt", SCF_FILES + "/codebk2022.txt",
     "SCF 2022 codebook for the full public data set (ASCII, last updated 4/3/2024): question text, X-variable "
     "definitions, survey design and weights (X42001)",
     "scf2022_variables.md (weight and design notes; X-variables referenced by the macro)"),
    ("scf/Networth_Flowchart.pdf", SCF_FILES + "/Networth%20Flowchart.pdf",
     "SCF 'Net Worth Flowchart' (PDF): how NETWORTH is built from the summary-extract asset and debt variables",
     "scf2022_variables.md; hierarchy check of ASSET/DEBT/NETWORTH"),
    ("scf/scf_2022.htm", FRB + "/econres/scf_2022.htm",
     "Federal Reserve page '2022 Survey of Consumer Finances' as of the pull date (file list, last-updated dates, "
     "the 2025-dollar note, record counts)", "provenance (README_fed.md)"),
    ("scf/scf-documentation.htm", FRB + "/econres/scf-documentation.htm",
     "Federal Reserve page 'SCF: Description of files and technical documentation' as of the pull date",
     "provenance and definitions (README_fed.md)"),
    ("scf/scfindex.htm", FRB + "/econres/scfindex.htm",
     "Federal Reserve page 'Survey of Consumer Finances (SCF)', current survey (2025) as of the pull date",
     "provenance: shows the 2025 survey release (README_fed.md)"),
    # --- Bulletin articles (cross-checks) ----------------------------------------------------------------------
    ("scf/scf23.pdf", FRB + "/publications/files/scf23.pdf",
     "Aladangady, Bricker, Chang, Goodman, Krimmel, Moore, Reber, Volz and Windle, 'Changes in U.S. Family "
     "Finances from 2019 to 2022: Evidence from the Survey of Consumer Finances', Federal Reserve Bulletin, "
     "October 2023 (PDF; amounts in 2022 dollars)",
     "cross-checks: Table 2 (net worth by usual-income percentile), homeownership and home-value rows"),
    ("scf/scf26.pdf", FRB + "/publications/files/scf26.pdf",
     "Federal Reserve Bulletin article on the 2025 SCF ('Changes in U.S. Family Finances from 2022 to 2025', "
     "October 2026, PDF; amounts in 2025 dollars, 2022 columns restated in 2025 dollars)",
     "cross-check of the re-issued 2022 extract in 2025 dollars; scf2025_summary.csv.gz cross-checks"),
    # --- SCF historic tables (Fed estimates for every survey year, public and internal data) ------------------
    ("scf/scf2025_tables_public_real_historical.xlsx", SCF_FILES + "/scf2025_tables_public_real_historical.xlsx",
     "SCF historic Bulletin tables estimated from the PUBLIC data, all survey years 1989-2025, inflation-adjusted "
     "to 2025 dollars (last updated 10/9/2026)", "cross-check of scf2022_summary.csv.gz in its own (2025) dollars"),
    ("scf/scf2025_tables_public_nominal_historical.xlsx",
     SCF_FILES + "/scf2025_tables_public_nominal_historical.xlsx",
     "SCF historic Bulletin tables estimated from the PUBLIC data, all survey years 1989-2025, nominal dollars "
     "(last updated 10/9/2026)", "cross-check: 2022 values in 2022 dollars; implied 2022->2025 price factor"),
    ("scf/scf2025_tables_internal_nominal_historical.xlsx",
     SCF_FILES + "/scf2025_tables_internal_nominal_historical.xlsx",
     "SCF historic Bulletin tables estimated from the INTERNAL data (the Bulletin's own numbers), all survey years "
     "1989-2025, nominal dollars (last updated 10/9/2026)",
     "cross-check: the Bulletin's 2022 values in 2022 dollars, public-vs-internal gap"),
    # --- SCF 2022 full public data set: only the household roster and a few KVW inputs are extracted ----------
    ("scf/scf2022s.zip", SCF_FILES + "/scf2022s.zip",
     "SCF 2022 full public data set, Stata version (zip of p22i6.dta; all ~5,300 X-variables, five implicates, "
     "nominal dollars; last updated 10/18/2023)",
     "scf2022_roster.csv.gz (household listing, PEU size) and scf2022_xvars.csv.gz (credit-card limit, pay "
     "amount and frequency)"),
    # --- SCF 2025 summary extract (released 2026-10-09; vendored beside 2022, same macro, same 2025 dollars) ----
    ("scf/scfp2025excel.zip", SCF_FILES + "/scfp2025excel.zip",
     "SCF 2025 Summary Extract Public Data, CSV version (zip of SCFP2025.csv; five implicates; 2025 dollars; "
     "released 10/9/2026)", "scf2025_summary.csv.gz (addition: the survey after 2022)"),
    ("scf/codebk2025.txt", SCF_FILES + "/codebk2025.txt",
     "SCF 2025 codebook for the full public data set (ASCII): question text of the items new in 2025 (total "
     "non-housing spending X7790, vacation spending X7791, hypothetical-windfall shares X9375-X9377)",
     "scf2022_variables.md (definitions of the 2025-only variables in scf2025_summary.csv.gz)"),
    # --- DFA ----------------------------------------------------------------------------------------------------
    ("dfa/dfa.zip", FRB + "/releases/z1/dataviz/download/zips/dfa.zip",
     "Distributional Financial Accounts, full data set ('Raw Data: CSV (ZIP)' on the DFA overview page), "
     "release of 2026-09-18 (2026:Q2 Financial Accounts)", "dfa_income_long.csv, dfa_wealth_long.csv"),
    ("dfa/dfa_public_code.zip", FRB + "/releases/z1/dataviz/download/zips/dfa_public_code.zip",
     "DFA public code package (Stata .do, R temporal-disaggregation script, documentation PDF, data dictionary, "
     "inputs), as of the 2026-09-18 release. Vendored as DOCUMENTATION ONLY: read as text, never executed",
     "group definitions (income percentile groups from SCF INCOME incl. Forbes 400; wealth groups) for README_fed.md"),
    ("dfa/dfa_overview.htm", FRB + "/releases/z1/dataviz/dfa/",
     "DFA overview page as of the pull date (group definitions, method summary, last update 2026-09-18)",
     "definitions (README_fed.md)"),
    ("dfa/dfa_announcements.htm", FRB + "/releases/z1/dataviz/dfa/announcements/",
     "DFA announcements page as of the pull date (relabelings, instrument changes, SCF incorporation dates)",
     "definitions and quirks (README_fed.md)"),
    # --- Z.1, the Board's own release (primary source of every Z.1 series FRED mirrors) ------------------------
    ("z1/z1_csv_files.zip", Z1_REL + "/z1_csv_files.zip",
     "Financial Accounts of the United States (Z.1), 2026:Q2 release of 2026-09-11: all tables as CSV with "
     "data dictionaries (dated release folder)",
     "z1_land.csv (series values); DFA aggregate cross-check against B.101.h"),
    ("z1/z1_code_changes.txt", Z1_REL + "/z1_code_changes.txt",
     "Z.1 series code changes log, 2026:Q2 release", "check that the paper's series codes were not changed"),
    # NFC structures at current cost (LM105012665, LM105013665; the paper's str_nfc_res / str_nfc_nonres) are not in
    # any table since the 2021-06-10 release; the 2021-03-11 release (2020:Q4 data) is the last that published them.
    ("z1/archive_20210311/z1_csv_files.zip", FRB + "/releases/z1/20210311/z1_csv_files.zip",
     "Z.1 2020:Q4 release of 2021-03-11, all tables as CSV (archived dated release folder): the last release whose "
     "B.103 carries NFC residential and nonresidential structures at current cost (LM105012665, LM105013665)",
     "z1_land.csv: NFC structures 1945-2020 for the paper's business/economy-wide residual (final published values)"),
    ("z1/archive_20210311/b103.htm", FRB + "/releases/z1/20210311/html/b103.htm",
     "Z.1 2021-03-11 release, table B.103 (nonfinancial corporate business balance sheet), HTML: shows the memo lines "
     "'residential/nonresidential structures, current cost basis' (LM105012665, LM105013665)",
     "evidence of the last publication of the NFC current-cost structures (README_fed.md)"),
    ("z1/archive_20210610/b103.htm", FRB + "/releases/z1/20210610/html/b103.htm",
     "Z.1 2021-06-10 release, table B.103, HTML: the current-cost structures memo lines are gone (historical-cost "
     "lines remain)", "evidence of the discontinuation (README_fed.md)"),
]

# The paper's FRED series (pinning/code/feasibility_kappa.py and three-taxes/code/fiscal_napkin.py), plus the
# quarterly twins of its annual business series, nonprofit nonresidential structures (left inside the paper's
# household residual) and households' owner-occupied real estate. FRED IDs map to Z.1 codes: BOGZ1<code><freq>.
FRED_SERIES = [
    # sid, Z.1 code, frequency, description (Z.1 label), role in the paper
    ("HNOREMV", "LM155035005", "Q", "Households and nonprofit organizations; real estate at market value; asset, level",
     "re_hh"),
    ("BOGZ1LM155012665Q", "LM155012665", "Q",
     "Households and nonprofit organizations; residential structures, current cost basis; level", "str_hh_res"),
    ("BOGZ1LM105035005A", "LM105035005", "A", "Nonfinancial corporate business; real estate at market value; level",
     "re_nfc"),
    ("BOGZ1LM115035005A", "LM115035005", "A", "Nonfinancial noncorporate business; real estate at market value; level",
     "re_nnb"),
    ("BOGZ1LM105012665Q", "LM105012665", "Q",
     "Nonfinancial corporate business; residential structures, current cost basis; level", "str_nfc_res"),
    ("BOGZ1LM105013665A", "LM105013665", "A",
     "Nonfinancial corporate business; nonresidential structures, current cost basis; level", "str_nfc_nonres"),
    ("BOGZ1LM115012665Q", "LM115012665", "Q",
     "Nonfinancial noncorporate business; residential structures, current cost basis; level", "str_nnb_res"),
    ("BOGZ1LM115013665A", "LM115013665", "A",
     "Nonfinancial noncorporate business; nonresidential structures, current cost basis; level", "str_nnb_nonres"),
    ("HHMSDODNS", "FL153165105", "Q", "Households and nonprofit organizations; home mortgages; liability, level",
     "mortg"),
    ("BOGZ1LM105035005Q", "LM105035005", "Q", "Nonfinancial corporate business; real estate at market value; level",
     "re_nfc (quarterly)"),
    ("BOGZ1LM115035005Q", "LM115035005", "Q", "Nonfinancial noncorporate business; real estate at market value; level",
     "re_nnb (quarterly)"),
    ("BOGZ1LM105013665Q", "LM105013665", "Q",
     "Nonfinancial corporate business; nonresidential structures, current cost basis; level", "str_nfc_nonres (quarterly)"),
    ("BOGZ1LM115013665Q", "LM115013665", "Q",
     "Nonfinancial noncorporate business; nonresidential structures, current cost basis; level", "str_nnb_nonres (quarterly)"),
    ("BOGZ1LM165013665Q", "LM165013665", "Q",
     "Nonprofit organizations; nonresidential structures, current cost basis; level", "memo (not in the paper)"),
]
for sid, code, freq, desc, role in FRED_SERIES:
    DOWNLOADS.append((f"fred/{sid}.csv", FRED_CSV.format(sid=sid),
                      f"FRED copy of Z.1 series {code}.{freq} ({desc}; millions of dollars), fredgraph.csv",
                      f"paper's series ID ({role}); cross-check of z1_land.csv against the Board's Z.1 CSV"))

# ---------------------------------------------------------------------------------------------------------
# 2. Download (skip vendored files; a failure is recorded and not retried unless --retry-failed).
#    After one failure on a host in a run, the remaining files on that host are not attempted in that run.
# ---------------------------------------------------------------------------------------------------------
FAIL_PATH = RAWF / "FETCH_FAILURES.csv"
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
    for rel, url, what, used in tqdm(downloads, desc="Fed downloads"):
        if (RAWF / rel).exists():
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
    mpath = RAWF / "MANIFEST.csv"
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
print("vendored files:", sum((RAWF / d[0]).exists() for d in DOWNLOADS), "of", len(DOWNLOADS),
      "| recorded failures:", len(FAILS))

# ---------------------------------------------------------------------------------------------------------
# 3. Helpers: checks log, weighted statistics, gzip CSV writer
# ---------------------------------------------------------------------------------------------------------
CHECKS = []


def check(name, computed, published, tol, unit, note="", source=""):
    """Log one cross-check. tol is an absolute tolerance in `unit`; published=None records a value without a test."""
    ok = None
    diff = None
    if published is not None and computed is not None and not (pd.isna(computed) or pd.isna(published)):
        diff = float(computed) - float(published)
        ok = abs(diff) <= tol
    CHECKS.append({"check": name, "computed": computed, "published": published, "diff": diff, "tolerance": tol,
                   "unit": unit, "pass": ok, "source": source, "note": note})
    flag = {True: "ok  ", False: "FAIL", None: "info"}[ok]
    print(f"  [{flag}] {name}: computed={computed} published={published} {unit} {note}")
    return ok


def wmedian(x, w):
    """Weighted median, SAS QNTLDEF=5 style: first value where cumulative weight passes half the total; average of
    the two neighbours when the cumulative weight hits one half exactly."""
    x = np.asarray(x, dtype=float)
    w = np.asarray(w, dtype=float)
    o = np.argsort(x, kind="mergesort")
    x, w = x[o], w[o]
    c = np.cumsum(w)
    half = c[-1] / 2.0
    k = int(np.searchsorted(c, half, side="left"))
    if np.isclose(c[k], half, rtol=0, atol=1e-9 * c[-1]) and k + 1 < len(x):
        return (x[k] + x[k + 1]) / 2.0
    return x[k]


def wmean(x, w):
    x = np.asarray(x, dtype=float)
    w = np.asarray(w, dtype=float)
    return float((x * w).sum() / w.sum())


def write_csv(df, name, gz=False):
    """Write a tidy file; gzip with mtime=0 so reruns are byte-identical."""
    path = TIDY / name
    if gz:
        df.to_csv(path, index=False, compression={"method": "gzip", "compresslevel": 9, "mtime": 0})
    else:
        df.to_csv(path, index=False)
    print(f"  wrote {path.relative_to(REPO)}: {len(df):,} rows x {df.shape[1]} cols")
    return path


# ---------------------------------------------------------------------------------------------------------
# 4. The SCF summary-extract program (bulletin.macro.txt): statements, enclosing %IF chains, year applicability.
#    Used to quote every kept variable's defining code in scf2022_variables.md (no SAS is executed).
# ---------------------------------------------------------------------------------------------------------
MACRO_LINES = (RAWF / "scf/bulletin.macro.txt").read_text(encoding="latin-1").splitlines()


def eval_cond(cond, year):
    """Evaluate a %IF condition for the public data of survey `year` with REAL=YES, ADJINC=YES (the posted extract).
    Returns None when the condition cannot be parsed, so nothing is silently assumed."""
    c = cond.strip()
    if c.startswith("(") and c.endswith(")"):
        c = c[1:-1]
    c = c.replace("&YEAR", str(year)).replace("&PUBLIC", "YES").replace("&REAL", "YES").replace("&ADJINC", "YES")
    c = re.sub(r"\b(YES|NO)\b", r"'\1'", c)
    for a, b in ((r"\bGE\b", ">="), (r"\bLE\b", "<="), (r"\bGT\b", ">"), (r"\bLT\b", "<"), (r"\bNE\b", "!="),
                 (r"\bEQ\b", "==")):
        c = re.sub(a, b, c)
    c = c.replace("^=", "!=")
    c = re.sub(r"(?<![<>!=])=(?!=)", "==", c)
    c = re.sub(r"\bAND\b|&", " and ", c)
    c = re.sub(r"\bOR\b|\|", " or ", c)
    if not re.fullmatch(r"[\s0-9'YESNO<>=!()andor]*", c):
        return None
    try:
        return bool(eval(c, {"__builtins__": {}}, {}))       # c holds only digits, quotes, comparisons, and/or
    except Exception:
        return None


DIRECTIVE = re.compile(r"%ELSE\s+%IF\s*(.*?)\s*%THEN\s*%DO\s*;|%IF\s*(.*?)\s*%THEN\s*%DO\s*;|%ELSE\s*%DO\s*;"
                       r"|%END\s*;|%DO\b[^;]*;", re.I)


def condition_map(lines, year):
    """Per line: (list of enclosing %IF/%ELSE texts, applies-at-year True/False/None)."""
    stack, last_chain, out = [], {}, []
    for ln in lines:
        for m in DIRECTIVE.finditer(ln):
            tok = m.group(0).upper()
            depth = len(stack)
            if tok.startswith("%ELSE") and "%IF" in tok:
                prev = last_chain.get(depth, [])
                v = eval_cond(m.group(1), year)
                val = None if (v is None or any(p is None for p in prev)) else (v and not any(prev))
                stack.append({"text": "%ELSE %IF " + m.group(1), "value": val, "chain": prev + [v]})
            elif tok.startswith("%IF"):
                v = eval_cond(m.group(2), year)
                stack.append({"text": "%IF " + m.group(2), "value": v, "chain": [v]})
            elif tok.startswith("%ELSE"):
                prev = last_chain.get(depth, [])
                val = None if any(p is None for p in prev) else (not any(prev))
                stack.append({"text": "%ELSE", "value": val, "chain": prev + [True]})
            elif tok.startswith("%END"):
                if stack:
                    blk = stack.pop()
                    last_chain[len(stack)] = blk["chain"]
            else:                                        # %DO loop: neutral block
                stack.append({"text": tok, "value": True, "chain": []})
        vals = [b["value"] for b in stack]
        applies = None if any(v is None for v in vals) else all(vals)
        out.append(([b["text"] for b in stack if not b["text"].startswith("%DO")], applies))
    return out


def macro_statements(lines):
    """Split SAS text into statements (code or comment), tracking line spans. Line numbers 0-based."""
    out, buf, start, kind, in_block = [], [], None, None, False
    for i, ln in enumerate(lines):
        j = 0
        while j < len(ln):
            if in_block:
                k = ln.find("*/", j)
                if k < 0:
                    buf.append(ln[j:])
                    j = len(ln)
                    continue
                buf.append(ln[j:k + 2])
                j = k + 2
                in_block = False
                if kind == "block":
                    out.append({"start": start, "end": i, "kind": "comment", "text": "\n".join(buf)})
                    buf, start, kind = [], None, None
                continue
            if start is None:
                rest = ln[j:]
                s = rest.lstrip()
                if not s:
                    break
                j += len(rest) - len(s)
                start = i
                if s.startswith("/*"):
                    kind, in_block = "block", True
                    buf.append("/*")
                    j += 2
                    continue
                kind = "comment" if (s.startswith("*") or s.startswith("%*")) else "code"
            k = ln.find(";", j)
            if kind == "code":
                b = ln.find("/*", j)
                if b >= 0 and (k < 0 or b < k):
                    buf.append(ln[j:b])
                    j = b + 2
                    in_block = True
                    continue
            if k < 0:
                buf.append(ln[j:])
                break
            buf.append(ln[j:k + 1])
            j = k + 1
            out.append({"start": start, "end": i, "kind": kind, "text": "\n".join(buf)})
            buf, start, kind = [], None, None
    return out


MACRO_STMTS = macro_statements(MACRO_LINES)
COND = {2022: condition_map(MACRO_LINES, 2022), 2025: condition_map(MACRO_LINES, 2025)}
SKIP_BACK = re.compile(r"^\s*((%ELSE\s+)?%IF\b.*%THEN\s*%DO|%ELSE\s*%DO|%END|%DO\b.*|ARRAY\b.*|DO\b.*|END)\s*;\s*$",
                       re.I | re.S)


def macro_definition(var):
    """Defining statements of `var` (with enclosing conditions and 2022/2025 applicability) and the comment above
    the first one. Returns dict(comment, stmts=[(line_from, line_to, cond_chain, applies22, applies25, text)])."""
    pat = re.compile(r"(?:^|\bTHEN\b|\bELSE\b|\bDO\b)\s*" + re.escape(var) + r"\s*=(?!=)", re.I)
    hits = [k for k, s in enumerate(MACRO_STMTS) if s["kind"] == "code" and pat.search(" ".join(s["text"].split()))]
    stmts = []
    for k in hits:
        s = MACRO_STMTS[k]
        chain, a22 = COND[2022][s["start"]]
        a25 = COND[2025][s["start"]][1]
        text = "\n".join(MACRO_LINES[s["start"]:s["end"] + 1])
        stmts.append((s["start"] + 1, s["end"] + 1, chain, a22, a25, text))
    comment = []
    if hits:
        k = hits[0] - 1
        while k >= 0 and (MACRO_STMTS[k]["kind"] == "comment" or SKIP_BACK.match(MACRO_STMTS[k]["text"])):
            if MACRO_STMTS[k]["kind"] == "comment":
                comment.insert(0, MACRO_STMTS[k]["text"])
            k -= 1
    return {"comment": " ".join(" ".join(comment).split()), "stmts": stmts}


print("macro statements parsed:", len(MACRO_STMTS))

# ---------------------------------------------------------------------------------------------------------
# 5. SCF summary extracts -> scf2022_summary.csv.gz (and scf2025_summary.csv.gz), values exactly as published
# ---------------------------------------------------------------------------------------------------------
# (variable, group, definition). Definitions paraphrase bulletin.macro.txt (its comments and code, quoted in
# scf2022_variables.md); codebook item numbers are the full-public-data X-variables the macro reads.
SCF_VARS = [
    ("YY1", "id", "Public-data family (case) identifier; identical across the family's five implicate records."),
    ("Y1", "id", "Public-data record identifier = 10*YY1 + implicate number (1-5)."),
    ("IMPLICATE", "id", "Implicate number 1-5, computed here as Y1 - 10*YY1 (not a published column)."),
    ("WGT", "id", "Analysis weight as published: WGT = X42001/5 (macro: 'divide weight by 5 so totals estimated on "
     "the 5 implicates jointly are correct'). Summed over all records (all five implicates) it gives the number of "
     "families; each implicate sums to one fifth of that. The weight differs across a family's implicates."),
    # demographics
    ("HHSEX", "demographics", "Sex of the reference person (X8021): 1=male, 2=female."),
    ("AGE", "demographics", "Age of the reference person in years (X14, reconciled age)."),
    ("AGECL", "demographics", "Age class of the reference person: 1=<35, 2=35-44, 3=45-54, 4=55-64, 5=65-74, 6=75+."),
    ("EDUC", "demographics", "Highest education of the reference person (X5931 code list, highest-degree style)."),
    ("EDCL", "demographics", "Education class of the reference person: 1=no high school diploma/GED, 2=high school "
     "diploma or GED, 3=some college or associate degree, 4=bachelor's degree or higher."),
    ("MARRIED", "demographics", "Marital status of the reference person: 1=married or living with a partner "
     "(X8023 in 1,2), 2=neither."),
    ("KIDS", "demographics", "Number of children of the reference person/spouse/partner in the household listing "
     "(relationship codes 4 child incl. in-law, 13, 36 foster [36 not in public data]) among listed persons #3-#12: "
     "any age and regardless of membership in the primary economic unit. Not a count of minors or of dependants."),
    ("LF", "demographics", "Labor force status of the reference person: 1=working in some way, 0=not working at all "
     "(X4100 in 50-80 or 97)."),
    ("LIFECL", "demographics", "Life-cycle class: 1=<55 not married/LWP no children, 2=<55 married/LWP no children, "
     "3=<55 married/LWP with children, 4=<55 not married/LWP with children, 5=55+ working, 6=55+ not working."),
    ("FAMSTRUCT", "demographics", "Family structure: 1=not married/LWP with children, 2=not married/LWP no children "
     "under 55, 3=not married/LWP no children 55+, 4=married/LWP with children, 5=married/LWP no children."),
    ("OCCAT1", "demographics", "Work status of the reference person: 1=works for someone else, 2=self-employed/"
     "partnership, 3=retired/disabled (+ student/homemaker/misc. not working and 65+), 4=other not working."),
    ("OCCAT2", "demographics", "Occupation of the reference person (public version): 1=managerial/professional, "
     "2=technical/sales/services, 3=other (production, craft, repair, operators, laborers, farming), 4=not working."),
    ("INDCAT", "demographics", "Industry of the reference person (public version): 1=mining, construction, "
     "manufacturing; 2=all other industries (internal categories 2 and 3 combined); 4=not working (OCCAT1>=3)."),
    # spending, saving and credit behaviour
    ("FOODHOME", "spending", "Annualized spending on food at home (X3024 converted from its reporting frequency X3025)."),
    ("FOODAWAY", "spending", "Annualized spending on food away from home (X3029, frequency X3030)."),
    ("FOODDELV", "spending", "Annualized spending on food delivered to the home (X3027, frequency X3028)."),
    ("RENT", "spending", "MONTHLY rent (largest of the rent amounts X602, X612, X619, X708 converted to a monthly "
     "basis); zero for owners without rent."),
    ("VACATION", "spending", "2025 ONLY (zero placeholder in 2022): annualized spending on vacations or trips over "
     "the last 12 months (X7791, frequency X7798)."),
    ("TOTSPENDNH", "spending", "2025 ONLY (zero placeholder in 2022): annualized total spending over the last 12 "
     "months on goods and services incl. food, trips, cars, appliances, clothing, utilities, insurance, "
     "transportation, education and health, EXCLUDING rent, mortgage or loan payments, investments and retirement "
     "contributions (X7790, frequency X7797)."),
    ("MPSPEND", "spending", "2025 ONLY (zero placeholder in 2022): percent of a hypothetical windfall equal to one "
     "month of the family's normal annual income that it would SPEND over the next 12 months (X9375; the three "
     "shares MPSPEND+MPSAVE+MPDEBT are asked to add to 100)."),
    ("MPSAVE", "spending", "2025 ONLY: percent of the same hypothetical windfall the family would SAVE (X9376)."),
    ("MPDEBT", "spending", "2025 ONLY: percent of the same hypothetical windfall used to PAY DOWN DEBTS (X9377)."),
    ("WSAVED", "saving", "Spending relative to income over the past year, adjusting for durables purchases and "
     "investments: 1=spending exceeded income, 2=spending equaled income, 3=spending less than income."),
    ("SAVED", "saving", "1 if spending was less than income over the past year (WSAVED=3), else 0."),
    ("SPENDMOR", "saving", "R would spend more if assets appreciated in value: 1=agree strongly ... 5=disagree "
     "strongly (X6789)."),
    ("SPENDLESS", "saving", "R would spend less if assets depreciated in value: 1=agree strongly ... 5=disagree "
     "strongly (X7492)."),
    ("EXPENSHILO", "saving", "Household's overall expenses over the last 12 months: 1=unusually high, "
     "2=unusually low, 3=normal (X7491)."),
    ("LATE", "credit", "1 if the household had any late debt payments in the last year (X3004=5)."),
    ("LATE60", "credit", "1 if the household had any payments more than 60 days past due in the last year."),
    ("HPAYDAY", "credit", "1 if the household has (had) a payday loan (X7063=1)."),
    ("BNKRUPLAST5", "credit", "1 if the household declared bankruptcy in the last five years (X6774)."),
    ("TURNDOWN", "credit", "1 if turned down for credit (X407=1)."),
    ("FEARDENIAL", "credit", "1 if did not apply for credit for fear of being denied (X441=3 or X409=1)."),
    ("TURNFEAR", "credit", "1 if TURNDOWN or FEARDENIAL."),
    ("EMERGBORR", "credit", "Hypothetical financial emergency (X7775; only asked if X7510 is not 1): 1 if would "
     "borrow from others."),
    ("EMERGSAV", "credit", "Hypothetical emergency (X7775): 1 if would spend from own savings."),
    ("EMERGPSTP", "credit", "Hypothetical emergency (X7775): 1 if would postpone payments."),
    ("EMERGCUT", "credit", "Hypothetical emergency (X7775): 1 if would cut back spending."),
    ("EMERGWORK", "credit", "Hypothetical emergency (X7775): 1 if would work more."),
    # income
    ("INCOME", "income", "Total before-tax family income in the calendar year before the survey (X5729, floored at "
     "0) plus withdrawals from IRAs and tax-deferred pension accounts (PENACCTWD). Prior-year dollars are moved to "
     "survey-year dollars by CPILAG (2022: 4315/3992; 2025: 4750/4625) before the 2025-dollar adjustment."),
    ("WAGEINC", "income", "Wage and salary income, prior calendar year (X5702)."),
    ("BUSSEFARMINC", "income", "Income from business, sole proprietorship or farm (X5704) plus from other "
     "businesses or investments, net rent, trusts or royalties (X5714); net rental income is in here."),
    ("INTDIVINC", "income", "Taxable and tax-exempt interest plus dividends (X5706+X5708+X5710)."),
    ("KGINC", "income", "Realized capital gains or losses (X5712)."),
    ("SSRETINC", "income", "Social Security, pensions, annuities and other retirement or disability programs "
     "(X5722) plus PENACCTWD."),
    ("TRANSFOTHINC", "income", "Unemployment/workers' compensation, child support/alimony, TANF/SNAP/SSI and other "
     "assistance, and other income (X5716+X5718+X5720+X5724)."),
    ("PENACCTWD", "income", "Withdrawals from IRAs and tax-deferred pension accounts, annualized; already included "
     "in INCOME and SSRETINC."),
    ("NORMINC", "income", "Usual ('normal') income: if prior-year income was not normal (X7650 not 3), the reported "
     "usual income X7362 plus PENACCTWD; otherwise INCOME. Basis of the Bulletin's 'percentile of usual income'."),
    # percentile categories (weighted, computed on all five implicates pooled)
    ("INCCAT", "categories", "Percentile group of INCOME: 1=<20, 2=20-39.9, 3=40-59.9, 4=60-79.9, 5=80-89.9, "
     "6=90-100."),
    ("NINCCAT", "categories", "Percentile group of NORMINC (usual income), same six groups as INCCAT (the "
     "Bulletin's 'percentile of usual income' rows)."),
    ("NINC2CAT", "categories", "Percentile group of NORMINC: 1=<50, 2=50-89.9, 3=90-100."),
    ("INCPCTLECAT", "categories", "Percentile group of INCOME: 1=<10, 2=10-19.9, ..., 9=80-89.9, 10=90-94.9, "
     "11=95-98.9, 12=99-100."),
    ("NINCPCTLECAT", "categories", "Percentile group of NORMINC, same twelve groups as INCPCTLECAT."),
    ("INCQRTCAT", "categories", "Quartile of INCOME: 1=<25, 2=25-49.9, 3=50-74.9, 4=75-100."),
    ("NINCQRTCAT", "categories", "Quartile of NORMINC."),
    ("NWCAT", "categories", "Percentile group of NETWORTH: 1=<25, 2=25-49.9, 3=50-74.9, 4=75-89.9, 5=90-100."),
    ("NWPCTLECAT", "categories", "Percentile group of NETWORTH, twelve groups as INCPCTLECAT."),
    ("ASSETCAT", "categories", "Percentile group of ASSET: 1=<20, 2=20-39.9, 3=40-59.9, 4=60-79.9, 5=80-89.9, "
     "6=90-100."),
    # financial assets
    ("CHECKING", "financial assets", "Checking accounts other than money market accounts."),
    ("PREPAID", "financial assets", "Prepaid card balances (X7596)."),
    ("SAVING", "financial assets", "Savings accounts."),
    ("MMDA", "financial assets", "Money market deposit accounts (at commercial banks, savings and loans, savings "
     "banks, credit unions)."),
    ("MMMF", "financial assets", "Money market mutual funds (money market accounts at other institutions)."),
    ("MMA", "financial assets", "All money market accounts = MMDA + MMMF."),
    ("CALL", "financial assets", "Call accounts at brokerages (X3930)."),
    ("LIQ", "financial assets", "All transaction accounts = CHECKING+SAVING+MMA+CALL+PREPAID, then LIQ=MAX(HLIQ,LIQ): "
     "a family that has an account but a zero total balance gets LIQ=1 before the price adjustment (=4789/4376 "
     "dollars in the 2022 file, 1 in the 2025 file)."),
    ("CDS", "financial assets", "Certificates of deposit (X3721)."),
    ("STMUTF", "financial assets", "Stock mutual funds."),
    ("TFBMUTF", "financial assets", "Tax-free bond mutual funds."),
    ("GBMUTF", "financial assets", "Government bond mutual funds."),
    ("OBMUTF", "financial assets", "Other bond mutual funds."),
    ("COMUTF", "financial assets", "Combination and other mutual funds."),
    ("OMUTF", "financial assets", "Other mutual funds (X7787)."),
    ("NMMF", "financial assets", "Directly held pooled investment funds excluding money market funds = STMUTF+"
     "TFBMUTF+GBMUTF+OBMUTF+COMUTF+OMUTF."),
    ("STOCKS", "financial assets", "Directly held stocks (X3915)."),
    ("NOTXBND", "financial assets", "Tax-exempt (state and local) bonds."),
    ("MORTBND", "financial assets", "Mortgage-backed bonds."),
    ("GOVTBND", "financial assets", "U.S. government and agency bonds and bills."),
    ("OBND", "financial assets", "Corporate and foreign bonds."),
    ("BOND", "financial assets", "Directly held bonds excluding bond funds and savings bonds = NOTXBND+MORTBND+"
     "GOVTBND+OBND."),
    ("IRAKH", "financial assets", "IRAs and Keogh accounts."),
    ("THRIFT", "financial assets", "Account-type pension plans (401(k), 403(b), thrift, savings, SRA, or any plan "
     "the participant can borrow from or withdraw from)."),
    ("FUTPEN", "financial assets", "Future pensions accumulated in an account for the reference person/spouse."),
    ("CURRPEN", "financial assets", "Account balances of pensions from which benefits are currently received."),
    ("RETQLIQ", "financial assets", "Quasi-liquid retirement accounts = IRAKH+THRIFT+FUTPEN+CURRPEN."),
    ("SAVBND", "financial assets", "U.S. savings bonds (X3902)."),
    ("CASHLI", "financial assets", "Cash value of whole life insurance (X4006)."),
    ("ANNUIT", "financial assets", "Annuities in which the household has an equity interest (X6577)."),
    ("TRUSTS", "financial assets", "Trusts and managed investment accounts with an equity interest (X6587)."),
    ("OTHMA", "financial assets", "Other managed assets = ANNUIT + TRUSTS."),
    ("OTHFIN", "financial assets", "Other financial assets: loans the household made to others, future proceeds, "
     "royalties, futures, non-public stock, deferred compensation, oil/gas/mineral investments, cash n.e.c."),
    ("FIN", "financial assets", "Total financial assets = LIQ+CDS+NMMF+STOCKS+BOND+RETQLIQ+SAVBND+CASHLI+OTHMA+OTHFIN."),
    ("EQUITY", "financial assets", "All stock held directly or indirectly: STOCKS, stock funds (full), combination "
     "funds (half), other funds, and the stock share of IRAs/Keoghs, account pensions, annuities and trusts."),
    ("DEQ", "financial assets", "Directly held equity = STOCKS + STMUTF + 0.5*COMUTF + OMUTF."),
    ("RETEQ", "financial assets", "Equity held in quasi-liquid retirement accounts."),
    # nonfinancial assets
    ("VEHIC", "nonfinancial assets", "Value of all vehicles (autos, motor homes, RVs, airplanes, boats)."),
    ("HOUSES", "nonfinancial assets", "Value of the primary residence (X604, X614, X623, X716 by housing type) plus "
     "the non-business share of a farm or ranch residence ((1-X507/10000)*(X513+X526)); 0 for non-owners."),
    ("HOUSECL", "nonfinancial assets", "Homeownership class: 1=owns ranch/farm/mobile home/house/condo/coop etc., "
     "2=otherwise."),
    ("ORESRE", "nonfinancial assets", "Other residential real estate (gross value of the family's share): 1-4 "
     "family residences other than the primary residence, time shares, vacation homes, land contracts/notes."),
    ("NNRESRE", "nonfinancial assets", "NET equity in nonresidential real estate: other real estate not classed as "
     "residential, net of mortgages and other loans taken out for investment real estate."),
    ("FARMBUS", "nonfinancial assets", "Business part of a farm/ranch primary residence net of its mortgages "
     "(counted in BUS, excluded from HOUSES)."),
    ("BUS", "nonfinancial assets", "Business interests = ACTBUS + NONACTBUS."),
    ("ACTBUS", "nonfinancial assets", "Businesses with an active management interest: net equity if sold today, plus "
     "loans from the household to the business, minus loans from the business to the household not reported "
     "elsewhere, plus personal assets pledged as collateral; includes FARMBUS."),
    ("NONACTBUS", "nonfinancial assets", "Businesses without an active interest: market value of the interest."),
    ("OTHNFIN", "nonfinancial assets", "Other nonfinancial assets (gold and other metals, jewelry, art, antiques, "
     "collections, etc.)."),
    ("NFIN", "nonfinancial assets", "Total nonfinancial assets = VEHIC+HOUSES+ORESRE+NNRESRE+BUS+OTHNFIN."),
    ("NHNFIN", "nonfinancial assets", "Nonfinancial assets excluding the primary residence = NFIN - HOUSES. 2022 "
     "FILE DEFECT: the published value is (NFIN - HOUSES) x 1.0943784 because NHNFIN appears twice in the macro's "
     "ARRAY VALUE and is price-adjusted twice; use NFIN - HOUSES. The 2025 file is unaffected (CPIADJ = 1)."),
    ("ASSET", "nonfinancial assets", "Total assets = FIN + NFIN."),
    # debts
    ("MRTHEL", "debts", "Debt secured by the primary residence: first, second and third mortgages (X805, X905, "
     "X1005) plus home equity lines of credit (HELOC)."),
    ("NH_MORT", "debts", "Mortgages on the primary residence excluding HELOCs = MRTHEL - HELOC."),
    ("HELOC", "debts", "Home equity lines of credit secured by the primary residence."),
    ("HOMEEQ", "debts", "Home equity = HOUSES - MRTHEL (macro: 'home value less all home secured debt')."),
    ("RESDBT", "debts", "Debt on other residential property (mortgages and land contracts on ORESRE properties, "
     "vacation homes, and loans for such property)."),
    ("OTHLOC", "debts", "Other lines of credit not secured by the primary residence."),
    ("CCBAL", "debts", "Credit card balances after the last payment, incl. revolving store accounts "
     "(X427+X413+X421+X7575)."),
    ("NOCCBAL", "debts", "1 if no credit card balance remained after the last payment (convenience use only)."),
    ("BNPL", "debts", "Buy-now-pay-later balances (X443; 2022 onward); included in INSTALL."),
    ("VEH_INST", "debts", "Vehicle installment loans."),
    ("EDN_INST", "debts", "Education installment loans."),
    ("OTH_INST", "debts", "Other installment loans = INSTALL - VEH_INST - EDN_INST."),
    ("INSTALL", "debts", "Total installment loans (vehicle, education, other consumer loans, BNPL)."),
    ("ODEBT", "debts", "Other debts: loans against pensions or life insurance, margin loans, miscellaneous."),
    ("DEBT", "debts", "Total debt = MRTHEL+RESDBT+OTHLOC+CCBAL+INSTALL+ODEBT."),
    ("NETWORTH", "debts", "Net worth = ASSET - DEBT."),
    # unrealized capital gains
    ("KGHOUSE", "capital gains", "Unrealized capital gain on the primary residence: current value less purchase "
     "price and improvements (farm business part removed)."),
    ("KGORE", "capital gains", "Unrealized gain on other real estate: current value less purchase price, by share "
     "owned."),
    ("KGBUS", "capital gains", "Unrealized gain on businesses: current value less tax basis."),
    ("KGSTMF", "capital gains", "Unrealized gain on stocks and mutual funds."),
    ("KGTOTAL", "capital gains", "Total unrealized gains = KGHOUSE+KGORE+KGBUS+KGSTMF."),
    # payments and ratios
    ("TPAY", "payments", "Total MONTHLY debt payments."),
    ("MORTPAY", "payments", "Monthly payments on mortgages, HELOCs and other residential debt."),
    ("CONSPAY", "payments", "Monthly payments on non-mortgage, non-revolving consumer debt."),
    ("REVPAY", "payments", "Monthly payments on revolving debt (credit cards, BNPL, lines of credit other than HELOCs)."),
    ("PIRTOTAL", "payments", "Ratio of monthly debt payments to monthly income: TPAY/max(INCOME/12, small floor)."),
    ("PIR40", "payments", "1 if PIRTOTAL > 0.4."),
    ("LEVRATIO", "payments", "Leverage ratio DEBT/ASSET (1 if debt but no assets; 0 if no debt)."),
    ("DEBT2INC", "payments", "Debt-to-income ratio DEBT/INCOME (10 if debt but no income; 0 if no debt)."),
]
SCF_2025_ONLY = ["VACATION", "TOTSPENDNH", "MPSPEND", "MPSAVE", "MPDEBT"]


def macro_dollar_vars():
    """Names in the macro's ARRAY VALUE{*} (the variables multiplied by CPIADJ when REAL=YES)."""
    s = next(st for st in MACRO_STMTS if st["kind"] == "code" and re.match(r"\s*ARRAY\s+VALUE\{\*\}", st["text"]))
    names = []
    for tok in " ".join(s["text"].split()).rstrip(";").split()[2:]:
        m = re.fullmatch(r"([A-Z_]+?)(\d+)-([A-Z_]+?)(\d+)", tok)
        if m:
            names += [f"{m.group(1)}{k}" for k in range(int(m.group(2)), int(m.group(4)) + 1)]
        else:
            names.append(tok)
    return set(names)


DOLLAR_VARS = macro_dollar_vars()
CPI = {"cpiadj_2022": 4789 / 4376, "cpilag_2022": 4315 / 3992, "cpiadj_2025": 4789 / 4789, "cpilag_2025": 4750 / 4625}
# the factors above are read off the macro; confirm they are what the macro says
_mac = "\n".join(MACRO_LINES)
assert "%LET CPIADJ=&CPIBASE/4376;" in _mac and "%LET CPILAG=4315/3992;" in _mac
assert "%LET CPIADJ=&CPIBASE/4789;" in _mac and "%LET CPILAG=4750/4625;" in _mac
assert "%BULLIT(YEAR=2022,REAL=YES,ADJINC=YES,CPIBASE=4789,PUBLIC=YES);" in _mac


def unit_of(v):
    if v in ("YY1", "Y1", "IMPLICATE"):
        return "id"
    if v == "WGT":
        return "families (weight)"
    if v in DOLLAR_VARS:
        return "2025 dollars" + (" per month" if v in ("RENT", "TPAY", "MORTPAY", "CONSPAY", "REVPAY") else "")
    if v in ("MPSPEND", "MPSAVE", "MPDEBT"):
        return "percent"
    if v == "AGE":
        return "years"
    if v in ("KIDS",):
        return "count"
    if v in ("PIRTOTAL", "LEVRATIO", "DEBT2INC"):
        return "ratio"
    return "code"


def read_scfp(year):
    """The summary-extract CSV as published: every column as text (so values are written back unchanged) and a
    numeric copy for checks."""
    z = zipfile.ZipFile(RAWF / f"scf/scfp{year}excel.zip")
    name = f"SCFP{year}.csv"
    assert z.namelist() == [name], z.namelist()
    with z.open(name) as fh:
        txt = pd.read_csv(fh, dtype=str, keep_default_na=False)
    num = txt.apply(pd.to_numeric, errors="coerce")
    nonnum = {c: int(num[c].isna().sum()) for c in num.columns if num[c].isna().any()}
    kept = [v for v, g, d in SCF_VARS if v in num.columns]
    assert not [c for c in kept if c in nonnum], f"SCF {year}: non-numeric cells in kept variables: {nonnum}"
    if nonnum:
        print(f"  SCF {year}: non-numeric cells (SAS special missing, e.g. 'B') only in unkept columns: {nonnum}")
    return txt, num


def build_scfp(year):
    txt, num = read_scfp(year)
    keep = [v for v, g, d in SCF_VARS if v != "IMPLICATE" and (year == 2025 or v not in SCF_2025_ONLY)]
    missing = [v for v in keep if v not in txt.columns]
    assert not missing, f"SCF {year}: variables not in the extract: {missing}"
    out = txt[keep].copy()
    imp = (num["Y1"] - 10 * num["YY1"]).astype(int)
    out.insert(2, "IMPLICATE", imp.astype(str))
    write_csv(out, f"scf{year}_summary.csv.gz", gz=True)
    return txt, num, out


print("\n[SCF] summary extracts")
SCF_TXT22, SCF22, SCF_OUT22 = build_scfp(2022)
SCF_TXT25, SCF25, SCF_OUT25 = build_scfp(2025)
print("  2022 extract columns:", SCF_TXT22.shape[1], "| kept:", SCF_OUT22.shape[1], "| 2025 kept:", SCF_OUT25.shape[1])

# ---------------------------------------------------------------------------------------------------------
# 6. SCF checks: structure, weights, hierarchies, and published comparators (parsed from vendored files)
# ---------------------------------------------------------------------------------------------------------
def page_text(rel):
    soup = BeautifulSoup((RAWF / rel).read_bytes(), "lxml")
    for t in soup(["script", "style", "noscript"]):
        t.decompose()
    return " ".join(soup.get_text(" ").split())


def pnum(s):
    return float(s.replace(",", "").replace("–", "-").replace("−", "-"))


NUMRE = r"[–−-]?[\d,]*\.?\d+"


def pdf_find_page(rel, pattern):
    with pdfplumber.open(RAWF / rel) as pdf:
        for i, p in enumerate(pdf.pages):
            t = p.extract_text() or ""
            if re.search(pattern, t):
                return i + 1, t
    raise ValueError(f"{rel}: no page matches {pattern!r}")


def row_numbers(text, label, after=None, n=None):
    """Numbers on the first line that starts with `label` (searching after the line `after` if given)."""
    lines = text.splitlines()
    k0 = 0
    if after is not None:
        k0 = next(k for k, l in enumerate(lines) if l.strip() == after) + 1
    for l in lines[k0:]:
        if l.startswith(label + " "):
            nums = re.findall(NUMRE, l[len(label):])
            vals = [pnum(x) for x in nums]
            if n is not None:
                assert len(vals) >= n, (label, l)
                vals = vals[:n]
            return vals
    raise ValueError(f"row {label!r} not found")


USUAL = ["Less than 20", "20–39.9", "40–59.9", "60–79.9", "80–89.9", "90–100"]


def bulletin_values(rel, y0, y1):
    """Table 2 (net worth by usual income) and Table 3 primary-residence row of a Bulletin article, as dicts in
    the article's thousands of dollars. Columns: (median y0, median y1, pct, mean y0, mean y1, pct)."""
    pg2, t2 = pdf_find_page(rel, r"Table 2\. Family median and mean net worth")
    out = {"page_table2": pg2, "all": row_numbers(t2, "All families", n=6)}
    for k, lab in enumerate(USUAL, start=1):
        out[f"ninccat{k}"] = row_numbers(t2, lab, after="Percentile of usual income", n=6)
    pg3, t3 = pdf_find_page(rel, r"Table 3\. Holding and values of assets")
    out["page_table3"] = pg3
    out["primary_residence"] = row_numbers(t3, "Primary residence", n=8)   # pct y0, pct y1, med y0, med y1, chg,
    #                                                                       mean y0, mean y1, chg
    pgb, tb = pdf_find_page(rel, r"Number of families represented")
    out["page_families"] = pgb
    out["families"] = {y: float(re.search(rf"(?m)^{y} (\d{{3}}\.\d)\b", tb).group(1)) for y in (y0, y1)}
    return out


def historic_sheet(rel, sheet):
    wb = openpyxl.load_workbook(RAWF / rel, read_only=True, data_only=True)
    rows = [list(r) for r in wb[sheet].iter_rows(values_only=True)]
    wb.close()
    return rows


def historic_t4(rel, year):
    """Historic Table 4 (net worth by family characteristics): All families and the 'Percentile of income' rows for
    `year` as {key: (median, mean)} in the table's thousands of dollars."""
    rows = historic_sheet(rel, "Table 4")
    hdr = next(r for r in rows if r and r[0] == "Family characteristic")
    col = hdr.index(year)
    assert rows[rows.index(hdr) + 1][col] == "Median" and rows[rows.index(hdr) + 1][col + 1] == "Mean"
    out, block = {}, None
    for r in rows:
        lab = (r[0] or "").strip() if isinstance(r[0], str) else r[0]
        if lab == "All families":
            out["all"] = (r[col], r[col + 1])
        if isinstance(lab, str) and not isinstance(r[1], (int, float)):
            block = lab
        if block == "Percentile of income" and lab in USUAL:
            out[f"inccat{USUAL.index(lab) + 1}"] = (r[col], r[col + 1])
    return out


def historic_t9(rel, year):
    """Historic Table 9 for one survey: primary residence percent holding, conditional median and mean (All
    families), in the table's units."""
    yy = str(year)[2:]
    pm = historic_sheet(rel, f"Table 9 {yy} %s & medians")
    mm = historic_sheet(rel, f"Table 9 {yy} means")
    hdr = next(r for r in pm if r and r[0] == "Family characteristic")
    col = hdr.index("Primary residence")
    alls = [r for r in pm if r and r[0] == "All families"]
    assert len(alls) == 2, "expected one percent-holding and one median block"
    hdr_m = next(r for r in mm if r and r[0] == "Family characteristic")
    mean_all = next(r for r in mm if r and r[0] == "All families")
    return {"pct": alls[0][col], "median": alls[1][col], "mean": mean_all[hdr_m.index("Primary residence")]}


def scf_stats(num):
    """Weighted statistics (all five implicates pooled with WGT), thousands of the file's dollars."""
    w = num["WGT"].to_numpy()
    own = (num["HOUSES"] > 0).to_numpy()
    st = {"families_m": w.sum() / 1e6,
          "own_rate_houses": 100 * w[own].sum() / w.sum(),
          "own_rate_housecl": 100 * w[(num["HOUSECL"] == 1).to_numpy()].sum() / w.sum(),
          "houses_mean_owners": wmean(num["HOUSES"][own], w[own]) / 1e3,
          "houses_median_owners": wmedian(num["HOUSES"][own], w[own]) / 1e3,
          "nw_median": wmedian(num["NETWORTH"], w) / 1e3,
          "nw_mean": wmean(num["NETWORTH"], w) / 1e3}
    for cat in ("NINCCAT", "INCCAT"):
        for k in range(1, 7):
            m = (num[cat] == k).to_numpy()
            st[f"{cat.lower()}{k}"] = (wmedian(num["NETWORTH"][m], w[m]) / 1e3, wmean(num["NETWORTH"][m], w[m]) / 1e3,
                                       100 * w[m].sum() / w.sum())
    return st


def scf_structure_checks(year, num, src_page):
    yy = f"scf{year}"
    n_fam = num["YY1"].nunique()
    imp = num["Y1"] - 10 * num["YY1"]
    check(f"{yy}: Y1 = 10*YY1 + implicate with implicates 1-5", int(imp.between(1, 5).all() and
          (num.groupby("YY1").size() == 5).all()), 1, 0, "bool")
    if src_page:
        t = page_text(src_page)
        m = re.search(r"there are ([\d,]+) records in the public data set for ([\d,]+) families", t)
        check(f"{yy}: records in the extract", len(num), pnum(m.group(1)), 0, "records", source=src_page)
        check(f"{yy}: families in the extract", n_fam, pnum(m.group(2)), 0, "families", source=src_page)
    w = num["WGT"]
    per_imp = w.groupby(imp).sum()
    check(f"{yy}: WGT summed over all records / 1e6 (= number of families, not 5x)", round(w.sum() / 1e6, 4),
          None, 0, "million families")
    check(f"{yy}: max relative spread of per-implicate WGT sums", float(per_imp.max() / per_imp.min() - 1), 0,
          1e-6, "ratio", note="each implicate sums to one fifth of the families")
    nvary = int((num.groupby("YY1")["WGT"].nunique() > 1).sum())
    check(f"{yy}: families whose WGT differs across implicates", nvary, None, 0, "families",
          note="weights are implicate-specific; never average a family's implicates without its own weights")
    # hierarchies (published values carry ~8 significant digits, so allow relative rounding)
    rules = [("ASSET", ["FIN", "NFIN"], []), ("NETWORTH", ["ASSET"], ["DEBT"]),
             ("DEBT", ["MRTHEL", "RESDBT", "OTHLOC", "CCBAL", "INSTALL", "ODEBT"], []),
             ("FIN", ["LIQ", "CDS", "NMMF", "STOCKS", "BOND", "RETQLIQ", "SAVBND", "CASHLI", "OTHMA", "OTHFIN"], []),
             ("NFIN", ["VEHIC", "HOUSES", "ORESRE", "NNRESRE", "BUS", "OTHNFIN"], []),
             ("BUS", ["ACTBUS", "NONACTBUS"], []), ("HOMEEQ", ["HOUSES"], ["MRTHEL"]),
             ("MRTHEL", ["NH_MORT", "HELOC"], []), ("MMA", ["MMDA", "MMMF"], []),
             ("NMMF", ["STMUTF", "TFBMUTF", "GBMUTF", "OBMUTF", "COMUTF", "OMUTF"], []),
             ("BOND", ["NOTXBND", "MORTBND", "GOVTBND", "OBND"], []),
             ("RETQLIQ", ["IRAKH", "THRIFT", "FUTPEN", "CURRPEN"], []), ("OTHMA", ["ANNUIT", "TRUSTS"], []),
             ("INSTALL", ["VEH_INST", "EDN_INST", "OTH_INST"], []),
             ("KGTOTAL", ["KGHOUSE", "KGORE", "KGBUS", "KGSTMF"], [])]
    f = CPI[f"cpiadj_{year}"]
    for tot, plus, minus in rules:
        # the macro leaves dollar values of exactly -1 or -2 unadjusted ('IF VALUE{I} NOT IN(-1 -2)'), so undo the
        # published price adjustment term by term (keep -1/-2, divide the rest by CPIADJ) and test in nominal terms
        cols = [tot] + plus + minus
        coded = num[cols].isin([-1, -2])
        nom = num[cols].where(coded, num[cols] / f)
        calc = nom[plus].sum(axis=1) - (nom[minus].sum(axis=1) if minus else 0)
        dev = (nom[tot] - calc).abs() * f
        scale = num[cols].abs().sum(axis=1)
        bad = int((dev > 1e-7 * scale + 0.01).sum())
        ncoded = int(coded.any(axis=1).sum())
        check(f"{yy}: {tot} = {'+'.join(plus)}{''.join('-' + m for m in minus)} (records off by more than "
              f"rounding)", bad, 0, 0, "records", note=f"max abs deviation ${dev.max():,.4f}" +
              (f"; {ncoded} records with a -1/-2 component left unadjusted by the macro (allowed for)" if ncoded
               and f != 1 else ""))
    # NHNFIN appears twice in the macro's ARRAY VALUE, so in a real-dollar extract it is multiplied by CPIADJ twice
    m = (num["NFIN"] - num["HOUSES"]).abs() > 1
    ratio = num["NHNFIN"][m] / (num["NFIN"] - num["HOUSES"])[m]
    check(f"{yy}: NHNFIN / (NFIN-HOUSES) on {int(m.sum())} records (publisher double-adjusts NHNFIN)",
          round(float(ratio.median()), 7), round(f, 7), 1e-6, "ratio",
          note=f"range {ratio.min():.7f}-{ratio.max():.7f}; NHNFIN is listed twice in ARRAY VALUE. Use NFIN-HOUSES "
               f"instead of NHNFIN" if f != 1 else "no effect when CPIADJ=1")
    liq_parts = num[["CHECKING", "SAVING", "MMA", "CALL", "PREPAID"]].sum(axis=1)
    dev = (num["LIQ"] - liq_parts).abs()
    marker = CPI[f"cpiadj_{year}"]
    is_marker = (liq_parts == 0) & np.isclose(num["LIQ"], marker, rtol=1e-7, atol=1e-6)
    bad = int(((dev > 1e-6 * num["LIQ"].abs().clip(lower=1) + 0.01) & ~is_marker).sum())
    check(f"{yy}: LIQ = CHECKING+SAVING+MMA+CALL+PREPAID except the LIQ=MAX(HLIQ,LIQ) marker", bad, 0, 0, "records",
          note=f"{int(is_marker.sum())} records have zero balances but an account: LIQ={marker:.6f} (=1 x CPIADJ)")


print("\n[SCF] checks")
scf_structure_checks(2022, SCF22, "scf/scf_2022.htm")
scf_structure_checks(2025, SCF25, "scf/scfindex.htm")
ST22, ST25 = scf_stats(SCF22), scf_stats(SCF25)
B23 = bulletin_values("scf/scf23.pdf", 2019, 2022)       # thousands of 2022 dollars (internal data)
B26 = bulletin_values("scf/scf26.pdf", 2022, 2025)       # thousands of 2025 dollars (internal data)
PUB_REAL, PUB_NOM, INT_NOM = ("scf/scf2025_tables_public_real_historical.xlsx",
                              "scf/scf2025_tables_public_nominal_historical.xlsx",
                              "scf/scf2025_tables_internal_nominal_historical.xlsx")
F22 = CPI["cpiadj_2022"]                                 # 2022 -> 2025 dollars (Fed's own factor, 4789/4376)
check("macro factor 2022->2025 dollars (CPIBASE 4789 / Sept-2022 CPI-U-RS 4376)", round(F22, 6), None, 0, "ratio")
# implied factor from the Fed's own public tables (real 2025$ / nominal) for 2022
t4r, t4n = historic_t4(PUB_REAL, 2022), historic_t4(PUB_NOM, 2022)
check("historic public tables: 2022 mean net worth real/nominal = macro factor", round(t4r["all"][1] / t4n["all"][1], 5),
      round(F22, 5), 2e-5, "ratio", source="Table 4, public real vs nominal")
t4i = historic_t4(INT_NOM, 2022)
check("historic internal-data table, 2022 median net worth = 2023 Bulletin Table 2", t4i["all"][0], B23["all"][1],
      0.05, "thousand 2022 $", source=f"{INT_NOM} Table 4 vs scf23.pdf p{B23['page_table2']}")
check("historic internal-data table, 2022 mean net worth = 2023 Bulletin Table 2", t4i["all"][1], B23["all"][4],
      0.05, "thousand 2022 $", source=f"{INT_NOM} Table 4 vs scf23.pdf p{B23['page_table2']}")

for year, st, b, pub in ((2022, ST22, B26, PUB_REAL), (2025, ST25, B26, PUB_REAL)):
    t4, t9 = historic_t4(pub, year), historic_t9(pub, year)
    col_med, col_mean = (0, 3) if year == 2022 else (1, 4)
    yy = f"scf{year}"
    check(f"{yy}: families (million) vs Bulletin", round(st["families_m"], 2), b["families"][year], 0.05,
          "million", source=f"scf26.pdf p{b['page_families']}")
    # exact comparator: the Fed's own public-data tables in 2025 dollars
    check(f"{yy}: median net worth vs historic PUBLIC table", round(st["nw_median"], 3), t4["all"][0], 0.006,
          "thousand 2025 $", source=f"{pub} Table 4")
    check(f"{yy}: mean net worth vs historic PUBLIC table", round(st["nw_mean"], 3), t4["all"][1], 0.006,
          "thousand 2025 $", source=f"{pub} Table 4")
    for k in range(1, 7):
        check(f"{yy}: median/mean net worth, INCOME percentile group {k}, vs historic PUBLIC table",
              round(st[f"inccat{k}"][0], 3), t4[f"inccat{k}"][0], 0.006, "thousand 2025 $",
              note=f"mean computed {st[f'inccat{k}'][1]:.3f} vs table {t4[f'inccat{k}'][1]}", source=f"{pub} Table 4")
        check(f"{yy}: mean net worth, INCOME percentile group {k}, vs historic PUBLIC table",
              round(st[f"inccat{k}"][1], 3), t4[f"inccat{k}"][1], 0.006, "thousand 2025 $", source=f"{pub} Table 4")
    check(f"{yy}: homeownership (HOUSES>0) vs historic PUBLIC table", round(st["own_rate_houses"], 3), t9["pct"],
          0.006, "percent", note=f"HOUSECL==1 gives {st['own_rate_housecl']:.3f}", source=f"{pub} Table 9")
    check(f"{yy}: median HOUSES of owners vs historic PUBLIC table", round(st["houses_median_owners"], 3),
          t9["median"], 0.006, "thousand 2025 $", source=f"{pub} Table 9")
    check(f"{yy}: mean HOUSES of owners vs historic PUBLIC table", round(st["houses_mean_owners"], 3), t9["mean"],
          0.006, "thousand 2025 $", source=f"{pub} Table 9")
    # Bulletin (internal data, so close but not identical): 2026 article, thousands of 2025 dollars
    rel = 0.03
    src = f"scf26.pdf p{b['page_table2']}"
    check(f"{yy}: median net worth vs 2026 Bulletin (internal data)", round(st["nw_median"], 1),
          b["all"][col_med], rel * b["all"][col_med], "thousand 2025 $", source=src, note="tolerance 3%")
    check(f"{yy}: mean net worth vs 2026 Bulletin (internal data)", round(st["nw_mean"], 1), b["all"][col_mean],
          rel * b["all"][col_mean], "thousand 2025 $", source=src, note="tolerance 3%")
    for k in range(1, 7):
        bm, bmean = b[f"ninccat{k}"][col_med], b[f"ninccat{k}"][col_mean]
        check(f"{yy}: median net worth, USUAL-income group {k} (NINCCAT) vs 2026 Bulletin", round(st[f"ninccat{k}"][0], 1),
              bm, max(0.10 * abs(bm), 2.0), "thousand 2025 $", source=src, note="tolerance 10% (internal vs public data)")
        check(f"{yy}: mean net worth, USUAL-income group {k} (NINCCAT) vs 2026 Bulletin", round(st[f"ninccat{k}"][1], 1),
              bmean, 0.10 * abs(bmean), "thousand 2025 $", source=src, note="tolerance 10% (internal vs public data)")
    pr = b["primary_residence"]
    i0 = 0 if year == 2022 else 1
    src3 = f"scf26.pdf p{b['page_table3']}"
    check(f"{yy}: homeownership vs 2026 Bulletin Table 3", round(st["own_rate_houses"], 2), pr[i0], 0.1, "percent",
          source=src3)
    check(f"{yy}: median HOUSES of owners vs 2026 Bulletin Table 3", round(st["houses_median_owners"], 1), pr[2 + i0],
          0.03 * pr[2 + i0], "thousand 2025 $", source=src3, note="tolerance 3%")
    check(f"{yy}: mean HOUSES of owners vs 2026 Bulletin Table 3", round(st["houses_mean_owners"], 1),
          pr[5 + i0], 0.03 * pr[5 + i0], "thousand 2025 $", source=src3, note="tolerance 3%")

# the two Bulletins agree: the 2026 article's 2022 column = the 2023 article's 2022 column x 4789/4376
worst = 0.0
for key in ["all"] + [f"ninccat{k}" for k in range(1, 7)]:
    for i23, i26 in ((1, 0), (4, 3)):                    # medians, means
        worst = max(worst, abs(B23[key][i23] * F22 - B26[key][i26]))
for i23, i26 in ((3, 2), (6, 5)):                        # primary residence conditional median, mean
    worst = max(worst, abs(B23["primary_residence"][i23] * F22 - B26["primary_residence"][i26]))
check("Bulletins: 2026 article's 2022 column = 2023 article x 4789/4376 (Table 2 all + 6 usual-income rows, Table 3 "
      "primary residence; worst abs diff)", round(worst, 3), 0, 0.15, "thousand 2025 $",
      note="tolerance covers rounding of both articles to 0.1")

# 2025-only spending items against the 2026 Bulletin's Box 1 (internal data, 2025 dollars)
pgx, tx = pdf_find_page("scf/scf26.pdf", r"With respect to total nonhousing expenditure")   # not the contents page
tx = " ".join(tx.split())
pgy, ty = pdf_find_page("scf/scf26.pdf", r"Box 1\u2014continued")
ty = " ".join(ty.split())


def box(pattern, text=tx):
    m = re.search(pattern, text)
    assert m, pattern
    return [pnum(g) for g in m.groups()]


w25 = SCF25["WGT"]
sp = SCF25["TOTSPENDNH"]
src = f"scf26.pdf Box 1 p{pgx}"
mean_b, med_b = box(r"families spent \$([\d,]+), on average.*?Median total spending was \$([\d,]+)")
check("scf2025: mean TOTSPENDNH vs 2026 Bulletin Box 1", round(wmean(sp, w25)), mean_b, 0.03 * mean_b, "2025 dollars",
      source=src, note="tolerance 3% (internal vs public data)")
check("scf2025: median TOTSPENDNH vs 2026 Bulletin Box 1", round(wmedian(sp, w25)), med_b, 0.03 * med_b, "2025 dollars",
      source=src, note="tolerance 3%")
agg_b = box(r"Aggregate spending across all families over the previous 12 months was \$([\d.]+) trillion")[0]
check("scf2025: aggregate TOTSPENDNH vs 2026 Bulletin Box 1", round(float((sp * w25).sum()) / 1e12, 3), agg_b, 0.03 * agg_b,
      "trillion 2025 dollars", source=src, note="tolerance 3%")
q1_b, q1s_b = box(r"bottom quintile of the usual income distribution was \$([\d,]+), ([\d.]+) percent of overall")
p80_b = box(r"to \$([\d,]+) among families in the 80th to 90th percentiles of usual income")[0]
top_b, tops_b = box(r"spent an average of \$([\d,]+), nearly double.*?accounted for ([\d.]+) percent of overall")
for k, val, lab in ((1, q1_b, "bottom quintile"), (5, p80_b, "80th-90th"), (6, top_b, "top decile")):
    m = SCF25["NINCCAT"] == k
    check(f"scf2025: mean TOTSPENDNH, usual income {lab} (NINCCAT={k}) vs Box 1", round(wmean(sp[m], w25[m])), val,
          0.05 * val, "2025 dollars", source=src, note="tolerance 5%")
for k, val, lab in ((1, q1s_b, "bottom quintile"), (6, tops_b, "top decile")):
    m = SCF25["NINCCAT"] == k
    check(f"scf2025: share of aggregate TOTSPENDNH, usual income {lab} vs Box 1",
          round(100 * float((sp * w25)[m].sum() / (sp * w25).sum()), 2), val, 1.0, "percent", source=src,
          note="tolerance 1 point")
nwq1_b = box(r"\$([\d,]+) among fami- ?lies in the bottom quintile of wealth")[0]
nwtop_b, nwtops_b = box(r"Families in the top decile, however, spent an average of \$([\d,]+) for the year, "
                        r"accounting for ([\d.]+) percent")
for cats, val, lab in (([1, 2], nwq1_b, "bottom wealth quintile (NWPCTLECAT 1-2)"),
                       ([10, 11, 12], nwtop_b, "top wealth decile (NWPCTLECAT 10-12)")):
    m = SCF25["NWPCTLECAT"].isin(cats)
    check(f"scf2025: mean TOTSPENDNH, {lab} vs Box 1", round(wmean(sp[m], w25[m])), val, 0.05 * val, "2025 dollars",
          source=src, note="tolerance 5%")
fh_b, fhm_b, fa_b, fam_b = box(r"average of \$([\d,]+) \(median of \$([\d,]+)\) on food at home and \$([\d,]+) "
                               r"\(median of \$([\d,]+)\) on food away", ty)
va_b, vam_b, vz_b = box(r"vacation spending across all families averaged \$([\d,]+) over the past year \(median "
                        r"\$([\d,]+)\), ([\d.]+) percent of families", ty)
src2 = f"scf26.pdf Box 1 p{pgy}"
# the Box's 'food away from home' is FOODAWAY + FOODDELV (dining out plus delivered food): FOODAWAY alone is ~12% low
for var, mb, medb in (("FOODHOME", fh_b, fhm_b), ("FOODAWAY+FOODDELV", fa_b, fam_b), ("VACATION", va_b, vam_b)):
    x = SCF25[var.split("+")].sum(axis=1)
    check(f"scf2025: mean {var} vs Box 1", round(wmean(x, w25)), mb, 0.05 * mb, "2025 dollars", source=src2,
          note="tolerance 5%" + ("; Box 'food away from home' = FOODAWAY + FOODDELV" if "+" in var else ""))
    check(f"scf2025: median {var} vs Box 1", round(wmedian(x, w25)), medb, 0.05 * medb + 50, "2025 dollars",
          source=src2, note="tolerance 5% + $50")
check("scf2025: percent of families with zero VACATION vs Box 1", round(100 * float(w25[SCF25["VACATION"] == 0].sum() /
      w25.sum()), 1), vz_b, 1.5, "percent", source=src2, note="tolerance 1.5 points")
mp = SCF25["MPSPEND"] + SCF25["MPSAVE"] + SCF25["MPDEBT"]
check("scf2025: windfall shares MPSPEND+MPSAVE+MPDEBT = 100 (weighted share of families)",
      round(100 * float(w25[mp.round(6) == 100].sum() / w25.sum()), 2), None, 0, "percent",
      note=f"others sum to {sorted(mp[(mp.round(6) != 100)].round(2).unique())[:5]} (equal-split rounding); zero-sum "
           f"records {int((mp == 0).sum())}; weighted means: spend {wmean(SCF25['MPSPEND'], w25):.1f}, save "
           f"{wmean(SCF25['MPSAVE'], w25):.1f}, pay debt {wmean(SCF25['MPDEBT'], w25):.1f} percent")

# the 2022 extract against the 2023 Bulletin, after dividing by the Fed's 2022->2025 factor
src = f"scf23.pdf p{B23['page_table2']}"
check("scf2022: families (million) vs 2023 Bulletin Table B.6", round(ST22["families_m"], 2), B23["families"][2022],
      0.05, "million", source=f"scf23.pdf p{B23['page_families']}")
check("scf2022: median net worth / factor vs 2023 Bulletin", round(ST22["nw_median"] / F22, 1), B23["all"][1],
      0.03 * B23["all"][1], "thousand 2022 $", source=src, note="tolerance 3% (internal vs public data)")
check("scf2022: mean net worth / factor vs 2023 Bulletin", round(ST22["nw_mean"] / F22, 1), B23["all"][4],
      0.03 * B23["all"][4], "thousand 2022 $", source=src, note="tolerance 3%")
for k in range(1, 7):
    check(f"scf2022: median net worth / factor, usual-income group {k} vs 2023 Bulletin",
          round(ST22[f"ninccat{k}"][0] / F22, 1), B23[f"ninccat{k}"][1], max(0.10 * abs(B23[f'ninccat{k}'][1]), 2.0),
          "thousand 2022 $", source=src, note="tolerance 10%")
    check(f"scf2022: mean net worth / factor, usual-income group {k} vs 2023 Bulletin",
          round(ST22[f"ninccat{k}"][1] / F22, 1), B23[f"ninccat{k}"][4], 0.10 * abs(B23[f'ninccat{k}'][4]),
          "thousand 2022 $", source=src, note="tolerance 10%")
pr = B23["primary_residence"]
src3 = f"scf23.pdf p{B23['page_table3']}"
check("scf2022: homeownership vs 2023 Bulletin Table 3", round(ST22["own_rate_houses"], 2), pr[1], 0.1, "percent",
      source=src3)
check("scf2022: median HOUSES of owners / factor vs 2023 Bulletin Table 3", round(ST22["houses_median_owners"] / F22, 1),
      pr[3], 0.03 * pr[3], "thousand 2022 $", source=src3, note="tolerance 3%")
check("scf2022: mean HOUSES of owners / factor vs 2023 Bulletin Table 3", round(ST22["houses_mean_owners"] / F22, 1),
      pr[6], 0.03 * pr[6], "thousand 2022 $", source=src3, note="tolerance 3%")

# ---------------------------------------------------------------------------------------------------------
# 7. SCF 2022 full public data: household roster (PEU membership, adults) and a few KVW inputs
# ---------------------------------------------------------------------------------------------------------
# household listing, positions #1-#12 (codebk2022.txt 'HOUSEHOLD LISTING'); #1 reference person, #2 spouse/partner
ROSTER = {
    "REL": ["X8020", "X102", "X108", "X114", "X120", "X126", "X132", "X202", "X208", "X214", "X220", "X226"],
    "AGE": ["X8022", "X104", "X110", "X116", "X122", "X128", "X134", "X204", "X210", "X216", "X222", "X228"],
    "MARITAL": ["X8023", "X105", "X111", "X117", "X123", "X129", "X135", "X205", "X211", "X217", "X223", "X229"],
    "LIVES_HERE": ["X8024", "X106", "X112", "X118", "X124", "X130", "X136", "X206", "X212", "X218", "X224", "X230"],
    "FIN_DEP": ["X8098", "X107", "X113", "X119", "X125", "X131", "X137", "X207", "X213", "X219", "X225", "X231"],
}
XFAM = ["X42001", "X101", "X7001", "X7050", "X7020", "X8000", "X414", "X4112", "X4113", "X4712", "X4713"]


def read_full_2022(cols):
    z = zipfile.ZipFile(RAWF / "scf/scf2022s.zip")
    assert z.namelist() == ["p22i6.dta"], z.namelist()
    b = io.BytesIO(z.read("p22i6.dta"))
    d = pd.read_stata(b, columns=[c.lower() for c in cols], convert_categoricals=False)
    d.columns = [c.upper() for c in d.columns]
    return d


print("\n[SCF] 2022 full public data: roster and selected X-variables")
FULL = read_full_2022(["YY1", "Y1"] + XFAM + sum(ROSTER.values(), []))
FULL["IMPLICATE"] = (FULL["Y1"] - 10 * FULL["YY1"]).astype(int)
XDOLLAR = ["X42001", "X414", "X4112", "X4712"]                 # weight and dollar amounts (may carry cents)
for c in ["YY1", "Y1"] + XFAM + sum(ROSTER.values(), []):
    v = FULL[c]
    assert (v == v.round()).all() or c in XDOLLAR, c             # every roster/code variable is integer-valued
pos_rows = []
for k in range(12):
    blk = pd.DataFrame({"YY1": FULL["YY1"].astype(int), "Y1": FULL["Y1"].astype(int), "IMPLICATE": FULL["IMPLICATE"],
                        "POSITION": k + 1})
    for key, cols in ROSTER.items():
        blk[key] = FULL[cols[k]].astype(int)
    blk = blk[blk["REL"] != 0]
    if k == 0:
        blk["IN_PEU"] = 1
    elif k == 1:
        blk["IN_PEU"] = (FULL.loc[blk.index, "X7020"] == 2).astype(int)
    else:
        blk["IN_PEU"] = (blk["FIN_DEP"] == 1).astype(int)          # every listed person under 18 is coded 1
    blk["ADULT"] = (blk["AGE"] >= 18).astype(int)
    pos_rows.append(blk)
ROST = pd.concat(pos_rows).sort_values(["Y1", "POSITION"]).reset_index(drop=True)
write_csv(ROST, "scf2022_roster.csv.gz", gz=True)

cnt = ROST.groupby("Y1").agg(N_PEU=("IN_PEU", "sum"),
                             N_ADULTS_PEU=("IN_PEU", lambda s: int((s * ROST.loc[s.index, "ADULT"]).sum())),
                             N_LISTED=("REL", "size"))
XV = FULL[["YY1", "Y1", "IMPLICATE"] + XFAM].copy()
for c in ["YY1", "Y1"] + [c for c in XFAM if c not in XDOLLAR]:
    XV[c] = XV[c].astype(int)
XV = XV.merge(cnt, left_on="Y1", right_index=True, how="left", validate="one_to_one")
XV["N_MINORS_PEU"] = XV["N_PEU"] - XV["N_ADULTS_PEU"]
XV = XV[["YY1", "Y1", "IMPLICATE", "X42001", "X101", "X7001", "X7050", "X7020", "X8000", "N_PEU", "N_ADULTS_PEU",
         "N_MINORS_PEU", "N_LISTED", "X414", "X4112", "X4113", "X4712", "X4713"]]
write_csv(XV, "scf2022_xvars.csv.gz", gz=True)

check("scf2022 full data: records", len(FULL), len(SCF22), 0, "records", note="same 22,975 records as the extract")
check("scf2022 full data: derived PEU size (rule) = X7001 on every record", int((XV["N_PEU"] != XV["X7001"]).sum()), 0,
      0, "records off", note="rule: #1 always; #2 if X7020=2; #3-#12 if financially dependent (code 1)")
check("scf2022 full data: X101 = X7001 + persons outside the PEU (X7050, -1=none)",
      int((XV["X101"] != XV["X7001"] + XV["X7050"].clip(lower=0)).sum()), 0, 0, "records off")
jj = SCF22[["Y1", "WGT", "KIDS", "MARRIED", "AGE"]].merge(XV[["Y1", "X42001"]], on="Y1", validate="one_to_one")
check("scf2022: extract WGT x 5 = full-data X42001 (relative, max over records)",
      float(((jj["WGT"] * 5 - jj["X42001"]).abs() / jj["X42001"]).max()), 0, 1e-7, "ratio",
      note="WGT = X42001/5, published to ~8 significant digits")
kids = ROST[(ROST["POSITION"] >= 3) & ROST["REL"].isin([4, 13, 36])].groupby("Y1").size()
jj["KIDS_ROSTER"] = jj["Y1"].map(kids).fillna(0).astype(int)
check("scf2022: extract KIDS = roster count of relationship 4/13/36 in positions #3-#12",
      int((jj["KIDS"] != jj["KIDS_ROSTER"]).sum()), 0, 0, "records off")
r1 = ROST[ROST["POSITION"] == 1].set_index("Y1")
jj["MAR1"] = jj["Y1"].map(r1["MARITAL"])
check("scf2022: extract MARRIED=1 iff X8023 in (1,2)", int(((jj["MARRIED"] == 1) != jj["MAR1"].isin([1, 2])).sum()),
      0, 0, "records off")
w = SCF22.set_index("Y1")["WGT"]
xa = XV.set_index("Y1")
adults_m = float((xa["N_ADULTS_PEU"] * w).sum() / 1e6)
peu_m = float((xa["N_PEU"] * w).sum() / 1e6)
check("scf2022: weighted adults in PEUs (million, derived)", round(adults_m, 2), None, 0, "million",
      note=f"persons in PEUs {peu_m:.2f} million; mean adults per family {adults_m / ST22['families_m']:.3f}")
out_peu = ROST[(ROST["IN_PEU"] == 0) & (ROST["ADULT"] == 1)].groupby("Y1").size()
adults_out_m = float((xa.index.map(out_peu).fillna(0).to_numpy() * w.reindex(xa.index).to_numpy()).sum() / 1e6)
check("scf2022: weighted listed adults OUTSIDE the PEU (million, derived)", round(adults_out_m, 2), None, 0, "million",
      note="household members aged 18+ in the listing who are not in the PEU (not covered by SCF balance sheets)")

# ---------------------------------------------------------------------------------------------------------
# 8. scf2022_variables.md: every kept variable, its definition, unit, and the macro/codebook text behind it
# ---------------------------------------------------------------------------------------------------------
CODEBOOK = {2022: (RAWF / "scf/codebk2022.txt").read_text(encoding="latin-1").splitlines(),
            2025: (RAWF / "scf/codebk2025.txt").read_text(encoding="latin-1").splitlines()}


def codebook_entry(var, year=2022, max_lines=40):
    """The codebook block that starts with `var` (alone or as '#1' of a roster group), up to the next variable."""
    lines = CODEBOOK[year]
    pat = re.compile(rf"^{re.escape(var)}(\(#\d+[ab]?\))?(\s|$)")
    starts = [k for k, l in enumerate(lines) if pat.match(l)]
    starts = [k for k in starts if k > 400] or starts            # skip the variable lists near the top
    if not starts:
        return None
    k0 = starts[0]
    out = [lines[k0]]
    roster = re.match(r"^X\d+\(#1\)", lines[k0]) is not None
    for l in lines[k0 + 1:k0 + 200]:
        m = re.match(r"^X\d+(\(#(\d+)[ab]?\))?", l)
        if m and not (roster and m.group(2) and int(m.group(2)) >= 2):
            break
        if l.startswith("-----"):
            break
        out.append(l)
    while out and not out[-1].strip():
        out.pop()
    return "\n".join(out[:max_lines]) + ("\n[... truncated]" if len(out) > max_lines else "")


def applies_txt(a):
    return {True: "yes", False: "no", None: "?"}[a]


md = ["# SCF summary-extract variables kept in the tidy files", "",
      "Files: `scf2022_summary.csv.gz` (SCF 2022, 22,975 records = 4,595 families x 5 implicates) and "
      "`scf2025_summary.csv.gz` (SCF 2025, 21,800 records = 4,360 families x 5 implicates). Values are written "
      "exactly as published (text copied, no float round trip); `IMPLICATE` is the only added column.", "",
      "Generated by `consumption/code/acquire_fed.py` from the vendored raw files. Definitions below are close "
      "paraphrases of the Federal Reserve's summary-extract program `bulletin.macro.txt` (raw/fed/scf/, the 'SAS "
      "macro - Variable Definitions' linked from the SCF 2022 page; this is the version re-posted with the 2025 "
      "survey on 2026-10-09). Under each definition the macro's own comment and defining statements are quoted "
      "with line numbers, each tagged with whether it applies to the 2022 and 2025 public data (the %IF chain is "
      "evaluated for YEAR=2022/2025, PUBLIC=YES, REAL=YES, ADJINC=YES; '?' would mark an unparsed condition). "
      "X-variable texts are in `codebk2022.txt` / `codebk2025.txt`.", "",
      "## Conventions that apply to every variable", "",
      f"* **Dollars.** Every dollar variable in BOTH files is in **2025 dollars**. The posted extracts are the "
      f"macro's REAL=YES run with CPIBASE=4789 (September 2025 R-CPI-U-RS x 100). For 2022 every dollar value was "
      f"multiplied by CPIADJ = 4789/4376 = {CPI['cpiadj_2022']:.6f} (4376 = September 2022 R-CPI-U-RS x 100); for "
      f"2025 CPIADJ = 1. To restate the 2022 file in 2022 dollars (the 2023 Bulletin's units) divide by "
      f"{CPI['cpiadj_2022']:.6f}. Dollar values of exactly -1 or -2 are left unadjusted by the macro.",
      f"* **Income timing.** Income variables refer to the calendar year before the survey (2021 for the 2022 "
      f"survey, 2024 for 2025) and are first moved to survey-year dollars by CPILAG (2022: 4315/3992 = "
      f"{CPI['cpilag_2022']:.6f}; 2025: 4750/4625 = {CPI['cpilag_2025']:.6f}), then by CPIADJ. Nominal 2021 "
      f"income = 2022-file value / ({CPI['cpilag_2022']:.6f} x {CPI['cpiadj_2022']:.6f}).",
      "* **Weights and implicates.** `WGT = X42001/5`. Summed over ALL records (all five implicates) it gives the "
      "number of families (131.31 million in 2022, 134.96 million in 2025); each implicate sums to one fifth. The "
      "full public data's X42001 sums to five times the number of families. Weighted statistics are computed on "
      "all records pooled with WGT (this reproduces the Fed's public-data tables exactly); standard errors need "
      "the replicate weights and the multiple-imputation formula (not done here).",
      "* **Percentile categories** (INCCAT, NINCCAT, ...) are weighted percentiles over all records pooled, so a "
      "family's category can differ across its implicates.",
      "* **Unit of observation** is the primary economic unit (PEU): the economically dominant single person or "
      "couple and everyone in the household financially interdependent with them (codebook, 'Unit of analysis').",
      "* **Known publisher-side defect:** in the 2022 file `NHNFIN` is multiplied by CPIADJ twice (it is listed "
      "twice in the macro's `ARRAY VALUE`), so NHNFIN = (NFIN - HOUSES) x 1.0943784 on every record. Use "
      "NFIN - HOUSES. The 2025 file is unaffected (CPIADJ = 1).",
      "* **2025-only items.** VACATION, TOTSPENDNH, MPSPEND, MPSAVE, MPDEBT were first asked in 2025; the 2022 "
      "extract carries them as zero placeholders, so they are dropped from `scf2022_summary.csv.gz` and kept in "
      "`scf2025_summary.csv.gz`.", "",
      "## Variable table", "",
      "| variable | group | unit | in 2022 file | in 2025 file | definition |", "|---|---|---|---|---|---|"]
for v, g, d in SCF_VARS:
    in22 = "no (2025 only)" if v in SCF_2025_ONLY else "yes"
    md.append(f"| `{v}` | {g} | {unit_of(v)} | {in22} | yes | {d} |")
md += ["", "## Definitions with the macro text", ""]
for v, g, d in SCF_VARS:
    md += [f"### {v}", "", f"*{g}; unit: {unit_of(v)}.* {d}", ""]
    if v == "IMPLICATE":
        md += ["Not in the macro: added by acquire_fed.py as Y1 - 10*YY1.", ""]
        continue
    if v in ("YY1", "Y1"):
        md += ["Macro: `%IF (&PUBLIC NE YES OR &YEAR EQ 1989) %THEN %DO; %LET ID=X1; %LET IID=XX1; %END; %ELSE "
               "%DO; %LET ID=Y1; %LET IID=YY1; %END;` (public data use Y1/YY1).", ""]
        continue
    if v.endswith("CAT") and v not in ("HOUSECL",) and v in ("INCCAT", "NINCCAT", "NINC2CAT", "INCPCTLECAT",
                                                             "NINCPCTLECAT", "INCQRTCAT", "NINCQRTCAT", "NWCAT",
                                                             "NWPCTLECAT", "ASSETCAT"):
        call = [l.strip() for l in MACRO_LINES if l.strip().startswith("%PCTL(") and
                f"TAG={v[:-3]})" in l.replace(" ", "")]
        md += ["Macro: computed after the main data step by `%MACRO PCTL`: records are sorted by the variable, the "
               "cumulative WGT share is computed over all records (all implicates pooled), and each record gets the "
               "category whose lower percentile point it has reached. Call:", "", "```sas"] + call + ["```", ""]
        continue
    dfn = macro_definition(v)
    if dfn["comment"]:
        md += [f"Macro comment: “{dfn['comment'].lstrip('*% ').rstrip(';')}”", ""]
    if not dfn["stmts"]:
        md += ["(no defining statement found in the macro)", ""]
        continue
    md += ["<details><summary>macro statements</summary>", "", "```sas"]
    for a, b, chain, a22, a25, text in dfn["stmts"]:
        cond = (" | within: " + " > ".join(chain)) if chain else ""
        md.append(f"/* lines {a}-{b}; applies 2022: {applies_txt(a22)}, 2025: {applies_txt(a25)}{cond} */")
        md.append(text)
    md += ["```", "", "</details>", ""]
md += ["## Full-public-data variables (scf2022_roster.csv.gz, scf2022_xvars.csv.gz)", "",
       "From the SCF 2022 full public data set (`scf2022s.zip`, Stata file p22i6.dta, 10/18/2023). These are raw "
       "X-variables in NOMINAL dollars where they are dollar amounts (not price-adjusted), plus counts derived "
       "here. Codebook text quoted from `codebk2022.txt`.", ""]
for v in ["X101", "X7001", "X7050", "X7020", "X8000", "X8020", "X8022", "X8023", "X8024", "X8098", "X414", "X4112",
          "X4113"]:
    e = codebook_entry(v)
    md += [f"### {v}", "", "```text", e if e else "(entry not found)", "```", ""]
md += ["### 2025-only summary variables: codebook text (codebk2025.txt)", ""]
for v in ["X7790", "X7791", "X9375"]:
    e = codebook_entry(v, 2025, max_lines=45)
    md += ["```text", e if e else "(entry not found)", "```", ""]
(TIDY / "scf2022_variables.md").write_text("\n".join(md) + "\n", encoding="utf-8")
print(f"  wrote consumption/data/tidy/scf2022_variables.md ({len(md)} lines)")

# ---------------------------------------------------------------------------------------------------------
# 9. DFA -> dfa_income_long.csv, dfa_wealth_long.csv (values as published; one row per date/group/category/measure)
# ---------------------------------------------------------------------------------------------------------
DFA_GROUPS = {
    "income": {"pct00to20": "income percentile 0-20", "pct20to40": "income percentile 20-40",
               "pct40to60": "income percentile 40-60", "pct60to80": "income percentile 60-80",
               "pct80to99": "income percentile 80-99", "pct99to100": "income percentile 99-100 (top 1%)"},
    "networth": {"Bottom50": "wealth percentile 0-50 (bottom 50%)", "Next40": "wealth percentile 50-90 (next 40%)",
                 "Next9": "wealth percentile 90-99 (next 9%)", "RemainingTop1": "wealth percentile 99-99.9 (next 0.9%)",
                 "TopPt1": "wealth percentile 99.9-100 (top 0.1%)"},
}
DFA_PARENT = {
    "Net worth": "", "Assets": "Net worth (+)", "Liabilities": "Net worth (-)",
    "Nonfinancial assets": "Assets", "Financial assets": "Assets",
    "Real estate": "Nonfinancial assets", "Consumer durables": "Nonfinancial assets",
    "Deposits": "Financial assets", "Money market fund shares": "Financial assets", "Debt securities": "Financial assets",
    "Loans (Assets)": "Financial assets", "Corporate equities and mutual fund shares": "Financial assets",
    "Life insurance reserves": "Financial assets", "Annuities": "Financial assets",
    "DC pension entitlements": "Financial assets", "DB pension entitlements": "Financial assets",
    "Miscellaneous other equity": "Financial assets", "Miscellaneous assets": "Financial assets",
    "U.S. government and municipal securities": "Debt securities", "Corporate and foreign bonds": "Debt securities",
    "Other loans and advances (Assets)": "Loans (Assets)", "Mortgages": "Loans (Assets)",
    "Loans (Liabilities)": "Liabilities", "Deferred and unpaid life insurance premiums": "Liabilities",
    "Home mortgages": "Loans (Liabilities)", "Consumer credit": "Loans (Liabilities)",
    "Depository institutions loans n.e.c.": "Loans (Liabilities)",
    "Other loans and advances (Liabilities)": "Loans (Liabilities)",
    "Household count": "memo", "Minimum Income Cutoff": "memo", "Maximum Income Cutoff": "memo",
    "Minimum Wealth Cutoff": "memo",
    # summary-file categories that are not in the detail files (renamed where a detail label already exists)
    "DC pension entitlements incl. annuities": "Assets (summary file: = DC pension entitlements + Annuities)",
    "Unincorporated businesses": "Assets (summary file: = Miscellaneous other equity)",
    "Other assets": "Assets (summary file residual)", "Other liabilities": "Liabilities (summary file residual)",
}
DFA_CHILDREN = {}
for c, par in DFA_PARENT.items():
    if par in DFA_PARENT and par not in ("memo",):
        DFA_CHILDREN.setdefault(par, []).append(c)


def read_dfa(name):
    z = zipfile.ZipFile(RAWF / "dfa/dfa.zip")
    with z.open(name) as fh:
        return pd.read_csv(fh, dtype=str, keep_default_na=False)


def dfa_num(df):
    out = df.copy()
    for c in out.columns[2:]:
        out[c] = pd.to_numeric(out[c].replace({"NA": np.nan, "": np.nan}))
    return out


def dfa_long(dim):
    lv, ld = read_dfa(f"dfa-{dim}-levels.csv"), read_dfa(f"dfa-{dim}-levels-detail.csv")
    sv, sd = read_dfa(f"dfa-{dim}-shares.csv"), read_dfa(f"dfa-{dim}-shares-detail.csv")
    for df in (lv, ld, sv, sd):
        assert list(df.columns[:2]) == ["Date", "Category"]
        assert (df[["Date", "Category"]].values == ld[["Date", "Category"]].values).all(), "row order differs"
    nlv, nld, nsv, nsd = dfa_num(lv), dfa_num(ld), dfa_num(sv), dfa_num(sd)
    memo = [c for c in ld.columns[2:] if DFA_PARENT.get(c) == "memo"]
    # summary vs detail: identical labels must carry identical values (except the summary 'DC', which adds annuities)
    for summ, det, kind in ((nlv, nld, "levels"), (nsv, nsd, "shares")):
        for c in summ.columns[2:]:
            if c in det.columns and c != "DC pension entitlements":
                d = (summ[c].fillna(-9) - det[c].fillna(-9)).abs()
                tol = 0 if kind == "levels" else 0.1 + 1e-9        # shares: one rounding step at most
                check(f"dfa {dim} {kind}: summary '{c}' = detail '{c}' (max abs diff)", float(d.max()), 0, tol,
                      "$ million" if kind == "levels" else "percentage points",
                      note=f"{int((d > 0).sum())} of {len(d)} cells differ" if (d > 0).any() else "")
    check(f"dfa {dim} levels: summary 'DC pension entitlements' = detail DC + Annuities (max abs diff, $M)",
          float((nlv["DC pension entitlements"] - nld["DC pension entitlements"] - nld["Annuities"]).abs().max()), 0, 2,
          "$ million", note="the summary/visualization 'DC' includes individual annuities")
    check(f"dfa {dim} levels: summary 'Unincorporated businesses' = detail 'Miscellaneous other equity'",
          float((nlv["Unincorporated businesses"] - nld["Miscellaneous other equity"]).abs().max()), 0, 0, "$ million")
    oth = nld["Assets"] - nlv[["Real estate", "Consumer durables", "Corporate equities and mutual fund shares",
                               "DB pension entitlements", "DC pension entitlements", "Unincorporated businesses"]].sum(axis=1)
    check(f"dfa {dim} levels: summary 'Other assets' = Assets - the six named summary assets (max abs diff)",
          float((nlv["Other assets"] - oth).abs().max()), 0, 3, "$ million")
    check(f"dfa {dim} levels: summary 'Other liabilities' = Liabilities - Home mortgages - Consumer credit",
          float((nlv["Other liabilities"] - (nld["Liabilities"] - nld["Home mortgages"] - nld["Consumer credit"]))
                .abs().max()), 0, 3, "$ million")
    for c in memo:
        check(f"dfa {dim}: memo '{c}' identical in levels and shares detail files",
              int(nld[c].fillna(-9).equals(nsd[c].fillna(-9))), 1, 0, "bool")
    # detail hierarchy
    for par, kids in DFA_CHILDREN.items():
        if par in ("Net worth (+)", "Net worth (-)") or par.startswith("Assets (") or par.startswith("Liab"):
            continue
        if par not in nld.columns:
            continue
        kids_d = [k for k in kids if k in nld.columns]
        dev = (nld[par] - nld[kids_d].sum(axis=1)).abs()
        check(f"dfa {dim} levels: {par} = sum of {len(kids_d)} components (max abs diff)", float(dev.max()), 0,
              len(kids_d), "$ million", note=" + ".join(kids_d))
    dev = (nld["Liabilities"] - nld[["Loans (Liabilities)", "Deferred and unpaid life insurance premiums"]].sum(axis=1)).abs()
    check(f"dfa {dim} levels: Liabilities = Loans (Liabilities) + deferred premiums (max abs diff)", float(dev.max()),
          0, 2, "$ million")
    dev = (nld["Net worth"] - (nld["Assets"] - nld["Liabilities"])).abs()
    check(f"dfa {dim} levels: Net worth = Assets - Liabilities (max abs diff)", float(dev.max()), 0, 2, "$ million")
    # shares: sum to 100 across groups, and match level/total
    ng = nld["Category"].nunique()
    s_sum = nsd.groupby("Date")[[c for c in nsd.columns[2:] if c not in memo]].sum(min_count=1)
    worst = float((s_sum - 100).abs().where(s_sum.notna()).max().max())
    check(f"dfa {dim} shares: published shares sum to 100 over the {ng} groups (worst |sum-100|)", round(worst, 3), 0,
          0.05 * ng + 0.01, "percentage points", note="shares are rounded to 0.1")
    tot = nld.groupby("Date")[[c for c in nld.columns[2:] if c not in memo]].transform("sum")
    calc = 100 * nld[[c for c in nld.columns[2:] if c not in memo]] / tot
    diff = (calc - nsd[[c for c in nld.columns[2:] if c not in memo]]).abs()
    big = diff.where(tot.abs() > 20000)              # aggregates above $20bn: rounding of levels to $1M negligible
    small = diff.where(tot.abs() <= 20000)
    check(f"dfa {dim} shares: published share = level / all-group total, aggregates > $20bn (worst abs diff)",
          round(float(big.max().max()), 3), 0, 0.06, "percentage points",
          note=f"{int(big.notna().sum().sum())} cells; tolerance 0.05 rounding + 0.01 for shares computed from unrounded "
               f"internal levels")
    check(f"dfa {dim} shares: same, aggregates <= $20bn (level rounding to $1M matters)",
          round(float(small.max().max()), 3), None, 0, "percentage points", note=f"{int(small.notna().sum().sum())} cells")
    # long format
    rows = []
    for df, measure, unit_fn, table in ((ld, "level", None, "detail"), (sd, "share", None, "detail"),
                                         (lv, "level", None, "summary"), (sv, "share", None, "summary")):
        for c in df.columns[2:]:
            if table == "detail" and measure == "share" and c in memo:
                continue                                  # memo items repeat the levels file
            if table == "summary" and c in ld.columns and c != "DC pension entitlements":
                continue                                  # identical to the detail row (checked above)
            cat = "DC pension entitlements incl. annuities" if (table == "summary" and c == "DC pension entitlements") else c
            if c in memo:
                unit = "households" if c == "Household count" else "dollars"
            else:
                unit = "millions of dollars" if measure == "level" else "percent of the all-household total"
            part = pd.DataFrame({"date": df["Date"].str.replace(":", "", regex=False), "group": df["Category"],
                                 "category": cat, "measure": measure, "value": df[c], "unit": unit, "table": table})
            rows.append(part)
    out = pd.concat(rows, ignore_index=True)
    out = out[out["value"] != ""]                         # cutoffs are published only at SCF survey quarters
    out["value"] = out["value"].replace({"NA": ""})      # 'NA' shares (0/0) kept as empty values
    out.insert(2, "group_label", out["group"].map(DFA_GROUPS[dim]))
    assert out["group_label"].notna().all()
    out["parent"] = out["category"].map(DFA_PARENT)
    assert out["parent"].notna().all(), set(out.loc[out["parent"].isna(), "category"])
    assert not out.duplicated(["date", "group", "category", "measure"]).any()
    gorder = {g: k for k, g in enumerate(DFA_GROUPS[dim])}
    corder = {c: k for k, c in enumerate(DFA_PARENT)}
    out = out.sort_values(["date", "group", "measure", "category"], key=lambda s: s.map(gorder) if s.name == "group"
                          else (s.map(corder) if s.name == "category" else s)).reset_index(drop=True)
    return out, nld


print("\n[DFA]")
DFA_INC, DFA_INC_LV = dfa_long("income")
DFA_WLT, DFA_WLT_LV = dfa_long("networth")
write_csv(DFA_INC, "dfa_income_long.csv")
write_csv(DFA_WLT, "dfa_wealth_long.csv")
for dim, lvl in (("income", DFA_INC_LV), ("networth", DFA_WLT_LV)):
    dates = sorted(lvl["Date"].unique(), key=lambda d: (int(d[:4]), int(d[-1])))
    full = pd.period_range(dates[0].replace(":", ""), dates[-1].replace(":", ""), freq="Q")
    check(f"dfa {dim}: quarters {dates[0]}..{dates[-1]} complete and every group every quarter",
          int(len(dates) == len(full) and (lvl.groupby("Date").size() == len(DFA_GROUPS[dim])).all()), 1, 0, "bool",
          note=f"{len(dates)} quarters")
# the two splits distribute the same aggregate
agg_i = DFA_INC_LV.groupby("Date")[["Net worth", "Real estate", "Corporate equities and mutual fund shares",
                                    "Household count"]].sum()
agg_w = DFA_WLT_LV.groupby("Date")[["Net worth", "Real estate", "Corporate equities and mutual fund shares",
                                    "Household count"]].sum()
rel = ((agg_i - agg_w).abs() / agg_w.abs()).max()
for c in agg_i.columns:
    check(f"dfa: income-split total = wealth-split total, {c} (max relative diff)", float(rel[c]), 0, 1e-5, "ratio")
LATEST_Q = max(DFA_INC_LV["Date"], key=lambda d: (int(d[:4]), int(d[-1])))
print("  DFA latest quarter:", LATEST_Q)

# ---------------------------------------------------------------------------------------------------------
# 10. Z.1 land and real-estate series -> z1_land.csv (Board CSV packages; the paper's FRED IDs carried alongside)
# ---------------------------------------------------------------------------------------------------------
Z1_CUR = ("z1/z1_csv_files.zip", "Z.1 2026:Q2 release (2026-09-11)")
Z1_ARC = ("z1/archive_20210311/z1_csv_files.zip", "Z.1 2020:Q4 release (2021-03-11), archived")
# (the paper's FRED ID or "" for memo series, Z.1 code as in the Board's CSV, table, package, paper role, description)
Z1_SERIES = [
    ("HNOREMV", "LM155035005.Q", "S1M_b", Z1_CUR, "re_hh",
     "Households and nonprofit organizations; real estate at market value (S1M.b line 3)"),
    ("BOGZ1LM155012665Q", "LM155012665.Q", "S1M_b", Z1_CUR, "str_hh_res",
     "Households; residential structures, current cost basis (S1M.b line 48; households only)"),
    ("HHMSDODNS", "LA153165105.Q", "D3_s", Z1_CUR, "mortg",
     "Households and nonprofit organizations; one-to-four-family residential (home) mortgages; liability; SEASONALLY "
     "ADJUSTED level (D3.s line 3): the series behind the paper's FRED HHMSDODNS (matches its cache exactly)"),
    ("", "FL153165105.Q", "S1M_b", Z1_CUR, "memo",
     "Households and nonprofit organizations; one-to-four-family residential (home) mortgages; liability; NOT "
     "seasonally adjusted balance-sheet level (S1M.b line 37; equals LA153165105 at Q4)"),
    ("", "LM155035015.Q", "S1M_b", Z1_CUR, "memo",
     "Households; owner-occupied real estate incl. vacant land and mobile homes at market value (S1M.b line 4)"),
    ("", "LM165035005.Q", "S1M_b", Z1_CUR, "memo",
     "Nonprofit organizations; real estate at market value (S1M.b line 5)"),
    ("", "LM155012605.Q", "S1M_b", Z1_CUR, "memo",
     "Households and nonprofit organizations; residential structures, current cost basis (S1M.b line 47)"),
    ("", "LM165012665.Q", "S1M_b", Z1_CUR, "memo",
     "Nonprofit organizations; residential structures, current cost basis (S1M.b line 49)"),
    ("", "LM165013665.Q", "S1M_b", Z1_CUR, "memo",
     "Nonprofit organizations; nonresidential structures, current cost basis (S1M.b line 50)"),
    ("BOGZ1LM105035005A", "LM105035005.Q", "S11_1_b", Z1_CUR, "re_nfc",
     "Nonfinancial corporate business; real estate at market value (S11.1.b line 3)"),
    ("BOGZ1LM115035005A", "LM115035005.Q", "S11_2_b", Z1_CUR, "re_nnb",
     "Nonfinancial noncorporate business; real estate at market value (S11.2.b line 3)"),
    ("", "LM115035023.Q", "S11_2_b", Z1_CUR, "memo",
     "Nonfinancial noncorporate business; residential real estate at market value (S11.2.b line 4)"),
    ("", "LM115035035.Q", "S11_2_b", Z1_CUR, "memo",
     "Nonfinancial noncorporate business; nonresidential real estate at market value (S11.2.b line 5)"),
    ("BOGZ1LM115012665Q", "FL115012665.Q", "S11_2_b", Z1_CUR, "str_nnb_res",
     "Nonfinancial noncorporate business; residential structures, current cost basis (S11.2.b line 43; FRED code LM, "
     "Board CSV code FL, same values)"),
    ("BOGZ1LM115013665A", "FL115013665.Q", "S11_2_b", Z1_CUR, "str_nnb_nonres",
     "Nonfinancial noncorporate business; nonresidential structures, current cost basis (S11.2.b line 44)"),
    ("BOGZ1LM105012665Q", "LM105012665.Q", "b103", Z1_ARC, "str_nfc_res",
     "Nonfinancial corporate business; residential structures, current cost basis (B.103 memo, last published "
     "2021-03-11; ends 2020:Q4)"),
    ("BOGZ1LM105013665A", "LM105013665.Q", "b103", Z1_ARC, "str_nfc_nonres",
     "Nonfinancial corporate business; nonresidential structures, current cost basis (B.103 memo, last published "
     "2021-03-11; ends 2020:Q4)"),
]
# how the paper annualizes each series: FRED 'A' IDs are year-end levels, FRED 'Q' IDs go through annualize() =
# the calendar-year mean of the quarterly levels (pinning/code/lambda_compute2.py)
PAPER_ANNUAL = {"re_hh": "A_mean", "str_hh_res": "A_mean", "mortg": "A_mean", "re_nfc": "A_eop", "re_nnb": "A_eop",
                "str_nfc_res": "A_mean", "str_nfc_nonres": "A_eop", "str_nnb_res": "A_mean",
                "str_nnb_nonres": "A_eop"}
_Z1_CACHE = {}


def z1_table(pkg, table):
    key = (pkg, table)
    if key not in _Z1_CACHE:
        z = zipfile.ZipFile(RAWF / pkg)
        with z.open(f"csv/{table}.csv") as fh:
            _Z1_CACHE[key] = pd.read_csv(fh, dtype=str, keep_default_na=False)
    return _Z1_CACHE[key]


def z1_series(pkg, table, code):
    d = z1_table(pkg, table)
    s = pd.to_numeric(d[code].replace({"ND": ""}), errors="raise")
    s.index = d["date"]
    s = s.dropna()
    assert s.index.str.fullmatch(r"\d{4}:Q[1-4]").all()
    return s / 1e3                                                     # $ millions -> $ billions


def qkey(d):
    return int(d[:4]) * 10 + int(d[-1])


z1_rows, Z1Q = [], {}
for sid, code, table, (pkg, release), role, desc in Z1_SERIES:
    s = z1_series(pkg, table, code)
    Z1Q[role if role != "memo" else code] = s
    years = sorted({int(d[:4]) for d in s.index})
    base = code.split(".")[0]
    for d, v in s.items():
        z1_rows.append((d.replace(":", ""), "Q", base, sid, role, desc, v, release))
    for y in years:
        q = s[[d for d in s.index if int(d[:4]) == y]]
        if f"{y}:Q4" in q.index:
            z1_rows.append((str(y), "A_eop", base, sid, role, desc, q[f"{y}:Q4"], release))
        if len(q) == 4 or (y < 1952 and len(q) == 1):            # complete years; pre-1952 Z.1 is year-end only
            z1_rows.append((str(y), "A_mean", base, sid, role, desc, q.mean(), release))

# the paper's residuals (feasibility_kappa.land_series), built with the paper's annualization of each input
A = {}
for role, how in PAPER_ANNUAL.items():
    rows = [(r[0], r[6]) for r in z1_rows if r[4] == role and r[1] == how]
    A[role] = pd.Series({int(d): v for d, v in rows})
resid_def = [
    ("LAND_HH_PAPER", "Household land residual, the paper's z1_hh: HH+NPO real estate at market value (annual mean of "
     "quarters) minus households' residential structures at current cost (annual mean)", ["re_hh"], ["str_hh_res"]),
    ("LAND_BUS_PAPER", "Business land residual implied by the paper's z1_econ minus z1_hh: NFC + NNB real estate "
     "(year-end) minus NFC residential (annual mean) and nonresidential (year-end) structures minus NNB residential "
     "(annual mean) and nonresidential (year-end) structures; ends 2020 with the NFC structures",
     ["re_nfc", "re_nnb"], ["str_nfc_res", "str_nfc_nonres", "str_nnb_res", "str_nnb_nonres"]),
    ("LAND_ECON_PAPER", "Economy-wide land residual, the paper's z1_econ = LAND_HH_PAPER + LAND_BUS_PAPER; ends 2020",
     ["re_hh", "re_nfc", "re_nnb"], ["str_hh_res", "str_nfc_res", "str_nfc_nonres", "str_nnb_res", "str_nnb_nonres"]),
    ("LAND_NNB_PAPERCONV", "Noncorporate business land residual with the paper's conventions (not a paper series): "
     "NNB real estate (year-end) minus NNB residential (annual mean) and nonresidential (year-end) structures",
     ["re_nnb"], ["str_nnb_res", "str_nnb_nonres"]),
    ("LAND_NFC_PAPERCONV", "NFC land residual with the paper's conventions (not a paper series): NFC real estate "
     "(year-end) minus NFC residential (annual mean) and nonresidential (year-end) structures; ends 2020",
     ["re_nfc"], ["str_nfc_res", "str_nfc_nonres"]),
]
for rid, desc, plus, minus in resid_def:
    yrs = sorted(set.intersection(*[set(A[r].index) for r in plus + minus]))
    for y in yrs:
        v = sum(A[r][y] for r in plus) - sum(A[r][y] for r in minus)
        z1_rows.append((str(y), "A_paper", rid, "", "residual", desc, v, "built here from the rows above"))
# consistent end-of-quarter residuals (all inputs at the same date)
qres = [("LAND_HH_Q", "Household land residual, end of quarter: LM155035005 - LM155012665", ["re_hh"], ["str_hh_res"]),
        ("LAND_HH_OWNOCC_Q", "Households-only owner-occupied land residual, end of quarter (not a paper series): "
         "LM155035015 (owner-occupied real estate, the DFA 'Real estate' concept) - LM155012665",
         ["LM155035015.Q"], ["str_hh_res"]),
        ("LAND_NNB_Q", "Noncorporate business land residual, end of quarter: LM115035005 - FL115012665 - FL115013665",
         ["re_nnb"], ["str_nnb_res", "str_nnb_nonres"]),
        ("LAND_NFC_Q", "NFC land residual, end of quarter: LM105035005 - LM105012665 - LM105013665 (ends 2020:Q4)",
         ["re_nfc"], ["str_nfc_res", "str_nfc_nonres"]),
        ("LAND_BUS_Q", "Business (NFC + NNB) land residual, end of quarter (ends 2020:Q4)",
         ["re_nfc", "re_nnb"], ["str_nfc_res", "str_nfc_nonres", "str_nnb_res", "str_nnb_nonres"])]
for rid, desc, plus, minus in qres:
    dates = sorted(set.intersection(*[set(Z1Q[r].index) for r in plus + minus]), key=qkey)
    for d in dates:
        v = sum(Z1Q[r][d] for r in plus) - sum(Z1Q[r][d] for r in minus)
        z1_rows.append((d.replace(":", ""), "Q", rid, "", "residual", desc, v, "built here from the rows above"))

Z1LAND = pd.DataFrame(z1_rows, columns=["date", "freq", "series_id", "paper_fred_id", "paper_role", "description",
                                        "value", "release"])
Z1LAND["unit"] = "billions of dollars, not seasonally adjusted, level"
Z1LAND["value"] = Z1LAND["value"].round(3)
assert not Z1LAND.duplicated(["date", "freq", "series_id"]).any()
Z1LAND = Z1LAND[["date", "series_id", "description", "value", "freq", "unit", "paper_fred_id", "paper_role", "release"]]
print("\n[Z.1]")
write_csv(Z1LAND, "z1_land.csv")


def z1v(sid, freq, date):
    col = "series_id" if (sid.startswith("LAND") or sid not in set(Z1LAND.paper_fred_id)) else "paper_fred_id"
    r = Z1LAND[(Z1LAND[col] == sid) & (Z1LAND.freq == freq) & (Z1LAND.date == str(date))]
    return float(r.value.iloc[0]) if len(r) else float("nan")


# annual .A series published by the Board equal the Q4 levels (FRED's 'A' convention = year-end)
for code, table, ta in (("LM105035005", "S11_1_b", "S11_1_i_a"), ("LM115035005", "S11_2_b", "S11_2_i_a"),
                        ("LM155035005", "S1M_b", "S1M_i_a")):
    a = pd.to_numeric(z1_table(Z1_CUR[0], ta).set_index("date")[f"{code}.A"].replace({"ND": ""}), errors="coerce").dropna()
    q = z1_series(Z1_CUR[0], table, f"{code}.Q") * 1e3
    q4 = q[[d for d in q.index if d.endswith("Q4")]]
    q4.index = [d[:4] for d in q4.index]
    common = a.index.intersection(q4.index)
    check(f"z1: {code}.A (annual table {ta}) = Q4 level of {code}.Q, {common[0]}-{common[-1]}",
          round(float((a[common] - q4[common]).abs().max()), 6), 0, 1e-6, "$ million")
# discontinued NFC structures: the archived release equals the paper's cached FRED copies (final published values)
for sid, role in (("BOGZ1LM105012665Q", "str_nfc_res"), ("BOGZ1LM105013665A", "str_nfc_nonres")):
    fp = REPO / "pinning" / "cache" / f"{sid}.csv"
    if fp.exists():
        c = pd.read_csv(fp)
        c["date"] = pd.to_datetime(c["observation_date"])
        if sid.endswith("Q"):
            c["key"] = c["date"].dt.year.astype(str) + ":Q" + c["date"].dt.quarter.astype(str)
            ours = Z1Q[role] * 1e3
        else:
            c["key"] = c["date"].dt.year.astype(str) + ":Q4"
            ours = Z1Q[role] * 1e3
        m = c.set_index("key")[sid].reindex(ours.index).dropna()
        check(f"z1: archived {role} = paper's cached FRED {sid} on all {len(m)} common dates (max abs diff)",
              round(float((ours[m.index] - m).abs().max()), 6), 0, 1e-6, "$ million", source=str(fp.relative_to(REPO)))
for sid, code, table, (pkg, release), role, desc in Z1_SERIES:
    if not sid:
        continue
    fp = next((b / f"{sid}.csv" for b in (REPO / "pinning" / "cache", REPO / "three-taxes" / "cache")
               if (b / f"{sid}.csv").exists()), None)
    if fp is None:
        continue
    c = pd.read_csv(fp)
    dts = pd.to_datetime(c["observation_date"])
    key = (dts.dt.year.astype(str) + ":Q" + dts.dt.quarter.astype(str)) if sid.endswith("A") is False or \
        sid in ("HNOREMV", "HHMSDODNS") else (dts.dt.year.astype(str) + ":Q4")
    cs = pd.Series(c[sid].astype(float).values, index=key)
    ours = Z1Q[role] * 1e3
    com = ours.index.intersection(cs.index)
    same = (ours[com] - cs[com]).abs() < 0.5
    first_diff = min((d for d in com[~same.values]), key=qkey) if (~same).any() else "none"
    check(f"z1: paper FRED ID {sid} = Z.1 {code}: identical on {int(same.sum())} of {len(com)} common dates (paper cache)",
          round(float(same.mean()), 4), None, 0, "share", source=str(fp.relative_to(REPO)),
          note=f"first differing date {first_diff} (later dates revised in the 2026:Q2 release)")
# FRED copies, if they were ever vendored (e.g. after --retry-failed): compare with the Board's values
for sid, code, freq, desc, role in FRED_SERIES:
    fp = RAWF / "fred" / f"{sid}.csv"
    if not fp.exists():
        continue
    c = pd.read_csv(fp)
    dts = pd.to_datetime(c["observation_date"])
    key = (dts.dt.year.astype(str) + ":Q" + dts.dt.quarter.astype(str)) if freq == "Q" else dts.dt.year.astype(str) + ":Q4"
    fs = pd.Series(pd.to_numeric(c[sid], errors="coerce").values, index=key).dropna()
    zs = next((Z1Q[k] for k in (role.split(" ")[0], f"{code}.Q", code) if k in Z1Q), None)
    if zs is None:
        continue
    com = fs.index.intersection(zs.index)
    check(f"fred vs Board Z.1: {sid} = {code} (max abs diff on {len(com)} dates)",
          round(float((fs[com] - zs[com] * 1e3).abs().max()), 3), 0, 0.5, "$ million", source=str(fp.relative_to(REPO)))
LAST_Z1Q = max(Z1Q["re_hh"].index, key=qkey)
check("z1: latest quarter of the current release", LAST_Z1Q, None, 0, "", note=f"NFC structures end "
      f"{max(Z1Q['str_nfc_res'].index, key=qkey)}")
neg = Z1LAND[(Z1LAND.series_id.str.startswith("LAND")) & (Z1LAND.value <= 0)]
check("z1: residual observations <= 0 (the paper drops these years)", len(neg), None, 0, "rows",
      note=", ".join(sorted(set(neg.series_id + ":" + neg.date)))[:400] if len(neg) else "none")
# 2025 against the paper's aggregates (three-taxes/data/aggregates_2025.csv)
agg = pd.read_csv(REPO / "three-taxes" / "data" / "aggregates_2025.csv", index_col=0)["value"]
for key, sid in (("land_hh_residual", "LAND_HH_PAPER"), ("hh_real_estate", "HNOREMV"), ("hh_structures",
                                                                                         "BOGZ1LM155012665Q"),
                 ("mortg", "HHMSDODNS")):
    freq = "A_paper" if sid.startswith("LAND") else "A_mean"
    ours = z1v(sid, freq, 2025)
    check(f"z1: 2025 {key} (current 2026:Q2 Z.1 vintage) vs three-taxes/data/aggregates_2025.csv", round(ours, 3),
          round(float(agg[key]), 3), round(0.005 * abs(float(agg[key])), 1), "$ billion",
          source="three-taxes/data/aggregates_2025.csv",
          note=f"diff {ours - float(agg[key]):+.1f} ({100 * (ours / float(agg[key]) - 1):+.2f}%); tolerance 0.5% for "
               f"revisions: aggregates_2025.csv came from the 2026:Q1 vintage (FRED cache ends 2026Q1); see the "
               f"exact reproduction and revision rows that follow")
# the paper's own cached vintage reproduces its 2025 numbers exactly (vintage, not method, explains any gap)
cache = {}
for sid in ("HNOREMV", "BOGZ1LM155012665Q", "HHMSDODNS"):
    for base in (REPO / "pinning" / "cache", REPO / "three-taxes" / "cache"):
        if (base / f"{sid}.csv").exists():
            c = pd.read_csv(base / f"{sid}.csv")
            cache[sid] = c[c["observation_date"].str.startswith("2025")][sid].astype(float).mean() / 1e3
            break
if len(cache) == 3:
    check("z1: paper's cached FRED vintage, 2025 land_hh_residual (mean HNOREMV - mean BOGZ1LM155012665Q)",
          round(cache["HNOREMV"] - cache["BOGZ1LM155012665Q"], 3), round(float(agg["land_hh_residual"]), 3), 0.001,
          "$ billion", source="pinning/cache/*.csv", note="same method on the paper's vintage reproduces it exactly")
    check("z1: 2025 HH real estate, current vintage minus paper's cached vintage (revision)",
          round(z1v("HNOREMV", "A_mean", 2025) - cache["HNOREMV"], 3), None, 0, "$ billion",
          note="the 2026:Q2 Z.1 release revised household real estate")
    check("z1: 2025 home mortgages (seasonally adjusted, as HHMSDODNS), current vintage minus paper's cached vintage",
          round(z1v("HHMSDODNS", "A_mean", 2025) - cache["HHMSDODNS"], 3), None, 0, "$ billion",
          note=f"the NSA balance-sheet level FL153165105 averages {z1v('FL153165105', 'A_mean', 2025):,.3f} in 2025")
for y in range(2019, 2026):
    check(f"z1: land residuals {y} (paper's way): household / business / economy-wide",
          round(z1v("LAND_HH_PAPER", "A_paper", y), 1), None, 0, "$ billion",
          note=f"business {z1v('LAND_BUS_PAPER', 'A_paper', y):,.1f}; economy {z1v('LAND_ECON_PAPER', 'A_paper', y):,.1f}; "
               f"NNB only {z1v('LAND_NNB_PAPERCONV', 'A_paper', y):,.1f}; HH real estate {z1v('HNOREMV', 'A_mean', y):,.1f}; "
               f"HH structures {z1v('BOGZ1LM155012665Q', 'A_mean', y):,.1f}")

# ---------------------------------------------------------------------------------------------------------
# 11. DFA against the Board's household balance sheet, DFA income cutoffs against the SCF, headline changes
# ---------------------------------------------------------------------------------------------------------
print("\n[DFA vs Z.1, DFA vs SCF]")
S14 = z1_table(Z1_CUR[0], "S14_b").copy()
S14 = S14.set_index("date").replace({"ND": ""}).apply(pd.to_numeric)
dfa_tot = DFA_INC_LV.groupby("Date").sum(numeric_only=True)
DFA_VS_Z1 = [  # DFA category (sum over groups) vs households-only S14.b codes (annual = year-end)
    ("Real estate", ["LM155035015.A"]), ("Consumer durables", ["LM155111005.A"]),
    ("Corporate equities and mutual fund shares", ["LM193064105.A", "LM193064703.A", "LM193064505.A"]),
    ("Deposits", ["FL193020005.A", "FL193030205.A"]), ("Money market fund shares", ["FL193034005.A"]),
    ("Life insurance reserves", ["FL153040005.A"]), ("Miscellaneous other equity", ["LM153081115.A"]),
    ("Assets", ["FL192000005.A"]), ("Home mortgages", ["FL153165105.A"]), ("Consumer credit", ["FL153166000.A"]),
    ("Liabilities", ["FL194190005.A"]), ("Net worth", ["FL192090005.A"]),
]
for cat, codes in DFA_VS_Z1:
    rel = {}
    for y in range(1990, 2026):
        d = f"{y}:Q4"
        if d in dfa_tot.index and str(y) in S14.index:
            z = S14.loc[str(y), codes].sum()
            rel[y] = dfa_tot.loc[d, cat] / z - 1
    rel = pd.Series(rel)
    check(f"dfa vs Z.1 S14.b (households only): {cat}, Q4 sum over income groups / year-end level - 1, 2025",
          round(float(rel[2025]), 6), 0, 0.001, "ratio", source="z1_csv_files.zip csv/S14_b.csv",
          note=f"max |rel| 1990-2025 {rel.abs().max():.2e} (in {int(rel.abs().idxmax())}); codes {'+'.join(codes)}")
pens = dfa_tot.loc["2025:Q4", ["DB pension entitlements", "DC pension entitlements", "Annuities"]].sum()
check("dfa vs Z.1 S14.b: DB+DC+Annuities 2025:Q4 / pension entitlements FL153050005.A - 1",
      round(float(pens / S14.loc["2025", "FL153050005.A"] - 1), 6), None, 0, "ratio",
      note="DFA splits the households' pension entitlements; S14.b line is households and nonprofits")
s1m = z1_table(Z1_CUR[0], "S1M_b").set_index("date").replace({"ND": ""}).apply(pd.to_numeric)
lq = LATEST_Q
for cat, code in (("Real estate", "LM155035015.Q"), ("Home mortgages", "FL153165105.Q"),
                  ("Consumer credit", "FL153166000.Q")):
    check(f"dfa vs Z.1 S1M.b (quarterly): {cat} {lq}, sum over income groups / {code} - 1",
          round(float(dfa_tot.loc[lq, cat] / s1m.loc[lq, code] - 1), 6), 0, 0.001, "ratio")

# DFA income groups are SCF INCOME percentiles (DFA public code); compare the 2022:Q3 cutoffs with the SCF 2022 extract
w22 = SCF22["WGT"].to_numpy()
inc22 = (SCF22["INCOME"] / F22).to_numpy()                        # 2025 -> 2022 dollars (Fed factor)
o = np.argsort(inc22, kind="mergesort")
cw = np.cumsum(w22[o]) / w22.sum()
for grp, p in (("pct00to20", 0.20), ("pct20to40", 0.40), ("pct40to60", 0.60), ("pct60to80", 0.80),
               ("pct80to99", 0.99)):
    scf_p = float(inc22[o][np.searchsorted(cw, p)])
    dfa_max = float(DFA_INC_LV[(DFA_INC_LV.Date == "2022:Q3") & (DFA_INC_LV.Category == grp)]["Maximum Income Cutoff"].iloc[0])
    check(f"dfa 2022:Q3 maximum income cutoff of {grp} vs SCF 2022 INCOME P{int(p * 100)} (2022 dollars)",
          round(scf_p), round(dfa_max), 0.03 * dfa_max, "dollars",
          note="tolerance 3%: the DFA adds the Forbes 400 and uses its own adjusted weights (wgt_nwgac)")

# headline: 2022:Q3 (SCF quarter) -> latest, by income group (nominal $bn)
for cat in ("Corporate equities and mutual fund shares", "Real estate", "Net worth"):
    for g in DFA_GROUPS["income"]:
        a = DFA_INC_LV[(DFA_INC_LV.Date == "2022:Q3") & (DFA_INC_LV.Category == g)][cat].iloc[0] / 1e3
        b = DFA_INC_LV[(DFA_INC_LV.Date == lq) & (DFA_INC_LV.Category == g)][cat].iloc[0] / 1e3
        check(f"dfa change 2022:Q3 -> {lq}, {cat}, {g}", round(b - a, 1), None, 0, "$ billion (nominal)",
              note=f"{a:,.1f} -> {b:,.1f} ({100 * (b / a - 1):+.1f}%)")

# ---------------------------------------------------------------------------------------------------------
# 12. Checks file and summary
# ---------------------------------------------------------------------------------------------------------
chk = pd.DataFrame(CHECKS)
write_csv(chk, "fed_checks.csv")
n_fail = int((chk["pass"] == False).sum())                                        # noqa: E712
print(f"\nchecks: {len(chk)} rows | pass {int((chk['pass'] == True).sum())} | FAIL {n_fail} | info "  # noqa: E712
      f"{int(chk['pass'].isna().sum())}")
if FAILS:
    print("recorded download failures (see raw/fed/FETCH_FAILURES.csv):", ", ".join(sorted(FAILS)))
