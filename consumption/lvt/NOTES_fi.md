# Question 1, Finland: an LVT funding the bridge's dividend, through the bridge's machinery

Stella's question about the 2026-06-14 post: "I'm wondering if an LVT-UBI loop would respond in a similar way, how
similarly?" The post co-launches a land-value tax but leaves its incidence and revenue unmodelled ("Mechanism two:
the base"). This unit models it for Finland. A tax on land value funds the same flat dividend per adult share (each
child 0.3). The money runs through the rebuilt machinery (`consumption/rebuild/code/bridge.py`, imported unchanged)
on the same HBS 2022 population, beside the Finnish VAT bridge. There is no household microdata here: land,
liquidity and mortgages come from the published wealth-survey tables (2023 wave), calibrated to the household balance
sheet. The US unit is `NOTES_us.md`.

## The answer in plain words

**Can it be done? Not at the bridge's scale.** Finnish households own about €131bn of land (2022). At the 2022
ten-year yield of 1.69% its rent is about €2.2bn a year. Taking 98% of it funds a dividend of €37 a month per adult
share. That is 19% of the VAT bridge's €199 (€193 under the post's own conventions).
- With the paper's +1.5-point band it funds €70 (35%).
- At the 2023-25 yields (2.9-3.0%) it funds a third, or half with the band.
- Adding firms' and non-profits' land lifts it to 25-48%.
- Residential land alone funds 15-28%.

Raising the bridge's €11.5bn from land would take a charge of 8.9% of land value a year. That is 5.2 times the
whole rent. Its present value equals the whole value of the dwellings on the land, so it would be a levy on owners,
not a tax on land rent (T4: τ > 1 is incoherent on this base). Only the paper's US flow measure "50% of housing
services", applied to Finnish housing services, would fund it. That measure implies land rent of 15% of land value a
year, which the balance sheet does not support.

**If it could be done, how similar would it look?** As in the US: the same direction and more of it. At the same
revenue the LVT is about twice as redistributive as the VAT.
- The bottom quintile gains €117 a month per share instead of €80.
- The top quintile pays €175 (6.2% of its budget) instead of €84 (3.0%).
- The fourth quintile is at break-even.

All 37 category bars keep their sign. Each LVT bar is the VAT bar times about 1.8 (US: 2.5). The ratio is smaller
because Finnish land is less top-heavy: the top income decile holds 28% of it, against 39% in the US. Rent stays the
largest mover, with 40% of the impulse against the VAT's 44%. Under the post's method the flow impulse is 0.77% of
consumption, against the VAT's 0.42%.

**Inside the quintiles it is a different instrument.** Whatever the rate, 35% of households pay net under the LVT,
and all of them are owners. Renters pay nothing; they are 36% of households and 73% of the bottom decile.
- *Tenure-aware baskets.* Put rent in renters' baskets and owner costs in owners'. The LVT's rent bar is then 2.5
  times the quintile-netted one (€16.9 against €6.9) and housing-company charges fall. The VAT's rent bar barely
  moves (€4.4 against €4.2).
- *The verifier's MPC worry.* It is real, but in Finland it cuts the other way. The LVT's payers in the bottom three
  deciles are owners with savings: 17-18% of them are hand-to-mouth by deposits, against 31-37% of all households
  there. Suppose unconstrained payers draw on wealth, with MPC 0.56 whatever their income. Then the flow impulse
  rises: from 0.77% to 1.08% at the bridge's revenue, and from 0.14% to 0.20% at full capture.

