# STATE — capability (resume point for the next session)

**Project:** paper P3, capability, education, experience (README.md here;
`../progress_and_prosperity/PLAN.md` for the program).
**Collaboration:** same contract as the sibling threads — working format, sequencing,
and drafting delegated to Claude; checks gate absolutely; direct critique; Stella's
standing rules (primary sources, stop and report on failure, sympy before prose,
notebook-cell code).
**State as of:** 2026-09-04 — folder created by the repository restructure. Nothing new
since the blocks' algebra pass (2026-08-09) and the premium-race data passes; all five
checks green from this path.

## Where things stand

The blocks were written and checked while the paper (now `../pinning/`) was the long
draft. Stella's pending decision of 2026-08-09 stands: the blocks become this paper
rather than merging into the pinning paper (Claude's recommendation on a full read of
the finished text; she had marked the critiques below as "probably the next paper, not
yet decided").

The parked critiques (2026-08-09): (1) the pinning paper's stark results live on the
empty-H edge of its own Baumol result while plausible H (law-reserved plus co-present
tasks) approaches half of employment — sizing H and modeling reallocation into it
(w_H dynamics, entry gates) is open machinery; (2) the land facts (the deflator fork,
Rognlie) have an unpriced rival in zoning, and the discriminating content is the second
derivative; (3) the rent taxonomy protects the migration claim from falsification and
needs dating like the stress test's pre-registered predictions; (4) the political
economy of enacting the remedy is absent (belongs with `../three-taxes/`).

## Next actions

1. Stella's placement decision (the blocks as this paper; the C-plus-experience vs
   wedge-anatomy split once the weight is known, per PLAN).
2. The junior extension and the credence application sketched in PLAN P3.
3. Numbers refresh at merge: the C-block sketches quote pass-one premium numbers
   (fixed-weight peak 1.887 in 2016); quote pass two (adjusted peak 1.925 in 2016,
   seam-safe compression −0.022 to −0.029) with the grid band.

## Repro notes

`code/pull_premium_race.py` is self-contained and idempotent (Cell 0 downloads MORG,
about 2 GB, plus Census A-2 and NCES 318.10; the NY Fed CSVs are fetched in-script).
With `data/morg_cache.csv` and the parquet present, later cells rebuild every series
with no downloads. `code/premium_pass_two.py` needs only the shipped parquet and
`morg_premium_annual.csv`: `../venv/Scripts/python.exe code/premium_pass_two.py` from
this folder, about a minute.
