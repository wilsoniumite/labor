# Assembly of the rewrite: "Pinning the Wage to Scarcity and Technology"

Build step: assembly, 2026-11-05. SP = `/tmp/claude-0/-home-user-labor/904c7da5-c8e1-5390-ac85-b6fa3b59f016/scratchpad`.

| Output | Path |
|---|---|
| The assembled paper | `SP/build/assembled/main_rewrite.tex` (2,227 lines) |
| Its PDF | `SP/build/assembled/main_rewrite.pdf`: **50 pages** (the baseline is 41) |
| Figures (a copy of `paper/figures`, `cp -r`) | `SP/build/assembled/figures/` |
| Assembly script (python3 -B) | `SP/build/work/assembly/assemble.py`, with `label_fixes.json` |
| Checks | `SP/build/work/assembly/verify_assembly.py`, `dup_scan.py`, `refs_report.json`, `latexmk.out` |

**Result.**
- `latexmk -pdf -interaction=nonstopmode main_rewrite.tex` exits 0 with 50 pages.
- No LaTeX errors, no undefined references or citations, no multiply defined labels, no overfull lines.
- All 8 figure files are found and embedded.
- The log's only box warnings are two underfull lines in one reference entry (Section 4 below).
- `checks/lint_tex_structure.py` is **ALL GREEN**: 113 labels, 274 refs, 115 environments, 8 figures.

**What the assembly changed and what it did not.**
- No sentence's wording was changed. The only differences between the assembled body and the 18 parts are:
  - the part-separator comment lines;
  - four narrowed `\ref` targets, each with a comment line before it (Section 3 below);
  - the reference list;
  - one `\sloppy` inside the reference group.
- `verify_assembly.py` confirms this: with the four fixes undone, the 18 segments are byte-identical to `SP/build/parts/*.tex`.
- Every reference entry is either main.tex's line, unchanged, or one of the six entries of brief §5, as given.
- Nothing under `/home/user/labor` was written: `git status` is clean, and Python ran with `-B`.

**Regression check.** The PDF text equals the part 13-17 integration build (`work/13_17/integ.pdf`, the same 18 parts without references) except in two places:
- the four narrowed pointers, whose paragraphs reflow;
- the added reference list.

## 1. Order of the parts

| # | Part | Contents | Printed as (first page) | Notes file |
|---|---|---|---|---|
| 1 | `00_front.tex` | preamble (main.tex L1-40, L35-38 replaced by synthesis §2.0), title, authors, abstract (unchanged), keywords, JEL | p. 1 | `00_03.notes.md` |
| 2 | `01_intro.tex` | Introduction (`sec:intro`) | §1, p. 1 | `00_03.notes.md` |
| 3 | `02_description.tex` | Description of the economy (`sec:description`) | §2, p. 3 | `00_03.notes.md` |
| 4 | `03_definition.tex` | Definition of equilibrium (`sec:economy`), Table 1 | §3, p. 4 | `00_03.notes.md` |
| 5 | `04_equilibrium.tex` | Equilibrium (`sec:equilibrium`), Figures 1-2 | §4, p. 12 | `04_equilibrium.notes.md` |
| 6 | `05_purchasing.tex` | Purchasing power and income (`sec:purchasing`) | §5, p. 18 | `05_06.notes.md` |
| 7 | `06_rent.tex` | Distribution: rent taxation and a uniform transfer (`sec:rent`) | §6, p. 21 | `05_06.notes.md` |
| 8 | `07_example.tex` | A numerical economy and an automation path (`sec:example`), Table 2, Figure 3 | §7, p. 23 | `07_08.notes.md` |
| 9 | `08_measurement.tex` | Measurement (`sec:measurement`), Figures 4-6 | §8, p. 25 | `07_08.notes.md` |
| 10 | `09_history.tex` | History and stabilizers (`sec:history`), Figure 7 | §9, p. 27 | `09_10.notes.md` |
| 11 | `10_ai.tex` | Artificial intelligence and conclusion (`sec:ai`), with Future Work | §10, p. 30 | `09_10.notes.md` |
| 12 | `11_appA.tex` | appendix switch; Proofs (`app:proofs`) | App. A, p. 32 | `11_12.notes.md` |
| 13 | `12_appB.tex` | Extensions of the economy (`app:extensions`), Table B.1 | App. B, p. 37 | `11_12.notes.md` |
| 14 | `13_appC.tex` | Expenditure shares under substitution (`app:C`) | App. C, p. 41 | `13_17.notes.md` |
| 15 | `14_appD.tex` | Fiscal transition while labor remains employed (`app:D`), Table D.1, Figure D.1 | App. D, p. 42 | `13_17.notes.md` |
| 16 | `15_appE.tex` | Human-required tasks (`app:E`) | App. E, p. 45 | `13_17.notes.md` |
| 17 | `16_appF.tex` | The financing and production accounts (`app:F`) | App. F, p. 47 | `13_17.notes.md` |
| 18 | `17_back.tex` | data, notation and checks note; declaration on generative AI | pp. 47-48 | `13_17.notes.md` |
| 19 | (assembly) | References (main.tex L919-981, reconciled), then main.tex L983 `\end{document}` | pp. 48-50 | this file |

**Printed numbers.** Old labels kept their names, so equations, figures and tables now print with new numbers. The notes files and decisions cite them by label or by main.tex's number. The map:

| Label | Prints | Label | Prints | Label | Prints | Label | Prints |
|---|---|---|---|---|---|---|---|
| eq:1 | (1) | eq:5 | (13) | eq:12 | (23) | eq:21 | (18) |
| eq:unitcost | (2) | eq:6 | (14) | eq:13 | (24) | eq:22 | (19) |
| eq:3 | (3) | eq:9 | (15) | eq:14 | (25) | eq:23 | (20) |
| eq:4 | (4) | eq:10 | (16) | eq:income | (26) | eq:24 | (21) |
| eq:tildem | (5) | eq:11 | (17) | eq:15 | (27) | eq:25 | (22) |
| eq:utility | (6) | eq:ownerseq | (10) | eq:16 | (28) | eq:2 | (B.1) |
| eq:7 | (7) | eq:ownerbudget | (11) | eq:17 | (29) | eq:assignment | (B.2) |
| eq:budget | (8) | eq:govbudget | (12) | eq:26 | (C.1) | eq:19 | (B.3) |
| eq:8 | (9) | eq:27 | (D.1) | eq:28 | (D.2) | eq:20 | (B.4) |

| Label | Prints | Label | Prints |
|---|---|---|---|
| fig:1, fig:2, fig:3 | Figures 1, 2, 3 | tab:notation, tab:instance | Tables 1, 2 |
| fig:5, fig:6, fig:7 | Figures 4, 5, 6 | tab:departures, tab:D.1 | Tables B.1, D.1 |
| fig:4 (eras) | Figure 7 | thm:1; lem:prices, lem:ceiling | Theorem 1; Lemmas 1, 2 |
| fig:8 | Figure D.1 | prop:1-prop:6; cor:statics, cor:vanishing, cor:fiscal | Propositions 1-6; Corollaries 1, 2, 3 |
| ass:tasks ... ass:owner | Assumptions 1-5 | def:equilibrium, def:margins, def:automation | Definitions 1, 2, 3 |
| lem:owner | Lemma A.1 | ass:network, def:network, prop:network | Assumption, Definition, Proposition B.1 |
| prop:E.1 | Proposition E.1 | | |

## 2. References

**Method.**
- The base is main.tex's `\section*{References}` block (L919-981, 59 entries).
- For each entry, `assemble.py` searches the assembled text with comments stripped for its surnames and year as printed:
  - "Author (year)", "(Author year)" and "Author's (year)";
  - author lists with or without the serial comma;
  - every order of the names, and "et al.". There are no "et al." forms in the text.