**The macro channels.** There is no price step (the VAT's is 8.9% [7.9, 9.9]), so no indexation plumbing and no λ.
Instead there is a stock shock at announcement: at full capture land prices fall 98% and dwelling values about 19%.

At what land can actually fund (full capture, 2022 yield), the flow impulse is +0.14% of consumption. The collateral
channel follows the US unit's corrected concept: a credit effect on the lost borrowing capacity of mortgaged owners
crossing 80% LTV. That is 122,000 owners, 14% of the mortgaged, and the effect is −0.11%. Net demand at impact is
**+0.04% [−0.01, +0.10]**, about where the post put the Finnish VAT (+0.04%).

The sign turns on how holders read their land loss.
- *Lost equity.* Applied to crossers' lost equity, which counts the bill twice, the net is −0.11%.
- *Non-occupiers' capitalized losses.* Cottages, rental dwellings, forest and farmland are 43% of Finnish household
  land. If their holders respond to their capitalized loss at the post's 3.5 cents, rather than to their bills, the
  net is −1.05% [−1.80, −0.29].
- *Why that loss is so large.* At the 2022 yield it is 59 times their bill. Low yields make Finnish land expensive
  relative to its rent, so a land tax that raises little destroys a lot of value.

**Does the US-Finland gap narrow? Yes, but not for the reason the post gives.**
- *The premise holds.* Land is far less top-heavy than financial wealth: the top income decile holds 29% of
  residential land in Finland and 39% in the US, against 51% and 66% of financial assets.
- *But concentration feeds only the flow channel.* There, the US raises more demand per euro, not less.
- *What closes the gap is that an LVT has no levy channel.* Under the VAT the whole US-Finland gap is the levy on
  net worth (1.2 points at impact on the same formulas; 0.7 points in the post), and the US has far more net worth.
- *On the clean reading both LVTs sit near zero.* At full capture the US is at −0.04% and Finland at +0.04%. At the
  same revenue the US is at +0.17% and Finland at +0.04%.
- *The gap reopens through the LVT's own stock channel, in opposite directions.* Crossers' lost equity hits the US
  (−1.50% against −0.11%), because land is 42% of US house values and 20% of Finnish ones. Non-occupiers'
  capitalized losses hit Finland (−1.05% against −0.48%).

So the post's prediction holds in outcome. On the central reading the gap shrinks from about a point to about a tenth
of a point. The mechanism, though, is the removal of λ, not land's lower concentration.

## Run

```
venv/bin/python -I consumption/lvt/code/run_lvt_fi.py      # about 20 s; writes out/fi_lvt_*.csv and figures/fig_fi_*.png
venv/bin/python -I consumption/lvt/checks/check_lvt_fi.py   # 85 PASS / 0 FAIL / 8 INFO; writes out/check_lvt_fi.csv
```

`bridge.py` is imported, not forked, and was not edited; no hook was needed (`net_from_base`, `per_share_monthly`,
`shifts_from_transfers(shock=...)`, `impulse(shock=...)`, `decompose`, `fi_eta_table`, `fi_vat_accounting` carry
everything), so the rebuild's gates are untouched. The checks re-derive the VAT side's dividends (193.01 post, 198.82
coherent), the published rent bar (4.928) and the division-parent over-allocation (1.052).
- *The yield files.* The yields were vendored once through `consumption/code/common.py`'s `fetch()`:
  - `data/raw/eurostat/data/irt_lt_mcby_{a,m}_FI.json`, added to that folder's `MANIFEST.csv`;
  - `data/raw/ecb/data/IRS_M.FI.L.L40.CI.0000.EUR.N.Z.csv`, with a new `MANIFEST.csv`.
- *The US numbers.* The comparison reads the US unit's outputs at run time. The US unit was revised while this unit
  ran, after its verifier found the collateral double count (commit b945fc8). This unit reads the revised outputs
  (bridge-rate central +0.15%, as `NOTES_us.md` now reports) and uses the same corrected concept. Rerun
  `run_lvt_fi.py` to refresh the comparison; check I3 fails if the US headline changes again.

## Method

The post's tiers: **accounting** = identities and mechanical arithmetic; **calibrated** = named behavioural
parameters with bands.

1. **Land by income decile (accounting, with judgment shares).**
   - *Items.* Wealth survey 2023 (vtutk 151u), mean per household by income decile:
     - main residence, other residential property and free-time residences (dwellings);
     - forest, farmland and business (FFB).
   - *Dwelling land share.* s_d = 1 − N111 / (survey dwelling value) = **0.197**: the paper's residual construction
     (market value of dwellings minus structures at current cost), with the survey's market values and the balance
     sheet's residential buildings (rtp 11zx, S14, 2023).
   - *FFB land share.* s_f = (N211 − s_d × dwellings) / FFB = **0.763**, so household land equals the balance sheet's
     N211 (€126.3bn) in the survey year.
   - *To 2022.* Every decile's land × N211 end-2022 / end-2023 = **1.0415**, the balance-sheet land series. Household
     land 2022 = €131.5bn.
   - *Bases.* B1 = residential land (US L1's analogue); B2 = B1 + FFB land = all household land (main).
   - *Quintiles.* Decile pairs averaged into the HBS 2022 household quintiles (both groupings are household-weighted).
2. **Rates (accounting).**
   - *The charge.* tau = φ × r a year on announcement-date land value. r is the 10-year yield (Eurostat EMU
     convergence series for Finland, annual 2022 = 1.69%; the ECB's identical series agrees to 0.002 points). m2
     adds the paper's 1.5 points.
   - *Sensitivities.* The 2023-25 yields. The paper's US flow measures (30% and 50% of housing services). Housing
     services × s_d.
   - *(a) Bridge-equivalent.* tau such that the dividend equals the VAT's: €198.82 (coherent) or €193.01 (post);
     then φ = tau / r.
   - *(b) Full capture.* φ = 0.98.
3. **Incidence (accounting).** `bridge.per_share_monthly` turns land per household into land per share. Then
   `bridge.net_from_base` gives net_q = dividend − tau × land_q, balanced under each convention's own weights.
4. **Inside the deciles (accounting with judgment).** No microdata, so the split is parametric.
   - *Owners' land.* Owners (main-residence participation, 27% in D1 to 92% in D10) hold the decile's land,
     log-normally spread. The dispersion comes from the published main-residence quartiles of holders.
   - *Who pays.* A household pays net if its land exceeds the mean land per share × its shares. That rule does not
     depend on the rate.
   - *VAT payers.* VAT-able spending is log-normal inside quintiles, σ = 0.45 (judgment).
   - *Liquidity.* Hand-to-mouth = deposits at or below half a month's disposable income (KVW with Finnish monthly
     pay). Deposits are log-normal through the published quartiles. Owners' rates are scaled by the tenure table's
     (151z) outright and mortgaged ratios.
5. **MPC grades (calibrated).**
   - *The post's grade.* The rebuild's quintile schedule (mid 1.000 / 0.940 / 0.814 / 0.688 / 0.562; low and high
     bands), applied to quintile nets.
   - *Liquidity grade.* Recipients at the schedule; payers at 1.0 if hand-to-mouth, else at the schedule.
   - *Wealth grade (the verifier's variant).* Recipients at the schedule; payers at 1.0 if hand-to-mouth, else at
     0.56 whatever their income (band 0.25-0.68).
   - *Deferral.* Outright owners defer the bill on their main-residence land.
6. **Demand (calibrated).** dC_q / B_q enters `bridge.shifts_from_transfers(shock=...)`, the post's θ·η machinery,
   in both conventions.
   - *Coherent (main).* Equal-household weights, the per-household table.
   - *Post.* Equal consumption units; reproduces the published VAT bars.
   - *Tenure-aware baskets (an extension, as in the US unit).* Actual rent sits with renters. Imputed rent, interest on
     housing loans and housing-company charges sit with owners. Elasticities are re-evaluated at each basket with
     `bridge.fi_eta_table`.
7. **Macro.** Two channels, kept apart.
   - *(i) Price level.* VAT: 15% × the aggregate VAT-able share (0.661) × 80-100% pass-through. LVT: 0.
   - *(ii) Demand.*
     - The flow impulse, every grade.
     - The VAT's levy, impact version as the US unit computes it: −mpw × λ × levy × survey net worth.
     - The LVT's stock channel, at decile level from housing loans against dwelling values (151u/151z): price falls by
       φ, or by the repo's phase-in and increment-only paths (`three-taxes/data/lvt_shock.csv`).
     - Collateral: the credit effect on crossers' lost borrowing capacity (clean), and lost equity (T4 overlap,
       band edge).
     - Non-occupiers: flow or wealth effect, never both.
     - The loop (T5).

## Judgment calls, bands and their effect

| Call | Choice | Band / alternatives | Effect on the headline |
|---|---|---|---|
| Dwelling land share s_d | 0.197, the residual (survey dwelling value − N111) | 0.13 (own vs rented plot price gap within region groups, a lower bound) to 0.24 (N211 / (N211 + N111) 2023, an upper bound), N211 held | funding share unchanged (N211 fixes the total); collateral −0.05 to −0.16; net at full capture +0.09 to −0.01 |
| FFB land share s_f | 0.763, the residual from N211 | 0.5-1.5, total departs from N211 | funding share 17-23%; net +0.03 to +0.06 |
| 2023 → 2022 | N211 end-2022 / end-2023 | mid-2022 level (mean of end-2021, end-2022) | φ 5.31 vs 5.24; nets unchanged in shape |
| Yield year | 2022, the flow year (1.69%) | 2023 3.04%, 2024 2.85%, 2025 3.00% | funding share 19% → 32-34%; flow at full capture 0.14 → 0.24-0.26; net +0.04 → +0.14-0.15 |
| Bridge target | the post's flags (€193 post / €199 coherent) | Finnish law line by line: €172.4 post / €178.0 coherent (the rebuild verifier's central law reading: €168.3) | φ 5.24 → 4.70; funding share 19% → 21% |
| Owners' land inside deciles | log-normal, σ from main-residence quartiles; renters' land (2.5% nationally) assigned to owners | none | who pays (35% of households); only the liquidity and wealth grades use it |
| Hand-to-mouth | deposits ≤ income/24 (half a month) | income/52 (the US unit's main), income/12 | wealth-grade flow at full capture 0.169-0.221 vs 0.201 |
| Unconstrained payers' MPC | 0.56 (the schedule's top) | 0.25 (judgment, below FHN's first-year one-half); 0.68 (high schedule's top) | flow at full capture 0.115-0.434 vs 0.201; at the bridge revenue 0.617-2.324 vs 1.076 |
| VAT spending dispersion inside quintiles | σ = 0.45 | 0.30-0.60 | VAT liquidity and wealth grades only |
| LTV shape inside deciles | US-shape: SCF 2025 mortgaged families by income decile, rescaled to each Finnish decile's count, mean value and aggregate LTV | log-normal, median 1.1 × aggregate, σ 0.5-0.8 (calibrated on the US microdata: it gets the US crossers' lost capacity within −16% to +1%) | collateral −0.08 to −0.12 vs −0.105 |
| Mortgaged owners' dwelling values by decile | 151z national means split by the decile's outright/mortgaged counts, scaled to the national total | none | LTVs by decile |
| Collateral response | 6c on crossers' lost borrowing capacity (4.7c Aladangady; 7c Mian-Rao-Sufi top); 10c stress | on lost equity (T4 overlap, band edge); hand-to-mouth crossers only | −0.105 [−0.123, −0.082], stress −0.175; T4 −0.253; hand-to-mouth −0.014 |
| Wealth-effect propensity | 3.5c (2-5c, post fn 31) | none | VAT levy; non-occupier and deferral alternatives |
| Deferral group | outright owners (no housing loan) | none: the tables do not cross age with tenure or income | see results |
| The loop | land share of a rent change = s_d; household landlords hold 55% of rental land | 0.13-0.30; 0.40-0.70 | extra dividend 0.18-0.72% of the dividend |

