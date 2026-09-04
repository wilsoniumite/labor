# The mix on the way down — a practical design

**Memo, 2026-09-02.** Stella's questions of this date: (1) what scarcities
to capture beyond land and how; (2) which source taxes on non-land returns,
and what mix; (3) the same for the VAT; (4) all three over an automation
path; (5) the order in which existing taxes and benefits go; (6) the split
of revenue between the dividend, government spending, and a sovereign
fund; then (7) the expected shocks, starting with the land revaluation and
the banks; and (8) whether the model tracks the global rise in sovereign
yields and what a stabilizing plan looks like. Her frame: away from the
limit, with a healthy land tax that still cannot carry the floor alone
(κ ≈ 0.33), money has two uses, adapting/developing the economy and
consuming from it, 40/60 by hypothesis.

**What this memo inherits and what it adds.** The three tiers, the
ceiling, the grandfathering dial, the circular-flow discipline, and the
gate-tax convergence are `SKETCH.md` T1–T9 and are used, not re-argued.
New here (SKETCH §11): the use split as a saving constraint and the
source tier it names (T10), the wage-share clock on which the gate
retires (T10b), and the announcement date sized with its shock list
(T11). Arithmetic: `code/fiscal_napkin.py` → `data/` (live FRED through
link-repo's gated machinery, 2025 values, lower-bound rent
constructions). Algebra: `checks/check_split.py`, 12 green. Register:
memo, not paper prose; nothing here is voiced.

**Ratings.** Each instrument carries two words: *feasibility* — can we
actually have it (legal, administrative, political), her "exposure to
have" — and *effectiveness* — does it do the model's job: collect the
rent without moving a margin, or reach the base it claims.

---

## 0. The frame, once

Every unit of final spending resolves into wage claims and scarcity
claims (T1). A tax system chooses where to stand in that circuit: at the
scarcity source, at the consumption gate, or athwart an externality.
This session adds that the source tier has *two* bases. The cadastral
base is land, collected by the land tax. The non-cadastral base is the
rent the cadastre cannot see — pure profits, institutional rents on
ideas, transitional windfalls while capacity builds, market power — and
its natural instrument is a cash-flow tax that expenses reinvestment and
taxes distribution. Her 40/60 split is what pins that instrument's rate,
because the split is a saving constraint: investment is financed by
saving, so "40% into adapting" is the statement that accumulators keep
40% of income after tax. The gate cannot do this job (investment is
outside its base by construction; it preserves capital return, it cannot
ration it), and neither can the land tax alone (land is 3–5% of GDP).
The calendar follows: the gate carries the early transition, the source
tier the middle, the land tax the end.

Aggregates used throughout (2025, $B, `data/aggregates_2025.csv`): GDP
30,762; PCE 20,955 (68.1%); government purchases 5,275 (17.1%); gross
private investment 5,459 (17.7%) against economy-wide depreciation 5,065
(16.5%); social benefits 4,845 (15.8%: Social Security 1,573, Medicare
1,221, Medicaid 1,011, other ≈ 1,040); personal current taxes 3,234;
social-insurance contributions 2,019; corporate profits 4,078 (13.3%);
federal corporate tax 497; state and local property tax 789; wages plus
supplements 15,727 (0.511 of GDP). Household real estate 52,151, of
which structures at current cost 28,638 and the land residual 23,513
(45%, 0.76×GDP); home mortgages 13,643; federal debt 37,144 (121% of
GDP). Floor bills: 2,810 (9.1% of GDP) on the family-of-four bundle
($8,219 per person), 5,535 (18.0%) on the single-person bundle
($16,186). Measured site rents 993–1,655 (3.2–5.4% of GDP), median
1,186; κ median 0.326.

---

## 1. Capturing scarcity (her Q1)

### 1.1 The land tax's parameters, and the valuation mechanism

**98%.** Right idea, wrong justification if the 2% is meant as an owner's
"incentive": land needs none (T3). The 2% is an *error buffer*: an
assessment above true rent taxes the occupant's contribution and idles
the parcel, so the rate must sit below the assessment's error. The
practical consequence of 98% is that the land price falls to about 2%
of its capitalized value plus option value, and sales stop revealing r.
Assessment must therefore move off transaction prices — onto the
mechanism at the end of this section. At 98% every version of it
converges on the state as landlord in all but name; say so in the paper
rather than let the reader discover it.

**The lag — her two purposes, checked** (S8, S13–S16; the assessment
follows true rent by partial adjustment at speed 1/L, L_up on the way
up, L_down on the way down). Her proposal: an up-lag as a prospecting
reward, lengthened by preregistration ("we will prospect here": ten
years instead of two); a two-year down-lag so that "you can't get a
revaluation loophole"; abandonment then "fine," the state taking title
for the period.

1. *Prospecting.* The problem is real, and the sketch's ceiling
   argument is static: discovering that a site is worth more — minerals
   below, a use no one had priced — raises the next-best bid, which a
   100% tax at instant revaluation takes entirely, so no one looks. But
   a general up-lag is the wrong reward. It pays whoever holds the site
   when rent rises, discoverer or not, and in steady 2% growth a
   ten-year adjustment leaves *every* holder 17% of rent permanently
   (a two-year one, 4%; exact ratio (1+g)/(1+gL), S15) — a rate cut
   concentrated in the fastest-growing metros, where the unearned
   increment is largest. The right instrument is the mineral-tax one:
   preregistration as an exclusive discovery licence — a fee, a work
   commitment, relinquishment if idle — with a retention window on the
   *verified discovered increment*, the difference between post- and
   pre-discovery next-best-bid rent, never on general appreciation. Her
   ten years is a fine term; the alternative is cost recovery with an
   uplift (to verify against the resource-rent literature). Urban
   "prospecting" — finding a site's best use — needs no window at all:
   its reward is the untaxed structure. Free registration for everyone
   is the free-option trap: everyone registers and the lag is ten years
   for all.
