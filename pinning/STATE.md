# STATE — pinning (the paper; resume point for the next session)

**Project:** *Pinning the Wage to Scarcity and Technology* (Johan Båge and Stella
Wilson), being prepared for submission.
**Collaboration:** her TeX is the working file. Claude ports edits exactly once, produces
word diffs (`../tools/word_diff_report.py`) and reading views
(`../tools/reading_view.py`), never re-voices, and flags slips for her one-word
decisions. Checks gate absolutely (`README.md` lists them).
**State as of:** 2026-11-03 — `paper/main.tex` is the version posted to SSRN on 2026-09-23,
rebuilt from its PDF (`paper/ssrn-7226858.pdf`) because her Overleaf source was unavailable
(Log, 2026-11-02; branch `ssrn-rebuild`), with polish 1–3 and, since 2026-11-03, Appendix B's
Lemma B.1 for durable machines with the SSRN instance as its flow case (Log). Calibration (c)
was ported, reviewed and not adopted (Log, 2026-11-03). The Economic Modelling package is built
(`paper/submission/em/`; `main` fast-forwarded to it and tagged `em-package-2026-11-03`); she
submits after Johan's sign-off (Open 11d) and revises the SSRN posting herself. Next: the polish pass for the next submission, the
Economic Modelling special issue "Artificial Intelligence, Data Investment and the Digital
Economy" (deadline 2027-02-28). STRECO desk-rejected the 4 September Word build on
2026-11-02, without comments. Before that, 2026-09-24: the SSRN PDF staged; 2026-09-21: the
interior revision landed. The folder dates from the
2026-09-04 restructure; its history is `../dynamics/STATE.md` logs 1–52 (the revision
thread, under its old name the-link-revision) and the former `effort-accounting/STATE.md`,
both at tag `pre-cleanup-2026-09-04`.

## Where things stand

- **2026-11-02:** `paper/main.tex` is the SSRN version, rebuilt from its PDF (Log). The
  bullets below describe the interior revision of 2026-09-21 that it replaced; the Word build
  still describes that revision until the polish pass rebuilds it. Since 2026-11-03 the
  batteries describe the SSRN version: `checks/check_interior.py` (110) backs Appendix B and
  Figure 3, `checks/check_cost_system.py` (22) the cost system the data note names.
- `paper/main.tex` was the interior revision of 2026-09-21, ported verbatim from her
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

