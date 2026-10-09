# Participation — the long-run protocol (an addendum to PROTOCOL.md)

Written 2026-10-08 and revised 2026-10-09 on three reviewers' findings (section 11), after the European look and
before any long-run outcome or regressor value was downloaded or read into this thread (the scouts' incidents are
listed in section 7). Settled on 2026-10-09 where the code review of the pipeline needed a reading (section 11, "Code
review of 2026-10-09"). The tag `participation-L-freeze` marks the commit that freezes it, together with the code that
runs it, the coverage decisions, the segment table, the frozen IPUMS sample list, the split, the pre-look MDEs and
the filled forecast sheets (`FORECASTS.md`). After that tag nothing below changes; any later departure is written in
`STATE.md` as a deviation and labelled exploratory wherever it is reported.

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
   predicted sign and the committed explore output that motivated it.
   - E-L may only use series in this protocol's manifest, and **only the unseen cells of L1-L2**: no E-L sample
     may contain a European 1997-2025 observation year or any other cell seen at the European look.
   - An E-L that varies a P-L test is labelled as such. It **never changes that test's verdict or the long-run
     model-level verdict**, and it appears only in the E-L table (the European rule, restated).
   - The tag `participation-LE-freeze` freezes them.
3. **The one look.** After the LE-freeze, `longrun/code/confirm.py` runs once. It reports P-L on all unseen
   country-years (primary), P-L on the confirm half (replication) and E-L on the confirm half (the only valid test
   of E-L). Every result is reported, nulls included.

**The US deep study (section 6) carries no verdict.** The US from 1948 (CPS by sex and age, BEA tenant rent over
goods, Census coresidence and enrolment) is studied as one country. The paper has already used US long series, so
whatever the US shows on its own settles nothing. The US also enters the panel as one country among the others.

**The time holdout** stays the only clean test: the frozen long-run code is rerun on the non-European countries
when the 2026-2028 data are published. The terciles and knots of section 5 are frozen at the look; new years take
the frozen basis and never move a knot.

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
  participation slope on q should **fall**, from the low-q part of each country's own history to the high-q part
  (γ3^H < γ1^H), and the high-q slope should lie **below the low-floor countries' high-q slope** (γ3^H < γ3). In
  low-floor countries it should stay positive and rising. Section 5's distinctive test is built on the difference
  in differences, with terciles of q fixed by a rule on q alone.
  - **The high-floor top slope is not predicted to be ≤ 0 in general.** A high-floor country mixes floor-types
    (share φ) with no-floor types. In regime (iii) its slope is φ·0 + (1 − φ)·slope_N, which is positive where work
    can be done from the parental home (the critic's `floor_regimes_v2.py`: slope 0 for floor-types and +2.5 for
    no-floor types at q 0.44-0.47). γ3^H is ≤ 0 only if floor-types dominate the high-floor countries' young, or if
    jobs require one's own dwelling (the paper's linear reduced form, slope −h_w). A smaller but positive γ3^H is
    the model's prediction for a top-half country with, say, 30-60% of its 25-34s at home. γ3^H is reported, not
    tested.
  - **The critic's refutation is a conjunction**, quoted as such: at high F, the top-tercile slope is
    significantly positive, **and** no smaller than at low F, **and** shows no drop from the low-q to the high-q
    tercile, with market-measured q, predetermined F and outright-owning parents. A positive γ3^H on its own
    refutes nothing.
- **What the distinctive test is distinctive against, and what it is not.**
  - **The no-coresidence income-effect account** predicts a convex, rising response in *each* group: top-minus-bottom
    > 0 within the low-floor and within the high-floor countries. It does **not** sign the difference between
    groups whose q-to-income positions differ (Latin America against North America and the Continent). Under equal
    scaling of the two groups its DiD is about 0. The within-high-floor change γ3^H − γ1^H > 0 is the quantity it
    signs unambiguously.
  - **An attenuation or family-insurance account.** Any account in which the high-floor young's response is a
    proportional attenuation λ < 1 of the same convex response (the symmetric family-insurance model the critic
    names in derivations headline (3), or a lower participation density at the margin where the high-floor 25-34
    rate sits) gives DiD = (λ − 1)(γ3 − γ1) < 0 too, with γ3^H − γ1^H > 0 and γ3^H > 0. **So DiD < 0 alone does
    not separate the floor from attenuation.** What separates them is a fall within the high-floor group
    (γ3^H − γ1^H < 0) with γ3^H not significantly positive. Section 5's model-level reading is conditional on
    exactly that (the drop condition), and a scale-free companion of DiD is reported with no verdict.
  - **Life-cycle models with a below-market parental room** (Kaplan 2012, "Moving back home"; Ermisch's
    household-formation models). Against them **the kink is not distinctive**. They produce the same DiD sign (a
    fall in the high-floor slope as q rises), with the turning point at a different q. Their floor-type slope is
    not the paper's (in the critic's `floor_regimes_v2.py` the coresidence model has no regime (ii) with b2 > 0, and
    its floor-type slope is negative where the paper's is positive), but the tested sign coincides. LR-K2 is
    distinctive only against models **without a coresidence option**. Nothing in D1-L or D2-L discriminates against
    Kaplan- or Ermisch-type models either. A supported LR-K2 says the young behave as if a flat parental floor
    exists; it does not say this model's account of it beats Kaplan's or Ermisch's.
- **The regime claim, written down now, on both sides.** LR-K2's predicted sign rests on three auxiliaries, which
  are stated here and never revised after the look:
  1. each high-floor country's top q tercile lies past the floor-types' enclosure point q_enc^F (regime (iii)),
     and not in regime (ii), where the floor-types' slope h/(s0 − qh) is steeper and rising;
  2. in each low-floor country, the no-floor young are not at a floor (state or tolerated use) in any tercile, so
     regime (iv) does not apply, and no rent-indexed out-of-work housing allowance applies to them;
  3. the parents' generation owns outright, so the host's room does not inherit the host's rent bill (paper l.383).

  The claim covers every country in LR-K2's frozen list (section 3; at L2: CA, CL, CO, CR, DE, FR, IL, MX, US).
  Which of them is high-floor is set by F_L after the freeze. On the broad prior knowledge of section 7 the high
  group is expected to be mostly CL, CO, CR, MX and IL, and the low group US, CA, DE and FR; that expectation is not
  a measurement.

  **Disclosed now, before any value:** the critic's rationale for LR-K2 (that within a 75-year history q crosses
  q_enc) was argued for the South of Europe and Japan, which have no 1955-1975 census and drop out. It does not
  carry to the short Latin American and Israeli histories (OECD rent index from the 1990s), and nothing in the
  derivations places their top tercile past q_enc^F: auxiliary 1 is untested. Auxiliary 2 is doubtful for DE, NL
  and FR, which had housing allowances from the 1970s (derivations (4g)). Auxiliary 3 is unmeasured (tenure is
  deliberately absent from the extract). A contradicted LR-K2 is therefore read as **against the floor mechanism
  together with its stated regime placement and auxiliaries 1-3**, never as against the mechanism alone. The
  European 2009-2025 leanings against the kink (D2's p_opposite 0.064; the confirm half's rent × F of +9.1) are not
  re-read after the look as regime (ii) or (iv), and if LR-K2 is contradicted no regime reinterpretation beyond
  this paragraph is allowed.
- **The primary sign is conditional on more than the mechanism.**
  - **No floor-group-specific trends.** The primary has year effects common to both floor groups. Women's entry,
    the expansion of schooling and conscription that differ by floor group, and that run later in the Latin
    American windows, load onto the tercile slopes. The bias can run either way; in the high-floor top tercile it
    runs against the model. Section 5's "rests on floor-group trends" and "indistinguishable from time curvature"
    qualifiers report how much the verdict depends on this; the primary does not condition on it (section 10,
    departure 8).
  - **The primary pools early women for whom the parental floor is not the operative floor.** Before about 1975
    young women's floor was the marital household (LR-F1), whose response to q follows the couple's net housing
    position, not parental F. The sexes are equal-weighted by her decision; the **men-only run** (no verdict) is
    the theory-clean version and is reported beside the primary.
  - **The outcome partly measures exit in agrarian and informal settings.** Activity rates count unpaid family
    workers as active. In the paper's terms that work is the land-access exit recorded as participation, and it is
    concentrated in the high-floor Latin American group.
  - **Rent control.** Under binding control the CPI rent prices sitting tenants, so the young's response to CPI-q is
    about 0 (LR-RC). In the long-history low-floor countries the bottom terciles fall partly in control eras and the
    top terciles in market years, so the low-floor top-minus-bottom difference can be positive by measurement, and
    DiD < 0 can arise mechanically in the predicted direction. Section 5's "rests on control-era years" qualifier
    reports this.
- **The floor measure's disclosed limits.** F_L comes from the earliest 1955-1975 census (her decision). For AT, CA,
  CH, DE, IE and GR that census is 1970-71, inside the panel's observation years, so F_L is not predetermined for
  earlier years. Under LR-C1 and LR-F1, 1960s-70s coresidence is itself a response to the early q path and to
  marriage timing: the endogeneity the critic raised against 2003-08 F. Census years range from 1960 to 1972 while
  coresidence was trending, so the high/low split partly reflects census year, and it may align with history
  length (long North Atlantic histories against short Latin American ones). The "F_L nearest 1970, later years
  only" run (section 5) reports how much this matters.
- **Signed but not distinctive.** Before enclosure the young's slope on q is positive and convex (LR-Y0), the same
  as the income-effect account; under binding rent control it is about zero (LR-RC). Coresidence rises with q where
  parents own outright (LR-C1), as in Ermisch- and Kaplan-type models. School is a paid exit whose take-up rises
  with prime-age unemployment (LR-S1), as in the standard schooling literature. These are the consistency checks of
  section 5.
