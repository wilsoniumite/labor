# Build brief: the full rewrite of "Pinning the Wage to Scarcity and Technology"

Date: 2026-11-05. Authors: Johan Båge and Stella Wilson. Stella is the co-author steering this
rewrite. The rewrite is for the Economic Modelling special issue on AI, with double-anonymized
review. It answers Magnus's notes: cut the literature survey (Section 2), introduce the model
systematically, and make the research question clear. Lucas (1978) is the model of exposition.

## 0. Where things are

| What | Path |
|---|---|
| The paper now (READ ONLY; never edit) | /home/user/labor/pinning/paper/main.tex (983 lines; labels sec:N, eq:N, prop:N, fig:N, app:X) |
| Its baseline PDF (41 pages, compiles clean) | SP/build/baseline/main.pdf |
| Decisions log (read the 2026-11-05 entries) | /home/user/labor/pinning/STATE.md, from "2026-11-05 — a rewrite asked for" to the end of that entry |
| The merged model-section design | SP/design/synthesis.md (§1 architecture, §2 LaTeX of the economy, §3 restated results with proofs, §3.5 Appendix A, §3.6 Appendix B.1, §3.7 other statements, §4 decisions, §5 claims, §6 port plan) |
| Its draft TeX pieces | SP/design/_work_synthesis/ (drafts_synthesis.tex is the assembled design draft) |
| The math checks of the design (full text) | SP/build/verdicts_full.md |
| Section 2 "Description of the economy" (v3, final) | SP/design/section2_description.md |
| The introduction (v2, final for now) | SP/intro/narrative_draft.md |
| Literature notes and verified quotes | SP/rq/precedence.md, SP/rq/quotes.md, texts in SP/rq/txt/ |
| Inventories of the paper | SP/design/inventory_results.md, inventory_primitives.md, inventory_section2.md |
| Repo checks | /home/user/labor/pinning/checks/ (lint_tex_structure.py, check_interior.py, check_cost_system.py, check_pinning.py, check_fan.py, corner/) |
| Solver for the numerical economy | /home/user/labor/pinning/code/appendix_b.py (import read-only; run Python with -B so no bytecode is written) |

SP = /tmp/claude-0/-home-user-labor/904c7da5-c8e1-5390-ac85-b6fa3b59f016/scratchpad

Write only under SP/build/. Never edit anything under /home/user/labor; the parent session copies the
result into the repository.

## 1. The rules

1. **Port, don't re-voice.** The authors' sentences survive verbatim wherever their content carries
   over. Put a provenance comment before every paragraph:
   - `% from main.tex L<n>` or `% from main.tex L<n>-<m>`: verbatim;
   - `% from main.tex L<n>, edited: <what changed and why>`: allowed only for cross-references, a
     notation rename from the design's Table 1, citation years, or the minimum change a math fix in
     §4 below requires;
   - `% NEW (design synthesis §x.y)`, `% NEW (section2_description v3)`, `% NEW (narrative_draft v2)`
     or `% NEW`.

   The design's drafts already carry `% NNN` source-line comments; keep them in the provenance
   form. Never improve the authors' prose. If one of their sentences must change for correctness,
   change the minimum and list it in your notes file as a one-word decision for Stella.