## Results

### 1. Land, and the evidence on its share (`fi_lvt_land_evidence.csv`, `fi_lvt_plot_gap_2022.csv`, `fi_lvt_land_by_decile.csv`)

How the residential land share is bounded:
- **Below:** the own-plot vs rented-plot price gap of housing-company dwellings. A buyer on a rented plot does not buy
  the land and pays ground rent instead, so the gap is the capitalized plot.
  - Old dwellings, whole country 2022: 9.4%.
  - Within region groups (major cities 16.6%, the rest 13.6%), sales-weighted: 15.0%.
  - New blocks of flats: 9.0% nationally, 18.8% in Greater Helsinki.
  - Why these are lower bounds: municipal ground rents sit below market, and rented plots (22% of sales) cluster in
    high-price cities, which pulls the national gap down.
- **Above:** the household balance sheet's N211 / (N211 + N111), 25.9% (2022) and 23.9% (2023). N211 also holds
  forest and farmland.
- **The single-family plot prices (kihi 11jc)** cannot give a share without matching house values. They show the
  regional spread instead: a mean plot cost €73,000 nationally in 2022 (€25.9/m² × 2,837 m²), €316,000 in Greater
  Helsinki and €41,000 in municipalities under 20,000.
- **The residual, 19.7%, sits inside the bounds.**
- **The FFB item.** The publisher values its forest at the bare-land taxation comparison value, which "does not
  reflect the real market value of forest land". So the survey's forest carries no timber and sits below market.
  Farmland is at purchase prices, and business net wealth is mostly not land: hence the wide s_f band.

