# the-link-revision

Working folder for the revision of *The Link: Wages, Machines, and What Remains* (Stella Wilson, working draft Aug 2026), developed in an ongoing collaboration with Claude. Sits next to the papers folder.

**Start with `STATE.md`** — it holds the current state, the session log, standing rules, decisions taken, and the prioritized next actions.

- `sketch/` — draft blocks for the paper (the talent/practice split, machine mirror, task anatomy, education race, anatomy of μ). Provisional numbering; the algebra pass is complete — every flag records its check outcome (two amendments), scripts in `checks/`.
- `stress-test/` — the blind-coding pilot for the task taxonomy: printed coding rule, 21 resolved cases, score, and six pre-registered dated predictions.
- `data/` — the three data items delivered so far, with `DATA_NOTES.md` as the record: the premium race (passes one and two: series CSVs, the 5.24M-row CPS MORG extract, composition-adjusted grid, race decomposition), the κ ceiling (32-member grid vs 1), and the demolition-order cross-section (D proxies × exposure × movement).
- `code/` — one script per data item: the pull (self-contained, idempotent; re-downloads the ~2 GB of raw MORG microdata, deliberately not vendored), pass two (extract only, no downloads), the κ ceiling (FRED live + HUD), and the demolition-order cross-section (offline from the companion's cache).
