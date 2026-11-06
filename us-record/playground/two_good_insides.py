# two_good_insides.py — the facts the fit never saw, read from a two-good fit (durables apart): the two-good economy's own
# equilibria (fit_base.durables_years), not the one-good helpers of code/report_B.py. Import and call insides(meta, par),
# or run it on the two-good main case and the land-growth leads (playground/land_grows.json).
# Run from us-record/:  python3 playground/two_good_insides.py
import json
import sys

import numpy as np

sys.path.insert(0, "code")
import fit_base as F  # noqa: E402

Y = F.YEARS
I23, I99, I53 = Y.index(2023), Y.index(1999), Y.index(1953)


def insides(meta, par):
    F.configure(meta)
    got = F.durables_years(par)
    if got is None:
        return None
    qs, es = got
    par = F.fill(par)
    eta_g = F.eta_path(par)
    col = np.array([q["Ps"] / getattr(e, "utility", 1.0) for q, e in zip(qs, es)])   # a basket of 1950's utility
    homes = np.array([q["B"] * q["sb"] for q in qs])
    cov = homes / (np.array([e.N for e in es]) * col)
    wl = np.array([q["m"] for q in qs]) / eta_g                                      # the margin in the other goods' capability
    out = dict(
        cfc_gross=np.array([q["inv_income"] / (1.0 + q["inv_income"]) for q in qs]),
        chain_share=np.array([q["chain_share"] for q in qs]), sigma_V=np.array([q["sigma_V"] for q in qs]),
        kappa_V=np.array([q["kappa_V"] for q in qs]), theta_V=np.array([q["theta_V"] for q in qs]),
        fixed=np.array([q["fixed_rents"] for q in qs]),                              # land and any value-share rent
        waterline=wl / wl[I99], coverage_homes=cov / cov[I53],
        site_share=np.array([q["sb"] / q["Ps"] for q in qs]), dur_share=np.array([q["dur_share"] for q in qs]),
        land_homes=homes / np.array([e.T for e in es]), x_g=np.array([q["xg"] for q in qs]), x_d=np.array([q["xd"] for q in qs]),
        gap=np.array([q["xg_ceiling"] - q["xg"] for q in qs]), land=np.array([e.T for e in es]) / es[0].T)
    return out


def show(label, meta, par):
    d = insides(meta, par)
    if d is None:
        print(f"{label}: no equilibrium path")
        return
    by = F.misfit_by_series(F.model_path(par))
    print(f"{label}: targets {np.mean(list(by.values())):.3f} | " + " ".join(f"{k} {v:.2f}" for k, v in by.items()))
    print(f"   replacement/gross 2023 {d['cfc_gross'][I23]:.3f} (NIPA 0.164) | chain 2023 {d['chain_share'][I23]:.3f} (0.151 domestic)"
          f" | fixed rents 1950 {d['sigma_V'][0]:.3f} 1997 {d['sigma_V'][Y.index(1997)]:.3f} 2023 {d['sigma_V'][I23]:.3f} (record 0.18-0.38)")
    print(f"   waterline 2023 {d['waterline'][I23]:.2f} (broad equipment 2.33) | coverage on housing land 2024 {d['coverage_homes'][-1]:.2f}"
          f" (rent flows 4.33) | site share {d['site_share'][0]:.4f} -> {d['site_share'][-1]:.4f} (housing +44%)"
          f" | durables' share {d['dur_share'][0]:.3f} -> {d['dur_share'][-1]:.3f} (record 0.190 -> 0.130)")
    print(f"   land in use x{d['land'][-1]:.1f} by 2024, in homes {d['land_homes'][0]:.2f} -> {d['land_homes'][-1]:.2f} | task line (other goods)"
          f" {d['x_g'][0]:.3f} -> {d['x_g'][-1]:.3f}, durables {d['x_d'][0]:.3f} -> {d['x_d'][-1]:.3f} | gap to the ceiling 2023 {d['gap'][I23]:.4f}")


if __name__ == "__main__":
    R = json.load(open("results/fit_Bd.json"))
    show("the two-good main case (return 2%)", R["meta"], R["best"]["par"])
    L = json.load(open("playground/land_grows.json"))
    meta2 = dict(R["meta"], land="grow", rho_fixed=None, names=R["meta"]["names"] + ["g_T", "rho"])
    seen = set()
    for r in sorted([r for r in L["part2"] if r.get("misfit") is not None], key=lambda r: r["total"]):
        if round(r["total"], 3) in seen:
            continue
        seen.add(round(r["total"], 3))
        p = r["par"]
        show(f"land growing {100 * p['g_T']:.2f}% a year, return {100 * p['rho']:.1f}%, clocks {100 * p['g_eta']:.1f}% / "
             f"durables {100 * p['g_dur']:.1f}% (all eight series {r['total']:.3f})", meta2, p)
