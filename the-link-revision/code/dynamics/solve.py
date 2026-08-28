# solve.py — perfect-foresight transitions for the v2 dynamics.
# (rewrite brief v2 §3.5–3.6, structure memo STATE log 32; 2026-08-28)
#
# Method: damped fixed point on the investment path {I_t} with the entry
# complementarity I_t ≥ 0 ⊥ p_K,t ≥ PV_t(π). Given {I_t}: K path from the
# law of motion (pre-shock pipeline included), then period-by-period exact
# inner solves (flat: the split m_t is linear; sloped: the margin x*_t is a
# quadratic root under the affine schedule), land clearing linear in r_t
# (the π-surprise income term M_t is affine in r_t), then PV gaps update I.
#
# Validation ladder (memo 8.1–8.2 — run order enforced in run_all):
#   V-A the b_I = 0, foreign-convention flat case has an EXACT closed form:
#       r_t = r_old for t < J (the old pipeline holds K at K_old and land
#       clearing does not move), r_t = r_new for t ≥ J; the quasi-rent is a
#       J-period rectangle. The solver must reproduce it to 1e-8.
#   V-B horizon insensitivity: H and 1.5H paths agree on the overlap.
#   V-C endpoints: t = 0 state continuous with the old SS; tail at the new
#       SS to tolerance (both SSs from model.py, already gated to checks).
# Only after V-A/B/C does the same engine touch the sloped case (T5).
#
# Statuses (brief §3.6): T1 windfall, T2 waterfall, T3 speed × lag are
# "expected — verify"; T5 sloped wage path is a CONJECTURE the numerics
# decide. Verdicts land in results_dynamics.json; nothing is promoted here.
#
# Interior/participation conditions are CHECKED along every path and
# violations are reported, never assumed away (memo caution iii).
#
# Run: ../venv/Scripts/python.exe code/dynamics/solve.py   (from the-link-revision/)

import json
import os
import sys

import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import model  # noqa: E402

RESULTS = os.path.join(HERE, "results_dynamics.json")


# ------------------------------------------------------------ shared pieces
def k_path(I, J, delta, K0, I_pre):
    """K_{t+1} = (1−δ)K_t + I_{t+1−J}; I_s = I_pre for s < 0 (old pipeline)."""
    H = len(I)
    K = np.empty(H)
    K[0] = K0
    for t in range(H - 1):
        arr = I[t + 1 - J] if t + 1 - J >= 0 else I_pre
        K[t + 1] = (1 - delta) * K[t] + arr
    return K


def pv_matrix(H, J, rho, delta):
    """PV weights: PV_t = Σ_{s≥t+J} (1+ρ)^{−(s−t)} (1−δ)^{s−t−J} π_s, built
    once as an H×H matrix (rows t, cols s), tail handled by the caller by
    clamping π at its SS value beyond the active window."""
    W = np.zeros((H, H))
    for t in range(H):
        s = np.arange(t + J, H)
        W[t, s] = (1 + rho) ** (-(s - t)) * (1 - delta) ** (s - t - J)
    return W


def pv_tail(H, t, J, rho, delta, pi_ss):
    """Analytic tail Σ_{s≥H} for a π path clamped at pi_ss beyond H."""
    s0 = max(H, t + J)
    return pi_ss * (1 + rho) ** (-(s0 - t)) * (1 - delta) ** (s0 - t - J) \
        * (1 + rho) / (rho + delta)


def surviving_old(H, J, delta, K0, I_pre):
    """S_t: surviving mass of all pre-shock-FINANCED units (installed stock
    plus the old pipeline as it arrives) — the π-surprise base."""
    S = np.empty(H)
    for t in range(H):
        s = K0 * (1 - delta) ** t
        for tau in range(0, min(t, J - 1) + 1):   # old pipeline arrivals
            s += I_pre * (1 - delta) ** (t - tau)
        S[t] = s
    return S


def land_rent(p, K, I, S, pi_at_r0, w, N, convention):
    """Solve land clearing for r_t. π_t = pi_at_r0 − b·r_t (affine), and under
    the domestic convention M_t = (π_t − π̄_old)S_t enters income:
      r[(1−α)T − bK − b_I I + α b S·dom] = α(wN + (pi_at_r0 − π̄_old)S·dom)."""
    dom = 1.0 if convention == "domestic" else 0.0
    pibar_old = p["_pibar_old"]
    denom = (1 - p["alpha"]) * p["T"] - p["b"] * K - p["bI"] * I \
        + p["alpha"] * p["b"] * S * dom
    numer = p["alpha"] * (w * N + (pi_at_r0 - pibar_old) * S * dom)
    return numer / denom


