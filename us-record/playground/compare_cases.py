# compare_cases.py — the flight's leads side by side (2026-11-06): the two-good main case against the best fit of each lead,
# on the six targets and on what no fit was shown (the machine chain's size, replacement, machines' share of a machine's
# cost, fixed rents, the site's share of spending, coverage, the waterline). Reads results/fit_Bd.json and the leads' json.
# Run from us-record/:  python3 playground/compare_cases.py
import json
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, "code")
sys.path.insert(0, "playground")
import fit_base as F  # noqa: E402
import two_good_insides as TI  # noqa: E402

Y = F.YEARS
I23 = Y.index(2023)
P = pd.read_csv("data/panel.csv").set_index("year")
R = json.load(open("results/fit_Bd.json"))
M0 = R["meta"]


def best(rows, key="total"):
    return min([r for r in rows if r.get(key) is not None], key=lambda r: r[key])


def cases():
    out = [("main case (two goods, return 2%)", M0, R["best"]["par"])]
    LG = json.load(open("playground/land_grows.json"))
    m2 = dict(M0, land="grow", rho_fixed=None, names=M0["names"] + ["g_T", "rho"])
    out.append(("land growing at a fitted pace, the chain and the band targeted: the best six-target point (it misses the band)",
                m2, best(LG["part2"], "misfit")["par"]))
    out.append(("the same, the best point overall (off the ceiling)", m2, best(LG["part2"])["par"]))
    VR = json.load(open("playground/value_rent.json"))
    out.append(("value-share rent 0.20, chain targeted", dict(M0, value_rent=VR["phi"], rho_fixed=None, names=M0["names"] + ["rho"]),
                best(VR["L2"])["par"]))
    LE = json.load(open("playground/land_ers.json"))
    ers = np.array(LE["land_path"])
    out.append(("land in use from ERS, chain targeted", dict(M0, land="path", rho_fixed=None, names=M0["names"] + ["rho"]),
                best(LE["E2"])["par"], ers))
    RL = json.load(open("playground/rent_and_land.json"))
    phi = RL["phi"]
    out.append((f"value-share rent {phi:.2f} and land growing at a fitted pace, chain targeted",
                dict(M0, value_rent=phi, land="grow", rho_fixed=None, names=M0["names"] + ["g_T", "rho"]),
                best([r for r in RL["fits"] if r["part"] == "C1"])["par"]))
    out.append((f"value-share rent {phi:.2f} and land in use from ERS, chain targeted",
                dict(M0, value_rent=phi, land="path", rho_fixed=None, names=M0["names"] + ["rho"]),
                best([r for r in RL["fits"] if r["part"] == "C2"])["par"], ers))
    return out


def cases_record():
    """The main case against the record-set lead (set_from_record.py): the return and the value-share rent set from the
    record, the chain read, not fitted."""
    S = json.load(open("playground/set_from_record.json"))
    RL = json.load(open("playground/rent_and_land.json"))
    phi, rho = S["phi"], S["rho"]
    out = [("main case (two goods, return 2%)", M0, R["best"]["par"]),
           ("C1: the value-share rent, land growing, the chain targeted, the return free",
            dict(M0, value_rent=phi, land="grow", rho_fixed=None, names=M0["names"] + ["g_T", "rho"]),
            best([r for r in RL["fits"] if r["part"] == "C1"])["par"])]
    metas = {"D1": dict(M0, value_rent=phi, land="grow", rho_fixed=rho, names=M0["names"] + ["g_T"]),
             "D2": dict(M0, value_rent=phi, land="path", rho_fixed=rho),
             "D3": dict(M0, value_rent=phi, land="grow", rho_fixed=None, names=M0["names"] + ["g_T", "rho"])}
    text = {"D1": f"D1: the rent {phi:.2f} and the return {rho:.0%} set, land growing at a fitted pace, the six targets only",
            "D2": f"D2: the rent {phi:.2f} and the return {rho:.0%} set, land growing with adults, the six targets only",
            "D3": f"D3: the rent {phi:.2f} set, land growing at a fitted pace, the return free, the six targets only"}
    for part in ("D1", "D2", "D3"):
        out.append((text[part], metas[part], best([r for r in S["fits"] if r["part"] == part], "misfit")["par"],
                    F.N_T.copy() if part == "D2" else None))
    return out


