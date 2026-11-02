# Fingerprint test: is US spending being held up by higher incomes, and can the national accounts see it?

Question 2, income-group angle (Stella's 2026-06-14 post). The sector angle is `NOTES_sectors.md`; the direct reads
of the official distributions are `NOTES_direct.md`. Built 2026-11-02 by `code/fingerprint.py`; checks in
`checks/check_fingerprint.py`. Re-derived independently by `checks/verify_independent_fingerprint.py`; section 11
records what that changed. Data, all vendored in `consumption/data/`: NIPA vintage of 2026-10-29 (monthly to 2026-09,
annual to 2025), BLS distributional PCE (March 2025), CE Tables 1110 and 2500 for 2014-2025, and the USDA TB-1929
demand-system parameters.

Run from the repo root:

    venv/bin/python -I consumption/recent/code/fingerprint.py           # about 11 min: out/, figures/
    venv/bin/python -I consumption/recent/checks/check_fingerprint.py   # about 10 s: 79 PASS, 0 FAIL, 2 INFO

## Answer in plain words

**The category mix of national-accounts spending cannot settle whether US spending is being held up by higher
incomes.**
- As built, its answer depends mostly on who the care boom is attributed to.
- With the care lines set aside, both sources read about what they read in the calm 2010s. That is not what a K
  would look like, but the estimator's noise is as large as Zandi's gap, so it cannot rule a K out either.
- The direct survey evidence is cleaner, and it shows no K across the top fifth.

- **What the test asks.** If the top 20%'s spending outgrew the rest, the categories the top buys should outgrow the
  rest in the national accounts. The estimator turns each category's growth and its top-20 market share into an
  implied top20 - bottom80 gap. Zandi's split (top 20% +4% a year in real terms, bottom 80% flat) is a gap of +12.5
  points over three years.
- **The care lines decide the sign.**
  - Health care, medical goods, net health insurance and child care are nearly a quarter of PCE. Health care
    services grew 15% in real terms from 2023-09 to 2026-09, and who that spending is attributed to decides the
    answer.
  - The official distributional PCE (source A) attributes Medicare- and Medicaid-financed care to the people who
    receive it, so health care is its most bottom-weighted line (top-20 share 0.26). A reads -3.6 points over three
    years in real terms, and +12.0 without the health-care line, about Zandi's +12.5.
  - The CE-mapped source (B) gives the care lines out-of-pocket distributions near the average (0.29-0.37). As first
    built it also gave home health care the distribution of child care (0.57). That mapping artifact put part of the
    care boom on the top's side. With it fixed, B reads +14.6 with the care lines and +20.2 without.
  - A care boom and a K both show up as fast growth in some categories, and the estimator cannot tell them apart.
    With the care lines in, it tests how care is attributed, not who is spending.
- **Without the care lines, both sources read about their calm-years level.**
  - Over three years, in real terms, A reads +12.0 against +11.8 on average in 2010-2019 windows of the same
    length, and B reads +20.2 against +20.9. Zandi's split predicts the calm reading plus 12.5 points (A +24.3,
    B +33.4).
  - In nominal terms both sit 5-11 points below their calm readings.
  - That leans against a K of Zandi's size, but only weakly:
    - the calm readings rest on 3 (A) and 1 (B) non-overlapping windows, so they are a reference, not a noise
      estimate;
    - where group totals are known, the estimator's three-year error has a standard deviation of 11 points (A,
      real) and 47 points (B);
    - B's own backtests: the CE's own group gap never moved by more than 2 points, yet in every one of seven
      windows B missed it by 14 to 54 points in nominal or real terms, and by more than 20 in five of them (p
      below 0.05 in two windows, below 0.10 in four).
  - The other windows are mixed:
    - over two years B reads 4.7 points above its calm reading (Zandi: 8.2);
    - over four years from 2022-09, the reopening year, B reads 13.5 points above it in real terms (Zandi: 17.0)
      but 5.5 below it in nominal terms, and over 2022-2025 the same estimator read +26.2 while the CE's own gap
      was +1.6;
    - A never reads more than 1.4 points above its calm reading, in any window or measure.
- **Engel effects.**
  - With equal elasticities (eta = 1), necessities growing slower than luxuries as real income rises reads as a K.
  - The Working-model variant uses TB-1929 elasticities at each group's budget shares. It takes 8 points off B's
    three-year readings (to +6.6 with the care lines, +12.3 without) and 7 off B's calm reading (+21.5 to +14.4).
    A without health care loses 7 points (to +5.2) and its calm reading 3 (to +8.6).
  - The readings move with their references, so the comparison, and the conclusion, do not depend on it.
- **The direct evidence carries more weight.**
  - In the CE, income-ranked spending of the top 20% and of the bottom 80% both rose 8.7% from 2023 to 2025
    (nominal).
  - The top quintile's share of spending was 38.86% in 2023 and 38.88% in 2025, where Zandi's split would have added
    about 1.9 points.
  - The official top shares are flat through their last year (CE to 2025; BLS distributional PCE and the BEA-BLS
    joint distribution to 2023; `NOTES_direct.md`).
  - The CE under-covers the very top, so a K confined to the top few percent could hide from it. It would also hide
    from this test, whose market shares come from the same surveys.

This revision weakens the first build's conclusion. That build put Zandi's split "about 2 (B) to 4 (A) standard
deviations" above what the categories show. Those standard deviations came from heavily overlapping calm windows;
A's evidence rested on the health-care line, and B's partly on a mapping artifact (section 11).

## 1. The question and the claim

Is US spending being held up by higher incomes, and can that be seen in spending patterns? Mark Zandi (Moody's;
EconoFact Chats, 24 July 2026, `data/raw/other/econofact_zandi_2026-07-24.pdf`): "over the past say three years,
overall real consumer spending growth has been 2%. Folks that are in the top 20% of the income distribution, the
growth in their spending has been, on a real basis, after inflation, close to 4%. And the folks in the rest of the
distribution, the bottom 80%, their spending growth has been close to zero." Spending growth is "dependent on a small
group, who in turn is dependent on a run-up in equity prices".

Scale. Over three years Zandi's split is a cumulative gap of 1.04^3 - 1 = 12.5 points (8.2 over two, 17.0 over four).
The official distributions put the top 20% at about 39% of spending:
- the CE top quintile, income-ranked, at 37.3-38.9% of spending in 2019-2025 (38.45-38.88% leaving out 2020, when it
  dipped to 37.29%; `fingerprint_coverage_B.csv`);
- the dPCE top two deciles, spending-ranked, at 39.5% in 2023.

At those shares a 4-point-a-year gap lifts the top 20%'s share of spending by about 1.9 points in two years and 2.8
in three. His 4% and 0% would then average about 1.6%, not 2%; the test keeps his gap and lets the level match the
actual aggregate. Moody's own estimates, with the top 10% near half of spending, are not what the official
distributions show.

Context from the watch site: care took 107% of net job growth from August 2024 to August 2026, and real spending rose
1.8% in the six months to September 2026 against 0.1% (BEA: 0.05%) for real personal income excluding transfers.

## 2. Method

**Model.** Let theta_qg be income group q's market share of category g (its share of all spending on g), x_q the
growth of group q's total spending and eta_gq an Engel elasticity. If each group's spending on g grows by eta_gq x_q,

    g_g = sum_q theta_qg * eta_gq * x_q + e_g,

