# hours_only.py — a lead, not a model: is the knife edge forced, or a choice of which clock moves? In the two-good main case
# (results/fit_Bd.json) the other goods' capability clock lowers both the land and the hours a task needs. Here it is held
# still (g_eta = 0, no wave: land per unit of task capacity constant for the other goods), so their progress can come only
# through the machine chain's hours (lambda, free); durables keep their own clock (g_dur, lowering both). Everything else
# refitted, from the calibrated 1950 starts and the main case. Writes playground/hours_only.json.
# Run from us-record/:  python3 playground/hours_only.py
import json
import sys
from multiprocessing import Pool

import numpy as np

sys.path.insert(0, "code")
import fit_base as F  # noqa: E402

R = json.load(open("results/fit_Bd.json"))
WAVE = [n for n in R["meta"]["names"] if n.startswith("w0_")]
META = dict(R["meta"], waves=[], fixed=dict(g_eta=0.0), names=[n for n in R["meta"]["names"] if n != "g_eta" and n not in WAVE])


def run(job):
    start, label = job
    F.configure(META)
    r = F.run_start(F.complete(start))
    m = F.model_path(r["par"])
    if m is None:
        return dict(label=label, misfit=None)
    return dict(label=label, misfit=r["misfit"], by=F.misfit_by_series(m), par=dict(r["par"], chi_max=F.pinned_chi(r["par"])),
                sigma_V={y: float(m.loc[y, "sigma_V"]) for y in (1950, 1970, 1997, 2023)},
                chain_2023=float(m.loc[2023, "chain_share"]), gap_2023=float(m.loc[2023, "x_ceiling"] - m.loc[2023, "x"]),
                x={y: float(m.loc[y, "x"]) for y in (1950, 2024)})


if __name__ == "__main__":
    F.configure(META)
    jobs = [(dict(R["best"]["par"], g_lam=R["best"]["par"]["g_lam"] - R["best"]["par"]["g_eta"]), "the main case, its hours clock")]
    jobs += [(dict(s, g_lam=-0.01), f"calibrated 1950 start {i + 1}") for i, s in enumerate(F.starts())]
    with Pool(4) as pool:
        out = pool.map(run, jobs)
    json.dump(out, open("playground/hours_only.json", "w"), indent=1)
    for r in sorted(out, key=lambda r: r["misfit"] if r["misfit"] is not None else 1e9)[:6]:
        if r["misfit"] is None:
            print(f"{r['label']:34s} failed")
            continue
        p = r["par"]
        print(f"{r['label']:34s} misfit {r['misfit']:6.3f} | " + " ".join(f"{v:5.2f}" for v in r["by"].values())
              + f" | sigma_V " + " ".join(f"{y}:{v:.3f}" for y, v in r["sigma_V"].items())
              + f" | chain {r['chain_2023']:.3f} | hours clock {100 * p['g_lam']:.1f}% durables {100 * p['g_dur']:.1f}% a {p['a']:.2f} k {p['k']:.1f}"
              f" | x {r['x'][1950]:.3f}->{r['x'][2024]:.3f} gap {r['gap_2023']:.4f}")
