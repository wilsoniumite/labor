# Exploration: occupations ai

Explore half only (16 countries), 2026-10-08, after the P freeze. Written from the explorer's structured return
(the harness did not let the explorer write this file). Exploratory: every estimate here was chosen along a path
of many tries (14 specifications by this explorer).

**Scope as the explorer stated it.** Occupations, automation and entrants (lfsa_egais ISCO-08 by age, explore half, 16 clusters). The harness refused to write findings.md ("Subagents should return findings as text"), so the findings are given here only. Figures (PNG), scripts and numbers are in C:\Users\s6068C\GitHub\laborformal\participation\explore\occupations_ai\, and the results file is C:\Users\s6068C\GitHub\laborformal\participation\results\explore_occupations_ai.json. Scripts run in order s02-s08: s02 C-4 anatomy, s03 young/prime share gaps, s04 the AI window, s05 aging and C-5, s06 the candidates, s07 the C-4 figure, s08 descriptive pace. Figures: fig1_young_vs_prime_shares, fig2_relative_clerical_share, fig3_aging_routine, fig4_clerical_gap_by_country, fig5_c4_anatomy. 25-64 is computed as 15-64 minus 15-24, because the manifest holds only those two ages. On the 2015 cells this is within 0.4 points of the direct 25-54 cells.

What country-level data can say: it can establish where entrants sit, and it can rule out large relative movements within an occupation (about 10% over 2-3 years). With manifest series it cannot separate AI from the 2022-23 cycle or from the post-COVID unwinding using cross-country exposure. Clerical exposure is concentrated in two small countries (CH, MT), so G* stays near 2 whatever the outcome. An AI exposure index would need ISCO 2-digit by age (lfsa_egai2d) and 20-24 detail, and neither is in the manifest. The better-powered design compares ages within an occupation in each country, using the country's older workers in the same occupation as control: G* about 14, no dependence on one country, MDE about 0.11 log points. The 2026-2028 time holdout supplies the post years this design most needs.

## Findings

### The young hold more of the clerical stretch: the clerical (OC4) share at 15-24 exceeds the share at 25-64 in 13 of 16 countries. (solid)

**Evidence.** Mean of 2011-2019: +1.8 points (sd 2.6). Largest in MT +7.4, CH +5.8, PL +4.0, LV +3.5, EE +3.0, LU +3.0. Negative in BE -2.5, IT -1.5, IE -0.8. Stacked test (young dummy, country x year FE, young x C3 breaks, clusters = country): +2.05 points, CR1 se 1.08, WCR one-sided p 0.007, G* 14.6. Largest leave-one-out p is 0.017 (CH out). Files: s03_young_gap.py, s06_candidates.py, young_gap.json, fig1, fig4.

**Model reading.** Supports the paper's post-industrial line that the entrant is the young clerk. This is a mapping fact that the standard entry-job-ladder account shares; it is not distinctive. It is C-4's premise.

### The young do not hold more of the operator/assembler jobs (OC8). Their routine excess (OC4+7+8) is mostly craft (OC7), which is apprenticeship-heavy. (suggestive)

**Evidence.** OC8 young minus 25-64, 2011-19: mean -0.4 points, positive in 8 of 15. Routine total: +3.3 points, of which OC7 +2.3 (CH +11.4, BE +6.0). Routine excess is negative in BG, IE, LV. File: young_gap.json.

**Model reading.** The 'assembler' part of the entrant description does not show at country level. Cashiers (OC5) are not in the manifest.

### The 2011-2019 routine decline happened within ages, mostly at 25-64. In the 2010s the young's clerical share relative to older workers rose rather than fell. (suggestive)

**Evidence.** Routine share at 15-64, 2011-19: CH -5.2, MT -4.2, SE -4.1, FI -3.9, IT -3.9, BE -3.5, HU +0.6 points. The between-age (fewer young) part is under 0.35 points everywhere (CH -0.34). log(OC4 share at 15-24 / at 25-64): +0.055 on average from 2011-13 to 2017-19, up in 11 of 15 (MT +0.32, IE +0.20, SE +0.14). Files: s05_aging.py, s08_descriptive.py, fig2, fig3.

