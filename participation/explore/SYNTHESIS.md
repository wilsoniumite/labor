# What the explore half says about participation

Synthesis of the five explorations and their vetting, written 2026-10-08 after the P freeze and before the E freeze.

**Scope.** These results cover 16 countries only: BE BG CH EE FI FR HR HU IE IT LU LV MT PL PT SE. They are
exploratory. The other 15 countries were not looked at. Every regression has at most 16 clusters (15 when F_c is
needed, because HR has no coresidence value before 2010). The effective number of clusters G* is often 3-6. Every
p-value below was chosen from a path of many tries, so the explore estimates are upper bounds on what a fresh sample
will show.

**Forking paths.** The five explorers estimated about 293 specifications in all:

| Theme | Specifications |
|---|---|
| women and men | 61 |
| aging and retirement | 52 |
| youth and school | 46 |
| housing and the floor | 120 |
| occupations | 14 |

The vetters ran several hundred more checks (scripts in `explore/_vet/`). The synthesis estimated 17 specifications
(the three shortlisted E and their no-verdict robustness runs) and 46 leave-one-out reruns, all fixed by the vetting
before they were run.

**Where the outputs are.** The explorers' own findings.md files could not be written (the harness refused them), so
their write-ups live in `results/explore_<theme>.json`, with scripts and figures in `explore/<theme>/`.

Strength labels:
- **solid**: holds across specifications and is mostly descriptive;
- **suggestive**: right sign and plausible, but fragile, or one reading among several;
- **weak**: rests on one choice, one country or one bloc, or fails a placebo.

## 1. Read through the model

The paper's comparison is `w + m_w >= s(q) + m_e`, with `s(q) = max(s0 - q h_e, s_under)`. The model's distinctive
piece is the floor kink. Where the parental home is the exit, a rise in rents stops pushing the young into work. The
standard income-effect account predicts the opposite. On the explore half:

- **The frozen tests are all inconclusive, and the model-level verdict is inconclusive** (`results/specs_explore.json`).
  - D1 (the kink across countries): +2.0 (se 5.2, p 0.65), the wrong sign.
  - D2 (the kink over time): +2.1 (se 2.7).
  - C-3 (second earners): both legs wrong-signed: women minus men -6.1, women -6.3.
  - C-6 (school as a paid exit): +0.29, p 0.061. It is the closest to the predicted sign.
- **The floor kink's sign appears only once country-specific linear trends are added.** That is a choice of
  identifying assumption, not a robust feature of the data (section 6). It is the main candidate for an E.
- **What does show up is what standard models also predict:**
  - women's participation converging on men's;
  - older participation rising after the pension reforms;
  - enrolment rising after high unemployment;
  - the young holding more clerical jobs.

  None of these separates the model from the standard account.
- **The model-specific pieces cannot be tested from the frozen manifest:**
  - school priced by q where students live independently (the ilc_lvps09 measure is mislabelled; section 7);
  - the AI-era entrant shock (no ISCO 2-digit by age; one usable pre-year).

## 2. Women and men