0. → Source resolved 2026-11-02: rebuilt from the PDF (Log), since the Overleaf copy was not
   at the SSRN state and the original TeX was on a machine she could not reach. If the
   original turns up, diff it against the rebuild. → 2026-11-03: the rest of this item is done —
   both new figures have scripts (Figure 2 in polish 3, Figure 3 now), and `check_cost_system.py`
   and the rebuilt `check_interior.py` are the scripts the data note names (Log). Only the diff
   against the original TeX, if it turns up, remains.
   **The SSRN version's source** (her go to bring it in, 2026-09-24). The posted PDF
   (SSRN 7226858, compiled 2026-09-23 on Overleaf's TeX Live) is a revision beyond
   anything on disk: `main.tex` is `v5_interior.tex`; her Overleaf edit of the same evening
   (`Downloads/v5 (4).tex`, 17:50 — "Existing characterizations of the wage", "our model")
   came next; the SSRN restructures further. What the PDF shows, for the port's word diff:
   Section 3 becomes "The model: task assignment and the cost system" with 3.2 "The cost
   recursion"; Section 5 "Replacement meets participation"; 6.1 "What an hour's wage buys";
   2.7 "Empirical measures"; Section 11 "Artificial intelligence and conclusion"; Appendix A
   in four parts (A.4 "Timing and institutional rents"); Appendix D holds the fiscal
   transition. **Eight figures**: two new — Figure 2, the replacement closure (curves at fixed
   full-chain labour in a machine-hour) and Figure 3, labour-market clearing in the Appendix B
   economy — and the six here renumbered (the eras figure becomes 4, the composition of
   consumption financing 8). **Appendix B's numerical instance changed** (same parameters):
   x* ≃ 0.86315, v ≃ 0.54344, Y ≃ 7.88061, N_a ≃ 1.34338, against main.tex's 0.96791, 0.59841,
   18.47540, 1.34285 — so `checks/check_interior.py` as it stands checks the superseded
   instance. `../paths/checks/check_macro.py` (P1) already reproduces the SSRN's published
   figures to five decimals from its own solver. **The data note names a new script**,
   `check_cost_system.py` (network prices against truncated production rounds, factor-income
   cancellation, feasible-method bounds, participation from utility), and a revised
   `check_interior.py` (a linear production program with 2,048 task cells); neither is here.
   The AI-use note again ends "the code and data are public" without the address — the
   standing edit re-applies at the port. Still no Lean or sympy sentence (item 1).
   **Needed from her:** Overleaf → Menu → Download → Source (the zip: `main.tex` and the
   figures), and the bundle the two check scripts came in, if they came from the ChatGPT
   side. The two new figures then get scripts here (the Route: no PNG is adopted in place of
   a script); the labour-market-clearing figure can be built on the Appendix B solver that
   `../paths/` already gates.

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
10. → Resolved 2026-11-02 (her yes, polish 2): the numerator is now households' own real estate
    (HOOREVLMHMV); 2025 median 0.30 [0.15–0.59], as estimated below. Log.
    **The coverage figure's Z.1 land residual mixes sectors** (found in the paths
    thread's feasibility study; levels verified on FRED 2026-09-30).
    `code/feasibility_kappa.py` takes households-and-nonprofits real estate (HNOREMV,
    $54.07T in 2026Q2) less households' residential structures alone (BOGZ1LM155012665Q,
    $29.70T), so about $4.3T of nonprofit property counts as land: the residual is
    $24.4T, where the matched numerator, households' own real estate (HOOREVLMHMV,
    $49.79T), gives $20.1T, about 18% lower. Of the 2025 members only the four household
    valuation members (`k_z1_hh_*`) are built on this residual, and they are overstated by
    about a fifth; the rent-bill members (`k_flow_*`) are unaffected, and the economy-wide
    valuation members (which include it too) are empty in 2025. So in Figure 4 the
    README's 2025 median 0.33 [0.18–0.59] would fall to roughly 0.30, the band's low end
    to about 0.15 and its top (a rent-bill member) not at all — an estimate, scaling
    those members by the 2026Q2 ratio (20.1/24.4), not rerun. The same pairing sits in
    `progress_and_prosperity/data_notes/terminal_rent/build_measurement.py:134`
    (untracked; not in the public repository), as recorded in that thread's STATE.
    Her call for the paper: switch the numerator and rebuild `data/kappa_results.csv`
    and the figure, or keep it and say so.
    → Decided 2026-10-01 (Claude, on her delegation; paths STATE decision 52): it stays
    open for the paper's authors, and the repository's figures keep matching the
    published paper, which a rebuild here would contradict.

11. **The Economic Modelling package (2026-11-03): her calls before submitting.** → Settled the same
   day but for (d): (a) yes, every caption ends "Drawn by code written with Claude (Anthropic)."
   ("Drawn" for "Plotted": Figures 1 and 4 are diagrams); (b) her "up to you": the title page
   declares her SEB employment (SEB had no role), as the declarations tool should; (c) none, the
   section is dropped from the title page; (e) "looks good"; (f) her "agreed": the new instance (Log).
   Open: (d) Johan's sign-off before submitting, since authorship is fixed at submission.

## Note on the batteries

`check_pinning`, `check_fan` and `checks/corner/` were written against the propositions
as they stood before the interior revision. They still pass, and the algebra they check
is still the paper's, but their mapping to section and appendix numbers moved: the
README's corner table now carries the new pointers. `check_cost_system.py` and
`check_interior.py` are what back Section 6 and Appendix B.

## Log

- **2026-11-03 — the repository brought up to the package.** Her go ("go ahead with the repo"; she
  revises SSRN herself). The paper's date reads November 2026 (was September 23, 2026; the anonymized
  build drops the date, so the package is unchanged); the checklist's data statement says the
  repository is public and only its link is left out during review; the README no longer calls
  main.tex the SSRN version's source. `main` fast-forwarded to `ssrn-rebuild` (no commits of its own
  since 43e32b3) and the package commit tagged `em-package-2026-11-03`. For SSRN she has the full
  version with the authors (main.tex compiled), not the anonymized one.

