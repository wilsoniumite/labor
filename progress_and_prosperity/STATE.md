# STATE — resume point for the next session

**Project:** Progress and Prosperity — the book (four parts, 17 chapters,
test-written as blog posts) and the papers around it (P1–P5, the λ series,
three data notes). Folder founded 2026-08-20. Governing docs: `PLAN.md`
(the program — phases, chapter map, paper sketches, provenance ledger) and
`lambda_spec.md` (Phase 0's gate, pre-registered). This file is the session
entry point; the PLAN is the program.
**Collaboration:** same contract as the sibling threads — Stella writes the
book posts; papers and data are joint with Claude drafting; working format,
sequencing, and drafting decisions delegated to Claude; direct critique
preferred. One work unit per session; checks gate absolutely; verify-lists
are veto windows (defaults stand unless vetoed).
**State as of:** 2026-08-20 (founding day: gates, founding, and λ unit 1).

## Where things stand

**Phase 0 — the gate — is IN PROGRESS.** Done on founding day:

1. **Provenance ledger settled:** every s? row confirmed Stella and flipped;
   the legend records the confirmation date. The preface can now be written
   from the table without pending rows.
2. **Working title collision-checked, CLEAR** (PLAN header updated): nearest
   matches are Earl Beach's self-published 1999 *Progress and Prosperity*, a
   2024 essay collection *On Progress and Prosperity* (Siegel et al.), and an
   antiquarian ~1900s volume. No prominent active claimant; the *Progress
   and Poverty* echo is unencumbered.
3. **λ assembly SPEC'D** (`lambda_spec.md`, pre-registered before any pull):
   primary object = vertically integrated labor-compensation share of
   machinery final output (nominal, deflator-free, the §11-kill-condition
   object); world content referees the falsifier (offshoring honesty);
   read criteria committed (pass / fail / ambiguous, with the timing-honesty
   clause); machine-sector definitions run as a grid. Source probes
   2026-08-20: BEA green, WIOD green, **OECD ICIO amber (landing 403 via
   harness fetcher; bulk-host route to resolve at pull; WIOD-only fallback
   armed)**. The spec serves double duty as pinning §10's assembly (2).
4. **Papers section expanded** (Stella, from a parallel chat, 2026-08-20):
   P1 recorded as SSRN working draft (Aug 2026) with queued revisions
   (human-capital subsection; provisioning identity promoted to spine; Lean
   λ > 0). P2's theory core stated — the provisioning identity
   Y_S = wL + τR + B and the endogenous dependency floor, twin-equilibrium
   result; **standing provenance obligation: the ChatGPT-side seed is
   credited in P2's AI-use note**. λ delivery default settled: both venues
   (P1 §10 results subsection + short companion note); spec updated to
   match.
5. **λ unit 1 DONE — prior-art scan + ICIO routing**
   (`lambda_prior_art.md`, committed same day). Existence verdict: build
   ours — the nearest existing object is the BLS employment-requirements
   matrix (the hours version), currently REMOVED by BLS pending an error
   correction; adopted as Family A's future hours cross-check. **ICIO
   routing RESOLVED GREEN:** direct zips on webfs-sti.oecd.org, harness
   fetcher passes the host (proven on the 2025 ReadMe), URL set recorded
   verbatim; local curl/PowerShell 403 → fetcher route with a manual
   vendored-download fallback for the large zips. 2025 edition = 1995–2022,
   81 areas × 50 activities; machine-set codes concordanced (C26/C27/C28
   narrow; J62_63 medium; C31T33 coarse-broad; leasing BEA-only). Spec
   sources table updated in place.
6. **λ unit 2 DONE — Family A built, checks ALL GREEN (11)** (2026-08-20).
   `lambda/`: pull + compute + reconstruction diagnostic + check battery;
   `lambda/data/lambda_us_family_a.csv` (1997–2023; {narrow, medium, broad}
   × {tot, dom} λ̂ members + dom_purch, direct shares, non-wage resolution)
   and the banded figure — both **UNREAD**; the gate read is unit 4.
   Construction verified, not assumed: the published IxC_TR is reproduced
   to 1.3e-04 from Make + published DR (the SUT-framework tables miss by
   ~0.3 — the published TR's basis is the MU after-redefinitions framework;
   `lambda/code/diag_reconstruction.py` is the record). Exact full-VA
   resolution identity holds at 1.4e-06; ρ(BW) ≤ 0.52 (net reproduction —
   the model's a < 1, empirically). Deferred axes recorded in
   `lambda/data/DATA_NOTES.md` (self-employment; import-matrix purge;
   before-redefinitions; 2017-detail/repair).
7. **Course correction (Stella, 2026-08-20, before unit 3) — SPEC AMENDED
   PRE-READ.** Two points, both accepted: (i) *rent wages* — A&R 2026
   ("Automation and Rent Dissipation," QJE 141(2); rents ≈35% [19–44.5%]
   on automated jobs, dissipation offsets 60–90%) means the compensation
   share alone can false-pass (rent dissipation mimics recursive
   automation) or false-fail (rent swelling masks it). The spec now
   commits the exact decomposition **λ̂ = H_rel × w̄_rel** (hours leg
   rent-immune; rent leg read against A&R + Stansbury–Summers published
   values), and PASS/FAIL require both legs, with the two mixed cases
   pre-named as ambiguous. (ii) *window too short* — the century arc is
   promoted into the gate: W1b (1982→2023 spliced direction) joins PASS;
   1947–1982 is context. Unit order is now 3 = century arc, 4 = Family B
   (+SEA hours), 5 = US hours + rent layer, 6 = THE GATE READ. Amendment
   log at the foot of `lambda_spec.md`.
8. **λ unit 3 DONE — century arc built, checks ALL GREEN (10)**
   (2026-08-20). Nine benchmark vintages parsed (1947–1992) from BEA's
   historical packages; compensation λ̂ points **1967–1992** (six, incl.
   both W1b anchors 1982 and 1992); 1947/1958/1963 carry no compensation
   split at the 85-level and are DROPPED from λ̂, not imputed (parses
   validated by the resolution identity; NIPA-bridge recovery queued).
   Identification is self-verifying (GDP anchor + dominant-component rule;
   externally cross-checked vs HIST components at 0.9%/0.7% for 1987/1992).
   Splice 1992 SIC → 1997 NAICS: ratio 0.9204, the classification-break
   step, stated on the figure with BEA's "should not be used as a time
   series" caveat. Outputs `lambda/data/lambda_us_century.csv` +
   `lambda/figures/lambda_us_century.png` — **UNREAD** (gate read =
   unit 6). SIC-era two-digit published TRs are NOT reproduced by the
   unit-2 algebra (recon 0.19–0.25, old conventions) — published TR used,
   recorded report-only.
9. **λ unit 4 DONE — the world referee built, checks ALL GREEN (11)**
   (2026-08-20). World λ̂ and H_rel from the global Leontief inverse:
   WIOD 2013 (1995–2009 labor-kept) + WIOD 2016 (2000–2014); grid
   {COMP, LAB} × {ROW=0, ROW=mean} × sector sets; world and US-purchases
   views with the US/foreign labor decomposition (the offshoring
   discriminator — foreign share of US machinery purchases spans
   [0.26, 0.57] over the window, UNREAD as to trend). Exact global
   identity ≤ 8e-15 every kept year; vintage overlap 2000–2009 agrees to
   0.019. **Two data-forced amendments, logged in the spec:** the LR-WIOD
   world leg is downgraded (its SEA has no labor variables → W2 world
   window = 1995–2014; deep history rides on the US century arc), and
   ICIO stays parked (data zips 403 all scriptable clients; manual
   vendored download = five clicks, decided before the gate read or not
   at all). SEA13's 2010–11 excluded at 24% labor coverage, flagged.
   Outputs `lambda/data/lambda_world_family_b.csv` +
   `lambda/figures/lambda_world_family_b.png` — **UNREAD** (gate read =
   unit 6).
10. **λ unit 5 DONE — US hours + rent layer, checks ALL GREEN (9)**
   (2026-08-20). H_rel for the US referee 1997–2023: block-level hours
   (28 blocks, BEA-71↔ISIC-56, bridge coverage exactly 1.0) on the unit-2
   requirements — WIOD SEA USA levels 2000–2014, KLEMS-index tails, seams
   ≤ 11.4% yoy; decomposition λ̂ = H_rel × w̄_rel exact (2.2e-16); W1b's
   H leg = NAICS segment only, stated. Rent layer: S&S BPEA replication
   (Brookings-hosted public — machinery industries map 1:1) → industry
   ρ = rents/compensation and λ̂_purged 1997–2016 (max purge 0.086);
   A&R §3.3 level anchor recorded. Outputs
   `lambda/data/lambda_us_hours_rent.csv` + figure — **UNREAD**. All
   three referees and both legs now exist; unit 6 is the gate read.
11. **λ unit 5b DONE — ICIO extension live, checks ALL GREEN (14)**
   (2026-08-20). Stella performed the five-click manual download; four of
   five SML zips supplied (**2006-2010_SML.zip still missing** — gap
   flagged in C11, WIOD covers it; drop it in `lambda/data/cache/` and
   rerun `compute_icio.py` any time). 23 ICIO years built on the unit-4
   engine: exact identity ≤ 5.7e-14; labor vintages labeled per year
   (sea13 1995–99 / sea16 2000–14 / **frozen2014 2015–22** — the
   structure-only member, all post-2014 movement from A + trade + demand,
   none from share drift). ICIO↔WIOD16 overlap: 0.031 max over 10 years.
   W2's world window is back to **1995–2022** (with the labeled frozen
   tail and the 2006–10 gap). Files moved to the gitignored cache.

**Phase 0 remainder:** the λ pull-and-read (next actions below); (S) the
education test post while the conversation is warm; (us) P1 absorbing
revision as usual (that work lives in `../the-link-revision/`, not here).

## Verify-list — 2026-08-20: the founding unit (veto window, current)

- [ ] `lambda_spec.md`'s five open choices, defaults live unless vetoed:
      world series as falsifier referee; VI compensation share as primary
      object; the read thresholds (¾-of-grid, sign-of-trend,
      no-zero-straddle); Family C's occupational extension deferred past
      the gate read; home = this folder with code/data under `lambda/`.
- [ ] The PLAN title line rewritten from "collision check pending" to the
      checked-clear record.
- [ ] This file's convention: STATE.md is the canonical session entry point
      for the thread; PLAN.md stays the program doc and is edited by both of
      us (Stella: phases, chapters, papers; Claude: status marks and
      reconciliations, logged here).
- [ ] Unit 1's delegated calls: the existence verdict (build, cite the
      Pasinetti/Leontief lineage); BLS ERM adopted as secondary member
      behind its dated wall; the ICIO fetcher route with manual-download
      fallback; f_M investment-flow weighting (vom Lehn–Winberry) deferred
      to build as a grid-axis candidate.