| Claim | Strength |
|---|---|
| Women's prime-age (25-54) participation rose in every explore country, and the gap with men narrowed sharply. Equal-weight means, nationals: women 76.0 (2005), 82.7 (2019), 86.8 (2025); men 90.8, 91.7, 92.0. The gap went from -14.8 to -5.2, and its cross-country sd fell from 13.4 to 3.9. The change in the gap from 2005 to 2025 regressed on its 2005 level has slope -0.59 (se 0.13, 13 countries; MT is the extreme point). Widest gaps in 2025: IT -17.0, IE -8.5, PL -7.4, BG -7.3. Narrowest: EE -0.8, FI -1.9, PT -2.5. | solid |
| By age, the gap is smallest at 25-29 (-4.8 in 2022-25), dips at 30-39 (about -7) and is widest at 60-64 (-11.2). It narrowed most at 50-59, by about 11 points from 2005-08 to 2022-25. | solid |
| Women's prime-age participation falls, not rises, with q within countries: C-3 legs -6.1 and -6.3 on 2003/2009-2025; -9.1 (se 7.2) on the long window 1997-2025. Catch-up drives this: the change in women's activity 2006-2019 correlates -0.86 with its 2006 level and -0.29 with the change in log q. MT, LU, IT and BE started low with flat q; the CEE countries started high with rising q. With country trends the slope is -2.6 (se 1.5). | suggestive |
| The q-response of women's participation is lower where older people own outright: -5.1 per sd, p 0.036, with trends only. Without trends it is +2.6. A plain CEE dummy does better as the moderator (-8.7). Within the 10 non-CEE countries it is +3.3. The lead q(t+1) has the opposite sign. Men show the same sign. This is a bloc contrast, not a tenure gradient. | weak |
| The women-minus-men gap widens when prime-age unemployment rises: +0.23 pp per pp (p 0.019, G* 11.1, lfsa_urgan, 1997-2025). In levels, men leave (-0.19) and women do not enter (+0.04). In first differences the pattern reverses: men do not move (+0.00) and women enter (+0.11). The gap estimate falls to +0.11 with HICP breaks and to +0.07 on 2005-2016. Which sex moves cannot be identified from this design. | suggestive |
| Men's inactivity at 25-29 rose from 10.2% (2005-08) to 12.0% (2022-25), up in 12 of 15 countries. The largest falls in activity were BE -5.9, FI -5.0, IT -4.3 and HR -3.0. At 45-54 men's inactivity fell. The rise at 25-29 tracks NEET inactivity (cross-country correlation -0.81), not schooling (-0.50) or coresidence (-0.09). Within countries, men's 25-29 activity does not move with their coresidence (b -0.013, se 0.030; outside the manifest). | suggestive |
| Care-related inactivity (FAM_CARE) is a small and falling share of women's inactivity: IT 5.5% of women 25-54 in 2008 to 3.1% in 2024; PL 5.0 to 2.1. It does not move with q or the cycle. | weak (outside the manifest) |

**Model reading.** Sex is not a primitive of the model. The convergence is the standard story (Goldin; the
end of the brawn premium). For the q tests it is a confound: within countries, women's catch-up runs against
Balassa-Samuelson q convergence. App B (the second earner housed by the household) makes the sign of the q-response
follow the household's net housing position. Most prime-age households in these countries own, so a non-positive
average slope is consistent with the model. C-3's unconditional positive sign is not implied by it.

## 3. Aging and retirement

| Claim | Strength |
|---|---|
| Activity at 55-64 rose in every explore country, mostly after 2009. At 60-64 the rise was about the same for women as for men. Women 60-64: 26.0 (2005), 29.3 (2009), 46.6 (2019), 57.5 (2025), 12 countries. Men 60-64: 37.9, 41.0, 58.0, 68.1. HU men 60-64 went from 21.2 to 75.6 and HU women from 9.8 to 46.5. BE women 60-64 went from 9.8 to 44.5. Exceptions: PL women 60-64 only 13.6 to 27.9; LU men 60-64 fell from 22.1 (2009) to 13.7 (2019). | solid |
| The rise was largest where 55-64 activity started lowest: 2009-19 change on the 2009 level -0.33 (se 0.09, p 0.006, 15 countries). HU, MT, PL, IT, BE and FR gained 17-28 points; SE and CH 6-7. As a description this is solid. As a retirement-margin finding it is not. Cohorts with higher participation (largely women) reaching 55-64 account for the whole effect (-0.63). Within-cohort exit does not converge (+0.31). The result also depends on the scale: it disappears in log(100-A). It is weaker with LU included, and LU is missing only because one 2009 cell is flagged u. | solid (descriptive) / weak (as retirement) |
| Older participation does not respond to q or to house prices within countries. A5564 on log q -5.0 (se 5.9); on log(HPI/CP00) -0.6 (se 4.1). All eight sex x age x price-measure estimates lie between -14 and +4.5, none with two-sided p below 0.12. IE (42%) and EE (24%) carry most of the identifying variation in q (G* 3.3). | suggestive |
| The old-minus-prime activity gap rises with house prices more where outright ownership at 55-64 is high: +6.2, p 0.026. That is the opposite of the net-long prediction. The predicted sign was registered after the result was seen. Without SE the p is 0.215. The lead fits as well as the lag. | weak |
| The 2012 ad hoc module (outside the manifest) splits the countries into two groups. In MT (87%), BG (80%), HU (66%) and PL (58%), people aged 50-69 who left work mostly left at pension eligibility. In EE (38.5% vs 12.7%) and PT (37.0% vs 13.6%), own health was the larger reason. 'Favourable financial arrangements' was highest in IE (16.8%), SE (12.8%) and BE (11.9%). | suggestive |
| Population aging is not related to the routine-job decline. C-5 gives -0.57 (MDE 48). Countries that aged faster (BG, HR, LV, PT) lost fewer routine jobs (0.6-3 points) than those that barely aged (LU, MT, SE, CH: 4-7 points). Realised aging mostly measures migration. | suggestive |

