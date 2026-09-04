# STATE — resume point for the next session

**Project:** "Three Taxes" — candidate standalone paper on the fiscal
architecture as labor's share falls: the three-tier taxonomy (scarcity /
gate / corrective), the convergence theorems (the gate tax retires into
rent collection as λ falls), the 100% ceiling, the grandfathering dial,
and the circular-flow discipline. Grown from P1 Appendix C's one
paragraph ("The mix on the way down").
**Collaboration:** same contract as the sibling threads — working format,
sequencing, and drafting decisions delegated to Claude; checks gate
absolutely; direct critique preferred over validation; her voice pass
re-voices any prose that enters a paper.
**State as of:** 2026-09-02, evening (the practical-design unit built; founded 2026-08-27).

## Where things stand

**2026-09-02 (evening): THE PRACTICAL-DESIGN UNIT IS BUILT — VETO WINDOW
HERE.** Her session arc: "what fills the D-F/D-Q gap" (answered in
conversation: the gross capital stack, housing rents first, depreciation
and retention reflux, fiscal recycling, the border; the gap as a net
bilateral flow) → "can we compute a VAT rate to hold a 60/40 split" →
her clarification (60/40 = consuming vs adapting/developing, away from
the limit, with a healthy LVT that cannot carry the floor) → "it's
probably another paper, let's have a folder for it" + six practical
questions → the shock list (LVT revaluation, property freeze, bank
collateral) → the global bond-yield rise. FOLDER DECISION: this thread
already existed as that paper, so the unit was built HERE; her call if
she wants it split out. Deliverables, all uncommitted:
- `docs/design_memo_2026-09-02.md` — the design: §1 scarcity capture
  (LVT at 98% = T3's error buffer, not an owner incentive; her 5-year
  lag is an assessment smoother, not a stock shock absorber, and turns
  the effective rate to 1.22 after a −20% rent step — keep it as a floor
  only; a rated table of eleven other scarcities in three groups);
  §2 source taxes (the use split is a saving constraint: t = 1 − 0.4/(sπ);
  the cash-flow tax as the reinvest-don't-consume enforcer; menu rated;
  no wealth/interest tax); §3 VAT design and rate (residual; 39%
  tax-exclusive under the split today, retiring at wage share 0.37/0.28);
  §4 the schedule over the path, both closures bracketing; §5 removal
  order in stages (structures tax and CIT conversion first; payroll and
  means-tested cash next; wage income tax at 0.45; the VAT itself at
  0.37; keep excises, public goods, in-kind health); §6 fill order
  (floor → G_c → κ-ceiling public investment → buffer fund → dividend
  above floor) and the SWF's three cases (domestic redundant; foreign
  scarcity fragile on the host's first claim; smoothing/windfall
  conversion is the real case); §7 shocks: the announcement date SIZED
  (land residual $23.5T = 0.76×GDP; mortgages $13.6T; aggregate LTV
  26% → 48%; phase-in leaves 86% of the stock loss at 10y; increment-
  only grandfathering caps it at 40%) with an eight-item rated toolkit
  (grandfather r₀; route the loss through the state's balance sheet via
  statutory write-down + recapitalization rather than defaults; deferral
  liens; sequencing; central bank; compensation logic; local finance)
  and ten other shocks; §8 sovereign yields (US legs FRED-verified:
  DGS30 5.25% on 2026-08-31 vs 2.06% 2021 mean; the model tracks through
  the fiscal-base channel — P1's borrowed channel, 19% of transfers —
  and consistently-but-not-quantitatively through ρ under a buildout;
  plan: base migration as term-premium policy, rent-backed debt — the
  capitalized flow is 63% of federal debt — explicit transition funding,
  monetary sequencing, the buffer fund); §9 decisions + the unverified
  list (every precedent named is memory, to live-verify).
- `code/fiscal_napkin.py` → `data/aggregates_2025.csv`,
  `vat_residual.csv`, `split_schedule.csv`, `lvt_shock.csv` (live FRED
  through link-repo's gated machinery; the paper's own rT/P_s inputs).
- `checks/check_split.py` ALL GREEN (12): S1–S2 the split identities,
  S3 the VAT residual identity (any closure), S4 the retirement
  threshold, S5 a schedule row, S6 the corner relabel of a VAT on
  fixed-supply land services at τ_R = 1, S7 the announcement-date price
  paths (immediate, increment-only closed form, the γ/δ dial within
  0.03), S8 the lagged-assessment overshoot.
- `SKETCH.md` §11 addenda: T10 (use split → source tier), T10b (the
  wage-share clock on which the gate retires), T11 (announcement date +
  shocks + sovereign yields); section-plan amendment; honesty-ledger
  additions (cash-flow-tax family and the Kaldor closure are cited, not
  claimed; no saving function in the model — the closure is imported).
