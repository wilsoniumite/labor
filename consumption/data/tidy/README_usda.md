# USDA ERS Technical Bulletin 1929 (Working/Florida demand system, 2005 ICP): tidy files

Built by `consumption/code/acquire_usda.py` from the raw files in `consumption/data/raw/usda/` and nothing else.
Run it from the repo root with `venv/bin/python -I consumption/code/acquire_usda.py`. Vendored files are never
downloaded again, so a rerun is offline and takes about 20 s (`--offline` skips the network check entirely). It
rebuilds every file below byte for byte: two clean reruns gave identical sha256 for all 8 outputs. The script stops
with an error if any `consistency` check fails. Every check it runs is in `usda_tb1929_checks.csv` (456 rows), and the
numbers quoted below come from that file.

Source: Andrew Muhammad, James L. Seale, Jr., Birgit Meade and Anita Regmi, *International Evidence on Food
Consumption Patterns: An Update Using 2005 International Comparison Program Data*, USDA Economic Research Service,
Technical Bulletin 1929 (TB-1929), March 2011, **revised February 2013**. Below, "TB-1929 p. N" is the bulletin's
printed page; the PDF page is printed page + 6 in the body.

## 1. What was vendored (`raw/usda/`, 17 files, all pulled 2026-11-02, no failures, no blocks)

| File | What |
|---|---|
| `report/tb-1929.pdf` | The bulletin, 59 pages, the revised version (PDF created 2013-02-12; abstract: "revised in February 2013 to correct the ordering of country names in the appendix tables. Additional clarifications to the data and estimation methods used were added to pages 1, 11, and 18"). The post's link (`.../_laserfiche/publications/47579/7637_tb1929.pdf`) served **byte-identical** content on 2026-11-02 (sha256 `d7db892a...67a9`), so it was not vendored twice. |
| `report/tb-1929-report-summary.pdf` | Two-page summary (modified 2013-02-13). Used only to confirm the category lists. |
| `report/download-tb1929.zip` | "TB1929.zip": `readme.txt` plus the four figures as PNG (March 2011). It holds no tables or data. Inventoried, not parsed. |
| `report/pub-details_47581.html` | The publication page (date 3/22/2011; lists the three downloads above). |
| `dataproduct/*.xls` (9 files) | ERS data product *International Food Consumption Patterns*, 2005 files. These are the bulletin's appendix tables 1-8 (sheets `Table1`-`Table8`) and its Table 2 (sheet `Table9`). Last updated 9/4/2013 (Table 2 file: 2/11/2011). They carry more digits than the PDF: per capita income to 14 significant digits, and the food-subgroup tables to 6 decimals. |
| `dataproduct/international-food-consumption-patterns.html`, `dataproduct/documentation.html` | The data product page (updated 12/31/2025: "This data product is no longer being updated") and its documentation page (scope, categories, estimation procedure). |
| `supplement/tb-1937.pdf`, `supplement/pub-details_47611.html` | TB-1937 (Meade, Regmi, Seale and Muhammad, January 2014), ERS's companion report on the same 2005 ICP data. The documentation page cites it as a source report. Used **only** for category definitions that TB-1929 does not spell out. TB-1937 states that its elasticities use TB-1929's Table 3 parameters, and none of its numbers enter the tidy files. |

Not vendored:
- the data product's 1996 ZIP, which is the earlier TB-1904 round and a different ICP vintage;
- the Amber Waves article;
- TB-1937's summary and ZIP;
- the World Bank's 2005 ICP report, which defines the ICP basic headings. It is another publisher and outside this source family. See section 7 for what that leaves open.

## 2. Coverage

- **One cross-section, 2005.** The model is estimated across countries, not within them. The 2005 ICP has 146 countries. ERS drops Greece (not available at the basic-heading level) and Comoros (excluded), which leaves 144. Egypt and Russia were reported twice and averaged (Tables 3-4 notes).
- **Outliers.** 19 countries were found to be outliers by an information-inaccuracy measure. The parameters were estimated on the other 125, and elasticities were then computed for all 144 (TB-1929 p. 11 and footnote 11). The 19 are flagged in `usda_tb1929_countries.csv`; Finland and the United States are not among them.
- **Income groups.** Groups are set by real per capita income relative to the US: low < 15% (77 countries), middle 15-45% (38), high >= 45% (29). The appendix group headers match these thresholds for all 144 countries.
- **Countries in every appendix table, listed by ascending per capita income:**
  - lowest: Congo, Dem. Rep., at 0.48% of US income;
  - highest: the United States, at 100%;
  - Finland: 56.2% of US per capita income and 70.9% of US per capita food spending (country order 122).

## 3. The model as printed (equations transcribed from the page images)

Notation: `i` is a good, `c` a country, and `w_ic` the budget share. Every equation was transcribed from the page rendered at 300 dpi. The text extraction garbles subscripts, so it was not used for the equations.

