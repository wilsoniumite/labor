# The Long Record — spec and phased plan

**Thread:** `long-record/` (founded 2026-08-17, spun out of the-link-revision).
**Working title:** *One Schedule, Seven Centuries* (provisional).
**Mandate (Stella, 2026-08-17):** extend the model so the long-run series become
fittable — beyond "the decade timescales we have now" — and use the fit to tease
out free parameters; keep the first paper simple (`pinning.html` untouched);
write the plan sparser as it goes, with breakpoints to zoom out.
**Status:** SPEC. Phase 0 executed in the founding session. Everything past
Breakpoint A is provisional by design.

---

## 1. Why

1. **Validate §9 by fitting, not reading.** The paper's historical section
   claims the long record is one relative-productivity schedule in three
   configurations, with the classical account as the floor-bound case
   "correctly described." Right now that is a reading. A model that generates
   the seven-century wage path — floor-bound, escape, fork — turns the paper's
   boldest framing claim into an estimated, rejectable statement. §10 already
   reserves the slot: assembly (3), "the long record," specified and open.

2. **Identify the parameters that are currently free.** The floor block's
   parameters (h_e, the s₀−s_d spread, and the demographic response φ) enter
   F.4's race condition symbolically; the worked instance is invented. The
   pre-industrial record identifies exactly these, because there the ceiling
   barely moves and the floor block operates alone. Identification is
   **regime-sequential** — each era switches one block off (see §6 below) —
   which is the cleanest identification structure this model will ever get.

3. **Move belief.** Rival accounts of the industrial wage takeoff (pure
   productivity growth, institutions) do not force the wage's escape from the
   land floor and land's exit from the production function to be *one dated
   event*. This model does. That coincidence-or-not is a genuine risk the
   account could fail, per the data-purpose rule.

4. **The family needs a credibility anchor.** Paper one is theory plus two
   measurements; the sequel (transition dynamics) is forward-looking and
   speculative by construction. A backward-looking fit on public,
   centuries-deep series is the low-speculation member — the one referees can
   check against data they already trust.

## 2. The extension, minimal by construction

The static model already delivers the whole per-period equilibrium
(w, c, x*, r, s) given parameters. The extension adds **laws of motion for
three slow states** and nothing else:

1. **Population:** Ṅ/N = φ(welfare ratio − 1), one parameter for the response
   speed. Nests Bouscasse–Nakamura–Steinsson's Malthusian block, so there is a
   published benchmark for φ.
2. **The idle margin:** the Prop 3(i)→(ii) switch as a dated institutional
   path (enclosure), plus the price-side closing via N against T.
3. **Technology:** exogenous piecewise paths for (schedule slope, level ρ̄, λ).
   Technology-as-driver is the paper's standing stance; the knot budget is
   capped (≤ 6 knots across seven centuries) and pre-registered at Breakpoint
   B, because a free tech path can fit anything (§5, risk 3).

Frequency: decadal baseline (the static-equilibrium-per-period assumption is
defensible at generation scale, not annual), with an annual window around the
Black Death if the data support it — Breakpoint A decision.

**Paper one is untouched.** No change to `pinning.html` follows from anything
in this thread. If the fit succeeds, the paper's §10 assembly (3) gains a
citation; that is all.

## 3. What Phase 0 found (correction on the record)

The founding discussion proposed a headline discriminator: a **sign flip in
wage–rent comovement** at the regime switch (floor era: rents up ⇒ wages down;
machine era: rents up ⇒ wages up). The Phase-0 check
(`checks/check_longrecord_regimes.py`, ALL GREEN, 12 checks) **refutes the
naive version**, on two grounds:

- **R3 (homogeneity):** the ceiling-regime price system is homogeneous of
  degree one in the terminal rent — nominal (w, r) comovement is numeraire
  content, not a prediction. Any fit must run on deflated objects (welfare
  ratio, w/r, q) only.
- **R4 (both channels negative):** the wage's population-response is negative
  in *both* regimes — via q in the floor regime, via the task margin in the
  ceiling regime. The sign of the N-response does not discriminate.

What survives is sharper and is now the thread's spine:

- **D1 — q's determinant flips at the switch.** In the floor regime, q is
  scarcity-determined: N against T (R1). In the flat-capability limit, q is
  cost-determined by the machine recipe alone — (1−a−λρ̄)/(ℓρ̄L̄), with N and T
  absent (R2e; this is Prop 4(ii)/D.1(iii) read historically). Empirically:
  before the switch, q tracks population against usable land; after, q tracks
  the recipe and decouples from N/T conditional on technology.
  **Open algebra:** R2e is an endpoint-configuration result. The sloped
  machine era (λ > 0, land in production *and* housing) needs App A's joint
  system before D1 can be asserted along the transition path. Queued for
  Phase 2's check pass; D1 may weaken to an endpoint contrast.
