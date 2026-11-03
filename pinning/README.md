# Pinning the Wage to Scarcity and Technology

Johan Båge (Stockholm School of Economics) and Stella Wilson (KTH Royal Institute of
Technology and SEB). Working paper, 2026.

This folder is the paper's public record: the source, the six figures, the code and
data behind every reported number, the check files the paper's data note refers to,
and the Lean 4 formalization.

## Layout

```
paper/main.tex      the paper (pdfLaTeX; an Overleaf project is this file plus figures/)
paper/figures/      the eight script-built figures, one script each, as PDF (what main.tex
                    includes) and PNG (table below); figures/ssrn/ holds the eight images
                    extracted from the SSRN PDF, which main.tex no longer uses
paper/ssrn-7226858.pdf  the version posted to SSRN on 2026-09-23; main.tex was rebuilt from
                    this PDF on 2026-11-02 and revised since for Economic Modelling (STATE.md, Log)
paper/submission/   the journal's Word files: the blind manuscript and the separate title
                    page, built by code/build_submission_docx.py (section below), plus
                    abstract.txt, the plain-text abstract for submission forms
code/               figure scripts and the FRED-based measurement scripts
data/               built results and vendored inputs
cache/              the FRED pulls the measurement scripts read (August 2026 vintage;
                    A2013C1A027NBEA, ASLCTAX and W054RC1A027NBEA first cached 2026-09-04
                    and reproducing the tracked results exactly); delete a file to
                    re-pull that series live
checks/             sympy and numerical checks; checks/corner/ is the lambda = 0 corner
                    spine inherited from the long draft (its own numbering; map below)
lean/               Lean 4 statements and proofs (mathlib v4.33.0); see lean/README.md
effort/             Appendix E: the reproduction archive of the financing and production
                    accounts (archive_v28/, verbatim, read-only) and the repo-side pipeline
docs/               the coverage-ratio measurement spec, the ceiling-grid note, and the
                    handoff note for the 2026-09-21 interior revision
```

## Figures

Numbered as in the paper (the SSRN version). Files are in `paper/figures/`; each script
writes its figure twice, as `.pdf` (vector, TrueType fonts embedded; what `main.tex`
includes) and as `.png` (300 dpi). Each script draws its figure at the width `main.tex`
prints it (0.88 of the 16 cm text width, 0.92 for Figure 7), so its text prints at
7.5–8.5 pt; a change to an `\includegraphics` width needs the matching `PRINT_W` in
the script.

| Figure | File | Script | Inputs |
|---|---|---|---|
| 1 The task-assignment schedule | `fig_schedule.pdf`, `.png` | `code/fig_schedule.py` | none (schematic) |
| 2 The replacement closure | `fig_replacement_closure.pdf`, `.png` | `code/fig_replacement_closure.py` | none (equation (5) with full-chain b_m = 1 and lambda_m = 0.3 and 0) |
| 3 Labor-market clearing | `fig_labor_market_clearing.pdf`, `.png` | `code/fig_labor_market_clearing.py` | none (Appendix B's illustrative instance, solved by `code/appendix_b.py`) |
| 4 Four configurations of the schedule | `fig_eras_workers.pdf`, `.png` | `code/fig_eras_workers.py` | none (schematic) |
| 5 The deflator fork | `fig_deflator_fork.pdf`, `.png` | `effort/code/build_fig3_realwage_fan.py` | `effort/data/raw/` (FRED: AHETPI, AHEMAN, CUSR0000SAD, CUUR0000SAD, CUSR0000SAH1, CUUR0000SEHA, CPIUFDNS, CPIENGNS); gated against `effort/data/fig3_realwage_fork_1950.csv` |
| 6 The coverage ratio | `fig_kappa_measurement.pdf`, `.png` | `code/fig_kappa_measurement.py` | `data/kappa_results.csv` (built by `code/feasibility_kappa.py`) |
| 7 Two labor linkages | `fig_consumption_financing_and_human_effort.pdf`, `.png` | `effort/code/build_fullband_df_figures.py` | `effort/archive_v28/expected/` (DF21, LR_Q1) |
| 8 Composition of consumption financing | `fig_fourway.pdf`, `.png` | `code/fig_fourway.py` | `data/four_way_split.csv` (built by `code/four_way.py`) |

The figures carry no in-image titles and no in-image notes; the captions carry the
words. Figure 5's two-line key was the last note, removed 2026-11-02 once the caption
marked the dashed pre-1964 stretch.

## Numbers in the text

| Reported | Source in this folder |
|---|---|
| Fork 4.8x; durables +277%, food +13%, shelter −21% over 1964–2024 | `effort/data/fig3_realwage_fan.csv`; anchored by `checks/check_fan.py` |
| Coverage ratio 0.30 [0.15–0.59] in 2025, about 0.05 in the 1950s | `data/kappa_results.csv` (`code/feasibility_kappa.py`; method in `docs/feasibility_empirics_spec.md`) |
| Labor-origin financing 69.6% (2004), 65.8% (2023), 64.2% (2025 extension); production content 50.1/47.2 (1997/2023), 66.4/46.2 (1950/2025 extension) | `effort/archive_v28/expected/DF19_…`, `DF21_…`, `LR_Q1_…`; verified by `effort/checks/check_effort_reproduction.py` |
| Share of tax revenue from labor-income bases 0.68 (2025), 0.64 (1965) | `data/lambda_results.csv`, column `lamR_med` (`code/lambda_compute2.py`) |
| Conditioned share of benefits at least 0.84; about 0.99 by withdrawal rule | `data/lambdaB_results.csv` (`lamB_floor`, `lamB_rule`), computed for the long draft in August 2026; the script that produced it predates this repository's first commit and is not included |
| Borrowing financed 19% of transfers in 2025, zero only in 1998–2000 | `data/four_way_split.csv` (`code/four_way.py`) |
| The HUD FY2025 fair-market-rent ceiling grid | `data/kappa_ceiling.csv` (`code/kappa_ceiling.py`, `data/hud_fy25_fmrs.xlsx`); `docs/kappa_ceiling_notes.md` |
| Appendix B's illustrative instance (durable machines; parameters set from U.S.-like shares: labor 0.456 of a machine's build cost and 0.469 of consumption, machine services 0.196, site 0.065 of the basket, participation 0.602; x* 0.82987 below the ceiling 0.94634, Y 3.01320, support 0.02599 of rent and interest 0.03520) and its automation path (participation 0.56 at eta 1, 0.13 at 0.01); Figure 3's equilibria, w/P_s and N_a/N 2.76/0.60 at baseline, 2.46/0.56 recursive, 2.66/0.59 task automation | `code/appendix_b.py` (`PRINTED`; how it was set is in its comments and STATE.md, Log 2026-11-03); every quoted number recomputed and matched to the text by `checks/check_interior.py` (group Q) |

