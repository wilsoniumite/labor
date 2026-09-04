# Data item one — premium race: pull notes (2026-08-09)

## Blocked sources (reported, not substituted)
- **FRED** (fred.stlouisfed.org): HTTP 503 "upstream connect error / remote reset" on root, fredgraph.csv, and search.
- **BLS API** (api.bls.gov): returns a "Temporarily Down for Maintenance" page to POST requests.
- **BLS flat files** (download.bls.gov): HTTP 403. **BLS data viewer** (data.bls.gov): HTTP 503.
- **EPI Data Library** (epi.org/data): HTTP 403.

These may be container-egress blocks rather than outages; retry later or adjust network settings if these specific sources are wanted. None were needed: the premium series was built from the **primary microdata** instead (a step up the authority chain, not a substitution).

## Sources used (all fetched live; exact URLs in pull_premium_race.py)
1. **NBER CPS Merged Outgoing Rotation Groups**, morg79–morg24 (46 files, ~2.0 GB) — primary microdata for the premium.
2. **Census Bureau Table A-2** (historical attainment) — supply stock: % of 25+ with 4 yrs college / BA+.
3. **NCES Digest 2023 Table 318.10** — bachelor's degrees conferred (flow), actuals through 2021–22.
4. **NY Fed, The Labor Market for Recent College Graduates** — underemployment (and unemployment) rates, monthly Jan 1990–Jun 2026; CSV endpoint mined from the interactive's JS bundle.

## Definitions and sample (premium series)
- Sample: age 25–64; wage & salary earners with earnwke>0 and earnwt>0; full-time = usual hours 35–99 (hours-vary excluded).
- Education: 1979–91 from gradeat/gradecp (years completed = gradeat − 1 if not completed; BA+ ≡ 16+; HS ≡ exactly 12); 1992– from grade92 (BA+ ≡ 43–46; HS ≡ 39). SC and <HS retained in the extract.
- Raw premium: ratio of earnwt-weighted **median** earnwke, BA+ / HS. Medians sit below all era topcodes.
- Fixed-weight premium: sex × age-band (25–34 … 55–64) cells; per-cell log median gap; aggregated with fixed 1989–91 pooled earnings-weight shares; cells need n≥30 per group; weights renormalized over available cells.

## Known break
CPS education redesign in 1992 (years → credential). Raw jumps 1.660→1.750 at the break; fixed-weight 1.648→1.686. **Marked, not spliced.** Compare within regime.

## Validation
- 46/46 years, 0 read errors. n(BA+): 24.6k (1979) → 40.8k (2024); n(HS): 43.9k → 20.9k.
- 2024 medians: BA+ $1,690, HS $942 — consistent in magnitude with BLS published usual-weekly-earnings levels.
- BA+ share of FT earners 25–64: 22.9% (1980) → 47.3% (2024); Census attainment (25+): 11.0% (1970) → 38.7% (2024) — coherent (earner sample skews educated).
- NCES conferrals: 792k (1970) → 2.04M (2020), with a post-2020 downturn in actuals.
- NY Fed: recent-grad underemployment 42.9% (Jan 1990) … 41.95% (Jun 2026); persistent ~8–9 pt gap over all college graduates.

## Headline readings (for Props C2/C3)
- **Widen:** raw 1.407 (1979) → 1.806 (2000).
- **Plateau:** 3-yr raw means 1.751 (1998–2000), 1.817 (2008–10), 1.790 (2022–24).
- **Turn:** fixed-weight peaks **1.887 in 2016**, 1.837 by 2024 (−0.05). The compression leg exists but is young and modest — the live, pre-registered claim is that it continues.
- **Queue:** chronically high (38–48%) with no trend collapse; the C3-relevant object is the recent-vs-all gap and its **field-level** structure (next pass).

---

# Pass two — composition adjustment + the race decomposition (2026-08-09, later session)

Everything below runs from the shipped extract alone (`code/premium_pass_two.py`;
no downloads). Reproduction gate: the extract reproduces pass one's raw median
ratios in all 46 years (max dev 4.4e-16) before anything else runs.

## Method (Goldin–Katz proper)
- Weighted **mean log** weekly wages in **sex × potential-experience** cells
  (10 cells: 2 sexes × bands 0–9/10–19/20–29/30–39/40+; potential experience =
  age − imputed years − 6, floored at 0; imputed years <HS 10, HS 12, SC 14,
  BA+ 16 — BA+ includes advanced degrees, so 16 overstates their experience:
  stated, not corrected).
- Per-cell BA+−HS log gap, aggregated with fixed weights. Grid, per the paper's
  §7 discipline — every contestable choice a labeled axis, medians with min–max
  bands: **topcode multiplier m ∈ {1.0, 1.4, 1.5} × weight base ∈ {base8991
  (pooled 1989–91 shares, pass one's base), meanshare (GK convention: within-year
  cell shares averaged over all 46 years)}** = 6 members. The n≥30-per-group rule
  never binds (min cell-year n = 110), so no year ever drops a cell.

