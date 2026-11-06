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
# THE SPLIT (her calls, 2026-11-05; --split 1970): people in two groups as the wage data split them, the production and
# nonsupervisory group (whose wage, AHETPI, is the wage the targets read) and managers and supervisors, each working its
# own block of tasks (code/split_model.py). Computing makes machines need comp_t = exp(-g_c max(0, t - 1970)) of their
# service at every task of the first group's block ("routine work all"); g_c is the one new free number. The groups'
# sizes are set, not fitted: managers and supervisors are S_N of the population, their mean share of private employment
# 1964-2024. The targets and the misfit are unchanged, read for the first group's wage; labour's share, employment and θ_V
# take both groups. The pay gap (all employees' average wage over the first group's, 1964 = 1) is a check only.
#
# THE CAP (her idea, 2026-11-05; --cap): prime-age participation has a ceiling: women entered work until both parents
# in most households worked, and then the rate stopped rising, so other things had to move. In the model a share 1 - cap
# of people never works at any wage (pinning_model.CappedEconomy); below the cap, participation follows the wage as before.
# The cap is set, not fitted: the mean prime-age employment rate since it first reached her 0.78 (1987–2024).
#
# THE BASKET (her framing and call, 2026-11-05; --basket): the economy finds ways to give people less land for the same
# utility; as goods cheapen, a basket holds more goods and less site (pinning_model.BasketEconomy: CES at constant
# utility, one unit of goods and h of site at the model's own 1950 price). The elasticity is set, not fitted: one minus
# the slope of the log odds of housing's share of consumer spending on the log of shelter's price over durables', all
# complete years 1950–2024 (SIGMA_SET). The basket's utility moves in straight lines (in logs) between knots, through the
# production worker's real hourly wage over the all-items CPI at each knot, and is held after the last: knots 1950 and
# 1970 (her note: "by most counts it was rising until then": 2.1% a year, then held), or with --utility-knots
# 1950,1970,1990,2024 (her call: "turning around in 1990": falling 1970–1990, rising after).
#
# THE PINNED START (her suggestion, 2026-11-05; --pin-start): the model's 1950 prime-age employment is the data's. The
# work cost's scale chi_max is then set by 1950 each time the path is solved (pinned_chi), not fitted: one free number
# fewer.
#
# MODEL B (her setup, 2026-11-06, from the explorer; STATE.md decision 23). Four changes, each its own switch:
#   --goods exshelter  the goods wage is read over the price of everything but shelter (CPI-U less shelter), not durables
#                      alone: the model has one good, and the consumer's goods are mostly not durables (playground Log 16).
#   --women 1990       women's entry: the work cost's scale falls, straight in logs, from 1950 to the year given and is
#                      held after; its level then (chi_w, a log) is one free number. 1950 is untouched, so the pin holds.
#   --rho 0.02         the required return set, not fitted (her call: about the real long rate's mean).
#   --waves 1948       dated technology waves (her idea, 2026-11-06): on top of the steady clock, each lowers the clock by
#                      size (1 - exp(-(t - year) / tau)) after its year, so fastest at the discovery; size and tau free.
# Two more switches are for the stress tests (code/stress_B.py): --hours-per-task g ties the machine chain's labour to the
# clock (g_lam = g_eta + g: hours per unit of task capacity change at g a year), and FIT_YEARS / DROP limit which years
# and series count in the misfit. configure(meta) sets every switch from a results file, so a stored fit re-solves alone.
#
# Run from us-record/:  python3 code/fit_base.py      (writes results/fit_base.json; about ten minutes)

import json
import os
import sys
import time
from dataclasses import replace
from multiprocessing import Pool

import numpy as np
import pandas as pd
from scipy.optimize import brentq, least_squares
from tqdm.auto import tqdm

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(ROOT)
sys.path.insert(0, os.path.join(REPO, "pinning", "code"))
import pinning_model as pm  # noqa: E402

sys.path.insert(0, os.path.join(ROOT, "code"))
import split_model as sm  # noqa: E402

