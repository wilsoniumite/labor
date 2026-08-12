# Readability rewrite — working brief (context lifeboat)

Read this first if context was compressed. It contains everything needed to
continue the rewrite without the conversation.

## Mandate (Stella, 2026-08-06)

Rewrite the paper's dense sections for a reader who is an economist, not us.
NO veto window: "copy the original document, then work on a new one until YOU
are satisfied, not me." Original preserved at repo root:
`the_link_pre_rewrite_snapshot.html` (86,243 bytes). Live file being rewritten
IN PLACE: `link-repo/paper/the_link.html`. Delete-first method: rewriter
subagents get a section's JOB, never its current prose. Her diagnosis
(accepted): the prose models a reader who already holds the whole system —
poetic compression carries technical claims instead of crowning them.

## The allocation rule (the voice's terms of survival)

Every technical claim is stated once in plain economist's prose — subject,
verb, condition — BEFORE any compressed phrase. Poetry after proof, never
instead of it. Summits keep the voice (§1's wage sentence, "the corner is a
fork between two bookkeeping systems", section-ending crown lines). Climbs
lose it (multi-claim em-dash chains inside remarks and proofs).

## The reader persona (give verbatim to reader-simulation agents)

"Dr. R.: associate professor, labor/public economics. Knows Acemoglu–Restrepo
2018/2022/2026, Autor, Diamond–Mirrlees, the EITC/NIT literature. Skeptical of
Georgist framing. Has 40 minutes, reads linearly, skims proofs. Knows NOTHING
of this paper's private vocabulary (link, waterline, demolition, corner,
fortified, K, κ) until the paper teaches it — and forgets a definition unless
it was memorable or repeated. Stalls on: unglossed notation, three-clause
em-dash sentences, rhetoric substituting for statements, propositions that
open with algebra before saying what the object is for. Annoyed by both
over-poetry AND beige filler."

## Paper state (2026-08-06, post-review)

- `link-repo/paper/the_link.html`: §§1–11 + appendix + references. 2 lemmas +
  Props 1–13. FINAL numbering: 1–4 baseline, 5 closure (§5), 6 conditionality,
  7 funding, 8 feasibility, 9 enclosure, 10 mix (all §6), 11 Baumol fork (§9),
  12 open economy (§10), 13 welfare (§11). 15 remarks, 13 predictions,
  7 figures. Straight-quote typography ONLY. Unicode math, <sub>/<sup>.
  Bare rT fused; subscripted r·T_P / r·T_H keep the middle dot.
- Checks: `checks/` — ELEVEN files, all green. Run all:
  venv\Scripts\python.exe on each. NO rewrite may alter what a formula claims;
  formulas byte-preserved per job specs below.
- NOTES.md = canonical project state; changelog there after each phase.
- Records at root: *_section.html per unit + snapshots.

## Rewrite targets

FULL REWRITE (rewriter agents, delete-first) — T1–T5:
- T1 §4 fortification remark. Anchor: `<p><b>Remark (fortification: what the
  demolition leaves standing).</b>` … ends `most sheltered.)</p>`
- T2 §6 decomposition remark + insurance paragraph. Anchors: `<p><b>Remark
  (the decomposition, and the price of a moved margin).</b>` and the following
  `<p>Read against the demolition schedule…</p>`
- T3 §6 enclosure subsection body. Anchor: `<h3>The commons, priced</h3>`
  through the remark `…applied to the woods.)</p>` (intro ¶ + Prop 9 statement
  decompressed + proof + remark).
- T4 §6 mix subsection. Anchor: `<h3>The mix on the way down</h3>` through
  `…becomes more necessary.</p>` (intro ¶ + Prop 10 statement + proof +
  remark "what the VAT is for").
