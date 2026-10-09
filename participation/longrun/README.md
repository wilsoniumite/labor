# participation/longrun — the long-run backward holdout

`PROTOCOL.md` is the contract (an addendum to `participation/PROTOCOL.md`); `FORECASTS.md` holds the forecast sheets.
Nothing here has read a long-run outcome or regressor value: until the tag `participation-L-freeze` exists, every value
door in `code/fetch.py` and `code/ipums.py` refuses. Run everything from `participation/longrun/` with
`../../venv/Scripts/python.exe`. `participation/code` is imported, never edited (a check compares it with the
`participation-E-freeze` tag).

## Code (`code/`)

**`fetch.py`** — the one door to long-run data (L14). It holds the member list (the 38 OECD members of 2026 in the
European protocol's codes), the unseen window (L1: European members 1950-1994; the others 1950-2025 without 2020-21;
L2: the transition members from 1991), the strata, and the guard. Five halves: `meta` (OECD SDMX structure and
availability messages only, never `/data/`), `doc` (an allowlist of documentation files), `design` (the 1960 WPP total
population of the members, nothing else), `explore` (after `participation-L-freeze`, the frozen explore countries) and
`confirm` (after `participation-LE-freeze`, on a clean tree with frozen code). Value doors: OECD SDMX data (queries pin
every dimension; European members end at 1994, q at 1993), the JST file, ILOSTAT, WPP by age, Giuliano-Nunn,
Kholodilin (refuses until its file is confirmed at L2), and DBnomics and Census for the US deep study (US only).
Single-file sources are cut to the allowed countries' rows and named columns by their loader. Outcome doors open only
after a logged q download of the half, then the opening's knots record covering the requested countries, then the
loader's F_L record (stray records open nothing). Both halves refuse a premature L tag (no production skeleton, unfilled
forecast sheets, no European run, the scouts' move unrecorded) and a working copy whose frozen inputs (segments,
coverage, skeleton, split, sample list, protocol) differ from the L tag or whose FORECASTS.md changed other than by
E-L rows. Every download is logged in
`data/fetch_log.jsonl` with its SHA-256 before the raw file is cached under `data/raw/` (gitignored); a cached file is
served only with its log record.

**`ipums.py`** — the only reader of her IPUMS-International extract in `data/ipums/` (gitignored). It refuses a closed
half, any column outside her variable list plus RELATED and the attached flags (no labour, education, income,
marital-status or tenure variable), and any sample outside the frozen list in `data/ipums_samples.json` as committed in
the L tag; it reads only the rows of the samples a purpose uses (F_L, F_L nearest 1970, the pointer check, Extract B)
for open countries. It refuses while any IPUMS microdata lies under `longrun/` outside `data/ipums/`, an extract whose
DDI lists a sample outside the frozen list, and a row aged outside 20-34; it reads Extracts A and B as one or two
extracts (each CSV with the DDI of its file stem). It computes F_L (L9: share of 25-34 and 20-29 who are children of
the head, PERWT-weighted, sexes equal-weighted, group quarters and unknown relationship out, grouped ages by recorded
intervals; a grouped sample without its L2 record is unusable alone) and records it.

**`coverage.py`** — the coverage decisions of section 3 from metadata only. Per-year OECD availability probes (one
`availableconstraint` call per key and year: the four A2534 cells, U, RPI and both CPI flows; cached and logged as
`meta`), the IPUMS-I sample lists parsed from the public sample and RELATE pages, the documented JST and ILOSTAT
coverage, the L6 ladder ('extend, don't fill': rung 2 extends the chosen JST run only beyond JST's first or last year,
never into a gap), each country's chosen q segment, and the testability counts. Writes `data/coverage_probes.json`,
`data/coverage.json` (the country x year x series availability cube with provenance and the families),
`data/coverage_l2.csv` (per country: chosen segment, eligible years, memberships), `data/ipums_samples.json` and
`data/seen.json`. The values-dropping masks for JST and ILOSTAT that section 3 asks for are coded as stubs and do not
run: they download value files, which waits for her go-ahead.

**`segments.py`** — 'a splice is a fixed effect' (L7). `data/segments.csv` is the hand transcription in
`data/segments_documented.csv` (OECD `LFSNOTES_SOURCES.pdf` Tables 1 and 6, the BLS CPS technical note and
documentation page, the RORE and JST R6 documentation; one citation per row, transcription rules in the module header)
plus the q source switches the ladder makes. `breaks()` turns rows into segment starts for the variables of a
regression (from tau, or tau + 1 for lagged q); OBS_STATUS B flags and ILOSTAT source changes are added when values
arrive. Post-freeze breaks go to `data/segments_postfreeze.csv` and feed only the no-verdict run.

**`split.py`** — the one split of section 4: the members entering a verdict test, strata, pairs by 1960 population
(the design half), the US forced into EXPLORE and its partner into CONFIRM, the protocol's seed. Writes
`data/split.json`.

**`build.py`** — the variables of L3-L12 from the doors, with every query listed in `MANIFEST` (written to
`data/manifest.json`). It builds A2534 (and by sex), A5564, AW/AM 25-54, U, log q by the ladder with its segment and
source (JST rent index over CPI, else RPI over the all-items CPI extended by the COICOP 2018 CPI), the house-price q,
school attendance, cohort size and the strict-control flag, each with its list of segment starts; L3's flags are
applied at the door of each value. `country_level` holds F_L, F_L at 20-29, F_L nearest 1970, the sample flags and
Giuliano-Nunn.

**`opening.py`** — opens a half in L14's order: q, the knots from q alone (recorded with their hash), F_L (recorded),
H at the look (recorded once), then outcomes. At the look the explore countries keep their explore-opening knots.

