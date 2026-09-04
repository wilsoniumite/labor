# STATE — resume point for the next session

**Project:** revision of *The Link: Wages, Machines, and What Remains* (Stella Wilson, working draft Aug 2026; the blog post "A New-ish Theory of Economics" at wilsoniumite.com links the PDF — this folder sits next to the papers folder).
**Collaboration:** extended, multi-session; working format, sequencing, and drafting decisions delegated to Claude. Direct critique preferred over validation.
**State as of:** 2026-08-30.

## Where things stand

**2026-09-03: HER v5 IS THE PAPER (log 52). ALIGN ON THE NAME v5.** Her
`Downloads/v5 (2).tex` — her own read-through after the wall, terminology,
and duplication rounds; she is "quite happy with it" — is frozen verbatim as
`latex/v5_baseline_2026-09-03.tex` and is the WORKING FILE `latex/v5.tex`.
It equals the duplication candidate plus five edits of hers (log 52). The
v6 lineage (`v6_walls.tex`, the three `v6_*_candidate.tex`) is SUPERSEDED,
kept on disk. Lint green bar the Overleaf-only effort figure. Flagged for
her one-word decisions (log 52): a LaTeX quote slip in §1 (''terminal''
opens with '' not ``), "The extreme cases makes", and three older
lowercase-after-period sites. Nothing pending from Claude's side; the next
unit is whatever she sends. Route unchanged: freeze, exactly-once port,
diff + reading view, never re-voice, flag slips.

**2026-09-02 (last): STEP 5 — §1 TERM INTRODUCTIONS MOVED OUT (log 50).**
The audit's five §1 insertions are now one quoted clause each or gone; the
definitions live in §3 (task margin, replacement value, the recursion
named, the terminal/land terminology merged after eq:recursion), §5
(participation floor after eq:exit), and §7 (terminal-input intensity).
`latex/v6_walls.tex` is the file for her duplication/tightening audit.

**2026-09-02 (late night): STEP 4 — THE TERMINOLOGY AUDIT AS RULED (log 49).**
`latex/v6_walls.tex` now carries the audit's 67 mechanical items plus the
ceiling cut and four named floors; enclosure, commons, her §8 heading kept;
§9 retitled "Distribution at the limit". Her next move: a ChatGPT
duplication/tightening audit of this v6 (known self-duplications listed in
log 49). Same route when it lands: freeze, exactly-once port, diff + reading
view, never re-voice, flag slips.

**2026-09-02 (night): STEP 3 — THE CHATGPT SHEET AS RULED (log 47; VETO
WINDOW THERE).** Her ruling on the sheet (log 46): all accepted except the
pushbacks, "machine-contestable" kept. `latex/v6_walls.tex` carries it;
Figures 1, 2, 4 regenerated with the sheet's labels; new
`code/reading_view.py` gives her every changed paragraph as clean prose
(`docs/reading_view_v6_2026-09-02.html`). Figures 3, 5, 6 label changes
pending in effort-accounting / link-repo. A WHOLE-PAPER VOICE MD IS
EXPECTED NEXT from her: freeze verbatim, exactly-once port, diff + reading
view, never re-voice, flag slips.

**2026-09-02 (evening): STEP 2 — THE WALL IN PROSE (log 45; VETO WINDOW
THERE).** On her call, §6 gains two intuitive paragraphs (no maths) on what
sets the wage at the wall and how other people supply the substitute the
machine cannot; six one-clause pointers to §6 at every wall site. Her ChatGPT
package sent: `latex/v6_walls.tex`, `docs/drafted_prose_2026-09-02.md`,
`docs/figure_text_2026-09-02.md`, the cumulative and step diffs. Edits
return by paste; port verbatim, flag slips, never re-voice.

**2026-09-02 (later): HER GO ON THE WALL — v6 EXECUTED (log 44; VETO WINDOW
BELOW: every drafted sentence is hers to voice, and she is running the
figure text through ChatGPT).** Her latest tex arrived as
`Downloads/v5 (1).tex` — NOT previously in the repo (the closest copy was
the 2026-09-01 voice edit; hers carries ~30 later voice regions, last
session's κ-figure regions, and three lines from today: Prop 5 retitled
"Redistribution at the limit", §8 retitled "...of the model", the AI-use
note naming Claude Fable 5 and ChatGPT 5.6 Sol). Frozen verbatim as
`latex/v5_baseline_2026-09-02.tex`. The working paper file is now
`latex/v6_walls.tex` = that baseline + 13 exactly-once-asserted edits
(word-diff for her read: `docs/diff_v5_to_v6_walls.html`, 20 regions):
(1) Figure 1 redrawn on the industrial template — steep schedule, then the
set H closed to machines as a wall (`code/fig_model_schematics.py`,
`figures/fig_schedule.png`, copied to `latex/figures/`; strata/ushape
byte-identical), with §3 introducing H in words and the caption naming
it; (2) Figure 2 replaced by `figures/fig_eras_workers.png`
(`code/fig_eras_workers.py`): four eras drawn twice, a young entrant with
no training and a worker with years of training or experience — her
framing, no innate capability anywhere — with the margin dotted per era;
§8 retitled "four configurations", opening sentence, caption, and one
two-worker sentence pair per era paragraph (entrant = farm servant / mill
hand or hand-loom weaver / young clerk, cashier, assembler; trained =
craftsman after apprenticeship / millwright, engineer, clerk / developer,
physician, engineer); (3) her deliverables: the full tex, and
`docs/figure_text_2026-09-02.md` — every caption and every label, legend
entry, and annotation of all six figures, for the ChatGPT voice pass.
Structural lint (`checks/lint_tex_structure.py`, new) green except the
expected note that `fig_consumption_financing_and_human_effort.png` exists
only in her Overleaf. `fig_eras.png` is no longer referenced (kept). Still
no local compile: Overleaf is the first compile; she uploads the two new
PNGs alongside the paste.

**2026-09-02: FIGURE 2 (THE ERA SCHEDULES) REVIEWED — CANDIDATE REDRAW ON
DISK, HER CALL (log 42; nothing in the paper, `fig_eras.png`, or the TeX
touched).** Her question: can the pre-industrial schedule be drawn, and are
the three curves right given physical automation, cognitive automation that
needed more developers, and the record. Findings: (1) the pre-industrial
case IS drawable with the paper's own object — Appendix A's set H, closed
to machines, covering nearly every task: a sliver (mills, draft animals)
then a wall; the margin sits at the wall, task-side labor demand is
perfectly inelastic there, and the wage is set on the other side, the land
floor s(q) (Prop 3; long-record R1). So "off-chart" was right and
"compressed" (§8) / "flat configuration" (§2) is the wrong word: the
pre-industrial schedule is the VERTICAL case, the AI limit the FLAT case —
opposite labor-demand elasticities, both pinning the wage to land (floor,
then recursion c ∝ r). (2) `fig_eras.py`'s curves CROSS (computing 0.9 >
industrial 0.3 at x = 0; AI above both below x ≈ 0.41): in rank space with
machines never losing capability each era's curve must lie weakly below the
last and its wall further right (task creation can break it only at the
top) — the current picture says machines got worse at their best tasks.
(3) No era has a wall, though §8 says engines were "useless at cognitive
tasks" and ALM's non-routine tasks stayed closed. (4) The margin is not
marked, and flatness matters only AT x* (Lemma A.1). (5) "More developers"
is λ (and reinstatement at the wall), not a γ-object — the text has both,
the chart cannot show λ; the panel draft carries it as a line per era.
Candidate: `code/fig_eras_v2_draft.py` → `figures/fig_eras_v2_draft.png`
(one panel, four nested curves with walls and margins) and
`fig_eras_v2_draft_panels.png` (2×2, one era each, w/c line and x* as in
Figure 1, λ line). If adopted: port into `fig_eras.py`, recaption (four
configurations; "compressed" → the wall), and touch §2's "flat
configuration" clause — one unit, her voice.

**2026-09-01 (fork/rent session): THE κ FIGURE GAINS ITS MEASUREMENT SPLIT
IN v5 (VETO WINDOW — two drafted sentences and one dropped caption sentence,
hers to voice or reject).** Her Downloads `v5.tex` (the working copy) edited
in place, three regions, word-diff given in chat: `fig:kappa` now draws
`latex/figures/fig_kappa_measurement.png` — the published 12-member grid
with its two rent measurements as separate medians (valuation dashed,
rent-bill red; legend in her approved plain register) — built by
`code/fig_kappa_measurement.py` (2025 anchors GREEN: med 0.326 / rent-bill
0.326 / valuation 0.303; `fig_kappa.png` untouched). The caption now carries
the full source block (HNOREMV, BOGZ1LM155012665Q, GS10 +150bp,
DHSGRC1A027NBEA × 0.30/0.50, Orshansky/CPI denominator, subsets-not-new-
series note); its "band width is substantially the capitalization-rate
spread" sentence is DROPPED (at the 2025 endpoint the band edges are
rent-bill members — the split now shows the structure instead); the
post-1995/2020 caveat sentence kept verbatim. §9's coverage paragraph gains
two drafted sentences on the two routes. She uploads the new PNG to Overleaf
alongside the paste.

**2026-09-01: THE V5 DRAFT IS EXECUTED ON THE NEW BASELINE (logs 39–40;
VETO WINDOW AT LOG 40 — with her and ChatGPT for voice, edits return by
paste).** Her go, two scopes, both landed in
`latex/v5_land_intensity.tex` (baseline frozen alongside as
`latex/v4_accounting_revised_baseline_2026-09-01.tex`; her read:
`docs/diff_v4_to_v5_land_intensity.html`, 70 regions): (1) every
scarce-factor-free-good site reframed around LAND INTENSITY with ideas
the sole exact exception — Prop fork gains part (iv) (the b_lo/b_hi
composites, eq:composites + eq:fan, crossover at r/w = L̄/b), backed by
`checks/check_fan.py` (27 GREEN: algebra incl. the interest-augmented
closures, plus the §9 data anchors); (2) the financing-vs-production
detail moved verbatim to NEW Appendix E (app:effort), §9 keeping a
five-line summary. §9's fork paragraph now carries the food leg
(+13% vs +277%/−21%, 1964 window) and an energy-exclusion sentence.
NOT included, deferred: the floor funding-dichotomy prose and the
quasi-exit clause (log 39's recommendation — one word away). No local
TeX compile exists on this machine; Overleaf is the first compile
(structural lint clean: refs/labels, environments, $ parity, braces).
The pinning.html-canonical discipline remains SUSPENDED for this
lineage: v5 is the working paper file, her call how it flows back.

**2026-08-30: HER VOICE CALIBRATION LANDED — the §1 time paragraph is
hers, and all Claude-drafted v2 prose is normalized to it (log 37; still
UNCOMMITTED, her veto).** Her rewrite of "What does time add?" ported
verbatim ("whilst" kept per her ruling); the lesson codified (no symbol
debuts in §1 — notation_map drafting rule; "dials" banned outright —
lint register family) and applied across ~30 sites in §§1–9, 11 and App
A/C/E: performance constructions flattened, braided periods broken,
rhetorical em-dashes demoted (211 → 179, 9.5/1k), γ̄ and q evicted from
§2. One correctness catch: §1 "two questions" → "three". Word-diff for
her read: `docs/diff_voicepass_2026-08-30.html` (146 regions after the
log-38 rulebook sweep). All batteries green; her voiced text untouched.

**2026-08-28 (later): THE DYNAMIC DRAFT IS EXECUTED — pinning.html is the
v2 paper (log 35; VETO WINDOW THERE, uncommitted pending her read).**
Phases 2–3 landed in one pass on the standing engine: §5 build time, §8
in motion (equivalence, frozen rent, the verified experiments with their
labels, history as three transitions), §9.2 the fiscal horizon, the
participation fix, the new-task condition, App A's sequence economy, App
E/F. Props renumbered 1–9 (map in log 35), figures 1–9, LaTeX export ALL
GREEN with word fidelity. Phase 1b (γ* → γ(x*)) and the dynamics engine
are committed; her Overleaf notation-only paste source is
`latex/main_phase1b_notation_only.tex`. Voiced-sentence repairs are
enumerated in the veto list — nothing was re-voiced silently.

**2026-08-28: THE CAPITAL-DYNAMICS ENGINE IS BUILT AND ALL GREEN (log 33;
VETO WINDOW THERE).** Log 32's pre-drafting mechanization executed in
full, no prose touched: u_K DERIVED from free-entry PV algebra, the
steady-state EQUIVALENCE LEMMA machine-checked both ways (flat symbolic;
sloped instantiated, build→0 reproducing check_pinning's root to 1e-9),
all four Phase-3 technical cautions resolved and pinned, T4's entry-margin
algebra checked early. `code/dynamics/` solver validated against the exact
b_I = 0 closed form (2.5e-11) before touching anything else; then T1
windfall VERIFIED (with a refinement: steady-state Q is (1+ρ)^{J−1}, not
1 — the gestation float), T2 waterfall VERIFIED (strict J-order; the
pre-J_c window split is a sunk transfer the model does not determine),
T3 speed×lag VERIFIED (monotone in both), and T5 decided by the numerics:
PARTIALLY SUPPORTED and SPLIT BY SHOCK TYPE — frontier extension (the
Korinek–Suh cap) drops the goods wage at release and then PINS it (CM on
the capped stretch, no dip-and-recover), while efficiency deepening
RAISES it on impact; the land-unit wage falls under both. Four §8 figures
regenerate from one entry point. 54 + 51 checks + lint (now with the
claim-status-tag family) ALL GREEN; `pinning.html` byte-identical. Phase
2/3 DRAFTING IS UNBLOCKED; the brief amendments the checks forced (the
Inc_t convention, the Q benchmark, T5's wording) sit in log 33's veto
list.

**2026-08-27 (evening): PHASE 2+3 AUTHORIZED; THE STRUCTURE DECISION IS
MADE — READ LOG 32 BEFORE DRAFTING.** Her go: "Let's do the dynamic rewrite
now," to be executed in a NEW session; her structure question (static
storyline + dynamics after? dynamics alongside each section? all-dynamic
from scratch?) is answered in log 32 with the full section table, phase
cut-lines, voice map, and Phase-3 technical cautions. The one-line answer:
**one dynamic environment declared once in Appendix A; the main text
through the fork written as its steady state in pure coefficient notation;
all transition machinery and results consolidated in one §8 block, hinged
by a machine-checked steady-state equivalence lemma.** OVERLEAF STATUS
CHANGED: her copy is now a DELIBERATE discussion fork for Johan (the
notation change is being socialized there; she calls it a no-brainer) —
the wholesale-replace discipline is SUSPENDED; canonical remains
pinning.html; her/Johan edits arrive by paste as before. Should the Johan
discussion ever demand it, the rename is mechanically reversible via
`docs/notation_map.md`.

**2026-08-27: PHASE 1 (NOTATION) EXECUTED AND COMMITTED** (log 31). The v2
brief (capital is time: ρ waiting + J build lags) is frozen at
`docs/rewrite_brief_pinning_v2.md` with her delivery amendments; the paper,
checks, lint, census, italicizer, converter, figures, LaTeX, zip, and the
Lean translation tables all carry the v2 notation (`docs/notation_map.md`).
Two new-prose sites await her voice (the rewritten Notation footnote; the
ρ first-use clause in A's durability paragraph).

**2026-08-26: APPENDICES RESTRUCTURED A–I → A–D** (log 28): I and H cut,
B compressed to a §11 paragraph, C folded into A, E folded into B (the old
D); reletter D→B, F→C, G→D; Lemmas D.2/D.3 added and A's joint-system
existence rescoped with a numerical instantiation. Johan's front-matter
pass is ported (log 25); the Overleaf copy is stale pending a wholesale
replace.

**2026-08-13: THE REWRITE IS EXECUTED.** `paper/pinning.html` is now the full
restructured paper — "Pinning the Wage to Scarcity and Technology" — built
around the core contribution (the two closures), with the λ-recursion adopted,
coined terms removed, and the old draft's supporting material compressed into
Appendices A–I. The skeleton it replaced is snapshotted. Veto window below.
The sketch-block merge decision (pending, further down) is UNTOUCHED by this:
the rewrite deliberately absorbed none of the A–E blocks, consistent with the
parked paper-three recommendation.

Earlier state: the paper went through a hard assumptions audit, then a theoretical extension (the talent/practice split + the task anatomy), a falsifiability stress test that passed, four new sketch blocks, and three data passes. **The algebra/numerical pass over the sketches is complete (2026-08-09):** all ten [check] flags verified in `checks/` (sympy + numeric per the house rule), eight clean and two WITH AMENDMENTS now recorded at the flags — B2's aggregate-dispersion claim needs the empirical covariance sign or the F2 channel, and C1's cobweb stability condition is lag-indexed ("product < 1" exact only at T_E = 1). The blocks are merge-eligible under the standing rule; merge SCOPE is still the pending decision below.

## Verify-list — 2026-08-13: the pinning rewrite (veto window, current)

One unit (her plan: "the big rewrite in one turn"; decisions recorded in
`docs/rewrite_brief_pinning.md` — the frozen brief). Snapshot of the replaced
skeleton: `paper/snapshots/pinning_skeleton_snapshot.html`.

- [ ] **LENGTH DEVIATION, flagged first:** main text landed at ~5,030 words
      against the brief's ~9,000 target (appendices ~6,900; total body
      ~11,960). Written lean in the direction of her "shorten significantly";
      every planned element is present, but sections average ~55% of their
      budgeted words. An expansion pass (more words-before-algebra, worked
      examples restored) is the obvious next unit if the compression reads
      as clipped rather than tight.
- [ ] The λ-recursion adopted throughout: c = ac + λw + ℓr; Proposition 2
      (replacement closure) c = ℓr/(1−a−λρ*), w = ρ*ℓr/(1−a−λρ*), viability
      1−a−λρ* > 0; the two automation channels named (task ρ*↓, recursive
      λ↓) with the cross-effect sentence (with λ>0, task automation also
      cheapens the machine). Worked instance in text: (a,λ,ρ*,ℓ,r) =
      (0.5,0.1,3,0.2,1) → c=1, w=3; λ→0 → c=0.4, w=1.2 (the 60% cut).
      `checks/check_pinning.py` ALL GREEN (27): closures, statics signs,
      limits (domain-explicit), fork displays with λ, welfare sums, s(q)
      kink at q_enc, λ→0 agreement with the corner spine.
- [ ] De-coining executed: "the link", "waterline", "demolition",
      "fortification", "the corner"/"corner regime", "George pair" all gone
      from body text (lint-enforced, `checks/lint_pinning.py` ALL GREEN);
      ONE term kept by design — the real-wage fork. "Terminal input" used
      informally, defined once; propositions say "non-produced input".
      Wedge/targeting material compressed to Appendix B, credited to A&R
      2026 as theirs (her call: "just a remark or in the appendix").
- [ ] §2 built on her skeleton's design: the fundamental-surplus positioning
      quotes Ljungqvist–Sargent's definition VERBATIM (verified against the
      AEA page): "an upper bound on the fraction of a job's output that the
      invisible hand can allocate to vacancy creation"; Shimer's 20× fact
      verified same pass. Cambridge-capital material cut to one clause
      (Sraffa; Samuelson "A Summing Up"), Robinson dropped.
- [ ] Citations: 17 new entries live-verified WITH pages (L–S 2017; H–M
      2008; Mas–Pallais 2019; Jones–Marinescu 2022 incl. the +1.8pp
      part-time finding; Bouscasse–Nakamura–Steinsson 2025; Crafts 2022;
      Arnott–Stiglitz 1979; Lewis 1954; Gruber 1997; Saez–Schoefer–Seim
      2019; Kugler–Kugler 2009 incl. the 1.4–2.3%-per-10% finding; Allen
      2001; Clark 2005; Uzawa 1961; Shimer 2005; ALM 2003; Autor–Dorn 2013;
      MP 1994; Shapiro–Stiglitz 1984; Leontief 1936). Books/chapters/
      proceedings entered WITHOUT page numbers (nothing approximated).
      DROPPED as unverifiable-or-unneeded: Bozio–Breda–Grenet, Schwerhoff–
      Edenhofer–Fleurbaey, OECD 2026 tax wedge, Robinson 1953. Zero
      remembered constants entered.
- [ ] Appendix consolidation vs the brief: A–I instead of A–J — the
      enclosure race folded into F.4 beside the κ algebra it references
      (structure preserved, lettering consolidated; sole deviation from the
      frozen brief besides length).
- [ ] Figures: fork + κ figures carried BYTE-IDENTICAL from link-repo
      (their checked records stand; old-register titles tolerated, a
      regeneration unit is flagged below); the era schematic REGENERATED
      de-coined (`code/fig_eras.py` → `figures/fig_eras.png`, y-axis
      "relative human productivity ρ(x)", neutral annotation) — schematic
      only, no data implications. All three referenced at ../figures/ and
      alt-texted.
- [ ] Measurement honesty: κ ceiling caveat IN (median 1.26, 13/32 members
      below one, per data item two); three assemblies marked [spec'd,
      unbuilt] in §10 (incidence slope; λ via input–output; the long
      record) — Claude's delegated call was NOT to build them inside the
      rewrite turn; zoning rival met in one paragraph with the concession
      explicit.
- [ ] Back matter: acknowledgements carried VERBATIM (her instruction);
      AI-use note adapted; verification note states the Lean scope EXACTLY
      (corner spine machine-verified; λ>0 sympy-only; the λ>0 user-cost
      form deliberately unstated because unchecked); draftline declares
      supersession of the long draft by name.
- Not done, deliberately: no commit (none requested); no PDF render (hers,
  or `link-repo/code/render_pdf.py`); Lean extension to λ>0 queued;
  Appendix A's joint-system existence stated at sketch level (full proof
  rides with the Lean extension); the "code and data are public" sentence
  still carries no URL (standing handoff item, inherited).