- Every match context was read by hand (`refs_report.json`).
- Every year mention not covered by an entry was listed and checked by hand. All are data years or dates, except the one under "No entry" below.

**Kept: 36 entries, verbatim.**

| Entry | Cited in (build part) |
|---|---|
| Acemoglu and Restrepo (2018) | §1 (twice), §2, §5 |
| Acemoglu and Restrepo (2026) | §3 wedge remark; §9.2 (L536) |
| Aghion, Jones, and Jones (2019) | App. E |
| Arnott and Stiglitz (1979) | §6 |
| Arrow (1951) | App. A (Proposition 6's proof) |
| Autor and Dorn (2013); Autor, Levy, and Murnane (2003) | §9.1 |
| Baumol (1967) | App. E |
| Bouscasse, Nakamura, and Steinsson (2025) | §9.1 |
| Card, Cardoso, Heining, and Kline (2018) | §3 wedge remark |
| Caselli and Manning (2019) | §5 |
| Diamond and Mirrlees (1971) | App. A |
| George (1879) | §1, §6 (also named without a year in §10, L550) |
| Grossman and Rossi-Hansberg (2008) | §1 |
| Gruber (1997); Kugler and Kugler (2009); Saez, Schoefer, and Seim (2019) | App. D.2 |
| Hoynes and Rothstein (2019); Jones and Marinescu (2022) | Table D.1 |
| Karabarbounis and Neiman (2014); Rognlie (2015); Knoll, Schularick, and Steger (2017) | §5.2 |
| Keynes (1936) | §10 |
| Korinek and Stiglitz (2019) | §1, §4.2 |
| Korinek and Suh (2024) | §1 |
| Leontief (1936); Sraffa (1960) | §2, §3.2, §5 |
| Lewis (1954); Marx (1867); Polanyi (1944) | §4.2 (L300) |
| Mas and Pallais (2019) | §3.3 |
| Romer (1990) | App. B.5 |
| Rosen (1981) | App. E |
| Samuels and Senel (2026) | App. F; the data note |
| Shapiro and Stiglitz (1984) | §3 wedge remark |
| Zeira (1998) | §1, §2 |

**Removed: 23 entries, cited nowhere in the assembled text.**
- The 19 that brief §5 drops with the survey:
  - Acemoglu and Autor (2011); Acemoglu and Restrepo (2022); Allen (2001); Autor (2015); Clark (2005); Diamond (1982);
  - Hagedorn and Manovskii (2008); Hall (2005); Ljungqvist and Sargent (2017); Manning (2003); Moll, Rachel, and Restrepo (2022);
  - Mortensen and Pissarides (1994); Piketty and Zucman (2014); Pissarides (2000); Sachs and Kotlikoff (2012);
  - Samuelson (1966); Shimer (2005); Susskind (2017); Uzawa (1961).
- Four more, each with a decision for Stella in Section 5:
  - **Crafts (2022)**: cited only in L471 S7, which part 09 cut (D63).
  - **Hémous and Olsen (2022)**: not placed; part 03 found no sentence at Definition 3 that takes the direction of technical change as given (D10).
  - **Ricardo (1817)** and **Malthus (1798)**: named without years in L469, kept verbatim. Brief §5: "They drop from the references unless cited" (D64).

**Added: the six entries of brief §5**, verbatim, in alphabetical order, each marked `% NEW (build brief §5)`:

| Entry | Placed | Cited in |
|---|---|---|
| Keynes (1930) | before Keynes (1936) | §1; §6 (the lilies aside) |
| Korinek and Juelfs (2022) | first of the Korinek entries | §1 |
| Korinek and Lockwood (2026) | after Korinek and Juelfs | §6, beside George (1879) |
| Leontief (1983) | after Leontief (1936) | §1; §10 (the horses aside) |
| Restrepo (2025) | between Polanyi and Rognlie | §4.1, after Proposition 1 and the loom |
| Trammell and Korinek (2026) | between Sraffa and Zeira | §3.6, the AI paragraph |

The final list has **42 entries**. Ordering follows main.tex's rule: first author, then a single author before coauthored works, then coauthors, then year. The script checks that the kept entries keep main.tex's relative order. Zeira (1998) stays last and keeps main.tex's `\par`.

**No entry.** The Figure 5 caption (main.tex L496-511, verbatim in §8) says "the Orshansky 1963 subsistence bundle". main.tex has no entry for it (STATE Open 12(k)). No entry was invented; see Problems.

## 3. Labels and cross-references

- **Every `\ref` and `\eqref` resolved on the first pass.** Each part referenced other parts' objects by the labels the defining parts use:
  - `sec:example`, not the design's `sec:instance`;
  - `app:D` and `app:D.1`-`app:D.5`, not `app:fiscal`;
  - `app:C`, `app:E`, `app:F`, `app:proofs`, `app:extensions`, `app:networks`, `lem:owner`;
  - `eq:2`, defined in B.1.
- **Lint.** ALL GREEN before and after the fixes below: 113 labels, all unique, and 274 references.
- **Narrowed pointers.** Four references to Appendix B as a whole were pointed at the subsection labels part 12 defined. Part 05 ("can be narrowed if B.6 gets a label") and part 12 ("let the assembler narrow") asked for this. Only `\ref` targets changed; the words did not. Each carries a `% assembly (label fix)` comment line.

| Part | Where | Old target | New target | Prints |
|---|---|---|---|---|
| 05 | §5.1, L351 last sentence, "... gives the task-level representation of these costs." | `app:extensions` | `app:tasklevel` | Appendix B -> Appendix B.6 |
| 06 | §6, L223-225 S6, "Several non-produced inputs enter as **B r** in ..." | `app:extensions` | `app:inputs` | Appendix B -> Appendix B.2 |
| 06 | §6, remark after Corollary 3, "... which compares rental values (...)" | `app:extensions` | `app:inputs` | Appendix B -> Appendix B.2 |
| 03 | §3.6, AI paragraph, "... data that law protects earn an institutional rent (...)" | `app:extensions` | `app:ideas` | Appendix B -> Appendix B.5 |

- **Left as delivered.** Section 3's wedge remark still points to `sec:history` (Section 9). The wedge itself is in 9.2. Part 09 put that change to Stella (D76).
- **Unchanged pointers to Appendix B as a whole:** the roadmap (§1) and Table B.1's own row.

## 4. Compile

- **Command.** `cd SP/build/assembled && latexmk -pdf -interaction=nonstopmode main_rewrite.tex`, exit 0.
- **Result.** 50 pages and 0 errors.
- **References and figures.** No undefined references or citations, no multiply defined labels, and no `\includegraphics` file missing. All 8 figures are embedded:
  - `fig_schedule`, `fig_replacement_closure`, `fig_labor_market_clearing`;
  - `fig_deflator_fork`, `fig_kappa_measurement`, `fig_consumption_financing_and_human_effort`;
  - `fig_eras_workers`, `fig_fourway`.
- **One typesetting fix, no text change.**
  - The first compile had one overfull line, 29.5pt, in the new Trammell and Korinek entry. Its DOI can break only after "10.1146/".
  - `\emergencystretch` alone did not help.
  - `\sloppy`, local to the reference group, fixes it and changes no other entry: pages 1-48 are text-identical, and only that entry's lines differ.
  - The cost is two loose lines in that entry, which the log reports as underfull (badness 5756 and 1237).
  - The alternative, url.sty's hyphen breaks set locally, left no box warnings. It also re-broke the Hoynes and Rothstein DOI at a hyphen and moved an entry across a page. It was not used (D110).
- **Pre-existing.** The Appendix D title hyphenates "em-ployed" and the declaration's heading "technolo-gies", as in the baseline.

## 5. Decisions for Stella

Each is one line, answerable in one word; the part's suggested answer is in parentheses. Duplicates across notes files are merged, and line numbers are main.tex's. D30, D109 and D110 come from this assembly step.

**Front matter and Sections 1-3 (part 00-03)**
1. Keep main.tex's abstract unchanged for now (the design's sketch, synthesis §1.2, is the alternative)? (yes/no)
2. §3: keep the authors' wording where the design only reworded it (L140-142, L203, L207, L223, L249, L251, L540)? (yes)
3. §3: keep the two passages the design left out, L153 S2-S3 (reservation wage) and L170 S7-S8 (interior margin with H nonempty)? (yes)
4. Drop five sentences that the new text says elsewhere (L149 S2, L219 S2, L249 S5, L268 S1, L274 S1)? (yes)
5. L203: the full stop becomes a colon before display (4)? (yes)
6. The parents example (L268 S3) and "stands for whoever sustains a person outside paid work" print in both §2 and §3.4: drop the repeats from §3.4? (yes/no)
7. L74's grid-connection sentence prints in §1 and again in §3.1: keep both? (yes/no)
8. Keep "Table 1 collects the notation." after the primitives sentence? (yes)
9. Cut ", not a capability" from the design's "A reservation is a rule, not a capability" (rule 2)? (yes)
10. Hémous and Olsen (2022) are not placed and their entry is removed: agree? (yes)
11. Keep "We return to Keynes's question, leave the old Adam out, and ask what prices do." despite rule 2's triad flag? (yes/no)
12. Rewrite main.tex's header comments (L1-11, kept verbatim) when the rewrite replaces main.tex? (yes)

