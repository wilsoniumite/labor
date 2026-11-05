# Labor, machines, and what remains

Working repository for **Pinning the Wage to Scarcity and Technology** (Johan Båge and
Stella Wilson) and for the papers planned around it. Written in collaboration with
Claude (Anthropic) and ChatGPT (OpenAI).

## The paper

[`pinning/`](pinning/README.md) holds the paper and nothing else: the LaTeX source and
its eight figures, the scripts and vendored data behind every figure and every number in
the text, the computer-algebra and numerical check files, the Lean 4 formalization, and
the reproduction archive behind the financing and production accounts of Appendix E.

## The models

Three models, each implemented once. Work that needs one imports it rather than copying it.

| Model | Code | What it is |
|---|---|---|
| The pinning model | `pinning/code/pinning_model.py` | The paper's Appendix B economy: task assignment, machines at Appendix A.4's user cost with the machine chain's ceiling, participation against funded support. Solved, and calibrated from seven shares in closed form, returning both roots in the schedule's convexity k. The paper's instance (`pinning/code/appendix_b.py`) is its calibration at U.S.-like shares, rounded. |
| The complex model | `paths/code/macro.py` and the modules built on it | The pinning model along a technology path at three speeds, with bridges to rates, public finances, households, a stylised bank and the yield curve. Its central calibration is (c), the machine chain at its measured size (`paths/code/calibration_c.py`). |
| The crash model | `paths/code/global_crash.py` (its fit: `paths/code/episodes.py`) | Four economies (five regions) through a bust: displacement, adoption in recessions, banks, trade and policy rules, fitted by month on past crashes from 1929–33 to 2008–10. It shares no code with the other two. The website runs it. |

`paths/README.md` groups the modules by model.

## Threads

Each folder is a self-contained thread whose `STATE.md` is the session entry point.

| Folder | What it grows toward |
|---|---|
| `paths/` | The complex and crash models' thread: the mechanism as paths over time at speeds set by three clocks (technology, recognition, institutions), built for risk; the yield curve and its checks (the public test on the Fed's 2021–23 cycle is a record at the tag `paths-pre-cuts`); her case on a dated vintage; the splits tracker. Public data only. |
| `participation/` | Participation in the model's terms (sex, age, retirement, schooling, youth): a pre-registered test of the outside option's floor kink on a European country panel, with an explore/confirm country split and a time holdout. Public data only. Its derivations predate the paper's support formulation (the floor kink left `main.tex` on 2026-11-02). |
| `capability/` | Capability, education, experience: the talent/practice split, the machine mirror, task anatomy, the education race, the anatomy of wedges; the MORG premium-race data; the blind-coding stress test. |
| `companion/` | The empirical schedule: the OEWS task panel on the occ1990dd classification, the w/c grid, the revealed-adoption envelope, wedges, the right tail. |
| `three-taxes/` | The fiscal architecture as labor's share falls: the three-tier taxonomy, gate-tax to rent-tax convergence, the 100 percent ceiling, the practical design. |
| `progress_and_prosperity/` | The book program (`PLAN.md`: phases, chapter map, papers P1 to P5), the lambda series (is the labor content of machine production falling?), and data notes (the Swedish deflator fork). |
| `three-drivers/`, `austax/` | Blog support, napkin-grade: data for a blog post, and Australian data for the Austaxpolicy article on the paper. |
| `tools/` | Editing utilities shared across threads: word-level diff reports, reading views, HTML-to-PDF rendering. |
| `archive/` | Parked lineages, not built on: the v2 dynamic draft and its transition engine, and the long wage record (`archive/README.md`). |

## History

This repository's history starts on 2026-09-24. The September restructure kept what it
moved or removed at the tag `pre-cleanup-2026-09-04`, which is not on GitHub; the August
history is on the branch `lean-formalization`. Paths quoted in `STATE.md` logs are as they
were when written.

## Environment

Python virtual environment at the repo root (`venv/`, Python 3.12: numpy, scipy, pandas,
sympy, matplotlib, requests, tqdm, openpyxl, pyarrow). Lean 4.33.0 with mathlib for
`pinning/lean` (see its README).
