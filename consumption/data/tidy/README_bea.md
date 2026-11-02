# BEA tidy files: PCE by product, personal income, and BEA's distributional statistics

Built by `consumption/code/acquire_bea.py` from the raw files in `consumption/data/raw/bea/` and nothing else.
Run it from the repo root with `venv/bin/python -I consumption/code/acquire_bea.py`. Files that are already
vendored are not downloaded again, and a download that failed once is not retried unless you pass
`--retry-failed` (`--offline` skips the network entirely). So a rerun is offline and rebuilds every file below
byte for byte. This was checked by running the script twice and comparing sha256 hashes; the gzip is written
with `mtime=0`.
Every cross-check is written to `bea_checks.csv`, which has 130 rows and the columns `check`, `status`
(pass / FAIL / info), `value` and `detail`. The numbers quoted in this README come from that file.

## 1. Vintage

| Source | Vintage | Coverage |
|---|---|---|
| NIPA flat files and both Section 2 workbooks | Released with *Personal Income and Outlays, September 2026* (BEA 26-46, 8:30 a.m. EDT, Thursday 2026-10-29). Workbook stamps read "Data published October 29, 2026". Files were created Oct 28 2026 at 2:35PM (underlying-detail workbook) and 1:59PM (published tables). The next release, with October 2026 data, is on 2026-11-25. | Monthly data run through **2026-09**. Annual data run through **2025**. |
| Distribution of personal income (national) | June 16, 2026 release. NIPA Table 2.10 is stamped "Data published June 16, 2026", the release blog post is dated 2026-06-16, and the workbooks say "Current Version: 2026". | 2000-2023 are final, 2024 is provisional, and 2025 is an experimental nowcast covering quintiles only. |
| Income-stratified PCE price index (ISPCEPX) | June 2026 release (same release as above) | Annual, 2000-2024. The 2024 weights are imputed. |
| Joint DPI/PCE distribution (distribution of personal saving) | Workbook posted under /2026-05/, documentation under /2026-04/ | Annual, 2000-2023 |

The distributional files predate the current NIPA vintage, and their NIPA totals differ from the October 2026
vintage from 2021 onward:

- **Summary-file personal income totals** (bn $) against today's Table 2.1:
  - 2021: 21,499 vs 21,507.
  - 2022: 22,154 vs 22,157.
  - 2023: 23,585 vs 23,642.
  - 2024: 24,906 vs 25,043.
  - 2000-2020 agree to within the $1bn rounding.
- **Joint-file totals** against today's Table 2.1:
  - 2023 DPI is 59 bn lower.
  - 2023 PCE is 61 bn higher.
  - 2022 PCE is 20 bn higher.
  - 2000-2020 match.
- **ISPCEPX "Published PCE PI"** against today's DPCERG: 2021 +0.07, 2022 +0.06, 2023 +0.01, 2024 +0.01 index points.

## 2. Raw files (`consumption/data/raw/bea/`; URLs, dates and sha256 in `MANIFEST.csv`)