2. **New prose** (only where the design or the drafts supply it, or a fix needs it) is plain and
   concrete:
   - never "turn" or "turns" in any sense;
   - no new em-dash asides (the authors' own "---" stay);
   - no "not X but Y" contrasts, staged openers, forced triads, inflated words (novel, crucial,
     fundamental, key, landscape, delve, notably) or one-line closers.
3. **Numbers.** Every number printed must already be in main.tex, in the design (which verified
   them), or be recomputed from code/appendix_b.py. Never invent or round differently from the
   source.
4. **LaTeX.**
   - The fragment must compile inside the shared preamble (§3 below), with no new packages unless
     you say why.
   - Use the label scheme in §3; list every label you define and every label you reference in your
     notes file.
   - Keep figure files and \includegraphics paths as in main.tex; figures are in paper/figures/.
5. **Citations.** Cite only works in main.tex's reference list or the new ones listed in §5. The
   citation style is plain text, "Author (year)", as in main.tex; there is no \cite.

## 2. The structure (final section order)

| § | Title (label) | Built from |
|---|---|---|
| — | Preamble, title, authors, abstract, keywords, JEL | main.tex 1–69 verbatim, with the theorem environments replaced by synthesis §2.0. The abstract is unchanged; flag it as a later decision. |
| 1 | Introduction (sec:intro) | narrative_draft.md v2: its NEW paragraphs exactly as written, the authors' lines 72, 74, 76, 78–86 verbatim where it says so, its closing paragraph (one "This paper argues" sentence, then the authors' George sentence, line 90 sentence 4), then a roadmap for THIS section order (new; no "turns"). |
| 2 | Description of the economy (sec:description) | section2_description.md v3, exactly as written. Its only citations are Zeira (1998) with Acemoglu and Restrepo (2018), and Leontief (1936) with Sraffa (1960). "Section 6 uses its instruments" must point to sec:rent. |
| 3 | Definition of equilibrium (sec:economy) | Opens with the primitives sentence in Lucas's form (in section2_description.md). Then synthesis §2.1 from "\subsection{Tasks, machines, and land}" through the AI paragraph that closes it: Assumptions 1–5, the cost system, workers, the owner and support, government, Definition 1, the note that the concept is standard, the wedge remark, Definitions 2–3, the loom and the AI paragraph. Then Table 1 (synthesis §2.2). Apply fix F5 (§4). |
| 4 | Equilibrium (sec:equilibrium) | synthesis §3.1, without its opening "What is easy and what is hard" paragraph (it moved to §2). Lemma 1; Propositions 1–3 with their proofs; Figures 1–2; the loom; (6); participation, with the authors' lines 294–300 (the enclosure paragraph with Marx, Polanyi and Lewis); (10)–(11); Lemma 2; Theorem 1; Corollary 1. A remark after each result on what it does not depend on. Add the citations of §5 placed here. |
| 5 | Purchasing power and income (sec:purchasing) | Opens with the authors' line 88 paragraph, moved verbatim. Then synthesis §3.2: Proposition 4, the authors' line 90 sentence 1 directly after it (edited only to "Acemoglu and Restrepo (2018)"), the readings at 351–353, Corollary 2 with fix F2, Proposition 5 with fix F3. Add the citations of §5 placed here. |
| 6 | Distribution: rent taxation and a uniform transfer (sec:rent) | synthesis §3.3: Proposition 6, (16) with public provision, Corollary 3, 425 and 437–439. Then, after eq. (17): the two lines the design and STATE ask for (see F6), then the lilies aside (§6 below). Korinek and Lockwood (2026) go beside George (§5). |
| 7 | A numerical economy and an automation path (sec:example) | synthesis §3.4: Table 2, the instance (745), Figure 3 with the AI framing in the text, the statics (324), the path (747), with funding proved for small eta and the 0.018 point. |
| 8 | Measurement (sec:measurement) | The authors' Section 9 (475–528) verbatim. Only cross-references and figure numbers change. |
| 9 | History and stabilizers (sec:history) | 9.1 is the authors' Section 8 (441–473), shortened by about a third as the design says, by cuts of whole sentences only; list every cut. "473 stated as a conditional" is an edit: make the minimum change and list it. 9.2 is the authors' Section 10 (530–536), with reservations named as a policy (synthesis; inventory R21): minimum edits, listed. The design opens 9.1 with the authors' line 326 (heterogeneity). |
| 10 | Artificial intelligence and conclusion (sec:ai) | The authors' Section 11 (538–550), less what the design moved to §1 and §3 (for example line 540's two-margins paragraph, now §3's AI paragraph); keep the rest verbatim. Then Section 12, Future Work (552–559), condensed to two paragraphs by cuts only (the monetary-policy and sovereign-fund paragraphs become one sentence each, per the design; take those sentences verbatim from the paragraphs). Put the Leontief aside (§6 below) directly after "A tax on pure fixed-factor rents can fund a payment paid equally in and out of work; the coverage ratio determines whether it can finance the full basket." |
| A | Proofs (app:proofs) | synthesis §3.5: Lemma A.1 (the owner), with fix F4; the proofs of Lemmas 1–2, Theorem 1, Corollaries 1–3 and Propositions 4–6; Proposition 5's identity with the interest term. |
| B | Extensions of the economy (app:extensions) | synthesis §3.6 and §1.3: B.1 production networks (app:networks: Assumption B.1 with fix F1, Definition B.1, the human chain, Proposition B.1); B.2 several non-produced inputs; B.3 several machine types and trade (the authors' Section 2.3 trade sentences, verbatim, belong here); B.4 worker types; B.5 ideas and institutional rents (677); B.6 task-level costs ((20), A.3); Table B.1 (departures). Material from the authors' A.1 and A.3–A.4 moves here verbatim where it survives. |
| C | Expenditure shares under substitution | The authors' Appendix C (759–763), with alpha renamed omega; its identity part moved into Proposition 5's proof. |
| D | Fiscal transition | The authors' Appendix D (765–874). m_w, m_e become g_w, g_e. D.2 gains the authors' Section 2.7 payroll-incidence sentences verbatim ("Payroll incidence: the quasi-experimental literature (Gruber 1997; Kugler and Kugler 2009; Saez, Schoefer, and Seim 2019) ..."). D.3 is on the price basis, as the design says. Apply any D fix the design lists in §3.7. |
| E | Human-required tasks | The authors' Appendix E (876–890); the H pointer updated. |
| F | The financing and production accounts | The authors' Appendix F (892–910); the price-basis mapping as the design says. |
| — | Back matter | The data, notation and checks note (913), with its notation sentence replaced by "Table 1 lists the notation"; the AI declaration (915–917) verbatim; the references (§5). |

Labels:
- Keep the design's semantic labels (sec:technology, sec:costs, sec:workers, sec:owner,
  sec:government, sec:eqdef, lem:prices, lem:ceiling, lem:owner, thm:1, def:equilibrium,
  def:margins, def:automation, ass:tasks ... ass:owner, tab:notation, eq:unitcost, eq:tildem,
  eq:utility, eq:budget, eq:ownerseq, eq:ownerbudget, eq:govbudget, ...).
