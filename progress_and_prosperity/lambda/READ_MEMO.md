# THE GATE READ — λ assembly, unit 6 (2026-08-20)

**Verdict, per the pre-committed criteria: AMBIGUOUS — the pre-named case
"λ̂ falling, H_rel flat" fired on the world referee's quantity leg.**
Per the protocol: stop, report, Stella decides. No silent proceeding.
Every number below is produced by `code/gate_read.py` (deterministic; the
operationalization is stated in its header and vetoable).

## The accounting

| Referee / leg | Window | Members | Verdict | Median slope /decade | Share negative | Member-Δ band |
|---|---|---|---|---|---|---|
| US λ̂ (W3) | 1997–2023 | 6 | **FALLING** | −0.0215 | 100% | [−0.077, −0.028] |
| US λ̂ (W1b, spliced) | 1982–2023 | 2 | **FALLING** | −0.0249 | 100% | [−0.103, −0.102] |
| US H_rel (W3; W1b = NAICS segment) | 1997–2023 | 6 | **FALLING** | −0.0245 | 100% | [−0.097, −0.045] |
| US λ̂ rent-purged (S&S) | 1997–2016 | 6 | **FALLING** | −0.0349 | 100% | [−0.081, −0.051] |
| World λ̂ (primary, sourced labor) | 1995–2014 | 12 | **FALLING** | −0.0439 | 100% | [−0.085, −0.040] |
| World λ̂ (supporting: ICIO incl. frozen tail) | 1995–2022 | 4 | **FALLING** | −0.0362 | 100% | [−0.108, −0.088] |
| **World H_rel (primary)** | 1995–2014 | 6 | **FLAT/RISING** | **+0.0958** | 33% | [−0.079, +0.315] |
| World H_rel (supporting: ICIO full) | 1995–2022 | 2 | MIXED | +0.0680 | 50% | [−0.051, +0.418] |

Within-segment (W1b): SIC 1982→1992 Δ = −0.108; NAICS 1997→2023 Δ = −0.035.
W1 context (no sign requirement, vintage scatter as expected): 1967→1992
path 0.642, 0.701, 0.658, 0.740, 0.607, 0.632.

Diagnosis layers (reported, not gated):
- US w̄_rel (price leg): FLAT/RISING (+0.040/decade) — the US decline sits
  **entirely on the quantity leg**.
- S&S rents: machinery-direct ρ 0.139→0.104 (1997→2016); aggregate
  0.123→0.088. Rents did erode — and purging that erosion still leaves the
  US λ̂ falling on 100% of members. **The US decline is not rent
  dissipation.** (A&R level anchor, automated jobs: ≈0.35 [0.19–0.445].)
- Offshoring: foreign-labor share of US machinery purchases rose in every
  release — wiod13 0.41→0.45, wiod16 0.36→0.48, icio25 0.29→0.44
  (1995→2022).

## Why the one flat leg is flat — composition, on the evidence

The pre-named interpretation for λ̂↓/H_rel→ was "rent-dissipation
candidate." The diagnosis layers do not support that mechanism here:

1. Within the US, the rent story is affirmatively ruled out: the purge
   survives and w̄_rel *rose*.
2. World H_rel = hours embodied × world average wage. Hours embodied per
   dollar of machinery **rose** while compensation embodied **fell** — and
   the foreign-labor share rose sharply over the same window. That is the
   signature of production shifting toward low-wage, high-hours suppliers
   (the China entry), a **cross-country composition effect** in the hours
   mix — not of any technology failing to shed labor. The criteria's
   H-leg was designed to catch within-economy rent masking; it did not
   anticipate that the *world* hours aggregate would be dominated by the
   relocation margin the λ̂ world referee was itself built to referee.
3. Where composition is held fixed — the US system — the quantity leg
   falls unambiguously.

Stated plainly, in unread-discipline terms: the machinery wage-bill share
fell everywhere we can measure it, at every level of resolution, and
survived rent purging; the world *hours* content per dollar rose because
machinery hours moved to cheap-hour countries. Whether that constellation
passes the gate is, by the committed criteria, **not the assembly's call —
it is Stella's**, and the criteria were written that way on purpose.

## The decision before Stella (Breakpoint)

- **Option A — repair the world quantity leg and re-read.** A
  fixed-composition variant (hours embodied at a fixed country mix, or a
  within-country-aggregated H) separates the technical margin from the
  relocation margin. One small unit; the criteria then apply unchanged.
- **Option B — judge the read a pass on the current evidence,** recording
  an amendment that the world H-leg is composition-confounded and that the
  rent channel (the leg's actual purpose) is resolved by the US purge +
  w̄_rel. This is a judgment call the protocol reserves to Stella.
- **Option C — hold at ambiguous.** The gate stays closed; downstream
  hypothesis-dependent book work waits.

Note for the PLAN's framing ("if λ isn't falling, everything downstream
gets rethought"): λ̂ IS falling — on the US referee over 40 years, on the
world referee across three independent releases, and through the rent
purge. The ambiguity is confined to the interpretation of one aggregate
quantity leg. The FAIL branch did not fire and is not close on any member.

## Caveats carried with the read

Timing honesty (committed): tables end 2022–23; the post-2023 AI wave is
expected to be invisible here; absence of a recent kink is not evidence in
either direction. ICIO 2015–22 runs on frozen-2014 labor shares
(structure-only, supporting members only — and they agree in sign with the
sourced members). The 2006–10 ICIO block is absent (WIOD covers it). W1b's
H leg covers the NAICS segment only. The 1992→1997 splice step (0.9204) is
a classification break, stated; both spliced members and both within-
segment directions agree in sign, so the splice does not carry the W1b
conclusion. BEA's "should not be used as a time series" caveat rides with
the SIC benchmark points.
