# capability — capability, education, experience (a later paper)

Question: how human capability investment, schooling before the market and experience
inside it, races the flattening front. This is paper P3 of the program in
`../progress_and_prosperity/PLAN.md`. The material was developed inside the revision
thread in August 2026 and split out on 2026-09-04.

- `sketch/` — the draft blocks: A the talent/practice split and B the machine mirror
  (`link-sketch-blocks-AB.md`); B.0' task anatomy, C the education race, D the anatomy
  of the wedge (`link-sketch-blocks-B0-C-D.md`); E the misallocation ledger, first look
  (`link-sketch-block-E-misallocation.md`). Numbering is provisional; every [check] flag
  records its outcome.
- `checks/` — one sympy plus numeric script per block (`check_split`, `check_mirror`,
  `check_anatomy`, `check_race`, `check_mu`); all pass, two with recorded amendments
  (B2's covariance term, C1's lag-indexed stability condition).
- `stress-test/` — the blind-coding pilot for the task taxonomy: the coding rule,
  21 resolved cases, the score, six pre-registered dated predictions.
- `data/` — `DATA_NOTES.md` is the record. The premium race (CPS MORG 1979–2024:
  `morg_extract_1979_2024.parquet`, 5.24M rows; `morg_premium_annual.csv`; pass two
  `morg_premium_pass2.csv` with the Goldin–Katz composition adjustment and
  `race_decomposition.csv`), attainment and conferrals (Census A-2, NCES 318.10), the
  NY Fed underemployment queue, the demolition-order cross-section, the misallocation
  first look.
- `code/` — `pull_premium_race.py` (self-contained, idempotent; re-downloads about
  2 GB of MORG microdata, deliberately not vendored), `premium_pass_two.py` (extract
  only, no downloads), `demolition_order.py` (offline from `../companion/cache`),
  `misallocation_firstlook.py`.

Related, kept elsewhere: the companion's schedule measurements (`../companion/`); the
parked second-paper critiques are recorded in `STATE.md`.
