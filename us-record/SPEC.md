# us-record — the paper's model against the US record, 1950–2025

The backward model: the pinning model run through 75 years of US data. Written 2026-11-05, before any fitting.
A working spec: it changes at the breakpoints below, and every change is recorded in `STATE.md` with its reason.

## 1. What it is for

1. **A test the mechanism could fail.** Does the paper's account (wages pinned at the task margin by the cost of
   machines, which traces back through machine-making to land) reproduce what happened to American wages, prices and
   work since 1950, without building in the answer?
2. **The clocks, measured.** How fast machine capability, the labour in machine-making and land scarcity actually
   moved. The forward model's speeds are guesses today.
3. **An attribution.** How much of each fact (the wage's lost ground against shelter, labour's falling share) each
   force carried.
4. **A starting point.** The economy in 2025 in the model's own terms, and the clocks' measured speeds, handed to the
   forward model (`../paths/`) in place of calibration (c)'s static targets.

It is not a forecaster (the forward model is), not a business-cycle model (recessions belong to the crash model), and
not a general-equilibrium model of everything. It may find that the mechanism explains part of the record and not
the rest. That is a result.

## 2. The discipline: accuracy through simplicity

Her thesis is that a small set of forces drives the economy; the model should show it or fail to.

- **The paper's model, with as few additions as the record forces.** The core is `../pinning/code/pinning_model.py`,
  unchanged, solved each year (annual and quasi-static, as in the paper).
- **Everything earns its place.** A component stays only if it does real work in the fit; the paper's own pieces face
  the same test as the additions (ablation, section 6). If something does not do much, it is cut.
- **Few free numbers, smooth in time.** Time variation enters only through measured inputs or a small number of smooth
  drivers, each a curve with at most three parameters. No year-by-year free parameters in the final model.
- **Credibility from economy, not from many holdout sets.** The case for believing the fit is the ratio of facts
  matched to numbers chosen, and the series the model was never fitted on (section 5). One time split (fit to 1995,
  read 1995–2025) is reported as a reading, not used as a gate.

## 3. The model

The pinning model each year. Its objects (rent r = 1, v = w/r): the capability schedule gamma(x) = eta (g0 + g1 x^k),
machines at user cost (rho + delta), the machine chain's labour lambda, the basket of one final good and h units of
site, participation from log(1 + w/P_s) against funded support, land T.

