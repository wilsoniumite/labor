# notation_map.md — v1 → v2 symbol map (Phase 1 of the v2 rewrite)

Adopted 2026-08-27 per the v2 rewrite brief (`rewrite_brief_pinning_v2.md` §2;
decisions frozen there — do not relitigate). This file is the authority for:
the Phase-1 rename executed on `paper/pinning.html`, the paper-to-Lean
translation table, and the appendix notation table that lands in Phase 2+.

Phase 1 is SYMBOLS ONLY: every formula identical, every sentence identical up
to the symbol tokens and the three notation-hygiene edits listed at the foot.

## The map

| object | v1 | v2 | HTML literal (v1 → v2) | sites |
|---|---|---|---|---|
| productivity schedule | ρ(x), ρ*, ρ̄ | γ(x), γ*, γ̄ | `&rho;` → `&gamma;` (combining U+0304 rides) | 105 |
| time preference (= interest rate) | δ | ρ | `&delta;` → `&rho;` | 14 |
| wear/depreciation rate | d | δ | wear-site `<i>d</i>` → `<i>&delta;</i>` | 4 |
| uniform transfer (the dividend) | u | d | `<i>u</i>` → `<i>d</i>` | 7 |
| land coefficient | ℓ, ℓ₀ | b, b₀ | `&#8467;` → `b` (`<i>b</i>` in prose) | 36 |
| rent tax rate | τ | τ_R | `&tau;` → `&tau;` + `<sub><i>R</i></sub>` | 11 |
| payroll tax rate | t | τ_w | `<i>t</i>` → `<i>&tau;</i><sub><i>w</i></sub>` | 5 |
| land expenditure weight | σ | α | `&sigma;` → `&alpha;` | 16 |
| realized land share | s_h(q) | α(q) | `s<sub>h</sub>(q)` → `&alpha;(q)` | 4 |
| CES elasticity, goods vs land | η (App A/B) | σ | `&eta;` → `&sigma;` | 17 |
| CES elasticity, H-content vs substitutes | η (App D) | σ_H | `&eta;` → `&sigma;` + `<sub><i>H</i></sub>` | 5 |
| human-essential task set | K | H | `<i>K</i>` → `<i>H</i>` | 39 |
| its measure | k | \|H\| | measure-site `<i>k</i>` → `\|<i>H</i>\|` | 6 |
| its wage | w_K | w_H | subscript rides with K → H | — |
| subsistence H-hours | k_s | n_s | `<i>k</i><sub><i>s</i></sub>` → `<i>n</i><sub><i>s</i></sub>` | 1 |
| dependency floor | s_d | s̲ | `s<sub><i>d</i></sub>`/`s<sub>d</sub>` → `s&#818;` | 5 |
| wage-linked consumption share | λ_C | φ_C | `&lambda;<sub><i>C</i></sub>` → `&phi;<sub><i>C</i></sub>` | 4 |
| wage-linked revenue share | λ_R | φ_G | `&lambda;<sub><i>R</i></sub>` → `&phi;<sub><i>G</i></sub>` | 3 |
| broadcastable fraction | β | ψ | `&beta;` → `&psi;` | 5 |
| goods price | p_g | p (numeraire, p = 1 as before) | `p<sub><i>g</i></sub>` → `p` | 17 |
| participant count (Lemma A.1) | n | N_a | `<i>n</i>` → `<i>N</i><sub><i>a</i></sub>` | 3 |
| produced-price / rent vectors | c, r (§10 plain) | bold **c**, **r** everywhere | §10 display bolded to match App A | 1 |

## Amendment 1b (2026-08-28, her call): the starred margin abbreviation dies

| object | v1b | v2b | HTML literal | sites |
|---|---|---|---|---|
| schedule at the margin | γ* | γ(x*) | `<i>&gamma;</i>*` → `<i>&gamma;</i>(<i>x</i>*)`; bare `&gamma;*` → `&gamma;(x*)` in .eq displays | 29 |

