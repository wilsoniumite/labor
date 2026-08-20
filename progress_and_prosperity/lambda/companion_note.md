# The Labor Content of Machine Production: United States 1967–2023, World 1995–2022

*Data note / short empirical paper — working draft, 2026-08-20. Working
title vetoable. Companion to "Pinning the Wage to Scarcity and Technology"
(P1), written to be citable independently of it: every construction below
is accounting on published statistics, and the falsification reading is
stated in both directions. Figures: `figures/lambda_delivery_fig1.png`,
`figures/lambda_delivery_fig2.png`. Register: measurement note.*

## Abstract

We measure the labor content of machine production — the labor
compensation embodied in one dollar of machinery final output, resolved
through published input-output total requirements — for the United States
(annual 1997–2023; SIC-era benchmarks back to 1967, spliced with the
classification step stated) and for the world (three inter-country IO
releases, 1995–2022, labor collected wherever it accrues). The series
falls everywhere measured: the US share declines from roughly 0.68 (1982,
spliced) to 0.55 (2023), on 100% of a six-member classification grid; the
world share falls on twelve of twelve grid members across three
independent releases (about 0.56 to 0.48, 1995–2022). Decomposition shows
the decline sits on the quantity side: hours embodied — valued at the
economy-average wage to immunize against sector rents — fall in step,
while the embodied labor's relative wage is flat to rising; purging
industry labor rents (Stansbury–Summers) leaves the decline intact on
every member; and a within-country hours index, which removes the
relocation margin, falls faster than any value series (to 0.52 by 2009,
0.38 by 2014, 0.15 by 2022, per release). The pre-committed falsifier —
that a flat series would have refuted the recursive-automation channel —
did not bite.

## 1. The object

Machinery output at purchasers of final demand embodies labor directly and
through every upstream intermediate. The object is the vertically
integrated labor-compensation share of one dollar of machinery final
output: v_w′ (I − A)⁻¹ f, the compensation row resolved through the
Leontief inverse — the one-sector λ of the machine-recipe closure
c = ac + λw + ℓr in its matrix form (Leontief 1936; Sraffa 1960; the
vertically integrated reading is Pasinetti 1973). The measure is a nominal
share: no deflator enters anywhere, which spares it the hedonic disputes
that attach to machinery quantities (Houseman, Bartik and Sturgeon 2015).
The motivation for measuring it — the claim that recursive automation
lowers λ and thereby decouples wages from machine costs — is P1's; nothing
below depends on accepting that claim.

Machine sets run as a grid, never a single pick: narrow (machinery;
computer and electronic products; electrical equipment — NAICS 333–335 /
ISIC C26–C28 / SIC 85-order 43–58), medium (+ software and IT services),
broad (+ leasing), with import treatment (total vs domestic requirements)
as a second axis. All headline statements are medians with min–max bands
across the grid.

## 2. Construction, verified rather than assumed

**United States (annual, 1997–2023).** BEA make–use framework after
redefinitions, producers' prices, summary level. The published
industry-by-commodity total requirements are used directly; the
construction W(I − BW)⁻¹ from the published Make and direct-requirements
tables reproduces them to 1.3e-04 (the reconstruction gates every year),
and the domestic variant (proportional import purge) is built only on the
verified matrices. Two closed-form identities hold to machine precision
throughout: the unit-cost identity (intermediates + value added = 1 per
industry, ≤ 1.1e-06) and the exact full-VA resolution of every commodity
through the published inverse (≤ 1.4e-06).

**United States (benchmarks, 1967–1992).** Nine historical benchmark
vintages parse (1947–1992); the compensation split exists at the 85-order
level from 1967 (earlier vintages carry only total value added and are
dropped, not imputed). Identification is self-verifying: value-added
blocks matched to revised GDP (with per-vintage unit scales detected),
compensation as the dominant component, and — where the retrospective
industry accounts allow (1987, 1992) — external cross-checks at 0.9% and
0.7%. Published total requirements exist for every vintage. The
1992→1997 SIC→NAICS splice is a ratio link of 0.9204, stated wherever the
spliced series appears; both within-segment directions agree in sign, so
the splice carries no conclusion. BEA's caveat that the historical
benchmarks "should not be used as a time series" rides with the points.

**World (1995–2022).** Three independent inter-country systems: WIOD 2013
(1995–2009 with sourced labor), WIOD 2016 (2000–2014), OECD ICIO 2025
(1995–2022), each inverted globally (up to 4,041 country-industries), with
labor compensation and hours from the WIOD socio-economic accounts
(currency handled by dimensionless shares). The closed world table makes
the resolution identity exact, and it holds at ≤ 8e-15 on every kept year.
Cross-release agreement on overlap years: WIOD 2013 vs 2016 within 0.019;
ICIO vs WIOD 2016 within 0.031. Honest labels carried in the data: ICIO
2015–22 runs on labor shares frozen at 2014 (structure-only; it agrees in
sign with sourced members); countries without labor accounts (incl. the
rest-of-world block) ride a zero-to-mean band; WIOD 2013's 2010–11 are
excluded at 24% labor coverage; the ICIO 2006–10 block is pending.

