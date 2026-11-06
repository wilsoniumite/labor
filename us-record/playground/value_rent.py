# value_rent.py — a flight lead (2026-11-06): the record's fixed rents in a machine's cost (imported content 18-21%,
# BEA, 1997-2023) as a value share phi priced with the machine, beside its land (code/two_goods.py's cmp["phi"]), on the
# two-good main case (results/fit_Bd.json), phi = 0.20 (the mean imported content, domestic basis):
#   L1  the six targets, the return at 2%;
#   L2  the six targets and the chain's share of pay (domestic basis, 1997-2023), the return free.
# Checks the income identity with phi (income = the baskets' cost) at L1's fit. Writes playground/value_rent.json.
# Run from us-record/:  python3 playground/value_rent.py
import json
import sys
from multiprocessing import Pool

import numpy as np
from scipy.optimize import least_squares

sys.path.insert(0, "code")
sys.path.insert(0, "playground")
import fit_base as F  # noqa: E402
import two_good_insides as TI  # noqa: E402

PHI = 0.20
R = json.load(open("results/fit_Bd.json"))
META1 = dict(R["meta"], value_rent=PHI)
META2 = dict(META1, rho_fixed=None, names=R["meta"]["names"] + ["rho"])
BUN = json.load(open("../paths/results/chains.json"))["bundles"]["equipment_ipp_structures"]
CHAIN = np.array([BUN[str(y)]["comp_share_of_total_comp_domp"] if str(y) in BUN else np.nan for y in F.YEARS])
MC = ~np.isnan(CHAIN)


def resid_chain(u):
    keep = {s: F.counted(s) for s in F.all_series()}
    w = len(keep) + 1.0
    n = sum(int(k.sum()) for k in keep.values()) + int(MC.sum())
    m = F.model_path(F.unpack(u))
    if m is None:
        return np.full(n, 10.0)
    dev = F.deviations(m)
    parts = [dev[s][keep[s]] / np.sqrt(keep[s].sum() * w) for s in keep]
    parts.append((m["chain_share"].values[MC] - CHAIN[MC]) / 0.02 / np.sqrt(MC.sum() * w))
    return np.concatenate(parts)


def l1(job):
    start, label = job
    F.configure(META1)
    r = F.run_start(F.complete(start))
    return dict(label=label, part="L1", total=r["misfit"], par=dict(r["par"], chi_max=F.pinned_chi(r["par"])))


def l2(job):
    start, label = job
    F.configure(META2)
    lo = [np.log(F.bounds(n)[0]) if F.is_log(n) else F.bounds(n)[0] for n in F.NAMES]
    hi = [np.log(F.bounds(n)[1]) if F.is_log(n) else F.bounds(n)[1] for n in F.NAMES]
    u0 = np.clip(F.pack(F.complete(start)), np.array(lo) + 1e-9, np.array(hi) - 1e-9)
    if F.model_path(F.unpack(u0)) is None:
        return dict(label=label, part="L2", total=None)
    r = least_squares(resid_chain, u0, bounds=(lo, hi), max_nfev=2000, ftol=1e-9, xtol=1e-9)
    if r.status == 0:
        r = least_squares(resid_chain, r.x, bounds=(lo, hi), max_nfev=2000, ftol=1e-9, xtol=1e-9)
    par = F.unpack(r.x)
    return dict(label=label, part="L2", total=float(np.sum(r.fun ** 2)), par=dict(par, chi_max=F.pinned_chi(par)))


if __name__ == "__main__":
    best = R["best"]["par"]
    d1950 = F.DELTA[0]
    a_phi = max(0.2, best["a"] - PHI / (best["rho"] + d1950))     # keep 1950's distance to the ceiling
    F.configure(META1)
    jobs1 = [(dict(best, a=a_phi), "the two-good main case, a lowered for phi")]
    jobs1 += [(s, f"calibrated 1950 start {i + 1}") for i, s in enumerate(F.starts())]
    with Pool(4) as pool:
        out1 = [r for r in pool.map(l1, jobs1) if r["total"] < 1e3]
    out1.sort(key=lambda r: r["total"])
    jobs2 = [(r["par"], f"from L1: {r['label']}") for r in out1[:3]]
    lead = json.load(open("playground/land_grows.json"))["part1"]          # a high-return start
    with Pool(4) as pool:
        out2 = [r for r in pool.map(l2, jobs2) if r.get("total") is not None and r["total"] < 1e3]
    out2.sort(key=lambda r: r["total"])
    json.dump(dict(phi=PHI, L1=out1, L2=out2), open("playground/value_rent.json", "w"), indent=1)
    for title, meta, rows in (("L1: the six targets, the return at 2%", META1, out1[:2]),
                              ("L2: the six targets and the chain, the return free", META2, out2[:2])):
        print(title)
        for r in rows:
            TI.show(f"  {r['label']} (all {r['total']:.3f}; return {100 * r['par']['rho']:.1f}%, a {r['par']['a']:.2f})", meta, r["par"])
    if out1:                                                          # the income identity with phi
        F.configure(META1)
        qs, es = F.durables_years(out1[0]["par"])
        gap = max(abs(q["income"] - q["Ps"] * q["B"]) / q["income"] for q in qs)
        print(f"income identity with phi = {PHI}: worst relative gap {gap:.1e}; rent's share of income 2023 "
              f"{qs[F.YEARS.index(2023)]['rent_income']:.3f}")
