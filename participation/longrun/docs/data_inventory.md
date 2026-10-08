# Long-run data inventory — coverage only (blind scouting, 2026-10-08, after the European look)

Six scouting agents checked sources for 1950-1996 (and to date where series continue) and reported coverage only.

## oecd_hist

**Best long panel.** Participation by sex and age comes from OECD.ELS.SAE DF_LFS_INDIC (LF_RATE, annual, 5-year bands; levels in DF_LFS). Start years: USA 1960; IRL 1961 (only 1961/66/71/75/77/79/81, then annual from 1983); FIN and SWE 1963; AUS 1966; JPN 1968; DEU (presumably West Germany before 1991) and ITA 1970; NLD 1971 (5-year youth bands from 1987); ESP and NOR 1972; PRT 1974; FRA 1975; CAN 1976; KOR 1980; BEL, DNK, GRC and LUX 1983; GBR 1984; ISR 1985; NZL 1986; CRI 1987; TUR 1988; EST 1990; CHE, ISL and MEX 1991; HUN and POL 1992; CZE 1993; AUT and SVK 1994; CHL 1996; LVA, LTU and SVN 2000; COL 2001. That is 8 countries by 1970, 13 by 1975, 21 by 1985, 25 by 1990 and 34 by 1996. Two sources reach further back: DF_IALFS_INDIC gives the USA from 1955 (sex x 15-24/25-54/55-64) and Japan from 1968 by age; ALFS DF_SUMTAB labour force by sex (15+ only) divided by DF_POP_HIST population (1950-2025 for all 38) gives 15+ participation by sex from 1955-56 for about 10 countries, but no age detail.

Rents relative to goods come from OECD.ECO.MPD DF_HOUSE_PRICES (RPI, annual or quarterly) over a goods or all-items CPI from OECD.SDD.TPS DF_PRICES_ALL. RPI start years: NZL 1956; CAN, FIN, IRL, PRT and CHE 1959; DEU, ITA, NLD and USA 1960; ESP 1961; GBR 1962; SWE 1963; AUT 1966; DNK 1967; FRA, ISR and JPN 1970; AUS 1973; BEL 1977; NOR 1979; MEX 1980; TUR 1982; KOR 1985; GRC 1989; CHL 1990; ISL and LTU 1993; CZE 1994; LVA, LUX, POL, SVK and CRI 1995; HUN 1996; EST 1998; COL 1999; SVN 2000. That is 10 countries by 1960, 18 by 1970, 22 by 1980 and 35 by 1996.

A true goods CPI (GD) is long only for PRT (1948), CAN (1961), JPN (1970) and AUS (1975). Before about 1985, the denominator has to be all-items CPI (1955 for 17 countries, plus CAN, NZL and AUS earlier) or food CPI CP01 (1955 for FIN, DEU, JPN, LUX, SWE, CHE and USA; 1957-61 for ITA, AUT, GRC, ESP, GBR, ISL, NZL, NLD and CAN). National-accounts deflators (T501 CP041 rentals over T117 goods) are an alternative from 1959 for FRA, 1966 for DNK, 1970 for USA, 1975 for FIN and 1981 for CAN.

The joint panel (participation by sex x age, RPI and CPI) starts at: USA 1960; FIN and SWE 1963; JPN, DEU and ITA 1970; NLD 1971; ESP 1972; AUS 1973; PRT 1974; FRA 1975; CAN 1976; NOR 1979; BEL and DNK 1983; GBR 1984; KOR and ISR 1985; NZL 1986; TUR 1988; GRC 1989; MEX and CHE 1991; ISL 1993; CZE and AUT 1994; LUX, POL, SVK and CRI 1995; HUN and CHL 1996. IRL is continuous only from 1983. That is 12 countries by 1975 and 19 by 1985. The non-European holdout inside this panel before 1997 is USA from 1960, JPN from 1970, AUS from 1973, CAN from 1976, KOR and ISR from 1985, NZL from 1986, MEX from 1991, and CRI and CHL from 1995-96. Nothing before 1960 exists by age except the US quarterly series from 1955.

- **https://sdmx.oecd.org/public/rest/data/OECD.ELS.SAE,DSD_LFS@DF_LFS_INDIC,1.1/{REF_AREA}.LF_RATE..{F|M|_T}.{AGE}.  (key = REF_AREA.MEASURE.UNIT_MEASURE.SEX.AGE.LABOUR_FORCE_STATUS; MEASURE LF_RATE / UNE_RATE / EMP_RATIO)** (OECD SDMX (OECD.ELS.SAE)) — Employment and unemployment by five-year age group and sex - indicators (participation, unemployment and employment rates). Verified. Machine-readable.
  - breakdowns: Sex F/M/_T x 40 age codes: 5-year bands 15-19 ... 80-84, plus 15-24, 15-29, 15-64, 25-54, 55-64, 20-64, 65+, 70+, total. LF_RATE (% of population in the subgroup), UNE_RATE (% of labour force), EMP_RATIO. Start years per country (women, 15-19/20-24/25-54; men the same): USA 1960, IRL 1961 (sparse, see caveats), FIN 1963, SWE 1963, AUS 1966 (25-29 from 1978), JPN 1968, DEU 1970, ITA 1970, NLD 1971 (15-24/25-54/55-64; the 5-year youth bands 15-19, 20-24 and 25-29 only from 1987), ESP 1972, NOR 1972, PRT 1974, FRA 1975, CAN 1976, KOR 1980, BEL 1983, DNK 1983, GRC 1983, LUX 1983, GBR 1984, ISR 1985, NZL 1986, CRI 1987, TUR 1988, EST 1990, CHE 1991, ISL 1991, MEX 1991, HUN 1992, POL 1992, CZE 1993, AUT 1994, SVK 1994, CHL 1996, LVA 2000, LTU 2000, SVN 2000, COL 2001. The 65-69 band often starts later: BEL, DNK, GRC, LUX 2000; DEU 1999; JPN 2002; ESP 1995; ITA 1993; CZE 2002. UNE_RATE by age has the same start years, except that some 20-24 cells start later: FIN 1964, SWE 1966, PRT 1975, NLD 1987, ISL 1992, LUX 1995.
  - countries: All OECD-38, plus DEU_F (former Federal Republic of Germany, 1970-1998) and about 20 non-members and aggregates
  - years: 1960-2025 (country starts listed in breakdowns)
  - caveats: IRL before 1983 has only the years 1961, 1966, 1971, 1975, 1977, 1979 and 1981. COL has no 2006. NLD 65+ is missing 1978 and 1980-86. OBS_STATUS break flags appear only for AUS (1985, 2000). Per the LFS sources notes: AUS before 1978 uses August only. FRA before 2003 uses March. NLD up to 1986 uses 1 January. In DEU before 1991, the labour force and population figures are averages of monthly estimates and unemployment is registered unemployment. The DEU series before 1991 is presumably West Germany (DEU_F is published separately). HUN up to 1994: '55-64' means 55-74 and the total means 15-74. MEX was biennial in 1991-95. PRT was bi-annual before 1983. The lower age limit is 16, not 15, in USA, GBR, ESP, ISL and NOR (NOR later moved from 16 to 15), so the '15-19' and '15-24' bands there start at 16. The LFS notes list further breaks with years: AUS 1985/86, BEL 1991/92, DEU 1983/84 and 1990/91, ITA 1970, 1982 and 1992/93, NLD 1986/87, 1991/92 and 1995/96, NOR 1974/75, 1979/80, 1985/86, 1987/88 and 1995/96, PRT 1982/83 and 1991/92, SWE 1986/87 and 1993/94, TUR 1991/92, FIN 1969/70, 1988/89 and 1995/96, KOR 1980 and 1988, DNK 1993/94, ESP 1995/96. The notes do not list the 1994 US CPS redesign.
- **https://sdmx.oecd.org/public/rest/data/OECD.ELS.SAE,DSD_LFS@DF_LFS,1.1/{REF_AREA}.POP.PS.{SEX}.{AGE}.{POP|LF|EMP|UNE}** (OECD SDMX (OECD.ELS.SAE)) — Employment and unemployment by five-year age group and sex - levels (population, labour force, employment, unemployment in persons). Verified. Machine-readable.
  - breakdowns: Sex x the same 40 age codes x labour force status (POP, LF, EMP, UNE), in persons. These are the levels behind DF_LFS_INDIC, so participation can be rebuilt as LF/POP.
  - countries: OECD-38 plus others (59 areas)
  - years: 1960-2025. Per-country starts are identical to DF_LFS_INDIC (checked for women 20-24: USA 1960 ... COL 2001)
  - caveats: Same as DF_LFS_INDIC. The population here is the LFS survey population, not the mid-year population.
- **https://sdmx.oecd.org/public/rest/data/OECD.SDD.TPS,DSD_LFS@DF_IALFS_INDIC,1.0/{REF_AREA}.{LF_WAP|UNE_LF}....{SEX}.{Y15T24|Y25T54|Y55T64|Y15T64|Y_GE15}._Z.{A|Q|M}  (key = REF_AREA.MEASURE.UNIT_MEASURE.TRANSFORMATION.ADJUSTMENT.SEX.AGE.ACTIVITY.FREQ). Single-measure flows: DF_IALFS_LF_WAP_Q, DF_IALFS_UNE_M, DF_IALFS_LF_Q, DF_IALFS_WAP_Q** (OECD SDMX (OECD.SDD.TPS) - infra-annual labour statistics (former MEI labour)) — Infra-annual labour statistics: participation rate (LF_WAP), unemployment rate (UNE_LF), levels. Verified. Machine-readable.
  - breakdowns: Sex x broad age (15-24, 25-54, 55-64, 15-64, 15+, 15-74, 25+). Seasonally adjusted (Y) and unadjusted (N). Annual participation by age (women) starts: USA 1955, JPN 1968 (15+ from 1955), CAN 1976, AUS 1979 (quarterly 1978), NZL 1986, GBR 15-64 and 15+ from 1971 (quarterly), 15-24 from 1992/93 and 25-54 from 1999/2000, ISR 1995. Most European countries start in 1998-2005. CHL 15+ starts 1986 and its age bands 2005. Monthly series by age exist only for USA (1955), JPN (1968), CAN (1976), AUS (1978), KOR (1999), CHL (2005), COL (2007), CRI (2010) and ISR (2012). Annual unemployment for 15+ starts earlier for some countries: JPN 1953, CAN 1956, DEU 1962, NZL 1965, AUT 1969.
  - countries: OECD-38 (all present), plus BRA, BGR, HRV, IDN, ROU, RUS, ZAF and aggregates
  - years: 1953/1955 to 2026
  - caveats: This is the longest OECD source for US participation by sex and broad age (from 1955) and for Japan (from 1968). Apart from USA, JPN, CAN, AUS, NZL and GBR, there is nothing before 1997. Annual values are averages of infra-annual estimates. CHL, CRI and GBR use rolling quarters.
- **https://sdmx.oecd.org/public/rest/data/OECD.SDD.TPS,DSD_ALFS@DF_SUMTAB,1.0/  (dims REF_AREA.MEASURE.UNIT_MEASURE.TRANSFORMATION.SEX.AGE.WORKER_STATUS.ACTIVITY.FREQ; MEASURE LF/EMP/UNE/EMP_WAP/UNE_LF)** (OECD SDMX (OECD.SDD.TPS) - Annual Labour Force Statistics (ALFS)) — Annual labour force survey, summary tables (ALFS). Verified. Machine-readable.
  - breakdowns: Sex F/M/_T, age 15+ only (no age bands). Labour force, employment and unemployment in persons, employment rate, unemployment rate, and employment by broad sector. Women's labour force starts: JPN 1955, GBR 1955, USA 1955, BEL 1956, CAN 1956, FRA 1956, NZL 1956, NOR 1956, ITA 1958, FIN 1959, DNK 1960, PRT 1960, GRC 1961, IRL 1961, DEU 1962, SWE 1963, AUS 1964, AUT 1968, ESP 1970, NLD 1975, CHL 1986, EST 1989, CZE 1990, KOR 1989, ISL 1991, HUN 1992, POL 1992, SVK 1994, ISR 1995, SVN 1996, LVA 1998, LUX 1998, LTU 2005, MEX 2005, CHE 2005, TUR 2006, COL 2007, CRI 2011. The both-sexes total starts earlier for AUT, DEU, IRL, ITA, ESP (1956), POL (1955) and ISL (1964). Unemployment rate by sex mostly starts in 1998-2003; exceptions: JPN 1953, USA 1955, CAN 1956, DEU 1962, NZL 1959-65, AUS 1979, AUT 1969, KOR 1989.
  - countries: OECD-38 plus BRA, BGR, HRV, ROU, RUS and aggregates
  - years: 1953-2025
  - caveats: Pairing it with DF_POP_HIST gives participation by sex for ages 15+ from the mid-1950s, but with no age detail. Gaps: DNK lacks 1961-64, 1966, 1968 and 1980; GRC lacks 1962-76; IRL lacks 1962-65; PRT lacks 1961-73; NOR lacks 1971. Break flags (OBS_STATUS B) before 1997: AUS 1977; AUT 1974 and 1994; CAN 1975; CZE 1992; DEU 1990; DNK 1993; ESP 1976; EST 1996; FIN 1988; FRA 1974 and 1981; GBR 1991; HUN 1993; ITA 1992; KOR 1990; NLD 1982, 1986 and 1991; NZL 1985; PRT 1982 and 1991; SWE 1985, 1986 and 1992. The latest years include OECD estimates (status E).
- **https://sdmx.oecd.org/public/rest/data/OECD.ELS.SAE,DSD_POPULATION@DF_POP_HIST,1.0/{REF_AREA}.POP.PS.{SEX}.{AGE}.  (also DF_POP_ALL, DF_POP_PROJ)** (OECD SDMX (OECD.ELS.SAE)) — Historical population data (mid-year population by sex and 5-year age group, dependency ratios). Verified. Machine-readable.
  - breakdowns: Sex x 5-year bands 0-4 ... 80-84, 85+, plus <15, 15-24, 15-64, 20-64, 65+, total. There is no '15+' code; derive it as total minus under-15.
  - countries: All OECD-38, plus EU27, G20, the World total and 10 non-members
  - years: 1950-2025 for every OECD-38 country, all bands, no gaps (76 years)
  - caveats: The flow description says the data run 'from 1961', but observations start in 1950. The 1950s are presumably model-based estimates (likely UN WPP style); check the linked 'Historical population metadata'. All OBS_STATUS are A. This serves as the denominator for ALFS labour force and as the age-structure control.
- **https://sdmx.oecd.org/public/rest/data/OECD.ECO.MPD,DSD_AN_HOUSE_PRICES@DF_HOUSE_PRICES,1.0/{REF_AREA}.{A|Q}.RPI.IX  (key = REF_AREA.FREQ.MEASURE.UNIT_MEASURE)** (OECD SDMX (OECD.ECO.MPD) - Analytical house prices) — Analytical house prices indicators: RPI rent prices, HPI nominal house prices, RHP real house prices, price-to-rent and price-to-income ratios. Verified. Machine-readable.
  - breakdowns: MEASURE: RPI (rent prices index), HPI, RHP, HPI_RPI, HPI_RPI_AVG, HPI_YDH, HPI_YDH_AVG. Seasonally adjusted, base 2015. Annual RPI start years: NZL 1956; CAN, FIN, IRL, PRT, CHE 1959; DEU, ITA, NLD, USA 1960; ESP 1961; GBR 1962; SWE 1963; AUT 1966; DNK 1967; FRA, ISR, JPN 1970; AUS 1973 (quarterly 1972); BEL 1977; NOR 1979; MEX 1980; TUR 1982; KOR 1985; GRC 1989; CHL 1990; ISL 1993; LTU 1993 (quarterly 1992); CZE 1994; LVA, LUX, POL, SVK, CRI 1995; HUN 1996; EST 1998; COL 1999; SVN 2000. Annual HPI starts: JPN 1960; GBR 1969; AUS, BEL, CAN, DNK, FIN, FRA, DEU, IRL, ITA, NLD, NZL, NOR, SWE, CHE, USA 1970; ESP 1971; KOR 1986; COL, PRT 1988; ISR 1994; GRC 1997; AUT 2000; ISL 2001; CHL 2002; EST, MEX, POL, SVK 2005; LVA, LTU 2006; HUN, LUX, SVN 2007; CZE 2008; TUR 2010; CRI none.
  - countries: All OECD-38 have RPI; 37 have HPI (not CRI); plus about 13 non-members and aggregates
  - years: RPI 1956-2025/26; HPI 1960/1970 to 2026
  - caveats: This is the longest OECD rent series. It covers 10 countries by 1960, 18 by 1970, 22 by 1980 and 35 by 1996. The OECD defines the RHP deflator as the national-accounts private consumption deflator. The flow description calls RPI 'rental prices'; that it is the CPI actual-rentals component is assumed but was not confirmed (the OECD FAQ page returned 503). No break flags (all OBS_STATUS A). Whether DEU before 1991 is West Germany is not stated. Series are seasonally adjusted, even the annual ones.
- **https://sdmx.oecd.org/public/rest/data/OECD.SDD.TPS,DSD_PRICES@DF_PRICES_ALL,1.0/{REF_AREA}.{A|Q|M}.N.CPI.IX.{_T|CP041|GD|CP01|SERV|CP04|...}.N._Z  (key = REF_AREA.FREQ.METHODOLOGY.MEASURE.UNIT_MEASURE.EXPENDITURE.ADJUSTMENT.TRANSFORMATION)** (OECD SDMX (OECD.SDD.TPS) - Consumer prices (former MEI prices)) — Consumer price indices (CPIs, HICPs), COICOP 1999: all items, actual rentals, goods, services, food, housing. Verified. Machine-readable.
  - breakdowns: 29 EXPENDITURE codes, including _T, CP041 (actual rentals), GD (goods), SERV, CP01, CP03, CP04, CP041T043, CP041T043X042 and SERVXCP041_042_0432. National (N) or HICP. All-items annual index starts: CAN 1914, NZL 1915, AUS 1949; 1955 for BEL, FIN, FRA, DEU, GRC, ISL, ITA, JPN, LUX, NOR, PRT, ESP (monthly 1954), SWE, CHE, TUR, GBR and USA; AUT 1958; NLD 1961; KOR 1965; DNK 1967; MEX 1969; CHL, COL, ISR 1970; IRL 1976 (monthly from 1955); CRI 1976; HUN, SVN 1980; POL 1989; CZE, SVK, LVA, LTU 1991; EST 1998. Actual rentals (CP041) starts: PRT 1948, CAN 1949, DNK 1967, FRA 1970, JPN 1970, AUS 1973, ESP 1976, MEX 1980, CHE 1982, BEL 1984, ISR 1985, KOR 1985, GBR 1988, GRC 1989, IRL 1990, LTU 1993, CZE, DEU, LUX, LVA, POL, SVK, CRI 1995, ITA, NLD 1996, AUT 1997, EST 1998, HUN, NZL, SVN 2000, TUR 2005, CHL, COL 2009, FIN, USA 2010 (NOR 1979, SWE 1980, ISL 2002). Goods (GD) starts: PRT 1948, CAN 1961, JPN 1970, AUS 1975, CHE 1983, ISR, KOR 1985, GBR 1988, NZL 1989, FRA 1990, CZE, CRI, LVA 1995, ITA, NLD 1996, AUT, IRL 1997, SVN, LTU 2000, LUX 2005, POL 2006, HUN 2007, CHL, GRC 2009, USA 2010, MEX 2011. There is no GD at all for BEL, COL, DEU, EST, FIN, ISL, NOR, SWE, TUR. Food (CP01) starts: PRT 1948; FIN, DEU, JPN, LUX, SWE, CHE, USA 1955; ITA 1957; AUT 1958; GRC, ESP 1959; GBR, ISL, NZL 1960; NLD 1961; CAN 1961; TUR 1963; DNK 1967; MEX 1969; FRA, ISR 1970; IRL 1976 (monthly 1955); AUS 1977; NOR 1979; HUN 1980; KOR 1985; BEL 1991.
  - countries: All OECD-38, plus non-members and aggregates
  - years: 1914 (CAN) / 1955 (most) to 2026
  - caveats: Growth-rate variants (PA/GY) start one year after the index; they do not extend history. The CP041 and GD indices are short for USA (2010), DEU, ITA and NLD (1995-96). For rents before the mid-1990s, use the analytical house prices RPI instead. A long goods series is missing for most countries, so before about 1985 the goods denominator has to be all-items CPI, food CPI (CP01) or national-accounts goods deflators. Break flags: DNK CP041 1978, GBR all-items 1988. JPN ends in 2020 here; it continues in the COICOP 2018 flow.
- **https://sdmx.oecd.org/public/rest/data/OECD.SDD.TPS,DSD_PRICES_COICOP2018@DF_PRICES_C2018_ALL,1.0/{REF_AREA}.A.N.CPI.IX.{EXP}.N._Z** (OECD SDMX (OECD.SDD.TPS)) — Consumer price indices, COICOP 2018. Verified. Machine-readable.
  - breakdowns: Same structure as DF_PRICES_ALL, with COICOP 2018 codes. In 28 OECD countries it does not extend history beyond DF_PRICES_ALL, except AUS CP01 from 1955 and JPN all-items 1955-2025 (CP041 1970-2025).
  - countries: 28 OECD members. Missing AUT, COL, DEU, ISR, KOR, NZL, POL, SVK, GBR, USA
  - years: 1914-2026
  - caveats: Use it for JPN after 2020 and for AUS food back to 1955.
- **https://sdmx.oecd.org/public/rest/data/OECD.SDD.NAD,DSD_NAMAIN10@DF_TABLE5_T501,1.0/A.{REF_AREA}.S14.S1.P31DC._Z._Z.{CP041|_T|CP01|...}..DR..** (OECD SDMX (OECD.SDD.NAD) - national accounts) — Annual household final consumption expenditure by purpose (COICOP 1999): current prices, volumes, deflators. Verified. Machine-readable.
  - breakdowns: 61 COICOP codes, including CP041 actual rentals. PRICE_BASE V (current), L (volume), DR (deflator). The CP041 deflator starts: AUS 1959, FRA 1959, DNK 1966, USA 1970, FIN 1975, CAN 1981, CRI 1991, MEX 1993, SWE 1993; most EU countries 1995 (DEU 1995, GBR 1995 with no L). CZE, IRL, ISR and NLD have current prices only.
  - countries: 33 OECD members. There is no CP041 for JPN, KOR, NOR, TUR, CHL, COL or NZL; CHE has only the total
  - years: 1959-2025
  - caveats: This is an alternative rent-relative-to-goods measure from deflators, but before 1995 it exists only for AUS, FRA, DNK, USA, FIN, CAN, CRI, MEX and SWE.
- **https://sdmx.oecd.org/public/rest/data/OECD.SDD.NAD,DSD_NAMAIN10@DF_TABLE5_T117,1.0/A.{REF_AREA}.S14.S1.{P311|P312|P313|P314}.....DR..** (OECD SDMX (OECD.SDD.NAD) - national accounts) — Annual household final consumption expenditure by durability (durable, semi-durable, non-durable goods, services). Verified. Machine-readable.
  - breakdowns: TRANSACTION P311 durable, P312 semi-durable, P313 non-durable, P314 services; deflator, current prices, volume. The deflator starts: FRA 1959, DNK 1966, NOR 1970, USA 1970, FIN 1975, CAN 1981, NZL 1987 (no P312), CRI 1991, DEU 1991, MEX 1993, SWE 1993; most others 1995; CHL 1996, COL 2005, TUR 2009.
  - countries: 33 OECD members. Missing AUS, IRL, ISR, JPN, KOR
  - years: 1959-2025
  - caveats: Goods deflators (P311-P313) can stand in for the goods CPI from 1959 to 1981 only in FRA, DNK, NOR, USA, FIN and CAN.