- NOT done, deliberately: no commit (none requested); no paper prose;
  no citation live-verification (memo §9 lists what is memory); the
  memory pointer updated to mark this thread ACTIVE.
- **ADDENDUM, same evening — T10c, the split as a rule** (her: "40/60
  is arbitrary ... even in the limit the dynamic extension keeps capex
  alive ... how much adaptability vs sit and enjoy ... read off
  depreciation? off the market? what am I missing? keep sketching").
  Memo §4b + SKETCH T10c + `code/split_determinants.py` →
  `data/split_determinants_{replacement,market,buildlag}.csv`;
  `checks/check_split.py` now 17 GREEN (S9 build-lag markup with her
  40 reproduced at g=5%, J=5; S10 pipeline stock; S11 the limit split
  1−α → 0 for σ<1; S12 the conversion golden rule). THE FINDING: gross
  investment flat at 21–23% of GDP every decade since 1950 while CFC
  rose 11.1% → 16.5%, so net fell 11% → 5% and public net 3% → 0.8% —
  the κ-ceiling conversion line is the starved one; her 40/60 is 1950s
  net accumulation on a higher floor plus a pipeline. THE MARKET READ:
  TIPS real 2.44% (2021: −0.91%), term premium 0.88 (at its 1990–
  mean), breakevens 2.35 (= 2021), Baa 1.59 (low), VIX 16 — the market
  prices ρ, not risk; saving short of investment demand at the old
  price = the split asking to move (ties Q8 to Q4; the TIPS yield is
  the rule's observable). Trajectory: a hump 21 → 40 → replacement-only
  (value share → 1−α → 0). Her missing-list (ten items) and the four-
  piece rule are in §4b; the shock ledger on P1's dynamics engine is
  specified, not run (her call whose unit it is).
- **ADDENDUM 2, same evening — the lag design and the valuation
  mechanism, HER CLAIMS CHECKED** (her: an up-lag for prospecting,
  scaled by preregistration to ten years; a two-year down-lag so "you
  can't get a revaluation loophole"; abandonment "fine, the state takes
  ownership for the period"; then "state run universal auction for
  land, anonymous buyers" and "government run land bureau ... catch
  collusion by buying undervalued land"; "please do actually check me
  on all I say"). `checks/check_split.py` now 26 GREEN (S13–S17, a
  partial-adjustment assessment simulation + sympy). VERDICTS:
  (1) prospecting is a real hole in T3's static ceiling, but a general
  up-lag is the wrong reward — every holder keeps 17% of rent at g=2%,
  L=10 (exact (1+g)/(1+gL)); registered discovery windows on verified
  increments instead; (2) the 2-year down-lag does NOT close the
  sawtooth under a 10-year up-lag (a real 2-year dip pays +1.75 years
  of rent; needs ~half the up-lag; symmetric (2,2) closes it), and the
  fake dip pays under ANY lags — only occupant-invariant valuation
  closes it; (3) abandonment is fine ONLY as ground-lease conversion
  with the structure retained + prompt re-letting + lender-neutral —
  else the β hold-up returns and the put never bites on built parcels;
  (4) her auction + bureau = the two-option bracket (owner's put caps
  the tax at r; the state's AUTOMATIC take-call at A(1−b) floors
  realized rent and kills self-reporting): effective rate ∈
  [0.98(1−b), 1]; auctions as a rolling anonymous SAMPLE for
  identification, not universal coverage; the occupant's match right
  and its bid-chilling cost is the open design question. Memo §1.1
  rewritten; SKETCH T12 added; two decisions added to the memo's §9.
  Follow-up (her: "title gives no rights to manage usage ... holders
  have only one incentive: set the highest rent that doesn't cause a
  user to flee, right?"): the incentive is T3(b)–(c)'s hold-up from the
  holder's side (reservation value = next-best bid + sunk stake), so
  the design removes pricing from holders entirely; title becomes a 2%
  annuity with no function; usage management migrates to user (lease
  design, β = 0), auction (bundle bids), and state (covenants, zoning).
  Paragraph added to memo §1.1.
- **ADDENDUM 3, same evening — SKETCH v1 WRITTEN** (her: "sketch it up
  in a big md file ... if you disagree with some of my ideas or don't
  think they should go in the paper, drop them ... mostly prose for the
  mechanisms and a structure for the paper ... this will come after the
  dynamics paper ... keep it light on those unknowns").
  `SKETCH_v1.md` is now THE paper sketch (v0 header points to it; v0
  stays as the T1–T12 block ledger; the memo stays as the Q&A record).
  Structure: §0 one page (claim, the system in five sentences, dropped,
  deferred); §1 intro; §2 model + resolution ledger; §3 tier 1 (ceiling
  3.1; valuation mechanism 3.2 — options not lags, sample auctions,
  discovery licence, who sets rent/usage; commons inventory 3.3; what
  tier 1 can't reach 3.4); §4 the gate (legs, design, residual rate,
  swap-first, the clock); §5 the source tier as the use-split enforcer
  (cash-flow base, both closures, what not to tax); §6 the split rule
  (four pieces, the CFC finding, the market read, the hump); §7
  convergence + the assembled clock table; §8 transition I (replacement
  map, allocation rule, the fund sized by its case); §9 transition II
  (announcement date static half, the shock list, the sovereign-yield
  reading); §10 public goods / Pigou / objections / falsifiers; §§11–15
  appendices plan, DROPPED (general lag; 2:1 rule; 40/60 as a number;
  foreign-scarcity fund as pillar; universal auctions; transitional-rent
  capture; private title's function; interest as a base), DEFERRED to
  the dynamics paper (announcement theorem + price paths; build-lag and
  pipeline identities; horizon terminality + time-inconsistency;
  transitional rents; shock experiments; interest channel), verify
  ledger, her decisions (8). Sequencing recorded: this paper AFTER the
  dynamics paper, consuming its results via the §1 imports paragraph.

**2026-08-27: THREAD FOUNDED; SKETCH v0 + CHECKS DELIVERED.**
- `SKETCH.md` — the paper sketch: claim, objects (φ_w/φ_r resolution
  shares), blocks T1–T9 + HGT corollary, the new-vs-already-claimed
  honesty ledger, section plan, empirical assemblies, literature ledger
  with verify status, objections, decisions pending.
- `checks/check_three_taxes.py` — ALL GREEN (35): resolution ledger
  closes and shares derived from the closure; tier-2 leg split + corner
  equivalence; convergence rate and DW monotonicity on both factors
  (with P1's measured instances 0.32 / 0.08 reproduced); circular-flow
  fixed point R₀/(1−φ_r·τ) tied to viability, transfer invariance,
  κ(g) = κ₀g/((1−h)+hg) with its three limits; grandfathering dial γ/δ;
  hold-up FOC e*(β); withholding identity (T−A/2)²/B; A–K levy share
  t/(1+t). Run: `../venv/Scripts/python.exe checks/check_three_taxes.py`
  (from three-taxes/).
- Provenance: the 2026-08-27 conversation (circular flow → conservation →
  stock/dial → state-landlord ceiling → her three-way split → the gate
  tax re-derived). Record the conversation arc in the paper's AI-use
  note at drafting, per program practice.
- NOT done, deliberately: no commit (none requested); no PLAN.md edit
  (program placement is hers — see decisions); no draft prose; no
  citation live-verification (nothing enters a draft before it).

**2026-09-02: HER CONCRETE SYSTEM, ASSESSED (conversation only; nothing
drafted, nothing in the paper).** Stella's proposal for the fiscal system
away from the limit, as she stated it: (1) a land tax near 100%, proceeds
earmarked to a UBI; (2) a VAT funding all other government spending under
a 2:1 rule — for each required dollar of spending raise two, one to
government and one to the UBI; (3) sovereign-wealth-fund nuances and
Pigouvian nuances deferred ("later"). Read against v5
(`Downloads/v5 (1).tex`, 2026-09-01) and this sketch:
- Leg (1) is prop:welfare's pair; v5 App C already states that production
  efficiency and the Δ=0 cancellation hold in the sloped regime. "Near"
  rather than "at" 100% = T3's error buffer (assessment above true rent
  taxes the occupant's contribution and idles land) and keeps a positive
  land price so transactions keep revealing r. T4's announcement-date levy
  on the stock is where the SWF nuance lives (grandfathering dial γ/δ;
  bank exposure = SEB material).
- Leg (2) is T6's gate tax. Two interactions flagged: (a) with τ_R≈1 the
  VAT's domestic-site-rent leg is a relabel, not new revenue (fixed
  supply → borne by rent → the land-tax base shrinks one-for-one), so a
  rule written in gross VAT dollars leaks roughly R/PCE ≈ 5–8% of the VAT
  take out of the UBI line into G's financing — write the rule net, and
  exempt residential site rent where it is visible; the VAT's genuinely
  new rent leg is non-site and foreign rents, as T6 has it. (b) The wage
  leg is a participation wedge (home production and exit escape the
  gate) — App C's incidence dial, decaying with λ per T7.
- The 2:1 rule stripped of its earmarks (money is fungible): τ_R≈1;
  UBI = R + G; VAT revenue = 2G; no other taxes. Clean reading: a person's
  net VAT payment is t(c_i − C̄/2), break-even at half of mean
  consumption, so nobody below that ever net-pays for G. Costs: it pegs
  the dividend to G rather than to P_s (the floor is reached by accident;
  a war doubles the dividend), and it doubles the VAT rate needed for G,
  with the wage-leg deadweight ~quadratic in the rate. Alternative inside
  existing objects: peg the UBI to P_s, fill κ of it from rent, let the
  VAT cover (1−κ)·P_s·N + G; then D = φ_C(1−κ)² is the residual index.
- Napkin (live FRED annual 2025; CPI average from 11 months, the
  Oct-2025 gap): G purchases 5.3T (17% GDP), social benefits 3.6T, PCE
  21.0T, housing PCE 3.3T, pop 341.9m; P_s single 16.2k / pc4 8.2k; R
  1.0–1.7T (grid low/high members, 3.0–4.8k per head). If the UBI
  replaces all existing benefits: VAT 10.6T = 34% GDP = 50% of PCE
  tax-inclusive (≈100% tax-exclusive; 60%/149% with housing exempt);
  UBI per head 18.4–20.3k = 1.1–1.25 single bundles. If existing benefits
  are kept inside G: VAT 17.8T = 58% GDP = 85% of PCE — infeasible. The
  right comparator for the 50% wedge is today's total wedge on the
  work–exit margin (income + payroll + VAT), not today's VAT: the
  "Nordic gate scale" assembly (§6). Script: session scratchpad
  `napkin.py`, not vendored.
- Pigou: T9 — corrective revenue must sit outside the 2:1 arithmetic;
  counting it toward "required dollars" makes the VAT rise as the
  corrective tax succeeds, a fiscal stake in the harm.
- Placement: a concrete instance of tiers 1–2, i.e. the worked design for
  the sketch's §7 (gate tax) and the Nordic-scale assembly. Not in P1.

## Decisions pending (hers)

- [ ] **Folder (2026-09-02):** the practical design lives here; split it
      out into its own folder, or keep the one paper.
- [ ] **The closure (2026-09-02):** full reinvestment vs the observed
      half — recommend carrying both as a bracket.
- [ ] **The split target (2026-09-02):** 40% gross (2× today) or 40% net
      (10× today's net investment); changes the paper.
- [ ] **98% + the lag (2026-09-02):** lag as an assessment floor only?
- [ ] **Announcement-date design (2026-09-02):** increment-only
      grandfathering (40% stock loss) vs full capture routed through the
      state's balance sheet (write-down + recapitalization), or both.
- [ ] **The fund's foreign leg (2026-09-02):** keep as a ceiling hedge or
      drop on the host-first-claim argument.
- [ ] **Which shocks get theorems (2026-09-02):** price paths are checked;
      bank pass-through and rent-backed debt are prose until she rules.
- [ ] **Title** (candidates at SKETCH.md head).
- [ ] **Dividend peg (2026-09-02):** her 2:1 rule pegs the UBI to G;
      the sketch's fill-order pegs it to P_s via κ. Which, and does the
      UBI replace existing benefits (the napkin's feasibility hinge).
- [ ] **Program placement:** standalone paper consumed by P2/P5 (the
      λ-series precedent) vs. P2's theory spine. P2's sketch already
      reserves "rent base first, VAT bridge, the λC(1−κ)² deadweight
      index" + the A–K levy reading; P5 reserves the loop-on-ramp and
      the political economy. Decide at delivery per program practice;
      then PLAN.md's papers section gets its line.
- [ ] Whether T3 (ceiling), T4 (dial), T5 (loop) feed the SEB talk's
      bank/κ material.
- [ ] The λ_C ↔ φ_w identification (SKETCH §6) — gating for T7(ii)'s
      measured version; needs App C's 0.72 construction traced.

## Next actions (after her read)

0. Her read of `docs/design_memo_2026-09-02.md` and the seven 2026-09-02
   decisions above; then live-verify the memo's precedent list (§9)
   before any of it becomes prose; pull LTV-by-metro data if the bank
   tail is to be sized rather than illustrated; extend the κ path from
   q rather than a stylized grid.
1. Her verdicts on the pending decisions above.
2. If green-lit toward drafting: live-verify the §7 ledger (D–M 1971,
   Mirrlees Review, A–K 1987, Fischer 1980, C–G 2018, ground-lease
   sources) before any prose cites them.
3. λ_C reconciliation against App C's data note.
4. Empirical assemblies per SKETCH §6 (φ_w rides the λ-series; h and κ
   ride existing machinery).

## Cross-thread map

- P1 (`the-link-revision/paper/pinning.html`): stays untouched — App C
  is the seed and remains the paper's own statement.
- P2/P5 (`progress_and_prosperity/PLAN.md` §The papers): overlapping
  reservations listed above; this thread must not silently absorb them.
- λ-series (`progress_and_prosperity`, gate PASSED 2026-08-20): φ_w is
  the same estimand — one series, two papers.
- SEB talk (the-link-revision STATE log 25): T4's dial is the bank
  slide's mechanism, formalized.