| File | What it is |
|---|---|
| `nipa/FlatFiles.zip` | NIPA flat files: `nipadataA.txt`, `nipadataQ.txt`, `nipadataM.txt`, `SeriesRegister.txt`, `TablesRegister.txt`. Each member has the same size as the file posted individually under `/national/Release/TXT/`, and the two registers are byte-identical to the separate downloads. **They carry the underlying-detail (U) series**: SeriesRegister maps 390 series to U20405 lines, and `nipadataM.txt` has them monthly from 1959M01 to 2026M09. No separate underlying-detail flat file exists; `NipaDataM_U.txt`-style URLs return BEA's 200-status "not found" HTML page. |
| `nipa/xls_underlying/Section2All_xls.xlsx` | Underlying-detail workbook for Section 2: Tables 2.3.4U-2.3.6U and 2.4.3U-2.4.6U, as A, Q and M sheets. |
| `nipa/xls_survey/Section2All_xls.xlsx` | Published-tables workbook for Section 2: Tables 2.1, 2.2B, 2.3.x, 2.4.x, 2.5.x, 2.6, 2.7B, 2.8.x and 2.10. |
| `nipa/nipa-handbook-chapter-05.pdf`, `nipa/faq-84-...html` | NIPA Handbook ch. 5 on PCE (updated Dec 2024), and BEA's FAQ on the detail beyond 2.4.5U. |
| `release/pi0926.pdf`, `release/personal-income-and-outlays-september-2026.html` | The September 2026 release, used for the headline cross-checks. |
| `distribution/national/summary-file.csv` (+ 2023 and 2024 inequality-metrics workbooks, technical document, read-me, summary of methodological updates) | National distribution of personal income. |
| `distribution/distribution-of-personal-income.html` | BEA's special-topics page as pulled on 2026-11-02. **It is the only place the 2025 nowcast table appears**: a static HTML table, with no downloadable file. |
| `distribution/blog_2026-06-16_...html` | Release blog post introducing IDAT, ISPCEPX and the nowcast. |
| `distribution/ispcepx/ispecpx_table.xlsx` (file name as published), `readme_ISPCEPX.pdf`, `BEA-WP2025-9.pdf` | ISPCEPX, its method note, and the method paper. |
| `distribution/joint_dpi_pce/joint_dist_summary.xlsx`, technical document, read-me | Joint distribution of DPI and PCE (BEA-BLS). |
| `FETCH_FAILURES.csv` | Downloads that failed and are not retried by default. Currently it lists only the FRED file (section 9). |

## 3. `bea_pce_u_long.csv.gz` — Tables 2.4.5U, 2.4.6U, 2.4.4U, 2.4.3U, monthly and annual

The file has 1,091,934 rows. It is gzip-compressed because the uncompressed CSV is 125 MB, and
`pd.read_csv` reads the .gz directly.

| table | freq | rows | lines with data | dates |
|---|---|---|---|---|
| 2.4.5U (current dollars) | A / M | 25,186 / 305,832 | 402 | 1959..2025 / 1959-01..2026-09 |
| 2.4.6U (chained 2017 dollars) | A / M | 7,600 / 94,800 | 400 | 2007..2025 / 2007-01..2026-09 |
| 2.4.4U (price indexes) | A / M | 25,052 / 304,206 | 400 | 1959..2025 / 1959-01..2026-09 |
| 2.4.3U (quantity indexes) | A / M | 25,052 / 304,206 | 400 | 1959..2025 / 1959-01..2026-09 |

**Columns**

- `table` is '2.4.5U', '2.4.6U', '2.4.4U' or '2.4.3U'.
- `freq` is 'M' or 'A'.
- `line` is BEA's line number. It is the key; series codes are not unique per line (see below).
- `series_code` is BEA's code: ...RC for current dollars, ...RX for chained dollars, ...RG for price indexes, ...RA for quantity indexes.
- `label` is BEA's label with the indentation and footnote markers stripped. Numbers in trailing parentheses, such as "(55)", are BEA's cross-references to Table 2.5.5 lines. They are kept here and split out in the lines file.
- `level` is the display indent depth. PCE (line 1) is 0, Goods and Services are 1, and the deepest lines are at **level 8**. BEA prints line 1 indented above Goods at indent 0, so line 1 is forced to level 0.
- `parent_line` is the nearest preceding line one level up. It is set only for the main hierarchy, lines 1-368, and is empty for line 1 and for the addenda. pandas reads it as float, so cast it with `astype('Int64')`.
- `date` is 'YYYY-MM' (monthly) or 'YYYY' (annual).
- `value` is the published value.
- `unit` is one of:
  - 'millions of dollars, SAAR' (monthly) or 'millions of dollars' (annual totals);
  - 'millions of chained 2017 dollars[, SAAR]';
  - 'index 2017=100[, SA]'.
  Monthly dollar values are at seasonally adjusted annual rates, so a month's flow is value/12.
- `sign` is -1 for "Less:" lines, which enter their parent negatively, and +1 otherwise.
- `section` is 'main' for lines 1-368 or 'addenda' for lines 369-402 ("Additional aggregates" and "Market-based PCE").
- `context` is the unnumbered header(s) an addenda line sits under, for example "Services: Of which:".
- `table_id` is BEA's TableId, for example U20405.