- **https://sdmx.oecd.org/public/rest/data/OECD.ECO.MAD,DSD_EO@DF_EO,1.5/{REF_AREA}.{WSST|WAGE|WRT|UNR|LF|LFPR1574|POP1574|CPI|PCP|ULC|EE|WSSS|ET}.A  (key = REF_AREA.MEASURE.FREQ); vintages DF_EO_114 ... DF_EO_118** (OECD SDMX (OECD.ECO.MAD) - Economic Outlook) — OECD Economic Outlook No 119 (annual and quarterly macro database). Verified. Machine-readable.
  - breakdowns: No sex or age breakdown. LFPR1574 is the participation rate for ages 15-74; also UNR, LF, ET, EE (dependent employment), POP1574, WSST (compensation per employee), WSSS (total compensation), WAGE, WRT (wage rate), ULC, CPI (only for non-euro-area countries), PCP (private consumption deflator). These start in 1960 for BEL, FIN, FRA, ITA, JPN, NLD, SWE, USA, GBR (GBR employment from 1971) and mostly for TUR, NZL, PRT and ESP (ESP UNR/LF from 1977). AUS starts 1964; KOR 1963 (wages 1970); ISL 1964; AUT 1969 (WSST 1976); DNK 1966-69; NOR 1970-72; CHE 1970-75 (wages 1990); CAN 1960, but wages and compensation only from 1981; IRL 1990 (LFPR 1960); LUX 1985; MEX 1991 (WSST 1970); DEU 1991/92; CEE countries and GRC 1990-96; CHL 1986; COL 2001; CRI 2010.
  - countries: OECD-38 plus non-members (65 areas)
  - years: 1960-2027 (includes projections for the last 2 years)
  - caveats: Only unified Germany (from 1991) is covered; there is no West Germany series. The last years are forecasts. Vintages are revised and the definitions are national-accounts-consistent. For euro-area members, CPI is under CPIH, not CPI.
- **https://sdmx.oecd.org/public/rest/data/OECD.SDD.TPS,DSD_EAR@DF_HOU_EAR,1.0/{REF_AREA}.EAR.IX.{Y|N}.{C|_Z}.{S1|S1D}.{A|Q|M}** (OECD SDMX (OECD.SDD.TPS) - hourly earnings (former MEI)) — Hourly earnings (manufacturing; private sector) index. Verified. Machine-readable.
  - breakdowns: Manufacturing (C, total economy S1) or private sector (_Z, S1D). Index only; no sex or age. Annual starts for manufacturing: BEL, CAN, FIN, IRL, ITA, JPN, USA 1955; FRA 1956 (quarterly 1955); DEU 1957; NOR 1959; GBR 1963; NLD 1970; DNK, SWE 1971; MEX 1980; ESP 1981; AUS 1983 (quarterly only); NZL 1989; KOR, SVK 1992; CZE 1993; HUN, ISR, POL 1995; SVN 1998; EST, LTU, LVA 2000; ISL 2005; LUX 2010; CRI 2011. Private sector: USA 1964, JPN 1970, GBR 1990, ISL 1990, KOR 1989, AUT 1996, PRT 1996 and other EU 1994-2000.
  - countries: 33 OECD members. There is no series for CHL, COL, GRC, CHE or TUR, and AUT and PRT have private sector only
  - years: 1955-2026
  - caveats: Break flags: CAN 1990, DNK 1973, FIN 1977, GBR 1969 and 1975, IRL 1976, KOR 2007, POL 1998. FRA has no 2020 annual value. Some series are weekly or monthly earnings, not hourly (per the flow description).
- **https://sdmx.oecd.org/public/rest/data/OECD.SDD.STES,DSD_KEI@DF_KEI,4.0/{REF_AREA}.A.{UNEMP|CP|H_EARN|EMP}.....** (OECD SDMX (OECD.SDD.STES)) — Key short-term economic indicators (headline unemployment rate, CPI, hourly earnings, employment). Verified. Machine-readable.
  - breakdowns: Totals only. UNEMP as % of labour force starts: CAN, JPN, USA 1955; NZL 1956; AUS 1967; BEL, DNK, FRA, GBR, GRC (1999), IRL, ITA, LUX, NLD, PRT, SWE 1983; MEX, ESP 1987; FIN 1988; KOR, NOR 1989; DEU 1991; AUT 1993; SVN, HUN 1996; CZE 1993; POL, EST, LTU, SVK, LVA 1997-99; ISL 2003; TUR 2005; COL 2007; CHE 2010; CRI 2011. EMP (persons) starts 1955-56 for most of Western Europe and North America.
  - countries: OECD-38
  - years: 1914/1955-2025
  - caveats: These are headline compilations drawn from the flows above; they add nothing by age. Before 1983 the European unemployment rate is not available here.
- **https://sdmx.oecd.org/public/rest/data/OECD.ELS.SAE,DSD_EARNINGS@AV_AN_WAGE,1.0/  (also DSD_EARNINGS@AGE_WAGE_GAP, DSD_EARNINGS@DATASET)** (OECD SDMX (OECD.ELS.SAE)) — Average annual wages (full-time-equivalent, national currency and USD PPP). Verified. Machine-readable.
  - breakdowns: Total only, current and constant prices
  - countries: OECD-38
  - years: 1990-2025 (CHL 1996, CZE 1995, CRI 1991, COL 2005; euro countries 1990-1996)
  - caveats: Nothing before 1990.
- **https://sdmx.oecd.org/public/rest/data/OECD.EDU.IMEP,DSD_EAG_LSO_EA@DF_LSO_TRANS,1.0/{REF_AREA}._T.{Y15T19|Y20T24|Y25T29}.._T.POP._Z._T._Z.ED.POP......** (OECD SDMX (OECD.EDU.IMEP) - Education at a Glance) — Transition from school to work: share of age group in education (EDU_STATUS = ED). Verified. Machine-readable.
  - breakdowns: Sex x age 15-19, 20-24, 25-29 x education status x labour force status
  - countries: 37 OECD members (not KOR)
  - years: 1997-2025 at the earliest (AUS, BEL, CAN, CZE, DNK, FRA, DEU, GRC, HUN, MEX, NLD, NOR, POL, PRT, SVK, ESP, SWE, CHE, TUR, USA 1997; others 1998-2013; JPN 2005-14)
  - caveats: Starts in 1997, so it is useless for the pre-1997 backward holdout. CAN, CHL and LTU have many gaps.
- **https://www.oecd.org/content/dam/oecd/en/data/datasets/employability-data/LFSNOTES_SOURCES.pdf** (OECD (PDF metadata)) — Labour Force Statistics in OECD countries: sources, coverage and definitions; Table 6 'breaks in series' (last update 28 Aug 2026). Verified. Not machine-readable.
  - breakdowns: For each country: survey source, survey period (month or averaging), age coverage, and a list of breaks
  - countries: OECD-38
  - years: All years of DF_LFS / DF_LFS_INDIC
  - caveats: PDF, 55 pages, linked from the DF_LFS and DF_LFS_INDIC descriptions. The early-year caveats summarised in the DF_LFS_INDIC entry come from here. Read Table 6 directly before fixing break dummies; the extraction here was automated and approximate.
- **OECD 'Manpower Statistics 1950-1962' (and 1954-1964) and OECD 'Labour Force Statistics 1956-1966' (published 1968), with later decade volumes. Library catalogue records: https://ci.nii.ac.jp/ncid/AA00294676 and https://kutuphane.sbb.gov.tr/vufind/Record/48623/Description; series page https://www.oecd.org/en/publications/oecd-labour-force-statistics_23083387** (OECD print yearbooks (archive)) — Manpower Statistics / Labour Force Statistics yearbooks. Not verified. Not machine-readable.
  - breakdowns: Unverified. Per the catalogue and series descriptions, they contain population, labour force, employment and unemployment, with participation by sex and age bands in later volumes
  - countries: OECD members of the time (about 20 Western countries, JPN, USA, CAN)
  - years: 1950s-1960s onward (catalogues disagree on exact spans)
  - caveats: This is the only OECD route toward 1950-59 participation by age. No digitised full text was found: the old SourceOECD link is subscription-only, and HathiTrust or a depository library would need checking. The figures would have to be keyed by hand from scans.

**Not found or not reachable.**
- Participation by sex x age band before 1955 in any OECD machine-readable flow. Before 1960, by broad age, only the USA has it (DF_IALFS_INDIC from 1955: 15-24, 25-54, 55-64). Before 1970, by 5-year age, only USA (1960), IRL (1961, sparse), FIN and SWE (1963), AUS (1966) and JPN (1968).
- Participation by sex x age before 1983 for BEL, DNK, GRC and LUX; before 1984 for GBR; before 1986 for NZL. For CHE, ISL, MEX (1991), HUN, POL (1992), CZE (1993), AUT, SVK (1994), CHL (1996), LVA, LTU, SVN (2000) and COL (2001) there is nothing before the dates shown.
- A 1950s-1960s participation series by sex x age from the OECD print yearbooks (Manpower Statistics 1950-62, Labour Force Statistics 1956-66): print or PDF only, and no digitised copy was found.
- A long CPI goods aggregate (GD) for most countries. Before 1985 it exists only for PRT (1948), CAN (1961), JPN (1970) and AUS (1975). There is none at all for BEL, COL, DEU, EST, FIN, ISL, NOR, SWE, TUR, and the USA has it only from 2010 in OECD data.
- CPI actual rentals (CP041) in DF_PRICES_ALL before the mid-1990s for USA (2010), DEU (1995), ITA and NLD (1996), GBR (1988). The analytical house prices RPI covers these from 1960-62.
- Any rent index before 1993 for CZE, LVA, LUX, POL, SVK, CRI, HUN, EST, COL and SVN (RPI starts 1993-2000).
- A West Germany series in the Economic Outlook, which covers unified Germany only, from 1991.
- Legacy MEI CPI component series (e.g. CPGRGO01 goods, CPGRHO housing) and the old stats.oecd.org MEI_PRICES dataset. They are not present in the new SDMX API, and FRED mirrors were not checked.
- Coresidence (young adults living with parents) or household-composition series before the 2000s. The OECD flows (EGDNA socio-demographic, Affordable Housing Database) are recent only.
- Housing tenure series in OECD SDMX before the 2000s.
- Schooling and enrolment by age before 1997 in OECD SDMX (EAG DF_LSO_TRANS starts 1997, UOE enrolment rates about 2013).
- Average annual wages (AV_AN_WAGE) before 1990.
- Unemployment rates by age before the start years of DF_LFS_INDIC, which are the same as for participation.
- The national-accounts CP041 rentals deflator for JPN, KOR, NOR, TUR, CHL, COL, NZL and CHE; goods deflators by durability for AUS, IRL, ISR, JPN and KOR.

**Access.** The SDMX REST base is https://sdmx.oecd.org/public/rest/. Data calls take the form data/{agency},{flow},{version}/{key}?dimensionAtObservation=AllDimensions with the header Accept: application/vnd.sdmx.data+csv; charset=utf-8. Keys must contain exactly one slot per dimension; a wrong count returns 403 'Not enough key values'. Multiple codes in one slot are joined with '+'. Structure, codelists and the actual content constraint come from dataflow/{agency}/{flow}/{version}?references=all; that response includes the time range and the codes actually present.

All calls in this session worked through the corporate proxy with truststore and the given User-Agent. There were no 429 responses. The largest single pull was about 35 MB (DF_IALFS_INDIC, OECD-38, two measures, annual and quarterly).

Blinding: every data pull went through cov.py, which drops OBS_VALUE straight after parsing. Only keys, years, counts and OBS_STATUS flags were written or printed. Files (values-free) are in C:\Users\s6068C\AppData\Local\Temp\claude\C--Users-s6068C-GitHub-laborformal\57a37d3a-ed63-4c7d-9808-2133339ff86c\scratchpad\lr_oecd\data\cov_*.csv, together with dataflows.tsv, struct_*.xml and pdf\LFSNOTES_SOURCES.pdf (plus .txt). Scripts are in ...\lr_oecd\code\: common.py, cov.py, covsum.py, gaps.py, dsdinfo.py, o38.py, flows.py and getpdf.py.

Blinding disclosure: two WebSearch result summaries (not data fetches) showed this scout a handful of values without being asked. They were a few US participation rates for 15-64 and 25-54 in 1959-1970 (FRED pages mirroring the OECD infra-annual series), one 1959 US 16-24 participation by sex (an EPI chart), and a few Austrian RPI index levels (DBnomics). None of them were recorded or used here, and none are reported. The researcher may want to log that the scout, not the researcher, saw them. After that, web searching was stopped.

The old OECD.Stat site is retired; the human-facing Data Explorer is https://data-explorer.oecd.org.

Membership note: the 'non-European OECD' holdout set in these flows is USA, CAN, AUS, NZL, JPN, KOR, ISR, MEX, CHL, COL and CRI. TUR may already have been in the Eurostat set.

## ilo_un_hist

**Best long panel.** Participation by sex and age: the best source in this family is ILOSTAT EAP_DWAP_SEX_AGE_RT_A, annual, in 5-year bands from 15-19 to 65+. It forms a two-tier panel.

Tier 1 is continuous annual labour force survey data:
- USA from 1948 (CPS; quarterly and monthly also from 1948).
- JPN from 1968.
- CAN from 1976 (monthly from 1976).
- ESP from 1977; ITA from 1977 (missing 1981).
- AUS from 1979 (monthly from 1978); FRA from 1979; FIN from 1979 (missing 1983); PRT from 1978 (missing 1983).
- NOR, KOR and CHL from 1980; GRC from 1981; AUT from 1982.
- BEL, DEU, GBR, LUX and IRL from 1983; DNK from 1983, with scattered years 1974-81.
- NZL from 1986; NLD from 1987 (scattered 1977-85); SWE from 1989 (scattered 1975-87).
- CHE and MEX from 1991; HUN and POL from 1992; CZE, SVK and SVN from 1993.

Tier 2 is roughly decennial census benchmarks before each country's survey begins:
- BEL and LUX from 1947; DNK, POL and PRT from 1950; GRC and COL from 1951; CHL from 1952; TUR from 1955 (every 5 years).
- HUN, CHE, KOR, NOR, ISL and NLD from 1960; AUS, AUT, ITA, IRL and CAN from 1961; FRA from 1962; SWE in 1965; GBR from 1966.

So a balanced annual panel by sex and 5-year age reaches back only to about 1983 for about 20 OECD countries and about 1979 for about 10. Before that, the US (from 1948), Japan (from 1968), and censuses around 1950/1960/1970 are all there is. All series continue to 2025.

The only harmonised 1950-based source, ILO EAPEP 4th edition (decennial 1950-2010), is print or diskette only.

Population by single age from 1950: UN WPP2024 covers all OECD members annually, 1950-2023.

Rents relative to goods: this family has no usable long panel.
- ILOSTAT CPI_XCPI_COI_RT_A has no rent sub-index.
- COICOP CP04 (housing and utilities) starts PRT 1948, AUS 1973, NOR 1979, SWE 1980, CHE and IRL 1983, ISR and KOR 1985, GBR 1988, FRA 1990, DEU 1991, ITA 1996, and later elsewhere (USA 2010, CAN 2015).
- Total CPI and food (CP01) start around 1955 for most OECD countries; the total CPI starts in 1940 for CAN and NZL.

Rent-to-goods ratios before about 1985 need another source family.

- **EAP_DWAP_SEX_AGE_RT_A; https://rplumber.ilo.org/data/indicator/?id=EAP_DWAP_SEX_AGE_RT_A&ref_area=USA+JPN&timefrom=1940&format=.csv (all countries if ref_area omitted; ~39 MB)** (ILOSTAT (ILO), LFS database) — Labour force participation rate by sex and age (%), annual. rep_var is 'previous ILO definition - ICLS13'. Verified. Machine-readable.
  - breakdowns: Sex (T/M/F) by age. Four age schemes: 5-year bands (15-19 ... 60-64, 65+), 10-year bands, an aggregate (15-24, 25-54, 55-64, 65+) and youth/adult (15-24, 25+, 15-64). The 'source' column gives the source type: AA = population census, BA = labour force survey (LFS), BX = other household survey, EA = official estimate. Notes columns give minimum and maximum age, armed-forces coverage and break flags.
  - countries: 316 areas in all, 204 with any year up to 1996. Countries with any data by 1950: 19; by 1955: 29; by 1960: 90; by 1970: 144; by 1990: 190. All 38 OECD members are covered. Annual LFS years by country (female 20-24 band): USA 1948-; JPN 1968-; CAN 1976-; ESP 1977-; ITA 1977-80 and 1982-; AUS and FRA 1979-; FIN 1979-82 and 1984-; PRT 1978-82 and 1984-; NOR, KOR, CHL 1980-; GRC 1981-; AUT 1982-; BEL, DEU, LUX, GBR 1983-; IRL 1977 then 1983-; DNK 1974, 1976-79, 1981, then 1983-; NLD 1977, 1979, 1983, 1985, then 1987-; SWE 1975-76, 1982-85, 1987, then 1989-; NZL 1986-; MEX 1991-; CHE 1991-; HUN 1992-; POL 1992-; CZE, SVK, SVN 1993-; EST 1990-; LVA, LTU 1996-; TUR 1988-90 then 2000-; ISR 1990-; CRI 1990-; COL 2001-. Census points before the LFS starts: BEL 1947, 1961, 1970, 1981; LUX 1947, 1960, 1966, 1970, 1981; DNK 1950, 1960, 1965, 1970; POL 1950, 1960, 1970, 1978, 1988; PRT 1950, 1960, 1970; GRC 1951, 1961, 1971; COL 1951, 1964, 1973; CHL 1952, 1960, 1970; TUR every 5 years 1955-85; KOR 1960, 1966, 1970, 1975; HUN and CHE 1960, 1970, 1980, 1990; NOR 1960, 1970; ISL 1960; NLD 1960; FIN 1960, 1970, 1976; AUS 1961, 1966, 1971, 1976; AUT, ITA 1961, 1971, 1981; IRL 1961, 1966, 1971, 1981; CAN 1961, 1971; FRA 1962, 1968, 1975; GBR 1966, 1971, 1981; SWE 1965; ESP 1970; MEX 1970, 1980, 1990. Official-estimate points: ISL 1975-83, NLD 1980-86, MEX 1978-88. DEU and JPN have no census points; USA has none because it is CPS-only from 1948. The series runs to 2025 for every OECD member; ISR's 5-year bands end in 2011.
  - years: 1946-2027 (annual; a few projected years at the end)
  - caveats: Before about 1980, outside the US and Japan, the series is mostly decennial census benchmarks (source AA), not an annual series. Census activity concepts (usual or current activity) and age floors differ from the LFS, so every census-to-LFS join is a level break. The minimum age is 16 in the US 1948-96, GBR 1981-96, ESP 1977-85 and SWE 1975-89; it is 14 in ITA 1971-82 and 10 in ITA 1961. SWE 1987-89 has a maximum age of 64. Armed forces are included or excluded depending on country and period. Flagged breaks: CAN 1976, FRA 1983, USA 1994, CHE 1991, SVN 1996. Source switches: ITA national LFS to EU-LFS in 1983; ESP national LFS to EU-LFS in 1986; PRT in 1986; GBR EU-LFS to national LFS in 1993. CAN 1961-71 excludes some areas and the indigenous population. Some pre-1997 rows come from the OECD repository and ILO microdata processing. DEU pre-1991 territory is not stated in the notes; check before use. The ILO updates this indicator continuously (last update 02/10/2026), so freeze a hashed snapshot before pre-registering.
- **EAP_DWAP_SEX_AGE_RT_Q and EAP_DWAP_SEX_AGE_RT_M; https://rplumber.ilo.org/data/indicator/?id=EAP_DWAP_SEX_AGE_RT_Q&ref_area=USA+JPN+CAN+AUS&timefrom=1940&timeto=1996&format=.csv. Seasonally adjusted versions: EAP_DWA1_SEX_AGE_RT_Q and _M, from 1955.** (ILOSTAT (ILO), LFS database) — Labour force participation rate by sex and age, quarterly and monthly. Verified. Machine-readable.
  - breakdowns: Sex by age. Quarterly data come in all four age schemes, including 5-year bands. Monthly data come in 10-year, aggregate and youth/adult bands only, with no 5-year bands.
  - countries: Quarterly data before 1997 with more than one observation a year: USA from 1948, JPN from 1968, CAN from 1976, AUS from 1978, NZL from 1986, GBR from 1983, CZE from 1993. EU countries from 1983 have one observation a year only. Monthly data before 1997: USA 1948, JPN 1968, CAN 1976, AUS 1978, NZL 1986 (quarterly-spaced months).
  - years: 1948-2026
  - caveats: Same source codes and breaks as the annual series. For most of Europe before 1997, the 'quarterly' series is really the single spring EU-LFS observation.
- **POP_XWAP_SEX_AGE_NB_A (working-age population), EAP_TEAP_SEX_AGE_NB_A (labour force), EIP_DWAP_SEX_AGE_RT_A (inactivity rate). URL pattern: https://rplumber.ilo.org/data/indicator/?id=<ID>&timefrom=1940&format=.csv** (ILOSTAT (ILO), LFS database) — Working-age population, labour force and inactivity by sex and age (levels in thousands; inactivity in %). Verified. Machine-readable.
  - breakdowns: Sex by age, the same four age schemes as the participation rate
  - countries: Per the TOC: 320 areas for population, 316 for labour force. Population-by-age coverage for OECD mirrors the participation series, for example USA 1948-, DNK 1950-, BEL and LUX 1947-, POL and PRT 1950-.
  - years: 1946-2030
  - caveats: These are the denominators and numerators behind the participation rate, so they share its source codes and breaks. They are not a continuous population series; use UN WPP for that.
- **UNE_DEAP_SEX_AGE_RT_A (also _Q and _M; the TUNE series gives levels)** (ILOSTAT (ILO), LFS database) — Unemployment rate by sex and age. Verified. Machine-readable.
  - breakdowns: Sex by age, the four age schemes
  - countries: 312 areas. OECD start years (5-year band): USA 1948, JPN 1968, SWE 1975, CAN 1976, ESP and NLD 1977, ITA, PRT 1978, AUS and FIN 1979, GRC 1981, AUT and NOR 1982, EU-LFS countries 1983, NZL 1986, KOR 1986, TUR 1988, CHE, CRI, EST and ISR 1990, MEX 1991, HUN and POL 1992. All run to 2025.
  - years: 1947-2027
  - caveats: Mostly LFS-based, so it is thinner before the 1980s than the participation series, which has census points. The breaks are the same as for participation.
- **EAP_3WAP_SEX_AGE_STU_RT_A (participation by school attendance); EIP_3EET_SEX_AGE_RT_A (NEET rate); POP_3WAP_SEX_AGE_STU_NB_A (population by school attendance)** (ILOSTAT (ILO), YOUTHSTATS database) — Youth labour force participation rate by sex, age and school attendance status; NEET rate. Verified. Machine-readable.
  - breakdowns: Sex; youth bands 15-19, 20-24, 25-29 and 15-29; school attendance (attending, not attending, not stated)
  - countries: 175 areas. Before 1997 among OECD: BEL, DNK, FRA, GBR, IRL, LUX 1983-; ITA 1983-; NLD 1983-; DEU 1983-; GRC 1987-; ESP, PRT 1986-; CAN 1976-; CHL 1990-; CHE 1991-; USA 1994-; AUT, ISL, SWE 1995-; FIN, HUN, SVN 1996-. Absent for JPN, ISR and NZL; most others start after 2000.
  - years: 1970-2025 (OECD data before 1983 exist only for CAN)
  - caveats: Comes from ILO microdata processing (EU-LFS and national LFS), so the definition of school attendance varies by survey.
- **EAP_2WAP_SEX_AGE_RT_A; also EAP_2EAP_SEX_AGE_NB_A, EIP_2WAP_SEX_AGE_RT_A, POP_2WAP_SEX_AGE_NB_A (UN WPP July 2024 population)** (ILOSTAT (ILO), ILOEST modelled estimates (Nov. 2025)) — Labour force participation rate by sex and age, ILO modelled estimates. Not verified. Machine-readable.
  - breakdowns: Sex by age
  - countries: 276 areas (complete balanced panel)
  - years: 1990-2027
  - caveats: Coverage was read from the ILO TOC only; no data were fetched. These are imputed and modelled values, not observations, and do not start before 1990. They replaced EAPEP editions 5 and 6. Not suitable as a pre-1990 holdout.