- **Unsigned by the model over the long run, so run with no verdict.** The young-minus-old gap (C-2) and the
  second-earner response (C-3). For young women before about 1975 the operative floor was the marital household,
  whose response to q follows the couple's net housing position (renters +, owners ≤ 0; LR-F1); the old's
  response follows their own net position (owners net long, LR-O1). Without tenure data, neither sign is fixed.
- **Not tested.** Women's rising participation (LR-W1), older men's falling participation (LR-O1) and prime-age
  men's mild decline (LR-M1) are known to everyone involved: they are postdictions, not tests. The
  pension-indexation interaction (LR-O2) needs indexation dates coded by hand from legal histories; this protocol
  admits no home-made coding, so it is dropped (as P7 was in Europe).

## 3. Sample and measures (common rules L1-L14)

- **L1. Unseen cells.**
  - The 31 countries of the European protocol (its rule C1): observation years 1950-1994 only, so the lagged q year
    is at most 1993 and no seen cell enters. The European study's 1995-1996 rows are seen: its panel grid starts in
    1995, its exploration's committed outputs hold 1995-1996 rows of activity rates for the explore countries, and
    its look built the confirm countries' 1995-1996 rows into its panel (settled 2026-10-09, section 11; the first
    draft's "1950-1996" assumed those years unseen).
  - OECD members outside those 31 (US, CA, AU, NZ, JP, KR, IL, MX, CL, CO, CR, TR): observation years 1950-2025,
    with 2020 and 2021 dropped as in C2.
  - Only OECD members enter: BG, HR, CY, MT and RO are not members and do not enter, even where an OECD flow
    publishes them.
- **L2. Excluded country-years:** the state-socialist administered-rent years: CZ, SK, HU, PL, EE, LV, LT, SI and
  East Germany, observation years up to 1990. This is a membership rule, applied before any value is seen.
- **L3. Only measured observations.**
  - A value flagged estimated, forecast, interpolated, projected or modelled is missing: OECD OBS_STATUS E, F or M;
    ILOSTAT source EA; JST `rent_ipolated`; and JST `housing_capgain_ipol` wherever `housing_capgain` enters q (ESP,
    ITA, PRT).
  - A JST rent year that the R6 documentation says was missing (the footnotes to Table 3 of the RORE R6
    documentation on the 2016-2020 update, read country by country at L2) is missing, flag or no flag; rung 2 of L6
    may then extend from the last documented year.
  - No series is interpolated, backcast or ratio-linked in a primary run. Model-based sources (ILO EAPEP, ILOSTAT
    modelled estimates, UN modelled series) are excluded.
  - **One stated exception:** UN WPP2024 population estimates are admitted for the split's design covariate and for
    the cohort-size control of LR-K2's "rests on cohort size" qualifier, and for nothing else. No measured
    population by five-year age exists for all these countries and years; both uses are a design covariate and a
    qualifier, never a tested variable, and the qualifier cannot be disowned after the look on the ground that WPP is
    modelled.