**Model reading.** A fall in the exit payment m_e (higher pension ages, closed early-exit routes) raises
participation at 55-64. This is the Gruber-Wise reading. It does not separate the model from the standard account,
and the P7 pension test was dropped for want of a pension-age table. There is no sign of the net-long income effect
at older ages. The derivations' wage pass-through term pushes the other way, and the data cannot separate the two.

## 4. Schooling and youth unemployment

| Claim | Strength |
|---|---|
| Enrolment at 20-24 rises with LAST year's prime-age unemployment: +0.415 pp per pp (se 0.165, p 0.006, 16 countries, 2004/2010-2025). With current-year U held fixed, the coefficient on current U is -0.09. The frozen C-6 (contemporaneous U) gives +0.29, p 0.061. The lagged effect is identified mostly from the 2010-13 crisis: excluding 2008-2013 it falls to +0.11 (p 0.33). With country trends it is +0.26 (p 0.095). The lead U(t+1) does not take it over (lag +0.38 with the lead held). | suggestive |
| Where coresidence is high, youth non-employment is not more often inactivity than unemployment. The share of NEETs aged 20-24 who are inactive correlates -0.25 with coresidence at 18-24 (HR 59.8% coresident and 40% inactive; FI 4.8% and 57%; SE 5.9% and 59%; BG the exception at 76% inactive). Nothing shows within countries or in the cyclical response either. This goes against the 'family floor = inactivity, state floor = unemployment' reading of the conditionality appendix. The model does not sign the split; that is why P4 was dropped. | solid (outside the manifest) |
| Enrolment shows no relation to q: -5.0 (se 5.6). The model-specific part of P8 (school priced by q where students live independently) cannot be tested, because the manifest's student measure is mislabelled (section 7). | suggestive |
| Since 2023 there is no sign that entrants have lost ground differentially, whether by clerical exposure or by floor availability. The apparent widening of the youth-prime employment gap in high-coresidence countries (BG -42.5 to -51.0; HR -33.5 to -43.1; IT -38.7 to -44.1, 2019 to 2025) is prime-age catch-up with a pre-trend from 2012. | suggestive |
| Youth unemployment relative to prime-age unemployment has risen since 2019: mean U15-29/U25-54 was 2.00 (2016-18), 2.11 (2019), 2.29 (2024) and 2.31 (2025). After allowing for the cycle, the ratio was above its 2012-19 relation in 14 of 16 countries in 2023-25. The rise starts before generative AI, and a common shift cannot be identified against other common shocks. | weak |
| The floor kink on employment at 20-24 has the model's sign: -8.4, p 0.069. It is about half the MDE. It goes to -0.7 with country trends and to -2.9 with the lead held. | weak |

**Model reading.** Countercyclical enrolment fits school as a paid exit priced against the entrant's prospects
(derivations P8). Standard human-capital theory predicts the same. The pieces of P8 that would set the model apart are
untestable with the frozen data.

## 5. Occupations and entrants

| Claim | Strength |
|---|---|
| The young hold more of the clerical stretch. The clerical (OC4) share at 15-24 exceeds the share at 25-64 in 12 of 15 countries, 2011-19 means: MT +7.4, CH +5.8, PL +4.0, LV +3.5, EE +3.0, LU +3.0; but BE -2.5, IT -1.5, IE -0.8, and FI and FR about zero. Stacked test: +2.08 pp, p 0.009, G* 13.9. Leaving out any one country, the p stays at or below 0.018. | solid |
| The young's routine-job excess is craft work (OC7, apprenticeships: CH +11.4, BE +6.0), not operators and assemblers (OC8: mean -0.4). | suggestive |
| The 2011-19 routine decline happened within age groups, mostly at 25-64 (CH -5.2, MT -4.2, SE -4.1 points). Over the 2010s the young's clerical share relative to older workers rose (+0.055 log points, up in 11 of 15). | suggestive |
| Since 2023 there is no relative loss of young clerical jobs. The within-occupation log ratio from 2022 to 2023-25 is -0.008 (se 0.043, 14 countries). The design could have detected a fall of about 10%. | suggestive (a null in a short window) |
| The frozen C-4 rests on CH alone (G* 1.8; CH 74% of the identifying variation). MT has no nationals employment at 20-24 after 2020. The 2021 break is flagged in 15 of 16 countries, which leaves only 2022 as a pre-year. C-4's null comes from the design and is not evidence against the model. | solid |