**`specs.py`** — the tests of section 5. The piecewise basis (terciles and knots from q alone inside the chosen
segment); LR-K2 (DiD by the frozen WCR after a contrast rewrite, and by randomisation inference over H, co-primary;
the verdict statistic max(p_WCR, p_RI)); LR-Y0, C-6L and LR-C1 by WCR; size calibration against the skeleton's null
distributions; Holm within K and C-L; LR-K2's five mechanical qualifiers (leave-one-out with the US wording,
floor-group trends with H x year effects rebuilt in the RI, cohort size, control-era years, time curvature by calendar
terciles and the series-permutation placebo); the drop condition; the model-level reading and the Kaplan/Ermisch
sentence; the reading table and LR-Y0's reading note; the joint reading with the European look; the no-verdict list
(D1-L, D2-L, C-2L, C-3L, E-SCH1-L, men only, leave-one-stratum-out); the ten robustness runs.

**`inference_l.py`** — additions to the frozen `inference.py`: the contrast rewrite, the fast CR1 t for H-dependent
regressors, the H-permutation RI (exact up to 10,000 assignments), a full-refit RI, and Newey-West for the US study.

**`skeleton.py`** — the coverage-skeleton simulation of section 5, published before the look: synthetic q, U, F and
outcomes on the frozen skeleton with the DGP of section 5 (parameters from the seen European look), 2000 null worlds
at rho 0.5 and 0.9 for the size calibration tables, MDEs and standardised MDEs at rho 0.7 for the long run and the
European benchmarks, power at the MDE, the calibrated size on held-out replications, and LR-K2's identifying-variation
shares by country. Writes `data/skeleton.json`.

**`simulate.py`** — the whole pipeline end to end on synthetic worlds (null, planted, opposite) through the real
guarded doors, with the tags simulated and the network blocked: the explore opening, then `confirm.py`. Writes
`results/simulate.json`.

**`confirm.py`** — the one look (L5): refuses unless the confirm guard passes, the skeleton is committed, the explore
knots are logged and no look is committed; then P-L on every unseen country-year (primary), on the confirm half
(replication), E-L on the confirm half, and the pointer check. Writes `results/confirm_<HEAD>.json`.

**`us_study.py`** — the US deep study of section 6 (no verdict): CPS participation and the cycle (DBnomics BLS),
BEA tenant rent over goods, Census coresidence and enrolment, Newey-West estimates in levels and five-year differences.
Runs once, first, after the L-freeze; writes `results/us_study.json`.

**`europe_run.py`** — the European real-data run of LR-K2 and LR-Y0 (exploratory, no verdict), once, from a commit in
which `specs.py` and `PROTOCOL.md` are committed; a rerun is a recorded amendment.

## Checks (`checks/`)

**`check_guard.py`** — every value door refuses before the L tag with no network call and nothing logged; meta and doc
doors keep to their endpoints; the design door returns 1960 totals only; the guard with simulated tags (explore and
confirm countries, aggregates, tag order, clean tree, frozen code); L14's order; L1's caps at the door; single-file
loaders cut rows and columns; the IPUMS whitelist; log before cache; `participation/code` unchanged since its E tag;
one door only; the split reproduced.

**`check_protocol.py`** — a transcription table of section 5's tests, families, no-verdict list, robustness rows and
qualifiers, compared line by line with `specs.py`; the measures' keys (L4-L6), the window rules, strata and seed, the
extract whitelist; the basis (knots, continuity, the invariance check, the six-year rule, seams, ties); H and the
testability rule; the contrast rewrite; the verdict, calibration, reading and joint-reading rules; the segment table;
the ladder and the coverage counts.

**`check_inference.py`** — the RI check against the frozen `inference.ri` (1e-10), the fast RI against the full refit,
the contrast t against the frozen WCR, Newey-West, and the skeleton: current code, production settings, the calibrated
size within the protocol's bound on held-out replications, MDEs with benchmarks, power, identifying-variation shares.

**`check_specs.py`** — unit checks, on synthetic data, of the rules the code review of 2026-10-09 found unguarded:
post-freeze segments only in their own run; the Kholodilin coding through the panel, the qualifier and the robustness
row; per-run guards on a degenerate design; the RI's missing value; time terciles from the ranking set; every
leave-one-out row and the US wording; Holm over the frozen families; the confirm-half LR-K2 for information; D2-L's
placebo and the pooled D1; q by the frozen ladder; outcome segments in C-6L's and LR-C1's counts; Mexico 2015 out;
the US deep study on synthetic tables; the blinded debugging panel.

**`check_freeze_ready.py`** — what must hold before the tag (her L2/L3 steps): it is expected to fail until they are
done, each failing line a to-do (the IPUMS file in `data/`, the IPUMS records, Kholodilin, the masks, the school and
coresidence segment rows, the scouts' folders, the forecast sheets, the European run, the production skeleton and
simulation, her Extract B decision in `data/decisions.json`).

**`check_look.py`** — the synthetic end-to-end look: the planted world gives 'favours the floor mechanism', the opposite
world 'against ...', the null world no support; every outcome fetch after its half's knots and F_L records; records in
order; H as the rule says; the explore knots kept; all qualifiers, robustness rows and no-verdict results reported.

## Data (`data/`)

`fetch_log.jsonl` (every download and record), `coverage_probes.json`, `coverage.json`, `coverage_l2.csv`,
`ipums_samples.json`, `seen.json`, `segments_documented.csv`, `segments.csv`, `split.json`, `manifest.json`,
`skeleton.json`; `raw/` and `ipums/` are gitignored.
