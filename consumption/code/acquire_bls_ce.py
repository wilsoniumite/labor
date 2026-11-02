# acquire_bls_ce.py — vendor the BLS Consumer Expenditure Surveys (CE) income-decile/quintile tables, the
# 2025 release and its notices, the CE glossary/method pages, and BLS's prototype distributional PCE files;
# then build tidy long files from the raw files only.
#
# Run from the repo root:  venv/bin/python -I consumption/code/acquire_bls_ce.py
# Downloads skip files already vendored, so a rerun is offline and rebuilds every tidy file from raw.
# Plain functions and top-level code (notebook-cell friendly). No modelling here.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import fetch, http_get, manifest_row, RAW, TIDY

import re
import requests
from tqdm.auto import tqdm

SRC = "bls_ce"
RAWDIR = RAW / SRC
TIDY.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------------------------------------
# 1. Download list. (rel_file, url, what_it_is, used_for)
# ---------------------------------------------------------------------------------------------------------
BLS = "https://www.bls.gov"
CY = BLS + "/cex/tables/calendar-year"
DECILE_YEARS = list(range(2014, 2026))      # Table 1110 exists 2014 forward (tables.htm: "2014 forward")
QUINTILE_YEARS = list(range(2019, 2026))    # Table 1101 requested for 2019-2025 (exists 2012 forward)
AGG_YEARS = list(range(2019, 2026))         # aggregate-share tables, publisher-side check of group shares
TENURE_YEARS = [2024, 2025]                 # housing-tenure tables, used to test how renters enter addenda means
RELEASES = {  # data year -> archived annual news release (www.bls.gov/bls/news-release/home.htm#CESAN)
    2014: "09032015", 2015: "08302016", 2016: "08292017", 2017: "09112018", 2018: "09102019",
    2019: "09092020", 2020: "09092021", 2021: "09082022", 2022: "09082023", 2023: "09252024",
    2024: "12192025", 2025: "10292026"}

DOWNLOADS = []
for y in DECILE_YEARS:
    DOWNLOADS.append((f"tables/deciles/cu-income-deciles-before-taxes-{y}.xlsx",
                      f"{CY}/mean-item-share-average-standard-error/cu-income-deciles-before-taxes-{y}.xlsx",
                      f"CE Table 1110, deciles of income before taxes: annual expenditure means, shares, SEs and "
                      f"RSEs/CVs, calendar year {y}",
                      "ce_income_deciles_long.csv"))
for y in QUINTILE_YEARS:
    DOWNLOADS.append((f"tables/quintiles/cu-income-quintiles-before-taxes-{y}.xlsx",
                      f"{CY}/mean-item-share-average-standard-error/cu-income-quintiles-before-taxes-{y}.xlsx",
                      f"CE Table 1101, quintiles of income before taxes: annual expenditure means, shares, SEs and "
                      f"RSEs/CVs, calendar year {y}",
                      "ce_income_quintiles_long.csv"))
for y in AGG_YEARS:
    for g in ["deciles", "quintiles"]:
        DOWNLOADS.append((f"tables/aggshare/cu-income-{g}-before-taxes-{y}.xlsx",
                          f"{CY}/aggregate-group-share/cu-income-{g}-before-taxes-{y}.xlsx",
                          f"CE aggregate expenditure shares table, {g} of income before taxes, calendar year {y}",
                          "ce_income_aggshare_long.csv; cross-check of group shares of total expenditure"))
for y in TENURE_YEARS:
    DOWNLOADS.append((f"tables/tenure/cu-housing-tenure-{y}.xlsx",
                      f"{CY}/mean-item-share-average-standard-error/cu-housing-tenure-{y}.xlsx",
                      f"CE housing tenure table (means, shares, SEs, RSEs), calendar year {y}",
                      "ce_housing_tenure_long.csv; check that renters count as zeros in the owned-home addenda means"))
for y, d in RELEASES.items():
    DOWNLOADS.append((f"release/cesan_{d}.htm", f"{BLS}/news.release/archives/cesan_{d}.htm",
                      f"CE annual news release 'Consumer Expenditures--{y}' (archived HTML)",
                      "headline cross-checks (all-CU and quintile income/expenditure means)"))
DOWNLOADS.append(("release/cesan_10292026.pdf", f"{BLS}/news.release/archives/cesan_10292026.pdf",
                  "CE annual news release 'Consumer Expenditures--2025' (PDF, USDL-26-1619)",
                  "headline cross-checks; funding-lapse note"))
