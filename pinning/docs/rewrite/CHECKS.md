# Checks of the rewrite

Two rounds, no ranking. Round 1 checked the assembled rewrite; its fixes, with the defaults for the build's
mechanical decisions (D6, D7, D25, D30, D73, D74, D76, D91, D101-D103, D106), were applied by
`tools/apply_defaults.py` and `tools/apply_findings.py`. Every edit leaves a `% Review edit (<id>)` comment in
`paper/main_rewrite.tex`. Round 2 verified those edits adversarially and read the paper a second time; its
fixes are `tools/apply_round2.py`. Round 3 read the model sections and proofs a third time.

## Round 1

### Math, Sections 3-4 and their proofs

- **mathA-1** (imprecision; REWRITE L337 (Section 3.2, sentence after display (unitcost))). This sentence says, without condition, that the user cost is the owner's first-order condition and that a machine 'must earn' rho V_m. Lemma A.1(c) derives the user cost from owner optimality only when c_o>0 and X>0. The F5 sentences at L475, L855 and L1541 say the condition does not bind when c_o=0. So this sentence, a fourth statement of the F5 point, contradicts the other three as written.
  - Fix: `the owner's first-order condition (Lemma~\ref{lem:owner}).` -> `the owner's first-order condition whenever it consumes and holds machines (Lemma~\ref{lem:owner}(c)).`
  - Disposition: applied.
- **mathA-2** (imprecision; REWRITE L1541 (remark after Lemma A.1)). The remark says that at c_o=0 'the constant plan is the owner's only feasible plan'. This is false in the case that motivates the remark. In the zero-rent configuration (verdicts C4/C5: r=0, land partly idle, return 0.192), the owner can vary l_t freely at r=0 without changing its consumption or stock, so other feasible plans exist. What the shortfall argument proves is that no feasible plan has different consumption or a different stock. The conclusion, that the first-order condition does not bind, is unaffected.
  - Fix: `the constant plan is the owner's only feasible plan, since any departure from it leaves` -> `the owner has no feasible plan with other consumption or stock, since any such departure leaves`
  - Disposition: applied.
- **mathA-3** (imprecision; REWRITE L376 (Section 3.2, last sentence of the cost-system paragraph)). The sentence says that the physical hours and land services per unit of each good, (I-A_0)^{-1}lambda and (I-A_0)^{-1}b, are no larger than the price coefficients, and cites Lemma 1. Lemma 1(iii) states and proves the comparison only for the basket (lt_s >= L_s, bt_s >= B_s). The comparison for every good is stated in Proposition B.1(a): A_0 <= A_rho entrywise, so the Neumann series compare term by term. The pointer lands on a weaker statement than the sentence claims.
  - Fix: `are no larger than the price coefficients (Lemma~\ref{lem:prices}).` -> `are no larger than the price coefficients (Lemma~\ref{lem:prices}(iii) for the basket; Proposition~\ref{prop:network}(a) for every good).`
  - Disposition: applied.
