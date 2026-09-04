# The coverage-ratio ceiling (data note, 2026-08-09)

The paper's data note cites HUD FY2025 fair-market rents "for the ceiling grid"; this is
that grid's record, originally data item two of the revision thread (moved here
2026-09-04). Files: `code/kappa_ceiling.py`, `data/kappa_ceiling.csv` (32 members),
`data/hud_fy25_fmrs.xlsx` (vendored raw, validated). The script imports the paper's own
rT machinery from `code/feasibility_kappa.py` and needs `python-calamine` for the HUD file.

**Object.** Prop 8's coverage ratio κ(q) rises toward T/(N·h_s) and never exceeds it;
the paper never checked that ceiling against 1 (audit point iv). In flow terms:
(aggregate site rent) / (N × site-rent bill of one person's floor housing).

**Method** (`code/kappa_ceiling.py`; FRED reachable from this machine — the pass-one
container blocks do not apply here). Numerator: the paper's own rT members rebuilt
live through `feasibility_kappa`'s import — all 12 FRED series re-validated by the
paper's own gates; 2025 members z1_hh × {GS10, GS10+150bp} = $1,009B/$1,362B and
PCE-housing × {0.30, 0.50} = $993B/$1,655B (z1_econ excluded: NFC structures end
2020; year-mixing refused). Denominator: HUD FY2025 Fair Market Rents (county file,
4,764 areas, validated by magic bytes, row count, and median sanity; the file's
malformed XML properties needed the calamine reader) — floor housing per person under
two labeled pairings (single ↔ efficiency ÷ 1; family-of-four ↔ 2BR ÷ 4), two
national summaries (median county; population-weighted), × site-share of gross rent
{0.30, 0.50}. 4 × 2 × 2 × 2 = 32 members.

**Result: the ceiling straddles 1.** Median 1.26, band [0.38, 4.91]; 13/32 members
below 1. Clean structure: every shared-housing (pc4_2br) member clears 1 (1.16–4.91);
solo-dwelling (single_eff) members mostly fail (0.38–1.62, 11/16 below 1);
population-weighted FMR (where people live) sits below median-county throughout.

**Verdict on audit iv: substantive robustness note, not fatal — but only because
every measurement bias runs downward.** (i) The rT members are the paper's own
lower bounds (financial/government/farm land omitted; Z.1 residual caveat);
(ii) FMR is GROSS rent including utilities — partly machine-made content in the
denominator; (iii) the economy-wide land member is missing from the numerator.
A corrected ceiling sits higher than measured. Still, the honest sentence for the
paper: **whether κ can ever reach 1 depends on the floor's housing standard —
shared housing yes, a dwelling of one's own only marginally and not in the
population-weighted metros** — and h_s is partly policy-made (zoning), which
connects this directly to the parked second-paper critique (the land facts' rival).
Prop 8's measured text ("κ = 0.33 and rising; κ = 1 not yet in reach") stands;
the "demolition funds its own remedy" framing takes a ceiling caveat.

**Bundle tension, stated.** The FY25 median-county efficiency FMR alone is
$9,960/yr gross vs the paper's whole Orshansky single bundle P_s(2025) = $16,186
(and pc4 = $8,219): the paper's 1963-weighted basket underprices modern floor
housing, so the paper's κ is if anything overstated at modern housing prices. The
ceiling here is bundle-free on the goods side; the two objects answer different
questions.

**Blocked (reported, not substituted):** BLS SPM threshold files 404 at both probed
paths (`spm_thresholds_2023/2024.xlsx`); Census SPM directory (www2) HTTP 520 on
two attempts. The SPM housing-portion member is therefore not in the grid.

**Files:** `code/kappa_ceiling.py`, `data/kappa_ceiling.csv` (32 members),
`data/hud_fy25_fmrs.xlsx` (vendored raw, validated).

