# record_split.py — a flight lead (2026-11-06): the record-set fit (set_from_record.py D2, its best from record_starts.py)
# out of sample, as code/stress_B.py's split: fitted on 1950-1995 (and 1950-1985) only, read on the later years with the
# inputs as measured. Scored as the stress battery scores it (the mean over the original five series of the mean squared
# scaled deviation in the years left out), so it compares with results/stress_Bd.json's 9.5 and 46 (two goods, the main
# case) and stress_Bw.json's 21.6 and 16 (one good). With the wave and without it.
# Writes playground/record_split.json.   Run from us-record/:  python3 playground/record_split.py
import json
import sys
from multiprocessing import Pool

import numpy as np

sys.path.insert(0, "code")
sys.path.insert(0, "playground")
import fit_base as F  # noqa: E402
import record_case as RC  # noqa: E402  (BASE, NOWAVE; sets land in use growing with adults)

FIVE = ["wage_goods", "wage_shelter", "labour_share_c", "prime_emp_rate", "theta_V"]


def score(par):
    m = F.model_path(par)
    dev = F.deviations(m)
    out = {}
    for s in FIVE + ["wage_durables"]:
        keep = F.counted(s)
        left = F.target(s).notna().values & ~keep
        out[s] = float(np.mean(dev[s][left] ** 2)) if left.any() else None
    return out


def job(j):
    label, meta, start, fy = j
    F.configure(dict(meta, fit_years=fy))
    r = F.run_start(F.complete(start))
    if r["misfit"] >= 10:
        return dict(label=label, fit_years=fy, misfit=r["misfit"])
    o = score(r["par"])
    return dict(label=label, fit_years=fy, misfit=r["misfit"], out=o, out5=float(np.mean([o[s] for s in FIVE])), par=r["par"])


if __name__ == "__main__":
    RS = json.load(open("playground/record_starts.json"))["fits"]
    wave = min([r for r in RS if r["group"] == "starts" and r["misfit"] < 10], key=lambda r: r["misfit"])["par"]
    nowave = min([r for r in RS if r["group"] == "wave" and r["misfit"] < 10], key=lambda r: r["misfit"])["par"]
    jobs = [(lab, meta, start, fy) for lab, meta, start in (("with the wave", RC.BASE, wave), ("without the wave", RC.NOWAVE, nowave))
            for fy in ([1950, 1995], [1950, 1985])]
    with Pool(4) as pool:
        out = pool.map(job, jobs)
    json.dump(dict(fits=out), open("playground/record_split.json", "w"), indent=1)
    B = {v["name"]: v for v in json.load(open("results/stress_Bd.json"))["variants"] if v["group"] == "split"}
    for r in out:
        name = f"fitted {r['fit_years'][0]}-{r['fit_years'][1]}, read {r['fit_years'][1] + 1}-2024"
        b = B.get(name)
        bo = float(np.mean([x for x in b["by_series_out"].values() if x is not None])) if b else float("nan")
        if "out" not in r:
            print(f"{r['label']:17s} {name}: no path ({r['misfit']:.1f})")
            continue
        print(f"{r['label']:17s} {name}: in {r['misfit']:.3f} | out, the five {r['out5']:.2f} (the two-good main case {bo:.2f}) | "
              + " ".join(f"{s} {v:.2f}" for s, v in r["out"].items() if v is not None))