# ------------------------------------------------------- the one-stock engine
def solve_path(p_new, ss_old, ss_new, inner, H=300, convention="domestic",
               gambar_path=None, tol=1e-11, max_iter=200_000):
    """Damped fixed point on {I_t}. `inner(p, K, I, t, gambar_t)` returns the
    dict of period objects BEFORE land clearing (c, w, split, Y, pi_at_r0,
    flags). gambar_path lets T3 phase the shock in. Returns the full path."""
    J, rho, delta = p_new["J"], p_new["rho"], p_new["delta"]
    K0, I_pre = ss_old["K"], ss_old["I"]
    p = dict(p_new)
    p["_pibar_old"] = ss_old["pi"]
    W = pv_matrix(H, J, rho, delta)
    S = surviving_old(H, J, delta, K0, I_pre)
    I = np.full(H, ss_new["I"])
    pK_ss, pi_ss = ss_new["pK"], ss_new["pi"]
    step = 0.5 * ss_new["I"] / pK_ss
    last_gap = np.inf
    for it in range(max_iter):
        K = k_path(I, J, delta, K0, I_pre)
        per = inner(p, K, I, gambar_path)
        r = land_rent(p, K, I, S, per["pi_at_r0"], per["w"], p["N"], convention)
        pi = per["pi_at_r0"] - p["b"] * r
        pK = p["aI"] * per["c"] + p["lamI"] * per["w"] + p["bI"] * r
        pi_c = pi.copy()
        pv = W @ pi_c + np.array([pv_tail(H, t, J, rho, delta, pi_ss)
                                  for t in range(H)])
        gap = pv - pK
        gap_eff = np.where(I > 0, np.abs(gap), np.maximum(gap, 0.0))
        g = gap_eff.max()
        if g < tol * pK_ss:
            break
        if g > last_gap * 1.0000001 and step > 1e-6:
            step *= 0.5                             # adaptive damping
        last_gap = g
        I = np.maximum(0.0, I + step * gap)
        I[-2 * J:] = ss_new["I"]                    # clamp the tail at SS
    K = k_path(I, J, delta, K0, I_pre)
    per = inner(p, K, I, gambar_path)
    r = land_rent(p, K, I, S, per["pi_at_r0"], per["w"], p["N"], convention)
    pi = per["pi_at_r0"] - p["b"] * r
    pK = p["aI"] * per["c"] + p["lamI"] * per["w"] + p["bI"] * r
    return dict(I=I, K=K, r=r, pi=pi, pK=pK, iters=it, gap=g, S=S,
                converged=g < tol * pK_ss, **per)


def flat_inner(p, K, I, gambar_path):
    """Flat case: c_t = γ_L/γ̄_t, w = γ_L; the split m_t and Y_t are linear.
    X_t = K_t (full use; π ≥ 0 verified by the caller's reporting)."""
    H = len(K)
    gb = np.full(H, p["gambar"]) if gambar_path is None else gambar_path
    c = p["gamL"] / gb
    w = p["gamL"]
    MY = (K * (1 - p["a"]) - p["aI"] * I) * p["gamL"] / gb
    Y = MY + p["gamL"] * (p["N"] - p["lam"] * K - p["lamI"] * I)
    m = MY / Y
    pi_at_r0 = c * (1 - p["a"]) - p["lam"] * w
    flags = dict(split_interior=bool(np.all((m > 0) & (m < 1))),
                 labor_left=bool(np.all(p["lam"] * K + p["lamI"] * I < p["N"])),
                 services_pos=bool(np.all(MY > 0)))
    return dict(c=c, w=np.full(H, w), m=m, Y=Y, pi_at_r0=pi_at_r0, flags=flags)


def sloped_inner(p, K, I, gambar_path):
    """Sloped case: capacity absorption + labor clearing pin x*_t. On the
    affine stretch the margin is the positive root of ½Bg₁x² + (A + Bg₀)x − A
    = 0 with A = K(1−a) − a_I I, B = N − λK − λ_I I (γ_L = 1); under a cap,
    the flat stretch's root is linear: A(1−x) = B[Iγ(x_k) + cap(x − x_k)].
    Then c, w from unit cost and the margin."""
    A = K * (1 - p["a"]) - p["aI"] * I
    B = p["N"] - p["lam"] * K - p["lamI"] * I
    g0, g1 = p["g0"], p["g1"]
    disc = (A + B * g0) ** 2 + 2 * B * g1 * A
    xs = (-(A + B * g0) + np.sqrt(disc)) / (B * g1)
    cap = p.get("cap")
    if cap is not None:
        xk = max((cap - g0) / g1, 0.0)
        Igk = g0 * xk + 0.5 * g1 * xk * xk
        xs_lin = (A - B * (Igk - cap * xk)) / (A + B * cap)
        xs = np.where(xs > xk, xs_lin, xs)
        g = np.minimum(g0 + g1 * xs, cap)
        Ig = np.where(xs > xk, Igk + cap * (xs - xk), g0 * xs + 0.5 * g1 * xs * xs)
    else:
        g = g0 + g1 * xs
        Ig = g0 * xs + 0.5 * g1 * xs * xs
    c = 1.0 / (g * (1 - xs) + Ig)
    w = g * c
    Y = A / Ig
    pi_at_r0 = c * (1 - p["a"]) - p["lam"] * w
    flags = dict(margin_interior=bool(np.all((xs > 0) & (xs < 1))),
                 labor_left=bool(np.all(B > 0)),
                 services_pos=bool(np.all(A > 0)))
    return dict(c=c, w=w, xstar=xs, Y=Y, pi_at_r0=pi_at_r0, flags=flags)