PANEL = pd.read_csv(os.path.join(ROOT, "data", "panel.csv")).set_index("year")
YEARS = list(range(1950, 2025))                       # every targeted series is complete here (checks/check_panel.py C1)
SERIES = ["wage_goods", "wage_shelter", "labour_share_c", "prime_emp_rate", "theta_V"]
TOL_LOG = {"wage_goods": 0.05, "wage_shelter": 0.05}
TOL_LEVEL = {"labour_share_c": 0.01, "prime_emp_rate": 0.015, "theta_V": 0.02}
SET = dict(b=0.4, g0=0.01, g1=0.99)
SHELTER_LAND_SHARE = None                             # None: shelter as pure site (the base); a share: addition A
SPLIT_FROM = None                                     # None: one kind of worker; a year: the split, computing from it
S_N = float(1.0 - PANEL.loc[1964:2024, "pns_share"].mean())   # the split's managers and supervisors (set)
CAP = None                                            # None: everyone can work (the paper); a share: the cap
_PE = PANEL.loc[1950:2024, "prime_emp_rate"]
CAP_SET = float(_PE.loc[int(_PE[_PE >= 0.78].index[0]):].mean())   # the cap's set value: the mean since her 0.78
SIGMA = None                                          # None: the fixed basket; a number: the basket at constant utility
_HS = PANEL.loc[1950:2024, "housing_share_pce"]
_REL = np.log(PANEL.loc[1950:2024, "wage_goods"] / PANEL.loc[1950:2024, "wage_shelter"])   # shelter's price / durables'
SIGMA_SET = float(1.0 - np.polyfit(_REL.values, np.log(_HS / (1.0 - _HS)).values, 1)[0])   # the share regression
UTILITY_KNOTS = [1950, 1970]                          # the basket's utility: straight (in logs) between these, held after
PIN_START = False                                     # True: chi_max set so that 1950's prime-age employment is the data's
GOODS = "durables"                                    # the goods wage's deflator: durables, or "exshelter" (model B)
WOMEN = None                                          # None: the work cost's scale steady; a year: women's entry until then
RHO_FIXED = None                                      # None: the required return fitted; a number: set
WAVES = []                                            # dated technology waves: their years (each adds a size and a pace)
HOURS_PER_TASK = None                                 # None: g_lam free; a number g: g_lam = g_eta + g (stress tests)
FIT_YEARS = None                                      # None: every year counts; [from, until]: only those (stress tests)
DROP = None                                           # None: every series counts; a list: those left out (stress tests)


def utility_path(knots):
    """The basket's utility each year: through the real wage over the all-items CPI at each knot (1950 = 1), straight in
    logs between knots, held after the last."""
    vals = np.log(PANEL.loc[knots, "real_wage_cpi"].values / PANEL.loc[1950, "real_wage_cpi"])
    return np.exp(np.interp(np.array(YEARS, dtype=float), np.array(knots, dtype=float), vals))
NAMES = ["T", "h", "a", "k", "chi_max", "rho", "g_eta", "lam0", "g_lam"]
LOG = {"T", "h", "a", "k", "chi_max", "lam0"}         # searched in logs (positive)
BOUNDS = dict(T=(1e-5, 10.0), h=(1e-6, 1.0), a=(0.01, 10.0), k=(0.05, 60.0), chi_max=(0.3, 20.0), rho=(0.0, 0.3),
              g_eta=(-0.05, 0.25), lam0=(0.01, 1000.0), g_lam=(-0.1, 0.25), g_c=(0.0, 0.25), chi_w=(-2.0, 2.0))
WAVE_BOUNDS = dict(size=(1e-4, 10.0), tau=(0.5, 80.0))   # each wave's size (in logs of the clock) and pace (years)

