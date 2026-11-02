# STATE — consumption (blog-support thread)

**Project:** two questions Stella asked on 2026-11-02 about the 2026-06-14 post *Labor pressures causing market
distortion and a minimally invasive solution*: (1) would an LVT-funded dividend ("an LVT-UBI loop") move consumption
the way the post's VAT bridge does, and how similarly; (2) has the consumption breakdown moved over the last four
years, the way care took more than all net job growth over the latest two years in the watch page's chart data
(107-113.5%; the page itself says "most"), and is spending being held up by higher incomes or by some sectors?
Napkin grade, same rules as `austax/`: public official data only, every raw file vendored with a manifest, every
headline number recomputed by a check script, nothing substituted when a source fails.
**State as of:** 2026-11-02 (founded, built, independently verified, audited and pushed in one session).

T4 and T5 below are the three-taxes paper's results (`three-taxes/SKETCH.md`): T4, a land tax's stock (the price
fall at announcement) and flow (the annual bill) are the same money at two dates; T5, a rent-funded dividend's
circular flow is real but second-order.

## The answers in brief

All demand figures are static and impact-year, as % of CE 2024 consumption (the post's denominator, 45.5% of PCE;
multiply by 0.455 for PCE). The post's own macro numbers come from its dynamic wealth block, which this thread did
not rebuild, so only signs and orders of magnitude compare with them.

### 1. An LVT dividend through the bridge's machinery — `lvt/NOTES_us.md`, `lvt/NOTES_fi.md`

Similar in direction and composition; different in size, in who pays, and in the stock channel (mortgage collateral
instead of the VAT's levy) that sets the demand sign.
- **Same fingerprint, bigger.** At the post's $249 dividend (US, CE 2024) and under the post's decile method, every
  charted category bar keeps its sign (with tenure-aware baskets home maintenance and reading flip), rented dwellings
  stays the largest mover, new cars fall and used cars rise; nearly every bar (31 of 36) is the VAT bar times
  2.3-3.0. On the SCF's land distribution the top income decile holds 39% of residential land against 22% of
  VAT-able spending, so the same dividend moves more money: flow impulse 0.98% against 0.39%, top decile -$514 a month
  per adult share against -$172, eight deciles gain instead of seven. On CE's own home values the top decile holds
  32%: -$365 and an impulse of 0.67%, about 1.7 times the VAT's (and an SCF bill over a CE budget overstates the top
  decile's -11.7% of budget). Finland at equal (notional) revenue: all 37 bars keep their sign, at a median 1.8 times
  the VAT bar (0.7-2.2).
- **Different payers.** 99% of US LVT payers own their home and owners over 65 make 45% of net payments; nearly all
  renters are pure recipients (1.4% of payers), so with tenure-aware baskets the rent bar more than doubles ($18.10
  against $8.28).
- **What vanishes:** the VAT's 7.4-9.3% price-level step (the LVT's zero is standard incidence theory; the dividend's
  own rent demand, 3.6% of rent spending, still lifts rents), its indexation plumbing, and the Auerbach-Kotlikoff
  levy on existing wealth with its perception parameter lambda.
- **What appears:** a visible capitalization shock. At the bridge rate on residential land (phi = 0.848 of land rent
  at the 10-year yield), land prices fall 85% at announcement ($19.8tn), owners' aggregate LTV goes 29% -> 44%, and
  16.8m mortgaged owners cross 80% LTV.
