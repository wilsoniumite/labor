# The Link Model — full statement with proofs

## 0. How to read this

Math required: ratios, inequalities, one linear equation, and two graphs you hold in your head. Nothing else. Every proposition comes in four layers: **plain statement**, *formal statement*, proof, and the running numerical example (the same $10 machine from our chat). Suggested first pass: read the plain statements and the examples only, skipping every proof. Second pass: proofs of P1 and P4 — they are the easiest and carry the most weight. P2's proof is literally one equation. P5's is the sneakiest; save it for last.

Notation, all of it: tasks x from 0 to 1; γ_L(x) and γ_M(x) are how much of task x one human-hour or one machine-hour completes; ρ(x) = γ_L(x)/γ_M(x) is the human edge at x; c is the rental cost of a machine-hour; w the wage; s the exit option; x* the marginal task; λ the wage-linkage share of a fiscal instrument; u an unconditional transfer; b, b′ conditional ones; r land rent.

---

## 1. Primitives

**Tasks.** Producing the final good requires a continuum of tasks x ∈ [0,1], each in equal amount — a checklist where every box gets ticked once per unit of output. The good's unit cost is the sum of its tasks' unit costs.

**Two ways to tick a box.** One human-hour completes γ_L(x) units of task x; one machine-hour completes γ_M(x) units. The human edge is ρ(x) = γ_L(x)/γ_M(x). Relabel tasks so ρ increases left to right: machines' best ground on the left, humans' on the right.

**Machines.** A machine-hour rents for c. Until §5, c is given; in §5 it becomes the theory's second protagonist.

**People.** N workers. Each either participates (one hour supplied) or exits to an outside option worth s — the woods, the family, the commons. This is essay footnote 4 made structural: s is the value of the best life available *without* selling labor, and notice it quietly presupposes access to some land.

**Land.** Fixed in total, heterogeneous in quality, worst parcel's reservation rent zero. Idle until §5, decisive after.

**Running example.** c = $10. Task A: ρ(A) = 1. Task B: ρ(B) = 5.

---

## 2. Equilibrium in one line

Competitive firms assign each task to the cheaper input. Labor does task x at unit cost w/γ_L(x); machines at c/γ_M(x). Labor wins x iff

> w/γ_L(x) ≤ c/γ_M(x), which rearranges to **w ≤ c·ρ(x)**.

Since ρ increases in x, there is a threshold x*: machines take [0, x*), labor takes [x*, 1]. Equilibrium = a wage and threshold such that firms are indifferent exactly at the margin and everyone willing to work at that wage is working (or has exited to s).

---

## 3. P1 — The wage is a price on the link

**Plain.** Your wage equals the rental price of a machine times your edge over it at the task where your edge is smallest among tasks humans still hold. Not need, not effort, not merit: replacement cost at the margin. Everything else in the theory follows from taking this sentence seriously.

*Formal.* (i) In any equilibrium using both inputs, w = c·ρ(x*). (ii) The wage's sensitivity to human scarcity is governed by the slope of ρ at x*: steep slope, responsive wage; flat ρ ≡ ρ̄, labor demand is perfectly elastic at c·ρ̄ and the wage is pinned there regardless of how many or few humans exist. (iii) No equilibrium wage sits below s while anyone works; if the market-clearing wage would fall below s, workers exit until the wage rises to s (possible only when ρ has slope) or all have exited.

**Proof.** (i) Suppose w > c·ρ(x*). At the marginal task, and by continuity at tasks just above it, machines are strictly cheaper; firms drop labor there; unemployed workers underbid; w falls. Suppose w < c·ρ(x*): tasks just below x* now strictly favor labor; firms demand more hours than exist; bidding raises w. Only equality is stable. (ii) To absorb more human hours, labor must win more tasks, and firms hand over a task only when the wage falls relative to the machine cost of that task — so more participants push x* left and w = c·ρ(x*) down, by an amount proportional to the slope of ρ there. If ρ is flat at ρ̄, no wage above c·ρ̄ employs anyone and every wage at c·ρ̄ employs everyone willing: perfectly elastic demand, wage decoupled from scarcity. (iii) is the participation condition applied to (i) and (ii). ∎