| Top income decile's share (151u 2023) | Finland | US (SCF 2025) |
|---|---|---|
| Residential land | 28.8% | 39.4% |
| All land in the wider base (definitions differ) | 28.1% | 51.5% |
| Financial assets | 50.9% | 65.6% |
| Net wealth | 37.3% | 61.3% |
| VAT-able consumption (top quintile) | 32.7% | 36.6% |

### 2. The tax: can household land fund the bridge? (`fi_lvt_phi.csv`, coherent; post within 0.1 point)

| Base, measure | r | φ for the €199 dividend | Full-capture dividend | Share of the bridge's |
|---|---|---|---|---|
| All household land (B2), 2022 yield | 1.69% | 5.24 | €37.2 | 18.7% |
| B2, 2022 yield + 1.5 | 3.19% | 2.78 | €70.1 | 35.3% |
| B2, 2023 / 2024 / 2025 yield | 3.04 / 2.85 / 3.00% | 2.92 / 3.11 / 2.96 | €66.8 / €62.7 / €65.9 | 33.6 / 31.5 / 33.1% |
| B2, 2023-25 yield + 1.5 | 4.35-4.54% | 1.95-2.04 | €95.6-99.8 | 48-50% |
| Residential land (B1), 2022 yield / + 1.5 | 1.69 / 3.19% | 6.72 / 3.56 | €29.0 / €54.7 | 14.6 / 27.5% |
| All private land (households, firms, non-profits: €176.9bn) | 1.69 / 3.19% | 3.86 / 2.04 | €50.5 / €95.4 | 25.4 / 48.0% |
| B1, housing services × s_d (€6.1bn) | 6.0% | 1.90 | €102.6 | 51.6% |
| B1, 30% of housing services (US measure) | 9.1% | 1.25 | €156.2 | 78.6% |
| B1, 50% of housing services (US measure) | 15.2% | 0.75 | €260.4 | 131.0% |

No yield-based case funds the bridge. The bridge-equivalent charge is 8.9% of land value a year (B2), or 11.4% on
residential land alone. Capitalized at the yield, it would take the dwellings' whole value at the 2022 yield, and 55%
of it at yield + 1.5 (`fi_lvt_capitalization.csv`).

Two comparisons:
- *Finnish VAT law as the target.* Against the €178.0 VAT dividend under Finnish law (coherent), φ is 4.70.
- *The US.* In the US, land rent is 10.9% of the survey consumption budget and the bridge needs φ = 0.85. In
  Finland land rent is 1.9% of it.

### 3. Incidence: net per adult share per month (`fi_lvt_accounting_by_quintile.csv`)

| Coherent convention | Q1 | Q2 | Q3 | Q4 | Q5 |
|---|---|---|---|---|---|
| VAT bridge, € (dividend 198.8) | +80.3 | +41.5 | +8.0 | −11.5 | −83.9 |
| LVT B2, same revenue (notional), € | +117.1 | +82.5 | +32.8 | −1.4 | −174.5 |
| LVT B1, same revenue (notional), € | +124.7 | +90.8 | +31.3 | −5.9 | −180.8 |
| LVT B2, full capture, 2022 yield (dividend 37.2), € | +21.9 | +15.4 | +6.1 | −0.3 | −32.6 |
| LVT B2, full capture, yield + 1.5 (dividend 70.1), € | +41.3 | +29.1 | +11.6 | −0.5 | −61.6 |
| VAT, % of budget | 6.1 | 2.6 | 0.4 | −0.5 | −3.0 |
| LVT B2 same revenue, % of budget | 8.9 | 5.2 | 1.7 | −0.1 | −6.2 |
| LVT B2 full capture, % of budget | 1.7 | 1.0 | 0.3 | −0.0 | −1.2 |

