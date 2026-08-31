# effort-accounting

Empirical companion measuring the two labor linkages of U.S. consumption,
1950–2025: **D-F** (what share of consumption spending is financed by
labor-origin income — roughly flat at 66–70%) versus **D-Q** (how much human
effort is in the production chain of what is consumed — falling from ~66% to
~47%). The wedge between them is the headline.

Produced in Stella's ChatGPT collaboration (August 2026, v1→v28); landed here
2026-08-31. `STATE.md` is the canonical state file — read it first, every
session. The manuscript itself is still ChatGPT-side; only the empirical
package lives here.

## Layout

- `archive_v28/` — the reproduction archive exactly as shipped (inputs,
  scripts, frozen expected outputs, source manifests, SHA-256 inventory,
  legacy chat archives). Treated as read-only provenance; never edited.
- `checks/` — `check_effort_reproduction.py` rebuilds everything in a temp
  dir from the archive's own scripts and verifies against the frozen
  outputs; `check_df910_consolidation.py` gates the consolidated long-run
  D-F rebuild against the archived ledgers.
- `code/` — repo-side pipeline: the adopted full-band D-F figures, the
  Figure 3 rebuild from live FRED, the legacy-input vendoring, the
  consolidated DF9/DF10 rebuild, and the S1 vintage cross-check.
- `data/` — vendored raw pulls, vendored legacy intermediates (with
  provenance manifest), rebuilt ledgers, and cross-check reports.
- `figures/` — the adopted paper-facing artwork (full-band D-F and D-F/Q,
  rebuilt Figure 3); frozen originals stay in `archive_v28/expected/`.

## Run the checks

```bash
./venv/Scripts/python.exe effort-accounting/checks/check_effort_reproduction.py
```

```bash
./venv/Scripts/python.exe effort-accounting/checks/check_df910_consolidation.py
```
