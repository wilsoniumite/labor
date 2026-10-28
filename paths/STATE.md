# STATE — paths (the dynamic model for risk; resume point for the next session)

**Project:** the paper's mechanism as paths over time, at speeds set by three clocks
(technology, recognition, institutions), coherent enough to stress a bank's balance sheet.
Founded 2026-09-24 from a risk question: what does a bank face if the world comes to see that
wages can no longer carry consumption? The first layer is the yield curve, because the rate
move under way in 2026 is not the supervisory parallel shock.
**Collaboration:** same contract as the sibling threads — drafting and sequencing delegated to
Claude, checks gate absolutely, direct critique over validation; the numbered design decisions
below are a veto window for her one-word calls.
**The wall:** this repository is public. Public data only (FRED, Statistics Sweden, the
Riksbank, the ECB). The bank-side application lives in an internal repository; nothing from it
is reproduced here, including the Swedish OIS measurements that motivated the curve layer —
their public counterparts are built here instead (US Treasuries; Swedish bills and bonds 1990–95 and 2021–26).
**State as of:** 2026-10-01. Built 2026-09-24: the curve layer (22/22), the US test, the openness principle, Sweden
1990–95, regime mixtures (12/12), the sovereign spread and its monitor (6/6), the macro block with calibrations (a)
and (b) (21/21), recognition as a mixture, reverse stress testing part 1, speed with the digestion history, the
forward-rate test, a stylised bank, the floor evidence (7/7), deposits against wages (9/9), the demand gap, the
household layer, the world crash model with two waves, care and its financing (exposure 20/20, financing 10/10). Built
2026-09-25: output without work (6/6), the pace (8/8), her case (11/11), the start pinned (global_crash 43/43). Built
2026-09-30 to 10-01, committed (b7df43c) and pushed 2026-10-01: **the machine chain measured** (`code/chains.py`,
23/23); **calibration (c)**, the chain at its measured size (`code/calibration_c.py`, `macro.central()`, 47/47); **the switch** — every
module on (c), (a) and (b) kept as named comparators (`check_macro_scenarios` 13/13, new; recognition 14/14, reverse
21/21, regime_digestion 11/11, speed 18/18, bank 24/24, demand 23/23, households 25/25); **the October bust**
(`code/october.py`, 40/40). **2026-10-01, on her delegation** (she left most of it to Claude and asked for one version,
so that it is easier to keep track of): her open calls taken by Claude, each recorded with its
reason (decisions 20, 21, 27, 32, 33, 39, 41–43, 47, 48 and 51; 52 new), and one version made — one dating (index 0 =
2026Q3, the state measured to September 2026; her case 12/12), the October central on the corporate spread alone with
hands tied read on four quarters' headline (october 42/42), decision 27 on Brent's level (log 35). All 23 batteries
green on 2026-10-01, stderr empty (check_october's W1 and W4 run the private watch repository's own code from a
checkout beside this one, and its D2 and check_case's K12 compare with git history: without them those parts are
reported, not gated; README). Committed and pushed 2026-10-01, in the order of Next 13; next, refit the bridges on
(c) (Next, first); part 2 — the bank's own balance sheet on these behaviours — stays on the internal side.
**Since:** 2026-10-12 and 13, the splits tracker (`SPLITS.md`, `code/splits.py`, `checks/check_splits.py` 25/25; the
unit under Where things stand, decisions 53-65, Next 14, Log 37-39), frozen 2026-10-13 (tag `paths-splits-freeze`).
**2026-10-26, the redo, under way** (Log 40; on her delegation: well calibrated, on new data, fitting the pop now seen,
simpler): the record before the FOMC (Log 40); the crash model's 2008–10 sign error fixed and the results regenerated,
the dot-com bust added as an out-of-sample check, the October bust retired to the tag `paths-pre-signfix` (Log 41);
her case, the central run and the website's model on one dated vintage, with the bust on the 2000–02 bust's measured
path from today's peak and the build-out measured as information processing equipment (Log 42; decisions 66-68);
four units nothing read cut, at the tag `paths-pre-cuts` (Log 43); the review's fixes — the bust's sizes measured and
dated from the peak's day, the Nasdaq rule on 2000's daily path, the website's wording, no US premium in the case
(Log 44; decision 69); France a region of its own, in a monetary union with the rest of the euro area, its
government's spread over Germany's passed to French borrowers and its banks, and the euro area's premium France's (Log
45; decisions 70-71). All 23 batteries green on 2026-10-27 (Logs 44-45 list the narrow passes).
**2026-10-27, the bridges refit on (c)** (Next, first; Log 46; decisions 72-79, hers to review): r* keyed to investment,
owners' saving and deficits on one evidence-based scale, the fiscal start at Sweden's measured primary balance, household
benefits following wages, rigid money wages falling at a limited pace; the comparators (a) and (b) on their own bridges.
On (c) the neutral rate now falls from the start at every speed (−3.0 / −5.3 / −5.3% at year 15), the curve falls a long
way through recognition, and both of the bank's branches fall. Entries below that predate it carry a "→ On the refit"
note where their findings moved. All 23 batteries green on 2026-10-27 after it, stderr empty; committed, not pushed
(watch first, then this repository).

## Design principle — stay open to a more extreme path (her call, 2026-09-24)

Better to be open about what happens than confident it will look like any time before. So:
**structure fixed, behaviour swappable.** The identities stay (the curve as the average expected
policy path plus a term premium; the paper's price system). Every behavioural piece — the policy
rule, how the market learns, how households and banks respond — is a named, replaceable component
with at least one extreme alternative. History calibrates only the *normal* version of each; the
paper's mechanism sets the size and direction of the drivers; scenarios are generated by reverse
stress testing (which path breaks the bank, then can the mechanism produce it); past extremes are
references, not templates. What "extreme" can mean — different in kind, not only in size:
1. the destination ratchets — a large one-way move for years (up: capex and fiscal strain; down:
   wage-financed demand shrinking), not a cycle around a stable level;
2. the central bank leaves the rule — will not deliver what is priced, cannot (currency defence,
   bank protection), or serves the fiscal need (a yield cap, where the curve stops being an
   expectation at all);
3. the front stops anchoring the curve — government bonds decouple from OIS, the term premium
   dominates, the interbank basis blows out;
4. speed — repricing in days, volatility regimes beyond March 2026; and her sharper version
   (2026-09-24): markets run on cognitive labour at a human speed, and if AI comes to be trusted to
   guide investment that bottleneck lifts — the recognition clock driven by the technology clock;
5. correlations flip — rates up with unemployment up;
6. feedback and thresholds — debt service to consumption to growth, house prices to collateral
   to lending, bank funding to basis: nothing moves, then everything flips at once.
The historical reading below ("late in the pricing phase") holds only if the market's destination
is right; in an extreme path the destination is what is wrong.

## Where things stand

- **`code/curve.py` — the curve layer.** The market's expected policy path is a two-stage
  cascade: policy `r0` moves toward a cycle target `m0` at speed `k1`; the target drifts to the
  long-run destination `rbar` at `k2`. The zero curve is the path's average plus an additive
  term premium; a delay pins the front (policy holds until the next priced move); an
  interbank basis sits on top. Closed forms for zeros and forwards; the modes (what a unit
  move in each state does to the curve); the timing share `tau`; a stepwise policy rule; the
  six supervisory shapes for comparison.
- **The theory, machine-checked** (`checks/check_curve.py`, 19/19 since 2026-10-26; 22/22 with the stylised cycle's C1-C3):
  - the cascade solves its two-stage dynamics, and the zero curve is its average (S1–S3);
  - **timing:** in the one-speed curve `dz/dk = (rbar − r0)/k · (L(kT) − e^{−kT})` — the
    Nelson–Siegel curvature loading scaled by the gap (S4, N3). A revision of *when* policy
    arrives moves the curve in a hump whose size is the slope; on a flat curve it cannot occur
    (N4, N5). The hump peaks at maturity 1.793/k (S8, N6);
  - equal speeds give Nelson–Siegel exactly — level `rbar`, slope `r0 − rbar`, curvature
    `m0 − rbar` — the cascade behind the arbitrage-free Nelson–Siegel model (Christensen,
    Diebold and Rudebusch 2011) (S5, N8); `m0 = rbar` gives the one-speed curve (S6);
  - the timing share rises with speed from a floor of `(1.5 − 1/24)/(7.5 − 1/24) ≈ 0.196`
    toward 1; readings below the floor need a delay, and a priced hold of two years or more
    gives exactly 0 (N7, N7b) — so a measured `tau` near 0 means the market priced a long hold;
  - the stylised cycle through the three clocks runs **hump while the market prices the
    moves (front pinned) → front catches up as policy delivers → front-heavy, near-parallel
    over the whole cycle** (C1–C3; parallel R² 0.94). `code/cycle.py` and C1–C3 are a record since 2026-10-26, at
    the tag `paths-pre-cuts` (Log 43); the US cycle below shows the same sequence in the data.
- **`code/us_modes.py` — the public test on a second cycle** (FRED, constant-maturity yields as
  zero proxies; a record since 2026-10-26, at the tag `paths-pre-cuts`: nothing read its results, and the watcher
  computes the timing share daily; Log 43):

  | Phase | Fed funds | 1M | 2Y | 10Y | 30Y | Closest SOT shape | `tau` |
  |---|---|---|---|---|---|---|---|
  | A pricing, Sep 21 → Feb 22 | 0 | −2 | **+138** | +74 | +45 | parallel up, 0.78 | 0.16 → 0.95 |
  | B delivery, Mar → Dec 22 | +375 | **+367** | +228 | +130 | +106 | short up, 0.94 | 1.18 → 0.16 |
  | C to the peak, Dec 22 → Jul 23 | +125 | +155 | +59 | +37 | +42 | short up, 0.90 | 0.16 → 0.65 |
  | Whole cycle, Sep 21 → Jul 23 | +500 | +542 | +462 | +255 | +202 | parallel up, 0.90 | 0.16 → 0.65 |
  | D hold, Jul 23 → Sep 24 | +25 | −41 | −123 | −21 | +2 | short down, 0.74 | 0.65 → 1.56 |
  | E cutting, Sep 24 → Dec 25 | −144 | −126 | −5 | +48 | +82 | reverse flattener, 0.94 | 1.56 → −0.39 |
  | F last 12 months, to 2026-09-22 | −21 | −21 | +114 | +80 | +53 | parallel up, 0.72 | −1.52 → 0.91 |

  The US cycle ran the same sequence as the stylised one: a pricing hump with the front
  pinned, the front catching up on delivery, a front-heavy near-parallel whole. At the peak
  the long end rose (~40 bp) and then the **timing mode re-armed in reverse**: phase D is a
  cuts-pricing hump with the front nearly still. The last twelve months are a pricing hump
  again, `tau` at 0.91.
- **`code/se_1990s.py` — an extreme in the record: Sweden 1990–95** (Riksbank SWEA API, public;
  `results/se_1990s.json`, `figures/fig_se_1990s.png`; bills and bonds as zero proxies):
  - **E1 defending the krona, 8 → 18 Sep 1992** (marginal rate 16 → 500%): 1M bill +7,700 bp (to
    99%), 3M +620, 12M +140, while 2Y −73 and 10Y −8. No supervisory shape comes close (best R²
    0.34). On the crisis day the curve ran spike → plateau → lower (1M 99%, 3–12M 23–31%, 10Y
    11.5%): the one-speed curve misses by 1,069 bp RMSE and the two-stage cascade by 296 bp with
    parameters at their bounds, against 17 bp on calm 1991–92 days. **Corrected (log 4):** the
    first reading here — "the market priced a mixture of regimes that no single smooth path can
    draw" — overreached. The 1M bill on 17–18 Sep implies a 1M→3M forward of −3.0% and −13.5%,
    which no expected path of a non-negative policy rate can produce, mixture or not: that quote
    sits outside what averaging can price (a disorderly 1M bill market). Without it, the two-stage
    cascade fits the 18th to 25 bp and the 17th to 111 bp, pricing the defence at 23–34% for a few
    months and ~10% beyond. The day's curve does not by itself require a mixture; the evidence for
    one is the jump at resolution (E3).
  - **E3 the float, one day (19 Nov 1992):** 1M −140, 3M −170, 12M −160, **2Y −210, 5Y −178, 10Y
    −101 bp** with the policy rate unchanged (11.5%; raised to 12.5% the next day) — the largest
    one-day moves of 1990–95 at both 2Y and 10Y. The regime resolved and the whole curve jumped.
  - **E3–E4 the float (19 Nov 1992) and 1993:** the whole curve fell; over 1993 by 270–340 bp at
    every maturity, **parallel down R² 0.99** — the only move of near-equal size at every maturity
    in any episode measured so far (the whole-cycle moves fit a parallel shape but are front-heavy),
    and it came after a regime break, when the anchor itself changed. `[inferred]` A
    destination that can **jump**, not only drift.
  - **E5 the fiscal bond crash, Jan → Sep 1994:** 5–10Y +450 bp with the policy rate −30 bp; of
    the 10Y rise, **+259 bp was the widening of the spread over German yields** (116 → 375 bp).
    The shape was ordinary (one-speed RMSE 16 bp); the extreme was size and source, and the curve
    showed no visible destination (the two-stage fit ran to its bound, still rising at 10Y).
    `[inferred]` An **anchor-failure** state: a sovereign spread over the common rate.
  - **Whole, Jun 1992 → Jun 1995:** front −233 bp, 10Y +127; spread over Germany 171 → 407 bp;
    the trade-weighted krona index +33.5% (the krona about a quarter weaker).
  - **Speed, same public series, 1990–95 against 2021–26** (99th percentile of daily moves): 3M
    **200 vs 17 bp** (12×), 2Y 52 vs 16, 10Y 40 vs 16; the largest single day at 3M 900 vs 51 bp.
- **`code/regimes.py` — expectations as a mixture of regimes** (checks `checks/check_regimes.py`,
  12/12). The curve the market shows is an average over worlds: each regime carries its own
  expected policy path and term premium (a `CurveState`), weighted per horizon — *static* (the
  regime is decided, only unknown: weights `π_j`) or *arrival* (a status quo holds until a new
  regime arrives, with eventual probability `p` and hazard `h`: `w_new(s) = p (1 − e^{−hs})`).
  Two events then move the curve with no policy move at all:
  - **recognition** — the market's `p` rises. The move is `(1/T) ∫ (1 − e^{−hs}) (f_new − f_old) ds`
    per unit of `p` (S2, N4): ~0 at the front and growing along the curve when the new world
    differs in destination (N5); the hazard sets how far out it bites (N6: the 2Y's share of the
    30Y move is 0.09, 0.24, 0.33 at `h` = 0.2, 1, 5 a year). Waking up moves the back of the curve
    first;
  - **resolution** — uncertainty ends and the curve jumps to one world's own curve:
    `(1 − π_B)(z_B − z_A)` for two static regimes (S3). Resolution to a **re-anchored** world is
    exactly parallel at every maturity (N7); to a world that differs only in timing it is a hump
    (N8). This is the mechanism behind E3 and E4: the one near-equal move in the record came when
    the anchor changed;
  - and a corollary for risk: two distant worlds can show an ordinary curve — 50/50 on 1% and 5%
    is flat at 3% with ±200 bp waiting in either resolution (N9). The curve alone does not show
    the size of the move it is hiding.
  `code/regimes_demo.py` (**stylised, not calibrated**; a record since 2026-10-26, at the tag `paths-pre-cuts`): recognition
  toward a higher-rate world (capex, fiscal strain) and a lower-rate world (wage-financed demand
  shrinking); two worlds behind one calm curve with ±112 bp at 2Y and ±186 bp at 10Y waiting; where
  recognition bites for different hazards.
- **`code/sovereign.py` — the anchor-failure state** (checks `checks/check_sovereign.py`, 6/6).
  A government's curve is the common curve plus a spread; the spread is the average expected
  loss rate (default intensity × loss) plus a convenience term, the loss path reusing the curve
  layer's cascade and fiscal regimes reusing `regimes.py`. It never moves the common curve, so
  the six supervisory rate shocks cannot see it (N3). A crunch expected to pass humps or inverts
  the spread curve; a slow erosion of the tax base slopes it up (N4). Recognising a fiscal regime
  moves spreads from the back, like recognition on the common curve (N5). A safe haven losing its
  convenience value moves the whole government curve in parallel with no default risk at all
  (N6).
- **`code/sovereign_monitor.py` — is the anchor failing now?** (a record since 2026-10-26, at the tag `paths-pre-cuts`:
  the watcher computes the same spreads and both falsifiers every day, anchor.fr.crunch and anchor.contagion; Log 43.
  Riksbank SWEA API, public; the cache stays in `cache/riksbank/`; spreads over the German
  benchmark of the same maturity, latest 2026-09-23):
  - **France +110 bp at 10Y — its widest since at least 2019, set on the latest day**; +34 bp in
    three months, +29 in twelve, with the 10Y widening 15 bp more than the 5Y: widening from the
    back, the erosion shape. The Netherlands (+7, −9 over twelve months) and Finland (+30, −8) are
    tightening, so it is French, not euro-wide.
  - Over other currencies (policy and currency included): Sweden −34 bp (through Germany; 25 bp
    tighter on the year), the UK +182, the US +155 (+19).
  - **Sweden 1994** over Germany: 5Y 114 → 359 bp, 10Y 116 → 375 bp. The one anchor failure in
    the record lifted the whole spread curve nearly level (+245 and +259), not only its back.
  - `[inferred]` The 2026 move sits on the common curve (timing: the US test here, `tau` 0.91); anchor failure so far is confined to one large sovereign and is
    shaped like erosion, with no broad fiscal repricing in public spreads. **Falsifiers:** the
    Netherlands and Finland widen with France; or the widening reaches the 5Y as much as the 10Y
    (a crunch, not erosion).
  - **Read again 2026-10-26** (the monitor's method on the watcher's SWEA series, latest 23 Oct; Log 40): France 166 bp
    at 10Y, 129 at 5Y. The shape has moved from erosion towards level. Since the reading above (23 Sep) the 5Y widened
    +61.9 against the 10Y's +56.6, and since 30 Sep +44.5 against +38.2; over three months +82.5 against +85.7, over
    twelve +78.0 against +86.4. The second falsifier is read on three months from now on (the window of the watcher's
    rules): **not met, but nearly level** (3 bp apart, against 15 at the first reading). The first falsifier is not
    met: the Netherlands +3.8 and Finland +9.6 at 10Y since 23 Sep (both, as written; the watcher's rule fires on
    either). Still French: the Netherlands at 11 bp and Finland at 40.
- **`code/macro.py` — the macro block** (checks `checks/check_macro.py`, 21/21 with (b)'s A1–A7; 14/14 at first).
  - **Structure: the paper's Appendix B, SSRN version of 2026-09-23** — the basket priced into
    participation, space scaling with output. ⚠ The repository's `pinning/` copy (main.tex of
    2026-09-21 and `checks/check_interior.py`) carries an older, different Appendix B (it solves to
    x 0.968, v 0.598, Y 18.5); the SSRN text cites a `check_interior.py` that is not in the
    repository. The macro block reproduces every SSRN figure to five decimals (P1: x* 0.86315, v
    0.54344, Y 7.88061, n 1.34338, final-task hours 1.07846, machine hours 0.26492, support 5.44630)
    and the paper's automation sequence (P2).
  - **Dynamics: quasi-static.** A technology clock (logistic in time) moves capability `eta` (task
    automation) and the labour in a machine-service hour `lambda` (recursive automation); each
    date is an equilibrium — no build lags, no adjustment costs.
  - **Calibration of the normal case** (her call (a), 2026-09-24): labour share 0.47 (the paper's
    full-chain human-effort share, Figure 7), employment 0.60, 3 support baskets of output per
    person (the basket as a subsistence bundle), the site 13% of the basket (the land part of a
    third-of-spending shelter, at the paper's 30–50% land shares). Exact fit with machines up to
    50× better than people on the easiest task (`g0` 0.02) and a convex schedule (`k` 4.83). Why
    the first targets failed: in a two-factor economy every krona not paid to hours is land rent,
    and Appendix B's space is pure site — a 33% shelter share makes a third of income site rent
    before any machine. **What the benchmark cannot separate:** the machine chains' land, 0.40 of
    income, also stands in for capital income (depreciation, interest, profits). Next unit (b)
    splits it.
    → The central is (c) since 2026-09-30 (decisions 31–37); (a) and (b) stay as named comparators.
  - **Bridges** (behaviour; named illustrative defaults, not estimates): nominal — the basket held
    on its target, so goods, shelter and wages inflate at the target plus their real change
    against it; fiscal — wage and non-wage taxes, spending, a public share of dependants' support;
    neutral rate — up with the pace of tasks moving to machines, down as income shifts to owners
    who save more, up with deficits; policy — the desired rate delivered by the curve layer's
    stepwise rule, with an effective lower bound; premia — term premium and sovereign loss from
    debt above thresholds.
    → On the refit (2026-10-27, Log 46; decisions 72-75): neutral rate — down as replacement investment / income falls
    and as income moves to owners who save more of it, up with primary deficits private saving does not offset, all at
    one evidence-based scale (0.3 pp per point of income); fiscal — the wage tax set so the start runs Sweden's measured
    primary deficit (0.16% of income).
  - **Deep automation at three speeds** (`code/macro_scenarios.py`, `results/macro_scenarios.json`,
    `figures/fig_macro_scenarios.png`; gated since 2026-09-30 by `checks/check_macro_scenarios.py`, 13/13; capability
    1 → 0.04, lambda to a fifth of its own start). **Restated on (c)'s central (2026-09-30), with (a) beside it — the
    pre-switch run, kept in `comparators.a`; (b) in `comparators.b`.** Labour's share (Figure 7 basis) falls at the
    technology clock's speed, halving in year 13.25 / 7.75 / 3.75 (slow / medium / fast; (a) 14.75 / 8.5 / 3.75);
    fast, 0.47 → 0.04 by year 6. **The real wage in baskets never rises on (c)**: its peak is the start at every speed
    and on both roots; medium 2.77 → 0.67, ending at x0.24 of its start (slow x0.58, fast x0.23). On (a) it first
    rose, then fell — a peak near 2.43 (x1.034, medium, year 6.25), ending x0.52; (b) x1.030 then x0.53 — the paper's
    two bounds in turn; on (c) cheaper goods never outrun site rent. Not a g0 effect: (b) at g0 0.01 still rises first
    (x1.014 / x1.237 by root); of the 22 (c) variants only the measured-site high root rises first (x1.092 at year
    7.75). The fork is sharper: at medium speed shelter inflation peaks at +28.7% a year and goods at −25.1% ((a)
    −17.1), fast +79.9% / −77.6%, with the basket on target. **The neutral rate's build-out hump survives only on the
    fast path, and smaller**: 0.76 → 1.35 → −0.13% ((a) 0.76 → 1.97 → −0.30); at medium and slow speed r* never rises
    above its start (medium 0.76 → −0.10; (a) 0.77 → 0.94 → −0.27). These are readouts of bridges tuned on (b): the
    capex channel is keyed to the pace of tasks moving to machines, while (c)'s own investment / income falls from the
    start (medium 0.178 → 0.045). Keyed to investment / income instead (a readout only; decision 39), r* never rises
    at any speed on either root and ends 0.50 / 0.55 / 0.53 pp below the pace-keyed r* at the bridge's converted scale
    (0.0394, the scale demand and bank use) and 4.57 / 7.99 / 8.07 pp at the demand layer's (0.6); on (b), at a fixed
    return, investment / income first rises (medium 0.239 → 0.245 at year 6) and the readout rises 15.9 bp at the
    demand-layer scale, none at the bridge's. **The fiscal base erodes faster**: the wage-tax share of revenue falls
    0.83 → 0.13 (medium; (a) 0.78 → 0.18) and debt reaches 121% of income by year 15 at medium speed and 187% fast
    ((a) 71% and 124%). (c) starts in surplus (−2.61% of income against (b)'s −0.10, because tau_w 0.40 falls on all
    wages, 0.554 of income), so debt first falls, 40 → about 32% by year 6 at medium speed (29 slow); re-centred to
    (b)'s start (tau_w 0.3547; `sensitivity_fiscal_start`) it is higher — 81 / 135 / 192% slow / medium / fast — so
    the surplus makes the finding
    milder, not harsher (decision 42). On (a), a mandate that leaves out shelter would want about −8% while goods
    deflate (B5); delivery stops at the lower bound.
    → On the refit (Log 46): r*'s highest point is the start at every speed, on both roots — no hump — and it ends at
    −3.0 / −5.3 / −5.3% (slow / medium / fast; high root −3.1 / −5.2 / −5.3); policy reaches the floor by year 10 at the
    medium speed. Debt rises from the start (a 0.16% primary deficit, tau_w 0.35) to 75 / 110 / 142% at year 15 (high
    root 64 / 94 / 124%); the surplus start (now the sensitivity) would end it at 52 / 100 / 140%. Keyed back to the pace
    of tasks (the readout), r* ends 2.4-4.0 points higher and still never rises a tenth of a point.
- **(b) Produced capital with an interest cost** (her call, 2026-09-24; checks A1–A7 in `checks/check_macro.py`, now
  21/21; `results/capital_feedback.json`, `figures/fig_capital_feedback.png`). Machines as a stock at the paper's
  Appendix A.4 user cost — a service unit costs (required return + depreciation) × a machine's build cost — so
  interest on machine capital becomes a third income; at return 0 and depreciation 1 the core is Appendix B exactly
  (A3). Calibration (b): 5.75% required return (0.75% real + a 5% premium), 8% depreciation, the same four targets hit
  exactly; the machine chains' 0.40 splits into **land 0.23 and interest 0.17**, with an implied capital stock of
  2.98× income (public fixed capital-to-GDP is about 3; housing structures sit inside this model's machine stock,
  since its space is pure site). Findings, restated on (c) since 2026-09-30 (`results/capital_feedback.json` now holds
  (c)'s central, with (b) in `comparator_b`; check_macro's A-checks still gate (b), `check_macro_scenarios` F7–F9 gate
  (c)):
  - **Under deep automation capital does not capture the gains; the fixed site does — more so on (c).** Along the
    medium path with the return following r*, interest falls 0.258 → 0.060 of income, machine-chain land 0.059 → 0.037
    and labour (all wages) 0.554 → 0.033, while the housing site rises 0.130 → **0.870** ((b): interest 0.17 → 0.08,
    chain land 0.23 → 0.13, labour → 0.07, the site 0.13 → 0.73). Produced capital cheapens with the technology; the
    non-produced input is what the income runs to. Part of "more so" is the open reading's import-as-land channel: the
    chain's imported content (0.559 of sigma_V) is modelled as chain land drawn from the endowment the housing site
    shares, and the chain's share of land rent falls 0.311 → 0.041 ((b) 0.637 → 0.148; medium path, return following
    r*); that channel's direction on the paths is open (decision 34).
  - **Rates feed back more strongly on (c) than on (b), still under a point of tasks.** +100 bp on the required return
    raises labour's share 1.55 / 1.14 pp at the start (all wages, low / high root; (b) 0.48 / 0.44); a sustained +200
    bp raises it by up to 2.98 pp (2.90 on the Figure 7 basis; (b) 1.57), about twice (b)'s, moves 0.61 pp of tasks
    back to people ((b) 0.34) and delays the medium path 18.9 weeks at year 6 ((b) 3.9). The gate (F8) is relative —
    more than (b), by over half as much again on labour's share and three times and more on the delay — not a claim
    of size. The response scales with 1/sigma_V (3.03 against (b)'s 1.05), and sigma's construction is open (decision
    34). "Monetary policy has little leverage over the automation margin" holds on (b); on (c) the leverage is larger
    but a sustained +200 bp still moves under a point of tasks, within the rate headroom (7.18 pp), past which there is
    no land-scarce equilibrium.
  - **The loop's lag phase shrinks to negligible.** With the return following the economy's own real rate (one-year
    half-life, decision 15), r* barely rises on (c)'s medium path (the return +0.003 pp at most; (b) +0.144), so
    automation runs behind the fixed-return path only in years 0.5–2.5, by at most 0.0006 pp of tasks (year 1.25; (b)
    years 0.5–8.75, at most 0.013 pp), then ahead: +0.23 pp of tasks by year 15 ((b) +0.14), correlation −1.00. The
    down-phase turn remains — cheaper capital speeds automation, owners' income rises, the neutral rate falls further
    — without the early lag. (The check's gate is the return's rise below 0.01 pp, a threshold, not zero.)
  → On the refit (Log 46): with the return following the refit's r*, which never rises, there is no lag phase at all;
    automation runs ahead from the start, 1.90 points of tasks by year 15; at year 15 interest 0.018, machine-chain land
    0.044, the site 0.924 and labour 0.014 of income; +200 bp delays the medium path 19.3 weeks and raises labour's share
    up to 3.24 points (3.18 on the Figure 7 basis).
- **The machine chain, measured** (her question, 2026-09-30: is the paths model's theta off?; `code/chains.py`,
  `results/chains.json`, `figures/fig_chains.png`, `checks/check_chains.py` 23/23). Publishers' own files only: BEA's
  input-output tables (the λ thread's cached release, data to 2023), Fixed Assets, GDP by industry and the NIPA flat
  file; OEWS for wage percentiles. Built on the λ thread's engine
  (`progress_and_prosperity/lambda/code/compute_family_a.py`), read-only: the thread's narrow / medium / broad series
  reproduce to 1.7e-16 in every year 1997–2023 before anything new is computed (C1), and an independent path from the
  raw Use and Make files, importing neither engine, reproduces the targets to 2.5e-7 (C20). Stated as found, 2023
  (decisions 28–30):
  - **Labour's full-chain share of a machine's build cost** (theta; tot = imports priced at US cost shares / dom /
    domp = US labour only): machinery (333) 0.540 / 0.449 / 0.292; computers and electronics (334) 0.557 / 0.503 /
    0.232; electrical (335) 0.540 / 0.449 / 0.220; software publishing (511) 0.438 / 0.426 / 0.422; data processing
    (514) 0.411 / 0.393 / 0.392; computer systems design (5415) 0.809 / 0.794 / 0.749; rental and leasing (532RL)
    0.341. The investment-weighted machinery + software set is 0.617 tot (0.546–0.617 across scopes). The bundle
    calibration (c) reads — equipment, IPP and private structures, all commodities — is 0.569 tot, 0.470 domp.
  - **The bundle's cost split** (tot / domp): compensation 0.569 / 0.470, consumption of fixed capital 0.154 / 0.114,
    taxes 0.047 / 0.038, net operating surplus 0.231 / 0.193, imported content 0 / 0.185. NOS bounds the fixed-rent
    share sigma from above (it also holds net interest, profits and proprietors' income): 0.231 closed (tot), 0.378
    open (domp, with imported content). The closure multiplier 1 + theta/sigma is at least 1/(1 − theta) for any
    sigma: 2.32 tot, 1.89 domp. The chain employs 18.3% of US compensation (tot; 15.1% domp; 12.3–13.6% of hours,
    domp, FTE to bridged).
  - **Hours of machine-chain labour per hour a machine replaces**, by wage percentile (the machinery + software set,
    service basis at rho 0.0575, bridged to hours worked): P10 0.165, P25 0.202, P50 0.273, P75 0.437, P90 0.689
    (unbridged FTE basis 0.149–0.623; asset basis 0.21–0.87). Each hour a machine replaces at the median still employs
    a quarter to a third of an hour in the chain.
  - **Against the model, like for like** (`model_vs_data`): the data's labour share of build cost is 34 times (a)'s
    and 272 times (b)'s on the asset basis (29 / 323 traced); the chain's share of compensation 8 / 159 times at the
    bundle's scope (2.6 / 51 for the set alone). (a) and (b) treat machines as almost free of labour (theta_V 0.018 /
    0.0023; the chain 2.3% / 0.1% of hours).
  - Caveats, each stated in the file: consumption of fixed capital capped at gross operating surplus (125
    industry-years capped, 18 on a fallback; at most 0.020 of the bundle's dollar); the I-O release (2024) older than
    the Fixed Assets and GDP-by-industry releases (2026); the thread's import convention (BEA's domestic-use
    convention lowers domp theta 0.470 → 0.459); employees' compensation only (proprietors' labour sits in NOS); stock
    options in compensation around 2000; the hours bridge borrowed from the medium set; robots not separable at the
    2017 detail; thresholds of C2, C6, C12, C15 and C20 set after seeing the data, flagged.
- **Calibration (c): the machine chain at its measured size** (the answer to her question; `macro.calibrate_c`,
  `macro.calibrate_roots`, `macro.central()`; `code/calibration_c.py`, `results/calibration_c.json`,
  `figures/fig_calibration_c.png`, `checks/check_calibration_c.py` 47/47). Appendix A.4 needed no new equation: the
  solver now searches up to the machine chain's ceiling (tasks where a machine-service hour would embody an hour or
  more are closed to machines — A.1's capability, A.4's positive denominator) instead of asserting at x = 1, and
  raises `NoEquilibrium` past it; the legacy solve is reproduced bit for bit on the paper's instance, (a), (b), (b)'s
  +200 bp path and 60 random economies (N1–N4), and the 20 earlier batteries printed byte-identical stdout across the
  change. Seven targets hit exactly (residuals at most 2.2e-16): her four (labour 0.47 on the Figure 7 basis,
  participation 0.60, 3 baskets a person, the site 13% of the basket) and the chain's theta_V, chain share and
  fixed-rent share sigma_V.
  - **The central reading is the open one** (decision 31): US labour throughout — her 0.47 is BEA WP2026-01's human
    effort, which keeps foreign content in its own bucket; theta_V 0.470 and the chain share 0.151 on domp — with the
    investment chain's imported content (0.185 of build cost) a fixed-quantity cost, in the model part of the chain's
    land. sigma_V = imports + NOS − CFC × rho/delta_chain, a fixed point: 0.330 (decision 34). delta 0.0522 (BEA Fixed
    Assets, all fixed assets, 2023; decision 36); rho 0.0755 an outcome, inside the NIPA return band 0.068–0.088; g0
    0.01 (decision 33). Two roots in k fit every target: 5.66 (low, the main reading) and 13.65 (high; decision 32);
    x* 0.830, the ceiling 0.914 / 0.866. Untargeted, on GDP net of the chain's imported content: compensation 0.483 of
    GDP (NIPA 0.512), CFC 0.155 (0.164), capital 2.98 times GDP (3.15); the net basis was adopted after seeing the
    data (on gross GDP compensation is 0.470), flagged in the battery.
  - **The closure multiplier is 2.42** (d ln(w/r)/d ln gamma at a fixed return; (b) 1.002): when labour is a large
    part of a machine's cost, cheaper labour makes machines cheaper, so the wage must fall further to hold the task
    margin; its floor for any sigma is 1/(1 − theta) = 1.89. **The rate headroom is 7.18 / 7.85 pp** (low / high root;
    (b) 20 or more): past it there is no land-scarce equilibrium. Headroom and the multiplier are one 1/sigma object:
    an economy that survives a sustained +5 pp rise in its required return has sigma at least 0.243 / 0.219
    (multiplier at most 2.94 / 3.15; participation at year 15 then 0.205 / 0.300), so evidence of that tolerance would
    move every (c) result toward the mild end. Headroom scales with delta (24.6 pp at the equipment + IPP delta).
  - **Findings, medium path, low / high root, root for root against (b):** participation 0.538 / 0.561 at year 6 and
    0.231 / 0.341 at year 15 ((b) 0.611 / 0.629 and 0.399 / 0.490); **the real wage in baskets never rises** — its
    peak is the start — and ends at 0.241 / 0.406 of it ((b) rises to x1.03 / x1.11 by years 6 / 7.25 and ends at
    0.526 / 0.717); w/r ends at 0.036 / 0.065 of its start ((b) 0.096 / 0.140); labour's share (Figure 7 basis) halves
    at year 7.75 / 8.75 ((b) 8.75 / 10.0). Like for like at g0 0.01 ((b) 0.371 / 0.587 at year 15), g0 explains 0.028
    (16.5%) of the 0.168 low-root gap at year 15 and runs the other way on the high root; the real-wage flip is not a
    g0 effect.
  - **The direction is robust; the size is not settled.** Across sigma 0.03–0.50, nearly its whole admissible range,
    every reading is below (b) at every date, root for root, and the real wage never rises: participation at year 15
    runs 0.058–0.266 (low root) and 0.134–0.385 (high). The tot-consistent reading (labour 0.47/(1 − 0.094) = 0.519;
    it needs g0 at most 0.0080 and runs at g0 0.005, and its rho, 0.050, is below the NIPA band) gives 0.199 / 0.292;
    the mixed basis, the severe bound of the three basis readings, 0.161 / 0.253; the measured site (ii) 0.351 /
    0.532, still below (b)
    calibrated at that same site (0.495 / 0.818 at g0 0.01) — its high root is the one (c) variant whose real wage
    rises first (x1.092 at year 7.75; (b) at that site x1.819). The superseded first central (sigma 0.090 from a
    mismatched scope, multiplier 7.34) gave 0.113 / 0.199.
  - **Recursive automation is first-order.** Lambda alone, capability fixed, lowers labour's share (all wages) by 12.7
    / 13.6 points by year 15 (0.554 → 0.427 / 0.418); under (b) by 0.05. Capability still drives participation (alone
    0.238 / 0.353 at year 15; lambda alone 0.548 / 0.544).
  - **What (c) cannot do** (open items in the file): sigma is a construction (delta_chain is BEA's private equipment +
    IPP rate, not the chain's own); the root is not identified; g0 had to move; the site target is 2–3 times the
    measured flow; the run is quasi-static; r*, the policy rate and debt are readouts of bridges tuned on (b) — the
    capex bridge is keyed to the pace of tasks and does not see investment / income fall (0.178 → 0.045 by year 15,
    medium); there is no land-slack corner, so a rate stress past the headroom raises NoEquilibrium rather than
    returning an outcome; imported content is modelled as land drawn from the endowment the housing site shares (0.559
    of sigma; the chain's share of it 0.311 → 0.040 by year 15, (b) 0.637 → 0.147, medium path at a fixed return;
    0.041 / 0.148 with the return following r*, the capital entry), its direction on the paths not
    quantified; the consumption chain's foreign content (0.094 of PCE) is left in capital services, and a probe moving
    it into a fixed rent is more severe (no root at g0 0.01), so the open reading's choice there is the mild one;
    WP2026-01's labour definition is unverified (if it imputes self-employed labour, theta_V is understated against
    it, toward a more severe result), and its numbers are the repository's digitisation of its Figure 9.
    → On the refit (Log 46): r*, the policy rate and debt rest on bridges refit against evidence, keyed to investment /
    income; that item is closed, with the investment key's pass-through (gross, or net for a growing stock) left open.
- **The switch to (c)** (her decision, 2026-09-30; decisions 37–42). Every module that runs the macro block now runs
  `macro.central()` (`'lo'`, the main reading; `'hi'`, the sensitivity): macro_scenarios and capital_feedback
  (`checks/check_macro_scenarios.py`, new, 13/13), recognition (14/14), reverse (21/21), regime_digestion (11/11),
  speed (18/18), demand (23/23), households (25/25), the stylised bank and the export (24/24). `central()` returns the
  stored central parameters once its re-solve of the stored targets agrees with them to a relative 1e-9 in every
  parameter, and refuses beyond that (since 2026-10-01, so that the website's builder, on other numpy and scipy builds,
  is not stopped by a last-bit difference; here the two are bit-identical, E1); `deep_tech` ends lambda at a fifth of
  each economy's own start (10.36 → 2.07 in model units; the absolute 0.01 was (b)'s), `hold_tech` holds it,
  `capital_premium` sets the premium per economy (rho·100 − r0*: 6.80 pp on (c), 5.0 on (b)) and `feedback_bridges`
  builds the bridges on it; on (b) the helpers give the old objects exactly (E2–E3). (a) and (b) stay as named
  comparators, gated equal to the pre-switch runs array for array; check_macro (21/21), check_global_crash and
  check_case print byte-identical stdout. No bridge coefficient was retuned, so on (c) r*, the policy rate and debt are
  readouts of bridges tuned on (b). The entries above and below are restated as found on (c), with the (a) / (b) numbers
  beside them; every pre-switch check id survives, and thresholds set after seeing (c)'s numbers are flagged in each
  battery's header.
  Bases (decision 38): a "labour share" in macro_scenarios is the Figure 7 basis (0.47 at the start); in recognition,
  speed, the capital split and the export's `labor_share` it is all wages over income (0.554 at (c)'s start, the
  chain's labour included). Every downstream (b) comparator is (b) at g0 0.02 while (c) runs at 0.01, so size ratios
  between them carry the g0 change (0.028 of the 0.168 low-root gap at year 15). HEAD's committed
  macro_scenarios.json, capital_feedback.json, recognition.json and regime_digestion.json differ from HEAD's code run
  today by up to about 1e-11 in some floats; every rounded number is identical, and the re-run removes the difference.
  In plain words: on (c) deep automation is harsher for wages and for the state from the start, the rate response is
  more two-sided with a longer rise tail, and rates matter more for automation.
  → 2026-10-27 (Log 46): the bridges are refit on (c); the comparators keep (b)'s (`macro.BRIDGES_B`). On the refit the
  rate response is no longer two-sided: rates fall under deep automation at every speed and in both of the bank's
  branches, and the rise tail is shorter than (b)'s.
- **`code/recognition.py` — the recognition clock as a mixture** (her call, 2026-09-24; checks
  `checks/check_recognition.py`, 14/14 since the switch, 10 before; `code/recognition_scenarios.py`,
  `results/recognition.json`, `figures/fig_recognition.png`). Two worlds, each a full macro path with the return
  following r* — on calibration (c)'s central since 2026-09-30 (premium 6.80 pp; (b) kept as `comparator_b`, the high
  root as `sensitivity_c_hi`): the status quo and medium deep automation. The market watches labour's share each
  quarter with noise — all wages over income, the machine chain's labour included (0.554 at (c)'s start; on (b) the
  two bases coincide to 0.001) — and updates the odds of the new world by Bayes' rule (L2: the noiseless log odds are
  exactly logit(p0) + Σ(s_new − s_old)²/2σ²); its curve is the probability-weighted mix of the two worlds' curves
  (M1), the central bank learns alongside it (M3), and revealing the truth jumps the curve by (1 − p)(z_new − z_old)
  at every date (M2). Narrative shocks move the odds with no data (L5). Findings, default bridges, restated on (c)
  ((b) beside):
  - **Late in the data, then fast — and earlier on (c).** With 1 pp noise and a 5% prior the market goes from 10% to
    90% between years 1.26 and 2.16 ((b) 2.3 and 3.6); it is past one half at year 1.83, when 3.0% of the eventual
    labour-share fall has happened ((b) 3.16, 3.4%) (S1). Over 500 noise draws the one-half date is 1.40 / 1.84 / 2.34
    years (10/50/90%; (b) 2.6 / 3.2 / 3.8); noise alone persuades the market of a new world that is not coming in 1.4%
    of draws ((b) 3.4%). The 1.33 years' advance is on the all-wages signal, whose chain labour falls fastest as
    lambda falls: watching the Figure 7 basis the one-half date is 2.34 (against (b)'s 3.17), 0.83 years earlier (high
    root 2.04 all wages, 2.76 Figure 7); at year 3 the fall is 3.93 pp on all wages and 2.43 on the Figure 7 basis
    ((b) 1.23 / 1.22) (S3; `sensitivity_signal_fig7`).
  - **The curve barely moves, and now edges down along its whole length.** Across the recognition window: 3M −0.3, 2Y
    −5.4, 10Y −15.3, 30Y −20.0 bp — a bull flattening; on (b) the front rose (3M +2, 2Y +5, 10Y −11, 30Y −20), so the
    2Y's sign flips (S4). Waking up from year 0 to 5 moves the 2Y −15, 10Y −33, 30Y −41 bp (S2; (b) +4 / −20 / −32,
    from HEAD's pre-switch check_recognition S2 output, not stored in recognition.json).
    The jump waiting at any date is at most 2Y −3.5, 10Y −11.0, 30Y −14.6 bp ((b) about 11). A narrative shock takes
    belief to 0.21 ((b) 0.48), moves the 10Y −2.5 bp ((b) −1.1) and is back below 0.1 by year 1.72 ((b) 3.0) when the
    data do not confirm it.
  - `[inferred]` **Under these coefficients the risk-free curve is still a poor early-warning signal for this risk;**
    the large moves are in the real economy — wages, labour's share, the fiscal base — which is where a bank's credit
    and income risk sits, and on (c) they are larger. How big the curve moves are hinges on the bridge coefficients
    (behaviour, not structure), tuned on (b) and not refitted: the question the reverse stress test asks.
  → On the refit (Log 46): across the window 3M −5, 2Y −70, 10Y −177, 30Y −227 bp, a bull flattening of about two
    points; the jump waiting up to 2Y −47, 10Y −133, 30Y −174 bp; a narrative shock moves the 10Y −27 bp. The curve no
    longer "barely moves": it moves a long way, down, once the data have persuaded the market — which is still late
    (10% → 90% between years 1.24 and 2.12, when 3% of the fall has happened). The early warning is still in the real
    economy; the curve's move, once it comes, is large.
- **`code/reverse.py` — reverse stress testing, part 1: the envelope over the dials** (checks
  `checks/check_reverse.py`, 21/21 since the switch, 11 before; `code/reverse_envelope.py`,
  `results/reverse_envelope.json`, `figures/fig_reverse_envelope.png`). Twelve dials — the technology path (depth,
  width, midpoint; lambda to a fifth of the economy's own start), the bridges (build-out, owners' saving, deficits →
  r*; term premium per debt, debt threshold, public support), the premium (since the switch `premium_shift`, ±2 pp
  around each economy's own premium: 6.80 on (c), 5.0 on (b), where it is the old 3–7 dial; decision 40), and the
  market's learning (noise, prior) — drawn 4,000 times by Latin hypercube over broad stated ranges (`RANGES`; scale
  dials in logs); each draw runs the two-world recognition model. Since 2026-09-30 the same 4,000 draws run on (c)'s
  central and on (b) (`comparator_b`, the pre-switch envelope exactly). All 4,000 solve on both; none loses its
  land-scarce equilibrium (a draw that did would be caught, counted and dated: N1). Findings, restated on (c) ((b)
  beside):
  - **The sign of the curve's move is not pinned by the mechanism; the same two bridges decide it.** The 10Y over ten
    years: −321 / −101 / +329 bp (5/50/95%; (b) −322 / −107 / +147); across the recognition window −226 / −34 / +171
    ((b) −191 / −23 / +128). In 54% of draws the 10Y never rises above its start (as on (b)); in 34% it never falls
    below it ((b) 24%). Owners' saving drives every curve outcome (rank correlation −0.68 to −0.82; (b) −0.83 to
    −0.85), deficits push the other way, more than on (b) (+0.37 to +0.48; (b) +0.32 to +0.35), and the build-out less
    (+0.14 in the recognition window; (b) +0.28). From the defaults, owners' saving at 0.02 rather than 0.15 is +75
    against −318 bp ((b) +35 / −322); deficits at 0 rather than 0.3 are −236 against +239 ((b) −174 / +112) (R3).
  - **The technology path decides the real economy, not the curve — and the damage is larger.** The real wage's low
    point is 0.13 / 0.39 / 0.73 of its start (5/50/95%; (b) 0.34 / 0.77 / 1.00), at most 0.82: below its start in
    every draw. Automation depth drives it (+0.90; (b) +0.94); public support drives debt (+0.67; (b) +0.62), whose
    peak is 57 / 119 / 201% of income ((b) median 75%, 95th percentile 124%). The technology path's correlations with
    the curve outcomes are at most 0.09 ((b) 0.17); the learning dials set when the market wakes up (the one-half date
    0.43 / 1.66 / 5.35 years; (b) 1.12 / 3.04 / 6.37), not how far the curve moves (|ρ| ≤ 0.07; (b) 0.11).
  - **Neither direction is far from the defaults, and the route is the two direction bridges.** The most plausible
    draw reaching +100 bp (nearest the defaults in the unit cube) is nearer on (c): draw 268, distance 0.511 ((b)
    0.608), +146 bp. Re-run with dial subsets (`reverse.attribute`; `cause_by_subset`), its cause is owners' saving at
    about half its default (0.05 → 0.023) and deficits at 1.5 times theirs (0.10 → 0.150), each moved by less than the
    0.15 of range at which the listing of "dials moved" starts: those two alone give +221.5 bp, set back to their
    defaults 0.0; the listed technology and fiscal dials (width 3.6, midpoint 7.0, term premium per debt 0.007, public
    support 0.21) alone give 0.0 and damp the rise. **Corrected (2026-10-01):** the first switch report read the
    listing as the cause ("through the technology path and fiscal dials alone, no neutral-rate bridge moved"), and
    this entry's (b) route ("build-out 0.25 → 0.44, deficits 0.10 → 0.18, premium 5 → 6.2", draw 3168, +101 bp) was
    the same listing: by subsets (b)'s route needs build-out, owners' saving (0.05 → 0.028, not listed), deficits and
    public support; owners' saving and deficits alone give +101.7; the premium is not needed. Reaching −100 bp is the
    same draw (1836) on both calibrations (−152 bp); it needs deficits at about half their default (0.0495), and the
    listed later midpoint, build-out and premium alone give −52.7 ((b) −87.2). A +50 bp move inside the recognition
    window is draw 268 again (+78 bp), needing owners' saving and deficits (alone +56.7; reset −16.6; on (b) the width
    as well). The default dials already reach −72 bp ((b) −91).
  - **The tails are asymmetric by assumption, not by mechanism — and the rise side is longer on (c).** Expectations
    stop at the −0.5% lower bound: policy reaches it in 30% of draws ((b) about a fifth), and the fall side piles up
    near −325 bp (the floor plus the term premium). The rise side has no ceiling: the largest rise's 95th percentile
    is +474 bp ((b) +215), the largest +1,378 ((b) +608), with policy up to 11.75% ((b) 11.25%). The largest rise in
    the required return (draw 1315) peaks 7.38 pp above the central's rho at year 13.75 — past the 7.18 pp start
    headroom — and solves because the headroom at that date's technology is 20 pp or more.
  - `[inferred]` **For a bank:** a rate stress for this risk has to be two-sided, because the mechanism fixes the
    real-economy damage (wages, labour's share, the tax base) far more firmly than the sign of the rate move — which
    rides on how owners' income is spent and how the state finances the transition. The largest curve moves come with
    fiscal strain (debt above the threshold) or a saving glut at the floor, and that pairing — not the rate level — is
    what to put against the balance sheet in part 2. On (c) the rise tail is more than twice as long, so the
    fiscal-strain branch weighs more than it did.
  - Three artefacts found and fixed on the way (log 9): a destination window that ran off the path's end, a rate
    feedback that cycled quarter to quarter, and uniform ranges that made most draws mild automation.
  → On the refit (Log 46; decision 77: the central's bridge dials the evidence's, (b) on its own): the sign is nearly
    pinned, downward — the 10Y falls over ten years in 94% of draws and through the recognition window in 95%; it never
    rises in 87%; policy reaches the floor in 64%. Owners' saving still drives the size most (−0.67), deficits push back
    (+0.37), the investment scale −0.13. The rise side's 95th percentile is +124 bp (shorter than (b)'s +215), its
    largest +754; a +100 bp rise needs fiscal strain (term premium per debt, public support) besides the two direction
    bridges; the default dials alone reach −320 bp. The largest rise in the required return is 3.29 pp, inside the
    headroom; on the investment key no draw cycles even undamped. The bank reading above flips with it: the fall side,
    not the rise side, is long.
- **Speed: markets at machine speed** (her point, 2026-09-24; `code/recognition.py` extended — capacity, trust, a
  shared error, digestion — `code/speed_scenarios.py`, `results/speed.json`, `figures/fig_speed.png`; checks
  `checks/check_speed.py`, 18/18 since the switch, 15 before). Two channels, run separately, plus a failure mode.
  Worlds on a weekly grid with the two bridges that decide direction, on (c)'s central since 2026-09-30 ((b) as
  `comparator_b`): "deficits dominate" moves the 10Y +118 bp through recognition ((b) +80) and "owners' saving
  dominates" −150 bp ((b) −119), in a window that opens more than a year earlier (years 1.61–2.85; (b) 2.73–4.21); the
  required return rises at most 3.10 pp of its 7.18 pp headroom ((b) 1.80) (F4). Restated on (c):
  - **More reading makes recognition earlier, not sharper.** Capacity c = c times as many independent readings (L2: a
    learner with noise σ/√c). With trust following the economy's own automation, the market recognises the new world
    while trust in AI is still 3–6% ((b) 6–15%) (F1): it wakes up from the data before the AI it would use is trusted,
    and the speed-up barely bites. If finance adopts three years ahead of the economy, ×100 moves the one-half date
    from year 2.24 to 0.92 (1.1% of the labour-share fall done, not 4.3%; (b) 3.6 → 1.6, 1% not 5%); the 10%→90%
    window shrinks from 64 to 22 weeks (×2.9; (b) 77 → 33, ×2.3): earlier holds, and the narrowing is a little
    stronger.
  - **Faster digestion makes it abrupt — about twice as abrupt on (c).** The same lump of news (+4 log odds at year
    1.5, before recognition) moves the 10Y 4 bp in its first week if regime news is digested with a quarter's
    half-life, 33 at ×10, 67 on the measured 1980s rung, 81 at ×100 or instantly ((b) 2 / 16 / 33 / 40 / 40); the 3M
    moves about 2 bp ((b) 1) because policy waits for meetings, so the long end gaps alone — a twist, not a parallel
    shift. Within a month: 16, 73, 82 bp ((b) 8, 36, 41); the saving-dominates world mirrors it (−103 bp in the week
    at machine speed; (b) −50). The worlds' curves differ more on (c): the deficits world's r* peaks at 3.86% against
    (b)'s 2.54 (the same world, gated in regime_digestion F7). (Numbers after the correction of log 11: digestion acts
    on the belief, not its log odds.)
  - **Faster, and easier to fool.** If the market's AI readings share an error (0.5 pp of the 1 pp) and it knows,
    capacity is capped at the shared error's precision (L4) and false dawns stay low but rise with capacity: 0–4%, 4%
    at ×100 ((b) 0.7–2.0%). If it takes them for independent confirmation, false dawns in a status quo world rise from
    0% today to 25% at ×10, 54% at ×30 and 83% at ×100 ((b) 28 / 61 / 82%; 300 draws) — and the same market is right
    early when the new world is real (one-half at 0.30 years at ×100, 10/90% 0.17 / 0.80; (b) 0.7) (F3).
  - **The history, her second point** (`code/digestion_history.py`, `results/digestion_history.json`,
    `figures/fig_digestion_history.png`; H1–H3). US Treasury yields since 1962: the 10Y's 21-day variance ratio was
    1.48 in 1962–81 and 1.26 in 1982–94 (news kept drifting in for weeks, z 2.8 and 2.2), 1.04 in 1995–2008 and 0.88
    since 2009 (a little overshoot). The decline is gradual — from 2.4–2.6 around 1970 through the screen-and-futures
    1980s to 1.0 by the mid-1990s — so it predates both the Fed's announcements (1994) and the internet, pointing at
    market technology and structure (with staler early quotes and Fed opacity as stated confounds). In 1982–94 about
    three quarters of a 10Y move came at once and the rest with a half-life of about two weeks. On that measured rung
    the same lump of news moves the 10Y 67 bp in its first week on (c) (33 on (b); F2) — so for quantified news the
    step from human to machine speed has largely happened already. What the speed results rest on is the assumption
    that humans still digest *regime judgements* slowly; daily yields cannot measure that — the forward-rate test
    below does.
  - `[inferred]` **For a bank:** machine-speed markets move the risk from a late, large resolution jump to an early,
    abrupt repricing of the long end while the policy rate waits — inside the interval between a bank's hedging
    decisions (a monthly ALCO absorbs 73–82 bp in the scenario where a human market would have shown 16; (b) 36–41
    against 8) — and they add a new tail: correlated models producing false dawns that reverse.
  → On the refit (Log 46): both branches move the 10Y down through recognition (deficits −44, owners' saving −194 bp);
    a lump of news moves the 10Y down along the ladder (−0.8 / −6.1 / −12.1 / −14.7 / −14.7 bp in its first week). The
    abrupt-repricing reading holds, in the falling direction.
- **The forward-rate test: how slowly are regime judgements digested?** (her go, 2026-09-24;
  `code/regime_digestion.py`, `results/regime_digestion.json`, `figures/fig_regime_digestion.png`; checks
  `checks/check_regime_digestion.py`, 11/11 since the switch, 9 before; layers 1–2 are data and unchanged by it).
  Public sources: the Fed Board's Gürkaynak–Sack–Wright zero curve (a trimmed vintage in `cache/fed/`), the
  Philadelphia Fed's Survey of Professional Forecasters (`cache/spf/`), Kim–Wright term premia and the 3-month bill
  (FRED). The test at the first layer is Coibion–Gorodnichenko's: forecast error on forecast revision, whose slope b
  gives the share of news not yet absorbed, b/(1 + b), and so a half-life (E2 checks the mapping on a simulated
  sticky-information forecaster). Findings — three layers, three speeds:
  - **Prices of quantified news: days** (above: none left since 1995; two weeks for a quarter of each
    10Y move in 1982–94).
  - **Expectations of the next year: months.** Survey forecasts of the bill rate under-react —
    half-life 1.1, 1.7, 2.4 months at 1, 2, 3 quarters ahead (F1; slopes +0.41 and +0.71, se 0.14
    and 0.22) — and market forwards a year ahead, net of term premia, likewise (+0.37, se 0.14:
    half-life about 6 months; +0.59 since 2008). Surveyed forecasters show no sign of speeding up
    across eras (+0.38, +0.81, +0.98 three quarters ahead; F3): prices got faster, the people did
    not — her bottleneck, located.
  - **Regime anchors: years.** The survey's expected 10-year bill average and the market's expected
    rate 9–10 years ahead (net of Kim–Wright) move toward realized rates with half-lives of 7–11 years
    before 2021 and 2–3 years since (F4). The survey anchor was too high in 96% of surveys 1992–2016
    (overlapping decades: about 2.5 independent ones), by 1.8 pp on average, and did worse than
    assuming no change (RMSE 2.0 against 1.8 pp; F5) — so its slowness is not only prudence. At
    longer market horizons (2–4 years) the slopes are unstable and turn negative before 2008,
    the term premium being the usual suspect; not relied on.
  - **What it means in the model** (layer 3, on (c)'s central since 2026-09-30, (b) kept as
    `layer3_model_catch_up_comparator_b`; F6, F7): if people digest regime news with a half-life of 3 years — inside
    the measured range — while AI digests it in weeks, adopting AI can itself reprice the curve. Deficits dominate, AI
    adopted around year 5 (×30): the 10Y rises 108 bp in the adoption year, against 38 without AI and 31 in the
    evidence itself ((b) 74 / 22 / 17) — a catch-up to what the data had long said, with no news that year. With AI,
    at half-lives of 1 / 3 / 5 years: +47 / +108 / +126 bp ((b) +40 / +74 / +79; without AI at 5 years 29, (b) 16).
    The new world's r* peaks at 3.86% ((b) 2.54); the required return rises at most 3.10 pp of its 7.18 pp headroom.
  - `[inferred]` **Reading:** the quarter-long half-life assumed in the speed scenarios was the
    fast end; the anchors say years. The human bottleneck sits in judgement about regimes, which is
    exactly where this risk lives — so the speed-up that matters is still to come, and it can arrive
    as a repricing driven by the market's tools rather than by news.
  → On the refit (Log 46): the catch-up runs down — adopting AI around year 5 moves the 10Y −22 / −47 / −54 bp at
    half-lives of 1 / 3 / 5 years, against −18 without AI and −16 in the evidence; even with deficits dominating the new
    world's r* never rises (−1.12% at year 15).
- **A stylised bank on the paths** (her question, 2026-09-24: real rate rises lift NII first — floating mortgages,
  cash at the central bank — then tightening lowers house and asset prices, then the interest income flows back into
  assets; `code/bank.py`, `code/bank_scenarios.py`, `results/bank.json`, `figures/fig_bank.png`; checks
  `checks/check_bank.py`, 24/24 since the switch, 12 before). An illustrative round-number Nordic-style balance sheet
  — not any bank's — with named behaviours: deposits (transaction accounts at zero, savings accounts catching up,
  migration between them), mortgage margins that lag funding and widen near the floor, reserves paid a share of the
  policy rate, a securities ladder, house prices as the belief-weighted expected site rent capitalised at the real 10Y
  plus a premium, wage-earning borrowers (debt-to-income and loan-to-value spread lognormally), commercial property
  (interest cover, refinancing over three years, rents following the site or the wage bill). Four paths, on (c)'s
  central since 2026-09-30, with (b) and the high root stored beside. Findings:
  - **A pure tightening** (+250 bp, announced at year 1, held two years, reversed): NII up 0.77 pp of assets at the
    peak (2.14 → 2.91%), nearly all of it the deposit spread; the windfall decays while rates are held (pass-through
    0.24 at the peak, 0.42 a year later); mortgage margins squeezed on the way up (0.46 → 0.25 pp of assets) and
    fattened on the way down; after the cycle NII dips below its start as savings rates lag down. House prices −18% at
    the announcement and back as the hike passes — the recovery rides the rate path back down. Borrowers over the
    debt-service line 8% → 15%; property loans below 1.5x cover 10% → 25%; losses peak at year 3.75, after NII's peak
    at 3.0 (F1). Her first half, confirmed, with the windfall located: deposits, not mortgages; reserves earn the
    policy rate, so "cash at the central bank" is the deposit spread on the money behind it. The pure tightening is
    identical on every calibration (R3).
  - **The paper's world with real rates rising** (deficits dominate): NII rises with the build-out (2.11 → 2.99% of
    assets; (b) 2.63) as policy peaks at 5.75% ((b) 4.50) and the 10Y reaches 7.0% by year 15 ((b) 5.0) — but house
    prices do not fall: they rise about 2.8 times in real terms by year 10 ((b) 3.0), the site's expected rents
    outweighing the higher discount rate, while the real wage falls to 0.29 of its start by year 15 ((b) 0.57) and 55%
    of borrowers have stopped working ((b) 30%); 70% of borrowers are over the debt-service line ((b) 14%; mean debt
    service up to 0.514 of income against 0.231). Mortgage losses stay near zero (0.005% a year) because loan-to-value
    falls to 0.13 by year 10: the collateral boom protects the bank, not the borrowers (F2, holding more strongly on
    the borrowers' side). The mortgage book's risk moves to households (forced sales at high prices), and the buyers
    become owners, not wage earners. The required return rises at most 3.10 pp of its 7.18 pp headroom (high root 2.61
    of 7.85; (b) 1.80; R4).
  - **Commercial property hangs on one assumption** (F3): rents following the site, cover improves; following the wage
    bill (offices need workers — the model's single land market cannot say which), the whole book is below 1.5x by
    year 15 ((b) 92%) and losses reach 0.35% of assets a year ((b) 0.33). **New on (c)** (F6): with wage-bill rents
    property breaks in both branches — 100% of the book below 1.5x when owners' saving dominates too ((b) 10%) on the
    central root, 58% on the high root.
  - **Her second half — the income flowing back — is the bank's worst path** (F4): owners' saving pulls rates to the
    floor and NII falls from 2.11 to 0.88% of assets, reached at year 10.75 ((b) 13.25), even with lending margins
    widening; house prices rise about 19 times in real terms, already by year 5 ((b) 9 times at year 5, 17 by year
    10). The recycling lifts asset prices by pulling rates down, and that is what compresses the bank's margin. **New
    on (c), central root only** (F5): the falling-rate branch squeezes borrowers too — money wages fall faster than
    mortgage rates, so up to 39.7% are over the debt-service line (mean debt service 0.348 of income), against 7.6% at
    the start; on the high root and on (b) the share stays at its start.
  - **The two-branch split rests on the capex key** (R5, a readout; decision 39): with r* keyed to investment
    spending, the deficits branch's policy peak is 5.75 / 5.25% / ends at the floor (task key / bridge scale /
    demand-layer scale), its NII low 2.11 / 2.11 / 0.88 and its 10Y at year 10 5.99 / 5.35 / −0.31% — at the
    demand-layer scale it takes the owners'-saving branch's NII low.
  - Also found: in the status quo a 5% prior on the new world is worth 18% of house value ((b) 15%); as the market
    learns the world is not changing, house prices fall to 0.82 of their start ((b) 0.85).
  - `[inferred]` **For the bank:** a tightening's NII gain is a deposit windfall that decays and reverses; in the
    paper's world the link between rates and house prices breaks (land up with rates up, borrowers' incomes down),
    credit risk moves from the bank's books to households and to commercial property, and the pressure on the bank's
    earnings comes from the falling-rate branch — on (c) sooner, with its borrowers squeezed as well on the central
    root.
  → On the refit (Log 46): the deficits branch's rates fall too — policy 2.75 → 1.0%, NII 2.11 → 1.49, house prices x10 by
    year 10, 40% of borrowers over the debt-service line; owners' saving to the floor as before (NII low 0.88), 72% over
    the line (18% on the high root). Keyed back to the pace of tasks, the deficits branch rises again (policy 4.75%): the
    split rests on the capex key, and on the refit it closes downward.
- **What Swedish banks did at the floor** (her call, 2026-09-24: test floor behaviour on public
  data; `code/floor_margins.py`, `results/floor_margins.json`,
  `figures/fig_floor_margins.png`; checks `checks/check_floor_margins.py`, 7/7). Public: Statistics
  Sweden's MFI interest-rate statistics (new and outstanding household mortgage rates by fixation;
  bank deposit rates, households and corporates; corporate floating lending) and the Riksbank's policy
  rate, STIBOR 3M (to 2020-07) and mortgage-bond yields, monthly 2005-2026. Findings:
  - **Mortgage rates stopped falling at zero.** With policy at -0.50% (2016-18) new floating mortgages
    cost 1.53%, against 1.48% with policy at 0% (2020-21): margins widened +1.03 per point below zero
    (regression over 2015-21, one capital regime; contrast 1.11; over STIBOR 1.13). The confound — FI's
    risk-weight floors of 2013-14 — sits before the window. **Corporate floating loans did pass negative
    rates through** (margin 1.94 against 1.92). **Deposit rates stopped at zero**, not below (households
    0.06%, corporates 0.007% at the lowest).
  - **Deposits rise more slowly than they fall.** Household deposit rates passed on 0.49-0.57 of the
    2022-23 hikes against 0.74-0.78 of the 2024-26 cuts (0.66-0.74 up against down), about two months
    later; corporates 0.89-0.90.
  - **Mortgage margins were squeezed on the way up and did not recover**: -0.13 per point over the
    hikes (1.41 in 2021H2 -> 0.91 in 2023H2; 0.97 in 2026H1).
  - The stylised bank now carries the measured floor rule (`margin_comp` 1.0 from zero, replacing a guessed 0.5 from
    0.5% — which happened to give the same margin at the model's -0.5% floor, so its levels do not move; the NII low
    in the owners'-saving path comes a quarter earlier, 13.25 years, on (b); on (c) it comes at 10.75).
- **Do deposits follow wages?** (her call, 2026-09-24, after credit: test the assumption that a bank's
  household deposits are a wage franchise; `code/deposits_wages.py`, `results/deposits_wages.json`,
  `figures/fig_deposits_wages.png`; checks `checks/check_deposits_wages.py`, 9/9). Public: Statistics Sweden's
  financial accounts (household deposits, quarterly 1996-2026), household income by transaction and the sector
  accounts, deposit rates; the Riksbank's policy rate. Questions fixed before fitting. Findings:
  - **A year's deposit growth does not follow its wage growth** (slope 0.30, s.e. 0.53, R² 0.01); it does
    follow disposable income growth (1.26, s.e. 0.50, R² 0.24).
  - **Deposits accumulate saving**: about 0.35 of each krona households save lands in deposits (s.e. 0.10);
    wage growth adds nothing measurable once saving is in (0.28, s.e. 0.38; a wage franchise implies ~0.8,
    not rejected at 5% — the data are not sharp enough to refute it outright).
  - **Against a wage franchise's sign**: relative to income, deposits are lower when wages are a larger share
    of income (-2.2, s.e. 0.6, with a trend). The wage share moved only between 0.82 and 0.93, and the
    obvious confound is age (pensioners hold deposits and receive transfers, not wages).
  - **Rates move them**: deposits fell from 0.96 to 0.90 of disposable income through the 2022-24 hikes,
    -2.8% per point of the cost of holding them (policy rate over the demand-deposit rate); over the whole
    sample, with and without a trend, -0.5% to -13% per point — the trend and the fall in rates are not
    separable, the hikes are the one clean episode.
  - **Households receive about half the economy's non-wage income** (their own surplus and net property
    income over the economy's net operating surplus and mixed income: 0.54 over 1996-2025, 0.63 since 2015).
  - The export gains the model's real income and labour share, so household income can be built as wages plus that
    share of non-wage income. **Restated on (c) (check_bank X4):** at year 10 real income is x1.35 / x1.33 (deficits /
    owners' saving) while the wage bill falls to 0.30 / 0.18 and employment to 0.63 / 0.51, so household income is
    about flat — 1.005 / 0.958 of its start at the measured share 0.536, 1.089 / 1.050 at 0.631 — and, on this
    evidence, the deposits that follow it with it. On (b) real income doubled (x2.04 / x2.03) while the wage bill fell
    to 0.74 / 0.63, and household income rose by about two-thirds (1.66 / 1.62); that reading disappears on (c). The
    export's `labor_share` is all wages over income, so its level at the start is 0.554 on (c) (0.47 on (b)); a
    `calibration` column is appended last.
- **A demand gap** (her call, 2026-09-24: can the paper's world produce a recession, high inflation or deflation,
  fast? `code/demand.py`, `results/demand.json`, `figures/fig_demand.png`; checks `checks/check_demand.py`, 23/23
  since the switch, 13 before). The macro block is at capacity every date with the central bank delivering r* + target
  at once, so it could not say. The layer: a reduced-form IS curve, an expectations-augmented Phillips curve, a
  smoothed Taylor rule with the -0.5% floor — and a central bank that learns r* with a lag (half-life 3 years; 1 and 8
  as variants, the range the forward-rate test measured). Okun and the Phillips slope measured on Swedish data
  2002-2026: unemployment -0.17 points per point of growth (s.e. 0.03); core inflation -0.78 per point of unemployment
  gap (s.e. 0.42 — 1.9 s.e., not sharp), so kappa 0.13 per point of output gap. The IS slope is the literature's
  (Laubach-Williams, approximate; 0.05-0.15 run). Findings, restated on (c)'s central since 2026-09-30 ((b) and the
  high root stored beside):
  - **Policy errs in the direction of the branch, more on (c)**: too tight when owners' saving dominates (gap −1.85%
    at year 15, still deepening at the horizon; inflation 1.73–2.0%; the floor binding 4.0 years from year 11.25; (b)
    −1.36 at year 12.5, 1.25 years from year 14), too loose when deficits dominate (+1.08% at year 10.5, inflation up
    to 2.16%; (b) +0.61, 2.09). Learning r* with a 1 / 3 / 8-year half-life gives gaps of 0.58 / 1.08 / 1.58
    (deficits) and 1.63 / 1.85 / 2.21 (owners' saving) ((b) 0.32 / 0.61 / 0.90 and 0.80 / 1.36 / 1.96). With fast
    automation and owners' saving the floor binds 8.25 years from year 7.0 (F6, new on (c)).
  - **The cycle stays normal-sized in the output gap, not quite in inflation** (F3, restated): every run stays within
    a 3% gap (largest 2.72%; (b) 2.29%) and the firm-anchor runs within 1.61–2.29% headline inflation, but with a weak
    anchor inflation runs 1.28–2.41%, its low outside the 1.5–2.5% band that held on (b) (27 runs, 1.54–2.26%). The
    weirdness
    is structural, not cyclical: participation falls to about half its start by year 10 (0.507; (b) 0.838) against a
    cyclical unemployment rise of 0.31 points ((b) 0.23); in the macro block's medium fork goods fall 25% a year and
    shelter rises 29% at the peak while the headline sits near 2% ((b)'s demand worlds: goods −15 to −20%, housing
    +28–30%).
  - **A 2009-size demand shock** (4% of capacity) takes today's Riksbank to the floor (room 2.25 points) and not
    2008's (5.25): with the Riksbank's 2008 response strength and a weak anchor, the gap three years on is −0.9%
    against −0.4%. A slower recovery, not a spiral. (A status-quo test, unchanged by the switch: −0.88 against −0.43.)
  - **The neutral rate keyed to investment** (R1–R6, a readout of the (b)-tuned bridge; decision 39): with the capex
    term keyed to replacement investment / income (17.8 → 4.4% of income on (c)) at the bridge's converted scale
    (0.0394) or the IS curve's (0.6), r* is lower at year 15 in every (c) world and the default fast rise (+0.54 pp)
    disappears; deficits at year 15 3.86 / 3.30 / −4.22%, owners' saving −3.83 / −4.38 / −11.65 (task key / bridge /
    demand-layer scale). At the demand-layer scale the owners'-saving gap reaches −11.85% with inflation down to
    0.27%, and the deficits branch becomes a slump at the floor (gap −2.25, 3.75 years at the floor); on (b) the hump
    survives at that scale. Net investment is negative on every deep path, (b) included — the machine stock falls by
    more than half by year 10 — so keying to it would lower r* further. The size of the cycle and the bank's two
    branches rest on this key.
  - `[inferred]` A spiral — deflation feeding real rates at the floor — does not come out of a linear layer with
    anchored expectations. It needs the channels this layer leaves out: debt deflation (fixed nominal debts
    against falling money wages, which the macro block produces at the peak), credit crunches, confidence. Those
    are the next things to add if the tail is the question.
  → On the refit (Log 46): the owners'-saving branch is no longer normal-sized — gap −7.2%, the floor 6.75 years from
    year 8.5, inflation down to 0.94% (−0.09 with a weak anchor); fast automation −9.0, a steeper IS curve −10.9; the
    deficits branch a small slump (−0.65%, inflation 1.91). The cyclical unemployment rise is 1.2 points. Keyed back to the
    pace, the deficits branch is a mild boom again (+0.8%).
- **Who carries the people who leave work** (her call, 2026-09-24: a surge in dependence — families, friends — and
  emergency policy such as stimulus checks; central case today's Swedish state support; `code/households.py`,
  `results/households.json`, `figures/fig_households.png`; checks `checks/check_households.py`, 25/25 since the
  switch; 11 at first, 18 with family-based support). The paper's economy pools everything (one owning household gives
  every member a basket, working or not), so dependence was in the model only in its frictionless form. The layer adds
  what pooling hides, as the extra spending of budget-constrained groups fed into the demand layer: people who lose
  work (net wage replaced by public support — 0.65 the first year, 0.50 after, approximate — family and friends' share
  of the rest, then their own savings), their supporters, borrowers' debt service on fixed money debts (floating on
  76.8% of housing loans, measured), and emergency checks. Measured start (Statistics Sweden): debt 1.74 x disposable
  income, mortgage margin 1.07. Findings, restated on (c)'s central since 2026-09-30 ((b) and the high root stored
  beside; year 10 unless stated). (c)'s collapse in money wages exposes two artefacts of the layer, now gated, not
  fixed (decision 41):
  - **The benefit artefact (A1).** Benefits paid on the start's real wage exceed the fallen wage from about year 9, so
    the job losers' drag is zero for good from year 9.25 (deficits) and 8.25 (owners' saving), and coverage of the
    lost wage passes 100% (176% / 315% by year 15). Not central-root only: on the high root from 11.75 / 9.75 (112% /
    158%); on (b) when owners' saving dominates, from year 12 (120% by 15), and never within 15 years when deficits do
    (92%). Paying benefits on each cohort's wage at exit delays it (to years 14.0 and 10.25); it does not remove it
    (S1).
  - **The employment floor (A2), central root only.** Rigid money wages take employment to the layer's 5% floor from
    year 10.5 (owners' saving; 15.5 deficits); no rigid-wage run reaches it on the high root or on (b).
  - **Today's Swedish state support absorbs the surge in dependence — on (c) partly through A1.** Without state
    support the job losers' drag at year 12 is 2.2% of GDP ((b) 1.1 against 0.1 with it); with it, zero (A1), and
    −0.11% with benefits at exit (F3). Under state support family and friends change almost nothing (−0.55 against
    −0.55; (b) −0.35 / −0.35).
  - **Floating-rate mortgages are a stabiliser that follows the branch.** Debt service goes from 10.2% of borrowers'
    income to about 15% when deficits dominate ((b) 13%) and down to 4.6% when owners' saving does ((b) 5.2%), so in
    the falling branch Swedish households cushion the downturn (gap −1.24% against −1.85% pooled; (b) −1.16 / −1.36).
  - **Rigid money wages are the dangerous case, and the realistic one** — capped on (c) by the employment floor. The
    macro block asks money wages to fall 60–80% by year 15; floored at zero, the adjustment lands on jobs
    (labour-demand elasticity 0.4): 87% of the start's employment out of work by year 10 against 49.5% with flexible
    wages (owners' saving; (b) 27% / 16%), the gap −4.97% against −1.24% ((b) −2.78 / −1.16), 5.75 years at the floor
    against 3.5. Debt deflation does not bite there — rates fall and wages hold — unemployment does.
  - **Emergency checks** (4% of household income for a year, triggered by unemployment) lift output about 0.5 points
    while paid (from year 4.0; (b) 0.3) and leave nothing after.
  - **Family-based support** (her next call, 2026-09-24; lean state support 0.40 then 0.25 of the net wage, family and
    friends covering half the rest, capped at 10% of supporters' net wages, supporters spending 0.6 of a krona — all
    assumed or approximate, no Swedish measure of private support). Leaning on families halves the state's bill (2.58
    against 5.01% of GDP at year 12, deficits dominate; (b) 0.8 / 1.5) and costs demand: the constrained households'
    drag rises from 0.59 to 1.09% of GDP ((b) 0.4 → 0.9). When owners' saving dominates the cost is 0.17% of GDP,
    under the claim's 0.2 ((b) 0.58), and its positive levels (+0.43 against +0.60) are A1's: with benefits at exit
    the family-based level is −0.29 against +0.43, a cost of 0.72. **Networks run out — on (b); on (c) A1 hides it.**
    The cap binds 3.25 years when deficits dominate (years 9.25–12.25) and 1.0 year when owners' saving does ((b)
    2–3.5 years), and coverage of the lost wage at year 15 is 94.6% / 158.6% ((b) 70–75%; 92% under state support):
    the "70–75% covered by year 15" reading disappears under A1 — it survives with benefits at exit when deficits
    dominate (59.6%), not when owners' saving does (82.0%) — and supporters are no longer at the cap at year 15
    (burden 7.2% / 0.0%; with benefits at exit 10.0 / 10.0, as on (b)). While the cap binds, lifting it covers up to
    2.2 / 0.6 points more of the lost wage and moves demand by under 0.014 / 0.004% of GDP: the cap moves who bears
    the loss, not demand (G3, restated to the binding window).
  - **The tail is families plus rigid money wages**: gap −9.27%, about twice 2009's ((b) −4.48), inflation 0.64% ((b)
    1.3), 6.75 years at the floor ((b) 3.5), 30.7% of the lost wage covered by year 15 ((b) a third) — the deepest run
    of all, its depth set partly by A2.
  → On the refit (Log 46; decisions 78-79: benefits follow the current money wage; rigid money wages fall at most 4% a
    year, the log excess costing a share of the jobs left): both artefacts are gone — coverage of the lost wage stays at
    55–84%, and no rigid-wage run reaches the employment floor. With them gone the constrained households deepen both
    branches a little (owners' saving −7.49 against −7.23 pooled) instead of cushioning the falling one; state support
    halves the job losers' drag (−0.93 against −1.98% of GDP at year 12); networks run out again (at their cap to year
    15, 28–31% of the lost wage covered); the tail is −12.1%, 7.25 years at the floor. The old rules are sensitivities.
- **Could it become a Great Depression, worldwide?** (her call, 2026-09-24: the single-country layers look soft on
  unemployment; bring in the US, Europe and China; the big picture, not a bank; `code/global_crash.py`,
  `results/global_crash.json`, `figures/fig_global_crash.png`, `figures/fig_global_crash_validation.png`; checks
  `checks/check_global_crash.py`, 12/12). My pushback first: the paper's structural job loss is already Depression
  scale (16% of jobs by year 10, 30-42% by 15 — on (b); on (c) about 37–49% by year 10 and 55–72% by 15, the deposits
  and bank entries); what was soft was the amplification — slow, supported, linear, with
  banks and policy working. Built four regions (US, euro area, Sweden, China) with four amplifiers: recessions
  trigger adoption (cyclical job loss turning permanent), bank capital and credit spreads (a money channel when
  deposits are uninsured), trade and a shared risk mood, and rules that can change (policy, support, fiscal, deposit
  insurance, backstop, tariffs, anchoring). **Validated first**, one parameter set, by month since 2026-10-28
  (decisions 91-92: `code/episodes.py` fits and stores it, `results/episodes.json`; restated then, in brackets the stored
  quarterly fit's values before it, refit 2026-10-26 after a sign error in the 2008-10 run's housebuilding term, Log
  41): fourteen parameters by a global search on nine episodes by month with measured shocks (stocks, exports,
  housebuilding; the 1930-33 bank runs on the money stock's measured fall), each target at the frequency it is
  measured: loss 424.54 on 966 points; the spread per unit of capital lost (sigma) 2.69 [3.21], US Okun 0.68 [0.71],
  the bank-run channel (money) 6.92, which bites only without deposit insurance [9.5], debt deflation 0.5 at its bound,
  levelling off at an 11.4% shortfall [0], a_r 0.03 at its bound [0.03]. US 1929-33 with the 1930s' rules: 1933 output
  0.71 of 1929 against 0.74; prices 0.70 against 0.75 on the year's average, still falling in December 1933 where the
  data's turned in March; unemployment 26.3 against 24.9 [0.71, 0.71, 27.3]. 2008-10 with today's: trough -6.4 against
  -6.3, unemployment's peak 9.32 against 10.0, eight months early [-7.2; 9.85 against 9.9 by quarter]. The fit misses
  1981-82 and 1937-38, which carry over half its loss (117.9 and 119.0; V5). **Out of sample, the dot-com bust**
  (2000-03, today's rules, measured household equity, equipment and exports; not in the fit; check V4): unemployment
  peaks at 5.89 in March 2003 against 6.30 in June and output's trough is -2.8 against -3.9; unemployment's RMS error by
  month 0.50, the gap's 1.24 [by quarter: 6.31 against 6.13, -3.3 against -3.9, RMS 0.66 and 1.11]. The search (scipy's
  `differential_evolution`, `episodes.fit`) is sensitive to the scipy version in the last bits (results stored under
  scipy 1.18.1). Regenerating it means regenerating `global_crash.json`, `pace.json` and `case.json` after it, in that
  order. Known bias: unemployment recovers from 2009 faster than the US's did (end-2010 7.6 against 9.3), while the gap
  does not — optimistic about how long joblessness lasts (V3). The fit makes interest rates a weak lever (a_r 0.03 at
  its bound, the literature's low end) and debt deflation a strong one at small shortfalls, its slope at its bound and
  its levelling-off weakly identified (decision 92). Start values measured on the dated vintage since 2026-10-26
  (decision 67: US unemployment, policy rate, core PCE, equity wealth from Z.1; the ECB's rate, euro-area unemployment
  and core HICP; Sweden's; since 2026-10-27 France and the rest of the euro area, decision 70), household debt on the BIS
  as cached in `cache/` (for the euro area's two parts, the BIS's own, in the vintage); since 2026-10-28 relief measured
  from each central bank's rate over the year to the start and the neutral rate HLW's latest (decision 91); the rest
  approximate, stated. Policy is dated, not triggered (decisions 81 and 91): each preset's levers start in the month its
  triggers fired in its central run (`preset_dates`; today's rules: the US and Sweden February 2028, France June 2028,
  the rest of the union September 2028, China August 2030). Findings on the monthly fit (decisions 91-92: the levers on
  those dates, the fit's debt deflation acting forward), the bust on the 2000-02 bust's measured path (decision 66), the
  vintage's start, France a region of its own (decision 70) (year 4; restated 2026-10-28, in brackets the stored
  quarterly fit's values before it, Log 45):
  - **Today's rules, the bust alone**: a world recession about 2001's depth, smaller than 2008's — the four 2.2% below
    capacity, the US 2.4%, US unemployment to 5.8% [2.1%, 3.2%, 6.4%].
  - **With the paper's displacement and recessions triggering adoption**: a jobs crisis larger than the output one — US
    non-employment +12 points (unemployment 9.2%, 7 points out of the labour force), US output 7.0% below capacity, about
    2008-10's trough [+10 points, unemployment 7.9%, output within 5% of capacity: a jobs crisis without an output
    one]. The US and Sweden lead (F6) [the US alone].
  - **When the rules erode** (austerity, no backstop, tariffs, looser anchoring): a world depression, over twice
    2008's — the four 15.6-20.4% below capacity, US unemployment 15-19%, US banks' capital 72-98% gone [8.8-11.3%,
    12-15%, 70-94%: about twice 2008's]. The 1930s' rules on today's debts are a depression (the four 54-56% below
    capacity, US unemployment 33-40%) [28-35%, 30-33%].
  - **When the rules expand** (an income guarantee at 90% of lost labour income, from its dates): by year 4, with today's
    stimulus still running, output no better than under today's rules (the US 5.4-6.0% below capacity, Sweden 9.0-9.8%),
    at up to 2.9-3.9% of US GDP a year; by year 6, after today's stimulus has run out, every region's output is closer to
    capacity than under today's rules (F4) — but US non-employment is still up 7-12 points by year 4: the guarantee
    holds demand, not jobs. No inflation surge in four years. (Year 4, with displacement, uniform and robotics two years
    out; before 2026-10-28 output held within about 5% (the US 4.6-5.0%), at 2.6-3.5% of US GDP a year, 7-11 points.)
  - `[inferred]` What makes a Depression is not the shock but the rules' response, as in 1929-33: on the monthly fit the
    same bust is a 2001 under today's rules, about twice 2008 when they erode (the US 11.8% below capacity by year 4),
    and deeper than 1929-33 under the 1930s' rules (the four 48.9% below). The AI-specific danger is the jobs crisis
    that today's rules do not prevent; on the monthly fit output follows jobs down after year 4 (the jobs-crisis row by
    year 6: US non-employment +26.8, output 13.2% below capacity) [before it, output recovered while jobs did not].
    Sweden's exposure is overstated here: the model
    has no exchange rates, and the krona's fall is Sweden's historical cushion (leaving gold in 1931, 2008-09); and its
    core inflation starts at 1.12% against its 2% target, so its price level falls behind the path its debts were
    written for from the start and the fit's debt deflation weighs on it most (D11).
- **Two waves, and Baumol concentration** (her calls, 2026-09-24: robotics is a year or two out at least; most job
  growth is going to women — care and other labour-intensive work, Baumol concentration? `code/exposure.py`,
  `code/baumol.py`, the split in `code/global_crash.py`; `results/exposure.json`, `results/baumol.json`,
  `figures/fig_baumol.png`, `figures/fig_global_crash_waves.png`; checks `checks/check_exposure.py` (20/20 with the
  care measures) and `checks/check_global_crash.py` (31/31 with the absorber)). Measured (ILOSTAT): cognitive work
  (ISCO 1-4) is 61% of US employment, 56%
  of the euro area's, 65% of Sweden's, 20% of China's; physical work (6-9) 70% of China's; cognitive work pays 1.14-1.22
  times the average. **Recessions cut physical work 2-3 times as fast as the whole** (US 2007-10: physical -11%,
  cognitive -3%; Spain and Sweden the same shape), so before robotics only 37% of a US recession's job loss is in work
  AI can take (6% of China's). In the crash model the drift and the adoption in recessions act only on work that can
  be automated at the time; the displaced carry their group's pay, support capped near average pay (approximate).
  The split nests the uniform case exactly (M4), and the fit and the earlier rows are unchanged. Findings (today's
  rules, year 4; [restated 2026-10-28 on the monthly fit, the levers on their stored dates (decisions 91-92); in brackets the values before it, Log 45]):
  - **The robotics lag holds the jobs crisis back; it does not prevent it.** US non-employment's rise in the jobs-crisis
    row: +12.2 points uniform, +11.3/+10.0/+8.4 with robotics 1/2/3 years out; by year 6 the physical wave arrives in a
    weak economy (+24.1 with a 2-year lag, above the uniform case's year 4) (W1, W2) [+10.5; +10.1/+8.8/+7.5; +17.9].
  - **The first wave costs more per job**: output falls 0.72 points per point of US non-employment with robotics 3
    years out against 0.57 uniform — fewer people out of work, each losing 1.2 times the average pay with support
    capped. Holds with no discretionary fiscal response (W3, W5) [0.59 against 0.46; with no fiscal response 0.70
    against 0.54].
  - **China waits for robotics** (its exposure is physical); the US, Sweden and the euro area take the first wave.
  - A model artefact, stated until 2026-10-28: the fiscal response started when unemployment was 2 points up, so a split
    that raised unemployment more slowly delayed it, and China's output looked slightly worse with the lag for that
    reason alone. Since decision 91 the levers start on each preset's stored dates whatever the run, so the artefact
    is gone; with no discretionary fiscal response China's output is better with the lag (W5).
- **Baumol concentration, measured** (`code/baumol.py`; stated as found):
  - **US payrolls, Aug 2024 - Aug 2026: health care and social assistance added 1,342k of 1,318k net jobs (102%); the
    rest of the economy shrank; women took 76%.** The last 12 months: 91% and 82%. Care is 15% of payrolls; its share
    of growth in each expansion since 1991 was 14-34%. Jobs outside care shrank over 12 months while the headline grew
    for 14 months (June 2025 - July 2026); since 1990 that had lasted 1-3 months, at recession onsets (2001, 2008)
    and in jobless recoveries (1992, 2003, 2010).
    **Qualified (log 32, 2026-09-30; FRED USPRIV, USGOVT, CES9091000001 and CES6562000001, 1 Oct vintage, not in
    `baumol.json`): outside care the net loss is government's.** Over the 24 months private employers outside care
    added 89k while government shed 113k (federal −337k, state and local +224k); over the 12 months to August federal
    employment fell 242k while private jobs outside care grew 269k. So "the rest of the economy shrank" is federal
    cuts, not private weakness. The 14-month episode was not all federal: in its 12-month windows to June 2025 – May
    2026 private jobs outside care fell as well (by 41k–390k; government was still growing to September 2025), and
    federal cuts weighed from October 2025 (−256k to −325k over 12 months); in its last two windows (to June and July
    2026) private jobs outside care grew (+52k, +128k) and the loss was federal.
  - **Germany likewise** (health and social work 74% of net employment growth 2022-25, manufacturing -282k); the
    Netherlands 35%; **Sweden not**: care flat at 14.9% of employment 2019-25 — yet women took 98% of Sweden's net
    growth 2022-25 (men's employment flat). France, Italy and Spain grew in hospitality, not care.
  - Care is 72-81% women everywhere measured; it pays below the average in Sweden, Germany, France and the
    Netherlands (0.83-0.87), and US education and health hourly pay has slipped from 1.01 of all private pay (2010)
    to 0.97. It absorbs jobs, not pay.
  - It is paid for mostly by the state: Medicare and Medicaid benefits come to 64% of US consumer spending on health
    care (the employers are private: 7% public); Swedish and most euro-area care is tax-financed. It grew 5% through
    2008-10 while payrolls fell 6% and fell 11% in 2020 (the in-person shock); US state and local government shed 726k
    jobs in 2008-13 (austerity on the public side).
  - Baumol's premise in prices, US: health care's price doubled against goods since 1990 and its spending share rose
    13.3% to 17.0%; 1990-2008 is consistent with the paper's sigma_H < 1 branch (implied 0.25), but since 2008 the
    share rose while its price fell against all consumer prices — the recent concentration is volume (ageing,
    coverage), not the price-driven concentration of the proposition.
  - `[inferred]` The paper's "aggregate rescue, median collapse" on the employment side may be starting to show in the
    US: job growth is concentrating in the human-required set, three-quarters women, at below-average and slipping
    relative pay, financed publicly. But the net loss outside care over the window is federal cuts, and private jobs
    outside care grew, so it is not yet private employers shedding work (the qualification above). For a crash, what
    holds employment up in an ordinary recession is a fiscal decision: under today's rules care kept hiring through
    2008-10; under eroding rules it is what austerity cuts. And the displaced
    (cognitive now, physical later; the physical wave mostly men) are not the people care has been hiring.
- **Care as the absorber** (her calls, 2026-09-24: build it; "there must be a limit to how much care can absorb";
  `global_crash.py` with `Waves(absorb=True)` and the rules' `care` setting, `exposure.care()`,
  `figures/fig_global_crash_care.png`; checks C1-C11 in `check_global_crash.py`, E7-E9 in `check_exposure.py`).
  The displaced (robotics two years out) can move into health and social work within three limits, each measured
  where it can be:
  - **the ceiling**: care, trend and build-out together, never past the largest share any rich economy employs
    today — Norway's 20.1% of employment (Denmark 18.7, Netherlands 17.3, Finland 16.8; the US and Sweden 15, the
    euro area 12.5). Room: about 5 points of employment in the US and Sweden, 7.6 in the euro area;
  - **the gate**: men work in care at a quarter of women's rate in every region (US 0.26, Sweden 0.28), so the
    displaced move at 0.65 (cognitive work, half women) and 0.41-0.45 (physical, a fifth women) of a woman's rate;
  - **the pace**: care's own trend (0.2 points of employment a year in the US and euro area, 0.1 in Sweden), and a
    funded build-out of up to a point a year under "rules expand into care" (approximate: Sweden's municipal build-out
    in the 1970s-80s); a quarter of the willing trained and hired each quarter (approximate; 0.10-0.50 tested).
  Findings (year 6, the jobs-crisis row unless stated; on non-employment since the measured US; [restated 2026-10-28 on the monthly fit, the levers on their stored dates (decisions 91-92); in brackets the values before it, Log 45]):
  - **Care's trend jobs exist anyway**: the displaced who take them take them from people who would have entered
    work — US non-employment +24.1 to +24.0 points, output no better (C4) [+17.9 to +17.4].
  - **A funded build-out works, at its pace**: a point of employment a year takes US non-employment from +24.1 to
    +16.6 at 1.1% of GDP a year, care at 19.7% by year 6, short of Norway's 20.1%. Three points a year reaches the
    ceiling and gains under a point more (+15.7), and without the ceiling 3.1 more again (+12.6, care at 22.9%). In the
    US **the ceiling binds before the pace** (C5, C6) [+17.9 to +12.6 at 0.9% of GDP, care at 19.3%; three points +11.3,
    without the ceiling +9.1 at 22.2%: both the pace and the ceiling bound].
  - **It cannot rescue the jobs crisis**: 9.6 points of US employment are still displaced at year 6 against 5.3 of
    room (C7) [7.9]. With displacement alone the build-out takes 5.1 points off Sweden's unemployment (27.1% to 22.0%,
    care at 18.2%): there the gate and training bind, not the ceiling (C8, C11) [it nearly rescued Sweden: 13.6% to
    11.3%, care at 17.5%].
  - **Care buys jobs, the guarantee buys demand**: per point of GDP a year the build-out takes 7.0 points off US
    non-employment against the income guarantee's 1.5, and the guarantee holds output closer to capacity (-5.5%
    against -8.7%) (C9) [5.9 against 1.3; -4.7% against -5.5%]. Eroding rules end it: care takes in nobody
    (C10). The physical wave is under-represented among those care takes in (US: 26% of the absorbed against 45% of
    the displaced) (C3) [42%].
  - Her observation, open: **Norway has its fund.** `[inferred]` The ceiling is then a limit of financing more than of
    need: Norway pays for part of its public spending from the fund's return — capital income, not wages — which is
    the paper's mechanism in small (a rent financing human-required work; Proposition "Baumol concentration" (iii)).
    First look (E9): across 15 rich economies care's share rises with the public sector's share of employment
    (correlation 0.61), but employer type is not financing (Dutch care is private and publicly paid; Swedish public
    employment is high and its care share middling). If financing sets the ceiling, then a fund or tax on the owners'
    AI income could raise it — within need and the gate, which money does not move.
- **Is care's ceiling need or financing?** (her calls, 2026-09-24: test the financing link; "Norway also has their
  sovereign wealth fund"; "even if they don't draw from the fund, the fund's existence may lower their borrowing
  costs"; `code/financing.py`, `results/financing.json`, `figures/fig_financing.png`; `checks/check_financing.py`
  10/10). Three questions, stated before fitting; data from the OECD health accounts and Economic Outlook, ILOSTAT,
  the World Bank and Statistics Norway. Stated as found:
  - **Financing, not need.** Across 34 OECD economies (Norway on mainland GDP), public spending on long-term care
    goes with care's share of jobs (R² 0.66; 0.64 among the 25 richest); income less (0.46; 0.14 among the rich);
    need — the share aged 65 and over — not at all (0.04; 0.00). Together: public long-term care t 6.3, income t 2.7,
    age t 0.6, R² 0.79. Caveat, stated: spending and employment are partly the same thing (the spending pays the care
    workers), so the fit is partly an identity; what the test establishes is the negative — two economies of the same
    age employ very different amounts of care, and the difference is what the public purse commits (Japan, the oldest,
    13.5% of jobs in care; Norway, younger than the OECD average, 20.1%).
  - **Norway commits the most**: public long-term care 3.7% of mainland GDP, the highest in the OECD (Sweden 3.4,
    Denmark 3.0); on mainland GDP it sits on the line (+1.0 point; on total GDP, which oil and gas inflate, it looked
    3.2 points above). Sweden sits below it (-2.9: much spending, fewer care jobs).
  - **The spending channel**: the fund's transfer into the state budget (the state's net petroleum cash flow less its
    net transfer to the fund) was 7-11% of mainland GDP in 2019-25 — two-thirds of Norway's whole public health and
    long-term care bill or more every year, above all of it in 2020, 2021 and 2025 (2025 health spending provisional).
    Money is fungible: the fund finances the budget, not care as such; the point is its size. **In a crisis the fund
    pays**: the transfer jumped to 13% of mainland GDP in 2020, the highest since 2010.
  - **Her balance-sheet channel**: across the OECD in 2010-24 (year effects), a government's long rate rises 4.6 bp
    per 10 points of net debt; without a central bank of its own (the euro area) 15 bp, 30 bp in the 2010-13 crisis
    against 17 bp in calm 2015-19; with its own central bank under 1 bp. Norway is a net creditor of 1.5-3.5 times
    GDP every year since 2012 while still borrowing (gross liabilities 35-51% of GDP). `[inferred]` So the fund's
    value is not cheaper borrowing in calm years — every AAA state borrows at about the same — but that the price of
    debt cannot bind in a crisis, which is what turns a bust into austerity in the crash model's eroding row.
  - `[inferred]` What this means for the crash model: the ceiling (Norway's 20.1%) is the most care any society has
    financed, not the most anyone needs. What finances care in a bust is the wage base (taxes and contributions on
    labour income, which displacement shrinks), deficits (priced as above), or capital income routed to the state —
    Norway's fund, or its analogue for AI rents. The paper's mechanism, applied: care paid for out of wages shrinks
    with its own tax base exactly when displacement needs it to grow; care paid for out of capital income does not.
- **The financing limit in the crash model** (her call, 2026-09-24: go ahead; `global_crash.py` with the rules'
  `care_finance`, `financing.labour_taxes()`, `figures/fig_global_crash_financing.png`; checks K1-K7 in
  `check_global_crash.py`, 38/38). Norway's share becomes a marker; the build-out is limited by what pays for it:
  - **taxes on labour income**: up to the highest take in the OECD (Austria, 27.9% of GDP; measured, OECD Global
    Revenue Statistics: the US 16.3, the euro area 24.3, Sweden 25.5, China 7.6), on a wage base displacement
    shrinks; the workers taxed spend half of what they pay (approximate);
  - **borrowing**: no quantity limit; the measured price of debt (the euro area 15 bp per 10 points, 30 when its banks
    are under stress; under 1 bp with a central bank of one's own), passed to private borrowers' spreads;
  - **a levy on AI income**: half the pay the displaced lost, now owners' income (a dial); owners spend like the
    representative household, so the levy costs no demand here. What a source cannot cover is borrowed.
  With the price of debt at zero every earlier run is reproduced exactly (62 runs); at the measured price 22 move by at
  most 0.05 points of unemployment. Findings (the jobs-crisis row, robotics two years out, year 6; [restated 2026-10-28 on the monthly fit, the levers on their stored dates (decisions 91-92); in brackets the values before it, Log 45]):
  - **At a point a year the pace binds first**: US non-employment +16.6 borrowed, the same capped at Norway's share —
    the sources do not differ (K7) [+12.6].
  - **At three points a year financing decides**: the levy and borrowing take US non-employment's rise to +12.6 (care
    at 22.9% of employment); taxes on labour to +14.5 (K5, K7) [+9.0, care at 22.2%; +10.2]. **Taxes on labour lose
    room as need grows**: the US room falls from 11.6% of GDP to 6.4 as the wage base shrinks; Sweden's, already near
    the top, from 2.4 to -3.5, below zero, and its build-out stalls at 16.8% against the levy's 20.7% (K3) [the US to
    7.7; Sweden to 1.1, its build-out level with the levy's, 18.05% against 18.03%].
  - **The levy gains room as displacement grows** (the US from 0 to 4.1% of GDP) and never binds in the US, the euro
    area or Sweden: the same jobs as borrowing, with no debt (K4) [3.4%].
  - **The price of debt does not bind at a build-out's size**: under 5 bp everywhere outside France, the rest of the
    euro area included, with at most 2.9% of GDP added over six years; France's spread rises 23.3 bp with 7.8% of GDP
    added, 21.4 bp and 7.2% of it its banks' recapitalisation, not the build-out (the levy's run, which borrows nothing
    for the build-out) (K6) [under 5 bp everywhere, at most 2.4%]. What limits a care build-out is not the bond market
    but the base it is taxed on.
  - `[inferred]` The paper's mechanism, in public finance: a welfare state financed from wages shrinks with its own
    base as income moves to owners; one financed from capital income — Norway's fund, or a levy on AI income — grows
    with it. Caveats: the levy's share and the taxed workers' spending are approximate; existing public spending on the
    shrinking base is held, not modelled; China's labour-tax room (20% of GDP on paper) is not a realistic limit.
- **Output without work, measured; the crash model on the measured US** (her question, 2026-09-25: output and GDPNow
  nowcasts rising while the US sheds labour — does it fit, is AI pushing manufacturing?; then her call on the three
  changes. `code/decoupling.py`, `results/decoupling.json`, `figures/fig_decoupling.png`, `checks/check_decoupling.py`
  6/6; the participation margin and the measured build-out in `global_crash.py`, 43/43; the watcher's tripwires in its
  own repository). Stated as found:
  - **The paper's mechanism in the national accounts**: since 2023Q2 US business output has grown 2.75% a year while
    hours grew 0.23%; output per hour 2.5% a year against 1.6% in 2015-19. Labour's share of business output is at its
    lowest since 1947 (93.4, 2017 = 100), down 3.3 points in a year — a fall that since 1990 only recessions and their
    recoveries matched.
  - **The nowcast**: GDPNow puts 2026Q3 at 5.1% a year; its final nowcasts have missed published growth by 1.2-1.4
    points on average (3.7 in 2025Q4).
  - **AI lifts a narrow slice of manufacturing**: since 2019 semiconductors +69%, computers +28%, power generation +11%;
    all manufacturing +0.1%, manufacturing jobs -1%.
  - **The build-out leaks abroad**: computer imports rose from 0.7% of GDP (2022) to 1.9% (2026Q2), more than
    investment in information processing equipment (+0.7); net of them the build-out is 0.4 points of GDP below its
    2015-22 trend (0.2 below its 2022 level) — the crash model had assumed 1.5% above. Restated 2026-10-26 (decision
    68): the measure had read all equipment (Y033) as information processing equipment (Y034), and on it the net was
    0.3 above trend. Data-centre buildings are not in the measure (lower bound).
  - **The displaced leave the labour force**: since the prime-age employment peak (September 2024) 94% of the fall in
    the employment rate is participation (unemployment +0.1); 12% in 2007-10, 36% in 2000-03. Small changes: survey
    noise is a few tenths.
  - **In the crash model** (the US measured, the other regions as before): the US exit share takes structural
    displacement out of the labour force; cyclical job loss stays unemployment. Measured unemployment then shows under
    the jobs crisis: in the jobs-crisis row (robotics two years out) US unemployment reads 13.6% at year 6 while 14.7
    more points have left the labour force (non-employment +24.1) (X3). The findings hold on non-employment: the
    jobs-crisis row +10.0 points by year 4 with US output 6.5% below capacity; the care build-out takes 7.5 points off
    by year 6; the robotics lag, the pace and the ceiling, the financing sources keep their order. The measured
    build-out makes the US bust milder: with nothing above trend the US has no capex leg, against the 1.5% assumed, which
    would have cut over a point deeper by year 4, with today's stimulus on its dates and without discretionary fiscal
    policy alike (X2): the imported servers' collapse lands abroad. **Displacement without a bust** (where the US is),
    the presets' levers on their stored dates: by year 4 US output 0.6% below capacity under today's rules and 1.2%
    under the guarantee; by year 6 today's stimulus has run out and output is 4.7% below capacity, the guarantee's 2.7%;
    non-employment up 9.5 and 8.3 points by year 6 (X4). The comparison of fiscal triggers keyed to unemployment and to
    non-employment, and X5's (in a bust the triggers fired either way), went with the triggers (decision 91).
    [restated 2026-10-28 on the monthly fit (decisions 91-92); before it: unemployment 10.2% with 11.9 points out
    (+17.9); +8.9 by year 4 with output 4.6% below; 5.3 off; X2's year-4 US gap without discretionary fiscal policy -5.4%
    against -6.8% assumed, with today's triggers -3.2% against -3.7%; without a bust, triggers keyed to unemployment
    -2.5% by year 4 against -0.7% keyed to non-employment, -2.7% against -4.5% by year 6, the guarantee -2.7%.]
  - The synthesis page ("After the Wage") revised on her call (2026-09-25): people out of work in place of unemployment,
    output without work added as a finding, plain wording throughout (her rule for outside readers).
  - **Corrected (log 27):** the 94% exit share is an endpoint measure from the employment peak, and the fall it measures
    came in one month: prime-age participation held 83.0-84.0% from 2023 to May 2026 and fell 0.6 points in June 2026.
    From other bases it is 0.59 (the 2024 average) or 0.18 (the 2023-24 average); on trends since 2024 participation is
    not falling and the exit share is negative — the displaced, if any, show up as unemployment. The crash model still
    carries 0.94 (decision 21).
- **The pace against what has been seen** (her question, 2026-09-25: is the model calibrated to the participation, output
  and hours changes already seen?; then her call to open it as a unit. `code/pace.py`, `results/pace.json`,
  `figures/fig_pace.png`, `checks/check_pace.py` 8/8, 10/10 since 2026-10-28; no change to `global_crash.py`). Before this unit the US exit share
  and the build-out were measured; the pace — `drift`, a point of the labour force a year — was the paper's, set by hand.
  Stated as found (September 2024 to August 2026, prime-age rates; endpoints on 3-month averages, trends by least squares
  with Newey-West errors):
  - **The trends show little yet.** Non-employment +0.05 ± 0.09 points of the labour force a year since the peak (+0.10
    ± 0.05 since January 2024); prime-age unemployment +0.17 ± 0.05 a year, significant; exits −0.11 ± 0.12 a year
    (participation not falling). The endpoint from the peak (+0.68, of which 0.64 exits) rests on June 2026 (A1-A3).
  - **The paper's pace runs far ahead of it.** Over the window the model at the paper's pace (today's rules with no
    lever, no bust, robotics not arrived, care at its trend) raises US non-employment 1.9 points (1.0 exits, 0.9
    unemployment; the gap −1.3). The trend's upper bound allows 0.218 of the paper's pace, the endpoint 0.39, the trend
    itself none: the model's start alone raises non-employment 0.11 over the window, the trend's 0.10 (A4). All
    of the observed change is attributed to displacement, so each is an upper bound on AI's. Restated 2026-10-28 on the
    monthly fit (decisions 91-92): the model now raises non-employment more over the window, so a slower pace fits what
    was seen [0.244, 0.423 and 0.007 before; 1.8 points at the paper's pace (1.0 exits, 0.8 unemployment; the gap −1.0)];
    on 2026-10-26 the corrected crash model had let a faster one fit (0.15 and 0.29 before the sign fix). `[inferred]`
    The bound is read through the model, so it moves with the model: a bound on AI's pace that depends on the fit is
    weaker evidence than one read off the data alone.
  - **The response to a bust carries the danger, not the pace seen so far.** At 0.218 of the paper's pace a
    dot-com-sized bust on its measured path and sizes under today's rules takes US out of work to 9.5% (17.4% at the
    paper's pace), and to 26.1% when the rules erode (34.9%); displacement without a bust to 5.4% (12.1%) (A5). The
    fit's debt deflation carries much of the rise: with it off, 7.2%, 15.8% and 5.4% (13.7%, 23.5% and 11.8% at the
    paper's pace) (A9) [restated 2026-10-28 on the monthly fit (decisions 91-92); at 0.244 on the stored quarterly fit:
    8.2% (14.4%), 16.7% (24.8%), 6.1% (10.6%)].
  - **The spending loop is not identified here.** Across the paces the data allow, the model's gap accounts for a fifth
    to over half of the CBO gap's fall (−0.15 and −0.39 against −0.69, from an overheated +1.5; restated 2026-10-28 on
    the monthly fit, −0.12 and −0.35 before); the rest may be that unwinding (A6). An
    endpoint fit tried first matched the exits and the gap with 0.71 of the paper's pace and 43% of the lost-pay spending
    cut left unoffset; dropped, since it rested on June 2026.
  - **Two sensitivities (her questions).** Care hired 0.39 points of the labour force a year over the window, twice the
    model's trend (0.20). Counting all of the excess as displaced people it took in — an upper bound, since care hires
    mostly women and new entrants — raises the paces the data allow to 0.45 (the trend's upper bound) and 0.59 (the
    endpoint) on the monthly fit [restated 2026-10-28 (decisions 91-92); 0.485 and 0.627 before; 0.35 and 0.47 before the sign fix]: still under two-thirds of the paper's. Counting all care hiring as non-employment would double count real jobs the
    model already hires at its trend. The build-out's own jobs are too few to matter: all of construction's gain is 0.06
    points of the labour force, and manufacturing lost 0.07 (A8).
  - `[inferred]` The model's central runs describe what the paper's pace would do, not what has been seen. The data do
    not refute the mechanism; they bound the pace so far. What would move the bound: participation staying down after
    June (two more quarters), or non-employment's trend clearing two standard errors. **Restated on (c)
    (2026-10-01):** this reading first reconciled the bound with the macro block because the block's own paths held
    participation up in the early years while the real wage rose first — true of (b) (on the low root its employment
    rate rises 0.05–0.10 points of population a year over years 0–3, slow / medium; the high root's medium path +0.20),
    not of (c)'s central reading, where it falls from year 0
    (0.13–0.19 a year on the slow path, 0.23–0.35 on the medium, by root) and the real wage never rises first. So the
    data now bound the macro block's clock as well as the crash model's drift (the units — employment over population
    against prime-age rates — and the dating of year 0 are approximate). The measured-site variant (ii) is the reading
    whose early years are not a loss (its high root's participation rises over years 0–6).
- **Her case: what we think is happening** (her call, 2026-09-25: pin down one case across the model, the watcher and
  the website. `code/case.py`, `results/case.json`, `figures/fig_case.png`, `checks/check_case.py` 17/17, 19/19 since
  2026-10-28). Her
  leanings: deficit and sovereign worry; recession and failing consumption demand; a stock bust bigger than dot-com;
  care capping out as the absorber; reckless US tariffs, Europe more sensible but still austere; a process under way
  for two to four years that accelerates as AI companies change behaviour. The settings are decisions 23-27, 66-68
  and 91 (the levers dated).
  **Redone 2026-10-26 on her delegation** (Logs 42 and 44: well calibrated, on new data, fitting the pop now seen): one
  start for the case and the model, a dated vintage (decision 67); the bust 1.5 times the 2000-02 bust's measured sizes
  on its measured path, dated from the day of today's peak, 6 Oct 2026, as 2000's is from 10 Mar (decision 66 as amended
  in Log 44); the build-out measured as information processing equipment, which leaves nothing above trend in the US
  (decision 68); no premium on US borrowing, her leaning kept as an alternative (decision 69); France a region of its
  own (decision 70) and the euro area's premium France's (decision 71); the October bust's energy run as an
  alternative. The 8 Oct case, which the 16 predictions were derived from, reproduces at the tag
  `paths-pre-signfix` (14.4–15.7% at 2028Q4 against 10.1%); on the corrected fit with its ramp and the stored start it
  read 11.0–12.0% against 7.6% (Log 41). **Restated 2026-10-28 on the monthly fit** (decisions 91-92): the case runs
  by month, and each region's fiscal lever starts the month after its unemployment first reads two points above its
  start (acting from the next month, as a trigger did),
  the midpoint of the case's low and high ends to the month (the US's stimulus from August 2027, Sweden's cuts from
  October 2027, France's from December 2027, the rest of the union's from February 2028, China's stimulus from March
  2030), the same dates in every piece, sensitivity and alternative; the fit's debt deflation acts in it (K14). Stated
  as found on 2026-10-28 (Log 45's values, on the stored quarterly fit with France, in its entry; Log 44's and Log
  42's in theirs), on the one dating at a monthly step (decisions 43 and 91: index 0 is the state measured on data to
  September 2026, the end of 2026Q3; index k the end of the k-th month after; a reading named by a quarter is its
  months' average, 2026Q4 the quarter of the peak; 73 months, to 2032Q3):
  - **The data so far fit the measured path, not the 8 Oct timing.** On 2026Q4's average the case has US household
    equity 2.5% down (4.7% at the quarter's end: 2000's fall 0.712 of a quarter after its peak, times 1.5), the first
    losses on AI lending, and US out of work at 4.36% (unemployment 4.34%); the 8 Oct timing puts it at 4.98%
    (unemployment 4.96%; claims to 17 Oct point to about 4.2) (A1). The
    Nasdaq's 2026Q4 average to 23 Oct is 2.6% above its 2026Q3 average and 6.0% off the 6 Oct high, 17 days on, against
    2000's 1.8% at the same day count (2.7% at the case's size): ahead of the case's path so far, not behind it. The
    path: US household equity 66.8% down at its deepest month's end, April 2029 (64.9% on 2029Q2's average; 2000-02's
    double bottom, 2002Q3 and 2003Q1, dated from the peak's day), then recovering as in 2003-05; the build-out keeps
    growing to 2027Q3, then falls (abroad: the US has none above trend, decision 68); the losses on AI lending (2.25% of
    US loans in all) are heaviest in 2029Q1 (K4).
  - **Through 2028 the case is well defined, a sixth to a quarter above the model's central run** (which carries the
    same measured bust at the dot-com size, dated by the quarter, today's rules on their stored dates): US out of work
    7.7–8.1% on 2028Q4's average against 6.5% (1.17–1.24 times); the four economies' output 4.0–4.2% below capacity
    (K7).
  - **After 2028 it depends on one lever.** By 2032Q3 US out of work is 22.7% if firms automate the usual share of the
    jobs they cut in the downturn and 31.9% if twice it (21.6–29.9% at 2032Q2), still rising at both ends; the four
    economies' output 14.1–16.9% below capacity at worst. Both ends are a labour depression (K7-K8): output is no longer
    held (more than 10% below capacity, short of the 20% that would make a depression). Sweden reaches the model's 50%
    cap from 2032Q1 at the high end (46.5% at the low end's peak). The model's central run is now itself a labour
    depression with output held (US out of work 18.1% at its peak, the four 8.9% below capacity at worst).
  - **What drives it depends on when.** By 2028Q4 the bust and the tariffs add the most, 1.2 and 1.1 points of US out
    of work; adoption 0.4, Europe's austerity 0.3, care capping out 0.2, France's premium nothing. By 2032Q3 adoption
    (9.2), then the bust (5.3), the tariffs (4.0) and Europe's austerity (2.1); care (0.4) and France's premium (0.2)
    under a point each to the US (K9-K10). Europe's and Sweden's cuts add 8.3 points to the rest of the union's peak,
    8.2 to France's and 5.4 to Sweden's (44.6% without them, at the cap with them). Each piece is the case minus the run
    without it, the difference of the unrounded runs' quarterly averages rounded once.
  - **France** (decision 70): out of work 13.3–13.4% at 2028Q4 (unemployment 8.2% at the start), 34.5–41.4% at the
    peak, against 10.2–10.4% and 29.8–36.5% in the rest of the union; its output 18.3–20.7% below capacity at worst,
    its private borrowers' spread up to 2.6 points. Its government's premium adds 2.1 points to France's out of work at
    the peak and 0.2 to the US's; the ECB capping its spread half a point above the start (TPI) takes 1.4 off France's
    peak, and two points of premium rather than one add 2.1 (case.json `alternatives`).
  - **Her acceleration story is milder than the model's central assumption.** The case starts at the pace seen so far
    (0.218 of the paper's on the monthly fit; 0.244 on the stored quarterly fit, 0.147 before the sign fix); taking it
    back to the paper's pace adds 1.4 points at 2028Q4 and 3.6 by 2032Q2 (K10).
  - **The premium on US borrowing, priced** (her leaning; the 8 Oct case's setting, an alternative since decision 69): a
    point more over the first year adds 1.4 points of US out of work at 2028Q4 and 5.3 by 2032Q2 (A1).
  - **What the case leaves out: debt deflation and the rate channel move it most.** With the fit's debt deflation off
    (decision 92) US out of work is 9.4 points lower at the peak (8.4 at 2032Q2) but much the same at 2028Q4 (8.0%), the
    four economies' output 7.5% below capacity at worst against 16.9, Sweden's out of work 31.3% against the cap; its
    largest drag at the high end is 3.79% of GDP in the US, 4.04 in the rest of the union, 6.72 in France, 10.22 in
    Sweden and 4.44 in China (K14). At the Holston-Laubach-Williams estimate (a_r 0.079, against the fit's bound of
    0.03) US out of work is 5.5 points lower at the peak (5.0 at 2032Q2); the euro area stimulating takes 2.0 off (1.8),
    a looser US anchor adds 1.8 (1.5) and lowers inflation's low (−2.4% against −0.8%); Germany's spending (−1.0) and the
    exit share (−0.8) move it under 1.5 (K11).
  - **Decision 27's run** (oil stays high: dated Brent's last five prints, $121.25, held a year, then its three-year
    average, $80.71; policy on four quarters' headline): +0.5 at 2028Q4, the Fed at 4.14 on 2026Q4's average against
    3.87 (A2).
    Its price leg is met on the vintage, its bust leg is not, so it stays an alternative.
  - **What the watcher would see** (the high end): the Nasdaq rule (20% under its high) on 2000's own daily path, scaled,
    by 30 Oct 2026 at the case's size (24 days after the high; 8 Nov, 33 days, at the dot-com size), so its firing then
    is the case, not "faster"; by month, late bounds, January 2027 on the 2000-02 ratio of the Nasdaq's fall to
    household equity's (1.6 to 3.85 by quarter; "1.7 to 3.9" before, corrected 2026-10-28) and July 2027 one for one;
    the US Sahm rule in February 2027 (on the model's months after the measured ones); the model's spread, fitted to
    Baa over Aaa since decision 90, never rises 0.56 in three months. The Fed raises in October (3.96 against 3.88) and
    cuts by December (3.78; 3.87 on 2026Q4's average), and the Riksbank cuts (1.63 in October, 1.66 in November,
    against 1.75): the tests registered in Log 40, on the case's own start (A3).
  - `[inferred]` Care capping out matters little because care at its trend absorbs about a point of employment over six
    years; what would matter is a funded build-out. The deficit worry works in the model only as a price: it has no
    revenue side and no default, so the case says what a premium does to borrowers, not whether one comes.
- **The October bust — a record since 2026-10-26** (her request, 2026-09-30, paraphrased: could a bust case start in
  October, within a month?). `code/october.py`, `results/october.json`, `figures/fig_october.png` and
  `checks/check_october.py` (42/42 on 2026-10-26, against watch 8b958af) are retired with the crash model's sign fix
  (Log 41) and reproduce at the tag `paths-pre-signfix` (`git checkout paths-pre-signfix`, then the check). Not
  regenerated on the corrected fit: its successor is her case on a dated vintage (Next 11). What it found, on the old
  fit, kept because the record and the registered tests cite it:
  - Her case's settings from a start measured to 30 Sep (US core PCE 3.01, headline 3.42, funds rate 3.88,
    unemployment 4.1, the build-out net of computer imports 0.47% of GDP above trend; euro area core 2.38, unemployment
    6.4; Sweden core 1.17, unemployment 8.9); the central with the corporate spread's three-month rise (+0.09) present
    at the start, no energy term (decisions 27, 47), hands tied on four quarters' headline (decision 48): US out of work
    14.7–16.1% at 2028Q4, 0.28–0.33 above her case. The labour jump in 2026Q4 came from the equity leg (5.58 with it,
    4.35 without; scratch, Log 40).
  - **The energy term** (decisions 44–46): pass-through of crude to headline-minus-core inflation measured (US PCE b0
    0.231, b1 0.099, R² 0.70; euro-area HICP 0.171 / 0.083; Sweden 0.142 / 0.015; China none). It moved jobs little
    (about −0.1 at 2028Q4 with oil high and policy looking through; +0.13–0.15 held high); hands tied tied policy but
    barely moved jobs (at most 0.11 on matched readings, +0.16 on the main runs) at a_r 0.03.
  - **Rates, registered as tests in Log 40**: the Fed raises once more in 2026Q4 (the quarter's average 4.02 looking
    through, 4.21 hands tied) and first cuts in 2027Q1; the ECB rises to 3.14 in 2026Q4 hands tied; the Riksbank cuts in
    2026Q4 in every run.
  - **Decision 27's condition** (as amended 2026-10-01: dated Brent at least 1.25 times its three-year average on a day
    a bust rule is active) was read from a day-by-day replay of the watcher's rules as they stood before its edition 2
    (8 Oct); the replay's dates ("claims about 19 Nov", "the Nasdaq rule 27 Nov") are not deadlines (Log 40).
- **The splits tracker** (her request, 2026-10-12: many headline statistics only make sense split into a machine/owner
  side and a human/wage side — put a tracker in this thread and on the website. A panel that day catalogued 46 measures,
  measured how easily a split is found by trying cuts, and designed the tracker on her participation method; a critic
  corrected it; three reviews on 2026-10-13 (statistics, public copy, protocol) revised it, Log 38. `SPLITS.md` (the
  protocol), `code/splits.py`, `results/splits.json`, `figures/fig_splits.png`, `checks/check_splits.py` 25/25; the
  tracker's own vintages in `cache/splits/`). **Not yet fixed** (decision 62): every reading below is the starting
  point, already seen and not judged. Stated as found (monthly data to August or September 2026, quarterly to 2026Q2):
  - **How easily a split is found.** Of all 2,047 two-way cuts of the twelve payroll supersectors, 7.5% split beyond
    2 sd of their normal 12-month range in September 2026, down from 23.2% a year earlier; in normal months 1992-2019 the
    median is 0.4% and the 95th percentile 26.6%, in recessions 54.0%. Thirteen of the 15 normal months at or above
    that percentile are recoveries (the year after a recession's exclusion ends; without them it would be 10.9%). Care
    against the rest (+2.2 points a year, z 1.1) ranks 684th of the 2,047. On the panel's 24-month windows (reproduced,
    S5a) the share was 26.6% against a 95th percentile of 18.7%, down from 48.7%: measure 2 moved from "above" to
    "within the normal range" when the reviews put it on 12-month windows (decision 64).
  - **Moved the paper's way over the latest window (E ≥ +1): three of twelve.** Care: in the year to September 2026 care
    added 520,000 jobs while all other jobs lost 24,000, and care's relative pay (production workers, education and
    health) fell 1.8% against a usual rise of 0.1% (E +2.9; jobs leg +1.1). Labour's share of nonfinancial corporate
    value added 54.6% in 2026Q2 (56.1% a year earlier, 58.6% in 2019Q4), the lowest since the series began in 1947;
    adjusted for unemployment E +1.36 (the raw share +1.44: the adjustment is small). Real investment in information
    processing equipment and software +16.8% on the year against housing −3.3% (E +1.2; the year holds a rate cut of
    75 bp, so a narrowing would have fitted the rival).
  - **No clear change: the other nine.** Payroll dispersion within its normal range, 7.5% from 23.2% without a
    recession: the direction the over-hiring unwind expects. Graduates: bachelor's+ 2.6% against high school 4.3%, ratio
    0.62 from 0.64 (E −0.4). Software postings: index 77 from 65 a year earlier while all postings held at 103 —
    recovering, the rival's direction, not yet clearly (E −0.8 on its own history to September 2025; reported beside the
    count). Hiring: 3.3% against the 3.9% unemployment implies; the gap closed 0.07 points (E −0.6), so it fits the
    paper's "stays below". Output per hour +2.2% on the year against a 2.0% average (E +0.3: output +2.5%, hours +0.2%,
    the immigration rival's call). Dividends 13.4% of pay (13.6% a year earlier), interest 15.2% (15.3%) (E −0.7).
    Transformer prices +7.8% on the year against finished goods +6.6% (now both unadjusted), 35% above their December
    2019 relative level (E −0.2: the premium is not falling back yet). Land $30.1 trillion, 1.84 years of pay (1.88;
    E −0.5; the 10-year real rate did not rise over the year). Saving 4.4% of income (5.8% a year earlier), 2.0 points
    below the 6.4% that equity wealth implies at the literature's slope (E −0.7; her call, decision 58); on the
    1960-2019 fit it would be 4.8 points above (E +0.6), on the 1990-2019 fit E −0.1, with no wealth term −1.0
    (household equities are 3.09 times income, beyond the 0.32-2.00 of 1960-2019).
  - **Combined:** count +3 over the eleven counted measures (three the paper's way, none against), above all 13
    benchmark years (2004-2007 and 2011-2019, built like the judged count: median 0, 90th percentile 1.8, highest +2).
    Tally: the paper's call fits four (1, 5, 7, 11), the rivals' two, both "nothing unusual" (2, 6), no signed call;
    neither five (3, 8, 9, 10, 12); measure 4 beside (neither). By the protocol's rules that would read "supports the
    paper", resting on two channels (without the rates measures or the price-shock measures it reads inconclusive) —
    and this is the explore half: the twelve were chosen by people who had seen these series, and it carries no weight.
  - **Base rates.** When a measure's excess was clear (|E| ≥ 1) in 1990-2019, it kept its sign the next year 59% of the
    time and was clear again 17% (pooled over the ten counted measures with E; the panel's construction: 64%). The split
    measures persist more: care 75%, the labour share 81%, the build-out 91%; persistence alone gives them `+` again with
    a chance of 57%, 23% and 41%. Measure 2: 1 of 14 normal months above its threshold was still above a year later.
    The rules in the 13 benchmark years: supports the paper none, favours the rivals 1, nothing unusual 8,
    inconclusive 4; the retirement rule would have been met in 6 of 12 consecutive pairs.
  - **Watch list (never judged).** Nasdaq-100 cap-weighted over its equal-weighted version +2.5 log points on the year,
    +41.6 since December 2019 (+36.3 since December 2022); large over small caps −1.6 on the year, +31.8 since 2019,
    with small caps ahead from December 2025 to July 2026 and behind again by September. Computer imports 72% of
    investment in information processing equipment in 2026Q2 (33% in 2015-19; 39% the pre-2020 high). Electricity
    +0.4 log points against all prices on the year, +10.2 since 2019. Consumer spending 67.5% of GDP (67.4% in 2015-19).
    Swedish household property income net of property income paid 6.09% of GDP (6.03% in 2015-19). Wealth (context for
    the website): the richest 1% held 32.5% of household net worth in 2026Q2, the highest since the series began in 1989
    (previous high 31.8% in 2025Q4); the richest 10% 68.9%, below their 70.2% peak of 2019Q1.
  - **The panel's numbers reproduced** (S5a): on its inputs and its recession dates the 24-month dispersion benchmark
    gives 0.4%, 17.9%, 55.7% and 27.7% exactly. On 24-month windows the tracker's 18.7% is NBER's dating (five more
    normal months); August 2026 reads 27.9% after the September release's revisions (26.0% on NBER dating before them).
  - `[inferred]` The splits moving most now are the build-out, the labour share and care's pay, all three measures
    whose splits persist from year to year; the payroll split has unwound without a recession, which is the rival's
    call coming true. Of the measures built to separate the explanations, care's pay leans to the paper, software
    postings and payroll dispersion lean to the rivals, and graduates and the produced-input premium against land show
    nothing yet. Care's pay is not yet clean: a shift toward low-paid home care would lower the average too.
- **Reading, for her question** ("does the hump give way to a truer parallel once the curve is
  flat?") `[inferred]`: over a whole cycle the move is near-parallel, front-heavy; phase by
  phase, a flat curve does not by itself bring parallel moves — it brings delivery (the front)
  and, at the turn, the timing mode in the other direction. A level move beyond the front needs
  the destination or the term premium to move — which is where the paper's drivers enter.

## Design decisions — veto window (her one-word calls)

1. **Two-stage cascade** for the expected path. Alternative: one speed only (simpler; cannot
   produce an overshoot above the long-run level or an inverted curve, both seen in 2022–23).
2. **The front is pinned by a delay** (time to the next priced move), not by a separate factor.
3. **Term premium additive**, with its own build-up speed; convexity ignored. Alternative: an
   arbitrage-free affine model (AFNS) — more rigorous, more parameters, same factor shapes.
4. **Basis as a flat spread state** (interbank over OIS); no term structure yet.
5. **Policy rule:** closes a fraction of the gap per meeting in 25 bp steps, at least one step
   when the gap is a step or more, at most four; its continuous speed is `−M ln(1 − inertia)`.
   The desired rate is exogenous until the macro block supplies it.
6. **Recognition is deterministic learning** (half-lives). The measured switch in volatility
   (calm to stressed in a month) is not in yet; a stochastic layer comes after the macro block.
7. **`tau` is the bridge statistic** between model and data (its floor and the delay reading are
   checks N7–N7b).
8. **Public validation on US Treasuries first**; Swedish government bonds and euro curves next.
9. **Regime mixtures: two weightings** (static; arrival with eventual probability `p` and hazard
   `h`), regimes as full `CurveState`s, a regime's curve applying from now rather than from its
   arrival date (the new world's path is a function of calendar time — simple, and exact for
   static mixtures; a switch-dated path is the alternative). The probabilities are the ones the
   curve prices, so they carry any premium for regime risk: belief and premium are not separated.
10. **Sovereign spread as expected loss plus convenience**, the loss path a cascade (so fiscal
    regimes mix, get recognised and resolve like rate regimes). Not yet in: the bank–sovereign
    link (the interbank basis moving with the sovereign spread) — a loading to add when the bank
    side needs it; and the spread over OIS itself, since public data gives spreads over Germany,
    which for non-euro countries mix policy and currency with credit.
11. **The macro block's core is the SSRN Appendix B, solved quasi-statically** along a logistic
    technology clock. Alternative: build lags and a capital stock (the old `dynamics/` engine's
    ground) — the (b) unit adds the capital stock through the paper's own Appendix A.4 user cost.
12. **Calibration (her call (a)):** four public targets hit exactly by `T`, `h`, `chi_max` and the
    schedule's convexity `k`, with `g0` set to 0.02; machine-chain land labelled as scarce inputs
    plus capital income, undivided, until (b).
    → The central is (c) since 2026-09-30 (decisions 31–37); (a) stays as a named comparator.
13. **Bridges are reduced forms with named coefficients** — the fiscal rule, the neutral-rate
    channels, the premia. They are the behaviour the openness principle makes swappable, and the
    dials a reverse stress test will turn; none is an estimate.
14. **The nominal anchor is a basket held exactly on target**, which makes the fork's size visible
    (and extreme on fast paths). Alternative mandates: goods-only (built, B5), flexible targets
    that let the basket undershoot, currency defence, a yield cap. An effective lower bound of
    −0.5% applies to delivery, not to the desired rate.
15. **Capital (b) at Appendix A.4's user cost**: required return = the real rate + a 5% premium,
    depreciation 8%; the capital-output ratio an outcome (2.98), not a target, because the
    labour-share target already fixes the machine services' share of spending and the user cost
    then fixes the stock. With the premium set, the return follows the economy's real rate with a
    one-step lag (quasi-static, no simultaneity) and partial adjustment, half-life one year
    (`Bridges.rho_halflife`): following last quarter's r* at once can cycle near full automation
    (check R6).
    → The central is (c) since 2026-09-30 (decisions 31–37), its premium set per economy (6.80 pp); (b) stays as a
    named comparator.
16. **Recognition: Bayesian learning on one signal** (labour's share, Gaussian noise, a correctly
    specified alternative world) — the fastest honest learner; realistic learning is slower
    (autocorrelated noise, a vaguer alternative, inattention), so the recognition dates are a lower
    bound on lateness. The central bank shares the market's belief. Each world's curve uses its own
    ten-year average neutral rate as the destination (a full window: past the simulated path's end
    its last value holds, so runs simulate ten years beyond the dates they report).
17. **Reverse stress, part 1: broad stated ranges, not a prior.** Uniform draws (logs for the scale
    dials: automation depth, noise, prior), Latin hypercube, and "most plausible" as the Euclidean
    distance to the defaults in the unit cube — every dial weighted equally. Alternatives: a
    prior-weighted distance (needs views on each dial), or ranges narrowed by evidence as it
    arrives. The ranges are the thing to veto: a dial whose range is too wide inflates the tails;
    one too narrow hides a driver.
18. **Speed as two channels and a failure mode**, on the learner rather than as a separate volatility
    layer: capacity (how much is read: recognition earlier), digestion (how fast it is priced: news
    gaps), and a shared error the market may not know it has. Trust follows the true world's own
    automation by default (the reflexive reading of her point), with a lead for finance adopting
    early. Today's digestion is measured for rate news (US 10Y, 1982–94 and since 1995); for regime
    news the speed scenarios assume a quarter (0.1 and 0.5 shown) and the forward-rate test measures
    years (anchors) — the scenarios' assumption is the fast end. Digestion acts on the belief (a
    level, like the forecasts and prices it is measured on), not on its log odds. Alternative: a
    stochastic volatility layer on the curve.
19. **The bank block is illustrative and static in size**: a round-number balance sheet, shares held
    fixed (no deposit outflows, no change in lending volumes, no costs, taxes or capital), behaviours
    named with stated defaults (deposit migration and lag; mortgage-margin lag and widening near the
    floor; reserve pay; house prices as capitalised site rent, discount rate floored at 1% real;
    lognormal borrowers and property companies; stylised default and loss mappings). The bank's own
    balance sheet and behaviours go on the internal side. Next candidates here: volumes (lending
    falls with affordability, deposits move), the buyer base shifting to owners, capital.
20. **The pace stays the paper's, a forward assumption, stated as such** (`pace.py`). The data since 2024 bound the pace
    so far at 0.15 of it (0.29 on the fragile endpoint). Alternatives: the measured bound as central (the central runs
    turn mild: a bust under today's rules takes 16% out of work); a pace that starts slow and rises on the macro block's
    logistic clock (consistent with the data and the mechanism, at the cost of structure). Recommended: keep the paper's
    pace central, quote the measured bound beside it wherever central numbers are quoted (the website too), and build the
    logistic pace as the next unit if she wants the central runs anchored to what has been seen.
    → Decided 2026-10-01 (Claude, on her delegation): the paper's pace stays the central forward assumption with the
    measured bound beside it. Reason: her case already carries a pace that starts at the bound and rises to the paper's
    (decision 23), so the central and the case together span both readings; the logistic pace fitted to the macro
    block's clock stays Next 10. Restated 2026-10-26 (Logs 41-44): on the corrected model the bound is 0.248 (0.427 on
    the endpoint), and a dot-com-sized bust under today's rules at the bound takes 8.2% out of work (16% quoted above
    was on the old fit); 0.244 since Log 45. Restated 2026-10-28 (decisions 91-92): 0.218 (0.39 on the endpoint), the
    bust at the bound 9.5% out of work.
21. **The exit share is not identified** (`pace.py`, A3). The crash model's 0.94 is the endpoint from the peak and rests
    on June 2026; other bases give 0.59 and 0.18; trends give none. Proposed: 0.36, the measured 2000-03 episode (a
    displacement shock inside a recession), with 0.94 and 0.12 as the range, until participation has stayed down two more
    quarters. It moves the split between unemployment and exits and when unemployment-keyed triggers fire, not the share
    out of work, which counts both. Alternative: keep 0.94, flagged.
    → Decided 2026-10-01 (Claude, on her delegation): the 0.94 exit share is kept, flagged, until the January re-check
    (Next 10). Reason: it moves the split between unemployment and exits, not the share out of work (her case at 0.36:
    −0.4 points by 2032Q3; −0.8, restated 2026-10-28 (decisions 91-92)), and the December CPS completes the second
    quarter of participation data the proposal waits
    for.
22. **The spending loop stays as fitted on 1929-33 and 2008-10** (`pace.py`, A6): the window cannot separate it from the
    unwinding of an overheated start. No offset parameter added.
23. **Her case's magnitudes are Claude's best guesses** (`case.py`; her leanings set the direction). A bust 1.5 times the
    dot-com one over two quarters (US stocks −60%, AI investment −90%); the pace from the upper bound seen (0.15 of the
    paper's) to the paper's, half-way by 2028Q2 (index 7; quoted "2028Q3" before 2026-10-01); care capped one year of
    trend above today's share; a premium on borrowing
    of a point in the US and half a point in the euro area, over the first year. Alternatives: each piece's size is in the
    attribution table (`piece_by_piece`), so any can be halved or doubled by reading across.
    → Amended 2026-10-26 (Claude, on her delegation; decision 66): the bust keeps 1.5 times the dot-com size, on the
    2000-02 bust's measured path from the quarter of today's peak (2026Q4) instead of over two quarters (the data so far
    fit the path, not the two quarters); the pace starts at 0.249 of the paper's (on the corrected model).
    → Amended again 2026-10-26 (Log 44, after the review): 1.5 times the measured sizes (US household equity −65% at the
    trough, the build-out's excess lost and more, losses 2.25% of US loans), not the ramp's −60% and −90%; dated from
    the peak's day; the pace at 0.248; no US premium (decision 69), the euro area's half point kept. Since Log 45 the
    pace at 0.244 and the euro area's premium France's (decision 71). Restated 2026-10-28 (decisions 91-92): the pace
    at 0.218; by month, household equity's trough 66.8% at a month's end (April 2029), 64.9% on 2029Q2's average (−65%
    above, at the quarterly step, in 2029Q3).
24. **Adoption in the downturn is a range, and the case a band** (the usual share of the jobs cut is automated, or twice
    it). It barely matters through 2028 (1.3 points at 2028Q4) and decides 2032 (about 16 points at 2032Q3, 15 at
    2032Q2; restated 2026-10-01 on the one dating, "15 points" quoted before). Quoted as the band; the high end is her
    full case. Alternative: a single central value (1.5x). Restated 2026-10-26 on the corrected fit and the measured
    bust (Log 44): 0.4 points at 2028Q4, 6.3 at 2032Q3, 5.8 at 2032Q2; with France a region (Log 45): 0.4, 6.2, 5.7;
    restated 2026-10-28 (decisions 91-92): 0.4, 9.2, 8.3.
25. **Deficit and sovereign worry enter as a premium only.** The model has no revenue side and no default. For the US the
    reading is fiscal dominance, not default; a looser US anchor stays a sensitivity, since in the bust it deepens
    deflation (decision 23's premium is what the case carries; since decision 69 only the euro area's, France's since
    decision 71). The fiscal
    arithmetic (revenue base, interest on rollover) is a separate unit (Next 11).
26. **The euro area is one region: austerity, her call.** Germany spending while the periphery cuts cannot be split; the
    model says it matters little (the euro area's out of work 0.5 points lower with no cuts by 2032Q3; restated
    2026-10-01 on the one dating, 0.4 quoted before; 0.2 since Log 44, and 0.8 if it stimulates). → Amended
    2026-10-27 (decision 70): France is a region of its own; the rest of the union stays one region (Germany and the
    periphery still cannot be split): with no cuts, 0.2 fewer out of work in each part; 0.8 and 0.7 if they stimulate.
    Restated 2026-10-28 (decisions 91-92): with no cuts 4.9 fewer in the rest of the union and 5.1 in France, 7.9 in
    each if the euro area stimulates; Europe's and Sweden's cuts add 8.3 to the rest of the union's peak and 8.2 to
    France's: no longer little. The US tariff is the model's symmetric tariff: US exports face
    retaliation of 25 points; the others face 25 points on their exports to the US.
27. **Energy, housing, Japan, Korea and Taiwan are watched, not modelled** (the watcher's wider rules, 2026-09-25). An oil
    surge would tie central banks' hands in the bust; the model's inflation has no energy term. Proposed: add one only if
    the oil rule and a bust fire together.
    → Built 2026-09-30 for the October bust, as an off-by-default term (decisions 44–45); whether the condition is met
    there is decision 51 — a knife-edge on the price.
    → Amended 2026-10-01 (Claude, on her delegation; decision 51): the condition becomes dated Brent at or above 1.25
    times its three-year average on a day a bust rule (bust.us.equity, bust.credit.us or crash.joint) is active; when it
    is met the energy term is switched on in the main case, and until then it stays off by default (on 1 Oct no bust
    rule is active). Reason: the first wording turned on the oil rule's base effects and was a knife-edge on the price
    ($109.65); the level bar is the oil rule's own.
    → 2026-10-26: its run is case.py's alternative "oil stays high and policy reads four quarters' headline", on the
    pass-through measured at the tag `paths-pre-signfix` (not refitted). On the vintage the price leg is met (dated
    Brent's last five prints $121.25 against 1.25 times its three-year average, $100.89) and the bust leg is not (no bust
    rule active on the watcher's state of 26 Oct). bust.credit.us, which the wording names, was retired by the watcher's
    edition 2 (8 Oct); whether it should name bust.credit.baa stays her call (lens).
28. **The machine chain is measured on the λ thread's engine, read-only and gated** (`chains.py`; Unit 1's D1, D11,
    D13–D14). The thread's narrow / medium / broad series must reproduce (1.7e-16) before anything new runs; its
    import convention (the domestic share q/(q + M)) is kept, with BEA's domestic-use convention stored beside (domp
    theta 0.470 → 0.459); so is its clip-at-zero rule (D14): each commodity's investment is clipped at 0, so used
    equipment's negative net investment is left out. For a single commodity the final-use weighting cancels, so each
    machine type is reported once; aggregates are weighted by equipment and IPP investment (private F02E and F02N,
    government F06–F10), and the
    bundle (c) reads adds private structures (F02S). CFC, NOS and GDP come from the NIPA flat file (FRED a mirror
    only); the 2017 detail inherits its summary parent's capped CFC ratio; the AI-compute composite is a labelled
    construction. Alternatives: BEA's import convention as central; an hours-worked vector rebuilt from WIOD SEA and
    the KLEMS workbook (no recorded source URL).
29. **The cost split** (D2, D5): consumption of fixed capital = Fixed Assets CFC over GDP-by-industry GOS, industry by
    industry, capped at 1 (the uncapped and economy-wide-ratio variants beside), applied to the I-O's own GOS row; CFC
    per dollar of gross output where GOS is not positive; the full-chain NOS share read as the upper bound on the
    fixed-rent share sigma; traced = theta/(1 − d), a one-sector approximation. Alternative: reassign FA's
    company-based R&D to establishments, which would remove the cap.
30. **Depreciation, the service flow and the per-income bridge** (D3–D4, D6–D10): delta = BEA current-cost
    depreciation over the average net stock (the implied replacement rate, not the published geometric one: 0.76
    against 0.55 for prepackaged software); the steady-state service share at rho 0.0575 — (b)'s return, kept for
    comparison, since (c)'s 0.0755 is an outcome of the targets this file feeds; hours = NIPA Table 6.5D full-time
    equivalents × 2,080 (Table 6.9D is gone and bls.gov is off limits), bridged to the λ thread's hours-worked basis
    by the medium set's ratio (0.904 in 2023; the unbridged values a co-headline); wage percentiles relative within
    OEWS, times economy over chain pay per hour; 2001 replaces 1999 (no all-occupations row before).
31. **(c)'s central is the open reading** (Claude's call after the review of 2026-09-30, open to her veto): every
    target on the domestic (domp) basis — her labour 0.47 is WP2026-01's human effort, which keeps foreign content
    apart — with the investment chain's imported content a fixed-quantity cost (in the model, part of the chain's
    land). One of two basis-consistent readings; preferred because the tot-consistent one (labour 0.519) has no root
    at g0 0.01 (it needs g0 at most 0.0080) and its return, 0.050, lies below the NIPA band, where the open reading's
    0.0755 lies inside. Alternatives: tot-consistent (run at g0 0.005; participation at year 15 0.199 / 0.292); the
    mixed basis, the severe bound (0.161 / 0.253).
32. **Decided 2026-10-01 (Claude, on her delegation): the low root in k is the main reading; results only the central
    root shows are reported as findings, marked "central root only"** (her open question: a finding or a sensitivity).
    Both roots fit every target exactly and the data cannot choose (so do (a)'s and (b)'s: (b) k 5.16 / 8.55); low by
    analogy with `macro.calibrate()`'s branch, not on evidence. The high root runs beside every result (`'hi'`); a
    result that only the low root shows (bank F5, households A2, bank F6 at 100%) is marked "central root only".
    Reason: the mark keeps such a result in view without claiming that the data back one root; as a sensitivity it
    would drop out of the main reading it belongs to. Alternative: report those as sensitivities only.
33. **Decided 2026-10-01 (Claude, on her delegation): g0 0.01 for (c)** (machines up to 100 times better on the easiest
    task), a departure from decision 12. Reason: her 0.02 has no root on the BEA basis (the central needs g0 at most
    0.0169). The downstream (b) comparators stay at 0.02 as stored; (b) at 0.01 sits beside in calibration_c.json, where
    g0 explains 0.028 of the 0.168 low-root gap at year 15 and runs the other way on the high root.
34. **sigma_V as a fixed point**: imports + NOS − CFC × rho/delta_chain, from the bundle's own split (0.330), with
    delta_chain BEA's private equipment + IPP rate; the bracket [imports, NOS + imports] = [0.185, 0.378]; the sweep
    over 0.03–0.50 gates the direction, not the size. The variants c_site, c_traced_g02 and the two delta variants
    (c_dnonres, c_deqipp) hold the central sigma (no fixed point of their own), to isolate the one change; c_eqipp uses
    its own split. Alternative: the chain's own depreciation from FA 3.1ESI / 3.4ESI by industry (open).
35. **The site target stays at 13% of the basket** (0.11 of GDP against the measured 4.2%, range 3.2–5.3%), with the
    measured site as variant (ii) and (b) calibrated at the same site as its comparator (c_site is below it at every
    date, root for root). Alternative: the measured site as central, which softens every (c) number (participation at
    year 15 0.351 / 0.532) and gives the one early real-wage rise (high root x1.092).
36. **delta for all fixed assets** (BEA Fixed Assets Tables 1.1 and 1.3, 2023: 0.0522); rho is an outcome (0.0755,
    inside the NIPA return band 0.068–0.088). delta leaves the real paths unchanged and scales the rate channel in pp
    (headroom 7.18 pp here, 24.6 at the equipment + IPP delta; headroom over delta is invariant). No land-slack corner
    yet: past the headroom `solve` raises NoEquilibrium, which the modules whose dials can move the return
    (calibration_c, macro_scenarios, reverse and its envelope) catch, record and date; the rest have no such dial and
    would stop on it; none swallows it. Alternatives:
    the equipment + IPP or nonresidential delta; a land-slack corner and `rho_rate_share` (only the financing part of
    rho following r*) before (c) carries rate stress.
37. **Every module on (c), with (a) and (b) as named comparators; no bridge retuned** (her decision of 2026-09-30 to
    switch; the method Claude's): `macro.central()` re-solves the stored central and refuses unless bit-identical;
    lambda ends at a fifth of each economy's own start; the capital premium is set per economy (rho·100 − r0*); the
    comparators are gated equal to the pre-switch runs. alpha_capex, alpha_rent, alpha_fiscal and the scenario
    settings stay as tuned on (b), so r*, policy and debt on (c) are readouts. The three speeds stay at a fixed
    return, as the pre-switch (a) runs were; return feedback appears only in the capital block (capital_feedback).
    Alternative: refit the bridges on (c) before quoting any rate or debt number.
    → 2026-10-01 (Claude, for the website's builder, whose numpy and scipy are not pinned): `macro.central()` returns
    the stored central and refuses only a re-solve more than a relative 1e-9 off it in any parameter; the bit-for-bit
    equality is gated in check_calibration_c E1, so the stored numbers do not move.
    → 2026-10-27 (Log 46; decisions 72-79): the bridges are refit on (c) (`macro.Bridges()`); the comparators (a) and (b)
    keep the bridges as tuned on (b) (`macro.BRIDGES_B`, `BRANCHES_B`, `reverse.DialsB`), so they stay the pre-switch runs
    array for array.
38. **Labour-share bases named, not merged**: macro_scenarios' `labour_share` is the basis each calibration targets —
    Figure 7 (`labour_share_bea`, 0.47) for (b) and (c), `labor_share` for (a) — with all wages beside; recognition's
    and speed's signal, capital_feedback's split and the export's `labor_share` are all wages over income (0.554 at
    (c)'s start, the chain's labour included). The CSV keeps its column name; its level at the start moves 0.47 →
    0.554. Alternative: the market watching the Figure 7 basis (one-half at 2.34 rather than 1.83).
39. **Decided 2026-10-01 (Claude, on her delegation): the capex key stays pace-keyed by default — the investment-keyed
    r* a readout — until the bridges are refit on (c) (Next, first); r* and debt stay on the site, labelled as
    illustrations.** The default bridge keys the build-out to the pace of tasks moving (on (c) a hump on the fast path
    only); keyed to replacement investment / income, which falls from the start on (c), r* never rises at any speed.
    Reported at the bridge's converted scale (0.0394) and the demand layer's (0.6), with alpha_capex's unconverted 0.25
    named only to place it; net investment is a diagnostic (negative on every deep path). The neutral-rate hump, the
    size of the cycle and the bank's two-branch split rest on this key. Reasons: making the investment key the default
    would be a new default set by hand, when the refit is what should set it; the site's guide states the rate path as
    an assumed link carried over from (b), and debt's dip from the surplus start, so the illustrations are honest as
    labelled, and taking them off would hide the direction the model gives.
    → Superseded 2026-10-27 by decision 72 (the refit: the investment key is the default, the pace key the readout).
40. **The reverse-stress premium dial is `premium_shift`**: ±2 pp around each economy's own premium (6.80 on (c), 5.0
    on (b), where it is the old 3–7); the bridge coefficients' ranges are not re-centred (they are behaviour); the
    technology dials are relative to the economy's own lambda. Alternative: re-centre every range on (c).
    → Amended 2026-10-27 by decision 77: the bridge dials' ranges are the refit's evidence on (c); (b) keeps its own.
41. **Decided 2026-10-01 (Claude, on her delegation): the household layer's artefacts stay disclosed and gated, not
    fixed, until the household layer is revised.** Benefits stay on the start's real wage (A1; the at-exit rule is a
    sensitivity that delays the artefact to years 14.0 / 10.25), and the layer's 5% employment floor and linear
    rigid-wage job loss stay (A2). Reason: either fix — benefits indexed to wages, job loss redesigned for money wages
    that would fall 60–80% — redesigns the layer rather than setting a parameter, and belongs with the refit (Next,
    first).
    → Superseded 2026-10-27 by decisions 78-79 (benefits follow wages; rigid wages fall at most 4% a year, job loss
    proportional).
42. **Decided 2026-10-01 (Claude, on her delegation): the fiscal start is not re-centred until the bridges are refit
    on (c); its sensitivity is reported.** tau_w 0.40 on all wages (0.554 of income on (c)) starts (c) in surplus
    (−2.61% of income against (b)'s −0.10). Re-centred (tau_w 0.3547), debt at year 15 is higher (81 / 135 / 192%
    against 57 / 121 / 187%, slow / medium / fast), so the default is the milder reading. Reason: re-centring one
    (b)-tuned fiscal bridge alone would retune the block piecemeal; the refit sets the start with the rest. Alternative:
    the re-centred start as the default.
    → Superseded 2026-10-27 by decision 75 (the start at Sweden's measured primary balance, with the rest of the refit).
43. **Decided 2026-10-01 (Claude, on her delegation): one dating — index 0 is the measured quarter** (2026Q3; the
    October unit's decision 1). `gc.quarter_label(k)` has no other dating (the 'start' / 'measured' option is gone);
    case.py runs 25 quarters to 2032Q3 with END_2028 = 9, its checks and figure relabelled and case.json regenerated
    (every stored array unchanged in its first 24 quarters, check_case K12); october.py and its checks on the same
    dating (retired to the tag `paths-pre-signfix` since Log 41). Her case then read 14.4–15.7% at 2028Q4, 1.43–1.56
    times the central run's 10.1 (quoted 13.8–14.8% against 9.2% before 2026-10-01: those were 2028Q3's); 8.2–8.6%
    against 6.5% since Log 44, 8.1–8.5% since Log 45; restated 2026-10-28 (decisions 91-92): 7.7–8.1% against 6.5% on
    2028Q4's average, the case run by month (73 months to 2032Q3, read as 25 quarters' averages; END_2028 = 9 a
    quarterly index). Reason: index 0 holds the data to September, so labelling it 2026Q4
    named every quarter one late. The website's lens carried the dating as pending until the watch branch's 878657d
    marked it decided, and the model page and Our view are dated on it (a4f24a9; Next 13).
44. **The crash model's inflation is core; headline = core + the energy term.** Its pi was fitted on core PCE (the
    stored US start is July core, 3.34); the stored euro-area, Swedish and Chinese starts are headline, left
    unchanged. The October runs start every region on core (US core PCE 3.01; euro-area and Swedish HICP excluding
    energy, food, alcohol and tobacco, 2.38 / 1.17); Sweden's headline at the start is core + the energy term (1.01),
    with CPIF (0.7, lowered by the food VAT cut) a variant; China has no energy term (its CPI on FRED ends 2025-04).
    → 2026-10-26: every region but China starts on core in the model itself (gc.regions_today on the vintage, decision
    67), so the stored runs, the case and the website share the start.
45. **The energy term** (`global_crash.energy_inflation`, off by default): pass-through measured (headline minus core
    on crude's change times energy's share of spending, this quarter and one lag, the previous quarter's weight; US
    PCE 1990–2026, euro-area and Swedish HICP 2000–2026 with quarter dummies; the constant and the dummies not
    carried); the real-income drag approximate (spending falls 0.8 of the bill; the US, a net petroleum exporter, gets
    half back; consumption shares 0.675 measured, 0.52 and 0.45 approximate); symmetric, so a collapse is a relief.
    The US on WTI, its own crude, is a sensitivity (b0 0.244 against Brent's 0.231). Alternative: a lagged real-income
    response (spending adjusting over a year), which would carry the pre-start surges' undelivered drag.
46. **Oil paths**: "stays high" = dated Brent held at its late-September level ($117.66, the last five EIA prints,
    above the futures strip) for four quarters, then its three-year average ($80.06); "held high throughout" a
    sensitivity; "collapses" = each currency's own 2008Q4–2010Q3 path anchored on 2026Q3's average ($95.99), with the
    late-September-spot anchor and the dollar's ratios in every currency as variants; exchange rates held at their
    last value. Since 2026-10-26 the case's energy run (`case.oil_high`) reads the vintage: the last five prints
    ($121.25) and the three-year average ($80.71); the collapse paths went with the October unit (Log 41).
47. **Decided 2026-10-01 (Claude, on her delegation): the spread already present — the corporate spread's rise alone in
    the central; the term premium's routing a named sensitivity.** 0.09 points, the ICE corporate spread's three-month
    rise, held on top of the case's premium from index 0, US only, labelled a treatment, not data. The ten-year term
    premium's three-month rise (+0.335), routed through the private credit-spread channel at a_s (a coefficient for
    corporate spreads), is the sensitivity: US out of work 15.2–16.6% at 2028Q4 against the central's 14.7–16.1%.
    Reason: decision 23 and case.py sized the case's premium on the term premium's rise since 2019 (decision 25 says the
    case carries it), so routing this autumn's rise as well would double count it.
48. **Decided 2026-10-01 (Claude, on her delegation): hands tied reads four quarters' headline; the
    quarterly-annualised reading is a sensitivity.** `Rules.react_to` takes 'headline' / 'core' and, off by default,
    'headline4' / 'core4' (the last four quarters, with index 0's year-on-year reading before the start); october.py's
    main hands-tied runs read 'headline4' (`TIED_READING`), the runs marked "on quarterly headline" are the
    sensitivity, and looking through reads the model's quarterly core, as fitted. Expectations stay on core except in
    one sensitivity. Rate findings are quoted on four quarters' headline, the quarterly reading beside them. The
    oil-collapse run is under hands tied, matching today's central-bank stance (the October unit's decision 8). Reason:
    central banks set their targets, and read inflation, over a year; the quarterly reading's whipsaws (the ECB's in the
    collapse run, the Fed at 2.18) come from annualising one quarter's oil move.
49. **The October start and its vintage** (superseded 2026-10-26 by decision 67; decisions 45-46, 48 and 50-51 are
    the October bust's, a record at the tag `paths-pre-signfix`; 46's "stays high" and 48's four-quarter reading are
    case.py's energy alternative; 50's mapping is `case.signals`, on the 2000-02 bust's measured Nasdaq-to-equity ratio
    and one for one): measured to 30 Sep (euro-area unemployment 6.4, ECB LFSI for the euro area
    of 21, July 2026; Sweden 8.9, SCB); the output gap left at 0 (measured about +1.4; open); a separate cache
    (`cache/october/`) read through a context manager, so no other module sees it; refreshed on 1 Oct (DFF, BAA10Y,
    NASDAQCOM, STLFSI4); re-run after each new print.
50. **The watcher mapping**: quarters interpolated linearly; the Nasdaq taken one-for-one from the model's US stock
    fall (in 2000–02 it fell about 1.6 times as far — the October build's reading, not traced to code, results or a
    check `[inferred]` — so the timing is on the late side); US high yield from stocks at the
    2023–26 slope; claims = the actual reading + 14.6 × unemployment's rise over its 12-month low; the oil and bust
    rules replayed daily on the watcher's own logic (EIA's calendar, England's bank holidays hard-coded through 2028);
    a rule is flagged knife-edge when a reading comes within 5% of its bar.
    → Amended 2026-10-26 (Log 44, after the review): the Nasdaq rule is read on 2000's own daily path from its high
    (10 Mar 2000), its drawdown times the case's scale, counted from the 2026 high (6 Oct): the reading the case's own
    dating implies (`case.signals`); the quarterly mappings — household equity's fall times the measured 2000-02 ratio
    of the two falls at the same quarter from the peak (1.6 to 3.85; "1.7 to 3.9" as first written, corrected
    2026-10-28), and one for one — are late bounds beside it, read by month since decision 91 (January and July 2027,
    restated 2026-10-28 (decisions 91-92); 2027Q1 and 2027Q3 before). The 1.6 above is superseded.
51. **Decided 2026-10-01 (Claude, on her delegation): decision 27's wording — the level-based one (decision 27,
    amended).** As first written (the oil rule and a bust rule active together) the condition is met in the replay of
    the October-bust run (a scenario; on 1 Oct no bust rule is active) under "stays high" or "held high" — 18 Dec 2026
    to 14 Jan 2027, 20 weekdays (17 Brent prints) — and not if oil collapses; but it is a knife-edge on the price: it
    needs dated Brent at $109.65 or more from 30 Sep through late December, and at the futures strip ($102–107) it is
    not met. The level-based wording — "Brent at or above 1.25 times its three-year average on a day a bust rule
    (bust.us.equity, bust.credit.us or crash.joint) is active" — is free of base effects; it needs $101.12 and is met at
    the strip (27 Nov 2026 to 30 Sep 2027 under "stays high"). Both thresholds move with each Brent print. Reason: the
    first wording turns on the oil rule's base effects rather than the price, so a few dollars decide it.
52. **Decided 2026-10-01 (Claude, on her delegation): the paper's land residual stays open for the paper's authors**
    (pinning Open 10: the Z.1 residual counts about $4.3T of nonprofit property as land in the coverage figure's
    household valuation members; estimated, not rerun, the 2025 median would fall from 0.33 to about 0.30). The
    repository's figures keep matching the published paper. Reason: correcting them here would make the repository
    disagree with the published PDF; the correction belongs in the paper's next version.
53. **The twelve judged measures are the critic's list** (`SPLITS.md` §2), where the paper and a named rival predict
    different signs, not the panel's first draft (which judged splits every explanation predicts). Three swaps from the
    brief, all for data: care's pay is production workers in education and health (`CES6500000008`; no health-care
    production-worker earnings series is on FRED); the build-out against housing uses BEA's chain-type quantity indexes
    (`B679RA3Q086SBEA`, `A011RA3Q086SBEA`, from 1947; the chained-dollar series on FRED start in 2007 and
    `A679RA3Q086SBEA` stops in 2013); computer imports are set against information processing equipment (`Y034RC1Q027SBEA`),
    since `Y033RC1Q027SBEA` is all equipment. Measure 9's finished goods are the unadjusted index (`WPUFD49207`), like the
    transformer index (the review: the adjusted one's seasonal factors are revised each February). Alternatives: the
    panel's draft list; credit stress by area income (NY Fed, not on FRED) in place of saving.
54. **One statistic, E, on the latest 12 months or 4 quarters**, against the mean and sd of such changes in 1990-2019
    windows without a recession month; thresholds ±1 (in plain units in `SPLITS.md` §2). It scores the excess over the
    1990-2019 pace, so a gap that keeps that pace scores nothing — but a split that continues at its recent pace scores
    again, which is why each measure carries the chance that persistence alone gives its reading (§5). Output per hour is
    judged on its growth over 4 quarters, not the brief's 8, so every measure has the same window (8-quarter growth is
    reported: 2.2% a year to 2026Q2). Alternatives: 24-month windows (fewer, slower), ±1.5 (fewer readings either way), a
    frozen persistence null for the count (not built).
55. **Recessions are NBER's (`USREC`)**, plus a real-time Sahm reading ≥ 0.5 for windows NBER has not dated, on judged
    windows and the count's benchmark alike. A recession voids every measure except 3 and 7, whose rival is the cycle
    (judged in a downturn); the combined verdict is void either way. On 24-month windows NBER's dating put measure 2's
    threshold at 18.7%, not the panel's 17.9% (its hand-typed peaks counted five more months as recession).
56. **Which explanation a reading fits** (`SPLITS.md` §2): a rival that predicts nothing unusual (6, 7; 12 only once
    measure 11 has turned; 2 below at both ends) fits when |E| < 1, but that is not a signed call; hiring's "stays below"
    fits the paper while the gap is below zero; care counts only while its jobs rise faster than usual; dividends are
    judged alone (rent is reported: it is mostly owner-occupiers' imputed rent, which overlaps measure 10). The rivals'
    conditions are tested: a rate cut (target at least 50 bp below its level a year earlier) for 5 and 11, a rising
    10-year real rate (Cleveland Fed) for 10; without them a `−` fits neither. Measure 9 is judged on its level at the
    window ending August 2028 ("falls back by 2028"). The paired reading of 9 with 10 is dropped: each is scored on its
    own, which already reads the produced-input premium falling while land holds as the paper's. Alternatives: a high
    (not rising) real rate for 10; the paired reading in place of 9's and 10's separate entries.
57. **Software postings are judged against their own history** (2021-04 to 2025-09, the window before the latest left
    out: mean −9.6, sd 34 log points a year), which contains the 2022-25 fall the measure tests; it reads `+` only on a
    35% relative fall in a year and `−` on a 28% rise. It is reported beside the count, not in it (the count's benchmark
    needs 1990-2019 history). Alternatives: a zero mean; moving it to the watch list.
58. **The residual fits** (coefficients frozen at the freeze; later vintages' estimates printed beside them): labour
    share on the unemployment rate's level over 1948-2019, no trend (over a year the adjustment is small: E +1.36 against
    +1.44 raw); hiring on unemployment over 2001-2019; saving on equities over disposable income at a slope set from
    the literature, its intercept the 1960-2019 mean. **Her call, 2026-10-13: the literature slope** — −1 point of the
    saving rate per unit of household equities over disposable income (about one cent of spending per dollar of equity
    wealth), not the 1960-2019 fit (slope −4.27), which is extrapolated far (equities 3.09 times income against
    0.32-2.00 in the fit, where it puts the saving rate at −0.4%). The intercept (9.46, the 1960-2019 mean of the saving
    rate plus the ratio) keeps the residual's level readable: saving is 2.0 points below what wealth implies. Today's E
    is −0.66 as built; +0.57 on the 1960-2019 fit, −0.12 on the 1990-2019 fit and −1.00 with no wealth term, all
    reported beside it, with the fitted slope and an out-of-range flag (`code/splits.py`, `SAVING_WEALTH_SLOPE`; check
    S22). It moves the history too: the count's benchmark has a 90th percentile of 1.8 (was 1; the bar is still a count
    of 2 or more) and the retirement rule would have been met in 6 of 12 pairs (was 4). Not taken: the 1960-2019 slope;
    a log wealth term; moving 12 to the watch list. Alternative for 7: a fit in changes.
59. **Verdicts and retiring** (`SPLITS.md` §6, §8), over the eleven counted measures: supports the paper when the count
    is above the benchmark's 90th percentile (today 1.8) and the paper fits at least twice as many measures as the rivals
    (all their fits); favours the rivals when the rivals' signed calls fit at least twice as many as the paper;
    nothing unusual at a count at or below the median (0) or with no fit for the paper and no signed call; given only at
    the yearly look, and recomputed without each channel (rates; the tech unwind; the price shock). Retire after two
    consecutive non-void windows that favour the rivals or read nothing unusual (void windows skipped): in the benchmark
    years that would have happened in 6 of 12 pairs. Alternative: retire only on two that favour the rivals (0 of 12).
60. **The watch list**: big stocks against the rest as the Nasdaq-100 over its equal-weighted version (the S&P 500
    equal-weight index is not on FRED; large against small caps beside it), computer imports, electricity, consumer
    spending's share, and Sweden's household property income net of property income paid (Statistics Sweden NR0103 sector
    accounts, cached; national accounts, not labour-force data). Reported, never judged. The wealth shares of the
    richest 1% and 10% (Fed distributional accounts) are fetched as context for the website's spending section.
61. **The tracker keeps its own vintages** (`cache/splits/`, refreshed each quarter with `--refresh`, committed with the
    freeze and with each look), so the other units' caches do not move; October 2025 (no household survey or CPI, the
    shutdown) is handled as never published. A failed refresh keeps the previous file and its record, marked and warned;
    the baseline and the look refuse it.
62. **The freeze date** — proposed: as soon as she has read this, before the September CPI and PPI and the third-quarter
    GDP release, so the starting point is not picked around them; the first judged look then falls on 15 November 2027.
    `--refresh --write-baseline`, the checks, a commit, then the tag `paths-splits-freeze`. Proposed (was her call): push
    the tag the same day, before the website says "fixed on" — an unpushed tag can be deleted and made again. The
    baseline lists the releases published after the 2026-10-13 vintage, as seen. Alternative: freeze at the next
    quarterly run.
63. **The count's benchmark is built like the judged count:** the eleven measures with 1990-2019 history, only years in
    which all eleven exist, each window ending in the calendar month its judged windows end in (September; August for 5,
    8, 9; the second quarter), and the same void rule (NBER or Sahm): 13 years, 2004-2007 and 2011-2019 (was: December
    windows over 8-11 measures, 25 years). Alternative: scale the count by the number of measures to use 1993-2019.
64. **Measure 2 on 12-month windows** (was 24, the panel's): a judged reading then holds nothing from before its window's
    start and consecutive windows share no data, as `SPLITS.md` §9.3 requires; its per-cut moments are frozen. Its
    threshold keeps the recovery years (13 of the 15 normal months at or above it), as judged windows in a recovery are
    not voided either. It reads "within the normal range" today (7.5% against 26.6%); on 24-month windows it read above
    (26.6% against 18.7%). Alternatives: 24-month windows judged from b+24 only; leaving out the year after each
    recession's exclusion (threshold 10.9%).
65. **The yearly look runs once and stands** (`SPLITS.md` §7): `--refresh --look` on 15 November (or the first day after
    it when every window is published), refusing a failed refresh; committed with the vintage and tagged
    `paths-splits-look-<year>`; later runs report the window on revised data beside it. A code change after the freeze is
    run beside the tagged code, whose judged readings stand; any difference is a deviation.
66. **Decided 2026-10-26 (Claude, on her delegation): the bust's path is the 2000-02 bust's, measured**
    (`global_crash.bust_2000`; `ai_shock`'s default, so the stored runs, the website's model and her case share it; her
    case at 1.5 times the size). Household equity −44.7% at its trough ten quarters after the peak (Fed Z.1), back at the
    peak by 2005Q4; the build-out (BEA, above its 1990-94 trend) still growing three quarters after the peak, most of its
    excess gone by four years; bank losses (C&I charge-offs above their 1997-99 mean, the Fed Board) peaking ten
    quarters after. The onset is the quarter of the peak, 2026Q4 (the Nasdaq's and the S&P's high, 6 Oct). Reason: the
    bust as first built (straight-line falls over four quarters, held for good; kept as `shape="ramp"`, check_case K1)
    was about 2.5 times faster than the dot-com bust on every leg and out of its order, and never recovered; October's
    data fit the measured path's first quarter (household equity at its Q3 level, the periphery and the lowest credit
    tier breaking, the build-out still rising) and not the ramp's (equity −30% and US out of work 5.6% in 2026Q4, against
    claims pointing to about 4.2; restated 2026-10-28 (decisions 91-92): US out of work 5.0% on 2026Q4's average).
    Alternatives (case.json `alternatives`): the ramp (the 8 Oct timing), the fall held at
    its trough, the core holding, a quarter later.
    → Amended 2026-10-26 (Log 44, after the review): the sizes are measured too, not only the path — household equity's
    fall, the share of the build-out's 2000Q1 excess lost (up to 76%), and the losses' timing; their total, 1.5% of US
    loans, stays assumed (`ai_shock` had multiplied the normalised path by the ramp's 40% and 60%). And the bust is
    dated from the peak's day, 6 Oct 2026 as 10 Mar 2000 is (`case.peak_shift`: 0.712 of a quarter), so the case's
    household equity falls from 2026Q4 (4.7% down in it; restated 2026-10-28 (decisions 91-92): 4.7% at its end, 2.5%
    on its average) and the website's model, dated by the quarter, shows the
    falls from 2027Q1; dated by the quarter is an alternative in the case (−0.5 at 2028Q4; −0.2, restated 2026-10-28
    (decisions 91-92)).
67. **Decided 2026-10-26 (Claude, on her delegation): one start, a dated vintage** (`code/vintage.py`, `cache/start/`
    with a manifest of each series' source, last observation and hash; `gc.regions_today` reads it to the end of 2026Q3;
    the case, the central run and the website's model on it; check_case V1-V2). US unemployment 4.2 (Sep), core PCE 3.01
    (Aug, after BEA's annual update; 3.34 stored before), equity wealth 2.27 times GDP (Z.1, 2026Q2; 1.9 approximate
    before); the euro area 6.5 (ECB LFSI, Aug; 6.3 hard-coded before) on core HICP 2.39 (headline 3.23 before); Sweden
    8.6 (SCB, Sep; 8.5) on core HICP 1.17 (0.7 hard-coded) at the Riksbank's 1.75; China stored. FRED refused this
    machine from the evening of 26 Oct, so the sources are FRED as cached on 30 Sep (after the annual update), the
    watcher's FRED copies of 26 Oct, BEA's bulk NIPA file and the ECB; the manifest names each. Since Log 44 the
    euro-area and Swedish HICP are September's, from Eurostat (prc_hicp_minr; EA core 2.50, headline 3.75; Sweden core
    1.12), and the vintage adds the US ten-year yield, term premium and Baa spread and France's and Germany's ten-year
    yields (the Riksbank's SWEA), for decision 69 and France; every earlier series bit-identical on the refresh. US
    core PCE for September comes on 29 Oct. A vintage is refreshed
    (`code/vintage.py --refresh`) and committed before the prints it is scored on (Next 11).
68. **Decided 2026-10-26 (Claude, on her delegation): the build-out is information processing equipment** (`decoupling.py`
    read Y033RC, all equipment, under that label, since 2026-09-25). Net of computer imports it sits 0.42 points of GDP
    below its 2015-22 trend (0.2 below its 2022 level), so the US capex leg is zero: a lower bound, since data-centre
    buildings are not in the measure. Alternative: add data-centre construction (Census, annual) — not done.
69. **Decided 2026-10-26 (Claude, on her delegation, and at her prompt: "my leanings may well be wrong now, at least the
    borrowing premium one"): no premium on US borrowing in the case; her leaning is an alternative.** The test the lens
    set for point 3 is `fiscal.premium.jobs` against `fiscal.premium.flight`: in October, as the slowdown began, US
    long rates fell (the ten-year 5.29% to 4.96% from 30 Sep to 22 Oct, the Kim-Wright term premium 1.08 to 0.99 to 16
    Oct, Baa over the ten-year 1.47 to 1.46), the flight direction; the case had priced a point more over the first
    year. Priced, it would add 1.2 points of US out of work at 2028Q4 and 3.8 by 2032Q2 (case.json `alternatives`;
    1.4 and 5.3, restated 2026-10-28 (decisions 91-92)).
    The euro area's half point stays: France's ten-year over Germany's rose from 1.28 to 1.66 points in October (0.81 a
    year earlier), while the Netherlands' and Finland's moved by 1 and 6 basis points (the Riksbank's daily yields);
    on the OECD's monthly long rates (to August or September) France was already the widest over Germany, above
    Italy's 0.8, Greece's 0.8 and Spain's 0.45. The premium is real and French, which is the case for France as a
    region of its own (Next 15). Alternative: keep the US point (her original leaning), or a half point. Reason: one
    month's data, but the case should carry what the data show so far, and the alternative keeps her reading one step
    away; if `fiscal.premium.jobs` fires, it comes back.
70. **Decided 2026-10-27 (Claude, on her delegation, at her suggestion of 2026-10-26: "maybe it would make sense to have
    france as its own region since that seems to be where some of the action is happening"): France is a region of
    its own, inside a monetary union with the rest of the euro area** (`global_crash.py`: `R` has five regions, the
    four economies with the euro area in two; `Region.union`, the sovereign block `sov0 ... sov_mtm`, `Rules.tpi`;
    `exposure.py` and `financing.py` split France out; checks E1-E6). The ECB sets one rate on its members'
    size-weighted readings (with one member the rule is the region's own: E2 nests the single euro area exactly).
    France's government has a spread over the union's benchmark — its ten-year over Germany's (the Riksbank's daily
    yields), 1.28 points at 30 Sep against 0.70 from July 2025 to June 2026 — plus the price of the debt it adds (the
    euro area's measured slope, 15 bp per 10 points of debt, 30 under bank stress) and any premium a run sets; half of
    its rise above the calm level reaches French borrowers (approximate); its banks hold euro-area government debt of
    14% of GDP (the ECB's BSI), marked to the spread (duration 7, 40% at market value: approximate); and with a
    backstop the recapitalisation is public debt, so bank losses raise the spread (the doom loop, at the measured price
    of debt; E4 finds it weak at these sizes). The ECB's Transmission Protection Instrument is a dial (off unless a run
    sets it: it has not been used at 1.66). Measured: France's unemployment (8.2%, Eurostat, August), core HICP
    (1.77%), debt (119.1% of GDP, 2026Q2), the BIS's credit (households 59.1%, private non-financial 214.3%), GDP's share
    of the euro area (18.7%); the rest of the union by difference (unemployment 6.0%, core 2.67%). Approximate, stated:
    Okun, speed, replacement (0.65), floating share (0.05), bank capital and loans, trade, the discretionary response
    (1.0% of GDP, under the excessive deficit procedure). Trade inside the union pays no tariffs (the single market),
    and a union partner's slump reaches a member only as far as it differs from its own: each part keeps the whole's
    own dynamics, which held the union's internal trade, so a shock to all of it moves it as the one region did (E2,
    the halves trading with each other), while a shock to France alone spills over (a French slump of 5.3 takes the
    rest down 1.9). Without that rule the split deepened the union's 1930s row from 26.0% to 29.9% below capacity and
    its eroding row from 8.1% to 9.0%: a double count, found and fixed the same day. France's care share fell in
    2019-25 (−0.03 points of employment a year, ILOSTAT): a shrinking care sector takes in none of the displaced, and
    the case caps France's care at today's share. Alternatives: France inside one euro area with a premium on
    all of it (as before: decision 26); the doom loop on every region's sovereign; a premium that rises with debt's
    level, not its change. Reason: the action in the union is French (decision 69), and only a region of its own can
    carry a spread the rest does not pay, one central bank rate for both, and its banks' exposure.
71. **Decided 2026-10-27 (Claude, on her delegation): the euro area's premium in the case is France's** — a point more
    on its government's spread over the first year, on top of the 0.58 above its calm level already there at the
    start, half of each reaching French borrowers; none in the rest of the union, whose spreads did not move (the
    Netherlands +1 bp and Finland +6 bp in October). Before it: half a point on all euro-area borrowers. Alternatives
    (case.json): two points; the ECB capping France's spread half a point above its start (TPI).
72. **Decided 2026-10-27 (Claude, on her delegation; Next, first): the capex key is investment** — r* moves with
    replacement investment / income (delta Vm K / income, the quasi-static accounts' only investment), one for one at
    the common scale of decision 73: alpha_inv 0.3 pp of r* per point of income [the pace of tasks moving to machines,
    alpha_capex 0.25 pp per pp a year: 0.039 per point of income at (b)'s start]. On (c) investment / income falls from
    the start (medium 0.178 → 0.049 by year 15 [0.046 at a fixed return]), so r* rises at no speed on either root: the
    build-out hump is gone [fast 0.76 → 1.35 → −0.13%]. Keyed to investment alone, the other bridges as tuned on (b)
    (`refit_steps`, step 1), r* at year 15 is −2.13 / −4.11 / −4.17% slow / medium / fast [0.26 / −0.10 / −0.13]. What
    it does, with the rest of the refit: the size of the cycle — the demand layer's owners'-saving gap −7.2% at the floor
    for 6.75 years from year 8.5 [−1.85%, 4.0 years from 11.25], the deficits branch a small slump (−0.65%) [a boom,
    +1.08%]; the bank's two-branch split — both branches' rates now fall: deficits dominating, policy 2.75 → 1.0% and
    NII 2.11 → 1.49 [policy up to 5.75%, NII up to 2.99]; owners' saving to the floor as before (NII low 0.88 [0.88]).
    Keyed back to the pace (the readout `r_star_capex_on_pace`) the refit's r* still rises under a tenth of a point at
    any speed, but the deficits branch rises again (policy to 4.75%): the split rests on this key (bank R5, demand R3-R4).
    Evidence: Rachel and Smith (2015) read gross investment against gross saving, so a fall in the investment share at a
    given saving share is excess saving (their 4 pp fall in investment ~80 bp). Alternatives: the pace key
    (`macro.BRIDGES_B`, the readout); only the net investment a growing stock needs (g / delta of replacement, about 0.4
    of the term: open). Reason: the accounts' investment falls with the technology (machines cheapen); keyed to the pace,
    the bridge saw a build-out the accounts do not have.
73. **Decided 2026-10-27 (Claude, on her delegation): one scale for the three channels; owners' saving on evidence, no
    new structure** — r* moves `macro.NEUTRAL_SCALE` 0.3 pp (range 0.2–0.5) per point of income by which desired saving
    outruns desired investment: Rachel and Smith (2015, BoE WP 571; calibrated elasticities 0.5 and −0.7: 0.20–0.25),
    Rachel and Summers (2019; 2–4 pp of GDP per point of r: 0.33, 0.25–0.5); Holston–Laubach–Williams's IS curve (0.82 in
    output-gap units, multipliers included) an upper bound. Owners' saving: the gap between owners' and wage earners'
    saving out of a marginal unit, retained earnings included, 0.30 (0.15–0.45) — Kaleckian estimates of C/Y per point
    of profit share (US −0.43 Onaran–Galanis 2012, −0.14 Hein–Vogel 2008; Sweden −0.39 Onaran–Obst 2016), Mian–Straub–
    Sufi (2021: a shift-share ~0.20; top 1% saving over 40% of income), Dynan–Skinner–Zeldes (marginal 0.03–0.43 between
    quintiles); Fagereng–Holm–Moll–Natvik's flat net saving rates are the household-only basis (smaller). alpha_rent
    0.09 [0.05]; Eggertsson–Mehrotra–Robbins's 8 bp per point of labour share is a cross-check. Step 2 lowers r* at year
    15 to −3.63 / −6.18 / −6.24%. No structure added: the evidence reads the same reduced form (a gap per unit shifted).
    Stated caveats: local estimates applied to a ~50-point shift; in the model owners fund dependants' support, so part
    of the shift is spent through them; payout matters (Swedish MPCs out of dividends 0.4–0.6, Di Maggio et al. 2020).
    Alternatives: the household-only gap (0.15–0.20); a gap that falls as ownership broadens.
74. **Decided 2026-10-27 (Claude, on her delegation): deficits at their pass-through** — 0.6 (0.5–1.0) of a primary
    deficit reaches net saving, one minus the Ricardian offset (Gale and Orszag 2004: 20–50%; Röhn 2010: ~40%; de Mello
    et al. 2004: a third to a half): alpha_fiscal 0.18 [0.10]. The direct long-yield estimates lie above it (Laubach 2009
    ~25 bp per point of projected deficit; Gale–Orszag 40–70 for primary deficits; Rachel–Summers's average 38); they
    carry term premia and expected inflation, and the model's term premium already rises with debt above 60% of income.
    Step 3 raises r* back part way (year 15: −2.70 / −4.82 / −4.87%), but investment and owners' saving outweigh it: on
    the refit rates fall under deep automation. Alternative: alpha_fiscal on the direct estimates (0.25–0.5).
75. **Decided 2026-10-27 (Claude, on her delegation): the fiscal start at Sweden's measured primary balance** — the wage
    tax is set so the start runs a primary deficit of 0.16% of income (`Bridges.deficit0`, tau_w 0.35 [0.40 on all
    wages, a surplus of 2.61%]): the general government's 2021–25 mean primary deficit, 0.14% of GDP (Eurostat
    gov_10a_main, B9 + D41PAY, cached in `cache/fiscal/`), on the model's income basis (x 1.145: GDP net of the chain's
    imported content over income). debt0's 40% kept: Sweden's 2025 debt, 35.1% of GDP, is 40.2% of income on that
    basis. 2025 alone: 1.15% of income (the slowdown). Debt at year 15: 75 / 110 / 142% slow / medium / fast [57 / 121 /
    187%; re-centred on the old r* 81 / 135 / 192%] — under the re-centring alone because the refit's r* falls (the
    interest-growth term); debt rises from the start [dipped to 29–32% by year 6]. The site's "starts in surplus" is
    restated (watch). Alternatives: 2025 alone; a US start (~3% of GDP); the surplus start (`sensitivity_fiscal_start`:
    52 / 100 / 140%).
76. **Decided 2026-10-27 (Claude, on her delegation): the bank's two branches at the evidence's ends** (`macro.BRANCHES`)
    — the two direction bridges at the ends of their ranges, each against the other's opposite end, the scale and the
    investment key held: deficits dominate, gap 0.15 and no offset (alpha_rent 0.045, alpha_fiscal 0.30) [0.02, 0.25];
    owners' saving dominates, gap 0.45 and offset 0.5 (0.135, 0.15) [0.12, 0.10]. Both now fall: through recognition the
    10Y moves −44 / −194 bp [+118 / −150 on (c); (b) +80 / −119] (speed F4). Alternative: branches that move the scale
    too (0.2 / 0.5).
77. **Decided 2026-10-27 (Claude, on her delegation): reverse stress on the refit's dials** (decision 40 amended: the
    bridge ranges are re-centred now that they rest on evidence) — the central's capex dial is alpha_inv over 0.2–0.5,
    alpha_rent over 0.03–0.225, alpha_fiscal over 0.10–0.50 (the scale's range times the gap's and the pass-through's)
    [alpha_capex 0–1, alpha_rent 0–0.2, alpha_fiscal 0–0.4]; (b) keeps its own (`reverse.DialsB`), so comparator_b is
    the pre-refit envelope draw for draw. Found: the 10Y falls over ten years in 94% of draws [63%] and never rises in
    87% [54%]; policy reaches the floor in 64% [30%]; the rise side's 95th percentile +124 bp [+474; (b) +215]; a +100 bp
    rise needs fiscal strain (a steeper term premium per point of debt, more public support) besides the two direction
    bridges, and lies farther from the defaults (0.823 [0.511]; (b) 0.608). Alternative: draw the scale, gap and
    pass-through as three dials (the shared scale kept).
78. **Decided 2026-10-27 (Claude, on her delegation): household benefits follow wages** — public support is the
    replacement rate on the current net money wage (`Support.benefit_base` 'wage') [the start's real net wage, indexed to
    prices]. Evidence: Sweden's a-kassa pays 80/70/65% of the person's own previous wage over 300 days, the base fixed for
    the spell, the ceiling not indexed (frozen nominally 2002–2015); the OECD's net replacement rates are measured against
    own previous earnings (Sweden at 67% of the average wage: 71% in month 2, 63% at 12, 59% at 60 with social
    assistance); minimum benefits follow wages in the Netherlands, Denmark and 35 US states. A1's artefact is gone:
    coverage 55–84% at every date, the job losers' drag never zero (−0.88 / −0.55% of GDP at year 15) [coverage 176% /
    315% by year 15, the drag zero from year 9.25 / 8.25]. A challenge to the earlier framing: Sweden's own long-term
    floor (riksnorm) is set on prices, so the old rule is also what a price-indexed floor does when money wages collapse,
    not only an artefact; kept as a sensitivity (coverage 245% / 492% by year 15) beside each cohort's real wage at exit
    (128% / 219%). Alternative: a hybrid (the first year on the wage at exit in money terms, then a price-indexed floor).
79. **Decided 2026-10-27 (Claude, on her delegation): rigid money wages fall at a limited pace, and job loss is
    proportional** — money wages fall at most 4% a year (`Support.wage_fall_max`; Schmitt-Grohé and Uribe 2016: W at
    least 0.99 of last quarter's; Greece's average wage −22% over 2009–15; the euro periphery's fall at most 5.1% in
    2008–11) [no cut at all]; the log excess over the market wage lowers log employment by the labour-demand elasticity
    0.4, a share of the jobs still there (Lichter, Peichl and Siegloch 2015: median 0.39, bias-corrected 0.25) [linear in
    the summed refused cut, a share of the start's employment]. A2's floor binds nowhere [from year 10.5, central root,
    owners' saving]; employment's low is 0.096 of the start's (owners' saving). Alternatives: no cut at all
    (`wage_fall_max` 0, a sensitivity: the gap −12.0% against −10.0%); rigidity that erodes (Fallick et al.'s ~24% a
    year; the Wage Dynamics Network's deep-shock erosion).
80. **Decided 2026-10-27 (her call: "refit monthly ... matching each target at the frequency it is measured"; the form
    Claude's): the crash model's step is a parameter** (`global_crash.simulate(..., dt)`, `ai_shock(..., dt)`; checks
    T1-T4; numbered after the bridges refit's 72-79). The per-step coefficients
    stay stated and fitted for a quarter, and at another step each is carried over to do over a quarter what it did:
    a share per quarter (Okun's speed, the share of cyclical unemployment turning structural, care's hiring, the gold
    standard's drift, the anchor's weight on the target) compounds, 1 − (1 − s)^(dt/Q); a persistence (the gap's, the
    rate's smoothing) is taken to the power dt/Q; the rate transmission keeps its long-run effect on the gap, a_r/(1 −
    a1); the Phillips slope its long-run effect on inflation given the anchor, κ·anchor_step/anchor. What the model
    counts in quarters (the stimulus's two years, the year it tapers over, a rule's four-quarter average, the quarter
    tariffs or a gold defence arrive, the energy term's one-quarter lag and its annualisation) is counted in steps; the
    bust's measured path is read at each step's end, its delay still in quarters. At a quarter every coefficient comes
    back untouched: on the stored regions and parameters, 80 runs across the rules, the bust's shapes, the energy term
    and the spreads are bit-identical to the model before (T1; the scratch comparison in Log 47). Before a refit, the
    quarterly fit run monthly is near itself in the central run (US out of work 15.1% at its peak against 14.4%, T4)
    and deeper in severe ones (eroding rules 27.2% against 24.8%): the loops — lost wages, bank capital, spreads — close
    within a month instead of a quarter. That is what the monthly refit (decision 82) settles. Alternatives: refit every
    coefficient, the literature's included, at each step (more freedom, less anchoring); a weekly step (her first
    leaning, challenged: outside financial prices no labour or output series is weekly, claims only from 1967, so a
    weekly fit would fit its interpolation).
81. **Decided 2026-10-27 (her call: "policy dated in the model instead of triggers"; the form Claude's): the
    discretionary levers start on dates** (`Rules.fiscal_at`, `care_at`, `tariff_at`, years after index 0's end; check
    T2). From its date the stimulus runs its programme (two years, `fiscal_quarters`) and tapers over a year, the
    guarantee and the cuts run on (the cuts still growing with unemployment's rise, as consolidation does), the care
    build-out hires and the tariffs apply; the step a date falls in counts the part of it after the date, so a date is
    continuous at any step. A lever dated at the start of the quarter its trigger fires reproduces the triggered run
    exactly (T2: today's stimulus in every region, US 2028Q2 to China 2031Q1). Until the refit is in, a lever without
    a date still starts on its trigger, so every stored result stands; with the refit the fitted episodes are dated to
    what governments did, the presets' dates are set, and the triggers and "what governments watch" go (one version).
    Alternatives: keep the triggers for the forward runs (the page's dates set only by the presets); end dates as well
    as start dates (a guarantee withdrawn, cuts reversed).
82. **Decided 2026-10-27 (her call): the monthly refit, with more crashes.** Her words: "refit monthly, with policy dated
    in the model instead of triggers, matching each target at the frequency it is measured. Keep the dot-com bust as
    the held-out check, and add the crashes you listed." The plan (Claude's): the fit at a monthly step (decision 80),
    each target compared with the model at its own frequency — monthly unemployment and twelve-month core inflation
    against the model's monthly path, quarterly output against three months of the model, annual output and the
    standard series' annual unemployment for 1929-33 against twelve — weighted so that each series counts by its years;
    the inputs (shocks) monthly where measured monthly, interpolated in time where not, and stated; policy in each
    episode dated to what governments did, with sources (decision 81). The episodes: 1929-33 and 2008-10 as now; the
    dot-com bust held out; added, US 1937-38, 1973-75, 1981-82 and 1990-91, Sweden 1990-93, the euro area 2011-13, Japan
    after 1990; 2020 left out (a lockdown, which the model has no channel for). Every number that rests on the fit is
    restated once it is in; the predictions of 8 October stay as written. Order: the step and dated policy (in, Log 47),
    the two fitted episodes and the held-out bust monthly, then the added crashes one at a time, then the restatement
    (the case, the website's export and its JavaScript at the new step).
83. **Decided 2026-10-27 (Claude, under decision 81): a central bank's rate can be the rate it set** (`Rules.policy =
    "path"`, `Shock.rate` by step): in an episode where the central bank followed no rule the model has (the Fed in
    1973-75 and 1981-82, and as measured in 1990-91), its policy is dated as it was, so the fit tests the transmission,
    not a rule. The forward runs keep the rule. Alternative: a rule fitted to each episode's central bank.
84. **Decided 2026-10-27 (her call: "Extend the model first: fast rate-sensitive spending, relief measured from a
    pre-episode norm, oil's effect on capacity, expectations on smoothed inflation. Then fit all the crashes."; the
    forms of 84-87 Claude's): rate-sensitive spending** (`Common.a_f`, `f_speed`; check T5). Housebuilding, durables and
    business investment as a demand level moving toward −a_f × the real-rate gap (the policy rate less expected
    inflation less the neutral rate) by the share f_speed of the way a quarter (compounded at a month), beside the gap's
    own slow transmission (a_r); both fitted; off at a_f = 0. Measured housebuilding stays among every US episode's inputs,
    as in 2008-10, so in the fit the channel is the rest of rate-sensitive spending (out of sample, with no housing input,
    it carries all of it: an understatement, stated). Alternatives: the channel carrying housebuilding in the recessions
    the rates drove, dropped from their inputs (tried, Log 50); one transmission at a faster persistence.
85. **Decided 2026-10-27 (her call, as 84): relief measured from the rate debts paid before the start**
    (`Common.reprice`, `Region.i_norm`; T6). Floating-rate debt reprices over a year: the rate it pays is the policy
    rate's average over the past year, the months before the start at the year's measured average (i_norm), and relief
    is the fall from i_norm. An episode starting at a rate peak (July 1981's 19%) no longer reads the first cuts as
    relief: its debts paid 15% over the year before. Not fitted (a year is the floating share's definition). Off:
    repricing at once, from the start's rate. Alternative: a norm over the years fixed-rate debts were written, for which
    the model has no channel.
86. **Decided 2026-10-27 (her call, as 84): oil idles capacity** (`Common.cap_oil`, `cap_speed`; T7). With the energy
    term on, the capacity lost moves toward cap_oil × the rise in consumers' energy bill (% of GDP), a quarter of the
    way a quarter (approximate: idled over about a year); the output lost lowers the measured gap, and with it employment
    and the banks' losses, but not inflation: core inflation answers the gap against capacity. cap_oil fitted. The energy
    term is off in the forward runs until decision 27's condition, so they do not move with it. Symmetric (capacity
    returns as oil falls; the literature's asymmetry is not modelled). Alternatives: the production function's cost
    share alone (small); none.
87. **Decided 2026-10-27 (her call, as 84): expectations on the past year's inflation** (`Common.expect_over`; T8).
    Adaptive expectations adapt to the average of the past year's inflation (core, or headline where they form on it)
    in place of the last step's, the months before the start at index 0's twelve-month reading: a month's spike no longer
    passes into expectations whole (Log 49's January 1974), and the step matters less. Not fitted (a year: households'
    expectations track twelve-month inflation). On the window the quarter's anchor and Phillips slope hold at any step
    (T10): its memory is the window, counted in steps. Decision 80's per-step conversion belongs to the last step's form;
    put on the window it made a month's expectations several times as persistent as a quarter's (found by review,
    2026-10-27; Log 51). At a step under a quarter the last step's form also multiplies a one-step price impulse (a
    tariff's pass-through, an oil spike in headline expectations) by one over the per-step anchor; the fitted model uses
    the window, so that is left to the restatement should a forward run go monthly without it.
88. **Decided 2026-10-27 (Claude, under decision 82): each era's neutral rate** (`Region.r_star`; T9). An episode's
    neutral real rate is its era's: the New York Fed's Holston-Laubach-Williams estimate for the start's quarter
    (current estimates, one-sided; cached), the US 4.05 (1973Q3), 3.77 (1981Q3), 3.73 (1990Q2), 3.71 (2000Q1), 2.61
    (2007Q4), the euro area 1.33 (2011Q1); Sweden the euro area's 2.40 (1990Q2; no estimate for Sweden); Japan 3%, stated
    (none; the Bank of Japan's staff put it near 3-4% around 1990); 1929-33 and 1937-38 the model's 0.75 (no estimate
    before 1961). Kept at the start's value through an episode (the one-sided estimate falls within a slump, 2.61 to 0.81
    by 2009Q2, reading part of it as a lower neutral rate). Before, every episode ran on today's 0.75 and read each era's
    normal real rates as tight money; fitted that way the extended model explained the post-war recessions by it (Log 50).
    Not kept: a measurement error the fit exploits. The forward runs keep 0.75 in every region; HLW's latest (2026Q2) puts
    the US at 1.01 and the euro area at 0.09, a question for the restatement.
89. **Decided 2026-10-27 (Claude, under decision 82): the crashes abroad and 1937-38, measured.** Each economy one region,
    its central bank's rate as set (decision 83): Sweden's three-month Treasury bill (the Riksbank; its 500% overnight
    days were not what borrowers paid), Japan's call rate, the euro area's EONIA, the US's Treasury bill in 1937-38; its
    fiscal stance measured, the OECD's underlying primary balance (Economic Outlook 119, cyclically adjusted, so the
    model's own automatic stabilisers are not counted twice; for 1990-91 too, in place of the austerity rule dated at the
    budget agreement), and for 1937-38 the federal surplus (actual, so fiscal 1938's tightening is understated). Targets
    at their measured frequency; abroad the output gap is the OECD's quarterly GDP against its potential, each year's
    average within 0.1 of the annual gap it publishes. The bust's own collapse is measured, as 2008-10's housebuilding and
    2000-03's equipment are: private investment in Sweden (down 10 points of GDP, 1990-93) and Japan (business investment
    down 5); the euro area's periphery spreads, half passed to borrowers (decision 70's pass-through; Greece's yields after
    its restructuring left out). No stated bank losses: for Sweden they counted the credit crunch twice once investment
    was measured; for the same reason the model's own credit spread is off in Sweden and Japan (a cap of zero), bank
    capital still tracked (found by review, Log 51). Property prices are the BIS's real series. Each region's Okun slope is fitted on its own episode, as the US's is. Stated where nothing public
    measures it, each in its episode's docstring: wealth, bank capital and loans, the replacement and floating shares,
    the anchors. Alternatives: investment endogenous (the model has no accelerator; without it Sweden and Japan boomed on
    their fiscal stances, Log 50); stated bank losses (Englund's for Sweden).
90. **Decided 2026-10-27 (her call: "Add measured credit spreads (Baa against Aaa) as a target in the episodes, refit,
    and then show me the result before restating."; the form Claude's): the credit spread measured** (`spread_target`).
    In every US episode the model's credit spread (s, from zero at the start) is set against the change in Moody's
    seasoned Baa corporate yield over Aaa since the start's month (FRED BAA, AAA, monthly averages from 1919), by month;
    one standard error is half a point (set before the fit). None abroad: no such series. With it, the shared risk mood is
    off in an episode (`Episode.run`): with one economy active, the four economies' size-weighted bank stress was its own,
    which added the mood's coefficient (1.0) to the fitted spread per unit of capital lost. Before the refit, at Log 50's
    parameters, the measured spreads rejected its bank channel: 1929-33's model spread reached 15 points against 4.3
    measured (May 1932), 1973-75's 3.0 against 1.0, 2000-03's 2.1 against 0.7. With it (Log 51) the spread per unit of
    capital lost is 2.67 and the bank-run channel 0. Alternatives: the Gilchrist-Zakrajsek spread (from 1973 only); Baa
    over Treasuries (which moves with the term premium too).
91. **Decided 2026-10-28 (her call: "Adopt this fit (Log 51) and restate: the case, the export and the page's
    JavaScript at the monthly step, including the stored quarterly fit's own-feedback fixes."; the forms Claude's): the
    monthly fit is the model's, and the model runs by month.**
    - The fit is the episodes' (`code/episodes.py` fits and stores it, `results/episodes.json`; `global_crash.main`
      reads it). The quarterly fit (`fit`, `fit_loss`, `validation_targets`) is retired: one version. `run_1929`,
      `run_2007` and `run_2000` stay as the quarterly check of the monthly fit, with their own feedback off (the
      region's trade and exports, the shared mood), their levers dated at the legislation, Smoot-Hawley counted once
      (the switch from imports to home goods; its export loss is in the measured exports) and exports on the calendar.
    - The step is a month (`gc.DT = 1/12`; index 0 the end of September 2026). What is named by a quarter (2028Q4,
      2032Q2) is the quarter's average of its months, as quarterly data are measured (`to_quarters`).
    - Policy is dated (decision 81 completed): the model has no triggers. Each preset's levers start in the months its
      triggers fired in its central run (`trigger_dates`: region by region, the earlier dates' spillovers counted; the
      page's central settings), stored in `results/global_crash.json` and used whatever the bust. The case's levers
      start at the midpoint of the months they fired at its low and high ends. "What governments watch" is retired.
    - Own feedback is off in the forward runs too: the rest of the world's gap and the shared mood leave out the region
      itself and its union partners (whose trade is in the spillover), so the euro area's halves nest the one (E2).
    - Today's regions: relief measured from each central bank's rate averaged over the year to the start; the neutral
      rate HLW's latest (2026Q2: the US 1.01, the euro area 0.09, France with it, Sweden the euro area's, China the
      model's 0.75; decision 88's question settled this way); the Okun slopes from the fit (Sweden's, the euro area's
      for both halves).
    - Found by review on the way and fixed: the bust's loan losses landed two months late at a monthly step and, at a
      speed other than one, off the level paths' clock (`_spread`).
    - Alternatives (the veto window): the forward neutral rate kept at 0.75; the stated Okun slopes abroad; the case's
      levers on either end's dates (in the case's alternatives).
92. **Decided 2026-10-28 (her calls: "Refit first", on a measured series that separates bank runs from debt deflation in
    1929-33, then "Saturating fit"; the forms Claude's): the bank runs measured, and debt deflation levelling off.**
    - The bank runs of 1930-33 follow the money stock's measured fall (Friedman and Schwartz's, FRED M1444AUSM027SNBR,
      monthly), over its 35.8% trough in April 1933, read as all the banks' capital lost (where the model's stress
      stands by then), in place of the model's stress in the run channel for that episode (`Shock.runs`). The
      model's stress rose in a straight line from the crash; the money stock fell late and in steps (a seventh of its
      fall by December 1930, half by December 1931, three-quarters by August 1932, the last quarter in the 1933 panic
      and holiday, February to April). Elsewhere, and forward, the channel
      is the model's stress, so its coefficient means the same thing.
    - Debt deflation levels off (`Common.dd_sat`, fitted): the drag reads s (1 - exp(-x / s)) of the price shortfall x
      in place of x, the same at a small shortfall and at most s. Fitted, s is 11.4% at the slope's bound (0.5): the
      record supports debt deflation at small shortfalls (Japan 1991-95, 2008-10, Sweden), and once the runs are
      measured 1929-33 wants less of it at its large one (Log 53).
    - Weakly identified, stated: with the slope's bound widened to 2 the search turns the pair into a fixed drag from a
      1% shortfall, no longer a debt-deflation form; the stated bounds are kept as a judgement. An open question.
    - Alternatives: debt deflation off (the record fits worse, Japan above all; the forward runs nearest the stored
      model's); the linear form at the bound (the adopted fit of 27 October; the forward runs collapse); the form
      capped at the record's shortfall (does not stop the collapses).

## Next

~~**First — refit the bridges on (c)**~~ — **done 2026-10-27** (Log 46; decisions 72-79, hers to review; not pushed: the
order is watch first, then this repository, as in Next 13). Every bridge from the real paths to rates, debt and households
now rests on published evidence: the capex key on investment, one scale for investment, owners' saving and deficits, the
fiscal start at Sweden's measured primary balance, benefits following wages, rigid wages falling at a limited pace. Left
open by it: the investment key's pass-through (gross replacement, as Rachel and Smith read it, or only the net investment a
growing stock needs, about 0.4 of the term: it sets the size of the fall); linear bridges applied to a shift of half of
income from wages to owners, far beyond the evidence's range (a gap that falls as ownership broadens; a scale that is
not constant); the benefit rule's long-term floor (Sweden's riksnorm is price-indexed: a hybrid rule); rigidity that
erodes with time (a reset rate); and the reverse stress's three bridge dials drawn independently, though they share a
scale.

1. ~~Measure an extreme first: Sweden 1990–95~~ — **done 2026-09-24**, above. What survives: the
   identity (the curve as an average of expected policy) and the shapes of ordinary moves, even
   at 1994's size. What is missing, each with its episode:
2. **The swappable pieces**, now named by evidence:
   a. ~~**regime-mixture expectations**~~ — **built 2026-09-24** (`code/regimes.py`, above). Its
      evidence is the jump at resolution (E3), not the crisis-day shape (E1, corrected);
   b. **a destination that can jump** as well as ratchet — a regime change moves the anchor at
      once, and that is what produced the only parallel move (E4);
   c. ~~**an anchor-failure state**~~ — **built 2026-09-24** (`code/sovereign.py`, above; the
      bank–sovereign link to the interbank basis still to add);
   d. **policy regimes** as alternatives to the rule — currency defence (E1), does not deliver,
      yield cap;
   e. **event-scale speed** — daily moves an order of magnitude beyond today's at the front.
3. ~~**The macro block**~~ — **built 2026-09-24** (above), with the calibration of her call (a).
4. ~~**(b) Produced capital with an interest cost**~~ — **built 2026-09-24** (above).
5. ~~**The recognition clock as a mixture**~~ — **built 2026-09-24** (above).
6. ~~**Reverse stress testing, part 1**~~ — **built 2026-09-24** (above): the envelope, the
   drivers, the most plausible routes to ±100 bp.
7. **Then:** part 2 — the same draws against an exposure profile the bank side supplies privately
   (the pairing to test: large curve moves with fiscal strain or with the floor, and the real
   wage's fall); the owners'-saving bridge, now the one that matters most, deserves evidence before
   more structure (how rentier and profit income is spent); alternative policy regimes (flexible
   target, currency defence, yield cap) — the lower bound is currently what bounds the fall side;
   speed as volatility; euro (the ECB's published AAA curve parameters) as a further cycle.
9. ~~**A stylised bank**~~ — **built 2026-09-24** (above). Then: part 2 on the internal side — the
   bank's own balance sheet and behaviours on these paths (the pairings to test: the deposit windfall
   decaying; the long end gapping between ALCO decisions; commercial property on the wage-bill
   assumption; the falling-rate branch).
8. ~~**Speed**~~ — **built 2026-09-24** (above), and ~~**the forward-rate test**~~ — **built
   2026-09-24** (above): regime judgements digest over years. Open: a proper post-FOMC drift test
   needs surprise measures not on FRED; Swedish counterparts (Riksbank forward guidance against
   realized policy, Prospera surveys) if the public data allow.
10. **The pace, anchored** (decisions 20-21): a displacement pace that starts slow and rises on the macro block's
    logistic clock, fitted to stay within what has been seen; the exit share rechecked after two more quarters of
    participation data (and `decoupling.py`'s D6 restated on trends). Her case uses such a pace (a logistic from the
    bound seen), set by hand rather than fitted to the macro block's clock. Re-check early in January 2027, when the
    December CPS completes decision 21's second quarter of participation data: the exit share (0.94 against 0.36) and
    the bound (no September prime-age employment rate between 80.6 and 79.8 clears it: across that range the upper
    bound runs 0.11–0.33 of the paper's pace and non-employment's trend reaches t 1.2 at most, against the 2 that
    would clear it — scratch reruns, not in pace.json, on the stored quarterly fit; not rerun on the monthly fit of
    2026-10-28, whose bound is 0.218). The 2 Oct print is read through FRED (bls.gov is off limits).
    `[inferred]` On (c) the bound limits the macro block's clock too (the pace entry; the units and the dating of year
    0 are approximate).
11. **Her case, onward** (decisions 23-27): the case on the website (a page stating it, with the watcher's signs for
    and against each leaning); the US fiscal arithmetic (revenue with the wage base, interest as debt rolls over) so
    that deficits are computed, not priced; the crash model's displacement on the dated clock (one dating since
    2026-10-01, decision 43). The prints ahead: the FOMC (27–28 Oct, to verify against the Fed's calendar; the model
    raised in 2026Q4 in every run; restated 2026-10-28 (decisions 91-92): by month the case and its central run raise in
    October, 3.96 against 3.88, and cut by December), US core PCE for September and BEA's Q3 advance estimate (29 Oct), the Riksbank (4
    Nov), October employment (6 Nov). (Until 2026-10-26 this item said to re-run `code/october.py` after each print;
    that unit is retired to the tag `paths-pre-signfix`, Log 41.) **Amended 2026-10-26 (Log 40):** a print is not folded into the inputs of a run that makes a claim about it.
    Each data vintage is frozen and committed before the prints it is scored on, and scored on them afterwards; the
    FOMC, the Riksbank's 4 Nov decision and October employment (6 Nov) are tests of the stored runs, registered in Log 40.
    **Since 2026-10-26 (Log 42):** the vintage is `cache/start/` (`code/vintage.py --refresh`, then `code/decoupling.py`,
    `code/global_crash.py`, `code/pace.py`, `code/case.py` and every battery, committed together); October's vintage
    (`cache/october/`) is kept for the record. The next refresh: after the December deadlines, or before a print the
    case should be scored on (the October employment report is already a test of this vintage: the case's 2026Q4 US
    out of work 4.53%, unemployment 4.49%, as restated in Log 44 before the print; 4.32 in Log 42; on the monthly fit,
    restated 2026-10-28 (decisions 91-92), 4.36% and 4.34% on 2026Q4's average, and in October 4.26% and 4.24%).
12. **(c), onward** (decisions 31–42; 39, 41 and 42 decided 2026-10-01, pending the refit of Next, first): before (c)
    carries rate stress, a land-slack corner and `rho_rate_share`; the chain's own depreciation (FA 3.1ESI / 3.4ESI)
    for sigma; WP2026-01's labour definition (the self-employed imputation) and a primary copy of its numbers; README's
    findings, not yet restated (its layout and battery list brought up to date 2026-10-01, log 36); `[inferred]` a lambda
    (recursive automation) dial in the watcher's dial table, since on (c) cheaper machine-building feeds straight back
    into wages.
13. **The commit and the watcher's site, in order** (the watcher is its own repository; nothing is deployed from here).
    Committed and pushed 2026-10-01. The site work is on watch main (785b34c and the fixes after it), pushed: 23 commits
    over 2b84476 to 785b34c (`git log --oneline 2b84476..785b34c`): fd4ede2 (patch 01, the site
    audit's fixes — the exit share and the pace bound as measured, and who shed the jobs outside care, computed from
    FRED at build time), e28a606 (02, the export and guide on (c) through `macro.central()` at both roots, return fixed,
    checked against macro_scenarios.json, calibration_c.json and capital_feedback.json), c22b122 (03, the lens on (c), a
    lambda dial), 95b822c (04, the stored results snapshotted with each export), and the branch review's fixes e130367
    (§4 states the rate path as an assumed link carried over from (b), with the debt dip from the surplus start; the
    pace bound with its endpoint; the job counts on one FRED release), 119b72e (the site server's deploy notes) and
    e94366a (the balanced-start debt figure in §4 labelled as the first fit's). After her instruction of 2026-10-01: fb32ab8 (the
    merge of origin/our-view a44da67, bringing b7f9d45, 64152fe, ebdf6f1 and a44da67 — "Our view", the wider watch as
    indicators, the model pinned to dates), a4f24a9 (the model page and Our view dated on the model's one dating,
    decision 43), ea85a7a (one version: the export's fallback to (b) removed — it refuses a model without
    `macro.central`, `deep_tech` or `global_crash.quarter_label` and writes nothing), b4270fd (guide §9 lists the wider
    watch's indicators), 878657d (the lens: her case's dating settled, decision 27 on Brent's level, the October
    central), d14e77e (the Swedish wage round's news query as phrases), 96ceabc (the charter spells out market
    shorthand), 931cceb (the data lines before the start stop at the start), 632f609 (the model's runs named by their
    end quarter, not "six years"), c1cb91c (a test's with statement split), 38c12f0 (basis points spelled out on the
    site's own pages) and 785b34c (the deploy notes: one site branch, main; the export's other failure). The site's
    crash runs stay at 24 quarters (to 2032Q2, each run's end quarter named on the page), because pace.json's quoted rows are the stored 24-quarter runs; Our view's case runs 25 (to 2032Q3); if the stored crash
    runs move to 25 quarters, the export's N follows. origin/main, origin/site (968a05e) and origin/our-view
    (a44da67) were all ancestors of the site work, so main fast-forwarded to it. **Her instruction of 2026-10-01**
    (paraphrased: one version, so that it is easier to keep track of; she updates the site server herself once
    everything is pushed and sorted): one site branch, main.
    **The order, decided 2026-10-01:** (i) watch main, fast-forwarded to the site work, pushed first; (ii)
    laborformal committed and pushed immediately after (the switch, with `code/macro.py` and
    `results/calibration_c.json`, which `macro.central` reads; the one dating in `global_crash.py`, `case.py` and
    `case.json`; the October bust; the calls of log 35); (iii) her update of the site server (the steps are in the watch
    repository's deploy notes). Why watch first: watch main has no fallback to (b), so between the two pushes the site
    server's new export refuses the old laborformal, the build fails and the last good site stays up, with nothing wrong
    on it; pushing laborformal first could let the server's old watch code publish a guide mixing (b) and (c) for a
    cycle. After her update the export runs on calibration (c) at both roots (a failed export keeps the last export and
    snapshot: consistent, but stale; a re-solve more than `macro.central`'s relative 1e-9 off the stored parameters
    would be a platform difference, not the push order); automation.json on calibration 'c' (the real wage's peak at
    t = 0, participation at year 6 0.54–0.56); the first build fetches the six payroll series together — PAYEMS,
    CES6562000001, CES0000000010, CES9091000001, USPRIV, USGOVT — and writes them only if total nonfarm equals private
    plus government in every month (otherwise, or if FRED fails, the build fails and is retried). After main is
    pushed, origin/site and origin/our-view (fully merged) are deleted, so there is one site branch; `claude/state` (the
    watcher's state) stays. Then re-run the site's facts against any re-run recognition.json and reverse_envelope.json
    (facts.py reads both). r* and debt stay on the site, labelled as illustrations (decision 39).
14. **The splits tracker** (decisions 53-65): her read and vetoes (decision 58, saving's wealth slope: her call of
    2026-10-13, the literature slope); then the freeze (`code/splits.py --refresh --write-baseline`, `checks/check_splits.py`,
    commit with `cache/splits/`, tag `paths-splits-freeze`, push the tag the same day; then `code/splits.py` again and
    commit and push `results/splits.json`, whose status then says frozen: the page says "fixed on" only from those
    results, `SPLITS.md` §9.2); a quarterly run of about an hour (`SPLITS.md` §7); the first judged look on 15 November
    2027 (`--refresh --look`, commit, tag `paths-splits-look-2027`); the page on the website reads `results/splits.json`
    (deploy it after this repository is pushed, so its link to `SPLITS.md` resolves).
15. ~~**France as a region of its own**~~ — **built 2026-10-27** (Log 45; decisions 70-71). (Decision 69; her suggestion of 2026-10-26: "maybe it would make sense to have
    france as its own region since that seems to be where some of the action is happening"). France's ten-year over
    Germany's is 1.66 points and rising, the widest in the euro area: a fifth region in the crash model, inside the
    monetary union (the ECB's rate set on the union's output and inflation, France's own spread over it, passed to
    French borrowers; its fiscal response bounded by the spread; its banks holding its debt, so the spread reaches their
    capital), on the vintage (INSEE or Eurostat unemployment, the HICP, the Riksbank's daily yields), through the
    website's simulator and the checks. Open: the doom loop for the rest of the union's and the US's sovereigns; a
    premium that rises with debt's level; France's own Okun slope and speed (approximate, as the euro area's).

## Siblings

`../three-taxes/docs/design_memo_2026-09-02.md` §7.1 (the land-tax announcement shock to
mortgages, covered bonds and banks) and its market reading of the real-rate rise (saving short
of investment: rho up). Here rho enters as the curve's destination; the two should agree when
the macro block lands.

## Log

1. **2026-09-24 — founded.** Her call after the curve measurement: start `paths/` with the
   curve layer (policy, destination, speed, basis). Her question on the day — is the hump a
   transitional shape, with a truer parallel mode once flat? — produced the timing result and
   the cascade. Built `code/curve.py`, `code/cycle.py`, `checks/check_curve.py` (first run
   18/21: one wrong expectation — the timing-share floor is 0.196, not 0, which is what made the
   delay reading visible; one real bug — the policy rule never took its last 25 bp step under
   round-half-even; one over-strict phase window — the 1M is pinned only while the first move is
   more than a month away; then 22/22), `code/us_modes.py` (FRED vintage in `cache/`). All
   uncommitted pending her read.
2. **2026-09-24 — the openness principle.** Her question: are we assuming what happens next will
   look like what happened before? Answer given: the curve identities and the paper's price
   system do not; the phase sequence, the parameter ranges, the policy rule, mean reversion and
   the "late in the pricing phase" reading do. Her call: stay open to a more extreme path. The
   principle is recorded above; the plan reordered so an extreme episode is measured (Sweden
   1990–95, public Riksbank data, confirmed reachable back to 1983–87) before the swappable
   pieces are built. The thread's first commit carries both entries.
3. **2026-09-24 — Sweden 1990–95, the first extreme.** `code/se_1990s.py` on the Riksbank's
   public API (cached in `cache/riksbank/`; the 12M bill ends in 2010, so the API answers 204 for
   the recent window and the script treats that as empty). Findings above: a regime mixture on
   the crisis day that neither path family draws (one-speed 1,069 bp, two-stage 296 bp RMSE, calm
   17 bp); the only parallel move came after the float, when the anchor changed; the 1994 crash
   ordinary in shape and extreme in size, with +259 bp of it a spread over Germany; front-end
   daily moves 12× today's. The plan's swappable pieces are now named by their episodes.
4. **2026-09-24 — regime mixtures, and a correction.** Her go on the mixed-regime piece. Before
   building, the 1992 evidence was rechecked and found overstated: the crisis-day 1M bill implies a
   negative 1M→3M forward, which no expected path can price, so the day's misfit came largely from
   that quote; without it the two-stage cascade fits (25 and 111 bp). The float day (19 Nov 1992:
   the curve down 100–210 bp in one day with policy unchanged, the period's largest daily moves at
   2Y and 10Y) is the evidence the piece rests on instead. Built `code/regimes.py` (static and
   arrival mixtures; recognition and resolution; closed forms where static, Gauss–Legendre where
   not), `checks/check_regimes.py` (12/12; first run 11/12 — the timing-only resolution hump was
   checked at 1M instead of in its limits), `code/regimes_demo.py` (stylised). `code/se_1990s.py`
   now records the 1M→3M forwards, the fit without 1M, and the float day. Commit e654d19's
   subject line ("a regime mixture no smooth path draws") carries the overreach; this entry is
   the record of the correction.
5. **2026-09-24 — the sovereign spread.** Her go. Built `code/sovereign.py` (spread = average
   expected loss + convenience; loss path a cascade; regimes reuse `regimes.py`),
   `checks/check_sovereign.py` (6/6; one reported detail was scaled ×100 too high — the per-10-
   points-of-p recognition move — and corrected before commit), `code/sovereign_monitor.py` on
   the Riksbank API's government benchmarks 2019–2026 and 1993–95. Finding: France's 10Y spread
   over Germany at +110 bp, its widest since at least 2019 on the latest day, widening from the
   back; the Netherlands and Finland tightening; Sweden 1994's spread curve lifted nearly level.
6. **2026-09-24 — the macro block, calibration (a).** Her go. Found first that the repository's
   `pinning/` Appendix B is older than the SSRN version she sent (different formulation, different
   numbers; the SSRN's `check_interior.py` is not in the repository) — built on the SSRN version,
   gated on its published figures. Calibration: the four first targets (labour 0.47, employment
   0.60, 3 baskets a person, shelter a third of the basket) are jointly infeasible in the two-factor
   benchmark — she asked why; answered with the accounting (non-wage income is all land rent;
   Appendix B's space is pure site) and three options; her call: (a) now — the site part of shelter
   (13%) as the target, machines up to 50x better on the easiest task, a convex schedule, the
   machine chains' 0.40 labelled as scarce inputs plus capital income — then (b). Bugs caught on
   the way: the owners'-saving channel entered r* with the wrong sign (fixed before any check ran);
   the investment proxy first used machine-service quantity, which falls as machines improve
   (replaced by the pace of tasks moving to machines); policy started off the 25 bp grid. Built
   `code/macro.py`, `checks/check_macro.py` (14/14; first run 13/14 — a check that compared the
   whole curve rather than its expected-path part with the policy rate), `code/macro_scenarios.py`.
7. **2026-09-24 — (b), produced capital.** Her call after (a). Built Appendix A.4's user cost into
   the core (nesting Appendix B at return 0, depreciation 1 — the old battery stayed green through
   the change), `CAPITAL_BASE`, the rate feedback in `macro_path` (sequential when the return follows
   r*), checks A1–A7, `capital_figure()` in `code/macro_scenarios.py`. A fifth target (capital at
   1.5× income) turned out inconsistent with the other four — the labour-share target fixes the
   machine services' share and the user cost then fixes the stock at ~3× — so it became an outcome,
   compared with public fixed capital (~3). Findings above: the site, not capital, takes the gains;
   rates feed back weakly; a small loop in the down-phase (on (b); restated on (c), log 33: the feedback stronger, the
   loop's lag phase negligible).
8. **2026-09-24 — recognition as a mixture.** Her go before going to lunch ("keep going without
   me for a while"). Built `code/recognition.py` (two worlds, Bayesian learning with narrative
   jumps, the market curve as a static mixture, a common policy rate), `checks/check_recognition.py`
   (10/10; first run 9/10 — L2 compared log odds recovered from probabilities that had rounded to
   one, so `learn()` now returns the log odds too), `code/recognition_scenarios.py`. Findings above;
   the headline for her: recognition comes early relative to the real change and fast, and under
   the default bridges it barely moves the curve — which points the next unit at the bridges.
9. **2026-09-24 — reverse stress testing, part 1.** Continuing while she was away. Built
   `code/reverse.py` (the dials, the sampler, the run, rank correlation, nearest breach),
   `code/reverse_envelope.py`, `checks/check_reverse.py` (11/11 on first run). Four problems found
   on the way, each fixed before the numbers above: (i) a first run had a −1,387 bp tail — the
   destination followed r* below the lower bound — so the destination is floored at −0.5% in both
   `recognition.py` and `macro.curve_path`, and the required return at zero (a few draws had broken
   the solver); (ii) the world's ten-year average neutral rate ran off the end of the 15-year path,
   jumping the curve in the last quarters — now a full window with the last value held, and the
   reverse runs simulate ten years beyond what they report (R2: the default run moves under 1 bp);
   (iii) the rate feedback cycled quarter to quarter in about 5% of draws (49 of 1,000; up to 65
   reversals) — near full automation a small change in the required return moves the automation
   margin a lot — now partial adjustment with a one-year half-life (R6); the committed recognition
   and capital numbers moved by at most 0.3 bp and 0.02 years (the loop's +0.16 pp is now +0.14,
   recognition starts at 2.3 rather than 2.4 years); (iv) uniform ranges in levels put the default
   automation depth at the edge of its range and made most draws mild (median real-wage low 0.97)
   — the scale dials are now drawn in logs (median 0.77). Findings above; the headline for her:
   under this mechanism the rate move's sign is a question about owners' saving against deficits,
   while the wage and fiscal damage is robust.
10. **2026-09-24 — speed, and its history.** Her point after reverse stress part 1: markets run on
    cognitive labour at a human speed; AI trusted to guide investment could lift that bottleneck.
    Built on the learner (`recognition.py`: capacity, trust following the technology with a lead,
    a shared error with an aware/unaware market, digestion with a share and a half-life; `refine`
    for a weekly grid; all defaults nest the committed model — `recognition.json` reproduced byte
    for byte). The first run changed the framing: more capacity mostly makes recognition *earlier*,
    and with trust following the economy the market wakes up before the AI is trusted; abruptness
    comes from digestion — the old default (instant Bayes) had been an AI-speed market all along.
    Mid-run her second point — internet adoption may have changed digestion before — became
    `code/digestion_history.py` on FRED's daily Treasury yields: drift in the 10Y and 2Y before
    the mid-1990s, none after, a little overshoot since 2009; the decline gradual, predating the
    Fed's 1994 announcements. The measured 1980s rung was added to the speed ladder, and the
    quarter-long half-life relabelled as the assumption for regime news it is. Also recorded: the
    monthly GS10 series was tried and dropped (monthly averages build in autocorrelation), and an
    event test on target-change days was inconclusive (31–99 events an era, the 3M bill as the
    surprise). Checks 15/15 (first run 14/15: one exact-equality check tripped on rounding —
    (σ/√7)² is not σ²/7 in floating point).
11. **2026-09-24 — the forward-rate test, and a correction.** Her go. The Fed Board's site failed
    certificate verification from Python behind the corporate proxy; verification was not turned
    off — the file was fetched through PowerShell (the Windows certificate store) and a trimmed
    vintage cached. statsmodels is not in the venv; the Newey–West regression is written out and
    checked against White's errors (E1). The correction: digestion first acted on the log odds,
    where a sliver of overwhelming evidence already means certainty — a 5-year half-life barely
    delayed recognition (5.0 against 3.3 years). Everything the evidence measures is a level
    (yields, forecasts, anchors) and the market's expected rate is linear in the belief, so
    digestion now acts on the belief; the committed recognition results are unchanged (they do not
    digest), the speed numbers above are restated (the first week's move under human digestion 0.6
    → 2 bp, the ladder 2 / 16 / 33 / 40 / 40 bp), check L6 restated. Findings above. The
    constant-gain check (E3) first failed on a residual tolerance tighter than the optimiser's own.
12. **2026-09-24 — a stylised bank.** Her question (NII up first, then tightening lowers house and
    asset prices, then the interest income flows back into assets), answered in text first — the
    windfall is the deposit spread, not the mortgage book; reserves are not money taken out of
    lending; the recycling lifts prices by pulling rates down (indebted demand); in the paper's world
    rates and wages move against each other — then built. Bugs caught before any finding: zero rates
    passed in basis points where the bank reads percent (NII 44% of assets); a single average
    loan-to-value made loss given default always zero (now a lognormal spread, closed form, checked
    against Monte Carlo); the deposit book began off its settled mix, drifting even in the status quo;
    a pure tightening known from the start put the price fall before the start (now a surprise at
    year 1); the figure's loop asked for a variant that did not exist. First calibration of deposits
    passed 75–80% of a rise through; recalibrated toward Sweden's 2023 experience (about 0.4–0.5 a
    year on). Checks 12/12 after two restatements: the house-price integral now exact per interval
    (it had been a right-endpoint sum, 0.2% off), and the refinancing check stated at the grid's
    ramp.
13. **2026-09-24 — the paths exported for banks.** Her call: part 2 — a bank's own balance sheet on
    these paths — runs on the bank's internal side, from first principles on its raw data. What
    crosses from here is only public: `code/export_paths.py` writes `results/paths_for_banks.csv` —
    per scenario and quarter over 25 years, the policy rate, the market's zero rates (3M to 10Y) and
    the true world's real wage bill (real wage x participation, 1 at the start), for the status quo,
    the pure tightening, deficits dominating, owners' saving dominating, and deficits dominating
    with slow regime digestion then AI adoption. A user lays the changes on their own curve. Nothing
    from the bank side is recorded here, by the wall.
14. **2026-09-24 — the floor evidence.** Her choice of next step: test floor behaviour on public data.
    SCB's PxWeb API and the Riksbank's
    SWEA API both reachable; STIBOR leaves SWEA in 2020-07 (publication moved), so margins are measured
    over the policy rate, STIBOR as the cross-check. Built `code/floor_margins.py` and
    `checks/check_floor_margins.py` (7/7 on first run). Findings above. Figure: two titles clipped and a
    label collision fixed before the commit. (Two clauses describing the internal side removed 2026-10-26,
    by the wall; Log 41.)
15. **2026-09-24 — the export carries the credit side.** Her call: credit, next. A bank's credit book needs
    more than rates and the wage bill, so `results/paths_for_banks.csv` gains, per scenario and quarter,
    each 1 at the start: the real wage, the share of the start's workers still employed, the real site
    rent, the real price of a site as the market values it (`bank.house_price`: belief-weighted rents
    discounted at the real 10Y plus a premium) and the price level. The existing columns are unchanged
    (checked cell by cell). What the new columns say, before any bank: **in the model's own world
    collateral is not where the risk is** — the site takes automation's gains, so the real site price is
    ×3.0 by year 10 when deficits dominate and ×17 when owners' saving dominates (rates at the floor, the
    discount rate at its 1% guard), while the wage bill falls to 0.74 and 0.63 and employment to 0.89
    and 0.84. A bank's credit loss therefore turns on a question the model's single land market cannot
    answer: whether property income and values follow the site (the model) or the wage bill (offices,
    shops and flats are rented by people who work). A user should run both. One quirk, disclosed: the
    status quo's site price drifts to 0.85 by year 5 because the market starts with a 5% belief in the
    automated world and learns it away; comparisons against the status quo cancel it.
    **Restated on (c) (log 33; check_bank X4):** at year 10 the site price is x2.79 / x19.34 (x18.9 by year 5), the
    wage bill 0.297 / 0.176 and employment 0.629 / 0.507; the status quo's drift is 0.818. The (b) numbers above are
    (b)'s, computed now from its export: x3.02 / x17.39, 0.736 / 0.625, 0.892 / 0.838, 0.853.
16. **2026-09-24 — deposits against wages.** Her choice after credit: measure the deposit side the paper's
    channel reaches. Statistics Sweden's household deposit volumes by type are not in the MFI tables' English
    tree; the financial accounts carry them (transferable and other deposits, households S14), with nearly
    all household deposits classed transferable, so the split by type is not usable — total household
    deposits are the series. Built `code/deposits_wages.py` and `checks/check_deposits_wages.py` (9/9). The
    export (`results/paths_for_banks.csv`) gains `income_real` and `labor_share`; earlier columns unchanged,
    checked cell by cell. Findings above. A figure fix before the commit (overlapping titles, a caption over
    an axis label); one heredoc edit that wrote literal line breaks into titles, fixed by hand.
    **Restated on (c) (log 33):** the household-income reading this export supported — up about two-thirds by year 10
    on (b) — disappears on (c): about flat (0.96–1.09 of the start; the deposits entry above).
17. **2026-09-24 — a demand gap.** Her questions after the short-term note: what if inflation rises, or deflation;
    fewer people with more income each; yields up, inflation up, stocks down — which weird scenario is likeliest?
    My pushback (income shifting to high savers lowers total demand; the likeliest weirdness is a price split under
    a calm headline; the model cannot make a recession) and her call to build it. Built `code/demand.py` (the
    measured Swedish Okun and Phillips slopes; monthly periods added to `deposits_wages.scb_table`) and
    `checks/check_demand.py` (13/13). A first version of the shock test started today's economy below neutral,
    which is a stimulus, and so mixed room with stance; restated to vary only the room to the floor.
18. **2026-09-24 — who carries the people who leave work.** Her question: is dependence in the model, and could
    stimulus checks be modelled? It was, frictionless (the paper's pooled household). Built `code/households.py`
    on the demand layer (which now takes a demand level from other layers, entering at once:
    `gap_t = a1 gap_{t-1} - a_r (real-rate gap) + level_t - a1 level_{t-1}`) and `checks/check_households.py`
    (11/11). Central case today's Swedish state support, her call; family-based support is the next variant. Bugs
    caught before any finding: debts that could not grow with income (the status quo drifted); temporary spending
    entered at a sixth of its size; a rigid-wage rule with elasticity 1 and no unwinding sent 70%+ out of work;
    and patch scripts that stopped at a text they could not match left the file unchanged — caught, redone by hand.
19. **2026-09-24 — family-based support.** Her call after the state-support central case. Added to `households.py`
    as a regime (`FAMILY`) with a finite network capacity — the one feature beyond the dials, because a network can
    carry a few people but not a mass exit — and variants without the cap, with rigid wages, with checks. Checks
    now 18/18; the tail check was first written claiming "longest at the floor" without testing it, fixed to test
    it. The figure's title strings broke once more on a heredoc escape, repaired in place.
20. **2026-09-24 — a world crash model.** Her questions: unemployment looks soft; why not a Great Depression, when
    pressure can change the rules; bring in the US, Europe (and China, insofar as possible); the big picture, not
    SEB. Proposed the design with a validation gate (reproduce 1929-33 and 2008-09 with one parameter set) and built
    `code/global_crash.py` and `checks/check_global_crash.py` (12/12). The first fit matched 1933's endpoints only and
    the path was wrong (no 1930 collapse, a 2011 trough); refitted on the paths with measured shocks (stocks, exports,
    housebuilding) and a global search. Fixes before findings: a fiscal cliff when stimulus ended (now tapered), the
    structural drift buried in "as usual" (now its own dial), an income guarantee standing in for "expand" (it had
    been a bigger temporary stimulus), and the 1930s' rules on today's debts running into a clamp (now reported at
    four years with a no-bottom flag). Two check texts claimed more than they tested; fixed.
21. **2026-09-24 — two waves, and Baumol concentration.** Her call: go ahead with the two-wave split; mid-build, her
    question on job growth going to women and labour-intensive sectors. Built `code/exposure.py` (ILOSTAT occupations,
    pay and recession behaviour; China from the ILO's modelled estimates) and the split in `global_crash.py`, and for
    her question `code/baumol.py` (US payrolls to Aug 2026, labour force surveys to 2025, BEA prices and spending,
    ILOSTAT earnings) with `checks/check_exposure.py` (17/17); `check_global_crash.py` 20/20. The ILO API needs the
    Windows certificate store here; its files are cached under `cache/ilo/`. A check caught round-off leaking
    physical displacement before robotics (fixed: the physical share is computed directly); the waves figure showed
    the fiscal trigger's timing moving China's output the wrong way (stated, tested without it: W5). Watcher: the
    second-wave and care-only tripwires, replayed on 1990-2026 (separate repository). Not done: the Swedish household
    layer's displaced still earn the average wage (the first wave's premium would deepen its losses).
22. **2026-09-24 — care as the absorber.** Her call: build it; mid-build, "there must be a limit to how much care can
    absorb", then "Norway also has their sovereign wealth fund". Added the ceiling (Norway's share, ILOSTAT for 18 rich
    economies), the gate (women's shares by occupation, men's propensity for care) and the pace to `exposure.py` and
    the absorber to `global_crash.py`; 31/31 and 20/20. Caught before findings: a quick comparison run on the rounded
    fitted parameters looked as if earlier rows had moved (they had not: all 48 identical with equal parameters); care's
    trend kept growing after the build-out hit the ceiling (fixed: one care level for both); and with a slow hiring
    rate (0.10) the unmeasured rate, not the measured limits, decided the result (set to 0.25, tested at 0.10 and 0.50).
23. **2026-09-24 — is the ceiling need or financing?** Her calls: test the financing link; Norway's fund; the fund's
    effect on borrowing costs. Built `code/financing.py` and `checks/check_financing.py` (10/10) on the OECD's health
    accounts and Economic Outlook (public SDMX API; the health accounts sit at version 1.1, the default key returned
    404), ILOSTAT for 37 OECD economies, the World Bank and Statistics Norway (10486, 11012, 09189); the IMF's API is
    closed to this machine. Norway put on mainland GDP, stated and shown both ways. No statsmodels in the venv: plain
    least squares with robust standard errors.
24. **2026-09-24 — the financing limit.** Her call: go ahead. Added taxes on labour by region to `financing.py` (OECD Global
    Revenue Statistics via SDMX), and the three sources with their limits, drag and price of debt to `global_crash.py`;
    38/38. Verified before findings: with the price of debt at zero the 62 earlier runs are reproduced exactly; the
    first draft counted no debt when borrowing paid for the build-out (fixed before any run was saved).
25. **2026-09-25 — the synthesis.** Her question: zoom out, what is all this pointing to; then her call to write it up.
    Written as a private page for her to present ("After the Wage"; outside the repo): seven findings in three parts
    (the danger; what is already visible; the way out and its limits), each with its evidence and one caveat, two
    charts drawn from the saved results, the reading marked `[inferred]`, what to watch, where the evidence is thin.
    Public data only; every number taken from results/global_crash.json, baumol.json, exposure.json, financing.json.
26. **2026-09-25 — output without work.** Her question on rising output and GDPNow against labour shedding; then her call
    on the three proposed changes (a participation margin, the build-out measured, two tripwires). Built
    `code/decoupling.py` (FRED: BLS productivity and labour force, Federal Reserve industrial production, BEA investment
    and imports, GDPNow; the FRED website's search found the import and structures series) and wired the measured US
    build-out and exit share into `global_crash.py`. Verified before findings: with the exit share at zero and the old
    build-out, all 74 earlier runs are reproduced; exits needed the same cap as unemployment (a first run put more than
    the labour force out of work under eroding rules); a variant keying the fiscal triggers to non-employment changed
    nothing in a bust, so the displacement-without-a-bust runs were added where it matters. Eleven findings checks moved
    from unemployment to non-employment and were restated as found. Watcher: the labour-share rule as first written fired
    14 times since 1990 (a long decline sets new lows often) and the participation rule missed today (a 12-month window
    on a 23-month slide); both redefined on the replay; participation kept out of crash.joint (it added a 2011 false alarm).
27. **2026-09-25 — the pace against what has been seen.** Her question (is the model calibrated to the participation,
    output and hours changes already seen?), then her call to open it as a unit. Built `code/pace.py` and
    `checks/check_pace.py` (8/8); `check_global_crash.py` 43/43 and `check_decoupling.py` 6/6 unchanged; no change to the
    model. Caught before findings: the first version fitted the pace to the exits at the window's endpoint (0.71 of the
    paper's) and a spending offset to the gap (43%); its figure showed the endpoint resting on June 2026 (participation
    −0.6 in a month after two flat years), so the unit was rebuilt on trends with robust errors and the offset dropped
    (the parameter added to `global_crash.py` for it was reverted, unused). Check A6 first claimed the loop explains under
    half of the gap's fall at the upper-bound pace; it is 55%, restated. Mid-unit, her questions on adjusting for care and
    for the build-out's jobs: added as sensitivities (A8), not corrections. Corrects log 26's reading of the exit share.
28. **2026-09-25 — her case.** Her call: pin down a "this is what we think is happening" case across the model, the watcher
    and the website, with her leanings; then, after Claude's critique (the US worry as fiscal dominance, Europe as one
    region, adoption as the lever, energy and Japan missing), her call to watch energy, private credit, housing, Japan,
    Korea and Taiwan (the watcher's wider rules) and to finish the case. Built `code/case.py` and `checks/check_case.py`
    (11/11) and four additions to `global_crash.py`, each off by default; `check_global_crash.py` 43/43, `check_pace.py`
    8/8, `check_decoupling.py` 6/6, `check_financing.py` 10/10 unchanged. Caught before findings: the first run quoted one
    number for 2032 (46%) when it rests on the adoption lever, and a peak that is the horizon's last quarter (still
    rising); restated as a band with 2028Q4 beside it. (That "2028Q4" was index 8, 2028Q3 as measured: one dating
    since 2026-10-01, log 35.)
29. **2026-09-25 — the start pinned, the bust movable.** Her call on the website's model page: dates from a start year,
    the data before it, and the bubble bursting at different times. `global_crash.py` gained `START` (2026Q4 — one
    quarter late; 2026Q3 since 2026-10-01, log 35 — quarter 0:
    the regions measured on data to September 2026; `case.py` now reads it) and `ai_shock(delay=...)`, the bust starting
    that many quarters later with the build-out holding until then. Off by default: `check_global_crash.py` 43/43 and
    `check_case.py` 11/11 unchanged.
30. **2026-09-30 — the machine chain measured.** Her question: is the paths model's theta off, and what would fixing
    it do? A feasibility study first (what the repository holds; wages and machines; rent and the basket;
    identification — each checked by a second pass that tried to refute it): (a) and (b) put labour's share of a
    machine's cost at 0.026 and 0.0013–0.0024 against a measured 0.47–0.58, and it is not a one-parameter fix — in
    both, the machine chain's non-labour cost is almost all "land". Built `code/chains.py` and
    `checks/check_chains.py` (18, then 23 after the review) on the λ thread's engine, read-only; one FRED mirror file
    in `cache/`, BEA's files in the λ thread's gitignored cache. Caught before findings: the first impact guess
    ("later and shallower, automation partly self-limiting") had the mechanism backwards — the closure multiplier
    amplifies — and Unit 2's runs showed the opposite; the model-against-data multiples first mixed bases (19 / 250
    times; like for like 34 / 272); the bundle's own cost split was missing, so (c) first paired the bundle's theta
    with the machinery set's split (G1 built it: the NOS bound 0.231, not 0.168); the CFC cap list left out 5415
    (22–24% of the set's weight in 1999–2007); an independent raw-file path added (C20); BEA's import convention and
    the I-O release's age disclosed; thresholds set after seeing the data flagged. Also found: the coverage figure's
    land residual counts nonprofit property as land (pinning STATE, Open 10).
31. **2026-09-30 — calibration (c).** Three designs built in parallel and judged (minimal, separate, data-first): the
    data-first one won, with grafts from both others; Appendix A.4 needed no new equation, only the solver's search up
    to the chain's ceiling. Built in `macro.py` (additive: the legacy solve bit-identical on the paper's instance,
    (a), (b), (b)'s +200 bp path and 60 random economies; all 20 batteries byte-identical across the change),
    `code/calibration_c.py` and `checks/check_calibration_c.py` (36, then 42, then 47). Caught before findings: the
    first central mixed import bases (WP2026-01's labour target keeps foreign content apart, against tot-basis theta
    and chain share) and paired the bundle's theta with the machinery set's split — sigma 0.090, multiplier 7.34,
    participation at year 15 0.113 / 0.199; restated on one basis with the bundle's own split (the open reading: sigma
    0.330, multiplier 2.42, 0.231 / 0.341), the old run kept, labelled superseded; the rate fragility and the
    multiplier are one 1/sigma object, so the +5 pp bound on sigma is now gated; (a) and (b) have second roots too, so
    comparisons are root for root; the g0 change separated from the chain's; the measured-site "exception" was a
    comparator at a different site (with (b) at the same site it disappears, bar the high root's real-wage rise); a
    division by zero at the ceiling's edge (none in 6,196 edge economies after the fix); M13 relabelled a readout; (a)
    first shown on the wrong Figure 7 object. The answer to her question: yes, the model was off on the machine chain,
    and fixing it deepens and speeds the paths rather than softening them.
32. **2026-09-30 — the week's reading and the watcher's site** (in scratch; no repository changed). The data, the
    news, the public site and the watcher read against her leanings, every claim checked at primary sources before
    use. What carries into this thread: the pace bound does not move (no CPS month since 25 Sep); on (c) the macro
    block's own employment path falls from year 0 (the pace entry); the site cannot move to (c) before the watcher's
    patches 02 and 04 (Next 13). Corrected by the check before anything went further: dated Brent ran $114–121 in the
    last week of September (22–29 Sep; the $102–107 of the news is the futures strip), after peaks of $130.80 (15 Sep)
    and $138.21 (7 Apr); the oil rule clears on base effects, not at a price; August core CPI was 2.76% (the watcher's
    2.4 was wrong); the care-only episode was federal job cuts (by its end; in its first year private jobs outside care
    fell too — the Baumol entry); the crash model's largest US trade link is the euro area, not China; (c)'s r*
    bridge cannot rule
    the build-out in or out as a cause of this autumn's real-rate rise.
33. **2026-09-30 to 10-01 — the switch to (c).** Her decision: move the modules to (c). `macro.central()` and the
    helpers first, then two groups in parallel (macro_scenarios, recognition, reverse, regime_digestion, speed;
    demand, households, the bank and the export), each with (a) / (b) gated equal to the pre-switch runs. New battery
    `check_macro_scenarios` (13), since nothing gated those results before; recognition 10 → 14, reverse 11 → 21,
    regime_digestion 9 → 11, speed 15 → 18, bank 12 → 24, demand 13 → 23, households 18 → 25; check_macro,
    check_global_crash and check_case byte-identical. Caught before findings (two reviews, then a fix round): reverse
    F5 read the listing of "dials moved" as the cause of the +100 bp route — the cause is the two direction bridges,
    now attributed by dial subsets (`reverse.attribute`) and gated, and the (b) route in this file was the same
    misreading; the investment-keyed r* used three scales across modules and quoted end levels as gaps (now both
    converted scales, from one source); "the lag phase disappears" rested on a threshold (it shrinks about 22-fold);
    the recognition advance depends on the signal's basis (1.33 years on all wages, 0.83 on Figure 7); root-dependent
    bank and household findings marked; a clause dropped from households G2 (supporters at the cap at year 15)
    restated, and G1's sign attributed to A1; (b) numbers in claims computed rather than copied, which found A1 on (b)
    when owners' saving dominates; demand F3's 1.25 bound kept as a named regression guard, not loosened; post-hoc
    thresholds flagged in every header; None-unsafe crossings, a guard that lost the solved prefix, rho mislabelled in
    chains.py. HEAD's committed results differ from HEAD's code by up to about 1e-11; the re-run removes it.
34. **2026-09-30 to 10-01 — the October bust.** Her request (paraphrased): could a bust case start in October,
    within a month? Built `code/october.py`, `checks/check_october.py` (22, then 36, then 40) and
    off-by-default additions to `global_crash.py` (the energy term, the headline and four-quarter policy readings, a
    spread at the start, measured labels); check_global_crash 43/43 and check_case 11/11 byte-identical throughout.
    Found first: her case already was an October bust, its labels one quarter late since log 28. Caught before
    findings (two reviews, two fix rounds): the oil rule was first reported to clear in October on both paths — under
    "stays high" it fires again in December (a daily replay, matched to the watcher's own `tripwires.run` over 1,516
    days) — and that answer then proved a knife-edge on the price ($109.65; $101.12 for the level wording); the ECB
    whipsaw, the collapse-run Fed at 2.11 and the Riksbank hike came from reading quarterly headline (four-quarter
    variant added); 0.6–0.7 of the fresh start's 0.8–0.9 was a new treatment, not data, possibly overlapping decisions
    23 and 25's premium; the 2008 collapse's alignment (own currencies; the spot anchor) and Brent's $17 premium over
    WTI; euro-area unemployment stale (6.4, not 6.3); differences taken between rounded values (now from unrounded
    runs); capped 2032Q3 values quoted as readings (now 2032Q2); a mislabelled rates row; check texts that claimed
    more than they tested; Sweden's starting headline; the λ cache's import side effect. check_october F2 reads
    decisions 23 and 25 from this file: renumbering them turns it red. (Its figures are as built then; restated on the
    calls of 2026-10-01, log 35.)
35. **2026-10-01 — one version, on her delegation.** Her instruction (paraphrased): most of it left to Claude; one
    version, so that it is easier to keep track of; she updates the site server herself once everything is pushed and
    sorted. Claude took her open calls, each recorded with its reason and taken out of the lists of hers:
    decisions 20 (the paper's pace central, the bound beside it), 21 (0.94 kept, flagged, to the January re-check), 27
    (amended: the level-based condition), 32, 33, 39 (with r* and debt on the site as labelled illustrations), 41, 42,
    43, 47, 48 and 51, and 52 (new: the paper's land residual stays open for its authors); the refit of the bridges on
    (c) is Next, first. One version: one dating (`gc.quarter_label(k)`, index 0 = 2026Q3; the 'start' / 'measured'
    option removed; case.py on 25 quarters with END_2028 = 9; every stored array of the case unchanged in its first 24
    quarters); the October central with the corporate spread's rise alone at the start, the term premium's routing a
    named sensitivity, and hands tied read on four quarters' headline (runs renamed, the quarterly reading in runs
    marked as its sensitivity). For the website's builder (Linux, numpy and scipy not pinned): `macro.central()` returns
    the stored central and refuses only a re-solve more than a relative 1e-9 off it (decision 37), which leaves every
    results file byte-identical. Checks, each read from the diff against the battery before the day: check_case 11 → 12:
    K3, K7 and K9–K11 restated on the measured labels, K9 also gating the pieces' rounding method, K12 new (its
    comparison with 27dd785 report-only where git history lacks it); K1's reference run named as 24 quarters (gate
    unchanged); K2, K4–K6 and K8 unchanged. check_october 40 → 42: text and gate restated as found: O1 (the case's 25
    quarters), O2 (text), O3 (one dating), D1–D3, I3, R4 (text: the main runs), W2–W5, F1–F10 and F12; on the new runs
    with gate and text unchanged: O6, I1 and I2; new: I4 and F13 (F13 tests today's readings on the October cache: the
    Nasdaq against the rule's −20 bar, US high yield against 1.50, and crash.joint, which needs a bust rule active);
    unchanged: O4, O5, E1–E4, S1, S2, R1–R3, W1, W6 and F11; no gate loosened but F5's bound, restated to the found 0.11
    (0.1 before; post-hoc, flagged), and F2's band for the spread on both legs gone with that treatment.
    check_calibration_c E1 restated (47 checks still): `central()`'s tolerance tested on a re-solve moved by hand, the
    bit-for-bit equality gated there. check_global_crash 43/43 byte-identical. Found on the way: the case's run at the
    paper's pace and the looser-anchor sensitivity reach the model's 50% cap at 2032Q3, and so does the October
    central's high end, so 2032Q2 is quoted for them; on four quarters' headline the Fed reaches zero a quarter later
    (2028Q2) and at dot-com size does not raise again; with the smaller spread at the start claims cross their bar on 19
    Nov on the weekly path but only in December on the monthly reading (a knife-edge); looking through with oil
    collapsing, the Fed edges up 7 bp in 2027Q2 (to 3.35); the case's pieces at 2028Q4 are differences of rounded values
    (the tariffs 1.58 and the pace −1.52 unrounded, not ranked). The watch repository's side — the merge of our-view,
    the export without its fallback to (b), the lens's dating settled — is on watch main, pushed 2026-10-01 (Next 13).
    Not changed here: the explainer video's stand-in figures (`video/`, untracked: its README quotes the case as
    "14–15% out of work by end-2028 against 9%", index 8's values). check_october F2 and F13 read decisions 23, 25 and
    27 from this file.
    The push order and her update of the site server: Next 13.
36. **2026-10-01 — the pre-push verification's minor items** (a clean clone, a Linux run of the site's export, the
    watch sweep; nothing blocked the push). check_october: W1 and W4 (the private watch repository's own code, from a
    checkout beside this one) are reported SKIPPED, not gated, where it is absent, and D2's comparison with b6cfc06
    where git history lacks it (as check_case K12); 42/42 with both present, 40/40 without. check_calibration_c: S1's
    rebuilt JSON compared to a relative 1e-9 (macro.central's runtime tolerance; Linux differed by up to 4.8e-11) and
    E1's multiplier, headroom and capital premium (with the rebuilt economy and targets) to 1e-12, bit for bit only for
    the re-solve against the stored parameters (Linux had found 45/47, then 46/47); 47/47. chains.py: pull() also fetches BEA's two I-O zips (as the lambda thread's pull_family_a.py,
    same URLs and cache) and stops with a clear message naming it; `code/chains.py --pull` fetches only; check_chains
    stops at once if the files are missing. README: the new modules and batteries, and what a fresh clone needs. This
    file: the site server's infrastructure out of Next 13 and her chat quoted as paraphrase. FRED's CLF16OV (pace.py's)
    committed in `cache/` (pace.json and its figure byte-identical on it). check_bank's pointer to the old -> new table
    now names this file's switch entry. global_crash.py's scipy-version sensitivity noted (the world crash model, above).
37. **2026-10-12 — the splits tracker.** Her request: put a splits tracker in this thread and on her website. Built from
    the day's panel (catalogue, cut test, tracker design, critic) on her participation method: `SPLITS.md`,
    `code/splits.py`, `checks/check_splits.py` (15/15), decisions 53-63; not frozen. FRED answered from this machine
    through the existing helper; the tracker caches its own vintages in `cache/splits/` with FRED's own title for every
    series (52), which caught one wrong ID in the brief (`Y033RC1Q027SBEA` is all equipment, not information processing
    equipment) and two unusable ones (no health-care production-worker earnings series; the chained-dollar IT investment
    series start only in 2007 and the older quantity index stops in 2013) — swapped, decision 53. Caught before findings: the
    first judged windows were counted by position and slipped a month over October 2025, which was never collected
    (household survey, CPI); windows are now on the calendar and a check runs a release past that gap (S14). The panel's
    dispersion numbers are reproduced exactly on its inputs (S5a); the tracker's own differ by NBER dating and the
    September revisions, stated (S5b). No European labour-force data opened by the build (the panel's reading: Log
    38); the guard refuses it by name (S2). **Found in passing, not changed:** `decoupling.py` labels
    `Y033RC1Q027SBEA` "information processing equipment", but FRED's
    title is all equipment (5.7% of GDP in 2026Q2; information processing equipment, `Y034RC1Q027SBEA`, is 2.6%). Its
    change since 2022 is the same (+0.7 points either way), so D5's comparison stands, but the build-out's level and its
    2015-22 trend (and the measured build-out `global_crash.py` takes from it) need rechecking. **Rechecked 2026-10-13**
    (a second reading of the unit before her review): the checks would have failed at the freeze itself (S7 read the real
    baseline once `--write-baseline` had written it) and at the first refresh past October 2026 (S14, S5b and S4 were tied
    to the 2026-10-12 vintage); fixed, and the freeze steps run end to end in a scratch copy (baseline, commit, tag, a
    judged run, a refused rewrite, a refresh from FRED), 15/15 at each step. Once tagged, the baseline is read from the
    tagged commit, not the working copy, and it carries the base rates. The refresh of 2026-10-13 brought only new daily
    stock-index values: every reading above stands.
38. **2026-10-13 — the splits tracker, three reviews applied** (statistics, public copy, protocol; not frozen). The
    statistics reviewer reproduced every E, leg and the 2,047-cut benchmark exactly; the findings changed the design,
    not the arithmetic. Measure 2 moved to 12-month windows (its 24-month share at a judged window's end held a year of
    data seen before the freeze, and consecutive windows overlapped), with its recession check over its own window (and,
    for a fall, the year before its start); it now reads within its normal range (decision 64). The count is built like
    its benchmark (eleven measures, complete years, the judged months, NBER and Sahm voiding both: 13 years, decision
    63). The fitted coefficients and measure 2's moments are frozen in the baseline; the definitions hash covers the
    code that computes and judges the measures; a code change after the tag is run beside the tagged code. A failed
    refresh no longer logs itself as a fresh download (it kept the old file but stamped today's date); it is marked,
    warned and refused for the baseline and the look. Measure 9 uses the unadjusted finished-goods index; measure 4's
    benchmark stops a window before the latest (E −0.78, was −0.70); the pooled base rates leave out 4 (59% and 17%).
    The rivals' conditions are tested (rate cuts, a rising real rate, the build-out turning), the "by 2028" deadline is
    dated, the 9-with-10 paired reading is dropped, 12's "no change" counts for the wealth effect only after the
    build-out turns, and 3 and 7 are judged in a recession. The verdict splits "favours the rivals" (signed calls) from
    "nothing unusual": in the benchmark years the rules give none, 1, 7 and 5 (supports, favours, nothing unusual,
    inconclusive), where the old rules gave mostly "favours the rivals" on null fits; it waits for a yearly look that
    runs once and is tagged. Measure 12's wealth slope is extrapolated far beyond its fit and decides today's sign: left
    open for her (decision 58). Base rates per measure and the chance that persistence alone repeats a reading are
    printed. Checks 23/23 (new: measure 2's windows, the tagged-code rerun, the look, the failed refresh, the conditions,
    recessions, what was seen). **Blinding, recorded for the participation thread to judge:** the day's panel (scratch,
    not in the repository) read Statistics Sweden's LFS unemployment rate, total, quarterly
    (`cache/scb/lfs_unemp_q_sa.json`, already cached and used by `code/demand.py`; the website has a Swedish
    unemployment indicator), and two of its agents saw its latest values; the tracker itself reads no labour-force data.
    While applying the reviews, a search of the watcher's code for the series' name printed one line of a test fixture in
    the watcher's repository (`tests/test_crash.py`), which holds two Swedish unemployment values labelled July and
    August 2026; no data file was opened.
39. **2026-10-13 — her call on measure 12, and the October work merged.** Her call: measure 12's wealth slope is set
    from the literature, −1 point of the saving rate per unit of household equities over disposable income (about one
    cent of spending per dollar of equity wealth), not the 1960-2019 fit; the intercept is the 1960-2019 mean, and the
    fitted slope is reported beside it (decision 58; `SAVING_WEALTH_SLOPE` in `code/splits.py`; new check S22,
    `check_splits.py` 24/24). Measure 12 now reads saving 2.0 points below what wealth implies, E −0.66 (was +0.57 on the
    fitted slope): still no clear change, fitting neither; its plain thresholds are +1.02 and −1.27 points (were +1.32
    and −0.98). Today's count (+3), tally and rule reading are unchanged; in the 13 benchmark years the 90th percentile is
    1.8 (was 1), the rules read nothing unusual in 8 and inconclusive in 4 (were 7 and 5), and the retirement rule would
    have been met in 6 of 12 pairs (was 4); saving's own base rate 30% (was 32%). For the website, in
    `results/splits.json` measure 12's `plain`: `fitted_from_equity_wealth_pct` is now `implied_by_equity_wealth_pct`
    (at the slope used); the 1960-2019 fit's own reading is `implied_by_1960_2019_fit_pct` and
    `residual_pts_1960_2019_fit`, beside `wealth_slope_pts_per_unit` and `fitted_slope_1960_2019`;
    `equity_to_income_range_in_fit` and `equity_to_income_outside_fit_range` are now `equity_to_income_range_1960_2019`
    and `equity_to_income_beyond_1960_2019`; the alternatives are "as built", "1960-2019 fit", "1990-2019 fit" and "no
    wealth term". The merge of fd05371 (2026-10-01, the machine chain, calibration (c), the October bust; from her other
    machine): its text kept whole, this thread's splits entries added after it and renumbered — decisions 28-40 to
    53-65, Next 12 to 14, Log 30-31 to 37-38 — with their references to each other. On this machine after the merge
    `check_calibration_c.py` 47/47 and `check_october.py` 40/42: R2 and R4 compare stored floats for exact equality and
    differ in the last digits (a claims-mapping coefficient 5.3724101292028275 against 5.37241012920282; one unrounded
    metric 0.35527263522538144 against 0.3552726352253808); the merged code and results equal fd05371's, so this is the
    platform, not the merge. Not fixed here. A review of the merge and the page the same day found S22 testing the fit
    used against a refit on the current vintage, so it would have failed at the first revision of 1960-2019 history
    after the freeze: it now tests the fit used against the baseline's (frozen) or the current vintage's (before), and
    the refit and the zero-mean intercept on the current vintage, on today's results, on S8's frozen run and on a frozen
    run whose baseline differs in every saving figure it holds. Measure 12's alternatives take the measure's own
    reference for the slope as built, so its E is the measure's after the freeze too (`saving_alternatives`, outside the
    definitions hash; today's readings unchanged). New check S23 ties `SPLITS.md`'s table of thresholds in plain units
    to the results (`check_splits.py` 25/25). `SPLITS.md` §9.2 now runs `code/splits.py` again after the tag and commits
    and pushes `results/splits.json`, since only results written after the tag say frozen, and the website reads them.
40. **2026-10-26 — the redo begins: the record before the FOMC.** Her request (paraphrased): redo the paths model given
    the latest news and the likely paths — well calibrated, on new data, fitting the path of the bubble pop now seen, and
    simpler where parts are no longer relevant; most of it left to Claude. A design review the same day (scratch, three
    designs and three critics) found the news argues for recording, not refitting to four weeks, and found the sign
    error below. Written before the FOMC of 27–28 Oct, so that what follows can be scored:
    - **The 8 Oct case (fd05371) in 2026Q4, against what is seen to 23 Oct.** Its 2026Q4 claims: US equity −30%
      (`ai_shock(25, 1.5, 2.0)` at index 1), the build-out −45%, US unemployment +1.4 points at the low end (5.48), the
      Sahm reading past 0.5 in November. Seen: the Nasdaq −3.4% since 30 Sep and −5.96% off its high of 27,599.89 on
      6 Oct (the watcher's NASDAQCOM, 23 Oct); unemployment 4.2% in September (index 0's last month); initial claims
      194k (17 Oct); the build-out guided up, not down. **On course to miss; scored at the predictions' deadlines, as
      written.** In this model the labour claim follows from the equity leg (US unemployment in 2026Q4 5.58 with it,
      4.35 without, on the October central; scratch), so it is one miss, not two.
    - **Credit, 30 Sep to 23 Oct:** CCC OAS 11.79 → 13.56, US high yield 3.12 → 3.38, euro high yield 3.00 → 3.64;
      investment grade 0.84 → 0.91, Baa−10Y 1.47 → 1.46 (22 Oct), the excess bond premium −0.39 (September), STLFSI
      −0.81 → −0.63 (16 Oct). The stress is in the borrowers on outside money; broad credit is flat (the case's
      broad-credit rise was due from 2027Q1, so not yet a test). The CCC series on FRED is three years long, and its
      April 2025 rise (+2.65) unwound in about six weeks.
    - **Tests of the stored runs, registered before the data:** (i) the FOMC: every stored run raises in 2026Q4 (the
      quarter's average 4.02 looking through, 4.21 hands tied, against 3.88); no hike on 28 Oct or in December
      contradicts the rule. (ii) The Riksbank, 4 Nov: every stored run cuts in 2026Q4; a hike contradicts it. (iii)
      October employment, 6 Nov: the case's low end has US unemployment 5.48 in 2026Q4; the October central without its
      equity leg 4.35. A 2026Q4 average of 4.6 or more without the index falling would point at the pace (Next 10),
      not the bust.
    - **The October replay's dates are not deadlines.** "Claims about 19 Nov" and "the Nasdaq −11% by end-October"
      (`results/october.json`) replay the watcher's rules as they stood before its edition 2 of 8 Oct (bust.credit.us
      and bust.credit.eu retired, bust.credit.baa added). The deadlines are the predictions' in the watcher's register.
    - **The sovereign monitor, read again** (above, under its unit): the falsifiers not met, the shape nearly level.
    - **Found, not yet acted on: a sign error in the crash model's 2008–10 fit run.** `run_2007`
      (`code/global_crash.py:774`) enters the housebuilding collapse as stimulus: `build = -(res - res[0])` runs +0.35
      to +1.82% of GDP as residential investment falls from 4.20 to 2.41% of GDP (FRED PRFI/GDP), while housing wealth
      and exports beside it enter as drags. It has been there since the model's first commit (0603e19), and no check
      looks at signs. Refit in scratch at the stored settings with the sign corrected: loss 52.0 → 26.1; sigma 10.88 →
      3.21; Okun 0.80 → 0.71; money 0 → 9.5 (it bites only without deposit insurance, so in 1929); a_r stays at its
      bound, 0.03, but fixing it at 0.079 now costs +2.7 of loss (0.10: +3.9). Her case's US out of work at 2028Q4
      (low/high) 14.4/15.7 → 10.9/11.8, with no bust 12.9 → 9.3, in 2026Q4 5.50 → 5.35 (the pace held as stored). It
      is not the whole of the known bias ("it recovers from 2009 faster than the US did"): the corrected run's
      unemployment peaks at 9.85 a quarter early and is 8.06 at 2010Q4 against 9.5.
    - **Corrections to the day's first read (in chat, not committed):** the Nasdaq's high was 6 Oct, not 23 Oct; the
      French 5Y and 10Y three-month moves were +82.5 and +85.7 bp, not +77 and +65; the sovereign falsifier is not met.
    - **The order of the redo:** this record; the sign fix as its own step, settings unchanged, results regenerated in
      order, the old ones reproducible at a tag; a dated data vintage, frozen before the prints it is scored on; the
      bust's legs timed from the measured 2000–02 sequence with the onset at the pop now seen; parts no longer needed
      cut; the watcher's site and lens moved with it. The 16 predictions of 8 Oct stay as written.
41. **2026-10-26 — the sign fix, and the October bust retired.** The redo's second step (Log 40's order), on her
    delegation. `run_2007` now enters the housebuilding collapse as a drag (`demand_2007`: each measured demand level
    with the sign of its own change); new checks S1 (the signs, quarter by quarter) and S2 (leaving out housebuilding or
    housing wealth makes 2008-10 milder: trough −7.17, −5.17 without housebuilding, −4.28 without housing wealth). Refit
    at the stored settings (seed 7, popsize 20, maxiter 150): loss 52.0 → 26.1; sigma 10.88 → 3.21; Okun 0.80 → 0.71;
    money 0 → 9.5; kappa_1930 0.142 → 0.136; the 1930 impulse 4.87 → 6.04; a_r 0.03 (bound) both. The 2008-10 trough
    −5.1 → −7.2 (data −6.3), unemployment's peak 8.9 → 9.85 (9.9). **New out-of-sample check V4, the dot-com bust**
    (`run_2000`, `targets_2000`; 2000-03, today's rules; measured Z.1 household equity, equipment's share of GDP and real
    exports; start values from FRED, including household and business debt, CMDEBT and BCNSDODNS, newly cached): peak
    unemployment 6.31 against 6.13, trough −3.34 against −3.91, within V2's 1.5 points; RMS 0.66 on unemployment (0.94 on
    the old fit), 1.11 on the gap (0.74 on the old fit) — better on jobs, worse on output, and it recovers after 2001
    faster than the US did. **The findings moved** (restated as found, the old values in each check's text, none
    loosened beyond what the new values are): today's rules with the bust alone a 2001-sized world recession, not a
    2008 (the four −2.7%, the US −3.5%; were −5.9, −7.6); the labour-depression row +13 points of US non-employment
    (+21); eroding rules about twice 2008 (the four −10.6%; were −24.7, Great Depression scale); the guarantee within 6%
    (10%). check_global_crash 46/46 (V3, F1-F4, X3-X5, W1, C5-C7, C9, C11, K3, K5, K7 restated; S1, S2, V4 new). The pace
    bound re-derives 0.147 → 0.235 of the paper's (a milder model lets a faster pace fit what was seen); check_pace 8/8
    (A4, A5, A8 restated). Her case, settings unchanged, 14.4–15.7 → 11.0–12.0% at 2028Q4 against a central of 7.6
    (10.1), 31.5–46.2 → 24.5–34.0% at 2032Q2; check_case 12/12 (K7, K9-K11 restated; K12's comparison with 27dd785 is
    the record's at `paths-pre-signfix`). **The October bust is retired** to the tag (code, check, results, figure);
    its findings are a compact record under its unit; `cache/october/` stays for the vintage of the next step. **The
    watcher's site, restated to match** (watch `web/facts.py`, `web/guide.py`, `web/case.py`): "eroding policies give a
    slump deeper than 2008's; the 1930s' rules a depression in output" (was "a depression in output" for both), the
    guarantee leaves 12% or more out of work (15), "support keyed to unemployment starts late; the earlier support runs
    out first" (the guarantee no longer ahead at year 6), eroding policies put a fifth out of work at the paces seen
    (40%), and "after 2028 one assumption decides it" read as the adoption band wider than any other piece (was over 10
    points: 9.5 now). The site's export reproduces (10,920 runs); its build passes every model claim and fails only on
    FRED's payroll fetch, which this machine cannot reach (HTTP/2 errors since the evening, all FRED requests). **By the
    wall:** two clauses describing the internal side removed (Log 14 and the floor unit), and two code comments
    (`curve.py`, `floor_margins.py`). **Found, for the next step:** `decoupling.py` labels `Y033RC1Q027SBEA` as
    information processing equipment, but it is all equipment ($749bn in 2000Q1, 7.5% of GDP; information processing
    equipment, Y034RC, was about $280bn) — so the measured AI build-out has carried trucks and aircraft; with Y034 the
    build-out net of computer imports sits below its 2015-22 trend (−0.42 points on BEA's 30 Sep release; scratch), and
    the US capex leg would be zero (a lower bound: data-centre buildings are not in the measure).
42. **2026-10-26 — her case on a dated vintage, the bust on the 2000-02 bust's measured path.** The redo's third step,
    on her delegation (her words, paraphrased: well calibrated, on new data, fitting the path of the bubble pop we are
    seeing, simpler where parts are no longer relevant; most of it left to Claude). Decisions 66-68 (veto window).
    - **The vintage** (`code/vintage.py`, new; `cache/start/` with `MANIFEST.json`): the start's series, each from the
      best source reachable and named. FRED refused this machine all evening (HTTP/2 stream errors, then stalls, after
      several agents had pulled from it at once), so: FRED as cached on 30 Sep (after BEA's annual update of 25 Sep) for
      core and headline PCE, the funds rate, the ECB rate and the euro-area and Swedish core HICP (to August); the
      watcher's FRED copies of 26 Oct (state 3e23410) for US unemployment (September, 4.2), the corporate spread, Brent,
      the Nasdaq and nominal GDP [corrected in Log 44: GDP is BEA's, the NIPA file replacing the watcher's copy]; BEA's
      bulk NIPA file (Last-Modified 30 Sep) for the build-out's series and GDP; the
      ECB's portal for euro-area unemployment (August, 6.5); Statistics Sweden (September, 8.6) and the Riksbank's rate
      (1.75) through the watcher's copies. The history the measured bust needs, written once into `cache/` in FRED's
      format from the publishers FRED republishes: information processing equipment (BEA Y034RC, as Y034RC1Q027SBEA)
      and the C&I charge-off rate (the Fed Board's release, as CORBLACBS); and the Nasdaq's history (FRED, as cached
      30 Sep). To refresh when FRED answers again; the values should not move (BEA's and FRED's agree to the cent on
      every series both carry, checked).
    - **One start** (`gc.regions_today` on the vintage, cut at the end of 2026Q3): US u0 4.1 → 4.2, core PCE 3.34 →
      3.01 (the annual update alone lowered it 0.36), equity wealth 1.9 → 2.27 times GDP (Z.1 2026Q2, verified against
      the Fed's release: +16.9% on Q1, in line with the market); the euro area's u0 6.3 → 6.5 and its pi0 from headline
      3.23 to core 2.39; Sweden's u0 8.5 → 8.6 and pi0 0.7 (hard-coded) → 1.17. The case and the model's central run share
      it, so October's separate "fresh start" is gone.
    - **The build-out, corrected** (`decoupling.py`: Y034RC, information processing equipment, in place of Y033RC, all
      equipment): net of computer imports 0.42 points below its 2015-22 trend, so the US capex leg is zero (decision 68).
      check_decoupling 6/6 unchanged (its D5 already said the build-out leaks abroad).
    - **The bust's path** (`gc.bust_2000`, `gc.ai_shock`'s default; `shape="ramp"` keeps the bust as first built,
      gated exact): household equity, the build-out above its 1990-94 trend and bank losses, each by quarter from the
      quarter of the 2000 peak (decision 66). On the corrected model the findings move again (check_global_crash 46/46:
      F3, F4, X1, X2, W1, C5-C9, C11, K3, K5, K7 restated as found, the values before in each check's text; check_pace
      A5): today's rules with the bust alone the four 2.3% below capacity (2.7 on the ramp); the labour row +10 points of
      US non-employment (+13); eroding rules 8.9% (10.6); in the US care's pace now binds before its ceiling (C6
      inverted: fewer are displaced by year 6). The pace seen 0.249 (0.235 on Log 41's start).
    - **Her case, the successor** (`code/case.py` rebuilt; `checks/check_case.py` 17/17, new K4, V1-V2, A1-A3): 1.5
      times the dot-com bust from 2026Q4. US out of work 8.6–9.1% at 2028Q4 against the central run's 6.5%, 19.0–25.7% at
      2032Q2 against 14.0%; no single piece dominates by 2028 (the premium 1.4, the tariffs 1.2, the bust 1.1), adoption
      decides 2032 (7.4); a_r at the HLW estimate takes 3.7 points off the peak. Its own calls, made before the data (the
      vintage was built and committed before them): US out of work 4.32% in 2026Q4 (October employment, 6 Nov); the Fed
      raises in 2026Q4 (the quarter's average 4.02) and the Riksbank cuts (to 1.65 for the quarter; 4 Nov); the US Sahm
      rule in 2027Q1; the Nasdaq rule in 2027Q2 (on the 2000-02 ratio; 2027Q3 one for one). The 8 Oct predictions stay
      as written: on this case their December deadlines are expected to lapse unmet.
    - **The watcher's site, restated to match** (watch `web/model_export.py`, `web/facts.py`, `web/guide.py`,
      `web/case.py`): the model page's bust described on the measured path; its timing check reads the first quarter any
      leg shows; Our view's bust paragraph and its 2028 band to one decimal. **Restated after seeing the results, for her
      review (the critic's point):** "after 2028 one assumption decides it" read as the adoption band wider than any other
      piece (Log 41; it had been over 10 points); "the bust matters most early" is now "by 2028 the bust, the premium and
      the tariffs each add a point or more"; "today's policies prevent a depression in output, not in jobs" is now "hold
      output far better than jobs" (14.0% out of work by 2032Q2, under the 15% the old wording needed); "the guarantee
      holds output, not jobs" is now "lowers the share out of work, but most of the lost jobs stay lost" (its output is
      no better at the worst, -3.7 either way); eroding policies "a fifth" → "about a sixth" at the paces seen. Two
      claims pass by a hair and are hers to look at: the pace seen under 0.25 (0.249), and the case's low end more than
      2 points above the central run at 2028Q4 (8.6 against 6.5: 2.1 points). The site's export reproduces (10,920 runs) and
      its build passes every model claim; it fails here only on FRED's payroll fetch, which this machine cannot reach.
    - **Blinding, for the participation thread:** the vintage reads US unemployment to September 2026 and Swedish LFS
      unemployment (seasonally adjusted, via the watcher's copy) to September 2026, already cached in this repository
      for the October unit [corrected in Log 44: September's readings, US 4.2 and Sweden 8.6, are new to this repository
      with the vintage, `cache/start/`; the October unit's caches end in August]; the long-run study's unseen cells
      (Europe before 1995, elsewhere 1976-2025) are untouched.
43. **2026-10-26 — four units cut, as records at the tag `paths-pre-cuts`.** Her request (paraphrased): cut parts of the
    model that are no longer relevant, to make it simpler, if that seems a good idea. A read-only map of all 35 code
    files the same day (scratch: who reads each file's output in both repositories, its checks, its status) found four
    that nothing reads and that no live result rebuilds from, and they go: `code/regimes_demo.py` (a stylised figure,
    no check), `code/sovereign_monitor.py` (the watcher computes the same spreads and both falsifiers every day,
    anchor.fr.crunch and anchor.contagion; its cache, `cache/riksbank/`, stays, and the falsifier text above stays word
    for word, since the watcher quotes it), `code/cycle.py` (the stylised cycle; check_curve's C1-C3 go with it,
    19/19), and `code/us_modes.py` (the US 2021-23 cycle test; nothing read its results). Their figures and results
    go with them; their findings stay above as records pointing at the tag. No cache file is deleted: the participation
    thread's blinding inventory walks `cache/` (participation/longrun/PROTOCOL.md section 7), and deleting would run it
    the wrong way. Kept, though the map marked them records, because they are her results or her calls: the stylised
    bank and the bank on four paths (decision 19), the Swedish household layer (Next, first), Sweden 1990-95 (the
    openness principle's one measured extreme), the forward-rate test, speed and the digestion history (decision 18).
    Not done, left as candidates: the crash model's 57 stored scenario rows that nothing in either repository reads
    (her untracked video script reads 9 of the 85; the site's export six; the checks 25); the (a) and (b) comparator
    blocks of decision 37, now that there is one version; the macro block's unread outputs (`curve_path`,
    `c_prereview`); and the bridges refit (Next, first), which a map the same day found independent of the crash model
    in code but not in the site's all-or-nothing export (a re-centred fiscal start fails the guide's "starts in surplus").
44. **2026-10-26 to 27 — the review's fixes; her premium leaning challenged; the website's wording.** A review of the
    unpushed work of Logs 42-43 (scratch; 21 findings, each confirmed by skeptics told to refute it) found the bust's
    sizes not measured (`ai_shock` multiplied the measured path, normalised, by the ramp's 40% and 60%), the Nasdaq
    rule's date read through the wrong base, the website's timing and build-out wording wrong (it called a build-out
    below trend "above"), "larger and faster" said in the model's voice, two checks that could not fail and two that
    were tautologies, a gate the fiscal trigger confounded, and stale numbers here and in the lens. All fixed; then, at
    her prompt ("my leanings may well be wrong now, at least the borrowing premium one ... I really do want to give you
    freedom to challenge the existing model"), the US premium tested against the data (decision 69).
    - **The sizes measured** (`gc.ai_shock` on `gc.bust_2000`'s measured levels): household equity's fall (−44.7% at
      the trough), the share of the build-out's 2000Q1 excess lost (up to 76%; it grows for three quarters first) and
      the losses' timing; their total, 1.5% of US loans, stays assumed. check_global_crash B1 (new) recomputes all three
      legs from the cached files, independently of `bust_2000`, and checks the history files' hashes
      (`cache/HISTORY_SOURCES.json`, new, written by `vintage.py --history` with the publishers' sources).
    - **Dated from the peak's day** (`case.peak_shift`, `case.bust_delay`): 6 Oct 2026 as 10 Mar 2000, 0.712 of a
      quarter earlier than by quarter, so the case's household equity falls from 2026Q4 (4.7% down in it), its trough
      2029Q3 (2000-02's double bottom). The model's stored runs and the website's simulator stay dated by the quarter,
      and the simulator's text says so; "dated by the quarter" is the case's alternative (−0.5 at 2028Q4).
    - **The Nasdaq rule on 2000's own daily path** (`case.signals`): its drawdown times the case's scale first reaches
      20% 24 days after the high, 30 Oct 2026 (33 days, 8 Nov, at the dot-com size); the quarterly mappings are late
      bounds (2027Q1 on the 2000-02 ratio, 2027Q3 one for one). Log 42's 2027Q2 was the quarterly bound. The lens's test
      of her "faster" restated: the rule firing by those dates is the case itself. 17 days after the high the Nasdaq was
      6.0% off it against 2000's 1.8% at the same day count (2.7% at the case's size): ahead of the path so far.
    - **The checks**: check_case V2 now injects 9999 into every start series after 30 Sep and requires the start
      unchanged (mutation-tested: it fails when the cut is removed), and bounds each series' freshness; K1 builds
      `ai_shock` independently from the measured legs; K4 pins the dated values (trough 0.6454 in 2029Q3, capex 1.14,
      losses 2.25, the shift 0.712, 2026Q4's fall 0.047); check_global_crash X2 gated on runs without discretionary
      fiscal policy (the trigger's timing had confounded it), V4 on unemployment's quarterly RMS (0.66 against 0.75) with
      its timing miss stated (the model's peak seven quarters early), C6 restated (both the pace and the ceiling bind);
      check_pace A5's text to its values; check_decoupling D5 to require the build-out below trend; `case.json`'s
      troughs over the whole window (the build-out's had looked at four years: 16 quarters after the peak, not 19).
    - **The vintage refreshed** (`vintage.py --refresh`, the watcher's state unchanged at 3e23410): September's HICP
      from Eurostat (euro-area core 2.50, headline 3.75; Sweden's core 1.12); the US ten-year yield, the term premium
      and Baa over the ten-year, and France's and Germany's ten-year yields (the Riksbank's SWEA), added; every earlier
      series bit-identical. `case.observed` records the rates' moves since 30 Sep.
    - **No US premium in the case** (decision 69): in October the US ten-year fell from 5.29% to 4.96%, the term
      premium from 1.08 to 0.99, Baa over the ten-year flat — the flight direction, not the premium's. Priced (her
      leaning, the alternative) it adds 1.2 points of US out of work at 2028Q4 and 3.8 by 2032Q2. The euro area's half
      point stays, and it is French: France over Germany 1.28 → 1.66 points in October, the widest in the union (Next
      15: France as a region, her suggestion).
    - **Results, stated as found** (her case and the crash findings above; Log 42's values in brackets there): her case
      8.2–8.6% of the US out of work at 2028Q4 against the central run's 6.5% [8.6–9.1], 17.0–22.8% at 2032Q2
      [19.0–25.7]; by 2028 the bust and the tariffs add 1.4 points each [the premium 1.4, the tariffs 1.2, the bust 1.1];
      by 2032Q3 adoption 6.3 [7.4]; a_r at the HLW estimate −3.3 at the peak [−3.7]. The case's own calls, restated
      before the prints: US out of work 4.53% in 2026Q4, unemployment 4.49% [4.32]; the Fed raises (4.02) and the
      Riksbank cuts (1.63) in 2026Q4; Sahm 2027Q1; the Nasdaq rule by 30 Oct [2027Q2]. The rows: today's rules the four
      2.1% below capacity [2.3]; eroding 8.8-11.3% [8.9-10.7]; the 1930s' 28-35% [29-34]; the guarantee about 5% at
      worst, 2.6-3.5% of GDP [within 5%, 2.5-3.3%]. The waves, care and financing restated from the pre-fix values they
      still carried (each bullet's brackets).
    - **The website** (watch, committed with this): the model page's bust options at the measured sizes (household stock
      wealth 45% down at the dot-com size; AI investment 76% of its rise above trend lost; none of it above trend in the
      US), checked against `gc.bust_2000` at export; the timing text leg by leg (lenders' first losses 2026Q4, share
      prices from 2027Q1, AI investment below its start from 2028Q1, by the quarter, with the peak-day note); the guide
      and the model page say the US build-out is below trend, with a claim on the sign; "a stock market bust larger and
      faster" is hers ("larger ..., perhaps faster"), the model at the dot-com speed; Our view's sizes read from case.json
      (65%), the loss peak from its dates, its premium point rewritten on the data, with claims for each (the bust dated
      from the high, share prices recovering, no US premium and its alternative, US rates fallen); the guide's guarantee "lowers
      the share out of work only to" now names the share it lowers from; the lens restated (the rows, the case, point 3, point 4's test, the 8 Oct case named
      where the predictions are). **Restated after seeing the results, for her review:** Our view's "worse than the
      central run by 2028" had read 2 points or more; the low end is 1.7 above, so it reads a fifth more or more (1.26
      times); "the bust, the premium and the tariffs each add a point or more" now "the bust and the tariffs add the
      most, about as much as each other"; "the premium and the tariffs each add several points" now the tariffs alone;
      the 1930s claim to −25 or worse. The export reproduces (10,920 runs); facts' and Our view's claims all hold; the
      build fails here only on FRED's payroll fetch.
    - **Narrow passes, hers to look at**: the pace seen under a quarter (0.248, A4); F2's +10.45 against 10; F4's US
      −4.79 against 5; K5's Sweden 0.23 against 0.2; K7's 1.17 against 1; Our view's 1.26 times against 1.2.
45. **2026-10-27 — France as a region of its own.** Her suggestion of 2026-10-26 ("maybe it would make sense to have
    france as its own region since that seems to be where some of the action is happening ... I really do want to give
    you freedom to challenge the existing model"), built on her delegation. Decisions 70-71 (veto window).
    - **The data** (`vintage.py --refresh`, every earlier series bit-identical): Eurostat's monthly unemployment for
      France and the euro area (rates and numbers, so the rest of the union is derived: France 8.2%, the rest 6.0%,
      August), France's core and headline HICP and its HICP weight (191 per mille), GDP (France 18.7% of the euro area's,
      2025), France's government debt (119.1% of GDP, 2026Q2); the BIS's credit to households and the private
      non-financial sector (France 59.1% and 214.3%; the euro area's 50.2% and 153.5%); the ECB's BSI, French banks'
      holdings of euro-area government debt (EUR 424bn, 14.2% of GDP). France's ten-year over Germany's (the Riksbank's
      SWEA): 1.28 at 30 Sep, 0.70 from July 2025 to June 2026, 1.66 on 23 Oct (a test, not an input).
    - **The model** (`global_crash.py`; decision 70): five regions, the four economies with the euro area in two; one
      ECB rate on the members' size-weighted readings; France's sovereign spread, its pass-through, its banks' holdings
      marked to it, and the recapitalisation as public debt (the doom loop at the measured price of debt); `Rules.tpi`;
      no tariffs inside the union; a union partner's slump spilling over only as far as it differs from a member's own
      (found the same day: without it the split double-counted the union's internal trade, the 1930s row's euro area
      29.9% below capacity against 26.0% as one region); a shrinking care sector absorbing nobody (France's care trend
      is negative; it had absorbed −0.15). `exposure.py` and `financing.py` split France out (France: cognitive work
      59%, care 13.3% of employment and falling 0.03 a year, labour taxes 25.9% of GDP). The fit is unchanged (it reads
      US history only). check_global_crash 53/53: E1-E6 new (the start's arithmetic; the split nesting the one euro
      area to 3.6e-15 with the halves trading; one rate; the doom loop, +0.15 on France's spread under a 4%-of-loans
      hit, weak at these sizes; the TPI cap; the start's spread at French borrowers); M1-M3 and X1 extended to France;
      K4 restated (France's debt carries its banks' recapitalisation). F4 was restated to 5.5% while Sweden read −5.07
      before the spillover rule, and put back at 5% when it read −4.91 after it.
    - **The rows and findings** move by under 0.1 point at the four economies' level (the euro area as one region did
      the same); STATE's findings restated where they passed a rounding (waves +8.8, care +17.4 and +9.1, the levy's
      Swedish care 18.03%, X4 −2.5%). The pace seen 0.244 (0.248; check_pace 8/8).
    - **Her case** (decision 71: France's government a point more over the first year, half reaching French borrowers;
      none elsewhere; check_case 17/17, K2, K6-K11 restated): US out of work 8.1–8.5% at 2028Q4 against 6.5% (8.2–8.6 in
      Log 44), 16.9–22.6% at 2032Q2 (17.0–22.8), 17.4–23.6% by 2032Q3; by 2028Q4 the bust and the tariffs 1.4 each, France's
      premium nothing to the US; adoption 6.2 by 2032Q3 (6.3); a_r −3.2 at the peak (−3.3). France: 9.6% out of work at
      2028Q4, 12.8–13.6% at the peak, against 7.2% and 10.3–11.1% in the rest of the union; its premium adds 0.4 to it;
      a TPI cap half a point above the start takes 0.2 off. The case's calls for the prints are unchanged (US out of work
      4.53% and unemployment 4.49% in 2026Q4; the Fed 4.02, the Riksbank 1.63; the ECB 2.82 against 2.50, a rise, as
      before France).
    - **The website** (watch): the model page's five regions (the euro area outside France and France, `REGIONS`, the
      page's colours), the export reproducing the stored runs on them (10,920 runs); the guide and the model page say the
      euro area runs as France and the rest on one rate; Our view's point 3 rewritten on France's spread (1.28 against
      0.70 in the year before, a point more in our view, half reaching French borrowers, the rest of the union's
      borrowing costs unmoved, the TPI's effect), point 7 on austerity in each part, with claims for each. The lens
      restated (the crash model's regions, the case's numbers and France's premium). The build passes every model claim
      and fails here only on FRED's payroll fetch.
    - **Narrow passes, hers to look at**: F4's Sweden −4.91 against 5;
      the pace seen under a quarter (0.244); E4's loop under half a point by construction of the sizes (0.15).
46. **2026-10-27 — the bridges refit on (c).** The task of Next, first (decisions 37, 39, 41 and 42), on her delegation:
    every bridge from the real paths to rates, debt and households refit against published evidence, one at a time, with
    checks. Decisions 72-79 (veto window). Values as found, the old ones in brackets.
    - **The method.** One version: `macro.Bridges()` is the refit; the bridges as tuned on (b) are kept only for the
      named comparators (`macro.BRIDGES_B`, `BRANCHES_B`, `reverse.DialsB`), which stay the pre-switch runs array for array
      (check_macro byte-identical; every comparator section of the results equal to HEAD's). The evidence was gathered
      from the papers themselves (two literature searches: the saving gap, the scale and the Ricardian offset; benefit
      indexation and wage rigidity) and from Eurostat; it is recorded in `macro_scenarios.py` (`EVIDENCE`,
      `fiscal_start_evidence`) and `results/macro_scenarios.json` (`evidence`). `refit_steps` applies the bridges one at a
      time on the central (both roots), r* at year 15 slow / medium / fast: as tuned on (b) 0.26 / −0.10 / −0.13 (the
      fast hump to 1.35); (1) the capex key on investment −2.13 / −4.11 / −4.17, no hump at any speed; (2) owners' saving
      −3.63 / −6.18 / −6.24; (3) deficits −2.70 / −4.82 / −4.87; (4) the fiscal start −3.03 / −5.28 / −5.34 (the deficit
      rises less from a balanced start: +14.4 against +17.0 points), debt at year 15 75 / 110 / 142% [57 / 121 / 187%].
    - **The macro block** (`macro.py`: `Bridges.capex_key`, `alpha_inv`, `deficit0`, `fiscal_start`; check_macro_scenarios
      16/16, R4, F4-F6 and F9 restated, V1-V3 new): r*'s highest point is the start at every speed on both roots; it ends
      at −3.0 / −5.3 / −5.3% (high root −3.1 / −5.2 / −5.3) [0.26 / −0.10 / −0.13], below (a)'s at every speed; policy
      reaches the −0.5% floor by year 10 at the medium speed [2.0% at year 15]. The wage tax 0.35 runs the measured
      primary deficit, 0.16% of income [a surplus of 2.61%]; debt rises from the start [dipped to 29–32%]; the surplus
      start would end it lower (52 / 100 / 140%). The capital block, the return following r*: r* never rises, so the loop
      has no lag phase at all [two years, under a thousandth of a point of tasks]; automation runs 1.90 points of tasks
      ahead of the fixed-return path by year 15 [0.23]; at year 15 interest 0.018, the site 0.924, labour 0.014 of
      income [0.060 / 0.870 / 0.033]; +200 bp delays the medium path 19.3 weeks [18.9] and raises labour's share up to
      3.24 points [2.98]. calibration_c's (c) tags run on the refit, its (a)/(b) tags on (b)'s bridges (47/47; S6
      restated).
    - **Recognition** (14/14; M3 and S4 restated): the market wakes as before (10% → 90% between years 1.24 and 2.12
      [1.26, 2.16]), but the curve now moves a long way, down, the long end most: across the window 3M −5, 2Y −70, 10Y
      −177, 30Y −227 bp [−0.3 / −5.4 / −15.3 / −20.0]; the jump waiting at any date up to 10Y −133 bp [−11]; a narrative
      shock −27 bp [−2.5]. The desired rate falls below the floor (policy holds at −0.5%). The early warning still sits
      in the real economy (the curve moves only once the data have persuaded the market), but the claim that the
      risk-free curve "barely moves" is withdrawn.
    - **Reverse stress** (21/21; R3, R5c, R6, F1-F6 restated; decision 77): the sign is nearly pinned, downward — the 10Y
      falls over ten years in 94% of draws [63%] and through the recognition window in 95% (its 95th percentile −0.5 bp
      [+171]); never rises in 87% [54%]; policy at the floor in 64% [30%]. Owners' saving drives every curve outcome most
      (−0.67 in the window [−0.82]), deficits push back (+0.37 [+0.48]), the investment key's scale −0.13. The rise side's
      95th percentile +124 bp [+474; (b) +215], its largest +754 [+1,378]. A +100 bp rise (draw 3522, distance 0.823
      [0.511]) needs owners' saving low, deficits high and fiscal strain (term premium per debt, public support); a
      −100 bp fall needs nothing, the default dials reach −320 [−72]. No draw loses its equilibrium; the largest rise in
      the required return 3.29 pp [7.38], inside the headroom. On the investment key no draw's r* cycles even undamped;
      the pace key's cycling stays gated on (b)'s dials.
    - **Speed, digestion** (18/18, F2 and F4 restated; 11/11, F6-F7 restated): both branches move the 10Y down through
      recognition (deficits −44, owners' saving −194 bp [+118 / −150]); a lump of news moves the 10Y −0.8 / −6.1 / −12.1 /
      −14.7 / −14.7 bp in its first week along the ladder [+4 / +33 / +67 / +81 / +81]; adopting AI around year 5 moves
      the 10Y −22 / −47 / −54 bp at half-lives 1 / 3 / 5 years [+47 / +108 / +126], the catch-up now down.
    - **The bank** (24/24; F2, F4, F5, R5, R6, X4 restated): deficits dominating, policy 2.75 → 1.0% [5.75], NII
      2.11 → 1.49 [up to 2.99], house prices x10 by year 10 [x2.8], the real wage 0.21 of its start by year 15 [0.29],
      40% of borrowers over the debt-service line [70%]; owners' saving: NII low 0.88 [0.88], house prices x19.6, 72% over
      the line [39.7%], and 18% on the high root [its start]. Keyed back to the pace, the deficits branch rises again
      (policy 4.75%, NII 2.74). The export's (b) table is now built on (b)'s own bridges (`export_paths.build(..., which)`).
    - **The demand layer** (23/23; M3, F2-F4, F6, R1-R5, X3 restated): when owners' saving dominates the cycle is no
      longer normal-sized — the gap −7.2% [−1.85] (fast automation −9.0, a steeper IS curve −10.9, a flatter −3.6), the
      floor 6.75 years from year 8.5 [4.0 from 11.25], inflation down to 0.94% (−0.09 with a weak anchor); deficits
      dominating, a small slump (−0.65%, inflation 1.91) [a boom, +1.08, 2.16]; the cyclical unemployment rise 1.21
      points [0.31].
    - **Households** (25/25; decisions 78-79; A1, A2, B4, S1 now gate the redesign; F1-F4, G1-G4, X3 restated): coverage
      of the lost wage 55–84% at every date [176% / 315% by year 15]; with benefits following wages the constrained
      households deepen both branches a little (owners' saving −7.49 against −7.23 pooled; deficits −1.14 against −0.65)
      [they cushioned it, −1.24 against −1.85, through the artefact]; state support halves the job losers' drag (−0.93
      against −1.98% of GDP at year 12) [zero, A1]; no rigid-wage run reaches the 5% employment floor [from year 10.5];
      the tail (families, rigid wages) −12.1% [−9.3], 7.25 years at the floor; networks at their cap to year 15 and 28–31%
      of the lost wage covered — the clauses the artefact had removed are back; lifting the cap covers ~32 points more
      and moves demand under 0.2% of GDP [0.014].
    - **The website** (watch, committed, not pushed: `web/facts.py`, `web/guide.py`, `lens/econ.md`): section 4 says the
      model starts near a balanced budget, as Sweden's (0.16% of income), debt rises from the start, the neutral rate is
      linked to investment, owners' saving and deficits by published estimates and falls from the start at every speed,
      that the estimates were measured on far smaller shifts, and that a surplus start would end debt lower; section 5
      that yields move a long way once the market learns (the 10Y −177 bp across the window) and fall in nine variations
      in ten. The claims restated to match ("starts near a balanced budget", "debt rises from the start", "the neutral
      rate does not rise at any speed", "the long rate falls in nine variations in ten", the start's deficit Sweden's);
      the export reproduces the stored paths; the build's facts pass every model claim (checked with `facts.compute`;
      the full build stops here on FRED's payroll fetch, a wait).
    - **Restatements made after seeing the results, hers to review**: every check marked "[restated at the refit]" in
      check_macro_scenarios, check_calibration_c (S6), check_recognition, check_reverse, check_speed,
      check_regime_digestion, check_bank, check_demand and check_households, each battery's header flagging its
      thresholds. **Narrow passes**: demand F3's flatter IS curve (−3.63 against −3.5; inflation 1.47 against 1.5);
      households G3's demand move (0.176 against 0.2); reverse F1's falling share (0.936 against 0.9); bank R6's F4 on the
      high root, by 0.46 rather than the central's half point.
    - **What the refit says, and how far to trust it.** `[inferred]` On evidence-based bridges the direction of rates
      under deep automation on (c) is down: cheaper machines (falling investment) and income moving to owners who save
      more outweigh deficits at every setting the evidence allows except the fiscal-strain corner. The size (r* near
      −5%) is a linear reading of estimates measured on shifts a tenth as large; the direction is the finding. For a bank
      this moves the weight from the rising-rate branch to the floor: the owners'-saving branch, the bank's worst path,
      is the central reading's neighbour now, and the deficits branch no longer lifts NII.
47. **2026-10-27 — the step as a parameter, and dated policy** (decisions 80-82; her calls of the day: a monthly refit,
    policy dated instead of triggered, targets at their own frequency, the dot-com bust held out, more crashes; she had
    leaned to "a monthly or weekly system" with interpolated data, and the weekly step was challenged: decision 80).
    - **The model** (`global_crash.py`): `simulate` and `ai_shock` take the step (`dt`, default a quarter); the per-step
      coefficients carried over by `step_common`, `step_region`, `step_rules` and `phillips_step`, the quarter's counts
      counted in steps (`quarter_steps`, `year_steps`, `step_index`), the measured bust read by step; dated levers
      (`Rules.fiscal_at`, `care_at`, `tariff_at`, `after`). Nothing refitted.
    - **The same model at a quarter**: on the stored regions and parameters, 80 runs (ten rule sets, four busts of both
      shapes and fractional dates, the energy term, a spread at the start and a premium, uniform and split waves) are
      bit-identical to main's (ad07564) code; the stored results stand.
    - **check_global_crash 57/57**: T1-T4 new (the coefficients untouched at a quarter and carried over at a month; a
      lever dated where its trigger fires reproduces the triggered run exactly; the bust by month is the bust by
      quarter at each quarter's end, its losses' total the same; the quarterly fit run monthly near itself in the
      central run, stated as found: 15.1% against 14.4% US out of work, output −6.5 against −5.9). T4's bounds (1.5
      points, 1 point) were set after seeing the numbers.
48. **2026-10-27 — the fitted episodes by month** (decision 82's second step; `code/episodes.py`, not yet the model's
    fit: `global_crash.fit` and its stored results stand until the added crashes are in). Each episode is the model at a
    monthly step on the economy of the time, its policy dated (1929-33: Smoot-Hawley 17 June 1930, the defence of gold
    in October 1931, the Revenue Act 6 June 1932; 2008-10: the Recovery Act 17 February 2009; the held-out dot-com bust:
    the tax cut of 7 June 2001, at the model's size and with none), its targets at their own frequency, each series
    counting by its years. Inputs changed with the step, each stated: 1929-33's equity is the NBER's monthly Dow-Jones
    index (FRED M1109BUSM293NNBR, cached; −87% by June 1932) in place of the stylised −40% then −86%; 2008-10's is
    household equity measured (Z.1, read by month between quarter ends) in place of the stylised −50% and −20%; a
    quarter's average enters in its middle month; 1929-33's exports are placed on the calendar (the quarterly fit read
    them a quarter early: index 0 at mid-1929, not its end, found here); 2008-10's inflation target is twelve-month core
    PCE against the model's own twelve-month change (before, the quarter's annualised rate against the data's year).
    - **The fit, by month, on 1929-33 and 2008-10** (the quarterly search, seed 7): loss 37.2 over 143 points, against
      44.0 at the quarterly fit's parameters run by month; the parameters barely move — spread per unit of capital lost
      3.10 (3.21), the money channel 9.18 (9.51), debt deflation 0 (0), the 1930s' Phillips slope 0.162 (0.136), Okun
      0.688 (0.713), 1930's spending collapse 6.9% of GDP (6.0), the rate transmission at its lower bound 0.03 (0.03).
      The misses are the quarterly fit's: 2008-10's gap too deep in 2008Q4-2009Q1 (−6.1 and −8.1 against −4.4 and −5.8),
      unemployment rising from early 2008 a few tenths too soon; 1929-33's unemployment too high in 1930 (12.9 against
      8.7). Held out, the dot-com bust: monthly unemployment's RMS error 0.54 (0.66 quarterly), the gap's 1.28 (1.11).
49. **2026-10-27 — the post-war US recessions added, and what they show** (decision 82's third step, under way; decision
    83; `code/episodes.py`: `us_state`, `us_episode`, `e1973`, `e1981`, `e1990`). Each on its measured start (FRED:
    unemployment, the funds rate, core PCE, debts, equity wealth, exports), measured shocks (Z.1 household equity,
    housebuilding, exports; oil as a three-month average where it drove the episode: 1973-75, 1990-91), the Fed's rate
    as set, and fiscal levers dated at their legislation at stated approximate sizes (the Tax Reduction Act of 29 March
    1975, about 1.4% of GDP over a year; the 1981 tax cut, 13 August 1981, about 1% a year; the 1990 budget agreement,
    5 November 1990, as consolidation). CBO's historical budget data (the deficit without automatic stabilisers, which
    would measure each size) refuse scripted fetches (403), so the sizes are stated, not measured.
    - **At the monthly fit on 1929-33 and 2008-10** (Log 48): 1973-75 misses (the gap −2.4 at worst against −7.3;
      core inflation's RMS error 6.5), 1981-82 misses (the gap near zero against −5.8), 1990-91 is too mild (−1.2
      against −3.5). Found and fixed on the way: at a monthly step the energy term read one month's oil jump, annualised
      (January 1974's tripling), and expectations formed on headline took it into core past 20%; the oil price now
      enters as a three-month average, the basis its pass-through was measured on.
    - **Fitted jointly as the model stands** (the five episodes, 371 points): the search takes the spread per unit of
      capital lost to its upper bound (15) and the money channel to zero, the rate transmission stays at its lower bound
      (0.03), 2008-10's gap goes to −10.8 against −5.8, and the added recessions still miss (loss 466). Not adopted.
    - **Why, as read here**: the model has no fast interest-sensitive spending (output answers the real rate with the
      gap's quarterly persistence, a half-life near three years, so 19% rates in 1981 bring no slump within the
      episode), no effect of oil on capacity (oil is only a tax on spending), and the relief to floating-rate borrowers
      is measured from the start's rate, so an episode starting at a rate peak (July 1981's 19%) reads falling rates
      as stimulus; the model was built for busts: falls in wealth, investment and banks' capital. Her call next (a
      veto-window question): fit on the busts and check on the rest, or extend the model first.
50. **2026-10-27 — the model extended, and fitted on all the crashes** (her call: "Extend the model first: fast
    rate-sensitive spending, relief measured from a pre-episode norm, oil's effect on capacity, expectations on smoothed
    inflation. Then fit all the crashes."; decisions 84-89; `global_crash.py`, `code/episodes.py`). Not yet the model's
    fit: `global_crash.fit` and every stored result stand until her call on adopting it and the restatement (the case,
    the website's export and its JavaScript at the monthly step).
    - **The extensions**, each off at its default: the 80 quarterly runs of Log 47 are bit-identical to main's
      (ad07564). check_global_crash 62/62, T5-T9 new; T7's condition was corrected after its first run (it compared the
      whole run's highest gap with the other run's lowest, where point by point was meant). Every battery passes (23;
      check_chains once its gitignored BEA cache was copied into the worktree).
    - **Each era's neutral rate** (decision 88). On today's 0.75 for every era the extended model fitted the US
      episodes at loss 128.6 (371 points) with rate-sensitive spending at its bound (1.0), by reading the 1970s-2000s'
      normal real rates (HLW's neutral rate 3.7-4.0) as tight money. On HLW's rate the fit sets rate-sensitive spending
      to zero, with housebuilding among the inputs (loss 210.7) or without it (229.9), and 1981-82 misses: the model's
      core inflation stays near 8.8% through 1982 (the data fall to 4.3%) because expectations are anchored on the
      start's own inflation, so the cuts read as easing and the channel adds stimulus from mid-1982. A lower stated
      target (4%) would let the channel help (1981-82's loss 117 to 61 at a_f 1). Not adopted: it would be tuning.
    - **The added crashes** (decision 89): 1937-38, Sweden 1990-93, the euro area 2011-13, Japan 1991-95 (December 1990
      to December 1995). Found on the way:
      - With investment endogenous, Sweden and Japan boomed on their measured fiscal stances (the gap +8 and +6 at the
        end, against −8 and −5).
      - Stated bank losses on top of measured investment counted Sweden's credit crunch twice.
      - The episodes' own trade channel read each economy's slump back to it as its partners'. The model's "rest of the
        world" is the regions' size-weighted gap, which is the economy itself at size 1 when the others are passive. It
        multiplied Sweden's slump about 2.2 times (−18 against −9) and fed back 0.07 and 0.16 of the gap in 1929-33
        and 2008-10.
      Fixed: the channel is off in every episode, whose exports are measured (`Episode.run`). The stored quarterly fit
      (`run_1929`, `run_2007`) has the same feedback; the restatement removes it.
    - **The joint fit** (nine episodes fitted, the dot-com bust held out; 750 points; 13 parameters; the search as
      before, seed 7; 12 minutes; `episodes.fit()` reproduces it): loss 421.6. The parameters:
      - the spread per unit of capital lost 15, at its bound, and the money channel 2.24 (3.10 and 9.18 at Log 48's
        fit); debt deflation 0;
      - the 1930s' Phillips slope 0.41; US Okun 0.64; 1930's spending collapse 7.9% of GDP;
      - the rate transmission at its bound, 0.03; rate-sensitive spending 0;
      - oil's capacity effect 1.77 per point of the energy bill;
      - Okun abroad: Sweden 0.92, the euro area 0.97, Japan 0.32.
      The worst gap and the highest unemployment, model against data:
      - 1929-33: output in 1933 0.69 of 1929's on the 2% trend (0.74); unemployment in 1933 26.0 (24.9).
      - 2008-10: −8.9 (−6.3); 10.3 (10.0).
      - 1973-75: −6.5 (−7.4); 8.9 (9.0).
      - 1981-82: −0.4 (−5.8); 7.5 (10.8).
      - 1990-91: −2.0 (−3.6); 6.4 (7.8).
      - 1937-38: unemployment 12.1 (20.0); output in 1939 1.06 of 1937's (1.04).
      - Sweden: −10.6 (−8.7); 9.9 (9.8).
      - The euro area: −2.8 (−2.7); 12.5 (12.2).
      - Japan: −5.9 (−7.0); 3.5 (3.4).
      Held out, the dot-com bust: unemployment's RMS error 0.42 (0.54 at Log 48), the gap's 1.10 (1.28), its trough
      −3.6 (−3.9).
    - **The misses, as read here**:
      - 1981-82: expectations in a disinflation, anchored on the start's own inflation.
      - 1937-38: the reserve requirement rises and the gold sterilisation have no channel, and the fiscal stance is
        the actual deficit, which understates fiscal 1938's tightening.
      - Core inflation late in the busts abroad runs too high (Sweden's fall in 1992 after the 1991 tax reform's VAT;
        Japan's to 0.3%).
    - **On today's 0.75 for every era**, for comparison: loss 379.6, lower by the same reading of normal real rates as
      tight money (1981-82's trough −1.5 against −0.4; Japan's −6.8). Not adopted (decision 88).
    - **Flag, hers to look at**: the bank channel is identified by 1929-33 alone, which cannot separate its two parts.
      The spread per unit of capital lost sits at its bound (1929-33's loss is 193 at 3 and 26 at 15). Widened to 40,
      the fit takes it to 19.1 and the money channel to 0, for a loss of 417.5. Under rules without a backstop the
      forward runs' spreads per unit of capital lost would be five to six times the stored fit's 3.21. Measured credit
      spreads as a target (Moody's Baa against Aaa, monthly from 1919, cached) would separate the two parts.
    - **Data** (all public, cached; no email in any request): the OECD's Economic Outlook 119 (SDMX: GDP, potential,
      the gap, the underlying primary balance, exports, investment); HLW's estimates (the New York Fed); Eurostat's
      quarterly accounts (the euro area's exports); FRED for the rest (OECD MEI unemployment, core prices, share
      prices and interest rates; BIS credit and property prices; the NBER's 1930s monthly unemployment and Dow-Jones;
      the federal surplus); the Riksbank's three-month bill, cached by se_1990s.py.
51. **2026-10-27 — the credit spread measured, a review, and the refit** (her call: "Add measured credit spreads (Baa
    against Aaa) as a target in the episodes, refit, and then show me the result before restating."; decision 90; not
    yet the model's fit: nothing restated).
    - **The target** (decision 90). Baa over Aaa rose from each start by 4.3 points in 1929-33 (May 1932), 1.7 in
      1937-38, 1.0 in 1973-75, 0.9 in 1981-82, 0.45 in 1990-91, 0.7 in 2000-03 and 2.2 in 2008-10 (December 2008). At
      Log 50's parameters the model's spread reached 15 in 1929-33. Refitted with the target alone, before the review
      below: the spread per unit of capital lost 3.18, the money channel 0, debt deflation 0.40; the spread's misfit
      fell from 1,200 to 44, the other targets' rose from 424 to 472.
    - **A review** (four independent readers, each finding reproduced in code by a second; then a second review of the
      fixes), every finding below found and fixed, and the episode results of Log 50 to be read with them:
      - Expectations on the window at a month took the per-step anchor and Phillips slope, which belong to the last
        step's form: a month's expectations were several times as persistent as a quarter's, and the 1930s' slope was
        fitted against a monthly slope cut to 0.36 of itself. Now the quarter's anchor and slope on the window (decision
        87; T10, T11 new; T11 added after the second review found T10, run without a slope, could not catch the slope's
        half reverted). Part of Log 50's "core inflation late in the busts abroad runs too high" was this.
      - Sweden's and Japan's model credit spread counted the crunch twice with their investment measured (now off
        there); the BIS's nominal property prices were read as real (the real series now); 1981-82's equity fall was
        measured from the end of September, not of July (`equity_fall`); the twelve-month inflation before the start
        abroad read indexes not seasonally adjusted (deseasonalised); relief was measured from the year before even with
        repricing off (from the start's rate now; T6 extended); 1929-33 counted Smoot-Hawley's export loss twice (only
        the switch from imports to home goods now: the loss is in the measured exports); 1975's tax cut was 2.16% of
        GDP in all where about 1.4 was stated (1.46 now); 2008-10 started from stated 2007Q4 averages (measured now, as
        every post-war episode); every US start's private debt was household plus corporate only, 19-29 points of GDP
        under the BIS total the forward runs use (the BIS's now); the episodes' printout zeroed the Okun slopes abroad.
      - Left for the restatement: the stored quarterly fit (`run_1929`, `run_2007`) has the trade feedback of Log 50
        and Smoot-Hawley's double count; the forward runs' shared mood adds each region's own bank stress at its size
        (the US's 0.44) to a spread now fitted with the mood off; by month the energy term's first two months drop the
        lagged pass-through of oil's change before the start (one earlier price is passed); at a step under a quarter
        the last step's form multiplies a one-step price impulse by one over the per-step anchor (the fitted model uses
        the window); rate-sensitive spending stays on where investment is measured (moot at its fitted zero).
    - **The refit** (966 points, the spread's 216 added; the dot-com bust held out; 13 parameters, seed 7; `episodes.fit()`
      reproduces it): loss 452.0, of it the spread 40.0 and the other targets 412.0 (Log 50's 424 on the same targets
      before the fixes). The parameters, with the stored quarterly fit's beside them:
      - the spread per unit of capital lost 2.67 (3.21); the money channel 0 (9.51); debt deflation 0.50, at its bound
        (0);
      - the 1930s' Phillips slope 0.137 (0.136); US Okun 0.64 (0.71); 1930's spending collapse 10% of GDP, at its bound
        (6.0); the rate transmission at its bound, 0.03 (0.03);
      - rate-sensitive spending 0; oil's capacity effect 2.67; Okun abroad: Sweden 0.93, the euro area 1.23, Japan 0.39.
      The worst gap and the highest unemployment, model against data:
      - 1929-33: output 0.85, 0.87, 0.81, 0.65 of 1929's in 1930-33 on the 2% trend (0.91, 0.86, 0.75, 0.74);
        unemployment 13.2, 13.6, 17.4, 27.6 (8.7, 15.9, 23.6, 24.9): too early, then too late.
      - 2008-10: −6.3 (−6.3); 9.0 (10.0). 1973-75: −6.5 (−7.4); 8.9 (9.0). 1990-91: −2.1 (−3.6); 6.5 (7.8).
      - 1981-82: −0.5 (−5.8); 7.5 (10.8). 1937-38: unemployment 12.2 (20.0).
      - Sweden: −10.6 (−8.7); 10.2 (9.8). The euro area: −2.0 (−2.7); 12.3 (12.2). Japan: −4.5 (−7.0); 3.4 (3.4).
      - The spread's peak: 1929-33 2.7 (4.3); 2008-10 1.1 (2.2); 1973-75 0.8 (1.0); 1981-82, 1990-91 and 1937-38 near
        zero (0.9, 0.45, 1.7): the post-war rises were default risk without bank losses, which the model has no
        channel for.
      Held out, the dot-com bust: unemployment's RMS error 0.55, the gap's 1.26, its trough −2.7 (−3.9).
    - **With the spread's effect on spending fitted too** (a check; a_s is fixed at 1.0, the low end of
      Gilchrist-Zakrajsek's range): it goes to 1.85, inside the range, and the loss to 449.1; the spread per unit of
      capital lost 2.54. So the fixed effect is not what holds the spread under the data; 1929-33's shape is.
    - **Flags, hers to look at**: 1929-33 now rests on debt deflation (at its bound) and 1930's spending collapse (at
      its bound), with the bank-run channel gone, and its unemployment path is early then late. The forward rows under
      the 1930s' rules (uninsured deposits) would lose the bank-run channel the stored fit gave them (9.51) and gain debt
      deflation wherever prices fall below the path debts were written for. The money and debt-deflation channels both
      grow with the banks' and prices' fall in 1931-33 and are weakly separated by one episode, as the spread and the
      runs were before the target.
52. **2026-10-28 — the monthly fit adopted, and the model run by month** (her call: "Adopt this fit (Log 51) and
    restate: the case, the export and the page's JavaScript at the monthly step, including the stored quarterly fit's
    own-feedback fixes."; decision 91).
    - **The model**: `episodes.py` fits and stores the fit (`results/episodes.json`); `global_crash.main` reads it,
      dates the presets on their central runs (`preset_dates`, stored), and runs the scenarios by month, their quarterly
      readings the quarter's average of its months. The triggered branches are gone from `simulate`; the "triggers on
      non-employment" rows are gone from the results. The quarterly fit is retired; `run_1929`, `run_2007` and
      `run_2000` are the quarterly check, own feedback off. Today's regions take the measured year-before rates, HLW's
      neutral rates and the fitted Okun slopes.
    - **Found on the way** (four parallel readers mapped every dependent first; reviewers checked the engine): the
      bust's loan losses at a month two months late (`_spread`); the euro area's halves reading each other as the rest
      of the world and the mood (E2); the site's engine already failing on this branch's new series before any change.
      All fixed.
    - **The restatement as first run, on Log 51's fit, was stopped before the numbers went anywhere**: debt deflation
      at its bound, linear, sent the forward runs past anything in the record (rules eroding: the four economies 39.2%
      below capacity, Sweden's drag 51% of GDP; the 1930s' rules at the model's floor with Sweden's at 153%). A cap at
      the record's largest shortfall (1929-33's, 37.9%) or debts re-written 10-20% a year did not stop it (39.2 and
      31.8 below capacity under eroding rules). Her call: refit first (Log 53).
53. **2026-10-28 — the bank runs measured, debt deflation levelling off, and the refit** (her calls: "Refit first", then
    "Saturating fit"; decision 92).
    - **The runs**: 1929-33's run channel reads the money stock's measured fall (Friedman and Schwartz's, FRED
      M1444AUSM027SNBR; trough 35.8% in April 1933). Refitted with it alone, the fit is the adopted one exactly (loss
      452.0; runs 0, debt deflation 0.5): the runs' measured timing does not by itself move the fit.
    - **Where debt deflation's support comes from** (at the fit; each episode's loss with it, then refitted without
      it): 1929-33 66.9 and 41.2 (the runs carry it better once measured); Japan 1991-95 26.8 and 74.4; 2008-10 21.4 and
      31.1; Sweden 46.1 and 47.8. The largest drags were 27% of GDP in 1929-33 (a 37.9% shortfall), 3.1% in Japan (3.0%),
      1.7% in 2008-10 (2.0%), 3.6% in Sweden (5.0%): the record supports the term at small shortfalls, not its slope at
      1929-33's.
    - **Fits compared** (loss on 966 points; the four economies' worst year-6 gap under today's rules on the page's
      central run, under eroding rules and under the 1930s' rules): the adopted linear 452.0 (-9.1, -39.2, -60); debt
      deflation held at 0.3, 463.9 (-6.8, -28.3, -60); at 0.15, 477.7 (-5.5, -21.1, -60); at 0, 493.7 (runs at their
      bound; -4.6, -15.6, -59.5); levelling off within the stated bounds, 424.5 (-8.5, -28.8, -59.5); the stored model
      before (-3.9, -13.2, -47.9); each fit, its episodes' losses and its forward runs in
      results/episodes_alternatives.json. With the slope's bound widened to 2 the levelling-off pair degenerates into a fixed
      drag from a 1.1% shortfall (388.5; the bust alone under today's rules -7.4): not adopted.
    - **The adopted fit** (decision 92; `episodes.fit()` reproduces it, loss 424.54): the spread per unit of capital
      lost 2.69; the bank runs 6.92; debt deflation 0.5 at its bound, levelling off at an 11.4% shortfall; the 1930s'
      Phillips slope 0.195; US Okun 0.681; 1930's spending collapse 7.5% of GDP; the rate transmission at its bound
      0.03; rate-sensitive spending 0; oil's capacity effect 2.50; Okun abroad, Sweden 0.953, the euro area 1.226, Japan
      0.400. Episode losses: 1929-33 36.0, 2008-10 20.2, 1973-75 23.3, 1981-82 117.9, 1990-91 31.4, 1937-38 119.0, Sweden
      45.1, the euro area 1.5, Japan 30.3; held out, the dot-com bust 8.8 (the best of every fit here).
    - **The forward runs on it** (year 6, the four economies' worst gap; stored model, then now): today's rules, the
      bust alone -2.24, -2.92; with displacement -4.45, -8.20; on the page's central run -3.93, -8.51; rules expand
      -3.67, -5.30; rules erode -13.21, -28.78; the 1930s' rules -47.87, -59.47; displacement without a bust -1.71,
      -3.83. Sweden moves most (the bust with displacement, today's rules: -5.26, -16.79): its inflation starts at 1.1%
      against its 2% target, so its price level falls behind the path its debts were written for from the start, on a
      private debt of 2.3 times GDP. The presets' dates: today's rules, the US and Sweden February 2028, France June,
      the rest of the union September, China August 2030.
    - **Flags, hers to look at**: debt deflation's slope at its bound and its levelling-off weakly identified
      (decision 92); under today's rules the forward runs rest on the slope at small shortfalls, which the record
      supports; the 1930s' rules on today's economy reach the model's floor (they were at -47.9 already).
