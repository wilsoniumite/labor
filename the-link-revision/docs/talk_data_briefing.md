# Data briefing — the three data figures, for the SEB talk

Built 2026-08-26 from the construction scripts and their records
(`link-repo/code/deflator_fork.py`, `feasibility_kappa.py`, `four_way.py`,
`lambda_compute2.py`; `the-link-revision/data/DATA_NOTES.md`; the built CSVs).
Purpose: enough construction detail to field questions cold. The other four
figures (schedule, eras, strata, U-shape) carry no data — schematics on the
running example's dollars, plus A&R 2026's estimated within-group pattern —
so they are not covered here.

## 0. The fork graph, from zero

Forget economics; the chart is four steps of arithmetic.

**Step 1 — one paycheck.** Take the average hourly pay of ordinary U.S.
workers (production and nonsupervisory — no managers). In 1964 it was $2.54
an hour. In 2024 it was $30.12. The paycheck grew about **12×**.

**Step 2 — two price tags.** Does ×12 make you richer? It depends on what
you buy. So track two price tags across the same sixty years: **durable
goods** (fridges, TVs, cars, furniture — things factories make) and
**shelter** (rent — and for homeowners, what renting their own home would
cost). Since 1964 the durables price tag rose about **3.2×**; the rent
price tag rose about **15×**.

**Step 3 — divide.** Paycheck ÷ price = how much of the thing one hour of
work buys.
- Durables: ×12 paycheck against ×3.2 prices → an hour buys 12/3.2 ≈ **3.8
  times as many durables** as in 1964.
- Shelter: ×12 against ×15 → an hour buys 12/15 ≈ 0.79 of the housing —
  **a fifth less**.

**Step 4 — plot it.** The chart draws those two divisions every year, both
forced to start at 100 in 1964. Blue = paycheck measured in durables. Red =
paycheck measured in shelter. A line going up means an hour of work buys
more of that thing than in 1964. Blue ends at 377, red at 79, and 377/79 =
**4.8** — the fork.

**The one clever bit.** 377/79 is also just 15/3.2: divide one line by the
other and the wage cancels. The gap between the lines is purely "rents rose
about five times faster than durables prices." So no objection to the wage
series — composition, coverage, measurement — can touch the 4.8; it can
only move both lines together.

**What the chart is NOT saying.**
- Not that workers are five times richer or poorer — it is per-unit
  purchasing power in two specific directions.
- Not house prices — shelter here is rent, a flow, not an asset price.
- Not one person tracked for sixty years — it is the average worker of each
  year.
- "100 in 1964" is not a claim that 1964 was good, or that durables and
  shelter cost the same then — indexing both to 100 just sets a common
  starting line so the divergence is visible.
- The durables line rides on quality adjustment: "3.8× the durables" means
  3.8× the quality-adjusted amount (a 2024 TV counts as much more TV than a
  1964 TV), not 3.8× the number of boxes.

**Why the paper cares.** The model says machine progress must cheapen the
things machines make relative to the things nobody can make more of — the
ground under housing. If that is right, the paycheck has to split exactly
this way: strong in gadgets, weak in ground. The chart is that prediction
sitting in public data.

---

## The discipline behind every number (worth one slide-line at a bank)

- Every series is pulled live from FRED, with the series ID verified against
  the FRED page title before use.
- Every pull must pass a sanity anchor (a loose value band at 2023, e.g. the
  wage series must sit in $26–32/hr) — this catches wrong-series pulls, and
  never substitutes data.
- Annual values are means over **complete calendar years only**; a partial
  vintage year cannot masquerade as an observation.
- On any failure the scripts **stop rather than approximate** (standing rule).
- Every contestable classification is a labeled axis of a grid; the reported
  number is the **median across the grid**, with the min–max band drawn. No
  series is spliced across a methodology break.

---

## 1. The fork (Figure 3 — `deflator_fork.py`, `data/deflator_fork.csv`)

**What the chart literally is.** One nominal wage series divided by two CPI
sub-indices, each rebased 1964 = 100:

- Wage: **AHETPI** — average hourly earnings, production & nonsupervisory
  employees, total private. Monthly, annualized. Chosen because it is the
  longest consistent hourly-wage series (1964 is its first full year).
- Deflator A: **CPI durables** (CUSR0000SAD).
- Deflator B: **CPI shelter** (CUSR0000SAH1).

