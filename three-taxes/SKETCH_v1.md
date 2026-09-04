# The Fiscal System as Labor's Share Falls — paper sketch v1

**Working title candidates** (hers to pick): "Three Taxes: The Fiscal
System as Labor's Share Falls" · "The Tax System at the Limit" · "Where
to Stand: Scarcity, Consumption, Correction" · "The State as Landlord."

**Status:** v1, 2026-09-02. Consolidates `SKETCH.md` (v0, the theory
ledger T1–T12) and `docs/design_memo_2026-09-02.md` (her six questions,
the shocks, the split rule, the valuation mechanism) into one paper
sketch: prose for the mechanisms, a section structure, the data anchors,
and a verify ledger. Algebra: `checks/check_three_taxes.py` (35 green)
and `checks/check_split.py` (26 green); data:
`code/fiscal_napkin.py`, `code/split_determinants.py` → `data/`. Nothing
committed, nothing drafted as paper prose; all prose here is draft
register, hers to re-voice.

**Placement.** This paper comes *after* the dynamics paper and depends
on it. It imports from P1 (pinning) the static model — the recursion,
the closure, the floor, the fork, the pair, κ — and from the dynamics
paper the results it cannot derive statically: that a credible permanent
rent tax is capitalized at announcement (stock and flow are one object
at two dates); the horizon-relative classification of terminal inputs
and the time-inconsistency of taxing rents on lagged produced inputs;
transitional rents while capacity builds; the build-lag markup on the
investment share and the pipeline stock; the shock experiments by shock
type; and the interest channel of the wage of waiting. Where a section
below leans on one of these it says "imported" and states only what it
needs. The sketch is deliberately light there: the dynamics paper is not
yet visible, and this paper should consume its results, not restate
them.

**Provenance.** Born 2026-08-27 from the circular-flow conversation
(v0's arc); grown 2026-09-02 from her concrete system (land tax near
100% → dividend; a consumption tax; a fund), her six practical questions,
the 60/40 use split, the shocks question, the lag design, and the
auction-and-bureau fragments. Record the arc in the AI-use note at
drafting, per program practice.

---

## 0. The paper in one page

**The question.** Every tax system now standing is built on wages.
Two-thirds of United States revenue is wage-linked (0.68 in 2025);
benefits are conditioned on work or means; the floor is financed, where
it is financed at all, from the one base the model says is shrinking.
What replaces it, in what order, and what does the terminal state look
like?

**The claim.** Every unit of final spending resolves, through the
machine recursion, into exactly two kinds of claim — wage claims and
scarcity claims (T1). A tax system is a choice of where to stand in that
circuit. Three stands are coherent: at the scarcity source (rent
collection — no margin moved, rate up to a definitional ceiling of
100%), at the consumption gate (a destination-based uniform tax — one
margin moved, and only on the wage-resolving share of the flow), and
athwart a named externality (corrective taxes — a margin moved on
purpose). A fourth stand, on the returns to non-land capital, is
coherent only as the *enforcer of a chosen use split* — it taxes what
owners consume out of returns and exempts what they reinvest — never as
a revenue base. The theorems: automation retires the gate into the
source at a computable rate, so the optimal system has a terminal state
and the economy is walking toward it (T7); the scarcity tier's ceiling
is definitional, not administrative (T3), and its assessment problem is
solved by two options rather than by lags (T12); the whole system has a
clock — the wage share — on which each instrument's rate is read (T10b);
and at the terminal state the fiscal system is the state as landlord,
paying a dividend, with everything else retired.

**The system in five sentences.** A land tax at 98% of
auction-identified rent, bracketed by the owner's surrender put and the
state's automatic take-call, with the un-parceled commons priced the
same way. A uniform destination-based consumption tax carrying the
state's purchases and the floor's residual while the wage share is
high, declining on the clock to zero. A cash-flow tax on non-land
capital returns at the rate that leaves accumulators exactly the
reinvestment the use-split rule requires. A uniform dividend pegged to
the floor, filled from rent first and from the gate and the source tier
in the transition, rising above the floor as the surplus appears.
Existing wage-linked taxes retired in the order of their distortion,
earnings-related promises grandfathered, in-kind human-essential
provision kept.

**Dropped, with reasons (§12).** The general valuation lag; the 2:1
rule; 40/60 as a number; the foreign-scarcity fund as a strategy;
universal auction coverage; capture of transitional rents on lagged
inputs; any function for private title beyond a transition annuity.

**Deferred to the dynamics paper (§13).** The announcement-date theorem
and its price paths; the build-lag and pipeline identities; horizon
terminality and time-inconsistency; transitional rents; the shock
experiments; the interest channel.

---

## 1. Introduction

Open on the base, not the model. The United States collects 28% of GDP;
0.68 of it is wage-linked, and the wage-linked share has been flat since
the mid-1980s while the labor share has fallen. Benefits are 16% of GDP,
at least 0.84 of them conditioned on work or means. Every instrument in
that system stands on a margin the automation literature expects to
thin. The question is not whether to redesign but where the replacement
stands: on which flow, at which point in the circuit, at what rate, in
what order, and with what end state.

Then the image. Trace a dollar of final spending back through the
machine sector's own recipe — machines from machines, labor, and
non-produced inputs — and it resolves into two claims and nothing else:
wages, and rents on inputs whose supply does not expand with
production. The shares are λρ*/(1−a) and its complement; the ledger
closes exactly (T1). A tax is a choice of where on that path to stand.
Standing at the source takes rent and moves no margin. Standing at the
consumption gate takes a uniform slice of the whole flow and moves one
margin — labor supply — on the wage-resolving share only. Standing on a
named externality moves a margin deliberately. Standing anywhere else —
on income, on payroll, on corporate profit as ordinarily defined, on
"the user of land" — is one of these three in disguise, with an origin
base that invites border games (T2). Diamond–Mirrlees closes the door
formally, and the scarcity tier's full rent capture supplies exactly the
no-pure-profits precondition they need.