- **2026-11-03 — Appendix B's instance set from U.S.-like shares; the AI line in every caption.**
  Her "agreed" (Open 11f), on two conditions she accepted: the parameters come from shares, not from
  the figure, and the text says so in a clause. The SSRN instance could not carry the ranking: land
  0.73 of its basket, labor 0.04 of a machine's cost, and raising lambda breaks the equilibrium near
  0.25. Set N 1, b 0.4, delta 0.05, gamma(0) 0.01; seven parameters solve labor 0.47 of a machine's
  build cost, machine services 0.20 of it, labor 0.47 of consumption on the full chain, site 0.06 of
  the basket (the measured order), the chain 0.15 of hours, participation 0.60 and 3 baskets a person,
  the return an outcome as in (c) (0.093); of the two roots in k the lower (4.36), as (c)'s main
  reading (the other, 15.5, has task automation raise w/P_s by 9% on the same shares, told to her);
  then two significant figures: T 0.01, h 0.0017, a 1.4, lambda 7.3, k 4.4, chi_max 2.2, rho 0.09.
  Figure 3: w/P_s 2.76 -> 2.46 under recursive automation (-11%) and 2.66 under task automation
  (-3%); participation 0.60 -> 0.56 and 0.59; Section 5's "both channels lower the real wage and
  participation" holds. Appendix B prints the instance with the clause ("These values are
  illustrative. They are chosen so that cost shares are of the order seen in U.S. data: ..."), its
  solution (x* 0.82987 below the ceiling 0.94634) and support (0.02599 of rent and interest 0.03520).
  The automation path now scales the instance's own schedule (the SSRN path, gamma = eta(1 + x),
  leaves support unfunded at high eta here), starts at Figure 3's recursive-automation economy, and
  keeps a hundred-to-one capability ratio, so Section 6.1 says "hundred-to-one". Figure 3 redrawn
  (legend in the band above the curves, frame to 7). The SSRN instance stays in the code as the flow
  test case (`appendix_b.SSRN_INSTANCE`; F1 still reproduces its printed numbers). Every figure
  caption ends "Drawn by code written with Claude (Anthropic)." (Open 11a). Title page: the SEB
  employment declared, no acknowledgments section. `check_interior.py` 112 (the shares the paragraph
  states, the AI line in all eight captions, the path on the new schedule); every battery green;
  41 pages.

