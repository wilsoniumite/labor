# Playground, the night of 2026-11-05

Her request: "play around with the model, try lots and lots of stuff cheaply." Each run changes one or two things
from the kept model (the paper's model with the cap, the basket and the pinned 1950 start, misfit 6.77) and refits the
free numbers once, from the kept fit, with the explorer's fitter (`explorer/model.js`). No multi-start search and no
validation beyond the fit itself: these are leads, not results. Scripts and raw numbers are in `../playground/`.

Misfit columns: total | wage in durables, wage in shelter, labour's share, prime-age employment, θ_V (1 = one tolerance).

## What the kept model's numbers can and cannot tell apart

| Fixed | Misfit | Clock | Return | a |
|---|---|---|---|---|
| nothing (kept) | 6.77 | 11.3% | 0 | 9.4 |
| clock 14% / 13% / 12% | 7.00 / 6.87 / 6.79 | | 0 | 9.6 |
| clock 10% / 9% / 8% | 6.85 / 7.02 / 7.28 | | 0 | 9.2-8.5 |
| clock 7% / 6% / 5% / 4% | 7.62 / 8.13 / 11.6 / 26.1 | | | |
| return 1% / 3% / 5% / 10% | 6.98 / 7.34 / 7.49 / 7.63 | 10.8% / 9.3% / 8.6% / 8.0% | | 7.9 / 5.8 / 4.6 / 3.1 |
| a 5 / 3 / 1 | 7.45 / 7.64 / 8.97 | 8.7% / 7.9% / 6.4% | 4% / 10% / 30% | |
| the measured real rate passed through, 10% / 50% / 100% | 7.47 / 9.74 / 10.15 | | | |

The clock's pace, the required return, the machine services in building a machine (a) and the machine-making labour
lie on a ridge: any clock from 8% to 14% a year fits within 0.5 of the best, and a 5% return costs 0.7 and brings the
clock to 8.6%. The zero return is not essential, but it is where land's share of a basket's cost is plausible
(0.11 -> 0.14 against housing's 0.11 -> 0.16 of spending; at a 5% return it is 0.04 -> 0.05). These five series do
not pin the clock. The untargeted waterline (the wage against machine cost at the margin, 1999-2025, `wc_median`) might.
The measured real rate in the required return makes every fit worse (candidate I fails again).

## The kept model's pieces

| Change | Misfit | By series |
|---|---|---|
| no cap | 11.85 | 24.9 10.3 9.7 7.9 6.4 |
| no basket (cap kept) | 117.8 | 198 258 78 51 3.8 |
| start not pinned | 6.74 | 6.2 5.1 16.9 1.4 4.2 |
| cap 0.80 / 0.815 (the 2000 peak) | 6.83 / 7.09 | |
| basket elasticity 0.5 / 1.0 / 1.2 (set: 0.875) | 9.25 / 6.35 / 6.04 | |
| utility flat from 1950 | 9.64 | 6.3 6.5 18.8 13.2 3.3 |
| utility rising all along at its 1950-70 pace | 11.92 | |
| utility kinked at 1973 (the real wage's peak) | 6.74 | |
| utility following the real wage every year | 6.77 | |

Both the cap and the basket do real work, and the basket is what lets the cap work at all. The rise-then-hold utility
matters (flat or always rising is far worse); where it turns (1970, 1973, or the real wage itself) hardly does.

## New ideas

| Idea | Misfit | By series | Note |
|---|---|---|---|
| A: shelter's building priced like durables (site 0.4) | 28.6 | 51.9 73.3 3.1 4.6 10.0 | as before: caps the fork |
| A′: the building priced like building work, at the wage (site 0.4) | 6.28 | 6.0 3.0 16.8 2.6 2.9 | site 0.3 / 0.5 / 0.6 / 0.7: 6.49 / 6.15 / 6.12 / 6.19 |
| her internet idea: tastes tilt from land after 1995 | 5.22 | 6.4 0.6 14.3 1.5 3.3 | the site's weight falls to 0.63 by 2024; from 1990: 5.38, from 2000: 5.19 |
| women's entry: the cost of working falls until 1985 | 6.73 | | does nothing |
| land expanding until 1970 (the suburbs) | 6.68 | | does nothing |
| land bent at 1970 and 2024 | 5.82 | 6.5 2.1 16.3 1.2 2.9 | |
| labour's share read as all labour (the machine chain's too) | 7.31 | 4.0 6.8 20.6 1.4 3.7 | worse |
| 1950 labour share pinned (through k) | none | | no steepness reaches 0.66 at the kept numbers |
| clock bendable (1970, 1990, 2010, 2024) | 5.47 | 4.7 4.5 12.5 1.7 3.8 | |
| machine-making labour bendable | 5.59 | 8.0 3.1 10.8 1.8 4.3 | |
| both bendable / with A′ | 5.05 / 4.93 | | |
| clock bent at 1973 and 1995 | 5.98 | 12.9 3.0 7.4 2.1 4.4 | the labour share fits, the durables wage does not |
| A′, clock and machine labour by decade | 4.71 | | the clock runs backwards in two decades: overfitting |

- **A′ is a mild, principled improvement**: houses are not built like durables, and pricing the building at the wage
  removes A's cap on the fork. A, as built, was the wrong version of a right idea.
- **Her internet idea fixes the wage in shelter after 1995** (misfit 0.6: it flattens and rises a little, as the record
  does), with one number. Its cost: land's share of spending then falls after 1995 (0.14 -> 0.10) while housing's share
  of spending rose. On this reading, people bought less land per head, yet spent more on housing; that has to be
  squared before the tilt is believed.
- **Labour's share before about 1985 is still the stubborn fact.** The principled ideas (women's entry, land supply,
  reading all labour) do not move it. Bending the clock or the machine-making labour does, but the bends' shapes change
  with where the knots are placed (the break-year clock and the decade clock tell different stories, one with the clock
  running backwards), so those are fits to the curve, not findings. An earlier remark that the bent clock rediscovers
  the 1973-95 productivity slowdown did not survive the break-year test.

## The waterline, as an independent read of the clock

The panel's untargeted waterline (`wc_median`: production wages over quality-adjusted machine prices, 1999 = 1, the
median of six members from `../companion/data/wc_grid.csv`) rose x7.6 from 1999 to 2023 (log +2.03; members x2.4 to
x16 by 2025). Its model counterpart, with machine prices quality-adjusted, is the margin's place on the schedule in
capability units, gamma(x*) / eta = g0 + g1 x*^k (`docs/measurement.md` maps it to gamma(x*) itself, which falls in every
run; with hedonic prices the ratio to eta looks like the right object: for her to confirm). On that reading the kept
model gives x3.6 (log +1.29), and so does every clock on the ridge, from 8% to 14% (+1.24 to +1.31):
the waterline cannot pin the clock's pace, and the model's margin climbs the schedule at about two thirds of the record's
pace in logs, inside the members' range but below their median (`playground/waterline.py`).

