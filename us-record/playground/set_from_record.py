# set_from_record.py — a flight lead (2026-11-06): the combination that matched every measured part of a machine's cost
# (rent_and_land.py C1: the value-share rent, land growing, the chain targeted, the return free -> 12.3%), now with what
# the record gives set rather than fitted, and the chain NOT targeted, so that the chain, replacement and the split of a
# machine's cost are read, not fitted. On the two-good main case (results/fit_Bd.json), the six targets only:
#   D1  the value-share rent 0.20 (BEA imported content), the return 8% (NIPA's split), land growing at a fitted pace;
#   D2  the same with land in use growing with adults (no free number for land);
#   D3  the value-share rent 0.20, land growing at a fitted pace, the return free.
# Writes playground/set_from_record.json.   Run from us-record/:  python3 playground/set_from_record.py
import json
import sys
from multiprocessing import Pool

import numpy as np

sys.path.insert(0, "code")
sys.path.insert(0, "playground")
import fit_base as F  # noqa: E402
import two_good_insides as TI  # noqa: E402

PHI, RHO = 0.20, 0.08
R = json.load(open("results/fit_Bd.json"))
M0 = R["meta"]
F.LAND_PATH = F.N_T.copy()                                    # D2: land in use growing with adults
META = {"D1": dict(M0, value_rent=PHI, land="grow", rho_fixed=RHO, names=M0["names"] + ["g_T"]),
        "D2": dict(M0, value_rent=PHI, land="path", rho_fixed=RHO),
        "D3": dict(M0, value_rent=PHI, land="grow", rho_fixed=None, names=M0["names"] + ["g_T", "rho"])}


def fit(job):
    part, start, label = job
    F.configure(META[part])
    r = F.run_start(F.complete(start))
    return dict(part=part, label=label, misfit=r["misfit"], par=dict(r["par"], chi_max=F.pinned_chi(r["par"])))


if __name__ == "__main__":
    RL = json.load(open("playground/rent_and_land.json"))["fits"]
    c1 = min([r for r in RL if r["part"] == "C1"], key=lambda r: r["total"])["par"]      # phi already in, return 12.3%
    c2 = min([r for r in RL if r["part"] == "C2"], key=lambda r: r["total"])["par"]
    LG = json.load(open("playground/land_grows.json"))["part2"]
    edge = min([r for r in LG if r.get("misfit") is not None], key=lambda r: r["misfit"])["par"]   # no phi, return 13.4%
    main = R["best"]["par"]                                                            # no phi, return 2%

    def from_phi(p, rho):                                     # a start fitted with phi: keep 1950's distance at a new return
        q = dict(p)
        q["a"] = max(0.011, (q["a"] * (q["rho"] + F.DELTA[0])) / (rho + F.DELTA[0]))
        q["rho"] = rho
        return q

    def no_phi(p, rho):                                       # a start fitted without phi: make room for it too
        q = dict(p)
        q["a"] = max(0.011, (q["a"] * (q["rho"] + F.DELTA[0]) - PHI) / (rho + F.DELTA[0]))
        q["rho"] = rho
        return q

    jobs = []
    for part in ("D1", "D2", "D3"):
        rho = RHO if part != "D3" else c1["rho"]
        jobs += [(part, from_phi(c1, rho), "from C1 (the value-share rent and land growing)"),
                 (part, no_phi(edge, rho), "from the land-growth lead's best six-target point"),
                 (part, no_phi(main, rho), "from the two-good main case"),
                 (part, from_phi(dict(c2, g_T=0.013), rho), "from C2 (the value-share rent, land from ERS)")]
    with Pool(4) as pool:
        out = pool.map(fit, jobs)
    out = [r for r in out if r["misfit"] < 10.0]
    out.sort(key=lambda r: r["misfit"])
    json.dump(dict(phi=PHI, rho=RHO, fits=out), open("playground/set_from_record.json", "w"), indent=1)
    for part, title in (("D1", "D1: phi 0.20, the return 8%, land growing at a fitted pace, the six targets only"),
                        ("D2", "D2: phi 0.20, the return 8%, land growing with adults, the six targets only"),
                        ("D3", "D3: phi 0.20, land growing at a fitted pace, the return free, the six targets only")):
        print(title)
        for r in [r for r in out if r["part"] == part][:2]:
            p = r["par"]
            TI.show(f"  {r['label']} (six {r['misfit']:.3f}; return {100 * p.get('rho', RHO):.1f}%, clock {100 * p['g_eta']:.1f}%,"
                    f" hours/task {100 * (p['g_lam'] - p['g_eta']):.2f}%" + (f", land {100 * p['g_T']:.2f}% a year" if "g_T" in p else "")
                    + ")", META[part], p)