where e_g collects relative prices and substitution, supply shocks, quality adjustment and taste shifts common to all
groups. The x_q are identified from the cross-section because categories differ in who buys them.

**Main specification** (eta = 1, Zandi's split): g_g = x_b80 + theta_top20,g (x_top20 - x_b80) + e_g, by weighted
least squares with base-period nominal spending as weights. The slope is the top20 - bottom80 gap. With these weights
the fitted values average exactly to the covered categories' aggregate growth.

**Why the inverse model, not a fixed-share basket.** A K can work within categories (the top buying more of
everything). A fixed-market-share basket attributes each category's growth to whoever already buys it, so it reads a K
as a small tilt. With the same weights the two are the same statistic in different units:

    basket gap = kappa x slope,   kappa = Var_w(theta_top20) / (theta_bar (1 - theta_bar)).

In the 2023-09 read kappa is 0.056 for the 16 lines (2023 theta) and 0.029 for the 133 CE-mapped lines (2024 theta),
so a basket index shrinks a K by a factor of 18 (A) to 34 (B). Over all years kappa runs 0.047-0.066 (A) and
0.027-0.032 (B). The inverse model puts it back into group-growth units; the t-statistic is unchanged. So power is the
same question either way: how wide is the spread of theta across categories against the category noise e_g?
- At the 16-line level a Zandi-size three-year K moves category growth by 1.4 points per standard deviation of
  theta (0.116). Categories scatter by 4.3 points real (5.8 nominal) around their mean over the same three years.
- At the 133-line level the numbers are 1.0 point against 8.7 real (8.0 nominal).

**Specs.**
- Two groups (main), run on a headline pair of samples: all categories, and without the care lines. The care lines
  are definition (c) of `NOTES_sectors.md`: health care services (172), pharmaceutical and other medical products
  (121), therapeutic appliances (66), net health insurance (275), child care (316) and social assistance (317). B drops
  the 15 lines it has under them. A can drop only line 16 (health care services); the rest sit inside lines 7, 12, 20
  and 21 with non-care spending.
- The eta variant (Working-model elasticities, section 7), on the same pair.
- Four groups (bottom 50 / 50-80 / 80-90 / top 10) and five (quintiles), for reference, by unconstrained WLS and by
  ridge toward equal growth (penalty lambda sum_k pi_k (x_k - xbar)^2, pi = groups' spending shares). Lambda is chosen
  by exact leave-one-category-out CV, re-chosen inside every bootstrap and permutation replicate.
- Robustness drops: health care, imputed items, energy, motor vehicles, and all four.
- Nominal and real for everything.

**Inference.**
- The two-group 95% interval comes from permutation test inversion: H0 gap = c is tested by permuting theta in
  g - c theta. This is exact because the slope is linear in c.
- 5,000 permutations, drawn fresh for every fit from a seed of its own. The first build reused one set of 1,000
  wherever the number of categories was the same.
- The placebo p-value is that test at c = 0 (theta permuted across categories); p_zandi is the test at Zandi's gap.
- Classical WLS and HC3 standard errors are also in the file (HC3 typically 1.5-2 times the classical).
- Multi-group intervals: pairs bootstrap (500); placebo 500.

**Zandi and flat.** Zandi's predicted pattern is the actual aggregate plus (theta - theta_bar) x his cumulative gap;
the flat split predicts the aggregate for every category. Fit is the weighted RMSE, and R^2 against flat. His numbers
are real; the same gap is used for nominal growth (ISPCEPX 2019-2024 inflation: top quintile 19.9%, others
19.1-19.5%, about 0.1 point a year).

**Two benchmarks**, attached to every headline read row (`fingerprint_read.csv`, `fingerprint_power.csv`) for both
samples and both eta settings:
1. **The estimator's error where group totals are known.** Annual windows of the same length: A against the dPCE
   group totals (2000-2023), B against the CE Table 1110 group totals (2014-2025). Read as a band, gap +- 1.96 sd. The
   rolling windows overlap, so the file also keeps the count of non-overlapping windows and the sd over those alone.
2. **The calm-period reference reading.** The mean estimate in windows of the same length that start after the
   2008-09 recession (A from 2010, B from 2014) and end by 2019-12, when neither the dPCE nor the CE shows a K. It is
   the estimator's ordinary reading in quiet years: Engel effects, secular trends, quality adjustment. Zandi's split
   predicts the reference plus his gap.
   - The calm windows overlap heavily. Three-year: A's 84 windows hold 3 non-overlapping ones, B's 36 hold 1.
     Four-year: A 72 and 2, B 24 and 1. Two-year: A 8 and 4, B 4 and 2.
   - So the reference is a reading, not a noise estimate. No z-score, minimum detectable effect or power is built on
     its spread. The non-overlapping windows' own readings are listed instead.

## 3. The two theta sources

**(A) BLS distributional PCE, Table 1** (`bls_dpce_long.csv`, March 2025 results, NIPA vintage of 2024-09).
- Decile shares of each of the 22 NIPA Table 2.3.5 lines, 2000-2023; the 16 leaf lines are the categories. Deciles
  are of equivalized total spending, not income.
- The dPCE imputes third-party health care to its recipients, so health care is A's most bottom-weighted line
  (top-20 share 0.26). Motor vehicles is its most top-weighted (0.67).
- Line 22 (NPISHs) carries the total-PCE shares by construction and has no leverage on the slope.
- Growth comes from Tables 2.3.5/2.3.6 (annual) and 2.8.5/2.8.6 (monthly). Lines 1-22 carry the same series codes in
  both and equal the 2.4.5U values cell for cell (checked).
- Real growth comes from chained dollars where both endpoints are published (2007 on), else from the 2.4.3U quantity
  index of the same series (identical ratios, checked).

**(B) CE Table 1110** (deciles of income before taxes, 2014-2025) mapped to 2.4.5U lines. The chain: line item -> UCCs
from BLS's integrated hierarchical-grouping file for the year (`raw/bls_ce/stubs/stubs.zip`, CE-HG-Integ-YYYY.txt) ->
PCE series from BLS's `ce_pce_map` -> 2.4.5U line through the BEA mnemonics. `out/fingerprint_mapping_B.csv` has every
year x item x UCC x target with its rule, the item whose distribution it takes, and the reason. The rules:

1. **Items.** Table 1110 leaf expenditure items, with three fixes, each recorded in the mapping file's `item_rule`:
   - 2023-2025 show only `Gasoline` under `Gasoline and other fuels`, so the parent is used.
   - `Other vehicles` (motorcycles, boats, campers) is the residual vehicle purchases minus new minus used, by decile,
     mapped through the stub's other-vehicles UCCs. BLS dropped the row in 2024-2025. In 2023 Table 1110 withholds
     every cell of it, the all-CU mean included. The residual keeps the published decile information where the parent
     and both children are shown (2023: d06-d10). Deciles where a child is withheld (2023: new cars d01-d05, used cars
     d02) are filled like any withheld cell (rule 5). Spreading the item's all-CU mean equally per CU over all ten
     deciles instead would throw the d06-d10 information away: line 54 (motorcycles) would get a top-20 share of 0.20
     instead of 0.37 in 2023, with no effect on any headline.
   - The addendum `Estimated monthly rental value of owned home` (x12; non-owners count as zero) stands for owners'
     imputed rent, as in BLS's own map (UCC 910050 -> DOWNRC).
   73 items match the stub by label path, 2 by group code (gasoline, other vehicles).
2. **UCC -> PCE line.** BLS's map where it has the UCC.
   - The published tables take food and alcohol away from home, some audio-video goods and newspapers from the Diary,
     while BLS's map sources the same spending from Interview UCCs. Those Diary UCCs, and UCCs newer than the map, go
     to the target BLS uses for the analogous UCC (78-UCC supplement in `fingerprint.py`, each with a reason).
   - Left out as not PCE: property taxes, mortgage interest, vehicle registration and licence fees,
     Medicare/Medicaid/Tricare/CHIP premiums (social-insurance contributions), cash contributions, pension and Social
     Security deductions, education savings and prepaid tuition, and owner- and renter-paid dwelling maintenance
     (inputs to housing services; BLS's map leaves them out too).
   - One small in-scope UCC has no target and is dropped (002120 other non-health insurance, about $45 a year per CU).
3. **Allocation.**
   - Each item's decile distribution holds for all its UCCs. A PCE line fed by several items takes the mix of their
     distributions, weighted by CE spending on the UCCs that feed it: all-CU UCC means from BLS Table 2500
     (`raw/bls_ce/tables/detail/cu-all-detail-YYYY.xlsx`, rows aligned to the stub with difflib) times a split share.
   - A UCC BLS sends to several PCE series is divided in proportion to those lines' PCE values (BLS publishes no split
     proportions).
   - Table 2500 withholds some UCC means in 2022-2023 (RSE >= 25%; 126 and 121 links). Those come from the nearest
     year that publishes a value, numeric or "too small". A year that codes the UCC "no data reported" is never a
     stand-in. The first build took 22 zero stand-ins from 2024 cells of UCCs discontinued after 2024Q1 (boats,
     motorized campers, camper rentals); the effect on thetas was below 0.01.
   - In 2014, 46 links point to UCCs discontinued in 2013Q1 that remain in the stub; they have no 2014 mean and get
     zero weight.
   - **One exception to "each item's distribution holds for all its UCCs" (judgment).** The elder- and adult-care
     UCCs inside `Personal services` (340906 care for elderly, invalids, handicapped; 340910 adult day care centers)
     take the distribution of `Medical services`.
     - `Personal services` is 86% child care (UCC 670320 in 2024), bought by working-age parents and top-weighted.
       Applied to elder care, it gave home health care (line 177, whose only feeder with spending is 340906) a
       child-care top-20 share of 0.52-0.62 in every year, on a line mostly financed by Medicare and Medicaid.
     - `Medical services` holds the other out-of-pocket elder care BLS sends to the same lines (care in convalescent
       or nursing homes 570220, medical care in retirement communities 570240).
     - Home health care now carries 0.34-0.40 (0.369 in 2024), and nursing homes (187) 0.369.
     - This is still an out-of-pocket distribution. Recipients of publicly financed home care are older and poorer,
       and A gives health care 0.26.
     - The first build's mapping is kept as a sensitivity (`theta_top20_rule1` in `fingerprint_theta_B.csv`;
       section 5).
4. **Categories.** The lowest mapped 2.4.5U lines, with subtrees collapsed (e.g. 160 owners' imputed rent, 183
   hospitals, 241 other purchased meals): 132-133 per year. One mapped line has mapped lines beneath it (74, fed only
   by 'food prepared on out-of-town trips'); its weight is spread over the food-at-home lines by PCE value.
5. **Withheld decile cells.** Table 1110 withholds decile means with RSE >= 25% in 2022-2023 (in 2023: new cars
   d01-d05, most children's-clothing deciles, all of other vehicles; 21-23 items per year). They are filled from the
   all-CU identity N_all m_all = sum_d N_d m_d, with the residual spread equally per CU over the withheld deciles.
   2024 and 2025 withhold nothing, which is why 2024 is B's main base year.

**Flags on the care lines.** All of these lines are inside the "without care" sample.
- **Net health insurance** (276, $229bn in 2024) takes the `Health insurance` item's distribution (top-20 share
  0.305). That item includes the out-of-scope Medicare, Medicaid, Tricare and CHIP premium UCCs: 18% of its UCC
  spending in 2014 and 25% in 2024 (`fingerprint_coverage_B.csv`). Those premiums are paid mostly by older, lower-income
  CUs, so the line's theta understates the top's share of private premiums. Table 1110 does not split the item, so
  this cannot be corrected.
- **Prescription drugs** (123, $549bn) carry the `Drugs` distribution (0.29). That is out-of-pocket spending, while
  most of the line is paid by insurers, Medicare Part D and Medicaid.
- **Every B health line** carries an out-of-pocket distribution (0.29-0.37), although most of its value is paid by
  insurers and government. A instead carries recipient-based shares (0.26 for health care). The two sources disagree
  most on exactly the lines the care boom runs through (section 5).

Checks:
- A single-feeder line's theta equals the share recomputed from Table 1110 (2024: tenant rent 0.138, tobacco 0.152,
  home health care 0.369 = `Medical services`).
