# Exploration: youth school

Explore half only (16 countries), 2026-10-08, after the P freeze. Written from the explorer's structured return
(the harness did not let the explorer write this file). Exploratory: every estimate here was chosen along a path
of many tries (46 specifications by this explorer).

**Scope as the explorer stated it.** youth, schooling and youth unemployment (explore half, 16 countries). findings.md was NOT written: the harness refused a .md report file from a subagent, so the findings are only in this output, in results/explore_youth_school.json and in the figures. Every regression has country and year fixed effects and the C3 break dummies of its own series, with the restricted WCR (Webb weights, B=9999), one-sided, on 16 clusters (15 where F_c is used, because HR has no F_c). One bug in my own helper was caught and fixed: break dummies were first taken from every series in the frame, not only those in the regression. All numbers here come from the corrected run; P1 (gapU on F x post) went from p=0.028 to p=0.36. The S1 replica of C-6 now reproduces specs_explore.json exactly.

## Findings

### Q1 is answered no. Where coresidence is high, young people's non-employment is not more often inactivity than unemployment: not across countries, not within countries over time, and not in how the young absorb the cycle. (solid)

**Evidence.** Cross-section (2015-19 means; xsec_2015_2019.csv, fig_neet_split_vs_coresidence.png): the share of NEETs aged 20-24 who are inactive correlates -0.25 with coresidence at 18-24 and -0.11 at 25-34. The unemployed NEET share of 20-24-year-olds correlates +0.45 with coresidence at 25-34. Examples, as share of 25-34 living with parents and share of NEETs 20-24 inactive: HR 59.8% and 40%; PT 45.5% and 37%; IT 50.2% and 54%; FI 4.8% and 57%; SE 5.9% and 59%. BG is the exception at 76% inactive. Within countries (N1): b=-0.06 per point of coresidence at 18-24, p(+)=0.62; at 25-29 (N1b), b=+0.13, p=0.15. Cycle by F_c: U15-29 on U25-54 x F gives b=+0.14, p(-)=0.75 (C2); inactivity 25-29 on U x F gives p(+)=0.62 (C3). The q x F versions on the NEET split (N2, N6, N7) are all null.

**Model reading.** The model does not sign the split (P4 was dropped), so the null removes nothing from it. It goes against the 'conditionality composition' reading (a family floor shows up as inactivity, a state floor as unemployment) as a description of these countries.

### Enrolment at 20-24 rises with LAST year's prime-age unemployment. The contemporaneous C-6 relation is weak. (suggestive)

**Evidence.** S10 (fig_E1_partial.png): b=0.454 pp per pp of U25-54(t-1), se 0.170, p=0.004, n=217, G=16, G*=8.2. With country trends (S12): 0.37, p=0.028. On 2010-2019 alone (S14): 0.47, p=0.006. Leaving out any one country: b from 0.37 to 0.51, p at most 0.027 (loo_school.json). In a horse race with contemporaneous U (S13), the lag keeps 0.45 and the contemporaneous term goes to about 0. The C-6 replica (S1) gives 0.29, p=0.061; on the long window with lfsa_urgan (S2), 0.26, p=0.11; with trends (S4), 0.08, p=0.37. Using lfsa_urgan, lagged (S11): 0.37, p=0.045.

**Model reading.** Consistent with school as a paid exit priced against the entrant's prospects (derivations P8). Not distinctive: standard human-capital theory predicts countercyclical enrolment too.

### Lagged youth employment as the prospects measure is partly mechanical, because enrolment is persistent. (solid)

**Evidence.** S3: educ2024 on E2024(t-1) gives -0.32, p=0.012. Holding last year's enrolment fixed (S9) halves it to -0.11, p=0.052. Lagged E25-54 (S8) gives -0.008, p=0.50.

**Model reading.** Not used for E. Prime-age unemployment is the cleaner proxy, as the derivations say.

### The enrolment response to the cycle is largest where unemployment moved least. F_c cannot be told apart from a concave response. (weak)

**Evidence.** Country-by-country slopes of enrolment on U25-54(t-1), without year effects (enrol_cycle_by_country.csv, fig_enrol_cycle_by_country.png): CH 4.6, LU 3.2, BE 2.3, FR 1.9, SE 1.9; IE -0.05, LV 0.10, PT 0.08, HR 0.39, BG -0.99. Spearman correlation with F_raw: -0.55. The pooled interaction U(t-1) x F (C1) is -0.65, p(-) about 0.05, but F correlates with the size of the unemployment swings.