**Diagnosis layers.** Hours enter as a block-level row vector (28
BEA↔ISIC blocks; the bridge covers the requirement mass exactly) with
levels from the WIOD accounts and tails extended by the BEA–BLS KLEMS
index; the decomposition λ̂ = H_rel × w̄_rel is exact by construction.
Labor rents by industry are Stansbury and Summers' (BPEA 2020,
published replication; their machinery industries map one-to-one), with
Acemoglu and Restrepo's (2026) estimate for automated jobs — rents about
35% [19–44.5%] — as a level benchmark. Forty-four checks across four
gating batteries are green; every number here is produced by the scripts
in §6.

## 3. Results

**The spine falls (Fig. 1).** The US share: 0.582 (1997) → 0.547 (2023)
on the narrow total-requirements member; 2023 band [0.471, 0.578] across
the six-member grid, median 0.541; spliced back, 0.681 (1982) → 0.547
(Δ −0.134 over the automation era), with the SIC benchmarks alone falling
1982→1992 and the annual series falling 1997→2023 — every member of every
window negative. The world share: 0.554 (2000) → 0.527 (2014) on WIOD
2016; 0.560 (1995) → 0.497 (2014) → 0.481 (2022, frozen-share tail) on
ICIO; twelve of twelve sourced members decline (median −0.044/decade).

**The decline is quantity, not price (Fig. 2a).** US hours embodied at
the economy-average wage: 0.514 → 0.482 (1997→2023), falling on all six
members; the embodied labor's relative wage w̄_rel is flat to rising
(1.13 → 1.14). Purging industry labor rents leaves the decline on 100% of
members (−0.035/decade, 1997–2016) even as machinery rents themselves
eroded (ρ 0.139 → 0.104) — the fall is not rent dissipation wearing an
automation costume.

**Within countries, hours collapse; relocation masked it (Fig. 2b).** The
raw world hours aggregate per dollar fell far less than its within-country
index — WIOD 2013: raw 0.92 vs within 0.52 by 2009; WIOD 2016: 0.49 vs
0.38 by 2014; ICIO: 0.09 vs 0.15 by 2022 — because production
simultaneously relocated toward low-wage, high-hours suppliers: the
foreign-labor share of US machinery purchases rose from 0.29 (1995) to
0.44 (2022). Within any given country's technology, the hours behind a
dollar of machinery fell by half to four-fifths over the windows measured.

## 4. The falsification reading, both ways

The criteria were committed before any series existed. Had the
compensation share held flat — or fallen only where rent purging or
fixed-composition hours could not follow — the recursive-automation
channel would have been refuted as measured: the wage bill would have
stayed inside the machine's cost base, and the closure resting on λ's
decline would have lost its mechanism. That is what a failure was defined
to look like, and no member of any referee produced it. Conversely, what
passing required — value and quantity legs falling together, on US and
world referees, surviving rent purging and composition repair — is what
every member shows. One committed timing caveat: the tables end 2022–23,
so the post-2023 wave of AI systems is not yet visible here; nothing in
this note is evidence about it, in either direction.

## 5. Caveats, in one place

Frozen-2014 labor shares on ICIO 2015–22 (structure-only, labeled); the
ICIO 2006–10 block pending; the 0.9204 splice step at the SIC→NAICS
boundary; no compensation split before 1967 (dropped, not imputed);
benchmark-vintage scatter (BEA's own time-series caveat); hours tails by
KLEMS index; the 28-block hours bridge; rest-of-world labor as a
zero-to-mean band; rents purged with Stansbury–Summers' definitions;
self-employment handled via the WIOD LAB variant on the world leg and
recorded as a deferred axis on the US leg; machinery-set membership as a
grid, software inseparable before the NAICS era.

## 6. Reproduction

BEA pulls run scripted (`pull_family_a.py`, `pull_century.py`; note the
TLS-interception fix via `truststore`); WIOD from DataverseNL
(`pull_family_b.py`); ICIO data zips require a manual browser download
(the OECD file host refuses scripted clients) into `data/cache/`.
Compute: `compute_family_a.py`, `compute_century.py`,
`compute_family_b.py`, `compute_icio.py`, `compute_us_hours_rent.py`,
`compute_world_h_within.py`. Gates: the four `checks/check_*.py`
batteries (44 checks). The read: `gate_read.py`; its memo is
`READ_MEMO.md`. Derived series ship as CSVs in `data/`.

## References (verify-quote pass at final drafting)

Acemoglu & Restrepo 2018 (AER); 2026 "Automation and Rent Dissipation"
(QJE 141(2)); Houseman, Bartik & Sturgeon 2015; Kehrig & Vincent 2021
(QJE); Leontief 1936 (REStat); Pasinetti 1973 (Metroeconomica); Sraffa
1960; Stansbury & Summers 2020 (BPEA); Timmer et al. 2015 (WIOD); OECD
ICIO 2025 edition (rev. 2026-01); vom Lehn & Winberry 2022 (QJE); P1
working paper (SSRN, Aug 2026).
