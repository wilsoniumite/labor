# Understanding the Great Stagnation — spec

Written 2026-11-16, before any outcome data for this paper was pulled. The commit that adds this file is the
freeze for the cross-country test H-X (Section 7); its hash is recorded in `../STATE.md`. Amendments after the
freeze go in the log at the foot of this file, dated, each saying whether outcome data had been seen.

## 0. Standing

- **A standalone paper.** It restates the model it uses and proves its own results. It cites Båge and Wilson
  (2026), *Pinning the Wage to Scarcity and Technology* (SSRN 7226858), for the general cost system, and cites the
  real-wage fork (4.8×, 1964–2024) and the coverage ratio (0.30 in 2025) from it without rebuilding them.
- **House rules, as in `pinning/`.** Every number in the text comes from a script; each result is checked in sympy
  and numerically before it enters the prose; figures come from scripts, drawn at print width; data come from primary
  public sources only, and on any access failure the work stops and reports instead of substituting; references are
  checked against Crossref before submission; code is written as plain functions in notebook-cell style, with tqdm on
  long loops.
- **Byline:** open (her call; `../STATE.md`).

## 1. Thesis

Measured output per hour is an equilibrium outcome: the inverse of the hours an economy uses per unit of output.
When production and living costs depend on an input that cannot be produced (sites, deposits, permits), machine
progress raises output per hour only as far as hours are released. Where support outside work is funded and
unconditional, falling wages release hours and measured productivity eventually rises in proportion to machine capability. Where
consumption is financed by wages and support is conditioned on work, the hours stay, the wage falls instead, displaced
workers are re-employed at tasks of low value, and the gains from machine progress go to rents. Keynes (1930) expected
the first. The record since about 1973 looks more like the second: Joan Robinson's (1936) disguised unemployment,
spread over decades. The same cost system says why real interest rates, land values, the gap between pay and
productivity, and the composition of employment moved as they did.

The paper does not claim that technology stopped improving or that its frontier did not slow; it claims that the
measured aggregate can stall while machines improve, and says what has to be true of hours, land and institutions
for that to happen.

## 2. What the paper must explain

Each item is measured in Section 6 (M1–M5) from primary sources; none is quoted from memory. The only values
computed so far are the output-per-hour eras, from the cached FRED vintage in `../paths/cache/OPHNFB.csv`
(annual averages of the quarterly index): 2.76%/yr 1948–73, 1.43% 1973–95, 3.04% 1995–2004, 1.50% 2004–19,
2.16% 2019–25. They are rebuilt from a fresh pull in M1.

- F1 the eras of output per hour (above);
- F2 typical pay against productivity;
- F3 hours per worker stopped falling in the U.S. around 1980 while they kept falling in much of Europe;
- F4 labor's share of income fell, mostly since 2000;
- F5 real interest rates fell from the early 1980s to 2020 and rose after 2022;
- F6 land's share of household real estate rose;
- F7 the real-wage fork (cited from pinning);
- F8 employment moved toward in-person services;
- F9 output per hour picked up after 2019.

## 3. The model (standalone)

A stationary task economy with durable machines and one non-produced input; the three-row instance of the cost
system in Båge and Wilson (2026, Appendix B), with labor supply generalized.

- **Tasks.** One unit of each task x ∈ [0,1] per unit of the final good. An hour completes one unit of any task; a
  machine-hour completes 1/γ(x) units of task x. γ (relative human productivity) is continuous, positive, strictly
  increasing on (0,1]. J(x) = ∫₀ˣ γ.
- **Machines.** A machine takes a units of machine services, λ hours and b units of land services to build, supplies
  one unit of service a period, depreciates at δ ∈ (0,1], and its owner requires the return ρ ≥ 0: p_m = (ρ+δ)V_m,
  V_m = a p_m + λw + br. Assume (ρ+δ)(a + λγ(0)) < 1 and aδ < 1.
