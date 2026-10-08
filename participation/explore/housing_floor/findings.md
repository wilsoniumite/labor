# Exploration: housing floor

Explore half only (16 countries), 2026-10-08, after the P freeze. Written from the explorer's structured return
(the harness did not let the explorer write this file). Exploratory: every estimate here was chosen along a path
of many tries (120 specifications by this explorer).

**Scope as the explorer stated it.** housing_floor: q, house prices, rent burden and coresidence, and the floor kink (D1/D2) on the explore half. 16 clusters, 15 where F_c is needed (HR has no SILC year before 2010). Inference is the frozen restricted WCR (Webb, B=9999, CR1, one-sided). NOTE: the harness refused to let me write findings.md ("subagents should return findings as text"), so the findings live here and in results/explore_housing_floor.json. Scripts are in explore/housing_floor/ (common.py, describe.py, d1d2.py, slopes.py, checks.py, cores_floor.py, e_candidates.py). Every regression is logged in specs_log.jsonl (120 lines).

## Findings

### q is mostly a common upward trend, so the within-country variation that D1/D2 use is small outside a few countries. (solid)

**Evidence.** Rise in log q, first year to 2025: BG +1.71, PL +1.37, IE +1.35, LV +1.05, HU +0.87, EE +0.81, HR +0.74, PT +0.57, FI +0.54, MT +0.47, CH +0.41, SE +0.39, FR +0.32, BE +0.24, IT +0.10, LU +0.09. Sd around a country linear trend is 0.01-0.05 in BE CH FI FR HU IT LU MT PT SE and 0.10-0.18 in BG EE HR IE LV. Residual sd of log q_{t-1} after two-way FE: 0.125 (1997+), 0.101 (2009+). Files: describe.py, describe.json, fig/q_measures.png

**Model reading.** Identification of a q effect leans heavily on trends and on a handful of volatile countries (CEE, IE).

### CP041 is only partly informative where rental markets are small: in BG and PL it behaves like an administered or indexed price; in EE and LV it tracks house prices. (solid)

**Evidence.** Share of 25-34 renting at market price (ilc_lvps05, 2015-17): HR 3, MT 4, BG 7, PL 8, EE 9, HU 11 (BE/FI/FR/IE/IT/LU 26-31, SE 50, CH 76). BG CP041: 1998 jump of 0.93 log points; annual changes correlate 0.91 with compensation and 0.65 with CP00. PL: correlation 0.88 with CP00. EE/LV: correlation 0.85/0.67 with HPI. SE: -0.59 with HPI (regulated rents). The 1997-2001 jumps in BG/LV/PL are rent liberalisations and sit in the long window. Files: describe.json