**Stage one: Florida-Preference Independence (Florida-PI) model, nine broad groups** (TB-1929 pp. 6-8, PDF pp. 12-14)

- (1), p. 6. Working's model:
  `w_i = E_i / E = alpha_i + beta_i log E + eps_i`, where `E = sum_i E_i` is real aggregate expenditure.
- (2), p. 7. Adding up:
  `sum_i alpha_i = 1;  sum_i beta_i = 0`.
- (3), p. 7. Marginal share:
  `theta_i = dE_i / dE = alpha_i + beta_i (1 + log E) = w_i + beta_i`.
- (4a)-(4d), p. 7. The Florida-PI model:
  - (4a) `w_ic = LINEAR + QUADRATIC + CUBIC + eps_ic`
  - (4b) LINEAR, the real-income term: `alpha_i + beta_i q_c`
  - (4c) QUADRATIC, the pure-price term: `(alpha_i + beta_i q_c) [ log(p_ic / pbar_i) - sum_j (alpha_j + beta_j q_c) log(p_jc / pbar_j) ]`
  - (4d) CUBIC, the substitution term: `phi (alpha_i + beta_i q_c*) [ log(p_ic / pbar_i) - sum_j (alpha_j + beta_j q_c*) log(p_jc / pbar_j) ]`
  - The symbols, as defined on p. 7:
    - `q_c` is "the natural logarithm of Q_c, which is a measure of real per capita income";
    - `q_c* = 1 + q_c`;
    - `log pbar_i = (1/N) sum_c log p_ic` is the geometric mean price;
    - `phi` is "the income flexibility coefficient - the inverse of the income elasticity of the marginal utility of income".
  - The bulletin adds: "Since the quadratic and cubic terms vanish at geometric mean prices, the linear term is also the budget share at geometric mean prices."
- **(5), p. 8. Expenditure (income) elasticity:**
  `eta_ic = d log E_ic / d log E_c = theta_ic / wbar_ic = 1 + beta_i / wbar_ic`
  - "where, in this case, wbar_ic represents the budget share of good i at geometric mean prices, c represents the country, theta_ic is the marginal share of good i in country c, and beta_i is the estimated coefficient on q_c in the ith good equation."
  - Footnote 8: "Because expenditures in this instance are spending on all product categories, equation (5) is also referred to as the income elasticity."
- (6), p. 8. Frisch own-price elasticity:
  `F = phi (wbar_ic + beta_i) / wbar_ic`.
- (7), p. 8. Slutsky own-price elasticity:
  `S = phi (wbar_ic + beta_i)(1 - wbar_ic - beta_i) / wbar_ic = F (1 - wbar_ic - beta_i)`.
- (8), p. 8. Cournot own-price elasticity:
  `C = phi (wbar_ic + beta_i)(1 - wbar_ic - beta_i) / wbar_ic - (wbar_ic + beta_i) = S - (wbar_ic + beta_i)`.

**Stage two: conditional Florida-Slutsky model, eight food subgroups** (TB-1929 pp. 9-10, PDF pp. 15-16)

- (9), p. 9. Florida-Slutsky model:
  `w_ic = (alpha_i + beta_i q_c) + (alpha_i + beta_i q_c)[ log(p_ic/pbar_i) - sum_j (alpha_j + beta_j q_c) log(p_jc/pbar_j) ] + sum_j pi_ij log(p_jc/pbar_j)`.
  The text adds that the compensated elasticity is `pi_ij / wbar_ic`, the Cournot own-price elasticity is `pi_ij / wbar_ic - (wbar_ic + beta_i)`, and "the expenditure elasticity for the Florida-Slutsky model can be calculated at geometric mean prices using the formula given by equation 5."
- (10), p. 9. Conditional model:
  `wbar*_ic = alpha*_i + beta*_i q_gc + (alpha*_i + beta*_i q_gc)[ log(p_{i in Sg, c} / pbar_{i in Sg}) - sum_{j in Sg} (alpha*_j + beta*_j q_gc) log(p_jc/pbar_j) ] + sum_{j in Sg} pi*_ij log(p_jc/pbar_j)`.
  The symbols:
  - `w*_ic = w_ic / W_gc` is the conditional budget share of good `i` in group `S_g`;
  - `W_gc` is the budget share of group `S_g` in country `c`;
  - `q_gc` is "the log of real expenditures on group S_g";
  - `alpha*`, `beta*` and `pi*` are the conditional parameters; `pi*_ij` is the conditional Slutsky price parameter.
