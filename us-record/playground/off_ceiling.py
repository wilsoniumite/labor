# off_ceiling.py — her go (2026-11-06): can the record be fitted with the economy off the machine chain's ceiling? The main
# case (B with the 1948 wave) refitted with two facts the forward model already uses, as targets beside the five:
#   the chain's share of all pay, 1997-2023, on the domestic-labour basis of the targeted theta_V (BEA input-output,
#     ../paths/results/chains.json bundles: equipment, IPP and private structures), tolerance 0.02 like theta_V;
#   fixed rents' share of a machine's cost (sigma_V = b / Vm), 1997-2023, as a band: at least the imported content, at
#     most imported content plus the net operating surplus (the same bundle and basis); only the distance outside the
#     band counts, at a tolerance of 0.02.
# The return is fitted. Each of the seven series weighs one seventh. Starts: the main case, the sixth-target fit
# (playground/chain_target.json, return 7.4%), and the twelve calibrated 1950 starts of fit_base.starts (calibration (c)'s
# closed form at fixed rents 0.30 of a machine's cost: off the ceiling). Writes playground/off_ceiling.json.
# Run from us-record/:  python3 playground/off_ceiling.py      (--base fit_Bd: the same test on two goods, durables apart,
#                                                              with the durables wage among the targets -> off_ceiling_Bd.json)
import json
import sys
from multiprocessing import Pool

import numpy as np
from scipy.optimize import least_squares

sys.path.insert(0, "code")
import fit_base as F  # noqa: E402

BASE = sys.argv[sys.argv.index("--base") + 1] if "--base" in sys.argv else "fit_Bw"
OUT = "playground/off_ceiling.json" if BASE == "fit_Bw" else f"playground/off_ceiling_{BASE[4:]}.json"
R = json.load(open(f"results/{BASE}.json"))
BUN = json.load(open("../paths/results/chains.json"))["bundles"]["equipment_ipp_structures"]


def series(key):
    return np.array([BUN[str(y)][key] if str(y) in BUN else np.nan for y in F.YEARS])


CHAIN = series("comp_share_of_total_comp_domp")
SIG_LO = series("imports_domp")
SIG_HI = series("sigma_upper_open_domp")               # imported content plus the net operating surplus
MC, MS = ~np.isnan(CHAIN), ~np.isnan(SIG_LO)
TOL = 0.02
META = dict(R["meta"], rho_fixed=None, names=R["meta"]["names"] + ["rho"])


def resid7(u):
    keep = {s: F.counted(s) for s in F.all_series()}
    w = len(keep) + 2.0                                  # every series weighs alike: the targets, the chain, the band
    n = sum(int(k.sum()) for k in keep.values()) + int(MC.sum()) + int(MS.sum())
    m = F.model_path(F.unpack(u))
    if m is None:
        return np.full(n, 10.0)
    dev = F.deviations(m)
    parts = [dev[s][keep[s]] / np.sqrt(keep[s].sum() * w) for s in keep]
    parts.append((m["chain_share"].values[MC] - CHAIN[MC]) / TOL / np.sqrt(MC.sum() * w))
    sv = m["sigma_V"].values[MS]
    parts.append((sv - np.clip(sv, SIG_LO[MS], SIG_HI[MS])) / TOL / np.sqrt(MS.sum() * w))
    return np.concatenate(parts)


def readout(par):
    m = F.model_path(par)
    by = F.misfit_by_series(m)
    sv = m["sigma_V"].values
    out = dict(misfit5=float(np.mean(list(by.values()))), by=by,
               chain_misfit=float(np.mean(((m["chain_share"].values[MC] - CHAIN[MC]) / TOL) ** 2)),
               sigma_misfit=float(np.mean(((sv[MS] - np.clip(sv[MS], SIG_LO[MS], SIG_HI[MS])) / TOL) ** 2)),
               sigma_V={y: float(m.loc[y, "sigma_V"]) for y in (1950, 1970, 1997, 2023)},
               chain_2023=float(m.loc[2023, "chain_share"]), gap_2023=float(m.loc[2023, "x_ceiling"] - m.loc[2023, "x"]),
               x={y: float(m.loc[y, "x"]) for y in (1950, 1990, 2024)})
    return out