- **Print: ILO, 'Economically active population: estimates and projections 1950-2010', 4th ed., Geneva 1996-97, Vols. I-VI (Vol. IV covers Northern America, Europe and Oceania). LABPROJ diskettes (ASCII) with a Diskettes User's Guide, 1997, and a CD-ROM. 2000 consolidated volume: 'Estimates and projections of the economically active population 1950-2010', Sources and Methods vol. 10. Methods: STAT working paper 2000-2.** (ILO, Economically Active Population Estimates and Projections (EAPEP), 4th edition) — EAPEP 1950-2010: population, activity rates and labour force by sex and 5-year age group. Not verified. Not machine-readable.
  - breakdowns: Sex by 5-year age groups 10-14 ... 60-64, 65+
  - countries: 178 countries or territories (those with at least 200,000 inhabitants in 1990)
  - years: Decennial 1950, 1960, 1970, 1980, 1990, plus 1995, with projections to 2000 and 2010
  - caveats: No official machine-readable copy was found online. ILOSTAT has no EAPEP indicator; its modelled series start in 1990. Archived LABORSTA EAPEP pages in the Wayback Machine (2006-2022) cover only the 5th edition, 1980-2020. Reusing the print tables would mean keying data from scans. These are ILO harmonised estimates, interpolated and adjusted, not observations.
- **http://web.archive.org/web/2009id_/http://laborsta.ilo.org/applv8/data/EAPEP/EAPEP_E.html; country profiles at .../applv8/data/EAPEP/Profiles/<ISO2>/<ISO2>.html (2007 and 2009 captures); methods PDF at .../applv8/data/EAPEP/EAPEP_methodology.pdf** (ILO LABORSTA, EAPEP 5th edition (2009 revision), via the Internet Archive) — EAPEP 5th edition: activity rates by sex and 5-year age, 1980-2020. Verified. Not machine-readable.
  - breakdowns: Sex by 5-year age groups 15-64 and 65+
  - countries: About 190 (per the annex list)
  - years: 1980-2008 estimates, projections to 2020
  - caveats: The landing page was fetched. The 'Statistics' link pointed to a LABORSTA query interface that is no longer live. The archived profiles are HTML and SAS-graph pages, not data files. Modelled values, starting in 1980.
- **CPI_XCPI_COI_RT_A (also _Q and _M); https://rplumber.ilo.org/data/indicator/?id=CPI_XCPI_COI_RT_A&timefrom=1914&format=.csv** (ILOSTAT (ILO), PRICES database) — National consumer price index by COICOP division (2017 = 100). Verified. Machine-readable.
  - breakdowns: COICOP divisions CP01-CP12 plus the total (CP01T12). CP04 is housing, water, electricity, gas and other fuels. There is no separate actual-rentals sub-index (CP041).
  - countries: 198 areas. Start years for OECD. Total CPI: CAN and NZL 1940; AUS 1949; KOR 1952; most others 1955. Food (CP01): about 1955-61 for most. Housing (CP04): PRT 1948, AUS 1973, NOR 1979, SWE 1980, CHE and IRL 1983, ISR and KOR 1985, GBR 1988, FRA 1990, DEU 1991, ITA 1996, many others 1995-2010, USA and FIN 2010, CAN 2015. JPN has the total only.
  - years: 1914-2026 (most OECD series from 1955)
  - caveats: Weak for the rent-relative-to-goods construct. CP04 bundles rents with utilities, and before the 1980s-90s only the total and food are available for most OECD countries. The older ILO Yearbook CPI tables had group indices that may have included rent, but those are not in ILOSTAT; this was not verified.
- **EAR_EMTA_SEX_ECO_NB_A (mean nominal monthly earnings of employees by sex and economic activity); also EAR_EMTA_SEX_CUR_NB_A** (ILOSTAT (ILO), COND database) — Mean nominal monthly earnings of employees by sex and economic activity. Verified. Machine-readable.
  - breakdowns: Sex by ISIC economic activity, in local currency
  - countries: 194 areas. 1969- for AUS, AUT, BEL, CAN, CHE, DNK, ESP, GBR, ISR, JPN, KOR, POL and USA (mostly 20-28 years up to 1996). NLD 1972; CRI 1973; CHL 1978; others 1980s-2000s.
  - years: 1969-2025
  - caveats: Pre-1997 values come from ILO October Inquiry and Yearbook submissions, with mixed concepts (hourly, daily or monthly, sector coverage). There is no age breakdown.
- **https://population.un.org/wpp/assets/Excel%20Files/1_Indicator%20(Standard)/CSV_FILES/WPP2024_PopulationBySingleAgeSex_Medium_1950-2023.csv.gz (62 MB). Also ..._PopulationBySingleAgeSex_Medium_2024-2100.csv.gz, WPP2024_PopulationByAge5GroupSex_Medium.csv.gz, WPP2024_Population1JanuaryBySingleAgeSex_Medium_1950-2023.csv.gz** (UN DESA Population Division, World Population Prospects 2024) — Population by single age and sex, 1 July (and 1 January), medium variant. Verified. Machine-readable.
  - breakdowns: Single ages 0-99 and 100+; male, female and total. Columns: LocID, ISO3_code, Time, AgeGrp, AgeGrpStart, PopMale, PopFemale, PopTotal.
  - countries: 237 countries and areas plus regional aggregates. All 38 OECD members are present for all 74 years.
  - years: 1950-2023 estimates; 2024-2100 projections
  - caveats: These are model-based reconstructions on current borders: DEU unified back to 1950, and CZE, SVK, SVN and the Baltic states as present-day units. They are smoothed, not census counts. Files named WPP2026 at the same path returned 404 on 2026-10-08, so WPP2024 (files dated December 2024) is current there. Licence CC BY 3.0 IGO.
- **https://www.un.org/development/desa/pd/sites/www.un.org.development.desa.pd/files/undesa_pd_2026_hh-size-composition.xlsx (also served as https://population.un.org/Household/assets/UNDESA_PD_2026_hh-size-composition.xlsx); methods: .../files/undesa_pd_2026_methodology-report_hh-size-composition.pdf** (UN DESA Population Division, Database on Household Size and Composition 2026) — Household size and composition 2026. Verified. Machine-readable.
  - breakdowns: One row per source-year: average household size; households by size; female head; head's age; households with members in age ranges (under 15, 18 or 20; 60+ or 65+); average numbers of members under 15, under 20 and aged 20-64; basic household types (one-person, couple only, couple with children, single parent, single mother or father, extended family, non-relatives); intergenerational types (nuclear, multi-generation, three-generation, skip-generation). There is no indicator for young adults living with their parents.
  - countries: 200 countries; 1,129 source-rows; 215 rows dated before 1997, covering 86 countries. Source-years for OECD (I = IPUMS, D = Demographic Yearbook, L = EU-LFS, M = MICS). USA I 1960, 1970, 1980, 1990, then 2000-. FRA I 1962, 1968, 1975, 1982, 1990, 1999. GBR I 1961, 1971, 1991. IRL I 1971, 1979, 1981, 1986, 1991, 1996. AUT, GRC I 1971, 1981, 1991. CHE, HUN I 1970, 1980, 1990. CHL I 1970, 1982, 1992. MEX I 1970, 1990, 1995. COL I 1973, 1985, 1993 and D 1990, 1995. CRI I 1973, 1984. ISR I 1972, 1983, 1995. PRT I 1981, 1991. POL I 1978, 1988. ESP I 1991. TUR I 1985, 1990 and D 1993. Most others, including AUS, CAN, JPN, KOR, NZL, DEU, ITA, NLD, NOR, FIN and the Nordics, only from 2000-2011. DNK and SWE are absent.
  - years: 1959-2025 (reference years)
  - caveats: Indicators are recomputed from IPUMS microdata, DYB tabulations, EU-LFS, DHS and MICS, so the source switches by year. Pre-1997 OECD coverage is almost entirely IPUMS census samples. For a young-adult coresidence measure, the IPUMS-International microdata it draws on would be needed (separate registration).
- **https://www.un.org/development/desa/pd/sites/www.un.org.development.desa.pd/files/undesa_pd_2026_living-arrangements-older-persons.xlsx** (UN DESA Population Division, Database on Households and Living Arrangements of Older Persons 2026) — Households and living arrangements of older persons 2026. Verified. Machine-readable.
  - breakdowns: Age ranges 60+, 65+ and 80+, by sex. Household size; head's age; coresidence with a child or young person; household type; coresidence with spouse, children under 20, or children 20+; intergenerational types.
  - countries: 181 countries; 9,333 rows; 1,845 rows before 1997 across 83 countries. OECD source-years are essentially the same as the household-size database (IPUMS census years from 1960 for USA, 1962 for FRA, 1961 for GBR, 1970-71 for AUT, CHE, CHL, GRC, HUN, IRL, MEX); SWE has 2012 only.
  - years: 1959-2025
  - caveats: Same source mix as the household-size database. It is about older persons; 'with children aged 20+' measures the parent side of coresidence with adult children.
- **https://unstats.un.org/unsd/demographic/products/dyb/DYBHist/HistTab12.csv (Table 12, marital status); HistTab03.csv (Table 3, population by age, sex and urban/rural, each census); notes in NotesHistTabNN.pdf; index at https://unstats.un.org/unsd/demographic/products/dyb/dybhist.htm** (UN Statistics Division, Demographic Yearbook 1997 Historical Supplement) — Population by marital status, age, sex and urban/rural residence, each census, 1948-1997 (Table 12). Table 3 gives population by age and sex for each census.. Verified. Machine-readable.
  - breakdowns: Sex; marital status (single, married or consensual, widowed, divorced or separated, unknown); 5-year age groups; total, urban and rural
  - countries: 215 countries or areas parsed. Census years: USA 1950, 60, 70, 80, 90. CAN 1951, 56, 61, 66, 71, 76, 81, 86, 91. JPN every 5 years 1950-95. KOR 1955-95 every 5 years. AUS 1954, 61, 66, 71, 76, 81, 86. NZL 1951, 56, 61, 66, 76, 81, 86, 91, 96. FRA 1954, 62, 68, 75, 82, 90. FRG 1950, 61, 70, 87; GDR 1950, 64, 71, 81. ITA 1951, 61, 71, 81. ESP and PRT 1950, 60, 70, 81, 91. SWE 1950, 60, 65, 70, 75, 80, 85, 90. NOR 1950-90 decennial. DNK 1950, 60, 65, 70, 81, 91. FIN 1950, 60, 70, 75, 80, 85. CHE 1950-90 decennial. AUT and GRC 1951-91 decennial. IRL 1951, 61, 66, 71, 79, 81, 86, 91, 96. England and Wales and Scotland 1951, 61, 66, 71, 81; UK 1991. NLD 1960 only. BEL 1961, 70, 81. LUX 1960, 66, 70, 81, 91. TUR 1950-90 every 5 years. POL 1950, 60, 78, 84, 88. HUN 1949, 60, 63, 70, 80, 90. ISL 1950, 60. ISR 1961, 72, 83. MEX 1960-90 decennial. CHL 1952, 60, 70, 82, 92. COL 1951, 64, 73, 93. CRI 1950, 63, 73, 84. Czechoslovakia 1961, 70, 80. CZE, SVK, SVN 1991. Baltics 1989.
  - years: 1948-1997
  - caveats: The CSV reproduces the print layout: wide, with country, date and sex blocks, and needs custom parsing (cell column 1 = country, column 2 = census date). It is a marriage proxy for leaving home, not coresidence itself. Territorial units are historical (FRG and GDR, the UK constituent countries, Czechoslovakia, the USSR).
- **http://data.un.org/Data.aspx?d=POP&f=tableCode%3a23 (marital status by age and sex). Per-country filter: ...&f=tableCode%3a23%3bcountryCode%3a<M49>%3brefYear%3a<y1>%2c<y2>&s=refYear%3aasc. Related tables: 22 (population by age, sex, urban/rural; 1948-2026); 327 (population in households by relation to head, by age and sex; 1995-2024); 32 (population by activity status, age, sex; 1995-2024); 29 (school attendance at ages 5-24 by single year of age and sex; 1995-2024); 50, 326, 328, 329, 330 (household tables; 1995-2024).** (UNdata, Demographic Statistics Database (UNSD DYB), POP datamart) — DYB tables in UNdata: marital status by age and sex (table 23, 1948-2025); census household relationship by age and sex (table 327, 1995-2024); activity status by age and sex (table 32, 1995-2024). Verified. Not machine-readable.
  - breakdowns: Table 23: sex, 5-year age, marital status, urban/rural, record type (census or estimate), reliability. Table 327: relation to the household head (including child of head) by age and sex. Table 32: activity status by age and sex.
  - countries: Table 23: 232 areas; 715,016 records. Record counts by decade (1948-59, 60s, 70s, 80s, 1990-96) are non-zero in every decade for AUS, AUT, CAN, CHL, CRI, DNK, FIN, FRA, GRC, HUN, IRL, ISL, JPN, KOR, NLD, NZL, NOR, POL, PRT, ESP, SWE, CHE, TUR and USA (earliest years: DNK and NLD 1948; USA and SWE 1949). BEL, ISR, LUX and MEX start in 1960-61. ITA has 1951-81 but nothing for 1990-96. Under current codes, DEU, GBR and CZE have nothing before 1982-91 (historical codes not queried). Table 327: 125 areas, 1995-2024. Table 32: 171 areas, 1995-2024.
  - years: Table 23: 1948-2025. Tables 327, 32 and 29: 1995-2024.
  - caveats: The bulk CSV download handler (data.un.org/Handlers/DownloadHandler.ashx) and the DataHandler both returned 404 on 2026-10-08. Data are reachable only by scraping the HTML record view (paged, 50 per page). The filter-panel year lists ignore the country filter, so use record counts or sorted pages. The census economic and household tables (32, 327) start in 1995 here; earlier editions exist only in the PDFs.
- **https://www.un.org/development/desa/pd/sites/www.un.org.development.desa.pd/files/undesa_pd_2019_wmd_marital_status.xlsx (sheets: MARITAL_STATUS_BY_AGE, CURRENTLY MARRIED, EVER_MARRIED, SMAM); metadata in undesa_pd_2019_world_marriage_metadata.pdf** (UN DESA Population Division, World Marriage Data 2019) — Marital status by age and sex; proportions ever married and currently married; singulate mean age at marriage. Verified. Machine-readable.
  - breakdowns: Sex; 5-year age groups (15-19, 20-24, 25-29, ...); marital status; data process (census, estimate, survey)
  - countries: 230 areas; 55,826 ever-married rows. OECD years for ages 20-24 (count before 1997): DNK, FIN, FRA, HUN, ISL, NLD, NOR, SWE nearly annual from 1970-74 (22-27 years each). CAN 1971- (21). AUS 1971- (11). AUT 1970- (14). GBR 1971, then 1982- (14). IRL 1971- (13). ISR 1972- (13). CHL 1970- (13). CHE 1970- (12). TUR 1970- (9). POL 1972- (8). JPN, KOR 1970-90 every 5 years. USA 1970, 1995. ESP, PRT, ITA, LUX, MEX about 5 each. DEU 1987-. EST 2000-.
  - years: 1960-2019 (OECD rows effectively from 1970)
  - caveats: Despite the 'around 1950' wording on the page, the earliest OECD row is 1970; use the DYB Historical Supplement for 1948-69. Mixes census, estimate and survey rows, and the treatment of consensual unions varies (flag column).
- **https://unstats.un.org/unsd/demographic-social/products/dyb/dybsets/<YYYY> DYB.pdf for 1948 through 2024 (1949-50 is a combined issue; special issues in 1978 and 1991; from 2009-10 the file name has no ' DYB'). Index at https://unstats.un.org/unsd/demographic-social/products/dyb/** (UN Statistics Division, Demographic Yearbook archive (PDF)) — Demographic Yearbook issues 1948-2024 (census-topic issues include economically active population and household tables). Not verified. Not machine-readable.
  - breakdowns: Varies by issue; census-topic issues tabulate economically active population by age and sex, and households
  - countries: All UN members reporting
  - years: 1948-2024
  - caveats: PDF scans only; the links were listed but no PDFs were downloaded. Which issues carry the activity and household tables was not checked in this session.

**Not found or not reachable.**
- ILO EAPEP 4th edition (1950-2010, 5-year age by sex, 178 countries): no machine-readable copy found on ILO websites, ILOSTAT, data.ilo.org or UNdata. It exists as print volumes I-VI (1996-97), the 2000 Sources and Methods vol. 10, LABPROJ ASCII diskettes (1997) and a CD-ROM. Wayback Machine captures of laborsta.ilo.org/applv8/data/EAPEP start in 2006-2008 and hold only the 5th edition (1980-2020). An EAPEP/v4 path has no captures.
- A third-party spreadsheet of EAPEP 4th-edition Table 4 (Victor Gay, ZBW Journal Data, CC-BY; metadata says 1950 and 1960 only), at https://journaldata.zbw.eu/dataset/57308aec-c23a-4cce-aee2-bafb75c96d83: the site sits behind an Anubis proof-of-work bot check, so it was not accessed. A manual browser download would be needed.
- ILOSTAT modelled participation estimates (ILOEST) do not go before 1990, so no ILO harmonised annual panel exists for 1950-89. Before LFS start dates, the only observed ILO data are census benchmarks (source AA, roughly decennial from 1947-61).
- UN Household Size and Composition database: no indicator for young adults living with their parents, and no age-specific coresidence of 20-34-year-olds. It has only household types and age-composition shares. Before 1997, OECD coverage comes only from IPUMS census samples (about 18 OECD countries; none for DNK or SWE; JPN, KOR, AUS, CAN, NZL, DEU, ITA, NLD, NOR and FIN only from 2000).
- UN DYB census table 'Population in households by relation to head of household, by age and sex' (UNdata POP table 327), which would give young adults who are children of the household head: only 1995-2024 in machine-readable form. Earlier rounds are only in the DYB PDFs.
- UNdata bulk CSV export (Handlers/DownloadHandler.ashx and DataHandler.ashx) returned HTTP 404 on 2026-10-08. DYB tables in UNdata can only be scraped from HTML record views.
- Rents relative to goods from this family: ILOSTAT CPI has no actual-rentals sub-index. COICOP CP04 (housing and utilities together) starts in 1973-2015 for most OECD countries (PRT 1948 the exception); before that only total CPI and food exist. Earlier ILO Yearbook CPI group tables are print/PDF only and not in ILOSTAT.
- The ILO Yearbook of Labour Statistics, Retrospective Edition on Population Censuses 1945-89 (1990, 1,059 pages, 559 censuses): print only. Its census activity tables appear to be the source of ILOSTAT's AA census points, which are machine-readable.
- UN WPP 2026 revision: files named WPP2026 at the standard WPP CSV path returned 404 on 2026-10-08. The WPP data-portal API requires a token and was not used.

**Access.** I scouted coverage only. No data values, levels, trends or relationships were reported. The values I fetched were reduced to years, counts and codes.

**Network.** All fetches went through Python with truststore and the User-Agent 'Mozilla/5.0 (research; laborformal)'.
- Scripts: C:\Users\s6068C\AppData\Local\Temp\claude\C--Users-s6068C-GitHub-laborformal\57a37d3a-ed63-4c7d-9808-2133339ff86c\scratchpad\lr_ilo_un\code\ (common.py, ilo_cov*.py, wpp_get.py, hh_cov.py, dybh12c.py, dyb_dec.py, wmd3.py).
- Data: ...\scratchpad\lr_ilo_un\data\, including the full-world ILOSTAT CSVs for EAP_DWAP, POP_XWAP, EAP_TEAP, UNE_DEAP, the STU and NEET series, CPI and EAR. These hold values; keep them blinded and do not open them before predictions are frozen.

**ILOSTAT.**
- The rplumber API works unauthenticated: /data/indicator/?id=..&ref_area=A+B&timefrom=&timeto=&format=.csv (.parquet and .rds also work). /metadata/toc/indicator/ gives indicator-level start and end years. /metadata/dic/?var=source|note_source|note_classif|obs_status gives the code labels. There is no per-country availability endpoint, so country coverage was computed from the fetched files.
- Source code prefixes: AA = population census, BA = LFS, BX = other household survey, EA = official estimate. The 'B' obs_status flags a break.
- The indicator updates often (last update 02/10/2026). Snapshot and hash the file before pre-registration.

**Holdout.** For the backward holdout, the pre-1997 European years and all years for the non-European OECD members exist in the same EAP_DWAP_SEX_AGE_RT_A file. Selection can be done by ref_area and time without inspecting values.

**UN WPP.** Direct CSV.gz files under population.un.org/wpp/assets/... work. The /wpp/downloads page itself returned 404.

**UN DESA households.** xlsx files on un.org work. The header rows sit on row 4 or 5 of the data sheet.

**UNSD DYB Historical Supplement.** CSVs at unstats.un.org/unsd/demographic/products/dyb/DYBHist/HistTabNN.csv work. They are in print layout.

**UNdata.** Data.aspx record views work. Sorting (&s=refYear:asc) and multi-year filters (refYear:1950,1951) work, and the record count is in spanRecordCount. The download handlers are 404.

**Blocked.** ZBW Journal Data is behind an Anubis bot check; it was not bypassed.

## us_long

**Best long panel.** This family covers the United States only, as one country.

Participation by sex and age: CPS NSA series LNU013xxxxx for 7 bands (16-19, 20-24, 25-34, 35-44, 45-54, 55-64, 65+) x men and women, monthly 1948-01 to 2026-09. Annual averages give 1948-2025, 78 years; 2025 averages 11 months because October is missing. The start year is 1948 for every one of the 14 cells.

Rents relative to goods, annual from 1929: BEA PCE price indexes DTENRG-A (tenant rent) over DGDSRG-A (goods), 1929-2025, quarterly from 1959-Q1. Alternatively, in CPI terms: CUUR0000SEHA (rent, monthly from 1947, irregular from 1914) over CUUR0000SACL1 (commodities less food, from 1935, quarterly until 1955) or CUUR0000SACL1E (commodities less food and energy, from 1957), monthly to 2026-08.

The joint participation-by-rent panel therefore runs 1948-2025 annual (1948-2026 monthly with CPI).

Moderators and controls:
- Unemployment by age: 1948.
- School enrollment by age and sex (Census A-2): 1947 for 16-19 and 25-34; 20-24 from 1959.
- Coresidence (child of householder): AD-3 annual 1967-2023; AD-1 adds census points for 1960, 1970 and 1980, and CPS for 1983-2025.
- Homeownership by age of householder: 1982 (HVS Table 12), quarterly from 1994 (Table 19).
- National homeownership: 1964/65 (HVS); decennial from 1900.
- Population by single year of age: 1900 (Census pe-11).

- **Not seasonally adjusted participation rates. Men: LNU01300013 (16-19), LNU01300037 (20-24), LNU01300164 (25-34), LNU01300173 (35-44), LNU01300182 (45-54), LNU01300190 (55-64), LNU01300199 (65+). Women: LNU01300014, LNU01300038, LNU01300327, LNU01300334, LNU01300341, LNU01300347, LNU01300354. Both sexes: LNU01300012, LNU01300036, LNU01300089, LNU01300091, LNU01300093, LNU01300095, LNU01300097. Extra bands for both sexes/men/women: 16-17 LNU01300086/152/317, 18-19 LNU01300088/154/319, 16-24 LNU01324887/885/886, 25-54 LNU01300060/061/062, 55+ LNU01324230/231/232. API: POST https://api.bls.gov/publicAPI/v1/timeseries/data/** (BLS Current Population Survey (LN database), checked through the BLS public API v1 and the DBnomics mirror BLS/ln) — Civilian labor force participation rate by sex and age. Verified. Machine-readable.
  - breakdowns: Sex (both, men, women) x 7 target age bands (16-19, 20-24, 25-34, 35-44, 45-54, 55-64, 65+), plus 16-17, 18-19, 16-24, 25-54 and 55+. Finer 5-year bands (25-29, 30-34, 55-59, 60-64, 65-69, 70+) start only in 1976-06 by sex and 1982-01 for both sexes.
  - countries: US
  - years: 1948-01 to 2026-09 (BLS API). The DBnomics mirror stops at 2025-01. 2025-10 is missing.
  - caveats: Verified with BLS API v1: all 14 sex-by-age series have 120/120 months for 1948-1957, and 116 months for 2017-01 to 2026-09. October 2025 is blank, with the footnote 'Data unavailable due to the 2025 lapse in appropriations'. Universe is the civilian noninstitutional population, so the armed forces are excluded. That matters for young men during Korea and the Vietnam draft years. Before 1967 BLS reconstructed the series on a 16+ basis, but the 1967 definition changes (job search, availability) are not fully bridged. Other known CPS breaks: new population controls in 1953, 1962, 1972, 1982 and 1994; Alaska and Hawaii added in 1960; the January 1994 questionnaire and collection redesign (CATI/CAPI), the largest break, which especially affects women and older workers; 2000-census controls; and population-control steps every January since the early 2000s that are not smoothed (BLS footnotes a January 2026 control revision). These breaks come from BLS documentation as I know it. bls.gov returned 403, so I could not re-read the documentation pages.
