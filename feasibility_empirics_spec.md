# Feasibility empirics — spec (queue item 3, empirical half)

Object: κ(t) = rT / (N·P_s) for the U.S., annual, as far back as sources
allow — Prop 8's coverage ratio — plus the distance to the κ = 1 threshold.
(Referenced by `feasibility_section.html`; written 2026-08-05 after the
authoring session was cut off before it could produce this file.)

Status: FIRST PASS implemented and run 2026-08-05 — `code/feasibility_kappa.py`;
all 12 FRED series validated; results `data/kappa_results.csv`, figure
`figures/kappa_coverage.png`; κ(2025) = 0.33 [0.18–0.59], ≈0.05 in the 1950s.
IMPLEMENTED from the grid below: Z.1 residuals (household; economy-wide to
2020) × two cap rates; PCE-housing flow × {0.30, 0.50}; the two Orshansky-base
bundles. NOT YET IMPLEMENTED: the Larson/BEA land-value family (no FRED
series — needs a BEA table pull), farm rents and the property-tax split proxy,
the SPM and CE bundle variants, and the crossing-year output (vacuous while
κ < 1 everywhere). The published band spans the implemented members only; SPM
thresholds would plausibly widen it, and the stock side currently rests on Z.1
alone — the grid's own "never the sole source" rule is unmet until the
Larson/BEA member lands. (Coverage gap surfaced by the 2026-08-05 review pass.)

Method inherits §7's discipline verbatim: live public pulls only (FRED /
BEA / Fed Z.1), validation identities and magnitude anchors before use,
stop-and-report on unreachable series, every contestable classification
computed under all defensible variants, medians with min–max bands.

## Numerator — aggregate site-rent flow rT

Grid axis 1 (source), axis 2 (capitalization where a stock needs a yield):

1. BEA/Larson-style land-value estimates × capitalization-rate band
   (10y Treasury ± premium variants; Davis–Heathcote-style implied yields).
2. Z.1 land residual (real estate at market value minus replacement-cost
   structures, households + nonfinancial business) — include WITH the
   post-1995 unreliability caveat as a band member, never the sole source.
3. Flow-side lower bound: NIPA housing gross rents (imputed + tenant) ×
   land-share-of-property variants, plus farm land rents; nonresidential
   site rent proxied through property-tax base splits. Flagged lower bound.

Blocking decision resolved 2026-08-05 under delegation: no single-source
pick — all defensible variants through the rule grid, bands reported.

## Denominator — N·P_s

- N: resident population, annual average.
- P_s variants (axis 3 — κ needs only the bundle's COST):
  1. Census/HHS poverty thresholds (single person; per-capita family-of-4).
  2. Supplemental Poverty Measure thresholds.
  3. CE bottom-quintile essential spending (shelter + utilities + food).

## Outputs

- κ(t) median with min–max band; shorter subperiods where a member's source
  starts late; κ = 1 line marked.
- Implied threshold-crossing years per variant.
- One figure + one row for §7's table; candidate prediction: κ trends up
  along the demolition (Prop 8's "the demolition funds its own remedy").

## Conventions

- Gross flows, consistent with §7's data note; κ is current-dollar ratio,
  deflator-free by construction.
- Cache under `cache/`; script `code/feasibility_kappa.py` (to be written
  in the computing session); results to `data/`, figure to `figures/`.
