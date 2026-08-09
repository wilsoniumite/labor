# The Layered Link — merging the Link Model with Acemoglu–Restrepo (2026, QJE)

*Companion to `link_model_formal.md`. P1–P5 refer to that document and are not restated. New results are numbered L0–L5.*

## 0. How to read this

The merger costs one new object (a wedge µ(x) ≥ 1 on tasks) and pays out five results. The math burden is unchanged: ratios, inequalities, one division. Read §1 (dictionary) even if you skip everything else — both papers use λ, µ, and ρ for *different things*, and the dictionary is the difference between citing both models and embarrassing yourself. First pass: §2, §3, and the example in §4. The proofs are shorter than the ones you've already survived.

**One sentence per model.** A&R (QJE 2026): automation is aimed at the *best-paid* versions of each job, demolishing job-specific rents (union premia, license rents, efficiency wages) first — with full incidence on the losers and a possible net TFP loss. The Link Model: beneath those rents sits the link premium, which automation also erodes, and beneath everything sits the exit floor and the land. Merged: **one demolition, read top-down through three strata** — and their machinery supplies the engine the Link Model previously only assumed.

---

## 1. The dictionary (read this or perish)

| Object | Their notation | Ours | Notes |
|---|---|---|---|
| task CES elasticity | λ (= 0.5) | not needed (checklist production) | remark in §8; NEVER our λ |
| wage-linkage share | — | λ | fiscal object; absent from their model |
| job wedge / rent markup | µ_gx ≥ 1 | µ(x) ≥ 1 | the new primitive here |
| their estimated dissipation ratio | ρ̂ ≈ 0.5 | written ρ̂_AR | a *wedge markup* estimate, NOT a capability schedule |
| capability edge | ψ_gx/ψ_kx (implicit) | ρ(x) = γ_L/γ_M | central to us, incidental to them |
| effective (wedge-deflated) edge | — | **ρ̃(x) = ρ(x)/µ(x)** | the merged model's central object |
| machine cost | 1/q_x, exogenous intermediate | c = ℓr/(1−a), P2 recursion | the substantive difference; §7 |

---

## 2. L0 — The Deflation Lemma

**Plain.** A wedge makes a task's labor artificially expensive, which is indistinguishable, from a hiring firm's chair, from the human edge being smaller. So the entire Link Model survives contact with wedges after a single substitution: allocation runs on the *effective* schedule ρ̃ = ρ/µ, not the raw one.

*Formal.* With task wedges, labor holds task x iff µ(x)·w/γ_L(x) ≤ c/γ_M(x), i.e. iff **w ≤ c·ρ̃(x)** where ρ̃(x) = ρ(x)/µ(x). Relabel tasks by ρ̃. All of P1–P5 hold verbatim with ρ̃ in place of ρ; in particular the base wage is w = c·ρ̃(x*) and *the link* is now the pair (ρ̃(x*), ρ̃′(x*)).

**Proof.** Divide both sides of the cost comparison by µ(x). ∎

**Geometric reading, worth keeping for the essay: a wedge is negative altitude.** It drags a task down the effective schedule toward the waterline without changing how good humans actually are at it.

---

## 3. L1 — Stratigraphy of a wage

**Plain.** A paycheck has three geological layers: the exit floor at the bottom, the link premium in the middle, the wedge rent on top. Different forces built each layer; different forces demolish each layer; and the merged model's whole story is that automation demolishes them in order, from the top.

*Formal.* A worker at task x with base wage w = c·ρ̃(x*) earns

> s  +  [c·ρ̃(x*) − s]  +  [µ(x) − 1]·c·ρ̃(x*)
> (floor)   (link premium)      (wedge rent)

The floor is set by the outside option (land-backed, P4i). The link premium is set by the effective schedule's level and slope at the margin (P1). The wedge rent is set by institutions — unions, licenses, monitoring frictions — and exists only where µ(x) > 1.

