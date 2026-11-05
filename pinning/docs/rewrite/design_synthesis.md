# Synthesis: the recommended architecture for the rewrite

This note recommends one architecture for rewriting *Pinning the Wage to Scarcity and Technology*. It is design only. Nothing under `/home/user/labor` was changed, and no git command that writes was run.

- Line numbers are lines of `/home/user/labor/pinning/paper/main.tex` (983 lines).
- "A", "B" and "C" are the three designs in this folder. "Inventory" means `inventory_results.md` (R-numbers), `inventory_primitives.md` (I- and O-numbers) or `inventory_section2.md` (Lit ¶1–4, remarks R1–R3).
- Every LaTeX block below is cut verbatim from `_work_synthesis/drafts_synthesis.tex`, which passes `checks/lint_tex_structure.py` (ALL GREEN). No TeX engine is installed here, so nothing was compiled.
- Lucas (1978) could not be read here. STATE.md's log of 2026-11-05 says Stella supplied it as a PDF in an earlier session, but it is not committed. I rely on the task's description of its order. Anything further is general knowledge.

**Her decisions on the rewrite's form.**
- While this synthesis was being written, the parent session committed c632516 (13:57) to STATE.md. It records "Her decisions on the rewrite's form, also the same day" (Log 2026-11-05).
- None of the three designs saw them, and the judges did not either.
- They are the authors' calls, so this note adopts them and says where they change a design or a judge's suggestion. They are:
  - a smaller stated economy, with the generality in remarks or an appendix;
  - one paragraph on what is easy and what is hard;
  - a formal definition, with a note that the concept is standard;
  - a remark after each result on what it does not depend on;
  - precedence in the introduction in place of a survey;
  - general results first, then examples, then AI;
  - proofs of Propositions 1–3 in the text, numbered assumptions;
  - an owner who optimizes, with ρ = 1/β − 1, the user cost as its first-order condition, and support a commitment in its budget;
  - Magnus's third note: the research question, "can you have an economy where people don't do any work?", opens the introduction.

---

## 0. The choice

### 0.1 Which design, and why

**Design B (concrete-first) is chosen.**

**How the rule was applied.**
- The highest summed total is C's: C 111, B 107, A 101.
- The mathematician's fatal-flaw list includes a false result in C. Corollary 1 (main_C.tex 426–439) fails inside C's own Definition 1, which admits an in-work payment: with g_w = P_s, participation tends to F(log 2) = 0.693, not 0 (`judge/j3_counterexamples.py`; rerun here). So the rule's exception applies to C.
- The next total is B's.
  - The mathematician lists a B item too: Definition 1 is wrong once an instrument is nonzero.
  - But its verdict says that in B "no restated result is false as drafted", and its first entry is "No structural fatal flaw in any design".
- A has two results that are false as drafted (Corollary 2 without "F fixed"; Proposition 6 without "bounded total hours").
- Applied literally to every design, the exception would leave none. I therefore read it as excluding designs whose stated results are false as drafted. That excludes C and A and leaves B.
- All three judges rank B first (theorist B, A, C; referee B, A, C; mathematician B, C, A). Her decisions point the same way: they prefer a small stated economy, which is B's.

**What B brings.**
- One concrete economy: Appendix B's economy (681–686) plus a wall of closed tasks. Every agent and every market is explicit, and machines are durable.
- Theorem 1: existence and uniqueness of that very equilibrium.
- A parameter table with targets (Table 2).
- The real-wage fork inside the solved economy.

**The structural defect, and how it is fixed.**
- All three judges object that B states two economies with two definitions, and that its network comes after Section 3's results.
- The fix follows her decision, not design A's route:
  - The four-good economy is the only economy the main text states.
  - The general network is an explicit extension in Appendix B.1 (Assumption B.1, Definition B.1, Proposition B.1). It is stated before the network versions of the results are, and the remark after each main-text result points to it.
  - The cost recursion, the paper's organizing idea (74, 86, 223), appears in §2.2 as the four-good input–output system.
- So every result is stated in an economy already defined, and the main text has one economy and one definition.

### 0.2 Grafts

| From | Graft | Where it lands |
|---|---|---|
| A | Consumption taken from the budgets in Definition 1, so it is right under every instrument | Def. 1(ii)–(v); eq. `budget`, `ownerseq`, `govbudget` |
| A | "When ρ = 0" in place of "in the flow benchmark": exact for every δ | Lemma 1(iii); Props. 2, 5; Cor. 3; the readings at 245, 257, 351 and 353; §4.2's ρ = 0 remark |
| A | Price coefficients are at least the physical ones, with equality when ρ = 0 | Lemma 1(iii), Prop. B.1(a) |
| A | H = {γ_M = 0} ∪ R: closure by capability or by rule, kept apart in Definition 3 | Ass. 1, Def. 3, Ass. B.1 |
| A | The AI paragraph after Definition 3 | §2.6 |
| A | The path's funding proved for η ≤ (T − Nh)/(Nπ) ≈ 0.119; X ≤ ηT/[h(1 − aδ)], so R/I → 1 | §6 |
| A | Corollary 3(ii) as a statement about prices at given methods | Cor. 3 and its remark |
| A | Notation repairs: bold **I**; g_w, g_e; ω; k for inputs; ξ | Table 1, §2.3 of this note |
| C | The owner chooses how much land to rent, so Proposition 6(i) is a result under a rental-value tax | Def. 1(iii), Lemma A.1(a), Prop. 6(i) |
| C | Support the government can provide in place of the owner (σ = 0) | §2.5, Prop. 3's remark, eq. (16) |
| C | The clause that no feasible method costs less than the price | Def. B.1, Prop. B.1(c)'s proof |
| C | The carry-over list, recast as the five statements that need ρ = 0 | §4.2 |
| C | Table A.1 recast as "where the paper departs from the stated economy" | Table B.1 |
| C | What funded support requires at ρ = 0 (κ ≥ 1), and how the measured 0.30 fits | §5 |
| C | The port discipline: exact one-match replacements on a scratch copy, checks before main.tex | §6 of this note |
| Theorist, and her decision | The owner lives forever with discount factor β, ρ = 1/β − 1: every agent optimizes, and the user cost is its first-order condition | Ass. 5, Lemma A.1 |
| Referee | Data, compute and datacenters mapped to the model's inputs; Figure 3's experiments framed as AI scenarios | §2.6, §6 |
| Mathematician (on C) | Corollary 2's participation limit needs no public payment that favors work (g_w ≤ g_e), as well as "F fixed" | Cor. 2 |
| Her decisions | Primitives sentence; easy and hard paragraph; standard-concept note; does-not-depend remarks; results, then examples, then AI; proofs of Propositions 1–3 in the text; the question first | §2, §3, every result, §§3–6, §1 |

### 0.3 Every defect the judges found in B, and its fix

| # | Judge | Defect in B | Fix here |
|---|---|---|---|
| 1 | all three (fatal) | Def. 1 wrong once an instrument is nonzero: workers maximize (8), c_o omits the tax, final-good clearing omits transfers | Consumption from the budgets (`budget`, `ownerseq`, `govbudget`). Walras checked under five policies (`verify_synthesis.py` S3: \|C − Y\| ≤ 1.3·10⁻¹⁵) |
| 2 | theorist (fatal) | Section 4 extends Prop. 2 to networks without b̃_m > 0 | Prop. B.1(b) states b̃_m > 0; without it the closure is 0/0. In the stated economy b > 0 gives it |
| 3 | all three | Two economies and two definitions; network after Section 3's results; recursion late | One stated economy and one Def. 1. The network is an explicit extension (App. B.1) to which each remark points. The recursion is in §2.2 |
| 4 | theorist | 417–423's replacement case has no formal home | σ = 0 (public provision) in §2.5; Prop. 3's remark; (16) |
| 5 | theorist, referee | The owner's land supply is stipulated, so Prop. 6(i) is partly true by definition | The owner chooses ℓ; Lemma A.1(a) gives ℓ = T at r > 0 for every τ_R ∈ [0, 1] |
| 6 | mathematician | "The owner is indifferent to the size of its stock" contradicts utility increasing in c_o in a static model | The owner lives forever with discount factor β. Lemma A.1 proves the constant plan optimal at the user cost, and the converse when c_o > 0 |
| 7 | theorist | "γ_L = 1 is a choice of units" overclaims | γ_L = 1 is part of Ass. 1, with no claim of generality; Ass. B.1 drops it |
| 8 | theorist | Cor. 3 part 2 is about a configuration that is not an equilibrium, unsaid | A price statement at given methods; its remark says why it is not an equilibrium |
| 9 | referee | H narrowed to capability; 532, 574, 878 need rewording | H = {γ_M = 0} ∪ R (graft from A); 532, 574, 878 stay true |
| 10 | referee, mathematician | Needs ρ = 0 qualifiers; two false prose sentences ("physically uses … smaller"; "b̃_s > B_s") fail when ρ = 0 < δ < 1 | Lemma 1(iii): "no larger" and "≥, with equality when ρ = 0"; §4.2 lists exactly what needs ρ = 0 |
| 11 | mathematician | Def. 4's "workers choose as in Definition 1" needs preferences for a general basket | Ass. B.1 states log min over i with z_i > 0 of c_i/z_i, minus χn |
| 12 | mathematician | "Every selection productive" | Def. B.1 requires productivity of the selected A_ρ only, and each human chain carries its own productivity condition |
| 13 | referee | Word estimate of +1,000 looks low | Counted: about 8,600 words of main-text prose against 7,988 now (§1.6). The network's words are in the appendix |
| 14 | referee | Section 4's title "Any production network" is non-standard | Section 4 is "Purchasing power and income"; the network is App. B.1 |
| 15 | theorist, referee | Risk: Q group re-pointed, new U group with x_H, about 30 labels | Kept, with the port discipline and a check plan (§6 of this note) |

### 0.4 The first proposal's open questions

**"The appendix": A.1 or B?**
- STATE.md's log of 2026-11-05 records "like the appendix" as Stella's own gloss, not Magnus's. She meant A.1, and she does not hold to it.
- Following her later decision, the stated economy is Appendix B's (681–686), plus a wall.
- A.1's list of parts (574–594), closed in B's way, becomes the extension in App. B.1.

**Durable machines in the stated economy?** Yes; her owner decision (ρ = 1/β − 1) presumes them. The earlier claim holds: the closure and the price bounds carry over on the user-cost coefficients (Claims 1 and 2). But its list of what needs the flow benchmark was too short. The full list, each item stated "when ρ = 0":
- the basket identity P_s = wL_s + rB_s (308);
- (15) as an equality;
- the interest term in Proposition 6(iii) and Corollary 3;
- the equivalence in (17);
- the readings at 245, 257, 351 and 353.

**Scope beyond Sections 1–3?** The whole paper.
- Sections 1–6 are rebuilt.
- Measurement, history and AI are moved and lightly edited.
- The appendices are regrouped.

---

## 1. The recommended architecture

### 1.1 Outline

The order is hers: general results (§§3–5), then examples (§6), then AI (§9, with the conclusion).