- B's thetas run from 0.14 (tenant rent) to 0.58 (higher education, educational books). The PCE-weighted mean is
  0.37 (2024).

**Coverage of PCE by B** (`out/fingerprint_coverage_B.csv`).
- 92% of PCE sits in mapped categories in every year (2024: $18.2tn of $19.8tn).
- That is generous. The health lines (22% of PCE) carry out-of-pocket distributions although most of their value is
  paid by insurers and government (employer- and government-paid care has no CE counterpart). Owners' imputed rent
  (12%) carries the CE rental-equivalence answers.
- Excluding the health lines, 70% of PCE has a CE counterpart.
- No CE counterpart, excluded (2024): NPISH final consumption ($614bn), financial services furnished without payment
  ($525bn), portfolio management and investment advice ($284bn), social assistance ($225bn), workers' compensation
  and income-loss insurance ($42bn), securities commissions and trust services ($54bn), religious, civic and
  foundation services ($42bn), net expenditures abroad ($13bn), and the foreign-travel adjustment (expenditures in
  the US by nonresidents, -$216bn).
- On the CE side, 73% of average annual expenditures sits in UCCs with a PCE target. The rest is mainly pensions and
  Social Security, cash contributions, mortgage interest and property taxes.

## 4. Backtest: the estimator where group totals are known

**What it can and cannot show.**
- The dPCE builds each year's group spending as that year's category totals times CE-based decile shares. Running
  the estimator on the dPCE's own category totals and comparing with its group totals is a consistency test: it
  shows how far category noise and within-category share drift push the inverse estimator.
- It cannot validate the dPCE's group totals, which are constructed, not observed. It cannot test an income ranking
  (the dPCE ranks by spending), and it says nothing about B.
- It contains no K of Zandi's size: the dPCE's own gap stays within -3.8 to +3.0 points in every window.
- The `nipa_current` variant adds the revisions since the dPCE vintage. Real "actuals" deflate each decile by its dPCE
  Table 3 price index.
- B runs against the CE's own group totals: income-ranked and survey-based. Their gap stays within -1.7 to +1.8
  points in every window (-2.5 to +4.2 for the PCE-scope part).
- Because the CE under-covers the very top, a B reading above the CE's own gap could in principle be a K the CE
  misses. In 2014-2019 and 2019-2023 nobody claims one; in 2022-2025 the two cannot be told apart.

Two groups, cumulative points; p is the placebo p-value from 5,000 fresh permutations per window
(`out/fingerprint_backtest.csv`, `figures/fig_fingerprint_backtest.png`).

