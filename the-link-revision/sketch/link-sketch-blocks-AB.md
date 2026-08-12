# The Split — working sketch, Blocks A & B

**Status.** Working draft for the revision of *The Link* (Aug 2026). Blocks C (education race) and D (anatomy of μ) to follow. Numbering is provisional (A·, B·) to avoid collision with the paper. **Algebra/numerical pass completed 2026-08-09** (`../checks/check_split.py`, `../checks/check_mirror.py` — sympy + numeric instantiation per the house rule); every flag below records its check's outcome, one with an amendment (B2).

**Notation.** Inherits the paper's objects: tasks x ∈ [0,1], machine rental c, wedges μ(x), outside option s, effective edge ρ̃. New: θ (talent/ability, scalar), q (practice stock), α(x) talent loading, β(x) practice loading, D(x) documentation density, λ(θ) learning gradient, δ_P practice decay. Known collisions to resolve on merge, not here: the paper's λ_i (wage-linkage shares), the superstar remark's β (reach fraction), Prop 10's D* (deadweight). Flagged again at the end.

---

## Block A — the split, static

### A.0 Setup

Worker i carries talent θ_i ∈ ℝ, drawn once from a distribution F (the prior; its shape matters only in the tails, where it sets superstar concentration, and nowhere else below). Practice at task x is a stock q_i(x) ∈ [0,1], measured as a share of the human practice frontier at x. Capability:

    log γ_L,i(x) = log γ̄(x) + α(x)·θ_i + β(x)·q_i(x)

α(x) ≥ 0 is the task's talent loading, β(x) ≥ 0 its practice loading, γ̄(x) a common baseline. A task is a point in (α, β)-space: "cognitive capability" is not one axis but two.

