# Federal Reserve Board data: SCF 2022 (and 2025), DFA, Z.1 land and real estate

Built by `consumption/code/acquire_fed.py` from the raw files in `consumption/data/raw/fed/` (pulled 2026-11-02;
every file is listed with URL, date, sha256 and size in `raw/fed/MANIFEST.csv`; failed downloads are in
`raw/fed/FETCH_FAILURES.csv`). Rerun from the repo root with `venv/bin/python -I consumption/code/acquire_fed.py`
(add `--offline` to never touch the network). Vendored files are never re-downloaded. A rerun rebuilds every
file below byte for byte (gzip is written with mtime 0). Every check the script runs is in `fed_checks.csv`: 311
rows, 262 passed, 0 failed, 49 informational.

## Read this first: what differs from what the task expected

1. **FRED was unreachable; the Z.1 series come from the Board's own Z.1 CSV package.** Every
   `fred.stlouisfed.org/graph/fredgraph.csv` request failed at the proxy with `ProxyError('Unable to connect to
   proxy', RemoteDisconnected('Remote end closed connection without response'))`, the same failure the BEA step
   recorded. `common.fetch()` tried once (4 attempts with backoff) on `HNOREMV`, and the other 13 FRED IDs were
   then not attempted (see `raw/fed/FETCH_FAILURES.csv`). Nothing was routed around. The Board publishes the Z.1
   (FRED mirrors it), so `z1_land.csv` is built from the Board's 2026:Q2 release CSV package
   (`releases/z1/20260911/z1_csv_files.zip`). Each paper series is mapped to its Z.1 code, and the mapping is
   verified against the paper's own cached FRED files (`pinning/cache`, `three-taxes/cache`). The FRED files are
   not vendored. If Stella wants FRED copies anyway, rerun with `--retry-failed` once FRED is reachable.
2. **The paper's `HHMSDODNS` is the seasonally adjusted mortgage level.** Its cached values match
   `LA153165105.Q` (table D.3, "Debt outstanding by sector … seasonally adjusted") exactly on every unrevised
   date. They do not match the not-seasonally-adjusted balance-sheet line `FL153165105.Q`, which agrees with it
   only at Q4. Both are in `z1_land.csv`. The paper's role `mortg` is the SA series.
3. **The NFC structures behind the paper's business residual end in 2020:Q4.** NFC residential and
   nonresidential structures at current cost (`LM105012665`, `LM105013665`) were last published in the
   2021-03-11 Z.1 release. The 2021-06-10 release dropped them from table B.103, and they are in no current table;
   both B.103 pages are vendored as evidence. They are taken from the archived 2021-03-11 package and are identical
   on all 283/76 dates to the paper's cached FRED copies. As a result the business and economy-wide land
   residuals can be built the paper's way only through 2020. The noncorporate part is available through 2026:Q2. No
   substitute (such as historical-cost structures) was used.
4. **The Z.1 2026:Q2 release revised household real estate back to 1983.** The 2025 household land residual
   on the current vintage is **23,466.4** $bn, against **23,513.1** in `three-taxes/data/aggregates_2025.csv`
   (−46.7, −0.20%). The whole gap is the revision of HH+NPO real estate (−46.7 in the 2025 annual mean).
   Structures are unchanged (28,638.0 both). The paper's method on the paper's cached 2026:Q1 vintage reproduces
   23,513.115 exactly.