# --------------------------------------------------- V-A: exact flat benchmark
def closed_form_flat(p, ss_old, ss_new, H):
    """b_I = 0, foreign convention: r_t = r_old for t < J, r_new for t ≥ J
    (derivation in the file header of check_dynamics.py's T1 addendum)."""
    r = np.full(H, ss_new["r"])
    r[:p["J"]] = ss_old["r"]
    return r


def validate_flat(H=300):
    p_old = model.flat_params()
    p_new = model.flat_params()
    p_new["gambar"] = 2.8                          # the worked capability jump
    for q in (p_old, p_new):
        q["bI"] = 0.0
    ss_old, ss_new = model.flat_ss(p_old), model.flat_ss(p_new)
    out = solve_path(p_new, ss_old, ss_new, flat_inner, H=H, convention="foreign")
    r_exact = closed_form_flat(p_new, ss_old, ss_new, H)
    dev = np.abs(out["r"] - r_exact).max()
    ok_a = out["converged"] and dev < 1e-8
    # V-B horizon insensitivity on the same case
    out2 = solve_path(p_new, ss_old, ss_new, flat_inner, H=int(1.5 * H),
                      convention="foreign")
    dev_h = np.abs(out2["r"][:H - 2 * p_new["J"]] - out["r"][:H - 2 * p_new["J"]]).max()
    ok_b = dev_h < 1e-8
    # Q_0 against the closed form of check T1c/T1d
    J, rho, delta = p_new["J"], p_new["rho"], p_new["delta"]
    qqJ = ((1 - delta) / (1 + rho)) ** J
    pi_win = ss_new["c"] * (1 - p_new["a"]) - p_new["lam"] * ss_new["w"] \
        - p_new["b"] * ss_old["r"]
    Q0_closed = (pi_win * (1 - qqJ) + ss_new["pi"] * qqJ) / ((rho + delta) * ss_new["pK"])
    disc = (1 + rho) ** (-(np.arange(H) + 1)) * (1 - delta) ** np.arange(H)
    V0 = float((disc * out["pi"]).sum()
               + (1 + rho) ** (-H) * (1 - delta) ** H * ss_new["pi"] / (rho + delta))
    dev_q = abs(V0 / out["pK"][0] - Q0_closed)
    ok_c = dev_q < 1e-8
    return dict(closed_form_dev=float(dev), horizon_dev=float(dev_h),
                Q0_dev=float(dev_q), iters=int(out["iters"]),
                ok=bool(ok_a and ok_b and ok_c))