- **2026-11-03 — the Economic Modelling package.** Her go; the journal's Guide for Authors (her
  attachment) and the special-issue call. **main.tex** (word diff against the Appendix B commit): the
  AI-use note becomes Elsevier's section "Declaration of generative AI and AI-assisted technologies in
  the manuscript preparation process", before the references, in the guide's template, naming Claude
  (Anthropic) and ChatGPT (OpenAI) without versions (her call), and the title footnote points to it;
  the data note moves before the references and drops the HUD FY2025 ceiling-grid clause (her call:
  the paper shows no ceiling grid); keywords and JEL codes under the abstract (drafts); appendix
  equations, figures and tables numbered by appendix as the guide asks ((A.1)–(D.2); Figure 8 is
  Figure D.1); the two tables become captioned floats, Tables A.1 and D.1, cited in the text (captions
  are drafts). **References** audited against Crossref and publishers' records (a subagent; every DOI
  then re-resolved here): 22 entries completed (pages for 20, Rognlie's subtitle and issue, the NBER
  volume's "An Agenda", Romer's "Part 2"), 45 DOIs added in Elsevier's form; no wrong author, year or
  source. Unverifiable (JSTOR blocks automated access), left as printed: Baumol 1967's volume, issue and
  pages; Leontief 1936's last page; Gruber 1997's issue label (Crossref says S3). 41 pages (40).
  **New:** `code/build_submission_em.py` (the anonymized LaTeX source with the figures as
  Figure_1–Figure_7 and Figure_D1, the title page, highlights and cover letter; it stops on any
  identifying string in the source, the compiled text or its metadata, and on the journal's limits),
  its sources in `paper/submission/em_src/` with `submission_notes.md` (what to upload and enter;
  the USD 125 fee), and its outputs in `paper/submission/em/`. Open 11 lists her remaining calls.
  Every battery green.

- **2026-11-03 — Appendix B: Lemma B.1 for durable machines; the SSRN instance as its flow case;
  Figure 3 and the checks from scripts.** Her call ("2"), the second of three options put to her
  after an independent review of the calibration port. **Calibration (c) not adopted.** It was
  ported into Appendix B and Figure 3 and reviewed; the maths and every quoted number held, two
  targets did not: the site at 13% of the basket applies a subsistence basket's shelter share
  (a third) to all consumption, where housing is 15.7% of 2023 PCE (DHSGRC1A027NBEA/PCECA), so
  model site rent is 0.11 of GDP against 0.03–0.05; and 3 baskets a person is assumed, where the
  paper's own single-person bundle (`code/feasibility_kappa.py`) puts 2023 PCE at 4.59 per person
  16+ (9.04 with the family-of-four bundle), with no root at g0 0.01 (it needs g0 ≤ 0.0085). With
  the site, output and employment (EMRATIO 60.3) at measured values (g0 0.008): recursive
  automation still lowers w/P_s and N_a/N on both roots; task automation lowers w/P_s slightly
  on the low root (4.21 → 4.12) and raises it on the high (→ 4.51); rho 0.095, above the NIPA
  band; and rho's place in the band had chosen (c)'s basis (`../paths/` decision 31). The port's
  files are not committed (its `check_interior.py` let swapped table rows pass, and its program
  took the solver's N_a, X and charge as inputs). **Kept from the port**, its maths verified by
  the reviewer: Lemma B.1 and its proof with machines at Appendix A.4's user cost (rho, delta,
  the ceiling x_c, (25) as T > Nh and n_S(x_c) > n_D(x_c), funding at x*: T + rho V_m X ≥ N P_s),
  (21)–(24) and the three-row system in general form; (21) now reads p_m, then v = gamma p_m, so
  its tag fits the line. **New text:** (4) on the replacement coefficients gives L_s and B_s, the
  basket's hours and land, and P_s = wL_s + rB_s + rho V_m X/Y, the two sets of coefficients
  coinciding in the flow benchmark (the reviewer's L_s/B_s clash); Section 5 and D.3 state
  P_s = wL_s + rB_s "in the flow benchmark". The instance, its numbers, the automation path,
  Figure 3's caption and Section 6.1's "two-to-one" are the SSRN version's, the instance now
  "in the flow benchmark, rho = 0 and delta = 1". Figure 3 from `code/fig_labor_market_clearing.py`
  (the SSRN curves on `code/appendix_b.py`; legend lower right, where at 8 pt it clears the
  participation curve; canvas aspect 1.70 for 1.894). **Checks:** `checks/check_interior.py`
  rebuilt (110; the 2026-09-21 battery is in git history): equilibrium conditions and income on
  the printed instance, Figure 3's two automation economies and two durable test economies (one
  with a binding ceiling); a 2,048-cell linear program that finds each equilibrium itself
  (participation from its dual wage; with durable machines the charge from the required return
  at its dual machine cost), within a priori discretization bounds; the flow special case; the
  path; every quoted number anchored to its words, no decimal unchecked, no calibration residue.
  Eight mutations (swapped or altered numbers in Appendix B, the caption and Section 6.1, D.3's
  qualifier, a wrong user cost in the solver) each fail it. `checks/check_cost_system.py` (22) is
  new. Also: the D.5 table's D, 0.29 → 0.31 (polish 2 changed the text and missed this cell).
  40 pages (39). Every battery green; word diff against polish 3: exactly these changes.

- **2026-11-02 — polish 3: the figures from their scripts.** Figures 1, 2 and 4-8 now come from
  their scripts as vector PDFs (PNG kept); only Figure 3 still points at `figures/ssrn/`
  (pending the calibration decision). Figure 1 and 4 labels read `w/p_m` as printed; no in-image
  titles or notes (Figure 4's "Dots:" line and Figure 5's note are gone; Open 6 moot); Figure 2
  has a script (`code/fig_replacement_closure.py`, from equation (5)); Figure 7 keeps the full-band
  version with plain legend names (her call); every figure is drawn at its printed width, so text
  prints at 7.5-8.5 pt (was 3.9-6.6), with Figures 6 and 7's legends below the axes. Text: Figure 5's
  caption marks the dashed pre-1964 segment; Figure 8's caption and the data note say 1960-2025
  (the series and the plot start in 1960; both said 1962). 39 pages, no figure moved page; gates,
  `check_fan` and the lint green. For the next Word build, map the PDFs to the PNGs
  (`build_submission_docx.py` passes figure files to pandoc).

- **2026-11-02 — polish 2: the coverage ratio's land residual matched (Open 10).** Her yes.
  `code/feasibility_kappa.py` takes households' own real estate (HOOREVLMHMV, first cached
  2026-11-02) in place of households-and-nonprofits' (HNOREMV), so the residual nets households'
  structures from households' real estate. 2025: 0.30 [0.15–0.59] (was 0.33 [0.18–0.59]); the
  1950s stay about 0.05; the top of the band is a rent-bill member and does not move. The figure
  gate in `code/fig_kappa_measurement.py` is re-anchored (kappa_med 0.298, stock_med 0.250;
  flow members unchanged at 0.326). Text: Section 9's estimate, the Figure 6 caption's series,
  "about 30 percent" (was "about one-third") in Section 10, Appendix D.5's D = 0.31 (was 0.29;
  0.64 x 0.70^2 = 0.314 on the printed inputs, 0.316 unrounded), and the summary table. Figure 6
  now points at the script-built file (no in-image title). Word diff: exactly these changes.

