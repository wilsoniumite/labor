# report_B.py — everything the report on model B shows (report/index.html), computed from the stored fits and the panel:
#   fit        the five targeted series, model against record, with each year's scaled deviation
#   checks     facts the fit never saw: housing's share of spending, the waterline (the wage against machine cost,
#              1999-2023), the coverage ratio (site rent against a fixed-utility basket for everyone), the nonfarm labour
#              share, the 16+ employment rate, the wage over durables (the old goods target) and over all items
#   insides    the task line, the machine's cost, land, hours, the basket, labour's share taken apart, the two real
#              clocks, prices, work and its cost
#   drivers    one driver held at its 1950 value at a time, everything else as fitted: what each did to the record
#   ahead      the fitted drivers carried on to 2050, two ways (the utility held, as B holds it, or rising as 1990-2024),
#              and with the clocks stopped in 2025
#   stress     results/stress_B.json (code/stress_B.py), read as it is
# For model B (results/fit_B.json) and B with the post-war wave (results/fit_Bw.json).
# Run from us-record/:  python3 code/report_B.py      (writes report/report_B.json and, from report/page.html, the page
# report/index.html with the numbers inlined; under a minute)

import json
import os
import sys
from dataclasses import replace

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "code"))
import fit_base as F  # noqa: E402

pm = F.pm
YEARS = F.YEARS
AHEAD = list(range(2025, 2051))


def num(x):
    return None if x is None or not np.isfinite(x) else round(float(x), 7)


def nums(xs):
    return [num(x) for x in xs]


def load(name):
    R = json.load(open(os.path.join(ROOT, "results", f"{name}.json")))
    F.configure(R["meta"])
    return R


def setup(par):
    """The fit's numbers with the set ones filled, the pinned work cost's scale, and the model's own 1950 price."""
    par = F.fill(par)
    if F.PIN_START:
        par = dict(par, chi_max=F.pinned_chi(par))
    p_ref = pm.solve(F.economies(par)[0])["p"] if F.SIGMA is not None else None
    return par, p_ref


def solve_all(es):
    """Each economy solved; NaN where it has no equilibrium (counterfactuals and the years ahead may leave it)."""
    rows = []
    for e in es:
        try:
            q = pm.solve(e)
        except (pm.NoEquilibrium, ValueError, ZeroDivisionError, FloatingPointError):
            rows.append(None)
            continue
        q = {k: v for k, v in q.items() if np.isscalar(v)}
        q.update(eta=e.eta, lam=e.lam, chi=e.chi_max, N=e.N, delta=e.delta, utility=getattr(e, "utility", 1.0),
                 z=float(np.log1p(q["v"] / q["Ps"])), T=e.T, b=e.b, rho=e.rho)
        rows.append(q)
    keys = next(r for r in rows if r is not None).keys()
    return pd.DataFrame([r if r is not None else {k: np.nan for k in keys} for r in rows])


