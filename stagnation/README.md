# Understanding the Great Stagnation

A paper that stands on its own and cites *Pinning the Wage to Scarcity and Technology* (`../pinning/`) for the
general cost system. Its claim: measured output per hour is an equilibrium outcome, the inverse of the hours an
economy uses per unit of output; in a task economy whose prices resolve into hours and the rents of inputs that
cannot be produced, machine progress raises output per hour only as far as hours are released. `STATE.md` is the
session entry point; `docs/spec.md` is the plan, the predictions and the pre-registered test.

**Status (2026-11-16):** the theory is complete and checked (Sections 3–4, Appendices A–B); the introduction and
Section 2 are drafted; Sections 5–7 are outlines until the data are pulled. Byline open.

## Layout

```
docs/spec.md          the spec: thesis, model, results, measurement plan M1-M5 with predictions, the frozen
                      cross-country test H-X (commit c8750c0, before any of the paper's data were pulled)
paper/main.tex        the paper (pdfLaTeX); paper/figures/ the script-built figures (PDF included, PNG kept);
                      paper/tables/ the script-built table; paper/_build/ the compiled PDF (not committed)
code/model.py         the model: the stationary task economy with durable machines, land, and who can leave work
                      (theta: no support outside work; Delta: support paid for working); plain functions
code/fig_paths.py     Figure 1: output per hour and hours along machine progress, four rules for who can leave work
code/fig_rates.py     Figure 2: the required return
code/table_regimes.py Table B.1: the instance under the four rules
code/eras.py          the introduction's eras of output per hour (FRED OPHNFB)
cache/                raw series as pulled (MANIFEST.md says what and when)
checks/check_theory.py  the battery (142 checks): sympy, a cross-check against the companion paper's solver,
                      equilibrium conditions from primitives, each result, 300 random economies, and every
                      number in the theory sections found in main.tex next to its words
```

## Figures and tables

| In the paper | File | Script | Inputs |
|---|---|---|---|
| Figure 1, output per hour and hours along machine progress | `paper/figures/fig_paths.pdf`, `.png` | `code/fig_paths.py` | none (the model) |
| Figure 2, the required return | `paper/figures/fig_rates.pdf`, `.png` | `code/fig_rates.py` | none (the model) |
| Table B.1, the instance under four rules | `paper/tables/tab_regimes.tex` | `code/table_regimes.py` | none (the model) |

Each figure is drawn at the width it prints (0.88 of the 16 cm text width), text at 7.5–8.5 pt, no titles in the
image; the captions carry the words and end "Drawn by code written with Claude (Anthropic)." Series colors follow a
validated categorical order (blue, orange, aqua, yellow), each rule keeping its color in every figure; lines are
also labeled directly, since aqua and yellow sit below 3:1 contrast on white.

## Numbers in the text

| Reported | Source |
|---|---|
| Every model number in Sections 3–4 and the appendices | `code/model.py`, `numbers()`; recomputed and found in `main.tex` by `checks/check_theory.py` (group Q) |
| Output per hour 2.8 / 1.4 / 3.0 / 1.5 percent a year (1948–73, 1973–95, 1995–2004, 2004–19) | `code/eras.py` on `cache/OPHNFB.csv` (FRED); checked by group Q |
| The real-wage fork, 4.8× (1964–2024) | cited from Båge and Wilson (2026), not rebuilt here |

## Reproduce

From this folder, with the repository's virtual environment (`../venv/Scripts/python.exe` on Windows,
`../venv/bin/python` on Linux):

```
python code/model.py              # prints the instance, the four rules, the paths, numbers()
python code/fig_paths.py          # Figure 1
python code/fig_rates.py          # Figure 2
python code/table_regimes.py      # Table B.1
python code/eras.py               # the introduction's eras
python checks/check_theory.py     # 142 checks; exit 0 only if all pass (about 10 s)
cd paper && latexmk -pdf -outdir=_build main.tex
```

The venv needs numpy, pandas, scipy, sympy, matplotlib and tqdm; the build needs TeX Live with latexmk.
