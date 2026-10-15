# What an hour's pay buys in Australia, by price category

The Australian mirror of the paper's Figure 5 (US hourly earnings deflated by the CPI for durables, food,
energy and shelter, 1964-2024). Blog-support numbers for the Austaxpolicy article: new, napkin-grade
estimates from official public data, not paper results. Built 2026-10-15; data pulled the same day.

Run, from the repository root:

    venv/Scripts/python.exe austax/paycheck/code/fetch.py     # downloads data/raw/*, writes MANIFEST.csv
    venv/Scripts/python.exe austax/paycheck/code/build.py     # writes out/*
    venv/Scripts/python.exe austax/paycheck/checks/check.py   # independent recomputation, PASS/FAIL

## Headline numbers (main series: Wage Price Index, 1998-2025)

Annual averages of complete calendar years, 2025 against 1998.

| What an hour's pay buys of ... | Change 1998-2025 |
|---|---|
| Durable goods (composite, see below) | +242% |
| Food and non-alcoholic beverages | +4% |
| Energy (electricity, gas, motor fuel) | -30% |
| Rents | +1.5% |
| All goods and services (All groups CPI) | +8.5% |

- In 2025 an hour's pay bought 3.4 times as much durable goods, relative to rented housing, as in 1998
  (ratio 3.37). The ratio is rents price growth over durables price growth: the wage cancels, so it is the
  same whichever wage series is used.
- Durables classes, same window: audio, visual and computing equipment +3,012%; small electric household
  appliances +173%; major household appliances +144%; motor vehicles +139%; furniture +78%; carpets and other
  floor coverings +15%. Durables without audio, visual and computing equipment: +113%. Composite range across
  the seven ABS weight vectors and two aggregation formulas: +221% to +268%.
- Energy classes: electricity -31%, gas and other household fuels -47%, automotive fuel -17%; household
  energy (electricity and gas) -36%.
- New dwelling purchase by owner-occupiers (a CPI class that prices the building and EXCLUDES land),
  1999-2025: -22%, against +1.0% for rents over the same years.
- Established houses (house prices including land; ABS index, not a CPI line), 2002-2021: -45%, against
  +6% for rents over the same years. Spliced long run 1998-2021: -59% (-61% if the splice is linked at 2004
  rather than 2002), against +8% for rents. Mean price of all residential dwellings, 2012-2025: -35%, against
  +5% for rents.

### Comparison wage: Average Weekly Earnings (AWE), 1995-2025

What a full-time week's ordinary pay buys, 2025 against 1995: durable goods +394% (composite range +367%
to +433%; without audio, visual and computing equipment +199%), food +30%, energy -5%, rents +26% (25.5),
All groups CPI +41%. Durables-to-rents ratio 3.94 (longer window). New dwellings 1999-2025 -6%;
established houses 2002-2021 -38%; spliced 1995-2021 -52%; mean dwelling price 2012-2025 -31%.
Over the WPI window (1998-2025) AWE gives durables +314%, food +26%, energy -15%, rents +23%.

### US over the same window, the paper's own series (context)

1998-2024 (2024 is the last complete US year: FRED has no October 2025 CPI observation). Average hourly
earnings of production and nonsupervisory workers deflated by: durables +140%, food +13%, energy -15%,
shelter +5%, rent of primary residence -5%. Durables-to-shelter ratio 2.28; durables-to-rent ratio 2.53.
Australia over the same years: WPI durables +229%, food +4%, energy -31%, rents +2.5%; ratio 3.21.

Every number is in `out/headline.csv` (metric, value, unit, period, definition, source), produced by
`code/build.py` (`add(...)` calls, lines 237-334; the main four lines and ratio at lines 237 and 240) and recomputed by `checks/check.py`.

## Sources

