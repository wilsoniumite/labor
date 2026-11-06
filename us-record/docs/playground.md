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
