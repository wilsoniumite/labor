# effort — the financing and production accounts (Appendix E)

Two labor linkages of U.S. consumption, 1950–2025: the share of consumption financed
from labor-origin resources (D-F, about 66–70 percent and roughly flat) and the share of
consumed production that resolves into human effort through the full production chain
(D-Q, from about 66 percent to 47 percent). Produced in Stella Wilson's ChatGPT
collaboration (August 2026, archive versions v1 to v28) and landed here 2026-08-31.

## Layout

- `archive_v28/` — the reproduction archive exactly as shipped: inputs, scripts, frozen
  expected outputs, source manifests, SHA-256 inventory, and the legacy chat archives.
  Read-only provenance; never edited.
- `checks/` — `check_effort_reproduction.py` rebuilds everything in a temporary
  directory from the archive's own scripts and compares to the frozen outputs (C28 to
  4e-12, DQ to 7e-16, S1/DF19/DF21 exact); `check_df910_consolidation.py` gates the
  consolidated long-run D-F rebuild against the archived ledgers (5 checks; the one
  documented exception is the 22 archived 1958–1979 capacity uppers, up to 3.28pp
  tighter than the archive's own DF9 implies).
- `code/` — `build_fullband_df_figures.py` draws the D-F figure and the paper's
  Figure 5 with the weak-year bounds drawn at a lighter tint (the archive's own
  guardrail); the Figure 3 chain is `build_fig3_realwage_fork.py` (1964 base, live FRED,
  vendored raws), `build_fig3_realwage_fork_1950.py` (the 1950 extension with spliced
  long members, the gate reference), and `build_fig3_realwage_fan.py` (the four-leg
  figure the paper prints); `vendor_legacy_inputs.py` and `build_df9_df10_longrun.py`
  rebuild the long-run financing ledgers from v28 inputs plus vendored legacy
  intermediates.
- `data/` — `raw/` holds the vendored FRED pulls with a manifest; `legacy_inputs/` the
  vendored intermediates with their provenance file; `rebuilt/` the DF9/DF10 rebuild and
  the 1958–79 discrepancy report; the Figure 3 series are `fig3_realwage_fork.csv`,
  `fig3_realwage_fork_1950.csv`, `fig3_realwage_fan.csv` and `fig3_dfq_gap_overlay.csv`.
- `figures/` — the D-F figure and the Figure 3 chain's intermediate renderings. The
  paper's own figures are written to `../paper/figures/`.

## Construction

D-F works decile by decile on equivalized disposable income: spending beyond current
income (about 6–11 percent of PCE) goes to a hard intertemporal bucket excluded from
labor attribution; within current-financed spending, labor origin is bounded (non-labor
spent first or labor spent first, tax-source incidence free) with a proportional
allocation as the central value. Judgment parameters, each with low and high bands: the
proprietor labor share (0.75 in 1950 to 0.38 in 2023) and the transfer wage-exposure
look-through (about 0.72–0.80). D-Q uses the BEA WP2026-01 full-chain benchmark for
1997–2023 (digitized and validated) and a five-specification composition ensemble
outside that window. Anchors: D-F 69.6 percent [59.8–83.1] in 2004 and 65.8 [52.7–80.1]
in 2023; D-Q about 66.4 percent (weak) in 1950 and 47.2 (strong) in 2023. The
ontology, the strong/weak memo with its guardrail, and the supersession register are
in `archive_v28/source_manifests/`.

## Known gaps

- Raw source binaries are absent for C1 (the BEA Section2All workbook) and D-Q (the
  WP2026-01 PDF); validated snapshots and digitizations are what is archived.
- The transfer wage-exposure low/high bounds, the 1950s composition and DPI backcast
  tables, and the DF8 timing floor are vendored archived outputs whose generating
  passes predate the export (`data/legacy_inputs/PROVENANCE_legacy_inputs.csv`).
- 2024–2025 D-F and D-Q values are weak-extension years (the tier column in the CSVs;
  dashed tails in the figures).
- The Figure 3 series end in 2024 because the October 2025 CPI was never published;
  the complete-calendar-year rule holds.

Run commands are in `../README.md`.
