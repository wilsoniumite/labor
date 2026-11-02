# Statistics Finland (StatFin) and Eurostat: tidy files for the Finnish side of the consumption thread

Built by `consumption/code/acquire_fin.py` from the raw files in `consumption/data/raw/statfin/` (56 files) and
`consumption/data/raw/eurostat/` (13 files). Every raw file is listed in its folder's `MANIFEST.csv` with URL,
pull date (2026-11-02), sha256, bytes and use. For StatFin data tables the manifest's `what_it_is` field also holds
the exact POST body sent. Run from the repo root: `venv/bin/python -I consumption/code/acquire_fin.py`. Vendored
files are never re-downloaded, so a rerun is offline (about 4 s) and rebuilds every file below byte for byte
(checked: two clean rebuilds gave identical sha256 for all 10 outputs). The script stops with an error if any
`consistency` check in `fi_checks.csv` fails.

Publishers: **Statistics Finland** (StatFin PxWeb API `https://pxdata.stat.fi/PxWeb/api/v1/en/StatFin/`, and
stat.fi documentation and release pages) and **Eurostat** (dissemination API
`https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/`). Requests carried `common.py`'s plain
research User-Agent; no request was blocked. Table metadata came by GET on the table URL; data came by POST
queries returning JSON-stat 2.0, which keeps codes, labels, units, notes and the table's `updated` stamp. Every
variable is listed explicitly in each query, because PxWeb collapses an omitted variable to its total. The
script pauses 1.6 s after each download (StatFin API limit: 40 calls per 60 s, `docs/pxweb_api_config.json`). stat.fi's
`robots.txt` excludes the Finnish documentation path `/tilasto/dokumentaatio/` and the site search, so only the
English documentation paths were fetched.

## Raw inventory

| Folder | Files | What |
|---|---|---|
| `statfin/data/` | `<db>_<table>.json` (13) | JSON-stat2 data: `ktutk_14pg`, `ktutk_14qa`, `tjt_12ew`, `tjt_152w`, `tjt_128c`, `tjt_14ya`, `vtutk_151u`, `vtutk_151z`, `rtp_11zx`, `kihi_11jc`, `ashi_12de`, `ashi_13mw`, `ntp_15ag` |
| `statfin/meta/` | `<db>_<table>.meta.json` (13) | GET metadata (variables, value codes and labels) for the same tables |
| `statfin/listing/` | `StatFin_<db>.json` (8) | database listings: root (135 databases), `ktutk` (16 tables), `tjt` (25), `vtutk` (11), `rtp` (5), `kihi` (13), `ashi` (15), `ntp` (19) |
| `statfin/search/` | `StatFin_query_<term>.json` (10) | StatFin table-search results for land, plot, plots, property tax, real estate tax, taxable value, building land, land area, forest, dwelling stock (the record of the land search, item 4) |
| `statfin/docs/` | 12 | SIMS documentation pages for `ktutk`, `tjt`, `vtutk`, `rtp` (English); HBS 2022 final release (2024-04-11) and preliminary release (2023-12-28); HBS table-change notice (2024-04-11); wealth-survey 2023 release (2025-03-12); two Finnish-language Statistics Finland articles giving the HBS income-group method (2008, 2022); `robots.txt`; PxWeb API config |
| `eurostat/data/` | `nama_10_co3_p3_<geo>.json`, `nama_10_cp18_<geo>.json` (10), `nama_10_nfa_bs_FI.json` | geo = FI, SE, DK, DE, EU27_2020; units CP_MEUR, CP_MNAC, CLV20_MEUR, CLV20_MNAC, PD20_EUR, PD20_NAC; 2015 onward; all COICOP codes. Plus Finland's non-financial balance sheets (all sectors and assets reported, CP_MEUR, 2015 onward) for the land search |
| `eurostat/docs/` | `nama10_esms.htm`, `eurostat_toc_en.txt` | ESMS metadata for annual national accounts (linked from both datasets); the Eurostat catalogue (dataset codes, last update, data start/end) |

StatFin tables vendored (cells = full query size, including empty cells):

