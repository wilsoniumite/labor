# fit_base.py — Phase 2 (SPEC.md section 8): the base model fitted to the US record, 1950–2024.
#
# THE MODEL. The pinning model (../pinning/code/pinning_model.py), unchanged, solved each year. Measured inputs, not
# fitted: adults N_t (indexed to 1950) and depreciation delta_t. Two smooth drivers: the capability clock
# eta_t = exp(-g_eta (t - 1950)) (machines need eta_t of their 1950 service units at every task) and the machine chain's
# labour lambda_t = lam0 exp(g_lam (t - 1950)), fitted to the measured θ_V where it exists. Fixed once over the whole
# record: T, h, a, k, chi_max and the required return rho. Set, as in the paper's instance and calibration (c): b 0.4
# (the land unit), g0 0.01, g1 0.99. Nine free numbers.
# The required return is CONSTANT (decision 11, after the first search, for her veto at breakpoint B): with machines
# carrying about half their cost in labour, the model has a few points of rate headroom, and a required return that
# follows the measured real long rate (-3% in 1950, +6% in the 1980s) leaves no land-scarce equilibrium in many years;
# the measured return on business capital is far steadier than bond yields. The measured rate's pass-through is a
# candidate addition (Phase 3), under the same rule as every other.
#
# THE TARGETS AND THE MISFIT (SPEC.md sections 4 and 6), set before the first fit (committed before it ran):
#   wage_goods      v/p, indexed to 1950          log deviation over 0.05
#   wage_shelter    v (shelter as pure site), indexed to 1950   log deviation over 0.05   (addition A is Phase 3's)
#   labour_share_c  v (1 - x) / P_s               level deviation over the band's half-width in WEAK years, 0.01 in
#                                                 STRONG years
#   prime_emp_rate  N_a / N                       level deviation over 0.015
#   theta_V         lambda gamma(x*) (rho + delta), where measured (33 years)   level deviation over 0.02
# The misfit is the mean over the five series of each series' mean squared scaled deviation, so each series weighs the
# same whatever its number of years. 1.0 means the model sits, on average, one tolerance from every series.
#
# THE SEARCH. Bounded least squares from a grid of starts spanning the schedule's convexity k (low and high roots, as in
# calibrate_c) and the clock's pace; the best fit is reported with every start's result. Then, as a diagnostic only
# (SPEC.md section 8), year-by-year accounting: the capability eta_t that would reproduce the fork exactly in each year,
# everything else at the fit, against the fitted clock.
#
# Run from us-record/:  python3 code/fit_base.py      (writes results/fit_base.json; about ten minutes)

import json
import os
import sys
import time
from dataclasses import replace

import numpy as np
import pandas as pd
from scipy.optimize import brentq, least_squares
from tqdm.auto import tqdm

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(ROOT)
sys.path.insert(0, os.path.join(REPO, "pinning", "code"))
import pinning_model as pm  # noqa: E402

PANEL = pd.read_csv(os.path.join(ROOT, "data", "panel.csv")).set_index("year")
YEARS = list(range(1950, 2025))                       # every targeted series is complete here (checks/check_panel.py C1)
SERIES = ["wage_goods", "wage_shelter", "labour_share_c", "prime_emp_rate", "theta_V"]
TOL_LOG = {"wage_goods": 0.05, "wage_shelter": 0.05}
TOL_LEVEL = {"labour_share_c": 0.01, "prime_emp_rate": 0.015, "theta_V": 0.02}
SET = dict(b=0.4, g0=0.01, g1=0.99)
NAMES = ["T", "h", "a", "k", "chi_max", "rho", "g_eta", "lam0", "g_lam"]
LOG = {"T", "h", "a", "k", "chi_max", "lam0"}         # searched in logs (positive)
BOUNDS = dict(T=(1e-5, 10.0), h=(1e-6, 1.0), a=(0.01, 10.0), k=(0.05, 60.0), chi_max=(0.3, 20.0), rho=(0.0, 0.3),
              g_eta=(-0.05, 0.25), lam0=(0.01, 1000.0), g_lam=(-0.1, 0.1))