## In the explorer

Three of these are presets in the explorer (https://claude.ai/artifact/SeXw2LyrPk8urB7aH7cMRs): the tastes tilt, A′,
and the kept model with a 5% return. The page now has switches for A′ (building priced like building work) and the
tilt (its start year and its 2024 weight), and the fit moves the tilt's weight when it is on.

## Her questions of 2026-11-06: equivalences, and two clocks

- **A machine's cost is three shares that add to one**: machine services (rho + delta) a, labour theta_V = lambda gamma(x*)
  (rho + delta), and land b / Vm. The record pins the shares, not a and the return separately: along the ridge a runs
  9.4 -> 3.1 while machine services stay 0.38-0.43 of the cost in 1950 and 0.47-0.50 in 2024. The machine's rental in land
  units is p_m = (rho + delta) b / (land's share): the paper's pinning in one line.
- **The kept fit's machines become almost land-free**: land's share of a machine's cost falls from 0.32 (1950) to 0.005
  (2024), where calibration (c) measured fixed costs (land rents and imported content) at 0.33 in 2023. Setting the
  return at 2% and a so that machine services are 0.20 of the cost in 2023 (calibration (c)'s split: labour 0.47, fixed
  0.33): misfit 9.14 (four series without theta_V 8.40, against 7.41), clock 5.8% a year, land's share 0.57 -> 0.28.
- **Land and population**: tripling adults and land together leaves the fit exactly unchanged; T is land per adult in
  1950, in units of the land in a machine (b, fixed at 0.4). (b, h, T) scale together exactly.
- **Two clocks**: the second clock is lambda's, and the record's theta_V pins it once the capability clock is set.
  Taking theta_V from the record year by year instead (lambda then needs no clock) breaks the fit (35.3: the wage in
  shelter 131): the measured series jumps between benchmark years and is missing before 1967, and its jumps pass straight
  into machine prices and the wage. A smooth lambda clock does the same job without passing on the noise
  (`playground/round5*.js`).

## Her spiky settings and technology waves, 2026-11-06

- **The machine is a free unit.** Scaling, year by year, the machine service a task needs by c_t and both the hours and
  the land in a machine by 1/c_t changes nothing: with wild spikes in c_t the kept model's misfit stays 6.772334 to the
  last digit (`playground/unit_check.js`); the same spikes in the clock alone leave 21 years without an equilibrium. So
  the model has two real clocks, the land and the hours embodied per unit of task capacity (b eta and lambda eta);
  "capability" on its own is a unit. Her spiky settings (misfit 15.9; labour's share 4.2 against the kept model's 17.1,
  bought with the wage legs) were mostly that unit changing size: her clock and hours-per-machine spikes mirror each
  other, and the hours per unit of task capacity fall smoothly throughout (`playground/her_spiky.json`,
  `waves_look.js`). What is left is the land per unit of task capacity: a steep fall to 1965, a rise around 1970, a fall
  to 1999.
- **Waves** (her idea: a discovery is chased hard, then the lower fruit comes slower): each lowers both real clocks by a
  size (logs) as size (1 - exp(-(t - year) / tau)), on a steady pace (`explorer/model.js`, S.waves).

  | Waves | Misfit | By series | Clock by era (1950s / 60-73 / 73-95 / 95-05 / 05-24) |
  |---|---|---|---|
  | none (kept) | 6.77 | 6.4 4.7 17.1 1.4 4.2 | 11.3% throughout |
  | fixed at 1970 and 1995, sizes free | 6.83 | | the fit shrinks both to nothing |
  | dates free, from 1970 and 1995 | 5.38 | 3.9 4.5 12.9 2.0 3.7 | 12.3 / 10.2 / 8.1 / 18.0 / 7.2 |
  | dates free, from 1960 and 1985 | 5.39 | 7.7 3.7 9.9 1.7 4.0 | 13.0 / 10.3 / 11.7 / 10.4 / 7.1 |
  | three, dates free | 5.31 | 4.4 4.6 12.2 1.8 3.7 | 12.9 / 10.1 / 9.1 / 17.7 / 7.2 |
  | dated from the productivity record: post-war 1948, IT 1995 | 5.53 | 4.4 5.0 12.6 2.0 3.7 | 13.0 / 10.7 / 9.1 / 17.3 / 8.3 |
  | dated: post-war 1948 alone | 6.39 | 7.3 4.2 13.6 2.5 4.2 | |
  | dated: IT 1995 alone | 6.68 | | |

  Every flexible fit finds an early burst (from about 1950, winding down over 15-20 years), and it is what pulls
  labour's share down early. With free dates the later wave lands at 1997 or 1984 for the same misfit: the record does
  not date it. Dated from outside (the textbook productivity breaks), two waves cost four numbers and take the misfit
  from 6.77 to 5.53, and the clock then runs the productivity record's shape (fast to 1973, slower to 1995, a burst to
  2005, slow after), but that shape is put in by the dates, not found. A third dated wave (2015) fell into a worse local
  optimum (6.53) from every start tried.

## While she was away, 2026-11-06: what labour's share needs

- **Labour's share against the wage in durables.** Weighting labour's share up shows the model can fit it (misfit 1.2
  at x30), but only by giving up the wage in durables (6.4 -> 33 at x10, 48 at x30) and θ_V; with the dated waves, labour's
  share reaches 0.9 at a cost of 29 on the durables wage (`explore2.js` A). Within this one-good model a sixfold rise of
  the wage in durables and a falling labour share pull against each other.
- **The early burst is labour's share's.** One wave with a free date lands at 1950-53 whether the start is pinned or
  not and whether or not 1950-55 are counted; with labour's share left out of the fit it vanishes (`explore2.js` D).
- **Waves on defensible numbers** (the return at 2%, a from the measured split): 9.14 -> 7.90 with the dated waves, the
  clock's pace 4.4% (`explore2.js` B).
- **Her developer surge** (the hours to build machines rising after a discovery, then fading): 5.55 -> 5.30 with four
  more numbers, the surge after 1995 coming out negative: not in the record (`explore2.js` C).
- **The goods wage read over everything but shelter.** The model has one final good; the wage target deflates it by
  durables, the goods that cheapened fastest (the real wage in durables x6.2 since 1950, over everything but shelter
  x2.0, over shelter x1.05). Read over the CPI less shelter (FRED CUUR0000SA0L2, now the panel's `wage_exshelter`, check
  I10), labour's share fits (17.1 -> 2.5) and employment becomes the strain (11.0): the real wage no longer rises enough
  to draw people in (`exshelter.js`). Then women's entry, which did nothing before, does the work: the cost of working
  falling to about 0.8 of 1950's by 1985-90, held after (`exshelter2.js`).

  | Goods wage over | Additions | Misfit | Goods, shelter, labour's share, employment, θ_V |
  |---|---|---|---|
  | durables | kept model | 6.77 | 6.4 4.7 17.1 1.4 4.2 |
  | all but shelter | kept model | 8.32 | 12.5 8.8 2.5 11.0 6.7 |
  | all but shelter | women's entry to 1990 (one number) | 2.92 | 1.2 5.3 3.2 1.1 3.8 |
  | all but shelter | women's entry to 1985 + the post-war wave | 2.42 | 1.5 5.3 1.3 1.2 2.8 |
  | all but shelter | women's entry, measured machine split (return 2%) | 12.67 | 12.4 7.7 14.1 12.4 16.8 |

  Ten of twelve scattered restarts reach the same optimum (2.92); two found no start (`exshelter3.js`). The fit still
  wants a zero return and machine services at half a machine's cost; with the measured split it falls back to 12.7.
  What it gives up: the model then has no durables, so the paper's fork (durables against shelter, x4.8 over 1964-2024)
  is not reproduced, only everything-but-shelter against shelter (x1.9). Holding both would take a second good: durables,
  automatable, beside labour-heavy services, both in the basket.

## Consolidated (2026-11-06)

Her setup from the explorer is now model B, the kept model (`STATE.md` decision 23, Log 18): fitted officially by
`code/fit_base.py`, stress-tested by `code/stress_B.py` and reported by `code/report_B.py`
(https://claude.ai/artifact/B9SmfZ8nbmTPQaSZTEHvir). The playground files above stay as the record of how it was found.

## While she flew (2026-11-06, evening)

Her go: "keep going or play around, ponder and test some extra ideas". The thread: the knife edge (the fitted economy sits
on the machine chain's ceiling, where land's share of a machine's cost goes to zero) and what could take it off.
Leads, not results; every number below is a fit's, from the files named.

- **Durables apart works for the wages, not the knife edge** (`results/fit_Bd.json`, STATE Log 21). Two goods, one
  machine: the durables wage is fitted (1.86) by a durables clock of 8.3% a year against 5.8%; the original five improve
  (2.00 -> 1.85); durables' share of spending falls 0.19 -> 0.137 untargeted (record 0.13). Off the ceiling the original
  five cost 8.9 (one good 11.1). The rent floors (`compare_floors.py`): two goods are cheaper at low floors (10%: 5.1
  against 6.4) and no better at the record's 18.5% (9.2 against 8.5).
- **A 1995 wave on durables' clock alone** (`results/fit_Bd95.json`): no gain (1.856 against 1.848, two more numbers).
- **Progress through hours only, outside durables** (`hours_only.py`): the other goods' land clock held still, the
  best fit is 15.6. The record needs land-saving progress, and in this model land-saving progress is exactly what takes
  land out of machines.
- **Land in use growing at a free pace** (`land_grows.py`, `fit_base --land-grows`). With the six targets and a 2%
  return the fit stays on the knife edge (1.45-1.76, land growing 0.4-1.1% a year). With the return free and the chain
  and the band as targets, the best six-target point (a local fit that gives up the band) is 1.51 (land growing 1.3% a year, about as fast as adults; the return 13%; the
  chain 14% and replacement 14% of gross output, both about right), still on the knife edge. Off the ceiling (the chain
  and the band for fixed rents as targets) it fits at 2.5-2.7 with fixed rents near 0.3 and the chain right, but then
  machines hold most of the land (homes 1% to 29%) and land multiplies 7- to 19-fold.
- **The reading.** If a machine's fixed rents are land, as calibration (c) treats them, the record's 30% would put most
  land in machines; they do not hold most land. The record's fixed rents are mostly imported content and business
  surplus (BEA: imported content 18-21%, surplus 16-19% of the machine bundle, 1997-2023, steady while machines improved
  enormously): a share of a machine's value, not a quantity of land. So the knife edge in land may not be the model's
  failure but its reading: automation limited by the machine chain's own costs, land a negligible part of a machine.
  Next lead: the record's imported content as a value-share rent beside the machine's land (`value_rent.py`).
- **Land in use, from the record** (`land_ers.py`; USDA ERS urban area, `cache/ERS_urban_area_1945_2022.xlsx`): 2.7% a
  year 1949-1997, 1.5% a year 2002-2017 (the Census changed its definitions in 2000 and 2020; the path is built within
  them), x5.3 1950-2024, about twice adults' growth. The lead: land in use set from it, not fitted.
- **A value-share rent in a machine's cost** (`value_rent.py`; `two_goods.py` cmp["phi"], `fit_base --value-rent`): the
  record's imported content (0.20 of the machine bundle) as a rent priced with the machine, beside its land; the rent on
  each machine built is the owners' income (the income identity holds to 4e-16; the rent is 10% of income). With the
  return at 2% the six targets fit slightly better (1.80 against 1.85) and fixed rents sit at the record's floor by
  construction, but the chain and replacement stay at a third of pay and of gross output. With the chain's measured
  share as a target (domestic basis, 15%) the return rises to 6.8%, the chain falls to 19% and replacement to 20%, and the
  six targets cost 2.80, mostly labour's share (5.1). Shrinking the chain to its measured size costs labour's share,
  whichever way it is done: the higher return that shrinks it raises capital's income.
- **Land in use from the record, fitted** (`land_ers.py` -> `playground/land_ers.json`). With the return at 2% (E1; 12 of
  13 starts agree) the six targets cost 2.09 (the main case 1.85) and the fit leaves the ceiling (the task line 0.09
  under it in 2023). The steady clock falls to 0.2% a year: the 1948 wave (about the main case's size) and land in use
  carry the growth; durables' clock 3.1% a year. Machines are then made without machines (a at its floor: machines' share
  of a machine's cost 0.001, the record's 0.28), land is about half a machine's cost (0.53; the record's fixed rents
  0.18-0.38) and machines hold about half the land; the site's share of spending is 10% (the main case 0.3%; housing,
  structures included, 11-16% in the record). With the chain as a target too (E2) the return rises to 9%, the chain and
  replacement fall to 14% (record 15% and 16%), and the six targets cost 2.11. Which land the model's T stands for is
  open: urban land (x5.3 since 1950) or all land in use (about flat, farmland included).
- **The two-good main case under the stress battery** (`stress_B.py --base fit_Bd` -> `results/stress_Bd.json`, 47
  fits). It is better pinned than one good. The clock's profile has a floor at 5.8-6.1% a year (4.4% costs 3.2, 9.5%
  2.2; one good's was flat, 2.0-2.5 from 2% to 12%), and below 3% a second basin where hours per task carry the progress
  (the clock 1.7-2.3%, hours per task 4.1-4.3% a year, 2.5). Leaving out the goods wage, the shelter wage or employment
  leaves the fit where it was, so the others predict them (one good moved to 3.6, 246 and 22); theta_V is still needed
  (13.3 without it; one good 95). Out of sample, fitted to 1995 and read after: 9.5 (one good 21.6); fitted to 1985: 46
  (one good 16). The same pieces earn their place: women's entry (4.37 without), the basket (6.20), the utility's rise
  (flat 3.15; held after 1970 2.49), the wave (2.52 without; from 1945 1.85, from 1952 1.96). As good or slightly better
  at no extra cost: the utility through the real wage every year (1.80), the Cobb-Douglas basket (1.81), the cap
  (1.81), a 3% return (1.84). One readout is worse than one good's: the site's share of spending, 0.3% against 1.4%.
- **Imported content and growing land together** (`rent_and_land.py` -> `playground/rent_and_land.json`; the value-share
  rent 0.20, the chain's share of pay a target, the return free). With land growing at a fitted pace (C1: 1.3% a year, a
  little faster than adults) the six targets cost 1.53 (the main case 1.85; the same without the rent 1.51) and every
  measured part of a machine's cost lines up: pay 48% (record 47%), machines 32% (the panel's median 28%), imported
  content 20% (set), land nil; the chain 14% of pay (record 15%), replacement 14% of gross output (16%); the site 3.4% of
  spending (the main case 0.3%). The shelter wage gains most (0.76 against 2.75). Still on the ceiling, with the return at
  12.3% (NIPA's split implies about 8%) and the clock at 21% a year, hours per machine rising almost as fast (21.0%):
  hours per unit of task capacity fall 0.35% a year, as in the main case (0.33%), and on the ceiling that difference is
  what the economy feels, so the clock's own pace is not pinned there. With land in use from ERS instead (C2) the rent
  takes part of land's share and changes nothing else (2.12; land and the rent 0.53 of a machine's cost together).
