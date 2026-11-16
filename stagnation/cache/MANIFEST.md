# cache/ — raw series as pulled, never edited

| File | Source | Pulled | Notes |
|---|---|---|---|
| `OPHNFB.csv` (removed 2026-11-16) | FRED OPHNFB, copied from `../paths/cache/OPHNFB.csv` (SHA-256 d42ef61a…) | copied 2026-11-16 | superseded the same day by the dated pull `fred/OPHNFB.csv` (fred/MANIFEST.csv), identical through 2019; the file is in git history at 444ce78 |
| `oecd/pdb_raw.csv` | OECD Productivity database, dataflow `OECD.SDD.TPS,DSD_PDB@DF_PDB,2.0`, key `.A.GDPHRS+HRSTO._T...N..`, 1990–2024, SDMX csvfilewithlabels (`https://sdmx.oecd.org/public/rest/data/...`) | 2026-11-16 | GDP per hour worked (USD at constant PPPs, chain-linked volume rebased 2020, and other variants) and total hours worked (millions); SHA-256 c839b8ae…. The older levels dataflow `DSD_PDB@DF_PDB_LV,1.0` answers only on the archive endpoint (HTTP 500 on the public one), so the live `DF_PDB` 2.0 is used |
| `oecd/pop_raw.csv` | OECD Historical population data, `OECD.ELS.SAE,DSD_POPULATION@DF_POP_HIST,1.0`, key `.POP.._T.Y15T64.`, 1990–2024 | 2026-11-16 | population aged 15–64, persons, historical; SHA-256 6343e323… |
| `pwt/pwt110.xlsx` | Penn World Table 11.0 (Feenstra, Inklaar and Timmer; Groningen Growth and Development Centre), Dataverse doi:10.34894/FABVLR, file id 554105 | 2026-11-16 | released 2025-10-10; avh, emp, pop to 2023; SHA-256 7b337e94… |
| `fred/*.csv` | FRED graph endpoint, one file per series | 2026-11-16 | see `fred/MANIFEST.csv`: pull time, rows, first and last dates, SHA-256 |
