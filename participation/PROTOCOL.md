# Participation — the protocol (pre-registration)

Written 2026-10-08, before any outcome value was downloaded into this thread. The tag
`participation-P-freeze` marks the commit that freezes it, together with the code that runs it. After that
tag nothing below changes; any later departure is written in `STATE.md` as a deviation and labelled
exploratory wherever it is reported.

## 1. The design: guided by the data, tested against something

Three tiers.

1. **P: what the model predicts, stated now.** These predictions come from `pinning/paper/main.tex`
   (Section 7 on the outside option, Appendix B on household participation, the eras section, the
   conditionality appendix). Each one is coded in `code/specs.py` with one primary specification and a
   predicted sign. P is never re-specified. The primary test of each P uses the **full sample** (every country
   is out of sample for a prediction stated before any data). The confirm half alone is reported as a
   clean-room replication.
2. **E: what the data suggest.** The countries are split once into an EXPLORE half and a CONFIRM half
   (Section 4). Any analysis is allowed on the explore half. Whatever it suggests is written as at most
   **five** E-hypotheses, each a function in `code/e_specs.py` with outcome, regressor, sample, controls and
   predicted sign. Each E cites the committed explore output that motivated it. E may only use series in this
   protocol's data manifest. The tag `participation-E-freeze` freezes them.
3. **The one look.** After the E freeze, `code/confirm.py` runs once. It reports:
   - P on the full sample (primary);
   - P on the confirm half (replication);
   - E on the confirm half (the only valid test of E).

   Every result is reported, nulls included. An E that varies a P is labelled as such and never changes that
   P's verdict.

A **time holdout** sits on top: the frozen code is rerun on all countries when the 2026-2028 data are
published. That is the only test on data nobody involved has seen.

## 2. What the model says, and what it does not

For a group *g* (sex × age), the paper's participation comparison is `w_g + m_w ≥ s_g(q) + m_e`, with
`s(q) = max(s0 − q·h_e, s_under)` and `q = r/p`, the price of non-produced services relative to goods.

Three theory critics checked the draft before this freeze (`docs/derivations.md` records their findings).
What survived:

- **The net-housing-position sign is standard.** The sign of d(participation)/dq follows the group's net
  housing position: net short works more when q rises, net long works less. This is the life-cycle hedging
  logic (Sinai–Souleles; house-price wealth effects by age and tenure). It is **not** a test of this model.
  The same holds for "young minus old responds positively to rents" and "women respond more than men".
- **The model's distinctive piece is the floor kink.** Exit to the dependency floor (a parent's home) makes
  `s` flat in q. Past the point where independent exit is unaffordable, a further rise in q no longer pushes
  the young into work. Instead it taxes working while living independently, so their participation response
  shrinks to zero or turns negative. The standard concave income-effect model predicts the opposite: the
  response *grows* as income net of housing goes to zero. Section 5's distinctive tests are built on this
  contrast.
- **The original P4 is dropped.** It said the inactive share of non-employed youth rises with coresidence.
  The model does not imply it, and the search alternative does not predict the opposite sign. Composition
  and reverse causality give the same correlation in any model.
- **The original P7 (pension ages) is dropped for now.** No annual table of earliest pension-eligibility
  ages by country and sex exists as data. The OECD's SDMX holds only the 2024 edition. Coding the table by
  hand from documents is a later unit.

## 3. Sample and measures (common rules C1–C10)

- **C1. Countries:** EU27 + NO, IS, CH, UK; 31 countries. No candidate countries. The UK is kept through 2019
  only, with no splice from ONS.
- **C2. Years:** 2020 and 2021 are dropped from every annual specification. The LFS years with q run from
  1997 to 2025, because the HICP starts in 1996 and q is lagged one year. The SILC specifications run
  2005-2025. Each test uses what exists inside those windows, as an unbalanced panel.