- **Set from the record, the chain read rather than fitted** (`set_from_record.py` -> `playground/set_from_record.json`;
  the six targets only). The rent at imported content's 0.20, the return at NIPA's 8%, land in use growing with adults
  (D2: no free number beyond the main case's): the six targets cost 1.54 (the main case 1.85), and what the fit never saw
  comes out near the record: the chain 18% of pay (15%), replacement 17.5% of gross output (16%), a machine's cost 48%
  pay (47%), 32% machines (28%), 20% imported content and no land; the site 5.1-5.4% of spending (housing with its
  structures 11-16%). With land at a fitted pace instead (D1) the fit picks 1.26% a year, adults' own pace (1.27%), and
  costs 1.50. With the return free too (D3) the six targets lean to a low return (0.8%, 1.43) and the chain goes back to a
  third of pay, so the return is set by the chain, not by the six. Unchanged: the coverage ratio (2.4 against 4.3), the
  waterline (1.13 against 2.33) and the task line on the ceiling. Only two of four starts reach these fits; the clock and
  hours per machine both run at about 22% a year (their difference -0.30%); the wave shrinks (0.36 against 1.34; 0.04
  with land fitted). The calibrated 1950 starts, moved to these settings (`record_starts.py`), find 1.53 from one
  start of twelve (the next 1.66, with a slower clock, 11.6%, and a bigger wave; most near 2.4); without the wave 1.58
  from two (`record_case.py`). The six targets are indifferent to the return (4-12%: 1.50-1.56) and the rent
  (0.10-0.30: 1.53-1.55); the record pins both: the chain's 15% sits at a return of about 11%, replacement's 16% at
  about 9.5%, machines' 28% at a rent of about 0.25. `compare_cases.py record` prints the table.
- **The record-set fit out of sample** (`record_split.py` -> `playground/record_split.json`; scored as the stress
  battery scores it, the original five series, the inputs as measured, the utility's knots included). Fitted on
  1950-1995 and read on 1996-2024: 2.2 with the wave, 5.2 without (the two-good main case 9.5, one good 21.6). Fitted on
  1950-1985: 49 with the wave (the main case 46, one good 16), 6.7 without. Without the wave it is the first fit that
  holds from 1985; the wave, fitted on the early years alone, carries them badly into the later ones. In this fit
  machines in 1950 are about a third land (pay's share of a machine 0.18-0.32) and reach the ceiling by about 1970;
  the record's share starts in 1967. Figure: `record_plot.py` -> `playground/record_case.png`.
- **The reading, revised.** On the ceiling a machine's price is set by what goes into it (pay, machines and imported
  content) and moves with the wage, so automation's margin is set by the machine chain's own costs (the return,
  depreciation, the imported share, the hours in a machine), not by the labour market. Land, which the ceiling drives out
  of a machine's cost, is not visible in the record's split (at most part of the surplus, which is mostly the return on
  machines), and the split is steady from 1997 to 2023, as it would be on the ceiling. Once the rents in a machine's cost
  are read as value shares, the knife edge looks like the model's reading of the record rather than its failure.

## After the doc for Johan (2026-11-07)

Her lean on the wave ("Perhaps drop it yeah"), then: "do a bit more pondering and exploration, try more things".

- **The main case without the wave** (`results/fit_Br0.json`): 1.582 from five of fifteen starts (the wave fit 1.529
  from two). Nine fitted numbers; hours per unit of task capacity fall 0.44% a year from 1950, with no burst.
- **The machine chain's surplus is a normal return** (BEA input-output, the bundle's split, 1997-2023): at an 8% return
  and the measured depreciation rate, the return the chain's own capital earns (its depreciation times rho / delta) is
  its measured surplus to within -0.02 to +0.03 of a machine's cost (+0.01 on average). Imported content is the only
  rent in a machine's cost, as decision 25 set it. The dip in pay's share of a machine, 52.5% in 2001 to 44% in 2011, is
  the chain's capital share rising (24.5% to 30.5%), which a constant number of machines in a machine cannot follow.
- **Measured machine progress is the durables clock** (`hours_measured.py` -> `playground/hours_measured.json`). Hours
  of work per dollar of the machine bundle (BEA input-output, full chain) times the bundle's quality-adjusted price (BEA
  NIPA, private nonresidential fixed investment, B008RG) = hours per real unit of machine: -2.90% a year 1998-2023
  (x0.47). The fit's hours per unit of task capacity in durables: -3.00% a year (x0.47; the wave fit -2.80%, two goods at
  2% -2.89%), never targeted; in the other goods -0.44%. The wage over a unit of machine capability, read with durables'
  capability: 2.14-fold 1999-2023 against broad equipment's 2.33 (the old waterline miss, 1.13, read the other goods'
  capability). Forcing the other goods' pace towards the record's breaks the six (-1% a year 2.22, -1.5% 3.39, -2% 4.89,
  -3% 8.72, the goods wage 20 tolerances off; the clock's bound widened, no change). Equipment price indexes measure the
  capability durables embody; the six series say machines get better at everything else at a seventh of that pace.
- **What a capability jump would do to the 2024 economy** (`ai_jump.py` -> `playground/ai_jump.json`; all else equal,
  the basket's utility held). Other goods' tasks needing e^-s as much machine service: s = 0.1 / 0.25 / 0.5 / 1.0 move the
  task line 0.797 -> 0.811 / 0.834 / 0.873 / 0.956, the wage over goods x1.04 / 1.12 / 1.27 / 1.75, prime-age employment
  0.79 -> 0.80 / 0.83 / 0.87 / 0.98, labour's share 0.474 -> 0.457 / 0.429 / 0.369 / 0.173, the machine chain's share of
  pay 0.18 -> 0.19 / 0.21 / 0.25 / 0.49, the return on machines 0.32 -> 0.33 / 0.35 / 0.39 / 0.52 of income, land rent per
  adult over the basket x1.09 / 1.24 / 1.62 / 3.63. Wages and employment rise, labour's share falls, income moves to the
  owners of machines and of land, and workers move into making machines. If hours in a machine rise with the capability
  (lambda times eta unchanged) nothing changes on the ceiling, as the identification says. With the basket's utility
  following the real wage, as along the fitted history (a fixed point), the goods side is unchanged (on the ceiling it is
  set by technology alone) and land takes more: at s = 0.5 the wage over goods is still x1.27 but over the whole basket
  x1.09 (held utility: x1.18), land rent per adult over the basket x1.41, employment 0.83; at s = 1, x1.75, x1.22, x2.68,
  0.88. As living standards rise the demand for land takes part of the gain to wages: the site takes the gains.
- **A change of pace** (`kinks.py`; fit_base `KINKS`, one fitted number per year, both goods). After 1973: 1.506
  (-4.8%), the pace 1.58% a year before and 0.35% after, the productivity slowdown's direction; after 1995: nothing
  (1.576); both: 1.491 (-1.71%, -0.16%, -0.46%); after 1960: nothing. The 1973 kink beats the 1948 wave (-3.4% for two
  numbers) with one number; neither earns its place by the 20% rule.
- **The slow clock is services** (`services_split.py`, BLS CPI via FRED: CUUR0000SAN nondurables, CUUR0000SASLE services
  less rent of shelter; `playground/services_split.csv`). The wage over durables x4.49 1957-2024, over nondurables x1.65,
  over all but shelter x1.55, over services less rent of shelter x0.78: an hour's pay buys fewer services than in 1957.
  1973-1995 is the low in every one (services -1.85% a year). The fit's other goods average a moderate nondurables clock
  and a services clock with no headway against labour; a third good would show it.
- **The land-rent miss is not the basket's elasticity** (`results/stress_Br.json`): rent on housing land per adult over
  the basket's cost, 1953-2024, is 2.68-fold at 0.636 (the elasticity on the goods wage's own price basis), 2.58 at 0.75,
  2.48 at 0.875, 2.36 at 1, 3.14 with a fixed basket, against the record's 4.33.
- **No 1950s benchmark yet.** The two readings of the 1950s (a technology burst, or machines shedding land) differ in
  pay's share of a machine's cost before 1967; the λ thread's century arc has rows for 1947, 1958 and 1963 but no
  compensation for them. BEA's historical industry accounts (1947 onward) could supply it: a lead.

## Services apart (her go, 2026-11-08: "go ahead with services, and update the explorer as you go")

- **Design.** Three goods, one machine, one wage and one land market: durables, nondurables and services (less rent of
  shelter), each with its own clock, all equal in 1950 (services differ from nondurables only in pace, as durables do).
  The other goods are a nest of nondurables and services inside the durables composite. The nest is Cobb-Douglas with
  services' spending share set from the record each year (BEA's NIPA file, the panel's `srv_in_rest`, 0.39 in 1950 to
  0.72 in 2024): the share regression gives an elasticity of -0.69 (services' share rose fourfold against nondurables'
  while their relative price only doubled), which no constant-taste CES can produce. No free number for the nest; one for
  services' clock. With services on nondurables' clock the model is the main case to 1e-15 (`check_two_goods` S1).