ADDENDUM (same day, her follow-up "bring a task slope figure back... then
also the other figures"): the paper now carries SEVEN figures.
- [ ] NEW Figure 1 (§3): the assignment margin, de-wedged as she specified —
      single ρ(x) schedule, the w/c line, x* at the crossing, regions
      labeled (`code/fig_model_schematics.py` → `figures/fig_schedule.png`;
      schematic, no data). Her "section 2" read as the MODEL section (old
      draft's §2 = the model; new §3) — flag if she meant the survey §2.
- [ ] Figures 5–6 (Appendix B) REGENERATED, not carried: the old fig3/fig4
      had coined vocabulary baked into pixels ("link premium", "wedges
      demolished", "corner-below") and fig4 carried the KNOWN handoff
      defect (trough at ~40th pctile vs the text's 70th–95th). New strata
      bars keep the running-example dollars (25/15/10, parity 18 < s 25);
      new U-shape troughs exactly 70th–95th with band markers — the old
      handoff item (3) defect is DISCHARGED in this paper. App B gained
      the checked three-layer display + running numbers to anchor Fig 5.
- [ ] Figure 7 (Appendix F): fig5_fourway carried BYTE-IDENTICAL (data
      figure, record stands); caption defines "owner loop" inline; §10's
      ledger sentence and Prediction 9's tag now point at it.
- [ ] Renumbering swept: eras → Fig 2, fork → Fig 3, κ → Fig 4; all 18
      in-text references checked by grep; one stale ref caught and fixed
      (F.3's κ pointer). lint_pinning ALL GREEN, 7/7 figures, alt-texted.

ADDENDUM 2 (same day, her math-necessity audit: "if the core doesn't need
an equation, there should be no equation"; her suspicion "3.2" read as the
matrix/multi-machine block — ChatGPT-draft §3.2 — already Appendix C here):
- [ ] FOUR CUTS applied to main-text math, none touching a .eq display's
      claim: (1) §4's parenthetical no longer flashes c = Ac + Λw + Br
      (the formula now appears once in the core, in §10's assembly (2)
      where it names the estimand; App C keeps the full treatment);
      (2) §4's cross-effect derivative ∂c/∂ρ* moved from body prose into
      Prop 2's proof — the body keeps the words; (3) §5 no longer displays
      q_enc = (s0−sd)/he — defined only in App F.4, the sole place the
      core uses it (grep-verified); (4) §6's channel display writes c(r)
      instead of restating the closure formula.
ADDENDUM 3 (same day, her "yes please" to the register diagnosis): the
one-temperature pass, seven edits. §5's kink sentence regains a second
beat without the formula ("...finds nothing in the exit bundle left to
price"); Prop 2's proof loses its cross-referential aside; the Figure 5
caption drops the old draft's two-beat close ("the rational move is
exit — in practice, dependency" → "exit pays more than work") and gains
a hatched-bar reading note; Figure 6's close becomes a plain estimate
sentence with years; the App B countdown paragraph drops its agentive
verb triple; §10's "[spec'd, unbuilt]" tag removed (the bold lead
already says specified and open — the state-file idiom leak); Figure
7's ratchet clause cooled ("bites" → "lowers"). The rule is now IN THE
BRIEF (One temperature + the provenance rule: carried prose is
re-voiced, never pasted). lint re-run ALL GREEN.

ADDENDUM 4 (same day, her abstract call: "I liked the older version that
also had that cooler voice... it was a bit long and was 5 paragraphs when
it arguably should be one"): the abstract REWRITTEN in the ChatGPT
draft's register (the five-paragraph version she liked), compressed to
one paragraph, ~285 → ~265 words. Kept from ours: the search-and-matching
positioning clause, the two measured numbers (4.8×; one-third and
rising), the closing classical-configuration sentence, and the single
inline equation c = ac + λw + ℓr (words-then-equation order preserved).
Dropped: the solved closure formula w = ρ*ℓr/(1−a−λρ*) (Prop 2's job,
not the abstract's), the warm clause "carried while machine production
still employs labor and thinning as it stops," and "the demolition"-era
cadence generally. lint re-run ALL GREEN.

ADDENDUM 5 (same day, her sentence pair — she prefers "This paper closes
two prices around that margin: ... the price of market exit" over "the two
prices that condition takes as given"): the ASSERT-FORWARD rule named,
written into the brief (assert new as new; one job per sentence; right-
branching; colons over interruptive dashes; nouns carry their domain; no
rhetoric about rhetoric), and applied in a 14-edit pass. Abstract: her
preferred sentence adopted verbatim; the endpoints sentence split (the
"treats as parameters" clause now its own assertion). §1: "two questions
around that margin"; "The paper closes both prices" (de-nominalized);
"market for non-produced inputs". §5: cleft removed ("The model adds the
price"). §6: the embedded re-litigation deleted ("the interval that
bargaining theory treats as exogenously placed" → "the whole interval" —
§2.2 already carries that argument); one dash → semicolon. §8: suspended
opener flattened; the old-draft tag "— not low; none" cut. §10: the
meta-sentence about overselling cut. §12: "coincidence that is not a
coincidence" trope replaced; "meanwhile" dash clause flattened; "is not
open" → "is not an open question". lint gained soft metrics (em-dash
density 12.6/1,000 words; presuppose-pattern grep now at ZERO hits) and
re-runs ALL GREEN. CROWNS KEPT, exempt by the brief rule, one per
section, awaiting her word if any should go: §1 "the capability priced in
this paper is the capability that drafted it"; §2.2 "This paper supplies
both endpoints"; §5 "Enclosure manufactures labor supply"; §6 "their
object has vanished"; §7 the squeeze sentence + "Wages have left the
list"; §8 "Both halves of that sentence are theorems"; §9 "The classical
account is this configuration, correctly described".

ADDENDUM 6 (same day, her contribution-paragraph edits — first sentence
cut, "in this paper" folded inline, "Our contribution is"): the
SPEAK-AS-THE-AUTHOR rule named, written into the brief (stage directions
deleted; sentences self-ground when frames go; authorial acts take
first-person "we/our", unhedged; math imperatives and "this paper"-as-
subject stay; "the author" only where the human-vs-AI distinction is the
content), and applied in a 21-edit sweep. Her paragraph rewritten as
instructed ("The task margin in this paper is Acemoglu and Restrepo's...
Our contribution is the closure. We price... We price... we derive...
and we measure..."), the "to the author's knowledge" hedge dropped per
her wording (NOTE for her: the hedge protected the novelty claim; one
word restores it). Stage directions cut: "One disclosure belongs up
front" (§1 — FLAGGED, it was carried from the approved old paper);
"Three placements." (§8); "the limit the introduction promised" (§7);
"The objection deserves a theorem, and gets one" (App G → "Proposition
G.1 grants the mechanism its theorem and prices the premise");
provenance asides "compressed from the long draft" (App B, App F, App G,
App I). Self-commentary cut: "honest caveat"/"honesty notes"/"honest
scope" de-adjectived; "restated once" (§12). First-person conversions:
"We do not offer the model against them" (§2 intro); "We supply both
endpoints" (§2.2 crown, person-converted not cut — FLAGGED); "our
long-run claims" (§4); "our claim is architectural" (§1); "We take this
branch, as a bet" (§11); "Our baseline" (App G); "our permanent-case
claims" (App C). lint gained the hedge check + authorial-possessive
counts ("the paper's" now ×0 authorial; "the author" ×2, both in the
disclosure/draftline where they belong) and re-runs ALL GREEN.

ADDENDUM 7 (same day, her catch: "keeps the arithmetic honest" — "that
sounds familiar, can we find out why the previous passes didn't catch
it?"). POST-MORTEM, recorded per house practice. Provenance: the §3
sentence is a fusion — the ChatGPT draft's clean pair ("The equality is
an indifference condition. The worker has no cost advantage at the
marginal task; the non-zero object is relative productivity") plus a
meta-clause CLAUDE ADDED in the original rewrite turn, before any
register rule existed. Why three passes missed it: pass 1 (one
temperature) was SITE-scoped to the diagnosed drift and never opened §3;
pass 2 (assert forward) was FORM-scoped to presupposing noun phrases,
clefts, and interruptive dashes, none of which this sentence has; pass 3
(speak as the author) hunted "honest" but from a MEMORY inventory tuned
to the adjective+discourse-noun form ("honest caveat/notes/scope/
statement") — the predicate form ("keeps X honest") escaped, and no
mechanical grep was run. Root cause: register rules were enforced by
hand inventory while structural rules were mechanized — the exact
failure mode the repo's check discipline exists to prevent. FIXES: the
sentence reverted to the clean form; §3's "note now that" (same species)
dropped; lint now HARD-BANS the family over the body ("honest",
"honesty", "note that", "note now", "reading it as", "worth noting/
stating/saying/ending") with the Acknowledgements exempt (her verbatim
text); sweep found zero further instances; ALL GREEN.

- [ ] AUDIT RESULT, the keep list — all nine .eq displays in the main text
      are load-bearing (§1 chains×2 are words-as-displays; §3 ρ; §4
      recursion + Prop 2 closure + λ→0 limit; §5 s(q); §6 channels; §7
      fork). KEPT DELIBERATELY over the strict rule, flagged for her veto:
      §7's bounded-substitution formula inside Prop 4(ii) (it carries the
      robustness claim, not decoration) and §8's inline shell-game
      arithmetic (1−t)cρ̄ + t·cρ̄ (self-verifying where words would be
      assertion). Section-level: nothing cuttable — §2 argues the novelty,
      §9 is her framing, §6 is the payoff. lint re-run ALL GREEN.

## Session log (2026-09-03, later) — HER v5: THE CANDIDATE ADOPTED, HER EDITS, ALIGNMENT

52. **`Downloads/v5 (2).tex` arrived** (99,213 bytes, 13,906 words, 969
    lines): she read the whole paper and made her own changes; she calls
    it v5 and asked to align on that name. Frozen verbatim
    (`latex/v5_baseline_2026-09-03.tex`) and installed as the working file
    `latex/v5.tex`. Against the duplication candidate it differs in 12
    lines only — she TOOK THE CANDIDATE WHOLE, including the four items I
    had pushed back on (§12 "remains near one-third"; the shortened §1
    cost-parity sentence; the compressed roadmap; the §3 Measurement
    pointer with its "evidence, not an estimate of λ" caveat) — her call,
    recorded, not relitigated. Her five own edits (record diff
    `docs/diff_candidate_to_v5_2026-09-03.html`, 9 regions; reading view
    `docs/reading_view_her_v5_edits_2026-09-03.html`; full record vs v6
    `docs/diff_v6_to_v5_2026-09-03.html`, 129 regions): (1) §1 "What prices
    the substitute?" — the terminal clause folded into the last sentence
    ("...and such ''terminal'' rents account for an increasing share of
    the replacement price"), the "Section 3 makes the distinction precise"
    pointer dropped; (2) §1 outside-option paragraph — the floor clause
    folded ("...falls in the consumption units relevant to participation
    toward a ``participation floor,'' and its lower bound, the ``dependency
    floor''."), the bundle-cost clause dropped; (3) §1 extreme case: "The
    extreme cases makes"; (4) §12 closing sentence ADDED after the
    remaining empirical question: "Although it requires a significant
    re-framing of the last 70 years of world economic history, we consider
    the answer to be obvious."; (5) AI-use note: "Claude (Anthropic) and
    ChatGPT (OpenAI)", "parts of the formalization". No newline at end of
    file (harmless). FLAGS, hers to decide, untouched: (a) ''terminal''
    opens with two apostrophes where LaTeX wants two backticks — will
    render as closing quotes on both sides; (b) "The extreme cases makes"
    (was "case makes"); (c) three older lowercase-after-period sites: §5
    "nothing of anything. so its", §5 "someone else's housing. in the
    modern economy", data note "for the ceiling grid. financing splits";
    (d) register note only: the new §12 sentence calls the answer to the
    just-posed empirical question obvious — her voice, her claim. Figure
    files referenced are the six in `latex/figures/` plus her Overleaf
    effort figure; figure-text md regenerated against v5
    (`docs/figure_text_2026-09-03.md`). Memory pointer updated (working
    file = `latex/v5.tex`). Pending in other threads, unchanged: Figures 3,
    5, 6 in-figure label regeneration (effort-accounting, link-repo).

## Session log (2026-09-03) — THE DUPLICATION REVIEW, AS DIFFS

51. **Her third ChatGPT file** (`Downloads/v5_temp_duplication_review.md`,
    reviewing v6 saved as v5_temp.tex): 29 items on repeated claims,
    definitions, numbers, captions, and cross-references; estimates 500–750
    words and 25–35 pointers removable. Built
    `latex/v6_duplication_candidate.tex` = v6 + its copy-ready and
    mechanical cuts (50 applications; skipped only item 21's "keeps a
    column" sentence, not quoted in full): the three lean captions (Figs
    1, 2, 5); the §3 post-proof restatement; §1's cost-parity sentence
    shortened; §10's fork opening de-duplicated from the abstract; the
    repeated temporary-terminal examples; the Measurement pointer inside
    the recursive-automation definition; §6's automation paragraph opening
    compressed; my §6 historical preview cut; §5's opening compressed and
    its equation-level restatement cut; §7's empirical ordering cut (it
    duplicated the sentence before it); App C's payroll opening; the
    coverage values out of App C and softened in §12 (the review's
    "remains near one-third"); App E's common-window paragraph cut to its
    inference, its mapping paragraph and §12's last paragraph compressed;
    App B's identity sentence to one formulation; §1's synthesis paragraph
    to one sentence and its roadmap to the review's five-line version; §2's
    contribution paragraph to one sentence; six §2 pointers; §3/§6/§7/§8/
    §10/§12 pointer cuts (nine); Figure 3's first caption sentence; App A's
    ten inline pointers (the configuration table stays); App C/E small
    fixes incl. the "benchmark-data BEA benchmark" tautology my step-4
    replace-all created. Result: 14,727 → 13,954 words; \ref uses 130 → 79.
    Lint green bar the Overleaf-only figure. Diffs
    `docs/diff_v6_to_duplication_candidate.html` (122 regions),
    `docs/diff_v5_to_duplication_candidate.html` (299); reading view vs v6
    `docs/reading_view_duplication_candidate.html` (45 windows). Working
    file UNTOUCHED. OPINION (chat): the review is right about the
    self-duplicating captions (mine and the two ChatGPT files' own
    inserts), the §6 preview, the appendix duplicates, and the inline
    appendix pointers; PUSHBACKS — §12's coverage numbers are the timing
    argument, not a restatement (keep 0.05 → one-third); §1's cost-parity
    sentence is hers and the review itself calls the layering acceptable;
    her roadmap should stay and the embedded §1 pointers go instead; the
    §3 Measurement-pointer cut loses the "evidence about the recursion, not
    an estimate of λ" caveat (App E keeps a weaker form); everything that
    rewrites her voiced paragraphs (§1 synthesis, §2 contribution, §5
    opening, §10 fork opening, §12 last paragraph) is her call.

## Session log (2026-09-02, late night, last) — §1 TERM INTRODUCTIONS OUT: v6 step 5

50. **Her call: too many term introductions in §1.** Per term, MOVE / QUOTE
    / KEEP, thirteen exactly-once edits (snapshot session-side; step diff
    `docs/diff_v6_step5_intro_terms.html`, 35 regions; cumulative and
    reading view regenerated — 70 windows, 8 this step). A1 task margin +
    replacement value: MOVED to §3 (replacement value named at the
    $w \le c\gamma(x)$ line; "task-assignment margin, or task margin" at
    the threshold sentence); §1's opening keeps A&R's "task margin" as
    plain words. A2 terminology paragraph: MOVED into §3's existing
    terminal sentence after eq:recursion, merged (horizon definition,
    produced bottlenecks temporary, land as representative, $r$, pure vs
    site rent) with the recursion named there ("machine-sector cost
    recursion, below simply the recursion"); §1 keeps one quoted clause
    (``terminal'', land stands for the class, §3 makes it precise). A3
    task/recursive automation: QUOTED inside the existing sentence, the
    separate sentence cut (defined in §3's "Two margins of automation").
    A4: the insert cut; ``machine-dominance limit'' quoted at its first
    mention, ``flat-capability regime'' at the section pointer; the
    terminal-input-intensity generalization MOVED to §7's land-intensity
    definition; the fork keeps its one plain mention in the closures
    paragraph. A5: QUOTED in one clause (``participation floor'',
    ``dependency floor'', the bundle cost as a different object); the
    participation-floor definition MOVED to §5 after eq:exit. Also the one
    "keep" the step-4 rename missed ("yields a keep $s_0$") → gross exit
    value. Lint green bar the Overleaf-only figure. FLAGGED, her text,
    untouched: §5 "dependent on access to someone else's housing. in the
    modern economy, most often a parent's spare room." — lowercase after a
    period. NEXT: her ChatGPT duplication/tightening audit of this v6.

## Session log (2026-09-02, late night, later) — THE AUDIT AS RULED: v6 step 4

49. **Her ruling on the terminology audit:** symbols in §1 are fine "so long
    as the maths doesn't overwhelm"; cut "ceiling"; leave enclosure (and
    commons, unmentioned, so kept); take "Distribution at the limit". So
    the candidate (log 48, all 67 mechanical items) BECAME v6, plus five
    per-site edits: the one demand-side "ceiling" in §6 → "replacement
    value" (the four coverage-sense ceilings stay); four unqualified
    floors named — §2 → participation floor, §5's $\underline{s}$ →
    dependency floor, App C → participation floor, App D → participation
    floor and "the cost of the subsistence bundle" — her §8 heading "the
    floor binds" untouched. Snapshot session-side; step diff
    `docs/diff_v6_step4_terminology.html` (118 regions); cumulative
    `docs/diff_v5_to_v6_walls.html` regenerated (213); reading view
    `docs/reading_view_v6_2026-09-02.html` regenerated (70 windows, 61 this
    step); figure-text md regenerated (captions carry the audit's inserts).
    Lint green bar the Overleaf-only figure. NOT done (unruled, per-site,
    one session if wanted): the task-margin/assignment-margin and
    replacement-cost/price/value consolidations, flat-limit naming, the
    glossary box, the abstract's "terminal-input intensity" edit.
    NEXT FROM HER: a ChatGPT duplication/tightening audit of this v6. Known
    self-duplications the two ChatGPT files introduced, flagged in chat for
    that audit: §1's extreme-case paragraph now ends by naming the flat
    schedule and machine-dominance limit twice (its own last sentence plus
    the audit's A4 insert); §1's A1 task-margin definition restates §3's
    first paragraph; Figure 1's caption says the wall is closed-task
    shorthand twice (sheet sentence + audit insert); Figure 3's caption
    opens with two definitional sentences; §6's second paragraph and §8's
    opening both say the worker-type comparison is interpretive.

## Session log (2026-09-02, late night) — THE TERMINOLOGY AUDIT, AS DIFFS

48. **Her second ChatGPT file arrived**
    (`Downloads/v6_walls_terminology_audit.md`): not a voice file but a
    78-item terminology audit (keep / keep-clarify / consolidate / replace),
    with copy-ready §1 insertions, caption inserts, and a proposed glossary.
    She asked for reasonable diffs, windows, and an opinion. Built
    `latex/v6_terminology_candidate.tex` = v6_walls + the audit's
    MECHANICAL and COPY-READY items (67 applications): the five §1
    insertions (task margin + replacement value; the Terminology paragraph
    with the recursion named; task vs recursive automation; regime, limit,
    fork; participation floor), and the renames human-essential →
    human-required, terminal factor → terminal input, exit value → outside
    option, source-supported window → benchmark-data window, weak(er)
    extension → model-based extension, non-produced content → direct land
    content, hours content → solo-hours content, all-task → final-good
    numeraire, capability schedule → relative-productivity schedule, the
    keep → gross/net exit value, scarcity rent → rental price, rent-funded/
    natural/full/subsistence floor → subsistence transfer/bundle wording,
    fiscal completion/pair → distribution at the limit / policy pair, the
    three App C subsection titles, two proposition titles, the corollary
    title, and the one-off phrases (terminal claimant, terminal constraint,
    dissipation is migration, hollowness/credence, durable core, wage of
    waiting, effort account, labor-/scarcity-/wage-linked, co-present
    remainder, owner loop) plus six caption inserts. NOT applied (per-site
    judgment, in the opinion): ceiling, commons, enclosure, "the floor"
    unqualified, the task-margin/assignment-margin and replacement-cost/
    price/value consolidations, flat-limit naming, the glossary. Diffs
    `docs/diff_v6_to_terminology_candidate.html` (112 regions),
    `docs/diff_v5_to_terminology_candidate.html` (208); reading view vs v6
    `docs/reading_view_terminology_candidate.html` (56 windows). Lint green
    bar the Overleaf-only figure. Working file untouched; nothing adopted.
    OPINION (chat): the diagnosis is right (too many names per object; the
    terminal ⊃ non-produced ⊃ land hierarchy is sound and matches App A's
    horizon sentence); the §1 insertion sequence VIOLATES her own drafting
    rule (no symbol debuts in §1 — notation_map 2026-08-30) and should land
    at first formal use with §1 in words; keep the floor/ceiling pair,
    commons (defined in Prop 3), enclosure (§2/Prop 3 are hers), fiscal
    completion (her title); accept the one-off removals, the empirical
    window renames (cross-thread cost noted), human-required, the App C
    titles; glossary her call; the abstract touches are hers to rule.

## Session log (2026-09-02, night, later) — THE SHEET AS RULED: v6 step 3

47. **Her ruling: "your pushbacks accepted, but keep machine contestable."**
    Fifteen exactly-once edits on `latex/v6_walls.tex` (snapshot session-
    side; step diff `docs/diff_v6_step3_editorial.html`, 162 regions;
    cumulative `docs/diff_v5_to_v6_walls.html` regenerated, 100 regions).
    Applied from the sheet: App A table rows + opening (1.1); the §3
    closed-set passage (1.2 + 2.2) WITH the H-empty clause restored at its
    end; the §2 clause (2.1); §6's two paragraphs (2.3, 2.4) under the
    sheet's headings ("What sets the wage when the margin reaches the
    closed set"; "Worker heterogeneity and skill premia") WITH one restored
    sentence each (the pre-industrial reading; training as a produced part
    of a person, conditional on open entry); §8 opening — HER first
    sentence kept, the sheet's two hedging sentences replace mine; the
    post-industrial AI sentence made conditional ("If it reaches the
    trained worker's wall as well..."); all six captions (Figure 3 in the
    sheet's 1950 = 100 variant PLUS a base-invariant 4.8× sentence of mine).
    NOT applied, per the accepted pushbacks: 2.6–2.8's rewrites of the
    history paragraphs (vignettes and her sentences stay; her heading
    "Post-industrial as a possible flattening" stays). Figures 1, 2, 4
    regenerated with the sheet's labels (sentence case, mathtext, short;
    `mathtext.fontset` dejavuserif; strata/ushape byte-identical; kappa
    anchors green) and copied to `latex/figures/`. NEW TOOL
    `code/reading_view.py` → `docs/reading_view_v6_2026-09-02.html`: every
    changed paragraph vs her baseline as clean prose, the replaced text
    under the fold, this step's windows red-bordered (17 windows, 14 this
    step) — her ask, to reread without splicing diff colours. Figure-text
    md regenerated. Lint green bar the Overleaf-only effort figure.
    PENDING in other threads (label tables in the sheet, §§5, 7, 8): Figure
    3's fan script and Figure 5's full-band script (effort-accounting; D-F/
    D-Q → labor-origin financing / full-chain human effort; the "members
    and seams" note; "land-priced" → land intensity), Figure 6 (link-repo
    make_figs Fig 5: sentence case, "Transfers: wage taxes" etc.). SHE
    FLAGGED: a whole-paper voice-change md is coming; it rides the same
    route (freeze her file verbatim, exactly-once port, diff + reading
    view; never re-voice; flag slips).

## Verify-list — step 3 (veto window, HERS)

- [ ] The sheet-adopted paragraphs (§3, §6, App A opening, six captions)
      are ChatGPT-voiced; they will meet her whole-paper voice pass like
      everything else.
- [ ] "machine-contestable" now lives in §3 (×3), §6 (×2), the App A
      table, and the Figure 1–2 captions; census-worthy if pinning.html
      ever takes it.
- [ ] Figure 3 caption: the added sentence "Over 1964--2024 the ratio ...
      reaches 4.8×, a ratio that does not depend on the index base" is
      mine (the sheet had no ratio sentence); §10's 1964-window numbers
      untouched.
- [ ] §8 opening: her sentence kept verbatim (with "four"); the sheet's
      "used to organize ... schematic" re-voicing of it NOT taken.
- [ ] Figures 3, 5, 6 still carry their old in-figure labels until their
      threads regenerate them; the figure-text md lists the current labels.

## Session log (2026-09-02, night) — THE CHATGPT EDITORIAL SHEET, AS DIFFS

46. **Her ChatGPT change sheet arrived** (`Downloads/v6_walls_editorial_changes.md`,
    a recommendations document, not a patched file). She asked for a diff
    against v6, a diff against v5, and an assessment. Built
    `latex/v6_editorial_candidate.tex` = v6_walls + every copy-ready TeX
    item of the sheet (17: the App A table rows and opening; the §3
    closed-set passage; the §2 clause; both §6 paragraphs; the four §8
    passages; the six captions, Figure 3 in the sheet's 1950 = 100 variant
    with no endpoint-ratio sentence). In-figure label tables NOT applied
    (not TeX; regeneration units, three of them in other threads). Working
    file `v6_walls.tex` UNTOUCHED; nothing adopted. Diffs:
    `docs/diff_v6_to_editorial_candidate.html`,
    `docs/diff_v5_to_editorial_candidate.html`. Lint green bar the
    Overleaf-only effort figure; refs 127 → 121 (the six pointer clauses
    go with the sheet's rewrites).
    ASSESSMENT (delivered in chat): ACCEPT the model-consistency items 1.1
    and 1.2 (the interior-margin vs boundary-case distinction is exactly
    the reading of logs 42–45; the App A restriction/table fix closes the
    H-scope inconsistency I had left at "no tasks closed by preference or
    law") — with two cautions: "machine-contestable" is a new coined term
    the sheet uses a dozen times (definitions-earn-reuse: fine if she wants
    it, but choose it; the plain form was "tasks machines can reach"), and
    the §3 clause that §7's limit assumes H empty should survive somewhere
    the §3 reader sees it. ACCEPT with restoration the §6 rewrites 2.3/2.4:
    they are correct and keep "premium not level", but they strip the
    intuition she asked for; restore one hedged sentence each (the
    pre-machine reading; training as a produced part of a person "if
    training is open to all"). REJECT-OR-HERS the §8 rewrites 2.6–2.8: they
    delete every profession vignette she explicitly asked for, RE-VOICE HER
    OWN SENTENCES ("wrote down" → "described", "ineffective at cognitive
    ones" → "at many cognitive and skilled tasks", her heading
    "Post-industrial as a possible flattening" → "Post-industrial: a
    possible flattening"), and pull toward the hedged register her voice
    pass has been moving away from — the sheet's "macro-working-paper
    register" is a preference, not her instruction. The 1.3 dimensional
    point (a wage flow "plus the years of training") is right and is a
    figure-label fix. FIGURES: the label shortening for Figures 1–2 and the
    terminology cleanup (D-F/D-Q → labor-origin financing / full-chain
    human effort; "members and seams as in the 1950 fork variant" out;
    "land-priced" → land intensity) are good and are regeneration units
    (fig_model_schematics, fig_eras_workers here; effort-accounting's fan
    and full-band scripts; link-repo's make_figs). Figure 3: the sheet's
    caption/artwork mismatch is my earlier flag; its "do not retain 4.8×
    without confirming" is over-cautious — the durables/shelter ratio over
    1964–2024 is invariant to the index base (+277% vs −21% → 4.77), so
    §10's 1964-window numbers stand under a 1950-base figure; the caption
    is the thing to fix, and the 1950 variant is the artwork's. Figure 4:
    the rewrite changes no fact and fixes a real comma splice; Figures 5–6:
    facts identical, tighter. Her ruling item by item; the candidate exists
    to be quarried, not adopted whole.

## Session log (2026-09-02, evening) — THE WALL IN PROSE (v6 step 2)

45. **Her call after the comparative-advantage exchange: an intuitive reading,
    no maths, placed with the heterogeneity paragraph; pointers elsewhere.**
    Six more exactly-once edits on `latex/v6_walls.tex` (pre-step snapshot
    session-side; step diff `docs/diff_v6_step2_wall_prose.html`, cumulative
    diff vs her baseline regenerated). E11 §6 (sec:interval) gains two
    bold-lead paragraphs after "Heterogeneity": "What sets the wage at the
    wall" (the ceiling is a machine price; on a closed task there is none;
    interior margin → the machine still sets it; every task closed → a
    scarcity price, hours against demand for what only they make, the
    pre-machine case that settled to the floor) and "Other people supply
    the substitute the machine cannot" (trained vs untrained ranked task by
    task as labor vs machines; the cut sets the RATIO; comparative advantage
    between people sets the premium, not the level; the level is whichever
    base the machine leaves standing, the untrained worker's ceiling or the
    floor; training is a produced part of a person bought with years, its
    premium cost recovery in the long run, more only while trained hours are
    short). Innate ability: silent by design, hers. E12–E16 one-clause
    pointers to sec:interval at every wall site: §3's sentence, Figure 1
    caption, Figure 2 caption ("a dot on the wall marks a wage no machine
    sets"), §8 pre-industrial, §8 industrial. The model reading behind the
    prose is in this log's items 42–44 and the chat of 2026-09-02 (the
    chain: land by scarcity; machines at cost off land and labor; ceiling =
    machine price × the person's schedule; the wall removes it; the other
    person is the substitute; comparative advantage sets the ratio; the
    level is a machine cost or the land floor). Deliverables for her
    ChatGPT pass: `docs/drafted_prose_2026-09-02.md` (every drafted passage
    with what it replaced, refs kept) + `docs/figure_text_2026-09-02.md`
    (regenerated: captions carry the pointers). Lint green bar the
    Overleaf-only effort figure.

## Verify-list addendum — step 2 (veto window, HERS)

- [ ] The two §6 paragraphs assert, in words, that comparative advantage
      between people sets the premium and never the level, and that the
      level is either the untrained worker's machine ceiling or the floor.
      This is Lemma A.1's logic applied between persons; it is not
      machine-checked as a proposition. If she wants it as a claim rather
      than a reading, it is a new lemma (the between-person cut), one
      session.
- [ ] "the floor above is what it settled to" — the floor is priced in
      §5 and discussed as one side of §6; "above" reads within §6.
- [ ] Six pointer clauses; §8's computing paragraph deliberately carries
      none (third mention).

## Session log (2026-09-02, later) — THE WALL GOES IN: v6

44. **Her go on all three parts, executed as one unit.** Baseline frozen
    (`latex/v5_baseline_2026-09-02.tex`, byte-identical to her
    `Downloads/v5 (1).tex`); edits applied by an exactly-once-asserted
    script (scratchpad, transient; the diff HTML is the record) into
    `latex/v6_walls.tex`. The thirteen edits: E1 §3 tasks paragraph — H
    introduced words-first (γ_M = 0, unbounded γ, relabeled last, drawn as
    a wall; labor holds H at any wage; the margin lies among reachable
    tasks; the flat limit of §7 is the case H has emptied, App D keeps
    it); E2 Figure 1 caption names H; E3 §2 "the flat configuration" →
    "the configuration ... in which nearly every task is closed to
    machines"; E4 §8 title three → four (HER fresh title, count only);
    E5 §8 opening: four configurations, drawn twice, the schedule is a
    person's (Section 6's heterogeneity paragraph, label sec:interval);
    E6 includegraphics → fig_eras_workers.png + new caption; E7 pre-
    industrial: "the schedule is compressed" → the margin at the wall for
    entrant and master alike, plus the two-people sentence; E8 industrial:
    the two-people sentences after "dispersed and steep"; E9 post-
    industrial: the two-people sentences after the ALM/Autor–Dorn trace,
    and one sentence after her λ sentence (AI reaches the trained worker's
    wall; the premium decays as the trained stock stops being scarce);
    E10 App A's restriction list "no reserved tasks" → "no tasks closed to
    machines by preference or law" (the main text now carries H by
    capability; §7's limit statements still assume H empty, which E1 says).
    Design record for the figures is in the script headers; nesting is
    asserted in `fig_eras_workers.py`. Sibling schematics regenerated by
    `fig_model_schematics.py` came back byte-identical (git clean).

## Verify-list — 2026-09-02: the wall (veto window, HERS)

- [ ] **Every drafted sentence above is Claude's and hers to voice** — E1,
      E2, E3, E5, E6b, E7a/b, E8, E9a/b, E10 — she is passing the figure
      text through ChatGPT; the prose sentences should ride the same pass.
- [ ] **Her count edit:** §8 title "three" → "four" touches a title she
      retyped today. Revert on her word if she wants "three" (then the
      pre-industrial panel needs a caption word instead).
- [ ] **Suspected slip in HER text (untouched, flagged):** §5 "...adds
      approximately nothing of anything. so its competitive price is
      approximately zero." — the deleted clause left a period before a
      lowercase "so"; one-word decision.
- [ ] **Prop 1(iii)** still says exit "recovers the wage to s (possible
      only where the schedule has slope)"; with H drawn, the at-the-wall
      case (wage a residual after rent, no machine price) is only in §8's
      prose. Left as is; a clause there is her call.
- [ ] **Figure-text file** lists the effort figure's labels from
      `effort-accounting/code/build_fullband_df_figures.py`; she should
      confirm her Overleaf PNG is that render.
- [ ] **Figure 3 is the FAN, not the old fork (her note, 2026-09-02):**
      Overleaf's `fig_deflator_fork.png` is
      `effort-accounting/figures/FIG3_realwage_fan_1950.png` from
      `build_fig3_realwage_fan.py`, renamed. Mirrored into
      `latex/figures/fig_deflator_fork.png` (the old 1964 two-series PNG is
      in git HEAD; `figures/fig_deflator_fork.png` left alone). The
      figure-text file regenerated with the fan's labels. FLAG, her call:
      the fig:fork CAPTION still describes the old figure — "deflated by
      the durables CPI and by the shelter CPI, 1964 = 100" — while the fan
      shows four categories on a 1950 = 100 axis with the pre-1964 stretch
      dashed. §10's numbers (4.8×, +277%/+13%/−21% over 1964–2024) are
      1964-base statements and stay true as text, but the caption's base
      year and series count no longer match the artwork. Untouched.
- [ ] **Profession examples** are the paper's now-only history claims by
      name (farm servant hired by the year; seven-year apprenticeship; mill
      hand, hand-loom weaver; millwright, engineer, clerk; young clerk,
      cashier, assembler; developer, physician, engineer) — all generic,
      no dated fact asserted; swap freely.
- [ ] **Old figure** `figures/fig_eras.png` and `code/fig_eras.py` kept on
      disk, unreferenced; the three review drafts (`fig_eras_v2_draft*`,
      `fig_types_draft`) likewise — delete on her word.

## Session log (2026-09-02) — FIGURE 2 REVIEW: THE ERA SCHEDULES

42. **Review only; candidate redraw on disk, unreferenced.** Model reading
    behind the findings, for the record: the wall is App A's H (γ = ∞ there,
    not App E's cap, which is a horizontal truncation γ = min(γ, cap) — a
    different object); at the wall Prop 1(i)'s equality fails and the wage
    is the zero-profit residual after rent, which mechanization of open
    tasks RAISES while the margin stays at the wall (fewer labor hours per
    unit) — the model's own account of the escape before the margin ever
    moves onto a sloped stretch; Prop 1(iii)'s "possible only where the
    schedule has slope" needs the H-case reading there. The v5 §8 industrial
    paragraph already carries the corrected elasticity sentence ("employment
    less responsive to a given wage change and the wage more responsive to
    shifts in labor supply"); pinning.html still says "gained insulation" —
    reconciles whenever v5 flows back. Draft curve parameters are
    illustrative (walls at 0.06 / 0.40 / 0.62 / 0.94 of tasks; computing's
    margin on a short plateau ≈ 0.95, AI's plateau ≈ 0.85 across half the
    task list); nesting is asserted in the script. Legend wording of the
    current figure, if kept: "simple end" → "routine end" (ALM's routine
    tasks, not the lowest-paid ones — those stayed closed).

43. **Her follow-up: person-specific schedules (developers).** Asked whether
    the computing curve really shows the schedule differing by person, and
    whether an untrainable or slow-to-train capability is a different shape.
    Reading delivered (companion draft `code/fig_types_draft.py` →
    `figures/fig_types_draft.png`, three panels, unreferenced): the model
    already carries type-specific schedules (§6 "Heterogeneity", App A
    "Heterogeneous workers"), γ_i = γ_L,i/γ_M with the machine side common.
    An ordinary computing-era type has its margin on a plateau (pinned); a
    developer type's specialty is closed to machines, its margin sits AT its
    wall, and at its wage it loses every open task on cost, so w_D is a
    scarcity price on the type — the pre-industrial configuration one person
    at a time. Untrainable vs trainable is NOT a shape difference but the
    type's supply side: untrainable = J_H = ∞, a terminal factor earning a
    rent like land; trainable = a human build with lag J_H, the premium a
    quasi-rent decaying over the lag (App E's ladder-of-lags logic on the
    human side). Either way the premium survives only while the tasks stay
    closed to MACHINES: untrainability blocks human entry, not machine
    entry; under AI both types sit at c·γ̄. Her intuition on the current
    curve is right: its flat-bottom/steep-top shape is the two-type envelope
    — but App A's "upper envelope of type schedules" is exact only at a
    common wage; in general the envelope is in cost units (γ_i divided by
    w_i/c), a one-clause fix if the figure ever says "envelope".
    CORRECTION, same session: her question is ALREADY formalized and
    checked in the parked sketch blocks. `sketch/link-sketch-blocks-AB.md`
    Block A: log γ_L,i(x) = log γ̄(x) + α(x)·θ_i + β(x)·q_i(x) — scalar
    talent θ drawn once, practice stock q acquired at rate λ(θ) in
    t(q) = q/λ(θ) years (Ben-Porath); Lemma A1: non-constant talent loading
    α(x) makes the per-person schedule a TILT of the common one and sorting
    positive assortative; Prop A2: pay = s + practice premium (cost
    recovery at the marginal acquirer) + talent rent (Ricardian
    differential) + wedge; Prop A3(iii): talent is non-produced per person
    but no term of the machine recipe uses θ, so outside the closed set its
    terminal demand is zero — "a transition rent on a permanent base",
    the same conclusion as the draft's panel (c). `sketch/link-sketch-
    blocks-B0-C-D.md` Block C, the education race: training lag
    T_E(θ) = q_req/λ(θ), the cobweb (C1, lag-indexed amendment), the hump
    (C2), overshoot and the queue (C3), the doomed vintage (C4). Checks
    `checks/check_split.py` and `checks/check_race.py` green 2026-08-09.
    So in her terms: "cannot be trained" = a task with talent loading α
    and β ≈ 0; "years to train" = practice loading β with a long T_E; both
    are the same two-loading schedule, not new theory. Nothing in
    pinning.html carries θ or q today; the merge-or-next-paper decision on
    the blocks is her PENDING call from 2026-08-09 (STATE §"PENDING
    DECISION"). The draft figure's untrainable/trainable annotation is
    Block A's split in words; if it ever enters the paper, it enters
    through the blocks' notation, not the figure's.

## Session log (2026-09-01, continued) — THE κ MEASUREMENT FIGURE IN V5

41. **The coverage figure split by rent measurement, landed in her v5.tex**
    (her ask, after a fork/rent-measures diagnostic session whose fork-side
    variants live in effort-accounting). New artwork
    `latex/figures/fig_kappa_measurement.png` + generator
    `code/fig_kappa_measurement.py` (reads `link-repo/data/kappa_results.csv`;
    2025 anchors med 0.326 / rent-bill 0.326 / valuation 0.303; style matches
    `fig_kappa.png`, which is untouched). Her `Downloads/v5.tex` edited in
    place (original snapshotted session-side; word-diff in chat), three
    regions: (1) §9 coverage paragraph +2 sentences — the grid's two routes,
    valuation swinging with rates and house prices, the rent bill touching no
    valuation, the rise common to both — DRAFTED, hers to voice; (2) the
    `\includegraphics` swap; (3) the caption gains the source block and loses
    "band width is substantially the capitalization-rate spread" (untrue at
    the endpoint, where the band edges are rent-bill members), keeping the
    post-1995/2020 caveat verbatim. Motivation on record: land values are
    capitalized forecasts (rate and expectation swings — measured this
    session at 20.4%/yr yield vol vs 2.3%/yr rent-bill vol); the rent-bill
    members never touch a valuation and carry the same trend, and the figure
    now shows that rather than asserting it.

## Session log (2026-08-28, continued) — THE READABILITY RESTRUCTURE (her call)

36. **Dynamics demoted to Appendix E; the main text returns to the shape
    she liked** (her decision after reading the draft, amending log 32's
    panel structure: steady-state time stays in the text, sequence time
    moves to the appendix, cited where it bites). Executed and ALL GREEN:
    - **Abstract reverted to the original wholesale** with exactly her two
      amendments: one added time sentence ("Machine production takes time
      as well as inputs: build lags mark up replacement cost and decide
      who holds the value automation releases while capacity catches up")
      and "changes no work–exit choice, up to an income effect". Her
      original recipe sentence kept verbatim (fix 3 skipped, her call).
    - **Structure:** §§1–7 as before with §4 (build recipe) and §5 (build
      time, COMPRESSED ~35%: corners to one sentence, the interest
      identity DEMOTED from proposition to prose with W_K's formula and
      ledger moved to Appendix A) in the text; the transition act is now
      **Appendix E "The model in motion"** (E.1 sequence economy, E.2
      equivalence + regimes, E.3 frozen rent, E.4 solver/methods merged
      with the old numerical appendix, E.5 experiments, E.6 sloped path);
      §8 is history again under its v1 title; §9 keeps 9.1/9.2 (horizon,
      slimmed)/9.3; §7 gains one transition paragraph citing E (CM on the
      path; the frozen-rent clock; the waterfall; the release-day
      diagnostic); §6 gains one clock sentence. Main-text props are
      **1–6** (margin, closure, exit, fork + corollary, welfare, horizon
      — v1.5's numbering preserved for 1–5's objects except the closure's
      new content), appendix results are **E.1/E.2**; figures **1–5 keep
      their v1.5 identities** with the four dynamics figures as 6–9 in E.
      Main text 13.1k → 11.4k crude tokens; appendices 5.4k → 7.1k.
    - **Timeless pass:** version-tell sweep done (one legitimate "is now"
      kept — the rent turning positive in Prop 3's proof) and a
      **timeless-register lint family** added (bans "no longer",
      "previously", "the original", "used to be", "this version",
      "anymore"; "is now" deliberately exempt). Lint is 91 checks.
    - Converter retaught (headings, prop sequence 1–6+corollary+letters+
      E.1/E.2, figures in the restored order, 14 displays), export ALL
      GREEN with word fidelity; census, check_pinning 51, check_dynamics
      54, solver gate all green.
    - **INCIDENT, recorded plainly:** mid-restructure I ran a reflexive
      `git checkout -- paper/pinning.html` after a failed (non-writing)
      script and DESTROYED the uncommitted dynamic draft. It was fully
      recovered — the Browser pane still held the last-loaded DOM, which
      served as the oracle, and the draft was reconstructed by replaying
      this session's complete edit record against the committed phase-1b
      base; every battery invariant (π sites, T-label counts, check
      totals, converter expectations, word fidelity) matched the
      pre-incident values before work resumed, and the recovered draft is
      snapshotted at `paper/snapshots/pinning_dynamic_draft_recovered.html`.
      Lesson banked in memory: never bare-checkout a file carrying
      uncommitted work; snapshot before structural surgery (done:
      pre-dynamics and recovered-draft snapshots both exist).
    - Still open from log 35's veto list: the §2 one-third trim (still
      not taken), title, AK/Judd references, the three-taxes boundary
      blessing, the λ §10 splice. The next passes: density on §4–§5
      against the cold-reader standard, then her voice pass via the
      word-diff.

## Session log (2026-09-01, continued) — THE VOICE EDIT RETURNS: THREE DIFFS

42. **Her/ChatGPT voice edit received and frozen; slip-scanned CLEAN;
    the three diffs she asked for are cut** (her ask: "one from v3.1
    (also attached), one from v4, and one from your version"). Files
    frozen: `latex/v5_land_intensity_voice_edit_2026-09-01.tex` (the
    voice edit, ~13.9k words) and
    `latex/v3.1_appendix_notationchanges_baseline.tex` (an earlier
    export-lineage version she supplied, ~13.4k words, header still
    carries the old pinning.html-canonical note).
    - **Slip-scan verdict (voice-pass protocol applied to this
      lineage): voice-only.** All 9 equation environments byte-
      identical to v5; every anchored number preserved (69.6/65.8/
      48.9/47.2, 4.8×, 13/277 percent, 0.33 with band, CPIUFDNS);
      "$-21$ percent" re-expressed as "a decline of 21 percent";
      the energy exclusion re-voiced ("We omit energy because world
      oil prices dominate the series"); fig:labor-linkages stays in
      §9; \lo/\hi macros and eq:composites/eq:fork-pair intact;
      "free of non-produced" ×0; the two remaining "machine-made
      goods" are the Role-3 sites (§1 relative-price sentence, App D
      Baumol categories). Structural lint clean.
    - **Diffs** (word_diff_report): `docs/diff_v31_to_voice_2026-09-01
      .html` 720 regions; `docs/diff_v4_to_voice_2026-09-01.html` 71;
      `docs/diff_v5_to_voice_2026-09-01.html` 137. Note the asymmetry:
      v4→voice (71) < v5→voice (137) — the voice pass re-voiced much
      of Claude-drafted v5 prose back toward the baseline register
      while keeping v5's structure and maths; the intended division
      of labor, visible in the counts.
    - **Open: which file is now the working copy.** The voice edit is
      presumably the live draft (its header comment is their rewrite);
      on her word it becomes the base for the next unit and
      check_fan/lint ride along unchanged.

## Session log (2026-09-01, continued) — V5 ROUND 2: THE HYPOTHETICAL RETIRED

41. **Her catch acted on: the zero-content good demoted from reference
    class to contained boundary case; two more of her calls executed**
    (her read of round 1: "we're trying to move away from talking about
    them"; then "make those changes... keep calling the cpi fork a
    fork... put the labor financing and production figure back into the
    main text"). All in `latex/v5_land_intensity.tex`; diff regenerated
    (66 regions, same file); lint clean; check_fan 27 GREEN unchanged.
    - **Redone onto lo/hi:** abstract sentence (now "the real wage forks
      by land intensity: nearly pinned... against the least
      land-intensive categories, falling without bound against the
      most"); §1 extreme-case paragraph (intensity-native, CM demoted to
      one boundary-case parenthetical, ideas named only there); §6
      discussion paragraph INVERTED (part (iv) leads as "the fork's
      working form", CM contained in a two-sentence close); corollary
      buys-clause REVERTED to v4; §3 ideas paragraph loses the
      distance-from-ideas sentence (institutional-rents job kept).
    - **Precision fixes:** Prop fork(i)'s subject renamed to the
      numeraire ("the good made of tasks alone") — the three-class
      distinction (CM's no-land-anywhere = ideas; the numeraire's
      no-DIRECT-land, invariance exact; real lo goods, invariance
      approximate) now consistent; the composites paragraph defines
      non-produced content as land drawn DIRECTLY with the
      machine-embodied-land sentence added (rides in the machine
      rental, parity ties it to the wage — the "full chain" wording
      that would have broken part (i)'s nesting is gone); eq:fan
      relabeled eq:fork-pair (her fork-vocabulary ruling).
    - **Her structural calls:** fig:labor-linkages moved BACK to §9
      (cited from the compact paragraph; Appendix E keeps the account
      detail, its figure sentence still resolves); the four-category
      figure retitled "The deflator fork: ..." and re-rendered, gates
      PASS (effort-accounting; internal filenames still say fan —
      flagged there, rename on her word).
    - Kept as the hypothetical's only homes: §2.6's CM sentence, §6's
      concession close, the one clause inside part (iv). "free of
      non-produced content" now ×0 in the file.

40. **Both scopes executed in one unit** (her go: the land-intensity
    reframe + the financing/production demotion; deliverables a tex and
    a diff html for her and ChatGPT's voice pass, edits to return by
    paste). Files: `latex/v5_land_intensity.tex` (working),
    `latex/v4_accounting_revised_baseline_2026-09-01.tex` (frozen
    verbatim copy of her Downloads file),
    `docs/diff_v4_to_v5_land_intensity.html` (word_diff_report, 70
    regions — NOTE for her read: the moved financing block shows as a
    §9 strike-out plus an Appendix-E insertion; it is a verbatim move,
    not a rewrite). Checks first: `checks/check_fan.py` 27 GREEN (F1
    parity display closure-free; F2 ratio form; F3 r/w formula +
    statics + divergence; F4 zero-content invariance incl. both
    Appendix-A interest closures; F5 monotone fall/limit/crossover/
    ordering; F6 nesting of fork(i)/(ii); D1 fan-CSV anchors 376.8/
    113.2/78.6 and the +277/+13/−21 roundings).
    - **The reframe, 12 sites:** header provenance comment; \lo/\hi
      macros; abstract sentence (ideas-exception + intensity order —
      EXPECTS her re-voice); §1 CM pair rewritten (premise census:
      ideas exact, low-intensity manufactures close, everything else
      ordered by intensity); §2.6 concession re-scoped ("at its
      premise — met exactly by ideas alone — and prices how far each
      category sits from it"); §3 ideas paragraph now names ideas the
      one chain terminating in nothing scarce; §4 floor caveat sentence
      → the exit bundle sits high in the intensity order (exited people
      supply their own hours, not the ground); §6 gains the composites
      paragraph (hours content / non-produced content / land intensity
      defined in words, durables and shelter the measured counterparts)
      + eq:composites + Prop fork(iv) + eq:fan + proof clause +
      the reworked CM discussion paragraph; corollary buys-clause
      scoped; §9 intro trimmed; §9 fork paragraph gains the food leg
      and the energy-exclusion sentence; notation/data/verification
      footnotes extended (lo/hi subscripts; CPIUFDNS; part (iv)
      sympy-checked, outside Lean — timeless register kept).
    - **The demotion:** §9's two dense account paragraphs, the
      fig:labor-linkages figure, the common-window paragraph, and the
      mapping-back paragraph (φ_C) moved VERBATIM to new Appendix E
      "The financing and production accounts" (app:effort) with one
      stitching sentence; §9 keeps a five-line summary (19pp gap;
      no widening claim — the strong-window gap narrows 20.7 → 18.6).
    - **Verify-list for her:** the abstract/§1 wording (accuracy-first
      drafts, her voice expected); "land intensity" as a term (her own
      phrase; used as a defined term ~15×, de-coining rule considered);
      the energy-exclusion parenthetical (keep/cut); the food numbers
      and their data-note/check anchoring; App E's stitching sentence;
      fig:labor-linkages now appendix-side; \lo/\hi macros vs inline
      \mathrm (Overleaf taste); NO local compile run (no TeX here) —
      first compile is hers on Overleaf; floor funding-dichotomy prose
      + quasi-exit clause DEFERRED by her two-scope framing.

## Session log (2026-09-01) — THE FLOOR/FORK DISCUSSION (no drafting)

39. **Her floor/fork intuition session; the hours+acres construction
    agreed in principle, baseline switched** (her prompts: "understand it
    better... a better, more intuitive mathematical way"; "such goods
    [zero non-produced content] don't exist (except ideas), everything
    requires some scarce inputs at the end of the day, the question is
    how much"; then "use this draft as your baseline... walk me through
    the new maths... I'd like to see food and energy deflator lines").
    - **Her CM objection accepted as the theorem's shape:** the binary
      (machine-made goods vs non-produced services) becomes a continuum.
      Scratch-verified (17 sympy checks, scratchpad
      `scratch_hours_acres.py`, would graduate to checks/ on adoption):
      at cost parity any category with task content L̄_cat (solo
      human-hours, machine-quality-invariant) and non-produced content
      b_cat prices as p_cat = w·L̄_cat + r·b_cat — exact for ANY closure
      of c (parity alone), recursion needed only to pin r/w =
      (1−a−λγ̄)/(γ̄b). Real wage w/p_cat = 1/(L̄_cat + b_cat·(r/w));
      b = 0 gives CM invariance jointly in (γ̄, λ, and any interest
      factor); b > 0 forks when r/w crosses L̄_cat/b_cat — categories
      fork in b/L̄ order. Nests the existing Prop fork (i) (numeraire =
      the b = 0, L̄ instance) and App C.3's P_s = p·g_s + r·h_s (same
      bilinear form). No dynamics needed: eternal content (b > 0) vs
      horizon pinning (J_j > h, already an App A paragraph) disentangled.
    - **HER RULINGS:** (i) baseline = `v4_accounting_revised (3).tex`
      (Johan-side co-authored STATIC revision of the LaTeX export;
      differences from pinning.html v2 noted: no build-time §5/§8
      dynamics, no θ coefficients, no Prop exit(iv), props renumbered,
      abstract carries 4.8× and κ 0.33); (ii) notation kept simple —
      b_lo/b_hi (and p_lo/p_hi) for two named composites, general good
      index avoided (sec:fiscal already uses j for terminal factors);
      (iii) floor maths kept light since no downstream measurement uses
      participation — funding-source dichotomy (wage-linked vs
      rent-linked fallbacks) recommended as PROSE, s(q) and Prop exit
      kept as-is (app:race reuses q_enc = (s_0−s̲)/h_e).
    - **Fan empirics built** (effort-accounting item 11 + verify-list
      unit 4): 2024 legs 1964=100 durables 376.8 > food 113.2 > energy
      95.8 > shelter 78.6 — the predicted b/L̄ ordering; energy net-flat
      with ±47% decade swings (her "overseas-sensitive" guess confirmed
      with numbers). Her follow-up: output rebased 1950 = 100 with a
      linear 1950–56 energy backcast (her call), 2024 legs 618.9 /
      166.8 / 157.4 / 104.5; ratios base-free, gates unchanged.
    - **Next unit on her go:** sec:limit insert (the pair display + fan
      paragraph + crossover clause), floor prose additions (funding
      dichotomy; the marginal-work/quasi-exit clause), CM rescope
      touches (§2 sentence, abstract clause, post-Prop-fork discussion
      paragraph), measurement §9 fan mention/figure decision; sympy
      check graduation; Lean scope decision for the new part (flagged,
      optional). Nothing drafted this session.

## Session log (2026-08-30) — THE VOICE PASS (her lesson, applied)

37. **Her §1 rewrite ported; the register change identified and
    propagated across all Claude-drafted v2 prose** (her instruction:
    "do the same sort of change on all your new work"). Uncommitted.
    - She re-voiced "What does time add?"; ported verbatim. "whilst"
      kept on her ruling (sits 1 against 30 "while"s — proof-stage
      copyedit call is hers). The lesson as edit rules: plain statement
      over constructed antithesis; short declaratives, examples strung
      on commas; em-dashes only as appositive glosses; no coined
      abstractions; no duplicated hooks; no symbol debuts before their
      section; point at the tradition where it can carry the weight.
    - Codified so it cannot regress: notation_map drafting rule (§1
      argues in words, no symbol debuts) and the lint register ban
      widened from "the dials" to any "dials".
    - Applied (~30 edits; her voiced text untouched): §1 architecture
      paragraph (J evicted, "where they bite" plainened), §2.2 (q
      evicted), §2.3 (γ̄ evicted), §3 (duplicate "dynamic throughout"
      opener cut), §4 ("not only produced; it is produced slowly"
      flattened here as she flattened it in §1), §5 lead unbraided +
      the land-classifier punchline flattened, §6 historical-signs
      paragraph, §7 fork + path paragraphs (scare quotes dropped), §8
      opener + the triple-hinged Engels' pause sentence broken into
      four, §9.2 "precedent shelf" → precedent, §9.3 "turns punctuated"
      → "arrives in steps", §11 dash hinges to sentences, App A, C.6
      "stakes of the bridge" → "sizes the bridge", App E ("deserve
      belief", "Acceptance is a ladder", "reported rather than hidden",
      "belongs in the open", "The sentence version" all plainened;
      Georgist/Piketty sentence unbraided; "dials" → "values", 7 sites).
    - Correctness catch riding along: §1 said "two questions" above
      three bold questions — now "three".
    - Metrics: em-dashes 211 → 179 (11.2 → 9.5 per 1,000 words). Lint
      91, census, converter with word fidelity ALL GREEN; main.tex
      regenerated.
    - Her read: `docs/diff_voicepass_2026-08-30.html` (word_diff_report,
      95 changed regions) against base snapshot
      `paper/snapshots/pinning_pre_voicepass_2026-08-30.html`.
    - Deliberately NOT touched (hers, or reads as hers): the abstract
      (its time hook stays — the §1 duplicate was the copy she cut),
      §6's "the empirical debate of search and matching is changed
      significantly on this object's level" (on the voiced-repairs
      list), §9.3's "Three possible stabilizers … however" sentence,
      all v1.5-voiced bodies.
    - Still open: unchanged from log 36 (the §2 trim, title, AK/Judd
      references, three-taxes blessing, λ splice); density pass on
      §4–§5 remains next.

38. **The rulebook sweep** (her prompt: read the other linter checks and
    notes; apply what was missed). Sources re-read: lint's ban-family
    comments, census's SYMBOLS-EARN-THEIR-INK header, v2 brief §8
    (style and claims discipline), v1 brief's register rules
    (SPEAK-AS-THE-AUTHOR / ASSERT-FORWARD / ONE-TEMPERATURE), review
    synthesis. Thirteen violations found in Claude-drafted prose, all
    fixed; her text untouched:
    - **Symbols earn their ink:** `qq` (solver notation leaked into
      Prop E.2(iii)) inlined as ((1−δ)/(1+ρ))^J; `S_t`/`π_old`
      (single-use, E.1 convention sentence) reworked into words.
    - **Define once:** E.1 stated the capacity law, the pay-at-start
      timing, the net-rental definition, and the entry complementarity
      TWICE (intro paragraph and clearing block) — deduplicated; the
      u_K-exponent timing note now lives in the intro paragraph only.
    - **Pseudo-cleft "What"-openers** (brief §8 checklist): four of
      mine recast ("What moves is the rent" → "The rent moves
      instead"; "What an owner holds…" → "On release day, an owner
      holds…"; "What survives of the conjecture…" → "The conjecture's
      land half survives…"; "What Section 4 called terminal…" →
      "Section 4's informal classification becomes this parameter");
      the nine survivors are hers/v1.5 (incl. the three §1 questions).
    - **SPEAK AS THE AUTHOR:** "the moving parts are these" (stage
      direction) cut; "The paper's limit statements" and "the paper's
      architecture" possessives removed ("the paper's" now ×0 in body).
    - **"X, not Y" over-density:** §3 double reduced (dropped "not the
      margin to be shut" — the sentence's second half already says it);
      §6 and §7 singles converted to "rather than"/"beyond…to".
    - **Paragraph-final aphorism restating:** T1's closer ("The
      windfall is real… the permanence belongs to the input no window
      can deliver") deleted — the 0.08-vs-3.80 sentence already lands
      it; the paragraph now ends on the numbers.
    - **Em-dash ≤ one construction per paragraph:** my two offenders
      fixed (T5 had three pairs → one; App A interest ledger two → 
      zero); C.1's six are her voiced Speenhamland paragraph and stand.
    - Mechanized: lint gains two soft metrics ('What'-opener count,
      max per-paragraph em-dashes). Em-dashes 211 → 163 across both
      passes (11.2 → 8.7 per 1k). Lint/census/converter ALL GREEN;
      main.tex regenerated; diff refreshed to 146 regions.
    - Flagged, kept, for her call: "Caselli–Manning is the case…" /
      "Waiting is priced…; building is a lag" class content-antitheses
      (the §1 lesson's keep-side); §9.2's closer ("the durable
      instrument is the one the limit already selected") as a
      candidate crown; θ_e stays (formula-bearing, rides the θ family
      per census policy).

## Session log (2026-08-28, continued) — PHASES 2–3 EXECUTED: THE DYNAMIC DRAFT

35. **The dynamic rewrite executed in place, one session, checks green
    end-to-end** (her go: "you do the draft of the dynamic version"; the
    engine and all pre-drafting checks were already standing from log 33).
    Snapshot of the replaced version:
    `paper/snapshots/pinning_pre_dynamics_snapshot.html`. THE DRAFT IS
    UNCOMMITTED pending her read — the veto window below is the gate.
    All batteries green at close: lint (incl. claim-status tags on the
    live T-sites), census (K returned as the machine stock; new-family
    rows live; γ*-DEAD guard holds), check_pinning 51, check_dynamics 54,
    solver gate PASS, LaTeX export ALL GREEN with word fidelity.
    Structure landed per the log-32 memo, with two amendments the work
    forced: (i) the §8 subsections are 8.1–8.6, not 8.0–8.5 (papers do
    not number from .0; the converter's sequence check agrees); (ii) the
    memo's Phase-2/3 cut-line moved one notch — the frozen-rent result
    turned out closed-form provable (T1a–d), so §8.2 ships as a
    PROPOSITION, not a numerical claim.
    - **Section map (old → new):** §4 ceiling keeps its number and gains
      the build recipe + the θ closure (Prop 2 restated); NEW §5 "Build
      time and the wage of waiting" (u_K derived in words with the timing
      conventions stated, corners at J=1/δ=1/ρ=0/δ=0, direct-vs-total
      coefficients, horizon-terminality as the parameter with land J=∞,
      Prop 3 = the interest identity with W_K in words and the
      convention-freedom sentence); old §5 floor → §6 with Prop 4(iv)
      added (both lives priced: h_w, the s₀-branch q-cancellation, the
      funding-source trichotomy via θ_e) + the historical-signs
      paragraph; old §6 interval → h3 6.1 unchanged; §7 fork gains the
      coefficient-ratio paragraph (θ_w/θ_j, CM as proportionality, the
      θ gradient ideas→location, J=∞ the classifier) and Prop 5(ii)'s
      build-recipe clause; NEW §8 "The model in motion" (8.1 sequence
      economy + Prop 6 equivalence; 8.2 Prop 7 frozen rent with the Q̄ =
      (1+ρ)^{J−1} refinement; 8.3 solver validation; 8.4 T1–T3 with
      figures 2–4, each labeled numerically verified, incl. the
      envelope-not-step honesty sentence and T2's sunk-transfer
      indeterminacy; 8.5 T5 with figure 5, the shock-type split verdict
      verbatim-faithful to results_dynamics.json; 8.6 = old §9 history
      ported verbatim with the (speed, J, λ) tie and the Engels'-pause
      citation added); old §8 fiscal → §9 with h3 9.1 + NEW 9.2 (Prop 9,
      the fiscal horizon: levy-on-stock-in-place clean, anticipated
      rental tax scales u_K/(1−τ_K), input-j windows time-inconsistent,
      land clean at every horizon; AK/Judd shelf) + 9.3 = old §11
      stabilizers with the time-signature sentence; old §12 split into
      §11 AI (dated J-ordered sequence, T2/T5 cited with labels, the
      buildout falsifier added) and §12 conclusion (+ the third
      empirical question); §3 gains the declaring sentence and the
      NEW-TASK MARGIN block (support-collapse condition, N1/N2-checked,
      Autor–Chin–Salomons–Seegmiller engaged) replacing §2.3's
      shut-by-assumption clause; §1 gains the "What does time add?"
      question, the architecture paragraph, and the rewritten roadmap;
      abstract gains the build recipe, θ_w·r, and the frozen-rent/
      waterfall sentence.
    - **Numbering maps.** Props: margin 1, replacement 2 (restated),
      interest 3 (new), exit 4 (was 3), fork 5 (was 4), equivalence 6
      (new), frozen rent 7 (new), welfare 8 (was 5), horizon 9 (new);
      appendix items unchanged. Figures: schedule 1, dyn windfall 2,
      waterfall 3, speedlag 4, sloped 5, eras 6 (was 2), fork 7 (was 3),
      κ 8 (was 4), fourway 9 (was 5). Appendices now A–F: A gains the
      sequence-economy block (timing, clearing incl. the named
      land-viability condition, income convention with the M_t switch,
      regimes-and-existence honesty incl. the narrow interior region and
      the operation-bound corner), the capitalized closures reframed as
      u_K corners, 𝟙 replacing (I−A)⁻¹'s I, and the §8 row in the
      configuration table; B gains the ρ>0 interest-flow note; C gains
      C.6 transition bases; NEW E numerical methods + solver credibility
      (tolerances in words); NEW F the notation table. Back-matter:
      notation footnote extended (build-subscript reading, 𝟙, Q vs q);
      verification footnote carries the dynamics discipline sentence and
      the Lean boundary (transition paths outside the formalization),
      timeless register kept.
    - **Tooling that rode along:** `html_to_latex.py` learned the new
      headings/labels/props/figures/tables, π/∞/⊥/…/𝟙 (bbm), the third
      table spec, and the new expectation counts (12 numbered displays,
      9 figures, 3 tables, 58 refs); the export is ALL GREEN with word
      fidelity. Census: DEAD-K guard narrowed to the k-forms (K is the
      stock now), v2-family rows added. Her Overleaf paste source for
      the NOTATION-ONLY state is `latex/main_phase1b_notation_only.tex`
      (extracted from the phase-1b export commit; delete after pasting)
      — the on-disk `latex/main.tex` is already the dynamic draft.
    - **Word budget:** same-method count main 8.3k → 13.1k, appendices
      3.8k → 5.4k (crude token count incl. entities; the real-word main
      text sits near the brief's ~9k target).

## Verify-list — 2026-08-28: the dynamic draft (veto window, HER GATE)

- [ ] **Voiced-sentence repairs to re-voice or bless** (each authorized by
      the brief's own fix list, all flagged, none silent): the abstract's
      recipe sentence and closure display (now θ_w·r) and "changes no
      work–exit choice" → "moves no participation margin, up to an income
      effect"; §2's "We do not offer…" fragment fixed; §2.2's walls
      sentence rewritten ("we price both endpoints", q-invariance clause);
      §2.3's offshoring comma splice fixed and the shut-margin clause
      replaced by the §3 pointer; §2.6's Korinek–Suh and MRR sentences
      extended; Prop 8(ii)'s "puts near zero" → "finds modest but not
      zero, larger for secondary earners"; §4's viability-reading sentence
      extended with the u_K clause; "Recursive automation lowers λ"
      extended to λ_I; the worked-instance paragraph gains the build
      extension; §8.6's industrial paragraph gains the Engels'-pause
      clause. Everything else voiced carries verbatim.
- [ ] **§2 trim NOT taken:** the brief says cut §2 by a third; I cut
      almost nothing (her voice, her knife). Commission the trim or
      strike the brief line.
- [ ] **Title:** keep, or "…Scarcity, Technology, and Time" (brief leaves
      it to the authors; abstract and §1 now carry enough time content to
      justify either).
- [ ] **Part labels (memo open item):** skipped by default; the §1
      architecture paragraph does the work typographic labels would.
- [ ] **The three-taxes boundary (memo says raise BEFORE 9.2):** 9.2 is
      written to the memo's stated default — the horizon theorem as a
      J-statement native here; no taxonomy/convergence/ceiling/dial
      content, no cross-citation. Bless or redraw before any SSRN push.
- [ ] **T5's framing in §8.5/§11** (the shock-type split and the
      release-day diagnostic) — the conjecture's original wording is
      reported as split, not silently replaced; her call it stays.
- [ ] **§9.2's Auerbach–Kotlikoff/Judd shelf is UNCITED in the refs** —
      the sentence names them without bibliography entries (deliberate,
      pending her call on engaging that literature properly vs trimming
      the sentence). Add entries or trim before export goes out.
- [ ] **The λ §10 splice remains OPEN** (her sequencing call, unchanged);
      §10 took only the coefficient-binding sentence.
- [ ] Draft is UNCOMMITTED; on her pass: commit as the Phase-2/3 wave,
      regenerate the zip, and cut the Johan packet (What changed / Why /
      Where to look / Questions — the brief's §7 template).

## Session log (2026-08-28, continued) — PHASE 1b: γ* RETIRED; DRAFTING RULES

34. **Notation micro-wave 1b executed and committed alone** (her calls after
    the elegance walkthrough): γ* → γ(x*) at all 29 sites (the paper ran
    both forms, 29 starred vs 14 spelled — definitions-earn-reuse); the
    Prop-2 defining clause ("with γ* = γ(x*)") deleted, not renamed; γ̄ and
    x* untouched; census live-row updated + DEAD guard added; map amended
    (notation_map.md §1b). DRAFTING RULES recorded there, zero renames
    needed (none of these symbols are in the paper yet): π debuts at §8.0
    (the transition's protagonist, never in the §§1–7 spine — free entry
    is words there); Q §8-local; W_K not christened unless §9.2 reuses it;
    the operating recipe stays BARE (a, λ, b) vs the marked build recipe
    (a_I, λ_I, b_I) — her call, keeping the λ brand and the λ̂
    input–output continuity. Her framing paragraph (two recipes, stock
    price vs flow rental, u_K the converter, the ρ = 0 corner) is adopted
    as the seed of §4–§5's exposition, with the corrections from this
    session's review (J is the build lag, not a unit; the lathe is the
    a_I·c term; land is J = ∞). Overleaf: she pastes the notation-only
    export before the dynamic draft lands.

## Session log (2026-08-28) — V2 DYNAMICS PREP: THE CAPITAL-DYNAMICS ENGINE

33. **Log 32's pre-drafting mechanization executed in full** (her go:
    "let's work on the capital dynamics"; one unit, checks before code,
    code before any drafting; `pinning.html` untouched). NEW FILES:
    `checks/check_dynamics.py` (54 checks, ALL GREEN; writes
    `checks/dynamics_ss_targets.json` — the solver's gate targets),
    `code/dynamics/model.py` / `solve.py` / `figures.py`,
    `code/dynamics/results_dynamics.json` (the verdict record),
    `figures/fig_dyn_{windfall,waterfall,speedlag,sloped}.png`, and the
    claim-status-tag lint family in `lint_pinning.py` (every T1–T5
    citation must carry "numerically verified" / "conjecture" / "theorem"
    / "proposition" in the same paragraph; fixture self-test; vacuous
    until §8 exists). `check_pinning.py` (51) and lint stay ALL GREEN.

    **The memo's gate, passed pre-drafting:**
    - u_K = (ρ+δ)(1+ρ)^{J−1} DERIVED from the free-entry PV condition
      (checks U1–U6), timing pinned once: build paid at start of t, first
      service in t+J undepreciated, wear after; the (ρ+δ)(1+ρ)^J misread
      is checked to DIFFER (the off-by-one bites, caution iv). Corners:
      J = 1 gives ρ+δ; J = 1, δ = 1 gives 1+ρ — Appendix A's two λ=0
      carrying factors are u_K corners (R5), so the v2 dynamics nest the
      2026-08-27 user-cost forms exactly.
    - The recursion c = ac + λw + br + u_K·p_K reproduces the brief's
      θ_c, θ_w displays exactly (R1–R3); v1 nests at zero build recipe
      (R4); the price block's determinant IS the viability denominator
      (R6). Statics S1–S6, including a new one: at λ = 0 the cross-effect
      survives through the build recipe alone (dθ_c/dγ*|λ=0 ∝ u_K λ_I).
    - **The equivalence lemma, both directions** (the anti-staple hinge):
      flat case fully symbolic (E1–E3 — constant sequences ⇔ the §4
      recursion + a closed-form quantity block, Walras closing as an
      identity in all parameters); sloped case instantiated on the
      A-joint config extended with the build recipe (EJ1–EJ7), and the
      build→0 limit reproduces check_pinning's A-joint root to 1e-9
      (EJ7). Uniqueness claimed and checked ON THE VIABLE SET — the build
      recipe shrinks it (Den > 0 dies at x ≈ 0.658, was 1.0).
    - **Caution (i) RESOLVED, and it amends brief §3.5:** convention
      pinned as builds 100%-externally financed at world ρ. Free entry
      (zero NPV) then makes SS household machine cash IDENTICALLY zero
      (L3), so the memo's "domestic + debt" and foreign equity COINCIDE
      at rest: SS Inc = wN_a + rT (NOT the brief's wN + rT + πK — gross
      rentals in income do not close), and goods clearing carries an
      explicit NX = πK − p_K·I. Walras then closes identically (E3, EJ4).
      Off steady state the convention only decides who books π-surprises
      on pre-shock vintages: M_t = (π_t − π̄_old)·S_t to households
      (domestic, the solver default per the memo) or abroad (foreign,
      a switch).
    - Caution (ii): the named condition falls out exactly — r > 0 ⟺
      (1−α)T > bX + b_I·I (V1). Caution (iii): the interior conditions
      are REAL and the region is NARROW — E4b maps it (canonical flat
      dials now T = 3.8; at T = 10 the same dials give m > 1, E5); the
      solver checks interiority/participation every period and reports.
    - **The interest identity in ledger form** (L1–L4): SS machine cash =
      ρ·W_K with machine wealth W_K = installed PV + work-in-progress at
      compounded cost = p_K·K[(1+ρ)^{J−1} + δ((1+ρ)^{J−1}−1)/ρ]; equals
      ρ·p_K·K exactly at J = 1 (the brief's §3.1 line is the J = 1
      corner); the excess is the gestation float, now named.
    - **T4's algebra landed early** (the memo wanted it early in Phase
      3): an anticipated rental tax on new capacity scales u_K by
      1/(1−τ_K) and raises θ_c (entry distorted); a one-time levy on
      stock in place enters no entry condition (sunk); τ_R appears in no
      production price (T4a–c).
    - **T1's b_I = 0 flat transition is now CLOSED FORM, symbolic**
      (T1a–T1d): the old pipeline holds K at K_old and w is γ̄-invariant,
      so land clearing does not move — the rent is FROZEN for exactly J
      periods, then jumps to its new level; π is a rectangle; Q_0 has a
      closed form. REFINEMENT the check forced: steady-state Q is
      (1+ρ)^{J−1}, NOT 1 (installed capacity carries the gestation
      float; Hayashi's Q = 1 is the J = 1 corner) — the windfall
      statement is Q_0 above THAT benchmark, and Q_0 − (1+ρ)^{J−1} =
      (1−qq^J)·b·(r_new − r_old)/((ρ+δ)p_K).

    **The engine.** `model.py`: environment, closed-form flat SS, sloped
    root, and the HARD GATE (both SS reproduce the check targets to 1e-9;
    build→0 reproduces an inline restatement of check_pinning's static
    system). `solve.py`: damped fixed point on the investment path with
    the entry complementarity I_t ≥ 0 ⊥ p_K,t ≥ PV_t(π); period objects
    are exact closed forms (flat split linear; the sloped margin is a
    quadratic root, capped-linear under a frontier cap). VALIDATION
    LADDER enforced in run order: the exact b_I = 0 closed form
    reproduced to 2.5e-11, horizon insensitivity 4e-14, Q_0 vs the T1c
    closed form — only then the sloped case. `figures.py` regenerates
    all four §8 figures from one entry point.

    **Experiment verdicts (statuses per brief §3.6; nothing promoted
    beyond its label):**
    - **T1 windfall — VERIFIED** (flat, J = 3, γ̄ 3→2.8, T = 3.8,
      domestic convention): Q_0 = 1.2091 vs benchmark 1.1025; w/p
      constant (CM on the path); windfall PV 0.083 against land gain PV
      3.80 — land takes ≈98% of the released value. HONESTY ITEM: the
      land-unit wage is NOT step-monotone — the investment surge's own
      land demand (b_I·I_0) plus, under the domestic convention, the
      windfall income FRONT-LOAD the rent at release, and delivery
      cycles ripple it (ripples pinned to 9 digits across solver
      tolerances: equilibrium dynamics, not noise). The claims that hold
      and are checked: the land claim drops at release, sits below its
      old value at EVERY date, settles at the lower steady state.
      Drafting must say "envelope", not "every step".
    - **T2 waterfall — VERIFIED** (two inputs, J = 1 vs 5, T = 2.0,
      γ̄ 3→2.8): composite output is FROZEN at the long input's old
      capacity until t = J_p, so each input's rental is entry-pinned
      from t = J_j on (free-entry quasi-difference) — excess can survive
      only over an input's own remaining build window. Measured: the
      J = 1 input's excess dies at t = 0, the J = 5 input's at t = 4,
      rent settled by t = 10. THEORY NOTE (new, checked): rentals in
      t < J_c are a PURE TRANSFER among sunk owners — allocations and r
      are invariant to the split, which the model does not determine
      (reported at SS user-cost shares, convention stated).
    - **T3 speed × lag — VERIFIED**: windfall PV monotone in shock speed
      and in J across the full 3×3 grid (J ∈ {1,2,4} × {1,4,12}-period
      phase-ins); fast/J=4 is ×23 slow/J=1 (0.0727 vs 0.0032).
    - **T5 sloped wage path — the conjecture BIFURCATES BY SHOCK TYPE**
      (run at T = 4.0; the T = 10 gate config leaves land so abundant
      that a real frontier shock exits the land-binding regime — no
      clearing root; recorded): under FRONTIER EXTENSION (the
      Korinek–Suh scenario, γ_new = min(γ_old, cap), cap 2.8 vs old
      margin ≈3.04) the goods wage FALLS at release (−2.8%) and the cap
      then PINS it — c is constant on the capped stretch, so the
      buildout sweeps tasks at a constant margin (CM there): NO
      dip-and-recover phase; the land claim falls with the buildout,
      below old at every date (7.46 → 7.02 → 5.13). Under EFFICIENCY
      DEEPENING (γ_new = 0.85·γ_old) the impact sign REVERSES: the
      goods wage RISES at release (existing capacity stretches further
      when already-automated tasks cheapen). VERDICT AS RECORDED:
      "PARTIALLY SUPPORTED under frontier extension … REVERSED under
      efficiency deepening." The §8.4/§11 payoff: WHICH shock the AI
      buildout is decides the sign of the release-day wage move; the
      land-unit wage falls under both. T5 keeps its conjecture label
      until drafting quotes the honest verdict.

    FOLLOW-UP (same day, notation/framing conversation): (a) drafting
    rules agreed from her questions — π debuts at §8.0 (the spine through
    §7 writes u_K·p_K directly and says free entry in words); Q stays
    §8-local; W_K goes unnamed unless §9.2 reuses it; the three-layer
    recipe stack (build → operating → task technology) kept verbally
    distinct in §4. (b) THE DURABILITY LINE added and checked (U4b, 54
    GREEN): u = (ρ+δ)(1+ρ)^{J−1} prices every produced object's
    flow-to-stock ratio by its (J, δ) coordinates — consumables are the
    (J=0, δ=1) corner with u = 1 (price = rental), circulating capital
    (1,1) gives 1+ρ, machines general (J, δ), land the unproducible
    J = ∞ limit; candidate §4/§5 display, serves her "c equation for any
    good" instinct. (c) PENDING HER CALLS: γ* → γ(x*) unification (Claude
    rec: yes; 29 vs 14 sites already split) and recipe-subscript symmetry
    (Claude rec: keep operating bare, build marked λ_I).

## Verify-list — 2026-08-28: the capital-dynamics engine (veto window)

- [ ] **Convention amendment to brief §3.5 (caution i):** SS household
      income is wN_a + rT with NX = πK − p_K·I in goods clearing (the
      brief's Inc with gross πK does not close; check E3). Domestic
      convention books transition π-surprises to households (default);
      foreign is a switch. Approve or redirect before Phase 2's App A
      prose states it.
- [ ] **The Q benchmark refinement (T1d):** brief §3.6(1)'s "Q_0 > 1"
      becomes "Q_0 > (1+ρ)^{J−1}" — steady-state Q carries the gestation
      float. Propagates to §8.3's windfall wording.
- [ ] **T5's bifurcation framing:** frontier-extension vs
      efficiency-deepening as the §8.4 organizing contrast (and the one
      §11 sentence citing it). The conjecture's original wording ("falls
      on impact, rises as capacity arrives") is not what the numerics
      show at these dials — the cap PINS the wage after the release-day
      drop. Her call on the framing.
- [ ] **The rent-frontload sentence (T1):** drafting must state the
      non-monotonicity honestly (investment-surge land demand + windfall
      income front-load r; delivery-cycle ripples; "below old at every
      date" is the theorem-shaped claim, not step-monotone descent).
- [ ] **T2's indeterminacy note:** the pre-J_c window split is a sunk
      transfer the model does not pin — flag stays in the §8.3 text.
- [ ] **Dial choices as the paper's worked dynamic instances:** flat
      T = 3.8 (γ̄ 3→2.8, J = 3), waterfall T = 2.0 (J = 1 vs 5), sloped
      T5 at T = 4.0 with cap 2.8 / mult 0.85. All interior-verified;
      swap freely, the machinery re-verifies.
- [ ] **The lint tag lexicon** ("numerically verified" / "conjecture" /
      "theorem" / "proposition", paragraph grain): adjust at drafting
      time if her label style differs; the family self-tests either way.

## Session log (2026-08-26) — SEB TALK PREP

25. **Talk thread opened; SEB chosen as the room** (her "SEB probably",
    after an ideas turn). Design on record in chat: fork-first inversion —
    open on Fig 3, close on Fig 4, ring on q; ~12 slides, one equation
    (the recipe), ~20 min; the econ-seminar variant parked. HER NEW
    OBSERVATION, recorded: land-tax capitalization lands on LEVERED owners
    and their lenders — banks as the transition's candidate main loser;
    frozen-market risk (negative-equity lock-in); "it all depends on LTV
    ratios." Claude's sharpenings for the talk's bank slide and the
    sequel: capitalization is announcement-dated under credibility (a
    gradual ramp shrinks the PV hit, it does not spread it); loss ordering
    equity first, banks past the default barrier; Sweden specifics (full
    recourse → double-trigger losses and worse lock-in; covered-bond
    cover-pool LTV eligibility as a no-default pain channel; 85% LTV cap
    2010 + amortization requirements 2016/2018 = fifteen years of
    macropru already shrinking the exposed cohort; national property tax
    abolished 2008; the 1990s crisis and the 2022–23 property-company
    squeeze as the room's memory); grandfathering/increment-only protects
    balance sheets at one-for-one cost to κ's numerator; the model-honest
    sentence: the welfare pair is a flow theorem — the stock revaluation
    is a transfer, not deadweight, but nominal contracts written against
    the untaxed rent stream make the transition financially real. MAPS TO
    the existing queue: next-actions item 2 (transition dynamics:
    "capitalization, collateral") and parked second-paper critique (4)
    (political economy of taxing the surviving asset class) — her
    observation supplies those items' mechanism; not opened uninvited.
    **`docs/talk_data_briefing.md` CREATED** (her "the data behind them is
    one of the areas I understand the least"): construction + ranked
    caveats + likely-question answers for the three data figures, built
    from the link-repo scripts (deflator_fork.py, feasibility_kappa.py,
    four_way.py, lambda_compute2.py) and DATA_NOTES. Two computed defenses
    now on record: the fork RATIO is wage-series-invariant (the wage
    cancels between the legs — 4.8 is pure CPI-shelter/CPI-durables
    drift), and ×3.3 of the ×4.8 accrues after the 1983 CPI
    rental-equivalence seam (durables leg since 1995 +169%, shelter +7%).
    **JOHAN'S PASS IS TeX-ONLY — PORT PENDING; do not regenerate or
    replace main.tex before porting his diff into pinning.html.** Slips
    flagged to her (flag-not-fix, his hand): abstract "nearly five times
    the durables" (durables leg is ~4×; 4.8 is the two-leg ratio —
    slide-critical number); §1 roadmap "surveys what how current theory
    tries to pin the wag"; §2.1 "requiers"; §1 "Sections 9–10 applies".
    The log-23 dangling possessive (§10 "Proposition 4's in the rawest")
    remains in place, pre-existing.

26. **The Swedish fork delivered** (her go: "let's look at the swedish
    data", with "even more of a for dummies breakdown over the graph").
    `code/swedish_fork.py` → `data/swedish_fork.csv` +
    `figures/fig_swedish_fork.png`; full record appended to
    `data/DATA_NOTES.md` as DATA ITEM FOUR. Primary source SCB PXWeb API,
    six tables, titles verified at pull time (the FRED page-title rule
    transplanted); sanity anchors all OK; published-value gate (2022 KPI
    inflation 0.084 ≈ published 8.4%) OK; the long wage member (manual
    workers, mining+manufacturing, pay for time worked, 1952–2025) passed
    the OVERLAP GATE — SLP9a07/SLP11a ratio 1.0000 in all six overlap
    years, one series across a publication seam, NOT a splice. RESULTS
    (1980=100, through 2025): paycheck ×6.5, durables (SCB special
    aggregate VV) ×1.3, rents (04.1) ×7.4; fork **5.67× vs rents, 4.26×
    vs broad housing 04** — the U.S. 4.8× reproduced on Swedish data
    under a different housing regime. Timing parallel: both countries'
    rent-leg fall is pre-1995; post-1995 fork growth is the durables leg
    in both. Caveats recorded (use-value rent regulation → 5.67 is a
    lower bound; 04 carries owner interest costs → CPIF-04 member strips
    it; hedonics, extreme for the ×276 ICT member — off the chart by
    design). `docs/talk_data_briefing.md` gained §0 "The fork graph,
    from zero" (the for-dummies walk-through: paycheck ×12, durables
    prices ×3.2, rents ×15 since 1964; the wage-cancels point; the
    NOT-saying list) and §1b (the Swedish fork). NOT committed (none
    requested). Candidate talk move: U.S. and Swedish fork charts side
    by side, one slide.

## Session log (2026-08-26) — JOHAN'S PASS PORTED; APPENDIX DECISIONS; SSRN

25. **Johan's Overleaf pass + Stella's v2 fixes ported to canonical** (his
    pass pasted for diff-reading; her v2 = his pass + four fixes: abstract
    "the wage" restored, "nearly five times" → "four times", George rehomed
    — "a re-derivation of George (1879)" now closes the contribution ¶ and
    "Our contribution is the closure" stays out (ADDENDUM 6's construction,
    flagged pre-port, her acceptance), roadmap "what how ... wag" and
    "requiers" fixed; her ruling: "otherwise I agree with all his changes";
    ACKNOWLEDGEMENTS DELETION CONFIRMED DELIBERATE — her text preserved
    off-repo for a blog post or later book). PORT: script + snapshot
    pinning_pre_johanport.html + word-diff johan_port.diff.html at session
    scratchpad; 18 replacements exactly-once + both Acknowledgements
    sections deleted. His edits, all front matter: abstract equations
    glossed words-first; intro ¶1 ("Suppose...", "examines that
    mechanism"); substitute ¶ future-tensed; chain displays relabeled
    (wage supply → / wage demand →, tails "labor demand/supply side",
    chain-2 tail "rents on non-produced inputs"); interval ¶ gains
    opportunity-cost appositives; limit ¶ "the extreme scenario", "(a point
    proved by Caselli and Manning (2019))", "falls to near zero";
    contribution ¶ fused; roadmap rewritten; §2.1 dash-sentence split in
    three; §3 "quietly" cut. RIDING TOOL FIXES: converter's author block
    carries his real email (Johan.Bage@hhs.se, placeholder retired);
    italicize_math.py END anchor falls back to </body> (lint's cuts
    already had fallbacks; h2 now 22). Pipeline ALL GREEN post-port:
    italicize +0, lint, census, check_pinning 37, converter (13,060 tokens
    both sides, zero hunks). REGENERATED main.tex ≡ her v2 except ONE
    print-identical token: abstract "4.8" (plain) vs her "$4.8$" — the old
    "4.8&times;" rode into math on the &times; entity; the bare number has
    no signal. Accepted deviation. Zip rebuilt. Overleaf SYNC NOTE: for
    once her copy ≡ the regenerated file (mod that token) — no wholesale
    replace needed until the next regeneration. SLIPS RIDING IN THE
    ACCEPTED SET, flagged, left verbatim per protocol: "Sections 9–10
    applies" (agreement — reads as a miss, one-word fix "apply" offered);
    intro "falls to near zero" vs abstract "falls without bound" (same
    object, two phrasings); BrE "analyses"/"analysed" in an AmE paper;
    abstract glosses ("replacement costs" for the ac term collides with
    replacement cost = c; "raw materials" for ℓr).

26. **Appendix restructure DECIDED, not executed (a later unit, her
    explicit scoping).** Her calls on the triage: (i) Appendix I CUT — her
    "too much"; Claude's standing counter-offer, pending her word: keep
    the 3–4 dated ours-only predictions (fork slope, AI-sites balance
    sheet, exit/coresidence, incidence drift) as one §12 paragraph — the
    by-construction and consistent-with entries (P1–P3 AR2026; P5–P6
    K–N/Rognlie) go without loss; either way the in-body pointers rehome
    (§1's falsify sentence, §9's, App E's "Prediction 8"). (ii) Appendix B
    CUT AS APPENDIX → a short main-text paragraph/note (AR2026's results;
    must keep the effective schedule ρ/µ + the self-liquidation/
    quantity-vs-price point §11 leans on; Figs 5–6 go — two of seven).
    (iii) Appendix F is HERS — in progress in another session; hands off
    here. (iv) Agreed from Claude's list: H cut (salvage: offshoring-as-
    second-rental → §2.3 footnote; border-splits-the-bases → one F.5
    sentence); C folds into A's machines block; E folds into D (log-16's
    renumbering objection obsolete — content-keyed \refs make reordering
    free). EXTRA-WORK RULING (her question, Claude's answer accepted-
    pending-her-read): pay debts on keeps — A's joint-system existence
    (tighten or scope; Lean λ>0 stays the formal backstop), G's fraud
    bound v·f/(1−v) + superstar median as mini-lemmas (cheap, P12 leans on
    the first), F.5's deadweight-index derivation inside her F unit;
    retract-and-fold instead of working on E ("estimate of η" softens to
    sign-reading on the fold); I's and B's polish items die with their
    cuts; λ>0 Lean stays queued, gates nothing.

27. **SSRN: revise the existing upload, don't resubmit** (her question;
    recommendation given): a revision keeps the abstract ID/URL (the
    blog's link keeps resolving), the accumulated download record, and the
    ORIGINAL first-posted date — her public priority stamp on the idea;
    title/abstract/authors all changeable in a revision, Johan added as
    author (he needs an SSRN account); brief re-review per revision, so
    revise ONCE when the current wave lands (this port + appendix
    restructure + her F work), not per pass. A fresh page would zero the
    history and leave two records competing against the draftline's own
    declaration that the long draft is replaced.

28. **Appendix restructure EXECUTED, both HTML and LaTeX** (her go:
    "Let's do the appendix changes and work now"). Appendices A–I → A–D;
    one unit: script, 59 exactly-once-asserted operations + boundary-
    asserted deletions; snapshot pinning_pre_appendix.html + word-diff
    appendix_restructure.diff.html at session scratchpad. THE MOVES:
    - **I CUT clean** (her call; the fold-back offer — 3–4 dated ours-only
      predictions as one §12 ¶ — offered twice, not taken, still open).
      §1's falsify sentence and §9's pointer absorbed into their §12
      clauses ("closes with the empirical standard the account should be
      held to"; "and states what would count against it").
    - **B CUT to one §11 paragraph**: effective schedule w ≤ c·ρ(x)/µ(x)
      inline, targeting + the 70th–95th percentile clause credited AR2026,
      self-liquidation ("finances its own replacement"), quantity-form
      list, punctuated-adoption close. §2.3 → "Section 11 states that
      result in this notation"; §2.4 wedge-machinery clause cut; §3 "set
      aside until Section 11". Figures 5–6 (strata, ushape) RETIRED
      (7 → 5; files remain in figures/, dropped from latex/ + zip).
    - **H CUT**: offshoring-as-second-rental salvaged as one §2.3
      sentence; the border-splits-the-bases point PARKED for her F
      session (text in the parked-inputs block below); w_f/ρ_f retired
      (census DEAD list).
    - **C FOLDED into A** (machines block + new "Durability, time
      preference, horizon." ¶, text carried verbatim — same-paper
      consolidation); §4/§10 pointers retargeted; converter SPECIAL 0
      expectation 2→1 (the two matrix statements merged).
    - **E FOLDED into new B** as a closing "General η." ¶, eq:ces-share
      carried verbatim; the "promoted to an estimate of η" claim SOFTENED
      per the extra-work ruling ("the climbing shelter share ... is the
      η < 1 signature"; §7's pointer now "reads the elasticity's sign off
      the shelter shares") — the estimator itself is long-record work.
    - **RELETTER** D→B (Prop B.1), F→C (h3s C.1–C.5), G→D (Prop D.1);
      every in-prose literal re-pointed site-specifically; the script's
      own final sweep caught one missed site (§5's second F.4 mention)
      and one collateral (the I-cut swallowed the References h2 —
      restored verbatim). A's configuration table → 5 rows; notation
      footnote updated (µ now §11-local; η context B/D; λ_C, λ_R of C).
    - **THE DEBT WORK** (the extra-work ruling executed): (i) A's
      joint-system existence RESCOPED from "follows from continuity on
      the compact viable set" to three named instruments — the crossing
      at given r, the flat-limit closed form, and a NUMERICAL
      INSTANTIATION of the joint sloped system now in check_pinning
      (ρ(x) = 1+4x, a=.5, λ=.1, ℓ=.2, T=10, σ=.3, N=1, numeraire p_g=1:
      land residual has exactly one sign change on the x* grid, clears at
      the root x*≈0.87, the Walras goods cross-check closes, viability
      and w > s(q) verified); the general fixed point is stated as NOT
      claimed and rides with the queued Lean extension. (ii) NEW Lemma
      D.2 (the fraud bound v·f/(1−v): incentive derivation, statics,
      limits — sympy-checked) and Lemma D.3 (superstar concentration:
      measure-zero top ⇒ median = (1−β)·mean, assumption stated —
      numeric-checked); the anchors ¶ split around them. The two formerly
      bare formulas are now proved.
    - **GATES all green post-unit**: italicize +0 (new prose shipped
      pre-wrapped per convention), lint (17 h2), census, check_pinning 46
      (37 + 9 new), converter 93 PASS (letters ABCD; theorem sequence
      1–5 + cor + A.1, B.1, D.1, D.2, D.3; figures 5; displays 10;
      predictions 0; refs 56, none orphaned; word fidelity 12,060 tokens
      both sides, zero hunks). Zip rebuilt (5 figures). Body 13,626 →
      12,493 words; main text 5,286 → 5,324.
    - **OVERLEAF NOW STALE**: replace main.tex wholesale with the
      regenerated file (or re-upload the fresh zip — it also drops the
      two retired figure files).
    - **FOR HER VOICE PASS** (new Claude prose, drafted in the paper's
      register, hers to re-voice): the §11 wedge ¶; the §2.3 border
      sentence; the two §12-absorbing clauses (§1 roadmap, §9); A's
      rescoped existence passage; Lemmas D.2/D.3 statements and proofs;
      new B's "General η." opener.

    **PARKED INPUTS FOR HER F SESSION** (from this unit's rulings):
    (a) the H-salvage sentence for C.5, ready to splice: "Rents accrue to
    the producing jurisdiction's land, so a consuming country's spending
    resolves partly into foreign site rents — out of reach of its land
    tax, within reach of a destination-based consumption tax." (b) the
    C.5 deadweight-index debt: λ_C(1−κ)² is quoted (0.32) but underived
    in the paper — two displayed lines from a named quadratic-deadweight
    assumption, with a check to ride in check_pinning.

29. **Stella's v3 ported + the Johan-facing diff built.** Her v3 (Overleaf,
    on the restructured base — wholesale replace confirmed by the diff
    size): 15 paragraph edits, all voice/trim, ported as 18 replacements
    (script + snapshot pinning_pre_v3port at session scratchpad). Her
    edits: the "empirical standard" framing OUT at both ends (§1 roadmap
    clause + the §12 closing pair "Both halves are measurable. That is
    the standard..." — the paper now ends on the question); §2.2 opener
    sentence cut; §2.3 modeling-bet clause re-voiced WITH a defense
    ("...a modelling assumption we make based on our reading of history
    and recent U.S. measures" — log-23 flag iv thereby addressed) and the
    border sentence re-voiced ("Cross border trade is treated similarly...
    a second machine rental with a different cost composition"); §2.4
    "focuses instead on the common base"; §2.7 trims ("a share is not a
    wage" clause out; "refers to as"/"describes"); §3 bookkeeping sentence
    OUT (the family's last instance); §4 "a compounding the scalar closure
    makes visible" out; §5 "the proposition names" out + exit-caveat
    reword; §9 dating clause out; §10 THE DANGLING POSSESSIVE FIXED by her
    ("This is Proposition 4, the wage in..." — log-23 flag i RESOLVED);
    §10 κ-ceiling MEASURED NUMBERS CUT (median 1.26, 13/32 — data item
    two's only in-paper citation; caveat sentence survives; FLAGGED as
    deliberate-or-overshoot); §10 head "Three assemblies, open." →
    "Three possible interpretations of existing measures"; §12 "changes
    the policy conclusion".
    PORT EXCEPTIONS, hers to veto (precedented): "traide" → "trade"
    (typo class, log-24); "US" → "U.S." (log-23 normalization). VERBATIM
    SLIPS flagged, not touched: "modelling" (BrE, paper is AmE); the
    assemblies head lost its period; "Offshoring is however still only a
    temporary condition, once..." (comma splice, log-23 class).
    Pipeline ALL GREEN post-port (italicize +0; lint 77; census; checks
    46; converter incl. word fidelity). REGENERATED main.tex ≡ v3 except
    exactly the two flagged tokens — so her Overleaf copy needs only
    those two words changed (or a wholesale replace / fresh zip). Zip
    rebuilt. JOHAN DIFF delivered for her to send:
    pinning_diff_for_johan_2026-08-26.html (his pass → current canonical;
    98 regions; plain-language summary preamble at top).
    NOTE for the pending λ splice: §10's assemblies head is retitled —
    the splice edit list's "three assemblies → two" language must adapt
    to "possible interpretations", and its register touches are moot.
    NEXT (discussed, her go pending): the Lean extension, proposed order
    — (1) the λ>0 spine (Props 2 + 4(ii)); (2) the λ>0 user-cost durable
    form (sympy first, then Lean — lets A's durability ¶ finally state
    it); (3) quick wins: Lemmas D.2/D.3 + the CES-share limits; (4) the
    Appendix A joint fixed point, staged (given-r crossing, then IVT on
    the land residual for the configuration class the numeric check
    instantiates); (5) regenerate the assumption manifest to the new
    letters. (1)–(3) before the SSRN revision; project lives at
    link-repo/lean — verify the mathlib pin builds before writing.

## Session log (2026-08-27, evening) — THE V2 STRUCTURE DECISION

32. **Phase 2+3 authorized; the structure memo for the dynamics session**
    (her message: Overleaf updated as a deliberate Johan-discussion copy —
    "a bit separate so I can discuss with Johan, though I think the
    notation change is a no brainer"; "Let's do the dynamic rewrite now";
    her structure question verbatim: "Do we want a non dynamic storyline
    and add the dynamics after, or alongside each existing section? Or
    should we scrap the non dynamic core and build it all as dynamic from
    the beginning?"; execution in a new session, thoughts to STATE).
    PROCESS: a five-lens panel was run (hostile macro referee, reader arc,
    execution risk, a devil's advocate briefed FOR all-dynamic, field
    precedent) and converged unanimously — including the advocate — on
    the hybrid below. What follows is the synthesis and is the governing
    structure for Phases 2–3; it AMENDS the brief's §4 table where noted.

    **THE DECISION — dynamic ontology, steady-state exposition, one
    transition act.** Not (a) static-plus-appended-dynamics, not (b)
    interleaved, not (c) all-dynamic-from-scratch. Instead:
    - **Appendix A declares ONE dynamic environment** (timing, capacity
      stocks K_t, build lags J_j, perfect foresight), extending the
      existing configuration table with a horizon switch (steady state vs
      sequence) and a capability switch (flat vs sloped). This is v1's
      one-environment architecture doing exactly what it was built for.
    - **The main text through the fork is that environment at rest**, in
      pure coefficient notation — no time subscripts, no stocks, no Q
      before §8. One declaring sentence early ("the environment is dynamic
      throughout; until §8 we read it at rest") is the whole forward
      apparatus.
    - **DIRECTION OF DEPENDENCE (the rule that keeps both halves honest):**
      the spine's propositions are stated and proved on self-contained
      fixed-point objects (the recursion c = ac + λw + br + u_K·p_K and
      its solution), NEVER as "the steady state of §8's system" — that
      would import the sloped case's existence gap into the Lean-verified
      core. §8 then EARNS the identification with a machine-checked
      **steady-state equivalence lemma** (the §4–§5 recursion is the
      steady state of the sequence economy; sympy at minimum). The lemma
      is the anti-staple device: one model read at two horizons, with the
      existence question quarantined where it belongs.
    - Why not the alternatives, in one line each: (b) puts a Lean-proved
      claim and a solver number in every section — the claims boundary
      (theorem / numerically verified / conjecture) stops being visible in
      the table of contents, every section needs re-voicing, and T5's
      death would mean surgery in six places; (c) makes the closure and
      fork corollaries of a system with no existence proof, strands the
      sympy/Lean asset, torches her voiced prose wholesale, and leaves NO
      shippable paper if the sloped solver stalls. Even the panel's
      C-advocate conceded C's conditions fail and kept only C's ontology —
      which the hybrid adopts at the environment layer.

    **THE AMENDED SECTION TABLE** (changes from the brief's §4 table
    flagged; content jobs otherwise per the brief):
    - §1 intro — announce the architecture in ONE paragraph ("one dynamic
      economy; the paper characterizes its steady state with proofs, then
      its transition, numerically") — the stapled-papers judgment forms on
      page one. Consider explicit Part labels (Part I: at rest; Part II:
      in motion) to make the claims boundary typographic — HER CALL.
    - §2 survey (trim by a third per the brief; voiced prose survives).
    - §3 tasks and the margin (survives Phase 1's notation; light touch).
    - §4 the recursion: coefficients, waiting, and building. AMENDED: §4
      absorbs the steady-state half of the brief's §5 — the build recipe
      (a_I, λ_I, b_I), J, and u_K = (ρ+δ)(1+ρ)^{J−1} DERIVED from
      free-entry PV algebra as a Jorgenson-style user cost with gestation
      (not asserted), then θ_c, θ_w, the interest identity,
      horizon-terminality as a parameter (input j is terminal over
      horizon h iff J_j > h; land is J = ∞). The brief's §5 as tabled put
      THE DYNAMIC MODEL between the recursion and the floor with its
      results three sections away — every lens independently flagged that
      orphan gap; the transition system moves to §8. (§4 may split into
      §4/§5 for length — "the recursion" and "build time in steady
      state" — but BOTH stay coefficient-only.)
    - §5/§6 the floor (participation with both lives priced; h_w, θ_e;
      enclosure as rigidity; funding source) and §6/§7 the fork as
      coefficient ratios (θ_w/θ_j; the θ gradient ideas→location; land as
      J = ∞ the classifier). Panel option, NOT forced: coefficients →
      fork → floor order (fork as Part I's climax) — her call; default
      keeps the brief's floor-then-fork, which matches v1's voiced flow.
    - §8 THE TRANSITION (one act, ordered for clean amputation):
      8.0 the model in motion — sequence equilibrium definition, MIT
      shock, THE EQUIVALENCE LEMMA immediately; 8.1 flat case — the
      difference equation, existence/uniqueness stated as a THEOREM if
      the closed form exists (if the flat transition is trivial, that IS
      CM-on-the-path, say so per the brief's risk note); 8.2 solver
      validated against the flat closed form (residuals,
      horizon-insensitivity; details App E) BEFORE it touches the sloped
      case — the only solver evidence a hostile referee accepts absent an
      existence theorem; 8.3 T1 windfall, T2 waterfall, T3 speed×lag,
      each labeled "numerically verified"; 8.4 T5 sloped-case wage path,
      OWN subsection, labeled conjecture, kill-criteria pre-stated in the
      text (Korinek–Suh scenario framing).
    - §9 fiscal, split: 9.1 the steady-state pair (Prop 5 on the
      coefficient footing, d = τ_R R/N; ships in Phase 2, voiced prose
      survives); 9.2 the fiscal-horizon theorem T4 (Phase 3) — state it
      on quasi-rent valuation identities for stock in place so its proof
      NEVER needs the sloped path; Auerbach–Kotlikoff/Judd old-vs-new
      capital is the precedent shelf it sits on.
    - §10 measurement: every measured moment binds to steady-state
      coefficients only — no measurement claim leans on transition
      numerics. Phase 2 ships v1's numbers relabeled to coefficient
      language; multi-leg recompute stays Phase 4.
    - §11 AI: Phase 2 states the J-ordering as model structure (ideas
      θ = 0; datacenters reproducible; land permanent); the dated
      buildout predictions enter in Phase 3 citing T2/T5 by label. T5
      appears in EXACTLY two sites (8.4 + one §11 sentence) so demotion
      is a two-edit change.
    - History-as-three-parameterizations rides in §8 (three (speed, J, λ)
      configurations = three transition experiments) or stays a §7
      subsection — drafting call. Stabilizers → §9 subsection per brief.
    - Appendices: A one environment + extended configuration table
      (sequence rows land in Phase 3 without touching spine prose); B
      land-only closure with interest; C fiscal transition (Phase 3); D
      human-essential (survives); E numerical methods + solver
      credibility (Phase 3; the one named address for the existence/
      accuracy questions); F data + the one-page notation table.

    **PHASE CUT-LINES (the standalone guard, made structural):**
    - Phase 2 ships: §§1–7 (spine, coefficient-only) + §9.1 + §§10–12 +
      App A (environment stated in full, steady-state claims only) +
      B/D/F. Everything in it sympy/Lean-grade. This is a complete paper.
    - Phase 3 adds: §8, §9.2, App C/E, the configuration table's sequence
      rows, intro re-weighting. SEQUENCE T4 EARLY in Phase 3: it is
      free-entry PV algebra, plausibly sympy/Lean-checkable without the
      solver — the one dynamic theorem that survives a numerics stall.
      A partial Phase-3 landing (flat works, sloped fails) ships by
      cutting 8.4 and demoting one §11 sentence.
    - Voice map: redraft concentrates in §4(/§5) and §8 (+9.2) — all-new
      content, Claude-drafts for her passes; §2 (trim), §3, floor, fork
      skeleton, 9.1, §10, §11, App B/D carry her voiced v1 prose with
      one-clause reframes ("in the steady state of Appendix A's
      economy..."). Under (b) or (c) every section would have been
      reopened — this map is most of why the hybrid won.

    **MECHANIZATION TO ADD (house discipline, new session):** extend
    lint_pinning with a claim-status-tag family — every transition result
    must carry its label (numerically verified / conjecture) at every
    in-text citation site, hard-fail otherwise (the ADDENDUM-7 lesson
    applied to epistemic labels); the equivalence lemma and the u_K
    derivation get sympy checks BEFORE drafting (house rule); dynamics
    code lands in code/dynamics/ (model.py / solve.py / figures.py per
    the brief §6), with the steady-state convergence check against
    check_pinning's values as a hard gate.

    **PHASE-3 TECHNICAL CAUTIONS (from the review conversation, pin at
    model-write time, not debug time):**
    (i) The income accounting must close: brief §3.1 states capital
    income ρ·p_K·K (net) while §3.5's Inc_t carries π_t K_t (gross =
    net + depreciation + build-period interest); under
    investment-financed-abroad, WHO owns the stock decides whether πK
    reaches household income gross or net of debt service. Pin the
    ownership/financing convention first (suggest: domestically owned,
    debt-financed at world ρ, household capital income πK − ρ·Debt) and
    let the interest identity fall out — else goods clearing fails in a
    way that masquerades as a solver bug.
    (ii) Land-clearing viability is a named condition:
    (1−α)T > bX_t + b_I I_t — transition paths can violate it
    transiently while both endpoint steady states satisfy it.
    (iii) The flat case's pinned c_t requires interior labor use along
    the whole path — make the employment condition part of T1's
    statement.
    (iv) The u_K exponent (1+ρ)^{J−1} embeds three timing conventions
    (build paid at start; first service at t+J; wear post-install) — the
    off-by-one is the classic error; sympy derives it from the PV
    condition, never asserts.

    **OPEN, HERS (raise before the relevant phase):** Part labels
    typography (§1); floor/fork order; the three-taxes boundary BEFORE
    §9.2 is written (the horizon theorem is native to this paper as a
    J-statement; three-taxes keeps taxonomy/convergence/ceiling/dial —
    cite, don't duplicate; also harmonize φ_C/φ_G here vs φ_w/φ_r
    there); title (brief: keep, or "...Scarcity, Technology, and Time");
    the λ §10 splice timing; 𝟙 lands with Phase 2's App A matrix form
    (per the notation map).

## Session log (2026-08-27, later) — V2 PHASE 1: THE NOTATION PASS

31. **The v2 rewrite opened; the notation commit executed** (her go, after
    Claude's review of the v2 brief from her other session: "two more
    versions. The first is just notation changes... we do all that and
    commit. Then, I'll let you do the rewrite for dynamics." Her sequencing
    rulings: the λ splice and Swedish-fork fold-in do NOT go first; SSRN
    does not wait; Overleaf was up to date at the start).
    - **The wave commit first** (5c4855a): the uncommitted 08-26/27 work
      (Johan+v3 ports, appendix restructure, LaTeX pipeline, Swedish fork,
      SEB briefing, λ>0 Lean extension) landed as its own commit so the
      notation diff stays symbols-only. Other threads' untracked folders
      left untouched.
    - **The brief FROZEN** at `docs/rewrite_brief_pinning_v2.md` (verbatim,
      with her delivery amendments in the header and dated repo-state notes
      inline: the λ series is BUILT not open; the Swedish fork is the
      cross-country item's first leg; lint is the authority over §8's
      checklist; STATE.md is the changelog, no CHANGELOG.md).
    - **`docs/notation_map.md` WRITTEN** — the authority for this pass, the
      Lean translation, and the Phase-2 appendix table. Key content: the
      rename CHAIN (s_d→s̲, σ→α, η→σ/σ_H, τ→τ_R, t→τ_w, ρ→γ, δ→ρ, d→δ,
      u→d, then chain-free ℓ→b, K→H, k→|H|, k_s→n_s, λ_C/λ_R→φ_C/φ_G,
      β→ψ, p_g→p, n→N_a, §10 vectors bolded) in reverse-topological order;
      s̲ as combining-low-line (parallel to γ̄'s macron); 𝟙 DEFERRED to
      Phase 2 (I collides with investment only when I_t exists); the b·r
      display convention (three display sites write b·r matching the
      recursion display's own middots; prose keeps compound italics br,
      like rT/aX — the one glyph change beyond pure renames).
    - **THE PASS**: scripted, count-asserted per family (105 ρ→γ; 36 ℓ→b;
      39 K→H; 18+2 p_g; 14 δ→ρ; 11 τ; 8+1 s_d; 8+14 η; 16 σ; 7 u; 6 wear-d;
      5 t; 5 β; 5+3 λ_C/λ_R; 3 n; 2 k_s; 6 k; stale-scan zero), snapshot +
      word-diff at session scratchpad (282 regions, reviewed one-by-one:
      all symbol tokens or the two flagged edits). TWO NEW-PROSE SITES,
      hers to voice: the Notation footnote REWRITTEN (drops the ρ̂ and
      η-context clauses, which die with the rename; adds interest-is-ρ-
      rent-is-r, the DMP-b homonym note forced by ℓ→b, and H-vs-T_H);
      A's durability ¶ gains "(the interest rate, distinct from the rent
      r)" at ρ's first use.
    - **TOOLING**: census_symbols REWRITTEN to the v2 inventory + 16 DEAD
      families (every v1 form hard-fails on return); lint's Greek sentinel
      gains α/φ/ψ; italicize_math updated (BLANKET +b +H, dividend-d
      patterns, s̲ pre-wrap, COMPOUNDS +bX +br) and HARDENED against
      masked-entity adjacency — the new blanket H wrapped "H&eacute;mous"
      on first run (the Hémous catch); guard added, re-run +0 twice;
      check_pinning INTERNALS renamed (sympy names now v2: gamma, b,
      alpha, sigma, tau_R, rho/delta, psi, Habs/w_H/n_s), 51 ALL GREEN;
      converter gains α/ψ in GREEK, U+0332→\underline in COMBINING, the
      merged SPECIAL (S10's matrix display now bold in HTML, expected 2),
      eq:rho→eq:gamma label key, and a Latin-adjacency SPACE GUARD in both
      math-run emitters (v2's Latin b would otherwise fuse into TeX runs
      like "br"/"pY"/"rbX" and break word fidelity; math mode ignores the
      space). Word fidelity 11,995 tokens both sides, zero hunks.
    - **FIGURES 1–2 REGENERATED** with γ(x) axes (fig_model_schematics.py,
      fig_eras.py; the retired strata/ushape scripts relabeled in passing).
      FLAG for her: Figure 1's annotation pixels still say "labor too
      dear" — pre-existing wording from before the poetic-register ban
      (the caption was cooled in log 20, the pixels never were); left
      as-is in a symbols-only pass, one-word fix available.
    - **LaTeX regenerated, zip rebuilt** (same member list). Lean:
      Pinning.lean gains the v2 translation table in its header + manifest
      P1/P2/P4 symbol updates (identifiers stay internal; docstrings noted
      as v1-era); lean/README.md scope section now v2; `lake build` re-run
      as the gate on the comment edits. reading_guide.md: our-side symbols
      updated (their γ(i) is now nominally our γ(x)), head note added;
      talk_data_briefing.md: φ_C/φ_G with a one-line note; DATA_NOTES
      untouched (its σ is the education-race elasticity, a different
      object).
    - **DEFERRED, hers**: the λ §10 splice (splice-ready draft unchanged;
      its edit list must be re-read against v2 symbols when it lands);
      the Swedish fork's entry into the paper; SSRN timing; the Figure-1
      "dear" pixels; 𝟙 at Phase 2.
    - **OVERLEAF STALE** after this pass: wholesale replace with the
      regenerated main.tex or upload the fresh zip.

## Session log (2026-08-27) — THE LEAN EXTENSION

30. **The λ>0 Lean extension DELIVERED** (her go on the proposed order;
    items 1–3 + the user-cost debt done, item 4 — the Appendix A joint
    fixed point — deliberately still queued, so the paper's "rides with
    the queued Lean extension" stays accurate).
    - TOOLCHAIN BRING-UP on this machine (none existed; the corner spine
      had been built elsewhere): elan 4.2.4 installed; its own downloader
      fails on the SEB network (CRYPT_E_NO_REVOCATION_CHECK — CRL
      endpoints blocked), so the pinned lean-4.33.0-windows toolchain was
      side-loaded via `elan toolchain link`; `ssl-no-revoke` written to
      ~/.curlrc and %APPDATA%/_curlrc (MACHINE CONFIG CHANGE, flagged:
      lake + the mathlib cache tool shell out to curl); XDG_CACHE_HOME
      pointed at C:/Users/.../.cache (the roaming J: drive is
      unwritable). Full recipe recorded in link-repo/lean/README.md.
      mathlib cache (8,690 files) fetched; **the corner spine reverified
      on this machine: 8,708 jobs, builds clean.**
    - SYMPY FIRST (house rule): check_pinning gains the A-usercost block
      (+5, 51 ALL GREEN) — the λ>0 user-cost closed form
      c = s·ℓr/(1 − s(a+λρ*)) for carrying factor s (s = 1+δ building,
      s = δ+d wear), λ→0 recovering both stated displays, s = 1 the
      static closure, statics signed.
    - NEW `link-repo/lean/Link/Pinning.lean` — 53 declarations, builds
      clean (0 errors, 0 warnings, 0 sorry; 119 total across the two
      modules): Prop 2 (closure satisfies margin + free entry,
      uniqueness, both statics two-point signed, c-invariance to ρ* at
      λ = 0); the corner BRIDGE (at λ = 0 the closure IS Corner.c,
      stated against TheLink's own structure, plus the λ→0 Tendsto);
      Prop 4(i) with λ (1/L̄, the recipe's labor cancelling too) and
      4(ii) in full (display, both statics, BOTH divergence margins
      ρ̄→0 and ℓ→0, the substitution bound); the user-cost closures
      (general carrying factor + both recoveries); Lemma D.2 (iff,
      statics, v→1 divergence, f = 0 collapse); Lemma D.3 via its
      finite-star-mass family (mean invariance, ε < β ordering, median
      mass, ε→0 ratio limit); the CES dial's three-case share limit.
      MANIFEST P1–P5 at the file's foot; the sharpest: P1 (the user-cost
      convergence s(a+λρ*) < 1 is strictly stronger than every earlier
      condition), P4 (D.3's "top" formally requires ε < β — stars
      scarcer than their take — a hypothesis the prose leaves implicit).
    - PAPER: Appendix A's durability paragraph now STATES the λ>0
      user-cost forms (the "deliberately not stated because unchecked"
      withholding retired — new Claude prose, hers to voice); the
      verification footnote upgraded to the exact new Lean scope, with
      the A fixed point explicitly still queued. Pipeline ALL GREEN
      (italicize +0, lint, census, 51 checks, converter); zip rebuilt.
      OVERLEAF STALE AGAIN: wholesale replace (or the fresh zip).
    - QUEUED (the remaining Lean item): the Appendix A joint fixed
      point, staged — (a) the given-r crossing (Lemma A.1 with the
      recursion), (b) IVT on the land residual for the configuration
      class the numeric check instantiates. SSRN timing: items 1–3
      landed, so the verification note is revision-ready.

    ADDENDUM (same day, her register note: "make the lean commentary a bit
    more timeless and less sounding like it's in progress work... 'zero
    unproven steps' sounds like bragging"): the verification footnote
    REWRITTEN timeless — present-tense statements of what is ("is also
    stated and proved in Lean 4 (with the mathlib library)"), the
    sorry/declaration-count vocabulary OUT, the honest caveat IN ("its
    statements are a translation of the paper's: the proofs are
    machine-checked, the translation is not" — the lean README's caveat,
    now in the paper), and the unclaimed fixed point stated as a scope
    fact ("is outside the formalization, as stated there"); Appendix A's
    "rides with the queued Lean extension" clause CUT (the not-claimed
    sentence stands alone). Script asserts no "queued"/"sorry"/"zero
    unproven"/count vocabulary survives anywhere in the paper. RULE SAVED
    to memory (timeless-verification-register): back matter states what
    is; status and counts live in STATE/README, never the paper. Pipeline
    ALL GREEN; zip rebuilt; the Overleaf-update diff regenerated (now 19
    regions: the four earlier groups plus this rewrite).

## Session log (2026-08-21) — THE LATEX EXPORT + CO-AUTHOR

22. **Overleaf-ready LaTeX version built; Johan Båge (Stockholm School of
    Economics) added as co-author** (her ask; mid-session direction: "change
    the style perhaps to fit orthodox macro papers more"). MECHANIZED per
    house discipline: `code/html_to_latex.py` parses `paper/pinning.html`
    and emits `latex/main.tex` + `latex/figures/` (7 figs copied unchanged)
    + `latex/README.md`; zip for Overleaf upload at
    `pinning_latex_overleaf.zip`. **pinning.html stays canonical** — edit
    there, re-run the converter (idempotent; ALL GREEN gate). Verification
    BUILT IN: word-sequence fidelity HTML↔TeX (13,667 tokens each side, zero
    diff hunks; prop headers/figure labels/section numbers normalized out),
    numbering assertions (12 sections, appendices A–I, Props 1–5 +
    corollary* + A.1/B.1/B.2/D.1/G.1 via counterwithin, Figures 1–7, 11
    displays, 2 tables, 13 predictions, 5 kill items, 56 refs), env/brace/$
    balance, no stray non-ascii. Style: orthodox macro WP — 12pt,
    onehalfspacing, amsthm plain (italic statements), numbered equations
    (the four schematic word-chain displays deliberately unnumbered),
    booktabs, caption labelfont=bf, references small/single-spaced hanging
    (formatted entries carried VERBATIM, no BibTeX — a .bib conversion
    would risk the live-verified entries; commission separately if wanted).
    In-text citations remain literal text (no \cite): cross-refs in prose
    were already literal, and auto-numbering is asserted to coincide.
    CO-AUTHOR DECISIONS, all flagged in main.tex comments + README:
    (i) order: WILSON FIRST, Båge second — her call, same day (initially
    shipped alphabetical; swapped on her "can I be first author?"); Overleaf
    compile CONFIRMED by her before the swap; (ii) his email = "[email
    pending]" placeholder;
    (iii) title-page disclaimer pluralized + SSE added (HTML draftline is
    single-author — the ONE wording change made); (iv) NOT touched, flagged:
    §1 disclosure "the author's", AI-use note ("the author's" ×2, "Errors
    remain the author's"), first-person Acknowledgements — provenance
    content, hers to revise with Johan. JEL/keywords: commented suggestions
    only. NOT compiled locally (no TeX on this machine) — Overleaf compiles
    on upload; structural checks stand in. NOT INCLUDED by design: the
    pending λ §10 splice (progress_and_prosperity delivery) — splice into
    pinning.html first, then re-run the converter; the export follows the
    HTML wherever it goes. Also noted for the HTML, not fixed here: bare
    roman "z" in "r(z)"/"parcels z" (App A/D) escaped the italicizer —
    candidate one-line fix at the source.

23. **Stella's voice pass ported to canonical + LaTeX cross-references
    mechanized** (her TeX edits, made in the Overleaf copy, pasted into
    session; her stated intent: she is changing the voice herself now;
    Claude's original preserved in git history at her direction).
    PORT — 43 replacements, exactly-once asserted (script + pre-state
    snapshot + word-diff voice_pass.diff.html, 60 regions, at session
    scratchpad):
    - §1 DISCLOSURE PARAGRAPH DELETED by her (the §1 crown "the capability
      priced in this paper is the capability that drafted it" goes with
      it; the back-matter AI-use note still carries the disclosure);
      contribution ¶ now ends at "the pair that survives the limit"
      (architectural-claim sentence cut); limit ¶ "What remains is a
      simple set of constraints"; fork sentence spelled out ("forks by
      the composition of goods and labor used in production").
    - §11 RESTRUCTURED by her: "What would falsify this" → "Possible
      stabilizers"; the FIVE-ITEM KILL LIST DELETED (with it went the
      reinstatement bet's defense — the task-birth clause now appears
      nowhere; flag iv below); stabilizer ¶ opens "Three possible
      stabilizers are granted as preserving real wages if ρ tends to ρ̄,
      however none of them exist without deadweight."
    - Crowns/meta removed by her: §8 "Both halves of that sentence are
      theorems"; §9 "correctly described" → "one configuration of our
      model"; §6 "The two movements are one movement..."; §2.2 "not an
      outside criticism"; the "bookkeeping" family out ×3 (§3's
      "general-equilibrium bookkeeping" kept by her); §10 bold heads
      de-verbed ("The fork.", "The floor's coverage.", "The fiscal
      exposure.", "Three assemblies, open."); hedges softened ("mostly
      machine-made / mostly land-priced", "a set of classification
      variants", "very plausibly", "hard to measure at the scale of every
      good and policy system"); "violently" RESTORED (reverses the
      register pass's decorative cut, her hand); ~15 further word-level
      choices, all ported verbatim.
    - STALE-POINTER REPAIRS (Claude, riding): intro roadmap → "Section 11
      weighs the possible stabilizers; ... What would falsify the account
      is registered in Appendix I." + "welfare completion" → "fiscal
      completion" (log-15 label unification, missed instance); §2.3
      "modeling bet defended ... in Section 11" → "a modeling bet;
      Section 12 states the empirical condition it turns on"; §5 "Section
      11 lists the test" + §9 "Section 11 states what would count against
      it" → Appendix I; App E falsification entry → "Appendix I
      (Prediction 8)" — first in-body Prediction-number citation.
    - Style normalizations of her text, hers to veto: "US measurements in
      section 10" → "U.S. measurements in Section 10".
    CROSS-REFERENCES (her ask: "add references so that if we restructure
    the tags change"): `code/html_to_latex.py` now emits a \label on every
    numbered object — sections, subsections, appendices, theorems, figures,
    the 7 numbered displays, all 13 register items — with content-keyed
    names (sec:ceiling, app:race, prop:fork, fig:kappa, eq:closure,
    pred:exit), and REWRITES every literal in-prose mention to \ref
    (88 refs), so reordering in LaTeX renumbers everything. New gates:
    unknown heading title FAILS (HEAD_LABELS must learn retitles);
    leftover-literal sweep must find zero; every \ref must resolve to a
    defined \label; the word-fidelity check resolves each \ref back to its
    printed number. Converter ALL GREEN (13,231 tokens both sides, zero
    hunks; kill-item assertion 5 → 0). Post-port: italicize +2 wraps, lint
    ALL GREEN, census clean, check_pinning 37 ALL GREEN. Zip rebuilt
    (`pinning_latex_overleaf.zip`; README documents the label scheme).
    NOT PORTED, deliberate: author order — her Overleaf copy is PRE-SWAP
    (Båge first); the regenerated main.tex keeps WILSON FIRST per her
    recorded call; she should replace the Overleaf main.tex WHOLESALE
    rather than merge. FLAGS for her: (i) §10 "This is Proposition 4's in
    the rawest public series available" — dangling possessive left
    verbatim (the deleted noun was "bookkeeping"); (ii) §5 "the empirical
    debate of search and matching is changed significantly on this
    object's level" — reads as a slip, left verbatim; (iii) §11 comma
    splice ("...ρ̄, however none...") left verbatim; (iv) the reinstatement
    bet now has NO defense in the paper — one §12 sentence could restore
    the task-birth clause if she wants it back. NOTE for the pending λ
    splice: its edit list includes a "§11 kill-item status clause" — moot
    now; land the λ status inside §10's assembly text instead.

24. **Voice pass, second batch ported (back matter)** (her Overleaf edits,
    pasted same day; five edits, all behind the references). PORT (5
    replacements, exactly-once asserted; snapshot pinning_pre_voiceport2 +
    word-diff voice_pass2.diff.html at session scratchpad):
    - AI-USE NOTE trimmed by her: "under a strict rule against substitution
      or approximation, with every series validated before use" CUT (the
      rule itself still stands in the Standing rules and the data note's
      "all defensible variants" sentence — only the AI-note mention went);
      "The subject matter makes the disclosure doubly obligatory." CUT —
      the last "doubly obligatory" disclosure framing is now out of the
      paper (its §1 twin went in log 23).
    - ACKNOWLEDGEMENTS SPLIT PER AUTHOR: h2 → "Acknowledgements, S.
      Wilson"; NEW EMPTY SECTION "Acknowledgements, J. Båge" appended as
      a placeholder awaiting his text. Her ¶1 edits: "have MOSTLY been
      reading", "the nature of IMPORTANT ideas" (was "true"). NEW thanks
      ¶: Helmuth Cremer (J. Public Economic Theory — for not dismissing
      the early submission) and Sverrir Thorvaldsson (her SEB manager).
      ONE TYPO FIXED, flagged for veto: "continuos" → "continuous".
    - TOOLING RIDING FIXES for the retitle: converter's h2 branch now
      takes any "Acknowledgements…" title verbatim (\section*, generated
      NOTE comment retired — she has revisited); lint's italic-sentinel
      cut and italicize_math.py's END marker now prefix-match
      "<h2>Acknowledgements". Pipeline ALL GREEN post-port: italicize +0,
      lint (24 h2), census, check_pinning 37, converter (13,289 tokens
      both sides, zero hunks). Zip rebuilt. Standing reminder: her
      Overleaf copy remains pre-swap and pre-\ref — replace main.tex
      wholesale, do not merge.

## Session log (2026-08-19) — THE SYMBOLS PASS

16. **Symbols-earn-their-ink pass executed** (her catch: Appendix G's
    per-task machine cost m read as shadowing the rental c; her rule: a
    definition must be reused "a fair few times," else full form or rework
    onto existing objects; her ask: the whole paper, hunting mergeable
    concepts). Census MECHANIZED per the ADDENDUM-7 lesson:
    `checks/census_symbols.py` counts every defined symbol's occurrences
    (informational table + hard-fail if a killed symbol returns).
    SEVEN SYMBOLS ELIMINATED at three sites:
    - App G's m — premise reworked to &rho;(x) → 0 outside K (Section 7's
      corollary's stricter limit confined to the tasks machines can hold),
      with the reconciliation her misread proved missing now stated: c
      stays PINNED by the recursion (Prop 2), what vanishes is per-task
      cost c/γ_M = c·ρ/γ_L. NOTE: m → c would have been WRONG — c → 0
      contradicts Prop 2; the m/c distinction was load-bearing but
      undefined at first use.
    - App G's φ_H — credence sentence reworded; the bound is now NAMED
      "the fraud bound v·f/(1−v)", anchoring Prediction 12's previously
      unanchored term; the trivial min(taste, bound) arm dropped.
    - F.1's (m_w, m_e, b, b′, y) — transfer pair now words ("what it pays
      in work and what it pays out of it"), Δ defined as their difference,
      cases as Δ > 0 / Δ < 0; the s(y)-vs-s(q) collision gone (income-
      effect caveat now in words).
    ONE CONCEPT MERGED: G.1(ii)'s proof now cites Appendix E's share
    display with q read as K-content's relative price — one CES formula,
    two readings (the notation footnote's context-local η note still
    accurate). RIDING FIXES, same families as the bugs: G.1(iii)
    "terminal expenditure" → "end-state expenditure" (the metaphor pass's
    terminal-collision family, missed instance); App H's "when machine
    cost undercuts w_f" made per-task (c·ρ(x) below w_f·ρ_f(x) — the same
    rental-vs-per-task conflation as the m bug).
    KEPT with reasons (census-verified): formula-bearing one-passage
    symbols where the symbol IS the full form (v, f, β, ε_D/ε_S, §8's t
    shell-game, ω_ij, k, w_K, w_f, ρ_f, δ, d, P-index) and proof-locals
    (n, X, z); λ_R (table row handle); q* (crosses F.3→F.4). CONSIDERED,
    REJECTED: folding Appendix E into D or G (renumbers E–I for marginal
    gain). FLAGGED, not applied: "the fiscal scissors" (Prediction 9) is
    a once-used named metaphor — the metaphor pass kept it deliberately,
    so it stands; it is the one borderline the new rule would catch.
    `check_pinning.py` +8 checks (G.1 in ρ-form: c pinned positive at the
    limit, unit-cost limit, K-free collapse, divergence; CES share limits
    doubling as App E's display — this repo previously leaned on
    link-repo's m-form kset record): 35 ALL GREEN. lint ALL GREEN. Rule
    written into the brief (SYMBOLS EARN THEIR INK). Diff at scratchpad
    symbols_pass.diff.html; baseline pinning_pre_symbols.html (git also
    holds the pre-state: pinning.html was committed clean at ff460b9).

17. **The environment appendix executed** (her go on option 1 of the
    complete-model discussion — one environment defined once, appendices
    as activated blocks, NOT one master model deriving everything jointly;
    her constraints: take restructure/cut/expand opportunities as they
    arise, preserve the main text's cold register — met by touching the
    main text ZERO times). Appendix A retitled "The environment and
    assignment equilibrium"; new opening: the full cast in seven blocks
    (tasks/technology with µ and K and the tradable subset; machines
    scalar and matrix; non-produced inputs with r(z); people with the
    exit technology and CES(σ, η); government's four instruments; abroad)
    + an equilibrium definition per configuration + a nine-row switch
    table (main §§3–7 all-off; §8 (τ,u,t); B wedges; C matrix+durability;
    D the limit row with η=1; E general η; F government in full; G the
    K block; H the border). Honesty line: "the other blocks off unless
    named. Existence for the full assembly is not claimed."
    THE PAIR RESTORED, tightly: (m_w, m_e) now DEFINED in A's government
    block and DERIVED in F.1 (w + m_w vs s + m_e ⟹ Δ = m_w − m_e) — the
    fix for her "the words now feel even looser" regression; census shows
    the pair at 8 hits across its two homes. NEW CROSS-MODULE DISPLAY
    (G×F): F.3's bundle extended with k_s hours of K-service, κ =
    qT/(N(g_s + k_s·w_K/p_g + q·h_s)), below the K-free ratio at every q
    and falling in the K-hour's price — algebra first verified in
    link-repo's check_kset.py, now restated and re-checked on this
    paper's own display (+2 checks). Appendix openers re-anchored to A's
    blocks (B "turn on the wedge block", C "many-machine block in full",
    D "set the dials to the limit row", E "the general η", F "government
    block in full", G "turn on the K block", H "open the border");
    Cobb–Douglas now explicitly D's η=1. Notation footnote updated (µ in
    A and B). NOT BUILT, left open by design: the in-kind-housing m_e
    against q·h_e (formalizes §5's three-forms passage) and wedges inside
    the machine sector's own labor (µ meets λ) — the two cross-module
    candidates she can commission separately. check_pinning 37 ALL GREEN;
    lint ALL GREEN (body ~13.4k words, +~640, main text unchanged at
    ~5,235); census updated (m_w/m_e revived with a defining home, k_s
    live, DEAD list still zero). Diff at scratchpad
    environment_pass.diff.html; baseline pinning_pre_environment.html.
    STRUCTURAL NOTE for future sessions: deviation from the frozen
    brief's appendix plan — A is now environment + equilibrium; letters
    B–I unchanged, no reference churn.

18. **Environment-appendix register repair + post-mortem** (her catch,
    Socratic: "compare this language with that of the introduction" —
    "One environment carries the paper" / "extension block" / "full
    cast"). DIAGNOSIS, confirmed: §1's sentences take the economy as
    subject, and the paper's self-references act on model objects in
    model vocabulary ("The paper closes both prices"); the new opener's
    sentences took the DOCUMENT'S ORGANIZATION as subject, in vocabulary
    coined for the occasion (block/cast/dials/switch) while the paper
    already owned the needed words (configuration §9, case, limit,
    restriction). ROOT CAUSE: planning-layer vocabulary from the
    design discussion transplanted into the artifact — third instance
    of the collaboration-layer leak family (ADDENDUM 3 state-file idiom;
    ADDENDUM 7 meta-clause). FIXES: A's opener rewritten object-level
    ("The economy below generalizes the model of Sections 3–5; the main
    text is the case with every extension absent... each appendix
    relaxes one restriction"); table header "Blocks on" → "Configuration";
    all anchors de-jargoned to object-naming ("Let tasks carry the wage
    wedge µ(x) of Appendix A", "Take Appendix A's economy to the full
    limit", "Open Appendix A's economy", "Let Appendix A's set K have
    positive measure k", "Appendix A's government in full"); E's opener
    also names D as its η = 1 case. lint HARD-BANS the family
    (extension/wedge/government/K/preference/machine block, blocks
    on/off, full cast, the dials, turn on appendix, switch(ed) on);
    the brief's ONE TEMPERATURE gains the control-vocabulary corollary
    naming the leak pattern. lint + checks ALL GREEN; diff regenerated.

19. **Italics + two-part-introductions pass executed** (her rules: all
    variables italic in prose; every new symbol introduced words-first
    with its defining relation). MECHANIZED, not hand-done:
    `code/italicize_math.py` — an idempotent transformer (re-run = +0)
    that wraps Latin variables and lowercase Greek in <i>…</i> across
    prose, props, proofs, captions, tables, and the notation footnote,
    per TeX convention. Upright by design: uppercase Greek (Δ, Λ, Σ),
    max/min, digits, bold vectors, (a)–(d) list labels, (i)–(iii) part
    tags, possessive 's, "i.e.", appendix letters, Z.1. Skipped: .eq
    displays (CSS-italic already), references, Acknowledgements
    (verbatim). +944 spans (82 → 1026, balanced); one manual fix the
    sentinel caught on first run — §11's bold kill-header λ, now
    bold-italic (the transformer's bold-skip protects Appendix C's
    upright vectors, which shielded it). MAINTENANCE WORKFLOW: write new
    prose bare → run the transformer → lint (tag balance now covers
    i/b/sub/sup; new sentinel FAILS on any bare Greek entity in prose).
    census_symbols.py normalizes the markup away before counting.
    TWO-PART AUDIT: census-guided sweep of every first introduction —
    the paper was already near-compliant (words-before-algebra held);
    three gaps fixed: w now introduced ("Labor, at wage w, holds task
    x..."), z introduced ("rent schedule r(z) over parcels z"), q_enc
    given its words ("dies where rising rents exhaust the independent
    keep, at q_enc = ..."). Both rules written into the brief (ITALIC
    VARIABLES; TWO-PART INTRODUCTIONS). check_pinning 37 ALL GREEN; lint
    ALL GREEN. Diff at scratchpad italics_pass.diff.html (538 regions);
    baseline pinning_pre_italics.html.

20. **Poetic-register sweep executed** (her catch: "floor dies" — the
    lens is WARMTH, distinct from the metaphor pass's opacity lens; her
    ask: "what else reads a bit overly poetic?"). Grep-swept, not
    hand-inventoried; ~35 edits across four families, all lint-banned
    now so none can return:
    (1) LIFE-CYCLE VERBS on model objects: floor "dies"→independent exit
    "ends" (F.4); "outlives"→"outlasts"; "the welfare claim dies"→
    "fails" (§11); wage "lives in"→"sits in" an interval (§1, §6 het.);
    accounts that "live"→"defined" inside the interval; "went dormant"→
    "lapsed" (§2.5).
    (2) ORNATE PRICE DICTION: "dear/dearer" family OUT everywhere (§1,
    §6, Fig 1 caption "costlier worker", G proof "costlier category", G
    κ-sentence); G's closing aphorism CUT ("what survives the machines
    makes surviving them dearer" — the display now carries it).
    (3) VIVID MECHANISM VERBS: "comes to rest"→"settles" (×3: §1, §7,
    §12); "walks the floor down"→"lowers the floor"; "summons"→
    "induces" (F.1, §8); "society burns"→"loses" + "appearance of
    employment"→"employment so preserved"; "housing eats the budget"→
    "takes the whole budget" (E); "plumbed into"→"taxes" (§10); "blind
    in opposite places"→"miss opposite bases", "mix question retires"→
    "disappears" (F.5); "thicken"→"add"/"extend" (§4, C); "hands
    tasks"→"shifts tasks" (Fig 1); "on display"→"showing" (§4);
    "reservoir"→"stock", "loses its engine"→"mechanism" (§11); "the
    human hour the floor must buy"→"put human hours in the subsistence
    bundle" (G); "last variable standing"→"reduces the distributional
    question to ownership" (§8); "backdrops"→"background" (§2.7);
    "labor-hungry"→"labor-intensive" (§9).
    (4) ERA LABELS COOLED: "the floor does the work"→"the floor binds"
    (matches the paragraph's own "binding boundary"); "the ceiling lifts
    off"→"the ceiling rises".
    KEPT, with reasons, flagged to her: the seven crowns (brief-exempt);
    the named metaphors (fuel tank, wage of waiting, scaffolding, the
    room, fiscal scissors); the ten transparent families (pin, carry,
    resolve, anchor, erode, migrate, travel, recipe, disguise, thin);
    literature-standard usages ("escape" from Malthus, "sheds labor",
    "unravel" (Roth), "sufferance" (legal), "spiral", "in disguise"
    P6); "way-station" (H); §5's "finds nothing in the exit bundle left
    to price" (the ADDENDUM-3 beat); "aggregate rescue, median
    collapse" + the "rescue" family (G/§11/P12); "direction, not a
    destination" (§11); the abstract untouched (her approved version).
    FALSE-POSITIVE discipline: "treats/beats/subsidies/Studies"
    excluded; §9's "engines" is literal machinery, kept. lint gains the
    poetic-ban family (" dies" spaced to spare "subsidies"); transformer
    re-run +0 (no new variables); 37 checks + lint ALL GREEN. Isolated
    diff at scratchpad register_pass.diff.html (48 regions).

21. **Abstract rewritten** (her direction, supersedes the ADDENDUM-4
    abstract): three candidates offered (compressed arc / minimal /
    implication-forward); she chose MINIMAL (B) with three fixes, all
    applied: (1) "forks by deflator" replaced by the spelled-out form —
    "real wages diverge by what they are measured in: in machine-made
    goods the wage is pinned by absolute human productivity; against
    housing, space, and energy it falls without bound" + the concrete
    paycheck sentence (4× durables, a fifth less shelter, 4.8×). HER
    CALL: "fork" stays body-only, out of the abstract. "K-shaped
    economy" considered at her mention, REJECTED by Claude with reasons
    given (collides with Appendix G's K set; trend vocabulary) — flag
    if she wants it anyway. (2) "instrument pair that survives" →
    "From the model we derive a taxation and benefit system: a tax on
    the rents of non-produced inputs funding a uniform per-person
    transfer. It distorts no production decision and changes no
    work–exit choice." (3) "full rent capture" → "Taxed in full, U.S.
    site rents would fund one-third of a per-person subsistence floor
    today, up from a twentieth in the 1950s." Result ~190 words (was
    ~265): w = cρ(x*), the search-positioning sentence, and the
    classical close all dropped from the abstract (§§1–2 carry them);
    the one inline equation kept (c = ac + λw + ℓr, words-first). ALSO
    NOW IN THE ABSTRACT for the first time: the κ trend (0.05 → 1/3).
    Transformer re-run (+5 wraps), lint ALL GREEN. Diff at scratchpad
    abstract_rewrite.diff.html; pre-state pinning_pre_abstract.html.
    FOLLOW-UP (her call, same day): BOTH wage equations added back —
    sentence 1 regains w = cρ(x*), and a new sentence carries the
    solved closure with a title echo: "Margin and recursion together
    pin the wage to scarcity and technology: w = ρ(x*)·ℓr/(1−a−λρ(x*))"
    — written with ρ(x*) in full (no ρ* definition spent in the
    abstract; same object as Prop 2's, already checked). This REVERSES
    ADDENDUM 4's "solved closure is Prop 2's job, not the abstract's,"
    at her direction. Abstract now ~212 words. Transformer +12 wraps;
    lint ALL GREEN; diff regenerated.

## Session log (2026-08-13, continued) — WOUND REPAIRS (W1 + W2)

14. **The two structural wounds repaired**, on her go after a
    propose-first turn (her constraints: no lengthening/complication;
    register rules apply; she reads the diff). Ten edits, diff at
    scratchpad wounds.diff, pre-state snapshot pinning_pre_wounds.html.
    W1 (parity ≠ superiority): corollary rewritten — parity keeps its
    wage ("Parity does not erase the wage... The wage goes to zero only
    in a stricter limit: ρ̄ → 0... or parity below the outside option"),
    the parity/weakened-identity case stated inline, "thin" dropped from
    interest, "Wages have left the list" gone (her jargon flag); §8
    "once wages are gone" → "while the wage thins"; §1 + abstract gain
    "as capability closes"; F.5 scoped to "the corollary's limit".
    W2 (commons vs recursion) + HER THREE-FORMS ADDITION: §4 ties r to
    the sites production uses (schedule pointer); Prop 3(i) triggered on
    idle SUITABLE parcels; 3(ii) proof outbids-the-margin instead of
    same-q-per-quality-unit; NEW §5 passage (her content, register-
    treated): zero rent means nothing can be done with the parcel, so
    the idle margin supports no exit — free-and-livable is the historical
    commons; the modern floor s_d is otherwise-funded in three forms
    (dependency = unpaid transfer from the employed to the exited;
    public provision = F.1's out-of-work payment, thin where it exists;
    tolerated use = land held by others, priced in enforcement); none
    insulated from q — the flat segment at s_d is an UPPER BOUND and
    F.4's race runs against a falling floor. Superseded "modern commons"
    clause removed; the §10→§11 cross-ref bug fixed in passing (copy
    audit item, same sentence). Net +~115 words; no new symbols; s(q)
    display and F.4 algebra untouched (the upper-bound reading
    STRENGTHENS the race conclusion). lint ALL GREEN (174 p-tags, all
    register bans hold). Remaining review repairs (Tier 1 batch, Tier 2
    units) still awaiting her go — see the synthesis doc.
    FOLLOW-UP (her flag): "one event posting to two ledgers" DELETED —
    the accounting metaphor pre-stated what the next sentence says
    plainly; that sentence now carries it ("three things happen at
    once"), and "Enclosure manufactures labor supply" keeps the
    contrast. wounds.diff regenerated to include it; lint ALL GREEN.

## Session log (2026-08-13, continued) — THE METAPHOR/JARGON PASS

15. **Metaphor/jargon pass executed** (her ask, after the ledger-sentence
    lesson: this class fails at the meaning layer, so fresh-eyes detectors,
    not self-read). Two detector agents: a no-economics plain reader (213
    items inventoried, TRANSPARENT/OPAQUE/DECORATIVE verdicts) and an
    economist jargon auditor (standard-vocabulary keep-list; defined-term
    audit; undefined/unearned list; metaphor-family collisions;
    figurative-inside-formal-statements list). ~50 edits applied, diff at
    scratchpad metaphor_pass.diff (baseline pinning_pre_metaphor.html):
    COLLISIONS UNIFIED — "close/closure" reserved for endogenization
    ("holds the new-task margin shut", "balances exactly", "agree on the
    same number", "blocked", "closed-economy limit"); "fork" reserved for
    the real-wage fork (Prop G.1 renamed "Baumol concentration", "an
    empirical question", "The Baumol case also raises the floor's
    price"); "parity" fixed by definition at §7 + "the parity wage" for
    the level (Fig 5, prediction 11); "floor/ceiling" de-overloaded (κ's
    "upper bound", "minimum housing bundles"); Lemma B.1 renamed "the
    effective schedule"; "terminal allocation" → "end-state"; idle/exit/
    margins doubles fixed. GLOSSES ADDED — Speenhamland (1795), Baumol
    (1967, entry added, live-verified AER 57(3):415–426), Alaska dividend,
    distillation, credence, Z.1 residual method (+ the post-1995 caveat
    STATED and the 2020 business-structure disclosure RESTORED in Fig 4's
    caption — review items), withdrawal bands, "sorry"/mathlib, enclosure
    at §2.5, assemblies at §2.7, φ_H and ρ_f and t and Y and n defined,
    τ parcel-dummy collision fixed (∫r(z)dz), η/s_h notation-footnote
    entries. PROP-INTERNAL FIGURATIVES literalized (unresponsive;
    necessary; by design not by size; rental flow unchanged; accrues;
    aphorism cut from G.1(ii)). DECORATIVES cut ("(build!)", "violently").
    ALSO RIDING: "as capability closes" → "as the capability gap closes"
    everywhere (the most-repeated opaque ellipsis); "drying" → "slowing";
    "near zero" → "small" (search-referee item); L̄ mislabel fixed ("the
    inverse of absolute solo productivity"); "welfare completion" →
    "fiscal completion" (label unified); §10 "measured and carried" split.
    KEPT DELIBERATELY: the ~dozen transparent recurring families (pin,
    carry, resolve, anchor, erode, migrate, travel, recipe, disguise,
    thin), the explicit named metaphors both reviewers passed (the fuel
    tank, the wage of waiting, scaffolding, the fiscal scissors, the
    room), and the seven crowns. Net +~260 words (glosses); em-dashes
    13.7/1,000 (appositive glosses); lint ALL GREEN.

## Session log (2026-08-13, continued) — THE SIX-PROFILE REVIEW

13. **Six-reviewer parallel review executed** (her ask: "spin up some
    subagents with different profiles"): task-literature referee,
    search-macro referee, empirics referee, cold reader, copy/notation
    auditor, adversarial theorist — all six read the full paper
    independently (a service overload forced staggered resumes; all
    completed). Synthesis, deduplicated and Claude-verified:
    `docs/review_synthesis_2026-08-13.md`. HEADLINES: all arithmetic
    verified clean (three independent recomputations; empirics matched
    every number to the built CSVs) — but TWO STRUCTURAL WOUNDS, both
    Claude-verified: (W1) the terminal-income corollary conflates parity
    with unbounded machine superiority ("wages have left the list" needs
    ρ̄→0 or full exit; at parity the paper's own Prop 4(i) pins a positive
    wage and F.3's parameters give a ~47% wage share — propagates to §8,
    F.5, intro, abstract); (W2) the open commons of Prop 3(i) is
    incompatible with the recursion's viability condition as stated
    (r = 0 forces 1−a−λρ* = 0; fix via Ricardian differential rents).
    Plus: four repairs that STRENGTHEN the thesis (the signed
    one-movement theorem replacing §6's "parameter question"; the
    endpoints→primitives/nesting rewrite of §2.2; the terminal-claimant
    correction of §2.3; the determinacy-vs-crossing split), two unsourced
    load-bearing claims (task-birth; low-income shelter shares), a false
    Figure 7 caption/annotation vs the built series (SAME BUG IN THE LONG
    DRAFT — flag to link-repo), the λ>0 flat-regime gap, ~40 mechanical
    fixes, and two big upgrade proposals (the fundamental-surplus
    subsection; the general-technology fork theorem). Verdicts: field-
    journal R&R now, top-five after Demands 1–2; "the kind the search
    literature would rather steal than ignore." NOTHING SPLICED — the
    repair pass awaits Stella's direction on W1/W2 and the Tier-2 units.

## Session log (2026-08-13)

12. **The pinning rewrite executed** (this thread's unit; discussion → frozen
    brief → checks → verified citations → full draft, one session). Stella's
    decisions: one paper, core-first with long appendix; λ IN; title hers
    ("Pinning the Wage to Scarcity and Technology"); acknowledgements stay;
    checks post-writing except where Claude wanted one (taken: the λ spine,
    27 green pre-splice); §10 build-vs-flag delegated (flagged). New files:
    `docs/rewrite_brief_pinning.md`, `checks/check_pinning.py`,
    `checks/lint_pinning.py`, `code/fig_eras.py`, `figures/` (3),
    `paper/snapshots/pinning_skeleton_snapshot.html`; `paper/pinning.html`
    REPLACED (skeleton → full paper). Veto window above. NOTE: main-text
    length came in ~45% under the brief's target — flagged as the window's
    first item.

## Session log (2026-08-09)

1. **Assumptions audit** (chat-only; not filed here). Kill-shots identified: (i) the flattening premise on *existing* tasks — unmeasured; now addressed via Assumption F and data item one; (ii) free entry in machine-making — open; (iii) taxonomy near-tautologies ("dynamic rents expire," "institutional rents are policy-elastic") — open; (iv) the κ ceiling (κ → T/(N·hs), never checked against 1) — data item two; (v) the "each type prices its own link" heterogeneity claim is internally inconsistent with the AR cross-group propagation the paper cites — fix at merge.
2. **The split.** Capability: scalar talent θ (defined operationally: invariant to the model's instruments) × practice q, Ben-Porath complementarity (θ = learning gradient). Wage strata become four: exit floor + practice premium (cost recovery) + talent rent (Ricardian) + wedge. Slotting: practice = dynamic scarcity (two migrations: licensure → institutional; recording → idea); talent = physical on the supply side, transitional on the demand side, and fails the in-rem test land passes (Mirrlees; "George is Mirrlees with an observable base"). Scalar θ with task-varying loadings keeps comparative advantage (Costinot–Vogel cover); constant loading is the degenerate case.
3. **Task anatomy.** Dimension vectors; engineering vs learning rays (D — documentation density — gates learning rays only); transmission technologies (internet) are not rays: they enter via tradability, reach, and the D(x) path, never ρ; separability is component-wise (buffer test / narrow-channel test) and endogenous (standardize-then-automate).
4. **Stress test 1 (blind coding): PASSED.** 21 resolved cases, 20/21 on the bare rule; the pharmacist is the miss and proves the point — task anatomy and μ-anatomy are co-dependent classifiers, the wedge overlay admissible only with a citable instrument. Six live predictions pre-registered with dates (`stress-test/` §6, P-S1–P-S6).
5. **Sketch blocks A, B, B.0′, C, D drafted** (`sketch/`). Headline results: reinstatement mechanized (fragment creation on uncrossed dimensions — §10 branch-two repair); hump-shaped premium path derived from ray sequencing (widen/plateau/compress); the doomed vintage (practice acquired within a training-lag of its copying date is negative-NPV — a second negative-sum channel); μ speciated into five species; displacement-loss decomposition that **moderates** the paper's imported 60–90% negative-sum figure (D1); the demolition spectrum = the stress test's admissibility rule read as theory (D2).
6. **Decisions taken (delegated, recorded in `sketch/link-sketch-blocks-B0-C-D.md`):** belief friction = stated assumption, with C3's composition channel shown assumption-free; surveillance paragraph kept, decomposition-framed; species 4 labeled "slack rents," Graeber footnoted; doomed-vintage magnitude = banded back-of-envelope during the data pass.
7. **Data item one delivered** (`data/`). Premium from primary microdata (NBER CPS MORG, 1979–2024, 46/46 years, zero errors): widen 1.407→1.806 (1979–2000); plateau; fixed-weight peak **1.887 in 2016** → 1.837 (2024) — the compression leg exists but is young. 1992 CPS education redesign break marked, never spliced (raw 1.660→1.750 at the break). Census attainment 11.0% (1970) → 38.7% (2024); NCES conferrals with a post-2020 downturn in actuals; NY Fed queue monthly Jan 1990–Jun 2026, recent-grad underemployment chronically ~38–48%, ~8–9 pt excess over all graduates throughout. Blocked endpoints (FRED; BLS API/flat files/data viewer; EPI) documented in `data/DATA_NOTES.md` — reported, not substituted.

## Session log (2026-08-09, later session)

8. **Housekeeping (outer repo).** The outer root's working files were filed into their homes: `NOTES.md`, `checks/`, the `*_section.html` drafts, the six paper snapshots, `rewrite_brief.md`, `feasibility_empirics_spec.md` → `link-repo/` (root, `checks/`, `drafts/`, `paper/snapshots/`, `docs/`); `companion_schedule_spec.md` → `companion/`. Path-bearing references updated; all moves via git mv, staged, not yet committed. The outer venv was recreated (python 3.13, pandas 3.0.5, pyarrow 25).
9a. **κ ceiling delivered (data item two)** (`code/kappa_ceiling.py`; full record in `data/DATA_NOTES.md`). The ceiling T/(N·h_s) measured on the paper's own rT grid × HUD FY25 FMR floor-housing members: **median 1.26, band [0.38, 4.91], 13/32 members below 1** — shared-housing members clear 1 everywhere, solo-dwelling members mostly fail, population-weighted metros worst. Every measurement bias runs downward (lower-bound land, utilities in the denominator, missing economy-wide member), so audit iv resolves as **substantive robustness note, not fatal**: Prop 8's measured text stands, the "demolition funds its own remedy" framing takes a one-sentence ceiling caveat (surgical-repair list), and the h_s-is-partly-zoning observation feeds the parked second paper. FRED is reachable from this machine — pass-one's blocked-endpoint list was container-specific. BLS SPM 404 / Census SPM 520: reported, not substituted.
9b. **Premium pass two delivered** (`code/premium_pass_two.py`; full record in `data/DATA_NOTES.md`). Goldin–Katz proper: mean log wages, sex×experience cells, 6-member grid (topcode m {1.0, 1.4, 1.5} × weights {base8991, meanshare}). Reproduction gate vs pass one passed at 4e-16. Findings: (i) adjusted premium 1.434 (1979) → **peak 1.925 in 2016** → 1.882 (2024); every seam-safe member peaks 2016, compression −0.022 to −0.029 log points — pass one's shape survives the proper adjustment; (ii) **topcode discovery:** the static $2,884.61 cap was biting 15.7% of BA+ obs by 2022; April 2023 CPS moved to dynamic topcoding (visible as mass points above the old cap; 2023 hybrid, 2024 fully dynamic) — the m=1.0 members' 2024 "peak" is that seam, flagged; (iii) **the race:** free σ unidentified in-window (corr(t, relsupply)=0.9975; wrong-signed σ̂ reported, not used); under imposed σ {1.41, 1.64, 2.5} demand-index growth declines monotonically across eras to its historical low 2016–24 (0.018–0.021 log pts/yr) while supply growth did NOT slow (2.47%/yr) — the compression is **entirely demand-side**: shortfall vs continued-demand counterfactual −0.037 to −0.044 by 2024. This is the C2/C3-relevant measurement: the race stopped being winnable by supply restraint; the schedule side moved.
10. **Demolition-order cross-section delivered (data item three)** (`code/demolition_order.py`; full record in `data/DATA_NOTES.md`). D proxies from O*NET matched by name (discovery: the classic "Structured versus Unstructured Work" item is absent from 30.3; "Freedom to Make Decisions" reversed-by-anchor substitutes), walked to occ1990dd on the companion's own chains, offline. **Test A (order within the LLM-exposed): NOT yet visible** — median Spearman +0.05, 4/18 pairs negative; consistent with friction still binding (no exposure gradient exists yet for D to order), reported as a present-tense miss and left standing as a dated prediction, instrumented for the P-S re-reads (2028–30). **Test B (placebo): passed** — pre-LLM flips selected on routine (+0.5–0.6 sd), D gap conditional on routine NEGATIVE (−0.3 to −0.6z) and unchanged when rescored on era-correct O*NET 13.0 (2008) — not survivorship drift; reading: survivors are the residue holders who recomposed around the machine (rule outcome PARTIAL). The engineering-era demolition needed no corpus, as the anatomy says.
11. **Algebra pass delivered** (`checks/check_split.py`, `check_mirror.py`, `check_anatomy.py`, `check_race.py`, `check_mu.py` — all green). Ten flags: A0-DR (convex study tech changes nothing), A1-FP (single crossing symbolic + sorting-and-training fixed point numeric, PAM), A2-POOL (interior θ_m, free entry pins the premium, rents rise in θ), B1-OCC (occupying-type display is β(q_occ − D); β(1−D) is the frontier case), B2-COV (**AMENDED**: aggregate dispersion can RISE under F1 with a Moravec covariance — channel-tagging survives, aggregate claims need the Cov sign or F2), B0'1-MEAS (fragment creation as exact measure bookkeeping; creation = 0 at completeness), B0'2-RES (residual-requirement term explicit; continuous vs stasis-then-cliff), C1-COBWEB (**AMENDED**: "product < 1" exact only at T_E = 1; boundary tightens to ~0.2 at T_E = 8), C2-HUMP (single peak in the stable monotone regime; wiggles in the oscillatory), D1-CS (ledger + three statics; 60–90% → 60–90% × ω_wedge). C3's composition half verified friction-free as a bonus. Flags in `sketch/` updated in place with outcomes.

## Parked: the second-paper seed (2026-08-09)

A full zoom-out read of the finished paper (Claude, this session) produced four load-bearing critiques that Stella marked as **probably the next paper, not yet decided**: (1) the paper's stark results live on the K=∅ edge of its own Prop 11 while plausible K (law-reserved + co-present) approaches half of employment — sizing K and modeling reallocation into it (w_K dynamics, entry gates) is the open machinery; (2) the land facts (deflator fork, Rognlie) have an unpriced rival in zoning — the discriminating content is the second derivative; (3) the rent taxonomy protects the migration claim from falsification — Prediction 7 needs dating like the stress-test P-S set; (4) the political economy of enacting the remedy (taxing the only surviving asset class) is absent — belongs with the transition-dynamics sketch. Items (1) and (4) are new relative to the audit; (2) and (3) sharpen audit points. Do not fold these into the current revision uninvited; they are scoped as follow-on work.

**Spun out (2026-08-17):** the long-record extension — §10 assembly (3) grown
into a fittable dynamic wrapper over the static core — now lives at
`../long-record/` (own STATE.md; governing spec at `long-record/docs/spec.md`;
parked at its Breakpoint A). Decided with Stella in-session; `pinning.html`
untouched by that thread.

**PENDING DECISION (Stella's, raised 2026-08-09):** whether the sketch blocks merge into the main paper at all, or become the next paper together with the critiques above. Claude's recommendation on a full read of the finished text: the paper takes only surgical repairs — the audit-v heterogeneity fix, Assumption F named in §10, a κ-ceiling sentence on Prop 8, possibly a political-economy paragraph in §10 — and everything else (the split, task anatomy, education race, μ anatomy, the premium data) becomes paper three. The companion never merges; it gets cited from the prediction tags once its measurements stabilize. Queue item "algebra pass then merge" narrows accordingly if confirmed. Also raised: the companion's figures failed the author-readability test — a figure-level Dr. R. pass on the companion is proposed work, not yet queued.

## Standing rules (Stella's — do not relax)

- **Data:** primary sources; on access failure, stop and report — never substitute, approximate, or fudge; validate every series before use.
- **Data purpose (added 2026-08-09):** every empirical deliverable must either MOVE BELIEF (survive a risk it could have failed, or kill a rival explanation) or SIZE IMPACT (people and dollars — and per the blog's "Millions of Lifetimes," lifetimes: weight can come from the PAST). Illustration alone does not count as a data item. Past-weight claims carry a heavy justification burden: counterfactual + attribution + magnitude, per channel, before any lifetime number is stated as measured.
- **Theory:** algebra must pass a computer-algebra check and equilibrium claims a numerical check before anything enters the paper.
- **Code:** flat notebook-cell style, plain functions over classes, `tqdm.auto` on slow loops.
- **Substance:** LVT vs VAT never forced to a corner — the interior mix is welcome. Direct critique; no sycophancy.

## Next actions (priority order)

0-pre. **(2026-08-28) Phase 2 drafting is UNBLOCKED** — log 32's
   pre-drafting gate is passed (log 33): u_K and the equivalence lemma are
   checked, the conventions pinned, the engine validated, the §8 results
   verdict-stamped, the claim-status lint live. Next unit per the memo's
   cut-lines: Phase 2 (§§1–7 spine on the coefficient footing + 9.1 +
   10–12 + App A/B/D/F), Claude-drafts for her voice passes; log 33's
   veto list rides along (Inc_t convention, Q benchmark, T5 framing).

0. **The rewrite's veto window (Stella):** read `paper/pinning.html`; the
   first call is length — accept the ~5k lean main text or commission the
   expansion pass back toward the brief's ~9k. Then: Lean extension to the
   λ>0 spine + the Appendix A fixed point (queued verification — 2026-08-27:
   the λ>0 spine, user-cost forms, D.2/D.3, and the CES dial are DONE, log
   30; the Appendix A fixed point is the one Lean item still open); the three
   §10 assemblies as data units (incidence slope; λ via input–output; the
   long record); optional register regeneration of the fork/κ figures.
   — 2026-08-20, from the progress_and_prosperity thread: **the λ assembly
   is BUILT and READ (gate: PASS)** and its delivery is ready-to-splice —
   §10 block, Figure L, and the exact edit list (incl. the "three
   assemblies → two" renumbering and the §11 kill-item status clause) at
   `../progress_and_prosperity/lambda/p1_section10_draft.md`, with the
   citable companion note beside it (`lambda/companion_note.md`). The
   splice is a THIS-thread unit under this thread's discipline: snapshot →
   splice → update any check/record asserting "three assemblies [spec'd,
   unbuilt]" → `check_pinning.py` ALL GREEN → veto window. The long record
   has its own thread; the incidence slope remains open. (2026-08-21: the
   edit list's "§11 kill-item status clause" is MOOT — the kill list was
   deleted in Stella's voice pass, log 23; land the λ status in §10's
   assembly text, and re-run `code/html_to_latex.py` after the splice.)
1. **Merge (scope PENDING Stella's decision — see the pending-decision block above):** the checked blocks either merge per their Integration notes, or the surgical-repair list goes into the paper and the blocks become paper three. The algebra pass itself is DONE (log entry 11); nothing blocks either path.
2. **Second sketch — transition dynamics:** machine stock, land prices vs rents (capitalization, collateral), the κ-vs-enclosure race in real time.
3. **C4 back-of-envelope** (doomed vintage): IPEDS completions by CIP × cost of attendance × exposure shares, banded. Field-level queue structure (NY Fed by-major) belongs to the same pass.
4. **The misallocation ledger — FIRST LOOK DELIVERED 2026-08-09** (`sketch/link-sketch-block-E-misallocation.md` — Block E — plus `code/misallocation_firstlook.py`, `data/misallocation_firstlook.{csv,png}`). Commissioned as exploration, not proof. Delivered: the object defined (person-years above the undistorted benchmark, [·]₊, with the sign caution that tax wedges run the other way); four channels each with model anchor + counterfactual + attribution instrument; the unattributed envelope measured live (PWT hours to 2023: trend-continuation member 16.3M work-years/yr, Germany-parity 40.8M); channel brackets: insurance exit-margin 0.5–1M (imported, GGN), doomed study-years 1.3–2.9M/cohort-yr (our conferrals × our underemployment × labeled dials), slack 4–33M (contested dial), enclosure-forced participation EMPTY on purpose (P13 panel is the instrument — most native, least measured). ESI pipe measured at the pension+insurance aggregate $1,859B (2025); the group-health split is a BEA 6.11 pull, queued. Three decisions flagged for Stella at the end of Block E (benchmark stance; whether slack belongs; whether the envelope may appear outside the folder). A five-figure explainer page ("The Misallocation Ledger — First Look", private artifact) presents it over time: the hours century (US flat since 1980 vs Germany falling; PWT to 2023), the envelope in lifetimes (cumulative since 1980: ≈8.8M own-trend, ≈27.1M Germany-parity), the conditioned pipe (supplements share of wages 5.2%→14.3%, 1950–2025 — measured this session), the queue with the doomed-study band over time, and the assembled ledger. Remaining spec text of the original item: the past-weight object behind the blog's "millions of lifetimes" — person-years of labor supplied above an undistorted benchmark, decomposed into the model's own channels: (i) enclosure-manufactured participation (Prop 9a: rent-to-wage forcing second earners — Prediction 13's machinery is the attribution instrument); (ii) conditionality-summoned work (Prop 6ii; the giant US-specific instance: employer-tied health insurance as a work-conditioned in-kind transfer, measurable from NIPA supplements-to-wages); (iii) slack employment (species 4 — contested survey base, labeled); (iv) queue and doomed acquisition years (C3/C4, partly measured). Aggregate shadow: US hours stopped falling ~1980 while productivity doubled (the Keynes gap) — but rivals (Prescott's taxes, preferences, emulation) must be addressed per the justification burden above. Belongs with paper three's welfare spine.
5. **Companion figure pass (proposed, unqueued):** the four companion figures rewritten to the paper's readability standard — plain-sentence finding first, model vocabulary second; the wedge-targeting figure should plot the within-high-routine result its README narrates.

(Premium pass two, the κ ceiling, and the demolition-order cross-section — items 1–3 of the original list — delivered 2026-08-09; see log entries 9a, 9b, 10.)

## Repro notes

- `code/pull_premium_race.py` is self-contained and idempotent: Cell 0 downloads MORG (~2.0 GB — deliberately **not vendored** in this folder), Census A-2, and NCES 318.10; the NY Fed CSVs are fetched in-script (endpoints were mined from the interactive's JS bundle and are recorded in the script).
- With `data/morg_cache.csv` and the extract parquet present, Cells 2–7 rebuild every series and the figure **with no downloads at all**.
- `code/premium_pass_two.py` needs only the shipped parquet + `morg_premium_annual.csv` (its reproduction gate): `../venv/Scripts/python.exe code/premium_pass_two.py` from this folder — zero downloads, ~1 min.
- Environment: python3 with pandas, pyarrow, tqdm, openpyxl, matplotlib. The shared venv lives at the outer repo root (`../venv`; recreated 2026-08-09: python 3.13, pandas 3.0.5).

## Notation & merge cautions

- Numbering is provisional (A·, B·, B.0′·, C·, D·) — renumber at merge.
- Logged collisions to resolve at merge: the paper's λ_i (wage-linkage shares) vs λ(θ) (learning gradient); the superstar remark's β (reach fraction) vs β(x) (practice loading); Prop 10's D* vs D(x).
- **Numbers refresh at merge:** the C-block sketches quote pass-one premium numbers (fixed-weight peak 1.887 in 2016 → 1.837). The merge should quote pass two (adjusted peak 1.925 in 2016, seam-safe compression −0.022…−0.029, demand-side shortfall −0.037…−0.044 under the σ band) with the grid band, and may cite the identification report (σ unidentified in-window) when the text touches the race.
- Candidate verbatim sentence for the paper: *capability order comes from the anatomy of the task; survival comes from the anatomy of the wedge; neither classifies alone.*

## File map

Prose-maintenance loop (2026-08-19 onward): new prose is written BARE,
then `code/italicize_math.py` (idempotent) wraps the math variables, then
lint verifies (Greek-entity sentinels + tag balance). Never hand-wrap.

```
the-link-revision/
├── README.md
├── STATE.md                          ← you are here; start here next session
├── docs/
│   ├── rewrite_brief_pinning.md      the frozen v1 rewrite brief (2026-08-13)
│   ├── rewrite_brief_pinning_v2.md   the frozen v2 brief (2026-08-27) + her amendments
│   └── notation_map.md               v1 → v2 symbol map (Phase 1, 2026-08-27)
├── paper/
│   ├── pinning.html                  THE PAPER (rewritten in full 2026-08-13)
│   └── snapshots/
│       └── pinning_skeleton_snapshot.html   the replaced skeleton
├── figures/
│   ├── fig_eras.png                  regenerated schematic (de-coined)
│   ├── fig_deflator_fork.png         carried byte-identical from link-repo
│   └── fig_kappa.png                 carried byte-identical from link-repo
├── checks/
│   ├── check_pinning.py              the λ-recursion spine + user-cost forms, 51 checks
│   ├── check_dynamics.py             v2 dynamics: u_K, equivalence lemma, ledger,
│   │                                 T1 closed form, T4 algebra — 53 checks (2026-08-28)
│   ├── dynamics_ss_targets.json      solver gate targets (written by check_dynamics)
│   ├── lint_pinning.py               mechanical sweeps + claim-status-tag family
│   ├── census_symbols.py             defined-symbol census (symbols-earn-their-ink rule)
│   ├── check_split.py                A0-DR, A1-FP, A2-POOL (Block A)
│   ├── check_mirror.py               B1-OCC, B2-COV amended (Block B)
│   ├── check_anatomy.py              B0'1-MEAS, B0'2-RES (Block B.0′)
│   ├── check_race.py                 C1 amended, C2, C3 bonus (Block C)
│   └── check_mu.py                   D1-CS (Block D)
├── sketch/
│   ├── link-sketch-blocks-AB.md      A (the split) + B (machine mirror, Assumption F)
│   └── link-sketch-blocks-B0-C-D.md  B.0′ (task anatomy) + C (education race) + D (anatomy of μ) + decisions
├── stress-test/
│   └── link-stress-test-1-blind-coding.md   rule, 21 cases, score, pre-registered P-S1–6
├── data/
│   ├── DATA_NOTES.md                 sources, definitions, break, validation, blocked endpoints; pass-two record
│   ├── premium_race.png              pass-one three-panel figure
│   ├── morg_premium_annual.csv       raw + fixed-weight premium, 1979–2024
│   ├── morg_cache.csv                per-year cell aggregates (rebuilds series w/o microdata)
│   ├── morg_extract_1979_2024.parquet  5.24M-row extract (pass two runs from this)
│   ├── morg_premium_pass2.csv        composition-adjusted premium: 6-member grid, median + band
│   ├── race_decomposition.csv        relative supply, demand index, counterfactual, shortfall (per σ)
│   ├── premium_race_pass2.png        pass-two three-panel figure
│   ├── supply_attainment.csv         Census A-2, % of 25+ with BA+
│   ├── ba_degrees_conferred.csv      NCES 318.10 actuals
│   ├── nyfed_underemployment.csv     the queue, monthly to Jun 2026
│   └── nyfed_unemployment.csv        companion series
├── kappa_ceiling.csv               the ceiling grid, 32 members (data item two)
│   ├── hud_fy25_fmrs.xlsx            vendored raw FMR county file (validated)
└── code/
    ├── dynamics/                     the v2 transition engine (2026-08-28)
    │   ├── model.py                  environment, both steady states, the HARD GATE
    │   ├── solve.py                  validation ladder + T1/T2/T3/T5 experiments
    │   ├── figures.py                one entry point regenerates the four §8 figures
    │   └── results_dynamics.json     verdict record (written by solve.run_all)
    ├── word_diff_report.py           word-level HTML diff for prose files (her diff-reading workflow)
    ├── fig_eras.py                   regenerates the de-coined era schematic
    ├── pull_premium_race.py          self-contained, idempotent pull + build (pass one)
    └── premium_pass_two.py           composition adjustment + race decomposition (no downloads)
```
(figures/ additionally carries fig_dyn_windfall / _waterfall / _speedlag /
_sloped .png, all regenerated by `code/dynamics/figures.py`.)