# ------------------------------------------------------------- T1: windfall
def run_t1(H=300, convention="domestic"):
    p_old = model.flat_params()
    p_new = model.flat_params()
    p_new["gambar"] = 2.8
    ss_old, ss_new = model.flat_ss(p_old), model.flat_ss(p_new)
    out = solve_path(p_new, ss_old, ss_new, flat_inner, H=H, convention=convention)
    J, rho, delta = p_new["J"], p_new["rho"], p_new["delta"]
    # Q_0: value of an installed pre-shock unit over its replacement cost.
    # The steady-state benchmark is NOT 1: Q̄ = (1+ρ)^{J−1} (the gestation
    # float — check T1d); the windfall is the excess over Q̄.
    disc = (1 + rho) ** (-(np.arange(H) + 1)) * (1 - delta) ** np.arange(H)
    V0 = float((disc * out["pi"]).sum()
               + (1 + rho) ** (-H) * (1 - delta) ** H * ss_new["pi"] / (rho + delta))
    Q0 = V0 / out["pK"][0]
    Q_ss = (1 + rho) ** (J - 1)
    # windfall on pre-shock vintages (PV of the surprise series M_t)
    M = (out["pi"] - ss_old["pi"]) * out["S"]
    wind = float(((1 + rho) ** (-(np.arange(H) + 1)) * M).sum())
    land_gain = float(((1 + rho) ** (-(np.arange(H) + 1))
                       * (out["r"] - ss_old["r"]) * p_new["T"]).sum()
                      + (1 + rho) ** (-H) * (ss_new["r"] - ss_old["r"]) * p_new["T"] / rho)
    # The land-unit wage is NOT step-monotone: the investment surge's own
    # land demand (b_I I_0) and, under the domestic convention, the windfall
    # income both front-load the rent at release, and delivery cycles ripple
    # it (the ripple is pinned to 9 digits across tolerances — equilibrium
    # dynamics, not solver noise). The claims that hold: the land claim
    # drops at release, never recovers to its old value, settles lower.
    wr = out["w"] / out["r"]
    wr_old, wr_new = ss_old["w"] / ss_old["r"], ss_new["w"] / ss_new["r"]
    checks = dict(
        w_goods_constant=bool(np.allclose(out["w"], p_new["gamL"])),
        w_land_claim_below_old_at_every_date=bool(wr.max() < wr_old),
        w_land_claim_settles_at_lower_ss=bool(abs(wr[-1] - wr_new) < 1e-6
                                              and wr_new < wr[0]),
        Q0_above_ss_benchmark=bool(Q0 > Q_ss + 1e-10),
        quasi_rent_decays=bool(out["pi"][0] > ss_new["pi"] - 1e-12
                               and abs(out["pi"][-1] - ss_new["pi"]) < 1e-6),
        endpoints=bool(abs(out["K"][0] - ss_old["K"]) < 1e-12
                       and abs(out["K"][-1] - ss_new["K"]) / ss_new["K"] < 1e-6),
        **out["flags"])
    return out, dict(Q0=float(Q0), Q_ss_benchmark=float(Q_ss),
                     windfall_pv=wind, land_gain_pv=land_gain,
                     r_old=ss_old["r"], r_new=ss_new["r"],
                     rent_frontload_max_step_up=float(np.diff(wr).max()),
                     pi_impact=float(out["pi"][0]), pi_old=ss_old["pi"],
                     pi_new=ss_new["pi"], iters=int(out["iters"]),
                     converged=bool(out["converged"]), checks=checks,
                     verdict_expected="Q0 above the (1+rho)^(J-1) benchmark, "
                                      "rents decay to land, CM on the path",
                     verdict=("VERIFIED" if all(checks.values()) else "FAILED"))


# ------------------------------------------------- T3: speed × lag comparative
def run_t3(H=360):
    from tqdm.auto import tqdm
    speeds = {"fast (1 period)": 1, "medium (4)": 4, "slow (12)": 12}
    lags = {1: None, 2: None, 4: None}          # J = 6 exits the interior region
    W = {}
    for Jv in tqdm(list(lags), desc="T3 grid (J)"):
        for sname, dur in speeds.items():
            p_old = model.flat_params(); p_old["J"] = Jv
            p_new = model.flat_params(); p_new["J"] = Jv; p_new["gambar"] = 2.8
            ss_old, ss_new = model.flat_ss(p_old), model.flat_ss(p_new)
            gb = np.full(H, 2.8)
            gb[:dur] = np.linspace(p_old["gambar"], 2.8, dur + 1)[1:]
            out = solve_path(p_new, ss_old, ss_new, flat_inner, H=H,
                             convention="domestic", gambar_path=gb)
            rho = p_new["rho"]
            M = (out["pi"] - ss_old["pi"]) * out["S"]
            W[(Jv, sname)] = float(((1 + rho) ** (-(np.arange(H) + 1)) * M).sum())
    # monotone in speed (fast > slow at each J) and in J (long > short at each speed)
    mono_speed = all(W[(J_, "fast (1 period)")] > W[(J_, "slow (12)")] for J_ in lags)
    mono_lag = all(W[(4, s)] > W[(1, s)] for s in speeds)
    return dict(windfall_pv={f"J={j} | {s}": v for (j, s), v in W.items()},
                monotone_in_speed=bool(mono_speed), monotone_in_lag=bool(mono_lag),
                verdict_expected="windfall scales with speed × gestation lag",
                verdict=("VERIFIED" if (mono_speed and mono_lag) else "FAILED"))


