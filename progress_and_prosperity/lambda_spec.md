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
- Hours decomposition (amended 2026-08-20, pre-read; previously
  "descriptive only"): λ̂ factors exactly as **λ̂ = H_rel × w̄_rel**, with
  H_rel = (hours embodied per $1 of machinery final output) ×
  (economy-wide average hourly compensation) — the labor content valued at
  the average wage: dimensionless, hedonics-free, and immune to
  machine-sector-specific wage rents — and w̄_rel = the embodied labor's
  average hourly compensation relative to the economy-wide average, which
  is where sector rents live. H_rel is the technical leg (recursive
  automation proper); w̄_rel is the rent-sensitive leg, read against the
  A&R 2026 anchors (rents ≈35% [19–44.5%] on automated jobs; dissipation
  offsetting 60–90% — "Automation and Rent Dissipation," QJE 141(2)). A
  constant-quality hours-per-unit variant stays descriptive and labeled
  (hedonics).

## Families

**Family A — the US long arc (BEA).** Benchmark IO tables 1947–2017
(SIC before 1997, NAICS after; historical make–use digitized), annual
supply–use 1997–2023, GDP-by-Industry value-added components (compensation,
GOS, taxes) 1947–. Import treatment is a grid axis: domestic-requirements
(US labor content only) vs total-requirements with the import proxy. Century
coverage; carries the offshoring caveat below. The BLS
employment-requirements matrices (direct + indirect jobs per $1M final
demand) join as the hours cross-check when BLS republishes them (dated
wall — sources table). Hours layer for H_rel: the BEA–BLS integrated
industry-level production accounts (hours by industry, 1997–2023;
concordance bridge to the 71-industry summary level stated at build).
Century-arc hours are best-effort and labeled.

