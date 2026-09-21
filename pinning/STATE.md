# STATE — pinning (the paper; resume point for the next session)

**Project:** *Pinning the Wage to Scarcity and Technology* (Johan Båge and Stella
Wilson), being prepared for submission.
**Collaboration:** her TeX is the working file. Claude ports edits exactly once, produces
word diffs (`../tools/word_diff_report.py`) and reading views
(`../tools/reading_view.py`), never re-voices, and flags slips for her one-word
decisions. Checks gate absolutely (`README.md` lists them).
**State as of:** 2026-09-21 — the interior revision landed. The folder dates from the
2026-09-04 restructure; its history is `../dynamics/STATE.md` logs 1–52 (the revision
thread, under its old name the-link-revision) and the former `effort-accounting/STATE.md`,
both at tag `pre-cleanup-2026-09-04`.

## Where things stand

- `paper/main.tex` is the interior revision of 2026-09-21, ported verbatim from her
  `Downloads/wages-and-scarcity-interior-source.zip` (`v5_interior.tex`, 104,177 bytes)
  plus the repository's one standing edit: the AI-use note names the repository ("the
  code and data are public at" the GitHub URL). The bundle had started from her raw
  `v5 (3).tex` and so arrived without that clause; it was re-applied, not re-voiced.
- What the revision does, in its own summary (`docs/interior_revision_2026-09-21.md`,
  the ChatGPT-side handoff note, kept verbatim): the flat-capability proposition is
  replaced by an exact interior category-price formula, general price bounds, and an
  income identity. Section 6 becomes "Purchasing power at an interior margin"; the
  land-only closure appendix is retired and replaced by Appendix B, a solved equilibrium
  with a strictly increasing schedule and explicit household participation; Appendix C
  is new (factor-income accounting and the conditional CES expenditure result). The
  abstract follows her Europe version. The flat case survives as one short remark. No
  equation of the empirical sections and no data series changed.
- The eras figure (Figure 2) was regenerated here from the revised
  `code/fig_eras_workers.py`: the logistic is gone from the computing and AI schedules,
  which are now smooth convex power curves rising to their walls, and the interior
  markers sit at their new intersections. The other five figures are the repository's
  own script-built originals, unchanged. The bundle also shipped those five, but as
  96-dpi re-encodings extracted from a PDF — two of them at different pixel dimensions —
  so they were not adopted.
- `checks/check_interior.py` is the bundle's check script, run here from the repository:
  it reproduces the bundle's `check-results.json` value for value. SciPy was added to
  the venv for it.
- Every battery is green after the port: `check_pinning` (51), `check_fan`,
  `check_interior`, `lint_tex_structure` (61 labels, no dangling references, six figures
  resolve), the eleven corner checks, effort reproduction (5) and consolidation (5), and
  `lake build` (8,709 jobs, both modules).
- `paper/submission/` was rebuilt from the new source: the blind manuscript carries 1,188
  Word equations, six figures, two tables, every cross-reference resolved, and no author
  name, affiliation, email or repository address in either the text or the file
  properties; the separate title page carries the author details.
  `paper/submission/abstract.txt` is the bundle's plain-text abstract for submission
  forms.

## Open — her calls

1. **The paper no longer mentions the Lean formalization or the sympy batteries.**
   The revision replaced the back-matter verification note with one paragraph about
   `check_interior.py`. The note it replaced named the Lean 4 scope (the full-automation
   chain, the lambda > 0 closure and its statics, the user-cost closures, the fraud and
   superstar lemmas, the CES share limits) and said the check files ship with the
   repository. Those files still build green, and several of the objects they prove are
   still in the paper. The register should state what is: restore a scoped sentence, or
   decide the paper stands without one. If restored, the CES share limits now live in
   Appendix C, not the retired land-only appendix.
2. **Figure 5's file in Overleaf**, and now the whole Overleaf project. The repository's
   `main.tex` and all six figures should replace her Overleaf copy wholesale — the source
   has moved further than a file swap. Figure 5 in particular
   (`fig_consumption_financing_and_human_effort.png`) is the adopted full-band D-F/Q
   artwork built by `effort/code/build_fullband_df_figures.py`, which her Overleaf upload
   never matched.
3. The title footnote says "see the AI-use note at the end"; the note sits before the
   references.
4. The data note cites HUD FY2025 fair-market rents "for the ceiling grid", but no
   ceiling-grid number appears in the paper. The grid ships (`data/kappa_ceiling.csv`,
   `docs/kappa_ceiling_notes.md`): quote it, or drop the clause.
5. Slips. The revision cleared four of the carried ones (the ''terminal'' quote, "The
   extreme cases makes", and the lowercase openings at "someone else's housing. in the
   modern economy" and "for the ceiling grid. financing splits"). Three survive,
   untouched: the Bullshit Jobs and gig economy quotes close with two backticks instead
   of two apostrophes; "nothing of anything. so its" is lowercase after a period; and the
   closing paragraph writes "at cost" with an italic command inside the sentence.
6. Figure 3 still carries its in-figure explanatory note (dashed pre-1964, the energy
   backcast); it duplicates the caption. Figure 2 now carries one line of its own above
   the panels, "Dots: illustrative wage ratios $w/c$", which its caption also states.
   Remove either on her word; the convention since 2026-09-04 has been that the captions
   carry the words.
7. The 22 archived 1958–1979 DF10 capacity uppers (up to 3.28pp tighter than the
   archive's own DF9 implies): adopt the rebuilt values or keep the frozen ones. The
   figures still draw the frozen DF21.
8. `checks/corner/check_closure.py` now backs nothing in the paper: the land-only closure
   appendix it mirrors is retired. It still passes. Keep it as the long draft's record,
   or retire it with the appendix.
9. The Word files follow no journal template (Times New Roman 12 pt, one-and-a-half
   spacing, A4, 2.5 cm margins; figure captions in Word's italic caption style; proofs
   end with ∎). Once the journal's requirements are known, adjust `reference_docx` in
   `code/build_submission_docx.py` and rebuild. The blind file keeps the AI-use note,
   which names no author.

## Note on the batteries

`check_pinning`, `check_fan` and `checks/corner/` were written against the propositions
as they stood before the interior revision. They still pass, and the algebra they check
is still the paper's, but their mapping to section and appendix numbers moved: the
README's corner table now carries the new pointers. `check_interior.py` is what backs
Section 6 and Appendix B.

## Route

Her TeX arrives as a Downloads file and is committed verbatim as `paper/main.tex`
(git is the freeze), then edited exactly once with a word diff for her read. Figures
regenerate only from their scripts — a rendered PNG that arrives alongside a script is
not adopted in place of running it. Nothing enters the text without its check.