- **Demand at impact, counted once** (each payer's bill as a flow at the decile MPC, plus a 6-cent credit effect on
  the borrowing room lost by owners crossing 80% LTV; same SCF balance sheets): LVT on residential land +0.15 [-0.20,
  +0.54], about neutral; with business and corporate land +0.67 [+0.10, +1.24] (corporate land on the wealth reading;
  +0.93 on the flow reading); the VAT on the same data, flow plus levy at lambda = 0.35, -1.37 [-2.21, -0.53] (the
  post's dynamic path: -0.69 at year 3). On PCE: +0.07, +0.30 and -0.62.
- **The LVT has its own lambda:** how holders read a price fall that is their own bill capitalized. It sets the sign.
  Counting crossers' lost equity on top of their bill double-counts (T4) and gives -0.91; only hand-to-mouth crossers
  responding gives +0.77; deferral for owners over 65 adds 2.0 points while the state lends; at the SCF's measured
  windfall MPCs (a one-off, one-month windfall question that speaks to the ordering, not the level: a stress case)
  LVT -0.68 and VAT -1.70.
- **Funding.** US: the bridge needs 53-88% of measured residential land rent (35-58% of all land rent) on the paper's
  four land-rent measures; full capture funds $276-461 per adult share a month on residential land. These are shares
  of the post's CE-based $249 ($835bn a year): a VAT on national-accounts consumption would raise up to $1.83tn
  ($548), which residential land cannot fund (phi > 0.98). Existing property taxes (US state and local $789bn in
  2025; Finland's municipal real-estate tax) are not netted, and corporate land after 2020 is assumed (Z.1 stopped
  publishing NFC structures after 2020Q4) and attributed wholly to SCF households, so L2's top-decile bills are an
  upper bound. Finland: household land rent cannot fund the bridge. Full capture funds EUR 37 a month per adult
  share, 19% of the bridge's EUR 199, at the 2022 yield (19-50% across every yield case: 30% at the December 2022
  yield, 32-34% at 2023-25 yields, up to 50% with the paper's +1.5-point band); a bridge-sized charge would be 8.9% of
  land value a year, a levy on dwellings, not a rent tax. At equal (notional) revenue the Finnish LVT is about twice
  as redistributive (bottom quintile +EUR 117 against +80; top -175 against -84).
- **Finland's demand.** At full capture and the 2022 yield, +0.04% [-0.01, +0.09] (+0.14 to +0.15 at the 2023-25
  yields; +0.13 if only hand-to-mouth crossers respond), against the Finnish VAT's -0.14% [-0.48, +0.20] on the same
  impact formulas. The Finnish sign turns on non-occupiers (cottages, rental flats, forest: 43% of household land):
  if they respond to their capitalized loss at 3.5 cents, -1.05% [-1.80, -0.29] at the 2022 yield and -0.49 to -0.57
  at 2023-25 yields. With no Finnish microdata, payers, hand-to-mouth shares and LTVs are parametric splits of
  published tables; the LTV shape and the collateral response are US transplants; renters pay nothing by assumption.
- **US vs Finland.** The post found the VAT's demand sign is substantially a wealth-concentration phenomenon. The VAT's
  US-Finland gap at impact (1.23 points on the same formulas) is almost entirely (1.20) its levy channel, which the
  LVT does not have, so on the clean reading both countries' LVTs sit near zero: at the US bridge's share of rent,
  both at 2024 yields, US +0.15 and Finland +0.13 (Finland +0.04 at its 2022 yield); at full capture US -0.04 and
  Finland +0.14 on 2024 yields, -0.37 and +0.04 on 2022 yields. Land being less top-heavy than financial wealth (top
  income decile: 29% of Finnish and 39% of US residential land, against 51% and 66% of financial assets) is true but
  works through the size of the flow, not the sign. At full capture, with both countries on the same year's yield,
  net demand with non-occupiers on the wealth reading is close (2024 yields: US -0.48, Finland -0.57; 2022: -1.17,
  -1.05), although the non-occupier channel itself is larger in Finland (-0.71 against -0.44 on 2024 yields). Only
  the collateral reading that double-counts the bill separates the countries (US -1.50, Finland -0.01 on 2024
  yields), because land is 42% of US house values against 20% of Finnish ones and 35% of US mortgaged owners cross
  80% LTV at full capture against 14%.
- **The loop** is real and second-order, as T5 says: in the US the LVT taxes back the land part of its own rent bar,
  about +1.1% of the dividend [0.9, 1.4] (Finland 0.4%); under the US VAT the same kind of increment goes to
  landlords, 60% of it to the top decile.

### 2. Moves in the breakdown, 2022-2026 — `recent/NOTES_sectors.md`, `NOTES_direct.md`, `NOTES_fingerprint.md`