D = PANEL.loc[YEARS]
N_T = (D["adults"] / D.loc[1950, "adults"]).values
DELTA = D["delta"].values
T_REL = np.array(YEARS) - 1950.0
WEAK = (D["labour_share_c_tier"] == "WEAK").values
LS_TOL = np.where(WEAK, (D["labour_share_c_hi"] - D["labour_share_c_lo"]).values / 2.0, TOL_LEVEL["labour_share_c"])


def unpack(u):
    return {n: (float(np.exp(x)) if n in LOG else float(x)) for n, x in zip(NAMES, u)}


def pack(par):
    return np.array([np.log(par[n]) if n in LOG else par[n] for n in NAMES])


def economies(par, eta=None):
    """The economy of every year: the measured inputs and the two drivers at par (or a given eta path)."""
    eta = np.exp(-par["g_eta"] * T_REL) if eta is None else eta
    lam = par["lam0"] * np.exp(par["g_lam"] * T_REL)
    return [pm.Economy(N=N_T[i], T=par["T"], h=par["h"], a=par["a"], lam=lam[i], k=par["k"], eta=eta[i],
                       chi_max=par["chi_max"], rho=par["rho"], delta=DELTA[i], **SET) for i in range(len(YEARS))]


def model_path(par, eta=None):
    """Each year's equilibrium, read as the five targeted objects. None if any year has no interior equilibrium."""
    rows = []
    for e in economies(par, eta):
        try:
            q = pm.solve(e)
        except (pm.NoEquilibrium, ValueError, ZeroDivisionError, FloatingPointError):
            return None
        rows.append(dict(x=q["x"], v=q["v"], p=q["p"], Ps=q["Ps"], wage_goods_raw=q["v"] / q["p"], wage_shelter_raw=q["v"],
                         labour_share_c=q["labour_share_bea"], prime_emp_rate=q["participation"], theta_V=q["theta_V"],
                         gamma=q["gamma"], x_ceiling=q["x_ceiling"]))
    m = pd.DataFrame(rows, index=YEARS)
    m["wage_goods"] = 100.0 * m["wage_goods_raw"] / m.loc[1950, "wage_goods_raw"]
    m["wage_shelter"] = 100.0 * m["wage_shelter_raw"] / m.loc[1950, "wage_shelter_raw"]
    return m


def deviations(m):
    """Each series' scaled deviations (NaN where the data are missing)."""
    out = {}
    for s in SERIES:
        y, f = D[s].values.astype(float), m[s].values
        if s in TOL_LOG:
            out[s] = (np.log(f) - np.log(y)) / TOL_LOG[s]
        elif s == "labour_share_c":
            out[s] = (f - y) / LS_TOL
        else:
            out[s] = (f - y) / TOL_LEVEL[s]
    return out


N_OBS = {s: int(D[s].notna().sum()) for s in SERIES}
N_RES = sum(N_OBS.values())


def residuals(u):
    m = model_path(unpack(u))
    if m is None:
        return np.full(N_RES, 10.0)
    dev = deviations(m)
    return np.concatenate([dev[s][~np.isnan(dev[s])] / np.sqrt(N_OBS[s] * len(SERIES)) for s in SERIES])


def misfit_by_series(m):
    dev = deviations(m)
    return {s: float(np.nanmean(dev[s] ** 2)) for s in SERIES}


def fit_from(start):
    lo = [np.log(BOUNDS[n][0]) if n in LOG else BOUNDS[n][0] for n in NAMES]
    hi = [np.log(BOUNDS[n][1]) if n in LOG else BOUNDS[n][1] for n in NAMES]
    u0 = np.clip(pack(start), np.array(lo) + 1e-9, np.array(hi) - 1e-9)
    r = least_squares(residuals, u0, bounds=(lo, hi), x_scale=1.0, max_nfev=3000, ftol=1e-10, xtol=1e-10)
    return unpack(r.x), float(np.sum(r.fun ** 2)), int(r.nfev), r.status


