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
**State as of:** 2026-11-16 — units 1 (the spec) and 2 (the theory) done, the theory revised after an independent
review; at the breakpoint, her read of both.

## Where things stand

- **The spec** (`docs/spec.md`) was committed alone at c8750c0 and pushed the same day, before any of the paper's data
  were pulled: it is the freeze for H-X, the cross-country test of absorption. Its other predictions (M2, M3, M5) are
  written down and can still be amended before their data are pulled, with a dated entry in its amendment log (two
  entries so far, both before any data: citations, and Section 4 restated after the review; H-X untouched).
- **The theory:** `code/model.py` (the stationary task economy of pinning's Appendix B, durable machines and land,
  with who can leave work generalized: θ, the share with no support outside work; Δ, support paid for working);
  `checks/check_theory.py`, 169/169; Figure 1 (`fig_paths`), Figure 2 (`fig_rates`); Table B.1 (`tab_regimes.tex`);
  `paper/main.tex`, 19 pages, no warnings (compiled to `paper/_build/main.pdf`, not committed).
- **The results** (numbered as in the spec; clearing and equilibrium are an unnumbered paragraph of Section 3.3 and
  Appendix A): Lemma 1, output per hour = 1/L_s(x*), elasticity −1/(1+ψ) ∈ (−1, 0) with respect to hours across
  equilibria with the same technology, T and h; Proposition 1, absorption (hours that cannot leave lower output per
  hour, w/r and w/P_s with technology unchanged); Proposition 2, machine progress and the hours that remain (output per
  hour → the ceiling T/(hN_∞) when some hours cannot fall, and the elasticity of output per hour with respect to
  machine capability → 0; with funded unconditional exit the elasticity → 1); Proposition 3, the required return
  (at a given threshold the elasticity of w/r w.r.t. ρ + δ is 1/D, D land's share of a machine's build cost; whoever
  can leave work, a lower return lowers w/r, w/P_s and labor's share and raises land's price in hours; enclosed, only
  prices move; funded, output per hour rises); Lemma 2, the price wedge on price requirements; Lemma 3, composition
  (Baumol with bound goods; consumption capped iff the elasticity is below one, the CES economy itself not solved).
- **The instance's numbers** (all from `model.numbers()`; θ = Δ = 0 reproduces pinning's Appendix B to machine
  precision): output per hour 5.01 funded, 4.87 conditioned (Δ = 0.3), 4.64 a quarter enclosed, 3.72 all enclosed
  (26 percent lower); elasticity −0.59, ψ 0.70; ceilings 49.3, 23.5, 5.88; elasticity of output per hour w.r.t.
  capability over the first tenfold gain 0.35 / 0.33 / 0.29 / 0.16, over the third 0.89 / 0.23 / 0.12 / 0.004;
  labor's share 0.55 → 0.58 under full enclosure (0.50 → 0.47 with the steeper schedule k = 8); ρ 0.09 → 0.04
  enclosed: w/r −52%, w/P_s −11%, labor's share 0.58 → 0.51, land in hours ×4.7; funded: w/r −60%, labor's share
  0.55 → 0.50, participation 0.58, output per hour +3%; rent alone pays for 0.38 of a basket per person (funded).
- **Data so far:** only the cached FRED OPHNFB (copied from `../paths/cache`, identical SHA-256 d42ef61a…; last
  observation 2026Q2), for the introduction's eras (2.8 / 1.4 / 3.0 / 1.5 percent a year). M1 replaces it with a dated
  fresh pull. Reachability checked 2026-11-16 (status codes only, no values): every FRED ID the spec names; BEA's GDP
  by industry files and NIPA flat files; the OECD productivity dataflows; the Penn World Table on Dataverse; Crossref.
  BLS's website returns 403 to scripts, its API answers.
- **References:** the journal entries checked against Crossref on 2026-11-16, DOIs added; Hansen (1939) and Baumol
  (1967) have no Crossref record and stay as printed; books and the NYT review unchecked. Dew-Becker and Gordon now cited
  as published (2012), Greaney (2026) verified.
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
6. **The policy reading** the review exposed: the paper no longer claims that a uniform rent dividend releases hours
   without a wedge, because the model has no such instrument and rent alone covers 0.38 of a basket per person in
   the instance (funded exit is paid mostly from interest). Whether the paper should model the dividend (a support
   level funded from rent, below one basket) or leave policy to pinning is hers to decide.

