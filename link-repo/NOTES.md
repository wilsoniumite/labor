# The Link — working notes (canonical state file)

Read first, every session. This file carries decisions, notation, the queue,
and a per-session changelog between conversations. The repo is the source of
truth; Claude's working context resets between sessions.

## Session protocol

1. Start of session: upload this NOTES.md plus the files being touched (or the
   whole repo as a zip).
2. One work unit per session — roughly one item from the agreed improvement
   plan. Small repairs can piggyback.
3. Deliverables back each session: changed files, an updated NOTES.md, and a
   verify-list — the specific claims Stella checks as author before they
   count as done.
4. Verification rule: no proposition enters the draft before its check in
   `checks/` passes. Sympy for algebra, numeric instantiation for equilibrium
   claims, fully reproducible pipeline for empirics. Empirical rule inherited
   from the draft's data note: live public data only, no substitution or
   approximation; stop and report if a source is unreachable.
5. One live session per repo at a time. A session cut off mid-unit leaves
   this file behind reality — the next session's first move is to reconcile
   disk state against NOTES (file mtimes, undocumented paper changes) before
   any new work. (Added after the 2026-08-05 concurrent-session incident:
   two sessions each applied the conditionality splices; duplicates had to
   be removed.)

## Verify-list — 2026-08-09: the acknowledgements splice (current)

One unit (her "go, with the comma") plus the PDF answer. Snapshot:
`the_link_pre_ack_snapshot.html` at repo root. Her text spliced verbatim
as sent; two mechanical normalizations only.
- [ ] Veto window: the Acknowledgements block as the document's final
      section — placed AFTER the AI-use note, so the paper ends on her
      closing question; the agreed comma after "Although it might seem
      strange"; her pasted curly apostrophes normalized to straight
      (house typography — the zero-curly gate); heading spelled
      "Acknowledgements" and "recognise" kept — the section's British
      forms are her hand showing, chosen not accidental (flagged, kept
      on her go); the AI-use note's "much of the prose" → "nearly all
      of the prose" (now agrees with the acknowledgements' stronger
      claim; the delegation record supports it); the draftline pointer
      "on the final page" → "at the end" (pagination no longer
      guarantees the note the last page).
- [ ] Noted, not touched: §1's disclosure paragraph still says "most of
      these sentences" — true under the stronger claim, read as the
      front matter's conservative register; say the word to harmonize.
- Verification, mechanical (the eleven checks not run: none reads the
  paper file, and the splice is back-matter prose, zero math): curly 0;
  <p> 160/160 and <div> 33/33 balanced; h2 15 (twelve sections +
  appendix + references + acknowledgements); each splice marker present
  exactly once. Main arc untouched; back matter +~230 words; the render
  is now 30 pages.

## Verify-list — 2026-08-07, pass 4: the finishing pass

Pass 4, the last of the readability arc (before-state:
`the_link_pre_pass4_snapshot.html`; PDF deferred by Stella — she reads the
HTML, renders later). Two final agent reads: Dr. R. bookend (45–50 min,
"would referee it seriously," arithmetic spot-checks all verify) and a full
copy-edit (zero spelling errors, every tag balanced, notation uniform, one
citation orphan). 37 fixes; ALL ELEVEN checks green; counts 15 props /
17 remarks / 13 preds / 7 figs / 11 eqs / 0 curly; main arc 13,883 words.
- [ ] Veto window, wording (from the Dr. R. read): §1's welfare sentence
      split in two and the second-welfare-theorem phrase de-pasted (verbatim
      in abstract + Prop 13 only — echo, not paste); §11's duplicated
      offshoring-inseparability clause cut; "Three notes and a coda"; "the
      interest sliver" named at first use; a one-line opener on the
      Predictions list; Figure 5's caption slimmed with its analysis moved
      into §8 body (the borrowed channel: "wage taxes if the link holds,
      rents or inflation if it does not"); "George is not merely elegant;
      in the corner, his base is the necessary one" (now matches 7(iii)'s
      proved scope); "whether it binds is political economy"; "Pigouvian
      charge"; "holds the adoption decision" harmonized at both sites; the
      manager pointer moved into ¶(c) so §4 closes on its crown alone; the
      manager appendix remark gains its mechanism sentence (the strike-
      threat logic); the κ-deferral paragraph fused to one sentence.
- [ ] Veto window, mechanics (from the copy-edit): the §8 garden-path
      "because of the $9.8T..." restructured; "remains" agreement; work–exit
      en dash; inframarginal; quantity exclusions; a serial comma;
      Proposition 1 finally named — "(The price on the link)"; "Prop. 8" →
      "Proposition 8"; Malthus (1798) cited in §1 and entered in References;
      Ricardo's entry notes the 1821 third edition and "On Machinery";
      editors (Agrawal, Gans, and Goldfarb) added to both book chapters;
      NBER 18629 and Oxford DP 819 verified live and added; Prediction 4's
      "METR microdata" → "effective-marginal-tax-rate microdata" (collision
      with the eval org and the capital-tax usage); html lang="en", a
      <title>, and alt text on all seven figures — the HTML is the reading
      copy now.
- [ ] FLAGGED, NOT FIXED — the handoff list, each needing Stella:
      (1) The AI note's "the code and data are public" has NO address, and
      the repo is not under version control on this machine. Needs a public
      repo + URL; wiring it in is a one-line edit once it exists.
      (2) Substantive referee-anticipation (authorial): Prop 2 cites A&R's
      condition as "their distributional sense" rather than stating it;
      w_K in Prop 11 is a primitive with no supply side.
      (3) Figure unit: Figures 6–7 are default-matplotlib against the house
      style of 1–5; Figure 6's y-label renders its subscript plain; Figure
      4's schematic U begins near the 40th percentile against the text's
      70th–95th. One contained regeneration unit under the figure protocol.
      (4) Journal-prep: abstract length vs journal limits; no JEL codes or
      keywords.
      (5) Voice, flagged by two independent readers and KEPT under the
      standing rule — the "surprise" aside, "Technology giveth", the mother
      sentence, Prop 1(ii)'s telegraph. Say the word and any goes.
      (6) Prediction 12's machinery lives one section later (§10); its tag
      admits it. Fixing it is structural; left.

## Verify-list — 2026-08-07, pass 3: the split and the basket

Pass 3 (before-state: `the_link_pre_pass3_snapshot.html`; adversarial audit:
50/50 hunks matched to manifest, ZERO unmanifested, equation multiset
byte-identical, independent renumber sweep 35/35 correct; ALL ELEVEN checks
green; structure now §§1–12, 15 props / 17 remarks / 13 preds / 7 figs /
11 eqs / 0 curly; main arc 14,058 → 13,848 words):
- [ ] Veto window: THE SPLIT — old §6 divided at its hinge into "6. The
      fiscal system sits downstream of the wage loop" (the failure half:
      Props 6–7, regime dial) and NEW "7. The remedy, priced" (feasibility,
      enclosure, mix) with a one-sentence lead naming the three steps;
      §§7–11 renumbered 8–12; twelve section references repointed; the
      fork's bill-and-credit sentence genericized to "the fiscal ledger"
      (it now spans both halves). Prop and figure numbers untouched.
- [ ] Veto window: THE DEMOTIONS (your basket, used) — three blocks moved
      whole to the appendix, each leaving a one-line pointer: the manager
      paragraph (§4; its crown "written in prices / written in law" stays
      in the body); the CES-dial remark (§5, moved byte-identical, §5's
      deferral sentence now counts three); the insurance reading (§6, now
      "Remark (insurance: conditioning as coverage)", its crown "the
      contract that pays in every state is the one written on none" moved
      with it). Not demoted, deliberately: everything else I probed is
      load-bearing for a later section — the enclosure remark items,
      the decomposition remark, the credence and superstar remarks, the
      §10 ledger. The basket takes passengers, not crew.
