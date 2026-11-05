# Measurement — how each panel column maps to the model

`data/panel.csv` (built by `code/panel.py`, gated by `checks/check_panel.py`), annual, 1950–2025. The model's objects are
`../pinning/code/pinning_model.py`'s (rent r = 1, v = w/r, p the final good's price in rent units, P_s = p + h the basket's).
Written 2026-11-05 at the end of Phase 1, before any fitting; breakpoint A is her review of this mapping.

## The targeted facts

| Column | Data | Model | Years |
|---|---|---|---|
| `wage_goods` | hourly earnings over the durables CPI, 1950 = 100 (AHEMAN to 1963, then AHETPI; CUUR0000SAD to 1955, then CUSR0000SAD; the paper's Figure 5 leg, `../pinning/effort/data/fig3_realwage_fork_1950.csv`) | v / p, indexed to 1950 | 1950–2024 |
| `wage_shelter` | the same earnings over shelter (CUUR0000SEHA rent of primary residence to 1952, then CUSR0000SAH1 shelter), 1950 = 100 | the wage over the shelter price; shelter is a built good plus site, so the price is a composite of p and r (addition A, `SPEC.md` section 6). Without A, shelter is pure site and the leg reads v | 1950–2024 |
| `labour_share_c` | the full-chain human-effort share of consumption (`LR_Q1`, headline) | v (1 - x) / P_s, the consumption chain's labour with capital services in surplus, as calibration (c) reads the same series (`ChainTargets`, basis "bea") | 1950–2025 |
| `labour_share_c_lo`, `_hi` | the regression (weak) estimate's band, in the 49 WEAK years only | the misfit's scale there; the 27 STRONG years (1997–2023, from annual input-output tables) carry no band and take a stated tolerance in Phase 2 | WEAK years |
| `prime_emp_rate` | employment over population, 25–54 (LNS12300060, aggregate; targeted since breakpoint A, her call) | N_a / N; adults 16+ set the population's growth | 1950–2024 |

Together, `wage_goods` over `wage_shelter` is the deflator fork: x4.8 over 1964–2024 (gated, I2).

## The measured inputs

| Column | Data | Model | Years |
|---|---|---|---|
| `adults` | civilian noninstitutional population 16+, thousands (CNP16OV) | N_t, indexed as the fit needs | 1950–2024 |
| `real_rate` | Moody's Aaa yield less the mean log CPI inflation (CPIAUCNS) of the five years to t | rho_t = `real_rate` + a constant premium (one fixed parameter) | 1950–2024 |
| `real_rate_gs10` | the ten-year Treasury yield, the same expectation | a variant | 1954–2024 |
| `delta` | BEA Fixed Assets, all fixed assets: current-cost depreciation (Table 1.3) over the average of the year's opening and closing current-cost net stock (Table 1.1) | delta_t (0.0522 in 2023, calibration (c)'s; gated, I3) | 1950–2025 |
| `theta_V` | the machine chain's full-chain labour share of a machine's build cost: annual 1997–2023 on calibration (c)'s basis (equipment + IPP + private structures, domestic labour; `../paths/results/chains.json`); six benchmark years 1967–1992 from the λ thread's century arc (narrow machinery, import-comparable), linked by the 1997 ratio | theta_V = lambda v / Vm, from which lambda_t follows given the solved v and Vm | 1967–2023, at 33 years |

## The facts the fit is judged on (never targeted)

| Column | Data | Model |
|---|---|---|
| `kappa_med` (`_min`, `_max`) | the coverage ratio: site rent over the subsistence bundle for every adult (`../pinning/data/kappa_results.csv`) | T / (N P_s) on the paper's definition |
| `labor_origin_fin` (`_lo`, `_hi`) | the share of consumption financed from labour income (`DF21`) | the wage bill's share of income |
| `fin_wage_direct`, `fin_wagetax`, `fin_ownertax`, `fin_borrowed` | the four-way financing split, medians over its grid (they need not add to one) | the model's income split, once a state is added (or not) |
| `wc_median` | the wage against machine cost at the margin, 1999 = 1 (`../companion/data/wc_grid.csv`) | gamma(x*), indexed: an independent read of the capability clock |
| `nfb_labour_share` | the nonfarm business labour share, 2017 = 100 (PRS85006173) | labour's share of income, on BLS's basis |
| `emp_rate` | civilian employment over the civilian noninstitutional population 16+ (EMRATIO; targeted until breakpoint A) | the targeted rate plus demography (ageing, school), which the model leaves out |
| `housing_share_pce` | housing and utilities services over all consumer spending (BEA) | shelter's share of the basket, structures and site |

