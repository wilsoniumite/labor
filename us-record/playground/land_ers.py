# land_ers.py — a flight lead (2026-11-06): land in use set from the record, not fitted. USDA ERS, Major Land Uses, urban
# area by state 1945-2022 (US total, 1,000 acres; cache/ERS_urban_area_1945_2022.xlsx, fetched 2026-11-06 from
# ers.usda.gov/data-products/major-land-uses, SHA-256 d0da463e...). The Census changed its urban definitions in 2000 and
# 2020 (the file's footnotes 6 and 9: pre- and post-2000 not directly comparable), so the path is built within
# definitions: log-linear between the ERS years to 1997 (2.7% a year from 1949), then 2002-2017 (1.5% a year), joined
# across 1997-2002 at that later pace; 2018-2024 at it too; 1950 = 1. On the two-good main case (results/fit_Bd.json):
#   E1  the six targets, the return at 2%;
#   E2  the six targets and the chain's share of pay (domestic basis), the return free.
# Writes playground/land_ers.json.   Run from us-record/:  python3 playground/land_ers.py
import json
import sys
from multiprocessing import Pool

import numpy as np
import openpyxl
from scipy.optimize import least_squares

sys.path.insert(0, "code")
sys.path.insert(0, "playground")
import fit_base as F  # noqa: E402
import two_good_insides as TI  # noqa: E402


def ers_land():
    wb = openpyxl.load_workbook("cache/ERS_urban_area_1945_2022.xlsx", read_only=True)
    rows = list(wb[wb.sheetnames[0]].iter_rows(values_only=True))
    head = rows[1]
    us = next(r for r in rows if r and isinstance(r[0], str) and r[0].strip() == "U.S. total")
    pts = {int(str(h).split()[0]): float(v) for h, v in zip(head[1:], us[1:]) if h is not None and v is not None}
    return pts


def land_path(pts):
    early = {y: v for y, v in pts.items() if 1949 <= y <= 1997}
    late = {y: v for y, v in pts.items() if 2002 <= y <= 2017}
    g_late = np.log(late[2017] / late[2002]) / 15.0
    ys = np.array(F.YEARS, dtype=float)
    ye, ve = np.array(sorted(early)), np.log(np.array([early[y] for y in sorted(early)]))
    out = np.interp(ys, ye, ve)                                  # log level, the pre-2000 definitions, to 1997
    l1997 = np.interp(1997.0, ye, ve)
    yl, vl = np.array(sorted(late)), np.log(np.array([late[y] for y in sorted(late)]))
    shift = (l1997 + g_late * 5.0) - vl[0]                       # 2002 joined to 1997 at the later pace
    for i, y in enumerate(F.YEARS):
        if 1997 < y < 2002:
            out[i] = l1997 + g_late * (y - 1997)
        elif 2002 <= y <= 2017:
            out[i] = np.interp(y, yl, vl) + shift
        elif y > 2017:
            out[i] = vl[-1] + shift + g_late * (y - 2017)
    return np.exp(out - out[0]), g_late


PTS = ers_land()
F.LAND_PATH, G_LATE = land_path(PTS)
R = json.load(open("results/fit_Bd.json"))
META1 = dict(R["meta"], land="path")
META2 = dict(META1, rho_fixed=None, names=R["meta"]["names"] + ["rho"])
BUN = json.load(open("../paths/results/chains.json"))["bundles"]["equipment_ipp_structures"]
CHAIN = np.array([BUN[str(y)]["comp_share_of_total_comp_domp"] if str(y) in BUN else np.nan for y in F.YEARS])
MC = ~np.isnan(CHAIN)


def resid_chain(u):
    keep = {s: F.counted(s) for s in F.all_series()}
    w = len(keep) + 1.0
    n = sum(int(k.sum()) for k in keep.values()) + int(MC.sum())
    m = F.model_path(F.unpack(u))
    if m is None:
        return np.full(n, 10.0)
    dev = F.deviations(m)
    parts = [dev[s][keep[s]] / np.sqrt(keep[s].sum() * w) for s in keep]
    parts.append((m["chain_share"].values[MC] - CHAIN[MC]) / 0.02 / np.sqrt(MC.sum() * w))
    return np.concatenate(parts)


def e1(job):
    start, label = job
    F.configure(META1)
    r = F.run_start(F.complete(start))
    return dict(label=label, total=r["misfit"], par=dict(r["par"], chi_max=F.pinned_chi(r["par"])))


def e2(job):
    start, label = job
    F.configure(META2)
    lo = [np.log(F.bounds(n)[0]) if F.is_log(n) else F.bounds(n)[0] for n in F.NAMES]
    hi = [np.log(F.bounds(n)[1]) if F.is_log(n) else F.bounds(n)[1] for n in F.NAMES]
    u0 = np.clip(F.pack(F.complete(start)), np.array(lo) + 1e-9, np.array(hi) - 1e-9)
    if F.model_path(F.unpack(u0)) is None:
        return dict(label=label, total=None)
    r = least_squares(resid_chain, u0, bounds=(lo, hi), max_nfev=2000, ftol=1e-9, xtol=1e-9)
    if r.status == 0:
        r = least_squares(resid_chain, r.x, bounds=(lo, hi), max_nfev=2000, ftol=1e-9, xtol=1e-9)
    par = F.unpack(r.x)
    return dict(label=label, total=float(np.sum(r.fun ** 2)), par=dict(par, chi_max=F.pinned_chi(par)))


if __name__ == "__main__":
    print(f"land in use (ERS urban area, within definitions): x{F.LAND_PATH[-1]:.2f} 1950-2024; 1949-97 "
          f"{100 * np.log(PTS[1997] / PTS[1949]) / 48:.2f}% a year, 2002-17 {100 * G_LATE:.2f}% a year")
    F.configure(META1)
    jobs1 = [(R["best"]["par"], "the two-good main case")] + [(s, f"calibrated 1950 start {i + 1}") for i, s in enumerate(F.starts())]
    with Pool(4) as pool:
        out1 = sorted([r for r in pool.map(e1, jobs1) if r["total"] < 1e3], key=lambda r: r["total"])
    LG = json.load(open("playground/land_grows.json"))["part1"]               # high-return land-growth fits as starts
    jobs2 = [(r["par"], f"from E1: {r['label']}") for r in out1[:2]]
    jobs2 += [(dict(r["par"]), f"from the land-growth lead: {r['label']}") for r in sorted(
        [r for r in LG if r.get("misfit") is not None], key=lambda r: r["total"])[:2]]
    with Pool(4) as pool:
        out2 = sorted([r for r in pool.map(e2, jobs2) if r.get("total") is not None and r["total"] < 1e3], key=lambda r: r["total"])
    json.dump(dict(land_path=list(F.LAND_PATH), E1=out1, E2=out2), open("playground/land_ers.json", "w"), indent=1)
    for title, meta, rows in (("E1: the six targets, land in use from ERS, the return at 2%", META1, out1[:2]),
                              ("E2: the six targets and the chain, land from ERS, the return free", META2, out2[:2])):
        print(title)
        for r in rows:
            TI.show(f"  {r['label']} (all {r['total']:.3f}; return {100 * r['par']['rho']:.1f}%, clock {100 * r['par']['g_eta']:.1f}%,"
                    f" durables {100 * r['par']['g_dur']:.1f}%)", meta, r["par"])
