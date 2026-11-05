# The Lucas-style rewrite (2026-11-05)

`paper/main_rewrite.tex` restructures the paper as Johan asked ("more in the style of other papers"), following
Magnus's notes: the literature survey (old Section 2) is cut, the model is introduced systematically, and the research
question is stated in the introduction. Lucas (1978) is the model of exposition: an informal description of the
economy, then a definition of equilibrium, then its characterization. `paper/main.tex` is unchanged until Stella has
read the rewrite.

It compiles with the same preamble and figures as `main.tex` (`latexmk -pdf main_rewrite.tex` in `paper/`).

## Structure

| | Section | Built from |
|---|---|---|
| 1 | Introduction | new history opening (Keynes, Leontief, three AI papers), then main.tex L72-86 verbatim, one "This paper argues" sentence, a new roadmap |
| 2 | Description of the economy | new, after Lucas's Section 2 (agents, households, firms, land, government, what is easy and what is hard) |
| 3 | Definition of equilibrium | primitives sentence in Lucas's form; Assumptions 1-5, the cost system, Definition 1, Definitions 2-3; Table 1 (notation) |
| 4 | Equilibrium | Lemma 1, Propositions 1-3 with proofs, Lemma 2, Theorem 1 (old Lemma B.1), Corollary 1 |
| 5 | Purchasing power and income | old Section 6 with Proposition 4, Corollary 2, Proposition 5 |
| 6 | Distribution: rent taxation and a uniform transfer | old Section 7, Proposition 6, Corollary 3 |
| 7 | A numerical economy and an automation path | old Appendix B's instance, with Table 2 and Figure 3 |
| 8 | Measurement | old Section 9, verbatim |
| 9 | History and stabilizers | old Sections 8 and 10 |
| 10 | Artificial intelligence and conclusion | old Sections 11 and 12 |
| A-F | Proofs; extensions; expenditure shares; fiscal transition; human-required tasks; accounts | old Appendices A-F, reorganized |

## How the source records where each paragraph came from

Every paragraph of `main_rewrite.tex` is preceded by a LaTeX comment:

- `% from main.tex L<n>, verbatim` — the authors' words, unchanged;
- `% from main.tex L<n>, edited: <old> -> <new> (<reason>)` — the authors' words with the stated edit;
- `% NEW (<source>)` — text written for the rewrite, from the design (`design_synthesis.md`), the build brief, or
  the drafts Stella approved (`drafts/`);
- `% Review edit (<id>): <reason>` — an edit made after the checks (ids in `CHECKS.md`; D-numbers are the build's
  decisions in `ASSEMBLY.md` §5).

The comments do not print. `tools/provenance_view.py` renders the rewrite with each paragraph marked (unchanged,
edited with an inline diff, or new) and lists every sentence of `main.tex` that is not in the rewrite word for word.

## Files

- `BRIEF.md` — the build brief: the structure, the rules (port verbatim; never re-voice), the six fixes F1-F6 from
  the math checks, the citation placements, the two asides.
- `design_synthesis.md` — the design the rewrite implements: the model section's LaTeX, the restated results and
  the changes to their proofs, the claims the design relies on.
- `math_verdicts.md` — the five math checks (C1-C5) of the design, which produced F1-F6.
- `notes/` — each build part's record: every edit to the authors' text with its reason, every dropped sentence.
- `ASSEMBLY.md` — the assembly: part order, references kept, dropped and added, labels, the compile, and the 110
  decisions D1-D110 the parts raised, with their suggested answers.
- `CHECKS.md` — two rounds of checks (math, sources, numbers, read-through; then verification of the fixes and a
  second read), every finding and its disposition.
- `drafts/` — the introduction (v2) and Section 2 (v3) as Stella approved them in session.
- `tools/` — the review scripts (below). `apply_defaults.py` and `apply_findings.py` are the exact edits of the
  review round, kept as a record.

Paths in these records that begin `SP/` refer to the build session's scratch directory, which was not kept; the
files that matter are copied here.

## Checks

From `pinning/`:

```
python3 checks/lint_tex_structure.py paper/main_rewrite.tex
python3 docs/rewrite/tools/port_fidelity.py paper/main.tex paper/main_rewrite.tex
python3 checks/check_interior_rewrite.py
python3 checks/check_rewrite_numbers.py
python3 docs/rewrite/tools/provenance_view.py paper/main.tex paper/main_rewrite.tex OUT.html "title"
```

- `lint_tex_structure.py` (the repository's) — labels, references, environments and figures resolve.
- `port_fidelity.py` — every paragraph whose comment says "verbatim" is in `main.tex` word for word.
- `check_interior_rewrite.py` — `check_interior.py` re-pointed at the rewrite: the same checks, expected values and
  tolerances, with its text anchors moved to where the material now stands.
- `check_rewrite_numbers.py` — recomputes every number printed in Sections 5-7, Table 2, Figure 3's caption and
  Appendix D from `code/appendix_b.py` and compares it with the printed value.

## Decisions

The build's decisions D1-D110 (`ASSEMBLY.md` §5) stand at their suggested answers, except:

- applied at review: D6, D7 (repeats dropped), D25 (workers of measure zero), D30 (F5's sentence printed twice, not
  three times), D73 ("stationary"), D74, D76 (pointers), D91 ("interior margin" throughout), D101 (D.2's repeat),
  D102 (the CES elasticity is epsilon, not sigma), D103 (the basket's quantities z_g, z_h, z_H), D106 (D.1's
  comparison with tau_w = d = 0);
- not applied: D90 and D108 (two local symbols that share a letter with another object far away; no confusion);
  D64 (Ricardo and Malthus are named without years and stay out of the references); D100 (Appendix D keeps the
  authors' title);
- open for Stella: D13 (whether Theorem 1's remark shows the second configuration that exists without the user-cost
  clause); D1 (the abstract is the old one, with one word changed, R22); D70-D72 (Future Work, cut to 372 of 456
  words); D55 and D12 (Figure 3's legend and main.tex's header comments, at adoption).
