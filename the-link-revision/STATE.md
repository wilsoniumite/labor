# STATE — resume point for the next session

**Project:** revision of *The Link: Wages, Machines, and What Remains* (Stella Wilson, working draft Aug 2026; the blog post "A New-ish Theory of Economics" at wilsoniumite.com links the PDF — this folder sits next to the papers folder).
**Collaboration:** extended, multi-session; working format, sequencing, and drafting decisions delegated to Claude. Direct critique preferred over validation.
**State as of:** 2026-08-26.

## Where things stand

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
│   └── rewrite_brief_pinning.md      the frozen rewrite brief (2026-08-13)
├── paper/
│   ├── pinning.html                  THE PAPER (rewritten in full 2026-08-13)
│   └── snapshots/
│       └── pinning_skeleton_snapshot.html   the replaced skeleton
├── figures/
│   ├── fig_eras.png                  regenerated schematic (de-coined)
│   ├── fig_deflator_fork.png         carried byte-identical from link-repo
│   └── fig_kappa.png                 carried byte-identical from link-repo
├── checks/
│   ├── check_pinning.py              the λ-recursion spine + ρ-form G.1, 35 checks
│   ├── lint_pinning.py               mechanical sweeps over pinning.html
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
    ├── word_diff_report.py           word-level HTML diff for prose files (her diff-reading workflow)
    ├── fig_eras.py                   regenerates the de-coined era schematic
    ├── pull_premium_race.py          self-contained, idempotent pull + build (pass one)
    └── premium_pass_two.py           composition adjustment + race decomposition (no downloads)
```
