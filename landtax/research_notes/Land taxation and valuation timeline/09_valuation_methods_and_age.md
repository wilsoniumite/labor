# Land valuation methods, valuation quality, and the age of recurrent property-tax valuations in selected European countries (notes to 4 November 2026)

Scope: (a) how land is valued separately from buildings, how valuation quality is measured, and how values are kept current; (b) the base dates and revaluation cycles behind recurrent property taxes in France, Belgium, Italy, Spain, Portugal, the Netherlands, Ireland, Northern Ireland, Switzerland, Greece, Poland and Czechia. German, Japanese, Taiwanese and US legal texts are cited only to illustrate methods; their national histories belong to other researchers.

Confidence labels used throughout:
- **[P]** = confirmed by me in a primary source I opened and read (statute, official gazette, tax-authority or official publication, parliamentary record, court text reproduced in an official gazette, professional standard).
- **[S]** = secondary source only (journalism, professional firm, academic commentary). "[S, snippet]" means I saw it only in a search-result summary and did not open the page.
- **[U]** = unresolved: not verified in this session, or sources conflict.

Process note: the shared web-search budget for this run ran out partway through, after about 25 searches. After that I only fetched documents whose URLs I already had. The gaps this leaves are listed under each question and in the Access log.

## 1. How do valuers estimate the value of land on its own?

