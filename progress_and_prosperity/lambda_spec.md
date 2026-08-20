# λ assembly spec — the labor content of machine production

Status: DESIGN SPEC, written 2026-08-20 (P&P session 1). Nothing pulled, no
code, no prose. Source reachability probed live this day via the harness
fetcher; every load-bearing member green except one amber (ICIO — landing page
403; routing deferred to the pull session, statuses below). This document is
the pre-registration for the pull and the read: the object, the grid, and the
read criteria are committed here before any series is assembled.

Double duty, recorded: this is Phase 0's gate in `PLAN.md` (falsifier #1 —
"if λ isn't falling, everything downstream gets rethought before a book
exists") and assembly (2) of `the-link-revision/paper/pinning.html` §10,
marked there [spec'd, unbuilt], with §11's first kill condition reading on it.
One build serves both; the paper's §10 sentence is the contract.

Inherited rules (house): live public data only, no substitution or
approximation — stop and report if a committed member is unreachable at build
time. Contestable measurement choices go through a rule grid — all defensible
variants, medians with bands, never a preferred pick alone (κ precedent).
Probe-first URLs. Splices under the standing splice discipline. Checks gate
absolutely. Figure output is tier-labeled **accounting** (book figure-spine
rule: bands everywhere).

Disambiguation, once: λ here is the machine-recipe labor coefficient of
`c = ac + λw + ℓr` (pinning §4). It is not λ_C/λ_R of
`link-repo/code/lambda_compute2.py` (wage-linkage of consumption financing
and tax revenue — Appendix F objects that share the letter). Code and data
for this assembly live under `progress_and_prosperity/lambda/` to keep the
namespaces apart.

## The object

The model prices machine services from their recipe: c = ac + λw + ℓr; in
general form **c** = **Ac** + **Λ**w + **Br**, so
**c** = (I−**A**)⁻¹(**Λ**w + **Br**) (Appendix C). §10 names the empirical
counterpart: the resolution of a unit of machine-intensive final output into
wages versus terminal rents after recursively removing intermediates.

**Primary series, committed — λ̂(t), the vertically integrated
labor-compensation share of machinery final output:**

    λ̂(t) = v_w(t)′ (I − A(t))⁻¹ f_M(t)

where v_w = compensation of employees per dollar of gross output by industry,
A = intermediate-requirements matrix, f_M = one dollar of final demand for
the machine-sector set (grid-defined below). All terms nominal: the object is
a share, and no deflator enters anywhere — that is a design advantage, not an
accident.

Model mapping, stated plainly: λ̂ is the counterpart of λw/((1−a)c) — the
wage bill inside the substitute's delivered price with the recursion resolved
(= λρ*/(1−a) at the margin). Any value measure confounds λ with w/c; here the
confounding is the object, not a nuisance, because §11's kill condition — "the
wage stays inside the substitute's price" — is a claim about exactly this
share. Recursive automation appears as λ̂ falling.

**Companion series** (built from the same pull, reported beside, never
substituted for the primary):

- Direct share: compensation over gross output within the machine-sector set,
  no inverse — locates where a fall happens (the sector's own wall vs
  upstream).
- The other half of the resolution: gross operating surplus + production
  taxes through the same inverse — "versus terminal rents," as far as IO
  accounting can carry it. Splitting that residual into produced-capital
  services vs terminal rent is κ-assembly territory and is NOT attempted in
  v1; stated as such wherever the residual is shown.
- Hours variant: total hours embodied per $1,000 of constant-quality
  machinery final demand (where hours-by-industry exist). Descriptive only:
  it inherits the hedonic deflator and falls partly by Moore's law; it is
  not the falsifier and is labeled so.

## Families

**Family A — the US long arc (BEA).** Benchmark IO tables 1947–2017
(SIC before 1997, NAICS after; historical make–use digitized), annual
supply–use 1997–2023, GDP-by-Industry value-added components (compensation,
GOS, taxes) 1947–. Import treatment is a grid axis: domestic-requirements
(US labor content only) vs total-requirements with the import proxy. Century
coverage; carries the offshoring caveat below. The BLS
employment-requirements matrices (direct + indirect jobs per $1M final
demand) join as the hours cross-check when BLS republishes them (dated
wall — sources table).

**Family B — world content (the falsifier's referee).** OECD ICIO 1995–2022
(2025 edition, rev. Jan 2026; ~45 industries, 80 economies) paired with a
labor layer (OECD TiM or national accounts); WIOD 2016 release 2000–2014
(43 countries, 56 sectors) + socio-economic accounts; WIOD long-run
1965–2000 (25 countries, 23 sectors). World λ̂ counts foreign labor embodied
in imported intermediates: a US-only fall with a flat world series is
relocation, not automation removing the wage bill. The domestic/foreign
decomposition is a committed deliverable. Overlap windows (1995–2000,
2000–2014) are splice checks.

**Family C — the operating margin.** The paper's λ includes operation and
maintenance. IO resolution sees the operating sectors that are sectors —
repair & maintenance (811), software publishers / systems design / hosting
(511, 5415, 518), machinery leasing (532) — and these enter through the grid
definitions below. Operation labor inside *using* industries is invisible to
IO and is out of scope for v1; an occupational family (OEWS
machine-operation and maintenance occupations) is the flagged extension,
built only if the gate read survives.

**Machine-sector grid axis** (with SIC/ISIC concordances at build):

- narrow: machinery, computer & electronic, electrical equipment
  (NAICS 333–335 / SIC 35–36 / ISIC 26–28)
- medium: narrow + software & IT services (511, 5415, 518)
- broad: medium + repair (811) + machinery/equipment leasing (532)

WIOD-LR's 23 sectors bound the narrow set's resolution there (ISIC 29–33
block); coarse members are labeled coarse in the band, never silently mixed.

Other grid axes: import treatment (A); self-employment adjustment
(compensation as published vs proportional proprietor-labor imputation);
BEA before- vs after-redefinitions where both are published; government
machinery purchases in or out of f_M.

## Read criteria — committed before the pull

Windows: W1 = US 1947–2023 (century arc, benchmarks + splice); W2 = world
1995–2022 (ICIO; 1965– via WIOD-LR); W3 = US annual 1997–2023.

- **PASS (the gate opens):** world λ̂ trending down over W2 and US λ̂ down
  over W3 — trend sign negative for the median and for ≥¾ of grid members,
  with the band not straddling zero over the window.
- **FAIL (falsifier #1 bites):** world λ̂ flat or rising across the grid.
  Then recursive automation is weak as measured, the wage stays inside the
  substitute's price, and per PLAN the downstream program is rethought
  before a book exists. This outcome is reported with the same care as a
  pass.
- **AMBIGUOUS:** bands straddle zero, or the US and world referees disagree
  in sign → stop, report, Stella decides. No silent proceeding.
- Timing honesty, committed now to prevent motivated reading later: the
  read is about automation to date. The post-2023 AI wave is expected to be
  barely visible in tables ending 2022–2023; absence of a recent kink is
  not evidence in either direction.

The gate read requires both referees (A and B). If ICIO stays blocked, the
world referee runs on WIOD 2016 + WIOD-LR and says so.

## Honesty ledger (pre-registered)

- Offshoring vs automation: the world series referees; a domestic-only fall
  never passes the gate alone.
- Share vs hours: the share is the model object (kill condition); the hours
  series is descriptive and hedonics-burdened; both labeled.
- Machine goods vs machine services: IO measures the production of machines
  and the listed operating sectors, not machine services directly; the
  user-cost bridge (Appendix C's δ, d) is stated, not estimated, in v1.
- Sector definition: grid, no preferred member.
- Classification splices: SIC→NAICS 1997, ISIC revisions, ICIO/WIOD edition
  boundaries — house splice rule, overlap windows reported.
- Pre-1997 benchmark heterogeneity: older layouts and redefinition regimes;
  the century arc is assembled last and flagged where formats forced choices.
- Compensation misses proprietors' labor: adjustment is a grid axis, not a
  correction applied silently.
- What v1 cannot see: operation labor inside using industries (Family C
  note); own-account software; the produced-vs-terminal split of the
  non-wage residual.

## Sources (probed 2026-08-20 via harness fetcher)

| Member | Coverage | Status |
|---|---|---|
| BEA IO accounts (benchmarks; annual supply–use; total/domestic requirements) | benchmarks 1947–2017; annual 1997–2023 | REACHABLE — landing green; tables live in the interactive app with no-registration XLSX/CSV; flat-file and API routes to title-verify at pull |
| BEA GDP-by-Industry value-added components | 1947– | REACHABLE — XLSX + archive, no registration |
| OECD ICIO, 2025 edition (rev. 2026-01) | 1995–2022; 81 areas × 50 activities | GREEN (unit 1, 2026-08-20) — direct zips on webfs-sti.oecd.org, URL set in `lambda_prior_art.md`; harness fetcher passes the host (ReadMe pulled), local curl/PowerShell 403 → fetcher route, manual vendored download as the large-file fallback |
| OECD TiM (labor layer for ICIO) | ~1995– | NOT PROBED — landing recorded unit 1 (`oecd.org/en/data/datasets/trade-in-employment.html`); WIOD SEA is the probed-green labor pairing |
| WIOD 2016 (+SEA) | 2000–2014 | REACHABLE (rug.nl/ggdc) — SEA presence known from the literature, confirm on release page at pull |
| WIOD 2013 | 1995–2011 | REACHABLE — splice-check member |
| WIOD long-run | 1965–2000 | REACHABLE — coarse-sector caveat above |
| BLS Employment Requirements Matrices (Family A hours cross-check) | ~1997–2023; nominal + chained-2017; domestic + total | DATED WALL — all ERM tables removed by BLS 2026-02-06 (value-added error), republication at the next EP release; revisit then (unit 1) |

Walls policy: BEA's API key is free registration — v1 routes through
no-registration downloads; if the key becomes necessary, that is an explicit
ask, not a silent signup. IPUMS/openICPSR-style walls: excluded as ever.

## Prior-art check (first next-unit, before any pull)

The series may already exist in pieces. Scan before building: vom Lehn &
Winberry (investment network); Krusell–Ohanian–Ríos-Rull–Violante (equipment
prices); Karabarbounis–Neiman and Elsby–Hobijn–Şahin (labor-share
measurement, incl. self-employment and depreciation choices worth stealing);
Pasinetti's vertically integrated sectors (the λ̂ formula's lineage beside
Leontief/Sraffa); anything under "labor embodied in investment/capital
goods." If a published series covers a window, the pull becomes replication
plus extension, and the paper cites instead of rediscovering.

## Open choices (the veto window for this unit)

1. Falsifier referee = world series, US as co-referee (default above) — or
   US-only.
2. Primary object = vertically integrated compensation share (default) — or
   the hours variant promoted.
3. Read thresholds (¾-of-grid, sign-of-trend, no-zero-straddle) — numbers
   vetoable.
4. Family C occupational extension deferred past the gate read (default) —
   or in v1.
5. Home: this folder, code/data under `progress_and_prosperity/lambda/`
   (default); the standalone short paper's title decided at drafting, not
   now.

## Next units (one per session)

1. Prior-art scan + ICIO route resolution (unblock or declare, with the
   WIOD-only fallback armed).
2. First pull, Family A modern leg: annual supply–use 1997–2023 + VA
   components; narrow/medium/broad grid; first λ̂_US series; checks green.
3. First pull, Family B: WIOD (and ICIO if unblocked) + SEA labor layer;
   world λ̂ + domestic/foreign decomposition.
4. **The gate read**: criteria above applied to both referees; memo with
   the pass/fail/ambiguous call; PLAN.md updated either way.
5. Century arc: benchmarks 1947–1997 spliced under the house rule; the
   accounting-tier figure (US arc + world overlay, banded).
6. Delivery, per PLAN's settled default (both venues): a results subsection
   for P1's §10 revision plus the short companion note — built once, so the
   series is citable by people who reject the theory and the gate never
   waits on P1's revision cycle.
