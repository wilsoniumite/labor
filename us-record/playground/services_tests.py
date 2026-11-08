# services_tests.py — a lead (2026-11-08): services apart (results/fit_Bs.json) fits the aggregate goods wage by
# automating nondurables fully by 2010 and de-automating services, and the wage over nondurables it never saw comes out
# at 308 in 2024 against the record's 165. Two tests:
#   T1  the wage over nondurables targeted too (eight series);
#   T2  T1 with services' 1950 level free (s0_srv: services' tasks e^s0 as hard for machines as nondurables' in 1950).
# Writes playground/services_tests.json.   Run from us-record/:  python3 playground/services_tests.py
import json
import sys
from multiprocessing import Pool

import numpy as np

sys.path.insert(0, "code")
import fit_base as F  # noqa: E402

R = json.load(open("results/fit_Bs.json"))
B0 = json.load(open("results/fit_Br0.json"))["best"]["par"]
M = R["meta"]
EXTRA = ["wage_durables", "wage_services", "wage_nondurables"]
META = {"T1": dict(M, extra=EXTRA), "T2": dict(M, extra=EXTRA, names=M["names"] + ["s0_srv"])}


def fit(job):
    part, start, label = job
    F.configure(META[part])
    r = F.run_start(F.complete(start))
    out = dict(part=part, label=label, misfit=r["misfit"], par=r["par"])
    if r["misfit"] < 10:
        m = F.model_path(r["par"])
        out["by"] = F.misfit_by_series(m)
        out["x"] = {str(y): [float(m.loc[y, "xd"]), float(m.loc[y, "x"]), float(m.loc[y, "xs"])] for y in (1950, 1970, 1990, 2024)}
    return out


if __name__ == "__main__":
    starts = [(R["best"]["par"], "the services fit"), (dict(B0, g_srv=B0["g_eta"]), "the main case, services on its clock")]
    starts += [(dict(s["par"]), f"services fit start {i}") for i, s in enumerate(R["starts"][1:3], 1)]
    jobs = [(p, dict(st), lab) for p in ("T1", "T2") for st, lab in starts]
    with Pool(4) as pool:
        out = pool.map(fit, jobs)
    json.dump(dict(fits=out), open("playground/services_tests.json", "w"), indent=1)
    for part in ("T1", "T2"):
        rows = sorted([r for r in out if r["part"] == part and r["misfit"] < 10], key=lambda r: r["misfit"])
        print(f"{part}: " + ", ".join(f"{r['misfit']:.3f}" for r in rows))
        if rows:
            r = rows[0]; p = r["par"]
            print("   by series: " + " ".join(f"{k} {v:.2f}" for k, v in r["by"].items()))
            print(f"   hours per unit of task capacity a year: durables {100 * (p['g_lam'] - p['g_dur']):.2f}%, nondurables "
                  f"{100 * (p['g_lam'] - p['g_eta']):.2f}%, services {100 * (p['g_lam'] - p['g_srv']):.2f}%"
                  + (f" | services' 1950 level e^{p['s0_srv']:.2f}" if "s0_srv" in p else ""))
            print("   tasks by machine (durables, nondurables, services): " + " | ".join(
                f"{y} " + "/".join(f"{v:.2f}" for v in x) for y, x in r["x"].items()))
