# Splits — the protocol

Written 2026-10-12, on her request: many headline statistics only make sense split into a machine/owner side and a
human/wage side. Revised 2026-10-13 after three reviews (statistics, public copy, protocol), and measure 12's wealth
slope set by her call the same day, before any freeze.
**Fixed by the tag `paths-splits-freeze`**, whose date is the fixed date; until the tag exists this is a draft and
every reading is a starting point. The tagged commit fixes this file together with `code/splits.py`,
`results/splits_baseline.json` and the vintage it was written on (`cache/splits/`), so nothing here needs editing at
the freeze. After the tag nothing below changes; a later departure is written in `STATE.md` as a deviation, and every
reading made after it carries the word. Method borrowed from `participation/PROTOCOL.md`.

## 1. The design

- **Explore = everything up to the freeze; confirm = what is published after it.** The panel of 2026-10-12 catalogued
  46 measures, tested 22 cuts and tried the 2,047 cuts of measure 2; she and Claude have seen every series below to
  September 2026. Those readings are the starting point, labelled "starting point (already seen; not judged)".
- **Score the excess over normal times, and say what persistence alone would give.** Each measure is a gap between
  the two sides. What counts is how far its change over the window departs from the usual change in 1990-2019 years
  without a recession (section 4). A gap that keeps moving at its 1990-2019 pace scores nothing; a split that continues
  at its recent pace scores again, so each measure carries the chance that persistence alone gives its reading
  (section 5).
- **Count what does not happen.** All twelve are reported every quarter in a fixed order, the ones going against the
  paper and the ones showing nothing included.
- **Each measure names one rival and the call where it differs from the paper's.** Measures where everyone agrees carry
  no weight. Where a rival's call depends on a condition (a rate cut, a rise in real rates, the end of the build-out)
  the condition is tested from data, and without it the rival makes no call. The rivals can all be partly true at
  once; the tally (section 6) shows which calls came true, not the single cause.
- **Additions are kept apart.** At most five per yearly look, each in a separate list with its own baseline and its own
  tag (`paths-splits-E-<year>`), judged only from the next window and reported measure by measure. Each cites the
  committed output that motivated it. An addition never enters the twelve's count, verdict or retirement, never
  replaces one of the twelve, and is outside the twelve's definitions hash. Swaps to the twelve before the freeze are
  design decisions in `STATE.md`.

## 2. The twelve judged measures

US public data via FRED. `L(x) = 100·ln(x)` (log points). Window: 12 months (monthly) or 4 quarters (quarterly).

