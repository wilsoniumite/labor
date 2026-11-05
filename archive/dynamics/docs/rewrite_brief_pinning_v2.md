# Rewrite brief: *Pinning the Wage to Scarcity and Technology*, v2

**Provenance:** drafted in Stella's review conversation of 2026-08-27 and
delivered to this thread the same day; frozen here per the v1-brief
precedent (`rewrite_brief_pinning.md`). Her amendments on delivery, which
override the workflow section where they conflict:

1. **Two versions, sequentially.** First the notation-only version
   (executed 2026-08-27 — `notation_map.md`, STATE log 31), committed
   alone. Then the dynamics rewrite, on her go.
2. **Sequencing:** the λ input–output splice and the Swedish-fork fold-in
   do NOT gate the start (her call); the SSRN revision does not wait for
   the rename. Overleaf was confirmed up to date at the start.
3. **Voice:** the redraft is expected to need many voice passes; the
   standing protocol (Claude drafts, she re-voices via Overleaf, ports
   ride back) applies throughout.

The body below is the brief as delivered, verbatim.

---

This brief carries the decisions and plan from the review conversation into the repo. Start with Phase 0. Do not begin content edits until the notation commit builds clean.

---

## 0. Diagnosis and target

v1's contribution is Proposition 2 (pricing the machine rental off its own recipe and substituting into the task margin, so the wage is a claim on terminal rents) and Proposition 4 (the real-wage fork). Four things hold it back.

1. **The two-category rhetoric is not supported by the model.** "Machine-made goods" versus "land-priced services" reads as a split between goods that contain land and goods that don't. Appendix B's Prop B.1 shows every good resolves to land rent. Once `w = c·γ*` closes the wage, every price is `r` times a technological coefficient. The real content is a coefficient statement: each good has a terminal coefficient, the wage has one, and the real wage in a good is the ratio. Caselli–Manning is the case where the two coefficients co-move; the fork is the case where the good's coefficient is bounded below.
2. **The participation condition nets rent on one side.** It compares a gross goods wage `w` with a keep net of land, `s₀ − q·hₑ`. Prop 4(iii) already prices the worker's basket with a land share; Props 3 and 5 drop it. With both lives priced, `q` drops out of the housing terms and Prop 3(iii)'s "rising q erodes exit and expands supply" is entirely the asymmetry. What survives is a rigidity claim (exit needs a specific plot, work can economize) and a funding-source claim (a land-funded exit holds its value; a wage-funded one shrinks).
3. **Interest income is a footnote and isn't one.** "All non-wage income is site rent" is a ρ = 0 result. With ρ > 0 machine owners collect ρ times the stock's value; the stock is land-bounded so this scales with `rT`, but the ratio can be large. Free entry competes away pure profit on datacenters, not the normal return, and Section 12 lists datacenters as if they were sites.
4. **"Horizon-terminal" is informal, and the empirics illustrate rather than discriminate.** The horizon sentence ("transformer capacity is terminal over five years and produced over twenty") needs a parameter. Figure 3 as drawn is the goods-versus-services fork with the most extreme goods deflator, consistent with Baumol-in-construction and zoning as much as with land.