- **Land.** Fixed service endowment T at rent r (the numeraire, r = 1; v = w/r).
- **The basket.** One unit of the final good and h > 0 units of space; P_s = p + h.
- **People.** N persons, one hour each or none. Work cost χ ~ F, continuous on [0,∞), F(0) = 0. A share 1−θ have
  *funded exit*: one basket of support in both states, plus Δ ≥ 0 baskets when working; such a person works iff
  log(1 + ω + Δ) ≥ χ, ω = w/P_s. A share θ have no support outside work and work at any positive wage. θ indexes
  enclosure (support eroded or never given), Δ conditioning (support paid for working). A provider owning the land
  and the machines pays the support from rent and interest.
- **Equilibrium at an interior margin x ∈ (0, x_c)** (x_c: first task where D(x) = 1 − (ρ+δ)(a + λγ(x)) = 0, or 1):
  - prices: p_m = (ρ+δ)b/D, v = γ p_m, p = v(1−x) + p_m J, P_s = p + h;
  - quantities: B_s = h + bδJ/(1−aδ) (full-chain land per basket), L_s = 1 − x + λδJ/(1−aδ) (full-chain hours per
    basket), Y = T/B_s, n_D = T L_s/B_s;
  - supply: n_S = N[θ + (1−θ) F(log(1 + ω(x) + Δ))];
  - clearing: n_D(x*) = n_S(x*); funding: T + ρV_mX ≥ P_s[(1−θ)N + Δ·(hours of the supported)].

## 4. Results to prove

Each is checked in `checks/check_theory.py` (sympy for the algebra, numbers on the instance and on random
economies). Restated 2026-11-16 after the independent review (Amendments); the statements below are the paper's.

- **Clearing and equilibrium.** If T > Nh and supply exceeds demand at x_c, exactly one threshold in (0, x_c) clears
  the labor market; it is an equilibrium if support is funded there, (7). Funding is a separate condition.
- **Lemma 1 (output per hour).** At an interior equilibrium, Y = T/B_s(x*), N_a = T L_s(x*)/B_s(x*), and output per
  hour π = Y/N_a = 1/L_s(x*). L_s is strictly decreasing and B_s strictly increasing on (0, x_c). Across equilibria
  with the same technology, land endowment T and basket h, d log π / d log N_a = −1/(1+ψ), ψ = (B_s'/B_s)/(−L_s'/L_s)
  > 0, so the elasticity lies in (−1, 0).
- **Proposition 1 (absorption).** Fix technology, T and h. If labor supply rises at every margin, strictly at the
  original equilibrium, the margin moves toward labor; hours and output rise; output per hour, w/r and w/P_s fall. A
  higher θ is such a shift where some supported people do not work; a higher Δ where F has a positive density at
  log(1+ω+Δ). Labor's share is ω L_s(x*), so absorption's effect on it depends on the schedule (it rises in the
  instance and falls with a steeper schedule).
- **Proposition 2 (machine progress and the hours that remain).** Let γ_η = ηγ̂ with η ↓ 0, along funded interior
  equilibria, everything else fixed. (i) w/r → 0, w/P_s → 0, labor's share → 0. (ii) Hours → N_∞ =
  N[θ + (1−θ)F(log(1+Δ))]. (iii) Output → T/h; output per hour → T/(hN_∞) if N_∞ > 0, a ceiling machine progress
  cannot raise, and diverges if N_∞ = 0. (iv) With γ̂ continuously differentiable near [0,1] and F with a continuous
  density near log(1+Δ), positive at zero when N_∞ = 0, the elasticity of output per hour with respect to machine
  capability across stationary equilibria, d log π / d log(1/η), tends to one when N_∞ = 0 and to zero when N_∞ > 0
  (a comparison of stationary states, not a growth rate along a path). Clearing thresholds are interior for small η
  when T > Nh and N_∞ > 0, or λ = 0 with F(z) > 0 for z > 0, or N_∞ = 0 with f(0) > 0 and condition (12); support is
  funded for small η if T > h[(1−θ)N + ΔN_∞].
