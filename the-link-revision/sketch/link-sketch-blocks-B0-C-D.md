# The Split — working sketch, Blocks B.0′, C & D

**Status.** Companion to `link-sketch-blocks-AB.md` and `link-stress-test-1-blind-coding.md`. B.0′ folds the task anatomy into Block B carrying the stress test's four amendments; C and D are drafted together because the pilot showed the two anatomies are co-dependent classifiers. Numbering provisional. **Algebra/numerical pass completed 2026-08-09** (`../checks/check_anatomy.py`, `check_race.py`, `check_mu.py`); flags below record outcomes, one with an amendment (C1's stability condition is lag-indexed).

---

## Block B.0′ — the anatomy of a task

### B.0′.1 Dimensions, rays, transmission

Capability is a vector over dimensions (pilot list: FRC, PRS, UNS, PER, SYM-R, SYM-O, SOC with a co-present/remote sub-code; the paper imports O*NET's). A task engages a requirement profile and is performable by a single agent iff every engaged dimension is met — Leontief within the task. Machine capability advances as **rays**, one dimension at a time, of two types: *engineering rays* (FRC, PRS, SYM-R), which cross by design and need no corpus, and *learning rays* (PER, SYM-O, SOC, UNS), which cross only where machine talent τ meets recorded practice — **D gates learning rays only** (amendment 1). *Transmission technologies* (telegraph, internet, containers) are not rays: they move work products, entering the model only through the tradable-set indicator, the reach fraction, and the D(x) path — never through ρ.

### B.0′.2 Separability

Defined at the component-pair level (amendment 2). Two components are **separable** iff the *buffer test* (output of one can be stored or queued before the other acts) or the *narrow-channel test* (their coordination fits a low-bandwidth channel without degrading the deliverable) holds; **bundled** iff they demand one agent, one body, one real-time loop. Separability is **endogenous**: environment and process re-engineering — the assembly line, the container, the script — manufactures it, and manufactures D along with it; the investment is predictable wherever the wage bill is large. Two-stage demolition follows: standardize, then automate, with the wage decline starting at the scripting stage.

### B.0′.3 The reduced form, and what "task" means

The paper's continuum x ∈ [0,1] is reinterpreted as the space of **fragments under the prevailing decomposition**; ρ̃(x) is the scalar shadow of the vector structure, governed by the fragment's weakest machine dimension. Because separability is manufactured, the fragment space is time-varying: re-engineering redraws it. Everything aggregate still runs on ρ̃; the anatomy sits underneath as its microfoundation, which is why Assumption F's order claim (β·D first) is now derived rather than asserted.

### Proposition B.0′-1 (reinstatement, mechanized)

Every historical reinstatement event is fragment creation on an uncrossed dimension: partial automation of a *separable* task strands a residue — the driver's seat, the crane cab, the exception queue — which becomes a new human fragment on the dimensions machines haven't reached. Reinstatement capacity is therefore bounded by the set of engaged-but-uncrossed dimensions. When rays advance on all engaged dimensions at once, fragment creation has nowhere to land. **§10's branch two acquires a mechanism: reinstatement is not a countervailing force but a consequence of incomplete crossing, and it shuts down with completeness.**

Proof sketch: under Leontief-within-task, a residue fragment exists iff the crossed/uncrossed boundary is separable; its human tenure lasts until its own dimensions cross. ∎ [checked ✓ 2026-08-09, check_anatomy.py B0'1-MEAS: formalized as a measure change on the fragment space — labor bookkeeping exact at every crossing, residues created iff the boundary is separable and the crossing partial, human measure exactly zero and fragment creation exactly zero at completeness.]

### Proposition B.0′-2 (continuous vs punctuated transmission)

At a separable boundary, machine progress transmits into the residual fragment's wage **continuously**, with sign set by whether decomposition raises the residual requirement (excavator, crane) or lowers it (the Taylorized line). At a bundled boundary, **nothing transmits until the last engaged ray crosses**; then the task flips discretely. The signature pair — continuous-with-sign versus stasis-then-cliff — is the anatomy's principal observable. ∎ [checked ✓ 2026-08-09, check_anatomy.py B0'2-RES: explicit term — the residue wage satisfies w·r_B + a_M·m_c = p̄ with r_B the residual requirement, so dw/dm_c = −a_M/r_B (continuous), the level shift at decomposition carries r_B's sign, and the bundled case is flat-then-cliff.]

### Proposition B.0′-3 (K, derived; co-dependence)

Prop 11's co-presence anchor is the bundled, low-D residue: tasks engaging SOC-co-present or UNS whose components fail both separability tests and whose practice leaves no records. The legal anchor is the fortified set (Block D, species 5). **Neither anatomy classifies alone** — the pilot's pharmacist row: capability order comes from the task anatomy, survival from the μ-anatomy, the latter admissible only with a citable instrument. Scope note (amendment 4): the classifier speaks at fragment level; occupation outcomes add demand elasticity and recomposition.

---

## Block C — the education race

### C.0 Setup

Untrained workers hold low-loading fragments at w₀(t). Training to qualification q_req takes T_E(θ) = q_req/λ(θ) years of foregone earnings; trained workers earn w₁ = w₀ + P + R(θ) per Block A. Two premia must be distinguished: the **published premium** Π̄(t) — the average over incumbents, which is what premium statistics report and what the beliefs literature says students track (Wiswall–Zafar) — and the **marginal premium** Π_m(t + T_E) that will actually greet the entrant at graduation, at the assignment margin, T_E years later. Π̄ ≥ Π_m structurally, because the average includes inframarginal talent rents and any credential wedges.

### Proposition C1 (the cobweb)

Entry is a talent threshold: θ̂(t) enters iff the annuitized Π̄(t) covers (r + δ_P)·C(q_req; θ). The trained stock evolves H_{t+1} = (1 − δ_P − retirement)·H_t + E_{t−T_E}; the marginal premium clears decreasing in H. The lag T_E plus elastic entry generates cobweb oscillations; stability iff the product of the entry elasticity and the inverse demand slope is below one. Freeman's engineers, in the model's own notation. ∎ [checked ✓ 2026-08-09 WITH AMENDMENT, check_race.py C1-COBWEB: the two-equation statement's characteristic polynomial is z^(T+1) − (1−δ)z^T + eb. "Product below one" is EXACT for T_E = 1 at every depreciation rate (Jury) and an upper bound generally: the boundary tightens with the training lag (T_E=4, δ=0.03: eb < 0.36; T_E=8: eb < 0.20). State the condition lag-indexed at merge.]

### Proposition C2 (the hump)

Demand drift has two eras, *derived from the ray table via B.0′*, not assumed. Engineering rays crossed structured, rule-based work sitting **below** the trained stratum: crowding pushed w₀ down (the paper's Prop 1 comparative statics) while residue-fragment creation (B.0′-1) raised demand for the trained — positive drift, the Tinbergen race, premium widening whenever supply lagged. Learning rays now cross the trained stratum's **documented practice** (F1) — negative drift, plateau, then compression. The composition-adjusted between-group premium is therefore **hump-shaped: widen, plateau, compress** — and its supply-adjusted path is a time series for the schedule's shape. This is the kill-shot-one measurement, and it is data item one. ∎ [checked ✓ 2026-08-09, check_race.py C2-HUMP: with single-peaked demand drift and adjustment in the stable MONOTONE regime (real non-negative roots), the premium path is single-peaked; in the oscillatory-stable regime the one era-scale hump carries cobweb wiggles — which is what the measured plateau looks like. C3's composition half also verified friction-free: Π̄ − Π_m = mean inframarginal rent ≥ 0.]

### Proposition C3 (systematic overshoot; the queue)

Because the signal is Π̄ and the truth is Π_m at t + T_E, the expectational error is one-signed in the flattening era — for two separable reasons that carry different burdens. **Composition** needs no friction at all: Π̄ averages over incumbents, so it includes their inframarginal talent rents and any wedges, and exceeds Π_m even in steady state under full information. **Lag** bites under negative drift and is the only part resting on the belief assumption of C.0 (documented directly: stated expectations track posted averages). Entry exceeds the perfect-foresight level; the excess queues for credential-wedged jobs or spills down the ladder, pushing w₀ lower still. The queue is observable as recent-graduate underemployment. **"Useless degrees" is the equilibrium marginal cohort**: realized premium near zero at a still-positive published average. ∎

### Proposition C4 (the doomed vintage)

Practice acquired within T_E-plus-payback of its fragment's copying date has negative NPV: tuition and foregone earnings spent on capability about to be copied. The transition burns resources on a **second front** beyond §4's wedge-targeting loss — doomed acquisition — with magnitude cohort flow × acquisition cost × exposed-field share. [Measurable; hook to the data plan.] ∎

**Remark (the remedy self-attenuates).** Training moves h, never θ; its power scales with the slope times the practice-loading of the surviving steep regions — both falling under F1 — and at the corner it does nothing. Education policy is a linked-regime instrument, and the paper should say so where it prices conditionality.

**Remark (signal decay → Block D).** Expansion lowers the credential's talent-certification content: the entry threshold θ̂ falls while the published average holds up. Employers drop requirements where the screen is price-form (skills-based hiring: self-liquidation) and keep them where it is quantity-form (licensure) — hand-off to species 2.

**Predictions.** P-C1: the hump, with the compression leg live and measurable now. P-C2: entry turns down before incumbent premia in exposed fields (B4 restated at occupation level). P-C3: recent-graduate underemployment tracks field-level exposure, not just the cycle. P-C4: degree-requirement dropping concentrates in unlicensed occupations.

---

## Block D — the anatomy of μ

### D.0 The black box, opened

AR's μ is measured at 40–50% through displacement losses, an identification that cannot distinguish sources. First the ledger: an observed displacement loss L decomposes as

**L = transferable rent + stranded specific practice + compensating differential**

and only the first is a wedge. Then the wedge itself speciates:

| # | Species | Sustained by | Dies by | Signature |
|---|---|---|---|---|
| 1 | Bargained rents (union premia, hold-up) | replacement cost of the workforce | automation feasibility itself | erodes continuously with machine cost; converts to quantity form under pressure |
| 2 | Credential rents | institutional screens: statutes, HR rules, pay scales | signal collapse where price-form; politics where quantity-form | Prop 2 targeting with teeth; requirement-dropping visible in postings |
| 3 | Monitoring rents (efficiency wages) | costly observation of effort | measurement technology — **no task flip needed** | wage compression in newly measurable jobs absent automation events |
| 4 | Slack rents ("bullshit" stratum) | product-market rents + agency costs, dissipated as employment | competition, measurement, downturns | tracks market power and management quality, not occupation; procyclical purges |
| 5 | Fortified pay | statute or contract reserving the task | politics only | punctuated adoption; the stress test's overlay |

Species 0, for completeness: compensating differentials are not rents, and privately-valuable but socially-zero-sum tasks (advertising and litigation arms races) are not wedges — real wages, real private product, zero net social product — a separate line for §4's accounting.

### Proposition D1 (loss decomposition; the negative-sum figure revised)

The imported 60–90% offset is the **wedge-share reading** of displacement losses, and it is an upper bound. Where the loss is stranded specific practice, pay equaled marginal product, so privately profitable automation was *socially* profitable too: the worker's loss is real — a capital write-off borne by them, plus distribution — but it is not allocative inefficiency, and it does not belong in the negative-sum column. Where the loss is a compensating differential, it is neither. The three components carry distinct signatures and are separable in microdata: wedge losses arrive discretely and show the U-shape incidence; stranded practice scales with tenure and specificity (Jacobson–LaLonde–Sullivan; Lachowska et al.); compensating-differential losses concentrate where disamenities were high and are offset by amenity gains. **The transition-loss estimate the paper imports should be restated as a range indexed by the decomposition weights.** ∎ [checked ✓ 2026-08-09, check_mu.py D1-CS: ledger L = b(μ−1) + (r+δ_P)σ·C(tenure) + d verified with the three statics — wedge term tenure-free and discrete, tenure gradient identifies the stranded share, differential cancels in welfare; measured ≥ welfare ≥ allocative (wedge only), so the 60–90% restates as 60–90% × ω_wedge.]

### Proposition D2 (the demolition spectrum; closure with the stress test)

Each species dies by a different weapon: machine cost kills 1; measurement kills 3 and 4 without any task flipping; signal collapse kills price-form 2; only politics kills 5 and quantity-form 2. Under sustained automation plus measurement progress, the surviving wedge stock's composition therefore drifts toward quantity and legal form — the paper's fortification filter, derived at species level. **Corollary (closure):** the stress test's admissibility rule — survival requires a citable instrument — is this proposition read as a classifier. The theory and the coding rule are the same object. Prediction: the share of surviving wage premia coincident with statutory instruments rises over time. ∎

**Remark (measurement demolishes without automating — flag it, and its price).** Species 3 and 4 dying to observation technology is a named confound for stage-one signatures: wage compression with no adoption event. It also suggests, as conjecture only, that some measured productivity gains of the automation era are slack purges misattributed to machines. And a normative paragraph belongs in the paper's voice: monitoring-driven wedge destruction is a transfer to firms priced in surveillance; an efficiency-wage wedge is not welfare-free to demolish.

**Remark (the subsidy mirror, speciated).** The μ < 1 half-line completes species-wise: in-work benefits are public slack; the paper's private/public symmetry holds at the species level.

**Predictions.** P-D1: wage compression without automation in newly measurable occupations. P-D2: displacement losses' tenure gradient identifies the stranded-practice share. P-D3: requirement-dropping in unlicensed occupations, persistence in licensed. P-D4: surviving premia increasingly statute-backed. P-D5: slack purges are procyclical and concentrated in high-market-power firms.

---

## Integration notes (for the merge)

- B.0′ inserts between B.0 and Assumption F; F's order claim cites B.0′ as its microfoundation; the paper's Prop 2 inherits the fragment reinterpretation of the task space.
- Prop B.0′-1 rewrites §10's first entry: branch two gets its mechanism.
- Block C is the paper's first dynamics section (after §4); C2 is data item one's theoretical object; C4 adds the doomed-vintage line to §4's transition accounting.
- Block D rewrites the wedge paragraphs of §2 and §4: μ speciated; D1 restates the imported 60–90% as a decomposition-indexed range; D2 absorbs and derives the fortification remark.
- One sentence for the paper, verbatim candidate: *capability order comes from the anatomy of the task; survival comes from the anatomy of the wedge; neither classifies alone.*
- Notation: C introduces Π̄, Π_m, T_E, H, E; no collisions spotted beyond those already logged (β-reach, D*, λ_i). [check on merge.]

## Decisions (taken 2026-08-09; veto anytime)

1. **C's information friction — stated assumption, not derived.** The overshoot splits in two (see revised C3): the composition half needs no friction at all, and the lag half is documented directly (Wiswall–Zafar: stated beliefs track posted averages). State it and cite it; a derivation from publication lags would invite the rational-expectations fight for no gain, since the belief pattern is measured, not conjectured.
2. **Species 3's surveillance paragraph — keep, decomposition-framed.** Monitoring-driven wedge demolition is observationally identical to efficiency gain in wage data while being partly a transfer priced in worker surveillance. One paragraph separating the efficiency component from the transfer component is bookkeeping, not editorializing — the same honesty the paper practices everywhere else. No sermon.
3. **Species 4 — "slack rents," Graeber in a footnote.** The other four species are named for their sustaining mechanisms; this one's mechanism is rent dissipated as employment through market power and agency costs, which "slack" names and "bullshit" doesn't. The footnote keeps the recognizable phenomenology without staking the theory on contested survey numbers (Soffia–Wood–Burchell).
4. **C4's magnitude — banded back-of-envelope, computed in the data pass.** The paper's style is theorem-then-measurement; the ingredients (completions by field, cost of attendance, exposure shares) are public and sit adjacent to data item one, so the bound is a day's work there. Bracketed band like everything in §8; no naked point estimate.