def row(label, meta, par, land_path=None):
    if land_path is not None:                                   # a set path of land in use (ERS, or with adults)
        F.LAND_PATH = land_path
    d = TI.insides(meta, par)
    F.configure(meta)
    by = F.misfit_by_series(F.model_path(par))
    pf = F.fill(par)
    return dict(label=label, targets=np.mean(list(by.values())), **{k: v for k, v in by.items()},
                ret=pf["rho"], clock=pf["g_eta"], dur=pf["g_dur"], land=d["land"][-1],
                chain=d["chain_share"][I23], repl=d["cfc_gross"][I23], kappa=d["kappa_V"][I23], theta=d["theta_V"][I23], fixed=d["fixed"][I23],
                site50=d["site_share"][0], site24=d["site_share"][-1], cov=d["coverage_homes"][-1], water=d["waterline"][I23],
                homes=d["land_homes"][-1], gap=d["gap"][I23])


def table(rows):
    rec = dict(theta=f"{P.loc[2023, 'theta_V']:.3f}", chain="0.151", repl="0.164", kappa=f"{P.loc[2023, 'kappa_med']:.2f} ({P.loc[2023, 'kappa_min']:.2f}-)",
               fixed="0.18-0.38", site50=f"<{P.loc[1950, 'housing_share_pce']:.3f}", site24=f"<{P.loc[2024, 'housing_share_pce']:.3f}",
               cov="4.33", water="2.33")
    lines = [("all six targets", "targets", "{:.2f}"), ("  wage over goods", "wage_goods", "{:.2f}"),
             ("  wage over shelter", "wage_shelter", "{:.2f}"), ("  labour's share", "labour_share_c", "{:.2f}"),
             ("  prime-age employment", "prime_emp_rate", "{:.2f}"), ("  theta_V", "theta_V", "{:.2f}"),
             ("  wage over durables", "wage_durables", "{:.2f}"),
             ("return", "ret", "{:.1%}"), ("clock, other goods", "clock", "{:.1%}"), ("clock, durables", "dur", "{:.1%}"),
             ("land, 2024 / 1950", "land", "{:.1f}"),
             ("chain's share of pay 2023", "chain", "{:.3f}"), ("replacement / gross 2023", "repl", "{:.3f}"),
             ("pay's share of a machine 2023", "theta", "{:.3f}"), ("machines' share of a machine 2023", "kappa", "{:.3f}"), ("fixed rents (land + phi) 2023", "fixed", "{:.3f}"),
             ("site's share of spending 1950", "site50", "{:.4f}"), ("site's share of spending 2024", "site24", "{:.4f}"),
             ("coverage on housing land 2024", "cov", "{:.2f}"), ("waterline 2023 / 1999", "water", "{:.2f}"),
             ("land in homes 2024", "homes", "{:.2f}"), ("task line under the ceiling 2023", "gap", "{:.4f}")]
    w = 11
    print(f"{'':34s}" + "".join(f"{i + 1:>{w}d}" for i in range(len(rows))) + f"  {'record':>{w}s}")
    for name, key, fmt in lines:
        print(f"{name:34s}" + "".join(f"{fmt.format(r[key]):>{w}s}" for r in rows) + f"  {rec.get(key, ''):>{w}s}")
    for i, r in enumerate(rows):
        print(f"  {i + 1}: {r['label']}")
    print("record: the chain on the domestic basis (BEA input-output, chains.json); replacement NIPA CFC / GDP; machines' share"
          " the panel's kappa (median, lowest); fixed rents imported content to it plus surplus; the site is housing's share of"
          " spending less structures (housing shown); coverage and the waterline as in report/misses.html")


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "both"
    if which in ("leads", "both"):
        print("THE LEADS")
        table([row(*c) for c in cases()])
    if which in ("record", "both"):
        print("\nSET FROM THE RECORD")
        table([row(*c) for c in cases_record()])
