# Long-run derivations — what the model predicts for 1950-1996 (theory critic, 2026-10-08, no data)

## LR-K1

The floor kink is regime-dependent, and the protocol's D1 sign (b2 < 0) is the model's prediction in only one of four q regimes. Take a youth population with a floor-available share (a parental room supplied below its rent) and a no-floor share. As q = r/p rises, the q x F interaction runs 0 -> + -> - -> +. (i) Both groups live independently in work and exit (q below the work-side switch q_WP): slopes are identical, b2 = 0. (ii) Floor-types already work from home but their exit is still priced (q_WP < q < q_enc^F): their slope h/(s0-qh) exceeds the no-floor slope h(w-s0)/((w-qh)(s0-qh)), so b2 > 0. (iii) Floor-types are past q_enc^F = (s0 - s_u e^-theta)/h and no-floor types are not: b2 < 0, the D1 window. (iv) Both groups are at a floor (no-floor types at a state or tolerated-use floor): b2 > 0 again, because floor-types are at 0 while independent workers lose -h/(w-qh). Verified with sympy and a numeric population (lr_derive/floor_regimes.py, floor_regimes_v2.py). For 1950-1996, most country-years plausibly sit in (i)-(ii): post-war rent control, low q, falling age at leaving home in the North and West. So the model predicts b2 >= 0 for the early decades and b2 < 0 only after a country's q crosses q_enc^F (plausibly the 1980s-90s in the South, the late 1980s in JP). A pooled 1950-1996 D1 averages opposite-signed regimes and is UNSIGNED by the model.

- **Measure:** 25-34 (also 20-29) activity rate, sexes separately and equal-weighted; country and year FE; log q_{t-1} x F_c estimated separately by pre-registered regime (early vs late period, or within-country q tercile), not pooled.
- **Sign:** b2 >= 0 in the low-q/rent-controlled regime; b2 < 0 only in the window between the floor-types' and the no-floor types' enclosure points; pooled 1950-1996: unsigned
- **Against standard models:** Only the sign SWITCH (from >= 0 to < 0 as q rises within high-F countries) is distinctive, and only against an income-effect model with no below-market coresidence option. A standard model with an endogenous coresidence choice, where parents supply the room below market (Ermisch; Kaplan 2012), produces the identical sign path, shifted in location: the numeric 'std' column, where exit at home = log(s0 - tau), is flat in q. Against life-cycle models with coresidence, the kink is NOT distinctive.
- **Assumptions:** Log or concave utility with s0 < w (or, in the linear reduced form, h_e > h_w); the parental room is supplied below market rent (outright-owner parents); F is time-invariant in rank; the no-floor types' floor is not rent-indexed (no out-of-work housing allowance); the regime of each country-period is fixed by a rule stated before outcome data are seen.
- **What a contrary result refutes:** A b2 < 0 in the low-q decades and a b2 >= 0 in the high-q decades (the reverse switch) would count against the floor mechanism's regime structure. A pooled-sample b2 of either sign refutes nothing, because the model does not sign it.

## LR-K2

The one long-run result with bite: within high-floor countries, the young's participation slope on q is <= 0 in the high-q part of each country's own 1950-2025 history and falls relative to the low-q part. Within low-floor countries the slope stays positive and rising (convex) over the same range. The model's within-country participation(q) curve for floor-types is convex-rising, then kinks to flat (work from home possible) or falling (some jobs need one's own flat). A quadratic in (log q - m_c), as in D2, is unsigned over the long range, because the convex pre-enclosure segment gives a positive square. It must be replaced by a piecewise slope.

- **Measure:** 25-34 activity rate on log q_{t-1}, slopes by within-country q tercile (terciles of the regressor fixed before outcomes are fetched), interacted with predetermined F; difference-in-differences [slope_top - slope_bottom]_highF - [slope_top - slope_bottom]_lowF.
- **Sign:** slope_top(high F) <= 0; DiD < 0
- **Against standard models:** Distinctive against the no-coresidence income-effect account, which predicts a convex, rising response everywhere, so DiD ~ 0 and slope_top > 0. NOT distinctive against life-cycle models with a below-market parental option (same shape). This is the best use of a 75-year window: within one country q crosses q_enc, which 2009-2025 (17 years, D2 close to a quadratic trend, IE carrying 61%) could not show.
- **Assumptions:** The q measure tracks the marginal (market) rent in the years used, which fails under rent control (LR-RC). The parents' generation owns outright, so host capacity does not shrink with q (the paper's own caveat that 'the host's capacity to share inherits the host's rent bill'). F is predetermined (historical family-ties classification or the earliest census coresidence, not 2003-08 coresidence). No F-specific trends in schooling, conscription or women's entry, or F x decade effects included.
- **What a contrary result refutes:** A significantly positive slope_top at high F where parents own outright, no smaller than at low F, together with no drop from the low-q to the high-q tercile, refutes the claim that the flat floor (s = s_u) is the operative margin for the young. That is the floor mechanism itself, given clean q and F. A null at high F refutes nothing (work-from-home compatibility gives exactly 0).

