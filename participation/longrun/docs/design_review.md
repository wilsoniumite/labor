# Long-run design review — a backward-holdout protocol (methodologist, 2026-10-08, no data)

## Outline

BACKWARD HOLDOUT ('L' study). An addendum to PROTOCOL.md, written and tagged before any long-run value is fetched. Nothing below required looking at data.

0. SCOPE AND WHAT IS ALREADY SEEN
- Unseen cells:
  - H-EU: the 31 European countries, observation years 1950-1996. European observation years are capped at 1996, so the lagged q year is at most 1995 and no seen 1997-2025 Eurostat cell enters.
  - H-NE: non-European OECD members (US, CA, AU, NZ, JP, KR, and others that pass coverage), 1950-2025. Observation years 2020 and 2021 are dropped, as in C2.
- Excluded country-years: COMECON members through 1990 (a mechanical metadata rule). Administered rents and near-universal participation make q meaningless there.
- Partially seen, listed in the addendum's prior-knowledge section:
  - US: the paper's shelter-vs-goods fork for 1950-2025 is effectively US q. paths/cache holds CLF16OV, CE16OV, UNEMPLOY, AHETPI and others. paths/ holds the US prime-age findings since 2023.
  - DE, ES, IT, NL, SE: ILO temporary-employment series in paths/cache/ilo (not participation).
  - Before the freeze, grep every cache and fetch log in the repo and list every country × series already on disk.
- Code layout: a new directory, participation/longrun/. It imports participation/code/inference.py and the helpers in specs.py (break_dummies, holm, holm_reject, verdicts, qualify) without editing them. A check asserts those files' SHA-256 equal their contents at the participation-E-freeze tag.

1. TESTS: the frozen P, adapted mechanically. No new P.
- D1-L: A2534 on log q_{c,y-1} × F_c, with log q_{c,y-1} and the cycle C_cy. Fixed effects: country × segment and grid-period. H1: b2 < 0. Same 'standard account' and the same no-verdict top-quartile slope as D1.
- D2-L: A2534 on log q and (log q − m_cs)². m_cs is the mean within country × q-segment, because a level shift in a spliced q is not absorbed by a square. H1 < 0.
- C-L family:
  - always: C-2 (A2534 − A5564 on q, H1 > 0) and C-3 (both legs, intersection-union);
  - only if the coverage rule in step 3 passes: C-1 (census coresidence of 25-34 on q) and C-6 (enrolment of 20-24 on the cycle).
  - C-4 and C-5 are not carried: their objects (2023+ entrants; ISCO-08 2011-2019) do not exist before 1997.