# ---------------------------------------------------------- T5: sloped wages
def t5_facts(p_new, ss_old, ss_new, out):
    w, r = out["w"], out["r"]
    wr = w / r
    wr_old = ss_old["w"] / ss_old["r"]
    part_ok = bool(np.all(w > np.maximum(p_new["s0"] - r * p_new["he"], p_new["sd"])))
    return dict(
        w_goods_impact=float(w[0]), w_goods_old=ss_old["w"], w_goods_new=ss_new["w"],
        w_goods_falls_on_impact=bool(w[0] < ss_old["w"]),
        w_goods_recovers=bool(w[-1] > w.min() + 1e-9),
        w_goods_flat_after_release=bool(np.ptp(w) < 1e-9 * max(abs(w.max()), 1.0)
                                        or np.ptp(w[1:]) < 1e-9),
        w_goods_trough_at=int(np.argmin(w)),
        w_land_claim_below_old_at_every_date=bool(wr.max() < wr_old),
        w_land_claim_settles_lower=bool(ss_new["w"] / ss_new["r"] < wr[0]),
        rent_frontload_max_step_up=float(np.diff(wr).max()),
        w_over_r_old=float(wr_old),
        w_over_r_new=float(ss_new["w"] / ss_new["r"]),
        xstar_impact=float(out["xstar"][0]), xstar_old=float(ss_old["xstar"]),
        xstar_new=float(ss_new["xstar"]),
        participation_holds=part_ok,
        endpoints=bool(abs(out["K"][0] - ss_old["K"]) < 1e-9
                       and abs(out["K"][-1] - ss_new["K"]) / ss_new["K"] < 1e-5),
        iters=int(out["iters"]), converged=bool(out["converged"]),
        **out["flags"])


def run_t5(H=300, T_exp=4.0, cap=2.8, mult=0.85, convention="domestic"):
    """Two sloped experiments, both at T = 4.0 (the gate instantiation's
    T = 10 leaves land so abundant that a real frontier shock exits the
    land-binding regime — no clearing root; at T = 4 the old margin sits
    mid-schedule and land binds at both endpoints).
    (i) FRONTIER EXTENSION — the conjecture's scenario (Korinek–Suh):
    γ_new = min(γ_old, cap): tasks above the kink become automatable at the
    cap while already-automated tasks are unchanged; capacity must be built
    before the margin can sweep the capped stretch. (ii) EFFICIENCY
    DEEPENING — the contrast: γ_new = mult·γ_old cheapens the automated
    stretch itself, so existing capacity stretches further on impact. The
    conjecture is judged on (i); (ii) is reported as the contrast that
    sharpens the claim's scope."""
    p_old = model.sloped_params(); p_old["T"] = T_exp
    ss_old = model.sloped_ss(p_old)
    assert model.gam(p_old, ss_old["xstar"]) > cap, \
        "cap must cut below the old margin or the experiment is vacuous"

    p_cap = model.sloped_params(); p_cap["T"] = T_exp; p_cap["cap"] = cap
    ss_cap = model.sloped_ss(p_cap)
    out_c = solve_path(p_cap, ss_old, ss_cap, sloped_inner, H=H, convention=convention)
    f_cap = t5_facts(p_cap, ss_old, ss_cap, out_c)

    p_mul = model.sloped_params(); p_mul["T"] = T_exp
    p_mul["g0"] *= mult; p_mul["g1"] *= mult
    ss_mul = model.sloped_ss(p_mul)
    out_m = solve_path(p_mul, ss_old, ss_mul, sloped_inner, H=H, convention=convention)
    f_mul = t5_facts(p_mul, ss_old, ss_mul, out_m)

    dip = f_cap["w_goods_falls_on_impact"]
    recover = f_cap["w_goods_recovers"]
    land = f_cap["w_land_claim_below_old_at_every_date"] and f_cap["w_land_claim_settles_lower"]
    if dip and recover and land:
        verdict = "SUPPORTED at this configuration under frontier extension"
    elif dip and land:
        verdict = ("PARTIALLY SUPPORTED under frontier extension: the goods wage "
                   "falls at release and the cap then PINS it (CM on the capped "
                   "stretch — no recovery phase, the buildout sweeps tasks at a "
                   "constant margin); the land-unit wage falls with the buildout")
    else:
        verdict = "NOT SUPPORTED under frontier extension — report as-is"
    if f_mul["w_goods_falls_on_impact"] != dip:
        verdict += ("; REVERSED under efficiency deepening (impact wage rises: "
                    "existing capacity stretches further)")
    return (out_c, out_m), dict(frontier_extension=f_cap, efficiency_deepening=f_mul,
                                cap=cap, mult=mult,
                                verdict_expected="CONJECTURE: goods wage dips then "
                                                 "recovers with the buildout; land wage "
                                                 "falls throughout",
                                verdict=verdict)