## LR-Y0

For the young in 1950-1996, where independent exit was still priced and affordable (q < q_enc), the model signs the participation response to rents relative to goods POSITIVE and convex. In the log case d(W-E)/dq = h(w - s0)/((w - qh)(s0 - qh)) > 0 iff s0 < w, and it rises in q. In the paper's linear reduced form the slope is h_e - h_w, positive only if exit is more housing-intensive than work (the historical plot exit, doubtful for urban youth).

- **Measure:** 20-24 and 25-34 activity rate on log(rent CPI / goods CPI)_{t-1}, country and year FE, by sex, early decades (or the bottom within-country q tercile).
- **Sign:** + (growing with q); about 0 for young men near saturation outside school and military service
- **Against standard models:** Not distinctive: the same sign and convexity as the standard income-effect, life-cycle and net-short-renter account.
- **Assumptions:** s0 < w (log case) or h_e > h_w (linear case); the goods wage is held fixed or the cycle controlled; q measured at the margin; young men's participation density at the margin is thin.
- **What a contrary result refutes:** A negative slope in clearly pre-enclosure, decontrolled settings refutes the enclosure channel (Prop. exit (iii)) for the young, or the s0 < w / h_e > h_w auxiliary. It does not refute the floor kink.

## LR-RC

Under post-war rent control the CPI rent component prices sitting tenants, so measured q is not the marginal price of independent exit. d log CPI_rent / d log r_market = (1 - phi) r_m / (phi r_c + (1 - phi) r_m) < 1 (attenuation; sympy). Where controlled units are rationed, young outsiders cannot buy independent exit at any measured q: they are de facto at the floor (queue, parental home, marriage), so their response to CPI-q is about 0 whatever the model's regime. Decontrol raises CPI-q while the market rent facing entrants may fall. Around decontrol the model predicts no youth response to the measured jump, and possibly a negative one, as independent living becomes available. For older sitting tenants, decontrol is an enclosure of a cheap exit: their participation rises (an income effect with the same sign as the standard account).

- **Measure:** Youth and 55-64 activity on CPI-q, split by a pre-registered rent-regulation indicator (decontrol dates from legal histories, e.g. US federal controls ended early 1950s, DE phased 1960-71, ES 1985, UK 1988; coded before outcomes are seen); decontrol event study.
- **Sign:** Youth: about 0 (attenuated) in controlled years, + only in market years; older renters: + at decontrol
- **Against standard models:** Not distinctive in sign; it is a measurement prediction that governs which years can test LR-K1/K2.
- **Assumptions:** Rent control binds on the CPI sample (sitting tenants); rationing rather than price clears entry; decontrol dates are exogenous to youth labour demand.
- **What a contrary result refutes:** Nothing in the mechanism. A youth q-response in controlled years that matches the market years refutes only the measurement claim (that the CPI rent was not the marginal price).

## LR-F1

The relevant floor changes by era, so a single parental-coresidence F mismeasures the floor before about 1975. For young women in 1950-1975 the dominant exit was the pooled marital household: the paper's 'household as pooled exit'. There the second earner's exit is housed by the household, the substitution term h_e - h_w is switched off, and dI/dq = w2(h - l)/((A + w1)(A + w1 + w2)) (sympy): the household's net housing position. So young women's q-response in 1950-1975 is + in renter-couple countries, about 0 or - where couples own, and does not depend on parental F. The parental-floor kink applies to young women only after marriage was delayed (from the 1970s-80s), and to young men throughout.

- **Measure:** 25-34 women's activity on log q_{t-1}, interacted with the pre-period renter share of couples (census tenure), early versus late decades; separately single versus married women where census or LFS marital status exists.
- **Sign:** Early decades: sign of household net position (+ renters, <= 0 owners); single women's slope > married women's slope (among renters)
- **Against standard models:** Not distinctive: this is the unitary household income effect and net-position hedging (Blundell-MaCurdy; Sinai-Souleles). The only model-specific element is the era sequencing of floors (land commons -> marital household -> parental home -> public provision), which is interpretive.
- **Assumptions:** Pooled (unitary) budget; mortgagors are hedged against rent flows; marriage is the operative floor for 1950-75 young women; marital status measured consistently.
- **What a contrary result refutes:** A failure refutes the App B income-effect auxiliary and the household-pooling assumption, not the floor kink. It does say that the D1 test, pooled over sexes, is mis-specified for the early decades.