- **LNS11300013/14 (16-19 M/F), LNS11300037/38 (20-24), LNS11300164/327 (25-34), LNS11300173/334 (35-44), LNS11300182/341 (45-54), LNS11324231/232 (55+), LNS11300152/317 (16-17), LNS11300154/319 (18-19), LNS11324885/886 (16-24), plus the both-sexes versions** (BLS CPS (LN), seasonally adjusted, via the DBnomics mirror BLS/ln) — Civilian labor force participation rate by sex and age, seasonally adjusted. Verified. Machine-readable.
  - breakdowns: Sex x age up to 45-54, plus 55+. There is no seasonally adjusted 55-64 or 65+ series.
  - countries: US
  - years: 1948-01 to 2025-01 on DBnomics (current at BLS)
  - caveats: Same CPS breaks as the unadjusted series. Seasonal factors are revised each year. For annual work, use the unadjusted (NSA) series, which exist for every band.
- **NSA both sexes: LNU04000012 (16-19), LNU04000036 (20-24), LNU04000089 (25-34), LNU04000091 (35-44), LNU04000093 (45-54), LNU04000095 (55-64), LNU04000097 (65+). Men/women: LNU04000013/14, 037/038, 164/327, 173/334, 182/341, 190/347, 199/354. Also 16-24 LNU04024887/885/886 and 55+ LNU04024230/231/232. Seasonally adjusted: LNS14000xxx (cached LNS14000060 is 25-54).** (BLS CPS (LN): unemployment rate by age and sex) — Unemployment rate by age (and sex). Verified. Machine-readable.
  - breakdowns: Sex x the same age bands as participation
  - countries: US
  - years: 1948-01 to 2026-09 (BLS API for the 7 both-sex bands). DBnomics to 2025-01.
  - caveats: Verified with BLS API v1: 7 both-sex bands complete for 1948-1957 and 2017-2026-09, with 2025-10 missing. The seasonally adjusted women 55+ series (LNS14024232) starts only in 1994-01; its NSA counterpart runs from 1948. The 1967 unemployment-definition change, the 1994 redesign and the population-control breaks all apply.
- **LNU00000012/13/14 (16-19), LNU00000036/37/38 (20-24), LNU00000089/164/327 (25-34), LNU00000091/173/334, LNU00000093/182/341, LNU00000095/190/347, LNU00000097/199/354, LNU00024887/885/886 (16-24)** (BLS CPS (LN): civilian noninstitutional population by age and sex, via DBnomics) — Civilian noninstitutional population by age and sex (CPS). Verified. Machine-readable.
  - breakdowns: Sex x age bands
  - countries: US
  - years: 1948-01 to 2025-01 on DBnomics (current at BLS)
  - caveats: Levels jump whenever population controls change (1953, 1962, 1972, 1982, 1994, 2000s and every January). Use these as weights within a year, not as a smooth demographic series.
- **Participation of those enrolled: LNU01322967 (16-24), LNU01322966 (16-19), LNU01322968 (20-24); by sex 16-24 LNU01322979 (M) and LNU01322985 (F). Not enrolled: LNU01323016 (16-24), LNU01323014, LNU01323020; by sex LNU01323048 and LNU01323059. By level of enrollment, 16-24: high school LNU01322990, college LNU01322996, college full-time LNU01323002, college part-time LNU01323008. Matching population (LNU000xxxxx), employment, unemployment and unemployment-rate (LNU04022967 etc.) series also exist. Quarterly versions carry a Q suffix.** (BLS CPS (LN): labor force status by school enrollment, via DBnomics) — Labor force participation and unemployment of 16-24 year olds by school enrollment status. Verified. Machine-readable.
  - breakdowns: Enrolled / high school / college (full-time, part-time) / not enrolled, by age 16-19, 20-24 and 16-24. Sex only for 16-24.
  - countries: US
  - years: 1985-01 to 2025-01 on DBnomics (quarterly 1985-Q1 to 2024-Q4)
  - caveats: Nothing before 1985 in the database. Earlier, the October CPS supplement figures (BLS 'College enrollment and work activity of high school graduates', from 1959) exist only as releases and PDFs on bls.gov, which returned 403 from this machine. The 1994 redesign also applies.
- **CUUR0000SEHA (NSA), CUSR0000SEHA (SA, from 1981)** (BLS CPI-U) — CPI-U, Rent of primary residence, U.S. city average. Verified. Machine-readable.
  - breakdowns: none (national)
  - countries: US
  - years: 1914-12 to 2026-08
  - caveats: Verified with BLS API v1: 120/120 months for 1948-1957, data to 2026-08, 2025-10 missing (lapse in appropriations). Known methodological breaks in the rent index: before January 1985 the treatment of nonresponse and vacant or turnover units is documented to bias measured rent change downward (Crone, Nakamura & Voith 2010, REStat; Gordon & van Goethem 2007, NBER CRIW 'Downward bias in the most important CPI component... 1914-2003'). An aging/depreciation adjustment was added in 1988, the estimator and sample were changed in the 1990s, and the housing sample was redesigned in 2005. Homeowner rental equivalence (1983 in CPI-U) changes shelter but not this series. Corrected long rent series appear in those papers.
- **CUUR0000SACL1E (NSA), CUSR0000SACL1E (SA)** (BLS CPI-U) — CPI-U, Commodities less food and energy commodities. Verified. Machine-readable.
  - breakdowns: none
  - countries: US
  - years: 1957-01 to 2026-08
  - caveats: Verified with BLS API v1, which answered 'No Data Available' for 1948-1956. The series starts in 1957. Before 1957, splice to CUUR0000SACL1 or CUUR0000SAC, or use the BEA PCE goods price index. Quality-adjustment and geometric-mean methods changed in the 1990s (from 1999 for lower-level indexes).
- **CUUR0000SACL1 (commodities less food), CUUR0000SAC (commodities)** (BLS CPI-U) — CPI-U, Commodities less food; Commodities. Verified. Machine-readable.
  - breakdowns: none
  - countries: US
  - years: 1935-03 to 2026-08
  - caveats: Verified with BLS API v1: 56 observations in 1948-1957 (quarterly until 1955), data to 2026-08. These include energy commodities, unlike SACL1E. They are the longest CPI 'goods' denominators for rents relative to goods from 1935.