A row exists only where BEA publishes a value; the workbook's "....." cells are dropped. Values come from
the flat files. Each value was checked against the matching workbook cell: every cell matches, with no
cell missing on either side and a maximum difference of 0. The comparison covered all eight A/M sheets,
about 1.09 million cells.

**Hierarchy facts (2.4.5U; the layout is identical in all four tables)**

- **Line count.** There are 402 numbered lines. Lines 1-368 form the additive hierarchy and 369-402 are addenda.
- **The top of the tree.**
  - PCE (line 1) = Goods (2) + Services (150).
  - Services = Household consumption expenditures for services (151) + Final consumption expenditures of NPISHs (342).
  - NPISH final consumption (342) = Gross output of nonprofit institutions (343) − Receipts from sales of goods and services by nonprofit institutions (356).
- **"Less:" lines.**
  - 149 Less: Personal remittances in kind to nonresidents.
  - 274 Less: Household insurance normal losses.
  - 338 Less: Expenditures in the United States by nonresidents.
  - 356 Less: Receipts from sales ... by nonprofit institutions.
- **Display parents agree with the register.** For every line, the display parent's series code is one of SeriesRegister's `SeriesCodeParents` for the line's code (0 disagreements).
- **Children sum to parents in 2.4.5U.** With signs applied, every parent equals the sum of its published children to within rounding. This held in all 95,691 monthly and 7,882 annual parent-periods:
  - Largest gap: 3 million $ (line 151 in 1976-07; line 356 in 1995).
  - Largest gap since 2022: 2 million $.
  - No gap beyond the rounding bound of (children + 1)/2 million $.
  - From 2007-01, PCE also equals the signed sum of the 243 current leaf lines (using `sign_to_root`) to within 11 million $.
- **Lines that appear twice with the same series code.** Each pair is the same series counted twice, once added and once subtracted, which nets to zero in PCE:
  - DNPHRC, Nonprofit hospitals' services to households: lines 184 and 359.
  - DNPNRC, Nonprofit nursing homes' services: lines 188 and 360.
  - DRELRC, Religious organizations' services to households: lines 325 and 364.
  - DGIVRC, Foundations ... services to households: lines 326 and 365.
  - In the addenda: DGOERC (113 and 382), DUTLRC (165 and 386), DHLCRC (172 and 387), DTRSRC (190 and 388), DCOMRC (281 and 393), DTEDRC (290 and 394), DPERRC (307 and 396), DCHCRC (316 and 397).
- **Lines that start or stop.**
  - 157 Tenant-occupied stationary homes and 158 Tenant landlord durables run to 2001-12. 159 Tenant-occupied, including landlord durables starts in 2002-01. So line 156 = 157 + 158 up to 2001 and = 159 from 2002.
  - Some detail starts later than its parent, and before that date the parent is the finest published level:
    - 10-11 start in 2002-01.
    - 18-19 start in 1983.
    - 46, 49 and 50 start in 1977.
    - 177, 178, 180, 181, 195, 196, 242-244, 267, 268, 289 and 318-323 start in 1987.
    - 224-225 start in 2007-01.
    - 262, 263, 265 and 266 start in 1997.
    - 285 starts in 1985.
    - 337, 340 and 341 start in 1981.
- **Lines with no price or quantity index.** 2.4.4U and 2.4.3U publish nothing for lines 145 (Net expenditures abroad by U.S. residents) and 333 (Net foreign travel); their code is ZZZZZZ. 2.4.6U has nothing for lines 157-158, because the table starts in 2007.
- **Chained dollars start in 2007.** Chained-dollar detail (2.4.6U) is published only from 2007 (2007-01 monthly). For earlier real detail, use the 2.4.3U quantity indexes, which go back to 1959.

**Chained-dollar detail is not additive (confirmed).**

- **BEA's own note** (on Tables 2.3.6 and 2.8.6): "Because the formula for the chain-type quantity indexes uses weights of more than one period, the corresponding chained-dollar estimates are usually not additive."
- **Gaps in 2.4.6U.**
  - PCE minus (Goods + Services) is −23,085 million chained 2017 $ in 2025 and −22,493 in 2026-09.
  - The largest children-sum gap is −45,925 (Durable goods, 2026-01).
  - Table 2.3.6 prints a "Residual" line (line 25) equal to line 1 minus the sum of its most detailed lines. It is −111,737 in 2025, and the script reproduces it to within 3.