- Old labels stay where the object survives: prop:1 ... prop:6, eq:1 ... eq:17, fig:N, and
  app:B ... app:F only where the design keeps them; app:D.x stays.
- New section labels are as in the table above, plus app:proofs, app:extensions and app:networks.

## 3. The preamble

main.tex lines 1–40 verbatim, except that lines 35–38 (the theorem environments) are replaced by
synthesis §2.0's block. The design's draft also needs these packages, already loaded in main.tex:
\usepackage{booktabs}, \usepackage{bm}. The appendix counters
(\counterwithin{lemma}{section} etc.) go beside main.tex 562–565 as the design notes.

## 4. Fixes from the math checks (SP/build/verdicts_full.md has the full text)

- **F1. Appendix B.1, networks.** Under the drafted Assumption B.1, a task good whose open tasks
  form two separate pieces can have an interior margin where gamma(x*) != w/p_m, and the closure
  then fails. Fix: Assumption B.1 requires each task good's open tasks to form an interval, as in
  the stated economy, so that gamma_i(x_i*) = w/p_m at every interior margin.
- **F2. Corollary 2's remark on in-work payments.** synthesis.md line 1259 says that
  "g_w − g_e = theta P_s gives N_a/N >= F(log(1+theta))". That holds only when d = g_e = 0.
  - The correct bound is N_a/N >= F(log(1 + theta P_s/(P_s + d + g_e))).
  - Use it, or state the remark only for d = g_e = 0.
  - Also: "F fixed" may be weakened to F_k(eps_k) -> 0 whenever eps_k -> 0, and g_w <= g_e is
    sufficient but not necessary. You may keep the drafted, stronger hypotheses; do not claim
    necessity.
- **F3. Proposition 5.** "with equality iff rho V_m X = 0" fails when nobody works: both sides are
  then zero. Fix: "with equality if rho V_m X = 0, and only if when N_a > 0", or equivalently
  "iff rho V_m X N_a = 0". Every equilibrium with an interior margin has N_a > 0.
- **F4. Lemma A.1(a).** "every optimal plan rents out l_t = T in every period" is false at beta = 1
  under the long-run-average criterion. Fix: "If beta < 1, every optimal plan rents out l_t = T in
  every period when r > 0; when beta = 1, every optimal constant plan does." Theorem 1's proof and
  Proposition 6(i) use only constant plans and are unaffected.
