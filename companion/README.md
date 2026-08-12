# Companion paper — the empirical ρ̃(x,t) schedule

Working home of the companion to "The Link" (design and pre-registration:
`companion_schedule_spec.md`, in this folder). The Link prices the capability schedule's
flattening; this paper measures the schedule.

## Layout

- `code/` — pipeline. `fetch.py` (download/cache/validate; every URL probed
  live before hardcoding), `build_panel.py` (the task panel),
  `probe_urls.py` (the probe record).
- `cache/` — raw downloads, validated by magic bytes and content, never
  edited.
- `data/` — built outputs (see below).
- `checks/` — gates. Nothing feeds the paper before its check runs green.

## Built so far (unit 1: the task panel)

`data/oews_occ1990dd_panel.csv` — year × occ1990dd (1999–2025, 326
occupations): employment, mean/median hourly and annual wages, source-code
counts, a derived convenience label. OEWS national files mapped onto the
harmonized Autor–Dorn occ1990dd classification through official Census/BLS
code lists, with a SOC hierarchy walk and the census lists' X-wildcard
prefixes; a source code with k targets splits employment equally
(SPLIT_EQUAL — a labeled choice, grid axis later).

`data/occ1990dd_attributes.csv` — occ1990dd × task descriptors: Autor–Dorn
DOT-1977 abstract/routine/manual intensities, offshorability, O*NET 30.3
attachments (task counts, mean importance), latest label.

`data/panel_coverage.csv` + `data/build_ledger.txt` — per-year mapped
employment share vs each file's own all-occupations total (0.91–0.97,
median 0.96), walk/split shares, top unmapped codes.

## Built so far (unit 2: the w/c grid and the family A envelope)

`data/wc_grid.csv` — the waterline: w/c annually 1999–2025, six members
(AHETPI and the panel's employment-weighted OEWS mean, over the hedonic
computers investment price index, the computer-manufacturing PPI, and the
broad-equipment index; every FRED ID title-verified live), normalized
1999 = 1. Median rises ×8.0 by 2025 (members ×2.4–×16).

`data/flips_*.csv`, `data/envelope.csv`, `data/envelope_stats.csv`,
`data/waterline_density.csv` — the revealed-adoption envelope (Lemma 1
inverted): flip detection under three labeled share-decline rules
(d30/d40/d50 → 33%/15%/11% of 1999 employment flipped by 2025), each
flipped occupation priced at the waterline of its flip year, era-sliced
quantiles and the density-at-the-waterline series. The schedule arrives
in waterline units (identified up to scale; no capability numeraire
claimed). Figure: `figures/schedule_envelope.png`.

Reproduce and gate:

    ../venv/Scripts/python.exe code/build_envelope.py
    ../venv/Scripts/python.exe checks/check_envelope.py

## Built so far (unit 3: family B, the right tail)

`data/exposure_occ1990dd.csv` + `data/right_tail.csv` +
`data/right_tail_stats.csv` — the Eloundou et al. LLM-exposure scores
(six published variants: {GPT-4, human} raters × {α, β, γ} aggregations —
the variants are the mapping grid; none of our own invented) mapped to
occ1990dd and joined with 2025 employment and unit-2 flip status. Headline
band: 0–56% of surviving 2025 employment sits at exposure ≥ 0.5 (α floor,
γ ceiling; ~23% at the median variant). Under the stricter flip rules the
surviving mass is MORE exposed than the flipped mass — the pre-LLM flips
were low-exposure routine work; the exposed mass is still standing.

`data/capability_clock.csv` — dated frontier traces (Epoch benchmark hub,
CC-BY): the Epoch Capabilities Index, GPQA Diamond, SWE-bench Verified,
and the METR 50%-success time horizon (the human-anchored member — task
scale is defined by human completion minutes, so no external human
baseline is injected). Horizon frontier: 0.04 minutes (2019) → ~17 hours
(2026); doubling every 5.0 months over the full span (steeper than the
7.1 months of METR's 2024 paper — their own later finding, visible here
in the longer window). `data/metr_raw_validation.csv`: horizons
recomputed from METR's raw runs (24,008 runs, weighted logistic per
model) match Epoch's republished values at log-correlation 0.993 on 15
rule-matched models (exact/unique-prefix matching only; ambiguous
variants dropped, never guessed). Figure: `figures/right_tail.png`.

Reproduce and gate:

    ../venv/Scripts/python.exe code/build_righttail.py
    ../venv/Scripts/python.exe checks/check_righttail.py

## Built so far (unit 4: family C, the wedge layer)

`data/wedges_occ1990dd.csv` — wedge measures per occupation:
Hirsch–Macpherson union membership/coverage (unionstats.com), pre-period
1999–2001 (measured at the panel base — no reverse causation from later
flips) and 2025; CPS table 53 licensed-or-certified share, published at
SOC-major-group level and attached to detailed occupations by employment
mix (ECOLOGICAL attachment — the resolution public data allows, labeled).
The A&R (2026) 40–50% wedge-rent magnitude stays a cited level anchor;
no per-occupation µ is constructed. Anchors: economy coverage 15.0%
(1999–2001) → 11.1% (2025), matching published aggregates.

