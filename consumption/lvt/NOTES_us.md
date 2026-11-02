# Question 1, US: an LVT funding the bridge's dividend, through the bridge's machinery

Stella's question about the 2026-06-14 post: "I'm wondering if an LVT-UBI loop would respond in a similar way, how
similarly?" The post co-launches a land-value tax but leaves its incidence and revenue unmodelled ("Mechanism two:
the base"). This folder models it. A tax on land rent funds the same flat dividend per adult share. The money runs
through the rebuilt machinery (`consumption/rebuild/code/bridge.py`, imported unchanged) on the same CE 2024
population, beside the VAT bridge.

## The answer in plain words

The two instruments are alike in direction, the LVT is much larger in size, and the stock channel that decides the
demand sign is a different one.

**What carries over.** Both instruments take from the top of the income distribution and pay a flat dividend, so the
demand tier tells the same story. All 36 charted category bars keep their sign. The make-up of the demand impulse is
nearly the same under both: rented dwellings is the largest mover (32% of the impulse), health insurance next (10%),
and new cars is the one large negative bar. Under the post's own decile method, every LVT bar is the matching VAT bar
times about 2.5. The flow impulse is positive under both, for the same reason (MPCs fall with income).

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
  recipient, since renters hold almost no land (1.4% of L1 payers are renters with other property). When the structural housing lines are split by tenure, two bars change. The LVT's rent
  bar doubles, to $18.10 a month from $8.28 decile-netted (VAT: $3.36, or $4.00 split the same way). Home maintenance,
  repairs and insurance turns negative (−$1.96 against +$0.81). Owners' mortgage interest (−$3.52) and property taxes
  (−$2.15) fall too, off the chart. The VAT barely moves under the same split. In this sense the payer basket moves
  away from the top's spending and toward homeowners' baskets.

**What vanishes.** The price step. The VAT raises the consumer price level by 7.4-9.3%. The LVT raises it by
nothing: land is in fixed supply and rents are set by demand, so there is nothing to pass through. That removes the
indexation plumbing (the constant-tax index for pensions, wages and contracts). It also removes the
Auerbach-Kotlikoff levy on existing wealth, together with its perception parameter λ, which the post calls its
"single most consequential judgment call".

**What appears instead.** A visible stock shock on land, and a collateral channel with it. Take a credible permanent
tax at the bridge rate (φ = 0.85 at the 10-year yield). It cuts land prices 85% at announcement, a $19.8tn loss. The
SCF owners' aggregate loan-to-value ratio goes from 29% to 44%, and 16.8 million mortgaged owners (30% of them) cross
80% LTV. At the housing-collateral responses in the literature (4.7-10 cents per dollar per year), that is −1.5% to
−3.1% of consumption. Counting only the lost borrowing capacity, it is −0.65% to −1.4%. So the LVT's demand sign at
impact turns on the collateral response, just as the VAT's turns on λ:

| Demand at impact, % of consumption (same SCF balance sheets, same bands) | central | band |
|---|---|---|
| VAT: flow + levy at λ = 0.35 | −1.37 | [−2.21, −0.53] |
| LVT at the bridge rate, base L1: flow + collateral | −0.91 | [−2.37, +0.54] |
| LVT at the bridge rate, base L2: flow + collateral | +0.52 | [−0.23, +1.26] |
| The post's published VAT path, central (year 3; year-5 band) | −0.69 | [−0.97, −0.14] |

The base matters here. With business and corporate land in the base (L2), the rate on homes falls to φ = 0.56, so
8.3 million mortgaged owners end up underwater instead of 14.4 million and the collateral channel is −0.73%. Flow plus
collateral is then +0.52%. That holds if the holders of business and corporate land respond to their bills. If they
respond to their capitalized loss at 3.5 cents per dollar instead, it is −0.55%.

**What it hinges on.**
1. *The collateral response of owners who lose borrowing room, and the capitalization design.* Increment-only
   grandfathering cuts the collateral channel to −0.26%. But it also leaves almost no revenue at launch, because only
   rent growth is taxed, and launch revenue is the bridge's whole job.
2. *The base.* L2 spreads the bill over $35.8tn of land instead of $23.4tn: a bigger flow (1.24%), a smaller
   collateral shock (−0.73%), and a top decile paying $750 a month per share.
