# Companion paper spec — the empirical ρ̃(x,t) schedule (item 9)

Status: DESIGN SPEC, written 2026-08-06 (session 3). Nothing built, no prose
drafted. Source reachability probed live this day; every load-bearing member
green (statuses below). This document is the veto-window record for the
scoping unit, and the build's pre-registration: identification families and
honesty items are committed here before any estimate is run.

Inherited rules: live public data only, no substitution or approximation —
stop and report if a source is unreachable (The Link's data note). House
method for contestable measurement choices: no single-source picks — all
defensible variants through a rule grid, medians with bands (the κ
precedent, `feasibility_empirics_spec.md`). Checks gate absolutely.

## The object

The Link runs on ρ̃(x,t) = ρ(x,t)/µ(x): tasks ordered by the wedge-deflated
human-over-machine capability ratio, with the waterline w = c·ρ̃(x*) setting
the threshold. The paper takes the schedule as given and prices its
flattening; §7 measures downstream shadows (λ shares, κ, the deflator fork).
The central premise — "whether the non-uniformity closes is an empirical
premise" (§1); the §9 fork between reinstatement continuing and the
reservoir thinning — is flagged, defended, and never measured. The
companion measures it: level, slope, and motion of the schedule, 1962–2025,
matching The Link's measurement window. Figure 2's three-era schematic
becomes a measured figure; Prediction 1's calibration becomes a test.

## Identification — three families, one grid

No family identifies the schedule alone; the grid crosses them and the
overlap cross-validates. Deliverables are quantile statements about the
ρ̃ distribution, never point claims about single tasks.

### Family A — the revealed-adoption envelope (1962–2025)

Lemma 1 inverted: a task flips exactly when ρ̃(x) crosses w/c, so a flip
date t_x plus the observed path of w(t)/c(t) pins ρ̃(x) = w(t_x)/c(t_x) on
the flipped set, and bounds the unflipped set below by today's w/c. The
schedule is reconstructed as a censored lower envelope — era-sliced
quantiles, the slope at the margin, and an interquartile-spread series
(the flattening statistic the premise needs).

Members (all probed 2026-08-06, all open):
- Task content of occupations: O*NET database 30.3, CC-BY 4.0, quarterly
  archive (onetcenter.org) — REACHABLE, no registration. Deep history:
  Autor–Dorn DOT-1977 task intensities + occ1990dd crosswalks 1980–2010
  (ddorn.net, free, cite AD 2013 AER) — REACHABLE.
- Occupational employment and wages: BLS OEWS flat files 1997–2025, with
  the 1988–1995 special section (bls.gov/oes) — REACHABLE, no
  registration. Pre-1988 employment shares: Census published occupation
  tables via api.census.gov (public; key optional). IPUMS is
  registration-walled — NOT a member; routing is Census API + published
  tables only.
- The w/c denominator: FRED members via the house pipeline
  (lambda_compute2 machinery) — hedonic computer/equipment price indexes
  and equipment PPIs for c's proxy grid; OEWS/CPS wage series for w.
  FRED is house-standard (κ precedent); IDs to be title-verified before
  use, per the probe-first rule.

Honesty, committed now: flip dating from occupational task-share declines
conflates demand shifts with automation. The build uses automation-exposure
measures to isolate flips, and where isolation fails it reports bounds, not
points. The right tail is censored by construction — family A can never see
tasks the waterline hasn't reached; that is family B's job.

### Family B — direct capability mapping (2018–2025, the right tail)

Benchmark trajectories mapped to task categories give γ_M(x,t) motion for
the unflipped set — the segment A is blind to, over exactly the years the
premise is live. Human baselines come from the same benchmark suites, so
the ratio is internal to each source.

Members (all probed 2026-08-06, all open):
- Epoch AI capabilities + models datasets, CC-BY, updated 2026-08-06
  (epoch.ai/data) — REACHABLE, ZIP/CSV, no registration.
- METR task-horizon runs (`runs.jsonl`, human_minutes fields; the
  doubling-every-~7-months series) in METR/eval-analysis-public —
  REACHABLE in-repo; license file present, confirm exact terms at build.
- Eloundou et al. GPT-exposure scores by occupation/task, MIT license
  (github.com/openai/GPTs-are-GPTs, occ_level.csv and variants) —
  REACHABLE.

Honesty, committed now: the benchmark-to-task mapping is a judgment layer.
The mapping rule is published in the grid with alternatives, and every
headline statistic is reported across mapping variants — medians with
bands, never a preferred mapping alone.

### Family C — the wedge layer µ(x)

ρ̃ is the deflated schedule; C locates the deflation. Deliverables: wedge
locations by occupation (price-form vs the fortified quantity-form set),
the ρ-vs-ρ̃ relabeling, and the targeting-order test — Proposition 2's
signature that flips concentrate in high-µ tasks first, era by era.

Members:
- Union density by detailed occupation, 1983– (unionstats.com,
  Hirsch–Macpherson) — REACHABLE (site live; download format to confirm
  at build).
- Licensure/certification prevalence by occupation, CPS 2015–
  (bls.gov/cps/certifications-and-licenses.htm) — REACHABLE, free XLSX.
- Wedge-rent magnitude calibration: A&R (2026) published estimates (the
  40–50% figure already cited at The Link's Figure 4). Their openICPSR
  replication package is REGISTRATION-WALLED — per the data rule it is
  NOT a member; the build uses published-table values only, stated as
  such in the data note.

### Cross-validation, and one bonus

- A×B overlap: tasks that flipped 2018–2025 (translation, transcription,
  routine coding) have both an adoption date (A) and a benchmark-crossing
  date (B). The gap between them estimates adoption friction — The Link's
  F, the punctuated-adoption cost from the fortification remark. The
  companion hands the parent a measured F; nothing in the parent changes.
- Reinstatement, measured: DOT→O*NET revisions record task birth and
  death, and the occ1990dd panel carries them across five decades. The
  new-task margin The Link closes by assumption becomes a measured series
  — the §9 fork (reservoir thinning vs refilling) gets its accounting.
  This is the companion's highest-value single figure for the parent.

## Paper shape (sketch, not prose)

1. The object, inherited: schedule, waterline, threshold (one page; cites
   The Link's Lemma 1 and §9 fork).
2. Identification: the three families and what each can and cannot see.
3. Construction: the task panel (DOT/O*NET × occ1990dd × OEWS/Census),
   flip dating, the w/c grid.
4. The schedule, drawn: era slices 1962–2025; slope-at-margin and IQR
   flattening series. (The measured Figure 2.)
5. The right tail: benchmark-mapped motion 2018–2025; where the waterline
   stands now; the A×B friction gap.
6. The wedge layer: locations, the fortified set, the targeting-order
   test.
7. What the parent inherits: the premise's accounting (reinstatement
   series), Prediction 1's test, measured F, and the fork stated as
   evidence rather than stance.

## Honesty ledger (pre-registered)

- Fixed task space inherited from the parent — except the panel itself
  reports the new-task margin, so the closure is measured, not assumed.
- Flip dating vs demand shifts: bounds where instruments fail.
- Benchmark-to-task mapping: judgment layer, full grid disclosure.
- Right-tail censoring in A; benchmark-shaped-task bias in B (benchmarks
  oversample verifiable tasks — state it, don't correct it silently).
- Walls: openICPSR (A&R replication) and IPUMS excluded by the data rule;
  routings stated above. If a committed member goes unreachable at build
  time: stop and report, no substitution.

## Open choices (the veto window for this unit)

1. Working title: "The Schedule" (companion to "The Link") — placeholder,
   not committed.
2. Home: start as `companion/` inside this repo (own NOTES section, shared
   venv and check discipline), spin out to its own repo if it grows.
   Default unless vetoed.
3. Register: same working-paper register and voice rules as the parent
   (plain statement before compression; poetry after proof), or drier —
   default: same rules, drier density (it is a measurement paper).
4. Whether the companion carries a worked instance the way the parent
   carries the running example — default: yes, one occupation traced
   end-to-end through all three families (candidate: telephone operators
   1962→ or translators 2018→).

## Next units (in order, one per session)

1. Task panel build: DOT/O*NET × occ1990dd × OEWS pull, cached, sanity
   checks green (`companion/code/`, house pipeline pattern).
2. The w/c grid (FRED IDs title-verified) + family A envelope, first
   era-sliced figure.
3. Family B pulls + mapping grid; the right-tail figure.
4. Family C layer + targeting-order test.
5. Cross-validation (friction gap) + reinstatement series.
6. First prose: sections 1–3 against built results.