| # | Measure | Series and transformation (the gap) | Paper's call | Named rival: its call |
|---|---|---|---|---|
| 1 | Care: jobs and relative pay | gap `L(CES6500000008/AHETPI)` (care's relative pay, production workers, education and health); leg `L(CES6562000001/(PAYEMS−CES6562000001))` (care's jobs) | crowding: pay falls (signed down) while jobs rise faster than usual | ageing demand: pay rises with jobs |
| 2 | Payroll dispersion | share (%) of all 2,047 two-way cuts of the 12 supersectors (USMINE, USCONS, MANEMP, USTPU, USINFO, USFIRE, USPBS, CES6561000001, CES6562000001, USLAH, USSERV, USGOVT; government always on side B) whose **12-month** relative growth is beyond 2 sd of its own 1990-2019 non-recession windows | stays above the normal months' 95th percentile without a recession | cycle and the over-hiring unwind: falls back below it |
| 3 | Graduates | `L(avg3(LNS14027662)/avg3(LNS14027660))` (bachelor's+ over high school only, 25+, 3-month averages) | rises without a recession | an ordinary slowdown: falls |
| 4 | Software postings | `L(mean_m(IHLIDXUSTPSOFTDEVE)/mean_m(IHLIDXUS))`, complete months | keeps falling | the 2022 over-hiring and the R&D-expensing rule (restored July 2025): recovers |
| 5 | Hiring | `JTSHIR − (b0 + b1·UNRATE)`, fit 2001-2019, monthly | stays below the fit (signed down) | interest rates and uncertainty: closes within four quarters of rate cuts |
| 6 | Output per hour | `L(OUTNFB/HOANBS)`; the 4-quarter change is output-per-hour growth | grows faster than its usual range (3.2% or more over four quarters) | lower immigration: hours slow, output per hour within its usual range |
| 7 | Labour share | `100·A460RC1Q027SBEA/A455RC1Q027SBEA` (nonfinancial corporate compensation over gross value added) less its 1948-2019 fit on the level of quarterly UNRATE | falls (signed down) | the cycle: moves only with unemployment |
| 8 | Asset income | gap `L(PDI/W209RC1)` (dividends over pay); legs `L(PII/W209RC1)` (interest) and `L(RENTIN/W209RC1)` (rent, quarterly, reported) | dividends (and rent) rise relative to pay | higher interest rates: only interest rises |
| 9 | Produced-input shortage premium | `L(PCU335311335311/WPUFD49207)` (transformer PPI over finished goods PPI, both not seasonally adjusted) | a temporary premium on produced capital: falls back by 2028 (signed down) | lasting scarcity, rents migrating to power equipment: keeps rising |
| 10 | Site rent | `L(land / annual pay)`, land = (BOGZ1FL155035015Q − RCVSHNWBSHNO) + BOGZ1FL105010005Q + BOGZ1FL115010005Q (owner-occupied real estate less its structures at current cost, plus business land at market value, Fed Z.1), pay = quarterly mean W209RC1 | rises | high real interest rates: falls as the real rate rises |
| 11 | Build-out against housing | `L(B679RA3Q086SBEA/A011RA3Q086SBEA)` (real quantity indexes: information processing equipment and software over residential investment) | widens (the neutral rate's rising phase) | interest rates: narrows after rate cuts |
| 12 | Saving | `PSAVERT` (quarterly mean) less what household equities over disposable income (`BOGZ1LM153064475Q / (1000·DSPI)`) imply at a wealth slope of −1 point per unit of the ratio, set from the literature (about one cent of spending per dollar of equity wealth), with the intercept the 1960-2019 mean of `PSAVERT` plus the ratio | the residual rises (owners save; the paper's later phase) | the wealth effect: no residual change |

The fitted coefficients of 5 and 7 and measure 12's intercept are estimated once, at the freeze, and kept in the
baseline; later vintages' estimates are printed beside them and never used for judging. Measure 12's slope is set from
outside the data (section 4).

**The conditions, tested from data:**

- *A rate cut* (5, 11): the fed funds target at the window's last month at least 50 bp below its level twelve months
  earlier (FRED `DFEDTAR` to 15 December 2008, then the range's upper limit `DFEDTARU`).
- *A rising real rate* (10): the 10-year real interest rate (Cleveland Fed, FRED `REAINTRATREARAT10Y`) higher in the
  window's last quarter than in the quarter before the window.
- *The build-out has turned* (12): measure 11's same window reads `−`.
- *The deadline* (9): the second judged window (ending 24 months after the baseline, August 2028 for a baseline in
  August 2026) is judged on the level: the relative price below its baseline level fits the paper, above it the rival.

**Which explanation a reading fits** (zones: `+` E ≥ +1, `0` in between, `−` E ≤ −1, E signed toward the paper). A
rival's fit is either a *signed call* (something moved its way) or *nothing unusual* (its call is that nothing
happens):

- 1: only while the jobs leg's E > 0: `+` paper, `−` rival (signed); otherwise neither (and the measure counts as `0`).
- 2: level ≥ the 95th percentile `+` (paper); started the window at or above and ended below `−` (rival, signed);
  below at both ends `0` (rival, nothing unusual).
- 3, 4: `+` paper, `−` rival (signed), `0` neither.
- 5: `+`, or `0` with the gap below zero, fits the paper (it stays below); `−` after a rate cut the rival (signed),
  without one neither.
- 6, 7: `+` paper, `0` rival (nothing unusual), `−` neither.
- 8: dividends `+` paper; otherwise the interest leg's E ≥ +1 rival (signed); otherwise neither.
- 9: `+` paper, `−` rival (signed), `0` neither; at the deadline window, its level as above.
- 10: `+` paper; `−` with a rising real rate the rival (signed), without one neither; `0` neither.
- 11: `+` paper; `−` after a rate cut the rival (signed), without one neither; `0` neither.
- 12: `+` paper; `0` the rival (nothing unusual) only once the build-out has turned, before that neither (the paper's
  call is for after the build-out); `−` neither.

**Thresholds in plain units** (the change over the window at which a measure reads `+` or `−`, on the vintage of
2026-10-13; the baseline fixes them):

| # | Reads the paper's way (`+`) | Reads the other way (`−`) | Units |
|---|---|---|---|
| 1 | ≤ −0.56% | ≥ +0.72% | change in care's relative pay |
| 2 | level ≥ 26.6% | (fell below it) | share of the 2,047 cuts |
| 3 | ≥ +8.6% | ≤ −7.6% | change in the graduates' rate relative to the high-school rate |
| 4 | ≤ −35.4% | ≥ +27.6% | change in software postings relative to all postings (its own history) |
| 5 | ≤ −0.14 | ≥ +0.13 | points, change in hiring's gap |
| 6 | ≥ +3.2% | ≤ +0.5% | output-per-hour growth over four quarters |
| 7 | ≤ −1.21 | ≥ +0.78 | points, change in the adjusted labour share |
| 8 | ≥ +15.1% | ≤ −3.7% | change in dividends relative to pay |
| 9 | ≤ −3.4% | ≥ +4.2% | change in transformer prices relative to finished goods |
| 10 | ≥ +11.6% | ≤ −5.8% | change in land values relative to pay |
| 11 | ≥ +18.9% | ≤ −1.3% | change in real IT investment relative to housing |
| 12 | ≥ +1.02 | ≤ −1.27 | points, change in the saving residual |

**Channels.** Several measures move together through one channel; the verdict is recomputed without each (section 6):
*rates* 5, 8, 10, 11, 12; *the tech unwind* 2, 3, 4, 5, 11; *the 2021-23 price shock* 1, 8, 9.

What the paper does **not** predict, and is therefore not judged: that rents migrate to power or utilities (electricity
and equipment are produced outputs; grid connections are scarce only until more are built), or anything about whether
the largest companies keep their share-price gains (they mostly own produced capital; some own sites, power contracts
and patents). The paper's lasting rent is land and sites, and legally protected rights.

## 3. The watch list (reported every quarter, never judged)

- Big stocks against the rest: `L(NASDAQ100/NASDAQNDXE)` (Nasdaq-100 cap-weighted over equal-weighted, monthly means);
  second, `L(NASDAQNQUSL/NASDAQNQUSS)`. A proxy for her "big ten up, the rest down": the S&P 500 equal-weight index is
  not on FRED, and a price split measures expectations and discount rates (small firms carry floating-rate debt).
- Computer imports over investment in information processing equipment: `100·B852RC1Q027SBEA/Y034RC1Q027SBEA`.
- Electricity against all consumer prices: `L(CUSR0000SEHF01/CPIAUCSL)`.
- Consumer spending, % of GDP: `100·PCEC/GDP`. Spending is outrunning income in 2026; the paper puts owners' saving
  after the build-out, so this is not judged.
- Sweden: household property income received less paid (D4), % of GDP, 4-quarter sums — Statistics Sweden NR0103 sector
  accounts (`cache/scb/sector_S14.json`, `gdp_current_sa.json`), national accounts, not labour-force data.
- Context for the website's spending section: the shares of US household net worth held by the richest 1% and 10%
  (Federal Reserve Distributional Financial Accounts, `WFRBST01134`, `WFRBSN09161`, from 1989Q3).

## 4. The statistic

`E = (change in the gap over the latest window − mean of such changes) / their sd`, signed toward the paper's call.
The mean and sd come from windows **ending in 1990-2019 that contain no NBER recession month** (FRED `USREC`, the
period after the peak through the trough). E ≥ +1: moved the paper's way; E ≤ −1: moved against it; otherwise no
clear change.

- **Short histories:** fewer than 120 monthly (40 quarterly) such windows → the longest available non-recession history
  up to the window before the latest (so the latest reading is not in its own benchmark), flagged `own_history`. Only
  measure 4 (Indeed, from February 2020) is affected: its benchmark is 2021-04 to 2025-09, which contains the 2022-25
  fall it is meant to test, and it reads `+` only on a fall of 35% relative to all postings in a year, `−` on a rise of
  28%. It is reported beside the count, never in it. Measure 5 uses 2002-2019 (JOLTS starts December 2000); measure 3
  1993-2019; measure 1's jobs leg 1992-2019.
- **Measure 2** is judged on its level: the share in the window's last month (12-month growth, so a judged reading holds
  nothing from before its window's start, and consecutive windows share no data) against the 95th percentile of the
  share in normal months (from 1992-03, 12-month windows without an NBER recession month), 26.6% on the 2026-10-13
  vintage. The per-cut means and sds are frozen in the baseline. Of the 15 normal months at or above that percentile,
  13 fall in the year after a recession's exclusion ends (recoveries; without those years the percentile is 10.9%).
  The threshold keeps them, because judged windows in a recovery are not voided either.
- **Recessions:** a window touched by an NBER recession month, or by a real-time Sahm reading ≥ 0.5 (`SAHMREALTIME`,
  for windows NBER has not yet dated), is void for the paper against the cycle — except measures 3 and 7, whose rival
  is the cycle itself: they are judged in a recession window. The combined verdict is void either way. For measure 2
  the window is its own 12 months, and for a fall below the threshold also the 12 months before its start. In a
  downturn the tracker therefore reports every measure, judges 3 and 7, and gives no combined verdict.
- **Measure 7's adjustment is small:** over a year the unemployment rate moves little, so the adjusted change is close to
  the raw share's (on 2026Q2: E +1.36 adjusted, +1.44 raw; the raw E is reported beside it).
- **Measure 12's wealth slope is set from outside the data** (her call, 2026-10-13; `STATE.md`, decision 58): −1 point
  of the saving rate per unit of household equities over disposable income, about one cent of spending per dollar of
  equity wealth, from the literature; the intercept is the 1960-2019 mean of the saving rate plus the ratio, so the
  residual averages zero over 1960-2019. The 1960-2019 fit (slope −4.27) would be extrapolated far: household equities
  are 3.09 times disposable income in 2026Q2, against 0.32-2.00 in that fit, which puts the saving rate at −0.4%. On
  2026Q2 E is −0.66 as built, +0.57 with the 1960-2019 fit, −0.12 with the 1990-2019 fit and −1.00 with no wealth term.
  The alternatives are reported beside it, with a flag while the ratio is beyond its 1960-2019 range.
- **The naive forecasts, printed beside each measure:** E if the last window repeats; E from the measure's carry-over
  regression (next non-overlapping window's E on this window's E, 1990-2019); and the chance that persistence alone
  gives today's reading next time.

## 5. Base rates (stated before any judged window)

- **Pooled** over the ten counted measures with E (not 2, judged on its level, nor 4, benchmarked on its own history),
  on the 2026-10-13 vintage: when |E| ≥ 1, the next window's excess had the same sign **59%** of the time and was again
  beyond 1 in that direction **17%** of the time (the panel's construction, an 8-quarter slope in its top quarter, gave
  64%).
- **The measures split at the starting point continue more often:** the same sign the next year 75% of the time for care
  (again beyond 1: 20%), 81% for the labour share (31%), 91% for the build-out (17%); against 30-32% for graduates,
  hiring and saving and 27% for software postings. From persistence alone, the chance that the next window reads `+`
  again is 57% for care, 23% for the labour share and 41% for the build-out. A single measure's "moved the paper's
  way" is therefore weak evidence where persistence is strong. Per-measure rates are in `results/splits.json`.
- **Measure 2:** of the 14 normal months at or above the 95th percentile, 1 (7%) was still above it 12 months later.
- **The rules in normal years (the power, stated now).** Applied to the 13 benchmark years (section 6), the verdict
  would have read *supports the paper* in none, *favours the rivals* in 1, *nothing unusual* in 8 and *inconclusive* in
  4. Of the explore years, 2022 reads *nothing unusual* and 2023 *inconclusive*; 2020, 2021, 2024 and 2025 are void (a
  recession, or a real-time Sahm reading ≥ 0.5 in 2024). So a year in which nothing unusual happens most likely reads
  just that, and *supports the paper* never came up in a normal year from 2004 to 2019. The measures move together
  more since 2021 than in 1990-2019, which is why the verdict is recomputed without each channel.

## 6. The combined reading

- **(a) The count:** measures moved the paper's way minus measures moved against it (the zones above; care counts only
  with its jobs leg above usual), over the **eleven measures with 1990-2019 history** — all but 4, which is reported
  beside the count. Set against the same count in every 1990-2019 year in which all eleven exist and no window touches
  an NBER recession month or a real-time Sahm reading ≥ 0.5 (the same void rule as judged windows), each measure's
  window ending in the calendar month its judged windows end in (September; August for 5, 8 and 9; the second quarter
  for the quarterly measures). On the 2026-10-13 vintage these are 13 years, 2004-2007 and 2011-2019 (hiring's history
  begins in 2001; recession or Sahm months void 2002-2003 and 2008-2010): median 0, 90th percentile 1.8, range −2 to
  +2.
- **(b) The tally:** per measure, which explanation the latest window fits: paper, rival (signed or nothing unusual),
  both, neither.
- **Verdict, per judged window** (all eleven counted windows past their end; given at the yearly look):
  - *void* when a recession or a Sahm month touches any counted measure's window;
  - *supports the paper*: count above the benchmark's 90th percentile and the paper fits at least twice as many
    measures as the rivals (all their fits, signed or not; and at least one);
  - *favours the rivals*: the rivals' signed calls fit at least twice as many measures as the paper (and at least one);
  - *nothing unusual*: the count at or below the benchmark's median, or no fit for the paper and no signed call for a
    rival;
  - *inconclusive* otherwise.
- **Channels:** the verdict is recomputed without each channel of section 2 (the benchmark too); a verdict that flips
  is reported as resting on that channel.
- **A window end never published** (a month never collected) is left out of the count and of the benchmark, which is
  recomputed without that measure.

## 7. Cadence

- **Quarterly (about an hour):** `../venv/Scripts/python.exe code/splits.py --refresh`, then
  `checks/check_splits.py`; read the fixed table; one Log line in `STATE.md`. No verdict: before its look date a judged
  window reads "awaiting the yearly look".
- **Yearly judged look:** on the first 15 November at least twelve months after the freeze (a freeze in October 2026
  gives 15 November 2027), or the first day after it on which every counted window has been published. It runs once,
  on one fresh vintage: `code/splits.py --refresh --look`, which refuses if any series failed to refresh or a window is
  incomplete, and writes `results/splits_look_<year>.json`. The main session commits it with `results/splits.json` and
  `cache/splits/`, tags `paths-splits-look-<year>` and pushes the tag the same day. That verdict stands; later runs read
  it from the tag and report the same window on revised data beside it, never in its place. Windows do not overlap.
- **Vintages:** every series' download date and hash sit in `cache/splits/vintages.json` and in the results; a refresh
  records how many observations each revision changed. A failed refresh keeps the previous file and its record, marks
  it `refresh_failed_utc` and warns. The frozen references, coefficients and moments are used; the current vintage's
  are printed beside them.

## 8. When to retire the idea

After two consecutive non-void judged windows that each favour the rivals or read nothing unusual; void windows are
skipped, not reset. Stated plainly: in the 13 benchmark years this would have happened in 6 of the 12 consecutive pairs
(in none with both favouring the rivals), so two ordinary years can retire it. Retiring ends this line of evidence; it
does not refute the paper.

## 9. The freeze

1. She says freeze. The main session runs `code/splits.py --refresh --write-baseline`, which refuses if any series
   failed to refresh and writes `results/splits_baseline.json`: per series its last observation, download date, hash
   and FRED's title, and the series whose last observation is later than in the 2026-10-13 vintage (published between
   the panel and the freeze, and so seen before it); per measure (and leg) its last observation, starting value and the
   reference mean and sd that E will use; the fitted coefficients of 5 and 7 and measure 12's intercept and (set) slope;
   measure 2's per-cut means and sds and its threshold; the benchmark years of section 6; the base rates of section 5;
   the SHA-256 of this file, of the measure definitions with the code that computes and judges them
   (`definitions_hash()`) and of the code file.
2. `checks/check_splits.py` passes; commit (with `cache/splits/`); tag `paths-splits-freeze` and push the tag the same
   day. Then run `code/splits.py` again, without `--refresh`, and commit and push `results/splits.json`: only results
   written after the tag record the freeze (status frozen, the tagged commit's SHA and the tag's date), and the website
   says "fixed on" only from those. The results flag a tag that has moved since the last run, or that was made more
   than a day after the baseline was written. The code refuses to rewrite the baseline once the tag exists, and from
   then on reads it from the tagged commit, not the working copy (a working copy that differs is flagged; a tagged
   commit without a baseline judges nothing).
3. After the tag only complete, non-overlapping windows that start at each measure's baseline observation are judged:
   [b, b+12 months], [b+12, b+24], … (quarters likewise). Nothing before b enters except its value as the first starting
   point. The latest rolling readings are labelled "latest 12 months (4 quarters), not judged". If this file or the
   definitions change after the tag, every reading is labelled a deviation.

## 10. Bug policy

Plumbing (fetching, parsing, output) may be fixed after the freeze, each fix in its own commit with the reason. A change
to a measure's series, transformation, window, reference, fit, condition or call is a deviation, recorded in
`STATE.md`, and the measure is reported both ways. This is enforced: the definitions hash covers the code of every
function that computes or judges the measures, and whenever the code file differs from the tagged one the tagged code
is run on the same data beside it. The judged readings are the tagged code's; if the working code judges any window
differently the run is labelled a deviation and both are reported; a change that leaves every judged reading unchanged
is labelled so.

## 11. Blinding

No European labour-force data enters this unit. `splits.py` fetches only the manifest (an allowlist of US series from
FRED) and refuses Eurostat, ILO, OECD European labour-rate and Statistics Sweden AKU/LFS identifiers and files by name
(`guard()`), so the participation thread's European tests stay blind.