**Model reading.** 'The entrant is the young clerk' (the eras section) holds on average as a mapping fact and is
the premise of C-4. Standard entry-job-ladder accounts share it.

## 6. Housing and the floor

| Claim | Strength |
|---|---|
| q is mostly a common upward trend. Rise in log q from the first year to 2025: BG +1.71, PL +1.37, IE +1.35, LV +1.05 ... IT +0.10, LU +0.09. The residual sd after two-way FE is 0.10-0.13. The within-country variation comes from a few volatile countries (BG EE HR IE LV). | solid |
| CP041 is a weak rent measure where rental markets are small. Market renters among 25-34s: HR 3%, MT 4%, BG 7%, PL 8% (SE 50%, CH 76%). BG's CP041 behaves like an indexed price (correlation 0.91 with compensation, a +0.93 log jump in 1998). | solid |
| The long window does not rescue D1 or D2. With lfsa_urgan U from 1997, D1 is +3.3 (p 0.71) and D2 +3.3. The 2009 start costs observations, not the sign. | solid |
| With country linear trends, D1's b2 has the model's sign: -6.1 (se 3.2, p 0.028, 15 countries, 1997-2025, G* 6.4). Leaving out any one country, the p stays at or below 0.063. The implied slope is +5.5 at the 25th percentile of F and -5.5 at the 75th. It holds in all residents (-4.0) and with quadratic trends (-5.2). Caveats: the sign is set by the trend term (+3.3 without trends on the same rows). The signal sits in 2013-2025 (-4.7), not in the boom and bust (+0.2 on 1997-2012). The goods-price leg (-7.5) carries at least as much as the rent leg (-4.3). It is a contrast between the high-F CEE and South blocs and the rest. It was the one sign-changing choice among about 11 structural D1 forks. | suggestive |
| D2 does not measure curvature. Because q trends, the squared deviation correlates above 0.88 with a quadratic time trend in 8 of 16 countries, and IE supplies 61% of its identifying variation. | solid |
| Coresidence rises with q more where F is high: +10.4, p 0.008, with trends. With F x year effects it becomes -4.8, so it is one time shape, and it rests on 2022-24, right after the SILC break. | weak |

**Model reading.** Where the floor is rare, q encloses a priced exit (positive slope). Where it is common, q taxes
independent work (negative slope). The trend version of D1 has this shape; the trend-free version does not. Two
readings fit the data:
- (a) the trend-free D1 confounds q with convergence (rising q and rising participation in MT, HU and LU), and the
  trends remove that;
- (b) the trends manufacture a high-F/low-F contrast out of one post-2013 shape.

The explore half cannot tell these apart. The goods-price leg weakens the claim that this is about rents.

## 7. Data problems (for the orchestrator)

1. **C7 window.** une_rt_a starts in 2009 for 14 of 16 countries (FR 2003, SE 2005, CH 2010), so every frozen test
   with U runs on about 2009-2025. lfsa_urgan covers 1995-2025 for all 16. The frozen code does what the rule says,
   so this is not a bug.
2. **C-6 secondary mislabelled (§7 call).** ilc_lvps09 is the distribution of coresiding 18-24-year-olds by status:
   EDUC + EMP_FT + EMP_PT + UNE + INAC_OTH = 100. It is not the share of students who live with their parents. So
   `student_indep` measures the non-student share of coresiding youth, and the frozen secondary (+131.5,
   p_opp 0.996) cannot be read as registered. The intended measure is not in the manifest.
