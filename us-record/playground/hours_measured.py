# hours_measured.py — a lead (2026-11-07): on the machine chain's ceiling the fit pins only one thing about technology,
# hours of machine-making per unit of task capacity (lambda times eta), and it falls 0.44% a year in the record-set fit
# without the wave (results/fit_Br0.json). The record has its direct counterpart: hours of work per dollar of the machine
# bundle (BEA input-output, full chain, domestic basis; paths/results/chains.json) times the bundle's quality-adjusted
# price (BEA's private nonresidential fixed investment price index, B008RG, NIPA annual file) = hours per real unit of
# machine. Here: (1) the record's path, 1998-2023, and its pace; (2) the fit redone with the pace set at faster values,
# stepped from fit_Br0: what do the six series say to the record's pace?
# The clock's bounds are widened (its own pace is not pinned on the ceiling; at 25% a year it sat on the bound).
# Writes playground/hours_measured.json.   Run from us-record/:  python3 playground/hours_measured.py
import csv
import json
import os
import sys

import numpy as np

sys.path.insert(0, "code")
sys.path.insert(0, "playground")
import fit_base as F  # noqa: E402
import two_good_insides as TI  # noqa: E402

NIPA = os.path.join("..", "progress_and_prosperity", "lambda", "data", "cache", "NipaDataA.txt")


def price_index(code="B008RG"):
    out = {}
    with open(NIPA, encoding="utf-8") as f:
        for row in csv.reader(f):
            if row and row[0] == code and row[1].isdigit():
                out[int(row[1])] = float(row[2].replace(",", ""))
    return out


def record_hours():
    """Hours per real unit of the machine bundle, 1998 = 1 (1997 has no hours in chains.json)."""
    B = json.load(open("../paths/results/chains.json"))["bundles"]["equipment_ipp_structures"]
    P = price_index()
    ys = [int(y) for y in sorted(B, key=int) if B[y].get("hours_per_dollar_domp") is not None]
    h = np.array([B[str(y)]["hours_per_dollar_domp"] * P[y] for y in ys])
    return ys, h / h[0]


def pace(ys, h):
    return float(np.polyfit(np.array(ys, dtype=float), np.log(h), 1)[0])


if __name__ == "__main__":
    F.BOUNDS["g_eta"] = (-0.05, 0.8)             # the clock's own pace is loose on the ceiling: let it go where it wants
    F.BOUNDS["g_dur"] = (-0.05, 0.9)
    ys, h = record_hours()
    rec_pace = pace(ys, h)
    R = json.load(open("results/fit_Br0.json"))
    meta0, par0 = R["meta"], R["best"]["par"]
    F.configure(meta0)
    p = F.fill(par0)
    lam_eta = p["lam0"] * np.exp(p["g_lam"] * F.T_REL) * F.eta_path(par0)
    i = [F.YEARS.index(y) for y in ys]
    fit_pace = pace(ys, lam_eta[i] / lam_eta[i[0]])
    print(f"hours per real unit of machine, record 1998-2023: {100 * rec_pace:.2f}% a year (x{h[-1]:.2f}); "
          f"the fit's hours per unit of task capacity: {100 * fit_pace:.2f}% a year")
    names = [n for n in meta0["names"] if n != "g_lam"]
    out = [dict(pace=float(p["g_lam"] - p["g_eta"]), misfit=R["best"]["misfit"], par=par0, label="fit_Br0 (free)")]
    start = dict(par0)
    for g in (-0.01, -0.015, -0.02, -0.025, -0.03):
        meta = dict(meta0, hours_per_task=g, names=names)
        F.configure(meta)
        r = F.run_start(F.complete({k: v for k, v in start.items() if k != "g_lam"}))
        if r["misfit"] >= 10:
            print(f"pace {100 * g:.1f}%: no equilibrium path")
            break
        par = dict(r["par"], chi_max=F.pinned_chi(r["par"]))
        start = par
        d = TI.insides(meta, par)
        by = F.misfit_by_series(F.model_path(par))
        rows = dict(pace=g, misfit=r["misfit"], par=par, by=by, x_2024=float(d["x_g"][-1]),
                    waterline=float(d["waterline"][F.YEARS.index(2023)]), chain=float(d["chain_share"][F.YEARS.index(2023)]),
                    clock=par["g_eta"], dur=par["g_dur"])
        out.append(rows)
        print(f"pace {100 * g:5.1f}% a year: misfit {r['misfit']:.3f} | " + " ".join(f"{k} {v:.2f}" for k, v in by.items())
              + f" | clock {100 * par['g_eta']:.1f}% durables {100 * par['g_dur']:.1f}% | tasks 2024 {rows['x_2024']:.3f}"
              f" | waterline 2023/1999 {rows['waterline']:.2f} | chain {rows['chain']:.3f}")
    json.dump(dict(record=dict(years=ys, hours=list(map(float, h)), pace=rec_pace), fit_pace=fit_pace, fits=out),
              open("playground/hours_measured.json", "w"), indent=1)
