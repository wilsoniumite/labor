# Understanding the Great Stagnation

A paper that stands on its own and cites *Pinning the Wage to Scarcity and Technology* (`../pinning/`) for the
general cost system. Its claim: measured output per hour is an equilibrium outcome, the inverse of the hours an
economy uses per unit of output; in a task economy whose prices resolve into hours and the rents of inputs that
cannot be produced, machine progress raises output per hour only as far as hours are released. It measures the
claim's implications in U.S. data since 1948 and across OECD countries since 1995, against predictions written down
before the data were pulled. `STATE.md` is the session entry point; `docs/spec.md` is the plan, the predictions and the
pre-registered test.

**Status (2026-11-16):** a complete draft, 30 pages. The theory (Sections 3–4, Appendices A–B) and the measurements
(Section 5) are checked by three batteries; Section 6 scores the predictions; Section 7 concludes. Byline: Stella
Wilson (see `STATE.md`).

## Layout

```
docs/spec.md          the spec: thesis, model, results, measurement plan M1-M5 with predictions, the frozen
                      cross-country test H-X (commit c8750c0, before any of the paper's data were pulled), amendments
paper/main.tex        the paper (pdfLaTeX); paper/figures/ the script-built figures (PDF included, PNG kept);
                      paper/tables/ the script-built table; paper/_build/ the compiled PDF (not committed)
code/model.py         the model: the stationary task economy with durable machines, land, and who can leave work
code/fig_paths.py     Figure 1: output per hour and hours along machine progress, four rules for who can leave work
code/fig_rates.py     Figure 2: the required return
code/table_regimes.py Table B.1: the instance under the four rules
code/fred.py          the FRED pulls (cache/fred/, with a manifest of times, rows and SHA-256)
code/eras.py          the eras of output per hour (FRED OPHNFB)
code/m1_eras.py       M1: the eras, hours per person, labor's share, the real rate, land's share; Figure 3
code/m2_industry.py   M2: the slowdown by sector (BEA-BLS integrated industry-level production account); Figure 4
code/m3_gap.py        M3: pay against productivity, labor's share and the price wedge; Figure 5
code/m4_hours.py      M4: hours per worker, U.S. against Europe (Penn World Table 11.0); Figure 6
code/m5_recent.py     M5: 2019 onward
code/hx_test.py       H-X: the frozen cross-country test (OECD Productivity Database); code/fig_hx.py, Figure 7
data/                 the measurement scripts' outputs (JSON, CSV)
cache/                raw data as pulled (MANIFEST.md says what, where from, when, and the SHA-256)
checks/check_theory.py  the theory battery (169 checks): sympy, a cross-check against the companion paper's solver,
                      equilibrium conditions from primitives, each result, 300 random economies, and every model
                      number in the theory sections found in main.tex next to its words
checks/check_hx.py    the H-X battery (21 checks): the frozen specification, the regressions recomputed with
                      statsmodels, the bootstrap at a second seed, the IV, leave-one-out, the decision rule, the text
checks/check_data.py  the measurement battery (107 checks): the caches' hashes, every data file against a fresh run,
                      second routes to the eras, the industry panel and the counterfactuals, the frozen verdicts, and
                      every number in the abstract, the introduction and Sections 5-7 inside a phrase rebuilt from
                      recomputed values, with no other number allowed there
```

## Figures and tables

| In the paper | File | Script | Inputs |
|---|---|---|---|
| Figure 1, output per hour and hours along machine progress | `paper/figures/fig_paths.pdf` | `code/fig_paths.py` | none (the model) |
| Figure 2, the required return | `paper/figures/fig_rates.pdf` | `code/fig_rates.py` | none (the model) |
| Figure 3, the eras | `paper/figures/fig_eras.pdf` | `code/m1_eras.py` | `cache/fred/` |
| Figure 4, where the slowdown lives | `paper/figures/fig_industry.pdf` | `code/m2_industry.py` | `cache/bea/` |
| Figure 5, pay against productivity | `paper/figures/fig_gap.pdf` | `code/m3_gap.py` | `cache/fred/` |
| Figure 6, hours per worker | `paper/figures/fig_hours.pdf` | `code/m4_hours.py` | `cache/pwt/` |
| Figure 7, the cross-country test | `paper/figures/fig_hx.pdf` | `code/fig_hx.py` | `cache/oecd/`, via `code/hx_test.py` |
| Table 1, the predictions scored | in `paper/main.tex` | numbers checked by `checks/check_data.py` | `data/` |
| Table B.1, the instance under four rules | `paper/tables/tab_regimes.tex` | `code/table_regimes.py` | none (the model) |

Each figure is drawn at the width it prints (0.88 of the 16 cm text width), text at 6.5–8.5 pt, no titles in the
image; the captions carry the words and end "Drawn by code written with Claude (Anthropic)." Series colors follow a
validated categorical order (blue, orange, aqua, yellow); lines are also labeled directly where the colors are light.

## Numbers in the text

| Reported | Source |
|---|---|
| Every model number in Sections 3–4 and the appendices | `code/model.py`, `numbers()`; recomputed and found by `checks/check_theory.py` (group Q) |
| Every data number in the abstract, the introduction and Sections 5–7 | the measurement scripts' outputs in `data/`; rebuilt from the cache and found in their phrases by `checks/check_data.py` (group Q) |
| The H-X results | `code/hx_test.py` → `data/hx_results.json`; recomputed by `checks/check_hx.py` |
| The real-wage fork, 4.8× (1964–2024), and the coverage ratio, 0.30 (2025) | cited from Båge and Wilson (2026), not rebuilt here |

## Reproduce

From this folder, with the repository's virtual environment (`../venv/Scripts/python.exe` on Windows,
`../venv/bin/python` on Linux). The data are cached; `code/fred.py` pulls only series not yet in `cache/fred/`.

```
python code/model.py              # the instance, the four rules, the paths, numbers()
python code/fig_paths.py          # Figure 1
python code/fig_rates.py          # Figure 2
python code/table_regimes.py      # Table B.1
python code/m1_eras.py            # M1, Figure 3
python code/m2_industry.py        # M2, Figure 4 (reads the BEA workbooks; about 15 s)
python code/m3_gap.py             # M3, Figure 5
python code/m4_hours.py           # M4, Figure 6
python code/m5_recent.py          # M5
python code/hx_test.py            # H-X (about 5 s)
python code/fig_hx.py             # Figure 7
python checks/check_theory.py     # 169 checks
python checks/check_hx.py         # 21 checks
python checks/check_data.py       # 107 checks
cd paper && latexmk -pdf -outdir=_build main.tex
```

The venv needs numpy, pandas, scipy, sympy, statsmodels, matplotlib, openpyxl, requests and tqdm; the build needs
TeX Live with latexmk.