- **Proposition 3 (the required return).** (i) At a given margin, ∂log(w/r)/∂log(ρ+δ) = 1/D(x) ≥ 1 (strictly if
  a + λγ > 0), where D is land's share of a machine's build cost; w/P_s is increasing in ρ. (ii) Whoever can leave
  work, the equilibrium with the lower required return has lower w/r, w/P_s and labor's share and a higher price of
  land in hours of work (proof through the identity 1/ω = m(x) + h/v, m(x) = 1 − x + J/γ nonincreasing). (iii) With
  θ = 1 the margin does not depend on ρ: hours, output and output per hour are unchanged, and the land price in hours
  has elasticity −1 − ρ/((ρ+δ)D) with respect to ρ. (iv) With θ < 1, a lower required return lowers labor supply at
  every margin, strictly where F has a positive density at log(1+ω+Δ): hours fall and output per hour rises.
- **Lemma 2 (the price wedge).** With prices resolved into hours and land at user cost, P_j = w L̃_j + r B̃_j (the
  price requirements, which with ρ > 0 charge each round of machine-building at ρ + δ), ∂log(P_C/P_Y)/∂log(r/w) =
  β_C − β_Y with β_j = r B̃_j / P_j; real pay per hour over output per hour equals labor's share times P_Y/P_C.
- **Lemma 3 (composition).** With CES consumption over a machine-made good and a bound good (land-bound or
  human-required): (a) at σ < 1, if the machine-made good's relative price falls to zero at a bounded rate, the bound
  good's expenditure share tends to one, measured (Divisia) growth tends to the bound good's growth, and consumption
  is bounded by a multiple of the bound good; (b) at σ ≥ 1, consumption is unbounded in the machine-made good. The
  economy with a CES basket is not solved. (Baumol 1967; Ngai and Pissarides 2007.)
- **Remarks.** (a) The results are positive: they describe measured output per hour, not welfare; ranking
  allocations needs a criterion the paper does not supply, and a uniform rent dividend is not in the model (in the
  instance rent alone covers 0.38 of a basket per person). (b) Directed automation: cheaper labor lowers the private
  return to automating labor-held tasks (Habakkuk 1962; Allen 2009; Acemoglu 2010), a channel not modeled. (c) θ is a
  primitive here; its endogenous version (support financed from wages) belongs to the transition paper (P2 in
  `../progress_and_prosperity/PLAN.md`).

## 5. The instance and the illustrations

The instance of Båge and Wilson (2026, Appendix B), set there from U.S.-like shares: N 1, T 0.01, h 0.0017, a 1.4,
b 0.4, λ 7.3, δ 0.05, ρ 0.09, γ(x) = 0.01 + 0.99x^4.4, χ uniform on [0, 2.2]; with θ = Δ = 0 it is that paper's
equilibrium (x* 0.82987, participation 0.602). A probe on 2026-11-16 (not committed; `code/model.py` reproduces and is
the only source for quoted numbers) found: output per hour 5.01 at θ = 0 and 3.72 at θ = 1; elasticity −0.589 at the
baseline; ceilings T/(hN_∞) reached along η ↓ 0; growth of output per hour per unit of log(1/η) → 1 at θ = 0 and → 0
at θ > 0; at θ = 1 a fall in ρ from 0.09 to 0.04 lowers w/r by about half with the margin fixed.

Figures planned from the model: output per hour and hours along a path of machine progress for funded exit, partial
enclosure, full enclosure and conditioned support (with the ceilings); the required return against w/r, w/P_s and the
price of land in hours, enclosed against funded.

## 6. Measurement (U.S. 1948–2025 spine; OECD for H-X)

Predictions are written here before the data are pulled. "Counts against" is what would make us drop or narrow the
claim. Classifications that can be argued run as a labeled grid; the reported object is the median with its min–max
band.

