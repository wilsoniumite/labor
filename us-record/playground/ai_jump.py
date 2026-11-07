# ai_jump.py — a lead (2026-11-07): what would an AI-style capability jump do to the fitted 2024 economy, all else equal?
# The record-set fit without the wave (results/fit_Br0.json), its 2024 economy as fitted (adults, depreciation, land,
# the basket's utility, the reference prices of 1950): the machine service that the other goods' tasks need (their clock
# eta_g) is lowered by a factor, durables' clock and everything else held; then also the case where hours in a machine
# (lambda) rise with it, as in the record (on the ceiling only lambda times eta matters). A comparative static, not a
# path: the same year's economy before and after. Reads: the share of tasks done by machines, the wage over goods and over
# the basket, prime-age employment, labour's share, the machine chain's share of pay, income shares, land rent per adult.
# A second set lets the basket's utility follow the real wage the jump brings (a fixed point), as along the fitted
# history. Run from us-record/:  python3 playground/ai_jump.py      (writes playground/ai_jump.json)
import json
import sys
from dataclasses import replace

import numpy as np

sys.path.insert(0, "code")
import fit_base as F  # noqa: E402
import pinning_model as pm  # noqa: E402
import two_goods as tg  # noqa: E402


def year_2024(meta, par):
    """The fitted economy of 2024 and its composite's settings, exactly as fit_base.durables_years builds them."""
    F.configure(meta)
    par = F.fill(par)
    par = dict(par, chi_max=F.pinned_chi(par))
    eta_g, eta_d = F.eta_path(par), F.eta_d_path(par)
    phi = F.VALUE_RENT or 0.0
    q0 = tg.solve(F.economies(par, eta_g)[0], eta_d[0], dict(mode="ref", omega_d=F.DURABLES["omega_d"], phi=phi))
    cmp = dict(omega_d=F.DURABLES["omega_d"], sigma_dg=F.DURABLES["sigma_dg"], pref_d=q0["pd"], pref_g=q0["pg"], phi=phi)
    es = F.economies(par, eta_g, q0["c"])
    return es[-1], eta_d[-1], cmp


def read(e, eta_d, cmp):
    q = tg.solve(e, eta_d, cmp)
    inc = q["income"]
    return dict(x_other=q["xg"], x_durables=q["xd"], wage_over_goods=q["v"] / q["pg"], wage_over_basket=q["v"] / q["Ps"],
                participation=q["participation"], labour_share=q["labour_share_bea"], chain=q["chain_share"],
                pay=q["v"] * q["n"] / inc, machines=e.rho * q["Vm"] * q["K"] / inc, imported=q["rent_income"], land=e.T / inc,
                rent_per_adult_over_basket=e.T / e.N / q["Ps"], margin=q["m"], ceiling=q["m_ceiling"])


if __name__ == "__main__":
    R = json.load(open("results/fit_Br0.json"))
    e, eta_d, cmp = year_2024(R["meta"], R["best"]["par"])
    base = read(e, eta_d, cmp)
    rows = []
    for s in (0.1, 0.25, 0.5, 0.75, 1.0):
        for lam_too in (False, True):
            # capability: the other goods' tasks need e^-s as much machine service; with lam_too, hours in a machine rise by
            # the same factor (lambda times eta unchanged: the jump then changes nothing on the ceiling but off it)
            e2 = replace(e, eta=e.eta * np.exp(-s), lam=e.lam * (np.exp(s) if lam_too else 1.0))
            try:
                r = read(e2, eta_d, cmp)
            except pm.NoEquilibrium as err:
                r = dict(error=str(err))
            rows.append(dict(size=s, lam_too=lam_too, **r))
    # the same jumps with the basket's utility following the real wage, as it does along the fitted history (utility set
    # through the real wage at its knots): a fixed point, utility scaled by the wage-over-basket gain it produces
    follow = []
    for s in (0.1, 0.25, 0.5, 0.75, 1.0):
        u = 1.0
        for _ in range(60):
            e2 = replace(e, eta=e.eta * np.exp(-s), utility=e.utility * u)
            try:
                r = read(e2, eta_d, cmp)
            except pm.NoEquilibrium as err:
                r = dict(error=str(err))
                break
            u_new = r["wage_over_basket"] / base["wage_over_basket"]
            if abs(u_new - u) < 1e-10:
                break
            u = 0.5 * u + 0.5 * u_new
        follow.append(dict(size=s, utility=u, **r))
    json.dump(dict(base=base, jumps=rows, utility_follows=follow), open("playground/ai_jump.json", "w"), indent=1)
    keys = ["x_other", "wage_over_goods", "wage_over_basket", "participation", "labour_share", "chain", "pay", "machines",
            "land", "rent_per_adult_over_basket"]
    print("2024 as fitted:   " + "  ".join(f"{k} {base[k]:.3f}" for k in keys))
    for r in rows:
        if "error" in r:
            print(f"jump {r['size']:.2f}{' (hours too)' if r['lam_too'] else ''}: {r['error']}")
            continue
        print(f"jump {r['size']:.2f}{' +hours' if r['lam_too'] else '       '}: " + "  ".join(
            f"{k} {r[k] / base[k]:.3f}x" if k.startswith(("wage", "rent")) else f"{k} {r[k]:.3f}" for k in keys))
    print("with the basket's utility following the real wage:")
    for r in follow:
        if "error" in r:
            print(f"jump {r['size']:.2f}: {r['error']}")
            continue
        print(f"jump {r['size']:.2f} (utility x{r['utility']:.3f}): " + "  ".join(
            f"{k} {r[k] / base[k]:.3f}x" if k.startswith(("wage", "rent")) else f"{k} {r[k]:.3f}" for k in keys))