DOWNLOADS += [
    # listing pages: provenance for which years exist
    ("index/tables.htm", f"{BLS}/cex/tables.htm", "CE tables index page", "provenance of table coverage"),
    ("index/mean-item-share-average-standard-error.htm", f"{CY}/mean-item-share-average-standard-error.htm",
     "CE calendar-year means/shares/SE tables listing (all years, all demographic tables)",
     "provenance of table coverage (deciles 2014 forward, quintiles 2012 forward)"),
    ("index/aggregate-group-share.htm", f"{CY}/aggregate-group-share.htm",
     "CE calendar-year aggregate expenditure share tables listing", "provenance of table coverage"),
    # 2025 funding lapse and 2025 release notices
    ("notices/2025-federal-government-shutdown-impact-ce.htm", f"{BLS}/cex/2025-federal-government-shutdown-impact-ce.htm",
     "BLS Q&A: 2025 lapse in appropriations, impact on CE and the weight adjustment used for 2025",
     "2025 caveats (README)"),
    ("notices/2026_2025-shutdown-impacts.htm", f"{BLS}/cex/notices/2026/2025-shutdown-impacts.htm",
     "CE notice: questions and answers on the 2025 federal government shutdown impact on CE", "2025 caveats"),
    ("notices/2026_missing-ce-data-impact.htm", f"{BLS}/cex/notices/2026/missing-ce-data-impact.htm",
     "CE notice: BLS engaged expert panels regarding missing CE data", "2025 caveats"),
    ("notices/2026_annual-data-release-2025.htm", f"{BLS}/cex/notices/2026/annual-data-release-2025.htm",
     "CE notice: 2025 annual data release", "2025 caveats"),
    ("notices/2026_2026-2-year-tables.htm", f"{BLS}/cex/notices/2026/2026-2-year-tables.htm",
     "CE notice: changes with the 2025 annual release (two-year tables, Fay's BRR)", "2025 caveats"),
    ("notices/ce-pumd-2025-shutdown-impact.htm", f"{BLS}/cex/ce-pumd-2025-shutdown-impact.htm",
     "CE PUMD note: replicating 2025 estimates with the missing-data weight factors", "2025 caveats"),
    ("notices/handling-missing-2025-CE-data.htm", f"{BLS}/cpi/additional-resources/handling-missing-2025-CE-data.htm",
     "BLS article: handling of missing data to produce 2025 consumer spending estimates and price index weights",
     "2025 caveats"),
    ("notices/2025-federal-government-shutdown-impact-cpi.htm",
     f"{BLS}/cpi/additional-resources/2025-federal-government-shutdown-impact-cpi.htm",
     "BLS resource page: 2025 lapse in appropriations impact on CE and CPI", "2025 caveats"),
    ("notices/ce-standarderrors.htm", f"{BLS}/cex/ce-standarderrors.htm",
     "CE note: change of variance method to Fay's BRR with the 2025 release", "se/rse comparability (README)"),
    ("notices/2025_annual-data-release-2024.htm", f"{BLS}/cex/notices/2025/annual-data-release-2024.htm",
     "CE notice: 2024 annual data release", "2024 caveats"),
    ("notices/2025_ce-after-tax.htm", f"{BLS}/cex/notices/2025/ce-after-tax.htm",
     "CE notice: changes to after-tax income (no tax/after-tax estimates for 2024)", "income-row coverage (README)"),
    # definitions and conventions
    ("docs/csxgloss.htm", f"{BLS}/cex/csxgloss.htm", "CE glossary", "definitions (README)"),
    ("docs/csxfaqs.htm", f"{BLS}/cex/csxfaqs.htm", "CE questions and answers",
     "definitions: table means are averages over all CUs in the group"),
    ("docs/tables-getting-started-guide.htm", f"{BLS}/cex/tables-getting-started-guide.htm",
     "CE tables getting started guide", "table conventions: high-RSE suppression/flags, addenda"),
    ("docs/hom_cex_concepts.htm", f"{BLS}/opub/hom/cex/concepts.htm", "BLS Handbook of Methods, CE: concepts",
     "definitions (README)"),
    ("docs/hom_cex_calculation.htm", f"{BLS}/opub/hom/cex/calculation.htm",
     "BLS Handbook of Methods, CE: calculation", "definitions (README)"),
    ("docs/hom_cex_presentation.htm", f"{BLS}/opub/hom/cex/presentation.htm",
     "BLS Handbook of Methods, CE: presentation", "definitions (README)"),
    # BLS prototype distributional PCE
    ("dpce/pce-ce-distributions.htm", f"{BLS}/cex/pce-ce-distributions.htm",
     "BLS page: Distribution of Personal Consumption Expenditures (prototype); embeds two chart tables",
     "dpce documentation; bls_dpce_page_charts.csv"),
    ("dpce/distributional-pce-2000-2023.xlsx", f"{BLS}/cex/cecomparison/distributional-pce-2000-2023.xlsx",
     "BLS prototype distributional PCE results workbook, 2000-2023 (last updated 2025-03-14)",
     "bls_dpce_long.csv"),
    ("dpce/ce_pce_map.xlsx", f"{BLS}/cex/cecomparison/ce_pce_map.xlsx",
     "BLS map of CE UCCs to PCE product categories used for the distributional PCE", "ce_pce_map.csv"),
    ("dpce/distributional-pce-2000-2022.xlsx", f"{BLS}/cex/cecomparison/distributional-pce-2000-2022.xlsx",
     "BLS prototype distributional PCE results workbook, 2000-2022 vintage (linked from the price index note; "
     "its Table 3 holds the decile price indexes)", "bls_dpce_2000_2022_long.csv"),
    ("dpce/pce-ce-distribution-methods.htm", f"{BLS}/cex/pce-ce-distribution-methods.htm",
     "BLS methodology summary for the distributional PCE (methodology update and supplementary results)",
     "dpce documentation"),
    ("dpce/Methods_changes_page.htm", f"{BLS}/cex/Methods_changes_page.htm",
     "BLS summary of methods changes (December 2024 release) for the distributional PCE", "dpce documentation"),
    ("dpce/Inflation_note.htm", f"{BLS}/cex/Inflation_note.htm",
     "BLS note: distributional PCE price indexes, initial results (2024-12-09); embeds chart tables",
     "dpce documentation"),
    ("dpce/methodology-for-distributing-personal-saving.htm", f"{BLS}/cex/methodology-for-distributing-personal-saving.htm",
     "BLS technical document: joint distribution of DPI, PCE and personal saving (with BEA)", "dpce documentation"),
    ("dpce/ec240050.pdf", f"{BLS}/osmr/research-papers/2024/pdf/ec240050.pdf",
     "BLS Working Paper 575 (2024): joint distribution of income, consumption and saving", "dpce documentation"),
    ("dpce/ec220120.pdf", f"{BLS}/osmr/research-papers/2022/pdf/ec220120.pdf",
     "BLS Working Paper 557 (Garner, Martin, Matsumoto, Curtin 2022): distribution of PCE for 2019, prototype",
     "dpce documentation"),
    ("dpce/a-distributional-approach-to-us-personal-consumption-expenditures-overview.pdf",
     f"{BLS}/cex/a-distributional-approach-to-us-personal-consumption-expenditures-overview.pdf",
     "Garner, Martin, Matsumoto, Curtin (2024), 'A Distributional Approach to U.S. PCE: An Overview', "
     "Business Economics 59(3) (BLS-hosted PDF)", "dpce documentation"),
    ("dpce/curtin-2020-annual-COVID-impact.pdf", f"{BLS}/cex/research_papers/pdf/curtin-2020-annual-COVID-impact.pdf",
     "Curtin, 'The Impact of COVID-19 on CE Survey Estimates for 2020' (linked from the dPCE page)",
     "2020 caveats"),
]
# Named only in a hidden <span> on pce-ce-distributions.htm (not a visible link); tried at the same folder as
# the other results workbooks. A 404 here is recorded, not substituted.
OPTIONAL = [
    ("dpce/distributional-pce-interim-2017.xlsx", f"{BLS}/cex/cecomparison/distributional-pce-interim-2017.xlsx",
     "BLS distributional PCE interim 2017 file (named in a hidden element of pce-ce-distributions.htm)",
     "dpce documentation"),
]


def vendor_all():
    failed = []
    for rel, url, what, used in tqdm(DOWNLOADS + OPTIONAL, desc="bls_ce downloads"):
        if (RAWDIR / rel).exists():
            continue
        try:
            if (rel, url, what, used) in OPTIONAL:     # one try only: known 404 on 2026-11-02, keep reruns fast
                r = http_get(url, tries=1, timeout=60)
                (RAWDIR / rel).write_bytes(r.content)
                manifest_row(SRC, rel, url, what, used)
            else:
                fetch(SRC, rel, url, what, used)
        except (requests.HTTPError, RuntimeError, requests.RequestException) as e:
            code = getattr(getattr(e, "response", None), "status_code", None)
            failed.append((rel, url, f"HTTP {code}" if code else repr(e)))
    for rel, url, msg in failed:
        print(f"NOT VENDORED: {rel} <- {url}: {msg}")
    return failed


FAILED = vendor_all()


# ---------------------------------------------------------------------------------------------------------
# 2. Parsing helpers for the CE xlsx tables (raw files are only read, never changed)
# ---------------------------------------------------------------------------------------------------------
import gzip
import json
import math
import warnings
import openpyxl
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

warnings.filterwarnings("ignore", message="Workbook contains no default style")
warnings.filterwarnings("ignore", message="Data Validation extension is not supported")

