# STATE — outlook (the case and the site's model; resume point for the next session)

**Project:** one coherent, current statement of what we think is happening as AI takes over paid work, with a model
run that puts numbers on it, for watch.wilsoniumite.com. `README.md` is the case; this file is how it was made and
what is open.
**Set:** 2026-11-13, from a clean slate, on her instruction: the thesis and the model rethought from what `paths/`
and seven weeks of the watcher's news had shown; one current case on the site, with no record there of earlier views.
**Collaboration:** as the sibling threads. Checks gate absolutely (`checks/check_outlook.py`, 17/17). She left the
case to Claude; every choice below is hers to veto with a word.
**The wall:** public data only, as everywhere in this repository.

## Why a new thread

`paths/` holds the engine (the crash model), the dated vintage and the splits tracker, and they stay there. Its case
(`paths/code/case.py`, of 25 September, restated to 28 October) and the long-run block on calibration (c) are records
now. What the evidence did to them, in short:

- **The dated calls missed.** The case had US unemployment at 4.24% in October (4.1%), the Riksbank cutting (it
  raised on 4 November), the Nasdaq 20% below its high by 8 November on the dot-com path at dot-com size (8%). Of the
  16 predictions of 8 October, 11 had moved away from their thresholds by 13 November and 2 toward.
- **The regime had the opposite sign.** The model had rates falling from the start and spending failing with wages;
  the data have inflation near 3%, central banks raising rates and long yields at twenty-year highs. The long-run
  block has no build-out phase: in it investment falls from the start.
- **The pace was set by hand.** A point of the workforce a year; the jobs data allow at most 0.22, and the trend is
  not distinguishable from zero.
- **Calibration (c) overstates site rent** (0.11 of GDP against a measured 0.03–0.05; the paper's review of
  3 November), and with it the long-run numbers the site led with.

## Design decisions (veto window)

1. **Keep the engine, replace the case.** The engine reproduces nine downturns and the dot-com bust out of sample;
   what failed was what was fed to it. Nothing in its equations or fit is changed. *Alternative:* a new model from
   scratch; it would have no such record.
2. **One input added to the engine's code**, `Shock.push`: inflation in the pipeline at the start. Without it core
   inflation falls from 3.0% to 2.1% in the first month and the Fed cuts through 2027 (3.4% by mid-2027), which is
   the call that failed. With it the Fed peaks at 4.1% in early 2027. Applied only where core inflation starts above
   target (US, euro area outside France): below target the engine's debt-deflation term would read a mild undershoot
   as heavier debt for years (France, Sweden, China). *Alternative:* a hybrid path of announced rates; needs sources
   the vintage does not hold.
3. **The pace: from the bound seen, doubling every two years, capped at a point a year.** The start is measured
   (the upper bound, so it overstates today's pace if anything); the doubling time and the cap are stated, not
   measured, and are the case's largest assumption: by 2032 the share out of work runs 5.8% to 10.1% between "as
   seen" and "doubling every year". *Alternatives on the page:* none, as seen, doubling every year.
4. **The exit share at the middle of its three bases** (0.59), not the highest (0.94, which rests on one month).
5. **The bust at half the dot-com crash's size**, on its measured path from the day of the high. Five weeks in, the
   Nasdaq's fall was about a quarter to a half of 2000's at the same day count; the watcher's own assessments had
   named the half-size bust as most likely since 7 October. Stated, not measured. *Alternatives on the page:* any
   size from none to twice, any speed, a later day.
6. **Robots not within the run.** They can do most physical tasks and are cost-competitive on very few (Anthropic,
   30 September 2026). `paths/` had them two years out. *Alternatives on the page:* from now to three years out.
7. **Policy responds to the run it is in.** Each lever starts the month after the region's own unemployment has
   risen by the rules' trigger (two points under today's rules), found per run by `global_crash.trigger_dates`. In
   `paths/` the levers started on dates fixed in the central run whatever the bust, so a run with no bust was
   stimulated and a severe one waited. In the case this puts the US response in April 2029.
8. **The regional paces at the engine's ratios to the US** (0.5 euro area and France, 0.6 Sweden, 0.8 China):
   stated in `paths/`, kept, unmeasured.