**By sector: care takes 1.5-1.8 times its weight in real spending growth, far from all of it.**
- Care (health care services incl. nonprofit health, medical goods, net health insurance, child care, social
  assistance; 23-24% of PCE) took 36-41% of real PCE growth in each of the five headline windows since 2022 (35-46%
  in single calendar years 2022-2025) against 26% in the four years to Sep 2019. Care services alone, the closest
  match to the jobs series, took 26-33% from 18-20% of the level. Care's share of net job growth, computed from the
  watch page's chart data (sums of its twelve-month changes), was 21% in the four years to Sep 2019, 58% in the four
  years to Sep 2026 and 107% in the two years to Aug 2026 (113.5% Sep 2024-Sep 2026).
- Spending outside care slowed but did not stall: 2.0% a year over the last four years against 2.5% before the
  pandemic; over Sep 2024-Sep 2026 it grew 4.0% while private jobs outside care fell by 31,000.
- In dollars the shift depends on the base. Since Sep 2022 care's share of PCE rose 1.4 points (22.9% to 24.3%),
  three quarters of its 1.8-point rise in volumes, but 1.2 of those points recover the 2019-22 fall (24.07% to
  22.88%); against Sep 2019 it is up 0.2 points in dollars and 1.8 in volumes, a relative-price gap (care prices
  +19.9%, all PCE +27.5% since Sep 2019). The gap between care's 41% of four-year real growth and its 30% of the dollar
  increase is mostly general inflation (10.0 of 11.4 points), not care prices.
- The watch site's gap (real spending +1.8% vs real income excluding transfers +0.05% over six months) depends on the
  base: from Sep 2022 it opened in Apr-Sep 2026 and 59% of the six-month gap is outside care in volumes (75% in
  dollars); from Jan 2024 care is about half (49% in volumes, 39% in dollars); over the full four years care's excess
  growth is about the whole gap (121% in volumes, 98% in dollars). Lower measured saving covers 80% of the six-month
  gap, but saving is the identity's residual, so that restates the gap rather than explaining it. Jul-Sep 2026 are
  advance estimates: 57% of care spending in Sep 2026 comes from lines BEA extrapolates from the same CES jobs data,
  and those lines gave about a third of care's Jul-Sep growth. BEA's October release (2026-11-25) revises them.

**By income group.** The claim tested is Mark Zandi's (Moody's; EconoFact Chats, 2026-07-24,
`data/raw/other/`): top 20% real spending about +4% a year and bottom 80% about zero over roughly mid-2023 to mid-2026.
Nothing distributional covers 2026 (CE to Dec 2025, SCF at its 2025 interview, the PI nowcast 2025, DPI 2024, BLS
distributional PCE and the BEA-BLS joint distribution 2023). No official spending distribution shows a K after 2022,
and one of the claimed size across the whole top fifth is not in the data over 2022-25 (the CE's latest year alone
fits both stories). Income after taxes tilted to the top once (2023), and equity wealth clearly did. A K confined to
the very top could hide.
- Top-decile spending shares show no rise after 2022: CE (income-ranked) 22.3-23.9% over 2014-2025; BLS distributional
  PCE (spending-ranked) 25-27% over 2000-2023; BEA-BLS joint distribution (disposable-income-ranked) 19-21% over
  2004-2023; SCF 2025 (one cross-section) 28.3% (2024 income). Moody's ~49% is not public data and was not used.
- CE 2022 -> 2025: real spending of the top fifth +6.3%, bottom 80% +5.3% (gap +1.0, SE 2.8) where Zandi's split
  implies +12.5; the top-fifth share went 38.5% -> 38.9% where the split implies 41.5%. The latest single year
  (2024 -> 2025: +1.9, SE 2.7, against +4.0) fits both stories; the equity run-up was fastest after the CE window
  (+$8.8tn in 2026H1). Zandi's own numbers do not add up on official shares (+4%/0% gives 1.6-1.7% a year, not 2%).