## The split (her calls, 2026-11-05)

People in two groups as BLS's wage data split them: the production and nonsupervisory group (about four in five private
jobs; the group whose hourly earnings, AHETPI, every wage target reads) and everyone else in private jobs, managers and
supervisors. Each works its own block of tasks (`code/split_model.py`).

| Column | Data | Model | Years |
|---|---|---|---|
| `pns_share` | the production and nonsupervisory group's share of private jobs (CES0500000006 over USPRIV) | its mean over 1964–2024, 0.8185, sets the groups' sizes: managers and supervisors are s_N = 0.1815 of the population and of the final good's tasks, and supply that share of the machine chain's hours. A set input, not a target; the model's own share of employment, n_R / (n_R + n_N), is a check | 1964–2025 |
| `pay_gap` | all private employees' average hourly wage over the production group's: NIPA private wages and salaries (A132RC1A027NBEA) over private jobs (USPRIV) times that group's weekly hours (AWHNONAG) times 52, over its hourly earnings (AHETPI); 1964 = 1 | (n_R v_R + n_N v_N) / ((n_R + n_N) v_R), 1964 = 1. A check, never targeted | 1964–2025 |
| `ahe_all` | all private employees' average hourly earnings (CES0500000003), from March 2006 | none: the pay gap's anchor (`checks/check_panel.py` I8) | 2007–2025 |

Caveats on the pay gap, which is why only its change is read: everyone is taken to work the production group's weekly hours
(managers work longer, so the level overstates their hourly pay); NIPA wages include bonuses and exercised stock options,
which CES hourly earnings leave out. Over 2007–2024 its change is within 0.025 (log) of BLS's own all-employee measure
(I8).

## The basket (decision 18)

| Column | Data | Model | Years |
|---|---|---|---|
| `housing_share_pce` | as above | with the basket, it sets the elasticity of substitution between goods and site: one minus the slope of its log odds on the log of shelter's price over durables' (the wage legs' ratio), 1950–2024: 0.875. No longer an independent check for that variant | 1950–2025 |
| `real_wage_cpi` | the production worker's real hourly earnings: AHEMAN (manufacturing) to 1964 and AHETPI after, linked at 1964, over the all-items CPI (CPIAUCNS), 1950 = 100 | sets the basket's utility path: rising at its 1950–1970 pace (2.1% a year) until 1970, held after | 1950–2024 |

## Choices made in Phase 1, with their reasons

1. **Complete calendar years only** (the repository's rule): a monthly series' year needs all twelve months. October 2025 was
   never published (the CPI, the household survey), so 2025 is missing for the wage legs, the employment rate, adults and the
   real rate. Nothing is filled or extended. The annual sources (the effort accounts, BEA, κ) run to 2025.
2. **The long rate is Moody's Aaa, not the ten-year Treasury.** The Treasury series starts in April 1953; Aaa covers the
   whole window and is closer to a firm's cost of funds. The Treasury version is kept beside it (`real_rate_gs10`).
3. **Expected inflation is adaptive: the mean of the five years to t.** Simple and available for every year. It lags turning
   points: it understates real rates in the disinflation of 1981–86 and overstates them in an inflation surge. The fit
   takes rho_t with a constant premium, so a level error in this proxy goes into the premium; a timing error does not.
4. **θ_V is linked across bases at 1997.** The benchmark years are a narrower machine set on a different import basis; linking
   them by the 1997 ratio assumes the two move in proportion. The λ thread's own splice (1992 SIC to 1997 NAICS) sets
   1992 equal to 1997, so 1992–97 carries no measured change. Before 1967 there is no compensation split: nothing is measured.
5. **The labour-share band is the WEAK years' only.** In the STRONG years the headline is the direct measurement and the file's
   band belongs to the regression estimate beside it (found by the battery's first run: B1).