- **F5. The user cost in Definition 1.**
  - KEEP Definition 1(i)'s clause that machine-hours rent at the user cost. Lemma A.1(c) shows that
    whenever the owner consumes (c_o > 0) and holds machines, the clause is the owner's
    first-order condition, as Stella decided.
  - The clause is load-bearing for uniqueness. Without it, the printed instance has a second
    stationary configuration in which the owner consumes nothing, land is partly idle at zero
    rent, and the return on machines is 0.192.
  - So DELETE the design's claim that the clause "costs nothing" (synthesis.md around lines
    584–587 and 1183, and any draft text saying so). Replace it with one plain sentence: when
    support absorbs all the owner's income, the first-order condition does not bind, and the clause
    selects the user cost at rho.
  - Do NOT require c_o > 0 in Definition 1. That would rule out the full-rent-capture equilibria of
    the flow benchmark (owner income zero) on which eq. (17) rests.
- **F6. After eq. (17)** (STATE: "Eq. (17) is narrower than the question it would answer"), add two
  lines, using the design's claim 3 and the check script SP/intro/verify_claims/durable_coverage.py:
  - With several non-produced inputs, the condition holds input by input: full capture funds one
    basket per person exactly when N B_{s,k} <= T_k for every input k. Check this against
    Appendix B.2 before writing it.
  - With durable machines, rent and interest together fund the basket. On Appendix B's parameters
    at full automation, full capture of rent and interest funds 1.71 baskets per person, and rent
    alone funds 0.66.
  - State only what is shown. If the several-input line cannot be proved in a sentence, say so in
    your notes and write the durable line only.

## 5. Citations: what is kept, and where

Stella's rule: "we don't need to revive everything from the cut section two, only when their time
comes later in the paper." The introduction is not a survey. Place a Section 2 citation in the body
only where a body passage makes the specific point it supports:

| Citation | Where |
|---|---|
| Shapiro and Stiglitz (1984); Card, Cardoso, Heining and Kline (2018); Acemoglu and Restrepo (2026) | §3, the wedge remark after Definition 1 (already in the design's text) |
| Marx (1867), Polanyi (1944), Lewis (1954) | §4, already in the authors' line 300 |
| Korinek and Stiglitz (2019), below-subsistence clause | §4, where dependence and exit are discussed, as the authors' line-128 clause, made a sentence: "Korinek and Stiglitz (2019) pose the below-subsistence scenario explored here through dependence and exit." Mark it `% from main.tex L128, edited: semicolon to period`. |
| Restrepo (2025) | §4, after Proposition 2 or 1, one sentence: "Restrepo (2025) finds that wages converge to the opportunity cost of computational resources required to reproduce human work." The quotation is exact (SP/rq/txt/w34423.txt line 53). |
| Trammell and Korinek (2026) | §3's AI paragraph or §4's two-margins passage (eq. 6), one sentence: "Trammell and Korinek (2026) find that fully automating production, so that machines can self-replicate, would raise growth and lower the labor share." Their Annual Review abstract says this. |
| Caselli and Manning (2019) | §5, beside Proposition 4's lower bound: the authors' line-128 sentence, with only its section pointer edited. |
| Karabarbounis and Neiman (2014); Rognlie (2015); Knoll, Schularick and Steger (2017) | §5, at Proposition 5 (labor's share), as the design's 393 qualification: the authors' Section 2.7 factor-share clause, verbatim, without Piketty and Zucman. |
| Korinek and Lockwood (2026) | §6, beside George (1879) at 439, one sentence: "Korinek and Lockwood (2026) show that in an economy without labor, taxing fixed factors is non-distortionary and can redistribute." |
| Gruber (1997); Kugler and Kugler (2009); Saez, Schoefer and Seim (2019) | Appendix D.2, the authors' Section 2.7 payroll sentences, verbatim |
| Aghion, Jones and Jones (2019) | Appendix E, already there (878) |
| Hémous and Olsen (2022) | §3, Definition 3's sentence that the direction of technical change is taken as given, if the design's text has it; otherwise drop |
| Ricardo (1817), Malthus (1798) | Named without years in the authors' line 469. Leave 469 verbatim. They drop from the references unless cited; list as a decision for Stella. |

Everything else that Section 2 alone cited drops: Samuelson (1966), Uzawa (1961), Diamond (1982),
Mortensen and Pissarides (1994), Pissarides (2000), Shimer (2005), Hagedorn and Manovskii (2008),
Hall (2005), Ljungqvist and Sargent (2017), Acemoglu and Autor (2011), Acemoglu and Restrepo (2022),
Autor (2015), Manning (2003), Susskind (2017), Sachs and Kotlikoff (2012), Moll, Rachel and Restrepo
(2022), Allen (2001), Clark (2005) and Piketty and Zucman (2014). Diamond and Mirrlees (1971) at 414
is a different work and stays.

New references (entries in the main.tex \refentry style; data verified on Crossref this session):

```latex
\refentry{Keynes, J. M. (1930). ``Economic Possibilities for our Grandchildren.'' \emph{The Nation and Athenaeum}, 11 and 18 October 1930. Reprinted in \emph{Essays in Persuasion}, Macmillan, 1931, pp. 358--373.}
\refentry{Korinek, A., and M. Juelfs (2022). ``Preparing for the (Non-Existent?) Future of Work.'' NBER Working Paper 30172. \url{https://doi.org/10.3386/w30172}.}
\refentry{Korinek, A., and L. Lockwood (2026). ``Public Finance in the Age of AI: A Primer.'' NBER Working Paper 34873. \url{https://doi.org/10.3386/w34873}.}
\refentry{Leontief, W. W. (1983). ``National Perspective: The Definition of Problems and Opportunities.'' In \emph{The Long-Term Impact of Technology on Employment and Unemployment: A National Academy of Engineering Symposium, June 30, 1983}, National Academy Press, pp. 3--7. \url{https://doi.org/10.17226/19470}.}
\refentry{Restrepo, P. (2025). ``We Won't be Missed: Work and Growth in the AGI World.'' NBER Working Paper 34423. \url{https://doi.org/10.3386/w34423}.}
\refentry{Trammell, P., and A. Korinek (2026). ``Economic Growth under Transformative AI.'' \emph{Annual Review of Economics} 18: 589--611. \url{https://doi.org/10.1146/annurev-economics-051624-061002}.}
```

## 6. The two asides (exact text, decided by Stella)

- **After eq. (17) in §6, after F6's lines:** Keynes (1930) looked forward to honoring ``the lilies
  of the field who toil not, neither do they spin.'' Equation~\eqref{eq:17} adds two conditions:
  the field must be large enough, and its rent must reach the lilies.
- **In §10, after the rent-tax sentence:** Leontief (1983) compared the future of human labor to
  that of horses after the tractor. The comparison fails in one respect: people, unlike horses, can
  vote for a rent dividend.

## 7. Other decisions to respect (STATE 2026-11-05)

- The owner optimizes: rho = 1/beta − 1. Support is a commitment in the owner's budget.
- The smaller stated economy is the one Section 3 states. Its generality (several inputs, a choice
  among methods, networks) is in Appendix B.
- Proofs of Propositions 1–3 are in the text; the rest are in Appendix A. Assumptions are numbered.
- After each result there is a remark on what it does not depend on.
- Results come first, then the example (§7), then AI (§10).
- Measurement (§8) comes before History (§9).
- The design's other decisions (synthesis §4) are taken as recommended:
  - durable machines are in the stated economy, with the flow benchmark at (rho, delta) = (0, 1);
  - H = {gamma_M = 0} ∪ R;
  - the rent tax is on rental value;
  - the government may provide the basket (sigma = 0);
  - Table 2's third target is relabeled;
  - semantic labels, with the Open 12(j) renames, keeping a, lambda, b, v, V_m, Y and s;
  - workers neither save nor borrow;
  - the new results Corollary 1(i)'s rate, Lemma A.1 and Proposition B.1 are included.
- The design's draft introduction is SUPERSEDED by narrative_draft.md v2. Do not fold the survey's
  "precedence paragraphs" into the introduction.

## 8. What each part delivers

- SP/build/parts/<NN>_<name>.tex: the LaTeX fragment, with provenance comments.
- SP/build/parts/<NN>_<name>.notes.md, which lists:
  - (a) labels defined and labels referenced;
  - (b) every edit to the authors' text, with old and new;
  - (c) every sentence of the authors' text dropped, with its line;
  - (d) the decisions for Stella, one line each, answerable in one word;
  - (e) citations used, and whether each is in main.tex's references or §5's new list;
  - (f) anything you could not do, and why.
- Use SP/build/work/<NN>/ for scratch. Run Python with -B.