| Item | Source | Identifier | Raw file |
|---|---|---|---|
| Wage Price Index | ABS Data API, dataflow WPI v1.2.0 | key `1.THRPEB.7.TOT.10.AUS.Q`: quarterly index, total hourly rates of pay excluding bonuses, private and public, all industries, original, Australia | `abs_wpi_api.csv` |
| Average Weekly Earnings | ABS Data API, dataflow AWE v1.0.0 | key `3.1.3.7.TOT.10.AUS.S`: full-time adult ordinary time earnings, persons, all sectors and industries, original, May and November | `abs_awe_api.csv` |
| AWE cross-check | ABS 6302.0 May 2026, Table 3 (original) | series A85002148L | `abs_6302003_awe_original.xlsx` |
| CPI (current) | ABS Data API, dataflow CPI v2.0.0 (base Sep 2025 = 100) | key `1.<codes>.10.50.Q`: index numbers, original, weighted average of eight capital cities, quarterly | `abs_cpi_v2_index_q.csv` |
| CPI (former quarterly) | ABS Data API, dataflow CPI v1.1.0 (ends Sep qtr 2025) | same key; seam test only | `abs_cpi_v1_index_q.csv` |
| CPI weights | ABS Data API, dataflow CPI_WEIGHTS | measure 1 (percentage contribution to All groups), eight capitals, 2018-Q3 to 2024-Q4 | `abs_cpi_weights.csv` |
| Established house prices | ABS 6416.0 Residential Property Price Indexes, Dec 2021 (final), Tables 2 and 8 | A83728456R (2002-2021), A2333613R (pre-Sep 2005 method, 1986-2005) | `abs_641602_...xlsx`, `abs_641608_...xlsx` |
| Mean dwelling price | ABS Data API, dataflow RES_DWELL_ST | measure 5, Australia, quarterly, from Sep qtr 2011 | `abs_res_dwell_mean_price.csv` |
| US series | FRED | AHETPI, CUSR0000SAD, CPIUFDNS, CPIENGNS, CUSR0000SAH1 (the paper's Figure 5), CUUR0000SEHA | `fred_*.csv` |

URLs and pull dates: `data/raw/MANIFEST.csv`. Code labels: `abs_*_structure.xml`.
API base: https://data.api.abs.gov.au/rest/data/ABS,<DATAFLOW>,<version>/<key>.
ABS pages: https://www.abs.gov.au/statistics/labour/earnings-and-working-conditions/average-weekly-earnings-australia/latest-release ;
https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/residential-property-price-indexes-eight-capital-cities/latest-release

CPI codes used: 20001 Food and non-alcoholic beverages (group); 30014 Rents; 97559 New dwelling purchase by
owner-occupiers; 40055 Electricity; 115524 Gas and other household fuels; 40081 Automotive fuel; 40080 Motor
vehicles; 40058 Furniture; 131185 Carpets and other floor coverings; 40060 Major household appliances; 115484
Small electric household appliances; 40098 Audio, visual and computing equipment; 10001 All groups CPI.

## Definitions and choices

- **Main wage: WPI, not AWE.** The brief set AWE as the main series if it gave a materially longer
  window. It does not: the consistent AWE level series starts in November 1994 (first complete year 1995),
  three years before the WPI (Sep quarter 1997, first complete year 1998). The ABS also says, in its
  dataflow description (`abs_awe_structure.xml`), that AWE "is not designed to produce movement in earnings
  data"; the series exists to measure levels. The WPI is
  hourly and holds job composition fixed, so it prices an hour of a given job, the closest Australian object
  to the paper's wage. AWE is kept as the comparison series. It is closer in construction to the US average
  hourly earnings series, since both are averages whose movement includes changes in the mix of jobs. To
  lead with AWE instead, use `figure_au_paycheck_awe.png` and the `awe_*` rows.
- **No longer AWE run exists in usable form.** The current ABS 6302.0 tables start in Nov 1994. The
  archived Feb 2012 release starts in Aug 1994, and older archived releases carry no spreadsheets. RBA
  Occasional Paper 8, Table 4.17, has only a male total-earnings series, spliced by the ABS from a
  different concept before 1981/82, which ends in 1995/96. Nothing was spliced onto AWE.
- **Annual averages**: calendar years, complete years only. CPI and WPI: mean of the four quarters. AWE:
  mean of May and November, the only months the series carries for all years. Original (not seasonally
  adjusted) data throughout.
- **Index base**: 100 in the first year in which the wage and all four main deflators exist: 1998 for WPI
  and 1995 for AWE. Classes that start later are indexed to their own first complete year: new dwellings
  1999, established houses 2002, mean dwelling price 2012.
- **Durable goods composite**: six ABS CPI expenditure classes (furniture, carpets and other floor
  coverings, major household appliances, small electric household appliances, audio, visual and computing
  equipment, motor vehicles). The ABS publishes no durables aggregate. The classes are chained annually with
  fixed shares from the ABS 2018-Q3 weight vector, the earliest one in the API (`out/composite_weights.csv`):
  motor vehicles 0.43, furniture 0.22, audio, visual and computing 0.19, major appliances 0.065, small
  appliances 0.05, carpets 0.05. Sensitivity runs use each of the seven ABS weight vectors (2018-Q3 to
  2024-Q4), arithmetic and geometric chaining, and a version without audio, visual and computing.
- **Energy composite**: electricity, gas and other household fuels, and automotive fuel, with the same
  method and 2018-Q3 shares (0.38, 0.14, 0.48), mirroring the US CPI energy index (household energy plus
  motor fuel). Household energy alone is also reported.
- **CPI vintage**: through the Sep quarter 2025, the current ABS CPI (v2.0.0) quarterly series are the
  former quarterly CPI (v1.1.0) rebased to Sep 2025 = 100: every class agrees within 0.1 index points,
  the old series' last decimal. From the Dec quarter 2025 they are averages of the new complete monthly
  CPI. Both facts are checked. So the only quarter of the new measure used here is Dec quarter 2025, inside
  the 2025 average. Two tests:
  - Rerunning on the former quarterly CPI through 2024 changes every line by 0.03 points or less (a
    rebasing test).
  - Rerunning on January-September averages, which use no quarter of the new measure, moves the four
    main lines by at most 1.2 points (WPI) and 0.8 points (AWE). This is the seam test.
- **Established-house splice (comparison only)**: the pre-2005-method index is linked to the current index
  at the 2002 annual average. The seam test is 2002-2004 growth in the two indexes: the current index grew
  3.3% less. Linking at 2004 instead gives -61% rather than -59% (WPI) and -53% rather than -52% (AWE).

## Caveats a referee would raise

1. **Thirty years, not sixty.** The Australian window is 1998-2025 (WPI) or 1995-2025 (AWE). The paper's
   US numbers cover 1964-2024. Compare over the same window: in 1998-2024 the US durables-to-rent ratio
   is 2.53 and Australia's durables-to-rents ratio is 3.21.
2. **The wage choice moves every line except the ratio.** AWE rose 177% and WPI 129% over 1998-2025.
   With AWE, a week's pay buys 23% more rent and 26% more food than in 1998. With WPI, an hour of the same
   job buys about the same rent (+1.5%) and food (+4%). The gap is mostly the changing mix of jobs. The
   durables-to-rents ratio is identical under both.
3. **Weekly vs hourly.** AWE is weekly ordinary-time earnings of full-time adults; the WPI is an hourly
   rate.
4. **CPI Rents is a slow, broad measure.** It covers the whole rental stock, private and public. Market
   rents pass through gradually because "new rents account for only a portion of the existing rental stock"
   (RBA, Statement on Monetary Policy, May 2019, Box C,
   https://www.rba.gov.au/publications/smp/2019/may/box-c-housing-in-the-consumer-price-index.html). It is
   also measured after Commonwealth Rent Assistance. The ABS reported that the 15% CRA rise from 20 September
   2023 reduced that quarter's rent increase by 0.3 percentage points
   (https://www.abs.gov.au/media-centre/media-releases/cpi-rose-12-cent-september-2023-quarter). It measures
   rental housing, not the price of buying a home.
5. **New dwelling purchase excludes land.** It prices the building only; the RBA box says it is measured
   "excluding the value of the land". It is not a house price. Purchases of established dwellings are not in
   the CPI at all.
6. **House-price comparisons are not like the CPI lines.** The established house price index stopped
   after Dec quarter 2021, and its pre-2005 predecessor uses a different method (the splice is shown with
   its seam). The mean dwelling price is total value over number of dwellings: it covers all dwellings,
   units included, and is not quality-adjusted. All three include land; none is a CPI series.
7. **The durables composite is our construction.** It applies fixed 2018-era shares to the whole window.
   It is dominated by motor vehicles and by audio, visual and computing equipment. The latter's CPI price
   index fell 93% over 1998-2025 (94% over 1995-2025), largely through quality adjustment of computers and
   electronics. Each class is reported, together
   with the composite range (+221% to +268%) and the figure without that class (+113%). The basket is
   narrower than the US BLS durables index.
8. **Quality adjustment.** All CPI lines are quality-adjusted. "Buys" means constant-quality quantities.
9. **Coverage and timing.** The CPI covers the eight capital cities; the wages are national. The AWE
   annual mean (May and November) is centred about six weeks after the CPI calendar-year mean.
10. **Descriptive only.** As in the paper, the comparison is consistent with the distinction between
    produced goods and goods that need scarce inputs. It does not identify that mechanism; the rents and
    house-price lines also reflect interest rates, population growth and supply policy.

## Files

- `code/fetch.py`: downloads every raw file (requests with truststore for the proxy) and writes MANIFEST.csv.
- `code/build.py`: builds `out/annual.csv` (levels, CPI series and pay-buys indexes by year),
  `out/headline.csv`, `out/composite_weights.csv`, `out/figure_au_paycheck.png` (WPI, main) and
  `out/figure_au_paycheck_awe.png` (AWE alternative). It asserts the US loader reproduces the paper's
  1964-2024 anchors (durables 376.8, shelter 78.6).
- `checks/check.py`: re-reads the raw files with csv/openpyxl and recomputes every headline row and the
  annual lines independently. It also checks that the AWE API equals the ABS spreadsheet, the windows, the
  CPI vintage facts, the seams and the figures (124 checks).
- Figure labels round to whole per cent (rents +1% in the WPI figure is the 1.5 in headline.csv, which is
  1.495 unrounded).