def starts():
    """1950 calibrated in closed form (pinning_model.calibrate_c) at its measured labour share and prime-age employment,
    across what 1950 does not measure (baskets a person 1.0 or 1.5; the site 0.03 or 0.06 of the basket; θ_V 0.5, about
    1967's; machine services 0.2 of a machine's cost), both roots in k; then the clock's pace 0.02 or 0.04 a year. Starts
    only: the fit moves every number. (The first search, from the paper's 2020s-like instance placed in 1950 with
    x_scale 'jac', stopped after two iterations at the bounds: Log 3.)"""
    d0 = D.loc[1950]
    out = []
    for baskets in (1.0, 1.5):
        for site in (0.03, 0.06):
            tg = pm.ChainTargets(theta_V=0.50, chain_share=0.15, sigma_V=0.30, delta=float(d0["delta"]),
                                 labour=float(d0["labour_share_c"]), participation=float(d0["prime_emp_rate"]),
                                 baskets_per_person=baskets, site=site, b=SET["b"], g0=SET["g0"], N=1.0)
            try:
                roots = pm.calibrate_c(tg)
            except ValueError:
                continue
            for e, _ in roots:
                for g in (0.02, 0.04):
                    out.append(dict(T=e.T, h=e.h, a=e.a, k=e.k, chi_max=e.chi_max, rho=e.rho, lam0=e.lam, g_lam=0.0,
                                    g_eta=g))
    return out


def accounting(par):
    """Diagnostic only: in each year, the capability eta_t that reproduces the fork (wage_goods / wage_shelter, i.e.
    p_1950 / p_t) exactly, everything else at the fit and 1950 at the fitted clock's value (1)."""
    base = model_path(par)
    fork_data = (D["wage_goods"] / D["wage_shelter"]).values
    p1950 = base.loc[1950, "p"]
    out = []
    for i, e in enumerate(economies(par)):
        target = fork_data[i]                          # the fork, 1950 = 1 (both legs indexed to 100)

        def gap(log_eta):
            ee = replace(e, eta=float(np.exp(log_eta)))
            try:
                q = pm.solve(ee)
            except (pm.NoEquilibrium, ValueError):
                return np.nan
            return np.log(p1950 / q["p"]) - np.log(target)

        grid = np.linspace(-8.0, 3.0, 45)
        vals = [gap(g) for g in grid]
        root = np.nan
        for j in range(len(grid) - 1):
            if np.isfinite(vals[j]) and np.isfinite(vals[j + 1]) and vals[j] * vals[j + 1] < 0:
                root = float(np.exp(brentq(gap, grid[j], grid[j + 1], xtol=1e-12)))
                break
        out.append(root)
    return pd.Series(out, index=YEARS)


if __name__ == "__main__":
    t0 = time.time()
    results = []
    for s in tqdm(starts(), desc="starts"):
        par, mis, nfev, status = fit_from(s)
        results.append(dict(start=s, par=par, misfit=mis, nfev=nfev, status=status))
    results.sort(key=lambda r: r["misfit"])
    best = results[0]
    m = model_path(best["par"])
    acc = accounting(best["par"])
    out = dict(
        meta=dict(years=[YEARS[0], YEARS[-1]], series=SERIES, tol_log=TOL_LOG, tol_level=TOL_LEVEL, set=SET,
                  names=NAMES, bounds=BOUNDS, n_obs=N_OBS, seconds=round(time.time() - t0, 1)),
        best=dict(par=best["par"], misfit=best["misfit"], by_series=misfit_by_series(m)),
        starts=[dict(start=r["start"], par=r["par"], misfit=r["misfit"], nfev=r["nfev"], status=r["status"])
                for r in results],
        path={c: [None if not np.isfinite(v) else float(v) for v in m[c].values] for c in m.columns},
        accounting_eta=[None if not np.isfinite(v) else float(v) for v in acc.values],
        fitted_eta=[float(v) for v in np.exp(-best["par"]["g_eta"] * T_REL)])
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    with open(os.path.join(ROOT, "results", "fit_base.json"), "w") as f:
        json.dump(out, f, indent=1)
    print(f"best misfit {best['misfit']:.3f}; by series", {k: round(v, 2) for k, v in out["best"]["by_series"].items()})
    print("parameters", {k: round(v, 5) for k, v in best["par"].items()})
    for r in results:
        print(f"  start k {r['start']['k']:<7.3f} g_eta {r['start']['g_eta']:<5} -> misfit {r['misfit']:9.3f}  "
              f"k {r['par']['k']:.3f}  g_eta {r['par']['g_eta']:.4f}  nfev {r['nfev']}")