**Model reading.** Read as a within-occupation flow claim, 'entrants first' does not describe the 2010s computing-era decline in these countries. Clerical work shrank among 25-64-year-olds at least as fast as among the young.

### Since 2023 there is no relative loss of young clerical jobs. The within-occupation design could have seen about a 10% relative fall. (suggestive)

**Evidence.** R = log(OC4 share 15-24 / OC4 share 25-64). From 2022 to the 2023-25 mean: -0.004 (sd 0.13, 14 countries). With country FE and C3 breaks: -0.008, CR1 se 0.043, one-sided p 0.41, G* 13.8, MDE on 15 clusters 0.11. Leave-one-out p ranges 0.17 (LV out) to 0.62. OC4+OC8 version +0.004; routine version +0.011 (MDE 0.04). Clerical share at 25-64 fell 0.18 points/yr over 2022-25 (0.11/yr over 2016-19), and at 15-24 it fell 0.19 points/yr: young and older are falling at the same pace. Files: s04_ai_window.py, s06_candidates.py, fig2.

**Model reading.** No sign through 2025 of AI acting on the entrant's clerical stretch first. Derivations.md says a null in this window refutes nothing, because of lags, low adoption, and the possibility that AI acts as a substitute for training rather than as gamma_M.

### Frozen C-4 on the explore half rests on CH alone (G* 1.8). MT, the most exposed country, has no nationals employment at 20-24 after 2020. The universal 2021 break leaves only 2022 as a pre-year. (solid)

**Evidence.** Share of identifying variation in X_c x post2023 after FE and breaks (nationals): CH 0.74, FI 0.14, IT 0.03, BG 0.03. CH contributes +0.058 of the +0.060 estimate. With CH left out: -0.013, p 0.48, FI 46% and IT 28% of variation, MDE 0.80. lfsa_ergan MT NAT 20-24 is empty from 2021. With all residents, MT takes 0.56 and CH 0.24 (beta -0.084, RI p 0.11). 15 of 16 countries carry a 2021 b-flag, so country x 1[year>=2021] removes their 2016-19 vs 2022-25 difference; break dummies absorb 62% of the regressor's variation. Raw change in E2024-E2554 from 2022 to 2023-25: HR -7.6, BG -4.0, IT -3.3, MT(all) -3.1, PT +2.5, LU(all) +2.3, BE +1.6, unrelated to X_c. Files: s02_c4_anatomy.py, s07_c4_figure.py, c4_anatomy.json, fig5.

**Model reading.** C-4's null is a property of the design, not evidence against the model. The confirm half will have the same one-pre-year structure.

### C-4's exposure measure (the young's own clerical share) is not the model's measure. The model's exposure gap (young minus 25-64 share) does no better on this design. (suggestive)

**Evidence.** Gap 2018-19: MT 13.0, CH 5.9, LV 4.6, PL 3.7, EE 3.2, SE 3.2 ... BE -1.9. Correlation with X_c is 0.81. C-4 with the gap: +0.21 (wrong sign), p 0.79, G* 5.8, MDE 0.75. With all residents: -0.076, p 0.37. File: s04_specs.json.

**Model reading.** Derivations.md's P5 measure. With 16 countries, cross-country exposure designs stay underpowered whichever measure is used.

### Aging is unrelated to the routine decline at country level, whether measured as the frozen cross-section or as an annual panel. (weak)

**Evidence.** Frozen C-5 explore: -0.57, MDE 48. IE has aging 0.18 and change -0.5; LU 0.25 and -7.0; HR 0.30 and -1.4. Panel of routine share 15-64 on the actual 56+/21-55 ratio with country and year FE and breaks: +12.7 (p 0.99, wrong sign); with U added: +0.4 (p 0.53), MDE 15. The frozen aging_pred (no mortality) correlates 0.44 with the actual 2011-19 change in the ratio. Files: s05_aging.py, fig3.

