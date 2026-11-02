# US rebuild: the VAT bridge's consumption machinery on CE 2024 deciles

The 2026-06-14 post ran a 15-point VAT surcharge, funding a flat per-adult dividend, through two tiers: an
accounting tier (who gains, who pays) and a demand tier (how each decile's budget change moves spending by
category). Its code was never committed anywhere we can reach, so this folder rebuilds the machinery from the
text and gates it on the published numbers (`data/tidy/post_published_numbers.csv`). The machinery is generic:
`shifts_from_transfers()` takes any per-share net-transfer vector, so the LVT step can run its own dividend
through exactly what the gate checks.

Result in one paragraph. All 36 Fig 5 bars come back within the printed rounding (±$0.005; RMSE $0.0027). The
ten largest movers come back in the published order. The accounting reproduces the $249 dividend, the 59-64% range,
D1's +4.8% and D10's -3.9%. Four of the ten Fig 4 net labels are off by $0.5 to $1.2 a month. Of the 301 published US
numbers the static machinery should reproduce, 256 PASS, 43 are CLOSE and 2 MISS. The two MISSes are the impulse in
the Fig 5 caption ("+0.4% of charted budget") and footer ("≈ +0.5% of consumption"), gated as the sum of the charted
bars over each label's own denominator. Swap the denominators and both PASS. The caption also passes on its own
denominator if its numerator is the flow impulse (0.442% of the charted budget); the footer has no such reading.

Which flags the outputs use: the EU Directive reading, except used cars (post-calibrated 1/2; the Directive's margin
scheme gives about 0.1), with rent at 0.0167. Two alternatives are carried beside it (`us_sensitivity.csv`,
`us_flag_variants.csv`). Rent at 0 is equally good: it fits the printed Fig 4 numbers better and the Fig 5 bars as
well, and only the read-off point positions prefer 0.0167. Used cars at 0.1 is what the Directive would give, but
the published figures rule it out.

## Run

```
venv/bin/python -I consumption/rebuild/code/run_us.py      # about 40 s; writes out/us_*.csv, figures/
venv/bin/python -I consumption/rebuild/checks/gate_us.py   # writes out/gate_us.csv, prints the summary
```

`run_us.py` re-derives every calibrated value and asserts that the constants in `bridge.py` equal what the
search finds, so the module and the evidence cannot drift apart.

## The method as rebuilt

Everything is in dollars per payment share per month. A share is one adult, or 0.3 for a child. Income group d is
a CE pretax-income decile.

- Payment units: adults = People - Children under 18 and shares = adults + 0.3 x children, from Table 1110's own
  composition rows (footnote 26). Population weight w_d = N_d x shares_d / sum, with N_d the printed CU count.
- Spending C_gd = annual mean per CU / 12 / shares_d. The 40 budget categories are the 36 bars of Fig 5, plus
  mortgage interest, property taxes and education (in the budget, off the chart), plus the residual of vehicle
  purchases. BLS dropped the "Other vehicles" row in 2024, so new plus used no longer exhaust the parent: the
  residual is $50 a CU a year, off-chart. Budget C_d = the sum of the 40 categories.
- Accounting: C_v,d = sum_g f_g C_gd with VAT flags f_g. Cbar_v = sum_d w_d C_v,d. Dividend = 0.15 Cbar_v.
  net_d = 0.15 (Cbar_v - C_v,d), so sum_d w_d net_d = 0 exactly.
- Market shares theta_dg = w_d C_gd / sum_d w_d C_gd. Cbar_g = sum_d w_d C_gd.
- Elasticities follow TB-1929 eq. 5, eta_gd = 1 + beta_k / w_kd. w_kd is decile d's observed share of USDA group
  k in its own consumption budget (off-chart rows included). Every category in a group inherits the group's eta.
  Food follows eq. 11, eta = eta_F,d x (1 + beta*_s / w*_s,d). Here w*_s,d is the observed share of the
  category's stage-two class in decile d's food-group spending, and food = food at home + away + alcohol + tobacco.
- Demand: shock_d = mpc_d net_d / C_d. dPct_g = sum_d theta_dg eta_gd shock_d. dUSD_g = dPct_g Cbar_g. The
  decile decomposition (Fig 6) is c_dg = w_d C_gd eta_gd shock_d. The ghost sets mpc = 1.