Under the post convention (VAT €193, the published Fig 1: +76.8 … −88.1) the same-revenue LVT gives +111.2, +76.7,
+26.9, −7.3 and −180.5. Every quintile but the top gains relative to the VAT; Q4 moves to near break-even.

**Inside the deciles** (`fi_lvt_within_decile.csv`, `fi_lvt_payer_shares.csv`):
- *Who pays.* 35.3% of households pay net, at any rate: 12% in D1, 27-36% in D4-D7, 80% in D10. All of them are owners.
  Under the VAT (judgment σ) payers rise from 8% of Q1 to 71% of Q5.
- *Netting hides payments in the lower deciles.* The bottom half makes 22.6% of all gross LVT payments. In D1-D2,
  gross payments are a fifth of gross receipts.
- *Liquidity* (`fi_lvt_liquidity.csv`): hand-to-mouth by deposits.
  - All households: 31% (D1), 37% (D2), 21% (D5), 7.5% (D10).
  - Owners: 17%, 18%, 12%, 5%.
  - Nationally (151z): outright owners 8.5%, mortgaged owners 21.6%, renters 36.2%.
  - Mean liquid assets are 9-15 months of disposable income in D1-D9 and 26 in D10. The median holder's deposits
    are 1.4-4.3 months.

### 4. Flow impulse by MPC grade (`fi_lvt_impulse.csv`, coherent, % of consumption)

| Grade | VAT | LVT B2 same revenue | LVT B2 full capture | LVT B2 full, yield + 1.5 |
|---|---|---|---|---|
| The post's schedule (mid) [high, low] | 0.422 [0.322, 0.524] | 0.771 [0.598, 0.948] | 0.144 [0.112, 0.177] | 0.272 |
| Payers graded by liquidity | 0.339 | 0.659 | 0.123 | 0.233 |
| Unconstrained payers draw on wealth (0.56) [0.68, 0.25] | 0.502 [0.298, 1.056] | 1.076 [0.617, 2.324] | 0.201 [0.115, 0.434] | 0.380 |
| Post convention, the post's schedule | 0.438 | 0.792 | 0.148 | 0.279 |

At the same revenue the LVT/VAT flow ratio is 1.83 (B2) or 1.94 (B1), against 2.51 in the US. The liquidity grade
lowers both instruments, because hand-to-mouth payers cut one for one. The wealth grade raises the LVT more than the
VAT, because the LVT's payers in the bottom three quintiles are mostly liquid owners whom the schedule puts at
0.81-1.0.

**Deferral** (`fi_lvt_deferral.csv`):
- *Who and how much.* Outright owners' main-residence land is 27.1% of the revenue.
- *Dividend paid in full.* The state lends the liens, and the impulse rises by 0.37 points at full capture (1.98 at
  the bridge revenue; US 2.0).
- *Cash-balanced.* The dividend falls from €37.2 to €27.1, and the impulse by 0.02 points.
- *Their capitalized loss* remains: −1.04% of consumption at 3.5 cents [0, −1.49], reported beside the flow, never
  added to it.
- *Age.* The tables do not allow an age-based deferral. 151u and 151z do not cross age with tenure or income.
  Outright ownership is the closest published group, and it is also the group whose lien can rank first.

### 5. Demand shifts (`fi_lvt_demand_shifts.csv`, `fi_lvt_demand_compare.csv`, `fi_lvt_decomposition_top10.csv`, `fi_lvt_tenure_aware.csv`)

Euros per adult share per month, coherent convention, same revenue, mid schedule:

| Category | VAT | LVT B2 (post's method) | LVT B2 tenure-aware, wealth grade | VAT tenure-aware |
|---|---|---|---|---|
| 04.1 Actual rents | +4.21 | +6.87 | +16.88 | +4.42 |
| 01.1 Food (at home) | +0.93 | +1.66 | +2.05 | +0.95 |
| 08.3 Information and communication services | +0.50 | +0.92 | | |
| 07.2 Operation of personal transport equipment | +0.43 | +0.85 | | |
| 07.1 Purchase of vehicles | −0.43 | −0.70 | −0.36 | −0.42 |
| 04.4 Water and misc. dwelling services (incl. housing-company charges) | +0.27 | +0.59 | −0.73 | +0.22 |
| Off chart: imputed rentals / interest on housing loans | −0.78 / −0.04 | −1.01 / −0.04 | −7.89 / −0.43 | −1.03 / −0.05 |
| Charted total | 9.68 | 17.27 | | |

**The post's method.** All 37 charted bars keep their sign, and the LVT/VAT ratio has median 1.80 over the bars
above €0.05.
- *Range.* 0.71 (13.9 other services, a small bar with mixed quintile signs) to 2.19 (04.4).
- *Rent.* 39.8% of the LVT's charted impulse, against 43.5% for the VAT.
- *On the post's own euro conversion.* Rent goes from €4.93 (the published bar) to €7.95, vehicles from −0.52 to
  −0.86, food from 0.92 to 1.63.
- *Fig 3 analogue.* Q5 supplies 98-99% of every top-10 withdrawal under the LVT, against 71-91% under the VAT. The
  LVT's Q4 is at break-even, so only the top withdraws.
- *Ghost flips.* 12 of the LVT's bars flip sign between the MPC=1 ghost and the MPC-adjusted bar, against 14 for the
  VAT; vehicle operation flips under both.
- *Under the wealth grade*, 35 of 37 bars keep their sign. Two near-zero bars flip: tools −0.005 → +0.013, other
  services −0.006 → +0.16.

**The tenure-aware version changes three things**, as in the US.
- Renters, who pay nothing under an LVT, spend 17-39 cents of an extra euro on rent at the margin (39 in the bottom
  quintile), where the quintile-average basket says 2-28 cents. So the rent bar is 2.5 times the netted one.
- Owners' cuts land on imputed rent and housing-company charges.
- The VAT barely moves, because renters pay VAT on their own spending.

The tenure-aware bars over all 47 lines still add up to the flow × 1.05, the division-parent factor.

### 6. Macro: two channels kept apart (`fi_lvt_macro_channels.csv`, `fi_lvt_headline.csv`, `fi_lvt_collateral.csv`, `fi_lvt_nonoccupier.csv`, `fi_lvt_vat_levy.csv`)

**(i) Price level.** VAT: 8.9% [7.9, 9.9]. LVT: 0. Land is in fixed supply and rents are set by demand, so nothing
passes through and nothing needs a constant-tax index.

**(ii) Demand at impact, % of consumption (HBS 2022 budget):**

| | central | band | stress (10c) |
|---|---|---|---|
| VAT: flow | +0.42 | [0.32, 0.52] | |
| VAT: levy, λ = 0.35 (survey net worth €647bn = 5.6 years of HBS consumption; levy 8.2%) | −0.56 | [−0.80, −0.32] | |
| VAT: net at impact, λ = 0.35 | −0.14 | [−0.48, +0.20] | |
| VAT: the post's published path, central / full A-K (year 3) | +0.04 / −0.65 | [−0.17, +0.29] / [−0.99, −0.09] | |
| LVT full capture: flow | +0.14 | [0.11, 0.18] | |
| LVT: collateral, credit effect on crossers' lost borrowing capacity (clean) | −0.11 | [−0.12, −0.08] | −0.18 |
| LVT: collateral on lost equity (T4 overlap, band edge) | −0.25 | [−0.30, −0.20] | −0.42 |
| LVT: collateral, hand-to-mouth crossers only | −0.01 | [−0.02, −0.01] | |
| LVT: collateral under a 10-year phase-in / increment-only grandfathering | −0.09 / −0.02 | | |
| **LVT: net at impact, flow + credit effect (2022 yield)** | **+0.04** | **[−0.01, +0.10]** | −0.06 |
| LVT: net, yield + 1.5 | +0.17 | [0.09, 0.25] | +0.04 |
| LVT: net, includes the T4 overlap | −0.11 | [−0.18, −0.02] | −0.31 |
| LVT: net, only hand-to-mouth crossers respond | +0.13 | [0.10, 0.17] | |
| LVT: net, crossers' stock response instead of their bill | −0.06 | [−0.14, +0.03] | |
| LVT: net, every non-occupier on the wealth reading | −1.05 | [−1.80, −0.29] | |
| LVT: net, unconstrained payers draw on wealth | +0.10 | [−0.01, +0.35] | |
| LVT at the notional bridge rate: flow + credit effect (dwellings worthless) | −2.77 | [−3.54, −1.83] | −5.31 |

**The collateral numbers behind these rows** (US-shape, full capture):
- *The price fall.* Dwelling values fall 19.3%.
- *LTVs.* Mortgaged owners' aggregate LTV goes from 48.2% to 59.7%; all owners' from 25.4% to 31.5%.
- *Crossers.* 121,500 mortgaged owners (14%) cross 80%. Those above 80% go from 175,000 to 296,000; those above
  100% from 47,000 to 172,000.
- *Euros.* Crossers' lost borrowing capacity is €2.0bn and their lost equity €4.9bn.
- *By decile.* Crossers concentrate in D6-D10, where the mortgages are (`fi_lvt_collateral.csv`).

**The two methods.** Both borrow a shape from the US. The US-shape population reproduces Finland's decile counts,
values and loans exactly, and its loan and value quartiles land within 4-32% of 151z's
(`fi_lvt_collateral_method_check.csv`). The Finnish distributions are wider than the US shape. The log-normal method
gives −0.08 to −0.12.

**Non-occupiers.** They hold 42.7% of B2 land. Their capitalized loss is 59 euros per euro of bill at the 2022 yield
(31 at yield + 1.5). On the wealth reading the impulse changes by −1.09 [−1.79, −0.39]; the US full-capture
equivalent is −0.44.

**The loop** (`fi_lvt_loop.csv`). At full capture the rent bar (€1.28) raises land rent by €14.7m a year. A
household-land tax takes back the household landlords' part, an extra dividend of 0.37% of the dividend [0.18, 0.72].
The multiplier is 1.005, second-order as T5 says. Under the VAT the increment (€48m a year, €2.8bn capitalized at the
2022 yield) goes to landlords.

### 7. The US beside Finland (`fi_lvt_us_compare.csv`; US figures read from the US unit's current outputs)

| % of consumption at impact | US | Finland | US − FI |
|---|---|---|---|
| VAT: flow (same formulas) | +0.39 | +0.42 | −0.03 |
| VAT: levy, λ = 0.35, 3.5c | −1.76 | −0.56 | −1.20 |
| VAT: net at impact | −1.37 | −0.14 | **−1.23** |
| VAT: the post's central path (year 3) | −0.69 | +0.04 | **−0.73** |
| LVT, same share of rent (φ 0.98): flow / credit effect | +1.13 / −1.16 | +0.14 / −0.11 | |
| LVT, φ 0.98: flow + credit effect | −0.04 | +0.04 | **−0.07** |
| LVT, the US bridge's share of rent (φ 0.85): flow + credit effect | +0.15 | +0.04 | +0.11 |
| LVT, same revenue (1.85% of consumption; US φ 0.17): flow + credit effect | +0.17 | +0.04 | +0.13 |
| LVT, φ 0.98: includes the T4 overlap | −1.50 | −0.11 | −1.39 |
| LVT, φ 0.98: non-occupiers on the wealth reading | −0.48 | −1.05 | +0.57 |
| LVT, same dividend as the bridge | +0.15 | −2.77 (not a land tax) | |

What is behind it:
- *Land.* Land's share of residential value is 0.416 in the US and 0.197 in Finland. Household land is 2.6 times
  the survey consumption budget in the US and 1.1 in Finland.
- *Rent.* Rent-to-value is 4.21% (US, 2024) against 1.69% (Finland, 2022), so land rent is 10.9% of consumption in
  the US against 1.9%.

### Robustness (`fi_lvt_robustness.csv`; B2, coherent unless stated)

| Variant | φ bridge | Full-capture share | Q5 net, same revenue | Flow, same revenue | Net, full capture (clean / T4) |
|---|---|---|---|---|---|
| Main | 5.24 | 18.7% | −174.5 | 0.771 | +0.039 / −0.109 |
| s_d 0.13 / 0.24 (N211 held) | 5.24 | 18.7% | −166.9 / −179.4 | 0.717 / 0.806 | +0.086 / −0.008 |
| s_f 0.5 / 1.5 | 5.67 / 4.33 | 17.3 / 22.6% | −176.4 / −170.6 | 0.785 / 0.743 | +0.030 / +0.063 |
| Carry to mid-2022 | 5.31 | 18.5% | −174.5 | 0.771 | +0.039 |
| Post convention | 5.25 | 18.7% | −180.5 | 0.792 | +0.043 |
| 14qa composition (coherent) | 5.25 | 18.7% | −174.0 | 0.780 | +0.041 |
| Yield 2023 / 2024 / 2025 | 2.92 / 3.11 / 2.96 | 33.6 / 31.5 / 33.1% | −174.5 | 0.771 | +0.154 / +0.138 / +0.151 |
| Residential land only (B1) | 6.72 | 14.6% | −180.8 | 0.817 | +0.014 |
| Finnish-law VAT target | 4.70 | 20.9% | −156.3 | 0.691 | +0.039 |
| Log-normal LTVs, σ 0.5 / 0.8 | | | | | +0.023 / +0.061 |

## Figures

- `figures/fig_fi_funding_gap.png`: what full capture funds, by base, measure and yield year, against the bridge's
  €199; and the share of dwelling value lost at announcement, Finland beside the US.
- `figures/fig_fi_net_by_quintile.png`:
  - net per adult share by quintile at the same revenue and at full capture (VAT, LVT on B2, LVT on B1);
  - households paying net by decile;
  - payers' hand-to-mouth shares.
- `figures/fig_fi_demand_shifts.png`: the 15 largest movers, VAT against LVT (the post's method and tenure-aware), in
  euros and as shares of each version's total.
- `figures/fig_fi_macro_channels.png`: the price step (VAT 8.9%, LVT 0); then demand: flow, levy, collateral and
  non-occupier rows with bands, and the post's published Finnish path.
- `figures/fig_fi_us_compare.png`: concentration (top-decile shares) and net demand at impact, US beside Finland, for
  the VAT and the LVT at three scales and two readings.

## Caveats

- **No microdata.** Who pays inside a decile, the hand-to-mouth shares and the LTV distribution are parametric splits
  of published means and quartiles. The LTV shape is borrowed from the SCF. Means, totals and the accounting tier are
  exact; the rest carries the bands above. The Finnish HFCS microdata (2023 wave) would replace all three.
- **Groupings.** Wealth-survey deciles and HBS quintiles are both household-weighted, but the ranking variables are
  not published and may differ (README_fin.md). Payment units are the rebuild's 12ew pair means, not HBS quintiles.
- **Land valuation.**
  - The survey prices dwellings at market m² prices, plot and building together. Housing-company flats on rented
    plots (22% of sales) carry no land for their owners: the municipality or other lessor holds it, outside B1 and
    B2.
  - Whether the survey's flat values include the housing company's loan share is not stated. If they do, and
    household debt excludes it, LTVs are understated.
  - Forest is at the bare-land taxation value (no timber, below market). N211's own forest valuation is not
    documented in the vendored files.
- **Years.** Land is the 2023 wave carried to 2022 by N211; net worth is deflated by the 2023 consumption deflator
  (1.043); LTVs are 2023's. The 2022 yield (1.69%) comes from a year when yields rose from 0.2% to 2.7%. The 2023-25
  rows show how much the yield year matters.
- **Static and impact-period.** No ramp, no rebuild of wealth, no repricing beyond the loop. The post's numbers come
  from its dynamic model and are compared for sign and size only.
- **First incidence.** The charge falls on announcement-date holders; land supply does not respond. Assessment,
  exemptions and rate design are not modelled; a credible permanent rate is assumed.
- **Overlaps.** Finland's municipal real-estate tax already taxes land in part; it is not netted (its size is not in
  the vendored data). The household-land tax leaves corporate and municipal land, rental housing companies' land
  included, untaxed; B3 adds firms' and non-profits' land for the revenue question only.
- **Measured MPCs.** Finland has no windfall question like the SCF's, so the US unit's measured-MPC grade has no
  Finnish counterpart. The wealth grade's 0.25 is the closest variant.
- **The deferral** uses outright owners, not older owners: age is not crossed with tenure in the published tables.

## What would change the answer

- **The yield.** At the 2023-25 yields, full capture funds a third of the dividend (half with the band) and net
  demand at impact is +0.14% to +0.15%. Higher yields mean more rent per euro of land value, so a land tax raises more
  and destroys less value per euro raised.
- **How holders read their land loss.**
  - *Owner-occupiers.* The clean reading treats their price fall as the bill they already pay (T4) and adds only the
    credit effect.
  - *Non-occupiers.* If holders of cottages, rental flats and forest cut spending on their capitalized losses at the
    post's 3.5 cents, the LVT at full capture is −1.05%: more negative than the VAT at λ = 0.35 (−0.14%) and than the
    US LVT on the same reading (−0.48%). This is the Finnish LVT's λ.
- **Taking more than the rent.** Any attempt to fund the bridge's dividend from land at 2022 yields turns the land
  tax into a levy on dwellings. The demand effect is then −2.8% (dwellings worthless) on the clean reading.
- **The land share.** At s_d = 0.24 the collateral effect is half as large again and net demand is −0.01%; at 0.13
  it is +0.09%.
- **The verifier's MPC variant.** If unconstrained payers draw on wealth, the LVT is more stimulative (+0.10% at full
  capture, up to +0.35% at an MPC of 0.25), because its low-income payers are liquid owners.

