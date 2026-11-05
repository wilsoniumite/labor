# STATE — us-record (the backward model; resume point for the next session)

**Project:** the paper's model run through the US record, 1950–2025: a test the mechanism could fail, the clocks
measured, an attribution, and a 2025 starting point for the forward model in `../paths/`. The governing document is
`SPEC.md`; read it first.
**Collaboration:** same contract as the sibling threads: drafting and sequencing delegated to Claude, checks gate
absolutely, direct critique over validation; the decisions below are a veto window for her calls. Code in plain
functions, notebook-cell style; `tqdm` on any outer loop that takes more than a few seconds.
**The wall:** this repository is public. Public data only (FRED, BEA, the Fed's Z.1).
**State as of:** 2026-11-05. Phase 0 done: `SPEC.md` written and committed before any fitting. Nothing fitted, no new
data fetched.

## The three models

1. The pinning model, `../pinning/code/pinning_model.py`: the paper's.
2. **This thread**: the backward model, the pinning model against 75 years of US data.
3. The forward model with a crash, in `../paths/`: the complex model (`code/macro.py` and its layers) and the crash
   model (`code/global_crash.py`), today two pieces that do not read each other's results, to be joined. It takes its
   start and its clock from this thread (`SPEC.md` section 9).

## Decisions (veto window)

1. **US first** (her call, 2026-11-05), annual, 1950–2025: the window the effort accounts and the fork cover.
2. **Accuracy through simplicity** (her call, 2026-11-05): the paper's model with as few additions as the record
   forces; anything that does not do much is cut; credibility from few free numbers and untargeted facts rather than
   many holdout sets. One time split reported as a reading only.
3. **Aggregate participation only.** The participation thread's US series by sex and age stay unseen until its
   long-run freeze (`../participation/STATE.md`, "The long run"); women's entry enters as a shift backed out of the
   aggregate rate (addition B), not read from those series.
4. **The earn-its-place rule** (`SPEC.md` section 6): a component stays if removing it raises the misfit by at least 20%
   or takes a targeted series out of its band; set before fitting, revisable once at breakpoint B.
5. **The folder** is `us-record/`, a new thread; `../archive/long-record/` (seven centuries of English wages) is the
   method's precedent, not its base.

## Next

1. Phase 1, the data panel (`SPEC.md` section 8): the four targeted series and the measured inputs, annual
   1950–2025, each stored with source and manifest; the measurement equations written out; then breakpoint A.

## Log

1. **2026-11-05 — founded.** From her question in the session that unified the pinning model ("what do we even want
   from this model?"): the three-model layout (pinning; backward over 70 years; forward with a crash), US first, and
   simplicity as the discipline. `SPEC.md` written before any data or fit.