**Model reading.** Measurement error in q is concentrated in CEE (protocol C6's known weakness, confirmed); CEE also carries most of the q variation.

### The long window (1997+, lfsa_urgan Y25-74 as U for every country) does not change D1 or D2. The 2009 start costs observations, not the sign. (solid)

**Evidence.** D1 b2: frozen +2.0 (se 5.2, p 0.65, n 230, G 15); long +3.3 (se 5.4, p 0.71, n 324); lfsa_urgan U 2009+ +1.8; no cycle control 1997+ +4.5. D2: frozen +2.1 (se 2.7); long +3.3 (se 2.9, p 0.89, n 342, G 16). Files: d1d2.py, d1d2.json

**Model reading.** Without trends, both D tests are inconclusive with the wrong-signed point estimate, whatever the window or control.

### With country linear trends, D1's b2 is negative (the model's sign) in every window, with every q measure and with or without the cycle control. Without trends it is positive. The trend-free primary identifies off co-trending convergence (rising q and rising participation in high-F countries such as MT, HU and LU). (suggestive)

**Evidence.** Trends: frozen window -4.5 (p 0.073, the protocol robustness run); long lfsa_urgan -6.1 (se 3.2, p 0.028, G* 6.4); 2009+ -4.3 (p 0.078); 1997-2019 -6.9 (p 0.014); no U -6.0 (p 0.029); q=CP041/CP00 -7.8 (p 0.001); q=CP041/comp -5.9 (p 0.12); q=HPI/CP00 -1.9 (se 0.7, p 0.022). Leave-one-out b2 runs from -4.8 to -8.0, max p 0.063 (LV out). Implied slope of A on log q is +5.5 at the F 25th percentile (se 3.7) and -5.5 at the 75th percentile (se 2.9, two-sided p 0.04). Country slopes with trends correlate -0.46 with F_raw (SE +11, FR +17, CH +12, LU +34, IE +8 against HU -19, PT -12, BG -23, IT -34; MT +22 is the exception). Files: checks.json, slopes.json, fig/country_slopes.png, fig/e_candidates_loo.png

**Model reading.** This is the floor kink's shape. q encloses a priced exit where the parental floor is rare (positive slope) and taxes independent work where it is common (negative slope). The standard concave income-effect account predicts b2 >= 0. It was selected among about 27 D1 variants, so it is exploratory.

### D2 does not measure curvature. Because q trends, (log q - m_c)^2 is nearly a quadratic time trend, and IE carries most of the identifying variation. (solid)

**Evidence.** Within-country correlation of (log q - m_c)^2 with (t - tbar_c)^2 is above 0.88 in BE BG FI HU IE MT PL PT. After the FE, IE supplies 61% of D2's identifying variation, EE 10%, every other country 6% or less; G* is about 4. D2 with country quadratic trends: -4.5 (se 4.9, p 0.12, G* 3.3). Leave-one-out of the long D2: +1.7 to +4.8. Files: checks.json

**Model reading.** A D2 null or positive estimate here says little about the kink. It tests whether fast-q countries had U-shaped participation paths.

### The coresidence mirror image: the coresidence response to q is zero on average but rises with floor availability, once country trends are included. (weak)

**Evidence.** Coresidence 25-34 on log q with trends, lfsa_urgan U, 2005-2025: b(q) -0.9 (se 3.8). With q x F added: b(qxF) +10.4 (se 3.6, p 0.008, n 282, G 15); leave-one-out +8.8 to +12.1, max p 0.064 (EE out). Less robust than the trend D1: 2005-2019 +7.5 (p 0.21); frozen une_rt_a U +5.9 (p 0.15); q=CP041/CP00 +5.5 (p 0.087); HPI +6.5 (p 0.071); without trends +1.2 (se 4.1). Files: cores_floor.json, e_candidates.json

**Model reading.** Consistent with the kink: where the floor exists, q moves the young home rather than into work. Not distinctive on its own (household formation with family insurance predicts it).

### The level of the rent burden moderates the q response less clearly than floor availability does. The host's-budget moderator (outright owners 55-64) behaves like F. (weak)

**Evidence.** With trends: moderator = overburden of 25-29 in 2005-2010 (not manifest) -4.2 (p 0.20); market-renter share 25-34 (not manifest) +5.7 (mirror sign); outright owners 55-64 (manifest, 2015-17, not predetermined, 16 countries) -5.4 (se 2.1, p 0.020). Overburden of 25-29, 2010-19 mean: SE 12.8, CH 12.5, BE 12.4, BG 12.3, HU 11.1; MT 2.1, HR 5.0. Files: checks.json, fig/overburden.png

**Model reading.** The host-budget channel in docs/derivations.md points the same way, but it is nearly collinear with F.

### Coresidence and participation paths per country. (solid)

**Evidence.** F_raw: SE 3, FI 6, FR 9, CH 11, BE 15, LU 19, EE 27, IE 27, HU 33, LV 36, PL 38, PT 38, MT 40, BG 44, IT 46 (HR none; about 60 after 2010). Coresidence rose in PL +14.6, IE +13.9 (mostly after 2015), CH +10.7, BE +9.7, and fell in EE -12.2. A2534 rose in MT 76 to 91 (2005-2019), HU 77 to 89, LU 76 to 90. Files: fig/cores_act.png

**Model reading.** Strong secular participation trends in some high-F countries are what the trend-free D1 confounds with q.

## Data problems

- une_rt_a starts in 2009 (FR 2003, SE 2005, CH 2010), so every frozen panel with U runs from about 2009. lfsa_urgan Y25-74 is available from 1995 for all 16 explore countries.
- MT activity rates for nationals (lfsa_argan citizen NAT) are blank from 2021 (citizen TOTAL is present), so MT leaves the A2534 panel after 2019.
- HR has no F_c (SILC starts 2010), so D1 and the q x F candidates have 15 clusters.
- HR has no nama_10_lp_ulc D1_SAL_PER in NAC, so log(CP041/compensation) is missing for HR.
- CH house prices exist only as I25_A_AVG from 2017, so CH's HPI robustness series starts in 2017, not 2005.
- CP041 in BG and PL behaves like an administered or indexed price (BG +0.93 log points in 1998; BG correlates 0.91 with compensation, PL 0.88 with CP00). HR, MT and BG have 3-7% market renters among 25-34s. The 1997-2001 CEE jumps are liberalisations.
- D2's squared deviation is about 0.9 correlated with a country quadratic time trend in 8 of 16 countries, and IE supplies 61% of its identifying variation (G* about 4).
- The harness blocked writing explore/housing_floor/findings.md (subagents must return findings as text), so the findings are in this output and in results/explore_housing_floor.json.

## Candidate E-hypotheses and their vetting

### E-HF1 — kept by the vetter (score 5/10)

Varies D1. Once country-specific linear trends absorb the secular co-movement of rents and participation, the young's (25-34) participation response to q is lower where the parental floor is more available: b2 on log q_{t-1} x F_c < 0. The cycle control is lfsa_urgan for every country, over the long window 1997-2025.

- Model link: Section 'The outside option', eq. (exit) s(q) = max(s0 - q h_e, s_under), and docs/derivations.md (P1/P4 critics): at the dependency floor, s is flat in q and q only taxes independent work, so the slope is <= 0 at high F and > 0 at low F. The standard concave income-effect / life-cycle account predicts b2 >= 0 (the response grows as income after housing falls), so it does not predict the same sign. Trends address the convergence (Balassa-Samuelson) confound named in protocol C6.
- Varies: D1 (adds country linear trends; U = lfsa_urgan Y25-74 TOTAL for all countries instead of C7's une_rt_a-first rule; window 1997-2025 effectively used). Never changes D1's verdict.
- Explore estimate: b2 = -6.09, CR1 se 3.21, one-sided WCR p 0.028 (p opposite 0.972), n 324, G 15, G* 6.4; one-sided 95% CI (-inf, -1.40]; leave-one-out b2 from -4.8 to -8.0, max p 0.063 (LV out). Implied slope at F p25 +5.5 (se 3.7), at F p75 -5.5 (se 2.9). Selected among variants, so expect shrinkage.
- Variants tried: 27
- Vetter's problems: Rescue of D1. The frozen D1 on the explore half has the wrong sign (b2 +2.0, p 0.65). E-HF1 adds country linear trends, which the protocol already lists as a no-verdict robustness run for D1, and swaps the cycle source. If it passes on the confirm half it must be reported as evidence for D1-with-trends only. It must never be presented as support for the floor mechanism while D1 itself is inconclusive.; Forking paths. Among the 11 one-at-a-time D1 departures in specs_log rows 1-11 (cycle source, window, no cycle control, three alternative q measures, trends, all residents), trends is the ONLY variant with b2 < 0. The other ten run from -9.7 (q_comp, p 0.15) to +5.4, and nine of the ten have p > 0.48. The explorer's count of 27 D1 variants is honest, but the effective selection is 1 of about 11 structural forks. A Bonferroni-style adjustment puts the explore p near 0.3, so expect strong shrinkage (winner's curse).; The sign is set by the trend term. On the identical 324-row frame, b2 is +3.34 without trends and -6.09 with them. The result is an identifying assumption (linear country trends absorb Balassa-Samuelson co-movement), not a robust feature of the data.; The long window does not carry the signal. On 1997-2012 alone b2 is +0.20 (p 0.53); on 2013-2025 it is -4.69 (p 0.10). The stated rationale (catching the 2000s boom and bust through the lfsa_urgan window) is not where the effect sits. The early years mainly help pin down the trends.; Identified from blocs, not countries. Leave-one-out is fine: max p 0.063 (LV out). Leave-two-out is also fine: 2 of 105 pairs have p > 0.10, worst IT+LV at p 0.11 with B = 999. But dropping the CEE countries (G 10) gives -5.1, se 6.4. Dropping the South gives -4.8, p 0.064. Dropping both (G 7) gives +4.7. The slope difference is the high-F CEE and South blocs against the rest. Nothing happens inside the low-F group.; Distinctiveness is weakened by the q decomposition, the most serious problem. In the joint regression (both components x F, plus main effects, trends), the rent leg log CP041 x F is -4.28 (se 4.13, p 0.11) and the goods leg -log IGD_NNRG x F is -7.46 (se 3.45, p 0.035). Homogeneity is not rejected, so q enters as a ratio, but the goods-price denominator carries at least as much weight as rents. A standard concave income effect also predicts that a goods-price squeeze (for example depreciations) raises the young's participation more in poorer, high-coresidence economies. The paper's mechanism is rents taxing independent living, so a goods-led signal is not distinctive.; Fragile to plausible controls. Adding general inflation (log CP00 x F and main effect) gives b2 -4.50 (p 0.081). Adding log real compensation and its interaction with F gives -7.16 (se 4.94, p 0.083). With the frozen U (une_rt_a, 2003/2009+) and trends: -4.53 (p 0.073).; The timing is not sharp. With the lead added, the lag coefficient is -7.06 (p 0.014), but the lead log q_{t+1} x F is -3.25 (se 3.19, two-sided p 0.22): same sign, about half the size. The contemporaneous q gives -9.11. This fits slow-moving co-trends more than a lagged price response, though it is not decisive.; Underpowered. The explore se is 3.21, so the MDE on 15 clusters is 8.43 at one-sided 0.05 and 11.2 at 0.01 (Holm's first step with 5 E). If the explore estimate is the truth, power is 0.55 at 0.05 and 0.24 at 0.01. At a shrunk true effect of 4.5 (or 3.0), power falls to 0.36 (0.21) at 0.05 and 0.12 (0.06) at 0.01. Most likely outcome: inconclusive.; Units. At the look, F is standardised with the 31-country mean and sd (confirm.py's fstd), not the explore sd, so the 8.43 MDE and the -6.09 estimate are in different units from the confirm-half coefficient. The p-values are unaffected. Confirm countries with no ilc_lvps08 value in 2003-2008 are dropped, so G can fall below 15 and the MDE rises.; What survives in its favour. Randomisation inference permuting F across the 15 countries (2000 draws, studentised) gives one-sided p 0.039, close to the WCR value. Quadratic trends: -5.21 (p 0.018). All residents: -3.97 (p 0.031). Start 2003: -5.81 (p 0.028). Start 2005: -5.62 (p 0.034). Excluding 2008-2013: -5.63 (p 0.084). The effect is larger at 25-29 (-8.0, p 0.017) than at 30-34 (-4.2), which fits the floor story (younger ages coreside more). Women: -6.9; men: -5.3. Computable from the manifest: yes (act, une_lfs, hicp, cores).
- Vetter's power note: The explore CR1 se is 3.21 (G 15, G* 6.4). MDE (one-sided, 80% power, t with 14 df): 8.43 at alpha 0.05, 9.66 at 0.025, 11.2 at 0.01. Power if the true b2 equals the explore -6.09: 0.55 at 0.05, 0.24 at 0.01. At a winner's-curse-shrunk 4.5: 0.36 and 0.12. At 3.0: 0.21 and 0.06. The selection was 1 of about 11 structural D1 forks, so shrinkage is likely; the realistic power under Holm with up to 5 E is roughly 15-35%. Units are explore-sd(F); at the look F uses the 31-country sd, so the coefficient rescales (p-values do not). G may be below 15 if a confirm country lacks F.

### E-HF2 — dropped by the vetter (score 2/10)

Varies C-1. The coresidence response of 25-34s to q rises with floor availability: within countries, after country trends, a rise in rents moves more young people back to the parental home where the parental floor is more available. b on log q_{t-1} x F_c > 0. This is the mirror image of E-HF1.

- Model link: docs/derivations.md, P2 and 'predictions the draft omitted': the coresidence response to q is larger where F is high (both thresholds q_WP and q_enc are crossed sooner where a parental room exists); jointly with E-HF1 it traces both arms of the kink. On its own it is not distinctive: a household-formation model with family insurance (Kaplan-type) predicts the same sign.
- Varies: C-1 (adds log q x F_c, country linear trends, and lfsa_urgan U for all countries). Never changes C-1's verdict.
- Explore estimate: b = +10.42, CR1 se 3.59, one-sided WCR p 0.008, n 282, G 15, G* 6.8; one-sided 95% CI [5.95, inf); leave-one-out +8.8 to +12.1, max p 0.064 (EE out). Fragile to window and control: 2005-2019 +7.5 (p 0.21); frozen une_rt_a U +5.9 (p 0.15); q=CP041/CP00 +5.5 (p 0.087); no trends +1.2.
- Variants tried: 5
- Vetter's problems: Identified off one common time shape, not off rents. If F_c x year dummies are added, so that q x F is identified only from country-specific deviations of q, b goes from +10.42 to -4.81 (se 8.09, p 0.76). If F_c x t^2 is added, b = +0.18 (se 5.98, p 0.48). What the estimate measures is that high-F and low-F countries' coresidence paths bend differently over 2005-2025, matched against the common rise in q (normalised flat around 2016, then up). Anything else that differs by F over time produces the same coefficient: the 2008-2013 youth labour-market collapse in the South and East (U is 25-74, not youth), the post-COVID resettling, and the 2021 SILC redesign. It is one shape degree of freedom, not 15 countries' worth of rent variation.; Rests on 2022-2025, right after the SILC 2021 break. In an FWL decomposition, 2022-2024 supply about 80% of the numerator (2022: 0.29, 2023: 0.21, 2024: 0.30; 2025: -0.17), and 2008-2009 most of the rest. On 2005-2019, b = +7.5 with se 8.9 (p 0.19-0.21), so there is no pre-COVID evidence. Nearly every country carries a 2021 break dummy; together with the country trends, each country's post-break period is about four points with its own level.; Overlaps mechanically with the definition of F. F_c is the mean of the outcome series (ilc_lvps08 25-34) over 2003-2007, and those years sit inside the outcome sample. Dropping each country's own F years from the outcome gives b = +9.3, se 7.6, p 0.074. Starting in 2008 gives +10.7 (se 8.2, p 0.066), and 2010+ gives +12.7 (se 9.3). The point estimate holds, but the precision that makes it 'significant' comes from the years used to build F plus 2022-2024.; The se of 3.59 is an outlier on the low side. Across neighbouring specifications the CR1 se runs from 4.6 to 9.3: 2005-2019 8.9, 2009+ 8.5, own-F-years dropped 7.6, F x year 8.1, q_cp00 4.6, q_hpi 4.7, no cycle control 4.9, frozen une_rt_a U 5.2. With 15 clusters a CR1 se is itself noisy, and the claimed MDE of 9.44 is built on the most favourable draw.; Forking paths are undercounted. 'Variants tried: 5' counts only the coresidence cells. The pairing of lfsa_urgan U with country trends was itself selected on the D1 side, where it was the only one of 11 D1 specifications with p < 0.05 (log line 10; the D2 block of the same grid added 11 more). On coresidence, the 2x2 {frozen U, lfsa_urgan U} x {no trends, trends} gave -2.5, +5.9, +1.2 and +10.4, so one of four cells clears 0.05. Without trends the estimate is +1.2. The sign and size depend entirely on the trend choice, which was picked on a different outcome. The honest count is about 25 or more specifications upstream of this cell.; Partly a rescue of a failed P. C-1 (coresidence on log q) is inconclusive on the explore half, and in this very specification it is -0.88 (p 0.60). E-HF2 adds a moderator so that C-1 'holds where F is high'. It is labelled as varying C-1, but in substance it moves the goalposts of a consistency check that failed.; Not distinctive, as the explorer concedes. Family insurance in a standard household-formation model (Kaplan-type) predicts the same sign. Even a confirm-half pass would not separate the paper's model from the standard account. The leverage would come only from the joint test with E-HF1, and E-HF1 shares the same selected trends + lfsa_urgan specification, so the two are not independent pieces of evidence.; Leave-one-out looks fine, but the support is narrow. LOO max p is 0.064 (EE out). The lowest leave-two-out beta is +6.3 (EE and FI out). Contributions to the numerator are concentrated in LV 22%, FI 22%, SE 21%, PT 16% and EE 15%. Two of these (FI, SE) are low-F countries where coresidence fell as q rose above trend: the effect is a contrast between the Nordic and Baltic/Portuguese paths. Randomising F's assignment across the 15 countries gives p = 0.004 (t). That confirms the WCR p conditional on this design, but it does not address the time-shape confounding found above.; Computability is fine. cores, une_lfs (lfsa_urgan Y25-74 TOTAL) and hicp CP041/IGD_NNRG are all manifest raw frames, and specs.estimate can run it with variant='country_trends'. At the look, F's standardisation constants must be the 31-country ones (C9), not the explore-half ones used here; this rescales b.
- Vetter's power note: The MDE claimed by the explorer, 9.44, is (t_.95 + t_.80, 14 df) x 3.59. That 3.59 is the smallest se among about ten neighbouring specifications, which run from 4.6 to 9.3 (2005-2019: 8.9; 2009+: 8.5; own F years dropped: 7.6; F x year: 8.1; frozen U: 5.2). With a realistic se of 5 to 8 on 15 confirm clusters, the MDE is about 13 to 21 points per unit of log q x sd(F). The explore estimate of +10.4 is the winner among four cells (the others are -2.5, +1.2 and +5.9), so the expected confirm-half effect is well below 10. Power at a true effect of 5 to 6 is roughly 20-35%. In the de-confounded form (with F x year), the explore estimate is -4.8 with se 8.1, so power is essentially nil. Across the two candidate specs this vet estimated 13 specifications, with B = 1999 and R = 499 F-permutations; the script is C:\Users\s6068C\GitHub\laborformal\participation\explore\_vet\vet_hf2.py and the output is C:\Users\s6068C\GitHub\laborformal\participation\explore\_vet\vet_hf2.json.

## Files

- `explore/housing_floor/common.py`
- `explore/housing_floor/describe.py`
- `explore/housing_floor/d1d2.py`
- `explore/housing_floor/slopes.py`
- `explore/housing_floor/checks.py`
- `explore/housing_floor/cores_floor.py`
- `explore/housing_floor/e_candidates.py`
- `explore/housing_floor/specs_log.jsonl`
- `explore/housing_floor/describe.json`
- `explore/housing_floor/d1d2.json`
- `explore/housing_floor/slopes.json`
- `explore/housing_floor/checks.json`
- `explore/housing_floor/cores_floor.json`
- `explore/housing_floor/e_candidates.json`
- `explore/housing_floor/fig/q_measures.png`
- `explore/housing_floor/fig/cores_act.png`
- `explore/housing_floor/fig/overburden.png`
- `explore/housing_floor/fig/country_slopes.png`
- `explore/housing_floor/fig/e_candidates_loo.png`
- `results/explore_housing_floor.json`
