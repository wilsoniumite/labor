# Question 1, US: an LVT funding the bridge's dividend, through the bridge's machinery

Stella's question about the 2026-06-14 post: "I'm wondering if an LVT-UBI loop would respond in a similar way, how
similarly?" The post co-launches a land-value tax but leaves its incidence and revenue unmodelled ("Mechanism two:
the base"). This folder models it. A tax on land rent funds the same flat dividend per adult share. The money runs
through the rebuilt machinery (`consumption/rebuild/code/bridge.py`, imported unchanged) on the same CE 2024
population, beside the VAT bridge.

## The answer

Similar in direction and in make-up; different in size, in who pays, and in the stock channel that sets the demand
sign.

- **What carries over: the directions and the composition.** Both instruments take from the top of the income
  distribution and pay the same flat dividend. Under the post's method all 36 charted category bars keep their sign,
  nearly every bar (31 of 36) is the VAT bar times 2.3-3.0, rented dwellings stays the largest mover (32% of the
  impulse under both), and new cars stays the one large negative bar. The flow impulse is positive under both,
  because MPCs fall with income.
- **What changes: the size and who pays.** Land is far more concentrated than VAT-able spending. The top income decile
  holds 39% of residential land but does 22% of VAT-able spending, so the same $249 dividend moves 2.5 times as much
  money: a flow impulse of 0.98% of consumption against 0.39%, and a top-decile net payment of $514 a month per adult
  share against $172. The payers are landowners, not big spenders: 99% of them own their home, and owners over 65
  make 45% of the net payments.
- **What vanishes: the price step and the Auerbach-Kotlikoff levy.** The VAT raises the consumer price level by
  7.4-9.3%. In standard incidence theory the LVT raises it by nothing, because a tax on a factor in fixed supply is not
  passed on. The indexation plumbing goes with the price step, and so does the levy on existing wealth, with its
  perception parameter λ.
- **What appears instead: a visible capitalization and collateral shock.** A credible permanent tax at the bridge rate
  cuts land prices 85% at announcement ($19.8tn). The SCF owners' aggregate loan-to-value ratio goes from 29% to 44%,
  and 16.8 million mortgaged owners cross 80%, 6.2 million of them hand-to-mouth.