- T5 §9 K-fork subsection. Anchor: `<h3>The strongest objection, as a
  theorem</h3>` through `…taxes its own remedy.</p>` (intro + Prop 11 +
  proof + 2 remarks + κ-feedback ¶; κ-claim is the LEVEL claim "sits lower
  at every q" — the rate claim was refuted, never reintroduce it).

ON-RAMPS / STATEMENT DECOMPRESSION (lighter, single agent each) — T6–T9:
- T6 §5 closure subsection: add a 3–5 sentence on-ramp before Prop 5 ("what
  this identity will say and why overidentification is a feature"), decompress
  the proof's longest sentence. Body otherwise kept.
- T7 §6 feasibility subsection: on-ramp before Prop 8 (κ in words: can full
  rent capture buy everyone the bundle; the land-constraint-in-disguise
  punchline pre-stated), split statement (iii)'s long sentence.
- T8 §10 open economy: on-ramp sentence for "foreign wage = second machine
  rental on human capability" as an explicit conceptual move (Stella's
  workers/owners standard: pre-empt the misreading); decompress Prop 12(iii).
- T9 §11 welfare: decompress Prop 13's statement (one clause per claim);
  second-best remark split into shorter sentences. MORAL REMARK UNTOUCHED.

HANDS OFF: §§1–3, §4 body through the negative-sum ¶, Props 1–4 + proofs,
Lemma 1–2, moral remark (§11), predictions list, appendix, references,
abstract, figures/captions.

## Job specs (content each rewrite MUST state; formulas verbatim)

T1 fortification: Prop 2 governs price-wedges; wedge power that reaches the
feasible set (law/contract) exits its domain. Bargained power erodes with
replaceability (vetoes get sold → transition rents); statutes survive parity;
under pressure protection converts price→quantity, so the demolition FILTERS
the wedge stock toward legal form. Consequences: (a) punctuated adoption —
nothing moves until the gap clears the confrontation cost, then the stratum
goes at once; (b) drag compounds twice — a blocked task's forgone saving
grows toward full labor cost as machine costs fall, AND fortified sectors
(sheltered, non-tradable, Baumol-side) grow their expenditure share; (c) a
fortified wage is institutional rent in wage form — infra-marginal, taxable
as rent, revocable as law (Prop 3's corollary holds the column open). Manager
= limiting case (wedge-holder = adoption-decider; only entry/takeover
discipline; slowest under product-market shelter). Checks: check_fortification
W-i…W-iv.

T2 decomposition: any instrument = pair (m_w, m_e), payments in/out of work;
the worker's margin sees only Δ = m_w − m_e. Reservation wage R = s − Δ, or
s(y) − Δ with exit value rising in exit-state cash y (s′ ≥ 0). Exactly two
channels: ∂R/∂Δ = −1 (substitution, full strength always) and ∂R/∂y = s′
(income; near zero empirically — Hoynes and Rothstein, 2019). u is the unique
Δ = 0 instrument (zero compensated response as identity); b is Δ = b; b′ is
Δ = −b′ with income term reinforcing. Corner: every misplaced participation
hour burns |c·ρ̄ − s| in either direction (make-work below s per 6ii;
income-effect exit above it); deadweight = margin-moving × that price. Linked
regime: u's residual exit RAISES the base wage (Speenhamland reversed,
accruing to workers). Insurance ¶: work-conditioned claims pay only in the
state the collapse removes; exit-conditioned claims manufacture entries and
tax the first hour (6iii); u is written on no state; 7(ii) is the same
property on the base side. On-ramp hook for Dr. R: compensated vs
uncompensated responses; EITC/NIT language. Checks: check_conditionality.

T3 enclosure: s was exogenous through Prop 8 because land wasn't scarce at
the margin — the commons IS the idle margin (reservation rent zero). Setup:
autarkic keep s_0 needing h_e land; dependency floor s_d. Corner closes the
idle margin (T_P + T_H = T by 5i) → exit plot pays ruling rent:
s(q) = max(s_0 − q·h_e, s_d); enclosure completes at q_enc = (s_0 − s_d)/h_e
— finite machine progress kills the natural floor. The race: κ(q) rises (8i)
while s(q) falls; gap between q_enc and q* is a crowding question:
q_enc ≥ q* iff N ≤ q_enc·T/(g_s + q_enc·h_s); in the gap the George
instruments are rescue, not optimization. Remark content: falling s
manufactures desperate labor supply in the linked regime (Prop 1 statics —
the historical enclosure reading); 6(i)'s cancellation survives any s(q) but
u's meaning shifts to replacing the commons (bill = h_e·q); funding circle:
exit-plot rents are inside rT and h_s is in P_s — the flow that priced the
commons away buys it back; s_0-constant caveat (autarkic exit; σ-logic of
4(iii) covers machine-tooled exits). Checks: check_enclosure.

T4 mix: two instruments, two blind spots. LVT: reaches every site rent
(consumed or saved, any owner), zero margin (7ii), needs a cadastre, cannot
touch non-site rents (bottleneck profits, royalties). VAT: reaches whatever
finances consumption (incl. dynamic + institutional rents), no valuation
needed, but its wage-financed slice is a payroll tax in disguise (regime-dial
deadweight). Prop 10: (i) κ ≥ 1 → LVT alone; (ii) κ < 1 → t_L = 1,
t_V = N·P_s·(1−κ)/E, minimized deadweight ∝ λ_C·(1−κ)² at given
floor-to-consumption ratio — the transition cost is the PRODUCT OF THE TWO
MEASURED SERIES, both moving favorably (0.32 at (0.72, 0.33); 0.08 at, say,
(0.50, 0.60)); (iii) at the corner the bases merge by Prop 5's identity —
the instruments become one. Remark: VAT's job on the way down is the
non-site rents; that reach decays by construction (transition rents expire,
labor-attached institutional rents self-liquidate §4); weights travel;
frontier interior for the whole crossing. Checks: check_mix.

T5 K-fork: K ⊂ [0,1], measure k, wage w_K — tasks machines cannot hold, for
any reason (capability residue / preference / law). Prop 11: (i) Leontief ⇒
any K-touching good's cost → k·w_K/γ_L as m → 0; labor's cost share → 1
(Baumol derived, not assumed); (ii) CES fork: K-expenditure share → 1 (η<1),
θ (η=1), 0 (η>1) — the rescue forks on substitutability, not sentiment;
(iii) terminal expenditure splits between land services and K-labor; machine
share → 0; THE CORNER OF PROPS 3–8 IS THE K = ∅ BOUNDARY (the paper's whole
baseline is one edge of this theorem — say this plainly). Credence remark:
π_H ≤ min(φ_H, v·f/(1−v)); f → 0 kills the premium for every v < 1 (fakes,
not robots — Prop 2's self-liquidation by another door); survivable anchors:
provenance law (f > 0, = quantity exclusion, the fortified set) and
co-presence (v → 1); "what law reserves plus what bodies witness" may crown
AFTER the plain statement. Superstar remark: top share β + (1−β)/n, rising
at rate 1 − 1/n; median/mean = 1 − β; aggregate labor share can persist while
the median wage collapses — aggregate rescue, median demolition. κ-feedback:
a K-service term in P_s makes κ SIT LOWER at every q (LEVEL claim only — a
rate version was refuted by review; do not state it). Checks: check_kset.

## Added targets (Stella, 2026-08-06 second message)

- T10 ABSTRACT — "a diamond could be made": two candidates (fresh-from-
  inventory + tightened-current) judged by an editor persona + Dr. R.;
  I pick/merge. Content inventory in workflow wf_b7177f69-452's script;
  current count word "thirteen falsifiable predictions" verified correct.
- T11 INTRO STORY — §1 opens as a story before the claim: (1) classical
  economics (Ricardo margin logic, Malthus subsistence, George residual
  rent) was coherent bookkeeping for a world of roughly uniform capability;
  (2) the industrial revolution split capability violently and the wage
  became a price on the gap — the classical laws went DORMANT, not wrong
  (conditional, premise paused); (3) AI closes the non-uniformity — the
  premise returns, the paper is bookkeeping for the return; (4) WHO IS
  WRITING THIS — one restrained, matter-of-fact paragraph: idea and central
  claims the author's; formalization, proofs, computations, most sentences
  by an AI under her direction — the capability priced in the paper drafted
  the paper; foregrounds (does not replace) the AI-use endnote; (5) ends
  with the existing claim sentences VERBATIM ("your wage is the rental
  price of a machine…"). Consequences/roadmap paragraph unchanged after.
  Splice region: after '<h2>1. The claim</h2>' up to the '<p>Three
  consequences follow' paragraph.
- Run: wf_b7177f69-452, task w157omi1s (6 agents). Merge both into the
  paper together with T1–T9 output, same rules.

## Merge rules (fresh draft vs original, applied by merge step)

1. Fresh draft's structure wins by default.
2. Plain statement precedes any compressed form of the same claim.
3. Original lines graft ONLY as crowns (paragraph/section end), each pointing
   at a plain statement it crowns.
4. Formulas byte-identical to the job spec.
5. Cross-references and numbering unchanged (props/sections/figures as in
   Paper state above).
6. Straight quotes; house markup (.prop/.proof/.eq, bold-lead remarks,
   tombstone ∎).
7. Length ≤ 1.35× the replaced text.

## Satisfaction criteria (mine — no user veto)

- Dr. R. simulation over the full §4–§11 arc reports NO high-severity stalls.
- All eleven checks green after every splice batch.
- A claims-fidelity review (like the 2026-08-05 workflow) finds no rewritten
  sentence that says more or less than its covering check.
- My own read-through: every proposition opens with purpose before algebra;
  no remark carries >1 claim per sentence on average; summits intact.
- Iterate as needed ("I think it needs a bit more" is licensed).

## Progress

- [x] Snapshot taken (the_link_pre_rewrite_snapshot.html)
- [x] Brief written
- [x] NOTES decision entry (decisions log, 2026-08-06)
- [x] Phase A workflow launched — run ID wf_b84d9abe-30a, task wz4i6d980
      (T1–T5 write→read→revise pipelines; T6–T9 edit-pair drafts; 19 agents).
      On completion: result has {rewrites: [{key, final: {html, notes}}],
      onramps: [{key, edits: [{old_string, new_string, rationale}]}]}.
      Merge T1–T5 inline against the CURRENT paper text (originals are in
      the snapshot and in context), applying the merge rules above; splice;
      apply T6–T9 edit pairs (verify each old_string unique first); then
      checks + whole-arc Dr. R. pass + fidelity review.
- [x] Merge + splice T1–T5 (2026-08-06). All five accepted essentially as
      revised — the read→revise loop had already done the merge work. Notable
      upgrades beyond decompression: T1 defines "fortified" explicitly and
      reconciles contract-vs-statute (contracts fortify until expiry); T2
      separates output cost from excess burden (u: zero excess burden — burn
      is forgone output at stale pre-transfer s; sharpens, does not
      contradict, Prop 13(i)); T3 fixes the original's billing overstatement
      (u's bill caps at h_e·q_enc past enclosure) and adds the
      enclosure-can-precede-the-corner point; T4 resolves interior-vs-corner
      ("a corner in t_L, not a compromise; both bases carry weight") with
      new crown "The VAT is scaffolding"; T5 moves the CES setup into the
      statement, adds the economy-wide-median point and the 7(iii)
      credit-side tie, cites Rosen (1981) — ADDED to References. One tweak
      applied at splice (T3: "the remark's caveat (d)").
- [x] Splice T6–T9 (all 10 edit pairs applied: closure on-ramp + proof
      split + migration-paragraph split; feasibility on-ramp + (iii) split;
      open-economy conceptual-move on-ramp + (iii) seven-sentence split;
      Prop 13 purpose-first decompression + second-best remark splits).
- [x] Post-splice: ALL ELEVEN checks green; 15 prop divs / 15 remarks /
      13 predictions / 7 figures / 0 curly; key formulas verified present.
- [x] T10 abstract spliced: candidate A (fresh-written, judge's pick over
      the tightened-current and the current: only version that glosses "the
      tax-and-dividend pair"; 227 words vs 270) + the judge's three grafts
      (strata not stack; "crosses the participation margin";
      "profit-directed adoption targets"). Judge also caught that candidate
      B's compression "the corner is institutional" was WRONG (the corner
      arrives technologically; its character is institutional) — A's full
      phrasing kept.
- [x] T11 intro spliced: five paragraphs — classical bookkeeping (Ricardo/
      Malthus/George, "not a naive picture, bookkeeping for the world they
      had"); the industrial break ("the laws were not wrong; they were
      conditional"); AI as candidate reversal with the premise flagged
      empirical and at-risk (points at §9 and §8); the disclosure paragraph
      (idea/claims the author's; formalization, proofs, computations, most
      sentences by an AI under her direction; the check discipline stated;
      "the capability priced in this paper is the capability that drafted
      it"); close on the claim verbatim. Roadmap paragraph untouched after.
- [x] Post-splice: all ELEVEN checks green; 15/15/13/7 structure; 0 curly.
- [~] SATISFACTION GATE running: workflow wf_19050800-fd0 (task w6pr2w7kl)
      — arc-flow read, arc-skeptic referee pass, fidelity-body sweep
      (rewritten regions vs checks), fidelity-frame sweep (abstract/intro/
      on-ramps vs body and repo); findings refute-verified. On completion:
      fix confirmed findings, re-run checks, iterate if high stalls remain;
      then final NOTES changelog + records + report.
- [~] FIGURE REPAIR running in parallel (Stella: figs 1-5 have text/lines
      covering other text; 6-7 fine): workflow wf_8779537b-4cb (task
      w3zgspwg0) — 7 visual inspectors on the PNGs → single fixer iterating
      on code/make_figs.py (layout-only; content frozen; verifies each fix
      by re-reading the regenerated PNG) → 7 fresh-eyes verifiers. Touches
      only figure scripts + figures/ — no conflict with the satisfaction
      gate. On completion: skim final verdicts, regenerate any stragglers,
      note in NOTES changelog.
- [x] SATISFACTION GATE COMPLETE (2026-08-06): 12 confirmed findings all
      fixed (3 highs: SWT overclaim → "delivers what SWT promises",
      one-parameter family stated honestly; U-shape → calibration-not-
      confirmation; excess-burden ledger → new check D-v) + 3 elective;
      check coverage extended (D-v, N-vi, W-iv label); 18+1 paper edits;
      confirmation agent 13/13 PASS, no new defects; all ELEVEN checks
      green. SATISFIED per the criteria above. NOTES changelog written.
- [x] Figure repair complete: 20 collisions found (incl. 2 in fig 6), 18
      fixed layout-only with pixel-verified re-renders, 2 kept as intended
      pointing; all seven figures fresh-eyes clean; NOTES changelog written.
- [x] EVERYTHING DONE. Final report delivered 2026-08-06.
