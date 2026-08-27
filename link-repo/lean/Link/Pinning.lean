/-
# Pinning the Wage — the λ>0 spine, as Lean 4 statements

STATUS: see README for the build line. Extends `Link/TheLink.lean` (the λ=0
corner spine) to the pinning paper's generalization: labor still inside the
machine recipe.

SCOPE, in the pinning paper's numbering:
  * Proposition 2 (replacement closure): the solved system, uniqueness on the
    viable set, and the comparative statics the text states in words — both
    prices rise in λ and in ρ*, and `c` moves with ρ* exactly when λ > 0.
  * The bridge: at λ = 0 the closure is the corner rental of `TheLink` —
    stated against `Corner` itself, not a lookalike.
  * Proposition 4(i)–(ii) with λ: the wage in goods is 1/L̄ (machine quality
    still cancels); the relative price of non-produced services is
    (1 − a − λρ̄)/(ℓρ̄L̄), falling in both automation margins, diverging as
    ρ̄ → 0, and bounded under machine-for-land substitution in the recipe.
  * The λ>0 user-cost form (Appendix A's durability paragraph): for carrying
    factor s — s = 1+δ one-period building, s = δ+d wear — the recursion
    closes at c = s·ℓr/(1 − s(a+λρ*)). First sympy-checked in
    `the-link-revision/checks/check_pinning.py` (house rule), stated here
    with its convergence condition in the open.
  * Lemma D.2 (the fraud bound) and Lemma D.3 (superstar concentration).
  * The CES dial of Appendix B's General-η display (the paper's three-case
    share limit).

Prop 4(iii) is regime-free given `pg` and `r` and is already covered by
`Corner.prop4_iii_decomp` / `prop4_iii_collapse`; nothing changes with λ.

PURPOSE, as in `TheLink.lean`: the assumption manifest, not re-certification
of algebra sympy already checks. `-- MANIFEST:` marks each place writing the
statement forced a hypothesis the prose leaves implicit; findings collect at
the foot of the file.
-/

import Link.TheLink

namespace Link

open Filter Topology

/-! ## §0. Primitives

The sloped/flat regime with the machine sector still buying labor. `lam` is
the machine-recipe labor coefficient λ; `ρ` is relative human productivity at
the working point — ρ* in the sloped regime, ρ̄ in the flat limit. `L` is L̄,
carried for the fork statements. -/

/-- λ>0 primitives. -/
structure Spine where
  /-- machine services required per unit of machine services -/
  a : ℝ
  /-- labor-hours per unit of machine services (the recipe coefficient λ) -/
  lam : ℝ
  /-- non-produced services per unit of machine services -/
  ℓ : ℝ
  /-- relative human productivity at the margin (ρ* / ρ̄) -/
  ρ : ℝ
  /-- L̄ = ∫dx/γL(x), the labour one human needs for the whole checklist -/
  L : ℝ
  /-- terminal rent -/
  r : ℝ
  ha₀ : 0 < a
  /-- λ = 0 is allowed: the corner is the boundary case, and the bridge
  theorem below meets `TheLink` there -/
  hlam : 0 ≤ lam
  hℓ : 0 < ℓ
  hρ : 0 < ρ
  hL : 0 < L
  hr : 0 < r
  /-- viability: the produced content of a unit of machine services, with its
  labor priced at the margin, runs below one.

  MANIFEST: this replaces the corner's `a < 1` and is *strictly stronger*
  whenever λ > 0; `a < 1` follows from it (see `a_lt_one`) but not
  conversely. The paper states it (`1 − a − λρ* > 0`) at Proposition 2 and
  the structure carries nothing weaker. -/
  hviable : a + lam * ρ < 1

namespace Spine

variable (M : Spine)

/-! ### Positivity -/

lemma a_lt_one : M.a < 1 := by nlinarith [M.hviable, mul_nonneg M.hlam M.hρ.le]

lemma denom_pos : 0 < 1 - M.a - M.lam * M.ρ := by linarith [M.hviable]

/-- Machine rental (Prop 2). -/
noncomputable def c : ℝ := M.ℓ * M.r / (1 - M.a - M.lam * M.ρ)

/-- The wage at the margin (Prop 2). -/
noncomputable def w : ℝ := M.ρ * M.c

lemma c_pos : 0 < M.c := div_pos (mul_pos M.hℓ M.hr) M.denom_pos

lemma w_pos : 0 < M.w := mul_pos M.hρ M.c_pos

/-! ## §1. Proposition 2 — the replacement closure -/

/-- Prop 2: the closure satisfies the task margin. -/
theorem prop2_margin : M.w = M.c * M.ρ := by unfold w; ring