D = PANEL.loc[YEARS]
N_T = (D["adults"] / D.loc[1950, "adults"]).values
DELTA = D["delta"].values
T_REL = np.array(YEARS) - 1950.0
WEAK = (D["labour_share_c_tier"] == "WEAK").values
LS_TOL = np.where(WEAK, (D["labour_share_c_hi"] - D["labour_share_c_lo"]).values / 2.0, TOL_LEVEL["labour_share_c"])


def is_log(n):
    return n in LOG or n.startswith("w") and n.endswith(("_size", "_tau"))


def fill(par):
    """The set numbers beside the fitted ones: the return when set, the machine chain's pace when tied to the clock."""
    par = dict(par)
    if RHO_FIXED is not None:
        par["rho"] = RHO_FIXED
    if HOURS_PER_TASK is not None:
        par["g_lam"] = par["g_eta"] + HOURS_PER_TASK
    return par


def unpack(u):
    return fill({n: (float(np.exp(x)) if is_log(n) else float(x)) for n, x in zip(NAMES, u)})


def pack(par):
    return np.array([np.log(par[n]) if is_log(n) else par[n] for n in NAMES])


def bounds(n):
    if n.startswith("w") and n.endswith(("_size", "_tau")):
        return WAVE_BOUNDS[n.split("_")[1]]
    return BOUNDS[n]


def wave_log(par):
    """The waves' part of the clock, in logs: each wave lowers it by size (1 - exp(-(t - year) / tau)) after its year."""
    out = np.zeros(len(YEARS))
    for i, y0 in enumerate(WAVES):
        t = np.array(YEARS, dtype=float) - y0
        out -= np.where(t > 0, par[f"w{i}_size"] * (1.0 - np.exp(-np.maximum(t, 0.0) / par[f"w{i}_tau"])), 0.0)
    return out


def eta_path(par):
    """The capability clock each year: the steady pace and any dated waves."""
    return np.exp(-par["g_eta"] * T_REL + wave_log(par))


def women_path(par):
    """The work cost's scale relative to 1950: with women's entry (WOMEN), straight in logs from 1 in 1950 to exp(chi_w)
    at WOMEN, held after; else 1."""
    if WOMEN is None:
        return np.ones(len(YEARS))
    return np.exp(np.interp(np.array(YEARS, dtype=float), [1950.0, float(WOMEN)], [0.0, par["chi_w"]]))


def economies(par, eta=None, p_ref=None):
    """The economy of every year: the measured inputs and the drivers at par (or a given eta path). With the basket
    (SIGMA) and p_ref (the model's own 1950 price, which model_path solves for first), the basket economy."""
    par = fill(par)
    eta = eta_path(par) if eta is None else eta
    lam = par["lam0"] * np.exp(par["g_lam"] * T_REL)
    chi = par["chi_max"] * women_path(par)
    kind, extra = (pm.Economy, {}) if CAP is None else (pm.CappedEconomy, dict(cap=CAP))
    if SIGMA is not None and p_ref is not None:
        kind, extra = pm.BasketEconomy, dict(cap=1.0 if CAP is None else CAP, sigma=SIGMA, p_ref=p_ref)
        util = utility_path(UTILITY_KNOTS)
        return [kind(N=N_T[i], T=par["T"], h=par["h"], a=par["a"], lam=lam[i], k=par["k"], eta=eta[i],
                     chi_max=float(chi[i]), rho=par["rho"], delta=DELTA[i], **SET, **extra, utility=float(util[i]))
                for i in range(len(YEARS))]
    return [kind(N=N_T[i], T=par["T"], h=par["h"], a=par["a"], lam=lam[i], k=par["k"], eta=eta[i],
                 chi_max=float(chi[i]), rho=par["rho"], delta=DELTA[i], **SET, **extra) for i in range(len(YEARS))]


