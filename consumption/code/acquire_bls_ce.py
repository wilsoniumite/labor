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
from common import fetch, RAW, TIDY

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
                      "check: are renters averaged in as zeros in the owned-home addenda rows"))
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
            fetch(SRC, rel, url, what, used)
        except (requests.HTTPError, RuntimeError, requests.RequestException) as e:
            code = getattr(getattr(e, "response", None), "status_code", None)
            failed.append((rel, url, f"HTTP {code}" if code else repr(e)))
    for rel, url, msg in failed:
        print(f"NOT VENDORED: {rel} <- {url}: {msg}")
    return failed


FAILED = vendor_all()