- **C3. Breaks:** every flag containing `b` on an outcome, regressor or control series for country *c* in year τ
  adds the dummy `1[geo = c, year ≥ τ]`. This is mechanical, with no judgement. For lagged q, a flag in year t
  acts from t+1.
- **C4. Unreliable cells:** cells flagged `u` (low reliability) or `c` (confidential) are missing. There is
  no interpolation.
- **C5. Rates:** rates are in percentage points. An activity or employment band (`lfsa_argan`, `lfsa_ergan`) is
  the equal-weight mean of its five-year sub-bands, and of the male and female rates (for example, 25-34 = mean
  of 25-29 and 30-34); it is missing if any sub-cell is missing. These rates are for **nationals**
  (`citizen=NAT`); all residents (`TOTAL`) is a robustness check. Unemployment rates, the education share
  (`edat_lfse_19`) and occupation shares (`lfsa_egais`) use sex T.
- **C6. q, the price of non-produced services relative to goods:**
  `log(HICP CP041 actual rentals / HICP IGD_NNRG non-energy industrial goods)`, annual averages
  (`prc_hicp_aind`, unit `INX_A_AVG`), lagged one year. The robustness measures carry no verdict:
  - `log(house price index / HICP all items)` (`prc_hpi_a` TOTAL; `tipsho20` for Greece);
  - `log(CP041 / CP00)`;
  - `log(CP041 / compensation per employee)` (`nama_10_lp_ulc`, D1_SAL_PER, national currency).

  Known weaknesses: CP041 covers sitting tenants, is regulated in many countries and is attenuated where
  rental markets are small. Balassa–Samuelson in converging economies raises q together with incomes.
- **C7. The cycle:** U_ct is the unemployment rate at 25-74, both sexes (`une_rt_a`, or failing that
  `lfsa_urgan` Y25-74 TOTAL citizenship). The fallback is per country: one source for a country's whole series,
  never spliced. The same rule builds U(25-54) and U(15-29).
- **C8. Weighting and clusters:** countries are weighted equally; the cluster is the country.
- **C9. Floor availability F_c, a predetermined moderator:** the share of 25-34-year-olds living with their
  parents (`ilc_lvps08`, sex T), averaged over the country's first three available years within 2003-2008.
  It is standardised across the 31 countries (mean 0, sd 1). Countries without a value inside 2003-2008 are
  dropped from tests that use F_c.
- **C10. Fetch discipline:** every download is logged in `data/fetch_log.jsonl` with URL, UTC time, half and
  SHA-256. Raw files are not committed. The confirm run downloads all countries in one vintage and reports
  any difference against the logged explore-half hashes.

## 4. The split

`code/split.py`, committed with this protocol (`data/split.json` is its output).

- **Strata:**
  - Nordic: DK, FI, SE, NO, IS
  - Continental: AT, BE, CH, DE, FR, LU, NL
  - Anglo: IE, UK
  - South: CY, EL, ES, IT, MT, PT
  - CEE: BG, CZ, EE, HR, HU, LT, LV, PL, RO, SI, SK
- **Pairing:** within each stratum, countries are ranked by population on 1 January 2010 (`demo_pjan` TOTAL;
  a design covariate, not an outcome) and adjacent countries are paired. One member of each pair goes to each
  half at random.
- **Odd strata:** the leftover country in each odd stratum is assigned at random, subject to the halves being
  15 and 16.
- **Seed:** `int(sha256(b'participation-split-v1|' + ','.join(sorted(codes))).hexdigest()[:16], 16)`, passed
  to `numpy.random.default_rng`.

**What the confirm half may be used for:**
- **Before the E freeze:** nothing beyond metadata (codelists, availability) and the design covariates named
  here (2010 population). The loader refuses confirm geographies.
- **At the look:** one run of `confirm.py`.
- **After the look:** free use, all labelled exploratory.

## 5. The tests

