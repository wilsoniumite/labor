# Six-profile review synthesis — pinning.html, 2026-08-13

Six independent reviewers (task-literature referee, search-macro referee,
empirics referee, cold reader, copy/notation auditor, adversarial theorist)
read the full paper. Their raw reports are in the session transcripts; this
file is the deduplicated, verified synthesis. Items marked [verified] were
checked by Claude against the file or the algebra before entering this
document; items marked [plausible] await a check before any fix enters the
paper.

## Overall verdict (convergent)

The algebra holds everywhere — three reviewers independently recomputed the
worked instances and the empirics referee matched every headline number to
the built CSVs (fork 4.79x, kappa 0.326 [0.179–0.589], ceiling median
1.2574 with exactly 13/32 below one, lambda_C 0.7181 [0.662–0.808]).
The task-literature referee's verdict: revise-and-resubmit at a top FIELD
journal now; top-five only after the structural repairs. The search referee:
the paper is "close enough to the literature to be judged by its standards,
not yet inside it" — and its two ideas are "the kind the search literature
would rather steal than ignore." The exposure is not arithmetic; it is
LIMIT HYGIENE (parity conflated with unbounded superiority), COMPOSITION
(the lambda>0 pieces verified as algebra but never composed into an
equilibrium), and a handful of UNSOURCED LOAD-BEARING CLAIMS.

## The two structural wounds (Tier 0 — direction needed before drafting)

W1. PARITY IS NOT SUPERIORITY [verified]. The terminal-income corollary
("capability uniform and lambda->0 ... wages have left the list") is
contradicted by Prop 4(i) (w/p_g = 1/Lbar > 0 at parity), Prop 1(ii)
(everyone willing works at the pinned wage), and Appendix D's own
labor-still-present addendum. With F.3's own parameters the "full limit"
carries a ~47% wage share (N·c·rho_bar = 90r vs rT = 100r). The conflation
propagates: the intro's "falls without bound" at "rough parity"; Section
8's "once wages are gone"; F.5's "at the limit the bases merge"; the
abstract's identity language. REPAIR DIRECTION (recommended): add the
missing hypothesis (rho_bar -> 0, or full exit s > c·rho_bar) wherever the
identity is claimed, and let parity keep its positive wage floor — this is
philosophically ALIGNED with the paper: the squeeze was always the fork,
not a zero wage. The retreat costs the necessity rhetoric some urgency and
makes the actual thesis cleaner.

W2. THE COMMONS CANNOT COEXIST WITH THE RECURSION AS WRITTEN [verified].
Setting r = 0 (open idle margin) in c = ac + lambda·w + l·r with w =
c·rho(x*) forces 1 - a - lambda·rho(x*) = 0: the viability condition is
"r > 0" in disguise, so Prop 3(i)'s free-exit regime and Prop 2's priced
machine sector are mutually exclusive in the homogeneous-quality-unit
model the text states ("pays the same q per quality unit as any other").
REPAIR DIRECTION (recommended): Ricardian differential rents — exit
happens at the zero-rent marginal quality while production sites earn
schedule rents (Appendix D's heterogeneous-parcels remark already contains
the structure); restate Prop 3(i) accordingly, state "recursion viable ⇔
production land priced" as a lemma, and drop or qualify the single-q
parcel-by-parcel language. Touches Prop 3, s(q)'s q, and the enclosure
narrative; the limit results are untouched.

## Repairs that STRENGTHEN the thesis (Tier 1a — do these with relish)

S1. Section 6's "which dominates is a parameter question" is false balance
[plausible — check-gate the derivative signs]: in the closed system the
two channels are ONE signed movement (higher q lowers the real wage in
goods and against the bundle a fortiori; "the nominal wage" is not an
object in a moneyless model). The replacement is a sharper theorem.
Relatedly [verified] the Section 4 60%-cut instance is a w/r statement and
lacks the "this arithmetic is nominal" flag its Section 3 twin carries.

S2. "We supply both endpoints" (Section 2.2 crown + abstract) is the one
sentence a search economist falsifies from memory [verified against DMP]:
the framework endogenizes both endpoint VALUES; what it leaves unpriced
are PRIMITIVES (z, beta, the productivity process). The accurate claim is
stronger: we price the interval's LOCATION; frictions set its width;
bargaining picks the point. Same repair fixes "it supplies none of the
three" (wrong on two of three).