3. *The rent-to-value rate.* At the bridge rate the bill is fixed, but the price fall it implies is not. It ranges
   from 53% (land rent = 50% of PCE housing) to 88% (30% of PCE housing) across the paper's four land-rent measures.
   The collateral channel ranges with it, from −0.6% to −2.0% (mid response).
4. *Deferral for older owners.* Owners over 65 owe 30% of the residential-land bill. If they defer it against their
   estates, either the state lends 30% of the revenue, which adds 2.0 points to the impulse while it lasts, or the
   dividend falls to $175 to stay cash-balanced. Their capitalized loss is then the open question: −2.3% of
   consumption at 3.5 cents per dollar, or 0 if they ignore it.
5. *MPCs.* The SCF 2025 windfall question measures MPCs of 0.29 at D1 to 0.18 at D10, a quarter of the post's level
   and a quarter of its slope. With them, both flow impulses nearly vanish (VAT 0.06%, LVT 0.15%), and the demand
   story becomes a pure stock story for both instruments.
6. *The top of the land distribution.* CE's own home values put 32% of residential land in the top decile, against
   39% in the SCF. That cuts the top decile's net payment from $514 to $365 and the impulse to 0.67%.

**The loop.** Under the LVT, the dividend's own rent bar raises land rent and the tax takes it back: +1.1% of the
dividend [0.9, 1.4], or 2.5% with tenure-aware baskets. Under the VAT, the same increment ($4.5bn a year of land
rent, worth $107bn at the 10-year yield) goes to landlords, 60% of them in the top decile. This is T5's arithmetic at
work: the gross multiplier is 1/(1 − φ·ls·q) = 1.017, second-order, as T5 says.

So the LVT bridge is a more redistributive version of the VAT bridge. It has the same demand fingerprint, with no
price step and no λ. Its macro risk sits in mortgage collateral instead of in perception, and a broader base shrinks
that risk.

## Run