**A against the dPCE's own group totals:**

| Window | Nominal, dPCE totals: estimate [95% CI], p | actual | error | Real: estimate [95% CI], p | actual | error |
|---|---|---|---|---|---|---|
| 2003-2007 | -21.0 [-82.4, +28.1], 0.35 | +1.8 | -22.8 | +19.2 [-30.0, +80.2], 0.42 | +2.8 | +16.4 |
| 2007-2009 | -46.7 [-89.4, -1.0], 0.046 | -3.8 | -42.9 | -25.2 [-59.7, +10.0], 0.14 | -1.8 | -23.4 |
| 2009-2013 | +12.3 [-31.0, +51.8], 0.50 | +3.0 | +9.2 | +14.6 [-24.2, +61.1], 0.40 | +2.1 | +12.5 |
| 2016-2019 | +1.1 [-14.5, +16.0], 0.84 | -2.2 | +3.2 | +1.4 [-30.6, +39.0], 0.93 | -2.6 | +4.0 |
| 2019-2023 | +15.1 [-16.9, +48.4], 0.33 | -1.8 | +16.9 | +8.3 [-35.4, +64.3], 0.67 | -2.3 | +10.6 |
| 2021-2023 | -4.3 [-39.0, +27.0], 0.76 | -0.9 | -3.4 | -7.0 [-36.3, +25.9], 0.64 | -0.8 | -6.2 |

**B against the CE's own group totals** (theta of the start year; for real estimates the nominal CE gap stands in):

| Window | Nominal: estimate [95% CI], p | Real: estimate [95% CI], p | CE gap, total spending | CE gap, PCE scope |
|---|---|---|---|---|
| 2014-2016 | +17.9 [-18.0, +52.6], 0.33 | +7.1 [-16.8, +29.4], 0.58 | +0.2 | -2.0 |
| 2016-2019 | +18.4 [-1.2, +39.0], 0.064 | +27.9 [-3.0, +59.6], 0.078 | -1.7 | +1.0 |
| 2019-2021 | -44.8 [-88.7, -2.9], 0.037 | -33.7 [-77.9, +9.4], 0.12 | -0.9 | -2.5 |
| 2021-2023 | +46.3 [+13.1, +83.0], 0.009 | +55.7 [+25.6, +88.6], 0.001 | +1.8 | +2.4 |
| 2019-2023 | -1.0 [-36.5, +34.3], 0.96 | +23.0 [-16.2, +63.8], 0.21 | +0.9 | -0.3 |
| 2023-2025 | +7.1 [-16.1, +30.2], 0.54 | +14.2 [-4.4, +33.3], 0.12 | +0.1 | +1.2 |
| 2022-2025 | +17.8 [-23.6, +60.4], 0.41 | +26.2 [-4.3, +59.0], 0.088 | +1.6 | +4.2 |

**False alarms.** A false alarm is p < 0.05 where the known gap is within 4 points, counted across nominal and real
(`out/fingerprint_false_alarms.csv`).
- **A: one window of six, and it is borderline.** 2007-2009 nominal gives p 0.046 with the dPCE's category totals
  (interval up to -1.0) and 0.051 with NIPA growth (interval up to +0.3). The first build's 1,000 draws gave 0.048;
  the verifier's 20,000 give 0.053. Durables and vehicles, bought by the top, collapsed for cyclical reasons. There
  is no false alarm in real terms.
- **B: two windows of seven at 5%, four at 10%.**
  - At 5%: 2019-2021 nominal (p 0.037), and 2021-2023 nominal and real (0.009, 0.001).
  - At 10% two more: 2016-2019 (0.064 nominal, 0.078 real) and 2022-2025 real (0.088).
  - With the first build's elder-care mapping, 2016-2019 nominal (0.041) and 2022-2025 real (0.038) were below 5%
    as well. The verifier's own rebuild of that mapping, with 20,000 draws, finds four windows below 5%.
  - Which side of 5% these fall on depends on the mapping and the draws; the errors do not. In every window one
    measure misses the CE's own gap by 14 to 54 points, by more than 20 in five of seven, and every CE gap is within
    1.8 points.
  - 2022-2025 overlaps the read period: B read +26.2 in real terms (+17.8 nominal) where the CE's own gap was +1.6.
- What the top buys fell harder in 2020 and rebounded harder after: category shocks correlated with theta. The
  permutation placebo assumes the opposite, so it does not protect against false alarms.
- **The eta variant does not remove them.** B 2019-2021 nominal (p 0.020) and 2021-2023 (0.018 nominal, 0.005 real)
  stay, and A 2007-2009 nominal falls to 0.028.

Across all rolling windows 2000-2023, A's error has a standard deviation of:

| Window length | nominal | real |
|---|---|---|
| two years | 15.5 | 8.6 |
| three years | 22.8 | 10.7 |
| four years | 30.4 | 12.6 |

The fixed-share basket's "errors" are tiny only because the basket barely moves (kappa x estimate).

## 5. The read

Two groups, main theta (A: dPCE 2023; B: CE 2024), cumulative points over the window (`out/fingerprint_read.csv`;
categories behind it in `out/fingerprint_read_categories.csv`). The calm reference is the mean reading in calm-period
windows of the same length (section 6). Zandi's prediction is the reference plus his gap. "Without health care" is
A's only care drop (line 16).

**Real terms:**