def pinned_chi(par):
    """The work cost's scale chi_max at which the model's 1950 prime-age employment is the data's (1950's economy is the
    same with or without the basket). None if no chi_max within its bounds does it."""
    e0 = economies(dict(par, chi_max=1.0))[0]
    target = float(D.loc[1950, "prime_emp_rate"])

    def gap(lc):
        try:
            return pm.solve(replace(e0, chi_max=float(np.exp(lc))))["participation"] - target
        except (pm.NoEquilibrium, ValueError, ZeroDivisionError, FloatingPointError):
            return np.nan

    grid = np.linspace(np.log(BOUNDS["chi_max"][0]), np.log(BOUNDS["chi_max"][1]), 25)
    vals = [gap(g) for g in grid]
    for j in range(len(grid) - 1):
        if np.isfinite(vals[j]) and np.isfinite(vals[j + 1]) and vals[j] * vals[j + 1] < 0:
            return float(np.exp(brentq(gap, grid[j], grid[j + 1], xtol=1e-14)))
    return None


def model_path(par, eta=None):
    """Each year's equilibrium, read as the five targeted objects. None if any year has no interior equilibrium."""
    if PIN_START:
        chi = pinned_chi(par)
        if chi is None:
            return None
        par = dict(par, chi_max=chi)
    rows, guess, p_ref = [], None, None
    if SIGMA is not None:                                 # the basket is (1, h) at the model's own 1950 price
        try:
            p_ref = pm.solve(economies(par, eta)[0])["p"]
        except (pm.NoEquilibrium, ValueError, ZeroDivisionError, FloatingPointError):
            return None
    for i, e in enumerate(economies(par, eta, p_ref)):
        try:
            if SPLIT_FROM is None:
                q = pm.solve(e)
            else:                                         # each year solved from the year before's margins
                comp = float(np.exp(-par["g_c"] * max(0.0, YEARS[i] - SPLIT_FROM)))
                q = sm.solve(e, S_N, comp, guess)
                guess = (q["xr"], q["xn"])
        except (pm.NoEquilibrium, ValueError, ZeroDivisionError, FloatingPointError):
            return None
        if SPLIT_FROM is None:
            rows.append(dict(x=q["x"], v=q["v"], p=q["p"], Ps=q["Ps"], wage_goods_raw=q["v"] / q["p"],
                             wage_shelter_raw=q["v"], labour_share_c=q["labour_share_bea"],
                             prime_emp_rate=q["participation"], theta_V=q["theta_V"], gamma=q["gamma"],
                             x_ceiling=q["x_ceiling"]))
            if SIGMA is not None:                         # the basket's make-up, for the figure's checks
                rows[-1].update(goods_basket=q["goods_basket"], site_basket=q["site_basket"],
                                site_share=q["site_basket"] / q["Ps"], utility=e.utility)
        else:                                             # the targets read the first group's wage (AHETPI's)
            rows.append(dict(x=q["xr"], xn=q["xn"], v=q["vr"], vn=q["vn"], p=q["p"], Ps=q["Ps"],
                             wage_goods_raw=q["vr"] / q["p"], wage_shelter_raw=q["vr"],
                             labour_share_c=q["labour_share_bea"], prime_emp_rate=q["participation"],
                             theta_V=q["theta_V"], gamma=q["gr"], comp=comp, pay_gap_raw=q["pay_gap"],
                             routine_share=q["routine_share"]))
    m = pd.DataFrame(rows, index=YEARS)
    if SPLIT_FROM is not None:                            # the checks, read as the data read them
        m["pay_gap"] = m["pay_gap_raw"] / m.loc[1964, "pay_gap_raw"]
    if SHELTER_LAND_SHARE is not None:
        # Addition A: shelter is a built good (priced at p) and site (r = 1) in fixed proportions, the site's value share
        # SHELTER_LAND_SHARE in the last year; earlier years' share then follows the model's own prices.
        w = SHELTER_LAND_SHARE
        m["wage_shelter_raw"] = m["v"] / (w + (1.0 - w) * m["p"] / m["p"].iloc[-1])
    m["wage_goods"] = 100.0 * m["wage_goods_raw"] / m.loc[1950, "wage_goods_raw"]
    m["wage_shelter"] = 100.0 * m["wage_shelter_raw"] / m.loc[1950, "wage_shelter_raw"]
    return m


