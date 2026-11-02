# Fingerprint test: is US spending being held up by higher incomes, and can the national accounts see it?

Question 2, income-group angle (Stella's 2026-06-14 post; the sector angle is `NOTES_sectors.md`). Built 2026-11-02 by
`code/fingerprint.py`; checks in `checks/check_fingerprint.py`. Data: NIPA vintage of 2026-10-29 (monthly to 2026-09,
annual to 2025), BLS distributional PCE (March 2025), CE Table 1110 2014-2025, all vendored in `consumption/data/`.

## Answer in plain words

**The mix of national-accounts spending does not show the fingerprint of a K, but the test is too weak to rule one
out at the size Zandi describes.**

- With the official 16-line distribution (BLS distributional PCE), the categories the top 20% buy did not outgrow the
  rest from 2023-09 to 2026-09: the implied top20 - bottom80 gap is -3.6 points in real terms (-1.0 nominal) against
  Zandi's +12.5 over three years. The 95% interval runs from -28 to +28 points, so Zandi's split and no split at all
  both fit.
- With the finer, income-ranked CE mapping (133 PCE lines), the gap leans the other way: +20.0 points real (+13.5
  nominal), placebo p = 0.10. But in the calm 2014-2019 years, when CE's own income-ranked spending totals show no
  K at all, the same estimator read +21 points on average over three-year windows (every window positive, +9 to +38
  points): the luxury-skewed lines the top buys normally outgrow necessities in real terms. The 2023-2026 reading
  sits at that norm (excess -1 point), not 12.5 points above it.
- The estimator's noise is as large as the signal. Where group totals are known, its error over three-year windows
  has a standard deviation of 11 points (A, real) to 45 points (B against CE). It produced false alarms of +19 to +45
  points in 2016-2019 and 2021-2023 (placebo p 0.01-0.04) while CE's own group spending grew alike. Its power
  against Zandi's split is 5-21% as a stand-alone test.
- Only against a calm-period norm, and only if 2023-2026 behaved like 2010/2014-2019 across categories, does the
  test have real power (smallest three-year gap detectable with 80% power: 15-18 points in real terms, 23-24
  nominal, against Zandi's 12.5). On that footing, for the three-year window, Zandi's split sits about 2 standard
  deviations (B) to 4 (A) above what the categories show. The two- and four-year windows are less clear-cut for B:
  its real-terms reading exceeds the calm norm by +6.6 points over 2023-2025 (Zandi's split then sits only 0.2 sd
  above it) and by +5 to +12 points over 2022-09 to 2026-09, though those norms rest on 4 and 24 overlapping calm
  windows. The care boom (Medicare- and Medicaid-financed, bottom-weighted in the official distribution) and the
  post-pandemic rebound of the services the top buys are exactly the kind of shocks that break the calm-period
  assumption, so treat all of this as suggestive, not decisive.
- The more direct evidence points the same way: CE's income-ranked group spending rose 8.7% for the top 20% and 8.7%
  for the bottom 80% from 2023 to 2025 (nominal), and the top quintile's share of spending was 38.86% in 2023 and
  38.88% in 2025, where Zandi's split would have added about 1.9 points. The CE under-covers the very top, so a K
  confined to the top few percent could hide from it; it would also hide from this test.

## 1. The question and the claim

Is US spending being held up by higher incomes, and can that be seen in spending patterns? Mark Zandi (Moody's;
EconoFact Chats, 24 July 2026, `data/raw/other/econofact_zandi_2026-07-24.pdf`): "over the past say three years,
overall real consumer spending growth has been 2%. Folks that are in the top 20% of the income distribution, the
growth in their spending has been, on a real basis, after inflation, close to 4%. And the folks in the rest of the
distribution, the bottom 80%, their spending growth has been close to zero." Spending growth is "dependent on a small
group, who in turn is dependent on a run-up in equity prices".

Scale. Over three years Zandi's split is a cumulative gap of 1.04^3 - 1 = 12.5 points (8.2 over two, 17.0 over four).
With the official distributions (CE top quintile 38.5-38.9% of spending in 2019-2025, income-ranked; dPCE top two
deciles 39.5% in 2023, spending-ranked) a 4-point-a-year gap lifts the top 20%'s share of spending by about 1.9 points
in two years and 2.8 in three. With those shares his 4% and 0% would average about 1.6%, not 2%; the test keeps his
gap and lets the level match the actual aggregate. (Moody's own estimates, top 10% near half of spending, are not
what the official distributions show.)

Context from the watch site: care took 107% of net job growth from August 2024 to August 2026, and real spending rose
1.8% in the six months to September 2026 against 0.1% (BEA: 0.05%) for real personal income excluding transfers.

## 2. Method

**Model.** Let theta_qg be income group q's market share of category g (its share of all spending on g), x_q the
growth of group q's total spending and eta_gq an Engel elasticity. If each group's spending on g grows by eta_gq x_q,

    g_g = sum_q theta_qg * eta_gq * x_q + e_g,

where e_g collects relative prices and substitution, supply shocks, quality adjustment and taste shifts common to all
groups. The x_q are identified from the cross-section because categories differ in who buys them.

**Main specification** (eta = 1, Zandi's split): g_g = x_b80 + theta_top20,g (x_top20 - x_b80) + e_g, by weighted
least squares with base-period nominal spending as weights; the slope is the top20 - bottom80 gap. With these weights
the fitted values average exactly to the covered categories' aggregate growth.

**Why the inverse model, not a fixed-share basket.** A K can work within categories (the top buying more of
everything). A fixed-market-share basket attributes each category's growth to whoever already buys it, so it reads a K
as a small tilt. With the same weights the two are the same statistic in different units:

    basket gap = kappa x slope,   kappa = Var_w(theta_top20) / (theta_bar (1 - theta_bar)),

and kappa is 0.056 for the 16 lines (2023) and 0.031 for the 133 CE-mapped lines (2024): a basket index shrinks a K by
a factor of 18 to 32. The inverse model puts it back into group-growth units; the t-statistic is unchanged. So power
is the same question either way: how wide is the spread of theta across categories against the category noise e_g?
At the 16-line level a Zandi-size three-year K moves category growth by 1.4 points per standard deviation of theta
(0.116); categories scatter by 4.3 points real (5.8 nominal) around their mean over the same three years. At the
133-line level the numbers are 1.1 points against 8.5.

**Specs.** Two groups (main); four groups (bottom 50 / 50-80 / 80-90 / top 10) and five (quintiles) by unconstrained
WLS for reference and by ridge toward equal growth (penalty lambda sum_k pi_k (x_k - xbar)^2, pi = groups' spending
shares; lambda by exact leave-one-category-out CV, re-chosen inside every bootstrap and permutation replicate).
Robustness drops: health care, imputed items, energy, motor vehicles, and all four. Nominal and real for everything.

**Inference.** Two-group 95% interval by permutation test inversion (H0 gap = c tested by permuting theta in
g - c theta, 1,000 permutations; exact because the slope is linear in c). The placebo p-value is that test at c = 0
(theta permuted across categories), p_zandi at Zandi's gap. Classical WLS and HC3 standard errors are also in the
file (HC3 typically 1.5-2 times the classical). Multi-group intervals: pairs bootstrap (500), placebo 500.

**Zandi and flat.** Zandi's predicted pattern is the actual aggregate plus (theta - theta_bar) x his cumulative gap;
the flat split predicts the aggregate for every category. Fit is the weighted RMSE and R^2 against flat. His numbers
are real; the same gap is used for nominal growth (ISPCEPX 2019-2024 inflation: top quintile 19.9%, others 19.1-19.5%,
about 0.1 point a year).

**Two benchmarks** attached to the read (`fingerprint_read.csv`): (1) the estimator's error where group totals are
known, annual windows of the same length (A against dPCE group totals 2000-2023; B against CE Table 1110 group
totals 2014-2025), as a band gap +- 1.96 sd; (2) the calm-period norm: mean and spread of the estimate in windows of
the same length that start after the 2008-09 recession (A from 2010, B from 2014) and end by 2019-12, and the excess
of the 2023-2026 estimate over that norm. Zandi's split predicts an excess equal to his gap.

## 3. The two theta sources

**(A) BLS distributional PCE, Table 1** (`bls_dpce_long.csv`, March 2025 results, NIPA vintage of 2024-09). Decile
shares of each of the 22 NIPA Table 2.3.5 lines, 2000-2023; the 16 leaf lines are the categories. Deciles are of
equivalized total spending, not income. The dPCE imputes third-party health care to its recipients, so health care
is A's most bottom-weighted line (top-20 share 0.26) and motor vehicles its most top-weighted (0.67). Line 22 (NPISHs)
carries the total-PCE shares by construction and has no leverage on the slope. Growth from Tables 2.3.5/2.3.6
(annual) and 2.8.5/2.8.6 (monthly): lines 1-22 carry the same series codes in both and equal the 2.4.5U values cell
for cell (checked). Real growth from chained dollars where both endpoints are published (2007 on), else the 2.4.3U
quantity index of the same series (identical ratios, checked).

**(B) CE Table 1110** (deciles of income before taxes, 2014-2025) mapped to 2.4.5U lines. Chain: line item -> UCCs from
BLS's integrated hierarchical-grouping file for the year (`raw/bls_ce/stubs/stubs.zip`, CE-HG-Integ-YYYY.txt) -> PCE
series from BLS's `ce_pce_map` -> 2.4.5U line through the BEA mnemonics. Rules (`out/fingerprint_mapping_B.csv` has
every year x item x UCC x target with its rule and reason):

1. **Items.** Table 1110 leaf expenditure items, with three fixes: 2023-2025 show only `Gasoline` under `Gasoline and
   other fuels`, so the parent is used; 2024-2025 dropped `Other vehicles`, so a residual item (vehicle purchases
   minus new minus used, by decile) is mapped through the stub's other-vehicles UCCs; and the addendum `Estimated
   monthly rental value of owned home` (x12; non-owners count as zero) stands for owners' imputed rent, as in BLS's
   own map (UCC 910050 -> DOWNRC). 73 items match the stub by label path, 2 by group code (gasoline, other vehicles).
2. **UCC -> PCE line.** BLS's map where it has the UCC. The published tables take food and alcohol away from home,
   some audio-video goods and newspapers from the Diary while BLS's map sources the same spending from Interview UCCs;
   those Diary UCCs, and UCCs newer than the map, go to the target BLS uses for the analogous UCC (78-UCC supplement in
   `fingerprint.py`, each with a reason). Left out as not PCE: property taxes, mortgage interest, vehicle registration
   and licence fees, Medicare/Medicaid/Tricare/CHIP premiums (social-insurance contributions), cash contributions,
   pension and Social Security deductions, education savings and prepaid tuition, owner- and renter-paid dwelling
   maintenance (inputs to housing services; BLS's map leaves them out too). One small in-scope UCC has no target and
   is dropped (002120 other non-health insurance, about $45 a year per CU).
3. **Allocation.** Each item's decile distribution holds for all its UCCs. A PCE line fed by several items takes the
   mix of their distributions weighted by CE spending on the UCCs that feed it: all-CU UCC means from BLS Table 2500
   (`raw/bls_ce/tables/detail/cu-all-detail-YYYY.xlsx`, rows aligned to the stub with difflib) times a split share. A
   UCC BLS sends to several PCE series is divided in proportion to those lines' PCE values (BLS publishes no split
   proportions). Table 2500 withholds some UCC means in 2022-2023 (RSE >= 25%; 126 and 121 links); those come from
   the nearest year. In 2014, 46 links point to UCCs discontinued in 2013Q1 that remain in the stub; they have no 2014
   mean and get zero weight.
4. **Categories.** The lowest mapped 2.4.5U lines, subtrees collapsed (e.g. 160 owners' imputed rent, 183 hospitals,
   241 other purchased meals): 132-133 per year. One mapped line has mapped lines beneath it (74, fed only by 'food
   prepared on out-of-town trips'); its weight is spread over the food-at-home lines by PCE value.
5. **Withheld decile cells.** Table 1110 withholds RSE >= 25% decile means in 2022-2023 (in 2023: new cars d01-d05,
   most children's-clothing deciles, all of other vehicles; 21-23 items per year). They are filled from the all-CU
   identity N_all m_all = sum_d N_d m_d, the residual spread equally per CU over the withheld deciles. 2024 and 2025
   withhold nothing, which is why 2024 is B's main base year.

Checks: a single-feeder line's theta equals the share recomputed from Table 1110 (tenant rent 0.138, tobacco 0.152;
2024). B's thetas run from 0.14 (tenant rent) to 0.58 (higher education, educational books), weighted mean 0.37.

**Coverage of PCE by B** (`out/fingerprint_coverage_B.csv`): 92% of PCE sits in mapped categories in every year
(2024: $18.2tn of $19.8tn). That is generous: the health lines (22% of PCE) carry out-of-pocket distributions although
most of their value is paid by insurers and government (employer- and government-paid care has no CE counterpart), and
owners' imputed rent (12%) carries the CE rental-equivalence answers. Excluding the health lines, 70% of PCE has a CE
counterpart. No CE counterpart, excluded (2024): NPISH final consumption ($614bn), financial services furnished
without payment ($525bn), portfolio management and investment advice ($284bn), social assistance ($225bn), workers'
compensation and income-loss insurance ($42bn), securities commissions and trust services ($54bn), religious, civic
and foundation services ($42bn), net expenditures abroad ($13bn), and the foreign-travel adjustment (expenditures in
the US by nonresidents, -$216bn). On the CE side, 73% of average annual expenditures sits in UCCs with a PCE target;
the rest is mainly pensions and Social Security, cash contributions, mortgage interest and property taxes.

## 4. Backtest (source A, where the dPCE gives group totals)

**What it can and cannot show.** The dPCE builds each year's group spending as that year's category totals times
CE-based decile shares. Running the estimator on the dPCE's own category totals and comparing with its group totals is
a consistency test: it shows how far category noise and within-category share drift push the inverse estimator. It
cannot validate the dPCE's group totals (constructed, not observed), cannot test an income ranking (the dPCE ranks by
spending), says nothing about B, and contains no K of Zandi's size (the dPCE's own gap stays within -3.8 to +3.1
points in every window). The `nipa_current` variant adds the revisions since the dPCE vintage. Real 'actuals' deflate
each decile by its dPCE Table 3 price index.

Two-group results (cumulative points; `out/fingerprint_backtest.csv`, `figures/fig_fingerprint_backtest.png`):

| Window | Nominal, dPCE totals: estimate [95% CI] | actual | error | Real: estimate [95% CI] | actual | error |
|---|---|---|---|---|---|---|
| 2003-2007 | -21.0 [-79.5, +22.9] | +1.8 | -22.8 | +19.2 [-25.8, +83.3] | +2.8 | +16.4 |
| 2007-2009 | -46.7 [-89.5, -1.2] | -3.8 | -42.9 | -25.2 [-59.3, +12.6] | -1.8 | -23.4 |
| 2009-2013 | +12.3 [-28.8, +52.6] | +3.1 | +9.2 | +14.6 [-19.7, +58.8] | +2.1 | +12.5 |
| 2016-2019 | +1.1 [-15.0, +16.8] | -2.2 | +3.2 | +1.4 [-32.9, +36.7] | -2.6 | +4.0 |
| 2019-2023 | +15.1 [-18.4, +47.2] | -1.8 | +16.9 | +8.3 [-34.3, +66.8] | -2.3 | +10.6 |
| 2021-2023 | -4.3 [-40.7, +30.1] | -0.9 | -3.4 | -7.0 [-34.1, +25.2] | -0.8 | -6.2 |

Every actual lies inside its interval, because the intervals are wide. The errors are not small: 2007-2009 gives a
"significant" -47 points (p = 0.048) when the dPCE's own gap was -3.8: durables and vehicles, bought by the top,
collapsed for cyclical reasons. Across all rolling windows 2000-2023 the error has a standard deviation of 15.5 points
nominal and 8.6 real over two years, 22.8 and 10.7 over three, 30.4 and 12.6 over four. The fixed-share basket's
"errors" are tiny only because the basket barely moves (kappa x estimate).

**B against CE's own group totals** (nominal, Table 1110 means x CU counts; income-ranked but survey-based). CE's
top20 - bottom80 gap stays within -1.7 to +1.8 points in every window (total spending; -2.5 to +4.2 for the
PCE-scope part); B's estimates (theta of the start year): 2014-2016 +17.7, 2016-2019 +19.0
(p = 0.04), 2019-2021 -43.8 (p = 0.06), 2021-2023 +45.4 (p = 0.01; real +54.9, p = 0.003), 2019-2023 -0.4,
2023-2025 +10.3, 2022-2025 +25.6. What the top buys fell harder in 2020 and rebounded harder after: category shocks
correlated with theta. The permutation placebo assumes the opposite, so it does not protect against false alarms.

## 5. The read

Two groups, all categories, main theta (A: dPCE 2023; B: CE 2024); cumulative points over the window
(`out/fingerprint_read.csv`; categories behind it in `out/fingerprint_read_categories.csv`):

| Window (Zandi's gap) | Source | Nominal: gap [95% CI], placebo p | Real: gap [95% CI], placebo p | Real, per year |
|---|---|---|---|---|
| 2023 -> 2025 (+8.2) | A | -2.7 [-29.3, +31.5], 0.86 | -5.0 [-22.5, +17.0], 0.67 | -2.4 |
| | B | +8.5 [-13.8, +31.4], 0.45 | +16.8 [-0.7, +34.8], 0.06 | +8.1 |
| 2023-09 -> 2026-09 (+12.5) | A | -1.0 [-33.7, +37.9], 0.95 | -3.6 [-27.7, +27.7], 0.83 | -1.1 |
| | B | +13.5 [-8.8, +36.7], 0.24 | +20.0 [-4.0, +44.8], 0.10 | +6.2 |
| 2022-09 -> 2026-09 (+17.0) | A | -7.2 [-51.3, +48.3], 0.77 | -6.5 [-43.6, +41.2], 0.78 | -1.5 |
| | B | +23.2 [-10.5, +61.2], 0.19 | +33.2 [-2.8, +71.8], 0.07 | +7.5 |

No interval excludes Zandi's gap (p_zandi 0.25-0.97) and none excludes zero. Fit: theta explains at most 5% of the
weighted variance of category growth. Against a flat split, Zandi's pattern fits worse in A (R^2 -0.05 to -0.19) and
marginally better in B (+0.01 to +0.04); the fitted line beats both only trivially (`fig_fingerprint_scatter.png`).

**Sensitivity.** Theta years barely matter (B real, 2023-09 window: 2023 theta +19.8, 2024 +20.0, 2025 +23.6; A 2022
theta for the 2022-09 window -8.1 real). The robustness drops move A a lot and B little: A without health care turns
positive (+12.0 real, +16.5 nominal, 2023-09 window) because health care is A's most bottom-weighted line and grew
15% in real terms; A without the imputed lines falls to -9.6. B stays between +17.8 and +25.0 real across the five
drops (all four dropped: +21.9).

**What carries B** (`out/fingerprint_influence.csv`). In the 2023-09 window (real), tobacco (theta 0.15, real -25%:
secular decline), home health care (0.57, from CE's out-of-pocket personal-care spending, but the PCE line is mostly
Medicare and Medicaid and grew 31%: the care boom), and tenant rent (0.14, real +3.6%: housing supply) contribute
+19 of the 20 points. Dropping those three leaves +1.8; dropping five, -5.9. Dropping the three largest negative
contributors (higher education, prescription drugs, new autos) gives +34.6. None of these has an income-group story.

**Four and five groups.** The group columns of theta are nearly collinear (median condition numbers of theta'W theta:
A 1,800 for four groups and 24,000 for five; B 900 and 2,300). Unconstrained fits are meaningless at the 16-line level
(A, 2023-09 window, real, five groups: quintile growth from -352% to +337%; four groups: gap -12.7 [-160.7, +139.1]).
Ridge CV chose the largest lambda (equal growth, gap near 0 by construction) in 77% of A's four-group fits and 46% of
its five-group fits, and in 15% of B's. When it does not, A's fits are as wild as the unconstrained ones (A, real,
five groups, lambda 1e-4: quintiles from -310% to +282%). B, 2023-09 window, real: four groups +14.5 [-0.0, +73.9]
(bottom 50% -2.7%, 50-80 +8.4%, 80-90 +25.5%, top 10% +11.6%; placebo p = 0.13); five groups +9.1 [-36.7, +42.4]. The
extra groups add nothing the two-group fit does not already say.

**Against the benchmarks.** Historically calibrated band (error sd where group totals are known): A real three-year
+-21 points, B +-88; neither band excludes zero or Zandi. Calm-period norm (three-year windows, 2010/2014-2019): see
section 6.

**eta variant: skipped.** `consumption/data/tidy/usda_tb1929_params.csv` does not exist, so the Working-model
elasticities (eta = 1 + beta / w) were not run. See the caveats for what that leaves open.

## 6. Power: can the method see a K of Zandi's size?

| Benchmark (three-year windows) | A nominal | A real | B nominal | B real |
|---|---|---|---|---|
| Error sd where group totals are known (A vs dPCE 2000-2023; B vs CE 2014-2025) | 22.8 | 10.7 | 43.9 | 44.8 |
| Power against Zandi's 12.5 (two-sided 5%) | 8% | 21% | 5% | 5% |
| Calm-period norm, 36-month windows: mean (sd) | +14.6 (8.6) | +7.1 (5.3) | +18.3 (8.1) | +21.0 (6.4) |
| 2023-09 -> 2026-09 estimate (theta of the start year, as in the rolling windows) | -1.0 | -3.6 | +16.5 | +19.8 |
| Excess over the calm norm (z) | -15.6 (-1.8) | -10.7 (-2.0) | -1.8 (-0.2) | -1.3 (-0.2) |
| Smallest gap detectable with 80% power, calm noise | 24 | 15 | 23 | 18 |
| Zandi's split, z against what is observed | -3.3 | -4.4 | -1.8 | -2.1 |

Calm windows: A starts 2010-01 to 2016-12 (84 windows), B 2014-01 to 2016-12 (36), all ending by 2019-12. Over all
36-month windows since 2007 (A) and 2014 (B), which include 2008-09 and 2020-21, the spread is far wider: sd 19.0 and
11.3 for A, 50.8 and 49.9 for B (nominal, real).

The other two windows against their calm norms (read table, main theta; real terms, nominal in brackets):

| Window (calm windows A / B) | A: excess (z); Zandi's z | B: excess (z); Zandi's z |
|---|---|---|
| 2023 -> 2025 (8 / 4 annual windows) | -9.5 (-2.0); -3.6 [nominal -11.0 (-1.6); -2.7] | +6.6 (+0.9); -0.2 [nominal -1.2 (-0.2); -1.4] |
| 2022-09 -> 2026-09 (72 / 24 monthly windows) | -16.6 (-2.1); -4.3 [nominal -28.9 (-2.7); -4.3] | +11.7 (+3.2); -1.4 [nominal +2.4 (+0.4); -2.2] |

For B's four-year window the theta year matters: with the 2022 theta (the start-year theta the rolling windows use)
the real excess is +4.9 (z +1.3) and Zandi's z -3.3. The four-year B norm is the thinnest (24 heavily overlapping
windows from two years of starts, sd 3.7 points) and its window starts in the reopening year, when the services the
top buys were still recovering (B's twelve-month tilt ran at +0.5 to +2.5 points, median +1.1, through 2022; section 7).

**Assessment.** As a stand-alone test the method does not have the power to see a K of Zandi's size: its errors
where the answer is known are as large as his gap (A) or three to four times larger (B), it gave significant false
alarms in two of seven B windows and one of six A windows, and power is 5-21%. Benchmarked against its own calm-period
readings it does better: the smallest three-year gap it could detect with 80% power is 15-18 points in real terms
and 23-24 nominal, 1.2 to 1.9 times Zandi's, and on that benchmark the 2023-2026 readings sit at (B) or below (A) the
norm, about 2 to 4 standard deviations short of Zandi's split, for the three-year window. Over two and four years B
sits above its norm (by +7 and +5 to +12 points real) and Zandi's split is 0.2 to 3.3 sd away, so the B evidence
against a Zandi-size K is limited to the three-year window. All of it is only as good as the assumption that
category shocks in 2023-2026 resembled 2010/2014-2019; the care boom, the 2026 energy-price spike and the
post-pandemic normalization of services all say they did not.

## 7. Top-tilt index (descriptive)

tilt = real growth of the top 20%'s basket minus that of the bottom 80%'s basket, each basket fixing the group's
base-year budget shares (omega_qg = theta_qg S_g / sum_g theta_qg S_g), chained by base year (dPCE theta of the base
year, frozen at 2023 afterwards; CE theta 2014-2025 for B). Monthly twelve-month changes: A from 2007-01 (2006 bases
from 2.4.3U quantity indexes), B from 2015-01; annual A from 2001 (`out/top_tilt_monthly.csv`,
`out/fingerprint_top_tilt_annual.csv`, `figures/fig_top_tilt.png`; NBER recessions and 2020 shaded).

**What it measures**: whether real spending growth comes from what the top buys or from what the bottom buys. **What
it does not measure**: group spending growth. A within-category K barely moves it (kappa 0.03-0.06), and it moves with
everything else that differs between the baskets: Engel effects, relative prices, supply shocks, quality adjustment
and secular trends. Divided by kappa it equals the two-group slope for that twelve-month window (identity checked).

Readings. A's annual tilt index stands at 100.2 in 2025 (2000 = 100): the two baskets grew at almost the same real
rate for 25 years, with dips in 2008-2009 (-0.5 and -0.7 points a year) and a rebound in 2021 (+0.7). A Zandi-size K
would add about +0.23 points a year (A weights) or +0.13 (B weights). A's twelve-month tilt averaged -0.08 points over
2023-2026 (implied gap -1.5 points a year), latest -0.01 (2026-09). B's averaged +0.36 points (implied +11 a year,
inflated by early-2023 reopening months) against +0.15 in 2015-2019 (implied +5); from 2024-01 to 2026-09 its median
was +0.29 (implied +9; range -0.3 to +14), latest +0.13 (implied +4.2, 2026-09). A's median over the same months was
-0.04 (implied -0.7; range -12 to +7).

## 8. Caveats

- **eta = 1.** Without Working-model elasticities the model reads ordinary Engel effects as a K: luxuries (high theta)
  outgrow necessities whenever aggregate real income rises. As an illustration only (assumed elasticities), if eta
  ran from 0.5 at theta = 0.15 to 1.5 at theta = 0.57 and real spending per household rose 6-8% in three years, the
  two-group slope would show a spurious 14-19 points with no change in the distribution. That is the size of B's
  calm-period norm, which is why the norm is the benchmark.
- **Category noise is not exchangeable with theta.** What the top buys is more cyclical (vehicles, travel,
  recreation), was hit harder in 2020 and rebounded harder; the placebo and the permutation intervals assume
  otherwise and understate the uncertainty (section 4).
- **Rankings differ.** A ranks by equivalized spending and gives third-party health care to its recipients; B ranks by
  income before taxes but gives the health lines out-of-pocket distributions near the average. They disagree most on
  health care, the line the care boom runs through.
- **Top coverage.** Both surveys put the top 20% near 39% of spending. If they compress the top's market shares
  (measured theta = c x true theta, c < 1) the slope is gap / c: a real K would be read as larger, and so would the
  noise. Compressed thetas do not create a K where category growth is unrelated to who buys.
- **Vintages and timing.** dPCE thetas and totals are on the 2024-09 NIPA vintage, category growth on 2026-10. CE 2025
  was collected through the October-November 2025 funding lapse (weights adjusted; larger variances). Monthly windows
  use single months at seasonally adjusted annual rates; monthly PCE detail is BEA's lowest-quality detail.
- **Recession dates** (NBER: 2001-03 to 2001-11, 2007-12 to 2009-06, 2020-02 to 2020-04) are typed in for shading.

## 9. Judgment calls

1. Theta base years: A dPCE 2023 for every read window (2022 as a sensitivity for the 2022-09 window). B CE 2024 main
   (no withheld cells), 2023 and 2025 as sensitivities, 2022 for the 2022-09 window; a 2024 theta sits inside the
   2023-2025 windows.
2. Weights: base-period nominal spending (annual: base year; monthly: base month at SAAR).
3. Real growth: chained dollars where both endpoints exist, else 2.4.3U quantity indexes.
4. Zandi's split as a cumulative gap 1.04^T - 1, bottom 80% at zero, level shifted to the actual aggregate; same gap
   for nominal growth.
5. A drops at whole-line level: health = line 16; imputed = 15, 20, 22 (owners' rent and FISIM cannot be split out);
   energy = 11; vehicles = 4 (parts included). B drops: everything under 172, 121, 66, 275 (health); 160 and 163
   (imputed rent; FISIM and NPISH are not covered anyway); under 113 and 169 (energy); under 5 and 12 (vehicles).
6. B mapping (section 3): item distribution applied to all its UCCs; Table 2500 spending weights; PCE-proportional
   splits; the 78-UCC supplement; the out-of-scope list; owners' rent through the rental-equivalence addendum; health
   lines with out-of-pocket thetas; withheld cells from the all-CU identity; withheld UCC means from the nearest year.
7. Inference: permutation test inversion for the main interval; ridge lambda by exact LOO-CV, re-chosen per
   replicate; 1,000 permutations (two groups), 500 + 500 replicates (multi-group).
8. Calm periods for the norm: A from 2010, B from 2014, both ending by 2019-12.
9. B benchmark: CE Table 1110 group totals (total spending; a PCE-scope variant is in the backtest file); for the real
   estimate the nominal CE gap stands in.

## Files

| File | What |
|---|---|
| `code/fingerprint.py` | Everything: thetas, mapping, backtest, read, influence, power, top tilt, charts (about 13 minutes; `# %%` cells). |
| `checks/check_fingerprint.py` | Independent re-implementation and identities; PASS/FAIL per check. |
| `out/fingerprint_theta_A.csv` | dPCE thetas, 16 lines x 2000-2023: deciles and every group, base spending (dPCE vintage and current NIPA). |
| `out/fingerprint_theta_B.csv` | CE-mapped thetas, 132-133 PCE lines x 2014-2025, with the feeding line items. |
| `out/fingerprint_mapping_B.csv` | Year x line item x UCC x PCE target: source (BLS map, supplement, out of scope, unmapped), weight, rule, reason. |
| `out/fingerprint_coverage_B.csv` | Coverage of PCE and of CE spending by year; PCE lines with no CE counterpart. |
| `out/fingerprint_backtest.csv` | A against dPCE group totals; B against CE group totals. |
| `out/fingerprint_read.csv` | Window x source x theta year x spec x sample x measure: gap, intervals, p-values, fit vs Zandi and flat, benchmarks. |
| `out/fingerprint_read_categories.csv` | Category-level data behind the scatter. |
| `out/fingerprint_influence.csv` | Each category's contribution to the slope and the gap without it. |
| `out/fingerprint_power.csv` | Rolling windows (A annual vs dPCE, B annual vs CE, 36- and 48-month) and summaries. |
| `out/top_tilt_monthly.csv`, `out/fingerprint_top_tilt_annual.csv` | Top-tilt index. |
| `figures/fig_fingerprint_scatter.png`, `fig_fingerprint_backtest.png`, `fig_top_tilt.png` | Charts (200 dpi). |

Raw files added through `common.fetch` (rows in `raw/bls_ce/MANIFEST.csv`): `raw/bls_ce/stubs/pumd_doc.htm`,
`raw/bls_ce/stubs/stubs.zip` (hierarchical groupings 1996-2025), `raw/bls_ce/tables/detail/cu-all-detail-2014..2025.xlsx`
(Table 2500).