| Window (Zandi's gap) | Source, sample | Gap [95% CI], placebo p | Calm reference | Gap - reference | Zandi's prediction |
|---|---|---|---|---|---|
| 2023 -> 2025 (+8.2) | A, all | -5.0 [-22.9, +16.1], 0.65 | +4.5 | -9.5 | +12.6 |
|  | A, without health care | +5.9 [-9.5, +20.9], 0.39 | +7.7 | -1.8 | +15.8 |
|  | B, all | +12.4 [-5.9, +31.6], 0.19 | +10.7 | +1.7 | +18.9 |
|  | B, without care lines | +15.5 [-1.9, +34.0], 0.077 | +10.8 | +4.7 | +18.9 |
| 2023-09 -> 2026-09 (+12.5) | A, all | -3.6 [-29.5, +25.7], 0.82 | +7.1 | -10.7 | +19.5 |
|  | A, without health care | +12.0 [-9.2, +31.2], 0.22 | +11.8 | +0.2 | +24.3 |
|  | B, all | +14.6 [-10.2, +39.8], 0.26 | +21.5 | -6.9 | +34.0 |
|  | B, without care lines | +20.2 [-1.0, +42.1], 0.061 | +20.9 | -0.7 | +33.4 |
| 2022-09 -> 2026-09 (+17.0) | A, all | -6.5 [-44.5, +40.5], 0.79 | +10.1 | -16.6 | +27.0 |
|  | A, without health care | +18.8 [-8.9, +48.5], 0.15 | +17.4 | +1.4 | +34.4 |
|  | B, all | +26.3 [-11.5, +65.0], 0.18 | +22.1 | +4.2 | +39.1 |
|  | B, without care lines | +34.5 [+2.9, +67.8], 0.034 | +21.0 | +13.5 | +38.0 |

**Nominal terms:**

| Window (Zandi's gap) | Source, sample | Gap [95% CI], placebo p | Calm reference | Gap - reference | Zandi's prediction |
|---|---|---|---|---|---|
| 2023 -> 2025 (+8.2) | A, all | -2.7 [-29.6, +30.4], 0.84 | +8.3 | -11.0 | +16.4 |
|  | A, without health care | +10.3 [-18.3, +41.5], 0.45 | +12.4 | -2.1 | +20.5 |
|  | B, all | +3.0 [-20.3, +26.5], 0.80 | +9.5 | -6.6 | +17.7 |
|  | B, without care lines | +4.7 [-21.7, +32.3], 0.75 | +11.1 | -6.4 | +19.3 |
| 2023-09 -> 2026-09 (+12.5) | A, all | -1.0 [-36.2, +35.7], 0.95 | +14.6 | -15.6 | +27.1 |
|  | A, without health care | +16.5 [-15.7, +46.0], 0.28 | +21.5 | -5.0 | +34.0 |
|  | B, all | +7.7 [-16.3, +32.0], 0.52 | +18.2 | -10.5 | +30.7 |
|  | B, without care lines | +8.6 [-14.4, +32.3], 0.46 | +19.8 | -11.2 | +32.3 |
| 2022-09 -> 2026-09 (+17.0) | A, all | -7.2 [-52.4, +44.0], 0.77 | +21.7 | -28.9 | +38.7 |
|  | A, without health care | +16.4 [-28.3, +61.1], 0.44 | +32.7 | -16.3 | +49.7 |
|  | B, all | +14.1 [-22.5, +52.3], 0.46 | +20.4 | -6.3 | +37.4 |
|  | B, without care lines | +17.5 [-21.6, +60.6], 0.40 | +23.0 | -5.5 | +40.0 |

**How to read the tables.**
- **No interval excludes Zandi's gap** (p_zandi 0.23-0.98).
- **One interval excludes zero:** B without the care lines over four years in real terms (+34.5 [+2.9, +67.8],
  p 0.034). Its window starts in the reopening year, and over 2022-2025 the same estimator read +26.2 against the
  CE's own +1.6 (section 4).
- **Fit.** With all categories, theta explains at most 3% of the weighted variance of category growth. Without the
  care lines it explains up to 16% (A) and 7% (B).
- **Zandi's pattern against a flat split.**
  - With all categories it fits worse than flat in A (R^2 -0.05 to -0.19) and about as well in B (-0.00 to +0.03).
  - Without the care lines it fits better than flat in both (A +0.05 to +0.16, B +0.00 to +0.05), but no better
    than the fitted line (`fig_fingerprint_scatter.png`).

**The care lines** (headline sensitivity).
- They move A by +15.7 points over three years (real: -3.6 with them, +12.0 without). Health care is A's most
  bottom-weighted line and grew 15% in real terms.
- They move B by +5.6 points (+14.6 to +20.2). B's care lines carry near-average out-of-pocket thetas and grew
  faster than the rest.
- Without them the two sources still disagree over two and four years (A below or at its reference, B above). Over
  three years they agree with each other and with their references.

**Elder care as first built** (sample `elder_care_on_personal_services`: home health care and nursing homes on the
`Personal services` distribution, 86% child care). B reads +16.8 / +20.1 / +33.3 real (two / three / four years) and
+8.5 / +13.5 / +23.2 nominal. The corrected mapping reads +12.4 / +14.6 / +26.3 and +3.0 / +7.7 / +14.1. The artifact
carried 4-7 points of B's real readings and 5-9 of its nominal ones.

**Theta years.** B real, 2023-09 window: 2023 theta +16.5, 2024 +14.6, 2025 +17.7. A with the 2022 theta for the
2022-09 window: -8.1 real.

**Robustness drops** (2023-09 window, real).
- B stays between +12.0 and +21.9 across the six drops: without energy +12.0, imputed +14.7, vehicles +19.2,
  health +19.5, care +20.2, all four +21.9.
- A moves a lot: without the imputed lines -9.6, energy -6.3, vehicles -1.9, all four +7.8, health care +12.0.

**What carries B** (`out/fingerprint_influence.csv`; 2023-09 window, real, all categories).
- Tobacco (theta 0.15, real -25%: secular decline) and tenant rent (0.14, real +3.6%: housing supply) contribute
  +13.1 of the 14.6 points. Dropping those two leaves +1.4; dropping the five largest positive contributors (adding
  gasoline, ground transportation, and clubs, parks and theaters) leaves -9.3.
- Dropping the three largest negative contributors (higher education, new autos, prescription drugs) gives +29.4.
- None of these has an income-group story.
- The first build's version of this paragraph listed home health care among the three main carriers (theta 0.57,
  "from CE's out-of-pocket personal-care spending"). That was the elder-care artifact: on the `Personal services`
  distribution, which is 86% child care, the line carried the care boom (+31% real) onto the top's side.

**Four and five groups.**
- The group columns of theta are nearly collinear. Median condition numbers of theta'W theta: A 1,800 for four
  groups and 24,000 for five; B 860 and 2,300.
- Unconstrained fits are meaningless at the 16-line level. A, 2023-09 window, real, five groups: quintile growth from
  -352% to +337%. Four groups: gap -12.7 [-145.3, +179.1].
- Ridge CV chose the largest lambda (equal growth, gap near 0 by construction) in 77% of A's four-group fits and 46%
  of its five-group fits, and in 23% of B's.
- When it does not, A's fits are as wild as the unconstrained ones (A, real, five groups, lambda 5.6e-5: quintiles
  from -310% to +282%).
- B, 2023-09 window, real: four groups +12.5 [-6.7, +51.8] (bottom 50% -4.0%, 50-80 +11.3%, 80-90 +31.7%, top 10%
  +5.0%; placebo p 0.14); five groups +2.0 [-38.6, +38.2].
- The extra groups add nothing the two-group fit does not already say.

## 6. Benchmarks: the error where group totals are known, and calm-period reference readings

Three-year windows; cumulative points (`out/fingerprint_power.csv`; summary rows by kind x measure x sample x spec).

| Three years, eta = 1 | A nominal | A real | B nominal | B real |
|---|---|---|---|---|
| Error sd where group totals are known, all windows (n) | 22.8 (21) | 10.7 (21) | 46.7 (9) | 46.7 (9) |
| ... non-overlapping windows only (n) | 27.4 (7) | 14.2 (7) | 77.5 (3) | 79.5 (3) |
| Power against Zandi's 12.5 from the all-window sd (two-sided 5%) | 8% | 21% | 5% | 5% |
| Calm reference reading, 36-month windows (n; non-overlapping) | +14.6 (84; 3) | +7.1 (84; 3) | +18.2 (36; 1) | +21.5 (36; 1) |
| ... the non-overlapping windows' own readings | +16.3, +23.2, +2.6 | +21.7, +4.0, -0.7 | +34.5 | +25.5 |
| ... range over all calm windows | -2.9 to +31.5 | -2.2 to +21.7 | +2.7 to +34.5 | +9.0 to +38.7 |
| 2023-09 -> 2026-09, theta of the start year | -1.0 | -3.6 | +13.2 | +16.5 |
| ... minus the reference | -15.6 | -10.7 | -5.0 | -5.1 |
| Zandi's prediction (reference + 12.5) | +27.1 | +19.5 | +30.7 | +34.0 |

