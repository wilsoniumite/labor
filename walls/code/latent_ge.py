# latent_ge.py — latent goods in general equilibrium on Appendix B's economy: does a reservoir of latent services
# cushion labor along the automation path once its labor demand feeds back on the wage?
#
# Services j: one task each; one unit takes one hour of labor or gamma_j machine-hours; no direct land. Demand is
# quasi-linear in baskets: each latent service, once its price (its cheaper route) is at or below R_j P_s, is bought in
# a fixed aggregate quantity; the reservoir's total size Q is the hours it would take if people did all of it. Walras'
# law holds as in Appendix B: services revenue equals their factor payments, the rest of income buys baskets. Land
# clearing with the services' machines: T = h Y + b delta (Y J + M_s)/(1 - a delta). At a threshold x (prices as in
# model.interior): L_s and M_s from the viable services, Y from land, n_D = Y (1 - x) + lam delta X + L_s, and the
# margin clears n_D = n_S.
# Run from walls/:  python code/latent_ge.py
import json
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import model as m  # noqa: E402

X0 = m.margin_from_targets()
RNG = np.random.default_rng(20261116)


def member(sigma):
    k = brentq(lambda kk: m.sigma_margin(m.calibrate(m.power_family(kk)), X0) - sigma, 3.95, 400.0, xtol=1e-8)
    return m.calibrate(m.power_family(k))


def prices(P, x):
    c, D = m.cpt(P), float(m.denominator(P, x))
    g, j = float(P["sched"]["g"](x)), float(P["sched"]["J"](x))
    pm = c * P["b"] / D
    v = g * pm
    return dict(g=g, J=j, pm=pm, v=v, Ps=v * (1 - x) + pm * j + P["h"])


def services(p, gam, R, Q):
    cost = np.minimum(p["v"], p["pm"] * gam)
    on = R * p["Ps"] >= cost
    lab = on & (gam > p["g"])
    return Q * lab.mean(), Q * np.mean(gam * (on & ~lab)), on.mean(), lab.mean()


def solve(P, gam, R, Q):
    ad = P["a"] * P["delta"]

    def parts(x):
        p = prices(P, x)
        L, Ms, on, lab = services(p, gam, R, Q) if Q > 0 else (0.0, 0.0, 0.0, 0.0)
        Y = (P["T"] - P["b"] * P["delta"] * Ms / (1 - ad)) / (P["h"] + P["b"] * P["delta"] * p["J"] / (1 - ad))
        Xm = (Y * p["J"] + Ms) / (1 - ad)
        nD = Y * (1 - x) + P["lam"] * P["delta"] * Xm + L
        nS = P["N"] * min(max(np.log1p(p["v"] / p["Ps"]) / P["chi_max"], 0.0), 1.0)
        return nD, nS, p, Y, L, on, lab

    xc = m.ceiling(P)
    f = lambda x: parts(x)[0] - parts(x)[1]          # noqa: E731
    # the services' switch-on makes n_D step; bisect on the sign (brentq would also work: f is piecewise smooth)
    lo, hi = 1e-9, xc * (1 - 1e-12)
    assert f(lo) > 0, "no crossing: labor demand below supply even with labor on every task"
    if f(hi) > 0:
        return absorbed(P, gam, R, Q, hi)
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if f(mid) > 0 else (lo, mid)
    x = 0.5 * (lo + hi)
    nD, nS, p, Y, L, on, lab = parts(x)
    return dict(x=x, real_wage=p["v"] / p["Ps"], participation=nS / P["N"], services_hours=L, Y=Y, on=on, lab=lab,
                regime="interior")


def absorbed(P, gam, R, Q, xtop):
    """Machines hold every final-good task (the margin at the top) and the latent services' labor demand still exceeds
    supply: the services market sets the wage. v rises above the wage that puts the margin at the top until the
    services that still employ people at v (viable, R_j P_s >= cost, and cheaper by hand, v < p_m gamma_j) match
    participation. The rental is the user cost on that wage (constant when lam = 0)."""
    c, ad = m.cpt(P), P["a"] * P["delta"]
    j = float(P["sched"]["J"](xtop))

    def at(v):
        pm = c * (P["lam"] * v + P["b"]) / (1 - c * P["a"])
        Ps = v * (1 - xtop) + pm * j + P["h"]
        cost = np.minimum(v, pm * gam)
        on = R * Ps >= cost
        lab = on & (v < pm * gam)
        L, Ms = Q * lab.mean(), Q * np.mean(gam * (on & ~lab))
        nS = P["N"] * min(max(np.log1p(v / Ps) / P["chi_max"], 0.0), 1.0)
        Y = (P["T"] - P["b"] * P["delta"] * Ms / (1 - ad)) / (P["h"] + P["b"] * P["delta"] * j / (1 - ad))
        return L + Y * (1 - xtop) - nS, v / Ps, nS, L, Y, on.mean(), lab.mean()

    v0 = prices(P, xtop)["v"]
    lo, hi = v0, v0 * 2
    while at(hi)[0] > 0:
        hi *= 2
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if at(mid)[0] > 0 else (lo, mid)
    ex, real, nS, L, Y, on, lab = at(0.5 * (lo + hi))
    return dict(x=xtop, real_wage=real, participation=nS / P["N"], services_hours=L, Y=Y, on=on, lab=lab,
                regime="services absorb labor")


if __name__ == "__main__":
    etas = [1.0, 0.3, 0.1, 0.03, 0.01, 0.003, 0.001]
    out = {}
    for name, sig in (("sigma 0.6", 0.6), ("low root (sigma 2.29)", 2.2932)):
        P = member(sig)
        P1 = {**P, "lam": 0.0}                                    # the path starts at the recursive-automation economy
        q1 = m.solve(P1)
        pos = RNG.uniform(X0, 1.0, 20_000)                        # latent tasks like labor's current ones
        gam0 = P["sched"]["g"](pos)
        p1 = prices(P1, q1["x"])
        u = RNG.uniform(0.0, 1.0, gam0.size)
        R = u * np.minimum(p1["v"], p1["pm"] * gam0) / p1["Ps"]   # none viable at the path's start
        out[name] = {}
        print(f"--- {name}")
        for Q in (0.0, 0.3):
            for reach in (("untouched", "general purpose") if Q > 0 else ("none",)):
                rows = []
                for eta in etas:
                    Pe = {**P1, "sched": m.scaled(P["sched"], eta)}
                    gam = gam0 * (eta if reach == "general purpose" else 1.0)
                    e = solve(Pe, gam, R, Q)
                    rows.append(dict(eta=eta, **{k: (v if isinstance(v, str) else float(v)) for k, v in e.items()}))
                key = "no reservoir" if Q == 0 else f"reservoir {Q}, {reach}"
                out[name][key] = rows
                print(f"    {key:32s}: " + "; ".join(f"{r['eta']:g}: {r['participation']:.3f}/{r['real_wage']:.2f}"
                                                   f" (svc {r['services_hours']:.3f}{'*' if r['regime'] != 'interior' else ''})" for r in rows))
    json.dump(out, open(HERE.parent / "results" / "latent_ge.json", "w"), indent=1)
    print("participation / w/P_s (services' hours per person); wrote results/latent_ge.json")
