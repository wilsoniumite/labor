# STATE — participation (resume point for the next session)

**Project:** what the paper's model says about who works — men and women, the young and the old, retirement,
time in school, youth unemployment — tested on data without letting the data write the test. Founded
2026-10-08 from the paper's Future Work paragraph on participation (her question; her call to start from the
data, with something to test against).
**Collaboration:** same contract as the sibling threads — drafting and sequencing delegated to Claude, checks
gate absolutely, direct critique over validation; the design decisions below are a veto window for her calls.
**The wall:** this repository is public. Public data only (Eurostat; OECD and ILO as named in the inventory).
**State as of:** 2026-10-08 (paused mid long-run drafting; see 'The long run') — protocol written, reviewed and amended; pipeline built, adversarially reviewed and
validated on synthetic data, all checks green; committed but NOT yet frozen (the `participation-P-freeze` tag
waits for her go-ahead); no outcome value downloaded (the fetch log holds one line: the 2010 population).

## How the thread works (read before touching anything)

`PROTOCOL.md` is the contract. In one paragraph: the model's predictions (D: distinctive, C: consistency
checks) were written down before any data; the 31 European countries are split once into an explore half and
a confirm half; exploration on the explore half is free and ends in at most five frozen E-hypotheses; then
`code/confirm.py` runs once — P on the full sample (primary) and the confirm half, E on the confirm half. Two
git tags carry the freezes: `participation-P-freeze` (protocol + all code + split) and
`participation-E-freeze` (E specs). `code/eurostat.py` refuses explore data before the first tag and confirm
data before the second. A 2026-2028 rerun of the frozen code is the only test on unseen data.

## Where things stand

- **The theory, checked before data** (`docs/derivations.md`). Three adversarial critics found the
  draft's headline predictions (young respond more to rents than old; women more than men) follow from
  standard life-cycle hedging and are not tests of this model. The model's distinctive piece is the
  **floor kink**: where the parental home is the exit, a rise in rents stops pushing the young into work (the
  exit value is flat at the dependency floor), while the standard income-effect account says the push grows
  as income after housing shrinks. D1 (across countries, moderated by pre-sample coresidence) and D2 (within
  country, curvature) test it. The original P4 (inactive NEETs vs coresidence) was dropped as not implied;
  P7 (pension ages) dropped for want of an annual pension-age table.
- **The design, checked before data** (`docs/design_review.md`): explore/confirm split by matched pairs
  within five regions, wild cluster bootstrap with Webb weights, Holm within families, G* < 8 =
  uninformative, mechanical break dummies, nationals, q = rents over non-energy industrial goods lagged.
  Departures from the reviewer's proposal: P on the full sample as primary (adopted); no hand-coded pension
  table (dropped with P7, so C-2 has no pension control — country trends as robustness); GitHub tag
  protection and a CI action not set up (the tags are local until she decides to push).
- **The data, scouted blind** (`docs/data_inventory.md`): all series exist and are reachable through the
  Windows certificate store (`truststore`); FRED timed out from this machine on 2026-10-08. Tenure by age only
  from 2015 (`ilc_lvps05`); youth wages only four-yearly (SES).

## Design decisions (veto window)

1. A new thread, not `paths/` — it is the paper's future work, not bank risk.
2. Europe (Eurostat, 31 countries) as the panel; OECD non-European members held back as a possible
   never-explored replication set, not added.
3. The model-level verdict rests on D1 and D2 only; the C checks speak to the mapping onto groups.
4. Participation (activity rate) as D1/D2's outcome; employment as a secondary.
5. The freezes are local git tags; pushing them to GitHub (and timestamping) is her call.
6. **No G* threshold; a leave-one-country-out qualifier instead** (amended before the freeze). The design
   critic's "design uninformative below G* = 8" rule would have voided D1 in about a third of full-sample
   designs, while the simulations held the bootstrap's size at 4.6-5.8% in exactly those designs. A verdict
   whose own-direction p exceeds 0.10 when some single country is left out reads "rests on one country (XX)".