γ* was a pure single-referent abbreviation and the paper already ran both
forms (29 starred vs 14 spelled) — definitions-earn-reuse retires it. The
Prop-2 defining clause ("with γ* = γ(x*)") is deleted, not renamed. γ̄ (the
flat schedule level) and x* are untouched. Census: live row updated, DEAD
guard added. DRAFTING RULES fixed the same day (not renames — none of
these symbols are in the paper yet): π debuts at §8.0 as the transition's
object of study, never in the §§1–7 spine; Q stays §8-local; W_K is not
christened unless §9.2 reuses it; the operating recipe stays BARE
(a, λ, b) against the marked build recipe (a_I, λ_I, b_I) — recipes are
named by the activity they feed and the service recipe is the default
(her call, 2026-08-28, after the λ-brand/measurement-continuity
argument).

## Rename order (chains — do not reorder)

The map contains two chains; each step frees the symbol the next step uses.
Applied in this order, with per-family count assertions:

1. `s_d → s̲` (frees the subscript d)
2. `σ → α`, `s_h(q) → α(q)` (frees σ)
3. `η → σ / σ_H` (context-split: App D sites get the H subscript)
4. `τ → τ_R` (frees bare τ)
5. `t → τ_w`
6. `ρ → γ` (all 105 sites are the schedule; frees ρ)
7. `δ → ρ` (time preference; uses freed ρ)
8. `d → δ` (wear; uses freed δ)
9. `u → d` (dividend; uses freed d)
10. everything chain-free: ℓ→b, K→H, k→|H|, k_s→n_s, λ_C/λ_R→φ_C/φ_G,
    β→ψ, p_g→p, n→N_a, §10 bold vectors

## Context notes

- **γ family.** v1 already defines ρ(x) = γ_L(x)/γ_M(x); the rename makes the
  schedule a member of its own family: γ(x) = γ_L(x)/γ_M(x). γ_L, γ_M
  unchanged. A&R's γ(i) is now the nominal neighbor it always was in spirit.
- **ρ is interest now.** First use (Appendix A, durability paragraph) carries
  the one-clause disambiguation: interest is ρ, rent is r. The old ρ̂
  collision note in the back-matter footnote dies with the rename.
- **b vs DMP's b.** ℓ→b creates the collision with search theory's
  non-market-activity parameter b; the back-matter notation footnote now
  carries it: our s is a priced object, their b is our b's homonym only.
- **σ vs σ_H.** The two context-local η's of v1 are now distinct symbols;
  the "context-local" footnote clause dies.
- **H vs T_H.** The human-essential set H shares a letter with the housing
  subscript in T_P/T_H (Appendix B). Same tolerated species as P (index) vs
  T_P. Noted in the footnote.
- **s̲** is written `s&#818;` (combining low line, inside the italic wrap),
  parallel to ρ̄'s combining macron. LaTeX: `\underline{s}`.
- **b·r in displays.** ℓr juxtaposed was unambiguous (ℓ is a distinct glyph);
  br juxtaposed is not. The three display sites write b&middot;r, matching the
  recursion display's own a&middot;c + &lambda;&middot;w + b&middot;r
  convention; prose keeps the compound italic (br), like rT and aX.
- **Carrying factor s** (sympy/Lean internal for the user-cost forms) never
  appears in the paper and is unaffected; the v2 dynamics replace it with
  u_K = (ρ+δ)(1+ρ)^{J−1} in Phase 3.
- **Identity matrix 𝟙** (brief §2.2) is deferred to Phase 2: I collides with
  investment I_t only once the dynamics exist, and the LaTeX macro choice
  (\mathbbm{1} vs \mathds{1}) rides with that edit. v1's single (I−A)⁻¹ keeps I.
- **Lean identifiers stay internal** (rho, ell, eta, …); only the
  paper-facing comments, manifest notes, and the README translation move to
  v2 symbols. `lean/README.md` §Scope is the translation table's home until
  the appendix table lands in Phase 2.

## New prose in this pass (hers to voice)

1. The rewritten back-matter **Notation** footnote (drops ρ̂ and η-context
   clauses; adds interest-vs-rent, DMP-b, H-vs-T_H).
2. The durability paragraph's **"time preference ρ"** disambiguation clause.
3. Nothing else: every other sentence is v1's with symbols swapped.

## Unchanged (confirmed against the paper at rename time)

x, x*, γ_L, γ_M, c, w, N, a, λ, Λ, A, B, T, T_j, T_P, T_H, R, ω_ij, μ(x),
ε_D, ε_S, κ, q, q*, q_enc, m_w, m_e, v, f, z, r(z), X, Y, L̄, P, P_s,
g_s, h_s, h_e, s, s₀, s(q), Δ, i, j.