- **What to use instead.** Compute shares and contributions from nominal 2.4.5U values and 2.4.4U prices, not by summing chained dollars.

**Contributions to percent change are not published for the U detail.**

- **Not in the registers or the workbook.** TablesRegister has no U20401, U20402 or U20802. The underlying workbook has no 2.4.1U or 2.4.2U sheet; its sheets are 2.3.4U-2.3.6U and 2.4.3U-2.4.6U only.
- **What BEA does publish.**
  - Contributions by type of product: Table 2.4.2, annual and quarterly only, at the published level of detail.
  - Monthly contributions: Table 2.8.2, by major type of product only.
- **What later steps must do.** Contributions of U lines have to be computed, from 2.4.5U values and the 2.4.4U and 2.4.3U indexes.

**Quality caveat (NIPA Handbook ch. 5, Dec 2024).** "BEA does not include these detailed estimates in the
published tables because their quality is significantly lower than that of the higher-level categories of
which they are a part. In particular, these detailed estimates are more likely to be based on judgmental
trends or on less reliable source data." BEA's FAQ 84 adds that 2.4.5U is the most detailed PCE time
series. More detail exists only in the benchmark input-output years (years ending in 2 and 7).

**Definitions that matter for these questions** (Handbook ch. 5):

- **What PCE covers.** PCE covers purchases by households and by NPISHs. It includes purchases directly financed by government social benefits, such as Medicaid. It includes imputations such as owner-occupied housing and financial services furnished without payment.
- **NPISH final consumption.** NPISH final consumption equals gross output less own-account investment and less sales to households and other sectors.
- **Household consumption for services (line 151)** already includes purchases *from* NPISHs. For example, nonprofit hospitals' sales to households sit in Health care, line 184.
- **Total health care services.** Health care services consumption, including the part of nonprofit health output that households do not pay for, is line 172 + (344 − 357). That part is the health slice of NPISH final consumption. Health goods (lines 66 and 121) and net health insurance (line 275) are separate lines.

## 4. `bea_pce_u_lines.csv` — one row per 2.4.5U line (402 rows)

**Columns**

- `line`, `label`, `level`, `parent_line`, `sign`, `section` and `context` are as in the long file.
- `label_short` is the label without the Table 2.5.5 cross-reference.
- `xref_table_2_5_5` is that cross-reference, for example '55' or 'parts of 31 and 32'.
- `n_children` is the number of child lines.
- `is_leaf` is true for main-hierarchy lines with no children (245 lines).
- `path_lines` is the line path from PCE, for example `1>150>342>356>357>358`.
- `sign_to_root` is the product of signs up to line 1, which is how the line enters PCE. Lines 357-368 enter PCE with −1.
- `code_2_4_5U`, `code_2_4_6U`, `code_2_4_4U` and `code_2_4_3U` are the series codes per table.
- `first_{A,M}_{table}` and `last_{A,M}_{table}` give each line's published date range.

**Key line numbers** (labels as published):

- **Health care.**
  - The services block: 172 Health care; 173 Outpatient services; 174 Physician services (44); 175 Dental services (45); 176 Paramedical services (46); 177 Home health care; 178 Medical laboratories; 179 Other professional medical services; 180 Specialty outpatient care facilities and health and allied services; 181 All other professional medical services; 182 Hospital and nursing home services; 183 Hospitals (51); 184 Nonprofit hospitals' services to households; 185 Proprietary hospitals; 186 Government hospitals; 187 Nursing homes (52); 188 Nonprofit nursing homes' services to households; 189 Proprietary and government nursing homes.
  - Health goods: 66 Therapeutic appliances and equipment (42); 67 Therapeutic medical equipment; 68 Corrective eyeglasses and contact lenses; 121 Pharmaceutical and other medical products (40 and 41); 122 Pharmaceutical products; 123 Prescription drugs; 124 Nonprescription drugs; 125 Other medical products.
  - Health insurance: 275 Net health insurance (112); 276 Medical care and hospitalization; 277 Income loss; 278 Workers' compensation.
  - Foreign: 340 Medical expenditures of foreigners, which sits under 338 "Less:".
  - NPISH health: 344 Health, gross output; 345 Outpatient services, gross output; 346 Nonprofit hospitals, gross output; 347 Nonprofit nursing homes, gross output; 357 Health services to households; 358 Outpatient services to households; 359 Nonprofit hospitals services to households; 360 Nonprofit nursing homes services to households.
  - Addenda: 387 Market-based PCE health care.
