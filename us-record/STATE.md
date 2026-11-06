# STATE — us-record (the backward model; resume point for the next session)

**Project:** the paper's model run through the US record, 1950–2025: a test the mechanism could fail, the clocks
measured, an attribution, and a 2025 starting point for the forward model in `../paths/`. The governing document is
`SPEC.md`; read it first.
**Collaboration:** same contract as the sibling threads: drafting and sequencing delegated to Claude, checks gate
absolutely, direct critique over validation; the decisions below are a veto window for her calls. Code in plain
functions, notebook-cell style; `tqdm` on any outer loop that takes more than a few seconds.
**The wall:** this repository is public. Public data only (FRED, BEA, the Fed's Z.1).
**State as of:** 2026-11-05. Phases 0 and 1 done: `SPEC.md` committed before any data; the data panel built
(`code/panel.py` -> `data/panel.csv`, 76 years x 32 columns, `data/manifest.csv` with each source's SHA-256),
gated (`checks/check_panel.py`, 21/21), its mapping written (`docs/measurement.md`) and drawn
(`code/fig_panel.py` -> `figures/fig_panel.png`). Breakpoint A passed (her call: prime-age employment targeted).
Phase 2 done: the base model fitted (`code/fit_base.py` -> `results/fit_base.json`, gated by `checks/check_fit_base.py`
9/9, drawn in `figures/fig_fit_base.png`). Breakpoint B passed. Phase 3 under way: the kept model is the base with the cap, the
basket and the pinned start (misfit 6.8; A dropped, the split and the 1990 utility turn shelved).

## The three models

1. The pinning model, `../pinning/code/pinning_model.py`: the paper's.
2. **This thread**: the backward model, the pinning model against 75 years of US data.
3. The forward model with a crash, in `../paths/`: the complex model (`code/macro.py` and its layers) and the crash
   model (`code/global_crash.py`), today two pieces that do not read each other's results, to be joined. It takes its
   start and its clock from this thread (`SPEC.md` section 9).

## Decisions (veto window)

1. **US first** (her call, 2026-11-05), annual, 1950–2025: the window the effort accounts and the fork cover.
2. **Accuracy through simplicity** (her call, 2026-11-05): the paper's model with as few additions as the record
   forces; anything that does not do much is cut; credibility from few free numbers and untargeted facts rather than
   many holdout sets. One time split reported as a reading only.
3. **Aggregate participation only.** The participation thread's US series by sex and age stay unseen until its
   long-run freeze (`../participation/STATE.md`, "The long run"); women's entry enters as a shift backed out of the
   aggregate rate (addition B), not read from those series.
4. **The earn-its-place rule** (`SPEC.md` section 6): a component stays if removing it raises the misfit by at least 20%
   or takes a targeted series out of its band; set before fitting, revisable once at breakpoint B.
5. **The folder** is `us-record/`, a new thread; `../archive/long-record/` (seven centuries of English wages) is the
   method's precedent, not its base.
6. **The long rate is Moody's Aaa** (Phase 1): the ten-year Treasury starts in April 1953; Aaa covers the window and is
   closer to a firm's cost of funds. The Treasury version is kept beside it.
7. **Expected inflation is the mean log CPI inflation of the five years to t** (Phase 1): simple and complete; it lags
   turning points (`docs/measurement.md`, choice 3).
8. **Complete calendar years only** (the repository's rule): with October 2025 never published, the monthly series end
   in 2024; nothing is filled or extended.
9. **θ_V linked across bases at 1997** (Phase 1): the λ thread's 1967–1992 benchmark points (narrow machinery,
   import-comparable) carried onto calibration (c)'s basis by the 1997 ratio; nothing measured before 1967.
10. **The targeted employment rate is prime-age, 25–54** (her call at breakpoint A, 2026-11-05): the 16+ rate's fall after
    2008 is mostly ageing, which the model does not have; the 16+ rate becomes a check. Adults 16+ still set the
    population's growth.
11. **The base model's required return is constant** (after the first search, 2026-11-05; **for her veto at
    breakpoint B**): with machines carrying about half their cost in labour, the model has a few points of rate
    headroom, and a required return following the measured real long rate (-3% in 1950, +6% in the 1980s) left no
    land-scarce equilibrium in 18 years of a 1950-calibrated start; the measured return on business capital is far
    steadier than bond yields. The measured rate's pass-through becomes candidate addition I (SPEC.md section 6).
    Not vetoed at breakpoint B.
12. **Changes are tried because they make sense on their own, not to fix a misfit** (her call at breakpoint B,
    2026-11-05): "not 'how do we adjust this curve to fit better' but 'what if we tried this change which feels
    intuitive anyways'". Each is tried once, at values set from evidence rather than fitted where possible; it stays if
    it improves the fit (the earn-its-place rule, decision 4), and is shelved if not. Candidates proposed because of a
    specific misfit (C as an answer to the employment overshoot; the clock's frontier form as an answer to labour's share)
    are off the list unless they come back on their own merit.
13. **Claude does not look at a change's fit; she judges it** (her call, 2026-11-05, during A): each change is run with
    its output unread (`code/fit_base.py --quiet`), checked blind (`checks/check_fit_base.py --results NAME --blind`:
    pass or fail, no numbers), drawn against the base model and the data (`code/fig_compare.py NAME`) and sent to her
    unopened; she says better or worse. That verdict replaces the mechanical 20% rule of decision 4. The base fit
    (Log 4) was seen before this, and serves as the reference.

14. **People are split as BLS's wage data split them** (her calls, 2026-11-05: "wage data split, routine work all, gap
    as a check"): the production and nonsupervisory group (about four in five private jobs; its hourly earnings, AHETPI,
    are the wage every wage target reads) and managers and supervisors, each working its own block of tasks against
    machines (`code/split_model.py`). Computing makes machines need exp(-g_c (t - 1970)) of their service at every task
    of the first group's block from 1970 (her "from around 1970"; the year is set, not fitted). The groups' sizes are set
    at the first group's mean share of private jobs, 1964–2024 (0.8185), not fitted; computing's pace g_c is the one new
    free number. The pay gap (all employees' average hourly wage over the first group's) and the group's share of jobs
    are checks, never targeted. With g_c = 0 the split is the one-group model exactly. It extends A (decision kept at
    Log 6), and is judged against A.

