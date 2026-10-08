# Participation — the long-run protocol (an addendum to PROTOCOL.md)

Written 2026-10-08, after the European look and before any long-run outcome or regressor value was downloaded or
read into this thread (the scouts' incidents are listed in section 7). The tag `participation-L-freeze` marks the
commit that freezes it, together with the code that runs it, the coverage decisions, the segment table, the split,
the pre-look MDEs and the filled forecast sheets (`FORECASTS.md`). After that tag nothing below changes; any later
departure is written in `STATE.md` as a deviation and labelled exploratory wherever it is reported.

`participation/PROTOCOL.md` (the European protocol) governs everything this addendum does not restate. Nothing here
changes a European verdict. Where the two differ, this addendum governs the long run only.

Her decisions of 2026-10-08 fix the scope, the floor measure and the distinctive test. The three reviews in
`longrun/docs/` (data inventory, derivations, design review) supply the rest; section 10 lists what was taken from
them and where this protocol departs.

## 1. The design

Three tiers, as in Europe, plus one study that carries no verdict.

1. **P-L: what the model predicts for the long run, stated now.** Each test is coded in `longrun/code/specs.py`
   with one primary specification and a predicted sign. Its primary uses **every unseen country-year** (section
   3, L1-L2): every one of them is out of sample for a prediction written before any long-run data. The confirm
   half alone is reported as a replication. There is no internal holdout for P-L.
2. **E-L: what the long-run data suggest.** The countries are split once into an EXPLORE and a CONFIRM half
   (section 4). From the L-freeze, any analysis is allowed on the explore half. Whatever it suggests is written as
   at most **three** E-L hypotheses in `longrun/code/e_specs.py`, each with outcome, regressor, sample, controls,
   predicted sign and the committed explore output that motivated it. E-L may only use series in this protocol's
   manifest. The tag `participation-LE-freeze` freezes them.
3. **The one look.** After the LE-freeze, `longrun/code/confirm.py` runs once. It reports P-L on all unseen
   country-years (primary), P-L on the confirm half (replication) and E-L on the confirm half (the only valid test
   of E-L). Every result is reported, nulls included.

**The US deep study (section 6) carries no verdict.** The US from 1948 (CPS by sex and age, BEA tenant rent over
goods, Census coresidence and enrolment) is studied as one country. The paper has already used US long series, so
whatever the US shows on its own settles nothing. The US also enters the panel as one country among the others.

**The time holdout** stays the only clean test: the frozen long-run code is rerun on the non-European countries
when the 2026-2028 data are published.

## 2. What the model says for 1950-1996, and what it does not

The participation comparison is the European one: `w_g + m_w ≥ s_g(q) + m_e`, with
`s(q) = max(s0 − q·h_e, s_under)` and `q = r/p` (paper, section "The outside option: pricing exit"). The theory
critic's derivations (`longrun/docs/derivations.md`) found the following. This protocol adopts them.

- **The pooled floor kink is unsigned over the long run.** With floor-available and floor-less young people, the
  q × F interaction runs 0 → + → − → + as q rises through the floor thresholds (LR-K1). The European D1 sign
  (b2 < 0) is the model's prediction in one of those four regimes only. The early decades, at low q and often
  under rent control, are mostly years in which the model and the standard account agree. A pooled D1 or D2 over
  1950-1996 therefore averages opposite-signed regimes. **D1-L and D2-L run with no verdict.**
- **The distinctive prediction is regime-aware and within country (LR-K2).** In high-floor countries the young's
  participation slope on q should fall, from the low-q part of each country's own history to the high-q part, to
  zero or below. In low-floor countries it should stay positive. Section 5's distinctive test is built on this
  difference in differences, with terciles of q fixed by a rule on q alone.
- **What the distinctive test is distinctive against.** LR-K2 discriminates the floor mechanism from an
  income-effect model with **no coresidence option**, which predicts a convex, rising response everywhere (so the
  difference in differences is about zero and the high-q slope positive). It does **not** discriminate the floor
  mechanism from life-cycle models in which parents supply a room below market rent (Kaplan 2012, "Moving back
  home"; Ermisch's household-formation models). Those models produce the same sign path, shifted in location. A
  supported LR-K2 says the young behave as if a flat parental floor exists; it does not say this model's account
  of it beats Kaplan's or Ermisch's.
- **The regime claim, written down now.** The model places the high-q part of a high-floor country's history past
  the floor-types' enclosure point (regime (iii)), so the young's slope there is ≤ 0. The European 2009-2025
  leanings against the kink (D2's p_opposite 0.064; the confirm half's rent × F of +9.1) are not re-read after the
  look as regime (ii) or (iv). If LR-K2 is contradicted, no regime reinterpretation rescues it.
- **Signed but not distinctive.** Before enclosure the young's slope on q is positive and convex (LR-Y0), the same
  as the income-effect account; under binding rent control it is about zero (LR-RC), because the CPI rent prices
  sitting tenants. Coresidence rises with q (LR-C1), as in Ermisch- and Kaplan-type models. School is a paid exit
  whose take-up rises with prime-age unemployment (LR-S1), as in the standard schooling literature. These are the
  consistency checks of section 5.
- **Unsigned by the model over the long run, so run with no verdict.** The young-minus-old gap (C-2) and the
  second-earner response (C-3). For young women before about 1975 the operative floor was the marital household,
  whose response to q follows the couple's net housing position (renters +, owners ≤ 0; LR-F1); the old's
  response follows their own net position (owners net long, LR-O1). Without tenure data, neither sign is fixed.
- **Not tested.** Women's rising participation (LR-W1), older men's falling participation (LR-O1) and prime-age
  men's mild decline (LR-M1) are known to everyone involved: they are postdictions, not tests. The
  pension-indexation interaction (LR-O2) needs indexation dates coded by hand from legal histories; this protocol
  admits no home-made coding, so it is dropped (as P7 was in Europe).
- **An assumption this design cannot check.** The critic's refutation of the floor mechanism requires that the
  parents' generation owns outright, so that the host's room does not inherit the host's rent bill. Tenure is
  deliberately absent from the floor extract (section 3, L9). The condition is assumed, not measured.

## 3. Sample and measures (common rules L1-L14)

- **L1. Unseen cells.**
  - The 31 countries of the European protocol (its rule C1): observation years 1950-1996 only, so the lagged q year
    is at most 1995 and no seen 1997-2025 cell enters.
  - OECD members outside those 31 (US, CA, AU, NZ, JP, KR, IL, MX, CL, CO, CR, TR): observation years 1950-2025,
    with 2020 and 2021 dropped as in C2.
  - Only OECD members enter: BG, HR, CY, MT and RO are not members and do not enter, even where an OECD flow
    publishes them.
- **L2. Excluded country-years:** the state-socialist administered-rent years: CZ, SK, HU, PL, EE, LV, LT, SI and
  East Germany, observation years up to 1990. This is a membership rule, applied before any value is seen.
- **L3. Only measured observations.** A value flagged estimated, forecast, interpolated, projected or modelled
  (OECD OBS_STATUS E, F or M; ILOSTAT source EA; JST `rent_ipolated`) is missing. No series is interpolated,
  backcast or ratio-linked in a primary run. Model-based sources (ILO EAPEP, ILOSTAT modelled estimates, UN modelled
  series) are excluded.
- **L4. The outcome, participation, from one source.** The activity rate by sex and five-year age from
  `OECD.ELS.SAE,DSD_LFS@DF_LFS_INDIC,1.1`, key `{REF_AREA}.LF_RATE.PT_POP_SUB.{F|M}.{AGE}.LF`.
  - **A2534** = the equal-weight mean of the sexes and of `Y25T29` and `Y30T34` (C5's rule). It is missing if
    any of the four cells is missing. There is no fallback to the `Y25T34` band or to both-sexes totals.
  - **A5564** = the same from `Y55T59` and `Y60T64`. **A_W(25-54)** and **A_M(25-54)** = the mean of the six
    five-year bands 25-29 … 50-54 for each sex.
  - The panel's participation series uses this flow only. The lower rungs of the design review's ladder (national
    LFS, ILOSTAT survey and census points) would add only a few country-years with five-year bands, few of them in
    countries with a floor measure, and none with this flow's cycle measure. They are not used in any test.
- **L5. The cycle, from the same source:** U_ct = the unemployment rate at 25-54, both sexes, from the same flow,
  key `{REF_AREA}.UNE_RATE.PT_LF_SUB._T.Y25T54.UNE`, at the observation year. One source per country, never
  spliced. An observation without U_ct leaves every test that controls for it.
- **L6. q, rents relative to prices, by a source ladder:** `x_ct = log q_{c,t-1}`, lagged one year.
  - **Rung 1, the Jorda-Schularick-Taylor Macrohistory Database, Release 6** (`JSTdatasetR6`, macrohistory.net).
    The rent index is `housing_rent_yd × hpnom`, or `housing_rent_yd ×` the cumulated `housing_capgain` for ESP,
    ITA and PRT, where `hpnom` starts late. q = rent index / `cpi`. Countries: AUS, BEL, CHE, DEU (from 1962), DNK,
    ESP, FIN, FRA, GBR, ITA, JPN (from 1960), NLD, NOR, PRT, SWE, USA, to 2020. BEL 1965-1975 is missing and stays
    missing.
  - **Rung 2, the OECD analytical house-price rent index over the all-items CPI.** RPI from
    `OECD.ECO.MPD,DSD_AN_HOUSE_PRICES@DF_HOUSE_PRICES,1.0`, key `{REF_AREA}.A.RPI.IX`; CPI from
    `OECD.SDD.TPS,DSD_PRICES@DF_PRICES_ALL,1.0`, key `{REF_AREA}.A.N.CPI.IX._T.N._Z`. For a year that flow lacks
    (JPN after 2020), the CPI comes from `DSD_PRICES_COICOP2018@DF_PRICES_C2018_ALL,1.0`, same key; that switch is
    a segment.
  - **Extend, don't fill.** A country takes rung 1 over its longest contiguous run. Rung 2 may only extend that run
    backwards or forwards (for JST countries: from q year 2021). It never fills a gap inside a rung-1 run. Inside a
    run, a gap stays missing. Overlap years are never used to choose a source and never to link levels.
  - **Known weaknesses, disclosed.** The denominator is all items (which contains rent), not goods: a long goods CPI
    exists for almost no country before 1985. The CPI rent component prices sitting tenants, is regulated in many
    countries and years, and under rationing is not the price young outsiders face (LR-RC). The JST rent index is
    a constructed series: a rent-price ratio anchored to 2012-2014 and extended backwards from national rent
    components, in places rescaled (RORE documentation, section 2.4). That OECD's RPI is the CPI actual-rentals
    component is assumed, not confirmed.
- **L7. Segments: a splice is a fixed effect.** A new segment starts, for a country and a series, at:
  - every source switch (including the L6 rung switch);
  - every break flag in the source (OECD OBS_STATUS B);
  - every redesign or definitional change named in the source documentation: the OECD's `LFSNOTES_SOURCES.pdf`
    Table 6, the BLS and Census notes for the US, the JST and RORE documentation (including R6's 2016-2020
    extension method);
  - every change in the lower age limit (14, 15, 16) and in the treatment of the armed forces or of unpaid family
    workers;
  - every territorial change (DEU 1991: the West German series is an earlier segment of the same DE cluster).

  The table `longrun/data/segments.csv` (geo, series, tau, reason, citation) is compiled from documentation alone
  by an agent given no values, and frozen at the L-freeze. Each segment start τ of any series in a regression
  (outcome, tested regressor, controls) adds `1[geo = c, year ≥ τ]`, through the frozen `specs.break_dummies`;
  for lagged q, a segment starting in year τ acts from τ + 1 (C3). With a country-level moderator this is
  equivalent to country × segment fixed effects for outcome and q. A break found after the freeze counts as
  plumbing only if its documentation predates the look and a citation is given; otherwise it is a deviation.
- **L8. Units and missing cells.** Rates in percentage points. A missing sub-cell makes the band missing. No
  outlier rule of any kind.
- **L9. The floor measure F_L, from IPUMS-International census microdata (Extract A).**
  - **Definition.** The share of persons aged 25-34 living with a parent, in the **earliest** census sample with
    1955 ≤ year ≤ 1975. "Living with a parent" is RELATE general code 3 (child of the household head, all detailed
    codes under it); persons in group quarters are excluded (GQ household codes only); RELATE unknown is excluded
    from numerator and denominator. The share is weighted by PERWT, computed for men and women separately, and
    F_L is their equal-weight mean.
  - **Territory.** The sample must cover the panel's territory: DE uses the 1970 (West German) sample; the 1971
    East German sample is excluded by L2.
  - **No proxy.** A country without such a sample with RELATE drops out of every test that uses F_L. No proxy
    substitutes in a primary run. The Giuliano-Nunn family-organisation measure is a no-verdict robustness run
    (section 5).
  - **Standardised and split.** For D1-L, F_L is standardised over the test's countries (mean 0, sd 1). For
    LR-K2, `H_c = 1` (high floor) for the countries in the top half of F_L among the test's countries; with an odd
    count, the middle country is low floor; ties are broken by country code.
  - **The extract, exactly.** She registers with IPUMS-International and makes it herself:
    - **Samples:** every IPUMS-I census sample for an OECD member (the 38 of 2026) with census year 1955-1975,
      as listed on the IPUMS-I sample page on the day of the extract. From the public lists of 2026-10-08 this is
      expected to be: AT 1971; CA 1971; CH 1970; CL 1960, 1970; CO 1964, 1973; CR 1963, 1973; DE 1970 (West),
      1971 (East); FR 1962, 1968, 1975; GB 1961, 1971 (no RELATE); GR 1971; HU 1970; IE 1971; IL 1972; MX 1960,
      1970; NL 1960, 1971; US 1960, 1970. Survey samples are not included.
    - **Variables:** COUNTRY, YEAR, SAMPLE, SERIAL, PERNUM, HHWT, PERWT, AGE, SEX, RELATE, MOMLOC, POPLOC, GQ.
      Nothing else: **no labour, education, income, marital-status or tenure variable.** Labour, education and
      tenure would be outcome values of this holdout.
    - **Case selection:** persons aged 20-34 only (household members of selected persons not included).
    - **Format:** CSV, rectangular (person records), compressed, plus the DDI codebook (XML).
    - **Where:** `participation/longrun/data/ipums/`, which must be gitignored before any file is placed there
      (it is not yet; IPUMS terms forbid redistributing microdata). Only the extract request (samples, variables,
      case selection, extract number) and, after the look, the aggregate F_L values with the IPUMS citation are
      committed.
    - **When:** after the `participation-L-freeze` tag. The extract holds regressor values.
    - **The guarded loader** (`longrun/code/ipums.py`) is the only reader. It refuses the file if it holds any
      column other than those listed, their IPUMS detailed versions (RELATED), their data-quality flags (QAGE,
      QSEX, QRELATE), the parent-link rule flags (MOMRULE, POPRULE) and sampling-design variables that the DDI
      marks as such. It reads a country's earliest sample (for F_L) only when that country's half is open. A
      country's later samples in the window are LR-C1 outcome values: read only when that half is open.
- **L10. Coresidence as an outcome (LR-C1), from Extract B.** The same variables, case selection and format as
  Extract A, for every IPUMS-I census sample of an OECD member in the unseen cells after 1975 (the 31 European
  countries: 1976-1996; the others: 1976-2025 except 2020-2021). It is made after the L-freeze. The outcome R_cy is
  F_L's construction applied to each census: the share of 25-34 living with a parent, sexes equal-weighted. Whether
  she makes Extract B is her call, recorded in the freeze commit; without it LR-C1 leaves its family before the tag.
- **L11. School attendance (C-6L):** the share of 20-24-year-olds attending school, both sexes, from ILOSTAT
  `POP_3WAP_SEX_AGE_STU_NB_A` (YOUTHSTATS, annual): attending / (attending + not attending); "not stated" is left
  out of the denominator. One source; each change of underlying survey named in the ILO notes is a segment.
- **L12. Design covariates and controls:**
  - population on 1 July 1960 (UN WPP2024, total; a design covariate for the split, fetched before the freeze);
  - relative cohort size = population 25-34 / population 35-64 (UN WPP2024, five-year groups; a control used
    only by LR-K2's cohort-size qualifier, fetched after the freeze);
  - rent regulation from Kholodilin's published rental-regulation dataset (Housing Policy Debate 2020 and its
    data release), used only to drop strict-control country-years in a robustness run. "Strict" means a year coded
    as having first-generation rent control (a rent freeze or nominal ceiling). This source was not scouted: its
    availability and variable names are checked from documentation at L2; if it is not available as data, the run
    is dropped before the freeze and replaced by nothing.
- **L13. Weighting and clusters:** countries weighted equally within each observation; the cluster is the country
  (C8). DE before and after 1991 is one cluster.
- **L14. Fetch discipline:** one door, `longrun/code/fetch.py`, logs every download in `longrun/data/fetch_log.jsonl`
  (URL, UTC time, half, SHA-256). Raw files are not committed. ILOSTAT and JST files are hashed at fetch, since both
  update. The confirm run downloads all countries in one vintage and reports any difference against the logged
  explore-half hashes. **Order at each opening:** q is fetched first, the terciles of section 5 are computed and
  written with their hash to the log, and only then are outcomes fetched. Terciles are never recomputed after
  outcomes are seen.

**Testability, from coverage alone.** A test runs only if enough countries can enter it. The counts come from
availability metadata (years and flags, no values) and the public IPUMS sample lists, by code, at L2:

- LR-K2: at least 8 countries with F_L and at least 9 eligible observation years each (an eligible year has
  A2534, U_ct and x_ct available), with at least 3 countries in each floor group.
- LR-Y0: at least 8 countries with at least 9 eligible years.
- C-6L: at least 8 countries with at least 2 observations inside one segment of outcome and regressor.
- LR-C1: at least 8 countries with at least 2 censuses with x.

A test that fails leaves its family before the L-freeze, and the family sizes are frozen with the tag. If LR-K2
fails, the long-run model-level verdict is "not testable" and only no-verdict results are reported.

**What coverage suggests now** (the scouts' years-only files and public sample lists; L2 decides by code):
- LR-K2: about 10 countries: CA, CL, CO, CR, DE, FR, IL, MX, NL, US. ES, IT and PT, and JP and KR, have no
  IPUMS-I census by 1975 and drop out. IE, CH, GR and AT have too few eligible years.
- LR-Y0: about 24 countries.
- C-6L: about 19 countries.
- LR-C1, with Extract B: about 13 countries.

So the primary floor test will in practice compare the long histories of North America and the Continent with
the shorter, later histories of Latin America and Israel. The Giuliano-Nunn run is the only one that brings in the
South of Europe and East Asia.

## 4. The split

`longrun/code/split.py`, committed with this protocol (`longrun/data/split.json` is its output). Only countries
that enter at least one verdict test (by the testability rules) are split.

- **Strata:**
  - Nordic: DK, FI, NO, SE, IS
  - Continental: AT, BE, CH, DE, FR, LU, NL
  - Anglo: IE, UK, US, CA, AU, NZ
  - South: ES, IT, PT, EL
  - Asia: JP, KR
  - Latin America: MX, CL, CO, CR
  - Other: IL, TR and any other member that enters
- **Pairing:** within each stratum, countries are ranked by 1960 population (UN WPP2024) and adjacent countries are
  paired. One member of each pair goes to each half at random. The leftover country of an odd stratum is assigned
  at random, subject to the halves differing in size by at most one.
- **Forced placement:** the US goes to EXPLORE by rule, its pair partner to CONFIRM. The US's long q and its
  aggregate participation are partly seen (section 7), so the confirm half then holds no country whose long-run q
  path anyone involved has studied.
- **Seed:** `int(sha256(b'participation-longrun-split-v1|' + ','.join(sorted(codes)).encode()).hexdigest()[:16], 16)`,
  passed to `numpy.random.default_rng`.

**What each half may be used for:**
- **Before the L-freeze:** nothing but metadata (codelists, availability, documentation, sample lists) and the 1960
  population.
- **From the L-freeze:** the explore half freely. The US deep study runs first (section 6).
- **Before the LE-freeze:** the loader refuses confirm countries (the European `eurostat.guard` pattern).
- **At the look:** one run of `confirm.py`.
- **After the look:** free use, all labelled exploratory. New long-run hypotheses go only to the 2026-2028 time
  holdout or to OECD members never fetched.

## 5. The tests

Every panel regression has country and year fixed effects, the segment dummies of L7 and the cycle control U_ct,
unless stated. Inference is the restricted wild cluster bootstrap-t (Webb weights, B = 9999, clustered by country,
CR1), one-sided in the predicted direction, with confidence intervals by test inversion. It uses the frozen
`participation/code/inference.py` (`wcr`, `ci`, `ri`, `g_star`, `mde`) and the verdict helpers of
`participation/code/specs.py` (`break_dummies`, `holm`, `holm_reject`, `qualify`), by import, unedited.

**The piecewise basis.** Several tests share it. For country c, its eligible observation years are ranked by
`x_ct = log q_{c,t-1}` (ties by the earlier year); with n years, rank r falls in tercile `ceil(3r/n)`. The knot
k1_c is the midpoint between the largest x in tercile 1 and the smallest in tercile 2; k2_c likewise between
terciles 2 and 3. The basis is

```
P1 = min(x, k1)            P2 = min(max(x − k1, 0), k2 − k1)            P3 = max(x − k2, 0)
```

so that A = γ1·P1 + γ2·P2 + γ3·P3 is a continuous broken line whose slopes are γ1 (bottom tercile), γ2 (middle) and
γ3 (top). The terciles use only q and the availability metadata, and are fixed at each opening before outcomes
are fetched (L14).

### K: the distinctive test (the model against the no-coresidence account)

- **LR-K2. The regime-aware floor kink.**
  - **Equation:**
    `A2534_ct = a_c + d_t + Σ_j [ γj·(1 − H_c)·Pj_ct + γj^H·H_c·Pj_ct ] + g·U_ct + segments + e_ct`, j = 1, 2, 3.
  - **Tested quantity:** the difference in differences `DiD = (γ3^H − γ1^H) − (γ3 − γ1)`: how much more the
    slope falls from the bottom to the top tercile in high-floor countries than in low-floor ones. It is estimated
    as one coefficient of the same regression written in the equivalent ramp basis, so that the frozen `wcr` can
    test it.
  - **H1:** DiD < 0.
  - **No-coresidence account:** DiD ≥ 0 (a convex, rising response everywhere).
  - **Reported with no verdict:** `slope_top(high F) = γ3^H`, the young's slope in the high-q tercile of
    high-floor countries, with its one-sided p for γ3^H > 0. The model says ≤ 0. A significantly positive value,
    no smaller than at low F, alongside a contradicted DiD, is the critic's full refutation condition (given the
    unmeasured outright-ownership assumption). Also reported: γ1, γ2, γ3 for each floor group, and each country's
    own top-minus-bottom change from a country-by-country fit (a table, no inference).
  - **Inference:** the tested variation is country-level (H_c), so **randomisation inference is co-primary**.
    H is permuted across all the test's countries (not within strata, since floor and stratum are likely
    aligned), every H-interaction is rebuilt for each assignment, and the CR1-studentised t is recomputed. With
    about 10 countries, enumeration is exact. The frozen `inference.ri` permutes only the tested regressor, so this
    RI is written in `longrun/code/inference_l.py` and checked against `inference.ri` on a design with one
    interaction. **The verdict p is max(p_WCR, p_RI)**; p_opposite is the larger of the two opposite p's.
  - **Mechanical qualifiers**, besides the frozen "rests on one country (XX)":
    - "rests on floor-group trends", if adding H × decade fixed effects flips the sign of DiD or pushes its
      own-direction p above 0.10;
    - "rests on cohort size", if adding relative cohort size (L12) does the same.

### C: consistency checks (shared with standard models)

- **LR-Y0. The young respond positively before enclosure.**
  - **Equation:** `A2534_ct = a_c + d_t + γ1·P1 + γ2·P2 + γ3·P3 + g·U_ct + segments + e_ct`, all countries with q
    (no floor measure needed).
  - **H1:** γ1 > 0, the slope in each country's bottom tercile of q.
  - **Reading:** under binding rent control the model predicts about 0 (LR-RC), so a null is not a contradiction of
    the floor; a negative γ1 counts against enclosure for the young (the paper's exit proposition (iii)) or the
    auxiliary s0 < w.
- **C-6L. School as a paid exit** (the European C-6, backwards).
  - **Equation:** the share of 20-24 attending school (L11) on U_ct (L5, the same year).
  - **Controls:** none beyond fixed effects and segments; the regressor is the cycle, so U_ct is not added again.
  - **H1:** b > 0.
  - **Reported with no verdict:** E-SCH1-L, the same on U_{c,t-1}, the form of the surviving European E.
- **LR-C1. Coresidence absorbs rents** (only if Extract B is made; L10).
  - **Equation:** `R_cy = a_c + r_round + b·x_cy + e_cy`, at census years. Round fixed effects by census decade
    (1955-64, 1965-74, … , 2015-24) replace year effects. No cycle control (U_ct is missing at many census years).
  - **H1:** b > 0.
  - **Reading:** a null or negative slope with clean q refutes the paper's mapping of the modern dependency floor to
    the parental home. That is an auxiliary, but the floor mechanism has no empirical carrier without it.

### No verdict (reported, never counted)

- **D1-L:** `A2534_ct = a_c + d_t + b1·x_ct + b2·(x_ct × F_c) + g·U_ct + segments`, F_c = standardised F_L.
  Reported: b2, its p in both directions by WCR and by `inference.ri` (x_unit = F_c, x_mult = x_ct, within the split
  strata, x_ct kept in Z), and the slope at the 75th percentile of F.
- **D2-L:** A2534 on x_ct and `(x_ct − m_cs)²`, where m_cs is the mean of x within country × q-segment (a level
  shift in a spliced q is not absorbed by a square otherwise). Reported with the series-permutation placebo of the
  design review: each country's q path replaced by another country's with matching coverage.
- **C-2L:** `A2534 − A5564` on x_ct. **C-3L:** `A_W(25-54) − A_M(25-54)` and `A_W(25-54)` on x_ct.
- **E-SCH1-L** (above) and the US deep study (section 6).

### Verdicts

- **Per test**, as frozen: *supported* when the one-sided p survives Holm within its family at familywise 0.05;
  *contradicted* when the opposite-direction p does; *inconclusive* otherwise.
- **Families:** K = {LR-K2}; C-L = {LR-Y0, C-6L, LR-C1} (LR-C1 only with Extract B); E-L = up to three, confirm half
  only. The sizes are frozen at the L-freeze from coverage.
- **Size correction.** Before the freeze, every verdict test is simulated on its real coverage skeleton (countries,
  years, segments; synthetic q paths for the terciles) with synthetic outcomes: AR(1) errors with ρ = 0.5 and
  ρ = 0.9, country trends, and trends by floor group, with variances from the European look. If a test's simulated
  size at nominal 0.05 exceeds 0.075, its threshold becomes the simulated 5% quantile of null p. The rule and its
  outputs are frozen with the tag.
- **Rests on one country:** the frozen leave-one-country-out qualifier (LOO_P = 0.10). Leave-one-stratum-out and
  G* are reported, not acted on.
- **The long-run model-level verdict rests on LR-K2 alone:**
  - *favours the floor mechanism against the no-coresidence account*: LR-K2 supported;
  - *against the floor mechanism*: LR-K2 contradicted;
  - *inconclusive* otherwise.

  It carries LR-K2's qualifiers. A supported LR-K2 is never reported without the sentence that it does not
  discriminate against life-cycle models with a below-market parental room (section 2).
- **What C-L does and does not settle:** C-L verdicts speak to the model's mapping onto groups and to the
  measurement. They do not settle the model against any standard account.

**The reading table, written now.** The stated prior is that the model should work back to 1950, so an imperfect
data set invites a motivated reading of a null. Each verdict test's MDE is computed before the look from the
skeleton simulation (the larger of the ρ = 0.5 and ρ = 0.9 values) and published with the freeze.

| Verdict | Reading |
|---|---|
| contradicted | stands, whatever the data quality |
| supported | stands, with its qualifiers |
| inconclusive, MDE at or below the European benchmark | "no support" |
| inconclusive, MDE above the European benchmark | "uninformative" |

The European benchmarks:
- C-6L: the European full-sample C-6 MDE, 0.280.
- LR-C1: the European full-sample C-1 MDE, 11.20.
- LR-K2 and LR-Y0 have no European test. Their benchmark is the MDE of the same specification run, before the
  freeze, on the frozen European panel (31 countries, about 2009-2025, European q per C6, F from C9 split at the
  median). That run uses data already seen. Its point estimates are committed with the freeze, labelled exploratory
  and no-verdict, and both forecasters see them.

**Two studies, two verdicts.** The European look and the long run each keep their own verdict. There is no
Fisher or Stouffer combination; an inverse-variance pooled number is reported with no verdict.

| European D1/D2 | Long-run LR-K2 | Joint reading |
|---|---|---|
| either contradicted | any | against the floor mechanism |
| any | contradicted | against the floor mechanism |
| not contradicted | supported | supported in the long run (against the no-coresidence account only), not in 2009-2025 Europe |
| otherwise | | inconclusive |

The European look found D1 and D2 inconclusive, so in practice LR-K2 decides the joint reading.

**Forecasts.** Before the freeze, she and Claude each fill `longrun/FORECASTS.md`: for each verdict test, the
expected sign of the estimate and the probabilities of each verdict. The sheets are committed with the tag and
reported beside the results. A verdict to which every forecaster gave at least 0.5 is marked "as forecast".

**Robustness, with no verdicts** (eight runs, no more):

| Run | Applies to |
|---|---|
| F from Giuliano-Nunn (Ancestral Characteristics Database v1.1, baseline: the ancestral share in extended-family domestic organisation, v8; codes confirmed from its codebook at L2), all countries with q | LR-K2, D1-L |
| F_L at ages 20-29 | LR-K2 |
| F_L as any coresident parent (MOMLOC or POPLOC > 0), where the sample has the pointers | LR-K2 |
| standardised F_L in place of the high/low split | LR-K2 |
| men only; women only | LR-K2, LR-Y0 |
| strict rent control dropped (L12) | LR-K2, LR-Y0, LR-C1 |
| q_hpi = log(house prices / CPI): JST `hpnom / cpi`, else OECD `{REF_AREA}.A.HPI.IX` over the CPI of L6 | LR-K2, LR-Y0, LR-C1 |
| without the US (the partly seen country) | LR-K2, LR-Y0, C-6L, LR-C1 |

The men-only run is the critic's (LR-F1): before about 1975, young women's floor was the marital household, so the
parental floor applies to young men throughout and to young women only later.

## 6. The US deep study (no verdict)

One country, 1948-2025, specified now and run once, first, after the L-freeze; its output is committed as it comes
out, before any free exploration of US data. The US is in the explore half.

- **Participation:** CPS civilian participation rates, not seasonally adjusted, annual means of monthly values:
  25-34 men `LNU01300164` and women `LNU01300327`; 20-24 `LNU01300037` and `LNU01300038`; 55-64 `LNU01300190` and
  `LNU01300347`. 2025 averages the eleven months published. From the BLS API v1 (25 calls a day) or its DBnomics
  mirror `BLS/ln`; the values are BLS's either way and the log records the door.
- **q_US:** `log(DTENRG / DGDSRG)_{t-1}`, the BEA PCE price indexes for tenant rent and for goods (NIPA Table 2.4.4,
  annual, 1929-2025), via DBnomics `BEA/NIPA-T20404`. Rent over goods, as in the paper.
- **Coresidence:** Census AD-3, 25-34 living as child of the householder, men and women equal-weighted, 1967-2023
  (CPS ASEC). AD-1 extends it forward (2024-2025) as a new segment. AD-1's census points (1960, 1970, 1980) are a
  separate segment.
- **Enrolment:** Census CPS October Table A-2 (`hst_enroll02.xlsx`), both sexes; 20-24 = (2 × the 20-21 rate +
  3 × the 22-24 rate) / 5, 1959-2024.
- **Cycle:** the CPS unemployment rate at 25-54 (`LNS14000060`, annual mean).
- **Segments:** from BLS and Census documentation, by the L7 rules: the CPS population-control introductions, the
  1967 definitions, the 1994 redesign, the 2014 ASEC redesign and others the documentation names.
- **Analyses, all no verdict:**
  - U-K2: the piecewise basis on the US's own q terciles (1948-2025); γ3 − γ1 and γ3;
  - U-Y0: γ1;
  - U-C1: coresidence on q_US;
  - U-S: enrolment on the cycle;
  - each by sex where the series allow.

  Each is reported in levels with the cycle and segment dummies, and in five-year differences within segments.
  Standard errors are Newey-West (Bartlett, 4 lags), written in `longrun/code`.
- **Why no verdict:** a single country's time series cannot separate q from any smooth trend (women's entry, the
  baby boom, schooling), and the US long q is the paper's own fork.

## 7. Disclosed prior knowledge

Everyone involved, the AI agents included, knows broad postwar facts:
- women's entry into paid work; early retirement in the 1970s-80s; the US prime-age male decline;
- late home-leaving in Southern Europe from the 1980s; Japan's coresiding singles of the 1990s; high young-adult
  coresidence in Latin America;
- the oil shocks; the baby-boom cohorts (Easterlin);
- rent-control histories (US federal controls ending in the early 1950s, German decontrol 1960-71, Spain 1985,
  UK 1988);
- the published literature on young adults' coresidence and labour markets (Kaplan; Ermisch; and others).

**Seen in this repository or this study:**
- The European 1997-2025 data, through the look (`results/confirm_8623706.json`). All eight European primaries were
  inconclusive. D2 leaned the other way (p_opposite 0.064). The confirm half's rent × F was +9.1 (two-sided p 0.033).
  C-6 and E-SCH1 were supported.
- US long series: the paper's shelter-versus-goods fork for 1950-2025 is effectively US q. Cached in `paths/cache`
  and `pinning/cache`: CIVPART, LNS11300060, LNS12300060, LNS14000060, UNRATE, EMRATIO, CLF16OV, CE16OV, UNEMPLOY,
  CPIAUCNS, CPIAUCSL, PCEPI, PCEPILFE, DGDSRG3Q086SBEA, DHLCRG3Q086SBEA, DHLCRC1Q027SBEA, DHSGRC1A027NBEA, PCECA,
  AHETPI, AWHMAN, PAYEMS, HOANBS, PRS85006092, the BIS and Case-Shiller house prices and others listed in the
  inventory. The US findings on prime-age participation since 2023 are in `paths/`. US participation by sex and
  age, CPI rent, BEA tenant rent and the Census coresidence and enrolment tables are cached nowhere.
- ILO temporary-employment series for DE, ES, IT, NL and SE (`paths/cache/ilo`; not participation).
- Before the freeze, `longrun/code/coverage.py` greps every cache and fetch log in the repository and writes the
  full list of country × series on disk to `longrun/data/seen.json`, committed with the tag.

**The scouts' incidents** (2026-10-08; values not recorded, not reported, and not seen by the orchestrating
analyst):
- web-search summaries showed one scout a few US participation rates for 15-64 and 25-54 in 1959-1970, one 1959 US
  16-24 rate by sex, and a few Austrian RPI index levels;
- a structure dump showed another scout four AD-1 cells (counts in thousands);
- web-search summaries volunteered headline coresidence and ownership figures for CA, JP and AU;
- one non-OECD row of the UN household file was printed.

**Files with values outside the repository.** The scouts' working folders in the session scratchpad hold
downloaded files with values (ILOSTAT world files, BLS API extracts for 1948-57 and 2017-26, Census tables, JST R6,
the Bank of England workbook, and others). No one opens them, and the pipeline never reads them: it fetches anew
through its own logged door.

**The forecast sheets** record what each participant expects before the look. Country-level prior knowledge cannot
be removed, so the time holdout remains the only clean test.

## 8. Bug policy

- **Between the L-freeze and the LE-freeze:** plumbing (fetching, parsing, variable construction) may be fixed where
  the code departs from text frozen here. Each fix gets its own commit with the reason.
- **A change to a rule is a deviation:** outcome, regressor, sample, controls, sign, a segment without a
  documentation citation, a tercile or threshold. It is recorded in `STATE.md`, and that P-L test's primary falls
  back to the confirm half.
- **Frozen code:**
  - a check asserts that the files of `participation/code` have the SHA-256 they had at `participation-E-freeze`;
  - `confirm.py` refuses to run unless `participation/longrun/code` is unchanged since the LE-freeze.
- **After the look:** a bug is fixed in a new commit, and the original and fixed results are reported together with
  the diff. No refetch after the look, except under this policy.
- **Debugging** before the look runs on a blinded panel, with q paths permuted across countries by a hidden seed.

## 9. Timeline and tags (local, like the existing ones; pushing is her call)

- **L0.** This protocol.
- **L1.** Blind coverage scouting: `longrun/docs/data_inventory.md`, done.
- **L2.** Coverage decisions, by code, from metadata only:
  - which countries enter each test (testability), the family sizes, the F_L sample per country;
  - `segments.csv`, from documentation;
  - `split.json`, from the 1960 population;
  - `seen.json`;
  - the gitignore entries for `longrun/data/ipums/` and `longrun/data/raw/`.
- **L3.** Before the tag:
  - `longrun/code` built and checked on synthetic data;
  - the skeleton simulation (size, size correction, MDEs);
  - the European benchmark runs;
  - the forecast sheets filled;
  - her Extract B decision recorded.

  **Tag `participation-L-freeze`.**
- **L4.** After the tag:
  - the US deep study, run once and committed;
  - she makes the IPUMS extract(s);
  - the explore half is free;
  - at most three E-L, with their forecast rows added to `FORECASTS.md`.

  **Tag `participation-LE-freeze`.**
- **L5.** `longrun/code/confirm.py`, once, on one vintage (q first, terciles hashed, then outcomes). The result is
  committed immediately.
- **L6.** Free exploratory use. New hypotheses go only to the 2026-2028 time holdout, or to OECD members never
  fetched.

## 10. What this protocol takes from the reviews, and where it departs

**Adopted:**
- unseen cells only;
- the matched-pair country split, with the US forced into the explore half and at most three E-L;
- P-L primary on all unseen country-years;
- "a splice is a fixed effect", "extend, don't fill" and only measured observations;
- the cycle from one source per country;
- rent-control robustness from a published coding only;
- the frozen leave-one-out qualifier;
- co-primary randomisation inference where the tested variation is country-level;
- skeleton MDEs and size correction before the look, with the reading table;
- the forecast sheets;
- the floor-group-trend and cohort-size qualifiers;
- the series-permutation placebo, kept for D2-L, which now carries no verdict.

**Departures, each for a stated reason:**
1. **Annual panel, not a five-year grid, as the primary.** LR-K2's tercile slopes are identified from
   within-segment annual variation in q. A grid would leave about four points per tercile per country. With
   participation from one OECD flow, there are no census-year points to align. Serial correlation is handled by
   clustering by country, and its effect on size by the skeleton simulation.
2. **Participation from `DF_LFS_INDIC` only, with its own unemployment rate as the cycle, not a GDP gap.** The flow
   publishes both with the same start years, so the cycle never needs a second source. GDP per head from Maddison
   was not scouted and ends before 2025.
3. **D1-L and D2-L carry no verdict** (her decision; LR-K1). **C-2L and C-3L carry no verdict** (LR-K1, LR-F1:
   unsigned without tenure). The design review had carried all four.
4. **LR-Y0 is added** as a consistency check. It is the one sign the model fixes for the early decades.
5. **LR-K2's randomisation is unstratified**, because high and low floor are likely to coincide with strata, which
   would leave a within-strata permutation nothing to permute.
6. **Extract B is proposed** so that LR-C1 can be tested across countries. It is her call.
7. **LR-O2 is dropped:** pension-indexation dates would have to be hand-coded.