def insides(q):
    """The model's insides, read from each year's equilibrium (q: solve_all's frame, one row a year)."""
    i0 = 0
    d = {}
    d["x"], d["x_ceiling"] = q["x"], q["x_ceiling"]
    d["wage_goods"] = 100 * (q["v"] / q["p"]) / (q["v"] / q["p"]).iloc[i0]
    d["wage_shelter"] = 100 * q["v"] / q["v"].iloc[i0]
    col = q["Ps"] / q["utility"]                              # the cost of a basket of 1950's utility, in site units
    d["wage_living"] = 100 * (q["v"] / col) / (q["v"] / col).iloc[i0]
    d["labour_share_c"], d["prime_emp_rate"], d["theta_V"] = q["labour_share_bea"], q["participation"], q["theta_V"]
    d["kappa_V"], d["sigma_V"] = q["kappa_V"], q["sigma_V"]
    d["goods_basket"] = q["goods_basket"] / q["goods_basket"].iloc[i0]
    d["site_basket"] = q["site_basket"] / q["site_basket"].iloc[i0]
    d["site_share"] = q["site_basket"] / q["Ps"]
    d["goods_share"] = q["p"] * q["goods_basket"] / q["Ps"]
    d["ls_wage_goods"] = (q["v"] / q["p"]) / (q["v"] / q["p"]).iloc[i0]
    d["ls_people"] = (1 - q["x"]) / (1 - q["x"]).iloc[i0]
    d["ls_goods_share"] = d["goods_share"] / d["goods_share"].iloc[i0]
    d["land_homes"] = q["site_basket"] * q["baskets"] / q["T"]
    d["land_machines"] = q["b"] * q["delta"] * q["K"] / q["T"]
    d["chain_share"] = q["chain_share"]
    d["inc_labour"] = q["v"] * q["n"] / q["income"]
    d["inc_land"] = q["T"] / q["income"]
    d["inc_interest"] = q["rho"] * q["Vm"] * q["K"] / q["income"]
    d["capital_income"] = q["Vm"] * q["K"] / q["income"]
    d["inv_income"] = q["inv_income"]
    d["cfc_gross"] = q["inv_income"] / (1.0 + q["inv_income"])   # replacement over gross output (income + depreciation)
    d["land_per_task"] = q["b"] * q["eta"] / (q["b"] * q["eta"]).iloc[i0]
    d["hours_per_task"] = q["lam"] * q["eta"] / (q["lam"] * q["eta"]).iloc[i0]
    d["eta"], d["lam"] = q["eta"], q["lam"] / q["lam"].iloc[i0]
    d["gamma_margin"] = q["gamma"]
    i99 = YEARS.index(1999)                                     # the wage over the price of a unit of machine capability
    d["waterline"] = (q["gamma"] / q["eta"]) / (q["gamma"] / q["eta"]).iloc[i99]
    d["p"], d["Ps"], d["v"] = q["p"] / q["p"].iloc[i0], q["Ps"] / q["Ps"].iloc[i0], q["v"] / q["v"].iloc[i0]
    d["z"], d["chi"] = q["z"], q["chi"] / q["chi"].iloc[i0]
    d["utility"] = q["utility"]
    d["people"] = q["n"] / q["N"]
    d["baskets_pp"] = (q["baskets"] / q["N"]) / (q["baskets"] / q["N"]).iloc[i0]
    d["coverage"] = q["T"] / (q["N"] * col)                     # site rent against a fixed-utility basket for everyone
    d["coverage_idx"] = d["coverage"] / d["coverage"].iloc[3]   # 1953 = 1, where the record starts
    # the record's coverage counts housing land (rent flows times a land share; Z.1 household land): the model's twin is
    # the site in baskets, not all land (machines held most of the land in 1950)
    d["coverage_homes"] = q["site_basket"] * q["baskets"] / (q["N"] * col)
    d["coverage_homes_idx"] = d["coverage_homes"] / d["coverage_homes"].iloc[3]
    return d


def counterfactual(par, p_ref, **hold):
    """One or more drivers held at their 1950 values, everything else as fitted; NaN where no equilibrium."""
    keep = dict(N_T=F.N_T, DELTA=F.DELTA, UTILITY_KNOTS=F.UTILITY_KNOTS)
    p2 = dict(par)
    eta = None
    if hold.get("clock"):
        eta = np.ones(len(YEARS))
    if hold.get("chain"):
        p2["g_lam"] = 0.0
    if hold.get("people"):
        F.N_T = np.ones(len(YEARS))
    if hold.get("depreciation"):
        F.DELTA = np.full(len(YEARS), F.DELTA[0])
    if hold.get("utility"):
        F.UTILITY_KNOTS = [1950]
    if hold.get("women") and F.WOMEN:
        p2["chi_w"] = 0.0
    try:
        q = solve_all(F.economies(p2, eta=eta, p_ref=p_ref))
    finally:
        F.N_T, F.DELTA, F.UTILITY_KNOTS = keep["N_T"], keep["DELTA"], keep["UTILITY_KNOTS"]
    return insides(q)


def ahead(par, p_ref, utility="held", clocks="on"):
    """The fitted drivers carried on, 2025-2050: the clock and the chain's labour at their paces (or stopped at 2024),
    adults growing at their 2014-2024 pace, depreciation at its 2015-2024 mean, the work cost as in 2024, the utility
    held at 2024 (B's own rule after its last knot) or rising at its 1990-2024 pace."""
    years = YEARS + AHEAD
    t = np.array(years, dtype=float) - 1950.0
    g_n = np.log(F.N_T[-1] / F.N_T[-11]) / 10.0
    N = np.r_[F.N_T, F.N_T[-1] * np.exp(g_n * (np.array(AHEAD) - 2024.0))]
    delta = np.r_[F.DELTA, np.full(len(AHEAD), F.DELTA[-10:].mean())]
    eta = np.exp(-par["g_eta"] * t + np.r_[F.wave_log(par), np.full(len(AHEAD), F.wave_log(par)[-1])])
    lam = par["lam0"] * np.exp(par["g_lam"] * t)
    if clocks == "stopped":
        eta[len(YEARS):], lam[len(YEARS):] = eta[len(YEARS) - 1], lam[len(YEARS) - 1]
    chi = par["chi_max"] * np.r_[F.women_path(par), np.full(len(AHEAD), F.women_path(par)[-1])]
    u_hist = F.utility_path(F.UTILITY_KNOTS)
    g_u = np.log(u_hist[-1] / u_hist[YEARS.index(1990)]) / (2024 - 1990)
    u = np.r_[u_hist, u_hist[-1] * np.exp((g_u if utility == "rising" else 0.0) * (np.array(AHEAD) - 2024.0))]
    es = [pm.BasketEconomy(N=float(N[i]), T=par["T"], h=par["h"], a=par["a"], lam=float(lam[i]), k=par["k"],
                           eta=float(eta[i]), chi_max=float(chi[i]), rho=par["rho"], delta=float(delta[i]), **F.SET,
                           cap=1.0 if F.CAP is None else F.CAP, sigma=F.SIGMA, p_ref=p_ref, utility=float(u[i]))
          for i in range(len(years))]
    q = solve_all(es)
    return insides(q), dict(g_n=g_n, delta=float(delta[-1]), g_u=g_u)