9. **The case is stated for the United States.** The engine's numbers for France and Sweden are overstated (no
   exchange rates; the debt-deflation term on a mild undershoot) and are shown on the model's page with that limit.
10. **No long-run block.** The site no longer shows fifteen-year paths of income shares; the paper's limiting
    results are stated as such.

## Where things stand

- `code/outlook.py`: the inputs (`seen`, `us_pace`, `push_paths`, `delay_of`), a run by its settings (`run`), its
  readings and paths, the runs around the case (`AROUND`), `results/outlook.json`.
- `checks/check_outlook.py`: 17/17. E1–E3 the engine and its one new input; I1–I5 the inputs; R1–R9 the results
  (R8 records the engine's upward drift with no shock at all).
- `paths/code/global_crash.py`: `Shock.push` added (six lines); `paths/checks/check_global_crash.py` 85/85 after it.
- The case's run: US unemployment 5.23% in 2027Q4, a first high of 6.2% in 2029Q1, 4.74% in 2030Q3, 7.42% in
  2032Q2; out of work 8.56% in 2032Q2, rising; the Fed's rate 4.13% in 2027Q1, 2.68% in 2028Q4, 1.75% in 2032Q2;
  the Sahm rule in July 2027; the four economies' output −2.33% at worst in the downturn (2029Q1) and −4.1% in the
  run's last month. A run's outcome in a word is read as the site's page reads it, on the run's months: the
  downturn is a recession, the run as a whole a deep one (it ends at its worst).
- The watcher and the site (`wilsoniumite/watch`, branch `claude/eloquent-gates-emehst` until merged) are on this
  case: the export and the page's engine with the pace, the inflation input and per-run levers (checked against
  the Python on 182 runs, to 1e-9); the seven points; sixteen predictions derived from the run
  (`docs/predictions-2026-11-13.md` there); the charter and the lens. The site builds from `main` of both
  repositories, so both branches are merged together.

## Next

1. **Merge and go live**: this branch and the watcher's into their `main`s (the watcher's `deploy/hal/README.md`
   has the steps and the log lines to expect). The first sweep after it writes the first assessment of this case.
2. **A measured doubling time for the pace.** Candidates: the share of firms using AI in production (Census BTOS),
   announced job cuts attributed to AI, entrants' hiring. Until then it is the case's largest stated assumption.
3. **The build-out as a model block:** investment demand, external funding and the long-term real rate, so that
   point 4 is computed and not only observed. The engine has no long rate.
4. **A floating exchange rate** for Sweden and the euro area, and the debt-deflation term on unexpected rather than
   below-target inflation: the two reasons the engine's European numbers are overstated. Both change the fit.
5. **Refresh the vintage** after the December data, and score the case's first quarter (2026Q4: unemployment 4.25%,
   the Fed's rate 4.02% on the quarter's average).

## Log

1. **2026-11-13 — the case set.** Her instruction (paraphrased): rewrite the thesis and the model from a clean
   slate; she has no fixed picture of the case and leaves it to Claude; one coherent current prediction on the site,
   without notes on what changed. Read first: `paths/STATE.md` and its record of the misses (Logs 40–44), the paper as
   polished 2–4 November and its review's finding on calibration (c), and the watcher's log of 24 September to
   13 November (327 flagged items, 13 assessments, the 16 predictions' readings). Built: `Shock.push`, this thread,
   the case's run and the runs around it. Decisions 1–10 above.
2. **2026-11-13 — the watcher and the site moved to the case.** In `wilsoniumite/watch`: the model export and the
   page's JavaScript engine on this module (`Shock.push`, the pace's paths, levers dated per run); the register's
   points and sixteen new predictions (US unemployment's signal by September 2027 from this run; the Nasdaq 20%
   below its high by 30 June 2027 on 2000's daily path at half size; the other downturn signals by their longest
   lag behind the unemployment signal in past downturns); the judge's charter and lens; every page of the site.
   Here: the run's outcome word read on months, as the page reads it (the case sits on the line: the four
   economies' output is 3.99% below capacity on the last quarter's average, 4.1% in the last month), and R7
   restated to what is found.