STAT_MAP = {"Mean": "mean", "Share": "share", "SE": "se", "RSE": "rse", "CV(%)": "rse"}  # CV(%) = RSE, renamed 2022
LEGEND_RE = re.compile(r"^(?P<code>[a-z]|n\.a\.|#)\s+(?P<text>\S.*)$")   # footnote legend lines under a table
CODE_RE = re.compile(r"^(?:[a-z]/|n\.a\.)$")                            # a cell holding only a code
FMT_FLAG_RE = re.compile(r"\\([a-z])\\/")                                # 2024+: flag carried in the number format
MARK_RE = re.compile(r"(?:\s+[a-z]/|\s*#)+\s*$")                         # footnote marker at the end of a label
DECILE_HEAD = ["All consumer units"] + [f"{w} 10 percent" for w in
               ["Lowest", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh", "Eighth", "Ninth", "Highest"]]
QUINTILE_HEAD = ["All consumer units"] + [f"{w} 20 percent" for w in ["Lowest", "Second", "Third", "Fourth", "Highest"]]
DECILE_GROUPS = ["all"] + [f"d{k:02d}" for k in range(1, 11)]
QUINTILE_GROUPS = ["all"] + [f"q{k}" for k in range(1, 6)]
TENURE_GROUPS = ["all", "owner", "owner_mortgage", "owner_no_mortgage", "renter"]
LONG_COLS = ["year", "row", "item", "indent", "parent_item", "path", "group", "stat", "value", "flag",
             "flag_kind", "item_clean", "item_row", "depth", "is_leaf", "stat_label", "unit"]


def flag_kind(flag, legend):
    """Normalise a cell code through that file's own legend: the letters are reassigned between years and
    even between tables of one year (2025: high-RSE is b/ in Table 1110, d/ in Table 1101, c/ in Table 1710)."""
    if not flag:
        return ""
    if flag == "n.a.":
        return "not_applicable"
    text = legend.get(flag.rstrip("/"), "").lower()
    for key, kind in [("too small to display", "too_small"), ("suppressed", "suppressed_rse25"),
                      ("relative standard error", "high_rse25"), ("no data reported", "no_data"),
                      ("large sampling errors", "large_sampling_error")]:
        if key in text:
            return kind
    raise ValueError(f"cell code {flag!r} has no recognised legend entry: {legend}")


def norm(s):
    return " ".join(str(s).split()) if s is not None else ""


def load_ws(path):
    wb = openpyxl.load_workbook(path)          # full mode: indent and number_format are needed
    assert len(wb.sheetnames) == 1, (path, wb.sheetnames)
    return wb.active


def find_row(ws, text, start=1, stop=15):
    for r in range(start, stop + 1):
        if norm(ws.cell(r, 1).value) == text:
            return r
    raise ValueError(f"{text!r} not found in the first {stop} rows")


def colmap_from_header(ws, hdr_row, expected, groups):
    got = [norm(ws.cell(hdr_row, c).value) for c in range(2, 2 + len(expected))]
    if got != expected:
        raise ValueError(f"unexpected column header {got}")
    if any(ws.cell(hdr_row, c).value not in (None, "") for c in range(2 + len(expected), ws.max_column + 1)):
        raise ValueError("extra header columns")
    return {2 + k: g for k, g in enumerate(groups)}


def cell_value(cell, fmts):
    """(value, flag) for one cell, None if blank. Codes ('c/', 'n.a.') give NaN plus the code; from 2024 a
    high-RSE flag is part of the number format ('#.00# \\b\\/...'), so the number is kept and the code extracted."""
    v = cell.value
    if v is None or (isinstance(v, str) and not v.strip()):
        return None
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        fmts[cell.number_format] = fmts.get(cell.number_format, 0) + 1
        m = FMT_FLAG_RE.search(cell.number_format or "")
        return float(v), (m.group(1) + "/" if m else "")
    s = str(v).strip()
    if CODE_RE.match(s):
        return math.nan, s
    raise ValueError(f"unparseable cell {cell.coordinate}: {v!r}")


def split_footer(ws, cols):
    """Last row holding a value in the group columns, plus the footnote legend and other text below it."""
    last = ws.max_row
    while last > 0 and all(ws.cell(last, c).value in (None, "") for c in cols):
        last -= 1
    legend, notes = {}, []
    for r in range(last + 1, ws.max_row + 1):
        s = norm(ws.cell(r, 1).value)
        if not s:
            continue
        m = LEGEND_RE.match(s)
        if m and m.group("code") not in legend:
            legend[m.group("code")] = m.group("text")
        else:
            notes.append(s)
    return last, legend, notes


def parse_ce_table(ws, colmap, first_row):
    """Long rows for one CE table. Hierarchy from the label cells' indent (openpyxl alignment.indent): the parent
    of a label is the nearest label above it with a smaller indent. Stat rows (Mean/Share/SE/RSE/CV(%)) belong
    to the label above them; a label row that carries numbers itself gets stat 'value'."""
    last, legend, notes = split_footer(ws, list(colmap))
    items, cells, fmts = [], [], {}
    stack, cur = [], None
    for r in range(first_row, last + 1):
        a = ws.cell(r, 1)
        label = a.value.strip() if isinstance(a.value, str) else norm(a.value)
        vals = {g: cell_value(ws.cell(r, c), fmts) for c, g in colmap.items()}
        has = any(v is not None for v in vals.values())
        if not label:
            if has:
                raise ValueError(f"row {r}: values without a label")
            continue
        if label in STAT_MAP:
            if cur is None:
                raise ValueError(f"row {r}: stat row before any item")
            for g, v in vals.items():
                if v is not None:
                    cells.append((cur, r - 1, g, STAT_MAP[label], label, v[0], v[1]))
            continue
        ind = float(a.alignment.indent or 0)
        while stack and stack[-1][0] >= ind:
            stack.pop()
        parent = stack[-1][1] if stack else None
        clean = norm(MARK_RE.sub("", label))
        path = (items[parent]["path"] + " > " if parent is not None else "") + clean
        items.append(dict(item_row=r - 1, item=label, item_clean=clean, indent=ind, depth=len(stack),
                          parent=parent, path=path))
        cur = len(items) - 1
        stack.append((ind, cur))
        for g, v in vals.items():
            if v is not None:
                cells.append((cur, r - 1, g, "value", "", v[0], v[1]))
    has_child = {it["parent"] for it in items if it["parent"] is not None}
    rows = []
    for i, row, g, stat, stat_label, value, flag in cells:
        it = items[i]
        rows.append(dict(row=row, item=it["item"], indent=it["indent"],
                         parent_item=items[it["parent"]]["item_clean"] if it["parent"] is not None else "",
                         path=it["path"], group=g, stat=stat, value=value, flag=flag, item_clean=it["item_clean"],
                         item_row=it["item_row"], depth=it["depth"], is_leaf=i not in has_child,
                         stat_label=stat_label))
    return pd.DataFrame(rows), legend, notes, fmts


def unit_mean_table(path, stat, item_clean):
    top = path.split(" > ")[0]
    if top.startswith("Number of consumer units"):
        return "thousands of consumer units"
    if top == "Lower limit":
        return "dollars of income before taxes (lowest value in the group)"
    if stat == "rse":
        return "percent (100 x SE / mean)"
    if top == "Percent distribution:":
        return "percent of consumer units in the group"
    if top == "Consumer unit characteristics:":
        if item_clean == "Age of reference person":
            return "years (mean)"
        if path.startswith("Consumer unit characteristics: > Average number in consumer unit:"):
            return "number per consumer unit (mean)"
        return "dollars per consumer unit per year"
    if top == "Average annual expenditures":
        return "percent of the group's average annual expenditures" if stat == "share" else \
            "dollars per consumer unit per year"
    if top.startswith("Sources of"):
        return "percent of the group's income before taxes" if stat == "share" else \
            "dollars per consumer unit per year"
    if top == "Addenda:":
        if item_clean == "Estimated monthly rental value of owned home":
            return "dollars per consumer unit per month (non-owners count as zero)"
        if item_clean == "Estimated market value of owned home":
            return "dollars per consumer unit, stock value (non-owners count as zero)"
        return "dollars per consumer unit per year"
    raise ValueError(f"no unit rule for {path!r} / {stat}")


FOOTNOTES = []   # dataset, year, code, meaning   (codes change meaning by year and by table)
FORMATS = []     # dataset, year, number_format, n_cells


def record_meta(dataset, year, ws, legend, notes, fmts):
    FOOTNOTES.append(dict(dataset=dataset, year=year, code="title", meaning=norm(ws.cell(1, 1).value)))
    for k, v in legend.items():
        FOOTNOTES.append(dict(dataset=dataset, year=year, code=k if k in ("n.a.", "#") else k + "/", meaning=v))
    for s in notes:
        FOOTNOTES.append(dict(dataset=dataset, year=year, code="source" if s.startswith("Source:") else "note",
                              meaning=s))
    for f, n in sorted(fmts.items()):
        FORMATS.append(dict(dataset=dataset, year=year, number_format=f, n_cells=n))


def build_mean_tables(kind, years):
    head, groups, tno = ((DECILE_HEAD, DECILE_GROUPS, "Table 1110.") if kind == "deciles"
                         else (QUINTILE_HEAD, QUINTILE_GROUPS, "Table 1101."))
    frames = []
    for y in tqdm(years, desc=f"parse CE {kind}"):
        ws = load_ws(RAWDIR / f"tables/{kind}/cu-income-{kind}-before-taxes-{y}.xlsx")
        title = norm(ws.cell(1, 1).value)
        if not (title.startswith(tno) and title.endswith(str(y))):
            raise ValueError(f"unexpected title {title!r}")
        hdr = find_row(ws, "Item")
        df, legend, notes, fmts = parse_ce_table(ws, colmap_from_header(ws, hdr, head, groups), hdr + 1)
        record_meta(f"means_{kind}", y, ws, legend, notes, fmts)
        df["flag_kind"] = [flag_kind(f, legend) for f in df.flag]
        df.insert(0, "year", y)
        frames.append(df)
    out = pd.concat(frames, ignore_index=True)
    out["unit"] = [unit_mean_table(p, s, i) for p, s, i in zip(out.path, out.stat, out.item_clean)]
    dup = out.duplicated(["year", "path", "group", "stat"])
    if dup.any():
        raise ValueError(f"duplicate cells: {out[dup].head()}")
    return out[LONG_COLS]


def build_tenure(years):
    frames = []
    for y in years:
        ws = load_ws(RAWDIR / f"tables/tenure/cu-housing-tenure-{y}.xlsx")
        title = norm(ws.cell(1, 1).value)
        assert title.startswith("Table 1710. Housing tenure") and title.endswith(str(y)), title
        hdr = find_row(ws, "Item")
        top = [norm(ws.cell(hdr, c).value) for c in range(2, 7)]
        sub = [norm(ws.cell(hdr + 1, c).value) for c in range(2, 7)]
        if top != ["All consumer units", "Homeowner", "", "", "Renter"] or \
                sub != ["", "Total", "Homeowner with mortgage", "Homeowner without mortgage", ""]:
            raise ValueError(f"unexpected tenure header {top} / {sub}")
        df, legend, notes, fmts = parse_ce_table(ws, dict(zip(range(2, 7), TENURE_GROUPS)), hdr + 2)
        record_meta("means_tenure", y, ws, legend, notes, fmts)
        df["flag_kind"] = [flag_kind(f, legend) for f in df.flag]
        df.insert(0, "year", y)
        frames.append(df)
    out = pd.concat(frames, ignore_index=True)
    out["unit"] = [unit_mean_table(p, s, i) for p, s, i in zip(out.path, out.stat, out.item_clean)]
    assert not out.duplicated(["year", "path", "group", "stat"]).any()
    return out[LONG_COLS]


def aggshare_stat_unit(path, group):
    top = path.split(" > ")[0]
    if top.startswith("Number of consumer units"):
        return "value", "thousands of consumer units"
    if top == "Percent distribution of consumer units":
        return "value", "percent of all consumer units"
    if top.startswith("Consumer unit characteristics"):
        if path.endswith("Age of reference person"):
            return "value", "years (mean)"
        if "Average number in consumer unit:" in path:
            return "value", "number per consumer unit (mean)"
        return "value", "dollars per consumer unit per year (mean)"
    if top == "Percent distribution:":
        return "value", "percent of consumer units in the group"
    if top == "Annual aggregate expenditures" or top.startswith("Sources of"):
        if group == "all":
            return "aggregate", "millions of dollars per year (all consumer units)"
        return "agg_share", "percent of the all-consumer-unit aggregate for the item"
    raise ValueError(f"no aggshare rule for {path!r}")


def build_aggshare(years):
    frames = []
    for kind in ["deciles", "quintiles"]:
        head, groups = (DECILE_HEAD, DECILE_GROUPS) if kind == "deciles" else (QUINTILE_HEAD, QUINTILE_GROUPS)
        head = ["Aggregate"] + head[1:]
        for y in years:
            ws = load_ws(RAWDIR / f"tables/aggshare/cu-income-{kind}-before-taxes-{y}.xlsx")
            title = norm(ws.cell(1, 1).value)
            assert "Shares of annual aggregate expenditures" in title and title.endswith(str(y)), title
            hdr = find_row(ws, "Item")
            df, legend, notes, fmts = parse_ce_table(ws, colmap_from_header(ws, hdr, head, groups), hdr + 1)
            record_meta(f"aggshare_{kind}", y, ws, legend, notes, fmts)
            if (df.stat != "value").any():
                raise ValueError("aggregate-share tables should have no stat rows")
            su = [aggshare_stat_unit(p, g) for p, g in zip(df.path, df.group)]
            df["stat"] = [s for s, _ in su]
            df["unit"] = [u for _, u in su]
            df["flag_kind"] = [flag_kind(f, legend) for f in df.flag]
            df.insert(0, "year", y)
            df.insert(1, "grouping", kind)
            frames.append(df)
    out = pd.concat(frames, ignore_index=True)
    assert not out.duplicated(["grouping", "year", "path", "group", "stat"]).any()
    return out[["year", "grouping"] + [c for c in LONG_COLS if c not in ("year", "stat_label")]]


# ---------------------------------------------------------------------------------------------------------
# 3. Distributional PCE workbooks, CE-to-PCE map, and the tables embedded in the dPCE web pages
# ---------------------------------------------------------------------------------------------------------
DPCE_COLS = ["vintage", "table", "year", "line", "nipa_2_3_5_line", "pce_mp", "category", "category_indent",
             "grouping", "group", "measure", "value", "unit"]
GROUPING_T1 = "deciles of equivalized total PCE (CU total spending / sqrt(CU size)), CU-weighted (finlwt21)"
PCT_GROUPS = {"0-10%": "d01", "10-20%": "d02", "20-30%": "d03", "30-40%": "d04", "40-50%": "d05",
              "50-60%": "d06", "60-70%": "d07", "70-80%": "d08", "80-90%": "d09", "90-100%": "d10",
              "0-20%": "q1", "20-40%": "q2", "40-60%": "q3", "60-80%": "q4", "80-100%": "q5",
              "80-99%": "p80_99", "Top 1%": "top1", "Top 5%": "top5"}


def t2_measure(stat):
    """Table 2 statistic label -> (concept, group, measure, unit)."""
    concept, _, rest = stat.partition(":") if ":" in stat else (None, None, None)
    if concept is None:   # e.g. 'Equivalized total mean (nominal)', 'Total median ($2017)'
        m = re.match(r"^(Equivalized total|Total) (mean|median) \((nominal|\$2017)\)$", stat)
        if not m:
            raise ValueError(f"unknown Table 2 statistic {stat!r}")
        concept, kind, base = m.groups()
        unit = "dollars per CU per year, nominal" if base == "nominal" else "dollars per CU per year, 2017 dollars (PCE price index)"
        return concept, "all", f"{kind}_{'nominal' if base == 'nominal' else 'real2017'}", unit
    rest = rest.strip()
    m = re.match(r"^(.*) share$", rest)
    if m:
        return concept, PCT_GROUPS[m.group(1)], "share_of_total", "fraction of total (unequivalized) PCE" \
            if concept == "Total" else "fraction of total equivalized PCE"
    named = {"90/10": ("ratio_p90_p10", "ratio"), "Gini index": ("gini", "index 0-1"), "Theil index": ("theil", "index"),
             "Log-Deviance": ("mean_log_deviation", "index"), "CV": ("coef_of_variation", "ratio")}
    if rest in named:
        return concept, "all", named[rest][0], named[rest][1]
    raise ValueError(f"unknown Table 2 statistic {stat!r}")


def parse_dpce_workbook(rel, vintage):
    wb = openpyxl.load_workbook(RAWDIR / rel, data_only=True)
    expect = ["Description of Tables", "Table 1", "table1data", "years", "Table 2", "Table 3"]
    if wb.sheetnames != expect:
        raise ValueError(f"{rel}: sheets {wb.sheetnames}")
    rows = []
    # Table 1 data sheet: one row per year x line, Total ($ billions) and ten decile shares
    ws = wb["table1data"]
    head = [norm(ws.cell(1, c).value) for c in range(1, ws.max_column + 1)]
    if head != ["year", "lineno", "pce_mp", "pce_title", "Total"] + [f"Decile{k}" for k in range(1, 11)]:
        raise ValueError(f"{rel}: table1data header {head}")
    for r in range(2, ws.max_row + 1):
        v = [ws.cell(r, c).value for c in range(1, 16)]
        if v[0] is None:
            continue
        year, line, mp, title = int(v[0]), int(v[1]), v[2], str(v[3])
        cat = norm(title)
        common = dict(vintage=vintage, table="T1", year=year, line=line, nipa_2_3_5_line=line if line <= 22 else 30,
                      pce_mp=mp, category=cat, category_indent=len(title) - len(title.lstrip(" ")),
                      grouping=GROUPING_T1)
        rows.append(dict(common, group="total", measure="pce", value=float(v[4]), unit="billions of current dollars"))
        for k in range(10):
            rows.append(dict(common, group=f"d{k + 1:02d}", measure="decile_share_of_category", value=float(v[5 + k]),
                             unit="fraction of the category's total (the ten deciles sum to 1)"))
    # Tables 2 and 3: statistic rows x year columns
    for tname in ["Table 2", "Table 3"]:
        ws = wb[tname]
        hdr = 3
        assert norm(ws.cell(hdr, 1).value) == "Line"
        years = {}
        for c in range(3, ws.max_column + 1):
            h = norm(ws.cell(hdr, c).value)
            if h:
                years[c] = int(h)
        series = None
        for r in range(hdr + 1, ws.max_row + 1):
            line = ws.cell(r, 1).value
            if not isinstance(line, (int, float)):
                continue
            stat = norm(ws.cell(r, 2).value)
            if tname == "Table 2":
                concept, group, measure, unit = t2_measure(stat)
                grouping = ("quintiles/top groups of equivalized total PCE, CU-weighted; Total = unequivalized PCE "
                            "of CUs ranked by equivalized PCE") if group != "all" else "all consumer units"
                category = f"{concept} PCE"
            else:
                if stat in ("Personal consumption expenditures", "Market-based personal consumption expenditures"):
                    series, group = stat, "all"
                else:
                    group = PCT_GROUPS[stat]
                category, measure, unit = f"{series} price index", "price_index", "index, 2017 = 100"
                grouping = "deciles of equivalized total PCE (market and non-market), CU-weighted" if group != "all" \
                    else "official (published) index"
            for c, y in years.items():
                val = ws.cell(r, c).value
                if val is None:
                    continue
                rows.append(dict(vintage=vintage, table="T2" if tname == "Table 2" else "T3", year=y, line=int(line),
                                 nipa_2_3_5_line=None, pce_mp=None, category=category, category_indent=None,
                                 grouping=grouping, group=group, measure=measure, value=float(val), unit=unit))
    out = pd.DataFrame(rows)[DPCE_COLS]
    for c in ["nipa_2_3_5_line", "pce_mp", "category_indent"]:
        out[c] = out[c].astype("Int64")
    # the 'Table 1' sheet is a year-selector view of table1data: its cached values must match the data sheet
    ws = wb["Table 1"]
    sel = int(ws.cell(4, 2).value)
    view = {}
    for r in range(6, 29):
        if isinstance(ws.cell(r, 1).value, (int, float)):
            view[int(ws.cell(r, 1).value)] = [ws.cell(r, c).value for c in range(3, 14)]
    t1 = out[(out.table == "T1") & (out.year == sel)]
    worst = 0.0
    for line, vals in view.items():
        sub = t1[t1.line == line].set_index("group").value
        ref = [sub["total"]] + [sub[f"d{k:02d}"] for k in range(1, 11)]
        worst = max(worst, max(abs(float(a) - float(b)) for a, b in zip(vals, ref)))
    desc = [norm(wb["Description of Tables"].cell(r, 1).value) for r in range(1, 23)]
    return out, dict(selected_year=sel, view_vs_data_maxdiff=worst, description=[d for d in desc if d])


def build_ce_pce_map():
    ws = load_ws(RAWDIR / "dpce/ce_pce_map.xlsx")
    head = [norm(ws.cell(1, c).value) for c in range(1, 9)]
    if head != ["UCC_Title", "UCC_Split", "CE_Source", "firstyq", "lastyq", "PCE_Title", "PCE_Series", "Notes"]:
        raise ValueError(f"ce_pce_map header {head}")
    rows = []
    for r in range(2, ws.max_row + 1):
        v = [ws.cell(r, c).value for c in range(1, 9)]
        if norm(v[0]) == "End of sheet" and all(x in (None, "") for x in v[1:]):
            continue
        v = ["" if x is None else str(x).strip() for x in v]
        ucc, _, split = v[1].partition("_")
        rows.append(dict(row=r - 1, ucc_title=v[0], ucc_split=v[1], ucc=ucc, split=split, ce_source=v[2],
                         ce_source_base=v[2].rstrip("*"), source_note_flag=v[2].endswith("*"),
                         firstyq=v[3], lastyq=v[4], pce_title=v[5], pce_series=v[6], notes=v[7]))
    return pd.DataFrame(rows)


def num_or_nan(s):
    t = s.replace(",", "").replace("$", "").replace("%", "").replace("–", "-").strip()
    try:
        return float(t)
    except ValueError:
        return math.nan


def page_tables(rel):
    """Every table on a vendored BLS page: Highcharts tables embedded as JSON strings ('input_table') and plain
    HTML <table>s. Long form: one row per data cell, values as printed plus a numeric parse."""
    html = (RAWDIR / rel).read_text(encoding="utf-8", errors="replace")
    found = [("chart_table", json.loads('"' + s + '"')) for s in re.findall(r'"input_table":"((?:[^"\\]|\\.)*)"', html)]
    found += [("html_table", str(t)) for t in BeautifulSoup(html, "lxml").find_all("table")]
    rows = []
    for k, (kind, frag) in enumerate(found):
        t = BeautifulSoup(frag, "lxml")
        cap = t.find("caption")
        title = cap.get_text(" ", strip=True) if cap else ""
        trs = t.find_all("tr")
        header = [c.get_text(" ", strip=True) for c in trs[0].find_all(["th", "td"])]
        section = ""
        for i, tr in enumerate(trs[1:], start=1):
            cells = [c.get_text(" ", strip=True) for c in tr.find_all(["th", "td"])]
            if not any(cells):
                continue
            if len(cells) == 1:             # section heading inside a table, or a source/footer line
                section = cells[0]
                continue
            for j, raw in enumerate(cells[1:], start=1):
                rows.append(dict(page=rel, table_no=k, kind=kind, title=title, section=section, row=i,
                                 row_label=cells[0], col_label=header[j] if j < len(header) else "",
                                 value_raw=raw, value=num_or_nan(raw), is_percent=raw.endswith("%")))
    return rows


# ---------------------------------------------------------------------------------------------------------
# 4. Headline numbers printed in the annual news releases (for cross-checks against the tables)
# ---------------------------------------------------------------------------------------------------------
REL_LINE = re.compile(r"^\s*(?P<label>Average annual expenditures|Average income before taxes|"
                      r"Number of consumer units(?:\s*\([^)]*\))*)\s+(?P<rest>[$\d].*)$", re.I)
LEVEL_TOK = re.compile(r"^\$?(?P<num>\d{1,3}(?:,\d{3})+|\d+)(?P<note>\([a-z]\))?(?P<star>\*{0,2})$")
YEAR_HDR = re.compile(r"^\s*Item\s+(?P<years>(?:(?:19|20)\d\d\s+){2,})")   # 'Item  2019  2020  2021  2019-20 ...'


def release_headlines(data_year, stamp):
    """Level values on the 'Average annual expenditures' / 'Average income before taxes' / 'Number of consumer
    units' lines of a release's <pre> tables. Year columns come from the table's own 'Item 2019 2020 ...' header;
    a line with six levels is the income-quintile table (all CUs, then quintiles 1-5) for the data year."""
    soup = BeautifulSoup((RAWDIR / f"release/cesan_{stamp}.htm").read_bytes(), "lxml")
    text = "\n".join(p.get_text() for p in soup.find_all("pre"))
    rows, years = [], None
    for line in text.splitlines():
        h = YEAR_HDR.match(line)
        if h:
            years = [int(x) for x in h.group("years").split()]
            continue
        m = REL_LINE.match(line)
        if not m:
            continue
        toks = [LEVEL_TOK.match(t) for t in m.group("rest").split()]
        levels = [(float(t.group("num").replace(",", "")), (t.group("note") or "") + t.group("star"))
                  for t in toks if t]
        label = norm(m.group("label")).lower()
        item = ("average_annual_expenditures" if label.startswith("average annual") else
                "income_before_taxes" if label.startswith("average income") else "consumer_units_thousands")
        if len(levels) == 6:            # quintile table: all CUs then the five quintiles, for the data year
            for g, (v, note) in zip(QUINTILE_GROUPS, levels):
                rows.append(dict(release=f"cesan_{stamp}", data_year=data_year, kind="quintile_table", item=item,
                                 label=norm(m.group("label")), ref_year=data_year, group=g, value=v, note=note))
        elif levels:                    # headline time series under the last year header
            if years is None or len(years) != len(levels) or years[-1] != data_year:
                raise ValueError(f"cesan_{stamp}: {len(levels)} levels under year header {years}: {line!r}")
            for yr, (v, note) in zip(years, levels):
                rows.append(dict(release=f"cesan_{stamp}", data_year=data_year, kind="time_series", item=item,
                                 label=norm(m.group("label")), ref_year=yr, group="all", value=v, note=note))
    return rows


# ---------------------------------------------------------------------------------------------------------
# 5. Writer: plain CSV, gzip (deterministic header) above ~20 MB
# ---------------------------------------------------------------------------------------------------------
def write_tidy(df, name):
    data = df.to_csv(index=False, float_format="%.10g", lineterminator="\n").encode("utf-8")
    plain, gz = TIDY / name, TIDY / (name + ".gz")
    if len(data) > 20_000_000:
        with open(gz, "wb") as fh, gzip.GzipFile(filename=name, mode="wb", fileobj=fh, mtime=0) as z:
            z.write(data)
        plain.unlink(missing_ok=True)
        out = gz
    else:
        plain.write_bytes(data)
        gz.unlink(missing_ok=True)
        out = plain
    print(f"wrote {out.relative_to(TIDY.parents[2])}: {len(df):,} rows, {out.stat().st_size / 1e6:.2f} MB")
    return out


# ---------------------------------------------------------------------------------------------------------
# 6. Build the tidy files
# ---------------------------------------------------------------------------------------------------------
dec = build_mean_tables("deciles", DECILE_YEARS)
qui = build_mean_tables("quintiles", QUINTILE_YEARS)
ten = build_tenure(TENURE_YEARS)
agg = build_aggshare(AGG_YEARS)
dpce, dpce_meta = parse_dpce_workbook("dpce/distributional-pce-2000-2023.xlsx", "2025-03")
dpce22, dpce22_meta = parse_dpce_workbook("dpce/distributional-pce-2000-2022.xlsx", "2024-11")
cemap = build_ce_pce_map()
ptab = pd.DataFrame(sum([page_tables(p) for p in ["dpce/pce-ce-distributions.htm", "dpce/pce-ce-distribution-methods.htm",
                                                  "dpce/Methods_changes_page.htm", "dpce/Inflation_note.htm"]], []))
rel = pd.DataFrame(sum([release_headlines(y, d) for y, d in RELEASES.items()], []))
foot = pd.DataFrame(FOOTNOTES)
fmts = pd.DataFrame(FORMATS)

write_tidy(dec, "ce_income_deciles_long.csv")
write_tidy(qui, "ce_income_quintiles_long.csv")
write_tidy(ten, "ce_housing_tenure_long.csv")
write_tidy(agg, "ce_income_aggshare_long.csv")
write_tidy(foot, "ce_table_footnotes.csv")
write_tidy(rel, "ce_release_headlines.csv")
write_tidy(dpce, "bls_dpce_long.csv")
write_tidy(dpce22, "bls_dpce_2000_2022_long.csv")
write_tidy(cemap, "ce_pce_map.csv")
write_tidy(ptab, "bls_dpce_page_tables.csv")


# ---------------------------------------------------------------------------------------------------------
# 7. Verification. Every number lands in bls_ce_checks.csv:
#    check, dataset, year, group, item, reference, observed, diff, rel_diff, bound, status, note
# ---------------------------------------------------------------------------------------------------------
CHECKS = []


def chk(check, dataset, year, group, item, reference, observed, bound=None, status=None, note=""):
    """Status: 'ok' = |diff| within the rounding bound; 'small_gap' = beyond it but |rel_diff| < 0.5%;
    'gap' = 0.5% or more; other statuses are set by the caller (flagged, partial_parent, revision, info)."""
    diff = observed - reference if (reference is not None and observed is not None) else None
    rel = diff / reference if (diff is not None and reference not in (0, None) and not math.isnan(reference)) else None
    if status is None:
        if diff is not None and bound is not None and abs(diff) <= bound + 1e-9:
            status = "ok"
        elif rel is not None and abs(rel) < 0.005:
            status = "small_gap"
        else:
            status = "gap"
    CHECKS.append(dict(check=check, dataset=dataset, year=year, group=group, item=item, reference=reference,
                       observed=observed, diff=diff, rel_diff=rel, bound=bound, status=status, note=note))


# Parents whose printed children do not exhaust them (BLS prints only some components): children sum below parent
PARTIAL_PARENTS = {
    "Average annual expenditures > Transportation > Gasoline and other fuels": 2023,      # only 'Gasoline' shown
    "Average annual expenditures > Transportation > Vehicle purchases (net outlay)": 2024,  # 'Other vehicles' dropped
}


def legend_lookup(dataset, year):
    f = foot[(foot.dataset == dataset) & (foot.year == year)]
    return dict(zip(f.code, f.meaning))


def hierarchy_checks(df, dataset):
    """Children vs parent for every item with children: 'sum' (dollar means, or Homeowner = with + without
    mortgage), 'difference' (net change in assets and liabilities = assets - liabilities), 'sum_to_100'
    (percent-distribution blocks). Bound = 0.5 per rounded number involved. A child coded 'value too small to
    display' counts as 0; a child suppressed or not reported makes the comparison 'flagged_children'."""
    for y, d in df.groupby("year"):
        leg = legend_lookup(dataset, y)
        v = d[d.stat.isin(["mean", "value"])]
        val = {(p, g): (x, f) for p, g, x, f in zip(v.path, v.group, v.value, v.flag)}
        items = d.drop_duplicates("path")[["path", "item_clean", "depth"]]
        kids = {}
        for p in items.path:
            if " > " in p:
                kids.setdefault(p.rsplit(" > ", 1)[0], []).append(p)
        groups = list(dict.fromkeys(d.group))
        for parent, ch in kids.items():
            pclean = parent.rsplit(" > ", 1)[-1]
            has_val = any((parent, g) in val for g in groups)
            if pclean == "Net change in total assets and liabilities":
                rel = "difference"
            elif has_val:
                rel = "sum"
            elif parent.startswith("Percent distribution: > "):
                rel = "sum_to_100"
            else:
                continue                      # headers such as 'Average number in consumer unit:'
            for g in groups:
                if rel == "sum_to_100":
                    ref = 100.0
                else:
                    if (parent, g) not in val:
                        continue
                    ref, pflag = val[(parent, g)]
                    if math.isnan(ref):
                        chk("hierarchy_" + rel, dataset, y, g, parent, None, None, status="flagged_parent",
                            note=f"parent coded {pflag}")
                        continue
                xs, notes, flagged = [], [], False
                for c in ch:
                    x, f = val.get((c, g), (math.nan, "missing"))
                    if math.isnan(x):
                        meaning = leg.get(f, "")
                        if "too small to display" in meaning.lower():
                            x = 0.0
                            notes.append(f"{c.rsplit(' > ', 1)[-1]}={f}(too small, as 0)")
                        else:
                            flagged = True
                            notes.append(f"{c.rsplit(' > ', 1)[-1]}={f}")
                            continue
                    xs.append(x)
                if rel == "difference":
                    if len(ch) != 2 or len(xs) != 2:
                        chk("hierarchy_difference", dataset, y, g, parent, ref, None, status="flagged_children",
                            note="; ".join(notes))
                        continue
                    obs = xs[0] - xs[1]
                else:
                    obs = sum(xs)
                bound = 0.5 * (len(ch) + (0 if rel == "sum_to_100" else 1))
                status = "flagged_children" if flagged else None
                if status is None and y >= PARTIAL_PARENTS.get(parent, 9999) and obs < ref - bound:
                    status = "partial_parent"
                    notes.append("BLS prints only part of this parent's components")
                chk("hierarchy_" + rel, dataset, y, g, parent, ref, obs, bound=bound, status=status,
                    note=f"{len(ch)} children" + ("; " + "; ".join(notes) if notes else ""))


def share_checks(df, dataset):
    """Share rows: expenditure shares vs 100*mean/average annual expenditures; income shares vs
    100*mean/income before taxes (same group). Bound 0.05 (one decimal) plus mean rounding."""
    for y, d in df.groupby("year"):
        m = d[d.stat == "mean"].set_index(["path", "group"]).value
        s = d[d.stat == "share"]
        ibt = [p for p in d.path.unique() if p.startswith("Sources of") and p.count(" > ") == 1 and "before taxes" in p]
        for p, g, sh in zip(s.path, s.group, s.value):
            if math.isnan(sh) or (p, g) not in m.index or math.isnan(m[(p, g)]):
                continue
            base = ("Average annual expenditures", g) if p.startswith("Average annual expenditures") else (ibt[0], g)
            calc = 100 * m[(p, g)] / m[base]
            tot = abs(m[base])     # share printed to 0.1; item mean and base mean each rounded to $1
            chk("share_vs_mean", dataset, y, g, p, calc, sh, bound=0.05 + 50 / tot + 50 * abs(m[(p, g)]) / tot ** 2)


def rse_checks(df, dataset):
    """RSE (printed as CV(%) before 2022) vs 100*SE/mean, using the exact interval implied by the printed
    rounding: mean to the unit shown (dollars, or 0.1 for counts/ages), SE and RSE to 0.01."""
    for y, d in df.groupby("year"):
        piv = d[d.stat.isin(["mean", "se", "rse"])].pivot_table(index=["path", "group"], columns="stat",
                                                                values="value", aggfunc="first").dropna()
        piv = piv[piv["mean"].abs() >= 1]
        m, se, rse = piv["mean"].abs(), piv["se"].abs(), piv["rse"].abs()
        lo = 100 * (se - 0.005) / (m + 0.5) - 0.005
        hi = 100 * (se + 0.005) / (m - 0.5) + 0.005
        sign_ok = (np.sign(piv["rse"]) == np.sign(piv["mean"])) | (piv["rse"] == 0)
        bad = (rse < lo - 1e-9) | (rse > hi + 1e-9) | ~sign_ok
        dev = (piv["rse"] - 100 * piv["se"] / piv["mean"]).abs()
        label = d[d.stat == "rse"].stat_label.iloc[0]
        chk("rse_vs_se_over_mean", dataset, y, "all groups", f"{len(piv)} cells (|mean|>=1), printed as {label}",
            0.0, float(dev.max()), status="ok" if not bad.any() else "gap",
            note=f"{int(bad.sum())} cells outside the rounding interval; median |dev| {dev.median():.4f}; "
                 f"largest |dev| at mean {piv['mean'][dev.idxmax()]:.0f}")


def pair_checks(dec, qui):
    """Deciles paired into quintiles (CU-weighted with the decile CU counts) vs the quintile table."""
    for y in sorted(set(dec.year) & set(qui.year)):
        d, q = dec[dec.year == y], qui[qui.year == y]
        n = d[d.path == "Number of consumer units (in thousands)"].set_index("group").value
        nq = q[q.path == "Number of consumer units (in thousands)"].set_index("group").value
        lo = d[d.path == "Lower limit"].set_index("group").value
        loq = q[q.path == "Lower limit"].set_index("group").value
        dv = d[d.stat.isin(["mean", "value"])].set_index(["path", "group"])
        qv = q[q.stat.isin(["mean", "value"])].set_index(["path", "group"])
        for k in range(1, 6):
            a, b = f"d{2 * k - 1:02d}", f"d{2 * k:02d}"
            chk("decile_pair_cu_count", "deciles_vs_quintiles", y, f"q{k}", "Number of consumer units (in thousands)",
                nq[f"q{k}"], n[a] + n[b], bound=1.0)
            if k > 1:
                chk("decile_pair_lower_limit", "deciles_vs_quintiles", y, f"q{k}", "Lower limit", loq[f"q{k}"], lo[a],
                    bound=0.5)
            for p in dv.index.get_level_values(0).unique():
                if p in ("Number of consumer units (in thousands)", "Lower limit") or (p, f"q{k}") not in qv.index:
                    continue
                x1, x2, xq = dv.loc[(p, a), "value"], dv.loc[(p, b), "value"], qv.loc[(p, f"q{k}"), "value"]
                unit = dv.loc[(p, a), "unit"]
                if any(math.isnan(x) for x in (x1, x2, xq)):
                    chk("decile_pair_mean", "deciles_vs_quintiles", y, f"q{k}", p, None, None, status="flagged",
                        note=f"codes: {dv.loc[(p, a), 'flag']} {dv.loc[(p, b), 'flag']} {qv.loc[(p, f'q{k}'), 'flag']}")
                    continue
                pair = (n[a] * x1 + n[b] * x2) / (n[a] + n[b])
                step = 1.0 if unit.startswith("dollars") or unit.startswith("percent") else 0.1
                # half a printed step for each side, plus CU counts rounded to thousands
                bound = step + 0.5 * abs(x1 - x2) / (n[a] + n[b])
                chk("decile_pair_mean", "deciles_vs_quintiles", y, f"q{k}", p, xq, pair, bound=bound, note=unit)


def all_vs_groups_checks(df, dataset):
    """Group CU counts add to the all-CU count, and every all-CU mean or value equals the CU-weighted average
    of the group means (tests the column-to-group mapping and that groups partition all CUs)."""
    for y, d in df.groupby("year"):
        n = d[d.path == "Number of consumer units (in thousands)"].set_index("group").value
        gs = [g for g in n.index if g != "all"]
        chk("group_cu_counts_sum", dataset, y, "groups", "Number of consumer units (in thousands)", n["all"],
            float(sum(n[g] for g in gs)), bound=0.5 * (len(gs) + 1))
        v = d[d.stat.isin(["mean", "value"]) & ~d.path.isin(["Number of consumer units (in thousands)", "Lower limit"])]
        for p, sub in v.groupby("path", sort=False):
            s = sub.set_index("group")
            if s.value.isna().any() or "all" not in s.index:
                continue
            w = float(sum(n[g] * s.loc[g, "value"] for g in gs) / sum(n[g] for g in gs))
            unit = s.loc["all", "unit"]
            step = 1.0 if unit.startswith("dollars") or unit.startswith("percent") else 0.1
            bound = step + 0.5 * sum(abs(s.loc[g, "value"] - w) for g in gs) / sum(n[g] for g in gs)
            chk("all_vs_cu_weighted_groups", dataset, y, "all", p, s.loc["all", "value"], w, bound=bound, note=unit)


def tenure_checks(ten):
    """Are non-owners averaged in as zeros? all-CU mean vs CU-share-weighted owner and renter means."""
    for y in sorted(ten.year.unique()):
        t = ten[ten.year == y]
        n = t[t.path == "Number of consumer units (in thousands)"].set_index("group").value
        for item in ["Estimated market value of owned home", "Estimated monthly rental value of owned home",
                     "Mortgage principal paid on owned property", "Other money receipts"]:
            m = t[(t.item_clean == item) & (t.stat == "mean")].set_index("group")
            own, ren = m.loc["owner", "value"], m.loc["renter", "value"]
            ren0 = 0.0 if math.isnan(ren) else ren
            calc = (n["owner"] * own + n["renter"] * ren0) / n["all"]
            # rounding: all-CU mean, owner/renter means ($1) and the three CU counts (thousands)
            bound = 0.5 + 0.5 * (n["owner"] + n["renter"]) / n["all"] + \
                0.5 * (abs(own) + abs(ren0)) / n["all"] + 0.5 * abs(calc) / n["all"]
            chk("tenure_all_cu_mean_vs_weighted", "means_tenure", y, "all", item, m.loc["all", "value"], calc,
                bound=bound, note=f"renter mean {'coded ' + m.loc['renter', 'flag'] + ' -> 0' if math.isnan(ren) else ren}; "
                                f"owner share {n['owner'] / n['all']:.4f}; owner+renter CUs {n['owner'] + n['renter']:.0f} "
                                f"vs all {n['all']:.0f}")


def aggshare_checks(agg, dec, qui):
    for (kind, y), a in agg.groupby(["grouping", "year"]):
        means = dec if kind == "deciles" else qui
        m = means[means.year == y]
        tot = a[(a.path == "Annual aggregate expenditures")].set_index("group")
        nm = m[m.path == "Number of consumer units (in thousands)"].set_index("group").value
        mm = m[(m.path == "Average annual expenditures") & (m.stat == "mean")].set_index("group").value
        chk("aggregate_vs_count_x_mean", f"aggshare_{kind}", y, "all", "Annual aggregate expenditures ($ million)",
            nm["all"] * mm["all"] / 1000, tot.loc["all", "value"], bound=None,
            status="info", note="aggregate column vs (CU count x all-CU mean); thousands x dollars / 1000")
        sh = tot[tot.stat == "agg_share"].value
        chk("aggshare_sum_to_100", f"aggshare_{kind}", y, "groups", "Annual aggregate expenditures", 100.0,
            float(sh.sum()), bound=0.05 * len(sh))
        denom = sum(nm[g] * mm[g] for g in sh.index)
        for g, v in sh.items():   # published group share (0.1 pt) vs CU count x mean from the means table
            chk("aggshare_vs_means_x_counts", f"aggshare_{kind}", y, g, "Annual aggregate expenditures (share, pct)",
                100 * nm[g] * mm[g] / denom, v, bound=0.05 + 0.001)


def release_checks(rel, dec, qui):
    paths = {"average_annual_expenditures": "Average annual expenditures",
             "income_before_taxes": "Consumer unit characteristics: > Income before taxes",
             "consumer_units_thousands": "Number of consumer units (in thousands)"}
    for r in rel.itertuples():
        tab = dec if r.kind == "time_series" else qui
        t = tab[(tab.year == r.ref_year) & (tab.path == paths[r.item]) & (tab.group == r.group) &
                (tab.stat.isin(["mean", "value"]))]
        if t.empty:
            continue
        chk("release_vs_table", f"release {r.release}", r.ref_year, r.group, r.item, float(t.value.iloc[0]), r.value,
            bound=0.5, note=(f"release footnote {r.note}; " if r.note else "") + f"{r.kind} of the {r.data_year} release")


def top_share_rows(dec, qui, agg, dpce):
    """Top decile / top quintile shares of total spending: CE (CU-weighted from the mean tables), CE's own
    aggregate-share tables, and the BLS distributional PCE (deciles of equivalized PCE)."""
    rows = []
    for name, df, top in [("deciles", dec, "d10"), ("quintiles", qui, "q5")]:
        for y in sorted(df.year.unique()):
            d = df[df.year == y]
            n = d[d.path == "Number of consumer units (in thousands)"].set_index("group").value
            m = d[(d.path == "Average annual expenditures") & (d.stat == "mean")].set_index("group").value
            gs = [g for g in n.index if g != "all"]
            tot = sum(n[g] * m[g] for g in gs)
            rows.append(dict(source=f"CE Table {'1110' if name == 'deciles' else '1101'} means x CU counts", year=y,
                             group=top, share_pct=100 * n[top] * m[top] / tot,
                             share_pct_alt=100 * n[top] * m[top] / (n["all"] * m["all"]),
                             note="denominator: sum over groups (share_pct) or all-CU count x mean (share_pct_alt)"))
    for (kind, y), a in agg.groupby(["grouping", "year"]):
        top = "d10" if kind == "deciles" else "q5"
        v = a[(a.path == "Annual aggregate expenditures") & (a.group == top)].value.iloc[0]
        rows.append(dict(source=f"CE aggregate-share table ({kind})", year=y, group=top, share_pct=v,
                         share_pct_alt=None, note="as published (percent of aggregate annual expenditures)"))
    t1 = dpce[(dpce.table == "T1") & (dpce.line == 1)]
    t2 = dpce[(dpce.table == "T2") & (dpce.measure == "share_of_total")]
    for y in sorted(t1.year.unique()):
        s = t1[t1.year == y].set_index("group").value
        rows.append(dict(source="BLS dPCE T1 line 1 (deciles of equivalized PCE)", year=y, group="d10",
                         share_pct=100 * s["d10"], share_pct_alt=None, note="share of total PCE"))
        rows.append(dict(source="BLS dPCE T1 line 1 (deciles of equivalized PCE)", year=y, group="q5",
                         share_pct=100 * (s["d09"] + s["d10"]), share_pct_alt=None, note="d09 + d10, share of total PCE"))
        q5 = t2[(t2.year == y) & (t2.group == "q5") & (t2.category == "Total PCE")].value
        if len(q5):
            rows.append(dict(source="BLS dPCE T2 line 26 'Total: 80-100% share'", year=y, group="q5",
                             share_pct=100 * q5.iloc[0], share_pct_alt=None, note="share of total (unequivalized) PCE"))
    return pd.DataFrame(rows)


def dpce_checks(dpce, meta, vintage):
    t1 = dpce[(dpce.table == "T1") & (dpce.group != "total")]
    sums = t1.groupby(["year", "line"]).value.sum()
    chk("dpce_decile_shares_sum_to_1", f"dpce {vintage}", f"{sums.index.get_level_values(0).min()}-"
        f"{sums.index.get_level_values(0).max()}", "d01..d10", f"{len(sums)} year x line rows", 1.0,
        float(sums.iloc[(sums - 1).abs().argmax()]), bound=0.0055, note=f"max |sum-1| = {(sums - 1).abs().max():.4f}")
    chk("dpce_view_sheet_vs_data_sheet", f"dpce {vintage}", meta["selected_year"], "all", "'Table 1' view vs table1data",
        0.0, meta["view_vs_data_maxdiff"], bound=1e-9)
    t3 = dpce[(dpce.table == "T3") & (dpce.year == 2017)]
    chk("dpce_price_index_2017_base", f"dpce {vintage}", 2017, "all + deciles", "T3 indexes in 2017", 100.0,
        float(t3.value.iloc[(t3.value - 100).abs().argmax()]), bound=0.0005)
    t2 = dpce[dpce.table == "T2"]
    for y in sorted(t2.year.unique()):
        s = dpce[(dpce.table == "T1") & (dpce.line == 1) & (dpce.year == y)].set_index("group").value
        q5 = t2[(t2.year == y) & (t2.group == "q5") & (t2.category == "Total PCE")].value.iloc[0]
        chk("dpce_T1_d09_d10_vs_T2_q5", f"dpce {vintage}", y, "q5", "Total PCE top-quintile share", q5,
            s["d09"] + s["d10"], bound=0.0011 if vintage == "2025-03" else 0.00011)


hierarchy_checks(dec, "means_deciles")
hierarchy_checks(qui, "means_quintiles")
hierarchy_checks(ten, "means_tenure")
share_checks(dec, "means_deciles")
share_checks(qui, "means_quintiles")
rse_checks(dec, "means_deciles")
rse_checks(qui, "means_quintiles")
pair_checks(dec, qui)
all_vs_groups_checks(dec, "means_deciles")
all_vs_groups_checks(qui, "means_quintiles")
tenure_checks(ten)
aggshare_checks(agg, dec, qui)
release_checks(rel, dec, qui)
dpce_checks(dpce, dpce_meta, "2025-03")
dpce_checks(dpce22, dpce22_meta, "2024-11")
# overlap of the two dPCE vintages (2000-2022): rounding only, or revisions?
ov = dpce.merge(dpce22, on=["table", "year", "line", "group", "measure"], suffixes=("_25", "_24"))
for (tb, ms), o in ov.groupby(["table", "measure"]):
    dd = (o.value_25 - o.value_24).abs()
    # 2025-03 prints shares to 4 decimals (2024-11: 4) and T1 totals to whole $ billions (2024-11: 3 decimals)
    bnd = {"decile_share_of_category": 0.0001, "share_of_total": 0.0001, "pce": 0.5}.get(ms)
    big = int((dd > bnd + 1e-9).sum()) if bnd is not None else None
    chk("dpce_vintage_2025_03_vs_2024_11", "dpce", "2000-2022", "all", f"{tb} {ms}", 0.0, float(dd.max()),
        bound=bnd, status=("ok" if big == 0 else "revision") if bnd is not None else "revision" if dd.max() > 0 else "ok",
        note=f"{len(o)} matched cells; median |diff| {dd.median():.6f}"
             + (f"; {big} cells differ by more than rounding" if bnd is not None else ""))
# number formats that carry text (flags) per file
for r in fmts.itertuples():
    letters = re.sub(r'\\[a-z]\\/|General|"[^"]*"', "", r.number_format)
    if re.search(r"[A-Za-z]", letters):
        chk("number_format_unknown_text", r.dataset, r.year, "", r.number_format, None, None, status="gap",
            note=f"{r.n_cells} cells")
    elif FMT_FLAG_RE.search(r.number_format):
        chk("number_format_flag", r.dataset, r.year, "", r.number_format, None, None, status="info",
            note=f"{r.n_cells} numeric cells carry flag {FMT_FLAG_RE.search(r.number_format).group(1)}/ in their format")

tops = top_share_rows(dec, qui, agg, dpce)
checks = pd.DataFrame(CHECKS)
write_tidy(checks, "bls_ce_checks.csv")
write_tidy(tops, "ce_dpce_top_shares.csv")

print("\nverification summary (bls_ce_checks.csv):")
print(checks.groupby(["check", "status"]).size().to_string())
if FAILED:
    print("\nnot vendored:", [f[0] for f in FAILED])
