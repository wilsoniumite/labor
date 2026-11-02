# Q2, sectors: is care absorbing US spending growth the way it absorbs job growth?

Question 2 of the consumption thread, sectors unit (Stella's question about the 2026-06-14 post). The watch site's
"private jobs outside care" page says health care and social assistance "have accounted for most US job growth", and
the page's own chart data put their share of net job growth above 100% over the latest two years: 113.5% from Sep 2024
to Sep 2026 (the page prints no share). The jobs window used below is Aug 2024 to Aug 2026 (107.2%). It ends in August
for a historical reason, not an analytical one: it is the window of this repository's earlier payroll finding
(`paths/STATE.md`), made when August 2026 was the latest month, and `NOTES_fingerprint.md` uses it too. Table 11a sets
the two windows side by side, and the answer does not change. Does the national-accounts breakdown of consumer
spending show the same thing?

Data: BEA's *Personal Income and Outlays, September 2026* (released 2026-10-29), monthly to 2026-09 and annual to
2025, as tidied in `consumption/data/tidy/` (see `README_bea.md`). Jobs: the watch page vendored in
`consumption/data/raw/watch/jobs-outside-care.html`. Nothing else.

Run from the repo root:

    venv/bin/python -I consumption/recent/code/sectors.py          # about 25 s: out/*.csv, figures/*.png
    venv/bin/python -I consumption/recent/checks/check_sectors.py  # about 10 s: 90 PASS/FAIL lines

## The answer in brief

1. **In volumes the breakdown has moved toward care, but far less than jobs have.** Under the broad definition (c),
   care is health care services (including the part of nonprofit health output households don't pay for), medical
   goods, net health insurance, child care and social assistance. It was 23-24% of PCE at the start of every window
   and took 36-41% of the growth of real PCE in every window from six months to four years examined here (the five in
   Table 1; 35-46% in single calendar years 2022-2025, and 26-33% for care services alone, definition (s), the closest
   match to the jobs series). In the four years to Sep 2019 it took 25.5%, about its share of the level. Health care
   and social assistance took 20.5% of net job growth in the four years to Sep 2019, 58% in the four years to Sep 2026
   and 107% in the two years to Aug 2026 (113.5% to Sep 2026). The watch page does not print these job shares. They
   are computed from its chart data: the 107% is 1,349 / (1 + 1,349 - 92) thousand jobs. Two- and four-year changes
   are sums of the page's twelve-month changes, exact only if the chart is a single data vintage.
2. **Spending outside care slowed, but it did not stall the way jobs outside care did.** Real spending outside care
   grew 4.7% in the jobs window (2.3% a year), while private jobs outside care grew by 1 thousand, that is, were flat:
   the figure is the sum of two twelve-month changes from the watch chart. Over the page's latest two years, Sep 2024
   to Sep 2026, real spending outside care grew 4.0% (2.0% a year) while private jobs outside care fell by 31 thousand
   (Table 11a). Over the four years to Sep 2026 total real PCE grew about as much as in the four years to Sep 2019
   (10.9% against 10.7%). Care's contribution rose from 2.7 to 4.5 points, so spending outside care grew 8.3% instead
   of 10.4%: about 2.0% a year instead of 2.5%, a fifth less growth over the four years.
3. **In dollars the shift since 2022 is about three quarters of the shift in volumes, and most of it recovers an
   earlier fall.** Care's share of the PCE level rose from 22.9% in Sep 2022 to 24.3% in Sep 2026 in current dollars
   (+1.40 points), against +1.81 points with both ends valued at Sep 2022 prices. That is about four and a half times
   the dollar shift of the four years to Sep 2019 (+0.31 points). But 1.2 of the 1.4 points recover a fall from Sep
   2019 to Sep 2022 (24.07% to 22.88%), which came in calendar 2021-22 (calendar-year shares 24.2% in 2020, 23.3% in
   2021 and 22.9% in 2022; Table 4 shows each as the next year's share at start). Over the four years to Sep 2022
   care's dollar share fell 1.1 points, as care prices rose 9.8% and all PCE prices 14.5%. Against Sep 2019, care's
   share of spending in Sep 2026 is up 0.2 points in dollars (24.1% to 24.3%) and 1.8 points in volumes. In the latest
   year it slipped in dollars (24.4% to 24.3%) while still rising in volumes, because care prices rose 1.9% and all
   PCE prices 3.65%.
4. **Care's share of the dollar increase is well below its share of real growth, mostly because of general
   inflation.** Care took 30% of the four-year increase in nominal spending, against 26% before the pandemic and
   23% of the level, and 41% of real growth. About half of the four-year dollar increase in PCE was higher prices,
   which add to every item's spending in proportion to its size and so pull an item's share of the increase toward
   its share of the level. Relative prices explain only 1.4 of the 11.4 points between 41% and 30% (0.2 of 9.6 on
   calendar years 2022-2025), although care's implicit prices rose 10.9% over the four years, all PCE prices 12.7%:
   had care prices risen as fast, care would have taken 31.3% of the increase. The 30% against 26% comparison is
   diluted too, by twice the pre-pandemic inflation (12.7% against 6.4% over four years). In the latest twelve
   months, with care prices further behind, relative prices explain more: 5.1 of 14.4 points.
5. **Measured from Sep 2022, the gap between spending and income opened in 2026, and most of the 2026 gap is outside
   care.** From Sep 2022 to Mar 2026 real PCE and real personal income excluding transfers grew about equally (8.9%
   against 8.8%, after income had run up to 2.2 points ahead in early 2024). In the accounts, care's growth beyond
   that of non-transfer income added 1.67 points to the gap and spending outside care, growing less than income, took
   1.55 points off it (Table 9a). This is an accounting split; it does not show that one caused the other. Real PCE
   rose 1.82% in the six months to Sep 2026 against 0.05% for real personal income excluding transfers, which took the
   gap since Sep 2022 from 0.1 to 2.05 points. The six-month gap itself is 1.77 points in volumes and 1.80 in dollars.
   Care (c), whoever paid, accounts for 41% of that gap measured in volumes and 25% measured in dollars, so 59% and
   75% of it is spending outside care. Both halves of the heading depend on the starting month (Table 9a). Care (c) is
   41% (volumes) and 19% (dollars) of the twelve-month gap and 121% and 98% of the four-year gap (item 6). Measured
   from Jan 2024, when income's lead was largest, the gap is 4.2 points, 2.4 of them already open by Mar 2026, and
   care is 49% and 39% of it (56% and 50% of the part to Mar 2026). So 'opened in 2026' holds only from Sep 2022, and
   'most of it is outside care' holds for the six- and twelve-month gaps, only barely in volumes for the gap since Jan
   2024, and not over four years. Medicare and Medicaid growing faster than income accounts for 15% of the dollar gap,
   and at most 25% even if all of their increase is counted as care paid by transfers. They are an upper-bound proxy
   for government-paid care (benefits are gross of premiums, and some of the increase replaces private payment), and
   the monthly Medicare series is interpolated, so over six months this is rough. In the accounts the gap as a whole
   was financed mostly by lower saving: personal saving fell by $306 billion (annual rate), 40% of the increase in PCE
   and 80% of its excess over the increase in non-transfer income. Saving is the residual of income minus outlays, so
   this restates the gap rather than explaining it, and the identity cannot say which spending the lower saving paid
   for. Jul-Sep 2026 are advance estimates (item 8).
6. **Over the whole four years care's excess growth is about the size of the gap, but that adds up two different
   periods.** Real spending outgrew real non-transfer income by 2.05 points from Sep 2022 to Sep 2026. Care's excess
   growth over income was larger than the gap in volumes (121% of it) and about equal to it in dollars (98%), so
   spending outside care grew a little less than income (8.3% against 8.8%). That total is care's excess growth to Mar
   2026, netted out in the accounts by spending outside care growing less than income (an accounting split, not a
   trade-off), plus the 2026 gap, most of which is outside care (Table 9a). Medicare and Medicaid growing faster than
   income accounts for two thirds of the dollar gap over the four years (item 5's upper-bound caveat applies). On
   calendar-year averages 2022 to 2025, spending grew *less* than non-transfer income (8.03% against 8.72%).
7. **Imputed items do not change the picture.** These are imputed rent, the rental value of farm dwellings (built
   partly from actual rents), financial services furnished without payment and nonprofits' own consumption. Taking
   them out as well moves outside-care growth by less than 0.1 point over four years (8.26% either way), and by 0.07
   point in the watch window. The largest move under (c) is 0.25 point in the jobs window (4.97% instead of 4.73%).
   Under the narrowest care definition (a) the moves reach 0.38 point over four years and 0.40 point on calendar
   years 2022-2025 (Table 3).
8. **The latest months are not independent evidence.** For the current quarter, BEA estimates spending on hospitals,
   nursing homes, paramedical services and most social services, and nonprofit health output, from BLS employment,
   hours and earnings (with trade-source volume or nursing-home occupancy data for some); physician services, child
   care and net health insurance from judgmental trends; and medical goods from monthly retail sales (NIPA Handbook
   ch. 5, Tables 5.A and 5.B). That is the same CES survey behind the watch site's jobs series. July to September 2026
   are advance estimates of this kind. The lines built from CES data are 57% of care (c) spending in Sep 2026 and the
   judgmental trends 23% (Table 12). In Jul-Sep the CES-based lines gave 0.10 of care's 0.29 points of real PCE
   growth, the judgmental trends 0.05 and medical goods 0.13: about a third of care's growth in those months echoes
   the jobs data.

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
  increase" is its dollar increase divided by the increase in PCE. Table 1a adds the share of the level at the end
  of the window, in current dollars and with both ends valued at start-of-window prices.
- **Group growth.** The real growth of a group (care, outside care, a line) is its own Fisher index built from its
  components the same way. For lines 145 and 333 (nets of two flows) BEA publishes no index and none is reported.

**Residuals against BEA's own real PCE.** The leaf-Fisher index reproduces BEA's annual real PCE growth in every
year 2008-2025 to within 0.0003 points, and the 2.4.3U index to within 0.0034 points in every year since 1960.
Monthly, it differs from BEA's chained-dollar real PCE by at most 0.007 points a month since 2022 (mean -0.0009).
The differences are smooth, not random. That fits the Handbook's description that quarterly chain indexes are
"adjusted so that the quarterly indexes average to the corresponding annual index". The monthly published indexes
evidently carry a similar adjustment, and the published detail is rounded. Over the windows the residuals are
+0.010 to +0.016 points of growth that is 1.8% to 10.9%, and zero for the annual window (Table R). Over Table 4's
monthly context windows they are larger: +0.044 points for Sep 2015 to Sep 2019, and +0.423 points for Sep 2018 to
Sep 2022, where the unadjusted chain drifts across 2020. Table 4 shows BEA's growth and care's share of it beside
them. The group tables carry the residual as its own row. Shares of growth are of the leaf-Fisher total, so they add
to 100.

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
  the quantity relative implied by 2.4.5U / 2.4.4U is not exactly the 2.4.3U relative. In the month-to-month
  changes from Jan 2022 to Sep 2026 the two differ by at most 0.43% (passenger fares for foreign travel, line 335,
  Dec 2021 to Jan 2022). Over 2007-2026 the largest gaps come with the 2020 travel collapse (3.7% for line 340 in
  May 2020). Per leaf: `out/leaf_vp_vs_q.csv`.
- **Quantity relatives.** Using 2.4.3U quantity relatives instead of 2.4.4U prices moves total growth by at most
  0.007 points and the care (c) contribution by at most 0.0004 points.

**Jobs.** The watch page embeds its chart data, twelve-month changes in thousands for private jobs outside health care
and social assistance, health care and social assistance, and government (BLS via FRED). Changes over two or four
years are sums of the twelve-month changes ending in each year. Those cover the jobs, twelve-month and four-year
windows, and the four years to Sep 2019 for context. A sum equals the change between its end months only if every
point on the chart comes from one data vintage. The page does not say which vintage its chart uses (its trigger
history uses the data as published at each date). The six-month and calendar-year windows cannot be built from
twelve-month changes, so they have no jobs figure. The page's text says health care and social assistance "have
accounted for most US job growth". It does not print the 107%, which is derived here from its chart data: care
+1,349k, private outside care +1k, government -92k, so 1,349 / (1 + 1,349 - 92) = 107.2%. The chart runs to Sep 2026,
so its latest two years are Sep 2024 to Sep 2026: care +1,285k, private outside care -31k, government -122k, so
113.5%. The jobs window ends in August for the historical reason given at the top (judgment call 10); Table 11a sets
the two windows side by side.

## Definitions

| Name | 2.4.5U lines | Note |
|---|---|---|
| (a) Health care services | 172 | Household purchases, including those paid by insurers, Medicare and Medicaid, and purchases from nonprofit hospitals and nursing homes (184, 188) |
| (a+) ... incl. NPISH health | 172 + (344 - 357) | Adds nonprofit health output households do not pay for (README_bea.md: "total health care services") |
| (b) + medical goods and insurance | (a+) + 121 + 66 + 275 | Pharmaceutical and other medical products; therapeutic appliances; net health insurance (275 includes income-loss and workers' compensation insurance, 277-278, as the brief specifies) |
| (c) + child care and social assistance | (b) + 316 + 317 | The main definition used in the headline and figures |
| (c+) + NPISH social services | (c) + (350 - 363) | Nonprofit social-service output households do not pay for |
| (s) care services only | (a+) + 316 + 317 + (350 - 363) | Not asked for: drops goods and insurance, which NAICS 62 workers do not produce, so it is the closest spending analogue of the jobs series |
| Imputed and non-cash items | 160 + 163 + 254 + 342 | Owner-occupied nonfarm imputed rent, rental value of farm dwellings (163; BEA builds it from actual and imputed farm rents), financial services furnished without payment, NPISH final consumption |
| Outside care (k) | PCE minus care (k) | A Fisher index of the remaining leaves |
| Excl. care (k) and imputed items | PCE minus care (k) minus imputed items | The overlap (NPISH health and social services are inside 342) is excluded once, so (a) and (a+) give the same series, as do (c) and (c+) |

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

| Window | Real PCE growth, % (BEA) | Care (c) share of PCE at start, % | Care (c) contribution, pp | Care (c) share of real growth, % | Care (c) share of the nominal increase, % | Care (c) real growth, % | Prices: care (c) / all PCE, % | Outside care (c) real growth, % (annualized) | Excl. care (c) and imputed items, real growth, % | Real income excl. transfers, % | Care share of net job growth, % (computed from the watch page's chart data) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Aug 2024 to Aug 2026 (jobs window) | 5.62 | 24.0 | 2.02 | 35.9 | 26.7 | 8.43 | 4.75 / 6.23 | 4.73 (2.3) | 4.97 | 2.69 | 107.2 |
| 12 months to Sep 2026 | 2.54 | 24.4 | 0.93 | 37.0 | 22.7 | 3.86 | 1.90 / 3.65 | 2.09 (2.1) | 2.02 | 0.54 | 104.8 |
| 6 months to Sep 2026 (watch window) | 1.82 | 24.3 | 0.74 | 40.8 | 24.8 | 3.06 | 0.50 / 1.65 | 1.41 (2.8) | 1.48 | 0.05 |  |
| 4 years to Sep 2026 | 10.87 | 22.9 | 4.48 | 41.3 | 29.9 | 19.63 | 10.87 / 12.74 | 8.26 (2.0) | 8.26 | 8.82 | 58.4 |
| 2022 to 2025 (annual data) | 8.03 | 22.9 | 3.31 | 41.2 | 31.6 | 14.49 | 9.15 / 9.33 | 6.11 (2.0) | 6.10 | 8.72 |  |

The jobs share for the six-month and calendar-year windows cannot be built from the page's twelve-month changes.

**Table 1a. Care (c) in dollars: its share of the PCE level at both ends of each window, and its share of the dollar
increase.** "At start-of-window prices" values the end-of-window volumes of care and of PCE at start prices,
s0 (1 + care real growth) / (1 + PCE real growth) on the leaf Fisher. "Same at all-PCE price growth" is care's share
of the dollar increase had care prices risen as fast as all PCE prices, with care's real growth and everything else
as published. The gap between care's shares of real growth and of the dollar increase then splits into general
inflation (share of real growth minus that counterfactual) and care's relative prices (the rest).

| Window | Share of PCE at start, % | Share of PCE at end, % (change, pt) | Share at end at start-of-window prices, % (change, pt) | Share of real growth, % | Share of the nominal increase, % | Same at all-PCE price growth, % | Real minus nominal share, pp = general inflation + relative prices | Prices: care (c) / all PCE, % |
|---|---|---|---|---|---|---|---|---|
| Aug 2024 to Aug 2026 (jobs window) | 24.03 | 24.33 (+0.29) | 24.67 (+0.64) | 35.9 | 26.7 | 29.0 | 9.2 = 7.0 + 2.2 | 4.75 / 6.23 |
| 12 months to Sep 2026 | 24.37 | 24.27 (-0.10) | 24.69 (+0.32) | 37.0 | 22.7 | 27.8 | 14.4 = 9.3 + 5.1 | 1.90 / 3.65 |
| 6 months to Sep 2026 (watch window) | 24.26 | 24.27 (+0.02) | 24.55 (+0.30) | 40.8 | 24.8 | 30.5 | 16.1 = 10.4 + 5.7 | 0.50 / 1.65 |
| 4 years to Sep 2026 | 22.88 | 24.27 (+1.40) | 24.69 (+1.81) | 41.3 | 29.9 | 31.3 | 11.4 = 10.0 + 1.4 | 10.87 / 12.74 |
| 2022 to 2025 (annual data) | 22.89 | 24.22 (+1.33) | 24.26 (+1.37) | 41.2 | 31.6 | 31.7 | 9.6 = 9.5 + 0.2 | 9.15 / 9.33 |
| 4 years to Sep 2019 (pre-pandemic) | 23.76 | 24.07 (+0.31) | 23.91 (+0.15) | 25.5 | 25.8 | 25.0 | -0.3 = 0.5 - 0.8 | 7.14 / 6.41 |
| 4 years to Sep 2022 | 23.98 | 22.88 (-1.11) | 23.95 (-0.03) | 23.4 | 18.9 | 22.4 | 4.5 = 1.0 + 3.5 | 9.81 / 14.54 |
| 7 years to Sep 2026 (from pre-pandemic) | 24.07 | 24.27 (+0.21) | 25.91 (+1.84) | 33.6 | 24.7 | 27.8 | 8.9 = 5.8 + 3.2 | 19.90 / 27.50 |

Before the pandemic the two shares were about equal (25.5% real, 25.8% nominal) for two reasons. Care's real share
was close to its level share (23.8%), so inflation had little to pull, and care prices rose a little faster than all
PCE prices (7.1% against 6.4%), which lifted its dollar share. The four years to Sep 2022 are the reverse: care
prices rose 9.8% against 14.5%, and care's dollar share fell 1.1 points while its volume share was flat.

**Table 2. Care's share of real PCE growth, % (share of PCE at the start of the window, %), by definition.**

| Care definition | Aug 2024 to Aug 2026 (jobs window) | 12 months to Sep 2026 | 6 months to Sep 2026 (watch window) | 4 years to Sep 2026 | 2022 to 2025 (annual data) |
|---|---|---|---|---|---|
| (a) Health care services, households (172) | 25.3 (16.9) | 23.0 (17.2) | 29.6 (17.1) | 31.8 (15.9) | 34.1 (15.9) |
| (a+) Health care services incl. NPISH health (172 + 344 - 357) | 25.2 (17.3) | 25.8 (17.5) | 26.9 (17.5) | 30.8 (16.3) | 31.4 (16.3) |
| (b) (a+) + medical products, appliances, net health insurance (121, 66, 275) | 34.1 (22.6) | 36.1 (22.9) | 38.5 (22.8) | 40.0 (21.5) | 39.7 (21.5) |
| (c) (b) + child care and social assistance (316, 317) | 35.9 (24.0) | 37.0 (24.4) | 40.8 (24.3) | 41.3 (22.9) | 41.2 (22.9) |
| (c+) (c) + NPISH social services (350 - 363) | 36.3 (24.6) | 36.7 (25.0) | 40.1 (24.9) | 41.7 (23.5) | 41.8 (23.5) |
| (s) Care services only: (a+) + 316 + 317 + (350 - 363) | 27.4 (19.3) | 26.4 (19.6) | 28.5 (19.6) | 32.5 (18.3) | 33.5 (18.3) |

**Table 3. Real growth of PCE outside care / excluding both care and imputed items, %, by definition.**

| Care definition | Aug 2024 to Aug 2026 (jobs window) | 12 months to Sep 2026 | 6 months to Sep 2026 (watch window) | 4 years to Sep 2026 | 2022 to 2025 (annual data) |
|---|---|---|---|---|---|
| (a) Health care services, households (172) | 5.04 / 5.39 | 2.34 / 2.25 | 1.54 / 1.72 | 8.79 / 9.17 | 6.28 / 6.68 |
| (a+) Health care services incl. NPISH health (172 + 344 - 357) | 5.08 / 5.39 | 2.27 / 2.25 | 1.60 / 1.72 | 8.98 / 9.17 | 6.57 / 6.68 |
| (b) (a+) + medical products, appliances, net health insurance (121, 66, 275) | 4.77 / 5.03 | 2.09 / 2.01 | 1.44 / 1.52 | 8.29 / 8.29 | 6.15 / 6.15 |
| (c) (b) + child care and social assistance (316, 317) | 4.73 / 4.97 | 2.09 / 2.02 | 1.41 / 1.48 | 8.26 / 8.26 | 6.11 / 6.10 |
| (c+) (c) + NPISH social services (350 - 363) | 4.74 / 4.97 | 2.12 / 2.02 | 1.44 / 1.48 | 8.27 / 8.26 | 6.10 / 6.10 |
| (s) Care services only: (a+) + 316 + 317 + (350 - 363) | 5.05 / 5.35 | 2.31 / 2.26 | 1.61 / 1.69 | 8.98 / 9.15 | 6.54 / 6.65 |

**Table 4. Context: care (c) year by year and over earlier four-year spans.** Annual rows are calendar years on
annual data; the "share of PCE at start" is the previous year's. The last two columns put BEA's own real PCE growth
beside the leaf Fisher (the residual is BEA minus leaf) and give care's share of BEA's growth. The annual rows agree
to the third decimal. The monthly rows carry the unadjusted chain's residual, which is largest across 2020: for
Sep 2018 to Sep 2022 care's 23.4% share of leaf-Fisher growth is 22.6% of BEA's.

| Period | Real PCE growth, % | Care (c) share of PCE at start, % | Care (c) contribution, pp | Care (c) share of real growth, % | Care (c) share of the nominal increase, % | Care (a+) share of real growth, % | Outside care (c) real growth, % | Real income excl. transfers, % | BEA real PCE growth, % (residual, pp) | Care (c) share of BEA's real growth, % |
|---|---|---|---|---|---|---|---|---|---|---|
| 2011 | 1.70 | 23.0 | 0.50 | 29.3 | 22.9 | 21.8 | 1.56 | 4.39 | 1.70 (0.000) | 29.3 |
| 2012 | 1.37 | 23.0 | 0.34 | 25.0 | 23.7 | 29.7 | 1.33 | 3.58 | 1.37 (0.000) | 25.0 |
| 2013 | 1.74 | 23.0 | 0.39 | 22.1 | 21.1 | 11.1 | 1.76 | -0.54 | 1.74 (0.000) | 22.1 |
| 2014 | 2.83 | 22.9 | 0.77 | 27.1 | 26.0 | 13.4 | 2.68 | 3.69 | 2.83 (0.000) | 27.1 |
| 2015 | 3.37 | 23.1 | 1.04 | 30.8 | 37.9 | 23.7 | 3.04 | 4.27 | 3.37 (0.000) | 30.8 |
| 2016 | 2.45 | 23.6 | 0.70 | 28.4 | 32.4 | 24.9 | 2.30 | 1.49 | 2.45 (0.000) | 28.4 |
| 2017 | 2.64 | 23.9 | 0.52 | 19.9 | 22.0 | 15.1 | 2.78 | 3.51 | 2.64 (0.000) | 19.9 |
| 2018 | 2.74 | 23.8 | 0.79 | 28.9 | 25.7 | 16.3 | 2.56 | 3.28 | 2.74 (0.000) | 28.9 |
| 2019 | 2.15 | 23.9 | 0.66 | 30.5 | 28.9 | 24.6 | 1.96 | 3.09 | 2.15 (0.000) | 30.5 |
| 2020 | -2.52 | 24.1 | -0.64 | 25.3 | 13.7 | 33.9 | -2.48 | 0.07 | -2.52 (0.000) | 25.3 |
| 2021 | 8.84 | 24.2 | 1.56 | 17.7 | 16.4 | 13.5 | 9.58 | 5.17 | 8.84 (0.000) | 17.7 |
| 2022 | 2.91 | 23.3 | 1.01 | 34.6 | 18.7 | 25.8 | 2.47 | 0.35 | 2.91 (0.000) | 34.6 |
| 2023 | 2.30 | 22.9 | 1.06 | 46.1 | 29.6 | 34.7 | 1.60 | 3.65 | 2.30 (0.000) | 46.1 |
| 2024 | 2.90 | 23.3 | 1.18 | 40.9 | 34.2 | 33.0 | 2.23 | 3.00 | 2.90 (0.000) | 40.9 |
| 2025 | 2.63 | 23.9 | 0.99 | 37.5 | 31.0 | 27.1 | 2.16 | 1.83 | 2.63 (0.000) | 37.5 |
| 2010 to 2019 | 23.05 | 23.0 | 6.26 | 27.2 | 26.7 | 19.7 | 21.82 | 30.05 | 23.05 (0.000) | 27.2 |
| 2015 to 2019 | 10.36 | 23.6 | 2.78 | 26.8 | 26.8 | 19.9 | 9.94 | 11.85 | 10.36 (0.000) | 26.8 |
| 2015-09 to 2019-09 | 10.65 | 23.8 | 2.72 | 25.5 | 25.8 | 18.7 | 10.42 | 11.78 | 10.69 (+0.044) | 25.4 |
| 2018-09 to 2022-09 | 11.46 | 24.0 | 2.69 | 23.4 | 18.9 | 14.8 | 11.54 | 8.93 | 11.88 (+0.423) | 22.6 |
| 2022-09 to 2026-09 | 10.85 | 22.9 | 4.48 | 41.3 | 29.9 | 30.8 | 8.26 | 8.82 | 10.87 (+0.016) | 41.2 |

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

The row is n/a where the gap is not positive (calendar 2022-2025). In the code the cut-off is a gap of 0.25 points;
no window in Table 9 falls between 0 and 0.25.

**Table 9a. When the gap opened, and how its split depends on the starting month: care (c) and the rest.** The same
arithmetic as Table 9, with the real gap split on the leaf Fisher. Jan 2024 is the month in which income's lead over
spending, measured from Sep 2022, was largest (-2.22 points), so the windows that start there give the largest gap to
Sep 2026. Shares are n/a where the gap is under 0.25 points.

| Period | Real PCE growth, % (BEA) | Real income excl. transfers, % | Real gap, pp (BEA) | Real gap, pp (leaf Fisher) | Care (c) part, volumes, pp | Outside care part, volumes, pp | Care (c) share, volumes, % | Nominal gap, pp | Care (c) part, dollars, pp | Outside care part, dollars, pp | Care (c) share, dollars, % |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Sep 2022 to Mar 2026 | 8.89 | 8.76 | 0.13 | 0.12 | 1.67 | -1.55 | n/a | 0.14 | 1.70 | -1.56 | n/a |
| Jan 2024 to Mar 2026 (from income's largest lead) | 5.90 | 3.54 | 2.36 | 2.36 | 1.31 | 1.05 | 55.7 | 2.52 | 1.25 | 1.26 | 49.9 |
| Sep 2022 to Sep 2026 (4 years) | 10.87 | 8.82 | 2.05 | 2.04 | 2.46 | -0.43 | 121.0 | 2.31 | 2.28 | 0.04 | 98.4 |
| Jan 2024 to Sep 2026 (from income's largest lead) | 7.83 | 3.59 | 4.24 | 4.22 | 2.08 | 2.14 | 49.3 | 4.58 | 1.79 | 2.80 | 39.0 |
| Sep 2025 to Sep 2026 (12 months) | 2.54 | 0.54 | 1.99 | 1.98 | 0.80 | 1.18 | 40.5 | 2.07 | 0.40 | 1.67 | 19.2 |
| Mar 2026 to Sep 2026 (watch window) | 1.82 | 0.05 | 1.77 | 1.76 | 0.73 | 1.03 | 41.3 | 1.80 | 0.45 | 1.34 | 25.2 |

Measured from Sep 2022 (BEA real PCE against real income excluding transfers, both indexed to Sep 2022), the
cumulative real gap was negative through most of 2023-2025, lowest at -2.22 points in Jan 2024. It stayed between
-0.31 and +0.13 points from Sep 2025 to Mar 2026 and reached 2.05 points in Sep 2026 (`out/outside_care_monthly.csv`).
Measured from Jan 2024 instead, spending outgrew income by 2.0 points during 2024, stayed 1.1 to 2.4 points ahead
through Mar 2026 and was 4.2 points ahead by Sep 2026. So 'the gap opened in 2026' describes the Sep 2022 base:
measured from Jan 2024, about half of it opened in 2024.

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

**Table 11a. The jobs window against the page's latest two years: jobs (thousands; twelve-month changes summed)
and spending over the same months, care (c).** The same arithmetic as Tables 1 and 11.

| Window | Private outside care, thousands | Health care and social assistance, thousands | Government, thousands | Care share of net job growth, % | Real PCE growth, % (BEA) | Care (c) share of real growth, % | Outside care (c) real growth, % (annualized) | Real income excl. transfers, % |
|---|---|---|---|---|---|---|---|---|
| Aug 2024 to Aug 2026 (jobs window) | +1 | +1349 | -92 | 107.2 | 5.62 | 35.9 | 4.73 (2.3) | 2.69 |
| Sep 2024 to Sep 2026 (the page's latest two years) | -31 | +1285 | -122 | 113.5 | 5.03 | 39.5 | 3.98 (2.0) | 2.30 |

**Table 12. Care (c) by the indicator BEA uses for the current quarter's advance estimate (NIPA Handbook ch. 5,
Tables 5.A and 5.B; nonprofits from the chapter's technical note).** Jul-Sep 2026 are advance estimates.
Contributions are to real PCE growth over the three advance months (Jun to Sep 2026) and over the watch window; the
shares are of care's own level and contribution. Every care (c) line is in exactly one row.

| Indicator for the advance estimate (Handbook ch. 5) | Care (c) lines | Share of care (c) spending, Sep 2026, % | Contribution to real PCE growth, Jul-Sep 2026, pp (share of care's, %) | Contribution, Mar to Sep 2026 (watch window), pp (share of care's, %) |
|---|---|---|---|---|
| CES employment, hours and earnings | paramedical services (176) and hospitals (183), with trade-source volume data; nursing homes (187), with CMS occupancy data; social assistance (317; 'most components'); NPISH health (344 - 357; 'based primarily on' CES) | 56.9 | 0.099 (34.5) | 0.410 (55.5) |
| Judgmental trend | physician services (174), child care (316), net health insurance (275) | 23.3 | 0.050 (17.5) | 0.154 (20.9) |
| Monthly retail sales (Census MRTS) | pharmaceutical and other medical products (121), therapeutic appliances and equipment (66) | 16.0 | 0.132 (46.3) | 0.206 (27.9) |
| Dental patient volumes (American Dental Association) | dental services (175) | 3.8 | 0.005 (1.7) | -0.032 (-4.3) |
| Care (c) | all of care (c) | 100.0 | 0.286 (100.0) | 0.739 (100.0) |

**Figures** (`figures/`, 200 dpi):

- `fig_care_share_of_growth.png`: care's share of real PCE growth against its share of the level, by window, for
  definitions (a+), (b) and (c), with the share of net job growth computed from the watch page's chart data.
- `fig_outside_care.png`: real PCE, real PCE outside care (c), real PCE excluding both care (c) and imputed items,
  and real income excluding transfers, Sep 2022 = 100.
- `fig_contributions_2024-08_2026-08.png` and `fig_contributions_2022-09_2026-09.png`: contributions by part of
  care and by function outside it.

## What it means, in plain words

Care is taking a bigger slice of real spending growth than it used to. Before the pandemic it took about a quarter,
roughly its weight in the budget. Since 2022 it has taken 36-41% of real growth in each of the five windows examined
here (35-46% in single calendar years 2022-2025, and 26-33% for care services only, definition (s), the closest match
to the jobs series), and its own volume has grown about 4.6% a year against about 2% for everything else. So the
spending data do lean the same way as the jobs data, toward health care, drugs and care services.

But the lean is much milder than in jobs. Outside care, real spending kept growing at about 2% a year. That is below
its pre-pandemic pace of 2.5%, a fifth less growth over four years, but it is not a stall. Over the last year it even
outgrew real non-transfer income by a wide margin (2.1% against 0.5%). Private employment outside care was flat over
the two years to Aug 2026 (+1 thousand, summed from the watch page's twelve-month changes; -31 thousand to Sep 2026)
and grew 192 thousand over the year to Sep 2026.

In money terms the answer depends on where you start. Since Sep 2022 care's share of consumer spending has risen 1.4
points, to 24.3%, three quarters of its rise in volumes. But care got relatively cheaper in the 2021-22 inflation and
its dollar share fell by almost as much before that, so it is now only 0.2 points above Sep 2019. Care's 30% share of
the four-year dollar increase says little either way: about half of that increase was inflation, which lands on
every item in proportion to its size and pulls each item's share of the increase toward its share of spending.

On the watch site's spending-and-income gap, the answer depends on the month you start from. From Sep 2022 to Mar 2026
spending and non-transfer income grew about equally: care grew faster than income and the rest of spending more
slowly, and in the accounts the two netted out, which does not show that one paid for the other. Measured from Sep
2022, the gap opened in the six months to Sep 2026. Care accounts for 25% (in dollars) to 41% (in volumes) of that
six-month gap; the rest, 59% in volumes and 75% in dollars, is spending outside care. Medicare and Medicaid growing
faster than income account for 15% of the dollar gap, or 25% if all of their increase is counted. They are an
upper-bound proxy for government-paid care, and the monthly Medicare series is interpolated, so over six months this
is rough. Measured from Jan 2024, when income was furthest ahead, spending has outgrown income by 4.2 points, about
half of it during 2024, and care is 49% of that in volumes and 39% in dollars. Over the full four years care is more
than all of it. Three of the six months to Sep 2026 are advance estimates in which much of care spending (57%) is
extrapolated from the same CES jobs data, and as item 8 shows, those lines gave about a third of care's growth in the
three months. So this split is not independent of the jobs figures, and it will be revised from 2026-11-25.

In the accounts, lower measured saving covers 80% of the rise in spending above non-transfer income over the six
months to Sep 2026 ($306 of $382 billion at annual rates). Saving is the residual of income minus outlays, so it
carries the revisions to both, and this restates the gap rather than explaining it. The accounts cannot say whether
the lower saving paid for care or for anything else.

## Caveats

- **The detail is weaker than the totals.** BEA warns, of the 2.4.5U detail used here (NIPA Handbook ch. 5): "BEA
  does not include these detailed estimates in the published tables because their quality is significantly lower
  than that of the higher-level categories of which they are a part. In particular, these detailed estimates are
  more likely to be based on judgmental trends or on less reliable source data." The care groups are mostly whole
  published categories (health care 172 is a Table 2.3.5 line), but variant (c) and the parts in Table 7 rest on
  U detail.
- **Recent care spending is partly built from employment.** Handbook ch. 5, Tables 5.A and 5.B (current quarterly
  estimates):
  - Hospitals, nursing homes, paramedical services and private social services: the advance estimate (and the
    second, for social services) uses "CES data on employment, hours, and earnings", with trade-source volume data
    (hospitals, paramedical services) or CMS nursing-home occupancy data.
  - Nonprofit output, including NPISH health: the second and advance estimates are "based primarily on CES data on
    employment, hours, and earnings" (the chapter's technical note on NPISHs).
  - Physician services, child care and net health insurance: judgmental trends.
  - Medical goods: monthly retail sales (Census MRTS). Dental services: American Dental Association patient volumes.
  - The Census Quarterly Services Survey arrives with the later estimates.
  - For services without such indicators, real spending is extrapolated "using the rate of change in population
    and a projected rate of change in real per capita consumption".

  The 2026 Q3 months (Jul-Sep) are advance estimates. So for the latest quarter the care share of spending growth
  is partly an echo of the jobs data, not an independent confirmation; Table 12 says how much of care's level and of
  its Jul-Sep growth comes from each kind of indicator. Revisions (2026-11-25 and later) will replace these with
  receipts data.
- **The real/nominal split for care depends on its price measures.** These are PPIs for physicians, hospitals,
  nursing care and home health; the CPI for child care; and a BEA input-cost index for other social services
  (Table 5.B). They decide how much of care's dollar growth counts as volume, and so care's share of real growth.
  Over the four years they are not what separates that share (41%) from care's share of the dollar increase (30%):
  relative prices account for 1.4 of the 11.4 points, general inflation for the rest (Table 1a). Over longer spans
  they matter more. Since Sep 2019 care prices rose 19.9% and all PCE prices 27.5%, which is why care's dollar share
  is only 0.2 points above Sep 2019 while its volume share is 1.8 points above.
- **The monthly residual is BEA's temporal adjustment.** Our monthly Fisher chain is the unadjusted one, so
  window totals sit 0.010-0.016 points below BEA's published real PCE (Table R). Table 4's monthly context rows sit
  further below it: 0.044 points for Sep 2015 to Sep 2019 and 0.423 points for Sep 2018 to Sep 2022, where the
  chain drifts across 2020. On BEA's totals their care (c) shares of growth are 25.4% and 22.6%, not 25.5% and 23.4%
  (Table 4, last columns). The detail-line growth rates in the per-line files are our chain's; BEA's own 2.4.3U
  growth is shown beside them.
- **Nets of two flows.** NPISH health (344 - 357) and NPISH social services (350 - 363) are each gross output
  minus sales. The net is about 5% of the gross flows for health and about half for social services. Their
  contributions are well defined, but their own real growth (for example -29% for NPISH health over four years) is
  not robust. Net foreign travel (333) has no real growth at all.
- **Two small mapping points.** Health care (172) includes nonresidents' medical spending in the US, which BEA takes
  out of PCE in net foreign travel (line 340, medical expenditures of foreigners; the entry "negates the expenditures
  by foreign residents that are embedded in the source data", Handbook ch. 5). So care includes 0.003-0.006% of PCE
  that residents do not consume; line 340 contributes under 0.003 points in every window, which moves care's share
  of growth by at most 0.03 points. The rental value of farm dwellings (163, 0.14% of PCE) is in the imputed set,
  but BEA builds it from "actual and imputed farm average rents" (Table 5.B), so it is mostly, not wholly, imputed.
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
- **The data will be revised.** Vintage: the 2026-10-29 release. The October data come on 2026-11-25. Personal
  saving is income minus outlays, so it carries the revisions to both (item 5 and Table 10 read it only as an
  identity). The distributional files are an older vintage and are not used here.

## Judgment calls

1. **Prices from 2.4.4U, with q = v / p.** The brief allows 2.4.4U prices or 2.4.3U quantities. The alternative
   changes nothing that matters (check H1).
2. **The care definitions build on (a+).** (b) and (c) build on (a+), which includes NPISH health, not on (a).
   (a) alone is reported in every table. (s) is added as the closest analogue of the jobs series.
3. **Farm dwellings are imputed but not functional imputed rent.** Rental value of farm dwellings (163) is in the
   imputed set, although BEA builds it from actual as well as imputed farm rents, so it is mostly, not wholly,
   imputed (0.14% of PCE). In the functional split, "imputed rent" is line 160 only, and 163 stays in housing and
   utilities.
4. **Other services exclude net foreign travel.** The functional "other services" group is line 280 without net
   foreign travel (333), which the brief lists separately. In BEA's Table 2.3.5, other services includes it.
5. **The residual is a separate row.** Window contributions add to the leaf-Fisher total, and the residual against
   BEA is reported as its own row, not spread over the components.
6. **Jobs over longer windows are summed.** Two- and four-year job changes are sums of twelve-month changes from
   the watch page, exact only if its chart is a single data vintage. The six-month and calendar-year windows have no
   jobs figure. Why the two-year window ends in August: judgment call 10.
7. **Gap shares need a clearly positive gap.** They are left blank where the gap is under 0.25 points, which in
   these windows means where it is not positive.
8. **NOTES embeds generated tables and passages.** The results tables are generated by `sectors.py`
   (`out/notes_tables_sectors.md`) and pasted here; check G1 fails if they drift apart. So are the passages with new
   or corrected numbers (`out/notes_text_sectors.md`): the opening paragraph, items 1, 2, 3, 5, 6 and 8 of the answer
   in brief, the Jobs paragraph of the Method, the heading of Table 9a and the paragraph after it, the first, second,
   fourth and fifth plain-words paragraphs, and judgment call 10. Each of their numbers is read back from the CSVs
   and rounded once, and the words that describe a number ('a fifth', 'two thirds', 'barely') are asserted against
   it in `sectors.py`. Check G3 fails if a passage here differs from its generated text. To change one, edit
   `sectors.py` and paste the new output.
9. **One extra fetch.** NIPA Handbook ch. 4 (Estimating Methods) was fetched through `common.fetch()` into
   `consumption/data/raw/bea/nipa/`, with its manifest row added, for the contributions formula and the
   temporal-adjustment text. No other download was made.
10. **The jobs window ends in August.** Aug 2024 to Aug 2026 is the window of this repository's earlier payroll
    finding (`paths/STATE.md`), made when August 2026 was the latest month; `NOTES_fingerprint.md` and the independent
    verifier use it too, so it is kept. The page's chart runs to Sep 2026. Over Sep 2024 to Sep 2026 care's share of
    net job growth is 113.5% instead of 107.2%, its share of real PCE growth 39.5% instead of 35.9%, and real spending
    outside care grew 4.0% instead of 4.7% (Table 11a).

## Files

| File | What |
|---|---|
| `code/sectors.py` | Everything: the Fisher engine, windows, groups, financing, jobs, published comparisons, figures, these tables |
| `checks/check_sectors.py` | 90 independent checks (relative-form recomputation, identities, BEA's published numbers, the watch figures and the page's latest two years, care in dollars, the timing of the gap and its dependence on the starting month, care by advance-estimate indicator, the notes tables and generated passages, figure dpi) |
| `out/sector_contributions_<start>_<end>.csv` | One row per 2.4.5U line published at both ends of the window (366 of lines 1-368: 157-158 end in 2001): label, level, parent, leaf flag, sign, functional group, care tags (yes/part/no per variant), imputed tag, signed start and end nominal values, start share, real growth (ours and BEA's 2.4.3U), contribution (pp), share of growth (%) |
| `out/sector_groups_<start>_<end>.csv` | One row per group: kind, definition (lines), number of leaves, start and end nominal values, start share, nominal and real growth, annualized real growth, contribution, share of growth, note; plus BEA's real PCE and the residual |
| `out/headline_sectors.csv` | Per window and care variant: shares of level, growth and nominal increase, care and outside-care growth, prices, real income, jobs shares |
| `out/care_dollar_shares.csv` | Per window (the five, the four years to Sep 2019 and to Sep 2022, and the seven years from Sep 2019) and care variant: share of PCE at both ends in current dollars and at start-of-window prices, shares of real growth and of the dollar increase, the dollar share had care prices risen as fast as all PCE prices, and the split into general inflation and relative prices (Table 1a) |
| `out/outside_care_monthly.csv` | Long format, 2007-01 to 2026-09: real PCE (BEA and leaf Fisher), care, outside care, and PCE excluding both care and imputed items for every variant, imputed items, real income excluding transfers; index (Sep 2022 = 100), 1-, 6- and 12-month changes, nominal value |
| `out/care_financing.csv` | Blocks `levels` (care variants, Medicare, Medicaid, transfers, taxes, saving: start, end, increment, growth, excess over income growth), `bridge` (Table 10) and `gap` (Table 9 and the per-variant rows) |
| `out/gap_timing.csv` | Real and nominal spending-income gaps and their care (c) and outside-care parts, from Sep 2022 (to Mar and Sep 2026), from Jan 2024, the month of income's largest lead (to Mar and Sep 2026), and over twelve and six months (Table 9a) |
| `out/care_share_history.csv` | Care (a+), (b), (c) by calendar year 1990-2025 and five multi-year spans |
| `out/care_share_history_bea.csv` | The same periods against BEA's chained-dollar real PCE (from 2008): BEA's growth, the residual of the leaf Fisher, care's share of BEA's growth (Table 4's last columns) |
| `out/jobs_watch_windows.csv` | Job changes and care shares from the watch page's chart data |
| `out/jobs_windows_compare.csv` | The jobs window (Aug 2024 to Aug 2026) beside the page's latest two years (Sep 2024 to Sep 2026): job changes and care shares, and care (c)'s share of real PCE growth, care and outside-care growth and real income over the same months (Table 11a) |
| `out/care_advance_sources.csv` | Care (c) split by the indicator BEA uses for the advance estimate (Handbook Tables 5.A and 5.B): share of care spending in Sep 2026 and contributions to real PCE growth in Jul-Sep 2026 and over the watch window (Table 12) |
| `out/published_comparison.csv`, `out/published_comparison_windows.csv` | Our contributions against Tables 2.3.2, 2.4.2 and 2.8.2, per period and chained over the windows |
| `out/leaf_fisher_vs_bea.csv` | The leaf-Fisher index against BEA's real PCE, every month 1959-2026 and year 1960-2025 |
| `out/leaf_vp_vs_q.csv` | Per current leaf: the largest monthly gap between the 2.4.5U / 2.4.4U quantity relative and 2.4.3U's, since 2022-01 and since 2007-02, with its month |
| `out/notes_tables_sectors.md` | The tables above, as generated |
| `out/notes_text_sectors.md` | The passages above with new or corrected numbers, as generated (judgment call 8) |
| `figures/fig_care_share_of_growth.png`, `fig_outside_care.png`, `fig_contributions_*.png` | The unit's four figures |
