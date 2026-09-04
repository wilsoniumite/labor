# P1 §10 delivery draft — "The recipe's labor content, measured."

*Ready-to-splice block for `pinning/paper/main.tex` (was the-link-revision/paper/pinning.html), drafted
2026-08-20 by the λ delivery unit. The splice itself belongs to a
the-link-revision session under that thread's discipline: snapshot first,
splice, update the affected checks, run `checks/check_pinning.py`, veto
window. Numbers are from `make_delivery_figures.py` (paste-source), all
reproducible from the λ assembly's scripts.*

## The block (insert after "The fiscal exposure, in one sentence.")

**The recipe's labor content, measured.** The labor compensation embodied
in one dollar of machinery final output, resolved through the published
input–output total requirements — the empirical counterpart of λ in the
recipe, taken as a share so that no deflator enters. It falls everywhere
measured (Figure L). In U.S. series: from 0.68 in 1982 to 0.55 in 2023
[2023 band 0.47–0.58 across the classification grid], every grid member
negative in every window, the SIC-era benchmarks and the NAICS-era annual
series agreeing in sign on both sides of the 1992/1997 splice. In world
series — three inter-country systems, labor counted wherever it accrues —
from roughly 0.56 in 1995 to 0.48 in 2022, twelve of twelve members
declining. The decline is quantity, not price: hours embodied, valued at
the economy-average wage, fall in step; the embodied labor's relative wage
is flat to rising; and purging industry labor rents (Stansbury and Summers
2020) leaves the fall on every member even as machinery's own rents eroded
— the decline is not rent dissipation misread as automation (Acemoglu and
Restrepo 2026). Within countries the hours collapse is steeper than any
value series shows — to a half by 2009, three-eighths by 2014, a sixth by
2022, by release — because production simultaneously relocated toward
low-wage suppliers: the foreign-labor share of U.S. machinery purchases
rose from 0.29 to 0.44, and the raw world aggregate understates the
technical margin by exactly that relocation wedge. The companion note
carries construction, verification, and the caveat ledger; the criterion
that would have falsified this — the series holding flat under rent
purging and at fixed composition — was committed before assembly, and did
not bite.

## Figure L (copy `lambda/figures/lambda_delivery_fig1.png` into the paper's figures)

Caption: **Figure L.** The labor content of machinery final output —
labor compensation embodied per dollar, resolved through published total
requirements. Left: United States — SIC-era benchmarks 1967–1992 (spliced
at the 1992/1997 classification break, link 0.920, unspliced points also
shown) and the annual 1997–2023 band across the classification grid.
Right: world — three inter-country systems, 1995–2022, all-country labor
through the global inverse; the shaded tail holds labor shares at 2014
(structure only). Bands are classification grids, not confidence
intervals. The 2006–2010 block of the 2025 ICIO edition is pending.

## Consequential edits at splice (exact)

1. **§10, "Three assemblies, specified and open."** Becomes **"Two
   assemblies, specified and open."** — delete item (2) (*λ, directly*),
   renumber (3)→(2) (the long record), keep (1) (incidence slope)
   verbatim. (The long-record assembly has its own thread; its item
   stands.)
2. **§11, first kill item.** Keep the falsifier's conditional form; append
   the measured status. Replace the item's closing clause "— measured as
   assembly (2) — recursive automation is weak, the wage stays inside the
   substitute's price, and the terminal-rent closure loses its mechanism."
   with: "recursive automation is weak, the wage stays inside the
   substitute's price, and the terminal-rent closure loses its mechanism.
   Measured (§10): it falls — in value and in hours, within countries and
   in the world aggregate — and the fall survives rent purging; the
   register carries the series forward."
3. **Checks.** `check_pinning.py` and the STATE verify-list record "three
   assemblies marked [spec'd, unbuilt]" — update whichever check or
   recorded item asserts that wording before running the battery; ALL
   GREEN required as ever.
4. **Back matter (optional, splicer's call):** one clause in the
   verification note that the λ assembly is code-gated (44 checks across
   four batteries) with the companion note as its record.
5. Bibliography: add Stansbury & Summers (2020, BPEA) if not present;
   A&R 2026 already cited.