The contribution, stated as new against what is already claimed. P1's
Appendix C states the architecture in a paragraph — rent base first, a
consumption-tax bridge, a deadweight index that falls as both its
factors improve. This paper grows that paragraph into a fiscal system
with its limit theorems, its clock, and its transition. Against the
Mirrlees Review, which recommends a snapshot of the same architecture,
the contribution is the trajectory, the rate of convergence, and the
terminal state; against George, the ceiling theorem, the valuation
mechanism, and the disciplined circular flow; against the
destination-based cash-flow tax literature, the resolution ledger that
says *why* destination and *which* margin. Say each in one sentence and
move on.

Roadmap; then the imports paragraph: what the paper takes from P1 as
given and what it takes from the dynamics paper as theorems it will use
but not prove.

---

## 2. The inherited model and the resolution ledger (T1–T2)

Recap P1 in a page: tasks, the assignment margin w = c·ρ*, the recipe
c = ac + λw + ℓr, the closure, viability, the floor s(q), the fork, the
pair (rent tax, uniform dividend), κ = rT/(N·P_s). Nothing new here
except the emphasis: every produced input's price passes backward until
anchored by a factor outside the recursion or by the labor still inside
it.

**The resolution ledger.** Unwind the recursion on one unit of final
price. The total wage content is λw/(1−a); the total rent content is
ℓr/(1−a); they sum to c exactly. Define φ_w = λρ*/(1−a) and φ_r = 1−φ_w.
Viability pins φ_r ∈ (0,1); the worked instance (0.5, 0.1, 3, 0.2, 1)
gives (0.6, 0.4); the corner λ→0 gives (0, 1). CHECKED. The empirical
counterpart is the labor-origin financing share of consumption (P1's
Appendix E, 0.66 in 2023 with bounds) — the identification claim
λ_C ↔ φ_w is to be confirmed against that construction before the
measured version of T7 is stated; the λ-series is then this paper's
health series too, one estimand in two papers.

**The taxonomy.** Three stands, and the decomposition of the tempting
fourth. "Tax the user of land" splits on incidence: the
land-conditioned part is borne by rent (bidders subtract it; with the
state as landlord it cannibalizes the source tier one-for-one), and the
activity-conditioned part is ordinary factor taxation with an origin
base. The corporate income tax as ordinarily defined is a mix of a tax
on pure profit (a scarcity claim, source-tier material) and a tax on the
normal return (a margin moved on accumulation); §5 separates them by
base design.

**The gap as evidence.** Consumption is 66% labor-financed and 47%
labor-made (2023): the nineteen-point gap is the aggregate footprint of
the recursion's non-wage terms — site rents, the gross return stack,
institutional rents, foreign content — and it exists only through four
doors (saving asymmetry, depreciation and retention reflux, fiscal
recycling, the border). One paragraph; the accounts are P1's.

---

## 3. Tier 1 — the scarcity source

### 3.1 The ceiling is definitional (T3)

Market rent is the next-best bid for the bare site: use-independent,
occupant-invariant. In the competitive closure there is nothing above
100% of r(z) to collect — site heterogeneity is already inside the base
(r(z) is the Ricardian differential) and person heterogeneity resolves
to wages. Three ways to try anyway, each with its theorem: a uniform
price above clearing is a withholding monopoly whose gain,
(T−A/2)²/B in the linear instance, is positive only by idling land and
grows with abundance — manufacturing scarcity pays most where natural
scarcity is mildest; discriminatory value-of-use pricing is a marginal
tax approaching 100% on what the occupant adds; and the dynamic version,
revaluation capturing a share β of tenant improvements, has the
occupant's effort e*(β) strictly falling in β, with β = 0 recovering the
first-best exactly when the valuation ignores the occupant — which is
the definition of market rent. CHECKED. The ceiling is where the
definition runs out, not where administration fails. State ownership's
genuine contribution is informational: auction the leases and r(z)
prices itself.

Real-world corroboration to verify at drafting: public ground-lease
regimes and their revaluation fights (Amsterdam erfpacht, Hong Kong,
Canberra).

### 3.2 The valuation mechanism: options, not lags (T12)

This is the section her practical questions built. Prose it fully.

**Why 98 and not 100.** The 2% is not an owner's incentive — land needs
none — but an *error buffer*: an assessment above true rent taxes the
occupant's contribution and idles the parcel, so the rate sits below the
assessment's error. The practical consequence of 98% is that the land
price falls to about 2% of its capitalized value plus option value, and
sales stop revealing rent. Assessment must therefore move off
transaction prices onto a mechanism, and every version of the mechanism
converges on the state as landlord in all but name. Say so.

**Why not a lag.** The natural instinct — smooth the assessment with a
multi-year lag, perhaps asymmetric, longer on the way up to reward those
who raise a site's value — fails three ways, each checked. A general
up-lag pays whoever holds the site when rent rises, discoverer or not:
under partial adjustment at speed 1/L in steady growth g the assessment
settles at (1+g)/(1+gL) of rent, so a ten-year lag at 2% growth leaves
every holder 17% of rent permanently, a two-year one 4% — a rate cut
concentrated in the fastest-growing metros, where the unearned increment
is largest (S15). An asymmetric lag opens the sawtooth: engineer a dip
in measured rent, let the assessment fall, ride the up-lag while true
rent recovers; at a 98% rate the owner's stake in rent is 2%, so a real
dip costs almost nothing beyond the tax paid on the old assessment while
the dip lasts, and under (up 10, down 2) a two-year engineered dip still
pays the owner 1.75 years of rent — it stops paying only near symmetry,
because the down-lag must be of the order of half the up-lag (S13). And
a fake dip — a low self-reported lease to a related party under
income-based assessment, true rent still received — pays under every lag
structure whatsoever (S14). Lags can do measurement only, short and
symmetric; error control needs something else. As a shock absorber for
the *stock* a lag does nothing at all: a credible permanent rate is
capitalized at announcement whatever the assessment lag (imported, T4).