- Conditional expenditure elasticity (text, p. 9): `eta*_ic = 1 + beta*_i / wbar*_ic`. On p. 18 `wbar*_ic` is called "the conditional fitted budget share (at geometric mean prices)".
- **(11), p. 9. Unconditional expenditure elasticity:**
  `eta^U_ic = eta_Fc eta*_ic  for all i in S_g`
  - "the unconditional expenditure elasticity (eta^U_ic) is simply the conditional expenditure elasticity (eta*_ic = 1 + beta*_i/wbar*_ic) multiplied by the income elasticity of demand for food as a group (eta_Fc) obtained from the Florida-PI model (equation 5)."
  - Footnote 9: "The subscript Fc is used instead of ic since we are referring to the food group."
- (12), p. 10. Unconditional Frisch own-price elasticity:
  `F^u_i = (phi Theta_gc / Wbar_gc)(theta*_ic / wbar*_ic) = phi eta_gc eta*_ic`
  - `Theta_gc` is the group's marginal share;
  - `theta*_ic = theta_ic / Theta_gc` is the conditional marginal share.
  - Footnote 10: the unconditional and conditional Frisch elasticities are equal.
- (13), p. 10. Unconditional Slutsky price elasticity:
  `eps_ijc = eps*_ijc + Phi_gc eta*_ic eta*_jc w*_ic (1 - Wbar_gc eta_gc)`, with `eps*_ijc = pi*_ij / wbar*_ic` and `Phi_gc = phi Theta_gc / Wbar_gc`.
  - Transcribed as printed, with `w*_ic`. For `i != j` the textbook block-independence form carries `w*_jc`; the two coincide for own-price terms.
  - The bulletin publishes no table from (13) or (14) (p. 18).
- (14), p. 10. Unconditional Cournot price elasticity:
  `C_ijc = eps_ijc - eta*_ic w*_jc eta_gc Wbar_gc`.
- (15), p. 15 (PDF p. 21). Derivative of the Slutsky elasticity in income, used only to explain where the food Slutsky elasticity turns:
  `d log(S/phi) / Q_c = (-beta_i wbar_ic^2 + beta_i (1 - beta_i)) / [wbar_ic (wbar_ic + beta_i)(1 - wbar_ic - beta_i)]`.

**What the symbols are in the published tables.** All three points were verified numerically (section 6).
- `Q_c` is real per capita income relative to the United States (US = 1), and the log is natural. The slope of `1/(eta - 1)` on `ln Q_c` across the 144 food elasticities is 0.9991. TB-1937 p. 12 states the normalisation in words.
- `q_gc` is the log of real per capita food spending relative to the US. The data product calls it "Per capita food" and gives it for every country.
- `wbar` is the **fitted** share at geometric mean prices, `alpha_i + beta_i q_c`, not the country's observed share. The observed shares were used only where the fitted share was negative or near zero. Those cells are marked 'a' (section 7).

## 4. What stage two holds, and what it does not

**Stage one** has nine groups (Table 3 labels): Food, beverage, and tobacco; Clothing and footwear; Housing and utilities; Furnishing, household equipment, and maintenance; Medical and health; Transportation and communication; Recreation and culture; Education; Other.

The food group is "food prepared and consumed at home, food away from home, and beverages and tobacco" (pp. iv, 6). New in 2005: "Unlike previous ICP data, restaurant and catering expenditures are included among food in the 2005 data" (p. iv).

**Stage two** has eight subgroups (Table 4 labels): Cereals, Meat, Fish, Dairy and eggs, Oils and fat, Fruit and vegetables, Food other, Beverages and tobacco. **There is no "food at home / alcohol and tobacco / restaurants" split in TB-1929.** Precisely:

- **Restaurants have no subgroup of their own.** Food away from home is "captured under the 'other food' category" (p. 4). "Food other" "includes away-from-home food purchases" (p. 5) and "includes restaurant expenditures and high-end purchases" (p. 16). So "Food other" is restaurants plus every food item not in the six named subgroups, which by elimination means sugar, confectionery and food n.e.c.
- **"Beverages and tobacco" is never qualified.** It is "alcohol and tobacco" only if non-alcoholic beverages sit in "Food other", and no ERS document read here settles which.
- **Fruit and vegetables includes roots and tubers** (p. 5).

The post's footnote 23 says the ICP food group "is split into food at home, alcohol and tobacco, and restaurants with the stage-two conditional βs via their eq. 11". On TB-1929's own definitions, that split has to take three judgment calls:
- "Food other" stands in for restaurants;
- "Beverages and tobacco" stands in for alcohol and tobacco;
- food at home is the sum of the other six subgroups, with the at-home part of "Food other" either left out of it or apportioned some other way.

One property of the model, not a modelling choice: fitted shares are linear in `q_gc`, so a union of subgroups has `alpha*_S = sum alpha*_i` and `beta*_S = sum beta*_i`. With the printed values, the six named at-home subgroups sum to `beta* = -0.138` and `alpha* = 0.440`.

## 5. Tidy files