- **Data.** The panel gains nondurables' and services' shares of spending on all but housing (BEA's NIPA file; FRED has
  no annual copy under the ID tried, `DNDGRC1A027NBEA` returned 404, and BEA's own file matches the panel's FRED series to
  the dollar), and the linked hourly earnings over the CPI for services less rent of shelter (CUUR0000SASLE, 1957 = 100)
  and for nondurables (CUUR0000SAN, complete from 1956, 1957 = 100). Existing columns unchanged; `check_panel` 31/31.
- **Services targeted alone** (`playground/fit_Bs_services_only.json`, 1.906 over seven series) the fit automated
  nondurables fully by 2010 and de-automated services (61% of tasks in 1957 to 39% in 2024): the wage over nondurables,
  never seen, came out at 308 in 2024 against the record's 165 (40 tolerances as a target).
- **All three wages targeted** (`results/fit_Bs.json`, `fit_base --services`): 2.268 over eight series; the original six
  2.21 against the main case's 1.58 (goods wage 2.60, shelter 1.29, labour's share 2.42, employment 2.79, theta_V 2.32,
  durables 1.84); nondurables 1.60, services 3.28. Hours per unit of task capacity: durables -3.15% a year (again near
  BEA's -2.9% for machines), nondurables -1.62%, services +1.25% (machines lose ground at service tasks: services' task line
  0.68 in 1950, 0.76 about 1960, 0.66 by 2024). Services' 1950 level freed (`s0_srv`, `playground/services_tests.py`): no
  gain (2.30; services start slightly more automated).