## LR-W1

Women 25-54, 1950-1996: participation rises. The model's channels are (a) the post-industrial schedule opening clerical and service tasks, with the wage drawn above s for second earners; (b) the household net position, where renting couples respond + to q and owner couples respond about 0; (c) the erosion of the pooled-household floor (later marriage, divorce), which moves women onto a priced independent exit whose slope is +. In agrarian economies (IT, ES, PT, EL, IE, FI, JP, KR in 1950-70) the measured activity rate of married women can FALL. Unpaid family farm work is the land-access exit in the paper's terms but is counted as participation, while the dependent-employment rate rises: the falling arm of Goldin's U.

- **Measure:** Women's 25-54 activity rate and, separately, the employee-to-population ratio, against the agricultural (self-employed and family-worker) share and log q.
- **Sign:** Activity: + trend, possibly - early where agriculture large; employees/pop: + with agricultural decline; q-slope + only among renters and singles
- **Against standard models:** Not distinctive: Goldin's U, Lewis (whom the paper cites as its ancestor), the unitary household and task-based accounts give the same signs. These are also postdictions, since the broad facts are known to everyone involved, so they are not blind tests.
- **Assumptions:** Family workers counted as active (ILO convention); the sex-to-task-location mapping; women's and men's exit values move together otherwise.
- **What a contrary result refutes:** Only the mapping of sex to task location and the measurement convention; no model primitive is involved.

## LR-O1

Men 55-64 (and 60-64), 1970-1995: participation falls. Model channels: (a) exit-conditioned early-retirement, disability and unemployment-to-pension routes make Delta = m_w - m_e < 0 (conditionality appendix); (b) routine industrial tasks become machine-contestable, so older routine workers' wages fall toward s; (c) outright owners are net long, so a rising q raises A and buys exit, while older renters are net short and pushed toward work. Women 55-64: rising cohort entry offsets this, so a smaller fall or a rise.

- **Measure:** 55-64 and 60-64 activity by sex; interaction of log q with the 55-64 outright-owner share (census tenure, pre-period).
- **Sign:** Men -; q x outright-owner share < 0
- **Against standard models:** Not distinctive: Gruber-Wise implicit tax, Juhn-Murphy-Topel low-wage withdrawal, and life-cycle housing wealth effects (Disney-Gathergood) give the same signs.
- **Assumptions:** Pension and disability routes measured or controlled; owners can realise housing gains; health and cohort mix fixed.
- **What a contrary result refutes:** A contrary sign refutes the shared participation step or the group-to-position mapping, not the floor.

## LR-O2

Pension indexation x q (weakly distinctive). If the goods wage is pinned to rent at an active margin (w = v q, v = w/r fixed by technology), then for a group whose non-labour income a is fixed in goods (price-indexed pensions) dI/dq = a v/(A(A + v q)) > 0. Where pensions are wage-indexed (a proportional to q), dI/dq = 0 (sympy, pension_index.py). The model therefore predicts that older participation responds more positively to q under price indexation than under wage indexation. The 1980s-90s switches from earnings to price indexation give within-country variation.

- **Measure:** 60-64 and 65-69 activity on log q_{t-1} x price-indexation indicator (legal histories coded before outcome data), country and year FE.
- **Sign:** interaction > 0
- **Against standard models:** Distinctive to the technology-pinned w/r, which no life-cycle or retirement-incentive account contains. The weak link is that the paper's own fork (the wage deflated by shelter fell) shows w/r is not fixed, so pass-through epsilon < 1 dilutes it.
- **Assumptions:** Pass-through of r into goods wages at an active contestable margin; the indexation switch is exogenous to older labour demand; pension levels otherwise controlled.
- **What a contrary result refutes:** A null or negative interaction refutes the pass-through closure's relevance for participation (an auxiliary link from c(r) to w), not the floor mechanism.

## LR-S1

Schooling, 1960-1996: enrolment at 20-24 rises when prime-age unemployment rises (the oil shocks, the early-1980s and early-1990s recessions, the FI/SE 1991-93 crisis): school as a paid exit whose relative value rises when entrant wages fall. Student grants and subsidised student housing (1960s-70s expansions) act as m_e restricted to school, lowering 15-24 participation. Model-specific variant: where students live independently at market rent, enrolment falls with q; where they live with parents, it does not.