**Section 4 (part 04)**

13. Theorem 1's remark: also disclose that without the user-cost clause the instance has a second configuration (return 0.192, owner consuming nothing, land partly idle)? (yes/no)
14. Proposition 3: the authors' "work is optimal ... exactly when" over the design's "prefers work"? (yes)
15. L253: the authors' "full machine-service chain" over the design's "machine chain"? (yes)
16. L257: only "When ρ = 0," added, and the authors' second sentence kept, over the design's rewording? (yes)
17. L245 S4: "and the selected recipes" gives way to a pointer to Theorem 1, as the design does? (yes)
18. Proposition 2: restore "Holding the other ... fixed" (as "price coefficients"), which the design dropped? (yes)
19. Proposition 1's proof (ii): the authors' L627 verbatim, with γ_L, over the design's γ_L = 1 form? (yes)
20. L294-300 verbatim, without the design's insertion of L124's Lewis sentence? (yes)
21. L155-157 (the "replacement value" the loom uses) placed before Proposition 1? (yes)
22. L136's proof pointer, edited, as Section 4's opening sentence? (yes)
23. L322's last sentence with two pointers, over the design's "funding is necessary and sufficient"? (yes)
24. Lemma 2: the new remark on what it does not depend on? (yes)
25. Theorem 1: "sets of tasks and of workers of measure zero", to cover the workers indifferent between work and exit (math check C4, condition 3)? (yes/no)
26. Proposition 2's remark: "any production network of Appendix B.1", the scope after F1? (yes)
27. Restrepo (2025) after Proposition 1 and the loom, leading into Proposition 2? (yes)
28. Korinek and Stiglitz (2019) at the end of the dependence paragraph (L298)? (yes)
29. Figure 1's float in Section 4, as the brief says, though Section 3 cites it first? (yes)
30. (assembly) F5's sentence prints in §3 after Definition 1: drop it from Theorem 1's remark, keeping "Its uniqueness rests on the clause ..."? (yes/no)

**Sections 5-6 (part 05-06)**

