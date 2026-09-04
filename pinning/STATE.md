# STATE — pinning (the paper; resume point for the next session)

**Project:** *Pinning the Wage to Scarcity and Technology* (Johan Båge and Stella
Wilson), being prepared for submission.
**Collaboration:** her TeX is the working file. Claude ports edits exactly once, produces
word diffs (`../tools/word_diff_report.py`) and reading views
(`../tools/reading_view.py`), never re-voices, and flags slips for her one-word
decisions. Checks gate absolutely (`README.md` lists them).
**State as of:** 2026-09-04 — the repository was restructured for submission; this
folder is new. Its history is `../dynamics/STATE.md` logs 1–52 (the revision thread,
under its old name the-link-revision) and the former `effort-accounting/STATE.md`, both
at tag `pre-cleanup-2026-09-04`.

## Where things stand

- `paper/main.tex` is her `Downloads/v5 (3).tex` of 2026-09-04 (103,806 bytes)
  verbatim plus one edit: the AI-use note now names the repository ("the code and data
  are public at" the GitHub URL, `wilsoniumite/labor`). Relative to her v5 (2): the
  date line is gone; two closing paragraphs were added to the conclusion (the
  grand-distortion reading; the synthesis of classical thought); a Future Work section
  is new; the AI-use note moved ahead of the references, and the data and verification
  notes were merged into one note after them.
- The six figures were regenerated on 2026-09-04 without in-figure titles (her ask).
  Figures 1 and C.1 are byte-identical to before (they had none); Figures 3, 4 and 5
  lost their titles; Figure 2 lost its two bold panel headers (the caption's "top" and
  "bottom" identify the panels).
- Every battery is green from the new paths: `check_pinning` (51), `check_fan`,
  `lint_tex_structure` (six figures resolve), the eleven corner checks, effort
  reproduction (5) and consolidation (5), and `lake build` (8,709 jobs, both modules).

- 2026-09-04, later: the journal's Word files exist. `paper/submission/manuscript_blind.docx`
  is the full paper with an anonymized title page (no authors, affiliations, emails, or
  disclaimer footnote; the repository address withheld; no author in the file properties),
  and `paper/submission/title_page.docx` is the separate title page with the author
  details. Both are built by `code/build_submission_docx.py` from `paper/main.tex` and
  checked: every equation pandoc parses is a Word equation, six figures, two tables, all
  cross-references resolved, no author name or address in the text, and the text equals
  the source word for word outside equation rendering. Rebuild after any change to
  main.tex.

## Open — her calls

1. **Figure 5's file in Overleaf.** The paper references
   `fig_consumption_financing_and_human_effort.png`, which until today existed only as
   her Overleaf upload. The repository's version is the adopted full-band D-F/Q artwork
   built from the archive by `effort/code/build_fullband_df_figures.py`, now title-free.
   Replace the Overleaf file with the repository's so the two agree; the other five
   figures should be re-uploaded too (titles gone).
2. The title footnote says "see the AI-use note at the end"; the note now sits before
   the references.
3. The data note cites HUD FY2025 fair-market rents "for the ceiling grid", but no
   ceiling-grid number appears in the paper. The grid ships (`data/kappa_ceiling.csv`,
   `docs/kappa_ceiling_notes.md`): quote it, or drop the clause.
4. Slips carried from the 2026-09-03 read, untouched: the ''terminal'' quote in the
   introduction opens with two apostrophes; "The extreme cases makes"; lowercase after a
   period at "nothing of anything. so its", "someone else's housing. in the modern
   economy", and "for the ceiling grid. financing splits". New in v5 (3): the Bullshit
   Jobs and gig economy quotes close with two backticks instead of two apostrophes, and
   the closing paragraph writes "at cost" with an italic command inside the sentence.
5. Figure 3 still carries its in-figure explanatory note (dashed pre-1964, the energy
   backcast); it duplicates the caption. Remove on her word.
6. The 22 archived 1958–1979 DF10 capacity uppers (up to 3.28pp tighter than the
   archive's own DF9 implies): adopt the rebuilt values or keep the frozen ones. The
   figures still draw the frozen DF21.
7. The URL in the paper points at the GitHub remote. The cleanup is committed locally
   only; push before submission, and update the URL if the repository is renamed.
8. The Word files follow no journal template (Times New Roman 12 pt, one-and-a-half
   spacing, A4, 2.5 cm margins; figure captions in Word's italic caption style; proofs
   end with ∎). Once the journal's requirements are known, adjust `reference_docx` in
   `code/build_submission_docx.py` and rebuild. The blind file keeps the AI-use note,
   which names no author.

## Route

Her TeX arrives as a Downloads file and is committed verbatim as `paper/main.tex`
(git is the freeze), then edited exactly once with a word diff for her read. Figures
regenerate only from their scripts. Nothing enters the text without its check.
