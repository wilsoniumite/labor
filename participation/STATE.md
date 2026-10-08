# STATE — participation (resume point for the next session)

**Project:** what the paper's model says about who works — men and women, the young and the old, retirement,
time in school, youth unemployment — tested on data without letting the data write the test. Founded
2026-10-08 from the paper's Future Work paragraph on participation (her question; her call to start from the
data, with something to test against).
**Collaboration:** same contract as the sibling threads — drafting and sequencing delegated to Claude, checks
gate absolutely, direct critique over validation; the design decisions below are a veto window for her calls.
**The wall:** this repository is public. Public data only (Eurostat; OECD and ILO as named in the inventory).
**State as of:** 2026-10-08 — protocol written, reviewed and amended; pipeline built, adversarially reviewed and
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