- **The reading.** The record's wage over services fell to 0.78 of 1957's: services' prices rose 28% faster than the
  production wage. In this model a good's price can rise against the wage only as machines lose ground at its tasks, and
  even so the fit misses it (most in 1973-1990) and pulling services that way costs labour's share and employment. Services
  apart does not earn its place; the main case stays two goods. The services price needs a channel the model lacks: most
  likely the wage of the people who make services rising faster than the production wage (the skill premium in health and
  education: the old split into two kinds of workers), or costs in services other than labour.
- **The explorer, v5** (`explorer/`, published at its usual link): the goods model in JavaScript (`model.js`: two_goods'
  economy line for line, the value-share rent, land with adults, services apart), presets `fit_Br0` (main), `fit_Bs`
  (services apart), `fit_Br` (with the wave); dials for each good's hours per unit of task capacity, the imported share
  and land with adults as set values; charts for the durables, nondurables and services wages, each good's task line,
  the machine chain and depreciation against the record, hours per unit of task capacity by good against BEA's hours per
  quality-adjusted machine, the shares of spending and of income. `check_explorer`: the JavaScript reproduces every
  preset to 1e-11 (two goods) and 2e-8 (services: the knife edge amplifies last-bit differences in the power function).

## Services by skill: a data look (her question, 2026-11-08: "do a worker for each good yeah. and can you split services into low and high skill? What do you think of that idea?")

