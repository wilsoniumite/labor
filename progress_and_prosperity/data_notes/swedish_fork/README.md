# The Swedish fork (data note, 2026-08-26)

The deflator fork rebuilt on Swedish primary data, originally data item four of the
revision thread (moved here 2026-09-04). Run `../../../venv/Scripts/python.exe swedish_fork.py`
from this folder; the SCB PXWeb responses are cached in `cache/`.

**Object.** The deflator fork (paper Figure 3) rebuilt on Swedish primary data for
the SEB talk: manual-worker hourly pay deflated by machine-made-goods CPI members
and by housing CPI members.

**Sources (all SCB PXWeb API; table titles verified at pull time; JSON responses
cached under `cache/`):**
1. `PR0101A/KPI2020COICOPM` — CPI by COICOP, all levels, 2020=100, monthly
   1980M01–2026M07 (members pulled: 00, 04, 04.1, 05, 08.1).
2. `PR0101DE/KPI2020SA1MA` — CPI special aggregates: **VV = durable goods** (the
   U.S. durables-CPI analog), monthly 1980M01–.
3. `PR0101G/KPIF2020COICOPM` — CPIF (fixed interest rate) by COICOP: member 04,
   monthly 1987M01–.
4. `AM0101A/LonArb07Privat` — KLP hourly earnings, manual workers private sector,
   all industry (B–S excl O), incl. overtime, monthly 2008M01–.
5. `AM0103A/SLP9a07` — SLP hourly pay by industry: B+C, pay for time worked
   (AM0103K8), annual 2008–2025.
6. `AM0103D/SLP11a` — SLP historical: mining+manufacturing manual workers, pay for
   time worked, annual 1952–2013.

**Validation.** Six table titles OK; per-series windows in the ledger; sanity
anchors at 2023 all OK (loose bands, wrong-pull catchers only); published-value
check: computed 2022 annual KPI inflation 0.084 vs the published ≈8.4% — OK.
**Overlap gate** (the no-splice rule): SLP9a07(B+C, pay for time worked) /
SLP11a = 1.0000 in every overlap year 2008–2013 → one series across a publication
seam, long wage member accepted, modern table used from 2008.

**Method.** Monthly series annualized over complete calendar years only; legs =
wage ÷ CPI-member, indexed 1980 = 100; every contestable choice a labeled member
(3 machine × 3 housing × 2 wage).

**Results (1980=100, through 2025).** Paycheck ×6.5; durables (VV) ×1.3; rents
(04.1) ×7.4; housing incl. energy (04) ×5.6. Legs at 2025: durables 498, rents
88, housing 117. **Fork 5.67× vs rents, 4.26× vs broad housing** (U.S.: 4.8×).
Since 1995: durables leg ×4.06, rent leg ×1.34. ICT member (08.1) ×276 by 2025 —
in the CSV, off the chart.

**Caveats.** (i) Use-value rent regulation → the rent index understates market
scarcity (queues and owner prices carry it); 5.67 is a lower bound on the
market-rent fork. (ii) KPI's 04 carries owners' mortgage-interest costs →
rate-sensitive (2022–24 visible); the CPIF-04 member strips it. (iii) Hedonics on
the machine legs, extreme for 08.1. (iv) COICOP 2018 relabeling: 04.2 is now
titled "imputed rentals" — the historical owner-cost content is flagged for
verification if the 04-vs-CPIF-04 gap ever becomes load-bearing.

**Files.** `code/swedish_fork.py`, `data/swedish_fork.csv`,
`figures/fig_swedish_fork.png`.