- [ ] Unit 2's delegated calls: MU after-redefinitions basis (forced by the
      reconstruction gate); proportional import purge for the domestic
      variant (import-matrix variant queued); final-use weights = all
      F-columns except inventories (F030) and imports (F050), clipped ≥ 0;
      summary-level sets with 514 (the summary code, not 518) and repair
      only at 2017 detail; raw-zip cache .gitignored while the derived CSV
      is committed as the checks' input; the figure stays UNREAD until
      the gate read.
- [ ] The 2026-08-20 amendment's delegated calls (veto window before unit
      3 builds on them): H_rel defined as hours embodied valued at the
      economy-average wage (machine-sector rents isolated in w̄_rel,
      economy-wide rent trends common-mode); 1982 as the automation-era
      start for W1b; A&R §3.3 + Stansbury–Summers as the published-values
      rent anchors; the two mixed-case interpretations as pre-named;
      century arc's 1947–1982 as context with no sign requirement.
- [ ] Unit 3's delegated calls: self-identifying parsing (GDP anchor with
      per-vintage scale detection; compensation = dominant VA-block row);
      pre-1967 points dropped rather than imputed (NIPA-bridge recovery
      queued); ratio splice at 1992→1997 with the 0.9204 step stated;
      published TR trusted over the failed 2-digit reconstruction
      (report-only); SIC machine set 43–58 with the +instruments (62)
      variant.
