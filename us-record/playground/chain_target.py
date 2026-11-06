# chain_target.py — is the main case's oversized machine chain fatal? Refit B with the 1948 wave with a sixth target,
# the machine chain's share of all pay, 1997-2023 (BEA input-output, US cost shares: ../paths/results/chains.json),
# tolerance 0.02 like theta_V, weighted as one series of six. Four starts: the main case; its profile point with the
# clock at 3.4% a year (results/stress_Bw.json); and with the return free, from the main case and from the return walked
# to 5% (playground/misses.json). Writes playground/chain_target.json.
# Run from us-record/:  python3 playground/chain_target.py
import json
import sys
from multiprocessing import Pool

import numpy as np
from scipy.optimize import least_squares

sys.path.insert(0, "code")
import fit_base as F  # noqa: E402

R = json.load(open("results/fit_Bw.json"))
CH = json.load(open("../paths/results/chains.json"))["economy"]
DATA = np.array([CH[str(y)]["inv_equipment_ipp_structures_comp_tot_share_of_total_comp"] if str(y) in CH else np.nan
                 for y in F.YEARS])
MASK = ~np.isnan(DATA)
TOL = 0.02


def resid6(u):
    """The five series' scaled deviations and the chain's, each series weighing one sixth (one solve of the path)."""
    keep = {s: F.counted(s) for s in F.SERIES}
    n = sum(int(k.sum()) for k in keep.values()) + int(MASK.sum())
    m = F.model_path(F.unpack(u))
    if m is None:
        return np.full(n, 10.0)
    dev = F.deviations(m)
    parts = [dev[s][keep[s]] / np.sqrt(keep[s].sum() * 6.0) for s in F.SERIES]
    parts.append((m["chain_share"].values[MASK] - DATA[MASK]) / TOL / np.sqrt(MASK.sum() * 6.0))
    return np.concatenate(parts)


def fit6(job):
    meta, start, label = job
    F.configure(meta)
    lo = [np.log(F.bounds(n)[0]) if F.is_log(n) else F.bounds(n)[0] for n in F.NAMES]
    hi = [np.log(F.bounds(n)[1]) if F.is_log(n) else F.bounds(n)[1] for n in F.NAMES]
    u0 = np.clip(F.pack(F.complete(start)), np.array(lo) + 1e-9, np.array(hi) - 1e-9)
    r = least_squares(resid6, u0, bounds=(lo, hi), max_nfev=1500, ftol=1e-9, xtol=1e-9)
    if r.status == 0:
        r = least_squares(resid6, r.x, bounds=(lo, hi), max_nfev=1500, ftol=1e-9, xtol=1e-9)
    par = F.unpack(r.x)
    m = F.model_path(par)
    if m is None:
        return dict(label=label, misfit6=None)
    by = F.misfit_by_series(m)
    ch = float(np.mean(((m["chain_share"].values[MASK] - DATA[MASK]) / TOL) ** 2))
    return dict(label=label, misfit6=float(np.sum(r.fun ** 2)), misfit5=float(np.mean(list(by.values()))), by=by,
                chain_misfit=ch, par=dict(par, chi_max=F.pinned_chi(par)), status=int(r.status), nfev=int(r.nfev),
                chain_2023=float(m.loc[2023, "chain_share"]), sigma_V_2023=float(m.loc[2023, "sigma_V"]),
                sigma_V_1950=float(m.loc[1950, "sigma_V"]), gap_2023=float(m.loc[2023, "x_ceiling"] - m.loc[2023, "x"]),
                x_1950=float(m.loc[1950, "x"]), x_2024=float(m.loc[2024, "x"]), rho_free=meta.get("rho_fixed") is None)


if __name__ == "__main__":
    meta = dict(R["meta"])
    S = json.load(open("results/stress_Bw.json"))["variants"]
    MS = json.load(open("playground/misses.json"))
    slow = min((v for v in S if v["group"] == "profile"), key=lambda v: abs(v["par"]["g_eta"] - 0.034))
    free_rho = dict(meta, rho_fixed=None, names=meta["names"] + ["rho"])
    top = max(MS["rho"], key=lambda r: r["rho"])
    jobs = [(meta, R["best"]["par"], "from the main case"),
            (meta, slow["par"], f"from the clock at {100 * slow['par']['g_eta']:.1f}%"),
            (free_rho, R["best"]["par"], "return free, from the main case"),
            (free_rho, top["par"], f"return free, from the return at {100 * top['rho']:.0f}%")]
    out = []
    with Pool(4) as pool:
        for r in pool.imap_unordered(fit6, jobs):
            out.append(r)
            print("done:", r["label"], flush=True)
    json.dump(out, open("playground/chain_target.json", "w"), indent=1)
    for r in sorted(out, key=lambda r: r["misfit6"] if r["misfit6"] is not None else 1e9):
        if r["misfit6"] is None:
            print(f"{r['label']:40s} failed")
            continue
        p = r["par"]
        print(f"{r['label']:40s} six {r['misfit6']:6.3f} | five {r['misfit5']:6.3f} | "
              + " ".join(f"{v:5.2f}" for v in r["by"].values()) + f" | chain {r['chain_misfit']:6.2f} ({r['chain_2023']:.3f} in 2023)"
              f" | rho {p['rho']:.3f} a {p['a']:.2f} clock {100 * p['g_eta']:.1f}% hours/task {100 * (p['g_lam'] - p['g_eta']):.1f}%"
              f" | sigma_V {r['sigma_V_1950']:.3f}->{r['sigma_V_2023']:.4f} gap {r['gap_2023']:.4f} x {r['x_1950']:.3f}->{r['x_2024']:.3f}"
              f" | status {r['status']} nfev {r['nfev']}")
