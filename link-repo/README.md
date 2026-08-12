# The Link — wages, machines, and what remains

A task model of automation, job rents, and the fiscal system, with U.S. measurements 1962–2025.

One sentence: wages are prices on the non-uniformity of human capability relative to machines across tasks; automation demolishes the strata of a paycheck from the top down (job rents first, capability premium second, participation last), the released value migrates to rents on non-produced factors, and the fiscal system — measured here at roughly seven-tenths wage-linked — thins with the base it stands on.

**Paper:** `paper/the_link.pdf` (HTML source alongside; figures rebuild from the `code/` scripts).

## Repository map

- `paper/` — the paper (PDF + HTML source; `the_link_plain.html` is the plain-English companion; `snapshots/` holds pre-pass states of the HTML)
- `NOTES.md` — working notes: decisions, notation registry, queue, per-session changelog
- `checks/` — the verification gate: one script per section of new material (sympy algebra + numeric instantiation); no proposition entered the draft before its check passed
- `drafts/` — the per-unit section drafts as authored (spliced into the paper; kept as provenance records)
- `code/` — all computation, plain Python, notebook-cell style
  - `lambda_compute2.py` — wage-linkage of consumption financing (λ_C) and tax revenue (λ_R), 1960–2025, medians and bands across a labeled grid of classification rules
  - `three_way.py` — split of non-owner-loop consumption financing: direct wages / wage-tax transfers / ownership-tax transfers
  - `four_way.py` — deficit-aware version: adds the borrowed channel with three attribution rules
  - `feasibility_kappa.py` — coverage ratio κ = rT/(N·P_s) of the rent-funded floor (Proposition 8), 1953–2025, medians and bands across land-source / cap-rate / bundle rules
  - `deflator_fork.py` — Prediction 8 drawn: the same paycheck deflated by durables CPI vs shelter CPI, 1964–2024 (complete calendar years only)
  - `make_figs.py` — regenerates Figures 1–5 (Figures 6–7 rebuild from `feasibility_kappa.py` and `deflator_fork.py`)
- `data/` — computed results (CSV). Re-running the code regenerates these from live pulls.
- `figures/` — paper figures plus the standalone λ band chart
- `docs/` — the formal model notes (`link_model_formal.md`), the merged-model companion (`layered_link_model.md`), a self-commissioned hostile referee report (`referee_report.md`) with the revisions it prompted already applied to the paper, the readability-rewrite brief (`rewrite_brief.md`), and the κ empirics spec (`feasibility_empirics_spec.md`)

## Reproduction

```
pip install -r requirements.txt
cd <repo root>
python3 code/lambda_compute2.py   # pulls ~17 annual NIPA series from FRED, ~2 min
python3 code/four_way.py
python3 code/three_way.py
python3 code/feasibility_kappa.py # pulls ~12 FRED series (Z.1, fixed assets, CPI), ~1 min
python3 code/deflator_fork.py     # pulls 3 FRED series, seconds
python3 code/make_figs.py
```

Data are pulled live from FRED (mirroring BEA NIPA annual series) and cached in `cache/` on first run; FRED rate-limits bursts, and the scripts back off politely and stop rather than substitute if a series cannot be validated. Every series is validated by identity checks and loose magnitude anchors before use; every contestable classification (proprietors' labor share, tax progressivity tilt, corporate incidence, transfer funding, saving attribution, deficit attribution) is computed under all defensible variants, and reported objects are medians with min–max bands across the grid. The paper's data note describes the method in one paragraph.

Vintage: series retrieved August 2026. Program-level benefit detail runs through 2024; gross imputed rent through 2022; everything else through 2025.

## Status

Working draft. Comments, corrections, and hostile readings welcome — the `docs/referee_report.md` shows the standard applied so far.

License: [to be added]. Contact: Stella Wilson — thmwi@kth.se.