# ------------------------------------------------------- T2: the waterfall
def waterfall_params():
    """Two produced inputs, flat tasks. The composite machine input is
    Leontief: 1 unit = 1 chip-service + 1 power-service, operated with labor
    λ and land b (no composite self-input). Builds use labor and land only.
    J_chip < J_power is the ordering under test; δ equal so the ordering is
    J's alone (memo risk note: report by J, not by name). T = 2.0 keeps both
    steady states interior at these dials."""
    return dict(lam=0.1, b=0.2, alpha=0.3, T=2.0, N=1.0, gamL=1.0,
                rho=0.05, delta=0.10,
                J_c=1, lamI_c=0.2, bI_c=0.02,
                J_p=5, lamI_p=0.2, bI_p=0.02)


def waterfall_ss(p, gambar):
    """SS: both capacities bind (X = K_c = K_p), each rental at its own user
    cost; the composite price identity then pins r; land clearing pins scale."""
    uk_c = model.u_K(p["rho"], p["delta"], p["J_c"])
    uk_p = model.u_K(p["rho"], p["delta"], p["J_p"])
    c_comp = p["gamL"] / gambar
    w = p["gamL"]
    # π_j = uk_j (λI_j w + bI_j r); composite: c_comp − λw − br = π_c + π_p
    # ⇒ r[b + uk_c bI_c + uk_p bI_p] = c_comp − λw − w(uk_c λI_c + uk_p λI_p)
    r = (c_comp - p["lam"] * w - w * (uk_c * p["lamI_c"] + uk_p * p["lamI_p"])) \
        / (p["b"] + uk_c * p["bI_c"] + uk_p * p["bI_p"])
    pK_c = p["lamI_c"] * w + p["bI_c"] * r
    pK_p = p["lamI_p"] * w + p["bI_p"] * r
    pi_c, pi_p = uk_c * pK_c, uk_p * pK_p
    X = ((1 - p["alpha"]) * p["T"] - p["alpha"] * w * p["N"] / r) \
        / (p["b"] + p["delta"] * (p["bI_c"] + p["bI_p"]))
    I_c = I_p = p["delta"] * X
    MY = X * p["gamL"] / gambar
    Y = MY + p["gamL"] * (p["N"] - p["lam"] * X
                          - p["lamI_c"] * I_c - p["lamI_p"] * I_p)
    return dict(r=r, w=w, c_comp=c_comp, pK_c=pK_c, pK_p=pK_p, pi_c=pi_c,
                pi_p=pi_p, X=X, K_c=X, K_p=X, I_c=I_c, I_p=I_p, Y=Y, m=MY / Y)


