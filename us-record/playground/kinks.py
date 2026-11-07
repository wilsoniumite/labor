# kinks.py — a lead (2026-11-07): does the record show a change in the pace of machine progress? On the record-set fit
# without the wave (results/fit_Br0.json) hours of machine-making per unit of task capacity fall a steady 0.44% a year from
# 1950. Here the clock may change pace after a set year (fit_base KINKS, one fitted number each, shared by both goods):
# 1973 (the productivity slowdown), 1995 (the IT speed-up), both, and 1960. The spec's rule keeps a piece that improves
# the misfit by 20%.
# Writes playground/kinks.json.   Run from us-record/:  python3 playground/kinks.py
import json
import sys
from multiprocessing import Pool

sys.path.insert(0, "code")
import fit_base as F  # noqa: E402

R = json.load(open("results/fit_Br0.json"))
META0, PAR0 = R["meta"], R["best"]["par"]


def fit(years):
    names = META0["names"] + [f"kink{i}" for i in range(len(years))]
    meta = dict(META0, kinks=list(years), names=names)
    F.configure(meta)
    r = F.run_start(F.complete(dict(PAR0)))
    by = F.misfit_by_series(F.model_path(r["par"])) if r["misfit"] < 10 else {}
    return dict(kinks=list(years), misfit=r["misfit"], par=r["par"], by=by)


if __name__ == "__main__":
    jobs = [[1960], [1973], [1995], [1973, 1995]]
    with Pool(4) as pool:
        out = pool.map(fit, jobs)
    json.dump(dict(base=R["best"]["misfit"], fits=out), open("playground/kinks.json", "w"), indent=1)
    print(f"no kink: {R['best']['misfit']:.3f}  (hours per unit of task capacity {100 * (PAR0['g_lam'] - PAR0['g_eta']):.2f}% a year)")
    for r in out:
        p = r["par"]
        base_pace = p["g_lam"] - p["g_eta"]
        paces = [base_pace]
        for i in range(len(r["kinks"])):
            paces.append(paces[-1] - p[f"kink{i}"])
        print(f"kinks {r['kinks']}: misfit {r['misfit']:.3f} ({100 * (r['misfit'] / R['best']['misfit'] - 1):+.1f}%) | hours per unit of "
              f"task capacity, pace by period: " + ", ".join(f"{100 * x:.2f}%" for x in paces) + " | "
              + " ".join(f"{k} {v:.2f}" for k, v in r["by"].items()))