31. Drop L330 (L88 now opens Section 5 and says the same)? (yes)
32. L351 S2 read on the price basis, in the design's words? (yes)
33. L353: ", valued at the user cost" added? (yes)
34. Rename \bar L_i to \bar\lambda_i throughout ((13), L353, Proposition B.1, B.6, Appendix C's \bar\lambda_0), as the design recommends? (yes)
35. Keep L374's second sentence, though the remark after Corollary 2 says the same? (yes)
36. Corollary 2's remark: the general in-work bound F(log[1+θP_s/(P_s+d+g_e)]), not only d = g_e = 0? (yes)
37. Proposition 5: state the converse "when N_a > 0, only if ρ = 0" (Appendix A proves it)? (yes)
38. L386: "When ρ = 0," added before "at given N_a and T"? (yes)
39. L393 S1: "When ρ = 0," in place of "in this two-factor flow benchmark", with the design's return-on-machines clause? (yes)
40. L393 S3: "this benchmark" -> "the flow benchmark"? (yes)
41. The factor-share sentence: keep the authors' "---" where the design had a comma? (yes)
42. §5.2's title: keep "Factor income while labor remains employed" (design: "Factor income")? (yes)
43. §6: keep all of L223-225 after its first sentence (the design showed only the two definitions)? (yes)
44. (16) as public provision: "R = rT > 0" and σ = 0 in place of "Funding exactly one basket per person requires d = P_s, hence"? (yes)
45. Keep L417 S1, L421's last sentence and L423 S1-4 in the authors' words, where the design reworded or cut them? (yes)
46. Keep "per person" in Proposition 6(iii) and Corollary 3 (design: "per worker")? (yes)
47. Proposition 6(i): keep L402's two sentences after the new sentence on the owner's choice (the design merged them)? (yes)
48. Corollary 3(i) and L434: the authors' words with only the math fixes (the design reworded both)? (yes)
49. Accept the two rule-2 edits to the design's remark after Corollary 3 ("not about an equilibrium", "rather than physical quantities" removed)? (yes)
50. F6's several-input line, stated for ρ = 0 with every input that earns a positive rent fully used? (yes)
51. Keep L268 S5, "The parents (Section 3.4) may themselves finance that support from wages.", in §6 before L437 S2, which says it generally? (yes)
52. L439: "Appendix A proves the corollary, and Appendices D.2 and D.3 develop ..."? (yes)
53. L334 S3-4 (the barred coefficients) replaced by the human chain of the remark after Proposition 4 and of B.1? (yes)

**Sections 7-8 (part 07-08)**

54. Figure 3's caption: n_D/N -> N_D/N, as in Table 1 and (24) [printed (21)]? (yes)
55. Regenerate Figure 3 so its legend no longer says "baseline (Appendix B)" (`code/fig_labor_market_clearing.py`, line 62)? (yes)
56. Table 2's caption: add "(ρ to two decimal places)", since the calibrated 0.093 prints as 0.09? (yes)
57. The new sentence "In the instance, H is empty (x_H = 1), every instrument is zero, and the owner provides support."? (keep/cut)
58. L324 S3-4: in §7 with "The participation response of Corollary 1(ii)", or verbatim after Corollary 1 in §4? (here/there)
59. The design's "draws this market" -> "draws the labor market"? (yes)
60. The curvature sentence placed after the "both automation channels" sentence it qualifies? (yes)
61. Keep L747 S7 (its pointer now Proposition 5), which the design drops? (keep/cut)

**Sections 9-10 (part 09-10)**

62. 9.1 cuts Section 8's prose to 65 percent (613 to 401 words) by whole sentences (see Section 6 of this file): accept? (yes)
63. Crafts (2022), cited only in the cut L471 S7, is removed from the references: agree, rather than restoring the sentence? (yes)
64. Ricardo (1817) and Malthus (1798), named without years in L469 (verbatim), are removed from the references: restore their entries? (yes/no)
65. L473 S7 as a counterfactual ("If ... both held contestable margins ..., ... would apply ... would cancel"), over the design's "each held an interior margin"? (yes)
66. L532 S2: "the median worker" -> "most workers" (Appendix E's words), over the design's "; most workers can still be exposed"? (yes)
67. The new sentence after L532 S3, "Such a reservation is a policy (Section 3.5), and Definition 3 does not count lifting it as automation."? (keep/cut)
68. Section 10 opens with L540 S3-S5, with "(Definition 3)" after "Either change"? (yes)
69. L540 S6-S7 left out, since Section 3's AI paragraph restates them? (yes)
70. The monetary-policy passage keeps L553 S7 (the low-interest-rate question): use S4, "It may also have implications for monetary policy.", instead? (yes/no)
71. The sovereign-fund passage keeps L557 S7 (owning part of the world's scarce-resource base): use S5, "Sovereign wealth funds may provide another instrument.", instead? (yes/no)
72. Future Work otherwise keeps L553 S1-S3, L555, L557 S1-S4 and L559 whole (372 of 456 words): cut further? (yes/no)
73. L553's "The static model": change "static" to "stationary"? (yes/no)
74. L542 S2 states that participation tends to zero without Corollary 2's condition g_w ≤ g_e: add a pointer to Corollary 2? (yes/no)
75. The design's Uzawa (1961) Future Work sentence is not added, since brief §5 drops Uzawa: agree? (yes)
76. Section 3's wedge remark points to Section 9 (`sec:history`), but the wedge is in 9.2: point it to `sec:stabilizers`? (yes/no)

**Appendices A-B (part 11-12)**

77. Lemma A.1(a) in F4's wording (at β = 1, only constant plans must rent out all land)? (yes)
78. The remark after Lemma A.1: keep F5's sentence there too, with its reason, though Sections 3 and 4 print it? (yes/no)
79. Theorem 1's proof built on the authors' Lemma B.1 proof (L729-740), with "provider" -> "owner"? (yes)
80. Theorem 1's proof names the user cost of Definition 1(i) in the zero-rent step (F5)? (yes)
81. Corollary 3's proof: drop "also" from "is also necessary and sufficient"? (yes)
82. Proposition 6's proof: "The taxed stock is fixed by assumption" -> the owner's choice (Lemma A.1(a))? (yes)
83. Proposition 5's proof: prove F3's converse in full (no equilibrium with r > 0 has X = 0 or w = 0)? (yes)
84. Definition B.1: keep operating inputs, crediting the owner with the machine-hour's price net of them (math check C1), or drop operating inputs? (keep/drop)
85. Proposition B.1(e): in a network, equality in (15) [printed (27)] forces ρ = 0 only when wN_a p_K X > 0? (yes)
86. B.1: port the authors' general cost recursion (L199-202 with (2), L203 without S4, L221)? (yes)
87. B.1: leave out L213 S2 (spectral radius), which Definition B.1 states as a condition? (yes)
88. B.2: add the return on machines to L757's several-input identity? (yes)
89. B.3: the authors' trade sentences verbatim (the brief), or the inventory's unit-cost wording R3? (verbatim/R3)
90. B.3: rename the machine-type index ℓ, which Table 1 uses for the land rented out? (yes/no)
91. B.2-B.4: keep the authors' "active (contestable) margin" where B.6 takes the design's "interior margin"? (keep/change)
92. B.4's title "Worker types" (the brief) over the authors' lead "Heterogeneous workers"? (yes)
93. B.4: "(Figure 7)" added after "The eras figure"? (yes)
94. B.5: the income-accounting pointer to Section 5.2? (yes)
95. Appendix B opens with L570's first sentence and a pointer to Table B.1? (yes)
96. The remarks after Lemma A.1 and Proposition B.1, which the design lacks? (yes)
97. Appendix A in main-text order (Corollary 1 before Proposition 4, unlike the design)? (yes)
98. The two local `\emergencystretch` settings (Proposition 4's proof; B.6) that avoid overfull lines without text change? (yes)
99. A.4's timing paragraph (L667-675) left out, its content now Section 3's user cost and (21) [printed (18)]? (yes)

**Appendices C-F and back matter (part 13-17)**

100. Appendix D's title: shorten the authors' "Fiscal transition while labor remains employed" to the brief's "Fiscal transition"? (yes/no)
101. D.2: trim the added Section 2.7 pair to its first sentence, without the run-in "Payroll incidence:" (its second repeats D.2's own)? (yes/no)
102. Appendix C: rename the CES elasticity σ, which shares its letter with Table 1's support indicator σ? (yes/no)
103. D.3 and E: rename the basket quantities g_s, h_s, n_s to z_g, z_h, z_H (g_s reads like a payment beside g_w, g_e)? (yes/no)
104. Appendix C: keep the run-in head "A conditional expenditure comparison." under the new title? (yes/no)
105. Appendix C's opening: keep the clause after the colon, taken from the design's Table B.1 row? (yes/no)
106. D.1: add "with τ_w = d = 0" to the utility comparison, since Definition 1 now admits every instrument at once? (yes/no)
107. Appendix F: "valued at the user cost" in place of the design's undefined "on the price basis"? (yes)
108. D.5's index D and Appendix A's D(x) in Lemma 2's proof share a letter: rename one? (yes/no)

**Assembly (this step)**

109. Keep the four narrowed pointers (Appendix B -> B.6 at L351; B.2 at L223-225 S6 and after Corollary 3; B.5 in §3.6's AI paragraph)? (yes)
110. References: keep the local `\sloppy` that keeps the new Trammell and Korinek DOI inside the margin, at the cost of two loose lines in that entry? (yes)

## 6. Edits to the authors' text and dropped sentences, by part

Line numbers are main.tex's; S = sentence. The notes files give each edit's reason and full old and new text; the provenance comment before each paragraph of the .tex repeats it. The design's own drafts (NEW text) are not the authors' text; edits to them are listed in the notes files.

### Part 00-03: front matter and Sections 1-3

**Edits**
- L35-38, the theorem environments -> design synthesis §2.0's block (brief §3).
- L70: `\label{sec:1}` -> `\label{sec:intro}`.
- L153 S3: `Section~\ref{sec:4}` -> `Section~\ref{sec:participation}`.
- L203 S4: the final full stop -> a colon, introducing display (4) (D5).
- Display (3), under L207: the authors' p = Ap + λw + br, p = (I−A)^{-1}(...) -> the design's four-good system with A_ρ, same label `eq:3`. L207's sentence is verbatim.
- Display (4): λ̃ = (I−A)^{-1}λ, b̃ = (I−A)^{-1}b -> p = wλ̃ + rb̃ with A_ρ and bold I, same label `eq:4`.
- Display (7): P_s = z^T p = Σ z_i p_i -> P_s = p + hr, same label.
- Display (8): ", \qquad \chi\ge0." -> "." (χ ≥ 0 is in Assumption 4), same label.

**The authors' wording restored over the design's rewording** (not edits): L140-147, L203, L207, L223 S1, L249 S2/S4, L251 S3, L540 S1-S2. L153 S2-S3 and L170 S7-S8 are also restored, though the design left them out (D2, D3).

**Dropped**
- L90 S2-S3, "Pricing the household's living basket ..." and "With support maintained ..." (STATE: said elsewhere).
- L92-96, the old roadmap (replaced by a new one).
- Section 2, the survey (brief; design §1.4):
  - L100 S1-S2; L104 S1-S5; L108 S1-S2; L110 S1-S3; L112 S1;
  - L116 S1, S3, S4. Elsewhere: S2 is adapted in §1, S5 is the wedge remark, S6-S7 are in B.3;
  - L120 S1-S3; L124 S1-S9;
  - L128 S1's second clause, S2, S3, S4, S6. Elsewhere: S1's first clause is in §4, S5 in §5;
  - L132 S1, S3, S4. Elsewhere: S2 is in §5.2, S5-S6 in D.2.
- L136 S1, "The model connects task assignment, production costs, and participation through a common price system."
- L149 S2, "The assignment condition compares labor with this rental; ..." (said by L229 in §4).
- L163-167 S3, "Where labor holds at least one machine-contestable task, ..." (false at the corner, Open 12i).
- L165-167 S4, "If labor holds only tasks in H, ..." (said by Figure 1's caption and Proposition 1).
- L205 S1-S4, the flow-benchmark sentences (cut by the design; durable machines are in the stated economy).
- L213 S3, "Define the total requirements, including all intermediate rounds, by".
- L219 S2, "The tilde distinguishes the full production chain ...".
- L249 S1, S3, the bold definitions of the two channels (replaced by Definition 3).
- L249 S5, "Software developers illustrate how the two channels can meet: ..." (said by L540 S2).
- L268 S1, "A person who declines paid work still needs somewhere to live, ..." (said by L76).
- L274 S1, "The production network therefore prices both ..." (said by L86 S2).
- L274 S2's first clause, "Housing services include their site costs".

**Restated by the design's new text** (content changed):
- L74 S2, S4-S5 (in §3.1; L74 is whole in §1);
- L149 S1, S3; L153 S1, S4, S5; L157 S3; L159-160; L161; L161-163 S2; L167-169 S5;
- L199 S3; L213 S1; L219 S3-S4; L270-272; L276 S1-S3; L540 S6-S7.

### Part 04: Section 4

**Edits**
1. L136 S2: "... are collected in Appendix~\ref{app:A.2}." -> "... are given in the text; the other proofs are collected in Appendix~\ref{app:proofs}." (D22).
2. L627, last sentence: `Appendix~\ref{app:B}` -> `Section~\ref{sec:example}`.
3. L242: "Holding the other total requirements fixed" -> "Holding the other price coefficients fixed" (D18).
4. L631: cross-references to Proposition 1 and Lemma 1(i) added, plus the design's clause "Since p_m > 0 and r b̃_m > 0, the feedback term is positive, and solving gives (5)." The display is verbatim.
5. L251 S1: "either channel" -> "either channel (Definition~\ref{def:automation})".
6. L257 S1: "The service price ..." -> "When ρ = 0, the service price ..." (D16).
7. L296 S3: `Appendix~\ref{app:B}` -> `Section~\ref{sec:example}`.
8. L128, the Korinek and Stiglitz clause: semicolon to full stop (brief §5).
9. L322 S3: "Appendix~\ref{app:B} constructs the household budgets and proves ..." -> "Section~\ref{sec:economy} constructs the household budgets, and Theorem~\ref{thm:1} proves ..." (D23).
10. (24), L703-707: n_D, n_S -> N_D, N_S (Table 1).
11. Proposition 1 (L186-193), as the design restates it:
    - (i) gains the boundary and corner inequalities;
    - (ii) "the margin" -> "an interior margin";
    - (iii) is removed.
12. Proposition 1's proof: (i) is replaced by the design's proof (Open 12i); (ii) is verbatim (D19).
13. Proposition 2 (L231-243): its hypotheses become conclusions ("In every equilibrium with an interior margin and r > 0, the feedback term ... is positive and (5)"), and (5) ends in a comma.
14. L245 S2-S4, read on the price basis:
    - S2 is restated (γ(x*)λ̃_m = wλ̃_m/p_m; labor's share only when ρ = 0);
    - S3: "this share" -> "it";
    - S4: "and the selected recipes" -> "(Theorem~\ref{thm:1})" (D17).
15. Proposition 3 (L284-292): "Suppose P_s > 0 ... Under (8), work is optimal exactly when" -> "In every equilibrium with τ_w = d = g_w = g_e = 0, work is optimal for a worker with cost of work χ exactly when". (10) is joined to it, and (9) ends in a comma.
16. L640: S1-S2 verbatim. S3 and (18) are replaced by "For χ > 0, ∂s/∂P_s = e^χ − 1 > 0. Workers with w = s have measure zero ...".
17. L317 is restated as the paragraph before (11), with its assumptions now derived. (11) itself (L318-321) is verbatim.
18. L687 S1-S2 are restated as Lemma 2 and its gloss; the ceiling is no longer called "closed".
19. L708 S2 is restated so that N_S(x_c) is defined as the limit (math check C4).
20. Lemma B.1 (L719-726) is restated as Theorem 1: every equilibrium is interior, and funding is necessary and sufficient.
21. Corollary 1 is restated:
    - (i) collects L324 S1 and L729-734 and adds the equilibrium rate;
    - (ii) restates L743 (and L324 S2).

**The authors' wording restored over the design's re-voicing:**
- L253's "full machine-service chain";
- L257 S2;
- L294-300, verbatim, without the merge or the L124 insertion;
- L627 (ii); L631 and its display; L640 S1-S2;
- L285's "work is optimal"; L242's "Holding the other ... fixed".

**Dropped**
- L136 S1 (as in part 03).
- L192, Proposition 1(iii), "A worker supplies the market hour only if its wage reaches the reservation value s."
- L627 (i), "At the boundary between human and machine assignment, continuity and cost minimization give w/γ_L(x*) = p_m/γ_M(x*)." (false at a corner).
- L627, "(iii) is the participation condition."
- L232 S1-2, "At an active contestable margin with r > 0, suppose ... imply" (restated, item 13).
- L245 S2, "At the margin, γ(x*)λ̃_m is the labor share of machine-service cost." (restated, item 14).
- L268 S1 (as in part 03).
- L285, "Suppose P_s > 0 and the supported basket remains available in both states." and "Under (8),".
- L304 S3, "Aggregating Section~\ref{sec:4}'s choice gives employed hours".
- L308, both sentences ("In the flow benchmark, the production network prices the basket ..."; "With durable machines, P_s also pays interest ...") (restated as Lemma 1(i), (iii)).
- L317, all three sentences, "For a transparent equilibrium, suppose ..." (restated, item 17).
- L640 S3 with (18), "Holding the supported basket and preferences fixed, ... ds/dr = (e^χ−1)dP_s/dr."
- L687 S1-2 (restated, item 18); L708 S2 (restated, item 19).
- L710-717, all but the last sentence: the three-row system and the two coefficient sets (replaced by §3's (3), (4) and Lemma 1).
- L717, last sentence, "Structures and maintenance could enter the space-service row through their own input requirements." (no home in the design).
- L719-726, Lemma B.1 (restated as Theorem 1); L743, three sentences (restated as Corollary 1(ii)).
- Headings: L227 "Closing the replacement price", L247 "Two margins of automation", L266 "The outside option: pricing exit", L302 "Replacement meets participation".

### Part 05-06: Sections 5 and 6

**Edits, Section 5**
1. L334 S1: "the total requirements in (4)" -> "the price coefficients in (4)".
2. L90 S1: "Acemoglu and Restrepo with" -> "Acemoglu and Restrepo (2018) with"; moved to stand after Proposition 4.
3. L128, the Caselli and Manning sentence: `Section~\ref{sec:6}` -> `Proposition~\ref{prop:4}`.
4. (13), L343-347, in the remark: \bar L_i -> \bar\lambda_i (D34).
5. L351 S2: "An hour's wage buys w/r units of the non-produced service; a unit of output embodies b̃_i units." -> "..., and the price of a unit of output carries b̃_i units, the return on the machines in its chain included; when ρ = 0, b̃_i is the input the unit embodies." (D32)
6. L351, last sentence: `app:A.3` -> `app:extensions`, narrowed at assembly to `app:tasklevel`.
7. L353 S4: "... throughout those supply chains." -> "..., valued at the user cost." (D33)
8. L353, last sentence: \bar b_i/\bar L_i -> \bar b_i/\bar\lambda_i.
9. L374, last sentence: `Appendix~\ref{app:B}` -> `Section~\ref{sec:example}`.
10. L376, last sentence: `Section~\ref{sec:7}` -> `Section~\ref{sec:rent}`.
11. L386 S1: "At given N_a and T, ..." -> "When ρ = 0, at given N_a and T, ..." (D38).
12. L393 S1: "Ownership of the non-produced input receives the non-wage component of income in this two-factor flow benchmark." -> "When ρ = 0, ownership of the non-produced input receives the non-wage component of income; with a positive return the owner also receives the return on machines, which (income) counts." (D39)
13. L393 S3: "outside this benchmark" -> "outside the flow benchmark" (D40).
14. L132, the factor-share clause: "Factor shares:" -> "In the data,", and "; Piketty and Zucman 2014" dropped. The authors' "---" is kept.

**Edits, Section 6**

15. L223-225 S6: `app:A` -> `app:extensions`, narrowed at assembly to `app:inputs`.
16. L406, Proposition 6(iii): "remain wN_a + R" -> "remain wN_a + R + ρV_mX".
17. L417 S2: "with R > 0" -> "with R = rT > 0".
18. L417 S3: "Funding exactly one basket per person requires d = P_s, hence" -> "If the government provides the basket (σ = 0) from the rent tax alone, its budget (govbudget) requires" (D44).
19. L423 S2: `Section~\ref{sec:4}` -> `Section~\ref{sec:workers}`.
20. L428, Corollary 3(i): "while R/I -> 1." -> "while the non-wage share of income, (R+ρV_mX)/I, tends to one; when ρ = 0, R/I -> 1." The label "(i)" is added.
21. L434: "exactly when NB_s ≤ T, the physical feasibility condition" -> "exactly when N b̃_s ≤ T, which implies NB_s ≤ T, the physical feasibility condition ...; when ρ = 0, b̃_s = B_s and the two conditions coincide."
22. L268 S5, moved to §6: "The parents may ..." -> "The parents (Section~\ref{sec:owner}) may ...".
23. L439 S1: "Appendix~\ref{app:D} proves the corollary and develops ..." -> "Appendix~\ref{app:proofs} proves the corollary, and Appendices~\ref{app:D.2} and~\ref{app:D.3} develop ..." (D52).

**Dropped**
- L330, both sentences, "Equation (5) links technology to the wage relative to rent. What that wage buys also depends on ..." (D31).
- L90 S2-S3 (as in part 03).
- L132, the citation "Piketty and Zucman 2014".
- L334 S3-4, "Where the entire production chain can be performed by a human method, let \bar L_i ... The barred coefficients describe ..." (D53).
- L337-348, Proposition 4's statement sentences (replaced by the design's Proposition 4 and its remark):
  - "At positive wages and rents, every positively priced good ... satisfies";
  - "At an active contestable margin, (5) determines r/w.";
  - "A feasible human method with \bar b_i = 0 gives w/p_i ≥ 1/\bar L_i.";
  - "The price identity and bounds hold also at boundary task assignments ...".
- L356-363, the corollary's sentences (replaced by the design's Corollary 2):
  - "Along a sequence of equilibria with an active contestable margin ...";
  - "Wage purchasing power tends to zero for every good whose total non-produced input requirement stays bounded away from zero.";
  - "A persistent unavoidable direct requirement is sufficient.";
  - "A feasible human method with no non-produced input and uniformly bounded human hours preserves a positive lower bound ...";
  - "If B_s stays bounded away from zero, one basket remains funded ..., then".
- L381-385, Proposition 5's setup, "In the competitive flow economy with human hours and one non-produced input as the two primary factors, let N_a ≤ N ..." and (15) as an equality (replaced by (income) and the inequality (15)).
- L399, both sentences, "Let non-produced inputs supply fixed service endowments T_j ..." and "A tax at rate τ_R on pure ownership rents finances a uniform per-person transfer ..." (replaced by Proposition 6's first sentence).
- L430-433, "In a fully automated economy, λ̃ = 0. With r > 0 and B_s > 0, full rent capture yields coverage κ = T/(NB_s)." (replaced by the design's statement at given methods).

**Moved to Appendix A, not dropped:** L370-372, L389-391, L413-415, L646-652, L769-775.

### Part 07-08: Sections 7 and 8

**Edits**
1. L745 S1: the parameter list ("take N = 1, T = 0.01, ..., and χ uniform on [0,2.2]") -> "Table~\ref{tab:instance} lists the parameters and the shares they are set to match."
2. L745 S3: "the full-chain cost of consumption" -> "the cost of a basket at final tasks".
3. L745 S5: "provider's rent and interest" -> "owner's rent and interest".
4. L313, Figure 3's caption: `Appendix~\ref{app:B}` -> `Section~\ref{sec:example}`.
5. L313, Figure 3's caption: n_D/N -> N_D/N (D54).
6. L324 S4: "This participation response" -> "The participation response of Corollary~\ref{cor:statics}(ii)" (D58).
7. L747 S2: the design's clause from ", since ..." is added after "The conditions in (25) hold throughout".
8. L747 S3: joined to the design's "With λ = 0 the machine rental is p_m = πr at every margin, ..., and the equilibrium wage satisfies ...". "The" is lowercased; the bound is unchanged.
9. L747 S7: "as in the proof of Lemma~\ref{lem:B.1}" -> "as in Proposition~\ref{prop:5}" (D61).
10. Figure 3 (L310-315) moved from Section 5 to Section 7; its file, width and label are unchanged.
11. L475: `\label{sec:9}` -> `\label{sec:measurement}`. Section 8 is otherwise verbatim.

**Dropped**
- L324 S5, "Figure~\ref{fig:3} draws this market for the numerical economy of Appendix~\ref{app:B}." (replaced by the design's AI-framing sentence).
- L747 S6, "The provider's rent and interest fund the support throughout." (replaced by the design's funding sentence).

### Part 09-10: Sections 9 and 10

**Edits**
- L441: `\section{History as four configurations of the model}\label{sec:8}` -> `\subsection{...}\label{sec:configurations}` (now 9.1).
- L473 S7, as a conditional:
  - old: "Where the trained worker and the entrant both hold contestable margins against the same machine, Proposition~\ref{prop:1}(i) applies to each and the rental cancels:";
  - new: "If ... both held ..., ... would apply to each and the rental would cancel:" (D65).
- L530: `\section{Possible stabilizers}\label{sec:10}` -> `\subsection{...}\label{sec:stabilizers}` (now 9.2).
- L532 S2: "while leaving the median worker exposed." -> "while leaving most workers exposed." (D66).
- L538: label `sec:11` -> `sec:ai`.
- L540 S3: "Either change" -> "Either change (Definition~\ref{def:automation})".
- L540 S4: `Section~\ref{sec:6}` -> `Section~\ref{sec:purchasing}`.
- L552: the heading `\section{Future Work}\label{sec:12}` is dropped; Future Work is folded into Section 10.
- Moves and joins, with no words changed:
  - L326 moves to open 9.1;
  - L553 (cut) and L555 are joined into one paragraph;
  - L557 (cut) and L559 are joined into another.

**Dropped**
- L443 S4, "A joint determination of their wages and training decisions requires the extension described in Section~\ref{sec:5}."
- L471 S3, "It did so for the entrant first: the young mill hand or hand-loom weaver held the tasks engines were reaching one by one, ..."
- L471 S4, "The trained worker, the millwright, the engineer, the clerk, held tasks closed to engines; ..."
- L471 S7, "The escape was neither immediate nor smooth --- real wages grew slowly in the early decades ... (Crafts 2022)."
- L473 S2, "The entrant is the young clerk, cashier, or assembler whose routine tasks software and machines reached at similar cost: ..."
- L473 S3, "The trained worker, the developer, the physician, the engineer, held tasks computers could not: ..."
- L473 S5, "It may also reduce λ̃_m, the labor embodied in machine services."
- L473 S8, "The interior result connects these replacement costs to wage purchasing power."
- L553 S4, "It may also have implications for monetary policy."
- L553 S5, "When machine-made goods become cheaper while housing, energy, and other scarce necessities become more expensive, a single inflation rate can hide significant nuances."
- L553 S6, "Can one interest rate stabilize both sides of a divide?"
- L553 S8, "The relative-price structure developed here provides a starting point for these questions."
- L557 S5, "Sovereign wealth funds may provide another instrument."
- L557 S6, "A country with little land, energy, or mineral wealth of its own cannot tax rents earned elsewhere, but it can acquire claims on them."
- Left out of §10 because they are in §3: L540 S1-S2 (verbatim there) and L540 S6-S7 (restated there).

### Part 11-12: Appendices A and B

**Edits, Appendix A**
1. L561-566, the appendix switch: `\counterwithin{lemma}`, `{assumption}` and `{definition}` added (brief §3).
2. L568: `\section{The environment and supporting results}\label{app:A}` -> `\section{Proofs}\label{app:proofs}`.
3. L729-734 (now in Theorem 1's proof): n_D, n_S -> N_D, N_S.
4. L736-740:
   - "above x_c" + " (Lemma~\ref{lem:ceiling})";
   - "provider" -> "owner", twice;
   - n_S -> N_S in the display and in "N + vN_S/P_s".
5. L743 (now Corollary 1(ii)'s proof): the part label "(ii)" added.
6. L647 S1: "(Lemma~\ref{lem:prices}(i))" added after "follows from the cost system".
7. L371 S1: ε -> ξ.
8. L751 S1: (I − A^T)y -> (I − A_0^⊤)y.
9. L751 S3 and display L752-756:
   - `\eqref{eq:2}` -> `\eqref{eq:3}`;
   - A -> A_0, \mathsf{T} -> \top;
   - the last line gains "+ρV_mX" and ends "= wN_a + rℓ + ρV_mX".
10. L413-415 (Proposition 6's proof):
    - a title is added;
    - (i) "The taxed stock is fixed by assumption" -> "The owner's plan is constant, so by Lemma A.1(a) it rents out all of the taxed stock at any positive rent, whatever the tax rate" (D82).
11. L769-775 (now Corollary 3's proof):
    - the title -> "Proof of Corollary~\ref{cor:fiscal}";
    - "and hence R/I -> 1" -> "and hence, by (income), (R+ρV_mX)/I -> 1, with R/I -> 1 when ρ = 0";
    - "In the fully automated economy, the cost system gives P_s = rB_s" -> "At methods with λ̃_s = 0, the cost system gives P_s = r b̃_s";
    - A^T, b^T -> A_0^⊤, b^⊤;
    - "is also necessary and sufficient" -> "is necessary and sufficient" (D81);
    - one new closing sentence.

**Edits, Appendix B**

12. L570 S1: `Section~\ref{sec:3}` -> `Section~\ref{sec:economy}`.
13. L594, last sentence: "Table~\ref{tab:A.1} lists the configuration each part of the paper uses." -> "Table~\ref{tab:departures} lists where the paper departs from the economy of Section~\ref{sec:economy}."
14. L203: S1-3 and S5-6 are verbatim in B.1; S4 is in §3.
15. L647 S3 (Proposition B.1(c)): \bar L_i -> \bar\lambda_i, and the label "(c)" added.
16. L647 S2: "All total requirements are nonnegative" -> "All price coefficients are nonnegative".
17. (19), L648-650: w\bar L_i -> w\bar\lambda_i (moved into Proposition B.1).
18. L371 S4 in Proposition B.1(d): "P_s ≥ rB_s gives ..." -> "P_s ≥ rB_s by (a) gives ..., and participation tends to zero as in the proof of Corollary 2". It is also verbatim in Corollary 2's proof.
19. L576-581: the bold lead is dropped; in the display, A -> A_ρ and (I−A)^{-1} -> (**I**−A_ρ)^{-1}.
20. L588: the bold lead "Non-produced inputs." is dropped.
21. L594 S2: A^T -> A_0^⊤, and \mathsf{T} -> \top throughout.
22. L757 S3 (to B.2): "I = wN_a + r^T T" -> "I = wN_a + r^⊤T + ρp_KX (Proposition~\ref{prop:5})" (D88).
23. L622:
    - the bold lead gives way to B.4's title "Worker types" (D92);
    - "The eras figure illustrates" -> "The eras figure (Figure~\ref{fig:4}) illustrates" (D93).
24. L677: the bold lead becomes B.5's title; `Section~\ref{sec:6}` -> `Section~\ref{sec:income}` (D94).
25. L656-661: "At an active margin" -> "At an interior margin"; \bar L_i -> \bar\lambda_i.
26. L663: \bar L_i -> \bar\lambda_i, three times.

**Dropped**
- Headings: L568 "The environment and supporting results", L572 "Environment and equilibrium", L624 "Proofs of the main results", L665 "Timing and institutional rents"; the bold leads of L574, L576, L588.
- L570 S2, "This appendix states the equilibrium conditions, proves the main results, and develops the task-level cost representation and timing extensions."
- L574 S1-S4, "A unit of a task-produced good requires tasks x ∈ [0,1] in equal amounts." / "One human-hour completes γ_L(x) units ..." / "Tasks in H are closed to machines by capability, preference, or law." / "Firms select the least-cost feasible method for every task." (superseded by Assumptions 1 and B.1 and Definitions 1 and B.1).
- L582 S1-S2, "The selected recipes are nonnegative and productive, ..." / "Unused feasible methods have unit costs at least as high ..." (Definition B.1 states both).
- L590 (People), all four sentences: "Each of N workers supplies one hour or exits." / "Types may differ ..." / "Section~\ref{sec:4}'s log-utility example gives s = ..." / "Appendix~\ref{app:B} specifies the provider's budget ...".
- L592 (Government), "The instruments are a payroll tax τ_w; a tax τ_R on pure ownership rents, ...; a uniform consumption tax; and a transfer program paying (m_w, m_e) ..." (superseded by §3.5; the consumption tax is cut by the design).
- L594 S1, "Prices, gross outputs y, final consumption f, task assignment, and participation form an equilibrium when ..." (superseded by Definitions 1 and B.1).
- L594 S5, "Output, participation, and the assignment margin are jointly determined; the replacement closure alone supplies a price condition." (L245 says it).
- L596-620, Table A.1 with its caption and six rows (replaced by Table B.1).
- L667-675, A.4's timing paragraph, every sentence (D99). Its content is now Assumption 2, (unitcost), (21) and Lemma 2:
  - "The main cost system prices contemporaneous service flows."
  - "A dated construction process requires an additional user-cost relation."
  - "Let a, λ, and b be ...", and "If all inputs are advanced one period ..., p_m = (1+ρ)(ap_m+λw+br), ...";
  - "At the task margin," with its display;
  - "For a durable asset costing V_m = ... suppose there are no separate operating costs or capital gains.";
  - "With depreciation δ, the user cost is p_m = (ρ+δ)V_m, giving" with its display;
  - "Each expression requires a positive denominator.";
  - "These are distinct timing conventions ...; interest introduces an income component beyond the main two-factor flow accounting."
- L757 S2, "This proves Proposition~\ref{prop:5}."
- L389 S1-S2, "Intermediate payments cancel when final expenditure is traced through the cost system, ..." / "Appendix~\ref{app:C} gives the cancellation explicitly."
- L371 S5, "Equation~\eqref{eq:10} and continuity of F at zero then give N_a/N -> 0." (replaced by the bound under payments).
- L213 S2, "The coefficients are nonnegative, and the spectral radius of A is below one, so intermediate production can deliver positive net output." (D87).

### Part 13-17: Appendices C-F and back matter

**Edits**
1. L749 title: "Factor income and expenditure shares" -> "Expenditure shares under substitution" (brief §2).
2. L759-763: the CES weight α -> ω in five places; the share α(q) keeps its name.
3. L763: \bar L_0 -> \bar\lambda_0, twice.
4. L767: "This appendix proves the fiscal corollary and develops conditionality, ..." -> "This appendix develops conditionality, ...".
5. L779-787: m_w, m_e -> g_w, g_e (five places, nine symbols).
6. L779: "Under \eqref{eq:8}" -> "Under \eqref{eq:utility} and \eqref{eq:budget}" (prints "Under (6) and (8)").
7. L801: `Section~\ref{sec:4}` -> `Section~\ref{sec:workers}`; z^{\mathsf T} -> z^⊤.
8. L805-810, D.3 on the price coefficients:
   - "In the flow benchmark with one non-produced input, the basket requirements defined in Section~\ref{sec:5} give" -> "With one non-produced input, the basket's price coefficients in Lemma~\ref{lem:prices}(i) give";
   - L_s, B_s -> λ̃_s, b̃_s in the display and in the full-coverage condition;
   - "both total requirements" -> "both price coefficients".
9. D.2 gains L132's last two sentences, verbatim: "Payroll incidence: the quasi-experimental literature (Gruber 1997; ...) ... Interpreting incidence ... participation." (D101)
10. L878: "Let Appendix~\ref{app:A}'s set H have positive measure" -> "Let the set H of Assumption~\ref{ass:tasks} have positive measure".
11. L890: `Section~\ref{sec:4}` -> `Section~\ref{sec:participation}`.
12. L894: `Section~\ref{sec:9}` -> `Section~\ref{sec:measurement}`.
13. L904: p = Ap + λw + Br -> p = A_ρp + λw + Br.
14. L905: "The human-effort content of final consumption is" -> "..., valued at the user cost, is" (D107). L906: ^{\mathsf T} -> ^⊤.
15. L913: the two notation sentences -> "Table~\ref{tab:notation} lists the notation."; and "solves Appendix~\ref{app:B}'s equilibrium" -> "solves Section~\ref{sec:example}'s equilibrium".
16. New sentence opening Appendix C: "This appendix departs from Assumption~\ref{ass:workers}: preferences are CES over goods, in place of a fixed basket." (D105)

**Dropped**
- L913, notation sentence 1, "In Appendices~\ref{app:A.4} and~\ref{app:B} and Figure~\ref{fig:3}, the scalars a, λ, and b are the machine-service, labor, and non-produced input requirements for building a machine, ...; and s denotes the reservation wage."
- L913, notation sentence 2, "Direct requirements of the non-produced input are b_i, total requirements are b̃_i, and P_s is the cost of the basic living basket."

**Moved, not dropped:** L751-757 (Proposition 5's proof, B.2, and the remark after Proposition 5) and L769-775 (Corollary 3's proof).

## 7. Problems

**Found or confirmed at assembly**
1. **Orshansky (1963) has no reference entry.** Figure 5's caption (main.tex L496-511, verbatim in §8) uses "the Orshansky 1963 subsistence bundle" (STATE Open 12(k)). No entry was invented.
2. **F5's plain sentence prints three times**, worded differently each time:
   - in §3 after Definition 1;
   - in Theorem 1's remark in §4;
   - in the remark after Lemma A.1.

   Brief §4 asks for one plain sentence. Part 04 asked to drop it from Theorem 1's remark if §3 has it, and §3 does. Left as delivered (D30, D78).
3. **Exact repeats across parts**, left as delivered:
   - L74 S6 (grid connection) in §1 and §3.1 (D7);
   - L268 S3 (the parents example) in §2 and §3.4 (D6);
   - "stands for whoever sustains a person outside paid work" in §2 and §3.4 (D6).
4. **Near repeats**, left as delivered:
   - L371 S4 in Corollary 2's proof and in Proposition B.1(d);
   - L374 S2 and the remark after Corollary 2 (D35);
   - L199 S3, verbatim in B.1 and restated in §3.2;
   - L268 S5 beside L437 S2 in §6 (D51).
5. **Two underfull lines** (badness 5756, 1237) in the Trammell and Korinek reference entry. They are the cost of the local `\sloppy` that keeps its DOI inside the margin; without it the line is 29.5pt overfull (D110).

**From the parts, still open**

6. **Figure 3's legend** reads "Labor demand, baseline (Appendix B)" (`code/fig_labor_market_clearing.py`, line 62); the instance is now Section 7. The figure is the repository's file, copied unchanged (D55).
7. **`checks/check_interior.py` needs re-pointing** before it backs the new text (design synthesis §6):
   - Section 7's "instance", "shares" and "support" templates no longer match;
   - regions R_B and R_S5 name section titles that no longer exist;
   - Q4's first clause anchors the old D.3 sentence. The new anchor is "With one non-produced input, the basket's price coefficients in Lemma~\ref{lem:prices}(i) give".
   Not run here.
8. **README line 166** maps `checks/corner/check_open.py` to "the trade remark in Section 2"; it should point to Appendix B.3. This is a repository file, for the parent session.
9. **STATE Open 12 items left as printed**, since the brief keeps the text verbatim:
   - (b) the band's specification count;
   - (c) Figure 5's legend labels;
   - (d) L513 against Appendix F;
   - (e) the unstated premise of Proposition E.1(ii)-(iii);
   - (f) D.5's index and max(0, 1−κ);
   - (g) D.2's circular share;
   - (k) the Orshansky reference and the data note's "All U.S. figures ... BEA national accounts".
10. **Unverified claims kept verbatim:**
    - L72's sentence on Zeira (1998), since the publisher's site blocked the fetch;
    - L536's "70th--95th within-group percentiles", attributed to Acemoglu and Restrepo (2026) but not in their abstract.
11. **Math-check items not applied**, since the brief lists no fix:
    - C4, condition 3: Theorem 1's "up to null sets" does not name the indifferent workers. It claims uniqueness of prices and aggregates only (D25).
    - C5: Assumption 5 ranks β = 1 paths by a long-run average that need not converge. Lemma A.1(b)'s proof bounds the limit superior, so it holds either way.
    - B.2 does not state that the owner rents out every input with a positive rent.
    - Definition B.1's operating-input repair (C1) was not rerun numerically (D84).
12. **Length:**
    - Section 10 is 851 words, against the design's estimate of about 630 (D72).
    - 9.1's cut to two-thirds is measured on Section 8's prose without its 200-word caption.

**Raised by the parts and resolved at assembly**
- Part 04: Trammell and Korinek (2026) not placed. Part 03 placed it in §3.6's AI paragraph, and it is cited once.
- Part 04: possible duplicates of L155-157, of L136 S2, and of Corollary 1 against L324 S1-2. None occurs: L155-157 and L136 S2 stand only in §4, and §7 ports only L324 S3-7.
- Part 05: Appendix D's label unsettled. It is `app:D`, as part 03 cites it, and `app:fiscal` is used nowhere.
- Part 05: Appendix B.6 had no label. It is `app:tasklevel`, and L351's pointer is narrowed to it.
- Parts 03, 07 and 09: `app:C`-`app:F`, `app:E` and `fig:4`. All are defined; fig:4 prints as Figure 7.
- Part 03: `eq:2` and the general cost recursion. Part 12 took them into B.1, except L213 S2 (D87).
- Part 11-12: line breaks in Table B.1 and B.4 might shift once the references print as numbers. The final compile has no overfull line.