- Income: pre-tax personal income shows no K through the 2025 nowcast; real disposable income did tilt to the top in
  2023 (+10.2% vs +7.7% over 2022-24) as taxes fell back from a 2022 peak heaviest at the top.
- Wealth: the top fifth by income took 88% of the $33tn rise in household equities since 2022Q3 (DFA, modelled after
  2022Q3). At an assumed 2-5 cents a dollar that could fund a 3-8 point spending gap by mid-2025 on SCF spending
  shares (4-10 on BEA-BLS shares; 5-13 and 7-17 by mid-2026), which the surveys do not show. For the top 1% alone to
  deliver Zandi's top-fifth gap, its spending would need about 80 points more growth than the bottom 80%'s in three
  years; the wealth-effect bound gives 12-29.
- Saving: by group the record ends in 2023, when the top decile was not saving less than in 2019 (45.6% -> 46.6%). The
  aggregate rate fell from 6.2% (2023-24) to 3.8% (Sep 2026). Both stories fit that.
- Stella's spending-pattern test (the category composition of national-accounts spending, with a backtest) can
  neither confirm nor rule out a K of Zandi's size: in real terms the spending-ranked source reads at its calm-2010s
  level once health care is set aside and the income-ranked source reads above its calm level in most windows, with
  errors about four times the size of the K it is looking for; in nominal terms both read below their calm levels in
  every window. The care lines move it, so as built it cannot tell a care boom from a K.
- MPC side-result: the SCF 2025 windfall question has spend shares falling from ~29% (bottom decile) to 18-20% (top),
  an ordering consistent with the post's MPC gradient, at its flat end (top/bottom 0.62-0.69, bootstrap 0.51-0.83,
  against the post's 0.40-0.65); it says little about the slope and nothing about the level.

## What the rebuild found about the post itself — `rebuild/NOTES_us.md`, `rebuild/NOTES_fi.md`

The post's code was never in this repository, so the machinery was rebuilt from the text and gated on the post's
published numbers (`data/tidy/post_published_numbers.csv`: 1,168 rows, 745 printed and 423 read off figures,
hand-transcribed and independently re-read; 529 gated). US: 256 PASS / 43 CLOSE / 2 MISS of 301; all 36 Fig 5 dollar
bars, the MPC calibration target, within the printed rounding. Finland: 160 / 57 / 11 of 228; Fig 1 exact. The
dynamic wealth block (Figs 8-10, Fig 9's year-2 bars) was not rebuilt. Things worth knowing:
1. Fig 5's two impulse labels disagree. The footer's "about +0.5% of consumption" fits only the charted bars over the
   charted budget (0.46%); the bars are 0.41% of consumption and the flow impulse 0.39%. The caption's "+0.4% of
   charted budget" fits the flow impulse (0.44% of the charted budget), not the bars it describes. The Finnish body
   text's "+0.4% of charted budget" has the same kind of slip: it fits the flow impulse as a share of consumption
   (0.44%), while the bars are 0.63% of the charted budget.
2. The macro text pairs the year-3 US central values (-0.69, -2.7) with Fig 8's year-5 band edges; Finland's year-3
   central (+0.04) gets a bracket [-0.17, +0.29] whose lower edge is from year 5 and upper edge from year 3 of Fig 10.
3. Method note: the US used-car VAT flag (0.5) is pinned by Fig 4, not by the EU Directive, whose margin scheme gives
   about 0.1 (dividend $242.5). The Finnish flags follow whole COICOP groups; Finnish law line by line funds about
   EUR 165-172 (central 168.5) instead of 193.
4. Method note: the Finnish machinery needs three conventions that do not fit together (equal-consumption-unit
   quintile weights, euro labels from the total column, division-level elasticities that break adding-up by 5.2%). A
   coherent version gives a rent bar of EUR 4.21 instead of 4.93 and a EUR 199 dividend, with nine of the post's ten
   largest movers still in the top ten.
5. Method note: the Finnish "15-point surcharge" is 15% of tax-inclusive spending (about 16.5-18.6 points on the
   existing rates); household composition comes from person deciles (tulonjako 12ew) that do not pair into the HBS
   household quintiles.
6. Smaller: the used-car ghost is -0.05 in the text and -0.04 on Fig 5; the wealth-effect range is 2-5 cents in
   footnote 31 and Fig 0 and three to five in the text (Figs 8-10 use 3.5). "About 3.7 years of national-accounts
   consumption" for Finnish wealth is not reproduced by the simple ratio (mean net wealth x households / 2023
   national-accounts consumption = 5.0; `data/tidy/README_fin.md`; not gated): check the concept before calling it a
   slip. The EUR 391k does reproduce.