7. Readings the reviewers flagged, written into `PROTOCOL.md` before the freeze: C3 breaks from control series
   too; the equal-weight sex rule for activity/employment bands only; C7's fallback per country; C-4 without the
   UK; C-5's breaks reported plus a drop-them robustness run; C-6 without U_ct; D1's top quartile = 75th
   percentile; the robustness table; Holm over the whole family; the design half limited to the 31 countries.

## Findings since the P freeze

- **The frozen panels run from 2009, not 1997** (found 2026-10-08 from `years_used`, before exploring). C7's
  `une_rt_a` (ages 25-74, 25-54, 15-29) starts in 2009 for 14 of the 16 explore countries (FR 2003, SE 2005), and
  the pre-freeze amendment "one source per country, never spliced" keeps it for every country it covers. So every
  test with U_ct (D1, D2, C-1 to C-4) and C-6 (U 25-54) runs on roughly 2009-2025, losing the 2000s housing boom
  and bust. `lfsa_urgan`, the named fallback, starts 1995-2002. The code does what the frozen rule says, so this
  is not a plumbing bug; changing it would be a deviation (section 7). Kept as frozen; the long-window versions
  are candidates for E (tested on the confirm half, never changing a P verdict).
- **The frozen tests on the explore half** (`results/specs_explore.json`, B = 9999): all eight inconclusive;
  model-level inconclusive. Explore-half MDEs: D1 13.6 points of participation per unit of log q x sd(F), D2 7.0,
  C-1 14.9, C-2 15.2, C-4 0.24, C-5 48, C-6 0.53. These are the pre-look MDEs the protocol asks for.

- **The exploration** (`explore/SYNTHESIS.md`; per theme `explore/<theme>/findings.md`; vetting scripts in
  `explore/_vet/`; about 293 specifications by five explorers plus several hundred vetting regressions). In one
  line each:
  - women's prime-age participation converged on men's everywhere (gap -14.8 → -5.2, 2005-2025): solid,
    standard;
  - older participation rose after 2009 (women 60-64 26 → 58), cohort replacement, no response to rents or
    house prices;
  - enrolment at 20-24 rises after high prime-age unemployment (lagged; crisis years);
  - the young hold more clerical jobs (+2.1 points);
  - nothing since 2023 for entrants;
  - the floor kink has the model's sign only with country trends (D1 -6.1, p 0.028; +3.3 without) — suggestive
    at most, and the goods leg of q carries as much as the rent leg.
  - Design flaws the explore half shows in the frozen tests, reported, not fixed:
    - D2's squared deviation is close to a quadratic time trend (IE supplies 61% of its variation);
    - C-4 rests on CH (G* 1.8);
    - the C-6 secondary's `ilc_lvps09` is the status mix of coresiding youth, not the share of students at home,
      so that no-verdict secondary cannot be read as registered;
    - CP041 is weak where rental markets are thin (BG, PL, HR, MT).