- **M1 — the eras.** FRED: OPHNFB (output per hour), HOANBS (hours), PRS85006173 (labor share), REAINTRATREARAT10Y
  (10-year real rate, from 1982) and DFII10 (TIPS, from 2003), HOOREVLMHMV and BOGZ1LM155012665Q (households' real
  estate and its structures: land's share = 1 − structures / real estate), CNP16OV and B230RC0A052NBEA (population),
  EMRATIO. Descriptive.
- **M2 — where the slowdown lives.** BEA GDP by industry (nominal value added and chain-type quantity indexes; the
  1947–97 historical file and the current release) and BEA NIPA hours of full-time and part-time employees by industry
  (Tables 6.9B, 6.9C, 6.9D, spliced at their overlap years at the sector level; self-employed hours not covered, said
  in the caption). Annual Törnqvist decomposition: g_{Y/H} = Σ s̄_i(g_{Y_i} − g_{H_i}) + Σ(s̄_i − h̄_i)g_{H_i}
  (value-added shares s̄, hours shares h̄; within-industry growth and the reallocation of hours). Eras 1948–73,
  1973–95, 1995–2004, 2004–19, 2019–last complete year. Era change against 1948–73 split exactly (midpoint weights)
  into within-industry slowdown, weight shift (Baumol) and hours reallocation, summed by class:
  - M machine-contestable: manufacturing, wholesale, transportation and warehousing, information, finance and
    insurance, professional and technical, management of companies;
  - S site- and resource-bound: agriculture, mining, utilities, construction;
  - H human-required, in person: education, health care and social assistance, arts and recreation, accommodation and
    food, other services.
  Grid: G1 baseline (retail and administrative services in M; real estate and government out); G2 retail and
  administrative services in H; G3 utilities in M; G4 government in H; G5 real estate in S (its owner-occupied
  value added has no hours, so G5 overstates S's productivity level); G6 accommodation and food in S.
  *Prediction:* the weight-shift and reallocation terms are negative in 1973–95 and 2004–19 and together account for
  at least a quarter of the slowdown against 1948–73 in the median member. *Counts against:* a tenth or less, or a
  positive sign. Between: partial.
- **M3 — pay against productivity.** FRED: OPHNFB, HCOMPBS, IPDNBS, PRS85006173, CPIAUCSL, CUUR0000SA0L2 (CPI less
  shelter). Identity: (real pay per hour)/(output per hour) = labor's share × P_Y/P_C. Windows 1973–2024 and 1983–2024
  (the CPI's owner-occupied housing method changed in 1983). *Prediction:* log(P_C/P_Y) rises, and using CPI less
  shelter removes at least a third of that rise. *Counts against:* less than a tenth. Descriptive alongside: CPI less
  energy, less medical care.
- **M4 — the hours that did not fall.** Penn World Table (average annual hours per worker; persons engaged;
  population), U.S. against Germany, France, the U.K., the Netherlands and Sweden, 1950–last year. Descriptive, with
  one mapping: the output-per-hour level implied by Lemma 1's elasticity if U.S. hours had followed (a) their own
  1950–80 trend or (b) the European path, labeled an unattributed envelope with ε from the instance and the range
  [−1, −0.4].
- **M5 — 2019 onward.** FRED: OPHNFB, HOANBS over CNP16OV (hours per person 16+), AHETPI over CES0500000003
  (production and nonsupervisory pay over all employees' pay, a compression index). *Counts against:* faster output
  per hour with rising hours per person and no compression.

## 7. H-X — the cross-country test (frozen by this commit)

- **Claim tested.** A necessary implication of absorption dominating across countries: where hours per working-age
  person grew faster, output per hour grew more slowly.
- **Data.** OECD Productivity Database (GDP per hour worked at constant prices and PPPs; total hours worked) and
  OECD population aged 15–64. If the OECD source cannot be reached or validated, stop and report; no substitute
  source is used without her decision.
- **Sample.** OECD members with complete annual data 1995–2019, excluding Ireland (multinationals' accounting moves
  GDP from 2015) and Luxembourg (cross-border commuters). The end year 2019 avoids the pandemic.
- **Variables.** g_π: annualized log growth of GDP per hour worked, 1995–2019. g_h: annualized log growth of hours
  worked per person aged 15–64, same window. Control: log GDP per hour in 1995 (catch-up).
- **Primary.** OLS g_π = α + β g_h + γ log π_1995 + ε, HC1 standard errors. Absorption predicts β < 0.
- **Secondary.** Five-year panel (1995–2000, 2000–05, 2005–10, 2010–15, 2015–19), country and period fixed effects,
  standard errors clustered by country (wild cluster bootstrap, Webb weights, 9,999 draws). β < 0 predicted.
- **Robustness, pre-declared.** Leave one country out (report any sign flip and the country); division bias (hours
  sit in both variables): the same regression with g_h from Penn World Table hours as an instrument for the OECD
  measure, if PWT is reachable.
- **Decision rule.** Consistent: β < 0 with two-sided p < 0.05 in the primary and the same sign in the secondary.
  Counts against: β > 0 with p < 0.05 in the primary. Otherwise uninformative.
- **What it cannot show.** β mixes supply shifts (absorption: negative) with technology and demand shocks (positive);
  a negative β is necessary for the account, not an estimate of the causal elasticity. Its size is compared with
  Lemma 1's elasticity only as an order of magnitude.

## 8. Rivals and what tells them apart

| Account | Says the slowdown is | Distinguishing evidence here |
|---|---|---|
| Exhausted opportunities (Gordon 2016; Cowen 2011; Bloom, Jones, Van Reenen and Webb 2020) | within industries, broad | M2: within term carries it, composition small |
| Mismeasurement (Byrne, Fernald and Reinsdorf 2016; Syverson 2017) | an artifact of prices | not tested; Syverson's evidence cited |
| Secular stagnation, demand (Hansen 1939; Summers 2014; Eggertsson, Mehrotra and Robbins 2019; Mian, Straub and Sufi 2021) | weak demand at the lower bound | Proposition 3 gives low rates a supply-side reading; M1 |
| Market power (De Loecker, Eeckhout and Unger 2020; Philippon 2019) | rents from markups | rents here are on fixed inputs; markups are institutional rents in the same accounting |
| Baumol, structural change (Nordhaus 2008; Vollrath 2020) | composition | Lemma 3 is the fixed-input version; M2 measures it |
| Housing constraints (Hsieh and Moretti 2019, magnitude disputed; Glaeser and Gyourko 2018) | spatial misallocation | Proposition 2: land per basket sets the ceiling |
| Labor reforms and productivity (Dew-Becker and Gordon 2012; Bourlès and Cette 2007) | employment composition | H-X re-measures it; Proposition 1 is the mechanism |

## 9. Risks and limits

- Cost disease is well trodden; the employment–productivity trade-off has earlier evidence. The novelty is one
  mechanism behind the faces, and Proposition 2.
- How many hours are forced rather than chosen is not measured; θ is not estimated. Absorption is a mechanism, an
  envelope (M4) and a necessary-implication test (H-X).
- The ceiling needs σ < 1 between machine-made and bound goods (Lemma 3); housing's share of U.S. consumption is
  roughly flat, so the bound side is mostly health, education and other in-person services, with housing land-bound.
- After 2004 the computer-producing industries slowed too (Fernald 2015); the account does not explain the frontier.
- Proposition 3's magnitudes depend on land's share of machine cost and on the return required on capital, which fell
  much less than safe rates (Caballero, Farhi and Gourinchas 2017); the paper states elasticities, not a number.
- Europe works fewer hours and still slowed after 1995; H-X and M4 meet this directly.

## 10. Literature to engage (each checked against Crossref before submission)

Keynes 1930; Robinson 1936; Hansen 1939; Habakkuk 1962; Baumol 1967; Solow 1987; Jorgenson 1988; Bruno and Sachs
1985; Ngai and Pissarides 2007; Nordhaus 2007, 2008; Allen 2009; Acemoglu 2010; Cowen 2011; Summers 2014; Rognlie
2015; Fernald 2015; Byrne, Fernald and Reinsdorf 2016; Gordon 2016; Syverson 2017; Caballero, Farhi and Gourinchas
2017; Knoll, Schularick and Steger 2017; Glaeser and Gyourko 2018; Hsieh and Moretti 2019 (and Greaney 2026, the comment on its
magnitude); Eggertsson, Mehrotra and Robbins 2019; Philippon 2019; Bloom, Jones, Van Reenen and Webb 2020; De
Loecker, Eeckhout and Unger 2020; Vollrath 2020; Mian, Straub and Sufi 2021; Brynjolfsson, Rock and Syverson 2021;
Goolsbee and Syverson 2023; Autor, Dube and McGrew 2023; Dew-Becker and Gordon 2012; Bourlès and Cette 2007;
Davis and Heathcote 2007; Deaton and Laroque 2001; Warren and Tyagi 2003; Prescott 2004; Goldin 2006; Stansbury and
Summers 2017; Acemoglu and Restrepo 2018; Båge and Wilson 2026.

## 11. Units and breakpoints

1. This spec (committed first: the H-X freeze).
2. Theory: `code/model.py`, `checks/check_theory.py`, the theory figures, Sections 3–4 and Appendix A of
   `paper/main.tex`. **Breakpoint: her read of the spec and the theory together.**
3. Data and figures: M1–M5 and H-X, each with its check.
4. The full draft, references checked, an independent review (maths, data, a referee read), the compiled PDF.

## Amendments

- 2026-11-16, no outcome data seen (none pulled): citations only, nothing tested changes. Dew-Becker and Gordon
  cited as published (Review of Economics and Institutions 3(2), 2012) instead of the 2008 working paper; the
  comment on Hsieh and Moretti named (Greaney 2026, AEJ: Macroeconomics 18(2)), verified the same day.
- 2026-11-16, no outcome data seen (none pulled): Section 4 restated as the paper now states its results, after an
  independent review of the theory (`../STATE.md`, Log): funding made a separate condition of equilibrium; Lemma 1
  at fixed T and h; the density conditions F needs; Proposition 2(iv) an elasticity across stationary states, not a
  growth rate; Proposition 3(ii) new (prices fall whoever can leave work); Lemma 2 on price requirements; Lemma 3(b)
  new; the welfare remark withdrawn. M4's mapping from hours to output per hour (Section 6) uses Lemma 1 and so holds
  technology, land and the basket fixed: it remains an envelope. Nothing in H-X changes.
- 2026-11-16, M2's data source, changed before any M2 outcome was computed (the files' structure seen, no values):
  BEA's NAICS-based GDP-by-industry history for 1947–96 is not where the spec expected it (BEA now lists only
  SIC-based history), and NIPA hours cover employees only. M2 therefore uses the BEA–BLS integrated industry-level
  production account, published by BEA: the 1947–2016 research tables' underlying data (Eldridge et al. 2020;
  nominal gross output and intermediate inputs, their quantity indexes, total hours of all workers) and the
  1997–2024 release (nominal value added, value-added and labor-hours quantity indexes). Real value added by
  double deflation; the vintages spliced at 1997 (hours levels carried forward by the newer hours index); the last
  era becomes 2019–2024. Sectors, classes, the grid G1–G6, the decomposition and the thresholds are unchanged.
- 2026-11-16, logged late (found by the referee read): when Section 4 was restated after the theory review (db7daad,
  10:44 UTC, before any outcome data were pulled), the thesis sentence of Section 1 changed with it, from "measured
  productivity grows at the pace of machine progress" to "measured productivity eventually rises in proportion to
  machine capability", to match Proposition 2(iv) as proved. The amendment above did not mention it.
- 2026-11-16, after the measurements were computed (outcome data seen); no prediction, threshold, window, source or
  verdict changes. Added, each labeled in the paper as a check or reading made after the data were seen: X1, the
  baseline without agriculture, read by the same thresholds; a comparison of BEA's two files over their overlap and the
  2004-16 shares on the older file alone; BLS's January population-control steps, smoothed as a sensitivity for hours
  per person; the dependence of M4's envelope, as a share of the slowdown, on the windows compared (the planned report,
  the level effect, unchanged); labor's share on decade averages beside the planned endpoint comparison. Descriptive
  numbers the text quotes were added to the scripts' outputs (class shares of hours and value added, sector pieces of
  the within and reallocation terms, Lemma 1's bound on the swing in hours per person between 1948-73 and 1973-95,
  Europe's and America's slowing of the fall in hours). Two descriptions corrected after the independent data review:
  M5 carried only a condition that would count against the account, not a prediction, and the paper now says so;
  the plan's M3 fact F2 says "typical pay", but M3 as specified uses average hourly compensation, and the paper says
  that the gap for the typical worker is wider.
