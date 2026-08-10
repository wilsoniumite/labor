/-
# The Link — corner-regime spine, as Lean 4 statements

STATUS: builds clean — Lean 4.33.0, mathlib v4.33.0, zero errors, zero `sorry`.

SCOPE: the corner-regime spine only — Propositions 3, 4, 5, 6(i), 7(i)–(ii), 8,
9(ii)–(iii), 10, 13(ii). That is the chain running

    machines make machines  (3)
  → the value lands on sites  (4, 5)
  → the wage column empties  (6, 7)
  → the rent column can fund the floor  (8, 9)
  → the mix on the way down  (10)
  → redistribution without deadweight  (13ii)

Deliberately omitted: Props 1–2 (equilibrium existence/stability — needs a large
definitional apparatus for little return), Prop 11 (the Baumol fork — `rpow`
limit tedium), Prop 12 (open economy — mostly verbal), and the uniqueness
converses 7(iii) and 13(iii), which are **not formalizable in principle**: they
quantify over fiscal instruments *in the world*, not over a defined set. Encoding
the instrument set as an inductive type would make those theorems true by
construction and worth nothing. The paper already hedges 7(iii) correctly.

PURPOSE: this file is not for certifying the algebra — `checks/*.py` already does
that with sympy. It exists to produce the **assumption manifest**: the complete,
enumerated list of hypotheses each proposition actually consumes. Every place
where writing this down forced a hypothesis the prose leaves implicit is marked

    -- MANIFEST:

and the findings are collected at the bottom of the file.

A caveat no proof assistant removes: the statements below are a *translation* of
the paper. Lean checks the derivations, not the translation. A mistranscribed
proposition yields a true theorem about the wrong claim.

Notation follows `checks/` and the paper: `a` machine-services recipe share,
`ℓ` non-produced services per unit machine services, `ρ` the flat effective
capability ratio ρ̄, `L` the solo labour requirement L̄, `σ` the Cobb-Douglas land
share, `q = r/pg`.
-/

import Mathlib

namespace Link

open Filter Topology

/-! ## §0. Primitives

The corner regime as a single structure. Every standing hypothesis of Sections
5–7 is a field, so that no proposition below can quietly consume one that isn't
listed here. -/