2. *The down-lag and the loophole.* The loophole is the sawtooth:
   engineer a dip in measured rent, let the assessment fall, ride the
   up-lag while true rent recovers. At a 98% rate the owner's stake in
   the rent is 2%, so a *real* dip — withdrawing the site — costs almost
   nothing beyond the tax paid on the old assessment while the dip
   lasts; that cost is exactly what a down-lag creates, so her instinct
   is right. Her numbers are not: under (up 10, down 2) a real two-year
   dip still pays the owner 1.75 years of rent; under (10, 5), 0.5; it
   stops paying only near symmetry, (10, 10) or (2, 2), because the
   down-lag must be of the order of half the up-lag before the
   overpayment during the dip outweighs the underpayment during recovery
   (S13). And a *fake* dip — a low self-reported lease to a related
   party under income-based assessment, the true rent still received —
   pays under every lag structure, symmetric or not (S14). Lags cannot
   close it; only a valuation that ignores the occupant can (T3), which
   is what her auction and bureau supply below. Verdict: short
   symmetric lags for measurement only, two years both ways; no general
   up-lag; the discovery window separately.
3. *Abandonment.* Right in principle, wrong as stated. Surrender is a
   *put*: an owner assessed above market walks, so the tax can never
   exceed the rent — the 1.22 overshoot of a lagged assessment after a
   rent fall (S8) is capped at 1.00 (S16). That is a feature, and it is
   half of a valuation mechanism. It works only if what is surrendered
   is the *land*, the structure retained — surrender as conversion to a
   ground lease at the next auction's rent, occupant in place. If the
   structure goes with the title, an owner tolerates over-assessment up
   to the structure's annual value before walking, the put never bites
   on built parcels, and the state holds up improvements — T3(c)'s β
   problem by another route (S16b). Two more conditions: the state must
   re-let promptly (the interim is idling, and in a rent downturn
   surrenders arrive by the million — auction capacity is the binding
   constraint), and lenders must be neutral to it (after the tax the
   land collateral is near zero, so a structure-retained surrender does
   not touch the mortgage; a structure-forfeit one is a default). Under
   those three conditions abandonment is fine; it is the owner's side of
   the bracket below.

**The valuation mechanism — her auction and her bureau.** Her two
fragments — a state-run universal auction with anonymous bidders, and a
land bureau that catches collusion by buying undervalued land — are one
mechanism, and with the surrender put they close the assessment
problem (S17).

- *Rolling anonymous auctions as sampling, not coverage.* Auction the
  ground lease of a random rolling sample of parcels each year, sealed
  and anonymous — not every parcel. Universal coverage founders on thin
  markets (most parcels have no genuine second bidder), on structures
  (an outside winner must buy the building, which moves the valuation
  problem onto structures), and on scale. The sample identifies the
  rent surface and the assessment of un-auctioned parcels is
  interpolated from it: T3's "auction the leases and r(z) prices
  itself," done as a survey. The sitting occupant needs a right to
  match (else the β hold-up); a match right chills outside bidding
  (bidders know they lose to a match — the auction-theory point, to
  verify), so bidders need a reason to bid: a premium paid to the
  matched bidder, or a match right limited to a share of the increment.
  Open design question; candidate theorem.
- *The bureau is the state's take-call, and it must be automatic.* When
  a parcel leases or trades below the assessment by more than the
  buffer, the state takes the lease at that price and re-lets it.
  Colluding bidders cannot obtain the parcel cheaply, because the state
  takes it; a self-reported low rent forfeits the parcel, so the fake
  dip dies (S17b). Precedents to verify: Sun Yat-sen's design in
  Taiwan's land-value tax (self-declared values with a state purchase
  right at the declared value) and the Harberger self-assessed tax with
  a standing purchase option. The one design rule that matters: the
  trigger is automatic — clearing price below assessment minus buffer,
  no discretion — or the bureau becomes the corruption locus; and its
  purchases carry a re-letting obligation, so it never becomes a land
  bank. Its tolerance band is the error buffer, the 2%.
- *The bracket.* The owner's put caps the tax from above at the rent;
  the state's call floors realized rent from below at assessment minus
  buffer. Between them the effective rate on true rent lies in
  [0.98(1 − b), 1] — [0.96, 1.00] at b = 2% (S17). Assessment error is
  bounded in both directions by options rather than by lags; the lag's
  only remaining job is measurement, and prospecting has its own
  window.

