# λ unit 1 — prior-art scan and ICIO routing (2026-08-20)

Scope per `lambda_spec.md` next-units item 1: does the series already exist;
what the adjacent literature offers; resolve the ICIO 403. Everything below
was probed or search-verified this day; items marked [model knowledge] are
from Claude's training and must be verify-quoted at drafting time before any
of them is cited in prose.

## Existence verdict: build ours

No published series is the committed object (vertically integrated
labor-compensation share of machinery final output, banded across sector
definitions, with a world-content referee). The near misses:

- **BLS Employment Requirements Matrices** — the closest existing object,
  and it is the *hours* version: direct + indirect employment per $1M of
  final demand by industry, historical tables in nominal and chained-2017
  dollars, domestic and total requirements variants
  (`bls.gov/emp/data/emp-requirements.htm`). **Dated wall:** BLS removed all
  ERM tables 2026-02-06 — "the percentage of total industry output that is
  value added was incorrect in some tables of employment projections data
  for researchers… therefore, those tables may also be incorrect and were
  removed" — republication promised at the next Employment Projections
  release. Consequence: adopted as Family A's secondary member (hours
  cross-check) once republished; our compensation-share build from BEA
  source tables is independent of the BLS error and does not wait.
- **Pasinetti vertically integrated subsystems** — an active empirical
  literature (a six-economies structural-dynamics implementation 1995–2015;
  a US industrial/electric-power subsystem study on 2014–2023 data). Method
  lineage for the λ̂ formula — none of it produces our series or window.
  The λ̂ construction should cite this lineage beside Leontief/Sraffa.

## Adjacent literature (what each contributes)

- **Kehrig & Vincent, "The Micro-Level Anatomy of the Labor Share Decline"
  (QJE 2021):** US manufacturing labor share fell ~67%→47% of value added
  over three decades, driven by reallocation to hyper-productive plants
  whose own labor share fell, while the typical plant's rose. This is the
  *direct-share* cousin at the manufacturing aggregate: our direct-share
  companion series will land in known territory; the VI resolution and the
  world referee are what the assembly adds.
- **"Labor share decline across US manufacturing sectors: 1979–2019"**
  (Utah WP 2023-07; Int. Rev. Applied Econ. 2026, 40(1)): sub-sector
  decomposition — pull at build to compare our narrow-set direct shares.
- **Houseman, Bartik & Sturgeon (2015), "Measuring Manufacturing: How the
  Computer and Semiconductor Industries Affect the Numbers and
  Perceptions":** the standing citation for why computer-sector real-output
  and productivity statistics mislead (hedonics, offshoring bias) — the
  honesty citation for demoting the hours variant and for the
  domestic-vs-world caveat.
- **vom Lehn & Winberry, "The Investment Network…" (QJE 2022):** builds the
  US sectoral investment network from BEA capital-flows data; "investment
  hubs" produce most investment goods. Two steals: (i) their network is a
  candidate weighting for f_M (machinery final demand weighted by actual
  investment flows rather than total final demand) — grid-axis candidate,
  decide at build; (ii) hub composition is an external check on our
  machine-sector definitions.
- **Caunedo & Keller, "Capital-Embodied Structural Change" (2023):**
  adjacent on capital embodiment across countries; not our object; possible
  positioning citation.
- [model knowledge, verify at drafting] **KORV (2000)** and
  **Karabarbounis & Neiman (QJE 2014)**: the falling relative price of
  investment as labor-share mechanism — the *cousin claim* (machines got
  cheap) to keep carefully distinct from ours (the wage bill inside the
  machine's own cost base shrank). **Grossman & Oberfield, "The Elusive
  Explanation for the Declining Labor Share" (Ann. Rev. 2022)** for
  positioning; **Elsby, Hobijn & Şahin (2013)** for labor-share measurement
  choices (self-employment imputation — already a grid axis).

## ICIO routing: RESOLVED, GREEN

The dataset landing page 403s every non-browser client on this machine
(harness fetcher, curl, PowerShell) — but the in-app browser loads it, and
the *file host behind it serves the harness fetcher without complaint*.
Verbatim URL set harvested from the live page 2026-08-20:

2025 edition (current: Jan-2026 second revision; "no further revisions
anticipated"), regular ICIO, CSV zips on
`https://webfs-sti.oecd.org/files/STI-PIE/ICIO/2025/`:

    1995-2000_SML.zip   2001-2005_SML.zip   2006-2010_SML.zip
    2011-2015_SML.zip   2016-2022_SML.zip
    ReadMe_ICIO_small.xlsx   ICIO2025annex.pdf

Extended (China/Mexico split) variants `*_EXT.zip` and
`ICIO2025econ{A,B,VB,Z,OTHER}.zip` (Rdata) on the same path. Earlier
editions same host: `/ICIO/2023/…` (1995–2020) and `/ICIO/2021/…`
(1995–2018) — pinned fallbacks if the 2025 files move.

Fetch matrix, tested this day: browser GREEN (page + links);
**harness fetcher GREEN** (`ReadMe_ICIO_small.xlsx`, 320.7KB, pulled);
local curl 403; PowerShell 403. Pull route: harness fetcher per file.
Residual risk, stated: the data zips are ~10²MB and the fetcher is proven
only on small files — fallback is a documented manual vendored-download
step (long-record precedent), five clicks.

2025-edition facts (annex + ReadMe, parsed): **1995–2022, 81 areas (80
economies + ROW), 50 activities** (ISIC Rev.4; agriculture and mining at
2-digit, basic metals split ferrous/non-ferrous, ships split from other
transport). Machine-set concordance for the grid:

- narrow: `C26` (computer, electronic, optical), `C27` (electrical
  equipment), `C28` (machinery n.e.c.)
- medium adds: `J62_63` (computer programming and information services).
  Coarseness caveat: software *publishing* sits inside `J58T60` with
  audiovisual — not separable in ICIO (BEA is finer).
- broad adds: `C31T33` — contains repair and installation of machinery but
  merged with furniture/other manufacturing (coarse member, labeled).
  Equipment leasing sits inside `N` (admin/support, 77–82) — too coarse to
  use in ICIO; the broad set's leasing member is BEA-only.
- ICIO rows carry value added but **no compensation split** — the labor
  layer must come from the pairing (WIOD SEA probed green; OECD TiM landing
  recorded: `oecd.org/en/data/datasets/trade-in-employment.html`, to probe
  at Family B build).

## Consequences folded back into the spec

1. Sources table: ICIO → GREEN with route; BLS ERM added as Family A
   secondary member with dated-wall status; TiM landing URL recorded.
2. Family A gains the ERM cross-check sentence.
3. f_M weighting by investment flows (vom Lehn–Winberry) noted as a
   grid-axis candidate, decided at build.