- **Social services and religious activities.** 315 Social services and religious activities (120); 316 Child care; 317 Social assistance; 318 Homes for the elderly; 319 Residential mental health and substance abuse; 320 Individual and family services; 321 Vocational rehabilitation services; 322 Community food and housing / emergency / other relief services; 323 Other social assistance, not elsewere classified (BEA's spelling); 324 Social advocacy and civic and social organizations; 325 Religious organizations' services to households; 326 Foundations and grantmaking and giving services to households. NPISH counterparts: 350 Social services, gross output; 363 Social services to households.
- **Owner-occupied housing.** 160 Imputed rental of owner-occupied nonfarm housing (21), with children 161 Owner-occupied mobile homes and 162 Owner-occupied stationary homes.
- **Financial services furnished without payment.** 254 Financial services furnished without payment (107), with children 255 Commercial banks, 256 Other depository institutions and regulated investment companies, and 257 Pension funds.
- **NPISHs.**
  - 342 Final consumption expenditures of nonprofit institutions serving households (NPISHs) (132).
  - 343 Gross output of nonprofit institutions (133), with lines 344-355 beneath it.
  - 356 Less: Receipts from sales of goods and services by nonprofit institutions (134), with lines 357-368 beneath it.
- **Net foreign travel.**
  - 333 Net foreign travel.
  - 334 Foreign travel by U.S. residents (129), with lines 335-337.
  - 338 Less: Expenditures in the United States by nonresidents (130), with lines 339-341.
  - Also, under goods: 145 Net expenditures abroad by U.S. residents (131), with lines 146-149.
- **Energy.**
  - 113 Gasoline and other energy goods.
  - 114 Motor vehicle fuels, lubricants, and fluids (59), with 115 Gasoline and other motor fuel and 116 Lubricants and fluids.
  - 117 Fuel oil and other fuels (29), with 118 Fuel oil and 119 Other fuels.
  - Addenda: 370 PCE food and energy, 371 PCE energy goods and services, 382 Market-based PCE gasoline and other energy goods.
- **Motor vehicles.**
  - 4 Motor vehicles and parts.
  - New vehicles: 5 New motor vehicles (55); 6 New autos (7 domestic, 8 foreign); 9 New light trucks (10 domestic, 11 foreign).
  - Used vehicles: 12 Net purchases of used motor vehicles (56); 13 Used autos (14 net transactions, 15 margin, 16 employee reimbursement); 17 Used light trucks (18 net transactions, 19 margin).
  - Parts: 20 Motor vehicle parts and accessories (58), with 21 Tires and 22 Accessories and parts.

## 5. `bea_pce_major_long.csv` — published Tables 2.3.5 and 2.3.6 (annual) and 2.8.5 and 2.8.6 (monthly)

The file has 35,317 rows and the same columns as the long U file.

| Table | Lines | Dates |
|---|---|---|
| 2.3.5 | 31 | 1929..2025 |
| 2.3.6 | 32, including line 25 'Residual', whose `section` is 'residual' | 2007..2025 |
| 2.8.5 | 31 | 1959-01..2026-09 |
| 2.8.6 | 31 | 2007-01..2026-09 |

Values for shared series codes are identical to the U tables in every period: 22,905 cells for 2.8.5 against
2.4.5U, and 6,873 for 2.8.6 against 2.4.6U. The published-only addenda series are LA001176/LB001176 (PCE
excluding food, energy, and housing), LA001260/LB001260 (PCE services excluding energy and housing) and
D236RX (Residual). Line 1 is "Personal consumption expenditures (PCE)", and line 22 is NPISH final
consumption.

## 6. `bea_pi_long.csv` — Table 2.6 (monthly, 1959-01..2026-09) and Table 2.1 (annual, 1929..2025)

The file has 38,856 rows, 43 lines per table, and the same columns as above.

**Read `table` as a string.** Use `pd.read_csv(..., dtype={'table': str})`; otherwise pandas parses '2.6' and
'2.1' as the floats 2.6 and 2.1. `freq` also identifies the table: M is 2.6 and A is 2.1.

**Lines**

- 1 Personal income.
- 2-8 Compensation of employees.
- 9-11 Proprietors' income.
- 12 Rental income.
- 13-15 Receipts on assets.
- 16 Personal current transfer receipts:
  - 17 Government social benefits to persons;
  - 18 Social security;
  - 19 Medicare;
  - 20 Medicaid;
  - 21 Unemployment insurance;
  - 22 Veterans' benefits;
  - 23 Other;
  - 24 Other current transfer receipts, from business (net).
- 25 Less: Contributions for government social insurance, domestic.
- 26 Less: Personal current taxes.
- 27 Equals: Disposable personal income.
- 28 Less: Personal outlays, made up of 29 PCE, 30 Personal interest payments, and 31-33 Personal current transfer payments.
- 34 Equals: Personal saving.
- 35 Saving rate (percent of DPI).
- Addenda:
  - 36 Personal income excluding current transfer receipts, millions of chained 2017 $ (series W875RX; FRED's W875RX1 is this series in billions);
  - 37 Real DPI (A067RX);
  - 38-39 Per-capita DPI, current and chained dollars;
  - 40 Population (thousands);
  - 41-43 Percent changes. Monthly percent changes are at monthly rates and are not annualized.

**Hierarchy, units and identities**

- **Parents.** PI's components have `parent_line` = 1. Lines 26, 27, 28 and 34 are top-level identity lines with no parent. Line 35 and the addenda have no parent, because they are a ratio and memo items.
- **Units.** Units are per line: millions of $, SAAR; percent; chained 2017 $; dollars per person; and thousands of persons.
- **Checks that hold.**
  - Children sum to parents within rounding in every month (largest gap: 2 million $).
  - The identities DPI = PI − taxes, saving = DPI − outlays, and saving rate = saving/DPI hold to 1 million $ and 0.0 pp.
- **Early Table 2.1 years.** In 1929-1932 and 1943-1945, line 17 exceeds the sum of its published children, by up to 492 million $ in 1932. Some children (Medicare, Medicaid, Other, ...) are unpublished ("....") in those years. These are pre-1959 annual figures, flagged in `bea_checks.csv`.

**Personal income excluding current transfer receipts**

- **Nominal.** There is no nominal line in 2.6 or 2.1. Compute it as line 1 − line 16.
- **Real.** Line 36 equals (line 1 − line 16) deflated by the PCE implicit price deflator, DPCERC/DPCERX. This is verified to a relative difference of 1.8e-7 over 2007-01..2026-09 and 2.2e-6 annually over 1959-2025, which confirms BEA's footnote 5.
- **Register label.** SeriesRegister labels W875RX "Billions of chained (2017) dollars", but its scale (−6) and the workbook show millions. The values are millions.

## 7. Distribution files

**`bea_dpi_distribution.csv`** (9,035 rows; years 2000-2025)

Columns:

- `year`.
- `status`: 'final' (2000-2023), 'provisional' (2024) or 'nowcast_experimental' (2025).
- `ranking`: 'equivalized_pi' (households ranked by equivalized personal income), 'equivalized_dpi', 'none' (aggregate totals and observation counts) or 'not_stated' (the nowcast; the page does not say).
- `income_concept`: the series distributed. 'Personal income', 'Disposable personal income', 'Household income', and the components: compensation, proprietors' income, rental income, receipts on assets (interest, dividends), household current transfer receipts (government social benefits; from business; from nonprofits), contributions for government social insurance, and taxes.
- `nipa_t29_line`: the series' line in NIPA Table 2.9, "Personal Income and Its Disposition by Households and by NPISHs".
- `group`: D01..D10 deciles, Q1..Q5 quintiles, B05 (bottom 5%), T05 and T01 (top 5% and top 1%), or ALL.
- `pct_lo`, `pct_hi`: the percentile bounds of the group.
- `metric`:
  - share;
  - gini_equivalized;
  - ratio_p50_p10_equivalized, ratio_p80_p20_equivalized, ratio_p90_p10_equivalized, ratio_p90_p50_equivalized;
  - mean_nominal, mean_2017usd, median_nominal, median_2017usd;
  - total;
  - obs_unweighted, obs_weighted;
  - growth_nominal_2024_2025.
- `value`; `value_lo` and `value_hi` (filled only for interval estimates); `unit`; `source`; `quantile_or_metric_raw`, the string exactly as published.

Definitions:

- **Ranking and equivalization.** Households (CPS units) are ranked by equivalized income, meaning household income divided by the square root of the number of household members.
- **Shares and dollar metrics** are shares of total, unequivalized income: a group's income divided by the income of all households, as a fraction.
- **Gini and percentile ratios** use equivalized income.
- **Means and medians** are per household, in current dollars or 2017 dollars. BEA's documentation does not name the deflator.
- **Totals** are billions of current dollars, at the June 2026 NIPA vintage (see section 1).
- **2024 top shares** are published as intervals. For personal income, ranked by equivalized PI, the top 1% share is [0.159-0.165] and the top 5% share is [0.297-0.303]. The point value is left empty; use `value_lo` and `value_hi`.
- **2025 nowcast rows** come from the HTML table on BEA's page: quintile shares of PI (published in percent, stored here as fractions) and 2024-2025 nominal growth in percent. The quintile shares are Q1 5.2, Q2 9.6, Q3 13.4, Q4 19.1 and Q5 52.7. The growth rates are 4.1, 5.8, 5.0, 5.4 and 4.6. The page does not say which ranking the nowcast uses. Its "2024 (published)" column equals the summary-file 2024 PI quintile shares (5.3/9.5/13.4/19.0/52.8), which are identical under both rankings. Combining the 2024 shares with each quintile's growth implies aggregate PI growth of 4.89% and 2025 shares within rounding of the published ones.

Checks:

- Decile and quintile shares sum to 1 within 0.003.
- Summary-file values equal the 2023 and 2024 inequality-metrics workbooks: 300/300 Table 1 decile shares and 30/30 Table 2 metrics in each year.
- NIPA Table 2.10 (published in percent to one decimal) equals the summary-file decile shares for 2000-2024 when each concept is ranked by its own equivalized income: 250/250 cells each for PI and DPI.

**`bea_pce_price_by_income_decile.csv`** (425 rows; 2000-2024)

Columns:

- `year`.
- `group`: D01..D10, Q1..Q5, or ALL (the published aggregate PCE price index).
- `grouping`: decile or quintile of equivalized DPI.
- `pct_lo`, `pct_hi`.
- `index_base`: '2000=100' for ISPCEPX and the rebased aggregate, or '2017=100' for "Published PCE PI".
- `value`.
- `imputed_weights`: True for the 2024 group indexes.
- `source_column`.

Definition (read-me): Fisher chain-linked price indexes per decile or quintile of equivalized DPI. Each uses its own group's expenditure weights over about 150 detailed PCE categories. The weights are scaled to Table 2.4.5U, and the category prices are from 2.4.4U, so groups differ only through expenditure composition. Quintile indexes are computed from the combined shares, not by averaging deciles. For 2024, each group's 2023 share of each category was applied to the 2024 category totals. The method paper is BEA WP 2025-9, Gindelsky and Martin. Checks: every index is 100 in 2000, and the rebased aggregate column is reproduced. Cumulative inflation, 2019-2024:

| Decile (equivalized DPI) | Cumulative inflation, 2019-2024 |
|---|---|
| D01 | 19.6% |
| D02 | 19.5% |
| D03 | 19.4% |
| D04 | 19.3% |
| D05 | 19.2% |
| D06 | 19.1% |
| D07 | 19.1% |
| D08 | 19.2% |
| D09 | 19.2% |
| D10 | 20.4% |
| Aggregate | 19.5% |

**`bea_joint_dpi_pce_by_decile.csv`** (1,632 rows; 2000-2023)

Columns:

- `year`.
- `ranking`: always equivalized_dpi.
- `series`: Disposable Personal Income, Personal Consumption Expenditures, Personal Saving, or Personal saving rate.
- `nipa_t21_line`: 27, 29 or 34.
- `group`, `pct_lo`, `pct_hi`.
- `metric`: share, total, mean_nominal, mean_2017usd, median_nominal, median_2017usd, or saving_rate.
- `value`, `unit`, `source_sheet`, `quantile_or_metric_raw`.

Definitions and checks:

- **Shares** are fractions of the NIPA Table 2.1 total of the series. Saving shares are negative for low deciles and exceed 1 at the top.
- **The `saving_rate`** is the group's saving divided by the group's DPI, as a fraction.
- **The read-me's description of the saving rate is imprecise.** It says "share of total personal saving divided by share of total DPI", which omits the ratio of the totals. The published values match saving share × total saving / (DPI share × total DPI) to within the rounding of the 3-decimal shares: median deviation 0.0006, maximum 0.042, in the bottom deciles.
- **Construction.** BEA's CPS-based DPI distribution is matched to BLS CE-based PCE. This is research-stage data.

**`bea_joint_dpi_pce_joint_shares.csv`** (3,456 rows; 2000-2023)

Columns: `year`, `dpi_group`, `pce_group` (D01..D10, T05, T01), `share_households`, `share_dpi`, `share_pce`,
and the raw group labels. Each value is the share of all households, DPI or PCE falling in the cell (income
group × consumption group). T01 and T05 overlap D10, so sum only over the D×D grid; it sums to 1 within 0.007.

The BEA page says these statistics are "provided for 2004-2023", but the workbook and its read-me cover 2000-2023.

## 8. Cross-checks against the release (all pass; see `bea_checks.csv`)

The September 2026 release's numbers are reproduced from the tidy data:

- **Changes in September:**
  - PI +$54.5bn (0.2%).
  - DPI +$52.7bn (0.2%).
  - PCE +$113.1bn (0.5%).
  - Outlays +$113.0bn.
  - Goods +$35.1bn and services +$78.1bn.
  - Real PCE +$2.6bn.
- **Levels:** personal saving $911.1bn and a saving rate of 3.8%.
- **PCE price index:** +0.5% m/m (core +0.3%) and 3.6% y/y (core 3.1%).
- **The release's August/September table:** PI 0.3/0.2, DPI 0.3/0.2, real DPI 0.0/−0.3, PCE 0.9/0.5, real PCE 0.5/0.0, PCE prices 0.3/0.5, core 0.3/0.3.
- **All 16 bars of the "Changes in Monthly Consumer Spending" chart**, from gasoline and other energy goods (+45.7) to motor vehicles and parts (−14.0).

## 9. Problems and open items

- **FRED cross-check not run.** `https://fred.stlouisfed.org/graph/fredgraph.csv?id=W875RX1` failed through `common.http_get` on 2026-11-02 after 4 tries. The error was `ProxyError('Unable to connect to proxy', RemoteDisconnected('Remote end closed connection without response'))`. The connection to fred.stlouisfed.org was closed during the CONNECT through this session's egress proxy, so FRED never answered. Per the stop-and-report rule, it is not retried by default and no substitute was used. An internal check stands in: line 36 is reproduced from lines 1 and 16 and the PCE deflator.
- **IDAT not used.** The Income Distribution Analysis Tool (https://tools.bea.gov/pidv/) is a JavaScript app; it was not used or scraped. The 2025 nowcast exists only as the HTML table on the special-topics page.
- **No quarterly U data.** Quarterly U tables are in the raw workbook and flat files but were not tidied.
- **Vintage mismatch.** The distributional files (June 2026 and earlier) are on an earlier NIPA vintage than the October 2026 NIPA files (section 1). Mixing them, for example applying 2024 shares to current totals, mixes vintages.