**Who sets the rent, and who manages usage** (her follow-up: "title
gives no rights to manage usage ... holders have only one incentive:
set the highest rent that doesn't cause a user to flee"). The incentive
she names is T3(b)–(c)'s pathology stated from the holder's side. "The
highest rent that doesn't cause the user to flee" is the user's
reservation value, which exceeds the next-best bid by the user's sunk
stake — structure, relocation cost, match value — so a holder acting on
it taxes the occupant's contribution, and improvements fall (e*(β)
falling in β). The mechanism therefore takes pricing away from holders
altogether: the rent is the auction-identified next-best bid and the
bracket enforces it. A private "title" is then a claim on 2% of a rent
someone else sets, on a parcel whose use someone else chooses; it has
no function beyond the transition (an annuity to former owners, the
error buffer's residual claimant). The paper should say so: this is
state landlordism, and "title" is a name. Usage management does not
vanish; it migrates. To the *user*: improvement incentives need long
leases, renewal rights, and compensation for improvements at lease end
— the β = 0 condition — or the leasehold dilapidation problem appears
(to verify against Hong Kong, Singapore, Canberra practice; Amsterdam
erfpacht is already on the list). To the *auction*: land assembly needs
bundle bids, or the state assembles. To the *state*: externalities,
zoning, covenants against depletion and contamination — so the state as
ultimate landlord keeps usage rights, and "no usage rights" is a
statement about private holders. The one productive incentive a
landlord has — raising the next-best bid by improving the site or
matching it to its best user — is worth 2% to a holder and 98% to a
state that lacks the local knowledge; hand it to the user through the
lease.

Ratings. Rolling sample auctions: feasibility medium (cadastre
digitization; the match-right design), effectiveness high
(identification). The automatic take-call: feasibility medium
(precedents exist; automaticity is the political fight), effectiveness
high (kills collusion and self-reporting). The surrender put:
feasibility high, effectiveness high *only* structure-retained. As a
stock shock absorber the lag remains useless: a credible permanent rate
is capitalized at announcement whatever the assessment lag (T4, §7).

**Overlap.** The state and local property tax already collects $789B
(2.6% of GDP), partly on land; its structure half is the part to abolish
(§5), its land half is continuity. Net new land-tax revenue is smaller
than the $1.0–1.7T gross figure by that overlap; not netted here.

### 1.2 Other scarcities

| Scarcity | Instrument | Feasibility | Effectiveness | Model note |
|---|---|---|---|---|
| Land (cadastral) | land tax at 98%, rental-basis or auction assessment | medium: assessment, and the announcement shock (§7) | high: ceiling 100% is definitional (T3) | the base; 3–5% of GDP today, rising with q |
| Minerals, oil, gas | resource-rent tax on the cash flow above cost; auctioned leases with periodic rentals | high: precedents (Norway's petroleum regime, Australia's PRRT, US federal leasing — to verify) | high | tier 1 already in practice; the US anomaly is private subsurface rights |
| Spectrum | recurring rentals on auctioned licences instead of one-time sales | high: FCC auctions exist | high | convert stock sales to flow rentals (T4's logic) |
| Water rights | tradable rights with an annual rental, auctioned where unallocated | low–medium: prior-appropriation politics | high where scarce | the exit bundle's water is in h_e |
| Transmission, interconnection, grid capacity | auctioned queue positions; public capture of congestion rents now paid to FTR holders | medium | medium | horizon-terminal (App A); see the windfall row |
| Permits, zoning, licences (artificial scarcity) | auction the permit (the Singapore vehicle-quota model, to verify), or abolish the scarcity | medium | high | supply expansion is the stabilizer (§11 of P1); prefer abolition |
| Congestion: roads, airports, slots, orbits | congestion charges, slot auctions | high: London, Singapore, New York | high | T8: tier 1 administratively, tier 3 where congestion is the externality |
| Atmosphere (carbon) | carbon price | medium–high | high | tier 3, booked as incidental (T9), never as core revenue |
| Ideas and IP | shorter and narrower terms; royalty withholding at source; the cash-flow tax gets the rest | medium | medium | institutional scarcity, policy-elastic (P1 §3); the creation-cost incentive bounds the rate |
| Market power, platforms | the cash-flow tax (§2) | high | medium–high | pure profit is rent in the model |
| Transitional windfalls (capacity build lags) | **do not tax ex post**; public co-investment ex ante where the state wants a share | — | — | anticipated windfall taxes on lagged inputs are time-inconsistent and deter the build (P1 v2 dynamics: input-j windows) |
| Agglomeration | nothing separate | — | — | already in land values |
| Residence rights | visa auctions | low | medium | the scarce right to be inside a high-rent jurisdiction; mention, do not build on |

Three groups. *Do now*: resource rents, recurring spectrum rentals,
congestion pricing, carbon as tier 3 — precedented, clean, real revenue
but not core-budget scale (T8). *Design*: water, interconnection,
permits, IP terms — feasible with reform, each with a concentrated
incumbent who holds a capitalized right (grandfather the increment, as
with land, §7). *Do not*: ex-post windfall taxes on lagged produced
inputs, general "excess profits" levies, and foreign land (§6). The
cadastral base dominates the scale; the rest is tidiness and
information.

---

## 2. Source taxes on non-land returns (her Q2)

### 2.1 Why the split needs one

Under the classical closure — wages and the dividend consumed, non-land
returns reinvested — I/Y = 0.4 requires the after-tax non-land share
kept by accumulators to be 0.4: t = 1 − 0.4/(s·π), s the reinvestment
fraction, π the gross non-land capital share (S1). Today π ≈ 0.42, so
t ≈ 5%: the split is essentially self-enforcing at today's factor split
*if* owners reinvest what they keep. They do not: gross private
investment is 17.7% of GDP against a 42% gross non-land share, so about
half of gross capital income returns as investment and the rest is
consumed or taxed to fund today's state. Under that observed closure the
split is not reachable by leaving returns with owners at any rate; the
state has to invest the gap itself, 0.4 − sπ ≈ 0.19 of GDP today, and
the gate cannot carry it (§4). Either way the instrument that enforces
"reinvest, don't consume" is a tax at source that *exempts* reinvestment
and *taxes* distribution — which is exactly a cash-flow tax.

### 2.2 The menu

| Instrument | Base | Feasibility | Effectiveness | Verdict |
|---|---|---|---|---|
| Cash-flow corporate tax (R-base; R+F to reach finance), full expensing, refundable losses | pure profits and rents; the normal return is exempt by expensing | high: expensing exists in US law; refundability is the missing piece; DBCFT was proposed in 2016 (to verify) | high: reaches non-cadastral rents at source, saved or consumed | **the workhorse.** Rate on distributions set by the yield target t·π = 0.6 − w − r_L |
| Rate-of-return allowance at the personal level | capital income above the normal return | medium: Norway's shareholder tax is the precedent (to verify) | medium | integrates with the cash-flow tax; exempt the normal return |
| Tax on interest or the normal return | ρ, the wage of waiting | high: exists | negative | do not: it taxes the build the split is trying to protect |
| Wealth tax | the stock of everything | low: valuation, flight, widely repealed | low on non-land | the land tax is the wealth tax that works; skip |
| Estate and inheritance tax | inherited rent claims | medium: exists; avoidance | medium | the ownership distribution ω_ij in prop:welfare is inherited; the stock-side complement to the dial |
| Financial activities tax | financial-sector rents | medium | medium | fold into the R+F base rather than a separate tax |
| Payroll and personal income tax on wages | wages | high: exists (φ_G = 0.68 of revenue) | negative under the model | retire (§5) |

### 2.3 The mix

Cash-flow tax as the workhorse, rate on distributions rising along the
path (§4) and thinning with the base in the limit, where reproducible
capital is competed to cost and the value migrates into land; a
rate-of-return allowance at the personal level so the normal return is
taxed once, at zero; an estate tax on rent-claim stocks as the
intergenerational complement; no wealth tax, no interest tax. Scale
check: corporate profits are $4.1T (13.3% of GDP), the visible part of
π; federal corporate tax collects $0.5T. The split needs the source tier
to yield 0.02 of GDP today, 0.10 at a 0.45 wage share, 0.18 at 0.35,
0.26 at 0.25 — a tax that starts near nothing and grows with the base
it taxes. Origin-based at first; the destination-based variant has a
trade-law problem (§7.2) the VAT already solves on the consumption side.

---

## 3. The VAT (her Q3)

**Design.** Credit-invoice (the chain enforces itself; the reason a VAT
outcollects a retail sales tax), destination-based (reaches the ~9% of
consumed production that is foreign content), uniform rate, broad base,
no reduced rates — the dividend is the progressivity (T6: flat gate plus
flat dividend gives rising average rates), and every zero-rating is a
hole the dividend fills better. Housing: exempt residential site rent,
because with the land tax at 98% a VAT on land services is a relabel
(fixed supply: the consumer price is demand-determined, the producer
rent falls one-for-one, the state's total take is unchanged; S6), and
tax new structures at sale as the present value of structure services,
the standard treatment. Financial services through the R+F cash-flow
base, not by exemption. New Zealand's near-uniform GST is the reference
design; the typical OECD VAT collects on the order of half of what a
uniform rate on all consumption would (to verify at drafting); the rate
tables below carry both efficiencies.

**Rate.** A residual: the funding need not met by the rent tier and the
source tier, divided by the base. Today, carrying the floor residual
only: 8% tax-exclusive on the family bundle at full efficiency, 13% at
the realistic base; 21% and 35% on the single bundle
(`data/vat_residual.csv`). Under her split the base shrinks to 0.46 of
GDP and the rate rises to 39% (family floor, full reinvestment) — above
the practical ceiling any VAT has held (the highest standard rates in
the OECD sit in the high twenties; to verify), so the split cannot be
fully gate-funded today; the shortfall is the source tier's job or the
transition deficit's.

**Over time.** The rate falls with the wage share and reaches zero at a
wage share of 0.37 (family floor) or 0.28 (single floor), S4: below
that, land plus the source tier already cover government consumption and
the floor. The schedule should be announced and monotone-declining: a
rising consumption-tax rate taxes waiting (consuming later costs more),
a falling one subsidizes it; a declining announced path is the one that
does not move the intertemporal margin against the build.

**Ratings.** Feasibility: medium — the United States has no federal VAT,
the single largest "exposure to have" gap in the whole design; state
sales taxes (about 2% of GDP) fold in. Effectiveness: high on goods
through the invoice chain; weak on cash services and the informal
sector — the same leak payroll has, and in the model the s(q) enclosure
margin (SKETCH objection iii). The distortion is the wage-tax distortion
on the labor-financed slice of the base, φ_C ≈ 0.64 today and falling.

---

## 4. Over time (her Q4)

Stylized path: wage share 0.55 → 0.15; κ 0.33 → 1.26 (the ceiling grid's
median); the floor held at the family bundle (0.091 of GDP) and
government consumption at 0.14. The land tax's yield rises from 3.0% to
11.5% of GDP along it. Full reinvestment first
(`data/split_schedule.csv`):

| wage share | κ | land tax yield | source tax rate (yield) | VAT excl./incl. | surplus |
|---|---|---|---|---|---|
| 0.55 | 0.33 | 0.030 | 5% (0.02) | 39% / 28% | — |
| 0.45 | 0.50 | 0.046 | 21% (0.10) | 18% / 15% | — |
| 0.35 | 0.75 | 0.068 | 31% (0.18) | 0 | 0.02 |
| 0.25 | 1.00 | 0.091 | 39% (0.26) | 0 | 0.12 |
| 0.15 | 1.26 | 0.115 | 46% (0.33) | 0 | 0.22 |

Under the observed half-reinvestment closure the source tax sits at zero
throughout (owners cannot reach 0.4 even untaxed), public investment
carries 0.19 → 0.03 of GDP, and the VAT needed to fund it runs
85% → 32% tax-exclusive (46% → 24% inclusive): infeasible at the front.
The two closures bracket the truth, and the bracket is the finding: the
split is cheap to enforce on accumulators who accumulate and impossible
to enforce through a consumption tax on accumulators who don't.

Three stages, then. **Stage 1 (wage share above ~0.45):** the gate
carries; the source tier is small; the land tax is continuity plus the
structure-tax abolition. **Stage 2 (0.45 → 0.37):** the gate declines,
the source tier rises past 20% of non-land returns, κ passes one-half.
**Stage 3 (below 0.37):** the gate retires (T7's convergence, now with a
date); the source tier peaks and then thins as reproducible capital is
competed to cost; the land tax carries and a surplus appears that lifts
the dividend above the floor. P1's D = φ_C(1−κ)² index falls along the
whole path, as T7(ii) says it must. Two stylizations to state in the
paper: the floor's share of GDP is held fixed, while in the limit it
rises toward 1/κ_max as all value migrates into land; and κ's path is
pinned to q, so the calendar is in wage-share time, not years.

### 4b. What determines the split: a rule, not a number (T10c)

Her two points, taken as given: the 40/60 is arbitrary; and even at the
capability limit the dynamic extension (durability δ, waiting ρ, build
lags J) relaxes instantaneous free entry, so capital expenditure never
stops — machines must be maintained and shocks met. The question
underneath is "how much adaptability and expansion do we need, and how
much can we just sit and enjoy what we have?" The answer the model
supports: the split decomposes into four pieces with four different
determinants, only one of which is a choice. Data:
`code/split_determinants.py` → `data/split_determinants_*.csv`; algebra
S9–S12.

**The decomposition.** I/Y = replacement + machine expansion + terminal
conversion + buffer.

1. *Replacement — "sit and enjoy what we have."* δK/Y, measured:
   consumption of fixed capital is 16.5% of GDP in 2025, up from 11.1%
   in 1950. It is a floor, it is measured, and it is rising, because the
   capital stock's composition shortens (equipment, software, IP; part
   of the rise is NIPA's 2013 capitalization of IP — caveat). A
   datacenter-heavy stock (δ near 25%) raises it further. Her instinct
   to read this piece off depreciation is right, with two caveats:
   economic depreciation includes obsolescence, so it contains
   adaptation and over-states pure maintenance; and the composition is
   endogenous to the split — what you build sets what you must replace.
   In the limit the piece never vanishes while b > 0: it is the machine
   sector's land bill, b·r(ρ+δ)/(1 − a(ρ+δ)) (App A).
2. *Machine expansion.* Demand-determined: free entry prices machines at
   cost, so no policy sets this piece; it is whatever tasks and land
   demand at cost. Its *value* share goes to zero on the path (prices
   → 0) while its physical scale explodes. Most AI capex is this piece,
   and most of that is replacement (short lives).
3. *Terminal-input conversion.* The public, lumpy, long-lived, high
   capital-output investment that raises the κ ceiling — housing
   density, energy capacity, transmission, water. If anything carries a
   40% share it is this: at v ≈ 12 and δ ≈ 1.5%, even 2% growth needs
   42% of output gross (the build-lag table), and it is the piece the
   golden rule governs — convert until the marginal rent yield equals ρ
   (S12). Its market signal is the land residual itself: $23.5T is the
   price of conversion not made, and the metro dispersion of land shares
   (a data item to build) reads how much of it regulation could
   dissipate.
4. *Buffer — resilience against shocks.* The piece she asks whether the
   market can price. Partly: see below. It is a *stock* (reserves,
   reserve margins, the fund of §6), whose flow cost is the carry.

**What the data say now — the finding.** Gross investment, private plus
public, has held at 21–23% of GDP in every decade since 1950. The
replacement floor rose from 11% to 16.5%. Net investment therefore fell
from 11% to 5%, and public net investment from 3% of GDP in the 1950s–60s
to 0.8% in the 2020s. The United States has been answering her question
with "sit and enjoy" for seventy-five years in net terms, and the line
that vanished is the terminal-conversion line — the κ-ceiling lever is
the starved one. Her 40/60 is therefore not "more of the same": it is
1950s net accumulation (11%) on top of a floor that has risen five
points, plus a conversion pipeline. The build-lag identity
I/Y = (g+δ)·v·(1+g)^J (S9) puts 40% at 5% growth with a five-year
pipeline at economy-wide capital intensity, or at 2% growth in the
conversion sector alone; today's 21% is 2% growth with no pipeline.

**Reading it off the market — what can and cannot be read.** Latest
against 2021, the 2010s, and the full sample: 10-year TIPS real yield
2.44% (−0.91 / 0.42 / 1.00); term premium 0.88 (−0.16 / 0.22 / 0.82);
10-year breakeven 2.35 (2.36 / 1.99 / 2.11); Baa spread 1.59 (1.95 /
2.59 / 2.27); VIX 16 (20 / 17 / 19). Inflation expectations are where
they were in 2021, credit risk is low, equity fear is low, the term
premium is back at its long-run mean — and the real rate is up 3.35
points, the one extreme. The market is not pricing a crisis premium; it
is pricing a higher required return on waiting: ρ has risen. In the
model's terms, saving supply is short of investment demand at the old
price. The bond market is answering her question — the split wants to
move toward adaptation — and it will move it the expensive way (crowding
out consumption and the state, §8) unless policy moves it the cheap way
(the source tier exempting reinvestment; public conversion). The TIPS
yield is thereby the observable for any split rule: set the split, and ρ
is the market's verdict on whether saving supply matches it.

What markets can price: insurable, diversifiable, near-horizon risk.
Catastrophe-bond spreads price physical shocks, and insurance *retreat*
(Florida, California, to verify) is the market declining to price — a
direct reading of adaptation not made. Energy futures volatility and
backwardation price terminal-input shocks. Sovereign spreads and term
premia price the fiscal base. Tobin's q by sector says where the market
wants capital; capex-to-depreciation ratios reveal the replacement-
versus-expansion split firm by firm. What markets cannot price:
systemic, uninsurable, long-horizon, and policy-endogenous risk (a
credible plan lowers the premium — §8's testable claim). Market reads
are therefore a lower bound on the buffer. The complement is ours: the
dynamics engine (P1 v2, `the-link-revision/code/dynamics/`) already runs
shock types (T5: frontier extension versus efficiency deepening); a
*shock ledger* would add a b-shock (energy — this week's), a T-shock
(land loss, climate), an N-shock (demography), and a G-jump (war), and
read off each the investment response, its timing through J, and who
bears it. That is the crisis-scenario modelling, on the existing engine.

**Trajectories, in value shares.** Today 21% gross, 5% net. A buildout
phase at 30–40% while the conversion pipeline fills over J years and the
short-lived AI stock turns over. Then decay toward replacement plus
growth. In the limit the value share of investment tends to the
production-land share 1 − α, which tends to zero when σ < 1 (S11):
everything is "enjoying," because what is had is land services and free
goods; replacement never stops physically, but its value is the machine
sector's land bill. The split is a hump — 21 → 40 → replacement-only —
and 40/60 is its peak, not a steady state. Variants: a permanently
high-δ stock keeps the gross floor near 25% with nothing net; war or
climate produce jumps funded from the buffer and the source tier.

**What she is missing — the list.** (a) Depreciation is endogenous to
the split's composition and rising. (b) Obsolescence versus wear: CFC
over-states pure maintenance. (c) Population: the ceiling T/(N·h_s) and
the conversion need scale with N; demographic decline is the cheapest
adaptation there is (Japan, Korea), and the long-record thread's φ is
the parameter. (d) Public versus private inside the 40: conversion
assets are natural monopolies with long J — public; private reinvests
half of gross returns (§2). (e) Human adaptation — retraining, education
— is consumption in the accounts and does not move the fork in the
model; it belongs in the 60, a call the paper should make out loud.
(f) Defense is the largest historical adaptation line (3% of GDP in
peace, 30–40% in war economies); war, not weather, is the crisis
scenario that sizes the buffer. (g) The buffer is a stock; only its
carry is a flow. (h) The split must be stated in physical or hours
terms, or as a share of land rent — not in money — because the value
share of machine investment goes to zero on the path. (i) The state's
own balance sheet: with the land tax the state is the residual claimant
on conversion, so public conversion is self-financing at the margin —
the Henry George theorem's dynamic form. (j) The real rate is the split's
price; the rule needs no other target.

**The rule.** Replacement as measured (δ by composition) + machine
expansion as demanded (no policy) + conversion to the golden rule
(marginal rent yield = ρ, read from the land residual and its
dispersion) + a buffer held as a stock, sized at the larger of the
market-priced and engine-modelled shock ledger — with the source tier's
rate set to leave exactly that in accumulators' hands and the state
investing the conversion piece. The rule gives 40/60 at 5% growth with a
five-year pipeline, 25/75 at 2% growth with none, and replacement-only
in the limit.

---

## 5. The order of removal (her Q5)

Principles, in the model's terms: (i) wage-linkage first — the
distortion is on the work–exit margin, and φ_G = 0.68 of revenue sits
there; (ii) base overlap — a tax goes when the new instrument stands on
its base; (iii) benefits with Δ ≠ 0 (work- or means-conditioned) go into
the dividend, which is the unique zero-wedge design (App C.1); (iv)
promises are honored by grandfathering, never by default; (v) in-kind
human-essential provision stays (App D: care hours are in the floor
bundle and their value share rises).

**Taxes.**

- *Stage 0, the announcement year:* property tax on structures to zero
  (the land tax stands on the land half; local finance replaced by
  formula, §7); corporate income tax converted to cash-flow (expensing,
  refundability, no interest deduction) — a conversion, investment-
  promoting, first; the VAT introduced the same day as the dividend at
  the floor, with state sales taxes folded in. Note the introduction
  step is the one-time levy of t/(1+t) on accumulated wealth (T4/T6 leg
  three) — the one instrument reaching escaped stock; announce it as
  such, do not "compensate" it broadly.
- *Stage 1, gate revenue online:* social-insurance contributions
  ($2.0T, the purest wage tax) to zero; Social Security accruals closed,
  accrued benefits grandfathered and paid from general revenue by
  attrition; the dividend replaces means-tested cash (SNAP, SSI, TANF,
  the EITC, the unemployment-insurance floor) — Δ = 0.
- *Stage 2, wage share below ~0.45:* personal income tax on wages
  retired (keep a surtax on the top of the labor distribution only if
  politics requires; the model gives it no job).
- *Stage 3, wage share below ~0.37:* the VAT itself retires; the source
  tier and the land tax carry.
- *Keep:* excises on externalities (tier 3, booked incidental, T9);
  public-goods purchases (the Henry George corollary); health as in-kind
  provision.

**Benefits.** Means-tested cash first (they are the withdrawal-band
traps that widen as wages compress toward the floor); housing vouchers
when supply expansion lands (vouchers are captured by rent, T5's
evidence item); Social Security by attrition; Medicare and Medicaid
never — they are the human-essential floor content the dividend cannot
buy at a fixed price.

"If at all": the model is unambiguous on the wage-linked taxes and the
conditioned cash benefits; it is silent on the earnings-related pension
promise, which is a fairness question the grandfathering dial answers;
and it says the in-kind human-essential slice grows.

---

## 6. Dividend, government, sovereign fund (her Q6)

**The fill order.** (1) The floor P_s, κ of it from land, the rest from
the gate and the source tier while needed. (2) Government consumption at
roughly today's 14% of GDP — public goods at the Henry George scale plus
the in-kind human-essential floor, whose value share drifts up (Baumol,
App D). (3) Public investment aimed at the κ ceiling: the public part of
the 40%, spent on converting horizon-terminal inputs into produced ones
— housing density, energy capacity, transmission — because that is the
only investment that moves the fiscal constraint (the ceiling's median
is 1.26, with 13 of 32 grid members below one, where the floor is
physically unreachable at any rent); the machine buildout needs no
public money, free entry prices it at cost. (4) A buffer fund. (5) The
dividend above the floor, from the surplus that appears below a wage
share of about 0.35.

**The sovereign fund, three cases.** *Domestic scarcity:* redundant —
the state as 98% rent collector already owns the domestic scarcity base
in all but title (T3); a fund holding domestic land would be the
cadastre with a brokerage. *Foreign scarcity-exposed assets* (her
proposal): three problems. Host governments have first claim on their
own rents — the model turned outward — so a foreign-scarcity fund is a
bet on the hosts' under-taxation, which the same model predicts they
will correct; foreign land ownership is restricted in most jurisdictions
(to verify country by country); and the optics are land-grab optics.
Feasibility low–medium, effectiveness contingent. Resource-company
equity is the tractable form and inherits the same first-claim problem.
*Smoothing and windfall conversion:* the real case. Site rents are
volatile — the Z.1 members of κ fell from 0.38 in 2006 to 0.13 in 2011
(`link-repo/data/kappa_results.csv`) — and a floor that is debt-financed
in every downturn is what §8 is about; transitional windfalls the state
takes ex ante (public co-investment, not ex-post taxation, §1.2) are
one-time and belong in a fund that spends its real return. Size by the
job, not by a share: one to two years of the floor bill ($3–11T) as the
buffer, plus the present value of the ceiling shortfall for the members
below one, funded from the Stage-3 surplus and from windfall captures
— not from today's revenue, where there is no surplus to fund it with.

---

## 7. Shocks and stabilizers (her Q7)

### 7.1 The announcement date: land, mortgages, banks

**Sizing** (`data/lvt_shock.csv`). The household land residual is
$23.5T, 45% of household real estate, 0.76×GDP (P1's lower-bound
construction, with its post-1995 caveat). A credible permanent 98% rate
removes 98% of it on the announcement date (T4: stock and flow are one
object at two dates). Home mortgages are $13.6T. Aggregate loan-to-value
goes from 26% to 48% when the land price goes to zero — survivable in
aggregate, catastrophic in the tail: a recent buyer at 85% LTV in a
metro where land is 65% of value is 60% underwater the next morning.

| Design | Land price after / before | Stock loss |
|---|---|---|
| Full capture, immediate | 0.02 | 98% |
| Phase-in, 5 years | 0.07 | 93% |
| Phase-in, 10 years | 0.14 | 86% |
| Phase-in, 20 years | 0.25 | 76% |
| Phase-in, 30 years | 0.34 | 66% |
| Increment-only (grandfather the announcement-date rent) | 0.60 | 40% |

Phase-in barely works on the stock because the present value sits in
the tail; grandfathering the current rent level caps the stock loss at
γ/δ = 40% (T4's dial, S7c) while the flow still arrives with growth.

**What breaks.** Sellers cannot clear their mortgages, so transactions
stop, and with them the price signal assessment needs (§1.1).
Construction lending stops. Bank mortgage books, mortgage-backed
securities, and covered bonds reprice on collateral; the double trigger
(negative equity plus an income shock) turns paper losses into defaults.
Commercial real estate takes the same hit on a smaller base. Local
government loses $789B of property tax. Pension funds and REITs holding
land mark down.

**The toolkit, rated.**

1. *Grandfather the announcement-date rent* (increment-only capture).
   Feasibility high; effectiveness high on the bank shock; cost: 60% of
   the stock forgone, the flow's growth still fully captured. The
   cleanest single lever the model offers.
2. *Phase-in* (including her five-year lag). Feasibility high;
   effectiveness low on the stock, useful only as cash-flow relief.
3. *Route the loss where it is designed to land.* The stock loss is
   unavoidable given the flow tax; the question is only whether it
   arrives through defaults or through the state's balance sheet.
   Statutory write-down of mortgage principal to the structure value,
   lender losses absorbed by state recapitalization (equity stakes),
   the state's compensating asset being the rent flow it now collects —
   one transfer, landowners to state, with banks as pass-through.
   Feasibility medium (contracts-clause and precedent questions; the
   Nordic 1990s bank resolutions and post-2008 principal write-downs are
   the cases to verify); effectiveness high. With option 1 in place the
   write-down is 40% of the land share, not 98%.
4. *Deferral lien for owner-occupiers.* The tax accrues with interest
   against the parcel, paid at sale or death. Feasibility high
   (property-tax deferral programs exist, to verify); effectiveness
   medium — a cash-flow fix for the house-rich and cash-poor, not a
   stock fix.
5. *Sequencing.* The dividend flows before the land tax bites, so
   household cash flow improves before the asset shock lands; announce
   the grandfathering with the tax, on the same day.
6. *Central bank.* Lend against structure collateral; the collateral
   collapse is deflationary while the VAT step (§7.2) is inflationary
   once — sequence the two inside one announcement window so the
   price-level effects offset.
7. *Compensation logic.* An owner-occupier holding less than the
   per-capita share of land is a net gainer over a lifetime — the asset
   goes, an equal share of all rent arrives — so compensation targets
   only over-leveraged recent buyers and land-heavy portfolios, never
   the top of the land distribution.
8. *Local government.* Replace the property tax with a formula share of
   the land tax; the assessment function centralizes into the cadastre.
   Feasibility medium; a real loss of local fiscal autonomy, to state
   plainly.

### 7.2 The other shocks

- *Assessment error and idling.* T3's buffer is 2% at a 98% rate — thin.
  Rental-basis assessment, auctions, and a cap at market rent; the lag
  only as a floor (§1.1).
- *The VAT step.* A one-time price-level jump of t/(1+t): 20% at a 25%
  rate, the Auerbach–Kotlikoff levy on old wealth (T4). Announce it,
  index the dividend, let the central bank look through it; it is the
  point, not a side effect.
- *Housing supply.* Land banking dies (good); homebuilders whose balance
  sheets are land appreciation break — a transitional construction
  credit facility, not a bailout of the land position.
- *The pension transition.* Grandfathering Social Security accruals
  costs about 5% of GDP a year for decades; it is funded from the gate
  in Stages 1–2 and is the intergenerational fairness question the paper
  should state as a choice, not solve.
- *The border.* A destination-based cash-flow tax invites retaliation
  (the DBCFT's known problem); take origin-based at first and let the
  VAT do the destination work.
- *Participation.* The Δ = 0 result says no compensated wedge; the income
  effect is small in the evidence P1 cites (Hoynes and Rothstein; Jones
  and Marinescu). A small shock; monitor.
- *Rent-price feedback of the dividend.* T5: second-order at h ≈ 0.62 —
  a 10% rent rise lifts κ about 3.6%; the loop cannot pass the
  land-per-head ceiling.
- *Commons repricing.* Spectrum, water, and permit auctions each have a
  concentrated incumbent holding a capitalized right; grandfather the
  increment exactly as with land.
- *Sovereign yields.* §8.
- *Political economy of 98%.* P5's paper; cite, do not absorb.

---

## 8. Sovereign yields (her Q8)

**The facts.** On 2026-08-31 the 30-year Treasury yield was 5.25% and the
10-year 4.75% (FRED DGS30, DGS10), against 2021 averages of 2.06% and
1.45%. The press on 2026-09-01 reports the 30-year above 5.3%, the
highest since 2007; the UK 30-year at 5.89%, highest since 1998, and the
10-year gilt above 5.2%, last seen in 2008; Japan's 10-year at 3% for
the first time since 1996 with the 30-year near a record 4.19%; France's
10-year at 4.9%, highest since 2008; German long yields at 2011 highs.
The drivers named are fiscal deficits, sticky inflation, and this week's
US–Iran flare-up pushing energy prices and rate-hike expectations. Only
the US legs are verified against a primary source here; the rest are
press figures, to verify before any draft
([Bloomberg](https://www.bloomberg.com/news/articles/2026-09-01/why-government-bond-yields-are-rising-and-causing-alarm),
[CNBC](https://www.cnbc.com/2026/09/01/bond-yields-iran-inflation-treasurys-japan-uk.html),
[Nikkei](https://asia.nikkei.com/business/markets/bonds/long-term-yields-in-us-japan-europe-soar-to-highest-in-years),
[Morningstar](https://www.morningstar.com/bonds/global-bond-selloff-extends-rate-hike-expectations-grow),
[WEF](https://www.weforum.org/stories/financial-and-monetary-systems/why-global-bond-market-treasury-yields/)).

**Does the model track it?** Three channels, in descending order of how
much the model actually says.

1. *The fiscal base, priced.* Revenue is 0.68 wage-linked on a base the
   model says shrinks; obligations rise as wage income falls; and the
   gap is being bridged by debt — P1's borrowed channel, 19% of
   transfers debt-financed by 2025 (fig_fourway). A term premium is the
   market pricing a state on a shrinking base with rising claims and no
   announced base migration. This is the model's strongest connection
   to the yield rise, and it is global for the same reason the labor
   share's fall and the rise of housing rents are global (Karabarbounis
   and Neiman; Knoll, Schularick, and Steger). What the model rules out
   as remedies: austerity (it cuts the floor while the wage base keeps
   shrinking) and inflation (a levy on bondholders — a badly targeted
   capital levy, T4's language).
2. *The wage of waiting under a buildout.* ρ is a parameter, so the
   model does not predict the level of rates. But the sequence economy
   (P1 v2, Appendix E: build lags J, the user cost u_K) says a capacity
   buildout with lags raises the demand for waiting, and the datacenter
   and power buildout is the model's horizon-terminal inputs being built;
   with inelastic saving, ρ rises. Direction consistent, magnitude
   outside the model. Two interactions worth stating: a higher ρ raises
   the machine rental (user cost ρ + δ), which supports the wage at the
   margin and slows the fork — a high-rate world *delays* automation's
   wage effect; and it lowers land prices (r/(ρ − γ)) without touching
   rents, shrinking the announcement shock of §7 — the 0.76×GDP figure
   is at a 4.3% ten-year, and at 2021's 1.45% it would have been two to
   three times larger. The current yield regime is, perversely, the
   cheapest moment to announce a land tax.
3. *Energy as a terminal input.* This week's trigger is an energy-price
   shock; P1 classifies energy capacity as terminal over years; a rent
   spike on a terminal input is what raises q and lowers the exit value
   in the model, and central banks answer it with ρ. Consistent, but
   generic.

What the model does not say: the size of the term premium, whether real
rates or inflation expectations carry it, or anything about Japan's
particulars.

**A stabilizing plan.**

1. *Base migration as term-premium policy.* Announce the rent tier and
   the gate with the schedule of §4. The revenue base becomes one that
   rises with q — κ went from 0.05 to 0.33 in seventy years — the
   opposite of the wage base. The paper's testable claim: an announced,
   credible migration compresses the term premium.
2. *Rent-backed debt.* The capitalized rent flow is $23.5T at current
   cap rates, 63% of federal debt ($37.1T). The state can issue
   land-rent-linked bonds — a consol whose coupon is a share of the land
   tax take — or pledge the flow, converting general-obligation debt
   into rent-backed debt. It recapitalizes the sovereign on the same
   date the private land stock is written down: the mirror image of §7.
   Feasibility medium (a novel instrument; market depth); effectiveness
   high.
3. *Fund the transition explicitly.* Stop bridging the (1 − κ) gap
   through the borrowed channel; the gate's Stage-0 introduction carries
   it; publish the D-index path.
4. *Monetary coordination.* The land-collateral shock is deflationary
   and the VAT step is inflationary once; sequence them in one window
   (§7.1, item 6); the central bank lends against structures.
5. *The buffer fund* (§6) so the floor is never debt-financed in a rent
   downturn.

One caution for measurement: rising yields raise the Z.1 members of κ
mechanically (they impute rent as land value times the ten-year yield);
do not read that as the base improving — the flow members are the ones
to trust on a rate move.

---

## 9. Decisions for her, and what is not verified

**Decisions.**
- *Folder.* Built here, in `three-taxes/`, because the thread already
  existed with this paper's sketch; one word if she wants the practical
  design split out.
- *The closure.* Which reinvestment assumption the paper carries —
  recommend bracketing both, with the bracket as the finding.
- *The split target.* 40% gross is twice today's gross investment; 40%
  net would be ten times today's net (gross private investment 17.7%
  against depreciation 16.5%, the latter including government capital).
  Which she means changes the paper.
- *98% and the lag.* Keep the lag as an assessment floor only (§1.1)?
- *The announcement-date design.* Increment-only grandfathering (40%
  stock loss) versus full capture with the write-down route (§7.1,
  items 1 and 3), or both.
- *The fund's foreign leg.* Keep as a hedge on the ceiling shortfall, or
  drop on the first-claim argument.
- *Which shocks get theorems.* T11 has the price paths; the bank
  pass-through and the rent-backed-debt swap are prose until she says
  otherwise.
- *The split as a rule (§4b).* Carry 40/60 as the buildout-phase value
  of the four-piece rule, with the hump trajectory, or as a fixed
  target? And whether the shock ledger on the dynamics engine is this
  paper's unit or P1's.
- *The lag design (§1.1).* Drop the general up-lag (17% leak at 2%
  growth, ten years); short symmetric measurement lags; a registered
  discovery window on verified increments only — ten years as the term,
  or cost recovery with uplift?
- *The valuation mechanism (§1.1).* Adopt rolling anonymous sample
  auctions + the automatic take-call + the structure-retained surrender
  put as the paper's assessment design (SKETCH T12), and whether the
  match-right bid-chilling problem gets a theorem or a citation.

**Not verified in this memo, to live-verify before any draft** (house
rule: nothing enters a draft on memory): every precedent named as such
(Norway, PRRT, Singapore's vehicle quota, New Zealand's GST and OECD VAT
efficiencies, Amsterdam and Hong Kong leases, property-tax deferral
programs, the Nordic bank resolutions and post-2008 write-downs, foreign
land-ownership limits, the 2016 DBCFT proposal); the non-US yield levels;
the mortgage tail distribution (no LTV-by-metro data pulled — the "60%
underwater" example is arithmetic on stated assumptions); the Z.1 land
residual's post-1995 reliability; the stylized κ path (pinned to q, not
to years).
