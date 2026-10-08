# Design review — the methodologist's findings (2026-10-08, before any data)

Reproduced as returned. `PROTOCOL.md` adopts most of it; departures are noted in `STATE.md`.

## Loopholes and fixes

- **[fatal]** The derivation the predictions rest on is marked 'to be checked', and as written it does not give the signs of P1 and P3. For P1, the model's own P2 and P4 say that a rise in q pushes some young people to the coresidence floor. At that floor the exit value is flat in q while net work value (w - q h_w) falls, so their participation falls. The young response to q is therefore ambiguous, which is the hump again. For P3, most prime-age households in Europe are owner-occupiers or mortgagors who own what they occupy, so they are hedged or levered long. On the protocol's own rule the aggregate sign for prime-age women is ambiguous and depends on the tenure mix. Any result could later be explained as 'the young were at the floor' or 'too many owners'. That is a forking path in the theory, not the data.
  - *Fix:* Finish the derivation before the P freeze and write down the conditions under which each sign holds. Restate P1 on the part of the age range off the floor (keep 25-34, but state the condition that most of the band lives independently), or make P1 conditional on tenure. Add a pre-specified tenure dose as a secondary to P1 and P3: the effect is larger where the baseline renter share of the group is higher. Measure that share from EU-SILC 2005-2007 tenure by age. It is a covariate, so it can be seen before the freeze without seeing outcomes. Then state in advance which pattern contradicts the model (for example, a W-M effect no larger in high-renter countries).
- **[fatal]** Reverse causality in P3 has the same sign as the prediction. Rising women's participation (from childcare, education, norms) raises household income and housing demand, and so rents. The W-M difference does not remove this, because the shock is to women's participation itself, not a common aggregate shock. The same applies to the level regressions in P1 and P2: young people are the marginal renters, so a rise in young people's participation and income feeds rents directly. A positive estimate is therefore equally predicted by the no-enclosure alternative.
  - *Fix:* Downgrade P3 from a distinctive causal test to a pre-registered sign of a conditional association, and say so in the protocol. Put the discriminating content in the tenure-dose interaction above. Use the HICP actual rentals index, which covers sitting tenants and is often regulated, so it responds sluggishly to current income, rather than house prices. Lag q by one year. Pre-register a lead diagnostic: q at t+1 added to the primary regression. A lead coefficient as large as the lagged one is reported as evidence of feedback. Treat any instrument as exploratory, for example a euro-area policy-rate change times the country's variable-rate mortgage share (fixed before the freeze). With 15-30 clusters a 2SLS is weak and must not decide the verdict.
- **[serious]** The difference designs (young minus old, women minus men, within country-year) are only partly robust to reverse causality. They remove channels where an aggregate income shock moves q and moves both groups' participation by the same number of points. They do not remove three things. (a) Shocks specific to one group that feed q through that group's housing demand: young people are the rental market. (b) Aggregate shocks with uneven incidence: young participation is far more cyclical than old, and booms raise q. That biases beta_young - beta_old upward, which is P1's predicted sign. (c) Trends specific to one group: pension reforms raise 55-64 participation in the same decades that q rose, which biases P1 downward.
  - *Fix:* Keep the difference outcome as primary, but add the aggregate unemployment rate for ages 25-74 as a control in P1, P3 and P4. In a difference regression this coefficient absorbs the groups' different cyclical sensitivity. Add sex-specific earliest pension eligibility age as a control in P1. In the write-up, state that the difference removes common-level reverse causality only, not feedback from group-specific shocks.
- **[serious]** Power. With about 15 country clusters per half, the minimum detectable effect at one-sided alpha 0.05 and 80% power is about 2.6 standard errors (t(14) critical values 1.76 + 0.87). The SE is about sqrt(2) larger than on about 31 countries, so the confirm-only MDE is about 1.45 times the full-sample MDE. Nulls on the confirm half will mostly be uninformative. P5 (3 post years) and P6 (one cross-section) are weaker still.
  - *Fix:* Test P on the full sample as its primary test. P is stated before any data, so every country is out of sample for it. Report P on the confirm half as the clean-room replication, and use the confirm half for E. Before the look, report the minimum detectable effect for each test, using the explore-half variance (allowed, because it does not change any specification). Report a pre-stated equivalence bound so a null can be read. Also register a time holdout: rerun the frozen code on all countries for 2026-2028 when those data are released.