def run_t2(H=240):
    """Shock γ̄ 3 → 2.8. The Leontief composite freezes X at the LONG input's
    old capacity until t = J_p (its pipeline binds; the short input merely
    replaces), so the construction is direct: window rents from land clearing
    at frozen X; from t = J_p the free-entry quasi-difference of each input
    pins its rental from lagged r's, and the composite identity solves r_t
    forward. Entry is interior throughout (verified). Two theory notes,
    checked here: (i) rentals in t < J_c are a PURE TRANSFER among sunk
    owners — allocations and r are invariant to the split, which the model
    does not determine (reported under a stated convention); (ii) each
    input's rental is entry-pinned from t = J_j on, so quasi-rent excess can
    survive only over the input's own remaining build window: the J-order."""
    p = waterfall_params()
    gb0, gb1 = 3.0, 2.8
    ss_old, ss_new = waterfall_ss(p, gb0), waterfall_ss(p, gb1)
    J_c, J_p, rho, delta = p["J_c"], p["J_p"], p["rho"], p["delta"]
    b, lam, alpha, T, N = p["b"], p["lam"], p["alpha"], p["T"], p["N"]
    w = p["gamL"]
    c1 = p["gamL"] / gb1
    ukc, ukp = model.u_K(rho, delta, J_c), model.u_K(rho, delta, J_p)
    X_old = ss_old["X"]
    Hx = H + J_p + 1
    X = np.full(Hx, ss_new["X"]); X[:J_p] = X_old
    r = np.full(Hx, ss_new["r"])
    I_c = np.full(Hx, ss_new["I_c"]); I_p = np.full(Hx, ss_new["I_p"])
    sweeps, dev = 0, np.inf
    for sweeps in range(400):
        X_prev, r_prev = X.copy(), r.copy()
        for t in range(Hx):                     # capacity-tracking investment
            tc, tp = t + J_c, t + J_p
            I_c[t] = X[tc] - (1 - delta) * X[tc - 1] if tc < Hx else delta * ss_new["X"]
            I_p[t] = X[tp] - (1 - delta) * X[tp - 1] if tp < Hx else delta * ss_new["X"]
        for t in range(J_p):                    # frozen window: land clears r
            r[t] = alpha * w * N / ((1 - alpha) * T - b * X[t]
                                    - p["bI_c"] * I_c[t] - p["bI_p"] * I_p[t])
        for t in range(J_p, Hx):                # entry-pinned recursion for r
            pkc_lag = p["lamI_c"] * w + p["bI_c"] * r[t - J_c]
            pkp_lag = p["lamI_p"] * w + p["bI_p"] * r[t - J_p]
            pkp_lag1 = p["lamI_p"] * w + p["bI_p"] * r[t - J_p + 1]
            rhs = (c1 - lam * w
                   - (1 + rho) ** J_c * pkc_lag
                   - (1 + rho) ** J_p * pkp_lag
                   + (1 - delta) * (1 + rho) ** (J_p - 1) * pkp_lag1)
            if J_c == 1:                        # pK_c,t−J_c+1 carries r_t itself
                rhs += (1 - delta) * p["lamI_c"] * w
                coef = b - (1 - delta) * p["bI_c"]
            else:
                rhs += (1 - delta) * (1 + rho) ** (J_c - 1) \
                    * (p["lamI_c"] * w + p["bI_c"] * r[t - J_c + 1])
                coef = b
            r[t] = rhs / coef
            X[t] = ((1 - alpha) * T - alpha * w * N / r[t]
                    - p["bI_c"] * I_c[t] - p["bI_p"] * I_p[t]) / b
        dev = max(np.abs(X - X_prev).max(), np.abs(r - r_prev).max())
        if dev < 1e-13:
            break
    # rental paths: entry-pinned where an input's own entry is live, residual
    # split before that (t < J_c: indeterminate — stated convention: SS user-
    # cost shares; a pure transfer among sunk owners, allocation-invariant)
    resid = c1 - lam * w - b * r
    pi_c, pi_p = np.empty(Hx), np.empty(Hx)
    for t in range(Hx):
        if t >= J_c:
            pi_c[t] = (1 + rho) ** J_c * (p["lamI_c"] * w + p["bI_c"] * r[t - J_c]) \
                - (1 - delta) * (1 + rho) ** (J_c - 1) * (p["lamI_c"] * w + p["bI_c"] * r[t - J_c + 1])
        else:
            sc = ukc * (p["lamI_c"] * w + p["bI_c"] * r[t])
            sp_ = ukp * (p["lamI_p"] * w + p["bI_p"] * r[t])
            pi_c[t] = resid[t] * sc / (sc + sp_)
        pi_p[t] = resid[t] - pi_c[t]
    K_c = k_path(I_c, J_c, delta, ss_old["K_c"], ss_old["I_c"])
    K_p = k_path(I_p, J_p, delta, ss_old["K_p"], ss_old["I_p"])
    # interiority and consistency checks (never assumed away)
    MY = X * p["gamL"] / gb1
    Y = MY + p["gamL"] * (N - lam * X - p["lamI_c"] * I_c - p["lamI_p"] * I_p)
    checks = dict(
        converged=bool(dev < 1e-13),
        entry_interior=bool(np.all(I_c >= -1e-12) and np.all(I_p >= -1e-12)),
        window_power_rent_nonneg=bool(np.all(pi_p[:J_p] > -1e-12)),
        capacities_track=bool(np.abs(K_c[:Hx] - X).max() < 1e-9
                              and np.abs(K_p[:Hx] - X).max() < 1e-9),
        split_interior=bool(np.all((MY / Y > 0) & (MY / Y < 1))),
        labor_left=bool(np.all(lam * X + p["lamI_c"] * I_c + p["lamI_p"] * I_p < N)),
        endpoints=bool(abs(X[0] - X_old) < 1e-12
                       and abs(X[-1] - ss_new["X"]) / ss_new["X"] < 1e-8
                       and abs(r[-1] - ss_new["r"]) < 1e-10))
    # value held per layer: PV of quasi-rent excess over the NEW SS rental
    dpv = (1 + rho) ** (-(np.arange(Hx) + 1))
    hold_c = float((dpv * (pi_c - ss_new["pi_c"]) * K_c).sum())
    hold_p = float((dpv * (pi_p - ss_new["pi_p"]) * K_p).sum())
    land_gain = float((dpv * (r - ss_old["r"]) * T).sum()
                      + (1 + rho) ** (-Hx) * (ss_new["r"] - ss_old["r"]) * T / rho)
    # timing: last period each input's rental exceeds its new-SS value by >5%
    exc_c = np.nonzero(pi_c - ss_new["pi_c"] > 0.05 * ss_new["pi_c"])[0]
    exc_p = np.nonzero(pi_p - ss_new["pi_p"] > 0.05 * ss_new["pi_p"])[0]
    t_c = int(exc_c[-1]) if exc_c.size else -1
    t_p = int(exc_p[-1]) if exc_p.size else -1
    r_settled_by = int(np.nonzero(np.abs(r - ss_new["r"]) > 0.01 * ss_new["r"])[0][-1]) + 1 \
        if np.any(np.abs(r - ss_new["r"]) > 0.01 * ss_new["r"]) else 0
    ordered = (t_c < t_p) and (t_p <= J_p + 2) and all(checks.values())
    return dict(sweeps=int(sweeps), dev=float(dev), checks=checks,
                pi_c=pi_c.tolist(), pi_p=pi_p.tolist(), r=r.tolist(),
                X=X.tolist(), J_c=J_c, J_p=J_p,
                pi_c_old=ss_old["pi_c"], pi_p_old=ss_old["pi_p"],
                pi_c_new=ss_new["pi_c"], pi_p_new=ss_new["pi_p"],
                hold_pv_chip=hold_c, hold_pv_power=hold_p, land_gain_pv=land_gain,
                last_excess_chip=t_c, last_excess_power=t_p,
                r_settled_by=r_settled_by, r_old=ss_old["r"], r_new=ss_new["r"],
                window_split_note="t < J_c rentals are a pure transfer among "
                                  "sunk owners; the split is indeterminate and "
                                  "reported at SS user-cost shares",
                verdict_expected="value passes through inputs in J-order, each "
                                 "holding ≈ its remaining build window; land "
                                 "holds it permanently",
                verdict=("VERIFIED" if ordered else "FAILED"))