def target(s):
    """The data a series is read against: the goods wage over durables' price, or (GOODS "exshelter") over the price of
    everything but shelter; the other series as named."""
    return D["wage_exshelter"] if s == "wage_goods" and GOODS == "exshelter" else D[s]


def deviations(m):
    """Each series' scaled deviations (NaN where the data are missing)."""
    out = {}
    for s in SERIES:
        y, f = target(s).values.astype(float), m[s].values
        if s in TOL_LOG:
            out[s] = (np.log(f) - np.log(y)) / TOL_LOG[s]
        elif s == "labour_share_c":
            out[s] = (f - y) / LS_TOL
        else:
            out[s] = (f - y) / TOL_LEVEL[s]
    return out


def counted(s):
    """The years a series counts in the misfit: where it is measured, within FIT_YEARS, unless DROP leaves it out."""
    ok = target(s).notna().values.copy()
    if FIT_YEARS is not None:
        ok &= (np.array(YEARS) >= FIT_YEARS[0]) & (np.array(YEARS) <= FIT_YEARS[1])
    if DROP is not None and s in DROP:
        ok[:] = False
    return ok


def residuals(u):
    """Each counted year's scaled deviation, weighted so that the squares sum to the misfit: the mean over the counted
    series of each one's mean squared scaled deviation."""
    keep = {s: counted(s) for s in SERIES}
    live = [s for s in SERIES if keep[s].any()]
    m = model_path(unpack(u))
    if m is None:
        return np.full(sum(int(keep[s].sum()) for s in live), 10.0)
    dev = deviations(m)
    return np.concatenate([dev[s][keep[s]] / np.sqrt(keep[s].sum() * len(live)) for s in live])


def misfit_by_series(m):
    dev = deviations(m)
    return {s: float(np.nanmean(dev[s] ** 2)) for s in SERIES}


def fit_from(start):
    lo = [np.log(bounds(n)[0]) if is_log(n) else bounds(n)[0] for n in NAMES]
    hi = [np.log(bounds(n)[1]) if is_log(n) else bounds(n)[1] for n in NAMES]
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


def split_starts(ref):
    """The split's starts: the best fit of the model it extends (results/<ref>.json, read by the code, not shown; the
    split with g_c = 0 is that model exactly) and the 1950 starts above (1950 is before computing, so the one-type
    calibration is the split's too): the first with computing's pace 0.01, 0.03 or 0.06 a year, the others with 0.03
    (the fit moves it)."""
    best = json.load(open(os.path.join(ROOT, "results", f"{ref}.json")))["best"]["par"]
    return [dict({n: best[n] for n in NAMES if n != "g_c"}, g_c=g) for g in (0.01, 0.03, 0.06)] + \
        [dict(s, g_c=0.03) for s in starts()]


def complete(s):
    """A start for every free number the settings add: the work cost not yet falling, any wave small and of fifteen
    years' pace."""
    s = dict(s)
    s.setdefault("chi_w", 0.0)
    for i in range(len(WAVES)):
        s.setdefault(f"w{i}_size", 0.05)
        s.setdefault(f"w{i}_tau", 15.0)
    return s


def playground_start(path, key):
    """A start from an explorer or playground fit (its par and settings S, as model.js stores them)."""
    r = json.load(open(os.path.join(ROOT, path)))[key]
    s = dict(r["par"])
    if r["S"].get("chi"):
        s["chi_w"] = float(r["S"]["chi"][-1][1])
    for i, w in enumerate(r["S"].get("waves") or []):
        s[f"w{i}_size"], s[f"w{i}_tau"] = float(w["size"]), float(w["tau"])
    return s


