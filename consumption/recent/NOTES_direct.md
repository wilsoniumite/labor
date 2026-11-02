# Direct reads: what the official distributions say about who is doing the spending

Question 2 of the consumption thread, direct-reads unit (Stella's 2026-06-14 post: "If consumption is being held up
by higher incomes or some sectors, perhaps one could see that in spending patterns?"). The sector angle is
`NOTES_sectors.md`, the category-composition test `NOTES_fingerprint.md`. This unit reads the distributions
themselves: who spends, who earns, who saves, who holds the equity, and what families say they would do with extra
money.

Built 2026-11-02 by `code/direct.py`; checks in `checks/check_direct.py`. Corrected the same day after an
independent re-derivation (`checks/verify_independent_direct.py`); the last section lists what changed. Run from the
repo root:

    venv/bin/python -I consumption/recent/code/direct.py           # about 15 s: out/direct_*.csv, figures/fig_direct_*.png
    venv/bin/python -I consumption/recent/checks/check_direct.py   # about 5 s: 76 PASS/FAIL lines

Data, all vendored (`consumption/data/tidy/`, see `README_bls_ce.md`, `README_bea.md`, `README_fed.md`):

- BLS Consumer Expenditure Surveys: Tables 1110 (deciles, 2014-2025) and 1101 (quintiles, 2019-2025) of income
  before taxes; 2025 released 2026-10-29.
- BLS distributional PCE, March 2025 results (2000-2023, NIPA vintage of 2024-09).
- BEA: the joint distribution of DPI, PCE and saving (BEA-BLS, 2000-2023, workbook of 2026-05); the distribution of
  personal income, disposable income and taxes (June 2026: 2000-2023 final, 2024 provisional, and a 2025
  experimental nowcast of personal income only); the income-stratified PCE price index ISPCEPX (2000-2024); NIPA
  Tables 2.1 and 2.6 of 2026-10-29 (monthly to 2026-09).
- Federal Reserve: SCF 2025 and 2022 summary extracts (2025 dollars), the Distributional Financial Accounts of
  2026-09-18 (1989Q3-2026Q2), the Z.1 of 2026-09-11.
- The post's own parameters as transcribed in `post_published_numbers.csv` (`README_post.md`).
- Two pages added through `common.fetch()` for this unit (rows in `raw/fed/MANIFEST.csv`, folder
  `raw/fed/feds_notes/`): the Board's FEDS Note "Heterogeneity in the Marginal Propensity to Consume among U.S.
  Households" (2026-10-09) and its accessible version with the figure data. They are the publisher's own analysis
  of the SCF windfall question, used to check the tabulation in section 5.

## The answer in brief

1. **The official spending distributions show no K after 2022, and most of them stop before Zandi's window
   starts.** The CE is the only one that reaches 2025. The top fifth's share of CE spending (ranked by income before
   taxes) was 38.5% in 2022 and 38.9% in 2025. Zandi's split (top 20% +4% a year in real terms, bottom 80% flat)
   would have lifted it to 41.5% by 2025, about four standard errors of the change above what the survey shows
   (three from the 2023 base). The BLS distributional PCE and the BEA-BLS joint distribution end in 2023. Both put
   the top's share slightly lower in 2023 than in 2022.
2. **In real terms, CE spending of the top fifth grew 6.3% from 2022 to 2025 and that of the bottom 80% 5.3%.**
   That is a gap of +1.0 point (approximate SE 2.8) against Zandi's +12.5. It is +2.5 points if pensions, Social
   Security and cash contributions are left out. From 2023 to 2025 the gap is -0.2 (Zandi: +8.2). The top tenth
   against the bottom 90% gives +3.8 points (SE 4.1) for 2022-2025: the right sign, but not large or significant.
   The latest year on its own fits both stories: from 2024 to 2025 the gap is +1.9 points (SE 2.7) against Zandi's
   +4.0. The case against his split therefore rests on the multi-year windows, and the equity run-up was fastest
   after the CE window closed: household equity holdings rose $8.8tn in the first half of 2026, more than in all of
   2024 ($7.6tn) or 2025 ($8.5tn). Zandi's own numbers do not quite add up either. With the top fifth at
   38.9-42.8% of spending, +4% and 0% average 1.6-1.7% a year, not the 2% he quotes. The CE's aggregate did grow
   1.9% a year in real terms from 2022 to 2025, matching his 2%, but with the bottom 80% at about 1.7% a year, not
   close to zero.
3. **On income, the answer depends on the concept: no K before taxes, a one-off tilt to the top after taxes.**
   Pre-tax personal income (which includes in-kind Medicare and Medicaid; households ranked by equivalized personal
   income) shows no K: the bottom 80%'s real income grew 8.7% from 2022 to 2025 and the top 20%'s 7.3%. The 2025
   part is an experimental nowcast: nominal +5.2% against +4.6%. Disposable income, which is what spending is paid
   from, did tilt to the top. Ranked by equivalized DPI, the top fifth's real DPI grew 10.2% from 2022 to 2024 and
   the bottom 80%'s 7.7% (BEA's DPI distribution ends in 2024). All of the difference came in 2023, when taxes fell
   back from a 2022 peak that weighed most on the top: taxes took 20.9% of the top fifth's personal income in 2022
   and 17.2% in 2023 and 2024 (bottom 80%: 7.7%, 6.3% and 6.1%). From 2023 to 2024 the two grew alike (+2.9%
   against +3.1%). So "no K on the income side" holds only before taxes. After taxes the top gained 2.5 points on
   the rest, once, about a third of the two-year gap Zandi gives for spending. In the CE the top fifth's spending
   outgrew the bottom 80%'s by 1.2 points in 2023 (SE 2.7).
4. **The wealth side does have one.** The top 20% by income received 88% of the $32.9tn rise in household equity
   holdings from 2022Q3 to 2026Q2 (DFA; model-based after 2022Q3, and in line with SCF 2025 for the top fifth). Take
   the post's wealth effect as given: 2-5 cents per dollar per year in its footnote 31 and Figure 0 (its body text
   says three to five cents, and Figures 8-10 use 3.5). With SCF 2025 spending shares as denominators, the equity
   revaluation gains would lift the top fifth's spending 3-8% relative to the bottom 80% by mid-2025 and 5-13% by
   mid-2026. With the BEA-BLS joint distribution's spending shares, which put less of spending at the top, it is
   4-10% and 7-17%. At the high end that is Zandi's size. This is arithmetic on an assumption, not a measurement,
   and the CE does not show it.
5. **What could reconcile the two is the very top, which the CE barely sees.** Suppose the CE missed the top 1%
   entirely. For Zandi's top-20% gap to hold, that group's spending would have had to grow about 80 points more
   than the bottom 80%'s over 2022-2025. The assumed wealth effect gives it 12-29 points. This needs the same
   spending shares on both sides: with the BEA-BLS shares for both, the need is 187 points against 35-87, while
   mixing them (the SCF-weighted need of 80 against the BEA-BLS bound of 87 at 5 cents) would reverse it. If the CE
   missed the top 5%, the needed gap is 28 points. A K confined to the top few percent is possible and would be
   invisible in the CE. A K of Zandi's size across the whole top fifth is not what the official data show.
6. **Saving: the top did not save less by 2023. After that only the total is known.** In the joint distribution
   the top decile saved 46.6% of its DPI in 2023, against 45.6% in 2019. The bottom 80% spent further above their
   income by 2022 (a saving rate of -24.5%, against -19.2% in 2019), and slightly less so in 2023 (-23.1%). Both
   series end in 2023, before the years Zandi describes, so neither tests his saving story. The aggregate saving
   rate then fell from 6.2% (2023-24) to 3.8% (Sep 2026). From March to September 2026 the fall in saving financed
   40% of the rise in spending. Both of Zandi's stories fit that, and no distribution yet says which it is: the rich
   saving less because their wealth grew, and the lower-middle drawing down. The fall is about what a 2-cent wealth
   effect on the gains since 2023-24 would give (1.8 points of DPI). It is less than the post's central 3.5 cents
   implies (3.2 points).
7. **The SCF's new windfall question bears on the ordering of the post's MPC gradient.** A bottom-decile family
   would spend 29% of a windfall of one month's income, a top-decile family 18-20%, the top 1% 14-18%. That is a
   top-to-bottom ratio of 0.62-0.69 (95% family bootstrap 0.51-0.83), against the post's assumed 0.40-0.65: at the
   flat end of the post's range for the top decile, and inside it for the top 1%. The question is a stated share of
   a one-off windfall sized at a month's income, while the post's MPC is for a permanent flow. So the SCF supports
   the ordering (lower-income families spend more of a windfall), says little about the slope and nothing about
   the level.
8. **Moody's numbers are not used.** The widely reported Moody's estimate puts the top decile near half of spending
   (about 49% in 2025). It is not public data: the method and the underlying distribution are not published, so it
   cannot be checked or put on a common footing. The official top-decile shares run from 20% to 28%, depending on
   ranking and scope (section 1).

## 1. Top shares over time, every official source on one footing

`out/direct_top_shares.csv` and `figures/fig_direct_top_shares.png`. All shares are of the source's own spending
total, in %. CE shares are CU count x mean over the groups; the published aggregate-share table agrees within 0.08
point (check A2). The SCF-like-scope variant divides by the all-CU count x mean instead, which avoids the suppressed
2022-23 cells; the two denominators differ by at most 0.015 point. The approximate SE of a CE share treats the group
means as independent samples, using BLS's published BRR standard errors (Fay's BRR in 2025).

| Source and group | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 | Change 2022 to last, pts | Approx. SE of the change, pts |
|---|---|---|---|---|---|---|---|---|---|
| CE, income before taxes: top 10% | 23.4 | 22.3 | 23.4 | 22.9 | 23.5 | 22.9 | 23.6 | +0.8 | 0.68 |
| CE, income before taxes: top 20% | 38.7 | 37.3 | 38.5 | 38.5 | 38.9 | 38.5 | 38.9 | +0.3 | 0.63 |
| CE, excl. pensions, Social Security, contributions: top 20% | 36.1 | 34.7 | 35.5 | 35.7 | 36.1 | 35.7 | 36.3 | +0.7 |  |
| CE, SCF-like scope: top 10% | 21.8 | 20.4 | 21.7 | 21.0 | 22.0 | 21.5 | 22.3 | +1.3 |  |
| CE, SCF-like scope: top 20% | 36.7 | 35.3 | 36.4 | 36.4 | 37.1 | 36.7 | 37.3 | +0.9 |  |
| BLS dPCE, equivalized spending: top 10% | 26.1 | 25.0 | 26.1 | 26.4 | 25.7 |  |  | -0.6 |  |
| BLS dPCE, equivalized spending: top 20% | 39.8 | 38.3 | 39.7 | 40.0 | 39.5 |  |  | -0.5 |  |
| BLS dPCE, equivalized spending: top 1% | 6.9 | 6.5 | 6.8 | 7.5 | 6.6 |  |  | -0.9 |  |
| BEA-BLS joint, equivalized DPI: top 10% | 20.6 | 19.6 | 19.3 | 20.4 | 20.2 |  |  | -0.2 |  |
| BEA-BLS joint, equivalized DPI: top 20% | 34.3 | 32.8 | 32.8 | 34.1 | 33.9 |  |  | -0.2 |  |
| BEA-BLS joint, equivalized DPI: top 1% | 2.4 | 2.4 | 2.1 | 2.3 | 2.1 |  |  | -0.2 |  |
| SCF 2025 non-housing, income 2024: top 10% |  |  |  |  |  |  | 28.3 |  |  |
| SCF 2025 non-housing, income 2024: top 20% |  |  |  |  |  |  | 42.8 |  |  |
| SCF 2025 non-housing, income 2024: top 1% |  |  |  |  |  |  | 6.3 |  |  |
| SCF 2025 non-housing, usual income: top 10% (Bulletin 28.5) |  |  |  |  |  |  | 28.4 |  |  |

How the four are built:

| Source | Ranking | Equivalized | Unit | Scope | Top tail |
|---|---|---|---|---|---|
| CE (BLS) | income before taxes (money income, past 12 months) | no | consumer unit (CU), CU-weighted groups | CE out-of-pocket expenditures incl. personal insurance and pensions and cash contributions; employer- and government-paid health care, imputed rent and FISIM not included | survey as collected; under-covers the very top (no oversample, top-coding, nonresponse rising with income) |
| BLS dPCE | total PCE per CU / sqrt(CU size) (spending, not income) | yes | CU, CU-weighted deciles (finlwt21) | all of PCE (national accounts), CE-allocated with imputations for out-of-scope items (third-party health care, FISIM, imputed rent) | Pareto adjustment of the top 5% of spenders |
| BEA-BLS joint | disposable personal income per household / sqrt(size) (CPS-based) | yes | household (CPS), household-weighted deciles | all of PCE, allocated by BLS CE-based shares matched to BEA's DPI distribution | DPI top tail from BEA's income distribution (tax-data adjusted); PCE side from the CE (BLS dPCE methods) |
| SCF 2025 (Fed) | family income in 2024 (INCOME), or usual income (NORMINC) | no | family (primary economic unit), WGT over all implicates | total non-housing spending over the past 12 months as reported (excludes rent, mortgage and loan payments, investments, retirement contributions) | list-sample oversample of wealthy families (Forbes 400 excluded); one question on total spending |

**Why the levels differ.**

- **Ranking variable.** Ranking by spending (dPCE) puts the biggest spenders at the top by construction. Its top
  fifth has 39.5% of PCE (2023). Ranking the same PCE by disposable income (joint distribution) gives the top fifth
  only 33.9%: high spenders with modest income, such as retirees drawing down assets, move down.
