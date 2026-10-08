# Exploration: women men

Explore half only (16 countries), 2026-10-08, after the P freeze. Written from the explorer's structured return
(the harness did not let the explorer write this file). Exploratory: every estimate here was chosen along a path
of many tries (61 specifications by this explorer).

**Scope as the explorer stated it.** women_men: prime-age and age-specific participation by sex on the 16 explore countries; how women's participation moves with rents, the cycle and care, plus men's prime-age non-participation. Note: the harness refused to write findings.md ("Subagents should return findings as text"), so the full write-up is in these findings. Scripts, figures, the spec ledger and results/explore_women_men.json are written. Read the findings with this in mind: there are 16 clusters, G* is often 3-6, and series marked (X) are outside the frozen manifest (used for understanding only).

## Findings

### Women's prime-age participation rose in every explore country, and the gap with men converged strongly. (solid)

**Evidence.** Equal-weight means for 25-54, nationals: women 76.0 (2005), 82.7 (2019), 86.8 (2025); men 90.8, 91.7, 92.0. The gap went from -14.8 to -5.2. Women's trend 2005-2025 averaged +5.5 pp per decade, from FI +1.1 and LV +1.3 to LU +9.6 and MT +26 (2005-19). Regressing the change in the gap 2005-2025 on its 2005 level gives slope -0.59 (se 0.13, r -0.81, n 13; MT, at -55 in 2005, is the extreme point). The cross-country sd of the gap fell from 13.4 (2005) to 10.1 (2010), 5.5 (2019) and 3.9 (2025). Widest gaps in 2025: IT -17.0, IE -8.5, PL -7.4, BG -7.3. Narrowest: EE -0.8, FI -1.9, PT -2.5. Files: explore/women_men/s01_levels.py, s01_levels.csv, fig01, fig02.