Every regression has country and year fixed effects, the break dummies of C3, and the cycle control U_ct
unless stated. Inference is the restricted wild cluster bootstrap-t (Webb weights, B = 9999, clustered by
country, CR1 statistic), one-sided in the predicted direction, with confidence intervals by test inversion
(`code/inference.py`).

### D: distinctive tests (the model against the standard account)

- **D1. The floor kink across countries.**
  - **Equation:** `A_ct = a_c + d_t + b1·log q_{c,t-1} + b2·(log q_{c,t-1} × F_c) + g·U_ct + breaks + e_ct`.
    A is the activity rate at 25-34, per C5.
  - **H1:** b2 < 0. Where the parental home is a widely used exit, the young's participation responds less
    to rents.
  - **Standard account:** b2 ≥ 0.
  - **Reported with no verdict:** the implied slope `b1 + b2·F` at the top-quartile F (the 75th percentile of
    standardised F over the D1 sample's countries).
- **D2. The floor kink over time.** The same outcome on `log q_{c,t-1}` and `(log q_{c,t-1} − m_c)²`, where
  m_c is the country's mean of log q over its sample.
  - **H1:** the coefficient on the square is < 0. The response weakens as rents rise within a country.
  - **Standard account:** ≥ 0.

### C: consistency checks (shared with standard models; they test the model's mapping, not its mechanism)

- **C-1. Coresidence absorbs rents.**
  - **Equation:** `ilc_lvps08` 25-34 (sex T) on `log q_{c,t-1}`; years 2005-2025.
  - **H1:** b > 0.
  - **Secondary, no verdict:** with youth unemployment at 15-29 added (it is a mediator); and interacted with
    the 55-64 outright-owner share (`ilc_lvps05` OWN_NL, mean of 2015-2017, flagged as not predetermined).
- **C-2. Young against old.**
  - **Equation:** `A(25-34) − A(55-64)` on `log q_{c,t-1}`.
  - **H1:** b > 0.
  - **Known confound:** pension reforms, with no pension control available. Robustness: country-specific
    linear trends.
- **C-3. Second earners.** An intersection–union test with two legs, both of which must reject:
  - `A_W(25-54) − A_M(25-54)` on `log q_{c,t-1}`, H1 > 0;
  - `A_W(25-54)` on `log q_{c,t-1}`, H1 > 0.

  This is reported as a conditional association, because the reverse channel has the same sign.
- **C-4. Entrants first.**
  - **Equation:** `E(20-24) − E(25-54)` (employment rates) on `X_c × 1[year ≥ 2023]`, with years 2016-2019
    and 2022-2025.
  - **Exposure X_c:** the share of ISCO-08 major group 4 (clerical support) in employment at 15-24
    (`lfsa_egais`), mean of 2018-2019.
  - **Sample:** the UK is excluded (it has no post-2019 data).
  - **H1:** b < 0.
  - **Inference:** randomisation inference is primary. X_c is permuted within strata, with a studentised
    statistic.
  - **Pre-trend:** an event-study check on 2016-2019, reported. Low power is expected; a null is
    uninformative.
- **C-5. Aging pulls the margin.**
  - **Cross-section:** the change in the share of ISCO-08 groups 4, 7 and 8 in employment at 15-64 from 2011
    to 2019, on predicted aging.
  - **Predicted aging:** the 2011 single-year age structure (`demo_pjan`) aged forward eight years with no
    migration and no mortality. The measure is the change in the ratio of population 56+ to 21-55.
  - **Controls:** stratum fixed effects only (no year effects, no cycle control).
  - **H1:** b < 0.
  - **Inference:** randomisation inference within strata (HC2-studentised). The UK enters with the
    2011-2019 change.
  - **Breaks:** C3's dummies have no panel to act on in a cross-section. The `b` years inside 2012-2019 on the
    occupation cells are reported per country; a robustness run drops those countries.
- **C-6. School as a paid exit.**
  - **Equation:** the share of 20-24-year-olds in formal education (`edat_lfse_19`, wstatus POP, training
    FE) on U(25-54), within the LFS window (the series starts in 2004).
  - **Controls:** none beyond the fixed effects and breaks; the regressor is the cycle, so U_ct is not added.
  - **H1:** b > 0.
  - **Secondary, no verdict:** `log q_{c,t-1} × (1 − share of students aged 18-24 living with their parents)`
    (`ilc_lvps09` EDUC, first three years within 2003-2008), predicted sign < 0.

### Verdicts

- **Supported / contradicted / inconclusive (per test):**
  - *supported* when the one-sided p-value survives Holm within its family at familywise 0.05;
  - *contradicted* when the one-sided p-value for the opposite sign survives Holm;
  - *inconclusive* otherwise.
- **Rests on one country:** every primary test is rerun leaving out each country in turn. A supported or
  contradicted verdict whose one-sided p in its own direction exceeds 0.10 when some single country is left out
  carries the qualifier "rests on one country (XX)". The model-level verdict carries the qualifiers of the D
  tests it rests on. The effective number of clusters G* (Carter, Schnepel and Steigerwald) is reported but not
  acted on. (Changed before the freeze, on the pre-freeze simulations: a "design uninformative below G* = 8"
  rule would have voided D1 in about a third of full-sample designs, while the bootstrap kept its 5% size in
  exactly those designs, a dominant country included. What low G* signals is dependence on few countries, which
  the leave-one-out run measures directly.)
- **Families:** D = {D1, D2}; C = {C-1 … C-6}; E = up to five, tested on the confirm half only. Holm runs over
  the whole family.
- **The model against the standard account:**
  - *favours the model*: at least one of D1, D2 is supported and neither is contradicted;
  - *against the floor mechanism*: either is contradicted;
  - *inconclusive* otherwise.
- **What C does and does not settle:** C verdicts speak to the model's mapping onto groups. They do not
  settle the model against the standard account.

Each test also reports the point estimate, the CR1 standard error, the number of country-years, G*, and the
minimum detectable effect computed from the explore-half variance before the look.

**Robustness, with no verdicts** (C-3 means both legs):

| Run | Applies to |
|---|---|
| all residents instead of nationals | D1, D2, C-2, C-3, C-4 |
| each alternative q measure of C6 | D1, D2, C-1, C-2, C-3 |
| country-specific linear trends | D1, D2, C-1, C-2, C-3, C-4, C-6 |
| stacked non-overlapping five-year long differences (1997, 2002, …, 2022) | D1, D2, C-1, C-2, C-3, C-6 |
| excluding 2008-2013 | D1, D2, C-1, C-2, C-3, C-6 |
| a lead check (q_{t+1} added) | D1, D2, C-1, C-2, C-3 |
| countries with occupation breaks in 2012-2019 dropped | C-5 |

## 6. Disclosed prior knowledge

Everyone involved, the AI agents included, knows the broad European facts, among them:
- high coresidence in the South and East, low in the Nordics;
- the Spanish, Irish and Greek housing busts;
- German and Italian pension reforms;
- Swedish rent control.

The repository's `paths/` thread holds:
- ILO employment-by-activity series for DE, ES, IT, NL and SE;
- US participation series (FRED);
- US findings on prime-age participation since 2023.

The US is not in this sample. The data scouts of 2026-10-08 fetched small slices of these tables to verify the
codes; their reports contain coverage only, and the analyst read no values. Because country-level prior
knowledge cannot be removed, the time holdout is the only clean test.

## 7. Bug policy

Between the P freeze and the E freeze, plumbing (fetching, parsing, variable construction) may be fixed when it
is wrong, each fix in its own commit with the reason; a change to a test's content (outcome, regressor, sample,
controls, sign) is a deviation, recorded in `STATE.md`, and that test's primary falls back to the confirm half.
`confirm.py` refuses to run unless `participation/code` is unchanged since the E freeze.

A bug found after the look is fixed in a new commit, and both the original and the fixed results are reported
together with the diff. No refetch after the look, except under this policy.
