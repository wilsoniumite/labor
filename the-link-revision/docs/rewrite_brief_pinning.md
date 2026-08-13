# Rewrite brief — "Pinning the Wage to Scarcity and Technology"

Frozen 2026-08-13 after two discussion turns (structure approved verbatim by
Stella; her words: "Alright, I like it"). This file is the context lifeboat
for the rewrite unit: if a session dies mid-write, the next session works
from here plus STATE.md.

## Decisions (Stella's, this thread)

1. **One paper.** Long is acceptable; structure carries it: core first, all
   necessary parts, then implications and data, then a long appendix. The
   fiscal arc beyond the welfare pair is the sequel paper.
2. **λ in.** The machine recursion is c = ac + λw + ℓr (labor still inside
   machine production). Task automation (ρ*↓) and recursive automation (λ↓)
   are separated throughout.
3. **Title:** "Pinning the Wage to Scarcity and Technology" (hers).
   Subtitle: "Replacement, exit, and the rents of non-produced inputs in a
   task economy."
4. **Coined terms removed.** No "link", "waterline", "demolition",
   "fortification", "corner" (→ "flat-capability limit"), "George pair".
   ONE term of art allowed for the headline observable: the real-wage fork
   (aka deflator fork). "Terminal input" allowed informally, defined once;
   propositions say "non-produced input".
5. **Wedges to the appendix.** Main text runs on ρ(x), not ρ̃. µ, deflation,
   targeting (credited A&R 2026), U-shape, negative-sum accounting,
   price-vs-quantity protection: all Appendix B.
6. **Acknowledgements carry verbatim** (her three paragraphs).
7. **Checks:** new λ-algebra checked in sympy BEFORE splicing (Claude's
   call, allowed by her "unless you really feel you want to do a check").
   Full Lean extension deferred until after writing (her instruction).
   Lean scope stated exactly in the verification note: corner spine only.
