# Pinning the Wage to Scarcity and Technology

Johan Båge (Stockholm School of Economics) and Stella Wilson (KTH Royal Institute of
Technology and SEB). Working paper, 2026.

This folder is the paper's public record: the source, the six figures, the code and
data behind every reported number, the check files the paper's data note refers to,
and the Lean 4 formalization.

## Layout

```
paper/main.tex      the paper (pdfLaTeX; an Overleaf project is this file plus figures/)
paper/figures/      the six figures, one script each (table below)
paper/submission/   the journal's Word files: the blind manuscript and the separate title
                    page, built by code/build_submission_docx.py (section below)
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
docs/               the coverage-ratio measurement spec and the ceiling-grid note
```

## Figures

| Figure | File | Script | Inputs |
|---|---|---|---|
| 1 The task-assignment schedule | `fig_schedule.png` | `code/fig_schedule.py` | none (schematic) |
| 2 Four configurations of the schedule | `fig_eras_workers.png` | `code/fig_eras_workers.py` | none (schematic) |
| 3 The deflator fork | `fig_deflator_fork.png` | `effort/code/build_fig3_realwage_fan.py` | `effort/data/raw/` (FRED: AHETPI, AHEMAN, CUSR0000SAD, CUUR0000SAD, CUSR0000SAH1, CUUR0000SEHA, CPIUFDNS, CPIENGNS); gated against `effort/data/fig3_realwage_fork_1950.csv` |
| 4 The coverage ratio | `fig_kappa_measurement.png` | `code/fig_kappa_measurement.py` | `data/kappa_results.csv` (built by `code/feasibility_kappa.py`) |
| 5 Two labor linkages | `fig_consumption_financing_and_human_effort.png` | `effort/code/build_fullband_df_figures.py` | `effort/archive_v28/expected/` (DF21, LR_Q1) |
| C.1 Composition of consumption financing | `fig_fourway.png` | `code/fig_fourway.py` | `data/four_way_split.csv` (built by `code/four_way.py`) |

The figures carry no in-image titles; the captions do.

## Numbers in the text

| Reported | Source in this folder |
|---|---|
| Fork 4.8x; durables +277%, food +13%, shelter −21% over 1964–2024 | `effort/data/fig3_realwage_fan.csv`; anchored by `checks/check_fan.py` |
| Coverage ratio 0.33 [0.18–0.59] in 2025, about 0.05 in the 1950s | `data/kappa_results.csv` (`code/feasibility_kappa.py`; method in `docs/feasibility_empirics_spec.md`) |
| Labor-origin financing 69.6% (2004), 65.8% (2023), 64.2% (2025 extension); production content 50.1/47.2 (1997/2023), 66.4/46.2 (1950/2025 extension) | `effort/archive_v28/expected/DF19_…`, `DF21_…`, `LR_Q1_…`; verified by `effort/checks/check_effort_reproduction.py` |
| Share of tax revenue from labor-income bases 0.68 (2025), 0.64 (1965) | `data/lambda_results.csv`, column `lamR_med` (`code/lambda_compute2.py`) |
| Conditioned share of benefits at least 0.84; about 0.99 by withdrawal rule | `data/lambdaB_results.csv` (`lamB_floor`, `lamB_rule`), computed for the long draft in August 2026; the script that produced it predates this repository's first commit and is not included |
| Borrowing financed 19% of transfers in 2025, zero only in 1998–2000 | `data/four_way_split.csv` (`code/four_way.py`) |
| The HUD FY2025 fair-market-rent ceiling grid | `data/kappa_ceiling.csv` (`code/kappa_ceiling.py`, `data/hud_fy25_fmrs.xlsx`); `docs/kappa_ceiling_notes.md` |

## Submission files

`code/build_submission_docx.py` builds `paper/submission/manuscript_blind.docx`, the full
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
```

## Reproduce

From this folder, with the repository's virtual environment:

```
../venv/Scripts/python.exe code/fig_schedule.py
../venv/Scripts/python.exe code/fig_eras_workers.py
../venv/Scripts/python.exe code/lambda_compute2.py        # FRED (cache/); writes data/lambda_results.csv
../venv/Scripts/python.exe code/four_way.py               # writes data/four_way_split.csv
../venv/Scripts/python.exe code/fig_fourway.py
../venv/Scripts/python.exe code/feasibility_kappa.py      # writes data/kappa_results.csv
../venv/Scripts/python.exe code/fig_kappa_measurement.py
../venv/Scripts/python.exe code/kappa_ceiling.py          # needs python-calamine; writes data/kappa_ceiling.csv
../venv/Scripts/python.exe effort/code/build_fig3_realwage_fork.py       # Figure 3 chain, step 1 (1964 base)
../venv/Scripts/python.exe effort/code/build_fig3_realwage_fork_1950.py  # step 2 (1950 extension, the gate reference)
../venv/Scripts/python.exe effort/code/build_fig3_realwage_fan.py        # step 3: paper/figures/fig_deflator_fork.png
../venv/Scripts/python.exe effort/code/build_fullband_df_figures.py      # paper/figures/fig_consumption_financing_and_human_effort.png
```

The measurement scripts read `cache/` and pull from FRED only for series not cached;
`--refresh` on the Figure 3 scripts re-pulls their raw series. Every FRED series is
validated by identity checks and magnitude anchors before use; every contestable
classification runs as a labeled grid, and the reported object is the median with its
min–max band. The scripts stop rather than substitute when a source cannot be validated.

## Checks

```
../venv/Scripts/python.exe checks/check_pinning.py               # 51 checks: the recursion, the replacement closure, statics, the fork, the welfare pair, the priced exit
../venv/Scripts/python.exe checks/check_fan.py                   # the composite pricing display, Proposition 4(iv), the fork's data anchors
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
| `check_baseline_props.py` | the task margin, the recursion, the flat limit | Propositions 1, 2 and 4 at lambda = 0 |
| `check_closure.py` | the land-only closure | Appendix B, Proposition B.1 |
| `check_conditionality.py` | conditionality | Appendix C.1 |
| `check_feasibility.py` | the coverage ratio | Appendix C.3 |
| `check_enclosure.py` | the priced commons | Proposition 3 and Appendix C.4 |
| `check_mix.py` | the mix frontier | Appendix C.5 |
| `check_kset.py` | the Baumol fork, the fraud bound, superstars | Appendix D |
| `check_open.py` | the open economy | the trade remark in Section 2 |
| `check_welfare.py` | the welfare pair | Proposition 5 |
| `check_fortification.py` | wedge targeting and punctuated adoption | the stabilizers section |
| `check_repairs.py` | existence and uniqueness; depreciation in the recursion | Lemma A.1 and Appendix A's durability paragraph |

`lean/` states and proves the full-automation chain, the lambda > 0 closure and its
comparative statics, the user-cost closures, the fraud and superstar lemmas, and the CES
share limits; its README lists the exact scope, the assumption manifest, and what is
deliberately left out.