- [ ] Unit 4's delegated calls: LR-WIOD downgrade accepted as data-forced
      (W2 world window = 1995–2014) rather than adding a non-WIOD labor
      layer for 1965–1995; ICIO parked behind the manual download with the
      decision deadline at the gate read; SEA13 2010–11 excluded at 24%
      coverage; ROW carried as a {0, mean} band; zero-GO sectors dropped
      with mass reported; the 2013↔2016 vintage overlap as report-only.
- [ ] Unit 5's delegated calls: hours as a block-level row vector (28
      blocks, no re-inversion) with WIOD-SEA levels + KLEMS-index tails
      (labeled mechanical extension); S&S replication adopted as a member
      (Brookings-hosted public zip — no wall, unlike openICPSR); ρ defined
      as implied rents / compensation; unmapped industries carry the
      aggregate ratio; W1b's H leg NAICS-segment-only; A&R stays a level
      anchor, never an industry series.
- [ ] Unit 5b's delegated calls: frozen-2014 shares as the 2015–22 labor
      layer (structure-only, labeled) rather than extrapolating shares;
      SEA13's coarser ISIC3 map for 1995–99 (C26/C27 pool into 30t33);
      DPABR kept in final demand, INVNT excluded; the 2006–10 gap accepted
      pending the fifth zip; ICIO zips kept out of git via the cache.

