# export_paths.py — the model's rate paths as a plain table, for anyone to put their own book on.
#
# Per scenario, per quarter over 25 years: the policy rate and the market's zero rates at 3M, 1Y,
# 2Y, 3Y, 5Y, 7Y and 10Y (%), in the model's own units (calibration (b), policy starting at 2.75%);
# and the true world's real wage bill of the start's workers (real wage x participation, 1 at t = 0).
# For a credit book, the pieces behind it and the property side, each 1 at t = 0: the real wage, the
# share of the start's workers still employed, the real site rent, and the real price of a site as the
# market values it (bank.house_price: its belief-weighted rents discounted at the real 10Y rate plus a
# premium); the price level carries them to nominal.
# A user applies the CHANGES from t = 0 to their own curve; the levels are the model's, not a market's.
# Scenarios: the status quo; a pure tightening (+250 bp, announced at year 1 — bank_scenarios.py);
# deep automation with deficits dominating (real rates rise) and with owners' saving dominating
# (rates fall), market beliefs by Bayesian learning; and deficits dominating with people digesting
# regime news over three years and AI adopted around year 5 (regime_digestion.py).
#
# Run from paths/:  ../venv/Scripts/python.exe code/export_paths.py
# Out: results/paths_for_banks.csv

from __future__ import annotations

import os
import sys
from dataclasses import replace

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bank as bk  # noqa: E402
import bank_scenarios as bs  # noqa: E402
import macro as m  # noqa: E402
import recognition as rc  # noqa: E402
import regimes as rg  # noqa: E402

TENORS = (0.25, 1.0, 2.0, 3.0, 5.0, 7.0, 10.0)
LABELS = ("z3M", "z1Y", "z2Y", "z3Y", "z5Y", "z7Y", "z10Y")


def curves(old, new, p):
    mixes, _, _, pol = rc.market_curves(old, new, p)
    z = np.array([rg.zero(np.array(TENORS), mx) for mx in mixes])
    return pol, z


def main():
    e, _, _, _ = m.calibrate(base=m.CAPITAL_BASE)
    rows = []

    def add(name, t, pol, z, world, old, new, p):
        wb = world["real_wage"] * world["participation"]
        wb = wb / wb[0]
        pi = new["pi_star"]
        house = bk.house_price(t, p, old["Ps"][0] / old["Ps"], new["Ps"][0] / new["Ps"], z[:, LABELS.index("z10Y")], pi)
        extra = {"real_wage": world["real_wage"] / world["real_wage"][0],
                 "employed": np.minimum(world["participation"] / world["participation"][0], 1.0),
                 "site_rent_real": world["Ps"][0] / world["Ps"], "site_price_real": house,
                 "price_level": np.exp(pi / 100.0 * t)}
        for i, ti in enumerate(t):
            rows.append({"scenario": name, "t_years": round(float(ti), 4), "policy": round(float(pol[i]), 4),
                         **{lab: round(float(z[i, k]), 4) for k, lab in enumerate(LABELS)}, "wage_bill_real": round(float(wb[i]), 5),
                         **{k: round(float(np.broadcast_to(v, t.shape)[i]), 5) for k, v in extra.items()}})

    for name, (bridges, truth) in bs.SCEN.items():
        old, new, p, _, _ = bs.path(e, bridges, truth)
        pol, z = curves(old, new, p)
        add(name, old["t"], pol, z, new if truth == "new" else old, old, new, p)
    old, new, p, _, _ = bs.path(e, {}, "old")
    t = old["t"]
    pol_t = np.interp(t, [a for a, _ in bs.TIGHTEN], [b for _, b in bs.TIGHTEN])
    zz = bk.expectation_zeros(t, pol_t, maturities=TENORS, known_from=1.0)
    add("a pure tightening", t, pol_t, np.column_stack([zz[f"{T:g}Y"] for T in TENORS]), old, old, new, np.zeros_like(t))
    br = m.Bridges(capital_premium=5.0, **bs.SCEN["deficits dominate"][0])
    old = rc.refine(m.macro_path(e, m.TechPath(eta_end=1.0, lam_end=e.lam), br, 25.0, 0.25), 1 / 12)
    new = rc.refine(m.macro_path(e, m.TechPath(eta_end=0.04, lam_end=0.01, t_mid=6, width=6), br, 25.0, 0.25), 1 / 12)
    lr = rc.Learning(sigma=1.0, p0=0.05, digest=3.0, trust=(5.0, 1.0), capacity_end=30.0)
    p = rc.learn(old, new, lr)
    pol, z = curves(old, new, p)
    add("deficits dominate, slow digestion then AI adoption", old["t"], pol, z, new, old, new, p)
    out = pd.DataFrame(rows)
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    out.to_csv(os.path.join(ROOT, "results", "paths_for_banks.csv"), index=False)
    print(out.groupby("scenario").agg(n=("t_years", "size"), policy_min=("policy", "min"), policy_max=("policy", "max"),
                                       z10_start=("z10Y", "first"), z10_min=("z10Y", "min"), z10_max=("z10Y", "max")))
    print(out[out.t_years.isin([5.0, 10.0, 15.0])].pivot(index="scenario", columns="t_years", values="site_price_real").round(3))


if __name__ == "__main__":
    main()