**Model reading.** Nothing distinguishes the margin account here. The discriminating test needs routine relative wages, which are not in the manifest. No E is proposed.

## Data problems

- lfsa_egais values before 2011 are ISCO-88 based (b flag in 2011 everywhere); only 2011+ is usable as ISCO-08.
- The 2021 LFS break is flagged b in the 15-24 OC4/TOTAL cells and in E2024/E2554/U for 15 of 16 explore countries. Under C3 it absorbs every country's pre/post level difference, so C-4 (and any post-2023 design over 2016-2025) is identified by 2022 versus 2023-25 only.
- MT: lfsa_ergan citizen NAT 20-24 has no values from 2021 on, so MT drops out of C-4's post period under the nationals rule.
- HR: OC4 at 15-24 is flagged u in most years (2012-15, 2019-20, 2023-25). LU: OC4 at 15-24 is u in 2023-25, and OC8 at 15-24 is mostly missing. LV and MT: OC7/OC8 at 15-24 are missing in later years. BG: OC4 at 15-24 is missing in 2020-21. FR: occupation cells are flagged d in 2022-25 with bd in 2021 and 2024.
- HU: demo_pjan 2011 has no single-year cells for ages 85-99, so HU's aging_pred is NaN and HU drops out of C-5.
- The frozen manifest's occupation query holds only sex T and ages 15-24 and 15-64: no 20-24, no 25-54 or 55-64 (25-64 must be computed by subtraction), and no ISCO 2-digit, so no AI exposure index can be built.
- CR1's small-sample factor counts fixed-effect dummies in K. In designs with country x year FE (E-OCC1, 138 dummies) the CR1 se, and hence inf.mde, is inflated by about 1.5. The WCR p is unaffected because the factor cancels in t*/t. The country-mean MDE for E-OCC1 is about 1.8 against 2.9 by the CR1 se.
- C-5's aging_pred assumes no mortality, so it is dominated by the 2011 stock of people aged 48 and over, the very old included. It correlates only 0.44 with the actual 2011-19 change in the ratio of 56+ to 21-55.
- 2019-2022: the clerical share at 25-64 rose 0.37 points on average (BE +1.7, PT +1.4, EE +1.2, PL +1.1, IT +0.9). This is COVID composition plus the 2021 break, so 2022 is an elevated base for any post-2023 clerical decline.

## Candidate E-hypotheses and their vetting

### E-OCC1 — kept by the vetter (score 4/10)

Entrants hold the clerical stretch: in each country, the clerical (ISCO-08 OC4) share of employment is higher at 15-24 than at 25-64.