- **D2 — the joint switch date.** The wage's escape from s(q) and land's exit
  from the production side are one reconfiguration, datable two ways that
  must agree (the §9 joint reading; the R5 toy shows the crossing object).
- **D3 — floor-era tightness.** Pre-industrial welfare-ratio variance should
  be explained by (N, T) alone, with an h_e magnitude consistent with the
  historical record on subsistence plots — the enclosure-era pamphlet
  literature on how much land a cottager needed is, literally, an h_e source.
  The Black Death is the identifying experiment: an exogenous N drop with
  wages and rents both measured through it.

## 4. Considerations and risks

1. **The wage-series construction debate.** Clark and Allen disagree on
   levels; Humphries–Weisdorf's annual-contract series moves the escape
   dating by decades relative to day-wage series. Treatment: fit on a *band*
   across constructions, per the house grid-of-variants practice, and report
   where conclusions are construction-dependent. The divergences are
   themselves information about the floor (day labor vs annual service is
   partly an exit-option story).
2. **BNS own the Malthusian estimation.** The novelty is never the Malthusian
   fit. It is the spine: one schedule across three regimes, the joint switch
   date, and the rent link. Phase 2 must *nest* their block (their φ as
   benchmark) and show what the land-priced floor adds beyond it — or find it
   adds nothing, which kills D3 and gets reported.
3. **A free technology path can fit anything.** The tech path has ≤ 6 knots,
   fixed before the full-spine fit (Breakpoint B), and the fit's honest moment
   count must comfortably exceed the parameter count (~10–12 new parameters
   total against seven centuries of decadal moments plus event windows).
4. **The switch must be discovered, not imposed.** The regime indicator
   (wage ≈ s(q) vs wage > s(q)) is an equilibrium outcome; the fit may not
   hard-code 1800. D2 is only a test if the two datings are estimated
   independently.
5. **Deflator discipline.** R3's verdict: nominal-comovement tests are banned
   in this thread. The cross-regime object is the welfare ratio; q and w/r
   are the auxiliary deflated objects.
6. **Scope: England first, alone.** Deepest series, one economy, no splice
   seam. Allen's cities enter only as robustness. Whether the modern end of
   the spine stays England/UK (BoE/ONS continuation) or hands over to the
   paper's US fork is a Breakpoint A decision; default is England-only spine
   with the US fork as a comparison, not a splice.
7. **Standing rules inherit in full:** primary sources; stop-and-report on
   access failure, never substitute; validate before use; sympy + numeric
   checks gate all algebra; every empirical deliverable moves belief or sizes
   impact; flat notebook-cell code style; direct critique.

## 5. Identification map (which era pins what)

| Era | What's shut off | What it identifies | Data |
|---|---|---|---|
| 1250–1750 floor-bound | ceiling barely moves | φ, h_e, s₀−s_d, land-margin path | Clark aggregates, Allen ratios, BNS population, Black Death window |
| 1750–1950 escape | population detaches (demographic transition) | schedule-slope path; **the switch date, twice** (D2) | wage escape dating vs land-share exit dating; Clark rents; BoE millennium set |
| 1950– machine era | floor otherwise-funded | σ (shelter share), λ-decline onset; terminal moments | the paper's built fork and κ series; BoE/ONS |

## 6. The plan (sparser as it goes, by design)

### Phase 0 — founding session (DONE 2026-08-17)
- [x] Regime algebra checked: `checks/check_longrecord_regimes.py` ALL GREEN
      (12), including the refutation record (§3) and verdicts D1–D3.
- [x] Source inventory with reachability statuses (§7).
- [x] This spec; thread STATE.md; memory pointer updated.

### BREAKPOINT A — before any data is pulled (Stella)
Zoom out. Answer in writing, in STATE.md:
1. Do D1–D3 justify the build, given the refutation narrowed the prize?
2. Frequency: decadal baseline + annual Black Death window — right?
3. Scope: England-only spine, US fork as comparison only — right?
4. Fit strategy: start calibration + pre-registered moment table (house-
   transparent), escalate to SMM only if moment count demands it — right?
5. Does the thread stay live, or park until the revision thread quiets?