**Model reading.** Sex is not a primitive of the model; standard accounts (Goldin's U, the brawn story) explain the secular rise and the convergence. Their importance here is as a confound: within-country q tests pick up the catch-up.

### By age, the gap is smallest at 25-29 and widest at 60-64, with a child-rearing dip at 30-39. It narrowed at every age, most at 50-59. (solid)

**Evidence.** Means over countries (composition varies). 2022-25: gap -4.8 at 25-29, about -7 at 30-39, -11.2 at 60-64. 2005-08 to 2022-25, the gap narrowed by about 11 pp at 50-59. Men 60-64 activity rose from 39.5 to 61.5 and women's from 25.4 to 50.3. Files: s01_levels.py, fig03_age_profile_gap.png.

**Model reading.** The older-age rise reflects pension reforms (no pension control is available). The model has nothing sex-specific to say about it.

### Men's prime-age inactivity rose at the young end (25-34) and fell at the old end (45-54). The young-end rise tracks rising NEET inactivity more than schooling. Young men's activity does not move with their coresidence within countries. (suggestive)

**Evidence.** 2005-08 to 2022-25, 15 countries. Men's inactivity at 25-29 went from 10.2 to 12.0% (rising in 12 of 15), at 30-34 from 5.9 to 7.0, at 45-49 from 9.8 to 7.4, at 50-54 from 14.5 to 10.2. The largest falls in activity at 25-29 were BE -5.9, FI -5.0, IT -4.3, HR -3.0 and FR -2.8; it rose only in HU +2.4, PL +0.7 and BG +0.5. Changes among men 25-29 (X): education +2.0, NEET-inactive +0.8, coresidence +3.6. Across countries, the change in activity correlates -0.81 with the change in NEET inactivity, -0.50 with education and -0.09 with coresidence. Women 25-29: NEET-inactive -5.8, coresidence +6.6. Within countries (X, FE): men 25-29 activity on men's coresidence b=-0.013 (se 0.030); men 25-34 b=0.000 (se 0.035). Across countries in 2017-19, men's coresidence at 25-34 correlates -0.21 with their activity and +0.54 with NEET inactivity. Files: s05_care_cores.py, s06_young_men.py, fig08.

**Model reading.** This fits a goods-rich, space-poor exit at the parental floor in levels. But nothing links it within countries, and the cross-country correlation has the same composition and reverse-causality problems that led to dropping the original P4. For young women, the shrinking NEET-inactive share alongside rising coresidence suggests the household-supplied exit (a partner's home) arrives later. The model does not sign this.

### On the explore half, women's prime-age participation falls with q within countries. The frozen C-3 legs are negative, and catch-up drives most of it. (suggestive)

**Evidence.** Frozen C3a (W-M) -6.1 (se 4.4) and C3b (W) -6.3 (se 4.7), n 245, G* 3.3. Over the long window 1997-2025 with the lfsa_urgan cycle: W -9.1 (se 7.2), M +1.4 (se 1.5). Every women's age band is negative (25-34 -7.9, 35-44 -11.4, 45-54 -8.0). Long changes: the change in women's activity 2006-2019 correlates -0.86 with its 2006 level and -0.29 with the change in log q 2005-2019. MT, LU, IT and BE had flat q and started low; CEE countries started high and had rising q. With country linear trends, women's slope is -2.6 (se 1.5, p_opp 0.17). Files: s02_rents.py, s02_rents.txt, fig04.

**Model reading.** App B (second earner housed by the household) gives a q effect with the sign of the household's net housing position, and most prime-age households in the explore half own. So a non-positive average slope is consistent with the model, while C-3's unconditional positive sign is not implied. But the dominant force is the convergence-versus-Balassa-Samuelson confound, not housing.

### Second-earner signature: with country trends, women's q-slope is higher where renters dominate and lower where outright owners dominate. It disappears without trends, men show the same sign, and the country-by-country slopes do not line up. (weak)

**Evidence.** Without trends: q x renter share 25-54 (X) -2.6 (se 5.9); q x OWN_NL 55-64 (M) +2.6 (se 5.3). With country trends: q x renter share +5.5 per sd (se 1.9, p 0.022); q x OWN_NL 55-64 -5.1 per sd (se 2.7, p 0.036, G* 5.4). Implied slope at the 10th percentile of ownership (CH, SE) +7.7 (se 5.9); at the 90th -3.9 (se 1.3). Robust to the frozen U (-5.9, p 0.035), no cycle control (-5.4) and 2005+ (-4.9). Leave-one-out max p 0.104 (EE out). Weaker for W-M (-2.5, p 0.15) and for all residents (-2.9, p 0.22); men -2.6 (p 0.11). Country slopes correlate -0.25 with ownership. Files: s03_tenure.py, s03_tenure.txt, s07_candidates.py, s07_candidates.txt, fig05.

**Model reading.** This is the critic's App B reading: the net housing position signs the second earner's response. A standard hedging model predicts the same, and the critic's simulation has the first earner responding too, which matches men's same-signed estimate. It is not distinctive.

### The gap W-M is countercyclical, but through men leaving the labour force rather than women entering: no added-worker effect in the pooled within-country data, including 2005-2016. (suggestive)

**Evidence.** 1997-2025, FE and breaks. W-M on U 25-54 (lfsa_urgan) +0.231 (se 0.111, p 0.019, G* 11.1); men -0.193 (se 0.094, p 0.003); women +0.038 (se 0.146). By band: 25-34 +0.19, 35-44 +0.30, 45-54 +0.21. With the frozen une_rt_a from 2003: +0.40 (p 0.008). With trends: +0.07 (p 0.038). Leave-one-out max p 0.097 (EE out). Window 2005-2016: gap +0.07 (se 0.19), women -0.12. Women on men's U holding women's U (X): +0.45 (se 0.47). Changes 2008-13 where men's U rose most: HR +10.3, PT +9.4, BG +7.9, IE +7.0, IT +5.6. Men's activity there fell by 2.0-3.1, and women's rose in PT +3.1, IE +1.9 and IT +1.0. Files: s04_cycle.py, s04_cycle.txt, fig06.

**Model reading.** The model has no unemployment. Through App B's pooled household, a man out of work can exit into a household his partner funds, so the household is the exit for either earner. The data show men leaving the labour force, which is the standard discouraged-worker pattern. There is nothing distinctive here.

### Care-related inactivity (FAM_CARE / FAM_CARE_PER_OTH) is a small and falling part of women's inactivity. It does not move with q or the cycle. (weak)

**Evidence.** (X) Women 25-54, FAM_CARE_PER_OTH as % of population: IT 5.5 (2008) to 3.1 (2024), PL 5.0 to 2.1, CH 5.5 to 2.7, MT 5.7 to 3.3 (2019), HU 2.3 to 0.6. In 2019, in HU, IE, IT, PL and PT, it is about 11% of the W-M inactivity gap. FE regressions: on q -0.05 (se 1.7); on U -0.04 (se 0.04). Files: s05_care_cores.py, s05_care_cores.txt, fig07.

**Model reading.** Home care is part of the exit's home production. Its decline as participation rises fits care moving from households into the paid human-required sector H. Occupations by sex are not in the manifest, so this cannot be shown.

### The floor kink split by sex shows nothing, and neither do older people's tenure-moderated q-slopes. (weak)

**Evidence.** D1 form (A 25-34 on q, q x F, U): women +4.6 (se 8.4), men -0.6 (se 2.9). Long window: women +7.1, men -0.4. 55-64 on q x OWN_NL 55-64 with trends: women -0.3 (se 2.7), men +6.7 (se 5.5). Files: s07_candidates.txt, s08_older.txt.

**Model reading.** The floor-kink test has no sex dimension that sharpens it.

## Data problems

- findings.md could not be written: the harness blocks report files from subagents. The write-up is in this output.
- MT has no 2025 activity value; IE and HR lack 2005. MT's series starts in 2005, and its +33 pp rise in women's activity dominates cross-country descriptives. The country composition of equal-weight means changes as BG (2001), PL/LV (2004), IT/MT (2005) and HR (2006) enter.
- lfsa_igar by reason is heavily blanked (u/c): men's care cells are almost all missing, and SE and BE have hardly any. It is not in the manifest by sex.
- Tenure by age exists only from 2015. The manifest holds only OWN_NL 55-64 (sex T), so a prime-age renter-share moderator is not available for an E. OWN_NL 55-64 correlates -0.85 with the 25-54 renter share and +0.89 with prime-age outright ownership, and it is not predetermined.
- Coresidence by sex and unemployment by sex are not in the manifest (sex T only), so neither the young men's coresidence link nor an added-worker test on men's unemployment can be an E.
- log q has very large early swings in CEE (log rises of 0.5-1.0 in the late 1990s). Together with women's catch-up, this produces a within-country negative correlation that has nothing to do with housing; country trends are needed.
- une_rt_a starts in 2009 for 14 of the 16 countries, so the frozen tests run on 2003/2009-2025. The manifest's lfsa_urgan (une_lfs) covers 1995-2025 for all 16, and both candidates use it as one source for every country.
- Activity by sex is for nationals. All-residents versions weaken WM-1 (p 0.22) and WM-2 (p 0.086).

## Candidate E-hypotheses and their vetting

### WM-1 — dropped by the vetter (score 2/10)

Women's prime-age participation responds less (more negatively) to rents relative to goods where the older generation mostly owns outright. In the second-earner reading, the q-response follows the household's net housing position.

- Model link: App B as the theory critic derived it (derivations.md, P3): the second earner's exit is housed by the household, so q reaches her only through the household's net position. That is positive where renters dominate and zero or negative where owners dominate. Standard hedging and income-effect models (Sinai-Souleles; unitary household) predict the same sign, so it is not distinctive. Men show the same sign, weaker (-2.6, p 0.11).
- Varies: C-3 (leg 2: women's 25-54 activity on log q). It never changes C-3's verdict.
- Explore estimate: beta -5.12 per sd of O_c; CR1 se 2.73; WCR one-sided p 0.036 (p_opposite 0.965); n 342; G 16; G* 5.4. Leave-one-out max p 0.104 (EE out). Frozen-U variant -5.92 (p 0.035).
- Variants tried: 21
- Vetter's problems: The sign depends on the trend choice. In the protocol's main form (country and year FE, no trends), q x O is +2.61 (se 5.35, p_opp 0.317), the wrong sign. It is -2.51 in 2005-2025 the same way. The candidate only appears with country linear trends, which PROTOCOL section 5 lists as a robustness run, not a main specification. Quadratic country trends weaken it to -3.90 (p 0.122).; Forking paths. s03_tenure.txt shows seven interaction variants tried on women and the W-M gap, with moderators renter share 25-54, outright owners 55-64 and outright owners 25-54, each with and without trends. All five no-trend versions are null or wrong-signed. Only the two trend versions 'work', and they are near-mirror images because corr(RENT_2554, OWNNL5564) = -0.85. The trend spec was chosen after seeing the no-trend nulls. The explorer's whole ledger runs to about 100 estimated specs, and 21 of them came before this candidate. My vetting script added 146 more, B=999 to 9999, all on explore data, listed in explore/_vet/wm1_vet.txt.; It is a regional contrast, not a tenure gradient. Replacing O with a plain CEE dummy (BG EE HR HU LV PL) gives a stronger result: -8.70, p 0.004. A median split of O gives -9.34, p 0.005. Within the 10 non-CEE countries the interaction is +3.31 (wrong sign, p_opp 0.171). Within the 6 CEE countries it is -0.19. With stratum x year FE plus trends it is -0.08 (p 0.48). The 'outright-owner share of the old' is standing in for the post-socialist bloc: 1990s privatisation, Balassa-Samuelson q convergence, regulated or thin rental markets, and the transition dynamics of women's participation. These are the confounds PROTOCOL C6 already flags.; Timing placebo fails. The lead q_{t+1} x O on its own, in place of the lag, has the opposite sign: +3.55, p_opp 0.074. With lead and lag both in, the lag drops to -4.49 (p 0.10). A level effect of persistent q should not flip sign between t-1 and t+1. This looks like a high-frequency artefact of the detrending.; Fragile across samples and measures. All residents instead of nationals: -2.87, p 0.22, half the size. Excluding 2008-2013: p 0.078. 1997-2015: p 0.185. Leave-one-out max p is 0.104 (EE out). Leave-two-out puts p above 0.10 for 10% of pairs, and EE is in nearly all the worst ones (EE-LV p 0.247, EE-HR p 0.239). G* is 5.4.; The age pattern contradicts the second-earner reading. The effect sits in women 25-34 (-9.78, p 0.001), is weak at 35-44 (-5.29, p 0.14) and absent at 45-54 (-0.28). Settled prime-age couples, where the household-pooling mechanism applies, show nothing. Women 25-34 overlap with the floor/coresidence margin of D1 (corr(O, F_raw) = 0.74) and with CEE's tertiary expansion. The effect is also not women-specific: W-M -2.54, p 0.15; men -2.58, p 0.11.; It rescues a failed P. On the explore half, C-3 leg 2 (women 25-54 on q) came out wrong-signed (-6.3, p_opp 0.115). WM-1 recasts this as 'the positive response exists only where renters dominate' (implied slope +7.7 at the 10th percentile of O, p 0.15; -3.9 at the 90th). That is a post-hoc moderator rescuing a failed P.; The theory link is weak and not distinctive. derivations.md P3 says the second earner's response follows the prime-age household's net position, and names the prime-age renter share as the moderator. The manifest has only the 55-64 outright-owner share, a parents'-generation proxy. Linking it to prime-age couples' net position needs an unstated transfer or inheritance step. derivations.md also says P3 'tests only the standard income effect' (unitary household, Sinai-Souleles hedging), so WM-1 cannot discriminate the paper's mechanism from standard models.; O_c is not predetermined: it is measured in 2015-2017, mid-sample, the same flag C-1's secondary carries. The standardisation constants ('over the run's countries') would have to be fixed in advance. Otherwise the confirm-half regressor depends on the confirm half's mix of high- and low-O countries, which again makes it a bloc contrast.; Underpowered. At 15 clusters, using the explore se (2.73 x sqrt(16/15), t with 14 df), the MDE is 7.4 at one-sided 5% and 9.8 at Holm's first-step 1%. The explore point estimate (5.12) is below both, and it is a winner's-curse maximum among variants.
- Vetter's power note: The explore half gives beta -5.12, CR1 se 2.73, G 16, G* 5.4. Scaled to 15 clusters (se about 2.81, t with 14 df), the MDE is 7.4 at one-sided 5% with 80% power, and 9.8 at Holm's first-step 1%. Power to detect a true effect equal to the explore estimate is about 0.52 at 5% and about 0.22 at 1%. At a shrunk true effect of 3 it falls to 0.25 and 0.07. The within-region estimates (-0.08 with stratum x year FE; +3.3 within non-CEE) suggest the true tenure gradient is near zero. The confirm test would mostly measure whether the confirm half's high-O countries happen to share CEE's q and participation trends.

### WM-2 — dropped by the vetter (score 2/10)

The women-minus-men gap in prime-age participation widens toward women when prime-age unemployment rises, because men leave the labour force. The gap is countercyclical.

- Model link: Weak. The model has no unemployment. In App B's pooled household, either earner's exit is funded by the household, so a first earner who loses work can exit. The standard discouraged-worker account predicts the same; the explore data show no added-worker entry by women.
- Varies: none
- Explore estimate: beta +0.231 pp per pp of U; CR1 se 0.111; WCR one-sided p 0.019 (p_opposite 0.981); n 376; G 16; G* 11.1. Leave-one-out max p 0.097 (EE out). Frozen une_rt_a variant +0.40 (p 0.008). Within 2005-2016 alone +0.07 (se 0.19).
- Variants tried: 11
- Vetter's problems: No link to the model. The paper's model has no unemployment (docs/derivations.md: 'no search state'; every non-employed person is in exit), so a gap-on-U slope cannot support or contradict it. A procyclical male participation rate, a female added-worker response and a countercyclical sex gap are all textbook, from discouraged workers, the added-worker effect and male-heavy cyclical sectors. Nothing distinguishes it from the standard account. The candidate's own model_link is 'Weak'. As one of at most five E-hypotheses it would use up Holm budget and power on a test that cannot speak to the paper.; The causal clause is not identified and flips with the specification. In levels with FE, the gap moves because men's activity falls (M -0.193, W +0.038). In within-country first differences (my check, explore/_vet/wm2_vet.py) men do not move (+0.001, se 0.048) and women rise (+0.113, p 0.028): an added-worker story. The candidate's own rationale says 'no added-worker entry by women'. The FD result contradicts that, so the stated mechanism 'because men leave' does not survive.; The estimate depends heavily on the mechanical C3 break dummies. With no break dummies it is +0.636 (p 0.002); with the argan and urgan breaks, +0.231. On the same 342 observations, adding the HICP q series' breaks without q gives +0.114 (p 0.259). The pivotal break set will differ in the confirm half, so the confirm estimate depends on survey and HICP flags as much as on the cycle.; It is unstable over time windows. 1997-2008 gives +0.42, 2009-2019 +0.42 and 2009-2025 +0.40, but the pooled 1997-2025 estimate is +0.23 and 2005-2016 (the bust) is +0.07 (se 0.19). The period that most directly shows the mechanism shows nothing. Adding q as a control (the C-3 environment) collapses it to +0.022.; It rests on a few countries. Leave-one-out is fine (max p 0.097, EE out). Leave-two-out with EE and LV dropped together gives beta +0.117 and p 0.282. Per-country raw time-series slopes are positive in only 8 of 16 countries (12 of 16 after country trends). LU (+8.4 raw) and MT (-10.5 raw) are large outliers in both directions.; Forking paths. The explorer's ledger holds about 93 estimated specifications for the theme, 11 of them on this relation: sexes separately, subperiods, men's-U regressors, with q, three age sub-bands, une_rt_a vs lfsa_urgan, trends, U 25-74, all residents. The candidate picked the lfsa_urgan long window, not the frozen C7 source. The headline p of 0.019 is the selected one, so the true effect is probably smaller (winner's curse). The all-residents version gives p 0.086 and the trends version shrinks it to +0.071.; It is underpowered on 15 clusters. The median leave-one-out se is 0.115, so the MDE at 80% power with G=15 is 0.30 at alpha 0.05 and 0.40 at the Holm-first alpha of 0.01. Power at the explore estimate of 0.231 is 0.60 at alpha 0.05 and 0.27 at alpha 0.01. At a shrunk true value of 0.15 it is 0.33 and 0.10.; It can be computed from the manifest (act cells M/F 25-29..50-54 NAT; une_lfs Y25-54 T TOTAL) and it is not a rescue of a P: it changes no P's regressor or outcome. Those are its only clean points.
- Vetter's power note: On 15 confirm clusters the MDE (80% power, one-sided) is about 0.30 at alpha 0.05 and about 0.40 at alpha 0.01 (Holm-first with 5 E). This uses the median leave-one-out se of 0.115 from the explore half. The explore point estimate of 0.231 is below both. Power is about 0.60 at alpha 0.05 and 0.27 at alpha 0.01, and falls to 0.33 and 0.10 if the true effect has shrunk to 0.15 after selection from 11 variants. My vetting ran about 150 regressions: 13 main checks, 16 leave-one-out runs for the se and 120 leave-two-out runs. Script and output are in C:\Users\s6068C\GitHub\laborformal\participation\explore\_vet\wm2_vet.py and wm2_vet.txt.

## Files

- `explore/women_men/common.py`
- `explore/women_men/s01_levels.py`
- `explore/women_men/s01_levels.csv`
- `explore/women_men/s02_rents.py`
- `explore/women_men/s02_rents.txt`
- `explore/women_men/s03_tenure.py`
- `explore/women_men/s03_tenure.txt`
- `explore/women_men/s04_cycle.py`
- `explore/women_men/s04_cycle.txt`
- `explore/women_men/s05_care_cores.py`
- `explore/women_men/s05_care_cores.txt`
- `explore/women_men/s06_young_men.py`
- `explore/women_men/s06_young_men.txt`
- `explore/women_men/s07_candidates.py`
- `explore/women_men/s07_candidates.txt`
- `explore/women_men/s08_older.py`
- `explore/women_men/s08_older.txt`
- `explore/women_men/s09_results.py`
- `explore/women_men/spec_count.txt`
- `explore/women_men/fig01_prime_age_by_country.png`
- `explore/women_men/fig02_gap_convergence.png`
- `explore/women_men/fig03_age_profile_gap.png`
- `explore/women_men/fig04_q_and_women.png`
- `explore/women_men/fig05_tenure_slopes.png`
- `explore/women_men/fig06_added_worker.png`
- `explore/women_men/fig07_care.png`
- `explore/women_men/fig08_men_young_cores.png`
- `results/explore_women_men.json`