/-- Corner-regime primitives (δ = 0; the interest sliver is suppressed, as in
Prop 5's setup). -/
structure Corner where
  /-- machine services required per unit of machine services -/
  a : ℝ
  /-- non-produced services (sites, energy, ore) per unit of machine services -/
  ℓ : ℝ
  /-- the flat effective capability ratio ρ̄ = γL/γM -/
  ρ : ℝ
  /-- L̄ = ∫dx/γL(x), the labour one human needs for the whole checklist -/
  L : ℝ
  /-- land stock -/
  T : ℝ
  /-- land rental -/
  r : ℝ
  /-- Cobb-Douglas expenditure share on direct land services -/
  σ : ℝ
  /-- population -/
  N : ℝ
  -- MANIFEST: `0 < a` is never stated in the paper. Prop 3 needs only `a < 1`
  -- (net reproduction). `0 < a` is used by Prop 4(ii)'s *bounded* claim along
  -- the a-margin (`q < 1/(ℓρL)`); without it that bound is not strict.
  ha₀ : 0 < a
  /-- machines net-reproduce; without this `c` is infinite -/
  ha₁ : a < 1
  hℓ : 0 < ℓ
  hρ : 0 < ρ
  hL : 0 < L
  hT : 0 < T
  hr : 0 < r
  hσ₀ : 0 < σ
  hσ₁ : σ < 1
  hN : 0 < N

namespace Corner

variable (M : Corner)

/-- Machine rental (Prop 3). -/
noncomputable def c : ℝ := M.ℓ * M.r / (1 - M.a)

/-- Unit price of the machine-made final good, `pg = c·ρ̄·L̄`. -/
noncomputable def pg : ℝ := M.c * M.ρ * M.L

/-- Relative price of land services in goods, `q = r/pg` (Prop 4(ii)).

MANIFEST: note what is *absent* on the right-hand side — `r` does not appear.
In the corner, `q` is a pure technology ratio. No fiscal action can move it.
That is stronger than the paper says out loud, and it is what rescues Prop 8
from the price-feedback worry the appendix flags as "tendency, not theorem":
the fundability condition (`prop8_iii_land_constraint`) is stated in `q` and
quantities alone, so it is invariant to the transfer's effect on `r`. -/
noncomputable def q : ℝ := (1 - M.a) / (M.ℓ * M.ρ * M.L)

/-! ### Positivity

Unglamorous, and the single largest source of Lean-side friction: every division
below needs these threaded explicitly. -/

lemma one_sub_a_pos : 0 < 1 - M.a := sub_pos.mpr M.ha₁

lemma ellrhoL_pos : 0 < M.ℓ * M.ρ * M.L := mul_pos (mul_pos M.hℓ M.hρ) M.hL

lemma c_pos : 0 < M.c := div_pos (mul_pos M.hℓ M.hr) M.one_sub_a_pos

lemma pg_pos : 0 < M.pg := mul_pos (mul_pos M.c_pos M.hρ) M.hL

lemma q_pos : 0 < M.q := div_pos M.one_sub_a_pos M.ellrhoL_pos

/-! ### The corner allocation (Prop 5(i)) -/

/-- Housing land. -/
noncomputable def TH : ℝ := M.σ * M.T

/-- Production land. -/
noncomputable def TP : ℝ := (1 - M.σ) * M.T

/-- Final output. -/
noncomputable def Y : ℝ := (1 - M.a) * (1 - M.σ) * M.T / (M.ℓ * M.ρ * M.L)

/-- Gross machine services, including services consumed making services. -/
noncomputable def X : ℝ := M.ρ * M.L * M.Y / (1 - M.a)

/-! ## §1. Proposition 3 — value collapse -/

/-- Prop 3, free entry: the machine rental satisfies its own recipe. -/
theorem prop3_zero_profit : M.c = M.a * M.c + M.ℓ * M.r := by
  have h : (1 : ℝ) - M.a ≠ 0 := M.one_sub_a_pos.ne'
  unfold c
  field_simp
  ring

/-- Prop 3, uniqueness: `c` is the only price satisfying free entry. -/
theorem prop3_unique (c' : ℝ) (h : c' = M.a * c' + M.ℓ * M.r) : c' = M.c := by
  have hne : (1 : ℝ) - M.a ≠ 0 := M.one_sub_a_pos.ne'
  unfold c
  rw [eq_div_iff hne]
  linear_combination h

/-- Prop 3 with time preference δ and wear `d` (the user-cost recursion).

MANIFEST: convergence needs `a·(δ+d) < 1`, a *strictly stronger* condition than
the `a < 1` carried in the structure. The paper states it for the δ-only case
("finite iff a(1+δ) < 1") and then presents the durability generalisation
without restating it. Anywhere the durable reading is in force, `ha₁` is not
enough. -/
theorem prop3_user_cost (δ d : ℝ) (_hδ : 0 ≤ δ) (_hd : 0 < d)
    (hconv : M.a * (δ + d) < 1) (c' : ℝ)
    (h : c' = M.a * (δ + d) * c' + M.ℓ * M.r * (δ + d)) :
    c' = M.ℓ * M.r * (δ + d) / (1 - M.a * (δ + d)) := by
  have hpos : 0 < 1 - M.a * (δ + d) := by linarith
  rw [eq_div_iff hpos.ne']
  linear_combination h

/-- The one-period case `d = 1, δ = 0` recovers `M.c`. -/
theorem prop3_user_cost_recovers :
    M.ℓ * M.r * (0 + 1) / (1 - M.a * (0 + 1)) = M.c := by
  unfold c; norm_num

/-! ## §2. Proposition 4 — real wages and the land content of subsistence -/

/-- Prop 4(i): the real wage in machine-made goods is absolute solo
productivity; the machine rental cancels.

MANIFEST: this is a **corner-ABOVE** statement — it presupposes labour still
employed at parity, so that a wage exists at all. Prop 5 below is stated for the
corner with labour exited ("labour has exited, or is of negligible measure").
The two cannot share a `Corner` structure without a sub-regime flag. The paper
carries this in an appendix remark rather than in the propositions; in Lean the
split is forced, because `w` has nowhere to live in the corner-below structure. -/
theorem prop4_i (w : ℝ) (hw : w = M.c * M.ρ) : w / M.pg = 1 / M.L := by
  subst hw
  unfold pg
  have h1 : M.c ≠ 0 := M.c_pos.ne'
  have h2 : M.ρ ≠ 0 := M.hρ.ne'
  have h3 : M.L ≠ 0 := M.hL.ne'
  field_simp

/-- Prop 4(ii), cost side. -/
theorem prop4_ii : M.r / M.pg = M.q := by
  have h1 : (1 : ℝ) - M.a ≠ 0 := M.one_sub_a_pos.ne'
  have h2 : M.ℓ ≠ 0 := M.hℓ.ne'
  have h3 : M.ρ ≠ 0 := M.hρ.ne'
  have h4 : M.L ≠ 0 := M.hL.ne'
  have h5 : M.r ≠ 0 := M.hr.ne'
  unfold q pg c
  field_simp

/-- `q` as a free function of the primitives, for the limit statements. -/
noncomputable def qOf (a ℓ ρ L : ℝ) : ℝ := (1 - a) / (ℓ * ρ * L)

/-- Prop 4(ii), the ρ̄ → 0 margin: closing the task-side edge sends the relative
price of land to infinity. -/
theorem q_tendsto_atTop_along_rho (a ℓ L : ℝ) (ha : a < 1) (hℓ : 0 < ℓ) (hL : 0 < L) :
    Tendsto (fun ρ => qOf a ℓ ρ L) (𝓝[>] 0) atTop := by
  have hc : 0 < (1 - a) / (ℓ * L) := div_pos (by linarith) (mul_pos hℓ hL)
  apply (tendsto_inv_nhdsGT_zero.const_mul_atTop hc).congr'
  filter_upwards [self_mem_nhdsWithin] with ρ hρ
  have hρ' : ρ ≠ 0 := (Set.mem_Ioi.mp hρ).ne'
  have hℓ' : ℓ ≠ 0 := hℓ.ne'
  have hL' : L ≠ 0 := hL.ne'
  unfold qOf
  field_simp

/-- Prop 4(ii), the ℓ → 0 margin. -/
theorem q_tendsto_atTop_along_ell (a ρ L : ℝ) (ha : a < 1) (hρ : 0 < ρ) (hL : 0 < L) :
    Tendsto (fun ℓ => qOf a ℓ ρ L) (𝓝[>] 0) atTop := by
  have hc : 0 < (1 - a) / (ρ * L) := div_pos (by linarith) (mul_pos hρ hL)
  apply (tendsto_inv_nhdsGT_zero.const_mul_atTop hc).congr'
  filter_upwards [self_mem_nhdsWithin] with e he
  have he' : e ≠ 0 := (Set.mem_Ioi.mp he).ne'
  have hρ' : ρ ≠ 0 := hρ.ne'
  have hL' : L ≠ 0 := hL.ne'
  unfold qOf
  field_simp

/-- Prop 4(ii), the a-margin is **bounded** — the paper's own catch, and the
reason the three margins are not interchangeable.

MANIFEST: `_ha₁ : a < 1` is stated but unused. The bound needs only `0 < a`. -/
theorem q_bounded_along_a (a ℓ ρ L : ℝ) (ha₀ : 0 < a) (_ha₁ : a < 1)
    (hℓ : 0 < ℓ) (hρ : 0 < ρ) (hL : 0 < L) :
    qOf a ℓ ρ L < 1 / (ℓ * ρ * L) := by
  have hd : 0 < ℓ * ρ * L := mul_pos (mul_pos hℓ hρ) hL
  unfold qOf
  rw [div_lt_div_iff_of_pos_right hd]
  linarith

/-- Prop 4(ii), regress: `a → 1` sends machine costs, not rents, to infinity. -/
theorem q_tendsto_zero_along_a (ℓ ρ L : ℝ) (_hℓ : 0 < ℓ) (_hρ : 0 < ρ) (_hL : 0 < L) :
    Tendsto (fun a => qOf a ℓ ρ L) (𝓝[<] 1) (𝓝 0) := by
  have h : Tendsto (fun a : ℝ => qOf a ℓ ρ L) (𝓝 1) (𝓝 0) := by
    have hz : ((1 : ℝ) - 1) / (ℓ * ρ * L) = 0 := by simp
    unfold qOf
    rw [← hz]
    exact (tendsto_const_nhds.sub tendsto_id).div_const _
  exact h.mono_left nhdsWithin_le_nhds

/-- Prop 4(ii), machine-for-land substitution inside the recipe (`ℓ = ℓ₀(1-a)`)
leaves `q` bounded. -/
theorem q_bounded_under_substitution (a ℓ₀ ρ L : ℝ) (ha₁ : a < 1)
    (_hℓ : 0 < ℓ₀) (_hρ : 0 < ρ) (_hL : 0 < L) :
    qOf a (ℓ₀ * (1 - a)) ρ L = 1 / (ℓ₀ * ρ * L) := by
  have h : (1 : ℝ) - a ≠ 0 := (sub_pos.mpr ha₁).ne'
  unfold qOf
  field_simp

/-- The geometric price index of Prop 4(iii).

MANIFEST: **asserted in the paper, not derived.** It appears inside the proof of
4(iii) ("A geometric price index P = pg^(1−σ)·r^σ gives …"). It *is* derivable
from Cobb-Douglas expenditure minimisation, but only up to a multiplicative
constant `σ^(-σ)(1-σ)^(σ-1)`, which is silently dropped. Harmless for the limit
claim (a positive constant does not change what tends to zero) but it means
`P` is a definition here, not a consequence. -/
noncomputable def P (s : ℝ) : ℝ := M.pg ^ (1 - s) * M.r ^ s

/-- Prop 4(iii), the decomposition.

MANIFEST: `s` here is the expenditure share on non-produced services in the
*price index*. The paper writes it `σ`, the same letter as the representative
household's Cobb-Douglas share in Prop 5. Whether they are the same object is
never stated. They are separate arguments here on purpose — see the manifest
note at the foot of the file. -/
theorem prop4_iii_decomp (w s : ℝ) (hw : w = M.c * M.ρ) (_hs₀ : 0 < s) (_hs₁ : s < 1) :
    w / M.P s = (1 / M.L) * (M.pg / M.r) ^ s := by
  subst hw
  have hpg := M.pg_pos
  have hrr := M.hr
  have hpg' : M.pg ≠ 0 := hpg.ne'
  have hL' : M.L ≠ 0 := M.hL.ne'
  have hps : (0 : ℝ) < M.pg ^ s := Real.rpow_pos_of_pos hpg s
  have hrs : (0 : ℝ) < M.r ^ s := Real.rpow_pos_of_pos hrr s
  have hps' : M.pg ^ s ≠ 0 := hps.ne'
  have hrs' : M.r ^ s ≠ 0 := hrs.ne'
  have hcr : M.c * M.ρ = M.pg / M.L := by unfold pg; field_simp
  unfold P
  rw [Real.rpow_sub hpg, Real.rpow_one, Real.div_rpow hpg.le hrr.le, hcr]
  field_simp

/-- Prop 4(iii), the collapse: with any positive land share in the bundle, the
real wage goes to zero along the divergent margins. Stated on the reduced form
`w/P = (1/L)·q^(-s)`, which is what `prop4_iii_decomp` delivers.

MANIFEST: `_hL` and `_hs₁` are stated but unused — the collapse needs only
`0 < s`. The upper bound `s < 1` does no work here. -/
theorem prop4_iii_collapse (L s : ℝ) (_hL : 0 < L) (hs₀ : 0 < s) (_hs₁ : s < 1) :
    Tendsto (fun q : ℝ => (1 / L) * q ^ (-s)) atTop (𝓝 0) := by
  simpa using (tendsto_rpow_neg_atTop hs₀).const_mul (1 / L)

/-- Prop 4(iii), the boundary case: at `s = 0` the real wage is bounded at `1/L̄`. -/
theorem prop4_iii_bounded_at_zero (L : ℝ) (_hL : 0 < L) :
    ∀ q : ℝ, 0 < q → (1 / L) * q ^ (-(0:ℝ)) = 1 / L := by
  intro q _
  rw [neg_zero, Real.rpow_zero, mul_one]

/-! ## §3. Proposition 5 — closure and conservation of rents -/

/-- Prop 5(i), land clearing. -/
theorem prop5_i_land_clearing : M.TP + M.TH = M.T := by
  unfold TP TH; ring

/-- Prop 5(i), Cobb-Douglas goods demand equals the claimed output. -/
theorem prop5_i_goods_demand : (1 - M.σ) * (M.r * M.T) / M.pg = M.Y := by
  have h1 : (1 : ℝ) - M.a ≠ 0 := M.one_sub_a_pos.ne'
  have h2 : M.ℓ ≠ 0 := M.hℓ.ne'
  have h3 : M.ρ ≠ 0 := M.hρ.ne'
  have h4 : M.L ≠ 0 := M.hL.ne'
  have h5 : M.r ≠ 0 := M.hr.ne'
  unfold pg c Y
  field_simp

/-- Prop 5(i), Cobb-Douglas housing demand equals the claimed housing land. -/
theorem prop5_i_housing_demand : M.σ * (M.r * M.T) / M.r = M.TH := by
  have h5 : M.r ≠ 0 := M.hr.ne'
  unfold TH
  field_simp

/-- The machine-services gross-up solves its own recursion. -/
theorem prop5_gross_up : M.X = M.ρ * M.L * M.Y + M.a * M.X := by
  have h1 : (1 : ℝ) - M.a ≠ 0 := M.one_sub_a_pos.ne'
  unfold X
  field_simp
  ring

/-- Production land demand exhausts production land. -/
theorem prop5_production_land : M.ℓ * M.X = M.TP := by
  have h1 : (1 : ℝ) - M.a ≠ 0 := M.one_sub_a_pos.ne'
  have h2 : M.ℓ ≠ 0 := M.hℓ.ne'
  have h3 : M.ρ ≠ 0 := M.hρ.ne'
  have h4 : M.L ≠ 0 := M.hL.ne'
  unfold X Y TP
  field_simp

/-- Prop 5(ii), first identity: the entire goods bill is production-land rent. -/
theorem prop5_ii_goods_bill : M.pg * M.Y = M.r * M.TP := by
  have h1 : (1 : ℝ) - M.a ≠ 0 := M.one_sub_a_pos.ne'
  have h2 : M.ℓ ≠ 0 := M.hℓ.ne'
  have h3 : M.ρ ≠ 0 := M.hρ.ne'
  have h4 : M.L ≠ 0 := M.hL.ne'
  unfold pg c Y TP
  field_simp

/-- Prop 5(ii), second identity: **national income is aggregate site rent**.
The conservation law. This is the load-bearing statement of Section 5 and the
one a reader is most likely to suspect of sleight of hand ("dissipation is
migration, by construction"). -/
theorem prop5_ii_conservation : M.pg * M.Y + M.r * M.TH = M.r * M.T := by
  have h1 : (1 : ℝ) - M.a ≠ 0 := M.one_sub_a_pos.ne'
  have h2 : M.ℓ ≠ 0 := M.hℓ.ne'
  have h3 : M.ρ ≠ 0 := M.hρ.ne'
  have h4 : M.L ≠ 0 := M.hL.ne'
  unfold pg c Y TH
  field_simp
  ring

/-- Prop 5(iii), the demand side reproduces the cost-side relative price.

MANIFEST: in this formalisation `prop5_iii` and `prop4_ii` are the *same
statement* — `pg` is defined from `c`, `c` from the zero-profit condition, and
`q` from the technology, so the "demand-side derivation" is definitional
unfolding. The paper says as much ("prices are cost-determined, so the
demand-side derivation is not a test the model could have failed"), and the
formalisation confirms the hedge rather than the claim. Kept as a separate
theorem only to mirror the paper's numbering — and note the proof is literally
`prop4_ii`, which is the finding. -/
theorem prop5_iii : M.r / M.pg = M.q := M.prop4_ii

/-! ## §4. Proposition 6(i) — conditionality: the cancellation

The paper's most consequential single claim, and — as predicted — its formal
content is one lemma about adding the same real to both sides. Lean certifies
nothing here that was ever in doubt. Included because the *statement* is the
thing worth pinning down: what cancels, and against what. -/

/-- Prop 6(i): an unconditional transfer enters both sides of the participation
comparison and cancels. Moves no margin. -/
theorem prop6_i_cancel (w s u : ℝ) : s + u ≤ w + u ↔ s ≤ w := add_le_add_iff_right u

/-- Prop 6(i): the disposable floor rises by exactly `u`. -/
theorem prop6_i_floor (s u : ℝ) : (s + u) - s = u := by ring

/-- An instrument as the pair (payment while working, payment while not). -/
structure Instrument where
  mw : ℝ
  me : ℝ

/-- The wedge the participation margin can actually see. -/
def Instrument.Δ (I : Instrument) : ℝ := I.mw - I.me

/-- Reservation wage. `s` is the exit option as a function of unearned cash in
the exit state; `s' ≥ 0` (leisure normal) is the income channel. -/
noncomputable def R (s : ℝ → ℝ) (y : ℝ) (Δ : ℝ) : ℝ := s y - Δ

/-- The decomposition of the Prop 6 remark: the margin sees only `Δ`, never the
pair. Two instruments with equal `Δ` are indistinguishable to participation
however differently they are labelled. -/
theorem prop6_margin_sees_only_delta (s : ℝ → ℝ) (y : ℝ) (I J : Instrument)
    (h : I.Δ = J.Δ) : R s y I.Δ = R s y J.Δ := by rw [h]

/-- The unconditional transfer is the unique instrument with `Δ = 0`. -/
theorem prop6_unconditional_delta_zero (u : ℝ) : (Instrument.mk u u).Δ = 0 := by
  simp [Instrument.Δ]

/-- `∂R/∂Δ = -1`: the substitution channel, always at full strength. -/
theorem prop6_dR_dDelta (s : ℝ → ℝ) (y : ℝ) :
    deriv (R s y) = fun _ => (-1 : ℝ) := by
  funext Δ
  unfold R
  exact deriv_const_sub_id _

/-- The compensated participation response to `u` is zero **as an identity** —
not as an empirical near-zero. -/
theorem prop6_u_compensated_zero (s : ℝ → ℝ) (y u : ℝ) :
    R s y (Instrument.mk u u).Δ = s y := by simp [R, Instrument.Δ]

/-! ## §5. Proposition 7 — funding -/

/-- Prop 7(i), full participation: a wage-funded universal transfer in the
corner is a closed loop through the same pockets, for **every** rate. -/
theorem prop7_i_shell (t : ℝ) :
    (1 - t) * (M.c * M.ρ) + t * (M.c * M.ρ) = M.c * M.ρ := by ring

-- MANIFEST: `_hn₀ : 0 < n` is stated but never used — the strict inequality
-- holds for any participation fraction below one, positive or not.
/-- Prop 7(i), partial participation: with a participating fraction `n < 1` the
tax falls on fewer than it pays, and disposable income drops strictly below
parity for every positive rate. -/
theorem prop7_i_partial (t n : ℝ) (ht : 0 < t) (_hn₀ : 0 < n) (hn₁ : n < 1) :
    (1 - t) * (M.c * M.ρ) + t * (M.c * M.ρ) * n < M.c * M.ρ := by
  have hcp : 0 < M.c * M.ρ := mul_pos M.c_pos M.hρ
  nlinarith [mul_pos ht hcp]

/-- Prop 7(ii), stated honestly as an **assumption bundle rather than a
theorem**.

MANIFEST: this is the sharpest instance of the manifest's point. The paper
argues 7(ii) from the standard result ("land's supply is fixed and its rent is a
residual, so a tax on site rent capitalises into the land price while leaving the
rent flow and land use unchanged"). But the corner model as written has **no
land-pricing equation and no land-use margin** — `TP` and `TH` are pinned by
Cobb-Douglas shares, and no asset price appears anywhere. So the invariance
cannot be derived here; it can only be assumed. Writing it as a structure makes
the assumption nameable and attackable, which is the entire point of the
exercise. Deriving it would mean *adding a model* (asset pricing as the present
value of the rent flow, plus a development or improvement margin), not proving a
theorem about the existing one.

Note also `flow_invariant` is doing more work than "supply is fixed": it also
requires that site value be separable from improvement value, since a tax that
touched improvements would move a real margin. The paper flags assessment
separability as a *practical* caveat; here it is load-bearing *theoretically*. -/
structure LandTaxInvariance (M : Corner) where
  /-- rent flow as a function of the land-tax rate -/
  rentFlow : ℝ → ℝ
  /-- land use `(TP, TH)` as a function of the land-tax rate -/
  landUse : ℝ → ℝ × ℝ
  flow_invariant : ∀ t, 0 ≤ t → t ≤ 1 → rentFlow t = M.r * M.T
  use_invariant : ∀ t, 0 ≤ t → t ≤ 1 → landUse t = (M.TP, M.TH)

/-- Prop 7(ii): given the invariance, the base cannot contract in response to
being taxed, so revenue is exactly linear in the rate. -/
theorem prop7_ii_base_cannot_contract (I : LandTaxInvariance M) (t : ℝ)
    (h₀ : 0 ≤ t) (h₁ : t ≤ 1) : t * I.rentFlow t = t * (M.r * M.T) := by
  rw [I.flow_invariant t h₀ h₁]

/-- Prop 7(ii) + 6(i): the conjunction that *is* the theorem — untaxable-away
base, distortion-free transfer. -/
theorem prop7_ii_conjunction (I : LandTaxInvariance M) (t w s : ℝ)
    (h₀ : 0 ≤ t) (h₁ : t ≤ 1) :
    t * I.rentFlow t = t * (M.r * M.T) ∧
      (s + t * (M.r * M.T) / M.N ≤ w + t * (M.r * M.T) / M.N ↔ s ≤ w) :=
  ⟨by rw [I.flow_invariant t h₀ h₁], add_le_add_iff_right _⟩

/-! ## §6. Proposition 8 — feasibility of the rent-funded floor -/

/-- Per-person cost of the subsistence bundle `(gs, hs)`.

MANIFEST: a bundle of **fixed quantities**, not fixed shares. Its implied land
share `r·hs/Ps = q·hs/(gs + q·hs)` therefore *varies with q*, while the
representative household's `σ` is constant by Cobb-Douglas. These are different
kinds of object and the paper's shared `σ` notation obscures it. Coherent as
written — a poverty line is a physical bundle — but it should be said. -/
noncomputable def Ps (gs hs : ℝ) : ℝ := M.pg * gs + M.r * hs

/-- Coverage ratio at full capture: the per-head dividend from total site rent,
against the price of one subsistence bundle. -/
noncomputable def κ (gs hs : ℝ) : ℝ := M.r * M.T / (M.N * M.Ps gs hs)

/-- Prop 8(i): the coverage ratio in terms of `q` alone. -/
theorem prop8_i_formula (gs hs : ℝ) (hgs : 0 < gs) (hhs : 0 < hs) :
    M.κ gs hs = M.q * M.T / (M.N * (gs + M.q * hs)) := by
  have hq : M.q = M.r / M.pg := M.prop4_ii.symm
  have hpg : M.pg ≠ 0 := M.pg_pos.ne'
  have hN : M.N ≠ 0 := M.hN.ne'
  have hb : gs + M.q * hs ≠ 0 := (add_pos hgs (mul_pos M.q_pos hhs)).ne'
  have hPs : M.Ps gs hs ≠ 0 :=
    (add_pos (mul_pos M.pg_pos hgs) (mul_pos M.hr hhs)).ne'
  unfold κ Ps
  rw [hq] at hb ⊢
  field_simp at hb ⊢

/-- κ as a free function of `q`, for monotonicity and limits. -/
noncomputable def kappaOf (T N gs hs q : ℝ) : ℝ := q * T / (N * (gs + q * hs))

/-- Prop 8(i): strictly increasing in `q`. The demolition funds its own remedy. -/
theorem prop8_i_strictMono (T N gs hs : ℝ) (hT : 0 < T) (hN : 0 < N)
    (hgs : 0 < gs) (hhs : 0 < hs) :
    StrictMonoOn (kappaOf T N gs hs) (Set.Ioi 0) := by
  intro x hx y hy hxy
  simp only [Set.mem_Ioi] at hx hy
  have hdx : 0 < N * (gs + x * hs) := mul_pos hN (by nlinarith)
  have hdy : 0 < N * (gs + y * hs) := mul_pos hN (by nlinarith)
  unfold kappaOf
  rw [div_lt_div_iff₀ hdx hdy]
  nlinarith [mul_pos (mul_pos (mul_pos (sub_pos.mpr hxy) hT) hN) hgs]

/-- Prop 8(i): the supremum is the physical land ratio. -/
theorem prop8_i_tendsto (T N gs hs : ℝ) (hT : 0 < T) (hN : 0 < N)
    (hgs : 0 < gs) (hhs : 0 < hs) :
    Tendsto (kappaOf T N gs hs) atTop (𝓝 (T / (N * hs))) := by
  have h1 : Tendsto (fun q : ℝ => gs * q⁻¹) atTop (𝓝 0) := by
    simpa using tendsto_inv_atTop_zero.const_mul gs
  have h2 : Tendsto (fun q : ℝ => N * (gs * q⁻¹ + hs)) atTop (𝓝 (N * hs)) := by
    simpa using (h1.add tendsto_const_nhds).const_mul N
  have hne : N * hs ≠ 0 := (mul_pos hN hhs).ne'
  have h3 : Tendsto (fun q : ℝ => T / (N * (gs * q⁻¹ + hs))) atTop (𝓝 (T / (N * hs))) :=
    tendsto_const_nhds.div h2 hne
  apply h3.congr'
  filter_upwards [eventually_gt_atTop 0] with q hq
  have hq' : q ≠ 0 := hq.ne'
  have hden : gs + q * hs ≠ 0 := by nlinarith
  unfold kappaOf
  field_simp

/-- Prop 8(i): and it is never attained at finite `q`. -/
theorem prop8_i_sup_unattained (T N gs hs q : ℝ) (hT : 0 < T) (hN : 0 < N)
    (hgs : 0 < gs) (hhs : 0 < hs) (hq : 0 < q) :
    kappaOf T N gs hs q < T / (N * hs) := by
  have hd : 0 < N * (gs + q * hs) := mul_pos hN (by nlinarith)
  have hd2 : 0 < N * hs := mul_pos hN hhs
  unfold kappaOf
  rw [div_lt_div_iff₀ hd hd2]
  nlinarith [mul_pos (mul_pos hT hN) hgs]

/-- Prop 8(ii): the threshold `q*` exists iff land per head exceeds the bundle's
direct land content.

MANIFEST: `_hT : 0 < T` is redundant throughout this group — it follows from
`hfund : N·hs < T` with `N, hs > 0`. -/
theorem prop8_ii_threshold (T N gs hs : ℝ) (_hT : 0 < T) (hN : 0 < N)
    (hgs : 0 < gs) (hhs : 0 < hs) (hfund : N * hs < T) :
    kappaOf T N gs hs (N * gs / (T - N * hs)) = 1 := by
  have hD : 0 < T - N * hs := by linarith
  unfold kappaOf
  rw [div_eq_one_iff_eq]
  · field_simp; ring
  · have : 0 < gs + N * gs / (T - N * hs) * hs := by positivity
    exact (mul_pos hN this).ne'

/-- Prop 8(ii): fundability is exactly clearing `q*`. -/
theorem prop8_ii_iff (T N gs hs q : ℝ) (_hT : 0 < T) (hN : 0 < N)
    (hgs : 0 < gs) (hhs : 0 < hs) (hfund : N * hs < T) (hq : 0 < q) :
    1 ≤ kappaOf T N gs hs q ↔ N * gs / (T - N * hs) ≤ q := by
  have hD : 0 < T - N * hs := by linarith
  have hd : 0 < N * (gs + q * hs) := mul_pos hN (by nlinarith)
  unfold kappaOf
  rw [le_div_iff₀ hd, div_le_iff₀ hD]
  constructor <;> intro h <;> nlinarith

/-- Prop 8(ii): if land per head falls short of the bundle's land content, **no**
machine progress funds the floor. -/
theorem prop8_ii_never (T N gs hs q : ℝ) (_hT : 0 < T) (hN : 0 < N)
    (hgs : 0 < gs) (hhs : 0 < hs) (hcrowd : T ≤ N * hs) (hq : 0 < q) :
    kappaOf T N gs hs q < 1 := by
  have hd : 0 < N * (gs + q * hs) := mul_pos hN (by nlinarith)
  unfold kappaOf
  rw [div_lt_one hd]
  nlinarith

/-- Prop 8(iii): **the fiscal constraint is the land constraint in disguise.**

MANIFEST: note that this form contains no price at all — only `q` (pure
technology, see `Corner.q`), quantities, and `N`. That makes fundability
*invariant to the transfer's own effect on `r`*, which answers the appendix's
"the base feeds back — tendency, not theorem" worry for the fundability question
specifically. The paper states this identity but does not deploy it against the
feedback objection. It should. -/
theorem prop8_iii_land_constraint (T N gs hs q : ℝ) (_hT : 0 < T) (hN : 0 < N)
    (hgs : 0 < gs) (hhs : 0 < hs) (hq : 0 < q) :
    1 ≤ kappaOf T N gs hs q ↔ N * (gs / q + hs) ≤ T := by
  have hd : 0 < N * (gs + q * hs) := mul_pos hN (by nlinarith)
  have expand : N * (gs / q + hs) = (N * gs + N * q * hs) / q := by
    field_simp
  rw [expand, div_le_iff₀ hq]
  unfold kappaOf
  rw [le_div_iff₀ hd]
  constructor <;> intro h <;> nlinarith

/-! ## §7. Proposition 9 — the enclosure margin -/

/-- The exit value once the idle margin has closed: autarkic keep minus the exit
plot's rent, floored at dependency. -/
noncomputable def sExit (s₀ sd he q : ℝ) : ℝ := max (s₀ - q * he) sd

/-- Prop 9(ii): while the keep binds, the exit value falls one-for-one with
`q·he`. -/
theorem prop9_ii_slope (s₀ sd he q : ℝ) (hhe : 0 < he) (_hq : 0 < q)
    (h : q < (s₀ - sd) / he) : sExit s₀ sd he q = s₀ - q * he := by
  unfold sExit
  apply max_eq_left
  rw [lt_div_iff₀ hhe] at h
  linarith

/-- Prop 9(ii): **finite** machine progress completes the enclosure. -/
theorem prop9_ii_enclosure_completes (s₀ sd he q : ℝ) (hhe : 0 < he) (_hsd : sd < s₀)
    (h : (s₀ - sd) / he ≤ q) : sExit s₀ sd he q = sd := by
  unfold sExit
  apply max_eq_right
  rw [div_le_iff₀ hhe] at h
  linarith

/-- Prop 9(ii): the exit value is monotonically non-increasing in `q`. -/
theorem prop9_ii_antitone (s₀ sd he : ℝ) (hhe : 0 < he) :
    Antitone (sExit s₀ sd he) := by
  intro q₁ q₂ hq
  unfold sExit
  exact max_le_max (by nlinarith) (le_refl sd)

/-- Prop 9(iii), the race: the natural floor dies at `q_enc`, the fundable floor
arrives at `q*`, and which comes first is a crowding condition. -/
theorem prop9_iii_race (T N gs hs s₀ sd he : ℝ) (_hT : 0 < T) (_hN : 0 < N)
    (hgs : 0 < gs) (hhs : 0 < hs) (hhe : 0 < he) (hsd : sd < s₀)
    (hfund : N * hs < T) :
    N * gs / (T - N * hs) ≤ (s₀ - sd) / he ↔
      N ≤ ((s₀ - sd) / he) * T / (gs + ((s₀ - sd) / he) * hs) := by
  have hqe : 0 < (s₀ - sd) / he := div_pos (by linarith) hhe
  have hD : 0 < T - N * hs := by linarith
  have hden : 0 < gs + ((s₀ - sd) / he) * hs := by positivity
  rw [div_le_iff₀ hD, le_div_iff₀ hden]
  constructor <;> intro h <;> nlinarith

/-- Prop 9, remark (b): the cancellation of 6(i) survives an endogenous `s(q)` —
the difference `(w + u) - (s(q) + u)` is independent of `u`. -/
theorem prop9_cancel_survives (s₀ sd he q w u : ℝ) :
    (w + u) - (sExit s₀ sd he q + u) = w - sExit s₀ sd he q := by ring

/-- Prop 9, remark (b): past enclosure the take is **capped** at `s₀ - sd`, not
at the still-rising plot rent. -/
theorem prop9_take_capped (s₀ sd he q : ℝ) (hhe : 0 < he) (hsd : sd < s₀)
    (h : (s₀ - sd) / he ≤ q) : s₀ - sExit s₀ sd he q = s₀ - sd := by
  rw [prop9_ii_enclosure_completes s₀ sd he q hhe hsd h]

/-! ## §8. Proposition 10 — the mix frontier -/

/-- VAT deadweight: the standard half-square on the wage-financed slice.

MANIFEST: `λC · E · tV²` treats the wage-financed *share* as invariant to the
VAT rate. If the VAT itself shifts the financing mix, `λC` is endogenous and
this is a first-order approximation, not a functional form. The paper introduces
it as a hypothesis ("Assume the VAT's deadweight is the standard half-square"),
which is the right move; recording it here so the assumption travels with the
theorem. -/
noncomputable def DWL (ψ lamC E tV : ℝ) : ℝ := (ψ / 2) * lamC * E * tV ^ 2

/-- A feasible instrument pair: rates in range, budget met.

MANIFEST: `htV₁ : tV ≤ 1` is **not in the paper**. Prop 10(ii) gives
`tV = N·Ps·(1−κ)/E` with no constraint, but that expression exceeds 1 whenever
`N·Ps·(1−κ) > E` — a VAT rate above 100%, i.e. an infeasible instrument. See
`mix_infeasible_when_floor_exceeds_bases`. -/
structure MixFeasible (rT E floor : ℝ) where
  tL : ℝ
  tV : ℝ
  htL₀ : 0 ≤ tL
  htL₁ : tL ≤ 1
  htV₀ : 0 ≤ tV
  htV₁ : tV ≤ 1
  hbudget : tL * rT + tV * E = floor

/-- Prop 10(i): when coverage suffices, the optimum is the land tax alone, at
zero deadweight. -/
theorem prop10_i_land_alone (ψ lamC rT E floor : ℝ) (hψ : 0 < ψ) (hlam : 0 ≤ lamC)
    (hE : 0 < E) (hrT : 0 < rT) (hfloor : 0 < floor) (hκ : floor ≤ rT) :
    IsLeast {d | ∃ p : MixFeasible rT E floor, d = DWL ψ lamC E p.tV} 0 := by
  constructor
  · refine ⟨⟨floor / rT, 0, div_nonneg hfloor.le hrT.le, (div_le_one hrT).mpr hκ,
      le_refl 0, zero_le_one, by field_simp; ring⟩, ?_⟩
    unfold DWL; ring
  · rintro d ⟨p, rfl⟩
    unfold DWL
    have h1 : 0 ≤ ψ / 2 * lamC * E :=
      mul_nonneg (mul_nonneg (by linarith) hlam) hE.le
    exact mul_nonneg h1 (sq_nonneg p.tV)

/-- Prop 10(ii): when coverage falls short, fill the rent base first — `tL = 1`
and the VAT covers exactly the shortfall.

This is the one proposition in the spine where I'd genuinely expect Lean to earn
its keep: it is a corner solution, and verbal optimisation arguments ("cheap
revenue precedes costly revenue") are where sloppiness hides. -/
theorem prop10_ii_optimum (ψ lamC rT E floor : ℝ) (hψ : 0 < ψ) (hlam : 0 < lamC)
    (hE : 0 < E) (hrT : 0 < rT) (hshort : rT < floor)
    (hfeas : floor - rT ≤ E) :
    IsLeast {d | ∃ p : MixFeasible rT E floor, d = DWL ψ lamC E p.tV}
      (DWL ψ lamC E ((floor - rT) / E)) := by
  have hpos : 0 ≤ (floor - rT) / E := div_nonneg (by linarith) hE.le
  constructor
  · -- `htV₁` is where `hfeas` is consumed: without it the optimum is infeasible.
    exact ⟨⟨1, (floor - rT) / E, zero_le_one, le_refl 1, hpos,
      (div_le_one hE).mpr hfeas, by field_simp; ring⟩, rfl⟩
  · rintro d ⟨p, rfl⟩
    have hle : (floor - rT) / E ≤ p.tV := by
      rw [div_le_iff₀ hE]
      have hb := p.hbudget
      nlinarith [p.htL₁, hrT]
    have hsq : ((floor - rT) / E) ^ 2 ≤ p.tV ^ 2 := by nlinarith
    have hcoef : 0 ≤ ψ / 2 * lamC * E := by positivity
    unfold DWL
    exact mul_le_mul_of_nonneg_left hsq hcoef

/-- **The feasibility bound is not decorative.**

If the floor exceeds what a full land tax and a 100% VAT can jointly raise, the
feasible set is *empty* — so Prop 10(ii)'s prescribed rate is not merely large,
it optimises over nothing. Together with `prop10_ii_optimum`'s `hfeas`, this
pins the condition exactly: a feasible pair exists iff `floor ≤ rT + E`, which
is precisely `hfeas`. The paper's `tV = N·Ps·(1−κ)/E` carries no such side
condition. -/
theorem mix_infeasible_when_floor_exceeds_bases (rT E floor : ℝ)
    (hrT : 0 ≤ rT) (hE : 0 ≤ E) (hgap : rT + E < floor) :
    IsEmpty (MixFeasible rT E floor) := by
  constructor
  rintro p
  have h1 : p.tL * rT ≤ rT := by nlinarith [p.htL₁, p.htL₀]
  have h2 : p.tV * E ≤ E := by nlinarith [p.htV₁, p.htV₀]
  have hb := p.hbudget
  linarith

/-- The same, instantiated at the paper's own measured coverage ratio. Take
`rT = 1`, `floor = 3` (so `κ = rT/floor = 1/3`, the 2025 measurement) and
aggregate consumption `E = 1`: the prescribed rate is `(3-1)/1 = 2`, a 200% VAT,
and no feasible pair exists. The empirical margin is comfortable — US `N·Ps/E`
looks like ~0.25 against a bound of ~1.5 at κ = 0.33 — but the *theorem* needs
the hypothesis. -/
example : IsEmpty (MixFeasible (1 : ℝ) 1 3) :=
  mix_infeasible_when_floor_exceeds_bases 1 1 3 zero_le_one zero_le_one (by norm_num)

/-- Prop 10(ii): the minimised deadweight is proportional to `λC·(1−κ)²` at a
given floor-to-consumption ratio — the crossing's price index. -/
theorem prop10_ii_cost_index (ψ lamC E floor kap : ℝ) (hE : 0 < E) :
    DWL ψ lamC E (floor * (1 - kap) / E)
      = (ψ / 2) * (lamC * (1 - kap) ^ 2) * (floor ^ 2 / E) := by
  unfold DWL
  field_simp

/-- Prop 10(ii): the index falls in κ and rises in λC — both measured series
moving the right way. -/
theorem prop10_ii_monotone_in_kappa (lamC : ℝ) (hlam : 0 < lamC) :
    StrictAntiOn (fun kap => lamC * (1 - kap) ^ 2) (Set.Iio 1) := by
  intro x hx y hy hxy
  simp only [Set.mem_Iio] at hx hy
  have h1 : 0 < 1 - y := by linarith
  have h2 : (1 - y) ^ 2 < (1 - x) ^ 2 := by nlinarith
  exact mul_lt_mul_of_pos_left h2 hlam

/-- Prop 10(iii): at the corner the bases merge — all consumption spending is
rent income, so a uniform VAT and a full land tax draw on one base.

MANIFEST: this is `prop5_ii_conservation` restated. The mix question retires at
the corner because the two instruments become the same instrument, which is a
consequence of the conservation identity and nothing further. -/
theorem prop10_iii_bases_merge : M.pg * M.Y + M.r * M.TH = M.r * M.T :=
  M.prop5_ii_conservation

/-! ## §9. Proposition 13(ii) — implementation

The payoff: the George pair spans the whole family of divisions of the rent, at
zero deadweight, without ever moving a margin. -/

/-- Prop 13(ii): for every rate, the post-transfer incomes sum to total rent —
the family is feasible throughout. -/
theorem prop13_ii_feasible {ι : Type*} [Fintype ι] (hne : 0 < Fintype.card ι)
    (ω : ι → ℝ) (hω : ∑ i, ω i = 1) (rT tL : ℝ) :
    ∑ i, ((1 - tL) * ω i * rT + tL * rT / (Fintype.card ι : ℝ)) = rT := by
  have hcard : (Fintype.card ι : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr hne.ne'
  rw [Finset.sum_add_distrib, Finset.sum_const, Finset.card_univ, nsmul_eq_mul]
  have h1 : ∑ i, (1 - tL) * ω i * rT = (1 - tL) * rT := by
    have hre : ∀ i, (1 - tL) * ω i * rT = ((1 - tL) * rT) * ω i := by intro i; ring
    simp_rw [hre, ← Finset.mul_sum, hω, mul_one]
  rw [h1]
  field_simp
  ring

/-- Prop 13(ii): at `tL = 0` the division is the inherited one. -/
theorem prop13_ii_inherited {ι : Type*} [Fintype ι] (ω : ι → ℝ) (rT : ℝ) (i : ι) :
    (1 - (0:ℝ)) * ω i * rT + 0 * rT / (Fintype.card ι : ℝ) = ω i * rT := by ring

/-- Prop 13(ii): at `tL = 1` it is the equal one, whatever the inherited shares. -/
theorem prop13_ii_equal {ι : Type*} [Fintype ι] (ω : ι → ℝ) (rT : ℝ) (i j : ι) :
    (1 - (1:ℝ)) * ω i * rT + 1 * rT / (Fintype.card ι : ℝ)
      = (1 - (1:ℝ)) * ω j * rT + 1 * rT / (Fintype.card ι : ℝ) := by ring

/-- Prop 13(ii): and no term in the family moves any margin — the transfer is
uniform, so 6(i)'s cancellation applies at every rate. -/
theorem prop13_ii_no_margin_moved {ι : Type*} [Fintype ι] (rT tL w s : ℝ) :
    s + tL * rT / (Fintype.card ι : ℝ) ≤ w + tL * rT / (Fintype.card ι : ℝ) ↔ s ≤ w :=
  add_le_add_iff_right _

end Corner

end Link

/-
## The manifest

What writing the statements down surfaced. Ordered by how much I think each one
matters, not by proposition number. None of these is an algebra error — the
sympy checks in `checks/` cover that ground and cover it well. They are places
where the *hypothesis set* is larger, or differently shaped, than the prose
suggests.

1. **Props 4 and 5 live in different sub-regimes and cannot share a structure.**
   4(i) needs labour employed at parity for a wage to exist (corner-above);
   5 sets labour to zero measure (corner-below). The paper carries the
   distinction in an appendix remark; here it is forced, because `w` has nowhere
   to live in the corner-below structure. Cheapest fix in the paper: one clause
   in Prop 4's preamble naming the sub-regime, rather than leaving it to the
   appendix.

2. **Prop 10's VAT rate has no feasibility bound.** *(Machine-checked — this is
   the one finding here that is proved rather than observed.)*
   `tV = N·Ps·(1−κ)/E` exceeds 1 whenever `N·Ps·(1−κ) > E`.
   `mix_infeasible_when_floor_exceeds_bases` proves the feasible set is *empty*
   once `floor > rT + E`, so together with `prop10_ii_optimum`'s `hfeas` the
   condition is pinned exactly: a feasible pair exists **iff** `floor ≤ rT + E`.
   Below that line Prop 10(ii) optimises over the empty set. At the measured
   pair (λC = 0.72, κ = 0.33) the requirement is that the floor run under
   roughly 1.5× aggregate consumption, and US `N·Ps/E` looks like ~0.25 — so
   this is a missing hypothesis, not a wrong result. But the theorem should
   carry it, because the interesting regime for the mix frontier is precisely
   low κ, where the bound tightens.

3. **Prop 7(ii) is an assumption, not a theorem, *in this model*.** The
   capitalisation result is standard, but the corner model has no asset-pricing
   equation and no land-use margin to derive it from — `TP`/`TH` are pinned by
   Cobb-Douglas shares and no land price appears. Encoded here as
   `LandTaxInvariance`. Deriving it means adding a model, not proving something
   about the existing one. Second-order but real: `flow_invariant` also silently
   requires site value separable from improvement value, which the paper flags
   as a *practical* assessment caveat while it is doing *theoretical* work.

4. **`σ` carries two jobs, and the subsistence bundle is a third kind of
   object.** In 4(iii) it is the land share of a price index; in 5 it is the
   representative household's Cobb-Douglas share. The subsistence bundle of
   Prop 8 is fixed *quantities*, so its implied land share `q·hs/(gs + q·hs)`
   moves with `q` and equals no constant. All three are defensible; the notation
   makes them look like one. Kept as separate arguments above.

5. **Prop 4(iii)'s price index is asserted, and drops a constant.** `P =
   pg^(1−σ)·r^σ` is derivable from Cobb-Douglas only up to
   `σ^(−σ)(1−σ)^(σ−1)`. Harmless for a limit claim; worth a footnote.

6. **`0 < a` is used but never stated**, and the durable reading needs
   `a·(δ+d) < 1`, strictly stronger than `a < 1`. The paper states the analogous
   condition for the δ-only case and then generalises without restating it.

7. **Stated-but-unused hypotheses**, flagged by Lean's linter and marked with a
   leading underscore above. Two kinds, and they should not be conflated.

   *Genuine* — the result really is stronger than the paper's conditions
   suggest: `prop3_user_cost` needs neither `0 ≤ δ` nor `0 < d`, only the
   convergence condition `a(δ+d) < 1`; `prop4_iii_decomp` holds for every `s`,
   not just `s ∈ (0,1)`; `_hT : 0 < T` is redundant across the Prop 8 group
   (it follows from `N·hs < T`); `prop9_ii_slope` does not need `0 < q`;
   `prop9_iii_race` needs neither `0 < T` nor `0 < N`; `_hn₀ : 0 < n` is not
   needed for Prop 7(i)-partial; `_ha₁ : a < 1` is not needed for the a-margin
   bound.

   *Artefact of Lean's convention* — `x / 0 = 0` in mathlib, so some positivity
   hypotheses go unused because the degenerate case happens to satisfy the
   equation rather than because the economics is more general. That covers
   `q_bounded_under_substitution`'s `_hℓ/_hρ/_hL` and
   `prop4_iii_bounded_at_zero`'s `_hL`. These carry no mathematical content and
   should not be read as findings. Same for `q_tendsto_zero_along_a`, where the
   degenerate denominator makes the function identically zero.

Two findings run the *other* way — the formalisation strengthens the paper:

8. **`q` is a pure technology ratio: no price appears in it.** Consequently
   `κ` (via `prop8_iii_land_constraint`) is invariant to any fiscal action's
   effect on `r`. That is a direct answer to the appendix's own "the base feeds
   back — tendency, not theorem" hedge, at least for the fundability question,
   and the paper does not currently deploy it.

9. **Prop 5(iii) is definitional, and the paper is right to hedge it.** The
   demand-side and cost-side prices agree by unfolding, not by coincidence — the
   Lean proof of `prop5_iii` is literally `prop4_ii`. The text already says the
   derivation "is not a test the model could have failed"; the formalisation
   confirms the hedge rather than the headline.
-/
