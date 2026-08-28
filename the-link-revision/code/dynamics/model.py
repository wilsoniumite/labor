# model.py — the v2 dynamic environment: recipes, steady states, the hard gate.
# (rewrite brief v2 §3.5, structure memo STATE log 32; 2026-08-28)
#
# Conventions pinned here (same as checks/check_dynamics.py, which derives them):
#   timing: build paid at start of t; first service in t+J (undepreciated);
#           wear post-install at δ per service period. u_K = (ρ+δ)(1+ρ)^{J−1}.
#   financing: builds 100%-externally financed at world ρ; free entry makes
#           SS machine cash to households exactly 0, so SS Inc = wN + rT and
#           goods clearing carries NX = πK − p_K I. In TRANSITION the
#           convention decides who books the π-surprises on pre-shock
#           vintages: "domestic" (baseline, memo's suggestion) adds
#           M_t = (π_t − π̄_old)·S_t to household income; "foreign" books
#           them abroad (M_t = 0).
#
# House gate: nothing in solve.py runs an experiment before gate() passes —
# both steady states here must reproduce checks/dynamics_ss_targets.json
# (written by check_dynamics.py, tied there to check_pinning's A-joint root).
#
# Run the gate alone: ../venv/Scripts/python.exe code/dynamics/model.py

import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))                # the-link-revision/
TARGETS = os.path.join(ROOT, "checks", "dynamics_ss_targets.json")


def u_K(rho, delta, J):
    """User cost with gestation, derived in check_dynamics U3 (never assert a
    different exponent here — the off-by-one is the classic error)."""
    return (rho + delta) * (1.0 + rho) ** (J - 1)


# ------------------------------------------------------------ configurations
def flat_params():
    """The worked flat instantiation. T = 3.8 keeps every experiment endpoint
    (γ̄ ∈ {3, 2.8} × J ∈ {1, 2, 3, 4}) inside the interior regime — the
    region is narrow (checks E4/E4b/E5)."""
    return dict(a=0.5, lam=0.1, b=0.2, aI=0.1, lamI=0.2, bI=0.02,
                rho=0.05, delta=0.10, J=3, gambar=3.0, gamL=1.0,
                alpha=0.3, T=3.8, N=1.0)


def sloped_params():
    """check_pinning's Appendix-A joint config extended with the build recipe."""
    return dict(a=0.5, lam=0.1, b=0.2, aI=0.1, lamI=0.2, bI=0.02,
                rho=0.05, delta=0.10, J=3, gamL=1.0,
                alpha=0.3, T=10.0, N=1.0, s0=1.0, he=0.5, sd=0.2,
                g0=1.0, g1=4.0)          # schedule γ(x) = g0 + g1·x


def gam(p, x):
    """Schedule γ(x) = g0 + g1·x, optionally capped: γ = min(·, cap). The cap
    is the frontier-extension shock (the sloped analogue of a γ̄ fall: tasks
    above the kink become automatable at the cap without cheapening the
    already-automated ones)."""
    g = p["g0"] + p["g1"] * x
    cap = p.get("cap")
    return min(g, cap) if cap is not None else g


def Igam(p, x):
    """∫_0^x γ(u) du, piecewise under a cap."""
    cap = p.get("cap")
    if cap is None or cap >= p["g0"] + p["g1"] * x:
        return p["g0"] * x + 0.5 * p["g1"] * x * x
    xk = max((cap - p["g0"]) / p["g1"], 0.0)
    return p["g0"] * xk + 0.5 * p["g1"] * xk * xk + cap * (x - xk)


# --------------------------------------------------------- flat steady state
def flat_ss(p):
    """Closed-form flat SS (interior regime), from check_dynamics section E.
    Returns the full state and the named interiority/viability flags."""
    uk = u_K(p["rho"], p["delta"], p["J"])
    c = p["gamL"] / p["gambar"]                    # 1 = c·γ̄·L̄, L̄ = 1/γ_L
    w = p["gamL"]                                  # w = γ̄c
    Den = 1 - p["a"] - p["lam"] * p["gambar"] - uk * (p["aI"] + p["lamI"] * p["gambar"])
    theta_c = (p["b"] + uk * p["bI"]) / Den
    r = c / theta_c
    pK = p["aI"] * c + p["lamI"] * w + p["bI"] * r
    pi = uk * pK
    X = ((1 - p["alpha"]) * p["T"] - p["alpha"] * w * p["N"] / r) / (p["b"] + p["bI"] * p["delta"])
    K, I = X, p["delta"] * X
    MY = X * (1 - p["a"] - p["aI"] * p["delta"]) * p["gamL"] / p["gambar"]
    Y = MY + p["gamL"] * (p["N"] - (p["lam"] + p["lamI"] * p["delta"]) * X)
    m = MY / Y
    flags = dict(viable=Den > 0,
                 land_viable=(1 - p["alpha"]) * p["T"] > p["b"] * X + p["bI"] * I,
                 interior_split=0 < m < 1,
                 labor_left=(p["lam"] + p["lamI"] * p["delta"]) * X < p["N"],
                 pos=min(X, Y, r) > 0)
    return dict(c=c, w=w, r=r, pK=pK, pi=pi, uK=uk, X=X, K=K, I=I, Y=Y, m=m,
                Den=Den, theta_c=theta_c, flags=flags)


