# land_grows.py — a flight lead (2026-11-06): the fitted economy saves land through machines alone, which is what drives
# land out of a machine's cost (the knife edge). In the record the land in use grew: suburbs, roads, the coverage
# ratio's rent flows. Here land in use grows at a free pace g_T (fit_base --land-grows) on the two-good main case
# (results/fit_Bd.json):
#   part 1  the six targets, the return at 2%: does the fit leave the ceiling, and what pace does it pick?
#   part 2  off the ceiling, as playground/off_ceiling.py: the chain's share of pay and the band for fixed rents as
#           targets beside the six, the return free.
# Writes playground/land_grows.json.   Run from us-record/:  python3 playground/land_grows.py
import json
import sys
from multiprocessing import Pool

import numpy as np
from scipy.optimize import least_squares

sys.path.insert(0, "code")
import fit_base as F  # noqa: E402

R = json.load(open("results/fit_Bd.json"))
META1 = dict(R["meta"], land="grow", names=R["meta"]["names"] + ["g_T"])
META2 = dict(META1, rho_fixed=None, names=META1["names"] + ["rho"])
BUN = json.load(open("../paths/results/chains.json"))["bundles"]["equipment_ipp_structures"]


def series(key):
    return np.array([BUN[str(y)][key] if str(y) in BUN else np.nan for y in F.YEARS])


CHAIN, SIG_LO, SIG_HI = series("comp_share_of_total_comp_domp"), series("imports_domp"), series("sigma_upper_open_domp")
MC, MS = ~np.isnan(CHAIN), ~np.isnan(SIG_LO)


def resid_off(u):
    keep = {s: F.counted(s) for s in F.all_series()}
    w = len(keep) + 2.0
    n = sum(int(k.sum()) for k in keep.values()) + int(MC.sum()) + int(MS.sum())
    m = F.model_path(F.unpack(u))
    if m is None:
        return np.full(n, 10.0)
    dev = F.deviations(m)
    parts = [dev[s][keep[s]] / np.sqrt(keep[s].sum() * w) for s in keep]
    parts.append((m["chain_share"].values[MC] - CHAIN[MC]) / 0.02 / np.sqrt(MC.sum() * w))
    sv = m["sigma_V"].values[MS]
    parts.append((sv - np.clip(sv, SIG_LO[MS], SIG_HI[MS])) / 0.02 / np.sqrt(MS.sum() * w))
    return np.concatenate(parts)


def readout(par, label, total, status):
    m = F.model_path(par)
    if m is None:
        return dict(label=label, misfit=None)
    by = F.misfit_by_series(m)
    sv = m["sigma_V"].values
    return dict(label=label, total=total, status=status, misfit=float(np.mean(list(by.values()))), by=by,
                par=dict(par, chi_max=F.pinned_chi(par)), sigma_V={y: float(m.loc[y, "sigma_V"]) for y in (1950, 1970, 1997, 2023)},
                band_misfit=float(np.mean(((sv[MS] - np.clip(sv[MS], SIG_LO[MS], SIG_HI[MS])) / 0.02) ** 2)),
                chain_2023=float(m.loc[2023, "chain_share"]), gap_2023=float(m.loc[2023, "x_ceiling"] - m.loc[2023, "x"]),
                x={y: float(m.loc[y, "x"]) for y in (1950, 2024)})


def part1(job):
    start, label = job
    F.configure(META1)
    r = F.run_start(F.complete(start))
    return readout(r["par"], label, r["misfit"], r["status"])


def part2(job):
    start, label = job
    F.configure(META2)
    lo = [np.log(F.bounds(n)[0]) if F.is_log(n) else F.bounds(n)[0] for n in F.NAMES]
    hi = [np.log(F.bounds(n)[1]) if F.is_log(n) else F.bounds(n)[1] for n in F.NAMES]
    u0 = np.clip(F.pack(F.complete(start)), np.array(lo) + 1e-9, np.array(hi) - 1e-9)
    if F.model_path(F.unpack(u0)) is None:
        return dict(label=label, misfit=None)
    r = least_squares(resid_off, u0, bounds=(lo, hi), max_nfev=2000, ftol=1e-9, xtol=1e-9)
    if r.status == 0:
        r = least_squares(resid_off, r.x, bounds=(lo, hi), max_nfev=2000, ftol=1e-9, xtol=1e-9)
    return readout(F.unpack(r.x), label, float(np.sum(r.fun ** 2)), int(r.status))


def show(title, rows):
    print(title)
    for r in sorted([r for r in rows if r.get("misfit") is not None], key=lambda r: r["total"])[:5]:
        p = r["par"]
        print(f"  {r['label']:38s} total {r['total']:6.3f} | targets {r['misfit']:6.3f} | " + " ".join(f"{v:5.2f}" for v in r["by"].values())
              + f" | g_T {100 * p['g_T']:5.2f}% rho {p['rho']:.3f} clock {100 * p['g_eta']:.1f}% dur {100 * p['g_dur']:.1f}%"
              f" | sigma_V " + " ".join(f"{y}:{v:.3f}" for y, v in r["sigma_V"].items())
              + f" | chain {r['chain_2023']:.3f} gap {r['gap_2023']:.4f}")


if __name__ == "__main__":
    F.configure(META1)
    best = R["best"]["par"]
    jobs1 = [(dict(best, g_T=g), f"main case, land growing {100 * g:.1f}%") for g in (0.005, 0.01, 0.02, 0.03)]
    jobs1 += [(dict(s, g_T=0.01), f"calibrated 1950 start {i + 1}") for i, s in enumerate(F.starts())]
    with Pool(4) as pool:
        out1 = pool.map(part1, jobs1)
    show("part 1: the six targets, land growing at a free pace, the return at 2%", out1)
    json.dump(dict(part1=out1), open("playground/land_grows.json", "w"), indent=1)
    oc = [r for r in json.load(open("playground/off_ceiling_Bd.json")) if r.get("misfit7") is not None]
    oc_best = min(oc, key=lambda r: r["misfit7"])["par"]
    good1 = sorted([r for r in out1 if r.get("misfit") is not None], key=lambda r: r["total"])[:3]
    jobs2 = [(dict(r["par"]), f"from part 1: {r['label']}") for r in good1]
    jobs2 += [(dict(oc_best, g_T=g), f"two-good off-ceiling fit, land {100 * g:.0f}%") for g in (0.01, 0.02, 0.03, 0.04)]
    with Pool(4) as pool:
        out2 = pool.map(part2, jobs2)
    show("part 2: off the ceiling (the chain and the band as targets too), the return free", out2)
    json.dump(dict(part1=out1, part2=out2), open("playground/land_grows.json", "w"), indent=1)