7. Other internal inconsistencies (`data/tidy/README_post.md`, `rebuild/NOTES_fi.md`): new-car A-K whisker -6.03 vs
   -6.04; inflation per ramp year 2.5-3 vs 2.5-3.1 points; levy "about 8%" vs -8.5%; demand impulse +0.4-0.6% /
   +0.3-0.5% / 0.39%; Finnish "three to eight percent of budgets" (the net transfer spans 0.2-5.9%) and "withdrawal
   halves" (MPC 0.56); the text's food elasticities use per-household shares while the figures use per-CU shares.

## Not done

- The post's dynamic wealth block was not rebuilt: there is no dynamic VAT or LVT path; everything is static and
  impact-year.
- LVT design is not modelled: assessment, exemptions, rate design, and the existing property taxes (US $789bn;
  Finland's municipal tax, size not vendored). The default risk of the 14.4m US owners left underwater at the bridge
  rate is not modelled either.
- Finland: no household microdata (HFCS would replace the parametric payer, hand-to-mouth and LTV splits) and no
  windfall-MPC question.
- Nothing distributional covers 2026; the recent/ units should be rerun after BEA's 2026-11-25 release (October data,
  revised Jul-Sep).

## Her calls

1. **FRED was unreachable** from this container (empty replies through the proxy). The paper's household land
   residual was rebuilt from the Fed Board's own Z.1 CSV release, which FRED mirrors, with each FRED ID mapped and
   checked against the paper's cached FRED history. BEA's W875RX1 cross-check failed too (Table 2.6 line 36 stands
   in). The US yield (GS10: 4.21% in 2024, 2.95% in 2022) comes from the paper's FRED copy in `pinning/cache/GS10.csv`,
   outside these manifests. Acceptable? (`acquire_fed.py` and `acquire_bea.py --retry-failed` vendor and compare the
   FRED copies once FRED answers.)
2. **The LVT's collateral reading** to publish as central: the clean +0.15 (each crosser counted once), or -0.91
   with the T4 overlap.
3. **Finnish convention** for the LVT comparison: `coherent` is the main case, `post` reproduces the post. Keep?
4. **The post's slips** (items 1, 2 and the ghost and cents in 6, and 7): correct on the site? Items 3-5 are method
   notes; the 3.7 years is unexplained.
5. **BLS LABSTAT CE** (cx.data.1.AllData 127 MB and cx.series 32 MB, plus cx.aspect 777 MB for SEs; over GitHub's
   100 MB limit unless compressed) would fill the 2022-2023 suppressed decile cells, letting the bridge run on CE
   2022-23 and replacing the identity fills in fingerprint and direct. No headline depends on it. Pull it?
6. **A watch indicator** "real spending outside care" (the mirror of "private jobs outside care") belongs in the
   watch repository, which is not attached to this session. The series is ready in `recent/out/outside_care_monthly.csv`
   (2007-01 to 2026-09, every care definition).

## Verification record