- **mathA-4** (cosmetic; REWRITE L639 (proof of Proposition 1(ii); from main.tex L627, verbatim)). The symbol N_F is used (dN_F/dx*, dw/dN_F) but never defined: it is not in the text and not in Table 1. The sentence before it names 'final-task labor demand' but does not attach the symbol to it. main.tex L627 has the same gap. The design (synthesis §3.1) had defined it as N_Y = Y(1-x*), but the rewrite keeps the authors' wording. The smallest fix inserts the symbol into the authors' sentence.
  - Fix: `final-task labor demand is $Y\int_{x^*}^1dx/\gamma_L(x)$` -> `final-task labor demand is $N_F=Y\int_{x^*}^1dx/\gamma_L(x)$`
  - Disposition: applied (one symbol added to the authors' sentence).

Passed (21):

- Assumption 2's condition (rho+delta)(a+lambda gamma(0))<1 is equivalent to (rho+delta)a<1 together with gamma(0) lt_m<1, as L308 says.
- (unitcost), (3), (4), (tildem): the spectral radius of A_rho is sqrt((rho+delta)a) and the machine rows give tildem; z'(4) gives P_s, lt_s and bt_s as in Lemma 1(i).
- Matrix form of Definition 1(v): (I-A_0')y = Cz, lambda'y = N_a, b'y = l with y=(Y,X,delta X,hY) reproduces the four clearing conditions.
- Walras identity after Definition 1: the three budgets with (govbudget) sum to P_s C = wN_a + r l + rho V_m X, for any policy, and Proposition 5 states the matching identity.
- Worker budget and (8); owner budgets (ownerseq)/(ownerbudget) at a constant stock and the user cost; (govbudget).
- F5: Definition 1(i) keeps the user-cost clause; c_o>=0 is kept and nothing requires c_o>0; 'costs nothing' appears neither in the tex outside comments nor in the PDF; Lemma A.1(c) gives the clause as the FOC when c_o>0 and X>0; the three F5 sentences (L475, L855, L1541) agree in substance with each other and with the math (at c_o=0, owner optimality gives only a positive net return).
- F4: Lemma A.1(a) reads as BRIEF §4 asks; its proof covers beta<1 for every plan and beta=1 for constant plans; Theorem 1's proof and L475 use only the constant plan.
- Lemma A.1(b) proof: the telescoped present-value bound with beta(1+rho)=1 and Jensen (beta<1); the average bound and limsup (beta=1); covers c_o=0.
- Lemma A.1(c) proof: two-period deviations for beta<1, permanent deviations for beta=1, feasible because c_o>0 and X>0.
- Lemma 1 (i)-(iii) and its proof, including P_s = wL_s + rB_s + rho V_m X/Y (checked numerically to 4e-18 on three economies).
- Proposition 1(i) proof covers the interior, boundary and corner cases; (ii)'s chain rule is correct.
- Proposition 2 and proof: the feedback term is positive from p_m>0 and r bt_m>0; the derivatives are correct.
- Proposition 3 and proof (ties have measure zero because F is continuous; the statement holds for either sigma).
- Lemma 2 and proof: the identity p_m gamma - w = [(rho+delta)br gamma - wD]/(1-(rho+delta)a), and the r=0, w=0 and H cases.
- (21)-(24) and the N_S(x_c) limit, including the ratio v/P_s -> gamma(x_c)/[gamma(x_c)(1-x_c)+J(x_c)] when the ceiling binds.
- Theorem 1 proof, first paragraph: N_D strictly decreasing below x_c (uses rho>=0); p'(x) and d(v/P_s)/dx formulas (verified numerically); one crossing.
- Theorem 1 exclusion proof: w=0; r=0 (lambda=0 with H empty or not; equality at the economic ceiling and strict inequality at the wall); corner; margin at the ceiling; wall boundary. Existence via Lemma A.1(b) and the income identity; necessity of funding via (ownerbudget).
- Theorem 1 covers beta=1/rho=0, c_o=0 (weak inequality) and H empty or nonempty.
- Corollary 1(i): dv/dx = p_m gamma'/[r(1-gamma lt_m)] and 1/(1-gamma lt_m) = 1+lambda v/b (numerically 0.857044 and 2.30768 on the instance); (ii)'s monotone comparative statics.
- Cross-references in scope land correctly: sec:owner, sec:government, sec:participation, sec:rent, app:D, app:D.1, app:D.3, sec:technology, app:networks, prop:5, prop:network (B.1(b) needs bt_m>0, i.e. a non-produced input in the machine chain), def:automation, fig:1, fig:2, sec:example, sec:economy, app:proofs, lem:owner (prints Lemma A.1), app:E.
- Table 1 entries match the text for every symbol used in scope except N_F (finding mathA-4).

Not checked:

- Cross-references already listed in ASSEMBLY §5/§7: the wedge remark's pointer to sec:history (D76), app:ideas (D109), Theorem 1's null-set wording (D25), and the triple printing of F5 (D30, D78, Problem 2).
- Section 2, the introduction and Sections 5-10, except where an in-scope sentence points into them (Proposition 5, Proposition B.1, D.1, D.3).
- Prose that is not a statement or proof (the loom, the enclosure paragraph, the AI paragraph), checked only for symbols and pointers.
- Appendix A proofs of Propositions 4-6 and Corollaries 2-3 (outside this scope).
- The C4/C5 equilibrium-enumeration scripts were not rerun. The formulas were checked independently in /tmp/claude-0/-home-user-labor/904c7da5-c8e1-5390-ac85-b6fa3b59f016/scratchpad/build/checks/mathA/num_check.py (report: /tmp/claude-0/-home-user-labor/904c7da5-c8e1-5390-ac85-b6fa3b59f016/scratchpad/build/checks/mathA/report.md).

### Math, Sections 5-6 and Appendices

- **mathB-1** (imprecision; REWRITE L1884 (Appendix B.6, sentence after (20)); bears on (20) at L1880-1883). After the design's decision that H is closed by capability or by rule, a human-required task may be reserved by rule with gamma_Mi > 0, so gamma_i is finite there. On such a task the min in (20) is below one whenever gamma_i(x) < gamma(x*), and (20) prices the reserved task at machine cost. The sentence 'The minimum is one on human-required tasks' is then false, and (20) misprices goods with reserved tasks.
  - Fix: `The minimum is one on human-required tasks.` -> `The minimum is taken to be one on human-required tasks, including tasks reserved by rule.`
  - Disposition: applied.
- **mathB-2** (imprecision; REWRITE L1915 (Appendix C, fourth sentence)). The pointer lands on the wrong object. Proposition 4 now states only the stated economy's final-good bound (w/p >= 1, i.e. lambda-bar = 1). The bound for a good with a feasible human method with general bounded lambda-bar_0 and b-bar_0 = 0, which gives r/p >= 1/[(w/r)lambda-bar_0], is (13), in the remark after Proposition 4, proved in Proposition B.1(c). Appendix C's CES economy departs from Assumption 4, so Proposition 4's 'every equilibrium' does not cover it either. (13) needs only the cost side, condition (i).
  - Fix: `Proposition~\ref{prop:4} gives $r/p\ge1/[(w/r)\bar\lambda_0]$` -> `\eqref{eq:13} gives $r/p\ge1/[(w/r)\bar\lambda_0]$`
  - Disposition: applied (same as R01).
- **mathB-3** (imprecision; REWRITE L998 (Section 5.2, last sentence of the L393 paragraph)). The sentence names conditions that Corollary 2 no longer has. main.tex's corollary required 'one basket remains funded in work and exit' for (14). The rewrite drops that clause, since funding is part of Definition 1, and conditions (14) on F fixed and g_w <= g_e. 'The funded-support conditions for (14)' therefore points at nothing in Corollary 2.
  - Fix: `When the funded-support conditions for \eqref{eq:14} also hold` -> `When the conditions for \eqref{eq:14} also hold`
  - Disposition: applied (same as R03).
- **mathB-4** (cosmetic; REWRITE L1036 and L1042-1044 (Proposition 6), against L1059). R first appears in the text in Proposition 6(iii), but the text defines it only 17 lines later ('with $R=rT>0$', L1059). main.tex defined R at L399, which the rewrite replaced by Proposition 6's first sentence. Only Table 1 defines R before its first use.
  - Fix: `pay $d=\tau_RrT/N$ to every worker` -> `pay $d=\tau_RR/N$ to every worker, where $R=rT$ is the rent,`
  - Disposition: applied, reworded: R is defined in the statement's first clause ("the rental value of land, $R=rT$").
- **mathB-5** (cosmetic; REWRITE L1608 (proof of Proposition 4)). The proof uses lambda~_g, which is defined nowhere. Proposition 4 defines only b~_g = b~_m J(x*), and Lemma 1 defines the basket's lambda~_s, not the final good's.
  - Fix: `because $\widetilde\lambda_g\ge0$` -> `because $\widetilde\lambda_g=1-x^*+\widetilde\lambda_mJ(x^*)\ge0$`
  - Disposition: applied in R14's wording.
- **mathB-6** (cosmetic; REWRITE L1751 (Appendix B.1, the authors' L221)). This is a stale unsubscripted input matrix. Everywhere else the rewrite writes A_rho for prices and A_0 for quantities: Section 3, Table 1, B.2's display (L1828) and Appendix F (L2133, where the authors' A was changed to A_rho for the same reason). Plain bold A is never defined. Relatedly, (2) at L1744 holds for the machine-hour's row only if a_mK is read as rho+delta, which L1760 states after the fact. That bears on D86 (porting the general cost recursion).
  - Fix: `Automation can therefore change $\mathbf{A}$, $\bm{\lambda}$, and $\mathbf{b}$` -> `Automation can therefore change $\mathbf{A}_\rho$, $\bm{\lambda}$, and $\mathbf{b}$`
  - Disposition: applied.

Passed (19):

- Proposition 4 (L893-900) and its proof (L1606-1608): p <= w because p_m gamma <= w below x*; p >= r b~_g; space costs r; b~_g > 0 when machines perform some tasks. Matches SYN §3.2.
- Remark after Proposition 4 and (13): agree with Proposition B.1(c) and its fixed-point proof on the human chain (L1795-1803); lambda-bar = 1 and b-bar = 0 for the final good.
- Corollary 2 (L934-945) and its proof (L1610-1624): r > 0 from p_m(1 - gamma lambda~_m) = r b~_m >= xi p_m; w/r <= gamma b~_m/xi; P_s >= r B_s >= h r. Participation: 1 + w/P_s minus the work ratio equals [P_s(g_e - g_w) + tau_w w P_s + w(d + g_e)]/[P_s(P_s + d + g_e)] >= 0 when g_w <= g_e. Matches SYN Claim 2.
- F2 (L951): the general bound N_a/N >= F(log[1 + theta P_s/(P_s + d + g_e)]) is derived correctly (the threshold is log[1 + (theta P_s + (1 - tau_w)w)/(P_s + d + g_e)]) and reduces to F(log(1 + theta)) at d = g_e = 0. No necessity is claimed.
- Proposition 5 with (income) (L969-979) and its proof (L1627-1657): (I - A_0^T)y = Yz checked entry by entry; A_rho - A_0 = rho e_m e_K^T gives rho V_m X; l = T at r > 0 via Lemma A.1(a) on the constant plan; the r = 0 case is trivial. F3 is applied ('equality if rho = 0 and, when N_a > 0, only if rho = 0'), and the converse is proved: the X = 0 and w = 0 cases at r > 0 are excluded step by step, and V_m >= br > 0.
- Section 5.2: 0.55/0.13/0.32 and the bound 0.81 recomputed (0.5505, 0.1277, 0.3218, 0.8117). The rho = 0 remark lists five statements, and its F3 clause 'when N_a>0' is present.
- Proposition 6 (L1035-1047), its remark and its proof (L1663-1665): (iii) holds with Nd = tau_R R; (i) holds via Lemma A.1(a) on the constant plan (F4-consistent).
- (16) under public provision (sigma = 0) against (govbudget); 'at rho = 0 every equilibrium has kappa >= 1' from (ownerbudget); rent covers 0.3848 of support in the instance.
- Corollary 3 (L1087-1095) and its proof (L1678-1684): kappa = T/(N b~_s) with P_s = r b~_s; N b~_s <= T implies N B_s <= T, with equality of the coefficients at rho = 0; wage-tax revenue/(N P_s) <= (w/r)/B_s.
- F6 several-input line (L1106): derived independently. With rho = 0, lambda~_s = 0 and every positive-rent input fully used, kappa = Y/N = min_k T_k/(N B_{s,k}), so full capture funds one basket per person iff N B_{s,k} <= T_k for all k. Consistent with B.2 (T = B^T y, unused inputs at zero rent, b~_s = B~^T z, P_s = w lambda~_s + r^T b~_s).
- F6 durable line (L1106): recomputed by importing code/appendix_b.py read-only (PRINTED, lambda = 0, x = 1). Rent alone gives T/(N b~_s) = 0.659369 (0.66); rent plus interest gives (T + rho V_m X)/(N P_s) = 1.707153 = T/(N B_s) (1.71).
- Lilies aside (L1111): identical to BRIEF §6.
- Section 7 statements: x_c = 1 at lambda = 0 with H empty; (25) holds (N_D(1) = 0 < N_S; T > Nh); p_m = pi r; v <= eta pi; P_s <= (eta pi + h) r since gamma_eta <= eta and J_eta(x*) <= eta x*; rent-alone threshold (T - Nh)/(N pi) = 0.11916; X <= eta T/[h(1 - a delta)]; R/I -> 1; participation -> 0 through (24) with P_s >= h at r = 1.
- F1 (Assumption B.1, L1736): the relabeled open tasks form an interval with gamma_i continuous. Checked that gamma_i(x_i*) = w/p_m then holds at every interior margin, including with ties, with x_i* defined as the essential supremum.
- Definition B.1 (C1 net-rental repair), Proposition B.1(a)-(f) and its proof: (a) Neumann series and A_0 <= A_rho; (b) the b~_m > 0 role; (c) the human-chain iteration; (d) P_s >= r B_s by (a); (e) the gap formula with p_K; (f) Corollary 3 with p_K.
- B.2: the closure with B~_{mk} r_k, the identity I = w N_a + r^T T + rho p_K X, and the b~_s vector; B.3-B.5 pointers; B.6's uniform-capability paragraph and the bound p_i >= r b_i.
- Appendix D.3 on the price coefficients: kappa = T/(N[lambda~_s(w/r) + b~_s]); N B_s <= T is necessary, and strict slack is needed when L_s > 0 and w > 0. D.1: (27) follows from its displayed comparison; the tau_w = d omission is D106, with no new evidence.
- Renames: no \bar L, m_w, m_e, n_D, n_S left outside comments; the CES weight is omega in Appendix C; g_w and g_e are used in D.1 and Section 6; A_0 and A_rho are used in the Proposition 5 and Corollary 3 proofs, B.2 and Appendix F (one exception, finding mathB-6).
- Every \ref and \eqref in L878-1131, L1142-1260, L1512-1888 and L1901-2140 resolves, and each target says what the sentence claims, except finding mathB-2.

Not checked:

- The numbers printed in Section 7 (scope was statements only); the Section 5.2 and Section 6 numbers and the F6 numbers were recomputed.
- Lemma A.1, Theorem 1's proof, Lemmas 1-2 and Corollary 1's proof in Appendix A: outside the assigned proofs.
- Edge case: the rho = 0 remark's 'basket price equals w L_s + r B_s only when rho = 0' can fail at an r = 0, lambda = 0 equilibrium with H nonempty (V_m = 0) under a wage-funded public basket. Not reported, because it is outside Theorem 1 and needs a policy-funded zero-rent configuration that was not constructed.
- Remark after Corollary 3: 'every positive wage draws some workers' fails under a wage tax near one combined with an exit payment (verdicts C3, policy route). Not reported: it holds under the full-rent-capture instruments that Corollary 3(ii) concerns.
- Terminology 'total (human) requirements' at L930 and L2137 (authors' words for the tilde coefficients, which elsewhere are renamed 'price coefficients'): judged readable as stated, not reported.
- Appendices D.2, D.4, D.5, E and F beyond their edited math and pointers; Tables D.1 and B.1 content beyond cross-references.
- The PDF was used only to confirm that the flagged sentences print as quoted; layout was not reviewed.

### Sources and quotations

- **S1** (imprecision; REWRITE L134 (Section 1, paragraph L133-136; NEW, narrative_draft v2)). The sentence says 'In these models machines are accumulated from output'. That is false for the third of the three papers just cited, Korinek and Juelfs (2022). Their formal models take the machine stock as given and accumulate nothing. The claim holds for Korinek and Suh (2024) and Korinek and Stiglitz (2019).
  - Fix: `In these models machines are accumulated from output` -> `In the first two of these models machines are accumulated from output`
  - Disposition: applied, reworded: "In the first two of these models machines are accumulated from output, so automating every task also automates the making of machines; in the third the stock of machines is given.".
- **S2** (cosmetic; REWRITE L652 (Section 4.1, after the loom; NEW, build brief §5)). The Restrepo (2025) sentence copies 14 consecutive words of the w34423 abstract without quotation marks. The source's exact words therefore read as the paper's own paraphrase. Build brief §5 itself treats the sentence as a quotation.
  - Fix: `Restrepo (2025) finds that wages converge to the opportunity cost of computational resources required to reproduce human work.` -> `Restrepo (2025) finds that ``wages converge to the opportunity cost of computational resources required to reproduce human work''.`
  - Disposition: applied.

Passed (28):

- Method: every quotation in the body was matched after normalizing whitespace and line-end hyphens; the script is checks/sources/scripts/quotes_check.py. Sources: Keynes in rq/keynes.txt (Norton 1963) and rq/ia_flat.txt (Macmillan, Popular Edition 1933, Internet Archive in.ernet.dli.2015.89977); Leontief on the page images rq/png/nap3.png and nap4.png, read in this session; Korinek and Suh in rq/txt/w32255.txt. Every quotation matches its source word for word.
- §1 L108-110, Keynes (1930), both quotations exact. 'may be solved, or be at least within sight of solution, within a hundred years' is at keynes.txt l.178-179 (Macmillan 1933 pp. 365-366). 'to satisfy the old Adam in most of us' is at l.249-250 (p. 369). 'still working a little' fits the three-hour-day passage. The quotation leaves out Keynes's proviso 'assuming no important wars and no important increase in population' but keeps his 'may'; noted, not a defect.
- §1 L116-118, Leontief (1983), both quotations exact against the page images: 'as the most important factor of production' (p. 3) and 'first diminished and then eliminated by the introduction of tractors' (p. 4). 'Half a century later' is right: 1930 to 1983.
- §1 L118-120, Acemoglu and Restrepo (2018), new tasks and the horses. w22252 l.107-109: 'Herein lies our answer to Leontief's analogy: the difference between human labor and horses is that humans have a comparative advantage in new and more complex tasks. Horses did not.' l.125 supports 'so far': 'new tasks and new job titles account for a large fraction of U.S. employment growth'. The word 'reinstatement' is the authors' later term and does not occur in w22252; the substance is supported.
- §1 L123-126, Korinek and Suh (2024). Both quotations are exact (w32255 l.74 and l.81). 'wages fall to the return on capital once every task is automated' is supported by Lemma 4(ii), l.760-761 ('both equal R = w = A. The latter condition always holds if Φ(I) = 1'), by Proposition 5 (l.1046-1048) and by l.1339-1340 ('After the collapse, wages are equal to the returns to capital').
- §1 L126-129, Korinek and Stiglitz (2019), both observations supported. Observation 8, c14018 l.1338-1340: 'human real wages fall, and the owners of nonreproducible factors absorb all the rents'. On housing, l.1344-1349: 'competition for fixed resources ... such as land used for housing, may lead workers to eventually be worse off'.
- §1 L129-130, Korinek and Juelfs (2022), exit. w30172 l.133-136: 'She enters the third regime if technological progress increases her non-labor income or reduces the marginal product of her labor sufficiently so that it becomes optimal for her to no longer work'. See also l.1543-1544.
- §1 L139 (main.tex L72, verbatim), new evidence for ASSEMBLY §7 item 10, which stays open only for Zeira's own text. w22252 l.233-234: 'Zeira's model is a special case of our framework'. Aghion, Jones and Jones (c14015 l.152-178) describe Zeira's per-good choice between labor and machines. Grossman and Rossi-Hansberg (2008): the Crossref abstract (tradeable tasks, offshoring) fits 'for offshoring'.
- §2 L213-214, the task-model lineage. 'task model of ... Acemoglu and Restrepo (2018)' is supported, and w22252 calls Zeira's model a special case. For the 'continuum' detail, see not_checked.
- §2 L229-230 and §3 L343, Leontief (1936) and Sraffa (1960) as input-output price systems. This repeats the authors' own attribution (main.tex L207 and L90 S1). Crossref confirms the Leontief 1936 title with 'Systems', as the kept entry has it.
- §3 L404, Mas and Pallais (2019), 'valuable'. Crossref abstract: the opportunity cost of a full-time job from lost leisure and household production is 60 percent of after-tax marginal product.
- §3 L479, the wedge remark. Acemoglu and Restrepo (2026), Crossref abstract: 'We show that automation targets high-rent tasks', with rents defined as 'wages above workers' outside options'. This matches 'automation targets the tasks that pay such premia'. §9.2 (L1426) does restate the targeting result. The labels 'efficiency wages' (Shapiro and Stiglitz 1984) and 'firm-level rent sharing' (Card et al. 2018) match those papers' titles and standard readings.
- §3 L517, Trammell and Korinek (2026). The Annual Review abstract (Crossref) and w31815 l.46-48 say: 'Robustly, fully automating production alone (so that machines can self-replicate) would dramatically raise the growth rate and lower the labor share'. The paraphrase does not overstate it.
- §4.1 L652, Restrepo (2025). The words are those of w34423's abstract, item (iv); only the quotation marks are missing (finding S2).
- §4.2 L768, Korinek and Stiglitz (2019), the below-subsistence scenario. c14018 l.250-252: 'pushing regular humans below their subsistence level'. l.1570-1573: 'falls below their cost of living at what they view as their basic subsistence'.
- §5 L904, the sentence after Proposition 4. Acemoglu and Restrepo (2018), Leontief (1936) and Sraffa (1960) are as in main.tex L90 S1. §5 L907, Caselli and Manning (2019): the pointer to Proposition 4 is apt, since Proposition 4 gives the hand-production lower bound and the rent upper bound.
- §5.2 L1001, the factor-share clause, checked against Crossref abstracts. Karabarbounis and Neiman: 'the global labor share has significantly declined'. Rognlie: the increase comes 'entirely from the housing sector'. Knoll, Schularick and Steger: 'Land prices, not replacement costs, are the key ...'; rising land prices explain about 80 percent of the boom.
- §6 L1111, the lilies aside. The quotation is exact: keynes.txt l.321-322, Macmillan 1933 p. 372. Keynes's 'We shall honour those who ... the lilies of the field' supports 'looked forward to honoring'. The text equals BRIEF §6 and stands after F6's lines.
- §6 L1130, Korinek and Lockwood (2026), checked against w34873 §3.4. The extension is Y = AK^γF^{1−γ}, with no labor (l.847-849). l.876: 'In an economy without labor'. l.895-896: 'taxing fixed factors is non-distortionary and can achieve powerful redistribution'.
- §10 L1455, the horses aside. It matches pp. 3-4: 'the role of humans ... bound to diminish—in the same way that the role of horses in agricultural production was first diminished and then eliminated by the introduction of tractors'. The text equals BRIEF §6 and is placed directly after the rent-tax sentence.
- D.2 L1968, the payroll citations. The sentences are main.tex L132 verbatim (the run-in head is D101). The Saez, Schoefer and Seim Crossref abstract (employment response to a payroll-tax cut) fits the sentence.
- New entry Keynes (1930). The title, 'Economic Possibilities for our Grandchildren', matches the 1933 edition's contents. 'The Nation and Athenaeum, 11 and 18 October 1930' matches that edition's own References list ('V. The Future ... 2. The same, Oct. 11 and 18, 1930'). 'Macmillan', first edition 1931, matches its copyright page. pp. 358-373 is confirmed in that edition (page heads run to 373; References begin at 375) and in Norton 1963 (keynes.txt footnote). There is no DOI.
- New entry Korinek and Juelfs (2022) matches the w30172 cover and abstract page and a fresh Crossref record: Anton Korinek and Megan Juelfs, June 2022, title exact, WP 30172, DOI 10.3386/w30172. A shorter Oxford Handbook of AI Governance version exists (doi 10.1093/oxfordhb/9780197579329.013.44). The cited WP is the version whose text was checked.
- New entry Korinek and Lockwood (2026) matches w34873 and Crossref: Anton Korinek and Lee Lockwood, February 2026, 'Public Finance in the Age of AI: A Primer', WP 34873, DOI 10.3386/w34873.
- New entry Leontief (1983). The chapter title, byline and pp. 3-7 match the page images (the chapter ends on p. 7). The volume title, subtitle 'A National Academy of Engineering Symposium, June 30, 1983' and 'NATIONAL ACADEMY PRESS, Washington, D.C. 1983' match the title page (rq/png/fmR1.png). Crossref 10.17226/19470 is an edited book from 1983 with no editor, as the entry implies.
- New entry Restrepo (2025) matches w34423 and Crossref: Pascual Restrepo, October 2025, WP 34423, DOI 10.3386/w34423. The title 'We Won't be Missed: Work and Growth in the AGI World' is spelled as on the abstract page and in Crossref.
- New entry Trammell and Korinek (2026) matches Crossref 10.1146/annurev-economics-051624-061002 (fetched in this session): Philip Trammell and Anton Korinek, Annual Review of Economics vol. 18, issue 1, pp. 589-611, issued 2026-08-07. Crossref capitalizes 'Under'; the entry's 'under' follows the list's lower-case style for prepositions.
- Every Crossref record was fetched fresh in this session and returned HTTP 200: 10.3386/w30172, w31815, w32255, w34423, w34873; 10.17226/19470; 10.1146/annurev-economics-051624-061002; plus the records of the moved citations, read for their abstracts. They are saved as cr_*.json in /tmp/claude-0/-home-user-labor/904c7da5-c8e1-5390-ac85-b6fa3b59f016/scratchpad/build/checks/sources/.

Not checked:

- Keynes (1930), the 1931 first edition's own pagination. The Internet Archive's two Macmillan 1931 copies (essaysinpersuasi0000unse_l9m7, essaysinpersuasi0000john_t4j1) are access-restricted: search-inside returned 403 and the page map 401. pp. 358-373 is confirmed only in the Macmillan 1933 Popular Edition and in Norton 1963. Both editions end at p. 376, which suggests the same setting, but this was not seen. The Nation and Athenaeum originals were not fetched; their dates come from the 1933 edition's References list.
- Zeira (1998), its own text. academic.oup.com returned a Cloudflare challenge (403), as earlier in rq/dl/zeiraoup. So §2 L213's 'a continuum of tasks, as in the task model of Zeira (1998) and Acemoglu and Restrepo (2018)' is unverified for Zeira. The only on-disk description of Zeira's production function is Aghion, Jones and Jones (c14015 l.152-171): 'In its simplest form, Zeira considers a production function like Y = A X1^α1 X2^α2 ... Xn^αn', and 'Zeira thought of the Xi's as intermediate goods'. That is a finite set of goods, not a continuum of tasks. w22252 l.234 calls Zeira's model 'a special case of our framework'. If Zeira has no continuum, a wording that holds either way, using w22252's own words: 'as in the task model of Acemoglu and Restrepo (2018), of which Zeira (1998) is a special case'.
- Caselli and Manning (2019), full text. The AEA PDF returned 403. The Crossref abstract ('new technology is unlikely to cause wages for all workers to fall and will cause average wages to rise if the prices of investment goods fall relative to consumer goods') is consistent with the authors' L128 sentence. It does not itself state 'real wages cannot fall in terms of goods produced entirely from reproducible inputs'.
- Mas and Pallais (2019), 'heterogeneous' (L404, main.tex L282 verbatim). The abstract does not address heterogeneity, and the full text is behind the AEA paywall.
- Gruber (1997), Kugler and Kugler (2009), Shapiro and Stiglitz (1984) and Card, Cardoso, Heining and Kline (2018): their texts are not on disk and Crossref has no abstract for them. The attributions are main.tex's own, verbatim, and only their placement and the titles in the entries were compared.
- report.md was not written. The harness refused the Write to checks/sources/report.md ('Subagents should return findings as text, not write report files'), so its content is this result: the findings, passed and not_checked lists. The scratch files are in /tmp/claude-0/-home-user-labor/904c7da5-c8e1-5390-ac85-b6fa3b59f016/scratchpad/build/checks/sources/: rw.txt (PDF text), cr_*.json (Crossref), ia_*.json (Internet Archive metadata and search), scripts/quotes_check.py and scripts/crsum.py, dl_cm/ (AEA), dl_zeira/ (OUP).

### Numbers against the code

- **N1** (imprecision; REWRITE L1212 (Figure 3 caption, third sentence); the definitions it conflicts with are at L290, L553, L793 and L804). The caption says each demand curve is traced as the margin moves over the tasks open to machines. The rewrite now counts every task in [x_c, x_H] as open, and in the instance H is empty (x_H = 1). The baseline curve stops at the ceiling x_c ≈ 0.94634, so the phrase overstates its domain. It was correct in main.tex, which called the tasks above x_c 'closed to machines at every wage'.
  - Fix: `as the task margin moves over the tasks open to machines.` -> `as the task margin moves over the tasks open to machines below the ceiling $x_c$.`
  - Disposition: applied.
- **N2** (cosmetic; REWRITE L1183 (Section 7, first sentence; the clause after 'For a numerical instance,' is the rewrite's own edit of main.tex L745 S1)). The sentence says Table 2 lists 'the shares' the parameters are set to match. One of the seven targets, baskets per worker Y/N = 3 (L1173), is a level, not a share. Table 2's caption (L1150) calls all seven 'targets'.
  - Fix: `For a numerical instance, Table~\ref{tab:instance} lists the parameters and the shares they are set to match.` -> `For a numerical instance, Table~\ref{tab:instance} lists the parameters and the targets they are set to match.`
  - Disposition: applied.

Passed (18):

- BASELINE. The repository's checks/check_interior.py on paper/main.tex passes all 112 checks. It was run with the scratchpad venv's python3, because the system python3 has no scipy, from /home/user/labor/pinning with PYTHONDONTWRITEBYTECODE=1. Afterwards git status was clean and code/__pycache__ was untouched. Output: /tmp/claude-0/-home-user-labor/904c7da5-c8e1-5390-ac85-b6fa3b59f016/scratchpad/build/checks/numbers/baseline_main_run.txt
- check_fan.py reads no paper text: it opens only effort/data/fig3_realwage_fan.csv, and main.tex appears only in a comment. So it was not copied. Run unchanged, it passes everything, including the +277%, +13% and -21% fork numbers that §8 prints at L1277.
- RE-POINTED COPY: /tmp/claude-0/-home-user-labor/904c7da5-c8e1-5390-ac85-b6fa3b59f016/scratchpad/build/checks/numbers/check_interior.py, with the original beside it as check_interior.orig.py for the diff. What changed:
- ROOT is /home/user/labor/pinning.
- It reads REWRITE with LaTeX comments stripped, as TeX strips them. main.tex's regions hold no comments, so this matches what the original reads; RAW_TEX=1 reads REWRITE raw.
- Region R_B is §3.1's flow-benchmark paragraph (L308) plus §7, without Figure 3's caption.
- Region R_S5 is old §5 in its new homes: §4.2, Corollary 1 and its remark, §7's statics (L1219-1227) and §9.1's heterogeneity paragraph.
- Region R_61 is §5.1. The old 6.1 is the new 5.1, with the same title, not 5.2 or 6; the hundred-to-one pointer is at L956.
- R_CAP and R_D3 are unchanged.
- Templates are re-worded only where the sentence survives: 'flow benchmark' (L308); 'instance' (now Table 2's parameter rows, L1157-1162, values in the table's order a, λ, b); 'shares' ('the cost of a basket at final tasks'); 'support' ('owner's').
- Q4's anchor is the new D.3 sentence. Q8 reads the figure file the rewrite includes, which is byte-identical to the repository's.
- No expected value, tolerance, computation or check was changed.
- RE-POINTED RUN, comments stripped: 110 PASS, 2 FAIL of 112 (run_rewrite_stripped.txt). All of groups E, I, L, F and S pass (100 checks). Q1[B] passes with all 9 passages, including Table 2's rows. Q1/Q2[CAP], Q1/Q2[61], Q4, Q5, Q6 (8 captions), Q7 and Q8 also pass.
- FAIL Q2[B]: the anchor coverage is at fault; the text is right. No template covers 19 decimals the rewrite added to §7:
- Table 2's targets 0.47, 0.20, 0.47, 0.06, 0.15, 0.60;
- Table 2's last column 0.456, 0.196, 0.469, 0.065, 0.148, 0.602, 3.01;
- 15.5 (L1232) and 0.12 (L1248);
- η = 0.001 (L1252, L1259), 0.018 (L1252) and 1.8 (L1259).
Every one recomputes correctly.
- FAIL Q3: the anchor is at fault; the text is right. Two of its five conjuncts are exact sentences from main.tex L308 ('In the flow benchmark, the production network prices the basket ...'; 'so $P_s=wL_s+rB_s$. With durable machines, ... (Appendix~\ref{app:B}).').
- The rewrite dropped L308 and restated it as Lemma 1(i) and (iii) (L586-588) and in the remark closing §5.2 (L1005).
- Groups I3/I4 verify that content (P_s = wL_s + rB_s + ρV_mX/Y; the coefficients coincide only in the flow benchmark) and pass for all five economies.
- Q3's other three conjuncts pass: no decimal in old §5's text; both channels lower w/P_s and N_a/N; 'In that example, both automation channels lower ...' is present at L1227.
- RAW RUN, comments kept: 109 PASS, 3 FAIL (run_rewrite_raw.txt). The extra failures come only from the provenance comments: Q2[61] on '3.2' and '2.3'; Q3's no-decimal conjunct; and 62 more Q2[B] decimals such as '0.4556' and '3.4'.
- TASK 3, parameters: Table 2's twelve parameters equal PRINTED in code/appendix_b.py: N 1, T 0.01, h 0.0017, a 1.4, λ 7.3, b 0.4, δ 0.05, ρ 0.09, γ = 0.01 + 0.99x^4.4 with η = 1, and χ on [0, 2.2]. γ(0) = 0.01 and γ(1) = 1, as the caption says.
- TASK 3, Table 2's caption: a closed-form recalibration confirms it. The targets force x* = 0.83, J(x*) = γ(x*)(1 - x*) and ρ + δ = 0.143167. The calibrated values are T 0.010013, h 0.0016938, a 1.39697, λ 7.29929, k 4.35513, χ_max 2.20945 and ρ 0.093167. They hit all seven targets to 1e-9 and round to Table 2 at two significant figures; ρ needs two decimal places (it would be 0.093 at two significant figures), as the caption says. The last column recomputes to 0.4556, 0.1960, 0.4691, 0.0654, 0.1480, 0.6017 and 3.0132.
- §7 L1232: exactly two curvatures match the targets, k = 4.3551 and 15.4984, searching [1e-3, 1e4]. At the upper one, halving γ raises w/P_s by 9.19% (8.73% once rounded). At the lower one it lowers w/P_s by 3.0% (3.4% rounded). All four economies are funded (other_root_details.txt).
- TASK 3, Section 7's text agrees with Table 2:
- 6.5 percent agrees with 0.0654, and 60 percent with 0.6017.
- Y 3.01320 and N_a 0.60165 agree with 3.01 and 0.602 at N = 1.
- 0.08902/0.60165 = 0.148 and h/NP_s = 0.065.
- v(1 - x*)/P_s = 0.469.
- x_c = 0.94634 follows from Table 2's a, λ, ρ, δ and γ.
- The path's γ and Figure 3's parameter list are Table 2's.
- §7, the instance: x* 0.829869, x_c 0.946343, v 0.071654, Y 3.013205, N_a 0.601654, hours 0.512639 + 0.089015, NP_s 0.025989, rent plus interest 0.035200.
- §7, the path:
- π = 0.0696517, and (T - Nh)/(Nπ) = 0.119164 ('about 0.12').
- Participation is 0.563972, 0.133981 and 0.017877 at η = 1, 0.01 and 0.001.
- From η = 1 to 0.001, w/p rises by a factor of 1.78037 and w/r falls by a factor of 426.193.
- On 2,001 log-spaced η in [1e-4, 1]: P_s ≤ (ηπ + h)r and P_s ≥ h; X ≤ ηT/[h(1 - aδ)]; 0 < v ≤ ηπ; (25) holds; rent alone funds the support for η ≤ 0.119; rent plus interest fund it at every point.
- R/I goes from 0.2698 to 0.99945, labor's share from 0.4457 to 1e-6, and γ_η(1)/γ_η(0) = 100.
- Figure 3's caption (L1212): the three equilibria are 2.757070/0.601654, 2.458169/0.563972 and 2.664394/0.590301, printed as 2.76/0.60, 2.46/0.56 and 2.66/0.59. Both channels lower w/P_s and N_a/N, as L1227 says.
- §5.2 L994: income shares are 0.550511 wages, 0.127697 rent and 0.321792 return on machines; they sum to 1, and P_sY = wN_a + rT + ρV_mX holds to 1e-12. Labor's share is 0.5505 and (15)'s bound is 0.811714. These match the printed 0.55, 0.13, 0.32, 0.55 and 0.81.
- §6:
- L1074: rent covers T/(NP_s) = 0.384778 of support (printed 0.38), and the return on machines covers 0.9696 of it, at least the rest.
- The measured κ of 0.30 matches §8 L1295 and data/kappa_results.csv (0.2976 [0.1504-0.5890]).
- L1106, at λ = 0 and x = 1: (T + ρV_mX)/(NP_s) = T/(NB_s) = 1.707153 (printed 1.71), and rent alone gives 0.659369 (printed 0.66).
- Appendix D:
- D.3 L2006 is exact: κ = 20/19 at q = 10/9 with fifty people; q* = 4 with eighty; 120 > 100.
- D.5 L2028: D = 0.3136 (printed 0.31) and 0.08.
- Table D.1 against the repository's data: φ_C 0.6416 [0.5412-0.8132]; 2023 0.6581 [0.5266-0.8011]; 1965 0.7407. φ_G (lamR_med) 0.6828; 1965 0.6387; mid-1980s 0.697-0.700. Conditioned share 0.8427 ≥ 0.84. κ 0.2976 [0.1504-0.5890]; 1950s 0.043-0.066.
- Figure D.1's caption: borrowing financed 18.95% of transfers in 2025, and was zero only in 1960, 1963, 1999 and 2000; the direct-wage share fell 19.4 points; taxes on ownership income financed 0.216 of transfers.
- IN ALL: recompute_numbers.py compares 114 printed numbers in §5, §6, §7, Table 2, Figure 3's caption and Appendix D, with 0 mismatches. Output: /tmp/claude-0/-home-user-labor/904c7da5-c8e1-5390-ac85-b6fa3b59f016/scratchpad/build/checks/numbers/recompute_numbers_out.txt

Not checked:

- report.md was not written: the harness refuses report files from subagents. Its content is in this output. The re-pointed check, its runs and recompute_numbers.py with its output are in /tmp/claude-0/-home-user-labor/904c7da5-c8e1-5390-ac85-b6fa3b59f016/scratchpad/build/checks/numbers/.
- Not applied, because each would add expected values or checks:
- Templates for Q2[B]'s 19 decimals. Table 2's targets panel could use NUM's theta_V, machines, labor, site, chain and participation at .3f and Y at .2f; 15.5, 0.12, 0.018, 1.8 and 1/426 need new computations.
- Regions for §5.2's and §6's numbers (L994, L1074, L1106), which no region covers.
- Replacements for Q3's two L308 anchors, for example Lemma 1(iii) at L588 and the §5.2 remark at L1005.
This bears on ASSEMBLY §7 problem 7.
- Table D.1's '≈0.99 by withdrawal rule (2024)' (L2042) is the authors' verbatim number. Its source according to the README, data/lambdaB_results.csv lamB_rule, is 1.0 in every year, and the script that made the CSV is not in the repository. I could not reproduce 0.99, so I did not report it as a defect.
- This is repository text, not REWRITE. code/appendix_b.py's header (line 33, 'labor 0.47 of consumption on the full chain') and check_interior.py's Q5 label ('full-chain cost of consumption') call the third target full-chain. The code computes, and the calibration matches, the final-task share v(1-x*)/P_s; the full-chain share wL_s/P_s is 0.5505. Table 2 and §7 (L1194) now say this correctly.
- Figure 3's image was not redrawn, because code/fig_labor_market_clearing.py writes into the repository. The rewrite's file is byte-identical to the repository's, and its legend still says 'baseline (Appendix B)' (D55).
- §8's numbers other than κ = 0.30 are outside this check. check_fan.py covers the fork numbers and passes.

### Read-through

- **R01** (error; REWRITE L1915 (Appendix C, p. 41)). After the restructure this cross-reference points at the wrong result. Proposition 4 now states only the final good's bounds (the human method with λ̄ = 1). The general human-method bound with λ̄_0, from which r/p ≥ 1/[(w/r)λ̄_0] follows, is (24) in the remark after Proposition 4, and Proposition B.1(c). The math check mathB also reports this.
  - Fix: `Proposition~\ref{prop:4} gives $r/p\ge1/[(w/r)\bar\lambda_0]$` -> `\eqref{eq:13} gives $r/p\ge1/[(w/r)\bar\lambda_0]$`
  - Disposition: applied (as mathB-2).
- **R02** (imprecision; REWRITE L1598 (Appendix A, proof of Corollary 1(ii), p. 35)). "The interior conditions" no longer refers to anything. It named the hypotheses of main.tex's Lemma B.1, "Interior equilibrium with funded support" (L719), which the rewrite restates as Theorem 1. Corollary 1(ii) now states its hypotheses as "(22) and funding hold under both", and nothing else in the rewrite is called "the interior conditions".
  - Fix: `If the interior conditions continue to hold` -> `If \eqref{eq:25} and funding continue to hold`
  - Disposition: applied.
- **R03** (imprecision; REWRITE L998 (Section 5.2, p. 21)). "The funded-support conditions for (25)" no longer refers to anything. It pointed to main.tex's corollary hypothesis that one basket remains funded. The design dropped that hypothesis (synthesis §3.2: "'one basket remains funded' is dropped (Def. 1)"). Corollary 2's conditions for (25) are now that F is fixed and g_w ≤ g_e. The math check mathB also reports this.
  - Fix: `When the funded-support conditions for \eqref{eq:14} also hold` -> `When the conditions for \eqref{eq:14} also hold`
  - Disposition: applied (as mathB-3).
- **R04** (imprecision; REWRITE L1184-1194 (Section 7, first paragraph, p. 23)). "These values" now points at the wrong sentence. The authors' "These values are illustrative. They are chosen so that cost shares are of the order seen in U.S. data" referred to L745's parameter list, which is now Table 2. A NEW sentence, "In the instance, H is empty (x_H = 1), every instrument is zero, and the owner provides support.", now stands between the two. As a result, "These values ... are chosen so that cost shares ..." reads as describing x_H = 1 and the zero instruments, which are not chosen to match any share. This bears on D57. Moving the NEW sentence, with its comment, to after the shares sentence fixes the reference without changing any of the authors' words.
  - Fix: `% NEW: the primitives Table 2 does not list. The stated economy has a wall x_H and a policy among its
% primitives (Section 3), and Theorem 1 assumes every instrument zero and the owner providing support
% (its wording, and Section 3's baseline); main.tex L683 had the household provide support, with` -> `% from main.tex L745, sentence 2, verbatim
These values are illustrative.
% from main.tex L745, sentence 3, edited: "the full-chain cost of consumption" -> "the cost of a basket at
% final tasks" (design synthesis §3.4 and its decision 6: the share the code computes and Table 2 prints,
% 0.469, is f`
  - Disposition: applied (the sentence moved, no words changed).
- **R05** (imprecision; REWRITE L494 (Section 3.6, p. 10)). The defined "interior margin" gets a second name. Two sentences after Definition 2 defines "interior margin" (and L491 says "The margin is interior when 0 < x* < x_H"), the authors' L170 S7 calls the same object "an active contestable margin". The stray name occurs at:
- L494 (§3.6);
- L1358 (§9.1, "An active contestable margin prices each type's wage");
- L1448 (§10, "at the active margin");
- L1833 (B.2, "At an active margin");
- L1856 (B.3, "an active margin satisfies");
- L1864 (B.4, "each type's active contestable margin");
- L1404 (§9.1, "both held contestable margins").
D91 covers only the B.2-B.4 places and D65 covers L1404; the three main-text places, L494, L1358 and L1448, are new. The provenance comment at L492-493 glosses this very sentence as "(an interior margin can have H nonempty)".
  - Fix: `An active contestable margin can coexist with human-required tasks in $H$.` -> `An interior margin can coexist with human-required tasks in $H$.`
  - Disposition: applied through D91.
- **R06** (imprecision; REWRITE L1358 (Section 9.1, first paragraph, p. 27)). This is the same second name for Definition 2's interior margin as in R05: "An active contestable margin" (main.tex L326, verbatim).
  - Fix: `An active contestable margin prices each type's wage against machine services.` -> `An interior margin prices each type's wage against machine services.`
  - Disposition: applied through D91.
- **R07** (imprecision; REWRITE L1448 (Section 10, first paragraph, p. 30-31)). This is the same second name: "the active margin" stands for the interior margin. Corollary 2, which this sentence summarizes, is stated "along a sequence of equilibria with interior margins" (main.tex L540 S5, verbatim).
  - Fix: `If replacement at the active margin drives` -> `If replacement at an interior margin drives`
  - Disposition: applied through D91, with "the" kept.
- **R08** (imprecision; REWRITE L930 (Section 5.1, p. 19); also L2137 and L1088). "Total human requirements" is an undefined second name for the price coefficients. Here it means λ̃_i, since p_i = wλ̃_i + rb̃_i. The rewrite cut both places where main.tex defined "total requirements": L213 S3, "Define the total requirements ...", and L913 S2, "total requirements are b̃_i". Everywhere else it renamed the term "price coefficients" (L671, L887, L1798, L1991). The name now also points two ways: Corollary 3(i) (L1088) calls the physical B_s "the basket's total non-produced input requirement", although B_s ≤ b̃_s, with equality only at ρ = 0. All places: L930, L2137 (Appendix F), L1088.
  - Fix: `At given wages, rents, and total human requirements, a lower $\widetilde b_i$ reduces the price.` -> `At given wages, rents, and $\widetilde\lambda_i$, a lower $\widetilde b_i$ reduces the price.`
  - Disposition: applied.
- **R09** (imprecision; REWRITE L2137 (Appendix F, last paragraph, p. 47)). This is the same undefined name as in R08: "total human requirements" stands for λ̃, two lines after the display wλ̃^⊤f that the sentence is about (main.tex L908, verbatim).
  - Fix: `final quantities when total human requirements fall;` -> `final quantities when $\widetilde{\bm{\lambda}}$ falls;`
  - Disposition: applied.
- **R10** (imprecision; REWRITE L209-210 (Section 2, p. 4)). Section 2 describes the owner differently from the body. Section 2 says the owner discounts the future, so a machine must earn a return. Assumption 5, however, admits β = 1 (ρ = 0, ranked by the long-run average), and the body uses ρ = 0, at which a machine earns no return, as the flow benchmark and in many "When ρ = 0" statements.
  - Fix: `The owner lives forever and
discounts the future, so a machine must earn a return to be worth holding.` -> `The owner lives forever and
may discount the future, so a machine may have to earn a return to be worth holding.`
  - Disposition: applied, reworded: "may discount the future, in which case a machine must earn a return to be worth holding".
- **R11** (imprecision; REWRITE L442 (Section 3.5, first sentence, p. 8)). This pointer misses Section 5. It says the instruments stay inactive until Section 6 or Appendix D uses them, but Corollary 2 in Section 5 already admits d, g_w, g_e and τ_w: in its hypothesis g_w ≤ g_e, in its remark's bound, and in its proof.
  - Fix: `each inactive until Section~\ref{sec:rent} or Appendix~\ref{app:D} uses it` -> `each inactive until Corollary~\ref{cor:vanishing}, Section~\ref{sec:rent}, or Appendix~\ref{app:D} uses it`
  - Disposition: applied.
- **R12** (imprecision; REWRITE L1951 (Appendix D.1, p. 42)). The symbol d has two different meanings. In Section 3.5 and budget (8), d is the uniform-transfer instrument, paid on top of g_n. In D.1, d is the common value of g_w and g_e. Read with (8), "g_w = g_e = d" therefore pays 2d. And if D106 adds "with τ_w = d = 0" to the comparison, the same sentence sets both payments to zero. This bears on D106.
  - Fix: `An unconditional payment $g_w=g_e=d$ gives $\Delta=0$ and the reservation wage $(e^\chi-1)(P_s+d)$.` -> `An unconditional payment $g_w=g_e$ gives $\Delta=0$ and the reservation wage $(e^\chi-1)(P_s+g_e)$.`
  - Disposition: applied.
- **R13** (imprecision; REWRITE L639 (Section 4.1, proof of Proposition 1(ii), p. 13)). The symbol N_F is never defined. The proof uses dN_F/dx* and dw/dN_F, but the clause before them names final-task labor demand without giving it a symbol. N_F appears nowhere else; Table 1 has only N_D and N_S. This is already the case in main.tex L627.
  - Fix: `final-task labor demand is $Y\int_{x^*}^1dx/\gamma_L(x)$` -> `final-task labor demand is $N_F=Y\int_{x^*}^1dx/\gamma_L(x)$`
  - Disposition: applied (as mathA-4).
- **R14** (imprecision; REWRITE L1608 (Appendix A, proof of Proposition 4, p. 35)). The symbol λ̃_g is never defined. Proposition 4 defines only b̃_g = b̃_m J(x*) (L899). The math check mathB also reports this.
  - Fix: `because $\widetilde\lambda_g\ge0$` -> `because $p=w\widetilde\lambda_g+r\widetilde b_g$ with $\widetilde\lambda_g=1-x^*+\widetilde\lambda_mJ(x^*)\ge0$`
  - Disposition: applied.
- **R15** (cosmetic; REWRITE L1982 (Appendix D.3, p. 43); variants at L156, L442, L1114, L1219, L1423, L1943, L2100). The basket has a second name whose definition was cut. "Basic living basket" was defined only by main.tex L913 S2 ("P_s is the cost of the basic living basket"). The rewrite replaced that sentence with Table 1, which calls it "the basket", and Section 3.3, the target of this pointer, also says only "baskets". Every place a variant occurs:
- L156 §1, "the household's living basket" (before the model; can stay);
- L442 §3.5, "the support basket";
- L1114 §6, "a living basket with a persistent non-produced input requirement";
- L1219 §7, "the living basket";
- L1423 §9.2, "holds the living basket fixed";
- L1943 D.1, "the supported basket";
- L1982 D.3 and L2100 Appendix E, "the basic living basket".
  - Fix: `Use the same basic living basket as in Section~\ref{sec:workers}` -> `Use the same basket as in Section~\ref{sec:workers}`
  - Disposition: applied.
- **R16** (cosmetic; REWRITE L2100 (Appendix E, last paragraph, p. 47)). This is the same stray name as in R15: "the basic living basket", which here is the basket z itself.
  - Fix: `Human-required services also enter the basic living basket through $\mathbf{z}$.` -> `Human-required services also enter the basket through $\mathbf{z}$.`
  - Disposition: applied.
- **R17** (cosmetic; REWRITE L759 (Section 4.2, p. 15); plural uses at L959, L1069, L2015). "The provider" is a second name for the agent now called the owner. In main.tex it named the household that maintains support (L276, L590, L725, L736-747). The rewrite renamed that agent "the owner" everywhere else: Theorem 1's proof, Section 7, Table 1. The definite "the provider" therefore reads as a third agent, although the remark three lines earlier says support comes from "the owner or the government". The other uses are plural and generic and can stay: L959 "providers' resources", L1069 "support providers", L2015 "existing providers".
  - Fix: `Maintaining that support requires resources from the provider.` -> `Maintaining that support requires resources from the owner or the government.`
  - Disposition: applied.
- **R18** (cosmetic; REWRITE L713 (Section 4.1, p. 14)). "Two-factor flow benchmark" is a variant of a defined term. Section 3.1 defines "the flow benchmark", (ρ,δ) = (0,1), and "two-factor flow benchmark" occurs only here. Part 05 dropped the same adjective at main.tex L393 (D40). The sentence also nearly repeats L998, "Interest, institutional rents, and transitional capacity rents add income components outside the flow benchmark"; that repeat is already in main.tex (L257, L393).
  - Fix: `outside the two-factor flow benchmark.` -> `outside the flow benchmark.`
  - Disposition: applied.
- **R19** (cosmetic; REWRITE L609 and L613 (Figure 1 caption, p. 12)). The caption gives the open tasks [0, x_H] of Assumption 1 a second name, "the machine-contestable set" and "machine-contestable task". The text says "open tasks" (Assumption 1, Definition 2, Lemma 2, Figure 7's caption), and Figure 3's caption says "the tasks open to machines". The caption's phrase occurs nowhere else.
  - Fix: `increases. On the machine-contestable set, the ratio $w/p_m$ divides tasks:
machines hold tasks with $\gamma(x)<w/p_m$, labor holds tasks with
$\gamma(x)>w/p_m$, and an interior margin $x^*$ satisfies equality. Tasks in
$H$ are closed to machines and appear as a wall at the right edge. If labor
hold` -> `increases. On the open tasks, the ratio $w/p_m$ divides tasks:
machines hold tasks with $\gamma(x)<w/p_m$, labor holds tasks with
$\gamma(x)>w/p_m$, and an interior margin $x^*$ satisfies equality. Tasks in
$H$ are closed to machines and appear as a wall at the right edge. If labor
holds no open tas`
  - Disposition: applied.
- **R20** (cosmetic; REWRITE L918 (Section 5.1, remark after Proposition 4, p. 19)). The subscript h in b̃_h is used before it is defined. The index h for space is introduced only in Assumption B.1 ("space h", p. 37), and Table 1 uses h for the space per basket. The same sentence writes the final good's coefficients without any subscript.
  - Fix: `and space has $\widetilde b_h=1$` -> `and space has $\widetilde b=1$`
  - Disposition: applied, reworded: "and space, which rents at $r$, has $\widetilde b=1$".
- **R21** (cosmetic; REWRITE L1243 (Section 7, p. 24-25)). π is a second name for b̃_m. The definition π = (ρ+δ)b/[1−(ρ+δ)a] is b̃_m of (5), so p_m = πr is the machine-service row with λ̃_m = 0. The paragraph introduces π without saying so, and the authors' bound later in the same sentence writes the expression a third time.
  - Fix: `where $\pi=(\rho+\delta)b/[1-(\rho+\delta)a]$` -> `where $\pi=(\rho+\delta)b/[1-(\rho+\delta)a]=\widetilde b_m$`
  - Disposition: applied.
- **R22** (cosmetic; REWRITE L87 (abstract, p. 1)). "Ceiling" names two different objects. The abstract calls the rent bound on wage purchasing power "a ceiling". The body names x_c "the ceiling" (Lemma 2's title, Table 1, and Section 7's "below the ceiling x_c") and calls the rent bound an "upper bound" (opening of Section 5, L881). This bears on D1 (abstract unchanged).
  - Fix: `embodied rent costs impose a ceiling` -> `embodied rent costs impose an upper bound`
  - Disposition: applied (one word of the abstract).
- **R23** (cosmetic; REWRITE L751 and L759 (Section 4.2, p. 15)). The same pointer appears twice within three lines. The NEW remark after Proposition 3 ends "With payments, Appendix D.1 gives the reservation wage.", and the authors' paragraph that follows ends "Payments that change upon employment are treated in Appendix D.1." The restructure created this repeat (the design's remark sits next to main.tex L296).
  - Fix: ` With payments, Appendix~\ref{app:D.1} gives the reservation wage.` -> ``
  - Disposition: applied.
- **R24** (cosmetic; REWRITE L311 (Section 3.1, foot of p. 5)). The run-in head "Land." is left alone as the last line of p. 5, and Assumption 3 starts p. 6. The head is a paragraph of its own (a blank line follows it), and LaTeX may break the page just before a theorem-type environment, so the head can be stranded. Dropping it leaves "Assumption 3 (land)" as the label. The head is the design's NEW text, so no words of the authors change; alternatively, keep it and suppress that break.
  - Fix: `\textbf{Land.}

\begin{assumption}[land]` -> `\begin{assumption}[land]`
  - Disposition: applied.
- **R25** (cosmetic; REWRITE L264 (pointer, p. 4) and L522-561 (Table 1, p. 11)). Table 1 is far from its first mention. Its only pointer, "Table 1 collects the notation.", is on p. 4, right after the primitives sentence, which uses about 18 symbols (γ, x_H, a, λ, b, δ, T, N, h, F, β, u, τ_R, τ_w, d, g_w, g_e, σ) that Sections 3.1-3.5 define only later. Table 1 prints as a float page on p. 11, seven pages on. D8 covers the sentence and D29 covers Figure 1, but neither covers this table. The fix is a move, not a string replacement: cut the block from "% NEW (design synthesis §2.2): Table 1" through its \end{table} (L522-561) and paste it directly after L264, "Table~\ref{tab:notation} collects the notation.". With [htbp] the table then prints at the top of p. 5 or on the next float page. No text changes.
  - Fix: see the defect
  - Disposition: applied (Table 1 moved; it prints on p. 5).

Passed (13):

- The tool refused to write report.md ("Subagents should return findings as text"), so this result is the report. Scratch files are in /tmp/claude-0/-home-user-labor/904c7da5-c8e1-5390-ac85-b6fa3b59f016/scratchpad/build/checks/read/: rewrite.txt, baseline.txt, img/, hi-*.png, fixes_all.json, fixes_long.json, and scripts/ (near_dups.py, near_dups_tex.py, check_fixes.py, build_fixes.py, validate_all.py).
- Read the PDF text start to finish (50 pages), then the LaTeX with its provenance comments, section by section.
- Every fix_old above occurs exactly once in REWRITE, and all 24 string fixes apply together without collision (validate_all.py).
- Cross-references: listed every label with its printed number and page from the aux file and checked each \ref and \eqref against the claim around it. All resolve to the intended object except R01 and R11. The phrases 'this section', 'this appendix', 'the main text', 'above', 'below' and 'here' land correctly.
- The roadmap at the end of Section 1 matches the section order and contents. It leaves out B.3 trade, B.5 and B.6, but says nothing false.
- Every claim in the abstract is supported by the body. Its only defect is the word 'ceiling' (R22); its narrower 'at an interior task margin' is still true.
- Section 2 matches the body (households, basket, support, tasks, machines, land, government, the three determinants of w/r), except the discounting sentence (R10).
- Sentence-initial This, These, Such, It, Its, Both and Either all have antecedents, except R04 and the known D68 ('Either change'). The Leontief aside leaves 'Its scale ...' pointing at the rent dividend, which is fine.
- Symbols used before they are defined: checked v, N_a, C, x*, λ̃_m, x_c, s, L_s, B_s, R, I, κ, ξ, θ, π, η, b̃_g, y, z, f, p_K, μ, w_H, φ_C, Δ, q and σ_H. Only N_F, λ̃_g and b̃_h are undefined (R13, R14, R20). R appears in Table 1 before Proposition 6.
- Ran a near-duplicate sentence scan over the body. The only restructure-made repeats are the known items (D6, D7, D30, D35, D51) plus R23.
- Page layout: rendered pp. 4-7, 11-13, 17, 19 and 39 as images. No heading is stranded at a page foot; the only stranded run-in head is 'Land.' (R24). No broken or overlapping math, and the log has no overfull boxes.
- Float distance: Figures 2-7 and Tables 2, B.1 and D.1 all print within two pages of their first mention. Figure 6 drifting into 9.1 and Figure D.1 drifting into Appendix E also happen in the baseline PDF.
- No lowercase n_D or n_S remains, in the text or in the figure files; Figure 3's caption reads N_D/N.

Not checked:

- Mathematical correctness of statements and proofs, and the numbers. These are for the math and number checks; I flagged only definitional and pointer defects. R01, R03 and R14 overlap with checks/mathB.
- Accuracy of citations and quotations.
- Figure artwork beyond the text pdftotext extracts. Figure 3's legend 'baseline (Appendix B)' is a known issue (ASSEMBLY §7 item 6).
- Pages not rendered as images; on those I checked layout only from the text.
- Not reported because they come from main.tex, not the restructure: (a) 'Personal assets, pensions, and savings ...' appears three times, in 4.2 (L766), Section 10 (L1475) and D.4 (L2015), from main.tex L298, L555 and L829. (b) 9.1's opening paragraph (L1358, from L326) and B.4 (L1864, from L622) restate each other. (c) Section 10's figure 0.68 has no pointer to Table D.1, as in main.tex.
- Bears on D62, not reported separately: the 9.1 cuts (L471 S3-S4, L473 S2-S3) remove the only text that explained Figure 7's labels 'Engines price the entrant; the trained worker is behind the wall' and 'Computers price the entrant ...'. The figure caption still covers them.
- Not re-reported (already in ASSEMBLY §5/§7): D6, D7, D29, D30, D40, D51, D57, D58, D60, D61, D62, D65, D68, D73, D76, D90, D91, D101-D108, and §7 items 1-12.

## Round 2

### Verification of the review edits

- **V1** (error; REWRITE L1137 (Section 6, after Corollary 3's remark; PDF p. ~22: "The parents (Section 3.4) may themselves finance that support from wages.")). Review edit D6 left this pointer dangling. D6 removed the parents example (main.tex L268 S3) from Section 3.4 (sec:owner). The build had added "(Section~\ref{sec:owner})" to this sentence only so that it would point to that example. The example now prints only in Section 2 (sec:description), so the pointer sends the reader to a subsection that no longer mentions parents.
  - Fix: `The parents (Section~\ref{sec:owner}) may themselves` -> `The parents (Section~\ref{sec:description}) may themselves`
  - Disposition: applied (the review's own D6 had broken this pointer).
- **V2** (imprecision; REWRITE L1125 (remark after Corollary 3, first sentence); check 5(a)). The remark says, without restricting the policy, that every positive wage draws some workers when F(z)>0 for z>0. The remark does not limit the instruments, and Corollary 3(ii) fixes only full rent capture. Under budget (8), a worker works only if log[(P_s+d+g_w+(1-tau_w)w)/(P_s+d+g_e)] >= chi. With an exit payment g_e > g_w + (1-tau_w)w, nobody works at that positive wage, and no wage tax is needed for this. A configuration with no labor can then clear the labor market, so the remark's conclusion fails as written. The claim holds exactly when no payment favors exit, g_e <= g_w. The gain is then log[1+((1-tau_w)w+g_w-g_e)/(P_s+d+g_e)] > 0 for every w>0 and tau_w<1.
  - Fix: `while every positive wage draws some workers when $F(z)>0$ for $z>0$, as in the instance,` -> `while, if no payment favors exit ($g_e\le g_w$), every positive wage draws some workers when $F(z)>0$ for $z>0$, as in the instance,`
  - Disposition: applied.
- **V3** (cosmetic; REWRITE L1053 (comment of review edit mathB-4)). The note says R 'was defined only in Corollary 3'. That is wrong. Before the edit, R was defined in the coverage paragraph after Proposition 6's remark ('with $R=rT>0$', L1078), which comes before Corollary 3. Corollary 3 does not define R. The edit itself is correct.
  - Fix: `(it was defined only in Corollary 3)` -> `(it was defined only in the coverage paragraph after Proposition 6's remark)`
  - Disposition: applied (a comment only).

Passed (45):

- R22: the abstract now says 'an upper bound'. 'Ceiling' is left only for x_c. The PDF reads correctly.
- S1: checked against rq/txt/w30172.txt l.881-882 ('We assume that there is a given amount of the other factors of the economy, here captured by machines m'). 'first two'/'third' match the order of citation (Korinek and Suh; Korinek and Stiglitz; Korinek and Juelfs). The sentence reads correctly.
- R10: 'may discount the future, in which case ...' is consistent with Assumption 5 (beta in (0,1]) and with the flow benchmark.
- R25: Table 1 now follows 'Table 1 collects the notation.' directly and prints on p. 5, next to the pointer on p. 4. No other text refers to its old place. The Appendix F run-in 'Table 1 lists the notation' still resolves.
- R24: the 'Land.' head is dropped. Assumption 3 (land) follows the flow-benchmark paragraph with no orphan.
- D7: L74 S6 still prints whole in Section 1 (L144). Section 3.1 reads correctly without it.
- mathA-1: 'whenever it consumes and holds machines (Lemma A.1(c))' matches Lemma A.1(c)'s hypotheses c_o>0 and X>0. It no longer contradicts the F5 sentences.
- mathA-3: Proposition B.1(a) states lambda~ >= (I-A_0)^{-1} lambda and b~ >= (I-A_0)^{-1} b for every good. Lemma 1(iii) covers the basket. The pointer is correct.
- D6: the paragraph in Section 3.4 reads correctly. The edit created the dangling pointer at L1137 (finding V1).
- R11: Corollary 2 uses g_w and g_e (hypothesis), d (remark) and tau_w (proof), so the pointer is correct.
- D76: sec:stabilizers is Subsection 9.2 'Possible stabilizers', where the mu(x) wedge and Acemoglu and Restrepo (2026) stand (L1451).
- D91 (all six places: L541, L1382, L1474, L1866, L1890, L1899) and L1404 (L1429): 'interior margin(s)' replaces 'active (contestable) margin' with no broken sentence. 'active' remains only as 'inactive' and 'active production method'. The plain-English 'As trained tasks become contestable' (L1421, authors' L473) was judged readable and is not a renamed term.
- R19: Figure 1's caption 'open tasks'/'open task' agrees with Assumption 1 and with Definition 2's boundary assignment.
- mathA-4: N_F = Y int_{x*}^1 dx/gamma_L defines the symbol before dN_F/dx* and dw/dN_F. The derivative is correct.
- S2: the quoted words match rq/txt/w34423.txt l.53-54 exactly. Punctuation outside the closing quotes is the paper's usage (as at L110 and L119).
- R18: 'outside the flow benchmark' agrees with Section 3.1's definition.
- R23: the remark after Proposition 3 ends cleanly. The D.1 pointer remains in the authors' paragraph two sentences on.
- R17: 'from the owner or the government' matches the remark above. The plural 'providers' at L976, L1088 and L2058 is generic, as the first round judged.
- D25: 'sets of tasks and of workers of measure zero' covers workers at the participation tie. It is consistent with Proposition 3's proof.
- D30 / check 5(b): Theorem 1's remark reads correctly ('Its uniqueness rests on the clause ... When the wall lies below the crossing ...'). Section 3.6 (L520) still states F5's point ('When support absorbs all the owner's income, the owner's first-order condition does not bind, and the user-cost clause of condition (i) selects the user cost at rho'), and the remark after Lemma A.1 gives the reason.
- R20: space's price coefficient is b~ = 1 (zero row of A_rho, b = 1), which agrees with w/p <= (w/r)/b~ and Proposition 4's 'w/r units of space'.
- R08: p_i = w lambda~_i + r b~_i, so at given w, r and lambda~_i a lower b~_i lowers p_i.
- mathB-3: Corollary 2 now has no funding hypothesis. 'the conditions for (14)' (printed (25)) is correct.
- mathB-4: R=rT is defined in Proposition 6's first sentence before (iii) uses it, and d = tau_R R/N. Only the note is inaccurate (finding V3).
- N2: Table 2's caption calls all seven 'targets', and Y/N = 3 is a level.
- R04: the NEW sentence now follows the shares sentence. 'These values are illustrative. They are chosen ...' directly follows Table 2's parameters and targets. The comment block moved with the sentence.
- N1: Figure 3's demand curves stop at x_c ~ 0.94634 < x_H = 1, as the caption now says.
- R21: pi = (rho+delta)b/[1-(rho+delta)a] equals b~_m of (tildem). With lambda = 0, p_m = pi r.
- D74: Corollary 2 is the result the sentence summarizes, and its pointer now carries the conditions F fixed and g_w <= g_e.
- D73: 'stationary' matches Definition 1's stationary equilibrium.
- mathA-2: at c_o = 0, the shortfall D_{t+1} = (1+g)D_t + P_s c_t + r(T - l_t) proves that no feasible plan has other consumption or stock. At r = 0, plans that differ only in l_t are allowed. The new wording is exact.
- R02: Corollary 1(ii) states '(22) and funding hold under both' (printed (22) = eq:25). The proof now names the same conditions.
- mathB-5: lambda~_g = 1-x*+lambda~_m J(x*) >= 0 follows from p = w(1-x*) + p_m J(x*) and p_m = w lambda~_m + r b~_m. The proof's inequality p >= r b~_g then holds.
- mathB-6: A_rho is defined in Section 3 and again in B.1 at L1792. No undefined plain A remains.
- mathB-1: 'taken to be one ... including tasks reserved by rule' states the convention (20) needs for reserved tasks with finite gamma_i.
- D102: no CES sigma remains in Appendix C or E. sigma now means only the support indicator. The CES epsilon (C), epsilon_H (E) and epsilon_D, epsilon_S (D.2) are distinct elasticities. The perturbation epsilon in Lemma A.1(c)'s proof is a bound variable local to that proof, judged acceptable.
- mathB-2: (13) with b-bar_0 = 0 gives w/p >= 1/lambda-bar_0, hence r/p >= 1/[(w/r) lambda-bar_0]. The pointer is correct.
- D106: under (8) with tau_w = d = 0, work gives log((P_s+w+g_w)/P_s) and exit log((P_s+g_e)/P_s), so the displayed comparison is exact.
- R12: (27) with Delta = 0 gives (e^chi - 1)(P_s + g_e). d is no longer reused. Section 6's (e^chi - 1)(P_s + d) for a supplement d stays consistent with (8).
- D101: the remaining sentence stands as its own paragraph. The dropped sentence repeated D.2's 'Identifying the slope requires accounting for these responses.'
- R15: 'the same basket as in Section 3.3' points to sec:workers, where the basket and P_s are defined.
- D103: z_g, z_h, z_H are the basket's components, consistent with z = (1,0,0,h)^T (z_g = 1, z_h = h) and with the workers' c_g, c_h. No g_s, h_s or n_s remains. The algebra (kappa, q*, the 20/19 and q >= 4 example) is unchanged under the renaming.
- R16: 'enter the basket through z' matches D.3. P_s = p z_g + r z_h + w_H z_H is the D.3 two-item basket plus care.
- R09: 'when lambda~ falls' names the vector in the display w lambda~^T f. No 'total human requirements' remains outside comments.
- Greps outside comments: 'two-factor', 'basic living basket', 'total human requirements', g_s, h_s and n_s do not occur. 'contestable' occurs once, as plain English (L1421).

Not checked:

- Page layout beyond the PDF text. Where Table 1 prints was inferred from the text order (caption after the p. 4 footer), not from rendered pages.
- The full text of Korinek and Stiglitz (2019) and Korinek and Suh (2024) on whether machines accumulate from output. S1's 'first two' rests on the first-round source check.
- LaTeX compile log after the review round (no recompile was run). The PDF text was taken as given.
- Provenance comments that the review edits made stale. Example: L474's 'from main.tex L268, sentences 2-4, verbatim' now covers sentences 2 and 4 only, but the D6 note beside it records the drop.

### Second read-through

- **X1** (error; REWRITE L1137 (Section 6, paragraph after the Keynes sentence; main.tex L268 S5 with a cross-reference the rewrite added)). The pointer "The parents (Section 3.4)" now lands on a section that no longer mentions parents. Review edit D6 (REWRITE L476) dropped the parents example from Section 3.4 because it already prints in Section 2. The only remaining mention of the parents is in Section 2 (REWRITE L211). So "The parents" in Section 6 has no antecedent at the place it cites.
  - Fix: `The parents (Section~\ref{sec:owner}) may themselves finance that support from wages.` -> `The parents (Section~\ref{sec:description}) may themselves finance that support from wages.`
  - Disposition: applied (as V1).
- **X2** (imprecision; REWRITE L300 (Table 1, row x*; x_c)). Table 1 glosses x_c only as "the first open task at which machines cannot undercut labor". Lemma 2 also sets x_c = x_H when no such task exists, and the paper uses that case: Section 7's path has "the ceiling x_c = 1" with lambda = 0. There D(x) = 1-(rho+delta)a > 0 at every task, so machines do undercut labor at x_c at a high enough wage, and the table's gloss is false for that case.
  - Fix: `ceiling, the first open task at which machines cannot undercut labor (Lemma~\ref{lem:ceiling})` -> `ceiling, the first open task at which machines cannot undercut labor, or $x_H$ if there is none (Lemma~\ref{lem:ceiling})`
  - Disposition: applied.
- **X3** (imprecision; REWRITE L1209 (Section 7, first paragraph; main.tex L745 S3, edited) against Table 2 (REWRITE L1186)). The text says the parameters are chosen so that site rent is 6.5 percent of the basket. The new Table 2 says the parameters are chosen to match a site-share target of 0.06, and that 0.065 is only the value at the rounded parameters. The two descriptions of the calibration target disagree. The text's other items (about half, about a fifth, 60 percent) agree with the table's targets.
  - Fix: `site rent is 6.5 percent of the basket` -> `site rent is about 6 percent of the basket`
  - Disposition: not applied: the authors' sentence is true as written (the solved share is 0.0654), and Table 2 lists the 0.06 target and the 0.065 value separately.
- **X4** (imprecision; REWRITE L1767 (Appendix B.1, Assumption B.1) against L1785-1797 ((B.2) and Definition B.1)). Assumption B.1 gives every good a nonempty finite set of feasible methods. A task-produced good, however, has one method for each assignment M of its open tasks by (B.2), which is a continuum. Definition B.1 counts these assignments among the feasible methods ("no feasible method of any good, including any assignment of a task-produced good's tasks"). As written, the assumption contradicts the definition that uses it.
  - Fix: `Each good $i\ne m$ has a nonempty finite set of feasible methods;` -> `Each good $i\ne m$ has a nonempty finite set of feasible methods (for a task-produced good, of its inputs other than tasks, each combined with any assignment of its tasks as in~\eqref{eq:assignment});`
  - Disposition: applied, reworded: "except that for a task-produced good the finite set lists combinations of its inputs other than tasks, each joined with any assignment of its tasks as in (B.2)".

Passed (14):

- Section 7 numbers recomputed with a bisection solver (script /tmp/claude-0/-home-user-labor/904c7da5-c8e1-5390-ac85-b6fa3b59f016/scratchpad/build/checks/verify/eq2.py): x*=0.82987, x_c=0.94634, v=0.07165, Y=3.01320, N_a=0.60165, final-task hours 0.51264, N P_s=0.02599, rent+interest 0.03520; Figure 3: baseline 2.76/0.60, lambda=0 gives 2.46/0.56, gamma halved gives 2.66/0.59; path: participation 0.13 at eta=0.01 and 0.018 at eta=0.001; final good x1.78 and space 1/426 from eta=1 to 0.001; support funded at every grid point; threshold (T-Nh)/(N pi)=0.119
- Table 2 last column: 0.456, 0.196, 0.469, 0.065, 0.148 recomputed from the equilibrium
- Section 5.2 income split 0.55/0.13/0.32 and bound 0.81; Section 6 rent coverage 0.38; Corollary 3 remark 1.71 and 0.66 baskets per person (lambda=0, x=1, rho=0.09)
- Cost system: matrix (3) rows and gross outputs y=(Y,X,deltaX,hY) are consistent with Definition 1(v); (5) derived from (2); spectral radius sqrt((rho+delta)a); Lemma 1(i)-(iii) coefficients and the identity P_sY=wN_a+r ell+rho V_m X
- Proposition 2 closure and both conditional derivatives; Corollary 1(i) rate and 1/(1-gamma lambda~_m)=1+lambda v/b
- Lemma 2 proof: p_m gamma - w = [(rho+delta)br gamma - wD]/[1-(rho+delta)a]; limit of v/P_s at a binding ceiling
- Theorem 1 proof: N_D strictly decreasing, p'(x) and d(v/P_s)/dx formulas, the zero-rent and boundary exclusions, the income decomposition at the crossing
- Proposition 3, (D.1), Section 6's reservation wage (e^chi-1)(P_s+d), Corollary 2 remark's in-work bound
- Lemma A.1(b) discounted-sum bound with 1+rho=1/beta; A.1(c) perturbations
- Proposition 5 converse proof (X>0 and w>0 when r>0)
- Loom example ($20, $16); D.3 illustration (kappa=20/19, q>=4); D.5 index 0.31 and 0.08; Table D.1 vs Appendix F intervals; 4.8x from +277% and -21%; gap of about 19 points (65.8-47.2)
- Appendix C limits of the CES share; B.6 task-cost formula
- Cross-references to Sections 3.3, 3.5, 9.2, Appendix B.5, D.1, D.3 and equation numbers (14), (18)-(22), (25), (29) land on the intended objects
- Abstract and Section 1 roadmap against the body; Section 2 description against Assumptions 1-5 and Definition 1

Not checked:

- Contents of the figure images (curves, axis ranges, annotations) beyond their captions and legends
- Empirical values in Section 8, Figures 4-6, Figure D.1 and Table D.1 against the data or code
- The claim that the second calibrated curvature (about 15.5) makes task automation raise w/P_s; not recalibrated
- Fidelity of the literature attributions (Korinek and Suh, Trammell and Korinek, Caselli and Manning, Rognlie, Knoll et al.) to the cited papers
- Reference list entries
- Proposition E.1 beyond its statement (excluded as STATE Open 12(e))