### Phase 1 — data spine (detailed, contingent on A)
- Pull order: BoE millennium set first (one file, most series, reachable
  directly), then Clark's aggregates/rent series, then BNS replication, then
  Allen (endpoint currently blocked; alternates below).
- Validation pass per house rule, series by series: coverage, units,
  overlap-checks between sources (Clark wages vs BoE wages vs BNS input
  series), break documentation. Nothing enters the panel unvalidated.
- Build the decadal panel 1209–2016 + Black Death annual window.
- **Descriptive figures before any model:** welfare ratio, farmland
  rent/wage, land share, population, q-proxy — one sheet, seven centuries.
- Deliverable: `data/DATA_NOTES.md` in this thread's folder, house format.

### BREAKPOINT B — the eyeball test (Stella + Claude)
The raw series must show the switch pattern descriptively — the floor era's
(N, wage) opposition, the escape, land's exit — before a fit is attempted.
If the pattern is not visible raw, the model will not conjure it honestly:
re-scope or kill here. Also: freeze the canonical wage band and the tech-path
knot budget. This is the thread's main kill point.

### Phase 2 — the floor block alone (medium detail)
- Fit φ, h_e, s₀−s_d on pre-1750 data: welfare-ratio level and variance,
  the Black Death window (response size and decay), rent–wage co-movement.
- Nest BNS: their φ as benchmark; report what the land-priced floor adds.
- Check pass first: the sloped-era q-determination algebra (D1's open half)
  and the floor-block comparative statics, sympy + numeric, before fitting.
- Sanity gates: h_e against the historical plot-size literature; φ against
  BNS's band.

### BREAKPOINT C — magnitudes and novelty (Stella)
Are the fitted magnitudes sane? Does the floor block beat/extend BNS by a
margin worth a paper? Decide whether D1's transition-path version survived
its check pass. Scope Phase 3 properly only now.

### Phase 3 — the switch (sparse; shaped at C)
Add the tech path; let the binding boundary switch endogenously; estimate the
two datings of D2 independently and test agreement. Whatever D1 became after
its check pass gets its empirical run here.

### Phase 4 — the spine and the paper (sparsest)
Full-record moment table; splice decision for the modern end; decide the
vessel (own paper is the default; a §9 companion note is the fallback).
Skeleton only after C; nothing else is scoped now.

## 7. Data sources and status (probed 2026-08-17)

| Series | Primary source | Status |
|---|---|---|
| UK/England macro, 1086/1209–2016 (wages, prices, GDP, population, rents coverage TBC) | Bank of England, "A millennium of macroeconomic data for the UK" v3.1 (xlsx), research-datasets page | **Reachable directly** (HTTP 200 from this machine) |
| England decadal aggregates 1209–2008 incl. land rents, factor shares | Clark (2010) "Macroeconomic aggregates for England"; Clark (2002) farmland rentals; Clark (2004) price history — UC Davis faculty pages | **Reachable via harness fetcher only** (local curl blocked); underlying spreadsheets may need the papers' data appendices — Phase 1 to resolve |
| Malthusian estimates, population, real wages 1250–1870 | Bouscasse–Nakamura–Steinsson (2025 QJE) replication archive | NBER reachable via harness fetcher (curl blocked); QJE/Dataverse archive to locate in Phase 1 |
| European city wages, prices, welfare ratios 1264–1913 | Allen (2001) spreadsheets, robert-c-allen.net | **BLOCKED (HTTP 403)** from both routes. Alternates to try at Phase 1, in order: the old Nuffield mirror, IISH labour-prices collection, gpih.ucdavis.edu mirrors. Reported per house rule, not substituted. |
| Population 1541–1871 | Wrigley–Schofield, incorporated in the BoE set | via BoE (confirm at validation) |
| Modern terminal moments (fork, κ) | in-repo, the-link-revision `data/` | **Built** (their checked records stand) |

## 8. Decisions pending (Stella's, at Breakpoint A)

Frequency; scope (England-only vs splice); fit strategy; live-or-parked. Plus
one standing question inherited from the founding discussion: whether this
thread is the sequel §12 promises or a separate paper beside it (default:
separate; the sequel keeps transition dynamics).

## 9. Relation to the other threads

- `the-link-revision/`: parent. Feeds this thread the model, the checked
  worked instance, and the modern terminal moments. Takes nothing back except
  (eventually) a citation at §10 assembly (3).
- `companion/`: none for now; its occupation-level machinery is orthogonal.
- Session protocol: one unit per session; checks gate absolutely;
  verify-lists as veto windows; this file plus STATE.md are canonical.
