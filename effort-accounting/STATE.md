# STATE — effort-accounting (empirical companion thread)

**Project:** the two labor linkages of U.S. consumption, 1950–2025 — D-F
(labor-origin *financing* of PCE) versus D-Q (human-effort *content* of
consumed production), with C1 (product mix) and S1 (owner-land stock residual)
as supporting evidence. The empirics were produced in Stella's ChatGPT
collaboration (August 2026, archive versions v1→v28); this thread is their
repo home. The manuscript is still ChatGPT-side — nothing here is paper prose.
**Collaboration:** family contract inherited (direct critique, verify-lists,
Stella's standing rules; her voice rules apply to any future manuscript port).
**State as of:** 2026-09-01, fourth unit (her ask: food and energy deflator
lines — the FAN variant built and gated, uncommitted, exploratory).

## Where things stand

1. **The v28 reproduction archive is landed verbatim** at `archive_v28/`
   (69 files, 19.4 MB, including six legacy chat archives). It is provenance:
   read-only by convention, never edited in place.
2. **Reproduction VERIFIED on this machine** —
   `checks/check_effort_reproduction.py` (temp-dir rebuild using the
   archive's own build + verify, unmodified) is GREEN: all five numeric
   comparisons PASS (C28 ≤ 4e-12, DQ ≤ 7e-16, S1/DF19/DF21 exact). The
   archive's SHA-256 inventory verifies; only `outputs_reproduced/` (the
   build dir) churns, and the check compares numerics only.
3. **Independent cross-checks from the v27 review session**: decile detail
   aggregates to the panel at machine precision; bounds nested, central
   inside; the DF20 validation claims (mean 0.13pp / max 0.50pp) and the
   0.40pp DPI-agreement claim reproduce exactly; aggregates match NIPA;
   both claimed BEA distribution products confirmed real.
4. **The construction, for future sessions.** D-F works decile-by-decile
   (equivalized-DPI ranking): spending beyond current income (~6–11% of PCE)
   goes to a hard-intertemporal bucket excluded from labor attribution;
   within current-financed spending, labor origin is *bounded* (spend
   non-labor first / labor first, tax-source incidence free) with a
   proportional-allocation central. Judgment parameters: proprietor labor
   share (mid 0.75 in 1950 → 0.38 in 2023) and transfer wage-exposure
   look-through (mid ~0.72–0.80), both with low/high bands. D-Q: BEA
   WP2026-01 full-chain benchmark 1997–2023 (digitized, validated), extended
   1950–2025 by a five-spec OLS composition ensemble. Anchors: D-F 2004
   central 69.6% [59.8–83.1], 2023 65.8% [52.7–80.1]; D-Q 1950 ~66.4% (weak)
   → 2023 47.2% (strong). `archive_v28/source_manifests/` carry the P/R/T/F/Q
   ontology, the strong/weak memo with its guardrail, and the supersession
   register.
5. **Full-band figures ADOPTED** (her go, 2026-08-31): the paper-facing D-F
   and D-F/Q artwork is `figures/FIG_DF_fullband_...png` and
   `figures/FIG_DFQ_fullband_...png` (weak-year intervals drawn at a lighter
   tint, per the archive's own guardrail). Frozen originals remain in
   `archive_v28/expected/` as the reproduction reference.
6. **Figure 3 REBUILT from live FRED** (replacing the broken placeholder
   artwork): `code/build_fig3_realwage_fork.py` — AHETPI deflated by CPI
   durables (CUSR0000SAD) and CPI shelter (CUSR0000SAH1), annual means over
   complete years, 1964 = 100; the house construction
   (link-repo/code/deflator_fork.py; talk_data_briefing §1). All gates PASS
   and the built series lands exactly on the briefing's documented anchors:
   1983 seam ratio 1.46, 2024 legs 376.8 / 78.6, fork 4.79×. Output:
   `figures/FIG3_realwage_fork.png` + `data/fig3_realwage_fork.csv`; raw
   pulls vendored in `data/raw/` with a manifest. The series end at 2024
   because the October 2025 CPI was never published (shutdown-cancelled
   release) — the complete-year rule holds; reported, not patched.
7. **DF9/DF10 CONSOLIDATED** — the audit's named gap ("source-to-model
   reconstruction spread across legacy archives") is closed:
   `code/build_df9_df10_longrun.py` rebuilds both long-run ledgers in one
   script from v28 inputs plus vendored legacy intermediates
   (`code/vendor_legacy_inputs.py` → `data/legacy_inputs/`, provenance
   manifest included). Reconstructed rules, each verified to machine
   precision: composition shares = legal_income_audit; proprietor
   parameters = linear interpolation on the five proxy anchors 2005–2025 +
   OLS logit-linear backcast 1950–2004; transfer wage-exposure MID =
   program-value-weighted DF_3 exposures (Medicaid/other = DF_1's 0.75×0.68
   = 0.51); DF10 centrals = (1−T)×DF9 mid; capacity lower =
   max(0, (1−T_weak_upper)·PCE − (1−labor_low)·DPI)/PCE; capacity upper =
   min(labor_high·DPI, PCE)/PCE. `checks/check_df910_consolidation.py` is
   GREEN (5 checks): DF9 exact on all 17 numeric columns × 76 years; DF10
   exact everywhere except the documented window below; DF21 weak years
   match the rebuilt ledger.
8. **FINDING, pending her call — the 1958–1979 capacity uppers.** The
   archived DF10 upper bound for 1958–1979 (22 values) sits up to 3.28pp
   BELOW what the archive's own DF9 labor_high implies under the formula
   that reproduces every other year exactly. Consistent with DF10 having
   been built from a preliminary DF9 vintage whose pre-1970 high-scenario
   program-funding handling was later revised (the low-scenario lower bound
   is exact in exactly those years). The rebuild emits the coherent — wider,
   more conservative — values; report at
   `data/rebuilt/DF10_upper_1958_1979_discrepancy.csv`. These years are
   visible in the adopted full-band figures, so the call is live: adopt the
   rebuilt uppers into DF21 + regenerate the two figures, or keep the frozen
   values. One word either way; the regeneration is mechanical.
9. **S1 freshness caveat RETIRED** — `code/crosscheck_s1_fred.py` pulled the
   two Z.1 series live (BOGZ1FL155035013A, BOGZ1LM155012665A): all 162
   year-series cells within 0.1% of the archived snapshot, 141 identical,
   worst < 0.001%, 2020+ exact. The archived snapshot remains the canonical
   repro input; report at `data/s1_fred_crosscheck.csv`.

10. **Figure 3 extended-to-1950 VARIANT built, pending her call** (her ask,
    2026-09-01): `code/build_fig3_realwage_fork_1950.py` →
    `figures/FIG3_realwage_fork_1950.png` + `data/fig3_realwage_fork_1950.csv`.
    The adopted figure and its inputs are untouched; the 1964+ segment is
    gated to equal the shipped CSV to 1e-9 (deviation 0). Three growth-spliced
    long members, drawn dashed: wage = AHEMAN manufacturing AHE (monthly from
    1939; seam 1964, factor 1.0537 — the Swedish fork's long-member move, and
    the between-legs ratio is wage-invariant so this seam cannot touch any
    ratio claim); durables = CUUR0000SAD NSA, quarterly Mar/Jun/Sep/Dec in
    1950–55 (seam 1956; overlap validations: SA-vs-NSA annual means ≤0.09%
    apart 1956–2024, quarterly-subsample rule ≤0.24% off the 12-month mean in
    1956–65); shelter = CUUR0000SEHA rent of primary residence (seam 1953 —
    rent is the CPI housing concept that existed before shelter did; first
    post-seam decade rent ×1.183 vs shelter ×1.186). Output indexed
    1950 = 100 (her call, mid-unit): 2024 legs 619.0 / 104.5 — a 5.9× fork
    over 1950–2024, the shelter leg ending ~flat against 1950. Gates run on
    the internal 1964 base, so the adopted anchors (2024 legs 376.8 / 78.6,
    1983 seam 1.46) stay checked verbatim; in that base the 1950 points are
    60.9 / 75.2 (ratio 0.81 — the divergence direction already runs through
    the 1950s, with both legs rising strongly pre-1964). Long-member raws
    vendored to `data/raw/` with manifest rows. A second output (her ask,
    same day) overlays the D-F − D-Q gap — financing origin minus
    production content, from the frozen DF21_FINAL / LR_Q1 ledgers the
    full-band figures already draw — rebased to 0 at 1950 on a right axis
    whose zero sits on the legs' 100 line: raw 1950 gap +5.85pp; rebased
    +14.9pp (2004), +12.7pp (2023), +12.3pp (2024); solid only in the
    both-strong window 2004–23 (`FIG3_realwage_fork_1950_dfq_overlay.png`,
    `data/fig3_dfq_gap_overlay.csv`). All gates PASS (incl. frozen-ledger
    anchors and the both-strong window check).

11. **The deflator FAN built (exploratory variant, her ask 2026-09-01:
    food and energy lines to inform the fork section's rework)**:
    `code/build_fig3_realwage_fan.py` → `figures/FIG3_realwage_fan_1964.png`
    + `data/fig3_realwage_fan.csv`. Four legs on the adopted base 1964 =
    100, drawn 1950–2024 (dashed pre-1964, spliced-wage era): the fork's
    two legs rebuilt with the 1950 variant's exact splice rules and GATED
    transitively — rebased 1950 = 100 they must equal the shipped
    `fig3_realwage_fork_1950.csv` to 1e-9 (PASS, plus the adopted 2024
    anchors re-checked directly) — and two new single-series members
    pulled live and vendored with manifest rows: food = CPIUFDNS (CPI food
    NSA, monthly from 1913, no splice) and energy = CPIENGNS (CPI energy
    NSA, exists only from 1957; leg drawn from there). NOTE: the FRED ids
    are the mnemonic forms — the BLS-style CUUR0000SAF1/SA0E return 404 on
    fredgraph. Frozen sanity bands guard id drift. RESULT (2024, 1964 =
    100): durables 376.8 > food 113.2 > energy 95.8 > shelter 78.6 —
    the fan lands in exactly the land-content order the fork rework
    predicts, with food/shelter at 1.44×. Energy verdict (her guess
    confirmed): net-flat over sixty years with ±47% decade swings (peak
    127.3 in 1972, trough 67.6 in 1981, 1981→98 +66%, 2020→22 −26%) —
    world-oil-priced and cartel-shocked, unusable as a trend member,
    usable only as an honesty note. Colors: family blue/red kept for the
    established legs; Okabe–Ito orange/bluish-green for the additions
    (CVD-safe against red); direct end labels on all four. HER FOLLOW-UP
    (same day): output rebased to 1950 = 100 ("start the series at
    1950") with energy backcast 1950–56 by her explicit call ("you can
    use linear") — least squares on the deflator's first ten complete
    years 1957–66 (slope +0.183/yr, 1950 level 20.28, fit-vs-actual gap
    at 1957 just 0.39%), drawn dotted and flagged in the CSV's
    energy_member column; gates stay on the internal 1964 base (the
    1964-base endpoints above are the gated values; between-legs ratios
    are window-dependent — 4.79× is the 1964 window, 5.9× the 1950 one,
    matching the fork variant's documented distinction). Output now
    `FIG3_realwage_fan_1950.png`; 1950-base 2024 legs 618.9 / 166.8 /
    157.4 / 104.5. The v5 paper quotes the FOOD leg only (1964 window:
    +13% vs +277%/−21%), anchored by
    `the-link-revision/checks/check_fan.py` D1.

## Known gaps (kept honest)

- Raw source binaries absent for C1 (BEA Section2All XLSX) and D-Q (WP2026-01
  PDF); validated snapshots/digitizations are what's archived.
- Consolidation frontier (documented in `data/legacy_inputs/PROVENANCE_...csv`):
  the transfer wage-exposure LOW/HIGH scenario bounds are vendored archived
  series (per-program scenario recomputation from the funding histories is
  the remaining step); the 1950s composition/DPI backcast tables and the DF8
  timing floor (strong 2000–2023 hard bound + four-model weak extension) are
  vendored archived outputs whose generating passes predate the export.
- 2024–2025 D-F/D-Q values are weak-extension years; visible in the CSVs'
  tier column, small dashed tails in the figures.

## Verify-list — 2026-09-01, unit 4: the fan (veto window, current)

- [ ] Exploratory status: built to inform the paper discussion (the fork
      section rework on the v4 tex baseline — see the-link-revision STATE
      log 39); NOT paper artwork unless she adopts it.
- [ ] Member choices: headline food (CPIUFDNS) vs food-at-home
      (CUUR0000SAF11, exists from 1947) — headline chosen; energy kept
      despite the verdict (drop it, keep it as caveat, or omit from any
      adopted figure — hers).
- [ ] Base: output 1950 = 100 (her call, mid-unit — "start the series at
      1950"); gates stay on the internal 1964 base, so the adopted
      anchors are checked verbatim and all ratio claims are base-free.
- [ ] The energy backcast 1950–56 (her call: "you can use linear") —
      linear fit on 1957–66, dotted in the figure, flagged in the CSV;
      the energy leg's 1950 = 100 anchor stands on the fit. Bless the
      window choice, or trim energy to 1957 in any adopted artwork.
- [ ] Figure retitled "The deflator fork: …" (her ruling 2026-09-01:
      the CPI fork stays a fork), re-rendered, gates PASS. Internal
      names (build_fig3_realwage_fan.py, fig3_realwage_fan.csv,
      FIG3_realwage_fan_1950.png, check_fan.py) still say "fan" —
      rename on her word if this becomes adopted artwork.
- [ ] Uncommitted — commit scope `effort-accounting/` only (script, CSV,
      PNG, two vendored raws + manifest rows, STATE).

## Verify-list — 2026-09-01, unit 3: the 1950 extension (veto window, current)

- [ ] The three long members and their seams (wage AHEMAN@1964, durables
      NSA-quarterly@1956, shelter rent@1953) — the construction call itself.
- [ ] Output base 1950 = 100 (her mid-unit call, executed) — confirm on the
      rendered figure; the briefing's 1964-base endpoints (376.8/78.6/4.8×)
      stay true but become window-specific once this base is shown.
- [ ] Start-year choice: 1950 as built; or trim to 1953 (no rent stub) or
      1956 (no deflator splices at all — wage seam only); or keep 1964. The
      output base would follow the chosen start.
- [ ] Adopt as Figure 3 vs keep as variant; if adopted, the talk briefing's
      §0/§1 wording ("since 1964", "both forced to start at 100 in 1964")
      needs a matching pass — hers.
- [ ] The dashed-segment convention and the figure's seam annotation wording.
- [ ] The gap overlay (her ask, executed): mixing the CPI fork and the
      D-F/D-Q ledgers on one chart is a synthesis figure — confirm the
      framing, the 0-at-1950 rebase, and the right-axis alignment (gap 0 on
      the legs' 100 line).
- [ ] Uncommitted — commit scope would be `effort-accounting/` only (script,
      CSV, PNG, three vendored raws + manifest rows, STATE).

## Verify-list — 2026-08-31, unit 2: her go executed (veto window, current)

- [ ] Full-band adoption recorded as done (item 5) — the two files in
      `figures/` are the paper-facing artwork from here on.
- [ ] Figure 3: construction, gates, title wording ("machine-made goods /
      land-priced shelter"), and the 2024 endpoint (Oct-2025 CPI gap note).
- [ ] The 1958–1979 upper finding (item 8) — adopt rebuilt uppers or keep
      frozen; currently the figures still draw the frozen DF21.
- [ ] Consolidation frontier labeling (Known gaps) — the vendored-vs-
      generated split as stated.
- [ ] The commit (scoped to `effort-accounting/` only; hash in the log
      below).

## Verify-list — 2026-08-31, unit 1: the landing (resolved by her go)

- [x] Thread placement/name; archive verbatim incl. legacy zips.
- [x] The reproduction check and its GREEN wording.
- [x] Full-band figure variants → ADOPTED (unit 2, item 5).
- [x] link-repo v0 scaffold noted as superseded, left in place.
- [x] Commit authorized ("commit at the end").

## Next actions (priority order)

0. **Stella:** the unit-2 and unit-3 veto lists — above all the 1958–1979
   upper call and the 1950-extension seam/adoption calls.
1. **Manuscript ingestion** when she ports it from ChatGPT — her voice rules
   apply in full; timeless register for any data note.
2. Optional frontier closure, in value order: per-program scenario
   recomputation of the transfer exposure bounds (funding histories are in
   the v2 bundle); DF8 four-model weak timing rebuild; fresh pulls of the
   BEA XLSX to retire the C1 raw-binary caveat.

## File map

```
effort-accounting/
├── STATE.md                            ← you are here; start here next session
├── README.md                           orientation + run commands
├── archive_v28/                        the shipped reproduction archive, verbatim (read-only)
├── checks/
│   ├── check_effort_reproduction.py    archive rebuild + verify (GREEN 2026-08-31)
│   └── check_df910_consolidation.py    consolidated DF9/DF10 vs archived (GREEN, 5 checks)
├── code/
│   ├── build_fullband_df_figures.py    ADOPTED paper-facing D-F / D-F/Q artwork
│   ├── build_fig3_realwage_fork.py     Figure 3 from live FRED (gates + vendored raw)
│   ├── build_fig3_realwage_fork_1950.py  1950-extension VARIANT (pending her call)
│   ├── vendor_legacy_inputs.py         extracts legacy intermediates from in-repo zips
│   ├── build_df9_df10_longrun.py       the consolidated long-run D-F rebuild
│   └── crosscheck_s1_fred.py           live Z.1 vs archived S1 snapshot (report-only)
├── data/
│   ├── raw/                            vendored FRED pulls + manifest
│   ├── legacy_inputs/                  vendored legacy intermediates + provenance
│   ├── rebuilt/                        DF9/DF10 rebuilt + the 1958–79 discrepancy report
│   ├── fig3_realwage_fork.csv          Figure 3 series
│   ├── fig3_realwage_fork_1950.csv     extended variant series (per-year member columns)
│   ├── fig3_dfq_gap_overlay.csv        D-F − D-Q gap series (raw + rebased, tiers)
│   └── s1_fred_crosscheck.csv          S1 vintage comparison
└── figures/
    ├── FIG_DF_fullband_...png          adopted D-F artwork
    ├── FIG_DFQ_fullband_...png         adopted D-F/Q artwork
    ├── FIG3_realwage_fork.png          rebuilt Figure 3
    ├── FIG3_realwage_fork_1950.png     extended variant (dashed long members)
    └── FIG3_realwage_fork_1950_dfq_overlay.png  + D-F − D-Q gap overlay
```

## Repro notes

- Checks, from the repo root (shared venv; python 3.13, numpy 2.5.1,
  matplotlib 3.11.1):
  `./venv/Scripts/python.exe effort-accounting/checks/check_effort_reproduction.py`
  `./venv/Scripts/python.exe effort-accounting/checks/check_df910_consolidation.py`
  (the consolidation check re-runs vendor + rebuild itself; both write
  nothing inside `archive_v28/`).
- Figures: `code/build_fullband_df_figures.py` (adopted artwork),
  `code/build_fig3_realwage_fork.py` (add `--refresh` to re-pull FRED; the
  build otherwise reruns from `data/raw/` with zero downloads),
  `code/build_fig3_realwage_fork_1950.py` (extension variant; its `--refresh`
  re-pulls the three long members only — the established raws stay frozen).
- FRED is reachable from python urllib on this machine (AHETPI + two CPI +
  two Z.1 series pulled 2026-08-31); the long-record thread's host-block
  quirk does not affect fred.stlouisfed.org.