- **L4. The outcome, participation, from one source.** The activity rate by sex and five-year age from
  `OECD.ELS.SAE,DSD_LFS@DF_LFS_INDIC,1.1`, key `{REF_AREA}.LF_RATE.PT_POP_SUB.{F|M}.{AGE}.LF`.
  - **A2534** = the equal-weight mean of the sexes and of `Y25T29` and `Y30T34` (C5's rule). It is missing if
    any of the four cells is missing. There is no fallback to the `Y25T34` band or to both-sexes totals.
  - **A5564** = the same from `Y55T59` and `Y60T64`. **A_W(25-54)** and **A_M(25-54)** = the mean of the six
    five-year bands 25-29 … 50-54 for each sex.
  - **Germany:** REF_AREA `DEU_F` (the former Federal Republic, published 1970-1998) for every DE observation year,
    1970-1994, for the outcome and the cycle alike. Its territory matches the West German 1970 census that sets
    DE's F_L, and East Germany is excluded up to 1990 by L2 in any case. The choice and its documentation citation
    are recorded in `segments.csv`. (`DEU` is not used: the source does not say which territory it covers before
    1991.)
  - The panel's participation series uses this flow only. The lower rungs of the design review's ladder (national
    LFS, ILOSTAT survey and census points) would add only a few country-years with five-year bands, few of them in
    countries with a floor measure, and none with this flow's cycle measure. They are not used in any test.
- **L5. The cycle, from the same source:** U_ct = the unemployment rate at 25-54, both sexes, from the same flow,
  key `{REF_AREA}.UNE_RATE.PT_LF_SUB._T.Y25T54.UNE`, at the observation year. One source per country, never
  spliced. An observation without U_ct leaves every test that controls for it.
- **L6. q, rents relative to prices, by a source ladder:** `x_ct = log q_{c,t-1}`, lagged one year.
  - **The ladder is frozen at L2** (`data/coverage.json`, `q_ladder`, from availability and documentation). At each
    opening every q year takes the source the frozen ladder names; a value that is missing, or flagged under L3, is
    missing inside its run and never shortens a run, moves a source or splits a segment (settled 2026-10-09). B flags
    and interpolated capital gains still start segments by rule (L7).
  - **Rung 1, the Jorda-Schularick-Taylor Macrohistory Database, Release 6** (`JSTdatasetR6`, macrohistory.net).
    The rent index is `housing_rent_yd × hpnom`, or `housing_rent_yd ×` the cumulated `housing_capgain` for ESP,
    ITA and PRT, where `hpnom` starts late. q = rent index / `cpi`. Countries: AUS, BEL, CHE, DEU (from 1962), DNK,
    ESP, FIN, FRA, GBR, ITA, JPN (from 1960), NLD, NOR, PRT, SWE, USA, to 2020. BEL 1965-1975 is missing and stays
    missing.
  - **Rung 2, the OECD analytical house-price rent index over the all-items CPI.** RPI from
    `OECD.ECO.MPD,DSD_AN_HOUSE_PRICES@DF_HOUSE_PRICES,1.0`, key `{REF_AREA}.A.RPI.IX`; CPI from
    `OECD.SDD.TPS,DSD_PRICES@DF_PRICES_ALL,1.0`, key `{REF_AREA}.A.N.CPI.IX._T.N._Z`.
    - For any country whose `DF_PRICES_ALL` annual CPI ends before its last q year (from the 2026-10 metadata: JPN
      after 2020, CRI after 2021, MEX and CHL after 2023), the CPI is extended from
      `DSD_PRICES_COICOP2018@DF_PRICES_C2018_ALL,1.0`, same key; the switch is a segment.
    - That flow does not cover AUT, COL, DEU, ISR, KOR, NZL, POL, SVK, GBR or USA, so their CPI cannot be extended
      this way. The RPI itself ends early for CHL (2023) and AUS (2024); nothing extends it.
  - **Extend, don't fill.** A country takes rung 1 over the **longest contiguous run of q years t − 1 that overlaps
    the country's unseen observation window**, its length counted inside the window (ties: the later run). Rung 2 may
    only extend that run backwards or forwards (for JST countries: from q year 2021, or from the last documented
    JST year under L3). It never fills a gap inside a rung-1 run. Inside a run, a gap stays missing. Overlap years
    are never used to choose a source and never to link levels.
  - **Known weaknesses, disclosed.** The denominator is all items (which contains rent), not goods: a long goods CPI
    exists for almost no country before 1985. The CPI rent component prices sitting tenants, is regulated in many
    countries and years, and under rationing is not the price young outsiders face (LR-RC). The JST rent index is
    a constructed series: a rent-price ratio anchored to 2012-2014 and extended backwards from national rent
    components, in places rescaled (RORE documentation, section 2.4). That OECD's RPI is the CPI actual-rentals
    component is assumed, not confirmed.
- **L7. Segments: a splice is a fixed effect.** A new segment starts, for a country and a series, at:
  - every source switch (including the L6 rung and CPI-flow switches);
  - every break flag in the source (OECD OBS_STATUS B), applied mechanically when the values arrive, as in C3;
  - every redesign or definitional change named in the source documentation: the OECD's `LFSNOTES_SOURCES.pdf`
    Table 6, the BLS and Census notes for the US, the JST and RORE documentation (including R6's 2016-2020
    extension method and every stretch the documentation says was rescaled), the ILO notes for L11;
  - every change in the lower age limit (14, 15, 16) and in the treatment of the armed forces or of unpaid family
    workers;
  - every territorial change (JST's Germany at 1991, if its documentation names one);
  - for census coresidence (L10), every change in a country's RELATE child-code scheme or household concept between
    two censuses, as recorded at L2.

  The table `longrun/data/segments.csv` (geo, series, tau, reason, citation) is compiled from documentation alone
  by an agent given no values, and **frozen at the L-freeze**. Each segment start τ of any series in a regression
  (outcome, tested regressor, controls) adds `1[geo = c, year ≥ τ]`, through the frozen `specs.break_dummies`;
  for lagged q, a segment starting in year τ acts from τ + 1 (C3). With a country-level moderator this is
  equivalent to country × segment fixed effects for outcome and q in a linear term. **It is not equivalent in the
  piecewise basis of section 5**, which is therefore built inside one q segment per country.

  A documented break found after the freeze **never enters a primary run** (section 8): it enters only the
  no-verdict run "with post-freeze segments".
- **L8. Units and missing cells.** Rates in percentage points. A missing sub-cell makes the band missing. No
  outlier rule of any kind.
- **L9. The floor measure F_L, from IPUMS-International census microdata (Extract A).**
  - **Definition.** The share of persons aged 25-34 living with a parent, in the **earliest** census sample with
    1955 ≤ year ≤ 1975 (her decision). The share is weighted by PERWT, computed for men and women separately, and
    F_L is their equal-weight mean.
  - **The frozen sample list.** At L2 the list of IPUMS-I sample IDs is frozen from the public sample list and
    codebooks (metadata): every IPUMS-I **census** sample for an OECD member (the 38 of 2026) with census year
    1955-1975. Survey samples are not included. Samples IPUMS releases after L2 are ignored. For each frozen sample
    the L2 file records the RELATE detailed codes it uses, its household concept, its GQ coding, whether it is
    organised into households, and any grouped-age coding (AGE2). From the public lists of 2026-10-08 the list is
    expected to be: AT 1971; CA 1971; CH 1970; CL 1960, 1970; CO 1964, 1973; CR 1963, 1973; DE 1970 (West), 1971
    (East); FR 1962, 1968, 1975; GB 1961, 1971 (no RELATE); GR 1971; HU 1970; IE 1971; IL 1972; MX 1960, 1970; NL
    1960, 1971; US 1960, 1970.
  - **Which sample sets F_L.** The earliest frozen sample of the country that records RELATE. A second sample, the
    one **nearest 1970** (ties: the earlier), is used only by the robustness run "F_L nearest 1970, later years
    only".
  - **Samples of individuals are admissible.** Several samples are "persons not organised into households" (from
    the sample pages: CA 1971, CL 1960, CO 1964, CR 1963, DE 1970, MX 1960, NL 1960). RELATE is recorded on each
    person's record, so F_L is computed from them like any other. MOMLOC and POPLOC do not exist there.
  - **"Living with a parent"** = RELATE general code 3 (child of the household head), every detailed code under it.
    - A sample whose child category, by its codebook or comparability notes, includes children-in-law or
      grandchildren, uses a combined detailed code (child/child-in-law, child/child-in-law/grandchild), defines the
      household as the census family rather than the dwelling, or codes persons outside the primary family as
      unknown, is **flagged** at L2. Expected flags from the comparability pages: DE 1970, AT 1971, CH 1970 (child
      includes children-in-law); FR 1962 (includes grandchildren); CO 1964 (census family: a married child living
      with a spouse in the parents' dwelling heads a separate household); IE 1971 and HU 1970 (persons outside the
      primary family coded unknown); NL 1960/1971 and CR 1963 (coarse coding) are recorded and flagged if the L2
      reading shows the child category is affected.
    - Flagged samples enter the primary as the earliest census (her decision); the no-verdict run "flagged samples
      dropped" reports what they carry. The share of 25-34s in each combined detailed code is reported per sample.
    - Not counted, by construction, and disclosed: a young adult who heads a household with a parent present, and
      a married child living with parents-in-law (coded child-in-law, outside general code 3). Both undercounts are
      likely larger in extended-household settings.
    - RELATE unknown is excluded from numerator and denominator; its share among 25-34s is reported per sample.
  - **Group quarters, by one mechanical rule.** A person whose GQ code is a group-quarters code is excluded. Where a
    sample does not identify group quarters (CO 1964, MX 1960, NL 1960 and 1971 by the 2026-10 notes), all persons
    are kept. Each sample's own GQ definition is followed as coded: US 1960-70 counts 5 or more unrelated persons as
    group quarters, and IL 1972 codes kibbutz households as "other group quarters", so kibbutz members are excluded
    in IL. The asymmetry is disclosed, not corrected.
  - **Grouped ages.** Where AGE is coded at interval midpoints (NL 1960/1971, IL 1972, IE 1971), cases are selected
    by interval. A sample whose intervals do not align with 25-34 (or 20-29) drops from that measure only. The
    intervals are an L2 record; a grouped sample read without one is unusable (that sample only), so the record is
    a condition of the tag (IL 1972 sets the F_L of an LR-K2 country).
  - **Territory.** The sample must cover the panel's territory: DE uses the 1970 West German sample, and DE's panel
    is the former Federal Republic (L4); the 1971 East German sample is excluded by L2.
  - **No proxy.** A country without such a sample with RELATE drops out of every test that uses F_L. No proxy
    substitutes in a primary run. The Giuliano-Nunn family-organisation measure is a no-verdict robustness run
    (section 5).
  - **Standardised and split.** For D1-L, F_L is standardised over the test's countries (mean 0, sd 1). For
    LR-K2, `H_c = 1` (high floor) for the countries in the top half of F_L among the test's countries; with an odd
    count, the middle country is low floor; ties are broken by country code.
    - **When H is computed, and over whom:** once, at the look, after q has been fetched and before any confirm
      outcome is fetched, over the LR-K2 countries left after the mechanical drops (a frozen F_L sample found
      unusable when read: no RELATE, no weights, no 25-34 cases, or grouped ages without a recorded interval; and
      the q rule of section 5). It is **never recomputed**: not in the leave-one-out, qualifier or robustness runs,
      and not if a country later drops for any other reason. The exception, settled 2026-10-09: the three robustness
      rows that define another F (Giuliano-Nunn, F_L at 20-29, F_L from the sample nearest 1970) split that F by
      the same rule over their own countries, since the other F is what those rows vary; every other robustness row
      holds H fixed. An H computed on the explore half alone before the look is exploratory.
    - If fewer than 8 countries, or fewer than 3 in either group, remain after these drops, LR-K2 is "not
      testable" and the model-level verdict is "not testable".
  - **The extract, exactly.** She registers with IPUMS-International and makes it herself:
    - **Samples:** exactly the frozen sample IDs, no others.
    - **Variables:** COUNTRY, YEAR, SAMPLE, SERIAL, PERNUM, HHWT, PERWT, AGE, SEX, RELATE, MOMLOC, POPLOC, GQ (her
      list). Nothing else: **no labour, education, income, marital-status or tenure variable.** Labour, education
      and tenure would be outcome values of this holdout.
    - **Case selection:** persons aged 20-34 only (household members of selected persons not included).
    - **Format:** CSV, rectangular (person records), compressed, plus the DDI codebook (XML) with the same file stem.
      Extracts A and B may be one extract or two; each CSV needs its own DDI.
    - **Where:** `participation/longrun/data/ipums/` (gitignored, with any stray `ipumsi_*` file anywhere; IPUMS
      terms forbid redistributing microdata). The loader refuses while any IPUMS microdata lies under `longrun/`
      outside that folder, an extract whose DDI lists a sample outside the frozen list, and a row aged outside
      20-34. Only the extract request (sample IDs, variables,
      case selection, extract number) and, after the look, the aggregate F_L values with the IPUMS citation are
      committed.
    - **When:** after the `participation-L-freeze` tag. The extract holds regressor values. (An extract was found
      on disk before the tag on 2026-10-09: section 7.)
  - **The guarded loader** (`longrun/code/ipums.py`) is the only reader.
    - It refuses the file if it holds any column other than: her variables; RELATED, the detailed version IPUMS
      delivers with RELATE; the technical variables the extract builder preselects; and data-quality flags of the
      listed variables that IPUMS attaches automatically. The IPUMS-I names (the flag variables and PARRULE,
      STEPMOM, STEPPOP if attached) are confirmed at L2 against the extract builder's variable list or the DDI of a
      test extract with no data. MOMLOC and POPLOC are read only for the pointer check of section 5.
    - **Row-level guard:** it reads a sample's rows only when that sample's country's half is open (the European
      `eurostat.guard` pattern), and it never reads a frozen sample a rule does not use.
- **L10. Coresidence as an outcome (LR-C1), from Extract B.**
  - **Which censuses:** every IPUMS-I **census** sample of an OECD member with census year 1976 or later inside the
    unseen cells (the 31 European countries: 1976-1994; the others: 1976-2025 except 2020-2021), with x available.
    Survey samples are excluded, including the US 2005-2020 samples that IPUMS-I flags as American Community Survey
    household surveys and Mexico's 2015 Encuesta Intercensal. Each sample's kind (census, count or survey) is read
    from its IPUMS description at L2 and recorded; Mexico's 1995 and 2005 Conteos stay as censuses unless that
    reading says otherwise. The F_L samples and the other 1955-1975 samples are **not** LR-C1 observations: the critic
    expects coresidence to fall in 1950-75 where q was low or controlled and marriage early, an opposite-signed
    regime that a linear b > 0 test must not mix in.
  - The sample IDs are frozen at L2 with Extract A's records (RELATE scheme, household concept, GQ coding). The same
    variables, case selection, format, RELATE, GQ and unknown rules as F_L apply. A change in a country's child-code
    scheme or household concept between censuses is an outcome segment (L7).
  - **The outcome R_cy** is F_L's construction applied to each census: the share of 25-34 living with a parent,
    sexes equal-weighted.
  - It is made after the L-freeze. Whether she makes Extract B is her call, recorded in the freeze commit; without
    it LR-C1 leaves its family before the tag.
- **L11. School attendance (C-6L):** the share of 20-24-year-olds attending school, both sexes, from ILOSTAT
  `POP_3WAP_SEX_AGE_STU_NB_A` (YOUTHSTATS, annual): attending / (attending + not attending); "not stated" is left
  out of the denominator. One source; each change of underlying survey named in the ILO notes is a segment.
- **L12. Design covariates and controls:**
  - population on 1 July 1960 (UN WPP2024, total; a design covariate for the split, fetched before the freeze; the
    L3 exception);
  - relative cohort size = population 25-34 / population 35-64 (UN WPP2024, five-year groups; a control used
    only by LR-K2's cohort-size qualifier, fetched after the freeze; the L3 exception);
  - **rent regulation from Kholodilin's published rental-regulation dataset** (Housing Policy Debate 2020 and its
    data release; the 2018 DIW discussion-paper version covered 47 countries). It is used only to drop strict-control
    country-years, in the "strict rent control dropped" run and in the "rests on control-era years" qualifier.
    - "Strict" is Kholodilin's own definition of **first-generation** rent control, quoted word for word from the
      dataset's documentation into the L2 file.
    - Second-generation (tenancy) controls also attenuate CPI-q, but they leave the entry rent at market, which is
      the price a young outsider pays, and they cover most post-1970s European years; dropping them would remove the
      panel. They are not dropped.
    - Countries the coding does not cover keep all their years, and the report lists them. The control-era bias of
      section 2 sits in the long-history low-floor countries, so the run is informative for LR-K2 even if the
      high-floor countries are absent.
    - At L2 the file, its country list and its variable codes are confirmed from documentation. If the coding is
      published only as tables, it is transcribed by the design review's double-entry rule (S10), from the published
      coding, with no judgement. If it is not published at all, the run and the qualifier are dropped before the
      freeze and replaced by nothing; LR-K2 and LR-Y0 then carry the standing disclosure "control-era years not
      separable".
- **L13. Weighting and clusters:** every country-year has weight one (no population weights, as in C8); the cluster
  is the country. DE is one cluster. In an unbalanced annual panel this gives long histories more country-years (the
  US holds 37 of LR-K2's 273 eligible country-years at L2), but not necessarily more identifying variation: before
  the look, each country's share of the identifying variation of LR-K2's DiD (its share of the squared residualised
  tested regressor, from the skeleton simulation) is published with the freeze (`data/skeleton.json`; at L2 the four
  Latin American countries hold over half of it and the US about a twentieth), and the same shares from the real
  data are reported after the look, by country and by stratum. If leaving out the US alone moves a verdict's
  own-direction p above 0.10 (or flips its sign), its leave-one-out qualifier reads "rests on the US, a partly seen
  country", whichever country's removal is worst; every country's leave-one-out row is reported.
- **L14. Fetch discipline:** one door, `longrun/code/fetch.py`, logs every download in `longrun/data/fetch_log.jsonl`
  (URL, UTC time, half, SHA-256). Raw files are not committed. ILOSTAT and JST files are hashed at fetch, since both
  update.
  - **Row-level guards** on every reader of a file that holds several countries (JST, ILOSTAT, IPUMS, OECD
    multi-country pulls): confirm-country rows are refused before the LE-freeze.
  - **Order at each opening** (the explore opening at L4, the confirm opening at the look): q is fetched first; the
    knots of section 5 are computed from q alone and written with their hash to the log; F_L is read (at the look,
    H is then computed); only then are outcomes fetched.
  - **Knots are never recomputed after outcomes are seen.** Explore countries keep their hashed explore-opening
    knots at the look; only confirm countries' knots are computed at the look. The confirm run downloads all
    countries in one vintage and reports any difference against the logged explore-half hashes; a changed explore
    q value enters with the frozen knots.

**Testability, from coverage alone.** A test runs only if enough countries can enter it. The counts are made by
code at L2 from:
- **OECD flows:** per-year `availableconstraint` probes (startPeriod = endPeriod = year) for every key a test
  uses, the A2534 cells `Y25T29` **and** `Y30T34` of both sexes, U, RPI and both CPI flows included. A range query
  gives only first and last years and hides gaps (IRL, MEX 1992/1994, COL 2006), so it is not used. These probes
  return no values and no flags.
- **JST and ILOSTAT**, which publish no values-free availability: a values-dropping script (the scouts' `cov.py`
  pattern) that keeps only country, year, non-missingness and the L3 flag columns, discards every value at parse,
  prints and writes no value, and is committed and logged.
- **IPUMS:** the frozen sample list and its codebook records.
- **segments.csv**, for the q segment of each country.

The resulting per-country eligible-year lists and counts are written to `longrun/data/coverage_l2.csv` and frozen.

- **LR-K2:** at least 8 countries with a frozen F_L sample and at least 9 eligible observation years each, counted
  inside the country's **chosen q segment** (section 5). An eligible year has the four A2534 cells and U_ct
  available by the probes and x_ct available inside the chosen segment. (With at least 8 countries the median split
  puts at least 4 in each group.)
- **LR-Y0:** at least 8 countries with at least 9 eligible years inside their chosen q segment.
- **C-6L:** at least 8 countries with at least 2 observations inside one segment of outcome and regressor.
- **LR-C1:** at least 8 countries with at least 2 Extract B censuses with x inside one q segment and one outcome
  segment.

**Frozen membership.** The country lists, the eligible-year lists and the family sizes are frozen with the tag.
A cell later found flagged under L3, when its value arrives, becomes missing in the regression; it never changes
a country's membership, a family size or a knot. The only post-freeze drops are the mechanical ones named in L9
(an unusable F_L sample) and section 5 (fewer than 6 ranked q years), all decided from regressor data before any
outcome of that half is fetched. A test that fails testability at L2 leaves its family before the L-freeze. If
LR-K2 fails, the long-run model-level verdict is "not testable" and only no-verdict results are reported.

**What coverage suggests now** (the scouts' years-only files, range queries and public sample lists; L2 decides by
code and recounts inside the chosen q segment, which will shorten some histories):
- **LR-K2 (at L2, `coverage_l2.csv`, inside each chosen q segment):** 9 countries: CA 48, IL 39, US 37, MX 30,
  CL 27, CR 25, DE 25, CO 22, FR 20 eligible years. The US's chosen q segment is 1950-1995 (JST's US rent index
  changes source in 1996, RORE Table 18), so its eligible years are 1960-1996, not 64. ES, IT and PT, and JP and KR,
  have no IPUMS-I census by 1975 and drop out. NL has 8 eligible years (1987-1994) and drops out; IE has 4, CH 4, GR 5
  and AT 1; HU has none (L2, and its RPI starts in 1996). **LR-K2 passes testability by 1 country**: losing any one
  country leaves 8, any two leave it "not testable". The confirm half holds 4 LR-K2 countries (CR, DE, IL, MX), below
  the floor of 8, so LR-K2's confirm-half replication is reported for information only (whenever each floor group has
  at least 2 countries) and LR-K2's primary can never fall back to it (section 8).