3. **C-5 plumbing (§7 call).** HU's 2011 demo_pjan reports Y_OPEN as 85+ with no single ages 85-99, so
   `build.aging` returns NaN and HU drops out of C-5 silently. A confirm country coded the same way would drop too.
   An open group above 56 holds everything the ratio needs.
4. **The 2021 LFS break.** It is flagged in 15 of 16 countries. Under C3 it absorbs every pre/post-2021 level
   difference, so C-4 and any post-2023 design are identified by 2022 against 2023-25 only.
5. **MT.**
   - Nationals' activity and employment at 20-24 are blank from 2021.
   - There is no 2025 activity value.
   - MT's women's activity rose 33 points from 2005, which dominates the equal-weight descriptives.
6. **HR.** No F_c (SILC starts in 2010). The OC4 cells at 15-24 are flagged u in most years; they are blanked
   selectively, and the blanked gaps are negative.
7. **CP041.** It is administered or indexed in BG and PL, and markets are thin in HR, MT and BG. The 1997-2001 CEE
   jumps are rent liberalisations.
8. **What the manifest lacks.**
   - activity below 25 or above 64;
   - the NEET split;
   - coresidence or unemployment by sex;
   - prime-age tenure;
   - ISCO 2-digit or 20-24 occupation cells.

   The manifest's tenure series (OWN_NL 55-64, 2015-17) is not predetermined.
9. **CR1 in designs with country x year FE.** CR1 counts the fixed-effect dummies in K, which inflates the reported
   se by about 1.5 (E-OCC1). The WCR p is unaffected.
10. **Other series.** lfsa_igar has no retirement category. lfsa_igaww BE has a classification jump in 2024.

## 8. The shortlist of E-hypotheses

Three, not five. Each was kept by its vetter, is computable from the frozen manifest's raw frames, and asks a
distinct question. With three, Holm tests the smallest p at 0.0167, the next at 0.025 and the last at 0.05. The code
is `explore/e_specs_draft.py`, and its run on the explore half reproduces the explore estimates below
(`results/explore_synthesis.json`). Every E reports, with no verdict:
- the leave-one-country-out maximum p, with the protocol's 'rests on one country' rule;
- G*;
- the named robustness runs.

### Rank 1: E-HF1 (varies D1; never changes D1's verdict)

- **Hypothesis:** with country-specific linear trends and one cycle source for every country, the 25-34 participation
  response to q is lower where the parental floor is more available. H1: b2 < 0.
- **Specification.**
  - Outcome: A2534 (C5, nationals).
  - Tested term: log q_{t-1} x F_c (q = CP041/IGD_NNRG; F_c from C9, standardised with confirm.py's 31-country
    constants).
  - Other terms: log q_{t-1}; U = lfsa_urgan Y25-74 sex T citizen TOTAL for every country (one source, no splice).
  - Country FE, year FE, country linear trends ((year-2010)/10), C3 breaks from act, une_lfs and hicp.
  - Years 1997-2025 without 2020-21; UK to 2019.
  - One-sided restricted WCR (Webb, B 9999, CR1), clustered by country.
  - Code: `specs.estimate(cy with U replaced, cl, TESTS['D1'], Ctx(cl, fstd), geos, variant='country_trends')`.
- **Reported, no verdict:**
  - the no-trend form on the same rows;
  - the lead (log q_{t+1} and its F interaction added);
  - the rent/goods decomposition;
  - the frozen U with trends.
- **Explore half:**
  - b -6.09, se 3.21, p 0.028, n 324, G 15, G* 6.4, one-sided 95% CI (-inf, -1.40].
  - Leave-one-out max p 0.063 (LV out).
  - Variants on the way: 27, the one sign-changing choice among about 11 structural forks.
- **MDE on 15 clusters:** 8.4 at 5% (10.4 at 1.67%). Power at the explore estimate is 0.56 at 5% and 0.35 at
  1.67%; at half of it, 0.23 and 0.11.
- **Why it is on the list.** It is the only candidate that speaks to the model against the standard account. It uses
  the long window STATE.md flags (2000s boom and bust, lfsa_urgan for every country). A pass supports D1-with-trends
  only: the decomposition is reported so that a goods-led result is visible.

### Rank 2: E-OCC1 (premise of C-4; varies no P)

- **Hypothesis:** on average across countries, the clerical (ISCO-08 OC4) share of employment is higher at 15-24
  than at 25-64. H1: b > 0.