v2 fixes all four with one move and its consequences: **capital is time.** Waiting time (ρ, Böhm-Bawerk/Sraffa) gives the interest identity. Build time (J, Kydland–Prescott) formalizes horizon-terminality, gives the transition its results, and gives the empirics a cross-sectional design (coefficient rigidity = build time of the good's terminal inputs; land is J = ∞).

---

## 1. Decisions already made — do not relitigate

- **Rebuild this paper**, not a sequel. The dynamics replace v1's Sections 9 and 11; the fiscal transition material in Appendix C becomes derivable instead of deferred.
- **Rename the schedule** `ρ(x) → γ(x)`. Accepted by Stella.
- **Discrete time.** Appendix A already compounds with `(1+δ)`; Kydland–Prescott is discrete.
- **Exogenous interest rate ρ**, small open economy in capital (investment financed at the world rate), closed in land and labor. This is the Caselli–Manning fixed-interest-rate premise and should be named as such. Households consume current income each period with Cobb–Douglas shares (goods, land services). Closed-economy intertemporal optimization is a listed extension, not the baseline.
- **MIT shock, perfect foresight after.** Unanticipated permanent fall in `γ̄` (flat case) or downward shift of `γ(·)` (sloped case).
- **Preferences:** Cobb–Douglas goods/land (σ = 1) as baseline; CES with elasticity σ as the extension that reads the sign off shelter shares.
- **One machine type in the main text; matrix form in Appendix A.** For the waterfall result, two produced inputs (chips, power) plus land.
- **Sloped regime is numerical.** Flat regime first, possibly closed form.
- **Notation is final as in Section 2 below.**

---

## 2. Notation

### 2.1 Changes

| Object | v1 | v2 | Reason |
|---|---|---|---|
| Rent tax, payroll tax | τ, t | `τ_R`, `τ_w` | `t` is time; parallel pair |
| Time preference, depreciation | δ, d | `ρ` (discount rate = interest rate, exogenous), `δ` | field standard; user cost `(ρ+δ)` |
| Productivity schedule | ρ(x), ρ̄, ρ* | `γ(x) = γ_L(x)/γ_M(x)`, `γ̄`, `γ*` | frees ρ; consistent with the γ_L, γ_M family and close to A-R's own γ(i) |
| Land coefficient, scalar / matrix | ℓ / B | `b` / `B` | ℓ reads as the Leontief labor coefficient; pair now consistent |
| Human-essential task set, measure, wage | K, k, w_K | `H`, `|H|`, `w_H` | frees K for the machine stock |
| Wage-linked shares (consumption, revenue) | λ_C, λ_R | `φ_C`, `φ_G` | λ is the recipe coefficient; G for government since R is rent |
| CES elasticities (two contexts) | η, η | `σ` (goods vs land), `σ_H` (H-content vs substitutes) | field: σ is the elasticity |
| Land expenditure weight / realized share | σ / sh(q) | `α` / `α(q)` | field: α is the Cobb–Douglas share; here land is the non-labor factor; ends the sh vs h_s clash |
| Uniform transfer | u | `d` (the dividend) | u reads as unemployment or utility |
| Dependency floor | s_d | `s̲` (underbar) | frees d; pairs with s₀ |
| Broadcastable fraction (D.3) | β | `ψ` | keep β free |
| Goods price | p_g | `p` (numeraire, p = 1) | dynamic subscripts |
| Participant count (Lemma A.1) | n | `N_a` | frees n |
| Produced-price and rent vectors | c, r | bold **c**, **r** | standard |

### 2.2 New symbols

| Object | Symbol | Source |
|---|---|---|
| Machine stock (capacity) | `K_t` | field |
| Gross investment, units started at t | `I_t` | field |
| Build lag of input j; land has J = ∞ | `J_j` | Kydland–Prescott |
| Build recipe per unit of I | `(a_I, λ_I, b_I)` | subscript; the existing `(a, λ, b)` is the operating recipe per unit of service, unchanged in meaning |
| Build cost | `p_K = a_I c + λ_I w + b_I r` | field |
| Capacity constraint | `X_t ≤ K_t` | |
| Net rental per unit of stock | `π_t = c_t − a c_t − λ w_t − b r_t` | |
| Tobin's average Q for installed stock | `Q_t` | Hayashi |
| Total (reduced) terminal coefficient of good j, of a machine service, of the wage | `θ_j`, `θ_c`, `θ_w` | Leontief total requirements; `b` is the direct one |
| Work-life land requirement | `h_w` | parallels `h_e`; the participation fix |
| Terminal coefficient of the exit's funding source | `θ_e` | |
| Subsistence bundle | `(g_s, h_s, n_s)` | `n_s` replaces `k_s` |
| Identity matrix | `𝟙` | since I is investment |

### 2.3 Unchanged, with notes

`x, x*, γ_L, γ_M, c, w, N, a, λ, Λ, A, T, T_j, T_P, T_H, R, ω_ij, μ(x), ε_D, ε_S, κ, q*, q_enc, m_w, m_e, v, f, z, r(z), X, Y, L̄, P, P_s, i, j.`

- `r` stays rent, `R` aggregate rent. One sentence at first use: interest is ρ, not r.
- `s` stays the outside option. Footnote: this is the priced object the paper builds, not DMP's parameter b.
- `q = r/p` stays. `Q_t` is Hayashi's average Q for machines; say so once.
- `λ` still collides with A-R's substitution elasticity; keep that footnote. The ρ̂ collision disappears.
- `L̄` is paper-specific; define once, prominently.

### 2.4 Propagation

- Write `notation_map.md` (old → new, with context notes for ambiguous cases such as δ→ρ and d→δ). Use it for the sed pass, the Lean translation table, and the appendix notation table.
- Regenerate Figures 1 and 2 (axes and labels).
- Update sympy check files and the Lean assumption manifest; Lean identifiers may stay internal, but the paper-to-Lean translation table must use v2 symbols.
- Replace the data note's collision paragraph with a one-page notation table in the appendix.

---

## 3. The model, v2

### 3.1 Static core on the coefficient footing

- Tasks `x ∈ [0,1]`, Leontief over tasks; `γ(x) = γ_L(x)/γ_M(x)`, relabeled increasing; `w = c·γ*` at the margin (Prop 1, unchanged in content).
- **Steady-state recursion** (nests v1 as the zero-build-recipe, J = 1 case):

  `c = a c + λ w + b r + u_K · p_K`, `p_K = a_I c + λ_I w + b_I r`, `u_K = (ρ+δ)(1+ρ)^{J−1}`

  Solve with `w = c γ*`:

  `θ_c := c/r = [b + u_K b_I] / [1 − a − λγ* − u_K(a_I + λ_I γ*)]`, `θ_w := w/r = γ* θ_c`.

  Viability: denominator > 0. Task automation lowers γ*; recursive automation lowers λ and λ_I.
- **Total coefficients.** For any good j with a task list, `θ_j = (machine-hours per unit)·θ_c + (labor-hours per unit)·θ_w`. Direct coefficients (`b`, `b_I`) are what a process uses; total coefficients are what its price resolves to. Use the Leontief direct/total language explicitly.
- **Real wage in good j** is `θ_w/θ_j`. Caselli–Manning: invariant whenever `θ_j ∝ θ_w` (goods produced by the same machines). Fork: `→ 0` whenever `θ_j` is bounded below because land is the thing consumed, not an input. Pure location is the `θ = 1` endpoint; ideas are `θ = 0`; housing, energy, food sit in between and should be placed there, not bundled with shelter.
- **Flat limit.** `θ_w/θ_p = 1/L̄` (CM restated: a guarantee denominated in goods whose terminal content is going to zero). `r/p = 1/θ_p` with `θ_p = γ̄ L̄ θ_c`.
- **Interest identity (new proposition).** In steady state with full use, `X = K` bounded by land; capital income `= ρ p_K K`; national income `= wN_a + rT + ρ p_K K`; state the interest-to-rent ratio in closed form as a function of `(a, a_I, λ, λ_I, b, b_I, γ*, ρ, δ, J)`. Say when it is small. This is where Moll–Rachel–Restrepo belongs.

### 3.2 Participation, both lives priced

- Work: income `w`, land requirement `h_w`. Exit: income `s₀` from a source with terminal coefficient `θ_e`, land requirement `h_e`, dependency floor `s̲`.
- Condition: work iff `w − q h_w ≥ max(s₀ − q h_e, s̲)`.
- Results to state:
  1. With `h_w = h_e`, `q` cancels; in the flat limit both sides are constant in goods and technology does not move participation.
  2. Rigidity version: under Cobb–Douglas, the working life's value degrades as `q^{−α}` (this is Prop 4(iii)); an exit with rigid `h_e` hits zero at `q = s₀/h_e`. This is the enclosure mechanism, now stated as a claim about `h_e` rigid and `h_w` flexible, with the historical and modern signs discussed (plot vs tenement then; location-rigid work now).
  3. Funding source: `s₀ = θ_e r`. A plot's output is a land claim and holds; a parent's wage is a `θ_w` claim and shrinks with the child's; a wage-funded transfer shrinks; a rent-funded transfer does not.
- Prop 5 restated: the dividend `d = τ_R R/N` is a land claim; beyond the cancellation `w + d ≥ s + d`, it is the only outside option whose coefficient does not shrink under automation.

### 3.3 New-task margin, formalized

New tasks arrive with `γ` drawn from a distribution `F_t` whose support collapses toward `γ̄` as capability generalizes. State the sufficient condition under which reinstatement is a transitional stabilizer and the flat limit still arrives. Engage Autor, Chin, Salomons and Seegmiller (2024) as the empirical counterpart. This replaces the clause that currently shuts the margin by assumption.

### 3.4 Waiting time

Read Appendix A's `c = b r (1+ρ)/(1 − a(1+ρ))` as Sraffa's reduction to dated land summed as a geometric series. Capital is the interval between when terminal inputs are applied and when output arrives, priced at ρ. This is what makes the interest identity an accounting statement rather than a separate claimant.

### 3.5 Build time: the dynamic model

Periods `t = 0, 1, …`. Goods numeraire `p = 1`, so `q_t = r_t`.

**State and timing**
- `K_t` installed at the start of t. `I_t` started at t, usable at `t + J`. `K_{t+1} = (1−δ) K_t + I_{t+1−J}`.
- Services `X_t ≤ K_t`, one unit of service per unit of stock per period.
- Operating recipe per unit of service: `(a, λ, b)`. Build recipe per unit started, paid at start: `(a_I, λ_I, b_I)`. (Spreading build inputs over J periods is a listed variant.)

**Prices and margins**
- Task margin `w_t = c_t γ(x*_t)` when both inputs are used.
- Final-good zero profit: `1 = c_t ∫₀^{x*_t} dx/γ_M(x) + w_t ∫_{x*_t}^1 dx/γ_L(x)`.
- Net rental `π_t = c_t − a c_t − λ w_t − b r_t`. If `X_t < K_t`, `π_t = 0`. If `X_t = K_t`, `c_t` clears the services market.

**Quantities**
- Services: `X_t = Y_t ∫₀^{x*_t} dx/γ_M + a X_t + a_I I_t`.
- Labor: `N_{a,t} = Y_t ∫_{x*_t}^1 dx/γ_L + λ X_t + λ_I I_t`.
- Land: `T = b X_t + b_I I_t + α · Inc_t / r_t`, with `Inc_t = w_t N_{a,t} + r_t T + π_t K_t` (net of taxes and plus transfers where the fiscal block is on).
- Goods: `Y_t = (1−α) Inc_t` (households consume income; investment is financed abroad at ρ).

**Investment (free entry, perfect foresight)**
- `p_{K,t} = a_I c_t + λ_I w_t + b_I r_t ≥ Σ_{s ≥ t+J} (1+ρ)^{−(s−t)} (1−δ)^{s−t−J} π_s`, with equality if `I_t > 0`.
- `Q_t = [Σ_{s ≥ t} (1+ρ)^{−(s−t)} (1−δ)^{s−t} π_s] / p_{K,t}`.
- Steady state: `π = (ρ+δ)(1+ρ)^{J−1} p_K`, which is the recursion in 3.1.

**Shock and solution**
- At t = 0, unanticipated permanent fall in `γ̄` (flat) or shift of `γ(·)` (sloped). Perfect foresight thereafter.
- Flat case: `c_t = 1/(γ̄ L̄)` is pinned while labor is employed, so the system reduces to a difference equation in `K_t` with `r_t` from land clearing and `I_t` from free entry. Check for a closed form before going numerical.
- Sloped case: extended-path / time iteration. Guess `{r_t, w_t, x*_t}` on a long horizon, compute forward-looking `I_t` from free entry, simulate `K_t`, compute clearing residuals, update, iterate to convergence. Verify horizon-length insensitivity.
- Waterfall: two produced inputs `j ∈ {chip, power}` with `(K_{j,t}, J_j, δ_j)`, an operating recipe that uses both services, land as the third input. Report the paths of `π_{j,t}` and `r_t`.

### 3.6 Target propositions and their status

Mark each in the draft with its status until the numerics settle it. Do not promote a conjecture to a claim before the check runs.

1. **Windfall, then transfer.** On impact the installed stock earns `Q_0 > 1`; the quasi-rent is the PV of `π_s` above its steady-state value over the build window; it decays as capacity arrives and the released value settles on land. In goods, `w/p = 1/L̄` throughout while labor is employed (CM holds on the path). In land units `w/r` falls on impact and keeps falling. *Status: expected; verify flat, then sloped.*
2. **The waterfall.** With inputs ordered by `J_j`, value passes through them in order, each holding it for roughly its build time; land holds it permanently. *Status: expected; verify with two inputs.*
3. **Speed and distribution.** Transitional value captured by produced capital scales with the speed of the capability change times the gestation lags. Slow automation is Georgist; fast automation with long build times is Piketty for the duration of the crossing. *Status: expected; derive the comparative static on shock duration.*
4. **The fiscal horizon.** A quasi-rent on stock in place is a sunk windfall and taxable without distortion; the same tax anticipated on new capacity deters the build. Input j is a clean base over `J_j` for existing stock only, with a time-consistency problem; land is the only base clean at every horizon. *Status: theorem-shaped; prove in the model.*
5. **Sloped-regime wage path.** Capacity shortage pushes labor onto tasks it is worse at; goods wage may fall on impact and rise as capacity arrives while the land wage falls throughout, so AI's wage effect arrives with the buildout rather than the model release. *Status: conjecture; numerics decide.*
6. **Interest identity** (3.1) and **participation invariance** (3.2). *Status: algebra; sympy and Lean.*
7. **New-task condition** (3.3). *Status: algebra.*

---

## 4. Structure of the paper, v2

| § | Title | Job |
|---|---|---|
| 1 | Introduction | Lead with the coefficient statement ("the wage is a coefficient on non-produced inputs, and automation shrinks it"), then time (waiting, build), then the fork, then the fiscal horizon. Numbers only after the multi-leg fork is recomputed. |
| 2 | What standing accounts pin the wage to | Keep the "what does each account terminate in" framing; cut length by a third; tone down "we supply both endpoints" to "we price both endpoints and show one is q-invariant under symmetric housing." |
| 3 | Tasks and the margin | γ notation; Prop 1; Lemma A.1's monotonicity now stated as coming from the land bound. |
| 4 | The recursion: direct and total coefficients | b and θ; Prop 2 restated; waiting time and the interest identity. |
| 5 | Build time | J; the dynamic model; horizon-terminality as a parameter. |
| 6 | The floor | Participation with both lives priced; enclosure as a rigidity claim; funding source. |
| 7 | The fork as coefficient ratios | CM restated; the θ gradient from ideas to location. |
| 8 | Transition results | Windfall, waterfall, speed × lag; figures. |
| 9 | Fiscal | The horizon theorem; rent tax and dividend; transition bases now derived. |
| 10 | Measurement | Coefficient rigidity across goods; shelter decomposition; energy leg; cross-country; κ as order of magnitude. |
| 11 | AI | Dated predictions: chip rents shortest-lived, power longer, land permanent; model weights as ideas. |
| 12 | Conclusion | Short. |
| A | Environment and equilibrium | Matrix form with 𝟙; existence claims scoped as now; numerical method. |
| B | Land-only closure | With interest; B.1 restated. |
| C | Fiscal transition | Derived, not deferred; ledger and figures. |
| D | Human-essential tasks | H notation; unchanged content. |
| E | Numerical methods and check files | New. |
| F | Data and notation | Data note plus the one-page notation table. |

v1's Section 9 (history) survives as one subsection of §7 or §8: the three configurations become three parameterizations (industrial: high λ, long-J engines; computing: short-J chips at the simple end; AI: both channels). v1's Section 11 (stabilizers) becomes a short subsection of §9: quantity protections with their own J.

Title: keep, or *Pinning the Wage to Scarcity, Technology, and Time*. Authors' call.

---

## 5. Empirics plan

Data rule (Stella's): pull live from public sources, log the pull, keep it reproducible. If a source fails (timeout, JS page, blocked domain), **stop and report**. Do not substitute a secondary source or fill the gap.

1. **Fork, multi-leg.** Add deflators: nondurables, all goods, energy, non-shelter services (medical care, tuition, personal care services). Add a total-compensation series alongside AHE production/nonsupervisory. State that durables CPI is hedonically adjusted. Expect: energy near the shelter side; medical and tuition faster than shelter, which is the Baumol signal and must be discussed. Do not anchor on 4.8×.
2. **Shelter decomposition.** Land versus structure (Davis–Heathcote; Lincoln Institute land-price series; KSS already cited). The land leg is the model's leg; the structure leg is a high-λ construction sector.
3. **Cross-country.** KSS / Jordà–Schularick–Taylor macrohistory house-price and land data, 14 countries. Japan is the test of the N channel. [Note, 2026-08-27: the Swedish fork is already built — `code/swedish_fork.py`, data item four — and is this item's first leg.]
4. **Gestation lags for calibration.** Fab construction and permitting times; interconnection queue durations (LBNL "Queued Up"); datacenter build times; EIA plant construction times. Cite each; illustrative, not estimated.
5. **κ.** Keep; present as order of magnitude with the band; note the cap-rate sensitivity and the post-1995 Z.1 residual issue.
6. **Open, unless cheap:** payroll-incidence assembly on a common pass-through definition; the λ input-output series. [Note, 2026-08-27: the λ series is BUILT — progress_and_prosperity λ thread, gate PASSED, §10 splice-ready; whether/when it lands in the paper is Stella's sequencing call.]

---

## 6. Computation

**sympy.** Verify: the steady-state recursion with the build recipe; θ_c, θ_w and their comparative statics in γ*, λ, λ_I, J; the interest-to-rent ratio; the fork with the build recipe; participation invariance under h_w = h_e; the new-task condition.

**Lean.** Rename via the translation table. Add the interest identity and participation invariance if they formalize cleanly. Do not formalize transition paths; state that boundary in the verification note.

**Numerics.** Python, per Stella's conventions: functions, no classes; notebook-cell style that moves into an importable `.py`; `from tqdm.auto import tqdm` on any outer loop that may run more than a few seconds. Suggested layout: `dynamics/model.py` (recipes, clearing, free entry), `dynamics/solve.py` (flat closed form or shooting; sloped time iteration), `dynamics/figures.py`, plus one notebook that runs the paper's cases. Every figure regenerable from one entry point.

---

## 7. Workflow

**Phase 0 — inventory.** Read the repo: tex, figure scripts, sympy checks, Lean project, data scripts. Confirm the build commands for PDF, checks and Lean. Write `CHANGELOG.md`. Keep the v1 PDF as `paper_v1.pdf` for reference and latexdiff. [Executed 2026-08-27 with repo-native instruments: STATE.md is the changelog; the word-fidelity gate and `word_diff_report.py` replace latexdiff; v1 is frozen as the pre-notation git commit.]

**Phase 1 — notation.** Apply `notation_map.md`; regenerate figures; update checks and the Lean translation table; build; latexdiff against v1 to confirm only symbols changed. **Commit this alone** so content diffs stay readable. [Executed 2026-08-27; STATE log 31.]

**Phase 2 — static rewrite.** §§3, 4, 6, 7 on the coefficient footing; participation fix; interest identity; new-task condition. sympy and Lean updated. Build. Commit.

**Phase 3 — dynamics.** Flat case (closed form if it exists), two-input waterfall, sloped case. §§5, 8, 9. Figures. Promote or demote each target proposition by result. Commit.

**Phase 4 — empirics.** §10 and Appendix C/F. Commit.

**Phase 5 — prose and structure.** Style pass (Section 8), structure checklist, abstract, AI-use note, title decision. Build final.

**Review packets for Johan** at the end of Phases 2, 3, 4 and 5: one page with *What changed / Why / Where to look (page refs) / Questions for you*, plus the PDF and a latexdiff where useful. Keep Johan's replies in `review/` and resolve each in the changelog.

**Decisions for Johan** (raise at Phase 2 packet): target venue; keep or drop the Lean development; open- vs closed-economy baseline; whether the sloped-regime dynamics sit in §8 or Appendix E; the AI-use note wording and the venue's policy on AI-drafted prose.

---

## 8. Style and claims discipline

v1's prose was Claude-drafted and it shows. Rules for the redraft:

- Em-dashes: at most one per paragraph; prefer none. Use commas, colons, or a second sentence.
- No paragraph-final aphorism that restates the paragraph. If the last sentence adds no new information, delete it.
- "X, not Y" antithesis at most once per section.
- No sentence fragments; no comma splices; check subject–verb agreement ("Sections 9–10 apply").
- Vary sentence length. Long declarative chains read as mannered.
- Define every symbol at first use and only there; the notation table is the second place, and the only other.
- Avoid "genuinely", "honestly", "straightforward".
- Propositions state their assumptions inline, mirroring the Lean assumption manifest.
- Classify every claim as theorem, numerically verified, or conjecture, and keep the label in the text until the status changes.
- Empirical claims are illustrative until a discriminating test is in; say so.
- Abstract: "changes no work–exit choice" becomes "moves no participation margin, up to an income effect"; "which the program-evaluation literature puts near zero" becomes an accurate summary of Hoynes–Rothstein and the NIT experiments (modest, nonzero, larger for secondary earners; Alaska's dividend is an order of magnitude below a subsistence floor).
- AI-use note: two authors ("the authors'"); accurate description of what was drafted by whom; check the target venue's policy.

**Structure checklist (run before each packet):** every section has one stated job and does it; propositions numbered continuously with no orphan lemmas; every symbol in the table; every figure referenced in text; every appendix referenced from the main text; no result asserted in the introduction that the body does not deliver; the fork's headline number matches the recomputed figure.

**Language checklist (grep-able):** count em-dashes per page; flag "not X but Y" and ", not " constructions; flag sentences beginning "What" or "That is"; flag paragraphs whose last sentence contains no symbol, number, or citation; run a grammar pass on fragments and splices.

[Note, 2026-08-27: where this section names checks the repo already mechanizes,
`checks/lint_pinning.py` is the authority — its ban families (register,
poetic, control-vocabulary, honest-family, presuppose patterns, em-dash
metrics) are a superset of the grep list above and must be carried into v2,
not replaced by it. The voice protocol also stands: Claude drafts, Stella
re-voices via Overleaf, ports ride back verbatim; her v1 voice-passed
sentences carry verbatim wherever their content survives.]

---

## 9. Carry-over fix list from the review

Nothing here should be lost in the rewrite.

- Interest income treated as a channel, with the identity in §4 and the speed × lag result in §8.
- Participation asymmetry fixed (§6); Aguiar–Bils–Charles–Hurst engaged; prime-age male participation trend acknowledged.
- New-task margin formalized (§3.3).
- "The interval" framing: either drop it or state precisely that "closes" means demand goes flat, not that ceiling meets floor.
- Lemma A.1: monotonicity comes from the land bound; say so.
- Fork empirics: hedonic caveat, added legs, shelter decomposition, cross-country.
- κ presented as order of magnitude.
- Hoynes–Rothstein / NIT summarized accurately.
- Abstract overclaims removed.
- Grammar: the fragment in §2 ("We do not offer the model … instead the objects at which they terminate"), "Sections 9–10 applies", comma splices in §2.3 and §11, the abstract's recipe sentence.
- AI-use note: singular/plural; venue policy.
- Section 2.6: MRR not dismissed in a clause.
- Section 12: datacenters are reproducible capital; the dated sequence replaces the flat list.
- Allen (2009) "Engels' pause" cited alongside Crafts (2022).
- Lean not oversold; the algebra is simple enough that sympy carries it.

---

## 10. Risks and considerations

- **Scope.** This is close to a second paper. Guard: the static rewrite (Phase 2) must stand on its own as a coherent paper before Phase 3 starts, so that if the dynamics stall the paper still ships.
- **Existence.** The dynamic sloped system with endogenous x*, land clearing and two stocks will not get an existence proof. Scope the claim as v1 does: closed form where it exists, numerical paths elsewhere, boundary stated in Appendix E.
- **Numerics credibility.** Report horizon-length insensitivity, convergence tolerances, and the steady-state check (the path must converge to the sympy-verified steady state). Ship the solver.
- **The flat case may be too clean.** If `c_t` pinned makes the flat transition trivial, that is itself the CM-on-the-path result; say so and lean on the sloped case for the wage-path claims.
- **Waterfall sensitivity.** The ordering result depends on `J_chip < J_power`; report it as an ordering by J, not by named input, and let calibration name the inputs.
- **Empirics may cut against the model.** If medical and tuition outpace shelter, the goods–services fork is mostly Baumol and the land claim must be carried by the land/structure decomposition and the cross-section. Write the section so it survives that outcome.
- **Journal policy.** Several venues restrict AI-drafted prose or require disclosure; settle this before Phase 5.
- **Reproducibility.** One entry point regenerates every figure and table from logged pulls.
- **What would falsify the strong scenario** (keep from v1 §12, sharpened): reinstatement replenishing γ faster than capability closes it; the machine-production network not shedding labor (λ, λ_I flat); land's share of housing value not rising in the cross-country data; quasi-rents on compute and power not decaying on the timescale of their build lags.
