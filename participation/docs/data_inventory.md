# Data inventory — coverage only (blind scouting, 2026-10-08)

Five scouting agents verified these codes against the live APIs and reported coverage only (no values).

## eurostat_lfs

- **lfsa_argan** (Eurostat EU-LFS (annual)) — Labour force participation rates by citizenship (sex x age x citizenship). Verified.
  - breakdowns: sex T/M/F; age 38 codes incl. full 5-yr ladder Y15-19,Y20-24,Y25-29,Y30-34,Y35-39,Y40-44,Y45-49,Y50-54,Y55-59,Y60-64,Y65-69,Y70-74,Y_GE75 plus aggregates Y15-24,Y15-29,Y20-29,Y25-54,Y15-64,Y20-64,Y55-64,Y_GE65 etc. (NO Y25-34 code: build from 25-29+30-34 via lfsa_pganws counts); citizen TOTAL/NAT/FOR/EU27_2020_FOR/NEU27_2020_FOR/STLS/NRP; unit PC
  - countries: 36 countries (EU27 + IS,NO,CH,UK + BA,ME,MK,RS,TR) plus aggregates EU27_2020, EA21. Starts: 1995 EU15(ex-none)+IS,NO; 1996 CH,HU,SI; 1997 CZ,EE,PL,RO; 1998 LT,LV,SK; 1999 CY; 2000 BG,MT; 2002 HR; 2006 MK,TR; 2010 RS; ME 2011-2020 only; BA from 2021; UK ends 2019
  - years: 1995-2025
  - notes: citizen=TOTAL slice: every 5-yr band 15-19..60-64 has all 36 countries with no internal gaps (985 country-years per sex x age slice); Y65-69 36 ctry (a few gaps), Y70-74 34-36 ctry, Y_GE75 31-35 ctry. Break flags 'b' widespread in 2005 and 2021 (IESS regulation), ES/FR flagged 'bd' 2021 and 'd' 2022+.
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/lfsa_argan?format=JSON&lang=EN&sex=T&sex=M&sex=F&age=Y25-54&unit=PC&citizen=TOTAL`
- **lfsa_argaed** (Eurostat EU-LFS (annual)) — Labour force participation rates by educational attainment level (sex x age x ISCED 2011). Verified.
  - breakdowns: sex T/M/F; age 30 codes incl. 5-yr ladder Y15-19..Y70-74 (no Y_GE codes, no Y15-29/Y20-29), Y25-54, Y15-64, Y20-64, Y55-64; isced11 TOTAL, ED0-2, ED3_4, ED34_44 (general), ED35_45 (vocational), ED5-8, NRP; unit PC
  - countries: 36 countries + EU27_2020, EA21. isced11=TOTAL starts: 1983 BE,DE,DK,EL,FR,IE,IT,LU,NL,UK; 1986 ES,PT; 1995 AT,FI,IS,NO,SE; 1996 CH,HU,SI; 1997 CZ,EE,PL,RO; 1998 LT,LV,SK; 1999 CY; 2000 BG,MT; 2002 HR; 2006 MK,TR; 2010 RS; ME 2011-2020; BA 2021+; UK ends 2019
  - years: 1983-2025 (TOTAL); education levels 1992-2025; general/vocational split 2014+ for Y25-29, 2021+ for Y25-54/Y55-59
  - notes: Use isced11=TOTAL as the long participation series (1121 country-years per prime-age slice vs 985 in lfsa_argan). Internal gaps: NL missing 1984 and 1986 in all slices; F Y15-19: EE 2002-04, LT 9 scattered years 2002-2012, LV 2001/2003, SK 2021-23. Y65-69 thin for LU (4 obs 2011-2022), MT from 2014, ME from 2015, SK from 2005. Break flags: 1998 (27 geos), 2005 (33), 2014 (37), 2021 (34) plus scattered national breaks.
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/lfsa_argaed?format=JSON&lang=EN&sex=F&age=Y25-54&age=Y15-19&age=Y60-64&age=Y65-69&unit=PC&isced11=TOTAL`
- **lfsa_ergan** (Eurostat EU-LFS (annual)) — Employment rates by citizenship (sex x age x citizenship). Verified.
  - breakdowns: sex T/M/F; age 36 codes incl. 5-yr ladder 15-19..70-74, Y_GE75, Y15-24, Y15-29, Y25-54, Y20-64, Y55-64; citizen as lfsa_argan; unit PC
  - countries: 36 countries + EU27_2020, EA21; same per-country start years as lfsa_argan
  - years: 1995-2025
  - notes: All 36 countries for every tested band 15-19..65-69; complete (985) for 15-24..55-59.
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/lfsa_ergan?format=JSON&lang=EN&sex=T&sex=F&age=Y20-24&age=Y25-54&unit=PC&citizen=TOTAL`
- **lfsa_ergaed** (Eurostat EU-LFS (annual)) — Employment rates by educational attainment level. Verified.
  - breakdowns: sex; age 5-yr ladder + aggregates; isced11 TOTAL + levels; unit PC
  - countries: 36 countries + aggregates; isced11=TOTAL same 1983/1986 starts as lfsa_argaed
  - years: 1983-2025 (TOTAL)
  - notes: 1121 country-years per prime-age slice (NL gap 1984/1986).
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/lfsa_ergaed?format=JSON&lang=EN&sex=T&sex=F&age=Y25-54&unit=PC&isced11=TOTAL`
- **lfsa_urgan** (Eurostat EU-LFS (annual)) — Unemployment rates by citizenship (sex x age x citizenship). Verified.
  - breakdowns: sex; age 35 codes incl. 5-yr ladder 15-19..70-74 and Y15-24, Y25-54, Y30-64 etc.; citizen; unit PC
  - countries: 36 countries + aggregates; cell suppression thins older/smaller groups: F Y55-59 33 ctry, F Y60-64 31 ctry, F Y65-69 10 ctry, T Y65-69 27 ctry
  - years: 1995-2025
  - notes: Y15-24 and Y25-54 near complete; 5-yr youth bands have scattered suppressed cells (e.g. F Y15-19 825 of 985 possible).
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/lfsa_urgan?format=JSON&lang=EN&sex=T&sex=F&age=Y15-24&age=Y25-54&unit=PC&citizen=TOTAL`
- **lfsa_urgaed** (Eurostat EU-LFS (annual)) — Unemployment rates by educational attainment level. Verified.
  - breakdowns: sex; age 5-yr ladder + aggregates; isced11; unit PC
  - countries: 36 countries + aggregates; same suppression pattern as lfsa_urgan at older ages
  - years: 1983-2025 (TOTAL)
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/lfsa_urgaed?format=JSON&lang=EN&sex=T&sex=F&age=Y15-24&unit=PC&isced11=TOTAL`
- **lfsa_ipga** (Eurostat EU-LFS (annual)) — Persons outside the labour force - % of total population in private households. Verified.
  - breakdowns: sex T/M/F; age 35 codes incl. 5-yr ladder 15-19..70-74, Y_GE75, Y25-54, Y55-64 etc.; unit PC
  - countries: 36 countries + aggregates; 1983/1986 starts for EU-12 as in lfsa_argaed
  - years: 1983-2025
  - notes: 1119-1120 country-years for every tested slice incl. Y65-69.
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/lfsa_ipga?format=JSON&lang=EN&sex=T&sex=F&age=Y15-19&age=Y60-64&unit=PC`
- **lfsa_igar** (Eurostat EU-LFS (annual)) — Persons outside the labour force not seeking employment by main reason. Verified.
  - breakdowns: sex; age 20 codes (Y15-19, Y15-24, Y15-29, Y25-54, Y25-49, Y55-64, Y55-74, Y50-64, Y15-64, Y20-64 ... NO 20-24, 60-64, 65-69 bands); reason LAYOFF, EDUC_TNG (education/training), ILL_DIS_OWN, B_NJOB (believing no job available = discouraged), FAM_CARE (care of children/adults with disabilities), FAM_CARE_PER_OTH (combined family/care/personal), FAM_PER_OTH, FAM_OTH, PER_OTH, OTH, NRP; unit PC_POP (% of population) and PC_INAC_WWRK (% of inactive wanting to work)
  - countries: 36 countries + aggregates; per-reason coverage varies: Y15-64 B_NJOB 36 ctry, EDUC_TNG 36, FAM_CARE 35, ILL_DIS_OWN 36; Y55-64 EDUC_TNG only 3 ctry; Y15-19 FAM_CARE 4 ctry
  - years: 1992-2025; FAM_CARE only 2006+; FAM_PER_OTH 1992-2020; FAM_OTH and PER_OTH 2021+ (reason scheme changed 2021); FAM_CARE_PER_OTH is the only consistent family/care/personal category 1992-2025
  - notes: NO RETIREMENT reason: the REASON codelist has RET/RETIRED/ERLY_RET codes but lfsa_igar uses none of them in its current version. Many 'u' (low reliability) flags, mostly small countries (DK, IS, LU, MT, NO, CH, CY, LT). Per-country starts for B_NJOB Y15-64 vary (e.g. DE 1996, PL/LT/LV 2001; IS only 3 obs; MT 2008-2012 only).
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/lfsa_igar?format=JSON&lang=EN&sex=T&age=Y15-64&unit=PC_POP&reason=EDUC_TNG&reason=B_NJOB&reason=FAM_CARE`
- **lfsa_igaww** (Eurostat EU-LFS (annual)) — Persons outside the labour force not seeking employment by willingness to work. Verified.
  - breakdowns: sex; age 20 codes (Y15-19, Y15-24, Y25-49, Y55-64, Y55-74 ...); wstatus TOTAL, NSEEK_WANT, NSEEK_NWANT, NRP; unit THS_PER
  - countries: 36 countries + aggregates
  - years: TOTAL 1983-2025; want/not-want split 1992-2025
  - notes: Counts, not rates; divide by lfsa_pganws population.
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/lfsa_igaww?format=JSON&lang=EN&sex=T&age=Y15-24&age=Y55-64&unit=THS_PER`
- **lfsa_pganws** (Eurostat EU-LFS (annual)) — Population in private households by citizenship and labour status (counts). Verified.
  - breakdowns: sex; age 34 codes incl. 5-yr ladder 15-19..70-74, Y_GE75; wstatus POP, ACT, EMP, UNE, INAC, UNK; citizen; unit THS_PER
  - countries: 36 countries + aggregates
  - years: 1995-2025
  - notes: UNE at Y60-64 thinner (35 ctry, gaps).
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/lfsa_pganws?format=JSON&lang=EN&sex=T&age=Y20-24&age=Y60-64&unit=THS_PER&citizen=TOTAL`
- **edat_lfse_20** (Eurostat EU-LFS (education theme)) — Young persons neither in employment nor in education and training by labour status (NEET rates) - THE NEET split table. Verified.
  - breakdowns: sex; age Y15-17, Y15-19, Y15-24, Y15-29, Y15-34, Y18-24, Y18-29, Y20-24, Y20-34, Y25-29, Y25-34, Y30-34; wstatus NEMP (= total NEET), UNE (unemployed NEET), INAC (inactive NEET), WANT (would like to work), NWANT (do not want to work); training NO_FE_NO_NFE; unit PC
  - countries: 36 countries + aggregates. Starts (T, Y20-24): 2000 most; BG,PL,SI 2001; CZ,HR,IE,LV,SK 2002; IS,NO 2003; MK,TR 2006; RS 2010; ME 2011-2020; BA 2021+; UK 2000-2019; LU INAC ends 2024
  - years: 2000-2025
  - notes: Near-complete for T; F Y15-19 UNE 33 ctry with gaps. Flags: 'b' 2003 (21 geos), 2006 (22), 2021 (33); 'u'/'bu' for LU, IS, LT, HR in early years.
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/edat_lfse_20?format=JSON&lang=EN&sex=T&age=Y20-24&wstatus=UNE&wstatus=INAC`
- **edat_lfse_21** (Eurostat EU-LFS (education theme)) — NEET rates by educational attainment level. Verified.
  - breakdowns: sex; same 12 youth ages; isced11 TOTAL, ED0-2, ED3-8, ED3_4, ED34_44, ED35_45, ED5-8, NRP; wstatus NEMP only
  - countries: 36 countries + aggregates
  - years: 2000-2025 (general/vocational split 2014+)
  - notes: No labour-status split here (use edat_lfse_20).
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/edat_lfse_21?format=JSON&lang=EN&sex=T&age=Y20-24&age=Y25-29&age=Y15-19`
- **edat_lfse_18** (Eurostat EU-LFS (education theme)) — Participation rate of young persons in education and training by labour status (incl. NEET rates). Verified.
  - breakdowns: sex; same 12 youth ages (Y15-17..Y30-34 incl. Y15-19, Y20-24, Y25-29); wstatus POP, EMP, NEMP; training FE_NFE (in formal or non-formal education/training, last 4 weeks) / NO_FE_NO_NFE; unit PC
  - countries: 36 countries + aggregates
  - years: 2000-2025
  - notes: POP x FE_NFE complete (855 country-years) for 15-19, 20-24, 25-29.
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/edat_lfse_18?format=JSON&lang=EN&sex=T&sex=F`
- **edat_lfse_19** (Eurostat EU-LFS (education theme)) — Participation rate of young persons in formal education by labour status. Verified.
  - breakdowns: sex; 12 youth ages; wstatus POP/EMP/NEMP; training FE (formal) / NO_FE
  - countries: 36 countries + aggregates
  - years: 2004-2025
  - notes: POP x FE complete (747 country-years) for 15-19, 15-24, 18-24.
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/edat_lfse_19?format=JSON&lang=EN&sex=T`
- **lfsa_pgaied** (Eurostat EU-LFS (annual)) — Population in private households by participation in education and training (last 4 weeks) - counts. Verified.
  - breakdowns: sex; age 18 codes (Y15-19, Y15-24, Y25-49, Y25-64, Y55-64 ...; NO Y20-24 code, derive 20-24 = 15-24 minus 15-19); training TOTAL, FE_NFE, NO_FE_NO_NFE, NRP; unit THS_PER
  - countries: 36 countries + aggregates. FE_NFE Y15-19 starts: 1983 BE,DE,DK,EL,FR,IE,IT,LU,NL,UK; 1986 ES,PT; 1995 AT,IS; 1996 CH,FI,HU,SE,SI; 1997 CZ,PL,RO; 1998 SK; 1999 LT,CY(1999); 2000 MT; 2001 BG; 2002 HR,LV; 2003 NO; 2006 MK,TR; 2010 RS; ME 2011-2020; BA 2021+
  - years: 1983-2025
  - notes: Several gappy countries (DE, IE, UK, CZ fewer obs than span). Pre-2003/2004 reference period for training questions differed in some countries (check metadata).
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/lfsa_pgaied?format=JSON&lang=EN&sex=T&sex=F&age=Y15-19&age=Y15-24&unit=THS_PER`
- **lfsi_neet_a / lfsi_neet_a_h** (Eurostat EU-LFS (main indicators)) — NEET rates - annual data (current, and historical 2006-2020). Verified.
  - breakdowns: sex; age Y15-24, Y15-29 only; unit PC_POP, THS_PER
  - countries: 35 countries each (lfsi_neet_a excludes UK; _h includes UK)
  - years: 2003-2025 (lfsi_neet_a); 2006-2020 (lfsi_neet_a_h)
  - notes: Coarser than edat_lfse_20; no labour status split.
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/lfsi_neet_a?format=JSON&lang=EN&sex=T&sex=F&unit=PC_POP`
- **lfsa_egais** (Eurostat EU-LFS (annual)) — Employed persons by professional status and occupation (ISCO one-digit; ISCO-88 COM to 2010, ISCO-08 from 2011). Verified.
  - breakdowns: sex T/M/F; age 23 codes: Y15-24, Y15-39, Y25-49, Y25-54, Y25-59, Y25-64, Y40-59, Y50-64, Y55-64, Y55-74, Y_GE15, Y_GE25, Y_GE50, Y_GE65, Y_GE75 ... (NO 5-yr youth bands 15-19/20-24/25-29); wstatus EMP, CFAM, NCFAM, NRP; isco08 TOTAL, OC0..OC9, NRP; unit THS_PER
  - countries: 36 countries + aggregates. OC codes start (Y15-24 OC4): 1992 DE,DK,EL,ES,FR,IE,IT,LU,NL,PT,UK; 1993 BE; 1995 AT,IS; 1996 CH,HU,NO,SI; 1997 CZ,FI,PL,RO,SE; 1998 EE,LT,LV,SK; 1999 CY; 2000 BG,MT; 2002 HR; 2006 MK,TR; 2010 RS (missing 2011-12); ME 2012-2020; BA 2021+
  - years: TOTAL 1983-2025; occupation groups 1992-2025
  - notes: Break flag 'b' in 2011 for all 36 countries + aggregates = ISCO-88(COM) -> ISCO-08 switch (LFS ESMS confirms 'ISCO 88 (COM) and ISCO 08 (from 2011)'); the pre-2011 values sit under the ISCO-08 one-digit codes. Further all-country breaks 2005 and 2021. Y25-54 and Y_GE15 occupation cells near complete (1012-1013 country-years for OC1-OC9); Y15-24 thin for OC0/OC1/OC6; Y_GE65 thin (28-33 ctry).
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/lfsa_egais?format=JSON&lang=EN&sex=T&age=Y15-24&wstatus=EMP&unit=THS_PER&isco08=OC4&isco08=TOTAL`
- **lfsa_egai2d** (Eurostat EU-LFS (annual)) — Employed persons by detailed occupation (ISCO-08 two-digit). Verified.
  - breakdowns: isco08 55 codes (all 2-digit sub-major groups, e.g. OC24 business/admin professionals, OC25 ICT professionals, OC41 general/keyboard clerks, OC42 customer services clerks); sex; age ONLY Y15-64, Y15-74, Y_GE15, Y20-64; unit THS_PER
  - countries: 36 countries + aggregates
  - years: 2011-2025
  - notes: Tested 2-digit codes complete (513-517 country-years).
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/lfsa_egai2d?format=JSON&lang=EN&sex=T&age=Y15-64&unit=THS_PER&isco08=OC24&isco08=OC41`
- **lfsa_ugpis** (Eurostat EU-LFS (annual)) — Unemployed persons by previous occupation. Verified.
  - breakdowns: sex; isco08 TOTAL, OC0-OC9, NAP_NEMP_Y8 (no employment in last 8 years), NRP; unit THS_PER; NO age dimension
  - countries: 36 countries + aggregates
  - years: 1992-2025
  - notes: Same 2011 ISCO break as lfsa_egais presumably (not flag-checked).
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/lfsa_ugpis?format=JSON&lang=EN&sex=T&unit=THS_PER&isco08=OC4`
- **lfst_r_lfp2actrt** (Eurostat EU-LFS regional) — Labour force participation rates by NUTS 2 region. Verified.
  - breakdowns: sex T/M/F; age 10-yr bands only: Y15-24, Y25-34, Y35-44, Y45-54, Y55-64, Y_GE65 (+ Y15-64, Y15-74, Y25-64, Y_GE15, Y_GE25); unit PC
  - countries: 35 countries (no BA regions); 350 distinct NUTS2 codes with data (DE 38, UK 45, FR 27, TR 26, IT 21, ES 19, PL 17, NL 14, EL 13, PT 12, BE 11, NO 10 ...). Regions with data per year: 247 (1999) -> 331 (2019) -> 288-290 (2020-2025, after UK's 45 end in 2019). Late starters: BG,MT 2000; CH,SI 2001; MK,TR 2006; DK,HR 2007; ME 2011-2020; RS 2013
  - years: 1999-2025
  - notes: Mixed NUTS vintages in the geo list (e.g. IE01/IE02 alongside IE04-IE06; HU10 alongside HU11/HU12; LT00 alongside LT01/LT02) - needs NUTS harmonisation before panel use. Y_GE65 thinner (124-158 regions/yr in 1999-2004).
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/lfst_r_lfp2actrt?format=JSON&lang=EN&sex=F&age=Y25-34&unit=PC`
- **lfst_r_lfe2emprt** (Eurostat EU-LFS regional) — Employment rates by NUTS 2 region. Verified.
  - breakdowns: sex; age Y15-24, Y25-34, Y35-44, Y45-54, Y55-64, Y_GE65, Y20-64, Y15-64 etc.; unit PC
  - countries: 35 countries; 350 NUTS2 codes; 244 (1999) -> 330 (2019) -> 287-288 regions/yr
  - years: 1999-2025
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/lfst_r_lfe2emprt?format=JSON&lang=EN&sex=F&age=Y25-34&unit=PC`
- **lfst_r_lfu3rt** (Eurostat EU-LFS regional) — Unemployment rates by educational attainment level and NUTS 2 region. Verified.
  - breakdowns: sex; age Y15-24, Y15-29, Y25-34, Y35-44, Y45-54, Y55-64, Y20-64, Y_GE15 ...; isced11 TOTAL/ED0-2/ED3_4/ED5-8; unit PC
  - countries: 347 NUTS2 codes; Y15-24 TOTAL: 193-314 regions/yr (suppression)
  - years: 1999-2025
  - notes: Thinner than activity/employment regional series.
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/lfst_r_lfu3rt?format=JSON&lang=EN&sex=T&age=Y15-24&unit=PC&isced11=TOTAL`
- **lfst_r_lfsd2pwn** (Eurostat EU-LFS regional) — Population in private households by citizenship, labour status and NUTS 2 region (counts). Verified.
  - breakdowns: sex; age ONLY Y15-24, Y15-64, Y15-74, Y_GE15, Y20-64, Y25-54; wstatus POP/ACT/EMP/UNE/INAC; citizen; THS_PER
  - countries: 350 NUTS2 codes; 245 (1999) -> 330 (2019) -> 286-288 regions/yr
  - years: 1999-2025
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/lfst_r_lfsd2pwn?format=JSON&lang=EN&sex=F&age=Y25-54&unit=THS_PER&citizen=TOTAL&wstatus=INAC`
- **edat_lfse_22** (Eurostat EU-LFS regional) — NEET rates by NUTS 2 region. Verified.
  - breakdowns: sex; age Y15-24, Y15-29, Y18-24, Y18-29; wstatus NEMP only (no unemployed/inactive split); unit PC
  - countries: 349 NUTS2 codes; 197 (2000) -> 322 (2014-16) -> 246-261 regions/yr 2020-2025
  - years: 2000-2025
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/edat_lfse_22?format=JSON&lang=EN&sex=T&age=Y15-24`
- **lfsi_emp_a / lfsi_emp_a_h** (Eurostat EU-LFS (main indicators)) — Employment and labour force by sex and age - annual (current 2003+, historical 1992-2020). Verified.
  - breakdowns: indic_em ACT, EMP_LFS; sex; age Y15-24, Y15-29 (current only), Y15-64, Y20-64, Y25-54, Y55-64; unit PC_POP, THS_PER
  - countries: 35 countries each (current excludes UK; historical includes UK 1993-2019). Historical geo list also names US and JP but the tested slice (F, Y25-54, PC_POP) has no US/JP observations
  - years: 2003-2025 / 1992-2020 (data from 1993 in tested slice; FR only from 2003 and CH from 2010 in _h)
  - notes: Prefer lfsa_argaed/lfsa_ergaed for long history.
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/lfsi_emp_a_h?format=JSON&lang=EN&sex=F&age=Y25-54&unit=PC_POP`
- **educ_uoe_enra02** (Eurostat UOE education statistics (administrative, not LFS)) — Pupils and students enrolled by education level, sex and age. Verified.
  - breakdowns: age single years Y15..Y49 plus Y20-24, Y25-29, Y30-34 ... ; sex; isced11 ED0-8 and each level ED0..ED8; unit NR (headcount)
  - countries: 37-39 countries with data (41 geo codes)
  - years: 2013-2024 with data (TOC lists 2012-2024)
  - notes: Predecessor educ_enrl1tl 'Students by ISCED level, age and sex (1998-2012)' exists in TOC (not fetched).
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/educ_uoe_enra02?format=JSON&lang=EN&sex=T&age=Y18&age=Y20-24&isced11=ED0-8&unit=NR`
- **lfsq_argan / lfsq_ergan / lfsq_urgan / lfsq_ipga / lfsq_igaww** (Eurostat EU-LFS (quarterly)) — Quarterly twins of the annual activity, employment, unemployment and inactivity tables. Not verified.
  - breakdowns: assumed same as annual twins (not checked)
  - countries: not checked
  - years: 1998Q1-2026Q2 (TOC)
  - notes: Listed in TOC only; not fetched.