/-- Prop 2: the closure satisfies free entry in machine production — the
recipe prices itself with its own labor inside. -/
theorem prop2_free_entry : M.c = M.a * M.c + M.lam * M.w + M.ℓ * M.r := by
  have h : (1 : ℝ) - M.a - M.lam * M.ρ ≠ 0 := M.denom_pos.ne'
  unfold w c
  field_simp
  ring

/-- Prop 2, uniqueness: any pair satisfying the margin and free entry is the
closure. -/
theorem prop2_unique (w' c' : ℝ) (hm : w' = M.ρ * c')
    (hf : c' = M.a * c' + M.lam * w' + M.ℓ * M.r) : c' = M.c ∧ w' = M.w := by
  have hD : (1 : ℝ) - M.a - M.lam * M.ρ ≠ 0 := M.denom_pos.ne'
  have hc : c' = M.c := by
    unfold c
    rw [eq_div_iff hD]
    linear_combination hf + M.lam * hm
  exact ⟨hc, by rw [hm, hc]; unfold w; ring⟩

/-! ### Comparative statics (Prop 2's second sentence)

Stated as two-point difference signs on free functions, the file's convention
for statics without calculus. -/

/-- The closure as a free function, for statics and limits. -/
noncomputable def cOf (a lam ℓ ρ r : ℝ) : ℝ := ℓ * r / (1 - a - lam * ρ)

/-- The wage as a free function. -/
noncomputable def wOf (a lam ℓ ρ r : ℝ) : ℝ := ρ * cOf a lam ℓ ρ r

theorem cOf_eq : M.c = cOf M.a M.lam M.ℓ M.ρ M.r := rfl

theorem wOf_eq : M.w = wOf M.a M.lam M.ℓ M.ρ M.r := rfl

/-- Prop 2 statics: the wage rises in λ — the recursion's amplification. Both
comparison points must be viable.

MANIFEST: viability at the *upper* point `a + lam₂·ρ < 1` is the binding
hypothesis; viability at the lower point follows from it. The paper's "on the
viable set both prices rise" is exactly this. -/
theorem w_strictMono_in_lam (a ℓ ρ r lam₁ lam₂ : ℝ) (hℓ : 0 < ℓ) (hρ : 0 < ρ)
    (hr : 0 < r) (hlt : lam₁ < lam₂) (hv₂ : a + lam₂ * ρ < 1) :
    wOf a lam₁ ℓ ρ r < wOf a lam₂ ℓ ρ r := by
  have hstep : lam₁ * ρ < lam₂ * ρ := mul_lt_mul_of_pos_right hlt hρ
  have hD₂ : 0 < 1 - a - lam₂ * ρ := by linarith
  have hnum : 0 < ℓ * r := mul_pos hℓ hr
  unfold wOf cOf
  have hfrac : ℓ * r / (1 - a - lam₁ * ρ) < ℓ * r / (1 - a - lam₂ * ρ) :=
    div_lt_div_of_pos_left hnum hD₂ (by linarith)
  exact mul_lt_mul_of_pos_left hfrac hρ

/-- Prop 2 statics: the rental rises in λ. -/
theorem c_strictMono_in_lam (a ℓ ρ r lam₁ lam₂ : ℝ) (hℓ : 0 < ℓ) (hρ : 0 < ρ)
    (hr : 0 < r) (hlt : lam₁ < lam₂) (hv₂ : a + lam₂ * ρ < 1) :
    cOf a lam₁ ℓ ρ r < cOf a lam₂ ℓ ρ r := by
  have hstep : lam₁ * ρ < lam₂ * ρ := mul_lt_mul_of_pos_right hlt hρ
  have hD₂ : 0 < 1 - a - lam₂ * ρ := by linarith
  have hnum : 0 < ℓ * r := mul_pos hℓ hr
  unfold cOf
  exact div_lt_div_of_pos_left hnum hD₂ (by linarith)

/-- Prop 2 statics: the wage rises in ρ*, with the `(1 − a)` factor the proof
of Prop 2 displays. -/
theorem w_strictMono_in_rho (a lam ℓ r ρ₁ ρ₂ : ℝ) (ha : a < 1) (hlam : 0 ≤ lam)
    (hℓ : 0 < ℓ) (hr : 0 < r) (hlt : ρ₁ < ρ₂) (hv₂ : a + lam * ρ₂ < 1) :
    wOf a lam ℓ ρ₁ r < wOf a lam ℓ ρ₂ r := by
  have hstep : lam * ρ₁ ≤ lam * ρ₂ := mul_le_mul_of_nonneg_left hlt.le hlam
  have hD₂ : 0 < 1 - a - lam * ρ₂ := by linarith
  have hD₁ : 0 < 1 - a - lam * ρ₁ := by linarith
  have hnum : 0 < ℓ * r := mul_pos hℓ hr
  unfold wOf cOf
  rw [← mul_div_assoc, ← mul_div_assoc, div_lt_div_iff₀ hD₁ hD₂]
  nlinarith [mul_pos hnum (mul_pos (sub_pos.mpr hlt) (sub_pos.mpr ha))]

/-- Prop 2 statics: the rental moves with ρ* exactly when λ > 0 — the
cross-effect the text calls the two margins' interaction. -/
theorem c_strictMono_in_rho (a lam ℓ r ρ₁ ρ₂ : ℝ) (hlam : 0 < lam)
    (hℓ : 0 < ℓ) (hr : 0 < r) (hlt : ρ₁ < ρ₂)
    (hv₂ : a + lam * ρ₂ < 1) :
    cOf a lam ℓ ρ₁ r < cOf a lam ℓ ρ₂ r := by
  have hstep : lam * ρ₁ < lam * ρ₂ := mul_lt_mul_of_pos_left hlt hlam
  have hD₂ : 0 < 1 - a - lam * ρ₂ := by linarith
  have hnum : 0 < ℓ * r := mul_pos hℓ hr
  unfold cOf
  exact div_lt_div_of_pos_left hnum hD₂ (by linarith)

/-- And at λ = 0 the cross-effect is exactly zero: the rental ignores ρ*. -/
theorem c_const_in_rho_at_corner (a ℓ r ρ₁ ρ₂ : ℝ) :
    cOf a 0 ℓ ρ₁ r = cOf a 0 ℓ ρ₂ r := by unfold cOf; norm_num

/-! ## §2. The bridge to the corner spine -/

/-- At λ = 0 the closure **is** the corner rental of `TheLink` — stated
against `Corner` itself. The two files meet here. -/
theorem corner_bridge (C : Corner) (hlam : M.lam = 0) (ha : M.a = C.a)
    (hℓ : M.ℓ = C.ℓ) (hr : M.r = C.r) : M.c = C.c := by
  unfold c Corner.c
  rw [hlam, ha, hℓ, hr]
  norm_num

/-- The λ → 0 limit, as a limit: the rental tends to the corner rental. This
is the display `c → ℓr/(1 − a)` of Section 4. -/
theorem c_tendsto_corner (a ℓ ρ r : ℝ) (ha : a < 1) :
    Tendsto (fun lam => cOf a lam ℓ ρ r) (𝓝 0) (𝓝 (ℓ * r / (1 - a))) := by
  have hne : (1 : ℝ) - a - 0 * ρ ≠ 0 := by
    have h : (0 : ℝ) < 1 - a := by linarith
    simpa using h.ne'
  have hc : ContinuousAt (fun lam : ℝ => ℓ * r / (1 - a - lam * ρ)) 0 :=
    ContinuousAt.div (by fun_prop) (by fun_prop) hne
  have h : Tendsto (fun lam : ℝ => ℓ * r / (1 - a - lam * ρ)) (𝓝 0)
      (𝓝 (ℓ * r / (1 - a - 0 * ρ))) := hc.tendsto
  have h0 : ℓ * r / (1 - a - (0:ℝ) * ρ) = ℓ * r / (1 - a) := by norm_num
  rw [h0] at h
  exact h.congr fun _ => rfl

/-! ## §3. Proposition 4(i)–(ii) with λ — the fork -/

/-- Unit price of the machine-made good at parity, `pg = c·ρ̄·L̄`. -/
noncomputable def pg : ℝ := M.c * M.ρ * M.L

lemma pg_pos : 0 < M.pg := mul_pos (mul_pos M.c_pos M.hρ) M.hL

/-- The relative price of non-produced services with λ inside,
`q = (1 − a − λρ̄)/(ℓρ̄L̄)` — Prop 4(ii)'s display. -/
noncomputable def q : ℝ := (1 - M.a - M.lam * M.ρ) / (M.ℓ * M.ρ * M.L)

lemma q_pos : 0 < M.q :=
  div_pos M.denom_pos (mul_pos (mul_pos M.hℓ M.hρ) M.hL)

/-- Prop 4(i): the wage in machine-made goods is absolute solo productivity —
machine quality *and the recipe's labor content* both cancel. λ appears
nowhere in the conclusion. -/
theorem fork_i : M.w / M.pg = 1 / M.L := by
  unfold w pg
  have h1 : M.c ≠ 0 := M.c_pos.ne'
  have h2 : M.ρ ≠ 0 := M.hρ.ne'
  have h3 : M.L ≠ 0 := M.hL.ne'
  field_simp

/-- Prop 4(ii), cost side: `r/pg` is the display. -/
theorem fork_ii : M.r / M.pg = M.q := by
  have h1 : (1 : ℝ) - M.a - M.lam * M.ρ ≠ 0 := M.denom_pos.ne'
  have h2 : M.ℓ ≠ 0 := M.hℓ.ne'
  have h3 : M.ρ ≠ 0 := M.hρ.ne'
  have h4 : M.L ≠ 0 := M.hL.ne'
  have h5 : M.r ≠ 0 := M.hr.ne'
  unfold q pg c
  field_simp

/-- `q` as a free function of the primitives, for statics and limits. -/
noncomputable def qOfL (a lam ℓ ρ L : ℝ) : ℝ := (1 - a - lam * ρ) / (ℓ * ρ * L)

theorem qOfL_eq : M.q = qOfL M.a M.lam M.ℓ M.ρ M.L := rfl

/-- Prop 4(ii): recursive automation (λ ↓) raises the ratio — removing labor
from the recipe is itself a divergence margin. -/
theorem q_strictAnti_in_lam (a ℓ ρ L lam₁ lam₂ : ℝ) (hℓ : 0 < ℓ) (hρ : 0 < ρ)
    (hL : 0 < L) (hlt : lam₁ < lam₂) :
    qOfL a lam₂ ℓ ρ L < qOfL a lam₁ ℓ ρ L := by
  have hd : 0 < ℓ * ρ * L := mul_pos (mul_pos hℓ hρ) hL
  have hstep : lam₁ * ρ < lam₂ * ρ := mul_lt_mul_of_pos_right hlt hρ
  unfold qOfL
  rw [div_lt_div_iff_of_pos_right hd]
  linarith

/-- Prop 4(ii): the closing capability gap (ρ̄ ↓) raises the ratio. Both
points viable, as in the wage statics. -/
theorem q_strictAnti_in_rho (a lam ℓ L ρ₁ ρ₂ : ℝ) (ha : a < 1)
    (hℓ : 0 < ℓ) (hL : 0 < L) (hρ₁ : 0 < ρ₁) (hlt : ρ₁ < ρ₂) :
    qOfL a lam ℓ ρ₂ L < qOfL a lam ℓ ρ₁ L := by
  have hρ₂ : 0 < ρ₂ := lt_trans hρ₁ hlt
  have hd₁ : 0 < ℓ * ρ₁ * L := mul_pos (mul_pos hℓ hρ₁) hL
  have hd₂ : 0 < ℓ * ρ₂ * L := mul_pos (mul_pos hℓ hρ₂) hL
  unfold qOfL
  rw [div_lt_div_iff₀ hd₂ hd₁]
  nlinarith [mul_pos (mul_pos hℓ hL) (mul_pos (sub_pos.mpr hlt) (sub_pos.mpr ha))]

/-- Prop 4(ii), the ρ̄ → 0 margin diverges with λ in place: the constant
`− λ/(ℓL̄)` shift does not tame `(1 − a)/(ℓρ̄L̄)`. -/
theorem q_tendsto_atTop_along_rho (a lam ℓ L : ℝ) (ha : a < 1) (hℓ : 0 < ℓ)
    (hL : 0 < L) :
    Tendsto (fun ρ => qOfL a lam ℓ ρ L) (𝓝[>] 0) atTop := by
  have hc : 0 < (1 - a) / (ℓ * L) := div_pos (by linarith) (mul_pos hℓ hL)
  have h1 : Tendsto (fun ρ : ℝ => (1 - a) / (ℓ * L) * ρ⁻¹) (𝓝[>] 0) atTop :=
    tendsto_inv_nhdsGT_zero.const_mul_atTop hc
  have h2 : Tendsto (fun ρ : ℝ => (1 - a) / (ℓ * L) * ρ⁻¹ + (-(lam / (ℓ * L))))
      (𝓝[>] 0) atTop := tendsto_atTop_add_const_right _ _ h1
  apply h2.congr'
  filter_upwards [self_mem_nhdsWithin] with ρ hρ
  have hρ' : ρ ≠ 0 := (Set.mem_Ioi.mp hρ).ne'
  have hℓ' : ℓ ≠ 0 := hℓ.ne'
  have hL' : L ≠ 0 := hL.ne'
  unfold qOfL
  field_simp
  ring

/-- Prop 4(ii), the ℓ → 0 margin diverges with λ in place as well. -/
theorem q_tendsto_atTop_along_ell (a lam ρ L : ℝ) (hv : a + lam * ρ < 1)
    (hρ : 0 < ρ) (hL : 0 < L) :
    Tendsto (fun ℓ => qOfL a lam ℓ ρ L) (𝓝[>] 0) atTop := by
  have hD : 0 < 1 - a - lam * ρ := by linarith
  have hc : 0 < (1 - a - lam * ρ) / (ρ * L) := div_pos hD (mul_pos hρ hL)
  have h1 : Tendsto (fun ℓ : ℝ => (1 - a - lam * ρ) / (ρ * L) * ℓ⁻¹)
      (𝓝[>] 0) atTop := tendsto_inv_nhdsGT_zero.const_mul_atTop hc
  apply h1.congr'
  filter_upwards [self_mem_nhdsWithin] with e he
  have he' : e ≠ 0 := (Set.mem_Ioi.mp he).ne'
  have hρ' : ρ ≠ 0 := hρ.ne'
  have hL' : L ≠ 0 := hL.ne'
  unfold qOfL
  field_simp

/-- Prop 4(ii), robustness: at λ = 0, machine-for-land substitution in the
recipe (`ℓ = ℓ₀(1 − a)`) leaves the ratio at `1/(ℓ₀ρ̄L̄)`, bounded as `a`
varies — the corner file's `q_bounded_under_substitution`, restated on this
file's `qOfL` so the two displays are the same object. -/
theorem q_substitution (a ℓ₀ ρ L : ℝ) (ha₁ : a < 1) :
    qOfL a 0 (ℓ₀ * (1 - a)) ρ L = 1 / (ℓ₀ * ρ * L) := by
  have h : (1 : ℝ) - a ≠ 0 := (sub_pos.mpr ha₁).ne'
  unfold qOfL
  field_simp
  ring

/-! ## §4. The λ>0 user-cost form (Appendix A, durability)

Sympy-checked first (`check_pinning.py`, the A-usercost block, 2026-08-27);
the paper's durability paragraph previously withheld the λ>0 form as
unverified. `s` is the carrying factor: `s = 1 + δ` for one-period building
under time preference alone, `s = δ + d` for the user-cost reading with wear. -/

/-- The user-cost closure as a free function. -/
noncomputable def ucOf (s a lam ℓ ρ r : ℝ) : ℝ :=
  s * (ℓ * r) / (1 - s * (a + lam * ρ))

/-- The λ>0 user-cost recursion closes at `c = s·ℓr/(1 − s(a + λρ*))`.

MANIFEST: convergence needs `s·(a + λρ*) < 1` — strictly stronger than both
the corner's `a·(δ+d) < 1` (finding 6 of `TheLink`) and the static viability
`a + λρ* < 1` whenever `s > 1`; none of the three implies another in
general. The durable λ>0 reading must carry this and nothing weaker. -/
theorem usercost_closed_form (s c' w' : ℝ)
    (hconv : s * (M.a + M.lam * M.ρ) < 1) (hm : w' = M.ρ * c')
    (hf : c' = s * (M.a * c' + M.lam * w' + M.ℓ * M.r)) :
    c' = ucOf s M.a M.lam M.ℓ M.ρ M.r := by
  have hpos : 0 < 1 - s * (M.a + M.lam * M.ρ) := by linarith
  unfold ucOf
  rw [eq_div_iff hpos.ne']
  linear_combination hf + s * M.lam * hm

/-- `s = 1` recovers the static closure — the flow model is the fully-worn,
zero-interest case. -/
theorem usercost_unit_recovers (a lam ℓ ρ r : ℝ) :
    ucOf 1 a lam ℓ ρ r = cOf a lam ℓ ρ r := by
  have h : (1:ℝ) - 1 * (a + lam * ρ) = 1 - a - lam * ρ := by ring
  unfold ucOf cOf
  rw [one_mul, h]

/-- λ = 0 recovers the corner's stated display for every carrying factor —
both the paper's `s = 1+δ` and `s = δ+d` cases at once. -/
theorem usercost_corner_recovers (s a ℓ ρ r : ℝ) :
    ucOf s a 0 ℓ ρ r = ℓ * r * s / (1 - a * s) := by
  have h1 : s * (ℓ * r) = ℓ * r * s := by ring
  have h2 : (1:ℝ) - s * (a + 0 * ρ) = 1 - a * s := by ring
  unfold ucOf
  rw [h1, h2]

/-! ## §5. Lemma D.2 — the fraud bound -/

/-- Lemma D.2: a premium on verified human work is sustainable iff it runs at
or below `v·f/(1 − v)` — nonpositive expected profit from a false claim,
solved for the premium. -/
theorem lemD2_iff (v f p : ℝ) (hv₁ : v < 1) :
    (1 - v) * p ≤ v * f ↔ p ≤ v * f / (1 - v) := by
  rw [le_div_iff₀ (by linarith : (0:ℝ) < 1 - v), mul_comm]

/-- Lemma D.2: the bound rises in verification power. -/
theorem lemD2_strictMono_in_v (f v₁ v₂ : ℝ) (hf : 0 < f)
    (hlt : v₁ < v₂) (h₁ : v₂ < 1) :
    v₁ * f / (1 - v₁) < v₂ * f / (1 - v₂) := by
  have hd₁ : 0 < 1 - v₁ := by linarith
  have hd₂ : 0 < 1 - v₂ := by linarith
  rw [div_lt_div_iff₀ hd₁ hd₂]
  nlinarith

/-- Lemma D.2: the bound rises in the penalty. -/
theorem lemD2_strictMono_in_f (v f₁ f₂ : ℝ) (hv₀ : 0 < v) (hv₁ : v < 1)
    (hlt : f₁ < f₂) : v * f₁ / (1 - v) < v * f₂ / (1 - v) := by
  have hd : 0 < 1 - v := by linarith
  have hnum : v * f₁ < v * f₂ := mul_lt_mul_of_pos_left hlt hv₀
  rw [div_lt_div_iff_of_pos_right hd]
  exact hnum

/-- Lemma D.2: perfect verification prices the premium out of reach — the
bound diverges as `v → 1⁻`. -/
theorem lemD2_tendsto_atTop_in_v (f : ℝ) (hf : 0 < f) :
    Tendsto (fun v => v * f / (1 - v)) (𝓝[<] (1:ℝ)) atTop := by
  have hmap : Tendsto (fun v : ℝ => 1 - v) (𝓝[<] (1:ℝ)) (𝓝[>] (0:ℝ)) := by
    rw [tendsto_nhdsWithin_iff]
    constructor
    · have h1 : Tendsto (fun v : ℝ => 1 - v) (𝓝 (1:ℝ)) (𝓝 ((1:ℝ) - 1)) :=
        tendsto_const_nhds.sub tendsto_id
      have h : Tendsto (fun v : ℝ => 1 - v) (𝓝 (1:ℝ)) (𝓝 (0:ℝ)) := by
        simpa using h1
      exact h.mono_left nhdsWithin_le_nhds
    · filter_upwards [self_mem_nhdsWithin] with v hv
      exact Set.mem_Ioi.mpr (sub_pos.mpr (Set.mem_Iio.mp hv))
  have hinv : Tendsto (fun v : ℝ => ((1:ℝ) - v)⁻¹) (𝓝[<] (1:ℝ)) atTop :=
    tendsto_inv_nhdsGT_zero.comp hmap
  have hshift : Tendsto (fun v : ℝ => ((1:ℝ) - v)⁻¹ + (-1)) (𝓝[<] (1:ℝ)) atTop :=
    tendsto_atTop_add_const_right _ _ hinv
  have hmul : Tendsto (fun v : ℝ => f * (((1:ℝ) - v)⁻¹ + (-1))) (𝓝[<] (1:ℝ)) atTop :=
    hshift.const_mul_atTop hf
  apply hmul.congr'
  filter_upwards [self_mem_nhdsWithin] with v hv
  have h1 : (1:ℝ) - v ≠ 0 := (sub_pos.mpr (Set.mem_Iio.mp hv)).ne'
  field_simp
  ring

/-- Lemma D.2: with price-only enforcement the bound collapses — at `f = 0`
the sustainable premium is zero for every `v < 1`. -/
theorem lemD2_collapses_at_f_zero (v : ℝ) : v * 0 / (1 - v) = 0 := by simp

/-! ## §6. Lemma D.3 — superstar concentration

The two-point income family: a star set of mass `ε` shares `β·E` of
K-expenditure; the co-present remainder, mass `1 − ε`, shares `(1 − β)·E`
uniformly. The paper's "measure-zero top" is this family's `ε → 0`
idealization.

MANIFEST: two hypotheses the prose leaves implicit. (i) The mean-invariance
is an accounting identity over the family — it needs no distribution theory,
only that expenditure is conserved. (ii) For the base income to sit *below*
the top — for "the top" to be the top — the star mass must run below the
star expenditure share: `ε < β` (`lemD3_top_is_top_iff`). Stars must be
scarcer than their take. At `ε = β` the distribution is flat and there is no
concentration to speak of. -/

/-- Star income in the two-point family. -/
noncomputable def starIncome (β E ε : ℝ) : ℝ := β * E / ε

/-- Co-present (base) income in the two-point family. -/
noncomputable def baseIncome (β E ε : ℝ) : ℝ := (1 - β) * E / (1 - ε)

/-- Lemma D.3: the mean is unchanged — total income is total expenditure at
every star mass. -/
theorem lemD3_mean_invariant (β E ε : ℝ) (hε₀ : 0 < ε) (hε₁ : ε < 1) :
    ε * starIncome β E ε + (1 - ε) * baseIncome β E ε = E := by
  have h1 : ε ≠ 0 := hε₀.ne'
  have h2 : (1:ℝ) - ε ≠ 0 := (sub_pos.mpr hε₁).ne'
  unfold starIncome baseIncome
  field_simp
  ring

/-- Lemma D.3: the top is the top exactly when stars are scarcer than their
expenditure share. -/
theorem lemD3_top_is_top_iff (β E ε : ℝ) (hE : 0 < E) (hε₀ : 0 < ε)
    (hε₁ : ε < 1) : baseIncome β E ε < starIncome β E ε ↔ ε < β := by
  unfold starIncome baseIncome
  rw [div_lt_div_iff₀ (sub_pos.mpr hε₁) hε₀]
  constructor <;> intro h <;> nlinarith

/-- Lemma D.3: for `ε < 1/2` the base income is a median — all but mass `ε`
of the workforce earns exactly it, so the sub-`base` mass `1 − ε` clears
one-half. -/
theorem lemD3_base_is_median_mass (ε : ℝ) (hε : ε < 1/2) : (1:ℝ)/2 < 1 - ε := by
  linarith

/-- Lemma D.3, the statement used in the paper: median over mean tends to
`1 − β` as the star set's mass vanishes. -/
theorem lemD3_ratio_tendsto (β E : ℝ) (hE : 0 < E) :
    Tendsto (fun ε => baseIncome β E ε / E) (𝓝[>] 0) (𝓝 (1 - β)) := by
  have hne : (1 : ℝ) - (0:ℝ) ≠ 0 := by norm_num
  have hc : ContinuousAt (fun ε : ℝ => (1 - β) * E / (1 - ε) / E) 0 :=
    ContinuousAt.div (ContinuousAt.div (by fun_prop) (by fun_prop) hne)
      (by fun_prop) hE.ne'
  have h : Tendsto (fun ε : ℝ => (1 - β) * E / (1 - ε) / E) (𝓝 0)
      (𝓝 ((1 - β) * E / (1 - (0:ℝ)) / E)) := hc.tendsto
  have h0 : (1 - β) * E / (1 - (0:ℝ)) / E = 1 - β := by
    have hE' : E ≠ 0 := hE.ne'
    field_simp
    ring
  rw [h0] at h
  exact (h.mono_left nhdsWithin_le_nhds).congr fun _ => rfl

/-! ## §7. The CES dial (Appendix B, the General-η display)

`s_h(q) = σq^(1−η)/(σq^(1−η) + 1 − σ)` and its three-case limit — the
paper's complements/knife-edge/substitutes trichotomy. -/

/-- The land expenditure share under CES. -/
noncomputable def shOf (σ η q : ℝ) : ℝ :=
  σ * q ^ (1 - η) / (σ * q ^ (1 - η) + (1 - σ))

/-- η < 1 (complements): housing takes the whole budget — the share tends to
one as `q` diverges, and the fork binds. -/
theorem sh_tendsto_one (σ η : ℝ) (hσ₀ : 0 < σ) (hσ₁ : σ < 1) (hη : η < 1) :
    Tendsto (shOf σ η) atTop (𝓝 1) := by
  have hu : Tendsto (fun q : ℝ => q ^ (1 - η)) atTop atTop :=
    tendsto_rpow_atTop (by linarith)
  have hden : Tendsto (fun q : ℝ => σ * q ^ (1 - η) + (1 - σ)) atTop atTop :=
    tendsto_atTop_add_const_right _ _ (hu.const_mul_atTop hσ₀)
  have hfrac : Tendsto (fun q : ℝ => (1 - σ) / (σ * q ^ (1 - η) + (1 - σ)))
      atTop (𝓝 0) := by
    have := hden.inv_tendsto_atTop
    simpa [div_eq_mul_inv] using this.const_mul (1 - σ)
  have hone : Tendsto (fun q : ℝ => 1 - (1 - σ) / (σ * q ^ (1 - η) + (1 - σ)))
      atTop (𝓝 1) := by
    have h1 : Tendsto (fun q : ℝ => 1 - (1 - σ) / (σ * q ^ (1 - η) + (1 - σ)))
        atTop (𝓝 ((1:ℝ) - 0)) := tendsto_const_nhds.sub hfrac
    simpa using h1
  apply hone.congr'
  filter_upwards [eventually_gt_atTop 0] with q hq
  have hup : (0:ℝ) < q ^ (1 - η) := Real.rpow_pos_of_pos hq _
  have hd : (0:ℝ) < σ * q ^ (1 - η) + (1 - σ) := by
    have h1 : (0:ℝ) < σ * q ^ (1 - η) := mul_pos hσ₀ hup
    linarith
  unfold shOf
  field_simp
  ring

/-- η > 1 (substitutes): substitution defuses the fork — the share tends to
zero. -/
theorem sh_tendsto_zero (σ η : ℝ) (_hσ₀ : 0 < σ) (hσ₁ : σ < 1) (hη : 1 < η) :
    Tendsto (shOf σ η) atTop (𝓝 0) := by
  have hu : Tendsto (fun q : ℝ => q ^ (1 - η)) atTop (𝓝 0) := by
    have h := tendsto_rpow_neg_atTop (y := η - 1) (by linarith)
    have hexp : ∀ q : ℝ, q ^ (-(η - 1)) = q ^ (1 - η) := by
      intro q; congr 1; ring
    simpa [hexp] using h
  have hnum : Tendsto (fun q : ℝ => σ * q ^ (1 - η)) atTop (𝓝 0) := by
    simpa using hu.const_mul σ
  have hden : Tendsto (fun q : ℝ => σ * q ^ (1 - η) + (1 - σ)) atTop (𝓝 (1 - σ)) := by
    have h1 : Tendsto (fun q : ℝ => σ * q ^ (1 - η) + (1 - σ)) atTop
        (𝓝 ((0:ℝ) + (1 - σ))) := hnum.add tendsto_const_nhds
    simpa using h1
  have hne : (1:ℝ) - σ ≠ 0 := (sub_pos.mpr hσ₁).ne'
  have h : Tendsto ((fun q : ℝ => σ * q ^ (1 - η)) / fun q : ℝ =>
      σ * q ^ (1 - η) + (1 - σ)) atTop (𝓝 0) := by
    simpa using hnum.div hden hne
  exact h.congr fun _ => rfl

/-- η = 1 (the knife edge): the share is the taste weight at every `q` — no
positivity needed anywhere (see manifest note P5). -/
theorem sh_const_at_eta_one (σ q : ℝ) : shOf σ 1 q = σ := by
  unfold shOf
  rw [show (1:ℝ) - 1 = 0 from by norm_num, Real.rpow_zero, mul_one]
  rw [show σ + (1 - σ) = 1 from by ring, div_one]

end Spine

end Link

/-
## The manifest — pinning extension

What writing the λ>0 statements down surfaced, beyond `TheLink.lean`'s nine.

P1. **Viability is one condition, and it is the strongest one in play.**
    `a + λρ* < 1` implies `a < 1` (`a_lt_one`) but not conversely; the
    user-cost reading needs `s(a + λρ*) < 1`, strictly stronger again for
    `s > 1`, and implying neither the static viability alone nor the
    corner's `a(δ+d) < 1` in isolation. The paper's durability paragraph now
    states the λ>0 form; it should carry this condition and nothing weaker
    (`usercost_closed_form`).

P2. **The comparative statics need viability at the upper comparison point
    only.** `w_strictMono_in_lam` consumes `a + lam₂·ρ < 1` and derives the
    lower point's viability from it. The paper's "on the viable set" is
    correct but does not say which endpoint binds.

P3. **Prop 4(i) is λ-free all the way down.** The wage in machine-made goods
    is `1/L̄` with the recipe's labor content cancelling alongside machine
    quality (`fork_i`) — the Caselli–Manning concession survives the λ>0
    generalization with no new hypothesis. Worth one clause in the paper if
    a referee asks whether the concession was corner-specific.

P4. **Lemma D.3's "measure-zero top" hides an ordering hypothesis.** For the
    star income to sit above the base income the star mass must run below
    the star expenditure share, `ε < β` (`lemD3_top_is_top_iff`) — stars
    scarcer than their take. The prose says "concentrates on top
    performers"; the formal content of "top" is exactly `ε < β`. And the
    mean-invariance is bookkeeping (`lemD3_mean_invariant`), not
    distribution theory — the lemma's force is entirely in the median's
    location, which is where the paper puts it.

P5. **The CES dial's knife edge needs no positivity.** `sh_const_at_eta_one`
    holds for every `q` including `q ≤ 0` — an artefact of `rpow`'s junk
    values, same family as `TheLink` finding 7's `x/0 = 0` artefacts; not
    a finding about the economics.
-/
