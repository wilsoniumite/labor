# Australian land rent against a basic living standard (Austaxpolicy support, 2026-10-15)

The question: if every dollar of Australian land rent were collected, how much of a basic living standard
could it pay for every resident? This is the Australian version of the paper's coverage ratio (Section 9,
Figure 6). The US figure is about one-third in 2025 (0.33, range 0.18 to 0.59). These are new, rough
estimates for a blog post. They are not results from the paper.

## Headline numbers (financial year 2024-25, land values at 30 June 2025)

| | value |
|---|---|
| Coverage, middle of 18 estimates | **0.48** (range 0.10 to 0.85) |
| Middle of the 12 estimates using land values at the bond yield | 0.57 |
| Middle of the 6 estimates using 30 or 50 per cent of housing rents | 0.14 |
| Land rent per resident, middle of the six rent measures | $14,607 a year |
| Henderson line, single adult in the workforce, including housing | $34,816 a year |
| JobSeeker single + Energy Supplement + maximum Rent Assistance | $25,756 a year |
| Age Pension single, maximum, with pension and energy supplements | $29,626 a year |
| Same grid in 1990-91 (first year with every measure) | 0.39 (range 0.08 to 0.70) |
| US, 2025 (paper) | 0.33 (range 0.18 to 0.59) |

Suggested wording (superseded; see the verifier note below): "Collecting all of Australia's measured land rent in 2024-25 could have paid for about
half of a basic living standard for every resident (0.48; between 0.10 and 0.85 depending on method)."

Verifier note (2026-10-15): do not lead with "about half" alone. The 0.48 median is set entirely by the
land-value-at-bond-yield estimates, and in 2024-25 that method gives more than all household spending on
rent, actual and imputed (residential land x yield = 1.17 x that rent bill). The article states the split:
about one-seventh by the housing-rent method and a little over half by land values at the bond yield, with
the range 0.10 to 0.85 across all 18 estimates. No ranking against the US 0.33: the benchmarks and land
measures differ.
The method choice matters more than anything else: valuing land at the bond yield gives 0.57, taking a
share of housing rents gives 0.14. This is a test of whether the money exists, not a proposal for a
100 per cent land tax.

Outputs: `out/coverage.csv` (every year 1990-91 to 2024-25, every input and all 18 estimates),
`out/headline.csv` (each number with its claim, definition, period, source and producing column),
`out/us_comparison.csv`, `out/figure_au_coverage.png`.

## Method

Coverage = land rent per year / (population x yearly cost of a basic living standard for one person).
Years are financial years ending 30 June.

