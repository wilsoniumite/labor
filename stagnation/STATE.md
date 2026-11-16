# STATE — stagnation (resume point for the next session)

**Project:** *Understanding the Great Stagnation*, a standalone paper begun 2026-11-16 at her request ("a new
paper, that may reference pinning the wage but apart from that should be standalone"). Byline open (Open 1).
**Collaboration:** her go on the plan of 2026-11-16 ("This sounds good, go for it"), with its defaults: a working
paper like pinning (about 30–40 pages, SSRN first); the model restated in the paper and pinning cited for the full
development, the fork and κ cited rather than rebuilt; the cross-country test pre-registered; one short closing section
on AI; breakpoints after the spec and after the theory (taken together, since the spec writes down the plan she had
just approved). House rules as in `../pinning/`: every number from a script, checks gate absolutely, figures from
scripts, primary data only, stop and report on any access failure, references checked against Crossref before
submission, code as plain functions in notebook-cell style.
**State as of:** 2026-11-16 — units 1 (the spec) and 2 (the theory) done; at the breakpoint, her read of both.

## Where things stand

- **The spec** (`docs/spec.md`) was committed alone at c8750c0 and pushed the same day, before any of the paper's data
  were pulled: it is the freeze for H-X, the cross-country test of absorption. Its other predictions (M2, M3, M5) are
  written down and can still be amended before their data are pulled, with a dated entry in its amendment log.
- **The theory** (commit 444ce78): `code/model.py` (the stationary task economy of pinning's Appendix B, durable
  machines and land, with who can leave work generalized: θ, the share with no support outside work; Δ, support paid
  for working); `checks/check_theory.py`, 142/142; Figure 1 (`fig_paths`), Figure 2 (`fig_rates`); Table B.1
  (`tab_regimes.tex`); `paper/main.tex`, 18 pages, no warnings (compiled to `paper/_build/main.pdf`, not committed).
- **The results** (numbered as in the spec; existence and uniqueness is an unnumbered paragraph of Appendix A):
  Lemma 1, output per hour = 1/L_s(x*), with elasticity −1/(1+ψ) ∈ (−1, 0) with respect to hours across equilibria
  with the same technology; Proposition 1, absorption (more hours that cannot leave lower output per hour, w/r and
  w/P_s with technology unchanged); Proposition 2, machine progress and the hours that remain (output per hour → the
  ceiling T/(hN_∞), and its growth rate → 0, when some hours cannot fall; growth → the pace of machine progress
  when exit is funded and unconditional); Proposition 3, the required return (elasticity of w/r at a given threshold =
  1/D, D land's share of a machine's build cost; enclosed, the threshold does not move and only prices do; funded,
  output per hour rises); Lemma 2, the price wedge; Lemma 3, composition (Baumol with bound goods).
- **The instance's numbers** (all from `model.numbers()`; θ = Δ = 0 reproduces pinning's Appendix B to machine
  precision): output per hour 5.01 funded, 4.87 conditioned (Δ = 0.3), 4.64 a quarter enclosed, 3.72 all enclosed
  (26 percent lower); elasticity −0.59, ψ 0.70; ceilings 49.3, 23.5, 5.88; labor's share rises with absorption (0.55 to
  0.58), so the fall in labor's share has to come from Propositions 2–3; ρ 0.09 → 0.04 enclosed: w/r −52%, w/P_s −11%,
  land in hours ×4.7; funded: w/r −60%, participation 0.58, output per hour +3%.
- **Data so far:** only the cached FRED OPHNFB (copied from `../paths/cache`, identical SHA-256 d42ef61a…; last
  observation 2026Q2), for the introduction's eras (2.8 / 1.4 / 3.0 / 1.5 percent a year). M1 replaces it with a dated
  fresh pull. Reachability checked 2026-11-16 (status codes only, no values): every FRED ID the spec names; BEA's GDP
  by industry files and NIPA flat files; the OECD productivity dataflows; the Penn World Table on Dataverse. BLS's
  website returns 403 to scripts, its API answers.
- **Environment (cloud session):** the venv was built at the repository root with numpy, pandas, scipy, sympy,
  matplotlib, tqdm, requests (`../venv/bin/python` here; `../venv/Scripts/python.exe` on her machine); TeX Live and
  latexmk installed with apt. Neither is committed.

## Open — her calls

1. **Byline:** her alone, with Johan, or other. The title page and the AI declaration say "[Byline to be confirmed]".
2. **The read:** the thesis, the six results and their framing (Sections 3–4), the introduction and Section 2.
3. **Proposition 3's magnitudes.** In the instance land is 35 percent of a machine's build cost, so the elasticity of
   w/r with respect to ρ + δ is 2.87 at the funded threshold; the text calls the magnitudes illustrative and notes that
   the return required on productive capital fell much less than safe rates. Keep Figure 2 in the main text, or move
   it to an appendix?
4. **The measurement thresholds** written before the data (M2: composition at least a quarter of the slowdown supports,
   a tenth or less counts against; M3: shelter removes at least a third of the price wedge, less than a tenth counts
   against). They can be amended, with a log entry, until their data are pulled; H-X is frozen.
5. **The rules' names** in the figures and Table B.1: Funded exit, Conditioned support, Quarter enclosed, All enclosed.
6. **References** are not yet checked against Crossref (unit 4); entries shared with pinning are copied from its
   audited list; Greaney (2026), the comment on Hsieh and Moretti, was verified on 2026-11-16 (AEJ: Macro 18(2):
   409–28, DOI 10.1257/mac.20230141).
7. **The independent maths review** of the theory: below (Log).

## Next

Unit 3, on her go after the read: the data and figures M1–M5 and H-X exactly as `docs/spec.md` states them, each with
its check; H-X first (it is the frozen one). Unit 4: Sections 1, 2 and 5–7 written in full, references checked against
Crossref, an independent review (maths, data, a referee read), the compiled PDF.

## Log

- **2026-11-16 — the theory unit.** `code/model.py`, `checks/check_theory.py` (142: A sympy algebra; X the funded case
  against pinning's `appendix_b.py`, worst gap 6.6e-16; E equilibrium conditions from primitives in four economies;
  L, P1, P2, P3 the results, P2 along a millionfold path; W, C the lemmas; R 300 random economies; Q every model number
  in the theory regions found next to its words, no decimal unchecked, the eras, Table B.1 rebuilt and compared, the
  figures' AI line). Figures drawn at print width with a validated categorical palette (the dataviz validator: all
  checks pass; aqua and yellow below 3:1 on white, so every line is labeled directly). `paper/main.tex` 18 pages.
  Found while checking, all in the checks rather than the results: a bound in P2 applies only once every task is open
  to machines; convergence along the path is linear in η and is now tested as such; Lemma 3's checks used a second CES
  normalization and now use the paper's; random economies in which every supported person already works do not shift
  supply with θ, so Proposition 1's hypothesis is tested with a shift in N and with θ only where supply is not
  saturated.
- **2026-11-16 — the spec** (`docs/spec.md`), committed alone (c8750c0) before any outcome data: the H-X freeze.
- **2026-11-16 — founded.** Plan put to her and approved ("This sounds good, go for it").