**Not found or not reachable.**
- Separate ISCO-88 LFS occupation tables: none in the dissemination database (searched all 8146 dataflows; the only ISCO-88 flows are the 2001 census tables cens_01naisco and cens_01reisco). The ISCO-88 (COM) one-digit groups for 1992-2010 are carried inside lfsa_egais under the ISCO-08 codes OC0-OC9, with a 'b' break flag in 2011 for all countries.
- yth_empl_150: does not exist (the yth_empl_* series stop at yth_empl_140 and none of them splits NEET by labour status). The NEET split by unemployed vs inactive is in edat_lfse_20 (wstatus UNE/INAC, plus WANT/NWANT).
- Retirement as a reason for inactivity: lfsa_igar uses no retirement code, although the REASON codelist contains RET, RETIRED and ERLY_RET. Pension and retirement information exists only in single-year ad hoc modules (lfso_06* in 2006, lfso_12* in 2012, lfso_23pens* in 2023).
- Five-year youth bands (15-19, 20-24, 25-29) for occupation: lfsa_egais has only Y15-24, Y15-39, Y25-49, Y25-54 and similar bands; lfsa_egai2d (2-digit) has only Y15-64, Y15-74, Y_GE15 and Y20-64; lfsa_ugpis has no age dimension at all.
- lfsa_igar has no 20-24, 60-64 or 65-69 bands; its youngest bands are Y15-19, Y15-24 and Y15-29, and its oldest are Y55-64 and Y55-74.
- lfsa_pgaied has no Y20-24 code (it can be derived as Y15-24 minus Y15-19, since the table holds counts).
- Y25-34 is missing from lfsa_argan, lfsa_ergan and lfsa_urgan (it can be built from 25-29 plus 30-34 using the lfsa_pganws counts). Y25-34 does exist in edat_lfse_* and in the NUTS2 tables.
- Regional (NUTS2) activity and employment rates come only in 10-year bands (15-24, 25-34, ... 55-64, 65+); there is no 15-19, 20-24 or 60-64 split. Regional NEET (edat_lfse_22) has no unemployed vs inactive split.
- No LFS data before 1983. Tables split by citizenship (lfsa_argan, lfsa_ergan, lfsa_urgan, lfsa_pganws) start in 1995; the long history comes from the isced11=TOTAL slices of the *aed tables (1983 for BE, DE, DK, EL, FR, IE, IT, LU, NL, UK; 1986 for ES and PT).
- UK data end in 2019 in every LFS table checked. ME covers 2011-2020 only. BA starts in 2021.
- US/JP in lfsi_emp_a_h: the codes appear in the geo list, but the slice tested (F, Y25-54, PC_POP) returned no observations for them.
- Not fetched: the quarterly lfsq_* twins, educ_enrl1tl (UOE enrolment by age 1998-2012), the SDMX-CSV bulk download route, and break flags for lfsa_ugpis.

**Access.** The proxy worked with truststore.inject_into_ssl() before importing requests, the -I flag and UA 'Mozilla/5.0 (research; laborformal)'. Every call returned HTTP 200 quickly. No rate limiting was seen across about 60 calls.

Endpoints that worked:
(1) Table of contents with codes, titles and first/last year: https://ec.europa.eu/eurostat/api/dissemination/catalogue/toc/txt?lang=en (TSV, about 2 MB). Columns are title, code, type, last update, last structure change, data start, data end, values.
(2) Structure restricted to the codes actually used: https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/dataflow/ESTAT/<CODE_UPPER>/latest?references=descendants&detail=referencepartial. Parse s:Codelist/s:Code and s:DimensionList.
(3) List of all dataflows: .../sdmx/2.1/dataflow/ESTAT/all/latest?detail=allstubs (7 MB, 8146 flows).
(4) Full codelist: .../sdmx/2.1/codelist/ESTAT/<ID>/latest.
(5) Data: https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/<code>?format=JSON&lang=EN&<dim>=<code>&... Dimension ids are lowercase (sex, age, unit, citizen, isced11, isco08, wstatus, training, reason, geo). Repeat a parameter to select several values. Leaving out geo and time returns all countries and years. The response is JSON-stat 2.0: 'id' and 'size' give the dimension order, and 'value' and 'status' are sparse dicts keyed by a flat row-major index. To get coverage without reading values, decode only the keys of 'value'. 'status' holds flags with labels in extension.status.label: b = break, bd, d = definition differs, u = low reliability, bu. Filtered slices of a few thousand to 120k cells came back in seconds.
(6) Metadata pages: https://ec.europa.eu/eurostat/cache/metadata/en/employ_esms.htm, which confirms 'ISCO 88 (COM) and ISCO 08 (from 2011)' and 'ISCED 2011 (from 2014)'.

Geo codes: 2-letter countries (EL = Greece, UK) plus aggregates EU27_2020 and EA21 (EA20 in lfsi_*; the _h tables add EU28, EU15, EA19, FX). Drop aggregates and any code that is not 2 letters for a country panel.

Breaks hit nearly all countries in 2005, 2011 (occupation), 2014 (education tables) and 2021 (new IESS LFS regulation). ES and FR carry 'bd' in 2021 and 'd' from 2022. These break years suit dummies or a split-sample holdout.

Some cells are suppressed or flagged unreliable: unemployment rates at 60-64 and 65-69, lfsa_igar reasons for small groups, and occupations OC0/OC1/OC6 among 15-24s.

Scripts are in C:\Users\s6068C\AppData\Local\Temp\claude\C--Users-s6068C-GitHub-laborformal\57a37d3a-ed63-4c7d-9808-2133339ff86c\scratchpad\scout_eurostat\code\. cov.py, covreg.py and missing.py report coverage only; flags.py tallies status flags; struct.py lists structure; get.py and fetch_toc.py download raw files. The data folder next to code/ holds the TOC, the structure XMLs and cov_*.json coverage summaries (country first/last year and counts only, no values).

Blinding: no observation values were read, printed or kept. The only numbers above are years and counts of countries, regions or observations.

## eurostat_housing