def configure(meta):
    """Every setting from a results file's meta, so that a stored fit re-solves alone (the checks, figures, stress tests
    and report read fits this way)."""
    global SHELTER_LAND_SHARE, SPLIT_FROM, S_N, CAP, SIGMA, PIN_START, UTILITY_KNOTS, GOODS, WOMEN, RHO_FIXED, WAVES
    global HOURS_PER_TASK, FIT_YEARS, DROP
    SHELTER_LAND_SHARE, SPLIT_FROM = meta.get("shelter_land_share"), meta.get("split_from")
    if SPLIT_FROM is not None:
        S_N = meta["s_n"]
    CAP, SIGMA, PIN_START = meta.get("cap"), meta.get("sigma"), bool(meta.get("pin_start"))
    u = meta.get("utility") or {}
    UTILITY_KNOTS = list(u.get("knots", [1950, u["until"]] if "until" in u else [1950, 1970]))  # older: the kink year
    GOODS, WOMEN, RHO_FIXED = meta.get("goods", "durables"), meta.get("women"), meta.get("rho_fixed")
    WAVES, HOURS_PER_TASK = list(meta.get("waves") or []), meta.get("hours_per_task")
    FIT_YEARS, DROP = meta.get("fit_years"), meta.get("drop")
    SET.update(meta.get("set") or {})
    NAMES[:] = meta["names"]


def settings_meta():
    """The settings as configure reads them back."""
    return dict(set=dict(SET), shelter_land_share=SHELTER_LAND_SHARE, split_from=SPLIT_FROM, cap=CAP, sigma=SIGMA,
                utility=None if SIGMA is None else dict(knots=list(UTILITY_KNOTS)), pin_start=PIN_START,
                s_n=None if SPLIT_FROM is None else S_N, goods=GOODS, women=WOMEN, rho_fixed=RHO_FIXED,
                waves=list(WAVES), hours_per_task=HOURS_PER_TASK, fit_years=FIT_YEARS, drop=DROP, names=list(NAMES))


