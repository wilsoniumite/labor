# Labor, machines, and what remains

Working repository for **Pinning the Wage to Scarcity and Technology** (Johan Båge and
Stella Wilson) and for the papers planned around it. Written in collaboration with
Claude (Anthropic) and ChatGPT (OpenAI).

## The paper

[`pinning/`](pinning/README.md) holds the paper and nothing else: the LaTeX source and
its six figures, the scripts and vendored data behind every figure and every number in
the text, the computer-algebra and numerical check files, the Lean 4 formalization, and
the reproduction archive behind the financing and production accounts of Appendix E.

## Threads for later papers

Each folder is a self-contained thread whose `STATE.md` is the session entry point.

| Folder | What it grows toward |
|---|---|
| `dynamics/` | The dynamic extension (capital as time: waiting and build lags): the v2 dynamic draft of the paper, its transition engine and checks, the HTML-to-LaTeX pipeline. |
| `three-taxes/` | The fiscal architecture as labor's share falls: the three-tier taxonomy, gate-tax to rent-tax convergence, the 100 percent ceiling, the practical design. Sequenced after the dynamics paper. |
| `capability/` | Capability, education, experience: the talent/practice split, the machine mirror, task anatomy, the education race, the anatomy of wedges; the MORG premium-race data; the blind-coding stress test. |
| `companion/` | The empirical schedule: the OEWS task panel on the occ1990dd classification, the w/c grid, the revealed-adoption envelope, wedges, the right tail. |
| `long-record/` | One Schedule, Seven Centuries: the model's configurations fitted to the English wage record (parked at Breakpoint A). |
| `progress_and_prosperity/` | The book program (`PLAN.md`: phases, chapter map, papers P1 to P5), the lambda series (is the labor content of machine production falling?), and data notes (the Swedish deflator fork). |
| `three-drivers/` | Napkin-grade data support for a blog post; not a paper. |
| `tools/` | Editing utilities shared across threads: word-level diff reports, reading views, HTML-to-PDF rendering. |

## History

The repository was restructured on 2026-09-04 for submission. Until then it held the long
draft *The Link* (`link-repo/`), the revision thread (`the-link-revision/`, now
`dynamics/`), and `effort-accounting/` (now `pinning/effort/`). Everything moved or
removed is at tag `pre-cleanup-2026-09-04`, and `git log --follow` traces every kept
file across the moves. Paths quoted in state files before that date refer to the old
layout.

## Environment

Python virtual environment at the repo root (`venv/`, Python 3.12: numpy, pandas, sympy,
matplotlib, requests, tqdm, openpyxl, pyarrow). Lean 4.33.0 with mathlib for
`pinning/lean` (see its README).