- **[serious]** Forking paths inside P. The draft fixes data codes later ('becomes PROTOCOL.md once data codes are fixed'). Many choices are still open: activity rate or employment rate, points or log-odds, age bands, nationals or all residents, deflator, rent or house prices, lag, sample years, break handling, missing cells, weights, controls. Each one made after seeing any value is a fork.
  - *Fix:* Freeze all of these, as code and not prose, at the P-freeze commit (F0). Run the pipeline end to end on a synthetic panel with the same schema first. Allow only outcome-blind design data before F0: Eurostat structure and codelists, SDMX availability constraints (which keys and years exist, without values), pension-age documents, population and tenure covariates. No outcome series.
- **[serious]** Forking paths in E. The number of E-hypotheses is unlimited. E-hypotheses written as prose can be reinterpreted at the look. An E can also be a rescue of a P that failed on the explore half (for example, 'P1 holds for women only'), which then confirms and gets read as support for the model.
  - *Fix:* Cap E at K = 5. Each E is a function in e_specs.py with its outcome, regressor, sample, controls and predicted sign, frozen by the E-freeze tag. E uses only series already in the frozen data manifest. Apply Holm within the E family. An E that varies a P is labelled as such and can never change that P's verdict.
- **[serious]** The measure of q is unsettled and each option carries a distinct bias. The HICP actual rentals index covers sitting tenants, is regulated in many countries and has a tiny weight in CEE countries with small rental markets. That causes attenuation and misses the market rents that entrants pay. House prices are an asset price: they capitalise q at the interest rate, and the 2014-2021 fall in rates moved them independently of q, while rates also affect labour supply through mortgages. Dividing rent by wages puts an outcome-related variable in the denominator. Dividing by all-items HICP includes rent itself and the energy shocks of 2008 and 2022. Dividing by goods brings in Balassa-Samuelson: tradables productivity raises q and incomes together in converging CEE countries.
  - *Fix:* Primary q is log(HICP CP041 actual rentals / HICP non-energy industrial goods), annual averages, lagged one year. This is closest to the model's r/p and avoids energy swings. Pre-registered robustness checks, reported without any verdict attached, are log(house price index / HICP), log(CP041 / HICP all items) and log(CP041 / nominal compensation per employee). State the Balassa-Samuelson confound in the limitations, and partly address it with year fixed effects and a robustness check with country-specific trends.
- **[serious]** Common trends. Women's participation, 55-64 participation and q all trend upward. Year fixed effects remove only the European-wide part. The rest is identified from country-specific trends: CEE convergence, the Southern European catch-up in women's participation, the 1997-2007 boom and bust in Spain, Ireland and Greece. Those trends are confounded and generate spurious regression with nonstationary series.
  - *Fix:* The primary specification is two-way fixed effects in levels with inference clustered by country, which is valid for arbitrary within-country serial correlation. Pre-register two robustness checks: country-specific linear trends, and stacked non-overlapping 5-year long differences. Report them, but only the primary sets the verdict, and say so in advance.
- **[serious]** Pension reforms. The equalisation of women's pension ages and the closing of early-retirement routes moved 55-64 participation by 10-20 points over the panel. That confounds P1's old group and is the treatment in P7. The pension-age table must be hand-coded (OECD Pensions at a Glance, MISSOC). Coding it while knowing outcomes, for example when timing a reform, is a quiet fork.
  - *Fix:* Code the earliest-eligibility and normal ages by country, sex and year from documents only, with sources cited per cell, and commit them at F0 before any outcome is loaded. Use the table as a control in P1 and as the regressor in P7.
- **[serious]** Survey breaks. The 2021 IESS regulation broke EU-LFS series in almost every country. There are also country breaks: Germany 2020 (Mikrozensus redesign, which also affects SILC), Germany, Italy, Spain and Austria in 2004-2005 (continuous survey), France in 2003, 2013 and 2021. A level break in one country moves the regression unless it is handled, and handling it case by case is a fork.
  - *Fix:* Apply a mechanical rule: every 'b' flag in an outcome or regressor series for country c in year tau adds the dummy 1[country = c, t >= tau]. Flags are metadata, so no judgement is involved. Difference outcomes cancel breaks that are common to both age groups. P5's comparison sits entirely inside the post-2021 regime.