| Table | Content | Coverage vendored | Cells | Table updated |
|---|---|---|---|---|
| ktutk 14pg | HBS: household consumption expenditure by income quintile, COICOP2018 | 2012, 2016, 2022; 510 codes; total + 5 quintiles; 10 measures | 91,800 | 2024-04-11 |
| ktutk 14qa | HBS: background information by income quintile | 2012, 2016, 2022; 6 measures | 108 | 2024-04-11 |
| tjt 12ew | households and persons by income decile and household's stage in life (sample data) | 1989-2024; 13 stages; 4 measures | 20,592 | 2026-02-26 |
| tjt 152w | housing costs and indicators by income quintile (sample data) | 2002-2024; 26 measures | 3,588 | 2026-02-26 |
| tjt 128c | income and income structure of household-dwelling units by income decile (register data) | 1995-2024; 39 measures | 12,870 | 2025-12-16 |
| tjt 14ya | persons by income decile, age group and origin (register data) | 1995-2024; ages 0-17, 18-64, 65-; 7 measures | 46,200 | 2025-12-16 |
| vtutk 151u | wealth survey: assets, liabilities and income of households by income decile | waves 1987, 1988, 1994, 1998, 2004, 2009, 2013, 2016, 2019, 2023; 29 items; 13 measures | 41,470 | 2025-03-12 |
| vtutk 151z | wealth survey, same items, by housing tenure | same waves; 4 tenure groups | 15,080 | 2025-03-12 |
| rtp 11zx | financial accounts: non-financial assets by sector and instrument | 1995-2025; 8 sectors; 10 instruments; stock and change | 4,960 | 2026-09-30 |
| kihi 11jc | price index and prices per m2 of single-family house plots, yearly | 2015-2025; 11 regions; 10 measures | 1,210 | 2026-02-24 |
| ashi 12de | prices per m2 of new dwellings in housing companies by form of ownership of plot | 2015-2025; 15 regions | 11,880 | 2026-02-19 |
| ashi 13mw | prices per m2 of old dwellings in housing companies by form of ownership of plot | 2009-2025; 5 aggregate regions of 87 (whole country, Greater Helsinki, country excl. Greater Helsinki, major cities, country excl. major cities) | 4,590 | 2026-05-19 |
| ntp 15ag | annual national accounts: household final consumption expenditure, COICOP2018 | 2015-2025 (2024, 2025 preliminary); 469 codes; 4 transactions; durability total; 3 of 8 measures (current prices, previous-year prices, volume reference 2025) | 61,908 | 2026-09-18 |

## The income groupings differ: read this before combining tables

| Grouping (column `grouping` in `fi_hh_composition.csv`) | Tables | Unit ranked and group size | Ranking variable (as documented) |
|---|---|---|---|
| `hbs_household_quintile` | ktutk 14pg, 14qa | **households**: each quintile holds 20% of households (582,714 to 584,445 of 2,919,000 in 2022; checked) | **Not stated** in the 2022 table notes, the HBS documentation or the 2022 releases. A Statistics Finland article on the HBS (2008, `docs/article_2008-03-12_kulutuserot_fi.html`) describes HBS income groups as households ranked by household disposable income divided by consumption units, cut into equal-size groups of households. A 2022 Tieto&trendit article (`docs/tietotrendit_...`) says its HBS income fifths hold equal numbers of households ranked by disposable income, without mentioning units. The HBS income concept is register-based disposable income, which the documentation says differs from the income-distribution concept. Treat equivalised household ranking as likely but unconfirmed for 2022. |
| `tjt_sample_person_decile` | tjt 12ew | **persons**: 10% of persons each (checked) | Table note: "Decile groups have been formed among persons according to disposable income per consumption unit"; household's disposable cash income excl. capital gains; Eurostat (OECD-modified) scale; household population, sample data (the SILC-based income distribution statistics). |
| `tjt_sample_person_quintile` | tjt 152w | **persons**: 20% of persons each (checked), although the code list is the HBS one | Household's disposable money income (excl. sales profits) per consumption unit; sample data. |
| `tjt_register_person_decile` | tjt 128c, 14ya | **persons**: 544,341 to 544,348 per decile in 2022 (checked) | Register-based total data. The unit is the household-dwelling unit (everyone living at one address), not the household. Ranked by disposable money income incl. sales profits per consumption unit. |
| `vtutk_household_decile` | vtutk 151u | **households**: 10% of households each (294,800 to 295,400 of 2,950,000 in 2023; checked) | **Not stated** in the table notes or the documentation. The wealth survey runs on the income-distribution sample, but its deciles are household-weighted, unlike the tjt person deciles. |

