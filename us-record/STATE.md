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
9/9, drawn in `figures/fig_fit_base.png`). Breakpoint B passed. Phase 3 under way, blind (decision 13): A kept; the split
(decision 14) and the cap (decision 15) run and sent for her verdict.

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

## Next

1. **Her verdicts on the split and the cap** (`figures/fig_fit_split.png`, `figures/fig_fit_cap.png`, both sent
   unopened; each against A). If she keeps both, they are run together.
2. **Her framing, 2026-11-05**: the economy finds ways to give people less land for the same utility: both parents
   working (the cap), then cheaper durables bought instead of space, then land-free goods (the internet). The model's
   basket is fixed (one good and h of site a person), so it has no room for the second step. Proposed, not built:
   **L, a basket held at constant utility**, goods and space substituting with one elasticity set from the panel
   (housing's share of spending 0.11 -> 0.16 over 1950–2024 while shelter got about 6x dearer than durables: about 0.8;
   a fixed basket would have taken the share from 0.15 in 1964 to about 0.45), checked on housing's share of spending.
   Waiting for her go and her call on setting the elasticity rather than fitting it.

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
