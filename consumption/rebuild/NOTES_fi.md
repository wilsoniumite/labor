# Finland rebuild: the VAT bridge's consumption machinery on HBS 2022 quintiles

Figures 1-3 of the 2026-06-14 post run the 15-point VAT surcharge and its flat per-adult dividend through Statistics
Finland's Household Budget Survey 2022, by household income quintile. The post's code was never committed anywhere we
can reach. This folder rebuilds the machinery from the post's text and its published numbers
(`data/tidy/post_published_numbers.csv`), extending `code/bridge.py` (the US rebuild) rather than forking it. The
Finnish model dicts plug into the same generic tier-2 functions (`net_from_base`, `shifts_from_transfers`,
`decompose`, `impulse`), so an LVT-funded dividend can run through exactly what this gate checks.

Result in one paragraph. Fig 1 reproduces exactly: all 19 gated numbers PASS. That covers the EUR 193.01 dividend,
all five net labels (76.75, 37.27, 4.23, -14.18, -88.06 against 77, 37, 4, -14, -88), all five percent-of-budget
labels, the five point positions (within EUR 2.3) and the break-even line (1,286.7 against 1,287). Fig 2's 37 bars
come back with RMSE EUR 0.0058 (20 within the EUR 0.005 printing rounding, the rest within 0.013) and its ghosts with
RMSE 0.0052 against the +/-0.01 read-offs. The Fig 3 top ten is the published set, in the published order, and its
50 quintile segments come back with RMSE 0.0074. The MPC schedule was not fitted to any Finnish number: it is the US
decile schedule averaged to quintiles. Of the 228 Finnish numbers the static machinery should reproduce, 160 PASS,
57 are CLOSE and 11 MISS. The post's stated composition route (tulonjako 12ew, decile pairs averaged) reproduces it.
The internally consistent route (the HBS's own 14qa table) does not: no flag set gets a single Fig 1 label.
Reproducing the post meant reproducing three conventions that are not coherent (below). The coherent machinery
gives a rent bar of EUR 4.21 instead of 4.92, with the same 2.8% change.

## Run

```
venv/bin/python -I consumption/rebuild/code/run_fi.py      # about 12 s; writes out/fi_*.csv, figures/fig2_rebuilt.png
venv/bin/python -I consumption/rebuild/checks/gate_fi.py   # writes out/gate_fi.csv, prints the summary
```

`run_fi.py` re-derives every calibrated or selected value and asserts that the constants in `bridge.py` are what
the searches find: the flag grid's best combination, and the units, budget, base, mapping and MPC choices. The US
results are untouched. After the bridge.py edits, `run_us.py` and `gate_us.py` were rerun, and all 16 US outputs
(both PNGs included) and both logs are byte-identical to the pre-edit run.

## The method as rebuilt

Everything is in euros per payment share per month: one share per adult, 0.3 per child. Group q is an HBS income
quintile, each holding 20% of households.

- **Data.** Every category comes from the per-consumption-unit table (ktutk 14pg, OECD-modified units, the table
  footnote 22 cites). The per-household table enters only through r_q = per-household total / per-CU total for
  the quintile (1.167, 1.351, 1.413, 1.464, 1.473; 1.404 in total). That is the ratio footnote 30 uses to bridge
  wealth to consumption units.
- **Payment units.** tulonjako 12ew 2022 gives households and persons by person income decile and life-cycle stage.
  - Adults: everyone in one-person, childless-couple and 'other' households, plus 2 per couple with children and 1
    per single parent.
  - Children: the rest.
  - Decile pairs are averaged: the mean of D1's and D2's per-household values gives q1, and so on (footnote 30's
    "pair-averaged").
  - Shares per household s_q: 1.251, 1.595, 1.709, 1.819, 1.903.
  - The population figure comes from the table's own total column: 1.617 shares per household.
- **Per share.** C_gq = cu_gq x r_q / (12 s_q). The budget is B_q = per-household total / (12 s_q): EUR 1,309,
  1,581, 1,878, 2,113 and 2,826. B_q is all consumption, including imputed rent, interest on housing loans,
  education and consumption abroad. Those lines are in the budget but off the chart.
- **Weights.** w_q is proportional to s_q / r_q, i.e. payment shares per consumption unit: the quintiles are
  treated as holding equal numbers of consumption units. This gives w = 0.179, 0.197, 0.202, 0.207, 0.215, against
  0.151, 0.193, 0.206, 0.220, 0.230 for the equal-household design. Two consequences follow:
  - theta_qg = w_q C_gq / sum is the per-CU market share cu_gq / sum_q cu_gq;
  - the dividend is tau x sum_q w_q x_q.
- **Accounting.** x_q = sum over VAT lines of flag x spending (tax-inclusive). The dividend is 0.15 x
  sum_q w_q x_q, and net_q = dividend - 0.15 x_q.
- **Elasticities.** eta_gq = 1 + beta_k / w_dq.
  - w_dq is the budget share of category g's COICOP division; "parent-group fidelity" in the Fig 2 caption means
    the division.
  - beta_k is the TB-1929 Table 3 beta of the division's group (README_usda sec. 8).
  - The food system is divisions 01 + 02 + 11 (restaurants and accommodation). Its eta_F comes from their joint
    budget share, and it is split by the stage-two betas (TB-1929 eq. 11).
  - In the split, 01.1 gets the six named at-home subgroups (beta* -0.138), 01.2 + 02.1 + 02.3 get 'Beverages
    and tobacco' (+0.051), and 11.1 + 11.2 get 'Food other' (+0.088). Each beta* is spread by spending.
  - Consumption abroad gets eta = 1.
- **Demand.** shock_q = mpc_q net_q / B_q, dPct_g = sum_q theta_qg eta_gq shock_q, and dEUR_g = dPct_g x Cbar_g.
  The quintile segments are theta_qg eta_gq shock_q Cbar_g.
- **Euro conversion.** Cbar_g comes from the per-CU total column converted on its own:
  cu_total_g x 1.404 / (12 x 1.617).
  - This is 4.1% above the weighted mean sum_q w_q C_gq that the dividend uses.
  - It is also the "budgets averaging EUR 2,051" (rebuilt 2,051.8; the weighted mean is 1,970.6).
- **MPC.** The US low, mid and high decile schedules (bridge.US_MPC_KNEE/TOP) are averaged in decile pairs:
  - mid 1.000, 0.940, 0.814, 0.688, 0.562;
  - low 0.997, 0.883, 0.735, 0.586, 0.437;
  - high 1.000, 0.982, 0.885, 0.780, 0.676.
- **Charted categories.** The 37 bars are COICOP 2018 groups. Ten more budget lines are off the chart:
  - imputed rentals, and interest on housing loans (the post's 'owner-occupied housing');
  - education (0.30% of the budget);
  - consumption abroad;
  - six groups too small to draw (06.3, 06.4, 07.4, 08.2, 09.5, 13.3).

## Every judgment call, its reason, and what pinned it

| Call | Choice | Reason | Pinned by | Alternatives tested (`fi_units_tests.csv` etc.) |
|---|---|---|---|---|
| Composition route | 12ew, decile pairs averaged | footnote 22 names 12ew; footnote 30 calls the same pairing "pair-averaged" | Fig 1: objective 11.2 with 5/5 net and 5/5 percent labels. Also the EUR 2,051, through the 12ew total column | pairs pooled: 14.4, 5/5 and 4/5. 'Other households' as two adults: 63.5, 3/5. **14qa: 862, 0/5 and 0/5, best dividend 191.2, average budget 1,946, Fig 2 euro/percent ratios 6/27 inside rounding (chi2 1,419 against 28)** |
| Per-CU to per-share conversion | r_q / s_q, r_q the HBS's own per-household / per-CU ratio | footnote 30 bridges with exactly this ratio | Fig 1 budgets (the percent labels) and the ghosts | CU from 14qa means: 72.5, 2/5. CU implied by the 12ew adults and children: 49.2, 3/5 |
| Population weights | proportional to s_q / r_q (equal consumption units per quintile) | the only weighting that makes the dividend and the nets agree. It is also what makes theta the per-CU market share, which Fig 3 and the ghosts require | Fig 1: objective 11.2 against 1,178 for equal-household weights, whose best dividend is 196.2 with 0/5 labels | equal households (the HBS's actual design) |
| Euro conversion | total column x 1.404 / (12 x 1.617) | the published EUR/percent label pairs | 27 categories with both labels identified: chi2 27.9, 25/27 inside rounding; also the EUR 2,051 | the weighted mean sum_q w_q C_gq: chi2 886, 10/27, average budget 1,971 |
| Budget rows | all consumption | the post: off-chart lines are "in the budget totals" | Fig 1 percent labels 5/5, Q1 VAT-able 59.2%, EUR 2,051, ghosts | minus abroad: 4/5. Minus imputed rent and interest: 0/5, average 1,724. Minus education: 5/5, but ghosts 0.006 against 0.005 and average 2,046 |
| Tax-inclusive or tax-exclusive base | tax-inclusive: tax = 0.15 x VAT-able spending | Fig 1's line has slope -0.15; the text has each adult pay tau x C_i | the dividend. Read as 15 points on the net-of-VAT price, the best of all 18,432 flag sets gives EUR 170.8 (`fi_base_tests.csv`) | tax-exclusive |
| VAT flags, big mixed lines | in: housing-company maintenance charges, used cars, licences and vehicle charges; out: package holidays, consumption abroad | the post flags whole COICOP groups, not Finnish law line by line | Fig 1 grid: each value holds in all 20 best combinations (`fi_flags_search.csv`) | Finnish law line by line (charges, licences out; used cars 1/2): dividend 172.4, 2/5 labels |
| VAT flags, weaker lines | games of chance and international flights in (19/20 and 17/20 of the best); other services n.e.c. in (14/20); domestic services in (16/20) | as above | Fig 1 grid | 0 or 1/2 |
| VAT flags, lines Fig 1 cannot see | the law reading: sea transport out, letter post out, church fees out, social services out | no published number separates them (10/10, 12/8, 11/9, 10/10 across the 20 best) | not pinned | 1 |
| Clear lines | exempt: rents, imputed rent, interest, health care (06.2-06.4), education, insurance, financial services; taxable: everything else at 24/14/10% | 2022 law; the post's own list (rents, health care, education, insurance and financial services) | not pinned | - |
| Elasticity parent | the COICOP division | Fig 2 caption ("subcategories inherit their group's quintile-specific eta") | ghost RMSE 0.0052 against 0.0236 when divisions are pooled into TB-1929 groups (07+08, 12+13). Personal care needs eta 1.93 in Q1, which only division 13's own share (3.2%) gives | TB-1929 groups |
| Food system | F3: divisions 01, 02, 11; 01.2 in 'Beverages and tobacco' | 11.2's ghost (-0.02) needs a food-like eta (F3 gives 0.88 in Q1 falling to 0.53 in Q5; division 11 with the food beta would give a negative eta); README_usda leaves 01.2 open | ghosts: F3 0.0052; F2 (01.2 at home) 0.0072; F4 (01.2 'Food other') 0.0101; F1 (11.2 outside food) 0.0115 with bars 0.041; F0 (no split) 0.0278 | as listed |
| Where eta is evaluated | the model's own (per-CU) budget shares | the figures' basis | ghosts 0.0052 against 0.0101 at per-household shares | per-household shares reproduce the text's food eta (0.435 and 0.302 print as 0.44 and 0.30; per-CU gives 0.425 and 0.299) |
| MPC schedule | the US decile schedules averaged in decile pairs | Fig 2's title: "literature MPC schedule (quintile-aggregated)"; one schedule for both countries | **not pinned by Finland**: US Fig 5 and Fig 7. Out of sample here: bars RMSE 0.0058 against 0.0047 for a free 5-parameter fit. The decile knee family fitted to the Finnish bars lands at knee 2.4, top 0.5325 (US: 2.55, 0.53). The Fig 3 segments imply 1.00, 0.93, 0.83, 0.75, 0.56 | quintile knee fit (0.0049); US monotone diagnostic pair means (0.0139, because its D1-D2 at 0.992 shrinks every bottom-heavy bar) |

## Gate summary (`out/gate_fi.csv`)

365 gate-list rows are Finnish; 137 are not gated. That leaves out 61 Fig 10 wealth-block rows (54 figure, 7 text),
52 axis ticks, and the rest: inputs (rate, payment weights, MPC=1), data vintages, labels, and one structural
description.

| Scope | PASS | CLOSE | MISS | Total |
|---|---|---|---|---|
| Fig 1 (dividend, nets, percent labels, positions, break-even, quintile sizes) | 19 | 0 | 0 | 19 |
| Fig 2 EUR bars | 20 | 17 | 0 | 37 |
| Fig 2 percent labels | 8 | 23 | 6 | 37 |
| Fig 2 ghosts | 35 | 2 | 0 | 37 |
| Fig 3 net labels and diamonds | 15 | 3 | 2 | 20 |
| Text (bridge paragraphs, Fig 1-3 captions, footnote 30's EUR 391k) | 22 | 3 | 3 | 28 |
| Headline scope: text, Fig 1, Fig 2, Fig 3 labels | 119 | 48 | 11 | 178 |
| Fig 3 quintile segments (read off, +/-0.01) | 41 | 9 | 0 | 50 |
| All gated | 160 | 57 | 11 | 228 |

By role:
- **Calibration** rows (Fig 1 and the text's accounting numbers): 24 PASS, 0 CLOSE, 0 MISS.
- **Selection** rows: 55 / 19 / 0. These are the Fig 2 ghosts, which chose the parent group and food system, and
  the Fig 2 EUR labels, whose ratio to the percent labels chose the euro conversion.
- **Checks**, used for nothing: 81 / 38 / 11.

The demand tier has no fitted parameter, so every Fig 2 bar and Fig 3 segment tests the structure. That differs from
the US, where the knee and top were fitted to the bars. One caveat: the structure itself was found by exploring
the ghosts, the EUR/percent ratios and the Fig 3 Q1 segments.

The text items reproduce:
- the dividend (EUR 193.01);
- Q1 +EUR 76.75 (+5.86%) and Q5 -EUR 88.06 (-3.12%);
- the middle quintile EUR 4.23 from break-even ("within EUR 5");
- the VAT-able share of 59.2% in Q1 and 65.4-67.0% in Q2-Q5 ("roughly two-thirds");
- two paying and three gaining quintiles;
- the ten largest movers;
- rent +EUR 4.93 ("+4.92", "about EUR 5");
- vehicle purchases -EUR 0.52 ("-0.5");
- education's 0.30% budget share;
- a receipt-weighted gainer MPC of 97% ("roughly all");
- EUR 391.2k per consumption unit for Q5 net worth. This is footnote 30's bridge, (D9 + D10)/2 / r_q5, which uses
  the same r_q as the conversion above.

Fourteen categories flip sign between the ghost and the MPC-adjusted bar, vehicle operation among them, as the text
says.

## The worst misses, and why

1. **The impulse (P113, MISS as labelled; PASS on the alternative reading).** The charted bars sum to EUR 10.46 a
   share-month (the 37 printed labels sum to 10.40). That is 0.63% of the charted budget and 0.51% of total
   consumption. The flow impulse sum_q w_q mpc_q net_q is EUR 8.64, 0.438% of consumption, which prints as
   "+0.4%". The US caption carried the same denominator slip (`NOTES_us.md`, miss 1). Here the label fits the flow
   impulse, the concept behind the US Fig 7 plateau.
2. **"A transfer worth three to eight percent of budgets" (P118, MISS; P117 PASS).** No rebuilt quantity spans
   3-8%:
   - net transfer / budget runs from 0.2% to 5.9% (3.1% at the top, 5.9% at the bottom);
   - dividend / budget runs from 6.8% to 14.7%;
   - extra VAT / budget runs from 8.9% to 10.05%.
   The gate reads the range as the two tails of Fig 1. "Three" passes and "eight" misses.
3. **"Once the top's withdrawal halves" (P114, MISS by 0.012 beyond +/-0.05).** The Q5 MPC is 0.5615. The 50 Fig 3
   segments imply 0.561 on their own, so this is wording, not a modelling gap.
4. **Six Fig 2 percent labels of small categories (MISS).**
   - 13.2 other personal effects: 1.13 against 1.26.
   - 05.2 household textiles: 0.43 against 0.51.
   - 05.4 glassware: 0.24 against 0.20.
   - 05.3 appliances: 0.15 against 0.18.
   - 05.1 furniture: 0.024 against 0.03.
   - 04.3 dwelling repair: +0.002 against -0.01 (a sign flip of a near-zero shift).

   Their euro bars are all within EUR 0.013, and within one division they share eta, so the gap is in their
   quintile profiles. The obvious data routes were tried during the rebuild: the published one-decimal shares,
   the per-household table, and sums of suppressed subclasses. None explains them (those exploratory runs are not
   kept as outputs). The other 23 CLOSE percent labels miss by 0.005-0.03 pp, and the percent-label RMSE is about
   0.031 pp under every composition (pairs averaged or pooled) and net vector (rebuilt or printed) tried.
5. **Two Fig 3 net labels (MISS).** Clothing "+0.3" against 0.353, and ICT services "+0.5" against 0.552. The post's
   own Fig 2 labels for these are 0.35 and 0.54. A value just below 0.35 prints as "0.3", so these are
   rounding-boundary crossings inherited from Fig 2 gaps of 0.003 and 0.012.
6. **The text's food elasticity (P109, CLOSE; PASS on the alternative).** On the figures' per-CU basis the
   food-at-home eta is 0.425 in Q1 and 0.299 in Q5. At per-household budget shares it is 0.435 and 0.302, which
   print as the text's "0.44" and "0.30". The text's numbers come from the other basis, a small inconsistency
   inside the post.
7. **"Budgets averaging EUR 2,051" (P116, CLOSE).** The total-column conversion gives EUR 2,051.8, which prints as
   2,052. The weighted mean of the quintile budgets is 1,970.6.
8. **The rent bar (P121, P119, CLOSE).** It comes out at EUR 4.928 against 4.92, with 2.810% against 2.80%. The
   bars as a whole sit EUR 0.0016 above the labels on average (they sum to 10.46 against 10.40), so the rebuilt
   impulse runs about 0.6% high.

## Three conventions in the post that are not coherent

Reproducing the published numbers required each of these. Each was identified by numbers no other choice
reproduces (see the table), and each is a judgment about the post, not about Finland.

1. **Equal consumption units per quintile.** The HBS quintiles hold equal numbers of households, and Q1 households
   carry fewer consumption units (1.18 against 1.50 in Q5). Weighting by payment shares per CU gives Q1 18% of the
   population instead of 15%. This weighting is what makes the dividend EUR 193 and the per-CU market shares; with
   the same data and units, equal-household weights balance at EUR 196.7. The nets would then be +80.4, +40.9,
   +7.9, -10.5 and -84.4 (`fi_accounting_by_quintile.csv`).
2. **The euro conversion from the total column.** The conversion is 4.1% above the weighted mean the dividend uses,
   because the 12ew population figure (1.617 shares per household) is not the mean of its decile pairs (1.656).
   Every Fig 2 euro label and the EUR 2,051 carry it; the percent labels do not.
3. **Division-level parents.** Splitting a TB-1929 group's beta over two divisions counts it twice (transport and
   communication, other). That leaves sum beta = +0.052 instead of 0, so Engel adding-up fails and the bars over all
   47 categories sum to 1.052 times the flow impulse. Pooling the divisions into TB-1929 groups restores adding-up
   (ratio 1.000; `fi_convention_compare.csv`) but fits the ghosts far worse (0.0236 against 0.0052).

The post's VAT flags also follow COICOP groups rather than Finnish law on several big lines. Housing-company
maintenance charges are not a VAT-able supply. Used cars are taxed on the dealer margin only, and private sales not
at all. Licences and vehicle charges are public fees. International flights are zero-rated, and gambling is exempt.
Line by line under the law, the same machinery funds EUR 172.4, not 193.

## What the coherent machinery says (`fi_convention_compare.csv`)

`build_fi_model(convention="coherent")` uses the per-household table, equal-household weights, and theta, Cbar and
eta all from the same data. It keeps the same flags, elasticity structure and MPC schedule.

| Variant | Dividend | Net Q1 / Q5 | Rent bar | Food | Vehicles | Charted impulse | Flow, % of consumption |
|---|---|---|---|---|---|---|---|
| Post conventions (reproduces the figures) | 193.0 | +76.8 / -88.1 | 4.93 | 0.92 | -0.52 | 0.63% | 0.438% |
| Coherent, 12ew composition | 198.8 | +80.3 / -83.9 | 4.21 | 0.93 | -0.43 | 0.60% | 0.422% |
| Coherent, 14qa composition | 193.7 | +80.3 / -84.8 | 4.21 | 0.92 | -0.43 | 0.61% | 0.430% |
| Coherent, 12ew, TB-1929 group parents | 198.8 | +80.3 / -83.9 | 4.21 | 0.93 | -0.44 | 0.57% | 0.422% |

The shape survives. Rent is still by far the largest mover, at +2.83% against the post's 2.81%. Its euro size falls
15%, because the post's per-CU euro conversion puts mean rent at EUR 175.3 per share-month; the per-household data
put it at 148.7. Nine of the post's ten largest movers stay in the top ten; electricity enters the coherent top ten
at the edge. The flow impulse moves from 0.44% to 0.42-0.43% of consumption.

## What remains uncertain

- **Pair means or pooled pairs.** Fig 1 prefers pair means (5/5 percent labels against 4/5; objective 11.2 against
  14.4), and footnote 30's wording agrees. The demand tier cannot tell them apart (ghosts 0.0052 against 0.0054).
- **Weak and unidentified flags.** Sea transport, letter post, church fees and social services are invisible to
  Fig 1. International flights, games of chance and other services n.e.c. are only moderately pinned. They move the
  dividend by at most about EUR 0.5 and the bars by at most a few cents.
- **12ew is not the HBS grouping.** Its deciles are person deciles on another income concept and sample, with
  unequal household counts (D1 401,798 households, D10 254,633). Pairing them does not give HBS quintiles
  (README_fin.md). The post does it anyway, and the rebuild follows it because the published numbers need it. The
  consistent alternative (14qa) splits adults from children at age 14, not 18: shares per household are 1.31-1.93
  against 1.25-1.90 under 12ew.
- **The MPC schedule inside the quintiles.** The pair means of the US knee schedule fit the bars within 0.0011
  RMSE of a free fit. The Fig 3 segments suggest Q3 and Q4 slightly higher (0.83 and 0.75 against 0.81 and 0.69),
  as the US Fig 6 segments did for D6 and D8 (`NOTES_us.md`, uncertain items). Not adopted: no Finnish number
  pins the schedule, and the post says it is the literature schedule.
- **Small categories.** The six percent-label misses above remain unexplained.
- **Survey limits the post names.** Quintile means compress the tails. Nothing is transacted for imputed and
  owner-occupied housing, so it stays off the chart. Education's beta/w is degenerate.

## For the LVT step

- `m = bridge.build_fi_model()` rebuilds the post's machinery (post conventions, 12ew, F3).
  `bridge.build_fi_model(convention="coherent", composition="14qa")` gives the internally consistent one. For an
  apples-to-apples VAT-against-LVT comparison, run both instruments through the same dict. The VAT bridge under
  each convention is `bridge.fi_vat_accounting(m)` (flags `bridge.fi_vat_flags()`).
- A per-household annual base by quintile becomes per share per month with `bridge.per_share_monthly(m, x)`. Use it
  for land values or land rents, e.g. wealth-survey deciles averaged in pairs as footnote 30 does. This holds under
  both conventions. An HBS per-CU amount must first be multiplied by `m["units"]["hh_per_cu_ratio"]`.
- `bridge.net_from_base(base, m["w"], tau, m["budget"])` gives the balanced-budget dividend and nets, balanced under
  the dict's own weights.
- `bridge.shifts_from_transfers(m, net)` uses the Finnish mid schedule by default (`m["mpc_default"]`).
  `bridge.fi_mpc_schedules()` gives low, mid and high. `bridge.decompose()` gives the quintile split and
  `bridge.impulse()` the aggregate.
- To compare with the published figures, `bridge.fi_post_eur(m, x)` puts euro amounts on the post's conversion. It
  is the identity under the coherent convention. Percent changes need no rescaling.
- Use the flow impulse (`impulse()["flow_pct_consumption"]`), not the sum of bars, for aggregates. With division
  parents the bars over-allocate by 5.2%; `eta_parent="usda"` restores adding-up.

## Files

- `code/bridge.py`, FINLAND section: `build_fi_model`, `fi_composition`, `fi_eta_table`, `fi_vat_flags`,
  `fi_vat_base`, `fi_vat_accounting`, `fi_mpc_schedules`, `fi_post_eur`, the category list and the VAT lines with
  their law readings and reasons. The US part is unchanged, apart from a default-MPC hook (`mpc_default`, absent
  from US dicts) and `per_share_monthly` indexing by the model's groups (identical for the US).
- `code/run_fi.py`: calibration and outputs.
- `checks/gate_fi.py`: the gate.
- `out/`:
  - `fi_accounting_by_quintile.csv`, `fi_demand_shifts.csv`, `fi_decomposition_top10.csv`, `fi_flags.csv`,
    `fi_mpc_schedules.csv`, `fi_eta.csv`: the deliverables.
  - `fi_units_tests.csv`, `fi_budget_tests.csv`, `fi_base_tests.csv`, `fi_flags_search.csv`,
    `fi_mapping_tests.csv`, `fi_mpc_tests.csv`, `fi_mpc_fit_surface.csv`, `fi_impulse.csv`,
    `fi_convention_compare.csv`: the evidence for each call.
  - `gate_fi.csv`: the gate.
- `figures/fig2_rebuilt.png`: the rebuilt Fig 2 with the published labels and ghosts marked, and the gaps.