**Family B — world content (the falsifier's referee).** OECD ICIO 1995–2022
(2025 edition, rev. Jan 2026; ~45 industries, 80 economies) paired with a
labor layer (OECD TiM or national accounts); WIOD 2016 release 2000–2014
(43 countries, 56 sectors) + socio-economic accounts; WIOD long-run
1965–2000 (25 countries, 23 sectors). World λ̂ counts foreign labor embodied
in imported intermediates: a US-only fall with a flat world series is
relocation, not automation removing the wage bill. The domestic/foreign
decomposition is a committed deliverable. Overlap windows (1995–2000,
2000–2014) are splice checks. The WIOD socio-economic accounts carry hours
by industry, so the world leg gets its H_rel decomposition from the same
pairing that supplies compensation.

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
## (amended 2026-08-20 after unit 2, PRE-READ: rent-robustness + long window)

Windows: W1 = US 1947–2023 (century arc, benchmarks + splice; **in the
gate**, not context only); W1b = US 1982→2023 (the automation-era spliced
direction — 1982 is a SIC benchmark year and the era claim under test is
"as automation deepens"); W2 = world 1995–2022 (ICIO; 1965– via WIOD-LR);
W3 = US annual 1997–2023.

Two legs per referee wherever the data pairing exists: the value leg λ̂
(compensation share — the coupling §11 names) and the quantity leg H_rel
(hours embodied valued at the economy-average wage — rent-immune). The
decomposition λ̂ = H_rel × w̄_rel is reported with every read.

- **PASS (the gate opens):** λ̂ falling AND H_rel falling, on the world
  referee (W2) and the US referee (W3 and W1b) — trend sign negative for
  the median and ≥¾ of grid members, band not straddling zero. Both legs,
  both referees: the decline must survive rent purging to count as
  recursive automation.
- **FAIL (falsifier #1 bites):** λ̂ AND H_rel flat or rising across the
  grid on the world referee. Recursive automation is weak as measured, the
  wage stays inside the substitute's price, and per PLAN the downstream
  program is rethought before a book exists. Reported with the same care
  as a pass.
- **AMBIGUOUS — including the two mixed cases, interpretations pre-named
  to prevent motivated reading later:**
  - λ̂ falling, H_rel flat: the decline is on the price leg — a
    rent-dissipation candidate (A&R 2026), not recursive automation. NOT a
    pass.
  - λ̂ flat, H_rel falling: rents are masking automation — the coupling is
    real today but rent-sustained and dissipation-fragile (A&R's own
    dynamic predicts the λ̂ fall arrives when the rents go). NOT a clean
    fail.
  - Plus the original triggers: bands straddling zero, or referees
    disagreeing in sign.
  Every ambiguous outcome: stop, report, Stella decides. No silent
  proceeding.
- 1947–1982 is reported as context with no sign requirement — machinery
  labor content may legitimately rise mid-century; the claim under test is
  the automation era.
- Timing honesty, unchanged: the read is about automation to date; the
  post-2023 AI wave is expected to be barely visible in tables ending
  2022–2023; absence of a recent kink is not evidence in either direction.

The gate read requires the century-spliced US referee (unit 3), the world
referee (unit 4), and the hours + rent layer (unit 5). If ICIO stays
blocked, the world referee runs on WIOD 2016 + WIOD-LR and says so. Rent
anchors are published values only (A&R 2026 §3.3; Stansbury–Summers
industry rent series, probed at unit 5) — openICPSR walls stay excluded.

## Honesty ledger (pre-registered)

- Offshoring vs automation: the world series referees; a domestic-only fall
  never passes the gate alone.
- Share vs hours: the share is the model object (kill condition); the
  H_rel × w̄_rel decomposition carries the diagnosis of which leg moves;
  the constant-quality hours variant stays descriptive and
  hedonics-burdened; all labeled.
- Rent contamination of the compensation share (added 2026-08-20,
  pre-read, on Stella's direction): wage rents ≈35% [19–44.5%] on
  automated jobs with 60–90% dissipation offsets (A&R 2026) make the rent
  channel first-order in both directions — dissipation mimics recursive
  automation (false pass); rent swelling masks it (false fail). The
  amended criteria require the quantity leg; the rent-purged variant uses
  published values only.
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
| BEA IO accounts (annual make–use + SUT; total requirements) | annual 1997–2023 (+2017 detail) | PULLED (unit 2) — static zips title-verified (`AllTablesIO.zip`, `AllTablesSUP.zip`, no registration); truststore/PowerShell routes; construction verified against the published IxC_TR (see `lambda/data/DATA_NOTES.md`) |
| BEA historical benchmark make–use (SIC era: 1947, '58, '63, '67, '72, '77, '82, '87, '92) | 1947–1992 | PULLED (unit 3) — per-year packages from the historical-benchmarks page (URLs in `pull_century.py`); all nine parse; compensation split exists 1967+ only (pre-1967 dropped, not imputed; NIPA-bridge recovery queued) |
| BEA GDP-by-Industry value-added components | 1947– | PULLED (unit 2) — cross-check members, report-only in v1 |
| OECD ICIO, 2025 edition (rev. 2026-01) | 1995–2022; 81 areas × 50 activities | GREEN (unit 1, 2026-08-20) — direct zips on webfs-sti.oecd.org, URL set in `lambda_prior_art.md`; harness fetcher passes the host (ReadMe pulled), local curl/PowerShell 403 → fetcher route, manual vendored download as the large-file fallback |
| OECD TiM (labor layer for ICIO) | ~1995– | NOT PROBED — landing recorded unit 1 (`oecd.org/en/data/datasets/trade-in-employment.html`); WIOD SEA is the probed-green labor pairing |
| WIOD 2016 (+SEA) | 2000–2014 | REACHABLE (rug.nl/ggdc) — SEA presence known from the literature, confirm on release page at pull |
| WIOD 2013 | 1995–2011 | REACHABLE — splice-check member |
| WIOD long-run | 1965–2000 | REACHABLE — coarse-sector caveat above |
| BLS Employment Requirements Matrices (Family A hours cross-check) | ~1997–2023; nominal + chained-2017; domestic + total | DATED WALL — all ERM tables removed by BLS 2026-02-06 (value-added error), republication at the next EP release; revisit then (unit 1) |
| BEA–BLS integrated industry accounts (hours by industry — the US H_rel leg) | 1997–2023 | NOT PROBED — unit 5 |
| A&R 2026 §3.3 published values (rent level anchor + dissipation mechanism) | level anchor, ≈35% [19–44.5%] | IN HAND — QJE 141(2) / NBER WP w32536 published tables only; openICPSR replication excluded by the data rule |
| Stansbury–Summers published industry rent series (rent time path) | ~1982–2016 | NOT PROBED — unit 5; published values only |

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

## Next units (one per session; reordered by amendment 2026-08-20)

1. Prior-art scan + ICIO route resolution — DONE 2026-08-20
   (`lambda_prior_art.md`).
2. Family A modern leg — DONE 2026-08-20 (checks ALL GREEN (11); series
   UNREAD).
3. **Century arc** (promoted into the gate): historical benchmark make–use
   1947–1992 (SIC) probed and pulled; SIC↔NAICS machinery concordance;
   splice onto 1997–2023 under the house rule; the accounting-tier long
   figure. W1b joins the PASS test.
4. **Family B:** WIOD SEA (compensation AND hours) + ICIO; world λ̂, world
   H_rel, domestic/foreign decomposition.
5. **US hours + rent layer:** BEA–BLS integrated-accounts hours → H_rel
   for W3/W1b; A&R §3.3 published values + Stansbury–Summers series
   probed; the w̄_rel series and the rent-purged variant.
6. **THE GATE READ** on the amended criteria (three referees, two legs);
   memo with the pass / fail / ambiguous call; PLAN.md updated either way.
7. Delivery, per PLAN's settled default (both venues): a results subsection
   for P1's §10 revision plus the short companion note — built once, so the
   series is citable by people who reject the theory and the gate never
   waits on P1's revision cycle.

## Amendment log (every amendment pre-read, dated)

- **2026-08-20, after unit 2, before any read (Stella's direction).**
  (1) *Rent robustness.* A&R 2026 ("Automation and Rent Dissipation," QJE
  141(2)): wage rents ≈35% [19–44.5%] on automated jobs; dissipation
  offsets 60–90% of automation's TFP gains; automation targets high-rent
  tasks. Consequence: the compensation share alone cannot distinguish
  recursive automation from rent dissipation (false pass) or rent swelling
  (false fail). Added: the exact decomposition λ̂ = H_rel × w̄_rel; hours
  members (BEA–BLS integrated accounts; WIOD SEA); rent anchors (A&R §3.3
  published values; Stansbury–Summers series); PASS/FAIL now require both
  legs; the two mixed cases pre-named as ambiguous with interpretations.
  (2) *Long window.* The century arc promoted from later-unit context into
  the gate: W1b (1982→2023 spliced direction) joins PASS; 1947–1982
  reported as context with no sign requirement. Unit order becomes
  3 = century arc, 4 = Family B, 5 = hours + rent, 6 = gate read.