- **The demand sign at impact.** Count each owner's response once: the bill as a flow at the owner's MPC, plus a
  credit effect on the borrowing room that the owners crossing 80% lose. On that clean reading the LVT is about
  demand-neutral on residential land (+0.15% of consumption). It is mildly positive with business land: +0.67% with
  corporate land on the wealth reading, +0.93% if shareholders paid the corporate bill from cash. The VAT is negative
  on the same SCF data: −1.37% at the post's λ = 0.35 (the post's own dynamic path has −0.69% at year 3). The sign
  depends on four things:
  - *the collateral concept.* Adding 6 cents per dollar of the crossers' lost equity on top of their bills counts the
    same money twice (T4). That reading gives −0.91% (the unit's earlier central, now a labelled band edge);
  - *who responds.* If only the hand-to-mouth crossers respond, +0.77%;
  - *deferral design.* If owners over 65 defer their bills and the dividend is paid in full, the state lends 30% of
    the revenue, which adds 2.0 points while it lasts (−0.12 if the dividend is cut to stay cash-balanced);
  - *the MPC level.* At the SCF's measured windfall MPCs both flows shrink to near zero (LVT 0.15%, VAT 0.06%), and both
    instruments turn negative (LVT −0.68%, VAT −1.70%).

So the LVT bridge is a more redistributive version of the VAT bridge, with the same demand fingerprint and no price
step. Its macro risk sits in mortgage collateral instead of in perception. Counted once, that risk is smaller than the
unit's earlier central suggested, and a broader base shrinks it further.

## The answer in more detail

**What carries over.** Both instruments take from the top of the income distribution and pay a flat dividend, so the
demand tier tells the same story. All 36 charted category bars keep their sign. The make-up of the demand impulse is
nearly the same under both: rented dwellings is the largest mover (32% of the impulse), health insurance next (10%),
and new cars is the one large negative bar. Under the post's own decile method, nearly every bar (31 of 36) is the
VAT bar times 2.3-3.0. The five outliers are small bars with mixed decile signs: public and other transportation,
vehicle finance charges, and vehicle rental, leases and licenses (3.3-3.6 times), and other entertainment equipment
and reading (1.5-1.6 times). The flow impulse is positive under both, for the same reason (MPCs fall with income).

**What changes.**
- *Size.* Land is far more concentrated than VAT-able spending. The top income decile holds 39% of residential land
  (52% once business land is counted) but does 22% of VAT-able spending. At the same $249 dividend, the top decile
  pays $514 a month net per adult share (−11.7% of its budget) against the VAT's $172 (−3.9%). Eight deciles gain
  instead of seven. The flow impulse is 0.98% of consumption against 0.39%. The LVT/VAT ratio stays at 2.5 to 3.0
  under every MPC grade tried, including the measured one.
- *Who pays.* The VAT's payers are big spenders. The LVT's payers are landowners, and 99% of them own their home.
  Below the top two deciles most net payments come from owners over 65: they make 45% of all net LVT payments, and
  60-82% of them in deciles 2-8. Hand-to-mouth families make 7% of the payments, nearly all of them house-rich
  ("wealthy hand-to-mouth"). Under the VAT, hand-to-mouth families make 14% of net payments.
- *Inside the deciles.* The post's method gives a decile's payers and recipients one shared basket. Under the LVT they
  do not share one. In the lower and middle deciles the payers are owners, and nearly every renter is a pure
  recipient, since renters hold almost no land (1.4% of L1 payers are renters with other property). When the
  structural housing lines are split by tenure, two bars change. The LVT's rent bar more than doubles, to $18.10 a
  month from $8.28 decile-netted. That comparison mixes two steps: the liquidity grade alone, at the household level
  with decile baskets, gives $8.14, and the tenure baskets alone multiply that by 2.2. (VAT: $3.36, or $4.00 split the
  same way.) Home maintenance, repairs and insurance turns negative (−$1.96 against +$0.81). Owners' mortgage interest
  (−$3.52) and property taxes (−$2.15) fall too, off the chart. The VAT barely moves under the same split. In this
  sense the payer basket moves away from the top's spending and toward homeowners' baskets.

**What vanishes.** The price step. The VAT raises the consumer price level by 7.4-9.3%. The LVT raises it by nothing.
That is incidence theory, not accounting: land is in fixed supply and rents are set by demand, so the owner cannot
pass the bill on. It removes the indexation plumbing (the constant-tax index for pensions, wages and contracts). It
also removes the Auerbach-Kotlikoff levy on existing wealth, together with its perception parameter λ, which the
post calls its "single most consequential judgment call". The program still moves rents through demand. The
dividend's own rent bar ($8.28 per adult share a month, 3.6% of rent spending) is extra demand for a fixed stock: a
rent-price effect, which the loop below taxes back at φ. "Nothing" is the pass-through of the tax, not the whole
rent-price effect of the program.

**What appears instead.** A visible stock shock on land, and a collateral channel with it. Take a credible permanent
tax at the bridge rate (φ = 0.85 at the 10-year yield). It cuts land prices 85% at announcement, a $19.8tn loss. The
SCF owners' aggregate loan-to-value ratio goes from 29% to 44%, and 16.8 million mortgaged owners (30% of them) cross
80% LTV.

The crossers' lost equity, $2,834bn, is their own-home bills ($119bn a year) capitalized at r (T4): the same money.
The flow already charges those bills at the owners' MPCs ($79bn a year less spending, 0.87% of consumption). The clean
reading therefore adds only what the bill does not contain: a credit effect on the borrowing room the crossers lose
($1,246bn of capacity below 80% LTV). At the housing-collateral responses in the literature, 4.7 cents per dollar per
year (Aladangady 2017) to 5-7 cents (Mian, Rao and Sufi 2013), that credit effect is −0.65% to −0.97% of consumption
(−0.83% at 6 cents). The unit's own stress value of 10 cents, which no source gives, makes it −1.38%. Applied to all
crossers' lost equity instead, the literature's 4.7-7 cents give −1.48% to −2.20%, and the 10-cent stress value
−3.14%. On top of the flow that reading counts each crosser's bill twice, so it appears only as a band edge labelled
"includes the T4 overlap".

Who responds is a judgment call. The 4.7-7 cent responses are averages over all owners, driven by the constrained
ones. Of the 16.8 million crossers, 6.2 million are hand-to-mouth (KVW, the unit's own flag), and these hand-to-mouth
crossers hold 28% of the lost equity. Another 40% of it sits with families holding at least three months' income in
liquid assets, who need not borrow. If only the hand-to-mouth crossers respond, the credit effect is −0.21% (−0.16% to
−0.24% at 4.7-7 cents).

| Demand at impact, % of consumption (same SCF balance sheets, same denominator) | central | band | band edge: includes the T4 overlap | band edge: only hand-to-mouth crossers respond |
|---|---|---|---|---|
| VAT: flow + levy at λ = 0.35 | −1.37 | [−2.21, −0.53] | | |
| LVT at the bridge rate, base L1: flow + credit effect on crossers' lost borrowing capacity | +0.15 | [−0.20, +0.54] | −0.91 | +0.77 |
| LVT at the bridge rate, base L2, corporate land on the wealth reading | +0.67 | [+0.10, +1.24] | +0.25 | +0.89 |
| ... corporate land on the flow reading | +0.93 | [+0.62, +1.26] | +0.52 | +1.15 |
| The post's published VAT path, central (year 3; year-5 band) | −0.69 | [−0.97, −0.14] | | |

The central counts each crosser's response once: the bill in the flow at the central MPC schedule, plus 6 cents per
dollar of lost borrowing capacity for every 80% crosser. The bands pair the extremes, as the VAT's does. The lower edge
takes the high MPC schedule (the smallest flow) with the top of the literature (7 cents, Mian, Rao and Sufi; 5 cents of
wealth effect on corporate land). The upper edge takes the low schedule with 4.7 cents (Aladangady; 2 cents). The VAT's
band is the same MPC schedules with the levy at 5 and 2 cents. The 10-cent stress value is outside the band: it would
put the L1 lower edge at −0.61 (L2: −0.05). The last two columns are the judgment edges, at the central schedule and 6
cents. "Includes the T4 overlap" adds 6 cents per dollar of the crossers' lost equity on top of their bills, so each
bill is counted twice; it was the unit's earlier central. "Only hand-to-mouth crossers respond" keeps the credit effect
for those crossers alone. The other clean reading lets the crossers respond to their lost equity instead of their
bill, and gives −0.04 on L1 (+0.59 on L2). On the PCE denominator every entry is × 0.455: L1 +0.07, L2 +0.30, VAT
−0.62.

The base matters here. With business and corporate land in the base (L2), the rate on homes falls to φ = 0.56. Then
8.3 million mortgaged owners end up underwater instead of 14.4 million, 10.3 million cross 80%, and the credit effect
is −0.31%. Corporate land is the one part of the base whose holders never see a bill: the corporation pays it out of
earnings, and its shareholders see a capitalized fall in their equity. The L2 central therefore takes their response
as a wealth effect on that loss (3.5 cents per dollar per year; 2-5 cents in the band), not as a bill paid from
household cash at the decile MPC: +0.67%. The flow reading for corporate land gives +0.93%. The rental and
noncorporate landlords do see bills and stay on the flow. If they too responded to their capitalized loss at 3.5 cents
instead of their bills, L2 would be −0.13% (L1, rental land alone: −0.23%).

**What it hinges on.**
1. *The collateral concept and who responds.* On the clean concept (a credit effect on the crossers' lost borrowing
   capacity, every crosser) L1 is +0.15%. With the T4 overlap it is −0.91%, and with only the hand-to-mouth crossers
   responding +0.77%. Increment-only grandfathering cuts the credit effect to −0.11% (−0.27% on lost equity). But it
   also leaves almost no revenue at launch, because only rent growth is taxed, and launch revenue is the bridge's
   whole job.
2. *The base.* L2 spreads the bill over $35.8tn of land instead of $23.4tn. That gives a bigger flow (1.24%), a
   smaller credit effect (−0.31%), and a top decile paying $750 a month per share. Corporate land on the wealth reading
   gives +0.67% (+1.03% at 2 cents, +0.30% at 5 cents); on the flow reading, +0.93%.
3. *The rent-to-value rate.* At the bridge rate the bill is fixed, but the price fall it implies is not. It ranges
   from 53% (land rent = 50% of PCE housing) to 88% (30% of PCE housing) across the paper's four land-rent measures.
   The credit effect ranges with it, from −0.27% to −0.88% at 6 cents (on lost equity, −0.64% to −2.04%).
4. *Deferral for older owners.* Owners over 65 owe 30% of the residential-land bill. If they defer it against their
   estates, either the state lends 30% of the revenue, which adds 2.0 points to the impulse while it lasts, or the
   dividend falls to $175 to stay cash-balanced. Their capitalized loss is then the open question: −2.3% of
   consumption at 3.5 cents per dollar, or 0 if they ignore it.
5. *MPCs.* The SCF 2025 windfall question measures MPCs of 0.29 at D1 to 0.18 at D10, a quarter of the post's level
   and a quarter of its slope. With them, both flow impulses nearly vanish (VAT 0.06%, LVT 0.15%), and demand becomes
   a pure stock story for both instruments: VAT −1.70% (the levy), LVT L1 −0.68% (the credit effect; −0.06% if only
   the hand-to-mouth crossers respond), L2 −0.79%.
6. *The top of the land distribution.* CE's own home values put 32% of residential land in the top decile, against
   39% in the SCF. That cuts the top decile's net payment from $514 to $365 and the impulse to 0.67%.

**The loop.** Under the LVT, the dividend's own rent bar raises land rent and the tax takes it back: +1.1% of the
dividend [0.9, 1.4], or 2.5% with tenure-aware baskets. The LVT's increment is $11.1bn a year of land rent. Under the
VAT, its own (smaller) increment, $4.5bn a year (worth $107bn at the 10-year yield), goes to landlords, 60% of them in
the top decile. This is T5's arithmetic at work: the gross multiplier is 1/(1 − φ·ls·q) = 1.017, second-order, as T5
says. The loop charges the holders of rental land the tax on the increment but does not credit them with the rent they
collect; that receipt is worth +0.07% of consumption under the LVT and +0.03% under the VAT (Results 7).

## Run

```
venv/bin/python -I consumption/lvt/code/run_lvt_us.py       # about 35 s; writes out/us_lvt_*.csv and figures/
venv/bin/python -I consumption/lvt/checks/check_lvt_us.py   # 261 PASS / 0 FAIL / 1 INFO; writes out/check_lvt_us.csv
venv/bin/python -I consumption/lvt/checks/verify_independent_lvt_us.py   # the independent re-derivation: 266 OK / 9 BAD of 275
```

`bridge.py` is imported, not forked. No hook was needed: `net_from_base()`, `per_share_monthly()`,
`shifts_from_transfers(shock=...)`, `impulse(shock=...)`, `decompose()` and `eta_table()` carry everything. The
concurrent Finland work added a FINLAND section and an `mpc_default` key to bridge.py. US model dicts do not carry
that key, and checks D1-D5 confirm the VAT side still reproduces the rebuild's nets, its 36 Fig 5 bars, its impulses
and its dividend.

## Method

Tiers as in the post: **accounting** = identities and mechanical arithmetic; **calibrated** = named behavioural
parameters with bands.

1. **The tax (accounting).** bill_i = φ · r · L_i on announcement-date land values. r is the rent-to-value rate of one
   of the paper's four land-rent measures (`pinning/code/feasibility_kappa.py`, household scope, 2024): (m1) household
   land residual × GS10 (4.208%); (m2) × GS10 + 1.5; (m3) 30% and (m4) 50% of PCE housing services ($3,148.6bn),
   divided by the household land residual. Revenue funds a flat dividend per payment share (adult 1, child 0.3) on CE
   2024's 279.1 million shares, the VAT bridge's rule. Rate (a), bridge-equivalent: φ is set so the dividend equals
   the rebuilt $249.38 ($835.1bn a year). Rate (b), full capture: φ = 0.98.
2. **Land by household (accounting with judgment inputs).** SCF 2025 families (income year 2024; every dollar value
   ÷ 1.027027, the extract's own 2025→2024 factor). For INCOME that restates the 2024 income year. Balance-sheet items
   are interview-date (2025) values, so their "2024 dollars" are a CPI deflation of 2025 values, not a 2024 valuation.
   Ratios (LTVs before the tax, hand-to-mouth flags, decile shares) do not depend on it, and the calibrated s absorbs
   it (s = 0.406 if the 2025 values are matched to Z.1 2025 instead). Base L1 = s · (HOUSES + ORESRE), with s set so
   that the SCF-weighted total equals the Z.1 2024 household land residual, $23,410.7bn. Base L2 adds the Z.1
   noncorporate business land residual ($8,354.4bn, allocated by NNRESRE + BUS) and nonfinancial-corporate land
   ($3,994.6bn, assumed, allocated by EQUITY).
3. **Incidence (accounting).** Families go to pretax-income deciles by the Fed's own pooled weighted percentile groups
   of INCOME (INCPCTLECAT; each decile holds 10.0% ± 0.03% of families). Each decile's land total is spread over its CE consumer
   units and converted to CE payment shares, exactly as the VAT accounting does. `bridge.net_from_base()` then
   returns net_d = dividend − φ·r·L_d with Σ w_d net_d = 0. At the household level, SCF payment shares come from
   MARRIED/KIDS calibrated on the 2022 roster, scaled within each decile to CE's totals (c_d = 0.92-1.19). Household
   nets therefore aggregate exactly to the decile nets.
4. **MPCs (calibrated).** The post's grade: the rebuilt mid schedule by decile (low/high bands; the monotone
   diagnostic for shape). The liquidity grade: recipients at the mid schedule, payers at 1.0 if hand-to-mouth and at
   the decile value otherwise. Hand-to-mouth follows KVW 2014: liquid = LIQ + STOCKS + BOND + NMMF − CCBAL at or below
   INCOME/52 (biweekly pay; INCOME/24 as the band); wealthy if illiquid wealth > 0. The measured grade: the SCF 2025
   windfall MPC by decile, and by decile × HtM. dC_i = mpc_i · net_i on a cash basis, aggregated to deciles.
5. **Demand (calibrated).** dC_d/C_d enters `bridge.shifts_from_transfers(shock=...)`, the post's θ·η machinery, in
   three versions. (i) Decile-netted: the post's method. (ii) Household level: the liquidity-graded MPCs, decile
   baskets. (iii) Household level with tenure-aware baskets: the structural housing lines (rent; mortgage interest,
   property taxes, home maintenance and insurance) sit with renters or owners inside each decile, in CE Table 1710's
   owner/renter ratios, with the elasticities re-evaluated at each tenure basket by `bridge.eta_table()`. The bars of
   (iii) still add up to the household flow (Engel aggregation, checked to 0.2%).
6. **Macro (theory for the price level; calibrated for demand).** (i) Price level: VAT 15% × the 61.7% VAT-able
   share × 80-100% pass-through (accounting given the pass-through); LVT 0 by standard incidence theory (a tax on a
   factor in fixed supply is not passed on). (ii) Demand: the flow impulse for every rate × base × measure × MPC grade
   × deferral variant (`us_lvt_impulse.csv`, 714 rows), then the stock channel. Capitalization: the land price falls
   by φ (credible permanent capture), and for the phase-ins and increment-only grandfathering by the repo's price-path
   table (`three-taxes/data/lvt_shock.csv`, computed at φ = 0.98 with γ/δ = 2%/5% and annual timing), scaled by
   φ/0.98. One convention for every design: the table's increment-only drop is 0.404 at 0.98 (0.349 at the bridge
   rate), against 0.392 (0.339) from the continuous approximation φ·γ/δ. No wealth effect is added for owner-occupiers,
   whose bill and price fall are the same money (T4). Collateral: LTVs of mortgaged owners (MRTHEL / HOUSES) before and
   after the land loss, and the owners who cross 80% / 90% / 100% lose their remaining borrowing room. The never-both
   rule applies to these crossers as to non-occupiers. Their bill is in the flow, so the clean reading adds only a
   credit effect on their lost borrowing capacity (4.7-7 cents per dollar per year, 6 central; 10 cents is a stress
   value). Their lost equity is the bill capitalized, so a response to it on top of the flow appears only as a band edge
   ("includes the T4 overlap"). Who responds: every crosser (central), or only the hand-to-mouth crossers.
   Non-occupying holders: either the flow (bill × MPC) or a wealth effect on the capitalized loss (2-5 cents per
   dollar per year), never both; both are shown. Corporate land is on the wealth reading in the L2 central (its holders
   never see a bill), with the flow reading beside it. The VAT's levy channel is run in an impact version on the same
   SCF balance sheets: −mpw · λ · 8% · net worth.
7. **The loop (calibrated).** The rent bar raises land rent by its land share ls. At φ, that increment is taxed back
   and paid out as a flat extra dividend, financed by the holders of rental land. Each round runs back through the
   bridge, iterated to the fixed point and checked against the closed form φ·ls·R0/(1 − φ·ls·q). The holders are
   charged the tax on the increment but not credited with the rent they collect (second order; Results 7).

## Judgment calls, bands and their effect

| Call | Choice | Band / alternatives | Effect on the headline |
|---|---|---|---|
| Land share of residential value s | uniform, calibrated: 0.416 (Z.1 2024 land / SCF 2025 property in 2024 $); Z.1's own aggregate ratio is 0.460 | 0.30-0.60 at a fixed aggregate property value | Bridge-rate nets and flows: none (a uniform s cancels). φ on the yield measures: 1.18 at s = 0.30 (infeasible on m1) to 0.59. Full-capture dividend (m1): $208-$416. Credit effect (6c): unchanged on the yield measures, −0.43% to −2.25% on m3 (on lost equity −0.99% to −4.96%) |
| s rising with home value | s = 0.30 + 0.30·F(V), F the weighted CDF of owners' home values, rescaled to Z.1 (effective 0.24-0.48) | judgment: expensive homes are expensive for their location | D10 −$588 vs −$514; impulse 1.09% vs 0.98%; credit effect −0.79% vs −0.83%; net at impact +0.30% vs +0.15% |
| Land concept | the paper's household residual (HH+NPO real estate − HH structures; nonprofit land and structures inside) | households-only owner-occupied residual, $19,374.9bn | φ on m1 = 1.02 (infeasible on L1); distribution unchanged |
| Matching year and dollars | SCF 2025 in 2024 $ (for balance sheets, a CPI deflation of interview-date 2025 values) vs Z.1 2024 | SCF 2025 nominal vs Z.1 2025: s = 0.406 | none on shares or nets |
| Survey year | SCF 2025 | SCF 2022 uprated: real 2024 $, land rescaled to Z.1 2024 (the 2022 distribution, uniformly uprated), roster adults; s = 0.442 | D10 −$524; impulse 0.997%; credit effect −1.00%; net at impact 0.00% vs +0.15% (L2 +0.58% vs +0.67%) |
| NFC land after 2020 | NFC land share of NFC real estate at its 2016-2020 mean (0.255): $3,994.6bn | low: NFC structures grown at noncorporate current-cost growth ($1,699.8bn); high: 2020 share ($4,306.2bn) | L2 φ 0.550-0.593; D10 −$724 to −$753 |
| Noncorporate land key | NNRESRE + BUS | + ORESRE (Z.1 books household rental property in NNB); NNRESRE + ACTBUS | D10 −$733 / −$739 vs −$750 |
| Corporate land owners | 100% to SCF households pro rata to EQUITY | foreign, government and DB-pension holders (Z.1 L.223 not used) | L2's top-decile bills are an upper bound; revenue unaffected |
| Payment units, 2025 | adults = 1 + partner + 2022-roster cell mean (AGECL × MARRIED × min(KIDS, 3)); minors likewise; scaled to CE decile totals | 2022 in-sample: decile means within 0.06 shares | household per-share nets only; decile results exact by construction |
| Hand-to-mouth band | biweekly, INCOME/52: 32.0% HtM (21.2% wealthy) | monthly, INCOME/24: 40.2% (27.4%) | LVT household impulse 0.885% vs 0.852% |
| MPC grades | the post's mid schedule | low/high; monotone diagnostic; liquidity-graded; measured windfall (decile; decile × HtM; shape scaled to D1 = 1) | LVT L1: 0.70-1.19% (post family), 0.14-0.52% (measured); the LVT/VAT ratio stays 2.5-3.0 |
| Deferral take-up | 100% of the eligible | flows are linear in take-up | owners 65+: +2.0 points (dividend paid in full) or −0.12 (cash-balanced) |
| Collateral concept | a credit effect on the crossers' lost borrowing capacity (their bill is already in the flow) | the crossers' lost equity on top of their bills: includes the T4 overlap, a band edge only; their lost equity instead of their bill (the other clean reading) | L1 net at impact +0.15%; −0.91% with the T4 overlap; −0.04% on the other clean reading |
| Collateral response | 6 cents per $ per year (midpoint of Mian, Rao and Sufi's 5-7) | 4.7 cents (Aladangady 2017) to 7 cents (the literature); 10 cents, the unit's stress value (not from the literature); thresholds 80/90/100% | credit effect −0.65% to −0.97% (stress −1.38%) on L1; on lost equity −1.48% to −2.20% (stress −3.14%) |
| Who responds through collateral | every 80% crosser (16.8m) | only the hand-to-mouth crossers (KVW biweekly: 6.2m, 28% of the lost equity; 40% of it sits with families holding three months' income in liquid assets) | L1 net at impact +0.15% vs +0.77%; L2 +0.67% vs +0.89% |
| Corporate (NFC) land holders' response | a wealth effect on the capitalized loss, 3.5 cents (holders never see a bill) | the flow reading (bill × decile MPC); 2-5 cents | L2 net at impact +0.67% vs +0.93%; +1.03% at 2 cents, +0.30% at 5 cents |
| Increment-only grandfathering | the repo's price-path table (`lvt_shock.csv`, as for the phase-ins): loss 0.349 at the bridge rate | the continuous approximation φ·γ/δ: 0.339 | credit effect −0.11% either way; on lost equity −0.27% vs −0.26% |
| Wealth-effect propensity | 2 / 3.5 / 5 cents per $ per year (the post's fn 31; midpoint judgment) | none | VAT levy; corporate land in the L2 central; LVT non-occupier alternative; deferrers' residual |
| Land share of a rent change (loop) | 0.40 | 0.30-0.50 (the paper's flow measures) | loop 0.86-1.44% of the dividend |
| VAT bills inside deciles | each decile's CE VAT total split by SCF TOTSPENDNH | none | VAT household-level grades only |
| Tenure split of housing lines | Table 1710 ratios (owners' rent = 0.8% of renters'; renters' owner costs = 0.6% of owners') | none | rent bar $18.10 vs $8.28; home maintenance −$1.96 vs +$0.81 |

Literature behind the collateral band, checked against the published abstracts on 2026-11-02:
- Aladangady (2017 AER), abstract: "A $1 increase in home values leads to a $0.047 increase in spending for
  homeowners, but a negligible response for renters". It attributes the response to looser borrowing constraints.
- Mian, Rao and Sufi (2013 QJE), abstract: the average MPC out of housing wealth "is 5-7 cents"; ZIP codes "with
  poorer and more levered households have a significantly higher MPC".
- Berger, Guerrieri, Lorenzoni and Vavra (2018 REStud): the response to a permanent house-price shock is
  approximately the MPC out of temporary income times the value of housing, so it concentrates on constrained,
  levered owners.

The 10-cent edge is the unit's own stress value (judgment): no source gives a number for the levered tail. These
estimates come from house-price changes that carry no tax bill. Under an LVT an owner-occupier's price fall is the
bill capitalized (T4), so the unit applies them to the crossers' lost borrowing capacity (a credit effect) and shows
lost equity only as a band edge. They are also averages over all owners, driven by the constrained ones (Aladangady;
Berger et al.), which is why who responds is a judgment call with a band.

## Results

### 1. The tax: φ for the bridge's dividend, and full capture (`us_lvt_phi.csv`)

| Measure | r | φ (a), L1 | φ (a), L2 | Full-capture dividend, L1 | Full-capture dividend, L2 |
|---|---|---|---|---|---|
| m1 household land × GS10 | 4.21% | 0.848 | 0.555 | $288 (1.16× VAT) | $440 (1.77×) |
| m2 household land × (GS10 + 1.5) | 5.71% | 0.625 | 0.409 | $391 (1.57×) | $597 (2.40×) |
| m3 30% of PCE housing | 4.03% | 0.884 | 0.579 | $276 (1.11×) | $422 (1.69×) |
| m4 50% of PCE housing | 6.72% | 0.530 | 0.347 | $461 (1.85×) | $704 (2.82×) |

Both bases can fund the bridge's dividend on all four measures (φ ≤ 0.98). Two variants cannot. With s = 0.30
(residential land $16.9tn), L1 on m1 needs φ = 1.18. With the households-only owner-occupied land concept
($19.4tn), L1 on m1 needs φ = 1.02. In both cases the yield-based measure leaves residential land alone short of the
bridge's dividend, while L2 still funds it. At the bridge rate the measure changes φ but not the bills (φ·r is fixed
by the dividend), so incidence and flows are the same on every measure. The capitalized loss is not the same: it is
φ·L, from $12.4tn (m4) to $20.7tn (m3) on L1.

### 2. Land by household (`us_lvt_s_calibration.csv`, `us_lvt_land_by_decile.csv`)

SCF 2025 HOUSES total $46.0tn (2024 $), against Z.1 households' owner-occupied real estate of $46.9tn. ORESRE is
$10.3tn. SCF property is $56.3tn against Z.1 HH+NPO real estate of $50.9tn, so the calibrated s (0.416) sits below
Z.1's aggregate land/real-estate ratio (0.460): the SCF's property total is larger.

| Decile share, % | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 |
|---|---|---|---|---|---|---|---|---|---|---|
| L1 residential land (SCF) | 1.8 | 2.5 | 3.7 | 4.5 | 6.0 | 7.1 | 9.4 | 10.6 | 15.0 | 39.4 |
| L2 all land | 1.7 | 1.7 | 2.8 | 3.3 | 4.8 | 5.4 | 7.4 | 8.4 | 13.0 | 51.5 |
| SCF HOUSES | 2.0 | 2.8 | 4.0 | 4.8 | 6.6 | 8.0 | 10.4 | 11.6 | 14.9 | 34.9 |
| CE 2024 home values (cross-check) | 3.4 | 5.5 | 6.5 | 6.7 | 7.5 | 8.3 | 9.8 | 11.8 | 15.0 | 25.5 |
| VAT-able consumption (CE) | 4.4 | 5.3 | 6.3 | 7.3 | 8.3 | 8.9 | 10.4 | 12.5 | 14.9 | 21.7 |

Homeownership by decile agrees between the surveys (SCF 39-93%, CE 34-90%). Home values at the top do not: the SCF's
top decile holds 35% of home value against CE's 26%, the familiar CE under-coverage of the top. The robustness table
runs the CE distribution as a variant.

### 3. Incidence: net per adult share per month (`us_lvt_accounting_by_decile.csv`)

| | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 |
|---|---|---|---|---|---|---|---|---|---|---|
| VAT bridge, $ | 87.8 | 53.4 | 60.8 | 55.5 | 30.2 | 38.6 | 16.9 | −13.8 | −37.9 | −172.0 |
| LVT (a) L1, $ | 183.4 | 157.3 | 139.4 | 130.5 | 89.7 | 80.4 | 40.1 | 24.7 | −39.4 | −514.4 |
| LVT (a) L2, $ | 188.8 | 185.6 | 166.7 | 161.3 | 121.9 | 121.8 | 83.7 | 71.8 | −1.0 | −749.6 |
| LVT (b) L1 m1, $ (dividend $288) | 212.0 | 181.8 | 161.2 | 150.9 | 103.7 | 92.9 | 46.4 | 28.5 | −45.5 | −594.7 |
| LVT (b) L2 m1, $ (dividend $440) | 333.3 | 327.8 | 294.4 | 284.8 | 215.3 | 215.2 | 147.9 | 126.8 | −1.8 | −1323.6 |
| VAT, % of budget | 4.8 | 2.4 | 2.9 | 2.6 | 1.3 | 1.6 | 0.7 | −0.5 | −1.2 | −3.9 |
| LVT (a) L1, % of budget | 10.0 | 7.2 | 6.7 | 6.2 | 3.8 | 3.4 | 1.6 | 0.9 | −1.3 | −11.7 |
| LVT (a) L2, % of budget | 10.3 | 8.5 | 8.0 | 7.6 | 5.1 | 5.2 | 3.3 | 2.5 | −0.0 | −17.1 |

Decile by decile: D1 gains twice as much under the LVT. D2-D7 gain 2-3 times as much. D8 switches from a small payer
(−$14) to a gainer (+$25). D9 pays about the same (−$39 against −$38). D10 pays three times as much. Under L2, D9 is
at break-even and D10 pays 4.4 times the VAT's net.

**Households** (`us_lvt_who_pays.csv`; SCF 2025 families, bridge rate):

| | VAT (household split) | LVT L1 | LVT L2 |
|---|---|---|---|
| Families that are net payers | 37.8% | 31.6% | 22.4% |
| ... in D1 / D5 / D9 / D10 | 13% / 39% / 50% / 65% | 6% / 28% / 49% / 85% | 4% / 19% / 32% / 78% |
| Payers who own a home | 75% | 99% | 98% |
| Payers aged 65+ | 35% | 44% | 49% |
| Payers who are hand-to-mouth | 24% | 16% | 11% |
| Share of net payments by owners 65+ | 36% | 45% | 46% |
| Share of net payments by hand-to-mouth families | 14% | 7% | 3% |
| Net per share, 10th / 50th / 90th percentile (all families) | −$234 / +$47 / +$167 | −$323 / +$117 / +$249 | −$236 / +$155 / +$249 |

Under the LVT the median family gains more and the payers pay more. 68% of families are net recipients, and the
third with no land at all (32.6%) pays nothing. Within deciles the spread is wide (Fig 1, right panel). D10's 10th
percentile pays $1,438 a month per share. The top quarter of D1-D6 and the top tenth of D7-D9 (families with no
land) receive the full $249. Among owners 65+, 57% are net payers. Net payments by decile and payer group are in
`us_lvt_payments_by_group.csv`: owners 65+ make 54% (D1), 74-82% (D2-D4), 60-71% (D5-D8), 41% (D9) and 36% (D10)
of each decile's net payments.

### 4. MPC grades (`us_lvt_mpc_grades.csv`, `us_lvt_feds_mpc_check.csv`)

| Decile | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 |
|---|---|---|---|---|---|---|---|---|---|---|
| Post, mid (rebuilt) | 1.00 | 1.00 | 0.97 | 0.91 | 0.85 | 0.78 | 0.72 | 0.66 | 0.59 | 0.53 |
| Post, monotone diagnostic | 0.99 | 0.99 | 0.96 | 0.91 | 0.88 | 0.82 | 0.77 | 0.77 | 0.61 | 0.53 |
| Measured windfall MPC (SCF 2025) | 0.29 | 0.26 | 0.25 | 0.23 | 0.22 | 0.19 | 0.21 | 0.19 | 0.21 | 0.18 |
| ... not hand-to-mouth | 0.30 | 0.23 | 0.25 | 0.23 | 0.22 | 0.20 | 0.22 | 0.20 | 0.22 | 0.19 |
| ... hand-to-mouth | 0.28 | 0.28 | 0.26 | 0.25 | 0.21 | 0.17 | 0.17 | 0.16 | 0.19 | 0.09 |
| Hand-to-mouth share (biweekly) | 0.46 | 0.50 | 0.44 | 0.40 | 0.34 | 0.35 | 0.29 | 0.21 | 0.14 | 0.07 |

The public extract reproduces the Fed's FEDS note (Aladangady, Bricker, Chang, Goodman and Li, 2026-10-09, Fig 3)
within 0.7 points in every usual-income group, and exactly overall (22.35% spend, 47.31% save, 30.30% pay down debt).
Compared with the post's schedule, the measured MPC is about a quarter of the level (0.18-0.29 against 0.53-1.00) and
about a quarter of the slope (D1 − D10 = 0.11 against 0.47). Within deciles it is barely higher for hand-to-mouth
families, and lower in D1 (0.28 against 0.30) and from D5 up, where the hand-to-mouth are mostly house-rich. The FEDS
note finds +2.6 points conditional on usual income (22.9% against 20.3%).

The question asks about a one-month windfall over 12 months, with debt repayment offered as an explicit option. The
dividend is permanent, so the level is not the right object for the post's flow. The ordering is the informative
part. Under the measured grades the flow impulses fall to 0.06% (VAT) and 0.15% (LVT L1). With the measured shape
scaled to 1.0 at D1, they are 0.21% and 0.52%.

### 5. Demand shifts (`us_lvt_demand_shifts.csv`, `us_lvt_demand_compare.csv`, `us_lvt_decomposition_top10.csv`)

$ per adult share per month at the bridge rate, mid schedule. The household columns use the liquidity grade.

| Category | VAT (post's method) | LVT L1 (post's method) | LVT L2 | VAT, tenure-aware | LVT L1, tenure-aware |
|---|---|---|---|---|---|
| Rented dwellings | +3.36 | +8.28 | +10.32 | +4.00 | +18.10 |
| Health insurance | +1.08 | +2.80 | +3.68 | +0.91 | +2.41 |
| Gasoline and other fuels | +0.68 | +1.78 | +2.38 | +0.58 | +1.54 |
| Electricity | +0.64 | +1.60 | +2.02 | +0.57 | +1.42 |
| Home maintenance, repairs & insurance | +0.35 | +0.81 | +1.00 | +0.03 | −1.96 |
| Food at home | +0.59 | +1.48 | +1.87 | +0.51 | +1.16 |
| Vehicle insurance | +0.53 | +1.39 | +1.86 | +0.45 | +1.20 |
| Cars and trucks, used | +0.38 | +1.14 | +1.66 | +0.27 | +0.88 |
| Cars and trucks, new | −0.39 | −1.09 | −1.59 | −0.48 | −1.31 |
| Telephone services | +0.46 | +1.16 | +1.52 | +0.40 | +1.03 |
| Fees and admissions | −0.20 | −0.55 | −0.75 | −0.24 | −0.64 |
| Other lodging | −0.13 | −0.37 | −0.52 | −0.18 | −0.49 |
| Off chart: mortgage interest / property taxes | −0.38 / +0.10 | −0.86 / +0.22 | −0.96 / +0.25 | −0.64 / −0.17 | −3.52 / −2.15 |
| Total (flow impulse), $ | 10.48 | 26.31 | 33.47 | 8.46 | 23.85 |

Keep sign and size? Under the post's method every one of the 36 charted bars keeps its sign. Sizes scale by 2.3-3.0
for 31 of them, and the share of the impulse each bar carries is within 0.7 points of the VAT's (rent 31.5% against
32.1%). The outliers are small bars with mixed decile signs: public transport, vehicle finance and vehicle rental
(3.3-3.6×), other entertainment equipment and reading (1.5-1.6×). The reason is the decile machinery. Both
instruments' net payments sit at the top (Fig 6 analog: D10 supplies 87-95% of each top-10 withdrawal under the LVT,
61-83% under the VAT), and the bars are θ·η weighted sums of decile shocks with the same signs. The quality-ladder
result survives: new cars fall and used cars rise under both, 2.8-3.0 times larger under the LVT.

What changes is what the decile method cannot see. In the tenure-aware version two bars flip against the VAT's
tenure-aware bars (home maintenance, and reading at −$0.002). Against the post's own decile-netted VAT bars a third
flips as well: vehicle rental, leases and licenses (+$0.016 for the VAT, −$0.015 for the LVT). The rent bar more than
doubles and owner costs turn negative. The rent comparison mixes two steps: $8.28 (decile-netted) to $8.14 is the
liquidity grade at the household level with decile baskets, and $8.14 to $18.10 (2.2 times) is the tenure baskets
alone. LVT payers in D1-D8 are owners, mostly retirees, so their withdrawal lands on owners' baskets. The recipients beside them are renters, who pay nothing
under an LVT, and renters spend 24-32 cents of an extra dollar on rent at the margin (owners 0.3 cents; the
decile-average basket that the post's method uses says 3-19 cents). Under the VAT, renters pay VAT on their own
spending, so their net is smaller and the split matters less (rent $4.00 against $3.36).

### 6. Macro: two channels kept separate (`us_lvt_macro_channels.csv`, `us_lvt_impulse.csv`, `us_lvt_collateral.csv`, `us_lvt_ltv.csv`, `us_lvt_capitalization.csv`, `us_lvt_nonoccupier.csv`, `us_lvt_vat_levy.csv`)

(i) **Price level.** VAT: 8.3% [7.4, 9.3] at 80-100% pass-through, the rebuild's number (post: 7-9%). LVT: 0. That
zero is incidence theory, not accounting. A tax on land rent is not a tax on transactions: rents are set by demand for
a fixed stock, the owner cannot shift the bill, and the price that falls is the land price, which is not in the
consumer price index. Nothing has to be indexed to a constant-tax index, no indexed contract is double-paid, and there
is no price step for the central bank to look through. The program still moves rents through demand. The dividend's
rent bar ($8.28 per share per month, 3.6% of rent spending) is extra demand for a fixed stock, a rent-price effect
separate from the tax's pass-through (Results 7).

(ii) **Demand.** Flow impulse at impact, % of consumption (CE 2024 budget, the post's denominator):

| Grade | VAT | LVT (a) L1 | LVT (a) L2 | LVT (b) L1 m1 | LVT (b) L2 m1 |
|---|---|---|---|---|---|
| Post mid, decile-netted (the post's method) | 0.389 | 0.976 | 1.242 | 1.129 | 2.194 |
| Post low / high | 0.474 / 0.305 | 1.188 / 0.768 | 1.505 / 0.983 | 1.374 / 0.888 | 2.658 / 1.736 |
| Monotone diagnostic schedule | 0.389 | 1.011 | 1.324 | 1.169 | 2.338 |
| Household: payers graded by liquidity (biweekly) | 0.314 | 0.885 | 1.183 | 1.023 | 2.089 |
| ... monthly hand-to-mouth band | 0.285 | 0.852 | 1.153 | 0.985 | 2.036 |
| ... every hand-to-mouth family at 1.0 | 0.441 | 1.114 | 1.457 | 1.288 | 2.572 |
| Measured windfall MPC by decile | 0.060 | 0.152 | 0.189 | 0.175 | 0.334 |
| Measured, decile × hand-to-mouth | 0.053 | 0.136 | 0.163 | 0.157 | 0.287 |
| Measured shape, scaled to 1.0 at D1 | 0.208 | 0.524 | 0.653 | 0.605 | 1.153 |

The schedule shape matters little: the monotone diagnostic moves the LVT by +3.6%, the VAT by nothing. The liquidity
grade lowers the VAT's impulse more (−19%) than the LVT's (−9%), because more of the VAT's payers inside the lower
deciles are hand-to-mouth.

Deferral (bridge rate, L1, m1; % of consumption):

| | none | owners 65+ defer | ... cash-balanced | wealthy-HtM owners defer | ... cash-balanced |
|---|---|---|---|---|---|
| Flow, post's method | 0.976 | 2.976 | 0.852 | 1.852 | 0.967 |
| Flow, liquidity-graded | 0.885 | 2.913 | 0.757 | 1.838 | 0.952 |
| Deferred share of revenue | 0 | 29.9% | 29.9% | 12.5% | 12.5% |
| Dividend | $249 | $249 | $175 | $249 | $218 |
| Deferrers' residual wealth effect, 3.5c (5c) | 0 | −2.30 (−3.29) | same | −0.96 (−1.37) | same |

Deferral removes the deferrers' cash bill (impact MPC 0 on it). If the dividend is still paid in full, the state lends
the deferred bills against the estates, and the extra impulse is that lending spent by recipients. If the dividend is
kept cash-balanced, the impulse barely changes. The deferrers' capitalized land loss remains. If they respond to it at
2-5 cents per dollar, the response (−1.3% to −3.3%) is about the size of the cash response they no longer make. It is
reported beside the flow and never added to it.

**Stock channel.** Capitalization at announcement, share of land value lost:

| Design | (a) L1 m1 | (a) L2 m1 | (b) φ = 0.98 |
|---|---|---|---|
| Immediate, credible permanent | 0.848 | 0.555 | 0.980 |
| Phase-in 5 / 10 / 20 / 30 years | 0.801 / 0.746 / 0.653 / 0.574 | 0.524 / 0.489 / 0.428 / 0.376 | 0.926 / 0.863 / 0.755 / 0.664 |
| Increment-only grandfathering (the repo's table, as for the phase-ins) | 0.349 | 0.229 | 0.404 |

The phase-ins and increment-only grandfathering both come from the repo's price-path table (`lvt_shock.csv`, annual
timing), scaled by φ/0.98. The continuous approximation φ·γ/δ would give 0.339 / 0.222 / 0.392 for increment-only;
on the clean concept the collateral result is the same either way (−0.11).

Owner-occupiers: none on top of the bill (T4). Collateral (L1, mortgaged owners crossing 80% LTV; MRTHEL includes
HELOCs; % of consumption, with the 10-cent stress value in brackets):

| | (a) immediate | (a) 10-y phase-in | (a) increment-only | (b) immediate |
|---|---|---|---|---|
| Aggregate LTV of owners, before → after | 28.7% → 44.4% | → 41.7% | → 33.6% | → 48.5% |
| Mortgaged owners underwater after (million, of 56.7) | 14.4 | 12.7 | 4.7 | 18.0 |
| Crossing 80% LTV (million; share of mortgaged) | 16.8 (30%) | 14.3 (25%) | 6.4 (11%) | 19.9 (35%) |
| ... of them hand-to-mouth (million) | 6.2 | 5.5 | 2.7 | 7.1 |
| Their lost borrowing capacity / lost equity, $bn | 1,246 / 2,834 | 914 / 2,107 | 169 / 410 | 1,751 / 3,948 |
| Share of the lost equity held by hand-to-mouth crossers; by families with ≥ 3 months' income in liquid assets | 28%; 40% | 29%; 41% | 33%; 34% | 28%; 40% |
| Their own-home bills at the full rate, $bn a year (= lost equity × r under the immediate designs: the T4 overlap) | 119 | | | 166 |
| Credit effect on lost capacity, all crossers, 4.7 / 6 / 7 c (10 c) | −0.65 / −0.83 / −0.97 (−1.38) | −0.48 / −0.61 / −0.71 (−1.01) | −0.09 / −0.11 / −0.13 (−0.19) | −0.91 / −1.16 / −1.36 (−1.94) |
| ... hand-to-mouth crossers only | −0.16 / −0.21 / −0.24 (−0.35) | −0.13 / −0.16 / −0.19 (−0.27) | −0.03 / −0.04 / −0.04 (−0.06) | −0.24 / −0.31 / −0.36 (−0.51) |
| On lost equity, includes the T4 overlap: all crossers, 4.7 / 6 / 7 c (10 c) | −1.48 / −1.88 / −2.20 (−3.14) | −1.10 / −1.40 / −1.63 (−2.34) | −0.21 / −0.27 / −0.32 (−0.45) | −2.06 / −2.63 / −3.06 (−4.38) |
| ... hand-to-mouth crossers only | −0.41 / −0.52 / −0.61 (−0.87) | −0.32 / −0.41 / −0.47 (−0.68) | −0.07 / −0.09 / −0.10 (−0.15) | −0.57 / −0.73 / −0.85 (−1.22) |
| At 6 c on the PCE denominator (× 0.455): credit all / hand-to-mouth; lost equity all | −0.38 / −0.09; −0.86 | −0.28 / −0.07; −0.64 | −0.05 / −0.02; −0.12 | −0.53 / −0.14; −1.20 |

The 4.7 cents are Aladangady (2017), and the 5-7 cents Mian, Rao and Sufi (2013), 6 central. The 10 cents are the
unit's own stress value, not a literature number. The crossers' lost equity is their own-home bills capitalized
($2,834bn = $119bn a year / r), and the flow already charges those bills at the decile MPCs ($79bn a year, 0.87% of
consumption, 0.66 per dollar of bill). A response to the lost equity on top of the flow therefore counts the same
money twice. At 6 cents it is 1.43 times the annual bill (6 cents > r = 4.2%), so together with the flow the crossers
would cut spending by 2.1 times their bill. The clean concept is the lost borrowing capacity: a credit effect, which is
not the present value of the bill. The never-both rule that the unit applies to non-occupiers applies here too, so the
lost-equity rows are band edges labelled "includes the T4 overlap".

On L2 at the bridge rate (φ 0.555) the aggregate LTV goes to 37.4% and 8.3 million owners are underwater. 10.3 million
cross 80% (4.1 million of them hand-to-mouth), with $470bn of lost borrowing capacity and $1,093bn of lost equity. The
credit effect is −0.24 / −0.31 / −0.36% at 4.7 / 6 / 7 cents (−0.52% at 10 cents; −0.09% if only hand-to-mouth
crossers respond). On lost equity it is −0.57 / −0.73 / −0.85% (−1.21% at 10 cents).

The memo's aggregate (§7.1: LTV 26% → 48% on Z.1 totals, with the land price at zero) holds within about one point like
for like. With the land price at zero, the SCF owners' LTV goes 28.7% → 49.2%, against Z.1's 26.0% → 48.2% (2024). The
SCF starts higher and its land share is lower (0.416 against 0.460), and the two offset. At full capture (φ = 0.98)
the SCF owners' LTV is 48.5%.

Across the four measures at the bridge rate, the 80% crossers number 9.7-17.3 million. The credit effect (6 cents) is
−0.27% (m4), −0.41% (m2), −0.83% (m1) and −0.88% (m3); on lost equity it is −0.64%, −0.94%, −1.88% and −2.04%. With
the 90% or 100% threshold the credit effect is about the same (+5% / −1%: each crosser of a higher threshold loses
more room), and the lost-equity reading is 10-27% smaller.

**The headline readings** (`us_lvt_headline.csv`; each crosser counted once unless labelled; the bands pair the
extremes: the high MPC schedule with 7 cents (5 cents on corporate land), the low schedule with 4.7 cents (2 cents)):

| Demand at impact, % of consumption (bridge rate, m1, immediate) | central | band | lower edge at 10c (stress) | central, % of PCE |
|---|---|---|---|---|
| VAT: flow + levy at λ = 0.35 (2-5c) | −1.37 | [−2.21, −0.53] |  | −0.62 |
| VAT at the measured windfall MPCs | −1.70 | [−2.45, −0.94] |  | −0.77 |
| **LVT L1: flow + credit effect on all crossers' lost borrowing capacity (the clean central)** | +0.15 | [−0.20, +0.54] | −0.61 | +0.07 |
| ... only hand-to-mouth crossers respond | +0.77 | [+0.52, +1.02] | +0.42 | +0.35 |
| ... crossers' stock response (lost equity) instead of their bill: the other clean reading | −0.04 | [−0.43, +0.44] |  | −0.02 |
| ... includes the T4 overlap: 6c on lost equity on top of the bill (band edge only) | −0.91 | [−1.43, −0.29] | −2.37 | −0.41 |
| ... landlords (other residential land) on the wealth reading, 3.5c (5c / 2c) | −0.23 | [−1.00, +0.56] |  | −0.11 |
| ... measured windfall MPCs (all crossers) | −0.68 | [−0.82, −0.50] |  | −0.31 |
| ... measured windfall MPCs, hand-to-mouth crossers only | −0.06 | [−0.09, −0.01] |  | −0.03 |
| **LVT L2, corporate land on the wealth reading, 3.5c (the clean central)** | +0.67 | [+0.10, +1.24] | −0.05 | +0.30 |
| ... only hand-to-mouth crossers respond | +0.89 | [+0.36, +1.41] | +0.31 | +0.40 |
| ... crossers' stock response instead of their bill | +0.59 | [+0.01, +1.20] |  | +0.27 |
| ... includes the T4 overlap (band edge only) | +0.25 | [−0.38, +0.91] | −0.75 | +0.11 |
| ... every non-occupier (rental, noncorporate, corporate) on the wealth reading | −0.13 | [−1.51, +1.22] |  | −0.06 |
| ... measured windfall MPCs | −0.79 | [−0.84, −0.72] |  | −0.36 |
| **LVT L2, corporate land on the flow reading** | +0.93 | [+0.62, +1.26] | +0.46 | +0.42 |
| ... only hand-to-mouth crossers respond | +1.15 | [+0.87, +1.43] | +0.83 | +0.52 |
| ... crossers' stock response instead of their bill | +0.86 | [+0.53, +1.23] |  | +0.39 |
| ... includes the T4 overlap (band edge only) | +0.52 | [+0.14, +0.94] | −0.23 | +0.23 |
| ... measured windfall MPCs | −0.12 | [−0.18, −0.06] |  | −0.06 |

The clean centrals use 6 cents on every 80% crosser's lost borrowing capacity at the central MPC schedule. The two
judgment calls that move the sign are the collateral concept (the T4 edge) and who responds (the hand-to-mouth edge).
The third is the MPC level: at the measured windfall MPCs the flows nearly vanish, and every measured reading in the
table turns negative (the L1 hand-to-mouth-only one barely, −0.06).

Non-occupying holders, either flow or wealth effect (bridge rate, m1, post's method):

| | flow (bill × MPC) | wealth effect 2c | 3.5c | 5c |
|---|---|---|---|---|
| L1 (other residential land: $152bn a year of bills, $3.6tn capitalized) | 0.976 | 1.197 | 0.594 | −0.008 |
| L2 (+ business and corporate land: $388bn, $9.2tn) | 1.242 | 1.714 | 0.181 | −1.353 |
| L2, corporate land only ($93bn a year of bills, $2.2tn capitalized) | 1.242 | 1.347 | 0.979 | 0.610 |

Because the capitalized loss is the bill divided by r (4.2%), a 3.5-cent wealth effect withdraws 0.83 dollars per
dollar of bill, more than the top decile's flow MPC (0.53-0.59). Corporate land is the one part of the base whose
holders never see a bill, so the wealth-effect reading is the natural one there, and the L2 central uses it for
corporate land alone. The rental and noncorporate landlords see their bills and stay on the flow. Taken alone, the
corporate-land switch moves the L2 flow by −0.26 at 3.5 cents (−0.63 at 5 cents, +0.10 at 2 cents).

VAT levy channel, impact version on the same SCF 2025 balance sheets: net worth $161.9tn (2024 $), which is 17.9×
CE consumption or 8.2× PCE; the 8% levy is $13.0tn.

| λ | 2c | 3.5c | 5c | 3.5c, % of PCE |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 0.35 | −1.00 | −1.76 | −2.51 | −0.80 |
| 1 | −2.87 | −5.02 | −7.18 | −2.29 |

Beside the post's published numbers: flow +0.38% (P662, the year-3 flow-only path; static flow 0.389%); central
−0.69% [−0.97, −0.14] (P663-P665); full A-K −2.7% [−3.3, −1.2] (P666-P668). The post pairs year-3 central values
with year-5 bands (the gate file's notes). Its model ramps the rate over three years and lets households rebuild, so
its levy response at year 3 (about −1.07 at λ = 0.35) is smaller than this unit's impact response on the CE
denominator. It is close to the impact response on the PCE denominator (−0.80; A-K −2.29 against the post's −3.1
levy part). Only signs and orders of magnitude are comparable. The like-for-like comparison is inside this unit:
the same SCF data and the same denominator, with the levy at the post's 2-5 cents.

### 7. The loop (`us_lvt_loop.csv`, `us_lvt_loop_rounds.csv`, `us_lvt_loop_landlord_gain_by_decile.csv`)

| | round-0 rent bar | land rent increment (ls 0.4) | extra dividend | % of dividend [ls 0.3-0.5] | q | 1/(1 − φ·ls·q) |
|---|---|---|---|---|---|---|
| LVT (a) L1 | $8.28 | $3.31 | $2.86 | 1.14 [0.86, 1.44] | 0.0495 | 1.017 |
| LVT (a) L2 | $10.32 | $4.13 | $2.32 | 0.93 [0.70, 1.17] | 0.0540 | 1.012 |
| LVT (b) L1 m1 | $9.57 | $3.83 | $3.83 | 1.33 [0.99, 1.67] | 0.0495 | 1.020 |
| LVT (a) L1, tenure-aware round 0 | $18.10 | $7.24 | $6.14 | 2.46 | | |
| VAT | $3.36 | $1.34 → landlords | 0 | 0 | | |

Under the VAT its own (smaller) increment, $4.5bn a year [3.4, 5.6] against the LVT's $11.1bn, goes to landlords.
Capitalized at r it is worth $107bn on m1 ($50bn to $139bn across measures and ls). The holders of rental land get it:
60% the top decile, 16% D9 (by ORESRE; 71% to D10 with noncorporate land). The tenure-aware rent bar ($4.00) makes it
about $127bn.

What the loop leaves out, both second order:
- *The rent-price effect.* The round-0 rent bar is extra demand for a fixed stock: $8.28 per share per month is 3.6%
  of rent spending (VAT: $3.36, 1.5%). Rents rise with it beyond the land-rent increment that the loop taxes back.
- *The landlords' receipt.* The loop charges the holders of rental land the tax on the increment ($9.4bn a year) but
  does not credit them with the extra rent they collect ($11.1bn). Credited, they keep 1 − φ of it, $1.7bn a year,
  against the whole $4.5bn under the VAT. At their MPC (0.61, the mid schedule weighted by rental land) the uncredited
  receipt is worth +0.07% of consumption under the LVT and +0.03% under the VAT. That would add 0.04 points to the
  LVT's flow lead. It stays outside the headline, which counts no first-round receipt of any producer.

Relation to T5. The gross fixed point R0/(1 − φ_r·τ) is the extra dividend here: φ_r is the land-rent content of the
spending a dollar of round transfer buys (ls·q = 0.020), and τ is φ. The geometric factor is 1.017, so the loop is
second-order, as T5 says. q is already T5's net quantity, (m_p − m_r): the rent bar per dollar moved from rental-land
holders (60% D10, who rarely rent) to everyone. With the decile basket q = 0.05. With tenure-aware baskets the round-0
bar is 2.2 times larger, which is T5's "shelter-heavy recipient baskets" made concrete: renters receive and owners
pay. At φ < 1, the fraction 1 − φ of the increment still leaks to landowners (15% at the bridge rate on m1).

### Robustness (`us_lvt_robustness.csv`, `us_lvt_s_band.csv`)

Bridge rate, m1:

| Variant | Base | φ | D1 | D5 | D9 | D10 | Net payers | Impulse (post) | Impulse (liquidity) | Credit effect (6c) | Net at impact (clean) | 6c on lost equity (includes the T4 overlap) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Main: SCF 2025, uniform s | L1 | 0.848 | 183 | 90 | −39 | −514 | 31.6% | 0.976 | 0.885 | −0.83 | +0.15 | −1.88 |
| SCF 2022 | L1 | 0.848 | 167 | 88 | −64 | −524 | 29.8% | 0.997 | 0.937 | −1.00 | 0.00 | −2.20 |
| s rising with home value | L1 | 0.848 | 193 | 106 | −41 | −588 | 27.4% | 1.090 | 0.993 | −0.79 | +0.30 | −1.79 |
| CE home-value distribution | L1 | 0.848 | 140 | 71 | −41 | −365 | | 0.672 | | | | |
| Main | L2 | 0.555 | 189 | 122 | −1 | −750 | 22.4% | 1.242 | 1.183 | −0.31 | +0.67 | −0.73 |
| SCF 2022 | L2 | 0.555 | 153 | 123 | −10 | −751 | 21.9% | 1.234 | 1.182 | −0.39 | +0.58 | −0.83 |
| NFC land, low ($1.7tn) | L2 | 0.593 | 186 | 116 | −3 | −724 | 22.9% | 1.207 | 1.141 | −0.35 | +0.74 | −0.83 |
| CE home-value distribution | L2 | 0.555 | 161 | 110 | −2 | −652 | | 1.043 | | | | |

The L2 net at impact takes corporate land on the wealth reading (3.5 cents), as in the headline.

## Figures

- `figures/us_lvt_net_by_decile.png`: net transfer per adult share by decile, VAT and LVT on L1 and L2, at the bridge
  rate and at full capture, plus the within-decile spread (10th-90th percentiles) for the VAT and LVT L1.
- `figures/us_lvt_demand_shifts_top15.png`: the 15 largest movers, VAT against LVT L1 (post's method and household
  level with tenure-aware baskets), in dollars and as shares of each version's own impulse.
- `figures/us_lvt_who_pays.png`: the share of families that are net payers by decile, and who makes the LVT's net
  payments (owners 65+, younger owners by hand-to-mouth status, non-owners).
- `figures/us_lvt_macro_channels.png`: the two channels. The price step (VAT 7.4-9.3%, LVT 0), then demand in three
  blocks (VAT, LVT L1, LVT L2): the flows, the levy, the collateral credit effect (all crossers and hand-to-mouth
  crossers), the lost-equity reading, and the net at impact with each crosser counted once (dot: central; line:
  band). On the net rows, open markers show the labelled readings that move the LVT's sign: includes the T4 overlap
  (square) and only hand-to-mouth crossers respond (triangle). A value column prints every central and band, and the
  post's published path is shown for orientation.

## Caveats

- **What "bridge-equivalent" equals.** The post's dividend is CE-based: the bridge's consumption budget is 45.5% of
  PCE, and the VAT raises $835bn on it. The LVT's revenue is national-accounts land rent. A VAT on national-accounts
  consumption would raise more: up to $1.83tn (a $548 dividend) if PCE's VAT-able share equalled CE's 61.7%. That
  overstates it, since PCE adds imputed rent and third-party-paid health care, both exempt, and the share is not
  computed here. Matching a dividend on that scale would need φ > 0.98 on L1 at every measure, and on L2 only m2 and
  m4 would do (0.90, 0.76). The comparison here is with the post's dividend as published.
- **Static and impact-period.** No ramp, no rebuild of wealth, no repricing beyond the loop; one year of flows.
- **First incidence.** The bill falls on announcement-date holders; land supply does not respond. Assessment,
  exemptions and rate design, which the post names as its reason for leaving the LVT unmodelled, are not modelled
  here either. A credible permanent rate is assumed.
- **Property-tax overlap.** State and local property taxes ($789bn in 2025) already tax land in part. Net new revenue
  is smaller, and the existing tax's land half is continuity (memo §1.1). Not netted, as in the memo.
- **Survey coverage.** SCF land at the top is better measured than CE consumption at the top, so the LVT's top-decile
  bill sits on firmer data than the VAT's. Mixing an SCF bill with a CE budget makes the top decile's % of budget an
  overstatement. The CE home-value variant bounds this from the other side.
- **Concept mismatches.** Z.1 books household-owned rental property in noncorporate business, while the SCF's ORESRE
  holds it; L1 follows the task (HOUSES + ORESRE calibrated to the household residual), so land is allocated slightly
  off between the L1 components and NNB, though the totals are exact. The paper's household residual leaves
  nonprofit structures and land inside "land"; the households-only concept is 17% smaller.
- **Corporate land** is attributed in full to SCF households by EQUITY. Foreign, government and defined-benefit
  holders own part of it, so L2's top-decile bills are an upper bound. The tax still collects the revenue.
- **Collateral.** The response band comes from studies of house-price changes that carry no tax bill and that mix
  wealth and credit effects. Under an LVT the owner-occupier's price fall is the bill capitalized, so the central
  applies the band only to the crossers' lost borrowing capacity (a credit effect). The lost-equity reading, which
  counts the bill twice (T4), is a labelled band edge. Who responds is not observed: the central takes every crosser,
  and the other edge only the hand-to-mouth crossers. Owners who stay below 80% lose some borrowing room too, and that
  is not counted. Owners already above a threshold before the tax lose no borrowing room they had, but sink deeper
  underwater: 14.4 million are underwater after the bridge-rate tax. The double-trigger default risk in memo §7.1 is
  not modelled.
- **Hand-to-mouth** without credit limits (not in the 2025 extract): a negative liquid position counts as HtM.
- **Measured MPCs** answer a one-month transitory windfall; the dividend is permanent.
- **Deferral liens** add to state borrowing: 30% of revenue, for as long as the deferrers live.

## What would change the answer

- **The collateral concept.** Counting the crossers' lost equity on top of their bills (the T4 overlap) turns the L1
  central from +0.15% to −0.91%, and to −2.37% with the high MPC schedule and the 10-cent stress value. How owners read
  a price fall that is their own tax bill capitalized is the LVT's λ.
- **Who responds.** If only the hand-to-mouth crossers respond through collateral, L1 is +0.77% and L2 +0.89%.
- **The collateral response.** At the literature's 4.7-7 cents, with the MPC schedules, L1 runs from −0.20% to +0.54%.
  The 10-cent stress value puts the lower edge at −0.61%.
- **The base and corporate land.** Adding business and corporate land (L2) lowers the rate on homes. With corporate
  land on the wealth reading L2 is +0.67%, and +0.93% on the flow reading. If every holder of non-occupied land cut
  spending on the capitalized loss at 3.5 cents instead of paying the bill from cash, L2 would be −0.13%.
- **The land rent-to-value rate.** If land rent is 50% of PCE housing (m4, r = 6.7%), the bridge-rate tax takes only
  53% of rent. The price falls 53%, and the credit effect is −0.27% (on lost equity −0.64%). At r = 4.0% (m3) it is
  −0.88% (−2.04%).
- **Grandfathering.** It removes most of the stock shock (credit effect −0.11%), and with it the revenue at launch. A
  phase-in does little for the stock: a 10-year phase-in still capitalizes 88% of the immediate loss.
- **A flatter MPC gradient** (the SCF windfall evidence) makes both flows small. Demand is then a pure stock story:
  the VAT's levy (−1.70%) against the LVT's collateral (L1 −0.68%; −0.06% if only hand-to-mouth crossers respond).
- **A national-accounts VAT base** would make the bridge's dividend larger than residential land can fund (above).
- **Land at the top closer to CE's distribution** makes the LVT less progressive: D10 −$365 instead of −$514, and an
  impulse of 0.67%.
- **Deferral design.** A cash-balanced deferral by owners 65+ costs 30% of the dividend (−0.12 points). An accrual
  deferral is a large deficit-financed stimulus while it lasts (+2.0 points).

## Independent verification

`checks/verify_independent_lvt_us.py` re-derives the unit from raw data without importing its code. Its first run gave
264 of 275 claims OK, with every number reproducing; this version applies its corrections. Run unedited afterwards,
it gives 266 OK and 9 BAD. The nine claims the first run marked BAD now read OK: the T4 overlap, who responds, the
literature attribution, one increment-only convention, the headline header, the VAT's own increment, the data-defect
paragraph, the hand-to-mouth MPC in D1, and "nearly every bar". The nine that remain BAD are hard-wired to the
pre-correction unit:
- *Capitalization, three rows (bridge L1, bridge L2, full L1).* The verifier still computes increment-only
  grandfathering with the continuous φ·γ/δ (0.339 / 0.222 / 0.392). The unit now reads it from the repo table, as the
  verifier's own review claim asked (0.349 / 0.229 / 0.404). The immediate and phase-in values agree.
- *The collateral grid.* Same cause: only the increment-only rows differ. Every other row of `us_lvt_collateral.csv`
  and `us_lvt_ltv.csv` is unchanged from the version the verifier checked.
- *The headline table, L1 and L2.* The verifier hard-codes the pre-correction rows (−0.91 [−2.37, +0.54] and +0.52
  [−0.23, +1.26]) and their band definition. Those rows now carry the clean centrals (+0.15 [−0.20, +0.54] and +0.67
  [+0.10, +1.24]), which its review claim on the T4 overlap (now OK) asked for. The old centrals appear as the labelled
  T4 edges: −0.91, and +0.52 with corporate land on the flow reading.
- *The builder's own checks.* The verifier expects 228 PASS / 0 FAIL / 1 INFO of 229. The check script now has 261 / 0
  / 1 of 262: section K recomputes the corrected headline.
- *Corporate land in L2.* The verifier's +0.25 pairs the wealth reading for corporate land with the T4-overlap
  collateral (6 cents on lost equity). The L2 central uses that wealth reading, as asked, but on the clean collateral
  concept: +0.67. The verifier's +0.25 is reproduced as the L2 row's T4 edge.
- *Double rounding.* The verifier compares against its own copies of the old printed values (2.6, 4%, 0.58, −1.89,
  −1.17). These NOTES now print 2.5, 3%, 0.57, −1.88 and −1.16, taken from the unrounded CSVs.

## Data defect found

`consumption/data/tidy/scf2022_xvars.csv.gz` and `scf2022_roster.csv.gz` carry a wrong `IMPLICATE` for families
with YY1 ≥ 3277 (values 65537-65541). The cause was `acquire_fed.py` line 1135, `FULL["Y1"] - 10 * FULL["YY1"]`: YY1
comes out of the Stata file as a 16-bit integer, so 10·YY1 wrapped past 32,767. Commit aeba577 fixed that line with
an int64 cast, and the same expression in `build_scfp`. The two tidy files predate the fix and still carry the 6,625
bad values; the orchestrator will regenerate them. `Y1` is correct in both files. This unit merges on Y1 and
recomputes IMPLICATE = Y1 − 10·YY1, which reproduces the README's 225.0 million PEU adults and 74.1 million minors, so
the unit is unaffected before and after the regeneration. Until then, a merge on (YY1, IMPLICATE) silently drops 6,625
of 22,975 records.

## Files

- `code/lvt_us.py`: functions (SCF loading and payment units, Z.1 targets, rent measures, land holdings, KVW flags,
  accounting through `bridge.net_from_base`, MPC grades, collateral, the VAT levy channel, the loop, tenure-aware
  baskets, who pays).
- `code/run_lvt_us.py`: steps 1-7 and the figures.
- `checks/check_lvt_us.py`: 262 identity and recomputation checks (261 PASS, 1 INFO), the headline readings among
  them (section K); output `out/check_lvt_us.csv`.
- `checks/verify_independent_lvt_us.py`: the independent re-derivation (not imported from or edited by the unit);
  output `out/verify_independent_lvt_us.csv`.
- `out/`: `us_lvt_inputs.csv`, `us_lvt_phi.csv`, `us_lvt_s_calibration.csv`, `us_lvt_s_band.csv`,
  `us_lvt_land_by_decile.csv`, `us_lvt_accounting_by_decile.csv`, `us_lvt_who_pays.csv`,
  `us_lvt_payments_by_group.csv`, `us_lvt_mpc_grades.csv`, `us_lvt_feds_mpc_check.csv`, `us_lvt_impulse.csv`,
  `us_lvt_demand_shifts.csv`, `us_lvt_demand_compare.csv`, `us_lvt_decomposition_top10.csv`,
  `us_lvt_capitalization.csv`, `us_lvt_collateral.csv`, `us_lvt_ltv.csv`, `us_lvt_nonoccupier.csv`,
  `us_lvt_vat_levy.csv`, `us_lvt_macro_channels.csv`, `us_lvt_headline.csv` (every demand reading at impact, with
  its band, the 10-cent stress edge and the PCE denominator), `us_lvt_loop.csv`, `us_lvt_loop_rounds.csv`,
  `us_lvt_loop_landlord_gain_by_decile.csv`, `us_lvt_robustness.csv`, `check_lvt_us.csv`.
- `figures/`: the four PNGs above (200 dpi).
