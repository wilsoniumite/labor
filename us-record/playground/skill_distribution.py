# skill_distribution.py — a lead (2026-11-08), after the skill split's fits: with each good's pay at its industries' level
# and the model's average held at the production wage (results/fit_Bkl.json), high-skill services gain almost nothing
# against the average, because the hours that move into them raise the average itself. In the record the offset came
# partly from the workers who bring goods to buyers: trade, transportation and utilities' hourly earnings fell from 1.13
# to 0.86 of the production wage over 1964-2024 while their jobs grew from 11.7 to 28.8 million. Here the goods' workers
# are manufacturing's (durable or nondurable) and trade, transportation and utilities' together: each good's pay level
# is the geometric mean of the two on their shares of jobs each year (BLS CES via FRED: CES4000000008, USTPU, MANEMP;
# trade's earnings begin in 1964 and are held at 1964's ratio before). Everything else as fit_Bkl; refitted from its best
# and from the one-wage split's best. Writes playground/skill_distribution.json.
# Run from us-record/:  python3 playground/skill_distribution.py
import json
import os
import sys
from multiprocessing import Pool

import numpy as np

sys.path.insert(0, "code")
sys.path.insert(0, "playground")
import fit_base as F  # noqa: E402
from services_skill import fred, production_wage  # noqa: E402

R = json.load(open("results/fit_Bkl.json"))
RK = json.load(open("results/fit_Bk.json"))


def goods_levels():
    w = production_wage()
    ttu = (fred("CES4000000008") / w).reindex(F.YEARS)
    ttu = ttu.fillna(float(ttu.loc[1964])).where(lambda s: s.index >= 1964, float(ttu.loc[1964]))
    jobs_t, jobs_m = fred("USTPU").reindex(F.YEARS), fred("MANEMP").reindex(F.YEARS)
    share = (jobs_t / (jobs_t + jobs_m)).values
    out = {}
    for k in ("r_d", "r_n"):
        out[k] = np.exp((1.0 - share) * np.log(F.LVL_PATHS[k]) + share * np.log(ttu.values))
    return out, share


def fit(start):
    F.configure(R["meta"])
    F.LVL_PATHS.update(goods_levels()[0])
    r = F.run_start(F.complete(dict(start)))
    m = F.model_path(r["par"])
    out = dict(misfit=r["misfit"], par=r["par"])
    if m is not None:
        out["by"] = F.misfit_by_series(m)
        out["path"] = {c: [float(v) for v in m[c].values] for c in ("xd", "x", "xl", "xh", "r_d", "r_n", "r_l", "r_h", "kappa")}
    return out


if __name__ == "__main__":
    lv, share = goods_levels()
    print("trade's share of the goods' jobs:", " ".join(f"{y} {share[F.YEARS.index(y)]:.2f}" for y in (1950, 1964, 1990, 2024)))
    print("goods' levels, durables:", " ".join(f"{y} {lv['r_d'][F.YEARS.index(y)]:.3f}" for y in (1950, 1964, 1990, 2024)),
          "| nondurables:", " ".join(f"{y} {lv['r_n'][F.YEARS.index(y)]:.3f}" for y in (1950, 1964, 1990, 2024)))
    starts = [R["best"]["par"], RK["best"]["par"]] + [s["par"] for s in R["starts"][1:3]]
    with Pool(4) as pool:
        res = pool.map(fit, starts)
    res.sort(key=lambda r: r["misfit"])
    best = res[0]
    p = best["par"]
    print(f"best misfit {best['misfit']:.3f}", {k: round(v, 2) for k, v in best["by"].items()})
    print("hours per task capacity %%/yr: d %+.2f n %+.2f l %+.2f h %+.2f" % tuple(100 * (p["g_lam"] - p[k]) for k in ("g_dur", "g_eta", "g_low", "g_high")))
    for k in ("xh", "r_h", "kappa"):
        print(k, " ".join(f"{y} {best['path'][k][F.YEARS.index(y)]:.3f}" for y in (1950, 1980, 2000, 2024)))
    json.dump(dict(fits=res), open("playground/skill_distribution.json", "w"), indent=1)