**Land rent, six measures** (as in the paper's grid):
1. Residential land value (ABS 5204.0 Table 61, series A2423270K, $8,317bn at 30 June 2025) x the
   financial-year average 10-year Commonwealth bond yield (4.29 per cent in 2024-25) = $357bn.
2. The same at the yield + 1.5 points = $482bn.
3. All land, residential, commercial, rural and other (Table 61, A2423297K, $10,374bn) x yield = $445bn.
4. The same at the yield + 1.5 points = $601bn.
5. 30 per cent of household spending on actual and imputed rent for housing (ABS 5204.0 Table 42,
   A2422100A + A2422101C, $305bn) = $91bn.
6. 50 per cent of the same = $152bn.

Bond yield: FRED IRLTLT01AUM156N (OECD, monthly), July to June average. It equals RBA F2.1 FCMYGBAG10 in every
month from June 2013 (the RBA table's first month, May 2013, differs and is skipped in the comparison).
Land is the closing stock at 30 June; the average of opening and closing stock gives 0.47 instead of 0.48.

**Cost of a basic living standard, three measures** (each averaged over the days of the financial year):
1. Henderson poverty line, single person, head in the workforce, including housing (Melbourne Institute,
   *Poverty Lines: Australia*, June Quarter 2026, Table 1: $708.86 a week). Earlier quarters use the
   Institute's own method: the current line times the ratio of household disposable income per head in
   that quarter to the current quarter (Table 2, every quarter since September 1973). Weekly x 52.
2. JobSeeker Payment (Newstart Allowance before 20 March 2020), single, no children, maximum rate
   + Energy Supplement (Clean Energy Supplement from 20 March 2013, Energy Supplement from 20 September 2014)
   + maximum Rent Assistance, single, no children. DSS *Guide to Social Security Law* 5.2.1.20 (Table 5),
   5.2.6.10 (Table 1), 5.2.9.30, 5.1.10.20. Fortnightly x 26; weekly x 52 before 20 March 2020, when the
   Guide switches from weekly to fortnightly figures.
3. Age Pension, single, maximum basic rate (Guide 5.2.2.10) + maximum pension supplement (5.2.8.10) + Energy
   Supplement. Before 20 September 2009 the pension supplement did not exist; the series uses the four payments
   it absorbed, as defined in Guide 1.1.P.155: GST supplement (from 1 July 2000), pharmaceutical allowance
   (from 1 November 1990, 5.2.6.50), utilities allowance (from 20 March 2005, 5.2.6.100) and telephone
   allowance (from 1 July 1992, higher rate from 20 March 2008, 5.2.6.40). Published yearly rates are used as
   printed (26 fortnights).

Rates in force during 2024-25 (fortnightly unless stated): JobSeeker $762.70 / $778.00 / $781.10 (from
20 Mar 2024 / 20 Sep 2024 / 20 Mar 2025); Rent Assistance $188.20 / $211.20 / $212.00; Energy Supplement
$8.80 ($228.80 a year). Age Pension basic $26,535.60 / $27,224.60 / $27,333.80 a year; pension supplement
$2,121.60 / $2,163.20 / $2,173.60 a year; Energy Supplement $366.60 a year.

Rates in force now, for quoting (Guide pages last reviewed 21 September 2026 unless stated):
- JobSeeker single, no children: $824.90 a fortnight from 20 Sep 2026 (5.2.1.20); Energy Supplement $8.80
  a fortnight ($228.80 a year; 5.1.10.20, reviewed 2 Jan 2026); maximum Rent Assistance, single, no children:
  $223.80 a fortnight (5.2.6.10). Together $1,057.50 a fortnight, $27,495 a year.
- Age Pension single: basic $29,520.40 a year ($1,135.40 a fortnight; 5.2.2.10) + pension supplement
  $2,293.20 a year ($88.20; 5.2.8.10) + Energy Supplement $366.60 a year ($14.10). Together $1,237.70 a
  fortnight, $32,180 a year.
- Henderson line, single in the workforce, including housing: $708.86 a week in the June quarter 2026
  ($36,861 a year at 52 weeks).
- Cross-check: the Melbourne Institute's own Table 4 (June quarter 2026) lists the single allowee payment at
  $408.75 a week, Rent Assistance at $109.70 and the single pensioner at $600.45; all three equal the DSS
  rates used here.

**Population:** ABS 3101.0 (March 2026 release), Table 4, estimated resident population, Australia, persons
(A2060842F), average of the four quarter-end values in the financial year (27,455,073 in 2024-25).

The headline is the median of all 18 combinations (6 rent measures x 3 costs) and the range is the lowest
and highest. Each yearly cost is matched to the same financial year as the land rent.

## Comparison with the US

The two countries' numbers use different baskets, so 0.48 against 0.33 is not like for like.
- The Australian costs are generous relative to income: the Henderson line is 62.5 per cent of household
  disposable income per head, the JobSeeker package 46 per cent and the Age Pension 53 per cent (2024-25).
  The paper's US basket (Orshansky 1963, price-updated) is 24 per cent of US disposable income per head for
  a single person and 12 per cent per head for a family of four (2025).
- Measured on a common scale, land rent is much larger in Australia: about 26 per cent of household
  disposable income per head (middle of the six measures) against about 5 per cent in the US measures.
- The gap comes almost entirely from land values. Residential land at the bond yield is 23 to 32 per cent
  of income per head in Australia against 4 to 6 per cent for US household land. The housing-rent measures
  are close: 6 to 10 per cent of income per head in Australia, 4 to 7 per cent in the US.
- The US land measure is household land only, a lower bound; the Australian one is all land valued by the ABS.
See `out/us_comparison.csv`.

## History

The measure can be carried back to 1990-91 using only published rates (no price indexing of today's rates).
There is no steady trend. The housing-rent measures rise slowly, from 0.11 in 1990-91 to 0.14 in 2024-25.
The land-value measures move with interest rates: 0.49 in 1990-91 (bond yield 12.1 per cent), 0.64 in
2007-08, 0.16 in 2019-20 (yield 1.0 per cent) and 0.57 in 2024-25. Falling yields raise land values and lower
the rate applied to them at the same time, and the two do not cancel within a year.

## Caveats a referee would raise

1. **Valuing land at the bond yield is only a stand-in for the rent it earns.** In Australia it overstates the current flow.
   Residential land x the bond yield ($357bn) is 1.17 times all household spending on rent, actual and
   imputed ($305bn), and that spending pays for the buildings as well as the land. Australian house prices
   are high relative to rents, so the bond yield gives too much rent. The same check was below 1 in most years
   from 1992-93 to 2000-01, in 2008-09 and from 2011-12 to 2021-22 (column
   `diag_res_land_at_yield_over_housing_rent`).
2. **The 30 and 50 per cent land shares are taken from the paper and probably understate Australian land.**
   The ABS balance sheet puts residential land at 72 per cent of residential property value (land plus
   dwellings, 30 June 2025). Taking 72 per cent of housing rents gives a middle value of 0.27 (residential
   land only). This is a sensitivity, not part of the grid.
3. **ABS land values cover all land.** That includes commercial, rural and other land, and land owned by
   governments. The residential-only measures exclude it. Mineral and energy resources ($2,103bn at 30 June
   2025, ABS 5204.0 Table 10, A2421133C) and other pure rents are outside every measure.
4. **A full rent tax is a test of feasibility, not a proposal.** Collecting all rent would change land prices,
   and other behaviour, in ways this arithmetic ignores. The figures are gross of collection costs and of
   rates and land taxes already paid.
5. **Henderson line vintage.** The Henderson line follows household disposable income per head, and the ABS
   revises that. The latest release (June quarter 2026) puts the 2024-25 line at $34,816 a year. The four
   releases published during 2024-25 gave $33,846 ($636.46, $645.19, $660.72 and $661.52 a week). With those
   values the median is 0.49 instead of 0.48. The Institute's income index is seasonally adjusted, as
   published.
6. **Timing.** Every cost is the 2024-25 average, matching the land data. Setting 2024-25 land rent against
   rates in force now (September 2026) gives 0.46.
7. **JobSeeker choices.** The package uses the rate for a single person with no children, which is the
   standard adult rate. Single parents get a higher rate ($883.30 a fortnight from 20 Sep 2026, Guide
   5.2.1.20 Table 6), as do some older long-term recipients. The temporary Coronavirus Supplement (2020-21) is
   left out. The $50 a fortnight rise of 1 April 2021 and the $40 rise of 20 September 2023 are in the basic
   rate.
8. **The three costs cover different people.** The JobSeeker package includes Rent Assistance for a renter.
   The Age Pension does not include it. The Henderson line includes housing costs. None is a costed
   household budget. Each is an official benchmark for a single adult, applied to every resident, children
   included, as the paper does.

## Sources that could not be reached

- servicesaustralia.gov.au rate pages (JobSeeker, Age Pension, Rent Assistance) timed out through the proxy,
  with both curl and WebFetch. The DSS *Guide to Social Security Law* rate tables were used instead. They
  are the official rate history Services Australia applies, and the Melbourne Institute's Table 4 matches them.

## Run

```
venv\Scripts\python.exe austax\coverage\code\build_coverage.py      # out/coverage.csv, out/headline.csv
venv\Scripts\python.exe austax\coverage\code\us_comparison.py       # out/us_comparison.csv
venv\Scripts\python.exe austax\coverage\code\figure_au_coverage.py  # out/figure_au_coverage.png
venv\Scripts\python.exe austax\coverage\checks\check_coverage.py    # 32 checks, PASS/FAIL
```
The check reads the raw files again by a separate route: pandas instead of openpyxl, pdfplumber
instead of pypdf, and regular expressions on page text instead of an HTML table parser. It recomputes every
headline number and the whole 1990-91 to 2024-25 grid, and cross-checks the land, bond-yield, population and
payment sources against each other.
