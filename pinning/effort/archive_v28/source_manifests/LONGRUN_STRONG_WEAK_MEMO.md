# Long-run strong/weak evidence architecture

Date: 2026-08-26

## Decision

The project should keep the 1950–2025 horizon.

Missing historical detail will no longer force a shorter x-axis. Instead every long-run empirical object will be split into:

- **STRONG:** measured/official benchmark in the source-supported window;
- **WEAK:** transparent estimated extension outside that window, always shown with a distinct visual treatment and a specification/calibration band;
- **DIAGNOSTIC ONLY:** source data whose concept does not map cleanly to the paper's latent target.

This is a better fit to the research question than either pretending all years are equally measured or abandoning the long run.

## Long-run D-Q factor-content prototype

The strong middle window is the BEA full-upstream consumption benchmark for 1997–2023.

Outside that window, a weak compositional model uses the fully observed 1950–2025 NIPA product mix. Five parsimonious specifications are estimated only on the 1997–2023 overlap. Their spread, widened by in-sample RMSE, becomes the weak band.

The resulting **weak** human-effort backcast is approximately:
- 1950: **66.4%** of PCE, band 61.3–68.6%
- 1990: **50.7%**
- 2025: **46.2%**, band 45.1–47.4%

The strong BEA benchmark itself is roughly:
- 1997: **50.1%**
- 2023: **47.2%**

This gives a plausible long-run decline in production labor content, but **only 1997–2023 is source-supported as the full-chain benchmark**. The earlier decline is an estimated compositional backcast and must be described as such.

## Long-run owner-land flow proxy

For owner housing, the evidence can also be made long-run without inventing an arbitrary capitalization rate.

- **Strong data window:** BLS owner-occupied land capital-cost allocation, 1987–2024.
- **Weak extension:** matched Fed/BEA owner-land stock residual × median 1987–2024 cross-system land-cost/stock ratio.
- **Weak band:** P10–P90 of that observed cross-system ratio, 2.67%–4.45%.
- Median calibration: **3.19%**.

This produces:
- 1950 weak owner-land user-cost proxy: **0.05% of PCE**
- 1987 observed BLS measure: **1.45%**
- 2024 observed BLS measure: **2.80%**
- 2025 weak extension: **2.60%**

The observed BLS series is "strong" only as a BLS user-cost object. It remains conceptually a proxy, not observed terminal scarcity rent. The weak extension is weaker still and is never called a capitalization-rate series.

## What strong/weak means in the final paper

A final figure can legitimately have:
- solid line: measured/official benchmark;
- dashed line: estimated continuation/backcast;
- shaded band: weak-specification or calibration uncertainty;
- footnote: concept mismatch where the measured object is still only a proxy for terminal rent.

The paper should not hide the weak section. The point is to make **where measurement ends and inference begins visually obvious**.

## Recommended headline architecture

### A / household resource origin
Strong modern anchors + weak historical extension if we build one.

### C / consumption product and route
Product spine is strong 1950–2025. Route resolution becomes weaker backward in time rather than disappearing.

### D-Q / production factor content
Strong full-chain benchmark 1997–2023; weak compositional extension to 1950–2025.

### Scarcity sub-panel
Strong long-run stock evidence; observed BLS user-cost window; weak stock-calibrated flow extension; no single series promoted to "terminal rent."

## Guardrail

A weak historical estimate is acceptable because it answers the long-run research question transparently. It becomes unacceptable only if:
- its estimated years are visually indistinguishable from observed years;
- the uncertainty band is omitted;
- or a proxy concept is silently renamed as the theoretical target.
