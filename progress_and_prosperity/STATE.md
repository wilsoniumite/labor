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
      unit 4.

## Next actions (priority order)

1. **λ unit 3 — Family B pull:** WIOD + ICIO (route proven, unit 1) + SEA
   labor layer; world λ̂; domestic/foreign decomposition.
2. **λ unit 4 — THE GATE READ:** criteria applied to both referees; memo
   with the pass / fail / ambiguous call; PLAN.md updated either way. No
   book work that depends on the hypothesis proceeds past a fail or an
   unresolved ambiguous.
3. Then per spec: century arc (benchmarks + splice) and delivery (P1 §10
   subsection + companion note).

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