## Submission files

**Economic Modelling (2026-11-03).** `code/build_submission_em.py` builds `paper/submission/em/`
for the special issue "Artificial Intelligence, Data Investment and the Digital Economy"
(double-anonymized review): `manuscript.tex`, the anonymized LaTeX source (no authors,
affiliations, emails, title footnotes, date, or preamble comments), with the figures beside
it as `Figure_1.pdf` … `Figure_7.pdf` and `Figure_D1.pdf`; `title_page.docx`,
`highlights.docx` and `cover_letter.docx`, from the editable sources in
`paper/submission/em_src/`; and `manuscript_preview.pdf`, compiled from the anonymized source
for checking (not an upload). The build stops before writing if an author's name, email,
affiliation, or the repository or SSRN address survives in the source or the compiled text
and metadata, if a figure is missing, or if the abstract (250 words), keywords (1–7) or
highlights (3–5, 85 characters) break the journal's limits. It needs `latexmk` and `pandoc`
on the path. `paper/submission/em_src/submission_notes.md` lists what to upload and what to
enter in Editorial Manager.

**STRECO (2026-09-04).** `code/build_submission_docx.py` builds `paper/submission/manuscript_blind.docx`, the full
paper with an anonymized title page (no authors, affiliations, emails, or disclaimer
footnote; the repository address withheld for review; no author in the file properties),
and `paper/submission/title_page.docx`, the separate title page with the author details.
Every equation is a Word equation, the six figures are embedded, cross-references carry
the numbers LaTeX prints, and theorem environments are written out with their numbers.
Styling is Times New Roman 12 pt, one-and-a-half spacing, A4 with 2.5 cm margins; adjust
`reference_docx` in the script for a journal template. The build needs the
`pypandoc_binary` package in the venv (it bundles pandoc); rebuild after any change to
`paper/main.tex`:

```
../venv/Scripts/python.exe code/build_submission_docx.py
../venv/Scripts/python.exe code/build_submission_em.py      # the Economic Modelling files
```

## Reproduce

From this folder, with the repository's virtual environment:

```
../venv/Scripts/python.exe code/fig_schedule.py             # Figure 1
../venv/Scripts/python.exe code/fig_replacement_closure.py  # Figure 2
../venv/Scripts/python.exe code/appendix_b.py               # prints Appendix B's and Figure 3's numbers
../venv/Scripts/python.exe code/fig_labor_market_clearing.py  # Figure 3
../venv/Scripts/python.exe code/fig_eras_workers.py         # Figure 4
../venv/Scripts/python.exe code/lambda_compute2.py        # FRED (cache/); writes data/lambda_results.csv
../venv/Scripts/python.exe code/four_way.py               # writes data/four_way_split.csv
../venv/Scripts/python.exe code/fig_fourway.py            # Figure 8
../venv/Scripts/python.exe code/feasibility_kappa.py      # writes data/kappa_results.csv
../venv/Scripts/python.exe code/fig_kappa_measurement.py  # Figure 6
../venv/Scripts/python.exe code/kappa_ceiling.py          # needs python-calamine; writes data/kappa_ceiling.csv
../venv/Scripts/python.exe effort/code/build_fig3_realwage_fork.py       # Figure 5 chain, step 1 (1964 base)
../venv/Scripts/python.exe effort/code/build_fig3_realwage_fork_1950.py  # step 2 (1950 extension, the gate reference)
../venv/Scripts/python.exe effort/code/build_fig3_realwage_fan.py        # step 3: paper/figures/fig_deflator_fork.pdf and .png
../venv/Scripts/python.exe effort/code/build_fullband_df_figures.py      # Figure 7: paper/figures/fig_consumption_financing_and_human_effort.pdf and .png
```

Each figure script writes both the `.pdf` and the `.png` of its figure.

The measurement scripts read `cache/` and pull from FRED only for series not cached;
`--refresh` on the Figure 5 scripts re-pulls their raw series. Every FRED series is
validated by identity checks and magnitude anchors before use; every contestable
classification runs as a labeled grid, and the reported object is the median with its
min–max band. The scripts stop rather than substitute when a source cannot be validated.

The venv needs NumPy, Matplotlib, SymPy and SciPy (`code/appendix_b.py`, `checks/check_cost_system.py`,
`checks/check_interior.py`), plus
`python-calamine` for the ceiling grid and `pypandoc_binary` for the Word build.

## Checks

```
../venv/Scripts/python.exe checks/check_pinning.py               # 51 checks: the recursion, the replacement closure, statics, the fork, the welfare pair, the priced exit
../venv/Scripts/python.exe checks/check_fan.py                   # the composite pricing display, the flat-case parity, the fork's data anchors
../venv/Scripts/python.exe checks/check_cost_system.py           # network prices against truncated production rounds, factor-income cancellation, Section 6's feasible-method bounds, participation from utility; random networks and Appendix B's economies
../venv/Scripts/python.exe checks/check_interior.py              # Appendix B (about 90 s): Lemma B.1 with durable machines on the printed instance, Figure 3's economies and two durable test economies — the equilibrium conditions, income with interest, a 2,048-cell linear production program that finds the equilibrium itself, the flow special case, the automation path, every quoted number against main.tex
../venv/Scripts/python.exe checks/lint_tex_structure.py paper/main.tex
for f in checks/corner/*.py; do ../venv/Scripts/python.exe "$f"; done
../venv/Scripts/python.exe effort/checks/check_effort_reproduction.py   # rebuilds archive_v28 in a temp dir and compares to the frozen outputs
../venv/Scripts/python.exe effort/checks/check_df910_consolidation.py   # the consolidated long-run financing ledgers against the archive
cd lean && lake exe cache get && lake build
```

`checks/corner/` keeps the long draft's proposition numbering. What each file backs in
the paper:

| File | Long-draft object | In the paper |
|---|---|---|
| `check_baseline_props.py` | the task margin, the recursion, the flat limit | Propositions 1 and 2 at lambda = 0; the flat-case remark in Section 6 |
| `check_closure.py` | the land-only closure | nothing: the interior revision of 2026-09-21 retired that appendix |
| `check_conditionality.py` | conditionality | Appendix D.1 |
| `check_feasibility.py` | the coverage ratio | Appendix D.3 |
| `check_enclosure.py` | the priced commons | Proposition 3 and Appendix D.4 |
| `check_mix.py` | the mix frontier | Appendix D.5 |
| `check_kset.py` | the Baumol fork, the fraud bound, superstars | Appendix E |
| `check_open.py` | the open economy | the trade remark in Section 2 |
| `check_welfare.py` | the welfare pair | Proposition 6 |
| `check_fortification.py` | wedge targeting and punctuated adoption | the stabilizers section |
| `check_repairs.py` | existence and uniqueness; depreciation in the recursion | Appendix A's durability paragraph; the existence half is no longer a paper object, the interior revision having replaced the old Lemma A.1 with Appendix B's worked equilibrium (`check_interior.py`) |

`lean/` states and proves the full-automation chain, the lambda > 0 closure and its
comparative statics, the user-cost closures, the fraud and superstar lemmas, and the CES
share limits; its README lists the exact scope, the assumption manifest, and what is
deliberately left out. The interior category-price results that Section 6 and Appendix B
now carry are outside that scope; `checks/check_cost_system.py` and `checks/check_interior.py`
are what back them.