- Model link: Eras section, post-industrial configuration ('the entrant is the young clerk, cashier, or assembler'); it is the premise of C-4's exposure measure. A standard entry-job-ladder model predicts the same, so this is a mapping check, not a distinctive test.
- Varies: none (tests the premise of C-4, not C-4 itself)
- Explore estimate: beta +2.05 pp, CR1 se 1.08, WCR one-sided p 0.0073 (16 clusters), n 276 country-year-age rows, G 16, G* 14.6; leave-one-out p max 0.017 (CH out)
- Variants tried: 4
- Vetter's problems: The statement is false as written. 'In each country' fails in 3 of the 16 explore countries: BE -2.46, IT -1.47 and IE -0.80 pp (2011-19 means), and FI +0.03 and FR +0.14 are about zero. The regression tests the cross-country average gap, so the statement must say 'on average across countries'. A per-country reading would need an intersection-union test, which would fail.; Forking is low but not zero. The explorer reports 4 E-OCC1 variants (2011-25, 2011-19, routine 4+7+8, no breaks) plus about 10 earlier OC specs in s04/s05 on the same table. All the OC4 variants agree: beta 1.83 to 2.05, WCR p 0.0071 to 0.0073. My own checks add 5 estimates: the 2022-25 era alone (+2.37, p 0.011), the log ratio (+0.192, p 0.0047), an exact sign-flip on country means (p 0.0063), drop-top-k, and a min-years rule. None reverses the sign. The OC4-only choice is anchored by C-4's frozen exposure definition, not picked from the data. The paper's own entrant list, though, is 'clerk, cashier, or assembler' (OC4, part of OC5, OC8). The OC8 gap is mixed (negative in BG, CH, EE, IE, LV), so this E checks only the 'clerk' leg of that sentence.; Concentration: no single country drives it (LOO max p 0.017, CH out), but the effect is heterogeneous. The sd of the country means is 2.60 against a mean of 1.80, and MT (+7.4) and CH (+5.8) are the two largest. Dropping both gives a mean of 1.11 (t 2.18); dropping the top 3 gives t 1.79.; C4 selection bias, mechanical and upward. HR's young OC4 cells are flagged u in 2011-15 and 2019, and the blanked raw gaps are negative (-1.8, -1.4, -1.4, +0.1, -2.6, -2.9). Only HR's 3 positive-ish years survive (mean +1.06). Since 'u' depends on the absolute cell count, a small country's low young clerical counts get blanked, which selects against negative gaps. The effect on the explore estimate is tiny (HR carries 3 of 138 country-years), but it can recur in small confirm countries. Fix: a country enters only with at least 5 of the 9 years. In the explore half this drops HR, and the mean pp gap becomes 1.85 (t 2.67, n 15).; Using break dummies for a level hypothesis is arbitrary. 1[c, t>=tau] x young throws away a country's post-break segment rather than correcting it. Flags in 2012-19 (BE17, BG19, FR13/14, HU18, IE17, IT18, LU15, PL19, SE18) move beta from 1.83 (no breaks) to 2.05. The universal 2021 flag discards all of 2022-25, which is why 2011-25 and 2011-19 give identical estimates. Freeze the sample at 2011-2019 explicitly. The 2011 flags at the start of the ISCO-08 series carry no dummy.; The reported MDE is misleading. The CR1 se of 1.08 is inflated about 1.5x because K counts the 138 country-year dummies; the bootstrap-t p is unaffected because the scaling cancels. Report the MDE from the dispersion of the country means instead.; The model link is real but weak. The eras figure is explicitly 'interpretive' in the paper, the sentence concerns the post-industrial era as a whole rather than 2011-19, and the explorer concedes that a standard entry-job-ladder model predicts the same. derivations.md (C-4 entry) says the right exposure is the entrant-minus-prime exposure gap, not the level C-4 uses. So E-OCC1 supports the idea behind 'entrants first' but does not validate C-4's frozen X_c, which is the 15-24 level.; Not distinctive, and close to a known descriptive fact. A pass adds almost nothing on the model against the standard account. A fail would mainly undercut the interpretation of C-4 (already inconclusive on the explore half), which is the main reason to spend a slot on it.
- Vetter's power note: The explore half has 16 clusters: beta +2.05 pp (no breaks +1.83), WCR one-sided p 0.0073, exact sign-flip on the country means p 0.0063.

On 15 confirm clusters the MDE (80% power, t with 14 df) comes from the sd of the country means, 2.60 pp:
- 1.76 pp at alpha 0.05;
- 2.27 pp at the Holm second step (0.0125);
- 2.34 pp at the Holm first step (0.01).

If the explore mean of 1.80 is the truth, power is about 0.82 at 0.05 but only about 0.54 at 0.01. If the confirm-half effect is half that, power is 0.36 and 0.13. So the test is adequately powered only if it ends up first in the Holm order with a large margin, and the heterogeneity across countries (3 of 16 negative) makes that uncertain.

The log-ratio outcome is less exposed to CH and MT (mean 0.188, sd 0.239, t 3.15; MDE 0.16 at 0.05 and 0.22 at 0.01). It was computed after the pp outcome, though, so switching to it would be a fork; keep it as robustness unless the orchestrator prefers it on prior grounds (E-OCC2 already uses this R). The explorer's 2.94 pp MDE from the CR1 se is inflated by the count of the 138 fixed-effect dummies and should not be reported.