*Convention, flagged honestly:* wedge jobs are rationed (their model's queues), so the marginal participant is evaluated at the base wage; participation is w ≥ s, not µ̄w ≥ s. This matches their efficiency-wage micro-foundation and keeps P1(iii) intact. An alternative lottery-ticket convention (participate iff expected wage ≥ s) softens the floor by µ̄; nothing downstream flips.

**Example (the $10 machine acquires a union).** c = $10, s = $25. Task A: ρ = 1, µ = 1 (machines hold it). Task C: ρ = 4.5, µ = 1. Task B: ρ = 5, µ = 1.25 — objectively humans' best task, but wedged. Effective edges: ρ̃(B) = 4, ρ̃(C) = 4.5. Labor holds B and C; the *effective* marginal task is B, so w = $40. Stratigraphy: the C-worker earns 25 + 15 + 0 = $40; the B-worker earns 25 + 15 + 10 = $50. Note the inversion already: the task where humans have the *largest* raw edge has become the effectively marginal one, purely because of its wedge.

---

## 4. L2 — Targeting: dissipation transplanted, and one step further

**Plain.** Their Proposition 2 says: when new automation opportunities arrive, firms flip the expensive-labor tasks first — which, at equal capability, means the high-wedge tasks. In our geometry that is one sentence: **the flood takes tasks in order of effective altitude ρ̃, and wedges are negative altitude.** The corollary is the cruel one: the better protected the job, the earlier the robot comes for it, *even when the protected workers are objectively better at their task than the unprotected ones are at theirs.*

*Formal (theirs, transplanted).* Let an automation advance make a set of tasks feasible for machines. Under their conditions (opportunities not biased toward low-ρ̃ tasks; wedges orthogonal to capability within the opportunity set), the tasks actually flipped are those with the lowest ρ̃ among the feasible — first-order stochastically the high-µ tasks. Proof: adoption occurs where µ(x)w/γ_L ≥ c/γ_M, i.e. where ρ̃(x) ≤ w/c; the adoption region is a lower set in ρ̃. ∎

**Example continued.** Uniform machine improvement of 25%: raw edges fall to ρ(B) = 4, ρ(C) = 3.6; effective edges ρ̃(B) = 3.2, ρ̃(C) = 3.6. B floods before C — automation takes the task where humans are objectively *better* (4 > 3.6), because the wedge made it the cheapest conquest. The displaced B-worker loses twice, and differently: the $10 wedge rent vanishes with **full incidence** (a composition effect — no margin moves, so no one shares it; their finding that dissipation is undampened by ripples), while the base-wage fall to the new margin is shared economy-wide through P1's comparative statics. Their empirics and your slope-sharing logic are the same sentence read in opposite directions.

*One step further — labeled as ours, a conjecture.* Their theorem governs *adoption within* an exogenous opportunity set. Directed-technical-change logic extends it to the opportunities themselves: R&D aims where labor expense is greatest, i.e. at the peaks of c·ρ(x)·µ(x). This endogenizes the flattening: **the link erodes because its highest points are the most profitable points to attack.** The Link Model previously assumed ρ's compression as a trend; the merged model derives its direction. Their paper licenses the adoption half only; the direction half is the merger's conjecture, and a referee should be told so.

*Corollary (self-liquidation of labor-side institutional rents).* A wedge that operates through *price* raises its own task's automation priority: labor-attached institutional scarcity is self-undermining under sustained automation. Only *quantity* exclusion — law removing a task from the automatable set entirely — survives L2. This re-derives, inside their machinery, the essay's verifiability judgment: a human-provenance premium enforced as a price markup invites its own replacement; one enforced as a task reservation does not. (Ledger item 5 of the Link Model, now with a mechanism.)

*Remark (the µ-axis as the one distortion dial).* Their footnote observes that subsidies are anti-rents. Precisely: an in-work benefit b is a wedge µ < 1 (labor accepts less at the task), producing *over*-employment where private rents produce under-employment — and in the corner regime, P4(ii)'s make-work. Her conditionality distortions and their labor-market rents are the two half-lines of a single µ-axis, with the competitive model at µ = 1.

---

## 5. L3 — Sequencing: the demolition schedule and its signatures

**Plain.** Under sustained automation pressure the strata die from the top: wedge rents first (L2 targets them), then the link premium's slope and level (the flattening), then participation itself (corner-below). Each stage has an observable signature, and the first stage's signature is already in their data.

*Formal.* (i) Stage one: E[µ] → 1 on held tasks; within-group wage dispersion *compresses* (their Figure 5's U-shape — losses concentrated in the 70th–95th within-group percentiles, the wedge-job holders). (ii) Stage two: ρ̃ flattens; the base wage decouples from scarcity and falls toward machine parity (P1ii). (iii) Stage three: parity crosses s; exit (P1iii). The stages overlap in calendar time but are ordered in each task's history.

**The hand-off that matters for the essay:** stage one's compression-toward-the-floor is exactly the premise P4(iii) needs — as wages pile up just above the base, the mass of workers sitting inside any fixed benefit-withdrawal band grows, and the poverty trap worsens under unchanged rules. Their 1980–2016 evidence is the empirical opening act of your trap proposition. Also note, quietly: their accounting framework for this period contains **no reinstatement term** — a fixed task space, your ledger item 1, adopted without ceremony for precisely the window where wages stagnated.

*Sizing, from their estimates, used as sizing only:* ρ̂_AR ≈ 0.5 — automated jobs carried wedges of order 40–50% of base wages; automation accounts for 52% of the rise in between-group inequality since 1980, with dissipation responsible for about a fifth of that contribution; full incidence on the displaced.

---

## 6. L4 — The finite fuel tank: transition deadweight

**Plain.** In a competitive world, automation is always weakly good for total output, however brutal its distribution. Wedges break that: a firm automating a $50 welder saves $50 minus the machine, but society only frees up what the welder produces elsewhere — $40 minus the machine. The $10 difference is a pure allocative loss, and their published estimates say it offset 60–90% of automation's productivity gains, 1980–2016 — possibly all of them. Privately profitable automation ran near socially break-even, perhaps negative-sum, *before any corner-regime concern arrives.*

*Formal.* Automating a wedge task yields private saving π_private = µw − κ but social saving w − κ; the gap (µ−1)·w per displaced hour is a first-order allocative loss (their welding example, verbatim in our notation). Aggregate sign of TFP is ambiguous during demolition. **Bound (merged model's addition):** the cumulative allocative loss is capped by the wedge stock — once E[µ] = 1, L2's targeting has nothing left to mis-target, the competitive envelope logic resumes, and automation is again weakly TFP-positive until P2's value migration becomes the story. The deadweight is a *transition* phenomenon with a finite fuel tank, burned during the third and fourth arcs.

*Honesty note:* "capped by the wedge stock" assumes wedges do not regenerate (unions re-form, licensure expands). Wedge regeneration slows L3 and refills L4's tank; the merged model takes wedge *locations* as given, exactly as they do, and their companion paper's micro-foundations are where an endogenous-wedge extension would start.

---

## 7. L5 — Conservation of rents: dissipation is migration

**Plain.** "Rent dissipation" is their name; the merged model's ledger says the rents are not destroyed but *reattached*. In their model the savings from automating wedge jobs flow to consumers as lower prices (competitive firms, capital conjured at cost from the final good — their machine sector has no land, no recursion, no residual claimant). Run the same flows through P2 instead: machine cost is c = ℓr/(1−a), consumption spending in the corner resolves into rents on non-produced factors, and the surplus released from labor-attached wedges comes to rest attached to land, sites, and energy.

*Formal (merged-model statement, honestly conditional).* In the corner regime, the incidence of wedge-demolition savings follows P2's corollary: physical rents, institutional rents, transition rents, thin interest. **Rent dissipation is rent migration: from labor-attached institutional scarcity to land-attached physical scarcity.** Their title mechanism, completed by P2, is a conservation law with a change of attachment point. This claim is the merger's, not theirs — their model *cannot* express it, because their machine cost 1/q_x is an exogenous parameter; their framework ends at exactly the wall P2 walks through. That is not a criticism; it is the seam where the models join.

---

## 8. Remnant differences, kept deliberately

Checklist production here vs their CES over tasks (their λ = 0.5): CES softens thresholds into bands and lets their quantitative formulas run; every mechanism above survives (Link Model ledger item 3). Groups: their 500 demographic groups are, in our terms, personal ρ̃ schedules — heterogeneity in both capability and wedge exposure; all results hold type by type (ledger item 2). Ripples: their propagation matrix is the many-type version of P1(ii)'s margin-sharing; their finding that dissipation, unlike displacement, does *not* propagate is L2's composition-vs-margin distinction and needs no new machinery.

---

## 9. What the merger buys the essay

| Essay claim | Now backed by |
|---|---|
| "the better protected the job, the earlier the robot" | L2 corollary + their Prop 2 |
| the flattening has an engine, not just a trend | L2 direction conjecture (flagged as conjecture) |
| human premium survives only as task reservation, not price premium | L2 self-liquidation corollary |
| compression toward the floor → worsening traps | L3 hand-off into P4(iii), with their Fig 5 as evidence |
| automation can be negative-sum before the corner | L4, their 60–90% offset of productivity gains |
| "where the rents go" | L5: dissipation = migration, via P2 |
| wedge stratum sizing | ρ̂_AR ≈ 0.5; dissipation ≈ a fifth of a 52% inequality contribution |

## Where a referee would push, in order

1. The direction conjecture in L2 — their evidence covers adoption, not R&D direction; keep the label "conjecture" glued on.
2. Wedge regeneration (L4's honesty note) — the fuel tank refills if institutions rebuild.
3. The participation-at-base-wage convention (L1) — state it, cite the queue logic, move on.
4. L5 inherits P2's assumptions and the fixed task space — the same first fight as before, now with company: their 1980–2016 accounting made the same choice.
5. ρ̂_AR = 0.5 rides on their identification — use it to size the stratum, never as a constant of nature.

Everything above those five lines, I would defend as written.