`playground/services_skill.py` (output in `services_skill.txt`, the group series in `services_skill.csv`). Data only, no
model: BEA's consumer spending by type of service (NIPA 2.4.4 and 2.4.5, the repository's flat file, 1959-2024) and BLS's
hourly earnings of production and nonsupervisory employees by industry (CES via FRED, 1964-2024; transportation 1972).
Groups are a first guess by who does the work: high (hospitals and nursing homes, outpatient care, education,
professional services, finance, insurance), low (food services, accommodations, recreation, personal care, household
maintenance, vehicle repair, public transportation, social services), and goods-like services (utilities,
communication, nonprofits' own consumption).

- **The rise sits in high-skill services.** Price over the production wage, 1959 = 1, by 2024: high 1.39 (1.08 in 1980,
  1.45 in 1990, 1.52 in 2010), low 0.91, goods-like 0.38. Low-skill services' prices tracked the production wage for 65
  years. Largest rises: education 2.52, hospitals and nursing homes 2.12, professional services 1.82, insurance 1.45;
  outpatient care only 1.07, finance fell (0.70). The high group's share of services less housing rose from 34% to 53%.
- **Pay explains most of it over the whole period, little of the 1980s.** High group, 1964 = 1: price over the production
  wage 1.38 by 2024; its industries' pay over the production wage 1.27 (education and health 0.79 to 1.04 of the
  production wage, finance 0.90 to 1.19); price over its own pay 1.09. But in 1980-1990 the price rose from 1.07 to 1.44
  while pay rose 1.01 to 1.15: price over own pay peaks at 1.26 (1990-2000). Health care alone: price 1.50 (peak 1.84),
  own-pay price 1.14 (peak 1.47 in 2000). Education is the outlier: own-pay price 1.98 by 2024.