## Next

Unit 3, on her go after the read: the data and figures M1–M5 and H-X exactly as `docs/spec.md` states them, each with
its check; H-X first (it is the frozen one). Unit 4: Sections 1, 2 and 5–7 written in full, the remaining references
checked, an independent review of the data and a referee read, the compiled PDF.

## Log

- **2026-11-16 — the theory revised after an independent review.** A reviewer (a subagent given the files, not my
  conclusions) re-derived every result and tried to break each statement; its scratch scripts were outside the
  repository. Every quoted number reproduced and every proof step held; the findings were missing assumptions and
  overstated prose, each re-checked here before it changed the text. **Fixed:** (1) funding is part of equilibrium but
  was missing from the existence statement and Proposition 2 (Δ = 1 clears the labor market unfunded; 131 of the 300
  random check economies had been unfunded): the statements now separate clearing from funding, Proposition 2 states
  the limit funding condition T > h[(1−θ)N + ΔN_∞], and the random economies are drawn until 300 are funded (211
  unfunded skipped); (2) Proposition 2's λ = 0 branch needs F(z) > 0 for z > 0; (3) strictness in Δ and in ρ needs a
  positive density of F at the point, not F < 1; (4) Lemma 1 holds T and h fixed (which M4's envelope inherits);
  (5) "grows at the pace of machine capability" overstated: Proposition 2(iv) is now the elasticity across stationary
  states, the text says "eventually", and Figure 1's discussion gives the elasticity by tenfold gain (the rules differ
  little at first, 0.35 against 0.16, and a great deal by the third gain, 0.89 against 0.004); (6) the introduction's
  elasticity is with respect to ρ + δ at a given threshold; (7) "absorption does not account for the fall in labor's
  share" was wrong in general (labor's share is ω L_s, and with a steeper schedule absorption lowers it): restated;
  (8) Lemma 2 needs the price requirements (with ρ > 0, P_s ≠ wL_s + rB_s on the stationary requirements; it equals
  wL̃_s + rB̃_s): restated, with the "first's cause" sentence corrected; (9) "if, and only if" on σ < 1 replaced by what
  Lemma 3 shows, with a new part (b) for σ ≥ 1; (10) the welfare paragraph's wedge and rent-dividend claims withdrawn
  (Open 6); (11) the existence proof no longer needs γ' (identity (A.1), m(x) = 1 − x + J/γ nonincreasing), a, λ ≥ 0
  stated, Ĵ defined in Proposition 2, the IFT branch shown to be the unique clearing threshold. **New:** Proposition
  3(ii), from the reviewer's observation that the claim about prices held for θ < 1 but was unproved: whoever can leave
  work, a lower return lowers w/r, w/P_s and labor's share, by (A.1). Checks 142 → 169.
- **2026-11-16 — references checked against Crossref** (DOIs added; Dew-Becker and Gordon 2012 as published).
- **2026-11-16 — the theory unit.** `code/model.py`, `checks/check_theory.py` (A sympy algebra; X the funded case
  against pinning's `appendix_b.py`, worst gap 6.6e-16; E equilibrium conditions from primitives in four economies;
  L, P1, P2, P3 the results, P2 along a millionfold path; W, C the lemmas; R random economies; Q every model number in
  the theory regions found next to its words, no decimal unchecked, the eras, Table B.1 rebuilt and compared, the
  figures' AI line). Figures drawn at print width with a validated categorical palette (the dataviz validator: all
  checks pass; aqua and yellow below 3:1 on white, so every line is labeled directly). Found while checking, all in the
  checks rather than the results: a bound in P2 applies only once every task is open to machines; convergence along
  the path is linear in η and is tested as such; Lemma 3's checks used a second CES normalization and now use the
  paper's; random economies in which every supported person already works do not shift supply with θ.
- **2026-11-16 — the spec** (`docs/spec.md`), committed alone (c8750c0) before any outcome data: the H-X freeze.
- **2026-11-16 — founded.** Plan put to her and approved ("This sounds good, go for it").