Every unit was built by one agent and re-derived from the raw files by an independent agent (`checks/
verify_independent_*.py`), then corrected; the sectors and fingerprint units had a second, fresh review of their
framing, after which the direct unit's cross-references were aligned; a final audit traced the numbers in this file
to the outputs and reran the thread. Material corrections made: the US LVT headline had counted crossers' lost equity
on top of their bill (T4); the US-Finland non-occupier comparison mixed yield years (now both on the same year's
yield) and the Finnish headline now stands beside the like-for-like VAT net (-0.14); care's real-vs-dollar share gap
is mostly general inflation, not care prices, and the sectors gap split now depends on the starting month; the
fingerprint's first verdict overstated the evidence (calm-period z-scores, minimum detectable effects and calm-based
power withdrawn; the care lines and an elder-care mapping artifact steered it; a second review turned "leans weakly
against a K" into "cannot tell"); the income side's "no K" holds before taxes only, the direct unit's saving rows
are "can't tell", and Zandi's 90% fits only directly held stocks ranked by wealth; the Finnish statutory VAT is now a
EUR 164.8-171.8 bracket; an SCF 2022 IMPLICATE overflow in `acquire_fed.py` was fixed and the two tidy files
regenerated, with no result changed. Remaining verifier BADs are fixed verdicts or pre-correction constants,
convention changes made on purpose (increment-only grandfathering, the elder-care mapping), or disagreements about
the post's own choices; none is an unexplained number. Each NOTES file explains them.

## Files and run order

```
consumption/
  code/common.py         downloads (BLS gets the approved contact address), per-source manifests
  code/acquire_*.py      five scripts (bls_ce, bea, fed, fin = StatFin + Eurostat, usda): raw -> tidy, any order,
                         offline once vendored; failures go to FETCH_FAILURES.csv (retried only with --retry-failed)
  data/raw/<source>/     vendored files + MANIFEST.csv (sha256); raw/post, watch, other, ecb and a few files the units
                         added were fetched once through common.fetch, each with a manifest row
  data/tidy/             tidy CSVs + README_<source>.md; post_published_numbers.csv is the hand-transcribed gate list
  rebuild/               bridge.py (generic machinery), run_us.py, run_fi.py, gates, verifiers, NOTES, figures
  lvt/                   lvt_us.py, lvt_fi.py, runners, checks, verifiers, NOTES, figures
  recent/                sectors.py, direct.py, fingerprint.py, checks, verifiers, NOTES, figures
```
From the repo root, `venv/bin/python -I consumption/...`:
1. (optional, offline) `code/acquire_{bls_ce,bea,fed,fin,usda}.py`, any order.
2. `rebuild/code/run_us.py`, then `run_fi.py` (reads `rebuild/out/us_mpc_schedules.csv`); then `rebuild/checks/
   gate_us.py` and `gate_fi.py`.
3. `lvt/code/run_lvt_us.py` (reads `rebuild/out` and, outside consumption/, `pinning/cache/GS10.csv` and `three-taxes/
   data/lvt_shock.csv`), then `run_lvt_fi.py` (reads the US LVT outputs; its check I3 fails until it is rerun after
   any US LVT change); then `lvt/checks/check_lvt_us.py` and `check_lvt_fi.py`.
4. `recent/code/sectors.py`, `direct.py`, `fingerprint.py` (~11 min); then `recent/checks/check_{sectors,direct,
   fingerprint}.py`.
5. Each unit's `checks/verify_independent_*.py` (records of the independent verification; they print, and some write
   out/verify_independent_*.csv).

Do not hand-edit numbers in the recent/ NOTES: they embed generated tables and passages (`recent/out/notes_tables_
sectors.md`, `notes_text_sectors.md`, `direct_notes_tables.md`, `fingerprint_notes_tables.md`), and the checks fail if
the two drift. Where to look first: `lvt/out/us_lvt_headline.csv`, `fi_lvt_headline.csv`, `fi_lvt_us_compare.csv`;
`recent/out/headline_sectors.csv`, `gap_timing.csv`, `direct_evidence_table.csv`, `fingerprint_read.csv`;
`rebuild/out/gate_us.csv`, `gate_fi.csv`. Figures: `lvt/figures/us_lvt_net_by_decile.png`, `us_lvt_macro_channels.png`,
`fig_fi_us_compare.png`, `fig_fi_funding_gap.png`; `recent/figures/fig_care_share_of_growth.png`, `fig_outside_care.png`,
`fig_direct_top_shares.png`, `fig_fingerprint_scatter.png`; `rebuild/figures/fig5_rebuilt.png`, `fig2_rebuilt.png`.
