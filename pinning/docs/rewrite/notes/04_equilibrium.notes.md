# Part 04: Section 4, Equilibrium (sec:equilibrium). Notes

Fragment: `SP/build/parts/04_equilibrium.tex`. Built from design synthesis §3.1 without its "What is easy and
what is hard" paragraph, with the authors' text wherever its content carries over, fix F5 applied to
Theorem 1, the sentence after it, its remark and Lemma 1's remark, and the two citations the brief places
here (Restrepo 2025; Korinek and Stiglitz 2019).

Test compile (`SP/build/work/04/test.tex`, main.tex 1-40 with synthesis §2.0's theorem block, the
graphicspath line, the fragment): `latexmk -pdf -interaction=nonstopmode -halt-on-error` exits 0, 7 pages,
no LaTeX errors, no overfull or underfull boxes, no warnings other than the 16 undefined references to labels
defined in other parts (listed in (a)). Both figure files resolve.

Check of the port: `SP/build/work/04/check_verbatim.py` (run with `python3 -B`) confirms that every passage
marked verbatim occurs word for word in main.tex (whitespace normalized), 41 of 41.

Order of the section:
- Head sentence (L136, edited), then 4.1 Prices: Lemma 1 and remark; L155-157; Figure 1; Proposition 1, its
  proof and remark; the loom (L195); Restrepo (2025) with L229; Proposition 2, its proof and remark; L245;
  L251; L253, (6), L257; Figure 2.
- 4.2 Participation and the labor market: Proposition 3 with (9)-(10), its proof and remark; L294; L296;
  L268's last sentence with L298 and the Korinek and Stiglitz sentence; L300; L304's first sentence with the
  (11) paragraph and L322.
- 4.3 Existence and uniqueness: Lemma 2 and remark; its gloss; L687-708 with (21)-(24); Theorem 1 with (25);
  the proof sentence; the remark; Corollary 1 and remark.

## (a) Labels

**Defined here (23):**
- Sections: `sec:equilibrium`, `sec:prices`, `sec:participation`, `sec:existence`.
- Results: `lem:prices`, `prop:1`, `prop:2`, `prop:3`, `lem:ceiling`, `thm:1`, `cor:statics`.
- Equations: `eq:5`, `eq:6`, `eq:9`, `eq:10`, `eq:11`, `eq:21`, `eq:22`, `eq:23`, `eq:24`, `eq:25`.
- Figures: `fig:1`, `fig:2`.

**Referenced here and defined in other parts (12; these are the 16 undefined references of the test compile):**