### Takeaway
Valuers prefer to use sales of vacant land. Where there are too few, they infer land value from sales of built property in one of four ways: allocation (a typical land share of the total), extraction/abstraction (sale price minus the depreciated cost of the building), anticipated use (a developer's residual), or land-residual capitalisation (the income left for the land after a return to the building). Some countries instead publish official zone values, such as Germany's Bodenrichtwerte and Japan's published land prices. Modern mass-appraisal models, from regression to gradient-boosted trees, mostly predict the value of the whole property. Land is then handled through separate rate tables or through "hybrid" models that can be split into land and building.

### Cited Findings

#### Why land must sometimes be valued separately
- The IAAO's mass-appraisal standard says: "State or local laws may require the value of an improved parcel to be separated into land and improvement components. When the sales comparison or income approach is used, an independent estimate of land value can be made and subtracted from the total property value to obtain a residual improvement value. Some computerized valuation techniques provide a separation of total value into land and building components." [P] — [IAAO, Standard on Mass Appraisal of Real Property, revised 2025, §4.5](https://www.iaao.org/wp-content/uploads/Standard_on_Mass_Appraisal.pdf)
- Standard history: the 2025 revision is "a partial update with revisions only to Section 3". It replaces the 2018 rewrite, which replaced the April 2013 standard. The 2002 standard had "combined and replaced the 1983 Standard on the Application of the Three Approaches to Value in Mass Appraisal, the 1984 Standard on Mass Appraisal, and the 1988 Standard on Urban Land Valuation." [P] — [IAAO 2025, revision notes](https://www.iaao.org/wp-content/uploads/Standard_on_Mass_Appraisal.pdf)

#### Method 1: sales of vacant land (sales comparison), base lots and unit values
- "The sales comparison approach is the primary approach to land valuation and is always preferred when sufficient sales are available." [P] — [IAAO 2025, §4.5](https://www.iaao.org/wp-content/uploads/Standard_on_Mass_Appraisal.pdf)
- In mass appraisal, valuers collect sales, plot them on maps, calculate "standard unit values (such as value per square foot, per front foot, or per parcel) by area and type of land use", and develop "land valuation maps or computer-generated tables in which the pattern of values is displayed." [P] — [IAAO 2025, §4.6.5](https://www.iaao.org/wp-content/uploads/Standard_on_Mass_Appraisal.pdf)
- Base-lot method: "The appraiser selects the most typical lot in the subarea as the base lot." Other parcels are then valued by adjusting for differences from the base lot in "Size, view, location, shape, topography and access". [P] — [Arizona Department of Revenue, Land Manual (effective 1 January 2001), ch. 3](https://azdor.gov/sites/default/files/2023-03/PROPERTY_LandManual.pdf)

#### Methods used when vacant-land sales are scarce
- IAAO lists the alternatives: "In the absence of adequate sales, other techniques that can be used in land appraisal include allocation, abstraction, anticipated use, capitalization of ground rents, and land residual capitalization." [P] — [IAAO 2025, §4.5](https://www.iaao.org/wp-content/uploads/Standard_on_Mass_Appraisal.pdf)
- **Allocation.** This method is based on "the theory that for a given type of property and area, the appraiser can determine a consistent overall relationship between land and improvement values". The manual's worked example shows land ratios of 0.253, 0.264 and 0.268 of total value in three neighbourhoods. [P] — [Arizona DOR Land Manual](https://azdor.gov/sites/default/files/2023-03/PROPERTY_LandManual.pdf)
- **Extraction / abstraction** (the appraisal literature says "extraction", US assessors say "abstraction"). The method "subtracts the depreciated replacement cost of improvement value from the sales price to yield the residual land value estimate." Worked example: sale price $180,000 minus ($200,000 replacement cost less $50,000 depreciation) gives land of $30,000. "The reliability of the generated improvement values depends on the accuracy of the cost model and the judgement of the appraiser in the calculation of depreciation." [P] — [Arizona DOR Land Manual](https://azdor.gov/sites/default/files/2023-03/PROPERTY_LandManual.pdf). IAAO adds that the technique "requires reliable cost data and tends to work best for relatively new improvements, for which depreciation is minimal." [P] — [IAAO 2025, §4.6.5](https://www.iaao.org/wp-content/uploads/Standard_on_Mass_Appraisal.pdf)
- **Anticipated use / cost of development** (also called subdivision development). The valuer imagines the site developed, then subtracts total development costs from the projected lot sales. Example: $3,600,000 of projected sales minus $2,700,000 of costs gives an undeveloped-land value of $900,000. The manual warns that "This method involves some speculation". [P] — [Arizona DOR Land Manual](https://azdor.gov/sites/default/files/2023-03/PROPERTY_LandManual.pdf)
- **Land residual capitalisation.** Used for income property when there are no vacant-land sales and the improvement value is known. The improvements must be "relatively new", must "represent the highest and best use", and must show "no observed depreciation". Inputs are net operating income, building value, discount rate, recapture rate and effective tax rate. [P] — [Arizona DOR Land Manual](https://azdor.gov/sites/default/files/2023-03/PROPERTY_LandManual.pdf)
- **Ground-rent capitalisation** appears in IAAO's list [P], but I did not obtain a primary description of the procedure. See Gaps.

#### Front-foot unit values and depth tables (the "Somers" tradition)
- The front-foot technique: multiply a unit front-foot value by a depth factor, then by the lot's frontage. Example: a 50 ft × 100 ft lot at $100 per front foot with depth factor 1.00 is worth $5,000. The manual notes that its depth and corner factors are hypothetical. [P] — [Arizona DOR Land Manual, Appendix C](https://azdor.gov/sites/default/files/2023-03/PROPERTY_LandManual.pdf)
- IAAO still lists "value per front foot" among standard unit values for land. [P] — [IAAO 2025, §4.6.5](https://www.iaao.org/wp-content/uploads/Standard_on_Mass_Appraisal.pdf)
- Attribution to William A. Somers's "unit-foot" system (St Paul, Minnesota, 1890s; book c. 1901) is **[U]**. I could not verify it in this session (see Gaps).

#### Standard land values by zone (approach only)
- **Germany, Bodenrichtwerte (BauGB §196).** Original text: "Auf Grund der Kaufpreissammlung sind flächendeckend durchschnittliche Lagewerte für den Boden … zu ermitteln (Bodenrichtwerte). In bebauten Gebieten sind Bodenrichtwerte mit dem Wert zu ermitteln, der sich ergeben würde, wenn der Boden unbebaut wäre. Es sind Richtwertzonen zu bilden, die jeweils Gebiete umfassen, die nach Art und Maß der Nutzung weitgehend übereinstimmen. … Die Bodenrichtwerte sind jeweils zu Beginn jedes zweiten Kalenderjahres zu ermitteln, wenn nicht eine häufigere Ermittlung bestimmt ist." Translation: average location values for land must be derived for the whole territory from the purchase-price collection. In built-up areas, the value is the one the land would have if it were unbuilt. Zones of broadly uniform type and intensity of use must be formed. Values are set at the start of every second calendar year unless more frequent determination is prescribed. They must be published, sent electronically to the tax authorities, and given to anyone who asks. [P] — [BauGB §196, gesetze-im-internet.de](https://www.gesetze-im-internet.de/bbaug/__196.html)
- **Japan, published land prices (地価公示, chika kōji), Land Price Publication Act, Act No. 49 of 1969, art. 2.** Once a year (毎年一回), the Land Appraisal Committee (土地鑑定委員会) obtains appraisals from two or more licensed real-estate appraisers (二人以上の不動産鑑定士) for each standard site (標準地). It reviews and adjusts them, then determines and publishes the "normal price" (正常な価格) per unit area at a reference date (基準日). For land that carries buildings, the normal price is the price "as if" the buildings or restricting rights did not exist (art. 2(2)). Art. 4 directs appraisers to consider prices of nearby comparable transactions, prices implied by nearby rents, and the cost of producing equivalent land. [P] — [e-Gov, 地価公示法 (law data 344AC0000000049)](https://laws.e-gov.go.jp/api/1/lawdata/344AC0000000049)
- **Spain.** Cadastral value must take account of location and planning status of the land; construction costs, quality and age; developer costs and profits; and "las circunstancias y valores del mercado" (market circumstances and values). It "no podrá superar el valor de mercado" (may not exceed market value), and a ministerial order fixes a "coeficiente de referencia al mercado" (market reference coefficient) (TRLCI art. 23). The criteria and valuation modules are set in municipal "ponencias de valores" (valuation reports) (arts. 25–26). [P] — [Real Decreto Legislativo 1/2004 (TRLCI), BOE consolidated text](https://www.boe.es/buscar/act.php?id=BOE-A-2004-4163)
- **Portugal.** Urban property value follows a formula, Vt = Vc × A × Ca × Cl × Cq × Cv: base construction value × gross area × use, location, quality and age coefficients (CIMI art. 38). Zoning and location coefficients are proposed every three years by the national commission CNAPU (art. 62). [P] — [CIMI art. 38](https://info.portaldasfinancas.gov.pt/pt/informacao_fiscal/codigos_tributarios/cimi/Pages/cimi38.aspx); [CIMI art. 62](https://info.portaldasfinancas.gov.pt/pt/informacao_fiscal/codigos_tributarios/cimi/Pages/cimi62.aspx)
- **Greece.** "Objective values" are built from zone prices (τιμές ζώνης). After the 2021 reform the system had 13,808 zones covering 98% of the population, up from 85%. [S] — [Ministry of Finance Q&A reproduced by CNN Greece, 7 June 2021](https://www.cnn.gr/oikonomia/story/269016/nees-antikeimenikes-axies-oi-perioxes-me-tis-megalyteres-ayxiseis-kai-tis-megalyteres-meioseis)
- **Belgium (historical method).** For the 1975 reference-date perequation, cadastre staff set each built parcel's cadastral income from sets of reference parcels ("parcelles de référence") and rental-value scales. Where no suitable reference parcel existed, cadastral income = 5.3% × the parcel's normal market value at 1 January 1975 (art. 478 CIR 92). Gross rents were reduced to net by a flat 40% allowance "quel que soit donc l'âge des constructions" (whatever the age of the buildings). [P] — [F. Gäbele, Belgian cadastre expert, FIG Congress, Sydney, 11–16 April 2010](https://www.fig.net/resources/proceedings/fig_proceedings/fig2010/papers/ts03j/ts03j_gabele_vanderschueren_4628.pdf)

#### Computer-assisted mass appraisal (CAMA), hedonic regression and machine learning
- IAAO's standard covers "computer assisted mass appraisal, CAMA systems, and/or automated valuation models", and discusses multiple regression analysis (MRA) for sales comparison. [P] — [IAAO 2025, §1 and §4](https://www.iaao.org/wp-content/uploads/Standard_on_Mass_Appraisal.pdf)
- "Another approach is a hybrid model decomposable into land and building values. Although these models can be calibrated from improved sales alone, separation of value between land and buildings is more reliable when both vacant and improved sales are available." [P] — [IAAO 2025, §4.6.5](https://www.iaao.org/wp-content/uploads/Standard_on_Mass_Appraisal.pdf)
- **A worked example of a modern assessor model (method illustration only):** the Cook County (Illinois) Assessor's residential model.
  - Model history: 2009–2017 "Linear regression per township"; 2019–2020 "Linear regression or GBM model per township"; 2021–2025 "County-wide LightGBM model", a gradient-boosted decision tree.
  - Evaluation: standard error measures (RMSE, MAE, MAPE) plus "assessor-specific metrics (COD, PRD, PRB, MKI)".
  - Land is not produced by the tree model. It comes from "Fixed $/sqft land rates by assessor neighborhood … Provided by the Valuations department".
  - The office lists LightGBM's downsides, including being "Relatively difficult to explain compared to simpler models such as linear regression" and "Prone to over-fitting".
  - [P] — [CCAO model-res-avm README](https://github.com/ccao-data/model-res-avm)
- In the Netherlands, the supervisor of the annual WOZ valuations reports a push for data quality and the "inzet van modellen voor marktanalyse en gecontroleerde taxatie" (use of models for market analysis and controlled valuation). [P] — [Waarderingskamer, Staat van de WOZ 2025 (letter of 19 June 2025)](https://www.waarderingskamer.nl/documenten/02.-Over-ons/Staat-van-de-WOZ/Staat-van-de-WOZ-2025.pdf)

### Inferences
- In plain terms, every land method answers the same question: "what would this site sell for with nothing on it?" When the market rarely sells empty sites (dense cities), valuers must either (i) borrow evidence from elsewhere (other areas' vacant sales, zone values) or (ii) subtract an estimate of the building from a sale price. Option (ii) moves the building-cost and depreciation errors into the land value.
- German and Japanese law both write the "as if unbuilt" rule into the definition of the land value. That makes zone values a legal construct calibrated to market evidence, not a direct observation, in built-up areas.
- Machine-learning models can predict total values accurately but do not naturally separate land from building. The Cook County practice (tree model for totals, table-based land rates) is one example of the split that land-only or split-rate taxes would need to resolve. This is my inference from the README, not a statement in it.

### Gaps
- **Somers system:** I could not verify the details or dates of William A. Somers's unit-foot system (the "unit foot" as a 1-ft strip of standard depth; depth tables; block-by-block public hearings; adoption in US cities after c. 1900). The search budget ran out, and I did not use archive services. Treat as [U].
- **Korea's standard land prices (표준지공시지가):** approach not verified in this session (other researchers cover Korea).
- **Ground-rent capitalisation:** no primary procedural description obtained.
- **Machine-learning comparisons:** peer-reviewed studies comparing ML with hedonic regression in mass appraisal were not re-verified (see Q3 background list).

## 2. How is valuation quality measured (ratio studies; IAAO COD, PRD, PRB)?

### Takeaway
Assessors test values against actual sale prices with "ratio studies" (assessed value ÷ sale price). They measure **level** (is the typical ratio close to 1?) and **uniformity**. Uniformity covers how widely ratios scatter (the coefficient of dispersion, COD) and whether expensive and cheap properties are assessed alike (the price-related differential, PRD, and price-related bias, PRB). IAAO standards set acceptable ranges, and accept more scatter for vacant land than for ordinary homes.

### Cited Findings
- Ratio studies "provide objective, bottom-line indicators of assessment performance". They cover "two primary aspects of assessment performance: level and uniformity." [P] — [IAAO 2025, §5.2](https://www.iaao.org/wp-content/uploads/Standard_on_Mass_Appraisal.pdf)
- **Level:** "the median ratio should be between 0.90 and 1.10" (citing the Standard on Ratio Studies, IAAO 2013). Values "can be statistically adjusted between full reappraisals or model recalibrations to ensure compliance." [P] — [IAAO 2025, §5.2.1](https://www.iaao.org/wp-content/uploads/Standard_on_Mass_Appraisal.pdf)
- **Consistency between groups:** "the level of appraisal for each major group of properties should be within 5 percent of the overall level for the jurisdiction". [P] — [IAAO 2025, §5.2.2](https://www.iaao.org/wp-content/uploads/Standard_on_Mass_Appraisal.pdf)
- **COD** is "the average percentage deviation from the median ratio. The lower the COD, the more uniform the ratios". IAAO COD standards:

  | Property group | COD standard |
  |---|---|
  | Single-family homes and condominiums | 5–10 for "newer or fairly similar residences"; 5–15 for "older or more heterogeneous areas" |
  | Income-producing property | 5–15 in "larger, urban areas"; 5–20 elsewhere |
  | Vacant land | 5–20 in "urban areas"; 5–25 in "rural or seasonal recreation areas" |
  | Rural residential, seasonal and manufactured homes | 5–20 |

  [P] — [IAAO 2025, §5.2.2](https://www.iaao.org/wp-content/uploads/Standard_on_Mass_Appraisal.pdf)
- "Poor uniformity within a property group is usually indicative of data problems or deficient valuation procedures or tables and cannot be corrected by application of market adjustment factors." [P] — [IAAO 2025, §5.2.2](https://www.iaao.org/wp-content/uploads/Standard_on_Mass_Appraisal.pdf)
- **PRD:** the standard "calls for PRDs of 0.98 to 1.03". Below 0.98 indicates assessment *progressivity* (ratios rise with price). Above 1.03 indicates *regressivity* (ratios fall with price, so cheaper homes are over-assessed relative to dearer ones). [P] — [IAAO 2025, §5.2.2](https://www.iaao.org/wp-content/uploads/Standard_on_Mass_Appraisal.pdf)
- **PRB** "indicates the percentage by which assessment ratios change whenever values double or are halved". For example, "a PRB of −0.03 would mean that assessment levels fall by 3 percent when value doubles". The standard "calls for PRBs of −0.05 to +0.05 and regards PRBs outside the range of −0.10 to +0.10 as unacceptable." [P] — [IAAO 2025, §5.2.2](https://www.iaao.org/wp-content/uploads/Standard_on_Mass_Appraisal.pdf)
- IAAO standards "are advisory in nature and the use of, or compliance with, such standards is voluntary"; national, state or provincial law governs where it conflicts. [P] — [IAAO 2025, front matter](https://www.iaao.org/wp-content/uploads/Standard_on_Mass_Appraisal.pdf)
- **Practice examples:**
  - Cook County publishes COD, PRD, PRB and MKI, the "Modified Kakwani Index", a further vertical-equity measure, for its model. [P] — [CCAO README](https://github.com/ccao-data/model-res-avm)
  - In the Netherlands, the Waarderingskamer reviews each municipality's valuation quality before values may be released. For the 1 January 2024 valuation date, some WOZ organisations "in eerste instantie niet voldeden aan onze kwaliteitseisen" (initially did not meet our quality requirements) and were reassessed after improvements. In 2025, 97.2% of WOZ values were issued on time, against 96.8% in 2024. [P] — [Waarderingskamer, Staat van de WOZ 2025](https://www.waarderingskamer.nl/documenten/02.-Over-ons/Staat-van-de-WOZ/Staat-van-de-WOZ-2025.pdf)

### Inferences
- The ratio-study framework only works where sales are frequent. It is weakest exactly where separate land valuation is hardest: built-up areas with few vacant sales. Vacant-land CODs can be measured only on the (often atypical) vacant parcels that sell.
- A regressive PRD is the usual statistical signature of ageing or frozen values in markets where cheaper areas appreciate faster. That links Q2 to the revaluation-frequency question in Q5. This is an inference; I did not obtain a study measuring it for the European countries in Q6.

### Gaps
- I could not open the IAAO Standard on Ratio Studies itself (see Access log). The thresholds above are as restated in IAAO's 2025 mass-appraisal standard. Whether IAAO has since revised the ratio-study standard is unconfirmed.
- No European tax administration in my list publishes IAAO-style COD/PRD tables that I could confirm in this session (the Dutch Waarderingskamer uses its own quality framework).

## 3. How accurately can land be valued separately from buildings, compared with whole properties?

### Takeaway
The profession's own standards expect land-only valuations to be less precise than whole-property valuations of homes: IAAO accepts a COD of up to 20–25 for vacant land against 10–15 for houses. They also say the split between land and building is "more reliable" when both vacant and improved sales exist. Practitioners report that residual (extraction) land values for built-up commercial property are "complex, inaccurate and prone to debate and challenge". Academic work splits between "residual" approaches (total value minus structure cost) and "direct" approaches (vacant-land and teardown sales). Each carries a known bias risk. I could not re-verify the academic literature online in this session.

### Cited Findings
- IAAO's acceptable COD for **vacant land** is 5–20 (urban) or 5–25 (rural), against 5–10 or 5–15 for **single-family homes**. [P] — [IAAO 2025, §5.2.2](https://www.iaao.org/wp-content/uploads/Standard_on_Mass_Appraisal.pdf)
- "The most difficult aspects of the cost approach are estimates of land value and accrued depreciation. These estimates must be based on non-cost data (primarily sales) and can involve considerable subjectivity. Land values used in the cost approach must be current and consistent. Often, they must be extracted from sales of improved property because sales of vacant land are scarce." [P] — [IAAO 2025, §4.2 "The Cost Approach"](https://www.iaao.org/wp-content/uploads/Standard_on_Mass_Appraisal.pdf)
- "Separation of value between land and buildings is more reliable when both vacant and improved sales are available." [P] — [IAAO 2025, §4.6.5](https://www.iaao.org/wp-content/uploads/Standard_on_Mass_Appraisal.pdf)
- Extraction works best "for relatively new improvements, for which depreciation is minimal" [P] — [IAAO 2025, §4.6.5](https://www.iaao.org/wp-content/uploads/Standard_on_Mass_Appraisal.pdf). Its reliability "depends on the accuracy of the cost model and the judgement of the appraiser in the calculation of depreciation" [P] — [Arizona DOR Land Manual](https://azdor.gov/sites/default/files/2023-03/PROPERTY_LandManual.pdf)
- **Australia (site-value taxation).** Boyd & Boyd (2011), a conference paper by two Australian valuation academics:
  - "in highly developed urban areas, it is often difficult to find comparative evidence of vacant land sales", so the land component is "at times, calculated from the improved capital value as the residual land value".
  - For investment property "this residual land exercise is complex, inaccurate and prone to debate and challenge". The residual or extraction technique "has a higher degree of uncertainty and thus the resultant valuation will probably have a higher margin of error".
  - They recommend it "should not be used as a primary method for the valuation of vacant land when comparable vacant land sales are available". They argue that deducting a depreciated-replacement-cost building value is "flawed" for investment property, and propose productivity-based benchmarks and ratio allocation instead.
  - [Scholarly conference paper, not a journal article] — [T. Boyd & S. Boyd, "Valuing the land component of improved investment property for tax purposes", 17th Pacific Rim Real Estate Society Conference, Gold Coast, January 2011](https://www.prres.org/uploads/727/1831/Boyd_Valuing_the_land_component.pdf)
- **Background academic references [U]** (from my background knowledge; NOT re-verified online in this session because the search budget ran out; check before citing):
  - *Residual / "land leverage" approach (total value minus structure replacement cost):*
    - Davis, M. A. & Heathcote, J. (2007), "The price and quantity of residential land in the United States", *Journal of Monetary Economics* 54(8).
    - Davis, M. A. & Palumbo, M. G. (2008), "The price of residential land in large US cities", *Journal of Urban Economics* 63(1).
    - Bostic, R. W., Longhofer, S. D. & Redfearn, C. L. (2007), "Land leverage: decomposing home price dynamics", *Real Estate Economics* 35(2).
    - Bourassa, S. C., Hoesli, M., Scognamiglio, D. & Zhang, S. (2011), "Land leverage and house prices", *Regional Science and Urban Economics* 41(2).
    - Larson, W., Shui, J., Davis, M. & Oliner, S. (2021), "The price of residential land for counties, ZIP codes, and census tracts in the United States", *Journal of Monetary Economics* 118.
  - *Direct approach (vacant-land or teardown sales):*
    - Dye, R. F. & McMillen, D. P. (2007), "Teardowns and land values in the Chicago metropolitan area", *Journal of Urban Economics* 61(1).
    - Haughwout, A., Orr, J. & Bedoll, D. (2008), "The price of land in the New York metropolitan area", Federal Reserve Bank of New York, *Current Issues in Economics and Finance* 14(3).
    - Albouy, D., Ehrlich, G. & Shin, M. (2018), "Metropolitan land values", *Review of Economics and Statistics* 100(3).
    - Kok, N., Monkkonen, P. & Quigley, J. M. (2014), "Land use regulations and the value of land and housing: an intra-metropolitan analysis", *Journal of Urban Economics* 81.
  - *Statistical land-value surfaces from total-property sales:* Kolbe, J., Schulz, R., Wersing, M. & Werwatz, A. (2015), "Identifying Berlin's land value map using adaptive weights smoothing", *Computational Statistics* 30(3). Compares statistical estimates with Berlin's official Bodenrichtwerte.
  - *Assessment-administration view:*
    - Bell, M. E., Bowman, J. H. & German, J. C. (2009), "The assessment requirements for a separate tax on land", in R. F. Dye & R. W. England (eds.), *Land Value Taxation: Theory, Evidence, and Practice*, Lincoln Institute of Land Policy.
    - Dye, R. F. & England, R. W. (2010), *Assessing the Theory and Practice of Land Value Taxation*, Policy Focus Report, Lincoln Institute of Land Policy. Download failed; see Access log.

### Inferences
- **Where sources disagree** (my synthesis; the specific academic positions are [U] until re-verified):
  1. *Residual vs direct evidence.* Residual methods depend on construction-cost and depreciation estimates, so building-cost errors land in the land value. IAAO, the Arizona manual and Boyd & Boyd all flag this. Direct methods depend on the few vacant or teardown sales, which may not represent typical built parcels.
  2. *Practice vs theory.* Valuation-administration sources stress that land-only values are harder and need more data. This shows in IAAO's wider vacant-land COD band and in Boyd & Boyd's Australian experience. Advocates of land taxation often argue that land is easier to value because location is the main driver. I found no head-to-head study in this session that measures land-only and whole-property accuracy in the same jurisdiction with ratio statistics.
  3. *Commercial vs residential.* The Australian paper's difficulties concern complex investment property (shopping centres). Residential land, with many comparable lots and zone values, appears more tractable in the methods literature, for example IAAO's base-lot and unit-value procedures.
- For a teaching narrative: whether "land can be valued accurately" depends on market structure. It is relatively easy on the urban fringe where vacant lots trade, and hardest in fully built city centres where land almost never trades empty.

### Gaps
- No verified quantitative comparison (for example COD of land-only vs total values in the same place) was obtained.
- The academic references above need checking (authors, years, volumes) and their findings summarising from the originals.
- The Lincoln Institute Policy Focus Report (Dye & England 2010) could not be downloaded.

## 4. Self-assessment with a state right to buy (Taiwan) and the "Harberger tax" idea

### Takeaway
In Taiwan's statute, owners "declare" their land value within a band around the government's announced value. If they declare too low (below 80% of the announced value), the government may buy the land at the declared value, or tax it at 80% of the announced value. The "Harberger tax" generalises this idea: owners name their own value, pay tax on it, and must sell at that price, so under-declaring risks losing the asset and over-declaring raises the tax. Ireland's Local Property Tax is also self-assessed but has no purchase right, only Revenue review.

### Cited Findings
- **Taiwan, Equalization of Land Rights Act (平均地權條例), English text on the Ministry of Justice database, amendment date 2023-02-08** [P] — [law.moj.gov.tw, pcode D0060009](https://law.moj.gov.tw/ENG/LawClass/LawAll.aspx?pcode=D0060009):
  - Art. 14: "The land value shall be reassessed once every two years after its initial assessment or reassessment. The reassessment of land value can be postponed if necessary."
  - Art. 15: the authorities "Investigate the transaction prices and income values of lands occurring in the last 12 months by sections". They demarcate "land value sections", send section values to the Land Value Evaluation Committee, calculate each plot's value, and "Publicly announce the land values for 30 days for the landowners to declare the values of their lands".
  - Art. 16: if the owner does not declare, "80 percent of the announced land values shall be deemed as his declared land value". A declaration above 120% of the announced value is capped at 120%. "If the land value declared by the owner is lower than 80 percent of the announced land values, the government reserves the right to purchase his land at the announced land value, or the 80 percent of the announced land value shall be deemed as his declared land value."
  - Art. 17: "A land value tax based on the declared land value shall be levied". Art. 18: progressive rates.
  - Chapter IV is titled "Government Purchase of Land According to the Declared Land Value". Art. 31(1): "The purchase price of land shall be the same as its declared value if it is purchased pursuant to the provisions of Article 16". Art. 32: registered land-improvement costs and paid construction benefit charges are added to the purchase price.
  - **Discrepancy:** the English Art. 16 says purchase "at the announced land value", while Art. 31(1) and the chapter title say the declared value. The Chinese original should be checked; my understanding is that 照價收買 means purchase at the declared price [U].
- **Ireland (self-assessment without purchase right):** "a system of self-assessment means that it is up to the liable person (usually the property owner) in the first instance to value his or her property and to declare that" value. Owners should keep evidence "in case of a subsequent Revenue review of their self-assessed valuation." [P] — [Revenue, Tax and Duty Manual LPT Part 04-01 (updated October 2025)](https://www.revenue.ie/en/tax-professionals/tdm/local-property-tax/part-04/04-01.pdf)
- **Harberger tax: references and mechanism [U]** (background; not re-verified online; the OUP page for Posner & Weyl returned HTTP 403):
  - Harberger, A. C. (1965), "Issues of tax reform for Latin America", in Joint Tax Program of the OAS and IDB, *Fiscal Policy for Economic Growth in Latin America* (Johns Hopkins Press). Proposes self-assessed property values combined with an obligation to sell at the declared value.
  - Posner, E. A. & Weyl, E. G. (2017), "Property is only another name for monopoly", *Journal of Legal Analysis* 9(1). Proposes a "common ownership self-assessed tax" (COST): owners declare values, pay a periodic tax on them, and must sell to any bidder at the declared price.
  - Posner & Weyl (2018), *Radical Markets* (Princeton University Press). Popularised the term "Harberger tax".

### Inferences
- **How it is meant to work (plain language):** the tax pushes the declaration down, while the threat of a forced sale at the declared price pushes it up. The owner is induced to state roughly what the property is worth to them, so the state needs no valuer.
- Taiwan's version is a hybrid. The government's announced value (set from transaction and income evidence, Art. 15) anchors a ±20% band, and only the government (not any private bidder) may buy. The value actually taxed therefore depends heavily on the official announced value. How often purchases happen in practice was not established (Gaps).
- Practical issues raised in the literature (owners' attachment and moving costs, uncertainty about who may buy, financing of purchases, and administration of forced sales) are [U]: not verified in this session.

### Gaps
- How often Taiwan's government has actually used the purchase power, and how announced values compare with market prices, were not found (other researchers cover Taiwan's history).
- The Chinese text of Art. 16 should be checked against the English translation.
- Harberger/Posner–Weyl citations need verification.

## 5. Keeping values current: annual vs periodic revaluation, indexation, caps and phase-ins

### Takeaway
Professional standards treat annual assessment as the goal. Between physical reinspections (every 4–6 years) values can be kept current by recalibrating models or applying market adjustment factors. Many European countries instead keep decades-old bases and update them with flat inflation coefficients, or not at all. International reviews (OECD 2022; European Commission 2012) say outdated values erode revenue, create unfairness between similar and between richer and poorer households, and discourage moving. Because each revaluation creates losers, it becomes politically harder the longer it is delayed. Governments soften revaluations with band widening, rate cuts, revenue-neutral resets, caps and phase-ins.

### Cited Findings
- **IAAO on frequency:** "The Standard on Property Tax Policy (IAAO 2020) states that current market value implies annual assessment of all property. Annual assessment does not necessarily mean, however, that each property must be re-examined each year. Instead, models can be recalibrated, or market adjustment factors derived from ratio studies or other market analyses applied". Property data "should be reviewed and updated at least every 4 to 6 years", either all at once, in cycles (for example "one-fourth or one-sixth each year"), or by priority. [P] — [IAAO 2025, §4.8](https://www.iaao.org/wp-content/uploads/Standard_on_Mass_Appraisal.pdf)
- "Land values should be reviewed annually. At least once every 4 to 6 years the properties should be physically inspected and revalued." [P] — [IAAO 2025, §4.5](https://www.iaao.org/wp-content/uploads/Standard_on_Mass_Appraisal.pdf)
- IAAO's standard does not cover "assessed values that differ from market value because of statutory constraints such as use value, classification, or assessment increase limitations". In other words, caps take assessed values away from market value by design. [P] — [IAAO 2025, §1](https://www.iaao.org/wp-content/uploads/Standard_on_Mass_Appraisal.pdf)
- **OECD (2022), *Housing Taxation in OECD Countries* (Tax Policy Studies No. 29), summary brochure:**
  - "Many countries levy recurrent taxes on immovable property on significantly outdated property values. This reduces horizontal equity (as households with properties of similar value may not face similar tax liabilities) and vertical equity (as households with more valuable housing may not pay more taxes). This also provides incentives for people to remain in undervalued housing even if it no longer suits their needs."
  - "Many countries levy recurrent property taxes on outdated property values, which significantly reduces their revenue potential (as revenues have not risen in line with property values)".
  - Policy option: "Regularly updating property values is key to the efficiency, equity and revenue potential of recurrent taxes on immovable property. Countries relying on outdated values and wishing to set up a system of regular valuations could consider embedding such a reform in a more comprehensive property tax overhaul, with measures to mitigate potential increases in tax liabilities."
  - [P] — [OECD brochure (2022)](https://www.oecd.org/tax/tax-policy/brochure-housing-taxation-in-oecd-countries.pdf); [report page](https://www.oecd.org/en/publications/housing-taxation-in-oecd-countries_03dfe007-en)
- **European Commission (October 2012), *Possible reforms of real estate taxation: Criteria for successful policies* (European Economy Occasional Papers 119), §4.1:**
  - "Most countries in the EU use, however, outdated property values." Examples given: Austria (1973 cadastral values), Cyprus (1980), the UK (1991); "Belgium (values from 1975) and Germany (from 1964) update the cadastral values with inflation or a corrective factor, but not with house price developments". "The Netherlands does it annually, Denmark biannually and Sweden every third year."
  - Rising prices create "political pressures to freeze the valuation (or reduce tax rates). Both Sweden and Denmark froze their tax bases… once the tax base is frozen, it becomes politically very difficult to update the tax base."
  - Citing Mirrlees et al. (2011): "any revaluation of properties creates losers and winners, with losers often being very vocal… the 'tyranny of the status quo'".
  - Failure to update "risks leading to an erosion of the tax base", although revenue "has been relatively stable"; "There are various ways to phase in the adjustment".
  - Box 4.1 sets the criterion: "The cadastral value (i.e. the tax base) should be regularly updated according to market values".
  - [P] — [EC, ECFIN Occasional Paper 119](https://ec.europa.eu/economy_finance/publications/occasional_paper/2012/pdf/ocp119_en.pdf)
- **Indexation in practice (details in Q6):**
  - Belgium: CPI indexation since 1991 [P] — [EC OCP 119 annex](https://ec.europa.eu/economy_finance/publications/occasional_paper/2012/pdf/ocp119_en.pdf)
  - Portugal: triennial update by currency-devaluation coefficients [P] — [CIMI art. 138](https://info.portaldasfinancas.gov.pt/pt/informacao_fiscal/codigos_tributarios/cimi/Pages/cimi138.aspx)
  - Spain: budget-law coefficients by year of the municipality's ponencia [P] — [TRLCI art. 32](https://www.boe.es/buscar/act.php?id=BOE-A-2004-4163)
  - Czechia: CPI-based inflation coefficient [P] — [Act 338/1992 §11f](https://www.zakonyprolidi.cz/cs/1992-338)
  - Poland: annual CPI indexation of maximum per-m² rates [P] — [Ministry of Finance note on 2026 rates](https://www.podatki.gov.pl/media/1p1hokoz/wysokość-stawek-w-opodatkowaniu-nieruchomości-w-2026-r.pdf)
- **Softening revaluations (caps, bands, rate cuts, neutrality):**
  - Ireland reset its bands and cut the basic rate at each revaluation: 0.18% (2013–2021) → 0.1029% (2022–2025) → 0.0906% (2026–2030), with the first band widened from €0–100,000 to €0–200,000 and then €0–240,000. The local adjustment factor is ±15% for 2013–2026, and up to +25% (−15%) from 2027. [P] — [Revenue TDM Part 04-01](https://www.revenue.ie/en/tax-professionals/tdm/local-property-tax/part-04/04-01.pdf)
  - Northern Ireland: homes worth more than £400,000 "are billed for rates as if the property was valued at £400,000". [P] — [DoF NI, Consultation Paper: Domestic Rating Measures, Nov 2023](https://minutes.belfastcity.gov.uk/documents/s112576/Appendix%202%20-%20DoF%20revenue%20raising%20consultation%20domestic.pdf)
  - Greece (2021): the zone-value update came with a redesigned ENFIA, applied from 2022, keeping "συνολική δημοσιονομική ουδετερότητα" (overall fiscal neutrality), "παρά τις μεταβολές στις αντικειμενικές αξίες τα δημόσια έσοδα που προβλέπονται από τον ΕΝΦΙΑ δεν θα αυξηθούν" (despite changes in objective values, expected ENFIA revenue will not rise). [S] — [MoF Q&A via CNN Greece, 7 June 2021](https://www.cnn.gr/oikonomia/story/269016/nees-antikeimenikes-axies-oi-perioxes-me-tis-megalyteres-ayxiseis-kai-tis-megalyteres-meioseis)
  - Spain: IBI tax bases equal cadastral values "minorados en la cuantía de la reducción" (less the statutory reduction) in TRLRHL arts. 65–70 [P] — [BOE-A-2026-3814](https://www.boe.es/boe/dias/2026/02/19/pdfs/BOE-A-2026-3814.pdf). The reduction's phase-in length (often cited as nine years) is [U].
- **The political-difficulty argument, voiced in France:** Laurent Saint-Martin, then the finance committee's general rapporteur, in 2021: "Plus on attend, plus c'est difficile et plus les valeurs cadastrales s'éloignent de la réalité du marché" (the longer we wait, the harder it is and the further cadastral values drift from market reality). [S] — [Meilleurtaux, 20 October 2026](https://www.meilleurtaux.com/credit-immobilier/actualites/2026-octobre/taxe-fonciere-revision-des-valeurs-locatives-des-2028.html)

### Inferences
- Two families of "keeping current" exist:
  - *Full market revaluation*, annual (Netherlands) or periodic (Ireland every 5 years), which changes relative values.
  - *Flat indexation* (Belgium, France, Portugal, Spain's coefficients, Czechia, Poland), which raises all values or rates by the same percentage and so preserves whatever relative distortions existed at the base date.
- Indexation protects revenue against inflation but does not fix horizontal or vertical inequity, which only a revaluation can do (this follows from the OECD and EC passages above).
- Softening devices (Ireland's band and rate reset, Greece's revenue-neutral ENFIA) let a revaluation update *relative* values without raising the *total* burden.

### Gaps
- IMF (Norregaard 2013, WP/13/129) and the World Bank's property-tax diagnostic work could not be accessed (HTTP 403, or not attempted after the search budget ran out). The Lincoln Institute report download failed. I therefore cannot quote what those bodies say about infrequent revaluation.
- The OECD 2022 full report's country table of valuation dates was not obtained; only the summary brochure was read.

## 6. How old are the valuations behind recurrent property taxes in the selected European countries (status at 4 November 2026)?

### Takeaway
The oldest bases still in use in this group are:
- France: 1 January 1970 rental values for homes, with general revision now postponed to 2031.
- Belgium: 1 January 1975 rental values, CPI-indexed since 1991.
- Italy: 1988–89 tariffs, adjusted only by ad hoc multipliers.
- Northern Ireland: 1 January 2005 capital values.

The Netherlands revalues every year, at 1 January of the prior year. Ireland revalued at 1 November 2025 for 2026–2030. Spain's base varies municipality by municipality with the date of each ponencia de valores. Portugal's base largely dates from the 2012–13 general valuation, updated every three years for inflation. Greece's zone prices date from the 2021 revision, applied from 2022. Poland and Czechia tax by floor or land area, not value. Switzerland's values are cantonal, and its imputed rent on owner-occupied homes will be abolished from 1 January 2029.

### Cited Findings

#### Summary table

| Country | Tax | Base date of values in use | Legal revaluation cycle | Last actual general revaluation | Indexation | Status in 2026 | Primary source |
|---|---|---|---|---|---|---|---|
| France | Taxe foncière sur les propriétés bâties (and other direct local taxes) on *valeur locative cadastrale* | 1 Jan 1970 for dwellings; 1 Jan 1975 in Guadeloupe, Guyane, Martinique, Réunion [P] | Dwellings: none in force; revision ordered by art. 146 LF 2020 [P]. Business premises (since 2017): tariffs yearly, location coefficients every 2 years, all parameters every 6 years [P] | Dwellings: the 1970 general revision [P for reference date]. Business premises: revised values from 1 Jan 2017 [P] | Annual flat-rate coefficient (CGI art. 1518 bis) [U this session] | Art. 106 LF 2026 (loi n° 2026-103, 19 Feb 2026) moves dwelling revision into tax bases at 1 Jan 2031, using rents at 1 Jan 2028 [P]; business-premises 6-year update moved to 1 Jan 2027 [P]. 2027 budget amendment I-CF1872 (revise at each sale from 2028) adopted in committee 9 Oct 2026; final fate unconfirmed [P/U] | [BOFiP BOI-IF-TFB-20-10-10](https://bofip.impots.gouv.fr/bofip/4889-PGP.html/identifiant=BOI-IF-TFB-20-10-10-20121210); [DGCL](https://www.collectivites-locales.gouv.fr/index.php/gerer-les-finances-publiques-locales/fiscalite-locale/fiscalite-directe-locale/reforme-des-valeurs-locatives); [AN I-CF1872](https://www.assemblee-nationale.fr/dyn/17/amendements/3210A/CION_FIN/CF1872) |
| Belgium | Précompte immobilier / onroerende voorheffing (regional, plus provincial and municipal surcharges) on indexed *revenu cadastral* / *kadastraal inkomen* | 1 Jan 1975 normal net rental value [P] | Not verified (code text unreachable) [U] | General perequation of 1975–1980 [P]; none since [S] | CPI since 1991 [P]; coefficient 2.2446 (2025) [S]; 2.3000 (2026) [P] | No general perequation in prospect found [U]; EC (2012): assessed value "on average below half of the market value" [P] | [Gäbele, FIG 2010](https://www.fig.net/resources/proceedings/fig_proceedings/fig2010/papers/ts03j/ts03j_gabele_vanderschueren_4628.pdf); [INAMI circular 6 Jan 2026](https://www.inami.fgov.be/SiteCollectionDocuments/bi2026_1_donnees_de_base_IV.pdf); [EC OCP 119](https://ec.europa.eu/economy_finance/publications/occasional_paper/2012/pdf/ocp119_en.pdf) |
| Italy | IMU (and before it ICI) on *rendita catastale* × statutory multipliers | Tariffs (*tariffe d'estimo*) referring to the 1988–89 biennium, set in 1990 [S] | Ten-yearly revision foreseen but "mai stato messo in atto" (never carried out) [S] | 1990 (1988–89 values) [S]; +5% in 1996 [S] | None automatic; multiplier raised 60% (Dec 2011, for 2012) [S] | No general reform enacted that I could confirm; 2014 delegation lapsed [U]; 2025–26 status unconfirmed [U] | None accessed (Normattiva and the Constitutional Court site were blocked); see [EC OCP 119](https://ec.europa.eu/economy_finance/publications/occasional_paper/2012/pdf/ocp119_en.pdf) (official staff paper) |
| Spain | IBI (Impuesto sobre Bienes Inmuebles) on *valor catastral* | Year of each municipality's *ponencia de valores* (varies) [P for rule] | New general valuation allowed 5+ years after the last; "se realizará, en todo caso, a partir de los 10 años" [P] | Varies by municipality; national distribution not obtained [U] | Budget-law coefficients by ponencia year, on municipal request [P]; 2026 coefficients unconfirmed [U]; 2023 budget rolled over into 2026 [P] | Plusvalía land-value method struck down 2017–2021 (see court rulings) [P] | [TRLCI arts. 23, 25–29, 32](https://www.boe.es/buscar/act.php?id=BOE-A-2004-4163); [BOE-A-2026-3814](https://www.boe.es/boe/dias/2026/02/19/pdfs/BOE-A-2026-3814.pdf) |
| Portugal | IMI on *valor patrimonial tributário* (VPT) | Date of each urban property's last CIMI valuation; most valued in the 2012–13 general valuation [S] | VPT updated every 3 years by inflation coefficient (100% commercial/industrial/services; 75% for housing, building land, others) [P]; zoning and location coefficients every 3 years [P]; construction base value yearly [P] | 2012 general valuation of urban property (notified Dec 2012) [S] | Triennial, art. 138 CIMI [P] | Rustic (rural) property status not verified [U] | [CIMI arts. 38](https://info.portaldasfinancas.gov.pt/pt/informacao_fiscal/codigos_tributarios/cimi/Pages/cimi38.aspx), [62](https://info.portaldasfinancas.gov.pt/pt/informacao_fiscal/codigos_tributarios/cimi/Pages/cimi62.aspx), [138](https://info.portaldasfinancas.gov.pt/pt/informacao_fiscal/codigos_tributarios/cimi/Pages/cimi138.aspx) |
| Netherlands | OZB (municipal property tax) and other levies on the WOZ value | 1 Jan 2025 for tax year 2026 (one year before the tax year) [P] | Annual: value valid for one calendar year [P] | Annual; latest valuation date 1 Jan 2025 (average +10.6% on the prior year) [P] | Not needed (annual revaluation) | About 9.4 million WOZ objects; 97.2% of decisions on time in 2025 [P] | [Wet WOZ arts. 18 and 22](https://wetten.overheid.nl/BWBR0007119/); [Waarderingskamer](https://www.waarderingskamer.nl/documenten/02.-Over-ons/04.-Onze-adviezen/Brief-bijstelling-eigenwoningforfait-2026.pdf) |
| Ireland | Local Property Tax (self-assessed by owners) | 1 Nov 2025, for 2026–2030 [P] | 5-year valuation periods (2025 amendment Act s.6); next valuation date intended 1 Nov 2030 [P] | 1 Nov 2025 (before that 1 Nov 2021 and 1 May 2013) [P] | None; bands and rates reset at revaluation [P] | 2026–2030 bands in force; basic rate 0.0906% [P] | [Revenue TDM 04-01 (Oct 2025)](https://www.revenue.ie/en/tax-professionals/tdm/local-property-tax/part-04/04-01.pdf) |
| Northern Ireland | Domestic rates on capital value | 1 Jan 2005 (list operative 1 Apr 2007) [P] | No fixed domestic cycle found [U] | 2005 valuation, effective 2007 [P] | None; new homes also valued at 2005 levels [P] | £400,000 cap; 2023–24 consultation on removing the cap, outcome unconfirmed [P/U] | [DoF NI valuation lists](https://www.finance-ni.gov.uk/topics/valuation-lists); [DoF consultation, Nov 2023](https://minutes.belfastcity.gov.uk/documents/s112576/Appendix%202%20-%20DoF%20revenue%20raising%20consultation%20domestic.pdf) |
| Switzerland | Cantonal and communal wealth tax on property tax values; imputed rental value (*Eigenmietwert*) in federal and cantonal income tax; cantonal property taxes in some cantons | Cantonal; not researched [U] | Cantonal [U] | Cantonal [U] | Cantonal [U] | *Eigenmietwert* abolished with effect from 1 Jan 2029 (Federal Council, 1 Apr 2026), after the 28 Sep 2025 vote [P] | [Federal Council press release, 1 Apr 2026](https://www.admin.ch/de/newnsb/yGTqBPowRqyVh0zPokW-q) |
| Greece | ENFIA (unified property tax) on zone-price "objective values" | Zone prices revised in 2021, applied from 2022 [S] | Not established in this research [U] | 2021–22 nationwide revision (13,808 zones) [S] | None found [U] | Automatic 2025 update via a mass-valuation system was planned; outcome unconfirmed [S/U] | Ministry of Finance Q&A via [CNN Greece, 7 Jun 2021](https://www.cnn.gr/oikonomia/story/269016/nees-antikeimenikes-axies-oi-perioxes-me-tis-megalyteres-ayxiseis-kai-tis-megalyteres-meioseis) [S] |
| Poland | *Podatek od nieruchomości* | No valuation: area-based (zł per m²); value-based (up to 2%) only for structures (*budowle*) [P] | Not applicable; maximum rates indexed yearly by CPI [P] | Not applicable | Annual CPI indexation of rate caps [P] | 2026 caps: 1.25 zł/m² for residential buildings, 35.53 zł/m² for business buildings, 1.45 zł/m² for business land [P]; 2027 caps notice dated 23 Jul 2026 [S] | [Ministry of Finance note on 2026 rates](https://www.podatki.gov.pl/media/1p1hokoz/wysokość-stawek-w-opodatkowaniu-nieruchomości-w-2026-r.pdf) |
| Czechia | *Daň z nemovitých věcí* (immovable property tax) | No valuation: area-based (Kč per m²), except agricultural land (area × official average price) [P] | Not applicable | Not applicable | Inflation coefficient from 2024 (base May 2023 = 100): 1.0 for 2024 [P]; reported 1.0 for 2026 [S] | Example rates: residential buildings 3.50 Kč/m²; building plots 3.50 Kč/m² × size-of-municipality coefficient 1.0–4.5 [P] | [Act No. 338/1992 Coll. (consolidated)](https://www.zakonyprolidi.cz/cs/1992-338) |

#### Country notes

**France**
- Built property is valued by reference to 1 January 1970: "La date de référence des évaluations foncières a été fixée au 1er janvier 1970 (code général des impôts (CGI), ann. III, art. 324 AK)". In Guadeloupe, Guyane, Martinique and Réunion the reference date is 1 January 1975 (CGI ann. II art. 333 A). [P] — [BOFiP, BOI-IF-TFB-20-10-10](https://bofip.impots.gouv.fr/bofip/4889-PGP.html/identifiant=BOI-IF-TFB-20-10-10-20121210)
- The French local-government ministry (DGCL) states: "Les locaux d'habitation sont aujourd'hui évalués par référence aux opérations de révision foncière menées en 1970" (dwellings are today valued by reference to the 1970 revision). [P] — [collectivites-locales.gouv.fr](https://www.collectivites-locales.gouv.fr/index.php/gerer-les-finances-publiques-locales/fiscalite-locale/fiscalite-directe-locale/reforme-des-valeurs-locatives)
- **Housing revision (RVLLH) timeline:**
  - Launched by art. 146 of the 2020 finance law (loi n° 2019-1479 du 28 décembre 2019, as cited in the 2026 amendment text [P]).
  - The DGCL page says integration was "Initialement prévue pour être intégrée dans les bases d'imposition en 2028". "L'article 106 de la loi de finances pour 2026 a prévu un report de l'intégration … dans les bases d'imposition au 1er janvier 2031".
  - New calendar: rental-data campaign during 2028; report to Parliament before 1 September 2029; commissions set sectors and tariffs in 2030; integration in 2031.
  - New values "sera déterminée en fonction de l'état du marché locatif au 1er janvier 2028. Elle sera annuellement mise à jour." (will reflect the rental market at 1 January 2028 and be updated annually).
  - [P] — [DGCL](https://www.collectivites-locales.gouv.fr/index.php/gerer-les-finances-publiques-locales/fiscalite-locale/fiscalite-directe-locale/reforme-des-valeurs-locatives)
  - The earlier postponement from 2026 to 2028 by art. 106 of the 2023 finance law is [S, snippet]; the DGCL page does not mention it.
- The 2026 finance law is loi n° 2026-103 du 19 février 2026 (Conseil constitutionnel décision n° 2026-901 DC of the same day). [S] — [Landot avocats, 20 Feb 2026](https://blog.landot-avocats.net/2026/02/20/publication-de-la-loi-de-finances-et-de-quelques-textes-connexes/), which links Légifrance JORFTEXT000053508155. I did not open Légifrance.
- **Business premises (RVLLP):** revised values apply "Depuis le 1er janvier 2017". Under art. 1518 ter CGI, "les tarifs catégoriels sont mis à jour chaque année et les coefficients de localisation sont revus tous les deux ans", and all collective parameters every 6 years. The sexennial update's integration "est reportée au 1er janvier 2027 aux termes de l'article 106 de la loi de finances pour 2026". [P] — [DGCL](https://www.collectivites-locales.gouv.fr/index.php/gerer-les-finances-publiques-locales/fiscalite-locale/fiscalite-directe-locale/reforme-des-valeurs-locatives)
- **Latest (October 2026):**
  - Amendment n° I-CF1872 to the 2027 finance bill (projet de loi de finances pour 2027, n° 3210) was filed on 7 October 2026 by Philippe Juvin (Droite Républicaine), the finance committee's general rapporteur. The finance committee adopted it on Friday 9 October 2026.
  - It would create CGI art. 1496 ter so that, "À compter du 1er janvier 2028, la valeur locative de chacun des locaux … est révisée à l'occasion de chaque mutation à titre onéreux du local" (from 1 January 2028, each dwelling's rental value is revised whenever it is sold). The revised value would reflect the rental market "à la date de référence du 1er janvier de l'année de la mutation" (at 1 January of the year of sale).
  - [P] — [Assemblée nationale, amendment I-CF1872](https://www.assemblee-nationale.fr/dyn/17/amendements/3210A/CION_FIN/CF1872)
  - As of 20 October 2026 it had been re-tabled for the plenary and the government had not given a view. [S] — [Meilleurtaux, 20 Oct 2026](https://www.meilleurtaux.com/credit-immobilier/actualites/2026-octobre/taxe-fonciere-revision-des-valeurs-locatives-des-2028.html)
  - **Status on 4 November 2026: unconfirmed [U].**
- **Source conflict:** the EC's 2012 annex says France's cadastral value dates "from 1970, no updating" ([EC OCP 119](https://ec.europa.eu/economy_finance/publications/occasional_paper/2012/pdf/ocp119_en.pdf)). That ignores France's annual flat-rate revaluation coefficients and is best read as "no general revaluation". The coefficients themselves are [U] in this session.

**Belgium**
- Cadastral income is defined as the normal net average annual income at a reference date. "Les revenus cadastraux actuels se réfèrent toujours à la période de référence prise en considération pour la dernière péréquation générale des revenus cadastraux, à savoir le 1er janvier 1975" (current cadastral incomes still refer to the reference date of the last general perequation, 1 January 1975), meaning the rents actually charged on that date. [P] — [Gäbele, FIG Congress 2010](https://www.fig.net/resources/proceedings/fig_proceedings/fig2010/papers/ts03j/ts03j_gabele_vanderschueren_4628.pdf)
- The governing rules are arts. 471 ff. of the income tax code (CIR 92), introduced by the law of 19 July 1979 and the royal decree of 10 October 1979. The paper describes the 1975–1980 operation as the last general perequation, the last done by hand ("manuscrite"). [P] — same source
- EC (2012) annex: "The assessed value of the property is based on 1975 values, which has been indexed to the development of the CPI since 1991. Thus, the assessed value is on average below half of the market value." In 2012 regional rates were 1.25% (Brussels and Wallonia) and 2.5% (Flanders), plus municipal surcharges. [P] — [EC OCP 119](https://ec.europa.eu/economy_finance/publications/occasional_paper/2012/pdf/ocp119_en.pdf)
- **Indexation coefficient** (art. 518 CIR 92): "Coefficient 2,3000 en 2026" [P] — [INAMI/RIZIV, circulaire O.A. n° 2025/361 du 6 janvier 2026](https://www.inami.fgov.be/SiteCollectionDocuments/bi2026_1_donnees_de_base_IV.pdf). The 2025 figure, 2.2446, is [S] — [BDO Belgium, 2026](https://www.bdo.be/en-gb/insights/news-alerts/2026/cadastral-income-indexation) (snippet), corroborated by an ULiège academic article (snippet). Some sites label these by income year and others by assessment year, so the same number appears under different years.
- Reported in secondary sources only: a Cour des comptes observation that the lack of perequation creates inequalities, and "La dernière péréquation cadastrale générale a eu lieu en 1980". [S, snippet] — via [jubel.be](https://www.jubel.be/fr/mais-cest-encore-quoi-ce-revenu-cadastral-au-1er-janvier-1975/) and [ULiège article](https://orbi.uliege.be/bitstream/2268/293511/1/MB_2021_RFRL_RevCadast.pdf)

**Italy**
- An ANSA report of 27 December 2011, relaying Agenzia del Territorio data and an Economy Ministry document:
  - For homes, market value averaged 3.73 times the ICI tax base (3.59 for main residences, 3.85 for other homes). Rents averaged 6.46 times the rendite catastali.
  - "le rendite catastali sono state rivalutate nel 1990 con riferimento al biennio 1988-1989" (cadastral incomes were revalued in 1990 with reference to 1988–89), with "nel 1996 … un adeguamento del 5%" (a 5% adjustment in 1996).
  - "La normativa vigente prevedeva una revisione delle rendite ogni dieci anni ma questo non e' mai stato messo in atto" (the law provided for a revision every ten years, but it was never carried out).
  - Some municipalities reclassified micro-zones ("riclassamento delle micro-zone").
  - The government raised the multiplier for cadastral values by 60%.
  - [S] — [ANSA via Blitzquotidiano archive, 27 Dec 2011](https://archivio.blitzquotidiano.it/cronaca-italia/ansa-focus-casa-rendite-37-volte-sotto-mercato-ferme-da-89-1064459)
- EC (2012) annex: "The cadastral values refer to 1988, and an average coefficient of 3.7 is applied. This correction factor was increased by 60% in 2012." [P as an official EU staff document; it is secondary for Italian law] — [EC OCP 119](https://ec.europa.eu/economy_finance/publications/occasional_paper/2012/pdf/ocp119_en.pdf)
- Search summaries (not opened) gave this legal chain:
  - Law 427/1989 authorised the general revision.
  - DM 20 January 1990 set tariffs referring to 1988–89.
  - The TAR Lazio (sentenza 184/1992) annulled the urban tariffs based on market values.
  - DL 388/1992 kept the 1990 rendite in force pending a new revision.
  - DPR 138/1998 is the regulation for revising census zones and tariffs.
  - [S, snippet; the hosting site geototus.altervista.org is not official] — treat as [U] until checked on Normattiva or the Gazzetta Ufficiale.
- Not verified: the 2014 delegation for catasto reform (Law 23/2014, art. 2) and its lapse in 2015; the current IMU multiplier (160 for dwellings, applied to rendita × 1.05); any 2025–26 reform steps. All [U].

**Spain**
- Art. 28.3.a TRLCI: a general collective valuation ("procedimiento de valoración colectiva de carácter general") "sólo podrá iniciarse una vez transcurridos, al menos, cinco años desde la entrada en vigor de los valores catastrales derivados del anterior procedimiento de valoración colectiva de carácter general y se realizará, en todo caso, a partir de los 10 años desde dicha fecha" (may start only 5+ years after the previous values took effect, and shall in any case be done from 10 years after that date). [P] — [TRLCI (Real Decreto Legislativo 1/2004, de 5 de marzo)](https://www.boe.es/buscar/act.php?id=BOE-A-2004-4163)
- Art. 28.2: collective valuation may begin when "se pongan de manifiesto diferencias sustanciales entre los valores de mercado y los que sirvieron de base para la determinación de los valores catastrales vigentes" (substantial differences appear between market values and those underlying current cadastral values). [P] — same
- Art. 32: budget laws may update cadastral values by coefficients, including coefficients "en función del año de entrada en vigor de la correspondiente ponencia de valores del municipio" (by the year the municipality's ponencia took effect). Conditions: at least five years since the last general valuation, substantial and homogeneous market divergence, and a municipal request before 31 May of the prior year. The Minister confirms eligibility by order published in the BOE. [P] — same
- The 2023 state budget (Ley 31/2022) was "prorrogados para el ejercicio 2026" (rolled over into 2026). [P] — [BOE-A-2026-3814 (Resolución de 11 de febrero de 2026)](https://www.boe.es/boe/dias/2026/02/19/pdfs/BOE-A-2026-3814.pdf). How the 2025 and 2026 coefficients were enacted without a new budget law is [U].
- The cadastral directorate issued a circular on 2026 ponencias, "Circular 02.04/2026/P" [S, snippet]. The Catastro site was unreachable (Access log).

**Portugal**
- The IMI code (CIMI) was approved by Decreto-Lei n.º 287/2003, de 12 de novembro (cited in CIMI art. 62(1)(f)). [P] — [CIMI art. 62](https://info.portaldasfinancas.gov.pt/pt/informacao_fiscal/codigos_tributarios/cimi/Pages/cimi62.aspx)
- Art. 138 (wording of Lei n.º 7-A/2016, de 30 de março):
  - Commercial, industrial and service buildings: VPT "são atualizados trienalmente, por aplicação do coeficiente de desvalorização da moeda" (updated every three years by the currency-devaluation coefficient).
  - Housing, building land and other urban property: updated triennially by "75 % do fator de atualização" (75% of that factor).
  - [P] — [CIMI art. 138](https://info.portaldasfinancas.gov.pt/pt/informacao_fiscal/codigos_tributarios/cimi/Pages/cimi138.aspx)
- Art. 62: CNAPU proposes "trienalmente, até 31 de Outubro" the minimum and maximum location coefficients, the zoning and location coefficients "para vigorarem nos três anos seguintes" (for the next three years), and "anualmente, até 30 de Novembro" the average construction value per m². [P] — [CIMI art. 62](https://info.portaldasfinancas.gov.pt/pt/informacao_fiscal/codigos_tributarios/cimi/Pages/cimi62.aspx)
- The Tax Authority's note of 30 March 2017 refers to corrections of VPT "determinado no âmbito da avaliação geral da propriedade urbana" (set in the general valuation of urban property). It reports IMI assessed of €1,347.0m for 2012 and €1,534.7m for 2015. In 2015, 41.3% of registered properties were urban and 58.7% rustic. [P] — [AT, Nota informativa IMI](https://info.portaldasfinancas.gov.pt/pt/dgci/divulgacao/estatisticas/estatisticas_patrimonio/Documents/Nota_Informativa_IMI_e_tranferencias_Municipios.pdf)
- Reported in secondary sources only:
  - The general valuation was carried out mainly in 2012–13 and notified in December 2012 [S, snippet] — [vLex, STA 2012 case summary](https://vlex.pt/vid/acordao-n-0327-12-1044109692)
  - The tax administration had intended to finish the general valuation within 10 years, by 2014 [S, snippet] — [OCC/Vida Económica](https://antigo.occ.pt/fotos/editor2/vidaeconomica29junhoii.pdf)
  - VPT rose 34% in five years, mainly because of the 2012–13 revaluation [S, snippet] — [idealista](https://www.idealista.pt/news/node/29563)

**Netherlands**
- Wet WOZ (Wet van 15 december 1994):
  - Art. 18(1)–(2): "De waarde van een onroerende zaak wordt bepaald naar de waarde die de zaak op de waardepeildatum heeft…" and "De waardepeildatum ligt één jaar voor het begin van het kalenderjaar waarvoor de waarde wordt vastgesteld." (Value is set at the valuation reference date, which lies one year before the start of the calendar year for which the value is fixed.)
  - Art. 22(2): "De bij de beschikking vastgestelde waarde geldt voor een kalenderjaar" (the value in the decision applies for one calendar year).
  - Version in force from 1 July 2026, consulted on 4 November 2026. [P] — [wetten.overheid.nl, BWBR0007119](https://wetten.overheid.nl/BWBR0007119/)
- The average rise in home WOZ values between the 1 January 2024 and 1 January 2025 reference dates was 10.6%. [P] — [Waarderingskamer letter, 21 Nov 2025](https://www.waarderingskamer.nl/documenten/02.-Over-ons/04.-Onze-adviezen/Brief-bijstelling-eigenwoningforfait-2026.pdf)
- About 9.4 million WOZ objects are valued. [P] — [Staat van de WOZ 2025](https://www.waarderingskamer.nl/documenten/02.-Over-ons/Staat-van-de-WOZ/Staat-van-de-WOZ-2025.pdf)
- The year annual revaluation began (commonly given as 2008) is [U] in this session.

**Ireland**
- Valuation history, quoted from the Revenue manual: "The first valuation date was 1 May 2013 which related to the valuation period 2013 to 2021."
  - It originally covered 2013–2016. The Finance (Local Property Tax) (Amendment) Act 2015 extended it to 2019; Ministerial Order S.I. 166/2019 (18 April 2019) to 2020; S.I. 458/2020 (27 October 2020) to 2021.
  - "The second valuation date was 1 November 2021", for 2022–2025 (2021 Act s.20(a) raised the standard period from 3 to 4 years).
  - "The third valuation date is 1 November 2025 which relates to the valuation period 2026 to 2030." The Finance (Local Property Tax and Other Provisions) (Amendment) Act 2025, s.6, raised the period to 5 years, "with the fourth valuation date intended to be 1 November 2030, for the valuation period 2031 to 2035".
  - [P] — [Revenue TDM, LPT Part 04-01 (document updated October 2025)](https://www.revenue.ie/en/tax-professionals/tdm/local-property-tax/part-04/04-01.pdf)
- Bands and rates for 2026–2030: band 1 €0–240,000 at a fixed €95; band 2 €240,001–315,000 at €235; then €105,000-wide bands to €2.15m at 0.0906% on the band midpoint, 0.25% above €1.26m, and 0.3% above €2.1m on actual value. [P] — same

**Northern Ireland**
- "The current valuation list for domestic properties became operative on 1 April 2007 and is based on capital values as at 1 January 2005." [P] — [DoF NI, Valuation lists](https://www.finance-ni.gov.uk/topics/valuation-lists)
- "To ensure the rate burden is distributed fairly, new property being valued for rates purposes is also valued at 1 January 2005 levels."
  - Policy reviews in 2016 and 2019 "have not resulted in any substantive changes to the rating system other than to implement more frequent non-domestic General Revaluations".
  - Consultation launched 7 November 2023 and closed 13 February 2024 on, among other things, removing the maximum capital value cap of £400,000.
  - [P] — [DoF NI, Consultation Paper: Domestic Rating Measures (Nov 2023), copy hosted by Belfast City Council](https://minutes.belfastcity.gov.uk/documents/s112576/Appendix%202%20-%20DoF%20revenue%20raising%20consultation%20domestic.pdf)

**Switzerland**
- Federal Council press release of 1 April 2026, "Bundesrat setzt Abschaffung des Eigenmietwerts auf 2029 in Kraft":
  - The reform enters into force on 1 January 2029. "Damit entfällt auf selbstgenutztem Wohneigentum die Besteuerung des Eigenmietwerts" (taxation of imputed rent on owner-occupied homes ends).
  - Cantons may introduce a special property tax on second homes.
  - Most cantonal finance directors favoured 2029 at the earliest. "Eine noch spätere Inkraftsetzung wäre aus Sicht des Bundesrats nicht vertretbar gewesen" (an even later date would not have been justifiable in the Federal Council's view).
  - [P] — [admin.ch](https://www.admin.ch/de/newnsb/yGTqBPowRqyVh0zPokW-q)
- The vote of 28 September 2025 passed with 57.7% in favour. Until the end of 2028 the imputed rent remains taxable and interest and maintenance deductions remain available. [S, snippet] — [SRF](https://www.srf.ch/news/schweiz/bundesratsentscheid-bundesrat-setzt-abschaffung-des-eigenmietwerts-ab-2029-in-kraft); [law.ch, April 2026](https://law.ch/lawnews/2026/04/systemwechsel-eigenmietwert-faellt-per-1-januar-2029/)
- Cantonal tax values (Steuerwerte / valeurs fiscales), their revaluation cycles and Federal Supreme Court case law were not researched (search budget). [U]

**Greece**
- Ministry of Finance Q&A, 7 June 2021 [S, Ministry text reproduced in the press] — [CNN Greece](https://www.cnn.gr/oikonomia/story/269016/nees-antikeimenikes-axies-oi-perioxes-me-tis-megalyteres-ayxiseis-kai-tis-megalyteres-meioseis):
  - The objective-value system set up in the 1980s relied on local committees, so ministerial decisions often lacked "επαρκούς αιτιολογίας και επιστημονικής μεθοδολογίας" (adequate reasoning and scientific method).
  - In 2018 certified valuers from the Ministry's register were used, but the process "κρίθηκε από το Συμβούλιο της Επικρατείας ως μη επαρκής" (was found insufficient by the Council of State). The framework was amended to comply with its "ακυρωτικών αποφάσεων" (annulment decisions).
  - The reformed system has 13,808 zones covering 98% of the population, up from 85%. Unzoned areas had been taxed at the lowest zone price of their municipality or region.
  - Examples of changes: three Mykonos zones from €1,200 to €3,800 and €3,950; Ithaca from €600 to €2,100 (+250%); Rhodes from €700 to €2,100 (+200%). The article gives zone prices in euros without stating the unit; zone prices are conventionally per m² [U].
  - A new ENFIA was to apply from 2022, with fiscal neutrality.
- June 2018: reporting on the European Commission's compliance report says Greece committed to close "at least 50%" of the remaining gap between objective and market values in 2019 and to align them fully in 2020. A property-valuation unit had been created at the Ministry of Finance and an electronic system was in development. [S] — [iefimerida, 21 June 2018](https://www.iefimerida.gr/news/425422/nees-anatropes-se-antikeimenikes-axies-kai-enfia-tin-epomeni-dietia-ti-tha-allaxei)
- 28 February 2024: ENFIA 2024 was calculated on objective values "που θεσμοθετήθηκαν το 2022" (legislated in 2022). Objections from 125 municipalities were still pending. Zone pricing was being extended to the remaining 1.5% of territory (2,167 areas). Zone prices nationwide were to be "αυτόματα" (automatically) readjusted in 2025 through a new electronic mass-valuation system provided for in the new tax law. [S] — [Powergame.gr](https://www.powergame.gr/forologia/609664/akinita-akyro-se-125-dimous-gia-ti-meiosi-ton-antikeimenikon-axion/)
- Whether the 2025 automatic readjustment happened is **[U]**.

**Poland**
- The local taxes act sets maximum rates; per-m² rates "są corocznie waloryzowane przy zastosowaniu wskaźnika wzrostu cen towarów i usług konsumpcyjnych ogłaszanego przez Prezesa GUS" (are indexed every year by the consumer price index published by the head of the statistics office).
  - 2026 maxima: business land 1.45 zł/m²; residential buildings 1.25 zł/m²; business buildings 35.53 zł/m²; structures (*budowle*) 2% of value.
  - Basis: obwieszczenie Ministra Finansów i Gospodarki z dnia 1 sierpnia 2025 r. (M.P. 2025 poz. 726). Municipal councils set actual rates up to these caps.
  - [P] — [Ministry of Finance, "Wysokość stawek w opodatkowaniu nieruchomości w 2026 r."](https://www.podatki.gov.pl/media/1p1hokoz/wysokość-stawek-w-opodatkowaniu-nieruchomości-w-2026-r.pdf)
- For comparison, in 2012 the rates ran from "PLN 0.67 (residential building) to 21.05 per m²". [P] — [EC OCP 119 annex](https://ec.europa.eu/economy_finance/publications/occasional_paper/2012/pdf/ocp119_en.pdf)
- The notice for 2027 is dated 23 July 2026 (M.P. 2026 poz. 741, published 28 July 2026). [S, snippet] — [infor.pl](https://www.infor.pl/akt-prawny/MPO.2026.209.0000741,obwieszczenie-ministra-finansow-i-gospodarki-w-sprawie-gornych-granic-stawek-kwotowych-podatkow-i-oplat-lokalnych-na-rok-2027.html)

**Czechia**
- Act No. 338/1992 Coll., in force from 1 January 1993 [P] — [zakonyprolidi.cz consolidated text](https://www.zakonyprolidi.cz/cs/1992-338). This is a non-official publisher reproducing the statute. All points below are [P] from that text.
- Tax base:
  - Building plots and other non-agricultural land: area in m² (§5(3)).
  - Agricultural land: area × an official average price per m² set by decree (§5(1)).
  - Buildings: built-up area in m² (§10(1)).
  - Units (flats): floor area × 1.22 or 1.20 (§10(3)).
- Rates (§11, §6):
  - Residential buildings: 3.50 Kč/m².
  - Family recreation buildings: 11.00 Kč/m².
  - Building plots: 3.50 Kč/m², multiplied by 1.0–4.5 depending on municipality size (4.5 in Prague).
  - Municipalities may also apply a local coefficient of 0.5–5.0 (§12).
- Inflation coefficient (§11f):
  - Equals the CPI for May of the preceding year with May 2023 = 100, "nejméně však inflační koeficient platný v bezprostředně předcházejícím zdaňovacím období" (but never below the previous year's).
  - Capped at one-fifth growth per year and "zaokrouhluje na 1 desetinné místo dolů" (rounded down to one decimal place).
  - Agricultural land is always 1.0.
  - The transitional provisions of Act No. 349/2023 Coll. set "Inflační koeficient platný ve zdaňovacím období roku 2024 činí 1,0" (the coefficient for 2024 is 1.0).
- The 2026 coefficient of 1.0 is [S, snippet] — [Daňaři online (dauc.cz)](https://www.dauc.cz/clanky/16035/dan-z-nemovitych-veci-aneb-co-noveho-nas-ceka-v-roce-2026); [muj-pravnik.cz](https://muj-pravnik.cz/inflacni-koeficient/)

#### Court rulings where valuations were challenged
- **Spain, municipal land-value increment tax (plusvalía municipal, IIVTNU), which used cadastral land values to compute gains:**
  - STC 59/2017 (11 May 2017) declared arts. 107.1, 107.2.a) and 110.4 of the TRLRHL unconstitutional "en la medida en que someten a tributación situaciones de inexistencia de incrementos de valor" (insofar as they tax situations where no increase in value exists).
  - STC 126/2019 (31 October 2019) struck down art. 107.4 where the tax exceeds the real gain.
  - STC 182/2021 (26 October 2021) annulled arts. 107.1 (second paragraph), 107.2.a) and 107.4. The Court held that the objective system, "por ser ajeno a la realidad del mercado inmobiliario y de la crisis económica" (being detached from the reality of the property market and the economic crisis), breached the ability-to-pay principle (art. 31.1 CE).
  - Real Decreto-ley 26/2021, de 8 de noviembre, rewrote the tax: a no-taxation rule where no gain exists, and a choice between actual gain and objective coefficients.
  - [P] — [BOE-A-2021-18276 (RDL 26/2021), preamble](https://www.boe.es/boe/dias/2021/11/09/pdfs/BOE-A-2021-18276.pdf)
- **Greece, Council of State:** annulment decisions found the 2018 objective-value process insufficient, prompting the 2021 reform of the legal framework. [S] — [MoF Q&A via CNN Greece, 7 June 2021](https://www.cnn.gr/oikonomia/story/269016/nees-antikeimenikes-axies-oi-perioxes-me-tis-megalyteres-ayxiseis-kai-tis-megalyteres-meioseis). Decision numbers not obtained [U].
- **Belgium / EU law:** Case C-110/17, *Commission v Belgium*, is understood to have held in 2018 that taxing foreign property on actual rental value, while Belgian property is taxed on 1975-based cadastral income, breached free movement of capital. **[U]**: EUR-Lex was blocked and I could not verify the date or holding. Gäbele (2010) notes that art. 478 CIR 92 governs CI based on market value. A "facteur de correction" for foreign-property CI under art. 478 CIR 92 appears in a blog snippet only [S, snippet].
- **Italy:** the Corte costituzionale ruling 352/1993 (apparently on the 1990 tariffs) could not be opened (CAPTCHA). TAR Lazio 184/1992 annulled the urban tariffs according to a non-official site [S, snippet]. Both are [U].

### Inferences
- Age ranking of base dates for residential recurrent taxes, as of November 2026 (my compilation):
  1. France (1970)
  2. Belgium (1975)
  3. Italy (1988–89)
  4. Northern Ireland (2005)
  5. Spain (varies; some municipalities likely much older; see Gaps)
  6. Portugal (largely 2012–13, with triennial inflation updates)
  7. Greece (2021–22)
  8. Ireland (2025)
  9. Netherlands (annual)
  - Poland and Czechia sit outside the ranking because they do not value property.
- Three patterns recur:
  - *Indexation instead of revaluation* (Belgium, France, Italy's multipliers): revenue keeps up with inflation while relative values stay frozen.
  - *Revaluation with neutralising devices* (Ireland, Greece).
  - *Revaluation repeatedly postponed* (France 2026 → 2028 → 2031; Ireland's 2013 values kept to 2021 by four successive extensions).
- France's October 2026 amendment would revalue at each sale. That is a "rolling" revaluation model resembling acquisition-value systems, so neighbours with identical homes could carry different values depending on when they last changed hands. This is an inference from the amendment text; the amendment's own drafting ties each new value to a sector tariff at 1 January of the year of sale.

### Gaps
- Spain: the national distribution of municipalities by year of their last ponencia, and the 2025 and 2026 update coefficients (legal instrument and values). The Catastro site was unreachable and the search budget was exhausted.
- Italy: no primary legal text opened. The 2014 delegation, the current IMU multiplier and the 2025–26 reform status are unverified.
- Belgium: the statutory perequation clause in CIR 92 (often said to require a 10-year cycle, repeatedly suspended) is unverified; C-110/17 is unverified.
- France: the annual revaluation coefficients for 2024–2026 and any 2025 "éléments de confort" (amenity) update are unverified; the plenary fate of amendment I-CF1872 is unknown at 4 November 2026.
- Northern Ireland: outcome of the 2023–24 cap consultation; details of the non-domestic revaluation in force in 2026.
- Switzerland: cantonal valuation dates and cycles; Federal Supreme Court case law on minimum imputed-rent and tax-value levels.
- Greece: legal cycle for zone-price revision; whether the 2025 mass-valuation update took effect; ENFIA's founding law (commonly Law 4223/2013) not verified.
- Portugal: status of rustic (rural) property values, which were reportedly never generally revalued.

## 7. Dated timeline of valuation events (for merging into the global chronology)

### Takeaway
The entries below are formatted for direct merging. Each carries a confidence label and source. Entries are restricted to valuation methods and to the countries in scope for (b), plus method-defining statutes from Germany and Japan.

### Cited Findings
- 1961-01-01 — France: reference date for unbuilt land (propriétés non bâties) values [U, background; not verified]
- 1965 — Arnold Harberger publishes the self-assessment-with-sale-obligation proposal in *Fiscal Policy for Economic Growth in Latin America* [U, reference not re-verified]
- 1969 — Japan: Land Price Publication Act (地価公示法, Act No. 49 of 1969) creates annual "normal price" publication for standard sites by two or more appraisers [P] — [e-Gov](https://laws.e-gov.go.jp/api/1/lawdata/344AC0000000049)
- 1970-01-01 — France: reference date of the cadastral rental values still used for dwellings [P] — [BOFiP](https://bofip.impots.gouv.fr/bofip/4889-PGP.html/identifiant=BOI-IF-TFB-20-10-10-20121210)
- 1975-01-01 — Belgium: reference date of cadastral income (rents actually charged on that day) [P] — [Gäbele 2010](https://www.fig.net/resources/proceedings/fig_proceedings/fig2010/papers/ts03j/ts03j_gabele_vanderschueren_4628.pdf); also the reference date for France's overseas departments [P] — [BOFiP](https://bofip.impots.gouv.fr/bofip/4889-PGP.html/identifiant=BOI-IF-TFB-20-10-10-20121210)
- 1975–1980 — Belgium: last general perequation of cadastral incomes, under the law of 19 July 1979 and the royal decree of 10 October 1979 [P] — [Gäbele 2010](https://www.fig.net/resources/proceedings/fig_proceedings/fig2010/papers/ts03j/ts03j_gabele_vanderschueren_4628.pdf)
- 1980s — Greece: objective-value (zone price) system established, based on local committees [S] — [MoF Q&A via CNN Greece](https://www.cnn.gr/oikonomia/story/269016/nees-antikeimenikes-axies-oi-perioxes-me-tis-megalyteres-ayxiseis-kai-tis-megalyteres-meioseis)
- 1988 — IAAO issues a "Standard on Urban Land Valuation" (later folded into the 2002 mass-appraisal standard) [P] — [IAAO 2025](https://www.iaao.org/wp-content/uploads/Standard_on_Mass_Appraisal.pdf)
- 1990 — Italy: rendite catastali revalued with reference to the 1988–89 biennium [S] — [ANSA 2011](https://archivio.blitzquotidiano.it/cronaca-italia/ansa-focus-casa-rendite-37-volte-sotto-mercato-ferme-da-89-1064459)
- 1991 — Belgium: cadastral income indexed to the CPI from this year [P] — [EC OCP 119](https://ec.europa.eu/economy_finance/publications/occasional_paper/2012/pdf/ocp119_en.pdf)
- 1993-01-01 — Czechia: area-based immovable property tax (Act No. 338/1992) in force [P] — [zakonyprolidi.cz](https://www.zakonyprolidi.cz/cs/1992-338)
- 1994-12-15 — Netherlands: Wet waardering onroerende zaken (WOZ) enacted [P] — [wetten.overheid.nl](https://wetten.overheid.nl/BWBR0007119/)
- 1996 — Italy: 5% adjustment of rendite [S] — [ANSA 2011](https://archivio.blitzquotidiano.it/cronaca-italia/ansa-focus-casa-rendite-37-volte-sotto-mercato-ferme-da-89-1064459)
- 2002 — IAAO consolidates its 1983, 1984 and 1988 standards into a Standard on Mass Appraisal [P] — [IAAO 2025](https://www.iaao.org/wp-content/uploads/Standard_on_Mass_Appraisal.pdf)
- 2003-11-12 — Portugal: Decreto-Lei 287/2003 approves the IMI code with formula-based VPT [P] — [CIMI art. 62](https://info.portaldasfinancas.gov.pt/pt/informacao_fiscal/codigos_tributarios/cimi/Pages/cimi62.aspx)
- 2004-03-05 — Spain: Real Decreto Legislativo 1/2004 (TRLCI) sets the 5-to-10-year general-valuation rule and update coefficients [P] — [BOE](https://www.boe.es/buscar/act.php?id=BOE-A-2004-4163)
- 2005-01-01 — Northern Ireland: valuation date of domestic capital values still in use [P] — [DoF NI](https://www.finance-ni.gov.uk/topics/valuation-lists)
- 2007-04-01 — Northern Ireland: domestic capital-value list becomes operative [P] — [DoF NI](https://www.finance-ni.gov.uk/topics/valuation-lists)
- 2011-12-27 — Italy: Agenzia del Territorio data show home market values at 3.73 times the tax base; multiplier raised by 60% for 2012 [S] — [ANSA 2011](https://archivio.blitzquotidiano.it/cronaca-italia/ansa-focus-casa-rendite-37-volte-sotto-mercato-ferme-da-89-1064459)
- 2012-10 — European Commission paper says "Most countries in the EU use… outdated property values" and describes the "tyranny of the status quo" [P] — [EC OCP 119](https://ec.europa.eu/economy_finance/publications/occasional_paper/2012/pdf/ocp119_en.pdf)
- 2012-12 — Portugal: results of the general valuation of urban property notified [S, snippet] — [vLex](https://vlex.pt/vid/acordao-n-0327-12-1044109692)
- 2013-05-01 — Ireland: first Local Property Tax valuation date [P] — [Revenue TDM](https://www.revenue.ie/en/tax-professionals/tdm/local-property-tax/part-04/04-01.pdf)
- 2013 — IAAO Standard on Ratio Studies sets median ratio 0.90–1.10, PRD 0.98–1.03 and PRB ±0.05 (as restated in 2025) [P] — [IAAO 2025](https://www.iaao.org/wp-content/uploads/Standard_on_Mass_Appraisal.pdf)
- 2015 — Ireland: Finance (LPT) (Amendment) Act 2015 extends use of 2013 values to 2019 [P] — [Revenue TDM](https://www.revenue.ie/en/tax-professionals/tdm/local-property-tax/part-04/04-01.pdf)
- 2016-03-30 — Portugal: Lei 7-A/2016 sets triennial inflation updating of VPT (75% for housing) [P] — [CIMI art. 138](https://info.portaldasfinancas.gov.pt/pt/informacao_fiscal/codigos_tributarios/cimi/Pages/cimi138.aspx)
- 2017-01-01 — France: revised rental values for business premises (RVLLP) take effect [P] — [DGCL](https://www.collectivites-locales.gouv.fr/index.php/gerer-les-finances-publiques-locales/fiscalite-locale/fiscalite-directe-locale/reforme-des-valeurs-locatives)
- 2017-05-11 — Spain: Constitutional Court STC 59/2017 on the cadastral-value-based plusvalía [P] — [BOE RDL 26/2021](https://www.boe.es/boe/dias/2021/11/09/pdfs/BOE-A-2021-18276.pdf)
- 2018 — Greece: zone prices revised using certified valuers; process later found insufficient by the Council of State [S] — [MoF Q&A via CNN Greece](https://www.cnn.gr/oikonomia/story/269016/nees-antikeimenikes-axies-oi-perioxes-me-tis-megalyteres-ayxiseis-kai-tis-megalyteres-meioseis)
- 2018-06-21 — Greece: reported commitment to the European Commission to align objective values fully with market values by 2020 [S] — [iefimerida](https://www.iefimerida.gr/news/425422/nees-anatropes-se-antikeimenikes-axies-kai-enfia-tin-epomeni-dietia-ti-tha-allaxei)
- 2019-04-18 — Ireland: S.I. 166/2019 extends 2013 values to 2020 [P] — [Revenue TDM](https://www.revenue.ie/en/tax-professionals/tdm/local-property-tax/part-04/04-01.pdf)
- 2019-10-31 — Spain: STC 126/2019 (plusvalía exceeding the real gain) [P] — [BOE RDL 26/2021](https://www.boe.es/boe/dias/2021/11/09/pdfs/BOE-A-2021-18276.pdf)
- 2019-12-28 — France: loi n° 2019-1479 (finance law for 2020), art. 146, launches the revision of dwelling rental values [P] — [AN I-CF1872 text](https://www.assemblee-nationale.fr/dyn/17/amendements/3210A/CION_FIN/CF1872)
- 2020-10-27 — Ireland: S.I. 458/2020 extends 2013 values to 2021 [P] — [Revenue TDM](https://www.revenue.ie/en/tax-professionals/tdm/local-property-tax/part-04/04-01.pdf)
- 2021-06-07 — Greece: Ministry of Finance presents the new objective-value system (13,808 zones, 98% population coverage, revenue-neutral ENFIA from 2022) [S] — [CNN Greece](https://www.cnn.gr/oikonomia/story/269016/nees-antikeimenikes-axies-oi-perioxes-me-tis-megalyteres-ayxiseis-kai-tis-megalyteres-meioseis)
- 2021-10-26 — Spain: STC 182/2021 annuls the objective plusvalía base [P] — [BOE RDL 26/2021](https://www.boe.es/boe/dias/2021/11/09/pdfs/BOE-A-2021-18276.pdf)
- 2021-11-01 — Ireland: second LPT valuation date (2022–2025) [P] — [Revenue TDM](https://www.revenue.ie/en/tax-professionals/tdm/local-property-tax/part-04/04-01.pdf)
- 2021-11-08 — Spain: Real Decreto-ley 26/2021 rewrites the plusvalía base [P] — [BOE](https://www.boe.es/boe/dias/2021/11/09/pdfs/BOE-A-2021-18276.pdf)
- 2022 — OECD *Housing Taxation in OECD Countries* says many countries tax "significantly outdated property values" [P] — [OECD brochure](https://www.oecd.org/tax/tax-policy/brochure-housing-taxation-in-oecd-countries.pdf)
- 2022 — Greece: new zone values and restructured ENFIA apply [S] — [Powergame, 28 Feb 2024](https://www.powergame.gr/forologia/609664/akinita-akyro-se-125-dimous-gia-ti-meiosi-ton-antikeimenikon-axion/)
- 2023-11-07 — Northern Ireland: Department of Finance consults (to 13 Feb 2024) on domestic rating measures, including removing the £400,000 cap [P] — [DoF NI consultation](https://minutes.belfastcity.gov.uk/documents/s112576/Appendix%202%20-%20DoF%20revenue%20raising%20consultation%20domestic.pdf)
- 2024 — Czechia: inflation coefficient for the area-based tax introduced (Act 349/2023; 1.0 for 2024) [P] — [zakonyprolidi.cz](https://www.zakonyprolidi.cz/cs/1992-338)
- 2024-02-28 — Greece: ENFIA 2024 computed on 2022 values; 125 municipalities' objections pending; automatic 2025 update planned [S] — [Powergame](https://www.powergame.gr/forologia/609664/akinita-akyro-se-125-dimous-gia-ti-meiosi-ton-antikeimenikon-axion/)
- 2025 — IAAO issues a revised Standard on Mass Appraisal of Real Property [P] — [IAAO](https://www.iaao.org/wp-content/uploads/Standard_on_Mass_Appraisal.pdf)
- 2025-06-19 — Netherlands: Waarderingskamer reports a positive "Staat van de WOZ" for the 1 Jan 2024 valuation date [P] — [Waarderingskamer](https://www.waarderingskamer.nl/documenten/02.-Over-ons/Staat-van-de-WOZ/Staat-van-de-WOZ-2025.pdf)
- 2025-08-01 — Poland: notice of 2026 maximum property tax rates (M.P. 2025 poz. 726) [P] — [Ministry of Finance](https://www.podatki.gov.pl/media/1p1hokoz/wysokość-stawek-w-opodatkowaniu-nieruchomości-w-2026-r.pdf)
- 2025-09-28 — Switzerland: voters approve the second-home property-tax decree linked to abolition of the imputed rental value [P for vote; 57.7% S] — [Federal Council](https://www.admin.ch/de/newnsb/yGTqBPowRqyVh0zPokW-q)
- 2025-11-01 — Ireland: third LPT valuation date (2026–2030); valuation period lengthened to 5 years [P] — [Revenue TDM](https://www.revenue.ie/en/tax-professionals/tdm/local-property-tax/part-04/04-01.pdf)
- 2025-11-21 — Netherlands: Waarderingskamer reports a 10.6% average rise in home WOZ values for the 1 Jan 2025 reference date [P] — [Waarderingskamer](https://www.waarderingskamer.nl/documenten/02.-Over-ons/04.-Onze-adviezen/Brief-bijstelling-eigenwoningforfait-2026.pdf)
- 2026-01-06 — Belgium: INAMI circular applies cadastral-income indexation coefficient 2.3000 for 2026 [P] — [INAMI](https://www.inami.fgov.be/SiteCollectionDocuments/bi2026_1_donnees_de_base_IV.pdf)
- 2026-02-19 — France: loi n° 2026-103 (finance law for 2026), art. 106, postpones dwelling revision to 1 Jan 2031 and the business-premises sexennial update to 1 Jan 2027 [P for content via DGCL; S for law number/date] — [DGCL](https://www.collectivites-locales.gouv.fr/index.php/gerer-les-finances-publiques-locales/fiscalite-locale/fiscalite-directe-locale/reforme-des-valeurs-locatives)
- 2026-04-01 — Switzerland: Federal Council sets 1 Jan 2029 for the end of imputed-rent taxation [P] — [admin.ch](https://www.admin.ch/de/newnsb/yGTqBPowRqyVh0zPokW-q)
- 2026-07-23 — Poland: notice of 2027 maximum rates (published 28 Jul 2026) [S, snippet] — [infor.pl](https://www.infor.pl/akt-prawny/MPO.2026.209.0000741,obwieszczenie-ministra-finansow-i-gospodarki-w-sprawie-gornych-granic-stawek-kwotowych-podatkow-i-oplat-lokalnych-na-rok-2027.html)
- 2026-10-09 — France: finance committee adopts amendment I-CF1872 (revalue each dwelling at sale from 2028) [P] — [Assemblée nationale](https://www.assemblee-nationale.fr/dyn/17/amendements/3210A/CION_FIN/CF1872)
- 2028-01-01 — France (planned): rental-market reference date for revised dwelling values [P] — [DGCL](https://www.collectivites-locales.gouv.fr/index.php/gerer-les-finances-publiques-locales/fiscalite-locale/fiscalite-directe-locale/reforme-des-valeurs-locatives)
- 2029-01-01 — Switzerland (scheduled): imputed rental value abolished [P] — [admin.ch](https://www.admin.ch/de/newnsb/yGTqBPowRqyVh0zPokW-q)
- 2030-11-01 — Ireland (intended): fourth LPT valuation date [P] — [Revenue TDM](https://www.revenue.ie/en/tax-professionals/tdm/local-property-tax/part-04/04-01.pdf)
- 2031-01-01 — France (planned): revised dwelling values enter tax bases [P] — [DGCL](https://www.collectivites-locales.gouv.fr/index.php/gerer-les-finances-publiques-locales/fiscalite-locale/fiscalite-directe-locale/reforme-des-valeurs-locatives)

### Inferences
- Across these entries, the moment when a base date is set and the moment when it is replaced are often separated by decades: France 1970 → 2031 planned; Belgium 1975 → none. Revaluations that did happen (Ireland 2021 and 2025, Greece 2021–22) came with tax-rate or band changes that limited aggregate increases.

### Gaps
- Exact dates are missing for: France's 1974 entry into force of the 1970 values and the 1990 revision law; Italy's DM of 20 January 1990 (date known but text not opened); Portugal's Lei 60-A/2011 (general valuation); Greece's ENFIA law and 2021–22 ministerial decisions; the start of annual WOZ valuation; Spain's 2026 coefficient instrument.

## Access log
- **Web search budget exhausted** after about 25 searches (a shared limit for this run). Not searched afterwards: Spain's 2026 coefficients and ponencia-age statistics; Italy 2014–2026 reform steps; Greece 2025–26; Northern Ireland's non-domestic revaluation in 2026 and the outcome of the cap consultation; Swiss cantonal practice; France's annual coefficients for 2024–26; the Somers system; Korea; verification of the academic literature in Q3; the Harberger references; World Bank and Lincoln Institute reports.
- **IAAO Standard on Ratio Studies** (https://www.iaao.org/wp-content/uploads/Standard_on_Ratio_Studies.pdf): returned an HTML page, not the PDF. Thresholds are taken from the IAAO 2025 mass-appraisal standard's restatement.
- **IAAO Glossary, 3rd ed.** (copy at bangormaine.gov): HTTP 404.
- **EUR-Lex, Case C-110/17** (WebFetch and direct request): empty response / HTTP 202 bot challenge. Not verified.
- **IMF Working Paper WP/13/129** (Norregaard 2013, imf.org): HTTP 403.
- **Lincoln Institute, Dye & England (2010) Policy Focus Report**: HTTP 404 at two URL forms tried.
- **Oxford Academic, Posner & Weyl (2017)**: HTTP 403.
- **Dirección General del Catastro** (catastro.hacienda.gob.es, Circular 02.04/2026/P): connection failed.
- **Portal das Finanças FAQ faqs-00464**: HTTP 404 (CIMI articles on the same site worked).
- **DoF NI "Rating policy questions and answers"**: HTTP 404.
- **BusinessInfo.cz** (Czech 2026 property tax article): HTTP 403.
- **Corte costituzionale** (sentenza 352/1993): Radware CAPTCHA page.
- **Normattiva** (Law 23/2014; Law 160/2019): connection closed mid-exchange, or article text not rendered (dynamic page).
- **bger.ch** (BGE 124 I 145): connection failed.
- **ejustice.just.fgov.be** (Belgian CIR 92 text): connection failed.
- **finance.belgium.be** (cadastral income page): human-verification challenge.
- **Légifrance** (LF 2026, JORFTEXT000053508155): not attempted. The law number and date come from a law-firm blog [S].
- **Worked around** (not failures): Revenue TDM 04-01, BOE-A-2026-3814 and the Polish Ministry of Finance PDF could not be parsed by the fetch tool but were downloaded and converted to text locally, so they count as primary [P]. BOE-A-2026-3814 turned out to concern municipal fiscal-effort reporting, not update coefficients. It is used only for the budget rollover and IBI base-reduction references.
