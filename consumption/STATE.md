# STATE — consumption (blog-support thread)

**Project:** two questions Stella asked on 2026-11-02 about the 2026-06-14 post *Labor pressures causing market
distortion and a minimally invasive solution*: (1) would an LVT-funded dividend ("an LVT-UBI loop") move consumption
the way the post's VAT bridge does, and how similarly; (2) has the consumption breakdown moved over the last four
years, the way care absorbed nearly all job growth on the watch site, and is spending being held up by higher incomes
or by some sectors? Napkin grade, same rules as `austax/`: public official data only, every raw file vendored with a
manifest, every number recomputed by a check script, nothing substituted when a source fails.
**State as of:** 2026-11-02 (founded, built, independently verified and pushed in one session).

## The answers in brief

### 1. An LVT dividend through the bridge's machinery — `lvt/NOTES_us.md`, `lvt/NOTES_fi.md`

Similar in direction and composition; different in size, in who pays, and in the macro channel that sets the demand
sign.
- **Same fingerprint, bigger.** At the post's $249 dividend (US, CE 2024), every charted category bar keeps its sign,
  rented dwellings stays the largest mover, new cars down and used cars up; nearly every bar (31 of 36) is the VAT
  bar times 2.3-3.0. Land is more top-heavy than VAT-able spending (the top income decile holds 39% of residential
  land against 22% of VAT-able spending), so the same dividend moves more money: flow impulse 0.98% of consumption
  against 0.39%, top decile -$514 a month per adult share (-11.7% of its budget) against -$172 (-3.9%), eight
  deciles gain instead of seven. Finland at equal revenue: all 37 bars keep their sign at about 1.8 times.
- **Different payers.** 99% of US LVT payers own their home; owners over 65 make 45% of the net payments; renters
  are pure recipients, so with tenure-aware baskets the rent bar is about twice as large.
- **What vanishes:** the VAT's 7.4-9.3% price-level step, its indexation plumbing, and the Auerbach-Kotlikoff levy
  on existing wealth with its perception parameter lambda.
- **What appears:** a visible capitalization shock. At the bridge rate on residential land (phi = 0.848 of land rent
  at the 10-year yield), land prices fall 85% at announcement ($19.8tn), owners' aggregate LTV goes 29% -> 44%, and
  16.8m mortgaged owners cross 80% LTV.