5. **The SCF 2022 summary extract on the Fed site is the 2026-10-09 re-issue, in 2025 dollars.** It is not the
   October 2023 file in 2022 dollars. Every dollar variable was multiplied by 4789/4376 = **1.094378** (the
   macro's CPI-U-RS factor). Divide by that factor to compare with the 2023 Bulletin. The extract reproduces the
   Fed's own public-data historic tables exactly, and the 2022-dollar comparisons with the 2023 Bulletin are
   below.
6. **The weighting convention is the reverse of what the task assumed.** In the summary extract `WGT = X42001/5`,
   so WGT summed over all 22,975 records (all five implicates) equals the number of families, **131.31 million**
   (Bulletin: 131.3). Each implicate sums to one fifth of that. The 5x convention applies to `X42001` in the full
   public data set, where WGT x 5 = X42001 was checked on every record. Weights also differ across a family's
   implicates.
7. **The SCF 2025 survey is out (released 2026-10-09), so its extract is vendored and tidied beside 2022.** The
   2025 Bulletin ("Changes in U.S. Family Finances from 2022 to 2025", `scf26.pdf`) is vendored as well. The 2025
   survey has the first SCF questions on **total non-housing spending** (`TOTSPENDNH`) and on how a family would
   use a **windfall of one month's income** (`MPSPEND`, `MPSAVE`, `MPDEBT`, in percent). Both bear directly on the
   MPC question. The 2022 extract carries these items as zero placeholders, so they are dropped from the 2022
   file.
8. **DFA quarters after 2022:Q3 are model extrapolations, and the 2025 SCF is not yet in the DFA.** The 2026:Q2
   DFA (released 2026-09-18) predates the 2025 SCF public release (2026-10-09). Its group splits after the
   2022:Q3 SCF quarter come from the DFA's temporal-disaggregation models, not from survey data. The next DFA
   release, which follows the 2026:Q3 Z.1 (scheduled 2026-12-10), will presumably bring in the 2025 SCF and may
   revise 2022:Q4-2026:Q2 by group.
9. **One publisher-side defect in the 2022 extract: `NHNFIN` is price-adjusted twice.** It is listed twice in
   the macro's `ARRAY VALUE`, so NHNFIN = (NFIN − HOUSES) x 1.0943784 on every record. Kept as published; use
   NFIN − HOUSES instead. The 2025 extract is unaffected.
10. **The SCF "Codebook Search" app (`/apps/scfcb`) needs JavaScript (Blazor) and was not used.** The Fed's
    documentation page says the summary-extract variables are defined by `bulletin.macro.txt`. That macro is
    vendored, and its code is quoted in `scf2022_variables.md`. The macro on the site is the 2026-10-09 version.
    It has explicit 2022 branches, but the 2023 original is no longer posted.

## Files

| File | Rows | What |
|---|---|---|
| `scf2022_summary.csv.gz` | 22,975 (4,595 families x 5 implicates) | SCF 2022 summary extract, 136 columns (133 published variables + YY1/Y1 + IMPLICATE), values exactly as published, 2025 dollars |
| `scf2025_summary.csv.gz` | 21,800 (4,360 x 5) | SCF 2025 summary extract, same variables plus the five 2025-only items (141 columns), 2025 dollars |
| `scf2022_variables.md` | | Definition, unit and quoted macro/codebook text of every kept variable (both files) |
| `scf2022_roster.csv.gz` | 58,135 | SCF 2022 full public data: one row per implicate record x listed household member (positions 1-12), with PEU membership and adult flag |
| `scf2022_xvars.csv.gz` | 22,975 | SCF 2022 full public data, one row per implicate record: weight X42001, household and PEU sizes, derived adult and minor counts per PEU, credit-card limit, pay amount and frequency |
| `dfa_income_long.csv` | 57,864 | DFA by income percentile group, 1989:Q3-2026:Q2, levels and shares, every published category |
| `dfa_wealth_long.csv` | 48,148 | DFA by wealth percentile group, same layout |
| `z1_land.csv` | 9,279 | Z.1 real estate, structures and mortgages (quarterly, year-end, annual mean) and the land residuals, $bn |
| `fed_checks.csv` | 310 | Every check: computed vs published value, tolerance, pass flag, source, note |

### scf2022_summary.csv.gz and scf2025_summary.csv.gz

* Columns: `YY1, Y1, IMPLICATE, WGT`, then the published variables in the order of the table in
  `scf2022_variables.md`. Every cell is the published text copied unchanged (no float round trip). `IMPLICATE` =
  Y1 − 10·YY1 is the only added column.
* Unit of observation: the primary economic unit (PEU, the SCF "family"): the economically dominant single
  person or couple plus everyone in the household who is financially interdependent with them.
* Dollars: **2025 dollars in both files.** See item 5 above. Income variables refer to the calendar year before
  the survey (2021, 2024). They are moved to survey-year dollars by CPILAG (2022: 4315/3992; 2025: 4750/4625) and
  then by CPIADJ (2022: 4789/4376; 2025: 1). Dollar values of exactly −1/−2 are left unadjusted by the macro.
  `RENT`, `TPAY`, `MORTPAY`, `CONSPAY` and `REVPAY` are monthly. Food, vacation and total-spending variables are
  annualized.
* Statistics: weight every record with WGT and pool all implicates. This reproduces the Fed's public-data tables
  exactly (see the checks below). Standard errors need replicate weights and the multiple-imputation formula; not
  provided here.
* Percentile categories (`INCCAT`, `NINCCAT` = usual income, `NINC2CAT`, `INCPCTLECAT`, `NINCPCTLECAT`,
  `INCQRTCAT`, `NINCQRTCAT`, `NWCAT`, `NWPCTLECAT`, `ASSETCAT`) are weighted percentiles over all records pooled.
  A family's category can therefore differ across its implicates. The Bulletin's "percentile of usual income"
  rows use `NINCCAT`. The Fed's historic tables' "percentile of income" rows use `INCCAT`.
* 2025-only, from the 2025 codebook. `TOTSPENDNH` (X7790) is total spending over the last 12 months including
  food, trips, cars and other large purchases, clothing, utilities, insurance, transportation, education and
  health, excluding rent, mortgage or loan payments, investments and retirement contributions. `VACATION`
  (X7791). `MPSPEND`/`MPSAVE`/`MPDEBT` (X9375-X9377) answer: "Imagine you unexpectedly receive a sum of money equal
  to one month of your (family's) normal annual income. Thinking over the next 12 months, please indicate the
  percent of this money that you would save, the percent you would spend, and the percent that you would use to
  pay down debts." 95.7% of families (weighted) answer shares summing to exactly 100. The rest sum to
  99/99.9/99.99 (equal splits). No record is all zero. Weighted means: spend 22.3, save 47.3, pay debt 30.3
  percent.
* The Bulletin's "food away from home" (2026 Box 1) is `FOODAWAY + FOODDELV`.

**Requested variables: all present** in both extracts: YY1, Y1, WGT, AGE, KIDS, MARRIED, INCOME, WAGEINC,
BUSSEFARMINC, INTDIVINC, KGINC, SSRETINC, TRANSFOTHINC, NORMINC, INCCAT, NINCCAT, NINC2CAT, INCPCTLECAT,
NINCPCTLECAT (also INCQRTCAT, NINCQRTCAT, NWCAT, NWPCTLECAT, ASSETCAT), HOUSECL, HOUSES, ORESRE, NNRESRE, MRTHEL,
RESDBT, HOMEEQ, BUS, ACTBUS, NONACTBUS, LIQ, CHECKING, SAVING, MMA, CALL, PREPAID, CDS, STOCKS, NMMF, RETQLIQ,
EQUITY, DEQ, FIN, NFIN, ASSET, DEBT, CCBAL, INSTALL, EDN_INST, VEH_INST, NETWORTH, HHSEX, OCCAT1. Kept besides:
components (MMDA, MMMF, fund types, bond types, IRAKH, THRIFT, FUTPEN, CURRPEN, ANNUIT, TRUSTS, OTHMA, OTHFIN,
VEHIC, FARMBUS, OTHNFIN, NHNFIN, NH_MORT, HELOC, OTHLOC, BNPL, OTH_INST, ODEBT, RETEQ, PENACCTWD), spending and
saving behaviour (FOODHOME, FOODAWAY, FOODDELV, RENT, WSAVED, SAVED, SPENDMOR, SPENDLESS, EXPENSHILO), credit
stress (LATE, LATE60, HPAYDAY, BNKRUPLAST5, TURNDOWN, FEARDENIAL, TURNFEAR, EMERG*), unrealized gains (KGHOUSE,
KGORE, KGBUS, KGSTMF, KGTOTAL), payments and ratios (TPAY, MORTPAY, CONSPAY, REVPAY, PIRTOTAL, PIR40, LEVRATIO,
DEBT2INC) and demographics (AGECL, EDUC, EDCL, LF, LIFECL, FAMSTRUCT, OCCAT2, INDCAT). The other columns of the
362-column extract (race, financial literacy, shopping, institution-choice items, loan detail by lender) are
not kept. They remain in the raw zip.

**Not in the summary extract:**
* A count of adults or household size: `KIDS` counts listed children of any age whether or not they are in the
  PEU, and `MARRIED` only flags a spouse or partner. Supplied from the full public data in
  `scf2022_roster.csv.gz` / `scf2022_xvars.csv.gz` (below).
* Income per pay period: see the KVW notes.

### Kaplan-Violante-Weidner hand-to-mouth inputs

* **Liquid wealth.** `LIQ` (= CHECKING + SAVING + MMA + CALL + PREPAID), plus directly held `STOCKS`, `BOND`
  (+ `SAVBND` if wanted) and `NMMF`, net of revolving debt `CCBAL` (`NOCCBAL` = 1 when nothing revolves). Quirk:
  families that report an account with a zero balance get `LIQ` = 1 x CPIADJ (1.094378 in 2022: 235 records; 1 in
  2025: 265 records). Cash is not measured by the SCF.
* **Illiquid wealth.** `HOMEEQ` (HOUSES − MRTHEL), `ORESRE` − `RESDBT`, `NNRESRE` (already net), `RETQLIQ`,
  `CASHLI`, `CDS`, `SAVBND`, `OTHMA`; `BUS` if business wealth is included. `VEHIC` is a durable.
* **Income per pay period.** The extract has annual income only (`INCOME`, `WAGEINC`, `TRANSFOTHINC`, `SSRETINC`,
  `NORMINC`). The full data give pay on the main job and its frequency for the reference person (`X4112`,
  `X4113`) and the spouse (`X4712`, `X4713`) in `scf2022_xvars.csv.gz`. Codes: 1 day, 2 week, 3 every two weeks,
  4 month, 5 quarter, 6 year, 8 lump sum, 11 twice a year, 12 every two months, 14 piece/job, 18 hour, 22 varies,
  31 twice a month, −1 nothing, −7 other, 0 inapplicable. Values are nominal, at the time of the interview.
* **Credit limit** (the KVW borrowing constraint): `X414`, the total credit-card limit, nominal, −1 = no limit,
  0 = no cards. It is in `scf2022_xvars.csv.gz`.

### scf2022_roster.csv.gz (from the full public data set, Stata p22i6.dta, 10/18/2023)

One row per implicate record x listed person (positions with a non-zero relationship code). Columns:
* `YY1, Y1, IMPLICATE`.
* `POSITION`: 1 = reference person, 2 = spouse/partner slot, 3-12 = other listed persons.
* `REL` (X8020, X102, X108, … X226). Relationship codes: 1 respondent, 2 spouse, 3 partner, 4 child (incl.
  in-law), 5 grandchild (12 merged in), 6 parent, 7 grandparent, 8 aunt/uncle, 11 sibling, 29 other relative
  (9, 10 merged in), 34 boarder, 35 paid help, 39 other unrelated (31, 32, 36 merged in).
* `AGE` (X8022, X104, X110, …; years; respondent and spouse are 18+).
* `MARITAL` (X8023, X105, …).
* `LIVES_HERE` (X8024, X106, …): 1 yes, 5 no, 0 inap. Persons #3-#12 under 18 are 0.
* `FIN_DEP` (X8098, X107, X113, …): 1 financially dependent or shared finances, 5 independent. Every listed
  person under 18 is coded 1.
* Derived: `IN_PEU` = 1 for #1; 1 for #2 if X7020 = 2; 1 for #3-#12 if FIN_DEP = 1. This rule reproduces the
  published PEU size X7001 on all 22,975 records. `ADULT` = AGE ≥ 18.

### scf2022_xvars.csv.gz (one row per implicate record)

`YY1, Y1, IMPLICATE`, plus:
* `X42001`: weight; = 5 x WGT.
* `X101`: persons in the household, excluding listed persons who neither usually live there nor share finances.
* `X7001`: persons in the PEU. `X7050`: persons in the household outside the PEU (−1 none).
* `X7020`: spouse/partner in the PEU (1 no, 2 yes). `X8000`: respondent/spouse swapped (1) or not (5).
* `N_PEU`: derived; equals X7001 everywhere.
* `N_ADULTS_PEU`, `N_MINORS_PEU`: derived from the roster.
* `N_LISTED`: listed persons with data.
* `X414, X4112, X4113, X4712, X4713` (KVW notes above).

Weighted totals (2022): 225.0 million adults in PEUs, a mean of 1.714 adults per family. Another 23.7 million
listed adults live in surveyed households but outside the PEU, and their finances are not in the SCF balance sheet.
That matters for any per-adult dividend computed on SCF families.

### dfa_income_long.csv and dfa_wealth_long.csv

Columns:
* `date` (YYYYQn) and `group`: income `pct00to20, pct20to40, pct40to60, pct60to80, pct80to99, pct99to100`; wealth
  `Bottom50, Next40, Next9, RemainingTop1, TopPt1`.
* `group_label`.
* `category`: the DFA instrument label as published, except the summary file's DC line, renamed (below).
* `measure`: `level` or `share`.
* `value`: published text; empty where the DFA publishes NA for a 0/0 share.
* `unit`: levels in **millions of current dollars**, shares in **percent of the all-household total**, `Household
  count` in households, cutoffs in current dollars.
* `table`: `detail` or `summary` file of origin.
* `parent`: the aggregate a category adds into, so the hierarchy can be summed without double counting.

Coverage: 1989:Q3-**2026:Q2**, 148 quarters, every group in every quarter. Source: `dfa.zip` (DFA release of
2026-09-18, built on the 2026:Q2 Z.1).

**Group definitions** (from the DFA's own public code, `dfa_public_code.zip`, read as text only):
* Income groups are weighted percentile groups of SCF total family income. This is the Bulletin `INCOME`: prior
  calendar year, before tax, including withdrawals from retirement accounts. The Forbes 400 are added with
  imputed income, and the DFA's adjusted weights are used.
* The 12-way split (0-10, …, 90-95, 95-99, 99-100) is aggregated to 0-20, 20-40, 40-60, 60-80, 80-99, 99-100.
* Check against the data: the DFA's published 2022:Q3 maximum-income cutoffs match SCF 2022 `INCOME` percentiles
  in 2022 dollars. P60 is 90,796 vs 90,797, P80 is 151,328 vs 151,328, and the others are within 0.7%.
* Income cutoffs are published only at SCF survey quarters (Q3 of 1989, …, 2019, 2022). Household counts are
  published every quarter.
* Wealth groups are percentiles of DFA-reconciled net worth: bottom 50, 50-90, 90-99, 99-99.9, top 0.1.

**Concepts:**
* The DFA distributes the Z.1 **households-only** balance sheet (excluding nonprofits). Summed over groups it
  equals the Board's S14.b year-end levels for real estate, consumer durables, corporate equities and mutual
  funds, deposits, MMF shares, life insurance, other equity, home mortgages, consumer credit and liabilities to
  within 2.5e-6 in every year 1990-2025. Total assets and net worth match to within 3e-4 (largest in 2020) and
  exactly in 2025. At 2026:Q2 it equals S1M.b quarterly real estate,
  home mortgages and consumer credit.
* "Real estate" is **owner-occupied real estate only** (Z.1 LM155035015, including vacant land and mobile homes).
  Real estate that households own and rent out sits in "Unincorporated businesses" (= detail "Miscellaneous other
  equity", proprietors' equity in noncorporate business).
* "Corporate equities and mutual fund shares" excludes holdings through DC pensions. Since the 2026:Q2 release
  it includes households' hedge-fund and private-debt-fund shares, which the Z.1 now shows separately (DFA
  announcement of 2026-09-18).

**Quirks:**
* The summary file's "DC pension entitlements" = detail DC + Annuities. It is kept as **"DC pension entitlements
  incl. annuities"** (table `summary`).
* Summary "Unincorporated businesses" duplicates detail "Miscellaneous other equity". It is kept, with its parent
  saying so.
* Summary-only residuals "Other assets" and "Other liabilities" are kept. Summary rows identical to detail rows
  were dropped after checking equality.
* "Corporate and foreign bonds" is 0 in 2016:Q2-2026:Q2 (except 2021:Q3) because the Z.1 households'
  corporate-and-foreign-bond holdings (LM193063005) are 0 from 2016. Debt securities are therefore almost all
  "U.S. government and municipal securities".
* "Private businesses" was relabeled "Unincorporated businesses" on 2026-06-18.
* Shares are rounded to 0.1. Levels are rounded to $1M.

**2022:Q3 (the SCF quarter) to 2026:Q2, by income group, nominal $bn:**

| Income group | Corporate equities and MF | Real estate (owner-occupied) | Net worth |
|---|---|---|---|
| 0-20 | 616.3 → 950.9 (+54.3%) | 2,149.9 → 2,546.4 (+18.4%) | 4,092.8 → 5,145.9 (+25.7%) |
| 20-40 | 337.9 → 670.8 (+98.5%) | 3,258.4 → 3,627.4 (+11.3%) | 6,327.0 → 7,381.5 (+16.7%) |
| 40-60 | 1,281.8 → 2,143.7 (+67.2%) | 5,658.0 → 6,036.3 (+6.7%) | 11,796.8 → 13,960.6 (+18.3%) |
| 60-80 | 2,098.3 → 4,488.3 (+113.9%) | 8,102.8 → 9,310.7 (+14.9%) | 18,413.7 → 24,332.8 (+32.1%) |
| 80-99 | 15,809.2 → 30,771.6 (+94.6%) | 18,281.5 → 21,946.1 (+20.0%) | 62,845.9 → 87,970.5 (+40.0%) |
| 99-100 | 11,632.9 → 25,614.9 (+120.2%) | 5,382.1 → 6,324.8 (+17.5%) | 29,698.0 → 46,859.8 (+57.8%) |

These are extrapolated allocations (item 8): use them as the DFA's model view, not survey evidence. The 2022 and
2025 SCF extracts give the survey view.

### z1_land.csv

Columns:
* `date`: YYYYQn for quarterly rows, YYYY for annual rows.
* `series_id`: the Board's Z.1 code without the frequency suffix, exactly as in the Board's CSV (so `FL115012665`
  where FRED says `BOGZ1LM115012665Q`), or `LAND_*` for a constructed residual.
* `description` and `value`: **billions of dollars**, not seasonally adjusted levels, except LA153165105, which is
  seasonally adjusted.
* `freq`:
  * `Q`: end-of-quarter level.
  * `A_eop`: the Q4 level, which is what the Board's annual `.A` series and FRED's "A" IDs report. Checked equal
    for three series, 1945-2025.
  * `A_mean`: the calendar-year mean of the four quarterly levels, i.e. the paper's `annualize()`. Complete years
    only. Before 1952 the Z.1 is year-end only, so A_mean = A_eop.
  * `A_paper`: residuals built the paper's way.
* `unit`.
* `paper_fred_id`: the FRED ID the paper uses for this series, else empty.
* `paper_role`: the concept name in `feasibility_kappa.py`; `memo`; or `residual`.
* `release`: Z.1 2026:Q2 release of 2026-09-11, or the archived 2021-03-11 release for the two NFC structures
  series.

Series, quarterly 1945:Q4-2026:Q2 unless noted:

| series_id | paper_fred_id | role | Z.1 line |
|---|---|---|---|
| LM155035005 | HNOREMV | re_hh | HH+NPO real estate at market value (S1M.b 3) |
| LM155012665 | BOGZ1LM155012665Q | str_hh_res | Households' residential structures, current cost (S1M.b 48; households only) |
| LA153165105 | HHMSDODNS | mortg | HH+NPO home mortgages, **seasonally adjusted** level (D3.s 3) |
| FL153165105 | | memo | HH+NPO home mortgages, NSA balance-sheet level (S1M.b 37) |
| LM155035015 | | memo | Households' owner-occupied real estate (S1M.b 4; the DFA "Real estate") |
| LM165035005 | | memo | Nonprofit real estate (S1M.b 5) |
| LM155012605, LM165012665, LM165013665 | | memo | HH+NPO residential structures; NPO residential; NPO nonresidential structures (S1M.b 47, 49, 50) |
| LM105035005 | BOGZ1LM105035005A | re_nfc | NFC real estate at market value (S11.1.b 3) |
| LM115035005 | BOGZ1LM115035005A | re_nnb | Noncorporate business real estate (S11.2.b 3) |
| LM115035023, LM115035035 | | memo | Noncorporate residential / nonresidential real estate (S11.2.b 4, 5) |
| FL115012665 | BOGZ1LM115012665Q | str_nnb_res | Noncorporate residential structures, current cost (S11.2.b 43) |
| FL115013665 | BOGZ1LM115013665A | str_nnb_nonres | Noncorporate nonresidential structures, current cost (S11.2.b 44) |
| LM105012665 | BOGZ1LM105012665Q | str_nfc_res | NFC residential structures, current cost (B.103 memo; **1945:Q4-2020:Q4**, archived release) |
| LM105013665 | BOGZ1LM105013665A | str_nfc_nonres | NFC nonresidential structures, current cost (B.103 memo; **1945:Q4-2020:Q4**, archived release) |

Residuals:
* `LAND_HH_PAPER` (A_paper, 1945-2025) is the paper's `z1_hh`: mean HH+NPO real estate minus mean households'
  residential structures. It **leaves nonprofit structures inside "land"**: NPO residential and nonresidential
  structures are not subtracted, while NPO real estate is included. That is the paper's construction, kept as is.
* `LAND_BUS_PAPER` and `LAND_ECON_PAPER` (A_paper, 1945-**2020**) are the paper's `z1_econ − z1_hh` and
  `z1_econ`. They mix year-end series (NFC and NNB real estate, nonresidential structures, which are FRED "A"
  IDs) with annual means (residential structures, FRED "Q" IDs), exactly as the paper does.
* `LAND_NNB_PAPERCONV` (A_paper, 1945-2025) and `LAND_NFC_PAPERCONV` (to 2020) split the business residual with
  the same conventions. They are not paper series.
* End-of-quarter versions with all inputs at the same date: `LAND_HH_Q`, `LAND_HH_OWNOCC_Q` (owner-occupied real
  estate minus households' structures, matching the DFA concept), `LAND_NNB_Q`, `LAND_NFC_Q` and `LAND_BUS_Q`
  (both to 2020:Q4).
* The paper drops non-positive residual years. The only ones are the NFC residual in 2009 (annual) and
  2009:Q4-2010:Q1. Rows are kept and flagged in `fed_checks.csv`.

Land residuals, paper's way, $bn (current Z.1 vintage):

| Year | HH real estate (mean) | HH structures (mean) | **Household land** | Business land | Economy-wide | Noncorporate only |
|---|---|---|---|---|---|---|
| 2019 | 31,894.4 | 18,317.8 | **13,576.6** | 10,614.5 | 24,191.0 | 6,971.5 |
| 2020 | 34,371.2 | 19,354.6 | **15,016.6** | 11,652.4 | 26,669.0 | 7,742.2 |
| 2021 | 41,114.0 | 22,271.5 | **18,842.5** | n.a. | n.a. | 9,325.4 |
| 2022 | 47,034.4 | 25,742.2 | **21,292.2** | n.a. | n.a. | 8,997.4 |
| 2023 | 48,445.6 | 26,558.2 | **21,887.4** | n.a. | n.a. | 8,442.1 |
| 2024 | 50,923.7 | 27,513.0 | **23,410.7** | n.a. | n.a. | 8,354.4 |
| 2025 | 52,104.5 | 28,638.0 | **23,466.4** | n.a. | n.a. | 8,152.0 |

The 2026:Q2 end-of-quarter household land residual is 24,376.7. Home mortgages (SA, annual mean) are 13,647.4 in
2025 (paper: 13,643.4; revision +3.9). The NSA balance-sheet level averages 13,623.4.

**Mapping of the paper's FRED IDs, verified on the paper's cached FRED history:**
* Identical on all dates: BOGZ1LM115013665A (81/81), BOGZ1LM105012665Q (283/283), BOGZ1LM105013665A (76/76).
* Identical except 2026:Q1: BOGZ1LM155012665Q and BOGZ1LM115012665Q (303/304).
* HHMSDODNS = LA153165105: identical up to 2021:Q2.
* HNOREMV and NFC/NNB real estate: no exact match anywhere in the current package, so these are genuine
  revisions. HNOREMV differs from 1983:Q4 on, by at most 0.33%. NFC real estate differs from 1990 on, by at most
  0.36% (−0.24% in 2025). Noncorporate real estate also differs from 1990 on, by at most 0.24% (−0.02% in 2025).
  The 2026:Q2 release "incorporates revisions" per its announcement.

## Cross-checks against the publisher (all in fed_checks.csv)

SCF, weighted over all records:

| Statistic | 2022 extract (2025 $) | Fed public-data table (2025 $) | ÷1.094378 (2022 $) | 2023 Bulletin (2022 $, internal data) | 2026 Bulletin 2022 col. (2025 $) |
|---|---|---|---|---|---|
| Families (million) | 131.31 | | | 131.3 | 131.3 |
| Homeownership (HOUSES>0; HOUSECL=1 identical) | 66.05% | 66.05 | | 66.1 | 66.1 |
| Mean HOUSES, owners ($k) | 515.52 | 515.52 | 471.1 | 471.0 | 515.5 |
| Median HOUSES, owners ($k) | 353.48 | 353.48 | 323.0 | 323.2 | 353.7 |
| Median net worth ($k) | 210.89 | 210.89 | 192.7 | 192.9 | 211.1 |
| Mean net worth ($k) | 1,159.45 | 1,159.45 | 1,059.5 | 1,063.7 | 1,164.1 |

* The extract reproduces the Fed's historic public-data tables to their last digit for the overall values and
  all six income groups (net worth), in both years.
* Against the Bulletins (internal data) the usual-income-group medians are within 4% and the means within 2.5%,
  except the 2022 bottom quintile's mean (+8.7%). The Bulletins use the internal data, whose weights carry
  internal-only adjustments (macro: "hardcoded adjustments to weights intended to dampen the influence of
  overly influential cases", `%INCLUDE HC&YEAR`, internal runs only), plus the public file's disclosure edits.
* 2025 extract vs the 2026 Bulletin:
  * families 134.96 vs 135.0 million;
  * homeownership 65.56 vs 65.6;
  * median and mean net worth 216.1 / 1,232.0 vs 215.9 / 1,241.5 $k;
  * Box 1 spending: mean total non-housing spending $48,693 vs $48,700, median $34,000 vs $33,700, aggregate
    $6.57tn vs $6.61tn;
  * by usual income: bottom quintile $17,653 vs $17,600 (share 7.25% vs 7.2%), 80-90th $68,704 vs $68,700, top
    decile $138,396 vs $138,800 (28.44% vs 28.5%);
  * food at home $7,731 vs $7,700; vacation $4,239 vs $4,200 (38.9% vs 39% spend nothing).
* Both Bulletins are mutually consistent: the 2026 article's 2022 column equals the 2023 article × 1.094378 to
  within 0.093 ($k), i.e. rounding, across Table 2 (all families and the 6 usual-income rows) and the Table 3
  primary-residence row.
* Asset and debt hierarchies (ASSET = FIN + NFIN, NETWORTH = ASSET − DEBT, DEBT, FIN, NFIN, BUS, HOMEEQ, MRTHEL,
  MMA, NMMF, BOND, RETQLIQ, OTHMA, INSTALL, KGTOTAL) hold on every record within the published rounding. The
  exceptions are the documented −1/−2 coding and NHNFIN.

## Raw files (raw/fed/)

* `scf/`
  * The summary extracts `scfp2022excel.zip` and `scfp2025excel.zip`.
  * The full public data `scf2022s.zip`.
  * `bulletin.macro.txt` (variable definitions).
  * `codebk2022.txt` and `codebk2025.txt`.
  * `Networth_Flowchart.pdf`.
  * The Bulletins `scf23.pdf` (Aladangady et al., October 2023) and `scf26.pdf` (October 2026).
  * The Fed's historic tables `scf2025_tables_public_real_historical.xlsx`,
    `scf2025_tables_public_nominal_historical.xlsx` and `scf2025_tables_internal_nominal_historical.xlsx`.
  * Page snapshots `scf_2022.htm`, `scf-documentation.htm` and `scfindex.htm`.
* `dfa/`: `dfa.zip` (26 CSVs plus the definitions and dictionary text files), `dfa_public_code.zip` (documentation
  only, never executed), and page snapshots `dfa_overview.htm` and `dfa_announcements.htm`.
* `z1/`:
  * `z1_csv_files.zip` (2026:Q2 release, all tables with data dictionaries) and `z1_code_changes.txt` (no changes
    to any series used here).
  * `archive_20210311/z1_csv_files.zip` plus `archive_20210311/b103.htm` and `archive_20210610/b103.htm`: the
    last publication of the NFC current-cost structures, and the release that dropped them.
* `fred/`: empty. Every FRED request failed (see `FETCH_FAILURES.csv`).