15. **A cap on participation** (her idea, 2026-11-05: "when prime age participation hit say, 0.78, it was just capped
    ... women entered the workforce until both parents in most households were working. Once that cap was hit, other
    things had to start moving"): a share 1 - cap of people never works at any wage; below the cap, participation follows
    the wage as before (`pinning_model.CappedEconomy`, a subclass, so the paper's economy and the forward model's stored
    parameters are untouched: the pinning battery 35/35, calibration (c)'s 47/47 and the macro battery 21/21 after it).
    The cap is set, not fitted: the mean prime-age employment rate since it first reached her 0.78, 1987–2024, 0.788.
    Tried on top of A (the last model she kept), judged against A, so it is read on its own whatever the split's verdict;
    combined with the split afterwards if she keeps both. A property found on the seen base fit before the run: with the
    cap, labour can run short of what the tasks machines cannot take need, and then the model has no land-scarce
    equilibrium (at the base fit's parameters, 2021–23: every task machines can take is taken, and the capped workforce
    still cannot staff the rest); the search has to keep away from such parameters.

16. **The cap is kept** (her verdict, 2026-11-05, on `figures/fig_fit_cap.png`). A + cap is the model the next change
    is judged against.
17. **The split is shelved** (her verdict, 2026-11-05: "its degenerate, so lets shelve it for now"). Its code stays
    (`code/split_model.py`, `checks/check_split_model.py`, `fit_base.py --split`), off by default.
18. **The basket at constant utility** (her framing and call, 2026-11-05: "build the basket next, set it from data";
    and "you may need to fix the utility around 1970, because I think by most counts it was rising until then"): goods
    and site substitute in a CES basket (`pinning_model.BasketEconomy`, calibrated share form), one unit of goods and h
    of site at the model's own 1950 price, so 1950 is unchanged. Two values set from the data, none fitted. The
    elasticity, 0.875: one minus the slope of the log odds of housing's share of consumer spending on the log of
    shelter's price over durables', all 75 years 1950–2024 (the rule fixed before computing; the two endpoints alone
    give 0.76 for 1950–2024 and 0.94 for 1964–2024). The basket's utility: rising until 1970 at the pace of the
    production worker's real hourly wage over the all-items CPI over 1950–1970 (2.1% a year; the same series grew 0.1%
    a year over 1970–2019), held after. The elasticity is between goods and shelter in the data and between goods and
    site in the model: shelter's price is taken to move with the site's.

19. **Claude looks at the fits again** (her call, 2026-11-05: "I take back my don't look at the graphs rule, just keep in
    mind the don't try to fit too hard rule"). Decision 13 is lifted; decision 12 stands.
20. **The start is pinned** (her suggestion, 2026-11-05: "fix prime age employments start point to the data"): the
    work cost's scale chi_max is set each time so that the model's 1950 prime-age employment is the data's
    (`fit_base.py --pin-start`), one free number fewer. Without A it costs nothing (misfit 6.74 -> 6.77).

21. **A is dropped** (her call, 2026-11-05: "drop a"). Shelter is read as site again (the base mapping). The kept model is
    the base with the cap, the basket and the pinned start (`results/fit_capbasket_pin.json`, misfit 6.8, eight free
    numbers).
22. **The basket's utility turning around in 1990 is shelved** (her idea, 2026-11-05, tried at once): knots at 1950,
    1970, 1990 and 2024 through the real wage over the all-items CPI (1.00, 1.52, 1.35, 1.66: falling 1970–1990, rising
    after; `fit_base.py --utility-knots 1950,1970,1990,2024`). Misfit 6.93 against 6.77 (Log 12): no better, so the
    utility rises to 1970 and is held after.

## Next

1. **Her model explorer** is built (Log 13): https://claude.ai/artifact/SeXw2LyrPk8urB7aH7cMRs (private to her).
   **The night's playground** (Log 14, `docs/playground.md`) for her morning: leads, not results.
2. **What is left** (Log 11): labour's share of consumption before about 1985, which the model holds up while
   participation rises; and the fit's strain (the required return at zero, the clock at 11% a year where the base's was
   6.4%, trading against the machine chain's labour growing 6.6% a year), so the clock's pace is not yet a number to
   hand to the forward model.
3. **A's shelter price capped the model's fork** (found at the basket's design; A dropped, decision 21). A prices shelter at w + (1 - w) p_t / p_2024 (rent 1, w 0.4):
   the built part moves with the final good, which the goods target reads as durables. The fork the model can then make
   between the two wage legs over any span is (S_t / p_t) / (S_0 / p_0) = 1 / (w p_t / p_0 + 1 - w) when t is the last
   year, at most 1 / (1 - w) = 1.67 whatever the fit, against the data's 5.9 (1950–2024) and the paper's 4.8
   (1964–2024). Arithmetic, found while designing the basket; no fit was looked at. On its own merit: building is not
   made like durables (construction's productivity has barely grown), so pricing the built part at the cost of building
   (the wage, in this model) rather than at the durables price is a candidate revision of A, for her call. Until then
   every variant on top of A carries the cap on the fork (the cap, the basket).
4. **Her framing, 2026-11-05**, the rest: land-free goods (the internet) after the basket, if the basket earns its
   place; kids staying home (household size) left out for now (it shrank from about 3.4 to 2.5 people over the record,
   from memory, unchecked).

## Log

1. **2026-11-05 — founded.** From her question in the session that unified the pinning model ("what do we even want
   from this model?"): the three-model layout (pinning; backward over 70 years; forward with a crash), US first, and
   simplicity as the discipline. `SPEC.md` written before any data or fit.
2. **2026-11-05 — Phase 1, the data panel.** Built from files already in the repository (the fork's legs, the effort
   accounts, κ, the financing splits, the λ series, chains.json, the waterline, FRED and BEA caches) and three new public
   fetches (FRED CNP16OV and CE16OV, BEA Fixed Assets section 1), each in `cache/` with its SHA-256 in the manifest.
   Gated 21/21 after the first run, which failed four checks, each fixed at its cause and marked in the battery: I4
   (the panel was written at ten digits; it is now full precision, and the check tolerates the last bit, because
   chains.json and calibration_c.json store the same number one unit apart); I5 (the four financing columns are separate
   medians and need not add to one); B1 (the labour-share band is the WEAK years' only); S2 (the 1981–85 real-rate floor
   was a guess; the adaptive expectation lags the disinflation). What the panel shows, before any model: the wage in
   durables rose about six-fold since 1950, while the wage in shelter peaked in 1973 and has stood near its 1950 level
   since 1990; labour's share of consumption fell from 0.66 to 0.47; the 16+ employment rate rose from 0.56 to 0.64 by
   2000 and stands at 0.60; the real long rate was highest in the 1980s and near 1% in 2023–24; depreciation rose from
   0.040 to 0.053; the machine chain's labour share fell from about 0.52 around 2000 to 0.45-0.47 since 2010.
3. **2026-11-05 — the first search, and decision 11.** From the paper's 2020s-like instance placed in 1950, with
   least_squares' Jacobian scaling, every start stopped after two iterations at the bounds (misfit 25.3): a broken search,
   not a result. Calibrating 1950 at its measured shares (pinning_model.calibrate_c) showed why the start mattered (at
   three baskets a person 1950 has no root: its labour share needs far fewer tasks on machines) and then that a required
   return following the measured real rate leaves no equilibrium in 1953-70: decision 11. The tolerances did not move
   (T1 gates them against 72adc83, the commit before the first fit).
4. **2026-11-05 — Phase 2, the base fit.** Twelve starts (1950 calibrated in closed form across what 1950 does not
   measure, both roots in k, two clock paces) all converge, in 79-96 iterations, to one optimum: **misfit
   19.3** (wage in durables 26.1, in shelter 14.2, labour's share
   13.4, prime-age employment 32.9, θ_V 10.1; 1 is one tolerance).
   Parameters: k 15.02, the clock 6.35% a year, rho 0.30 (at its bound), h at its floor
   (no land in the basket), lambda rising 3.64% a year. What fits: **the fork** — the capability path that
   reproduces the relative price of durables to shelter exactly each year (the accounting) lies on the constant-pace clock,
   about 6.4% a year, machines needing about a hundredth of their 1950 service per task by 2024. What does not: labour's
   share (the model's runs 0.45 -> 0.53 -> 0.40, hump-shaped, against 0.66 -> 0.47 falling; it cannot start at 0.66);
   prime-age employment (with support fixed at one basket it rises with the real wage to 0.94 by 2024, against 0.81 and
   flat since 2000); the wage in durables (x3.6 against x6.2); the wage in shelter (falls after 2008, against flat).
   A diagnostic fit without the employment target (not stored) still misfits 11.9, labour's share worst (17.2): the
   participation margin is not what drags the rest. Read against SPEC.md section 7: the base model gets the fork's
   direction and size with a smooth clock and does not get labour's falling share with it; the section allows A and B
   before that counts against the mechanism.
5. **2026-11-05 — A, run blind.** Shelter as a built good and site: the shelter price is (1 - w) p / p_2024 + w with
   rent the numeraire, w = 0.4, the site's value share of housing in 2024 (the paper's 30–50% midpoint); earlier years'
   share follows the model's own prices. No new free parameter; the same nine fitted, the same targets and tolerances.
   The search: one of twelve starts stopped at the iteration cap; continued from there it converged and did not beat the
   reported best (compared as a yes/no, no numbers shown), and the search now continues such starts itself (A re-run with
   it). Blind checks 8/8 (the accounting diagnostic reads the base mapping, so it is not run). `figures/fig_fit_A.png`
   sent to her unopened. Claude has not seen A's fit.
6. **2026-11-05 — A kept** (her verdict on `figures/fig_fit_A.png`). Her reading of it: the model's wage in durables does
   not kink up, nor its wage in shelter kink down and then flatten, as the data do; nothing obvious fixes that. Her
   question next, on its own merit: are people split yet, since computing (from about 1970) hit routine cognitive work?
7. **2026-11-05 — the split, run blind** (decision 14). Data: five new public fetches from FRED (CES0500000006, USPRIV,
   AWHNONAG and A132RC1A027NBEA; CES0500000003 as an anchor), giving the production group's share of private jobs
   (0.83 in 1964, between 0.81 and 0.83 since 1980) and the pay gap (1.00 in 1964, 1.22 in 1990, 1.35 in 2024). The pay gap takes
   everyone to work the production group's weekly hours, and NIPA wages include bonuses and exercised options, so only
   its change is read; over 2007–2024 that change is within 0.025 (log) of BLS's own all-employee earnings (I8). The
   panel battery gained five checks, 26/26. The model: `checks/check_split_model.py` 7/7 at its first run (without
   computing, the split equals the pinning model to 1e-13 on 87 economies at three group sizes; with computing both
   markets clear, income equals consumption, and the first group's wage falls below the second's). The fit: A's settings
   and targets unchanged, ten free numbers, fifteen starts (A's best with three paces of computing; the twelve 1950
   starts), run in parallel with the output unread (`code/fit_base.py --split 1970 --ref fit_A --quiet`). The first
   attempt, 39 starts one at a time, was stopped for time before it finished, unread. One start (the second 1950 start)
   stopped at the iteration cap twice; continued from where it stopped, it converged after 12,032 evaluations and did
   not beat the reported best (a yes/no, no numbers shown), and the search now continues such starts up to five times
   itself. Blind checks 9/9, with a new one: the split is no worse than A, which it nests (S3). `figures/fig_fit_split.png`
   sent to her unopened. Claude has not seen the split's fit.
8. **2026-11-05 — the cap, run blind** (decision 15). The cap set at 0.788; A's settings and targets unchanged, nine free
   numbers, thirteen starts (A's best and the twelve 1950 starts), in parallel, output unread
   (`code/fit_base.py --shelter-land-share 0.4 --cap --ref fit_A --out fit_cap --quiet`). The first launch was stopped
   at once, unread, to look at the property recorded in decision 15 on the seen base fit; the run that counts started
   after. Blind checks 8/8 (the re-solve reproduces the stored path with the cap as a subclass, R1). `figures/fig_fit_cap.png`,
   the prime-age panel with the cap drawn, sent to her unopened. Claude has not seen the cap's fit.
9. **2026-11-05 — her verdicts and her framing.** The cap kept (decision 16), the split shelved (decision 17). Her
   framing of land: "the economy wants to get the most money from you using the least amount of land": both parents
   working, then kids at home, then cheaper durables bought instead of shelter, then the internet; nobody worse off,
   since people substitute like for like, but each time the economy finds a way to give them less land. Read against the
   model: the participation margin and the machines' land were in it; the basket was fixed, so the substitution step had
   nowhere to act. The panel already showed it: housing's share of spending rose only from 0.11 to 0.16 over 1950–2024
   while shelter got about 6x dearer than durables; a fixed basket would have taken it from 0.15 in 1964 to about 0.45.
10. **2026-11-05 — the basket, run blind** (decision 18). Built as a subclass with a basket hook in the pinning model
    (`Economy.basket` returns one unit and h; `_parts` is bit-for-bit unchanged for Economy: the pinning battery 35/35,
    calibration (c)'s 47/47 with the macro battery inside it). `checks/check_basket.py` 11/11; its first run failed N2
    (the site's share as one minus the goods' share lost digits where h is tiny; each share is now computed directly).
    The panel gained the production worker's real wage over the all-items CPI (`real_wage_cpi`, two checks, 28/28). On
    the seen base fit, the basket removes the years without an equilibrium that the cap alone left (2021–23). The fit:
    A + cap's settings and targets unchanged, nine free numbers, thirteen starts (A + cap's best and the twelve 1950
    starts), output unread (`code/fit_base.py --shelter-land-share 0.4 --cap --basket --ref fit_cap --out fit_basket
    --quiet`); every start converged in 11-68 evaluations. Blind checks 8/8. `figures/fig_fit_basket.png`, against
    A + cap with the basket's make-up, the shares of spending and the utility path, sent to her unopened. Claude has not
    seen the basket's fit.
11. **2026-11-05 — the fits read together** (decision 19), and the pinned start with and without A (decision 20).

    | fit | misfit | wage, durables | wage, shelter | labour's share | prime-age emp. | θ_V |
    |---|---|---|---|---|---|---|
    | base | 19.3 | 26.1 | 14.2 | 13.4 | 32.9 | 10.1 |
    | A | 31.2 | 86.2 | 51.9 | 8.7 | 6.9 | 2.1 |
    | A + split | 31.2 | the same: computing went to zero (g_c 1e-38) | | | | |
    | A + cap | 28.3 | 72.9 | 55.3 | 9.6 | 1.6 | 2.0 |
    | A + cap + basket | 26.9 | 62.9 | 56.7 | 3.7 | 3.1 | 8.0 |
    | A + cap + basket, pinned | 27.9 | 54.1 | 67.8 | 2.8 | 4.0 | 11.1 |
    | cap + basket (no A) | 6.7 | 6.2 | 5.1 | 16.9 | 1.4 | 4.2 |
    | cap + basket, pinned | 6.8 | 6.4 | 4.7 | 17.1 | 1.4 | 4.2 |

    A raised the misfit by 60%: it fitted the levels (employment, θ_V) by giving up the fork, which its shelter price
    caps at 1.67x; every model built on it (the split, the cap, the basket) carried the same wrong wage legs (durables
    x2.6-2.9 against x6.2; shelter rising to 150-180 against a peak of 142 in 1973 and about 100 since 1990). Without A,
    the cap and the basket fit both wage legs (the wage in shelter rises to 1970 and falls after, as in the data, though
    it keeps falling after 2005 where the data flatten), employment and θ_V; all thirteen starts reach one optimum.
    What is left is labour's share: decomposed, it is the wage in goods times the share of tasks people do (1 - x)
    times goods' share of the basket's cost (0.86-0.89 throughout). From 1960 to 1990 the model's wage in goods rises
    x1.8 while 1 - x falls only from 0.40 to 0.25, so the share rises (0.48 to 0.54) where the data fall (0.61 to 0.50);
    once the cap binds (about 1985), tasks move to machines faster (x 0.75 -> 0.91 by 2024) and the share falls, as she
    framed it ("once that cap was hit, other things had to start moving"). The fit is strained: the required return is
    at its floor (0), the clock runs at 11.3% a year (the base's 6.4%), the machine chain's labour grows 6.6% a year,
    machine services in building a machine a = 9.4.
12. **2026-11-05 — A dropped; the utility turning in 1990 tried** (decisions 21, 22). With the knots 1950, 1970, 1990
    and 2024, the fit (thirteen starts, one optimum, checks 8/8) reaches 6.93 against 6.77: employment reaches the cap
    in 1980 rather than about 1987 (2.1 against 1.4), the rest within a few tenths. The wage in shelter still falls
    after 2005 (to 83 against the data's 105), so that gap is not the utility path's (`figures/fig_fit_kink90.png`).
13. **2026-11-05 — the explorer** (her wish and go). `explorer/model.js` is the model in JavaScript (the pinning
    model with the cap and the basket, the record's path, the misfit, a small Levenberg-Marquardt fitter);
    `checks/check_explorer.py` holds it to the Python model on every preset: 6/6 at the first run, every series and misfit
    to about 1e-13. `explorer/build.py` writes `explorer/data.json` (the panel's series and six stored fits as presets)
    and inlines both into `explorer/page.html` -> `explorer/index.html`, published as a private page. One path solves in
    about 1.4 ms, so the page re-solves as she drags; the fit runs in a Web Worker (from a perturbed start back to 6.78
    against the stored 6.77 in about three seconds). Controls: the cap, the basket, the pinned start, A, a steady or
    bendable clock; each number with a lock; draggable utility points, cap line and clock points; settings as text to
    copy back to Claude.
14. **2026-11-05, night — the playground** (her request: "play around with the model, try lots and lots of stuff
    cheaply"). About sixty one-start refits from the kept fit with the explorer's fitter (`playground/*.js`, raw numbers
    beside them), read in `docs/playground.md`. In short: the clock's pace, the return, a and the machine-making labour
    lie on a ridge (clock 8-14% within 0.5 of the best; a 5% return costs 0.7, clock 8.6%); the measured real rate in the
    return makes things worse; the cap and the basket both work, and the basket is what lets the cap work (without it
    117.8); the utility's rise-then-hold matters, its turning year hardly does; A′ (the building priced at the wage)
    is a mild, principled improvement (6.28); her internet idea, tastes tilting from land after 1995, fixes the wage in
    shelter after 1995 (5.22; shelter 0.6) at the cost of land's share of spending falling where housing's rose; labour's
    share before 1985 moves only under bendable clocks whose shapes depend on the knots (fits to the curve). The
    explorer gained switches for A′ and the tilt and three playground presets (`explorer/model.js` gained optional paths
    for land, the cost of working, the machine-making labour, the tilt, a pinned 1950 labour share and the measured rate,
    all off by default; `checks/check_explorer.py` 6/6 still).
15. **2026-11-06 — the explorer, second version** (her asks: linked numbers shown with what they imply; the fitter
    working in whichever of two linked numbers she chooses; bendable paths with points whose year or level can be fixed;
    sensitivities). `explorer/model.js` gained coordinates (land as T and h or T and h/T; machine services as a or their
    share of a machine's cost in 1950, so a follows the return; the hours to build a machine growing per machine or per
    fixed task), a fitter that works in them and moves knots' years as well as levels, a bendable land-in-a-machine path
    (her question: what is being built), and the model's insides year by year. With every number free, fitting in shares
    reaches the same optimum (6.7723). The page: the dials grouped where numbers are linked, each group saying what the
    other number comes to; a second view inside the model (the task line by year, a machine's cost, the land, the hours
    and a basket's cost in shares, labour's share taken apart); a third with sensitivities (each number nudged both ways:
    how many of the five misfits move more than 5% and the sum of their changes). At the kept model the clock's pace and
    the growth of the hours to build a machine are the sharpest numbers (half a point moves the misfits' sum by 10 to 18);
    the cap and the utility's turning year barely matter. Shown against the forward model's 2023 measures: the kept fit's
    machine-making takes 55% of all hours by 2024 (measured 15%) and land 0.5% of a machine's cost (measured 33%).
16. **2026-11-06 — the explorer, third version** (her asks). Years without an equilibrium no longer blank the model: the
    path is solved year by year, the years that fail are shaded, and the misfit is shown over the years that solve.
    "Find a start" (`model.js` `search`): moves the free numbers and points at random around where they are, keeping
    moves that leave fewer years without an equilibrium (or nearer to one), until every year solves; with the clock held
    at 4% a year it finds a start in under ten tries, and the fit from there reaches 24.3 (the continuation profile of
    Log 14 reached 26.1). The right pane stays in view as the controls scroll. Guides: each slider shades a usual range
    (evidence where there is some: the return 1-8%, machine services 10-40% of a machine's cost; judgments for the
    clock and the growth of machine-making hours, labelled as such; the stored fits' span for the scale numbers), and a
    number outside it is marked; each record chart marks the years more than one or three tolerances off. Each dial shows
    its sensitivity (the five series as squares, a bar for how much the misfits move, "near an edge" when a small step
    loses an equilibrium). Each bendable path has a small plot beside its table, points drawn by what can move. Cards
    and control groups can be focused: focused ones move to the top, the rest fold to their titles.
17. **2026-11-06 — exploring while she was away** (`docs/playground.md`, the last two sections). Her spiky settings are
    mostly the machine's size changing: the model has two real clocks, the land and the hours embodied per unit of task
    capacity, and rescaling the machine year by year leaves the fit exact to the last digit. Waves dated from the
    productivity record (1948, 1995) take the kept model from 6.77 to 5.53. The largest lead: labour's share is at odds
    with the wage in durables, not with the model; with the goods wage read over everything but shelter (the panel's new
    `wage_exshelter`, check I10) and women's entry (the cost of working falling to 0.77 by 1990, one number), every series
    fits within 1.1 to 5.3 tolerances (misfit 2.92, ten of twelve restarts to the same optimum). It still needs a zero
    return and half of a machine's cost in machine services, and it gives up the durables fork, which would take a second
    good. In the explorer: a switch for the goods deflator, a women's-entry control and the preset.