- **Measure:** 20-24 (and 15-19) enrolment or inactive-in-education share on lagged U(25-54); secondary: log q x pre-period independent-student share.
- **Sign:** U-slope +; q x independent-student share -
- **Against standard models:** The cyclical sign is not distinctive (Betts-McFarland; Dellas-Sakellaris). It replicates C-6/E-SCH1, which 2009-2025 supported but which rested on 2008-13. The q x student-housing interaction is weakly distinctive.
- **Assumptions:** Prime-age unemployment proxies entrant prospects; enrolment measured consistently (apprenticeships, conscription); grants not rent-indexed.
- **What a contrary result refutes:** A null cyclical slope refutes only the imported opportunity-cost auxiliary. A positive q-slope among independent students refutes the extension of eq. (exit) to schooling.

## LR-C1

Over the long run, the share of 25-34 (or 20-29) living with parents rises with q where parents own outright and less, or not at all, where the parent generation rents. This happens on both margins (the work-side switch at q_WP, which depends on q h/w, and the exit-side switch at q_enc). The paper says the mechanism 'is visible in ... household formation, and coresidence'. Over 1950-1975 coresidence should FALL where q was low or controlled and marriage was early, then rise once q crosses the thresholds.

- **Measure:** Census and IPUMS-type coresidence of 25-29/25-34 on log q (or rent over the all-age wage, never over the youth wage), with the pre-period outright-owner share of 50-64 as moderator.
- **Sign:** + overall; larger where parents own outright
- **Against standard models:** Not distinctive: Ermisch and Kaplan-type household-formation models give the same. It is a consistency check that the parental floor is the operative modern floor. C-1 was inconclusive (-3.38) on 2009-2025.
- **Assumptions:** Parental room supplied below market; jobs reachable from home; q measured at market; no reverse feedback from coresidence to rents.
- **What a contrary result refutes:** A long-run null or negative slope where parents own outright, with clean q, refutes the paper's mapping of the modern dependency floor to the parental home. That is an auxiliary in the derivations' terms, but the floor mechanism has no empirical carrier without it.

## LR-M1

