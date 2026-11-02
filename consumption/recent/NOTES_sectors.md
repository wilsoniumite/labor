# Q2, sectors: is care absorbing US spending growth the way it absorbs job growth?

Question 2 of the consumption thread, sectors unit (Stella's question about the 2026-06-14 post). The watch site's
"private jobs outside care" page says health care and social assistance took more than all net job growth
recently. Does the national-accounts breakdown of consumer spending show the same thing?

Data: BEA's *Personal Income and Outlays, September 2026* (released 2026-10-29), monthly to 2026-09 and annual to
2025, as tidied in `consumption/data/tidy/` (see `README_bea.md`). Jobs: the watch page vendored in
`consumption/data/raw/watch/jobs-outside-care.html`. Nothing else.

Run from the repo root:

    venv/bin/python -I consumption/recent/code/sectors.py          # about 25 s: out/*.csv, figures/*.png
    venv/bin/python -I consumption/recent/checks/check_sectors.py  # about 10 s: 82 PASS/FAIL lines

## The answer in brief

1. **The breakdown has moved toward care, but far less than jobs have.** Under the broad definition (c), care is
   health care services (including the part of nonprofit health output households don't pay for), medical goods,
   net health insurance, child care and social assistance. It was 23-24% of PCE at the start of every window and
   took 36-41% of the growth of real PCE in every window from six months to four years. In the four years to
   Sep 2019 it took 25.5%, about its share of the level. Health care and social assistance took 20.5% of net job
   growth in the four years to Sep 2019, 58% in the four years to Sep 2026 and 107% in the two years to Aug 2026
   (the watch site's figure, reproduced from the page's own chart data).
2. **Spending outside care did not stall the way jobs outside care did.** Real spending outside care grew 4.7% in
   the jobs window (2.3% a year), while private jobs outside care grew by 1 thousand. Over the four years to
   Sep 2026 total real PCE grew about as much as in the four years to Sep 2019 (10.9% against 10.7%). Care's
   contribution rose from 2.7 to 4.5 points, so spending outside care grew 8.3% instead of 10.4%: about 2.0% a
   year instead of 2.5%.
3. **In dollars the shift is much smaller.** Care took 30% of the four-year increase in nominal spending, against
   26% before the pandemic and 23% of the level. The difference between the real share (41%) and the dollar share
   (30%) is relative prices: care's implicit prices rose 10.9% over the four years, all PCE prices 12.7%. Before
   the pandemic the two shares were about equal (25.5% real, 25.8% nominal).
4. **Over the watch window the gap between spending and income is mostly not care, and less still government-paid
   care.** Real PCE rose 1.82% in the six months to Sep 2026 against 0.05% for real personal income excluding
   transfers. Care (c), whoever paid, accounts for 41% of that gap measured in volumes and 25% measured in
   dollars. Medicare and Medicaid growing faster than income accounts for 15% of the dollar gap, and at most 25%
   even if all of their increase is counted as care paid by transfers. The accounts show the rest of the gap
   financed by a fall in saving: personal saving fell by $306 billion (annual rate), 40% of the increase in PCE.
5. **Over four years the excess of spending over income is all care.** Real spending outgrew real non-transfer
   income by 2.05 points from Sep 2022 to Sep 2026. Care's excess growth was larger than that (121% of the gap in
   volumes, 98% in dollars), so spending outside care grew a little less than income (8.3% against 8.8%).
   Medicare and Medicaid growing faster than income accounts for two thirds of the dollar gap. On calendar-year
   averages 2022 to 2025, spending grew *less* than non-transfer income (8.03% against 8.72%).
6. **Imputed items do not change the picture.** These are imputed rent, financial services furnished without
   payment and nonprofits' own consumption. Taking them out as well moves outside-care growth by less than 0.1
   point over four years (8.26% either way), and by 0.07 point in the watch window.
7. **The latest months are not independent evidence.** For the current quarter, BEA estimates spending on
   hospitals, nursing homes, paramedical services and private social services from BLS employment, hours and
   earnings (NIPA Handbook ch. 5, Table 5.B). That is the same CES survey behind the watch site's jobs series. July
   to September 2026 are advance estimates of this kind.

## Method

**Contributions.** Real PCE is BEA's chain-type Fisher quantity index. For each pair of adjacent periods, the
contribution of component i to the percent change is BEA's formula (NIPA Handbook ch. 4, p. 4-28):

    C_i,t = [(p_i,t / F_t) + p_i,t-1] (q_i,t - q_i,t-1) / sum_j [(p_j,t / F_t) + p_j,t-1] q_j,t-1

F_t is the Fisher price relative of PCE. p is the component's price index from Table 2.4.4U. q = v / p is its
nominal value from Table 2.4.5U deflated by its own price. The contributions add exactly (to 1e-12) to the Fisher
quantity relative minus one.

- **Signs.** "Less:" lines (149, 274, 338, 356) and every line under them enter PCE with sign -1: their values
  and quantities are negative and their prices positive, as in BEA's practice.
- **Zero values.** The level form above is used instead of the relative form, so a component whose earlier value
  is zero works. Internet access (289) is published as 0 through 1987.
- **The components.** For each pair of periods the components are the finest lines usable in both periods. A
  line is split into its children only if the same children are published in both periods and add up to it within
  rounding. Otherwise the line itself is the component. This handles lines that start late (for example 10-11 in
  2002, 177-181 and 318-323 in 1987) and lines that stop (157-158 after 2001). Over 1959-2026 the partition has
  214 to 243 components. From 2007-02 (annual: 2008) it is always the 243 current leaves of 2.4.5U.
- **Windows.** Monthly contributions are chained over a window by weighting each month with the cumulative index
  to the previous month, C_i(a..b) = sum_t (I_t-1 / I_a) C_i,t. The window contributions then add exactly to the
  window's growth. Calendar years use the annual tables directly: the year-to-year contributions for 2023, 2024
  and 2025, chained the same way.
- **Shares.** "Share of growth" is a group's window contribution divided by total real growth. "Share of the
  level" is its current-dollar value at the start of the window divided by published PCE. "Share of the nominal
  increase" is its dollar increase divided by the increase in PCE.
- **Group growth.** The real growth of a group (care, outside care, a line) is its own Fisher index built from its
  components the same way. For lines 145 and 333 (nets of two flows) BEA publishes no index and none is reported.

**Residuals against BEA's own real PCE.** The leaf-Fisher index reproduces BEA's annual real PCE growth in every
year 2008-2025 to within 0.0003 points, and the 2.4.3U index to within 0.0034 points in every year since 1960.
Monthly, it differs from BEA's chained-dollar real PCE by at most 0.007 points a month since 2022 (mean -0.0009).
The differences are smooth, not random. That fits the Handbook's description that quarterly chain indexes are
"adjusted so that the quarterly indexes average to the corresponding annual index". The monthly published indexes
evidently carry a similar adjustment, and the published detail is rounded. Over the windows the residuals are
+0.010 to +0.016 points of growth that is 1.8% to 10.9%, and zero for the annual window (Table R). The group tables
carry the residual as its own row. Shares of growth are of the leaf-Fisher total, so they add to 100.

**Cross-checks against BEA's published contributions.** These are summed from the leaves to BEA's lines.

- **Annual.** Tables 2.3.2 and 2.4.2 for 1960-2025 (8,946 line-years) agree to within 0.0055 points. That is the
  rounding of the published two-decimal figures. Periods in which a line cannot be separated from its parent are
  skipped (2.4.2 lines 282 and 286 in 1987, when Internet access starts).
- **Monthly.** Table 2.8.2 for 2022-01 to 2026-09 (1,368 line-months) agrees to within 0.0081 points.
- **Sign conventions.** BEA prints line 356 (receipts of nonprofits) unsigned and line 338 (spending by
  nonresidents) signed. The comparison detects which.
- **Over whole windows.** Chaining BEA's two-decimal monthly contributions differs from ours by up to 0.055
  points (housing, 48 months). Rounding of a smooth series does not average out. Every single month is within
  0.0081.
- **Line growth rates.** In the annual window every parent line's own Fisher growth equals BEA's 2.4.3U index
  growth within 0.007 points. In the monthly windows the care lines agree within 0.07 points. Some volatile detail
  lines differ by more (indirect commissions, foreign travel, school meals, up to 4.9 points over four years),
  because BEA's monthly detail indexes carry the temporal adjustment while our monthly chain does not. For leaves,
  2.4.5U / 2.4.4U is not exactly 2.4.3U month by month (up to 1.4% for passenger fares).
- **Quantity relatives.** Using 2.4.3U quantity relatives instead of 2.4.4U prices moves total growth by at most
  0.007 points and the care (c) contribution by at most 0.0004 points.

**Jobs.** The watch page embeds its chart data, twelve-month changes in thousands for private jobs outside health
care and social assistance, health care and social assistance, and government (BLS via FRED). Changes over two or
four years are sums of the twelve-month changes ending in each year. Those cover the jobs, twelve-month and
four-year windows, and the four years to Sep 2019 for context. The six-month and calendar-year windows cannot be
built from twelve-month changes, so they have no jobs figure. The 107% is not in the page's text (as vendored) but
follows from its data: care +1,349k, private outside care +1k, government -92k.

## Definitions

| Name | 2.4.5U lines | Note |
|---|---|---|
| (a) Health care services | 172 | Household purchases, including those paid by insurers, Medicare and Medicaid, and purchases from nonprofit hospitals and nursing homes (184, 188) |
| (a+) ... incl. NPISH health | 172 + (344 - 357) | Adds nonprofit health output households do not pay for (README_bea.md: "total health care services") |
| (b) + medical goods and insurance | (a+) + 121 + 66 + 275 | Pharmaceutical and other medical products; therapeutic appliances; net health insurance (275 includes income-loss and workers' compensation insurance, 277-278, as the brief specifies) |
| (c) + child care and social assistance | (b) + 316 + 317 | The main definition used in the headline and figures |
| (c+) + NPISH social services | (c) + (350 - 363) | Nonprofit social-service output households do not pay for |
| (s) care services only | (a+) + 316 + 317 + (350 - 363) | Not asked for: drops goods and insurance, which NAICS 62 workers do not produce, so it is the closest spending analogue of the jobs series |
| Imputed and non-cash items | 160 + 163 + 254 + 342 | Owner-occupied nonfarm imputed rent, rental value of farm dwellings (163), financial services furnished without payment, NPISH final consumption |
| Outside care (k) | PCE minus care (k) | A Fisher index of the remaining leaves |
| Outside care (k) and imputed | PCE minus care (k) minus imputed items | The overlap (NPISH health and social services are inside 342) is excluded once, so (a) and (a+) give the same series, as do (c) and (c+) |

Functional groups (a partition of PCE): durable goods; nondurable goods excluding energy; gasoline and other energy
goods (113); housing and utilities excluding imputed rent; imputed rent (160); health care (172); transportation,
recreation, food services and accommodations; financial services and insurance excluding FSFWP; FSFWP (254); other
services excluding net foreign travel; net foreign travel (333); NPISH final consumption (342). The contribution
figures use a second partition: care (c) in five parts, and the rest of PCE by function with the care lines taken
out.

## Results

All growth rates are for the whole window, not annualized, unless marked. Contributions are in percentage points
of real PCE growth. Monthly windows run from the first month named to the last (for example Aug 2024 to Aug 2026
is 24 monthly changes). The annual window is calendar 2022 to 2025 on annual data.

**Table 1. Headline, care definition (c).**

| Window | Real PCE growth, % (BEA) | Care (c) share of PCE at start, % | Care (c) contribution, pp | Care (c) share of real growth, % | Care (c) share of the nominal increase, % | Care (c) real growth, % | Prices: care (c) / all PCE, % | Outside care (c) real growth, % (annualized) | Outside care (c) and imputed, % | Real income excl. transfers, % | Care share of net job growth, % (watch) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Aug 2024 to Aug 2026 (jobs window) | 5.62 | 24.0 | 2.02 | 35.9 | 26.7 | 8.43 | 4.75 / 6.23 | 4.73 (2.3) | 4.97 | 2.69 | 107.2 |
| 12 months to Sep 2026 | 2.54 | 24.4 | 0.93 | 37.0 | 22.7 | 3.86 | 1.90 / 3.65 | 2.09 (2.1) | 2.02 | 0.54 | 104.8 |
| 6 months to Sep 2026 (watch window) | 1.82 | 24.3 | 0.74 | 40.8 | 24.8 | 3.06 | 0.50 / 1.65 | 1.41 (2.8) | 1.48 | 0.05 |  |
| 4 years to Sep 2026 | 10.87 | 22.9 | 4.48 | 41.3 | 29.9 | 19.63 | 10.87 / 12.74 | 8.26 (2.0) | 8.26 | 8.82 | 58.4 |
| 2022 to 2025 (annual data) | 8.03 | 22.9 | 3.31 | 41.2 | 31.6 | 14.49 | 9.15 / 9.33 | 6.11 (2.0) | 6.10 | 8.72 |  |

The jobs share for the six-month and calendar-year windows cannot be built from the page's twelve-month changes.

**Table 2. Care's share of real PCE growth, % (share of PCE at the start of the window, %), by definition.**

| Care definition | Aug 2024 to Aug 2026 (jobs window) | 12 months to Sep 2026 | 6 months to Sep 2026 (watch window) | 4 years to Sep 2026 | 2022 to 2025 (annual data) |
|---|---|---|---|---|---|
| (a) Health care services, households (172) | 25.3 (16.9) | 23.0 (17.2) | 29.6 (17.1) | 31.8 (15.9) | 34.1 (15.9) |
| (a+) Health care services incl. NPISH health (172 + 344 - 357) | 25.2 (17.3) | 25.8 (17.5) | 26.9 (17.5) | 30.8 (16.3) | 31.4 (16.3) |
| (b) (a+) + medical products, appliances, net health insurance (121, 66, 275) | 34.1 (22.6) | 36.1 (22.9) | 38.5 (22.8) | 40.0 (21.5) | 39.7 (21.5) |
| (c) (b) + child care and social assistance (316, 317) | 35.9 (24.0) | 37.0 (24.4) | 40.8 (24.3) | 41.3 (22.9) | 41.2 (22.9) |
| (c+) (c) + NPISH social services (350 - 363) | 36.3 (24.6) | 36.7 (25.0) | 40.1 (24.9) | 41.7 (23.5) | 41.8 (23.5) |
| (s) Care services only: (a+) + 316 + 317 + (350 - 363) | 27.4 (19.3) | 26.4 (19.6) | 28.5 (19.6) | 32.5 (18.3) | 33.5 (18.3) |

**Table 3. Real growth outside care / outside care and imputed items, %, by definition.**

| Care definition | Aug 2024 to Aug 2026 (jobs window) | 12 months to Sep 2026 | 6 months to Sep 2026 (watch window) | 4 years to Sep 2026 | 2022 to 2025 (annual data) |
|---|---|---|---|---|---|
| (a) Health care services, households (172) | 5.04 / 5.39 | 2.34 / 2.25 | 1.54 / 1.72 | 8.79 / 9.17 | 6.28 / 6.68 |
| (a+) Health care services incl. NPISH health (172 + 344 - 357) | 5.08 / 5.39 | 2.27 / 2.25 | 1.60 / 1.72 | 8.98 / 9.17 | 6.57 / 6.68 |
| (b) (a+) + medical products, appliances, net health insurance (121, 66, 275) | 4.77 / 5.03 | 2.09 / 2.01 | 1.44 / 1.52 | 8.29 / 8.29 | 6.15 / 6.15 |
| (c) (b) + child care and social assistance (316, 317) | 4.73 / 4.97 | 2.09 / 2.02 | 1.41 / 1.48 | 8.26 / 8.26 | 6.11 / 6.10 |
| (c+) (c) + NPISH social services (350 - 363) | 4.74 / 4.97 | 2.12 / 2.02 | 1.44 / 1.48 | 8.27 / 8.26 | 6.10 / 6.10 |
| (s) Care services only: (a+) + 316 + 317 + (350 - 363) | 5.05 / 5.35 | 2.31 / 2.26 | 1.61 / 1.69 | 8.98 / 9.15 | 6.54 / 6.65 |

**Table 4. Context: care (c) year by year and over earlier four-year spans.** Annual rows are calendar years on
annual data; the "share of PCE at start" is the previous year's.

| Period | Real PCE growth, % | Care (c) share of PCE at start, % | Care (c) contribution, pp | Care (c) share of real growth, % | Care (c) share of the nominal increase, % | Care (a+) share of real growth, % | Outside care (c) real growth, % | Real income excl. transfers, % |
|---|---|---|---|---|---|---|---|---|
| 2011 | 1.70 | 23.0 | 0.50 | 29.3 | 22.9 | 21.8 | 1.56 | 4.39 |
| 2012 | 1.37 | 23.0 | 0.34 | 25.0 | 23.7 | 29.7 | 1.33 | 3.58 |
| 2013 | 1.74 | 23.0 | 0.39 | 22.1 | 21.1 | 11.1 | 1.76 | -0.54 |
| 2014 | 2.83 | 22.9 | 0.77 | 27.1 | 26.0 | 13.4 | 2.68 | 3.69 |
| 2015 | 3.37 | 23.1 | 1.04 | 30.8 | 37.9 | 23.7 | 3.04 | 4.27 |
| 2016 | 2.45 | 23.6 | 0.70 | 28.4 | 32.4 | 24.9 | 2.30 | 1.49 |
| 2017 | 2.64 | 23.9 | 0.52 | 19.9 | 22.0 | 15.1 | 2.78 | 3.51 |
| 2018 | 2.74 | 23.8 | 0.79 | 28.9 | 25.7 | 16.3 | 2.56 | 3.28 |
| 2019 | 2.15 | 23.9 | 0.66 | 30.5 | 28.9 | 24.6 | 1.96 | 3.09 |
| 2020 | -2.52 | 24.1 | -0.64 | 25.3 | 13.7 | 33.9 | -2.48 | 0.07 |
| 2021 | 8.84 | 24.2 | 1.56 | 17.7 | 16.4 | 13.5 | 9.58 | 5.17 |
| 2022 | 2.91 | 23.3 | 1.01 | 34.6 | 18.7 | 25.8 | 2.47 | 0.35 |
| 2023 | 2.30 | 22.9 | 1.06 | 46.1 | 29.6 | 34.7 | 1.60 | 3.65 |
| 2024 | 2.90 | 23.3 | 1.18 | 40.9 | 34.2 | 33.0 | 2.23 | 3.00 |
| 2025 | 2.63 | 23.9 | 0.99 | 37.5 | 31.0 | 27.1 | 2.16 | 1.83 |
| 2010 to 2019 | 23.05 | 23.0 | 6.26 | 27.2 | 26.7 | 19.7 | 21.82 | 30.05 |
| 2015 to 2019 | 10.36 | 23.6 | 2.78 | 26.8 | 26.8 | 19.9 | 9.94 | 11.85 |
| 2015-09 to 2019-09 | 10.65 | 23.8 | 2.72 | 25.5 | 25.8 | 18.7 | 10.42 | 11.78 |
| 2018-09 to 2022-09 | 11.46 | 24.0 | 2.69 | 23.4 | 18.9 | 14.8 | 11.54 | 8.93 |
| 2022-09 to 2026-09 | 10.85 | 22.9 | 4.48 | 41.3 | 29.9 | 30.8 | 8.26 | 8.82 |

**Table 5. Contributions by function, pp (share of real growth, %).**

| Group | Aug 2024 to Aug 2026 (jobs window) | 12 months to Sep 2026 | 6 months to Sep 2026 (watch window) | 4 years to Sep 2026 | 2022 to 2025 (annual data) | Share of PCE, Sep 2022, % |
|---|---|---|---|---|---|---|
| Goods | 1.93 (34.4) | 0.77 (30.5) | 0.42 (23.0) | 3.37 (31.1) | 2.41 (30.1) | 33.3 |
| Services | 3.68 (65.6) | 1.75 (69.5) | 1.39 (77.0) | 7.48 (68.9) | 5.61 (69.9) | 66.7 |
| Durable goods | 0.85 (15.2) | 0.35 (13.9) | 0.12 (6.7) | 1.65 (15.2) | 1.23 (15.3) | 11.6 |
| Nondurable goods excl. energy | 1.18 (21.0) | 0.54 (21.3) | 0.37 (20.3) | 1.80 (16.6) | 1.16 (14.5) | 19.0 |
| Gasoline and other energy goods | -0.10 (-1.8) | -0.12 (-4.7) | -0.07 (-4.0) | -0.07 (-0.7) | 0.02 (0.3) | 2.7 |
| Housing and utilities excl. imputed rent | 0.18 (3.2) | 0.11 (4.5) | 0.12 (6.9) | 0.34 (3.1) | 0.18 (2.2) | 6.2 |
| Imputed rent of owner-occupied housing (160) | 0.36 (6.4) | 0.14 (5.6) | 0.07 (4.1) | 0.79 (7.3) | 0.66 (8.2) | 11.5 |
| Health care (172) | 1.42 (25.3) | 0.58 (23.0) | 0.53 (29.6) | 3.45 (31.8) | 2.73 (34.1) | 15.9 |
| Transportation services | 0.14 (2.5) | 0.04 (1.5) | 0.06 (3.4) | 0.36 (3.3) | 0.28 (3.5) | 3.3 |
| Recreation services | 0.21 (3.8) | 0.09 (3.6) | 0.09 (4.8) | 0.27 (2.5) | 0.20 (2.5) | 3.9 |
| Food services and accommodations | 0.34 (6.0) | 0.21 (8.2) | 0.27 (14.8) | 0.59 (5.4) | 0.50 (6.2) | 7.1 |
| Financial services and insurance excl. FSFWP | 0.24 (4.3) | 0.10 (4.1) | 0.06 (3.1) | 0.33 (3.0) | 0.18 (2.2) | 4.9 |
| Financial services furnished without payment (254) | 0.28 (5.0) | 0.12 (4.8) | 0.08 (4.3) | 0.52 (4.8) | 0.33 (4.1) | 2.5 |
| Other services excl. net foreign travel | 0.27 (4.8) | 0.07 (2.8) | 0.05 (2.8) | 0.54 (4.9) | 0.47 (5.9) | 8.2 |
| Net foreign travel (333) | 0.19 (3.4) | 0.07 (2.9) | 0.05 (2.8) | 0.26 (2.4) | 0.21 (2.6) | 0.1 |
| NPISH final consumption (342) | 0.04 (0.8) | 0.22 (8.7) | 0.01 (0.4) | 0.04 (0.4) | -0.13 (-1.6) | 3.1 |
| PCE (sum of the 243 leaves) | 5.61 (100.0) | 2.52 (100.0) | 1.81 (100.0) | 10.85 (100.0) | 8.03 (100.0) | 100.0 |

**Table 6. Contributions under the care-first partition, pp** (the bars in the contribution figures).

| Group | Aug 2024 to Aug 2026 (jobs window) | 12 months to Sep 2026 | 6 months to Sep 2026 (watch window) | 4 years to Sep 2026 | 2022 to 2025 (annual data) |
|---|---|---|---|---|---|
| care: Health care services (172) | 1.42 | 0.58 | 0.53 | 3.45 | 2.73 |
| care: NPISH health (344 - 357) | -0.01 | 0.07 | -0.05 | -0.11 | -0.21 |
| care: Medical products and appliances (121, 66) | 0.47 | 0.25 | 0.21 | 0.94 | 0.62 |
| care: Net health insurance (275) | 0.03 | 0.01 | 0.00 | 0.06 | 0.05 |
| care: Child care and social assistance (316, 317) | 0.10 | 0.02 | 0.04 | 0.14 | 0.12 |
| Durable goods excl. therapeutic appliances | 0.81 | 0.32 | 0.10 | 1.59 | 1.20 |
| Nondurable goods excl. energy and medical products | 0.75 | 0.32 | 0.18 | 0.92 | 0.57 |
| Gasoline and other energy goods | -0.10 | -0.12 | -0.07 | -0.07 | 0.02 |
| Housing and utilities excl. imputed rent | 0.18 | 0.11 | 0.12 | 0.34 | 0.18 |
| Imputed rent of owner-occupied housing | 0.36 | 0.14 | 0.07 | 0.79 | 0.66 |
| Transportation services | 0.14 | 0.04 | 0.06 | 0.36 | 0.28 |
| Recreation services | 0.21 | 0.09 | 0.09 | 0.27 | 0.20 |
| Food services and accommodations | 0.34 | 0.21 | 0.27 | 0.59 | 0.50 |
| Financial services and insurance excl. FSFWP and health insurance | 0.21 | 0.09 | 0.05 | 0.27 | 0.13 |
| Financial services furnished without payment | 0.28 | 0.12 | 0.08 | 0.52 | 0.33 |
| Other services excl. net foreign travel, child care, social assistance | 0.17 | 0.05 | 0.01 | 0.39 | 0.35 |
| Net foreign travel | 0.19 | 0.07 | 0.05 | 0.26 | 0.21 |
| NPISH final consumption excl. health | 0.05 | 0.15 | 0.06 | 0.15 | 0.09 |

**Table 7. The pieces that separate the care definitions: contribution, pp (share of PCE at start, %).**

| Part | Aug 2024 to Aug 2026 (jobs window) | 12 months to Sep 2026 | 6 months to Sep 2026 (watch window) | 4 years to Sep 2026 | 2022 to 2025 (annual data) |
|---|---|---|---|---|---|
| NPISH health (344 - 357) | -0.01 (0.4) | 0.07 (0.3) | -0.05 (0.4) | -0.11 (0.4) | -0.21 (0.4) |
| Medical products, appliances, net health insurance (121, 66, 275) | 0.50 (5.3) | 0.26 (5.4) | 0.21 (5.3) | 1.00 (5.1) | 0.67 (5.2) |
| Child care (316) | 0.02 (0.3) | 0.00 (0.3) | 0.00 (0.3) | 0.01 (0.3) | 0.01 (0.3) |
| Social assistance (317) | 0.08 (1.1) | 0.03 (1.2) | 0.04 (1.1) | 0.13 (1.1) | 0.10 (1.1) |
| NPISH social services (350 - 363) | 0.02 (0.6) | -0.01 (0.6) | -0.01 (0.6) | 0.04 (0.6) | 0.05 (0.6) |
| Day care and nursery schools (296, education; not in any care variant) | 0.01 (0.1) | 0.00 (0.1) | 0.00 (0.1) | 0.00 (0.1) | 0.01 (0.1) |

**Table R. The leaf-Fisher index against BEA's published real PCE.**

| Window | Leaf Fisher, % | BEA chained dollars, % | Residual (BEA minus leaf), pp | Largest gap to chained published 2.8.2/2.3.2 contributions, pp |
|---|---|---|---|---|
| Aug 2024 to Aug 2026 (jobs window) | 5.6122 | 5.6224 | +0.0102 | 0.039 |
| 12 months to Sep 2026 | 2.5205 | 2.5366 | +0.0161 | 0.020 |
| 6 months to Sep 2026 (watch window) | 1.8088 | 1.8188 | +0.0100 | 0.016 |
| 4 years to Sep 2026 | 10.8532 | 10.8688 | +0.0155 | 0.055 |
| 2022 to 2025 (annual data) | 8.0251 | 8.0251 | -0.0000 | 0.012 |

**Table 8. Care spending against Medicare and Medicaid: growth over the window / increase, $ billion at annual
rates (annual window: calendar-year levels).**

| Item | Aug 2024 to Aug 2026 (jobs window) | 12 months to Sep 2026 | 6 months to Sep 2026 (watch window) | 4 years to Sep 2026 | 2022 to 2025 (annual data) |
|---|---|---|---|---|---|
| (a+) Health care services incl. NPISH health (172 + 344 - 357) | 14.4% / 495 | 6.5% / 241 | 3.8% / 146 | 34.7% / 1,016 | 26.0% / 750 |
| (b) (a+) + medical products, appliances, net health insurance (121, 66, 275) | 13.5% / 608 | 5.9% / 285 | 3.5% / 174 | 32.9% / 1,268 | 25.0% / 951 |
| (c) (b) + child care and social assistance (316, 317) | 13.6% / 650 | 5.8% / 301 | 3.6% / 188 | 32.6% / 1,341 | 25.0% / 1,010 |
| Medicare (19) | 19.7% / 220 | 10.7% / 131 | 5.2% / 67 | 41.9% / 399 | 27.1% / 256 |
| Medicaid (20) | 16.2% / 153 | 2.2% / 23 | 2.8% / 30 | 33.8% / 277 | 25.7% / 210 |
| Medicare + Medicaid (19 + 20) | 18.1% / 373 | 6.7% / 154 | 4.1% / 97 | 38.2% / 676 | 26.5% / 466 |
| PCE | 12.2% / 2,430 | 6.3% / 1,326 | 3.5% / 760 | 25.0% / 4,490 | 18.1% / 3,199 |
| Personal income excl. transfers (PI - line 16) | 9.1% / 1,871 | 4.2% / 910 | 1.7% / 378 | 22.7% / 4,160 | 18.9% / 3,398 |

**Table 9. The gap between spending and income excluding transfers.**

| Item | Aug 2024 to Aug 2026 (jobs window) | 12 months to Sep 2026 | 6 months to Sep 2026 (watch window) | 4 years to Sep 2026 | 2022 to 2025 (annual data) |
|---|---|---|---|---|---|
| Real gap, pp | 2.93 | 1.99 | 1.77 | 2.05 | -0.69 |
| Nominal gap, pp | 3.12 | 2.07 | 1.80 | 2.31 | -0.76 |
| Part of nominal gap from Medicare + Medicaid (19 + 20): s0 (g - gY), pp | 0.93 | 0.27 | 0.26 | 1.53 | 0.76 |
| Share of the nominal gap from Medicare + Medicaid (19 + 20), % | 29.85 | 13.22 | 14.61 | 65.95 | n/a |
| Gross upper bound: increase in Medicare + Medicaid / (increase in PCE - increase in income excl. transfers), % | 66.75 | 37.03 | 25.38 | 205.11 | n/a |
| Share of the nominal gap from (c) (b) + child care and social assistance (316, 317), % | 34.64 | 19.18 | 25.23 | 98.39 | n/a |
| Share of the real gap from (c) (b) + child care and social assistance (316, 317), % (gap on the leaf Fisher) | 46.88 | 40.52 | 41.33 | 121.01 | n/a |

The arithmetic. Write C for nominal PCE, Y for nominal personal income less current transfer receipts (Table 2.6
line 1 minus line 16), and M for Medicare plus Medicaid benefits (lines 19 + 20). Over a window,

    g_C - g_Y = s_M (g_M - g_Y) + (1 - s_M)(g_R - g_Y),     s_M = M_0 / C_0,  R = C - M

This is an identity, so "the part of the gap from M" is s_M (g_M - g_Y). It is the growth of M beyond what
it would have been at the growth rate of non-transfer income. The real gap uses the same deflator for both sides
(line 36 is deflated by the PCE price index), so the nominal and real gaps differ only by the factor 1 + PCE
inflation, and shares of the nominal gap are the same either way. The "gross upper bound" credits all of the
increase in M to the gap: dM / (dC - dY). For care spending (all payers) the same formula is used in dollars. In
volumes, care's part of the real gap is its contribution minus its start share times real income growth.

The row is n/a where the gap is not positive (calendar 2022-2025).

**Table 10. Where the change in spending came from: changes over the window, $ billion at annual rates.** From
the accounting identity PCE = income excl. transfers + transfer receipts - taxes - interest and transfer payments -
saving. Line 16 (transfer receipts) splits into Medicare + Medicaid, Social Security, and the rest (other social
benefits and transfers from business).

| Item | Aug 2024 to Aug 2026 (jobs window) | 12 months to Sep 2026 | 6 months to Sep 2026 (watch window) | 4 years to Sep 2026 | 2022 to 2025 (annual data) |
|---|---|---|---|---|---|
| Personal income excl. transfers | 1,871 | 910 | 378 | 4,160 | 3,398 |
| + Medicare + Medicaid | 373 | 154 | 97 | 676 | 466 |
| + Social security | 206 | 92 | 26 | 446 | 358 |
| + Other transfer receipts | 38 | -53 | 19 | -59 | -52 |
| - Personal current taxes | -383 | -27 | -41 | -211 | -100 |
| - Interest and transfer payments | -69 | -29 | -25 | -298 | -289 |
| - Personal saving | 395 | 279 | 306 | -226 | -583 |
| = Change in PCE (sum of the above) | 2,430 | 1,326 | 760 | 4,490 | 3,199 |
| Change in PCE (published) | 2,430 | 1,326 | 760 | 4,490 | 3,199 |

**Table 11. Jobs, from the watch page's chart data (thousands; twelve-month changes summed).**

| Window | Private outside care, thousands | Health care and social assistance, thousands | Government, thousands | Care share of net job growth, % | Care share of private job growth, % |
|---|---|---|---|---|---|
| Aug 2024 to Aug 2026 (jobs window) | +1 | +1349 | -92 | 107.2 | 99.9 |
| 12 months to Sep 2026 | +192 | +520 | -216 | 104.8 | 73.0 |
| 4 years to Sep 2026 | +1240 | +3192 | +1030 | 58.4 | 72.0 |
| 4 years to Sep 2022 | +3625 | +776 | -177 | 18.4 | 17.6 |
| 4 years to Sep 2019 (pre-pandemic) | +6612 | +1866 | +613 | 20.5 | 22.0 |

**Figures** (`figures/`, 200 dpi):

- `fig_care_share_of_growth.png`: care's share of real PCE growth against its share of the level, by window and
  definition, with the share of net job growth.
- `fig_outside_care.png`: real PCE, outside care (c), outside care (c) and imputed items, and real income excluding
  transfers, Sep 2022 = 100.
- `fig_contributions_2024-08_2026-08.png` and `fig_contributions_2022-09_2026-09.png`: contributions by part of
  care and by function outside it.

## What it means, in plain words

Care is taking a bigger slice of real spending growth than it used to. Before the pandemic it took about a
quarter, roughly its weight in the budget. Since 2022 it has taken about four tenths in every window you choose,
and its own volume has grown about 4.5% a year against about 2% for everything else. So the spending data do
lean the same way as the jobs data, toward health care, drugs and care services.

But the lean is much milder than in jobs, and in money terms it is mild indeed. Outside care, real spending kept
growing at about 2% a year, close to its pre-pandemic pace of 2.5%. Over the last year it even outgrew real
non-transfer income by a wide margin (2.1% against 0.5%). Private employment outside care grew by 1 thousand over
the two years to Aug 2026 and by 192 thousand over the year to Sep 2026. In dollars care took
30% of the four-year increase in spending, not much above its 23% weight. The volume share is higher mainly
because measured care prices rose more slowly than other prices after 2022.

On the watch site's spending-and-income gap: over four years the excess of spending over non-transfer income is
small, and care accounts for all of it. The big gap is recent, in 2026. Care accounts for only a quarter to two
fifths of it, and government-paid care for about 15 to 25%. Most of the 2026 gap was paid for by households
saving less, which is a different story from care.

## Caveats

- **The detail is weaker than the totals.** BEA warns, of the 2.4.5U detail used here (NIPA Handbook ch. 5): "BEA
  does not include these detailed estimates in the published tables because their quality is significantly lower
  than that of the higher-level categories of which they are a part. In particular, these detailed estimates are
  more likely to be based on judgmental trends or on less reliable source data." The care groups are mostly whole
  published categories (health care 172 is a Table 2.3.5 line), but variant (c) and the parts in Table 7 rest on
  U detail.
- **Recent care spending is partly built from employment.** Handbook ch. 5, Table 5.B:
  - Hospitals, nursing homes, paramedical services and private social services: the advance estimate (and the
    second, for social services) uses "CES data on employment, hours, and earnings".
  - Physician services and child care: judgmental trends.
  - The Census Quarterly Services Survey arrives with the later estimates.
  - For services without such indicators, real spending is extrapolated "using the rate of change in population
    and a projected rate of change in real per capita consumption".

  The 2026 Q3 months (Jul-Sep) are advance estimates. So for the latest quarter the care share of spending growth
  is partly an echo of the jobs data, not an independent confirmation. Revisions (2026-11-25 and later) will
  replace these with receipts data.
- **The real/nominal split for care depends on its price measures.** These are PPIs for physicians, hospitals,
  nursing care and home health; the CPI for child care; and a BEA input-cost index for other social services
  (Table 5.B). Care's real share of growth (41%) and nominal share (30%) differ only through these prices.
- **The monthly residual is BEA's temporal adjustment.** Our monthly Fisher chain is the unadjusted one, so
  window totals sit 0.010-0.016 points below BEA's published real PCE (Table R). The detail-line growth rates in
  the per-line files are our chain's; BEA's own 2.4.3U growth is shown beside them.
- **Nets of two flows.** NPISH health (344 - 357) and NPISH social services (350 - 363) are each gross output
  minus sales. The net is about 5% of the gross flows for health and about half for social services. Their
  contributions are well defined, but their own real growth (for example -29% for NPISH health over four years) is
  not robust. Net foreign travel (333) has no real growth at all.
- **Medicare + Medicaid as "care paid through government" is an upper-bound proxy.**
  - PCE health care is paid by households, private insurers, Medicare, Medicaid and others.
  - Medicare benefits are gross of the premiums enrollees pay, so the net transfer is smaller. As far as I know
    the NIPAs count these premiums among contributions for government social insurance (line 25), but no vendored
    document here says so.
  - Some of the increase replaces private payment, for example as people age into Medicare.
  - The monthly Medicare series is a smooth path: its monthly increments rise by under $0.4 billion a month
    through 2025-26, so it is evidently interpolated. Short-window comparisons with it are rough.
  - Veterans' health care is not in PCE at all: Handbook ch. 5, Table 5.1, says PCE "excludes services provided
    directly at government-owned facilities (such as Veterans' Administration hospitals)".
- **What care leaves out.** Day care and nursery schools (296, education services, 0.1% of PCE) is not in any care
  definition; Table 7 shows it would change nothing. Net health insurance includes income-loss and workers'
  compensation insurance (277-278) because the brief defines (b) with line 275.
- **The imputed set is the brief's four lines.** BEA's Table 5.1 lists other imputations inside PCE, such as
  employer-paid medical insurance, wages and salaries paid in kind and private workers' compensation. They are not
  separate 2.4.5U lines and are not in the imputed set.
- **Jobs and spending are different units.** Jobs are a headcount in NAICS 62 (health care and social assistance).
  Spending is the volume of goods and services bought, whoever produced them. Definition (s) is the closest match
  to the industry.
- **The data will be revised.** Vintage: the 2026-10-29 release. The October data come on 2026-11-25. The
  distributional files are an older vintage and are not used here.

## Judgment calls

1. **Prices from 2.4.4U, with q = v / p.** The brief allows 2.4.4U prices or 2.4.3U quantities. The alternative
   changes nothing that matters (check H1).
2. **The care definitions build on (a+).** (b) and (c) build on (a+), which includes NPISH health, not on (a).
   (a) alone is reported in every table. (s) is added as the closest analogue of the jobs series.
3. **Farm dwellings are imputed but not functional imputed rent.** Rental value of farm dwellings (163) is in the
   imputed set. In the functional split, "imputed rent" is line 160 only, and 163 stays in housing and utilities.
4. **Other services exclude net foreign travel.** The functional "other services" group is line 280 without net
   foreign travel (333), which the brief lists separately. In BEA's Table 2.3.5, other services includes it.
5. **The residual is a separate row.** Window contributions add to the leaf-Fisher total, and the residual against
   BEA is reported as its own row, not spread over the components.
6. **Jobs over longer windows are summed.** Two- and four-year job changes are sums of twelve-month changes from
   the watch page. The six-month and calendar-year windows have no jobs figure.
7. **Gap shares need a positive gap.** They are left blank where the gap is not positive.
8. **NOTES embeds generated tables.** The results tables are generated by `sectors.py`
   (`out/notes_tables_sectors.md`) and pasted here. Check G1 fails if they drift apart.
9. **One extra fetch.** NIPA Handbook ch. 4 (Estimating Methods) was fetched through `common.fetch()` into
   `consumption/data/raw/bea/nipa/`, with its manifest row added, for the contributions formula and the
   temporal-adjustment text. No other download was made.

## Files

| File | What |
|---|---|
| `code/sectors.py` | Everything: the Fisher engine, windows, groups, financing, jobs, published comparisons, figures, these tables |
| `checks/check_sectors.py` | 82 independent checks (relative-form recomputation, identities, BEA's published numbers, the watch figures, the notes tables, figure dpi) |
| `out/sector_contributions_<start>_<end>.csv` | One row per 2.4.5U line 1-368: label, level, parent, leaf flag, sign, functional group, care tags (yes/part/no per variant), imputed tag, signed start and end nominal values, start share, real growth (ours and BEA's 2.4.3U), contribution (pp), share of growth (%) |
| `out/sector_groups_<start>_<end>.csv` | One row per group: kind, definition (lines), number of leaves, start and end nominal values, start share, nominal and real growth, annualized real growth, contribution, share of growth, note; plus BEA's real PCE and the residual |
| `out/headline_sectors.csv` | Per window and care variant: shares of level, growth and nominal increase, care and outside-care growth, prices, real income, jobs shares |
| `out/outside_care_monthly.csv` | Long format, 2007-01 to 2026-09: real PCE (BEA and leaf Fisher), care, outside care and outside care with imputed items for every variant, imputed items, real income excluding transfers; index (Sep 2022 = 100), 1-, 6- and 12-month changes, nominal value |
| `out/care_financing.csv` | Blocks `levels` (care variants, Medicare, Medicaid, transfers, taxes, saving: start, end, increment, growth, excess over income growth), `bridge` (Table 10) and `gap` (Table 9 and the per-variant rows) |
| `out/care_share_history.csv` | Care (a+), (b), (c) by calendar year 1990-2025 and five multi-year spans |
| `out/jobs_watch_windows.csv` | Job changes and care shares from the watch page's chart data |
| `out/published_comparison.csv`, `out/published_comparison_windows.csv` | Our contributions against Tables 2.3.2, 2.4.2 and 2.8.2, per period and chained over the windows |
| `out/leaf_fisher_vs_bea.csv` | The leaf-Fisher index against BEA's real PCE, every month 1959-2026 and year 1960-2025 |
| `out/notes_tables_sectors.md` | The tables above, as generated |
| `figures/*.png` | The four figures |