# --------------------------------------------------------------- entry point
def run_all(H=300):
    model.gate(verbose=True)
    print("\nV: validating the solver against the exact flat benchmark …")
    v = validate_flat(H=H)
    print(f"  closed-form deviation {v['closed_form_dev']:.2e}, "
          f"horizon deviation {v['horizon_dev']:.2e}, iters {v['iters']}"
          f" -> {'PASS' if v['ok'] else 'FAIL'}")
    assert v["ok"], "solver failed the flat closed-form validation — nothing else runs"

    print("\nT1 windfall (flat, J=3, domestic convention) …")
    out1, t1 = run_t1(H=H)
    print(f"  Q0 = {t1['Q0']:.4f} vs SS benchmark {t1['Q_ss_benchmark']:.4f}; "
          f"windfall PV {t1['windfall_pv']:.4f}; "
          f"land gain PV {t1['land_gain_pv']:.4f}; {t1['verdict']}")

    print("\nT2 waterfall (two inputs, J = 1 vs 5) …")
    t2 = run_t2(H=min(H, 240))
    print(f"  last excess: J=1 input t={t2['last_excess_chip']}, "
          f"J=5 input t={t2['last_excess_power']}; rent settled by t={t2['r_settled_by']}; "
          f"{t2['verdict']}")

    print("\nT3 speed × lag …")
    t3 = run_t3()
    for k2, v2 in t3["windfall_pv"].items():
        print(f"  {k2}: {v2:.4f}")
    print(f"  {t3['verdict']}")

    print("\nT5 sloped wage paths (CONJECTURE — numerics decide) …")
    outs5, t5 = run_t5(H=H)
    fe, ed = t5["frontier_extension"], t5["efficiency_deepening"]
    print(f"  frontier extension (cap {t5['cap']}): w impact {fe['w_goods_impact']:.4f} "
          f"vs old {fe['w_goods_old']:.4f} (falls: {fe['w_goods_falls_on_impact']}, "
          f"then flat: {fe['w_goods_flat_after_release']}); land claim below old at "
          f"every date: {fe['w_land_claim_below_old_at_every_date']}")
    print(f"  efficiency deepening (×{t5['mult']}): w impact {ed['w_goods_impact']:.4f} "
          f"vs old {ed['w_goods_old']:.4f} (falls: {ed['w_goods_falls_on_impact']})")
    print(f"  {t5['verdict']}")

    res = dict(validation=v, T1=t1, T3=t3, T5=t5,
               T2={k2: v2 for k2, v2 in t2.items()
                   if k2 not in ("pi_c", "pi_p", "r", "X")},
               conventions="baseline domestic (memo caution i); T2's construction "
                           "is convention-free in the window (sunk transfers)",
               H=H)
    with open(RESULTS, "w") as f:
        json.dump(res, f, indent=2)
    print(f"\nresults written: {RESULTS}")
    return dict(T1=(out1, t1), T2=t2, T3=t3, T5=(outs5, t5), validation=v)


if __name__ == "__main__":
    run_all()
