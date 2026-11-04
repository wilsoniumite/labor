# Land and property taxation and land valuation in Denmark and Estonia, with notes on Sweden, Finland and Norway (1660s to 4 November 2026)

Prepared 4 November 2026. All URLs accessed 4 November 2026.

**Confidence labels used throughout**
- **[P]**: confirmed in a primary source (statute or official legal guidance, parliamentary record, tax-authority or valuation-agency publication, official statistics, or a contemporaneous official report).
- **[S]**: secondary source only (encyclopedia written by named scholars, a peer-reviewed article's abstract, a thesis, journalism, or a bank or industry publication).
- **[U]**: unresolved or unverified. This covers claims seen only in a search-result snippet, claims where sources conflict, and claims I could not open.

**Method notes for the report writer**
- Partway through, the shared web-search budget for this session ran out. After that I worked only from direct reads of official URLs I already had or could build from known patterns: statute databases, statistics APIs, and ministry and agency pages. Several leads therefore stayed unchased; the Access log at the end lists them.
- Danish official legal guidance (*Den juridiske vejledning* 2026-2, issued by the Danish tax administration) was read from the verbatim reproduction at tax.dk. I treat it as primary.
- Danish revenue series come from Statistics Denmark's StatBank table SKAT, read through its public API. Cross-country shares come from Eurostat's `gov_10a_taxag` dataset, last updated 28 October 2026.

---

## 1. Dated timeline (merge-ready)

Format: date, then event, then source and label.

**Denmark: the hartkorn era**
- 1660/1662: Denmark's first cadastre, the *Landgildematriklen*, is compiled in 1660 and valid from 1662. It converts each tenant farm's dues (*landgilde*) into *hartkorn* ("hard grain"), which becomes the base of a *hartkornsskat*. Bornholm is excluded. Sources: [Lex: matrikel](https://lex.dk/matrikel_-_register_og_kortv%C3%A6rk_over_ejendomme), [Lex: hartkorn](https://lex.dk/hartkorn). [S]
- 1664: The cadastre is revised because of many errors; the revision is called the *Amtsstuematriklen*. Source: [Lex: matrikel](https://lex.dk/matrikel_-_register_og_kortv%C3%A6rk_over_ejendomme). [S]
- 1681–1683: All cultivated land in Denmark is surveyed "efter svensk forbillede" (on the Swedish model). Source: [Lex: matrikel](https://lex.dk/matrikel_-_register_og_kortv%C3%A6rk_over_ejendomme). [S]
- 1688: Christian V's "Great Matrikel" comes into force. This is the first nationwide soil grading (*bonitering*): arable land is classed as good, middling or poor and converted into *tønder hartkorn*. Source: [Lex: jordbonitering](https://lex.dk/jordbonitering). [S]
- 1692–1813: The *matrikelskat* (cadastre tax) is 1 rigsdaler 84 skilling per tønde hartkorn per quarter. In 1813 it is merged with several extraordinary taxes, and from 1818 the combined tax is called *landskat*. Source: [Lex: hartkorn](https://lex.dk/hartkorn). [S]
- 1802: A building levy (*bygningsafgift*) is added alongside the hartkorn-based taxes. Source: [Lex: ejendomsskat](https://lex.dk/ejendomsskat). [S]
- Early 1800s to 1826: A new survey and soil grading on a 0–24 scale is carried out: islands east of the Great Belt by 1813, Funen by 1820, Jutland by 1826. Source: [Lex: jordbonitering](https://lex.dk/jordbonitering). [S]
- 1844: The "new matrikel" comes into force as the tax base and stays the tax base until 1903. Source: [Lex: jordbonitering](https://lex.dk/jordbonitering). [S]
- 1863: Market-town plots are also assessed in hartkorn on the 1844 principles. Source: [Lex: matrikel](https://lex.dk/matrikel_-_register_og_kortv%C3%A6rk_over_ejendomme). [S]

**Denmark: from hartkorn to market value**
- 1903-05-15: The Property Tax Act (*Ejendomsskyldsloven*) introduces a "new form of taxation of the country's real property", based on valuation. Sources: [Danmarks Statistik 1906, *Vurderingen til Ejendomsskyld pr. 1. Juli 1904*](https://rss.dst.dk/pubfile/20984/skyld1904) [P]. The tax (*ejendomsskyld*) is initially 0.11% of total property value, and income tax, including tax on the rental value of owner-occupied homes, is introduced at the same time: [Lex: ejendomsskat](https://lex.dk/ejendomsskat). [S]
- 1904-07-01: First general valuation for ejendomsskyld: 357,751 valuations with a total value of DKK 5,358 million. Source: [DST 1964, *Vurderingen af landets faste ejendomme pr. 1. september 1960*, Table 1](https://rss.dst.dk/pubfile/20969/vurd1960). [P]
- 1909: Second general valuation. Source: [DST 1964](https://rss.dst.dk/pubfile/20969/vurd1960). [P]
- 1915-12-22: Law no. 321 orders a general valuation as of 1 July 1916 in which valuation councils must "særskilt fastsætte" (separately fix) the value of the land. Source: [DST 1919, *Vurderingen til Ejendomsskyld pr. 1. Juli 1916*](https://rss.dst.dk/pubfile/20981/skyld1916). [P]
- 1916-07-01: Third general valuation and the first separate land valuation. Land is valued at DKK 3,697 million out of a total of DKK 7,952 million (46.5%). Source: [DST 1919](https://rss.dst.dk/pubfile/20981/skyld1916). [P]
- 1919: The Georgist *Danmarks Retsforbund* (Justice Party) is founded. It decides in 1922 to run in elections. Source: [Lex: Retsforbundet](https://lex.dk/Retsforbundet). [S]
- 1919-10-04: The Land Laws (*jordlovene*) create holdings on "jordrentevilkår" (land-rent terms). In 1957 these holdings are cited as paying the equivalent of full land tax. Source: [Folketingstidende 1956–57, Tillæg A, L 105](https://folketingstidende.dk/samling/19561/lovforslag/L105/19561_L105_som_fremsat.pdf). [P]
- 1922-08-07: Law no. 352 on state taxation of real property. It sets a state land tax (*grundskyld*) of 1.5‰ of land value, plus ejendomsskyld of 1.1‰ on the amount by which total value exceeds land value, with a tax-free deduction of DKK 10,000 per property. It also orders a general valuation as of 1 January 1924. Source: [DST 1926, *Vurderingen til Ejendomsskyld pr. 1. Januar 1924*](https://rss.dst.dk/pubfile/20979/skyld1924). [P]
- 1924: Lex dates the start of grundskyld to 1924. Source: [Lex: grundskyld](https://lex.dk/grundskyld). [S]
- 1926-03-31: Law no. 83 on municipal property taxes introduces municipal grundskyld. Source: [Den juridiske vejledning 2026-2, C.H.4.3](https://tax.dk/jv/ch/C_H_4_3.htm). [P]
- 1926–1965: An increment tax on rising land values (*grundstigningsskyld*) is levied. It is municipal until 1933 and a state tax after that. Source: [Lex: grundstigningsskyld](https://lex.dk/grundstigningsskyld). [S]
- 1926: Retsforbundet enters the Folketing with 1.3% of the vote and 2 seats, and holds seats continuously until 1960. Source: [Lex: Retsforbundet](https://lex.dk/Retsforbundet). [S]
- 1927 and 1932: General valuations. Total land value falls at both, because agricultural values decline. Source: [DST 1964](https://rss.dst.dk/pubfile/20969/vurd1960). [P]
- 1936, then 1945: General valuations. DST's published series lists none between 1936 and 1945. Source: [DST 1964](https://rss.dst.dk/pubfile/20969/vurd1960). [P]
- 1948-03-11: The government appoints a Land Tax Commission (*Grundskyldskommissionen*) to study full land value taxation. Source: [Folketingstidende 1956–57, L 105](https://folketingstidende.dk/samling/19561/lovforslag/L105/19561_L105_som_fremsat.pdf). [P]
- 1950: Retsforbundet reaches its peak: 8.2% of the vote and 12 seats. Source: [Lex: Retsforbundet](https://lex.dk/Retsforbundet). [S]
- 1954-10-14: The Land Tax Commission reports that "hele jordrenten burde tilfalde det samfund, der skaber den" ("the whole land rent should accrue to the society that creates it"). Source: [Folketingstidende 1956–57, L 105](https://folketingstidende.dk/samling/19561/lovforslag/L105/19561_L105_som_fremsat.pdf). [P]
- 1955-04-19 and 1956-01-20: Retsforbundet introduces a "Forslag til lov om jordrente" (Land Rent Bill). In January 1956 only the valuation basis of the government's parallel bill is enacted. Source: [Folketingstidende 1956–57, L 105](https://folketingstidende.dk/samling/19561/lovforslag/L105/19561_L105_som_fremsat.pdf). [P]
- 1956-06-23: Law no. 179 requires general valuation in 1956 and every 4th year thereafter; Law no. 305 of 1 August 1960 repeats the rule. Source: [DST 1964](https://rss.dst.dk/pubfile/20969/vurd1960). [P]
- 1957-01-17: Viggo Starcke, Oluf Pedersen and Søren Olesen (all Retsforbundet) introduce a bill for a voluntary transition to full land tax (*fuld grundskyld*). Source: [Folketingstidende 1956–57, L 105](https://folketingstidende.dk/samling/19561/lovforslag/L105/19561_L105_som_fremsat.pdf). [P]
- 1957-05 to 1960-02: The "triangle government" (*Trekantregeringen*) of the Social Democrats, the Social Liberals (*Radikale Venstre*) and Retsforbundet. Starcke is minister without portfolio, Pedersen fisheries minister and Olesen interior minister. Sources: [Lex: Retsforbundet](https://lex.dk/Retsforbundet) [S]; dates per the [Lex: Trekantregeringen](https://lex.dk/Trekantregeringen) entry, seen only as a search excerpt [U].
- 1960: Retsforbundet loses all its seats. Source: [Lex: Retsforbundet](https://lex.dk/Retsforbundet). [S]
- 1960-09-01: 12th general valuation. Land value is DKK 17,175 million, 25.1% of total property value of DKK 68,419 million. Source: [DST 1964](https://rss.dst.dk/pubfile/20969/vurd1960). [P]
- 1961: Municipalities are allowed to levy a coverage tax (*dækningsafgift*) on business and public properties. Source: [Lex: ejendomsskat](https://lex.dk/ejendomsskat). [S]
- 1965–1966: State land tax revenue falls from DKK 97 million (1965) to 24 million (1966) and is not recorded afterwards. State grundstigningsskyld is DKK 33 million in 1965, has no data for 1966–1970, and is zero from 1971. Source: [Statistics Denmark, StatBank SKAT](https://www.statbank.dk/SKAT). [P]
- 1969-03-14: The finance minister introduces a release levy (*frigørelsesafgift*), charged when farmland is moved into an urban or summer-house zone. Source: [Folketingstidende 1968–69, L 33](https://folketingstidende.dk/samling/19681/lovforslag/L33/19681_L33_som_fremsat.pdf). [P]
- 1969-08-01: 14th general valuation. Source: [Folketingstidende 1968–69, finance minister's introductory speech](https://folketingstidende.dk/samling/19681/lovforslag/L32/19681_L32_fremsaettelsestale.pdf). [P]
- 1972: Release levy revenue first appears in the statistics (DKK 21.4 million). It peaks at DKK 140.9 million in 1978 and 139.5 million in 2000, and is zero from 2015. Source: [StatBank SKAT](https://www.statbank.dk/SKAT). [P]
- Late 1960s–2006: Municipal grundskyld ranges from 6 to 24‰, plus county (*amt*) grundskyld of up to 10‰. Source: [Lex: ejendomsskat](https://lex.dk/ejendomsskat). [S]
- 1996: From this year, agricultural land is taxed at a lower rate than other land. Source: [Lex: grundskyld](https://lex.dk/grundskyld). [S]

**Denmark: owner-occupier tax, caps and the move to state valuation**
- 1998-06-26: Law no. 425 introduces the property value tax on owner-occupied homes (*ejendomsværdiskat*) from income year 2000, initially 10‰ of property value. It replaces the income tax on the imputed rental value of the home (*lejeværdi*). Source: [Den juridiske vejledning C.H.4.2.1](https://tax.dk/jv/ch/C_H_4_2_1.htm). [P]
- 2001/2002: The tax freeze (*skattestop*) is introduced. Law no. 290 of 15 May 2002 caps the ejendomsværdiskat base, and a ceiling on the land tax base (*grundskatteloft*) limits annual growth of the grundskyld base to at most 7%. Sources: [JV C.H.4.2.1](https://tax.dk/jv/ch/C_H_4_2_1.htm); [Engberg report 2014, §4.2.9](https://www.skm.dk/media/Skatteministeriet/Dokumenter/PDF%27er/forbedring-af-ejendomsvurderingen_web.pdf). [P]
- 2002-05-15: Law no. 292 moves the valuation date from 1 January to 1 October and reduces the parameters used in valuation. Sources: [JV C.H.4.2.1](https://tax.dk/jv/ch/C_H_4_2_1.htm); [Engberg report](https://www.skm.dk/media/Skatteministeriet/Dokumenter/PDF%27er/forbedring-af-ejendomsvurderingen_web.pdf). [P]
- 2003: Responsibility for valuation passes from the municipalities to the state (the Ministry of Taxation and SKAT). Sources: [Rigsrevisionen 2013](https://www.rigsrevisionen.dk/Media/4/C/den-offentlige-ejendomsvurdering.pdf) [P]; [Lex: ejendomsskat](https://lex.dk/ejendomsskat) [S].
- 2006-06-07: Law no. 514 makes ejendomsværdiskat a state tax instead of a municipal and county tax. Source: [JV C.H.4.2.1](https://tax.dk/jv/ch/C_H_4_2_1.htm). [P]
- 2007: The counties are abolished, and their 10‰ grundskyld is folded into municipal rates, which then range from 16 to 34‰. Sources: [Lex: ejendomsskat](https://lex.dk/ejendomsskat) [S]; county grundskyld revenue drops to zero in 2007 in [StatBank SKAT](https://www.statbank.dk/SKAT) [P].

**Denmark: breakdown and rebuild of valuation**
- 2011 (owner-occupied homes) and 2012 (other property): The last valuations under the old system. Sources: [ICE 2016](https://regeringen.dk/media/xpfbadgj/nye-og-mere-retvisende-ejendomsvurderinger.pdf) [P]; [Lex: ejendomsskat](https://lex.dk/ejendomsskat) [S].
- 2013-08: The National Audit Office (*Rigsrevisionen*) reports on public property valuation. It finds land-value zones correctly drawn in only 17 of 98 municipalities, and 3 in 4 houses sold in the second half of 2011 valued outside the legal target band. Source: [Rigsrevisionen 2013](https://www.rigsrevisionen.dk/Media/4/C/den-offentlige-ejendomsvurdering.pdf). [P]
- 2013-10: The government's paper *Tillid til ejendomsvurderingerne* ("Trust in property valuations") proposes making the 2013 and 2014 valuations by carrying the 2011 and 2012 valuations forward unchanged. Source: [Government paper, October 2013](https://regeringen.dk/media/ag4jilfk/tillid_til_ejendomsvurderingerne.pdf). [P]
- 2014-09-11: The Engberg committee reports, recommending an objective, statistical valuation system. Sources: [Skatteministeriet, *Forbedring af ejendomsvurderingen*](https://www.skm.dk/media/Skatteministeriet/Dokumenter/PDF%27er/forbedring-af-ejendomsvurderingen_web.pdf) [P]; [Altinget, 11 September 2014](https://www.altinget.dk/artikel/engberg-udvalg-anbefaler-ny-model-til-ejendomsvurderinger) [S].
- Autumn 2016: Political agreement on a new valuation system. Source: [Tryghed om boligbeskatningen, 2 May 2017](https://regeringen.dk/media/zjepu0dl/tryghed-om-boligbeskatningen.pdf). [P]
- 2016-10: The ministry's implementation centre (ICE) publishes its blueprint for the new system. Source: [ICE, *Nye og mere retvisende ejendomsvurderinger*](https://regeringen.dk/media/xpfbadgj/nye-og-mere-retvisende-ejendomsvurderinger.pdf). [P]
- 2017-05-02: The housing tax settlement *Tryghed om boligbeskatningen* ("Security in housing taxation"). It introduces a 20% precautionary deduction, deferral (*indefrysning*) of tax increases, a tax rebate (*skatterabat*), and a lower rate ceiling of 30‰. Source: [Tryghed om boligbeskatningen](https://regeringen.dk/media/zjepu0dl/tryghed-om-boligbeskatningen.pdf). [P]
- 2017-06-08: Law no. 654 enacts the new Property Valuation Act (*ejendomsvurderingsloven*, EVL), in force 1 January 2018. Source: [JV H.A.1](https://tax.dk/jv/ha/H_A_1.htm). [P]
- 2018-04-17: Law no. 278 introduces the precautionary principle (*forsigtighedsprincip*): tax is charged on 80% of the valuation. Source: [JV C.H.4.3.4.1](https://tax.dk/jv/ch/C_H_4_3_4_1.htm). [P]
- 2018-06-20: Executive order no. 804 allocates tasks within the tax administration. The Danish Property Assessment Agency (*Vurderingsstyrelsen*) administers EVL. Source: [JV H.A.1](https://tax.dk/jv/ha/H_A_1.htm). [P] The agency's exact founding date was not confirmed. [U]
- 2023-06-03: Law no. 678 enacts the new Property Tax Act (*ejendomsskatteloven*, ESL), in force 1 July 2023 with effect from 1 January 2024. Source: [JV C.H.4.2.1](https://tax.dk/jv/ch/C_H_4_2_1.htm). [P]
- 2024-01-01: The new property tax rules apply. Grundskyld is capped at 30‰, with per-municipality ceilings for 2024–2028; ejendomsværdiskat is 5.1‰ up to DKK 9.2 million and 14‰ above; both are charged on 80% of the valuation. Sources: [JV C.H.4.3.4.4](https://tax.dk/jv/ch/C_H_4_3_4_4.htm); [JV C.H.4.2.5.1](https://tax.dk/jv/ch/C_H_4_2_5_1.htm). [P] Lex reports the average grundskyld rate falling from 27‰ (2023) to 7.4‰ (2024): [Lex: grundskyld](https://lex.dk/grundskyld). [S]
- 2024–2025: Taxes are charged on *preliminary* 2022 and 2023 valuations, made by model only, with no hearing and no appeal. The 2024 and 2025 valuations are made by indexing earlier ones. Sources: [JV H.A.3.3](https://tax.dk/jv/ha/H_A_3_3.htm); [JV H.A.3.4](https://tax.dk/jv/ha/H_A_3_4.htm). [P]
- 2024-06-04: Law no. 594 amends the indexation rules (EVL §§ 87 b and 88 a). Source: [JV H.A.3.4](https://tax.dk/jv/ha/H_A_3_4.htm). [P]
- 2026-01-13: Vurderingsstyrelsen is reported to have sent final 2022 valuations for about 900,000 properties; more than 120,000 owners have final 2024 valuations. Source: [Faglig Senior, 13 January 2026, updated 9 March 2026](https://fagligsenior.dk/2026/01/13/endelig-nu-kommer-de-nye-ejendomsvurderinger/). [S]
- 2026-06-14: The Ministry of Taxation and Growth announces that the 2026 and 2027 valuations will be made by price-indexing the 2022 and 2023 valuations, because Vurderingsstyrelsen cannot deliver the 2026 valuations in time. Source: [Skatte- og Vækstministeriet press release](https://www.skm.dk/aktuelt/presse-nyheder/pressemeddelelser/ro-om-boligskatten-ejendomsvurderinger-for-2026-og-2027-bliver-prisfremskrevet). [P]
- 2026-06-30: Law no. 615 is enacted, in force 1 July 2026. Among other things, it simplifies the 2026 and 2027 valuations. Source: [JV H.A.3](https://tax.dk/jv/ha/H_A_3.htm). [P]
- 2026-08-10: Nykredit, a mortgage bank, estimates that housing tax for income year 2027 will rise by 21% for an example Copenhagen flat and fall by 1% for an example Frederikshavn house. Source: [Nykredit, 10 August 2026](https://www.nykredit.dk/dit-liv/bolig/nyheder-om-bolig--og-privatokonomi/2026/08/indeksering-af-boliskatter/). [S]

**Estonia**
- 1932: Under the interwar Republic, a state real-estate tax on urban property is set at 15% of the municipal real-estate tax. Tallinn normally revalued every five years. Source: [Sultanjants, TalTech master's thesis 2020, citing Aasmäe 1999 and Lehtmets 2009](https://digikogu.taltech.ee/en/Download/fc77e15a-37dc-4c9c-8383-e692c97643ac). [S]
- 1993-07-01: The Land Tax Act (*Maamaksuseadus*) enters into force. It taxes land only, at 0.5% for the municipality plus 0.5% for the state in 1993–94. Source: [Sultanjants 2020, citing Wenner](https://digikogu.taltech.ee/en/Download/fc77e15a-37dc-4c9c-8383-e692c97643ac). [S]
- 1993: First regular land valuation. Source: [Maa-amet leaflet, *Maa korraline hindamine 2022*](https://maaruum.ee/sites/default/files/documents/2024-12/Maa%20korraline%20hindamine%20voldik%202022.pdf). [P]
- 1994: Land Valuation Act (*Maa hindamise seadus*). Source: [Sultanjants 2020](https://digikogu.taltech.ee/en/Download/fc77e15a-37dc-4c9c-8383-e692c97643ac). [S]
- 1996: Second regular valuation. From this year all land tax revenue goes to municipalities, although the tax stays a state tax. Sources: [Maa-amet leaflet](https://maaruum.ee/sites/default/files/documents/2024-12/Maa%20korraline%20hindamine%20voldik%202022.pdf) [P]; [Sultanjants 2020](https://digikogu.taltech.ee/en/Download/fc77e15a-37dc-4c9c-8383-e692c97643ac) [S].
- 1997–2012: Municipal rates of 0.5–2.5% (0.3–1.0% on agricultural land). From 2012 the range is 0.1–2.5% (0.1–2.0% on agricultural land). Source: [Sultanjants 2020, citing Wenner](https://digikogu.taltech.ee/en/Download/fc77e15a-37dc-4c9c-8383-e692c97643ac). [S]
- 2001: Third regular valuation. These values remain the tax base until the end of 2023. Sources: [Maa-amet leaflet](https://maaruum.ee/sites/default/files/documents/2024-12/Maa%20korraline%20hindamine%20voldik%202022.pdf); [Ministry of Finance guidance 2023](https://agri.ee/sites/default/files/documents/2023-09/KOVidele%20uute%20maamaksum%C3%A4%C3%A4rade%20kehtestamise%20juhend%202023.pdf). [P]
- 2012: The National Audit Office (*Riigikontroll*) audits land tax administration. It finds that the impact of the bill exempting homeowners was not assessed. Source: [Sultanjants 2020](https://digikogu.taltech.ee/en/Download/fc77e15a-37dc-4c9c-8383-e692c97643ac). [S]
- 2013: Land under a registered home (*kodualune maa*) is exempted up to 0.15 ha in towns and densely populated areas and 2.0 ha elsewhere. Source for the start year: [Sultanjants 2020](https://digikogu.taltech.ee/en/Download/fc77e15a-37dc-4c9c-8383-e692c97643ac) [S]. Source for the exemption's terms as still in force in 2025: [Estonian Tax and Customs Board (EMTA)](https://www.emta.ee/eraklient/maksud-ja-tasumine/muud-maksud-ja-nouded/maamaks) [P].
- 2021: A test valuation puts the value of all Estonian land at €30 billion, against €4 billion at the 2001 valuation. Source: [Maa-amet leaflet](https://maaruum.ee/sites/default/files/documents/2024-12/Maa%20korraline%20hindamine%20voldik%202022.pdf). [P]
- Autumn 2022: Regular valuation, with results published on 31 October 2022. Valuation is now due every fourth year (2026, 2030, …), with one buffer year before new values apply. Sources: [Maa-amet leaflet](https://maaruum.ee/sites/default/files/documents/2024-12/Maa%20korraline%20hindamine%20voldik%202022.pdf); [Ministry of Finance guidance 2023](https://agri.ee/sites/default/files/documents/2023-09/KOVidele%20uute%20maamaksum%C3%A4%C3%A4rade%20kehtestamise%20juhend%202023.pdf). [P]
- 2023-07-01: Deadline for municipal councils to set new rates within lower ceilings: 0.1–0.5% for residential land and farm yard land, 0.1–0.5% for other agricultural land, and 0.1–1.0% for other land. Source: [Ministry of Finance guidance 2023](https://agri.ee/sites/default/files/documents/2023-09/KOVidele%20uute%20maamaksum%C3%A4%C3%A4rade%20kehtestamise%20juhend%202023.pdf). [P]
- 2024-01-01: The 2022 values take effect, with each taxpayer's annual increase capped at 10% (minimum step €5). Sources: [Ministry of Finance guidance 2023](https://agri.ee/sites/default/files/documents/2023-09/KOVidele%20uute%20maamaksum%C3%A4%C3%A4rade%20kehtestamise%20juhend%202023.pdf); [Tallinn City](https://www.tallinn.ee/en/maamaks). [P]
- 2025: The national cap is raised to 50% or €20. Rate ceilings rise to 1% for residential land and 2% for other land; agricultural land stays at 0.5%. Sources: [EMTA](https://www.emta.ee/eraklient/maksud-ja-tasumine/muud-maksud-ja-nouded/maamaks) [P]; [ERR, January 2025](https://www.err.ee/1609585508/maamaksu-laekumine-ei-kasva-tanavu-vaid-uhes-vallas) [S].
- 2026-01-01: The area-based home exemption is replaced by an amount-based relief of €0–1,000, set by each municipality, and each municipality sets its own cap on annual increases between 10% and 100%. Source: [EMTA](https://www.emta.ee/eraklient/maksud-ja-tasumine/muud-maksud-ja-nouded/maamaks). [P] Tallinn applies the full €1,000: [Tallinn City](https://www.tallinn.ee/en/maamaks). [P]
- 2026: Regular valuation is under way, with results to be used for land tax from 2028. Sources: [ERR interview with Minister Erkki Keldo, 2026](https://www.err.ee/1610109331/keldo-maahindamine-ei-tahenda-automaatselt-maamaksu-tousu) [S]; the buffer-year rule in the [Ministry of Finance guidance](https://agri.ee/sites/default/files/documents/2023-09/KOVidele%20uute%20maamaksum%C3%A4%C3%A4rade%20kehtestamise%20juhend%202023.pdf) [P].

**Sweden**
- 1979: The Real Property Assessment Act, *Fastighetstaxeringslag* (1979:1152), is passed. Under it, the assessed value (*taxeringsvärde*) is 75% of market value, split into land value (*markvärde*) and building value (*byggnadsvärde*). Source: [SFS 1979:1152](https://www.riksdagen.se/sv/dokument-och-lagar/dokument/svensk-forfattningssamling/fastighetstaxeringslag-19791152_sfs-1979-1152/). [P]
- 2001: A limitation rule (*begränsningsregel*), Lag (2001:906), caps property tax on a home at 4% of household income in defined cases. Source: [Riksdag committee report 2007/08:SkU10](https://www.riksdagen.se/sv/dokument-och-lagar/dokument/betankande/reformerad-beskattning-av-bostader_gv01sku10/html/). [P]
- 2006: Lag (2006:1340) freezes the property tax base for houses at the 2006 level for the 2008–2009 taxations, and caps tax on land value at 2 SEK/m² or SEK 5,000. Source: [2007/08:SkU10](https://www.riksdagen.se/sv/dokument-och-lagar/dokument/betankande/reformerad-beskattning-av-bostader_gv01sku10/html/). [P]
- 2007-10-29: Government bill prop. 2007/08:27, *Avskaffad statlig fastighetsskatt* ("State property tax abolished"), is published. The Riksdag approves it on 17 December 2007. Source: [Regeringen.se](https://www.regeringen.se/rattsliga-dokument/proposition/2007/10/prop.-20070827). [P]
- 2008-01-01: A municipal property fee (*kommunal fastighetsavgift*) replaces the state property tax on homes. For a house it is SEK 6,000 or 0.75% of assessed value if lower, indexed from 2009. Source: [Lag (2007:1398)](https://www.riksdagen.se/sv/dokument-och-lagar/dokument/svensk-forfattningssamling/lag-20071398-om-kommunal-fastighetsavgift_sfs-2007-1398/). [P]

**Finland**
- 1993: The municipal property tax (*kiinteistövero*) begins under the Property Tax Act, *Kiinteistöverolaki* 654/1992. Sources: law number per [Verohallinto](https://www.vero.fi/syventavat-vero-ohjeet/ohje-hakusivu/48219/kiinteistojen-arvostaminen-kiinteistoverotuksessa7/) [P]; start year inferred from the article title "Kiinteistöverotus 25 vuotta" (Verohallinto, *Verotus* 5/2018), listed in the [Eduskunta information package](https://www.eduskunta.fi/fi/lakihankkeiden-tietopaketit/kiinteistoverotuksen-arvostamisperusteet) [S].
- 2018-10-26: The Ministry of Finance announces that the property tax reform is postponed and that taxable values and tax rates will be decided together. 2022-09-02: a further postponement is announced. Source: press-release titles listed by the [Eduskunta](https://www.eduskunta.fi/fi/lakihankkeiden-tietopaketit/kiinteistoverotuksen-arvostamisperusteet). [P for titles; texts not opened]
- 2023: Petteri Orpo's government programme commits to the valuation reform, and project VM095:00/2023 starts on 15 August 2023. The government bill was "intended" for late spring 2026; I could not confirm whether it was submitted. Source: [Eduskunta](https://www.eduskunta.fi/fi/lakihankkeiden-tietopaketit/kiinteistoverotuksen-arvostamisperusteet). [P / U]
- 2026: Property tax is forecast at €2,443 million, of which land accounts for €677 million (27.7%). Source: [Verohallinto, 30 March 2026](https://www.vero.fi/tietoa-verohallinnosta/tilastot/kiinteistoverotilastoj/ennakkotietoa-kiinteistoverotuksesta-2026/). [P]

**Norway**
- 1975-06-06: The Property Tax Act, *eigedomsskattelova* (Act no. 29), makes property tax optional for each municipal council. Source: [Lovdata](https://lovdata.no/dokument/NL/lov/1975-06-06-29). [P]
- 2020: Municipal mergers cut the number of municipalities levying property tax from 371 to 319. Source: [SSB](https://www.ssb.no/offentlig-sektor/kommunale-finanser/artikler/kommuner-med-eiendomsskatt). [P]
- 2024: Property tax revenue is NOK 17.5 billion. Source: [SSB](https://www.ssb.no/offentlig-sektor/kommunale-finanser/artikler/kommuner-med-eiendomsskatt). [P]
- 2026: 329 of 357 municipalities levy property tax, and 249 of them tax homes. Source: [SSB, 15 June 2026](https://www.ssb.no/offentlig-sektor/kommunale-finanser/artikler/kommuner-med-eiendomsskatt). [P]

---

## 2. Denmark before land value: hartkorn and Christian V's 1688 matrikel

### Takeaway
For about 240 years, from 1662 to 1903, Danish land was taxed through *hartkorn*. Hartkorn was a notional measure of a farm's grain-producing capacity, and it was not a market value. The 1688 matrikel built it from a national survey (1681–83) and a soil grading carried out by farmers sent to parishes other than their own. Those 1688 values were not kept up to date, so they had to be replaced by the 1844 matrikel (graded 1806–1826). The 1844 hartkorn remained the tax base until the 1903 reform.

### Cited Findings
**What hartkorn measured**
- Hartkorn ("hard grain") meant rye and barley. One *tønde hartkorn* equalled the value of one tønde of rye or barley, or two tønder of oats. Source: [Lex: hartkorn](https://lex.dk/hartkorn) (Karl-Erik Frandsen and Per Grau Møller, revised 3 October 2024). [S]
- The subdivisions were: 1 tønde = 8 *skæpper*; 1 skæppe = 4 *fjerdingkar*; 1 fjerdingkar = 3 *album*. Sources: [Lex: hartkorn](https://lex.dk/hartkorn); [Lex: matrikel](https://lex.dk/matrikel_-_register_og_kortv%C3%A6rk_over_ejendomme). [S]
- From about 1500, hartkorn was used to convert tenants' varied dues (*landgilde*) to a common value. The 1662 matrikel converted each farm's landgilde into hartkorn as the basis of the *hartkornsskat*. Source: [Lex: hartkorn](https://lex.dk/hartkorn). [S]
- Under the 1688 matrikel, "the tax base was now calculated from the potential use value of each farm's land". Arable land was measured and graded, and the sowing frequency of each parcel was recorded. Source: [Lex: hartkorn](https://lex.dk/hartkorn). [S]

**How the 1688 survey and grading worked**
- The 1688 "Great Matrikel" came into force after a "storstilet opmåling 1681-83 efter svensk forbillede af al dyrket jord i Danmark" (a large-scale survey in 1681–83, on the Swedish model, of all cultivated land in Denmark). Source: [Lex: matrikel](https://lex.dk/matrikel_-_register_og_kortv%C3%A6rk_over_ejendomme). [S]
- It was the first nationwide soil grading. Land was graded as good, middling or poor (*ond*), with separate scales for the islands and Jutland. On the islands the conversions were:
  - good or middling barley, rye and pea land: 2 tønder land = 1 tønde hartkorn;
  - poor, sharp land fit for rye and similar crops: 3 tønder land = 1 tønde hartkorn;
  - good oat land: 4 = 1;
  - middling and poor oat land: 6 = 1.

  Source: [Lex: jordbonitering](https://lex.dk/jordbonitering). [S]
- No cadastral maps were drawn; the values were entered in cadastral registers (*matrikelprotokoller*). Source: [Lex: jordbonitering](https://lex.dk/jordbonitering). [S]
- Bornholm and Sønderjylland had no 1688 matrikel, and calculation methods differed between the islands and northern Jutland. Source: [Lex: hartkorn](https://lex.dk/hartkorn). [S]

**Who valued**
- "Selve taksationen blev foretaget af udvalgte bønder, der ikke måtte taksere jorder i egne sogne" (the valuation itself was done by selected farmers, who were not allowed to value land in their own parishes). Source: [Lex: jordbonitering](https://lex.dk/jordbonitering). [S]
- In the 1844 regrading, valuation was at first done by two assessors, normally land surveyors. From 1807 a single assessor did it. Source: [Lex: jordbonitering](https://lex.dk/jordbonitering). [S]

**Taxes built on hartkorn, and how long they lasted**
- 1692–1813: *matrikelskat* of 1 rigsdaler 84 skilling per tønde hartkorn per quarter. In 1813 it was merged with several extraordinary taxes; from 1818 the merged tax was called *landskat*, at 8⅓ rigsdaler (the Lex summary does not state the unit). Source: [Lex: hartkorn](https://lex.dk/hartkorn). [S]
- From 1802, a building levy (*bygningsafgift*) supplemented the hartkorn taxes. Source: [Lex: ejendomsskat](https://lex.dk/ejendomsskat). [S]
- Hartkorn was "the official basis for land valuation in Denmark from 1662 to 1903". The 1903 reform removed it from state property taxes from 1904, and then gradually from municipal and county taxes. Source: [Lex: hartkorn](https://lex.dk/hartkorn). [S]
- The 1844 grading "trådte i kraft som skattegrundlag, hvilket den var indtil 1903" (took effect as the tax base, which it remained until 1903). Source: [Lex: jordbonitering](https://lex.dk/jordbonitering). [S]
- The 1844 hartkorn was still used for subdividing agricultural properties until 1 July 1970. After the 1920 reunification, Prussian land taxes in Sønderjylland were converted at 40 Thaler *Reinertrag* (net yield) = 1 tønde hartkorn. Source: [Lex: hartkorn](https://lex.dk/hartkorn). [S]
- When the 1903 reform began, DST tabulated each municipality's new valuation alongside its hartkorn and area. Source: [DST 1906, foreword and introduction](https://rss.dst.dk/pubfile/20984/skyld1904). [P]

**What happened as the 1688 values aged**
- "Behovet for en ny landsdækkende bonitering blev påtrængende i begyndelsen af 1800-t., idet 1688-matriklen ikke var blevet vedligeholdt" (the need for a new national grading became pressing in the early 1800s because the 1688 matrikel had not been maintained). Source: [Lex: jordbonitering](https://lex.dk/jordbonitering). [S]
- The new survey produced cadastral maps at 1:4,000 and graded soils "efter deres indvortes Godhed og naturlige Beskaffenhed" (by their inner goodness and natural character) on a scale where the best land was 24. Land graded 12 was expected to give half the yield. The islands east of the Great Belt were finished in 1813, Funen in 1820 and Jutland in 1826, and the result took effect in 1844. Source: [Lex: jordbonitering](https://lex.dk/jordbonitering). [S]
- Because of enclosure (*udskiftning*), the 1844 revision also took account of land improvements, and in large part reused the late-18th-century enclosure maps. Sources: [Lex: hartkorn](https://lex.dk/hartkorn); [Lex: matrikel](https://lex.dk/matrikel_-_register_og_kortv%C3%A6rk_over_ejendomme). [S]
- Historian Per Grau Møller cautions that hartkorn "cannot reliably be related to actual farm production at the micro level". Source: reader-comment reply on [Lex: hartkorn](https://lex.dk/hartkorn). [S]

### Inferences
- Measured from the 1681–83 survey, the 1688 values served as the tax base for about 156 years (to 1844). The hartkorn concept itself lasted about 241 years (1662–1903). This is a textbook case of a valuation that aged out: values fixed by grain-yield potential were never updated, and they drifted from economic reality as agriculture changed through enclosure and land improvement.
- Hartkorn was a yield-capacity (productivity) assessment of agricultural land. It ignored location value and buildings, which were taxed separately by the 1802 building levy. That fits the "by area and yield" stage of a global chronology.

### Gaps
- I could not open Rigsarkivet (Danish National Archives) or danmarkshistorien.dk material on the 1688 matrikel's administration: the names of the survey commissions and the exact dates of the field books (*markbøger*). The Lex entries are the only sources used.
- A search snippet attributed the 1688 split of hartkorn by owner type (nobility about 46%, burgher owners about 17%, church and university about 10%, the rest mostly crown) to a core.ac.uk article. The PDF returned HTTP 403, so the split is **[U]**.
- The unit of the 1818 *landskat* rate (8⅓ rigsdaler) is not stated in the source summary used.

---

## 3. Denmark's move to taxing land value: 1903, 1916, 1922, 1926; Georgism and Retsforbundet; increment taxes

### Takeaway
- **1903:** Denmark replaced hartkorn with taxation of market value set by public valuation boards.
- **1916:** Land was valued separately from buildings for the first time.
- **1922:** A small national land value tax was legislated (1.5‰ of land value), alongside a lower rate on the rest of property value.
- **1926:** A municipal land tax (*grundskyld*) was added. It became the durable core of Danish land taxation.
- **Increment taxes:** grundstigningsskyld taxed rises in land value (1926–1965), and a release levy (*frigørelsesafgift*) on farmland rezoned for urban use produced revenue from 1972 until about 2014.
- **Retsforbundet:** the Georgist Justice Party pushed repeatedly for "full grundskyld", meaning collection of the whole land rent, and sat in government in 1957–60. I could not confirm any specific land-tax law it achieved in office. The national land taxes disappeared in the mid-1960s.

### Cited Findings
**1903: from hartkorn to market value (*værdi i handel og vandel*)**
- The Law of 15 May 1903 introduced "den ved Lov 15. Maj 1903 indførte nye Beskatningsform for Landets faste Ejendomme" (the new form of taxation of the country's real property introduced by the Law of 15 May 1903). Owners filled in forms describing size and use. Valuation councils (*Vurderingsraad*) then drew up valuation lists, and the Superior Assessment Council (*Over-Skyldraadet*) revised them and decided complaints. Source: [DST 1906, *Vurderingen til Ejendomsskyld pr. 1. Juli 1904*, foreword and introduction](https://rss.dst.dk/pubfile/20984/skyld1904). [P]
- The 1903 reform introduced *ejendomsskyld*, at first 0.11% of total property value. Together with the reform's new income tax, which included tax on the rental value of owner-occupied homes, "Fra 1903 blev skattegrundlaget for ejendomsskatter baseret på ejendommens handelsværdi" (from 1903 the property tax base became the property's sale value). Source: [Lex: ejendomsskat](https://lex.dk/ejendomsskat). [S]
- The Engberg committee's 2014 history describes the same shift: alongside income and wealth tax, property taxation moved from "de gamle hartkornsansættelser (en kombination af jordens areal og ydeevne)" (the old hartkorn assessments, a combination of the land's area and yield) to "værdi i handel og vandel fastsat ved en vurdering" (value in ordinary trade, set by a valuation). Property was valued without livestock, equipment or machinery, but with land and buildings, and that definition still applied in 2014. Source: [Engberg report 2014, §4.2.1, pp. 27–28](https://www.skm.dk/media/Skatteministeriet/Dokumenter/PDF%27er/forbedring-af-ejendomsvurderingen_web.pdf). [P for the 2014 statement; S for 1903]

**1915–1916: first separate land valuation**
- Law no. 321 of 22 December 1915 ordered a general valuation for ejendomsskyld as of 1 July 1916. At that valuation the councils were to fix separately "hvad Jorden kunde antages at være værd i ubebygget Stand under Hensyn til Beskaffenhed og Beliggenhed og til en i økonomisk Henseende god Anvendelse" (what the land could be assumed to be worth in an unbuilt state, given its nature and location and an economically good use). Source: [DST 1919, *Vurderingen til Ejendomsskyld pr. 1. Juli 1916*, foreword and §1](https://rss.dst.dk/pubfile/20981/skyld1916). [P]
- Results: DKK 7,952 million in total over 439,000 valuations, of which land was DKK 3,697 million (46.5%). Land's share of property value was 55.4% in rural districts, 37.5% in the capital and 31.5% in provincial towns. Two-thirds of all land value, DKK 2,478 million, lay in rural districts. Source: [DST 1919, §2](https://rss.dst.dk/pubfile/20981/skyld1916). [P]

**1922: the national land value tax**
- The Law of 7 August 1922 changed state property taxation "saaledes, at der nu udskrives en Grundskyld paa 1,5 ‰ af de faste Ejendommes Grundværdi og en Ejendomsskyld, der udskrives med 1,1 ‰ af det Beløb, hvormed Vurderingssummen til Ejendomsskyld overstiger Grundværdien, dog at der gives et skattefrit Fradrag af 10 000 Kr. pr. Ejendom" (so that a land tax of 1.5‰ of land value is levied, plus an ejendomsskyld of 1.1‰ of the amount by which the assessed value exceeds the land value, with a tax-free deduction of DKK 10,000 per property). The valuation rules changed only slightly; one change was that public parks would no longer be valued. Source: [DST 1926, *Vurderingen til Ejendomsskyld pr. 1. Januar 1924*, §1](https://rss.dst.dk/pubfile/20979/skyld1924). [P]
- The 1922 law clarified that agricultural land was to be valued as if part of "en middelstor bondegård i middelgod kultur" (a medium-sized farm in medium-good cultivation), known as the *bondegårdsregel* (farm rule). It still applied in 2014. Source: [Engberg report §4.2.1](https://www.skm.dk/media/Skatteministeriet/Dokumenter/PDF%27er/forbedring-af-ejendomsvurderingen_web.pdf). [P] Lex states that the rule values production land at "omkring en tredjedel af jordens reelle markedsværdi" (around a third of the land's real market value). Source: [Lex: grundskyld](https://lex.dk/grundskyld). [S]

**1924 or 1926? Dating the land tax (sources differ)**
- Lex: "Grundskyld blev indført i Danmark med virkning fra 1924 og var inspireret af georgismen" (grundskyld was introduced with effect from 1924 and inspired by Georgism). Sources: [Lex: grundskyld](https://lex.dk/grundskyld); [Lex: ejendomsskat](https://lex.dk/ejendomsskat). [S]
- Official guidance: "Grundskylden blev indført i 1926 med lov om kommunale ejendomsskatter. Se lov nr. 83 af 31. marts 1926." That 1926 law was repealed by Law no. 678 of 3 June 2023, and the grundskyld rules now sit in the new Property Tax Act. Source: [JV C.H.4.3](https://tax.dk/jv/ch/C_H_4_3.htm). [P]
- Reconciliation: the **state** grundskyld under the 1922 law used the 1 January 1924 valuation, while the **municipal** grundskyld dates from the 1926 law. This is **[P]** for each law separately. Treating them as two layers is my inference, but both primary sources support it.

**Rates over time (the municipal layer)**
- From the late 1960s to 2007, municipalities set grundskyld at 6–24‰, and counties levied up to 10‰ more. After the counties were abolished in 2007, their 10‰ was folded into municipal rates of 16–34‰. Source: [Lex: ejendomsskat](https://lex.dk/ejendomsskat). [S] The pre-2024 minimum of 16‰ and maximum of 34‰ are also stated in [JV C.H.4.3.4.4](https://tax.dk/jv/ch/C_H_4_3_4_4.htm). [P]
- From 1996, agricultural land was taxed at a lower rate than other land. Source: [Lex: grundskyld](https://lex.dk/grundskyld). [S] Production land now pays 1.2–7.2‰, and before 2024 its rate was tied to the general rate minus 14.8 percentage points. Source: [JV C.H.4.3.4.4](https://tax.dk/jv/ch/C_H_4_3_4_4.htm). [P]

**Increment tax: *grundstigningsskyld*, 1926–1965**
- Lex: "en skat på stigninger i jordværdien", introduced in 1926 and abolished in 1965; municipal until 1933, then state. It was levied as a percentage "rente" on the difference between the latest land valuation and a baseline valuation (*nulpunktsvurdering* or *udgangsvurdering*). It was presented as an alternative to full grundskyld, on the reasoning that owners had already paid for past socially created increases but future ones should go wholly or partly to the public. It was abolished because it became very complicated to administer, partly because of a *konjunkturtillæg* (cyclical adjustment) meant to exempt purely inflationary increases. Source: [Lex: grundstigningsskyld](https://lex.dk/grundstigningsskyld). [S]
- Revenue from the state increment tax: DKK 3 million (1947), 9 million (1956), 14 million (1960), 48 million (1964), 33 million (1965); no data for 1966–70; zero from 1971. The series for municipal grundstigningsskyld shows identical figures, which looks like a duplication in the table. Source: [StatBank SKAT](https://www.statbank.dk/SKAT), API series 4.4.13 and 4.4.14. [P; the duplication is **U**]
- The 1960 valuation rules required that land and property values be assessed "dog at der ikke tages hensyn til grundstigningsskylden" (without regard to the increment tax). This stopped the tax's own capitalised burden from depressing the values on which it was charged. Source: [DST 1964, §2](https://rss.dst.dk/pubfile/20969/vurd1960). [P]

**Increment tax: *frigørelsesafgift* (release levy on rezoning)**
- On 14 March 1969 the finance minister introduced a bill for a "frigørelsesafgift m.v. af fast ejendom" (release levy on real property). It was charged when agricultural, nursery or orchard property was moved into an urban zone (*byzone*) or summer-house area, and was computed on the property's "frigørelsesværdi" (release value). The base amount was the last valuation before rezoning plus 50%, or the acquisition price, or the 13th general valuation. Land held under land-rent obligations was exempt. Source: [Folketingstidende 1968–69, L 33](https://folketingstidende.dk/samling/19681/lovforslag/L33/19681_L33_som_fremsat.pdf). [P]
- The minister linked it to a planned "tidssvarende jord- og planlægningslovgivning" (up-to-date land and planning legislation), including the Urban and Rural Zones Act. Source: [Folketingstidende 1968–69, finance minister's speech](https://folketingstidende.dk/samling/19681/lovforslag/L32/19681_L32_fremsaettelsestale.pdf). [P]
- Revenue from release and transfer levies (*frigørelses- og afståelsesafgift*): DKK 21.4 million (1972), 140.9 million (1978), 139.5 million (2000), 33.9 million (2005), 0.2 million (2010), 33.5 million (2014), and zero from 2015 onwards. Source: [StatBank SKAT](https://www.statbank.dk/SKAT), series 4.6.1. [P] The formal repeal date was not found. [U]

**Georgism, the Land Tax Commission and Retsforbundet**
- Lex describes Retsforbundet's ideology as Henry George's ideas combined with Severin Christensen's legal philosophy (*retsliberalisme*). The party wants "fuld grundskyld, dvs. skat på hele afkastet (renten) af en jordbesiddelse" (full land tax, i.e. tax on the whole return, the rent, of a landholding). Its founders included C.N. Starcke, C. Lambek and Signe Bjørner. Source: [Lex: Retsforbundet](https://lex.dk/Retsforbundet). [S] Lex defines full grundskyld the same way: [Lex: jordrentebeskatning](https://lex.dk/jordrentebeskatning). [S]
- Electoral record: in the Folketing continuously 1926–1960, from 1.3% of the vote (1926, 2 seats) to 8.2% (1950, 12 seats); all seats lost in 1960; back in 1973–75 and 1977–81. Source: [Lex: Retsforbundet](https://lex.dk/Retsforbundet). [S]
- 11 March 1948: the government set up the Grundskyldskommission to study "gennemførelse af fuld grundskyld, det vil sige inddragelse af den del af grundrenten, som ikke gennem den almindelige grundskyld og grundstigningsskyld er eller bliver inddraget" (implementing full grundskyld, i.e. capturing the part of ground rent not already captured by ordinary grundskyld and grundstigningsskyld). Source: [Folketingstidende 1956–57, L 105, remarks](https://folketingstidende.dk/samling/19561/lovforslag/L105/19561_L105_som_fremsat.pdf). [P]
- 14 October 1954: the Commission reported. It quoted (p. 154) that because land rent "alene skyldes knapheden på og efterspørgslen efter jord … og efter sin natur ikke er vederlag for nogen indsats af arbejde … synes det nærliggende, at hele jordrenten burde tilfalde det samfund, der skaber den" (arises solely from scarcity of and demand for land … and is by nature no reward for any work … it seems natural that the whole land rent should accrue to the society that creates it).
  - It drafted a "lov om jordrente til staten" (state land rent bill) that would put all Danish landholding on the land-rent terms of the land laws of 4 October 1919: 4% of assessed land value per year as land rent, on top of grundskyld.
  - On the 1950 taxable land value of DKK 7½ billion, that would raise about DKK 300 million.
  - Only 1% would be levied at once. The remaining 3% would follow a buy-out at 25 times the 3%.

  Source: [Folketingstidende 1956–57, L 105](https://folketingstidende.dk/samling/19561/lovforslag/L105/19561_L105_som_fremsat.pdf). [P]
- Retsforbundet introduced a land rent bill on 19 April 1955 and again on 20 January 1956. In January 1956 the government also introduced a bill on valuation and state taxation of real property. Committee agreement was reached only on the valuation basis, which became Law no. 179 of 23 June 1956. Sources: [Folketingstidende 1956–57, L 105](https://folketingstidende.dk/samling/19561/lovforslag/L105/19561_L105_som_fremsat.pdf); [DST 1964](https://rss.dst.dk/pubfile/20969/vurd1960). [P]
- By January 1957 the government had reintroduced the taxation part, including "afvikling af ejendomsskylden og fuld grundstigningsskyld af stigning ud over den i 1956 ansatte grundværdi" (phasing out ejendomsskyld, and full increment tax on increases above the 1956 land value). Source: [Folketingstidende 1956–57, L 105](https://folketingstidende.dk/samling/19561/lovforslag/L105/19561_L105_som_fremsat.pdf). [P that it was proposed; enactment **U**]
- 17 January 1957: Starcke, Pedersen and Olesen introduced a "Lov om frivillig overgang til fuld grundskyld" (Act on voluntary transition to full land tax). Under it:
  - an owner could ask the state to buy out the land value, paid in 4% state bonds or cash;
  - the owner would then pay "som fuld grundskyld en årlig jordrente til staten på 4 pct." of the current land value after deducting improvements, and would no longer pay increment tax;
  - the buy-outs would be financed by a levy of ½% every six months (1% a year) on taxable wealth of DKK 20,000 or more, for 25 years, estimated at about DKK 300 million a year;
  - all land rent revenue would go to tax cuts, "fortrinsvis … for told og forbrugsafgifter" (preferably customs and consumption duties).

  Source: [Folketingstidende 1956–57, L 105](https://folketingstidende.dk/samling/19561/lovforslag/L105/19561_L105_som_fremsat.pdf). [P]
- In government (1957–60), Starcke was minister without portfolio, Oluf Pedersen fisheries minister and Søren Olesen interior minister. Source: [Lex: Retsforbundet](https://lex.dk/Retsforbundet). [S] Lex's article does not name any land-tax law passed by that government.

**Revenue evidence on the end of national land taxes (Statistics Denmark)**
- State grundskyld: DKK 37 million (1947), 51 million (1956), 61 million (1957), 67 million (1960), 84 million (1961), 97 million (1965), 24.4 million (1966), then no record.
- State ejendomsskyld: about DKK 31–33 million a year from 1950 through 1965, then declining (21.8 million in 1970, 10.5 million in 1980, 5.1 million in 1985), and zero by 1995.
- County and municipal grundskyld grew, with the county layer ending in 2007.
- Source for all three series: [StatBank SKAT](https://www.statbank.dk/SKAT), series 4.4.1, 4.4.2, 4.4.3 and 4.4.4. [P]
- Lex: "I løbet af 1950'erne og 1960'erne blev ejendomsskylden afviklet, og samtidig afvikledes også al ejendomsskat til staten" (during the 1950s and 1960s ejendomsskyld was phased out, and with it all property tax to the state). Source: [Lex: ejendomsskat](https://lex.dk/ejendomsskat). [S] This **partly conflicts** with the StatBank series, which shows small state ejendomsskyld receipts into the mid-1980s.
- The land-based taxes (state, county and municipal grundskyld plus state grundstigningsskyld) were 5.1% of all Danish taxes in 1947 and 1950, 4.7% in 1960, 3.2% in 1965, 1.9% in 1990 and 2.5% in 2023. These are my calculations from [StatBank SKAT](https://www.statbank.dk/SKAT). [P data; calculation mine]

### Inferences
- The Danish sequence teaches a three-layer progression:
  1. A yield-based land assessment (hartkorn).
  2. A market-value assessment of whole properties (1903–04).
  3. Separate valuation of the land component (1916), which made a land value tax possible (state 1922/1924; municipal 1926).
- The state and municipal land taxes reused one valuation, so the quality of that single public valuation became the bottleneck. Section 4 shows this mattered after 2011.
- Retsforbundet's main documented contribution lies in the framing it kept in front of parliament: full grundskyld, voluntary buy-outs, and land rent replacing consumption taxes. It also tied its proposals to the 1948–54 Land Tax Commission. Its time in office (1957–60) coincides in the revenue data with a nominally frozen state ejendomsskyld and a rising grundstigningsskyld. That is consistent with the government's 1957 programme, but I could not confirm that the bill was enacted or that Retsforbundet won any specific measure.
- Both increment taxes ran into administrative trouble. Grundstigningsskyld had to separate inflation from real gains, and the release levy depended on rezoning events. Both faded away. This is a recurring pattern worth flagging in the global chronology.

### Gaps
- I could not confirm the enactment, law number or contents of the 1957 government bill on valuation and state taxation (phasing out ejendomsskyld; full grundstigningsskyld above 1956 values). I also could not confirm any specific land-tax measures passed by the 1957–60 government. Searching Folketingstidende 1957–60 would be the next step.
- Abolition of the state grundskyld: the law and date were not found, and the revenue series implies 1965–66.
- The repeal date of the frigørelsesafgift was not found; the revenue series implies about 2014.
- The original 1926 municipal grundskyld rates, and the rates of the grundstigningsskyld, were not found.

---

## 4. Denmark's public valuation system (1903–2026): who valued, how often, the 2011–2014 breakdown, the new system, the 2024 reform, revenue, and the 2024–2026 transition

### Takeaway
- **Who valued, and how often:** from 1904 to 2002, local lay valuation councils valued all property periodically: at irregular intervals of 4–9 years until 1956, then every four years by law from 1956, and later every two years. The state took over in 2003.
- **The breakdown:** quality collapsed. Rigsrevisionen found in 2013 that land-value zones were right in only 17 of 98 municipalities. Valuations were suspended, and the 2011/2012 values were carried forward for a decade, while tax freezes since 2001/02 had already disconnected most bills from the valuations.
- **The new system:** a statistical model run by Vurderingsstyrelsen, with a 20% safety deduction, lower rates, caps, rebates and deferral, took effect for tax in 2024.
- **The transition so far:** delivery has lagged. 2024–25 taxes ran on preliminary model valuations, and valuations for 2024–2027 are, by law, price-indexed rather than freshly made.

### Cited Findings
**Who valued and how often, 1904–2010**
- In 1904 owners filed forms and district valuation councils (*Vurderingsraad*) set values. The Over-Skyldraad revised them and handled complaints. Source: [DST 1906](https://rss.dst.dk/pubfile/20984/skyld1904). [P]
- The general valuations listed by DST were held in 1904, 1909, 1916, 1920, 1924, 1927, 1932, 1936, 1945, 1950, 1956 and 1960; the 1960 valuation is "12. almindelige vurdering pr. 1. september 1960". Law no. 179 of 23 June 1956, repeated in Law no. 305 of 1 August 1960, required valuation "i 1956 og derefter hvert 4. år" (in 1956 and every fourth year after). By 1960 the council-made values were processed by the tax directorate (*Ligningsdirektoratet*), which revised the assessment councils' (*skyldråd*) figures and handled complaints. Source: [DST 1964, §1](https://rss.dst.dk/pubfile/20969/vurd1960). [P]
- Growth of the valuation, 1904 to 1960:
  - number of valuations: 358,000 to 984,000;
  - total property value: DKK 5,358 million to 68,419 million;
  - land value (first assessed separately in 1916): DKK 3,697 million in 1916 to 17,175 million in 1960;
  - land as a share of total property value: 31.4% (1950), 26.6% (1956), 25.1% (1960);
  - area valued in 1960: 41,733 km², 97% of Denmark's 43,033 km².

  Source: [DST 1964, §3 and Table 1](https://rss.dst.dk/pubfile/20969/vurd1960). [P]
- The 14th general valuation was as of 1 August 1969. Source: [Folketingstidende 1968–69](https://folketingstidende.dk/samling/19681/lovforslag/L32/19681_L32_fremsaettelsestale.pdf). [P]
- The 1956 Valuation Act modernised the 1922 law "men de grundlæggende principper blev ikke ændret" (but the basic principles were not changed). Under the law as it stood in 2013:
  - all property was valued every second year as of 1 October: owner-occupied homes in odd years and other property in even years;
  - SKAT did the valuing;
  - new or changed properties were revalued each year (*årsomvurdering*).

  Source: [Engberg report §§4.2.1–4.2.2, 4.2.7](https://www.skm.dk/media/Skatteministeriet/Dokumenter/PDF%27er/forbedring-af-ejendomsvurderingen_web.pdf). [P]
- Before 2003, the work was done by "vurderingsråd og de kommunale sekretariater" (valuation councils and municipal secretariats). SKAT inherited their "relatively limited" IT tools, and its process still involved "manuelle korrektioner baseret på subjektive og vurderingsfaglige skøn" (manual corrections based on subjective professional judgement). Source: [Engberg report §4.4](https://www.skm.dk/media/Skatteministeriet/Dokumenter/PDF%27er/forbedring-af-ejendomsvurderingen_web.pdf). [P]
- In 2003 the Ministry of Taxation took over valuation, "bl.a. med det formål at øge kvaliteten og ensartetheden" (partly to raise quality and consistency). Source: [Rigsrevisionen 2013](https://www.rigsrevisionen.dk/Media/4/C/den-offentlige-ejendomsvurdering.pdf). [P]

**The definitions that survived a century**
- Land value has been defined, in essence unchanged since 1916, as the value of the plot "i ubebygget stand" (unbuilt), given its nature, location and "en i økonomisk henseende god anvendelse" (an economically good use). Sources: [DST 1964, §2](https://rss.dst.dk/pubfile/20969/vurd1960); [Engberg report §4.2.1](https://www.skm.dk/media/Skatteministeriet/Dokumenter/PDF%27er/forbedring-af-ejendomsvurderingen_web.pdf). [P]
- In 1960 property value meant the value of the whole property in ordinary trade ("værdien i handel og vandel"). The term *ejendomsværdi* replaced *ejendomsskyldværdien* in 1956. Source: [DST 1964, §2](https://rss.dst.dk/pubfile/20969/vurd1960). [P]

**Caps layered on top of the valuations (2001/02–2023)**
- From 2002, ejendomsværdiskat was charged on the lowest of three figures: the current value, the 1 January 2001 value plus 5%, or the 1 January 2002 value. The municipal grundskyld base could rise by at most a regulation rate (*reguleringssats*), capped at 7% a year (the *grundskatteloft*), and could not exceed the current land value. Source: [Engberg report §4.2.9](https://www.skm.dk/media/Skatteministeriet/Dokumenter/PDF%27er/forbedring-af-ejendomsvurderingen_web.pdf). [P]
- By 2014, "knap 5 pct. af boligejerne betaler ejendomsværdiskat efter den seneste vurdering, mens 95 pct. betaler … efter 2001- eller 2002-vurderingen" (just under 5% of homeowners paid on the latest valuation; 95% paid on the 2001 or 2002 valuation). The rate was 1% up to DKK 3,040,000 and 3% above. Source: [Engberg report §4.3](https://www.skm.dk/media/Skatteministeriet/Dokumenter/PDF%27er/forbedring-af-ejendomsvurderingen_web.pdf). [P]
- In 2013 the government noted that only "hver 10. boligejer" (one homeowner in ten) paid grundskyld on the current valuation, and one in twenty paid ejendomsværdiskat on it. Source: [*Tillid til ejendomsvurderingerne*, October 2013](https://regeringen.dk/media/ag4jilfk/tillid_til_ejendomsvurderingerne.pdf). [P]

**The breakdown, 2011–2014**
- Rigsrevisionen (August 2013) found the following. Source for all points: [*Beretning til Statsrevisorerne om den offentlige ejendomsvurdering*](https://www.rigsrevisionen.dk/Media/4/C/den-offentlige-ejendomsvurdering.pdf). [P]
  - Property taxes raised about DKK 38 billion in 2012.
  - SKAT had to value more than 1.7 million owner-occupied homes in odd years and about 500,000 business properties in even years.
  - Land-value areas (*grundværdiområder*) were correctly drawn in only 17 of 98 municipalities, so two identical plots risked different values.
  - Of the houses sold in the second half of 2011, 41% were overvalued (valuation above the sale price), 34% were more than 15% below it, and only 25% fell in the legal target band just below the sale price.
  - The share of overvalued properties had grown since 2003.
  - SKAT had "forringet eller fravalgt" (degraded or dropped) parts of the 2010 and 2011 valuations.
  - The ministry had known of problems "generelt siden 2003 og konkret siden 2007" (in general since 2003, and in specific terms since 2007).
  - The government's lawyer (*Kammeradvokaten*) judged SKAT's practice on extraordinary reopening of cases "klart ulovlig" (clearly illegal).
  - SKAT disputed judging accuracy by individual sale prices.
- In October 2013 the government proposed making the 2013 and 2014 valuations by carrying forward the 2011 and 2012 valuations unchanged. They would then be the tax base for 2013–2016, and a new system was promised "fra 2015". Source: [*Tillid til ejendomsvurderingerne*](https://regeringen.dk/media/ag4jilfk/tillid_til_ejendomsvurderingerne.pdf). [P]
- Looking back from 2016: "Ejendomsvurderingerne blev suspenderet tilbage i 2013" (property valuations were suspended back in 2013). Since then, SKAT's 2011 valuation of homes and 2012 valuation of business property "(fratrukket en varierende rabat)" (less a varying discount) had been the tax base. Source: [ICE, October 2016](https://regeringen.dk/media/xpfbadgj/nye-og-mere-retvisende-ejendomsvurderinger.pdf). [P]
- The Engberg committee (chair Peter Engberg Jensen; report 11 September 2014). Source for all points: [*Forbedring af ejendomsvurderingen*, Skatteministeriet, September 2014, p. 16](https://www.skm.dk/media/Skatteministeriet/Dokumenter/PDF%27er/forbedring-af-ejendomsvurderingen_web.pdf) [P]; chair and date per [Altinget](https://www.altinget.dk/artikel/engberg-udvalg-anbefaler-ny-model-til-ejendomsvurderinger) [S].
  - SKAT's model valued 62.9% of detached houses within ±20% of the sale price.
  - The committee's prototype regression model, using projected neighbourhood prices, reached 67.5%: 12.3% of houses undervalued by more than 20% and 20.2% overvalued by more than 20%. Its row-house and flat models reached 81% and 83.4%.
  - Every averaging model overvalued the cheapest properties and undervalued the dearest.
- Valuations of about 1.7 million homes rested on the 3–4% of properties sold each year. Only 1,300–1,400 vacant house plots were sold freely each year nationwide (2,467 in 2009; 1,385 in 2013), and Copenhagen recorded just 128 vacant-plot sales in five years (2009–2013). Source: [Engberg report pp. 46, 166–167](https://www.skm.dk/media/Skatteministeriet/Dokumenter/PDF%27er/forbedring-af-ejendomsvurderingen_web.pdf). [P]

**The rebuild (2016–2018)**
- ICE (*Implementeringscenter for Ejendomsvurderinger*) set out the new system in October 2016. Source for all points: [ICE 2016, §§3.2–3.3, 5.1](https://regeringen.dk/media/xpfbadgj/nye-og-mere-retvisende-ejendomsvurderinger.pdf). [P]
  - Land and property would still be valued separately.
  - Land is valued at its expected price "i ubebygget stand og til den bedste økonomiske anvendelse" (unbuilt and at its best economic use), drawing on municipal planning data.
  - Because few vacant plots sell, land values for houses come from a statistical "grundværdikurve" (land-value curve). It combines vacant-plot sales, "nedrivningssalg" (purchases for demolition) and estate agents' valuations of built plots.
  - Land under flats is valued residually: the value of a new building at optimal use, minus construction cost, shared out by registered allocation figures.
  - Test values for 2015 rose, against SKAT's figures, by an average of 26% (house property values), 47% (house land values), 46% (flat property values) and 330% (flat land values). SKAT's 2011 land values for flats had been "systematisk undervurderede" (systematically undervalued).
- The housing tax agreement of 2 May 2017 was made by the government (V, LA, K) with the Social Democrats, the Danish People's Party and the Social Liberals. Source for all points: [*Tryghed om boligbeskatningen*](https://regeringen.dk/media/zjepu0dl/tryghed-om-boligbeskatningen.pdf). [P]
  - The new valuations were first planned for homes in 2018 and other property in 2019, and the new tax for 2021.
  - Tax would be charged on 20% less than the valuation (the *forsigtighedsprincip*).
  - Increases would be deferred (*indefrosset*): grundskyld increases interest-free until 2021, then all increases in a state scheme at interest.
  - A rebate (*skatterabat*) would ensure that no existing owner paid more in total in 2021, phasing out over about 20 years.
  - The ejendomsværdiskat rate was expected to be about 0.55%, with 1.4% above a threshold of about DKK 6 million (2017 level).
  - The average grundskyld rate was expected to fall "fra 26 promille til knap 16 promille" (from 26‰ to just under 16‰).
  - The rate ceiling would drop from 34‰ to 30‰, and the 16‰ floor would be abolished.
- The new Property Valuation Act (EVL) is Law no. 654 of 8 June 2017, in force 1 January 2018. It is administered by Vurderingsstyrelsen, part of the tax administration, under executive order no. 804 of 20 June 2018. Source: [JV H.A.1](https://tax.dk/jv/ha/H_A_1.htm). [P] The old deductions for land improvements (*grundforbedringsfradrag*) were not carried over, except those already granted. Source: [JV H.A.5](https://tax.dk/jv/ha/H_A_5.htm). [P]
- The 80% tax base was introduced by Law no. 278 of 17 April 2018. The bill's preparatory works (L 211, 2016–17, p. 20) state that a band of ±20% reflects "den naturlige usikkerhed" (the natural uncertainty) in valuing a home. Sources: [JV C.H.4.3.4.1](https://tax.dk/jv/ch/C_H_4_3_4_1.htm); [JV C.H.4.2.5.1](https://tax.dk/jv/ch/C_H_4_2_5_1.htm). [P]

**The property tax reform in force from 1 January 2024**
- The Property Tax Act (ESL), Law no. 678 of 3 June 2023, in force 1 July 2023 with effect from 1 January 2024, consolidated the rules. It introduced the rebate, an increase-limitation scheme for grundskyld, and a loan scheme. Source: [JV C.H.4.2.1](https://tax.dk/jv/ch/C_H_4_2_1.htm). [P]
- **Grundskyld:**
  - The municipal rate can be at most 30‰ (ESL § 28).
  - For 2024–2028, each municipality's rate is capped at a figure in Annex 1 to the act. The caps were fixed by law "så provenuet fra grundskylden i hver enkelt kommune i 2024 svarer til, hvad grundskylden i 2024 ville udgøre med de skatteregler, der var gældende i 2023" (so that each municipality's 2024 grundskyld revenue equals what the 2023 rules would have produced).
  - A municipality may cut its rate, even to 0, and raise it back up to the cap. From 2029 it may set any rate up to 30‰.
  - Production land pays 1.2–7.2‰, capped at its 2023 rate through 2028, and is taxed on 100% of its value (no 20% deduction).

  Sources: [JV C.H.4.3.4.4](https://tax.dk/jv/ch/C_H_4_3_4_4.htm); [JV C.H.4.3.4.1](https://tax.dk/jv/ch/C_H_4_3_4_1.htm). [P]
- Lex reports an average municipal rate of 27‰ in 2023 and 7.4‰ in 2024, ranging from Frederiksberg (3.3‰) to Varde (17.7‰). Source: [Lex: grundskyld](https://lex.dk/grundskyld). [S]
- **Ejendomsværdiskat:** 5.1‰ on the base up to DKK 9,200,000 (2024 level, unchanged in 2025) and 14‰ above. The base is 80% of the previous year's property value, and the threshold is adjusted every second year by a house-price index. Source: [JV C.H.4.2.5.1](https://tax.dk/jv/ch/C_H_4_2_5_1.htm). [P]
- **Rebate:** owners who bought before 2024 receive a rebate so that they do not pay more in 2024 than they would have under the old rules, including the 2001/02 freeze. Sources: [JV C.H.4.2.5.1](https://tax.dk/jv/ch/C_H_4_2_5_1.htm); [JV C.H.4.5](https://tax.dk/jv/ch/C_H_4_5.htm) (ESL §§ 35–43). [P]
- **Dækningsafgift:** Lex says the base for business property moved from the building-value component (*forskelsværdi*) to land value (*grundværdi*) in 2024: [Lex: ejendomsskat](https://lex.dk/ejendomsskat) [S]. StatBank instead shows the series switching in 2022: DKK 2.26 billion on forskelsværdi in 2021, 2.23 billion on land value in 2022: [StatBank SKAT](https://www.statbank.dk/SKAT) [P]. **The sources conflict on the date.**

**The 2024–2026 transition**
- The ordinary 2022 and 2023 valuations "kunne ikke udsendes tids nok" (could not be sent out in time) for the 2024 provisional tax assessments. Taxes for 2024–2025 were therefore computed on *preliminary* valuations. These were made from "den indledende modelberegning … alene baseret på registrerede oplysninger" (the initial model calculation, based only on registered data), without manual checks, without hearing the owner and with no right of appeal. Part of the purpose was to free resources to finish the remaining 2020 valuations and the 2021, 2022 and 2023 valuations. Source: [JV H.A.3.3](https://tax.dk/jv/ha/H_A_3_3.htm). [P]
- The 2024 valuations (homes) and 2025 valuations (other property) are made by indexing the latest 2022 or 2023 valuation with Statistics Denmark price indices. Land values receive an extra 0.8%, because the ministry expected land prices to grow about 0.4% a year faster than property prices. The indexation cannot be appealed; the underlying 2022 or 2023 valuation can, and the reopening deadline was extended by two years. Rules: EVL §§ 87 b and 88 a, amended by Law no. 594 of 4 June 2024. Source: [JV H.A.3.4](https://tax.dk/jv/ha/H_A_3_4.htm). [P]
- By January 2026, Vurderingsstyrelsen reported about 900,000 properties with a final 2022 valuation, and more than 120,000 owners with a final 2024 valuation. The 2025 tax, first computed on a preliminary basis, would be recalculated automatically. Source: [Faglig Senior, 13 January 2026 (updated 9 March 2026)](https://fagligsenior.dk/2026/01/13/endelig-nu-kommer-de-nye-ejendomsvurderinger/). [S]
- 14 June 2026: the 2026 and 2027 valuations will be price-indexed from the 2022 and 2023 valuations, using the same method as for 2024–25. Source for all points: [Ministry press release, 14 June 2026](https://www.skm.dk/aktuelt/presse-nyheder/pressemeddelelser/ro-om-boligskatten-ejendomsvurderinger-for-2026-og-2027-bliver-prisfremskrevet). [P]
  - The reason given: "det ikke er muligt for Vurderingsstyrelsen at udsende 2026-vurderingerne i tide til, at de kan nå at blive indarbejdet i forskudsopgørelsen for 2027" (Vurderingsstyrelsen cannot send out the 2026 valuations in time to be included in the 2027 provisional tax assessments).
  - Owners may ask for an ordinary, appealable 2026 valuation if the indexed value deviates by more than 20% from market value. This option does not cover business property or production land.
  - Minister Jakob Engel-Schmidt: the change frees staff at Vurderingsstyrelsen and the Tax Appeals Agency (Skatteankestyrelsen) to clear backlogs, and is "den mindst bøvlede løsning for boligejerne i den aktuelle situation" (the least troublesome solution for homeowners in the current situation).
- Law no. 615 of 30 June 2026 (in force 1 July 2026) includes "Forenkling af ejendomsvurderingerne for vurderingsårene 2026 og 2027". It also creates a single property category for agricultural, forestry and nature properties from the 1 January 2027 valuation. Source: [JV H.A.3](https://tax.dk/jv/ha/H_A_3.htm). [P]
- Nykredit (10 August 2026) estimated changes in total monthly housing tax for 2027: +21% for an 80 m² Copenhagen flat (+DKK 500 a month, after flat prices rose 20% between 2024 and 2026), +6% Kolding, +13% Næstved, −1% Frederikshavn. It noted that municipalities "er forhindret i at lade dem [promillerne] stige, men de må gerne sætte dem ned" (are prevented from raising the rates, but may lower them). Source: [Nykredit](https://www.nykredit.dk/dit-liv/bolig/nyheder-om-bolig--og-privatokonomi/2026/08/indeksering-af-boliskatter/). [S]
- An October 2025 bill (L 54 of 31 October 2025) widened the tax authority's power to set a preliminary tax base, with retroactive effect from 1 January 2024. Source: [JV C.H.4.2.5.1](https://tax.dk/jv/ch/C_H_4_2_5_1.htm). [P]
- A ruling of the National Tax Tribunal (SKM2026.124.LSR) held that an owner seeking to change a preliminary valuation must document both sale efforts and the expected price. Source: [JV H.A.3.3](https://tax.dk/jv/ha/H_A_3_3.htm). [P]

**Revenue and shares (Statistics Denmark; Eurostat)**
- Municipal grundskyld, in DKK billion:

  | Year | 1947 | 1960 | 1970 | 1980 | 1990 | 2000 | 2010 | 2020 | 2023 | 2024 | 2025 |
  |---|---|---|---|---|---|---|---|---|---|---|---|
  | Revenue | 0.08 | 0.25 | 0.97 | 2.26 | 4.12 | 7.05 | 19.64 | 28.44 | 30.44 | 23.12 | 23.71 |

  County grundskyld (to 2006) was 4.88 billion in 2005. Ejendomsværdiskat: 8.40 billion (2000), 12.61 billion (2010), 14.58 billion (2023), 14.33 billion (2024), 14.56 billion (2025). Source: [StatBank SKAT](https://www.statbank.dk/SKAT), updated 3 June 2026. [P]
- My calculations from StatBank SKAT and NAN1 (GDP):
  - Property taxes (category 4.4, which includes grundskyld and dækningsafgift) plus ejendomsværdiskat were DKK 48.1 billion in 2023: 3.9% of all taxes and 1.7% of GDP.
  - In 2024 they were DKK 41.0 billion: 3.1% of all taxes and 1.4% of GDP.
  - In 2025 they were DKK 41.8 billion: 3.0% of all taxes and 1.3% of GDP.
  - Grundskyld alone was 2.5% of taxes and 1.09% of GDP in 2023, and 1.7% of taxes and 0.76% of GDP in 2025.

  Sources: [StatBank SKAT](https://www.statbank.dk/SKAT); [StatBank NAN1](https://www.statbank.dk/NAN1). [P data; calculation mine]
- Eurostat records Denmark's "taxes on land, buildings and other structures" (ESA category D.29A) at 1.2% of GDP and 2.7% of total taxes in 2023, and 0.9% and 2.0% in 2024–2025. Ejendomsværdiskat, classed as "current taxes on capital" (D.59A), is 0.5% of GDP and 1.1% of total taxes. Source: [Eurostat gov_10a_taxag](https://ec.europa.eu/eurostat/databrowser/view/gov_10a_taxag/default/table?lang=en). [P]
- **Cross-country snapshot, 2024** (Eurostat D.29A, as % of GDP and % of total taxes): Denmark 0.9 / 2.0; Finland 0.8 / 1.9; Sweden 0.6 / 1.5; Norway 0.3 / 0.8; Estonia 0.1 / 0.4. In 2025 Estonia rises to 0.2 / 0.5. Source: [Eurostat gov_10a_taxag](https://ec.europa.eu/eurostat/databrowser/view/gov_10a_taxag/default/table?lang=en). [P]

**Evidence on who bears the land tax (capitalisation)**
- Høj, Jørgensen and Schou use variation in land tax rates created by Denmark's 2007 local government reform. They find that land tax changes are fully capitalised into house prices under reasonable discount rates: the incidence of a permanent change falls on the owner at the time it is announced, and later buyers are compensated through lower prices. Source: Anne Kristine Høj, Mads Rahbek Jørgensen and Poul Schou, "Land Tax Changes and Full Capitalisation", *Fiscal Studies* 39(2) (2018): 365–380, [DOI 10.1111/1475-5890.12163](https://doi.org/10.1111/1475-5890.12163); abstract at [EconPapers](https://econpapers.repec.org/RePEc:wly:fistud:v:39:y:2018:i:2:p:365-380). [S, abstract read]
- Lex likewise states that grundskyld changes are normally expected to be capitalised into land prices, so future buyers "reelt ikke vil blive beskattet" (are not in reality taxed). Source: [Lex: grundskyld](https://lex.dk/grundskyld). [S]

### Inferences
- Denmark shows two different ways a valuation system can fail. The first is quiet decoupling: from 2002 the tax freeze and the 7% base cap meant 95% of owners paid on 2001/02 values. The second is visible collapse: audited inaccuracy (2013), suspension (2013–2023), then indexation in place of fresh valuation (2024–2027).
- In 2024 the reform cut rates sharply (27‰ to 7.4‰ on average), so that much higher, more current land values would not raise revenue. Recorded grundskyld revenue nevertheless fell from DKK 30.4 billion (2023) to 23.1 billion (2024), even though the per-municipality caps were designed to keep revenue neutral. One plausible explanation is that StatBank records tax net of the state-financed rebate and of deferrals. **I could not confirm this [U].**
- Statistical valuation solved the consistency problem that Rigsrevisionen identified. It did not, by 2026, solve the throughput problem: Vurderingsstyrelsen still could not deliver fresh valuations on schedule.

### Gaps
- The date and law number of the 2013 suspension, and of the later laws carrying forward the 2011/2012 values to 2015 and beyond, were not found; the October 2013 proposal is documented.
- Vurderingsstyrelsen's founding date: I have only the June 2018 executive order.
- When the first new (2020-vintage) valuations were sent, and how far behind delivery was at each point: only the January 2026 snapshot (about 900,000 final 2022 valuations) was found, and that came from secondary journalism.
- The decision postponing the new tax from 2021 to 2024 (reportedly 2020) was not found in a primary source.
- The reason for the 24% fall in recorded grundskyld revenue in 2024 is unresolved.
- Evidence disputing capitalisation: I found no Danish study contradicting Høj et al. (2018). Absence in this session is not evidence that none exists.
- I did not find an assessment of how the 2026 general election, if one was held, affected housing tax policy.

---

## 5. Estonia: the 1993 Land Tax Act, valuations of 1993, 1996 and 2001, the 2013 home exemption, the 2022 valuation and its 2024–2026 phase-in

### Takeaway
- **Design:** since 1993 Estonia has taxed land only, not buildings, at municipal rates on state-set taxable values.
- **Ageing values:** after three valuations (1993, 1996, 2001), values were frozen at 2001 levels for 22 years. By then land values had risen between 3-fold and 30-fold depending on location.
- **The new values:** the 2022 mass valuation took effect in 2024 alongside sharply lower rate ceilings and a 10% annual cap. The cap was loosened to 50% or €20 in 2025, and handed to municipalities (10–100%) in 2026.
- **The home exemption:** the 2013 area-based exemption for home land became a municipal relief of €0–1,000 in 2026.
- **Revenue:** flat at about €58–59 million a year from 2012 to 2024, then €80.5 million in 2025.
- **Next round:** a 2026 valuation is under way for use from 2028.

### Cited Findings
**Before 1993**
- In the interwar Republic, cities taxed real estate under a law of the Russian Provisional Government. City councils could tax land and buildings separately and organise general revaluations. A 1932 law added a state tax on urban real estate equal to 15% of the municipal tax. Real estate tax was about 9% of tax revenue in 1936–37, and Tallinn revalued as a rule every five years. Source: [Sultanjants, *Maamaksu laekumiste analüüs…*, TalTech master's thesis 2020, pp. 23–25, citing Aasmäe 1999 and Lehtmets 2009](https://digikogu.taltech.ee/en/Download/fc77e15a-37dc-4c9c-8383-e692c97643ac). [S]

**The 1993 Land Tax Act (*Maamaksuseadus*): design**
- In force from 1 July 1993, as part of the land and tax reform. Its aims, citing Tomson 2000 and Lehis 2009 [S]:
  - to encourage more efficient use of restituted and privatised land;
  - to raise revenue for local government;
  - to counter the fear that owners would hold restituted land for speculation "kui maa omamine midagi ei maksa" (if owning land cost nothing).

  Land alone was chosen as the base, for economic, political and practical reasons. Source: [Sultanjants 2020, pp. 25–26](https://digikogu.taltech.ee/en/Download/fc77e15a-37dc-4c9c-8383-e692c97643ac). [S]
- A government development plan of 1998 foresaw replacing the land tax with a full property tax in 2002. This did not happen. Source: [Sultanjants 2020, p. 25, citing Aasmäe 1999](https://digikogu.taltech.ee/en/Download/fc77e15a-37dc-4c9c-8383-e692c97643ac). [S]
- Mechanics:
  - the tax is charged on the land's taxable value (*maa maksustamishind*), set under the Land Valuation Act;
  - payers are owners, or users where the land reform is unfinished;
  - there are exemptions for public roads and waters, churches, municipal land and some other categories.

  Source: [Sultanjants 2020, pp. 26–27 (MaaMS §§ 1, 3, 4)](https://digikogu.taltech.ee/en/Download/fc77e15a-37dc-4c9c-8383-e692c97643ac). [S]
- The land tax "on maamaksuseadusega kehtestatud riiklik maks. Maamaks laekub täies ulatuses kohaliku omavalitsuse eelarvesse" (is a state tax established by the Land Tax Act, and its revenue goes entirely to the local government budget). The Tax and Customs Board (EMTA) calculates and bills it. Source: [EMTA](https://www.emta.ee/eraklient/maksud-ja-tasumine/muud-maksud-ja-nouded/maamaks). [P]
- Rate history (Sultanjants 2020, p. 28, table citing Wenner, *Land Use Policy* 77: 790–800, which the thesis dates 2016) [S]:

  | Period | Municipal rate | State rate |
  |---|---|---|
  | 1993–94 | 0.5% | 0.5% |
  | 1995 | 0.3–0.7% | 0.5% |
  | 1996 | 0.8–1.2% | none |
  | 1997–2012 | 0.5–2.5% (0.3–1.0% agricultural) | none |
  | From 2012 | 0.1–2.5% (0.1–2.0% agricultural) | none |

  Source: [Sultanjants 2020](https://digikogu.taltech.ee/en/Download/fc77e15a-37dc-4c9c-8383-e692c97643ac).
- Tallinn charged 2.5% from 2012 to 2023, under a council regulation of 16 June 2011. Source: [Tallinn City](https://www.tallinn.ee/en/maamaks). [P]

**Valuations of 1993, 1996 and 2001, and the long gap to 2022**
- The earlier regular valuations were held "1993., 1996. ja 2001. aastal". Source: [Maa-amet, *Maa korraline hindamine 2022* leaflet](https://maaruum.ee/sites/default/files/documents/2024-12/Maa%20korraline%20hindamine%20voldik%202022.pdf). [P]
- The 1993 valuation faced major obstacles: no developed market, too few qualified appraisers, and gaps in methodology and data. The OECD and the Finnish and Danish governments helped design a market-value mass valuation. Fewer than 3% of taxpayers contested the 1996 results. Source: [Sultanjants 2020, pp. 30–32, citing J. Malme and T. Tiits, "The Land Tax in Estonia", in Malme and Youngman (eds.), *The Development of Property Taxation in Economies in Transition*, World Bank, 2001, pp. 27–38](https://digikogu.taltech.ee/en/Download/fc77e15a-37dc-4c9c-8383-e692c97643ac). [S]
- Under the old Land Valuation Act, regular valuation was not periodic: the government ordered it, on the environment minister's proposal, when market values had changed significantly. Maa-amet explained the post-2001 delay this way:
  - valuing at the boom's peak would have produced unjustifiably high values, so the market was left to calm;
  - prices then fell, and values would have come out too low.

  In 2016 Maa-amet proposed four-yearly valuation separated from taxation, but "plaan ei leidnud poliitilist toetust" (the plan found no political support). Source: [Sultanjants 2020, pp. 32–33](https://digikogu.taltech.ee/en/Download/fc77e15a-37dc-4c9c-8383-e692c97643ac). [S]
- "Viimasest korralisest hindamisest möödunud 20 aasta jooksul on maa väärtus turul kordades kasvanud. Mõnel maaüksusel on väärtus kasvanud 3 korda, mõnel 30 korda." (In the 20 years since the last valuation, market land values have multiplied: some parcels threefold, some thirtyfold.) Owners whose land had risen relatively less were therefore paying "ebaõiglaselt rohkem" (unfairly more). Source: [Maa-amet leaflet](https://maaruum.ee/sites/default/files/documents/2024-12/Maa%20korraline%20hindamine%20voldik%202022.pdf). [P]

**The 2013 home-land exemption (*kodualune maa*)**
- From 2013, owners or users were exempt for residential land or farm yard land carrying a building in which they were registered as resident. The limit was 0.15 ha in towns and areas designated densely populated, and 2.0 ha elsewhere. Source: [Sultanjants 2020, p. 29 (MaaMS § 11)](https://digikogu.taltech.ee/en/Download/fc77e15a-37dc-4c9c-8383-e692c97643ac). [S]
- The same limits still applied in 2025: "2025. aastal oli maamaksust vabastatud kodualune maa, mille suurus oli tiheasustusega alal … 0,15 hektarit ja mujal kuni 2 hektarit" (in 2025, home land of up to 0.15 ha in densely populated areas and up to 2 ha elsewhere was exempt). Source: [EMTA](https://www.emta.ee/eraklient/maksud-ja-tasumine/muud-maksud-ja-nouded/maamaks). [P]
- The 2012 audit by the Riigikontroll found that "koduomanikke maamaksust vabastava seaduseelnõu menetlemisel jäeti hindamata seaduse rakendamise mõju" (the impact of the homeowner-exemption bill was not assessed during its passage). Source: [Sultanjants 2020, p. 29](https://digikogu.taltech.ee/en/Download/fc77e15a-37dc-4c9c-8383-e692c97643ac). [S]

**The 2022 valuation: method and who valued**
- The valuation is market-based mass valuation, "statistiline üldistus" (a statistical generalisation), carried out by Maa-amet with professional appraisers. Source for all points: [Maa-amet leaflet](https://maaruum.ee/sites/default/files/documents/2024-12/Maa%20korraline%20hindamine%20voldik%202022.pdf). [P]
  - It uses registry data and transactions, with no site visits.
  - Estonia is divided into 8 location classes, and 5 models cover building land, building rights (central Tallinn and Tartu), agricultural land, forest land (land only, excluding the timber) and land with no active market.
  - The base value for building land is the average of the area mean and the 10 nearest transactions.
  - Residential land exceeds €300/m² in central Tallinn and Tartu, while most of Estonia lies in the lowest class at €0.3–1.0/m².
  - Results were published on 31 October 2022 and used from 1 January 2024.
  - The 2021 test valuation raised the total value of Estonian land from €4 billion (2001) to €30 billion.
- Municipalities have no role in valuation. Valuation is now due every fourth year (2022, 2026, 2030), and one buffer year separates valuation from use (MaaMS § 1(2)). Source: [Ministry of Finance, guidance to municipalities on setting land tax rates after the valuation (2023)](https://agri.ee/sites/default/files/documents/2023-09/KOVidele%20uute%20maamaksum%C3%A4%C3%A4rade%20kehtestamise%20juhend%202023.pdf). [P]

**The 2024 phase-in: lower rate ceilings and a cap on increases**
- Maximum rates fell "2,5–5 korda" (by a factor of 2.5–5) from 2024. Councils had to set new rates by 1 July 2023 within these ranges: 0.1–0.5% for residential land and farm yard land, 0.1–0.5% for other agricultural land, and 0.1–1.0% for other land. The ministry supplied each municipality with a "tasakaalumäär" (balance rate) at which 2024 revenue would equal 2023 revenue. Source: [Ministry of Finance guidance 2023](https://agri.ee/sites/default/files/documents/2023-09/KOVidele%20uute%20maamaksum%C3%A4%C3%A4rade%20kehtestamise%20juhend%202023.pdf). [P]
- Cap (MaaMS § 8¹): no taxpayer's land tax may rise by more than 10% a year. Where 10% is less than €5, the rise is €5. In the ministry's example, a €30 bill that would jump to €70 instead reaches it "11 aasta jooksul" (over 11 years). Exemptions and changes in a parcel's area or use fall outside the cap. Source: [Ministry of Finance guidance 2023](https://agri.ee/sites/default/files/documents/2023-09/KOVidele%20uute%20maamaksum%C3%A4%C3%A4rade%20kehtestamise%20juhend%202023.pdf). [P]
- The ministry framed the tax's purpose as: "Piiratud ressursina peab maa olema kasutuses. Maamaks peab suunama omanikke ja rentnikke maad kasutama ühiskonna heaolu ja majanduskasvu edendaval viisil." (As a limited resource, land must be in use; land tax should steer owners and tenants to use land in ways that promote social welfare and economic growth.) Source: [Ministry of Finance guidance 2023](https://agri.ee/sites/default/files/documents/2023-09/KOVidele%20uute%20maamaksum%C3%A4%C3%A4rade%20kehtestamise%20juhend%202023.pdf). [P]
- Tallinn set 0.5% for residential and profit-yielding land and 1% for other land from 1 January 2024. The rates were unchanged in 2026. Source: [Tallinn City](https://www.tallinn.ee/en/maamaks). [P]

**2025 and 2026: loosening the cap, and municipalisation**
- 2025: "maamaksu tõusu üleriigiline piirmäär 50 protsenti või 20 eurot" (the national cap on increases was 50% or €20). Source: [EMTA](https://www.emta.ee/eraklient/maksud-ja-tasumine/muud-maksud-ja-nouded/maamaks). [P]
- ERR reported in January 2025 the following. Source: [ERR, January 2025](https://www.err.ee/1609585508/maamaksu-laekumine-ei-kasva-tanavu-vaid-uhes-vallas). [S]
  - In 2024, 63 of 79 municipalities used the maximum rate, yet many still saw revenue fall.
  - For 2025 the rate ceilings rose to 1% (residential and garden land) and 2% (other land), with agricultural land staying at 0.5%.
  - 26 municipalities raised rates, 39 kept them, 11 cut them and 3 did both for different categories.
  - Forecast 2025 revenue gains: Tallinn +€9.5 million, Tartu +€1.2 million, Viimsi about +€1 million. Narva's revenue more than doubled, to €468,000.
  - Väike-Maarja was the only municipality where revenue was forecast to fall (€400,988 to €350,000), after its council rejected a rise. Its mayor warned of cuts to schools and roads.
- 2026, from EMTA. Source for all points: [EMTA](https://www.emta.ee/eraklient/maksud-ja-tasumine/muud-maksud-ja-nouded/maamaks). [P]
  - Rate ranges: 0.1–1% for residential land and farm yard land, 0.1–0.5% for agricultural land, 0.1–2% for other land.
  - Each municipality chose its own cap on increases, "vahemikus 10 kuni 100 protsenti" (between 10 and 100%), with a €5 minimum step.
  - The homeowner relief became amount-based, "vahemikus 0–1000 eurot", decided locally. If a municipality set no amount, no relief applies.
  - Pensioners' extra relief also became amount-based.
- Tallinn applies the full €1,000 automatically to owners registered at the address on 1 January, and caps increases at 10%. Source: [Tallinn City](https://www.tallinn.ee/en/maamaks). [P]

**The 2026 valuation and political framing**
- Minister of Economic Affairs Erkki Keldo said the values now being assessed apply to land tax "alles 2028. aastal" (only from 2028), and that "Maamaks on puhtalt kohaliku omavalitsuse otsustada" (land tax is purely for local government to decide). Source for all points: [ERR, 2026; exact date not shown on the page, before the end of October 2026](https://www.err.ee/1610109331/keldo-maahindamine-ei-tahenda-automaatselt-maamaksu-tousu). [S]
  - The newspaper Postimees reported likely rises in taxable value of about 25–40% in many areas. The Land and Spatial Board (*Maa- ja Ruumiamet*) said results were unfinished and expected by the end of October.
  - The €1,000 relief ceiling dates from "the 2024 reform".
  - Saue parish grants €1,000 to all registered residents.
  - Some municipalities in south-east Estonia and Ida-Viru County raised land tax without introducing relief.

**Revenue**
- Eurostat (D.29A, "taxes on land, buildings and other structures", which in Estonia is essentially the land tax): €10.1 million (1995), €23.9 million (2000), €32.3 million (2005), €48.3 million (2008), €51.3 million (2010), €58.6 million (2012), €57.2 million (2013), €59.2 million (2023), €58.5 million (2024), €80.5 million (2025). As a share of GDP: 0.4% (1995, 2000), 0.2% (2017–2023), 0.1% (2024), 0.2% (2025). As a share of total taxes: 1.0% (2012), 0.5% (2023), 0.4% (2024), 0.5% (2025). Source: [Eurostat gov_10a_taxag](https://ec.europa.eu/eurostat/databrowser/view/gov_10a_taxag/default/table?lang=en). [P]

### Inferences
- Estonia is a clean "land only" case. Its trajectory shows the typical political economy of a stale base.
  1. As values aged, revenue stalled in nominal terms, at €57–59 million a year from 2012 to 2024 despite rising land prices, while relative burdens drifted apart.
  2. Revaluation (2022) needed offsetting rate cuts plus a cap.
  3. The cap was then adjusted twice in two years (10% in 2024, 50% or €20 in 2025, 10–100% locally from 2026).
- The 2013 exemption shows no visible revenue drop in the Eurostat series (€58.6 million in 2012 against €57.2 million in 2013). How it was financed or offset is a gap.
- Separating valuation (state, every four years) from taxation (municipal rates, caps and reliefs) was an explicit design goal after 2016. Maa-amet's line was that valuation is economic analysis while taxation is a political decision.

### Gaps
- The Land Tax Act's adoption date and original gazette reference, and the 2012 amending act behind the 2013 exemption: Riigi Teataja pages would not render. The 1 July 1993 date and the 2013 start rest on the thesis [S], with EMTA confirming the exemption's terms [P].
- The date the Riigikogu passed the 2024 amendments (2025 cap and ceilings; 2026 municipal caps and €1,000 relief). Only an explanatory memorandum dated 10 April 2024 was seen, as a search hit on a third-party mirror, and it was not opened.
- The date of the Riigikogu act making valuation four-yearly: the press release URL returned 404.
- Official national revenue figures from the Ministry of Finance or EMTA: Eurostat used instead.
- The causes of the 2008 jump (€35.3 million to €48.3 million) were not investigated.

---

## 6. Sweden: *fastighetstaxering*, the 2008 switch to a capped municipal fee, and earlier freezes and caps (short notes)

### Takeaway
Sweden values every property's land (*markvärde*) and buildings (*byggnadsvärde*) separately, at 75% of market value. The general assessment for each property type comes every six years, with a simplified one in between. In 2008 the state property tax on homes was replaced by a municipal fee, indexed and capped (SEK 6,000 or 0.75% of value for a house in 2008). The government said the old tax was unfair, unpredictable and blind to ability to pay. Before that, assessed values had been frozen in some years, and household bills capped by income.

### Cited Findings
**Valuation**
- "Taxeringsvärde skall bestämmas till det belopp som motsvarar 75 procent av taxeringsenhetens marknadsvärde." (Assessed value is set at 75% of the unit's market value.) Market value is the price level of the second year before the assessment (*nivååret*, the reference year). It is found first by the sales-comparison method (*ortsprismetoden*), then by yield, then by depreciated replacement cost. Source: [Fastighetstaxeringslag (1979:1152), ch. 5 §§ 2–6](https://www.riksdagen.se/sv/dokument-och-lagar/dokument/svensk-forfattningssamling/fastighetstaxeringslag-19791152_sfs-1979-1152/). [P]
- Component values, ch. 5 § 7, source as above [P]:
  - for houses, owner-occupied flats, rental blocks and industrial units: *byggnadsvärde* (buildings) and *markvärde* (land: plot land, extraction land, waterfall rights and land works);
  - for farm units, separate values for dwelling, farm buildings, plot land, arable land and forest.
- Cycle, ch. 1 §§ 7–7a [P]:

  | Property type | General assessment (*allmän*), every 6th year from | Simplified assessment (*förenklad*), every 6th year from |
  |---|---|---|
  | Houses (*småhus*) | 2003 | 2006 |
  | Farm units | 2005 | 2008 |
  | Rental, industrial, power and special units | 2007 | 2004 (rental units) |
  | Owner-occupied flats (*ägarlägenheter*) | 2013 | 2010 |

  So houses are assessed generally in 2003, 2009, 2015, 2021, 2027, and in simplified form in 2006, 2012, 2018, 2024. This is my reading of the statute.
- Skatteverket, with the national land survey authority, drafts guide-value maps (*riktvärdekartor*) for plot land and guide-value tables for houses before each general assessment. Source: [FTL ch. 19 § 5](https://www.riksdagen.se/sv/dokument-och-lagar/dokument/svensk-forfattningssamling/fastighetstaxeringslag-19791152_sfs-1979-1152/). [P]

**Earlier freezes and caps**
- A limitation rule in Lag (2001:906) limited property tax on a house assessed at SEK 280,000–3 million to 4% of household income; households with incomes above SEK 750,000 were excluded. Source: [2007/08:SkU10](https://www.riksdagen.se/sv/dokument-och-lagar/dokument/betankande/reformerad-beskattning-av-bostader_gv01sku10/html/). [P]
- Lag (2006:1340) froze the property tax base for houses and the housing part of rental blocks at 2006 levels for the 2008 and 2009 taxations. It also capped tax on land value at SEK 2 per m² or SEK 5,000, "i avvaktan på att denna skatt kan avskaffas" (pending abolition). Source: [2007/08:SkU10](https://www.riksdagen.se/sv/dokument-och-lagar/dokument/betankande/reformerad-beskattning-av-bostader_gv01sku10/html/). [P]
- The committee noted that since the early-1990s tax reform rates had been cut several times and that "taxeringsvärdena varit frysta under vissa år" (assessed values were frozen in certain years). It also listed a smoothing rule (*dämpningsregel*). Source: [2007/08:SkU10](https://www.riksdagen.se/sv/dokument-och-lagar/dokument/betankande/reformerad-beskattning-av-bostader_gv01sku10/html/). [P]

**The 2008 reform**
- Bill prop. 2007/08:27, *Avskaffad statlig fastighetsskatt, m.m.*, was published on 29 October 2007 and approved by the Riksdag on 17 December 2007. It took effect on 1 January 2008. Capital gains tax on private homes rose from 20% to 22% of the gain. Source: [Regeringen.se](https://www.regeringen.se/rattsliga-dokument/proposition/2007/10/prop.-20070827). [P]
- The fee in 2008 was SEK 6,000 per house, at most 0.75% of building plus land value. From 2009 it is indexed to the change in the income base amount (*inkomstbasbelopp*). Rental flats now pay SEK 1,027 per flat, at most 0.3% of value; the 2008 bill set SEK 1,200 and 0.4%. New homes are exempt for 15 years. Sources: [Lag (2007:1398) §§ 3, 6](https://www.riksdagen.se/sv/dokument-och-lagar/dokument/svensk-forfattningssamling/lag-20071398-om-kommunal-fastighetsavgift_sfs-2007-1398/); [Regeringen.se](https://www.regeringen.se/rattsliga-dokument/proposition/2007/10/prop.-20070827). [P]
- Unbuilt plot land and leasehold plots stayed under state property tax at 1% of assessed value. Source: [2007/08:SkU10, reservation](https://www.riksdagen.se/sv/dokument-och-lagar/dokument/betankande/reformerad-beskattning-av-bostader_gv01sku10/html/). [P]
- Reasons given by the Riksdag committee majority (report signed 6 December 2007): "Den statliga fastighetsskatten på bostäder är orättvis och saknar folkligt stöd och legitimitet" (the state property tax on homes is unfair and lacks public support and legitimacy). The committee also said that:
  - its link to market value made it rise unpredictably;
  - it did not sufficiently respect ability to pay;
  - it caused liquidity problems because it was charged on non-monetary income.

  The committee accepted that the fee "i statsrättslig mening är en skatt" (is a tax in constitutional terms), as the Council on Legislation (*Lagrådet*) had said, but kept the name to mark the break with the criticised state tax. Source: [2007/08:SkU10](https://www.riksdagen.se/sv/dokument-och-lagar/dokument/betankande/reformerad-beskattning-av-bostader_gv01sku10/html/). [P]
- The Social Democrat, Left and Green opposition argued that the reform favoured the highest-valued homes: "Slott och koja ska inte beskattas lika" (castle and cottage should not be taxed alike). Under the cap the fee would be 0.75% of value for houses up to SEK 800,000, but 0.20% at SEK 3 million and 0.10% at SEK 6 million. Source: [2007/08:SkU10, motions and reservation](https://www.riksdagen.se/sv/dokument-och-lagar/dokument/betankande/reformerad-beskattning-av-bostader_gv01sku10/html/). [P]
- Eurostat D.29A for Sweden (taxes on land and buildings, all sectors): SEK 25.9 billion (2007), 23.6 billion (2008), 41.6 billion (2024; 0.6% of GDP, 1.5% of taxes), 45.6 billion (2025; 0.7% of GDP, 1.7% of taxes). Source: [Eurostat gov_10a_taxag](https://ec.europa.eu/eurostat/databrowser/view/gov_10a_taxag/default/table?lang=en). [P]

### Inferences
- Sweden kept a full, separate land-and-building valuation, renewed every three years, while cutting the link between that valuation and most household bills. Value matters only below the cap, which fits about the cheapest homes: 0.75% of SEK 800,000 is SEK 6,000. This is the opposite of Denmark's choice, which kept value-based taxation and capped the increases.

### Gaps
- The current (2025–2026) fee amounts were not found, because Skatteverket pages could not be searched.
- The specific years of the pre-2008 freezes, and the state property tax rates in 1991–2007 (houses and flats), were not found.
- The government's own reasoning in prop. 2007/08:27 was not read; the committee report and the bill page were used instead.

---

## 7. Finland: municipal property tax, separate land and building values, and the valuation reform (short notes)

### Takeaway
Finland's municipal property tax (since 1993) values land and buildings separately:
- **land:** at area prices from municipal plot-price maps, discounted to 75%;
- **buildings:** at nationally uniform replacement cost less age deductions.

The values have lagged. The building method dates from the 1970s, and broad land-value updates are more than 15 years old. A valuation reform has been prepared under five prime ministers since about 2016. It was postponed in 2018 and 2022, and under the Orpo government a bill was "intended" for late spring 2026. Its status on 4 November 2026 is **unconfirmed**. Land supplies about 28% of 2026 property tax revenue.

### Cited Findings
- Under the Property Tax Act (KiVL 654/1992) § 15, property value is computed under the Valuation Act (*arvostamislaki* 1142/2005) ch. 5 for the year before the tax year. "Kiinteistön verotusarvo on määrättävä erikseen maapohjan ja rakennuksen osalta." (Taxable value must be set separately for land and building.) Source: [Verohallinto, *Kiinteistöjen arvostaminen kiinteistöverotuksessa*, issued 23 April 2026](https://www.vero.fi/syventavat-vero-ohjeet/ohje-hakusivu/48219/kiinteistojen-arvostaminen-kiinteistoverotuksessa7/). [P]
- **Land:** each year Verohallinto sets building-land values from municipality-specific plot-price maps (*tonttihintakartat*) giving an area price (*aluehinta*) per floor-m² of building rights or per m² of plot. The maps reflect location, transport, utilities and the price level in free sales. Verohallinto may limit increases. In 2025 the taxable value was 75% of the area price, with a minimum area price of €1/m², giving at least €0.75/m². Source: [Verohallinto guidance, ch. 1–2](https://www.vero.fi/syventavat-vero-ohjeet/ohje-hakusivu/48219/kiinteistojen-arvostaminen-kiinteistoverotuksessa7/). [P]
- **Buildings:** replacement cost (*jälleenhankinta-arvo*) less annual age deductions by building type, under an annual Ministry of Finance decree (e.g. 1073/2025). The same cost basis applies nationwide; "rakennuksen sijainti ei vaikuta sen verotusarvoon" (location does not affect a building's value). Source: [Verohallinto guidance](https://www.vero.fi/syventavat-vero-ohjeet/ohje-hakusivu/48219/kiinteistojen-arvostaminen-kiinteistoverotuksessa7/). [P]
- **Court rulings:**
  - KHO 2025:60 (Supreme Administrative Court): land should in principle be valued by its actual use when building rights are under-used.
  - KHO 2025:58 (18 August 2025): a precedent on land and building tax values, decided by vote.

  Sources: [Verohallinto guidance](https://www.vero.fi/syventavat-vero-ohjeet/ohje-hakusivu/48219/kiinteistojen-arvostaminen-kiinteistoverotuksessa7/); [Eduskunta information package](https://www.eduskunta.fi/fi/lakihankkeiden-tietopaketit/kiinteistoverotuksen-arvostamisperusteet). [P]
- **2026 figures** (forecast, published 30 March 2026). Source: [Verohallinto, *Ennakkotietoa kiinteistöverotuksesta 2026*](https://www.vero.fi/tietoa-verohallinnosta/tilastot/kiinteistoverotilastoj/ennakkotietoa-kiinteistoverotuksesta-2026/). [P]
  - Total property tax: €2,443 million (+1.0%).
  - Buildings: €1,766 million (72.3%); land: about €677 million (27.7%).
  - Assessed values: €276 billion in total, of which buildings €226 billion (81.9%) and land €50 billion (18.1%); land values rose 1.1%.
  - Statutory ranges: general building rate 0.93–2.00%, general land rate 1.30–2.00%, permanent-residence rate 0.41–1.00%.
  - The 2024 revenue increase came largely from raising the lower limit of the land rate.
- Eurostat D.29A for Finland: €2,258 million (2024) and €2,302 million (2025), 0.8% of GDP and 1.9% of total taxes. Source: [Eurostat](https://ec.europa.eu/eurostat/databrowser/view/gov_10a_taxag/default/table?lang=en). [P]
- **Status of the reform.** Source: [Eduskunta (Parliament) information package, *Kiinteistöverotuksen arvostamisperusteet*](https://www.eduskunta.fi/fi/lakihankkeiden-tietopaketit/kiinteistoverotuksen-arvostamisperusteet). [P]
  - "Nykyinen rakennusten arvostamisjärjestelmä on 1970-luvulta ja maapohjan arvojen laajemmat päivitykset ovat yli 15 vuoden takaa. Selvitysten mukaan verotusarvot ovat jääneet yleisesti jälkeen kustannus- ja hintakehityksestä." (The building valuation system dates from the 1970s and broad land-value updates are over 15 years old; taxable values have generally fallen behind cost and price developments.)
  - Under the Orpo government programme, "Hallituksen esitys asiasta on tarkoitus antaa eduskunnalle loppukeväällä 2026. Uudistus toteutetaan pitkillä siirtymäajoilla." (The government bill is intended for submission in late spring 2026; the reform will have long transition periods.) The project is VM095:00/2023, from 15 August 2023.
- **Reform history**, from documents listed in the same information package. These are titles only; I did not open the documents. [P titles]
  - Development projects for new price zones (VM142:00/2016) and building valuation (VM152:00/2017).
  - Ministry press release of 26 October 2018: *Kiinteistöverouudistus lykkääntyy – verotusarvoista ja veroprosenteista päätetään samanaikaisesti* (property tax reform postponed; values and rates to be decided together).
  - Draft government bill of 25 March 2022.
  - Ministry press release of 2 September 2022: *…arvostamisuudistus siirtyy* (the valuation reform is postponed).
  - Eduskunta press release of 8 November 2023: Parliament approved an amendment to the Property Tax Act.
  - Government spending-framework session of 22–23 April 2025: minuted entries on the reform.
  - Press headlines: Yle (19 December 2021) called it an "Ikuisuusprojekti … valmisteltu viiden pääministerin kausilla" (eternal project, prepared under five prime ministers); Helsingin Sanomat (31 January 2024) reported a warning by the employers' confederation EK that individual plots' taxable values could rise "jopa 100-kertaisesti" (up to 100-fold).

### Inferences
- Finland gives a third model alongside Denmark and Sweden: valuation by administrative formula (area-price maps and replacement cost), with built-in discounts and no market revaluation. It is stable and cheap to run, but drifts from market values. Reform has been blocked repeatedly by fears of redistribution, hence the 2018 rule to decide values and rates together.

### Gaps
- Whether the government bill was submitted in spring 2026, and the planned first tax year of new values: not confirmed. The Ministry of Finance pages (vm.fi) returned HTTP 403.
- What the 8 November 2023 amendment contained. My reading is that it separated the land rate and raised its floor from 2024, based on Verohallinto's 2024 remark, but this is **[U]**.
- The scope of the farm and forest land exemption: not confirmed from the statute text, because Finlex would not render.

---

## 8. Norway: the optional municipal property tax (*eiendomsskatt*) (brief)

### Takeaway
Norwegian municipalities choose whether to levy property tax, and on which categories. In 2026, 329 of 357 do, and 249 of them tax homes. Homes are valued either by municipal assessment at estimated sale value, renewed every 10 years, or by reusing the tax authority's wealth-tax housing values. Either way, homes are taxed on 70% of value at 1–4‰. Revenue is about NOK 17.5 billion, 0.3% of GDP.

### Cited Findings
- "Kommunestyret avgjer om det skal skrivast ut eigedomsskatt i kommunen." (The municipal council decides whether to levy property tax.) Councils choose among seven area and category options (§ 3), including all property, only built-up areas, or only power plants and industry. Sources: [Eigedomsskattelova (Act of 6 June 1975 no. 29) §§ 2–3](https://lovdata.no/dokument/NL/lov/1975-06-06-29); [SSB](https://www.ssb.no/offentlig-sektor/kommunale-finanser/artikler/kommuner-med-eiendomsskatt). [P]
- **Valuation:**
  - value is the likely sale price on the open market, and the tax base for homes and holiday homes is "verdet multiplisert med 0,7" (value multiplied by 0.7) (§ 8 A-2);
  - valuation is by assessment (*takst*), with a general assessment every ten years (§ 8 A-3);
  - instead of reassessing, the council may raise old values by office adjustment (*kontorjustering*), with increases capped at 10% a year (§ 8 A-4);
  - for homes, the council may instead use the wealth-tax value (*formuesgrunnlag*) computed by the tax authority (Skatteetaten), also multiplied by 0.7 (§ 8 C-1).

  Source: [Lovdata](https://lovdata.no/dokument/NL/lov/1975-06-06-29). [P] SSB adds that the base for a given year comes from the tax return of two years earlier. Source: [SSB](https://www.ssb.no/offentlig-sektor/kommunale-finanser/artikler/kommuner-med-eiendomsskatt). [P]
- **Rates:** 1–7‰, but "for bustader og fritidsbustader … ikkje … meir enn [4 promille]" (at most 4‰ for homes and holiday homes). A per-dwelling basic deduction (*bunnfradrag*) is optional (§ 11). The first-year rate may not exceed 1‰, and rates may rise by at most 1‰ a year (§ 13). Source: [Lovdata](https://lovdata.no/dokument/NL/lov/1975-06-06-29). [P]
- **Uptake and revenue:**
  - 2026: 329 of 357 municipalities levy, 249 on homes and 315 on business property and power plants.
  - The number fell from 371 to 319 in 2020, because of municipal mergers.
  - Revenue was NOK 17.5 billion in 2024, after nearly 10% growth in 2022–23 and a slight fall in 2024.

  Source: [SSB, 15 June 2026](https://www.ssb.no/offentlig-sektor/kommunale-finanser/artikler/kommuner-med-eiendomsskatt). [P] Eurostat D.29A: NOK 17,536 million (2024) and 17,956 million (2025), 0.3% of GDP and 0.8% of total taxes. Source: [Eurostat](https://ec.europa.eu/eurostat/databrowser/view/gov_10a_taxag/default/table?lang=en). [P]

### Inferences
- Norway taxes whole properties (land plus buildings), not land separately. Its relevance to a land-tax chronology is as a contrast case: a local, optional tax with a hard rate ceiling and a mandatory 30% discount on homes.

### Gaps
- When the home rate ceiling was cut to 4‰ and the 0.7 factor introduced: the statute shows only the current text.
- The split of revenue between homes and business property was not extracted (SSB table 12364).

---

## 9. Concepts a newcomer needs (plain language)

- ***Hartkorn* (Denmark, 1662–1903):** a notional measure of how much grain a farm's land could yield. A farm was "rated" at so many *tønder hartkorn*, and taxes were charged per tønde. It measured productive capacity, not price.
- ***Bonitering* (soil grading):** classing land by quality. In 1688 the classes were good, middling and poor; in 1844, a scale with 24 as the best. The grade converted area into hartkorn.
- ***Matrikel* (cadastre):** the official register of land parcels. It was originally made for taxation; today it underpins property rights.
- **General valuation (*almindelig vurdering*):** a periodic revaluation of every property by a public body. In Denmark this was valuation councils from 1904, SKAT from 2003, and Vurderingsstyrelsen from 2018.
- **Property value (*ejendomsværdi*) versus land value (*grundværdi*):** property value is the price of land plus buildings. Land value is what the plot would fetch if it were empty ("i ubebygget stand"), assuming its best economic use. The difference (*forskelsværdi*) is, roughly, the buildings.
- **Land value tax (*grundskyld*):** an annual tax on land value only. Because land supply is fixed, economists argue that it does not discourage building or work, though this is contested in practice. Expected future tax is "capitalised", meaning it is subtracted from what buyers will pay.
- **Full grundskyld:** the Georgist goal of taxing away the whole annual rent of land, typically put at 4% of land value in Danish proposals.
- **Land value increment tax (*grundstigningsskyld*):** a tax only on the rise in land value since a base date. It is hard to separate from general inflation.
- **Betterment or release levy (*frigørelsesafgift*):** a one-off charge when a planning decision (rezoning farmland to urban use) suddenly raises land value.
- **Coverage tax (*dækningsafgift*):** a Danish municipal tax on public and business property, levied where ordinary property taxes do not apply.
- **Property value tax (*ejendomsværdiskat*):** Denmark's annual tax on the value of an owner-occupied home since 2000. It replaced taxing the home's imputed rent as income.
- **Tax freeze (*skattestop*) and land-tax base ceiling (*grundskatteloft*):** political brakes that let bills lag behind valuations. Most Danish owners paid on 2001/02 values for over 20 years.
- **Precautionary deduction (*forsigtighedsprincip*):** in Denmark since 2018/2024, tax is charged on 80% of the valuation to allow for the ±20% uncertainty of any valuation.
- **Deferral (*indefrysning*):** a tax increase is postponed, as a loan, until the home is sold.
- **Rebate (*skatterabat*):** a fixed discount guaranteeing that pre-2024 owners did not pay more after the reform.
- **Mass valuation or automated valuation model:** a statistical model that values thousands of properties from sales and registry data, instead of individual inspection. Used in Denmark (new system), Estonia (2022) and Sweden (guide-value maps).
- **Preliminary valuation and indexation (*prisfremskrivning*):** when fresh valuations are late, an older value is moved forward with a price index. Denmark's 2024–2027 valuations were made this way.
- **Taxable value (*maksustamishind*) and home land (*kodualune maa*) (Estonia):** the land value set by mass valuation, and the land under the owner's own registered home, which was exempt by area (2013–2025) and is now subject to municipal relief of up to €1,000.
- **Cap on annual increase (*maamaksu tõusu piirmäär*) (Estonia):** each bill may rise by at most a set percentage a year: 10% in 2024; 50% or €20 in 2025; 10–100% set locally from 2026.
- **Assessed value (*taxeringsvärde*), land value (*markvärde*) and building value (*byggnadsvärde*) (Sweden):** assessed value is 75% of market value, split into its land and building parts.
- **Area price (*aluehinta*) and replacement cost (*jälleenhankinta-arvo*) (Finland):** price-map values for land, and rebuilding cost less age deductions for buildings.
- ***Takst*, *kontorjustering* and *bunnfradrag* (Norway):** municipal assessment of property; indexing old assessments; and a tax-free slice of value per home.

---

## 10. Scenes and anecdotes (each sourced)

1. **Farmers forbidden to judge their own parish (1680s).** Christian V's soil grading was done by selected farmers who "ikke måtte taksere jorder i egne sogne" (could not value land in their own parishes), an early anti-capture rule. Source: [Lex: jordbonitering](https://lex.dk/jordbonitering). [S]
2. **Denmark's best field (early 1800s).** The 1844 grading needed a national benchmark. "Danmarks bedste jord" (Denmark's best soil), graded 24, was found on freeholder Niels Nielausen's plot in Karlslunde, Roskilde county. It was described as a mix of sand, clay and humus "i en Dybde af over 18 Tommer … imod Sønden med et godt Fald" (to a depth of over 18 inches … sloping well to the south). Every other field in Denmark was rated against it. Source: [Lex: jordbonitering](https://lex.dk/jordbonitering). [S]
3. **One register page, two eras.** Register no. 1818 (Riberhus county, 1688) lists each tenant's hartkorn under both the "Gammel Matrikel" of 1664 and the "Nye Matrikel" of 1688, recorded in tønder, skæpper, fjerdingkar and album. Source: [Lex: matrikel](https://lex.dk/matrikel_-_register_og_kortv%C3%A6rk_over_ejendomme). [S]
4. **The first look at land alone (1916).** Valued separately for the first time, land made up 46.5% of all Danish property value: 55.4% in the countryside but only 31.5% in provincial towns. Source: [DST 1919](https://rss.dst.dk/pubfile/20981/skyld1916). [P]
5. **"The whole land rent should accrue to the society that creates it" (1954/1957).** In January 1957, months before entering government, three Georgist MPs put the Land Tax Commission's words before parliament. They proposed buying out landowners with 4% state bonds and using the land rent to cut customs and consumption duties. Source: [Folketingstidende 1956–57, L 105](https://folketingstidende.dk/samling/19561/lovforslag/L105/19561_L105_som_fremsat.pdf). [P]
6. **Seventeen out of ninety-eight (2013).** Rigsrevisionen found land-value zones drawn correctly in only 17 of 98 municipalities. Of the houses sold in late 2011, 41% had been valued above their sale price. Source: [Rigsrevisionen 2013](https://www.rigsrevisionen.dk/Media/4/C/den-offentlige-ejendomsvurdering.pdf). [P]
7. **128 empty plots (2014).** To value land "as if unbuilt", Copenhagen had just 128 vacant-plot sales in five years. Nationally, only about 1,300–1,400 house plots changed hands freely each year. Source: [Engberg report pp. 166–167](https://www.skm.dk/media/Skatteministeriet/Dokumenter/PDF%27er/forbedring-af-ejendomsvurderingen_web.pdf). [P]
8. **95% paying on 2001 values (2014).** Under the 2002 tax freeze, 95% of Danish homeowners paid property value tax on their 2001 or 2002 valuation. Source: [Engberg report §4.3](https://www.skm.dk/media/Skatteministeriet/Dokumenter/PDF%27er/forbedring-af-ejendomsvurderingen_web.pdf). [P]
9. **"The least troublesome solution" (2026).** Unable to deliver 2026 valuations in time, the minister chose to index the 2022 values forward: "den mindst bøvlede løsning for boligejerne i den aktuelle situation". Source: [Skatte- og Vækstministeriet, 14 June 2026](https://www.skm.dk/aktuelt/presse-nyheder/pressemeddelelser/ro-om-boligskatten-ejendomsvurderinger-for-2026-og-2027-bliver-prisfremskrevet). [P]
10. **3 times here, 30 times there (Estonia, 2022).** After 21 years without revaluation, some Estonian parcels had risen 3-fold and others 30-fold, and the country's land rose from €4 billion to €30 billion in value. Under the 10% cap, a €30 bill bound for €70 would take 11 years to get there. Sources: [Maa-amet](https://maaruum.ee/sites/default/files/documents/2024-12/Maa%20korraline%20hindamine%20voldik%202022.pdf); [Ministry of Finance 2023](https://agri.ee/sites/default/files/documents/2023-09/KOVidele%20uute%20maamaksum%C3%A4%C3%A4rade%20kehtestamise%20juhend%202023.pdf). [P]
11. **The one parish that said no (Estonia, 2025).** Väike-Maarja was the only Estonian municipality where land tax revenue was forecast to fall in 2025: its council rejected a rise, and the mayor warned of cuts to schools and roads. Source: [ERR, January 2025](https://www.err.ee/1609585508/maamaksu-laekumine-ei-kasva-tanavu-vaid-uhes-vallas). [S]
12. **"Castle and cottage" (Sweden, 2007).** As the state property tax was abolished, the opposition protested: "Slott och koja ska inte beskattas lika" (castle and cottage should not be taxed alike). They pointed out that a SEK 6 million villa would pay 0.10% of value and a modest house 0.75%. Source: [2007/08:SkU10](https://www.riksdagen.se/sv/dokument-och-lagar/dokument/betankande/reformerad-beskattning-av-bostader_gv01sku10/html/). [P]
13. **Five prime ministers (Finland).** A 2021 Yle headline listed by the Eduskunta called Finland's valuation reform an "eternal project" prepared under five prime ministers. Source: [Eduskunta information package](https://www.eduskunta.fi/fi/lakihankkeiden-tietopaketit/kiinteistoverotuksen-arvostamisperusteet). [P for the listing]

---

## 11. Access log

- **Web search budget:** the shared WebSearch quota was exhausted after about 13 searches. All later work used direct fetches of known official URLs: Statistics Denmark and Eurostat APIs, riksdagen.se, folketingstidende.dk, tax.dk (Den juridiske vejledning), lex.dk, and agency pages. Unrun follow-up searches:
  - the Danish 2013 suspension law;
  - Vurderingsstyrelsen's founding date;
  - Retsforbundet's 1957–60 legislative record;
  - the Estonian 2012 and 2024 amending acts;
  - Swedish 2025–26 fee amounts;
  - the status of the Finnish 2026 government bill;
  - Norwegian 2020–21 rate changes.
- **Riigi Teataja (Estonian gazette):** the English and Estonian consolidated texts of the Land Tax Act (e.g. /en/eli/505012026005/consolide) returned only a JavaScript shell. The statute text could not be read; EMTA and Ministry of Finance documents were used instead.
- **riigikogu.ee:** the press release "The Riigikogu passed an Act on the mass valuation of land" returned HTTP 404.
- **IMF eLibrary:** "Options to Strengthen the Tax System in Estonia" (2025, Selected Issues) returned HTTP 403. Not used.
- **vm.fi and valtioneuvosto.fi (Finnish Ministry of Finance and project register):** HTTP 403 for the 2018 and 2022 press releases and project VM095:00/2023. Only titles, as listed by the Eduskunta, were used.
- **Finlex:** the Property Tax Act (654/1992) page did not render (JavaScript). Not read.
- **eduskunta.fi:** the page is JavaScript-rendered; content was extracted from the JSON embedded in the HTML.
- **retsinformation.dk:** JavaScript-only. Law no. 615/2026 was confirmed through Den juridiske vejledning instead.
- **eu.dk:** the minister's introductory speech for L 76 (2014–15) returned HTTP 403.
- **vurderingsportalen.dk:** HTTP 403 (no delivery-status data).
- **core.ac.uk:** two Danish history articles on the 1688 matrikel returned HTTP 403 or HTML. The hartkorn-ownership shares seen in a search snippet stay unverified.
- **lovdata.no:** curl returned HTTP 405, but WebFetch succeeded.
- **Lex:** the article "Trekantregeringen" was seen only as a search excerpt (May 1957 to February 1960) and was not opened.
- **Secondary sources I relied on, and why:**
  - Lex (Den Store Danske), for the hartkorn and early-modern history, because no Rigsarkivet source was reachable.
  - Sultanjants (2020) TalTech master's thesis, for the 1993 Estonian design, rate history and the 2013 exemption date, because Riigi Teataja did not render. It cites Malme and Tiits (World Bank 2001) and Wenner (*Land Use Policy* 77), which I did not open.
  - Faglig Senior and Nykredit, for 2026 Danish delivery status and estimated tax effects, because vurderingsportalen.dk returned 403.
  - ERR, for Estonian municipal reactions.

  These are labelled [S].
- **Leads seen only in search snippets and not used as facts:** an Engberg-related parliamentary question claiming that 76% of houses valued under DKK 0.5 million were overvalued by more than 20%; the founding of the implementation centre ICE on 1 October 2014; a 2020 agreement postponing the reform from 2021 to 2024; EY's summary of Estonia's 2025–2026 changes (superseded by EMTA). All **[U]**.