- **LR-Y0:** 21 countries (AU, BE, CA, CL, CO, CR, DE, DK, ES, FI, FR, IL, IT, JP, KR, MX, NZ, SE, TR, UK, US).
  IT's `Y30T34` starts in 1983, against 1970 for `Y25T29`.
- **C-6L:** 16 countries from the documented ILOSTAT first years (BE, CA, CH, CL, DE, DK, EL, ES, FR, IE, IT, LU, NL,
  PT, UK, US); L2's values-dropping pull decides.
- **LR-C1, with Extract B:** 13 countries (AT, CA, CH, CL, CR, ES, FR, IE, IL, MX, PT, TR, US). CO has only its 2005
  census with q, DE no RELATE after 1970, GR only 1991 with q; HU and PL fall under L2.
- **D1-L:** about 9. **The Giuliano-Nunn run:** about 21.
- **The standardised MDEs** (`data/skeleton.json`) are above their European benchmarks for every verdict test, so
  under the reading table an inconclusive verdict will read "uninformative", not "no support"; the forecasters are
  told so on the sheets.

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
- **Before the L-freeze:** nothing but metadata (codelists, availability, documentation, sample lists), the
  values-dropping coverage masks of section 3, the 1960 population, and the seen European data (observation years
  1995 on) for the benchmark and simulation steps of section 5; European raw rows at or before 1994 are dropped at
  parse.
- **From the L-freeze:** the explore half freely, inside the unseen cells. The US deep study runs first (section 6).
- **Before the LE-freeze:** the loaders refuse confirm countries, row by row (L14).
- **At the look:** one run of `confirm.py`.
- **After the look:** free use, all labelled exploratory. New long-run hypotheses go only to the 2026-2028 time
  holdout or to OECD members never fetched.

## 5. The tests

Every panel regression has country and year fixed effects, the segment dummies of L7 and the cycle control U_ct,
unless stated. Inference is the restricted wild cluster bootstrap-t (Webb weights, B = 9999, clustered by country,
CR1), one-sided in the predicted direction, with confidence intervals by test inversion. It uses the frozen
`participation/code/inference.py` (`wcr`, `ci`, `ri`, `g_star`, `mde`) and the verdict helpers of
`participation/code/specs.py` (`break_dummies`, `holm`, `holm_reject`, `qualify`), by import, unedited.

**The piecewise basis.** LR-K2 and LR-Y0 share it, and the US deep study uses it on US data.
- **One q segment per country.** Terciles and knots are computed within a single q segment: the **chosen q
  segment**, the country's longest q segment by its count of q years t − 1 whose observation year t lies in the
  unseen window (ties: the later segment). It is chosen at L2 from `segments.csv` and availability. If B flags
  arriving with the q values split it at the opening, the longest piece is used (ties: the later), still from q
  alone. Observations whose lagged q lies in another segment are dropped from LR-K2 and LR-Y0 (they stay in every
  other test). No tercile spans a seam, so no unlinked index base decides which years are "high q".
- **The ranking set** is every observation year t inside the country's unseen window with x_ct available (L3 flags
  of q applied) inside the chosen segment, known from q alone. Outcome and U availability play no part; years
  whose outcome or U later proves missing drop from the regression without moving the knots.
- **Terciles and knots.** The ranking-set years are ranked by `x_ct = log q_{c,t-1}` (ties by the earlier year);
  with n years, rank r falls in tercile `ceil(3r/n)`. The knot k1_c is the midpoint between the largest x in
  tercile 1 and the smallest in tercile 2; k2_c likewise between terciles 2 and 3. A country with fewer than 6
  ranked years at its opening leaves LR-K2 and LR-Y0, mechanically, from q alone.
- **The basis:**

  ```
  P1 = min(x, k1)            P2 = min(max(x − k1, 0), k2 − k1)            P3 = max(x − k2, 0)
  ```

  so that A = γ1·P1 + γ2·P2 + γ3·P3 is a continuous broken line whose slopes are γ1 (bottom tercile), γ2 (middle)
  and γ3 (top). Adding a constant to x within the segment shifts both knots by it, leaves P2 and P3 unchanged and
  shifts P1 by the constant, which the country effect absorbs: a check asserts this invariance on synthetic data.
- The knots are fixed at each opening before outcomes are fetched, and frozen thereafter (L14).

### K: the distinctive test (the model against the no-coresidence account)