**Model reading.** The floor and school could be competing exits, but nothing here separates that from nonlinearity. No E is drawn.

### Enrolment shows no relation to rents q, on its own or with any moderator available. (suggestive)

**Evidence.** S7: educ on log q(t-1) gives -4.96, se 5.6, p(-)=0.26, MDE15 14.7. S6: q x F_c gives -1.2, se 9.5, MDE15 25. S15: q x a rebuilt student-independence measure from the extras gives se 39 and cannot be used.

**Model reading.** The model-specific part of P8 (school as an exit priced by q where students live independently) cannot be tested from the manifest; see data problems.

### Q3: there is no sign since 2023 that entrants lost ground differentially, whether by clerical exposure or by floor availability. The apparent widening of the youth-prime employment gap in high-coresidence countries is prime-age catch-up. (suggestive)

**Evidence.** Exposure gap (OC4 share at 15-24 minus at 15-64, 2018-19) x post: gapU p=0.48, educ p=0.22, gapE p(-)=0.80, not-employed-not-in-education p=0.72 (X1-X4). MT dominates the gap (11.6 pp; G*=2.4); without MT the results are the same. F x post (P1-P6): all p>=0.15. Event study (fig_event_F.png): the gapE x F coefficients fall steadily from 4.4 in 2012 to 2.3 in 2019 and -1.5 in 2025 (base 2022), a pre-trend. From 2016-19 to 2023-25, the change in E25-54 correlates +0.71 with F, while the change in E20-24 correlates 0.00. BG gap: -42.5 in 2019, -51.0 in 2025; HR -33.5 to -43.1; IT -38.7 to -44.1 (post2023_changes.csv, fig_post2023_vs_F.png).

**Model reading.** C-4's null on the explore half extends to the other moderators and outcomes. Three post years cannot separate an entrant shock from trends.

### Youth unemployment relative to prime-age unemployment has risen on average since 2019, before generative AI. After the cycle is accounted for, it was above its 2012-19 relation in 2024-25. (weak)

**Evidence.** Mean U15-29/U25-54: 2.00 (2016-18), 2.11 (2019), 2.21 (2022), 2.24 (2023), 2.29 (2024), 2.31 (2025). The residual of gapU from a 2012-19 fit on U25-54 with country intercepts is +0.20 (2022), +0.32, +0.63, +0.73 (2025), positive in 14 of 16 countries for 2023-25. Residuals of +0.3 also occurred in 2012-14 (common_shift.json, fig_common_shift.png).

**Model reading.** Consistent with entrants holding the most contestable tasks, but the rise starts in 2019, and a common year shift is not identified against other common shocks. Not testable as an E with year fixed effects.

### The floor-kink equation (D1's) on employment at 20-24 has the model's sign but is weak and trend-fragile. (weak)

**Evidence.** N3: E2024 on log q(t-1) x F_c, with log q and U: b2=-8.44, se 6.01, p=0.069, n=229, G=15. All residents (K2): -8.85, p=0.048. Men (K3): -8.1, p=0.059. Women (K4): -8.8, p=0.11. Long window with UL (N5): -7.6, p=0.11. With country trends (K1): -0.68, p=0.44. Leaving out one country: b from -5.2 to -11.4, p from 0.03 to 0.15. Activity at 25-29 (N4): -0.3, p=0.48.

**Model reading.** The distinctive prediction (the standard account says b2>=0), but the estimate is about half the MDE on 15 clusters and disappears with country trends.

## Data problems