### E-OCC2 — dropped by the vetter (score 3/10)

Entrants first in the AI window: from 2023 the young's clerical share falls relative to the 25-64 clerical share in the same country (log ratio lower in 2023-25 than in 2022).

- Model link: derivations.md P5: if AI raises machine capability on the entrant's contestable stretch, entrants are hit before trained workers behind the wall. This is the within-occupation, country-level analogue of the canaries design. Standard hiring-margin and insider-outsider models predict the same sign, so it is not distinctive. A null refutes nothing (lags, adoption, and AI possibly substituting for training).
- Varies: C-4 (same question; a within-occupation age contrast replaces cross-country clerical exposure; never changes C-4's verdict)
- Explore estimate: beta -0.0084 log points, CR1 se 0.043, WCR one-sided p 0.41 (14 clusters with data; HR and LU lack post cells), n 56, G* 13.8; leave-one-out p ranges 0.17 (LV out) to 0.62. Explore does NOT support it.
- Variants tried: 7
- Vetter's problems: The explore half gives no support at all. The estimate is beta -0.0084 (CR1 se 0.043, WCR one-sided p 0.415, 14 clusters) and the median country change is +0.010. The per-country changes from 2022 to the 2023-25 mean split 5 negative (FI -0.25, HU -0.15, MT -0.14, IE -0.10, PT -0.06) against 9 zero or positive (LV +0.27, EE +0.14, BG +0.10). As an E, a hypothesis the data are supposed to suggest, it is a pre-registered hope rather than a finding. Reproduced exactly in explore/_vet/vet_eocc2.py.; Leave-out checks find no hidden signal. Leave-one-out p runs from 0.17 (LV out) to 0.62. The lowest leave-two-out p is 0.07 (EE and LV out); the highest is 0.76. The explore null is not the work of one country, and any rejection on the confirm half would be new evidence, not a replication.; Power is too low for a Holm slot. The MDE on 15 clusters is 0.109 at alpha 0.05, but 0.145 at Holm's first step (0.01 with 5 E). At the explore attrition rate (2 of 16 countries lost to u-flagged youth OC4 cells: HR, LU), about 13 confirm clusters remain, giving 0.118 at 0.05 and 0.159 at 0.01. Plausible effects are smaller: the outcome covers all of ISCO group 4 (not only AI-exposed 2-digit groups), ages 15-24 including teenagers, and annual averages with only 1-3 post years. Power against a 0.03-0.05 log-point effect is roughly 10-20%. Keeping it tightens the Holm thresholds for the other E.; The base is a single post-COVID year. The 2021 IESS break flag sits on the OC4/TOTAL cells of nearly every explore country, so C3's dummy 1[year>=2021] absorbs every pre-2021 year. Bases 2019+2022 and 2016-19+2022 give the identical beta (-0.0084); the effective base is 2022 alone. In 2022 the youth clerical cells were at a rebound high in several countries (FR 227, IT 143, FI 20.4, IE 28.4 thousand). Mean reversion from that year favours the predicted sign without any AI.; No year effects and no control group: every country is treated, so the test is a before-after on one base year. Any common 2023-25 shift in where the young sit, such as the youth-cyclical rate shock or the shift of young workers into hospitality after COVID, loads onto beta. The derivations note for P5 lists exactly these confounds. The pre-AI placebo windows (base b, post b+1..b+3, for b = 2011-2016) are reassuring on calibration (mean beta -0.001, sd 0.040, about the reported se), but they are only 6 draws.; The pre-trend runs against the sign. Within countries, R rose about +0.009 per year over 2011-19 (pooled slope p(positive) 0.056). A continuing trend biases the before-after toward zero or positive and lowers power further. Adjusting for the trend (2015-19 slopes extrapolated across the 2021 break and COVID) gives -0.061 with p 0.107. That is my own extra fork, fragile, and not a basis for re-specifying.; Small cells are noisy. The young clerical cells are a few thousand people in EE, LV, MT and BG (EE swings 0.38 to 0.65 to 0.28 to 0.62 from year to year), and with equal country weights the smallest countries dominate the variance. The confirm half also contains small countries, so expect similar noise; no confirm values were consulted for this.; The model link is real but weak. derivations.md (P5) says the model's first-order prediction concerns the ENTRY WAGE, that employment responds only second-order through participation, and that the right exposure is the 20-24 versus 25-54 gap from 2-digit or 3-digit occupation mixes. None of that is in the manifest: this design uses 15-24, a whole ISCO group, and occupation shares. The sign is not distinctive (hiring margin, insider-outsider and seniority models predict the same), and a null refutes nothing (lags, adoption, the novice-biased or training-substitute sign risk). Neither outcome moves the model against the standard account.; Forking paths are not the problem, since nothing significant was selected: the explorer counts 7 variants on the way (OC4, OC4+8 and routine R versions in s04; with and without breaks; with and without singleton countries). I ran 106 more specifications, including the placebo-window and leave-two-out loops; all are null or wrong-signed. The placebo occupations also show nothing: OC7 +0.019 (p 0.78) and OC8 +0.031 (p 0.73).; Partly a re-design of C-4. Its motivation is C-4's degenerate exposure design (G* about 2.6, carried by CH and MT), and it is correctly labelled as varying C-4. It is not a dressed-up rescue of a significant failure: C-4 is inconclusive, and the new design is null on explore too.; Computability is fine. It needs only the manifest's occ frame (lfsa_egais THS_PER, sex T, Y15-24 and Y15-64, OC4 and TOTAL). 25-64 = 15-64 minus 15-24 is exact, and rounding error is about 1% of the smallest cells, well below sampling noise.
- Vetter's power note: The explore se is 0.043 on 14 clusters, which scales to 0.0445 on 15. MDE on 15 clusters: 0.109 log points at alpha 0.05 with 80% power, 0.125 at 0.025, 0.140 at 0.0125, and 0.145 at Holm's first step (0.01). At the explore attrition rate (2 of 16 countries lost to u-flagged young OC4 cells), about 13 confirm clusters remain: MDE 0.118 at 0.05 and 0.159 at 0.01. The pre-AI placebo windows have a beta sd of 0.040, so the se is about right. A realistic effect for all of ISCO 4 at ages 15-24 in 2023-25 is a few hundredths of a log point, which gives roughly 10-20% power. The upward pre-trend of R (+0.009 per year) biases the before-after toward zero and lowers power further.

## Files

- `results/explore_occupations_ai.json`
- `explore/occupations_ai/s00_load.py`
- `explore/occupations_ai/s01_shares.py`
- `explore/occupations_ai/s02_c4_anatomy.py`
- `explore/occupations_ai/s03_young_gap.py`
- `explore/occupations_ai/s04_ai_window.py`
- `explore/occupations_ai/s05_aging.py`
- `explore/occupations_ai/s06_candidates.py`
- `explore/occupations_ai/s07_c4_figure.py`
- `explore/occupations_ai/s08_descriptive.py`
- `explore/occupations_ai/c4_anatomy.json`
- `explore/occupations_ai/young_gap.json`
- `explore/occupations_ai/s04_specs.json`
- `explore/occupations_ai/s05_specs.json`
- `explore/occupations_ai/s06_specs.json`
- `explore/occupations_ai/shares_T.csv`
- `explore/occupations_ai/gap_young_minus_2564.csv`
- `explore/occupations_ai/descriptive_clerical_pace.csv`
- `explore/occupations_ai/fig1_young_vs_prime_shares.png`
- `explore/occupations_ai/fig2_relative_clerical_share.png`
- `explore/occupations_ai/fig3_aging_routine.png`
- `explore/occupations_ai/fig4_clerical_gap_by_country.png`
- `explore/occupations_ai/fig5_c4_anatomy.png`
