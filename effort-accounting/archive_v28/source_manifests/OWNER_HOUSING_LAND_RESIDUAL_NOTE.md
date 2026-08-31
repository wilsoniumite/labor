# Owner-housing land/site residual note

Date: 2026-08-21

## What is now identified without a capitalization assumption

The Federal Reserve publishes a matched pair for the household owner-occupied housing sector:

- owner-occupied real estate at market value;
- household residential structures at current cost, sourced at year-end from BEA Fixed Assets Table 5.1, owner-occupied line.

Therefore the stock residual

`site/land value = owner-occupied real-estate market value - current-cost residential structures`

can be calculated directly.

This is materially cleaner than subtracting a broad economy-wide residential structure stock from household real estate.

## What it shows

The residual is small in the early postwar data and becomes a large share of owner-occupied property value later. In the modern years:

- 2022: real estate $40.10T; structures $26.52T; residual $13.58T.
- 2023: real estate $42.90T; structures $27.00T; residual $15.90T.
- 2024: real estate $45.00T; structures $27.91T; residual $17.09T.
- 2025: real estate $45.99T; structures $28.95T; residual $17.04T.

The 2025 residual is about 37% of owner-occupied real-estate market value.

## Why this does not finish Graph D

The residual is a **stock value**, while Graph D ultimately needs an **income/service flow**.

It would be tempting to multiply the residual by an arbitrary capitalization rate, or to allocate gross imputed rent in proportion to land and structure values. We do not do that here.

Instead, D3 reports a stock/flow diagnostic: site-value residual divided by annual imputed owner-housing services. This shows how large the site-value stock has become relative to the service flow without pretending that the ratio is itself a site-rent yield.

The paper already uses Z.1 market-value-minus-replacement-cost residuals under capitalization-rate variants for its site-rent coverage exercise. For the consumption-origin graph, we should preserve the same sensitivity discipline rather than hard-code one rate.

## Next step

There are now two defensible choices for the owner-housing branch:

1. carry `site/structure split unresolved` in the main Graph D and show D2 as a supporting stock diagnostic; or
2. import the paper's exact capitalization-rate grid into this ledger and report a band for site-rent flow rather than a point estimate.

Until the paper's exact rate grid is recovered, choice (1) is safer.
