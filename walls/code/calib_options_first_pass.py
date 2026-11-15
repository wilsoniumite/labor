# calib_options.py — scratch (not part of the paper): Appendix B's backward calibration (parameters from shares,
# pinning/STATE.md Log 2026-11-03) redone in closed form, then the wall options held against it.
#   1. What the seven shares pin: the margin x*, the return, and the machine chain's wall as a multiple of gamma(x*).
#   2. The two roots in k, both solved with appendix_b.solve, with Figure 3's comparative statics on each.
#   3. A hard wall H (law, preference or capability) above the margin: the calibrated economy is unchanged, the
#      automation path is not.
# Run from walls/:  python code/calib_options_first_pass.py
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "pinning" / "code"))
import appendix_b as ab  # noqa: E402

TG = dict(theta_V=0.47, machines=0.20, labor=0.47, site=0.06, chain=0.15, part=0.60, Y=3.0)   # unrounded targets
FIX = dict(N=1.0, b=0.4, delta=0.05, g0=0.01, g1=0.99, eta=1.0)
R = (1 - TG["labor"] - TG["site"]) / TG["labor"]        # machine-task over labor-task cost in the basket (= 1 here)


def x_star(tg=TG, N=1.0):
    """Participation, the chain's share of hours and baskets a person pin the margin: 1 - x* = n (1 - chain) / Y."""
    return 1 - tg["part"] * N * (1 - tg["chain"]) / tg["Y"]


def gam(x, k, g0=0.01, g1=0.99):
    return g0 + g1 * x ** k


def Jint(x, k, g0=0.01, g1=0.99):
    return g0 * x + g1 * x ** (k + 1) / (k + 1)


def k_equation(k, x):
    """The schedule's one condition: machine cost of the tasks below the margin = R x labor cost of those above."""
    return Jint(x, k) - R * gam(x, k) * (1 - x)


def calibrate(k, tg=TG, fix=FIX):
    x, d = x_star(tg, fix["N"]), fix["delta"]
    cpt = tg["machines"] * d + tg["theta_V"] * d * R * (1 - tg["chain"]) / tg["chain"]     # rho + delta
    a, g = tg["machines"] / cpt, gam(x, k)
    lam = tg["theta_V"] / (cpt * g)
    D = 1 - tg["machines"] - tg["theta_V"]
    pm = cpt * fix["b"] / D
    v = g * pm
    Ps = v * (1 - x) / tg["labor"]
    h = tg["site"] * Ps
    T = tg["Y"] * (h + fix["b"] * d * Jint(x, k) / (1 - a * d))
    return dict(N=fix["N"], T=T, h=h, a=a, b=fix["b"], lam=lam, g0=fix["g0"], g1=fix["g1"], k=k, eta=1.0,
                chi_max=np.log1p(v / Ps) / tg["part"], rho=cpt - d, delta=d)


def solve_H(P, xH):
    """Appendix B's economy with tasks [xH, 1] closed to machines outright. Interior margin as in Lemma B.1 when the
    crossing falls below min(x_c, xH); otherwise, if xH comes first, labor holds only H and the wage clears
    n_S(w/P_s) = n_D(xH), with the machine rental at its user cost on the wage, no longer tied to a margin."""
    xc = ab.ceiling(P)
    up = min(xc, xH)
    if up == xc or ab.excess_demand(P, up) < 0:
        q = ab.solve(P) if up == xc else None
        if q is None:
            x = brentq(lambda t: ab.excess_demand(P, t), 0.0, up, xtol=1e-15)
            q = ab.at(P, x)
        return dict(x=q["x"], real_wage=q["real_wage"], participation=q["nD"] / P["N"], regime="interior")
    cpt = P["rho"] + P["delta"]
    nD = ab.demand(P, xH)[4]
    J = ab.J(P, xH)

    def real(v):
        pm = cpt * (P["lam"] * v + P["b"]) / (1 - cpt * P["a"])
        return v / (v * (1 - xH) + pm * J + P["h"])

    need = np.expm1(P["chi_max"] * nD / P["N"])          # the w/P_s at which n_S = n_D (F uniform)
    v0 = ab.gamma(P, xH) * cpt * P["b"] / ab.denominator(P, xH)      # the wage at which the margin sits at xH
    vmax_real = 1 / ((1 - xH) + cpt * P["lam"] * J / (1 - cpt * P["a"]))
    assert real(v0) <= need < vmax_real, "no boundary equilibrium"
    v = brentq(lambda t: real(t) - need, v0, v0 * 1e12)
    return dict(x=xH, real_wage=real(v), participation=nD / P["N"], regime="only H")