- **Plumbing fix before the E freeze** (section 7): `build.aging` returned NaN for HU (2011 open age group 85+),
  dropping it from C-5 silently; fixed, check G5b added, `results/specs_explore.json` rerun (C-5 now 16
  countries; C-5's explore p 0.23).
- **The E freeze** (her go-ahead, 2026-10-08): `code/e_specs.py` = `explore/e_specs_draft.py` with a new header.
  The E-hypotheses are:
  - E-HF1: D1 with country trends and the long window; varies D1;
  - E-OCC1: the young hold the clerical stretch;
  - E-SCH1: enrolment on lagged prime-age unemployment; varies C-6.

  Holm within the three. E-OCC2 is not frozen; it can run as exploratory on the 2026-2028 data. Check J4 now runs
  the three E in the synthetic look; checks 65/65.

## The look (2026-10-08, `results/confirm_8623706.json`, commit c3f702b; B = 9999)

One download of all 31 countries; the explore half's 61,000 cells identical to the explore download.

**Model-level verdict: inconclusive.** Primary tests, full sample (31 countries, about 2009-2025):

| Test | Estimate | One-sided p (predicted / opposite) | Verdict |
|---|---|---|---|
| D1 floor kink across countries (< 0) | +0.72 (se 4.96) | 0.56 / 0.44 | inconclusive |
| D2 floor kink over time (< 0) | +3.93 (se 2.54) | 0.94 / 0.064 | inconclusive |
| C-1 coresidence on rents (> 0) | -3.38 (se 4.39) | 0.77 / 0.23 | inconclusive |
| C-2 young minus old on rents (> 0) | -0.05 (se 3.85) | 0.50 / 0.50 | inconclusive |
| C-3 second earners (> 0, both legs) | W-M -3.51, W -3.37 | 0.94 / 0.066 | inconclusive |
| C-4 entrants since 2023 (< 0) | -0.03 (se 0.11) | 0.38 / 0.62 | inconclusive |
| C-5 aging and routine jobs (< 0) | -5.98 (se 13.4) | 0.33 / 0.67 | inconclusive |
| C-6 school on prime-age unemployment (> 0) | +0.31 (se 0.11) | 0.005 / 0.995 | **supported** (LOO max p 0.012) |

Confirm-half replication (labels for information): all inconclusive; C-6 +0.33, p 0.039.

**E on the confirm half (Holm within three):**
- **E-HF1** (the trend-dependent kink): +1.61 (se 1.96), p 0.83 — inconclusive; the explore half's -6.1 did not
  replicate. No-verdict decomposition: rent x F +9.1 (two-sided p 0.033), the opposite of the kink.
- **E-OCC1** (young hold clerical jobs): +0.26 (se 0.64), p 0.29 — inconclusive; did not replicate.
- **E-SCH1** (enrolment on last year's prime-age unemployment): +0.52 (se 0.09), p 0.0016 — **supported**
  (LOO max p 0.008, G* 4.4). Without 2008-2013 it is +0.03: it rests on the crisis years, as on the explore half.

**Reading.** Over 2009-2025 the model's distinctive prediction finds no support in 31 European countries, and the
one data-suggested rescue failed on fresh countries; nothing is formally contradicted, but the leanings
(D2's p_opposite 0.064, the confirm half's rent x F +9.1) point the other way. What holds is standard: schooling is
countercyclical. Everything after this point is post-look and exploratory.

## The long run (opened 2026-10-08 on her call: "look further back ... to say 1950, even if data is imperfect")

Post-look. The years before 1997, and the non-European OECD members in any year, are unseen in this study and can be
a second, backward holdout. Blind scouting, a theory critic and a design critic ran first (`longrun/docs/`: coverage
only, no values). What they found:
- **Data.** Only the US reaches 1950 by sex and age: CPS 1948+, BEA tenant rent over goods 1929+, young adults at
  home 1960/1967+. Across countries, participation by sex and five-year age (OECD `DF_LFS_INDIC`) starts US 1960,
  FI/SE 1963, AU 1966, JP 1968, DE/IT 1970, ... : 8 countries by 1970, 13 by 1975, 21 by 1985. Rents relative to
  prices: Jorda-Schularick-Taylor (rent yield x house prices / CPI) for 13 countries unbroken 1950-2020; the OECD
  rent index for 10 countries from 1960, 18 by 1970. A goods-only CPI before about 1985 exists for few countries.
  A predetermined floor measure: census microdata (IPUMS-International; registration needed: hers to do) from
  1960-75 for about 15 countries; or a time-invariant family-organisation measure (Giuliano-Nunn, all OECD).
- **Theory (the critic's headline).** Over 1950-1996 the model's D1 sign is regime-dependent (0, +, -, + as rents
  rise relative to the floor thresholds), so a pooled 1950-1996 D1 is unsigned. The early, low-rent, rent-controlled
  decades are years in which the model and the standard account agree. The discriminating content is within-country:
  in high-floor countries the young's slope on rents should fall to <= 0 in the high-rent part of their own history
  (a piecewise test by within-country rent tercile). And against life-cycle models WITH a below-market parental
  room (Kaplan; Ermisch), the kink is not distinctive at all: only against models with no coresidence option.
- **Design.** No internal holdout for the P tests (all unseen country-years); a matched-pair country split with the
  US forced into the explore half for any new E; every splice a segment fixed effect, no ratio-linking; rent-control
  robustness from a published coding; MDEs and forecast sheets published before the look.
- **Her decisions (2026-10-08):** scope BOTH (the OECD panel from the 1960s-70s as the test; the US from 1948 as a
  deep study with no verdict of its own); the floor measure from IPUMS-International 1955-1975 census samples (she
  is registering; the extract holds household-structure variables only, no labour/education/income/tenure, and
  goes to `longrun/data/ipums/`, gitignored, read only by the guarded loader); the regime-aware within-country
  test as the long-run distinctive test, pooled D1/D2 with no verdict.
- **PAUSED here (her call, 2026-10-08).** On disk: `longrun/PROTOCOL.md` and `longrun/FORECASTS.md`, the FIRST
  DRAFT, unrevised; `longrun/docs/protocol_review_draft1.md`, three reviewers' 34 findings on it, not yet worked
  in. Next: revise the protocol from those findings; build the long-run pipeline (guarded loaders, split, segments
  from documentation, the coverage-skeleton simulation, checks); show her the protocol; forecast sheets; tag
  `participation-L-freeze`; then fetch (incl. her IPUMS extract). No long-run value has been downloaded.
- **2026-10-09: protocol revised, pipeline built, code-reviewed (uncommitted, untagged).** `longrun/PROTOCOL.md` was
  revised on the 34 findings; `longrun/code`, `checks`, `data` (coverage, segments, split, skeleton) were built from
  metadata only; three code reviewers (fidelity, blinding, statistics) found 2 blockers, 16 major and 26 minor issues,
  fixed except where marked for her (`longrun/PROTOCOL.md` section 11, "Code review of 2026-10-09").
  - **INCIDENT: an IPUMS-I extract on disk before the tag.** `longrun/data/ipumsi_00001.csv.gz` (1,565,024,917 bytes,
    created 10:37, written 11:08; no DDI, no fetch-log record), outside `data/ipums/`, before the L tag (L9 says the
    extract is made after it). Its size suggests more than the frozen samples x 13 variables x ages 20-34. No agent
    opened it (name, size and times only). Its access time moved at 12:16 and 12:21 with no agent reading it
    (likely an antivirus scan; not attributable from here). The loader now refuses while it lies there; the gitignore
    covers it. **Her call:** where it goes (out of the repository), and whether it is kept; after the tag it is re-made
    or re-verified against the frozen sample IDs, variables and the 20-34 selection.
  - **L1 changed: the European cut is 1994, not 1996.** The European study's 1995-1996 rows were seen (its panel grid
    starts in 1995; its exploration's outputs hold 1995-1996 activity rows). Applied to all 26 European members. At L2
    this takes NL out of LR-K2 (9 countries: CA CL CO CR DE FR IL MX US; passes testability by one) and AT and IS out
    of the split, which was redrawn by its frozen rule: EXPLORE BE CA CL CO EL FR IE IT KR LU SE TR US; CONFIRM AU CH CR
    DE DK ES FI IL JP MX NL NZ PT UK. **Her confirmation asked:** cutting only the European explore countries would
    keep NL (LR-K2 at 10).
  - **Correction to the incident note:** the extract was made early on Claude's advice (2026-10-09: "get it all in
    one extract", including EMPSTAT, LABFORCE, SCHOOL, OWNERSHIP, MARST — the fuller variable list was Claude's,
    so the loader's 13-variable allowlist must become a read-only-these-columns rule). An agent read its column names
    (hours scout, about 12:16-12:21: "no hours variable"); its access time moved again at 13:50 (during the check
    runs). No values were read by anyone, as far as can be established.
- **Her decisions (2026-10-09, after the build):**
  1. **Floor measure:** Giuliano-Nunn ancestral family organisation becomes the MAIN floor measure for LR-K2 (all
     OECD countries: Southern Europe, Japan and Korea come back, roughly twice the countries); the IPUMS census
     measure F_L becomes a robustness run. Reason: with census F only 9-10 countries enter and Latin America carries
     57% of the identifying variation; every long-run MDE was above its European benchmark.
  2. **The extract:** kept, moved into `longrun/data/ipums/` (done 2026-10-09), fingerprint recorded in
     `longrun/data/ipums_extract_sha256.txt` (SHA-256 71121ee2...040a, 1,565,024,917 bytes), disclosed. No
     re-download. It already holds the post-1975 censuses, so it serves as Extract B (LR-C1) too.
  3. **European cut by what was examined:** explore countries of the European split end at 1994 (their 1995-96 rows
     were looked at); held-back countries end at 1996 (downloaded, never examined). NL stays in.
- **PAUSED here (her call, 2026-10-09).** Next, in order:
  1. Amend `longrun/PROTOCOL.md` for decisions 1-3. G-N: the exact variable and ancestry weighting from its codebook;
     a pre-freeze validation against the European SILC coresidence F_c (already seen) and nothing else; H recomputed;
     coverage, split (frozen rule), skeleton and synthetic look rerun.
  2. Code: F from G-N; F_L robustness; the loader reads only the household-structure columns of her fuller extract
     (usecols), accepts a pre-tag extract matching the recorded SHA-256, and still refuses to read before the tag;
     the European cut by half; the checks updated.
  3. The remaining L2 steps (below), an adversarial review of the amendment and code, then the forecast sheets and
     her go-ahead for the tag. Ask her to download the extract's DDI codebook (.xml) if the loader needs labels.
  - Before the tag (`longrun/checks/check_freeze_ready.py` lists them): the IPUMS file above (now moved); the L2 records (IPUMS
    age intervals for IE 1971, IL 1972, NL 1960/71; RELATE codes, household concept, GQ coding, sample kinds;
    Kholodilin's file; the school and coresidence segment rows; the JST and ILOSTAT masks); the scouts' folders and
    the European raw cache (her choice of place); her decisions on the stress nulls and a realised-H calibration
    (reported now, not in the verdict) and on naming LR-K2's identifying-variation shares in the model-level
    sentence; her Extract B decision (`longrun/data/decisions.json`); the European real-data run; the forecast
    sheets.

## The split (frozen with the P tag)

EXPLORE (16): BE BG CH EE FI FR HR HU IE IT LU LV MT PL PT SE.
CONFIRM (15): AT CY CZ DE DK EL ES IS LT NL NO RO SI SK UK.

## Next

1. Her go-ahead → tag `participation-P-freeze` (local; pushing is her call).
2. Fetch the explore half (`code/specs.py explore` writes `results/specs_explore.json`, the pre-look MDEs);
   explore freely on it; write at most five E in `code/e_specs.py`; tag `participation-E-freeze`.
3. The look: `code/confirm.py`, once; commit its result immediately.

## Code

- `code/eurostat.py` — the only door to data: JSON-stat fetch, cache, fetch log, and the blinding guard.
- `code/split.py` — the seeded matched-pair split (`data/split.json`).
- `code/inference.py` — restricted wild cluster bootstrap-t (Webb), CI by inversion, randomisation inference,
  G*, MDE. Validated in `code/simulate_inference.py` (`results/simulate_inference.json`).
- `code/build.py` — the variables of PROTOCOL sections 3 and 5 (`data/manifest.json` lists every query).
- `code/specs.py` — the tests, verdicts, leave-one-out qualifiers.
- `code/confirm.py` — the one look.
- `code/simulate_pipeline.py` — synthetic end-to-end runs (null, planted, opposite worlds; replications).
- `checks/check_guard.py`, `checks/check_inference.py`, `checks/check_protocol.py` — run from `participation/`
  with `../venv/Scripts/python.exe checks/<file>.py`.

## Log

1. **2026-10-08 — founded; the protocol.** Her question (how men's and women's participation, aging and
   retirement, schooling and youth unemployment are understood by the model), then her call to start from
   data with something to test against. Draft predictions written from the paper (`docs/protocol_draft.md`);
   one workflow ran five blind data scouts, three theory critics and a design critic in parallel (coverage
   only, no values); `PROTOCOL.md` written from their findings; a second workflow built the pipeline (guarded
   fetcher and split; inference validated for size, power, coverage; variables, tests, the look), three
   adversarial reviewers (protocol fidelity, blinding leaks, statistics) found 5 major and 21 minor issues, all
   fixed or decided. Decisions 6-7 amended the protocol before the freeze. Caught: the design half first
   accepted any population query (incl. the C-5 regressor) and the confirm guard could be opened by an E tag
   without a P tag — both closed before any outcome fetch.