- **LR-K2. The regime-aware floor kink.**
  - **Equation:**
    `A2534_ct = a_c + d_t + Σ_j [ γj·(1 − H_c)·Pj_ct + γj^H·H_c·Pj_ct ] + g·U_ct + segments + e_ct`, j = 1, 2, 3,
    on each country's chosen q segment.
  - **Tested quantity:** the difference in differences `DiD = (γ3^H − γ1^H) − (γ3 − γ1)`: how much more the
    slope falls from the bottom to the top tercile in high-floor countries than in low-floor ones. It is estimated
    as one coefficient of the same regression written in the equivalent ramp basis, so that the frozen `wcr` can
    test it.
  - **H1:** DiD < 0.
  - **The foils** (section 2): the no-coresidence account has DiD of about 0 under equal scaling of the two groups,
    and a top-minus-bottom difference > 0 within each group; any proportional attenuation at high floor also gives
    DiD < 0, with γ3^H − γ1^H > 0.
  - **The drop condition** (decides the model-level reading of a supported LR-K2): γ3^H − γ1^H < 0 (point
    estimate) and γ3^H not significantly positive (WCR one-sided p ≥ 0.05 for γ3^H > 0).
  - **Reported with no verdict:**
    - `slope_top(high F) = γ3^H`, with its one-sided WCR p for γ3^H > 0, beside γ3 at low floor and γ3^H − γ1^H.
      The model predicts γ3^H < γ1^H and γ3^H < γ3; it predicts γ3^H ≤ 0 only if floor-types dominate or jobs
      require one's own dwelling (section 2).
    - **The scale-free companion:** γ3^H / γ1^H against γ3 / γ1 (each group's top slope over its bottom slope),
      point estimates with both bottom slopes and their standard errors. It is unstable where a bottom slope is
      near 0 (control eras, LR-RC) and is read with that caveat.
    - γ1, γ2, γ3 for each floor group, and each country's own top-minus-bottom change from a country-by-country
      fit (a table, no inference).
  - **Inference:** the tested variation is country-level (H_c), so **randomisation inference is co-primary**.
    - H is permuted across all the test's countries (not within strata, since floor and stratum are likely
      aligned), with the number of high-floor countries fixed. Every H-interaction is rebuilt for each assignment
      and the CR1-studentised t recomputed. Enumeration is exact (252 assignments for 10 countries).
    - The frozen `inference.ri` permutes only the tested regressor, so this RI is written in
      `longrun/code/inference_l.py`. It is checked against `inference.ri` on a design with one interaction and at
      most 7 units, where both enumerate exactly, to a tolerance of 1e-10 in p.
    - **The verdict statistic is max(p_WCR, p_RI)** in each direction; p_opposite is the larger of the two
      opposite p's. It is then size-calibrated (below). If the RI cannot be computed (the observed contrast is
      not identified, or an enumerated assignment leaves it unidentified), the verdict statistic is missing,
      never the WCR p alone, and the test takes p = 1 in its family (below).
  - **Mechanical qualifiers.** Each uses the verdict statistic (max(p_WCR, p_RI), calibrated) and fires when the
    named change flips the sign of DiD or pushes the p in the verdict's own direction above 0.10. H is held fixed
    in every qualifier run.
    - **"rests on one country (XX)"**, the frozen leave-one-country-out qualifier; for XX = US it reads "rests on
      the US, a partly seen country", and that sentence is added whenever the US row alone crosses 0.10 (L13).
    - **"rests on floor-group trends"**: H × year fixed effects added. In years in which only one floor group is
      observed, the H × year dummies are collinear with the year effects and are dropped by rule.
    - **"rests on cohort size"**: relative cohort size (L12) added as a control.
    - **"rests on control-era years"**: the Kholodilin strict-control country-years dropped (L12).
    - **"indistinguishable from time curvature"**, which fires if either of two runs says so:
      - *time terciles*: the same regression with each country's ranking-set years assigned to terciles by
        calendar year instead of by x (x × 1[year tercile j] by floor group, with country × year-tercile effects;
        the terciles are formed on the ranking set, from q alone, before any outcome filter);
        it fires if the time-tercile DiD's t is at least as large in the predicted direction as the primary's t;
      - *series-permutation placebo*: each country is given another LR-K2 country's x path (a random derangement;
        999 draws, seed `inference.SEED`), aligned at the start of its own ranking set, with years beyond the
        donor's length dropped from that draw; terciles and knots are recomputed from the donor path by the rule
        above; it fires if the observed t lies inside the central 80% of the placebo t's.
  - **Where reported:** the men-only run is reported beside the primary, not in the robustness table's place, as
    the theory-clean version (section 2). It carries no verdict.

### C: consistency checks (shared with standard models)

- **LR-Y0. The young respond positively before enclosure.**
  - **Equation:** `A2534_ct = a_c + d_t + γ1·P1 + γ2·P2 + γ3·P3 + g·U_ct + segments + e_ct`, all countries with q
    (no floor measure needed), on each country's chosen q segment.
  - **H1:** γ1 > 0, the slope in each country's bottom tercile of q.
  - **Reading:** under binding rent control the model predicts about 0 (LR-RC), and about 0 for young men near
    saturation, so a null is not a contradiction of the floor; a negative γ1 counts against enclosure for the young
    (the paper's exit proposition (iii)) or the auxiliary s0 < w.
  - **Reading note for an inconclusive LR-Y0.** In long-history countries the bottom tercile is largely the
    control era. An inconclusive LR-Y0 reads "no support" only if the strict-control-dropped run is itself not
    significant in the predicted direction (max p ≥ 0.05) and LR-Y0's pre-look standardised MDE (the primary's: the
    strict-control years are control values, unknown before the freeze, so that run has no pre-look MDE; settled
    2026-10-09) meets the benchmark rule below.
    If that run is significant in the predicted direction, it reads "consistent with LR-RC attenuation". Otherwise,
    or if the Kholodilin coding is unavailable, it reads "uninformative".
- **C-6L. School as a paid exit** (the European C-6, backwards).
  - **Equation:** the share of 20-24 attending school (L11) on U_ct (L5, the same year).
  - **Controls:** none beyond fixed effects and segments; the regressor is the cycle, so U_ct is not added again.
  - **H1:** b > 0.
  - **Reported with no verdict:** E-SCH1-L, the same on U_{c,t-1}, the form of the surviving European E.
- **LR-C1. Coresidence absorbs rents** (only if Extract B is made; L10).
  - **Equation:** `R_cy = a_c + r_round + b·x_cy + segments + e_cy`, at the Extract B census years. Round fixed
    effects by census decade (1975-84, 1985-94, … , 2015-24) replace year effects. No cycle control (U_ct is missing
    at many census years).
  - **H1:** b > 0.
  - **Reading:** a null or negative slope with clean q, **and assuming outright-owning parents, which is
    unmeasured**, would refute the paper's mapping of the modern dependency floor to the parental home. That is an
    auxiliary, but the floor mechanism has no empirical carrier without it. Because the ownership condition is not
    measured, a contradicted LR-C1 is reported as against the mapping "where parents own outright, if they do".

### No verdict (reported, never counted)

- **D1-L:** `A2534_ct = a_c + d_t + b1·x_ct + b2·(x_ct × F_c) + g·U_ct + segments`, F_c = standardised F_L.
  Reported: b2, its p in both directions by WCR and by `inference.ri` (x_unit = F_c, x_mult = x_ct, within the split
  strata, x_ct kept in Z), and the slope at the 75th percentile of F.
- **D2-L:** A2534 on x_ct and `(x_ct − m_cs)²`, where m_cs is the mean of x within country × q-segment (a level
  shift in a spliced q is not absorbed by a square otherwise). Reported with the series-permutation placebo of
  LR-K2's qualifier, applied to D2-L's t.
- **C-2L:** `A2534 − A5564` on x_ct. **C-3L:** `A_W(25-54) − A_M(25-54)` and `A_W(25-54)` on x_ct.
- **The pointer check** (a measurement check, no regression): in the frozen samples organised into households with
  MOMLOC and POPLOC (expected: US 1960, FR 1962, IL 1972 among the F_L samples), the share of 25-34s with a
  coresident parent by the pointers, against the RELATE share.
- **E-SCH1-L** (above) and the US deep study (section 6).

### Verdicts

- **Per test**, as frozen: *supported* when the one-sided p survives Holm within its family at familywise 0.05;
  *contradicted* when the opposite-direction p does; *inconclusive* otherwise. The p is the size-calibrated one
  (below).
- **Families:** K = {LR-K2}; C-L = {LR-Y0, C-6L, LR-C1} (LR-C1 only with Extract B); E-L = up to three, confirm half
  only. The sizes are frozen at the L-freeze from coverage. A frozen member whose run errors at the look takes p = 1
  in both directions inside its family; it never leaves the family (settled 2026-10-09).
- **Qualifiers never change a verdict label, in either direction.** They attach to a supported and to a
  contradicted verdict alike, by the same mechanical rules. The one pre-registered condition that shapes the
  model-level reading is LR-K2's drop condition, defined above.
- **Rests on one country:** the frozen leave-one-country-out qualifier (LOO_P = 0.10), with H held fixed.
  Leave-one-stratum-out and G* are reported, not acted on; leave-one-stratum-out reports "not estimable" when either
  floor group falls below 2 countries.
- **The long-run model-level verdict rests on LR-K2 alone:**
  - *favours the floor mechanism against the no-coresidence and attenuation accounts*: LR-K2 supported and the drop
    condition holds;
  - *consistent with the floor mechanism or with an attenuated response at high floor (carried by low-floor
    convexity)*: LR-K2 supported and the drop condition fails;
  - *against the floor mechanism together with its stated regime placement and auxiliaries 1-3* (section 2): LR-K2
    contradicted;
  - *inconclusive* otherwise; *not testable* under section 3 or L9.

  It carries LR-K2's qualifiers. A supported LR-K2 is never reported without the sentence that it does not
  discriminate against life-cycle models with a below-market parental room (section 2). Whenever LR-C1 is
  contradicted, the model-level sentence reports LR-C1's verdict beside LR-K2's.