def fit7(job):
    start, label = job
    F.configure(META)
    lo = [np.log(F.bounds(n)[0]) if F.is_log(n) else F.bounds(n)[0] for n in F.NAMES]
    hi = [np.log(F.bounds(n)[1]) if F.is_log(n) else F.bounds(n)[1] for n in F.NAMES]
    u0 = np.clip(F.pack(F.complete(start)), np.array(lo) + 1e-9, np.array(hi) - 1e-9)
    if F.model_path(F.unpack(u0)) is None:
        return dict(label=label, misfit7=None, why="no equilibrium path at the start")
    r = least_squares(resid7, u0, bounds=(lo, hi), max_nfev=2000, ftol=1e-9, xtol=1e-9)
    if r.status == 0:
        r = least_squares(resid7, r.x, bounds=(lo, hi), max_nfev=2000, ftol=1e-9, xtol=1e-9)
    par = F.unpack(r.x)
    if F.model_path(par) is None:
        return dict(label=label, misfit7=None, why="no equilibrium path at the end")
    return dict(label=label, misfit7=float(np.sum(r.fun ** 2)), status=int(r.status), nfev=int(r.nfev),
                par=dict(par, chi_max=F.pinned_chi(par)), **readout(par))


if __name__ == "__main__":
    F.configure(META)
    CT = json.load(open("playground/chain_target.json"))
    best6 = min((r for r in CT if r.get("misfit6") is not None), key=lambda r: r["misfit6"])
    jobs = [(R["best"]["par"], "the base fit"), (best6["par"], "the chain-target fit (return 7.4%)")]
    if BASE != "fit_Bw":                                  # the one-good off-ceiling fit as one more start
        oc1 = [r for r in json.load(open("playground/off_ceiling.json")) if r.get("misfit7") is not None]
        jobs.append((min(oc1, key=lambda r: r["misfit7"])["par"], "the one-good off-ceiling fit"))
    jobs += [(s, f"calibrated 1950 start {i + 1} (k {s['k']:.2f}, clock {100 * s['g_eta']:.0f}%)") for i, s in enumerate(F.starts())]
    out = []
    with Pool(4) as pool:
        for r in pool.imap_unordered(fit7, jobs):
            out.append(r)
            print("done:", r["label"], "->", "failed" if r.get("misfit7") is None else f"{r['misfit7']:.3f}", flush=True)
    json.dump(out, open(OUT, "w"), indent=1)
    print()
    for r in sorted(out, key=lambda r: r["misfit7"] if r.get("misfit7") is not None else 1e9):
        if r.get("misfit7") is None:
            print(f"{r['label']:44s} {r['why']}")
            continue
        p = r["par"]
        print(f"{r['label']:44s} all {r['misfit7']:6.3f} | targets {r['misfit5']:6.3f} | "
              + " ".join(f"{v:5.2f}" for v in r["by"].values()) + f" | chain {r['chain_misfit']:5.2f} ({r['chain_2023']:.3f})"
              f" sigma-band {r['sigma_misfit']:5.2f} | sigma_V " + " ".join(f"{y}:{v:.3f}" for y, v in r["sigma_V"].items())
              + f" | rho {p['rho']:.3f} a {p['a']:.2f} k {p['k']:.2f} clock {100 * p['g_eta']:.1f}%"
              f" wave {np.exp(-p['w0_size']):.2f}/{p['w0_tau']:.0f}y hours/task {100 * (p['g_lam'] - p['g_eta']):.1f}%"
              f" | x {r['x'][1950]:.3f}->{r['x'][2024]:.3f} gap {r['gap_2023']:.4f}")
