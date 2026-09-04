# Three Taxes — paper sketch (v0)

> **Superseded as the paper sketch by `SKETCH_v1.md` (2026-09-02).** This
> file remains the theory ledger (blocks T1–T12 with their check IDs) that
> v1 consolidates with `docs/design_memo_2026-09-02.md`; v1 carries the
> paper structure, the prose mechanisms, the dropped list, and the
> dynamics-paper deferrals. Edit v1, cite this for the block-level record.

**Working title candidates** (hers to pick; none is settled):
"Three Taxes: The Fiscal System as Labor's Share Falls" ·
"The Tax System at the Limit" ·
"Scarcity, Consumption, Correction".

**Status:** v0 sketch, 2026-08-27. Algebra checked: `checks/check_three_taxes.py`
ALL GREEN (35). Nothing committed, nothing drafted, no PLAN.md change —
program placement is Stella's call (see §10).

**Provenance:** born from the 2026-08-27 conversation. Arc: Stella's
circular-flow question (rent-funded UBI as a self-supporting base) →
conservation discipline → stock/flow and the grandfathering dial → the
state-as-landlord ceiling → her three-way tax split → the consumption tax
re-derived as the workhorse. Her scoping words: pinning is "too mature for
an addition like this ... probably a paper of its own."

---

## 1. The claim

Every unit of final spending resolves, through the machine recursion, into
exactly two kinds of claim: wage claims and scarcity claims. A tax system
is a choice of where to stand in that circuit. Three stands are coherent:
at the scarcity source (rent collection: land plus the un-parceled
commons — no margin moved, rate up to a definitional ceiling of 100%), at
the consumption gate (a destination-based uniform tax — one margin moved,
and only on the wage-resolving share of the flow), and athwart a targeted
externality (corrective taxes — the margin moved on purpose). The paper's
theorems: the gate tax's distorting share is φ_w = λρ\*/(1−a), so
automation retires tier 2 into tier 1 at a computable rate — the optimal
system has a terminal state and the economy is walking toward it; the
scarcity tier's 100% ceiling is definitional, not administrative (above
it every instrument switches base onto the occupant's own contribution);
capitalization makes the stock and the flow one object, so the
stock-redistribution dial is grandfathering inside τ ≤ 1, never τ > 1;
and the rent-funded transfer's circular flow is real but conserving — it
inflates gross flows and both sides of κ, and cannot pass the land-per-head
ceiling. P1 (Appendix C) states the architecture in one paragraph; this
paper is that paragraph grown into a fiscal system with its limit theorems.

## 2. Objects

Inherited from P1 unchanged: the recursion c = ac + λw + ℓr; the closure
w = ρ\*ℓr/(1−a−λρ\*); viability 1−a−λρ\* > 0; κ = rT/(N·P_s); the pair
(rent tax, uniform dividend); s(q), q_enc; r(z) parcels.

New, reused throughout (definitions earn reuse):
- **φ_w = λρ\*/(1−a)**, **φ_r = 1−φ_w**: the wage- and rent-resolution
  shares of one unit of final price (T1). Viability pins φ_r ∈ (0,1);
  worked instance (0.5, 0.1, 3, 0.2, 1) gives (φ_w, φ_r) = (0.6, 0.4).
