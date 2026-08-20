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
**State as of:** 2026-08-20 (founding day, sessions 1–2).

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

## Next actions (priority order)

1. **λ unit 1 — prior-art scan + ICIO routing:** vom Lehn–Winberry, KORV,
   Karabarbounis–Neiman, Elsby–Hobijn–Şahin, Pasinetti's vertically
   integrated sectors, "labor embodied in investment goods"; resolve the
   ICIO 403 (Data Explorer bulk / direct zip) or declare the WIOD fallback.
2. **λ unit 2 — first pull, Family A:** BEA annual supply–use 1997–2023 +
   VA components; the sector grid; first λ̂_US series; checks green before
   anything is read.
3. **λ unit 3 — Family B pull:** WIOD (+ICIO if unblocked) + SEA labor
   layer; world λ̂; domestic/foreign decomposition.
4. **λ unit 4 — THE GATE READ:** criteria applied to both referees; memo
   with the pass / fail / ambiguous call; PLAN.md updated either way. No
   book work that depends on the hypothesis proceeds past a fail or an
   unresolved ambiguous.
5. Then per spec: century arc (benchmarks + splice) and delivery (P1 §10
   subsection + companion note).

## File map

```
progress_and_prosperity/
├── STATE.md          ← you are here; start here next session
├── PLAN.md           the program: phases, chapter map, papers P1–P5, provenance ledger
├── lambda_spec.md    Phase 0 gate spec, pre-registered 2026-08-20
└── (lambda/          code, data, figures — created at the pull, not before)
```

## Repro notes

- No code in this thread yet. When the pull starts: shared repo venv
  (`./venv/Scripts/python.exe`), house pipeline patterns (probe-first URLs,
  cache, validation ledgers, BLOCKED-and-stop).
- Network, recorded 2026-08-20: OECD ICIO dataset landing returns 403 to the
  harness fetcher; BEA and rug.nl/ggdc (WIOD) open. Sibling-thread precedent
  says several academic hosts block local curl while the harness fetcher
  passes — expect the pull scripts to need per-host routing, documented when
  built.
