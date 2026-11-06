# misses.py — her question (2026-11-06): how bad are the main case's misses? Is there an easy extension, are the data not
# fit for purpose, or do they kill the fit? Quick refits of the main case (results/fit_Bw.json, B with the 1948 wave)
# with one set value walked, and the readings each miss is judged on. Writes playground/misses.json.
# Run from us-record/:  python3 playground/misses.py
import json
import os
import sys

import numpy as np
from tqdm.auto import tqdm

sys.path.insert(0, "code")
import fit_base as F  # noqa: E402
import report_B as RB  # noqa: E402

R = json.load(open("results/fit_Bw.json"))
F.configure(R["meta"])
META = dict(R["meta"])
i = F.YEARS.index


def readings(par):
    """The misfit and what each miss is judged on, at a fit's numbers."""
    p2, p_ref = RB.setup(par)
    d = RB.insides(RB.solve_all(F.economies(p2, p_ref=p_ref)))
    by = F.misfit_by_series(F.model_path(par))
    return dict(misfit=float(np.mean(list(by.values()))), by=by, rho=p2["rho"], a=p2["a"], g_eta=p2["g_eta"],
                g_lam=p2["g_lam"], sigma=F.SIGMA,
                chain_2023=float(d["chain_share"][i(2023)]), cfc_gross_2023=float(d["cfc_gross"][i(2023)]),
                kappa_V=float(d["kappa_V"][i(2023)]), theta_V=float(d["theta_V"][i(2023)]),
                sigma_V=float(d["sigma_V"][i(2023)]), gap_2023=float(d["x_ceiling"][i(2023)] - d["x"][i(2023)]),
                x_2024=float(d["x"][i(2024)]), waterline_2023=float(d["waterline"][i(2023)]),
                coverage_homes_2024=float(d["coverage_homes_idx"][i(2024)]),
                site_share_1950=float(d["site_share"].iloc[0]), site_share_2024=float(d["site_share"].iloc[-1]),
                inc_interest_2023=float(d["inc_interest"][i(2023)]), inc_land_2023=float(d["inc_land"][i(2023)]),
                capital_income_2023=float(d["capital_income"][i(2023)]))


def fit_at(meta, par):
    """Refit at meta from par; None if the fit finds no equilibrium path there."""
    F.configure(meta)
    r = F.run_start(F.complete(par))
    chi = F.pinned_chi(r["par"]) if r["misfit"] < 10.0 else None
    return None if chi is None else dict(r["par"], chi_max=chi)


def walk(key, targets, par, meta0=None, step=0.0025):
    """A set value walked to each target in small steps (halved where a step loses the equilibrium), refitting at
    every step; each target's fit recorded."""
    out, meta = [], dict(meta0 or META)
    cur = meta[key] if meta.get(key) is not None else (par.get("rho", 0.02) if key == "rho_fixed" else F.SIGMA)
    for tgt in tqdm(targets, leave=False):
        while abs(cur - tgt) > 1e-12:
            h = step
            while True:
                nxt = cur + np.sign(tgt - cur) * min(h, abs(tgt - cur))
                start = dict(par)
                if key == "rho_fixed":           # keep 1950's machine-cost shares: a and lam0 scale with 1/(rho + delta)
                    f = (cur + F.DELTA[0]) / (nxt + F.DELTA[0])
                    start.update(a=par["a"] * f, lam0=par["lam0"] * f)
                got = fit_at(dict(meta, **{key: float(nxt)}), start)
                if got is not None:
                    par, cur, meta = got, float(nxt), dict(meta, **{key: float(nxt)})
                    break
                h /= 2
                if h < step / 16:
                    F.configure(META)
                    print(f"  stopped: no equilibrium path beyond {key} = {cur:.4f}")
                    return out
        F.configure(meta)
        out.append(dict(change={key: tgt}, par=par, **readings(par)))
    F.configure(META)
    return out


def show(label, rows):
    print(label)
    for r in rows:
        print(f"  {json.dumps(r['change']):36s} misfit {r['misfit']:6.3f} | " + " ".join(f"{v:5.2f}" for v in r["by"].values())
              + f" | a {r['a']:.2f} clock {100 * r['g_eta']:.1f}% chain {r['chain_2023']:.3f} cfc/gross {r['cfc_gross_2023']:.3f}"
              f" kV {r['kappa_V']:.3f} tV {r['theta_V']:.3f} sV {r['sigma_V']:.4f} gap {r['gap_2023']:.4f}"
              f" water {r['waterline_2023']:.2f} cov {r['coverage_homes_2024']:.2f} site {r['site_share_1950']:.3f}->{r['site_share_2024']:.3f}")


out = json.load(open("playground/misses.json"))
out["rho"] = walk("rho_fixed", [0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.12], R["best"]["par"], step=0.005)
show("the required return walked up", out["rho"])
json.dump(out, open("playground/misses.json", "w"), indent=1)
if out["rho"]:
    best = min(out["rho"], key=lambda r: abs(r["chain_2023"] - 0.18))
    out["both"] = walk("sigma", [0.75, 0.636], best["par"], meta0=dict(META, rho_fixed=best["rho"]), step=0.025)
    show(f"both: the return at {best['rho']:.3f} and the elasticity walked", out["both"])
json.dump(out, open("playground/misses.json", "w"), indent=1)
