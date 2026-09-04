# three-drivers — data support for the blog post "What do we do if many people aren't working?"

Blog-support thread (napkin grade: judgment calls allowed but visible; numbers still primary-source
only). The post argues that placements/apprenticeships in automated-but-vital fields need a way to
estimate "true" value beyond market prices, balanced against two other drivers. This folder holds
the first data pass behind that argument.

**The three drivers, operationalized (US, coarse 15-sector napkin):**

1. **Market pull** — share of the 2024 wage bill (BLS QCEW): where the market pays people now.
2. **Crisis value** — how many of seven standing risk / essential-service lists name the sector
   (NSM-22, NATO, Finland, UK NRR 2025, Sweden MSB NRSB 2025, Lloyd's RDS 2026, WEF GRR 2026):
   where planners and insurers say the stakes live.
3. **People pull** — share of bachelor's degrees by field (NCES 322.10, 2021-22): where people
   actually go.

Plus the majors→jobs match question (do people end up working in what they trained for):
NSCG 2023 relatedness + NY Fed underemployment by major.

## What the napkin shows

- The paradox-of-value corner is real and populated: **water** is on 6 of 7 crisis lists but is
  0.2% of the wage bill and ~0% of degrees; **energy** is on all 7 at 1.4% of wages; **food &
  agriculture** 6 of 7 at 1.4% of wages — and the few agriculture majors are the **5th most
  underemployed major** (57% in jobs not requiring the degree).
- The opposite corner too: **retail & leisure** (1 list) carries 16.6% of wages and 26.2% of
  jobs; **professional services** (1 list) 15.3% of wages. **Media & arts** shows people-pull
  excess: 8.7% of degrees against 2.5% of wages and 3 lists.
- **Health & care** is the aligned case — high on all three — proof the drivers *can* line up.
- Baseline for "people work in their field": 53.7% of employed graduates say closely related
  (NSCG 2023); median underemployment across majors 42.9% (NY Fed).

## Files

```
three-drivers/
├── README.md            this file
├── STATE.md             thread state; start here next session
├── DATA_NOTES.md        sources, access record, failures, judgment layers, headline numbers
├── code/
│   ├── build_risk_lists.py     seven lists → data/risk_lists.csv (190 items; sector_map = judgment)
│   ├── build_majors_match.py   NSCG 1-3 + NY Fed by-major → tidy CSVs + headlines
│   ├── build_three_drivers.py  QCEW + lists + NCES → data/three_drivers.csv
│   └── fig_three_drivers.py    the two figures
├── data/
│   ├── raw/                    vendored source files (PDFs, xlsx, csv)
│   ├── risk_lists.csv          the seven lists, structured
│   ├── majors_match_nscg.csv   job-degree relatedness by field & level
│   ├── majors_match_nyfed.csv  74 majors: under/unemployment, wages
│   └── three_drivers.csv       the napkin: 15 sectors × three drivers
└── figures/
    ├── fig_drivers_scatter.png          crisis value vs market pull, bubble = degrees
    └── fig_majors_underemployment.png   best/worst-matched majors, essential feeders marked
```

Reproduce: `../venv/Scripts/python.exe code/<script>.py` from this folder, in the order listed
(only `build_three_drivers.py` depends on `build_risk_lists.py`'s output).