def record():
    """The record: targets and the facts the fit never saw."""
    D = F.D
    out = {s: nums(F.target(s).values) for s in F.SERIES}
    out["wage_durables"] = nums(D["wage_goods"].values)
    out["wage_exshelter"] = nums(D["wage_exshelter"].values)
    out["ls_lo"], out["ls_hi"] = nums(D["labour_share_c_lo"].values), nums(D["labour_share_c_hi"].values)
    out["ls_tol"] = nums(F.LS_TOL)
    out["weak"] = [bool(x) for x in F.WEAK]
    out["real_wage_cpi"] = nums(100 * D["real_wage_cpi"] / D.loc[1950, "real_wage_cpi"])
    out["housing_share_pce"] = nums(D["housing_share_pce"].values)
    wc = D["wc_median"]
    out["waterline"] = nums(wc.values)
    k = D["kappa_med"]
    out["kappa_med"], out["kappa_lo"], out["kappa_hi"] = nums(k.values), nums(D["kappa_min"].values), nums(D["kappa_max"].values)
    out["kappa_idx"] = nums((k / k.loc[1953]).values)
    nfb = D["nfb_labour_share"]
    out["nfb_labour_share"] = nums((nfb / nfb.loc[1950]).values)
    out["emp_rate"] = nums(D["emp_rate"].values / 100.0 if D["emp_rate"].max() > 1.5 else D["emp_rate"].values)
    out["adults"] = nums(F.N_T)
    out["delta"] = nums(F.DELTA)
    out["utility_knots_real_wage"] = nums(D["real_wage_cpi"] / D.loc[1950, "real_wage_cpi"])
    # the machine chain as the BEA input-output accounts measure it (../paths/results/chains.json, 1997-2023): the chain's
    # share of all compensation (the model's chain_share: one wage, so hours and pay shares agree), its labour share of
    # cost, and the 2023 cost split of the bundle calibration (c) reads (equipment, IPP and private structures)
    ch = json.load(open(os.path.join(F.REPO, "paths", "results", "chains.json")))
    eco = ch["economy"]
    key = "inv_equipment_ipp_structures_comp_{}_share_of_total_comp"
    out["chain_share_tot"] = [num(eco[str(y)][key.format("tot")]) if str(y) in eco else None for y in YEARS]
    out["chain_share_domp"] = [num(eco[str(y)][key.format("domp")]) if str(y) in eco else None for y in YEARS]
    g1 = ch["targets_for_macro"]["g1_equipment_ipp_structures_full_chain"]
    out["cost_split_2023"] = {b: {k: g1[f"{k}_{b}"]["2023"] for k in ("theta", "cfc", "tax", "nos", "imports")}
                              for b in ("tot", "domp")}
    out["cfc_over_gdp_2023"] = ch["targets_for_macro"]["c_nipa"]["cfc_over_gdp"]["2023"]
    out["chain_hours_bridged_2023"] = {b: g1[f"hours_share_of_total_hours_bridged_{b}"]["2023"] for b in ("tot", "domp")}
    return out