- **Equivalization.** dPCE and the joint distribution divide by the square root of household size. CE and SCF do
  not, so larger households, which spend more, sit higher in the CE and SCF rankings.
- **Scope.** PCE includes employer- and government-paid health care, imputed rent, financial services furnished
  without payment and nonprofits. These are spread more evenly than out-of-pocket spending, and Medicare- and
  Medicaid-financed care leans to the bottom. CE expenditures include personal insurance and pensions (mostly Social
  Security and pension contributions; in 2025 the top quintile accounts for 55.5% of it) and cash contributions.
  Leaving those out lowers the CE top fifth from 38.9% to 36.3%. The SCF question leaves out housing payments,
  loan payments and retirement contributions.
- **Top tail.** The dPCE Pareto-adjusts the top 5% of spenders. In 2019 that adjustment supplies 9% of the top
  spending decile's PCE (BLS methods page, Figure 3.1). The SCF oversamples wealthy families. The joint
  distribution's PCE side is CE-based, so it gives the top 1% by DPI only 2.1% of PCE. The dPCE gives the top 1% of
  spenders 6.6%, and the SCF gives the top 1% by income 6.3% of non-housing spending.

The SCF puts more of spending at the top than the CE does, even on a comparable scope:

| Measure (2025) | Aggregate, $tn | Top 10%, % | Top 20%, % |
|---|---|---|---|
| CE average annual expenditures (all CUs) | 11.30 | 23.6 | 38.9 |
| CE, SCF-like scope (minus owned and rented dwellings, pensions and insurance, cash contributions) | 7.35 | 22.3 | 37.3 |
| SCF 2025 total non-housing spending (income 2024 ranking) | 6.57 | 28.3 | 42.8 |
| PCE (NIPA Table 2.1, calendar 2025) | 20.87 |  |  |

On a scope close to the SCF question the CE's top tenth falls slightly (23.6% to 22.3%). The SCF's 28.3% is
therefore not a scope effect. The SCF reaches the top better (list sample), and its single recall question records
less spending in total than the CE's detailed interview ($6.6tn against $7.4tn), so less of it sits at the bottom.
Which effect dominates cannot be separated here. The PCE row is calendar 2025 (NIPA Table 2.1, $20.87tn), the same
figure the evidence table quotes in section 6.

**What the trends say about 2019-2025.** All three time series have the same shape: a dip in 2020, when the
services the top buys were shut, a recovery by 2021-2022, and no rise after.

- **CE, the only series through 2025.** The top fifth's share sits at 38.5-38.9% in 2021-2025. It was 38.7% in
  2019 and 38.8-39.6% in 2014-2018 (from deciles). The change from 2022 to 2025 is +0.3 point (SE 0.6), against the
  3.0 points Zandi's split would add. The top tenth moves in a saw-tooth (22.9, 23.5, 22.9, 23.6) with no trend.
- **dPCE.** The top fifth's share was 39.8% (2019), 40.0% (2022) and 39.5% (2023). The top 1% was 7.5% in 2022 and
  6.6% in 2023.
- **Joint distribution.** The top fifth by DPI was 34.3% (2019), 34.1% (2022) and 33.9% (2023).
- **SCF.** One cross-section, the first time the question was asked, so it has no trend to read.

## 2. CE 2019-2025 by quintile and decile

`out/direct_ce_groups.csv` (blocks `levels`, `growth`, `gap_top_vs_rest`, `zandi_implied_share`,
`zandi_arithmetic`, `composition`). Means are per consumer unit and per year, in current dollars. Aggregates are
means times CU counts.