- **h**: the rent content of the floor bundle P_s (first cut: FMR/bundle
  ≈ 0.62 from P1's ceiling grid inputs).
- Section-local: t (gate-tax rate), τ (rent-tax rate), g (rent-price
  scaling factor in the κ formula), γ/δ (rent growth / discount — the
  dial; distinct from g), β (revaluation-capture share in the hold-up
  block), m_p/m_r (basket rent contents).

## 3. The blocks

**T1 — The resolution ledger.** Unwinding the recursion, the total wage
and rent contents of one unit's price are λw/(1−a) and ℓr/(1−a); they sum
to c exactly (the ledger closes). Shares φ_w, φ_r as above; corner
(λ→0): (0, 1). CHECKED (7).

**T2 — The taxonomy.** Tier 1 stands at the source; tier 2 at the gate;
tier 3 athwart a named externality. The tempting fourth stand — "tax the
user of land" — decomposes on incidence and vanishes: the land-conditioned
part is borne by rent (bidders subtract it; with the state as landlord it
cannibalizes tier 1 one-for-one), and the activity-conditioned part is
ordinary factor taxation with an origin base (border games included).
Diamond–Mirrlees closes the door formally: optimal systems leave
intermediate inputs untaxed — and tier 1's 100% rent capture supplies
exactly the no-pure-profits precondition D–M needs. The architecture is
self-reinforcing. [D–M 1971 to live-verify.]

**T3 — Tier 1's ceiling is definitional.** Market rent is the next-best
bid for the bare site: use-independent, occupant-invariant. In the
competitive closure (free entry, zero pure profit) there is *nothing*
above 100% of r(z) to collect — site heterogeneity is already inside the
base (r(z) is the Ricardian differential), person heterogeneity resolves
to wages. Three ways to try anyway, each checked:
(a) *uniform price above clearing* — withholding monopoly; gain over the
competitive bill = (T−A/2)²/B in the linear instance, positive only by
idling land, and growing with abundance: manufacturing scarcity pays most
where natural scarcity is mildest. CHECKED (3).
(b) *discriminatory "value of use" pricing* — a marginal tax approaching
100% on what the occupant adds.
(c) *the dynamic version* — revaluation captures β of tenant improvements;
e\*(β) = (αA(1−β))^{1/(1−α)}, strictly falling in β; β = 0 recovers the
first-best and β = 0 ⟺ the valuation ignores the occupant ⟺ the price is
the next-best bid ⟺ market rent. CHECKED (3). The only valuation that
does not tax the occupant is the one that ignores the occupant; that
valuation *is* the market rent, so the ceiling is where the definition
runs out, not where administration fails. State ownership's genuine
contribution is informational: auction the leases and r(z) prices itself.
Real-world corroboration to verify at drafting: public ground-lease
regimes and their revaluation fights (Amsterdam erfpacht; Hong Kong;
Canberra).

**T4 — Stock, flow, and the dial.** The land price is the PV of future
after-tax rents: a credible permanent τ = 1 is a one-stroke 100% levy on
land wealth, collected at announcement via the price collapse and paid
out as the flow — stock and flow are one object at two dates. τ > 1 is
incoherent on this base (hot-potato title; transient over-collection =
a badly targeted capital levy; charging occupiers above rent idles land —
T3). What no rate reaches: wealth that already left the base. The real
dial for stock redistribution is grandfathering inside τ ≤ 1:
increment-only taxation captures exactly γ/δ of the stock (40% at
γ = 2%, δ = 5%; full immediate capture = 100%). CHECKED (2). Who eats
the announcement date is the SEB bank material (LTV, double-trigger,
covered bonds) — cite, don't absorb. The escaped stock has one front-door
instrument: the gate tax's introduction step is an Auerbach–Kotlikoff
one-time levy of t/(1+t) on accumulated wealth (20% at t = 25%) —
non-distortionary only as a surprise, so a step, not a lever. CHECKED (2).
[A–K to live-verify; seeded in P2's sketch.]

**T5 — The circular flow, disciplined.** The gross recirculation of a
rent-funded dividend has fixed point R\* = R₀/(1−φ_r·τ); the convergence
gap at τ = 1 is exactly φ_w, so the loop closes only in the corner — the
Tableau with the state as the landlord class. CHECKED (3). Net
discipline: transfers move spending, they don't create it; ΔR =
(m_p−m_r)·x, zero in the single-good model, mildly positive empirically
(shelter-heavy recipient baskets, rentier dissaving — the η < 1
signature). κ under a rent-price scaling g: κ(g) = κ₀·g/((1−h)+hg) —
rises in g only because h < 1, is fully invariant at h = 1, and a 10%
rent-price rise at today's h ≈ 0.62 lifts κ ~3.6%: second-order, as the
conservation argument requires. CHECKED (6). The land-per-head ceiling is
loop-proof: the circle inflates kronor on both sides of κ and creates no
square meters. Voucher-capture evidence [Collinson–Ganong 2018, to
verify] gives m > 0 and prices the τ < 1 leak to untaxed landowners — the
circularity argument is an argument *for* full capture. P5's
"loop-raises-rents on-ramp" gets its algebra and its limits here.

**T6 — Tier 2: the gate tax's three legs.** Per unit at rate t, revenue
t·c splits t·c·φ_w + t·c·φ_r (0.15/0.10 at the worked instance, t = 25%).
CHECKED (3). Leg one (wage) is P1's "payroll tax in disguise," decaying
at dφ_w/dλ = ρ\*/(1−a) per unit of λ. Leg two (rent) is lump-sum and
reaches what the cadastre can't: non-site rents (P1's sentence) and — 
destination-based — foreign site rents (the parked C.5 border sentence is
this paper's to develop). Leg three (stock) is the A–K introduction step
(T4). Against a payroll tax: strictly larger lump-sum share, border-proof
base, and an impurity that automation retires. Progressivity is the
pair's: flat gate plus flat dividend = rising average rates.

**T7 — Convergence (the paper's spine).** (i) *Incidence:* as λ→0 the
gate tax and the rent tax become the same tax collected at opposite ends
of the pipe — corner equivalence t·c = τ·R_u at τ = t, CHECKED (2); P1's
prop:landonly/"the bases merge" sentence is the limit point; the new
content is the path and the rate. (ii) *Welfare:* deadweight ∝
λ_C(1−κ)², and along automation BOTH factors fall through one process
(λ_C rises in λ; κ falls in λ through the rent-share channel), so
dDW/dλ > 0 — the index falls monotonically on the way down, not only at
the limit. CHECKED (4), including P1's measured instances (0.72, 0.33) →
0.32 and (0.50, 0.60) → 0.08. *Identification claim, to confirm against
App C's construction:* λ_C (the measured wage-financed share of
consumption, 0.72) is the empirical counterpart of φ_w — if so, the
λ-series (ICIO) is also tier 2's health series: one estimand, two papers.

**T8 — The commons are tier 1.** Congestion, spectrum, water, fisheries,
slots, orbits: user charges administratively, rent collection
economically — scarcities outside the cadastre, auction-revealed,
100%-capturable, hybrid with tier 3 exactly where congestion is the
externality. Real revenue, not core-budget scale.

**T9 — Pigou discipline.** A corrective tax that works erodes its own
base; budgeting core spending on it gives the state a fiscal stake in the
harm (the tobacco-shareholder problem). Book the revenue as incidental.

**Corollary (public goods).** The purchases slice — army, academia — is
public goods, not transfers: the Henry George Theorem's home turf
(differential rents cover public-goods spending at optimal scale;
Arnott–Stiglitz 1979, already live-verified in P1's bibliography). The
floor rides κ; purchases ride HGT; the two claims are disjoint and both
live in tier 1's world.

## 4. New vs. already claimed (the honesty ledger)

Already in P1 (App C "The mix on the way down" + §10/§11 + prop:landonly):
fill-the-rent-base-first optimality; the λ_C(1−κ)² index with the
"both factors improving" register row; the wage slice as "payroll tax in
disguise"; the gate's reach to non-site rents; "in the corollary's limit
the bases merge ... the mix question disappears"; the capitalization
sentence; the payroll-circularity sentence; the physical ceiling; the
pair. Seeded in P2's sketch: the funding taxonomy phrase ("rent base
first, VAT bridge, the λC(1−κ)² deadweight index"); the A–K levy reading
with the λ-perception parameter and US/Nordic calibrations; sovereign
fund vs Meidner; trigger design. Seeded in P5's sketch: the
loop-raises-rents on-ramp; the political economy of τ.

New here: the resolution ledger and the φ_w/φ_r identity (giving λ_C a
model formula and a predicted trajectory); the incidence-convergence
statement with its rate; DW monotonicity along the path as a theorem;
the corner fiscal equivalence as an identity; the entire ceiling block
(definitional 100%, hold-up FOC, withholding identity with the abundance
perversity, auction-as-valuation, the base-switch reading of both τ > 1
and use-charges); the γ/δ grandfathering dial; the loop fixed point tied
to viability, transfer invariance, κ(g), and loop-proofness of the
physical ceiling; the commons tier; the Pigou discipline; the D–M tie;
the three-tier frame itself.

## 5. Paper plan (sections)

1. Introduction — the question, the ledger image, the answer in a
   paragraph. 2. The inherited model (P1 recap). 3. The resolution ledger
   and the taxonomy (T1–T2). 4. Tier 1: the ceiling (T3). 5. Tier 1:
   stock and dial (T4). 6. The circular flow, disciplined (T5). 7. Tier
   2: the gate tax (T6). 8. Convergence (T7). 9. Commons and correction
   (T8–T9). 10. Public goods, objections, and what would count against
   the account.

## 6. Empirical assemblies

- **φ_w series** = the λ-series ICIO estimand (progress_and_prosperity;
  READ memo `lambda/READ_MEMO.md`). Shared, already under construction.
- **λ_C reconciliation**: find App C's 0.72 construction and confirm (or
  refute) λ_C ↔ φ_w. Gating for T7(ii)'s measured version.
- **h**: bundle rent content beyond the 0.62 FMR first cut — CE/HBS
  machinery already built for P2.
- **κ series**: P1 data item (0.33 [0.18–0.59]).
- **Voucher capture**: Collinson–Ganong 2018 for m > 0 and the τ < 1 leak.
- **Nordic gate scale**: standard VAT rates and revenue/GDP as the
  feasibility datum for tier-2-carries-the-state.
- **Commons inventory**: spectrum receipts, congestion schemes, resource
  royalties — one table.
- **γ/δ calibration**: rent growth vs discount for the dial; joins the
  SEB LTV material.
- **Regulated-rent caveat**: where the price channel is muted (Sweden),
  recapture shows in queues and condo prices — how κ and the loop read
  there (the Swedish-fork caveat's fiscal cousin).

## 7. Literature ledger

Verified already (P1's live-verified bibliography): Arnott–Stiglitz 1979;
George 1879. To live-verify before any draft (house rule; zero remembered
constants enter text): Diamond–Mirrlees 1971 (I/II); Mirrlees Review
(Tax by Design, 2011); Auerbach–Kotlikoff (Dynamic Fiscal Policy, 1987);
Fischer 1980 (time inconsistency) and a capital-levies history
(Eichengreen); Collinson–Ganong 2018 (AEJ: Policy); ground-lease sources
(Amsterdam erfpacht, Hong Kong, Canberra); DBCFT (Auerbach, Devereux et
al.) for the same-family discussion; Atkinson–Stiglitz 1976 optional
(uniformity of the gate); ATCOR (Gaffney) only if engaged, and as
conjecture.

## 8. Objections to pre-empt

(i) "A uniform consumption tax is a wage tax" — classically yes on leg
one; the claim is legs two and three plus the decay rate: comparative and
dynamic, not painless. (ii) "λ won't reach zero" — nothing waits on the
corner; T7's theorems are monotone path statements. (iii) Home production
and the informal sector escape the gate — the same leak payroll has; the
relative statement survives; in-model it is the s(q) enclosure margin.
(iv) λ_C ↔ φ_w contested — bands and all-variants discipline, per the
λ-series practice. (v) "The Mirrlees Review already recommends this
architecture" — the snapshot yes; the trajectory, the rate, and the
terminal state are the contribution. (vi) Political economy of 100% —
P5's paper; cite. (vii) Why not DBCFT — same destination family; work
the equivalence at drafting. (viii) Sweden's regulated rents — §6's
caveat item.

## 9. Formalization (later, cheap targets)

T1's ledger identity, T6's leg split, and T7's corner equivalence are
Lean-cheap against the existing `Link/Pinning.lean` structures; the
hold-up FOC and the dial are one-lemma each. Not now; gates nothing.

## 10. Decisions for Stella

1. **Title.** 2. **Program placement:** standalone theory paper that P2
   and P5 consume (the λ-series precedent), vs. P2's theory spine —
   program practice says decide at delivery; PLAN.md gets its line after
   the ruling (untouched tonight). 3. Whether T3/T4/T5 feed the SEB talk
   (bank-slide adjacency). 4. Lean depth, later.

---

---

## 11. Addenda v0.1 (2026-09-02) — the practical design unit

From the 2026-09-02 conversation: her 60/40 use split, her six practical
questions, the shock list, the bond-yield question. Arithmetic:
`code/fiscal_napkin.py` → `data/` (live FRED through link-repo's gated
machinery). Algebra: `checks/check_split.py` ALL GREEN (12). Design:
`docs/design_memo_2026-09-02.md`.

**T10 — The use split is a saving constraint, and it names the source
tier.** Away from the limit output has two uses, adapting/developing (I)
and consuming (C). Under the classical closure (wages and the dividend
consumed, non-land returns reinvested) I/Y = 0.4 is the statement that
accumulators keep 0.4 of income after tax: t = 1 − 0.4/(s·π) on non-land
returns, s the reinvestment fraction, π the non-land capital share
(0.42 gross today, so t ≈ 5% today); consumers' share = w + r_L + tπ.
CHECKED (S1–S2). The instrument is a source tax on non-land returns —
tier 1's second base, the rents the cadastre cannot see (pure profits,
IP, transitional windfalls) — collected as a cash-flow tax that expenses
reinvestment and taxes distribution: the reinvest-don't-consume enforcer.
It is not the gate: investment is outside the gate's base by construction;
the gate preserves capital return, it cannot ration it.

**T10b — The gate retires on a wage-share clock.** With the split
enforced, gate revenue = (w + u) − C_p exactly, so the inclusive rate is
1 − C_p/(w + u + owners' consumption) and reaches zero at
w\* = (1 − I − G_c) − u: 0.37 on the family floor, 0.28 on the single
floor. CHECKED (S3–S5). T7's convergence gets a calendar: gate first,
source tier second, rent tier last. Under the observed half-reinvestment
closure (gross investment 0.18 of GDP against π = 0.42) the split needs
public investment of 0.4 − sπ ≈ 0.19Y today, and the gate cannot carry
it (85% tax-exclusive on the family floor).

**T10c — What determines the split: a rule, not a number.** Her
correction: 40/60 is arbitrary, and even at the capability limit the
dynamic extension (δ, ρ, J) keeps capital expenditure alive. The split
decomposes into four pieces with four determinants: replacement
(measured: CFC/GDP 16.5% in 2025, up from 11.1% in 1950; rising with
composition; in the limit the machine sector's land bill, never zero
while b > 0), machine expansion (demand-determined at cost; its value
share → 0 on the path), terminal conversion (the κ-ceiling investment;
golden rule m = ρ·κ_c, S12; read off the land residual), and a buffer
(a stock; market-priced as a lower bound, engine-modelled as the
complement). The finding: gross investment flat at 21–23% of GDP in
every decade since 1950, net down from 11% to 5%, public net from 3% to
0.8% — the conversion line is the starved one. The build-lag identity
I/Y = (g+δ)·v·(1+g)^J (S9–S10) puts 40% at 5% growth with a five-year
pipeline; today's 21% is 2% growth with none. The market read: TIPS real
yield 2.44% vs −0.91% in 2021, term premium at its mean, breakevens and
credit spreads unchanged — the market is pricing ρ, not risk: saving
supply short of investment demand, which is the split asking to move.
Trajectory: a hump, 21 → 40 → the production-land share 1 − α → 0 for
σ < 1 (S11). CHECKED (S9–S12). Data: `code/split_determinants.py`.
Missing-list and the rule: memo §4b.

**T11 — The announcement date, sized, and the shock list.** Household
land residual $23.5T (45% of real estate, 0.76×GDP; the P1 lower-bound
construction). A credible permanent 98% removes 98% of it at
announcement; a phase-in barely helps (10y: 86%; 30y: 66%) because the
PV sits in the tail; increment-only grandfathering caps the stock loss
at 40% (γ/δ, S7c — T4's dial, now with its price path). A lagged
assessment does not soften the stock shock and pushes the effective rate
above 1 after a rent fall (S8): T3's error buffer in reverse. The
balance-sheet map (mortgages, banks, local government, pensions), the
stabilizer toolkit, and the other shocks are the memo's §7. New
channel: sovereign yields (memo §8) — the transition gap is currently
debt-financed (P1's borrowed channel, 19% of transfers by 2025), which
is what a term premium prices; base migration is term-premium policy;
the capitalized rent flow (≈ 0.76×GDP at current cap rates) is
pledgeable against federal debt.

**T12 — The valuation mechanism: options, not lags.** Her 2026-09-02
fragments (up-lag for prospecting scaled by preregistration; a two-year
down-lag against "the revaluation loophole"; abandonment "fine"; a
state-run anonymous universal auction; a bureau that catches collusion
by buying undervalued land) checked and assembled, S13–S17. A general
up-lag leaves every holder 1 − 0.98(1+g)/(1+gL) of rent — 17% at
g = 2%, L = 10 — and opens the sawtooth: a real engineered dip pays
under (up 10, down 2) and stops only near symmetry, because the
down-lag must be of the order of half the up-lag; a fake dip
(self-reported income) pays under any lags. Lags therefore do
measurement only, short and symmetric. Assessment error is instead
bracketed by two options: the owner's surrender put — conversion to a
ground lease with the structure retained, else the β hold-up returns
(S16b) — capping the tax at r; and the state's automatic take-call at
A(1 − b), her bureau, flooring realized rent and killing
self-reporting (Taiwan's self-declared value with a state purchase
right and the Harberger self-assessed tax, to verify). Effective rate
∈ [0.98(1 − b), 1]. The rent surface is identified by rolling anonymous
sample auctions — T3's auction-as-valuation as a survey — with the
occupant's match right and its bid-chilling cost the open design
question. Prospecting gets a registered discovery window on verified
increments (the exploration-licence logic; her ten years as the term),
not a general lag. CHECKED (S13–S17).

**Section plan amendment.** §9 becomes "Commons, correction, and the
source tier" (T8–T10); §4 "Tier 1: the ceiling" gains the valuation
mechanism (T12) as its second half; new §10 "The transition: shocks and
stabilizers" (T11, including the sovereign-yield channel); old §10 →
§11.

**Honesty ledger, additions.** New here: T10, T10b, T11 and the
wage-share calendar. Already claimed elsewhere, to cite not absorb: the
cash-flow-tax family (Meade 1978; Mirrlees Review; DBCFT), the
Kaldor/Pasinetti saving closure, the SEB bank material (LTV,
double-trigger, covered bonds). Not in the model: a saving function (ρ
is a parameter) — the closure is imported and bracketed, never derived.

---

All prose here is draft register — hers to re-voice at drafting time per
the standing protocol. Checks: `checks/check_three_taxes.py`, ALL GREEN
(35), and `checks/check_split.py`, ALL GREEN (12), sympy + numeric per
the house rule.
