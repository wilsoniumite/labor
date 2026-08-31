# Major-product decomposition pass

Date: 2026-08-23

## What this pass does

The remaining consumption residual is now split into stable, mutually exclusive **major product families** using NIPA Table 2.3.5.

The detailed ledger contains the 16 leaf categories:
- four durable-goods categories;
- four nondurable-goods categories;
- seven household-service categories;
- NPISH final consumption.

For a readable paper figure, C28 collapses those to ten families while preserving the 100% identity.

## Full 1950–2025 axis without pretending every source has the same vintage

The direct current BEA `Underlying/Section2All_xls.xlsx` file supplies 1959–2025.
For 1950–1958, the pass uses the US-BEA GitHub `Section2All_xls.xlsx` snapshot.

This splice is unusually clean:
- at the 1959 join, the maximum difference across the 20 audited Table 2.3.5 series is **0.000000%**;
- by 2025, the maximum difference between the snapshot and current release is only **0.177%**.

So the 1950s bridge does not introduce a visible level break. The output still records the source vintage year by year.

## The long-run budget shift

Largest 1950→2025 share gains:
- Health care: +13.62 percentage points
- Financial services & insurance: +5.23 percentage points
- Housing & utilities: +5.08 percentage points

Largest share losses:
- Food & beverages (off-premises): -14.26 percentage points
- Clothing & footwear: -7.18 percentage points
- Durable goods: -6.08 percentage points

The important methodological point is that these are **product shares**, not financing origins. A category can become larger because its relative price rose, its real quantity rose, or both.

## Why this helps Graph D

Each product family now has a routing status:

- `advanced`: the project already has a dedicated accounting module strong enough to serve as a Graph-D branch;
- `partial`: relevant pieces exist but cannot yet be applied directly to purchaser-price PCE;
- `open`: a dedicated product/input look-through still has to be built;
- `open-mixed`: the product family is too heterogeneous and should be split before attribution.

The next Graph-D work should therefore be targeted rather than generic:
1. energy goods;
2. food/agriculture;
3. other household services, especially transport/accommodations;
4. purchaser-price bridge for manufactured goods (domestic value added + imports + trade margins + taxes).

## Important warning

The existing industry compensation-share pilot is **not** directly multiplied by these PCE shares.
PCE is at purchaser prices and can contain imported content, wholesale/retail margins, taxes, and inputs from multiple producing industries.
Industry value-added shares are useful only after a concordance/input-output bridge.

## Files

- `graph_C27_detailed_major_product_spine_1950_2025.csv`
- `graph_C27_source_join_audit.csv`
- `graph_C28_broad_product_families_1950_2025.csv/.png`
- `graph_C29_product_share_change_1950_2025.csv/.png`
- `GRAPH_D_PRODUCT_LOOKTHROUGH_REGISTRY.csv`
- `graph_D6_product_module_readiness_2025.csv/.png`
- `major_product_anchor_shares.csv`