## Next actions (priority order)

1. **λ unit 6 — THE GATE READ** on the amended criteria (three referees,
   two legs); memo with the pass / fail / ambiguous call; PLAN.md updated
   either way. No book work that depends on the hypothesis proceeds past a
   fail or an unresolved ambiguous. (Stella: the ICIO manual download —
   five clicks — extends the world window to 2022 if done before this.)
2. Then per spec: delivery (P1 §10 subsection + companion note).

## File map

```
progress_and_prosperity/
├── STATE.md          ← you are here; start here next session
├── PLAN.md           the program: phases, chapter map, papers P1–P5, provenance ledger
├── lambda_spec.md       Phase 0 gate spec, pre-registered 2026-08-20
├── lambda_prior_art.md  unit 1: existence verdict, literature, ICIO routing
└── lambda/              unit 2 build (Family A)
    ├── code/            pull_family_a.py · compute_family_a.py · diag_reconstruction.py
    ├── checks/          check_family_a.py — ALL GREEN (11); gates the build
    ├── data/            lambda_us_family_a.csv · DATA_NOTES.md · cache/ (.gitignored; the pull script recreates it)
    └── figures/         lambda_us_family_a.png (UNREAD until unit 4)
```

## Repro notes

- No code in this thread yet. When the pull starts: shared repo venv
  (`./venv/Scripts/python.exe`), house pipeline patterns (probe-first URLs,
  cache, validation ledgers, BLOCKED-and-stop).
- Network, recorded 2026-08-20 (updated at unit 1): oecd.org pages 403 every
  non-browser client but load in the in-app browser; the file host
  webfs-sti.oecd.org 403s local curl and PowerShell yet serves the harness
  fetcher (proven on the 2025 ReadMe, 320KB). BEA and rug.nl/ggdc open.
  Pull scripts need per-host routing — fetcher route for OECD files, manual
  vendored download as the large-file fallback — documented when built.
