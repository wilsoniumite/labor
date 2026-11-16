# STATE — stagnation (resume point for the next session)

**Project:** *Understanding the Great Stagnation*, a standalone paper begun 2026-11-16 at her request ("a new
paper, that may reference pinning the wage but apart from that should be standalone"). Byline: Stella Wilson alone
for now (Decision 1).
**Collaboration:** her go on the plan of 2026-11-16 ("This sounds good, go for it"), with its defaults: a working
paper like pinning (about 30–40 pages, SSRN first); the model restated in the paper and pinning cited for the full
development, the fork and κ cited rather than rebuilt; the cross-country test pre-registered; one short closing section
on AI; breakpoints after the spec and after the theory (taken together). At that breakpoint she delegated the open
calls ("I leave those questions up to you, go ahead"): they were decided as under **Decisions** below, and units 3 and
4 were done without a further stop. House rules as in `../pinning/`: every number from a script, checks gate
absolutely, figures from scripts, primary data only, stop and report on any access failure, references checked against
Crossref before submission, code as plain functions in notebook-cell style.
**State as of:** 2026-11-16 — all four units done: the spec, the theory, the measurements, the full draft, revised
after an independent data review and a referee read (36 pages, `paper/_build/main.pdf`, not committed). Three
batteries pass: `check_theory.py` 171/171, `check_hx.py` 21/21, `check_data.py` 123/123. At her read of the whole;
the referee's larger requests, which need new modeling or data, are listed under Open for her decision.

## Where things stand

- **The spec** (`docs/spec.md`) was committed alone at c8750c0, before any of the paper's data were pulled: the freeze
  for H-X. Its amendments log has three entries, all made before the outcome they touch was computed (citations; Section
  4 restated after the theory review; M2's source changed when the planned BEA files turned out not to exist), and a
  fourth recording the exploratory readings and descriptive numbers added after the measurements were seen.
- **The theory** (Sections 3–4, Appendices A–B): unchanged since the review (Log, theory review). `code/model.py`,
  169 checks, Figure 1 (`fig_paths`), Figure 2 (`fig_rates`, now drawn over ρ 0.04–0.10), Table B.1.
- **The measurements** (Section 5; scripts in `code/`, outputs in `data/`, raw pulls in `cache/`, all pulled
  2026-11-16; times in `cache/MANIFEST.md`, `cache/fred/MANIFEST.csv` and the paper's Appendix C):
  - M1 (FRED): output per hour 2.8 / 1.4 / 3.0 / 1.5 / 2.2 percent a year over the five eras; hours per person 16+
    −0.07 / +0.25 / −0.52 / −0.22 / −0.48 (with BLS's January population steps smoothed: 0.00 / +0.30 / −0.35 / −0.24 /
    −0.31), so since 1973 the eras rank in exactly opposite orders on the two (not a prediction; 1948–73 breaks it;
    women's entry, which raised hours in 1973–95, raised productivity: Hsieh et al. 2019). Lemma 1 bounds what the
    swing in hours per person from 1948–73 to 1973–95 can do: at most 0.32 of the 1.3-point slowdown (0.19 at the
    instance's elasticity). Labor's share on decade averages −3.6% (1948–57 to the 1990s), −9.3% (the 1990s to
    2016–25); the Cleveland Fed 10-year real rate 6.5% (1982–84) to −0.12% (2020); land's share of household real
    estate 22% (1952–72) to 37% (2004–19), a residual that dropped in 1974.
  - M2 (BEA–BLS integrated industry-level production account, spliced at 1997): **supports** by the frozen rule —
    composition is 47% (41–58) of the 1973–95 slowdown and 38% (38–47) of 2004–19. But: the grid's three class-swap
    members cannot move the total, so the median is the baseline's; Baumol's weight shift is only 14% and 13%;
    without agriculture (exploratory) 27% and 19%, partial; composition took more from the boom of 1995–2004 (1.21
    points) than from either slow era, so what separates the slow eras from the boom is within sectors (53% and 62%
    of the slowdowns, manufacturing the largest piece; construction +2.3% to −0.9%). BEA's two files differ by 0.34
    points a year over 1998–2016; on the older alone the 2004–16 share is 34% against 38%.
  - M3: **supports**, narrowly in the later window — the price wedge is 73% of the pay–productivity gap; CPI less
    shelter removes 37% (1973–2024) and 34% (1983–2024) of it; energy 4% / −6%, medical care 13%. The text now says
    the test is close to mechanical (owner-occupied housing is outside the sector and heavy in the CPI) and that the
    pay is average pay.
  - M4 (PWT 11.0): U.S. hours per worker −0.31%/yr 1950–80, −0.07% after; the envelope at the instance's elasticity is
    6.5% by 2023, 0.15 points a year (0.10–0.25). No share of the slowdown is stated: it is 17%, 46% or 7% by the
    windows compared. The hours that stopped falling are mostly high earners' (Kuhn and Lozano 2008; Costa 2000);
    Europe is discussed as the objection it is.
  - M5: the plan stated only what would count against the account; it did **not** count against (output per hour
    2.25% against 1.50%, hours per person −0.48%/yr, compression 0.40%/yr), and the text says demographic and demand
    accounts predict the same.
  - H-X: **uninformative** by the frozen rule — across countries +0.33 (p 0.39), within countries −0.25 (bootstrap
    p 0.013), IV +0.16 (p 0.72); no leave-one-out flips the sign.
- **The draft** (`paper/main.tex`): the abstract now says that land caps output under every rule and that the gains
  go to rents under every rule; the introduction speaks of one cost system moved by a few primitives, not one cause;
  Section 2 gained paragraphs on energy and labor's share and the literature the referee expected; Section 3.3 says
  the instance was not set to land's share of machine cost (machines use 49 percent of the land in it); Section 4.2
  states the basket's assumptions; a new Section 4.5 and Table 1 map each fact to what moves it in the model (two are
  primitives, not results); Section 5 as above; Section 6 (Table 2) scores three predictions and one condition;
  Section 7 restated policy and AI in the theorems' terms with a comparative prediction; Appendix C gives the record
  of the plan with commit and pull times (checked against git and the manifests).
- **References:** 21 added after the referee read (Acemoglu et al. 2014 … Vivalt et al. 2024; Ricardo 1817 and
  George 1879 as books), each journal entry checked against Crossref on 2026-11-16. Before that, 14 added for the
  measurements, each checked against Crossref on 2026-11-16 (Autor, Dube and McGrew
  2023; Borjas 1980; Brynjolfsson, Rock and Syverson 2021; Cameron, Gelbach and Miller 2008; Eldridge et al. 2020;
  Feenstra, Inklaar and Timmer 2015; Feldstein 2008; Garner, Harper, Russell and Samuels 2026; Goldin 2006; Haubrich,
  Pennacchi and Ritchken 2012; Jorgenson 1988; MacKinnon and White 1985; Stansbury and Summers 2017; Webb 2023) and one
  book unchecked (Bruno and Sachs 1985).
- **Environment (cloud session):** the venv at the repository root (numpy, pandas, scipy, sympy, statsmodels,
  matplotlib, tqdm, requests, openpyxl; `../venv/bin/python` here, `../venv/Scripts/python.exe` on her machine);
  TeX Live and latexmk from apt. Neither is committed. BLS's website refuses scripts (403); FRED, OECD, Dataverse
  (PWT), BEA and Crossref answered.

## Decisions taken for her (2026-11-16, on "I leave those questions up to you, go ahead")

1. **Byline:** Stella Wilson alone, with pinning's affiliation and email and a views disclaimer. Johan is added only
   with his agreement; hers to change.
2. **Figure 2** stays in the main text, drawn over ρ from 0.04 to 0.10, the range the text discusses (lower required
   returns on productive capital are not in view).
3. **Policy:** the rent dividend stays unmodeled and is left to pinning; the conclusion says that rent alone pays for
   0.38 of a basket in the instance, the same order as pinning's measured coverage ratio (0.30 in 2025).
4. **The thresholds** were kept as written and then applied as frozen. The rules' names were kept too.

## Open — her calls

1. **The byline** (Johan or not) and the AI declaration's statement of review, left in brackets because only she can
   make it. The referee also asked to drop "Drawn by code written with Claude" from the captions; it is pinning's
   house rule, so it stays unless she says otherwise.
2. **The read of the whole**, and whether the reframing is enough for SSRN. The referee recommended a major revision
   and a change of framing before posting; the framing changes were made (land caps output under every rule; several
   primitives, not one cause; the weaker measurements said plainly).
3. **The referee's larger requests**, each new modeling or data work, none started:
   (a) solve the economy with a CES basket and structures that substitute for land, so the ceiling is not an artifact
   of the Leontief land basket (Lemma 3(b) removes the cap at σ ≥ 1; housing's spending share is roughly constant);
   (b) recalibrate b and h to land and resource rents in full-chain costs (in the instance machines use 49 percent of
   the land; Lemma 1's elasticity and Proposition 3's magnitudes depend on it);
   (c) one path of (η, ρ, θ, Δ) that matches the facts jointly;
   (d) a Domar-weighted gross-output decomposition, era-to-era comparisons, and a growth-accounting test (absorption
   works through capital per hour; standard accounts put much of each slowdown in TFP);
   (e) a decomposition of the price wedge in the manner of Pessoa and Van Reenen (2013), land intensities from
   input–output tables, and CPI-U-X1 for the 1973 window;
   (f) a section on Europe with one hours concept (prime-age denominators);
   (g) evidence to discipline the work-cost distribution F (transfers, lotteries).
4. **SSRN:** whether and when to post. Journals will want an abstract of 100–150 words (it is about 240).

## Next

Her read, then revisions. A further test the paper names but cannot run: Proposition 2(iv) across countries that share
a frontier (output per hour should respond less to machine capability where more hours cannot leave work), which needs
a measure of θ.

## Log

- **2026-11-16 — the data review and the referee read, and the revision after them.** Two subagents, given the files
  and not my conclusions. The data reviewer rebuilt M1–M5 and H-X from the cache with its own code (its Törnqvist
  double deflation reproduces BEA's own research tables to 0.0006 points) and reproduced every quoted number; it found
  ten problems, none changing a frozen verdict, all fixed: the M4 share of the slowdown compared mismatched windows
  (now no share; the sensitivity stated); M5 had been called a prediction (the plan stated only what would count
  against); Lemma 1's bound used the 1973–95 rise instead of the swing (0.32, not 0.25); the computers clause
  contradicted the industry data (dropped); "as much as in the slow eras" understated (composition took more in the
  boom); the grid's class-swap members cannot move the verdict (said); X1 labeled and worded precisely; the
  attribution footnote's reason was wrong; BLS's January population steps (smoothed as a sensitivity); the IV's shared
  sources and §6's firmness about the within estimate. The referee (major revision) found the proofs correct and the
  numbers reproducible, and asked for the framing to change: land caps output under every rule; the theory has
  several primitives, not one cause; the instance is not disciplined on land's share of machine cost; composition
  does not test the mechanism; hours concepts and Europe; the wedge test is nearly mechanical and uses average pay;
  the pre-registration was described too strongly (the eras were known; M5 had no prediction; the §1 edit was not
  logged; the exploratory readings were not logged); policy and AI beyond the model; literature. Fixed in the text,
  the checks and the plan's log, except the requests under Open 3. Checks 169 → 171 (theory), 107 → 123 (data).
- **2026-11-16 — the full draft (unit 4).** Sections 5–7 written; the abstract and introduction carry the measured
  facts; the decisions applied (byline, Figure 2's range, the policy paragraph); `checks/check_data.py` written (107
  checks: the caches' hashes, every data JSON against a fresh run, M1–M5 by second routes where one exists, every data
  number in the text inside a recomputed phrase and none outside); `check_theory.py` Q5 counts seven figures;
  `check_hx.py` reads Section 5.5. 14 references added after Crossref. 30 pages, no LaTeX warnings.
- **2026-11-16 — the measurements M1–M5 (unit 3).** FRED (18 series), the BEA–BLS production account, PWT 11.0; the
  results as under *Where things stand*. October 2025 was not collected for the household survey and the CPI (the
  shutdown): 2025 averages use 11 months. CUUR0000SA0LE does not exist on FRED; CPI less energy is CPILEGSL.
- **2026-11-16 — H-X run as frozen: uninformative** (aff91f3).
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