| Three years, eta = 1, without the care lines | A nominal | A real | B nominal | B real |
|---|---|---|---|---|
| Error sd where group totals are known, all windows (non-overlapping) | 23.9 (26.2) | 11.1 (11.9) | 46.7 (73.6) | 47.8 (81.4) |
| Calm reference reading (the non-overlapping windows' readings) | +21.5 (+18.6, +36.6, +6.0) | +11.8 (+25.6, +11.8, +1.6) | +19.8 (+38.1) | +20.9 (+24.4) |
| 2023-09 -> 2026-09, theta of the start year (minus the reference) | +16.5 (-5.0) | +12.0 (+0.2) | +12.0 (-7.8) | +22.7 (+1.8) |
| Zandi's prediction | +34.0 | +24.3 | +32.3 | +33.4 |

**What the benchmarks can carry.**
- **The error sd** comes from overlapping annual windows too (A three-year: 21 windows, 7 non-overlapping; B: 9 and
  3). The non-overlapping sds are of the same size or larger. Read as a scale, it says the estimator's three-year
  errors are about Zandi's gap (A real) or several times it (A nominal, B). The power numbers rest on that scale and
  on seven (A) or three (B) independent windows.
- **The calm reference** is the estimator's ordinary reading in quiet years. A's three-year windows hold three
  non-overlapping readings that run from -0.7 to +21.7 (real), and B's hold one.
  - So no noise estimate comes from them. The first build's z-scores, minimum detectable effects and calm-based power
    ("about 2 to 4 standard deviations") are withdrawn.
  - What remains is a comparison: Zandi's split predicts the reference plus his gap. Without the care lines, the
    three-year readings sit near the reference (A +0.2, B -0.7 with the main theta, +1.8 with the start-year theta),
    11-13 points short of Zandi's prediction.
  - Errors of 11 (A) and 47 (B) points where the answer is known say that comparison is weak evidence.
- **Spread over all windows.** Over all 36-month windows since 2007 (A) and 2014 (B), which include 2008-09 and
  2020-21, the readings' standard deviation is 19.0 and 11.3 for A and 54.2 and 52.4 for B (nominal, real).
- **Two- and four-year windows** (real, without the care lines; calm windows A 8 and 72, B 4 and 24, non-overlapping
  A 4 and 2, B 2 and 1):
  - over two years A reads 1.8 points below its reference and B 4.7 above (Zandi: 8.2);
  - over four years A reads 1.4 above and B 13.5 above (Zandi: 17.0).
  - B's four-year reference rests on one independent window (+30.8). Its window starts in the reopening year, when the
    services the top buys were still recovering (B's twelve-month tilt ran at +0.4 to +2.5 points, median +1.1,
    through 2022; section 8).
  - With the 2022 theta, the start-year theta the rolling windows use, the four-year B reading is +36.3 (all
    categories +18.3).

## 7. The eta variant (Working model, TB-1929)

**What it does.** The elasticities follow TB-1929 eq. 5, eta_gq = 1 + beta_k / w_kq, where w_kq is income group q's
observed budget share of the TB-1929 stage-one group k holding category g. Food lines follow eq. 11,
eta_F,q (1 + beta*_s / w*_sq), where w*_sq is the subgroup's share of q's food spending. The betas are Table 3 (nine
groups) and Table 4 (eight food subgroups) as printed (`usda_tb1929_params.csv`; equations in `README_usda.md`).

**Budget shares** are PCE-concept: q's spending on g is theta_qg x S_g, summed over the source's categories (dPCE
totals for A, NIPA values for B, theta year). That is the same total whose growth x_q the model estimates. Engel
aggregation holds by construction: every decile's spending-weighted mean elasticity is 1 within 1e-4 (checked;
stage-one betas sum to 0, stage-two to 0.001).