| Kind | What | Source |
|---|---|---|
| Measured input | adults N_t (population 16+) | FRED CNP16OV, 1948– (to fetch; total population is cached, `../pinning/cache/B230RC0A052NBEA.csv`) |
| Measured input | depreciation delta_t; the required return rho is a constant in the base model (decision 11; the measured real long rate, Moody's Aaa less expected inflation, is candidate I) | BEA Fixed Assets; `docs/measurement.md`, choice 2 |
| Measured input | the machine chain's labour content: theta_V,t, from which lambda_t follows | `../progress_and_prosperity/lambda/data/` (1997–2023; benchmark years from 1947) |
| Free driver | machine capability eta_t: the capability clock, one smooth curve | fitted |
| Fixed parameters | a, b, g0, g1, k, h, T, chi_max | fitted once over the whole record |

About ten free numbers in the base model, against four targeted series over 75 years.

## 4. Facts to match (targeted)

Each is mapped to a model object by a stated measurement equation; where the data carry a band, the misfit is measured
against it.

1. **The real wage in goods**: hourly earnings over the durables price (AHEMAN, AHETPI; CUUR0000SAD), 1950–2025.
   Model: v / p. Already built: `../pinning/effort/data/fig3_realwage_fork_1950.csv`.
2. **The real wage in shelter**: the same earnings over rent of primary residence (CUUR0000SEHA). Model: the wage over
   the shelter price. Shelter is structures and site, so the measurement equation is a composite (addition A below).
   Together, 1 and 2 are the deflator fork.
3. **Labour's share of consumption, full chain**: the human-effort share, 0.66 in 1950 to 0.46 in 2025, with its band.
   Model: v (1 - x) / P_s, the consumption chain's labour with capital services left in surplus, as calibration (c)
   reads the same series (`ChainTargets`, basis "bea").
   `../pinning/effort/archive_v28/expected/LR_Q1_fullchain_factor_content_strong_weak_1950_2025.csv`.
4. **The prime-age employment rate, 25–54** (LNS12300060, aggregate), 1950–2024. Model: N_a / N, the participation
   margin where retirement and school matter least; adults 16+ set the population's growth (her call at breakpoint
   A, 2026-11-05: the 16+ rate's fall after 2008 is mostly ageing, which the model does not have). Aggregate rates
   only (decision 3).

## 5. Facts not targeted (what the fit is judged on)

The model must get these roughly right without being fitted to them:

- the coverage ratio κ, 1953–2025: site rent against the subsistence bundle (`../pinning/data/kappa_results.csv`);
- labour-origin financing, 1950–2025, and the four-way financing split, 1960–2025
  (`DF21_FINAL_longrun_labor_origin_financing_1950_2025.csv`; `../pinning/data/four_way_split.csv`);
- the wage against machine cost at the margin, 1999–2025, an independent read of the capability clock: the model's
  gamma(x*) (`../companion/data/wc_grid.csv`);
- the nonfarm business labour share (PRS85006173), on its own basis;
- land values and housing's share of spending (Z.1 and BEA series in `../pinning/cache/`);
- the 16+ employment rate (EMRATIO): the targeted rate plus demography (ageing, school), which the model leaves out;
- with the split (J below): the pay gap, all private employees' average hourly wage over the production and
  nonsupervisory group's, 1964–2024, and that group's share of private jobs.

## 6. Additions and rivals, under one rule

The base model is section 3. Each candidate below enters only if it earns its place:

- **The rule, set before fitting.** A component stays if removing it raises the misfit by at least 20%, or if without
  it some targeted series leaves its measured band. Otherwise it is cut. The base model's own pieces are tested the same
  way at the end (ablation). The threshold may be revisited once, at breakpoint B, with the reason recorded.
- **The misfit.** The mean squared log deviation over the targeted series, each scaled by its band where it has one and
  by a stated tolerance where it has none.

Candidates the paper's account would add:

- **A. Shelter as structures and site.** A measurement equation, not new economics: the CPI's shelter is a built good
  plus land. Likely needed for fact 2. Dropped (decision 21): priced with the final good, the built part caps the
  model's fork at 1 / (1 - w) = 1.67x, against the data's 5.9x.
- **B. A shift in who is willing to work.** One smooth curve in the work-cost distribution (women's entry, 1950–2000).
  Likely needed for fact 4. In model B (decision 23): the cost of working falls, straight in logs, to 1990 and is held
  after; its level by 1990 is one free number (`fit_base.py --women 1990`). Removing it raises B's misfit 133%.
- **C. Support that rises with income.** The outside option partly indexed to wages (balanced growth).

Rivals, under the same rule so the record can favour them:

- **D. New human tasks**: the top of the schedule extending (reinstatement).
- **E. Land supply restricted**: effective land T_t falling (zoning), rather than land fixed while demand grows.
- **F. Markups**: a wedge between price and cost.
- **G. Trade**: a foreign wage as a second machine rental on tradable tasks.
- **H. Time to build**: investment that runs ahead of the margin. Only if the record's investment swings force it.
- **I. The required return following the market** (decision 11, 2026-11-05): rho_t passing through the measured real
  long rate, against the base model's constant rho.

Her additions in Phase 3, tried on their own merit (decision 12):

- **J. People split in two, and computing** (her question and calls, 2026-11-05; decision 14): BLS's production and
  nonsupervisory employees (the group whose wage every wage target reads) and everyone else in private jobs, managers
  and supervisors, each working its own block of tasks; computing, from 1970, makes machines better at every task of the
  first group's block. One new free number (computing's pace); the groups' sizes set from the data. Nests the one-group
  model exactly when computing is off (`checks/check_split_model.py`).
  Shelved by her verdict (decision 17).
- **K. A cap on participation** (her idea, 2026-11-05; decision 15; kept, decision 16): women entered work until both parents in most
  households worked, and then prime-age participation stopped rising, so other things had to move. A share of people
  never works at any wage (`pinning_model.CappedEconomy`); the cap is set at the mean prime-age employment rate since it
  first reached her 0.78 (1987–2024: 0.788). No new free number. Out of model B (decision 23): with women's entry it
  adds 1.5%.
- **L. The basket at constant utility** (her framing and call, 2026-11-05; decision 18): the economy finds ways to give
  people less land for the same utility; as goods cheapen, a basket holds more goods and less site
  (`pinning_model.BasketEconomy`). The elasticity is set from the data (housing's share of spending against shelter's
  price over durables', 1950–2024: 0.875); the basket's utility rises until 1970, at the production worker's real-wage
  growth (2.1% a year), and is held after. No new free number. In model B the utility's knots are 1950, 1970, 1990 and
  2024 (the dip, decision 23): the rise is worth 58% of B's misfit and the dip 29%; the basket 197%.
- **M. The goods wage read over everything but shelter** (her setup, 2026-11-06; decision 23): a measurement change. The
  model has one good, and the consumer's goods are mostly not durables; the target becomes production workers' earnings
  over CPI-U less shelter (`wage_exshelter`, `fit_base.py --goods exshelter`). The durables wage becomes a fact not
  targeted (section 5); one good cannot carry both (it rises 6.2-fold against 2.0-fold).
- **N. Dated technology waves** (her idea, 2026-11-06): on top of the steady clock, a discovery chased hard and then the
  lower fruit; the clock falls by size (1 - exp(-(t - year) / tau)) after the wave's year (`fit_base.py --waves 1948`).
  Two free numbers a wave. A post-war wave (1948) takes B from 2.81 to 2.00 (-29%) and the clock from 12.5% to 6.8% a
  year: it passes the rule. Kept: the main case (decision 24). A wave dated before 1950 is the same model whatever its
  year (the record starts in 1950): an early clock running fast and slowing.

## 7. What would count against the mechanism

Written now, so they cannot be redrawn after the fit:

- no smooth capability clock lets the base model (with A and B at most) reproduce the fork's direction and roughly
  its size (4.8 over 1964–2024) and labour's falling share together;
- the capability path the fit needs contradicts its independent reads: it falls for long stretches, or it moves against
  the wage-to-machine-cost record of 1999–2025, or the fit needs lambda to move against its measured fall;
- the rivals (E, F, G) carry most of the fork or of labour's fall, and ablation cuts the paper's channels.

Any of these is reported as found, and the forward model does not take its start from a model that failed them.

## 8. The order of work

| Phase | What | Ends at |
|---|---|---|
| 0 | This spec | committed before any fitting |
| 1 | The data panel, annual 1950–2025: each series stored in the repo with its source and a manifest, measurement equations stated | **Breakpoint A** (hers): the mapping and the panel |
| 2 | The base model fitted (section 3); year-by-year accounting as a diagnostic only, to see what the capability path would have to be | **Breakpoint B** (hers; the stop point): does the paper's model get the core facts' direction and size with a smooth clock? |
| 3 | Additions and rivals under the rule; ablation; the attribution | the model as small as the record allows |
| 4 | The untargeted facts; the time split as a reading; the hand-off | **Breakpoint C** (hers): the forward model takes the 2025 state and the clock speeds |

## 9. The hand-off

The 2025 state (every parameter and driver) and the capability clock's speed go to `../paths/`. The forward model takes
them as a new central calibration, with calibration (c) kept beside it as a sensitivity, after its checks pass.
The forward model's clock is then the measured one, extended.

## 10. Data

Public sources only (FRED, BEA, the Fed's Z.1, BLS through FRED). Much is already in the repository: the fork and its
raw series (`../pinning/effort/data/`), the effort accounts, κ, the financing splits and the tax-base shares
(`../pinning/data/`), the λ series (`../progress_and_prosperity/lambda/data/`), the waterline
(`../companion/data/wc_grid.csv`), and FRED and Z.1 caches (`../pinning/cache/`, `../paths/cache/`). New series are
fetched once, stored with a manifest and checked against identities. A source that fails or cannot be validated stops
the step, and it is reported, not substituted (her standing rule).