**The two options.** Assessment error is bracketed by options instead.

*The owner's surrender put.* An owner assessed above market surrenders,
so the tax can never exceed the rent: the overshoot after a rent fall is
capped at 1.00 (S16). Surrender must be of the *land*, the structure
retained — conversion to a ground lease at the next auction's rent with
the occupant in place. If the structure goes with the title, an owner
tolerates over-assessment up to the structure's annual value before
walking, the put never bites on built parcels, and the state holds up
improvements — the β problem by another route (S16b). Two more
conditions: the state re-lets promptly (the interim is idling, and in a
rent downturn surrenders arrive by the million — auction capacity is the
binding constraint), and lenders are neutral to it (after the tax the
land collateral is near zero, so a structure-retained surrender does not
touch the mortgage; a structure-forfeit one is a default).

*The state's automatic take-call.* When a parcel leases or trades below
the assessment by more than the buffer, the state takes the lease at
that price and re-lets it. Colluding bidders cannot obtain the parcel
cheaply, because the state takes it; a self-reported low rent forfeits
the parcel, so the fake dip dies (S17b). Precedents to verify: Sun
Yat-sen's design in Taiwan's land-value tax, self-declared values with a
state purchase right at the declared value; the Harberger self-assessed
tax with a standing purchase option. The one design rule that matters:
the trigger is automatic — clearing price below assessment minus buffer,
no discretion — or the bureau becomes the corruption locus; and its
purchases carry a re-letting obligation, so it never becomes a land
bank. Its tolerance band is the error buffer.

*The bracket.* The put caps the tax from above at the rent; the call
floors realized rent from below at assessment minus buffer. Between them
the effective rate on true rent lies in [0.98(1−b), 1] — [0.96, 1.00] at
b = 2% (S17). Error is bounded in both directions, and the lag's only
remaining job is measurement.

**Identification: rolling anonymous sample auctions.** The rent surface
is identified by auctioning the ground lease of a random rolling sample
of parcels each year, sealed and anonymous — not every parcel. Universal
coverage founders on thin markets (most parcels have no genuine second
bidder), on structures (an outside winner must buy the building, which
moves the valuation problem onto structures), and on scale. The sample
identifies the surface; the assessment of un-auctioned parcels is
interpolated from it — the ceiling section's "auction the leases and
r(z) prices itself," done as a survey. The sitting occupant needs a
right to match, else the β hold-up; a match right chills outside bidding
(bidders know they lose to a match — the auction-theory result on
rights of first refusal, to verify), so bidders need a reason to bid: a
premium paid to the matched bidder, or a match right limited to a share
of the increment. Open design question; a candidate theorem if cheap.

**Discovery.** The ceiling argument is static. Discovering that a site
is worth more — minerals below, a use no one had priced — raises the
next-best bid, which a 100% tax at instant revaluation takes entirely,
so no one looks. The reward is not a lag but a licence: preregistration
as an exclusive discovery right with a fee, a work commitment, and
relinquishment if idle, carrying a retention window on the *verified
discovered increment* — the difference between post- and pre-discovery
next-best-bid rent, never general appreciation. Ten years is a
defensible term; the alternative is cost recovery with an uplift (to
verify against the resource-rent literature: Garnaut–Clunies Ross, the
Brown tax, Norway's and Australia's designs). Urban "prospecting" —
finding a site's best use — needs no window: its reward is the untaxed
structure. Free registration for everyone is the free-option trap.

**Who sets the rent, and who manages usage.** The incentive a private
holder has — "the highest rent that doesn't cause the user to flee" —
is the ceiling section's pathology stated from the holder's side: the
user's reservation value exceeds the next-best bid by the user's sunk
stake, so a holder acting on it taxes the occupant's contribution and
improvements fall. The mechanism therefore takes pricing away from
holders altogether; the rent is the auction-identified next-best bid and
the bracket enforces it. A private "title" is then a claim on 2% of a
rent someone else sets, on a parcel whose use someone else chooses; it
has no function beyond the transition — an annuity to former owners, the
residual claimant of the error buffer. The paper says so: this is state
landlordism, and "title" is a name. Usage management does not vanish; it
migrates. To the user: improvement incentives need long leases, renewal
rights, and compensation for improvements at lease end (β = 0), or the
leasehold dilapidation problem appears (verify against Hong Kong,
Singapore, Canberra practice). To the auction: land assembly needs
bundle bids, or the state assembles. To the state: externalities,
zoning, covenants against depletion and contamination — the state as
ultimate landlord keeps usage rights. The one productive incentive a
landlord has — raising the next-best bid by improving the site or
matching it to its best user — is worth 2% to a holder and 98% to a
state that lacks the local knowledge; the lease is where it is handed to
the user.

### 3.3 The commons are tier 1 (T8) — the inventory

Congestion, spectrum, water, fisheries, slots, orbits, the carbon sink,
minerals and hydrocarbons, transmission and interconnection capacity,
permits and zoning: scarcities outside the cadastre, auction-revealed,
100%-capturable, hybrid with the corrective tier exactly where
congestion is the externality. Real revenue, not core-budget scale. The
paper carries one table, rated on feasibility and effectiveness:

- *Clean, precedented, do now:* minerals and hydrocarbons (resource rent
  taxes: Norway's petroleum regime, Australia's PRRT); spectrum
  (recurring rentals rather than one-time sales — the difference between
  a sale and a lease is the whole point); congestion (London, Singapore,
  New York); the carbon sink (the EU ETS; the model's terminal-input
  reading, with the Pigou discipline of §10 attached).
- *Feasible with reform:* water rights (auctioned rentals; politically
  hardest); transmission and interconnection (auctioned queue positions,
  public congestion rents); permits and zoning (auction the scarcity or
  abolish it — Singapore's certificate-of-entitlement auction is the
  clean instance of pricing an artificial scarcity; supply expansion is
  the stabilizer P1 names, and the permit auction is its fiscal shadow).
- *Do not:* transitional rents on lagged produced inputs — energy
  capacity built over years, fabrication bottlenecks — because an
  anticipated levy on rents that exist only while capacity builds deters
  the build (imported: the dynamics paper's time-inconsistency result);
  general "windfall" taxes for the same reason; intellectual property
  beyond term reform, because the rent is chosen to elicit creation with
  fixed costs (P1's ideas paragraph, Romer) — the instrument there is the
  term and the scope, not a levy.

All precedents are memory until live-verified.

### 3.4 What tier 1 cannot reach

Non-site rents — pure profit, market power, institutional rents — sit
outside the cadastre; so do foreign site rents embodied in imports. The
gate reaches both when they are consumed (§4); the source tier reaches
the first at source (§5). Say this here so the tiers' division of labor
is visible before the gate is introduced.

---

## 4. Tier 2 — the consumption gate (T6, T10b)

**The three legs.** Per unit at rate t, revenue t·c splits into
t·c·φ_w + t·c·φ_r (0.15/0.10 at the worked instance, t = 25%). CHECKED.
Leg one, the wage leg, is P1's "payroll tax in disguise," decaying at
dφ_w/dλ = ρ*/(1−a) per unit of λ. Leg two, the rent leg, is lump-sum and
reaches what the cadastre cannot: non-site rents and, destination-based,
foreign site rents — the 9.4 points of consumed production that resolve
abroad. Leg three, the stock leg, is the introduction step: a one-time
levy of t/(1+t) on accumulated wealth (20% at t = 25%), non-distortionary
only as a surprise — a step, not a lever (CHECKED; Auerbach–Kotlikoff to
verify). Against a payroll tax: a strictly larger lump-sum share, a
border-proof base, and an impurity that automation retires.
Progressivity is the pair's: a flat gate plus a flat dividend is a rising
average rate.

**Design.** Uniform rate, credit-invoice method (self-enforcing along
the chain), destination-based, no reduced rates — the dividend is the
progressive element and replaces zero-rating. Base: as broad as New
Zealand's (C-efficiency near 0.95 against an OECD norm near 0.56 — to
verify); financial services in; imputed rent out (it cannot be observed
at the transaction, so new construction is taxed at sale as the present
value of structure services, the standard treatment); residential site
rent visible in leases exempt, because with the source tier at 98% a
gate on land services is a relabel — fixed supply means the tax is borne
by rent, and the land-tax base falls one-for-one (T2). Rate ceiling from
practice: evasion rises with the rate, and 27% tax-exclusive (Hungary) is
the observed top.

**The rate is a residual, and the first use is the swap.** Given the
floor and what the gate must carry, the rate is need over base. On the
2025 napkin: the floor's residual after rent alone needs 8–13% on the
family-of-four bundle (21–35% single; the second figure at a 0.6 base);
the two-instrument system that also carries all government purchases
needs 33–77% and is infeasible; the revenue-neutral swap that retires
personal income taxes and payroll contributions needs 19% (32% at a
realistic base). The swap is the first use, not the floor: for a worker
a gate at inclusive rate τ is a wage tax at τ, but to raise the same
revenue the gate's rate on the labor margin is lower by the factor φ_C,
because a third of its base is rent-origin, dissaving-origin, and
foreign-content consumption that payroll never reaches — a third off the
labor-margin distortion today, growing as φ_C falls. A gate-funded
dividend, by contrast, is circular on the labor slice and, in the limit,
a closed loop.

**The clock.** Under the use-split rule of §5 the gate's rate has a
closed form: τ = 1 − C_p/(ω + u), the excess of consumers' income over
the consumption allotment, with ω the wage share and u the floor's share
of output. It is 28% inclusive today on the family bundle and reaches
zero when the wage share falls below C_p − u ≈ 0.37 (0.28 on the single
bundle), because below that the source tier and the land tax already
cover purchases and the floor (S5). The gate is the *early* instrument.
Two structural facts go with the clock. In the limit a uniform gate and
the land tax are the same tax: with all income rent on a fixed factor,
any uniform consumption tax is incident on that factor (T7's corner
equivalence). And a *rising* gate rate over time taxes waiting, so the
schedule must be announced and monotone-declining — which the clock's
is.

---

## 5. The source tier — the cash-flow tax as the use-split enforcer (T10)

**The split is a saving constraint.** Money has two uses: adapting and
developing the economy, and consuming from it. Investment is financed by
saving. If wages and the dividend are consumed and owners reinvest their
after-tax non-land returns, a use split I/Y = s is the same statement as
"accumulators keep s of income after tax, consumers get 1−s": under the
classical closure the use split *is* a distribution rule, and the
financing-versus-production gap is the evidence the closure roughly
holds. Today's gross non-land capital share is about 0.42 (wages and
supplements 0.51, proprietors' labor about 0.04, measured land 0.03), so
a 40% target is essentially today's factor split, and "land tax at
98%, leave the rest of capital income alone, gate within the
consumption flow" is nearly self-consistent today under full
reinvestment.

**The instrument.** Holding the split as the factor split moves
requires taking the excess capital return at source: consumers' share
= ω + r_L + t·π = 1 − s, hence t = 1 − s/π on non-land returns (S1–S2).
The gate cannot do it — investment is outside its base by construction;
the gate is the instrument that *preserves* capital return, not one
that rations it. The land tax does it for the land part only. The
right base for t is the cash-flow corporate tax with full expensing and
loss refundability: it taxes distributions and exempts reinvestment, so
it is precisely a tax on what owners consume out of returns — the
enforcer of the closure — and it reaches pure profit and institutional
rents (the 8.4 points of consumed production the WP2026 benchmark
identifies as IT, R&D, software, and artistic capital) without touching
the normal return. Rate schedule along the clock: 5% today, 21% at a
wage share of 0.45, 31% at 0.35, 39% at 0.25, 46% at 0.15, on the family
bundle with full reinvestment. In the limit the base thins — reproducible
capital is competed to cost — and the value migrates into land, where
the source tier takes over: the terminal-claimant result.

**The realistic closure.** Owners do not reinvest everything: gross
investment is 21% of GDP against a gross non-land capital share of 42%,
so about half of gross returns come back as investment. Under that
behavior a 40% split cannot be reached by leaving returns with owners;
the state invests the gap itself — 19% of GDP of public "adapting"
today — and funding it through the gate pushes the rate to 85–104%
tax-exclusive. The consistent alternative is the cash-flow tax on the
*consumed* half, which is roughly what income and corporate taxes do
now, done badly. This is the paper's most exposed calibration; carry it
with both closures.

**What not to tax at source.** Interest — the wage of waiting — is
competitive and real (imported: the dynamics paper's interest identity);
a tax on it moves the accumulation margin and the model does not
determine the supply response. A wealth tax is a poor substitute for the
land tax plus cash-flow tax (it taxes the normal return at a rate that
hits low-return assets hardest). Personal capital income is exempt up to
the normal return (a rate-of-return allowance — Mirrlees Review, to
verify) with rents above it inside the cash-flow base. An estate tax is
the periodic capital levy on inherited rent claims — the ownership
distribution the pair redistributes is inherited — and belongs in the
paper as the instrument on the *stock* of scarcity claims, with the
avoidance caveat.

---

## 6. What determines the split: a rule, not a number (T10c)

Her correction, taken as the section's premise: the split is arbitrary,
and even at the capability limit capital expenditure never stops —
machines must be maintained and shocks met. The question underneath is
how much adaptability and expansion the economy needs against how much
it can sit and enjoy what it has. The split decomposes into four pieces
with four determinants, only one of which is a choice.

**Replacement — sit and enjoy what we have.** Consumption of fixed
capital is 16.5% of GDP in 2025, up from 11.1% in 1950: a floor, measured,
and rising, because the capital stock's composition shortens (equipment,
software, IP; part of the rise is the 2013 capitalization of IP in the
accounts — caveat). A datacenter-heavy stock raises it further. Reading
this piece off depreciation is right, with two caveats: economic
depreciation includes obsolescence, so it contains adaptation and
over-states pure maintenance; and the composition is endogenous to the
split — what you build sets what you must replace. In the limit the
piece never vanishes while the machine sector uses land: it is the
machine sector's land bill (imported: the user-cost closure).

**Machine expansion.** Demand-determined: free entry prices machines at
cost, so no policy sets this piece. Its *value* share goes to zero on the
path while its physical scale explodes. Most AI capex is this piece, and
most of that is replacement.

**Terminal-input conversion.** The public, lumpy, long-lived,
capital-heavy investment that raises the κ ceiling — housing density,
energy capacity, transmission, water. If anything carries a large share
it is this: at a capital-output ratio near 12 even 2% growth needs 42% of
output gross (imported: the build-lag table). It is the piece the golden
rule governs — convert until the marginal rent yield equals the interest
rate (S12) — and its market signal is the land residual itself: $23.5T is
the price of conversion not made, and the metro dispersion of land
shares (a data item to build; the Glaeser–Gyourko zoning-tax literature,
to verify) reads how much of it regulation could dissipate. With the
land tax in place the state is the residual claimant on conversion, so
public conversion is self-financing at the margin — the Henry George
theorem's dynamic form.

**The buffer.** A stock — reserves, reserve margins, the fund of §8 —
whose flow cost is the carry. Markets price part of it: insurable,
diversifiable, near-horizon risk (catastrophe-bond spreads; energy
futures volatility and backwardation as the price of terminal-input
shocks; sovereign spreads and term premia as the price of the fiscal
base; Tobin's q by sector and capex-to-depreciation ratios as the
revealed replacement-versus-expansion split). Insurance *retreat* is the
market declining to price — a direct reading of adaptation not made.
What markets cannot price is systemic, uninsurable, long-horizon, and
policy-endogenous risk, so market reads are a lower bound; the
complement is the shock ledger on the dynamics engine (imported).

**The finding.** Gross investment, private plus public, has held at
21–23% of GDP in every decade since 1950; the replacement floor rose
from 11% to 16.5%; net investment therefore fell from 11% to 5%, and
public net investment from 3% of GDP in the 1950s–60s to 0.8% in the
2020s. The United States has been answering the question with "sit and
enjoy" for seventy-five years in net terms, and the line that vanished
is the conversion line — the κ-ceiling lever. A 40% target is therefore
1950s net accumulation on a floor five points higher, plus a pipeline;
it is the buildout-phase value of the rule, not a steady state.

**The market read.** Latest against 2021: the 10-year real yield 2.44%
against −0.91%; the term premium 0.88 against −0.16 but at its
long-run mean; breakevens unchanged; credit spreads low; equity
volatility low. The market is not pricing a crisis premium; it is
pricing a higher required return on waiting. In the model's terms,
saving supply is short of investment demand at the old price: the bond
market is saying the split wants to move toward adaptation, and it will
move it the expensive way (crowding out consumption and the state)
unless policy moves it the cheap way — the source tier exempting
reinvestment, public conversion. The real yield is thereby the rule's
observable: set the split, and the market reports whether saving supply
matches it. (The interest channel itself is the dynamics paper's; this
paper uses only the reading.)

**The rule and the trajectory.** Replacement as measured, machine
expansion as demanded, conversion to the golden rule, a buffer held as a
stock sized at the larger of the market-priced and engine-modelled
ledger — with the source tier's rate set to leave exactly that in
accumulators' hands and the state investing the conversion piece. In
value shares the trajectory is a hump: 21% today, 30–40% while the
conversion pipeline fills and the short-lived AI stock turns over, then
decay toward replacement plus growth, and in the limit the production-
land share 1−α, which tends to zero when goods and land services are
complements (S11) — everything is "enjoying," because what is had is
land services and free goods. Two further points the paper should make
out loud: the split must be stated in physical or hours terms, or as a
share of rent, not in money, because the value share of machine
investment goes to zero on the path; and human adaptation — retraining,
education — is consumption in the accounts and does not move the fork
in the model, so it belongs on the consumption side of the ledger.
Population enters through the ceiling T/(N·h_s): demographic decline is
the cheapest adaptation there is.

---

## 7. Convergence — the paper's spine (T7)

**Incidence.** As λ→0 the gate and the land tax become the same tax
collected at opposite ends of the pipe: corner equivalence t·c = τ·R_u at
τ = t. CHECKED. P1's "the bases merge" sentence is the limit point; the
new content is the path and the rate, dφ_w/dλ.

**Welfare.** The deadweight index is λ_C(1−κ)², and along automation both
factors fall through one process — λ_C rises in λ, κ falls in λ through
the rent-share channel — so the index falls monotonically on the way
down, not only at the limit. CHECKED, including P1's measured instances
(0.72, 0.33) → 0.32 and (0.50, 0.60) → 0.08.

**The clock, assembled.** One table for the whole system along the wage
share and κ, on the family bundle with full reinvestment: land tax
constant at 98% with a rising yield (3% of GDP today, 9% at κ = 1); the
gate 28% inclusive today, 15% at ω = 0.45, zero below 0.37; the source
tier 5% → 21% → 31% → 39% → 46%; the surplus above purchases and floor
appearing below ω ≈ 0.35 and reaching 0.22 of output at ω = 0.15, which
is what funds the dividend above the floor and the buffer. The realistic
closure's version alongside. Every number is a napkin on live accounts;
the shapes are the claims.

**What the clock is not.** It is indexed by the wage share, not by
calendar time; the paper makes no forecast of when. The dynamics paper's
path results — how fast, through which lags — are imported where the
transition sections need them and otherwise left alone.

---

## 8. The transition, part one: removal order and revenue allocation

### 8.1 The replacement map (her Q5)

Taxes, in the order of their distortion and their replacement:

1. *Property tax on structures* → gone; the land part continues as the
   land tax (the split-rate move: Denmark, Estonia, Pennsylvania's
   cities, to verify). Same administrative base; do first.
2. *Corporate income tax* → converted, not removed: expensing, loss
   refundability, no interest deduction — the cash-flow base of §5.
   Investment-promoting; do early.
3. *Payroll contributions* → the purest wage tax; replaced by the gate's
   swap. But they fund earnings-related promises, so removal pairs with
   the grandfathering below: stop accruals, honor the accrued, fund from
   general revenue.
4. *Personal income tax on wages* → last, in steps as the wage share
   falls; its base shrinks anyway (the wage-linked share 0.68, flat
   since the mid-1980s, declines from here). Keep a progressive surtax on
   high labor incomes only as long as institutional wedges on tasks are
   large — P1's wedge material says those are automation's first
   targets, so the surtax's base is the one that goes first.
5. *Capital gains and dividend taxes* → the rate-of-return allowance;
   rents above the normal return inside the cash-flow base.
6. *Sales taxes and general excises* → folded into the gate; excises on
   externalities (fuel, tobacco, carbon) stay — they are prices, not
   revenue, under the Pigou discipline of §10.

Benefits:

1. *Cash means-tested programs* (SNAP, TANF, SSI, EITC, the floor of UI)
   → the dividend, first. The conditionality result: within the
   two-payment class the same transfer in and out of work is the unique
   design with zero compensated participation effect; means-testing is
   the out-of-work withdrawal band that traps more workers as wages
   compress.
2. *Social Security* → its floor function to the dividend; the
   earnings-related part grandfathered — closed to new accruals, not
   removed; retired by attrition.
3. *Health and care* (Medicare, Medicaid) → kept in kind. They are the
   human-essential floor content of P1's Appendix D — care hours in the
   bundle whose price rises on the Baumol branch — and cannot be cashed
   out without the floor's price rising against the dividend that pays
   it.
4. *Housing subsidies* → redundant once land tax and dividend stand,
   but the physical constraint (the ceiling below one on 13 of 32 grid
   members) says supply, not vouchers, is the fix; remove last, replaced
   by conversion spending. Voucher capture (Collinson–Ganong, to verify)
   prices the τ < 1 leak to untaxed landowners meanwhile.

"If at all": the wage-linked instruments go; the in-kind human-essential
ones stay; earnings-related promises are honored by grandfathering; the
corrective instruments are re-booked, not removed.

### 8.2 The allocation rule (her Q6)

Revenue has four claimants and the paper orders them:

1. *The floor first.* The dividend pegged to P_s, filled from rent (κ of
   it) then from the gate and source tier; the pair is the
   non-distortionary transfer and the land tax's natural home. Her 2:1
   rule — for each required dollar of purchases raise two, one to
   government and one to the dividend — is dropped: it pegs the dividend
   to purchases rather than to the floor (a war doubles the dividend), it
   doubles the gate's rate for a given G, and the deadweight on the wage
   leg is quadratic in the rate (v0's assessment stands).
2. *In-kind human-essential provision.* Its value share rises on the
   Baumol branch even at fixed quantity; budget it as a rising share, not
   a fixed one.
3. *Conversion investment.* The public part of the split rule — the
   κ-ceiling raiser; self-financing at the margin under the land tax.
4. *The buffer, then the dividend above the floor.* The buffer is a
   stock sized by the shock ledger and the ceiling shortfall, not a
   fixed share; the dividend rises above the floor only from the surplus
   that appears below a wage share of about 0.35.

**The fund, sized by its case.** A sovereign fund has three coherent
jobs and one incoherent one. Coherent: smoothing (rent is volatile —
κ's grid fell from 0.35 to 0.13 through 2008–12 on the balance-sheet
members; a two-to-five-year assessment average or a fund of one to two
years of the floor bill is the choice); intergenerational conversion of
one-time transitional rents into permanent income (the dynamics paper's
windfall result, imported); and a hedge on the domestic ceiling
shortfall — for the grid members where T/(N·h_s) < 1, domestic rent can
never fund the floor, and a claim on rent elsewhere is the only fiscal
fix. Incoherent as a strategy: "owning foreign scarcity." Foreign land
is restricted in most jurisdictions, politically explosive, and — the
model's own point — the host state's rent tax has first claim, so the
fund's exposure is only as good as the host's under-taxation of its own
rents. Domestically the fund is redundant: with the land tax the land
registry *is* the fund. Size it by the ceiling shortfall and the shock
ledger, not by a share of revenue; it exists in the paper as a hedge and
a smoother, not a pillar. Alaska's dividend fund is the precedent to
verify for the smoothing role.

---

## 9. The transition, part two: shocks and stabilizers (T11)

Keep this section to the *static* half — who bears what, and what the
state can do — and import the price paths.

**The announcement date.** A credible permanent rate is capitalized at
announcement (imported): the household land residual, about $23.5T on
the balance-sheet construction, falls to its 2% remainder plus option
value. Who eats it: owners, disproportionately older and richer; and
lenders, because roughly $13T of household mortgage debt is
collateralized on land plus structures, and the land part of the
collateral vanishes. The property market freezes because sellers cannot
clear their loans from sale proceeds. What the state can do, in order of
coherence:

1. *The dial.* Grandfathering inside τ ≤ 1 — increment-only taxation
   captures exactly γ/δ of the stock (40% at 2% rent growth and a 5%
   discount; CHECKED) — is the only stock-redistribution instrument that
   is not a base switch. A phase-in is the dial's time form; the price
   table (imported) says even a ten-year phase-in leaves most of the
   stock loss in place, because the market prices the end state. The
   dial is a *distributional* choice about how much of the stock the
   state takes, not a stabilizer.
2. *The rent-backed-debt swap.* The state, now the rent claimant, is
   the natural counterparty for the collateral it removed: mortgages
   whose land component is impaired are refinanced against the parcel's
   rent stream — a structure-retained ground lease with the mortgage
   re-collateralized on the structure and the state's rent claim netted
   against the borrower's tax. Prose until she says otherwise.
3. *Bank pass-through.* Loan-to-value limits, the double trigger, covered
   bonds — the SEB material; cite, don't absorb. The paper states the
   exposure (land share of mortgage collateral × the rate) and leaves the
   prudential response to the practitioners.
4. *The surrender put* (§3.2) is itself a stabilizer: it converts a
   frozen sale into a ground-lease conversion with the occupant in place.

**The other shocks, listed for the paper to work through.** Base
volatility (rent's cyclicality against a floor bill that is not; the
fund's smoothing role). Assessment at scale (auction capacity in a
downturn; the take-call's automatic trigger under stress). Collusion and
self-reporting (closed by the bracket, §3.2). The fiscal cliff of
payroll removal (the swap's revenue neutrality holds only at the
realistic base; the transition year needs the stock leg). The
sovereign-yield channel: a wage-based state's revenue elasticity to
automation is the source of its risk premium, and a rent-based state's
base has zero supply elasticity — a testable claim (announcement of a
credible rent-based system should *lower* the term premium; the
sovereign-yield reading is this paper's; the interest channel is the
dynamics paper's). Political capture of the bureau (automaticity is the
defense). Legal: the takings clause and its foreign equivalents — the
dial is also the constitutional instrument. International: the gate's
border adjustment and its trade-law status (DBCFT's history, to
verify); capital flight from the source tier (the cash-flow base is
origin-based unless border-adjusted — the DBCFT equivalence to work at
drafting). Regulated-rent jurisdictions (Sweden): where the price
channel is muted, recapture shows in queues and condo prices; how κ and
the loop read there.

---

## 10. Public goods, correction, objections, and what would count against the account

**Public goods (the corollary).** The purchases slice — army, academia —
is public goods, not transfers: the Henry George Theorem's home turf
(differential rents cover public-goods spending at optimal scale;
Arnott–Stiglitz 1979, live-verified in P1). The floor rides κ; purchases
ride the theorem; the two claims are disjoint and both live in tier 1's
world.

**Pigou discipline (T9).** A corrective tax that works erodes its own
base; budgeting core spending on it gives the state a fiscal stake in
the harm. Book the revenue as incidental, outside every rule in §8.

**Objections to pre-empt.** (i) "A uniform consumption tax is a wage
tax" — classically yes on leg one; the claim is legs two and three plus
the decay rate. (ii) "λ won't reach zero" — nothing waits on the corner;
the theorems are monotone path statements. (iii) Home production and the
informal sector escape the gate — the same leak payroll has; in-model it
is the s(q) enclosure margin. (iv) λ_C ↔ φ_w contested — bands and
all-variants discipline. (v) "Mirrlees already recommends this" — the
snapshot yes; the trajectory, the rate, and the terminal state are the
contribution. (vi) The political economy of 100% — P5's paper; cite.
(vii) "Why not DBCFT" — same family; work the equivalence. (viii) "This
is state ownership of land" — yes, in all but name, and the paper says
so in §3.2 rather than being caught saying it. (ix) "The source tier is
just a corporate tax" — no: it exempts the normal return by
construction, and its rate is set by the split rule, not by revenue.
(x) "The use split is arbitrary" — it is a rule with one free
parameter, the buffer, and an observable, the real yield.

**What would count against the account.** The wage-financed share of
consumption (φ_w's counterpart) failing to fall as λ falls. κ failing to
rise as q rises. A credible rent-based announcement that raises rather
than lowers the term premium. Conversion investment failing to raise the
measured ceiling. The gate's rate failing to fall on the clock in any
jurisdiction that adopts the pair.

---

## 11. Appendices (plan)

A. The algebra, mapped to the check files (T1–T12; S1–S17).
B. The napkin: 2025 accounts, the κ grid, the bundle costs, the rate
   tables under both closures, the market dashboard — all live-pulled,
   scripts vendored.
C. The scarcity inventory table with feasibility and effectiveness.
D. The precedents ledger — every regime named above, with its
   verification status.
E. The replacement map as a table, with revenue magnitudes.

---

## 12. Dropped, with reasons

- *The general valuation lag* (five-year, or ten-up/two-down). Leaks
  17% of rent to every holder in growing areas; opens the sawtooth
  under asymmetry; cannot close the fake dip; does nothing for the
  stock. Replaced by the bracket and short symmetric measurement lags
  (§3.2). Her *purpose* — rewarding discovery — survives as the licence.
- *The 2:1 rule.* Pegs the dividend to purchases; doubles the gate's
  rate; quadratic deadweight on the wage leg. Replaced by the fill order
  (§8.2).
- *40/60 as a target number.* Kept as the buildout-phase value of the
  four-piece rule (§6); the number itself makes no claim.
- *The foreign-scarcity fund as a pillar.* Restricted, explosive, and
  second in line behind the host state's own rent tax. Kept as a hedge
  and a smoother, sized by its case (§8.2).
- *Universal auction coverage.* Thin markets, structures, scale.
  Replaced by rolling sample auctions for identification (§3.2).
- *Capturing transitional rents on lagged inputs.* Time-inconsistent:
  an anticipated levy deters the build (imported). The commons table
  says "do not."
- *Any function for private title.* No pricing power, no usage rights,
  a 2% annuity: a transition object, named as such (§3.2).
- *Interest and normal returns as a source base.* The supply response
  is outside the model; the cash-flow base exempts them by construction
  (§5).

## 13. Deferred to the dynamics paper

The announcement-date theorem and the price-path table (this paper
cites the capitalization result and the dial). The build-lag markup
(g+δ)·v·(1+g)^J and the pipeline stock (this paper cites the 40%
instance). Horizon-relative terminality and the time-inconsistency of
taxing rents on lagged produced inputs (this paper cites "do not"). The
transitional-rent and windfall results (the fund's intergenerational
role cites them). The shock experiments and the shock ledger (this
paper's §9 lists the shocks and imports the responses). The interest
channel of the wage of waiting (this paper uses the market reading
only). If the dynamics paper lands with different names or scopes for
any of these, the imports paragraph in §1 is the single place to
reconcile.

## 14. Verify ledger (nothing enters a draft before live verification)

Diamond–Mirrlees 1971; Mirrlees Review (Tax by Design, 2011: the
rate-of-return allowance, the cash-flow base); Meade 1978;
Auerbach–Kotlikoff 1987; Auerbach–Devereux et al. on the DBCFT and the
2016 US proposal's history; Fischer 1980 and a capital-levies history
(Eichengreen); Collinson–Ganong 2018; Arnott–Stiglitz 1979 (verified in
P1); George 1879 (verified); Harberger self-assessment and Posner–Weyl's
common-ownership tax; Taiwan's land-value tax and Sun Yat-sen's design;
Amsterdam erfpacht, Hong Kong, Singapore, Canberra leasehold practice;
Denmark, Estonia, Pennsylvania split-rate; Norway's petroleum tax,
Australia's PRRT, Garnaut–Clunies Ross, the Brown tax; FCC spectrum
auctions; Singapore's certificate of entitlement; London, Singapore, and
New York congestion pricing; the EU ETS; New Zealand's GST and the OECD
C-efficiency figures; Hungary's rate; the auction-theory result on
rights of first refusal; Glaeser–Gyourko on the zoning tax; Kaldor's
saving closure; Kremer on prizes; Romer 1990 (verified in P1); Kim–Wright
term premium; Alaska's dividend fund and Jones–Marinescu (verified in
P1); Hoynes–Rothstein (verified in P1).

## 15. Decisions for her

1. Title. 2. Program placement (standalone consumed by P2/P5 vs P2's
spine), now with the sequencing after the dynamics paper. 3. Whether the
split is carried as the rule with the hump or as a fixed target. 4.
Which shocks get theorems (the swap, the bank pass-through) and whether
the shock ledger runs here or in the dynamics paper. 5. The discovery
window's term (ten years) versus cost recovery with uplift. 6. Whether
the match-right chilling problem gets a theorem or a citation. 7. The
dividend peg (P_s, per the fill order) — confirming the 2:1 rule's
retirement. 8. Lean depth, later.