**PCE lines to TB-1929 groups.** The mapping is the COICOP 1999 reading of `README_usda.md` section 8 (`USDA_MAP` in
`fingerprint.py`, each root with its reason; `fingerprint_eta.csv` lists every category's parts).
- Every B line falls in one group or food subgroup.
- A's major lines are mixtures. For example, line 12 (other nondurables) is 41% medical, 27% recreation, 13% other,
  12% furnishings and 8% tobacco. Each takes the spending-weighted mix of its parts' elasticities, with the same
  composition for every decile, which is all the dPCE allows.
- Judgment: nonalcoholic beverages go in `Food other` (TB-1929 does not say); net health insurance, child care,
  social assistance and accommodations go in `Other` (COICOP).
- The rebuild's `bridge.py` maps CE Table 1110 categories, not PCE lines, and was still being edited when this ran,
  so it is not imported. The two agree where they overlap (telephone in transport and communication, restaurants in
  `Food other`, alcohol and tobacco in `Beverages and tobacco`). They differ where `bridge.py` follows the post's
  figures (CE health insurance in medical, personal services in furnishings).

**What the elasticities look like.**
- Food is the strong necessity. Its budget share runs from 17.5% (d01) to 14.6% (d10) in B (2024), and from 19.9% to
  12.2% in A (2023). The food elasticity is 0.38 to 0.26 in B and 0.46 to 0.11 in A.
- Within food:
  - restaurants, alcohol and tobacco come out at 0.3-0.5;
  - cereals, bakery products, fish, and fats and oils come out near or below zero (E between -0.09 and +0.02 in
    B 2024).
- Outside food the elasticities run from 0.8-0.94 (education, clothing) to 1.2-1.34 (recreation, `Other`).
- The fit is g_g - pbar = x_b80 E_g + gap z_g + e_g, with no intercept, where:
  - E_g = sum_d theta_dg eta_gd is the category's elasticity, weighted by market share;
  - z_g is its top-20 part;
  - pbar is 0 for real growth. For nominal growth it is the covered categories' common price change, because the
    elasticities apply to real income, not to inflation.
- With eta = 1 this is the main fit.
- It is estimated as y = (g - pbar) / E on [1, s = z / E] with weights w E^2. That is the same least squares, so the
  permutation inversion applies with s, the top 20%'s share of the category's Engel response, permuted.
- Categories with |E| < 0.05 are left out. In B these are cereals and bakery products every year, and fish in most
  years. They carry no weight (w E^2), but s is undefined for them (-18 to +2.5 in 2014-2016 and 2020).

**What it removes** (cumulative points, real; `eta_engel_bias_uniform` in `fingerprint_read.csv` is the Engel effect
proper: what eta = 1 reads if every group's real spending rose by the window's aggregate real growth and each
category followed its elasticity, no K at all):

| Three years, 2023-09 -> 2026-09 | A, all | A, without health care | B, all | B, without care lines |
|---|---|---|---|---|
| Reading, eta = 1 | -3.6 | +12.0 | +14.6 | +20.2 |
| Reading, eta variant | -8.3 | +5.2 | +6.6 | +12.3 |
| Calm reference, eta = 1 | +7.1 | +11.8 | +21.5 | +20.9 |
| Calm reference, eta variant | +4.4 | +8.6 | +14.4 | +13.4 |
| Engel effect proper (uniform real rise of 8.6 / 7.3 / 8.2 / 6.1%) | +5.6 | +8.2 | +4.5 | +3.9 |

- The variant takes 7 points off B's calm reference reading (+21.5 to +14.4; without the care lines +20.9 to +13.4).
  So about two thirds of B's quiet-years reading survives: the luxury skew of category growth in quiet years is more
  than the Engel effects of nine broad groups and eight food subgroups.
- The variant takes 8 points off B's 2023-2026 readings and 7 off A's without health care.
- How much of that is the Engel effect proper (+4 to +8 points over three years) differs by source:
  - in A it is as large as the whole change or larger (+5.6 against 4.7; +8.2 against 6.8 without health care);
  - in B it accounts for about half (+4.5 of 8.0; +3.9 of 7.9 without the care lines). The rest comes from the low
    weight the variant gives low-elasticity lines (food, alcohol, tobacco, with E 0.1-0.5), which also discounts
    tobacco's secular decline (-25% real over the window), B's largest single contributor (section 5).
- The comparison with the reference barely moves: without the care lines, B goes from -0.7 to -1.1 points relative to
  its reference, and A from +0.2 to -3.4. Over two years the corresponding figures are B +4.7 to +5.1 and A -1.8 to
  -3.6; over four years, B +13.5 to +13.6 and A +1.4 to -3.3. Nominal results are in the file.
- In the backtests the variant does not remove the false alarms: B 2019-2021 nominal (p 0.020) and 2021-2023 (0.018
  nominal, 0.005 real) stay below 5%, and A 2007-2009 nominal falls to 0.028 (section 4).

## 8. Top-tilt index (descriptive)

**Construction.**
- tilt = real growth of the top 20%'s basket minus that of the bottom 80%'s basket. Each basket fixes the group's
  base-year budget shares (omega_qg = theta_qg S_g / sum_g theta_qg S_g) and is chained by base year: dPCE theta of the
  base year for A (frozen at 2023 afterwards), CE theta 2014-2025 for B.
- Monthly twelve-month changes run from 2007-01 for A (2006 bases from 2.4.3U quantity indexes) and from 2015-01 for
  B; annual A from 2001.
- Files: `out/top_tilt_monthly.csv`, `out/fingerprint_top_tilt_annual.csv`, `figures/fig_top_tilt.png` (NBER
  recessions and 2020 shaded).

**What it measures**: whether real spending growth comes from what the top buys or from what the bottom buys. **What
it does not measure**: group spending growth.
- A within-category K barely moves it (kappa 0.03-0.07).
- It moves with everything else that differs between the baskets: Engel effects, relative prices, supply shocks,
  quality adjustment and secular trends.
- Divided by kappa it equals the two-group slope for that twelve-month window (identity checked).

**Readings.**
- **A, annual.** The tilt index stands at 100.2 in 2025 (2000 = 100): the two baskets grew at almost the same real
  rate for 25 years. It dipped in 2008-2009 (-0.5 and -0.7 points a year) and rebounded in 2021 (+0.7).
- **What a K would add.** A Zandi-size K would add about +0.22 points a year (A weights) or +0.12 (B weights).
- **A, monthly.** The twelve-month tilt averaged -0.08 points over 2023-2026 (implied gap -1.5 points a year). The
  latest reading is -0.01 (2026-09). From 2024-01 to 2026-09 the median was -0.04 (implied -0.7; range -12 to +7).
- **B, monthly.** The twelve-month tilt averaged +0.30 points over 2023-2026 (implied +9.7 a year, inflated by
  early-2023 reopening months), against +0.15 in 2015-2019 (implied +5.3). From 2024-01 to 2026-09 its median was
  +0.22 (implied +7.2; range -2.9 to +13.1). The latest reading is +0.10 (implied +3.5, 2026-09). Through 2022 it ran
  at +0.4 to +2.5 points (median +1.1). The elder-care fix lowered B's tilt by 0.06-0.07 points a year since 2023.

## 9. Caveats

- **Care attribution.** The care lines are nearly a quarter of PCE and its fastest-growing part.
  - A attributes them to the people who receive the care. B attributes them in proportion to out-of-pocket payments.
  - Medicare- and Medicaid-financed care is government-financed consumption of the old and the poor. Employer-paid
    insurance is part of workers' compensation.
  - Neither attribution answers "whose spending is holding up demand" for these lines. With them in, the reading is a
    statement about the attribution.
- **eta.** TB-1929's elasticities come from one 2005 cross-section of 144 countries and nine broad groups.
  - At US budget shares they make food a strong necessity and some food subgroups inferior.
  - Luxuries and necessities within a group (new against used cars, restaurants against fast food) are not captured.
  - So the variant removes only the Engel effects across the broad groups and food subgroups.
- **Category noise is not exchangeable with theta.**
  - What the top buys is more cyclical (vehicles, travel, recreation). It was hit harder in 2020 and rebounded harder.
  - The placebo and the permutation intervals assume otherwise and understate the uncertainty (section 4).
- **Rankings differ.** A ranks by equivalized spending and gives third-party health care to its recipients. B ranks by
  income before taxes but gives the health lines out-of-pocket distributions near the average. They disagree most on
  health care, the line the care boom runs through.
- **Top coverage.** Both surveys put the top 20% near 39% of spending. If they compress the top's market shares
  (measured theta = c x true theta, c < 1), the slope is gap / c: a real K would be read as larger, and so would the
  noise. Compressed thetas do not create a K where category growth is unrelated to who buys.
- **Vintages and timing.**
  - dPCE thetas and totals are on the 2024-09 NIPA vintage, category growth on 2026-10.
  - CE 2025 was collected through the October-November 2025 funding lapse (weights adjusted; larger variances).
  - Monthly windows use single months at seasonally adjusted annual rates, and monthly PCE detail is BEA's
    lowest-quality detail.
- **Recession dates** (NBER: 2001-03 to 2001-11, 2007-12 to 2009-06, 2020-02 to 2020-04) are typed in for shading.

## 10. Judgment calls

1. Theta base years: A dPCE 2023 for every read window (2022 as a sensitivity for the 2022-09 window). B CE 2024 main
   (no withheld cells), 2023 and 2025 as sensitivities, 2022 for the 2022-09 window; a 2024 theta sits inside the
   2023-2025 windows.
2. Weights: base-period nominal spending (annual: base year; monthly: base month at SAAR).
3. Real growth: chained dollars where both endpoints exist, else 2.4.3U quantity indexes.
4. Zandi's split as a cumulative gap 1.04^T - 1, bottom 80% at zero, level shifted to the actual aggregate; same gap
   for nominal growth.
5. The care lines, the headline sample: definition (c) of `NOTES_sectors.md` (172, 121, 66, 275, 316, 317). B drops
   the 15 lines it has under them; A drops line 16 only.
6. Robustness drops at whole-line level in A: health = 16; imputed = 15, 20, 22 (owners' rent and FISIM cannot be
   split out); energy = 11; vehicles = 4 (parts included). B drops: everything under 172, 121, 66, 275 (health); 160
   and 163 (imputed rent; FISIM and NPISH are not covered anyway); under 113 and 169 (energy); under 5 and 12
   (vehicles).
7. B mapping (section 3):
   - each item's distribution applied to all its UCCs, except elder and adult care (340906, 340910), which take
     `Medical services`;
   - Table 2500 spending weights;
   - PCE-proportional splits;
   - the 78-UCC supplement;
   - the out-of-scope list;
   - owners' rent through the rental-equivalence addendum;
   - health lines with out-of-pocket thetas;
   - withheld cells from the all-CU identity;
   - withheld UCC means from the nearest year that publishes one, never a "no data reported" year;
   - 2023 "Other vehicles" as the residual.
8. eta variant:
   - TB-1929 Table 3 and 4 betas as printed;
   - PCE lines to groups by the COICOP 1999 reading of `README_usda.md` section 8 (nonalcoholic beverages in
     `Food other`; net health insurance, child care, social assistance and accommodations in `Other`);
   - elasticities at observed PCE-concept budget shares of the source's categories;
   - A's mixed lines by their parts' spending;
   - categories with |E| < 0.05 left out of the eta fits;
   - nominal fits net of the covered categories' common price change.
9. Inference:
   - permutation test inversion with 5,000 fresh permutations per fit;
   - ridge lambda by exact leave-one-out CV, re-chosen per replicate;
   - 500 + 500 replicates for the multi-group fits.
10. Calm periods for the reference reading: A from 2010, B from 2014, both ending by 2019-12. Non-overlapping windows
    are counted greedily from the first start.
11. B benchmark: CE Table 1110 group totals (total spending; a PCE-scope variant is in the backtest file). For real
    estimates the nominal CE gap stands in.
12. False alarm: placebo p < 0.05 in a backtest window, nominal or real. Borderline: p in 0.04-0.06.

## 11. Revision after the independent verification

`checks/verify_independent_fingerprint.py` rebuilt the unit from the raw files, with its own parsers, its own CE
mapping and 20,000 permutations of its own. It reproduced every headline of the first build and found the problems
below. This revision handles them as follows.

1. **The calm-period "norm" came from heavily overlapping windows.** A's 84 three-year windows hold 3
   non-overlapping ones (+21.7, +4.0, -0.7 points); B's hold 1. It is now a reference reading. The z-scores, minimum
   detectable effects and calm-based power ("about 2 to 4 standard deviations") are withdrawn. The non-overlapping
   windows' readings are listed, and the error-sd benchmark now carries its own count of non-overlapping windows
   (sections 2 and 6).
2. **The care lines steer both sources in opposite directions, and B's home health care carried a child-care
   distribution.**
   - "Without the care lines" is now a headline sample, with matching reference readings, for both sources.
   - The elder- and adult-care UCCs take the `Medical services` distribution (section 3). B's three-year real reading
     falls from +20.0 to +14.6 (nominal +13.5 to +7.7). The first build's mapping is kept as a sensitivity.
   - Net health insurance (out-of-scope premium UCCs in its item) and prescription drugs (out-of-pocket
     distribution) are flagged.
   - A's evidence against Zandi rested on the health-care line: without it A reads +12.0, about Zandi's +12.5, and
     its calm reference +11.8.
3. **The Working-model eta variant had not been run** although `usda_tb1929_params.csv` exists. It now runs for both
   sources, every window, both samples, the backtests and the reference readings (section 7).
4. **False alarms, borderline cases and permutation draws.**
   - False alarms are now counted across nominal and real. B: 2 of 7 windows at 5%, 4 at 10%, against "two of
     seven" on one measure in the first build. The 2022-2025 real reading, which overlaps the read period, is
     reported.
   - A 2007-2009 is marked borderline.
   - Permutations are drawn fresh for every fit (5,000 instead of one reused set of 1,000).
5. **Minor corrections.**
   - CE's top-quintile range is 37.3-38.9% (38.45-38.88% without 2020).
   - The 133-line scatter is 8.7 points real and 8.0 nominal, not 8.5.
   - Stand-ins for withheld UCC means skip years that code the UCC "no data reported".
   - The 2023 "Other vehicles" residual rule is documented (section 3).
   - The code header's kappa now reads 0.047-0.066 at the 16-line level, with a shrink factor of 18 to 34.
   - The A ridge lambda label reads 5.6e-5, not 1e-4.
   - The dPCE's own backtest gap tops out at +3.0, not +3.1.
6. **The plain-words answer** is rewritten. It now says what the composition can and cannot show about a K once
   the care lines are handled, and how it sits beside the direct survey evidence.

The verifier's script compares many claims with the numbers the first build's notes quoted, so a rerun flags every
number this revision changed on purpose: B's readings, p-values, R^2 and top tilt after the elder-care fix, and B's
2022-2025 and 2023-2025 backtests. It also keeps a few fixed verdicts on statements this revision withdraws or
corrects: fewer than five independent calm windows, the eta file exists, the old code comment and the notes' wording.
The rerun of 2026-11-02 printed 407 claims, 358 OK and 49 BAD; every BAD is one of these two kinds or a first-build
number the notes now correct (line 54's residual rule is documented, not changed).

## Files

| File | What |
|---|---|
| `code/fingerprint.py` | Everything: thetas, mapping, elasticities, backtest, read, influence, benchmarks, top tilt, charts (about 11 minutes; `# %%` cells). |
| `checks/check_fingerprint.py` | Independent re-implementations and identities (own permutations, own eta recomputation, own reference readings); PASS/FAIL per check (79 PASS, 2 INFO). |
| `checks/verify_independent_fingerprint.py` | The independent re-derivation (not edited by this revision; see section 11). |
| `out/fingerprint_theta_A.csv` | dPCE thetas, 16 lines x 2000-2023: deciles and every group, base spending (dPCE vintage and current NIPA). |
| `out/fingerprint_theta_B.csv` | CE-mapped thetas, 132-133 PCE lines x 2014-2025, with the feeding items, the items whose distributions they take (`theta_items`) and the rule-1-only top-20 share (`theta_top20_rule1`). |
| `out/fingerprint_mapping_B.csv` | Year x line item x UCC x PCE target: item rule, source (BLS map, supplement, out of scope, unmapped), UCC mean and the year and code it came from, weight, theta item, rule, reason. |
| `out/fingerprint_coverage_B.csv` | Coverage of PCE and of CE spending by year; PCE lines with no CE counterpart; the `Health insurance` item's out-of-scope share; CE's top-20 share of spending. |
| `out/fingerprint_eta.csv` | Working-model elasticities by source x theta year x category and decile, each category's TB-1929 parts, E, z and the marginal top-20 share; group budget shares and food subgroup shares. |
| `out/fingerprint_backtest.csv` | A against dPCE group totals; B against CE group totals; eta = 1 and the eta variant; false-alarm and borderline flags. |
| `out/fingerprint_false_alarms.csv` | False alarms counted by source x spec x measure (nominal, real, either). |
| `out/fingerprint_read.csv` | Window x source x theta year x spec x sample x measure: gap, intervals, p-values, fit against Zandi and flat, benchmarks (error band; calm reference, its non-overlapping windows, gap - reference, Zandi's prediction), eta diagnostics, permutation seed. |
| `out/fingerprint_read_categories.csv` | Category-level data behind the scatter. |
| `out/fingerprint_influence.csv` | Each category's contribution to the slope and the gap without it. |
| `out/fingerprint_power.csv` | Rolling windows (A annual against dPCE, B annual against CE, 36- and 48-month) for both samples and both eta settings, and their summaries (error sd with non-overlapping counts; reference readings). |
| `out/top_tilt_monthly.csv`, `out/fingerprint_top_tilt_annual.csv` | Top-tilt index. |
| `figures/fig_fingerprint_scatter.png`, `fig_fingerprint_backtest.png`, `fig_top_tilt.png` | Charts (200 dpi). The scatter marks the care lines and draws the fit with and without them; the backtest labels every p below 0.06. |

Raw files added through `common.fetch` (rows in `raw/bls_ce/MANIFEST.csv`):
- `raw/bls_ce/stubs/pumd_doc.htm`;
- `raw/bls_ce/stubs/stubs.zip` (hierarchical groupings 1996-2025);
- `raw/bls_ce/tables/detail/cu-all-detail-2014..2025.xlsx` (Table 2500).

The eta variant reads `data/tidy/usda_tb1929_params.csv` (built by `code/acquire_usda.py`).