So the tjt deciles do **not** match the HBS quintiles. They are person-weighted, use a different income concept and
come from a different sample, and pairing tjt deciles does not give HBS quintiles. The wealth-survey deciles are
household-weighted like the HBS quintiles, so pairing them (D1+D2, ..., D9+D10) gives household quintiles. That is
consistent in weighting with the HBS, though the income concept and sample may still differ. Totals agree where
they should: HBS 2022 households = tjt 12ew 2022 households = 2,919,000 (Statistics Finland has estimated total
households from registers since 2021).

## Tidy files

All plain CSV, UTF-8, header row, `\n` line ends; numbers up to 10 significant digits; empty field = missing.
None exceeds 20 MB, so none is gzipped.

| File | Rows | Content |
|---|---|---|
| `fi_hbs2022_long.csv` | 18,360 | HBS 2022, every COICOP2018 code (510) x total and quintiles x 6 measures |
| `fi_hh_composition.csv` | 2,319 | households, persons, consumption units, ages, by income group, from every table that has them |
| `fi_wealth_2023_deciles.csv` | 1,914 | wealth survey 2023 by income decile, 29 balance-sheet items x 6 measures |
| `fi_wealth_2023_tenure.csv` | 696 | the same by housing tenure |
| `eurostat_coicop_long.csv` | 14,386 | nama_10_co3_p3 (COICOP 1999), FI SE DK DE EU27_2020, 2015 onward |
| `eurostat_coicop2018_long.csv` | 20,830 | nama_10_cp18 (COICOP 2018, the current dataset), same geos and units |
| `fi_na_hfce_coicop2018_long.csv` | 15,537 | Finnish national accounts household consumption by COICOP2018, 2015-2025 |
| `fi_nonfin_assets_long.csv` | 4,960 | non-financial assets incl. land, by sector, 1995-2025 |
| `fi_land_indicators_long.csv` | 6,791 | plot prices and dwelling prices by plot ownership |
| `fi_checks.csv` | 165 | every verification number (see "Verification") |

### `fi_hbs2022_long.csv` (ktutk 14pg, 2022)

