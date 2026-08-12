# STATE — resume point for the next session

**Project:** revision of *The Link: Wages, Machines, and What Remains* (Stella Wilson, working draft Aug 2026; the blog post "A New-ish Theory of Economics" at wilsoniumite.com links the PDF — this folder sits next to the papers folder).
**Collaboration:** extended, multi-session; working format, sequencing, and drafting decisions delegated to Claude. Direct critique preferred over validation.
**State as of:** 2026-08-09.

## Where things stand

The paper went through a hard assumptions audit, then a theoretical extension (the talent/practice split + the task anatomy), a falsifiability stress test that passed, four new sketch blocks, and three data passes. **The algebra/numerical pass over the sketches is complete (2026-08-09):** all ten [check] flags verified in `checks/` (sympy + numeric per the house rule), eight clean and two WITH AMENDMENTS now recorded at the flags — B2's aggregate-dispersion claim needs the empirical covariance sign or the F2 channel, and C1's cobweb stability condition is lag-indexed ("product < 1" exact only at T_E = 1). The blocks are merge-eligible under the standing rule; merge SCOPE is still the pending decision below.

## Session log (2026-08-09)

1. **Assumptions audit** (chat-only; not filed here). Kill-shots identified: (i) the flattening premise on *existing* tasks — unmeasured; now addressed via Assumption F and data item one; (ii) free entry in machine-making — open; (iii) taxonomy near-tautologies ("dynamic rents expire," "institutional rents are policy-elastic") — open; (iv) the κ ceiling (κ → T/(N·hs), never checked against 1) — data item two; (v) the "each type prices its own link" heterogeneity claim is internally inconsistent with the AR cross-group propagation the paper cites — fix at merge.
2. **The split.** Capability: scalar talent θ (defined operationally: invariant to the model's instruments) × practice q, Ben-Porath complementarity (θ = learning gradient). Wage strata become four: exit floor + practice premium (cost recovery) + talent rent (Ricardian) + wedge. Slotting: practice = dynamic scarcity (two migrations: licensure → institutional; recording → idea); talent = physical on the supply side, transitional on the demand side, and fails the in-rem test land passes (Mirrlees; "George is Mirrlees with an observable base"). Scalar θ with task-varying loadings keeps comparative advantage (Costinot–Vogel cover); constant loading is the degenerate case.
3. **Task anatomy.** Dimension vectors; engineering vs learning rays (D — documentation density — gates learning rays only); transmission technologies (internet) are not rays: they enter via tradability, reach, and the D(x) path, never ρ; separability is component-wise (buffer test / narrow-channel test) and endogenous (standardize-then-automate).
4. **Stress test 1 (blind coding): PASSED.** 21 resolved cases, 20/21 on the bare rule; the pharmacist is the miss and proves the point — task anatomy and μ-anatomy are co-dependent classifiers, the wedge overlay admissible only with a citable instrument. Six live predictions pre-registered with dates (`stress-test/` §6, P-S1–P-S6).
5. **Sketch blocks A, B, B.0′, C, D drafted** (`sketch/`). Headline results: reinstatement mechanized (fragment creation on uncrossed dimensions — §10 branch-two repair); hump-shaped premium path derived from ray sequencing (widen/plateau/compress); the doomed vintage (practice acquired within a training-lag of its copying date is negative-NPV — a second negative-sum channel); μ speciated into five species; displacement-loss decomposition that **moderates** the paper's imported 60–90% negative-sum figure (D1); the demolition spectrum = the stress test's admissibility rule read as theory (D2).
6. **Decisions taken (delegated, recorded in `sketch/link-sketch-blocks-B0-C-D.md`):** belief friction = stated assumption, with C3's composition channel shown assumption-free; surveillance paragraph kept, decomposition-framed; species 4 labeled "slack rents," Graeber footnoted; doomed-vintage magnitude = banded back-of-envelope during the data pass.
7. **Data item one delivered** (`data/`). Premium from primary microdata (NBER CPS MORG, 1979–2024, 46/46 years, zero errors): widen 1.407→1.806 (1979–2000); plateau; fixed-weight peak **1.887 in 2016** → 1.837 (2024) — the compression leg exists but is young. 1992 CPS education redesign break marked, never spliced (raw 1.660→1.750 at the break). Census attainment 11.0% (1970) → 38.7% (2024); NCES conferrals with a post-2020 downturn in actuals; NY Fed queue monthly Jan 1990–Jun 2026, recent-grad underemployment chronically ~38–48%, ~8–9 pt excess over all graduates throughout. Blocked endpoints (FRED; BLS API/flat files/data viewer; EPI) documented in `data/DATA_NOTES.md` — reported, not substituted.

## Session log (2026-08-09, later session)

8. **Housekeeping (outer repo).** The outer root's working files were filed into their homes: `NOTES.md`, `checks/`, the `*_section.html` drafts, the six paper snapshots, `rewrite_brief.md`, `feasibility_empirics_spec.md` → `link-repo/` (root, `checks/`, `drafts/`, `paper/snapshots/`, `docs/`); `companion_schedule_spec.md` → `companion/`. Path-bearing references updated; all moves via git mv, staged, not yet committed. The outer venv was recreated (python 3.13, pandas 3.0.5, pyarrow 25).
9a. **κ ceiling delivered (data item two)** (`code/kappa_ceiling.py`; full record in `data/DATA_NOTES.md`). The ceiling T/(N·h_s) measured on the paper's own rT grid × HUD FY25 FMR floor-housing members: **median 1.26, band [0.38, 4.91], 13/32 members below 1** — shared-housing members clear 1 everywhere, solo-dwelling members mostly fail, population-weighted metros worst. Every measurement bias runs downward (lower-bound land, utilities in the denominator, missing economy-wide member), so audit iv resolves as **substantive robustness note, not fatal**: Prop 8's measured text stands, the "demolition funds its own remedy" framing takes a one-sentence ceiling caveat (surgical-repair list), and the h_s-is-partly-zoning observation feeds the parked second paper. FRED is reachable from this machine — pass-one's blocked-endpoint list was container-specific. BLS SPM 404 / Census SPM 520: reported, not substituted.
9b. **Premium pass two delivered** (`code/premium_pass_two.py`; full record in `data/DATA_NOTES.md`). Goldin–Katz proper: mean log wages, sex×experience cells, 6-member grid (topcode m {1.0, 1.4, 1.5} × weights {base8991, meanshare}). Reproduction gate vs pass one passed at 4e-16. Findings: (i) adjusted premium 1.434 (1979) → **peak 1.925 in 2016** → 1.882 (2024); every seam-safe member peaks 2016, compression −0.022 to −0.029 log points — pass one's shape survives the proper adjustment; (ii) **topcode discovery:** the static $2,884.61 cap was biting 15.7% of BA+ obs by 2022; April 2023 CPS moved to dynamic topcoding (visible as mass points above the old cap; 2023 hybrid, 2024 fully dynamic) — the m=1.0 members' 2024 "peak" is that seam, flagged; (iii) **the race:** free σ unidentified in-window (corr(t, relsupply)=0.9975; wrong-signed σ̂ reported, not used); under imposed σ {1.41, 1.64, 2.5} demand-index growth declines monotonically across eras to its historical low 2016–24 (0.018–0.021 log pts/yr) while supply growth did NOT slow (2.47%/yr) — the compression is **entirely demand-side**: shortfall vs continued-demand counterfactual −0.037 to −0.044 by 2024. This is the C2/C3-relevant measurement: the race stopped being winnable by supply restraint; the schedule side moved.
10. **Demolition-order cross-section delivered (data item three)** (`code/demolition_order.py`; full record in `data/DATA_NOTES.md`). D proxies from O*NET matched by name (discovery: the classic "Structured versus Unstructured Work" item is absent from 30.3; "Freedom to Make Decisions" reversed-by-anchor substitutes), walked to occ1990dd on the companion's own chains, offline. **Test A (order within the LLM-exposed): NOT yet visible** — median Spearman +0.05, 4/18 pairs negative; consistent with friction still binding (no exposure gradient exists yet for D to order), reported as a present-tense miss and left standing as a dated prediction, instrumented for the P-S re-reads (2028–30). **Test B (placebo): passed** — pre-LLM flips selected on routine (+0.5–0.6 sd), D gap conditional on routine NEGATIVE (−0.3 to −0.6z) and unchanged when rescored on era-correct O*NET 13.0 (2008) — not survivorship drift; reading: survivors are the residue holders who recomposed around the machine (rule outcome PARTIAL). The engineering-era demolition needed no corpus, as the anatomy says.
11. **Algebra pass delivered** (`checks/check_split.py`, `check_mirror.py`, `check_anatomy.py`, `check_race.py`, `check_mu.py` — all green). Ten flags: A0-DR (convex study tech changes nothing), A1-FP (single crossing symbolic + sorting-and-training fixed point numeric, PAM), A2-POOL (interior θ_m, free entry pins the premium, rents rise in θ), B1-OCC (occupying-type display is β(q_occ − D); β(1−D) is the frontier case), B2-COV (**AMENDED**: aggregate dispersion can RISE under F1 with a Moravec covariance — channel-tagging survives, aggregate claims need the Cov sign or F2), B0'1-MEAS (fragment creation as exact measure bookkeeping; creation = 0 at completeness), B0'2-RES (residual-requirement term explicit; continuous vs stasis-then-cliff), C1-COBWEB (**AMENDED**: "product < 1" exact only at T_E = 1; boundary tightens to ~0.2 at T_E = 8), C2-HUMP (single peak in the stable monotone regime; wiggles in the oscillatory), D1-CS (ledger + three statics; 60–90% → 60–90% × ω_wedge). C3's composition half verified friction-free as a bonus. Flags in `sketch/` updated in place with outcomes.

## Parked: the second-paper seed (2026-08-09)

A full zoom-out read of the finished paper (Claude, this session) produced four load-bearing critiques that Stella marked as **probably the next paper, not yet decided**: (1) the paper's stark results live on the K=∅ edge of its own Prop 11 while plausible K (law-reserved + co-present) approaches half of employment — sizing K and modeling reallocation into it (w_K dynamics, entry gates) is the open machinery; (2) the land facts (deflator fork, Rognlie) have an unpriced rival in zoning — the discriminating content is the second derivative; (3) the rent taxonomy protects the migration claim from falsification — Prediction 7 needs dating like the stress-test P-S set; (4) the political economy of enacting the remedy (taxing the only surviving asset class) is absent — belongs with the transition-dynamics sketch. Items (1) and (4) are new relative to the audit; (2) and (3) sharpen audit points. Do not fold these into the current revision uninvited; they are scoped as follow-on work.

**PENDING DECISION (Stella's, raised 2026-08-09):** whether the sketch blocks merge into the main paper at all, or become the next paper together with the critiques above. Claude's recommendation on a full read of the finished text: the paper takes only surgical repairs — the audit-v heterogeneity fix, Assumption F named in §10, a κ-ceiling sentence on Prop 8, possibly a political-economy paragraph in §10 — and everything else (the split, task anatomy, education race, μ anatomy, the premium data) becomes paper three. The companion never merges; it gets cited from the prediction tags once its measurements stabilize. Queue item "algebra pass then merge" narrows accordingly if confirmed. Also raised: the companion's figures failed the author-readability test — a figure-level Dr. R. pass on the companion is proposed work, not yet queued.

## Standing rules (Stella's — do not relax)

- **Data:** primary sources; on access failure, stop and report — never substitute, approximate, or fudge; validate every series before use.
- **Data purpose (added 2026-08-09):** every empirical deliverable must either MOVE BELIEF (survive a risk it could have failed, or kill a rival explanation) or SIZE IMPACT (people and dollars — and per the blog's "Millions of Lifetimes," lifetimes: weight can come from the PAST). Illustration alone does not count as a data item. Past-weight claims carry a heavy justification burden: counterfactual + attribution + magnitude, per channel, before any lifetime number is stated as measured.
- **Theory:** algebra must pass a computer-algebra check and equilibrium claims a numerical check before anything enters the paper.
- **Code:** flat notebook-cell style, plain functions over classes, `tqdm.auto` on slow loops.
- **Substance:** LVT vs VAT never forced to a corner — the interior mix is welcome. Direct critique; no sycophancy.

## Next actions (priority order)

1. **Merge (scope PENDING Stella's decision — see the pending-decision block above):** the checked blocks either merge per their Integration notes, or the surgical-repair list goes into the paper and the blocks become paper three. The algebra pass itself is DONE (log entry 11); nothing blocks either path.
2. **Second sketch — transition dynamics:** machine stock, land prices vs rents (capitalization, collateral), the κ-vs-enclosure race in real time.
3. **C4 back-of-envelope** (doomed vintage): IPEDS completions by CIP × cost of attendance × exposure shares, banded. Field-level queue structure (NY Fed by-major) belongs to the same pass.
4. **The misallocation ledger — FIRST LOOK DELIVERED 2026-08-09** (`sketch/link-sketch-block-E-misallocation.md` — Block E — plus `code/misallocation_firstlook.py`, `data/misallocation_firstlook.{csv,png}`). Commissioned as exploration, not proof. Delivered: the object defined (person-years above the undistorted benchmark, [·]₊, with the sign caution that tax wedges run the other way); four channels each with model anchor + counterfactual + attribution instrument; the unattributed envelope measured live (PWT hours to 2023: trend-continuation member 16.3M work-years/yr, Germany-parity 40.8M); channel brackets: insurance exit-margin 0.5–1M (imported, GGN), doomed study-years 1.3–2.9M/cohort-yr (our conferrals × our underemployment × labeled dials), slack 4–33M (contested dial), enclosure-forced participation EMPTY on purpose (P13 panel is the instrument — most native, least measured). ESI pipe measured at the pension+insurance aggregate $1,859B (2025); the group-health split is a BEA 6.11 pull, queued. Three decisions flagged for Stella at the end of Block E (benchmark stance; whether slack belongs; whether the envelope may appear outside the folder). A five-figure explainer page ("The Misallocation Ledger — First Look", private artifact) presents it over time: the hours century (US flat since 1980 vs Germany falling; PWT to 2023), the envelope in lifetimes (cumulative since 1980: ≈8.8M own-trend, ≈27.1M Germany-parity), the conditioned pipe (supplements share of wages 5.2%→14.3%, 1950–2025 — measured this session), the queue with the doomed-study band over time, and the assembled ledger. Remaining spec text of the original item: the past-weight object behind the blog's "millions of lifetimes" — person-years of labor supplied above an undistorted benchmark, decomposed into the model's own channels: (i) enclosure-manufactured participation (Prop 9a: rent-to-wage forcing second earners — Prediction 13's machinery is the attribution instrument); (ii) conditionality-summoned work (Prop 6ii; the giant US-specific instance: employer-tied health insurance as a work-conditioned in-kind transfer, measurable from NIPA supplements-to-wages); (iii) slack employment (species 4 — contested survey base, labeled); (iv) queue and doomed acquisition years (C3/C4, partly measured). Aggregate shadow: US hours stopped falling ~1980 while productivity doubled (the Keynes gap) — but rivals (Prescott's taxes, preferences, emulation) must be addressed per the justification burden above. Belongs with paper three's welfare spine.
5. **Companion figure pass (proposed, unqueued):** the four companion figures rewritten to the paper's readability standard — plain-sentence finding first, model vocabulary second; the wedge-targeting figure should plot the within-high-routine result its README narrates.

(Premium pass two, the κ ceiling, and the demolition-order cross-section — items 1–3 of the original list — delivered 2026-08-09; see log entries 9a, 9b, 10.)

## Repro notes

- `code/pull_premium_race.py` is self-contained and idempotent: Cell 0 downloads MORG (~2.0 GB — deliberately **not vendored** in this folder), Census A-2, and NCES 318.10; the NY Fed CSVs are fetched in-script (endpoints were mined from the interactive's JS bundle and are recorded in the script).
- With `data/morg_cache.csv` and the extract parquet present, Cells 2–7 rebuild every series and the figure **with no downloads at all**.
- `code/premium_pass_two.py` needs only the shipped parquet + `morg_premium_annual.csv` (its reproduction gate): `../venv/Scripts/python.exe code/premium_pass_two.py` from this folder — zero downloads, ~1 min.
- Environment: python3 with pandas, pyarrow, tqdm, openpyxl, matplotlib. The shared venv lives at the outer repo root (`../venv`; recreated 2026-08-09: python 3.13, pandas 3.0.5).

## Notation & merge cautions

- Numbering is provisional (A·, B·, B.0′·, C·, D·) — renumber at merge.
- Logged collisions to resolve at merge: the paper's λ_i (wage-linkage shares) vs λ(θ) (learning gradient); the superstar remark's β (reach fraction) vs β(x) (practice loading); Prop 10's D* vs D(x).
- **Numbers refresh at merge:** the C-block sketches quote pass-one premium numbers (fixed-weight peak 1.887 in 2016 → 1.837). The merge should quote pass two (adjusted peak 1.925 in 2016, seam-safe compression −0.022…−0.029, demand-side shortfall −0.037…−0.044 under the σ band) with the grid band, and may cite the identification report (σ unidentified in-window) when the text touches the race.
- Candidate verbatim sentence for the paper: *capability order comes from the anatomy of the task; survival comes from the anatomy of the wedge; neither classifies alone.*

## File map

```
the-link-revision/
├── README.md
├── STATE.md                          ← you are here; start here next session
├── checks/
│   ├── check_split.py                A0-DR, A1-FP, A2-POOL (Block A)
│   ├── check_mirror.py               B1-OCC, B2-COV amended (Block B)
│   ├── check_anatomy.py              B0'1-MEAS, B0'2-RES (Block B.0′)
│   ├── check_race.py                 C1 amended, C2, C3 bonus (Block C)
│   └── check_mu.py                   D1-CS (Block D)
├── sketch/
│   ├── link-sketch-blocks-AB.md      A (the split) + B (machine mirror, Assumption F)
│   └── link-sketch-blocks-B0-C-D.md  B.0′ (task anatomy) + C (education race) + D (anatomy of μ) + decisions
├── stress-test/
│   └── link-stress-test-1-blind-coding.md   rule, 21 cases, score, pre-registered P-S1–6
├── data/
│   ├── DATA_NOTES.md                 sources, definitions, break, validation, blocked endpoints; pass-two record
│   ├── premium_race.png              pass-one three-panel figure
│   ├── morg_premium_annual.csv       raw + fixed-weight premium, 1979–2024
│   ├── morg_cache.csv                per-year cell aggregates (rebuilds series w/o microdata)
│   ├── morg_extract_1979_2024.parquet  5.24M-row extract (pass two runs from this)
│   ├── morg_premium_pass2.csv        composition-adjusted premium: 6-member grid, median + band
│   ├── race_decomposition.csv        relative supply, demand index, counterfactual, shortfall (per σ)
│   ├── premium_race_pass2.png        pass-two three-panel figure
│   ├── supply_attainment.csv         Census A-2, % of 25+ with BA+
│   ├── ba_degrees_conferred.csv      NCES 318.10 actuals
│   ├── nyfed_underemployment.csv     the queue, monthly to Jun 2026
│   └── nyfed_unemployment.csv        companion series
├── kappa_ceiling.csv               the ceiling grid, 32 members (data item two)
│   ├── hud_fy25_fmrs.xlsx            vendored raw FMR county file (validated)
└── code/
    ├── pull_premium_race.py          self-contained, idempotent pull + build (pass one)
    └── premium_pass_two.py           composition adjustment + race decomposition (no downloads)
```
