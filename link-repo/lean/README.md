# Lean statements — the corner-regime spine and the λ>0 extension

**Status: builds clean — 0 errors, 0 `sorry`, 0 warnings.** Lean 4.33.0, mathlib
pinned to tag `v4.33.0`. All 119 declarations across the two modules are
machine-checked: 66 in the corner spine (`TheLink.lean`), 53 in the pinning
extension (`Pinning.lean`, 2026-08-27).

```bash
cd link-repo/lean && lake exe cache get && lake build
```

First run downloads ~5-8GB of mathlib oleans into `.lake/` (gitignored). If
`lean` isn't on your PATH, elan puts it at `~/.elan/bin/`.

**Corporate-network notes (SEB laptop, 2026-08-27):** elan's own downloader
fails behind the proxy (`CRYPT_E_NO_REVOCATION_CHECK` — the CRL endpoints are
blocked, and schannel curl requires revocation by default). Working setup:
`ssl-no-revoke` in `~/.curlrc` and `%APPDATA%/_curlrc` (lake and the mathlib
cache tool shell out to curl, which then works); the toolchain side-loaded —
download `lean-4.33.0-windows.zip` from the lean4 GitHub releases, extract,
then `elan toolchain link "leanprover/lean4:v4.33.0" <dir>` so elan never
needs the network; and `XDG_CACHE_HOME=C:/Users/<user>/.cache` so the cache
tool avoids the unwritable roaming drive `J:`.

One caveat no proof assistant removes: these statements are a *translation* of
the paper. Lean checks the derivations, not the translation. A mistranscribed
proposition yields a true theorem about the wrong claim.

## What this is for

Not verification of the algebra — `checks/*.py` already does that with sympy,
against numeric instantiations too. This file exists to produce the **assumption
manifest**: the complete enumerated list of hypotheses each proposition actually
consumes, with the implicit ones forced into the open.

A Lean theorem's hypotheses are exactly what its proof consumed, so a
formalisation cannot leave an assumption in the author's head. That does not tell
you whether the assumptions are *true* — nothing about a proof assistant bears on
whether the new-task margin is closed, whether λ_C = 0.72, or whether
tasks-with-a-capability-schedule is the right ontology. It tells you what the
assumptions *are*, which is upstream of arguing about them.

## Findings

Collected in a comment at the foot of `Link/TheLink.lean`. Summary:

1. **Props 4 and 5 are different sub-regimes** and cannot share a structure —
   4(i) needs labour employed at parity, 5 sets it to zero measure. The paper
   carries this in an appendix remark; Lean forces it, since `w` has nowhere to
   live in the corner-below structure.
2. **Prop 10's VAT rate has no feasibility bound** — *the one finding here that
   is proved rather than observed.*
   `mix_infeasible_when_floor_exceeds_bases` shows the feasible set is empty once
   `floor > rT + E`, so a feasible pair exists **iff** `floor ≤ rT + E`. Below
   that line Prop 10(ii) optimises over the empty set. Empirically comfortable
   (US `N·Ps/E` ≈ 0.25 against a bound near 1.5 at κ = 0.33), but the theorem
   should carry the hypothesis — and the bound tightens exactly in the low-κ
   regime the mix frontier is written for.
3. **Prop 7(ii) is an assumption, not a theorem, in this model** — the corner has
   no asset-pricing equation and no land-use margin to derive capitalisation
   from. Encoded as `LandTaxInvariance`.
4. **`σ` carries two jobs**, and Prop 8's subsistence bundle is a third kind of
   object (fixed quantities, so its implied land share moves with `q`).
5. **Prop 4(iii)'s price index is asserted** and drops a constant.
6. **`0 < a` is used but never stated**; the durable reading needs
   `a(δ+d) < 1`, stronger than `a < 1`.
7. **Stated-but-unused hypotheses** — several genuine (e.g. `prop3_user_cost`
   needs neither `0 ≤ δ` nor `0 < d`; `prop9_iii_race` needs neither `0 < T` nor
   `0 < N`), several mere artefacts of mathlib's `x / 0 = 0` convention. The file
   separates the two; don't read the artefacts as findings.

Two that run the other way and **strengthen** the paper:

8. **`q` is a pure technology ratio** — no price appears in it — so κ, via
   `prop8_iii_land_constraint`, is invariant to any fiscal action's effect on
   `r`. That answers the appendix's "the base feeds back — tendency, not
   theorem" hedge for the fundability question, and the paper doesn't deploy it.
9. **Prop 5(iii) is definitional**, and the paper is right to hedge it: the Lean
   proof of `prop5_iii` is literally `prop4_ii`.

## Scope

`TheLink.lean` (old-draft numbering): Propositions 3, 4, 5, 6(i), 7(i)–(ii),
8, 9(ii)–(iii), 10, 13(ii) — the chain from "machines make machines" to
"redistribution without deadweight".

`Pinning.lean` (pinning-paper numbering, 2026-08-27): Proposition 2 — the
λ>0 replacement closure, uniqueness, and both comparative statics, with a
bridge theorem meeting `Corner` at λ = 0; Proposition 4(i)–(ii) with λ —
the 1/L̄ wage, the (1 − a − λρ̄)/(ℓρ̄L̄) display, both divergence margins
(ρ̄ → 0 and ℓ → 0), both automation statics, and the substitution bound;
the λ>0 user-cost closures for both carrying factors (1+δ and δ+d), sympy
first per the house rule; Lemmas D.2 (fraud bound: the iff, both statics,
the v → 1 divergence, the f = 0 collapse) and D.3 (superstar concentration
via its finite-star-mass family — mean invariance, the ε < β ordering, the
median mass, and the ε → 0 ratio limit); and the CES dial's three-case
share limit (Appendix B's General-η display). Its manifest findings
(P1–P5) are at the foot of the file.

Omitted, deliberately:

- **Props 1–2** — equilibrium existence and stability. Large definitional
  apparatus for little return, since the substance is the definitions rather
  than the proofs.
- **Prop 11** — the Baumol fork. Formalizable, but `Real.rpow` limit work in
  three cases and mostly a slog.
- **Prop 12** — the open economy, mostly verbal.
- **Props 7(iii) and 13(iii)** — the uniqueness converses. Not formalizable in
  principle: they quantify over fiscal instruments *in the world*, not over a
  defined set. Encoding the instrument set as an inductive type would make them
  true by construction and worth nothing. The paper's own hedge on 7(iii) ("what
  is proved is base-class necessity plus within-class dominance — not, strictly,
  instrument necessity") is the correct statement and Lean cannot improve it.

## Layout

```
lean/
  lakefile.toml       mathlib pinned to v4.33.0
  lean-toolchain      leanprover/lean4:v4.33.0
  Link.lean           root module
  Link/TheLink.lean   the corner spine: statements, proofs, and its manifest
  Link/Pinning.lean   the λ>0 extension: Prop 2, Prop 4(i)-(ii) with λ,
                      user-cost closures, Lemmas D.2/D.3, the CES dial,
                      and its manifest (P1-P5)
```