- **[serious]** The 2008 and 2020 shocks. In 2020-2021 participation collapsed, short-time work schemes counted furloughed workers as employed, and rent indices hardly moved. In 2008-2013 the housing busts in Spain, Ireland and Greece coincided with mass unemployment and an added-worker effect: women's participation rose while q fell. That biases P3 and P1 in opposite directions and depends on country timing that year fixed effects do not absorb.
  - *Fix:* Drop 2020 and 2021 from all annual specifications. Control for the 25-74 unemployment rate. Pre-register a robustness check that excludes 2008-2013, with no verdict attached.
- **[serious]** Composition. Inside a band, the share of 60-64-year-olds in the 55-64 group shifts as baby-boom cohorts pass through. Immigration is concentrated at young ages, raises rents and changes the composition of young participation (lower for some groups of women, higher for men). Expanding tertiary education raises participation at 25-34 and delays entry at 20-27.
  - *Fix:* Build each band as the equal-weight mean of its 5-year sub-bands. Use nationals (citizenship = NAT) for LFS rates where coverage allows. Use the equal-weight mean of the male and female rates. Pre-register a robustness check that controls for the group's tertiary-attainment share.
- **[serious]** Bad or mechanical controls and regressors. In P2, youth unemployment is affected by the same q shock. In P8, the youth unemployment rate has youth labour-force participation in its denominator, so students leaving the labour force lower it mechanically. In P4, both sides are outcomes of the cycle: in recessions unemployed NEETs and coresidence rise together, which biases the estimate towards the search reading.
  - *Fix:* P2 keeps youth (15-29) unemployment because the prediction says 'holding' it, and also reports the estimate without it. P8 uses the 25-54 unemployment rate as the measure of labour prospects. P4 controls for 25-74 unemployment, and reports the reduced form of the inactive share on q as a secondary.
- **[serious]** P5 confounds. There are only three post years (2023-2025). The ECB's 2022-2023 rate rises and the energy shock hit at the same time. The clerical share is correlated with how service-heavy the economy is and with youth cyclicality. ISCO cells by age are unreliable in small states. Generative-AI adoption in European firms was low over the window.
  - *Fix:* Use the 2018-2019 clerical share among employed 20-29-year-olds as exposure, fixed before the freeze. Run an event study on 2016-2019 and 2022 as a pre-trend check: report it, and flag 'pre-trend' if the 2016-2019 coefficients jointly differ from zero at 10%. Use randomization inference over exposure across countries within region. Report the minimum detectable effect and expect an inconclusive result.
- **[serious]** P6 has reverse causality through migration. Poor routine labour markets in CEE (the Baltics, Romania, Bulgaria) drove young people to emigrate, which raises measured aging. So the realised change in aging is partly an outcome of the labour market.
  - *Fix:* Use predicted aging as the regressor: the 2011 single-year age structure aged forward 8 years with no migration and no mortality, then the change in the ratio of population 56+ to population 21-55. That is the Acemoglu-Restrepo idea, implemented from demo_pjan. Report realised aging as a secondary.
- **[serious]** Prior knowledge breaks the country split. Everyone involved, including the AI agents, already knows the Spanish bust, Swedish rent control, Italian NEETs and German pension reforms. The repo's paths/ cache also already holds ILO temporary-employment series for Germany, Spain, Italy, the Netherlands and Sweden. An E-hypothesis can be informed by the confirm countries without any file being opened.
  - *Fix:* Disclose this in the protocol and list the data already seen. Require each E to cite the explore-half output that motivated it, committed with the E freeze. Add the 2026-2028 time holdout as the only test of data that no one has seen.