- **What C-L does and does not settle:** C-L verdicts speak to the model's mapping onto groups and to the
  measurement. They do not settle the model against any standard account.

**Size calibration, before the freeze** (`longrun/code/skeleton.py`, its code and seed `inference.SEED` committed
with the tag).
- **The skeleton:** each verdict test's frozen countries, eligible years, chosen q segments and segment table.
- **Synthetic regressors, by a DGP fixed now:**
  - log q: a Gaussian random walk with drift, the drift and innovation SD equal to the pooled mean and SD of the
    annual change in European log q (CP041 / IGD_NNRG, C6) over the frozen European panel (seen data); terciles
    and knots are built from it by the rule above;
  - U: an AR(1) with the pooled mean, SD and autoregressive coefficient of the European U(25-54) series (seen);
  - F: standard normal, split at the median for H.
- **Synthetic outcomes under the null:** country and year effects, country-specific linear trends, floor-group
  linear trends and AR(1) errors, with ρ = 0.5 and ρ = 0.9; the ratios of trend to error variance from the European
  look's D1 full-sample residuals (seen). R = 2000 null replications per ρ.
- **Calibration:** for each test and each direction, the calibrated p is the share of null replications (at the ρ
  that gives the larger share) whose verdict statistic (max(p_WCR, p_RI) for LR-K2) is at or below the observed one.
  The p used for the verdict is max(raw p, calibrated p), in both directions, so calibration can only make a verdict
  harder. Holm runs on these p's; for K, a family of one, that is the calibrated p against 0.05. There is no 0.075
  band: every test is calibrated.

**MDEs and the reading table, before the freeze.** The stated prior is that the model should work back to 1950, so
an imperfect data set invites a motivated reading of a null. The MDEs are computed by one procedure for the long
run and for the European benchmarks alike:
- the skeleton simulation above, with a single ρ = 0.7 on both sides (the midpoint of the calibration range; the
  same value for long run and benchmark, so the comparison does not turn on it);
- MDE = `inference.mde` of the SD of the tested estimate across the null replications (the SD-based t-formula
  figure, labelled so; the power of the actual verdict procedure at it, calibrated, is published beside it);
- **standardised MDE** = MDE × SD(residualised tested regressor) / SD(residualised outcome), so that differently
  scaled regressors and outcomes compare like for like;