S3. Section 2.3's "the machine rental enters as a parameter" is false for
A&R 2018 and Zeira (accumulation closes it into time preference)
[verified]. The true contrast is the TERMINAL CLAIMANT: their recursion
ends in the discount rate with no land and a fixed machine relative
price; ours ends in non-produced factors with lambda as a measured dial.
Stating it correctly removes the referee's easiest kill.

S4. Section 6 "the interval closes when the schedule flattens" conflates
determinacy with crossing [two independent reviewers]: flattening pins
the wage (kills slope-dependent statics and upward institutions);
closure requires the ceiling to CROSS the priced floor — which is what
Figure 5 actually shows (18 < 25). Split the claim; both halves are true
and the mechanism reads better.

## Genuine gaps to fill (Tier 1b — small new content, some check-gated)

G1. UNSOURCED LOAD-BEARING CLAIMS (unanimous / near-unanimous):
   (a) "the task-birth series ... has been drying for a decade" — no
   source; engage Autor–Chin–Salomons–Seegmiller (QJE 2024, verify live)
   and/or point at the companion's O*NET reinstatement series; or hedge.
   (b) "the climbing shelter share of low-income budgets" — asserted 3x,
   sourced 0x, and it is the paper's ENTIRE live case for eta<1 (CEX
   citation or one-panel figure; the cheapest major repair).
G2. "Thin interest" is an adjective where a bound is needed (2 reviewers):
   derive the steady-state interest/rent split in the delta>0 closure or
   demote to an empirical question. Check-gated.
