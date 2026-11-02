# BLS Consumer Expenditure Surveys (CE) and BLS prototype distributional PCE: tidy files

Built by `consumption/code/acquire_bls_ce.py` from the raw files in `consumption/data/raw/bls_ce/`
(80 files, every one listed in that folder's `MANIFEST.csv` with URL, pull date 2026-11-02, sha256, bytes, use).
Run from the repo root: `venv/bin/python -I consumption/code/acquire_bls_ce.py`. Vendored files are never
re-downloaded, so the rerun is offline (about 15 s) and rebuilds every file below byte for byte (checked: two
clean rebuilds gave identical sha256 for all 12 outputs). The only network call left on a rerun is one try at
the single file that was not available (see "Not vendored").

Publisher for everything here: U.S. Bureau of Labor Statistics (www.bls.gov), CE program and the Division of
Price and Index Number Research. Requests carried the BLS User-Agent from `common.py`.

## Raw inventory (`raw/bls_ce/`)

| Folder | Files | What |
|---|---|---|
| `tables/deciles/` | `cu-income-deciles-before-taxes-YYYY.xlsx`, 2014-2025 (12) | Table 1110, deciles of income before taxes: means, shares, SEs, RSEs (CVs before 2022). BLS lists it "2014 forward"; every year exists as xlsx (BLS also lists PDF versions for 2014-2022; not vendored). |
| `tables/quintiles/` | `cu-income-quintiles-before-taxes-YYYY.xlsx`, 2019-2025 (7) | Table 1101, quintiles of income before taxes (exists 2012 forward; 2019-2025 requested). |
| `tables/aggshare/` | deciles and quintiles, 2019-2025 (14) | "Shares of annual aggregate expenditures and sources of income" tables (also numbered 1110/1101). BLS's own group shares of aggregate spending. |
| `tables/tenure/` | `cu-housing-tenure-2024.xlsx`, `-2025.xlsx` | Table 1710, housing tenure. Used to test how renters enter the owned-home addenda. |
| `release/` | `cesan_MMDDYYYY.htm` for data years 2014-2025 (12), plus `cesan_10292026.pdf` | Annual news releases "Consumer Expenditures--YYYY" (archived copies). 2025: USDL-26-1619, 2026-10-29. |
| `index/` | `tables.htm`, `mean-item-share-average-standard-error.htm`, `aggregate-group-share.htm` | BLS listing pages (provenance for which years exist). |
| `notices/` | 11 pages | 2025 funding-lapse Q&A and weight adjustment, PUMD replication note, BLS missing-data article (background paper for the expert panels), CPI-side lapse page, expert-panel notice, 2025 release notice, two-year-tables/Fay's BRR notice, standard-errors page, 2024 release notice, after-tax income notice. |
| `docs/` | `csxgloss.htm`, `csxfaqs.htm`, `tables-getting-started-guide.htm`, `hom_cex_{concepts,calculation,presentation}.htm` | Glossary, Q&A, tables guide, Handbook of Methods chapters. |
| `dpce/` | 13 files | Distributional PCE: `pce-ce-distributions.htm` (main page), `distributional-pce-2000-2023.xlsx` (results, March 2025), `ce_pce_map.xlsx`, `distributional-pce-2000-2022.xlsx` (November 2024 results, the file the price-index note links), `pce-ce-distribution-methods.htm`, `Methods_changes_page.htm`, `Inflation_note.htm`, `methodology-for-distributing-personal-saving.htm`, `ec240050.pdf` (WP 575), `ec220120.pdf` (WP 557), the 2024 Business Economics overview PDF, `curtin-2020-annual-COVID-impact.pdf`. |

**Not vendored.** `distributional-pce-interim-2017.xlsx`: named only in a hidden `<span>` (display:none) at the
bottom of `pce-ce-distributions.htm`, not linked. Tried at
`https://www.bls.gov/cex/cecomparison/distributional-pce-interim-2017.xlsx` (the folder of the other results
files): HTTP 404 on 2026-11-02. No substitute taken. Also not fetched, as they are other publishers or out of
scope: the BEA distribution pages, the Wiley article (doi 10.1111/roiw.70004), the OECD EG DNA page, and the CE
2020 annual report.

## Tidy files

| File | Rows | Content |
|---|---|---|
| `ce_income_deciles_long.csv` | 71,643 | Table 1110, 2014-2025, every cell, long |
| `ce_income_quintiles_long.csv` | 21,408 | Table 1101, 2019-2025, same schema |
| `ce_housing_tenure_long.csv` | 4,710 | Table 1710, 2024-2025, same schema |
| `ce_income_aggshare_long.csv` | 16,473 | aggregate-share tables, deciles and quintiles, 2019-2025 |
| `ce_table_footnotes.csv` | 208 | per table and year: title, footnote legend, source line, notes |
| `ce_release_headlines.csv` | 114 | headline numbers printed in the 12 annual releases |
| `bls_dpce_long.csv` | 7,296 | distributional PCE results workbook, March 2025 (2000-2023) |
| `bls_dpce_2000_2022_long.csv` | 6,992 | same schema, November 2024 workbook (2000-2022) |
| `ce_pce_map.csv` | 799 | CE UCC to PCE category map used for the distributional PCE |
| `bls_dpce_page_tables.csv` | 802 | every table and chart table embedded in the four dPCE web pages |
| `ce_dpce_top_shares.csv` | 105 | top-decile and top-quintile shares of total spending, CE and dPCE (derived check) |
| `bls_ce_checks.csv` | 34,216 | every verification number (see "Verification") |

All files are plain CSV with a header row, UTF-8, `\n` line ends; numbers written with up to 10 significant
digits; empty field = missing. None is above 20 MB, so none is gzipped.

### `ce_income_deciles_long.csv`, `ce_income_quintiles_long.csv`, `ce_housing_tenure_long.csv`

One row per numeric (or coded) cell of the table.

| Column | Meaning |
|---|---|
| `year` | calendar year of the table (data year) |
| `row` | 0-based row index in the sheet of the cell's row (openpyxl row minus 1) |
| `item` | the row label as printed, stripped (keeps footnote markers such as `Number of consumer units (in thousands) a/`) |
| `indent` | the label cell's indent level from openpyxl `alignment.indent` (see "Hierarchy") |
| `parent_item` | clean label of the parent (empty at top level) |
| `path` | clean labels from the top of the hierarchy joined by `' > '`, e.g. `Average annual expenditures > Housing > Shelter > Owned dwellings`. Unique per year, group and stat. |
| `group` | deciles: `all`, `d01`..`d10` (Lowest..Highest 10 percent); quintiles: `all`, `q1`..`q5`; tenure: `all`, `owner`, `owner_mortgage`, `owner_no_mortgage`, `renter` |
| `stat` | `mean`, `share`, `se`, `rse`, or `value` for a label row that carries a single number (CU count, lower limit, age, average numbers, percent distributions) |
| `value` | the number (float); empty when the cell holds a code |
| `flag` | the code as printed when the cell is a code (`b/`, `c/`, `d/`, `n.a.`), or, for 2024 and 2025, the code BLS attaches to a number through the cell's number format (`#.00# \b\/`) while the number itself is kept in `value` |
| `flag_kind` | the code resolved through that table's own legend: `too_small` (value too small to display), `suppressed_rse25` (2022-2023: withheld because RSE >= 25%), `high_rse25` (2024-2025: shown, RSE >= 25%, use with caution), `no_data` (no data reported), `not_applicable` (n.a.) |
| `item_clean` | `item` without trailing footnote markers (` a/`, ` b/`, `#`) and with whitespace normalised |
| `item_row` | 0-based sheet row of the item's label (stat rows sit below it) |
| `depth` | 0-based depth in the hierarchy |
| `is_leaf` | the item has no child items in that year's table |
| `stat_label` | the stat row label as printed: `Mean`, `Share`, `SE`, `RSE`, `CV(%)`; empty for `value` rows |
| `unit` | e.g. `dollars per consumer unit per year`, `percent of the group's average annual expenditures`, `thousands of consumer units`, `number per consumer unit (mean)`, `percent (100 x SE / mean)` |

**Coverage.** Deciles 2014-2025 (12 tables), quintiles 2019-2025 (7), tenure 2024-2025; latest period 2025
(released 2026-10-29). Items carrying numbers per year: 174 (2014-2019), 148 (2020-2022), 144 (2023), 137
(2024-2025); expenditure items including the total: 102 (2014-2023), 101 (2024-2025), of which leaves 76 (to
2022), 75 (2023), 74 (2024-2025). The quintile table has exactly the decile table's stub, in the same order,
every year 2019-2025. Included: CU count (thousands), lower income limit, income before taxes (mean, SE,
RSE), income after taxes (to 2023), age of reference person, average numbers (people, children under 18,
adults 65 and older, earners, vehicles), percent distributions (reference person sex, housing tenure with and
without mortgage, race, Hispanic origin, education, at least one vehicle), every expenditure row, sources of
income, personal taxes (to 2023), and the addenda (net change in assets and liabilities to 2022, other money
receipts, mortgage principal paid, estimated market value of owned home, estimated monthly rental value of
owned home, gifts of goods and services to 2019). Header labels without numbers ("Consumer unit
characteristics:", "Average number in consumer unit:", "Addenda:", ...) have no rows of their own; they appear
in `path` and `parent_item`.

**Hierarchy.** Every one of the 12 decile workbooks, 7 quintile workbooks and 2 tenure workbooks carries indent
levels in the label cells, so the hierarchy is read from the files, not reconstructed: the parent of a label
is the nearest label above it with a smaller indent. Two indent scales occur: 2014-2016 labels use 0-4 (stat
rows 10); 2017-2025 labels use 0, 2, 4, 6, 8 (stat rows 13; footnote legend lines 1). Top-level sections:
`Number of consumer units (in thousands)`, `Lower limit`, `Consumer unit characteristics:`, `Percent
distribution:`, `Average annual expenditures` (the 14 major categories sit directly under it), `Sources of
income and personal taxes:` (to 2023) or `Sources of pretax income:` (2024-2025), `Addenda:`. The same label
can occur twice in a year (`Income before taxes` under characteristics and under sources of income); `path`
tells them apart.

Children add to parents (checked every year and group, see "Verification"), with two exceptions where BLS
prints only part of a parent's components, so leaves do not exhaust the parent and the remainder has no row:

- `Transportation > Gasoline and other fuels` (2023-2025): only `Gasoline` is shown; the unshown remainder is
  up to 14.9% of the parent (2025 d10: $548 of $3,680).
- `Transportation > Vehicle purchases (net outlay)` (2024-2025): `Other vehicles` was dropped; new plus used
  cars and trucks fall short of the parent by up to 2.5%.

Before 2023 `Gasoline, other fuels, and motor oil` (`Gasoline and motor oil` to 2016) is a leaf. Aggregating
leaves therefore needs a residual (parent minus shown children) for these two parents in those years.

**Codes change meaning by year and by table.** Read codes through `flag_kind` (or `ce_table_footnotes.csv`),
never by letter: in 2025 the high-RSE code is `b/` in Table 1110, `d/` in Table 1101 and `c/` in Table 1710;
`c/` means "too small to display" in 2024 deciles but "suppressed" in 2023. Counts of coded mean cells in
Table 1110: 2022: 136 suppressed (RSE >= 25%) and 11 no data; 2023: 101 suppressed; 2024: 94 means shown but
flagged high-RSE; 2025: 124 flagged; earlier years at most 3. In 2022-2023 suppression reaches major
categories for some deciles (2022: Apparel d01, Cash contributions d02/d03/d06, Education d02/d05; 2023: Reading
d01, Education d01-d03, Miscellaneous d04, Cash contributions d09), so the 14 majors do not add to the total in
those groups. BLS says the suppressed estimates are in the CE database (LABSTAT `cx`, not vendored here).
Within a parent, a child coded "too small to display" can be read as zero; suppressed or no-data children
cannot.

**Statistics.** `share` = percent of the group's average annual expenditures for expenditure rows, percent of
the group's income before taxes for income and tax rows (both verified on every cell). `rse` = 100 x SE / mean;
before 2022 BLS printed it as `CV(%)` (coefficient of variation): same statistic (every printed CV and RSE lies
inside the interval implied by rounding of 100 x SE / mean), so both map to `rse` and `stat_label` keeps the
printed name. Variance method: standard BRR through 2024, Fay's BRR from 2025 (BLS did not publish 2024-2025
two-year tables because of this), so `se`/`rse` are not comparable across the 2024/2025 seam. RSEs are negative
where the mean is negative (mortgage principal paid, some tax rows).

**Units and rounding.** Means in whole dollars per consumer unit per year (monthly for `Estimated monthly
rental value of owned home`; a stock for `Estimated market value of owned home`); CU counts in thousands;
average numbers to one decimal (so children, adults 65+ and people per CU carry up to +/-0.05 rounding: e.g.
0.3 children can be 0.25-0.35); percent distributions in whole percent; shares to 0.1; SE and RSE to 0.01.
`Mortgage principal paid on owned property` is printed negative (a reduction in liabilities; it is not an
expenditure).

### `ce_income_aggshare_long.csv`

Same columns as above plus `grouping` (`deciles`/`quintiles`), without `stat_label`. One row per item and group
(no stat rows in these tables). `stat`: `aggregate` for the `all` column of expenditure, income and tax rows
(millions of dollars per year, all CUs); `agg_share` for the group columns of those rows (percent of the
all-CU aggregate for that item); `value` for CU counts (thousands), `Percent distribution of consumer units`,
characteristics (means) and percent distributions. The expenditure total is labelled `Annual aggregate
expenditures` here (not `Average annual expenditures`). Extra code `e/` = "data are likely to have large
sampling errors" (`flag_kind` `large_sampling_error`). Shares are printed to 0.1 point, so implied group means
are coarse (a 0.05-point rounding on a 4% share is 1.25% of the mean).

### `ce_table_footnotes.csv`

`dataset` (`means_deciles`, `means_quintiles`, `means_tenure`, `aggshare_deciles`, `aggshare_quintiles`),
`year`, `code`, `meaning`. Codes: `a/`..`e/`, `n.a.`, `#` (2020: "Data collection for this item began in June
2020. Stimulus payments delivered to respondents interviewed in April and May of 2020 were not included"),
plus pseudo-codes `title` (sheet title), `source` (source line with BLS release month) and `note`. The legend
also defines label markers: `a/` on the CU count = "rounded to the nearest thousands" (2020+); 2023 `b/` on the
tax and after-tax rows = computed with two versions of NBER TAXSIM Model 35.

### `ce_release_headlines.csv`

Numbers printed in the annual releases' `<pre>` tables: `release`, `data_year`, `kind` (`time_series` = the
headline table's year columns, read from its own `Item 2019 2020 2021` header; `quintile_table` = the
all-CU-plus-five-quintiles table, 2024 and 2025 releases), `item` (`average_annual_expenditures`,
`income_before_taxes`, `consumer_units_thousands`), `label` as printed, `ref_year`, `group`, `value` (dollars or
thousands), `note` (release markers: `(b)` and `*` both mean "differs from earlier publication because of
post-publication corrections"; the tables were not republished).

### `bls_dpce_long.csv` and `bls_dpce_2000_2022_long.csv`

Columns: `vintage` (`2025-03` / `2024-11`), `table` (`T1`, `T2`, `T3`), `year`, `line` (workbook line),
`nipa_2_3_5_line` (T1 only: NIPA Table 2.3.5 line 1-22, and 30 for the market-based PCE addendum, per the
workbook note "lines 1-22 and 30"), `pce_mp` (T1 only: a code carried in the data sheet, 0..830, not defined in
the workbook), `category`, `category_indent` (leading spaces of the printed title, T1), `grouping`, `group`,
`measure`, `value`, `unit`.

What the March 2025 workbook (`distributional-pce-2000-2023.xlsx`, "Version: March 2025", "Results are based
on NIPA data released September 26, 2024") contains:

- Sheets: `Description of Tables`; `Table 1` (a year-selector view, cached on 2023, identical to the data
  sheet); `table1data` (the data: 24 years x 23 lines); `years` (the drop-down list); `Table 2`; `Table 3`. The
  description sheet says "This file contains 2 tables" but there are three (Table 3 was added in December 2024).
- Ranking: consumer units ranked by total PCE per CU equivalized by the square root of CU size, weighted by the
  CE sampling weight finlwt21; deciles are tenths of weighted CUs (not of persons). It ranks on spending, not
  income. PCE is allocated with CE microdata (Interview, with Diary matched in for about 6%), imputations for
  out-of-scope items (third-party health care, financial services furnished without payment, ...), a Pareto
  adjustment of the top 5% of spenders, and scaling to PCE for 150 categories (NIPA Table 2.4.5U detail).
- T1 "Personal Consumption Expenditures by Major Type of Product and Decile": for each year 2000-2023, the 22
  lines of NIPA Table 2.3.5 (PCE; goods; durable; motor vehicles; furnishings; recreational goods; other
  durable; nondurable; food off-premises; clothing; gasoline and energy; other nondurable; services; household
  services; housing and utilities; health care; transportation services; recreation services; food services
  and accommodations; financial services and insurance; other services; NPISH final consumption) plus
  market-based PCE. Measures: `pce` (category total, billions of current dollars, whole billions in this
  vintage) and `decile_share_of_category` (fraction of the category total going to each decile; the ten add to
  1 within 0.0002). The NPISH line carries exactly the total-PCE decile shares (allocated in proportion). So
  the workbook has category x decile x year detail at the 22-line major-product level; the 150-category detail
  is not published.
- T2 "Inequality Metrics", 2000-2023: lines 1-17 for equivalized PCE (mean and median, nominal and 2017
  dollars; quintile, 80-99%, top 5% and top 1% shares; 90/10; Gini; Theil; mean log deviation; CV), lines
  18-29 for total (unequivalized) PCE (mean, median, the same shares) with groups still ranked by equivalized
  PCE. Groups `all`, `q1`..`q5`, `p80_99`, `top1`, `top5`. Units: dollars per CU per year or fractions.
- T3 "Price Indexes by decile of Equivalized PCE (2017 = 100)", 2000-2023: the published PCE price index and
  the market-based PCE price index (`group` `all`) and their decile versions `d01`..`d10` (Fisher chain of NIPA
  Table 2.4.4U detail indexes with decile weights).

Vintages: the November 2024 file (`2024-11`, 2000-2022, same layout) is kept because the price-index note links
it. The March 2025 file revises it: T1 totals agree to rounding, but 4,446 of 5,290 overlapping decile shares
differ by more than rounding (median 0.0004, largest 0.045: 2020 furnishings, top decile 0.2601 vs 0.3054); T2
statistics and T3 indexes also moved (indexes by up to 0.13 points). Use `bls_dpce_long.csv` (2025-03) for all
years; do not mix vintages.

### `ce_pce_map.csv`

The 799 data rows of `ce_pce_map.xlsx` (trailing "End of sheet" row dropped): `row` (0-based sheet row),
`ucc_title`, `ucc_split` (as printed, text; suffixes `_1`, `_2` mark a UCC split across PCE categories),
`ucc` (6-digit code before the suffix, text, leading zeros kept), `split`, `ce_source` as printed
(`Interview`, `Diary`, `Interview*`, `Diary*`), `ce_source_base` (without `*`), `source_note_flag` (`*`
present: per the map's notes, the Interview supplies the food or alcohol aggregate and the Diary the
proportions within it), `firstyq`, `lastyq` (first and last year-quarter of the UCC, e.g. `19902`, blank =
current), `pce_title`, `pce_series` (BEA series mnemonic, e.g. `DNEARC` new autos; 135 distinct), `notes`.
746 distinct UCCs. Per the dPCE page, this map differs from the one the CE division uses for its routine
CE-PCE comparisons (more is sourced from the Interview).

### `bls_dpce_page_tables.csv`

Every table on `pce-ce-distributions.htm`, `pce-ce-distribution-methods.htm`, `Methods_changes_page.htm` and
`Inflation_note.htm`: Highcharts chart tables (embedded as JSON strings) and HTML tables. Columns: `page`,
`table_no`, `kind` (`chart_table`/`html_table`), `title` (caption), `section` (a one-cell heading row inside a
table), `row`, `row_label`, `col_label`, `value_raw` (as printed), `value` (numeric parse, `$ , %` stripped;
empty for text), `is_percent`. Contents worth knowing: real PCE by quintile of equivalized PCE 2000-2023
($2017 bn); DPI, PCE and saving for the bottom and top quintiles of equivalized disposable income 2004-2022
(BEA-BLS joint distribution, $2017 bn: the one series here ranked by income); Table 3.1 CE/PCE coverage ratios
by product group 2019-2023 after adjustments and imputations (0.74-0.78 overall); Table 3.2 weighting
alternatives (2019); Table 3.3 used-vehicle processing (2019); decile shares of PCE in 2022, July vs December
2024 methods (top decile 27.3% vs 26.5%); the price-index note's Figures 1-7.

### `ce_dpce_top_shares.csv`

Derived (a cross-check, not modelling): `source`, `year`, `group` (`d10`, `q5`), `share_pct`, `share_pct_alt`,
`note`. For CE: share of total spending = N_g x mean_g / sum over groups of N x mean, with N the printed CU
counts and mean the printed `Average annual expenditures` (`share_pct_alt` uses the all-CU count x mean as
denominator; the two agree to 0.01 point); and the published aggregate-share table value. For the dPCE: T1
line 1 top decile, top two deciles, and T2 line 26.

| Year | CE top decile, means x counts | CE published agg. share | CE top quintile, means x counts | CE published agg. share |
|---|---|---|---|---|
| 2019 | 23.36 | 23.3 | 38.70 | 38.7 |
| 2020 | 22.26 | 22.3 | 37.30 | 37.3 |
| 2021 | 23.40 | 23.4 | 38.49 | 38.5 |
| 2022 | 22.88 | 22.9 | 38.54 | 38.6 |
| 2023 | 23.45 | 23.4 | 38.86 | 38.9 |
| 2024 | 22.89 | 22.9 | 38.45 | 38.4 |
| 2025 | 23.64 | 23.6 | 38.88 | 38.8 |

CE deciles and quintiles are of income before taxes, CU-weighted, unequivalized; dPCE deciles are of
equivalized PCE and the shares are of PCE (national-accounts scope). The two are different concepts and should
not be compared as levels. dPCE top decile share of total PCE: 26.30 (2000), 27.18 (2007, peak), 26.26 (2017),
26.11 (2019), 24.96 (2020), 26.07 (2021), 26.39 (2022), 25.74 (2023); top quintile (T2 line 26) 40.07 (2000),
41.12 (2007), 39.83 (2019), 38.31 (2020), 39.67 (2021), 39.98 (2022), 39.50 (2023); all years in the file.

### `bls_ce_checks.csv`

Columns: `check`, `dataset`, `year` (text: a year or a range such as `2000-2022`), `group`, `item`,
`reference`, `observed`, `diff` (observed minus reference), `rel_diff`, `bound` (the rounding bound for that
comparison), `status`, `note`. Status: `ok` within the bound; `small_gap` beyond it but under 0.5% relative;
`gap` 0.5% or more; `partial_parent` (the two parents above); `flagged_children` / `flagged_parent` / `flagged`
(a coded cell makes the comparison impossible); `revision` (dPCE vintages differ beyond rounding); `info`.

## Definitions (BLS glossary, Q&A, tables guide; raw `docs/`)

- **Consumer unit (CU):** "families, single persons living alone or sharing a household with others but who are
  financially independent, or two or more persons living together who share major expenses."
- **Income before taxes:** "the total money earnings and selected money receipts during the 12 months prior to
  the interview date": wages and salaries, self-employment income, Social Security and retirement, interest,
  dividends, rental and other property income, unemployment, workers' compensation and veterans' benefits,
  public assistance, SSI and SNAP, regular contributions for support, other income. Missing income components
  are multiply imputed (since 2004).
- **Deciles/quintiles:** CUs sorted by income before taxes; cumulative population weights; first decile =
  cumulative weight up to 10% of CUs, and so on. BLS does the cumulation within each quarter, so group counts
  are not exactly equal. The two groupings nest only approximately in the published tables: decile-pair CU
  counts equal the quintile counts, but lower limits differ by up to $3 and means by up to 0.5% (below).
- **Expenditures:** "the transaction costs, including excise and sales taxes, of goods and services acquired
  during the interview or recordkeeping period," including gifts, excluding business purchases and periodic
  credit or installment payments; full cost recorded at purchase. Vehicle purchases are net outlays (price
  minus trade-in). Mortgage principal is not an expenditure (it is in the addenda).
- **Owned dwellings:** mortgage interest, home equity interest, property taxes and insurance, refinancing and
  prepayment charges, ground rent, management and security, maintenance and repairs (owner occupied).
  **Rented dwellings:** rent paid, rent received as pay, parking, maintenance and other. **Other lodging:** "all
  expenses for vacation homes, school, college, hotels, motels, and other lodging while out of town."
- **Personal insurance and pensions:** life, endowment, annuities and other personal insurance, other non-health
  insurance, and retirement, pensions and Social Security (employee Social Security contributions, employee
  contributions to railroad, government and private pensions, self-employed retirement).
- **Cash contributions:** "cash contributed to persons or organizations outside the consumer unit, including
  alimony and child support payments; care of students away from home; and contributions to religious,
  educational, charitable, or political organizations."
- **Other money receipts:** lump sums from estates or trusts, insurance, sale of house furnishings, refunds
  (Social Security overpayment, insurance policies, property taxes).
- **Estimated market value of owned home / Estimated monthly rental value of owned home:** not defined in the
  glossary. The Q&A states that published figures "are averages for all consumer units, or for all the consumer
  units in a particular demographic group", including CUs that did not buy the item. Verified for these rows
  with the tenure table: the all-CU mean equals the owners' mean times the owner share of CUs, with renters
  counted as zero (renter column coded "no data reported"): 2024 market value $310,670 printed vs $310,671
  computed (owner share 0.6491 x $478,639); monthly rental value $1,556 vs $1,555.8; 2025 $317,320 vs
  $317,321 and $1,578 vs $1,578.6. So in the all-CU and decile means renters (and other non-owners) count as
  zeros. Divide by the homeowner percentage to get a per-owner figure.
- **Health:** CE healthcare is out-of-pocket (premiums the household pays, medical services, drugs, supplies);
  employer-paid premiums and public programs are not in CE (the dPCE imputes them).

## Line-item changes 2014-2025 (Table 1110; Table 1101 identical where it overlaps)

- 2015: `Public assistance, supplemental security income, food stamps` renamed `Public assistance, Supplemental
  Security Income, Supplementary Nutrition Assistance Program (SNAP)`.
- 2017: `Gasoline and motor oil` renamed `Gasoline, other fuels, and motor oil`.
- 2020: the addenda block `Gifts of goods and services` (27 rows including its total) removed; `Money income before taxes` renamed
  `Income before taxes`; `Stimulus payment (new UCC Q20202)` added under personal taxes (negative values; with
  it personal taxes = federal + state and local + other + stimulus within rounding).
- 2021: wording only: `Food prepared by consumer unit on out of town trips`, `Small appliances and miscellaneous
  housewares`, `Maintenance, repairs, insurance, and other expenses`, `White, Asian, and all other races, not
  including Black or African-American`, `Interest, dividends, rental income, and other property income`;
  `Stimulus payment`.
- 2022: `Stimulus payment (through Q20221)`.
- 2023: `Processed fruits` + `Processed vegetables` merged into `Processed fruits and vegetables`; `Laundry and
  cleaning supplies` became `Laundry and cleaning products (new UCC Q20231)`; `Gasoline, other fuels, and
  motor oil` became `Gasoline and other fuels` with one child `Gasoline`; `Stimulus payment` removed; `Net
  change in total assets and liabilities` (and its two children) removed.
- 2024: `Income after taxes` (characteristics and income block) and the whole `Personal taxes` block removed
  (NBER TAXSIM was not updated for tax year 2024; still absent in 2025); `Sources of income and personal
  taxes:` renamed `Sources of pretax income:`; `Pensions and Social Security` renamed `Retirement, pensions, and
  Social Security`; `Other vehicles` removed from vehicle purchases; `Laundry and cleaning products` without the
  UCC remark.
- 2025: no change in the stub (a new military-status table was added elsewhere).

## 2025 and other year-specific caveats

- **2025 funding lapse.** Census could not collect CE in October and November 2025 (lapse 2025-10-01 to
  2025-11-12; collection resumed 2025-12-05). BLS adjusted weights: Interview expenditures for July and October
  2025 x 3/2 and for August and September x 3 (about a third and two thirds of those months' reports were
  missing because of the 3-month recall); Diary weights for September and December 2025 doubled to stand for
  October and November. BLS expects accurate estimates with larger variances; the adjustments are not applied
  to the PUMD (factors and MO_SCOPE changes in `notices/ce-pumd-2025-shutdown-impact.htm`). The 2025 annual
  CPI-U used in the release averages 11 months (October 2025 CPI not collected).
- **2025 methods.** Fay's BRR variances (SE/RSE break); geographic sample redesign based on the 2020 census
  (some MSAs in or out of the sample); part of `Other vehicle expenses` now sourced from the Diary (BLS says
  this contributes to the significant 13.3% rise in that category).
- **2024-2025:** no tax or after-tax income rows. **2022-2023:** RSE >= 25% cells suppressed (see above);
  **2024-2025:** shown with a high-RSE flag. **2023:** tax rows computed with two TAXSIM versions. **2020:**
  pandemic collection disruption (BLS research paper by Curtin vendored in `dpce/`), stimulus row.
- **Corrections not republished.** BLS reports some earlier-year totals differently in later releases, saying
  the post-publication corrections did not meet the republication threshold, so the tables (as vendored) keep
  the original numbers: 2015 income before taxes $69,627 in the table vs $69,629 in the 2015 and 2016 data
  releases;
  2020 average annual expenditures $61,334 vs $61,332 (2021 and 2022 releases, marked `*`); 2022 $72,967 vs
  $72,973; 2023 $77,280 vs $77,158; 2024 $78,535 vs $78,527 (2024 and 2025 releases, marked `(b)`). The
  vendored 2024 table (the one the 2026-06-14 post used) carries the source line "December, 2025" and the
  December 2025 release's totals.

## Verification (all in `bls_ce_checks.csv`)

- **Hierarchy** (every parent with children, every year and group, deciles, quintiles and tenure): 5,478 sums,
  106 differences (net change in assets minus liabilities) and 866 percent blocks summing to 100 lie within
  their rounding bounds; 2 sums are just outside (Transportation 2023 d08 and q4: $3 against a bound of $2.5,
  0.02%), so the largest non-structural gap anywhere is $3. The 14 major categories add to `Average annual
  expenditures` within $3 in all 173 testable cases. Not testable because a child or the parent is coded: 278
  comparisons (196 sums, 54 percent blocks, 28 with a coded parent; mostly 2022-2023 suppression and the
  tenure table's `n.a.` cells). The two partial parents listed above: 98 comparisons.
- **Shares:** all 19,056 printed shares equal 100 x mean / group total (expenditure) or / income before taxes
  (income and taxes) within rounding.
- **RSE/CV:** every printed RSE or CV(%) (684-1,661 cells per table-year with |mean| >= $1) lies in the
  interval implied by rounding of 100 x SE / mean.
- **All-CU vs groups:** decile and quintile CU counts add to the all-CU count every year; all-CU means and
  values equal the CU-weighted average of the group values within rounding for 2,648 of 2,760 item-years, the
  rest within 0.31% (Diary-sourced items mostly).
- **Deciles paired into quintiles (2019-2025):** CU counts of each decile pair equal the quintile count within
  1 thousand; of 4,904 comparable means and values, 4,752 within rounding (including the CU-count rounding
  term), 152 beyond it but under 0.5% (largest: Footwear 2023 q1, $212.97 vs $214, 0.48%; largest absolute:
  total expenditure 2025 q5, $159,493 vs $159,512, 0.012%; income before taxes always within $1.7); 206 not
  comparable (coded). Quintile lower limits equal the odd decile's lower limit within $3.
- **Aggregate-share tables:** shares add to 100 within 0.1; published group shares of total spending match CU
  count x mean within the 0.05 printing rounding in 89 of 105 cases and within 0.08 point in all (largest:
  2025 d04 7.0 published vs 6.92, 2025 q5 38.8 vs 38.88); `Annual aggregate expenditures` differs from all-CU
  count x mean by -0.065% to +0.027%. The aggregate tables are therefore close to, but not exactly, count x
  mean.
- **Releases:** the 2025 tables reproduce the 2025 release exactly (all CUs: 137,994 thousand CUs, income
  $110,847, expenditures $81,905; quintile expenditures $37,935 / $51,405 / $68,983 / $92,250 / $159,512, income
  $18,125 / $46,080 / $78,584 / $126,349 / $286,188); 101 of 108 release-vs-table comparisons (reference years
  2014-2025) exact, the 7 others are the corrections listed above.
- **dPCE:** decile shares add to 1 (max deviation 0.0002 in 2025-03, 0.0000 in 2024-11); `Table 1` view equals
  `table1data`; all T3 indexes equal 100.000 in 2017; T1 top-two-decile share equals T2 line 26 within 0.0001
  in every year; the vintage comparison is described above.
- **Renters in the owned-home addenda:** see Definitions (8 tenure comparisons, all within rounding).
- **Number formats:** the only text-bearing number formats are the 2024-2025 flag formats (46 file x format
  combinations, all decoded into `flag`).

## Open items for later steps

- The 2022-2023 decile and quintile tables suppress RSE >= 25% cells, including some major categories for some
  deciles. BLS states the values are in the CE database (`https://download.bls.gov/pub/time.series/cx/`,
  `cx.data.1.AllData` 127 MB and `cx.series` 32 MB on 2026-11-02, plus `cx.aspect` 777 MB for SEs and shares).
  Not vendored (outside this step's list; the data file exceeds GitHub's 100 MB file limit unless compressed).
- `distributional-pce-interim-2017.xlsx`: 404 (see above).
- The BLS dPCE stops at 2023; the BEA distribution of personal income pages hold the joint DPI-PCE-saving
  results (another source family).