| § | Title | Contents | From (main.tex) |
|---|---|---|---|
| — | Abstract | AI in the first sentence; results; the 4.8 fork; κ = 0.30 (sketch below; about 210 words, under the 250 limit) | 63–65; 540; 542 |
| 1 | Introduction | The research question first (drafted below); AI (540); the two questions (74, 76); what we do; results (86–90, restated where statements changed); evidence (479, 494, 513); precedence (the inventory's four paragraphs, folded in with no survey heading); roadmap | 70–96, 100–132 |
| 2 | The economy | The primitives sentence. 2.1 tasks, machines, land (Ass. 1–3); 2.2 the cost system; 2.3 workers (Ass. 4); 2.4 the owner and support (Ass. 5); 2.5 government; 2.6 equilibrium (Defs. 1–3, the standard-concept note, the AI paragraph, Table 1) | 140–170, 199–225, 268–282, 590–594, 665–675, 681–686, 540 |
| 3 | Equilibrium | The easy and hard paragraph. 3.1 prices: Lemma 1; Prop. 1 with Figure 1, the loom (195) and its proof; Prop. 2 with its proof, Figure 2, the two channels (251) and (6). 3.2 participation: Prop. 3 with its proof; 294, Allen; the enclosure and Lewis paragraph; (11). 3.3 existence and uniqueness: Lemma 2, (21)–(24), Theorem 1, Cor. 1. A remark after each result | 155–195, 227–324, 687–743 |
| 4 | Purchasing power and income | 4.1 Prop. 4, the readings at 351–353, Cor. 2, 374–376. 4.2 Prop. 5, 393 with the factor-share sentence, the ρ = 0 remark | 328–393, 749–757 |
| 5 | Distribution: rent taxation and a uniform transfer | Terminal, pure and site rent defined; Prop. 6; (16) with public provision; what funded support requires; Cor. 3; 425, 437–439 | 223–225, 395–439 |
| 6 | A numerical economy and an automation path | Table 2; the instance (745); Figure 3 with the AI framing; the statics sentence (324); the path, proved where it can be | 313, 324, 745–747 |
| 7 | Measurement | Unchanged; Figures 4–6 | 475–528 |
| 8 | History and stabilizers | 8.1 four configurations (Figure 7), shortened, opening with 326; 8.2 stabilizers (530–536), with reservations named as a policy | 326, 441–473, 530–536 |
| 9 | Artificial intelligence and conclusion | 540–550 less what moved to §1 and §2.6; Future Work condensed to two paragraphs, with Uzawa (1961) | 538–559 |
| A | Proofs | Lemma A.1 (the owner); Lemmas 1–2; Theorem 1; Cors. 1–3; Props. 4–6. Props. 1–3 are proved in the text | 728–741, 751–757, 769–775, 413–415 |
| B | Extensions of the economy | B.1 production networks (Ass. B.1, Def. B.1, the human chain, Prop. B.1); B.2 several non-produced inputs; B.3 several machine types and trade (inventory R3, `check_open.py`); B.4 worker types; B.5 ideas and institutional rents; B.6 task-level costs (20); Table B.1 | 574–588, 622, 326, 334, 576–586, 654–663, 677 |
| C | Expenditure shares under substitution | (26) with weight ω, opening "This appendix departs from Assumption 4" | 759–763 |
| D | Fiscal transition | D.1 with g_w, g_e; D.2 with the incidence citations; D.3 on the price basis; D.4; D.5; Table D.1; Figure D.1 | 765–874 |
| E | Human-required tasks | "Let the set H of Assumption 1 have positive measure"; E.1's proof applies to reserved tasks unchanged | 876–890 |
| F | The financing and production accounts | The mapping paragraph on the price basis | 892–910 |

The back matter follows: the data, notation and checks note (913), with its notation sentence replaced by "Table 1 lists the notation"; the AI declaration (915–917); and the references, less six (§1.4).

### 1.2 Front matter

**The abstract.** A sketch built from B's, with "data" added for the special issue's theme. It could also open with the research question; that is the authors' call.

```latex
\begin{abstract}
\noindent Artificial intelligence, and the investment in computing and data behind it, can make machines better at tasks and can reduce the labor needed to build and run the machines themselves. We study what these two kinds of automation do to wages when machines are produced from labor, machine services, and inputs that production cannot add to, such as land. In a stationary economy with task assignment, durable machines, and workers who choose between work and support outside it, we give conditions under which equilibrium exists and is unique. Both kinds of automation can lower the wage relative to rents on non-produced inputs. Embodied rents cap what an hour's wage buys, good by good, while feasible human production supplies a floor. If the wage--rent ratio tends to zero, wage purchasing power over goods that embody non-produced inputs tends to zero, and with support maintained so does participation. U.S. wages deflated by durables and by shelter prices diverged by a factor of 4.8 over 1964--2024. A tax on pure rents funding a uniform transfer redistributes purchasing power without changing the supply of the taxed input or withdrawing benefits upon employment; full capture of measured U.S. site rents would cover about 30 percent of a subsistence basket per person in 2025.
\end{abstract}
```

**The opening of the introduction**, with her question first, and the two changed precedence sentences. The opening is new prose for the authors to re-voice. Its numbers are verified (`_work_synthesis/path_numbers.py`):
- participation 0.6017 at baseline;
- 0.5640 once machine-making needs no labor;
- 0.1340 at η = 0.01;
- 0.0179 at η = 0.001.

```latex
\section{Introduction}\label{sec:intro}

Can there be an economy in which people do not work? The usual route is a machine that can do everything a person can. This paper studies another, on which machines need not take over every task: an hour's wage buys less and less of what a life outside work also needs. Machines are produced from labor, from machine services, and from inputs that production cannot add to, such as land. Automation can then drive the wage toward zero relative to the rent on those inputs. An hour's wage still buys manufactured goods, but ever less space, and a person supported outside work, by a family or by public provision, has ever less reason to take a job. In the economy we solve, the share of people working falls from 60 percent to 13 percent once making machines needs no labor and machines become a hundred times more capable at every task, and below 2 percent at a thousandfold gain, while relative capability at the last task remains a hundred times that at the first.

Artificial intelligence is the leading candidate for such automation. It can make machines effective at tasks that only people could do, and it can reduce the labor needed to supply machine services, since software generation, chip design, datacenter operation, logistics, and research are part of the chain that produces them. % 540

% ... 72, 74, 76, the results (86-90), the evidence (479, 494, 513), then the precedence paragraphs (inventory Lit 1-4).
% Lit paragraph 1, second sentence, becomes:
In Acemoglu and Restrepo (2018), whether every task is eventually automated depends on the long-run rental rate of capital relative to the wage, and new tasks in which labor has a comparative advantage offset automation; we set them aside (Section~\ref{sec:technology}) and take as given the direction of technical change, which Acemoglu and Restrepo (2018) and H\'emous and Olsen (2022) make endogenous.
% Lit paragraph 4, second sentence, becomes:
In our economy, the income share labor loses as the wage--rent ratio falls goes to the owner, as rent on land and as the return on machines; when $\rho=0$, all of it is rent (Proposition~\ref{prop:5}).
```

**Paragraph plan for the rest of the introduction.**

| ¶ | Content | Source |
|---|---|---|
| 3 | A firm indifferent between a worker and a machine ties the wage to the substitute's cost | 72 |
| 4–5 | The two questions: what prices the substitute; what prices exit | 74, 76 |
| 6 | What we do, in three sentences:<br>• one small economy stated in full;<br>• its equilibrium proved to exist and to be unique;<br>• results first, then a solved example, then AI | new |
| 7 | Results | 86–90, restated where §3 of this note changes a statement |
| 8 | Evidence: the fork 4.8×; κ = 0.30; financing 65.8% against effort 47.2% in 2023 | 479, 494, 513 |
| 9–12 | Precedence: the inventory's Lit ¶1–4. The precedence sentences on Korinek–Stiglitz (2019) and Korinek–Suh (2024) survive, as STATE asks | inventory §3.1 |
| 13 | Roadmap | replaces 92–96 |

### 1.3 Where every result, equation, figure and table goes

**Results.**

| Object (old lines) | New home | What changes |
|---|---|---|
| Threshold, H, "usual indifference condition" (155–170) | Ass. 1, Def. 2, Prop. 1(i) | 163–165 is false at the corner (Open 12i); replaced by the corner and boundary inequalities |
| Prop. 1 (186–193) | §3.1, Prop. 1, proved in the text | The boundary and corner inequalities are added. Differentiability comes from Ass. 1. (iii) moves into Prop. 3 |
| Loom example (195) | §3.1 | Verbatim |
| Cost recursion (197–225) | §2.2 (four goods); App. B.1 (any table) | The durable good is entered at ρ + δ in prices and δ in quantities. Terminal, pure and site rent move to §5 |
| Prop. 2 (231–243) | §3.1, Prop. 2, proved in the text | Price coefficients in closed form (`tildem`). The hypotheses are an interior margin and r > 0; the other three become conclusions |
| 245, 257 | §3.1 | "When ρ = 0" |
| Two margins (247–251) | Def. 3 and the AI paragraph (§2.6) | Defined as changes in primitives |
| Section 4 prose (268–282, 294–300) | §2.3, §2.4, §3.2 | 268's sentence on wage-financed parents moves to §5 (437) |
| Prop. 3 (284–292) | §3.2, Prop. 3, proved in the text | "In every equilibrium with τ_w = d = g_w = g_e = 0". (10) joins it |
| (11), 317–321 | §3.2 | Derived; L_s and B_s are physical (as at 717) |
| "Proves existence and uniqueness" (322) | Theorem 1 | Now true (Open 12h) |
| Statics (324), 743 | Cor. 1; "both channels" in §6 | The rate in (i) is new. §6 discloses that at the other calibration root (k ≈ 15.5) task automation raises w/P_s |
| Heterogeneity (326) | §8.1 opening; App. B.4 | — |
| Human method (334) | App. B.1, the human chain; in the main text, the final good made by hand | Closed under inputs; contains neither machines nor machine-hours; productive |
| Prop. 4 (336–349) | §4.1, Prop. 4; the general (13) in its remark and in Prop. B.1(c) | In the stated economy: space at w/r, the final good between 1 and (w/r)/b̃_g |
| 351, 353 | §4.1 | Price-basis readings |
| Corollary (355–372) | §4.1, Cor. 2 | Numbered. "F fixed" kept; g_w ≤ g_e added; B_s ≥ h automatic. Good-by-good in Prop. B.1(d) |
| 374–376 | §4.1 | Points to §6. The "hundred-to-one" anchor is kept |
| Prop. 5 (380–391) | §4.2, Prop. 5 | Identity with ρV_mX; (15) an inequality, with equality when ρ = 0 |
| 393 | §4.2 | Qualified, plus the factor-share sentence (Karabarbounis–Neiman; Rognlie; Knoll–Schularick–Steger) |
| Prop. 6 (399–415) | §5, Prop. 6 | (i) is a result (Lemma A.1(a)). (iii) adds the return on machines |
| (16), 417–425 | §5 | Public provision σ = 0 is (16)'s case; 423's replacement case is formal |
| Fiscal corollary (427–435) | §5, Cor. 3 | (i): non-wage share → 1, and R/I → 1 when ρ = 0. (ii): a price statement. A line for several inputs (STATE's note on (17)) |
| 437–439 | §5 | The pointer becomes Appendix A |
| Section 8 (441–473) | §8.1 | Shortened by a third; 473 stated as a conditional |
| Section 10 (530–536) | §8.2 | 532 reworded (R21); reservations as policy |
| Section 11 (538–550) | §1, §2.6, §9 | AI last, as she decided |
| Section 12 (552–559) | §9 | Condensed (Open 12k) |
| A.1 (572–594) | §2 (people, government, equilibrium); App. B.1–B.4 (network, inputs, machine types, worker types) | — |
| Table A.1 (596–620) | Table B.1 | Departures from the stated economy |
| A.2 proofs (624–652) | §3 (Props. 1–3); App. A and B.1 (the rest) | (18) replaced by ∂s/∂P_s; the fixed-point step added to (19) |
| A.3 (654–663) | App. B.6 | "At an interior margin" |
| A.4 (665–675) | Ass. 2, eq. (2) (`unitcost`) | The one-period advance is the user cost at δ = 1; "distinct timing conventions" is cut |
| A.4 ideas (677) | App. B.5 | — |
| App. B setup and ceiling (681–687) | §2.1, Lemma 2 | The ceiling is not called "closed" |
| (21)–(24), 708 | §3.3 | n_D, n_S become N_D, N_S |
| Three-row system (710–717) | §2.2 (four rows); Lemma 1 | — |
| Lemma B.1 (719–741) | Theorem 1; App. A | Every alternative is excluded; funding is necessary and sufficient |
| Instance (745) | §6, Table 2 | "Full-chain cost of consumption" relabeled (decision 6) |
| Path (747) | §6 | Funding proved for small η; (25) proved along the path; R/I → 1; 0.018 at η = 0.001; the fork in numbers |
| App. C identity (749–757) | App. A (Prop. 5's proof) | Interest term |
| App. C CES (759–763) | App. C | α → ω |
| App. D (765–874) | App. D | D.3 on the price basis; m_w, m_e → g_w, g_e |
| App. E, F (876–910) | App. E, F | H pointer; price-basis mapping |

**Equations.**
- Old (1)–(17) keep their labels where the object survives. Printed numbers change.
- (13), the general purchasing-power bounds, is displayed in the remark after Prop. 4 and used by Prop. B.1(c).
- New labels: `unitcost`, `tildem`, `utility`, `budget`, `ownerseq`, `ownerbudget`, `govbudget`, `assignment`, `income`.
- (18) is cut. (19)–(28) move with their appendices: (19) to Prop. B.1, (20) to App. B.6, (21)–(25) to §3.3, (26) to App. C, (27) to App. D.1 and (28) to App. D.3.

**Figures.**
- Figures 1–2 stay in §3.1.
- Figure 3 moves to §6. Its caption is unchanged except that "Appendix B" becomes §6; the AI framing goes in the text, so the Q[CAP] templates stand.
- Old Figures 5–7 become Figures 4–6, in §7.
- Old Figure 4 becomes Figure 7, in §8.1.
- Figure D.1 is unchanged.

**Tables.**
- New: Table 1 (notation, §2.6) and Table 2 (the instance, §6).
- Table A.1 becomes Table B.1.
- Table D.1 stays.

### 1.4 Section 2's content (the survey, 98–132)

Her decision is "precedence in the introduction in place of a survey". The inventory's four paragraphs (`inventory_section2.md` §3.1) are folded into the introduction without a heading.

| Survey content (lines) | Home |
|---|---|
| Lead and frames (100) | Cut |
| 2.1 marginal product (104) | Cut. Uzawa (1961) moves to §9, as further work |
| 2.2 search and matching (108–112) | Precedence ¶2 (Mortensen–Pissarides; Pissarides; Shimer; Hagedorn–Manovskii; Hall; Ljungqvist–Sargent's fundamental surplus fraction). Diamond (1982) is dropped |
| 2.3 task models (116) | Precedence ¶1 (Zeira; Acemoglu–Autor; Acemoglu–Restrepo 2018, 2022), with the changed sentence keeping Hémous–Olsen (2022). Autor (2015) is dropped |
| 2.3: trade as a second machine rental | App. B.3 (inventory R3; `checks/corner/check_open.py`) |
| 2.3 and 2.4: wedges | The remark after Definition 1 (Shapiro–Stiglitz; Card et al.; Acemoglu–Restrepo 2026) and §8.2. Manning (2003) is dropped: monopsony is a markdown |
| 2.5 classical (124) | Marx, Polanyi and Lewis go to §3.2's enclosure paragraph. Ricardo (1817), Malthus (1798) and the 1821 chapter go to §8.1. George (1879) stays at 90 and 439 |
| 2.6 automation and the wage (128) | Precedence ¶3: Korinek–Stiglitz; Korinek–Suh, reworded to credit their scarce-factor remark; Sachs–Kotlikoff; Susskind; Caselli–Manning, per their abstract; Aghion–Jones–Jones, pointing to App. E. Precedence ¶4 holds Moll–Rachel–Restrepo, with the changed sentence |
| 2.7 empirical measures (132): factor shares | §4.2. Piketty–Zucman (2014) is dropped |
| 2.7: welfare ratio | §3.2 (Allen 2001). Clark (2005) is dropped |
| 2.7: payroll incidence | App. D.2 (Gruber; Kugler and Kugler; Saez, Schoefer and Seim) |

The six dropped references are Samuelson (1966), Diamond (1982), Autor (2015), Manning (2003), Piketty and Zucman (2014), and Clark (2005). Candidates to add are decision 9.

### 1.5 What is cut

- Section 2 as a section, and Section 12 as a section.
- Proposition 1(iii); the display (18); 205's flow-benchmark sentences; A.4 as a subsection.
- 592's unnamed consumption tax, which no equation uses.
- The data note's scalars sentence (913).
- About a third of Section 8.
- Future Work's monetary-policy and sovereign-fund paragraphs, cut to a sentence each.
- The general network: it leaves the main text for App. B.1. That is her decision, and it is not a cut.

### 1.6 Length

All counts use one counter (`_work_synthesis/wc_strict.py`), which counts prose words only and drops comments, math and tables.

**Now.** The main text, 70–559, is 7,988 words; the survey is 1,021.

**After.** Section 2 is 2,052 words. By the same counter, A's Section 2 is 2,262 and B's 1,864, before B's network subsection.

The drafted blocks:

| Block | Words |
|---|---|
| Introduction opening | 317 |
| §3 | 1,111 |
| §4 | 547 |
| §5 | 480 |
| §6 | 256 (Table 2 excluded) |

Adding the passages they keep from main.tex gives about 8,600 words of main-text prose:

| Section | Words (about) |
|---|---|
| §1 | 1,380 |
| §2 | 2,050 |
| §3 | 1,260 |
| §4 | 800 |
| §5 | 715 |
| §6 | 430 |
| §7 | 580 |
| §8 | 750 |
| §9 | 630 |
| **Total** | **8,600** |

**The appendices grow.**
- Appendix A has 671 drafted words plus Lemma B.1's proof.
- Appendix B.1 has 639 drafted words.
- B.2–B.6 take about 700 words moved from Appendix A.

I have not checked Economic Modelling's length limit.

---

## 2. LaTeX drafts of the model section

### 2.0 Preamble

These lines replace 35–38.
- Lemmas get their own counter.
- The corollaries are numbered.
- A starred remark environment carries the does-not-depend remarks.

```latex
% ---- preamble: replaces main.tex lines 35-38
\theoremstyle{plain}
\newtheorem{theorem}{Theorem}
\newtheorem{proposition}{Proposition}
\newtheorem{lemma}{Lemma}
\newtheorem{corollary}{Corollary}
\theoremstyle{definition}
\newtheorem{assumption}{Assumption}
\newtheorem{definition}{Definition}
\theoremstyle{remark}
\newtheorem*{remark}{Remark}
% in the appendix, add \counterwithin{lemma}{section} and \counterwithin{assumption}{section} and
% \counterwithin{definition}{section} beside main.tex 562-565, so they print as Lemma A.1, Assumption B.1, Definition B.1
```

### 2.1 Section 2, complete

```latex
\section{The economy}\label{sec:economy}

This section states the economy before deriving anything; Table~\ref{tab:notation} collects the notation. Time is discrete, and we study stationary equilibria, in which prices and quantities are the same in every period. The primitives are the relative-productivity schedule $\gamma$ and its wall $x_H$; the recipe $(a,\lambda,b)$ for building a machine and the machine's depreciation rate $\delta$; the land $T$; the $N$ workers, the space $h$ in their basket, and the distribution $F$ of their costs of work; the owner's discount factor $\beta$ and utility $u$; and the policy $(\tau_R,\tau_w,d,g_w,g_e,\sigma)$. Each is used by a result below. Appendix~\ref{app:networks} extends the results to any production network, with several non-produced inputs and a choice among methods.

\subsection{Tasks, machines, and land}\label{sec:technology}

The economy has four produced goods (a final good made by performing tasks; machines; the machine-hours that machines supply; and space) and one non-produced input, land.

\textbf{Tasks.} One unit of the final good requires one unit of each task $x\in[0,1]$, each in equal amount (Leontief aggregation over tasks): the good's unit cost is the sum of its tasks' unit costs. % 140-142
One human-hour completes $\gamma_L(x)$ units of task $x$; one machine-hour completes $\gamma_M(x)$. Relative human productivity is % 142-144
\begin{equation}\label{eq:1}
\gamma(x)=\gamma_L(x)/\gamma_M(x),
\end{equation}
the number of machine-hours that do the work of one hour at task $x$. Some tasks are closed to machines: machines cannot perform them, $\gamma_M(x)=0$, or they are reserved for people, by law or because the good is defined by its human performance.

\begin{assumption}[tasks]\label{ass:tasks}
One hour completes one unit of every task, $\gamma_L=1$. The tasks closed to machines form the set $H=(x_H,1]$, with $x_H\in(0,1]$, so that $H$ is empty when $x_H=1$. On the open tasks $[0,x_H]$, $\gamma$ is positive and continuously differentiable, with $\gamma'(x)>0$ for $0<x<x_H$.
\end{assumption}

Relabeling the open tasks so that $\gamma$ increases changes the measure of no set of tasks; we place the closed tasks after them, and Figure~\ref{fig:1} draws $H$ as a wall at the right edge of the schedule. The assumption restricts only the relabeled schedule, which has no jumps or flat stretches below $x_H$. A reservation is a rule, not a capability: lifting it opens tasks without any change in machines. The schedule $\gamma$ and the set $H$ are exogenous; new versions of tasks in which people hold a comparative advantage would raise $\gamma$ at the tasks they replace, the reverse of task automation (Definition~\ref{def:automation}), and we do not model their creation.

\textbf{Machines.} A machine is itself produced: from other machines, from labor, and from land, such as a site, a mineral deposit, or the ground under a plant or a datacenter. % 74

\begin{assumption}[machines]\label{ass:machines}
Building a machine takes $a\ge0$ machine-hours, $\lambda\ge0$ hours of labor, and $b>0$ units of land services. A machine supplies one machine-hour per period, and a fraction $\delta\in(0,1]$ of the machine stock wears out each period. With $\rho$ the owner's rate of time preference (Assumption~\ref{ass:owner}), $(\rho+\delta)(a+\lambda\gamma(0))<1$.
\end{assumption}

The last condition has two parts: $(\rho+\delta)a<1$, so that machine-hours have a finite price, and, at the first task, the machine-hours that replace an hour of work cost less than that hour at a high enough wage (Lemma~\ref{lem:ceiling}). With $\rho=0$ and $\delta=1$ a machine lasts one period and earns no return, so machine services are priced at their current cost; we call this case the flow benchmark.

\textbf{Land.}

\begin{assumption}[land]\label{ass:land}
There are $T>0$ units of land, each yielding one unit of land services per period. No activity adds to the land.
\end{assumption}

Land services are used to build machines and, rented directly, as living space: a unit of space is a unit of land services. Land stands for the paper's non-produced inputs, resources whose supply the production process does not generate, such as mineral deposits. A grid connection or fabrication bottleneck can occupy the same position over a horizon on which its capacity is fixed. % 74
We write $r$ for the rent on land services; it is not an interest rate.

\subsection{The cost system}\label{sec:costs}

Let $w$ be the wage, $p$ the price of the final good, $p_m$ the rental of a machine-hour, and $V_m$ the price of a machine. Under constant returns and competitive free entry, each good's price equals its unit cost. % 199
If machines perform the tasks in a set $\mathcal M$ and labor the rest, a unit of the final good uses $\int_{\mathcal M}\gamma(x)\,dx$ machine-hours and $|[0,1]\setminus\mathcal M|$ hours, so
\begin{equation}\label{eq:unitcost}
p=w\,\bigl|[0,1]\setminus\mathcal M\bigr|+p_m\int_{\mathcal M}\gamma(x)\,dx,\qquad
V_m=ap_m+\lambda w+br,\qquad
p_m=(\rho+\delta)V_m,
\end{equation}
and space rents at $r$. A machine rented out for a period loses $\delta V_m$ of its value and must earn the return $\rho V_m$ at which the owner holds it, so a machine-hour rents at the user cost $(\rho+\delta)V_m$, the owner's first-order condition (Lemma~\ref{lem:owner}).

With machines on the tasks below $x$, these are the input--output price system of Leontief (1936) and Sraffa (1960): % 207
\begin{equation}\label{eq:3}
\mathbf p=\mathbf A_\rho\mathbf p+\bm\lambda w+\mathbf b r,\qquad
\mathbf p=\begin{pmatrix}p\\p_m\\V_m\\r\end{pmatrix},\quad
\mathbf A_\rho=\begin{pmatrix}0&J(x)&0&0\\0&0&\rho+\delta&0\\0&a&0&0\\0&0&0&0\end{pmatrix},\quad
\bm\lambda=\begin{pmatrix}1-x\\0\\\lambda\\0\end{pmatrix},\quad
\mathbf b=\begin{pmatrix}0\\0\\b\\1\end{pmatrix},
\end{equation}
where $J(x)=\int_0^x\gamma(t)\,dt$ and row $i$ records the inputs per unit of good $i$. The machine rows are a recursion: a machine-hour's price includes the machine-hours used to build the machine, whose price includes those used to build them, and so on. Tracing input costs through successive rows reaches the human hours and land services in the full chain: % 203
\begin{equation}\label{eq:4}
\mathbf p=w\widetilde{\bm\lambda}+r\widetilde{\mathbf b},\qquad
\widetilde{\bm\lambda}=(\mathbf I-\mathbf A_\rho)^{-1}\bm\lambda,\qquad
\widetilde{\mathbf b}=(\mathbf I-\mathbf A_\rho)^{-1}\mathbf b.
\end{equation}
We call the tracing of prices through intermediate inputs the \emph{cost recursion}, % 223
and $\widetilde{\bm\lambda}$ and $\widetilde{\mathbf b}$ the \emph{price coefficients}: the full-chain hours and land services per unit of each good, valued at the user cost. For a machine-hour,
\begin{equation}\label{eq:tildem}
\widetilde\lambda_m=\frac{(\rho+\delta)\lambda}{1-(\rho+\delta)a},\qquad
\widetilde b_m=\frac{(\rho+\delta)b}{1-(\rho+\delta)a}.
\end{equation}
Quantities use the replacement rate in place of the user cost: a stock of $X$ machines supplies $X$ machine-hours and needs $\delta X$ new machines each period. We write $\mathbf A_0$ for $\mathbf A_\rho$ with $\delta$ in place of $\rho+\delta$; the two coincide when $\rho=0$. The hours and land services that production physically uses per unit of each good, $(\mathbf I-\mathbf A_0)^{-1}\bm\lambda$ and $(\mathbf I-\mathbf A_0)^{-1}\mathbf b$, are no larger than the price coefficients (Lemma~\ref{lem:prices}).

\subsection{Workers}\label{sec:workers}

\begin{assumption}[workers]\label{ass:workers}
There are $N>0$ workers. Each has one indivisible hour per period, which it sells ($n=1$) or keeps ($n=0$), and consumes its income each period, neither saving nor borrowing. A worker who consumes $c_g$ units of the final good and $c_h$ units of space and sells $n$ hours has utility
\begin{equation}\label{eq:utility}
\log\min\{c_g,\,c_h/h\}-\chi n,\qquad h>0.
\end{equation}
The cost of work $\chi\ge0$ differs across workers, with a continuous distribution function $F$ and $F(0)=0$.
\end{assumption}

A worker therefore consumes baskets of one unit of the final good and $h$ units of space, each costing
\begin{equation}\label{eq:7}
P_s=p+hr,
\end{equation}
the subscript standing for support. Each worker receives one basket per period as support, in work and in exit (Section~\ref{sec:owner}), and spends its net earnings and any public payments (Section~\ref{sec:government}) on additional baskets, so that it consumes $c$ baskets with
\begin{equation}\label{eq:budget}
P_s\,c=P_s+(1-\tau_w)wn+d+g_n,\qquad g_1=g_w,\quad g_0=g_e.
\end{equation}
With every instrument at zero, the utility of the choice $n$ is
\begin{equation}\label{eq:8}
u_n=\log\left(1+\frac{wn}{P_s}\right)-\chi n.
\end{equation}
Consumption is measured in baskets, with one supplied through support. The parameter $\chi$ is the utility cost of the market hour, including the value of time it displaces. Non-work time is valuable and heterogeneous (Mas and Pallais 2019). % 282

\subsection{The owner and support}\label{sec:owner}

\begin{assumption}[the owner]\label{ass:owner}
One further household, the owner, does not work and lives forever. It owns the land and the machines. Unless the government provides it (Section~\ref{sec:government}), the owner gives each worker one basket per period, in work and in exit. It ranks paths of its own consumption $c_{o,t}$, in baskets, by $\sum_{t\ge0}\beta^tu(c_{o,t})$, with $\beta\in(0,1]$ and $u$ continuous and concave on $[0,\infty)$ and differentiable with $u'>0$ on $(0,\infty)$; when $\beta=1$, by the long-run average of $u(c_{o,t})$. We write $\rho=1/\beta-1$.
\end{assumption}

Each period the owner rents out $\ell_t\le T$ units of land and its $X_t$ machines, provides the support, buys machines, and consumes. With the instruments of Section~\ref{sec:government}, its budget is
\begin{equation}\label{eq:ownerseq}
P_s\,(c_{o,t}+\sigma N)+V_m\bigl[X_{t+1}-(1-\delta)X_t\bigr]=r\ell_t-\tau_RrT+p_mX_t,
\end{equation}
where $\sigma=1$ while the owner provides the support. With a constant stock and $p_m=(\rho+\delta)V_m$, the budget is
\begin{equation}\label{eq:ownerbudget}
P_s\,(c_o+\sigma N)=r\ell-\tau_RrT+\rho V_mX.
\end{equation}
Support is a commitment in this budget, and it is \emph{funded} when the budget leaves $c_o\ge0$. The owner is not among the $N$ workers, so ``per person'' below means per worker.

The owner stands for whoever sustains a person outside paid work. Our participation benchmark focuses on dependence: a household or public institution provides the living standard available outside employment. For example, an adult may live with parents who provide housing and basic consumption while the adult decides whether to take paid work. If support continues during employment, earnings buy additional consumption. % 268
Here the support is funded from ownership income, the rent on land and the return on machines; Section~\ref{sec:rent} lets the government provide it from a tax on rents, and shows why support financed from wages faces an aggregate limit as wages fall relative to rents.

\subsection{Government}\label{sec:government}

The government has six instruments, each inactive until Section~\ref{sec:rent} or Appendix~\ref{app:fiscal} uses it. It taxes the rental value of land at the rate $\tau_R\in[0,1]$, owed whether or not the land is used, as a land-value tax is; taxes wages at the rate $\tau_w\in[0,1)$; pays every worker a uniform transfer $d\ge0$; pays $g_w\ge0$ to a worker in work and $g_e\ge0$ to a worker in exit; and may provide the support basket itself ($\sigma=0$) in place of the owner ($\sigma=1$). Its budget balances each period:
\begin{equation}\label{eq:govbudget}
\tau_RrT+\tau_wwN_a=Nd+g_wN_a+g_e(N-N_a)+(1-\sigma)NP_s,
\end{equation}
where $N_a$ is the number of workers who work. In the baseline every instrument is zero and $\sigma=1$. A law that reserves tasks for people is a further policy, recorded in $H$ (Section~\ref{sec:technology}).

\subsection{Equilibrium}\label{sec:eqdef}

\begin{definition}[equilibrium]\label{def:equilibrium}
Given the policy $(\tau_R,\tau_w,d,g_w,g_e,\sigma)$, a \emph{stationary equilibrium} consists of prices $w$, $r$, $p$, $p_m$, and $V_m$, all nonnegative, with $P_s>0$; a set $\mathcal M\subseteq[0,x_H]$ of tasks performed by machines, labor performing the others; the output $Y$ of the final good and the machine stock $X$; each worker's choice $n(\chi)\in\{0,1\}$ and consumption $c(\chi)$; and the land $\ell\in[0,T]$ that the owner rents out and its consumption $c_o\ge0$, such that:
\begin{enumerate}
\item[(i)] \emph{Producers} minimize cost and earn zero profit: each task goes to the cheaper input, $p_m\gamma(x)\le w$ on $\mathcal M$ and $p_m\gamma(x)\ge w$ on $[0,x_H]\setminus\mathcal M$; prices satisfy~\eqref{eq:unitcost}; and machine-hours rent at the user cost.
\item[(ii)] \emph{Each worker} chooses $n(\chi)$ to maximize~\eqref{eq:utility} subject to~\eqref{eq:budget}, and $c(\chi)$ is the resulting consumption.
\item[(iii)] \emph{The owner}'s plan of renting out $\ell$, holding $X$, and consuming $c_o$ in every period maximizes its objective subject to~\eqref{eq:ownerseq} at these prices, starting from the stock $X$.
\item[(iv)] \emph{The government's} budget~\eqref{eq:govbudget} balances.
\item[(v)] \emph{Markets clear.} With $N_a=N\int n(\chi)\,dF(\chi)$ and $C=N\int c(\chi)\,dF(\chi)+c_o$ baskets consumed in all,
\[
N_a=Y\bigl|[0,1]\setminus\mathcal M\bigr|+\lambda\delta X,\qquad
X=Y\!\int_{\mathcal M}\gamma(x)\,dx+a\delta X,\qquad
hY+b\delta X=\ell,\qquad
Y=C,
\]
for labor, machine-hours, land, and the final good, whose $Y$ units are consumed with $hY$ units of space.
\end{enumerate}
\end{definition}

The equilibrium concept is standard: a stationary competitive equilibrium, in which every agent optimizes at constant prices and every market clears. In matrix form, condition~(i) is~\eqref{eq:3} and condition~(v) is $(\mathbf I-\mathbf A_0^{\top})\mathbf y=C\mathbf z$, $\bm\lambda^{\top}\mathbf y=N_a$, and $\mathbf b^{\top}\mathbf y=\ell$, with gross outputs $\mathbf y=(Y,X,\delta X,hY)^{\top}$ and the basket $\mathbf z=(1,0,0,h)^{\top}$; Appendix~\ref{app:networks} uses this form for any production network. Under condition~(iii) the owner rents out all its land at any positive rent, since the land tax does not depend on use, so land is idle only at zero rent. By Walras's law one clearing condition follows from the others and the budgets: whatever the policy, the baskets bought cost $wN_a+r\ell+\rho V_mX$, the value of those produced (Proposition~\ref{prop:5}). When $r>0$ we measure prices in land services, $r=1$, and write $v=w/r$ for the wage--rent ratio.

In this economy every hour earns the same wage, and every market is competitive. Premia on particular tasks, such as union premia, licensing rents, efficiency wages (Shapiro and Stiglitz 1984), and firm-level rent sharing (Card, Cardoso, Heining, and Kline 2018), are set aside until Section~\ref{sec:history}, which enters them as a multiplicative wedge and recovers the finding of Acemoglu and Restrepo (2026) that automation targets the tasks that pay such premia.

\begin{definition}[margins]\label{def:margins}
An equilibrium with $w>0$ and $p_m>0$ has an \emph{interior margin} if machines perform a set of tasks of positive measure and labor performs a set of open tasks of positive measure. It has a \emph{boundary assignment} if labor performs almost none of the open tasks, and a \emph{corner} if machines perform almost none.
\end{definition}

Since $\gamma$ increases on the open tasks, condition~(i) gives machines, up to a set of measure zero, the open tasks below a threshold $x^*$ and labor those above it, together with every closed task. We call the threshold the \emph{task-assignment margin}, or task margin. % 168-170
The margin is interior when $0<x^*<x_H$; the assignment is a boundary assignment when $x^*=x_H$, and a corner when $x^*=0$.

\begin{definition}[automation]\label{def:automation}
Compare two economies that differ only as stated. \emph{Task automation} raises machine capability: $\gamma_M$ is nowhere lower and is higher on a set of tasks of positive measure, with the reserved tasks unchanged, so that $\gamma$ is nowhere higher and some tasks may leave $H$. \emph{Recursive automation} lowers $\lambda$, the labor needed to build a machine.
\end{definition}

A faster loom reduces the machine time needed to replace an hour of weaving: task automation. Automating the manufacture and maintenance of looms can lower the labor required to supply a loom-hour: recursive automation. % 249
Artificial intelligence may move both margins at once. It raises machine capability at tasks where models become effective substitutes, and can open tasks that were closed to machines by capability; tasks reserved by law stay closed until the rule changes. Software generation, chip design, datacenter operation, logistics, and research contribute to the chain that supplies machine services, so automating them is recursive automation. % 540
In the model's terms, computing capacity is machine-hours; chips, servers, and datacenters are machines, built from machine-hours, labor, and land services such as sites, grid connections, and water; electricity is an input whose own chain reaches non-produced inputs; and preparing data takes hours and machine-hours, while data that law protects earn an institutional rent (Appendix~\ref{app:extensions}). % 540
Actual technological changes may alter several coefficients at once and move the margin. % 251
```

### 2.2 Table 1

```latex
\begin{table}[htbp]
\centering
\caption{Notation.}
\label{tab:notation}
{\small
\begin{tabular}{@{}l p{11.2cm}@{}}
\toprule
Symbol & Meaning \\
\midrule
\multicolumn{2}{@{}l}{\emph{Technology}}\\
$x$; $\gamma_L$, $\gamma_M$; $\gamma$ & a task in $[0,1]$; task units per hour ($\gamma_L=1$) and per machine-hour; relative human productivity $\gamma_L/\gamma_M$ \\
$H=(x_H,1]$ & tasks closed to machines, by capability ($\gamma_M=0$) or by rule \\
$J(x)$ & $\int_0^x\gamma(t)\,dt$: machine-hours per unit of the final good when machines perform the tasks below $x$ \\
$a$, $\lambda$, $b$ & machine-hours, hours, and land services used to build a machine \\
$\delta$; $\beta$, $\rho$ & depreciation rate of machines; the owner's discount factor and rate of time preference $1/\beta-1$, the return on machines \\
$T$ & land, yielding $T$ units of land services per period \\
$\mathbf A_\rho$, $\mathbf A_0$ & input matrices with a machine-hour's use of machines at $\rho+\delta$ (prices) and at $\delta$ (quantities) \\
$\bm\lambda$, $\mathbf b$; $\widetilde{\bm\lambda}$, $\widetilde{\mathbf b}$ & direct hours and land services per unit of each good; price coefficients, \eqref{eq:4} \\
\multicolumn{2}{@{}l}{\emph{Households and government}}\\
$N$; $n$; $\chi$, $F$ & workers; hours sold, $n\in\{0,1\}$; a worker's cost of work and its distribution \\
$h$; $\mathbf z$ & space per basket, which also holds one unit of the final good; the basket $(1,0,0,h)^{\top}$ \\
$c$; $c_o$; $C$ & baskets consumed by a worker, by the owner, in all \\
$u$; $\ell$; $X$ & the owner's period utility; land it rents out; the machine stock \\
$\tau_R$; $\tau_w$; $d$ & tax on the rental value of land; tax on wages; uniform transfer per worker \\
$g_w$, $g_e$; $\sigma$ & payments to a worker in work and in exit; $1$ if the owner provides support, $0$ if the government does \\
\multicolumn{2}{@{}l}{\emph{Prices and quantities}}\\
$w$; $r$; $v$ & wage; rent per unit of land services; the wage--rent ratio $w/r$ \\
$p$; $p_m$; $V_m$ & price of the final good; rental of a machine-hour; price of a machine \\
$P_s$; $s$ & cost of the basket (the subscript stands for support); reservation wage \\
$Y$; $N_a$ & output of the final good; employment, including hours in machine production \\
$x^*$; $x_c$ & task margin; ceiling, the first open task at which machines cannot undercut labor (Lemma~\ref{lem:ceiling}) \\
$N_D(x)$, $N_S(x)$ & labor demand and supply when the margin is at $x$ \\
$\widetilde\lambda_s$, $\widetilde b_s$; $L_s$, $B_s$ & the basket's price coefficients; the hours and land services one basket physically requires \\
$I$; $R$; $\kappa$ & income; rent $rT$; coverage $R/(NP_s)$ \\
$\mathbf I$; ${}^{\top}$ & identity matrix; transpose \\
\bottomrule
\end{tabular}
}
\end{table}
```

### 2.3 Notes on the drafts

**Definition 1, against what a definition of equilibrium must cover.**

| Requirement | Where |
|---|---|
| Firms optimize | (i): cost minimization task by task; zero profit; the user cost |
| Workers optimize | (ii), with the budget (`budget`) under every instrument |
| The owner optimizes | (iii): land (Lemma A.1(a)); the stock and consumption (Lemma A.1(b)–(c)) |
| Government | (iv), with public provision (1 − σ)NP_s in its budget |
| Every market | (v): labor, machine-hours, land, and the final good with its space. Machines clear as δX built and replaced. By Walras's law one follows (Claim 5(b); S3) |
| Feasibility | Nonnegative quantities; land used equals land offered, at most T; P_s > 0 |
| The support provider's budget | (`ownerseq`) and (`ownerbudget`); support is a commitment in it, with c_o ≥ 0 |

**The owner, and why Definition 1 states the user cost.**
- Her decision is ρ = 1/β − 1, with the user cost as the owner's first-order condition. It is adopted in Assumption 5 and Lemma A.1(c): whenever c_o > 0, any other rental would make a deviation profitable.
- Definition 1(i) also states the user cost. When support absorbs all the owner's income (c_o = 0), its only feasible plan is constant whatever the return, so the first-order condition does not bind there.
- Without the clause, Theorem 1's uniqueness would need a proof that no zero-consumption configuration at another return clears every market.
- Scans of the return find none:
  - from −0.045 to 0.168 on the instance, where c_o stays between 0.24 and 1.02 (`knife_edge.py`);
  - from −0.19 to 0.10 at δ = 0.2, where c_o stays negative (`knife_edge2.py`).
- So the clause costs nothing in these economies and makes the theorem hold in general.
- At β = 1 the discounted sum diverges, so Assumption 5 ranks paths by long-run average utility.
- Workers neither save nor borrow (Assumption 4). Otherwise a worker who could save at ρ would smooth by working in some periods only, and (8)–(10) would change.

**Who may perform a task.**
- H = (x_H, 1] collects tasks closed by capability (γ_M = 0) and by rule (law, or a good defined by human performance).
- Placing H last is a labeling convention.
- Definition 3 keeps the two apart: task automation raises γ_M with the reserved tasks unchanged. Section 8's "same wall" (443) holds by definition.
- The economic ceiling x_c (687) is separate, in Lemma 2.

**The primitives sentence** (her decision 1). It names every primitive, and each is used by a result:
- γ and x_H: Props. 1–2, Theorem 1;
- a, λ, b, δ: `tildem`, Theorem 1, Lemma 1(iii);
- T, N, h: Theorem 1, Props. 4–5, Cor. 3;
- F: Prop. 3, Theorem 1, Cor. 2;
- β and u: Lemma A.1;
- the policy: Props. 3 and 6, Cors. 2–3, (16).

**Renames implied** (Open 12j).
- Required:
  - plain I → bold **I** at 211, 215, 217 and 580;
  - m_w, m_e → g_w, g_e at 592 and 779–787;
  - α → ω (759–763);
  - j → k for inputs (399);
  - \mathsf{T} → ^\top.
- Recommended: n_D, n_S → N_D, N_S; the corollary's ε → ξ; L̄_i → λ̄_i; n_s → z_H.
- Kept, for the check templates and Figure 3's legend: a, λ, b, v, V_m, Y and s.

---

## 3. Restated results, and the changes to their proofs

The blocks are the new text, with the proofs of Propositions 1–3 in it, as she decided. The notes give what changed against main.tex. Proofs sent to the appendix are in §3.5.

### 3.1 Section 3: equilibrium

```latex
\section{Equilibrium}\label{sec:equilibrium}

What is easy and what is hard. Once $w$ and $r$ are known, the cost recursion prices every good: Lemma~\ref{lem:prices} resolves each price into wages and rents through the price coefficients, a linear computation. The hard part is $w/r$ itself. It is set at the task margin against a machine whose own price contains wages (Propositions~\ref{prop:1} and~\ref{prop:2}), by workers who compare the wage with the cost of a basket that the same recursion prices (Proposition~\ref{prop:3}), and by a labor market that the land constraint closes (Theorem~\ref{thm:1}).

\subsection{Prices}\label{sec:prices}

\begin{lemma}[prices and quantities]\label{lem:prices}
In every equilibrium with margin $x^*$:
(i) $\mathbf p=w\widetilde{\bm\lambda}+r\widetilde{\mathbf b}$, and the basket costs $P_s=w\widetilde\lambda_s+r\widetilde b_s$, with $\widetilde\lambda_s=1-x^*+\widetilde\lambda_mJ(x^*)$ and $\widetilde b_s=h+\widetilde b_mJ(x^*)$;
(ii) $Y$ baskets employ $N_a=YL_s$ hours and use $\ell=YB_s$ units of land, with $L_s=1-x^*+\lambda\delta J(x^*)/(1-a\delta)$ and $B_s=h+b\delta J(x^*)/(1-a\delta)$;
(iii) $\widetilde\lambda_s\ge L_s$ and $\widetilde b_s\ge B_s$, with equality when $\rho=0$, and $P_s=wL_s+rB_s+\rho V_mX/Y$.
\end{lemma}

\begin{remark}
Lemma~\ref{lem:prices} uses only cost minimization and market clearing. It does not depend on preferences, on the owner, or on policy.
\end{remark}

\begin{proposition}[the task margin]\label{prop:1}
In an equilibrium with $w>0$ and $p_m>0$:
(i) at an interior margin,
\[
w=p_m\gamma(x^*);
\]
at a boundary assignment, $w\ge p_m\gamma(x_H)$; at a corner, $w\le p_m\gamma(0)$.
(ii) Holding the machine rental fixed, movement of an interior margin changes the wage at rate $dw/dx^*=p_m\gamma'(x^*)$. Where a fixed-output labor-demand schedule absorbs additional final-task hours by lowering $x^*$, a steeper capability schedule requires a larger wage change for the same movement of the margin. % 191
\end{proposition}

\begin{proof}
(i) By Definition~\ref{def:equilibrium}(i), $p_m\gamma(x)\le w$ for almost every $x<x^*$ and $p_m\gamma(x)\ge w$ for almost every open task $x>x^*$. At an interior margin both sets have positive measure, and continuity of $\gamma$ at $x^*$ gives equality. At a boundary assignment only the first inequality holds on the open tasks, and at a corner only the second. (ii) Differentiate the equality at fixed $p_m$. Final-task labor demand is $Y(1-x^*)$, so $dN_Y/dx^*=-Y$ and $dw/dN_Y=-p_m\gamma'(x^*)/Y$.
\end{proof}

\begin{remark}
Proposition~\ref{prop:1} compares unit costs at given prices. It does not depend on how the machine rental is set, on preferences, or on the labor market.
\end{remark}

\begin{proposition}[replacement closure]\label{prop:2}
In every equilibrium with an interior margin and $r>0$, the feedback term $1-\gamma(x^*)\widetilde\lambda_m$ is positive and
\begin{equation}\label{eq:5}
\frac{p_m}{r}
=
\frac{\widetilde{b}_m}{1-\gamma(x^*)\widetilde{\lambda}_m},
\qquad
\frac{w}{r}
=
\frac{\gamma(x^*)\widetilde{b}_m}{1-\gamma(x^*)\widetilde{\lambda}_m},
\end{equation}
with $\widetilde\lambda_m$ and $\widetilde b_m$ given by~\eqref{eq:tildem}. The wage--rent ratio rises with $\gamma(x^*)$ and with $\widetilde\lambda_m$.
\end{proposition}

\begin{proof}
The machine-hour's row of Lemma~\ref{lem:prices}(i) is $p_m=w\widetilde\lambda_m+r\widetilde b_m$, and Proposition~\ref{prop:1} gives $w=p_m\gamma(x^*)$. Hence $p_m(1-\gamma(x^*)\widetilde\lambda_m)=r\widetilde b_m>0$, so the feedback term is positive, and solving gives~\eqref{eq:5}. The derivatives of $w/r$ with respect to $\widetilde\lambda_m$ and $\gamma(x^*)$ are $\gamma(x^*)^2\widetilde b_m/(1-\gamma(x^*)\widetilde\lambda_m)^2$ and $\widetilde b_m/(1-\gamma(x^*)\widetilde\lambda_m)^2$, both positive. % 631-636
\end{proof}

\begin{remark}
Proposition~\ref{prop:2} uses only Proposition~\ref{prop:1} and the machine-hour's row of the cost system. It does not depend on preferences, on support, or on the labor market, and it holds in any production network whose machine chain uses a non-produced input (Proposition~\ref{prop:network}).
\end{remark}

The denominator measures the feedback from the wage into the cost of its substitute. % 245
At the margin, $\gamma(x^*)\widetilde\lambda_m=w\widetilde\lambda_m/p_m$ is the part of the machine-hour's price that resolves into wages, including the return on the wages advanced to build machines; when $\rho=0$ it is labor's share of machine-service cost. A positive rent bill requires it to be below one. The closure is a price condition at the equilibrium assignment; household choices and market clearing also determine $x^*$ (Theorem~\ref{thm:1}). % 245, reading on the price basis

When the labor requirement of the machine chain vanishes and $\gamma(x^*)\widetilde\lambda_m\to0$, equation~\eqref{eq:5} gives % 253
\begin{equation}\label{eq:6}
\frac{p_m/r}{\widetilde b_m}\to1.
\end{equation}
When $\rho=0$, the service price is then accounted for by its embodied claim on the non-produced input; with a positive return, by that claim and the return on the machines that embody it. Institutional rents introduce further income components. % 257, qualified

\subsection{Participation and the labor market}\label{sec:participation}

\begin{proposition}[dependence, living costs, and participation]\label{prop:3}
In every equilibrium with $\tau_w=d=g_w=g_e=0$, a worker with cost of work $\chi$ prefers work exactly when
\begin{equation}\label{eq:9}
w \ge s,
\qquad
s = (e^{\chi}-1)P_s,
\end{equation}
and employment is
\begin{equation}\label{eq:10}
N_a=NF\left(\log\left[1+\frac{w}{P_s}\right]\right).
\end{equation}
For $\chi>0$, the reservation wage rises with the cost of the basket.
\end{proposition}

\begin{proof}
Exit gives utility zero, and work gives $\log(1+w/P_s)-\chi$, which is nonnegative exactly when~\eqref{eq:9} holds; $\partial s/\partial P_s=e^\chi-1>0$ for $\chi>0$. Workers with $w=s$ have measure zero because $F$ is continuous, which gives~\eqref{eq:10}. % 640
\end{proof}

\begin{remark}
Proposition~\ref{prop:3} does not depend on technology, or on who provides the basket, the owner or the government: a worker has one basket in work and in exit either way. With payments, Appendix~\ref{app:fiscal} gives the reservation wage.
\end{remark}

Access to support, its security, and the obligations it carries help determine the value of exit. Personal assets, pensions, and savings can also support life outside employment; the benchmark isolates the choice faced by someone whose living standard is sustained through dependence. % 268, 298
Access to common land is a historical example of support through shared resources. Enclosure could remove that access and increase the need for wage income, the mechanism emphasized by Marx (1867), Lewis (1954), and Polanyi (1944). Lewis pinned the modern-sector wage to what the traditional sector affords; his traditional sector supplies an outside option until its surplus labor is absorbed. In a modern economy, housing arrangements, household support, and public provision shape the corresponding outside option. % 300, 124

If $r>0$, the owner rents out all its land, so by Lemma~\ref{lem:prices}(ii) the economy produces $T/B_s$ baskets and employs $TL_s/B_s$ hours. With Proposition~\ref{prop:3}, labor-market clearing is % 317
\begin{equation}\label{eq:11}
\underbrace{\frac{TL_s}{B_s}}_{\text{hours required}}
=\underbrace{NF\left(\log\left[1+\frac{w}{P_s}\right]\right)}_{\text{hours supplied}}.
\end{equation}

\subsection{Existence and uniqueness}\label{sec:existence}

\begin{lemma}[the ceiling]\label{lem:ceiling}
Let $x_c$ be the first open task at which $(\rho+\delta)(a+\lambda\gamma(x))\ge1$, or $x_c=x_H$ if there is none. Then $x_c>0$, and in every equilibrium machines perform almost no task in $[x_c,1]$.
\end{lemma}

Machines cannot perform the tasks in $H$. At a task in $[x_c,x_H]$ they can, but the machine-hours that would replace an hour there embody at least that hour of labor, counting the labor needed to build them at the required return, so they cost at least the hour at any wage. % 687
Unlike $H$, the ceiling depends on the labor in the machine chain and on the return, as well as on capability.

% ... (21)-(24) follow as at main.tex 688-707, with n_D, n_S renamed N_D, N_S, and the limit sentence of 708:
% "As x rises to x_c, N_S(x) tends to a limit, which we write N_S(x_c). If the ceiling binds before H, v and P_s grow without
% bound while v/P_s tends to gamma(x_c)/[gamma(x_c)(1-x_c)+J(x_c)]."

\begin{theorem}[existence and uniqueness]\label{thm:1}
With every instrument zero and the owner providing support, suppose
\begin{equation}\label{eq:25}
T>Nh,\qquad
N_S(x_c)>N_D(x_c).
\end{equation}
Then every equilibrium has $w>0$, $r>0$, and an interior margin, at the unique $x^*\in(0,x_c)$ with $N_D(x^*)=N_S(x^*)$. Up to the choice of numeraire and sets of tasks of measure zero, its prices are \eqref{eq:21}--\eqref{eq:22} and its quantities \eqref{eq:23}--\eqref{eq:24} at $x^*$. An equilibrium exists if and only if the owner's income covers the support there, $rT+\rho V_mX\ge NP_s$.
\end{theorem}

The proof (Appendix~\ref{app:proofs}) uses~\eqref{eq:25} to rule out a zero wage, a zero rent, a corner, a margin at the ceiling, and a boundary assignment at the wall; one crossing remains, and the owner's budget decides whether it is an equilibrium.

\begin{remark}
Theorem~\ref{thm:1} does not depend on the shape of $\gamma$ beyond Assumption~\ref{ass:tasks}, or on whether $H$ is empty, once~\eqref{eq:25} holds. When the wall lies below the crossing, \eqref{eq:25} fails: labor demand still exceeds supply at $x_H$, no interior margin clears the labor market, and labor works only in $H$ and in the machine chain. The theorem does not cover that case.
\end{remark}

\begin{corollary}[labor supply and the margin]\label{cor:statics}
(i) As the margin $x$ rises on $(0,x_c)$, labor demand $N_D(x)$ falls, while the wage--rent ratio $v(x)$ and the real wage $v(x)/P_s(x)$ rise; the wage--rent ratio rises at the rate $dv/dx=p_m\gamma'(x)/[r(1-\gamma(x)\widetilde\lambda_m)]$, the rate of Proposition~\ref{prop:1}(ii) amplified by $1/(1-\gamma\widetilde\lambda_m)=1+\lambda v/b$ because the machine rental rises with the margin.
(ii) If the distribution of work costs changes from $F$ to $\widehat F\le F$ at fixed technology and support, and \eqref{eq:25} and funding hold under both, the equilibrium margin, wage--rent ratio, and real wage weakly rise, and strictly if supply falls at the original margin. % 743
\end{corollary}

\begin{remark}
Part~(i) concerns the margin-indexed functions \eqref{eq:21}--\eqref{eq:24} and does not need~\eqref{eq:25}; part~(ii) does not depend on the form of $F$.
\end{remark}
```

**The easy and hard paragraph** (her decision 2) is used once, at the head of §3.

**Lemma 1 (new).**
- (i) is (3)–(4), 219 and 717 made a result for the four goods, including the basket's price coefficients.
- (ii) is the quantity side (717).
- (iii) is A's comparison of the two bases, plus the identity P_s = wL_s + rB_s + ρV_mX/Y. It removes the one tilde that served two objects (308 against 717; I-12).

**Proposition 1.**
- Statement:
  - "interior machine-contestable task margin" (187) becomes the defined interior margin (Def. 2);
  - (i) adds the inequalities at a boundary and at a corner, the correction to 163–165;
  - differentiability comes from Assumption 1 (Open 12i);
  - (iii), which restated 153, is removed.
- Proof: in the text. (i) uses the a.e. inequalities of Def. 1(i) and continuity; that is the step 627 took for granted. (ii) is 627 with γ_L = 1.

**Proposition 2.**
- Statement:
  - "at an active contestable margin, suppose γ(x*) > 0, b̃_m > 0 and 1 − γλ̃_m > 0" (232) becomes "every equilibrium with an interior margin and r > 0";
  - in the stated economy, b̃_m > 0 follows from b > 0, and the other two are conclusions (inventory R4);
  - the coefficients are in closed form (`tildem`) and do not depend on the assignment, so "holding the other total requirements fixed" is no longer needed. Prop. B.1(b) restores it for networks.
- Proof: in the text (631–636). Positivity of the feedback term is derived.

**Readings.**
- At 245, γ(x*)λ̃_m is the part of p_m that resolves into wages, valued at the user cost. It is labor's share of cost only when ρ = 0: on the instance, 0.567 against 0.456.
- At 257, land alone accounts for the price only when ρ = 0.

**Proposition 3.**
- Statement:
  - "Suppose P_s > 0 and the supported basket remains available in both states" (285) becomes "In every equilibrium with τ_w = d = g_w = g_e = 0";
  - (10) joins it.
- Proof: in the text. (18), ds/dr, becomes ∂s/∂P_s (R7), and ties have measure zero.
- The remark gives the formal home of 423's replacement case.

**(11).** Derived. Land is fully used at r > 0 because the owner chooses so (Lemma A.1(a)), not by assumption (317).

**Lemma 2 (new).** It is 687 made a result, with H allowed. It rests on p_mγ − w = [(ρ+δ)brγ − wD]/(1 − (ρ+δ)a) (S7, sympy).

**Theorem 1.**
- Lemma B.1 (719–726) proved only that "there is a unique interior threshold". Theorem 1 says that every equilibrium is that one and that funding is necessary as well as sufficient. This closes Open 12(h).
- Proof (App. A): Lemma B.1's proof (728–741), plus the exclusion paragraph and Lemma A.1.

**Corollary 1.**
- (i) collects 324 and 729–734, and adds the equilibrium rate.
- On the instance, dv/dx = 0.857044 numerically and by the formula, against a partial rate of 0.371388. The multiplier is 2.3077 = 1 + λv/b (S7).
- (ii) is 743.

### 3.2 Section 4: purchasing power and income

```latex
\section{Purchasing power and income}\label{sec:power}

\subsection{What an hour's wage buys}\label{sec:wagebuys}

For every good or service, the price coefficients in~\eqref{eq:4} give an exact price. A feasible alternative method also bounds that price from above. % 334
A worker can make a unit of the final good by hand in an hour, using neither machines nor land.

\begin{proposition}[the real-wage fork]\label{prop:4}
In every equilibrium with $w,r>0$, every good or service $i$ satisfies
\begin{equation}\label{eq:12}
p_i=w\widetilde\lambda_i+r\widetilde b_i,\qquad
\frac{w}{p_i}=\frac{1}{\widetilde\lambda_i+\widetilde b_i(r/w)}.
\end{equation}
An hour's wage buys $w/r$ units of space and at least one unit of the final good; when machines perform some tasks, it buys at most $(w/r)/\widetilde b_g$ units of the final good, where $\widetilde b_g=\widetilde b_mJ(x^*)>0$.
\end{proposition}

\begin{remark}
Proposition~\ref{prop:4} does not depend on the margin being interior, or on there being four goods. In any production network, every good $i$ that people can make with a \emph{human chain}, which uses neither machines nor machine-hours anywhere and has full-chain requirements $\bar\lambda_i$ of hours and $\bar b_i$ of non-produced services, satisfies
\begin{equation}\label{eq:13}
\frac{1}{\bar\lambda_i+\bar b_i(r/w)}
\le\frac{w}{p_i}
\le\frac{w/r}{\widetilde b_i}
\end{equation}
when $\widetilde b_i>0$ (Proposition~\ref{prop:network}). Here the final good has $\bar\lambda=1$ and $\bar b=0$, and space has $\widetilde b_h=1$.
\end{remark}

The rent bound counts the whole supply chain. An hour's wage buys $w/r$ units of the non-produced service, and the price of a unit of output carries $\widetilde b_i$ units, the return on the machines in its chain included; when $\rho=0$, $\widetilde b_i$ is the input the unit embodies. % 351
% ... the rest of 351 (cloth) and 353 follow, 353's fifth sentence ending "...valued at the user cost".

\begin{corollary}[vanishing wage purchasing power and participation]\label{cor:vanishing}
Along a sequence of equilibria with interior margins and a fixed $h$, suppose
\[
\gamma(x^*)\widetilde b_m\to0,\qquad
1-\gamma(x^*)\widetilde\lambda_m\ge\xi>0.
\]
Then $w/r\to0$: an hour's wage buys ever less space, while it still buys at least one unit of the final good. If, in addition, the distribution $F$ of work costs is fixed and no public payment favors work, $g_w\le g_e$, then
\begin{equation}\label{eq:14}
\frac{w}{P_s}\to0,\qquad
\frac{N_a}{N}\to0.
\end{equation}
\end{corollary}

\begin{remark}
Corollary~\ref{cor:vanishing} does not depend on which channel drives $\gamma(x^*)\widetilde b_m$ to zero. Recursive automation alone cannot: with no labor in the machine chain, $w/r=\gamma(x^*)\widetilde b_m>0$, so people leave work only as machines improve at the tasks people still do. In a production network the corollary holds good by good, for every good whose price coefficient $\widetilde b_i$ stays bounded away from zero (Proposition~\ref{prop:network}).
\end{remark}

\subsection{Factor income}\label{sec:income}

\begin{proposition}[labor's share]\label{prop:5}
In every equilibrium, final expenditure equals factor income,
\begin{equation}\label{eq:income}
I=wN_a+rT+\rho V_mX,
\end{equation}
where $N_a$ counts all employed hours, including those in machine production, and $\rho V_mX$ is the return on the machine stock. If $r>0$, labor's share satisfies
\begin{equation}\label{eq:15}
\frac{wN_a}{I}\le\frac{(w/r)N_a}{(w/r)N_a+T},
\end{equation}
with equality when $\rho=0$; then, at given $N_a$ and $T$, a lower wage--rent ratio lowers labor's share. With bounded total hours and fixed $T>0$, $w/r\to0$ implies that labor's share tends to zero.
\end{proposition}

\begin{remark}
The identity does not depend on which cost-minimizing assignment supplies the coefficients (757), and it holds in any production network (Proposition~\ref{prop:network}).
\end{remark}

% Replaces 393's first sentences; its other sentences stay, then the factor-share relocation:
When $\rho=0$, the owner's land receives all non-wage income; with a positive return the owner also receives the return on machines, which~\eqref{eq:income} counts. In the instance of Section~\ref{sec:instance}, income is $0.55$ wages, $0.13$ rent, and $0.32$ return on machines, and labor's share is $0.55$ against the $0.81$ that~\eqref{eq:15} gives as its bound. In the data, the labor share's decline is documented and global (Karabarbounis and Neiman 2014), and its capital-side counterpart resolves substantially into housing, which is to say land (Rognlie 2015; Knoll, Schularick, and Steger 2017). % 132, via the inventory's relocation 4

% The rho = 0 remark (design C's carry-over list, recast):
Durable machines change five statements, each of which holds as in the flow benchmark when $\rho=0$, whatever $\delta$: the basket's price equals $wL_s+rB_s$ only when $\rho=0$, and otherwise also pays the return on the machines that supply it; \eqref{eq:15} holds with equality only then; Proposition~\ref{prop:6}(iii) and Corollary~\ref{cor:fiscal} count the return on machines beside rent; \eqref{eq:17} is equivalent to physical feasibility only then; and the readings of $\gamma(x^*)\widetilde\lambda_m$, of~\eqref{eq:6}, and of $\widetilde b_i$ as physical quantities need it. Every other statement holds as stated with durable machines.
```

**Proposition 4.**
- In the stated economy it is the fork itself: an hour's wage buys w/r of space and at least one unit of the final good.
- The general bounds (13) of 343–347 are in the remark and in Proposition B.1(c), on price coefficients and with the human chain.
- "In the two-factor cost system" (337) and "at an interior margin" (title) are gone. Corners are covered.
- Proof (App. A): p ≤ w, because p_mγ ≤ w below x*.

**Corollary 2.**
- Changes against 355–363:
  - numbered;
  - "active contestable margin" becomes "interior margins";
  - "one basket remains funded" is dropped (Def. 1);
  - "continuous with F(0) = 0" is part of Assumption 4;
  - B_s ≥ h holds automatically;
  - **"no public payment favors work, g_w ≤ g_e" is added**: Definition 1 admits payments, and without it the limit fails (j3: 0.693; S5: 0.0830 with g_w = 0.2P_s);
  - "F fixed" stays (A dropped it).
- The remark adds STATE's check: recursive automation alone leaves w/r = γ(x*)b̃_m > 0.
- Proof (App. A): r > 0 follows from the feedback bound.

**Proposition 5.**
- "In the competitive flow economy" (381) becomes "every equilibrium", with ρV_mX in the identity.
- (15) is an inequality, with equality when ρ = 0.
- "Bounded total hours" stays (A dropped it).
- Proof (App. A): Appendix C's cancellation on two coefficient sets.

### 3.3 Section 5: rent taxation

```latex
\section{Distribution: rent taxation and a uniform transfer}\label{sec:rent}

% 397 stays; then, from 223-225 (the definitions move here, where the tax uses them):
An input is \emph{terminal over a horizon} when its supply cannot expand through production within that horizon. We reserve \emph{pure rent} for income due to fixed supply and \emph{site rent} for the land component of real-estate income, excluding structures. % 223-225

\begin{proposition}[sharing rents while labor remains employed]\label{prop:6}
Let the government tax the rental value of land at $\tau_R\in[0,1]$ and pay $d=\tau_RrT/N$ to every worker, with $\tau_w=g_w=g_e=0$ and $\sigma=1$.
(i) At any positive rent the owner rents out all its land, whatever the tax rate, and producers pay the gross rental for using it: the physical supply of the fixed factor is invariant to the tax.
(ii) An unconditional transfer pays the same amount in work and exit. Its direct payment differential at the participation boundary is zero, while participation can respond through income effects. % 404
(iii) At given gross prices and hours, aggregate receipts remain $I=wN_a+R+\rho V_mX$, since
\[
(1-\tau_R)R+Nd=R.
\]
The tax redistributes the rent component toward an equal per-worker allocation. % 410
\end{proposition}

\begin{remark}
Proposition~\ref{prop:6} does not depend on demand or supply elasticities: the taxed input's supply is fixed, and the tax does not depend on its use. With a tax on rent received instead, part~(i) would hold only for $\tau_R<1$.
\end{remark}

Rent revenue can also finance the basket itself. Define coverage by $\kappa=R/(NP_s)$, with $R=rT>0$. If the government provides the basket ($\sigma=0$) from the rent tax alone, its budget~\eqref{eq:govbudget} requires
\begin{equation}\label{eq:16}
\tau_R=\frac{NP_s}{R}=\frac{1}{\kappa}.
\end{equation}
A tax rate between zero and one can meet this budget exactly when $\kappa\ge1$, evaluated at equilibrium prices. % 421
Public provision that replaces the owner's, at the same prices, leaves the participation comparison unchanged (Proposition~\ref{prop:3}). If the payment instead supplements the owner's basket ($\sigma=1$, $d>0$), the preferences of Section~\ref{sec:workers} give the reservation wage $(e^\chi-1)(P_s+d)$: the extra consumption available in both states reduces the gain from work. % 423
With every instrument at zero, the owner's budget~\eqref{eq:ownerbudget} requires $rT+\rho V_mX\ge NP_s$, so at $\rho=0$ every equilibrium has $\kappa\ge1$. The measured coverage, $0.30$ (Section~\ref{sec:measurement}), therefore fits the stated economy only with another source of support: in the instance of Section~\ref{sec:instance}, rent covers $0.38$ of it and the return on machines the rest.

\begin{corollary}[fiscal capacity as wage income vanishes]\label{cor:fiscal}
(i) Along a sequence of equilibria with $N,T>0$ fixed and $w/r\to0$, revenue from a wage tax at any rate between zero and one becomes a vanishing fraction of income, and the non-wage share of income, $(R+\rho V_mX)/I$, tends to one; when $\rho=0$, $R/I\to1$. If $B_s$ stays bounded away from zero, that revenue also funds a vanishing fraction of one basket per worker.
(ii) At given methods that use no labor anywhere in the basket's chain, $\widetilde\lambda_s=0$, and any rent $r>0$, full rent capture yields coverage
\begin{equation}\label{eq:17}
\kappa=\frac{T}{N\widetilde b_s}.
\end{equation}
Coverage $\kappa\ge1$ implies $NB_s\le T$, the physical condition for producing one basket per worker with these methods; when $\rho=0$, $\widetilde b_s=B_s$ and the two conditions coincide.
\end{corollary}

\begin{remark}
Part~(ii) is a statement about prices at given methods, not about an equilibrium: with $H$ empty, a configuration with no labor in the basket's chain demands no labor, while every positive wage draws some workers when $F(z)>0$ for $z>0$, as in the instance. With several non-produced inputs, \eqref{eq:17} becomes $\kappa=\mathbf r^{\top}\mathbf T/(N\mathbf r^{\top}\widetilde{\mathbf b}_s)$, which compares rental values rather than physical quantities (Appendix~\ref{app:extensions}).
\end{remark}
```

**Proposition 6.**
- Statement:
  - the instruments are named;
  - (i) is a result for every τ_R ∈ [0, 1] under the rental-value tax;
  - (iii) includes ρV_mX;
  - "per person" becomes per worker (I-5).
- Proof: (i) is Lemma A.1(a), replacing "fixed by assumption" (414). The Diamond–Mirrlees sentence stays.

**(16).**
- Its case is public provision σ = 0.
- The added paragraph states that at ρ = 0 every equilibrium with zero instruments has κ ≥ 1. The measured 0.30 (494) therefore needs another source of support. In the instance, rent covers 0.385 of support and the return on machines 0.970.

**Corollary 3.**
- (i): "while R/I → 1" (428) becomes the non-wage share. The counterexample without ρ = 0 is R20's land-only structure, R/I = δ/(ρ + δ) = 0.357 (j1).
- (ii):
  - a price statement at given methods (430);
  - (17) on the price basis;
  - at the instance's parameters with λ = 0 and every task automated, κ = 0.659 while T/(NB_s) = 1.707 (j1);
  - the remark adds the several-input line, after STATE's note that (17) is "narrower than the question it would answer".
- Proof (769–775): with P_s = rb̃_s and b̃_s ≥ B_s.

### 3.4 Section 6: the examples

```latex
\section{A numerical economy and an automation path}\label{sec:instance}

\begin{table}[htbp]
\centering
\caption{The numerical instance. $N$, $b$, $\delta$, $\gamma(0)$, and $\gamma(1)$ are set. The other seven parameters are chosen together to match the seven targets in the lower panel and then rounded to two significant figures; the last column gives the values at the rounded parameters.}
\label{tab:instance}
{\small
\begin{tabular}{@{}l l l@{}}
\toprule
\multicolumn{3}{@{}l}{\emph{Parameters}}\\
\midrule
workers; land & $N$; $T$ & $1$; $0.01$ \\
space per basket & $h$ & $0.0017$ \\
machine-hours, hours, and land to build a machine & $a$, $\lambda$, $b$ & $1.4$, $7.3$, $0.4$ \\
depreciation; rate of time preference & $\delta$; $\rho$ & $0.05$; $0.09$ \\
relative human productivity & $\gamma(x)$ & $0.01+0.99x^{4.4}$ \\
cost of work & $\chi$ & uniform on $[0,2.2]$ \\
\midrule
\multicolumn{3}{@{}l}{\emph{Targets}}\\
\midrule
 & target & at the rounded parameters \\
labor's share of a machine's cost & $0.47$ & $0.456$ \\
machine services' share of a machine's cost & $0.20$ & $0.196$ \\
final-task labor's share of a basket's cost & $0.47$ & $0.469$ \\
site's share of a basket's cost & $0.06$ & $0.065$ \\
machine production's share of hours & $0.15$ & $0.148$ \\
participation, $N_a/N$ & $0.60$ & $0.602$ \\
baskets per worker, $Y/N$ & $3$ & $3.01$ \\
\bottomrule
\end{tabular}
}
\end{table}

% The instance sentences of main.tex 745 follow, with the parameter list replaced by "Table~\ref{tab:instance} lists the
% parameters and the shares they are set to match", "the full-chain cost of consumption" replaced by "the cost of a basket at
% final tasks", "provider's" by "owner's", and one sentence added:
Of the two curvatures that match the targets, we take the lower; at the other, about $15.5$, task automation raises $w/P_s$.

% Before Figure 3, the two experiments framed as artificial intelligence (the caption itself is unchanged but for its pointer):
Figure~\ref{fig:3} draws this market for the instance and for two experiments of Definition~\ref{def:automation}: recursive automation that removes labor from building machines ($\lambda=0$), as when chip design and datacenter operation are automated, and task automation that halves $\gamma$ at every task, as when models improve at every task at once.

% The automation path, replacing main.tex 747 (the anchored clauses are kept):
For an illustrative automation path, retain these parameters and set $\lambda=0$ and $\gamma_\eta(x)=\eta(0.01+0.99x^{4.4})$, with $0<\eta\le1$; at $\eta=1$ this is the recursive-automation economy of Figure~\ref{fig:3}. The conditions in \eqref{eq:25} hold throughout, since with $\lambda=0$ and $H$ empty no labor is demanded at the ceiling $x_c=1$, while some is supplied at every positive wage; so by Theorem~\ref{thm:1} each economy on the path has at most one equilibrium, and has one when its support is funded. With $\lambda=0$ the machine rental is $p_m=\pi r$ at every margin, where $\pi=(\rho+\delta)b/[1-(\rho+\delta)a]$, and the equilibrium wage satisfies $0<v\le\eta(\rho+\delta)b/[1-(\rho+\delta)a]\to0$. Since $\gamma_\eta\le\eta$, $P_s\le(\eta\pi+h)r$, so rent alone funds the support whenever $\eta\le(T-Nh)/(N\pi)$, about $0.12$ here; rent and the return on machines fund it at every $\eta$ on a grid from $10^{-4}$ to $1$. Relative capability remains a hundred times as high at the last task as at the first. Since $P_s\ge h>0$, participation tends to zero through \eqref{eq:24}: it is $0.56$ at $\eta=1$ and $0.13$ at $\eta=0.01$. At $\eta=0.001$ it is $0.018$. The machine stock satisfies $X\le\eta T/[h(1-a\delta)]$, so the return on machines vanishes relative to income and $R/I\to1$. From $\eta=1$ to $\eta=0.001$ an hour's wage comes to buy $1.8$ times as much of the final good and $1/426$ as much space: the real-wage fork of Proposition~\ref{prop:4} in its simplest form.
```

**Table 2.**
- It follows `code/appendix_b.py` 31–37. N, b, δ and γ(0) are set, and γ(1) = 1 is implicit in `PRINTED`. Seven parameters match seven targets.
- The third target is labeled as the code computes it: final-task labor's share of a basket's cost, 0.469. The full-chain share is 0.551 on physical requirements and 0.733 on the price basis (S6; decision 6).

**The path paragraph.**
- It keeps every anchored clause of 747.
- It replaces "fund the support throughout" (R35) with:
  - the analytic small-η bound and the grid statement;
  - the proof that (25) holds;
  - R/I → 1;
  - STATE's thousandfold point and fork ratios: 0.0179; w/p × 1.78 and w/r ÷ 426 from η = 1 to 0.001 (`path_numbers.py`).

### 3.5 Appendix A: the new lemma and the proofs sent to the appendix

```latex
\appendix
\section{Proofs}\label{app:proofs}

\begin{lemma}[the owner's problem]\label{lem:owner}
Take constant prices with $P_s>0$ and $V_m>0$, a machine-hour rental $p_m$, and a policy with $\tau_R\in[0,1]$.
(a) If $r>0$, every optimal plan rents out $\ell_t=T$ in every period.
(b) If $p_m=(\rho+\delta)V_m$, the constant plan that rents out $\ell$ (with $\ell=T$ if $r>0$), holds the stock $X$, and consumes $c_o=[r\ell-\tau_RrT+\rho V_mX]/P_s-\sigma N$ in every period is optimal from the initial stock $X$ whenever $c_o\ge0$.
(c) If a constant plan with $X>0$ and $c_o>0$ is optimal at a rental $p_m$, then $p_m=(\rho+\delta)V_m$: the user cost is the owner's first-order condition.
\end{lemma}

\begin{proof}
(a) The land tax $\tau_RrT$ does not depend on $\ell_t$, so renting out more land raises the period's resources whenever $r>0$, and $u$ is strictly increasing. (b) Write $W_t=V_mX_t\ge0$ and $y_o=r\ell-\tau_RrT-\sigma NP_s$, so that~\eqref{eq:ownerseq} at the user cost is $W_{t+1}=(1+\rho)W_t+y_o-P_sc_{o,t}$, and let $c^*=(\rho W_0+y_o)/P_s\ge0$ be the constant plan's consumption. For $\beta<1$, summing the budget with weights $\beta^t$ and using $W_t\ge0$ gives $\sum_t\beta^tc_{o,t}\le\sum_t\beta^tc^*$ for every feasible plan; since $u$ is concave and increasing, Jensen's inequality with the weights $(1-\beta)\beta^t$ gives $\sum_t\beta^tu(c_{o,t})\le\sum_t\beta^tu(c^*)$. For $\beta=1$, the budget gives $\frac{1}{t_1}\sum_{t<t_1}c_{o,t}\le c^*+W_0/(t_1P_s)$ for every horizon $t_1$, and concavity and continuity bound the long-run average utility by $u(c^*)$. In both cases the constant plan attains the bound. (c) If $p_m>(\rho+\delta)V_m$, cutting consumption by $\varepsilon$ in one period and spending it on machines raises the next period's consumption by $(1+p_m/V_m-\delta)\varepsilon>(1+\rho)\varepsilon$, a first-order gain since $u'>0$; if $p_m<(\rho+\delta)V_m$, the reverse change gains. Both are feasible because $c_o>0$ and $X>0$. With $\beta=1$, the first change raises consumption in every later period, and the second, which buys fewer replacement machines once, raises it in every later period, so each raises the long-run average.
\end{proof}

\begin{proof}[Proof of Lemma~\ref{lem:prices}]
(i) The matrix $\mathbf A_\rho$ in~\eqref{eq:3} has spectral radius $\sqrt{(\rho+\delta)a}<1$ by Assumption~\ref{ass:machines}, so $(\mathbf I-\mathbf A_\rho)^{-1}=\sum_{t\ge0}\mathbf A_\rho^t\ge\mathbf 0$; its machine-hour row gives~\eqref{eq:tildem}, and $\mathbf z^{\top}$ applied to~\eqref{eq:4} gives $P_s$. (ii) Definition~\ref{def:equilibrium}(v): $X=YJ(x^*)/(1-a\delta)$, so labor and land are $YL_s$ and $YB_s$. (iii) $(\rho+\delta)/[1-(\rho+\delta)a]\ge\delta/(1-\delta a)$, with equality when $\rho=0$; and adding the cost equations as in main.tex 737--738 gives $P_sY=wN_a+r\ell+\rho V_mX$.
\end{proof}

\begin{proof}[Proof of Lemma~\ref{lem:ceiling}]
By~\eqref{eq:unitcost}, $p_m\gamma(x)-w=[(\rho+\delta)br\gamma(x)-wD(x)]/[1-(\rho+\delta)a]$, with $D(x)=1-(\rho+\delta)(a+\lambda\gamma(x))$. Where $D(x)\le0$ the difference is nonnegative, and it is zero only if $r=0$ and $D(x)=0$, at a single task because $\gamma$ increases strictly, or if $w=r=0$, which would make every price zero. Assumption~\ref{ass:machines} gives $D(0)>0$, so $x_c>0$.
\end{proof}

\begin{proof}[Proof of Proposition~\ref{prop:4} and Corollary~\ref{cor:vanishing}]
(12) is Lemma~\ref{lem:prices}(i). Below $x^*$, $p_m\gamma(x)\le w$, so $p=w(1-x^*)+p_mJ(x^*)\le w$; and $p\ge r\widetilde b_g$ because $\widetilde\lambda_g\ge0$. Space costs $r$. For the corollary, $p_m(1-\gamma(x^*)\widetilde\lambda_m)=r\widetilde b_m$ with the feedback term at least $\xi$ gives $r>0$, so Proposition~\ref{prop:2} applies and $w/r\le\gamma(x^*)\widetilde b_m/\xi\to0$, and $P_s\ge hr$ gives $w/P_s\le(w/r)/h\to0$. A worker works only if $\chi\le\log[(P_s+d+g_w+(1-\tau_w)w)/(P_s+d+g_e)]$, which is at most $\log(1+w/P_s)$ when $g_w\le g_e$; so $N_a/N\le F(\log(1+w/P_s))\to F(0)=0$, because $F$ is fixed and continuous.
\end{proof}

\begin{proof}[Proof of Corollary~\ref{cor:statics}]
(i) As at main.tex 729--734 for $N_D$, $v$ and $v/P_s$. Writing $v=\gamma\widetilde b_m/(1-\gamma\widetilde\lambda_m)$ with $r=1$ gives $v'=\widetilde b_m\gamma'/(1-\gamma\widetilde\lambda_m)^2=(p_m/r)\gamma'/(1-\gamma\widetilde\lambda_m)$, and $1/(1-\gamma\widetilde\lambda_m)=1+v\widetilde\lambda_m/\widetilde b_m=1+\lambda v/b$. (ii) As at main.tex 743.
\end{proof}

\begin{proof}[Proof that every equilibrium of Theorem~\ref{thm:1} is interior, with $w>0$ and $r>0$]
Take an equilibrium. By Definition~\ref{def:equilibrium}(i) and Lemma~\ref{lem:ceiling}, up to measure zero machines perform an initial segment $[0,x^*)$ of the open tasks, with $x^*\le x_c$.
\emph{The wage is positive.} If $w=0$, almost no worker works, since $F(0)=0$. If also $r=0$, every price is zero by~\eqref{eq:4}, contradicting $P_s>0$. If $r>0$, then $p_m>0$ because $b>0$, labor is strictly cheaper at every task, and labor demand is at least $Y=C\ge N>0$.
\emph{The rent is positive.} Suppose $r=0$. By~\eqref{eq:tildem}, $p_m=w\widetilde\lambda_m$, so machines are cheaper exactly at the open tasks where $\gamma(x)\widetilde\lambda_m<1$, and $x^*=x_c$. If $\lambda=0$ and $H$ is empty, every price but $w$ is zero and $P_s=0$. Otherwise $w/P_s=1/[1-x_c+\widetilde\lambda_mJ(x_c)]$. This is at least the limit of $v/P_s$ as the margin rises to $x_c$: equal to it when $\gamma(x_c)\widetilde\lambda_m=1$, and larger when $\gamma(x_c)\widetilde\lambda_m<1$, which requires $x_c=x_H$. So at least $N_S(x_c)$ hours are supplied. Land used, $YB_s(x_c)$, cannot exceed $T$, so at most $TL_s(x_c)/B_s(x_c)=N_D(x_c)$ hours are employed, and $N_D(x_c)<N_S(x_c)$ by~\eqref{eq:25}.
\emph{The margin is interior.} With $r>0$, Lemma~\ref{lem:owner}(a) gives $\ell=T$, so land is fully used. If $x^*=0$, no machine is used, $Y=T/h$, and labor demand $T/h$ exceeds $N$. If $x^*=x_c$ and $\gamma(x_c)\widetilde\lambda_m=1$, cost minimization needs $w\ge v(x)r$ for almost every $x<x_c$, and $v(x)\to\infty$ as $x$ rises to $x_c$. If $x^*=x_c=x_H$ and $\gamma(x_H)\widetilde\lambda_m<1$, the assignment is a boundary assignment with $w\ge v(x_H)r$. There $P_s=w[1-x_H+\widetilde\lambda_mJ(x_H)]+r[h+\widetilde b_mJ(x_H)]$, so $w/P_s$ rises with $w$ and is at least its value at $w=v(x_H)r$. Hence at least $N_S(x_c)$ hours are supplied, against a demand of $N_D(x_c)$, and~\eqref{eq:25} gives excess supply.
So $0<x^*<x_c$. By Propositions~\ref{prop:1} and~\ref{prop:2}, prices are \eqref{eq:21}--\eqref{eq:22} at $x^*$; quantities follow from Definition~\ref{def:equilibrium}(v) as in \eqref{eq:23}--\eqref{eq:24}; and labor-market clearing selects the unique crossing. If the owner's income covers the support at $x^*$, Lemma~\ref{lem:owner}(b) makes its constant plan optimal, and the remaining conditions hold as in the verification of main.tex 736--740; if it does not, $c_o<0$, and no equilibrium exists.
\end{proof}

\begin{proof}[Proof of Proposition~\ref{prop:5}]
Let $\mathbf f=C\mathbf z$. By Definition~\ref{def:equilibrium}, $\mathbf y=\mathbf A_0^{\top}\mathbf y+\mathbf f$ and $\mathbf p-\mathbf A_0\mathbf p=\bm\lambda w+\mathbf b r+(\mathbf A_\rho-\mathbf A_0)\mathbf p$, where $\mathbf A_\rho-\mathbf A_0$ has the single nonzero entry $\rho$, in the machine-hour's row and the machine's column. Hence
\[
I=\mathbf p^{\top}\mathbf f=(\mathbf p-\mathbf A_0\mathbf p)^{\top}\mathbf y=w\bm\lambda^{\top}\mathbf y+r\mathbf b^{\top}\mathbf y+\rho V_mX=wN_a+r\ell+\rho V_mX,
\]
and $r\ell=rT$ because $\ell=T$ when $r>0$. Intermediate payments cancel, while human hours and land services are counted at every stage; the machine row leaves the return on the stock. The inequality~\eqref{eq:15} follows from $\rho V_mX\ge0$, with equality when $\rho=0$. For the limit, $wN_a/I\le(w/r)N_a/T$.
\end{proof}
```

The proofs not drafted (Theorem 1's existence half, Proposition 6, Corollary 3) change only as §§3.1–3.3 say. Theorem 1 keeps main.tex's verification at 736–740.

### 3.6 Appendix B.1: production networks, and Table B.1

```latex
\section{Extensions of the economy}\label{app:extensions}

\subsection{Production networks}\label{app:networks}

\begin{assumption}[networks]\label{ass:network}
In place of the technology of Assumptions~\ref{ass:tasks} and~\ref{ass:machines}, there are finitely many produced goods, among them machines $K$, machine-hours $m$, and space $h$. Each good $i\ne m$ has a nonempty finite set of feasible methods; a method uses $a_{ij}\ge0$ units of each good $j$, $\lambda_i\ge0$ hours, and $b_i\ge0$ units of land services per unit of output. A machine-hour uses one machine for one period, together with operating inputs, which may be zero; space uses one unit of land services and nothing else; no other good uses machines directly. Some goods other than $m$ are task-produced: good $i$ requires one unit of each task in a set $\mathcal X_i\subseteq[0,1]$ of positive measure, with $\gamma_{Li}>0$, $\gamma_{Mi}\ge0$, and closed tasks $H_i$ as in Section~\ref{sec:technology}, and $\gamma_i=\gamma_{Li}/\gamma_{Mi}$ is continuous and nondecreasing on its open tasks. In place of~\eqref{eq:utility}, workers' utility is $\log\min_{i:z_i>0}(c_i/z_i)-\chi n$ for a basket $\mathbf z\ge\mathbf 0$, $\mathbf z\ne\mathbf 0$, with $z_m=z_K=0$.
\end{assumption}

An assignment of good $i$'s tasks gives every closed task to labor and the open tasks in a set $\mathcal M$ to machines; with the good's other inputs $(\mathbf a_i^0,\lambda_i^0,b_i^0)$ it generates the method
\begin{equation}\label{eq:assignment}
\lambda_i=\lambda_i^0+\int_{\mathcal X_i\setminus\mathcal M}\frac{dx}{\gamma_{Li}(x)},\qquad
a_{im}=a_{im}^0+\int_{\mathcal M}\frac{dx}{\gamma_{Mi}(x)}.
\end{equation}
For a selection of one method per good, $\mathbf A_\rho$ and $\mathbf A_0$ are its input matrices with the machine-hour's use of machines entered at $\rho+\delta$ and at $\delta$, \eqref{eq:4} defines the price coefficients, and $P_s=\mathbf z^{\top}\mathbf p$.

\begin{definition}[equilibrium in a network]\label{def:network}
An equilibrium of the economy of Assumptions~\ref{ass:land}--\ref{ass:owner} and~\ref{ass:network} is as in Definition~\ref{def:equilibrium}, with a method for each good in place of $\mathcal M$, the machine stock $X=y_m$, the price of a machine $p_K$ in place of $V_m$, and conditions~(i) and~(v) read in matrix form: the selected methods satisfy $\mathbf p=\mathbf A_\rho\mathbf p+\bm\lambda w+\mathbf b r$, with $\mathbf A_\rho$ of spectral radius below one, and no feasible method of any good, including any assignment of a task-produced good's tasks, has a lower unit cost at these prices; and gross outputs $\mathbf y\ge\mathbf 0$ satisfy $(\mathbf I-\mathbf A_0^{\top})\mathbf y=C\mathbf z$, $\bm\lambda^{\top}\mathbf y=N_a$, and $\mathbf b^{\top}\mathbf y=\ell$.
\end{definition}

Condition~(i) gives machines, up to a set of measure zero, the open tasks of each task-produced good at which $\gamma_i<w/p_m$, and labor those at which $\gamma_i>w/p_m$, together with every closed task; ties, which have positive measure only where $\gamma_i$ is flat, permit more than one cost-minimizing assignment. Good $i$'s margin $x_i^*$ is the essential supremum of its machine tasks, and Definition~\ref{def:margins} applies good by good; at every interior margin $\gamma_i(x_i^*)=w/p_m$, a value common to all goods, which we write $\gamma(x^*)$. Recursive automation lowers the labor requirements of feasible methods of the goods $j$ in the machine-hour's chain, those with $[(\mathbf I-\mathbf A_\rho)^{-1}]_{mj}>0$ at the selected methods. A \emph{human chain} for good $i$ is a set $S$ of goods that contains $i$ but neither machines nor machine-hours, together with a feasible method for each good in $S$ that uses inputs only from $S$ and, for a task-produced good, gives every task to labor, such that the methods' input matrix $\bar{\mathbf A}_S$ has spectral radius below one; its full-chain requirements $\bar\lambda_i$ and $\bar b_i$ are the entries for $i$ of $(\mathbf I-\bar{\mathbf A}_S)^{-1}\bar{\bm\lambda}_S$ and $(\mathbf I-\bar{\mathbf A}_S)^{-1}\bar{\mathbf b}_S$.

\begin{proposition}[the results in any production network]\label{prop:network}
In every equilibrium of Definition~\ref{def:network}:
(a) $\mathbf p=w\widetilde{\bm\lambda}+r\widetilde{\mathbf b}$ with $\widetilde{\bm\lambda},\widetilde{\mathbf b}\ge\mathbf 0$; $\mathbf y=C(\mathbf I-\mathbf A_0^{\top})^{-1}\mathbf z$; and $\widetilde{\bm\lambda}\ge(\mathbf I-\mathbf A_0)^{-1}\bm\lambda$ and $\widetilde{\mathbf b}\ge(\mathbf I-\mathbf A_0)^{-1}\mathbf b$, with equality when $\rho=0$;
(b) at an interior margin with $r>0$ and $\widetilde b_m>0$, Proposition~\ref{prop:2} holds, at given price coefficients;
(c) if $w,r>0$, every good $i$ with a human chain and $\widetilde b_i>0$ satisfies~\eqref{eq:13};
(d) along a sequence of equilibria with interior margins, $\gamma(x^*)\widetilde b_m\to0$ and $1-\gamma(x^*)\widetilde\lambda_m\ge\xi>0$ imply $w/r\to0$ and $w/p_i\to0$ for every good with $\widetilde b_i$ bounded away from zero; with $B_s$ bounded away from zero, $F$ fixed, and $g_w\le g_e$, also~\eqref{eq:14};
(e) Proposition~\ref{prop:5} holds, with $p_K$ in place of $V_m$;
(f) Corollary~\ref{cor:fiscal} holds.
\end{proposition}

\begin{proof}
(a) By Definition~\ref{def:network}, $(\mathbf I-\mathbf A_\rho)\mathbf p=\bm\lambda w+\mathbf b r$, and $(\mathbf I-\mathbf A_\rho)^{-1}=\sum_{t\ge0}\mathbf A_\rho^t\ge\mathbf 0$ because the spectral radius of $\mathbf A_\rho$ is below one. $\mathbf A_0\le\mathbf A_\rho$ entrywise, so $\mathbf A_0$ is productive too, the clearing conditions give $\mathbf y$, and $\sum_t\mathbf A_\rho^t\ge\sum_t\mathbf A_0^t$ term by term, with equality when $\rho=0$. (b) As for Proposition~\ref{prop:2}, from the machine-hour's row of (a); $\widetilde b_m>0$ makes the right side of $p_m(1-\gamma\widetilde\lambda_m)=r\widetilde b_m$ positive, and without it the closure is $0/0$. (c) For each good $j$ of the human chain $S$, Definition~\ref{def:network}(i) prices $j$ at no more than its human method's cost at market prices, so $\mathbf p_S\le\bar{\mathbf A}_S\mathbf p_S+\bar{\bm\lambda}_Sw+\bar{\mathbf b}_Sr$ entry by entry; substituting the inequality into itself $t$ times and letting $t\to\infty$ gives $\mathbf p_S\le(\mathbf I-\bar{\mathbf A}_S)^{-1}(\bar{\bm\lambda}_Sw+\bar{\mathbf b}_Sr)$, whose entry for $i$ is $w\bar\lambda_i+r\bar b_i$; the upper bound is $p_i\ge r\widetilde b_i$. (d) As for Corollary~\ref{cor:vanishing}: $p_m(1-\gamma\widetilde\lambda_m)=r\widetilde b_m\ge\xi p_m>0$ gives $r>0$ and $\widetilde b_m>0$, so $w/r\le\gamma\widetilde b_m/\xi\to0$, and $P_s\ge rB_s$ by (a). (e) and (f) As in the proofs of Proposition~\ref{prop:5} and Corollary~\ref{cor:fiscal}, with the cancellation run on $\mathbf A_\rho-\mathbf A_0=\rho\,\mathbf e_m\mathbf e_K^{\top}$.
\end{proof}

% B.2-B.6 follow: several non-produced inputs (576-588; the closure at 584), several machine types and trade (574 and
% inventory R3), worker types (622, 326), ideas and institutional rents (677), task-level costs (654-663).

\begin{table}[htbp]
\centering
\caption{Where the paper departs from the economy of Section~\ref{sec:economy}.}
\label{tab:departures}
{\small
\begin{tabular}{@{}p{4.4cm} p{10.2cm}@{}}
\toprule
Where & Departure \\
\midrule
Section~\ref{sec:history} & two worker types with schematic schedules; wage premia on particular tasks, entered as a multiplicative wedge \\
Appendix~\ref{app:extensions} & any production network with a choice among methods; several non-produced inputs; several machine types and trade in tasks; worker types; ideas and institutional rents \\
Appendices~\ref{app:ces} and~\ref{app:human} & CES preferences over goods in place of a fixed basket; in Appendix~\ref{app:human}, a separate wage on $H$ along an assumed price path \\
Appendix~\ref{app:fiscal} & partial-equilibrium incidence (Appendix~\ref{app:fiscal}.2) and a descriptive index outside the model (Appendix~\ref{app:fiscal}.5) \\
\bottomrule
\end{tabular}
}
\end{table}
```

**Proposition B.1** carries every network claim the judges tested: j4's 365 random durable networks; the human chain without machines or machine-hours, which fixes A's error; and b̃_m > 0, which fixes B's. B.2–B.6 follow from 574–588, 622, 326, 677 and 654–663 as listed in §1.1.

### 3.7 Other statements that change

| Lines | Change | Reason |
|---|---|---|
| 163–167 | Replaced by Def. 2 and Prop. 1(i)'s inequalities | False at the corner (Open 12i) |
| 205 | Cut | Durable machines are in the economy |
| 308 | Lemma 1(i), (iii) | Two coefficient sets (I-12) |
| 322 | "Theorem 1 proves existence and uniqueness; funding is necessary and sufficient" | Open 12(h) |
| 443 | Unchanged; true by definition | H depends on machines and rules, not on the worker |
| 473 | "If the trained worker and the entrant each held an interior margin against the same machine, Proposition 1(i) would apply to each…" | One worker type in the stated economy (R21) |
| 532 | "Appendix E shows that this can preserve aggregate labor income; most workers can still be exposed" | R21 |
| 540 | Its mapping moves to §2.6 and §1; §9 keeps the purchasing-power reading | AI in the model section and the opening |
| 574, 878 | "by capability, preference, or law" matches Ass. 1's H | Open 12(i) |
| 745 | "the cost of a basket at final tasks"; "provider's" → "owner's" | Mislabel; the agent's name |
| 805–808 (D.3) | P_s = wλ̃_s + rb̃_s; κ = T/(N[λ̃_s(w/r) + b̃_s]); "NB_s ≤ T is necessary" stays true | Price basis |
| 906 (App. F) | wλ̃⊤f "on the price basis" | Cost-based measure |
| 913 | "Table 1 lists the notation" | Table 1 |

---

## 4. Decisions for the authors

**Already decided by her (STATE.md, Log 2026-11-05) and adopted here:**
- the small stated economy, with the generality in App. B.1;
- the easy and hard paragraph;
- the standard-concept note;
- the does-not-depend remarks;
- precedence in place of a survey;
- results, then examples, then AI;
- proofs of Propositions 1–3 in the text;
- numbered assumptions;
- the optimizing owner;
- the question first.

The open ones follow, each with a recommendation and its trade-off in two sentences.

1. **Whether Definition 1 states the user cost, or leaves it to the owner's first-order condition.**
   - *Recommendation:* state it in (i), and prove that it is the first-order condition whenever c_o > 0 (Lemma A.1(c)).
   - *Trade-off:* Stated, it guarantees Theorem 1's uniqueness even where support absorbs all of the owner's income and the first-order condition does not bind. Left out, the definition is leaner, and scans of the return find no rival equilibrium on the instance or at δ = 0.2, but the theorem would then need a proof that none exists anywhere.
2. **Durable machines in the stated economy.**
   - *Recommendation:* yes, with the flow benchmark as (ρ, δ) = (0, 1).
   - *Trade-off:* The paper's only solved equilibrium has no flow version ((ρ + δ)a = 1.4 at (0, 1); I-11), and her owner decision presumes a return on machines. The price is two coefficient bases and "when ρ = 0" on the five statements of §4.2's remark.
3. **Which tasks are in H.**
   - *Recommendation:* closure by capability or by rule, H = {γ_M = 0} ∪ R.
   - *Trade-off:* 532, 574, 878 and Section 8's common wall (443) stay true, and Definition 3 keeps rules apart from capability. Lifting a reservation is then a policy change, not automation, which §8.2 must say.
4. **The base of the rent tax.**
   - *Recommendation:* rental value whether or not the land is used, as a land-value tax.
   - *Trade-off:* Proposition 6(i) becomes a result for every τ_R ∈ [0, 1]. With a tax on rent received the owner is indifferent at τ_R = 1, exactly (16)'s κ = 1 case, so (i) would hold only for τ_R < 1.
5. **Public provision of the basket (σ).**
   - *Recommendation:* include it.
   - *Trade-off:* It gives 423's replacement case, (16) and 437's wage-funded support a formal home, and shows that the measured κ = 0.30 needs a source of support beyond rent. It adds one instrument and one budget term, and checks under five policies show the definition stays consistent (S3).
6. **Table 2's third target.**
   - *Recommendation:* relabel it "final-task labor's share of a basket's cost".
   - *Trade-off:* Relabeling moves no number: 0.469 is what `appendix_b.py` computes and check Q5 tests. A full-chain target (0.551 physical, 0.733 on the price basis) would move every number of the instance, Figure 3 and the templates.
7. **Measurement and history within her order.**
   - *Recommendation:* examples (§6), then Measurement (§7), then History and stabilizers (§8), then AI and the conclusion (§9).
   - *Trade-off:* The evidence then comes before its interpretation, and AI stays last, as she decided. Figures renumber (5–7 → 4–6, 4 → 7), and the README's figure table must change.
8. **Labels and notation.**
   - *Recommendation:* semantic labels and the Open 12(j) renames at the rewrite, keeping a, λ, b, v, V_m, Y and s.
   - *Trade-off:* The renames remove every overload STATE lists, and keeping those symbols spares six `check_interior.py` templates and Figure 3's legend. The header comment at line 7 must change, and Appendix B.1 writes the machine's price p_K.
9. **Citations and the opening's precedents.**
   - *Recommendation:* read and then cite the AI-macro papers STATE lists as checked on Crossref:
     - Restrepo (2025), NBER w34423;
     - Korinek and Juelfs (2022), w30172;
     - Korinek and Lockwood (2026), w34873;
     - Trammell and Korinek (2023), w31815, Annual Review of Economics 2026.

     Consider its precedents for the opening: Keynes (1930); Ricardo's Notes on Malthus (1820); Leontief (1983). Add Economic Modelling's own papers and production-network work only after reading them.
   - *Trade-off:* The special issue is on "Artificial Intelligence, Data Investment and the Digital Economy", and the current reference list has none of these. I have read none of them here, so their content must not be described until it is checked.
10. **New results.**
    - *Recommendation:* include Corollary 1(i)'s equilibrium rate, Lemma A.1, and Proposition B.1.
    - *Trade-off:* All three are proved and checked; they give Proposition 1(ii) its equilibrium counterpart, the owner its problem, and the network its statements. Each is a statement a referee can test, and Corollary 1(i) can go if the authors want no new claims.
11. **Workers who neither save nor borrow.**
    - *Recommendation:* state it in Assumption 4.
    - *Trade-off:* With an owner who lives forever, it is what keeps the participation choice (8)–(10) period by period. Workers who could save at ρ would smooth by working in some periods only, a richer model that the paper's Future Work already points to (555).
12. **How to port.**
    - *Recommendation:* build the rewrite on a scratch copy with exact one-match replacements, run the lint and a re-pointed `check_interior.py`, and add a uniqueness group (an `x_H` parameter in `code/appendix_b.py`), all before `main.tex` is touched.
    - *Trade-off:* The battery then backs Theorem 1's uniqueness half, Lemma A.1, the policy cases and Proposition B.1, not only existence. It costs about 6–8 of the 30–38 hours estimated in §6 of this note.

---

## 5. Mathematical claims the design relies on that main.tex does not prove as written

Five claims, each stated so that it can be checked. Scripts are in `_work_synthesis/` and `judge/` of this folder.

### Claim 1. Prices and the replacement closure with durable machines, in the stated economy and in any network

**Statement.** In every equilibrium of Definition 1, and of Definition B.1 under Assumption B.1:
- (a) p = wλ̃ + rb̃ with λ̃ = (**I** − A_ρ)⁻¹λ ≥ 0 and b̃ = (**I** − A_ρ)⁻¹b ≥ 0.
- (b) λ̃ ≥ (**I** − A_0)⁻¹λ and b̃ ≥ (**I** − A_0)⁻¹b. Equality holds when ρ = 0, for every δ ∈ (0, 1]. In the stated economy, P_s = wL_s + rB_s + ρV_mX/Y.
- (c) At an interior margin with r > 0 and b̃_m > 0 (automatic in the stated economy, since b > 0), 1 − γ(x*)λ̃_m > 0 and w/r = γ(x*)b̃_m/(1 − γ(x*)λ̃_m).
- (d) b̃_m > 0 cannot be dropped in a network. If the machine chain uses no land, then p_m = wλ̃_m at every margin, an interior margin forces γ(x*)λ̃_m = 1, and (5) is 0/0.

**Checked.**
- Analytically: (a) by the Neumann series; (b) because A_ρ ≥ A_0 entrywise; (c) from the machine-hour row and Proposition 1.
- On 365 random durable networks (`judge/j4_networks.py`, rerun), with operating inputs, walls and machines built partly from a task good:
  - price identity error at most 6.7·10⁻¹³;
  - closure error at most 1.9·10⁻¹³ at the 314 interior margins;
  - price coefficients never below physical ones, and equal on the 73 networks with ρ = 0.
- On the instance (S1b): w/r = 0.071654 on price coefficients, which is the solver's v, against 0.011620 on physical ones; P_s = 0.0259890 on both decompositions.

**Why it matters.** It is what lets durable machines into the stated economy without qualifying Propositions 2 and 4 or Corollary 2.

### Claim 2. The purchasing-power bounds and their limits, with corrected hypotheses

**Statement.** In every equilibrium of Definition B.1 with w, r > 0, take any good i and any human chain S that contains it. S contains neither machines nor machine-hours; each good in S has a method using inputs only from S and giving every task to labor; and the spectral radius of Ā_S is below one. Then r b̃_i ≤ p_i ≤ w λ̄_i + r b̄_i.

In the stated economy this reads 1 ≤ w/p ≤ (w/r)/b̃_g and w/p_h = w/r.

Along a sequence of equilibria with interior margins, suppose γ(x*)b̃_m → 0 and 1 − γλ̃_m ≥ ξ > 0. Then:
- w/r → 0, and w/p_i → 0 whenever b̃_i ≥ b̲ > 0;
- if also B_s ≥ B̲ > 0 (automatic, B_s ≥ h, in the stated economy), F is fixed and g_w ≤ g_e, then w/P_s → 0 and N_a/N → 0.

Both added hypotheses are needed:
- With g_w − g_e = θP_s and F fixed, N_a/N ≥ F(log(1 + θ)) > 0.
- With F varying, participation can stay bounded away from zero (the theorist's and referee's counterexamples to A).

**Checked.**
- Analytically: the lower bound by iterating p_S ≤ Ā_S p_S + λ̄_S w + b̄_S r. The participation limit from log[(P_s + d + g_w + (1 − τ_w)w)/(P_s + d + g_e)] ≤ log(1 + w/P_s) when g_w ≤ g_e.
- Numerically:
  - j4's human-chain bound: maximum violation 3.2·10⁻¹⁶.
  - S5, on the path (λ = 0, η from 1 to 10⁻⁵): with equal payments of 0.2P_s, participation falls from 0.516 to 0.0002; with an in-work payment of 0.2P_s, it falls to 0.0830 against F(log 1.2) = 0.0829.
  - j3: C's case g_w = P_s gives 0.693 = F(log 2).

**Why it matters.** It is the headline result, vanishing purchasing power and participation, now true under a definition that admits policy. It also fixes the hypotheses A dropped ("F fixed") and C omitted (payments).

### Claim 3. Income with the return on machines, labor's share, and the automation path

**Statement.** In every equilibrium, I = P_sC = wN_a + rT + ρV_mX. If r > 0, then wN_a/I ≤ (w/r)N_a/[(w/r)N_a + T], with equality if and only if ρV_mX = 0. With N_a ≤ N and T fixed, w/r → 0 implies wN_a/I → 0.

On the path (λ = 0, γ_η = ηγ, Table 2's other parameters), x_c = 1 and (25) holds for every η ∈ (0, 1]. Also:
- v ≤ ηπ, with π = (ρ + δ)b/[1 − (ρ + δ)a] = 0.06965;
- P_s ≤ (ηπ + h)r;
- X ≤ ηT/[h(1 − aδ)].

So rent alone funds support for η ≤ (T − Nh)/(Nπ) = 0.1192, and R/I → 1 as η → 0.

**Checked.**
- Analytically: the cancellation with A_ρ − A_0 = ρ e_m e_K⊤. The path bounds follow from p_mγ_η ≤ w below x*, J_η ≤ η, and Y ≤ T/h. (25) holds because labor demand at x = 1 is zero while supply is positive.
- Numerically:
  - The instance (S1c): labor's share is 0.5505 against the bound 0.8117; the interest share is 0.3218.
  - j4 income identity: error at most 1.8·10⁻¹⁵.
  - S4, at 1,201 values of η in [10⁻⁴, 1]:
    - every bound holds;
    - rent alone funds support up to η ≈ 0.78;
    - rent and interest fund it on the whole grid;
    - R/I = 0.27 at η = 1 and 0.9995 at 10⁻⁴.
  - `path25.py`: the (25) margin stays positive to η = 10⁻⁵.
  - `path_numbers.py` confirms STATE's 0.0179 at η = 0.001.

**Why it matters.** Proposition 5, Corollary 3 and the path's "funded throughout" (747, R35) rest on it. Without the interest term labor's share would be misstated: 0.81 instead of 0.55.

### Claim 4. Theorem 1: existence and uniqueness of the stated economy's equilibrium

**Statement.** With every instrument zero and σ = 1, suppose T > Nh and N_S(x_c) > N_D(x_c). Then:
- every equilibrium of Definition 1 has w > 0, r > 0 and an interior margin, at the unique x* ∈ (0, x_c) with N_D(x*) = N_S(x*);
- its prices and quantities are (21)–(24) at x*, up to numeraire and null sets;
- an equilibrium exists if and only if rT + ρV_mX ≥ NP_s at x*.

The printed instance satisfies every condition of Definition 1.

**Checked.**
- Analytically: the exclusion proof in App. A rules out w = 0; r = 0 at the ceiling or at the wall; the corner; a margin at the economic ceiling; and a boundary at the wall. N_D falls and N_S does not on (0, x_c) (728–734). Existence follows with Lemma A.1.
- Numerically:
  - `_work_B/wall_test.py` W1–W5 pass.
  - `judge/j2_uniqueness.py`, an independent scan over w/r ∈ [10⁻⁹, 10⁶] that does not assume an interior margin, finds exactly one candidate on the five solver economies and with a wall at 0.90. Where (25) fails (walls at 0.825 and 0.80), it finds boundary equilibria.
  - S1: C from the budgets = Y = 3.013205 and c_o = 0.354.
  - S8: at δ = 0.2, (25) holds but support costs 0.405 against income 0.112, so there is no equilibrium. The funding condition is not vacuous.

**Why it matters.** It closes Open 12(h) and gives the paper Lucas's existence-and-uniqueness step for the economy it states and solves.

### Claim 5. Definition 1 is consistent, every agent optimizes, and Propositions 1 and 3 hold in every equilibrium

**Statement.**
- (a) Lemma A.1. Take constant prices with rental (ρ + δ)V_m, P_s > 0, V_m > 0, and a tax on rental value with τ_R ∈ [0, 1].
  - The owner rents out ℓ = T whenever r > 0.
  - The constant plan with c_o = [rℓ − τ_R rT + ρV_mX]/P_s − σN ≥ 0 maximizes Σβ^t u(c_o,t) (β < 1) or long-run average utility (β = 1).
  - If c_o > 0 and X > 0, optimality forces p_m = (ρ + δ)V_m, the first-order condition.
- (b) Walras. For every policy satisfying `govbudget`, the budgets give C·P_s = wN_a + rℓ + ρV_mX, so final-good clearing follows from the rest.
- (c) Propositions 1 and 3. In every equilibrium with w, p_m > 0:
  - w = p_mγ(x*) at an interior margin, w ≥ p_mγ(x_H) at a boundary, and w ≤ p_mγ(0) at a corner;
  - with τ_w = d = g_w = g_e = 0, for either σ, N_a = NF(log(1 + w/P_s)).

**Checked.**
- Analytically: present-value budget and Jensen's inequality; a first-order deviation for the converse; the sum of the three budgets.
- Numerically:
  - S2: all 1,553 random feasible deviations at the instance lose (largest gain −3.0·10⁻⁶), and a return of ρ ± 0.01 makes a two-period deviation gain about 8·10⁻⁶.
  - S2b: the land choice under both tax bases.
  - S3: five policies solved as equilibria. In each, |C − Y| ≤ 1.3·10⁻¹⁵, the budget balances and c_o ≥ 0.
  - `knife_edge.py`, `knife_edge2.py`: no zero-consumption configuration at another return, on the scanned ranges.

**Why it matters.** It answers the three judges' fatal flaw for B (Definition 1 under policy) and the owner defects (land supply stipulated; "indifferent to its stock"). It also implements her decision that the owner optimizes.

---

## 6. Checks, port and effort

**`checks/check_interior.py`** (the anchors) breaks by design. Its regions and templates are re-pointed:

| Item | Now (file lines) | Here |
|---|---|---|
| R_B | Appendix B's title → Appendix C's (414) | §6's title → §7's title |
| R_S5 | Section 5 → Section 6 (415) | §3.2's title → §3.3's; Q3's quoted P_s sentence becomes Lemma 1(iii) |
| R_CAP | Figure 3's caption (416) | Unchanged |
| R_61 | 6.1 → 6.2 (417) | §4.1 → §4.2; the "hundred-to-one" anchor is kept |
| R_D3 | D.3 → D.4 (418) | Unchanged; Q4's sentence becomes the price-basis one |
| "flow benchmark" (448) | 685's sentence | Ass. 2's gloss; new region |
| "instance" (449) | Parameters inline | Templates for Table 2's rows; Q2[B] scans R_B without R_CAP, as Q3 does |
| "shares" (453) | "…full-chain cost of consumption…" | The relabeled sentence (decision 6); Q5 unchanged |
| "support" (459) | "provider's" | "owner's" |
| "path participation" (anchors "…at η = 0.01.") | Kept: the new 0.018 sentence follows it | One new template |

**New check groups.**
- U: Theorem 1's uniqueness, from `wall_test.py` and `j2_uniqueness.py`, with `x_H` added to `appendix_b.py`.
- O: Lemma A.1, from S2.
- W: Walras under policy, from S3.
- P: the path's bounds, funding, R/I and the 0.018 point, from S4, `path25.py` and `path_numbers.py`.
- C2: Corollary 2's payment condition, from S5.
- E12b: Corollary 1(i)'s rate, from S7.
- Durable networks in `check_cost_system.py`, from j4, for Proposition B.1.

**Port discipline (graft from C).**
1. Apply every edit as an exact one-match replacement on a scratch copy.
2. Run the lint and the re-pointed `check_interior.py`.
3. Produce word diffs with `../tools/word_diff_report.py` for her read, then Johan's and Magnus's.
4. Only then edit `main.tex`.

The drafts reuse the authors' sentences wherever the content carries over (each is marked with a `%` source line). That keeps STATE's "never re-voices" rule as far as a rewrite can. The new prose (the opening, the assumptions and the remarks) is hers to re-voice.

**Effort.** About 30–38 hours: four or five drafting sessions and one of checking, plus the authors' reading. B estimated 25–33; the owner's lemma, the budgets, σ, the remarks and Appendix B.1 add about 5.

---

## 7. Verification record

Every script below was run here; no compile was possible.

| Script | Result |
|---|---|
| `_work_synthesis/verify_synthesis.py` | 12 of 12 pass (S1–S8) |
| `_work_synthesis/path25.py`; `path_numbers.py` | (25) holds on the path to η = 10⁻⁵; STATE's 0.60, 0.56, 0.13, 0.018 and the fork ratios 1.78 and 426 reproduced |
| `_work_synthesis/knife_edge.py`; `knife_edge2.py` | No zero-consumption equilibrium at another return on the scanned ranges, on the instance or at δ = 0.2 |
| `_work_synthesis/explore_funding.py` | 41 economies near the instance where (25) holds and funding fails |
| `_work_B/wall_test.py` (rerun) | 8 of 8 pass |
| `judge/j1`–`j4` (rerun) | As quoted in §5 |
| `checks/lint_tex_structure.py` on `_work_synthesis/drafts_synthesis.tex` | ALL GREEN |
| `_work_synthesis/wc_strict.py`, `count_blocks.py` | The word counts of §1.6 |

All scripts import `code/appendix_b.py` read-only, with bytecode writing disabled.

## Files

All in `/tmp/claude-0/-home-user-labor/904c7da5-c8e1-5390-ac85-b6fa3b59f016/scratchpad/design/`:

| File | Contents |
|---|---|
| `synthesis.md` | This note, assembled by `_work_synthesis/assemble.py` from `_work_synthesis/synthesis_template.md` |
| `_work_synthesis/drafts_synthesis.tex` | Every LaTeX block above, linted; `drafts_synthesis_v1.tex` is the version before her recorded decisions were folded in |
| `_work_synthesis/verify_synthesis.py`, `path25.py`, `path_numbers.py`, `knife_edge.py`, `knife_edge2.py`, `explore_funding.py` | The checks |