- **2026-11-02 — polish 1: the slips fixed.** Her yes to all. "both parameters" becomes
  "both" (2.3); "meters" twice; Proposition 2 gains its serial comma; "urbanization";
  "attributing ... require"; A.1's machine-type index is now `\ell` (k stays the non-produced
  input); the identity matrix is bold `\mathbf{I}` in its four uses, so Appendix C's `I` is
  expenditure only; "An $H$-free good's"; the Zeira entry closes inside the reference group
  (hanging indent restored) and gains its pages, 1091--1117. Word diff against the rebuild:
  exactly these changes. Her Figure 7 call, same day: the repo's full-band version, with
  plainer legend names than its D-F/D-Q labels (polish, figures).

- **2026-11-02 — the SSRN version rebuilt from its PDF.** Her go ("start the rebuild"); the
  Overleaf copy was not at the SSRN state and the original TeX sat on a machine she could not
  reach. Method: verbatim transcription of `paper/ssrn-7226858.pdf`, reusing the 21 September
  `main.tex` wherever text or math carried over; nothing re-voiced. Six parallel transcribers
  (front and Sections 1-2; 3-4; 5-7; 8-12; Appendices A-C; D-F, notes, references), then one
  assembly. Same preamble plus `array`, which the SSRN table on p. 34 needs.
  Verification: 39 pages, as in the SSRN PDF; the extracted text matches word for word in
  every section (the only diff is text-extraction order inside the underbraces of (11), whose
  page renders identically); at 100 dpi, 37 of 39 pages are pixel-identical, and pages 18 and 20
  differ by a sub-pixel offset of one caption line each; `lint_tex_structure` green
  (84 labels, 95 refs, 8 figures); no undefined or duplicate references.
  Labels follow the printed numbering (`sec:N`, `app:X`, `eq:N`, `prop:N`, `lem:B.1`, `fig:N`).
  Figures: `paper/figures/ssrn/` holds the eight images extracted from the SSRN PDF, which
  `main.tex` points at so it reproduces the posted version. They are placeholders: the polish
  pass points each figure back at a script-built file (the Route). Found on the way: the
  script-built `fig_schedule.png` and `fig_eras_workers.png` still label the ratio `w/c`
  where the SSRN prints `w/p_m`; Figures 5 and 6 in the SSRN carry in-image titles (the
  script builds do not); and the SSRN Figure 7 is a different plot from the adopted full-band
  `fig_consumption_financing_and_human_effort.png` (Open 2).
  Slips seen while transcribing, left as printed and marked `% SLIP:` in the source, for her
  one-word calls: Section 2.3 "This paper endogenizes both parameters" (no antecedent left
  for "parameters"); "metres" twice in the loom example (otherwise American spelling);
  Proposition 2 lacks a serial comma; "urbanisation" (otherwise -ization); "Identifying ...
  and attributing ... requires" (agreement); Appendix A.1 uses `k` for machine types, then for
  non-produced inputs; the Appendix C display uses `I` for expenditure and for the identity
  matrix; Proposition E.1 proof "A $H$-free good's"; the Zeira reference prints without its
  hanging indent.

- **2026-09-24 — the SSRN version staged.** Her go ("you can bring the ssrn version in").
  Only the PDF exists on disk (no newer TeX or bundle in Downloads, Desktop, Documents or
  OneDrive), so the PDF is committed as `paper/ssrn-7226858.pdf` (SHA-256 a4dc7e87…) and the
  differences it shows are recorded under Open 0; `main.tex` is untouched until her source
  arrives, because a TeX rebuilt from a PDF would be a re-voicing and would then overwrite
  her Overleaf copy.

## Route

Her TeX arrives as a Downloads file and is committed verbatim as `paper/main.tex`
(git is the freeze), then edited exactly once with a word diff for her read. Figures
regenerate only from their scripts — a rendered PNG that arrives alongside a script is
not adopted in place of running it. Nothing enters the text without its check.