# ------------------------------------------------------- sloped steady state
def sloped_state(p, xs):
    """The extended joint system at a candidate margin x* (γ_L = 1 form).
    One land residual; free entry π = u_K p_K replaces flow zero-profit."""
    uk = u_K(p["rho"], p["delta"], p["J"])
    g = gam(p, xs)
    Ig = Igam(p, xs)
    c = 1.0 / (g * (1 - xs) + Ig)                  # unit cost of the good = 1
    w = g * c                                      # the margin
    Den = 1 - p["a"] - p["lam"] * g - uk * (p["aI"] + p["lamI"] * g)
    r = c * Den / (p["b"] + uk * p["bI"])          # free entry
    Y = p["N"] / ((1 - xs) + (p["lam"] + p["lamI"] * p["delta"]) * Ig
                  / (1 - p["a"] - p["aI"] * p["delta"]))
    X = Y * Ig / (1 - p["a"] - p["aI"] * p["delta"])
    land = (p["b"] + p["bI"] * p["delta"]) * X + p["alpha"] * (w * p["N"] + r * p["T"]) / r
    return dict(resid=land - p["T"], c=c, w=w, r=r, Y=Y, X=X, K=X,
                I=p["delta"] * X, Den=Den, uK=uk, xstar=xs,
                pK=p["aI"] * c + p["lamI"] * w + p["bI"] * r)


def sloped_ss(p):
    """Bisect the land residual on the viable set (unique crossing there —
    check EJ1). Returns the full state."""
    grid = [i / 1000.0 for i in range(1, 990)]
    vgrid = [x for x in grid if sloped_state(p, x)["Den"] > 0]
    lo, hi = vgrid[0], vgrid[-1]
    assert (sloped_state(p, lo)["resid"] > 0) != (sloped_state(p, hi)["resid"] > 0), \
        "no crossing on the viable set"
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if (sloped_state(p, lo)["resid"] > 0) == (sloped_state(p, mid)["resid"] > 0):
            lo = mid
        else:
            hi = mid
    st = sloped_state(p, 0.5 * (lo + hi))
    st["pi"] = st["c"] * (1 - p["a"]) - p["lam"] * st["w"] - p["b"] * st["r"]
    return st


# ------------------------------------------------------------- the hard gate
def gate(verbose=True):
    """Reproduce checks/dynamics_ss_targets.json to 1e-9 before anything runs.
    Also re-derive the degenerate (build → 0) sloped root and match it against
    an inline restatement of check_pinning's static joint system."""
    with open(TARGETS) as f:
        tg = json.load(f)

    fs = flat_ss(tg["flat"]["params"])
    for k in ("c", "w", "r", "X", "Y", "m", "uK"):
        assert abs(fs[k] - tg["flat"][k]) < 1e-9, f"flat gate: {k} mismatch"
    assert all(fs["flags"].values()), f"flat gate: flags {fs['flags']}"

    sp_ = dict(sloped_params())
    sp_.update({k: v for k, v in tg["sloped"]["params"].items()
                if k in sp_ and not isinstance(v, str)})
    ss = sloped_ss(sp_)
    for k in ("xstar", "c", "w", "r", "Y", "X", "pK", "uK"):
        assert abs(ss[k] - tg["sloped"][k]) < 1e-9, f"sloped gate: {k} mismatch"

    # build → 0 nesting against check_pinning's A-joint formulas, restated
    p0 = dict(sp_)
    p0.update(aI=0.0, lamI=0.0, bI=0.0)
    d0 = sloped_ss(p0)

    def joint_static(xs):                          # check_pinning lines 238-248
        g = 1 + 4 * xs
        Ig = xs + 2 * xs * xs
        c = 1.0 / (g * (1 - xs) + Ig)
        w = g * c
        r = c * (1 - 0.5 - 0.1 * g) / 0.2
        Y = 1.0 / ((1 - xs) + 0.1 * Ig / 0.5)
        X = Y * Ig / 0.5
        return 0.2 * X + 0.3 * (w + r * 10.0) / r - 10.0, w, c, r, Y, X

    lo, hi = 0.001, 0.989
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if (joint_static(lo)[0] > 0) == (joint_static(mid)[0] > 0):
            lo = mid
        else:
            hi = mid
    xs0 = 0.5 * (lo + hi)
    st0 = joint_static(xs0)
    assert abs(d0["xstar"] - xs0) < 1e-9, "nesting gate: x* mismatch"
    for got, want in zip((d0["w"], d0["c"], d0["r"], d0["Y"], d0["X"]), st0[1:6]):
        assert abs(got - want) < 1e-9, "nesting gate: value mismatch"

    if verbose:
        print("GATE PASS: flat SS, sloped SS match check targets to 1e-9; "
              "build→0 reproduces check_pinning's A-joint root.")
    return dict(flat=fs, sloped=ss)


if __name__ == "__main__":
    gate()