## Files

- `code/lvt_fi.py`: functions:
  - loading (wealth survey, balance sheet, national accounts, the yields through `common.fetch`);
  - land shares and holdings, the plot evidence;
  - accounting through `bridge.net_from_base`, the within-decile owner model, hand-to-mouth shares, MPC grades;
  - tenure baskets, capitalization, collateral (log-normal and US-shape), the VAT levy, the loop;
  - read-only US helpers.
- `code/run_lvt_fi.py`: steps 0-7 and the five figures.
- `checks/check_lvt_fi.py`: 85 re-derivations and identities plus 8 reported numbers; output `out/check_lvt_fi.csv`.
- `out/`: CSV tables, by step:
  - inputs and land: `fi_lvt_inputs.csv`, `fi_lvt_yields.csv`, `fi_lvt_land_evidence.csv`, `fi_lvt_plot_gap_2022.csv`,
    `fi_lvt_balance_sheet_ratio.csv`, `fi_lvt_land_by_decile.csv`, `fi_lvt_land_by_quintile.csv`,
    `fi_lvt_concentration.csv`;
  - rates and incidence: `fi_lvt_phi.csv`, `fi_lvt_accounting_by_quintile.csv`, `fi_lvt_within_decile.csv`,
    `fi_lvt_payer_shares.csv`, `fi_lvt_liquidity.csv`, `fi_lvt_liquidity_tenure.csv`, `fi_lvt_mpc_grades.csv`;
  - flows and demand: `fi_lvt_impulse.csv`, `fi_lvt_demand_shifts.csv`, `fi_lvt_demand_compare.csv`,
    `fi_lvt_decomposition_top10.csv`, `fi_lvt_tenure_aware.csv`;
  - macro: `fi_lvt_vat_levy.csv`, `fi_lvt_capitalization.csv`, `fi_lvt_collateral.csv`,
    `fi_lvt_collateral_lognormal_totals.csv`, `fi_lvt_collateral_method_check.csv`, `fi_lvt_nonoccupier.csv`,
    `fi_lvt_deferral.csv`, `fi_lvt_loop.csv`, `fi_lvt_macro_channels.csv`, `fi_lvt_headline.csv`;
  - comparison and robustness: `fi_lvt_us_compare.csv`, `fi_lvt_robustness.csv`, `check_lvt_fi.csv`.
- `figures/`: the five PNGs above (200 dpi).