2024 endpoints: durables leg **376.8** ("nearly four times the durables"),
shelter leg **78.6** ("a fifth less shelter"). Fork ratio 376.8/78.6 =
**4.8×**. (Abstract slip to fix: it currently says "nearly five times the
durables" — the durables leg is ~3.8×; 4.8 is the *ratio between the legs*.)

**The shape, in three phases** (useful when walking the slide):
1. 1964–78: both legs drift up together — no fork.
2. 1978–94: the shelter leg does its falling (96 → 74); durables roughly flat.
3. 1995–2024: the durables leg does its rising (140 → 377, +169%) while
   shelter is flat (73 → 79, +7%). A pandemic wiggle: the durables leg
   *fell* 2020–22 (359 → 331, the durables inflation burst), then recovered.

**Defenses to have ready, strongest first.**

- **The ratio is wage-series-invariant.** Durables-leg ÷ shelter-leg =
  CPI-shelter ÷ CPI-durables — the wage cancels. Any attack on AHETPI
  (composition, coverage) moves both legs identically and leaves the 4.8×
  untouched. The 4.8 is a pure relative-price fact — it is the model's
  *q* rising, measured in CPI space; the paycheck framing only converts it
  into wage units.
- **Not a CPI-methodology artifact.** The CPI moved shelter to rental
  equivalence in January 1983 (before that, homeownership entered via house
  prices and mortgage interest). Computed from the built series: the fork
  ratio was 1.46 in 1983 and 4.79 in 2024 — a factor of **3.3 of the total
  4.8 accrues after the seam**, under the modern flow methodology. And the
  pre-1983 bias runs *against* the shelter leg's fall being understated:
  1979–82 mortgage rates inflated measured shelter inflation, i.e. the old
  methodology, if anything, overstates the early erosion — a segment that
  is not carrying the result anyway.
- **Shelter CPI is a rent, not a price.** It measures rents and rental
  equivalence — a flow — which is exactly the model's *r*. At a bank,
  "shelter" will be heard as house prices; say explicitly that no asset
  price is in the chart, so no interest-rate repricing is either.
- **The durables leg owes nothing to housing policy** (the §10 reply to the
  zoning rival), and since 1995 it is the larger share of the divergence.

**The honest soft spot.** The durables leg is quality-adjusted (hedonics):
"3.8× the durables" means 3.8× the *quality-adjusted quantity*, not 3.8
fridges. If pressed: the adjustment is BLS's, applied consistently across
the whole CPI; shrinking it shrinks the durables leg but cannot touch the
shelter leg's absolute fall; and the fork's *sign* survives any defensible
hedonics stance. Do not claim the 4.8 is invariant to hedonics — it is not.

**Likely SEB question — "does this exist for Sweden?"** Not computed.
The mechanism predicts it wherever machine-made goods cheapen against
land-priced services; SCB publishes comparable CPI sub-aggregates, so a
Swedish companion panel is a one-evening unit *under the house rules*
(primary source, validated) if wanted before the talk.

---

## 1b. The Swedish fork (built 2026-08-26 — `code/swedish_fork.py`, `data/swedish_fork.csv`, `figures/fig_swedish_fork.png`)

Same construction, Swedish primary sources (SCB PXWeb API, six tables,
titles verified at pull time; full record: `data/DATA_NOTES.md`, item four).

- **Wage:** manual workers' hourly pay. Long member: mining+manufacturing,
  "pay for time worked," 1952–2025 — the historical table (SLP11a,
  1952–2013) and the current table (SLP9a07, 2008–2025) agree to four
  decimals in every overlap year 2008–2013, so this is one series across a
  publication seam, not a splice. Short member: all private industry incl.
  overtime (KLP), 2008–2025.
- **Machine leg:** SCB's "Durable goods" special aggregate (VV) — the
  direct analog of the U.S. durables CPI; alternates: furnishings/household
  equipment (05) and ICT equipment (08.1).
- **Housing leg:** actual rents (04.1); broad housing incl. energy and
  owner costs (04); CPIF-04 (fixed interest rate, 1987–) as the
  rate-insensitive variant.

**Results (1980 = 100, complete years, through 2025).** Paycheck ×6.5;
durables prices ×1.3; rents ×7.4. Durables leg ends at 498, rents leg at
88: fork **5.7× against rents** (4.3× against broad housing; U.S.: 4.8×).
The ICT member alone is ×276 — reported in the CSV, kept off the chart.

**The timing parallel.** Both countries did their rent-leg falling before
1995 (U.S. shelter leg 100→74 by 1994; Swedish rent leg 100→66 by 1995 —
the tax-reform and crisis years), and nearly all fork growth since 1995 is
the durables leg (U.S. ×2.7, Sweden ×4.1).

**Swedish caveats, ranked.**
- **Rent regulation makes 5.7 a lower bound.** Swedish rents are negotiated
  under the use-value system; scarcity a market would price into rents
  shows up instead as queue-years and as owner-market prices, which are not
  in the CPI at all. A market-rent fork would be larger, not smaller.
- **The broad-housing member (04) carries owners' mortgage-interest costs**
  (Swedish KPI convention), so it swings with the policy rate — the dashed
  line's 2022–24 dip is that. The CPIF-04 member exists to strip it.
- Same hedonics caveat as the U.S. durables leg; extreme for the ICT member.
- The long wage member is manufacturing manual workers (the population with
  a 1952 record); the all-industry member (2008–) tells the same story
  where they overlap — and the between-legs ratio is wage-invariant anyway.

---

## 2. Coverage κ (Figure 4 — `feasibility_kappa.py`, `data/kappa_results.csv`)

**What the chart literally is.** κ = rT / (N·P_s): the aggregate site-rent
flow, divided by (population × the cost of one person's subsistence bundle).
"If the state captured every dollar of site rent and mailed everyone an
equal check, what fraction of one subsistence would it buy?" 2025 reading:
**0.33 [0.18–0.59]**, up from ≈0.05 in the 1950s.

**Numerator rT — six members, two families.**
- *Stock × cap rate:* land value = Z.1 market value of real estate minus
  BEA replacement-cost structures (the **land residual**), × a
  capitalization rate ∈ {10-year Treasury, 10y + 150bp}. Two scopes:
  households+nonprofits only (`z1_hh`, e.g. HNOREMV minus household
  residential structures), and economy-wide adding nonfinancial corporate +
  noncorporate real estate minus their structures (`z1_econ` — its NFC
  structures series ends 2020, so that member stops there; disclosed in the
  caption).
- *Flow-side lower bound:* PCE housing services × a land share of housing
  ∈ {0.30, 0.50} — no valuation, no cap rate, housing only.
- 2025 magnitudes for feel: z1_hh members $1,009B/$1,362B; flow members
  $993B/$1,655B.

**Denominator N·P_s.** NIPA population × the Orshansky 1963 poverty basket,
CPI-updated (that is literally how official U.S. thresholds are constructed;
the bases — $782/head family-of-four, $1,540 single, 1963 dollars — were
validated against the published 2023 thresholds before use). Two bundle
members × six rent members = 12-member grid; median + min–max band.

**Caveats, ranked.**
- **The residual method is the weak joint.** Land = market value − *estimated*
  replacement cost of structures; the Fed's own literature flags the
  residual as unreliable after ~1995 (this is stated in the figure caption).
  It is why every land member is treated as a **lower bound** — financial,
  government, and farm land are omitted entirely.
- **Band width is mostly the cap-rate spread.** At SEB this is home turf:
  invite the room to argue the cap rate — the band already contains the
  argument, and the flow members (which use no rate at all) show the same
  seventy-year trend. That also answers "isn't this just falling interest
  rates inflating land values?": the flow members never touch a valuation.
- **The bundle cuts the other way.** The 1963 basket underprices modern
  floor housing: the FY25 median-county efficiency fair-market rent alone is
  $9,960/yr gross vs. the whole single-person bundle P_s(2025) = $16,186.
  Against a modern housing standard, κ is *overstated*. Net position to
  state plainly: **the level is soft in both directions; the claim is the
  seventy-year trend**, which every member shows.
- **The physical ceiling.** κ can never exceed land-per-head; measured on
  HUD FY2025 fair-market rents (32-member grid): median 1.26, 13/32 members
  below 1 — shared housing clears the ceiling everywhere, solo dwellings in
  the priciest metros do not. The paper states this; do not let a questioner
  discover it first.

---

## 3. The financing split (Figure 7 — `four_way.py`) and φ_C, φ_G

(Paper symbols are v2 as of 2026-08-27: the wage-linkage shares are now φ_C and φ_G — `docs/notation_map.md`.)

**What the chart literally is.** NIPA income-side bookkeeping of what
finances U.S. consumption **outside the owner loop** (i.e. excluding
household capital income financing its own owners' consumption): direct
wages | transfers funded by wage taxes | transfers funded by ownership
taxes | transfers funded by borrowing. Headline: direct wages ceded ~20
points in sixty years, in a ratchet (each recession cuts, each recovery
restores only part); the borrowed channel reached 19% of transfers by 2025
and was zero only in 1998–2000.

**Construction.** Wage-side income = wages + supplements + a labor share of
proprietors' income; capital side = the rest of property income. Transfers
= NIPA social benefits; their funding is split by classifying revenue
(payroll contributions fully wage-linked; personal/corporate/property taxes
split under grid rules), with the government current deficit attributed to
transfers under three labeled rules (protected / pro-rata / marginal — a
grid axis). Grid axes: proprietors' labor share {0.50, 0.65, 0.80},
capital-tax tilt {1.0, 1.5}, corporate-tax wage linkage {0.25, 0.50},
earmarking {pooled, earmarked}, financing order {3 rules}, deficit
attribution {3 rules}. A fixed-point step makes the sales-tax linkage
consistent with the wage-financed consumption share it feeds.

**The two ledger numbers.** φ_C = **0.72 [0.66–0.81]** (2025): wage-linked
share of consumption financing. φ_G = **0.68** (2025): wage-linked share of
tax revenue. Same machinery (`lambda_compute2.py`), same grids.

**The one sentence to repeat under questioning.** This is **pro-rata
accounting, not estimated incidence** — the caption says so, and so should
you. It answers "which dollar finances which purchase?" as bookkeeping
attribution; it does not claim a causal experiment. Its job in the talk is
one claim only: the state's revenue and the household sector's consumption
financing are both keyed to the wage base the technology is eroding.

---

## Repro

All three rebuild from `link-repo/`: `code/deflator_fork.py`,
`code/feasibility_kappa.py`, `code/four_way.py` (FRED pulls cache to
`cache/`; venv at the repo root). Built series: `data/deflator_fork.csv`,
`data/kappa_results.csv`, `data/four_way_split.csv`. The κ-ceiling grid is
`the-link-revision/code/kappa_ceiling.py` + `data/kappa_ceiling.csv` (HUD
FMR file vendored and validated).