- The C-6 secondary's moderator is mislabelled in the frozen pipeline. ilc_lvps09 is the DISTRIBUTION of young people living with their parents by economic status: EDUC + EMP_FT + EMP_PT + UNE + INAC_OTH = 100 in every country-year checked (e.g. FI 18-24, 2015-19: 54.6+15.5+7.1+12.3+10.5). It is not the share of students living with their parents. So build.py's student_indep = 1 - EDUC/100 is the non-student share of coresiding 18-24-year-olds, and C6.student_independence on the explore half (+131.5, p(-)=0.996) cannot be read as the registered hypothesis. The intended measure needs the coresidence rate and the enrolment rate at 18-24, and neither is in the manifest. An approximation from the extras (coresidence 18-24 x EDUC share / education rate 20-24) gives values above 100% for BE, FR, IT, LU, MT, PT. Correcting it would change a no-verdict secondary's content, so it is the orchestrator's call under PROTOCOL section 7.
- MT: lfsa_ergan NAT employment at 20-24 (M and F) is missing from 2021 on. LU 2025 is flagged u. Both drop out of post-2022 youth employment comparisons (C-4 runs on 15 countries' post data).
- HR has no ilc_lvps08 value before 2010, so it has no F_c and drops from every F-moderated test (G=15).
- une_rt_a starts in 2009 for 14 of the 16 countries (FR 2003, SE 2005), so E1, which uses lagged U25-54 under the C7 rule, runs on 2010-2025 for those countries.
- The manifest holds no activity rate below 25 (lfsa_argan starts at 25-29), no enrolment outside 20-24, and no NEET split. Youth inactivity and NEET composition can be studied only from the extras, never in an E.
- The clerical exposure gap is dominated by MT (11.6 pp, against at most 5.2 elsewhere), which gives G* = 2.4 for any exposure-moderated youth test.
- findings.md could not be written: the harness refused a report-style .md file from this subagent. The content is in this output; the figures, CSVs and results/explore_youth_school.json were written.

## Candidate E-hypotheses and their vetting

### E1 — kept by the vetter (score 4/10)

The share of 20-24-year-olds in formal education rises when prime-age unemployment was high the previous year.

- Model link: Derivations P8: school is a paid exit whose value rises against work when the entrant's prospects fall; prospects are measured by prime-age unemployment from the previous year. A standard human-capital model predicts the same sign (countercyclical enrolment), so this is a consistency check, not evidence for the floor mechanism.
- Varies: C-6 (the same outcome, fixed effects and breaks; the regressor U25-54 lagged one year)
- Explore estimate: beta=0.454, CR1 se=0.170, WCR one-sided p=0.0040 (B=9999), n=217, G=16 (G*=8.2). Leave-one-out: beta 0.37-0.51, p at most 0.027. With country trends: 0.366, p=0.028.
- Variants tried: 9
- Vetter's problems: The estimate doesn't match the statement. The candidate says the 2022 row uses 2021's U, but S10 was run on the frozen panel's U2554, which already has 2020-21 removed. So the lag of 2022 is missing, and every country's 2022 row was dropped (n=217). My check: 'excl 2022' reproduces 0.4541 / n=217 exactly. The stated version has the lag taken on the full annual grid, which is how build.py lags q (C2: 'lags and leads are taken on the full annual grid first'). Built from the manifest raw frames (une Y25-54 for all 16 explore countries under C7's rule, une_lfs never used), it gives beta=0.415, CR1 se=0.165, WCR one-sided p=0.0058 (B=9999), n=233, G=16, G*=8.2. The robustness the explorer quoted belongs to the 217-row sample. On the stated version, country trends give 0.260, p=0.095, not 0.366, p=0.028.; Part of the gain over C-6 comes from the sample, not the lag. C-6 on the explore half gives 0.292 (p=0.061, n=248). The same contemporaneous regression on E1's 217-row sample gives 0.384 (p=0.038); on the stated 233-row sample, 0.321 (p=0.048). Dropping the 2009 and 2022 rows by itself moves C-6 most of the way. In a horse race the lag beats U_t (0.454, p=0.084, se 0.33 with U_t in), but the two are highly collinear and the data can't cleanly separate them.; The effect is identified from the 2010-2013 crisis years. Excluding 2008-2013: stated version 0.107 (p=0.33); explorer's sample 0.239 (p=0.165). Using 2014-2025 only: 0.239 (p=0.165). Outside the euro-crisis rise in unemployment there is almost no signal on the explore half. On the confirm half the test will also mostly be a test of the crisis years.; The result depends on the break dummies. With no C3 breaks: 0.177 (p=0.31). With only the 2021/22 redesign breaks: 0.321 (p=0.11). With all breaks except 2021/22: 0.372 (p=0.0065). The pre-2021 national breaks (for example BG 2010/2011, PL 2010, CH 2010 in U and educ) coincide with the crisis years. C3 is mechanical and frozen, so this is allowed, but it is fragile.; Within-country slopes (FE-demeaned, no breaks; descriptive) vary widely: BE 3.9, PL 3.5, HU 2.2 against IE -1.9, LU -1.3, BG -0.9, FR -0.8. Leave-one-out holds on the stated version (beta 0.34-0.47, max p 0.036, worst when EE or HU is left out). Leave-two-out (-EE,-HU) gives p=0.07 on the explorer's sample.; Forking paths. S10 was the 10th educ2024 regression in specs_log.jsonl. Before it came S1-S5, S8, S9 (cycle measures: U2554, UL2554, E2024_l1, E2554_l1, trends variants, a persistence diagnostic) and S6, S7 (q). Robustness S11-S14 and C1 followed it. The claim of '9 variants' is roughly honest. With about 9 correlated tries, the selected p of 0.004 is still at most about 0.04 after a crude Bonferroni.; It is close to a rescue of C-6. C-6 came in at p=0.061 on the explore half, and E1 re-specifies its regressor timing after that was seen. The model link overstates the theory: derivations P8 attaches 'of the previous year' most naturally to the 20-24 employment ratio, which needs a lag because it is mechanically tied to enrolment, not to prime-age unemployment. C-6 was frozen with contemporaneous U. The lag is defensible on timing (enrolment decisions are made before the academic year), but it was chosen from the data.; It is not distinctive. Countercyclical enrolment is standard human-capital theory (Betts-McFarland; Dellas-Sakellaris), as the candidate admits. It cannot move the model-level verdict, and it overlaps heavily with C-6, which is tested anyway on the full sample and on the confirm half. Its marginal information is only whether the response is lagged.; Timing placebo passes. The lead U_{t+1} alone gives 0.14 (p=0.25). With U_{t-1} included, the lead goes to 0.05 while U_{t-1} stays at 0.43 (p=0.033). So this is not a common trend. A second lag (U_{t-2}) alone is 0.42 (p=0.054), so the response is persistent rather than sharply one-year.
- Vetter's power note: At the explore se of 0.165 on 15 clusters (t with 14 df), the MDE at 80% power is 0.43 for alpha=0.05, 0.50 for alpha=0.025 and 0.58 for alpha=0.01. Under Holm, the first E is tested at 0.01 when five are frozen. The explore estimate (0.415) was selected and is identified mostly from 2010-2013. A plausible true effect is about 0.3, near the unselected C-6 estimate on the common sample. Power at 0.3 is about 53% (alpha 0.05), 40% (0.025) and 25% (0.01); at 0.415 it is 77%, 65% and 48%; at 0.2, 31%, 20% and 11%. Expect roughly 25-50% power in practice. This assumes the confirm-half se is similar, and I did not inspect the confirm data. The vet ran about 60 diagnostic regressions (leave-one-out, leave-two-out, windows, breaks, leads and lags), none logged as candidates. Scripts: explore/_vet/e1_school_vet.py, e1_school_vet2.py, e1_school_vet3.py; output in explore/_vet/e1_school_vet.json and e1_school_vet2.json.