- **Per-good pay changes the low side's reading.** Low group from 1972: price 1.02, pay 1.23, own-pay price 0.83 (machines
  gaining ground). From 1964 (without public transportation) pay rose 1.65x, most of it by 1973 (1.29x), the years the
  federal minimum wage was extended to restaurants, hotels and hospitals (the 1966 amendments): some pay gaps are
  institutions, not markets.
- **What these pay series miss.** BLS's are nonsupervisory hourly earnings: no physicians in their own practices, no
  managers. BEA's all-employee pay per full-time equivalent by industry is in the flat file only from 1998 (table 6.6D);
  over 1998-2024 it shows high-skill services flat against the private average (hospitals 1.03 to 1.06, outpatient care
  1.25 to 1.02, education 0.77 to 0.74; finance 1.58 to 1.74). Its older tables (6.6B, 6.6C) were not reachable at BEA's
  download paths (the historical workbook path returns BEA's not-found page; BEA's site notes it is not being updated
  during the lapse in appropriations). Not sought elsewhere, per her rule.
- **Job shares against pay** (share of private jobs, 1964 to 2024; pay over the production wage): manufacturing 33% to
  10% with pay 0.95 to 0.92; education and health 7% to 20% with pay 0.79 to 1.04; professional and business 8.5% to 17%
  with pay 1.25 to 1.18; retail (from 1972) 13% to 12% with pay 0.90 to 0.69. Pay gaps did not follow job shifts in any
  one direction: a single mobility elasticity would be poorly pinned by this record.