8. **§10 measurement (Claude's call, delegated):** fork + κ figures carried
   (built, checked); incidence assembly and λ input–output first look
   flagged [spec'd, unbuilt] in pinning.html's .unver style — building them
   sloppily inside the rewrite turn would violate the data rules.
9. **Voice:** plain declarative register; the question opens the paper.
   First-person origin material lives in back matter, not §1. Compact
   AI-disclosure paragraph stays in §1 (load-bearing for honesty).

## Structure (approved)

Main text ~9,000 words, ±10%:

1. Introduction (~900) — the question; the answer in one paragraph (two
   closures, both endpoints priced in the same scarcity market); the
   flat-capability limit as organizing device; inherited-vs-own paragraph
   (the de-coining move); disclosure + verification note; roadmap.
2. What standing accounts pin the wage to (~1,100) — marginal product (an
   instance, not a rival; Uzawa one sentence; capital-measurement one
   sentence); search/bargaining (fundamental surplus; WE SUPPLY BOTH
   ENDPOINTS — crown positioning, not compressed); task models (ancestor;
   c and s taken as given; reinstatement closed, defended later);
   institutional accounts = theories of µ (Appendix B); classical accounts
   (Lewis, Polanyi → §5); contemporary automation lit one paragraph; three
   measurement hooks (shares, long record, incidence).
3. The model: tasks and the margin (~700) — primitives; Prop 1 w = cρ(x*)
   (inherited, A&R mapping); level/slope statics unnamed; participation
   floor; pointers to Appendices A, B.
4. The ceiling: what prices the machine (~950) — recursion (Leontief/Sraffa
   lineage); Prop 2 replacement closure c = ℓr/(1−a−λρ*), w = ρ*ℓr/(1−a−λρ*),
   viability 1−a−λρ* > 0; two automation channels; λ→0 limit; terminal
   inputs defined operationally + horizon honesty; ideas/Romer one
   paragraph; matrix form → Appendix C.
5. The floor: what prices exit (~1,000; longest model section — the paper's
   own) — outside option as consumption problem (Hagedorn–Manovskii,
   Mas–Pallais); s(q) = max(s₀ − q·h_e, s_d); idle margin = commons;
   trigger is land scarcity NOT machine parity (fires in the sloped
   regime); Prop 3 priced exit (supply out, wage weakly down, participation
   weakly up); enclosure manufactures labor supply — one event, two
   ledgers; Lewis and Polanyi in body; modern commons = family + transfers,
   stated as the case.
6. The interval, closed (~500) — r enters demand via c and supply via s;
   channels can oppose on the nominal wage, the interval's LOCATION
   migrates onto scarcity unambiguously; flattening kills the inside
   accounts' comparative statics; heterogeneity type-by-type; fixed point →
   Appendix A.
7. The flat-capability limit: the real-wage fork (~900) — Prop 4:
   (i) w/p_g = 1/L̄ (Caselli–Manning conceded); (ii) r/p_g =
   (1−a−λρ̄)/(ℓρ̄L̄), rising as λ↓, ρ̄↓, diverging ρ̄→0, ℓ→0, bounded under
   ℓ = ℓ₀(1−a−λρ̄)-type recipe substitution (state λ=0 case if cleaner);
   (iii) w/P falls iff σ > 0. Corollary terminal income (full limit λ→0);
   closure identity → Appendix E pointer; CES dial → Appendix F pointer.
8. The fiscal completion (~900) — R = Σ r_j T_j; Prop 5 limit welfare
   theorem (efficiency; no participation wedge, with the two-sentence
   conditionality contrast folded in + Hoynes–Rothstein + Jones–Marinescu
   honest distinction; spans inherited→equal at zero deadweight; Arrow;
   Arnott–Stiglitz relation stated); wage-funded contrast one sentence →
   Appendix G; George one sentence.
9. History as three configurations (~800) — pre-industrial (Bouscasse et
   al.); industrial (Crafts; joint prediction: wage's escape and land's
   exit are one event); post-industrial (ALM, Autor–Dorn carry the dating).
10. Measurement (~1,000) — fork figure (carried); κ figure + ceiling caveat
    sentence (FMR grid); incidence assembly [spec'd, unbuilt]; λ
    input–output first look [spec'd, unbuilt]; zoning rival met in one
    paragraph (cross-sectional discriminating content).
11. What would falsify this (~500) — five kill conditions tied to the
    closures; stabilizers granted (reinstatement, K-set → Appendix H,
    reservation, supply expansion, substitution).
12. AI implications + conclusion (~700) — both margins move at once; the
    finding: the same price that lowers the wage and erodes exit raises the
    replacement base — necessity and feasibility climb together; κ today;
    sequel pointed at; the empirical question restated.

Back matter: References (new entries live-verified or .unver-tagged) ·
Data & computation (narrowed) · Verification note (Lean corner spine
exactly; sympy the rest) · AI-use note · Acknowledgements (verbatim).

Appendix (~5–6k words):
A. Assignment equilibrium — existence/uniqueness; flat stretches;
   participation resolution; heterogeneous types; the (w,c,x*) joint
   monotone argument given r, and the four-price fixed point.
B. Institutional wedges and directed adoption — µ, ρ̃ = ρ/µ, targeting
   as lower set (A&R 2026), U-shape signature, negative-sum accounting,
   price-form vs quantity-form protection, subsidy mirror.
C. The machine sector in general form — c = Ac + Λw + Br; spectral
   condition; multiple terminal factors; durability/time preference;
   marginal substitute selection.
D. The enclosure race — q_enc; race vs feasibility threshold; desperate
   supply; the funding circle.
E. The land-only closure — Cobb–Douglas; T_H = σT; income = rT identity;
   demand-side price recovery; heterogeneous parcels; corner-above.
F. CES consumption — s_h(q); η thresholds; fork as estimate of η.
G. The fiscal system in the sloped regime — conditionality decomposition
   (Δ = m_w − m_e); funding + incidence dial; LVT/VAT mix, deadweight
   ∝ λ_C(1−κ)²; κ algebra + grid + ceiling; scissors table. Sequel pointer.
H. Human-essential tasks — Baumol fork compressed; credence bound;
   superstar split.
I. The open economy — half page: foreign wage as second machine rental;
   way-station; border splits bases.
J. Prediction register — the numbered predictions with tags and status.

## Register rules (carried from the readability arc)

- SPEAK AS THE AUTHOR (added 2026-08-13, from her contribution-paragraph
  edits): (1) stage directions deleted — no sentence whose only content
  is what the following text will do or how to read it ("should be
  stated against", "deserves a theorem, and gets one", "Three
  placements.", provenance asides like "compressed from the long
  draft"); navigation proper (the roadmap, section overview sentences)
  stays; (2) when a frame sentence is deleted its anchor folds inline
  ("in this paper", "here") so every sentence self-grounds; (3)
  authorial acts take the first person plural — contribution claims,
  modeling bets, judgment calls are "we/our", unhedged ("Our
  contribution is", not "What is new here, to the author's knowledge");
  math-register imperatives ("Write any transfer as...", "Call an input
  terminal...") stay; "this paper" stays as plain grammatical subject;
  "the author" stays ONLY where the human-vs-AI distinction is the
  content (disclosure, AI-use note, draftline).

- ASSERT FORWARD (added 2026-08-13, from her sentence pair — "the two
  prices that condition takes as given" vs the preferred "two prices
  around that margin"): (1) new information is asserted as new —
  indefinite article, local anchor — never presupposed by a definite
  noun phrase that characterizes it; (2) one job per sentence —
  positioning claims ("...treats as parameters", "...takes as given")
  get their own sentence, usually in §2, never a restrictive clause
  inside an announcement; (3) right-branching syntax — subject, verb,
  object, then the colon-list; no noun phrase held open by stacked
  clauses; (4) colons and semicolons for structure; em-dashes only for
  true parentheticals and lists; (5) nouns carry their domain ("market
  exit", not "exit" where the domain is inferable only from context);
  (6) no meta-commentary on the paper's own rhetoric. EXEMPT: the
  rationed crowns, about one per section, listed in STATE — they are
  voice, not drift, and they go only on Stella's word.

- ONE TEMPERATURE (added 2026-08-13, after the drift diagnosis): body prose
  holds the rewrite's cool setpoint; captions are procedural-informative at
  one temperature across main text and appendix; no working-notes idiom
  inside the paper (status carried by the sentence, not by tags).
  Provenance rule: any prose carried from the long draft is RE-VOICED to
  the setpoint, never pasted with its cadence — pasted captions were how
  the drift got in.

- Every technical claim stated plainly before any compressed form.
- Words before algebra at each section opening.
- Proofs inline, short; heavy derivations to appendix.
- No coined terms per decision 4. Inherited results credited by name in
  the sentence that uses them.
- House HTML style (the_link.html CSS), straight quotes only, <html
  lang="en">, alt text on every figure.

## Source documents

- `link-repo/paper/the_link.html` — the finished long draft; appendix
  content compresses FROM it; its checked numbers carry.
- `the-link-revision/paper/snapshots/pinning_skeleton_snapshot.html` —
  Stella's skeleton (the §2 survey design and scaffold jobs).
- ChatGPT draft (Downloads, what_pins_the_wage_draft_v3_cited.html) —
  frame source for §§4–8; its DOIs unverified; its OECD number dropped.
- `the-link-revision/STATE.md` — thread state; κ-ceiling numbers (log 9a).