- **ilc_lvps08** (Eurostat (EU-SILC)) — Persons living with their parents or contributing/benefiting from the household income (population aged 18 to 34 years) [formerly 'Share of young adults aged 18-34 living with their parents by age and sex']. Verified.
  - breakdowns: sex T/M/F; age Y16-19, Y16-24, Y16-29, Y18-24, Y18-34, Y20-24, Y20-29, Y25-29, Y25-34; unit PC
  - countries: 37 countries (EU27 + IS NO CH UK ME MK AL RS TR XK) + 9 aggregates (EU, EU27_2020, EU28, EU27_2007, EA, EA21, EA20, EA19, EA18). Most EU start 2003-2005; HR from 2010, RO from 2007; IS ends 2020, UK 2005-2018, CH ends 2024, XK 2018 only
  - years: 2003-2025 (annual)
  - notes: Full table = 22032 non-missing obs, all 9 age x 3 sex categories populated. The dataset label was changed (structure update 2026-04-30) to wording about 'contributing/benefiting from the household income'; the dataflow points to an ILC explanatory note (https://ec.europa.eu/eurostat/databrowser-backend/api/public/explanatory-notes/get/Info_note_ILC_20251009.pdf) that was NOT read - check whether the concept/definition changed before using it as a time series.
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/ilc_lvps08?format=JSON&lang=EN&sex=T&age=Y25-29`
- **ilc_lvps09** (Eurostat (EU-SILC)) — Share of young adults aged 18-34 living with their parents by self-defined current economic status. Verified.
  - breakdowns: wstatus EMP_FT, EMP_PT, UNE, EDUC, INAC_OTH; age Y18-24, Y18-34, Y25-34; no sex dimension
  - countries: 46 geo codes (37 countries + aggregates), same set as ilc_lvps08
  - years: 2003-2025
  - notes: 12330 non-missing obs in full table.
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/ilc_lvps09?format=JSON&lang=EN&age=Y25-34&wstatus=UNE`
- **ilc_lvps10** (Eurostat (EU-SILC)) — Share of young adults aged 18-34 living with their parents by type of contract. Verified.
  - breakdowns: wstatus SAL_PERM, SAL_TEMP; age Y18-24, Y18-34, Y25-34
  - countries: 45 geo codes with data; for Y25-34 SAL_TEMP DK and XK have no data
  - years: 2003-2025
  - notes: 4838 non-missing obs in full table; some countries have interior gaps (e.g. SE, NO, FI fewer years than span).
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/ilc_lvps10?format=JSON&lang=EN&age=Y25-34&wstatus=SAL_TEMP`
- **yth_demo_030** (Eurostat (LFS-based estimate)) — Estimated average age of young persons leaving the parental household. Verified.
  - breakdowns: sex T/M/F; unit AVG (years)
  - countries: 34 countries (EU27 + NO UK BA ME MK RS TR) + EU27_2020, EA21. Not available: IS, CH, AL, XK. Starts: most 2000-2004; IE 2006, SE 2009, DK 2010, NO only 2021-2025, BA 2021-2025, ME 2011-2020, RS 2014+, UK ends 2019, TR ends 2024
  - years: 2000-2025
  - notes: 2331 non-missing obs. Estimated series, not directly surveyed.
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/yth_demo_030?format=JSON&lang=EN`
- **ilc_lvps05** (Eurostat (EU-SILC)) — Distribution of population by sex, age and tenure status. Verified.
  - breakdowns: tenure OWN, OWN_L (owner with mortgage/loan), OWN_NL (owner outright), RENT, RENT_MKT (tenant market rent), RENT_FR (tenant reduced/free); sex T/M/F; age TOTAL, Y_LT16, Y_GE16, Y_LT18, Y18-24, Y18-64, Y_GE18, Y25-34, Y35-44, Y45-54, Y55-64, Y_GE65; unit PC
  - countries: 37 countries (EU27 + IS NO CH UK ME MK AL RS TR XK) + EU27_2020, EA21, EA20. Full 2015-2025 for all EU27, NO, RS, TR; IS 2015-2020, UK 2015-2018, CH/ME/MK to 2024, AL 2017-2023, XK 2018 only
  - years: 2015-2025
  - notes: 88776 obs in full table (TOC). This is the answer to 'tenure by age group' - but only from 2015.
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/ilc_lvps05?format=JSON&lang=EN&sex=T&age=Y25-34&tenure=OWN_L`
- **ilc_lvps15** (Eurostat (EU-SILC)) — Distribution of population by group of citizenship and tenure status (population aged 18 and over). Verified.
  - breakdowns: tenure OWN/RENT only; citizen NAT, FOR, EU27_2020_FOR, NEU27_2020_FOR (+ older EU28/EU27_2007 variants); sex T/M/F; age Y18-54, Y18-59, Y18-64, Y_GE18, Y20-64, Y25-54, Y25-59, Y55-64, Y_GE55, Y_GE60, Y_GE65 (no 25-34 band)
  - countries: 37 countries + aggregates; with citizen=NAT, age Y18-64: most from 2003-2007, DE from 2005 (with gaps), HR 2010
  - years: 2003-2025
  - notes: No TOTAL citizenship category; ilc_lvps16 (by country of birth) has the identical age/tenure structure (structure fetched only).
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/ilc_lvps15?format=JSON&lang=EN&citizen=NAT&sex=T&age=Y18-64&tenure=OWN`
- **ilc_lvho02** (Eurostat (EU-SILC)) — Distribution of population by tenure status, type of household and income group. Not verified.
  - breakdowns: tenure TOTAL, OWN, OWN_L, OWN_NL, RENT, RENT_MKT, RENT_FR; hhcomp 17 household types (incl. A1_LT65, A2_2LT65, A1_GE65, DCH/NDCH); rskpovth TOTAL/A_60/B_60. NO age dimension
  - countries: 46 geo codes (37 countries + 9 aggregates)
  - years: 2003-2025
  - notes: Structure fetched (codes listed), data cells not fetched.
  - example: `https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/dataflow/ESTAT/ilc_lvho02/latest?references=descendants&detail=referencepartial`
- **ilc_lvho07a** (Eurostat (EU-SILC)) — Housing cost overburden rate by age, sex and poverty status. Verified.
  - breakdowns: age TOTAL, Y_LT6, Y6-11, Y12-17, Y15-19, Y15-24, Y15-29, Y16-19, Y16-24, Y16-29, Y_LT18, Y18-24, Y18-64, Y20-24, Y20-29, Y25-29, Y_GE65 (no 30-34/25-34 band); sex T/M/F; rskpovth TOTAL/A_60/B_60; unit PC. No tenure dimension
  - countries: 37 countries + 9 aggregates; all 17 age bands populated for all 46 geos. DE from 2010; most others from 2003-2005; IS to 2020, UK 2005-2018, CH 2009-2024
  - years: 2003-2025
  - notes: 14047 non-missing obs for sex=T, rskpovth=TOTAL, all ages. Companion ilc_lvho08a = median housing cost burden by age/sex/poverty (not fetched).
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/ilc_lvho07a?format=JSON&lang=EN&sex=T&rskpovth=TOTAL&age=Y25-29`
- **ilc_lvho07c** (Eurostat (EU-SILC)) — Housing cost overburden rate by tenure status. Verified.
  - breakdowns: tenure TOTAL, OWN_L, OWN_NL, RENT_MKT, RENT_FR; unit PC. No age or sex dimension
  - countries: 37 countries + 9 aggregates; RENT_MKT: DE from 2010, EL/ES/CY/LV/LU/AT/PL from 2007, most others 2004-2006
  - years: 2003-2025
  - notes: Related: ilc_lvho28 (distribution by burden thresholds >25/40/50/60/75% x tenure, no age; structure only).
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/ilc_lvho07c?format=JSON&lang=EN&tenure=RENT_MKT`
- **prc_hpi_a** (Eurostat (HPI)) — House price index - annual data. Verified.
  - breakdowns: purchase TOTAL, DW_NEW, DW_EXST; unit I15_A_AVG, I25_A_AVG, RCH_A_AVG
  - countries: 31 countries: EU27 EXCEPT Greece (EL) + IS NO CH UK TR, + 7 aggregates. CH only in I25_A_AVG unit (not I15). Starts 2005 for most; ES/LV/LT/SK 2006, LU/HU/SI 2007, CZ/HR/PT 2008, RO 2009, IT/AT/PL/TR 2010; UK ends 2019, TR ends 2024
  - years: 2005-2025
  - notes: Base switched to 2025=100 (I25) alongside 2015=100 (I15).
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/prc_hpi_a?format=JSON&lang=EN&purchase=TOTAL&unit=I15_A_AVG`
- **tipsho20** (Eurostat (MIP scoreboard)) — House price index, nominal - annual data. Verified.
  - breakdowns: unit I15_A_AVG, I25_A_AVG, RCH_A_AVG, PCH_3Y
  - countries: EU27 only (includes EL) + EU27_2020, EA21, EA20. 2000-2025 for most; EE and PL from 2005, RO and SK from 2002
  - years: 2000-2025
  - notes: tipsho10 = deflated HPI (annual 2000-2025, not fetched).
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tipsho20?format=JSON&lang=EN&unit=I15_A_AVG`
- **tipsho60** (Eurostat (MIP scoreboard)) — Standardised house price-to-income ratio - annual data. Verified.
  - breakdowns: unit PTIR_I15 (index 2015=100), PTIR_LT_AVG (relative to long-term average), RCH_A_AVG
  - countries: EU27 + EU27_2020, EA21, EA20; 2000-2024 for most; EE, PL from 2005; RO, SK from 2002
  - years: 2000-2024
  - notes: Last data update 2026-04-16; 2025 not yet published.
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/tipsho60?format=JSON&lang=EN&unit=PTIR_I15`
- **prc_hicp_aind** (Eurostat (HICP, legacy ECOICOP v1)) — HICP - annual data (average index and rate of change) (1996-2025). Verified.
  - breakdowns: unit INX_A_AVG, RCH_A_AVG, CID_EA; coicop 467 codes incl. CP00 (all items), CP041 (actual rentals for housing), CP0411 (rentals paid by tenants), CP053 (household appliances), CP0531 (major appliances), CP0532, CP0531_0532, GD (goods), SERV (services), SERV_HOUS, IGD_NNRG_D (durables), NRG, TOT_X_* aggregates
  - countries: 38 countries (EU27 + IS NO CH UK ME MK AL RS TR XK US) + 7 aggregates. CP00 45 geos; CP041 44; CP0411 42; CP053 44; CP0531 42; GD/SERV 44. CP041/CP053: most EU 1996-2025, CZ/SI 2000, HU/RO 2001, HR 1998, CH/MK 2005, RS 2006, ME 2015, AL/XK 2016, UK to 2019. CP0531 starts LATE in this table: e.g. BE 2005, SI 2001, DK/IT/NL 2010, AT/BG 2013, SE 2014, CZ/DE/EL/LV/LU/HU/PL/PT 2015, EE/ES/HR/CY/MT/SK 2016, IE/RO/FI 2017; only FR, LT and few others full. SERV starts 2000-2001 for many countries
  - years: 1996-2025
  - notes: CLOSED legacy series (ends 2025, last update 2026-02-06). Continues as prc_hicp_ainr (ECOICOP v2).
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/prc_hicp_aind?format=JSON&lang=EN&unit=INX_A_AVG&coicop=CP00&coicop=CP041&coicop=CP053&coicop=CP0531&coicop=GD&coicop=SERV`
- **prc_hicp_ainr** (Eurostat (HICP, ECOICOP ver.2)) — Harmonised index of consumer prices (HICP) - ECOICOP ver.2 - indices and rates of change, annual data. Verified.
  - breakdowns: unit INX_A_AVG, RCH_A_AVG, CID_EA21, CID_EA20; dimension is 'coicop18' (553 codes) - all items = TOTAL (not CP00); CP041 (actual rental payments for housing), CP0411/CP04110 (tenants, main residence), CP053, CP0531 (major electric household appliances), CP0532, GD, SERV, SERV_HOUS, IGD_NNRG_D etc.
  - countries: 39 countries (EU27 + IS NO CH UK ME MK GE AL RS TR XK US) + 7 aggregates. TOTAL 46 geos; CP041/CP053/CP0531 44 geos; GD/SERV 45. CP0531 back-cast: most EU 1996-2025 (CZ/SI 2000, HU/RO 2001, HR 1998, BG/SK 1997), IS 2016+, NO 2000+, CH/MK 2005, RS 2006, ME 2015, AL 2016, XK 2015, GE 2025 only
  - years: 1996-2025 (annual); monthly prc_hicp_minr to 2026-09
  - notes: Preferred over prc_hicp_aind for appliances (CP0531 back-cast far longer). UK appears absent for CP041/CP0531 in this table.
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/prc_hicp_ainr?format=JSON&lang=EN&unit=INX_A_AVG&coicop18=TOTAL&coicop18=CP041&coicop18=CP0531&coicop18=GD&coicop18=SERV`
- **nama_10_lp_ulc** (Eurostat (national accounts)) — Labour productivity and unit labour costs - annual data. Verified.
  - breakdowns: na_item D1_SAL_PER (compensation per employee), D1_SAL_HW, NLPR_PER/HW, RLPR_PER/HW, NULC_PER/HW, EMP_HAB, HW_HAB, HW_EMP; unit EUR, NAC, PPS_EU27_2020, I20/I15/I10, PCH_PRE, etc.
  - countries: D1_SAL_PER (EUR or NAC): 34 countries with data = EU27 EXCEPT Croatia (HR has no data for this item) + IS NO CH UK BA ME MD RS; + 6 aggregates. Most 1995-2025; DE 1991, FR and NO 1975, FI 1980, SE 1993; UK to 2019; BA 2010-2024, ME 2006+, MD 2014-2024
  - years: 1975-2025 (mostly 1995-2025)
  - notes: Updated 2026-10-07.
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/nama_10_lp_ulc?format=JSON&lang=EN&na_item=D1_SAL_PER&unit=EUR`
- **nama_10_fte** (Eurostat (national accounts)) — Average full time adjusted salary per employee. Verified.
  - breakdowns: unit EUR, NAC; no other breakdown
  - countries: 26 countries = EU27 EXCEPT Netherlands (NL absent); no non-EU; + EU27_2020, EA20 (2002+). BE DK DE IE EL ES FR IT LU AT PT FI SE 1995+; others 1996-2002 starts
  - years: 1995-2024
  - notes: Last updated 2025-11-12; 2025 not yet available.
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/nama_10_fte?format=JSON&lang=EN&unit=EUR`
- **earn_nt_net** (Eurostat (tax-benefit model)) — Annual net earnings. Verified.
  - breakdowns: currency EUR, PPS, NAC; estruct TOTAL, GRS, TAX, SOC, FAM, NET; ecase 13 household cases (e.g. P1_NCH_AW100 single no children at 100% average wage, P1_NCH_AW67, couples with/without children)
  - countries: 34 countries: EU27 + IS NO CH UK TR US JP, + 6 aggregates. Most EU 2000-2025; BG/RO 2008+, HR 2013+, CY 2005+ (with gaps), MT 2005+; non-EU end 2023, UK to 2019
  - years: 2000-2025
  - notes: Model-based hypothetical earner, not survey data.
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/earn_nt_net?format=JSON&lang=EN&ecase=P1_NCH_AW100&estruct=NET&currency=EUR`
- **earn_ses_pub2a** (Eurostat (Structure of Earnings Survey)) — Median hourly earnings, all employees (excluding apprentices) by age. Verified.
  - breakdowns: age TOTAL, Y_LT30, Y30-49, Y_GE50 (broad bands, 44 geos); fine bands Y_LT20, Y20-29, Y30-39, Y40-49, Y50-59, Y_GE60 only 3 geos (CY, NO, MK); unit EUR, NAC, PPS; sizeclas GE10
  - countries: 44 geo codes with data (EU27 + IS NO CH UK BA ME MK AL RS TR + aggregates); Y_LT30: EU27 mostly all 5 waves, HR from 2010, CH 2010+, UK to 2018, TR to 2018, RS 2014+
  - years: 2006, 2010, 2014, 2018, 2022 (four-yearly)
  - notes: Microdata-rich earn_ses_hourly / earn_ses_annual (2002-2022) and earn_ses22_13/20 (2022, by age x NACE) exist but were not probed.
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/earn_ses_pub2a?format=JSON&lang=EN&unit=EUR&age=Y_LT30`
- **ilc_di03** (Eurostat (EU-SILC)) — Mean and median income by age and sex. Verified.
  - breakdowns: age 25 bands incl. Y16-24, Y18-24, Y25-49, Y25-54, Y50-64, Y55-64, Y18-64, Y_GE65 (no 25-34 band); sex T/M/F; statinfo MEAN_EI/MED_EI (equivalised disposable income); unit EUR, NAC, PPS
  - countries: 37 countries + aggregates (47 geo codes incl. EU15); Y18-24 MED_EI EUR: most 2003-2005 starts, HR 2010, RO 2007
  - years: 1995-2025 (ECHP 1995-2001, SILC 2003+)
  - notes: ilc_di09 = mean/median income by tenure (OWN/RENT) x age (TOTAL, Y_LT18, Y18-64, Y_GE18, Y_GE60, Y_GE65, Y_GE75) x sex, 1995-2025 - structure fetched only.
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/ilc_di03?format=JSON&lang=EN&age=Y18-24&sex=T&statinfo=MED_EI&unit=EUR`
- **demo_pjan** (Eurostat (demography)) — Population on 1 January by age and sex. Verified.
  - breakdowns: age single years (Y_LT1 ... open-ended) + TOTAL, 103 codes; sex T/M/F; unit NR
  - countries: 59 geo codes (EU27 + EFTA + candidates + others incl. UA, BY, RU, AM, AZ, GE, MD, AD, MC, SM) incl. aggregates; for age Y27 since 1990: EU27 mostly full 1990-2025, HR 2001+, CY 1993+, FR 1991+ (FX metropolitan 1960-2013), UK to 2019
  - years: 1960-2025
  - notes: 743221 obs (TOC).
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/demo_pjan?format=JSON&lang=EN&sex=T&age=Y27&sinceTimePeriod=1990`
- **demo_pjangroup** (Eurostat (demography)) — Population on 1 January by age group and sex. Verified.
  - breakdowns: age 5-year bands Y_LT5 ... Y80-84, Y_GE75, Y_GE80, Y_GE85, TOTAL, UNK; sex T/M/F
  - countries: 58 geos with data for Y25-29; most EU 1960-2025 (some with gaps: PL n=42, CY, MT 1977+, SI 1982+, RO 1968+, LV/LT 1970+); HR 2001+, FR 1991+
  - years: 1960-2025
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/demo_pjangroup?format=JSON&lang=EN&sex=T&age=Y25-29`
- **demo_pjanind** (Eurostat (demography)) — Population structure indicators at national level. Verified.
  - breakdowns: indic_de (55 codes) incl. OLDDEP1 (65+/15-64), OLDDEP2, OLDDEP3 (65+/20-64), OLDDEP4, DEPRATIO1-4, MEDAGEPOP, PC_Y20_39, PC_Y25_29, PC_Y15_29 etc.
  - countries: 58 geos with data for OLDDEP1; EU mostly 1960-2025 (EE, EL, LV, LT from 1970; CY 1976; MT 1977; SI 1982; RO 1968; HR 2001; FR 1991)
  - years: 1960-2025
  - notes: Dimension name is indic_de (lowercase, underscore).
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/demo_pjanind?format=JSON&lang=EN&indic_de=OLDDEP1`
- **educ_uoe_enra02** (Eurostat (UOE education)) — Pupils and students enrolled by education level, sex and age. Verified.
  - breakdowns: age single years 2-49 plus 5-year bands to Y_GE65; sex T/M/F; isced11 ED0-8, ED0..ED8; unit NR (counts)
  - countries: 39 countries (EU27 + IS LI NO CH UK BA ME MK GE AL RS TR) + EU27_2020, EU28. Age 25, ED0-8: most 2013-2024; CZ only 3 obs; NL to 2021; LI to 2022; UK 2014-2019; ME 2018+; RS 2015+
  - years: 2013-2024 (TOC says from 2012)
  - notes: Pre-2013 continuation is educ_enrl1tl (ISCED97, 1998-2012) - classification break.
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/educ_uoe_enra02?format=JSON&lang=EN&age=Y25&isced11=ED0-8&sex=T`
- **educ_uoe_enra05** (Eurostat (UOE education)) — Pupils and students in education by age group - % of corresponding age population. Verified.
  - breakdowns: age Y0-29, Y5-29, Y15-19, Y15-24, Y15-29, Y16-18, Y18, Y20, Y20-24, Y22, Y24, Y25-29, Y26; no sex
  - countries: 37 countries + EU27_2020, EU28. Single ages (Y20, Y22, Y24, Y26) 2012-2024 for 39 geos; bands Y20-24 only ~2014/2015-2022, Y25-29 and Y15-29 2015-2022; RO Y20-24 2022 only
  - years: 2012-2024
  - notes: 4722 obs in full table.
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/educ_uoe_enra05?format=JSON&lang=EN&age=Y20-24`
- **educ_enrl1tl** (Eurostat (UOE education, archived)) — Students by ISCED level, age and sex (1998-2012). Verified.
  - breakdowns: age single years 3-34 + bands; sex T/M/F; isced97 TOTAL, ED0..ED6; unit NR
  - countries: 35 countries + BE_FRA, BE_VLA; Y25 TOTAL: mostly 1998-2012; IE 1998-2008 (6 obs), HR/LI 2003+, CH 2002+, SK 2001+, AL 2000-2007
  - years: 1998-2012
  - notes: ISCED97 vs ISCED11 break at 2012/2013.
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/educ_enrl1tl?format=JSON&lang=EN&age=Y25&isced97=TOTAL&sex=T`
- **isoc_eb_p3d** (Eurostat (ICT usage in enterprises)) — 3D printing and robotics by size class of enterprise. Verified.
  - breakdowns: indic_is E_RBTI (industrial robots), E_RBTS (service robots), E_RBT (either), robot counts bands, service-robot purposes, reasons (E_RBTWHCL high labour cost, E_RBTWDR recruitment difficulty, etc.) + 3D printing items; size_emp GE10, 10-49, 50-249, GE250, 0-9 etc.; unit PC_ENT, PC_ENT_RBT, PC_ENT_RBTS
  - countries: 40 geo codes (EU27 + NO UK BA ME MK AL RS TR + aggregates). E_RBT GE10: 39 geos; most EU 2018/2020/2022; BE IE HR LV LU only 2020+2022; EL 2 waves; UK 2020 only; candidate countries 2020+2022
  - years: 2018, 2020, 2022 (3 waves only)
  - notes: isoc_eb_p3dn2 = same by NACE. Adjacent: isoc_eb_ai (AI use by enterprises; waves 2021, 2023, 2024, 2025; 36 geos; headline E_AI_TANY) verified with a small query.
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/isoc_eb_p3d?format=JSON&lang=EN&size_emp=GE10&indic_is=E_RBT&unit=PC_ENT`
- **isoc_eb_ai** (Eurostat (ICT usage in enterprises)) — Artificial intelligence by size class of enterprise. Verified.
  - breakdowns: indic_is 63 codes incl. E_AI_TANY (any AI technology), E_AI_TGE2, E_AI_TGE3, per-technology items; size_emp as above; unit PC_ENT etc.
  - countries: 36 geos: EU27 + NO BA ME MK AL RS TR + EU27_2020, EA
  - years: 2021, 2023, 2024, 2025
  - notes: 5313 non-missing obs for GE10/PC_ENT.
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/isoc_eb_ai?format=JSON&lang=EN&size_emp=GE10&unit=PC_ENT`
- **ilc_di09** (Eurostat (EU-SILC)) — Mean and median income by tenure status. Not verified.
  - breakdowns: tenure TOTAL, OWN, RENT; age TOTAL, Y_LT18, Y18-64, Y_GE18, Y_GE60, Y_GE65, Y_GE75; sex; statinfo MEAN_EI/MED_EI; unit EUR/NAC/PPS
  - countries: not probed (codelist only)
  - years: 1995-2025 (per structure annotation)
  - notes: Structure only.
  - example: `https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/dataflow/ESTAT/ilc_di09/latest?references=descendants&detail=referencepartial`
- **prc_hpi_ooa** (Eurostat (HPI)) — Owner-occupied housing price index - annual data. Not verified.
  - breakdowns: expend TOTAL, DW_ACQ, DW_ACQ_NEW, DW_ACQ_EXST, DW_OWN, etc.; unit I15_A_AVG, I25_A_AVG, RCH_A_AVG
  - countries: 36 geo codes (EU27 except EL + IS NO UK + aggregates) per codelist
  - years: 2005-2025
  - notes: Structure only.
  - example: `https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/dataflow/ESTAT/prc_hpi_ooa/latest?references=descendants&detail=referencepartial`

**Not found or not reachable.**
- No Eurostat table crosses housing cost overburden with BOTH age and tenure: ilc_lvho07a is age x sex x poverty status (no tenure); ilc_lvho07c is tenure only (no age, no sex); ilc_lvho28 is burden-threshold x tenure (no age). Searched the full TOC for 'tenure'.
- Full tenure split (owner outright / mortgage / market tenant / reduced-rent tenant) by age exists only from 2015 (ilc_lvps05). Before 2015 the only age x tenure tables are ilc_lvps15/ilc_lvps16 (OWN/RENT only, by citizenship / country of birth, broad bands such as Y18-64, Y25-54, Y55-64; no 25-34 band).
- ilc_lvho02 has no age dimension (household type x income group x tenure); ilc_lvho01 is by degree of urbanisation and dwelling type, not age.
- prc_hpi_a has no Greece (EL); Greece's house price index is only in tipsho20/tipsho10 (2000-2025). prc_hpi_a has no non-EU countries beyond IS, NO, CH (I25 base only), UK (to 2019), TR (2010-2024).
- nama_10_fte has no Netherlands and no non-EU countries; data end 2024.
- nama_10_lp_ulc D1_SAL_PER (compensation per employee): Croatia has no data although HR is in the codelist.
- earn_ses_pub2a: fine age bands (Y20-29, Y30-39 ...) only for CY, NO, MK; broad Y_LT30 / Y30-49 / Y_GE50 for all. SES is four-yearly (2006-2022), no annual young-worker wage series found.
- Robots: only 2018, 2020, 2022 waves in isoc_eb_p3d / isoc_eb_p3dn2; no later robot module and no robot stock/density series on Eurostat (IFR data not on Eurostat).
- HICP major household appliances CP0531 in the legacy prc_hicp_aind starts 2010-2017 for most countries; long CP0531 history only in the ECOICOP v2 table prc_hicp_ainr (dimension coicop18). UK seems absent for CP041/CP0531 in prc_hicp_ainr.
- Enrolment: participation-rate bands Y20-24 / Y25-29 in educ_uoe_enra05 only ~2015-2022; single-year ages run 2012-2024. ISCED97 (educ_enrl1tl, 1998-2012) to ISCED11 (2013+) classification break.
- yth_demo_030 (average age of leaving home) has no IS, CH, AL, XK; NO only 2021-2025; DK from 2010; SE from 2009; IE from 2006.
- ilc_lvps08 definition/label change (now 'Persons living with their parents or contributing/benefiting from the household income'): the linked ILC explanatory note PDF (Info_note_ILC_20251009.pdf) was not downloaded or read, so whether the concept changed is unresolved.

**Access.** Data endpoint: https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/<code>?format=JSON&lang=EN&<dim>=<code>... returns JSON-stat 2.0 (keys: id, size, dimension, value as a dict keyed by flat row-major index, status). Repeat a parameter to select several codes (coicop=CP00&coicop=CP041). sinceTimePeriod=YYYY works. Dimension names are the lowercase SDMX ids (indic_de, coicop, coicop18, isced11, rskpovth, wstatus, size_emp, indic_is, na_item, ecase, estruct); a wrong name gives HTTP 400 'INVALID_QUERY_DIMENSION'. Full small tables download whole without trouble (e.g. ilc_lvps08 complete ~300 KB; ilc_lvho07a with sex=T&rskpovth=TOTAL ~190 KB). No rate limiting hit across about 60 calls. Structure/codelists without data: https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/dataflow/ESTAT/<code>/latest?references=descendants&detail=referencepartial (SDMX-ML; codelists cut down to codes actually used; annotations OBS_PERIOD_OVERALL_OLDEST/LATEST give the year span, UPDATE_DATA gives last update). Full catalogue with data start/end and observation counts: https://ec.europa.eu/eurostat/api/dissemination/catalogue/toc/txt?lang=en (~2 MB TSV); grep it to find table families. HICP: the legacy prc_hicp_aind/midx/manr (ECOICOP v1, 'coicop' dimension, all-items = CP00) are closed at 2025; the continuing ECOICOP v2 tables are prc_hicp_ainr (annual) and prc_hicp_minr (monthly to 2026-09), dimension 'coicop18', all-items = TOTAL. House price index now has both 2015=100 (I15_A_AVG) and 2025=100 (I25_A_AVG) bases; CH only on I25. Euro-area aggregate codes now include EA21. Networking: truststore.inject_into_ssl() before importing requests works through the corporate proxy; UA 'Mozilla/5.0 (research; laborformal)'. Scripts: C:\Users\s6068C\AppData\Local\Temp\claude\C--Users-s6068C-GitHub-laborformal\57a37d3a-ed63-4c7d-9808-2133339ff86c\scratchpad\scout_eurostat_housing\code\probe.py (coverage-only: per-geo year span and counts, optional --by <dim> per-category coverage, never prints values) and struct.py (codelists from the SDMX dataflow); raw downloads in ...\scout_eurostat_housing\data\. BLINDING: no observation values were printed or looked at; only codes, years and counts of geos/observations.

## oecd

- **OECD.ELS.SAE,DSD_LFS@DF_LFS_INDIC,1.1** (OECD SDMX (sdmx.oecd.org/public/rest)) — Employment and unemployment by five-year age group and sex - indicators (includes labour force participation rate). Verified.
  - breakdowns: Key order: REF_AREA.MEASURE.UNIT_MEASURE.SEX.AGE.LABOUR_FORCE_STATUS. MEASURE: LF_RATE (participation rate, unit PT_POP_SUB), EMP_RATIO, UNE_RATE (PT_LF_SUB). SEX: F, M, _T. AGE has 40 codes: 5-year bands Y15T19, Y20T24, Y25T29, Y30T34, Y35T39, Y40T44, Y45T49, Y50T54, Y55T59, Y60T64, Y65T69, Y70T74, Y75T79, Y80T84, Y85T99; broad bands Y15T24, Y15T29, Y15T64, Y15T74, Y20T64, Y25T34, Y25T39, Y25T54, Y25T64, Y30T39, Y35T44, Y40T49, Y45T54, Y50T59, Y55T64, Y65T74, Y80T99; open bands Y_GE60, Y_GE65, Y_GE70, Y_GE75, Y_GE80, Y_GE85; plus _T and _U. LABOUR_FORCE_STATUS: LF, EMP, UNE. Annual. OBS_STATUS A, or B (series break).
  - countries: All 38 OECD members, plus ARG BGR BRA CHN CYP HRV IDN IND MKD MLT PER ROU RUS THA ZAF, DEU_F (West Germany, 1970-1998), and aggregates EU19OECD EU22OECD EU27 G7 OECD OECD_REP. That makes 60 areas.
  - years: 1960-2025. Every OECD member's series runs to 2025. First year for the 5-year bands under 65 (the 25-29 band): USA 1960; IRL 1961 for broad bands, 1981 for 5-year bands; FIN and SWE 1963; AUS 1966 for broad bands, 1978 for 25-29 and 30-34; JPN 1968; DEU and ITA 1970; NLD 1971 for broad bands, 1987 for 5-year bands; ESP and NOR 1972; PRT 1974; FRA 1975; CAN 1976; KOR 1980; BEL DNK GRC LUX 1983; GBR 1984; ISR 1985; NZL 1986; CRI 1987; TUR 1988; EST 1990; CHE ISL MEX 1991; HUN POL 1992; CZE 1993; AUT SVK 1994; CHL 1996; COL 2001; LTU LVA SVN 2000. For the bands under 65: 25 OECD members by 1990 and 37 by 2000. The 65-69 band starts later: 15 members by 1990 and 34 by 2000. Y_GE65: 20 by 1990 and 36 by 2000.
  - notes: This is the best single source for participation by sex and age. Male, female and total have the same coverage; checked for the 25-29 and 60-64 bands across all 38 members. Only the 1.1 version is current (1.0 also exists). The fetch returned 24,450 observations for women across 11 age codes. Series breaks are flagged OBS_STATUS=B and should be kept as a break indicator. The rate is persons in the labour force as a share of the population of the same sex and age.
  - example: `https://sdmx.oecd.org/public/rest/data/OECD.ELS.SAE,DSD_LFS@DF_LFS_INDIC,1.1/.LF_RATE..F.Y15T19+Y20T24+Y25T29+Y30T34+Y55T59+Y60T64+Y65T69+Y15T64+Y25T54+Y55T64+Y_GE65.?dimensionAtObservation=AllDimensions`
- **OECD.ELS.SAE,DSD_LFS@DF_LFS,1.1** (OECD SDMX) — Employment and unemployment by five-year age group and sex - levels. Verified.
  - breakdowns: Same DSD and key order as DF_LFS_INDIC: REF_AREA.MEASURE.UNIT_MEASURE.SEX.AGE.LABOUR_FORCE_STATUS. MEASURE=POP, UNIT_MEASURE=PS (persons). LABOUR_FORCE_STATUS: POP, LF, EMP, UNE. Same 40 age codes and SEX F/M/_T.
  - countries: All 38 OECD members plus the same non-members and aggregates as DF_LFS_INDIC; 59 areas in total.
  - years: 1960-2025. Coverage matches DF_LFS_INDIC: 25 members by 1990 and 37 by 2000 for 5-year bands; Y_GE65 20 by 1990 and 36 by 2000.
  - notes: Use this flow when rates must be rebuilt for non-standard age bands or weighted by population. The verification query returned 39,012 observations.
  - example: `https://sdmx.oecd.org/public/rest/data/OECD.ELS.SAE,DSD_LFS@DF_LFS,1.1/.POP.PS..Y25T29+Y60T64+Y_GE65.LF+POP?dimensionAtObservation=AllDimensions`
- **OECD.SDD.TPS,DSD_LFS@DF_IALFS_LF_WAP_Q,1.0** (OECD SDMX) — Infra-annual labour statistics: labour force participation rate. Verified.
  - breakdowns: Key order: REF_AREA.MEASURE.UNIT_MEASURE.TRANSFORMATION.ADJUSTMENT.SEX.AGE.ACTIVITY.FREQ. MEASURE=LF_WAP. ADJUSTMENT: Y (seasonally and calendar adjusted) or N (not adjusted). SEX: F, M, _T. Only broad age groups: Y15T24, Y25T54, Y55T64, Y15T64, Y15T74, Y_GE15. FREQ: Q, A and M.
  - countries: All 38 OECD members plus BGR BRA HRV ROU ZAF and aggregates EA EU OECD; 46 areas.
  - years: Quarterly, 1955-Q1 to 2026-Q3. Non-adjusted series: 5 OECD members by 1990 and 32 by 2000. Adjusted series: 26 by 2000. Starts range from 1955 to 2010.
  - notes: This flow has no 5-year age bands, so it supplements DF_LFS_INDIC and cannot replace it. Related flows in the same DSD: DF_IALFS_LF_Q (labour force levels), DF_IALFS_WAP_Q (working-age population), DF_IALFS_OLF_WAP_Q (population outside the labour force), DF_IALFS_EMP_WAP_Q and DF_IALFS_INDIC. Those were not fetched.
  - example: `https://sdmx.oecd.org/public/rest/data/OECD.SDD.TPS,DSD_LFS@DF_IALFS_LF_WAP_Q,1.0/.LF_WAP....F+M+_T.Y15T24+Y25T54+Y55T64+Y15T64..Q?dimensionAtObservation=AllDimensions`
- **OECD.ECO.MPD,DSD_AN_HOUSE_PRICES@DF_HOUSE_PRICES,1.0** (OECD SDMX) — Analytical house prices indicators. Verified.
  - breakdowns: Key order: REF_AREA.FREQ.MEASURE.UNIT_MEASURE. FREQ: A or Q. MEASURE: HPI (nominal house price index), RHP (real house price index), RPI (rent prices), HPI_RPI (price-to-rent), HPI_YDH (price-to-income), HPI_RPI_AVG (standardised price-rent ratio), HPI_YDH_AVG (standardised price-income ratio). UNIT_MEASURE: IX (index, BASE_PER=2015), or PT_AVG_L_TERM (percent of long-term average) for the _AVG ratios. ADJUSTMENT attribute = S.
  - countries: Areas by measure, out of the 38 OECD members. RPI: all 38. HPI, RHP and HPI_RPI: 37, missing CRI (Costa Rica has RPI only). HPI_YDH: 35, missing CRI MEX TUR. HPI_RPI_AVG and HPI_YDH_AVG: 24, missing CHL CRI CZE EST HUN ISL LVA LTU LUX MEX POL SVK SVN TUR. Also BGR BRA CHN HRV IDN IND ROU RUS SAU ZAF, with BRA CHN IDN IND SAU having HPI and RHP only. Aggregates: EA, EA17, OECD. 51 areas in total.
  - years: Annual, 1956-2025; quarterly up to 2026-Q3 per the constraint. First year of RHP: JPN 1960; GBR 1969; AUS BEL CAN CHE DEU DNK FIN FRA IRL ITA NLD NOR NZL SWE USA 1970; ESP 1971; COL PRT 1988; KOR 1986; ISR 1994; GRC 1997; AUT 2000; ISL 2001; CHL 2002; EST MEX POL SVK 2005; LTU LVA 2006; HUN LUX SVN 2007; CZE 2008; TUR 2010. RHP: 21 members by 1990 and 24 by 2000. RPI: 26 by 1990 and 38 by 2000; it is the longest series, starting 1956 for NZL. HPI_YDH: 19 by 1990 and 24 by 2000. Last years for HPI_YDH vary: ISR ends 2016, ISL 2019, KOR and COL 2024, most others 2025. KOR's house price series end in 2024.
  - notes: The annual pull covering all measures has 11,724 observations. Only version 1.0 exists. A related flow, OECD.SDD.TPS DSD_RHPI@DF_RHPI_ALL 1.1 (national and regional house price indices), was not fetched.
  - example: `https://sdmx.oecd.org/public/rest/data/OECD.ECO.MPD,DSD_AN_HOUSE_PRICES@DF_HOUSE_PRICES,1.0/.A..?dimensionAtObservation=AllDimensions`
- **OECD.ELS.SAE,DSD_EARNINGS@AV_AN_WAGE,1.0** (OECD SDMX) — Average annual wages. Verified.
  - breakdowns: Key order: REF_AREA.MEASURE.UNIT_MEASURE.PAY_PERIOD.PRICE_BASE.AGGREGATION_OPERATION.SEX. MEASURE=WG; PAY_PERIOD=A; AGGREGATION_OPERATION=MEAN. SEX=_Z only, so there is no sex or age split. PRICE_BASE: V (current prices) or Q (constant prices, BASE_PER=2025). UNIT_MEASURE: national currency codes (24 currencies) or USD_PPP. Available combinations: Q+USD_PPP, Q+national currency, V+national currency.
  - countries: All 38 OECD members plus BGR HRV ROU and the OECD aggregate; 42 areas. Constant-price USD PPP: all 38 members.
  - years: 1990-2025. Constant USD PPP: 24 members by 1990 and 38 by 2000, starting between 1990 and 1995. Current national currency: 21 by 1990 and 37 by 2000. Last years run 2023-2025; for example CHL ends 2023.
  - notes: The full pull has 4,031 observations. The definition is average annual wages per full-time-equivalent dependent employee. There is no breakdown by sex or age; see AGE_WAGE_GAP for age.
  - example: `https://sdmx.oecd.org/public/rest/data/OECD.ELS.SAE,DSD_EARNINGS@AV_AN_WAGE,1.0/......?dimensionAtObservation=AllDimensions`
- **OECD.ELS.SAE,DSD_EARNINGS@AGE_WAGE_GAP,1.0** (OECD SDMX) — Wage gap by age (youth-to-prime-age, senior-to-prime-age). Verified.
  - breakdowns: Key order: REF_AREA.MEASURE.UNIT_MEASURE.PAY_PERIOD.PRICE_BASE.AGGREGATION_OPERATION.SEX. MEASURE: Y_PA_WP (youth to prime-age wage gap) or S_PA_WP (senior to prime-age wage gap). UNIT: PT_WG_SAL_PA. AGGREGATION_OPERATION: MEAN or MEDIAN. SEX: F, M, _T.
  - countries: Y_PA_WP MEAN _T: 37 members, missing ISR. S_PA_WP MEAN _T: all 38. MEDIAN variants: 33-34 members, missing CZE NZL SWE GBR, and ISR for youth. HUN has no sex split for MEAN.
  - years: 1973-2025. First years range from 1973 to 2010; last years from 2018 to 2025. MEAN _T: 5 members by 1990 and 14 by 2000, so this is mostly a post-2000 panel.
  - notes: This is an extra; it was not requested. 72 rows in the pull had empty values and were excluded from the coverage counts.
  - example: `https://sdmx.oecd.org/public/rest/data/OECD.ELS.SAE,DSD_EARNINGS@AGE_WAGE_GAP,1.0/.......?dimensionAtObservation=AllDimensions`
- **OECD.ELS.SPD,DSD_PAG@DF_PAG,1.0** (OECD SDMX) — Pensions at a Glance (full flow: retirement ages, replacement rates, labour market exit age, context). Verified.
  - breakdowns: Key order: REF_AREA.FREQ.MEASURE.UNIT_MEASURE.SEX.AGE.OPTIONALITY. 32 measures, including: CRPLF22 (current normal retirement age for someone entering the labour force at 22, in years); FRPLF22 (future normal retirement age, same entry age); GPRR50/100/200 and NPRR50/100/200 (gross and net pension replacement rates at 50%, 100% and 200% of the average wage); ELMEA (effective labour market exit age, in years); EYLME (expected years after labour market exit); GPW and NPW (pension wealth); LE (life expectancy); OAWAR (old-age to working-age ratio); PEP (public pension spending, % of GDP); PPEP (projected pension spending); OAIP (old-age income poverty); income of older people (EDIOP, EIOP, CIOP, OCOP, PTOP); AWGW (average worker gross wage); ATRW, ATRAEP, ATRPPAE (average tax rates); FR (fertility rate); ER (employment rate). SEX: F, M, _T, _Z. OPTIONALITY for replacement rates: M (mandatory) or MV (mandatory plus voluntary).
  - countries: All 38 OECD members plus ARG BGR BRA CHN CYP HRV IDN IND MLT ROU RUS SAU ZAF and aggregates EU27, EU28, OECD_REP; 54 areas.
  - years: Most measures cover the single year 2024, the 2024 edition: CRPLF22, FRPLF22, the replacement rates, pension wealth, tax rates, AWGW, ER and FR. Real time series exist only for ELMEA and EYLME (annual 1970-2024; 33 members by 1990 and 37-38 by 2000), OAWAR (1950-2084, with projections), PEP (1990-2021, 5 time points), and the income measures (2014-2022, 5 time points). LE covers 2024 and 2065.
  - notes: The whole flow has 17,960 observations. Only version 1.0 exists, so no earlier editions are on SDMX. Retirement ages and replacement rates are a single 2024 cross-section and cannot be used as time-varying regressors from this source. The sub-flows DF_PRR, DF_DPS and DF_DEC are subsets of this flow (entries below). ELMEA has UNIT=Y, AGE=_Z and OPTIONALITY=_Z, by sex F/M; its annual series has no internal gaps.
  - example: `https://sdmx.oecd.org/public/rest/data/OECD.ELS.SPD,DSD_PAG@DF_PAG,1.0/.......?dimensionAtObservation=AllDimensions`
- **OECD.ELS.SPD,DSD_PAG@DF_DEC,1.0** (OECD SDMX) — Pensions at a Glance: demographic and economic context (effective labour market exit age). Verified.
  - breakdowns: Same DSD as DF_PAG. MEASURE: ELMEA, EYLME, LE, ER, OAWAR. SEX: F, M, _Z. Query used: .A.ELMEA....
  - countries: All 38 OECD members plus the same non-members as DF_PAG.
  - years: ELMEA is annual from 1970 to 2024. Members that start late: AUT 1995, DEU 1995, COL 1995 for men and 2006 for women, CRI 1985, ISR 1990, LTU 1994, LVA 1994. All other members start in 1970. 33 members by 1990; by 2000, 38 for men and 37 for women.
  - notes: The ELMEA query returned 5,143 observations. The OECD computes ELMEA from LFS participation changes over 5-year windows, so it is partly derived from the same source as DF_LFS_INDIC. Keep this in mind if it is used as an independent test.
  - example: `https://sdmx.oecd.org/public/rest/data/OECD.ELS.SPD,DSD_PAG@DF_DEC,1.0/.A.ELMEA....?dimensionAtObservation=AllDimensions`
- **OECD.ELS.SPD,DSD_PAG@DF_PRR,1.0** (OECD SDMX) — Pension replacement rates. Verified.
  - breakdowns: Same DSD. MEASURE: GPRR50/100/200 (unit PT_EARN_G_PRE_RET_INC) and NPRR50/100/200 (unit PT_EARN_N_PRE_RET_INC). SEX: F, M. OPTIONALITY: M (mandatory) for both sexes; MV (mandatory plus voluntary) for men only.
  - countries: All 38 OECD members for every measure, sex and optionality combination present; 52 areas.
  - years: 2024 only; one cross-section.
  - notes: 936 observations. There is no time variation; earlier PaG editions are not on SDMX.
  - example: `https://sdmx.oecd.org/public/rest/data/OECD.ELS.SPD,DSD_PAG@DF_PRR,1.0/.......?dimensionAtObservation=AllDimensions`
- **OECD.ELS.SPD,DSD_PAG@DF_DPS,1.0** (OECD SDMX) — Design of pension systems (normal retirement ages). Verified.
  - breakdowns: Same DSD. MEASURE: CRPLF22 (current) and FRPLF22 (future) normal retirement age for someone entering at 22, in years. SEX: F, M.
  - countries: All 38 OECD members plus non-members; 53 areas.
  - years: 2024 only.
  - notes: 209 observations. There is no historical retirement-age time series on SDMX.
  - example: `https://sdmx.oecd.org/public/rest/data/OECD.ELS.SPD,DSD_PAG@DF_DPS,1.0/.......?dimensionAtObservation=AllDimensions`
- **OECD.EDU.IMEP,DSD_EAG_LSO_EA@DF_LSO_TRANS,1.0** (OECD SDMX) — Education at a Glance - distribution of young adults' education and work status (NEET by labour status). Verified.
  - breakdowns: 17-position key: REF_AREA.SEX.AGE.ATTAINMENT_LEV.EDUCATION_FIELD.MEASURE.INCOME.BIRTH_PLACE.MIGRATION_AGE.EDU_STATUS.LABOUR_FORCE_STATUS.DURATION_UNEMP.UNIT_MEASURE.STATISTICAL_OPERATION.WORK_TIME_ARNGMNT.QUESTIONNAIRE.FREQ. NEET is EDU_STATUS=NED with LABOUR_FORCE_STATUS=NE (not in employment); it splits into UNE (unemployed NEET) and OLF (inactive NEET). EDU_STATUS=ED with LABOUR_FORCE_STATUS POP/EMP/NE gives the share in education, and the share in education and working or not working. Other EDU_STATUS codes: ED_E_O, ED_WS, ED_NED. AGE: Y15T19, Y20T24, Y25T29, Y15T24, Y15T29, Y18T24. SEX: F, M, _T. ATTAINMENT_LEV: _T or ISCED groups. STATISTICAL_OPERATION: OBS (use this) or SE. UNIT: PT_POP_SUB.
  - countries: NEET: 37 OECD members. KOR is missing: its rows exist but every value is empty. Non-members with values: ARG (2018 only), BGR, BRA, HRV, PER, ROU, ZAF; aggregates EU25, OECD. CHN, IDN and IND have only empty rows.
  - years: 1997-2025, using rows with values only. First years: AUS BEL CHE CZE DEU DNK ESP FRA GRC HUN LUX MEX NLD NOR POL PRT SVK SWE TUR USA 1997; ITA 1998; IRL 1999; GBR 2000; ISR LVA 2002; EST FIN ISL SVN 2003; AUT NZL 2004; LTU 2005 (14 observations, with gaps); COL 2007; CHL 2009 (8 observations, with gaps); CRI 2013. CAN covers 1997-2025 with 15 observations, so it has gaps. JPN covers only 2005-2014. ISL ends 2023. 24 members by 2000. Y18T24 is a newer band: only 2 members by 2000.
  - notes: The flow returns placeholder rows with empty OBS_VALUE (OBS_STATUS O). In the NEET pull, 17,619 of 57,510 rows were empty, so filter on non-empty values before measuring coverage. The education-status pull (ED with POP/EMP/NE) covers the same 37 members, from 1997 to 2013 (24 members by 2000). DF_LSO_TRANS_ALL is the full-dataset variant, and DF_LSO_TRANS_MIGR splits NEET by country of birth; neither was fetched.
  - example: `https://sdmx.oecd.org/public/rest/data/OECD.EDU.IMEP,DSD_EAG_LSO_EA@DF_LSO_TRANS,1.0/.F+M+_T.Y15T29+Y20T24+Y25T29+Y18T24+Y15T19._T......NED.NE+UNE+OLF...OBS...?dimensionAtObservation=AllDimensions`
- **OECD.EDU.IMEP,DSD_EAG_UOE_NON_FIN_STUD@DF_UOE_NF_ENRL_RATE,1.1** (OECD SDMX) — Enrolment rate by age (UOE administrative data). Verified.
  - breakdowns: 15-position key: REF_AREA.EDUCATION_LEV.MEASURE.EDUCATION_TYPE.INTENSITY.EDUCATION_FIELD.GRADE.FREQ.ORIGIN.DESTINATION.INST_TYPE_EDU.MOBILITY.UNIT_MEASURE.SEX.AGE. EDUCATION_LEV: _T or 21 ISCED-2011 levels. EDUCATION_TYPE: FE (formal education) or ISCED11_OUT. SEX: F, M, _T. AGE: single years Y1 to Y49, bands Y3T5, Y6T14, Y15T19, Y20T24, Y25T29, Y30T34, Y35T39, Y50T54, Y55T59, Y60T64, Y_GE65, and _T. Unit: PT_POP_SUB.
  - countries: All 38 OECD members plus BGR BRA HRV PER ROU and aggregates EU25, G20, OECD; 46 areas. Y30T34 has values for the OECD aggregate only.
  - years: 2013-2024, the ISCED-2011 era only. Most members start in 2013. Late starts: HRV 2014; JPN 2014 for Y15T19 and 2015 for other ages; CRI 2015; COL 2016. No member has data before 2013.
  - notes: The panel is short. For a longer enrolment proxy back to 1997, use the LSO_TRANS EDU_STATUS=ED share. 756 empty rows were excluded.
  - example: `https://sdmx.oecd.org/public/rest/data/OECD.EDU.IMEP,DSD_EAG_UOE_NON_FIN_STUD@DF_UOE_NF_ENRL_RATE,1.1/._T..FE..........F+M+_T.Y15T19+Y20T24+Y25T29+Y30T34+Y18+Y20+Y22+Y24+Y26+Y28?dimensionAtObservation=AllDimensions`
- **OECD.WISE.WDP,DSD_HSL@DF_HSL_CWB,1.1** (OECD SDMX) — How's Life? current well-being (includes youth NEET 15-24 and housing affordability). Verified.
  - breakdowns: Key order: REF_AREA.MEASURE.UNIT_MEASURE.AGE.SEX.EDUCATION_LEV.DOMAIN. MEASURE 2_4 is youth NEET, with UNIT PT_POP_Y15T24 or PT_POP_Y15T24_SUB. MEASURE 3_2 is housing affordability (unit PT_B7G_S14, share of household gross adjusted disposable income left after housing costs). MEASURE 3_3 is housing cost overburden (unit PT_POP). SEX: F, M, _T. AGE in this pull: _T. The flow has 68 measures in total.
  - countries: 2_4: 37 OECD members, missing KOR. 3_2: 37, missing ISR. 3_3: 36, missing ISR and NZL.
  - years: 2_4 runs from 2004-2013 (first year varies) to 2018-2024. 3_2 from 2004-2020 to 2021-2025. 3_3 from 2010-2016 to 2012-2024. All series start after 2000.
  - notes: This is an extra. The panel is short and starts after 2000. 3,517 observations for the three measures.
  - example: `https://sdmx.oecd.org/public/rest/data/OECD.WISE.WDP,DSD_HSL@DF_HSL_CWB,1.1/.3_2+3_3+2_4......?dimensionAtObservation=AllDimensions`

**Not found or not reachable.**
- Young adults living with parents: there is no OECD SDMX dataflow. I searched all 1,548 dataflow names and the measure codelists of Child Well-being (DF_CWB), How's Life (DF_HSL_*), regional housing (DSD_REG_SOC@DF_HOUSING) and the distributional national accounts household-type flows. The OECD publishes this indicator only in the Family Database and the Affordable Housing Database, as Excel downloads that are not on the SDMX API. For Europe, Eurostat ilc_lvps08/ilc_lvps09 is the usual alternative. For the US, CA, AU, NZ, JP and KR, national censuses or surveys would be needed.
- Historical statutory/normal retirement ages and pension replacement rates as time series: the SDMX Pensions at a Glance flows (DF_PAG, DF_DPS, DF_PRR, DF_PW) exist only as version 1.0 and hold only the 2024 edition (TIME_PERIOD=2024). Earlier editions (2005-2023) are available only as PDF/Excel annexes on oecd.org, not via the API.
- Pension replacement rates for women under the mandatory-plus-voluntary option (OPTIONALITY=MV): DF_PRR has MV for men only. Women have OPTIONALITY=M only.
- Average annual wages by sex or by age: AV_AN_WAGE has SEX=_Z only and no age dimension. The age split exists only as relative gaps in AGE_WAGE_GAP. The full earnings dataset (DSD_EARNINGS@DATASET) and the gender wage gap flow (GENDER_WAGE_GAP) were not explored.
- Annual LFS by age from the SDD.TPS ALFS family: DSD_ALFS@DF_SUMTAB 1.0 has only AGE=Y_GE15 (structure checked, data not fetched), so it is useless for age bands. The age-band source is OECD.ELS.SAE DSD_LFS@DF_LFS_INDIC / DF_LFS.
- NEET for Korea: DF_LSO_TRANS returns rows for KOR, but every value is empty (OBS_STATUS O). How's Life 2_4 also lacks KOR. Japan's LSO_TRANS NEET covers only 2005-2014.
- UOE enrolment rates before 2013: DF_UOE_NF_ENRL_RATE has only 2013-2024 (ISCED 2011). No pre-2013 enrolment-by-age series was found on SDMX. LSO_TRANS EDU_STATUS=ED from 1997 is the longest available proxy.
- Analytical house price ratios for Costa Rica (CRI): only RPI (rent index) exists. MEX and TUR have no price-to-income (HPI_YDH). The standardised long-term-average ratios (HPI_RPI_AVG, HPI_YDH_AVG) are missing for 14 members: CHL CRI CZE EST HUN ISL LVA LTU LUX MEX POL SVK SVN TUR.

**Access.** Python setup: use C:\Users\s6068C\GitHub\laborformal\venv\Scripts\python.exe with -I. Run `import truststore; truststore.inject_into_ssl()` before importing requests, and send the header User-Agent 'Mozilla/5.0 (research; laborformal)'. Every request succeeded through the corporate proxy. No HTTP 429 or 5xx responses came back in about 30 calls spread over roughly 20 minutes. common.py backs off 20 s × attempt on 429/5xx anyway, since the OECD documents a per-IP rate limit.

Discovery: GET https://sdmx.oecd.org/public/rest/dataflow/all with Accept 'application/vnd.sdmx.structure+xml; version=2.1' returns 8.9 MB of XML listing 1,548 flows. A parsed TSV (agency, id, version, English name) is saved at C:\Users\s6068C\AppData\Local\Temp\claude\C--Users-s6068C-GitHub-laborformal\57a37d3a-ed63-4c7d-9808-2133339ff86c\scratchpad\scout_oecd\data\dataflows.tsv.

Structure: GET dataflow/{agency}/{flowid}/{version}?references=all with the same Accept header. It returns the DSD (dimension order = key order), codelists, and an 'Actual' ContentConstraint. That constraint lists the codes actually present per dimension and the overall time range, though not per-country years.

Data: GET data/{agency},{flowid},{version}/{key}?dimensionAtObservation=AllDimensions&startPeriod=YYYY with Accept 'application/vnd.sdmx.data+csv; charset=utf-8'. The CSV comes back flat with code columns, TIME_PERIOD, OBS_VALUE and attributes (OBS_STATUS, UNIT_MULT, DECIMALS, BASE_PER and so on).

Keys: positions are separated by '.', an empty position is a wildcard, and '+' ORs codes. The number of positions must exactly match the DSD dimension count: 6 for ELS LFS, 4 for house prices, 7 for earnings and PAG, 9 for IALFS, 15 for UOE, 17 for LSO_TRANS. A wrong position count or an empty result gives HTTP 404 with the body 'NoResultsFound'; that happened once when IALFS was off by one dot.

Gotchas:
(1) The EAG/EDU flows return placeholder rows with empty OBS_VALUE (OBS_STATUS O), about 30% of LSO_TRANS rows. Filter non-empty values before measuring coverage.
(2) LSO_TRANS has a STATISTICAL_OPERATION dimension (OBS vs SE). Filter OBS or standard errors get mixed in.
(3) Series breaks are flagged OBS_STATUS=B in DF_LFS_INDIC and LSO_TRANS.
(4) Codelist names are UTF-8. The Windows console mangles them (e.g. Türkiye), so write to file.
(5) Naming a local script struct.py shadows the stdlib and breaks ssl; avoid stdlib module names.
(6) PAG time series beyond 2024 are projections: OAWAR runs to 2084, LE has 2065, PPEP to 2060.
(7) DF_LFS_INDIC and DF_LFS also carry DEU_F (West Germany, 1970-1998) alongside DEU (1970-2025), so choose one to avoid double counting.
(8) OECD_REP ('OECD average country') and the other aggregates should be dropped from country panels.

Blinding: every coverage fetch went through code\cov.py, which drops OBS_VALUE immediately after parsing. It never prints values and writes only values-stripped files (data\cov_<label>.csv: keys, TIME_PERIOD and attributes, no OBS_VALUE), plus structure XMLs (data\struct_*.xml). No values were viewed or summarised.

Scripts are in C:\Users\s6068C\AppData\Local\Temp\claude\C--Users-s6068C-GitHub-laborformal\57a37d3a-ed63-4c7d-9808-2133339ff86c\scratchpad\scout_oecd\code\: common.py (session, retry, paths), flows.py (dataflow list), dsdinfo.py (dimensions plus actual-constraint codes), cov.py (blinded coverage), o38.py (OECD-38 coverage counts from the stripped files).

## ilo_automation

- **EAP_DWAP_SEX_AGE_RT_A** (ILOSTAT (rplumber API), LFS database) — Labour force participation rate by sex and age (%), annual. Verified.
  - breakdowns: sex: SEX_T/SEX_M/SEX_F. Four age schemes in classif1: AGE_5YRBANDS (Y15-19, Y20-24 ... Y60-64, YGE65, YGE15), AGE_10YRBANDS (Y15-24, Y25-34, Y35-44, Y45-54, Y55-64, YGE65, YGE15), AGE_AGGREGATE (Y15-24, Y25-54, Y55-64, YGE65, YGE15), AGE_YTHADULT (Y15-24, Y15-64, YGE15, YGE25). Also has a 'source' column (survey/census id) and note columns
  - countries: All 43 of 43 OECD+EU (the 38 OECD members plus BGR, HRV, CYP, MLT, ROU). The ILO's own table of contents lists 316 ref_areas globally. Every country has all four age schemes
  - years: Overall 1946-2027. The latest year is 2025 for all 43 countries. Each country's trailing run of consecutive years with 5-year bands starts by 2000 in 40 countries, by 2005 in 42 and by 2010 in all 43. Late starters: COL 2007, HRV 2002, MEX 2002 (but 1990 for youth/adult), BGR, MLT and TUR 2000. Earliest: USA 1948, JPN 1953, CAN 1976. ISR's 5-year bands run only 1990-2011, but its 10-year bands run 1978-2024. Earlier census-only years go back to the 1940s-1960s with gaps. The survey source changes inside the run (possible series breaks) for AUT, CHE, CRI, ESP, EST, GBR, NLD, POL, PRT and ITA (3 sources)
  - notes: Fetched for all 43 countries in 4 chunks, 153,584 rows. By default the API returns one 'best source' per country and year; best_source=all returns the competing sources. Sibling tables with an extra split exist: by education (_EDU_), urban/rural (_GEO_), marital status (_MTS_), disability (_DSB_), place of birth (_CBR_) and citizenship (_CCT_).
  - example: `https://rplumber.ilo.org/data/indicator/?id=EAP_DWAP_SEX_AGE_RT_A&ref_area=AUS+AUT+BEL+CAN+CHL+COL+CRI+CZE+DNK+EST+FIN&format=.csv.gz`
- **EAP_2WAP_SEX_AGE_RT_A** (ILOSTAT (rplumber API), ILO modelled estimates (ILOEST, Nov. 2025)) — Labour force participation rate by sex and age -- ILO modelled estimates (%). Verified.
  - breakdowns: sex T/M/F. Age schemes AGE_AGGREGATE (Y15-24, Y25-54, Y55-64, YGE65, YGE15) and AGE_YTHADULT (Y15-24, Y15-64, YGE15, YGE25). No 5- or 10-year bands
  - countries: 43 of 43 OECD+EU (276 ref_areas globally)
  - years: 1990-2027, the same 38 years for every country with no gaps. Years after the last survey year are model projections
  - notes: These are model-imputed, not observed. Use for robustness only, not as the test outcome.
  - example: `https://rplumber.ilo.org/data/indicator/?id=EAP_2WAP_SEX_AGE_RT_A&ref_area=AUS+AUT+BEL+CAN+CHL+COL+CRI+CZE+DNK+EST+FIN&format=.csv.gz`
- **EMP_TEMP_SEX_AGE_OCU_NB_A** (ILOSTAT (rplumber API), LFS database) — Employment by sex, age and occupation (thousands), annual. Verified.
  - breakdowns: sex T/M/F. Age (classif1): AGE_10YRBANDS (Y15-24, Y25-34, Y35-44, Y45-54, Y55-64, YGE65, YGE15), AGE_AGGREGATE, AGE_YTHADULT. Occupation (classif2): OCU_ISCO08 major groups 0-9 plus X and TOTAL, OCU_ISCO88 major groups 0-9 plus X and TOTAL, OCU_SKILL (L1, L2, L3-4, X, TOTAL). ISCO is 1-digit only in this table
  - countries: 42 of 43. NZL is missing. CAN has only 2 years (2001, 2011). 178 ref_areas globally
  - years: Overall 1982-2025. ISCO-08 unbroken runs: most EU countries 2011-2024 (or 2025). Earlier starts: CHE 1991, JPN 2000, KOR 2000, USA 2003, GBR 2005, GRC 2006, COL 2007, POL 2008. Later starts: ISR 2012, TUR 2012, MEX 2013, CRI 2017, AUS 2018, CHL 2019. ISCO-08 runs end in or after 2024 for 39 of 42 countries (ISL and JPN end 2023). ISCO-88 runs cover mostly 1992-2010 (34 countries). OCU_SKILL spans both vintages: it starts by 2000 in 31 countries and by 2010 in 40, and ends in or after 2024 in 39
  - notes: 612,558 rows for the 42 countries. In the EU the classification switches from ISCO-88 to ISCO-08 in 2011, so a continuous series needs either a crosswalk or the OCU_SKILL grouping. Related table: EMP_TEMP_SEX_OCU_NB_A (sex x occupation, 296 ref_areas, 1969-2025 per the table of contents; not fetched per country).
  - example: `https://rplumber.ilo.org/data/indicator/?id=EMP_TEMP_SEX_AGE_OCU_NB_A&ref_area=LTU+LUX+MEX+NLD+NZL+NOR+POL+PRT+SVK+SVN+ESP&format=.csv.gz`
- **EMP_TEMP_AGE_OC2_NB_A** (ILOSTAT (rplumber API), LFS database) — Employment by age and occupation - ISCO level 2 (thousands), annual. Verified.
  - breakdowns: Age is only AGE_YTHADULT (Y15-24, YGE25, YGE15). No sex split. Occupation (classif2): OC2_ISCO08 (45 codes, 2-digit sub-major groups) or OC2_ISCO88 (30 codes)
  - countries: 40 of 43. CAN, KOR and NZL are missing. CHL has ISCO-08 only for 2022. MLT has only ISCO-88 (2009-2010)
  - years: ISCO-08 unbroken runs: EU mostly 2011-2024. Earlier starts: CHE 1996, JPN 2000, USA 2003, GBR 2005, GRC 2006, COL 2007, POL 2008. Later starts: AUS 2018, CRI 2017, MEX 2013, ISR and TUR 2012. ISCO-08 runs end in or after 2024 for 36 of 39 countries. ISCO-88 runs cover mostly 1992-2010
  - notes: Companion table EMP_TEMP_SEX_OC2_NB_A (sex x 2-digit ISCO, no age) was also fetched: 40 of 43 countries (same three missing), the same ISCO-08 run pattern, and 37 of 39 countries end in or after 2024. ILOSTAT has no 2-digit occupation table with 10-year age bands.
  - example: `https://rplumber.ilo.org/data/indicator/?id=EMP_TEMP_AGE_OC2_NB_A&ref_area=FRA+DEU+GRC+HUN+ISL+IRL+ISR+ITA+JPN+KOR+LVA&format=.csv.gz`
- **EMP_2EMP_SEX_OCU_NB_A** (ILOSTAT (rplumber API), ILO modelled estimates (ILOEST, Nov. 2025)) — Employment by sex and occupation -- ILO modelled estimates (thousands). Verified.
  - breakdowns: sex T/M/F. Occupation is ISCO-08 1-digit, with codes OCU_ISCO08_1, _2, _3, _4, _5, _7, _8, _96 and _TOTAL (code 96 is a combined group; no separate 6, 9 or 0)
  - countries: 43 of 43 OECD+EU (276 ref_areas globally)
  - years: 1991-2025, the same 35 years for every country with no gaps
  - notes: Modelled, and has no age split.
  - example: `https://rplumber.ilo.org/data/indicator/?id=EMP_2EMP_SEX_OCU_NB_A&ref_area=SWE+CHE+TUR+GBR+USA+BGR+HRV+CYP+MLT+ROU&format=.csv.gz`
- **EIP_NEET_SEX_RT_A** (ILOSTAT (rplumber API), LFS database) — NEET rate: share of youth not in employment, education or training, by sex (%). Verified.
  - breakdowns: sex T/M/F. Youth means age 15-24 only. A sibling table, EIP_NEET_SEX_AGE_RT_A, adds age AGE_YTHBANDS (Y15-19, Y20-24, Y15-24)
  - countries: EIP_NEET_SEX_RT_A has 43 of 43 (278 ref_areas globally). EIP_NEET_SEX_AGE_RT_A has 40 of 43 (ISR, JPN and NZL missing)
  - years: Overall 1970-2027 (table of contents). Unbroken runs start by 2000 in 27 countries, by 2005 in 38 and by 2010 in 39; 41 of 43 end in or after 2024. Thin coverage: KOR only 2000-2002; JPN 2009-2019 (10 years, gaps); CHL has 23 years over 1990-2025 but is unbroken only from 2020; COL has 22 years over 2002-2025 but is unbroken only from 2021; AUS from 2009; ISR 2012-2024. Long runs: CAN 1976-2025; BEL, DNK, FRA, ITA and LUX 1983-2025
  - notes: No 25-29 or 15-29 NEET in ILOSTAT, so look to Eurostat or OECD for those. Other sibling splits exist (education, urban/rural, place of birth and others).
  - example: `https://rplumber.ilo.org/data/indicator/?id=EIP_NEET_SEX_RT_A&ref_area=AUS+AUT+BEL+CAN+CHL+COL+CRI+CZE+DNK+EST+FIN&format=.csv.gz`
- **Final_Scores_ISCO08_Gmyrek_et_al_2025.xlsx (+ 4digits_with_tasks.xlsx)** (ILO / Gmyrek et al. 2025, ILO Working Paper 140 (GitHub pgmyrek/2025_GenAI_scores_ISCO08, linked from the ILO WP140 web page)) — Refined global index of occupational exposure to generative AI (task- and occupation-level scores). Verified.
  - breakdowns: Task level, keyed to ISCO-08 4-digit units. Columns: label4d, label1d, ISCO_08, Title, taskID, Task_ISCO, score_2023, predicted_score_2025_gpt4o, predicted_score_2025_gemini (with justifications), score_2025, source, mean_score_2023, mean_score_2025, SD_2023, SD_2025, potential25, potential23 (exposure-gradient categories). The second file carries the isco08_1d to 5d hierarchy labels plus potential25
  - countries: Occupation-level (applies to any country through ISCO-08 employment weights)
  - years: 2023 and 2025 score vintages (published May 2025, repo updated 2026-09)
  - notes: 3,265 task rows covering 427 distinct ISCO-08 4-digit codes. Each sheet has 3,265 rows. The repo has no LICENSE file; the WP140 paper is CC BY 4.0. Because ILOSTAT occupation tables are 1- or 2-digit only, the 4-digit scores must be aggregated, either unweighted or with outside weights. The repo also holds the WP140 PDF. A related repo, pgmyrek/POLAND_2025_GenAI_scores_6digit_occupations, holds Polish 6-digit scores and an ISCO_mapping.csv; it was not fetched.
  - example: `https://raw.githubusercontent.com/pgmyrek/2025_GenAI_scores_ISCO08/main/Final_Scores_ISCO08_Gmyrek_et_al_2025.xlsx`
- **output_data.json** (ILO / Gmyrek, Berg & Bescond 2023, ILO Working Paper 96 (GitHub pgmyrek/GenAI_Exposure_Radial_Plot, CC0)) — GenAI exposure scores by ISCO-08 4-digit occupation (2023 index). Verified.
  - breakdowns: A hierarchical JSON tree from 1-digit down to 4-digit groups. Each leaf has a 'name' and a 'risk' field
  - countries: Occupation-level
  - years: 2023 vintage
  - notes: 436 4-digit leaves. The task-level 2023 scores are also in the 2025 workbook (column score_2023).
  - example: `https://raw.githubusercontent.com/pgmyrek/GenAI_Exposure_Radial_Plot/main/output_data.json`
- **AIOE_DataAppendix.xlsx (Appendix A-E); 'Language Modeling AIOE and AIIE.xlsx'; 'Image Generation AIOE and AIIE.xlsx'** (Felten, Raj & Seamans (GitHub AIOE-Data/AIOE)) — AI Occupational Exposure (AIOE), industry exposure (AIIE) and geographic exposure (AIGE), plus generative-AI (language modeling and image generation) variants. Verified.
  - breakdowns: Appendix A: AIOE by US SOC 6-digit code (774 occupations). B: AIIE by NAICS 4-digit (250 industries). C: AIGE by US county FIPS (3,271 rows). D: AI application x O*NET ability matrix. E: ability-level exposure. The language-modeling file has an LM AIOE sheet (774 SOC codes) and an LM AIIE sheet (250 NAICS codes)
  - countries: US occupation codes. Not ISCO, so a SOC to ISCO-08 crosswalk is needed
  - years: Built from 2019-2020 O*NET/OES inputs (SOC 2010-era codes; check the vintage before crosswalking)
  - notes: The repo also includes construction code and inputs (Stata). Cite Felten, Raj & Seamans (2021), Strategic Management Journal 42(12).
  - example: `https://raw.githubusercontent.com/AIOE-Data/AIOE/main/AIOE_DataAppendix.xlsx`
- **data/occ_level.csv (+ full_labelset.tsv task level)** (Eloundou, Manning, Mishkin & Rock, 'GPTs are GPTs' (GitHub openai/GPTs-are-GPTs)) — LLM exposure ratings by O*NET-SOC occupation. Verified.
  - breakdowns: Columns: O*NET-SOC Code (8-character XX-XXXX.XX), Title, dv_rating_alpha/beta/gamma (GPT-4 ratings) and human_rating_alpha/beta/gamma
  - countries: US O*NET-SOC codes. To get ISCO-08 you need O*NET-SOC to SOC to ISCO-08
  - years: 2023 vintage
  - notes: 923 occupations. The repo also has task-level labels, an O*NET-to-SOC crosswalk (nem-onet-to-soc-crosswalk.xlsx) and BLS employment files.
  - example: `https://raw.githubusercontent.com/openai/GPTs-are-GPTs/main/data/occ_level.csv`
- **data-raw/stata_dset/onetsoc_to_isco_cws_ibs/soc10_isco08.dta** (IBS (Hardy, Keister & Lewandowski) crosswalks, redistributed in GitHub eworx-org/iscoCrosswalks) — US SOC 2010 to ISCO-08 crosswalk. Verified.
  - breakdowns: Two columns: soc10 (6-digit) and isco08 (4-digit; 20 entries are 3-character codes, which look like dropped leading zeros or armed forces, so check them). The same folder has onetsoc09_onetsoc10, soc00_soc10 and isco88_soc00 bridges; the repo also has O*NET 2010-to-2019 crosswalks
  - countries: n/a
  - years: SOC 2010 / ISCO-08
  - notes: 1,131 pairs covering 839 SOC codes and 436 ISCO-08 codes. It is many-to-many, so it needs employment weights. The official BLS crosswalk (bls.gov/soc/ISCO_SOC_Crosswalk.xls) returned 403 from this machine.
  - example: `https://raw.githubusercontent.com/eworx-org/iscoCrosswalks/master/data-raw/stata_dset/onetsoc_to_isco_cws_ibs/soc10_isco08.dta`
- **HS 847950 (industrial robots n.e.s.), flowCode M (imports), partnerCode 0 (World)** (UN Comtrade public API (no key)) — Imports of industrial robots by reporter country and year (robot-adoption proxy). Verified.
  - breakdowns: Reporter x year x flow. Exports (flowCode X) and bilateral partners are also available; only imports from World were tested. Each record holds a trade value plus a quantity: qtyUnitCode 5 (number of items) in 3,043 of 3,457 reporter-year rows, kg in 173, N/A in 241. The data are as reported, under HS vintages H1-H6
  - countries: All 43 OECD+EU appear. Over 1996-2025 most have all 30 years; the exceptions are CYP 25, LTU 26, ISL 27, LUX 27, CRI 28, LVA 28, and CHL, CZE, DNK, HRV, ROU and SVK 29. Over 2007-2024 every country has all 18 years except CYP (16). Reporters per year: 42 in 1996, 120 or more from 2008, 136 in 2024
  - years: 1996-2025. There is no 1995 data (the code dates from HS1996). 2025 is still incomplete (106 reporters so far, 42 of the 43)
  - notes: Leaving out reporterCode returns all reporters in one call. The preview endpoint returns null labels (reporterISO, cmdDesc, qtyUnitAbbr), so map codes with the reference files Reporters.json and QuantityUnits.json. These are imports, not installations, so the series misses domestic production (it undercounts the JPN, DEU and KOR producers).
  - example: `https://comtradeapi.un.org/public/v1/preview/C/A/HS?period=2022&partnerCode=0&partner2Code=0&cmdCode=847950&flowCode=M&customsCode=C00&motCode=0`
- **isoc_eb_p3d (by size class); isoc_eb_p3dn2 (by NACE Rev.2)** (Eurostat (ICT usage in enterprises survey)) — 3D printing and robotics use by enterprises. Verified.
  - breakdowns: indic_is includes E_RBTI (industrial robots), E_RBTS (service robots), E_RBT (either), robot-count bands (E_RBT_LT5, E_RBT_5_10, E_RBT_GT10), service-robot purposes and reasons for using robots. size_emp has 8 classes (GE10 is the headline). unit includes PC_ENT. isoc_eb_p3dn2 has 51 NACE codes
  - countries: E_RBTI, GE10, PC_ENT. 2018: 23 countries (BG CZ DK DE EE EL ES FR IT CY LT HU MT NL AT PL PT RO SI SK FI SE NO; BE, IE, HR, LV, LU and UK missing). 2020: 33 (EU minus EL, plus NO, UK, TR, BA, ME, MK, RS). 2022: 34 (all EU27 plus NO, TR, BA, ME, MK, AL, RS). No non-European OECD countries
  - years: 2018, 2020, 2022 only
  - notes: Too few waves for a time-series test. Mainly useful as a cross-sectional validation.
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/isoc_eb_p3d?lang=en`
- **isoc_eb_ai (by size class); isoc_eb_ain2 (by NACE, 2021-2025); isoc_r_eb_ain2 (NUTS2, 2023-2025)** (Eurostat (ICT usage in enterprises survey)) — Artificial intelligence use by enterprises. Verified.
  - breakdowns: 63 indic_is codes, e.g. E_AI_TANY (uses at least one AI technology), technology types (TTM, TSR, TNLG, TIR, TML, TPA, TAR), purposes, sourcing and barriers. size_emp has 8 classes; unit has 6 codes
  - countries: E_AI_TANY, GE10, PC_ENT. 2021: 33 countries (EU27, NO, BA, ME, AL, RS, TR). 2023: 32 (no AL). 2024 and 2025: 33. No non-European OECD countries
  - years: 2021, 2023, 2024, 2025
  - notes: Only isoc_eb_ai was fetched; the NACE and NUTS2 versions were seen only in the catalogue.
  - example: `https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/isoc_eb_ai?lang=en`
- **capital accounts (K_IT, K_CT, K_Soft_DB, K_OMach ...; I_*, Iq_*, Kq_*); growth accounts (CAPICT_QI, CAPNICT_QI, VAConTangICT ...)** (EU KLEMS & INTANProd (LUISS Lab, 2023 release)) — ICT and non-ICT capital stocks, investment and capital services by country x NACE industry. Not verified.
  - breakdowns: Asset types: IT, CT, Soft_DB, TraEq, OMach, OCon, Rstruc, Cult, RD, OIPP, plus the intangibles in the analytical module. Values come in current prices, previous-year prices, chain-linked volumes (2015) and price indices. 59 NACE Rev.2 codes, including aggregates (TOT, MARKT, sections and divisions)
  - countries: AT BE BG CY CZ DE DK EE EL ES FI FR HR HU IE IT JP LT LU LV MT NL PL PT RO SE SI SK UK US, plus aggregates EU27_2020, EU11 and EU12. The data map shows CAPICT_QI with industry detail for AT, CZ, DE, DK, FI and UK (55 industries each), SK 53, LV 50, SE 49, FR, IT and NL 47, BE 46, LU 28, ES 27, SI 22, LT 18 and US 13. BG, EE, EL, HR, IE, PL, PT and RO have only 1 series each. CY, HU, JP and MT have none
  - years: 1995-2020 (some countries start in 2000; DK ends 2019, EL 2015)
  - notes: Only the metadata were fetched: Variable-List-2023.xlsx and the Data_Map_Growth_Accounting coverage map (88,792 rows of industry x country x variable with start, end and year count), both from luiss.it. The data files (CSV, Stata, R and per-country xlsx) are hosted on Dropbox, which the corporate proxy blocks. There is no robot asset; the closest is OMach (other machinery).
  - example: `https://euklems-intanprod-llee.luiss.it/wp-content/uploads/2023/02/Data_Map_Growth_Accounting.xlsx`
- **robot_exposure/robot_exposure_occupations.csv; labor_market_impacts/job_exposure.csv; release_*/ aei_*claude_ai* country files** (Anthropic Economic Index (Hugging Face Anthropic/EconomicIndex)) — Occupation-level robot-exposure and observed AI-exposure indices; country-level Claude usage snapshots. Verified.
  - breakdowns: robot_exposure_occupations: 923 O*NET-SOC 2019 codes, column robot_exposure_index (a task file of about 100 MB also exists). job_exposure: 756 SOC occ_code values, column observed_exposure. Country files (Aug 2025 snapshot) have columns geo_id (ISO2), geography (country/global/state_us), date_start, date_end, facet (country, onet_task, request, collaboration), variable (usage_count, usage_pct, onet_task_pct ...) and value
  - countries: The Aug 2025 snapshot has 171 ISO2 country codes, including all 43 OECD+EU. Later snapshots were not checked
  - years: Usage snapshots: Aug 2025 (release_2025_09_15), Nov 2025 (release_2026_01_15), Feb 2026 (release_2026_03_24), Apr-May 2026 (release_2026_06_26)
  - notes: Extra, not requested. Only the Aug 2025 country file and the two occupation files were downloaded; the later country files are 40-220 MB. The country data measure usage of a single AI product, which is post-treatment and covers only about a year.
  - example: `https://huggingface.co/datasets/Anthropic/EconomicIndex/resolve/main/robot_exposure/robot_exposure_occupations.csv`

**Not found or not reachable.**
- IFR World Robotics (robot installations and operational stock by country x industry x application, 1993-2025): proprietary. It is sold through the VDMA online shop (Premium data-query edition about EUR 2,500 excluding VAT) under a licence agreement, and there is no public API or redistributable file. Only press-release headlines are free. Confirmed from ifr.org and vdmashop.de listings; nothing was downloaded.
- WITS API for HS6 robot trade: the WITS tradestats-trade API accepts only aggregated product groups (HS sections, Total, UNCTAD stages of processing). product=847950 returns 'Invalid Product Code', and the WITS Comtrade web page for 847950 returns an error page. HS6 detail in WITS needs a WITS login or desktop query, so use UN Comtrade directly.
- EU KLEMS & INTANProd data files (capital, growth, national and labour accounts in CSV/Stata/R/xlsx): every download link points to dropbox.com or dl.dropboxusercontent.com, and the corporate proxy returns HTTP 403 with an 'Access Denied' policy page. Only the metadata on luiss.it (variable list and coverage data map) could be fetched. The data need another network or a manual download by the user.
- BLS official ISCO-08 to SOC 2010 crosswalk (bls.gov/soc/ISCO_SOC_Crosswalk.xls): HTTP 403 (bot blocking). The IBS crosswalk on GitHub was used instead.
- IMF Pizzinelli et al. (2023) complementarity-adjusted AIOE / theta file: not public. It is shared by email from the authors under a no-redistribution licence (per the World Bank reproducibility catalogue entry).
- ILO Gmyrek et al. country-level GenAI exposure shares (computed from LFS microdata in WP96/WP140): not published as a downloadable file; they appear only in the paper's tables and figures. Only the occupation-level scores are public.
- ILOSTAT has no NEET series for ages 25-29 or 15-29 (youth bands 15-19, 20-24 and 15-24 only), and no table crossing ISCO 2-digit occupation with 10-year age bands (EMP_TEMP_AGE_OC2 has youth/adult only).
- ILOSTAT occupation x age gaps: NZL is absent from EMP_TEMP_SEX_AGE_OCU_NB_A; CAN has only 2001 and 2011; CAN, KOR and NZL are absent from the 2-digit tables (EMP_TEMP_AGE_OC2_NB_A, EMP_TEMP_SEX_OC2_NB_A); MLT has no ISCO-08 2-digit data.
- Eurostat robot/AI enterprise tables do not cover non-European OECD countries (USA, JPN, KOR, CAN, AUS, NZL, ISR, CHE, ISL, MEX, CHL, COL, CRI). Robot use has only the 2018, 2020 and 2022 waves.
- Gmyrek 2025 GitHub repo: no LICENSE file in the repo (the WP140 paper itself is CC BY 4.0), so check reuse terms before redistributing derived files.

**Access.** BLINDING: every coverage script dropped obs_value and value columns before summarising, and only codes, years and row/country counts were printed. The scripts are in C:\Users\s6068C\AppData\Local\Temp\claude\C--Users-s6068C-GitHub-laborformal\57a37d3a-ed63-4c7d-9808-2133339ff86c\scratchpad\scout_ilo_ai\code\ (the shared helper common.py does the truststore injection and sets the User-Agent; the ILO coverage scripts are ilo_cov.py and ilo_cov2.py). Raw downloads are in ...\scout_ilo_ai\data\. Nothing was written to the repo. The repo already has an ILO helper (paths/code/exposure.py) and an ILO cache (paths/cache/ilo/).

ILOSTAT rplumber:
- Data: https://rplumber.ilo.org/data/indicator/?id=<ID>&ref_area=AAA+BBB+CCC&format=.csv.gz. Multiple countries are joined with '+'. Optional filters: sex=SEX_F, classif1=AGE_10YRBANDS_Y25-34, classif2=OCU_ISCO08_2, timefrom/timeto/time, latestyear=TRUE, best_source=yes|all (default yes, meaning one source per country and year), type=code|label|both. Up to 3 ids per call.
- Chunks of about 11 countries returned 0.2-1.1 MB gz in a few seconds, with no rate-limit problems.
- Indicator table of contents: https://rplumber.ilo.org/metadata/toc/indicator/?lang=en&format=.csv (1,964 indicators, with data.start, data.end and n.ref_area). Country table of contents: /metadata/toc/ref_area/?lang=en&format=.csv. Code dictionaries: /metadata/dic/?var=classif1. API spec: https://rplumber.ilo.org/openapi.json.
- CSV columns: ref_area, source, indicator, sex, classif1, classif2, time, obs_value, obs_status, note_classif, note_indicator, note_source. Classification codes carry a scheme prefix (AGE_5YRBANDS_, AGE_10YRBANDS_, OCU_ISCO08_, OCU_ISCO88_, OCU_SKILL_, OC2_ISCO08_), and several schemes are mixed in one file, so filter on the prefix. Use the source column to detect series breaks.

UN Comtrade public preview:
- https://comtradeapi.un.org/public/v1/preview/C/A/HS?period=YYYY&partnerCode=0&partner2Code=0&cmdCode=847950&flowCode=M&customsCode=C00&motCode=0 works without a key. Leaving out reporterCode returns all reporters.
- The preview caps results at 500 records per call and returns HTTP 429 when calls are only about 1-2 s apart; a 6 s sleep between calls worked.
- Label fields are null in the preview. Map them with https://comtradeapi.un.org/files/v1/app/reference/Reporters.json and QuantityUnits.json (qtyUnitCode 5 = number of items).

Eurostat:
- JSON-stat at https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/<code>?lang=en. The catalogue is at https://ec.europa.eu/eurostat/api/dissemination/catalogue/toc/txt?lang=en. Both work through the proxy.

Other hosts:
- GitHub raw and api.github.com work, as do Hugging Face resolve URLs.
- dropbox.com is blocked by corporate policy (403), which affects EU KLEMS; bls.gov returns 403.
- The ILO WP140 page (webapps.ilo.org/static/english/intserv/working-papers/wp140/index.html) links the exposure data repo at https://pgmyrek.github.io/2025_GenAI_scores_ISCO08/; the repo is github.com/pgmyrek/2025_GenAI_scores_ISCO08.

## us

- **LFPR 20-24: LNS11300036 (T) / LNS11300037 (M) / LNS11300038 (W); 25-34: LNS11300089 (T) / LNS11300164 (M) / LNS11300327 (W); 25-54: LNS11300060 / LNS11300061 (M) / LNS11300062 (W); 55-64 (NSA only): LNU01300095 (T) / LNU01300190 (M) / LNU01300347 (W); 60-64 (NSA only): LNU01300096 (T) / LNU01300197 (M) / LNU01300352 (W)** (BLS CPS (LN) via BLS public API v1) — Civilian labor force participation rate by sex and age (monthly). Verified.
  - breakdowns: sex T/M/W; ages 20-24, 25-34, 25-54, 55-64, 60-64. The 'LNS' codes are seasonally adjusted. 55-64 and 60-64 exist only as NSA ('LNU'); there is no SA version by sex. Also available, confirmed through DBnomics metadata but not through the BLS API: 16-19 LNS11300012/13/14, 16-24 LNS11324887/85/86, 55+ LNS11324230/31/32, 65+ LNU01300097/199/354
  - countries: USA (national) only
  - years: 1948-01 to 2026-09 monthly (60-64: from 1976-06). 2025-10 is missing (footnote: 'Data unavailable due to the 2025 lapse in appropriations'). January 2026 was revised for new population controls
  - notes: All 22 LFPR/EPOP codes returned data in one v1 call. Start years were checked on data.bls.gov/timeseries/<id>?from_year=1913 pages (year row labels only) and in the DBnomics mirror. Sex codes run men=lower, women=higher (e.g. 164 M / 327 W for 25-34; 190 M / 347 W for 55-64).
  - example: `POST https://api.bls.gov/publicAPI/v1/timeseries/data/ body {"seriesid":["LNS11300164","LNS11300327",...],"startyear":"2024","endyear":"2026"}. Metadata page: https://data.bls.gov/timeseries/LNU01300164`
- **EPOP 20-24: LNS12300037 (M) / LNS12300038 (W); 25-34: LNS12300164 (M) / LNS12300327 (W); 25-54: LNS12300061 (M) / LNS12300062 (W); 55-64 NSA: LNU02300190 (M) / LNU02300347 (W); 60-64 NSA: LNU02300197 (M) / LNU02300352 (W); employment levels LNS12000036 (20-24), LNS12000060 (25-54)** (BLS CPS (LN) via BLS public API v1) — Employment-population ratio and employment level by sex and age. Verified.
  - breakdowns: sex M/W (totals: replace the sex digits, e.g. LNS12300089, LNS12300060, LNU02300095); ages 20-24, 25-34, 25-54, 55-64, 60-64
  - countries: USA only
  - years: 1948-01 to 2026-09 (60-64 EPOP from 1994-01; 2025-10 missing)
  - notes: P5 (20-24 relative to 25-54) can be built from LNS12300036 / LNS12300060 or from the level series.
  - example: `POST https://api.bls.gov/publicAPI/v1/timeseries/data/ (call 1 and call 3 of this session)`
- **LNU00022968 (pop 20-24 enrolled), LNU00023020 (pop 20-24 not enrolled), LNU01023020 (labor force 20-24 not enrolled), LNU01323020 (LFPR 20-24 not enrolled), LNU02023020 (employed 20-24 not enrolled), LNU01322968 (LFPR 20-24 enrolled). By sex, only for 16-24: LNU00022979 / LNU00022985 (enrolled M/W), LNU00023048 / LNU00023059 (not enrolled M/W), LNU01323048 / LNU01323059 (LFPR not enrolled M/W)** (BLS CPS (LN) via BLS public API v1) — School enrolment status of youth and their labour force status (monthly, NSA). Verified.
  - breakdowns: activity: enrolled / not enrolled (also high school vs college for 16-24: LNU00022990, LNU00022996); ages 16-19, 16-24, 20-24; sex only at 16-24
  - countries: USA only
  - years: 1985-01 to 2026-09 monthly NSA (2025-10 missing)
  - notes: NEET-type count for 20-24 = population not enrolled minus labor force not enrolled (LNU00023020 - LNU01023020). There is no direct 'NILF and not enrolled' LN series; the DBnomics query found none.
  - example: `POST https://api.bls.gov/publicAPI/v1/timeseries/data/ (call 2)`
- **LNU05027036 (NILF 16-24, want a job now), LNU05027040 (NILF 16-24, do not want a job now), LNU05027037 / LNU05027041 (same for 25-54); NILF levels LNU05000036/37/38 (20-24 T/M/W), LNU05000089/164/327 (25-34 T/M/W); reasons not in LF for 16-24 / 25-54: LNU05027046/47 (did not search in past year) through LNU05027696/97 (rnlf codes 60-69: discouraged, family responsibilities, in school, ill health, other)** (BLS CPS (LN) via BLS public API v1) — Not in labor force by job desire, reason, sex and age. Verified.
  - breakdowns: job desire want/don't want; reason codes; ages 16-24, 20-24, 25-34, 25-54; sex for the level series
  - countries: USA only
  - years: Job desire and reasons: 1994-01 to 2026-09. Levels by age and sex: 1976-06 to 2026-09 (NSA)
  - notes: The reason-code series were seen only in the DBnomics mirror (to 2025-01) and were not pulled through the BLS API. Codes in the 'serves P4' set that the API confirmed: LNU05027036, LNU05027040, LNU05027037, LNU05027041 and the LNU05000xxx levels.
  - example: `POST https://api.bls.gov/publicAPI/v1/timeseries/data/ (calls 2 and 3)`
- **LNS14000036 (unemployment rate 20-24), LNS14024887 (16-24)** (BLS CPS (LN) via BLS public API v1) — Youth unemployment rate (SA). Verified.
  - breakdowns: ages 16-24, 20-24 (by sex: LNS14000037/38, LNS14024885/86 by the same pattern; not separately verified)
  - countries: USA only
  - years: 1948-01 to 2026-09
  - notes: Control variable for P2 and the driver for P8.
  - example: `POST https://api.bls.gov/publicAPI/v1/timeseries/data/ (call 2)`
- **CUSR0000SEHA (rent of primary residence, US city average, SA), CUUR0000SEHA (NSA), CUSR0000SEHC (owners' equivalent rent, SA); regional/metro: CUUR0100SEHA (Northeast), CUURS12ASEHA (New York metro), CUURS49ASEHA (Los Angeles metro)** (BLS CPI (CU) via BLS public API v1) — CPI rent of primary residence and owners' equivalent rent. Verified.
  - breakdowns: US city average; Census regions (CUUR0100/0200/0300/0400SEHA pattern); about 20 metro areas (CUURSxxxSEHA pattern)
  - countries: USA (national, regions, metros)
  - years: CUUR0000SEHA 1914 to 2026-08; CUSR0000SEHA 1981 to 2026-08; CUSR0000SEHC 1983 to 2026-08; Northeast 1977-; NY and LA metros 1914- (metro series are partly bimonthly/semiannual). 2025-10 missing
  - notes: Numerator for q = r/p. A goods denominator (e.g. CPI commodities CUSR0000SAC) was not checked. CPIAUCSL/CPIAUCNS are already cached. Metro rent series could support a within-US panel.
  - example: `POST https://api.bls.gov/publicAPI/v1/timeseries/data/ (calls 1-2); https://data.bls.gov/timeseries/CUSR0000SEHA?from_year=1913`
- **Median usual weekly earnings, full-time wage and salary workers, current dollars: LEU0252887100 / LEU0252887300 / LEU0252887500 (20-24 T/M/W); LEU0252888500 / LEU0252888700 / LEU0252888900 (25-34 T/M/W); LEU0252887900 / 888100 / 888300 (25-54 T/M/W); LEU0252890900 / 891100 / 891300 (55-64 T/M/W); LEU0252886300 / 882100 / 883000 (16-24 T/M/W); LEU0252881500 (all 16+)** (BLS CPS earnings (LE) via BLS public API v1) — Median usual weekly earnings by age and sex (quarterly, NSA). Verified.
  - breakdowns: sex T/M/W; ages 16-24, 20-24, 25-34, 25-54, 55-64; full-time (lfst 25) and part-time (lfst 26, LEU0262xxxxxx, mostly annual from 2012). The LE dataset also has a 'fips' state dimension (state codes not explored)
  - countries: USA only
  - years: Age-by-sex series: 2000Q1 to 2026Q2. LEU0252881500 (all workers): 1979 to 2026Q2
  - notes: Gives P2's 'rent relative to the young's wage' as CUUR0000SEHA / LEU0252888500. The age bands start in 2000, not 1979.
  - example: `POST https://api.bls.gov/publicAPI/v1/timeseries/data/ (call 2); https://data.bls.gov/timeseries/LEU0252888500?from_year=1913`
- **Table AD-1 (ad1.xls)** (US Census Bureau, CPS ASEC historical families tables) — Young adults 18-34 living at home: 1960 to present. Verified.
  - breakdowns: sex M/W; ages 18-24 and 25-34; total and 'child of householder' count plus percent
  - countries: USA only
  - years: CPS ASEC annual 1983-2025 (1981-1982 marked N), plus decennial Census 1960, 1970, 1980. Break flags: 2011r, 2014s, 2021r, 2025t
  - notes: Released Dec 2025. Dormitory students are counted as living in the parental home (CPS convention, per table note). Saved to scratchpad scout_us/data/ad1.xls (structure read; values not looked at).
  - example: `https://www2.census.gov/programs-surveys/demo/tables/families/time-series/adults/ad1.xls`
- **Table AD-3 (ad3-25-34.xls; also ad3-18-24.xls, ad3-35-64.xls, ad3-65-74.xls, ad3-75andover.xls, ad3.xls, ad2.xls, uc1.xls in the same folder)** (US Census Bureau, CPS ASEC historical families tables) — Living arrangements of adults 25-34 (child of householder, alone, with spouse, with partner, other relatives, nonrelatives). Verified.
  - breakdowns: sex M/W; one age band per file
  - countries: USA only
  - years: 1967-2023 annual (56 year rows; 2014s and 2021r flags); released Nov 2024
  - notes: Longer coresidence series than AD-1, but it ends in 2023. Only the 25-34 file was opened.
  - example: `https://www2.census.gov/programs-surveys/demo/tables/families/time-series/adults/ad3-25-34.xls`
- **HVS historical Table 19 (histtab19.xlsx)** (US Census Bureau, Housing Vacancies and Homeownership (CPS/HVS)) — Homeownership rates by age of householder. Verified.
  - breakdowns: age of householder: US, under 35, 35-44, 45-54, 55-64, 65+; no sex breakdown
  - countries: USA only
  - years: Quarterly 1994Q1-2026Q2 (2002 revision flag)
  - notes: Tenure split for P1 (young = net short, 55-64 = net long), national level only.
  - example: `https://www.census.gov/housing/hvs/data/histtab19.xlsx`
- **Table A-2 (tablea-2.xlsx / tablea-2.csv); siblings tablea-1..7 and hst_enroll01..07** (US Census Bureau, CPS October school enrollment historical tables) — Percentage of the population 3 years and over enrolled in school, by age, sex, race. Verified.
  - breakdowns: sex both/male/female; race groups; ages 18-19, 20-21, 22-24, 25-29, 30-34, 35+
  - countries: USA only
  - years: 1947-2022 annual (76 years). The 22-24 cell is N for about a dozen early years; the 1993r flag marks a revision
  - notes: Ends 2022. For later years use LN enrolment series (1985-2026) or CPS microdata.
  - example: `https://www2.census.gov/programs-surveys/demo/tables/school-enrollment/time-series/cps-historical-time-series/tablea-2.xlsx`
- **B23001 (sex x age x employment status), B09021 (living arrangements of adults by age: 18-34 'child of householder'), B25007 (tenure by age of householder), B25072 (age of householder by rent as % of income), B19049 (median household income by age of householder), B25064 (median gross rent), B14005 (16-19 enrolment x employment by sex), B24010 (sex by occupation), B01001 (sex by age)** (US Census Bureau, ACS 1-year detailed tables (table-based summary files on www2.census.gov; API metadata)) — ACS 1-year state and metro tables for a within-US panel. Verified.
  - breakdowns: B23001 ages 16-19, 20-21, 22-24, 25-29, 30-34, 35-44, 45-54, 55-59, 60-61, 62-64, 65-69, 70-74, 75+ by sex x LF status; B09021 ages 18-34, 35-64, 65+; B25007 householder age 15-24, 25-34, 35-44, 45-54, 55-59, 60-64, 65-74, 75-84, 85+ by owner/renter
  - countries: USA: 50 states + DC + PR (52 state-level rows), 530 metro (CBSA) rows, counties and places in the 2023 B09021 file
  - years: ACS 1-year 2005-2024 excluding 2020 (B09021 only 2015-2024 excl. 2020). Table-based .dat summary files exist for 2021-2024
  - notes: Only B09021 2023 was downloaded. B23001 table-based files for 2021, 2022 and 2024 returned HTTP 200 on HEAD. API data queries return 'Missing Key', so 2005-2020 needs a free Census API key or the older sequence-based summary files (not tested). This is the main route to a state-level split that does not depend on other countries.
  - example: `https://www2.census.gov/programs-surveys/acs/summary_file/2023/table-based-SF/data/1YRData/acsdt1y2023-b09021.dat (downloaded, 8102 rows, header and geo counts read only); metadata: https://api.census.gov/data/2023/acs/acs1/groups/B23001.json`
- **https://www2.census.gov/programs-surveys/cps/datasets/<year>/basic/<mon><yy>pub.csv|zip ; .../<year>/march/asecpub<yy>csv.zip** (US Census Bureau, CPS public-use microdata (basic monthly and ASEC)) — CPS microdata: person-level LF status x age x sex x relationship to householder x housing tenure x school enrolment x state. Not verified.
  - breakdowns: Any (variables such as HETENURE tenure, PERRP relationship, PESCHENR enrolment, PEMLR LF status, state FIPS, occupation). Variable names come from general knowledge, not from opening the files
  - countries: USA, state-identified
  - years: Basic monthly 1994 to Sep 2026 (sep26pub.csv listed); ASEC 'march' folders present from at least 2000 to 2025
  - notes: Directory listings were fetched and checked. No microdata was downloaded. This would allow P1's tenure split to be measured by actual tenure rather than by age proxy.
  - example: `https://www2.census.gov/programs-surveys/cps/datasets/2025/march/asecpub25csv.zip (HEAD 200, about 147 MB, not downloaded)`
- **LNU02032489 (employed, office and admin support occupations, men), LNU02032547 (women), LNU02032518 (men 20+); percent-type by age (pcts 05): LNU0201CB76 (16-19), LNU0201CB85 (20-24), LNU0201CB94 (25-34), LNU0201CBB2 (45-54), LNU0201CBC1 (55-64); men LNU0201CBDF..CC39, women LNU0201CC48..CCA2** (BLS CPS (LN) via BLS public API v1) — Employment in office and administrative support occupations (clerical) by sex and by age. Verified.
  - breakdowns: occupation 4999 (Census 2018 occupation code); sex; ages in the pcts series
  - countries: USA only
  - years: By sex, monthly: 1983-01 to 2025-12 (verified 2016-2025). By age: annual 2023-2025 only. The API returned 'No Data Available' for 2016-2022
  - notes: There is no pre-2023 age split for clerical work in LN, so P5's pre-2023 exposure needs ACS B24010 (states) or ILO ISCO-08 group 4 (cross-country). Occupation codes change in 2020 and 2011.
  - example: `POST https://api.bls.gov/publicAPI/v1/timeseries/data/ (call 3, years 2016-2025)`
- **BLS/ln (67,741 series), BLS/le (11,053 series)** (DBnomics mirror of BLS (code and metadata discovery)) — DBnomics BLS Labor Force Statistics and Weekly & Hourly Earnings mirrors. Verified.
  - breakdowns: Full LN dimension lists (ages, sexs, lfst, activity, rnlf, jdes, mari, chld, occupation, ...), queryable by dimension
  - countries: USA
  - years: Mirror is stale: LN data end 2025-01, LE end 2024Q4 (indexed 2026-03-07 / 2026-01-30)
  - notes: Has no daily quota. Use it to find codes and start years, then pull current data from the BLS API.
  - example: `https://api.db.nomics.world/v22/series/BLS/ln?dimensions={"lfst":["13"],"sexs":["1","2"],"ages":["31"]}&observations=1&limit=1000`
- **CIVPART, LNS11300060 (LFPR 25-54), LNS12300060 (EPOP 25-54), LNS14000060 (unemp 25-54), EMRATIO, UNRATE, CE16OV, CLF16OV, UNEMPLOY, LNS13026638, CSUSHPINSA (Case-Shiller), CPIAUCNS, AHETPI, JTSHIR; pinning/cache: CPIAUCSL, HNOREMV (household real estate market value)** (Already cached on disk (FRED CSVs in paths/cache)) — Cached US aggregates bearing on participation and housing price. Verified.
  - breakdowns: None by sex. Only 25-54 for the LNS*60 series
  - countries: USA
  - years: LN and CIVPART files: 1948-01 to 2026-08 (944 monthly rows); LNS13026638 1994-01 to 2026-08; CSUSHPINSA 1987-01 to 2026-06; CPIAUCNS 1913-01 to 2026-08; AHETPI 1964-01 to 2026-08; CPIAUCSL 1947-01 to 2026-06; HNOREMV 1945Q4 to 2026Q1
  - notes: Nothing cached is split by sex and age. CUSR0000SEHF01 in the cache is CPI electricity, not rent. Only dates and file names were read.
  - example: `C:\Users\s6068C\GitHub\laborformal\paths\cache\LNS11300060.csv`
- **ilo/EMP_2EMP_SEX_OCU_NB_A_<ISO3>[_all].csv (USA, CHN, DEU, ESP, FRA, ITA, NLD, SWE); ilo/EMP_TEMP_SEX_OCU_NB_A_<ISO3>.csv (+ _2006 variants for ESP, SWE, USA); ilo/EAR_EMTA_SEX_OCU_NB_A_<ISO3>.csv; ilo/EMP_TEMP_SEX_ECO/INS_* (about 30 OECD countries); ilo/toc.csv (ILOSTAT catalogue, lists EAP_DWAP_SEX_AGE_RT_A etc.); worldbank/SP.POP.65UP.TO.ZS.json** (Already cached on disk (ILO and World Bank in paths/cache)) — Cached employment by sex x ISCO-08 occupation, and population 65+ share. Verified.
  - breakdowns: sex F/M/T; ISCO-08 major groups (group 4 = clerical support); no age
  - countries: ILO occupation files: 8 countries. EMP_TEMP_SEX_ECO: about 30 countries. World Bank: 264 economies/aggregates
  - years: ILO USA occupation files 2015-2025 (11 years); USA _2006 file 2006-2012; World Bank SP.POP.65UP 2018-2024
  - notes: Only the time, sex and classification columns were read. The ILO toc shows EAP_DWAP_SEX_AGE_RT (LFPR by sex and age) exists on ILOSTAT but is not cached.
  - example: `C:\Users\s6068C\GitHub\laborformal\paths\cache\ilo\EMP_2EMP_SEX_OCU_NB_A_USA_all.csv`

**Not found or not reachable.**
- fred.stlouisfed.org/graph/fredgraph.csv?id=LNS11300060: one retry with a 90s timeout failed after about 81s with ProxyError 'Remote end closed connection without response'. FRED is unreachable from this machine today; the ALFRED/FRED API was skipped as instructed (needs a key).
- download.bls.gov/pub/time.series/ln/ln.series (BLS flat files): HTTP 403. BLS requires a contact e-mail in the User-Agent, which was not sent (privacy rule). DBnomics used instead for the code catalogue.
- www.bls.gov pages (LAUS demographic state tables ex14tables.htm, Geographic Profile /gps/, cpsaat annual tables): HTTP 403 for the scripted User-Agent. data.bls.gov/timeseries/<id> pages DO work.
- Census API data queries (api.census.gov/data/<yr>/acs/acs1?get=...): return a 'Missing Key' HTML page. Metadata (groups/<table>.json) works without a key. 2005-2020 ACS state data need a free key or sequence-based summary files (not tested).
- Seasonally adjusted LFPR/EPOP for 55-64 and 60-64 by sex: do not exist in LN (NSA only). 55+ is SA (LNS11324230/31/32).
- LN employment by age for office and admin support occupations before 2023: the API returned 'No Data Available' for 2016-2022. Annual by-age series start 2023.
- LE median weekly earnings by age x sex before 2000: the age-band series start 2000Q1 (only the all-workers series goes back to 1979).
- Census Table A-2 school enrolment ends 2022; AD-3 ends 2023; HVS Table 19 has no sex breakdown; AD-1 and HVS have no state detail.
- Direct 'NILF and not enrolled' (NEET) LN series for 20-24: none found. Derive as population not enrolled minus labor force not enrolled.
- data.bls.gov/pdq/SurveyOutputServlet all-years form: returned a page without the data table as submitted. Not used.
- IPUMS CPS/ACS extracts: need account registration, not attempted. CPS public-use microdata on www2.census.gov is the no-registration alternative (listed, not downloaded).
- Not checked: CPI goods/commodities denominator for q (e.g. CUSR0000SAC), HUD Fair Market Rents, Zillow ZORI, SSA replacement-rate data (P7), Census population estimates by age (P6).

**Access.** The scout used 3 of the 25 daily BLS API v1 queries. It downloaded 7 files and read only their structure: headers, labels, row and year labels, and missing-value markers. The BLINDING RULE held throughout: no values, levels or trends were printed or examined.

FRED: a single retry with a 90s timeout failed after about 81s with a ProxyError. Treat FRED as down from this machine.

BLS API v1:
- POST https://api.bls.gov/publicAPI/v1/timeseries/data/ with JSON {"seriesid":[up to 25 ids],"startyear":"YYYY","endyear":"YYYY"} and header Content-type: application/json.
- No key; up to 25 series and 10 years per call; 25 calls a day. Each call used here mixed LN, CU and LE series without trouble.
- Responses carry per-observation footnotes. 2025-M10 is a non-numeric placeholder for all CPS and CPI series ('2025 lapse in appropriations'). January 2026 CPS has a population-control revision footnote.
- Raw JSON from the three calls is saved under scratchpad\scout_us\data\blsv1_call1.json, blsv1_call2.json and blsv1_call3.json; values were not inspected.
- To fetch full history within quota, request 10-year windows. About 22 series times 8 windows is about 8 calls for 1948-2026, or about 5 calls for 1976-2026 per 25-series batch.

Without using quota:
- https://data.bls.gov/timeseries/<SERIES>?from_year=1913 returns an HTML page. It has a catalog table (th class="catalog") with series title, age and sex, and a data table whose year row labels give the start year.
- download.bls.gov and www.bls.gov return 403 to the scripted User-Agent.

DBnomics (https://api.db.nomics.world/v22):
- Mirrors BLS/ln and BLS/le with full dimension labels, and can be filtered with ?dimensions=<json>&observations=1.
- No quota, so it is good for finding codes and start years. Its data stop at 2025-01 (LN) and 2024Q4 (LE).

Census:
- www2.census.gov serves directory listings and files without a key: AD tables, HVS, school enrolment tables, ACS table-based summary files for 2021-2024 (one .dat per table, pipe-delimited, all geographies), and CPS microdata.
- www.census.gov/housing/hvs/data/histtab19.xlsx works.
- api.census.gov metadata works, but data needs a key.

Python and files:
- Use truststore.inject_into_ssl() before requests, the venv interpreter with -I, and the given User-Agent.
- Scripts are in C:\Users\s6068C\AppData\Local\Temp\claude\C--Users-s6068C-GitHub-laborformal\57a37d3a-ed63-4c7d-9808-2133339ff86c\scratchpad\scout_us\code\ (fetch.py, blsv1.py, dbn_ln.py, blspage_years.py, xlstruct.py, acsyears.py).
- Downloads are in ...\scout_us\data\ (ad1.xls, ad3-25-34.xls, histtab19.xlsx, tablea-2.xlsx, acsdt1y2023-b09021.dat, dbn_ln_dataset.json, dbn_le_dataset.json, acs_*_vars.json, blsv1_call*.json).
- Nothing was written inside the repository.

Design note for the explore/confirm protocol: the US alone gives one country. ACS state tables (52 units: B23001, B25007, B09021, B25072) and CPS microdata (state-identified, with tenure and relationship to householder) would give a within-US population of states that can be split into explore and confirm halves by seeded draw within Census regions.