- **[minor]** Data vintages and revisions. Eurostat revises series. If the explore half is downloaded months before the confirm half, the two halves and the full sample come from different vintages. Re-downloading also creates a quiet way to shop for a vintage.
  - *Fix:* Every fetch is logged with URL, UTC time and SHA-256 hash in a committed fetch_log.jsonl. The confirm run downloads all countries in one vintage and reports any difference in the explore-half data against the logged hashes. No refetch after the look, except under the bug policy.
- **[minor]** Sample scope. Widening to 38 OECD countries after exploration is a fork, and it mixes non-harmonised sources. The UK leaves Eurostat in 2020, and splicing in ONS data would be a discretionary choice.
  - *Fix:* Decide before the P freeze. The recommendation is that the primary sample is Eurostat only: EU27 plus Norway, Iceland, Switzerland and the UK, with no candidate countries. Keep the UK through 2019 only and do not splice. That costs little, because 2020-2021 are dropped anyway, and the UK simply drops out of P5. If OECD countries are added, the non-European members form a separate replication set that is never explored, built from OECD sources: labour force statistics by sex and age, and the Analytical House Price database rent and price indices.
- **[minor]** Small-state noise and unreliable cells. Luxembourg, Malta, Cyprus and Iceland have small LFS samples, especially for 60-64 by sex and ISCO by age.
  - *Fix:* Treat cells flagged 'u' (low reliability) and 'c' (confidential) as missing, with no interpolation. Weight countries equally, with country as the cluster.
- **[minor]** Few clusters with treatment variation. In P7, within-country variation in the women-minus-men eligibility-age gap may come from only a handful of reforming countries. The wild cluster bootstrap is then unreliable (MacKinnon and Webb 2017). The 'one look' also has no policy for bugs.
  - *Fix:* Report the effective number of clusters G* (Carter, Schnepel and Steigerwald 2017) and the count of countries whose regressor varies after fixed effects. If G* < 8, that P's verdict is reported as 'design uninformative' whatever the p-value. Bug policy: a bug found after the look is fixed in a new commit, and both the original and the fixed results are reported, with the diff.

## Split design

The unit is the country, and the list is fixed before the split: EU27 + NO + IS + CH + UK, 31 countries, with no candidate countries.

Strata are five regions:
- Nordic: DK, FI, SE, NO, IS
- Continental: AT, BE, CH, DE, FR, LU, NL
- Anglo: IE, UK
- South: CY, EL, ES, IT, MT, PT
- CEE: BG, CZ, EE, HR, HU, LT, LV, PL, RO, SI, SK

Inside each stratum, rank countries by 2010 population (not an outcome), pair adjacent countries, and assign one of each pair to each half at random. The leftover country in the Nordic, Continental and CEE strata is assigned so the halves are 15 and 16. Matched pairs balance the halves on regime (busts, convergence, pension systems), so a regime difference between halves cannot pass for a failure to replicate.

Seed: seed = int(sha256(b'participation-split-v1|' + ','.join(sorted(codes))).hexdigest()[:16], 16), passed to numpy.random.default_rng. The seed is a function of the committed country list, so the only way to shop for a split is to change the list, which git would show. split.py and split.json are committed in the P-freeze commit (F0).

What the confirm half may be used for:
- Before the E freeze: nothing except outcome-blind metadata (codelists, SDMX availability constraints) and design covariates that are not outcomes. No values are downloaded.
- After the E freeze: one run of the frozen pipeline, which produces (i) P on the full sample (primary, because P was stated before any data, so every country is out of sample for it), (ii) P on the confirm half (clean-room replication), and (iii) E on the confirm half (the only valid test of E).
- After that look: free use, all labelled exploratory.

If any P is amended after any data value has been seen, that P's primary test falls back to the confirm half only.

A time split was rejected as the main design. Eras such as AI after 2023 and COVID would confound the halves, and overfitting in country panels comes from country-level idiosyncrasy. A time holdout is added on top: the frozen code reruns on 2026-2028 data for all countries.

## Inference method

Implementation uses numpy and scipy only.

(1) Partial out. Build Z, the fixed-effect dummies (country and year, dropping one of each), the controls and the break dummies. Compute M_Z = I - Z pinv(Z) once; N is about 800, so this is cheap. Set xt = M_Z x and yt = M_Z y. Then beta_hat = xt'yt / xt'xt and residuals u = yt - xt * beta_hat.