- **CUUR0000SA0 (all items, 1913-01), CUUR0000SAA (apparel, 1914-12; monthly from 1941), CUUR0000SAD (durables, 1935-03), CUUR0000SAN (nondurables, 1935-03), CUUR0000SAS (services, 1935-03), CUUR0000SAH1 (shelter, 1952-12), CUUR0000SAH (housing, 1967-01), CUUR0000SEHC (owners' equivalent rent, 1982-12), CUUR0000SAS2RS (rent of shelter, 1982-12), CUUR0000SA0L1E (all items less food and energy, 1957-01), CUUR0000SACE (energy commodities, 1957-01), CUUR0000SASLE (services less energy, 1957-01), CUUR0000SACL11 (commodities less food and beverages, 1967-01)** (BLS CPI-U, other components (coverage via the DBnomics mirror BLS/cu)) — CPI-U component indexes for building rent and goods ratios. Verified. Machine-readable.
  - breakdowns: item groups
  - countries: US
  - years: Start years as listed; DBnomics to 2025-01, BLS current
  - caveats: DBnomics BLS mirror is stale (last observation 2025-01). Refresh from the BLS API. The shelter and housing aggregates change concept with 1983 rental equivalence.
- **DTENRG-A / DTENRG-Q (rental of tenant-occupied nonfarm housing), DHSGRG (housing), DOWNRG (imputed owner rent), DGDSRG (goods), DDURRG (durable goods), DNDGRG (nondurable goods), DGOERG (gasoline and other energy goods), DPCERG (PCE). Cached in paths/cache: DGDSRG3Q086SBEA (goods, 1947Q1-2026Q2) and DHLCRG3Q086SBEA (housing and utilities, 1947Q1-2026Q2).** (BEA NIPA Table 2.4.4 (PCE price indexes by type of product), via the DBnomics mirror BEA/NIPA-T20404) — PCE price indexes: tenant rent, housing, goods. Verified. Machine-readable.
  - breakdowns: product type
  - countries: US
  - years: Annual 1929-2025 for every line listed. Quarterly from 1947-Q1 for goods, durables, nondurables and housing-and-utilities; from 1959-Q1 for tenant rent and housing; to 2026-Q2.
  - caveats: DBnomics BEA data are current (indexed 2026-10). The tenant-rent price index draws on CPI rent, so it likely carries the pre-1985 CPI rent bias. Goods excluding food and energy is not a published line here and would need Fisher chaining from the components. Comprehensive NIPA revisions re-base the whole history.
- **https://www2.census.gov/programs-surveys/demo/tables/families/time-series/adults/ad1.xls** (US Census Bureau, Families and Living Arrangements historical tables) — Table AD-1. Young Adults, 18-34 Years Old, Living At Home: 1960 to Present. Verified. Machine-readable.
  - breakdowns: Ages 18-24 and 25-34 x men/women. Columns: total, child of householder, percent.
  - countries: US
  - years: 1960, 1970 and 1980 (decennial census), CPS 1983-2025 annual. 1981-1982 have totals only; child of householder is 'N'. Revised rows for 2011 and 2021; flags for 2014 and 2025.
  - caveats: Excel (.xls) with a spreadsheet layout. In CPS, unmarried college students in dormitories count as living at home; the census points use a different concept and source. There is a 1980-to-1983 gap and a census-versus-CPS seam. No 1950 point; 1950 needs IPUMS USA microdata, which requires an account.
- **https://www2.census.gov/programs-surveys/demo/tables/families/time-series/adults/ad3-18-24.xls ; .../ad3-25-34.xls ; also ad3-35-64.xls, ad3-65-74.xls, ad3-75andover.xls, ad3.xls** (US Census Bureau, Families and Living Arrangements historical tables) — Table AD-3. Living Arrangements of Adults by Age Group, 1967 to 2023. Verified. Machine-readable.
  - breakdowns: Men/women x living alone, with spouse, child of householder, with partner, with other relatives, with nonrelatives (numbers and percent)
  - countries: US
  - years: 1967-2023 annual (CPS ASEC, March). 58 year rows including the revised 2021 row.
  - caveats: Excel (.xls). This is the longest annual coresidence series. 'Child of householder' excludes people living with a spouse or partner. Before 1995 partners are measured indirectly (POSSLQ). The 2014 ASEC redesign and population-control revisions also apply. Dormitory students count as living at home. Ends 2023 (AD-1 runs to 2025).
- **https://www.census.gov/housing/hvs/data/histtab19.xlsx** (US Census Bureau, CPS/Housing Vacancy Survey historical tables) — HVS Table 19. Quarterly Homeownership Rates by Age of Householder: 1994 to Present. Verified. Machine-readable.
  - breakdowns: Age of householder: under 35, 35-44, 45-54, 55-64, 65+ (plus the US total)
  - countries: US
  - years: 1994-Q1 to 2026 (file dated 2026-07-28)
  - caveats: XLSX with a spreadsheet layout. Revised on the 2000 census basis. 2025-Q4 is based only on November and December, because October 2025 was not collected.
- **https://www.census.gov/housing/hvs/data/histtab12.xlsx (also hist_tab_12a_v2025.xlsx; histtab15.xlsx for age x family status)** (US Census Bureau, CPS/HVS historical tables) — HVS Table 12. Household Estimates by Age of Householder (total and owner): 1982 to Present. Verified. Machine-readable.
  - breakdowns: Age of householder in 5-year bands (<25, 25-29, ... 75+) and summary bands (<35, 35-44, 45-54, 55-64, 65+), total and owner households, so an ownership rate by age can be computed
  - countries: US
  - years: 1982-2025 annual
  - caveats: XLSX laid out in year blocks. Footnoted breaks at 1982, 1989, 1993 (r1) and 2002 (r2), from population-control and weighting revisions. 2025 is affected by the missing October. Nothing by age before 1982 in HVS.
- **https://www.census.gov/housing/hvs/data/histtab14.xlsx ; histtab13.xlsx ; histtab11.xlsx ; histtab1.xlsx** (US Census Bureau, CPS/HVS historical tables) — HVS Table 14 Homeownership Rates US and Regions (1964/65-); Table 13 Monthly Household Estimates (1955-); Table 11A Median Asking Rent (1988-); Table 1 Rental Vacancy Rates (1956-). Verified. Machine-readable.
  - breakdowns: US and 4 regions (Table 14); no age breakdown
  - countries: US
  - years: Table 14: year labels 1964-2026. Table 13: 1955-2026. Table 11: 1988-2026. Table 1: 1956-.
  - caveats: Revisions flagged r1 (1980 changes), r2 (1990 census) and r3 (2000 census). October 2025 not collected. Table 1 (rental vacancy) is listed but was not downloaded.
- **https://www2.census.gov/programs-surveys/decennial/tables/time-series/coh-owner/owner-tab.txt ; .../coh-grossrents/grossrents-unadj.txt (and -adj) ; .../coh-values/values-unadj.txt (and -adj)** (US Census Bureau, Historical Census of Housing Tables (decennial)) — Homeownership rates (1900-2000); Median gross rents (1940-2000); Median home values (1940-2000). Verified. Machine-readable.
  - breakdowns: US and states. No age breakdown.
  - countries: US
  - years: Decennial: homeownership 1900-2000 (11 points); gross rent and home value 1940-2000 (7 points)
  - caveats: Fixed-width text. Concepts differ across censuses. Tenure by age of householder before 1982 exists only in printed census reports (PDF) or in IPUMS microdata, which needs an account.
- **https://www2.census.gov/programs-surveys/demo/tables/school-enrollment/time-series/cps-historical-time-series/hst_enroll02.xlsx (A-2); hst_enroll05b.xlsx (A-5b); hst_enroll06.xlsx (A-6); hst_enroll07.xlsx (A-7)** (US Census Bureau, CPS October School Enrollment historical tables) — Table A-2. Percentage of the Population 3+ Enrolled in School, by Age, Sex, Race, Hispanic Origin: October 1947 to 2024. Verified. Machine-readable.
  - breakdowns: Age 3-4, 5-6, 7-9, 10-13, 14-15, 16-17, 18-19, 20-21, 22-24, 25-29, 30-34, 35+, by both sexes, male and female (and race blocks)
  - countries: US
  - years: 1947-2024 annual (October), with a revised 1993 row
  - caveats: XLSX. Cells for 20-21 and 22-24 are missing 1947-1958, so those ages start in 1959. 30-34 is missing 1950-1951. 3-4 starts in 1964, and kindergarten is excluded 1947-1963. 1993 is re-controlled to the 1990 census. Universe is the civilian noninstitutional population. A-5b (18-19 by enrollment status) covers 1967-2024.
- **https://www2.census.gov/programs-surveys/popest/tables/1900-1980/national/asrh/pe-11-YYYY.csv (also .xls/.pdf); 1980-1990: https://www2.census.gov/programs-surveys/popest/tables/1980-1990/national/asrh/ (zipped e8081*.zip ...)** (US Census Bureau, national population estimates (pre-1990)) — Resident population plus armed forces overseas, by single year of age, sex and race, July 1. Verified. Machine-readable.
  - breakdowns: Single year of age x sex x race (white / nonwhite)
  - countries: US
  - years: 1900-1979 (80 annual files); 1980-1990 quarterly zipped files; later vintages elsewhere on census.gov
  - caveats: One CSV per year, so it has to be stitched. Universe includes armed forces overseas, which differs from the civilian noninstitutional CPS base. The 1950 file is marked as including Alaska and Hawaii. Intercensal revisions apply.
- **Shiller: http://www.econ.yale.edu/~shiller/data/Fig3-1.xls ; FHFA: https://www.fhfa.gov/hpi/download/monthly/hpi_master.csv ; Jorda-Schularick-Taylor Macrohistory R6: https://www.macrohistory.net/app/download/9834512469/JSTdatasetR6.xlsx (the file is actually Stata .dta). Cached in paths/cache: QUSPAM770A and QUSHAM770A (BIS, 1947-10 to 2025-10), CSUSHPINSA (1987-01 to 2026-06).** (House prices, long series) — Shiller US home price index; FHFA HPI; JST house prices and rental yields. Verified. Machine-readable.
  - breakdowns: Shiller: real home price, building cost, population, long rate. FHFA: US, census divisions, states and metros. JST: hpnom, housing_rent_yd, housing_rent_rtn, cpi, wage, unemp, pop.
  - countries: Shiller and FHFA: US. JST: 18 countries (AUS BEL CAN CHE DEU DNK ESP FIN FRA GBR IRL ITA JPN NLD NOR PRT SWE USA).
  - years: Shiller: 1890-1952 annual, monthly from 1953, to 2023 in this file. FHFA: all-transactions quarterly 1975-2026, purchase-only monthly 1991-2026. JST USA: hpnom 1890-2020, housing_rent_yd 1890-2020, cpi and wage 1870-2020, unemp 1890-2020.
  - caveats: Shiller splices several sources (the column headers name Grebler and Homer). FHFA covers conforming-mortgage transactions only. JST ends in 2020, and its rent indices are implied from rental yields times prices.
- **CES3000000008 (average hourly earnings, production and nonsupervisory, manufacturing); CES0500000008 (total private, same as cached AHETPI); PRS85006103 (hourly compensation, nonfarm business); LEU0252881500 (median usual weekly earnings, full-time, 16+); age-specific: LEU0252886500 (16-19), LEU0252887100 (20-24), LEU0252886300 (16-24), LEU0252888500 (25-34), LEU0252889100 (35-44), LEU0252889700 (45-54), LEU0252890900 (55-64), LEU0252891500 (65+), with sex variants** (BLS wages (CES, Productivity, CPS weekly earnings), via the DBnomics mirror) — Wages: average hourly earnings, hourly compensation, median weekly earnings by age. Verified. Machine-readable.
  - breakdowns: Industry (CES); age x sex (LE)
  - countries: US
  - years: CES3000000008 1939-01 onward; CES0500000008 1964-01 onward; PRS85006103 1947-Q1 onward; LEU0252881500 1979-Q1 onward; age-specific LE 2000-Q1 to 2024-Q4 on DBnomics
  - caveats: DBnomics BLS copies are stale (CES to 2025-01, LE and PR to 2024-Q4). There are no age-specific earnings in the database before 2000; 1979-1999 by age exists only in BLS print tables. Cached locally: AHETPI 1964-01 to 2026-08 and AWHMAN 1939-01 to 2026-08.

**Not found or not reachable.**
- FRED and ALFRED from this machine in this session. FRED: one retry with a 90 s timeout ended in a ProxyError (remote end closed the connection) after 81 s. ALFRED: read timeout after 40 s. The FRED-format files already in paths/cache came from earlier sessions.
- bls.gov web pages and download.bls.gov flat files (pub/time.series/ln, cu) return HTTP 403 with the given User-Agent. CPS documentation and comparability notes, and the BLS 'College enrollment and work activity' releases, could not be read.
- The DBnomics BLS mirror is stale: LN, CU and CE have last observation 2025-01; LE and PR end 2024-Q4. Use the BLS API for 2025-2026.
- No seasonally adjusted participation series for 55-64 or 65+ (no LNS11300095/097/190/199/347/354). Use NSA.
- 5-year CPS age bands (25-29, 30-34, 55-59, 60-64, 65-69, 70+) start only in 1976-06 (by sex) or 1982-01 (both sexes), not 1948.
- CPI commodities less food and energy (SACL1E) does not exist before 1957. For 1935-1956 the closest are SACL1 or SAC (quarterly until 1955) or the BEA PCE goods index (annual from 1929).
- CPI rent of primary residence is not monthly before 1947 (irregular 1914-1946), and before 1985 it carries a documented downward methodological bias.
- Young adults living with parents: no annual series 1950-1966. AD-3 starts in 1967; AD-1 gives only 1960, 1970 and 1980 census points, then CPS from 1983 (1981-82 without the child-of-householder split). No published 1950 point; it would need IPUMS USA microdata, which requires an account.
- Homeownership by age of householder before 1982: not in HVS. Only decennial printed reports (PDF) or IPUMS microdata. Decennial census-of-housing text tables give totals by state, not age (1900-2000). HVS national homeownership starts 1964/65.
- School enrollment for ages 20-21 and 22-24 is missing for 1947-1958 in Table A-2 (available from 1959). Ages 30-34 are missing for 1950-1951.
- Monthly CPS labor force by school-enrollment status before 1985.
- CPS earnings by age before 1979, and age-specific earnings in the BLS LE database before 2000.
- October 2025 CPS and CPI observations do not exist (2025 lapse in appropriations). The HVS 2025-Q4 figure is based on two months.
- Non-European OECD countries other than the US are not covered by this source family. JST R6 does include CAN, AUS and JPN for house prices, wages, unemployment and CPI through 2020, but has no participation by age.

**Access.** What worked: the DBnomics API v22 (fast; series coverage pulled with observations=1, but only first and last periods and counts were printed); the BLS public API v1 by POST (2 of the 6 permitted calls used, each with 25 series over 10 years: 2017-2026 and 1948-1957); www.census.gov and www2.census.gov (XLS, XLSX, CSV and TXT downloads); econ.yale.edu (Shiller); fhfa.gov; macrohistory.net (redirects to jimcontent.com; the file named .xlsx is a Stata .dta, so read it with pandas.read_stata).

What did not work: FRED and ALFRED (proxy timeouts), and bls.gov web pages and download.bls.gov (403).

Files: scripts are in C:\Users\s6068C\AppData\Local\Temp\claude\C--Users-s6068C-GitHub-laborformal\57a37d3a-ed63-4c7d-9808-2133339ff86c\scratchpad\lr_us\code\ (get.py, dbn_query.py, dbn_ids.py, dbn_cov.py, bls_v1.py, struct.py, years.py, links.py, cache_ranges.py, fred_try.py). Downloads are in ...\lr_us\data\: the BLS API JSONs bls_v1_2017_2026.json and bls_v1_1948_1957.json, the DBnomics JSONs, census\*.xls/xlsx/txt, census_pop\pe-11-1950.csv, and hp\ (Shiller, FHFA, JST). Nothing was written in the repository.

Blinding disclosure: while dumping the AD-1 structure, the first version of my year-mask let through 4 numeric cells whose values happened to lie between 1890 and 2030. These were counts in thousands, not percentages, and the scout saw them on screen. The mask was then restricted to column 0. No values are reported here.

Already cached (file, first to last observation):
paths/cache: CIVPART 1948-01..2026-08; LNS11300060 (participation 25-54) 1948-01..2026-08; LNS12300060 1948-01..2026-08; LNS14000060 1948-01..2026-08; LNS13026638 1994-01..2026-08; UNRATE, EMRATIO, CLF16OV, CE16OV and UNEMPLOY each 1948-01..2026-08; CPIAUCNS 1913-01..2026-08; CUSR0000SEHF01 (CPI electricity) 1952-01..2026-08; PCEPI and PCEPILFE 1959-01..2026-07; DGDSRG3Q086SBEA (PCE goods price) 1947Q1..2026Q2; DHLCRG3Q086SBEA (PCE housing and utilities price) 1947Q1..2026Q2; DHLCRC1Q027SBEA 1959Q1..2026Q2; AHETPI 1964-01..2026-08; CES0500000003 2006-03..2026-08; AWHMAN 1939-01..2026-08; PAYEMS 1939-01..2026-08; CSUSHPINSA 1987-01..2026-06; QUSPAM770A and QUSHAM770A (BIS US residential property prices) 1947-10..2025-10; MORTGAGE30US 1971-04..2026-09; HOANBS 1947Q1..2026Q2; PRS85006092 1947Q2..2026Q2; worldbank/SP.POP.65UP.TO.ZS.json (261 economies, 2018-2024); ilo/*USA* files (earnings, employment and temporary employment, not participation).
pinning/cache: CPIAUCSL 1947-01..2026-06; DHSGRC1A027NBEA (PCE housing services, nominal) 1929..2025; PCECA 1929..2025; HNOREMV 1945Q4..2026Q1; GS10 1953-04..2026-07.

Not cached anywhere: sex-by-age participation, unemployment by age (other than 25-54), CPI rent (SEHA), CPI commodities indexes, BEA tenant-rent and goods price indexes (annual 1929-), the Census AD-1/AD-3, HVS, school-enrollment and pe-11 tables, Shiller, FHFA and JST.

## national_long

**Best long panel.** PARTICIPATION by sex and age, longest usable national-statistics-office runs (pre-1997 years and non-European members are the untouched holdout):
- CA 1946-2025: HSC D205-222 (1946-1975, ages 14-19, 20-24, 25-44, 45-64, 65+; break 1975/76) plus WDS 14-10-0327 (1976-, 5-year ages).
- JP 1953-2025 by sex (15+, with 'attending school' counts). 5-year ages x sex 1968-2025 (Okinawa from 1973).
- AU 1966-2025: 6204.0.55.001 (August 1966-1977, 15-19 ... 65+) plus SDMX LF_AGES (monthly 1978-02-).
- NL 1969-2021 (15-24, 25-44, 45-74, reconstructed), then 2013-2026.
- SE 1970-2025: prime and older bands from 1970, 20-24 from 1987, 15-19 from 2001.
- NO 1972-2025 (5-year ages, 16-19 before 2006).
- DK 1981-2024 (register; 16-19, 20-24 ...).
- FI 1989-2025.
- UK 1971 (16+ only), with ages from 1992.
No source in this family reaches 1950 by age for any country except CA (1946) and, by sex only, JP (1953). Getting to 1950 elsewhere means census benchmarks (print).

RENTS relative to goods:
- SE 1950-2024: national-accounts COICOP 04 housing deflator vs food, clothing and furnishings deflators. Actual rentals from 1980; SCB rent changes 1969- (1981 missing); CPI 04.S and the goods aggregate 1980-.
- FI 1940-1982 (dwelling vs food/clothing, chained cost-of-living and CPI bases), gap 1983-1994, 1995-.
- CA rent 1949- vs all-items 1914-; vs the goods aggregate only from 1961.
- NO: housing group 1959-1998; rent vs goods by delivery sector 1969-1992 (HTML); CPI 04.1 1979-; national-accounts 04.1 deflator 1970-.
- DK: national-accounts actual-rentals deflator vs goods groups 1966-2025.
- JP rent vs goods groups 1970-2025.
- AU rents vs food/clothing 1972Q3-.
- NL rent increases 1959- vs all-items CPI (goods split only from 1996).
- UK RPI rent vs RPI goods 1987-.

Best joint panel back to about 1970: CA, JP, AU, SE, NO, FI (Finland's gap 1983-1994 for rents and 1970-1988 for participation), NL (coarse ages) and DK from 1981.

- **https://api.scb.se/OV0104/v1/doris/en/ssd/AM/AM0403/AM0403A/NAKUBefolkning2ArTD (v2 id TAB1271); quarterly NAKUBefolkning2KTD 1970K1-2020K4; monthly NAKUBefolkning2MTD 1970M01-2020M12** (Statistics Sweden (SCB) PxWeb v1) — Population aged 15-74 (LFS) by sex, age and labour status, previous definitions, 1970-2020. Verified. Machine-readable.
  - breakdowns: sex (men, women, total) x age (15-19, 15-24, 20-24, 25-34, 35-44, 45-54, 55-64, 65-74, plus totals 16-64/20-64 etc.) x labour status (employed, unemployed, in LF, not in LF); contents thousands and percent (IAKR+percent = participation rate)
  - countries: SE
  - years: 1970-2020 annual. Age coverage within it: 25-34, 35-44, 45-54, 55-64 from 1970; 20-24 only from 1987; 15-19, 15-24, 65-74 only from 2001 (no estimates for these cells before)
  - caveats: Table note: 1970-2004 is 'linked data' (SCB macro-linked to 2005 definitions); population 16-64 for 1970-2000; no 20-24 estimates 1970-1986; break 2020/2021 (new EU framework regulation), continued in AM0401A/AKURLBefAr 2001-2025. Pre-1970 AKU (quarterly 1961-1969, 16-64, redesign Feb 1964) exists only in print (e.g. SOU 1966:8).
- **https://api.scb.se/OV0104/v1/doris/en/ssd/AM/AM0401/AM0401A/AKURLBefAr (also AKURLBefK quarterly, AKURLBefM monthly)** (Statistics Sweden (SCB) PxWeb v1) — Population aged 15-74 (LFS) by labour status, type of data, sex and age, 2001-2025. Not verified. Machine-readable.
  - breakdowns: sex x age (15-19, 15-24, 20-24, 25-34, 25-54, 35-44, 45-54, 55-64, 55-74, 65-74, totals) x labour status incl. participation rate percent
  - countries: SE
  - years: 2001-2025
  - caveats: Current definitions; 2021 framework-regulation break. Metadata only checked.
- **https://statistikdatabasen.scb.se/api/v2/tables/TAB6332 (v1 path NR household consumption by COICOP)** (Statistics Sweden (SCB) PxWeb v2) — Household consumption expenditure (ESA2010) by purpose COICOP, 1950-2024. Verified. Machine-readable.
  - breakdowns: 154 COICOP items x current prices, constant 2020 prices, price change %, volume change %
  - countries: SE
  - years: CP04 housing/water/energy, CP01 food, CP03 clothing, CP05 furnishings: 1950-2024; CP041 actual rentals, CP042, CP043-044, CP045: 1980-2024; CP0411 tenants' rentals 1993-2024
  - caveats: Implicit deflators (current/constant) give a housing (COICOP 04, incl. energy and imputed rent) price vs goods-group prices from 1950; actual-rentals detail only from 1980. National-accounts deflator, not a CPI.
- **https://api.scb.se/OV0104/v1/doris/en/ssd/BO/BO0406/BO0406G/BO0406TabHf (v2 TAB6051)** (Statistics Sweden (SCB) PxWeb v1) — Rental changes in rented dwellings, 1969-2026. Verified. Machine-readable.
  - breakdowns: Sweden total; average percent change and margin of error
  - countries: SE
  - years: 1969-2026 (1981 missing)
  - caveats: Percent changes only (chain to an index); 1981 gap must be bridged (e.g. with KPI 04.S from 1980).
- **https://api.scb.se/OV0104/v1/doris/en/ssd/PR/PR0101/PR0101L/KPICOI80Ar (TAB2061); goods/services aggregates: .../PR/PR0101/PR0101DE/KPI2020SA1AR; monthly .../PR0101A/KPICOI80MN** (Statistics Sweden (SCB) PxWeb v1) — CPI annual averages by product group (COICOP), 1980=100, 1980-2025; CPI special aggregates goods/services 1980-2024. Verified. Machine-readable.
  - breakdowns: 79 groups incl. 04.S rented and co-operative dwellings rent incl. heating, 04.S.1 rented dwelling rents and fuel, 01 food, 03 clothing; aggregates V goods, T services, durable/semi-durable/non-durable goods
  - countries: SE
  - years: 04.S, 01, 03: 1980-2025; 04.S.1 annual cell empty, monthly 2005M01-2025M12 only; goods V/services T: long-term index 1980-2003 + year-to-year index 2003-2024 (chainable)
  - caveats: KPICOI80 tables not updated after 2025M12 (replaced by 2020=100 tables). Total CPI from 1914 in KPILevindexAr (not fetched).
- **https://statistikdatabasen.scb.se/api/v2/tables/TAB6446 (main occupation); TAB6439 (housing/tenure)** (Statistics Sweden (SCB) PxWeb v2 (ULF/SILC long time series)) — Long time series - Main occupation (16-74) and Housing (tenure) by indicator, age and sex, 1980/81-2025. Not verified. Machine-readable.
  - breakdowns: TAB6446: work, studies, unemployed, retired x age (16-19, 16-24, 20-29, 25-34 ... 65-74) x sex; TAB6439: rented / tenant-owned / owner-occupied dwelling, one-/multi-dwelling, crowding x age (16-19, 16-24, 20-29 ... 85+) x sex
  - countries: SE
  - years: 1980-81 to 2025 (double-year periods to 2020, single years from 2021)
  - caveats: Survey (ULF then SILC), age restriction 16-84 in 1980-87 and 1990-2001; 2021 sample redesign. No 'living with parents' indicator. Metadata only.
- **https://api.scb.se/OV0104/v1/doris/en/ssd/BE/BE0101/BE0101A/BefolkningR1860N** (Statistics Sweden (SCB) PxWeb v1) — Population by single year of age and sex, 1860-2024. Verified. Machine-readable.
  - breakdowns: age 0-110+ single years x sex
  - countries: SE
  - years: 1860-2024 (2025 in BefolkningR1860NCKM)
  - caveats: Register population, 31 Dec.
- **https://api.scb.se/OV0104/v1/doris/en/ssd/BE/BE0101/BE0101S/HushallT08 ; https://api.scb.se/OV0104/v1/doris/en/ssd/LE/LE0102/LE0102E/LE0102T29** (Statistics Sweden (SCB) PxWeb v1 (registers)) — Persons by age, household status and sex (2011-2024); Young persons 16-21 who have left home (2014-2025). Not verified. Machine-readable.
  - breakdowns: household status x age x sex; left-home by age 16-21, sex, family type
  - countries: SE
  - years: 2011-2024; 2014-2025
  - caveats: Register-based household statistics start 2011; nothing earlier in the API (census FoB 1960-1990 only in print). Metadata only.
- **https://www.scb.se/hitta-statistik/aldre-statistik/innehall/sveriges-officiella-statistik-sos/priser-och-konsumtion-19101994/ (e.g. Konsumentpriser och indexberakningar 1931-1959 PDF on share.scb.se)** (Statistics Sweden (SCB) digitised historical publications) — Priser och konsumtion 1910-1994 (CPI and group indices, SOS volumes). Not verified. Not machine-readable.
  - breakdowns: CPI groups incl. housing/rent (as printed)
  - countries: SE
  - years: 1931/1959-1994
  - caveats: PDF scans only; would need transcription for pre-1969 rent/goods relatives.
- **https://data.ssb.no/api/pxwebapi/v2/tables/03780 (quarterly 03777 1972K1-2026K2)** (Statistics Norway (SSB) PxWebApi v2) — 03780: Persons in the labour force, by age and sex 1972-2025. Verified. Machine-readable.
  - breakdowns: sex (M, F) x age 15-19, 20-24, 25-29, ..., 60-64, 65-74, 15-74; thousands and per cent of population (participation rate)
  - countries: NO
  - years: 1972-2025, all cells filled
  - caveats: Notes: Jan 2006 restructuring, lower age limit 16->15 (so '15-19' is 16-19 before 2006); new estimation method 2018 revised back to 2006; Jan 2021 major restructuring, proxy interviews ceased, break noted especially for young people. Quarterly table 05110 restarts 1988K2 (possible 1988 revision; not stated in notes). 1972-1991 also in SSB Historisk statistikk table 9-9 (HTML).
- **https://data.ssb.no/api/pxwebapi/v2/tables/05111 ; break-adjusted 13618 (2009-2025)** (Statistics Norway (SSB) PxWebApi v2) — 05111: Population, by labour force status, age and sex 1972-2025. Not verified. Machine-readable.
  - breakdowns: LF status (total, LF, employed, unemployed, outside LF) x sex x age (15-24, 25-54, 55-74, 15-74, 20-64, 75-89...)
  - countries: NO
  - years: 1972-2025
  - caveats: Same breaks as 03780. Metadata only.
- **https://data.ssb.no/api/pxwebapi/v2/tables/03014 (monthly 03013); continuation 14701/14700 (2000-, 2025=100, goods and services groups)** (Statistics Norway (SSB) PxWebApi v2) — 03014: Consumer Price Index, by consumption group (2015=100) (closed series) 1979-2025. Verified. Machine-readable.
  - breakdowns: 339 COICOP groups incl. 04.1 actual rentals for housing, 04.1.1 rentals paid by tenants, 01 food, 03 clothing, 05 furnishings
  - countries: NO
  - years: 1979-2025
  - caveats: Closed series, replaced by 14700/14701 from Feb 2026; ECOICOP from 2016. Goods vs services aggregates in 14701 from 2000 (metadata only).
- **https://data.ssb.no/api/pxwebapi/v2/tables/14656** (Statistics Norway (SSB) PxWebApi v2) — 14656: Final consumption expenditure of households 1970-2025. Verified. Machine-readable.
  - breakdowns: 124 COICOP items incl. 04.1 actual rental payments, 01.1 food, 03.1 clothing; current prices, constant 2023 prices, volume change, price change
  - countries: NO
  - years: levels 1970-2025; price change 1971-2023
  - caveats: Chained components not additive; post-2023 preliminary.
- **https://www.ssb.no/a/histstat/tabeller/12-6.html ; https://www.ssb.no/a/histstat/tabeller/12-5.html ; https://www.ssb.no/a/histstat/tabeller/9-9.html** (Statistics Norway (SSB) Historisk statistikk (HTML tables)) — 12.6 CPI for goods and services by delivery sector 1969-1992 (incl. 'Husleie' rent); 12.5 CPI by consumption group 1959-1998; 9.9 Labour force participation by age and sex 1972-1991. Verified. Machine-readable.
  - breakdowns: 12.6: agricultural goods, other Norwegian-produced goods, imported goods, rent, other services; 12.5: food, beverages/tobacco, clothing/footwear, housing-light-fuel, furniture, health, transport, recreation, other; 9.9: sex x age
  - countries: NO
  - years: 12.6: 1969-1992 (24 year rows); 12.5: 1959-1998 (40 rows); 9.9: 1972-1991
  - caveats: Static HTML (scrapable), 1985=100. 12.5 housing group bundles rent with light/fuel. Census-based activity 1875-1990 (selected years, no age detail) in tables 9-1..9-4.
- **https://pxdata.stat.fi/PxWeb/api/v1/en/StatFin_Passiivi/tyti/statfinpas_tyti_pxt_11pl_2020.px (quarterly ..._11c8_2020q4.px 1989Q1-2020Q4; monthly ..._11af_2020m12.px 1989M01-2020M12)** (Statistics Finland PxWeb (StatFin_Passiivi archive)) — 11pl -- Population by labour force status, sex and age, 1989-2020. Verified. Machine-readable.
  - breakdowns: sex x age (15-19, 20-24, 25-29, ... 70-74, 15-24, 15-64, 15-74 etc.) x population, LF, employed, unemployed, inactive, activity rate %, employment rate %, unemployment rate %
  - countries: FI
  - years: 1989-2020
  - caveats: Old-method series; LFS renewed 2021 with new estimation method back-revised only to 2009 (current StatFin tyti 13aj 2009-2025, 137h quarterly, 135y monthly). LFS exists from 1959 but 1959-1988 is not in the API (1959-1975 results in PDF 'Statistical Surveys No. 61', 1978, otos.stat.fi).
- **https://pxdata.stat.fi/PxWeb/api/v1/en/StatFin_Passiivi/khi/statfinpas_khi_pxt_12rf_1983.px (monthly 12rc 1939M08-1983M12; 1914-base 12rh 1921-1983)** (Statistics Finland PxWeb (StatFin_Passiivi archive)) — 12rf -- Cost-of-living index (1938:8-1939:7=100) by commodity, yearly data, 1940-1983. Verified. Machine-readable.
  - breakdowns: total, total excl. taxes/child benefits, 01 food, 03 clothing, 041 dwelling, 0455 heating and lighting, 12 other, taxes
  - countries: FI
  - years: total 1940-1983; food, clothing, dwelling 1940-1967
  - caveats: Cost-of-living concept; commodity detail ends 1967.
- **https://pxdata.stat.fi/PxWeb/api/v1/en/StatFin_Passiivi/khi/statfinpas_khi_pxt_14ta_1986.px (monthly 14t9 1968M01-1986M12)** (Statistics Finland PxWeb (StatFin_Passiivi archive)) — 14ta -- Consumer Price Index, main headings (1967=100, 1972=100, 1977=100, 1981=100), 1967-1986. Verified. Machine-readable.
  - breakdowns: 12 headings incl. 041 dwelling, 045 heating/lighting, 01 food, 03 clothing, 05 furnishings
  - countries: FI
  - years: 1967 base 1967-1978; 1972 base 1972-1977; 1977 base 1977-1982; 1981 base 1981-1986 (no 041 dwelling in 1981 base)
  - caveats: Overlapping base series must be chained; dwelling sub-index missing 1983-1994 in the API (1985/1990-base heading tables not online).
- **https://pxdata.stat.fi/PxWeb/api/v1/en/StatFin/khi/15b5.px ; archive main headings https://pxdata.stat.fi/PxWeb/api/v1/en/StatFin_Passiivi/khi/statfinpas_khi_pxt_11xr_2025.px (2000-2025)** (Statistics Finland PxWeb) — 15b5 -- Consumer Price Index (2025=100) by commodity (ECOICOP v2), monthly 1995M01-2026M08. Verified. Machine-readable.
  - breakdowns: 390 commodity codes incl. 041 actual rentals, 0411 tenants' rentals, 01 food; goods/services flags (ND/SD/D/S) on items
  - countries: FI
  - years: 1995M01-2026M08
  - caveats: Rent index statistics (asvu) only from 2010/2015 in the API.
- **https://api.statbank.dk/v1/data table RAS1 (continued RAS207 2006-2011, RAS201/RAS202 2008-2024, rates RAS1F 1997-2006 and RAS200 2008-2024; RAS33 1980-2005 LF by age 16-17, 18-19, 20-24...)** (Statistics Denmark StatBank API) — RAS1: Population by region, socioeconomic status, ancestry, age and sex (register-based labour force statistics, end-November) 1981-2006. Verified. Machine-readable.
  - breakdowns: socioeconomic status (employed, unemployed, outside LF) x age (under 16, 16-19, 20-24, ..., 60-64, 65-66, 67+) x sex x ancestry x region
  - countries: DK
  - years: 1981-2006 (all cells for national total)
  - caveats: Register-based (RAS), not LFS; participation = (employed+unemployed)/total. Table changes 2006/2008 (RAS201 etc.). LFS (AKU) tables in StatBank only from 1995/1996 (AKU1, AKU100/120 inactive) and 2008 (AKU110A/111A).
- **https://api.statbank.dk/v1/data table NAHC022 (also NAHC023 73 groups 1966-2023; NAHC3 by durability 1966-2025)** (Statistics Denmark StatBank API) — NAHC022: Final consumption of households on the economic territory (44 groups) 1966-2025. Verified. Machine-readable.
  - breakdowns: COICOP groups incl. CP0410 actual rentals for housing, CP0420 imputed rentals, CP0113 food, CP0310 clothing; current prices and 2020 chained prices
  - countries: DK
  - years: 1966-2025
  - caveats: Implicit deflators give rent vs goods-group prices from 1966; NAHC3 durability split (durable/semi-durable/non-durable goods, services) for a goods deflator (metadata only). CPI by commodity group in StatBank only from 2000 (PRIS01/PRIS6); CPI total 1900-2025 (PRIS8).
- **https://api.statbank.dk/v1/data table FAM111N (also FAM133N by household type)** (Statistics Denmark StatBank API) — FAM111N: Children 1 January by region, family type, family size, number of children, sex and age (0-24) 1986-2026. Verified. Machine-readable.
  - breakdowns: single age 0-24 x sex x family type; footnote: children include persons up to age 24 living with at least one parent (never married, no own children, not in a couple)
  - countries: DK
  - years: 1986-2026
  - caveats: Register family statistics; coresidence share for 18-24 = FAM111N count / population (BEFOLK2/FOLK). Cut-off at age 24.
- **https://api.statbank.dk/v1/data table BEFOLK2 (single-year BEFOLK1 1971-2026; HISB4 1901-1970)** (Statistics Denmark StatBank API) — BEFOLK2: Population 1 January by sex and age (5-year groups) 1901-2026. Verified. Machine-readable.
  - breakdowns: sex x 5-year age groups
  - countries: DK
  - years: 1901-2026
  - caveats: Tenure: BOL6 occupants by tenure, age, sex 1981-2006 and BOL201/BOL204 2010-2026; BOLRD occupied dwellings by tenure 1930-2026 (census years before 1980) - metadata only.
- **https://www150.statcan.gc.ca/t1/wds/rest/getDataFromCubePidCoordAndLatestNPeriods productId 14100327 (table 14-10-0327-01); monthly 14-10-0017** (Statistics Canada WDS API) — Labour force characteristics by gender and detailed age group, annual 1976-2025. Verified. Machine-readable.
  - breakdowns: geography (Canada + 10 provinces) x characteristic (population, LF, employment, unemployment, participation rate, ...) x gender x age (15-19, 20-24, 25-29, ..., 60-64, 65-69, 70+ and aggregates)
  - countries: CA
  - years: 1976-2025
  - caveats: 1976 LFS redesign (direct labour-status questions); 2006 processing changes; population rebasings (e.g. 2015 rebase revised to 2001). Excludes territories.
- **https://www150.statcan.gc.ca/n1/pub/11-516-x/sectiond/D205_222-eng.csv (participation rates); D160_174-eng.csv (civilian LF by age/sex 1946-1975); D124_133-eng.csv (LF components 1921-1960); index https://www150.statcan.gc.ca/n1/pub/11-516-x/sectiond/4057750-eng.htm** (Statistics Canada, Historical Statistics of Canada (11-516-X), Section D) — Series D205-222: Civilian labour force participation rates, by age and sex, annual averages, 1946 to 1975. Verified. Machine-readable.
  - breakdowns: sex (total, males, females) x age 14-19, 20-24, 25-44, 45-64, 65+, all ages
  - countries: CA
  - years: 1946-1975
  - caveats: Old LFS (main-activity questionnaire, population 14+); Newfoundland from 1950; excludes Yukon/NWT, Indian reserves, inmates; 1975/76 break (parallel run showed the new questionnaire captured more youth/female employment). Revised 1966-1975 15+ series only in print (CS71-201, publications.gc.ca). Census-date LF 1881-1971 in D1-123.
- **productId 18100005 (table 18-10-0005-01; monthly 18-10-0004-01) coordinates 2.81 rent, 2.80 rented accommodation, 2.274 goods, 2.282 services, 2.2 all-items** (Statistics Canada WDS API) — Consumer Price Index, annual average, not seasonally adjusted. Verified. Machine-readable.
  - breakdowns: geography x 361 products incl. Rent, Rented accommodation, Shelter, Goods, Services, Goods excl. food/energy, All-items
  - countries: CA
  - years: All-items 1914-2025; Rent and Rented accommodation 1949-2025; Goods and Services 1961-2025; Shelter 1979-2025 in this cube
  - caveats: Basket updates; city/province emphasis changed with 1992 basket (1995).
- **https://data.api.abs.gov.au/rest/data/ABS,LF_AGES,1.0.0/M12.1+2.<age>.10.AUS.M (dataflow LF_AGES; LF for totals)** (Australian Bureau of Statistics Data API (SDMX)) — Labour Force: Age Groups (participation rate M12 etc.), monthly from Feb 1978. Verified. Machine-readable.
  - breakdowns: measure (employed, unemployed, LF, NILF, civilian population, participation rate, ...) x sex x age (15-19, 20-24, 25-29 ... 60-64, 65+, aggregates) x original/SA/trend; Australia only
  - countries: AU
  - years: 1978-02 to 2026-08
  - caveats: Survey redesigns 1986, 2001 (telephone interviewing), 2014 etc. backcast by ABS. Annual = average of months.
- **https://www.abs.gov.au/AUSSTATS/abs@.nsf/DetailsPage/6204.0.55.0011966%20to%201984?OpenDocument (data cube 6204055001_02.xls by age and sex; _05.xls participation by age and marital status; _01 by sex and marital status)** (Australian Bureau of Statistics, 6204.0.55.001 Labour Force Historical Timeseries, Australia, 1966 to 1984 (xls)) — Labour Force Historical Timeseries: Labour Force Status by Age and Sex, 1966-1977 (August). Verified. Machine-readable.
  - breakdowns: sheets Men, Married women, All women, Persons x age 15-19, 20-24, 25-34, 35-44, 45-54, 55-59, 60-64, 65+ x employed FT/PT, unemployed, LF, NILF, population, participation rate, E/P
  - countries: AU
  - years: 1966-1977 (August each year); other cubes in the release to 1984
  - caveats: Pre-1978 quarterly-survey design; August reference month only; join to 1978+ monthly series at a design break.
- **https://data.api.abs.gov.au/rest/data/ABS,CPI,2.0.0/1.10001+20003+30014+115522+20001+20002.10.50.Q** (Australian Bureau of Statistics Data API (SDMX)) — Consumer Price Index (CPI), index numbers, weighted average of eight capital cities. Verified. Machine-readable.
  - breakdowns: 166 index codes incl. 10001 all groups, 20003 housing, 30014/115522 rents, 20001 food, 20002 clothing; goods component 104101 only monthly by city from 2024-04
  - countries: AU
  - years: All groups 1948Q3-2026Q2; rents, housing, food, clothing 1972Q3-2026Q2
  - caveats: Long-run goods-component series not in API (only 2024+); use food/clothing groups as goods proxies or ABS 6401.0 spreadsheets.
- **https://www.e-stat.go.jp/en/stat-search/file-download?statInfId=000001082683&fileKind=0 (table 3-2); list https://www.e-stat.go.jp/en/stat-search/files?tclass=000001226526&cycle=0; monthly by age 1-b-5 statInfId=000031897991** (Statistics Bureau of Japan, Labour Force Survey Historical data (Excel via e-Stat files)) — Historical data 3(2): Labour force and labour force participation rate by age (five-year group), annual since 1968. Verified. Machine-readable.
  - breakdowns: sheets both sexes / male / female x age 15-19, 20-24, ..., 60-64, 65+, 65-69, 70-74, 75+, 70+; LF (10k persons) and LFPR %
  - countries: JP
  - years: 1968-2025 (58 years)
  - caveats: Pre-1978 data are compatible series adjusted for the 1967 methodological reform and 1975 benchmark revision; '*' = Okinawa excluded (before 1973); benchmark population revised every 5 years since 1982 and 2020-census rebasing (initially released values kept in separate sheets); 2011 supplementary estimates (earthquake).
- **https://www.e-stat.go.jp/en/stat-search/file-download?statInfId=000001082681&fileKind=0 (table 2-1)** (Statistics Bureau of Japan, Labour Force Survey Historical data (Excel via e-Stat files)) — Historical data 2-1: Major items (LF, employed, unemployed, not in LF by activity, LFPR, employment rate, unemployment rate) since 1953. Verified. Machine-readable.
  - breakdowns: both sexes / male / female x LF status; not in LF split into attending school, housekeeping, other
  - countries: JP
  - years: 1953-2025
  - caveats: No age detail before 1968 in this release; same compatibility adjustments as above.
- **https://api.db.nomics.world/v22/series/STATJP/CPIa (series 282 Rent, 737 Rent less imputed rent, 001 All items, 002 Food, 393 Clothing, 322 Household durable goods, 365 Domestic non-durable goods); official entry https://www.stat.go.jp/english/data/cpi/ -> Historical Data -> e-Stat** (Statistics Bureau of Japan CPI 2020-base historical data (e-Stat database; mirrored by DBnomics STATJP/CPIa)) — Consumer Price Index - Annual Average (2020-base), 78 series. Verified. Machine-readable.
  - breakdowns: item groups incl. rent, rent excl. imputed rent, food, clothing, durable and non-durable goods aggregates
  - countries: JP
  - years: 1970-2025
  - caveats: Verified via the DBnomics mirror; e-Stat API needs a registered appId. 2025-base released Aug 2026. CPI exists from Aug 1946 but item detail before 1970 not located online.
- **dataset LMS: YCAJ/YCAK/YCAL (economic activity rate 18-24 all/male/female, SA); MGWG (activity rate 16+, SA); other age bands (16-17, 25-34, 35-49, 50-64, 65+) in LMS table A05** (Office for National Statistics (ONS) time series (website /data JSON; search via api.beta.ons.gov.uk/v1/search)) — LFS: Economic activity rate by age and sex (Labour market statistics). Verified. Machine-readable.
  - breakdowns: sex x age band; SA/NSA
  - countries: UK
  - years: age bands 1992Q2-2026Q2 (monthly rolling 1992APR-); 16+ total 1971Q1-2026Q2
  - caveats: ONS publishes age x activity only from 1992. LFS was biennial 1973-1983 and annual 1984-1991 (microdata at UK Data Service); NISRA has a Northern Ireland 1984-1991 Excel. Census 1951-1981 economic activity by age in print.
- **MM23: DOBP RPI housing rent (Jan 1987=100); D7CE CPI 04.1 actual rents (2015=100); CHAW RPI all items; CHOF RPI all goods; CHOK RPI other goods. CT: ADUX 04.1.1 actual rentals CP NSA; AWMD 04.1.1 implied deflator** (Office for National Statistics (ONS) time series, datasets MM23 and CT) — RPI/CPI rent and goods indices; Consumer Trends actual rentals. Verified. Machine-readable.
  - breakdowns: rent, all items, goods aggregates; household consumption actual rentals current prices and deflator
  - countries: UK
  - years: DOBP, CHAW, CHOK 1987-2026; D7CE 1988-2026; ADUX 1985-2025; AWMD 1997-2025
  - caveats: Pre-1987 RPI section indices (rent from the late 1940s) are not online as time series; printed in Employment Gazette / 'Retail Prices 1914-1990' (HMSO).
- **https://opendata.cbs.nl/ODataApi/odata/83752NED/TypedDataSet (continued by 85264NED 2013-2026)** (Statistics Netherlands (CBS) OData v3) — 83752NED Arbeidsdeelname, vanaf 1969 (labour participation from 1969). Verified. Machine-readable.
  - breakdowns: sex x person characteristic (age 15-24, 25-44, 45-74; education levels) x topics: population, LF, employed, unemployed, unemployment %, gross participation % (LF/pop), net participation %
  - countries: NL
  - years: 1969-2021 (all 53 years filled)
  - caveats: Reconstructed series: CBS back-cast the old national-definition series to current definitions with an error-correction model (Kosters et al. 2009); intermittent early surveys implied, so early years are model-based; 2021 EBB redesign break; only three broad age bands.
- **https://opendata.cbs.nl/ODataApi/odata/70675ned/TypedDataSet** (Statistics Netherlands (CBS) OData v3) — 70675ned Consumentenprijzen; huurverhoging woningen vanaf 1959. Verified. Machine-readable.
  - breakdowns: Netherlands; average annual rent increase %
  - countries: NL
  - years: 1959-2026
  - caveats: Percent changes (chain to index). CPI by spending category (incl. 04.1 rent, goods/services) only from 1996 (83131NED, 86141NED); all-items CPI 1900-2025 (71905ned) and 1969- (83136NED) - metadata only.
- **https://opendata.cbs.nl/ODataApi/odata/37620/TypedDataSet** (Statistics Netherlands (CBS) OData v3) — 37620 Personen in huishoudens naar leeftijd en geslacht, 1 januari; 1995-2025. Verified. Machine-readable.
  - breakdowns: sex x single year of age x household position (thuiswonend kind = child living at home, single, partner, lone parent, other, institutional)
  - countries: NL
  - years: 1995-2025
  - caveats: Register-based. Earlier: cohort table 82028NED (living situation in parental family, birth cohorts 1950-1980) and OG98 survey (37274) - metadata only.

**Not found or not reachable.**
- Sweden: AKU 1961-1969 (quarterly, 16-64) by age/sex is not in the SCB database; it exists only in printed reports (e.g. SOU 1966:8). Archived microdata are at Riksarkivet. In the API, youth bands start late: 20-24 from 1987, 15-19 from 2001. Before 1970 only census-based activity is available, in print.
- Sweden: the CPI COICOP rent sub-index 04.S.1 is not in the annual table, only monthly from 2005. CPI group indices before 1980 are only in the digitised SOS PDFs (Priser och konsumtion 1910-1994). The rent-change series 1969- is missing 1981.
- Sweden: no 'living with parents' series before the 2011 household register; censuses 1960-1990 are print only.
- Norway: there is no LFS before 1972, so 1950-1971 needs the 1950/1960/1970 censuses (NOS PDFs via ssb.no/a/histstat). The CPI rent index (husleie) is only in the 1969-1992 HTML historical table and from 1979 in the StatBank. The goods aggregate in the StatBank starts in 2000.
- Finland: LFS 1959-1988 is not in the API (a PDF covers 1959-1975). The CPI dwelling/rent sub-index has a gap 1983-1994 because the 1985/1990-base heading tables are not online. Long rent-index (vuokraindeksi) history is not in the API, which has only 2010/2015-.
- Denmark: LFS (AKU) before 1994/95 is not in the StatBank. Register labour status by age starts 1981 (RAS1), and 1950-1980 is census print only. CPI by commodity group starts only in 2000 in the StatBank; rent before then has to come from national-accounts deflators (1966-). Coresidence in FAM111N starts 1986 and stops at age 24.
- Canada: the revised 1966-1975 LFS on a 15+ basis consistent with 1976 is print only (CS71-201). No coresidence/living-with-parents time series in WDS; only census products (98-10-0137 for 2021, earlier censuses 1981-2016 outside WDS).
- Australia: the CPI goods component has no long run in the API (monthly by city from 2024 only). LFS by age before 1966 is census only. Living arrangements by age are census only (SDMX census flows for 2006-2021; earlier via TableBuilder/print).
- Japan: e-Stat API calls need a registered appId (not used). Historical Statistics of Japan pages on stat.go.jp return 404 (moved). No LFS age detail before 1968 online, and CPI item detail before 1970 was not located. Not scouted: coresidence/parasite-single series (census only).
- UK: no ONS series of activity by age before 1992. LFS 1973-1991 survives only as microdata at the UK Data Service, plus an NI-only NISRA 1984-1991 Excel. Pre-1987 RPI rent and section indices are print only.
- Netherlands: the CPI by spending category (rent vs goods) starts in 1996 in OData; only all-items and rent increases (1959-) are longer. The 83752NED participation series has only three broad age bands, and its early years are model-reconstructed. Coresidence by age starts 1995.
- Not scouted in this family: US BLS/Census, Stats NZ, Korea KOSIS (separate scouts or families).

**Access.** All access was Python with truststore. Note that '-I' disables PYTHONIOENCODING, so each script calls sys.stdout.reconfigure(encoding='utf-8') for Nordic and Japanese labels.

Working endpoints:
- SCB PxWeb v1 (GET for metadata, POST json-stat2 for data): https://api.scb.se/OV0104/v1/doris/en/ssd/...
- SCB API v2 has table search with first/last period (GET /tables?query=) and data via GET /tables/{TAB}/data?valueCodes[...]: https://statistikdatabasen.scb.se/api/v2/tables
- SSB PxWebApi v2, same pattern as SCB v2 with numeric table ids: https://data.ssb.no/api/pxwebapi/v2/tables
- SSB historical HTML tables: https://www.ssb.no/a/histstat/tabeller/<n>.html
- Statistics Finland PxWeb v1, including the StatFin_Passiivi archive, which holds the pre-2009 LFS and pre-1995 CPI: https://pxdata.stat.fi/PxWeb/api/v1/en/StatFin(_Passiivi)/...
- Statistics Denmark StatBank: POST https://api.statbank.dk/v1/tableinfo and /v1/data with format JSONSTAT. GET /v1/tables?includeInactive=true lists 5,737 tables with first/latest periods, and inactive tables hold the long history. Variable codes contain non-ASCII letters (OMRÅDE, KØN).
- StatCan WDS: POST getCubeMetadata, getDataFromCubePidCoordAndLatestNPeriods (10-part coordinate) and getAllCubesListLite at https://www150.statcan.gc.ca/t1/wds/rest/. Pre-1976 data are CSVs under /n1/pub/11-516-x/sectiond/.
- ABS SDMX: GET https://data.api.abs.gov.au/rest/dataflow/ABS/{id}?references=all for structure, /rest/availableconstraint/ABS,{id}/all for time range, and /rest/data/ABS,{flow},{ver}/{key} with Accept application/vnd.sdmx.data+json. The 1966-84 LFS xls is at abs.gov.au AUSSTATS subscriber.nsf links.
- Japan: e-Stat file-download?statInfId=...&fileKind=0 (Excel) works without a key. The e-Stat API needs an appId. The CPI was checked via DBnomics api.db.nomics.world/v22/series/STATJP/CPIa.
- ONS: the old time-series API is gone. Find the CDID with https://api.beta.ons.gov.uk/v1/search?q=..&content_type=timeseries, then GET https://www.ons.gov.uk{uri}/data (JSON with years, quarters and months).
- CBS: https://opendata.cbs.nl/ODataApi/odata/{id}/TableInfos, /DataProperties, /{Dimension}, /TypedDataSet?$filter=...; the catalogue is at https://opendata.cbs.nl/ODataCatalog/Tables.

Downloads are under C:\Users\s6068C\AppData\Local\Temp\claude\C--Users-s6068C-GitHub-laborformal\57a37d3a-ed63-4c7d-9808-2133339ff86c\scratchpad\lr_nso\data\ (au/, jp/, uk/ subfolders). Scripts are in ...\lr_nso\code\ (px.py, pxfetch.py, v2meta2.py, v2fetch.py, dst.py, dstfetch.py, sc_meta.py, sc_cov.py, abs_struct.py, abs_data.py, ons_cov.py, cbs_meta.py, cbs_cov.py, cov.py, xlstruct.py).

Blinding: only years, counts and labels were printed. No values were inspected. Some table notes quote break magnitudes (SSB 2021), and these were deliberately not carried over.

## macrohistory

**Best long panel.** Participation by sex and age: this family has no annual country x year panel back to 1950.
- Best decadal option: IPUMS-International census microdata, from which participation by sex and any age band can be computed (along with coresidence via RELATE and tenure via OWNERSHIP). It covers about 21 OECD members in 1960-2000: USA 1960-2000 decennial; FRA 1962/68/75/82/90/99; CHE 1970-2000; CAN, AUT, GRC 1971/81/91; IRL 1971-96; ESP, PRT 1981/91; MEX, CHL, ISR, TUR, and others.
- Best annual or near-annual microdata: LIS, with USA annual from 1963, GBR annual from 1968, CAN from 1971, FRA from 1970, DEU from 1973, SWE from 1975, ITA from 1977, NOR and ISR from 1979, ESP from 1980, AUS from 1981 (1981/85/89/95), CHE from 1982, NLD from 1983. Japan (2008) and Korea (2006) come too late.
- Aggregate participation only: the BoE UK series (total 1856-2016; by sex from 1971) and OWID's female 15+ series (US, CA, DE, GB; census years from 1890-1911, annual from 1960 for the US).

Rents relative to goods (all-items CPI): JST R6, using an implied rent index = housing_rent_yd x house-price level (hpnom, or cumulated housing_capgain for ESP/ITA/PRT), divided by cpi.
- Unbroken 1950-2020 for 13 countries: AUS, CHE, DNK, ESP, FIN, FRA, GBR, ITA, NLD, NOR, PRT, SWE, USA.
- Partial: BEL 1950-2020 with 1965-1975 missing; DEU from 1962; JPN from 1960.
- None for CAN or IRL.
- Pre-1950 starts for these series run from 1870 (FRA, NLD, DEU) to 1948 (PRT).
- Non-European backward holdout from this source: USA 1950-2020, AUS 1950-2020, JPN 1960-2020.
- The same file gives annual unemployment (complete 1950-2020 except IRL from 1960 and PRT from 1953), nominal wages and CPI (complete 1950-2020) for all 18 countries.

- **https://www.macrohistory.net/app/download/9834512569/JSTdatasetR6.xlsx?t=1763503850 (also .dta: https://www.macrohistory.net/app/download/9834512469/JSTdatasetR6.dta?t=1763503850). Variables: housing_rent_yd (rent[t]/price[t]), housing_rent_rtn (rent[t]/price[t-1]), housing_capgain, rent_ipolated (flag). Docs: RORE_documentation.pdf https://www.macrohistory.net/app/download/9834516469/RORE_documentation.pdf?t=1614633099 and JST_RORE_Documentation_R6.pdf https://www.macrohistory.net/app/download/9918957869/JST_RORE_Documentation_R6.pdf?t=1658254098** (Jorda-Schularick-Taylor Macrohistory Database, Release 6 (macrohistory.net); rent side from Jorda, Knoll, Kuvshinov, Schularick and Taylor (2019), 'Rate of Return on Everything' (RORE)) — JST R6 housing rental yield / rental return: an implied rent index, recovered as rent index proportional to housing_rent_yd x house-price level. Verified. Machine-readable.
  - breakdowns: Country x year. There is no separate rent-index variable. A rent index proportional to the true one is recovered as housing_rent_yd x hpnom, or as housing_rent_yd x the cumulated housing_capgain where hpnom starts late (ESP, ITA, PRT). Dividing by JST cpi gives rents relative to the all-items CPI.
  - countries: 16 of the 18 JST countries: AUS, BEL, CHE, DEU, DNK, ESP, FIN, FRA, GBR, ITA, JPN, NLD, NOR, PRT, SWE, USA. CAN and IRL have no housing returns at all. Outside Europe this covers USA, AUS and JPN.
  - years: File spans 1870-2020. housing_rent_yd starts per country: FRA, NLD, DEU 1870; DNK 1875; NOR 1871; SWE 1883; BEL, USA 1890; GBR 1895; ESP 1900; AUS, CHE 1901; FIN 1920; ITA 1927; JPN 1931; PRT 1948. All end 2020. Complete every year 1950-2020 for AUS, CHE, DNK, ESP, FIN, FRA, GBR, ITA, NLD, NOR, PRT, SWE, USA. Gaps: BEL 1965-1975 missing; DEU missing 1950-1961, so usable 1962-2020; JPN missing 1950-1959, so usable 1960-2020.
  - caveats: Rent indices come from Knoll's unpublished 2017 PhD thesis. They mostly use the rent component of national cost-of-living or CPI indices, spliced with city or other sources before WWII (per-country sources in RORE_documentation.pdf, section 2.4, pp. 30-47). The rent-price ratio is anchored to a benchmark year (2012-2014) and extrapolated back. In some countries rent-index growth was scaled by a multiplicative factor, or benchmarked to historical yield estimates, so the implied rent index is adjusted, not raw. Housing includes owner-occupied dwellings and imputed rents. Years flagged by rent_ipolated (BEL 1965-75; JPN 1945-59; also ESP 1937-38 and SWE 1915) are blank in the yield series. AUS has a documented structural break in 1949/50, when wartime price controls were lifted. For 2016-2020 R6 extended the series with the rent-price approach, using OECD house prices and national rent CPIs (sources in R6 doc Table 3). Coverage only was inspected; no values were read.
- **Same file, variable hpnom (nominal house price index, 1990=100). Docs: NPLH_documentation.pdf https://www.macrohistory.net/app/download/9834516269/NPLH_documentation.pdf?t=1763503850** (JST Macrohistory Database R6 (house prices from Knoll-Schularick-Steger 2017, extended)) — JST R6 nominal house price index (hpnom). Verified. Machine-readable.
  - breakdowns: Country x year; national index
  - countries: 18: AUS, BEL, CAN, CHE, DEU, DNK, ESP, FIN, FRA, GBR, IRL, ITA, JPN, NLD, NOR, PRT, SWE, USA
  - years: Starts: AUS, DEU, FRA, NLD, NOR 1870; DNK, SWE 1875; BEL 1878; USA 1890; GBR 1899; CHE 1901; FIN 1905; JPN 1913; CAN 1921; IRL 1945; ITA 1970; ESP 1971; PRT 1988. All end 2020. Since 1950 there are gaps in CAN (1950-55 missing), DEU (1950-61 missing), ITA (starts 1970), ESP (starts 1971) and PRT (starts 1988).
  - caveats: Each country splices several indices of differing quality: existing vs new dwellings, urban vs national, hedonic vs median/mean, and construction-cost proxies in some periods. NPLH documentation (171 pp.) gives source tables per country and structural-break tests (Table 3). For ESP, ITA and PRT a longer price-growth series exists in housing_capgain (from 1901, 1928 and 1932).
- **Same file, variable cpi (consumer prices, index 1990=100). Per-country sources: JST_documentationR6.pdf https://www.macrohistory.net/app/download/9834516169/JST_documentationR6.pdf?t=1676279836** (JST Macrohistory Database R6) — JST R6 consumer price index (all items). Verified. Machine-readable.
  - breakdowns: Country x year; headline, all items only
  - countries: 18 (as above)
  - years: 1870-2020 for 17 countries; IRL from 1922. No missing years 1950-2020 in any country.
  - caveats: All-items CPI, which includes rents. There is no goods-only or ex-housing CPI, so the result is 'rents relative to all items', not 'rents relative to goods'. Pre-war values are cost-of-living indices.
- **Same file, variable unemp (unemployment rate, percent)** (JST Macrohistory Database R6 (from Gabriel 2021, long-run Phillips-curve data)) — JST R6 unemployment rate. Verified. Machine-readable.
  - breakdowns: Country x year; total only, no sex or age
  - countries: 18
  - years: Starts: GBR, NLD 1870; DNK 1874; DEU 1887; USA 1890; FRA 1895; AUS 1901; NOR 1904; SWE 1911; CHE 1913; CAN 1916; ITA 1919; FIN 1920; BEL 1921; JPN 1930; ESP 1933; PRT 1953; IRL 1960. All end 2020. Complete 1950-2020 except IRL (from 1960) and PRT (from 1953).
  - caveats: The definition changes over time. Before the wars the series measures union or insured unemployment, assuming its growth tracks national growth. Recent years use LFS-based rates (CPS, EU-LFS via ILOSTAT), supplemented by NSOs. The date of the switch differs by country (e.g. AUS uses Mitchell table B2 up to the ILOSTAT period starting 1981). Details are in the Gabriel (2021) online appendix.
- **Same file, variable wage (nominal wage index, 1990=100)** (JST Macrohistory Database R6 (from Gabriel 2021)) — JST R6 nominal wage index. Verified. Machine-readable.
  - breakdowns: Country x year; average earnings of all employees where possible
  - countries: 18
  - years: 1870-2020 for most countries (BEL 1870 with gaps; ITA from 1871; IRL from 1943). No missing years 1950-2020 in any country.
  - caveats: Early years may rest on sector-specific series. Recent years come from the IMF and OECD wage indices. JST also has total population (pop, 1870-2020, IRL from 1921), but nothing by age.
- **openICPSR project 113055, https://www.openicpsr.org/openicpsr/project/113055/version/V1/view (DOI 10.3886/E113055V1)** (Knoll, Schularick and Steger (2017), 'No Price Like Home: Global House Prices, 1870-2012', AER 107(2)) — NPLH replication data: house prices, construction costs, land prices. Not verified. Machine-readable.
  - breakdowns: Country x year; house price, construction cost and (for 6 countries) residential land price indices
  - countries: 14: AUS, BEL, CAN, CHE, DEU, DNK, FIN, FRA, GBR, JPN, NLD, NOR, SWE, USA
  - years: 1870-2012
  - caveats: The openICPSR download needs a free login, so it was not fetched. The house-price series are already inside JST hpnom, extended to 2020. Knoll's rent indices are not in this package.
- **https://www.bankofengland.co.uk/-/media/boe/files/statistics/research-datasets/a-millennium-of-macroeconomic-data-for-the-uk.xlsx; sheet 'A50. Employment & unemployment' (also Q6 quarterly, M5 monthly administrative unemployment)** (Bank of England, 'A millennium of macroeconomic data for the UK' (version 3.1, Excel)) — UK labour market quantities 1855-2016: workforce/participation, by sex from 1971. Verified. Machine-readable.
  - breakdowns: Total workforce/participation (persons). Census-based economically active women (16+ and 15+) in 1951-1971 census years. LFS series by sex from 1971 (ONS codes MGSA/MGSB, MGSD/MGSE, MGSI; claimant count by sex, DPAA/DPAB, from 1939). No age bands.
  - countries: United Kingdom (UK incl. S. Ireland 1855-1920)
  - years: Total workforce/participation 1856-2016. Official mid-year working population and participation 1950-1972. Workforce jobs 1959-2016. LFS by sex 1971-2016. Census female activity 1951-1971 (census years).
  - caveats: Splices Feinstein, Boyer-Hatton, Economic Trends and ONS data. There are break-adjusted and break-retained variants (the 1920 S. Ireland break). A note flags a possible +1% mean break around 1977 in one series. The workbook is a 27 MB archive, last updated with data to 2016, and is not maintained.
- **Same workbook; sheets 'A32. Property prices & rent' and 'A47. Wages and prices'** (Bank of England, 'A millennium of macroeconomic data for the UK' (v3.1)) — UK house prices, rent indices, CPI and earnings. Verified. Machine-readable.
  - breakdowns: A32 has house price indices: Knoll et al. 1899-2013; Holmans 1934-2002; Nationwide 1953-2016; Halifax 1983-2016; ONS 2002-2016; composite 1847-2016. It also has three rent series: Holmans house rents 1874-1913, rent and rates 1914-1939, and registered regulated private rents in England and Wales 1966-2000. A47 has a composite CPI (1209-2016), an RPI-based index and average weekly earnings.
  - countries: United Kingdom (England/GB for early years)
  - years: 1209-2016 (sheet-dependent; see breakdowns)
  - caveats: There is no continuous UK rent index for 1940-1965 in this workbook: the 1966-2000 series covers regulated tenancies only. The JST implied rent series for GBR is the continuous alternative. The CPI is all items.
- **https://ourworldindata.org/grapher/female-labor-force-participation-long-run.csv?v=1&csvType=full&useColumnShortNames=true (metadata: same path with .metadata.json). The slug female-labor-force-participation-oecd serves identical content. Column female_labor_force_participation.** (Our World in Data grapher (Killingsworth and Heckman 1986, which compiles Long 1958 and ILO Yearbooks; plus ILOSTAT national estimates via World Bank WDI)) — Female labor force participation rate, long run. Verified. Machine-readable.
  - breakdowns: Women of working age (15+; 14+ in some pre-1960 points; 12+ for GB 1921). Female only, no age bands.
  - countries: 4: United States, Canada, Germany, United Kingdom
  - years: USA: census years 1890-1950, annual 1960-2025. CAN: census years 1911-1971, then annual 1976-2025. DEU: 1895, 1907, 1925, 1939, 1946, 1950, 1960, 1970, 1981, then annual 1983-2025. GBR: 1921, 1931, 1951, 1961, 1966, 1971, then annual 1978-2025 (1982 missing). Last updated 2026-02-17.
  - caveats: The splice switches source at the K-H end year (CAN 1951, DEU 1981, GBR 1951, USA 1950); ILOSTAT is kept wherever both exist. Territory changes: GBR is Great Britain to 1951; DEU uses post-WWI borders to 1925 and West Germany (without Berlin) from 1939. The early US census figures undercount married women's work. OWID's standard chart female-labor-force-participation-rates is ILO modelled data, 1990-2025 only (200 entities).
- **https://docs.iza.org/dp9659.pdf; https://www.nber.org/system/files/working_papers/w21887/w21887.pdf (no data file found; Annual Reviews supplement page returned 403)** (Olivetti and Petrongolo (2016), 'The Evolution of Gender Gaps in Industrialized Countries', Annual Review of Economics 8:405-434 (IZA DP 9659, NBER w21887); data per Olivetti (2014) NBER chapter c12892) — Female employment-to-population ratio, 19 high-income countries, 1850-2008. Not verified. Not machine-readable.
  - breakdowns: Women 15+ employed / female population 15+. No age bands. Post-1970 hours by gender come from other sources (EU KLEMS, IPUMS-I).
  - countries: 19: AUS, AUT, BEL, CAN, DNK, FIN, FRA, DEU, GRC, IRL, ITA, JPN, NLD, NOR, PRT, ESP, SWE, GBR, USA
  - years: 1850s-2008 (BEL, FRA, NLD, UK from the 1850s; most countries from 1900; GRC and JPN from 1920)
  - caveats: Pre-WWII figures come from Mitchell's International Historical Statistics (US from Goldin 1990, Table 2.1), spliced to ILO post-war data. The authors call it imperfect but as harmonised as possible. Only figures are published, so the series would have to be rebuilt from Mitchell and ILO.
- **https://clio-infra.eu/data/AverageYearsofEducation_Compact.xlsx ; https://clio-infra.eu/data/GenderEqualityYearsofEducation_Compact.xlsx** (Clio-Infra (clio-infra.eu)) — Average years of education, and gender equality in years of education. Verified. Machine-readable.
  - breakdowns: Country x year. Total population (average years); a female/male ratio for 24 countries. No age bands.
  - countries: 138 countries for average years, including all current OECD members (CZE, SVK, EST, LVA, LTU only from 1950/1960). The gender-equality file covers 24 countries, including AUS, CAN, FRA, DEU, ITA, JPN, MEX, NLD, POL, ESP, SWE, TUR, GBR, USA.
  - years: Average years 1820-2010; after 1945 only 1950, 1960, ..., 2010. Gender equality 1950-2000, decadal.
  - caveats: A stock measure, not enrolment. Too coarse for cyclical schooling tests. Clio-Infra has no participation, rent, tenure, coresidence or age-structure series.
- **https://clio-infra.eu/data/Inflation_Compact.xlsx ; https://clio-infra.eu/data/LabourersRealWage_Compact.xlsx** (Clio-Infra (clio-infra.eu)) — Inflation (CPI-based) and labourers' real wage. Verified. Machine-readable.
  - breakdowns: Country x year; all-items inflation; real wage of unskilled or building labourers
  - countries: Inflation: 175 countries, including all OECD members (CZE, SVK, SVN, EST, LVA, LTU only from the 1990s). Real wage: 126 countries with uneven OECD coverage.
  - years: Inflation 1500-2010; for most OECD members 1950-2010 is complete or nearly so. Real wages 1820-2008, uneven after 1950 (e.g. FRA has only 2 obs after 1950, ESP ends 1973, NLD ends 1983).
  - caveats: All-items CPI only, ending 2010. Real wages are occupation-specific and patchy after 1950. For the 18 JST countries, the JST cpi and wage series are better.
- **https://raw.githubusercontent.com/barrolee/BarroLeeDataSet/master/LeeLee/LeeLee_v1.dta (also LeeLee_enroll_F.xls, _M.xls, _MF.xls; sources in LeeLee_enroll_source.pdf)** (Lee and Lee (2016), 'Human Capital in the Long Run', J. Development Economics 122 (Barro-Lee site / GitHub)) — Long-run school enrolment ratios and attainment, by sex. Verified. Machine-readable.
  - breakdowns: sex (MF, F, M); enrolment ratios pri, sec, ter; attainment shares lu, lp, lpc, ls, lsc, lh, lhc; years of schooling tyr, pyr, syr, hyr; human capital hc, hca; pop. Attainment files also exist for ages 15-24, 15-64 and 25-64.
  - countries: 111, including AUS, CAN, JPN, KOR, NZL, USA, MEX, CHL, TUR, ISL, CHE, NOR, GBR and most of Europe
  - years: Enrolment 1820-2010; attainment 1870-2010
  - caveats: Enrolment ratios are estimated and interpolated from census and survey benchmarks. 5-yearly data cannot show year-to-year cyclicality, but they can serve as a trend control.
- **https://raw.githubusercontent.com/barrolee/BarroLeeDataSet/master/BLData/BL_v3_F.csv (also _M, _MF; v2.2 files BL2013_F_v2.2.csv with 5-year age groups)** (Barro and Lee educational attainment dataset, v3 (GitHub barrolee/BarroLeeDataSet)) — Educational attainment by sex and age group, 1950-2015. Verified. Machine-readable.
  - breakdowns: Sex; ages 15-24, 25-34, 35-44, 45-54, 55-64 (v3; v2.2 has 5-year groups); attainment shares and years of schooling by level; pop
  - countries: 146
  - years: 1950-2015
  - caveats: Measures the stock of attainment, not current enrolment. The barrolee.com HTTPS certificate does not match its hostname; use plain http or GitHub.
- **Subscription product on Springer Link (formerly palgraveconnect); tables export as ePDF or Excel for subscribers only** (Mitchell, International Historical Statistics 1750-2010 (Palgrave Macmillan / Springer Link)) — International Historical Statistics: population by sex and age; labour force (economically active population by sex and industry, census years); unemployment; wages; prices. Not verified. Not machine-readable.
  - breakdowns: Regional volumes (Europe; Americas; Africa, Asia and Oceania). Chapters A Population (incl. sex and age at censuses) and B Labour Force (B1 economically active by sex and industry; B2 unemployment; wages).
  - countries: Worldwide
  - years: 1750-2010 (print 6th ed. to 2005)
  - caveats: Not free. Confirmed as a subscription product from library catalogues. The online edition has not been updated since about 2013. It is the source behind the Olivetti-Petrongolo and JST pre-war series.
- **Sample list: https://international.ipums.org/international-action/samples ; variable availability: https://international.ipums.org/international-action/variables/{RELATE|OWNERSHIP|LABFORCE|EMPSTAT|SCHOOL}. Extracts via the IPUMS API (collection 'ipumsi', supported) with a free registration and API key.** (IPUMS International (Minnesota Population Center)) — Harmonised census microdata: coresidence (RELATE), tenure (OWNERSHIP), labour force (LABFORCE/EMPSTAT), school attendance (SCHOOL), by AGE and SEX. Not verified. Machine-readable.
  - breakdowns: Person-level microdata (any age band, sex, relationship to head, tenure, activity, school attendance). No public summary tables; only the variable-availability and codes pages are open.
  - countries: OECD samples 1945-2000: AUT 1971/81/91; CAN 1971/81/91; CHL 1960/70/82/92; COL 1964/73/85/93; CRI 1963/73/84/2000; FRA 1962/68/75/82/90/99; DEU 1970/71/81/87; GRC 1971/81/91; HUN 1970/80/90; IRL 1971/79/81/86/91/96; ISR 1972/83/95; MEX 1960/70/90/95/2000; NLD 1960/71; POL 1978/88; PRT 1981/91; SVK 1991; ESP 1981/91; CHE 1970/80/90/2000; TUR 1985/90/2000; GBR 1961/71/91; USA 1960/70/80/90/2000. Not in IPUMS-I: AUS, NZL, JPN, KOR, BEL, NOR, SWE, DNK, FIN, ITA (before 2001).
  - years: 1960-2000 for OECD members; also 19th-century samples and 2000s-2020 samples (incl. ESP and ITA LFS)
  - caveats: Variables vary by sample (OECD samples, 1945-2000). RELATE is missing for GBR 1961/71, DEU 1971/81/87 and POL 1988. LABFORCE/EMPSTAT are missing for DEU 1971/81, HUN 1970/80, NLD, POL and GBR 1961/71. OWNERSHIP is missing for AUT 1971, CAN 1971, NLD and SVK. SCHOOL covers fewer samples. Samples are 1-10% of the census. Activity definitions follow each census. Microdata were not fetched because registration is needed.
- **Dataset list: https://www.lisdatacenter.org/our-data/lis-database/ ; variables: https://www.lisdatacenter.org/wp-content/uploads/files/data-lis-variables.pdf ; remote execution via LISSY (registration: https://www.lisdatacenter.org/data-access/lissy/)** (Luxembourg Income Study (LIS) Database) — Harmonised household-survey microdata: age, sex, lfs (labour force status), relation (to household reference person), own (main residence tenure), enroll (enrolled in education). Not verified. Machine-readable.
  - breakdowns: Microdata, run remotely through LISSY; only aggregate output is returned. Public Key Figures cover inequality and poverty only, not participation or coresidence.
  - countries: Pre-1997 datasets: USA annual from 1963; GBR annual from 1968; CAN 1971, 73, 75, 77, 79, 81, 82, 84-; FRA 1970, 75, 79, 84, 90, 96-; DEU 1973, 78, 83-; SWE 1975, 81, 84-; ITA 1977-; ISR 1979, 86, 92; NOR 1979, 86, 91, 95; ESP 1980, 85, 90, 93-; AUS 1981, 85, 89, 95; CHE 1982, 92; NLD 1983, 87, 90, 93; MEX 1984, 89, 92, 94, 96; BEL 1985, 88, 92, 95; LUX 1985-; DNK 1987, 92, 95; FIN 1987, 91, 95; IRL 1987, 94-96; POL 1986, 92, 95; HUN 1991, 94; CZE 1992, 96; SVK 1992, 96; AUT 1994-; GRC 1995. JPN only from 2008, KOR from 2006, no NZL.
  - years: 1963-2024 (income reference years)
  - caveats: Free registration is needed for LISSY. Underlying surveys change within countries (e.g. US CPS-ASEC; UK FES/FRS). Variable availability varies by dataset. Only the variable list was checked; the contents_combined_LIS.xlsx matrix documents income variables only.
- **GESIS study ZA8673, DOI 10.4232/1.12995 (https://search.gesis.org/research_data/ZA8673); histat topic 'Bauen'** (Kohl (2017/2018), 'Homeownership, Renting and Society: Historical and Comparative Perspectives, 1920 (1950)-2015', GESIS Data Archive / histat) — Homeownership rates, raw census-date points and linearly interpolated series. Not verified. Machine-readable.
  - breakdowns: Country x year; homeownership rate under 5 definitions (unit-, household-, population-, property-based, private property)
  - countries: Many OECD and non-OECD countries (146 time series)
  - years: Raw points from about 1920 (most from 1950) to 2015; interpolated series 1900-2015
  - caveats: Not fetched: GESIS histat downloads may need a free login. The raw data change definition between censuses, and the interpolated series are linear and therefore unusable for annual variation.
- **https://journaldata.zbw.eu/dataset/57308aec-c23a-4cce-aee2-bafb75c96d83/resource/6d3826b7-f27a-4616-a804-f7a27bd3745a (behind an Anubis bot-protection challenge; not fetched)** (ILO, 'Economically Active Population 1950-2010', 4th ed. (1996-97, vols I-IV); third-party Excel extract by Victor Gay on ZBW Journal Data Archive) — Population and economically active population by sex and age group, 1950-2010 (ILO Table 4). Not verified. Machine-readable.
  - breakdowns: Sex x 5-year age groups (ILO original)
  - countries: ILO original: all countries with more than 200,000 inhabitants in 1990; the Gay extract's coverage is unknown
  - years: ILO original: 1950, 1960, 1970, 1980, 1990 estimates, with projections to 2010. ZBW metadata reportedly lists only 1950 and 1960 as temporal coverage.
  - caveats: This is a lead, not a verified source. The values are ILO model estimates, not observations. It probably overlaps the ILO family's scope, so route it there. Open the link in a normal browser to inspect it; the bot challenge was not bypassed.

**Not found or not reachable.**
- JST R6 has no published rent index: rents exist only as rental yield/return (housing_rent_yd, housing_rent_rtn), with an index implied through house prices. Knoll's (2017) raw rent indices are in an unpublished PhD thesis.
- JST R6 has no housing return or rent data for Canada or Ireland. Canada is the one non-European JST country without rents.
- No source in this family has a goods-only (ex-housing) CPI back to 1950. JST, Clio-Infra and BoE give all-items CPI only.
- No source in this family has an annual panel of participation by sex and age band before about 1970. The annual or decadal options are census microdata (IPUMS-I, LIS) and the UK-only BoE LFS series from 1971.
- The OWID long-run female participation series covers only 4 countries (US, CA, DE, GB), women 15+ only, with no age bands.
- Olivetti-Petrongolo (2016) series: no public data file found. The Annual Reviews supplement page returned 403, and the working papers contain figures only.
- Mitchell's International Historical Statistics is subscription-only (Springer/Palgrave) and was not accessed.
- Japan, Korea, Australia and New Zealand are absent from IPUMS-I. In LIS, Japan starts 2008, Korea 2006 and Australia 1981; NZ is absent.
- IPUMS-I and LIS microdata were not fetched because they need registration (IPUMS API key; LISSY account). Neither publishes summary tables of participation or coresidence by age.
- Clio-Infra has no labour-force participation, rent, housing tenure, coresidence or population-by-age series. Its CPI and education series end in 2010.
- The ILO 1950-2010 EAPEP (4th ed.) Excel extract on journaldata.zbw.eu was not fetched because the site sits behind Anubis bot protection.
- Kohl homeownership (GESIS ZA8673) and the KSS openICPSR package were not fetched because they need a login.
- The BoE millennium workbook has no continuous UK rent index for 1940-1965; the 1966-2000 series covers regulated tenancies only. Its data end in 2016 (v3.1, not updated).

**Access.** Everything was fetched with the corporate-proxy recipe (truststore, then requests, UA 'Mozilla/5.0 (research; laborformal)'). Note that python -I also ignores PYTHONIOENCODING, so scripts call sys.stdout.reconfigure(encoding='utf-8') to print PDF text on Windows.

Downloaded under C:\Users\s6068C\AppData\Local\Temp\claude\C--Users-s6068C-GitHub-laborformal\57a37d3a-ed63-4c7d-9808-2133339ff86c\scratchpad\lr_macrohist\data\:
- JSTdatasetR6.xlsx; JST_documentationR6.pdf, JST_RORE_Documentation_R6.pdf, RORE_documentation.pdf, NPLH_documentation.pdf (macrohistory.net links redirect to sfff5b3ac9317c4be.jimcontent.com and download without login)
- boe_millennium.xlsx (27 MB)
- owid\*.csv and *.metadata.json
- clio\*.xlsx (wide format, year columns 1500-2050)
- LeeLee_v1.dta and BL_v3_F.csv (via raw.githubusercontent.com/barrolee/BarroLeeDataSet; barrolee.com over https fails on a certificate hostname mismatch)
- OP2016 working-paper PDFs (IZA, NBER)
- IPUMS-I sample and variable-availability HTML pages (public)
- LIS dataset list HTML, data-lis-variables.pdf and contents_combined_LIS.xlsx (income variables only)

Scripts are in the sibling code\ folder: get.py, jst_cov.py, boe_sheets.py, boe_cov.py, owid_cov.py, clio_cov.py, ipumsi_samples.py, ipumsi_var.py, ipumsi_avail.py, pdfgrep.py, links.py. All of them print coverage only (columns, first and last years, counts, missing years), never values.

Blocked or gated:
- journaldata.zbw.eu: Anubis proof-of-work bot challenge, also on its CKAN API. Not bypassed; open it in a browser.
- annualreviews.org: 403.
- openICPSR (KSS 113055): login.
- GESIS histat (ZA8673): JS app, likely login.
- IPUMS-I: registration plus API key. ipumspy and the IPUMS API v2 support collection 'ipumsi'.
- LIS: LISSY account.
- Mitchell IHS: subscription.

Blinding: the OWID metadata and web-search summaries returned some numeric snippets. They were not used or recorded, and no values from fetched files were read.

## household_hist

**Best long panel.** This family has no participation or rent/goods series; those come from other families. What it supplies is the conditioning 'floor availability' variable, and its longest usable panels are listed below.

**(a) Cross-country, person-level: IPUMS-I census microdata.** The 18-34 or 20-29 share living with a parent (RELATE child of head) can be built at census-round frequency.
- Start years: US 1960, NL 1960, MX 1960, CL 1960, FR 1962, CR 1963, CO 1964; CH 1970, DE-West 1970, HU 1970, AT 1971, CA 1971, GR 1971, IE 1971, IL 1972.
- That gives 15 OECD countries by 1975 (8 European) and 21 by 1996, roughly decennial to 2011-2020.
- The MOMLOC-based any-parent variant gives 13 countries by 1975.
- A predetermined baseline taken from the c.1960-1975 round would serve a 1976-1996 holdout. For a test starting in 1950, only time-invariant measures are predetermined.

**(b) Time-invariant, predetermined:**
- Giuliano–Nunn ancestral family organisation: all 38 OECD, machine-readable.
- Reher (1998) classification: about 15-20 countries, hand-coded.

**(c) Annual national series:**
- US AD-1: 1960, 1970, 1980 census anchors, then annual 1983-2025.
- Japan: LFS September tabulation 1980-2016 (PDF); IPSS headship rates by age 1955-2020 (census years).
- Canada: census 1981-2021 (2011+ machine-readable).
- Australia: census 1981-2006 (PDF).

**(d) Modern Europe:**
- EU-SILC ilc_lvps08: 2003/2005-2025 for 30+ countries, by sex and age bands.
- yth_demo_030 (leaving-home age): 2000-2025 for 11 countries from 2000.
- Census cens_01nhtype: 2001 for 30 countries.

- **https://international.ipums.org/international-action/samples ; variables RELATE (https://international.ipums.org/international-action/variables/RELATE), MOMLOC/POPLOC (https://international.ipums.org/international-action/variables/MOMLOC)** (IPUMS-International (Minnesota Population Center), census microdata) — Harmonised census microdata; young-adult coresidence derivable as child-of-head (RELATE) or any coresident parent (MOMLOC/POPLOC>0). Not verified. Machine-readable.
  - breakdowns: Person level: single-year age, sex, marital status, school attendance, labour-force status, relationship to head, parent pointers; any age band (e.g. 18-24, 20-29, 25-34) can be built
  - countries: 29 OECD members have some sample. RELATE in a 1950-1996 sample: 21 (AT, CA, CL, CO, CR, FR, DE, GR, HU, IE, IL, MX, NL, PL, PT, SK, ES, CH, TR, GB, US). MOMLOC in 1950-1996: 18 (no CA, NL or SK). Not in IPUMS-I modern censuses: AU, BE, CZ, EE, JP, KR, LV, LT, LU, NZ. DK, IS, NO and SE have only pre-1911 historical samples; FI has 2010 only; IT has 2001+
  - years: OECD samples from 1960; RELATE by 1964: 7 (CL 1960, CO 1964, CR 1963, FR 1962, MX 1960, NL 1960, US 1960); by 1975: 15 (adds AT 1971, CA 1971, DE-West 1970, GR 1971, HU 1970, IE 1971, IL 1972, CH 1970). MOMLOC by 1975: 13 (AT, CL, CO, CR, FR 1962, DE-East 1971, GR, HU, IE, IL, MX, CH, US 1960). Roughly decennial to 2011-2020
  - caveats: Variable availability differs by sample. GB 1961/1971 have no RELATE (only 1991, 2001). CA 1971-2001 have no MOMLOC. DE: 1970 and 1987 are West, 1971 and 1981 are East. RELATE 'child' misses young adults whose coresident parent is not the head. Treatment of students away from home differs between censuses. Microdata need a free account and an approved application; this scout did not register (no account creation), so only public availability pages were fetched. The online tabulator also needs a login
- **https://www.un.org/development/desa/pd/sites/www.un.org.development.desa.pd/files/undesa_pd_2026_hh-size-composition.xlsx (2022 ed.: .../undesa_pd_2022_hh-size-composition.xlsx; page https://www.un.org/development/desa/pd/data/household-size-and-composition)** (UN DESA Population Division) — Database on Household Size and Composition 2026 (and 2022). Verified. Machine-readable.
  - breakdowns: Household level only, no person-level young-adult coresidence: household size; age of head (<20, 20-64, 60+, 65+); basic types (one-person, couple only, couple with children, single parent, extended family, non-relatives); intergenerational (nuclear, multi-generation, three-generation, skip-generation)
  - countries: About 200 countries; 36 of 38 OECD members (DK and SE absent). Extended-family share available by 1965: 1 OECD country (US); by 1975: 9 (AT, CL, CO, CR, GR, HU, IL, MX, US); by 1996: 14 (adds ES, GB, IE, PT, TR). Multi-generation available by 1996: 12
  - years: Reference dates 1960-2024 (OECD pre-1997 points all come from IPUMS-I censuses)
  - caveats: Mixes sources (IPUMS, DYB, EU-LFS 2001/2011, DHS, MICS), so definitions shift between source types. Several IPUMS samples lack type detail (FR, CH and HU 1980/1990 have no household types). EU-LFS rows have no type indicators. The 2026 file stores numbers as text, and its column layout differs from the 2022 file
- **https://www2.census.gov/programs-surveys/demo/tables/families/time-series/adults/ad1.xls** (US Census Bureau) — Table AD-1. Young Adults, 18-34 Years Old, Living At Home: 1960 to Present. Verified. Machine-readable.
  - breakdowns: Age 18-24 and 25-34, by sex (men, women); total, child of householder, percent
  - countries: US
  - years: 1960, 1970, 1980 (decennial census); 1981-2025 (CPS March/ASEC). For 1981-1982 only totals are shown; child-of-householder and percent are N/A
  - caveats: Census points (1960-1980) vs CPS points (1981+) are different sources. In CPS, unmarried college students in dorms count as living in the parental home. Revised 2011 and 2021 rows reflect population controls; 2014 ASEC redesign; 2025 vintage note
- **https://www2.census.gov/programs-surveys/decennial/tables/time-series/coh-ownerchar/ownerchar-{1950,1960,1970,1980,1990,2000}.txt** (US Census Bureau, Historical Census of Housing Tables) — Homeownership rates by selected characteristics, including age of householder (under 35, 65+). Verified. Machine-readable.
  - breakdowns: US and states; age of householder under 35 and 65 and over; units in structure; 1-person households; recent movers
  - countries: US (and states)
  - years: 1950-2000 decennial; the under-35 householder column is available only for 1980, 1990 and 2000 (marked '...' for 1950-1970)
  - caveats: Plain-text tables. Under-35 band only
- **https://www.census.gov/housing/hvs/data/histtab19.xlsx ; annual tables histtab12.xlsx / histtab15.xlsx (1982-)** (US Census Bureau, CPS/Housing Vacancy Survey) — Table 19. Quarterly Homeownership Rates by Age of Householder: 1994 to Present (Tables 12/15 annual by age, 1982-). Verified. Machine-readable.
  - breakdowns: Age of householder: under 35, 35-44, 45-54, 55-64, 65+
  - countries: US
  - years: T19: 1994Q1-2026; T12/T15: 1982- (listed, not fetched)
  - caveats: Data for October 2025 were not collected (funding lapse). Vintage population revisions
- **Table 98-10-0137-01 (WDS productId 98100137)** (Statistics Canada) — Census family status and household living arrangements, presence of parent in household, age group and gender. Verified. Machine-readable.
  - breakdowns: Ages 20-34, 20-24, 25-29, 30-34; gender (total, men+, women+); living with at least one parent or not; family status; 166 geographies
  - countries: CA (provinces, CMAs)
  - years: Census 2011, 2016, 2021
  - caveats: 2021 concept counts young adults in skip-generation families living with a grandparent; the concept was reapplied to 2011 and 2016. 2021 uses gender (earlier rounds used sex)
- **https://www150.statcan.gc.ca/n1/pub/75-006-x/2016001/article/14639-eng.htm** (Statistics Canada, Insights on Canadian Society 75-006-X (Milan 2016)) — Diversity of young adults living with their parents (census trend chart). Not verified. Not machine-readable.
  - breakdowns: Ages 20-29, 20-24, 25-29; by sex in several charts
  - countries: CA
  - years: Censuses 1981, 1986, 1991, 1996, 2001, 2006, 2011 (NHS)
  - caveats: HTML chart data tables only. Defined as son or daughter of the economic-family reference person; 2011 is the NHS, not the census. For a pre-1981 point use IPUMS-I CA 1971 (RELATE only)
- **https://www.ipss.go.jp/syoushika/tohkei/Data/Popular2025/T07-25.files/sheet001.htm (chapter index https://www.ipss.go.jp/syoushika/tohkei/Popular/Popular2025.asp?chap=7)** (National Institute of Population and Social Security Research (IPSS), Japan, Population Statistics 2025 (from census)) — Table 7-25: Headship rates (ordinary households) by sex and 5-year age group, 1955-2020. Verified. Machine-readable.
  - breakdowns: Sex by 5-year age group
  - countries: JP
  - years: 1955, 1965, 1970, 1980, 1990, 1995, 2000, 2005, 2010, 2015, 2020
  - caveats: Household-formation (headship) measure, not direct coresidence with parents. 1955 and 1965 are sample tabulations. 'Ordinary household' concept. HTML or Excel export
- **https://www.ipss.go.jp/syoushika/tohkei/Data/Popular2025/T06-24.files/sheet001.htm** (IPSS Japan, Population Statistics 2025) — Table 6-24: Population by sex, 5-year age and marital status (share never married), 1920-2020. Verified. Machine-readable.
  - breakdowns: Sex by 5-year age; never married (other statuses on further sheets)
  - countries: JP
  - years: 1920, 1930, 1950, 1960, 1970, 1980, 1990, 2000, 2010, 2015, 2020
  - caveats: Marital status is a household-formation proxy only
- **English summary: https://www.stat.go.jp/training/english/reseach/parasite_eng.pdf ; Japanese 2016 update formerly at https://www.stat.go.jp/training/2kenkyu/pdf/parasi16.pdf (now returns 404)** (Statistical Research and Training Institute, MIC Japan (F. Nishi; Nishi and Kan)) — Never-married persons living with parents ('parasite singles'): Labour Force Survey special tabulation. Not verified. Not machine-readable.
  - breakdowns: Ages 20-34 and 35-44; never married and living with parent(s); by labour status; sex in the Japanese reports
  - countries: JP
  - years: September of each year, 1980-2004 (summary); the Japanese reports extend to 2016
  - caveats: PDF tables only. Counts never-married persons only (married coresidents excluded). Only the English summary was fetched; the data tables were not
- **https://www.e-stat.go.jp (census tables: relationship to household head by sex and age)** (Statistics Bureau of Japan, Population Census (e-Stat statistics code 00200521)) — Persons in general households by relationship to household head, sex and age (child of head). Not verified. Not machine-readable.
  - breakdowns: Relationship categories differ by round (1985: only head vs non-head; 2010 and 2020: 12 categories including child, by 5-year age)
  - countries: JP
  - years: Per census round; no harmonised time series found. 2000-2015 'living with parents' comparison is in 2015 final-results PDFs
  - caveats: The e-Stat API needs an appId (registration), so it was not accessed. Category changes across rounds
- **https://www.abs.gov.au/AUSSTATS/abs@.nsf/Lookup/4102.0Main+Features50June+2009 (PDF https://www.ausstats.abs.gov.au/ausstats/subscriber.nsf/LookupAttach/4102.0Publication30.06.096/$File/41020_Homeandaway.pdf); 1994 edition covers 1981-1991** (Australian Bureau of Statistics, Australian Social Trends 4102.0) — Home and away: the living arrangements of young people (census-based). Not verified. Not machine-readable.
  - breakdowns: Ages 20-34 (also 18-34, 20-24, 25-29, 30-34); by sex
  - countries: AU
  - years: Census 1981, 1986, 1991 (1994 edition), up to 2006 (2009 edition); later censuses via TableBuilder (registration)
  - caveats: Census includes non-private dwellings (residential colleges); identified via relationship to household reference person. Article PDFs only. The AIFS fact sheet (aifs.gov.au) returned 403
- **https://webfs.oecd.org/Els-com/Affordable_Housing_Database/HM1-4-Living-arrangements-age-groups.xlsx** (OECD Affordable Housing Database) — HM1.4.2 Living arrangements of youth (20-29): with parents, alone, single parent, partnered, with other youth/adults. Verified. Machine-readable.
  - breakdowns: Age 20-29; no sex split in HM1.4.2 (living-alone sheets by age and gender)
  - countries: About 38 OECD and EU countries (incl. KR, CA, US, AU, NZ, CL, MX, CO, CR; no JP or IL)
  - years: Cross-section: 2024 or latest (2020-2024). Annex A1 (living alone by age) covers 2010-2024
  - caveats: Mixed survey sources (EU-SILC, HILDA, CIS, CASEN, KLIPS, ...). Not predetermined for a pre-1997 test
- **https://webfs.oecd.org/Els-com/Affordable_Housing_Database/HM1-3-Housing-tenures.xlsx (sheets HM1.3.4, HM1.3.A6)** (OECD Affordable Housing Database) — Housing tenure by age group (15-29, 30-49, 50-64, 65+). Verified. Machine-readable.
  - breakdowns: Own outright, own with mortgage, rent (private, subsidised), other; by age group
  - countries: About 40 (OECD plus EU non-members)
  - years: 2010-2024
  - caveats: Post-1996 only. Rent categories are pooled for several countries
- **https://webfs.oecd.org/Els-com/Family_Database/SF_1_1_Family_size_and_composition.xlsx (index https://www.oecd.org/en/data/datasets/oecd-family-database.html)** (OECD Family Database) — SF1.1 Family size and household composition (no young-adults-living-with-parents indicator in any SF table). Verified. Machine-readable.
  - breakdowns: Household types and average size by type; households by number of children
  - countries: OECD plus partners
  - years: Cross-sections 2021 and 2024
  - caveats: SF series do not cover young adults' coresidence; the indicator sits in the Affordable Housing DB (HM1.4)
- **ilc_lvps08 (also ilc_lvps09 by economic status, ilc_lvps10 by contract)** (Eurostat (EU-SILC)) — Share of young adults aged 18-34 living with their parents (current label: 'Persons living with their parents or contributing/benefiting from the household income'). Verified. Machine-readable.
  - breakdowns: Ages 16-19, 16-24, 16-29, 18-24, 18-34, 20-24, 20-29, 25-29, 25-34; sex T/M/F
  - countries: EU27 plus IS, NO, CH, UK, ME, MK, AL, RS, TR, XK (46 geos)
  - years: 2003-2025 (first year: 2003 for 7 geos, 2004 for 8, 2005 for 15; UK 2005-2018; TR 2006-)
  - caveats: The label wording changed. EU-SILC 2020/2021 methodological changes; check flags. Nothing before 2003
- **yth_demo_030** (Eurostat (EU-LFS based)) — Estimated average age of young persons leaving the parental household. Verified. Machine-readable.
  - breakdowns: Sex T/M/F
  - countries: 36 geos (EU27, NO, UK, TR, MK, RS, ME, BA)
  - years: 2000-2025 (11 geos start 2000: BE, CY, DE, EE, EL, ES, HU, LU, NL, PT, UK; DK from 2010, SE from 2009, NO from 2021)
  - caveats: Model-estimated from coresidence shares by age. Not before 2000
- **cens_01nhtype (also cens_01nhhst, cens_01rhtype NUTS3)** (Eurostat, 2001 census round) — Population by sex, age and household status (incl. 'child living with at least one parent'). Verified. Machine-readable.
  - breakdowns: Single years and 5-year age groups; sex; household status (married, consensual union, lone parent, child with parent(s), alone, institutional)
  - countries: 30 (EU25 minus SE and MT, plus BG, RO, IS, LI, NO, CH, TR)
  - years: 2001 only
  - caveats: The earliest Eurostat person-level household-status-by-age table. It ends the 1950-1996 window, so it is not predetermined
- **cens_91hpnper, cens_91hnnch (1991); cens_hndwsize (1991, 2001)** (Eurostat, 1991 census round and historical selection) — Household composition by size; family nuclei by number of children; households by size. Verified. Machine-readable.
  - breakdowns: Household size (1 to 7+ persons) or number of children; no age-of-member or household-status-by-age table in the 1991 round
  - countries: cens_91hpnper: 19 countries (EU15 plus CH, LI, NO); cens_hndwsize: 29
  - years: 1991 (and 2001)
  - caveats: Household size only, so a weak proxy. No 1981 household tables (cens_hnmga 1981 is population by sex and age only)
- **ilc_lvho03h, ilc_lvho04h (also ilc_mdes05h, ilc_di07h, ilc_li06h)** (Eurostat, ECHP-era aggregates) — Average rooms per person by tenure status and dwelling type, and by household type (until 2001). Verified. Machine-readable.
  - breakdowns: Tenure (owner, tenant, reduced/free rent); household types incl. one adult under 30
  - countries: EU15 (AT from 1995, FI from 1996, SE from 1997)
  - years: 1994-2001
  - caveats: These are the only ECHP-based aggregates on Eurostat. None covers young adults living with parents. Microdata (ECHP UDB) need a research contract
- **demo_pjanmarsta** (Eurostat demography) — Population on 1 January by age, sex and legal marital status. Verified. Machine-readable.
  - breakdowns: Single year of age, sex, marital status
  - countries: 46 geos, but early coverage is sparse (at single age 25: HU from 1960, IS 1971, NO 1972, RO 1981, FX 1983; most others 1990s or later)
  - years: 1960-2025
  - caveats: Marital-status proxy for household formation only
- **https://www.un.org/development/desa/pd/sites/www.un.org.development.desa.pd/files/undesa_pd_2019_wmd_marital_status.xlsx** (UN DESA Population Division) — World Marriage Data 2019 (marital status by age and sex; SMAM). Verified. Machine-readable.
  - breakdowns: 5-year age groups by sex; never, currently and ever married; singulate mean age at marriage
  - countries: All countries; for 20-24/25-29: 30 OECD members by 1975, 37 overall (EE from 2000)
  - years: 1970-2019 (no OECD observation before 1970 in this edition)
  - caveats: Proxy only: marriage timing is not coresidence. Consensual-union treatment varies
- **https://unstats.un.org/unsd/demographic/products/dyb/dyb_Household/5.xls (page .../dyb_Household/dyb_household.htm)** (UN Statistics Division, Demographic Yearbook household tabulations) — Table 5: Population in households by relation to head of household, age and sex: 1995-2013. Verified. Machine-readable.
  - breakdowns: Relation to head (head, spouse, child, child's spouse, grandchild, parent, other relative, domestic, unrelated) by age and sex
  - countries: 65 countries; 23 OECD (only IL 1995 is pre-1997)
  - years: Censuses 1995-2013
  - caveats: The file is XML Spreadsheet 2003 despite the .xls extension. UNdata census datamart also starts with the 1995 round
- **https://unstats.un.org/unsd/demographic-social/products/dyb/dybsets/1987%20DYB.pdf (about 55 MB; also 1971/1976 DYB PDFs about 45-51 MB)** (UN Statistics Division, Demographic Yearbook 1987 (special topic: household characteristics)) — DYB 1987 special-topic tables: population by marital status and household composition (censuses c.1975-1986). Not verified. Not machine-readable.
  - breakdowns: Household composition tables (exact relationship-by-age content not confirmed)
  - countries: Reporting countries (unknown count)
  - years: Census round c.1975-1986
  - caveats: Scanned PDF, not downloaded (size). Content not confirmed
- **EB 28.1 1987 ZA2041 (doi:10.4232/1.10898); 1990 EB 34.2 (doi:10.4232/1.10894); EB 47.2OVR 1997 ZA2938 (doi:10.4232/1.10928); first youth study Dec 1982; EB 55.1 2001** (European Commission, Eurobarometer 'Young Europeans' youth surveys (GESIS)) — Young Europeans (youth samples aged 15-24). Not verified. Machine-readable.
  - breakdowns: Ages 15-24; sex; living situation (whether a 'living with parents' item exists in each wave is not confirmed)
  - countries: EC-10 (1982), EC-12 (1987, 1990), EU-15 (1997, 2001); about 600 interviews per country
  - years: 1982, 1987, 1990, 1997, 2001
  - caveats: Age band stops at 24. GESIS download needs registration (not done). Codebooks are needed to confirm the coresidence item
- **SHARE waves 3 (2008-09) and 7 (2017): https://share-eric.eu ; ESS3 2006 'Timing of life' module: https://www.europeansocialsurvey.org ; FFS (UNECE, 23 countries 1989-1999); GGS wave 1 (2002-2013)** (Retrospective life-history surveys (SHARELIFE; ESS round 3; UNECE FFS; GGS wave 1)) — Age or year left the parental home (cohort-based reconstruction of home-leaving back to the 1930s-1960s). Not verified. Machine-readable.
  - breakdowns: Birth cohort, sex, age at leaving home, reason (varies by survey)
  - countries: SHARELIFE w3: about 13 (AT, DE, SE, NL, ES, IT, FR, DK, GR, CH, BE, CZ, PL) plus w7 additions; ESS3: about 25 European; FFS: 23 ECE-region incl. US, CA, NZ; GGS about 19
  - years: Recall covers home-leaving roughly 1930s-2000s depending on survey
  - caveats: Recall bias. Not period measures. All require registration (not done). Exact variable names not verified
- **https://www.lisdatacenter.org (LISSY remote access) ; EU-LFS microdata via Eurostat research contract** (Luxembourg Income Study (LIS) and EU-LFS microdata) — Household microdata with relationship to head (young adults coresiding with parents derivable). Not verified. Machine-readable.
  - breakdowns: Person level: age, sex, labour status, relationship
  - countries: LIS: about 20+ OECD with datasets from the late 1960s-1980s (exact list not retrieved; the site's country page is JS-rendered); EU-LFS: EC members from 1983
  - years: LIS from about 1967-1985 depending on country; EU-LFS 1983-
  - caveats: Both need registration or accreditation (not done). Whether EU-LFS household-relationship variables exist pre-1998 for each country is unconfirmed
- **doi:10.2307/2807972** (Reher, D.S. (1998), 'Family ties in Western Europe: persistent contrasts', Population and Development Review 24(2): 203-234) — Strong vs weak family-ties classification (historical, regional). Not verified. Not machine-readable.
  - breakdowns: Country or regional grouping (qualitative, ordinal)
  - countries: Western Europe (Mediterranean, Scandinavia, British Isles, Low Countries, Germany/Austria) and North America; no formal score table
  - years: Predetermined (historical patterns; published 1998)
  - caveats: Not machine-readable; must be hand-coded from the article. Groupings are deliberately not reported here (blinding)
- **https://www.anderson.ucla.edu/documents/sites/faculty/review%20publications/research/Ancestral_Characteristics_Database_Complete_Version_1_1.xlsx** (Giuliano and Nunn (2018), Ancestral Characteristics of Modern Populations, Economic History of Developing Regions 33(1)) — Ancestry-weighted Ethnographic Atlas traits by country, incl. v8 domestic organisation (family type: nuclear vs small or large extended) and v12 marital residence. Verified. Machine-readable.
  - breakdowns: Share of ancestral population in each category (v8_grp1-9, v12_grp1-11, ...); three variants (Baseline; Eastern Europe/Siberia extensions)
  - countries: About 211 countries; all 38 OECD members have v8 values
  - years: Pre-industrial (fully predetermined)
  - caveats: Ethnographic coding is distant from modern young-adult coresidence. European countries rest on few Atlas societies plus language mapping; check the paper's construction
- **https://www.worldvaluessurvey.org ; EVS 1981 via GESIS ; Alesina and Giuliano (2010) J. Econ. Growth** (Integrated Values Surveys (EVS/WVS) wave 1, as used by Alesina and Giuliano (family-ties index)) — Family-ties items (importance of family; respect and love for parents; parents' duties to children). Not verified. Machine-readable.
  - breakdowns: Individual responses; age and sex
  - countries: Wave 1 (1981-84) about 24 countries (EVS 1981 Western Europe plus WVS w1 incl. US, CA, AU, JP, KR, MX, FI, HU)
  - years: 1981-84 first wave; later waves to 2022
  - caveats: Attitudes, not behaviour. Item availability in wave 1 is not verified. Download needs registration (not done)

**Not found or not reachable.**
- No cross-country young-adult coresidence measure for 1950-1959 was found. The earliest OECD census microdata with a relationship variable start in 1960 (US, MX, CL, NL; FR 1962). Before that, IPUMS-I has only historical samples to 1911 (CA, DK, IS, IE, NO, SE, GB, US); US 1940/1950 exist only in IPUMS-USA (registration).
- Eurostat has no table on young adults living with parents before 2003 (ilc_lvps08) or 2000 (yth_demo_030).
- The 1991 census-round tables (cens_91*) have no household-status-by-age table. The earliest such Eurostat table is cens_01nhtype (2001).
- ECHP 1994-2001 aggregates on Eurostat cover only income, poverty, rooms and arrears (ilc_*h). None covers living with parents. ECHP UDB microdata need a research contract.
- OECD Family Database: no SF indicator on young adults living with parents. The OECD indicator is Affordable Housing DB HM1.4.2, a single latest-year cross-section (2020-2024) with no history.
- UN DYB and UNdata census datasets on relationship to head by age start with the 1995 census round. The pre-1995 equivalent exists only in scanned DYB PDFs (1987 special topic), about 55 MB, not downloaded.
- IPUMS-I has no modern census samples for AU, BE, CZ, EE, JP, KR, LV, LT, LU or NZ. It has none for DK, NO, SE or IS after 1911, FI only 2010, IT only 2001+. GB 1961/1971 samples lack RELATE. CA 1971-2001 lack MOMLOC.
- The UN Household Size and Composition DB omits DK and SE entirely.
- Registration-gated sources were not accessed (account creation is outside this scout's permissions): IPUMS-I and IPUMS-USA extracts and SDA tabulator, LIS/LISSY, ESS, SHARE, GGS, FFS, Eurobarometer and EVS (GESIS), WVS, ABS TableBuilder, e-Stat API (appId).
- Japan SRTI 'parasite single' 2016 report (stat.go.jp/training/2kenkyu/pdf/parasi16.pdf) now returns 404; only the 2006 English summary PDF was retrievable.
- AIFS Australia 'young people living with parents' fact sheet returned HTTP 403.
- Korea: census relationship-to-head tables for 1960-1990 appear only in scanned KOSTAT library reports. No KOSIS time series was found.
- US decennial homeownership by age of householder: the under-35 column is not available for 1950, 1960 or 1970.

**Access.** The corporate TLS proxy worked with truststore. Scripts are in C:\Users\s6068C\AppData\Local\Temp\claude\C--Users-s6068C-GitHub-laborformal\57a37d3a-ed63-4c7d-9808-2133339ff86c\scratchpad\lr_coresidence\code\ and downloads are in ...\lr_coresidence\data\. Nothing was written to the repo.

**Endpoints that worked:**
- Eurostat dissemination API (JSON-stat, …/statistics/1.0/data/{code}?format=JSON) and the TOC txt.
- UN DESA xlsx files, OECD webfs xlsx files, census.gov xls/xlsx/txt files.
- Statistics Canada WDS (POST getCubeMetadata and getDataFromCubePidCoordAndLatestNPeriods).
- IPSS HTML sheets (cp932 encoding).
- Public IPUMS-I samples and variable-availability pages.
- The Giuliano–Nunn xlsx.

**File-format quirks:**
- UN DYB '5.xls' is XML Spreadsheet 2003 with ss: namespaces.
- The UN HH 2026 file stores numbers as text and has a different column layout from 2022.

**Blinding log:**
- A structure dump printed one non-OECD row (Afghanistan) of the 2026 UN HH file, because its numbers are stored as text. No OECD-country values were seen by this scout.
- WebSearch summaries volunteered a few headline coresidence/ownership figures for Canada, Japan and Australia without being asked. They are not reproduced or used here. Flag them in the pre-registration if the orchestrating model shares context with the scout.
- No values, levels, trends or country groupings appear in this report. Reher's groupings are deliberately not listed.

**Answer to the key question (earliest predetermined cross-country 'floor availability' measure):**
- **Earliest and widest: the c.1960-1975 census round in IPUMS-I.** A person-level share of 18-34 or 20-29 living with a parent can be built from it.
  - With the RELATE child-of-head definition: 7 OECD countries by 1964 (CL, CO, CR, FR, MX, NL, US) and 15 by 1975 (AT, CA, CL, CO, CR, FR, DE-West, GR, HU, IE, IL, MX, NL, CH, US). Eight of these are European. The count reaches 21 by 1996.
  - With the stricter MOMLOC/POPLOC any-parent pointer: 2 by 1965 (FR, US), 13 by 1975, 18 by 1996.
  - Access requires IPUMS registration and an approved application, which the researcher must do.
- **Published, no registration: household-level proxies only.**
  - UN HH database extended-family household share: 1 OECD country by 1965, 9 by 1975, 14 by 1996.
  - UN World Marriage Data never-married shares: 30 OECD countries by 1975, none before 1970.
- **Fully predetermined, time-invariant, all 38 OECD:** Giuliano–Nunn ancestral family organisation (machine-readable).
- **Hand-coded:** Reher (1998) North/South classification, about 15-20 Western European and North American countries.

**Country-specific long series (not cross-country):**
- US: censuses 1960, 1970, 1980, then annual CPS from 1983.
- Japan: headship rates from 1955; never-married shares from 1920; LFS coresidence of never-married 20-34 from 1980.
- Canada: censuses 1981-2011 plus IPUMS 1971.
- Australia: censuses 1981-2006 (PDF).