```
venv/bin/python -I consumption/lvt/code/run_lvt_us.py       # about 35 s; writes out/us_lvt_*.csv and figures/
venv/bin/python -I consumption/lvt/checks/check_lvt_us.py   # 228 PASS / 0 FAIL / 1 INFO; writes out/check_lvt_us.csv
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
   ÷ 1.027027, the extract's own 2025→2024 factor). Base L1 = s · (HOUSES + ORESRE), with s set so that the
   SCF-weighted total equals the Z.1 2024 household land residual, $23,410.7bn. Base L2 adds the Z.1 noncorporate
   business land residual ($8,354.4bn, allocated by NNRESRE + BUS) and nonfinancial-corporate land ($3,994.6bn,
   assumed, allocated by EQUITY).
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
6. **Macro (accounting for the price level; calibrated for demand).** (i) Price level: VAT 15% × the 61.7% VAT-able
   share × 80-100% pass-through; LVT 0. (ii) Demand: the flow impulse for every rate × base × measure × MPC grade ×
   deferral variant (`us_lvt_impulse.csv`, 714 rows), then the stock channel. Capitalization: the land price falls
   by φ (credible permanent capture), by φ·γ/δ under increment-only grandfathering (γ/δ = 2%/5%, T4), and along the
   repo's phase-in table. No wealth effect is added for owner-occupiers, whose bill and price fall are the same money
   (T4). Collateral: LTVs of mortgaged owners (MRTHEL / HOUSES) before and after the land loss, and a response band
   applied to the owners who cross 80% / 90% / 100%. Non-occupying holders: either the flow (bill × MPC) or a wealth
   effect on the capitalized loss (2-5 cents per dollar per year), never both; both are shown. The VAT's levy channel
   is run in an impact version on the same SCF balance sheets: −mpw · λ · 8% · net worth.
7. **The loop (calibrated).** The rent bar raises land rent by its land share ls. At φ, that increment is taxed back
   and paid out as a flat extra dividend, financed by the holders of rental land. Each round runs back through the
   bridge, iterated to the fixed point and checked against the closed form φ·ls·R0/(1 − φ·ls·q).

## Judgment calls, bands and their effect

| Call | Choice | Band / alternatives | Effect on the headline |
|---|---|---|---|
| Land share of residential value s | uniform, calibrated: 0.416 (Z.1 2024 land / SCF 2025 property in 2024 $); Z.1's own aggregate ratio is 0.460 | 0.30-0.60 at a fixed aggregate property value | Bridge-rate nets and flows: none (a uniform s cancels). φ on the yield measures: 1.18 at s = 0.30 (infeasible on m1) to 0.59. Full-capture dividend (m1): $208-$416. Collateral: unchanged on the yield measures, −1.0% to −5.0% on m3 |
| s rising with home value | s = 0.30 + 0.30·F(V), F the weighted CDF of owners' home values, rescaled to Z.1 (effective 0.24-0.48) | judgment: expensive homes are expensive for their location | D10 −$588 vs −$514; impulse 1.09% vs 0.98%; collateral −1.79% vs −1.89% |
| Land concept | the paper's household residual (HH+NPO real estate − HH structures; nonprofit land and structures inside) | households-only owner-occupied residual, $19,374.9bn | φ on m1 = 1.02 (infeasible on L1); distribution unchanged |
| Matching year and dollars | SCF 2025 in 2024 $ vs Z.1 2024 | SCF 2025 nominal vs Z.1 2025: s = 0.406 | none on shares or nets |
| Survey year | SCF 2025 | SCF 2022 uprated: real 2024 $, land rescaled to Z.1 2024 (the 2022 distribution, uniformly uprated), roster adults; s = 0.442 | D10 −$524; impulse 0.997%; collateral −2.20% |
| NFC land after 2020 | NFC land share of NFC real estate at its 2016-2020 mean (0.255): $3,994.6bn | low: NFC structures grown at noncorporate current-cost growth ($1,699.8bn); high: 2020 share ($4,306.2bn) | L2 φ 0.550-0.593; D10 −$724 to −$753 |
| Noncorporate land key | NNRESRE + BUS | + ORESRE (Z.1 books household rental property in NNB); NNRESRE + ACTBUS | D10 −$733 / −$739 vs −$750 |
| Corporate land owners | 100% to SCF households pro rata to EQUITY | foreign, government and DB-pension holders (Z.1 L.223 not used) | L2's top-decile bills are an upper bound; revenue unaffected |
| Payment units, 2025 | adults = 1 + partner + 2022-roster cell mean (AGECL × MARRIED × min(KIDS, 3)); minors likewise; scaled to CE decile totals | 2022 in-sample: decile means within 0.06 shares | household per-share nets only; decile results exact by construction |
| Hand-to-mouth band | biweekly, INCOME/52: 32.0% HtM (21.2% wealthy) | monthly, INCOME/24: 40.2% (27.4%) | LVT household impulse 0.885% vs 0.852% |
| MPC grades | the post's mid schedule | low/high; monotone diagnostic; liquidity-graded; measured windfall (decile; decile × HtM; shape scaled to D1 = 1) | LVT L1: 0.70-1.19% (post family), 0.14-0.52% (measured); the LVT/VAT ratio stays 2.5-3.0 |
| Deferral take-up | 100% of the eligible | flows are linear in take-up | owners 65+: +2.0 points (dividend paid in full) or −0.12 (cash-balanced) |
| Collateral response | 4.7 / 6 / 10 cents per $ per year on crossers' lost equity | thresholds 80/90/100%; lost borrowing capacity instead of lost equity | −0.65% to −3.14% (bridge, L1, m1) |
| Wealth-effect propensity | 2 / 3.5 / 5 cents per $ per year (the post's fn 31; midpoint judgment) | none | VAT levy; LVT non-occupier alternative; deferrers' residual |
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

The 10-cent upper edge is a stress value (judgment): no source gives a number for the levered tail.

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
| LVT (a) L2, % of budget | 10.3 | 8.5 | 8.0 | 7.6 | 5.1 | 5.2 | 3.3 | 2.6 | −0.0 | −17.1 |

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
| Share of net payments by hand-to-mouth families | 14% | 7% | 4% |
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
families: lower, in fact, from D5 up, where the hand-to-mouth are mostly house-rich. The FEDS note finds +2.6 points
conditional on usual income (22.9% against 20.3%).

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
| Electricity | +0.64 | +1.60 | +2.02 | +0.58 | +1.42 |
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

What changes is what the decile method cannot see. In the tenure-aware version two bars flip (home maintenance, and
reading at −$0.002), the rent bar doubles and owner costs turn negative. LVT payers in D1-D8 are owners, mostly
retirees, so their withdrawal lands on owners' baskets. The recipients beside them are renters, who pay nothing
under an LVT, and renters spend 24-32 cents of an extra dollar on rent at the margin (owners 0.3 cents; the
decile-average basket that the post's method uses says 3-19 cents). Under the VAT, renters pay VAT on their own
spending, so their net is smaller and the split matters less (rent $4.00 against $3.36).

### 6. Macro: two channels kept separate (`us_lvt_macro_channels.csv`, `us_lvt_impulse.csv`, `us_lvt_collateral.csv`, `us_lvt_ltv.csv`, `us_lvt_capitalization.csv`, `us_lvt_nonoccupier.csv`, `us_lvt_vat_levy.csv`)

(i) **Price level.** VAT: 8.3% [7.4, 9.3] at 80-100% pass-through, the rebuild's number (post: 7-9%). LVT: 0. A tax
on land rent is not a tax on transactions: rents are set by demand for a fixed stock, the owner cannot shift the bill,
and the price that falls is the land price, which is not in the consumer price index. Nothing has to be indexed to a
constant-tax index, no indexed contract is double-paid, and there is no price step for the central bank to look
through.

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
| Increment-only grandfathering (γ/δ = 0.4) | 0.339 | 0.222 | 0.392 |

Owner-occupiers: none on top of the bill (T4). Collateral (L1, mortgaged owners; MRTHEL includes HELOCs):

| | (a) immediate | (a) 10-y phase-in | (a) increment-only | (b) immediate |
|---|---|---|---|---|
| Aggregate LTV of owners, before → after | 28.7% → 44.4% | → 41.7% | → 33.5% | → 48.5% |
| Mortgaged owners underwater after (million, of 56.7) | 14.4 | 12.7 | 4.6 | 18.0 |
| Crossing 80% LTV (million; share of mortgaged) | 16.8 (30%) | 14.3 (25%) | 6.3 (11%) | 19.9 (35%) |
| Their lost equity / lost borrowing capacity, $bn | 2,834 / 1,246 | 2,107 / 914 | 390 / 163 | 3,948 / 1,751 |
| Response at 4.7 / 6 / 10 c on lost equity, % of consumption | −1.48 / −1.89 / −3.14 | −1.10 / −1.40 / −2.34 | −0.20 / −0.26 / −0.43 | −2.06 / −2.63 / −4.38 |
| Response on lost capacity only (6 c) | −0.83 | −0.61 | −0.11 | −1.17 |

On L2 at the bridge rate (φ 0.555) the aggregate LTV goes to 37.4%, 8.3 million owners are underwater, and 10.3
million cross 80% with $1,093bn of lost equity: −0.57 / −0.73 / −1.21% at 4.7 / 6 / 10 cents (lost capacity only:
−0.31%). The memo's aggregate (§7.1: LTV 26% → 48% at full capture, on Z.1 totals) is reproduced on SCF owners:
28.7% → 48.5%. Across the four measures at the bridge rate, the 80% crossers number 9.7-17.3 million and the mid response is
−0.64% (m4), −0.94% (m2), −1.89% (m1) and −2.04% (m3). With the 90% or 100% threshold the response is 10-27% smaller.
The crossers' lost equity overlaps the bill they also pay (T4: the same money), so the MRS/Aladangady numbers applied
to it are an upper reading. The lost-capacity row isolates credit and is the lower one.

Non-occupying holders, either flow or wealth effect (bridge rate, m1, post's method):

| | flow (bill × MPC) | wealth effect 2c | 3.5c | 5c |
|---|---|---|---|---|
| L1 (other residential land: $152bn a year of bills, $3.6tn capitalized) | 0.976 | 1.197 | 0.594 | −0.008 |
| L2 (+ business and corporate land: $388bn, $9.2tn) | 1.242 | 1.714 | 0.181 | −1.353 |

Because the capitalized loss is the bill divided by r (4.2%), a 3.5-cent wealth effect withdraws 0.83 dollars per
dollar of bill, more than the top decile's flow MPC (0.53-0.59). For the corporate land in L2, where holders never
see a bill, the wealth-effect column is the natural reading.

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
same SCF data, same 2-5 cent band, same denominator.

### 7. The loop (`us_lvt_loop.csv`, `us_lvt_loop_rounds.csv`, `us_lvt_loop_landlord_gain_by_decile.csv`)

| | round-0 rent bar | land rent increment (ls 0.4) | extra dividend | % of dividend [ls 0.3-0.5] | q | 1/(1 − φ·ls·q) |
|---|---|---|---|---|---|---|
| LVT (a) L1 | $8.28 | $3.31 | $2.86 | 1.14 [0.86, 1.44] | 0.0495 | 1.017 |
| LVT (a) L2 | $10.32 | $4.13 | $2.32 | 0.93 [0.70, 1.17] | 0.0540 | 1.012 |
| LVT (b) L1 m1 | $9.57 | $3.83 | $3.83 | 1.33 [0.99, 1.67] | 0.0495 | 1.020 |
| LVT (a) L1, tenure-aware round 0 | $18.10 | $7.24 | $6.14 | 2.46 | | |
| VAT | $3.36 | $1.34 → landlords | 0 | 0 | | |

Under the VAT the increment, $4.5bn a year [3.4, 5.6], goes to landlords. Capitalized at r it is worth $107bn on m1
($50bn to $139bn across measures and ls). The holders of rental land get it: 60% the top decile, 16% D9 (by ORESRE;
71% to D10 with noncorporate land). The tenure-aware rent bar ($4.00) makes it about $127bn.

Relation to T5. The gross fixed point R0/(1 − φ_r·τ) is the extra dividend here: φ_r is the land-rent content of the
spending a dollar of round transfer buys (ls·q = 0.020), and τ is φ. The geometric factor is 1.017, so the loop is
second-order, as T5 says. q is already T5's net quantity, (m_p − m_r): the rent bar per dollar moved from rental-land
holders (60% D10, who rarely rent) to everyone. With the decile basket q = 0.05. With tenure-aware baskets the round-0
bar is 2.2 times larger, which is T5's "shelter-heavy recipient baskets" made concrete: renters receive and owners
pay. At φ < 1, the fraction 1 − φ of the increment still leaks to landowners (15% at the bridge rate on m1).

### Robustness (`us_lvt_robustness.csv`, `us_lvt_s_band.csv`)

Bridge rate, m1:

| Variant | Base | φ | D1 | D5 | D9 | D10 | Net payers | Impulse (post) | Impulse (liquidity) | Collateral (6c) |
|---|---|---|---|---|---|---|---|---|---|---|
| Main: SCF 2025, uniform s | L1 | 0.848 | 183 | 90 | −39 | −514 | 31.6% | 0.976 | 0.885 | −1.89 |
| SCF 2022 | L1 | 0.848 | 167 | 88 | −64 | −524 | 29.8% | 0.997 | 0.937 | −2.20 |
| s rising with home value | L1 | 0.848 | 193 | 106 | −41 | −588 | 27.4% | 1.090 | 0.993 | −1.79 |
| CE home-value distribution | L1 | 0.848 | 140 | 71 | −41 | −365 | | 0.672 | | |
| Main | L2 | 0.555 | 189 | 122 | −1 | −750 | 22.4% | 1.242 | 1.183 | −0.73 |
| SCF 2022 | L2 | 0.555 | 153 | 123 | −10 | −751 | 21.9% | 1.234 | 1.182 | −0.83 |
| NFC land, low ($1.7tn) | L2 | 0.593 | 186 | 116 | −3 | −724 | 22.9% | 1.207 | 1.141 | −0.83 |
| CE home-value distribution | L2 | 0.555 | 161 | 110 | −2 | −652 | | 1.043 | | |

## Figures

- `figures/us_lvt_net_by_decile.png`: net transfer per adult share by decile, VAT and LVT on L1 and L2, at the bridge
  rate and at full capture, plus the within-decile spread (10th-90th percentiles) for the VAT and LVT L1.
- `figures/us_lvt_demand_shifts_top15.png`: the 15 largest movers, VAT against LVT L1 (post's method and household
  level with tenure-aware baskets), in dollars and as shares of each version's own impulse.
- `figures/us_lvt_who_pays.png`: the share of families that are net payers by decile, and who makes the LVT's net
  payments (owners 65+, younger owners by hand-to-mouth status, non-owners).
- `figures/us_lvt_macro_channels.png`: the two channels. The price step (VAT 7.4-9.3%, LVT 0), then demand: flow,
  levy and collateral rows with their bands, and the post's published path for orientation.

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
- **Collateral.** The response band is taken from studies of house-price changes, which mix wealth and credit
  effects. Applying it to crossers' lost equity on top of the bill partly counts the same money twice (T4); the
  lost-capacity row is the clean credit effect. Owners already above a threshold before the tax lose no borrowing
  room they had, but sink deeper underwater: 14.4 million are underwater after the bridge-rate tax, against the
  double-trigger default risk in memo §7.1, which is not modelled.
- **Hand-to-mouth** without credit limits (not in the 2025 extract): a negative liquid position counts as HtM.
- **Measured MPCs** answer a one-month transitory windfall; the dividend is permanent.
- **Deferral liens** add to state borrowing: 30% of revenue, for as long as the deferrers live.

## What would change the answer

- **The collateral response.** At the low end (4.7 cents, lost borrowing capacity only), the LVT's demand at impact
  is +0.1% to +0.5% of consumption, a mild stimulus. At 10 cents on lost equity it is −2.2% (mid schedule) to −2.4%.
  This is the LVT's λ.
- **The base.** Adding business and corporate land (L2) lowers the rate on homes and turns flow plus collateral
  positive (+0.52%), unless the holders of that land cut spending on their capitalized loss (then −0.55%).
- **The land rent-to-value rate.** If land rent is 50% of PCE housing (m4, r = 6.7%), the bridge-rate tax takes only
  53% of rent. The price falls 53%, and collateral is −0.64%. At r = 4.0% (m3) it is −2.04%.
- **Grandfathering.** It removes most of the stock shock (−0.26%), and with it the revenue at launch. A phase-in does
  little for the stock: a 10-year phase-in still capitalizes 88% of the immediate loss.
- **A flatter MPC gradient** (the SCF windfall evidence) makes both flows small. Demand is then a pure stock story:
  the VAT's λ against the LVT's collateral.
- **A national-accounts VAT base** would make the bridge's dividend larger than residential land can fund (above).
- **Land at the top closer to CE's distribution** makes the LVT less progressive: D10 −$365 instead of −$514, and an
  impulse of 0.67%.
- **Deferral design.** A cash-balanced deferral by owners 65+ costs 30% of the dividend. An accrual deferral is a large
  deficit-financed stimulus while it lasts.

## Data defect found

`consumption/data/tidy/scf2022_xvars.csv.gz` and `scf2022_roster.csv.gz` carry a wrong `IMPLICATE` for families
with YY1 ≥ 3277 (values 65537-65541). The cause is `acquire_fed.py` line 1135,
`FULL["Y1"] - 10 * FULL["YY1"]`: YY1 comes out of the Stata file as a 16-bit integer, so 10·YY1 wraps past 32,767.
`Y1` is correct in both files. This unit merges on Y1 and recomputes IMPLICATE = Y1 − 10·YY1, which reproduces the
README's 225.0 million PEU adults and 74.1 million minors. Merging on (YY1, IMPLICATE) silently drops 6,625 of 22,975
records. Not fixed here (outside this unit); flagged for the acquisition owner.

## Files

- `code/lvt_us.py`: functions (SCF loading and payment units, Z.1 targets, rent measures, land holdings, KVW flags,
  accounting through `bridge.net_from_base`, MPC grades, collateral, the VAT levy channel, the loop, tenure-aware
  baskets, who pays).
- `code/run_lvt_us.py`: steps 1-7 and the figures.
- `checks/check_lvt_us.py`: 229 identity and recomputation checks; output `out/check_lvt_us.csv`.
- `out/`: `us_lvt_inputs.csv`, `us_lvt_phi.csv`, `us_lvt_s_calibration.csv`, `us_lvt_s_band.csv`,
  `us_lvt_land_by_decile.csv`, `us_lvt_accounting_by_decile.csv`, `us_lvt_who_pays.csv`,
  `us_lvt_payments_by_group.csv`, `us_lvt_mpc_grades.csv`, `us_lvt_feds_mpc_check.csv`, `us_lvt_impulse.csv`,
  `us_lvt_demand_shifts.csv`, `us_lvt_demand_compare.csv`, `us_lvt_decomposition_top10.csv`,
  `us_lvt_capitalization.csv`, `us_lvt_collateral.csv`, `us_lvt_ltv.csv`, `us_lvt_nonoccupier.csv`,
  `us_lvt_vat_levy.csv`, `us_lvt_macro_channels.csv`, `us_lvt_loop.csv`, `us_lvt_loop_rounds.csv`,
  `us_lvt_loop_landlord_gain_by_decile.csv`, `us_lvt_robustness.csv`, `check_lvt_us.csv`.
- `figures/`: the four PNGs above (200 dpi).