def run_start(s):
    """One start, fitted; continued from where it stopped while it stops at the iteration cap, at most five times (once,
    until the split's start 4 needed more: Log 7)."""
    par, mis, nfev, status = fit_from(s)
    for _ in range(5):
        if status != 0:
            break
        par, mis, more, status = fit_from(par)
        nfev += more
    return dict(start=s, par=par, misfit=mis, nfev=nfev, status=status)


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
    # python3 code/fit_base.py                                   the base model -> results/fit_base.json
    # python3 code/fit_base.py --shelter-land-share 0.4 --out fit_A   addition A -> results/fit_A.json
    # python3 code/fit_base.py --shelter-land-share 0.4 --split 1970 --ref fit_A --out fit_split --quiet
    #                                                             the split on top of A -> results/fit_split.json
    # python3 code/fit_base.py --shelter-land-share 0.4 --cap --ref fit_A --out fit_cap --quiet
    #                                                             the cap on top of A -> results/fit_cap.json
    # python3 code/fit_base.py --shelter-land-share 0.4 --cap --basket --ref fit_cap --out fit_basket --quiet
    #                                                             the basket on top of A and the cap
    # add --pin-start for 1950's prime-age employment pinned to the data; leave out --shelter-land-share for no A
    # python3 code/fit_base.py --basket --utility-knots 1950,1970,1990,2024 --pin-start --goods exshelter --women 1990 \
    #     --rho 0.02 --start-from playground/newmodel.json --start-key "her setup: ..." --out fit_B      model B
    # ... --waves 1948 --out fit_Bw                                                         model B and the post-war wave
    args = sys.argv[1:]
    OUT = args[args.index("--out") + 1] if "--out" in args else "fit_base"
    REF = args[args.index("--ref") + 1] if "--ref" in args else None
    if "--shelter-land-share" in args:
        SHELTER_LAND_SHARE = float(args[args.index("--shelter-land-share") + 1])
    if "--split" in args:
        SPLIT_FROM = int(args[args.index("--split") + 1])
        NAMES.append("g_c")
    if "--cap" in args:
        CAP = CAP_SET
    if "--basket" in args:
        SIGMA = SIGMA_SET
    if "--utility-knots" in args:
        UTILITY_KNOTS = [int(y) for y in args[args.index("--utility-knots") + 1].split(",")]
    if "--pin-start" in args:
        PIN_START = True
        NAMES.remove("chi_max")
    if "--goods" in args:
        GOODS = args[args.index("--goods") + 1]
    if "--women" in args:
        WOMEN = int(args[args.index("--women") + 1])
        NAMES.append("chi_w")
    if "--rho" in args:
        RHO_FIXED = float(args[args.index("--rho") + 1])
        NAMES.remove("rho")
    if "--waves" in args:
        WAVES = [int(y) for y in args[args.index("--waves") + 1].split(",")]
        NAMES.extend(n for i in range(len(WAVES)) for n in (f"w{i}_size", f"w{i}_tau"))
    if "--hours-per-task" in args:
        HOURS_PER_TASK = float(args[args.index("--hours-per-task") + 1])
        NAMES.remove("g_lam")
    t0 = time.time()
    todo = starts() if SPLIT_FROM is None else split_starts(REF)
    if SPLIT_FROM is None and REF is not None:            # the model it extends: its best fit is one more start
        ref_best = json.load(open(os.path.join(ROOT, "results", f"{REF}.json")))["best"]["par"]
        todo = [{n: ref_best[n] for n in NAMES if n in ref_best}] + todo
    if "--start-from" in args:                            # a fit found in the explorer or playground: one more start
        todo = [playground_start(args[args.index("--start-from") + 1], args[args.index("--start-key") + 1])] + todo
    todo = [complete(s) for s in todo]
    with Pool(min(4, os.cpu_count() or 1)) as pool:        # the starts in parallel; each is deterministic
        results = list(tqdm(pool.imap(run_start, todo), total=len(todo), desc="starts"))
    results.sort(key=lambda r: r["misfit"])
    best = results[0]
    m = model_path(best["par"])
    plain = SHELTER_LAND_SHARE is None and SPLIT_FROM is None and CAP is None and SIGMA is None and not PIN_START \
        and GOODS == "durables" and WOMEN is None and RHO_FIXED is None and not WAVES and HOURS_PER_TASK is None
    acc = accounting(best["par"]) if plain else None      # the diagnostic reads the base model only
    if PIN_START:                                         # the set chi_max stored beside the fitted numbers
        for r in results:
            r["par"]["chi_max"] = pinned_chi(r["par"])
    out = dict(
        meta=dict(years=[YEARS[0], YEARS[-1]], series=SERIES, tol_log=TOL_LOG, tol_level=TOL_LEVEL, **settings_meta(),
                  ref=REF, bounds=BOUNDS, n_obs={s: int(counted(s).sum()) for s in SERIES},
                  seconds=round(time.time() - t0, 1)),
        best=dict(par=best["par"], misfit=best["misfit"], by_series=misfit_by_series(m)),
        starts=[dict(start=r["start"], par=r["par"], misfit=r["misfit"], nfev=r["nfev"], status=r["status"])
                for r in results],
        path={c: [None if not np.isfinite(v) else float(v) for v in m[c].values] for c in m.columns},
        accounting_eta=None if acc is None else [None if not np.isfinite(v) else float(v) for v in acc.values],
        fitted_eta=[float(v) for v in eta_path(best["par"])])
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    with open(os.path.join(ROOT, "results", f"{OUT}.json"), "w") as f:
        json.dump(out, f, indent=1)
    if "--quiet" in args:                                # the blind protocol (decision 13): no fit numbers on screen
        print(f"results/{OUT}.json written")
        sys.exit(0)
    print(f"best misfit {best['misfit']:.3f}; by series", {k: round(v, 2) for k, v in out["best"]["by_series"].items()})
    print("parameters", {k: round(v, 5) for k, v in best["par"].items()})
    for r in results:
        print(f"  start k {r['start']['k']:<7.3f} g_eta {r['start']['g_eta']:<5} -> misfit {r['misfit']:9.3f}  "
              f"k {r['par']['k']:.3f}  g_eta {r['par']['g_eta']:.4f}  nfev {r['nfev']}")