- **Demand at impact, counted once** (each owner's bill as a flow, plus a credit effect on lost borrowing room; % of
  consumption, same SCF balance sheets): LVT on residential land +0.15 [-0.20, +0.54], about neutral; with business
  and corporate land +0.67 [+0.10, +1.24]; the VAT on the same data -1.37 [-2.21, -0.53] (the post's own dynamic path:
  -0.69 at year 3). The sign turns on the collateral concept (counting lost equity on top of the bill double-counts,
  T4: -0.91), on who responds (only hand-to-mouth crossers: +0.77), on deferral for older owners (+2.0 points while
  the state lends), and on the MPC level (at the SCF's measured windfall MPCs: LVT -0.68, VAT -1.70).
- **Funding.** US: the bridge needs 53-88% of measured residential land rent (35-58% of all land rent) on the paper's
  four land-rent measures; full capture funds $276-461 per adult share a month on residential land. Finland:
  household land rent cannot fund the bridge. Full capture funds EUR 37 a month per adult share, 19% of the bridge's
  EUR 199, at the 2022 yield (19-50% across every yield case: 30% at the December 2022 yield, 32-34% at 2023-25
  yields, up to 50% with the paper's +1.5-point band); a bridge-sized charge would be 8.9% of land value a year, a levy
  on dwellings, not a rent tax. At equal (notional) revenue the Finnish LVT is about twice as redistributive (bottom
  quintile +EUR 117 against +80, top -175 against -84). At full capture Finnish net demand at impact is +0.04%
  [-0.01, +0.09], against the Finnish VAT's -0.14% [-0.48, +0.20] on the same impact formulas.
- **US vs Finland.** The post found the VAT's demand sign is mostly a wealth-concentration story. The VAT's US-Finland
  gap at impact (1.2 points on the same formulas) is entirely its levy channel, which the LVT does not have, so on
  the clean reading the two countries' LVTs nearly coincide: at the US bridge's share of rent, US +0.15 and Finland
  +0.13. Land being less top-heavy than financial wealth (top income decile: 29% of Finnish and 39% of US residential
  land) is true but works through the flow channel, not the sign. With both countries on the same year's yields their
  non-occupier stock channels are also close (2024 yields: US -0.48, Finland -0.57); only the collateral reading that
  double-counts the bill separates them (US -1.50, Finland -0.01), because land is 42% of US house values against 20%
  of Finnish ones and far more US owners cross 80% LTV.
- **The loop** is real and second-order, as three-taxes T5 says: the LVT taxes back the land part of its own rent bar,
  about +1.1% of the dividend; under the VAT the same kind of increment goes to landlords, 60% of it to the top decile.

### 2. Moves in the breakdown, 2022-2026 — `recent/NOTES_sectors.md`, `NOTES_direct.md`, `NOTES_fingerprint.md`

**By sector: care takes about twice its share of spending growth, not all of it.**
- Care (health care services, medical goods, net health insurance, child care, social assistance; 23-24% of PCE)
  took 36-41% of real PCE growth in each window examined since 2022 (41% over Sep 2022-Sep 2026), against 26% in the
  four years to Sep 2019. Its share of net job growth went 21% -> 58% -> 107% (Aug 2024-Aug 2026; 113.5% Sep-Sep),
  computed from the watch page's chart data.
- Spending outside care slowed but did not stall: 2.0% a year over the last four years against 2.5% before the
  pandemic; over Sep 2024-Sep 2026 it grew 4.0% while private jobs outside care fell by 31,000.
- In dollars the shift is small: care's share of PCE was 24.07% in Sep 2019 and 24.27% in Sep 2026. The volume shift
  is larger because measured care prices rose less than other prices.
- The watch site's gap (real spending +1.8% vs real income excluding transfers +0.05% over six months) depends on the
  base: from Sep 2022 it opened in Apr-Sep 2026 and 59% of it is outside care; from Jan 2024 care is about half.
  Lower measured saving covers 80% of the six-month gap, but saving is the identity's residual, so that restates the
  gap rather than explaining it. The latest care spending is partly extrapolated by BEA from the same CES jobs data.

**By income group: no official series shows a K through its last year; one of the claimed size across the whole top
fifth is not in the data, but a K confined to the very top could hide.**
- Top-decile spending shares are flat: CE (income-ranked) 22.3-23.9% over 2014-2025; BLS distributional PCE
  (spending-ranked) about 26% over 2000-2023; BEA-BLS joint distribution (disposable-income-ranked) 19-21% over
  2004-2023; SCF 2025 28.3% (2024 income). Moody's ~49% is not public data and was not used.
- CE 2022 -> 2025: real spending of the top fifth +6.3%, bottom 80% +5.3% (gap +1.0, SE 2.8) where Zandi's split
  (top 20% +4% a year, bottom 80% ~0) implies +12.5; the top-fifth share went 38.5% -> 38.9% where the split implies
  41.5%. The latest single year fits both stories, and the equity run-up was fastest after the CE window (2026H1).
- Income: pre-tax personal income shows no K through the 2025 nowcast; real disposable income did tilt to the top
  in 2023 (+10.2% vs +7.7% over 2022-24) as taxes fell back from a 2022 peak heaviest at the top.
- Wealth: the top fifth by income took 88% of the $33tn rise in household equities since 2022Q3 (DFA, modelled after
  2022Q3). At 2-5 cents a dollar that could fund a 3-8 point spending gap by mid-2025, which the surveys do not show.
  For the top 1% alone to deliver Zandi's top-fifth gap, its spending would need about 80 points more growth than the
  bottom 80%'s in three years; the wealth-effect bound gives 12-29.
- Stella's spending-pattern test (category composition of national-accounts spending, with a backtest) can neither
  confirm nor rule out a K of Zandi's size: the spending-ranked source reads at its calm-2010s level once health
  care is set aside; the income-ranked source reads above its calm level in most windows, with errors about four
  times the size of the K it is looking for. The care lines move it, so it cannot tell a care boom from a K as built.
- MPC side-result: the SCF 2025 windfall question has spend shares falling from ~29% (bottom decile) to 18-20% (top),
  an ordering consistent with the post's MPC gradient (top/bottom 0.62-0.69 against the post's 0.40-0.65).

## What the rebuild found about the post itself — `rebuild/NOTES_us.md`, `rebuild/NOTES_fi.md`

The post's code was never in this repository, so the machinery was rebuilt from the text and gated on its 1,168
published numbers (`data/tidy/post_published_numbers.csv`). US: 256 PASS / 43 CLOSE / 2 MISS of 301; all 36 Fig 5
dollar bars within the printed rounding. Finland: 160 / 57 / 11 of 228; Fig 1 exact. Things worth knowing:
1. Fig 5's caption and footer swap their impulse denominators (the bars are 0.41% of consumption and 0.46% of the
   charted budget); the Finnish caption has the same slip.