- **Specification.**
  - Data: lfsa_egais THS_PER, sex T, EMP; C4 applies (u/c cells missing).
  - Two rows per country-year:
    - s_young = 100 x OC4[15-24] / TOTAL[15-24];
    - s_prime = 100 x (OC4[15-64] - OC4[15-24]) / (TOTAL[15-64] - TOTAL[15-24]).
  - Years 2011-2019. A country enters with at least 5 years with both rows.
  - Model: s on young + country x year FE + 1[geo=c, year>=tau] x young for every b flag in 2012-2019 on the four cells.
  - Equal weights.
  - One-sided restricted WCR, clustered by country.
- **Reported, no verdict:**
  - the exact sign-flip test on the country means;
  - the log-share outcome;
  - no break dummies;
  - the 2022-2025 era.
- **Explore half:**
  - b +2.08 pp, se 1.12 (CR1, inflated by the fixed-effect count), p 0.009, n 270, G 15 (HR has under 5 years),
    G* 13.9.
  - Leave-one-out max p 0.018. Sign-flip on the country means: p 0.008.
  - Variants: 4 by the explorer; the 5-year rule was added by the vetter.
- **MDE on 15 clusters, from the dispersion of the country means:** 1.82 at 5% and 2.24 at 1.67%. Power at the
  explore mean of 1.85 is 0.81 and 0.63; at half of it, 0.35 and 0.18.
- **Why it is on the list.** It is the best powered of the three. It tests the mapping the paper states ('the entrant
  is the young clerk') and the premise of C-4's exposure measure. A fail would undercut C-4's reading. It is not
  distinctive.

### Rank 3: E-SCH1 (varies C-6; never changes C-6's verdict)

- **Hypothesis:** the share of 20-24-year-olds in formal education rises with prime-age unemployment of the previous
  year. H1: b > 0.
- **Specification.**
  - Outcome: educ2024 (edat_lfse_19 POP FE Y20-24, sex T).
  - Regressor: U(25-54) under C7's rule (une_rt_a where it covers a country, else lfsa_urgan, one source per country),
    lagged one year on the full annual grid before 2020-21 are dropped. The 2022 row carries 2021's U, and break years
    move one year later.
  - Country and year FE, C3 breaks from educ and the lagged U. No other controls.
  - Years 1997-2025 without 2020-21.
  - One-sided restricted WCR.
- **Reported, no verdict:**
  - country trends;
  - excluding 2008-2013;
  - the lead U_{t+1} held;
  - the horse race with U_t.
- **Explore half:**
  - b +0.415, se 0.165, p 0.006, n 233, G 16, G* 8.2.
  - Leave-one-out max p 0.045.
  - Variants: 9 by the explorer. The vetter corrected the lag so that 2022 is kept; the explorer's 0.454 had dropped
    every 2022 row.
- **MDE on 15 clusters:** 0.45 at 5% and 0.55 at 1.67%. Power at the explore estimate is 0.75 and 0.54; at half of
  it, 0.31 and 0.16.
- **Why it is on the list.** It is a well-identified timing question (decisions are made before the academic year),
  with a passing lead placebo. Two caveats: it is close to a re-specification of C-6 after seeing C-6, and it rests on
  the crisis years.

### Considered and not shortlisted

| Candidate | Why not |
|---|---|
| The long-window D1 without trends (STATE.md's flag) | +3.3 (p 0.71) on the explore half, the wrong sign; its trend form is E-HF1. |
| WM-1 (women, q x outright owners) | A bloc contrast; the lead placebo fails; it rescues C-3. |
| WM-2 (countercyclical sex gap) | No model link; the mechanism flips between levels and first differences; underpowered. |
| E-AR1 (older-participation convergence) | Cohort replacement and scale-dependent; no information on the model. |
| E-AR2 (old-gap x ownership x house prices) | Sign chosen after the result; rests on SE; the lead fails. |
| E2 (employment 20-24 floor kink) | Rescues D1; the lead fails; MDE twice the estimate. |
| E-HF2 (coresidence x F) | Collapses with F x year effects; rests on 2022-24. |
| E-OCC2 (entrants first since 2023) | Null on the explore half; about 10-20% power. It would serve better as a no-verdict descriptive in the 2026-2028 time holdout. |
