# rent_and_land.py — a flight lead (2026-11-06): the two leads that each matched part of a machine's measured cost, together.
# playground/compare_cases.py showed the trade: land growing at a fitted pace with a high return matches the chain and
# replacement and fits the six targets best (1.51), but leaves fixed rents at zero; the record's imported content as a
# value-share rent (value_rent.py) puts fixed rents at the record's floor, but fits worse (2.80). Here both, on the
# two-good main case (results/fit_Bd.json), the value-share rent phi 0.20, the chain's share of pay (domestic basis,
# 1997-2023) a target beside the six, the return free:
#   C1  land growing at a fitted pace (fit_base --land-grows);
#   C2  land in use set from the record (USDA ERS urban area, playground/land_ers.py's path).
# Writes playground/rent_and_land.json.   Run from us-record/:  python3 playground/rent_and_land.py
import json
import sys
from multiprocessing import Pool

import numpy as np
from scipy.optimize import least_squares

sys.path.insert(0, "code")
sys.path.insert(0, "playground")
import fit_base as F  # noqa: E402
import land_ers as LE  # noqa: E402  (sets F.LAND_PATH to the ERS path; resid_chain: the six targets and the chain)
import two_good_insides as TI  # noqa: E402

PHI = 0.20
R = json.load(open("results/fit_Bd.json"))
M0 = R["meta"]
META1 = dict(M0, value_rent=PHI, land="grow", rho_fixed=None, names=M0["names"] + ["g_T", "rho"])
META2 = dict(M0, value_rent=PHI, land="path", rho_fixed=None, names=M0["names"] + ["rho"])


def fit(job):
    meta, start, label = job
    F.configure(meta)
    lo = [np.log(F.bounds(n)[0]) if F.is_log(n) else F.bounds(n)[0] for n in F.NAMES]
    hi = [np.log(F.bounds(n)[1]) if F.is_log(n) else F.bounds(n)[1] for n in F.NAMES]
    u0 = np.clip(F.pack(F.complete(start)), np.array(lo) + 1e-9, np.array(hi) - 1e-9)
    if F.model_path(F.unpack(u0)) is None:
        return dict(label=label, total=None)
    r = least_squares(LE.resid_chain, u0, bounds=(lo, hi), max_nfev=2000, ftol=1e-9, xtol=1e-9)
    if r.status == 0:
        r = least_squares(LE.resid_chain, r.x, bounds=(lo, hi), max_nfev=2000, ftol=1e-9, xtol=1e-9)
    par = F.unpack(r.x)
    return dict(label=label, total=float(np.sum(r.fun ** 2)), par=dict(par, chi_max=F.pinned_chi(par)))


def lowered(par, phi=PHI):
    """A start with room for phi: a lowered so that 1950's distance to the ceiling is kept."""
    p = dict(par)
    p["a"] = max(0.011, p["a"] - phi / (p.get("rho", 0.02) + F.DELTA[0]))
    return p


if __name__ == "__main__":
    LG = json.load(open("playground/land_grows.json"))["part2"]
    edge = min([r for r in LG if r.get("misfit") is not None], key=lambda r: r["misfit"])["par"]     # the 1.51 point
    off = min([r for r in LG if r.get("total") is not None], key=lambda r: r["total"])["par"]       # off the ceiling
    VR = min([r for r in json.load(open("playground/value_rent.json"))["L2"] if r.get("total") is not None],
             key=lambda r: r["total"])["par"]
    E2 = min([r for r in json.load(open("playground/land_ers.json"))["E2"] if r.get("total") is not None],
             key=lambda r: r["total"])["par"]
    jobs = [(META1, lowered(edge), "C1 from the land-growth lead's best six-target point"),
            (META1, lowered(off), "C1 from the land-growth lead's off-ceiling point"),
            (META1, dict(VR, g_T=0.011), "C1 from the value-rent lead, land growing 1.1%"),
            (META1, dict(E2, g_T=0.023), "C1 from the ERS lead, land growing 2.3%"),
            (META2, dict(E2), "C2 from the ERS lead"),
            (META2, dict(VR), "C2 from the value-rent lead"),
            (META2, lowered(edge), "C2 from the land-growth lead's best six-target point"),
            (META2, lowered(off), "C2 from the land-growth lead's off-ceiling point")]
    with Pool(4) as pool:
        out = pool.map(fit, jobs)
    out = [dict(r, part=r["label"][:2]) for r in out if r.get("total") is not None and r["total"] < 1e3]
    out.sort(key=lambda r: r["total"])
    json.dump(dict(phi=PHI, fits=out), open("playground/rent_and_land.json", "w"), indent=1)
    for part, meta in (("C1", META1), ("C2", META2)):
        print(f"{part}: phi {PHI}, the chain targeted, the return free, " + ("land growing at a fitted pace" if part == "C1"
                                                                           else "land in use from ERS"))
        for r in [r for r in out if r["part"] == part][:3]:
            p = r["par"]
            TI.show(f"  {r['label']} (all {r['total']:.3f}; return {100 * p['rho']:.1f}%, clock {100 * p['g_eta']:.1f}%, durables"
                    f" {100 * p['g_dur']:.1f}%" + (f", land {100 * p['g_T']:.2f}% a year" if "g_T" in p else "") + ")", meta, p)