## Topcode facts (detected in the microdata, validated against known caps)
- Static caps: $999 (1979–88), $1,923 (1989–97), $2,884.61 (1998–2022; the 1998
  file rounds to 2884). Weighted at-cap share, BA+: 16.4% (1988), 6.0% (1997),
  **15.7% (2022)** — the unchanged 1998 cap was biting hard again; HS peaks ~2%.
- **April 2023: CPS switched to dynamic topcoding** (top earners replaced by
  their group mean). Visible here: 2023 is a hybrid year (5,087 obs still at
  exactly $2,884.61 from early months + 69 distinct mass points above), 2024 is
  fully dynamic (83 mass points; 8.1% of obs above the old cap).
- Treatment: m multiplies **at-cap observations only**; dynamic replacement
  values are already conditional means and stay untouched under every m. The
  m=1.0 members are therefore **not comparable across the 2023 seam** (truncated
  top → mean-replaced top); their 2024 "peak" is the seam, not economics. The
  m=1.4/1.5 members approximate the top-group mean throughout and cross the seam
  meaningfully — compression is quoted from them. Jensen caveat, stated: mean
  replacement sits mean-log slightly above the true top tail, so 2023–24 sit a
  hair high under m=1.0 relative to their own truth.

## Results (premium)
- Adjusted ratio (median member): 1.434 (1979) → 1.700 (1991) ‖ 1.745 (1992) →
  1.818 (2000) → **peak 1.925 in 2016** → 1.882 (2024). Log-gap readings within
  regime: widen +0.170 (1979–91), +0.041 (1992–2000); 3-yr means 0.592 (1998–2000),
  0.628 (2008–10), 0.647 (2014–16), 0.627 (2022–24).
- **Seam-safe compression** (m=1.4/1.5 members): every one peaks **2016**;
  peak→2024 = −0.022 to −0.029 log points. Pass one's shape (widen → plateau →
  young compression, peak 2016) survives the proper adjustment; the adjusted
  level sits above the raw ratio late (composition of the BA+ pool broadening
  downward) and the peak is sharper.
- Band mechanics: wide 2010–22 (the static cap bit ~16% of BA+ obs by 2022, so
  m matters), mechanically narrow 2023–24 (no static cap → m has no effect).
- 1992 redesign: raw 1.700→1.745 at the break on the adjusted median; **never
  spliced, never differenced across** — all readings within regime. Note the
  break moves BOTH the gap and relative supply (years→credential reclassifies
  SC/BA+ membership).

