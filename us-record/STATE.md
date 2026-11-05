# STATE — us-record (the backward model; resume point for the next session)

**Project:** the paper's model run through the US record, 1950–2025: a test the mechanism could fail, the clocks
measured, an attribution, and a 2025 starting point for the forward model in `../paths/`. The governing document is
`SPEC.md`; read it first.
**Collaboration:** same contract as the sibling threads: drafting and sequencing delegated to Claude, checks gate
absolutely, direct critique over validation; the decisions below are a veto window for her calls. Code in plain
functions, notebook-cell style; `tqdm` on any outer loop that takes more than a few seconds.
**The wall:** this repository is public. Public data only (FRED, BEA, the Fed's Z.1).
**State as of:** 2026-11-05. Phases 0 and 1 done: `SPEC.md` committed before any data; the data panel built
(`code/panel.py` -> `data/panel.csv`, 76 years x 32 columns, `data/manifest.csv` with each source's SHA-256),
gated (`checks/check_panel.py`, 21/21), its mapping written (`docs/measurement.md`) and drawn
(`code/fig_panel.py` -> `figures/fig_panel.png`). Nothing fitted. **Waiting at breakpoint A (hers): the mapping and
the panel.**

## The three models

1. The pinning model, `../pinning/code/pinning_model.py`: the paper's.
2. **This thread**: the backward model, the pinning model against 75 years of US data.
3. The forward model with a crash, in `../paths/`: the complex model (`code/macro.py` and its layers) and the crash
   model (`code/global_crash.py`), today two pieces that do not read each other's results, to be joined. It takes its
   start and its clock from this thread (`SPEC.md` section 9).

## Decisions (veto window)

1. **US first** (her call, 2026-11-05), annual, 1950–2025: the window the effort accounts and the fork cover.
2. **Accuracy through simplicity** (her call, 2026-11-05): the paper's model with as few additions as the record
   forces; anything that does not do much is cut; credibility from few free numbers and untargeted facts rather than
   many holdout sets. One time split reported as a reading only.
3. **Aggregate participation only.** The participation thread's US series by sex and age stay unseen until its
   long-run freeze (`../participation/STATE.md`, "The long run"); women's entry enters as a shift backed out of the
   aggregate rate (addition B), not read from those series.
4. **The earn-its-place rule** (`SPEC.md` section 6): a component stays if removing it raises the misfit by at least 20%
   or takes a targeted series out of its band; set before fitting, revisable once at breakpoint B.
5. **The folder** is `us-record/`, a new thread; `../archive/long-record/` (seven centuries of English wages) is the
   method's precedent, not its base.
6. **The long rate is Moody's Aaa** (Phase 1): the ten-year Treasury starts in April 1953; Aaa covers the window and is
   closer to a firm's cost of funds. The Treasury version is kept beside it.
7. **Expected inflation is the mean log CPI inflation of the five years to t** (Phase 1): simple and complete; it lags
   turning points (`docs/measurement.md`, choice 3).
8. **Complete calendar years only** (the repository's rule): with October 2025 never published, the monthly series end
   in 2024; nothing is filled or extended.
9. **θ_V linked across bases at 1997** (Phase 1): the λ thread's 1967–1992 benchmark points (narrow machinery,
   import-comparable) carried onto calibration (c)'s basis by the 1997 ratio; nothing measured before 1967.

## Next

1. **Breakpoint A (hers):** the mapping (`docs/measurement.md`) and the panel (`figures/fig_panel.png`). Then Phase 2:
   the base model fitted — the pinning model each year on the measured inputs, one smooth capability clock, the fixed
   parameters once over the record — with year-by-year accounting as a diagnostic, up to breakpoint B, the stop point.

## Log

1. **2026-11-05 — founded.** From her question in the session that unified the pinning model ("what do we even want
   from this model?"): the three-model layout (pinning; backward over 70 years; forward with a crash), US first, and
   simplicity as the discipline. `SPEC.md` written before any data or fit.
2. **2026-11-05 — Phase 1, the data panel.** Built from files already in the repository (the fork's legs, the effort
   accounts, κ, the financing splits, the λ series, chains.json, the waterline, FRED and BEA caches) and three new public
   fetches (FRED CNP16OV and CE16OV, BEA Fixed Assets section 1), each in `cache/` with its SHA-256 in the manifest.
   Gated 21/21 after the first run, which failed four checks, each fixed at its cause and marked in the battery: I4
   (the panel was written at ten digits; it is now full precision, and the check tolerates the last bit, because
   chains.json and calibration_c.json store the same number one unit apart); I5 (the four financing columns are separate
   medians and need not add to one); B1 (the labour-share band is the WEAK years' only); S2 (the 1981–85 real-rate floor
   was a guess; the adaptive expectation lags the disinflation). What the panel shows, before any model: the wage in
   durables rose about six-fold since 1950, while the wage in shelter peaked in 1973 and has stood near its 1950 level
   since 1990; labour's share of consumption fell from 0.66 to 0.47; the 16+ employment rate rose from 0.56 to 0.64 by
   2000 and stands at 0.60; the real long rate was highest in the 1980s and near 1% in 2023–24; depreciation rose from
   0.040 to 0.053; the machine chain's labour share fell from about 0.52 around 2000 to 0.45-0.47 since 2010.