**Example.** w = 10 × 5 = $50. AI improves at task B so ρ(B): 5 → 2. New wage: $20. No human got worse at anything; the edge shrank. A 60% pay cut delivered entirely by someone else's machine getting better at *your* task.

**Definitions the essay needs.** *The link* is the pair (level, slope) = (ρ(x*), ρ′(x*)). The **level** sets the wage; the **slope** insulates it from scarcity. *Linked regime*: slope meaningfully positive. *Corner regime*: ρ flat at ρ̄. Two sub-cases of the corner: **corner-above** (c·ρ̄ ≥ s — everyone works, at a pinned wage) and **corner-below** (c·ρ̄ < s — rational exit; Korinek–Stiglitz "below subsistence" resolved as your footnote 4 says, by leaving, not by dying).

*Heterogeneity note.* Real people carry personal ρ's. Every result below holds type by type; the essay's "heterogeneity lifts the mean above the floor" is the cross-sectional shadow of P1, and the floor claim applies to the *support*, not the average.

---

## 4. Interlude: the four arcs, restated

Pre-industrial: machines scarcely exist; wages pinned near s by land scarcity (Ricardo's version of the same margin logic). Industrial revolution: capabilities split violently — machines absurdly better at the physical, useless at the cognitive — so ρ becomes enormously *dispersed*, the schedule steep, the link tight, wages high and insulated. Computing: the flattening begins at the simple-cognitive end. AI: flattening becomes general — the level falls and the slope falls, and they are separate injuries. That is the whole historical argument in the model's vocabulary; no proofs needed, just P1 read four times.

---

## 5. P2 — Where value goes when machines make machines

**Plain.** A machine's price is its recipe cost. When the recipe reads "machines, plus land and energy," the price collapses to marked-up land content plus a thin fee for waiting. Owning machines becomes a derivative claim on land. Ideas priced at the cost of copies go to zero unless law forbids the copying.

*Formal.* Let producing one unit of machine services require a units of machine services (a < 1: machines net-reproduce) and ℓ units of non-produced services (sites, energy, ore) renting at r. Free entry forces

> c = a·c + ℓ·r  ⟹  **c = ℓr / (1 − a)**.

With time preference δ (building takes a period): c = ℓr(1+δ)/(1 − a(1+δ)), finite iff a(1+δ) < 1. The wedge δ is interest — the wage of waiting — competitive, real, and thin. An idea's reproduction requires approximately nothing of anything, so its competitive price is approximately zero; any positive price is institutional scarcity, chosen rather than natural.

**Proof.** If machines sold above recipe cost, entrants would build machines with machines and undercut; below it, builders exit. The displayed equation is the zero-profit condition; solving it is one step. ∎ *(Honesty note: with many machine types this is a matrix equation c = Ac + Lr with solution through (I − A)⁻¹ — the same conclusion wearing linear algebra. The scalar carries the full logic.)*

**Corollary — the surviving-income taxonomy.** In the corner regime, gross income decomposes exactly into the essay's opening trichotomy: **physical scarcity** earns permanent rents (land, energy, sites, water); **institutional scarcity** earns whatever rents law elects to create (IP, licenses); **dynamic scarcity** earns transition rents while capacity builds — real, temporary, and "temporary" can mean decades (your nuclear plant). Plus thin interest. Wages have left the list. The taxonomy you opened the essay with turns out to be the classification of everything that survives it.

**Example.** Model weights are an idea; distillation pierces even trade secrecy, because the behavior leaks out through the product's own outputs. The datacenter sites, the power contracts, the water rights are physical. P2 says the market value migrates from the former to the latter — essay footnote 2, now a theorem's worked example, and a strong candidate for the body of the piece.

---

## 6. P3 — The fiscal system is a tributary of the labor loop

For each instrument i, let λ_i be the wage-linked share of its base (for transfers: of its eligibility). Given P1–P2, the following are accounting facts:

(i) In the corner regime the current-wage base shrinks toward participation × parity — toward zero in corner-below — so λ-weighted revenue contracts in proportion.

(ii) Eligibility scissors: work-history-conditioned claims contract with participation while need-based claims expand. Revenue and obligations cross like blades.

(iii) Instruments taxing **embodied past labor** — the structures share of property tax, consumption financed by drawdown of past-wage savings — keep yielding through the collapse and decay only at depreciation and drawdown rates. The fiscal cliff has a time constant, measured in years to decades. Cushion, not comfort.

(iv) VAT is the exception that matters: its base (consumption) survives, and its incidence migrates by itself to whatever finances consumption — which in the corner regime, by P2, is rents. The one instrument that follows the value without being redesigned.

The empirical content of this section is the λ measurement program (separate spec); the theoretical content is only this: **the fiscal state is a sub-circuit of the labor loop, and it thins when the loop does.**

---

## 7. P4 — Conditionality

**(i) The cancellation.** With an unconditional transfer u, the participation condition reads: work iff w + u ≥ s + u. The u appears on both sides and cancels — no margin moves — while the disposable floor rises by exactly u. And once u ≥ s, exit is feasible without woods or family: **the UBI is a purchased commons**, re-providing the outside option that enclosure priced away. *Honesty note: exact on the participation margin; if hours are chosen and leisure is a normal good, hours fall somewhat. Exact for whether, approximate for how much.*

**(ii) In-work benefits (paid b iff working).** The condition becomes w + b ≥ s: the reservation wage falls to s − b. In the *linked* regime, when the participation margin is populated, the influx pushes x* left and w down: part of b leaks away as lower wages. This is the Speenhamland result rebuilt honestly — no employer power required; the leak flows through the market's own margin, and it grows as ρ flattens. In the *corner* regime the wage is pinned, so no leak — but if s > c·ρ̄ ≥ s − b, the benefit summons work whose replacement value is c·ρ̄ from people whose time is worth s outside: society burns s − c·ρ̄ per hour to preserve the appearance of employment. **The failure mode is regime-dependent: leak when linked, make-work in the corner.**

**(iii) Out-of-work benefits (paid b′ iff not working).** The reservation rises to s + b′, and withdrawal-on-entry taxes the first hour at b′. As machine parity compresses the wage distribution toward the floor, the mass of workers sitting inside any fixed withdrawal band rises mechanically: **the same rulebook generates a worsening trap.** The dysfunction belongs to the regime, not the rules.

Proofs of all three are the displayed inequalities plus P1's comparative statics. ∎

---

## 8. P5 — Funding: the shell game and the resumed George

**(i) Wage-funded UBI in the corner regime: exact futility.** Labor demand is perfectly elastic at gross wage c·ρ̄ (P1ii), so a payroll or income tax t cannot pass to firms: workers' net wage is (1−t)·c·ρ̄, full incidence on labor. With full participation the transfer is u = t·c·ρ̄, so disposable income is

> (1−t)·c·ρ̄ + t·c·ρ̄ = c·ρ̄ — identically, for every t.

A wage-funded UBI in the corner regime is a closed loop through the same pockets. With *partial* participation it is worse than futile: u is spread over N people while the tax falls on fewer than N workers, so each worker's disposable income drops strictly below c·ρ̄; when it crosses s, marginal workers exit, the base shrinks, u falls — **the self-undermining spiral, running downhill at the margin.** ∎

**(ii) LVT-funded UBI: invariance.** Land's supply is fixed and its rent is a residual, so a tax on site rent capitalizes into the land *price* while leaving the rent flow and land use unchanged: **the base cannot contract in response to being taxed.** By P4(i), the UBI it funds moves no margin either. That conjunction — untaxable-away base, distortion-free transfer — is the theorem. The stronger claim (UBI spending raises land-using demand, which in the corner resolves into rents by P2, growing the base) is real but second-order: claim it as tendency, never as theorem.

**(iii) Necessity — George resumed.** P2's corollary is exhaustive: in the corner regime the non-empty funding bases are physical rents, institutional rents, transition rents, and thin interest. The wage column is blank. Funding transfers from rents on non-produced factors is therefore not a preference among options but the only column with anything in it. VAT participates indirectly, as §6(iv)'s migrated rent tax.

And the converse deserves equal billing: **in the linked regime, standard redistribution works roughly as advertised** — labor demand inelastic enough that taxes stick where aimed. The theory does not say the textbook was wrong; it says which regime the textbook was written in, and identifies the switch. Essay footnote 1's "the floor is always at subsistence" is exactly the corner case of this proposition: with N fixed and a steep schedule, a whole population can sit above s; flatten the schedule and the footnote comes true. The inflammatory footnote survives — as a regime statement, which is both more defensible and more useful.

---

## 9. The ledger of assumptions

Honest boundaries, each with its cost:

1. **Fixed task space.** Reinstatement is read as existing tasks crossing the waterline (essay footnote 5). Acemoglu–Restrepo would insist genuinely *new* tasks are history's counterweight; here that becomes a movement of ρ. A reinterpretation, and the single assumption a hostile economist will probe first.
2. **Homogeneous workers.** Heterogeneity = personal ρ schedules and personal s; every proposition holds type by type; distributional statements refer to the support.
3. **Checklist production (Leontief over tasks), one final good.** CES aggregation softens thresholds into bands; regimes and propositions survive.
4. **s exogenous but land-backed.** Enclosure lowers the outside option and manufactures desperate labor supply; P4(i) is its repair. The model contains the commons without having been asked to.
5. **Human-premium tasks.** A permanently steep patch of ρ where consumers insist on humans. Where the premium relies on enforced provenance it is institutional scarcity — chosen, revocable; and your normalization observation erodes the taste side. Treated throughout as transition buffer, not rescue. This is a judgment, flagged as yours.
6. **Hours margin.** P4(i)'s cancellation is exact for participation, approximate for hours.
7. **Closed economy.** Trade is wage arbitrage arriving before machine parity — same direction, earlier timing. One flag, no modeling.
8. **Transition dynamics unmodeled.** Dynamic scarcity is classified (P2 corollary) but not tracked; buildout-era rents and bottlenecks are real and belong to a sequel.
9. **The Pigouvian floor (the b in ax + b).** Deliberately *outside* the propositions: it is an externality-pricing add-on justified by standard Pigouvian logic, and the theory's novel content neither strengthens nor weakens it. The essay should present it as a companion, not a consequence.

---

## 10. Sentence → proposition map (for the rewrite)

| Essay language | Formal object |
|---|---|
| "the link," "capability non-uniformity" | the pair (ρ(x*), ρ′(x*)) — level and slope, P1 |
| "wages set by subsistence… optimized down to that" | P1(i) arbitrage + P1(iii) floor |
| the natural system that "raises the true minimum wage above subsistence" | steep ρ in the linked regime, P1(ii) |
| four historical arcs | §4, P1 read four times |
| footnote 4 (woods, mum) | the exit option s, structural in §1 |
| footnote 5 (reinstatement = augmentation) | fixed-task reinterpretation, ledger item 1 |
| footnote 2 (weights, datacenters) | P2 corollary + worked example |
| clothes / owner loop | P2: produced goods as embodied land + past labor |
| footnote 1 (redistribution "can never work") | P5(iii) corner case — survives as a regime statement |
| "8 to 1" | λ_C, pending the measurement program (§6, separate spec) |
| the land loop, LVT + UBI | P4(i) + P5(ii) |
| "George isn't just elegant, he's necessary" | P5(iii) |
| Pigouvian floor, ax + b | ledger item 9 — companion, not consequence |

---

## Where a referee would push, in order

1. Fixed task space (ledger 1) — the real fight.
2. P5(ii)'s tendency claim if overstated as theorem — hence stated as tendency.
3. The linked-regime leak magnitude in P4(ii) — qualitative here; quantifying it needs elasticities I recommend citing, not estimating.
4. "Nearly all site rent" as the capture condition — phrase as "the leak scales with the shortfall," which is what the model actually delivers.

Everything above those four lines, I would defend as written.