### `usda_tb1929_params.csv`: every estimated parameter (47 rows)

| column | meaning |
|---|---|
| `stage` | 1 = Florida-PI over the nine broad groups (Table 3); 2 = conditional Florida-Slutsky over the eight food subgroups (Table 4) |
| `category` | Group label exactly as in Tables 3-4; `(all)` for phi, K2 and K3 |
| `parameter` | `alpha`, `beta`, `phi` (income flexibility), `K2`, `K3` (heteroskedasticity of country groups 2 and 3 relative to group 1) for stage 1; `alpha_star`, `beta_star`, `pi_star_ii` (diagonal conditional Slutsky price effects), `K2`, `K3` for stage 2 |
| `value`, `se` | As printed, kept as text so the three printed decimals survive (`0.060`, not `0.06`). The significance stars are moved to `note`. |
| `table`, `page` | `Table 3` (printed p. 12, PDF p. 18) or `Table 4` (printed p. 16, PDF p. 22) |
| `note` | The meaning of the significance marker, the PDF page, the verification result for that parameter, the group's short definition on the `beta`/`beta_star` rows, and "se as printed (not recomputable)" |

Units: alpha, beta, alpha* and beta* are budget-share units. beta is the change in the budget share per unit of `ln` real per capita income at geometric mean prices; alpha is the fitted share at US income (`q = 0`). phi is dimensionless.

Coverage:
- Off-diagonal `pi*_ij` are not reported in TB-1929.
- There are no stage-one price parameters other than phi: the PI model's cross effects come from phi, alpha and beta.

Adding-up as printed:
- the nine stage-one alphas sum to 1.000 and the betas to 0.000;
- the stage-two alpha* sum to 1.001 and the beta* to +0.001 (rounding).

### `usda_tb1929_categories.csv`: definitions and mapping (17 rows: 9 groups + 8 subgroups)

| column | meaning |
|---|---|
| `stage`, `order`, `category` | Table 3/4 order and label (the join key to every other file) |
| `label_tb1929_text`, `label_tb1929_table2_appendix`, `label_data_product` | The same group as the bulletin's text, its Table 2 and appendix columns, and the data product's XLS headers name it |
| `short_definition` | One line |
| `definition_tb1929`, `definition_other_ers` | Verbatim quotes with source and page. The script finds each quote in the vendored text and fails if one is missing (44 checks), so the page labels are machine-located. `definition_other_ers` quotes the ERS documentation page and TB-1937. |
| `coicop_1999`, `coicop_2018`, `bls_ce`, `judgment_calls` | The mapping of section 8, in the same words |

### `usda_tb1929_countries.csv`: the 144 countries (144 rows)

