# Self-contained reproduction archive v28

This archive fixes the provenance problem in the v27 empirical freeze.

## Run the final numerical pipeline

```bash
python scripts/00_reproduce_all.py
python scripts/99_verify_reproduction.py
```

Requirements: `numpy`, `matplotlib`.

The reproduction scripts regenerate the C1, D-Q, S1, D-F, and D-F/Q figure data and artwork. `99_verify_reproduction.py` compares the reproduced numerical outputs against the frozen reference CSVs.

## What is complete

At the **final-figure level**, the archive is self-contained: every numerical input referenced by the final figures is included, and every transformation from those inputs to the final figure data is executable.

## Raw-source caveat

This is intentionally distinguished from perfect **primary-source-binary preservation**. Some older public-source files were not retained during the exploratory passes:

- C1: original BEA Section2All XLSX binaries are not present; their extracted Table 2.3.5 leaf-value snapshot is.
- D-Q: original BEA working-paper PDF is not present; the validated annual Figure-9 digitization is.
- S1: the exact annual Federal Reserve/FRED values and series IDs are archived, but the v28 snapshot was recovered from the prior D2 output.
- D-F: the uploaded BEA national distribution CSV is present; the weak long-run outer extension still uses the archived DF10 model output.
- Existing manuscript Figure 3 is retained as artwork rather than rebuilt from raw AHETPI/CPI series.

`REPRODUCTION_AUDIT.csv` records these distinctions so nothing is silently filled from inference.

## Why v28 is better than v27

v27's provenance file named upstream CSVs that were not packaged and did not include executable transformation scripts. v28 packages the upstream numerical inputs, the scripts, frozen expected outputs, source manifests, selected historical archives, SHA-256 inventory, and a successful verification log.