- Replication of a surviving E: E-SCH1 (enrolment of 20-24 on the previous year's cycle) joins the C-L family if C-6's data qualify. E-HF1 and E-OCC1 failed on fresh countries and are not re-tested; they may run as exploratory only.
- Variables:
  - q = log(rent index / CPI all items), one rule for every country. Source ladder: the Jorda-Schularick-Taylor Macrohistory rent index and CPI (18 countries), else the OECD CPI rent component / CPI all items.
  - C (the cycle) = the Hamilton-filter residual of log real GDP per head (annual, h = 2, two lags), one source per country (Maddison Project, or JST). It is measured at the observation year.
  - F_L = the share of 25-34-year-olds living with a parent in the earliest census with 1955 <= year <= 1975 (IPUMS-International tabulations or national census tables), standardised over the D1-L countries. A country without such a census is dropped from D1-L. No proxy substitutes (for example, marriage age).
  - A2534 = equal-weight mean of the sexes, and of the 25-29 and 30-34 bands where those exist (C5's rule). Otherwise the 25-34 band directly. Otherwise the both-sexes total. Each change of construction is a segment break (section 'splice rules').
- Model-level verdict: as frozen ('favours the model' / 'against the floor mechanism' / 'inconclusive'), on D1-L and D2-L only.

2. INFERENCE (implementable with the existing inference.py)
- WCR (Webb weights, B = 9999, CR1, cluster = country), one-sided, as frozen.
- D1-L: randomisation inference is co-primary. inf.ri with x_unit = F_c and x_mult = log q_{c,y-1}, permuted within strata, CR1-studentised, with log q kept in Z. The verdict p is max(p_WCR, p_RI); p_opposite is the max of the opposite p's. This is valid whenever either procedure is valid.
- D2-L: WCR. Plus a no-verdict series-permutation placebo: each country's q path is replaced by another country's, among those with matching coverage.
- Size check before the freeze, step L3. Every test is simulated on the real coverage skeleton with synthetic values: AR(1) errors with rho 0.5 and 0.9 at five-year spacing, country trends, and trends by F group. Variance parameters come from the European look, which is already seen and allowed.
  - If a test's simulated size at nominal 0.05 exceeds 0.075, its verdict threshold becomes the simulated 5% quantile of null p (a size-corrected alpha).
  - This rule and its outputs are frozen at participation-L-freeze.
- G* reported, not acted on. Leave-one-country-out qualifier as frozen (LOO_P = 0.10). Leave-one-stratum-out reported without a qualifier.
- Testability floor: a test runs only if at least 8 countries have at least 2 observations inside one overlapping outcome segment × q segment. This is computed from coverage, before values. Otherwise the test is 'not testable' and leaves its family before the look.

3. DECIDED AFTER COVERAGE SCOUTING, BEFORE VALUES
The rules are written now. Code applies them to the availability cube.
- Which countries enter each test, by step 2's testability floor and the COMECON rule.
- Which source each series uses per country, by the ladder written now ('extend, don't fill').
- The segment table: one row per break, each with a metadata citation.
- The grid mapping, the testability of C-1, C-6 and E-SCH1, and hence the size of each Holm family.
- The strata and the explore/confirm split.
- The F_L census year per country.
- The skeleton simulation's size correction, and the pre-look MDE per test (from the European look's variances, scaled to the skeleton).
- Forbidden before the look: anything computed from a value. That covers plots, means and ranges, outlier rules, choosing between sources by fit or correlation, and 'sanity checks' that print numbers.

4. FAMILIES, MULTIPLICITY AND READING
- Families and Holm:
  - D-L = {D1-L, D2-L};
  - C-L = the carried subset (at most 5, E-SCH1 included);
  - E-L = at most 3 data-suggested hypotheses, tested on the confirm half only.
  - Holm runs over each whole family at 0.05, with sizes frozen from coverage.
- No-verdict list, enumerated and capped at 8 robustness runs:
  - q_hpi;
  - goods-denominator q where a national CPI-goods series exists;
  - unemployment (AMECO) as the cycle;
  - an annual panel;
  - five-year differences within segments;
  - overlap-ratio splices;
  - men only / women only;
  - drop strict rent control.
- Mechanical qualifiers, beyond the frozen leave-one-out one. A D verdict carries:
  - 'rests on floor-group trends' if adding F_c × period fixed effects flips its sign or pushes its own-direction p above 0.10;
  - 'rests on cohort size' if the same happens with relative cohort size (UN WPP population 25-34 / population 35-64) as a control;
  - 'indistinguishable from trend curvature' (D2-L only) if the observed t lies inside the central 80% of the series-permutation placebo distribution.
- Two holdouts, two verdicts:
  - The European look and the L study each carry their own verdict. There is no ex-post Fisher or Stouffer combination.
  - A decision table written now:
    - contradicted in either study → 'against the floor mechanism';
    - supported in L and not contradicted in Europe → 'supported in the long run, not in 2009-2025 Europe';
    - otherwise inconclusive.
  - An inverse-variance pooled b2 is reported with no verdict.
- Reading rule for 'imperfect data', written now:
  - a contradiction stands whatever the data quality;
  - an inconclusive result whose pre-look MDE is at or below the European full-sample MDE reads 'no support';
  - above it, it reads 'uninformative'.

5. TIMELINE AND TAGS (local, like the existing ones)
- L0: write PROTOCOL_LONGRUN.md and commit it.
- L1: blind coverage scouting.
- L2: the coverage decisions, produced by code.
- L3: the skeleton simulation, the MDEs and the prior-forecast sheet. Then tag participation-L-freeze.
- L4: explore half (free); at most 3 E-L in longrun/code/e_specs_longrun.py. Then tag participation-LE-freeze.
- L5: confirm_longrun.py runs once on one vintage; the result is committed immediately.
- L6: free exploratory use of everything. New hypotheses go only to the 2026-2028 time holdout, or to OECD members never fetched.
- Bug policy as in section 7:
  - a plumbing fix is allowed only when the code departs from the frozen text;
  - any change to a rule is a deviation, and that P-L test's primary falls back to the confirm half.

## Holdout design

RECOMMENDATION: no new holdout for the P tests. One country split for any new E. The time split is demoted to a stability report.

(a) P-L needs no internal holdout.
- D1-L, D2-L and the C-L checks are the predictions already written down and tested on Europe. Every pre-1997 country-year and every non-European country-year is out of sample for them.
- A further split would cut the cluster count of a test that already has about 10-22 clusters, where the D1-L clusters are limited by the F_L census.
- So P-L's primary is the full set of unseen country-years. The confirm half is reported as a replication, as in PROTOCOL section 1.

(b) Give the researcher a broad look without spending the whole test: mirror the European design across countries.
- Strata, each run in 1960 population order (UN WPP; a design covariate):
  - Nordic: DK, FI, NO, SE, IS;
  - Continental: AT, BE, CH, DE, FR, LU, NL;
  - Anglo: IE, UK, US, CA, AU, NZ;
  - South: ES, IT, PT, EL, CY, MT;
  - Asia: JP, KR;
  - any other OECD member that passes coverage goes to a residual stratum.
- Only countries that pass the coverage rule enter.
- Adjacent countries are paired; one of each pair goes to each half. Seed: int(sha256(b'participation-longrun-split-v1|' + sorted codes).hexdigest()[:16], 16).
- Forced placement: the US (whose q and aggregate participation are partly seen through the paper and paths/) is placed in EXPLORE by rule, and its pair partner goes to CONFIRM. The confirm half then holds no country whose long-run q path anyone has studied.
- The explore half is open for free analysis over 1950-1996 (non-European countries over all years) from participation-L-freeze. That is the broad look.
- At most 3 E-L may be frozen, not 5: each half has only about 5-11 clusters, so the confirm-half MDE is roughly 1.45 × 2.6 full-sample standard errors.
- The confirm loader refuses confirm countries until participation-LE-freeze, using the same guard pattern as eurostat.guard.

(c) The time split (explore 1950-1972, confirm 1973-1996) is rejected as a holdout. Five reasons:
1. The cut coincides with the regime change: the oil shock, decontrol of rents in several countries, the inflection in women's participation, and the arrival of early-retirement schemes. A failed replication could not be told apart from the model's own regime dependence (Proposition 7.1(i), the idle margin).
2. Coverage is asymmetric. Before 1973 the data are mostly census-year and mostly European; after 1973 they are mostly annual surveys. The two halves measure different things.
3. The halves share countries, country fixed effects and persistent shocks, so the 'confirm' half is not independent of the explore half.
4. Whoever explores 1950-72 for a country knows that country's later history.
5. Country × segment fixed effects would be estimated within each half, discarding the seam.
Keep it as one pre-registered no-verdict report: the D1-L and D2-L coefficient difference between grid periods up to 1970 and from 1975, two-sided.

(d) After the look (L6), everything is exploratory.
- New long-run hypotheses are tested only on:
  - the 2026-2028 time holdout, for the non-European countries;
  - OECD members never fetched, if any remain.
- They are never re-tested on L data.

(e) Two paths, and the choice is hers.
- She may prefer 'look first, explore after': run P-L on all countries before anyone browses the long-run data, then explore everything.
- That is cleaner for P-L: no explore-half plumbing fixes made with data in view. But no E tier then has a confirm half.
- Recommended default: the mirrored path (b). The bug policy and the segment table frozen at L-freeze limit what exploration can change.

## Splice rules

Principle: a splice is a fixed effect. No series is ever ratio-linked, interpolated or backcast in a primary run. Every rule is written before scouting and applied by code to metadata.

S1. Source ladder per series, written now. Coverage then picks the source mechanically.
- A2534, A5564, AW2554, AM2554, in rank order:
  1. OECD DSD_LFS@DF_LFS_INDIC 5-year bands;
  2. OECD broad band 25-34 (only if 5-year bands are absent);
  3. a national LFS from an official statistical office or the ILO yearbook / LABORSTA archive;
  4. census tabulations (IPUMS-International aggregates or national census reports).
  Model-based series (ILO EAPEP estimates and projections, UN modelled series) are excluded from the ladder.
- q: the JST rent index / JST CPI, else the OECD CPI rent component / CPI all items, else national CPI rent / CPI all items. q_hpi (robustness): JST or OECD real house prices.
- Cycle: Maddison or JST real GDP per head (one source per country). Unemployment (AMECO ZUTN) is robustness only.
- F_L: the earliest census in 1955-1975, IPUMS-I aggregate first, national tabulation second.
- Enrolment 20-24 (for C-6 and E-SCH1): census 'student' status, or national LFS.

S2. 'Extend, don't fill.' A country's series takes its highest-ranked source over that source's longest contiguous run. A lower-ranked source may only extend that run backwards or forwards. It never fills gaps inside a higher-ranked run. Inside a run, a gap stays missing.

S3. Segments. A new segment starts, for a given country and series, at every one of the following:
- a source switch;
- a break flag in the source metadata (OECD 'B', Eurostat 'b', national 'series break' notes);
- a documented survey redesign or definitional change listed in source documentation (age floor 14→15→16; civilian vs total labour force; reference week vs usual status; unpaid family workers counted or not; census vs survey);
- a change in how the band is built (sub-bands vs a direct band; sexes vs total);
- a territorial change (DE 1991, with West Germany as an earlier segment in the same DE cluster; any other territorial change).
The table longrun/data/segments.csv (geo, series, tau, reason, citation) is compiled from documentation alone, by an agent given no values, and frozen at L-freeze. A break found later counts as plumbing only if its documentation predates the look and a citation is given; otherwise it is a deviation.

S4. Estimation:
- Every segment start tau of every series in a regression (outcome, tested regressor and controls) adds 1[geo = c, year >= tau]. This is C3 generalised and reuses specs.break_dummies unchanged. With a country-level moderator, this makes the regression equivalent to country × segment fixed effects for outcome and q, since a level shift delta in q makes Q × F shift by delta × F_c, which is constant within the segment.
- D2-L demeans q within country × q-segment.
- A segment with one observation contributes nothing to identification. The count of such segments is reported.

S5. Overlaps:
- When two sources overlap, the higher-ranked one is used. The overlap years serve only the no-verdict robustness run 'ratio splice': the mean log ratio over at least 2 overlap years, applied to the lower-ranked segment.
- Overlaps are never used to choose a source.

S6. Five-year panel, the primary:
- Grid years 1950, 1955, ..., 1995 for Europe; 1950, ..., 2025 for non-European countries.
- Each grid point takes the nearest available observation year within ±2; ties go to the earlier year.
- European observation years must be ≤ 1996. Observation years 2020 and 2021 never count, so grid 2020 takes 2019.
- q (lagged one year), the cycle and the controls are aligned to the actual observation year, not the grid year.
- Fixed effects are grid-period fixed effects.

S7. Annual panel, robustness:
- only segments from annual surveys, observation years ≥ 1960;
- the same segment rules;
- annual year fixed effects.

S8. Five-year differences, robustness: only within a segment, never across a seam. Breaks are differenced as in specs.long_differences.

S9. Unit conventions:
- rates in percentage points;
- a missing sub-cell makes the band missing;
- cells flagged unreliable or estimated are missing (C4);
- no outlier rule of any kind.

S10. Hand transcription, for printed censuses and yearbooks:
- Two isolated agents enter each table, without the hypotheses and without q.
- A script compares the two entries and reports mismatched cell identifiers only.
- A third agent resolves the mismatched cells from the source image.
- Transcripts are stored by hash outside git until the relevant tag. Analysts never open them before then.

S11. Licensing (the repository's public-data wall):
- Only public sources: JST, Maddison, OECD, UN WPP, AMECO, Kholodilin's regulation index.
- IPUMS-I requires her registration, and the account is hers to create. Its microdata may not be redistributed, so only aggregate tabulations, with the citation, are committed.

## Loopholes and fixes

- Part of the data is already seen. The paper's 1950-2025 shelter-vs-goods fork is essentially US q, paths/cache holds US aggregate labour-force series, and agents know the US prime-age findings since 2023. The US is also the most data-rich long-run country, so it could carry a verdict whose direction was effectively known.
  - *Fix:* Before the freeze, grep every cache and fetch log in the repo and list each seen country × series in the addendum. Place the US in the explore half by rule. The leave-one-country-out qualifier names the US if a verdict rests on it, and a 'without seen countries' run is reported with no verdict.
- Splices chosen with history in mind. Ratio-linking at a chosen overlap, or picking which source 'looks right', moves levels and trends without anyone seeing a regression.
  - *Fix:* No ratio splicing in a primary run: every seam becomes a segment fixed effect (S3, S4). The source ladder and 'extend, don't fill' are written before scouting. segments.csv is compiled from documentation only, with a citation per break, and frozen at L-freeze.
- Model-based or interpolated sources (ILO EAPEP 1950-2010, modelled ILOSTAT estimates, linear backcasts like the paper's energy series) put smooth artificial within-country curvature and false precision into the panel. That is exactly what D2 reads as a floor kink.
  - *Fix:* Only measured observations count. Any value flagged estimated, interpolated, projected or modelled is missing. No backcast enters a primary run.
- D2 is close to a country-specific quadratic time trend: in Europe one country (IE) supplied 61% of its variation. In the long run q rises almost monotonically everywhere as goods cheapen, so (q − m)² is a U shape in time. That shape is confounded with the S-curve of women's participation and the expansion of education.
  - *Fix:* Add a series-permutation placebo: each country is given another country's q path, among those with matching coverage. D2-L carries the qualifier 'indistinguishable from trend curvature' if its t lies inside the placebo's central 80%. G* and each country's share of the tested variation are reported.
- Known postwar timing confounds D1. High-F countries (the South, possibly Japan) had a late surge in women's participation and a late expansion of schooling while q was rising, so b2's sign could follow from known history.
  - *Fix:* Add the mechanical qualifier 'rests on floor-group trends', triggered if adding F_c × period fixed effects flips b2's sign or pushes its own-direction p above 0.10. The primary keeps the frozen form, so the specification is not chosen by knowledge of the confound.
- Cohort size (Easterlin). When the baby boom entered ages 25-34 (1970s-80s) it raised rents and depressed young people's wages and participation, which can produce a spurious q-participation link.
  - *Fix:* Add the qualifier 'rests on cohort size', triggered if adding relative cohort size (UN WPP population 25-34 / population 35-64, one source) as a control flips the sign or pushes p above 0.10.
- Rent control. CPI rent indices in the 1950s-70s track controlled sitting-tenant rents, flat through a freeze and jumping at decontrol. Decontrol dates are policy-timed and correlated with the cycle, so q is mismeasured, and coding control eras by hand invites selection by history.
  - *Fix:* q_hpi (log real house prices) as robustness. Robustness runs that drop 'strict control' country-years, using a pre-existing published coding (Kholodilin's rental-regulation index), with the threshold fixed now. No home-made rent-control dummies.
- Changes in how women's activity was recorded (unpaid family workers on farms) and switches between census and survey produce level jumps and trend breaks in A2534, concentrated in the South and Japan.
  - *Fix:* Every such switch is a segment break (S3), and the equal sex weighting is kept. A men-only outcome run is reported with no verdict. The no-verdict agricultural-share heterogeneity is the only regime moderator.
- The paper's own history ('four configurations'; the idle margin in Proposition 7.1(i)) offers a ready post-hoc reason to discard periods that disagree ('the commons still held in the 1950s').
  - *Fix:* Any prediction that depends on regime is written before the freeze, or it does not exist. The only one allowed is the pre-registered, no-verdict split by agricultural employment share (one source, threshold fixed now). Any era split after the look is labelled exploratory.
- Motivated reading of an 'imperfect data' null. The stated prior is that the model works best back to 1950, so an inconclusive or contradicted result could be put down to data quality.
  - *Fix:* Publish each test's MDE before the look, from the coverage skeleton and the European variances. A reading table, written now:
- 'contradicted' stands whatever the data quality;
- 'inconclusive' reads 'no support' if the MDE is at or below the European full-sample MDE;
- otherwise it reads 'uninformative'.
- Broad prior knowledge of postwar history steers the analysis in ways that cannot be removed (female participation, early-retirement schemes, the German reunification, the Spanish transition, Japanese and Korean growth). The AI agents also know the published literature on these data.
  - *Fix:* Extend the disclosed-knowledge list. Before the look, each participant fills a forecast sheet with a sign and a probability for every P-L test; the sheets are committed with L-freeze and reported beside the results. A result that matches every forecast is noted as 'not news'. Debugging runs on a blinded panel, with q paths permuted across countries by a hidden seed. The pipeline is unblinded once, at the look.
- Thresholds set after scouting could be tuned to keep or drop particular countries known to be informative (for example, admitting a census year in order to keep Italy's 1950s).
  - *Fix:* The thresholds (the testability floor, the ±2 grid window, the F_L census window 1955-1975, the COMECON rule) are written in L0, before scouting. Code produces the coverage decisions from the availability cube. Any human override is logged with its reason, and an 'every country with any data' run is reported.
- Few, high-leverage clusters. F is skewed, with few high-F countries, and roughly 10-22 clusters in all. A WCR with Webb weights can over-reject when the tested variation concentrates in 2-4 countries.
  - *Fix:* For D1-L, randomisation inference permuting F within strata is co-primary, and the verdict uses max(p_WCR, p_RI). A skeleton simulation sets a size-corrected alpha when simulated size exceeds 0.075. The frozen leave-one-out qualifier is kept; leave-one-stratum-out is reported.
- Explore-half plumbing fixes could become rule changes driven by values. The long-run pipeline has far more construction choices than the Eurostat one.
  - *Fix:* The frozen bug policy applies. A fix is plumbing only if the code departed from text frozen at L-freeze. Any change to a rule is a deviation, and that P-L test's primary falls back to the confirm half. The confirm loader refuses confirm countries before participation-LE-freeze. A hash check holds the frozen participation/code unchanged.
- Seen 1997-2025 European data could leak into the backward test through the ±2 grid window, through segments that run past 1996, or through overlap splices.
  - *Fix:* European observation years are capped at 1996 (q lag year at most 1995). Segment effects are estimated only from observations inside the window. Overlap ratios enter only the no-verdict 'ratio splice' run.
- A time split as the holdout (1950-72 / 1973-96). Regime, coverage and serial dependence are all confounded with the cut, and the explorer knows the later history.
  - *Fix:* Use a matched-pair country split, with the US forced into the explore half, for any E. The time comparison stays as one two-sided report with no verdict.
- Cherry-picking across the two holdouts and the many variants: whichever of Europe or the long run, or whichever robustness run, supports the model gets cited.
  - *Fix:* Each study carries its own verdict. A cross-study decision table is written now. The pooled b2 carries no verdict. The no-verdict list is enumerated and capped at 8 runs. The size of each Holm family is frozen from coverage before values.
- F is not predetermined. A 1960s-70s census postdates the 1950s outcomes, and the SILC 2003-08 F is both seen and later than everything. Substituting a proxy such as women's marriage age would itself be a choice informed by known Southern patterns.
  - *Fix:* The primary F_L is the earliest census in 1955-1975. D1-L is also run on years at or after each country's census year, with no verdict. The SILC-era F is robustness, labelled 'not predetermined'. A country without F_L is dropped from D1-L, with no proxy.
- q and the cycle differ in definition from the European primary (rent / CPI all items instead of rent / non-energy goods; GDP gap instead of U25-74). Comparing coefficients across the two studies could mislead.
  - *Fix:* D-L replicates the mechanism's sign, not the European coefficient. A goods-denominator q is run where a national CPI-goods series exists. Unemployment (AMECO) is run as the cycle. Both carry no verdict, and pooling across the studies carries no verdict.