**Deflation.** Real values are in 2024 dollars. Each CE group is deflated by the ISPCEPX index of the same rank
(quintile or decile of equivalized DPI), a different ranking from the CE's income before taxes. ISPCEPX is a
PCE-scope deflator: each group's index weights its own PCE basket over about 150 categories, including employer-
and government-paid health care and imputed rent, not the CE's out-of-pocket basket. Its 2024 weights are imputed
(each group's 2023 category shares applied to the 2024 category totals; flagged in the tidy file, check A6).
ISPCEPX ends in 2024. For 2025 every group's index is carried forward by the aggregate PCE price index from the
current vintage (+2.59% from 2024 to 2025), so no differential inflation is assumed for 2025. Over 2019-2024 the top
quintile's index rose 19.9% and the others 19.1-19.5%: a differential of about 0.1 point a year, too small to
matter here.

| Group | 2019 nominal $ | 2022 nominal $ | 2023 nominal $ | 2024 nominal $ | 2025 nominal $ | 2025 real (2024 $) | Real mean 2022-2025, % | Real aggregate 2022-2025, % | Real mean 2023-2025, % | Real aggregate 2023-2025, % | Real agg. 2022-2025 excl. pensions/contrib., % |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Q1 | 28,672 | 32,612 | 33,776 | 35,046 | 37,935 | 36,977 | 6.5 | 10.1 | 6.8 | 11.0 | 9.8 |
| Q2 | 40,472 | 47,657 | 48,923 | 50,054 | 51,405 | 50,107 | -1.2 | 1.5 | -0.1 | 2.0 | 2.9 |
| Q3 | 53,045 | 61,950 | 65,487 | 66,900 | 68,983 | 67,241 | 2.1 | 6.2 | 0.2 | 2.9 | 5.6 |
| Q4 | 71,173 | 81,957 | 87,922 | 89,972 | 92,250 | 89,920 | 3.2 | 5.0 | -0.2 | 1.5 | 5.3 |
| Q5 (top 20%) | 121,571 | 140,654 | 150,093 | 150,342 | 159,512 | 155,484 | 3.4 | 6.3 | 0.7 | 3.1 | 8.1 |
| Bottom 80% | 48,350 | 56,045 | 59,070 | 60,496 | 62,555 | 60,975 | 2.3 | 5.3 | 0.7 | 3.3 | 5.6 |
| All CUs | 63,036 | 72,967 | 77,280 | 78,535 | 81,905 | 79,836 | 2.7 | 5.7 | 0.7 | 3.2 | 6.5 |

Deciles (aggregates). The approximate SEs treat groups and years as independent. For real growth, each end's
relative SE comes from the deflated aggregate and is scaled by the real growth factor:

| Decile | 2022 nominal $ | 2025 nominal $ | Real mean 2022-2025, % | Real aggregate 2022-2025, % | approx. SE 2022-2025 | Real mean 2023-2025, % | Real aggregate 2023-2025, % | approx. SE 2023-2025 |
|---|---|---|---|---|---|---|---|---|
| D01 | 31,039 | 35,986 | 6.1 | 9.4 | 5.8 | 7.3 | 12.5 | 6.2 |
| D02 | 34,192 | 39,875 | 6.8 | 10.7 | 3.9 | 6.5 | 9.6 | 3.8 |
| D03 | 44,698 | 46,003 | -5.7 | -2.4 | 6.6 | -4.4 | -3.1 | 3.7 |
| D04 | 50,578 | 56,794 | 2.9 | 4.7 | 3.3 | 3.5 | 6.5 | 3.5 |
| D05 | 57,057 | 65,312 | 4.9 | 9.0 | 3.4 | 1.9 | 4.4 | 3.4 |
| D06 | 66,831 | 72,639 | -0.3 | 3.8 | 3.1 | -1.4 | 1.7 | 3.0 |
| D07 | 76,275 | 86,767 | 4.4 | 5.3 | 3.7 | 2.9 | 4.4 | 3.6 |
| D08 | 87,675 | 97,689 | 2.1 | 4.7 | 2.9 | -2.8 | -1.0 | 2.7 |
| D09 | 114,182 | 125,226 | 0.4 | 2.9 | 3.1 | -0.2 | 2.1 | 3.2 |
| D10 | 167,200 | 193,649 | 5.4 | 8.6 | 3.9 | 1.4 | 3.7 | 3.8 |
| Top 10% | 167,200 | 193,649 | 5.4 | 8.6 | 3.9 | 1.4 | 3.7 | 3.8 |
| Bottom 90% | 62,512 | 69,494 | 1.9 | 4.8 | 1.3 | 0.5 | 3.1 | 1.2 |

**Top against the rest.** Gaps are in real aggregate growth, in cumulative points. Zandi's gap is 1.04^T - 1.

| Groups | Window | Top real % | Rest real % | Gap, pts | Approx. SE, pts | Gap excl. pensions/contrib., pts | Zandi's gap, pts |
|---|---|---|---|---|---|---|---|
| top20 vs bottom80 | 2019-2025 | 10.7 | 10.5 | +0.2 | 2.7 | +0.3 | 26.5 |
| top20 vs bottom80 | 2019-2022 | 4.2 | 4.9 | -0.8 | 2.6 | -2.1 | 12.5 |
| top20 vs bottom80 | 2022-2025 | 6.3 | 5.3 | +1.0 | 2.8 | +2.5 | 12.5 |
| top20 vs bottom80 | 2022-2023 | 3.1 | 1.9 | +1.2 | 2.7 | +1.9 | 4.0 |
| top20 vs bottom80 | 2023-2025 | 3.1 | 3.3 | -0.2 | 2.7 | +0.6 | 8.2 |
| top20 vs bottom80 | 2024-2025 | 4.5 | 2.6 | +1.9 | 2.7 | +3.0 | 4.0 |
| top10 vs bottom90 | 2019-2025 | 11.1 | 10.4 | +0.6 | 3.9 | +0.7 | 26.5 |
| top10 vs bottom90 | 2022-2025 | 8.6 | 4.8 | +3.8 | 4.1 | +6.1 | 12.5 |
| top10 vs bottom90 | 2023-2025 | 3.7 | 3.1 | +0.6 | 4.0 | +0.6 | 8.2 |

**The latest year alone fits both stories.** From 2024 to 2025 the top fifth's real spending grew 4.5% and the
bottom 80%'s 2.6%: a gap of +1.9 points (SE 2.7), as close to Zandi's +4.0 as to none. The multi-year windows are
what rule out his split: over 2022-2025 his +12.5 is about four SEs from the CE's +1.0, and over 2023-2025 his +8.2
is three SEs from -0.2. The equity run-up was fastest after the CE window closed (section 4). In 2023 alone, the
year the top fifth's disposable income pulled ahead (section 3), the CE gap is +1.2 (SE 2.7).

**Zandi's own arithmetic.** His split averages 4% times the top fifth's share of spending, so his 2% needs a top
fifth with half of spending:

| Item | Top-20 share, % | % a year |
|---|---|---|
| Zandi's split (top 20% +4%, bottom 80% 0%) averaged with the CE 2025 top-20 share | 38.9 | 1.6 |
| Zandi's split (top 20% +4%, bottom 80% 0%) averaged with the BLS dPCE 2023 top-20 share | 39.5 | 1.6 |
| Zandi's split (top 20% +4%, bottom 80% 0%) averaged with the SCF 2025 top-20 share | 42.8 | 1.7 |
| Top-20 share at which his split averages his 2% | 50.0 | 2.0 |
| CE real aggregate spending 2022-2025, all CUs, a year |  | 1.9 |
| CE real aggregate spending 2022-2025, top 20%, a year |  | 2.1 |
| CE real aggregate spending 2022-2025, bottom 80%, a year |  | 1.7 |

On the official shares his +4% and 0% give 1.6-1.7% a year, not 2%. The CE's aggregate did grow at about his 2%
(1.9% a year from 2022 to 2025), but its bottom 80% grew about 1.7% a year, not close to zero.

**Zandi's split implies a top-quintile share of 41.5% by 2025** if it starts from the 2022 share, and 40.8% if it
starts from 2023. The observed share is 38.9%: 4.2 and 3.1 standard errors of the change below his. The nominal
version adds each side's own ISPCEPX inflation.

| Base year | Top-20% share in base year, % | Zandi's split, 2025 (real), % | Zandi's split, 2025 (nominal), % | Observed 2025, % | Zandi minus observed, pts | Approx. SE of the change, pts | Zandi minus observed, SEs | Same, excl. pensions/contrib.: Zandi / observed, % |
|---|---|---|---|---|---|---|---|---|
| 2022 | 38.5 | 41.4 | 41.5 | 38.9 | 2.6 | 0.63 | 4.2 | 38.5 / 36.3 |
| 2023 | 38.9 | 40.7 | 40.8 | 38.9 | 1.9 | 0.63 | 3.1 | 38.0 / 36.3 |

**Budget composition, 2022 to 2025** (shares of each group's own total, in %; growth is nominal). Suppressed cells
are filled from the all-CU identity N_all m_all = sum N_g m_g. Two cells need it: drugs for Q3 and cash
contributions for Q2, both in 2022 and both in the bottom 80%. The 28 items add to the published totals within $4.

| Item | Q1 share 2022, % | Q1 2025, % | Q1 change, pts | Q1 growth, % | Q5 share 2022, % | Q5 2025, % | Q5 change, pts | Q5 growth, % |
|---|---|---|---|---|---|---|---|---|
| Food at home | 11.1 | 9.5 | -1.62 | -1 | 6.1 | 6.5 | +0.40 | +21 |
| Food away from home | 4.5 | 4.1 | -0.39 | +6 | 5.1 | 5.1 | -0.03 | +13 |
| Alcoholic beverages | 0.7 | 0.6 | -0.14 | -7 | 0.9 | 0.9 | +0.06 | +22 |
| Owned dwellings (mortgage interest, property taxes, upkeep) | 8.4 | 10.0 | +1.61 | +39 | 13.0 | 13.9 | +0.93 | +22 |
| Rented dwellings | 15.5 | 16.6 | +1.09 | +24 | 2.6 | 3.1 | +0.50 | +35 |
| Other lodging (incl. vacation homes, hotels) | 1.2 | 0.7 | -0.52 | -34 | 2.5 | 2.4 | -0.11 | +8 |
| Utilities, fuels, public services | 8.7 | 8.3 | -0.47 | +10 | 4.6 | 4.3 | -0.31 | +6 |
| Household operations | 2.4 | 2.8 | +0.41 | +36 | 2.8 | 2.7 | -0.07 | +10 |
| Housekeeping supplies | 1.5 | 1.3 | -0.21 | +0 | 0.9 | 0.9 | -0.00 | +13 |
| Household furnishings and equipment | 3.2 | 2.9 | -0.26 | +7 | 3.8 | 3.1 | -0.76 | -9 |
| Apparel and services | 2.8 | 2.2 | -0.60 | -9 | 2.6 | 2.7 | +0.10 | +18 |
| Vehicle purchases (net outlay) | 4.3 | 5.3 | +0.97 | +42 | 6.9 | 6.4 | -0.48 | +5 |
| Gasoline and other fuels | 4.8 | 3.3 | -1.48 | -20 | 3.3 | 2.3 | -0.98 | -21 |
| Other vehicle expenses | 5.2 | 5.4 | +0.22 | +21 | 4.6 | 5.2 | +0.57 | +27 |
| Public and other transportation | 0.8 | 1.3 | +0.48 | +85 | 1.5 | 1.9 | +0.40 | +43 |
| Health insurance | 6.9 | 6.9 | -0.05 | +15 | 4.0 | 4.0 | -0.07 | +11 |
| Medical services | 2.0 | 2.1 | +0.09 | +21 | 1.5 | 1.4 | -0.07 | +8 |
| Drugs | 1.0 | 1.1 | +0.05 | +22 | 0.6 | 0.7 | +0.10 | +34 |
| Medical supplies | 0.3 | 0.4 | +0.04 | +32 | 0.2 | 0.2 | -0.02 | +5 |
| Entertainment | 3.8 | 4.3 | +0.53 | +33 | 5.3 | 5.8 | +0.57 | +26 |
| Personal care | 1.2 | 1.1 | -0.11 | +5 | 1.1 | 1.2 | +0.14 | +28 |
| Reading | 0.2 | 0.1 | -0.13 | -54 | 0.2 | 0.2 | +0.00 | +14 |
| Education | 2.0 | 2.1 | +0.14 | +25 | 2.6 | 3.0 | +0.40 | +31 |
| Tobacco | 1.1 | 0.8 | -0.33 | -17 | 0.2 | 0.2 | -0.04 | -11 |
| Miscellaneous | 1.5 | 2.0 | +0.45 | +50 | 1.3 | 1.4 | +0.09 | +21 |
| Cash contributions | 2.7 | 2.9 | +0.22 | +26 | 4.6 | 3.0 | -1.58 | -26 |
| Life and other personal insurance | 0.6 | 0.5 | -0.11 | -7 | 0.9 | 0.8 | -0.02 | +11 |
| Pensions and Social Security | 1.4 | 1.5 | +0.15 | +29 | 16.6 | 16.9 | +0.29 | +15 |
| Total (sum of items) | 100.0 | 100.0 | +0.00 | +16 | 100.0 | 100.0 | +0.00 | +13 |

Both ends spent more of their budget on shelter: owned dwellings (mortgage interest, property taxes, upkeep) and
rent. Both spent less on gasoline, as pump prices fell from their 2022 peak, and more on entertainment and on
public and other transport, which includes airfares.

- **Top quintile, the main shifts:**
  - cash contributions fell from 4.6% to 3.0% of the budget (-26% in dollars);
  - furnishings fell and vehicle purchases slipped;
  - food at home, other vehicle expenses (insurance and maintenance) and education rose.
- **Bottom quintile:**
  - food at home fell from 11.1% to 9.5% (-1% in dollars over three years in which food prices rose);
  - vehicle purchases and household operations rose.

Nothing in the top quintile's mix looks like a spending boom in discretionary goods. Its biggest gains are in
shelter costs and insurance-type spending. Its two big discretionary lines gained about as much budget share as the
bottom quintile's did: entertainment +0.57 points against +0.53, public and other transport +0.40 against +0.48.
Its travel lodging (other lodging) slipped by 0.11 point.

**How fast would a top group the CE misses have to grow?** This is arithmetic, not data. The top-20% gap is
[S_h (g_h - g_b80) + (S20 - S_h) gap_seen] / S20. The S are SCF 2025 shares of non-housing spending; gap_seen is
the CE's top-quintile gap, standing in for the rest of the top fifth.

| Group the CE misses | Its share of spending (SCF 2025), % | CE gap for the rest of the top 20%, pts | CE concept | Gap that group needs over 2022-2025, pts | Per year if the bottom 80% were flat, % |
|---|---|---|---|---|---|
| top 1% | 6.3 | +1.0 | total expenditures | 79.7 | 21.6 |
| top 1% | 6.3 | +2.5 | excl. pensions and contributions | 70.7 | 19.5 |
| top 5% | 18.0 | +1.0 | total expenditures | 28.3 | 8.7 |
| top 5% | 18.0 | +2.5 | excl. pensions and contributions | 26.2 | 8.1 |
| top 10% | 28.3 | +1.0 | total expenditures | 18.4 | 5.8 |
| top 10% | 28.3 | +2.5 | excl. pensions and contributions | 17.6 | 5.6 |

The last column annualizes 1 + gap, so it is the group's own growth a year only if the bottom 80% were flat. The
CE's bottom 80% grew 5.3% over the three years, and the group would need correspondingly more.

**Like with like.** Both the need and the wealth-effect bound (section 4) depend on how much spending sits with the
top 1%. The SCF puts 6.3% there (top 1% by income), the BEA-BLS joint distribution 2.1% (top 1% by DPI). With the
same shares on both sides the need exceeds the bound at any of the post's propensities. Mixing them, the SCF-weighted
need against the BEA-BLS bound, would reverse the comparison at 5 cents:

| Weights | Top 20% share, % | Top 1% share, % | Gap the top 1% needs, 2022-2025, pts | Bound on the top 1% by 2025Q2 at 2 / 3.5 / 5 cents, % of its spending | Need above the 5-cent bound? |
|---|---|---|---|---|---|
| SCF 2025 shares for both | 42.8 | 6.3 | 80 | 11.6 / 20.3 / 29.1 | yes |
| BEA-BLS 2023 shares for both | 33.9 | 2.1 | 187 | 34.6 / 60.6 / 86.6 | yes |
| Mixed: SCF-weighted need, BEA-BLS bound | 42.8 | 6.3 | 80 | 34.6 / 60.6 / 86.6 | no |

## 3. Income side

`out/direct_income_saving.csv` (blocks `income_quintile_levels`, `income_quintile_growth`, `taxes_by_dpi_group`,
`joint_by_dpi_group`, `saving_rate_monthly`, `saving_rate_annual`).

BEA's distribution of personal income (June 2026) gives two income concepts:

- **Personal income (PI):** before taxes, including in-kind transfers such as Medicare and Medicaid; households
  ranked by equivalized PI. It is the only concept with a 2025 nowcast.
- **Disposable personal income (DPI):** PI minus personal current taxes, the income spending is paid from;
  households ranked by equivalized DPI. It ends in 2024 (provisional). In the file DPI = PI - taxes exactly.

**BEA personal income by quintile of equivalized personal income** (shares of personal income by year, then
growth). Levels are share x NIPA total of the June
2026 vintage. The 2025 nowcast's ranking is not stated: its 2024 column equals the published 2024 shares, which are
the same under both rankings. Real values use ISPCEPX quintile indexes, and 2025 uses the aggregate PCE price index
as in section 2. The shares are printed to 0.001, which moves a bottom-quintile level by about 1% and its growth by
1-2 points.

| Group | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 (prov.) | 2025 (nowcast) | Real 2019-2024, % | Real 2022-2025, % | Real 2023-2025, % | Real 2024-2025, % | Nominal 2024-2025, % |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Q1 | 0.052 | 0.054 | 0.054 | 0.050 | 0.053 | 0.053 | 0.052 | 15.7 | 13.6 | 4.5 | 1.5 | 4.1 |
| Q2 | 0.094 | 0.100 | 0.100 | 0.095 | 0.096 | 0.095 | 0.096 | 14.9 | 9.0 | 5.1 | 3.1 | 5.8 |
| Q3 | 0.135 | 0.142 | 0.142 | 0.135 | 0.134 | 0.134 | 0.134 | 13.0 | 7.4 | 5.4 | 2.3 | 5.0 |
| Q4 | 0.194 | 0.201 | 0.199 | 0.191 | 0.189 | 0.190 | 0.191 | 11.5 | 8.1 | 6.4 | 2.7 | 5.4 |
| Q5 (top 20%) | 0.525 | 0.503 | 0.504 | 0.528 | 0.527 | 0.528 | 0.527 | 13.7 | 7.3 | 4.9 | 2.0 | 4.6 |
| Bottom 80% | 0.475 | 0.497 | 0.495 | 0.471 | 0.472 | 0.472 | 0.473 | 13.0 | 8.7 | 5.7 | 2.6 | 5.2 |
| All | 1.000 | 1.000 | 0.999 | 0.999 | 0.999 | 1.000 | 1.000 | 13.4 | 7.9 | 5.3 | 2.2 | 4.9 |

From 2022 to 2025 the top fifth's share of personal income stayed at 52.7-52.8%. The bottom 80%'s income grew a
little faster: real 8.7% against 7.3%, and nominal +5.2% against +4.6% in the 2025 nowcast. Taking the bottom 80%
as one minus the top fifth's share instead (the 2022 quintile shares sum to 0.999) gives 8.4% rather than 8.7%; the
sign survives. Before taxes there is no K.

**Disposable income by quintile of equivalized DPI**, with taxes by quintile (sums of decile shares x the file's
totals) and taxes as a share of each group's personal income under the same ranking:

| Group | DPI share 2019 | DPI share 2022 | DPI share 2023 | DPI share 2024 (prov.) | Real DPI 2019-2024, % | Real DPI 2022-2023, % | Real DPI 2023-2024, % | Real DPI 2022-2024, % | Taxes 2022, $bn | Taxes 2024, $bn | Taxes, % of PI 2022 | Taxes, % of PI 2023 | Taxes, % of PI 2024 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Q1 | 0.058 | 0.057 | 0.059 | 0.059 | 15.4 | 9.4 | 3.0 | 12.7 | 42 | 36 | 3.8 | 3.1 | 2.7 |
| Q2 | 0.103 | 0.106 | 0.105 | 0.104 | 14.7 | 4.8 | 2.0 | 6.9 | 101 | 93 | 4.7 | 3.9 | 3.9 |
| Q3 | 0.145 | 0.147 | 0.144 | 0.144 | 13.1 | 3.7 | 3.0 | 6.8 | 217 | 188 | 7.3 | 6.0 | 5.6 |
| Q4 | 0.201 | 0.200 | 0.196 | 0.197 | 11.5 | 3.7 | 3.6 | 7.4 | 441 | 400 | 10.4 | 8.6 | 8.5 |
| Q5 (top 20%) | 0.493 | 0.489 | 0.496 | 0.497 | 14.0 | 7.1 | 2.9 | 10.2 | 2,442 | 2,265 | 20.9 | 17.2 | 17.2 |
| Bottom 80% | 0.507 | 0.510 | 0.504 | 0.504 | 13.1 | 4.5 | 3.1 | 7.7 | 801 | 717 | 7.7 | 6.3 | 6.1 |
| All | 1.000 | 0.999 | 1.000 | 1.001 | 13.5 | 5.8 | 3.0 | 9.0 | 3,243 | 2,982 | 14.6 | 12.0 | 12.0 |

After taxes the top fifth did pull ahead: its real DPI grew 10.2% from 2022 to 2024 against 7.7% for the bottom
80%. All of the difference came in 2023 (7.1% against 4.5%); in 2024 the two grew alike (2.9% against 3.1%). The
cause is taxes. 2022 was a high-tax year, most of all at the top: taxes took 20.9% of the top fifth's personal
income, against 17.2% in 2023 and 2024 (bottom 80%: 7.7%, then 6.3% and 6.1%). The top fifth's taxes fell $177bn
from 2022 to 2024 while its personal income grew. The ranking does not explain it: DPI ranked by equivalized PI
shows the same tilt, and PI ranked by equivalized DPI shows none (real growth, top 20% against bottom 80%):

| Concept and ranking | 2022-2024: top 20%, % | 2022-2024: bottom 80%, % | 2022-2024: gap, pts | 2022-2023: top 20%, % | 2022-2023: bottom 80%, % | 2022-2023: gap, pts | 2023-2024: top 20%, % | 2023-2024: bottom 80%, % | 2023-2024: gap, pts |
|---|---|---|---|---|---|---|---|---|---|
| Personal income, ranked by equivalized PI (main) | 5.2 | 6.0 | -0.8 | 2.2 | 2.9 | -0.6 | 2.9 | 3.0 | -0.1 |
| Personal income, ranked by equivalized DPI | 5.2 | 5.7 | -0.5 | 2.2 | 3.1 | -0.8 | 2.9 | 2.6 | +0.3 |
| Disposable income, ranked by equivalized PI | 10.5 | 7.5 | +2.9 | 7.3 | 4.1 | +3.2 | 2.9 | 3.3 | -0.3 |
| Disposable income, ranked by equivalized DPI (main) | 10.2 | 7.7 | +2.5 | 7.1 | 4.5 | +2.6 | 2.9 | 3.1 | -0.1 |

So the income that pays for spending did tilt toward the top, once, in 2023, by about 2.5 points over two years.
That is about a third of the 8.2 points Zandi gives for spending over two years, and the CE's spending gap in 2023
was +1.2 (SE 2.7). DPI ends in 2024, before most of his window, and in 2024 it showed no tilt.

**Saving rates by DPI group, joint distribution** (deciles of equivalized DPI, 2019-2023). Saving is DPI minus
outlays. The rates are recomputed from the 3-decimal shares and the vintage's totals; the published rates agree
within rounding (check B5). PCE/DPI is the group's spending out of its disposable income.

| DPI group | Saving rate 2019, % | Saving rate 2020, % | Saving rate 2021, % | Saving rate 2022, % | Saving rate 2023, % | Change 2019-2023, pts | PCE/DPI 2019 | PCE/DPI 2023 |
|---|---|---|---|---|---|---|---|---|
| D1 | -126.2 | -112.8 | -101.5 | -144.9 | -134.2 | -8.0 | 2.17 | 2.29 |
| D2 | -48.7 | -32.5 | -38.2 | -54.0 | -50.4 | -1.7 | 1.46 | 1.44 |
| D3 | -35.4 | -19.4 | -26.2 | -39.2 | -35.8 | -0.4 | 1.32 | 1.32 |
| D4 | -26.5 | -12.4 | -17.4 | -29.5 | -27.8 | -1.3 | 1.22 | 1.22 |
| D5 | -16.9 | -4.7 | -10.8 | -20.9 | -21.6 | -4.7 | 1.13 | 1.17 |
| D6 | -10.0 | 0.6 | -5.5 | -15.2 | -16.0 | -6.0 | 1.05 | 1.12 |
| D7 | -3.6 | 4.8 | 1.0 | -9.4 | -8.0 | -4.4 | 1.00 | 1.04 |
| D8 | 1.8 | 11.9 | 7.0 | -3.5 | -1.3 | -3.1 | 0.94 | 0.97 |
| D9 | 7.6 | 19.2 | 11.2 | 1.9 | 5.0 | -2.6 | 0.89 | 0.91 |
| D10 | 45.6 | 50.1 | 49.3 | 44.3 | 46.6 | +1.0 | 0.52 | 0.52 |
| Bottom 80% (from shares) | -19.2 | -7.5 | -12.4 | -24.5 | -23.1 | -3.9 | 1.15 | 1.18 |
| Top 20% | 34.9 | 41.0 | 38.4 | 32.5 | 35.1 | +0.2 | 0.63 | 0.62 |
| Top 5% | 58.9 | 61.5 | 62.6 | 59.0 | 61.4 | +2.5 | 0.40 | 0.37 |
| Top 1% | 83.0 | 83.8 | 85.8 | 83.9 | 85.7 | +2.7 | 0.16 | 0.14 |
| All (from shares) | 7.3 | 15.3 | 11.6 | 3.3 | 5.6 | -1.7 | 0.89 | 0.91 |

**Did the top's saving rate fall? Not by 2023.** The top decile saved 45.6% of its DPI in 2019, 49-50% in
2020-2021 when services were shut, 44.3% in 2022 and 46.6% in 2023 (BEA's published rates; groups marked "from
shares" have no published rate). Its PCE/DPI was 0.52 in both 2019 and 2023. The
aggregate rate in this vintage fell from 7.3% to 5.6%, and that fall came from the bottom 80%: their spending rose
from 1.15 to 1.18 times their DPI. Their saving rate fell by 2022 (-24.5%, from -19.2%) and recovered a little in
2023 (-23.1%). The joint distribution ends in 2023, so it cannot say which of Zandi's two saving stories holds in
2025-26 (the rich saving less, or the lower-middle drawing down); the evidence table scores both rows "can't tell".
The negative rates at the bottom are partly a construction effect: CE-based PCE is allocated to CPS-based DPI
groups, and the bottom's income is under-reported. The change over time, not the level, is the signal.

**The personal saving rate** (NIPA, vintage of 2026-10-29; annual from Table 2.1, monthly from Table 2.6):

| Period | Saving rate, % of DPI |
|---|---|
| 2019 | 7.3 |
| 2020 | 15.3 |
| 2021 | 11.6 |
| 2022 | 3.5 |
| 2023 | 6.1 |
| 2024 | 6.3 |
| 2025 | 5.4 |
| 2026-01 | 5.6 |
| 2026-02 | 5.3 |
| 2026-03 | 5.1 |
| 2026-04 | 4.4 |
| 2026-05 | 4.4 |
| 2026-06 | 4.4 |
| 2026-07 | 4.5 |
| 2026-08 | 4.0 |
| 2026-09 | 3.8 |

From March to September 2026 personal saving fell by an amount equal to 40% of the rise in PCE (as in
`NOTES_sectors.md`). Who drew it down is not observed.

## 4. Wealth side: DFA by income group

`out/direct_dfa_wealth.csv` (blocks `levels`, `gains`, `z1_revaluation_share`, `wealth_effect_bound`,
`wealth_effect_gap`, `concentration_scf_vs_dfa`, `equity_runup_timing`) and `figures/fig_direct_dfa_equity.png`.

- **Income groups** are percentiles of SCF total family income (unequivalized, pre-tax), the same ranking the SCF
  uses.
- **Units:** $ billion, nominal. Equities exclude DC pensions. Since the 2026:Q2 release they include hedge and
  private-debt fund shares. Real estate is owner-occupied only.
- **After 2022Q3** (the last SCF quarter in the DFA) the group splits are the DFA's model extrapolations. SCF 2025
  is not yet in.

| Item | Income group | 2019Q4, $bn | 2022Q3, $bn | 2026Q2, $bn | Change 2022Q3-2026Q2, $bn | Change, % | Share 2026Q2, % | Per household 2026Q2, $k |
|---|---|---|---|---|---|---|---|---|
| Net worth | 0-20 | 3,227 | 4,093 | 5,146 | +1,053 | +26 | 2.8 | 190 |
| Net worth | 20-40 | 4,463 | 6,327 | 7,381 | +1,054 | +17 | 4.0 | 273 |
| Net worth | 40-60 | 8,188 | 11,797 | 13,961 | +2,164 | +18 | 7.5 | 516 |
| Net worth | 60-80 | 15,573 | 18,414 | 24,333 | +5,919 | +32 | 13.1 | 900 |
| Net worth | 80-99 | 49,499 | 62,846 | 87,971 | +25,125 | +40 | 47.4 | 3,425 |
| Net worth | 99-100 | 26,695 | 29,698 | 46,860 | +17,162 | +58 | 25.2 | 34,635 |
| Net worth | Top 20% | 76,194 | 92,544 | 134,830 | +42,286 | +46 | 72.6 | 4,986 |
| Net worth | Bottom 80% | 31,452 | 40,630 | 50,821 | +10,190 | +25 | 27.4 | 470 |
| Net worth | All | 107,646 | 133,174 | 185,651 | +52,477 | +39 | 100.0 | 1,373 |
| Corporate equities and mutual fund shares | 0-20 | 451 | 616 | 951 | +335 | +54 | 1.5 | 35 |
| Corporate equities and mutual fund shares | 20-40 | 360 | 338 | 671 | +333 | +99 | 1.0 | 25 |
| Corporate equities and mutual fund shares | 40-60 | 836 | 1,282 | 2,144 | +862 | +67 | 3.3 | 79 |
| Corporate equities and mutual fund shares | 60-80 | 2,212 | 2,098 | 4,488 | +2,390 | +114 | 6.9 | 166 |
| Corporate equities and mutual fund shares | 80-99 | 12,773 | 15,809 | 30,772 | +14,962 | +95 | 47.6 | 1,198 |
| Corporate equities and mutual fund shares | 99-100 | 11,812 | 11,633 | 25,615 | +13,982 | +120 | 39.6 | 18,933 |
| Corporate equities and mutual fund shares | Top 20% | 24,584 | 27,442 | 56,387 | +28,944 | +105 | 87.2 | 2,085 |
| Corporate equities and mutual fund shares | Bottom 80% | 3,860 | 4,334 | 8,254 | +3,919 | +90 | 12.8 | 76 |
| Corporate equities and mutual fund shares | All | 28,444 | 31,776 | 64,640 | +32,864 | +103 | 100.0 | 478 |
| Real estate | 0-20 | 1,525 | 2,150 | 2,546 | +396 | +18 | 5.1 | 94 |
| Real estate | 20-40 | 2,281 | 3,258 | 3,627 | +369 | +11 | 7.3 | 134 |
| Real estate | 40-60 | 3,359 | 5,658 | 6,036 | +378 | +7 | 12.1 | 223 |
| Real estate | 60-80 | 5,246 | 8,103 | 9,311 | +1,208 | +15 | 18.7 | 344 |
| Real estate | 80-99 | 12,428 | 18,282 | 21,946 | +3,665 | +20 | 44.1 | 854 |
| Real estate | 99-100 | 3,688 | 5,382 | 6,325 | +943 | +18 | 12.7 | 4,675 |
| Real estate | Top 20% | 16,117 | 23,664 | 28,271 | +4,607 | +19 | 56.8 | 1,045 |
| Real estate | Bottom 80% | 12,412 | 19,169 | 21,521 | +2,352 | +12 | 43.2 | 199 |
| Real estate | All | 28,528 | 42,833 | 49,792 | +6,959 | +16 | 100.0 | 368 |
| Consumer credit | 0-20 | 324 | 365 | 361 | -4 | -1 | 7.1 | 13 |
| Consumer credit | 20-40 | 603 | 599 | 668 | +69 | +11 | 13.0 | 25 |
| Consumer credit | 40-60 | 887 | 892 | 962 | +70 | +8 | 18.8 | 36 |
| Consumer credit | 60-80 | 1,145 | 1,233 | 1,329 | +96 | +8 | 25.9 | 49 |
| Consumer credit | 80-99 | 1,180 | 1,516 | 1,624 | +108 | +7 | 31.7 | 63 |
| Consumer credit | 99-100 | 53 | 149 | 176 | +27 | +18 | 3.4 | 130 |
| Consumer credit | Top 20% | 1,233 | 1,665 | 1,801 | +136 | +8 | 35.2 | 67 |
| Consumer credit | Bottom 80% | 2,959 | 3,089 | 3,320 | +230 | +7 | 64.8 | 31 |
| Consumer credit | All | 4,192 | 4,754 | 5,120 | +366 | +8 | 100.0 | 38 |

**Equity gains by group since 2022Q3.** Holdings of corporate equities and mutual fund shares rose $32.9tn
(+103%). The top 20% got 88.1% of it: the 80-99 group 45.5% and the top 1% 42.5%. The bottom 80% got $3.9tn, 11.9%,
on a base that also nearly doubled.

Not all of a change in holdings is a price gain. In the Z.1 the revaluation share of the change in household and
nonprofit equity-type holdings over the same window is 0.93 (S1M.r; corporate equities, mutual funds, hedge and
private-debt funds). It is applied to every group. The 2024Q2-2026Q2 row is used only as a sensitivity in the
saving cross-check below.

| Window | Z.1 level start, $bn | Z.1 level end, $bn | Change, $bn | Revaluations, $bn | Revaluation share |
|---|---|---|---|---|---|
| 2022Q3->2026Q2 | 35,139 | 69,167 | 34,028 | 31,535 | 0.927 |
| 2022Q3->2025Q2 | 35,139 | 54,629 | 19,490 | 18,505 | 0.949 |
| 2019Q4->2026Q2 | 31,124 | 69,167 | 38,043 | 33,354 | 0.877 |
| 2024Q2->2026Q2 | 47,580 | 69,167 | 21,587 | 19,297 | 0.894 |

**Timing.** The run-up was fastest at the end, after the CE window closed (all income groups):

| Window | Quarters | DFA equity holdings, change, $bn | Change, % | Z.1 revaluations, $bn | DFA change per quarter, $bn | Z.1 revaluations per quarter, $bn |
|---|---|---|---|---|---|---|
| 2022Q3->2023Q4 | 5 | +7,899 | 24.9 | +8,376 | +1,580 | +1,675 |
| 2023Q4->2024Q4 | 4 | +7,638 | 19.3 | +7,141 | +1,909 | +1,785 |
| 2024Q4->2025Q4 | 4 | +8,510 | 18.0 | +8,027 | +2,127 | +2,007 |
| 2025Q4->2026Q2 | 2 | +8,817 | 15.8 | +7,991 | +4,409 | +3,995 |

Holdings rose $8.8tn in the two quarters to 2026Q2, $4.4tn a quarter against $1.6-2.1tn a quarter before. Z.1
revaluations in those two quarters ($8.0tn) equal those of all of 2025.

**A hypothetical wealth effect at the post's 2-5 cents per dollar per year.** This is an assumption-driven bound,
not a measurement. The post states its propensity two ways: 2-5 cents in footnote 31 and the Figure 0 box, and
"three to five cents" in the body text. Figures 8-10 use 3.5 cents (`post_published_numbers.csv` rows P051-P052,
P570-P571 and P618). The range here is the wider 2-5, with 3.5 as the central case.

- The spending effect is c_w x revaluation gain, in $ per year.
- It is expressed as a share of each group's spending, with group spending equal to PCE at the window's end (mean
  of the monthly SAAR values) x the group's share. The main shares are SCF 2025 non-housing spending shares for the
  same income groups as the DFA. The alternative is the BEA-BLS 2023 PCE shares (DPI deciles; the top 1% is
  T01).
- It assumes the same propensity in every group and no lags.

| Window | Denominator | Group | Revaluation gain, $bn | Group spending, $bn | 2 cents: % of group spending | 3.5 cents | 5 cents | % of PCE at 2 / 3.5 / 5 cents |
|---|---|---|---|---|---|---|---|---|
| 2022Q3-2025Q2 | SCF 2025 shares | 0-20 | 189 | 1,489 | 0.3 | 0.4 | 0.6 | 0.02 / 0.03 / 0.05 |
| 2022Q3-2025Q2 | SCF 2025 shares | 20-40 | 181 | 2,326 | 0.2 | 0.3 | 0.4 | 0.02 / 0.03 / 0.04 |
| 2022Q3-2025Q2 | SCF 2025 shares | 40-60 | 479 | 3,303 | 0.3 | 0.5 | 0.7 | 0.05 / 0.08 / 0.12 |
| 2022Q3-2025Q2 | SCF 2025 shares | 60-80 | 1,290 | 4,733 | 0.5 | 1.0 | 1.4 | 0.12 / 0.22 / 0.31 |
| 2022Q3-2025Q2 | SCF 2025 shares | 80-99 | 8,148 | 7,560 | 2.2 | 3.8 | 5.4 | 0.79 / 1.38 / 1.97 |
| 2022Q3-2025Q2 | SCF 2025 shares | 99-100 | 7,530 | 1,296 | 11.6 | 20.3 | 29.1 | 0.73 / 1.27 / 1.82 |
| 2022Q3-2025Q2 | SCF 2025 shares | Top 20% | 15,679 | 8,856 | 3.5 | 6.2 | 8.9 | 1.51 / 2.65 / 3.79 |
| 2022Q3-2025Q2 | SCF 2025 shares | Bottom 80% | 2,140 | 11,851 | 0.4 | 0.6 | 0.9 | 0.21 / 0.36 / 0.52 |
| 2022Q3-2025Q2 | SCF 2025 shares | All | 17,818 | 20,707 | 1.7 | 3.0 | 4.3 | 1.72 / 3.01 / 4.30 |
| 2022Q3-2025Q2 | BEA-BLS 2023 shares | 0-20 | 189 | 2,381 | 0.2 | 0.3 | 0.4 | 0.02 / 0.03 / 0.05 |
| 2022Q3-2025Q2 | BEA-BLS 2023 shares | 20-40 | 181 | 3,085 | 0.1 | 0.2 | 0.3 | 0.02 / 0.03 / 0.04 |
| 2022Q3-2025Q2 | BEA-BLS 2023 shares | 40-60 | 479 | 3,748 | 0.3 | 0.4 | 0.6 | 0.05 / 0.08 / 0.12 |
| 2022Q3-2025Q2 | BEA-BLS 2023 shares | 60-80 | 1,290 | 4,473 | 0.6 | 1.0 | 1.4 | 0.12 / 0.22 / 0.31 |
| 2022Q3-2025Q2 | BEA-BLS 2023 shares | 80-99 | 8,148 | 6,585 | 2.5 | 4.3 | 6.2 | 0.79 / 1.38 / 1.97 |
| 2022Q3-2025Q2 | BEA-BLS 2023 shares | 99-100 | 7,530 | 435 | 34.6 | 60.6 | 86.6 | 0.73 / 1.27 / 1.82 |
| 2022Q3-2025Q2 | BEA-BLS 2023 shares | Top 20% | 15,679 | 7,020 | 4.5 | 7.8 | 11.2 | 1.51 / 2.65 / 3.79 |
| 2022Q3-2025Q2 | BEA-BLS 2023 shares | Bottom 80% | 2,140 | 13,687 | 0.3 | 0.5 | 0.8 | 0.21 / 0.36 / 0.52 |
| 2022Q3-2025Q2 | BEA-BLS 2023 shares | All | 17,818 | 20,707 | 1.7 | 3.0 | 4.3 | 1.72 / 3.01 / 4.30 |
| 2022Q3-2026Q2 | SCF 2025 shares | 0-20 | 310 | 1,581 | 0.4 | 0.7 | 1.0 | 0.03 / 0.05 / 0.07 |
| 2022Q3-2026Q2 | SCF 2025 shares | 20-40 | 308 | 2,470 | 0.2 | 0.4 | 0.6 | 0.03 / 0.05 / 0.07 |
| 2022Q3-2026Q2 | SCF 2025 shares | 40-60 | 799 | 3,508 | 0.5 | 0.8 | 1.1 | 0.07 / 0.13 / 0.18 |
| 2022Q3-2026Q2 | SCF 2025 shares | 60-80 | 2,215 | 5,028 | 0.9 | 1.5 | 2.2 | 0.20 / 0.35 / 0.50 |
| 2022Q3-2026Q2 | SCF 2025 shares | 80-99 | 13,866 | 8,030 | 3.5 | 6.0 | 8.6 | 1.26 / 2.21 / 3.15 |
| 2022Q3-2026Q2 | SCF 2025 shares | 99-100 | 12,957 | 1,376 | 18.8 | 33.0 | 47.1 | 1.18 / 2.06 / 2.95 |
| 2022Q3-2026Q2 | SCF 2025 shares | Top 20% | 26,823 | 9,406 | 5.7 | 10.0 | 14.3 | 2.44 / 4.27 / 6.10 |
| 2022Q3-2026Q2 | SCF 2025 shares | Bottom 80% | 3,632 | 12,587 | 0.6 | 1.0 | 1.4 | 0.33 / 0.58 / 0.83 |
| 2022Q3-2026Q2 | SCF 2025 shares | All | 30,455 | 21,993 | 2.8 | 4.8 | 6.9 | 2.77 / 4.85 / 6.92 |
| 2022Q3-2026Q2 | BEA-BLS 2023 shares | 0-20 | 310 | 2,529 | 0.2 | 0.4 | 0.6 | 0.03 / 0.05 / 0.07 |
| 2022Q3-2026Q2 | BEA-BLS 2023 shares | 20-40 | 308 | 3,277 | 0.2 | 0.3 | 0.5 | 0.03 / 0.05 / 0.07 |
| 2022Q3-2026Q2 | BEA-BLS 2023 shares | 40-60 | 799 | 3,981 | 0.4 | 0.7 | 1.0 | 0.07 / 0.13 / 0.18 |
| 2022Q3-2026Q2 | BEA-BLS 2023 shares | 60-80 | 2,215 | 4,751 | 0.9 | 1.6 | 2.3 | 0.20 / 0.35 / 0.50 |
| 2022Q3-2026Q2 | BEA-BLS 2023 shares | 80-99 | 13,866 | 6,994 | 4.0 | 6.9 | 9.9 | 1.26 / 2.21 / 3.15 |
| 2022Q3-2026Q2 | BEA-BLS 2023 shares | 99-100 | 12,957 | 462 | 56.1 | 98.2 | 140.3 | 1.18 / 2.06 / 2.95 |
| 2022Q3-2026Q2 | BEA-BLS 2023 shares | Top 20% | 26,823 | 7,456 | 7.2 | 12.6 | 18.0 | 2.44 / 4.27 / 6.10 |
| 2022Q3-2026Q2 | BEA-BLS 2023 shares | Bottom 80% | 3,632 | 14,537 | 0.5 | 0.9 | 1.2 | 0.33 / 0.58 / 0.83 |
| 2022Q3-2026Q2 | BEA-BLS 2023 shares | All | 30,455 | 21,993 | 2.8 | 4.8 | 6.9 | 2.77 / 4.85 / 6.92 |

The implied top-20% minus bottom-80% gap, in points of group spending, by what is counted as the gain:

| Window | Gain counted | SCF shares, 2 cents | SCF shares, 3.5 cents | SCF shares, 5 cents | BEA-BLS shares, 2 cents | BEA-BLS shares, 3.5 cents | BEA-BLS shares, 5 cents |
|---|---|---|---|---|---|---|---|
| 2022Q3-2025Q2 | equities (revaluation share applied) | 3.2 | 5.6 | 7.9 | 4.2 | 7.3 | 10.4 |
| 2022Q3-2025Q2 | equities (level change) | 3.3 | 5.9 | 8.4 | 4.4 | 7.7 | 10.9 |
| 2022Q3-2025Q2 | net worth (level change) | 4.7 | 8.3 | 11.8 | 6.4 | 11.2 | 16.0 |
| 2022Q3-2026Q2 | equities (revaluation share applied) | 5.1 | 9.0 | 12.8 | 6.7 | 11.7 | 16.7 |
| 2022Q3-2026Q2 | equities (level change) | 5.5 | 9.7 | 13.8 | 7.2 | 12.6 | 18.1 |
| 2022Q3-2026Q2 | net worth (level change) | 7.4 | 12.9 | 18.4 | 9.9 | 17.4 | 24.9 |

**Against the spending data.** For 2022Q3 to 2025Q2, which lines up with CE 2022-2025, the bound gives a gap of
3.2-7.9 points (5.6 at 3.5 cents) with SCF denominators and 4.2-10.4 with BEA-BLS denominators. By 2026Q2 it is
5.1-12.8 and 6.7-16.7. The CE shows +1.0 (+2.5 without pensions and contributions); Zandi says +12.5.

The bound puts most of the effect on the top 1%: 20% of its spending at 3.5 cents by 2025Q2, and 61% with the
BEA-BLS denominators, whose top-1% PCE share is only 2.1%. That says the uniform propensity is too high for the very
top more than it says anything about spending.

**The saving rate against the bound** (like with like: the 2023-24 saving rate already contains the effect of
gains up to then):

| Item | Value |
|---|---|
| Saving rate, 2023-2024 average of annual rates, % of DPI | 6.20 |
| Saving rate, 2026Q3 (Jul-Sep monthly average), % of DPI | 4.10 |
| Change, pts of DPI | -2.10 |
| Household equity holdings (DFA), 2023-2024 average, $bn | 41,196 |
| Revaluation gain from that average to 2026Q2 (Z.1 2022Q3-2026Q2 revaluation share applied), $bn | 21,726 |
| Wealth effect of that gain at 2 cents, % of DPI (2026Q2) | 1.81 |
| Wealth effect of that gain at 3.5 cents, % of DPI (2026Q2) | 3.17 |
| Wealth effect of that gain at 5 cents, % of DPI (2026Q2) | 4.53 |
| Same at 2 / 3.5 / 5 cents with the 2024Q2-2026Q2 revaluation share (0.894), % of DPI | 1.75 / 3.06 / 4.37 |

The saving rate fell 2.1 points of DPI. A wealth effect on the gains since the 2023-24 average would give 1.8
points at 2 cents, 3.2 at 3.5 cents and 4.5 at 5 cents (1.75, 3.06 and 4.37 with the revaluation share of the
window that starts nearer the base). The fall is therefore of the size of the low end of the post's range, if
nothing else moved saving. The bottom's drawdown, interest rates, taxes and transfers all did move it, so this
cannot identify a wealth effect.

**Concentration: survey against model, and Zandi's "90%".** In the table below each cell is the SCF share / the
DFA equities share (for net worth, the DFA net worth share), in % by income group. The DFA's split at the 2022 SCF
quarter is survey-based by construction. At 2025Q3 it is model-based; it matches SCF 2025 for the top fifth (87.0%
against 87.2% of directly held stocks and funds) but gives the top 1% a little more (39.0% against 36.4%).

| SCF year (DFA quarter) | SCF concept | 0-20 | 20-40 | 40-60 | 60-80 | 80-99 | 99-100 |
|---|---|---|---|---|---|---|---|
| 2022 (2022Q3) | SCF directly held stocks + non-money-market funds (STOCKS + NMMF) | 2.1 / 1.9 | 0.8 / 1.1 | 3.4 / 4.0 | 5.4 / 6.6 | 50.8 / 49.8 | 37.5 / 36.6 |
| 2022 (2022Q3) | SCF all equity held directly or indirectly (EQUITY, incl. retirement accounts) | 1.7 / 1.9 | 1.5 / 1.1 | 4.7 / 4.0 | 8.6 / 6.6 | 55.1 / 49.8 | 28.4 / 36.6 |
| 2022 (2022Q3) | SCF net worth | 3.7 / 3.1 | 3.7 / 4.8 | 7.8 / 8.9 | 11.3 / 13.8 | 47.9 / 47.2 | 25.7 / 22.3 |
| 2025 (2025Q3) | SCF directly held stocks + non-money-market funds (STOCKS + NMMF) | 0.7 / 1.6 | 1.3 / 1.0 | 2.7 / 3.5 | 8.0 / 6.9 | 50.8 / 48.1 | 36.4 / 39.0 |
| 2025 (2025Q3) | SCF all equity held directly or indirectly (EQUITY, incl. retirement accounts) | 0.8 / 1.6 | 1.7 / 1.0 | 4.4 / 3.5 | 10.8 / 6.9 | 56.5 / 48.1 | 25.7 / 39.0 |
| 2025 (2025Q3) | SCF net worth | 2.4 / 2.9 | 4.1 / 4.2 | 7.5 / 7.8 | 13.0 / 13.3 | 48.9 / 47.4 | 24.0 / 24.4 |

| Measure | Year | Share, % |
|---|---|---|
| SCF EQUITY: share held by the top10 by income | 2022 | 70.8 |
| SCF EQUITY: share held by the top20 by income | 2022 | 83.5 |
| SCF EQUITY: share held by the top1 by income | 2022 | 28.4 |
| SCF EQUITY: share held by the top10 by WEALTH | 2022 | 81.7 |
| SCF DEQ: share held by the top10 by income | 2022 | 79.0 |
| SCF DEQ: share held by the top20 by income | 2022 | 87.9 |
| SCF DEQ: share held by the top1 by income | 2022 | 37.8 |
| SCF DEQ: share held by the top10 by WEALTH | 2022 | 90.8 |
| SCF DIRECT_EQ_MF: share held by the top10 by income | 2022 | 79.4 |
| SCF DIRECT_EQ_MF: share held by the top20 by income | 2022 | 88.3 |
| SCF DIRECT_EQ_MF: share held by the top1 by income | 2022 | 37.5 |
| SCF DIRECT_EQ_MF: share held by the top10 by WEALTH | 2022 | 91.5 |
| SCF EQUITY: share held by the top10 by income | 2025 | 70.8 |
| SCF EQUITY: share held by the top20 by income | 2025 | 82.3 |
| SCF EQUITY: share held by the top1 by income | 2025 | 25.7 |
| SCF EQUITY: share held by the top10 by WEALTH | 2025 | 81.5 |
| SCF DEQ: share held by the top10 by income | 2025 | 79.6 |
| SCF DEQ: share held by the top20 by income | 2025 | 87.7 |
| SCF DEQ: share held by the top1 by income | 2025 | 35.7 |
| SCF DEQ: share held by the top10 by WEALTH | 2025 | 90.9 |
| SCF DIRECT_EQ_MF: share held by the top10 by income | 2025 | 79.5 |
| SCF DIRECT_EQ_MF: share held by the top20 by income | 2025 | 87.2 |
| SCF DIRECT_EQ_MF: share held by the top1 by income | 2025 | 36.4 |
| SCF DIRECT_EQ_MF: share held by the top10 by WEALTH | 2025 | 91.6 |
| DFA corporate equities and MF: share held by the top 10% by WEALTH (Next9 + RemainingTop1 + TopPt1) | 2022Q3 | 87.0 |
| DFA corporate equities and MF: share held by the top 20% by INCOME (80-99 + 99-100) | 2022Q3 | 86.4 |
| DFA corporate equities and MF: share held by the top 10% by WEALTH (Next9 + RemainingTop1 + TopPt1) | 2025Q3 | 87.8 |
| DFA corporate equities and MF: share held by the top 20% by INCOME (80-99 + 99-100) | 2025Q3 | 87.0 |
| DFA corporate equities and MF: share held by the top 10% by WEALTH (Next9 + RemainingTop1 + TopPt1) | 2026Q2 | 88.0 |
| DFA corporate equities and MF: share held by the top 20% by INCOME (80-99 + 99-100) | 2026Q2 | 87.2 |

Zandi said the top 10% of the income distribution hold 90% of equities, counting "corporate equity, directly held,
indirectly held, and mutual funds and everything else". On that concept, all equity held directly or indirectly
(SCF EQUITY, which includes retirement accounts), SCF 2025 gives the top 10% by income 70.8% and the top 10% by
wealth 81.5%. The 90% fits directly held stocks and funds ranked by wealth: 91.6% in SCF 2025 (90.9% for directly
held equity, DEQ = stocks, stock funds, half of combination funds and other funds) and 88.0% in the DFA, which
leaves out DC pensions. Ranked by income, the same directly held assets give the top 10% 79.5%. So his figure is
about right for the stocks and funds the wealthiest tenth hold directly, and too high for the holdings he
described under either ranking (81.5% by wealth, 70.8% by income).

## 5. SCF 2025: the windfall question and the MPC gradient

`out/direct_scf2025_windfall.csv` (blocks `windfall`, `gradient_vs_post`), `out/direct_scf2025_spending.csv`,
`figures/fig_direct_windfall.png`.

**The question** (X9375-X9377): "Imagine you unexpectedly receive a sum of money equal to one month of your
(family's) normal annual income. Thinking over the next 12 months, please indicate the percent of this money that
you would save, the percent you would spend, and the percent that you would use to pay down debts."

**Method.**

- Family-weighted means use WGT over all five implicates.
- SEs come from a family bootstrap: 400 replicates, with each family's five implicates resampled together. The
  extract has no replicate weights, so the SCF design is ignored.
- The publisher's figures come from the FEDS Note's accessible tables.
- The extract reproduces the overall means exactly (22.35 / 47.31 / 30.30) and the wealth table within 0.3 point.
  The normal-income table matches within 0.2 point from the 60th percentile up and within 0.7 point below it. The
  note presumably used the internal data (check A10).

| Usual income | Spend % | Spend % (publisher) | Save % | Save % (publisher) | Pay debt % | Pay debt % (publisher) | SE spend (bootstrap) | Spend nothing, % of families | Mean windfall, $ |
|---|---|---|---|---|---|---|---|---|---|
| 0-10 | 28.81 | 28.30 | 45.17 | 45.60 | 25.97 | 26.10 | 1.97 | 38.4 | 1,467 |
| 10-20 | 24.30 | 25.00 | 48.95 | 48.40 | 26.70 | 26.60 | 1.67 | 37.9 | 2,733 |
| 20-30 | 25.59 | 24.90 | 45.52 | 45.50 | 28.85 | 29.50 | 1.77 | 40.5 | 3,837 |
| 30-40 | 23.23 | 23.70 | 44.25 | 43.90 | 32.48 | 32.30 | 1.84 | 43.8 | 4,907 |
| 40-50 | 22.23 | 22.70 | 44.80 | 45.00 | 32.92 | 32.20 | 1.60 | 43.2 | 6,272 |
| 50-60 | 20.02 | 19.40 | 44.74 | 45.00 | 35.19 | 35.50 | 1.72 | 47.7 | 7,874 |
| 60-70 | 20.44 | 20.50 | 41.70 | 41.80 | 37.81 | 37.60 | 1.62 | 50.3 | 9,753 |
| 70-80 | 19.88 | 19.80 | 43.53 | 43.50 | 36.57 | 36.60 | 1.75 | 51.1 | 12,518 |
| 80-90 | 19.12 | 19.20 | 53.49 | 53.50 | 27.35 | 27.30 | 1.54 | 51.7 | 17,055 |
| 90-95 | 22.21 | 22.20 | 53.06 | 53.00 | 24.69 | 24.70 | 2.32 | 56.8 | 24,726 |
| 95-99 | 18.33 | 18.40 | 66.72 | 66.60 | 14.92 | 15.00 | 1.74 | 57.7 | 48,166 |
| 99-100 | 14.06 | 14.00 | 77.38 | 77.50 | 8.54 | 8.50 | 2.73 | 67.8 | 193,963 |
| All families | 22.35 | 22.35 | 47.31 | 47.31 | 30.30 | 30.30 | 0.54 | 46.3 | 11,746 |

By decile, under three rankings (income-weighted = dollar-weighted by usual income, the response to a windfall
proportional to income):

| Ranking | Decile | Spend % | Save % | Pay debt % | Spend + debt % | Spend, income-weighted % | SE spend |
|---|---|---|---|---|---|---|---|
| income 2024 | D1 | 29.0 | 44.1 | 26.9 | 55.9 | 26.8 | 2.02 |
| income 2024 | D2 | 25.5 | 47.1 | 27.3 | 52.8 | 25.3 | 1.62 |
| income 2024 | D3 | 25.4 | 44.7 | 29.8 | 55.2 | 25.9 | 1.68 |
| income 2024 | D4 | 23.4 | 45.0 | 31.5 | 54.9 | 23.9 | 1.83 |
| income 2024 | D5 | 21.9 | 44.0 | 34.0 | 55.9 | 22.2 | 1.57 |
| income 2024 | D6 | 19.3 | 45.5 | 35.2 | 54.5 | 19.3 | 1.64 |
| income 2024 | D7 | 20.9 | 41.2 | 37.9 | 58.8 | 20.6 | 1.73 |
| income 2024 | D8 | 18.8 | 46.5 | 34.7 | 53.5 | 18.7 | 1.72 |
| income 2024 | D9 | 21.2 | 52.2 | 26.6 | 47.7 | 21.7 | 1.67 |
| income 2024 | D10 | 18.1 | 62.8 | 19.1 | 37.2 | 16.5 | 1.25 |
| usual income | D1 | 28.8 | 45.2 | 26.0 | 54.8 | 27.8 | 1.97 |
| usual income | D2 | 24.3 | 49.0 | 26.7 | 51.0 | 24.3 | 1.67 |
| usual income | D3 | 25.6 | 45.5 | 28.9 | 54.4 | 25.6 | 1.77 |
| usual income | D4 | 23.2 | 44.3 | 32.5 | 55.7 | 23.1 | 1.84 |
| usual income | D5 | 22.2 | 44.8 | 32.9 | 55.1 | 22.3 | 1.60 |
| usual income | D6 | 20.0 | 44.7 | 35.2 | 55.2 | 20.1 | 1.72 |
| usual income | D7 | 20.4 | 41.7 | 37.8 | 58.3 | 20.4 | 1.62 |
| usual income | D8 | 19.9 | 43.5 | 36.6 | 56.4 | 20.0 | 1.75 |
| usual income | D9 | 19.1 | 53.5 | 27.4 | 46.5 | 19.1 | 1.54 |
| usual income | D10 | 19.8 | 61.0 | 19.2 | 39.0 | 17.3 | 1.38 |
| net worth | D1 | 25.0 | 35.2 | 39.7 | 64.7 | 20.8 | 1.65 |
| net worth | D2 | 25.4 | 47.0 | 27.5 | 53.0 | 23.0 | 1.75 |
| net worth | D3 | 23.6 | 44.1 | 32.3 | 55.9 | 22.8 | 1.70 |
| net worth | D4 | 23.7 | 38.0 | 38.2 | 61.9 | 23.1 | 1.91 |
| net worth | D5 | 20.3 | 44.3 | 35.3 | 55.6 | 18.3 | 1.55 |
| net worth | D6 | 20.9 | 43.6 | 35.4 | 56.3 | 19.3 | 1.64 |
| net worth | D7 | 19.8 | 45.1 | 35.1 | 54.9 | 19.4 | 1.66 |
| net worth | D8 | 21.1 | 52.0 | 26.9 | 48.0 | 19.8 | 1.81 |
| net worth | D9 | 21.7 | 56.4 | 21.9 | 43.5 | 19.9 | 1.76 |
| net worth | D10 | 21.9 | 67.3 | 10.8 | 32.7 | 17.8 | 1.50 |

**Liquidity.**

- *Hand-to-mouth, FEDS Note definition:* liquid assets below half a month of usual income. Liquid assets are
  transaction accounts, call accounts, CDs, prepaid cards, and directly held funds, stocks and bonds.
- *KVW-style variant:* net liquid wealth (the same assets less CDs, minus credit card balances) at or below half a
  month of 2024 income. It counts as wealthy hand-to-mouth if illiquid wealth is positive (home equity, other
  residential real estate net of its debt, net equity in nonresidential real estate (NNRESRE), retirement accounts,
  life insurance cash value, CDs, savings bonds, other managed assets). The 2025 extract lacks pay frequency and
  credit limits, so KVW's pay-period and borrowing-limit refinements are not possible.
- *Months of usual income:* liquid assets over a month of usual income. Families with zero or negative usual
  income have no ratio; those holding any account (the extract sets LIQ to $1 for zero balances) are put in the 24+
  group (0.01m families). That keeps the "<0.5 month" group identical to the hand-to-mouth group: they are not
  hand-to-mouth under the note's definition either.
- *Regression-adjusted means:* the FEDS Note's Figure 4 recipe (WLS on hand-to-mouth status and log usual income, at
  the mean log income) gives 23.7 against 21.7. The note's own figures are 22.9 against 20.3.

| Grouping | Group | Families, m | Spend % | Save % | Pay debt % | SE spend | Publisher spend % |
|---|---|---|---|---|---|---|---|
| hand-to-mouth (FEDS Note definition) | not hand-to-mouth | 92.7 | 21.2 | 52.8 | 26.0 | 0.64 |  |
| hand-to-mouth (FEDS Note definition) | hand-to-mouth | 42.3 | 24.9 | 35.2 | 39.8 | 1.01 |  |
| hand-to-mouth (KVW-style, poor/wealthy) | poor hand-to-mouth | 17.3 | 27.9 | 39.9 | 32.2 | 1.53 |  |
| hand-to-mouth (KVW-style, poor/wealthy) | wealthy hand-to-mouth | 36.9 | 21.5 | 31.2 | 47.2 | 1.08 |  |
| hand-to-mouth (KVW-style, poor/wealthy) | not hand-to-mouth | 80.8 | 21.5 | 56.2 | 22.2 | 0.69 |  |
| liquidity, months of usual income | <0.5 month (hand-to-mouth) | 42.3 | 24.9 | 35.2 | 39.8 | 1.01 |  |
| liquidity, months of usual income | 0.5-2 months | 35.3 | 21.4 | 43.1 | 35.5 | 1.09 |  |
| liquidity, months of usual income | 2-6 months | 22.4 | 21.4 | 49.7 | 28.8 | 1.26 |  |
| liquidity, months of usual income | 6-24 months | 18.4 | 19.9 | 61.0 | 19.0 | 1.26 |  |
| liquidity, months of usual income | 24+ months | 16.6 | 21.7 | 68.7 | 9.6 | 1.56 |  |
| hand-to-mouth x usual-income quintile | HtM, usual-income Q1 | 14.1 | 29.2 | 39.8 | 30.9 | 1.79 |  |
| hand-to-mouth x usual-income quintile | HtM, usual-income Q2 | 11.4 | 25.7 | 38.7 | 35.5 | 1.94 |  |
| hand-to-mouth x usual-income quintile | HtM, usual-income Q3 | 8.8 | 21.5 | 31.0 | 47.4 | 2.19 |  |
| hand-to-mouth x usual-income quintile | HtM, usual-income Q4 | 5.6 | 22.8 | 22.9 | 54.3 | 2.65 |  |
| hand-to-mouth x usual-income quintile | HtM, usual-income Q5 | 2.3 | 13.4 | 35.7 | 50.9 | 3.00 |  |
| hand-to-mouth x usual-income quintile | not HtM, usual-income Q1 | 12.8 | 23.6 | 55.1 | 21.3 | 1.97 |  |
| hand-to-mouth x usual-income quintile | not HtM, usual-income Q2 | 15.6 | 23.5 | 49.4 | 27.1 | 1.76 |  |
| hand-to-mouth x usual-income quintile | not HtM, usual-income Q3 | 18.2 | 20.9 | 51.4 | 27.6 | 1.33 |  |
| hand-to-mouth x usual-income quintile | not HtM, usual-income Q4 | 21.4 | 19.5 | 47.8 | 32.7 | 1.34 |  |
| hand-to-mouth x usual-income quintile | not HtM, usual-income Q5 | 24.7 | 20.1 | 59.3 | 20.6 | 1.06 |  |
| spending vs income last year (WSAVED) | spending exceeded income | 25.5 | 23.8 | 34.3 | 41.8 | 1.46 |  |
| spending vs income last year (WSAVED) | spending equaled income | 37.4 | 25.1 | 42.0 | 32.8 | 1.08 |  |
| spending vs income last year (WSAVED) | spending below income | 72.1 | 20.4 | 54.6 | 24.9 | 0.72 |  |
| hand-to-mouth, regression-adjusted (FEDS Note Fig. 4 recipe) | not hand-to-mouth |  | 21.7 |  |  |  | 20.3 |
| hand-to-mouth, regression-adjusted (FEDS Note Fig. 4 recipe) | hand-to-mouth |  | 23.7 |  |  |  | 22.9 |

**The gradient against the post's assumption.** The post's MPC schedule runs from 1.0 in the bottom deciles to
0.40-0.65 at the top, for a permanent flow (Fig 0 box and footnote 27), so its top-to-bottom ratio is 0.40-0.65.

| Ranking | Top | Bottom | Spend top % | Spend bottom % | Ratio | 95% (family bootstrap) | Ratio, spend + debt | Ratio, income-weighted | Post's ratio |
|---|---|---|---|---|---|---|---|---|---|
| usual income, deciles | D10 | D1 | 19.8 | 28.8 | 0.69 | 0.57-0.83 | 0.71 | 0.62 | 0.40-0.65 |
| income 2024, deciles | D10 | D1 | 18.1 | 29.0 | 0.62 | 0.51-0.75 | 0.67 | 0.62 | 0.40-0.65 |
| usual income, 12 groups | 99-100 | 0-10 | 14.1 | 28.8 | 0.49 | 0.32-0.71 | 0.41 | 0.50 | 0.40-0.65 |
| income 2024, 12 groups | 99-100 | 0-10 | 17.6 | 29.0 | 0.61 | 0.41-0.86 | 0.47 | 0.57 | 0.40-0.65 |

- **Spending.** The share spent falls gently with income from about 29% in the bottom decile to about 20%, then
  drops to 14-18% in the top 1%. A top-decile family would spend 0.62-0.69 times what a bottom-decile family would.
  That sits at the flat end of the post's range, and the 95% bootstrap intervals (0.51-0.83) straddle it. The top
  1% (0.49-0.61) is inside it.
- **Saving.** Saving is flat at 41-49% over the bottom 80% and rises to 77% in the top 1%. Paying down debt peaks in
  the 60-80 range and is small at the top.
- **Liquidity.** It matters less than models imply. Hand-to-mouth families would spend 24.9% against 21.2%, and
  within the bottom quintile 29.2% against 23.6%. Most of the liquidity gradient is in saving against debt
  repayment, not in spending.

**Caveats on reading this as an MPC.**

- **The question.** It is hypothetical and records a stated intention over 12 months. The windfall is one-off and
  sized at a month of usual income, so it rises with income. The FEDS Note (fn 9) points out that a fixed-dollar
  windfall would load any size effect onto the gradient differently. What it can speak to is the ordering of the
  post's gradient: who spends more of a windfall.
- **Debt repayment.** It is offered as a third option; economists count it as saving.
- **The answers.** They bunch at round numbers: 46% of families would spend nothing, 4% all of it.
- **The level.** It is not comparable with the post's 1.0 at the bottom, which is for a permanent flow.
- **The note's interval.** Its "conventional" 95% interval for the top 1% (12.9-15.0) is much narrower than the
  family bootstrap gives (SE 2.7). That is a difference of method: the note uses the internal data and the SCF's
  design, while the bootstrap here resamples families and ignores the design. The top-1% group has 508 distinct
  families (492 family-equivalents, implicate records / 5) with very unequal weights.

**SCF 2025 spending against the Bulletin** (Box 1; checks A9):

| Grouping | Group | Mean, $ | Bulletin mean, $ | Share of aggregate, % | Bulletin share, % |
|---|---|---|---|---|---|
| all | all families | 48,693 | 48,700 | 100.0 |  |
| usual income, 6 groups | 0-20 | 17,653 | 17,600 | 7.2 | 7.2 |
| usual income, 6 groups | 80-90 | 68,704 | 68,700 | 14.1 |  |
| usual income, 6 groups | 90-100 | 138,396 | 138,800 | 28.4 | 28.5 |
| net worth, 6 groups | 0-20 | 23,392 | 23,400 | 9.6 |  |
| net worth, 6 groups | 80-90 | 68,729 | 68,800 | 14.1 |  |
| net worth, 6 groups | 90-100 | 135,631 | 136,000 | 27.9 | 27.9 |

## 6. Evidence summary for the K-shape question

`out/direct_evidence_table.csv`:

| Source | Ranking | Years | What it shows for the top vs the rest | Consistent with Zandi's split? | Caveat |
|---|---|---|---|---|---|
| CE Table 1101/1110 (BLS), top shares of total expenditures | income before taxes, consumer units, unequivalized | 2014-2025 (deciles), 2019-2025 (quintiles) | Top 20% share 38.7% (2019), 38.5% (2022), 38.9% (2023), 38.9% (2025), approx. SE 0.35-0.46; Zandi's split implies 41.5% by 2025 from 2022 (4.2 SEs of the change above the observed share; 40.8% from 2023, 3.1 SEs). Top 10% 22.9% -> 23.6%. | no | CE under-covers the very top (no oversample; nonresponse and under-reporting rise with income); 2025 collected through the Oct-Nov 2025 funding lapse (reweighted, Fay's BRR SEs). |
| CE (BLS), real growth by group, ISPCEPX-deflated | income before taxes, CU, unequivalized | 2022-2025, 2023-2025, 2024-2025 | Real aggregate spending 2022->2025: top 20% +6.3%, bottom 80% +5.3% (gap +1.0 pts, approx. SE 2.8; Zandi +12.5). 2023->2025 gap -0.2 (SE 2.7; Zandi +8.2). Excluding pensions, Social Security and cash contributions: +2.5 and +0.6. Top 10% vs bottom 90%, 2022->2025: +3.8 (SE 4.1). The latest year alone, 2024->2025: +1.9 (SE 2.7) against Zandi's +4.0, which fits either story. | no | Same coverage caveat. The case against the split rests on the multi-year windows, and the equity run-up was fastest after the CE window closed (DFA equity holdings +$8.8tn in 2026H1). ISPCEPX is a PCE-scope deflator by deciles of equivalized DPI, not CE income groups, with imputed 2024 weights; 2025 deflated with aggregate PCE prices (no group index yet). |
| BLS distributional PCE, top shares of PCE | equivalized total PCE (spending), CU-weighted | 2000-2023 | Top 20% 39.8% (2019), 40.0% (2022), 39.5% (2023); top 10% 26.4% -> 25.7%. | can't tell | Ends in 2023, the start of Zandi's window; ranked by spending, so the top is the top spenders, not the top earners; 2022->2023 moved against a K. |
| BEA-BLS joint distribution, PCE shares | equivalized disposable personal income, households | 2000-2023 | Top 20% by DPI 34.3% of PCE (2019), 34.1% (2022), 33.9% (2023); top 10% 20.2%. | can't tell | Ends in 2023; research-stage statistics; PCE side allocated with CE-based shares, which put only 2.1% of PCE with the top 1% by DPI. |
| BEA-BLS joint distribution, saving rates (top) | equivalized DPI | 2019-2023 | Top decile saving rate 45.6% (2019), 49.3% (2021), 44.3% (2022), 46.6% (2023): not below 2019 by 2023. | can't tell | Ends in 2023, before most of Zandi's window and before the 2025-26 equity run-up, so it cannot test his claim that the rich now save less: it shows only that the top's saving rate had not fallen by 2023. |
| BEA-BLS joint distribution, saving rates (bottom 80%) | equivalized DPI | 2019-2023 | Bottom 80% saving rate -19.2% (2019), -24.5% (2022), -23.1% (2023): spending further above income by 2022, slightly less so in 2023. | can't tell | Ends in 2023, before the drawdown Zandi describes (2025-26), and the 2019-2023 fall happened by 2022, then partly reversed. Negative rates at the bottom are partly a construction effect (CE-based PCE allocated to CPS-based DPI groups); the change, not the level, is the signal. |
| BEA distribution of personal income (2025 experimental nowcast) | equivalized personal income, households (2025: ranking not stated) | 2019-2025 | Real PI 2022->2025: top 20% +7.3%, bottom 80% +8.7%; nominal 2024->2025 nowcast: top 20% +4.6%, bottom 80% +5.2%. | no | Income before taxes, including in-kind Medicare and Medicaid; spending is paid from disposable income (next row). 2024 provisional, 2025 an experimental nowcast; shares rounded to 0.001 (bottom 80% taken as one minus the top fifth's share: +8.4%). |
| BEA distribution of personal income: disposable personal income (DPI) | equivalized disposable personal income, households | 2019-2024 | Real DPI 2022->2024: top 20% +10.2%, bottom 80% +7.7% (gap +2.5 pts), all of it in 2022->2023; 2023->2024 top 20% +2.9%, bottom 80% +3.1%. Taxes took 20.9% of the top fifth's personal income in 2022 and 17.2% in 2024 (bottom 80%: 7.7% and 6.1%). | can't tell | The income spending is paid from. The tilt to the top came from taxes falling back from a 2022 peak that was heaviest at the top (DPI ranked by personal income shows it too), is 31% of Zandi's two-year 8.2 points, and stopped in 2024; the series ends in 2024 (provisional), before most of his window. |
| NIPA personal saving rate (Table 2.6) | aggregate (no distribution) | 2019-01 to 2026-09 | 7.3% (2019), 3.5% (2022), 6.3% (2024), 5.4% (2025), 3.8% (Sep 2026); the fall in saving from Mar to Sep 2026 equals 40% of the rise in PCE over those six months (as in NOTES_sectors.md). | can't tell | Who is drawing down saving is not observed after 2023: Zandi's two stories (the rich need to save less; the lower middle draws down) both fit an aggregate decline. |
| SCF 2025 (Fed), total non-housing spending | family income in 2024 (also usual income) | 2025 survey (spending over the past 12 months) | Top 10% by income 28.3% of non-housing spending, top 20% 42.8%, top 1% 6.3%. | can't tell | One cross-section, first time asked: no trend. Scope excludes housing, loan payments and retirement contributions; one summary question; aggregate $6.6tn against $20.87tn of PCE in calendar 2025 (NIPA Table 2.1). |
| SCF 2025 (Fed), one-month windfall question | usual income (publisher), 2024 income, liquidity | 2025 survey | Share spent: bottom decile 28.8%, top decile 19.8%, top 1% 14.1%; top/bottom decile ratio 0.69 (95% 0.57-0.83) against the post's 0.40-0.65. | can't tell | A hypothetical, one-off windfall of a month's income, stated intention, 12-month horizon: bears on the ordering of the post's MPC gradient (who spends more of a windfall), not on the level or the exact slope of an MPC out of a permanent flow. |
| Fed DFA, corporate equities and mutual fund shares | SCF family income percentiles (unequivalized), households | 2019Q4-2026Q2 | Equity holdings rose $32.9tn from 2022Q3 to 2026Q2; the top 20% by income got 88% of it (80-99: 46%, 99-100: 43%). | yes | Wealth, not spending. After 2022Q3 the group split is the DFA's model extrapolation (SCF 2025 not yet in); for directly held stocks and funds SCF 2025 gives the top 20% a similar share. |
| Wealth-effect bound (assumption: 2-5 cents per dollar per year, the post's range) | DFA income groups; SCF 2025 or BEA-BLS 2023 spending shares as denominators | 2022Q3-2025Q2, 2022Q3-2026Q2 | Implied top 20% minus bottom 80% spending gap from equity revaluation gains, SCF denominators: 3.2 to 7.9 pts by 2025Q2 (5.6 at 3.5 cents), 5.1 to 12.8 by 2026Q2; BEA-BLS denominators: 4.2 to 10.4 and 6.7 to 16.7. CE shows +1.0 (+2.5 excluding pensions and contributions). | can't tell | An assumption-driven bound, not a measurement: uniform propensity across groups (likely too high for the top 1%), no lags, gains include 2026 and only revaluations count. The post's footnote 31 and Fig 0 give 2-5 cents, its body text 3-5; Figs 8-10 use 3.5. |
| Fingerprint test (sibling unit, NOTES_fingerprint.md) | dPCE (spending) and CE (income) category market shares | 2023-09 to 2026-09 | No K beyond the calm-period norm in the category composition of national-accounts spending. | can't tell | Low power: alone it cannot rule out a K of Zandi's size. |
| Moody's estimates (press reports: top 10% about half of spending) | not published | 2025 | Not used: method and data are not public, so the figure cannot be checked or put on a footing. | can't tell | Not data in the sense used here. |

### What it means, in plain words

The official numbers do not show the K Zandi describes, but they cannot rule out one confined to the very top, and
most of them stop before his window starts.

**Spending.** The data that reach into 2025 point one way. In the CE, which ranks households by pre-tax income, the
top fifth's real spending grew about as fast as everyone else's from 2022 to 2025. That is a one-point difference,
with a sampling error of a little under three, against Zandi's twelve and a half. Its share of spending stayed near
39%; his split would have pushed it to about 41.5%. The latest year on its own is too noisy to choose between his
story and none, and the stock-market surge was fastest after it. His own figures do not add up on official shares:
a top fifth at 4% and the rest at 0% average 1.6-1.7% a year, not his 2%. The CE's total does grow at about his 2%,
but with the bottom 80% at 1.7% a year, not zero.

**Income.** Before taxes, BEA's income distribution agrees: through the 2025 nowcast, the bottom 80%'s income grew
slightly faster than the top fifth's. After taxes it does not quite. In 2023 the top fifth's disposable income
outgrew everyone else's by about two and a half points, because its 2022 tax bill had been unusually high. That
stopped in 2024. It is a real, if one-off, tilt in the income that pays for spending, about a third the size Zandi
describes.

**Wealth.** This is where the K is plain. The top fifth by income got almost nine-tenths of the $33 trillion rise
in household stock holdings since late 2022. Apply the post's own 2-5 cents a year to those gains and the top
fifth's spending would have risen 3-8% more than everyone else's by mid-2025 and 5-13% by mid-2026 (4-10% and 7-17%
if the spending shares come from the BEA-BLS joint distribution); the top of those ranges is Zandi's size. But the
spending data don't show it. The way to square them is the very top. The CE barely covers the richest families.
Suppose spending by the top 1-5% surged while the rest of the top fifth spent like everyone else. The CE would miss
the surge, and so would the category test in `NOTES_fingerprint.md`. For Zandi's top-20% numbers to hold that way,
though, the top 1%'s spending would have had to rise about 80 points more than the bottom 80%'s in three years.
That is far beyond even the assumed wealth effect, whichever spending shares are used, as long as the same ones are
used on both sides.

**Saving.** The record is short. Through 2023 the top decile was not saving less than in 2019; the bottom 80% were
spending further beyond their income by 2022, a little less so in 2023. Neither series reaches the years Zandi
talks about. Since then only the total is known. The saving rate fell from about 6% in 2023-24 to 3.8% in
September 2026; from March to September the fall in saving paid for 40% of the rise in spending. Both stories fit
that: rich households saving less because their portfolios grew, and stretched households running down savings.
The size of the drop matches the low end of the post's wealth-effect range, not its center.

**The post's MPC gradient.** The new SCF question supports the ordering the post assumes: the bottom spends more of
a windfall than the top, by a ratio near the flatter end of the post's range (0.6-0.7 for the top decile, 0.5-0.6
for the top 1%). It says little about the slope and does not support the level: households say they would spend
only about a quarter of a one-off windfall. That is a different thing from spending out of a permanent income gain.

**Measurement limits to keep in view.**

- The official spending distributions end in 2023 (dPCE, joint distribution), except the CE (2025) and the SCF (a
  single 2025 cross-section with 2024 income).
- The CE under-covers the very top.
- The DFA's split after 2022Q3 is modelled.
- The 2025 income figures are an experimental nowcast of pre-tax income; the disposable-income distribution ends
  in 2024.
- Moody's distributional numbers are not public data and are not used.

## Caveats

- **CE coverage of the top.** There is no oversample. Nonresponse and under-reporting rise with income, and income
  is top-coded in the public files (not used here). Even after BLS's adjustments and imputations, CE spending covers
  0.74-0.78 of comparable PCE (BLS dPCE methods page, Table 3.1, 2019-2023). A K confined to the top few percent
  could hide from the CE. Section 2 sizes what it would take.
- **CE 2025.** It was collected through the Oct-Nov 2025 funding lapse: BLS reweighted Interview months and
  doubled Diary weights for September and December. Variances are Fay's BRR, not comparable with earlier years'
  SEs. A sample redesign moved some MSAs in or out. In 2022-2023 RSE >= 25% cells are suppressed; two quintile cells
  needed here are filled from the all-CU identity (exact up to rounding).
- **Approximate SEs.** The CE SEs treat group means and years as independent. For real growth, each end's relative
  SE comes from the deflated aggregate and is scaled by the real growth factor. Adjacent years share some Interview
  CUs, so the SE of a one-year change is overstated; windows of two or more years have no overlap. The SCF SEs are
  a naive family bootstrap.
- **The CE deflator.** ISPCEPX is the only group price index used. It has PCE scope, it is ranked by equivalized DPI
  rather than the CE's income before taxes, its 2024 weights are imputed, and 2025 is carried by the aggregate
  index. Its group indexes differ by only about 0.1 point a year over 2019-2024, so the choice of deflator moves the
  top-against-bottom gaps little, though no index on CE baskets by income group is available here to check that.
- **Vintages.**
  - dPCE: NIPA of 2024-09.
  - Joint distribution: 2026-05 workbook; its 2023 DPI is $59bn lower and PCE $61bn higher than the current vintage.
  - PI, DPI and tax distribution: June 2026; 2024 PI total $137bn below today's.
  - NIPA saving rate and PCE: 2026-10-29.
  - Mixing them is avoided except where noted: the wealth-effect denominators combine current PCE with
    distributional shares.
- **Rankings.**
  - CE: income before taxes per CU, unequivalized.
  - dPCE: equivalized spending.
  - Joint: equivalized DPI per household.
  - PI distribution: equivalized PI per household; DPI distribution: equivalized DPI per household (each concept is
    also shown under the other ranking, as a check).
  - SCF and DFA: family income, unequivalized.
  - ISPCEPX: deciles of equivalized DPI, applied to CE income groups.
  - No level is compared across rankings without saying so. The trend comparisons are within a source.
- **DFA.**
  - The post-2022Q3 split is modelled.
  - Equities exclude DC pensions, so the bottom groups' indirect equity is understated (see the SCF EQUITY row).
  - The revaluation share is the aggregate HH+NPO ratio applied to every group.
  - The wealth-effect bound assumes one propensity for all groups. The literature's estimates (Chodorow-Reich, Nenov
    and Simsek 2021, among those the post cites) are averages, and applying them to the top 1% gives implausible
    spending responses.
- **Zandi's window** is "the past say three years" as of July 2026: mid-2023 to mid-2026. The CE covers it to
  December 2025, the SCF to the 2025 interview, the PI nowcast to 2025, the DPI distribution to 2024. Nothing
  distributional covers 2026.

## Judgment calls

1. **Main SCF ranking.** For the section 1 top shares it is family income in 2024 (INCOME), as the brief asks;
   usual income (the Bulletin's ranking) is reported beside it and used for the publisher checks. For the windfall
   it is usual income, because the windfall is defined on usual income and it is the publisher's ranking; 2024
   income is reported too.
2. **CE top quintile 2014-2018** comes from deciles d09+d10, because Table 1101 is vendored from 2019. In 2019-2025
   the two agree within 0.01 point.
3. **CE "excluding pensions and contributions"** leaves out personal insurance and pensions (mostly Social Security
   and pension contributions) and cash contributions. These are saving or transfers rather than consumption, and
   they are concentrated at the top.
4. **CE real values.** ISPCEPX of the same rank is used for each CE group, with its PCE scope and imputed 2024
   weights (Caveats). 2025 is carried by the aggregate PCE price index, with no differential inflation assumed for
   2025.
5. **CE "SCF-like scope"** subtracts owned and rented dwellings, personal insurance and pensions, and cash
   contributions. The SCF question's treatment of property taxes and home upkeep is not stated.
6. **Zandi's split** is taken as 4% against 0% real a year, a cumulative gap of 1.04^T - 1, starting from the 2022
   (three-year) or 2023 (two-year) shares. The nominal version adds each side's ISPCEPX inflation.
7. **Joint distribution.** Quintiles and the bottom 80% are sums of decile shares times totals. The chart shows it
   from 2004, the years BEA's page says the statistics are provided for; all years are in the CSV.
8. **Wealth-effect bound.**
   - The gain counted is revaluations (Z.1 revaluation share), with level changes and net worth as alternatives.
   - The denominators are SCF 2025 spending shares (same ranking as the DFA), with BEA-BLS 2023 PCE shares as the
     alternative; the brief quotes both.
   - Two windows: to 2025Q2, aligned with CE 2022-2025, and to 2026Q2, the latest.
   - The saving cross-check uses the gains since the 2023-2024 average.
9. **Hand-to-mouth.** The FEDS Note definition is the main one, so the regression-adjusted figures can be compared;
   the KVW-style poor/wealthy split is a variant with a monthly pay period.
10. **The hidden-top arithmetic** uses SCF 2025 shares for the hidden group and the CE's top-quintile gap for the
    rest of the top fifth. That is an approximation, since the CE's top quintile contains some of the hidden group.
    Set against the wealth-effect bound, it uses the same spending shares on both sides (SCF for both, or BEA-BLS
    for both).
11. **Two Fed pages fetched.** Both were fetched through `common.fetch()`: the FEDS Note and its accessible version.
    They are the publisher's analysis of a question asked for the first time, needed to check the tabulation. No
    other download was made.
12. **Income concept.** Both are reported, each ranked by itself: pre-tax PI by equivalized PI (the only concept
    with a 2025 nowcast) and DPI by equivalized DPI (the income spending is paid from, to 2024). Each concept under
    the other's ranking is a check on the ranking.

## Files

| File | What |
|---|---|
| `code/direct.py` | Everything: loads, the six sections, charts and the generated tables (`# %%` cells) |
| `checks/check_direct.py` | 76 PASS/FAIL checks: publisher figures (CE release, dPCE, joint, BEA PI and nowcast, ISPCEPX, NIPA, SCF Bulletin Box 1, FEDS Note tables, DFA, the post's parameters), identities recomputed independently (including the real-growth SEs, DPI and taxes, SCF equity shares by wealth, the hidden-top comparison), notes and figures |
| `out/direct_top_shares.csv` | Top 1/5/10/20% shares by source and year, with ranking, equivalization, unit, scope and top-tail treatment; CE approximate SEs and the CE variants |
| `out/direct_ce_groups.csv` | CE quintiles and deciles 2019-2025: levels (nominal and real, both concepts), growth over seven windows with approximate SEs (nominal and real), top-vs-rest gaps, Zandi's implied share and his arithmetic, budget composition |
| `out/direct_income_saving.csv` | PI and DPI by quintile 2019-2025 (levels, growth), each under both rankings; taxes by DPI group 2019-2024; joint-distribution saving and PCE/DPI by DPI group 2019-2023; the saving rate (monthly 2015-2026, annual) |
| `out/direct_dfa_wealth.csv` | DFA levels by income group, gains over three windows, Z.1 revaluation shares, the wealth-effect bound by group and denominator, implied gaps, SCF-vs-DFA concentration (SCF also by wealth), the timing of the run-up |
| `out/direct_scf2025_spending.csv` | SCF 2025 non-housing spending by income, usual income and wealth groups, with the Bulletin's figures |
| `out/direct_scf2025_windfall.csv` | Windfall allocations by 15 groupings with bootstrap SEs and the publisher's figures; the gradient against the post |
| `out/direct_evidence_table.csv` | The evidence summary (section 6) |
| `out/direct_notes_tables.md` | The tables above as generated (check C1 fails if NOTES drifts from them) |
| `figures/fig_direct_top_shares.png` | Top 10% and top 20% shares by source, 2000-2025, with CE under Zandi's split |
| `figures/fig_direct_dfa_equity.png` | DFA equity holdings by income group, and the wealth-effect bound by group |
| `figures/fig_direct_windfall.png` | SCF 2025 windfall allocations by usual income, liquidity and hand-to-mouth status |

## Corrections after the independent check (2026-11-02)

`checks/verify_independent_direct.py` re-derived this unit from the raw files by a separate route (105 of 113
claims OK). Its corrections are applied above. Three of them weaken a conclusion:

1. **Income.** The brief said the income side has no K. That holds for pre-tax personal income only. Disposable
   income, now added, tilted to the top by 2.5 points from 2022 to 2024, all of it in 2023, through taxes.
2. **Saving.** The joint-distribution saving rows were scored "no" (top) and "yes" (bottom 80%) against Zandi. They
   end in 2023, before the saving behaviour he describes, and are now "can't tell". The dated facts stand.
3. **Zandi's 90%.** The notes said it fits a ranking by wealth. It fits directly held stocks and funds ranked by
   wealth (SCF 2025 91.6%, DFA 88.0%). For the direct-plus-indirect holdings he described, the top 10% hold 81.5%
   by wealth and 70.8% by income.

One makes the spending result a little firmer. The approximate SEs of real growth had scaled the relative SE by the
nominal growth factor instead of the real one, which overstated them by 2-23% (more over longer windows, as prices
rose more). The 2022-2025 top-20 against bottom-80 gap now has an SE of 2.8 (was 3.1), the top-10 against bottom-90
gap 4.1 (was 4.5). The latest single year still fits both stories (+1.9, SE 2.7, against Zandi's +4.0).

Other changes:

- The evidence table's PCE figure is now computed: calendar-2025 PCE, $20.87tn (it was a typed $20.5tn).
- Both sets of wealth-effect ranges are quoted (SCF and BEA-BLS denominators), along with the post's two
  statements of its propensity.
- New: Zandi's own arithmetic, the like-with-like hidden-top comparison, the timing of the equity run-up and the
  CE's 2023 gap.
- Stated or relabelled: ISPCEPX's scope and imputed 2024 weights, NNRESRE in the KVW list, the hidden-top per-year
  column, the SCF-like scope's denominator, the PI rounding variant, the liquidity bins for nonpositive income,
  the bootstrap interval's method and the top-1% family count.