## Services by skill and a worker for each good (her go, 2026-11-08: "go ahead with step 1, BLS is fine for now")

- **Built.** Four goods, one machine: durables; nondurables with the goods-like services (utilities, communication);
  low-skill services; high-skill services (the data look's groups; nonprofits' own consumption left out, an accounting
  remainder). Each services group has its own clock's pace (`g_low`, `g_high`), all equal in 1950; the nest is
  Cobb-Douglas at the record's shares each year (`two_goods.rest_skill`). BEA's file carries every type of service from
  1929, so the split runs from 1950, not 1959 as first said.
- **Targets on the CPI's level.** BEA's and the CPI's prices drift apart: the wage over BEA's prices of everything but
  housing ends 17% above the panel's CPI-based wage by 2024 (over durables 84% above). So each group's wage takes BEA's
  prices relative to the other groups and the CPI's level for the three together (the CPI less shelter less durables, as
  `dur_rel_price` splits it); the groups' prices aggregate back to that level exactly (`check_panel` I13). Targets: the
  main case's six and the wages over the three groups (`wage_ndg`, `wage_low`, `wage_high`, 1950 = 100): nine series.
- **A worker for each good, three ways.** (a) As designed (`--pay record`): each good's pay moves against the production
  wage as its industries' did (BLS: durable and nondurable manufacturing from 1950; services' industries from 1964; equal
  in 1950). (b) Found when fitting: BLS's production wage is the average over every industry, services included, and (a)
  lets the model's average pay drift 21% above it by 2024. So (`--pay levels`) each good's pay is its industries' level
  against the production wage (1964: low-skill 0.47, high-skill 0.92, durables 1.10, nondurables 0.86), times one factor
  per year that holds the model's hours-weighted average pay at the production wage (`fit_base.solve_year`). (c) A lead
  (`playground/skill_distribution.py`): (b) with the goods' workers counting trade, transportation and utilities, whose
  pay fell from 1.13 to 0.86 of the production wage while their jobs grew from 11.7 to 28.8 million.
- **Checks.** Panel 37/37 (C7, I12-I15, S10 new); goods 23/23 (K1: one clock and one wage is the main case to 2e-15; K2:
  one services clock is services apart to 3e-15; K3, K6: pay at one is one wage bit for bit; K4: the accounts add up with
  each good's pay; K5: dearer high-skill workers make their services dearer and machines take more of their tasks; K6: the
  average held to 1e-13); fit 9/9; explorer 6/6.

| | misfit (series) | the main case's six | hours per unit of task capacity, a year: durables / nondurables / low / high |
|---|---|---|---|
| main case `fit_Br0` | 1.582 (6) | 1.582 | -3.00 / -0.44 (with services) |
| services apart `fit_Bs` | 2.268 (8) | 2.210 | -3.15 / -1.62 / services +1.25 |
| **split, one wage `fit_Bk`** | **1.787 (9)** | 2.005 | -2.93 / -1.85 / +0.28 / +4.68 |
| split, pay as designed `fit_Bkp` | 2.209 (9) | 2.372 | -3.30 / -1.94 / -0.54 / +2.85 |
| split, pay levels, average held `fit_Bkl` | 1.975 (9) | 2.040 | -2.65 / -1.89 / -0.93 / +4.31 |
| lead (c), with trade and transport | 2.035 (9) | | -2.75 / -1.77 / -1.13 / +3.34 |

- **The split with one wage** fits low-skill services almost exactly (0.52: their hours per task capacity are flat, their
  task line steady at about two-thirds), nondurables at 1.30, high-skill services at 2.23 (services apart: 3.28). But it
  leans on corners: durables fully automated from 1997, nondurables from 2023, and high-skill services' task line falls
  from 0.58 in 1960 to 0 in 2020, machines losing ground at 4.7% a year. By 2024 the model has no hours in goods (25% in
  low-skill services, 57% in high-skill, 18% making machines), while about 30% of private jobs are still in manufacturing,
  trade and transportation. On the main case's six series it is worse than the main case (2.01 against 1.58).
- **Each good's pay does not help, in any form tried.** As designed it halves the needed loss of ground in high-skill
  services (+2.85% a year; their task line 0.58 to 0.48, no corner) but the model's average pay ends 21% above the
  production wage, costing labour's share and employment. With the average held, high-skill workers keep almost none of
  their relative gain (1.19 of the average in 1950, 1.20 in 2024): as hours move into high-skill services the average
  itself rises, and the record's offsets (falling pay in retail and transportation, the growth of low-paid leisure and
  hospitality jobs) are outside the model's four goods or, counted in the goods' pay, too small. In every version
  low-skill services' pay rises faster than their prices (+58% against about +25% over the production wage since 1964;
  the leisure and hospitality jump of 1964-1973 coincides with the 1966 minimum-wage extension), which the model can only
  meet by having machines take their tasks.
- **Open.** The corners suggest a target the record has: each good's share of hours against the record's jobs by
  industry. And pay from the model (step 2) is still what the forward model needs.
- **Explorer v6** (published, version 9): presets for the split with one wage, with pay at levels, with pay as designed;
  dials for each services group's hours per unit of task capacity; a switch for each good's pay; charts for the three
  groups' wages, four task lines, each good's pay and the average; `check_explorer` 6/6 (1e-8 or better).