- Impulse: sum_d w_d mpc_d net_d. The betas sum to zero over the nine groups, and the three food classes' beta*
  sum to +0.001. So the impulse also equals the sum of all 40 bars, to $0.002.

## Every judgment call, its reason, and what pinned it

| Call | Choice | Reason | Pinned by | Alternatives tested |
|---|---|---|---|---|
| Budget rows | total expenditures minus personal insurance and pensions minus cash contributions, computed as the sum of the 40 lines (within $4 a CU-year of the printed rows, which CE rounds to whole dollars) | pensions, Social Security and life insurance are saving and contributions, cash contributions are transfers to others | Fig 4: D1 +4.8% and D10 -3.9% of budget, the 59-64% range (58.9-63.9%; top 63.928) | on the same 40-line budget: cash contributions in: 4.69% / -3.76% / 57.6-61.5% (all fail); everything in: 4.63% / -3.04%; off-chart rows out: 5.24% / -4.74% (`us_budget_tests.csv`) |
| Payment units | printed one-decimal People and Children rows | footnote 26 | the labels: these rows reproduce 6 of 10 exactly; random ±0.05 perturbations of the same rows reproduce a median of 1 | none needed |
| Decile weights | CU count x shares | balanced budget per share | dividend, labels | equal CU weights: the same to ±$0.1 |
| VAT flags | EU Directive reading, except used cars (post-calibrated 1/2; the Directive's margin scheme, Arts. 311-325, gives about 0.1); mixed lines at their 2024 Table 2500 composition; two lines calibrated | the task's starting point; Table 2500 gives the within-line split for 2024 | used cars and water, see below | grid of 1,280 Directive-consistent sets; looser grid of 983,040 (`us_flags_search.csv`) |
| Used cars | 1/2, the post's own value and not a Directive reading | dealer sales taxed in full, private sales outside VAT; CE cannot split them. The Directive's margin scheme (Arts. 311-325) taxes dealer sales on the margin only, about 0.1 of the line | Fig 4 point profile and labels: every one of the 20 best sets has 1/2; the line's dip at D7 and fall from D9 to D10 is the gap's signature | 0, 1/4, 3/4, 1 all worse. 0.1 is carried as a sensitivity: dividend $242.5, 2 of 10 labels exact, 17 of 36 bars within rounding at the mid schedule (RMSE $0.0215), and the best refit reaches only $0.0058 (knee 3.68, top 0.55) |
| Water and other public services | 0.688: water taxable; sewerage and septic cleaning taxed as in Nordic practice; municipal refuse collection outside the scope (Art. 13) | public bodies are outside the scope (Art. 13) except for the Annex I activities, and Annex I(2) covers only the supply of water. Public sewerage is outside under Art. 13 unless member-state practice differs; the Nordic countries tax it | the $249 dividend level, given the rest: the Nordic reading (1.0) gives $250.9 with Directive-consistent flags | 1.0 |
| Rent | 0.0167 (renter-paid repair services and materials, Table 2500 2024); the outputs use it | letting is exempt (Art. 135(1)(l)); the repairs part is taxable | not pinned by a printed number. The grid takes it over 0 only through the read-off point positions (±5): objective 40.7 + 22.5 (printed numbers + read-offs) against 26.5 + 42.7 at 0 | 0, the post's own "rent exempt", equally Directive-consistent and equally good: 8 of 10 labels exact against 6, label SSE 2.10 against 3.23, dividend $248.80, ghost RMSE 0.0050 against 0.0058, and the Fig 5 bars refit as well (knee 2.46, top 0.5275, RMSE $0.0027; the adopted flags give knee 2.56, top 0.53 on the same knee-step-0.01 grid). Every bar then moves by $0.002 or less (`us_flag_variants.csv`) |
| Other mixed lines | home maintenance/repairs/insurance 0.722; other lodging 0.727; vehicle rental, leases, licences 0.706; miscellaneous 0.483; housekeeping 0.951; education 0.063 (books, supplies) | Table 2500 2024 composition; insurance, credit, ground rent, licences, registration and vehicle property tax, tuition, lotteries, postage exempt or outside | not pinned (Directive reading) | trips-only lodging 0.673; tolls as public charges 0.626 (both in the grid, both worse) |
| Clear lines | taxable: food, alcohol, tobacco, energy, telephone, furnishings, apparel, new cars, fuel, repairs, transport, drugs, medical supplies, recreation, personal care, reading; exempt: mortgage interest, property taxes, vehicle finance, vehicle and health insurance, medical services, child and elderly care | Directive Arts. 132, 135, Annex III | not pinned | drugs at the OTC share (0.42), local transit exempt (0.90), non-profit clubs exempt (0.71): in the grid, worse |
| Stage-one mapping | CE major categories, with telephone in "Transportation and communication" | TB-1929's own grouping (COICOP 08), as README_usda sec. 8 maps it | Fig 5: telephone ghost 0.264 vs 0.30 read off when in housing; ghost RMSE $0.0088 to $0.0058, bar RMSE at the best knee $0.0085 to $0.0027 | personal services, health insurance, vehicle insurance, other lodging, vehicle finance to "Other"; lodging to recreation; home maintenance to furnishings; reading to "Other": none improves both fits by more than 10% (`us_mapping_tests.csv`) |
| Food split | A: food at home = the six named at-home subgroups (beta* = -0.138); food away from home = "Food other" (+0.088); alcohol and tobacco = "Beverages and tobacco" (+0.051, one eta for both) | the bulletin's "Food other" is its only restaurant subgroup | the four food ghosts: 0.440 / 0.083 / -0.029 / 0.117 against 0.44 / 0.08 / -0.03 / 0.12 read off | A2 (non-alcoholic drinks in B&T), B and B2 (CE lines mapped one by one, at-home sweets and miscellaneous foods sharing "Food other" with restaurants), F (no split): ghost RMSE 0.0077 to 0.019, bar RMSE 0.006 to 0.030 |
| Where eta is evaluated | observed decile shares of the consumption budget (stage one) and of food spending (stage two), not the bulletin's fitted shares | the post (fn. 23) | the ghosts | back-solved unrounded betas: no change at the second decimal |
| MPC mid | flat at 1.0 through decile 2.55, then linear to 0.53 at D10: 1.00, 1.00, 0.97, 0.91, 0.85, 0.78, 0.72, 0.66, 0.59, 0.53 | footnote 27 shape; knee family per the task | least squares on the 36 Fig 5 dollar bars: RMSE $0.0027 against a printing floor of $0.0029; the 68% region (rounding noise only) is the single grid point | integer knees: knee 2 top 0.5125 (RMSE $0.011), knee 3 top 0.545 ($0.010); fit surface in `us_mpc_fit_surface.csv` and `figures/us_mpc_fit.png` |
| MPC low / high | tops 0.40 / 0.65 (footnote 27); knees 1.93 / 3.29 | the same family | Fig 7's band edges, 0.474 and 0.305% of consumption (two numbers, two knees: no test) | common knee 2.55: band 0.290-0.497 (5-6% too wide) |

Two consistency checks the calibration did not use support the MPC reading. The mid schedule's impulse is
0.389% of consumption against Fig 7's central plateau of 0.390. The mid schedule is within 0.011 of the average of
the separately pinned low and high schedules at every decile. The post's mid schedule may simply be the average
of the other two.

## Gate summary (`out/gate_us.csv`)

669 gate-list rows are US. 368 are not gated: 170 are Fig 8/9 wealth-block values, 87 are axis ticks, and the
rest are inputs (rate, payment weights, pass-through range), labels, cited statistics, time references and the
text's quotes of Fig 8/9 results.

| Scope | PASS | CLOSE | MISS | Total |
|---|---|---|---|---|
| Fig 4 (labels, point positions, dividend, % of budget) | 17 | 7 | 0 | 24 |
| Fig 5 (36 bars: $, %, ghost; footer impulse) | 102 | 6 | 1 | 109 |
| Fig 6 diamonds (solid = bar, hollow = ghost) | 17 | 3 | 0 | 20 |
| Text (bridge paragraph, Fig 4-7 captions, footnote 27) | 34 | 2 | 1 | 37 |
| Headline scope: text, Fig 4, Fig 5, Fig 6 diamonds | 170 | 18 | 2 | 190 |
| Fig 6 decile segments (read off, ±0.01) | 80 | 20 | 0 | 100 |
| Fig 7 static parts (price level, impulse band, MPC wording) | 6 | 5 | 0 | 11 |
| All gated | 256 | 43 | 2 | 301 |

By role: calibration rows (used to pin a parameter) 73 PASS / 8 CLOSE / 0 MISS. Selection rows (ghosts, used to
choose the mapping and food split) 36 / 2 / 0. Checks (used for nothing) 147 / 33 / 2. The Fig 5 dollar bars count as
calibration, but two parameters were fitted to 36 numbers, so they still test the structure. The Fig 5 percent
labels are a genuine check of the category definitions and the per-share conversion: 32 of 36 PASS, and the other
four are within 2.3%.

The text items reproduce: dividend $249.38 ("about $249"); seven deciles gain; break-even between D7 (+16.94) and
D8 (-13.81); top decile -$172.05 (-3.91%); VAT-able share 58.9% to 63.9% across deciles; rent +$3.36; new cars
-$0.39 against a ghost of -$1.23; used cars +$0.38 against a ghost of -$0.05; health insurance +$1.08; vehicle
insurance +$0.53; fees and admissions -$0.20; other lodging -$0.13; renters 66% of D1 and 10% of D10; the bottom
three deciles supply 63.5% of the gross rent additions. The price level reproduces too: 7.4% to 9.3% at 80-100%
pass-through ("7-9%") and 2.47 to 3.09 points per ramp year ("2.5-3"), from an aggregate VAT-able share of 61.7%
("roughly three-fifths").

## The worst misses, and why

1. **The impulse denominators (P436, P438: MISS as labelled).** The charted bars sum to $10.950 a share-month,
   the same as the sum of the 36 printed labels. That is 0.406% of total consumption and 0.462% of the charted
   budget. The caption says "+0.4% of charted budget" and the footer "≈ +0.5% of consumption". With the charted bars
   as the numerator, each label sits on the other one's denominator. The exact flow impulse is $10.48, 0.389% of
   consumption, which is Fig 7's 0.390. It differs from the charted sum because the off-chart rows absorb $0.47 of
   withdrawals: mortgage interest -$0.38 and education -$0.19 (property taxes +$0.10).
   The caption does have a consistent reading on its own denominator: the flow impulse over the charted budget is
   0.442%, which prints as 0.4 (PASS; `gate_us.csv` columns `alt2_*`). The footer has none: "of consumption" passes
   only with the swapped denominator (bars / charted budget, 0.462). The two rows stay MISS in the counts, since the
   gate scores each number as labelled.
2. **Fig 4 labels at D8, D10, D2, D4 (CLOSE, $0.5 to $1.2).** The rebuilt nets are -13.81, -172.05, 53.43 and
   55.49 against -15, -173, 54 and 56. No Directive-consistent flag set reproduces all ten labels and the
   dividend at once: the dividend pins the level of the base and the labels its decile profile, and they pull
   apart by about $9 of VAT-able spending a share-month. A looser grid does get 9 of 10 labels with the dividend.
   But it does so by putting licences, registration and vehicle property taxes and vacation-home interest in
   the base, and by partly exempting drugs and transit. That suggests the post's own flags were coarser than the
   Directive reading on those lines; we do not adopt them because they contradict it. The effect downstream is small: the published
   labels used as the net vector move no bar by more than $0.011 (rent).
3. **Fig 6 segments at D8 and D6 (20 CLOSE, all within $0.018).** Every one of the ten categories has a rebuilt
   D8 withdrawal about $0.012 smaller than published, and a D6 addition about $0.008 smaller. Per decile, the
   segments imply MPCs near 0.98, 1.0, 0.95, 0.90, 0.88, 0.82, 0.75, 0.75-0.81, 0.60, 0.52. That is higher at D6
   and D8 than the knee line (0.78, 0.66). Part of the D8 gap is the D8 net above. The Fig 5 bars sum over deciles
   and cannot see the difference. A non-increasing per-decile fit to bars plus segments (0.99 at D1-D2,
   0.96, 0.91, 0.88, 0.82, 0.77, 0.77, 0.61, 0.53) fits the bars equally well ($0.0028) and cuts the segment RMSE
   from $0.0073 to $0.0049. It is in `us_mpc_schedules.csv` as a diagnostic. It is not adopted, because the task
   fixes the knee family.
4. **The rent ghost (CLOSE, 3.240 vs 3.26 on both Fig 5 and Fig 6).** It is 0.6% low while the rent bar is exact,
   so the MPC fit absorbs a small difference in rent's decile profile. Ghosts that both figures show are often
   read 0.01 apart (food at home 0.44 / 0.43, new cars -1.23 / -1.24, health insurance 0.48 / 0.47), which is the
   real precision of these read-offs; the rebuilt values are 0.440, -1.225 and 0.473.
5. **Fig 7 left panel (CLOSE, 8.33 and 7.41 vs 8.32 and 7.39).** The rebuilt aggregate VAT-able share is 61.71%;
   the figure implies 61.6%. That is the same ~0.2% level gap as the dividend ($249.38 rebuilt; anything from
   $248.5 to $249.5 prints as 249).
6. **The Fig 7 wording (CLOSE).** "Recipients spend ≈ all of it": the receipt-weighted MPC of D1-D7 under the mid
   schedule is 91%. "Payers cut spending by only 40-70%": the payment-weighted MPC of D8-D10 is 42% under the low
   schedule and 66% under the high one. Read as the lowest and highest payer MPC, it is 40% and 75%.
7. **The text's "+0.38%" flow impulse (CLOSE).** The static flow is 0.389%. The text quotes Fig 8's flow-only
   path at year 3 (0.376), which carries the wealth block's dynamics and is outside this rebuild.

## What remains uncertain

- **The used-car flag is pinned only by Fig 4.** One half has a story (dealer sales taxed in full, private sales
  out), but the EU margin scheme would tax dealer sales on the margin only, about 0.1. At 0.1, with everything else
  as adopted, the dividend is $242.52, D1 gains $83.28 and D10 pays $169.68, and the flow impulse is 0.377% of
  consumption. No bar changes sign. Rent moves most in dollars ($3.25 against $3.36, -3.4%); in percent the small
  bars move most (other entertainment equipment and reading about -8%, public transportation +3%). Used cars
  (+$0.378) overtakes miscellaneous for tenth place. All bars are in `us_flag_variants.csv`. If the LVT comparison
  leans on vehicle categories, carry this.
- **Rent at 0 or 0.0167.** The printed numbers prefer 0 and the read-off point positions prefer 0.0167 (see the
  judgment-call table). At 0, with its own MPC refit, every bar moves by $0.002 or less and the top ten keep their
  order, so the choice does not matter downstream.
- **Beyond used cars, the flags are weakly identified.** Water, drugs, transit, lodging and licences trade off
  against each other within ±$1 a share-month on the nets. The demand tier notices little: across the 20 best
  Directive-consistent flag sets (MPC held at the mid schedule) the rent bar stays between $3.34 and $3.38, health
  insurance between $1.07 and $1.09, and new cars at -$0.39.
- **Which grid each RMSE comes from.** Every bar RMSE above is on the calibration grid (knee step 0.05, top step
  0.0025), including the mapping tests. The rent and used-car refits use knee steps of 0.01; on that grid the adopted
  flags refit at knee 2.56, top 0.53, with the same RMSE ($0.0027).
- **The MPC shape inside the deciles.** The knee line fits every Fig 5 bar at the printing floor, but Fig 6 says
  the post's mid schedule was not exactly a knee line (D6 and D8 higher). The low and high knees are pinned by the
  two Fig 7 band edges with no degrees of freedom left, so the band is reproduced, not tested.
- **Payment-unit rounding is a property of the data, shared with the post.** The People and Children rows print to
  one decimal. Drawn uniformly within ±0.05, they move D8's net between -$20 and -$8 and D10's between -$181 and
  -$163 (5th to 95th percentile), and the dividend between $247.5 and $251.3. The rent bar moves between $3.24
  and $3.48. Statements about the world inherit that spread; statements about the post do not, since the post
  used the same printed rows.
- **Survey limits the post itself names.** These are income deciles, not consumption deciles. CE covers about
  three-fifths of national-accounts consumption, with the gap concentrated at the top. Health lines are out of
  pocket only.
- **High-RSE cells.** Twenty-seven 2024 decile cells of charted categories carry BLS's RSE ≥ 25% flag (29 with
  education's two, off-chart) and are used as printed: new cars D1-D6, used cars D1-D3, other entertainment
  D2-D8, personal services D1-D5, fuel oil D1 and D4, and medical services, medical supplies, miscellaneous and
  reading in one low decile each. The count per category
  is in `us_flags.csv` and `us_demand_shifts.csv`.
- **The Table 2500 shares are all-CU compositions applied to every decile.** For example, the homeowners-insurance
  part of the home-maintenance line is surely larger at the top. The detail table has no decile split.

## Independent verification

`checks/verify_independent_us.py` re-derives the unit from the raw files without importing `code/` (426 claims;
`out/verify_independent_us.csv`, headline sensitivity in `out/verify_independent_us_sensitivity.csv`). Every number
reproduced. Its notes were applied without changing any output the LVT and recent units read
(`us_accounting_by_decile.csv`, `us_demand_shifts.csv`, `us_impulse.csv`, `us_mpc_schedules.csv`, the figures and
every `bridge.py` function are byte-identical, and no gate status moved). Rerun afterwards, unedited, it reports 421
OK and 5 BAD. The water-line reason now cites the Directive correctly, which turned one BAD to OK. The other five are
verdicts fixed in the script, each addressed here:
- P438 "a MISS under every reading": the caption's flow / charted-budget reading (0.442%, PASS) is now in
  `gate_us.csv` and in the worst misses above; the row stays MISS as labelled.
- the budget tests' denominator: `us_budget_tests.csv` now uses the 40-line sum (top VAT-able share 63.928).
- rent 0.0167 "not pinned": rent 0 is carried as an equally good alternative with its own refit; the outputs use
  0.0167.
- two bar RMSEs for one fit: the mapping tests now use the calibration grid, so the chosen mapping's figure is $0.0027
  everywhere.
- used cars at 1/2 is not a Directive reading: it is labelled as the post's value, with 0.1 as a sensitivity. This
  one stays BAD by design.

## For the LVT step

- `bridge.build_model(2024)` builds the model.
- `bridge.per_share_monthly(m, x)` turns any annual per-CU base by decile into the model's units.
- `bridge.net_from_base(base, m["w"], tau, m["budget"])` gives the balanced-budget flat dividend net of a
  proportional tax on that base.
- `bridge.shifts_from_transfers(m, net, mpc=bridge.mpc_mid())` returns every category's $ and % shift, with the
  MPC=1 ghost alongside. Pass `shock=` instead to supply dC_d/C_d directly.
- `bridge.decompose()` and `bridge.impulse()` give the Fig 6 split and the aggregate.
- `bridge.mpc_schedules()` gives low, mid and high. The monotone per-decile diagnostic is in
  `out/us_mpc_schedules.csv` if the comparison should be checked against the schedule shape.
- The loader handles CE 2014-2021, 2024 and 2025, and the quintile table. 2022 and 2023 fill 48-49 suppressed cells
  as parent minus siblings and then stop, because new, used and other vehicles are suppressed together; the BLS
  LABSTAT `cx` data that could separate them is not vendored.

## Files

- `code/bridge.py`: the machinery (plain functions; constants hold the calibrated judgment inputs).
- `code/run_us.py`: calibration and outputs.
- `checks/gate_us.py`: the gate.
- `out/`:
  - `us_accounting_by_decile.csv`, `us_demand_shifts.csv`, `us_decomposition_top10.csv`, `us_flags.csv`,
    `us_mpc_schedules.csv`, `us_eta.csv`: the deliverables.
  - `us_budget_tests.csv`, `us_flags_search.csv`, `us_mapping_tests.csv`, `us_mpc_fit_surface.csv`,
    `us_mpc_params.csv`, `us_impulse.csv`, `us_sensitivity.csv`: the evidence for each call.
  - `us_flag_variants.csv`: every bar, percent change and ghost under the adopted flags, rent at 0 (at its own MPC
    refit) and used cars at 0.1 (at the mid schedule); the accounting side of the same variants is in
    `us_sensitivity.csv`.
  - `gate_us.csv`: the gate (`alt_*` and `alt2_*` hold alternative readings of a published number; they never change
    a status).
- `figures/fig5_rebuilt.png`: the rebuilt Fig 5 with the published labels and ghosts marked, and the gaps.
- `figures/us_mpc_fit.png`: the fit surface and the schedules.