## The race decomposition (supply-adjusted)
- Relative supply in Katz–Murphy efficiency units from the same cells:
  CE = BA+ + ½·SC, HE = HS + <HS + ½·SC; efficiency weight per sex×exp×educ
  cell = its within-year wage relative to the year mean, averaged over all 46
  years (nominal drift cancels; m=1.4 wage member). Supply concept = **FT weekly
  earners 25–64** (the extract's reach; not economy-wide hours — labeled).
  ln(CE/HE): −0.328 (1979) → 0.054 (1992) → 0.592 (2016) → 0.789 (2024); growth
  2.94%/yr (1979–92), 1.99 (1992–2005), 2.54 (2005–16), **2.47 (2016–24)** —
  supply growth did NOT slow after 2016. (Covid 2020–21 briefly spikes the
  FT-earner composition; era growth is endpoint-based.)
- **Identification report:** the free Katz–Murphy regression is unidentified in
  this window — corr(t, ln relsupply) = 0.9975, so σ̂ comes out wrong-signed and
  absurd (−585 with the post-92 dummy, −2.3 without). Reported, not used. KM's
  1963–87 window identified σ from supply-growth fluctuation this window lacks.
- **Imposed-σ decomposition** (labeled members KM 1.41, GK 1.64, CL 2.5): demand
  index D_t = σ·gap_t + ln relsupply_t is then arithmetic. Growth by era, within
  regime (log pts/yr): 0.046–0.062 (1979–91), 0.030–0.035 (1992–2000),
  0.027–0.031 (2000–16), **0.018–0.021 (2016–24)** — the slowest era on record
  under every member, and monotone declining throughout.
- Counterfactual (anchored at the 2016 actual gap; demand continues its 1992–2016
  trend; supply follows its actual path): 2024 gap 0.669–0.677 predicted vs
  **0.633 actual → shortfall −0.037 to −0.044** log points. Reading: none of the
  post-2016 compression is supply-explained — it is a demand-side event under
  every σ member. (Anchor choice stated: granting 2016 its actual level; a
  trendline anchor would shift the shortfall by 2016's own residual.)

## Files (pass two)
- `code/premium_pass_two.py` — the pass (validation gates print as they pass).
- `data/morg_premium_pass2.csv` — 46 years × {gap median/min/max, ratio
  median/min/max, all 6 members, pass-one comparators}.
- `data/race_decomposition.csv` — gap, ln relsupply, efficiency units, and per-σ
  demand index / counterfactual / shortfall.
- `data/premium_race_pass2.png` — three panels: adjusted premium with band; the
  race after 2016 (actual vs counterfactuals); demand index (1992=0, pre-break
  faded).

---

# Data item three — the demolition-order cross-section (2026-08-09, later session)

**Claim under test** (stress-test §1, refinement logged before scoring): documentation
density D gates the LEARNING rays only; engineering rays cross by design. Occupation-level
shadows: (A) among LLM-exposed occupations, post-2022 movement ordered by D; (B) placebo —
the pre-LLM flip set selected on routine structure, NOT on D conditional on routine.

**Method** (`code/demolition_order.py`; fully offline from the companion's validated
cache, reusing its SOC→occ1990dd walk). D proxies, pre-registered with the clause each
serves: D_doc = O*NET "Documenting/Recording Information" importance (digital exhaust);
D_comp = "Working with Computers" importance (exhaust channel); D_struct = "Freedom to
Make Decisions" REVERSED by anchor test (written-procedure clause; the classic
"Structured versus Unstructured Work" item is ABSENT from O*NET 30.3 — discovered, not
assumed; "Repeating Same Tasks" rejected as circular with routine, "Degree of Automation"
as circular with the outcome; D_struct flagged most routine-adjacent). 319 occupations
merged with the companion's exposure (6 Eloundou variants), friction trends, flip rosters.

**TEST A result: the ordering is NOT yet visible — reported as a miss, not classified
away.** Within the top exposure tercile, Spearman(D, post-minus-pre trend): 4/18
member-pairs negative, median +0.05, range [−0.08, +0.23]. Consistent with the
companion's unit-5 finding that adoption shows NO exposure gradient at all yet (friction
F still binding, three years post-arrival) — the D-ordering cannot appear before the
exposure response does — but as of 2026 the anatomy's order-within-the-exposed
prediction has no cross-sectional support. It stays a dated prediction (the P-S set:
2028–2030 reads), now instrumented at scale: rerun this script when the P-S dates come due.

**TEST B result: PASSED, with a finding.** Pre-LLM flips (flip_year ≤ 2015) are selected
on routine intensity (+0.46 to +0.60 sd across the three flip rules) and NOT positively
on D — the gap conditional on routine terciles is NEGATIVE: D_doc −0.6z, D_comp −0.4z.
**Era-correctness checked:** rescored with O*NET 13.0 (June 2008 — the eve of the
2008–15 flip mass; the rule requires D on the eve of the wave): gaps essentially
unchanged (D_doc08 −0.52 to −0.59z, D_comp08 −0.29 to −0.36z), so the negative sign is
not survivorship drift in the 2025 instrument. Reading offered: the survivors of the
computing era are the RESIDUE HOLDERS — occupations that recomposed around the machine
(rule outcome PARTIAL: crossed components ceded, human residue with a machine
multiplier), which is what high computer-interaction measures. Caveats: 2008 is still
mid-wave for the 1999–2007 flips (no pre-1999 O*NET exists; DOT would be the only
earlier instrument); everything is ecological (occupation = bundle; D is defined per
component; the 21-case stress test is the component-level pilot).

**Construct overlap, stated:** corr(exposure, D_comp) = +0.78 — the Eloundou instrument
partly encodes documentation by construction; Test A conditions on exposure precisely to
step past this.

**Files:** `code/demolition_order.py`, `data/demolition_order.csv` (occupation-level
cross-section incl. 2008 members), `data/demolition_order_stats.csv` (all member-pair
stats), `data/demolition_order.png` (plain-sentence-titled, per the figure standard).

## Not done (next passes)
- Field-level entry/completions for P-C2 (IPEDS by CIP) and NY Fed by-major underemployment.
- SPM-based ceiling member if a working SPM threshold endpoint is found.
- Demolition-order re-read at the P-S dates (2028–2030): rerun `demolition_order.py`
  on refreshed friction trends; a continued Test-A null past the dates, absent a citable
  wedge, is evidence against the anatomy per the stress test's own falsifier rule.

---


---

Items two (the kappa ceiling, 2026-08-09) and four (the Swedish fork, 2026-08-26) moved on
2026-09-04: the ceiling note is `pinning/docs/kappa_ceiling_notes.md` (its grid, script and
raw HUD file ship with the paper), the Swedish fork is
`progress_and_prosperity/data_notes/swedish_fork/`.