G3. lambda>0 flat-regime taxonomy [verified as a real gap]: machine-sector
   labor demand lambda·X is inelastic, so Prop 1(ii)'s "regardless of how
   many or few workers" fails at lambda>0, and at s > c·rho_bar the
   machine sector still hires at w = s (Figure 5's ordering and Appendix
   B's removal ordering are lambda=0 statements). State results at
   lambda=0 exactly; add the lambda>0 branches as a lemma.
G4. Prop 5(ii)/(iii) fixed-price absolutes: "w − s is untouched" and "no
   margin moved at any point on the path" fail under the price changes
   the transfer itself induces (the paper's own Appendix D feedback
   remark); "zero substitution wedge / zero deadweight" survives. Restate;
   index R by tau. Abstract inherits one softening.
G5. Appendix A: full-system uniqueness is claimed in Section 6 and not
   proven; the production-land monotonicity claim has the wrong sign
   component; the flat-stretch employment selection ("nothing riding on
   it") decides exactly the Attack-1 identity. Downgrade honestly or
   close the sloped GE properly (unit).
G6. "The fiscal base that survives" — definite article proven only
   against wages; free entry in machine services is a load-bearing scope
   condition (IP on the recursion's produced inputs would terminate it
   partly in law). Wording: "the non-elective base" + one scope sentence.
   Plus the assessment-problem sentence (2 reviewers).
G7. Section 5 mapping to the z-debate: s(q) prices the participation
   margin, not the spell-margin flow value (rent nets out of the
   employment/unemployment comparison to first order); add the mapping
   paragraph, fix the HM attribution ("requires", not "for exactly this
   reason"), instrument exit at bottom-quartile/marginal rents, add the
   transfers-gross qualifier (sharpens prediction 13 for free), and a
   sentence on s_d's own rent exposure.
G8. Empirics disclosure batch [all verified against CSVs]: Figure 7's
   caption and IN-FIGURE annotation are false against four_way_split.csv
   (borrowed_med = 0 in 1960, 1963, 1999, 2000; NOT 1998) — caption fix
   now, figure regeneration as a unit, and the same bug exists in the
   LONG DRAFT's Figure 5 (flag to link-repo); window is 1960–2025 not
   1962–2025; kappa's 2021–25 grid loses the four z1_econ members
   (restore the dropped "business-structure coverage ends in 2020"
   disclosure; consider a constant-subgrid robustness line); "one-third
   AND RISING" overstates the post-1988 plateau-with-cycles (2 reviewers;
   soften to endpoint + cycle acknowledgment); lambda_R has a band in the
   build ([0.638–0.729]) — print it; conditionality row needs a
   construction line; deadweight 0.32 is the rounded-inputs value
   (unrounded gives 0.33 — state the convention); the two 0.72s (lambda_C
   vs the figure's within-slice wage share) need one disambiguating
   clause; durables-leg hedonics caveat (cold reader's drafted sentence);
   zoning needs the cross-sectional fork named as a FOURTH assembly
   (WRLURI x Saiz slopes; land-vs-structure decomposition of the shelter
   leg); incidence assembly needs the epsilon_S caveat.
G9. Cold-reader clarity batch: the "close/shut" verb fix in 2.3; the
   pre-industrial "same flat geometry at opposite levels, opposite walls
   binding" sentence (rescues the abstract's last line); the
   l = l0(1-a) motivation clause and the l->0 intuition clause;
   the kappa-ceiling sentence decompressed; F.4's q_enc = 1.5 primitives
   stated (pick a clean triple, add to check_pinning).
G10. Copy/notation batch [all verified]: define phi_H, rho_f, t, Y; fix
   the tau parcel-dummy collision (App D dummy -> z); eta double-duty
   note; s_h/h_s note; mu domain (mu > 0); lambda_R prose definition;
   Sec 2.1 forward-notation note; p_g declaration; Lbar wording ("the
   inverse of absolute solo productivity"); s_i subscript; Fig 4 caption
   gloss; Sec 10 matrix pointer/bolding; x*(n), s(y), gamma_L glosses.
   Cross-refs: "Section 10 lists the test" -> Section 11; "Section 4's
   results" -> "this section's results"; Figure 3 "panels" -> one panel,
   two series. Prose: abstract dangler + tense; "drying up"; "cannot
   hold durably"; the 60–90% garden path; the Delta miscount ("three
   instruments", not "three failure modes at three values"); double
   colons x2; Baumol-fork disambiguation; wage-linked harmonize; number
   style; max() spacing; dead style attribute. References: Marx 1867
   entry or recast; Baumol 1967 entry (verify live) or attribute via
   AJJ; Diamond initials; Polanyi publisher; Rognlie season/pages
   (verify); "Capital Is Back"; the 18 page-range gaps (live-verify
   batch — deliberate omissions to date, now worth completing).

## New-work proposals surfaced by the review (Tier 2 — Stella's call)

P1. "The fundamental surplus, priced" — a two-page subsection embedding
   the walls in a DMP wrapper: FS ≈ c·rho*(lambda, q) − s(q). Converts
   HM's z/y ≈ 0.955 from calibration to prediction; implies a TRENDING
   Shimer elasticity (testable; assembly (1) half-covers it). The search
   referee's assessment: this is the difference between being cited by
   that literature and being presented in it.
P2. The general-technology fork theorem: state the boundedness hypothesis
   (land content of final output bounded away from zero; substitution
   at-or-below one on the land margin inside machine production), prove
   which divergence margins survive, restate Prop 4/corollary under it.
   The referee's Demand 1; the adversary's Attack 8.
P3. Sloped-regime GE closure (demand side beyond the flat limit), full
   existence/uniqueness or honest multiplicity (the enclosure spiral as
   a possible trap equilibrium is ON-THEME).
P4. Reinstatement race model (birth rate of high-rho tasks vs flattening
   rate) — turns the paper's bet into a parameter.
P5. Figure 7 regeneration (annotation correction) + upstream long-draft
   erratum note in link-repo NOTES.
P6. Citation additions to verify live if adopted: Autor–Chin–Salomons–
   Seegmiller 2024; Chodorow-Reich–Karabarbounis 2016; Costain–Reiter
   2008; Baumol 1967; a CEX shelter-share source; Davis–Heathcote land
   share (for the shelter-leg decomposition).

## What the review did NOT find

No arithmetic errors anywhere (三 independent recomputations); no
orphaned references; no coined-term regressions; no figure/caption
mismatches beyond Figure 7's annotation; the register held (the cold
reader's quote-to-a-colleague pick was the Section 7 crown, and the
verification note "bought a lot of trust"). The Ljungqvist–Sargent
quotation and the Shimer numbers are verbatim-faithful.