`country` (ERS spelling), `country_order` (1-144, ascending per capita income, as in every appendix table),
`income_group` (low/middle/high, from the appendix headers), `per_capita_income_rel_us` (real per capita income relative to the US, 14 significant digits from the data product; `Q_c`), `per_capita_food_rel_us` (real per capita food spending relative to the US, 4-6 significant digits; `Q_gc`), `outlier_in_estimation` (one of footnote 11's 19 outliers).

### `usda_tb1929_country_long.csv`: every published country cell (9,936 rows = 144 countries x (9 groups x 5 tables + 8 subgroups x 3 tables))

| column | meaning |
|---|---|
| `appendix_table` | 1-8 |
| `measure` | 1 `income_elasticity` (eq. 5); 2 `frisch_own_price_elasticity` (eq. 6); 3 `slutsky_own_price_elasticity` (eq. 7); 4 `cournot_own_price_elasticity` (eq. 8); 5 `unconditional_income_elasticity` of food subgroups (eq. 11); 6 `unconditional_frisch_own_price_elasticity` of food subgroups (eq. 12); 7 `marginal_share` (eq. 3: the share of an extra dollar of total spending); 8 `conditional_marginal_share` (share of an extra dollar of food spending) |
| `equation`, `stage`, `category`, `country`, `country_order`, `income_group`, `outlier_in_estimation`, `per_capita_income_rel_us`, `per_capita_food_rel_us` | As above |
| `value`, `flag` | From the data product: tables 1-4 and 7 to 3 decimals, tables 5, 6 and 8 to 6 decimals. `flag` is the table's footnote letter: `a` = computed from the **actual** budget share because the fitted share was negative; `b` = a positive (Giffen) unconditional Frisch value set to zero by ERS (stored as `-0.0`, as ERS prints ` -0.000b`). |
| `value_pdf`, `flag_pdf` | The same cell as printed in the PDF (3 decimals) |
| `release_note` | Set on the 4 cells where the two ERS releases differ (section 7) |
| `pdf_page`, `printed_page`, `xls_file` | Where the cell is |

Elasticities are dimensionless. Marginal shares are fractions of a dollar.

The PDF and the data product agree on every other cell: exactly for tables 1-4 and 7, and to the PDF's rounding (<= 0.0005) for tables 5, 6 and 8. They also agree on every other footnote letter.

### `usda_tb1929_group_averages.csv`: income-group numbers (273 rows)

- The bulletin's Table 2 (`source_table = Table 2`). These are average **actual** budget shares by income group: broad groups as shares of total spending, and food subgroups as shares of food spending. They equal the data product's sheet `Table9` in all 51 cells.
- The three group averages printed under each appendix table, beside the simple mean of the printed country values (`mean_of_countries`, `n_countries`, `diff`). They are unweighted means: the largest |diff| over all eight tables is 0.0006.
- Table 2 is the only place TB-1929 reports actual budget shares, and only by group. Country-level actual shares are not published (see World Bank 2008, as the bulletin's footnote 6 says).

### `usda_tb1929_recompute.csv`: cell-level verification (9,936 rows)

One row per published cell, recomputed from the transcribed parameters and `Q_c` / `Q_gc`. Columns:
- `w_fitted`: the fitted share at geometric mean prices, broad or conditional;
- `published`, `flag`, `published_pdf`, `flag_pdf`;
- `status`: recomputed, or skipped as an `a` or `b` cell;
- `recomputed`, `band_lo`, `band_hi`, `gap`, `within_band`: computed with Table 3's phi;
- `recomputed_phi_hat`, `band_lo_phi_hat`, `band_hi_phi_hat`, `gap_phi_hat`, `within_band_phi_hat`: computed with the phi implied by ERS's own Frisch tables, -0.73356;
- `w_implied_actual`: for `a` cells, the actual share that reproduces the published elasticity;
- `half_unit_published`.

The band is the min and max of the recomputation over every parameter at its printed value and +-0.0005 (3^3 or 3^5 points), widened by the published cell's own half unit of rounding.

### `usda_tb1929_backsolved.csv`: parameters implied by ERS's own country tables (35 rows)

Marginal shares are linear in log income, `theta = alpha + beta (1 + q)`. A least-squares line through the 144 published marginal shares therefore returns alpha and beta: appendix table 7 for stage one (3 decimals) and appendix table 8 for stage two (6 decimals). phi is the median of `F_u / eta_U` (eq. 12).

Columns: `stage`, `category`, `parameter`, `value_printed`, `value_backsolved`, `rounds_to_printed`, `n_cells`, `max_abs_residual`, `method`.

These are **derived, not published**. They are the unrounded values behind ERS's tables:
- food beta is -0.108002 (printed -0.108) and food alpha 0.165214 (0.165);
- beta* for Food other is 0.087899 and for Beverages and tobacco 0.050889.

### `usda_tb1929_checks.csv`: every check (456 rows)

Columns: `kind`, `check`, `computed`, `published`, `diff`, `tolerance`, `unit`, `pass`, `source`, `note`. There are four kinds:
- `consistency` (136, all pass): my parsing and transcription. Two text extractors agree, PDF and data product agree, and counts, orders and quotes check out.
- `verification` (297: 291 pass, 6 fail): recomputing the bulletin's numbers. All 6 failures are the phi finding in section 7.
- `source_finding` (14): features of the source, recorded and not corrected.
- `info` (9): values recorded without a test.

## 6. Verification results

**Transcription.**
- Tables 3 and 4 parse identically from pdfplumber and pypdf, and both match the page images.
- Table 2 equals the data product's sheet.
- Appendix tables 1-8, 1,152-1,296 cells each, agree between PDF and data product except in the 4 cells listed in section 7.

**Recomputation from the transcribed parameters (eqs. 3, 5, 11).**
- All **4,876** income-elasticity and marginal-share cells that are not 'a' cells lie inside their rounding band. These are appendix tables 1, 5, 7 and 8.
- Largest gaps:
  - Food income elasticity, all 144 countries: max |gap| **0.0010** (Switzerland: published 0.460, recomputed 0.4590).
  - All cells: max |gap| **3.22** (Liberia, medical and health: published 8.62, recomputed 5.40, band 3.66 to 12.63). Liberia's fitted health share is 0.0045, so `1 + beta/w` swings wildly with the third decimal of alpha and beta.
  - Cells whose fitted share is at least 0.02: max |gap| **0.104** (Tanzania, medical and health: published 2.092, recomputed 1.988, inside the band).
  - Appendix table 5 ("Food other"): max |gap| 0.15 (The Gambia, fitted conditional share near zero, inside the band).
  - Appendix table 5 ("Beverages and tobacco"): max |gap| 0.003.

The spot checks requested for this step all pass. Columns: income elasticity (eq. 5) for food, marginal share for food, and eq. 11 for "Food other" and "Beverages and tobacco".

| country | eta food (pub / recomputed) | theta food | eta^U Food other | eta^U Bev. & tobacco | fitted food share |
|---|---|---|---|---|---|
| Finland | 0.525 / 0.5248 | 0.119 / 0.1193 | 0.677563 / 0.6773 | 0.652432 / 0.6519 | 0.2273 |
| United States | 0.346 / 0.3455 | 0.057 / 0.0570 | 0.437568 / 0.4367 | 0.423664 / 0.4227 | 0.1650 |
| Tanzania | 0.812 / 0.8119 | 0.466 / 0.4661 | 1.423754 / 1.4265 | 1.216367 / 1.2163 | 0.5741 |
| India | 0.782 / 0.7820 | 0.388 / 0.3873 | 1.331856 / 1.3341 | 1.153936 / 1.1538 | 0.4953 |
| Kenya | 0.791 / 0.7910 | 0.409 / 0.4088 | 1.457242 / 1.4605 | 1.214583 / 1.2145 | 0.5168 |

**Back-solve.**
- All 34 alpha and beta values round to the printed ones.
- Stage two fits to 2.3e-6, against a data-product rounding of 5e-7. The conditional model is exactly what ERS computed, and the back-solved alpha* and beta* sum to 1 and 0 to 1e-6.

**Text claims.**
- 35 numbers quoted in the bulletin's text against its own tables: all pass. Examples:
  - DR Congo food marginal share 63 cents vs US 6 cents;
  - food elasticity ranges 0.85-0.71 (low income), 0.71-0.57 (middle), 0.56-0.35 (high);
  - recreation elasticity from 13.1 (Angola) to 1.25 (US);
  - the Slutsky food peak of -0.384 runs "Ukraine to Argentina" (17 countries);
  - the turning point is at 22% of US income.

**Not verifiable by recomputation.** These are transcribed, and two extractors and the page image agree, but no table in TB-1929 depends on them:
- pi*_ii (the conditional Slutsky effects);
- K2 and K3 in both stages;
- every standard error.

## 7. Problems found in the source (flagged, not corrected)

1. **phi in Table 3 does not reproduce ERS's own price-elasticity tables.**
   - Table 3 prints phi = -0.732 (se 0.034). Every published Frisch elasticity divided by its income elasticity gives **-0.73356**: across the 1,129 six-decimal stage-two cells the ratio runs from -0.7339 to -0.7332, and the 3-decimal stage-one median is -0.73355. That would print as -0.734.
   - With -0.732, 51 of 4,981 recomputed Frisch, Slutsky and Cournot cells fall outside their rounding band, missing by up to 0.0018 (Guinea-Bissau food Frisch: published -0.607, recomputed -0.6052). They are concentrated in food (tables 2 and 4) and cereals (table 6).
   - With -0.73356 all 3,846 stage-one cells fall inside. That test is out of sample, since phi_hat comes from the stage-two tables.
   - The income elasticities, marginal shares, alpha and beta are unaffected. The post's eq. 5 does not use phi.
   - The cause is unknown: a misprint, or a different run behind the appendix. The SE makes the difference statistically irrelevant, but it is not rounding.
2. **Release differences between the PDF (Feb 2013) and the data product (Sep 2013):**
   - **Zambia, "Food other", appendix table 5.** The data product marks 1.672 'a'; the PDF does not. The fitted conditional share is -0.021, so 1.672 cannot be a fitted-share value. The data product is right, and the PDF's table 6 also marks Zambia 'a'.
   - **Appendix table 6, three cells.** For Spain cereals, Spain oils and fat, and Italy cereals, the data product keeps the raw positive Frisch values (0.180192, 0.054637, 0.006518). The PDF prints 0.000b, set to zero. The raw values match the recomputation with phi_hat.
   - Both versions are in `usda_tb1929_country_long.csv` (`value` vs `value_pdf`).
3. **'a' cells (actual instead of fitted shares).**
   - Stage one has 15 in table 1: health for DR Congo and Burundi, recreation for 10 countries, and "Other" for DR Congo, Burundi and Liberia. The text on p. 13 lists only 11 of them, and says the fitted shares "were negative". With the printed parameters, three of the 15 are tiny but positive: Burundi health 0.0022, Burundi Other 0.0002, Liberia Other 0.0038.
   - **Liberia "Other"** is 'a' in table 1 (1.415a) but not in tables 2-4, which print fitted-share values (-8.254, -7.980, -8.013).
   - The actual shares are not published. `w_implied_actual` gives the share that reproduces each 'a' cell.
   - Stage two has 5 'a' cells, all "Food other": DR Congo, Burundi, Liberia, Malawi and Zambia. They are exactly the countries whose fitted conditional share is negative, and all five are estimation outliers.
4. **'b' cells.** The PDF zeroes 12 unconditional Frisch values: cereals and/or oils for Cyprus, the United Kingdom, Switzerland, Austria, Luxembourg, the United States, Spain and Italy. They are exactly the cells whose income elasticity in appendix table 5 is negative. The text on p. 18 still quotes the US cereals Frisch value as "0.06": that is the positive value (+0.061) the table zeroed, printed without its sign.
5. **Significance markers.** Table 3 marks clothing and education beta (-0.002, se 0.002, |t| = 1) as significant at 0.01. Table 4 leaves pi*_ii for Beverages and tobacco (-0.127, se 0.027, |t| = 4.7) unmarked. These are recorded as printed.
6. **Smaller items.**
   - Table 4's note cites "equations 10a-10c", which do not exist (eq. 10 is a single equation).
   - The stage-two alpha* and beta* print to 1.001 and +0.001.
   - The PDF wraps three country names across lines ("Bosnia and Herze- / govina", "Central African / Republic"). The parser matches them to the clean names, and the checks list each one.
   - The data product's file title reads "For For Subcategories".
7. **What the documents leave open:**
   - The ICP basic headings inside each group and subgroup: TB-1929 never lists them (section 8).
   - Whether "beverages" includes non-alcoholic beverages.
   - Where accommodation (hotels) and net purchases abroad went.
   - Whether ERS's consumption aggregate is household expenditure only, or includes government-provided health and education.

## 8. Mapping to COICOP and to the BLS CE survey (judgment calls flagged)

ERS gives each group as a label plus at most one sentence. It never lists ICP basic headings, so every row below beyond "stated" is a judgment. COICOP 1999 is the classification the 2005 ICP and Eurostat's `nama_10_co3_p3` follow; COICOP 2018 is the one Statistics Finland's HBS 2022 and `nama_10_cp18` use in this thread. CE labels are the Table 1110 item names in `ce_income_deciles_long.csv`.

**Stage one: the nine groups**

| TB-1929 group | ERS definition | COICOP 1999 | COICOP 2018 | BLS CE | Judgment calls |
|---|---|---|---|---|---|
| Food, beverage, and tobacco | food at home + food away from home + beverages and tobacco; restaurants and catering new in 2005 (stated, pp. iv, 4, 6) | 01, 02, 11.1 | 01, 02, 11.1 | Food at home; Food away from home; Alcoholic beverages; Tobacco products and smoking supplies | 11.1 "in full" (canteens, take-away) is a judgment; accommodation 11.2 is not food; narcotics presumably here. CE on-premise alcohol and food on trips land here either way. |
| Clothing and footwear | label only | 03 | 03 | Apparel and services | CE "Other apparel products and services" holds watches and jewelry (COICOP personal effects, so Other). Small. |
| Housing and utilities | label only; TB-1937: "gross rent, fuel, and power" | 04 | 04 | Housing > Shelter; Housing > Utilities, fuels, and public services, less Telephone services | **Imputed rent.** ICP/COICOP include owner-occupiers' imputed rent (04.2, 15.2% of Finnish HBS 2022 spending); CE has none, and its "Owned dwellings" are cash outlays (mortgage interest, property taxes, insurance, repairs). CE "Other lodging" mixes second homes with lodging on trips (11.2, so Other). CE telephone sits in CE utilities but is communication. |
| Furnishing, household equipment, and maintenance | "house furnishings and operations"; TB-1937: "includes spending on household equipment and maintenance" | 05 | 05 | Housing > Household furnishings and equipment; Housing > Housekeeping supplies, less Postage and stationery; Housing > Household operations > Other household expenses | CE "Household operations > Personal services" is mostly child and adult care (COICOP social protection, so Other). |
| Medical and health | "medical care" | 06 | 06 | Healthcare | CE "Health insurance" is premiums, which COICOP books as insurance (12.5.3 / 12.1.3, so Other). Whether ERS's aggregate includes government-provided care is not stated. |
| Transportation and communication | "transport and communications" | 07, 08 | 07, 08 | Transportation; Telephone services (from CE utilities); postage | CE "Vehicle finance charges" are interest, outside consumption; CE "Vehicle insurance" is insurance (12.5.4 / 12.1.4, so Other); CE vehicle purchases are net of trade-ins. COICOP 2018's 08.1 "Information and communication equipment" merges phones (1999 08.2, here) with computers and audio-visual equipment (1999 09.1, recreation). |
| Recreation and culture | "recreation" | 09 | 09 | Entertainment; Reading | Package holidays are 09.6 / 09.8; CE spreads trips over lodging, transport and food away. In earlier ICP rounds food away from home sat here (TB-1937 fn. 11). |
| Education | "education" | 10 | 10 | Education | CE includes school books and supplies (COICOP recreation). Small. |
| Other | "other expenditures"; TB-1937: "grooming services, jewelry, and other miscellaneous expenditures" | 12 (+ 11.2 by judgment) | 12, 13 (+ 11.2 by judgment) | Personal care products and services; Miscellaneous (+ the items moved here above) | The residual. Where accommodation and net purchases abroad went is not stated. CE "Cash contributions" and "Personal insurance and pensions" are outside consumption and should be left out. |

**Stage two: the eight food subgroups** (shares of the food group, so they include food away from home)

| TB-1929 subgroup | ERS definition | COICOP (1999 = 2018 numbering) | BLS CE | Judgment calls |
|---|---|---|---|---|
| Cereals | "bread and cereals" | 01.1.1 | Food at home > Cereals and bakery products | none |
| Meat | "meat" | 01.1.2 | Meats, poultry, fish, and eggs > Beef, Pork, Other meats, Poultry | none |
| Fish | "fish" | 01.1.3 | Meats, poultry, fish, and eggs > Fish and seafood | none |
| Dairy and eggs | "dairy products" (text), "Dairy" (Table 2) | 01.1.4 | Food at home > Dairy products; Meats, poultry, fish, and eggs > Eggs | label differs between tables |
| Oils and fat | "oils and fats" | 01.1.5 | Other food at home > Fats and oils | none |
| Fruit and vegetables | includes roots and tubers (p. 5) | 01.1.6, 01.1.7 | Food at home > Fruits and vegetables | none |
| Food other | food away from home; "restaurant expenditures and high-end purchases" (pp. 4, 5, 16) | 11.1 (stated) + 01.1.8, 01.1.9 (by elimination); 01.2 here or in Beverages and tobacco (not stated) | Food away from home; Other food at home > Sugar and other sweets, Miscellaneous foods, Food prepared by consumer unit on out of town trips | **Not restaurants alone**, and the only subgroup holding restaurants |
| Beverages and tobacco | "beverages and tobacco" (unqualified) | 02 (+ 01.2 probably, not stated) | Alcoholic beverages; Tobacco products and smoking supplies (+ Other food at home > Nonalcoholic beverages if they belong here) | **"Alcohol and tobacco" only if non-alcoholic beverages sit in Food other**; unresolved |

**CE top-level items, read the other way**

| CE item | TB-1929 group (subgroup) |
|---|---|
| Food at home | Food, beverage, and tobacco (Cereals; Meat; Fish; Dairy and eggs; Oils and fat; Fruit and vegetables; Food other for sweets and miscellaneous foods; nonalcoholic beverages unresolved) |
| Food away from home | Food, beverage, and tobacco (Food other) |
| Alcoholic beverages | Food, beverage, and tobacco (Beverages and tobacco) |
| Tobacco products and smoking supplies | Food, beverage, and tobacco (Beverages and tobacco) |
| Housing > Shelter | Housing and utilities (concept differs: no imputed rent in CE; lodging on trips arguably Other) |
| Housing > Utilities, fuels, and public services | Housing and utilities, except Telephone services: Transportation and communication |
| Housing > Household furnishings and equipment; Housekeeping supplies | Furnishing, household equipment, and maintenance (postage: Transportation and communication) |
| Housing > Household operations | Furnishing ... (other household expenses); Other (personal services: child and adult care), by judgment |
| Apparel and services | Clothing and footwear (jewelry and watches: Other, by judgment) |
| Transportation | Transportation and communication (vehicle insurance: Other; finance charges: outside consumption), by judgment |
| Healthcare | Medical and health (premiums arguably Other), by judgment |
| Entertainment | Recreation and culture |
| Personal care products and services | Other |
| Reading | Recreation and culture |
| Education | Education |
| Miscellaneous | Other |
| Cash contributions; Personal insurance and pensions | outside consumption (no TB-1929 group) |

## 9. How the post uses it, in the bulletin's terms (definitions only, no modelling here)

- **What the post takes.** Footnote 23 cites "Tables 3-4" and uses beta from Table 3 for eq. 5, and the stage-two beta* through eq. 11. These are the parameters in `usda_tb1929_params.csv`.
- **Where the post evaluates eq. 5.** The post evaluates `eta = 1 + beta/w` at observed quintile (Finland HBS 2022) and decile (US CE 2024) budget shares. The bulletin evaluates it at the country's fitted share at geometric mean prices, `alpha + beta q_c`. Its own 2005 food elasticities are 0.525 for Finland (fitted share 0.2273) and 0.346 for the US (0.1650).
- **The bulletin endorses reuse with newer data.** The conclusion (p. 19) says: "parameters estimated from our models can be used (with more recent expenditure data) to estimate new elasticities for more recent years for the countries included in our analysis, as well as for other countries (Cox and Alm, 2007)".
- **What the broad groups contain.** The post's broad groups have to be mapped onto TB-1929's nine (section 8). Two of them include items the US and Finnish surveys book elsewhere:
  - TB-1929's food group includes restaurants;
  - TB-1929's housing group includes owner-occupiers' imputed rent.