Men 25-54, 1950-1996: near-saturated with a mild decline from the 1970s, concentrated among the low-wage. In the post-industrial configuration the routine stretch becomes contestable, entrant and low-skill wages are priced by machines and fall toward s, and those at a flat floor (partner's household, parents, disability) exit. Rising q pushes single renting men toward work (+), which partly offsets this.

- **Measure:** Men 25-54 activity rate by education or marital status where available.
- **Sign:** - (small), with q-slope + for single renters
- **Against standard models:** Not distinctive (Juhn 1992; Juhn-Murphy-Topel; Autor-Dorn).
- **Assumptions:** Wages at the bottom fall toward exit values; floor availability is unchanged.
- **What a contrary result refutes:** The mapping only.

## Era notes and adversarial headlines

I looked at no data. The algebra is verified in C:\Users\s6068C\AppData\Local\Temp\claude\C--Users-s6068C-GitHub-laborformal\57a37d3a-ed63-4c7d-9808-2133339ff86c\scratchpad\lr_derive\ (floor_regimes.py, floor_regimes_v2.py, pension_index.py).

ADVERSARIAL HEADLINES

(1) Going back to 1950 mostly adds years in which the model and the standard account agree. Real rents relative to goods rose over the period, which is the paper's own fork, so earlier years sit at lower q: below q_enc, often under rent control. There the model's youth slope is positive and convex, h(w - s0)/((w - qh)(s0 - qh)), exactly the income-effect account's. The discriminating information sits only in the transition years in which a country's q crosses the floor-types' enclosure point: plausibly 1975-1996 in the South and JP/KR, and decontrol episodes. A long window helps D2 (75 years of non-quadratic q paths instead of 17 years close to a quadratic trend), but the early decades add almost no power against the standard account.

(2) D1's sign is the model's prediction in only one of four regimes. With floor-available and floor-less youth, the q x F interaction runs 0 -> + -> - -> + as q rises: + while floor-types work from home but their exit is still priced, - in the window between the two groups' enclosure points, + again once both are at floors. Numerically (v2): b2 = 0 up to q 0.26, +0.07 to +0.53 for q 0.29-0.41, -2.5 for q 0.44-0.47, +0.41 to +0.52 above 0.50. So a pooled 1950-1996 D1 is unsigned by the model, and its early decades are predicted b2 >= 0. Regimes must be fixed ex ante by a rule on the regressor or on legal dates, never on outcomes.

(3) The kink is not distinctive against life-cycle models with a coresidence choice. A 'standard' model in which the parental room is available at a below-market cost tau in both work and exit (exit at home = log(s0 - tau), flat in q) gives the identical sign path, only shifted (its enclosure point is 0.17-0.23 against the paper's 0.34-0.41). The asymmetry 'host pays in exit, self pays in work' arises endogenously from any below-market parental option. The protocol's foil ('standard account: b2 >= 0') holds only for an income-effect model with no coresidence option. A symmetric family-insurance model that attenuates the slope also gives b2 <= 0. The discriminating quantity against the no-coresidence model is the SIGN of the slope at high F in the high-q range (<= 0), not b2. Against Kaplan/Ermisch-type models nothing in D1/D2 discriminates; at most the q = r/p (goods-deflated, flow rent) specification and the host-tenure moderation have weak edge.

(4) Answer to Q2. D1/D2 is testable on 1950-1996 with a time-invariant F only under: (a) rank stability of host capacity across 75 years; (b) predeterminedness. 2003-08 coresidence is itself an outcome of the 1980-2003 q path (C-1's mechanism), so with a regime-dependent model it proxies 'already crossed by 2003' and mechanically mixes D1 with D2's curvature; prefer a pre-1950 family-ties classification (Reher-type) or the earliest census coresidence. (c) A pre-registered regime per country-period. (d) The right floor for the group: for young women before about 1975 the floor was the marital household, so parental F is the wrong moderator and the early test should run on men, or on women only from the 1980s. (e) q at the margin: CPI rent prices sitting tenants, with elasticity to market rent (1 - phi) r_m / CPI < 1, and rationing makes outsiders de facto floor-bound. Restrict to decontrolled years and markets, or code control regimes from legal histories before fetching outcomes. (f) No F-specific trends in schooling, conscription and women's entry; add F x decade effects. (g) No rent-indexed out-of-work housing allowance for the low-F young (Nordic, UK, NL, DE allowances from the 1970s put low-F countries in regime (iv) and flip b2 positive). The model's sign for the young's q-response in that era: + where independent exit was priced and affordable (q < q_enc; log case needs s0 < w, linear case needs h_e > h_w). It is about 0 against CPI-q where controls bound and units were rationed, and about 0 for young men near saturation. In none of these cases is it distinctive.

(5) Answer to Q3. Against the floor mechanism: with market-measured q, predetermined F, and the parents' generation owning outright (so the paper's own 'host's capacity inherits the host's rent bill' escape is closed), the high-F young's participation slope in the high-q part of their own history is significantly positive, no smaller than in low-F countries, and does not drop from the low-q to the high-q range (LR-K2). Also against it, as an empirical carrier: a long-run null or negative coresidence-on-q slope where parents own outright (LR-C1). Against auxiliaries only: no positive slope in the pre-enclosure decades (enclosure for the young, s0 < w or h_e > h_w, or rent-control measurement); a pooled-period D1 of either sign (unsigned); results that hold with 2003-08 F but not with historical F (rank instability or endogeneity); effects carried by the goods leg rather than the rent leg (the q measure; test homogeneity, rent and goods coefficients equal and opposite); breaks from unpaid family workers, conscription or the 1983/1992 LFS definitions; women's and older-age nulls (income-effect, pooling and pension proxies). Note that the 2009-2025 leanings (D2 p_opposite 0.064; confirm-half rent x F +9.1) are absorbable by the model only by declaring 2009-2025 Europe to be in regime (ii) or (iv). Regime (ii) contradicts the paper's own text that the modern floor is 'often a parent's spare room' at historically high Southern coresidence. Regime (iv) needs rent-indexed state floors in the low-F countries. Write that claim down before the backward data are seen, or the long run becomes an excuse rather than a test.

(6) Blindness. The backward holdout is clean only for the specific interactions nobody has computed. The era facts (women's entry, early retirement in the 1970s-80s, Southern late home-leaving from the 1980s, Japan's 1990s coresiding singles, US prime-age male decline) are known to everyone involved, so LR-W1, LR-O1 and LR-M1 are postdictions, not tests. Non-European OECD members (US, CA, AU, NZ: low F, mostly decontrolled after the early 1950s; JP, KR: high F, tenant-protective law, jeonse in KR) give G of about 6-8. Expect large MDEs and binding leave-one-out qualifiers, and state the MDE before the look.

(7) Data caveats to pre-register (no values consulted). Pre-1970 age-sex participation is mostly decennial census or OECD/ILO yearbook data with definitional breaks. Unpaid family workers counted as active make the 1950s activity rate of women and youth in agrarian countries a measure of the land-access exit, not market work. Use the employee-to-population ratio as a secondary outcome mapped to 'selling the market hour'.