(2) CR1 standard error. For each cluster g, s_g = sum over i in g of xt_i * u_i. V = c * sum_g s_g^2 / (xt'xt)^2, with c = G/(G-1) * (N-1)/(N-K). The constant c cancels in bootstrap-t p-values, so the question of counting fixed effects in K does not matter. The statistic is t = (beta_hat - beta0) / sqrt(V).

(3) Restricted fit under H0: beta = beta0. Regress y - beta0 * x on Z to get fitted values yr and residuals ur. Since M_Z annihilates yr, the bootstrap only needs M_Z(ur * v).

(4) Bootstrap, b = 1..9999. Draw v_g independently per country from the Webb distribution: {-sqrt(1.5), -1, -sqrt(0.5), sqrt(0.5), 1, sqrt(1.5)}, each with probability 1/6. Set e* = M_Z(ur * v_g(i)), beta* = beta0 + xt'e* / xt'xt, residuals u* = e* - xt * (beta* - beta0), and compute the CR1 statistic t*. Vectorise by stacking the B weight vectors as an N x B matrix. Use a fixed rng seed committed at F0.

(5) p-values. For predicted sign s: p = (1 + #{s * t* >= s * t}) / (B + 1). The two-sided version is used for the 'contradicted' test in the opposite direction.

(6) Confidence intervals by test inversion over a grid of beta0. Reuse the same v draws (common random numbers) and solve for p = alpha by bisection.

(7) Diagnostics. Compute G* (Carter, Schnepel and Steigerwald): G* = G / (1 + Var_g(gamma_g)/mean(gamma_g)^2), where gamma_g = xt_g'xt_g / xt'xt in the scalar case with spherical within-cluster errors. Also count the clusters with nonzero variation in xt. If G* < 8, the verdict is 'uninformative'.

(8) Validation before F0, on synthetic data with the same schema: rejection rate under the null between 3% and 7% over 1,000 synthetic panels with G = 15, and recovery of a planted effect.

(9) Randomization inference, primary for P5 and P6, where the treatment is at country level. Permute the country-level regressor across countries within region strata. Enumerate exactly when the product of stratum factorials is 10,000 or less, otherwise use 9,999 draws. Recompute the full regression and the studentized t (CR1, or HC2 for the cross-section). p = (1 + #{s * t_perm >= s * t}) / (1 + R). Studentizing keeps the test valid for the weak null asymptotically (Chung and Romano), and the test is exact under the sharp null.

(10) Randomization inference is not used for the q specifications. Reassigning q paths across countries assumes exchangeability, which is not credible, and the year coverage is unbalanced. It may be reported, labelled as a sensitivity check.

Reporting: point estimate, CR1 SE, WCR p, inverted CI, G*, number of country-years, and the MDE.

## Multiplicity

Verdict per P. 'Supported' means the one-sided p for the predicted sign survives Holm-Bonferroni across the 8 primary P tests at familywise alpha 0.05. 'Contradicted' means the one-sided p for the opposite sign survives Holm across the same 8. Otherwise the P is 'inconclusive'.

P3 is an intersection-union test: both legs must reject at the Holm-adjusted level for P3, and the two legs need no adjustment for each other.

Model-level verdict, stated in advance:
- Supported: at least two of the three distinctive predictions (P1, P3, P4) are supported and none is contradicted.
- Contradicted: any distinctive prediction is contradicted.
- Otherwise: inconclusive.

Consistency checks P7 and P8 are reported but do not enter the model verdict.

The E family is separate: at most K = 5 hypotheses, Holm at familywise 0.05, on the confirm half only.

Robustness and secondary specifications, the confirm-only P replication and full-sample E estimates are reported with unadjusted CIs and no verdicts. Benjamini-Hochberg q-values are shown alongside as information.

An E can never change the verdict of a P.

## Blinding enforcement

Three annotated tags, pushed to origin when created and protected by a GitHub tag-protection rule on participation-*, so they are never moved and never force-pushed. Optionally, also timestamp each tag's hash externally (OpenTimestamps or OSF).
- participation-P-freeze (F0): PROTOCOL.md, split.py and split.json, the data manifest (dataset codes and filters), the hand-coded pension table with sources, all estimation and inference code, simulate.py with passing synthetic tests, and the bootstrap seeds.
- participation-E-freeze (F1): e_specs.py with at most 5 coded hypotheses, plus the committed explore outputs each E cites.
- participation-confirm-run (F2): results.

Code guards:
- fetch.py --half {explore, confirm}. It queries the Eurostat API with a geo filter, so confirm values never reach the disk before F1. Every fetch appends {dataset, url, utc, sha256, half} to the committed data/fetch_log.jsonl. Raw files are gitignored; their hashes are committed.
- For half=confirm, fetch.py refuses unless all four hold: the tag exists; git merge-base --is-ancestor participation-E-freeze HEAD; git status --porcelain participation/ is empty; git diff --quiet participation-E-freeze HEAD -- participation/code.
- load.py applies the same guard and asserts that the geos returned are a subset of the allowed set. All analysis code goes through load().
- confirm.py is the only entry point for the look. It writes results/confirm_<HEAD>.json with the code hash. It refuses to run if a committed confirm result already exists; later runs write results/postlook_*.json, labelled as such.

A committed CI check (a GitHub Action, since .git/hooks is not versioned) fails if:
- any fetch_log entry with half=confirm comes from a commit that is not a descendant of the E-freeze tag;
- data/raw/confirm or confirm geo codes appear in tracked data files before F1;
- the first fetch_log entry of any kind is not a descendant of the P-freeze tag. This is the condition for P being primary on the full sample.

Human and agent discipline cannot be enforced in code. That means no browsing Eurostat or OECD for outcome values of confirm countries. State it in participation/STATE.md, disclose prior knowledge and the series already cached in paths/, and rely on the 2026-2028 time holdout as the only test of data no one has seen.

## Primary specifications as proposed

### P1 (distinctive): a rise in q raises the participation of 25-34-year-olds relative to 55-64-year-olds. H1: beta > 0.
- **estimating equation:** D_ct = a_c + d_t + beta * log q_{c,t-1} + g * U_ct + h * EEA_ct + sum_k k_k * B^k_ct + e_ct, where D_ct = LFPR_25-34,ct - LFPR_55-64,ct in percentage points. Each band rate is the equal-weight mean of its 5-year sub-bands, and of the male and female rates. Citizenship = nationals (Eurostat lfsa_argan; verify the code from metadata). Years from the first available year to 2025, excluding 2020 and 2021.
- **measure of q:** log(HICP CP041 actual rentals / HICP non-energy industrial goods), annual average, lagged one year (prc_hicp_aind; verify the codes from the codelist). Robustness checks, with no verdict attached: log(house price index / HICP), log(CP041 / HICP all items), log(CP041 / compensation per employee).
- **fixed effects and controls:** Common rules C1-C8 apply to every P. C1: countries are EU27 + NO + IS + CH + UK; the UK is kept through 2019 only, with no ONS splice. C2: drop 2020 and 2021. C3: each 'b' flag in a series for country c in year tau adds the dummy B = 1[c, t >= tau]. C4: cells flagged 'u' or 'c' are missing; no interpolation; unbalanced panel. C5: rates are in percentage points; bands are equal-weight means of 5-year sub-bands; nationals where available. C6: q as above. C7: countries weighted equally; cluster = country. C8: U_ct is the unemployment rate at 25-74, both sexes (une_rt_a). P1 itself has country and year fixed effects, U_ct (absorbs the different cyclical sensitivity of young and old), and EEA_ct, the mean of male and female earliest pension eligibility ages from the hand-coded table committed at F0. Secondary, reported only: the tenure dose, beta interacted with the baseline 25-34 renter share from SILC 2005-2007; a lead check with q_{t+1}.
- **inference:** Restricted wild cluster bootstrap-t (WCR) with Webb weights, B = 9999, clustered by country, one-sided p for beta > 0. Confidence interval by test inversion. The P verdict comes from the full sample (about 31 countries); the confirm half is reported as the replication.
- **power note:** G is about 31 on the full sample and about 15 on the confirm half. MDE at 80% power is about 2.55 SE on the full sample and about 2.63 times a sqrt(2)-larger SE on the confirm half. Report the MDE from the explore-half variance before the look.

### P2: the share of 25-34-year-olds living with their parents rises with q. H1: beta > 0.
- **estimating equation:** C_ct = a_c + d_t + beta * log q_{c,t-1} + g * UY_ct + sum_k k_k * B^k_ct + e_ct. C_ct is the percentage of 25-34-year-olds living with their parents, both sexes (EU-SILC ilc_lvps08, age band 25-34; verify from metadata). UY_ct is the unemployment rate at 15-29. Years 2005-2025, excluding 2020-2021.
- **measure of q:** As in P1 (rent / non-energy industrial goods, lagged). The draft's 'rent relative to the young's wage' is not available annually, because the Structure of Earnings Survey runs every four years. Rent / compensation per employee is a robustness check only.
- **fixed effects and controls:** Country and year fixed effects, and youth unemployment 15-29 (the prediction says 'holding' it, but it is a possible bad control, so the estimate without it is also reported). C3 applies, notably to the Germany 2020 SILC break.
- **inference:** WCR with Webb weights, B = 9999, one-sided. Full sample is primary; confirm half is the replication.
- **power note:** Within-country variation in coresidence is small, and SILC sampling error at 25-34 is roughly 1 point. Expect a large MDE; a reverse effect (more young people at home lowers rental demand) attenuates the estimate.

### P3: prime-age women's participation rises with q more than men's. Intersection-union test: support needs both beta_gap > 0 and beta_W > 0, each at alpha. The two tests need no adjustment for each other.
- **estimating equation:** Primary: G_ct = LFPR_W,25-54 - LFPR_M,25-54, where each is the equal-weight mean of the six 5-year bands, nationals. G_ct = a_c + d_t + beta_gap * log q_{c,t-1} + g * U_ct + sum_k k_k * B^k_ct + e_ct. Second leg: the same equation with LFPR_W,25-54 as the outcome (coefficient beta_W).
- **measure of q:** As in P1.
- **fixed effects and controls:** Country and year fixed effects, U_ct (cycle), break dummies per C3. Reported as a conditional association, not a causal effect, because the reverse channel has the same sign. Secondary: beta_gap interacted with the baseline renter or mortgagor share at 25-54 (the model's discriminating implication), and a lead check with q_{t+1}.
- **inference:** WCR with Webb weights, B = 9999, one-sided for each leg. P3 is supported only if both legs reject. Full sample is primary.
- **power note:** The W-M gap is less noisy than the levels. Reverse causality and the added-worker effect of 2008-2013 bias in opposite directions, so the sign of the net bias is unknown.

### P4 (distinctive): among young people not in employment, the inactive share rises with the coresidence share. The search reading predicts beta < 0. H1: beta > 0.
- **estimating equation:** I_ct = a_c + d_t + beta * C_ct + g * U_ct + sum_k k_k * B^k_ct + e_ct. I_ct is the percentage of NEETs aged 25-29 who are inactive rather than unemployed (edat_lfse_20 by labour status, both sexes). C_ct is the coresidence share at 25-29 (ilc_lvps08). Years 2005-2025, excluding 2020-2021.
- **measure of q:** Not used in the primary specification. Secondary reduced form: I_ct on log q_{c,t-1} with the same controls.
- **fixed effects and controls:** Country and year fixed effects, U_ct (25-74 unemployment; the cycle pushes I and C apart and so biases towards the search reading), break dummies. Secondary: the outcome restricted to inactive people who do not want to work, which separates discouraged searchers.
- **inference:** WCR with Webb weights, B = 9999, one-sided. Full sample is primary.
- **power note:** Both sides are survey ratios with sampling error. Measurement error in C attenuates beta towards zero, so a null is weak evidence.

### P5: from 2023 on, the employment rate of 20-24-year-olds falls relative to 25-54-year-olds more where pre-2023 clerical exposure was higher. H1: beta < 0.
- **estimating equation:** R_ct = ER_20-24,ct - ER_25-54,ct, both sexes. R_ct = a_c + d_t + beta * X_c * 1[t >= 2023] + sum_k k_k * B^k_ct + e_ct. Years 2016-2019 and 2022-2025. X_c is the share of ISCO-08 major group 4 in employment of 20-29-year-olds, mean of 2018-2019 (lfsa_egais).
- **measure of q:** Not used.
- **fixed effects and controls:** Country and year fixed effects. Under C3, the 2021 break dummy where flagged means beta is identified from 2023-2025 against 2022 for those countries. UK excluded (no post-2019 data). Event-study pre-trend check on 2016-2019, relative to 2022, reported. Secondary: ISCO 2-digit generative-AI exposure index instead of the clerical share.
- **inference:** Randomization inference is primary. Permute X_c across countries within region strata, enumerating exactly if there are 10,000 or fewer permutations, otherwise 9999 draws. The statistic is the studentized CR1 t, and the test is one-sided. WCR is reported alongside.
- **power note:** About 30 clusters and 3 post years, with concurrent rate and energy shocks. Expect this to be underpowered; report the MDE.

### P6: faster population aging goes with a faster fall in the employment share of routine occupations. H1: beta < 0.
- **estimating equation:** Cross-section: dRout_c = a_r(c) + beta * dAgeHat_c + e_c. dRout is the change in the share of ISCO-08 groups 4, 7 and 8 in employment at 15-64, 2011 to 2019, in points. dAgeHat is the predicted change in the ratio of population 56+ to population 21-55, from the 2011 single-year age structure aged forward 8 years with no migration and no mortality (demo_pjan).
- **measure of q:** Not used.
- **fixed effects and controls:** Region fixed effects for the five strata. Secondary checks: realised rather than predicted aging; the window 2011-2025.
- **inference:** Randomization inference, permuting dAgeHat within region strata, studentized HC2 t, one-sided. Wild bootstrap (each country its own cluster, Webb weights) reported alongside.
- **power note:** N is about 31 with 5 region fixed effects, so about 25 degrees of freedom on the full sample. On the confirm half (about 15 countries) it is close to uninformative, which is why P is tested on the full sample.

### P7 (consistency): a later earliest pension eligibility age, meaning less public provision of exit, raises participation at 60-64. H1: beta > 0.
- **estimating equation:** Women-minus-men difference: GP_ct = LFPR_W,60-64 - LFPR_M,60-64; GE_ct = EEA_W - EEA_M (years). GP_ct = a_c + d_t + beta * GE_ct + phi * (LFPR_W,50-54 - LFPR_M,50-54)_{c,t-10} + sum_k k_k * B^k_ct + e_ct. Years 2005-2025, excluding 2020-2021. The phi term controls for the same cohort's gender attachment gap ten years earlier.
- **measure of q:** Not used. Net replacement rates are not annual and appear only in robustness.
- **fixed effects and controls:** Country and year fixed effects absorb all shocks common to a country-year, so the variation comes from reforms that equalise women's pension ages. The cohort attachment control handles the rising attachment of younger cohorts of women. The pension table is hand-coded and committed at F0.
- **inference:** WCR with Webb weights, B = 9999, one-sided. Also report G* and the count of countries where GE varies. If G* < 8, the verdict is 'uninformative'.
- **power note:** The effects in the literature are large (around 10 points per year of eligibility age), so power is good if enough countries reformed.

### P8 (consistency): enrolment at 20-24 rises when labour prospects fall. H1: beta > 0.
- **estimating equation:** S_ct = a_c + d_t + beta * U2554_ct + sum_k k_k * B^k_ct + e_ct. S_ct is the percentage of 20-24-year-olds in formal education, from the LFS (edat_lfse_18 or equivalent; fix the code from metadata before the freeze). U2554 is the unemployment rate at 25-54, both sexes. Years from the first available year to 2025, excluding 2020-2021.
- **measure of q:** Not used.
- **fixed effects and controls:** Country and year fixed effects, and break dummies. The 25-54 rate replaces youth unemployment, whose denominator moves mechanically with enrolment. Bologna degree-length reforms are a known country-specific confounder; they are listed as a limitation, with no ad-hoc dummies.
- **inference:** WCR with Webb weights, B = 9999, one-sided. Full sample is primary.
- **power note:** A long panel with large cyclical variation (2008-2013), so this should be the best-powered P.