# ---------------------------------------------------------------- 1. what the shares pin
x = x_star()
cpt = TG["machines"] * FIX["delta"] + TG["theta_V"] * FIX["delta"] * R * (1 - TG["chain"]) / TG["chain"]
print(f"1. x* = {x:.4f}; rho = {cpt - FIX['delta']:.4f}; w/P_s = labor/(1 - x*) = {TG['labor'] / (1 - x):.3f}")
print(f"   the chain's wall: gamma(x_c)/gamma(x*) = (1 - machines)/theta_V = {(1 - TG['machines']) / TG['theta_V']:.3f}"
      f"; full-chain labor share of machine services at the margin = {TG['theta_V'] / (1 - TG['machines']):.4f}")

# ---------------------------------------------------------------- 2. the two roots in k
ks = np.linspace(1.0, 40.0, 4000)
fk = np.array([k_equation(k, x) for k in ks])
roots = [brentq(k_equation, ks[i], ks[i + 1], args=(x,)) for i in range(len(ks) - 1) if fk[i] * fk[i + 1] < 0]
print(f"2. roots in k: {', '.join(f'{r:.3f}' for r in roots)}")
CAL = {}
for r in roots:
    P = calibrate(r)
    q = ab.solve(P)
    s = ab.shares(P, q)
    f3 = ab.figure3(P)
    CAL[r] = P
    print(f"   k {r:6.3f}: x* {q['x']:.4f}  x_c {q['x_ceiling']:.4f} (gap {q['x_ceiling'] - q['x']:.3f})  gamma* {q['gamma']:.4f}"
          f"  participation {q['participation']:.3f}  Y {q['Y']:.3f}  rho {P['rho']:.4f}  lam {P['lam']:.2f}  a {P['a']:.3f}")
    print(f"            shares: theta_V {s['theta_V']:.3f} machines {s['machines']:.3f} labor {s['labor']:.3f} "
          f"site {s['site']:.3f} chain {s['chain']:.3f}")
    b0 = f3["baseline"]["real_wage"]
    print("            Figure 3: " + "; ".join(f"{n} w/P_s {e['real_wage']:.3f} ({e['real_wage'] / b0 - 1:+.1%}), N_a/N "
                                             f"{e['participation']:.3f}, x* {e['x']:.4f}" for n, e in f3.items()))

# ---------------------------------------------------------------- 3. a hard H above the margin (the low root)
P = CAL[roots[0]]
print(f"3. low root: the calibrated equilibrium with a hard H at the top (H = [xH, 1]) and along the automation path")
for xH in (1.0, 0.95, 0.90, 0.85):
    base = solve_H(P, xH) if xH < 1 else dict(x=ab.solve(P)["x"], real_wage=ab.solve(P)["real_wage"],
                                             participation=ab.solve(P)["participation"], regime="interior")
    task = solve_H({**P, "eta": 0.5}, xH) if xH < 1 else None
    line = f"   |H| {1 - xH:.2f}: baseline x* {base['x']:.4f} w/P_s {base['real_wage']:.3f} N_a/N {base['participation']:.3f}"
    if task:
        line += f" | task automation: {task['regime']}, w/P_s {task['real_wage']:.3f}, N_a/N {task['participation']:.3f}"
    print(line)
    path = []
    for eta in (1.0, 0.3, 0.1, 0.03, 0.01, 0.001):
        Q = ab.sequence(P, eta)
        e = solve_H(Q, xH) if xH < 1 else dict(regime="interior", **{k: ab.solve(Q)[kk] for k, kk in
                                                                       (("x", "x"), ("real_wage", "real_wage"),
                                                                        ("participation", "participation"))})
        path.append(f"eta {eta}: {e['participation']:.3f}/{e['real_wage']:.2f}{'*' if e['regime'] == 'only H' else ''}")
    print("            automation path N_a/N / w/P_s (* = labor holds only H): " + "; ".join(path))
