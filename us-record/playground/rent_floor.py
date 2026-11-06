# rent_floor.py — how much fixed rent in a machine's cost can the record's wages carry? The main case refitted on its five
# targets alone, the return free, with a floor under fixed rents' share of a machine's cost (sigma_V) in 1997-2023 held
# by a stiff penalty (tolerance 0.005, weighing as five series): the best five-target fit at each floor. Floors from
# near zero to the record's imported content (18%, the band's lower edge in playground/off_ceiling.py). Starts: the main
# case and the off-ceiling fit. Writes playground/rent_floor.json.
# Run from us-record/:  python3 playground/rent_floor.py      (--base fit_Bd: two goods -> rent_floor_Bd.json)
import json
import sys
from multiprocessing import Pool

import numpy as np
from scipy.optimize import least_squares

sys.path.insert(0, "code")
import fit_base as F  # noqa: E402

BASE = sys.argv[sys.argv.index("--base") + 1] if "--base" in sys.argv else "fit_Bw"
SUFFIX = "" if BASE == "fit_Bw" else f"_{BASE[4:]}"
R = json.load(open(f"results/{BASE}.json"))
OC = json.load(open(f"playground/off_ceiling{SUFFIX}.json"))
BUN = json.load(open("../paths/results/chains.json"))["bundles"]["equipment_ipp_structures"]
CHAIN = np.array([BUN[str(y)]["comp_share_of_total_comp_domp"] if str(y) in BUN else np.nan for y in F.YEARS])
MS = ~np.isnan(CHAIN)                                  # 1997-2023
META = dict(R["meta"], rho_fixed=None, names=R["meta"]["names"] + ["rho"])


def resid(u, floor):
    keep = {s: F.counted(s) for s in F.all_series()}
    w = float(len(keep))
    n = sum(int(k.sum()) for k in keep.values()) + int(MS.sum())
    m = F.model_path(F.unpack(u))
    if m is None:
        return np.full(n, 10.0)
    dev = F.deviations(m)
    parts = [dev[s][keep[s]] / np.sqrt(keep[s].sum() * w) for s in keep]
    sv = m["sigma_V"].values[MS]
    parts.append(np.minimum(sv - floor, 0.0) / 0.005 / np.sqrt(MS.sum() / w))     # stiff: weighs as all the targets
    return np.concatenate(parts)


def fit_floor(job):
    floor, start, label = job
    F.configure(META)
    lo = [np.log(F.bounds(n)[0]) if F.is_log(n) else F.bounds(n)[0] for n in F.NAMES]
    hi = [np.log(F.bounds(n)[1]) if F.is_log(n) else F.bounds(n)[1] for n in F.NAMES]
    u0 = np.clip(F.pack(F.complete(start)), np.array(lo) + 1e-9, np.array(hi) - 1e-9)
    r = least_squares(lambda u: resid(u, floor), u0, bounds=(lo, hi), max_nfev=2000, ftol=1e-9, xtol=1e-9)
    if r.status == 0:
        r = least_squares(lambda u: resid(u, floor), r.x, bounds=(lo, hi), max_nfev=2000, ftol=1e-9, xtol=1e-9)
    par = F.unpack(r.x)
    m = F.model_path(par)
    if m is None:
        return dict(floor=floor, label=label, misfit5=None)
    by = F.misfit_by_series(m)
    sv = m["sigma_V"].values
    return dict(floor=floor, label=label, misfit5=float(np.mean(list(by.values()))), by=by,
                sigma_min_1997_2023=float(np.min(sv[MS])), sigma_V={y: float(m.loc[y, "sigma_V"]) for y in (1950, 1970, 1997, 2023)},
                chain_2023=float(m.loc[2023, "chain_share"]), rho=float(par["rho"]), g_eta=float(par["g_eta"]), a=float(par["a"]),
                k=float(par["k"]), x_2024=float(m.loc[2024, "x"]), gap_2023=float(m.loc[2023, "x_ceiling"] - m.loc[2023, "x"]),
                par=dict(par, chi_max=F.pinned_chi(par)))


if __name__ == "__main__":
    best_oc = min((r for r in OC if r.get("misfit7") is not None), key=lambda r: r["misfit7"])
    jobs = [(f, s, lab) for f in (0.03, 0.06, 0.10, 0.14, 0.185)
            for s, lab in ((R["best"]["par"], "from the main case"), (best_oc["par"], "from the off-ceiling fit"))]
    out = []
    with Pool(4) as pool:
        for r in pool.imap_unordered(fit_floor, jobs):
            out.append(r)
            print(f"done: floor {r['floor']:.3f} {r['label']} -> " + ("failed" if r["misfit5"] is None else f"{r['misfit5']:.3f}"), flush=True)
    json.dump(out, open(f"playground/rent_floor{SUFFIX}.json", "w"), indent=1)
    print()
    for f in sorted({r["floor"] for r in out}):
        rs = [r for r in out if r["floor"] == f and r["misfit5"] is not None]
        if not rs:
            print(f"floor {f:.3f}: no fit")
            continue
        r = min(rs, key=lambda r: r["misfit5"] + 100 * max(0.0, f - r["sigma_min_1997_2023"]))
        print(f"floor {f:.3f}: five {r['misfit5']:6.3f} | " + " ".join(f"{v:5.2f}" for v in r["by"].values())
              + f" | min sigma_V 1997-2023 {r['sigma_min_1997_2023']:.3f} | sigma_V " + " ".join(f"{y}:{v:.3f}" for y, v in r["sigma_V"].items())
              + f" | chain 2023 {r['chain_2023']:.3f} | rho {r['rho']:.3f} clock {100 * r['g_eta']:.1f}% a {r['a']:.2f} k {r['k']:.1f}"
              f" | x 2024 {r['x_2024']:.3f} gap {r['gap_2023']:.4f} ({r['label']})")