`data/targeting_cohorts.csv` + `data/targeting_by_routine.csv` +
`data/protection_survival.csv` — the Prop 2 targeting-order TEST
(direction reported, not assumed). Result, honestly mixed and then
sharp where the theory says to look: unconditionally, early flip cohorts
carry more pre-period union coverage but weakly and rule-sensitively
(Spearman −0.10 to −0.18); WITHIN THE HIGH-ROUTINE TERCILE — the
automatable set, where the mechanism operates — the signature is clean
under every rule (early flippers ~19–20% covered vs ~5–14% late,
Spearman −0.19 to −0.35). The fortification glance: licensed share sits
7–9 points HIGHER among survivors under every rule, while union coverage
converges low everywhere by 2025 — price-form protection died with its
jobs, quantity-form protection survives. Figure:
`figures/wedge_targeting.png`.

Reproduce and gate:

    ../venv/Scripts/python.exe code/build_wedges.py
    ../venv/Scripts/python.exe checks/check_wedges.py

## Built so far (unit 5: cross-validation and the reinstatement series)

`data/reinstatement_series.csv` — the new-task margin, measured: task
births and deaths across 23 archived O*NET releases (2003–2026, dates
parsed live from the archive page), counted two ways per adjacent pair —
by Task ID (churn undercount) and by normalized statement text (rewording
counts, churn overcount) — over occupations present in both releases.
Result: in the mature era (2012+) recorded births decline from ~12 to
ZERO per 1,000 tasks per year (both members; the 30.0→30.3 pair records
not one new task across 18,797), with a real pruning wave in 2024
(deaths ~26/1,000). The reservoir The Link's branch two posits as
thinning is measured, on this instrument, as thinning to zero. Caveats
stated in the ledger: the early-2000s levels partly reflect O*NET's own
database-construction ramp (trend read from 2012+ only); O*NET records
task birth with a lag and through an occupational lens — it measures the
margin O*NET SEES, and that instrument's own drying is part of the
finding, not separable from it.

`data/friction.csv` + `data/friction_stats.csv` + `data/friction_named.csv`
— the A×B adoption-response measurement: employment-share log-trends
2015–19 vs 2022–25 (covid years excluded) joined against LLM exposure.
Aggregate: every exposure tercile decelerated post-LLM with NO positive
exposure gradient (low-exposure decelerated most) — the friction gap is
open on average, F still binding three years after the capability
arrival the unit-3 clock dates. Instance level: punctuated flips exactly
as the fortification remark predicts — Customer Service Representatives
(2.76M workers) swung from +1.7%/yr to −5.9%/yr, translators' growth
stopped (+5.0 → +0.5), Data Scientists' growth decelerated sharply,
Data Entry's old decline accelerated. Figure: `figures/crossval.png`.

Reproduce and gate:

    ../venv/Scripts/python.exe code/build_crossval.py
    ../venv/Scripts/python.exe checks/check_crossval.py

## Reproduce

    ../venv/Scripts/python.exe code/build_panel.py
    ../venv/Scripts/python.exe checks/check_panel.py

Live pulls hit ddorn.net, onetcenter.org, bls.gov, census.gov; the cache
makes reruns offline. `fetch.py` uses `truststore` (OS certificate stack) —
ddorn.net serves an incomplete TLS chain that browsers repair via AIA;
nothing disables verification.

## Honesty notes (carried into the paper's data note later)

- 1997–1998 OEWS use pre-SOC OES codes: PARKED, not dropped — the
  deep-history unit reaches them with the Census 1950–1990 extension.
- Unmapped residuals (2.6–8.8% of employment, mostly "all other" education
  and transport-supervisor codes, plus the 2019–20 hybrid code 15-1256)
  are reported in `panel_coverage.csv`, never imputed.
- OEWS excludes self-employment throughout; wage top-codes are counted and
  left missing, never filled.
- The flip rules catch every sustained share decline, whatever its cause:
  the d40 roster is dominated by the classic automation set (data entry
  keyers, sewing machine operators, packers, machinists, tellers) but
  includes known non-automation intruders — Chief Executives (the 2001
  OEWS classification/coverage break) and Carpenters (the housing crash).
  Pre-registered in the spec: share declines conflate demand and
  classification shifts with automation; the exposure-instrument
  refinement (families B/C, cross-validation) separates them. Nothing is
  hand-dropped.

- Benchmark-shaped-task bias (spec, pre-registered): capability benchmarks
  oversample verifiable tasks; the clock measures what benchmarks can see.
  Stated, not corrected. Exposure is an LLM-era measure and is NOT used to
  explain pre-LLM flips.

## Sources and credit

O*NET 30.3 database (U.S. DOL/ETA, CC-BY 4.0). Autor and Dorn (2013 AER)
task measures and occ1990dd crosswalks via ddorn.net. BLS OEWS national
files and SOC crosswalks. Census Bureau occupation code lists.

Family C: Hirsch and Macpherson, Union Membership and Coverage Database
(unionstats.com; cite Hirsch–Macpherson 2003 ILRR and the site's current
update note). BLS CPS annual-average table 53 (certification/licensing).
Acemoglu–Restrepo (2026) wedge-rent magnitude from published tables only
(their openICPSR package is registration-walled; per the data rule it is
not a member).

Family B: Eloundou, Manning, Mishkin, Rock (2023) occupation-level
exposure scores (openai/GPTs-are-GPTs, MIT license). Epoch AI benchmark
hub and Capabilities Index (CC-BY, credit Epoch AI). METR time-horizon
raw runs (METR/eval-analysis-public) — NOTE: the repo README points to a
LICENSE file absent from the repository (checked 2026-08-06); raw runs
are used only as a validation member with attribution, and the primary
horizon series is Epoch's CC-BY republication. Flag carried to the
paper's data note.