### E2 — dropped by the vetter (score 2/10)

Where the parental home is a widely used exit, employment at 20-24 responds less (or negatively) to rents: the floor kink at the age most likely to be at the floor.

- Model link: Section 7 eq. (exit) with s = max(s0 - q h_e, s_under): at the dependency floor, s is flat in q and q only taxes working while living independently, so the youth q-slope shrinks to zero or below where F is high (derivations, P4 revision and the conflict with P1). The standard concave income-effect model predicts b2 >= 0. Distinctive, but WEAK and LOW POWER: offer it only if the E family has room, since it costs Holm power.
- Varies: D1 (the outcome is employment 20-24, NAT, mean of M and F, instead of activity 25-34)
- Explore estimate: b2=-8.44, CR1 se=6.01, WCR one-sided p=0.069, n=229, G=15 (G*=8.5). With country trends: -0.68, p=0.44. Leave-one-out: -5.2 to -11.4.
- Variants tried: 7
- Vetter's problems: It rescues a failed P. E2 is the frozen D1 equation with only the outcome changed, from A2534 to E2024. Frozen D1 on the explore half has the wrong sign: b2 = +2.02, p(-) = 0.65 (results/specs_explore.json). Activity at 25-29 (N4) is also null: -0.32, p = 0.48. E2 is the one youth outcome in the q x F family that came out with the predicted sign.; Forking paths. The explorer's '7 variants' counts only the N3/K1-K4 line. Counting every q x F regression on an outcome they logged (N2-N7, K1-K4, S6, S15) gives about 12, out of 43 specifications in specs_log.jsonl, plus frozen D1. The best of roughly six outcomes giving one-sided p = 0.069 is what chance alone would produce. The p < 0.10 results K2 and K3 are the same regression with all residents or men only, so they are not independent support.; The lead check fails, and this alone kills it. With q_{t+1} x F added (the frozen 'lead' robustness), the lagged q x F coefficient falls to -2.86 (p = 0.36). The lead x F is -8.02 (se 4.04, two-sided p = 0.096), as large as the original lag effect. Future rents 'predict' youth employment as well as past rents do. That points to a slow differential trend in high-F countries, not a response to q.; It does not survive trend controls. Country linear trends give -0.68 (p = 0.46; the explorer reported the same), F x year fixed effects give -4.01 (p = 0.34), F x linear trend gives -3.54 (p = 0.32), and dropping 2008-2013 gives -3.66 (p = 0.30). The identifying variation is the crisis and recovery path of the high-F countries (BG, PT, IT, MT, PL).; It does not hold across q measures. HPI gives -1.62 (p = 0.22), CP00 gives -5.43 (p = 0.19), and rent over compensation per employee gives +9.00, the wrong sign (p(-) = 0.80). Long differences: -27 with se 30.; It depends on a few countries. Leave-one-out p rises above 0.10 without BG (0.151), PT (0.146), SE (0.142) or FI (0.101). In leave-two-out, a third of all pairs push p above 0.10, and dropping PT+SE or BG+SE leaves about -2.6 (p of about 0.28). Under the protocol's own qualifier the explore result already 'rests on one country'. Country-by-country slopes are scattered: BE -46, BG -48, PT -35, LU +76, MT +30, which is noise, not a dose-response in F.; Mismatch with the outcome and the mechanism. The floor kink is about participation; E2024 is employment, and at 20-24 school enrolment dominates it. School is an exit in its own right (C-6), so a negative q x F on employment could come from enrolment or unemployment, which the paper's model does not separate. Activity 20-24 is not in the manifest (act starts at 25-29), so the participation version cannot be computed from the frozen manifest.; Distinctiveness is weak. Besides the concave income-effect model (b2 >= 0), standard mobility-friction or spatial-mismatch accounts also predict that rents depress youth employment where youth live at home. A negative b2 would not single out the dependency-floor kink.; Underpowered. MDE on 15 clusters is 15.8, about twice the explore estimate, and that estimate is inflated by selection (winner's curse). Power is about 25-30% at one-sided 0.05 and about 10% at Holm's first step of 0.01 among five E-hypotheses. The 15-cluster sample also loses HR, which has no F_c.
- Vetter's power note: Explore half: b2 = -8.44, CR1 se 6.01, WCR one-sided p = 0.069, n = 229, G = 15 (HR has no F_c), G* = 8.5. MDE on 15 clusters (inf.mde, alpha 0.05 one-sided, 80% power) = 15.8 points per unit of log q x sd(F), about 1.9 times the estimate. If the true effect equals the explore estimate, power is about 25-30% at 0.05 and about 10% at Holm's first step of 0.01. Selection bias means the true effect is probably smaller. With country trends the se rises to 6.7 (MDE 17.6). My vetting ran 1 replication, frozen D1, 8 frozen robustness variants, 15 leave-one-out runs, 105 leave-two-out runs (B=499), F x year fixed effects, F x trend and per-country slopes. Script: C:\Users\s6068C\GitHub\laborformal\participation\explore\_vet\vet_ys_e2.py; output: C:\Users\s6068C\GitHub\laborformal\participation\explore\_vet\vet_ys_e2.json.

## Files

- `results/explore_youth_school.json`
- `explore/youth_school/specs_log.jsonl`
- `explore/youth_school/common.py`
- `explore/youth_school/youth.py`
- `explore/youth_school/s02_describe.py`
- `explore/youth_school/s05_school.py`
- `explore/youth_school/s06_school2.py`
- `explore/youth_school/s07_post2023.py`
- `explore/youth_school/s08_event.py`
- `explore/youth_school/s09_common_shift.py`
- `explore/youth_school/s10_floor_youth.py`
- `explore/youth_school/s11_school_robust.py`
- `explore/youth_school/s12_exposure_gap.py`
- `explore/youth_school/s13_cycle_by_floor.py`
- `explore/youth_school/s14_country_slopes.py`
- `explore/youth_school/s15_kink2024.py`
- `explore/youth_school/s16_figs.py`
- `explore/youth_school/s17_results.py`
- `explore/youth_school/fig_E1_partial.png`
- `explore/youth_school/fig_enrol_cycle_by_country.png`
- `explore/youth_school/fig_neet_split_vs_coresidence.png`
- `explore/youth_school/fig_event_F.png`
- `explore/youth_school/fig_post2023_vs_F.png`
- `explore/youth_school/fig_common_shift.png`
- `explore/youth_school/fig_ts_emp_educ_U.png`
- `explore/youth_school/xsec_2015_2019.csv`
- `explore/youth_school/post2023_changes.csv`
- `explore/youth_school/enrol_cycle_by_country.csv`
- `explore/youth_school/loo_school.json`
- `explore/youth_school/common_shift.json`