2. The macro text pairs year-3 central values (-0.69, -2.7, +0.04, -0.65) with year-5 band edges.
3. The US used-car VAT flag (0.5) is pinned by Fig 4, not by the EU Directive, whose margin scheme gives about 0.1
   (dividend $242.5). The Finnish flags follow whole COICOP groups; Finnish law line by line funds about EUR 165-172
   instead of 193.
4. The Finnish machinery needs three conventions that do not fit together (equal-consumption-unit quintile weights,
   euro labels from the total column, division-level elasticities that break adding-up by 5.2%). A coherent version
   gives a rent bar of EUR 4.21 instead of 4.93 and a EUR 199 dividend, with nine of the ten top movers unchanged.
5. The Finnish "15-point surcharge" is 15% of tax-inclusive spending (about 16.5-18.6 points on the existing rates);
   household composition comes from person deciles (tulonjako 12ew) that do not pair into the HBS household quintiles.
6. Smaller: the used-car ghost is -0.05 in the text and -0.04 on Fig 5; "about 3.7 years of consumption" for Finnish
   wealth is not reproduced (5.0 by the simple ratio; the EUR 391k does reproduce); the wealth-effect range is 2-5
   cents in a footnote and three to five in the text.

## Her calls

1. **FRED was unreachable** from this container (empty replies through the proxy). The paper's household land
   residual was rebuilt from the Fed Board's own Z.1 CSV release, which FRED mirrors, with each FRED ID mapped and
   checked against the paper's cached FRED history. Acceptable? (`acquire_fed.py --retry-failed` vendors the FRED
   copies and compares them once FRED answers.)
2. **Finnish convention** for the LVT comparison: `coherent` is the main case, `post` reproduces the post. Keep?
3. **The post's slips** above: correct on the site?
4. **BLS LABSTAT CE database** (127 MB) would fill the 2022-2023 suppressed decile cells; not pulled.
5. **A watch indicator** "real spending outside care" (the mirror of "private jobs outside care") belongs in the watch
   repository, which is not attached to this session.

## Verification record

Every unit was built by one agent and re-derived from the raw files by an independent agent (`checks/
verify_independent_*.py`), then corrected; the question-2 units had a second, fresh review. Material corrections
made: the US LVT headline had double-counted the stock and the flow for collateral crossers (T4); care's real-vs-
dollar share gap is mostly general inflation, not care prices; the fingerprint's first verdict overstated the
evidence (calm-period z-scores and power withdrawn; care lines and a child-care mapping artifact steered it); the
income side's "no K" holds before taxes only. Remaining verifier BADs are documented in each NOTES file (they are
deliberate rewrites, not number disagreements).

## Files and run order

```
consumption/
  code/common.py          downloads (BLS gets the approved contact address), manifests
  code/acquire_*.py       bls_ce, bea, fed, fin, usda: vendor raw -> data/tidy (rerun offline)
  data/raw/<source>/      vendored files + MANIFEST.csv (sha256)
  data/tidy/              tidy CSVs + README_<source>.md; post_published_numbers.csv (the gate list)
  rebuild/                bridge.py (generic machinery), run_us.py, run_fi.py, gates, verifiers, NOTES
  lvt/                    lvt_us.py, lvt_fi.py, runners, checks, verifiers, NOTES, figures
  recent/                 sectors.py, fingerprint.py, direct.py, checks, verifiers, NOTES, figures
```
Run from the repo root with `venv/bin/python -I`: `code/acquire_*.py` (offline once vendored) -> `rebuild/code/run_us.py`,
`run_fi.py` -> `lvt/code/run_lvt_us.py`, `run_lvt_fi.py` -> `recent/code/sectors.py`, `direct.py`, `fingerprint.py`
(~11 min) -> each unit's `checks/check_*.py` and `checks/verify_independent_*.py`.
