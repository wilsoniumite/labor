# record_case.py — a flight lead (2026-11-06): is D2 (set_from_record.py: two goods, imported content as a value-share
# rent 0.20, the return 8%, land in use growing with adults, the six targets only) a fit to stand on? Three checks:
#   starts   the calibrated 1950 starts (fit_base.starts) beside D2's best: does anything fit better?
#   wave     without the 1948 wave (two numbers fewer), from D2's best and the calibrated starts;
#   return   the return set at 4, 6, 10 and 12% (stepped from D2's best), and the rent at 0.10 and 0.30.
# Writes playground/record_case.json.   Run from us-record/:  python3 playground/record_case.py
import json
import sys
from multiprocessing import Pool

import numpy as np

sys.path.insert(0, "code")
sys.path.insert(0, "playground")
import fit_base as F  # noqa: E402
import two_good_insides as TI  # noqa: E402

R = json.load(open("results/fit_Bd.json"))
M0 = R["meta"]
S = json.load(open("playground/set_from_record.json"))
D2 = min([r for r in S["fits"] if r["part"] == "D2"], key=lambda r: r["misfit"])["par"]
F.LAND_PATH = F.N_T.copy()                                   # land in use growing with adults
BASE = dict(M0, value_rent=S["phi"], land="path", rho_fixed=S["rho"])
NOWAVE = dict(BASE, waves=[], names=[n for n in M0["names"] if not n.startswith("w0_")])


def fit(job):
    group, meta, start, label = job
    F.configure(meta)
    r = F.run_start(F.complete(start))
    return dict(group=group, label=label, meta=F.settings_meta(), misfit=r["misfit"],
                par=dict(r["par"], chi_max=F.pinned_chi(r["par"])) if r["misfit"] < 10 else r["par"])


def moved(par, rho=None, dphi=0.0):
    """D2's best moved to a new return (a and lam0 scaled by the ratio of rho + delta in 1950) or a rent dphi higher (a
    lowered by dphi / (rho + delta)), so that 1950's distance to the chain's ceiling, 1 - phi - (rho + delta)(a + lam m),
    is about kept."""
    p = dict(par)
    old = p["rho"] + F.DELTA[0]
    new = (rho if rho is not None else p["rho"]) + F.DELTA[0]
    p["a"] = max(0.011, (p["a"] * old - dphi) / new)
    p["lam0"] = p["lam0"] * old / new
    if rho is not None:
        p["rho"] = rho
    return p


if __name__ == "__main__":
    F.configure(BASE)
    cal = F.starts()
    jobs = [("starts", BASE, dict(D2), "D2's best")] + [("starts", BASE, s, f"calibrated 1950 start {i + 1}") for i, s in enumerate(cal)]
    nw = {k: v for k, v in D2.items() if not k.startswith("w0_")}
    jobs += [("wave", NOWAVE, nw, "D2's best without the wave")]
    jobs += [("wave", NOWAVE, {k: v for k, v in s.items() if not k.startswith("w0_")}, f"calibrated 1950 start {i + 1}")
             for i, s in enumerate(cal[:5])]
    for rho in (0.04, 0.06, 0.10, 0.12):
        jobs.append(("return", dict(BASE, rho_fixed=rho), moved(D2, rho=rho), f"the return {rho:.0%}"))
    for phi in (0.10, 0.30):
        jobs.append(("rent", dict(BASE, value_rent=phi), moved(D2, dphi=phi - S["phi"]), f"the rent {phi:.2f}"))
    with Pool(4) as pool:
        out = pool.map(fit, jobs)
    json.dump(dict(base=dict(phi=S["phi"], rho=S["rho"], land="adults"), fits=out), open("playground/record_case.json", "w"), indent=1)
    for group in ("starts", "wave", "return", "rent"):
        rows = sorted([r for r in out if r["group"] == group], key=lambda r: r["misfit"])
        ok = [r for r in rows if r["misfit"] < 10]
        print(f"{group}: {len(ok)} of {len(rows)} reach an equilibrium path; best " +
              ", ".join(f"{r['label']} {r['misfit']:.3f}" for r in (ok if group in ("return", "rent") else ok[:4])))
    best_nw = min([r for r in out if r["group"] == "wave" and r["misfit"] < 10], key=lambda r: r["misfit"], default=None)
    if best_nw:
        F.LAND_PATH = F.N_T.copy()
        TI.show(f"without the wave ({best_nw['misfit']:.3f})", NOWAVE, best_nw["par"])