- [ ] Veto window: TWO MICRO-CUTS — the fortification block's restated
      parity sentence fused ("A statute never expires; what it protects,
      only politics can dislodge, at a price"); the closure setup's
      duplicate "wage of waiting" appositive removed (the identification
      lives in Prop 3's statement). The knife's full haul was ~17 words:
      after two gated passes the sentence-level fat is gone, which is why
      this pass restructured instead of deleting.
- the_link_new.pdf remains stale relative to the HTML (render is yours).

## Verify-list — 2026-08-07, readability pass 2

Pass 2 on the paper (before-state: `the_link_pre_pass2_snapshot.html`;
verifier reports summarized in the changelog; ALL ELEVEN checks green ×3
runs; structure 15/15/13/7; zero curly; zero "↓" glyphs):
- [ ] Veto window: the §6 title change ("The fiscal system sits downstream
      of the wage loop" — the old "tributary of the labor loop" pointed the
      metaphor backwards; the abstract's tributary got the same fix) and
      the wage-loop gloss in §1 ("funded by wages, keyed to work"); the two
      abstract restructures (strata sentence linearized; uniqueness
      sentence main-clause-first, with "fiscal" scoping the domain and
      "that becomes exact" resolving the qualifier); the new §5 and §6
      on-ramp sentences (words before algebra, the house pattern); Prop 3's
      ideas/Romer discussion moved OUT of the statement to a bold-led
      paragraph before the model-weights instance, + Romer (1990) added to
      References (was cited with no entry); Prop 6's purpose-first opener;
      Prop 10's h → ψ rename (collision with land services h and h_s/h_e);
      first-use glosses (waterline = w/c in §2 prose, machine parity =
      c·ρ̄, LVT acronym, corner in §1's roadmap, "Machinery in Section 9"
      on Prediction 12, §9 ledger's bare K reworded); §10's announced
      metaphor hand-off ("Section 6's scaffolding hardens into structure"
      — replaces the unannounced "bridge"); 13(i) "at every rate t_L";
      7(iii)'s fragment given a verb; the re-paragraphings (§1 roadmap →
      4 ¶s incl. two long-sentence splits, §9 ledger → 7 ¶s, related work
      → 2 ¶s, fortification (b)/(c), Prop 6 statement at (ii)/(iii));
      Fig 5 caption's apposition ("the owner loop being").
- [ ] Kept deliberately against the cold reader's complaints (voice): the
      "Technology giveth" crown, the "surprise" worked-instance aside,
      Prop 1(ii)'s telegraph, "prices a near-empty set", "the proviso is
      load-bearing". Say the word and any of these goes.
- [ ] Flagged, not treated: the cold read clocks the paper at ~45 min
      (~13k body words) against the 40-minute target. Cutting length was
      not this unit's mandate; available as a next unit (the cut pass).
- the_link_new.pdf is now stale relative to the HTML (render is yours).

## Verify-list — 2026-08-06 session 3 cont., all data units built

Companion unit 5 — cross-validation + reinstatement (checks/
check_crossval.py ALL GREEN, 18; records: `companion/data/
crossval_ledger.txt`, README §unit 5):
- [ ] Veto window: the reinstatement instrument (23 O*NET releases,
      2003–2026, dates live-parsed; two members bracketing rewording
      churn — ID undercount, text overcount; matched-occupation
      restriction; the Green-Task-Statements member-match trap caught and
      killed; cp1252 era handled); the HEADLINE — mature-era births ~12 →
      0.0 per 1,000/yr, latest pair literally zero, 2024 pruning wave
      real — and its honesty frame (construction-ramp caveat, trend read
      2012+ only, "the instrument's own drying is part of the finding");
      the friction design (2015–19 vs 2022–25 log-share slopes, covid
      excluded, MIN_EMP screen) and its two guarded sentences (no
      positive aggregate exposure gradient — low decelerated MOST; the
      flagship customer-service instance +1.7 → −5.9 %/yr) plus the
      punctuated-instances framing (translators stalled, data scientists
      decelerated, data entry accelerated down); the named-instances
      selection rule (top-8 exposure among ≥200k emp + labeled canonical
      adds).

## Verify-list — 2026-08-06 session 3 cont., wedge layer built

Companion unit 4 — family C wedge layer (checks/check_wedges.py ALL GREEN,
24; records: `companion/data/wedges_ledger.txt`, README §unit 4):
- [ ] Veto window: the wedge members (H–M union coverage/membership
      pre-period 1999–2001 + 2025; CPS-53 licensure at SOC-major level,
      ECOLOGICAL attachment to detailed occupations by employment mix —
      labeled, the resolution public data allows; A&R 40–50% kept as a
      cited level anchor, no per-occupation µ constructed); the
      hand-verified CPS-group→SOC-major table (22 entries, mechanical);
      the test framing — direction reported not gated, with exactly two
      SENTENCE GUARDS pinning published claims (licensure survivor gap
      all rules; high-routine early>late all rules); the honest-mixed
      unconditional result stated as such (Spearman −0.10 to −0.18,
      rule-sensitive cohort pattern) beside the clean conditional one
      (high-routine tercile: ~19–20% early vs ~5–14% late); the 2025
      unionstats mapping floor at 0.80 (extra SOC-2018 hop; realized
      0.982); economy anchors (15.0% → 11.1% coverage, matching
      published aggregates).

## Verify-list — 2026-08-06 session 3 cont., right tail built

Companion unit 3 — family B right tail (checks/check_righttail.py ALL
GREEN, 23; records: `companion/data/righttail_ledger.txt`, README §unit 3):
- [ ] Veto window: the exposure mapping (Eloundou's six published variants
      AS the mapping grid — no invented mapping; soc8→soc6→occ1990dd by
      the unit-1 chains, mean across mapped codes; 100% of 2025
      employment covered); the headline band framing (0–56% of surviving
      mass at exposure ≥ 0.5 — α floor to γ ceiling, ~23% median variant;
      the "survivors more exposed than the flipped under strict rules"
      sentence, now check-guarded); the clock membership (ECI + GPQA +
      SWE-bench + METR horizon, frontier = cummax, deterministic
      tie-break after the quicksort-instability catch); doubling 5.0
      months over 2019–2026 stated WITH the METR-2024 7.1-month contrast
      (their own steepening, longer window); the METR licensing posture
      (README points to an absent LICENSE — Epoch's CC-BY republication
      is primary, raw runs validation-only with attribution, flag carried
      to the data note); rule-based-only model matching (15 matched,
      log-corr 0.993; ambiguous variants dropped, never guessed, gate
      sized accordingly at ≥10).

## Verify-list — 2026-08-06 session 3 cont., envelope built

Companion unit 2 — w/c grid + family A envelope (checks/check_envelope.py
ALL GREEN, 35; records: `companion/data/envelope_ledger.txt`, README §unit 2):
- [ ] Veto window: the six-member w/c grid (AHETPI + panel-internal OEWS
      wage × hedonic-computers B935RG3Q086SBEA + computer-PPI
      PCU334111334111 + broad-equipment Y033RG3Q086SBEA, all
      title-verified; hedonic sanity band widened 0.25→0.40 with reason —
      the post-2010 decline slowdown; waterline ×8.0 median, ×2.4–×16
      band); normalization 1999=1, schedule delivered in waterline units,
      scale-free by construction (stated, not hidden); the three labeled
      flip rules (d30/d40/d50 share-decline from within-panel peak, ≥3
      post-peak years, MIN_EMP 10k screen) → 33%/15%/11% of 1999 mass
      flipped; the envelope identity ρ̃ = w/c(flip year) (re-derived in
      the check); era stats incl. rho_iqr_log ~0.3→~0.9 (the spread the
      flattening argument will read); the CONFOUND ON DISPLAY — Chief
      Executives (2001 OEWS classification break) and Carpenters (housing
      crash) flip under the rules and are kept + documented, not
      hand-dropped (pre-registered; instrument refinement in later
      units); the tie-aware operators anchor (rank-position check after
      the discrete-rho tie tripped the naive median comparison).

## Verify-list — 2026-08-06 session 3 cont., panel built

Companion unit 1 — task panel (checks/check_panel.py ALL GREEN, 24 checks;
records: `companion/data/build_ledger.txt`, `companion/README.md`):
- [ ] Veto window: the mapping machinery — SOC hierarchy walk (exact →
      census X-wildcard prefix → parent broad → children union; 30-37% of
      early-year employment arrives via the walk, 5-6% in 2021+) and
      SPLIT_EQUAL for one-to-many codes (binds on ≤2% of codes; flagged
      grid axis); coverage floors (yearly ≥0.85 gate, realized 0.91-0.97,
      median 0.96, measured against each file's own all-occupations
      total); the parked members (1997-98 pre-SOC files; 2019-20 hybrid
      code 15-1256 ≈1% employment those two years — reported unmapped,
      not imputed); the derived top_source_title/label_latest convenience
      columns (majority-employment source titles, labeled as derived);
      and the worked-instance anchor choice (telephone operators,
      occ1990dd 348: 299k → 38k over 1999-2025, in the checks as a
      structural gate).

## Verify-list — 2026-08-06 session 3, companion scoped

Carried items closed this session (no veto needed, recorded for the file):
- the_link.pdf regeneration — done by Stella outside the session;
  `the_link_new.pdf` (Aug 6 15:40) verified against the rewrite's markers
  ("capability that drafted it", "one-third and rising") — it IS the
  current paper. `the_link.pdf` and `the_link_1.pdf` are stale
  intermediates, left in place for Stella to keep or delete.
- Closure subsection read in place (end of §5) — clean; on-ramp, Prop 5,
  CES dial, and the stark-distribution remark hand off to Prop 8 as
  intended.
- No .tex master exists — repo-wide glob finds only `closure_section.tex`
  (the derivation record).

Companion paper scoping unit (`companion_schedule_spec.md` = record):
- [ ] Veto window: the three identification families (A revealed-adoption
      envelope via Lemma 1 inversion; B benchmark-mapped right tail
      2018–2025; C wedge layer + Prop 2 targeting-order test); the
      pre-registered honesty ledger (flip-dating bounds, mapping-grid
      disclosure, benchmark-shaped-task bias stated); the wall routings
      (openICPSR and IPUMS excluded — A&R wedge rents from published
      tables only, employment shares via Census API/OEWS); the
      reinstatement-series bonus (DOT→O*NET task birth/death — measures
      the §9 fork's premise); and the four open choices — working title
      ("The Schedule", placeholder), home (`companion/` in this repo,
      default), register (parent's voice rules, drier density), worked
      instance (one occupation end-to-end, default yes).

## Verify-list — 2026-08-05, all units spliced + review pass

Last bits + review (record: `repairs_section.html`):
- [ ] Veto window: Lemma 2's statement and proof; Prop 3's durability
      sentence (c = ℓr(δ+d)/(1−a(δ+d))); Prediction 1's by-construction
      tag; the abstract's uniqueness qualifier; the five new reference
      hooks in related work; Figure 7 + its §7 paragraph (complete
      calendar years only, fork 4.8×); and the review fixes — κ "sits
      lower at every q" (the rate claim was false), §7's "the
      propositions", captions without build-script pointers, superstar
      share "rising at rate 1 − 1/n", bare r·T fused to rT (subscripted
      forms keep the dot), the co-presence cite "(the remark to
      Proposition 11)", the empirics spec's implemented-vs-open honesty
      block, make_figs.py + README reproduction fixes.

The gate evolved (decisions log): units now splice under standing delegation
with the veto window open; exact records kept per unit, so a veto comes back
out cleanly. Everything below is IN the paper.

Item 4 — conditionality decomposition (`conditionality_section.html` =
record; checks green):
- [ ] Veto window: s(y) reduced-form income channel; symmetric corner burn
      |c·ρ̄ − s|; the "u pushes wages up / Speenhamland reversed" sentence
      (salient — easy to soften); (m_w, m_e) notation (τ was taken by the
      parcel dummy); Hoynes–Rothstein entry (ARE vol. 11, no pages —
      confirm against your copy); remark length/voice.

Item 3, theorem half — feasibility Prop 8 (spliced by the cut-off session;
verified independently this session; `feasibility_section.html` = record):
- [ ] Veto window: Prop 8 statement/proof/worked instance (N = 50/80/120 in
      the closure world); both remarks; §5 forward-refs now naming
      Proposition 8; and one post-splice wording repair — 8(i)'s "without
      bound" clause corrected (κ is bounded by T/(N·h_s); a ↓ raises it
      only as far as bounded q allows, ρ̄/ℓ margins run toward the ratio).

Fortification (`fortification_section.html` = record; checks green):
- [ ] Veto window: Prop 2 proviso sentence; the §4 remark (filter/
      distillation, punctuated adoption, twice-compounding drag, fortified
      wages as institutional rents, the manager parenthesis); Prediction 2
      amended (count stays 11); §9 "Exogenous wedges" sentence upgraded.

Item 8 — open economy (SPLICED; `open_section.html` = record; checks
green):
- [ ] Veto window: §10's existence, title, and one-page discipline;
      Prop 12 (i)–(iii) — the min-waterline, the way-station claim, the
      jurisdictional split and "bridge is constitutive"; the borders/
      rooms/feet remark (incl. the automation-vs-offshoring
      inseparability sentence and the migration flag); §9 ledger entry
      retitle; Grossman–Rossi-Hansberg in related work + References;
      w_f, ρ̃_f notation; welfare's bump to §11 / Prop 13.

Item 7 — welfare (SPLICED; `welfare_section.html` = record; checks green;
NOTE: now §11 / Proposition 13 after the open-economy page took §10 / 12):
- [ ] Veto window: §10's existence and title; Prop 12 (i)–(iii), incl. the
      "second welfare theorem with instruments that exist" framing and the
      converse's scope ("within the model's instrument set, up to the
      corner base-equivalence"); the moral remark ("fork between two
      bookkeeping systems"; the Pigouvian composes-freely sentence keeps
      the companion boundary); the second-best remark (Diamond–Mirrlees
      cite; "the planner's timetable is two time series"); §1 roadmap and
      abstract one-liners ("dystopia or inheritance — a choice of tax
      base"); ω_i notation.

Item 2 — enclosure margin (SPLICED; `enclosure_section.html` = record;
checks green):
- [ ] Veto window: Prop 9 (i)–(iii) — the idle-margin reading of the
      commons, s(q) = max(s_0 − q·h_e, s_d) with the autarkic-keep
      convention (s_0 machine-independent; the honesty parenthesis covers
      machine-tooled exit), q_enc finite, the crowding race and N_crit;
      the desperate-supply remark and its "transfer becomes the commons"
      closing; §2's "a debt Section 6 prices" pointer; the mix intro now
      citing 8 and 9; Prediction 13 (coresidence tracks rent-to-wage);
      abstract count thirteen; the double renumber (mix → 10, fork → 11
      FINAL — third number today for the fork, flagged for your patience).

Item 6 — mix frontier (SPLICED; `mix_section.html` = record; checks
green; NOTE: now Proposition 10 after the enclosure splice took 9):
- [ ] Veto window: Prop 9 (i)–(iii) — rent-base-first optimum (t_L = 1 at
      full capture), the λ_C·(1−κ)² deadweight display and its "product of
      the two measured series" sentence, the corner coincidence via Prop
      5's identity; the "what the VAT is for" remark incl. the in-text
      pair "(0.72, 0.33) → 0.32; at, say, (0.50, 0.60) → 0.08"; the Baumol
      fork's renumber 9 → 10; E for consumption (C taken by the fork's
      unit cost).

Item 5 — K-set / Baumol fork (SPLICED; `kset_section.html` = record;
checks green; NOTE: renumbered twice — FINAL number Proposition 11):
- [ ] Veto window: Prop 9 (i)–(iii), incl. the three-way terminal split
      and the K = ∅ boundary claim; the credence bound π_H ≤ min(φ_H,
      v·f/(1−v)) and "what law reserves plus what bodies witness"; the
      superstar/barbell remark ("aggregate rescue, median demolition");
      Prediction 12; abstract count eleven → twelve; the §9 Human-premium
      ledger block replaced (AJJ engagement now runs through Prop 9); the
      κ-feedback sentence; n reused as K-worker count (registry note).

Item 3, empirical half — κ pipeline (ran clean; row in §7):
- [ ] Veto window: the Orshansky-base bundle method (1963 constants 782/1540
      per capita, CPI-updated — methodological parameters in the grid,
      validated against published 2023 thresholds at $7,778/$15,318); the
      §7 table row "κ 0.33 [0.18–0.59] (2025)"; the data-note clause adding
      Z.1/fixed-assets/CPI sources; the README lines. Caveats lodged in the
      script header: all land measures are lower bounds (household-only or
      housing-only; farm/government/financial land omitted), so true κ sits
      above the band's middle; band width is substantially cap-rate spread
      (z1 members inherit the rate cycle — the 1980s bulge is GS10, not
      land); NFC structures end 2020, so the economy-wide member stops
      there; Z.1 post-1995 caveat carried from the spec.

Consistency pass (2026-08-05; before-state snapshot =
`the_link_pre_consistency_snapshot.html` at repo root):
- [ ] Veto window: straight-quote normalization (the original's typography;
      the curly marks came from the day's splices); the timeless
      rewordings (closure intro, migration paragraph, §9 pointer, Prop 9
      intro, Prop 8 tense); §1 roadmap sentence; abstract κ sentence
      ("one-third and rising"); the appendix (heterogeneous-land,
      corner-above, base-feeds-back remarks moved out with pointers in
      place); §7 "The remedy, measured" paragraph + Figure 6. A deeper
      restructure (own section for Props 8–9, section renumbering) was
      considered and NOT done — available as a later unit.

Carried: (all three closed 2026-08-06 session 3 — see the current
verify-list block at top for how).

Pre-splice list (Prop C derivation, erratum patch, simplifications, audience
call, numbering, forward refs, 4(iii) micro-patch): signed off 2026-08-05 —
see decisions log.

## Decisions log

- 2026-08-07 · Appendix policy (Stella, mid-pass-3: "the appendix, that's a
  kind of wastepaper basket, use it liberally"): demotion to the appendix
  is a standing instrument for main-arc length. Rules as practiced: blocks
  move whole (never paraphrased down), every demotion leaves a one-line
  body pointer, crowns the arc needs stay in the arc, and nothing moves
  that a later section leans on.

- 2026-08-07 · Ownership delegation made standing (Stella: "You can touch
  anything, it's your paper"; "if you wanna change the world, don't ask for
  permission"): readability pass 2 executed with no scope restriction and
  no pre-approval. Checks still gate absolutely; snapshots and verify-lists
  still written per unit — the delegation changes who decides, not what
  gets recorded.

- 2026-08-06 · READABILITY REWRITE delegated with NO veto window ("copy the
  original document, then work on a new one until you are satisfied, not
  me"). Original preserved: `the_link_pre_rewrite_snapshot.html`. Brief,
  targets, job specs, merge rules, and satisfaction criteria:
  `rewrite_brief.md` (the context lifeboat — read it before continuing the
  rewrite). Voice allocation rule adopted: every technical claim stated
  plainly before any compressed form; poetry after proof, never instead;
  summits keep the voice, climbs lose it. Delete-first method: rewriter
  subagents receive section JOBS, never current prose.

- 2026-08-05 · Working format: repo lives with Stella (`paper/`, `checks/`,
  `data/`, `NOTES.md`); session protocol above. Claude keeps only a status
  pointer in its own memory; this file is canonical.
- 2026-08-05 · Audience: working-paper register (arXiv/SSRN-serious), voice
  kept — it is load-bearing; a journal-style sanding pass is a separable
  later project. (Claude's call under delegation; open to veto.)
- 2026-08-05 · LVT vs VAT: not forced to a choice. Item 6 targets an
  interior-mix theorem — weights travel with the regime dial (VAT-heavy in
  transition: reaches dynamic and institutional rents, needs no cadastre;
  LVT-heavy in the corner: the sole invariance; the two bases coincide at the
  pure corner by Prop C). If the algebra ever collapses to knife-edge
  dominance, flag it before writing it in.
- 2026-08-05 · Sequencing confirmed: 1 → 4 → 3 → 5 → 6, then 2, 7, 8; item 9
  (empirical capability schedule) spun off as a companion-paper candidate.
- 2026-08-05 · Verify-list signed off in full ("all sounds good"): Prop C
  derivation (incl. pass-through and corner-above remark), erratum patch,
  homogeneous-land + δ = 0 simplifications, audience call stands, renumber
  at splice (C → Prop 5; Conditionality → 6; Funding → 7), feasibility
  forward-references kept, 4(iii) proof micro-patch approved. Splice
  executed the same day; see changelog.
- 2026-08-05 · Standing delegation broadened (Stella, in both parallel
  sessions: "I trust you on any calls you need to make, keep going" / "I
  leave the call up to you"): the gate moves from ask-then-splice to
  splice-with-veto-window. Checks still gate absolutely; the verify-list
  becomes the veto window; exact pre-splice records kept per unit.
- 2026-08-05 · Land-value series blocker dissolved by house method (under
  delegation): no single-source choice — all defensible variants through
  §7's rule grid (Larson/BEA-style × cap-rate band; Z.1 residual with
  post-1995 caveat; flow-side lower bound), medians with bands. Spec:
  `feasibility_empirics_spec.md`.
- 2026-08-05 · Fortification critique adopted at assessed size (her "go for
  it"): Prop 2 proviso + §4 remark + amended Prediction 2 + upgraded §9
  ledger sentence; no new proposition; bindingness of blocking flagged as
  political economy outside the model.

## Notation registry

In use (current draft): x task index; γL, γM capabilities; ρ = γL/γM; μ wedge;
ρ̃ = ρ/μ; x* threshold; c machine rental; w wage; s outside option; a, ℓ
machine recipe; r site rent; δ time preference; ρ̄ flat-schedule edge;
L̄ = ∫dx/γL; pg final-good price; σ land share of expenditure; λi wage-linkage
shares; t tax rate; u, b, b′ transfers; N workers. Entered with the closure
splice (2026-08-05): T, T_P, T_H land stocks; X gross machine services;
q ≡ r/pg; η CES elasticity (goods vs land services); s_h(q) CES
land-expenditure share. Entered with the conditionality splice: m_w, m_e
instrument payments in/out of work; Δ = m_w − m_e work-contingent
differential; R reservation wage (standalone — unrelated to λ_R's
subscript); y exit-state unearned cash (lowercase — unrelated to output Y);
s(y) reduced-form outside-option schedule, s′ ≥ 0, s(0) = s. Entered with
the feasibility splice: g_s, h_s subsistence bundle quantities; P_s =
pg·g_s + r·h_s subsistence cost; κ = rT/(N·P_s) coverage ratio at full
capture; q* = N·g_s/(T − N·h_s) feasibility threshold. The fortification
unit adds no paper notation (check-internal symbols only).

Entered with the K-set splice (2026-08-05): K non-automatable task set,
measure k; w_K K-wage; φ_H latent human-provenance taste; v verification
power; f provenance-fraud penalty; π_H sustainable provenance premium
(≤ min(φ_H, v·f/(1−v))); β broadcastable fraction of K-demand; θ, θ_T, θ_K
CES taste weights (context-local); n K-worker count (superstar remark).
Entered with the mix splice (2026-08-05): t_L, t_V LVT/VAT rates; E
aggregate consumption spending (bare C deliberately avoided — it is the
Baumol fork's unit cost).
The June–July framing ("the floor is a property of the proof apparatus
over tasks, not of the tasks") is now Prop 9's first remark, near-verbatim.

Entered with the enclosure splice (2026-08-05): s_0 autarkic keep of the
exit life (goods numeraire, machine-independent by construction); s_d
dependency floor; h_e exit-plot land requirement; q_enc = (s_0 − s_d)/h_e
enclosure threshold. The reserved s(r) is delivered as s(q) — the same
object on the paper's relative-price dial; item 2 needed no
participation-count symbol after all (n stays the K-worker count).

Entered with the welfare splice (2026-08-05): ω_i inherited land share of
person i (§11, context-local). Entered with the open-economy splice
(2026-08-05): w_f foreign wage; ρ̃_f wedge-deflated home-over-foreign
human edge (§10).

Entered with readability pass 2 (2026-08-07): ψ — the deadweight scale in
Prop 10's half-square hypothesis, renamed from a bare h that had escaped
this registry and collided with land services h and the (h_s, h_e) family.
Alpha-rename only; no claim touched; check_mix unaffected (sympy-internal
symbols).

Reserved for new sections: (none — every reserved symbol is delivered).
σs (subsistence land share) RETIRED 2026-08-05 — superseded by the
(g_s, h_s) quantity pair. τ deliberately NOT used for instruments — it is
the parcel dummy in the idle-margin remark (now in the appendix, moved by
the consistency pass). Entered with the small-repairs splice (2026-08-05):
d machine wear rate (Prop 3's durability sentence).

Collisions already footnoted in the draft, keep avoiding: A&R's λ
(task-substitution elasticity) and ρ̂ (wedge-markup estimate) are unrelated to
the λi and ρ used here.

## Queue (from the agreed plan)

1. GE closure / conservation-of-rents identity — **DONE — SPLICED
   2026-08-05** into the paper as Proposition 5 (erratum patch and 4(iii)
   micro-patch applied; downstream props renumbered 6, 7).
   `closure_section.tex` = derivation record; `closure_section.html` =
   pre-splice record.
4. Prop 6(i) decomposition — **DONE — SPLICED 2026-08-05** (by the parallel
   session, from `conditionality_section.html`; surviving session
   double-applied and then deduped, see changelog). Checks:
   `checks/check_conditionality.py`.
3. Feasibility theorem + coverage ratio κ = rT/(N·P_s) — **DONE, BOTH
   HALVES 2026-08-05.** Theorem half spliced as Proposition 8 (cut-off
   session; verified + one wording repair; `checks/check_feasibility.py`).
   Empirical half ran clean: `code/feasibility_kappa.py`, 12 FRED series
   all validated (Z.1 real-estate/structures residuals, PCE housing, GS10,
   NIPA population, CPI), κ(2025) = 0.33 [0.18–0.59], ≈0.05 in the 1950s —
   the U.S. is in Prop 8's "not yet" region (q < q*) with κ climbing
   secularly; outputs `data/kappa_results.csv` +
   `figures/kappa_coverage.png`; §7 table row + data-note clause added;
   README updated.
5. K-set / Aghion–Jones–Jones fork — **DONE — SPLICED 2026-08-05** as
   Proposition 9 (the Baumol fork) in a subsection closing §9, with the
   credence remark (φ_H × verifiability; terminal K = provenance law +
   co-presence, tying back to fortification), the superstar/barbell
   remark, the κ-feedback sentence, Prediction 12 (abstract count →
   twelve), and the §9 Human-premium ledger block replaced by a pointer.
   Checks: `checks/check_kset.py`; record: `kset_section.html`.
6. LVT/VAT mix frontier — **DONE — SPLICED 2026-08-05** as Proposition 9
   (The mix frontier), subsection "The mix on the way down" closing §6:
   corner coincidence of the bases (Prop 5's identity), transition blind
   spots (LVT misses non-site rents; VAT misses saved rents and carries
   the regime dial on its wage slice), rent-base-first optimum with
   t_V = N·P_s·(1−κ)/E, transition deadweight ∝ λ_C·(1−κ)² — the product
   of the two measured series (0.32 today). Interior for the whole
   crossing; no knife-edge dominance (the decisions-log worry did not
   materialize). Baumol fork renumbered 9 → 10 (two sites). Checks:
   `checks/check_mix.py`; record: `mix_section.html`.
2. Endogenous s(r) — **DONE — SPLICED 2026-08-05** as Proposition 9 (The
   enclosure margin), subsection "The commons, priced" in §6 between
   feasibility and the mix: the commons is the idle margin and the corner
   closes it (5i); s(q) = max(s_0 − q·h_e, s_d) falls one-for-one with the
   land price of subsistence living; enclosure completes at finite
   q_enc = (s_0 − s_d)/h_e; the race q_enc vs q* orders by crowding
   (N_crit = q_enc·T/(g_s + q_enc·h_s) = 60 in the closure instance); the
   desperate-supply remark (linked regime) + the transfer-as-commons
   closing (past q_enc the floor is s_d + u, billed at exactly h_e·q,
   funded from inside rT). Companions: §2 pointer ("a debt Section 6
   prices"), mix intro now cites 8 and 9, Prediction 13 (coresidence
   tracks rent-to-wage), abstract count → thirteen. Renumbered: mix → 10,
   Baumol fork → 11 (final). Checks: `checks/check_enclosure.py`;
   record: `enclosure_section.html`.
7. Welfare / optimal policy — **DONE — SPLICED 2026-08-05** as the new
   closing §10 ("What the planner would do") with Proposition 12 (The
   corner welfare theorem): (i) under u the private participation rule
   coincides with the social one (the corner wage IS the machine's
   replacement cost); (ii) the George pair implements the one-parameter
   family from inherited to equal division of rT at zero deadweight — the
   second welfare theorem with instruments that exist; (iii) uniqueness up
   to the corner base-equivalence. Remarks: the moral (the fork is a tax
   base — "dystopia or inheritance") and the second best (production
   efficiency survives, Diamond–Mirrlees 1971 cited + added to refs; the
   schedule is the two measured series; Prop 9(iii)'s gap treated as the
   emergency). §1 roadmap + abstract gained the one-line versions. NO
   renumbering (Prop 12 follows 11 in document order). Checks:
   `checks/check_welfare.py`; record: `welfare_section.html`.
8. Open-economy page — **DONE — SPLICED 2026-08-05** as the new §10 ("The
   open economy, in one page") with Proposition 12 (Trade as the early
   waterline): the foreign wage as a second machine rental (same
   targeting, earlier timing; wedges negative altitude in both waters);
   offshoring as way-station (the terminal allocation is the closed
   corner); rents to the producing jurisdiction's land, with the border
   splitting the bases — destination VAT reaches the imported land
   content the domestic LVT cannot, so the mix frontier is interior for a
   second reason and the bridge is constitutive for deficit consumers.
   Remark: one waterline at two heights; the room shields twice; migration
   flagged per-jurisdiction. Welfare renumbered to §11 / Proposition 13.
   Companions: §9 ledger entry retitled and pointed; Grossman–
   Rossi-Hansberg (2008) added to related work + References. Checks:
   `checks/check_open.py`; record: `open_section.html`. **The numbered
   queue (items 1–8) is complete.** NEXT: the small-repairs batch + the
   deflator-fork figure (Prediction 8) — the remaining in-paper work.
Small-repairs batch — **DONE IN FULL 2026-08-05** (`checks/check_repairs.py`
green; record `repairs_section.html`): abstract uniqueness qualifier
(aligned with 13(iii)); "ever more gadgets" → "as many gadgets as ever";
Prediction 1 relabeled by-construction; 7(i) display marked "at full
participation"; Lemma 2 (existence/uniqueness, single crossing) into §2;
Prop 3's durability generalization c = ℓr(δ+d)/(1−a(δ+d)); all five
references added with in-text hooks (Zeira; Autor; Hémous–Olsen;
Karabarbounis–Neiman; Knoll–Schularick–Steger for Prediction 6). Earlier
from this batch: wedge-endogeneity caveat (absorbed by fortification);
Hoynes–Rothstein (added with conditionality).
9. Empirical ρ̃(x,t) schedule — companion paper, **SCOPING UNIT DONE
   2026-08-06** (her go-ahead: "the next paper... shall we give it a go").
   Design spec + pre-registration: `companion_schedule_spec.md` — three
   identification families (A: revealed-adoption envelope, Lemma 1
   inverted, DOT/O*NET × occ1990dd × OEWS/Census; B: benchmark-mapped
   right tail 2018–2025, Epoch/METR/Eloundou; C: wedge layer,
   unionstats/BLS-licensure/A&R-published), all load-bearing sources
   probed live 2026-08-06 and REACHABLE with open licenses; walls
   (openICPSR, IPUMS) routed around per the data rule. **UNIT 1 (task
   panel) DONE same day** — `companion/` built (code/cache/data/checks,
   README): OEWS 1999-2025 × occ1990dd panel (8,696 rows, 326 occs,
   coverage 0.91-0.97) + ALM/offshorability/O*NET attributes table;
   check_panel.py ALL GREEN (24). **UNIT 2 (w/c grid + family A envelope)
   DONE same day** — waterline ×8.0 since 1999 (6-member grid), flip
   rules d30/d40/d50 → 33%/15%/11% of 1999 mass flipped, envelope +
   era-sliced quantiles + density series + first figure
   (`companion/figures/schedule_envelope.png`); check_envelope.py ALL
   GREEN (35). **UNIT 3 (family B right tail) DONE same day** — Eloundou
   exposure × occ1990dd (six-variant grid, 100% 2025-emp coverage),
   capability clock (ECI/GPQA/SWE-bench/METR-horizon; doubling 5.0 months
   2019–2026), METR raw revalidated at log-corr 0.993, surviving-mass
   exposure band 0–56% (≥0.5 threshold), figure
   `companion/figures/right_tail.png`; check_righttail.py ALL GREEN (23).
   **UNIT 4 (family C wedge layer) DONE same day** — H–M union
   coverage (pre-period + 2025) and CPS-53 licensure mapped to occ1990dd,
   targeting-order test run (unconditional weak-but-right-signed;
   high-routine tercile clean under all rules; licensure survivor gap
   7–9pp), figure `companion/figures/wedge_targeting.png`;
   check_wedges.py ALL GREEN (24). **UNIT 5 (cross-validation +
   reinstatement) DONE same day — ALL DATA UNITS COMPLETE.** The
   new-task margin measured across 23 O*NET releases: mature-era births
   ~12 → 0.0 per 1,000/yr (latest pair records zero); friction: no
   aggregate exposure gradient post-LLM (gap open, F binding),
   punctuated instances (customer service +1.7 → −5.9 %/yr);
   check_crossval.py ALL GREEN (18); figure
   `companion/figures/crossval.png`. Remaining: FIRST PROSE (sections
   1–3 against built results) — the writing phase begins.
Deflator-fork figure — **DONE 2026-08-05**: `code/deflator_fork.py` (three
FRED series title-verified; complete-calendar-years guard added after the
review caught a half-year 2026 endpoint), Figure 7 + §7 paragraph +
Prediction 8 tag; fork 4.8× at 2024, from 1.0 at 1964.
Fortification — **DONE — SPLICED 2026-08-05** (Stella's critique, adopted
at assessed size: Prop 2 proviso; §4 remark — filter/distillation,
punctuated adoption, twice-compounding drag, fortified wages as
institutional rents; Prediction 2 amended; §9 ledger upgraded; checks:
`checks/check_fortification.py`; record: `fortification_section.html`).
Interacts with item 5: the fortified set is a policy-made K — pick the
thread up there.

## Changelog

- 2026-08-09 (later session) · HOUSEKEEPING: the working files moved off the
  outer repo root into their homes. This NOTES.md now lives at link-repo root
  (was outer root); `checks/` → `link-repo/checks/`; the per-unit
  `*_section.html` + `closure_section.tex` → `link-repo/drafts/`; the six
  `the_link_pre_*_snapshot.html` → `link-repo/paper/snapshots/`;
  `rewrite_brief.md` and `feasibility_empirics_spec.md` → `link-repo/docs/`;
  `companion_schedule_spec.md` → `companion/`. All moves via git mv; the two
  path-bearing references updated (companion/README.md,
  code/feasibility_kappa.py header); link-repo/README.md map extended. Older
  entries below that say "repo root" mean the OUTER root as it stood then —
  read them against this map. The revision working folder is
  `../the-link-revision/` (its own STATE.md is the resume point for that
  thread).

- 2026-08-09 · ACKNOWLEDGEMENTS SPLICED + THE PDF MYSTERY SOLVED. The
  splice: her three closing paragraphs (final wording, one agreed comma)
  entered as the paper's last section, after the AI-use note; manifest in
  the verify-list above. THE PDF: her "print to pdf has no selectable
  text" diagnosed by byte-level forensics on the three on-disk PDFs.
  the_link.pdf and the_link_1.pdf (Aug 6 morning, 16.8/19.6 MB) carry
  Producer "Microsoft: Print To PDF": ZERO font objects, zero text
  operators — every glyph drawn as vector outlines, so no text layer
  exists and there is nothing to select; the seven JPEGs inside are the
  figures. Cause: choosing the "Microsoft Print to PDF" printer DEVICE
  in the print dialog routes rendering through the Windows driver, which
  outlines all text. the_link_new.pdf (Aug 6 15:40, 0.88 MB) is Producer
  "Skia/PDF m151": 21 embedded fonts, ToUnicode maps, ~78k text
  operators — selectable and searchable; that was the good path all
  along (browser-internal printToPDF). RENDER RULE, now canonical: use
  the browser's built-in "Save as PDF" destination, or the new repo
  pipeline `link-repo/code/render_pdf.py` (Playwright Chromium
  page.pdf, prefer_css_page_size; reproduces the good signature
  exactly). A fresh 30-page selectable render of the post-splice paper
  was produced this session and sent to Stella; then, on her follow-up
  instruction, the two outline intermediates were DELETED and
  the_link_new.pdf refreshed in place — it is now the 30-page
  post-splice render (0.88 MB, text layer verified; paper/ holds just
  the two HTMLs and the one PDF). Edge
  headless was tried first and silently no-ops on this machine (exit 0,
  no output — enterprise policy, likely). DejaVu Serif (the CSS first
  choice) is not installed here, so renders fall back to Georgia —
  cosmetic only. Handoff list otherwise unchanged; the AI note's public
  code/data URL remains the open item.

- 2026-08-07 · PASS 4 EXECUTED: THE FINISHING PASS — THE READABILITY ARC IS
  CLOSED (her "one last pass"; snapshot `the_link_pre_pass4_snapshot.html`).
  Method: mechanical sweeps first (double spaces: only the strata display's
  deliberate ones; zero doubled words, zero unspaced dashes, zero
  hyphenation drift, zero space-before-punctuation) → two working-paper
  numbers verified LIVE per the no-remembered-constants rule (Sachs–
  Kotlikoff = NBER 18629, confirmed at nber.org; Susskind = Oxford DP 819,
  confirmed against the paper's own posted copy) → two parallel finishing
  agents: the Dr. R. bookend read (verdict: finishes in 45–50 min, would
  referee seriously; referee report would ask for A&R's condition stated,
  w_K's determination, and the George-slogan/7(iii) reconciliation — the
  third now fixed, the first two flagged as authorial) and a full
  copy-edit (zero misspellings; 155 <p>/223 <sub>/all tags balanced;
  µ uniformly U+00B5, · ×179, − ×78, zero bare underscores; no citation
  orphans except Malthus — now entered). 37 fixes in two batches; full
  manifest in the verify-list. Leftover greps all zero; ALL ELEVEN checks
  green; figure paths verified on disk (7/7). Main arc 13,883 words.
  THE FOUR-PASS ARC: rewrite (voice, 8-06) → surgery (clarity, 8-07) →
  split + basket (architecture, 8-07) → finish (polish, 8-07). The paper
  stands: §§1–12 + appendix, 2 lemmas + 13 propositions (every one
  machine-verified), 17 remarks, 13 predictions, 7 figures, four
  adversarial audits passed. Remaining work lives in the handoff list
  (verify-list above): the code/data URL, two authorial calls, the
  figs 6–7 unit, journal prep. NEXT sessions: the companion's FIRST PROSE
  (its data phase closed 8-06), and the scorecard idea (annual re-run of
  the prediction pipelines) if Stella wants it.

- 2026-08-07 · PASS 3 EXECUTED: THE CUT THAT BECAME A SPLIT (her "alright,
  another pass" + the mid-turn appendix directive; snapshot:
  `the_link_pre_pass3_snapshot.html`). Went in as a cut pass — the
  flagged ~45-min read vs the 40-min target — with a fresh full read,
  knife-first. FINDING: after passes 1–2 and the review gates, true
  sentence-level fat totals ~17 words in ~15,000; forcing a quota would
  have cut claims or voice, so deletion was refused as the instrument.
  The length problem is architectural: old §6 ran ~3,600 words, five
  props, three subsections, no reader's rest (Dr. R.: flow 3, "reads
  like two sections" — and it IS two: failure, then remedy). EXECUTED
  INSTEAD: (1) the deferred restructure, scoped to the split — new
  "7. The remedy, priced" opens at the feasibility hinge with a
  three-step lead; §§7–11 → 8–12; 12 references repointed; the
  bill-and-credit sentence genericized ("the fiscal ledger") because it
  now spans both halves; prop/figure numbers untouched. (2) The basket,
  per her directive: manager paragraph, CES-dial remark, and insurance
  reading demoted whole to the appendix with body pointers; crowns kept
  in the arc; everything else probed proved load-bearing downstream
  (the paper is unusually cross-referential — the reason the knife came
  back empty). (3) The two real micro-cuts (statute restatement; wage-
  of-waiting appositive). VERIFICATION: token-level diff audit — 50/50
  hunks matched, ZERO unmanifested, equation multiset byte-identical,
  demotions byte-preserved modulo declared fusions, micro-cut survivals
  quoted and confirmed; independent renumber sweep verified all 35
  "Section N" strings against content (no §/Sec./Sections variants
  exist); appendix internals resolve; the audit's one finding — a
  nine-word verbatim echo between the manager pointer and its appendix
  remark, the single redundancy the pass introduced — trimmed. ALL
  ELEVEN checks green (2 runs). Structure: §§1–12 + appendix; 15 props /
  17 remarks (+manager, +insurance) / 13 predictions / 7 figures /
  11 equations / 0 curly. Main arc 14,058 → 13,848 words; total 15,051
  (+70, pointer scaffolding — demotion moves, it does not delete).
  the_link_new.pdf stale (Stella renders). Open question for a future
  unit, honestly stated: the arc now breathes at twelve stations, but
  if the 40-minute budget still binds after her read, the next
  instrument is neither knife nor basket but scope — and that is an
  authorial call, not an editorial one.

- 2026-08-07 · READABILITY PASS 2 executed under the standing ownership
  delegation (snapshot first: `the_link_pre_pass2_snapshot.html`).
  Method: reconciliation (disk = NOTES, clean) → rewrite_brief.md reread →
  own full cold read → nine surgical targets in wave 1 (walls
  re-paragraphed: §1 roadmap → 4 ¶s, §9 assumptions ledger → 7 ¶s, related
  work → 2 ¶s; the abstract's two knotted sentences unknotted
  content-identically; Prop 3's ideas/Romer discussion moved out of the
  statement — the statement now asserts only what the proof proves — and
  re-seated before the model-weights instance; Romer (1990) added to
  References, repairing a dangling citation found in passing; Prop 6
  purpose-first opener; Prop 12(i) run-on split) → adversarial diff audit
  (agent; 9/9 manifest PASS, ZERO unmanifested hunks, all 11 equation
  displays byte-identical; its two flags both adopted: "fiscal" restored
  to the abstract's uniqueness scope after the dropped "such" quietly
  widened the claim; "in each regime" trimmed from Prop 6's opener as an
  overpromise for (iii)) → Dr. R. cold arc read (agent, persona verbatim
  from the brief; verdict: finishes at ~45 min, would referee seriously;
  1 HIGH + 12 MEDIUM + 16 LOW stalls, plus a vocabulary audit) → triage:
  defect-class fixed in wave 2, voice-class kept. Wave 2: the HIGH —
  "improvement is a ↓" (Prop 4(ii), reads as a typo) and its 8(i) twin,
  both now words; §5 and §6 on-ramps added (both sections cold-opened on
  algebra/notation — the persona's pet peeve, and the paper's own
  "Closing the loop" subsection shows the fix); "tributary" pointed the
  wrong way in the abstract and the §6 title (a tributary FEEDS a river)
  → "sits downstream of", and the title's "labor loop" unified to §1's
  "wage loop", now glossed at first use; waterline was defined only in
  Fig 1's caption — now glossed in §2 prose (w/c); machine parity glossed
  at first use (c·ρ̄); heterogeneity ¶ made plain-statement-first with
  the "cross-sectional shadow" kept as crown; fortification (b)/(c) and
  Prop 6's (ii)/(iii) split to paragraphs (Props 11–12 house pattern);
  7(iii)'s verbless scope fragment given a subject; Prop 10's h → ψ
  (notation collision, registry updated); Fig 5's caption apposition
  disambiguated; Prediction 12 tagged "Machinery in Section 9" (only
  prediction leaning on later machinery); §9 ledger's pre-definition K
  reworded; LVT expanded at first use; §10's unannounced bridge/
  scaffolding swap made explicit ("scaffolding hardens into structure");
  13(i)'s "pair's family" forward-reference dissolved ("at every rate
  t_L"). KEPT against the reader, deliberately: "Technology giveth", the
  "surprise" aside, 1(ii)'s telegraph, "near-empty set", "proviso is
  load-bearing" — summits under the allocation rule. Verification: ALL
  ELEVEN checks green after every wave (3 full runs); 15 props / 15
  remarks / 13 predictions / 7 figures; zero curly; zero ↓; 100,101 →
  101,381 bytes (+1.3%, well under the 1.35× rule). the_link_new.pdf now
  stale (Stella renders). Flagged for a future unit: the ~45-min read
  time — a length cut was outside this unit's mandate.

- 2026-08-06 · Session 3, continued — COMPANION UNIT 5 EXECUTED:
  CROSS-VALIDATION + THE REINSTATEMENT SERIES; ALL DATA UNITS COMPLETE
  (her "go for it"). Reinstatement half: 22 more O*NET archives pulled
  (annual majors 5.1–30.0; old-style through 20.0, text-style after;
  release dates parsed live off db_releases.html — no remembered
  constants), task universes per release, births/deaths per adjacent
  pair in TWO members (Task ID = churn undercount; normalized text =
  rewording-inclusive overcount), matched-occupations restriction.
  Traps caught in-build: cp1252 encoding in the early era; the
  endswith-member match grabbing "Green Task Statements.txt" for
  16.0/23.0/24.0 (tiny-universe artifact, wild fake churn — fixed to
  exact basename, series stabilized). RESULT: mature-era (2012+)
  recorded task births fall ~12 → 0.0 per 1,000/yr, BOTH members; the
  30.0→30.3 pair records zero births across 18,797 tasks; a real 2024
  pruning wave (deaths ~26/1,000). Framed honestly: construction-ramp
  caveat (2003–08 levels reflect database population), trend read
  2012+, the instrument's own drying named part of the finding.
  Friction half: log-share slopes 2015–19 vs 2022–25 (covid excluded)
  × exposure — aggregate gradient ABSENT (low-exposure decelerated
  most; the F gap open three years after the clock's capability
  arrival), instances punctuated (customer service 2.76M: +1.7 → −5.9
  %/yr; translators +5.0 → +0.5; data scientists +45 → +15; data entry
  −6.5 → −9.4). Four sentence guards pin the README claims (zero-births
  latest pair; mature-era falling mean; customer-service flagship; no
  positive gradient). check_crossval.py: 18 checks ALL GREEN. Figure
  collision-checked. NEXT: FIRST PROSE — sections 1–3 of "The Schedule"
  against built results; the companion's data phase is closed.

- 2026-08-06 · Session 3, continued — COMPANION UNIT 4 EXECUTED: FAMILY C,
  THE WEDGE LAYER (her "go for it"). Probes: unionstats frameset resolved
  to per-year xlsx (occ/xls/occ_YYYY.xlsx, 1983–2025 all listed); BLS
  cpsaat49–55 pulled and the by-occupation table identified by its own
  title row (53). Build: pre-period union coverage/membership (1999–2001
  avg — measured at the panel base, no reverse causation) via 1990-basis
  COC → occ1990dd (100% employment mapped); 2025 via census2018 →
  SOC2018 → dd chain (98.2%); CPS-53 licensure at SOC-major resolution
  attached ecologically by employment mix (labeled; hand-verified
  22-entry group table); A&R 40–50% kept as cited anchor only. TESTS
  (direction reported, not gated): T1 unconditional targeting order
  right-signed but weak/rule-sensitive (Spearman −0.10 to −0.18); T2
  the paper-grade result — within the HIGH-ROUTINE tercile the Prop 2
  signature is clean under every rule (early ~19–20% covered vs late
  ~5–14%, Spearman −0.19 to −0.35); T3 fortification glance — licensure
  7–9pp higher among survivors under every rule while union coverage
  converges low (price-form dies with its jobs, quantity-form survives
  — The Link's §4 filter, in data). Two sentence guards added to the
  check so README prose cannot drift from the tables. Economy anchors:
  15.0% coverage 1999–2001 → 11.1% 2025, matching published aggregates;
  operators more unionized than the economy. Figure collision-checked
  (headroom for the n=5 label). check_wedges.py: 24 checks ALL GREEN.
  NEXT: unit 5 — cross-validation (A×B friction gap) + the
  reinstatement series (DOT→O*NET task birth/death), the companion's
  highest-value figure for the parent.

- 2026-08-06 · Session 3, continued — COMPANION UNIT 3 EXECUTED: FAMILY B,
  THE RIGHT TAIL (her "go for it"). Sources resolved by probe (Epoch
  benchmark_data.zip + ai_models.zip hrefs off the /data page; METR
  runs.jsonl under reports/time-horizon-1-1; Eloundou occ_level.csv +
  MIT LICENSE via raw.github; fetch.py gained jsonl/csv/text validation
  kinds). LICENSE FINDING: METR's README references a LICENSE file that
  does not exist in the repo — posture set to Epoch's CC-BY republication
  as primary horizon series, raw runs as attribution-credited validation
  member only; flag carried to the future data note. Build: exposure
  layer (six published variants as the mapping grid, mean-across-codes
  convention from unit 1; covers 100% of 2025 emp); right-tail join
  (survivors vs flipped × exposure; stats banded rules × variants — the
  d50 survivors-more-exposed direction is real and now check-guarded);
  the clock (four dated frontier traces; METR horizon 0.04 min 2019 →
  ~17 h 2026; doubling 5.0 months, band-gated 4–12, stated against
  METR-2024's 7.1 as their own steepening in the longer window); METR
  raw recompute (24,008 runs, weighted per-model logistic in log2
  minutes) matched to Epoch on 15 models rule-based-only (exact +
  unique-prefix preferring Epoch's METR-tagged rows; Airtable id dead
  end discovered and dropped; ambiguity never guessed), log-corr 0.993.
  Defects caught in-build: pandas Series [:, None] indexing; quicksort
  tie instability making cummax order-dependent (deterministic
  date+model+value sort both sides — a reproducibility bug that would
  have bitten replicators); figure collisions (workday label behind
  legend; -0.0 bin label; legend over tallest bar). check_righttail.py:
  23 checks ALL GREEN (variant nesting α≤β≤γ rowwise, join accounting
  vs panel and flips files, frontier running-max per source, doubling
  re-derived from the written CSV, validation floor, stats-cell exact
  recompute, figure). NEXT: unit 4 — family C wedge layer (unionstats +
  BLS licensure + A&R published wedge rents; the Prop 2 targeting-order
  test).

- 2026-08-06 · Session 3, continued — COMPANION UNIT 2 EXECUTED: THE W/C
  GRID + FAMILY A ENVELOPE (her "go for it"). FRED members title-verified
  live before hardcoding (AHETPI 1964–; B935RG3Q086SBEA hedonic computers
  1959–; PCU334111334111 computer PPI 1990-12–; Y033RG3Q086SBEA broad
  equipment 1947–; CES0500000003 probed, rejected — 2006 start doesn't
  span the panel; software index considered, excluded — weak
  machine-rental claim). One sanity-band repair with reason logged
  (hedonic 2025/1999 = 0.286 vs my 0.25 prior — the post-2010 slowdown is
  real; wrong-series pulls sit ≥0.8, catcher intact). Envelope: Lemma 1
  inverted on the unit-1 panel — three labeled flip rules, ρ̃ = w/c(flip
  year) per flipped occupation, era slices 2005/2015/2025, waterline
  density series, telephone operators flip 2004-05 at the 30-47th
  percentile of flipped ranks (tie-aware check after discrete-rho ties
  tripped strict-median; check repaired, anchor substance held). Top
  flipped roster face-valid (data entry, sewing, packers, machinists,
  tellers) with the pre-registered confound VISIBLE and kept: Chief
  Executives (2001 OEWS classification break) and Carpenters (housing
  crash) — documented in README/ledger, nothing hand-dropped. Figure
  collision-checked visually (era labels moved off the title, then off
  the legend). check_envelope.py: 35 checks ALL GREEN (grid construction,
  envelope identity re-derived from CSVs, rule orderings, era
  monotonicity, density integral = 2025 mass, anchors, figure). NEXT:
  unit 3 — family B right tail (Epoch/METR/Eloundou pulls + mapping
  grid).

- 2026-08-06 · Session 3, continued — COMPANION UNIT 1 EXECUTED: THE TASK
  PANEL (her "go for it"; spec defaults stand unvetoed). Built
  `companion/` on the house pipeline pattern (fetch/cache/validate with
  magic-byte checks — a BLS 200-with-HTML-stub taught the lesson early;
  probe-first URLs; BLOCKED-and-stop gates; truststore for ddorn.net's
  incomplete TLS chain, no verification bypass). 46 source files pulled
  live and validated: 11 ddorn (ALM tasks, offshorability, occ crosswalks
  1950-2010, occgroups), O*NET 30.3, 29 OEWS national files 1997-2025
  (real pre-2003 pattern is oesYYnat; oesmYY stubs for those years), 2
  BLS SOC crosswalks, 3 Census code lists. Build iterations caught and
  fixed: 2012+ files stack all aggregation levels (o_group filter; the
  390M-employment triple-count trap); 1999-2000 data hidden behind docs
  sheets/blocks; no 00-0000 row in 1999-2000 (majors-sum denominator);
  census X-wildcards (37-201X janitors, 15-10XX) as a prefix map tier;
  2019+ ownership blocks (string-compare filter). Result: 27-year ×
  326-occupation panel with wages, ALM/O*NET attributes, coverage
  0.91-0.97 vs each file's own total, everything unmapped REPORTED
  (panel_coverage.csv), nothing imputed. check_panel.py: 24 checks ALL
  GREEN (structure, coverage floors, wage skew/level anchors, the
  telephone-operators collapse 299k→38k as a structural gate, ALM
  direction anchors operators-vs-managers). pypdf/xlrd/openpyxl/
  truststore added to venv. NEXT: unit 2 — the w/c grid (FRED IDs
  title-verified) + the family A envelope's first era-sliced figure.

- 2026-08-06 · Session 3 — CARRIED ITEMS CLOSED + COMPANION PAPER SCOPED
  (item 9; her go-ahead). Reconciliation first, per protocol: disk matches
  NOTES at the rewrite state; only new files are Stella's three PDF
  renders — `the_link_new.pdf` verified current via rewrite markers
  (pypdf installed into venv for the check), other two stale, untouched.
  Carried items all closed (PDF hers; closure read clean in place; no
  .tex master — only the derivation record). Then the scoping unit:
  `companion_schedule_spec.md` written — the companion measures the
  schedule ρ̃(x,t) itself (The Link's flagged-empirical premise), three
  identification families (adoption envelope / benchmark right tail /
  wedge layer), rule-grid discipline inherited from the κ program, every
  load-bearing source probed live and reachable (O*NET 30.3 CC-BY;
  ddorn.net AD task measures; OEWS 1997– + 1988–95; Epoch CC-BY updated
  same day; METR runs.jsonl; Eloundou MIT; unionstats live 1983–; BLS
  licensure 2015–), walls excluded and routed (openICPSR → published
  tables; IPUMS → Census API). Bonus identified: DOT→O*NET task
  birth/death = a measured reinstatement series — direct evidence on the
  §9 fork. Veto window in the current verify-list; four open choices
  flagged (title, home, register, worked instance). NO paper prose, NO
  pipeline code — next unit is the task-panel build.

- 2026-08-06 · FIGURES REPAIRED (Stella: text/lines covering text in figs
  1–5). Workflow: 7 visual inspectors on the PNGs → single fixer iterating
  on the figure code with pixel-verified re-renders → 7 fresh-eyes
  verifiers. Initial: 20 collisions across figs 1–6 (the inspectors also
  caught 2 in fig 6 — the κ = 1 dotted line striking through the legend —
  despite its all-clear); fig 7 clean. 18 fixed, layout-only (annotation
  repositioning, fig 3's legend moved outside the axes with taller canvas,
  fig 5's arrow tails shortened, fig 6 legend framealpha) — no word,
  number, or data series changed; 2 deliberately kept (fig 1's leader
  arrows crossing curves en route to targets: intended pointing). Final
  verification: ALL SEVEN CLEAN, captions still matched. Files touched:
  `code/make_figs.py`, `code/feasibility_kappa.py` (one line), figs 1–6
  regenerated. Worth knowing: the collisions were in the Aug 3 renders —
  the fixes add real clearance, robust to font-metric drift across
  environments.
- 2026-08-06 · READABILITY REWRITE EXECUTED AND GATED (no-veto delegation;
  `rewrite_brief.md` = full record; original preserved at
  `the_link_pre_rewrite_snapshot.html`). Method: delete-first — five dense
  regions (fortification remark, decomposition remark + insurance ¶,
  enclosure/mix/K-fork subsections) rewritten by agents given section JOBS
  but never the old prose, each cold-read by the Dr. R. economist persona
  and revised (19 agents); four on-ramp/decompression edit sets (closure,
  feasibility, open economy, Prop 13); abstract diamond-cut (two candidates
  + editor judge — fresh candidate won; judge caught a real error in the
  tightened one) and the five-paragraph STORY INTRO (classical laws
  dormant-not-wrong; AI as candidate reversal, premise flagged empirical;
  the authorship disclosure foregrounded — "the capability priced in this
  paper is the capability that drafted it"; ends on the claim verbatim).
  Rewrites IMPROVED content in passing: "fortified" now defined; output
  cost vs excess burden separated; enclosure billing cap corrected;
  interior-vs-corner mix tension resolved; Rosen (1981) cited + added to
  References. SATISFACTION GATE (20 agents): two full-arc cold reads +
  two claims-fidelity sweeps, findings refute-verified — 12 confirmed,
  4 refuted, all 12 fixed plus 3 elective: SWT language cut to what the
  proof delivers ("delivers what the second welfare theorem promises —
  redistribution without deadweight" — one-parameter family, person-
  specific lump sums named as the missing rest); §4 U-shape reframed
  calibration-not-confirmation matching Prediction 1's tag; Prop 2's FOSD
  step attributed to A&R's conditions (lower-set result is what the proof
  shows); "overidentified" boast replaced (non-substitution theorem:
  cost-determined prices); abstract glosses "the corner" at first use;
  "proof apparatus" → "where humanity can be verified"; Ricardo's 1821
  machinery chapter now IN the intro ("The concession stayed a chapter;
  here it becomes the model"); decomposition wall split into three ¶s;
  Fig 5 caption disambiguated from λ_C; series-windows sentence added to
  the data note; Prop 13 opener carries the base-equivalence qualifier.
  CHECK COVERAGE EXTENDED: D-v derives EB(b) = (φ/2)b² and EB(u) = 0
  (also grounds 10(ii)'s half-square hypothesis); N-vi verifies the
  enclosure take-cap; W-iv relabeled per-period gap. ALL ELEVEN checks
  green; structure 15/15/13/7; zero curly; confirmation agent: 13/13
  fixes verified, no new defects. Arc verdict (Dr. R.): finishes in the
  40 minutes; "I'd referee it seriously, and I'd assign Sections 4 and 6
  to my grad class."

- 2026-08-05 · Session 2, continued — REVIEW PASS (her ask; workflow: five
  review dimensions → refute-biased verifier per finding; 13 agents, ~937k
  tokens, 216 tool calls). RESULT: 8 findings confirmed, 0 refuted, plus 7
  low-severity triaged by hand. All fixed: (1) §9's κ-feedback RATE claim
  was false — the K-term lowers κ's LEVEL at every q but the slope
  comparison crosses at finite q (verifier reproduced numerically) → now
  "sits lower at every q", matching the check; (2) §7's "Propositions 1–8"
  fossil → "the propositions" (the other 1–8, inside Prop 9's statement,
  is content-bearing and stays); (3) Figure 6/7 captions' "Rebuilds from
  code/…" pointers removed (provenance lives in the data note and README);
  (4) THIS FILE was a full unit behind reality — reconciled below;
  (5) item 5's verify-header said Prop 10; fork is 11 — fixed; (6) the
  deflator fork treated half-year 2026 as annual — annualize_complete()
  guard added, series ends at complete-2024, headline 5.1× → 4.8×, paper
  corrected; (7) make_figs.py ended with a hardcoded /home/claude/figs
  listing that crashed replicators — fixed, README's "regenerates all
  paper figures" scoped to Figures 1–5; (8) the empirics spec's status
  line overclaimed — now states implemented members vs open ones
  (Larson/BEA family, SPM/CE bundles, farm rents; "never the sole source"
  unmet on the stock side until Larson lands). Low-severity: superstar
  "one-for-one" → "at rate 1 − 1/n" (the check's own derivative);
  co-presence cite → "(the remark to Proposition 11)"; check_open's
  vacuous Min self-comparison → two-branch test; the ℓ = ℓ₀(1−a) bound now
  asserted in check_baseline_props (was print-only); bare r·T fused to rT
  (7 sites; subscripted keep the dot); τ registry note → appendix;
  verify-list heading refreshed. Final audit: 2 lemmas + 13 propositions,
  15 remarks, 13 predictions, 7 figures, §§1–11 + appendix, zero curly,
  zero archaeology, ELEVEN check files green.
- 2026-08-05 · Session 2, continued — LAST BITS: SMALL REPAIRS + DEFLATOR
  FORK (details in the queue entries above; `checks/check_repairs.py`;
  record `repairs_section.html`). Lemma 2 and the durability
  generalization verified before splicing; Figure 7 drawn from three
  title-verified FRED series.

- 2026-08-05 · Session 2, continued — ITEM 8 EXECUTED AND SPLICED; THE
  NUMBERED QUEUE (1–8) IS COMPLETE. The open-economy page as the new §10
  with Proposition 12 (Trade as the early waterline); welfare bumped to
  §11 / Proposition 13 (one title edit + one header edit; nothing else
  referenced either; records updated). Content: (i) tradable tasks face
  waterline min(c·ρ̃, w_f·ρ̃_f) — the foreign wage is a second machine
  rental; same targeting, earlier timing; wedges are negative altitude in
  both waters (both thresholds ∝ 1/µ); (ii) offshoring is a way-station
  (40 → 35 → 30 instance: home → offshore → machine) — the terminal
  allocation is the closed corner, production where sites/energy/water
  are cheapest; (iii) rents accrue to the producing jurisdiction's land;
  destination VAT reaches the imported land content (T-iv: rents 60 <
  floor 100, VAT at 0.4 bridges), domestic LVT reaches domestic sites
  whoever owns them — the border splits the bases, the mix frontier is
  interior for a second reason, the bridge constitutive for deficit
  consumers. Remark: one waterline at two heights (automation/offshoring
  inseparability); the room shields twice (co-presence blocks ships and
  fakes; terminal K unchanged); migration flagged per-jurisdiction, not
  modeled. Companions: §9 ledger retitled ("Transition dynamics unmodeled
  (and the border, one page)"), Grossman–Rossi-Hansberg (2008) in related
  work + References. `checks/check_open.py` all green (9 checks).
  Structure: 14 props (Lemma 1 + 1–13), 15 remarks, 13 predictions, §§1–11
  + appendix, zero curly; ALL TEN check files green. Record:
  `open_section.html`. NEXT: small-repairs batch + deflator-fork figure.
- 2026-08-05 · Session 2, continued — ITEM 7 EXECUTED AND SPLICED. Welfare
  as the new closing §10, "What the planner would do", Proposition 12
  (The corner welfare theorem) — no renumbering, 12 follows 11 in document
  order. (i) Participation efficiency under u: private rule = social rule
  because the corner wage is the machine-replacement cost (6(i)'s
  cancellation read at the social wage); b/b′ open inefficiency bands of
  width b/b′ burning |c·ρ̄ − s| per hour. (ii) Implementation: incomes
  (1−t_L)·ω_i·rT + t_L·rT/N sum to rT for every t_L, dispersion shrinks
  linearly, equal split at t_L = 1, no margin moved (6i, 7ii) — the
  second welfare theorem with real instruments; land rent as the one true
  lump sum. (iii) Converse: unique up to 10(iii)'s base-equivalence;
  work-conditioned floors fail (i), wage-funded floors fail (ii). Moral
  remark: same technology, two architectures — George floor 2.0 ≥ P_s
  1.9 vs wage-linked floor 0 in the closure world; "the corner is a fork
  between two bookkeeping systems"; Pigouvian companion composes freely
  (boundary kept). Second-best remark: negative-sum adoption band
  (µ−1)·w/γ_L (social margin uses the base wage); production efficiency
  survives the second best (Diamond–Mirrlees 1971, cited and added to
  References); the schedule = the two measured series; Prop 9(iii)'s gap
  = the emergency. Companions: §1 roadmap + abstract one-liners.
  `checks/check_welfare.py` all green (13 checks). Structure: 13 props
  (Lemma 1 + 1–12), 14 remarks, 13 predictions, zero curly; ALL NINE
  check files green. Record: `welfare_section.html`. NEXT: item 8, the
  open-economy page — the queue's last numbered item.
- 2026-08-05 · Session 2, continued — ITEM 2 EXECUTED AND SPLICED. The
  enclosure margin as Proposition 9 ("The commons, priced", §6, between
  feasibility and the mix; mix → 10, Baumol fork → 11 FINAL — three
  in-paper renumber sites + records). Content: (i) the commons is the
  idle margin (reservation rent zero + excess supply), and the corner
  closes it — 5(i)'s land clearing read as endogenous enclosure; (ii)
  s(q) = max(s_0 − q·h_e, s_d), ds/dq = −h_e, enclosure complete at
  finite q_enc = (s_0 − s_d)/h_e — the margins that demolish the wage
  demolish the escape; (iii) the race: κ rises while s falls, gap between
  q_enc and q* iff N > N_crit = q_enc·T/(g_s + q_enc·h_s) (= 60 in the
  closure instance; N = 50 safe, N = 80 gapped) — in the gap the mix's
  instruments are rescue, not optimization. Remark: desperate supply in
  the linked regime (s 25→20 ⇒ n 0.5→0.6, w 30→26 — enclosure
  manufactures workers); 6(i)'s cancellation survives s(q); past q_enc
  the floor is s_d + u — the transfer IS the commons, billed at exactly
  the h_e·q taken, funded from inside the same rT (Prop 8's bundle
  already carries the plot). Companions: §2 pointer, mix intro cites 8
  and 9, Prediction 13 (coresidence/household formation tracks
  rent-to-wage), abstract → thirteen. `checks/check_enclosure.py` all
  green (one sympy Max-limit fix in the check). Structure: 12 props
  (Lemma 1 + 1–11), 12 remarks, 13 predictions, zero curly; ALL EIGHT
  check files green. Registry: s_0, s_d, h_e, q_enc in; reserved list
  now empty. Record: `enclosure_section.html`. NEXT: item 7 (welfare /
  optimal policy).
- 2026-08-05 · Session 2, continued — ITEM 6 EXECUTED AND SPLICED. The mix
  frontier as Proposition 9, in a subsection ("The mix on the way down")
  closing §6 after feasibility; the Baumol fork renumbered 9 → 10 (its
  header + the §9 ledger pointer; records updated). Content: (i) κ ≥ 1 →
  LVT alone, no mix question; (ii) κ < 1 (the measured present) →
  rent-base-first: t_L = 1, t_V = N·P_s·(1−κ)/E, minimized deadweight ∝
  λ_C·(1−κ)² at given floor-to-consumption ratio — the transition cost is
  the product of the paper's two measured series, both moving favorably
  (index 0.32 today at (0.72, 0.33); 0.08 at (0.50, 0.60)); (iii) corner
  coincidence — Prop 5's identity merges the bases and the instruments
  become one. Remark: the VAT's job on the way down is reaching dynamic +
  institutional rents that pay no ground rent; its reach decays by
  construction; weights travel with the regime; frontier interior for the
  whole crossing — the decisions-log knife-edge worry did NOT materialize
  (the only corner solution is the benign κ ≥ 1 region). E chosen for
  consumption to avoid the fork's unit-cost C. `checks/check_mix.py` all
  green (one type slip caught and fixed in the check itself: κ was an
  expression, not a symbol, in a derivative). Structure: 11 props, 11
  remarks, 12 predictions, zero curly; all SEVEN check files green.
  Record: `mix_section.html`. NEXT: item 2 (endogenous s(r), the
  enclosure margin).
- 2026-08-05 · Session 2, continued — CONSISTENCY PASS (her directive:
  timeless voice, walk-through story, appendix triage, figures). Snapshot
  kept at repo root: `the_link_pre_consistency_snapshot.html`. (a) Figures
  fixed: img srcs `figs/` → `../figures/`; all five originals render in
  place, and the κ chart entered as Figure 6. (b) Typography normalized:
  the ORIGINAL paper is straight-quote; the day's splices had introduced
  25 curly apostrophes and 3 curly quote pairs (the "house style = curly"
  inference came from the parallel session's splice, not the original);
  all normalized to straight, zero remain — memory pointer corrected.
  (c) Timeless voice: revision archaeology removed ("from a bookkeeping
  remark into", "now by construction rather than assertion", "the informal
  version left open", "now a theorem", "has treated", "asked") → timeless
  equivalents. (d) Story: §1 gains a closing roadmap sentence (feasibility
  ratio + the priced objection); the abstract gains the κ result
  ("one-third and rising"). (e) Structure: heterogeneous-land,
  corner-above, and base-feeds-back remarks moved to a new "Appendix:
  deferred remarks" with pointers left in place; the measurement remark
  dissolved into §7 as "The remedy, measured" + Figure 6 — theory in §6,
  measurement in §7. Audit: 10 props, 10 remark labels (7 body + 3
  appendix), 12 predictions, 6 figures all loading in the browser, zero
  archaeology phrases, zero curly characters; all six check files re-run
  green (no verified formula touched). Root fragments are pre-pass
  records; the snapshot is the authoritative before-state.
- 2026-08-05 · Session 2, continued — ITEM 5 EXECUTED AND SPLICED. The
  strongest objection, as a theorem: new subsection closing §9 with
  Proposition 9 (the Baumol fork) — (i) Leontief cost concentration
  (labor's share of any K-touching good's cost → 1 as machine costs
  collapse: Baumol derived, not assumed); (ii) the CES fork
  (K-expenditure share → 1 | θ | 0 by η); (iii) the three-way terminal
  split (machine share → 0; land and K-labor split the limit; the K = ∅
  boundary returns the corner exactly) — plus the credence remark
  (π_H ≤ min(φ_H, v·f/(1−v)); price-only enforcement kills the premium
  for every v < 1; terminal K = provenance law + co-presence — the
  fortified set again) and the superstar remark (top share β + (1−β)/n,
  median-to-mean 1−β; aggregate rescue, median demolition) and the
  κ-feedback sentence (a K-service term in P_s slows κ at every q). §9's
  Human-premium ledger block replaced by a pointer, AJJ credit kept;
  Prediction 12 added; abstract count eleven → twelve.
  `checks/check_kset.py` all green (14 checks, incl. the barbell
  instance: labor share 100%, median wage at the floor, K-wage 28.5× the
  floor for 5 of 100 workers). Structure audit: 10 prop divs, 11 remarks,
  12 predictions; all six check files green. Record: `kset_section.html`.
  NEXT: item 6, the LVT/VAT mix frontier (decisions log holds the
  standing frame).
- 2026-08-05 · Session 2, continued — ITEM 3 EMPIRICAL HALF RAN CLEAN.
  Probed and title-verified all FRED IDs before use (three rounds; the Z.1
  market-value real-estate series resolve as HNOREMV and
  BOGZ1LM1x5035005A, structures as BOGZ1LM1x501x665; several first-guess
  mnemonics 404 — verified IDs hard-coded with titles in the script).
  Wrote and ran `code/feasibility_kappa.py` (house pattern: reuses
  lambda_compute2's pull/cache/sanity machinery; 12 series, all validated;
  courtesy-delayed live pulls). Land residuals positive over full ranges
  (household ≈ $22.0T at 2023, economy-wide ≈ $26.7T at 2020, both in the
  literature's range); Orshansky-CPI bundles reproduce published 2023
  thresholds. RESULT: κ(2025) = 0.33 [0.18–0.59], up from ≈0.05 in the
  1950s — κ < 1 across the whole band: the U.S. is in Prop 8's "not yet"
  region, with the secular climb the theorem predicts and rate-cycle noise
  in the z1 members. Outputs: `data/kappa_results.csv`,
  `figures/kappa_coverage.png`; §7 got the κ table row and the data-note
  source clause; README repo-map + reproduction updated; spec stamped
  run-complete. Discovered in passing: the cut-off session had also already
  fixed §7's "Propositions 1–6" → "1–8" (undocumented, correct). Queue
  item 3 fully done; NEXT is item 5.
- 2026-08-05 · Session 2, continued — RECONCILIATION + THREE UNITS LIVE.
  (a) Discovered the cut-off parallel session's work: it had spliced the
  conditionality unit (from the pending fragment, apostrophes house-styled)
  AND built + spliced item 3's theorem half — Proposition 8, coverage ratio
  κ = rT/(N·P_s), with `checks/check_feasibility.py` and the §5 forward-ref
  tightenings — but died before updating NOTES or writing the empirics
  spec. (b) Verified its work independently: check re-run green, derivation
  re-checked by hand (κ algebra, q* threshold, land-constraint identity,
  demand-independence of q), splices inspected in place. One defect found
  and repaired: 8(i) claimed coverage rises "without bound" along ρ̄/ℓ —
  κ is bounded by T/(N·h_s); corrected clause now distinguishes the bounded
  a-margin from the toward-the-ratio margins. (c) Incident: the surviving
  session double-applied conditionality splices B/C before noticing the
  parallel application; duplicates (remark + insurance paragraph, H–R
  reference) removed; audit confirms 8 remarks, 11 predictions, single
  copies. Protocol line 5 added (one live session per repo; reconcile disk
  vs NOTES on start). (d) FORTIFICATION unit executed under the broadened
  delegation: `checks/check_fortification.py` all green (selection/
  distillation monotonicity; blocked-task loss growing toward full labor
  cost; Baumol limit 1|θ|0 by η; punctuated-adoption threshold g1 =
  m0/(µw − F), delay increasing in F, gap at adoption exactly F) — spliced
  as Prop 2 proviso + §4 remark + amended Prediction 2 + upgraded §9
  ledger sentence (record: `fortification_section.html`). (e) Wrote
  `feasibility_empirics_spec.md` (the cut-off session's dangling
  reference), land-value blocker dissolved via rule grid. All four check
  files green at session end. the_link.pdf now three units stale.
- 2026-08-05 · Session 2, continued — ITEM 4 DRAFTED. Substitution/income
  decomposition of conditionality, verified in
  `checks/check_conditionality.py` (all green): the (m_w, m_e)/Δ
  decomposition — u is the unique Δ = 0 instrument, compensated response
  zero identically, dR/du = s′ income-only; b is full-strength substitution
  (dR/db = −1); b′ is substitution plus income, reinforcing (dR/db′ =
  1 + s′) — the symmetric corner burn |c·ρ̄ − s| for misplaced
  participation in either direction (running-example numbers: 7 make-work
  at s = 25, 3 income-effect exit at s = 15, 0 at the boundary s = 18);
  the linked-regime direction (exit raises the wage: 30 → 34 in the sloped
  instance, k = 0 pins it — so u's residual accrues to workers); and
  coverage by state (work-conditioned claims pay zero in the loss state;
  u's disposable income continuous at the regime boundary). Drafted
  `conditionality_section.html`: one sentence into 6(i)'s statement, the
  decomposition remark + insurance paragraph after Prop 6's proof, and the
  Hoynes–Rothstein (2019, Annual Review of Economics 11) reference entry.
  NOT spliced — the verify-list gates it. Next per sequencing: item 3
  (feasibility theorem; the land-value-series decision blocks only its
  empirical half).
- 2026-08-05 · Session 2, continued — SPLICE EXECUTED after full sign-off.
  `link-repo/paper/the_link.html` now carries the closure subsection at the
  end of §5 (replacing the "Conservation of rents" paragraph; its Rognlie
  sentence preserved in the migration paragraph) as Proposition 5, with the
  Prop 4(ii) erratum patch and the 4(iii) proof micro-patch applied, and
  Conditionality/Funding renumbered to 6/7. Seven cross-reference sites
  updated — the six planned plus one caught by the post-splice audit (the
  Funding proof's "plus (5i)"). Check-file labels updated to post-splice
  numbering; both checks re-run green. Prop numbers in older entries below
  are pre-splice. the_link.pdf is now stale relative to the HTML
  (regeneration on the verify-list, with the figs/ path note).
- 2026-08-05 · Session 2. Stella added the source to `link-repo/`: the paper
  (HTML + rendered PDF), the §7 pipeline (`code/`), computed results
  (`data/`), figures, and docs (formal notes; the self-commissioned referee
  report, whose revisions are already in the draft — note the draft also
  renumbered props relative to that report). Cross-checked session 1 against
  the actual paper: Prop 4(ii)'s faulty clause is present verbatim
  ("diverges along every margin … a → 1"; the a → 1 limit is 0 — erratum
  confirmed against source); the splice target ("Conservation of rents"
  paragraph, end of §5) exists; the notation registry matches; all reserved
  symbols are unused in the paper. Key finding: the paper's source is HTML —
  no .tex anywhere — so the closure section was converted to the paper's
  idiom: `closure_section.html` (splice-ready; splice instructions, the
  renumbering site list, and the erratum patch in its header/body; the .tex
  stays as derivation record). Moved both check scripts into `checks/` so
  this file's paths are true; installed sympy into the venv (it was
  missing); both check files pass locally, all green. New loose end caught:
  Prop 4(iii)'s proof clause "tends to zero as machines improve" — optional
  micro-patch added to the verify-list. Also noted: the_link.html points its
  <img> tags at `figs/` but the repo stores figures in `figures/`, so the
  HTML shows broken images opened in place — matters only when regenerating
  the PDF. No paper files were modified; the splice waits on the verify-list.
- 2026-08-05 · Session 1 of the revision phase. Built the `checks/` harness
  and ran the existing draft's algebra through it — Props 3, 4(i), 4(iii),
  6(i), Lemma 1, the running example, Prop 2's targeting order, Fig 3's
  terminal numbers, Prop 5(ii)'s burn rate: all pass. Caught one genuine
  erratum: Prop 4(ii)'s a→1 margin anti-diverges. Derived, verified, and
  drafted Proposition C (closure); wrote this file.