| Column | Meaning |
|---|---|
| `coicop_code` | StatFin code: `0` total; `01`-`13` COICOP2018 divisions; 3/4/5 digits = group/class/subclass (`0111` is 01.1.1); `77` Total consumption abroad; `99` Items outside consumption expenditure |
| `label` | label without the dotted code and the durability marker |
| `level` | 0 total, 1 division (and `77`, `99`), 2 group, 3 class, 4 subclass. Counts: 1, 15, 52, 145, 297 |
| `parent_code` | code[:-1] for 3-5 digits; `0` for `01`-`13` and `77`; empty for `0` and `99` |
| `group` | `total`, `q1` (lowest-income 20%) ... `q5` (highest) |
| `measure` | `per_household_year`, `per_cu_year`, `per_household_month`, `per_cu_month` (EUR, current prices); `share_household_pct`, `share_cu_pct` (published shares of the group's total, one decimal) |
| `value`, `unit` | number and unit text |
| `status` | publisher symbol when the cell is empty: `.` missing, `..` not applicable, `...` confidential, `.....` not asked. 1,960 rows carry one (373 per euro measure, 234 per share measure); 116 codes have at least one empty per-CU cell (`...` 78 codes, `.....` 30, `.` 8) |
| `durability` | `ND`, `SD`, `D`, `S` from the label marker (empty for 77 codes without one) |
| `is_leaf`, `in_total` | no children (299 codes); counted in total `0` (false only for `99`) |
| `measure_code`, `label_published` | PxWeb contents code; label exactly as published |

**Hierarchy (checked).** Total `0` = divisions 01-13 **plus `77` Total consumption abroad**, which is a separate
top-level item and is not spread over the divisions (EUR 553 per consumption unit per year, 2.0% of the total;
Q5 3.0%). `99` Items outside consumption expenditure (EUR 104 per CU) is outside the total (table note: "Total
(group 0) does not include items beyond consumption expenditure"); its shares are empty. Division `04` includes a
national item, **`04.6` Owner-occupied housing / `04.6.3` Interest on housing loans** (EUR 219 per CU, 0.8% of the
total; 0.3% in Q1 and 1.0% in Q5). Interest on housing loans is therefore inside "consumption expenditure" here.
It is not in COICOP 2018 and not in the national accounts, and it is not VAT-able. Every parent equals the sum of its children within
whole-euro rounding (max abs difference EUR 3 over 942 complete parent-child sets per euro measure; 324 sets per
measure have a suppressed child and cannot be summed). Published shares of `0` are exactly 100; shares of 01-13 +
77 sum to 100 within 0.2.

**Measures and conventions.** In 2022 the "at 2022 prices" measures equal current prices cell for cell (checked),
so they are omitted here; they remain in the raw file with 2012 and 2016, which the tidy file leaves out. Monthly =
yearly / 12, rounded to whole euros (|12 x monthly - yearly| <= EUR 6, checked). Consumption units are the
OECD-modified scale (first adult 1, others aged 14+ 0.5, children 0-13 0.3). **Per-CU figures are not per-household
figures divided by the mean consumption units of 14qa.** The ratio per-household / per-CU total is 1.404 (total),
1.167, 1.351, 1.413, 1.464, 1.473 (Q1-Q5), against 14qa mean CUs of 1.39, 1.18, 1.36, 1.43, 1.47, 1.50. Per-CU
values look like means of household-level ratios, but the method is not documented. Budget shares therefore
differ by basis: Q1 actual rentals are 27.3% per household and 29.0% per CU.

**Publisher notes carried in the table (2022 data collection changes):** clothing and footwear (03) now
collected by interview and much higher than in earlier years; transport (07, especially 07.2.3 maintenance and
repair) lower because of a method change; insurance and financial services (12) higher because financial-service
fees (12.2) were asked more fully under COICOP2018; education (10) excludes Åland's early-childhood fees; sewage
(04.4.3) split from water (04.4.1). Total consumption excludes goods and services received from others (from
2022), repayments of loans, direct taxes and investment. It includes imputed rent of owner-occupiers (gross rent
principle) and own production. Since 2022 the reference person is the member with the highest income (register).
Sample: 8,453 net sample, 3,138 responding households; population 2.919 million households (documentation).
The institutional population is excluded. A few labels are truncated by the publisher (e.g. `01124` ends "...in
brine or sm").

**Vintage.** Final data, table updated 2024-04-11. The preliminary release (2023-12-28) gave EUR 27,800 per CU
and EUR 39,000 per household; the final figures are EUR 28,354 and EUR 39,808.

### `fi_hh_composition.csv`

Columns: `source_table`, `year`, `grouping` (see the table above), `group` (`total`, `q1`-`q5`, `d01`-`d10`),
`subgroup` (`all`; `stage_<code>` for 12ew stages in life; `age_0_17`, `age_18_64`, `age_65plus`, `age_18plus`
for 14ya), `measure`, `value`, `unit`, `derived` (true = computed here, not published), `bound_low`/`bound_high`
(for derived rows: range implied by the publisher's rounding), `measure_label` (publisher label), `subgroup_label`,
`note`.

| Source | Years | Measures |
|---|---|---|
| ktutk 14qa (HBS quintiles) | 2022 | `households_in_sample`, `households`, `avg_household_size` and `avg_consumption_units` (means, 2 decimals), `disposable_income_per_household` (EUR, nominal). Derived: `persons` = households x mean size, `consumption_units` = households x mean CUs, and an age split (below) |
| tjt 12ew (sample person deciles) | 2022-2024 | `households`, `persons`, `share_of_decile_households_pct` (publisher label "% of population in the income decile group", which is in fact the stage's share of the decile's households; checked), `share_of_stage_households_pct` ("% of households in the population group" = the decile's share of the stage's households; checked); by stage in life: 1 one-person (1.1 under 35, 1.2 35-64, 1.3 over 64), 2 childless couples (2.1-2.3 likewise), 3 families with children (3.1 couples with children, 3.2 single parents), 4 other households |
| tjt 152w (sample person quintiles) | 2022-2024 | `households`, `persons`, `avg_household_size` (1 decimal only), `floor_area_per_household`, `disp_money_income_per_cu_mean` / `_median` (prices of the latest statistical year) |
| tjt 128c (register person deciles) | 2022-2024 | `household_dwelling_units`, `persons`, `avg_household_size`, `avg_consumption_units` (2 decimals), `disp_money_income_per_cu_mean`/`_median`, `disp_money_income_per_unit_mean` (latest-year values) |
| tjt 14ya (register person deciles) | 2022-2024 | `persons` by age group 0-17, 18-64, 65+ and all (origin total); derived `age_18plus` = 18-64 + 65+ |
| vtutk 151u (wealth household deciles) | 2023 | `households`, `avg_household_size`, `households_in_sample` (identical for every asset item; checked) |

**Adults and children per group: what exists.**
- No table gives adults and children per **HBS quintile**. 14qa gives households, mean persons and mean
  OECD-modified consumption units. Because the scale is linear, the means imply persons aged 14+ per household,
  `a = (CU - 0.5 - 0.3 n) / 0.2`, and children aged 0-13, `c = n - a`. These are rows `avg_persons_14plus`,
  `avg_children_under14`, `persons_14plus`, `children_under14` (`derived` = true). The split is at age **14**, not
  18, and rounding of the published means gives +-0.033 (14+) and +-0.038 (under 14) per household. Example 2022:
  total 1.63 aged 14+ and 0.25 under 14 per household; Q1 1.255 and 0.175, i.e. 102,000 children under 14 in Q1
  households (rounding range 80,000-124,000).
- **Register person deciles** (14ya): exact counts aged 0-17 and 18+ per decile, e.g. 2022 D1 84,136 children and
  460,212 adults; D10 76,502 and 467,839. These are deciles of persons in household-dwelling units, not of
  households.
- **Sample person deciles** (12ew, the table the post cites): households and persons by stage in life only.
  Persons per household are exactly 1 for one-person households and 2 for childless couples, in every decile and
  year (checked). Families with children (3.1: 4.07, 3.2: 2.72 persons per household in 2022) and other households (2.72)
  need an assumption to split adults from children. The stage classification is "based on type of household, age
  of reference person and age of children"; the age limit for children is not stated in the table or documentation.
- **Housing tenure by income group**: no ktutk or tjt table crosses tenure with income quintile or decile. The
  nearest published items are the wealth survey's participation rate for the household main residence by income
  decile (`fi_wealth_2023_deciles.csv`, component `main_residence`, measure `participation_rate_pct`: 27% in D1,
  rising to 92% in D10, 64% overall, 2023), and the HBS split of rent into 04.1 actual rentals and 04.2 imputed
  rentals by quintile.

### `fi_wealth_2023_deciles.csv` and `fi_wealth_2023_tenure.csv` (vtutk 151u, 151z; 2023 wave)

Columns: `component` (slug), `decile` (`total`, `d01`-`d10`) or `tenure` (`all`, `outright_owner`,
`owner_with_mortgage`, `renter_or_other`), `measure`, `value`, `unit`, `status`, `component_code` (publisher code),
`item_no` (number in the publisher's label), `component_label`.

Measures: `mean` (EUR per household, **mean over all households in the group**; table note), `median`, `p25`,
`p75` (EUR, **conditional on holding the item**; table note), `households_holding`, `participation_rate_pct`. The
"real terms" measures equal nominal in 2023 (checked) and are omitted. Households per decile are in
`fi_hh_composition.csv`.

Components, with the identities checked on means (all hold within EUR 1):
- `net_wealth` = `total_assets` - `debt_total`; `total_assets` = `real_wealth` + `financial_assets`.
- `real_wealth` (1-3) = `housing_wealth` (1) + `vehicles` (2) + `forest_farmland_business` (3).
- `housing_wealth` (1) = `main_residence` (1.1) + `free_time_residences` (1.2, leisure homes) +
  `other_residential_property` (1.3, other dwellings).
- `financial_assets` (4-9) = `deposits` (4) + `listed_shares_and_mutual_funds` (5 = `mutual_funds` 5.1 +
  `listed_shares` 5.2) + `unlisted_shares` (6) + `private_pension_wealth` (7) + `savings_investment_insurance` (8)
  + `other_financial_assets` (9).
- `debt_total` (10) = `housing_loans` (10.1) + `consumer_and_other_loans` (10.2).
- `main_residence_net_value` = `main_residence` - `housing_loans`.
- Variants: `*_excl_insurance_crypto` leave out item 8 and crypto-assets. Crypto has no line of its own and
  averages EUR 743 per household (implied). `*_narrow` leave out forests, farmland, business wealth, item 8 and
  crypto. `real_wealth_narrow` = 1 + 2. `disposable_income` is the household's annual disposable (money) income.

**Not published separately in 151u:** forest (inside item 3, together with farmland and business wealth), bonds
(the survey covers "bonds, derivatives" but the table has no line for them; presumably inside item 9 other
financial assets, which is not stated), cash and valuables (not in the 2023 survey at all).

**Valuation (documentation):** dwellings are priced at market prices per m2 from transfer-tax and real-estate
price data, i.e. building and plot together where the plot is owned; there is no land/building split. Free-time residences are priced from the National Land Survey purchase-price
statistics. Forest land is valued at the taxation comparison value of bare land by municipality, which the
publisher says "does not reflect the real market value of forest land"; it counts only land owned by natural
persons, so estates are excluded. Farmland is valued at purchase prices, considerably above the taxation value.
Population: private households at 31 December, excluding about 2% of persons (institutional population, no postal
address, abroad). The 2023 figures are not fully comparable with earlier waves (method change in 2009).

2023 means per household (EUR), total / D1 ... D10:
- main residence 124,311 / 28,790, 47,756, 55,107, 83,824, 102,169, 122,443, 136,499, 162,185, 191,134, 313,389
- other residential property 31,194 / 6,076, 5,568, 8,481, 12,187, 19,487, 25,064, 21,105, 32,647, 43,873, 137,509
- free-time residences 13,924 / 2,243, 5,025, 7,811, 9,912, 11,475, 14,063, 13,708, 17,261, 20,835, 36,929
- forest, farmland and business 12,318 / 4,098, 6,096, 7,747, 9,631, 10,744, 9,819, 11,013, 14,071, 18,517, 31,464
- net wealth 228,742 / 47,822, 72,599, 92,589, 140,484, 161,771, 184,183, 194,827, 240,763, 299,859, 852,926

### `eurostat_coicop_long.csv` (nama_10_co3_p3) and `eurostat_coicop2018_long.csv` (nama_10_cp18)

Columns: `geo`, `coicop`, `label`, `unit`, `year`, `value`, `flag` (Eurostat status), `level` (0 TOTAL,
1 division, 2 group, 3 for CP122/CP127 in COICOP 1999), `parent_coicop`, `unit_label`. Only cells with a value or
a flag are written.

Units: `CP_MEUR`, `CP_MNAC` (current prices, million EUR / national currency); `CLV20_MEUR`, `CLV20_MNAC`
(chain-linked volumes, reference year 2020, the current reference year; **not additive** across codes);
`PD20_EUR`, `PD20_NAC` (implicit deflator 2020=100). PD20 = 100 x CP / CLV20 holds within 0.01 index points
(checked). For SE and DK the EUR series include exchange-rate movements; use `_MNAC`/`_NAC` for domestic growth
and prices. Older reference years (CLV15, CLV10, CLV05), PYP, PC_TOT and per-capita units exist and were not
pulled.

**Two datasets, and why both are here.** The requested `nama_10_co3_p3` ("Household final consumption expenditure
by purpose (COICOP 1999)", last update 2026-10-21) **ends in 2022 for SE, DK, DE and EU27_2020** and in 2024 for
FI. Eurostat now publishes the series as `nama_10_cp18` ("... (COICOP 2018)", last update 2026-10-30; catalogue
in `docs/eurostat_toc_en.txt`), which runs to **2025 for FI, SE, DK and DE and to 2024 for EU27_2020**. Same
publisher, same units: `nama_10_cp18` is the successor dataset, not a substitute source. Its classification
matches the Finnish HBS (13 divisions: 08 information and communication, 12 insurance and financial services, 13
personal care, social protection and miscellaneous). The co3 TOTAL is the **domestic concept** and equals
Statistics Finland's P31DCK exactly for 2015-2022. Its FI values for **2023 and 2024 are an older vintage**
(134,797 vs 134,509; 135,467 vs 136,333 EUR million). `nama_10_cp18` FI equals Statistics Finland's September-2026
figures in every year 2015-2025 (checked).

Coverage and gaps (CP_MEUR; years with data):

| geo | co3 years | co3 codes not published | cp18 years | cp18 codes not published |
|---|---|---|---|---|
| FI | 2015-2024 | CP101-CP104 (all education in CP105) | 2015-2025 | none (PD20: CP013, CP022; CP102 to 2023) |
| SE | 2015-2022 | none (PD20: CP044, CP102-CP105) | 2015-2025 | CP013, CP022 (PD20 also CP102, CP103) |
| DK | 2015-2022 | CP023, CP122, CP127 | 2015-2025 | CP024 |
| DE | 2015-2022 | CP023, CP122, CP127; CP022 only 2015-2017 (CLV/PD none) | 2015-2025 | CP013, CP022, CP023, CP024 |
| EU27_2020 | 2015-2022 | CP101-CP105, CP122, CP127 | 2015-2024 | none |

Flags: DE `p` (provisional) 2020-2022 in co3 and 2020-2025 in cp18; DE `d` (definition differs) on cp18 CP012
and CP021, all years. No other flags. In COICOP 1999, `CP122_127` "Prostitution; other services n.e.c." = CP122 +
CP127 (checked), so `CP12` = CP121 + CP122_127 + CP123 + CP124 + CP125 + CP126. TOTAL = sum of divisions and every
division = sum of its groups where all groups are published, within 0.2 (checked). The codes in the two files do
not mean the same thing (e.g. CP023 is narcotics in COICOP 1999 and tobacco in COICOP 2018; CP12 differs).

### `fi_na_hfce_coicop2018_long.csv` (ntp 15ag)

Statistics Finland's own annual national accounts, the source of Eurostat's FI series. Columns: `transaction`
(`P31DCK` household consumption in Finland, domestic concept, with full COICOP detail; `P31NCK` consumption of
resident households, national concept; `P33K` residents abroad; `P34K` non-residents in Finland; the last three at
total level only), `coicop_code` (`0` total, then as in the HBS), `label`, `level`, `parent_code`, `year`,
`measure` (`current_prices`, `previous_year_prices`, `volume_ref2025`: EUR million; volumes chain-linked, not
additive), `value`, `unit`, `status`, `preliminary` (2024 and 2025 are preliminary), `durability`,
`transaction_label`, `label_published`. P31NCK = P31DCK + P33K - P34K (checked). Every P31DCK parent = sum of
children in all 2,310 sets, 2015-2025 (checked).

The national-accounts code list differs from the HBS list. It has 469 codes, against 510 in the HBS. Codes with a
`Y` suffix stand for classes not split further: `041Y`/`041YY` is all of 04.1 actual rentals, with no
tenants/other split; likewise `042Y`/`042YY` for imputed rentals, plus 0212Y, 0230Y, 0314Y, 0441Y, 0443Y, 0444Y,
0454Y, 0611Y-0623Y, 0733Y, 0839Y, 0911Y, 0912Y, 0922Y, 0942Y, 0943Y, 0946Y, 0971Y, 1010Y, 1050Y, 1112Y and
1229Y. The NA has 02.4 narcotics; the HBS has 04.6 interest on housing loans, 77 and 99, which the NA lacks.
HBS 2022 aggregate (EUR 39,808 x 2,919,000 households = EUR 116.2 bn) is 89.8% of NA P31DCK 2022 (EUR 129.4 bn);
the concepts differ (institutional population, FISIM, interest on housing loans, consumption abroad).

### `fi_nonfin_assets_long.csv` (rtp 11zx) and the land question

Columns: `sector` (S0 total, S11, S12, S1311, S1313, S1314, S14 households, S15 NPISH), `instrument` (N0 total,
N111 residential buildings, N112 other buildings and structures, N113, N114, N115_N116, N117, N1171 (memo, inside
N117), N12_N13, **N211 land**), `year` 1995-2025, `measure` (`stock` end of year, `change` during the year),
`value` (EUR million, current prices), `unit`, `sector_label`, `instrument_label`. Sectors sum to S0 and
instruments to N0 exactly (checked).

**Land search (item 4).** Statistics Finland publishes no land/building split of residential property values and
no property-tax base by land and buildings. The table searches in `raw/statfin/search/` found none, and the
property-tax base is the Tax Administration's (Verohallinto), not Statistics Finland's (not fetched). What exists:
- Balance-sheet land N211 by sector (11zx). Households (S14): land EUR 131,495 m and residential buildings EUR
  375,993 m at end-2022; 126,251 m and 401,294 m at end-2023. Land / (land + residential buildings) is 25.9% in
  2022, 23.9% in 2023 and 24.5% in 2025. N211 covers **all** land owned by households, including forest and
  farmland, and is not split by land use, so this is an upper bound for the land share of household dwellings.
  N111 is buildings only. Finland transmits only total land (N211N) to Eurostat: `nama_10_nfa_bs` has none of the
  ESA 2010 subdivisions such as AN.2111 land underlying buildings. Its N211N equals 11zx for S1 and for S14+S15 in
  2022-2024 (checked).
- Single-family house plot prices (kihi 11jc): mean, median and quartile EUR per m2, mean plot area, number of
  sales and price indices by region. Whole country 2022: mean EUR 25.9/m2, median 20.3/m2, mean plot 2,837 m2;
  Greater Helsinki EUR 214.3/m2.
- Dwelling prices per m2 by form of ownership of the plot, own vs rented (ashi 12de new, 13mw old dwellings in
  housing companies). A buyer on a rented plot does not buy the land, so the gap is a land signal, but it is
  confounded by location and building differences; the publisher warns that m2 prices describe price levels and
  should not be used for price change. Old dwellings, whole country 2022: own plot EUR 2,902/m2, rented plot
  2,630/m2.

### `fi_land_indicators_long.csv`

Columns: `source_table` (kihi 11jc, ashi 12de, ashi 13mw), `region_code`, `region`, `building_type`, `rooms` (12de
only), `plot_ownership` (Own plot / Rented plot / Plot forms in total; empty for 11jc), `year`, `measure`
(publisher label), `value`, `unit`. Only cells with a value are written: 12de has 8,645 `.` and 260 `...`
(confidential) cells, 13mw 1,962 `.`, 11jc 22 `.`. 13mw reports the number of sales (asset transfer tax data) as
two measures, one up to 2019 and one from 2020.

### `fi_checks.csv`

Columns: `check_id`, `kind`, `table`, `description`, `value`, `reference`, `diff`, `tolerance`, `passed`, `note`.
`kind` is one of:
- `consistency`: internal arithmetic; all 89 pass, and the script stops if any fails.
- `crosscheck`: against a publisher headline, the other publisher, or the post; 40 rows, 38 pass. The 2 misses are
  the FI 2023-2024 values in `nama_10_co3_p3` (older vintage, above).
- `info`: 36 reported numbers, no pass/fail.

## Verification summary

- HBS 2022 against the release (2024-04-11): Q1 food share 17.7% ("18 per cent"); Q5 11.7% ("12"); Q1 housing and
  energy 38.6% ("39"); Q1 food + housing 56.3% ("56"); Q1 / Q5 housing and energy EUR 556 / 1,112 per CU per month
  ("approximately EUR 560 / 1,100"); the food share rose 1.2 pp on 2016 ("one percentage point"). All within
  rounding. Households 2,919,000 = documentation's 2.919 million = tjt 12ew 2022.
- Wealth 2023 against the release (2025-03-12): mean net wealth EUR 228,742 ("228,700"); median 96,020 ("96,000");
  main residence 44.9% of total assets ("45 per cent").
- Eurostat FI vs Statistics Finland: `nama_10_cp18` TOTAL = 15ag P31DCK in all 11 years; `nama_10_co3_p3` equal for
  2015-2022, older vintage for 2023-2024.
- Against the 2026-06-14 post: (D9 + D10)/2 mean net wealth divided by the Q5 per-household/per-CU consumption
  ratio gives EUR 391,207 per CU (post: "EUR 391k"), so the post used these vintages of 151u and 14pg. Deposits
  plus all of item 9 minus total debt is negative in every decile (maximum -357, D3), consistent with the post.
  The post's "about 3.7 years of national-accounts consumption" is not reproduced by mean net wealth x households /
  P31NCK 2023 (= 5.0), so the post used a different concept; left to the rebuild step.

## Not available or not vendored

- Adults/children and housing tenure per HBS quintile: not published (see above).
- Ranking variables of the HBS quintiles and the wealth-survey deciles: not stated by the publisher.
- Forest and bonds as separate wealth items: not published (inside combined lines).
- Land under dwellings, or a land/building split of dwelling values, at Statistics Finland: not published.
  Property-tax base by land and buildings: not a Statistics Finland product.
- tjt tables 15bv (finer ages by decile and main income source), 11wh (decile income shares and bounds), 15at and
  13dp (by numbers of adults and children, no income groups) were inspected but not vendored: 14ya and 12ew cover
  the age and composition needs, and 15at/13dp have no income grouping.