Acquisition (Ben-Porath 1967): practice accumulates at rate λ(θ) per unit of study time, λ′ > 0 — talent is the *gradient*, the rate at which practice converts into capability — and decays at δ_P. Reaching share q therefore costs t(q) = q/λ(θ) years of foregone earnings, so acquisition cost is C(q; θ) = w_alt · q/λ(θ), with w_alt the untrained alternative wage. [checked ✓ 2026-08-09, check_split.py A0-DR: every sign and the free-entry premium formula survive any convex study technology g(q); the indifference equation never references g's shape.] An optional ceiling q ≤ q̄(θ, x) is available but unused below.

Two definitional commitments, stated once. θ is defined **operationally**: the component of capability invariant to the model's instruments (schooling, training, tools) on the horizons modeled. No claim about biology is made or needed. And the split is **not orthogonal**: λ(θ) makes the components complements, which absorbs gene–environment correlation in reduced form — the talented select more practice, and the model prices the package.

### Lemma A1 (sorting survives the scalar; the degenerate case)

For θ′ > θ at equal practice, log[γ_θ′(x)/γ_θ(x)] = α(x)(θ′ − θ). If α(·) is non-constant, order tasks by α: capability is log-supermodular in (θ, x), higher-talent workers hold *comparative* — not merely absolute — advantage in higher-loading tasks, and equilibrium assignment is positive assortative (Costinot–Vogel 2010; Teulings 1995). If α is constant, the ratio is task-independent: workers are perfect substitutes in efficiency units and the model collapses to the paper's homogeneous case wearing a label.

*Scalar talent is safe; constant loading is the degenerate case.*

Proof: read off the display; assignment is the cited assignment theory. ∎
[checked ✓ 2026-08-09, check_split.py A1-FP: single crossing verified symbolically (∂²V/∂θ∂α = p·e^(αθ+βq)(1+αθ) > 0 with q at its envelope optimum); the sorting-and-training fixed point exists numerically (400 types × 8 pools, fictitious-play averaging, clearing within the discrete-type granularity bound) and is positively assortative throughout.]

### Proposition A2 (four strata)

Steady state; free entry into acquisition; competitive per-efficiency-unit pay within labor's region; wedges as in the paper. The pay of worker i at task x decomposes:

    w_i(x) = s + P(x) + R_i(x) + wedge stratum

(i) **Practice premium** P(x) = (r + δ_P) · C(q(x); θ_m(x)): the amortized acquisition cost of the **marginal acquirer** θ_m(x) — the slowest learner for whom entry into training at x just breaks even. Free entry pins it: above cost, training entry expands the qualified stock and the premium falls; below cost, the stock decays unreplaced and it rises. **Cost recovery, not rent.**

(ii) **Talent rent** R_i(x) ≥ 0, collected through two channels: the *level* channel, α(x)(θ_i − θ_m) in log pay (paid per efficiency unit at the task), and the *gradient* channel, (r + δ_P)·[C(q; θ_m) − C(q; θ_i)] — the same premium acquired more cheaply. Both are Ricardian differentials over the marginal acquirer, exactly as parcels earn their advantage over the worst in cultivation.

(iii) The paper's "link premium" is therefore P + R: a produced component priced at reproduction cost and a non-produced residue earning differential rent. **The wage decomposes the way the paper's whole economy does.**

Proof sketch: (i) indifference of θ_m between training-then-working at x and the untrained alternative; entry and exit into acquisition do the rest. (ii) subtract θ_m's condition from worker i's pay. ∎
[checked ✓ 2026-08-09, check_split.py A2-POOL: the pooled qualification requirement delivers an interior θ_m in every trained pool of the numeric equilibrium; free entry pins the pool premium to the marginal acquirer's amortized cost (boundary types indifferent), and inframarginal rents increase in θ within the pool.]

### Proposition A3 (the slotting)

Into the taxonomy of the paper's Prop 3 corollary (physical / institutional / dynamic / interest):

(i) **Practice is dynamic scarcity.** Produced (stored labour, self-invested — the Wicksellian stock worn on the inside), delivered through a pipeline measured in years to decades, depreciating at δ_P. Its premium is a quasi-rent: pinned to reproduction cost in steady state, positive while the trained stock is short, and **stranded** when demand dies — sunk acquisition earns nothing against a vanished task. [Hook: the pipeline lag is Block C's cobweb.]

(ii) **Two migrations out of the dynamic column.** *Licensure* converts a practice premium into institutional rent: entry capped by law, so the premium stops eroding with supply — the credential wedge, now derived rather than listed. *Recording* converts practice into an idea: reproduction cost ≈ 0, competitive price ≈ 0, any positive return institutional (copyright, licensing) or dynamic (data moats). **Live practice is dynamically scarce; recorded practice is an idea.**

(iii) **Talent is physical scarcity on the supply side — with two asymmetries against land.** *Supply*: non-produced, per-person inelastic; it prices as Ricardian differential rent and enters the physical column. *Demand*: no term of the machine recipe uses θ, so outside K its terminal demand is zero — a **transition rent on a permanent base**. The physical column splits into scarcities machines require (sites, energy: terminal rents, rising with automation) and scarcities machines obsolete (talent). *Fiscal*: land's rent flows in rem; talent's flows only through chosen participation and effort, so any tax on it moves a margin — it fails exactly the test that made land the surviving base (Prop 7(ii)). Talent belongs to the pricing taxonomy and not the funding one. This is Mirrlees (1971) restated from the paper's side: the unobservable non-produced base whose taxation must travel through income. **George is Mirrlees with an observable base.** [Footnote, for symmetry with fusion: embryo selection would make talent produced and migrate it out of the physical column entirely; not modeled.]

(iv) **Co-presence** is the one human physical scarcity with terminal demand (Prop 11's K-anchor): bodies are non-produced per person, and the room requires one.

**Remark (the four-column wage).** Every stratum of pay now files where the paper files everything else: practice → dynamic; credentials → institutional; talent → physical-transitional; co-presence → physical-terminal; fortified pay → institutional, as before. The taxonomy covers labour income with the same columns it uses for the corner.

**Remark (for §10, honesty entry).** The clean split is false as psychology: heritability is a population statistic, not an individual decomposition; schooling detectably moves measured ability; deliberate practice explains a minority of performance variance, with enormous domain spread. The model buys none of those fights: θ is operational, λ(θ) absorbs the entanglement, and every result here survives any origin story for θ.

---

## Block B — the machine mirror

### B.0 Machines on the same axes

Machine capability at task x, time t:

    log γ_M(x, t) = τ_t · α_M(x) + m(x, t)

τ_t is machine "talent" — architecture and scale, a rising path — with its **own** loading α_M(x): nothing forces α_M ≈ α, and their historical mismatch is Moravec's paradox in this notation. m(x, t) is machine practice, acquired not by study but by **copying**: training data is the recorded practice of humanity, so

    m(x, t) → β(x) · D(x)   as training effort grows,

where D(x) ∈ [0, 1] is **documentation density** — the share of the task's practice frontier that leaves records (text, code, images, logs; tacit and embodied craft sit at low D).

Two asymmetries do all the work: human practice is paid for per person, per generation; machine practice once per model, replicated at ~zero marginal cost. And machines can only copy what was recorded.

### Assumption F (flattening, named, with an order)

The paper's flattening premise, promoted from implicit premise to stated assumption with structure:

- **(F1) Copying (certain where D > 0):** m(x, t) rises toward β(x)·D(x) at every task, fastest where D is high.
- **(F2) Crossing (open):** τ_t rises without a known bound; the talent gap at task x closes only when τ_t·α_M(x) exceeds α(x)·θ for the relevant θ.

Flattening of ρ̃ is the sum of the two channels. This replaces §10's bare fork with something measurable: (F1) is already underway wherever records exist; (F2) is the genuine unknown. Every claim below is tagged by the channel it needs.

### Proposition B1 (the order of demolition, refined) — needs F1 only

At equal wedge and equal feasibility, the human edge compresses first at tasks with high β(x)·D(x) and small talent gap: **practice-heavy, well-documented work goes first**. The adoption lower set of the paper's Prop 2 fills in (β·D)-order; wedges still raise priority one-for-one on top. Radiology before plumbing, because the archive exists.

Proof sketch: residual log edge at the occupying type ≈ α(x)(θ − τ_t·α_M(x)/α(x)) + β(x)(1 − D(x)); the copying term removes β(x)·D(x) and nothing else. ∎
[checked ✓ 2026-08-09, check_mirror.py B1-OCC: for the occupying type the display is β(x)(q_occ(x) − D(x)) — the sketch's β(1−D) is the q_occ = 1 frontier case; copying removes β·D and nothing else (∂logρ/∂D = −β); the endogenous-practice feedback (dq*/d premium > 0) reinforces, never reverses, the β·D order.]

### Proposition B2 (which claims need which channel) — the tagging

Dispersion of the effective schedule decomposes into a **practice-gap** component — driven by β(x)(1 − D(x)) plus the not-yet-copied remainder, shrinking with certainty under (F1) — and a **talent-gap** component that shrinks only as τ crosses. Stage-one and most stage-two demolition (wedge targeting; premium erosion at documented tasks) need (F1) alone. The corner, and everything downstream of it, needs (F2).

**The paper can therefore make near-term claims independent of any AGI debate, and should say which are which.** ∎
[checked ✓ 2026-08-09 WITH AMENDMENT, check_mirror.py B2-COV: the decomposition carries a covariance term. F1 always shrinks the practice component, but AGGREGATE dispersion falls only if Var(copied) + 2·Cov(copied, remainder) > 0 — a sufficiently Moravec-negative covariance reverses the aggregate sign (shown numerically: +0.099 var change in the Moravec calibration vs −0.003 independent). The channel-tagging survives either way; any aggregate-dispersion claim in the merge must carry the empirical covariance sign or lean on F2.]

### Proposition B3 (the corpus at the idea boundary) — needs F1 only

Recorded practice inherits the paper's idea boundary verbatim: reproduction ≈ free, competitive price ≈ 0, positive returns only where law or moat creates exclusion — copyright and licensing (institutional), data access and first-mover training (dynamic).

**Corollary (double doom).** The practice component of wages is removed twice: copied on the machine side (B1), and priced at zero in its recorded form on the asset side. None of the corpus's value returns as wages absent statute. The current litigation wave is the institutional column being priced in court.

### Proposition B4 (erosion order inside the wage; entry dies first) — needs F1 only

At an exposed task, (F1) erodes the market value of trained human capability. Incumbents' practice is sunk — a quasi-rent — so incumbent pay glides down with replacement cost. But the **entry condition dies discretely**: acquisition stops when the expected premium over the remaining horizon falls below (r + δ_P)·C. Hence completions and entry collapse **before** incumbent wage premia do, and the talent-rent layer outlives the practice layer at every task.

[Hook: stranded practice joins Block D's displacement-loss decomposition — wedge rent + destroyed capital — which revises the paper's negative-sum accounting.]

**Remark (tutors deflate the layer they teach).** Machine tools also raise λ effectively: acquisition gets cheaper for humans. Since P is priced at marginal acquisition cost, education technology **lowers** the practice premium in equilibrium while leaving talent rents relatively larger — when anyone can learn anything cheaply, only the unlearnable differentiates. Screening should migrate from certified practice toward direct talent verification (work trials, contests, interviews-as-auditions).

### Provisional predictions (to join the paper's list)

- **P-A.** Automation adoption order, conditional on wedges, tracks β·D: practice-loaded, well-documented tasks first; talent-residual and unrecorded tasks last. Operationalizable as published AI-exposure scores × a documentation-density proxy.
- **P-B.** In exposed occupations, entry (enrollment, completions, apprenticeships) turns down before incumbent wage premia do.
- **P-C.** Returns to tenure and experience flatten earliest in high-D occupations.
- **P-D.** As tutoring technology spreads, measured education premia compress while selection shifts toward direct talent screens.
- **P-E.** Corpus value accrues as licensing and moat rents, not wages; the human authors of recorded practice capture approximately nothing absent statute.

---

## Integration notes (for the merge)

- Block A lands as a new subsection after the paper's §3; the strata display in §4 becomes four layers, with "link premium" redefined as P + R.
- A3 extends the Prop 3 corollary's taxonomy; the Mirrlees remark attaches to §6–7 ("George is Mirrlees with an observable base").
- Assumption F replaces the first entry of §10's list, converting the fork into a measured object; B2's channel-tagging should then be applied to the existing thirteen predictions.
- B3 extends §5's worked instance (weights → corpus).
- Notation on merge: rename the superstar remark's β (reach) and Prop 10's D*; the learning gradient λ(θ) collides with the paper's wage-linkage λ_i — rename one at merge time.

## Open choices (Stella's call)

1. **Talent enters twice** — level channel α(x)·θ and gradient channel λ(θ). Collapsible to gradient-only for fewer objects, at the cost of losing A2(ii)'s level channel.
2. **One practice stock with loading β(x)** vs task-specific stocks. The sketch uses the loading — lighter, and sufficient for Block B. Task-specific stocks matter only for cross-task transferability (Block D's stranded-practice accounting may want them).
3. **Assumption F's order claim**: correlational (as stated) or lexicographic (β·D strictly first). Correlational is the defensible version; lexicographic is the punchy one.