| Label | What it must be | Expected part |
|---|---|---|
| `sec:economy` | Section 3, Definition of equilibrium | 03 |
| `ass:tasks` | Assumption 1 | 03 |
| `def:equilibrium` | Definition 1 (cited twice, both times as "Definition 1(i)") | 03 |
| `def:automation` | Definition 3 | 03 |
| `eq:tildem` | the closed-form price coefficients of a machine-hour | 03 |
| `sec:example` | Section 7, the numerical economy (the brief's label; the design wrote `sec:instance`) | 07 |
| `app:proofs` | Appendix A (cited twice) | A |
| `lem:owner` | Lemma A.1, the owner's problem | A |
| `app:networks` | Appendix B.1 | B |
| `prop:network` | Proposition B.1 | B |
| `app:D.1` | Appendix D.1, conditionality (cited twice) | D |
| `app:D.3` | Appendix D.3, the coverage ratio | D |

Labels defined here and referenced elsewhere in the design: `prop:1`-`prop:3` (Sections 5 and 6, Appendix
A), `thm:1` and `eq:24`, `eq:25` (Section 7's path), `lem:ceiling` (Section 3's Assumption 2 gloss),
`lem:prices`, `cor:statics`, `eq:5`, `eq:21`-`eq:24` (Appendix A), `fig:1` (Section 3).

I pointed Proposition 3's remark at `app:D.1` in place of the design's `app:fiscal`, so this part uses only
labels the brief says stay (`app:D.x`). If Appendix D is labeled `app:fiscal`, nothing here depends on it.

## (b) Every edit to the authors' text, with old and new

Edits allowed by the brief (cross-references, Table 1 renames, the minimum math change):

1. **L136, sentence 2 (opens the section).** This edit follows Stella's decision that proofs of Propositions
   1-3 stand in the text (D10).
   - Old: "Proofs of the main price and participation results are collected in Appendix~\ref{app:A.2}."
   - New: "Proofs of the main price and participation results are given in the text; the other proofs are
     collected in Appendix~\ref{app:proofs}."
2. **L627 (Proposition 1's proof), last sentence.** Cross-reference.
   - Old: "...; Appendix~\ref{app:B} supplies a complete interior example under stated conditions."
   - New: "...; Section~\ref{sec:example} supplies a complete interior example under stated conditions."
3. **L242 (Proposition 2's last sentence).** Table 1 rename. The design dropped this clause; restored (D6).
   - Old: "Holding the other total requirements fixed, the wage--rent ratio rises..."
   - New: "Holding the other price coefficients fixed, the wage--rent ratio rises..."
4. **L631 (Proposition 2's proof).** Cross-references, plus the design's clause, since positivity is now a
   conclusion. The display and "both positive." are verbatim.
   - Old: "Substitute $w=p_m\gamma(x^*)$ into the machine-service row to obtain
     $p_m(1-\gamma(x^*)\widetilde{\lambda}_m)=r\widetilde{b}_m$. The conditional derivatives are"
   - New: "Substitute $w=p_m\gamma(x^*)$ (Proposition~\ref{prop:1}) into the machine-service row of
     Lemma~\ref{lem:prices}(i), $p_m=w\widetilde\lambda_m+r\widetilde b_m$, to obtain
     $p_m(1-\gamma(x^*)\widetilde{\lambda}_m)=r\widetilde{b}_m$. Since $p_m>0$ and $r\widetilde b_m>0$, the
     feedback term is positive, and solving gives~\eqref{eq:5}. The conditional derivatives are"
5. **L251, sentence 1.** Cross-reference. The two channels' definitions (L249) now stand in Section 3.
   - Old: "...either channel lowers the wage supported by a given rent."
   - New: "...either channel (Definition~\ref{def:automation}) lowers the wage supported by a given rent."
6. **L257, sentence 1.** The minimum math change for durable machines (design §1.3: "When ρ = 0"). With
   ρ > 0, the price coefficient also carries the return on the machines. Sentence 2 is verbatim (D4).
   - Old: "The service price is then accounted for by its embodied claim on the non-produced input."
   - New: "When $\rho=0$, the service price is then accounted for by its embodied claim on the non-produced
     input."
7. **L296, sentence 3.** Cross-reference. The old Appendix B example is now Section 7's numerical economy.
   - Old: "Appendix~\ref{app:B} gives a fully funded household example, ..."
   - New: "Section~\ref{sec:example} gives a fully funded household example, ..."
8. **L128 (Korinek and Stiglitz), as the brief prescribes.** The rest of L128 is not used here.
   - Old: "...through dependence and exit; Korinek and Suh (2024) is ..."
   - New: "...through dependence and exit."
9. **L322, sentence 3.** Cross-references (D11).
   - Old: "Appendix~\ref{app:B} constructs the household budgets and proves existence and uniqueness under
     explicit funding conditions."
   - New: "Section~\ref{sec:economy} constructs the household budgets, and Theorem~\ref{thm:1} proves
     existence and uniqueness under explicit funding conditions."
10. **(24), L703-707.** Table 1 rename: $n_D$, $n_S$ become $N_D$, $N_S$.

Edits that come with the design's restated results. I kept these because the stated economy needs them for
correctness; the provenance comments say so.

11. **Proposition 1 (L186-193).**
    - (i), old: "At an interior machine-contestable task margin, $w=p_m\gamma(x^*)$."
    - (i), new: "In an equilibrium with $w>0$ and $p_m>0$: (i) at an interior margin, $w=p_m\gamma(x^*)$; at a
      boundary assignment, $w\ge p_m\gamma(x_H)$; at a corner, $w\le p_m\gamma(0)$."
    - (ii): "movement of the margin changes the wage" becomes "movement of an interior margin changes the
      wage". Its second sentence is verbatim.
    - (iii) is removed (see (c)).
12. **Proposition 1's proof (L627).** (i) is replaced by the design's proof (the old one asserted
    indifference at every boundary, Open 12i). (ii) is verbatim (D7).
13. **Proposition 2 (L231-243).**
    - Old: "At an active contestable margin with $r>0$, suppose $\gamma(x^*)>0$, $\widetilde{b}_m>0$, and
      $1-\gamma(x^*)\widetilde{\lambda}_m>0$. The conditions $w=p_m\gamma(x^*)$ and
      $p_m=w\widetilde{\lambda}_m+r\widetilde{b}_m$ imply (5)."
    - New: "In every equilibrium with an interior margin and $r>0$, the feedback term
      $1-\gamma(x^*)\widetilde\lambda_m$ is positive and (5), with $\widetilde\lambda_m$ and $\widetilde b_m$
      given by~\eqref{eq:tildem}."
    - (5) ends in a comma, not a period.
14. **L245, sentences 2-4.** Sentence 1 is verbatim (D5).
    - Sentence 2, old: "At the margin, $\gamma(x^*)\widetilde{\lambda}_m$ is the labor share of machine-service
      cost."
    - Sentence 2, new: "At the margin, $\gamma(x^*)\widetilde\lambda_m=w\widetilde\lambda_m/p_m$ is the part of
      the machine-hour's price that resolves into wages, including the return on the wages advanced to build
      machines; when $\rho=0$ it is labor's share of machine-service cost."
    - Sentence 3: "this share" becomes "it".
    - Sentence 4: "...also determine $x^*$ and the selected recipes." becomes "...also determine $x^*$
      (Theorem~\ref{thm:1})."
15. **Proposition 3 (L284-292).** The authors' "work is optimal ... exactly when" is kept over the design's
    "prefers work" (D2), and the last sentence (L291) is verbatim.
    - Old: "Suppose $P_s>0$ and the supported basket remains available in both states. Under (8), work is
      optimal exactly when (9)."
    - New: "In every equilibrium with $\tau_w=d=g_w=g_e=0$, work is optimal for a worker with cost of work
      $\chi$ exactly when (9), and employment is (10)."
    - (9) ends in a comma, not a period.
16. **Proposition 3's proof (L640).** Sentences 1-2 are verbatim. Sentence 3 and (18) are replaced by "For
    $\chi>0$, $\partial s/\partial P_s=e^\chi-1>0$. Workers with $w=s$ have measure zero because $F$ is
    continuous, which gives~\eqref{eq:10}." The design cuts (18).
17. **L317 is restated as the (11) paragraph** (see (c)): "If $r>0$, the owner rents out all its land, so by
    Lemma~\ref{lem:prices}(ii) the economy produces $T/B_s$ baskets and employs $TL_s/B_s$ hours. With
    Proposition~\ref{prop:3}, labor-market clearing is". (11) itself, L318-321, is verbatim.
18. **L687, sentences 1-2, are restated as Lemma 2 and its gloss.** The ceiling is no longer called "closed".
    - Old: "Tasks at which $(\rho+\delta)(a+\lambda\gamma(x))\ge1$ are closed to machines at every wage: the
      machine services that would replace an hour there cost more than the hour, because building them takes
      labor and machine services of their own. Let $x_c$ be the first such task, or $x_c=1$ if there is
      none."
    - New: Lemma 2, then "Machines cannot perform the tasks in $H$. At a task in $[x_c,x_H]$ they can, but the
      machine-hours that would replace an hour there embody at least that hour of labor, counting the labor
      needed to build them at the required return, so they cost at least the hour at any wage. Unlike $H$, the
      ceiling depends on the labor in the machine chain and on the return, as well as on capability."
19. **L708, sentence 2.** The design's note, which defines $N_S(x_c)$ as the limit (math check C4 needs this
    reading of (25)).
    - Old: "As $x$ rises to $x_c<1$, $v$ and $P_s$ grow without bound while $v/P_s$ tends to
      $\gamma(x_c)/[\gamma(x_c)(1-x_c)+J(x_c)]$; $n_S(x_c)$ denotes the corresponding limit."
    - New: "As $x$ rises to $x_c$, $N_S(x)$ tends to a limit, which we write $N_S(x_c)$. If the ceiling binds
      before $H$, $v$ and $P_s$ grow without bound while $v/P_s$ tends to
      $\gamma(x_c)/[\gamma(x_c)(1-x_c)+J(x_c)]$."
20. **Lemma B.1 (L719-726) is restated as Theorem 1.**
    - Old: "...Then there is a unique interior threshold ... If the provider's rent and interest cover the
      support there, $T+\rho V_mX\ge NP_s$, the prices and quantities in (21)-(24) give a competitive
      equilibrium with the promised support fully funded."
    - New: "Then every equilibrium has $w>0$, $r>0$, and an interior margin, at the unique $x^*\in(0,x_c)$
      with $N_D(x^*)=N_S(x^*)$. Up to the choice of numeraire and sets of tasks of measure zero, its prices
      are (21)-(22) and its quantities (23)-(24) at $x^*$. An equilibrium exists if and only if the owner's
      income covers the support there, $rT+\rho V_mX\ge NP_s$."
21. **Corollary 1.** (i) restates L324 sentence 1 and L729-734 and adds the equilibrium rate. (ii) restates
    L743 (and L324 sentence 2).

Where the design's draft re-voiced an authors' sentence without a need of correctness, I restored the
authors' words:
- L253: "full machine-service chain" (the design wrote "machine chain").
- L257, sentence 2: verbatim (the design wrote "Institutional rents introduce further income components"
  and lengthened sentence 1).
- L294-300: verbatim, per the brief. The design had merged L268, L298 and L300, dropped L298's second
  sentence, and inserted L124's Lewis sentence.
- L627 (ii): verbatim (the design rewrote it with $\gamma_L=1$ and $N_Y$).
- L631 and its display (the design inlined them).
- L640, sentences 1-2 (the design wrote "Exit gives utility zero, and work gives ...").
- L285's "work is optimal".
- L242's "Holding the other ... fixed".

Edits to the design's own text, with reasons:
- **Lemma 1's remark: "at the user cost" added (F5).** The price coefficients rest on Definition 1(i)'s
  user-cost clause.
- **Proposition 2's remark: "any production network" becomes "any production network of Appendix B.1"
  (F1).** The closure needs Assumption B.1 as F1 restricts it.
- **Proposition 3's remark: pointer `app:D.1`.** Appendix D.1 derives the reservation wage with payments
  (L779-787).
- **The sentence after Theorem 1: "and the user cost" added (F5).** The proof excludes a zero rent, and every
  return but ρ, through the clause.
- **Theorem 1's remark: two sentences added (F5).** "Its uniqueness rests on the clause of Definition 1(i)
  that machine-hours rent at the user cost. When support absorbs all the owner's income, its first-order
  condition (Lemma A.1) does not bind, and the clause selects the user cost at ρ." The second is F5's plain
  sentence. Nothing in this section says the clause "costs nothing"; the design's claim was only in its
  notes (synthesis.md 584-587, 1183).
- **Lemma 2: a new remark (the brief asks for one after each result).** "Lemma 2 compares unit costs at the
  user cost. It does not depend on preferences or on the labor market."

## (c) Every sentence of the authors' text in this section's range that is dropped, with its line

Range: the lines the design maps to this section (155-195, 227-324, 626-644, 687-743, with 136).

**Dropped:**
- L136, s1: "The model connects task assignment, production costs, and participation through a common price
  system." The design gives it no home; Section 3 opens with the primitives sentence.
- L192, Proposition 1(iii): "A worker supplies the market hour only if its wage reaches the reservation value
  $s$." The design removes it; Proposition 3 states participation.
- L627, (i): "At the boundary between human and machine assignment, continuity and cost minimization give
  $w/\gamma_L(x^*)=p_m/\gamma_M(x^*)$." It is false at a corner (Open 12i) and is replaced.
- L627: "(iii) is the participation condition." Dropped with Proposition 1(iii).
- L232, s1-2: "At an active contestable margin with $r>0$, suppose ... The conditions ... imply". Restated
  (item 13).
- L245, s2: "At the margin, $\gamma(x^*)\widetilde{\lambda}_m$ is the labor share of machine-service cost."
  Restated (item 14).
- L268, s1: "A person who declines paid work still needs somewhere to live, food, energy, and care." The
  design places it nowhere; the introduction's L76 says the same.
- L285: "Suppose $P_s>0$ and the supported basket remains available in both states." and "Under (8),". Both
  are now in Definition 1 and the worker's budget.
- L304, s3: "Aggregating Section~\ref{sec:4}'s choice gives employed hours". Replaced by Proposition 3's "and
  employment is".
- L308, both sentences: "In the flow benchmark, the production network prices the basket through its total
  human hours ... so $P_s=wL_s+rB_s$. With durable machines, $P_s$ also pays interest on the machines that
  supply the basket (Appendix~\ref{app:B})." Restated as Lemma 1(i) and (iii).
- L317, all three sentences: "For a transparent equilibrium, suppose all households consume in the basket's
  proportions, support is fully funded, and the endowment $T$ is fully used at $r>0$. With $B_s>0$, total
  production supports $T/B_s$ baskets and requires $TL_s/B_s$ human hours. Labor-market clearing is
  therefore". Restated (item 17); the assumptions are now derived.
- L640, s3 with (18): "Holding the supported basket and preferences fixed, differentiation along a change in
  rents gives $ds/dr=(e^\chi-1)dP_s/dr$." The design cuts (18).
- L687, s1-2: restated as Lemma 2 (item 18).
- L708, s2: restated (item 19).
- L710-717, all but the last sentence: the three-row system and the passage on the two coefficient sets
  ("These equations are a three-row instance ..." to "...and $P_s=wL_s+rB_s$ as in Section~\ref{sec:5}.").
  Replaced by Section 3's four-row system (eq:3, eq:4) and Lemma 1.
- L717, last sentence: "Structures and maintenance could enter the space-service row through their own
  input requirements." The design gives it no home. It could go after Section 3's eq:3 or in Appendix B.2.
- L719-726: restated as Theorem 1 (item 20).
- L743, all three sentences: restated as Corollary 1(ii).
- Headings dropped for the structure: L227 "Closing the replacement price", L247 "Two margins of
  automation", L266 "The outside option: pricing exit", L302 "Replacement meets participation".

**Placed by other parts, not dropped from the paper:**
- L251, s3: "Actual technological changes may alter several coefficients and move the margin together." The
  design places it, edited ("at once"), at the end of Section 3's AI paragraph.
- L249: Section 3 (Definition 3 and the loom).
- L268, s2-s5: Section 3 (the owner). L268, s6, "The parents may themselves finance that support from
  wages.": Section 6 (437).
- L270-282: Section 3 (workers).
- L304, s2: Section 3 (Assumption 4).
- L310-315 (Figure 3) and L324, s3-s7: Section 7. The brief's "the statics (324)" is there. L324, s1-s2 are
  restated as Corollary 1 here, so Section 7 should not print them again.
- L326: Sections 9.1 and B.4.
- L728-741: Appendix A.
- L745-747: Section 7.

## (d) Decisions for Stella (one word each)

1. Theorem 1's remark: also disclose that, without the clause, Section 7's instance has a second configuration
   (return 0.192, owner consuming nothing, land partly idle at zero rent)? (yes/no)
2. Proposition 3: the authors' "work is optimal ... exactly when", over the design's "prefers work"? (yes)
3. L253: the authors' "full machine-service chain", over the design's "machine chain"? (yes)
4. L257: only "When ρ = 0," added and the authors' second sentence kept, over the design's rewording? (yes)
5. L245, sentence 4: drop "and the selected recipes" for a pointer to Theorem 1, as the design does? (yes)
6. Proposition 2: restore "Holding the other total requirements fixed" (as "price coefficients"), which the
   design dropped? (yes)
7. Proposition 1's proof (ii): the authors' L627 verbatim, with $\gamma_L$, over the design's $\gamma_L=1$ form?
   (yes)
8. L294-300 verbatim, without the design's insertion of L124's Lewis sentence? (yes)
9. L155-157 (the "replacement value" the loom uses), placed before Proposition 1? (yes)
10. L136's proof pointer, edited, as Section 4's opening sentence? (yes)
11. L322's last sentence with two pointers, over the design's "funding is necessary and sufficient"? (yes)
12. Lemma 2: the new remark on what it does not depend on? (yes)
13. Theorem 1: "sets of tasks and of workers of measure zero", to cover the workers indifferent between work
    and exit (math check C4, condition 3)? (yes/no)
14. Proposition 2's remark: "any production network of Appendix B.1", the scope after F1? (yes)
15. Restrepo (2025): after Proposition 1 and the loom, leading into Proposition 2? (yes)
16. Korinek and Stiglitz (2019): at the end of the dependence paragraph (L298)? (yes)
17. Figure 1's float in Section 4, as the brief says, though Section 3 cites it first? (yes)

## (e) Citations

| Citation | Where | In main.tex's references | In the brief's §5 new list |
|---|---|---|---|
| Restrepo (2025) | 4.1, after Proposition 1 and the loom | no | yes (NBER w34423). Wording checked against SP/rq/txt/w34423.txt line 53, "(iv) wages converge to the opportunity cost of computational resources required to reproduce human work" |
| Korinek and Stiglitz (2019) | 4.2, end of the L298 paragraph | yes (main.tex 952) | no |
| Marx (1867) | 4.2, L300 | yes (960) | no |
| Lewis (1954) | 4.2, L300 | yes (956) | no |
| Polanyi (1944) | 4.2, L300 | yes (966) | no |

No `\cite`; plain "Author (year)", as in main.tex. Allen (2001), which the design's outline places in 4.2,
is not cited: the brief drops it.

## (f) What I did not do, and why

- **Trammell and Korinek (2026) is not placed here.** The brief's §5 allows Section 3's AI paragraph or this
  section's two-margins passage at (6), and my task named only Restrepo and Korinek and Stiglitz. If Section 3
  does not carry it, the brief's sentence fits after the paragraph on (6) (main.tex L257).
- **Possible duplicates with other parts, for the merge:**
  - F5's plain sentence, if Section 3 also adds it beside Definition 1. Then this remark can keep only "Its
    uniqueness rests on the clause of Definition 1(i) that machine-hours rent at the user cost."
  - L155-157, if Section 3 keeps them after Definition 1(i).
  - L136, sentence 2, if another part uses it.
  - Corollary 1 against L324, sentences 1-2, if Section 7 ports L324 whole.
- **Math check C4, condition 3, is not applied.** "Up to null sets" in Theorem 1 does not name the indifferent
  workers. The statement claims uniqueness of prices and of the aggregates (23)-(24) only, so it is not
  false; decision 13 asks.
- **Fix F4 (Lemma A.1(a) at β = 1) is consistent here.** The (11) paragraph says "If $r>0$, the owner rents out
  all its land". That holds for the constant plans of Definition 1(iii) at every β, which is what F4 keeps.
- **Section 7's label.** I used `sec:example` (the brief), not the design's `sec:instance`.
- **Numbers.** None is printed beyond main.tex's own ($80, $20, $16 in the loom; $\widetilde b_m=1$ in Figure 2's
  caption). The design's 0.567 and 0.456 appear only in a source comment.