- the European benchmarks are the same procedure on the European skeletons, with the segment dummies the European
  look's frames carried: C-6's for C-6L, C-1's for LR-C1, and D1's (31 countries, the years used at the look, H from
  C9's F split at the median) for LR-K2 and LR-Y0.
- **Reported beside the calibration, not in it** (added 2026-10-09; no role in any verdict): LR-K2's size, raw and
  calibrated, at the expected floor split of section 2 (high = the first of CL, CO, CR, MX, IL up to half the
  members), and under stress nulls the calibration DGP leaves out (country-specific logistic curves in calendar time
  timed by floor group, amplitude 10 points, early or late in the high-floor windows; AR(1) errors with ρ = 0.95).
  Whether either should enter the calibration envelope, or the calibration be rerun at the realised H at the look,
  is her decision before the freeze (section 11).

| Verdict | Reading |
|---|---|
| contradicted | stands, whatever the data quality, with the auxiliaries its label names |
| supported | stands, with its qualifiers |
| inconclusive, standardised MDE at or below the European benchmark's | "no support" (LR-Y0: its reading note) |
| inconclusive, standardised MDE above the European benchmark's | "uninformative" |

**The European real-data run of LR-K2 and LR-Y0 (exploratory, no verdict).** `longrun/code/specs.py` (LR-K2,
LR-Y0, their qualifiers) and this protocol are committed first and their hashes logged. The two specifications are
then run **once** from that commit on the frozen European panel (data already seen; European q per C6, F from C9
split at the median), and the commit hash and output are logged. Any later change to the LR-K2 or LR-Y0 code before
the freeze is a recorded pre-freeze amendment, rerun once, and every run is reported. The point estimates are
committed with the freeze, labelled exploratory and no-verdict, and both forecasters see them.

**Two studies, two verdicts.** The European look and the long run each keep their own verdict. There is no
Fisher or Stouffer combination; an inverse-variance pooled number (the European D1's b2 with D1-L's) is reported with
no verdict. The rows are read
in order; the first that applies decides.

| European D1/D2 | Long-run model-level | Joint reading |
|---|---|---|
| either contradicted | any | against the floor mechanism |
| any | against | against the floor mechanism together with its long-run regime placement and auxiliaries 1-3 |
| not contradicted | favours | supported in the long run (against the no-coresidence and attenuation accounts only), not in 2009-2025 Europe |
| not contradicted | consistent with the floor or attenuation | consistent with the floor mechanism in the long run but not told apart from attenuation; not supported in 2009-2025 Europe |
| otherwise | | inconclusive |

The European look found D1 and D2 inconclusive, so in practice LR-K2 decides the joint reading.

**Forecasts.** Before the freeze, she and Claude each fill `longrun/FORECASTS.md`: for each verdict test, the
expected sign of the estimate and the probabilities of each verdict, and the probabilities of each model-level
reading. The sheets are committed with the tag and reported beside the results. A verdict to which every
forecaster gave at least 0.5 is marked "as forecast".

**Robustness, with no verdicts** (ten runs, no more; each row is one run):

| Run | Applies to |
|---|---|
| F from Giuliano-Nunn (Ancestral Characteristics Database v1.1, baseline: the ancestral share in extended-family domestic organisation, v8; codes confirmed from its codebook at L2), all countries with q | LR-K2, D1-L |
| F_L at ages 20-29 | LR-K2 |
| standardised F_L in place of the high/low split | LR-K2 |
| men only (reported beside the primary) | LR-K2, LR-Y0 |
| women only | LR-K2, LR-Y0 |
| strict rent control dropped (L12) | LR-K2 (also its qualifier), LR-Y0 (also its reading note), LR-C1 |
| q_hpi = log(house prices / CPI): JST `hpnom / cpi`, else OECD `{REF_AREA}.A.HPI.IX` over the CPI of L6 | LR-K2, LR-Y0, LR-C1 |
| F_L from the sample nearest 1970, on observation years after that sample's year only (predeterminedness and comparable census timing) | LR-K2, D1-L |
| flagged F_L samples dropped (L9) | LR-K2, D1-L |
| with post-freeze segments (section 8; run only if such segments exist; the rows reach this run only) | every verdict test |

The men-only run is the critic's (LR-F1): before about 1975, young women's floor was the marital household, so the
parental floor applies to young men throughout and to young women only later. The "without the US" comparison is
the US row of the leave-one-out run, reported by name for every verdict test.

## 6. The US deep study (no verdict)

One country, 1948-2025, specified now and run once, first, after the L-freeze; its output is committed as it comes
out, before any free exploration of US data. The US is in the explore half.

- **Participation:** CPS civilian participation rates, not seasonally adjusted, annual means of monthly values:
  25-34 men `LNU01300164` and women `LNU01300327`; 20-24 `LNU01300037` and `LNU01300038`; 55-64 `LNU01300190` and
  `LNU01300347`. 2025 averages the months published. From the BLS API v1 (25 calls a day) or its DBnomics
  mirror `BLS/ln` (last indexed 2026-03-07 when checked; the fetch log records the mirror's index date); the values
  are BLS's either way and the log records the door.
- **q_US:** `log(DTENRG / DGDSRG)_{t-1}`, the BEA PCE price indexes for tenant rent and for goods (NIPA Table 2.4.4,
  annual, 1929-2025), via DBnomics `BEA/NIPA-T20404`, series `DTENRG-A` and `DGDSRG-A`. Rent over goods, as in the
  paper.
- **Coresidence:** Census AD-3, 25-34 living as child of the householder, men and women equal-weighted (CPS ASEC,
  from 1967 to AD-3's last year). AD-1 extends it forward **from the first year after AD-3's last year**, as a new
  segment. AD-1's census points (1960, 1970, 1980) are a separate segment.
- **Enrolment:** Census CPS October Table A-2 (`hst_enroll02.xlsx`), both sexes; 20-24 = (2 × the 20-21 rate +
  3 × the 22-24 rate) / 5, 1959-2024.
- **Cycle:** the CPS unemployment rate at 25-54, not seasonally adjusted (`LNU04000060`), annual mean of monthly
  values, matching the participation series. Its annual mean is close to that of the seasonally adjusted
  `LNS14000060` cached in `paths/cache`, so the US cycle is effectively seen (section 7).
- **Segments:** from BLS and Census documentation, by the L7 rules: the CPS population-control introductions, the
  1967 definitions, the 1994 redesign, the 2014 ASEC redesign and others the documentation names.
- **Analyses, all no verdict:**
  - U-K2: the piecewise basis on the US's own q_US terciles, computed within q_US's longest segment by the rule of
    section 5; γ3 − γ1 and γ3;
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
  UK 1988) and housing allowances (DE, NL, FR from the 1960s-70s);
- the published literature on young adults' coresidence and labour markets (Kaplan; Ermisch; and others).

**Seen in this repository or this study:**
- The European data, through the look (`results/confirm_8623706.json`), observation years 1995-2025: the European
  panel grid starts in 1995, and the exploration's committed outputs hold 1995-1996 activity rows for the explore
  countries (hence L1's cut at 1994). Three exploration outputs reach back to 1983 for BE, CH, FI, FR, HU, IE, IT, LU,
  PT and SE (inactive 55-64 by wish to work; occupation shares by age); none holds a verdict test's variable, and
  they are listed by name in `data/seen.json`. The European raw cache (`participation/data/raw`) holds the full
  Eurostat history, pre-1995 values of the long-run outcome and cycle included (lfsa_argan, lfsa_urgan, lfsa_ergan,
  prc_hicp_aind); nobody viewed them, and the skeleton drops every row at or before 1994 at parse. Moving or trimming
  that cache before the tag is her call. All eight European primaries were
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
the Bank of England workbook, and others). The pipeline never reads them: it fetches anew through its own logged
door. Because a promise alone is no guard, **before the freeze** every such file is hashed and listed in
`seen.json`, and the folders are moved to a location she chooses outside the repository and outside any session
scratchpad that agents read; deleting them is her call. The move is recorded in `STATE.md` and the freeze commit.

**Incidents of 2026-10-09 (the pipeline's code review).**
- An IPUMS-International extract (`ipumsi_00001.csv.gz`, 1,565,024,917 bytes, created 10:37 and last written 11:08)
  was found directly in `longrun/data/`, outside `data/ipums/`, before the L-freeze tag, with no DDI beside it and no
  fetch-log record. Its size suggests more than the frozen samples, the 13 variables and the 20-34 selection. No
  agent opened it: the reviewers and the fixing agent read its name, size and times only. Its last-access time moved
  twice during the review (12:16 and 12:21) without any agent opening it; it cannot be attributed from here (an
  antivirus scan is the likely reader). The loader refuses while it lies there, the gitignore covers it, and
  `checks/check_freeze_ready.py` lists it. Where it goes, and whether it is kept, is her call; after the tag the
  extract is re-made or re-verified against the frozen sample IDs, variables and case selection before the loader
  reads it.
- Single-file sources (the JST workbook, WPP by age, Giuliano-Nunn) are cached whole under `longrun/data/raw/<half>/`
  after the L tag, so the explore half's JST file holds confirm countries' rows before the LE tag. Only the loaders'
  row cut stands between them and an analysis; `checks/check_guard.py` K1 checks that no script under `code/` or
  `checks/` names those folders.

**The forecast sheets** record what each participant expects before the look. Country-level prior knowledge cannot
be removed, so the time holdout remains the only clean test.

## 8. Bug policy

- **Between the L-freeze and the LE-freeze:** plumbing (fetching, parsing, variable construction) may be fixed where
  the code departs from text frozen here. Each fix gets its own commit with the reason.
- **Segments are not plumbing.** `segments.csv` is frozen at the L-freeze for every primary run. B flags arriving
  with values are applied by rule (L7), with no judgement. A documented break found after the freeze enters only the
  no-verdict run "with post-freeze segments". Before the LE-freeze she may commission **one** documentation re-read
  by a fresh agent given no values, covering every country of both halves; its complete output, not a selection
  from it, defines that run. Nothing found after the freeze enters a primary.
- **A change to a rule is a deviation:** outcome, regressor, sample, controls, sign, segments, a tercile, knot or
  threshold. It is recorded in `STATE.md`.
  - For a P-L test whose **confirm half passes the frozen testability rule**, its primary then falls back to the
    confirm half (the European rule).
  - For a test whose confirm half fails it (**LR-K2**, 4 confirm countries at L2), the **frozen
    specification stays the primary** whatever deviation occurs, and the deviated version is reported as
    exploratory beside it. A deviation can never make LR-K2 "not testable" or "uninformative".
- **Frozen code:**
  - a check asserts that the files of `participation/code` have the SHA-256 they had at `participation-E-freeze`;
  - `confirm.py` refuses to run unless `participation/longrun/code` is unchanged since the LE-freeze.
- **After the look:** a bug is fixed in a new commit, and the original and fixed results are reported together with
  the diff. No refetch after the look, except under this policy.
- **Debugging** before the look runs on a blinded panel, with q paths permuted across countries by a hidden seed
  (`specs.blind`).

## 9. Timeline and tags (local, like the existing ones; pushing is her call)

- **L0.** This protocol.
- **L1.** Blind coverage scouting: `longrun/docs/data_inventory.md`, done.
- **L2.** Coverage decisions, by code, from metadata and values-dropping masks only (section 3):
  - per-year availability probes for every OECD key (`Y30T34` included); values-dropping masks for JST and
    ILOSTAT, committed and logged;
  - `coverage_l2.csv`: which countries enter each test, the eligible-year lists and counts, each country's chosen
    q segment, the family sizes;
  - the frozen IPUMS-I sample list, with each sample's RELATE codes, household concept, GQ coding, household
    organisation, age coding and flags; the loader's variable whitelist checked against the extract builder;
  - `segments.csv`, from documentation, including the R6 Table 3 footnotes and the `DEU_F` citation;
  - Kholodilin's file, country list, codes and first-generation definition; Giuliano-Nunn's codes;
  - `split.json`, from the 1960 population;
  - `seen.json`, and the scouts' folders moved (section 7);
  - the gitignore entries for `longrun/data/ipums/` and `longrun/data/raw/`.
- **L3.** Before the tag:
  - `longrun/code` built and checked on synthetic data (the basis invariance check and the RI check included);
  - `longrun/code/specs.py` committed and hashed, then the European real-data run of LR-K2 and LR-Y0, once;
  - the skeleton simulation (calibration, MDEs, the European benchmarks, each country's share of DiD's identifying
    variation);
  - the forecast sheets filled;
  - her Extract B decision recorded (`data/decisions.json`);
  - `checks/check_freeze_ready.py` passes (every L2/L3 item above, the IPUMS records and the scouts' move
    included); the value doors also refuse a tag whose commit lacks the production skeleton, the filled sheets, the
    European run, the segment table or the scouts' move, and any working copy whose frozen inputs differ from it.

  **Tag `participation-L-freeze`.**
- **L4.** After the tag:
  - the US deep study, run once and committed;
  - she makes the IPUMS extract(s), exactly the frozen sample IDs;
  - the explore half is opened (q first, knots hashed, F_L, then outcomes) and is free inside the unseen cells;
  - at most three E-L, with their forecast rows added to `FORECASTS.md`.

  **Tag `participation-LE-freeze`.**
- **L5.** `longrun/code/confirm.py`, once, on one vintage (q first, confirm knots hashed, F_L and H, then outcomes).
  The result is committed immediately.
- **L6.** Free exploratory use. New hypotheses go only to the 2026-2028 time holdout, or to OECD members never
  fetched.

## 10. What this protocol takes from the reviews, and where it departs

**Adopted:**
- unseen cells only, for P-L and E-L alike;
- the matched-pair country split, with the US forced into the explore half and at most three E-L;
- P-L primary on all unseen country-years;
- "a splice is a fixed effect", "extend, don't fill" and only measured observations;
- the cycle from one source per country;
- rent-control robustness from a published coding only, now also as a qualifier;
- the frozen leave-one-out qualifier;
- co-primary randomisation inference where the tested variation is country-level;
- skeleton MDEs and size calibration before the look, with the reading table;
- the forecast sheets;
- the floor-group-trend and cohort-size qualifiers;
- the series-permutation placebo, for LR-K2 (as a qualifier) and D2-L.

**Departures, each for a stated reason:**
1. **Annual panel, not a five-year grid, as the primary.** LR-K2's tercile slopes are identified from
   within-segment annual variation in q. A grid would leave about four points per tercile per country. With
   participation from one OECD flow, there are no census-year points to align. Serial correlation is handled by
   clustering by country, and its effect on size by the skeleton calibration.
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
8. **Floor-group time effects are a qualifier, not part of the primary.** The critic makes "F × decade effects
   included" a condition of LR-K2's sign. Within-country q terciles track calendar time, so group-specific time
   effects in the primary would absorb much of the variation that identifies the group-specific tercile slopes,
   leaving the test to a handful of countries' cross-sectional q differences within a year. They enter as the "rests
   on floor-group trends" qualifier, with H × year rather than H × decade effects (decade effects miss curvature
   within a decade), and section 2 states that the primary sign is conditional on no floor-group-specific trends.
9. **No employee-to-population secondary and no agricultural-share split.** The critic's secondary outcome (the
   employee ratio) and the design review's no-verdict agricultural-share split are dropped: no single source
   publishes employees by five-year age, or the agricultural share, over these countries and years, and a second
   source would be a splice by construction. Section 2 discloses that the activity rate partly measures exit where
   unpaid family work is large.
10. **The pointer (MOMLOC/POPLOC) robustness run is dropped.** Seven of the ten LR-K2 floor samples are not organised
    into households and have no pointers, so the run would have three countries. MOMLOC and POPLOC stay in the
    extract (her variable list) for the descriptive pointer check.
11. **Ten robustness runs, not eight.** The first draft's table held nine runs (men and women on one row). The
    reviews added three that answer specific threats (F_L timing, flagged samples, post-freeze segments) and removed
    two (the pointer run; "without the US", which is the leave-one-out run's US row). The list is enumerated and
    frozen.
12. **Size calibration for every test, not only above 0.075, and MDEs at one ρ.** The design review corrected only
    sizes above 0.075 and took MDEs at the larger of two ρ's; the calibrated p (section 5) closes the 0.05-0.075 band
    and covers both directions, and one ρ on both sides keeps the reading table from tilting toward "uninformative".
13. **Values-dropping coverage masks for JST and ILOSTAT before the freeze.** Neither publishes values-free
    availability. The masks pass values through memory and discard them at parse; nothing is printed or written.
    OECD coverage uses per-year availability probes, which carry no values; its observation flags are not pulled
    before the freeze and act only as missing cells afterwards.

## 11. Review record (first draft, 2026-10-08; revised 2026-10-09)

Three reviewers read the first draft (`longrun/docs/protocol_review_draft1.md` holds the first two in full): T =
theory, D = design, A = data feasibility. "Adopted" means the fix as proposed, or an equivalent named here.

| # | Severity | Finding (short) | Disposition |
|---|---|---|---|
| T1 | major | DiD not scale-free; attenuation also gives DiD < 0 | Adopted: attenuation/insurance foil in s.2; foil line corrected; scale-free companion (no verdict); model-level reading conditional on the drop condition |
| T2 | major | "slope_top ≤ 0" overstates the paper (mixture of types) | Adopted: prediction restated (falls; below low-F top; ≤ 0 only if floor-types dominate or jobs need own dwelling); refutation quoted as a conjunction |
| T3 | major | Contradicted DiD consistent with model under regime auxiliaries | Adopted: two-sided regime claim with auxiliaries 1-3; countries named; 75-year rationale disclosed as not carrying; "contradicted" label names the auxiliaries |
| T4 | major | Terciles rank q across unlinked segments | Adopted (with D1): terciles and knots within one chosen q segment; other segments dropped from LR-K2, LR-Y0, U-K2 |
| T5 | major | Control-era bottom terciles create DiD < 0 mechanically | Adopted: "rests on control-era years" qualifier; first-generation only, with the reason; not made the primary |
| T6 | major | F × decade effects demoted without saying so | Adopted as departure 8, with H × year (D2); conditionality stated in s.2 |
| T7 | minor | Ranking set used outcome availability | Adopted: ranking set from q alone within the chosen segment; outcome-missing years drop without moving knots |
| T8 | minor | Kaplan/Ermisch wording overstated | Adopted: "same DiD sign, turning point at a different q"; D1-L/D2-L equally non-distinctive |
| T9 | minor | LR-C1 dropped the ownership condition; pre-1976 censuses | Adopted: condition restored in the reading; LR-C1 = censuses from 1976 only |
| T10 | minor | LR-Y0 null read "no support" in control era | Adopted: reading note via the strict-control-dropped run |
| T11 | minor | Unpaid family workers; employee ratio and agricultural split dropped silently | Adopted: s.2 sentence; departure 9 |
| T12 | minor | F_L not predetermined for 1970-71 censuses | Adopted: disclosed in s.2; robustness run "F_L nearest 1970, later years only" (merged with D12) |
| T13 | minor | Primary pools early women; men-only only in a footnote | Adopted: s.2 sentence; men-only reported beside the primary |
| D1 | blocker | Kinked basis breaks "a splice is a fixed effect" | Adopted (longest-segment rule, as T4); invariance check added |
| D2 | blocker | Terciles ≈ calendar time; no curvature guard on LR-K2 | Adopted: "indistinguishable from time curvature" (time terciles and series-permutation placebo); floor-group trends via H × year; men-only beside primary |
| D3 | major | segments.csv open after values are seen | Adopted, stricter: post-freeze breaks never enter a primary; one complete blind re-read defines a no-verdict run |
| D4 | major | Confirm-half fallback is an escape hatch for LR-K2 | Adopted: frozen spec stays primary where the confirm half fails testability |
| D5 | major | Rival's DiD unsigned across groups; DiD < 0 from low-F convexity | Adopted: foil corrected; the drop condition decides between "favours" and "consistent with the floor or attenuation (carried by low-floor convexity)" |
| D6 | major | MDE reading table steerable | Adopted: synthetic-q DGP fixed; one ρ on both sides; benchmarks by the same simulation; standardised MDE; code and seed committed |
| D7 | major | European benchmark run is a forking path | Adopted: specs committed and hashed first; run once; amendments recorded and all runs reported |
| D8 | major | Flags and coverage can shift membership after values | Adopted: membership, eligible years and knots frozen; flagged cells become missing; H computed once and held; values-dropping masks for JST/ILOSTAT |
| D9 | major | IPUMS sample set fixed on extract day | Adopted: sample IDs frozen at L2 with RELATE schemes; later releases ignored |
| D10 | major | Weighting ambiguous; US dominates | Adopted, second option: unit weights stated; identifying-variation shares published before the look; "rests on the US, a partly seen country" |
| D11 | major | E-L not restricted to unseen cells; E-L could rescue LR-K2 | Adopted: s.1 |
| D12 | minor | F_L timing, DE territory | Adopted: `DEU_F` for DE 1970-1996 (with A6); "F_L nearest 1970, later years only" run |
| D13 | minor | Combined RELATE codes inflate F_L where H is set | Adopted (with A2): codes listed per sample at L2; flags; combined-code shares reported; flagged-dropped run |
| D14 | minor | Qualifier mechanics unspecified | Adopted: max p (calibrated); collinear H × year dropped; H fixed in LOO; "not estimable" rule; exact RI check with tolerance |
| D15 | minor | Size correction ambiguous | Adopted: calibrated max p in both directions, Holm on calibrated p's (departure 12) |
| D16 | minor | Knots at the look and in the time holdout | Adopted: explore knots from the explore opening; confirm knots at the look; frozen for the time holdout; row-level guards |
| D17 | minor | WPP is modelled, against L3 | Adopted: stated exception in L3 |
| D18 | minor | Which censuses enter LR-C1 | Adopted: Extract B censuses from 1976 only; F_L samples excluded |
| D19 | minor | Robustness table held nine runs | Adopted: ten runs, one per row (departure 11) |
| D20 | minor | Scouts' value files readable by agents | Adopted: hashed, listed and moved before the freeze; deletion her call |
| D21 | minor | Qualifiers asymmetric; LR-C1 contradicted beside supported LR-K2 | Adopted: qualifiers never change labels; LR-C1 reported in the model-level sentence |
| A1 | major | Seven floor samples are person-level; pointer run has 3 countries; GQ uneven | Adopted: person-level samples admissible; pointer run dropped (option b; departure 10); per-sample GQ rule; IL kibbutz members excluded as coded |
| A2 | major | "Child" differs by sample, correlated with the split | Adopted in part: per-sample records, flags and a flagged-dropped run. Not adopted: replacing CO 1964 by CO 1973 in the primary (her "earliest census"; see open questions) |
| A3 | major | Range queries hide gaps; Y30T34 unchecked | Adopted: per-year probes for every key, Y30T34 included. Not adopted: a values-dropping OBS_STATUS pull for OECD (flags act after the freeze as missing cells only) |
| A4 | minor | "Longest run" not tied to the unseen window | Adopted: longest run overlapping the window, counted inside it, ties to the later |
| A5 | minor | CPI ends early for CR, MX, CL | Adopted: generalised C2018 extension; uncovered countries listed |
| A6 | minor | DEU vs DEU_F | Adopted: `DEU_F` for all DE observation years, cited in segments.csv |
| A7 | minor | `housing_capgain_ipol`; R6 Table 3 footnotes | Adopted: L3 |
| A8 | minor | US series codes, NSA cycle, AD-3/AD-1 seam | Adopted: `DTENRG-A`/`DGDSRG-A`; `LNU04000060`; seam by rule |
| A9 | minor | Loader whitelist names wrong | Adopted in part: names confirmed at L2 against the extract builder. AGE2 and PARRULE are not added to the requested variables (her list; AGE midpoints suffice, pointer run dropped) |
| A10 | minor | Kholodilin availability and coverage unknown | Adopted in part: confirmed at L2; own definition verbatim. Not adopted: dropping the run for LR-K2 if high-F countries are absent (the bias it checks sits in the low-F group) |
| A11 | minor | Extract B: ACS samples and coding | Adopted: census samples only, ACS excluded; same RELATE rules |
| A12 | minor | C-6L coverage unverified | Adopted: values-dropping pull at L2, logged and hashed |
| A13 | minor | Coverage counts and thin margins | Adopted: counts published in coverage_l2.csv; "passes by 2"; the unusable-sample rule (L9) |

### Code review of 2026-10-09 (the pipeline, before the freeze)

Three reviewers (fidelity, blinding, statistics) read `longrun/code`, `longrun/checks` and `longrun/data` against this
protocol. Their findings were fixed in the code and checks; where the code needed a reading the text did not give,
the reading was settled here. Settled readings (each marked "settled 2026-10-09" where it sits):
- **L1's European cut is 1994, not 1996** (q to 1993). The first draft took 1995-1996 as unseen; the European panel
  grid starts in 1995 and its exploration's outputs hold 1995-1996 activity rows. The cut is applied to all 26
  European members (the confirm countries' 1995-1996 rows were built into the European look's panel too). At L2 this
  takes NL out of LR-K2 (8 eligible years) and AT and IS out of the split; the split was redrawn by its frozen rule.
  Her confirmation is asked for: cutting only the European explore countries would keep NL (LR-K2 at 10).
- **q by the frozen ladder** (L6): a flagged or missing value is missing inside its run, never a reason to rebuild
  the ladder from values.
- **H in the robustness rows** (L9): the three rows that define another F split it by the rule; all others hold H.
- **LR-Y0's reading note** uses LR-Y0's pre-look standardised MDE (no pre-look MDE exists for a run whose dropped
  years are control values).
- **Frozen families**: an erroring member takes p = 1 inside its family.
- **The RI's missing value**: a co-primary that cannot be computed makes the verdict statistic missing (p = 1), never
  the WCR p alone.
- **The US wording** (L13) is added whenever the US row alone crosses 0.10, and every country's leave-one-out row is
  reported.
- **Extracts A and B** may be one extract or two; a grouped-age sample without its interval record is unusable alone;
  Mexico 2015 is a survey; each sample's kind is an L2 record.
- **Reported, no verdict role** (section 5): LR-K2's size at the expected split and under stress nulls; the MDE is
  labelled the SD-based t-formula figure, with the procedure's power beside it.

Left to her before the freeze (listed by `checks/check_freeze_ready.py`): where the IPUMS file found in `data/` goes;
the European cut (all 26 members, or the explore countries only); whether the stress nulls or a realised-H
calibration enter the verdict's calibration; whether the model-level sentence names LR-K2's identifying-variation
shares and the leave-Latin-America-out run; the L2 records (IPUMS age intervals, RELATE codes, household concept, GQ
coding, sample kinds; Kholodilin's file; the school and coresidence segment rows; the JST and ILOSTAT masks); the
scouts' folders; the European raw cache; her Extract B decision; the forecast sheets.