def model_block(name):
    R = load(name)
    par, p_ref = setup(R["best"]["par"])
    q = solve_all(F.economies(par, p_ref=p_ref))
    d = insides(q)
    m = F.model_path(par)
    dev = F.deviations(m)
    cf = {}
    for key, hold in [("clock", dict(clock=True)), ("chain", dict(chain=True)), ("both_clocks", dict(clock=True, chain=True)),
                      ("people", dict(people=True)), ("depreciation", dict(depreciation=True)),
                      ("utility", dict(utility=True)), ("women", dict(women=True))]:
        c = counterfactual(par, p_ref, **hold)
        cf[key] = {s: nums(c[s].values) for s in ("wage_goods", "wage_shelter", "wage_living", "labour_share_c",
                                                   "prime_emp_rate", "theta_V", "x", "site_share")}
    fwd = {}
    for key, kw in [("held", dict(utility="held")), ("rising", dict(utility="rising")),
                    ("stopped", dict(utility="held", clocks="stopped"))]:
        a, info = ahead(par, p_ref, **kw)
        fwd[key] = dict(info=info, **{s: nums(a[s].values) for s in (
            "x", "x_ceiling", "wage_goods", "wage_shelter", "wage_living", "labour_share_c", "prime_emp_rate",
            "theta_V", "site_share", "chain_share", "inc_labour", "inc_land", "inc_interest", "coverage_idx")})
    return dict(
        name=name, label=R["meta"].get("label", name), meta={k: R["meta"][k] for k in (
            "goods", "women", "rho_fixed", "waves", "sigma", "utility", "pin_start", "names", "set")},
        par={k: float(v) for k, v in par.items()}, p_ref=p_ref, misfit=R["best"]["misfit"], by_series=R["best"]["by_series"],
        starts=[dict(misfit=s["misfit"], status=s["status"]) for s in R["starts"]],
        utility=nums(F.utility_path(F.UTILITY_KNOTS)), women=nums(F.women_path(par)),
        dev={s: nums(dev[s]) for s in F.SERIES},
        series={k: nums(v.values) for k, v in d.items()},
        counterfactual=cf, ahead=fwd)


if __name__ == "__main__":
    out = dict(years=YEARS, ahead=AHEAD, series=F.SERIES, tol_log=F.TOL_LOG, tol_level=F.TOL_LEVEL,
               record=None, models={})
    for name in ("fit_B", "fit_Bw"):
        out["models"][name] = model_block(name)
    load("fit_B")
    out["record"] = record()
    sp = os.path.join(ROOT, "results", "stress_B.json")
    out["stress"] = json.load(open(sp)) if os.path.exists(sp) else None
    os.makedirs(os.path.join(ROOT, "report"), exist_ok=True)
    with open(os.path.join(ROOT, "report", "report_B.json"), "w") as f:
        json.dump(out, f, separators=(",", ":"))
    page = os.path.join(ROOT, "report", "page.html")         # the page, with the numbers inlined: one file
    if os.path.exists(page):
        kit = open(os.path.join(ROOT, "report", "chartkit.js")).read()
        html = open(page).read().replace("/*CHARTKIT_JS*/", kit).replace("/*DATA_JSON*/", json.dumps(out, separators=(",", ":")))
        with open(os.path.join(ROOT, "report", "index.html"), "w") as f:
            f.write(html)
        print("report/index.html written")
    for name, mb in out["models"].items():
        s = mb["series"]
        print(name, f"misfit {mb['misfit']:.3f}", {k: round(v, 2) for k, v in mb["by_series"].items()})
        print("   x 1950/2024", s["x"][0], s["x"][-1], "| ceiling 2024", s["x_ceiling"][-1],
              "| site share", s["site_share"][0], s["site_share"][-1], "| chain share", s["chain_share"][0], s["chain_share"][-1])
        print("   income: labour", s["inc_labour"][0], s["inc_labour"][-1], "land", s["inc_land"][0], s["inc_land"][-1],
              "interest", s["inc_interest"][0], s["inc_interest"][-1], "| capital/income", s["capital_income"][0], s["capital_income"][-1])
        print("   land per task 2024", s["land_per_task"][-1], "| hours per task 2024", s["hours_per_task"][-1],
              "| land homes", s["land_homes"][0], s["land_homes"][-1])
        for k, c in mb["counterfactual"].items():
            print(f"   hold {k:13s} 2024: goods {c['wage_goods'][-1]}, shelter {c['wage_shelter'][-1]}, LS {c['labour_share_c'][-1]}, "
                  f"emp {c['prime_emp_rate'][-1]}, x {c['x'][-1]}; years solved {sum(v is not None for v in c['x'])}")
        for k, a in mb["ahead"].items():
            ok = [y for y, v in zip(YEARS + AHEAD, a["x"]) if v is not None]
            print(f"   ahead {k:8s} solved to {max(ok)}; 2050 x {a['x'][-1]}, LS {a['labour_share_c'][-1]}, emp {a['prime_emp_rate'][-1]}, "
                  f"goods {a['wage_goods'][-1]}, shelter {a['wage_shelter'][-1]}, info {a['info']}")
    print("report/report_B.json written")
