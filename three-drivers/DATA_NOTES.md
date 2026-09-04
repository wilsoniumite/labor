# DATA_NOTES — three-drivers (blog-support thread)

All pulls 2026-08-14, from this machine (not the container). Raw source files vendored in
`data/raw/`. Napkin-grade thread: judgment calls are allowed but must be visible; every number
still comes from a primary source; nothing approximated or remembered.

## Sources

| File (data/raw/) | Source | URL | Notes |
|---|---|---|---|
| `nyfed_outcomes_by_major.csv` | NY Fed, The Labor Market for Recent College Graduates, outcomes by major | newyorkfed.org/medialibrary/research/interactives/data/college-labor-market/college-labor-outcomes-by-major-data.csv | endpoint pattern from the-link-revision pass; 74 majors; underemployment = employed grads in jobs not typically requiring a degree (their O*NET-based definition). Page states by-major table updates each February; we record access date only. |
| `nscg23_tab1-3.xlsx` | NSF NCSES, NSCG 2023, Table 1-3 (nsf25322) | ncses.nsf.gov/pubs/nsf25322/... | self-reported relationship of job to highest degree: closely / somewhat / not related. 'S' cells = suppressed → NaN. Components sum to totals (<0.5% tolerance, asserted). |
| `uk_nrr_2025.pdf` | UK Cabinet Office, National Risk Register 2025 (2025-01-16) | assets.publishing.service.gov.uk/media/67b5f85732b2aab18314bbe4/National_Risk_Register_2025.pdf | 187 pp. Document states **89 risks in 9 themes**; the contents pages and a page-title sweep of pp.27–186 both yield **88** titled risk summaries. Recorded 88; the one-risk gap is unresolved and left as stated. |
| `msb_nrsb_2025.pdf` | MSB, Nationell risk- och sårbarhetsbedömning 2025 (MSB2560, feb 2025) | rib.msb.se/filer/pdf/31068.pdf | 26 särskilt allvarliga hot och risker, Tabell 1 p.27; table transcribed by column (layout verified against category counts 2+5+6+4+5+4=26). English translations ours. |
| `lloyds_rds_2026.pdf` | Lloyd's, RDS Scenario Specification, January 2026 | assets.lloyds.com/... (see build script) | 20 compulsory scenarios incl. Alternatives A&B (§1.2.1) + syndicate-specific de minimis set; cyber sub-scenarios from §17 headings (Business Blackout II, Cloud Cascade, Ransomware Contagion). Political-risks detail is a separate on-request document — names only here. |
| `wef_gr_2026.pdf` | WEF, Global Risks Report 2026 (2026-01-14) | reports.weforum.org/docs/WEF_Global_Risks_Report_2026.pdf | top-10 by severity, 2y and 10y horizons, Figure 3 p.9, transcribed verbatim. Perception survey — weakest evidentiary class of the seven, included as the "what elites worry about" instrument. |
| `qcew_2024_us000.csv` | BLS QCEW open-data API, annual 2024, US000 all industries | data.bls.gov/cew/data/api/2024/a/area/US000.csv | UI-covered employment & wages. Total covered 2024: 155.0M jobs, $11.71T wages (validated against agglvl 10/own 0 row). |
| `nces_322_10.xlsx` | NCES Digest of Education Statistics, table 322.10 (d23 edition) | nces.ed.gov/programs/digest/d23/tables/xls/tabn322.10.xlsx | bachelor's degrees by field, latest column 2021-22 (total 2,015,035). d24 edition 404s (tried first). Field labels carry footnote markers, stripped in code; fn.3: Engineering technologies includes construction trades and mechanic/repair. |

Web-page sources (no file): NSM-22 sector list (bidenwhitehouse.archives.gov, fetched 2026-08-14 —
CISA's own sector page returns 403 to non-browser agents; NSM-22 is the primary designation
anyway); NATO baseline requirements (nato.int topic 132722); Finland vital functions
(turvallisuuskomitea.fi). Exact item texts as fetched are frozen in `code/build_risk_lists.py`.

## Access failures (reported, not substituted)

- CISA critical-infrastructure-sectors page: HTTP 403 (bot blocking). Replaced by NSM-22, the
  primary source of the designation.
- NCES d24 tables: 404 for tabn322.10 → used d23 (2021-22 latest year).
- WEF press-release URL: 404 → full report PDF used instead.
- git-bash curl hit TLS errors (exit 35) on several .gov/.se hosts from this machine;
  PowerShell `Invoke-WebRequest` succeeded everywhere. All vendored files came via PowerShell
  or the one successful curl (NY Fed).

## Judgment layers (napkin quality — the open part)

1. `sector_map` in `risk_lists.csv`: our mapping of each list item to the 15-sector napkin set;
   `cross_cutting` items (nat-cat scenarios, "societal polarization", …) are excluded from
   sector tallies. Lives entirely in `code/build_risk_lists.py`.
2. QCEW sector compositions (signed NAICS pieces) in `code/build_three_drivers.py`; covers
   99.8% of the total wage bill. Known undercounts stated in the script header: no active-duty
   military (~1.3M, defense), UI-noncovered self-employed farmers (food & ag) — both
   *strengthen* the napkin's contrast rather than create it.
3. NCES degree fields → sectors with fractional weights; 16.6% of degrees deliberately left
   `unmapped` (humanities, social sciences, liberal arts, interdisciplinary) rather than
   force-fitted. Weights sum to 1 per field, asserted; fields sum to the table total, asserted.
4. Figure 2's `ESSENTIAL` major set (majors feeding 6-7-list sectors): coarse, in the figure
   script, in the open.

## Figure palette

dataviz reference palette slots 1–2 (#2a78d6 blue, #eb6834 orange) in the skill's documented
passing order (adjacent CVD ΔE 9.1 light; first three slots pass all-pairs). Node was not
available on this machine to re-run the validator; usage stays within the combinations the
palette file itself documents as validated. Chrome/ink hexes likewise from the reference file.

## Headline numbers (as built)

- NSCG 2023: 56.1M employed graduates — **53.7% closely related / 27.1% somewhat / 19.1% not
  related** to their degree. Bachelor's-highest only: 43.6 / 31.1 / **25.3%**.
- NY Fed by-major: median underemployment across 74 majors **42.9%**; Agriculture **57.1%**
  (5th worst); Criminal Justice worst at 65.8%; Nursing best at 12.8%.
- Three drivers (2024 wages / 2024-26 lists / 2021-22 degrees): water 6/7 lists, 0.2% of wage
  bill, ~0.0% of degrees; energy 7/7, 1.4%, 1.8%; food & ag 6/7, 1.4%, 2.0%; retail & leisure
  1/7, 16.6% of wages, 26.2% of jobs; professional services 1/7, 15.3% of wages.
