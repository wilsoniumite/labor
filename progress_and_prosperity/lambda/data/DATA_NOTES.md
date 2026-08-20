# Data notes — λ Family A (unit 2, built 2026-08-20)

## Sources (all live public BEA static files, pulled by `code/pull_family_a.py`)

- `AllTablesIO.zip` — make-use framework: Make and Use (before/after
  redefinitions, producers' prices, PRO) 1997–2023 Summary; **CxI direct
  requirements** (after redefinitions, incl. V001/V002/V003 coefficient rows).
- `AllTablesSUP.zip` — SUT framework + the published **IxC total
  requirements** 1997–2023 Summary (the λ̂ workhorse).
- `GrossOutput.xlsx`, `ValueAdded.xlsx` — GDP-by-Industry cross-check members.
- Route (this machine): local curl fails (proxy code 000); plain requests
  fails (TLS interception); `truststore.inject_into_ssl()` fixes requests —
  house precedent. PowerShell also passes. Cache dir is .gitignored; the pull
  script recreates it; the derived CSV is committed and is what the checks
  gate against.

## Construction (verified, not assumed)

Basis: make-use framework, after redefinitions, producers' prices, summary
level (71 industries × 73 commodities incl. Used/Other).

- v_w = DR row V001; v_nw = V002 + V003 (per $ industry output).
- W = Make/q market shares (all 73 commodities); B = DR commodity rows.
- **Reconstruction gate (C4):** W(I − BW)⁻¹ reproduces the published IxC_TR
  to max|err| ≈ 1.3e-04 (DR rounding) every year. The SUT-framework
  Supply/Use tables do NOT reproduce it (miss ~0.3) — the published TR's
  basis is the MU after-redef framework; recorded via
  `code/diag_reconstruction.py`.
- λ̂_tot = v_w′ · TR_pub · f (import-comparable total requirements).
- λ̂_dom = v_w′ · W(I − diag(φ)BW)⁻¹ · f, φ_c = q_c/(q_c + M_c),
  M_c = −Use[c, F050] — proportional import purge; per $1 of domestically
  produced machinery final output. λ̂_domp adds the final-layer purge
  (per $1 purchased). Exact identity check (C8a): full VA resolution of
  every commodity through the published TR ≡ 1 (max dev 1.4e-06).
- f = final uses of member commodities (all F-columns except F030
  inventories and F050 imports), clipped ≥ 0, normalized.
- Sets (summary level): narrow {333, 334, 335}; medium + {511, 514, 5415}
  (514 is the summary code for data processing/internet services); broad
  + {532RL}. Repair (811) is not separable at summary level — 2017-detail
  check only, queued.

## Checks

`checks/check_family_a.py` — ALL GREEN (11) on 2026-08-20: panel complete;
unit-cost identity ≤ 1.1e-06; v_w ∈ [0,1); C4 ≤ 1.3e-04; ρ(BW) ≤ 0.52 < 1
(net reproduction, the model's a < 1, empirically); member ordering
dom ≤ tot; exact VA resolution; domestic resolution ∈ [0.572, 0.996]
(leakage = import content); grid codes present; weights well-defined.

## Deferred, recorded (not silently dropped)

- Self-employment imputation axis (spec): not in v1 grid.
- Import-matrix (non-proportional) purge: BEA import matrices exist as a
  separate static file; queued as a grid extension.
- Before-redefinitions variant: files in hand (AllTablesIO), queued.
- 2017-detail run (repair 811, finer software split): queued.
- GDPxInd cross-check is report-only in v1 (C7); tighten if promoted.

## Century arc (unit 3, built 2026-08-20)

Sources: BEA historical benchmark packages (harvested via the in-app browser
from `bea.gov/industry/historical-benchmark-input-output-tables`, pulled by
`code/pull_century.py`): 85-order Excel vintages 1947/1958/1963/1967/1972/
1977, two-digit text vintages 1982 (`ndn0125`), 1987 (`ndn0019`), 1992
(`ndn0180`); plus `AllTablesHIST.zip` (historical GDP-by-Industry 1947–1997,
NAICS-basis retrospective) for the GDP anchor and the 1987+ compensation
cross-check. BEA's own caveat is carried on every output: the historical
benchmarks "should not be used as a time series" — used as benchmark POINTS,
splice stated.

Construction (`code/compute_century.py`), self-identifying by design:
industries = numeric prefix 1–85; the VA block is the greedy special-row
subset matching revised GDP (scales {1e-3, 1e-1, 1, 1e3} tried — 1982 ships
in $100K units; scale cancels everywhere but the anchor); compensation =
the dominant VA-block row (share ∈ [0.45, 0.72]); FD columns = positive-
total specials, cell-clip rule; published total requirements used for every
vintage (in-file, the 1958 TR workbook, 1982's trailing ×1e7 fields, 1987
TBL5, 1992 IXCTR.TXT). Machine set: SIC 85-order 43–58; "+i" adds 62
(instruments, NAICS-334 ancestry). Software not separable pre-NAICS —
century set is narrow-only, stated.

Results discipline: compensation λ̂ points 1967–1992 (six, incl. both W1b
anchors); **1947/1958/1963 carry no compensation split at the 85-level and
are dropped from λ̂, not imputed** — their parses are validated by the
resolution identity (res_va 0.955–0.994). External verification where
possible: comp row vs HIST components, dev 0.9% (1987) and 0.7% (1992).
Splice 1992 SIC → 1997 NAICS narrow: ratio link 0.9204, the classification-
break step, reported on the figure. The unit-2 algebra does NOT reproduce
the SIC-era two-digit published TRs (recon_err 0.19–0.25 — old transfer/
secondary-product conventions); published TR is the source there,
reconstruction recorded report-only.

Checks: `checks/check_century.py` — ALL GREEN (10) on 2026-08-20.

Queued extensions, recorded: pre-1967 compensation via NIPA 6.2-style
industry compensation bridged to 85-order sets (recovers 1947/58/63 points
if wanted); hours layer for the century arc (best-effort, unit 5 scope).

## Family B — the world referee (unit 4, built 2026-08-20)

Sources (GGDC DataverseNL, public GET; URL↔content mapping browser-harvested;
pulled by `code/pull_family_b.py`): WIOD 2016 release (WIOTs in Stata,
639MB, per-year wide dta; SEA16 with COMP, LAB, H_EMPE), WIOD 2013 release
(`wiot_full.dta`, 724MB long panel; SEA13 July-2014 with COMP, LAB, H_EMP).
**Long-run WIOD DOWNGRADED, recorded:** its SEA carries only GO/II/VA/EXP —
no labor variables — so no world λ̂ before 1995 from WIOD; the partial LR
WIOT download was killed and the member dropped. **ICIO parked:** the file
host serves small files to the harness fetcher but 403s the data zips to
every scriptable client (fetcher, curl, PowerShell, requests) — extension
lives behind a documented manual vendored download (five clicks).

Construction (`code/compute_family_b.py`): global Leontief inverse per year
(1435 and 2464 country-industries); currency handled by shares —
(COMP/GO)_SEA is dimensionless, hours use WIOT USD output as denominator;
zero-GO sectors dropped from the system (the exact identity holds only on
GO > 0; dropped flow ≤ $15.3B, reported). Grid: {COMP, LAB (self-employment
adjustment — that deferred axis now live on the world leg)} × {ROW=0 lower
bound, ROW=mean} × sector sets (ISIC4 C26/C27/C28 narrow, +J62_J63 medium;
ISIC3 items 13/14 for 2013 — mapping verified via USA machinery GO, WIOT vs
SEA, dev 0.000). Views: world $1 and US-purchases $1, the latter split into
US vs foreign labor content (the offshoring decomposition). FD excludes the
inventory category (detected by sign), cell-clip ≥ 0. H_rel = hours embodied
× world average hourly compensation (USD) — the amended criteria's quantity
leg — with w̄_rel = λ̂/H_rel derivable at the read.

Discipline items: exact global identity ≤ 8e-15 every kept year (the closed
world table makes it exact — no import leakage exists at world level);
SEA13's labor layer thins to 24% output coverage in 2010–11 → those two
years are EXCLUDED and flagged, not kept; vintage overlap 2000–2009 agrees
to 0.019 max deviation (report-only — classifications differ). Kept
coverage ≥ 0.84.

Checks: `checks/check_family_b.py` — ALL GREEN (11) on 2026-08-20.

## US hours + rent layer (unit 5, built 2026-08-20)

Hours (H_rel for W3/W1b's NAICS segment): r_vec = TR·f from the unit-2
verified construction; hours applied as a BLOCK-level row vector (28 blocks
bridging BEA-71 ↔ ISIC-56; no re-inversion; bridge coverage of requirement
mass = 1.0000 exactly, checked). Levels 2000–2014 from WIOD16 SEA USA
H_EMPE; tails 1997–99 and 2015–23 extended per block by the BEA–BLS KLEMS
hours index (2017=100), compensation-weighted within block — mechanical,
continuous at the seams (max |yoy| 11.4%), labeled. H_rel = H × w̄_US
(economy average hourly compensation from unit-2 levels / block hours —
$19.4→$49.0/hr over the window, which pins the units). w̄_rel = λ̂/H_rel;
the decomposition λ̂ = H_rel × w̄_rel is exact (2.2e-16). **W1b's H leg
covers the NAICS segment (1997–2023) only** — no SIC-era hours at these
levels; stated for the read.

Rent layer (published values only): Stansbury–Summers BPEA 2020 replication
(Brookings-hosted, public, no wall — a legitimate member): industry panel
1987–2016 with implied labor rents; ρ_i = implabrents/compensation per
industry, mapped by name onto BEA codes (machinery 1:1: Dur_machinery→333,
Dur_computer→334, Dur_electrical→335, Computer_serv→5415/514; other
manufacturing mapped; unmapped industries carry the corporate-business
aggregate ratio). λ̂_purged = Σ(1−ρ_i)·v_w_i·r_vec_i, populated exactly
1997–2016 (max purge 0.086). Machinery-direct ρ ∈ [0.104, 0.142];
aggregate ρ ∈ [0.087, 0.123] — trends UNREAD. A&R 2026 §3.3 level anchor
recorded for the read: rents ≈35% central [19–44.5%] on *automated jobs*
(QJE 141(2); a displaced-job level, not an industry series — magnitude
benchmark only).

Checks: `checks/check_us_hours_rent.py` — ALL GREEN (9) on 2026-08-20.

## Read status

**UNREAD.** The series and figure exist; the committed read criteria are
applied at unit 4 (the gate read), after Family B. No verdict is stated in
this note, by design.
