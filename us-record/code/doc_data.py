# doc_data.py — the numbers behind the doc on the record-set fit (results/fit_Br.json, decision 25), every chart's rows in
# one file: the six series against the record, the machine chain against BEA's input-output tables and NIPA, the share of
# tasks automated, hours per unit of task capacity, the split of income and of a machine's cost, the held-out tests, and
# the return profile (the six series against the chain's measured size).
# Run from us-record/:  python3 code/doc_data.py              (writes results/doc_data.json; reads the stored fits)
#                       python3 code/doc_data.py --profile    (also refits the return at 4, 6, 10 and 12%: a few minutes)
import csv
import json
import os
import sys
from multiprocessing import Pool

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REPO = os.path.dirname(ROOT)
sys.path.insert(0, HERE)
import fit_base as F  # noqa: E402

Y = F.YEARS
NIPA_FILE = os.path.join(REPO, "progress_and_prosperity", "lambda", "data", "cache", "NipaDataA.txt")
NIPA_URL = "https://apps.bea.gov/national/Release/TXT/NipaDataA.txt"
SERIES = [("wage_goods", "Wage over goods (all but shelter)", "index"), ("wage_shelter", "Wage over shelter", "index"),
          ("wage_durables", "Wage over durables", "index"), ("labour_share_c", "Labour's share", "share"),
          ("prime_emp_rate", "Prime-age employment rate", "share"), ("theta_V", "Pay's share of a machine's cost", "share")]


def r4(v):
    return None if v is None or not np.isfinite(v) else round(float(v), 4)


def nipa():
    """GDP, consumption of fixed capital and net operating surplus by year ($ millions), BEA's NIPA flat file."""
    codes = {"A191RC": "gdp", "A262RC": "cfc", "W271RC": "nos"}
    out = {v: {} for v in codes.values()}
    with open(NIPA_FILE, encoding="utf-8") as f:
        for row in csv.reader(f):
            if row and row[0] in codes and row[1].isdigit():
                out[codes[row[0]]][int(row[1])] = float(row[2].replace(",", ""))
    return out


def years_of(meta, par):
    """Each year's two-good equilibrium and the drivers at par."""
    F.configure(meta)
    qs, es = F.durables_years(par)
    p = F.fill(par)
    lam = p["lam0"] * np.exp(p["g_lam"] * F.T_REL)
    return qs, es, lam, F.eta_path(par), F.eta_d_path(par)


def profile_fit(job):
    """The fit with the return set at rho, from fit_Br's best moved there (1950's distance to the chain's ceiling kept)."""
    meta, par, rho = job
    F.configure(dict(meta, rho_fixed=rho))
    old, new = par["rho"] + F.DELTA[0], rho + F.DELTA[0]
    start = dict(par, a=par["a"] * old / new, lam0=par["lam0"] * old / new, rho=rho)
    r = F.run_start(F.complete(start))
    if r["misfit"] >= 10:
        return dict(rho=rho, misfit=None)
    qs, _, _, _, _ = years_of(dict(meta, rho_fixed=rho), r["par"])
    i23 = Y.index(2023)
    q = qs[i23]
    return dict(rho=rho, misfit=r["misfit"], chain_2023=q["chain_share"], repl_2023=q["inv_income"] / (1 + q["inv_income"]))


if __name__ == "__main__":
    R = json.load(open(os.path.join(ROOT, "results", "fit_Br.json")))
    meta, par = R["meta"], R["best"]["par"]
    qs, es, lam, eta_g, eta_d = years_of(meta, par)
    F.configure(meta)
    m = F.model_path(par)
    by = F.misfit_by_series(m)
    out = dict(meta=dict(fit="results/fit_Br.json", misfit=R["best"]["misfit"], by_series=by, par=par, years=[Y[0], Y[-1]]))

    # the six series: record and model, by year
    rows = []
    for key, name, unit in SERIES:
        rec = F.target(key).values
        mod = m[key].values
        for i, y in enumerate(Y):
            rows.append(dict(series=key, name=name, unit=unit, year=y, record=r4(rec[i]), model=r4(mod[i])))
    out["six"] = rows
    out["six_misfit"] = [dict(series=k, name=n, misfit=round(by[k], 2)) for k, n, _ in SERIES]

    # the machine chain: the model's share of pay and replacement, against BEA input-output and NIPA; the 2% case beside
    B = json.load(open(os.path.join(REPO, "paths", "results", "chains.json")))["bundles"]["equipment_ipp_structures"]
    N = nipa()
    D = json.load(open(os.path.join(ROOT, "results", "fit_Bd.json")))
    qd, _, _, _, _ = years_of(D["meta"], D["best"]["par"])
    F.configure(meta)
    chain = []
    for i, y in enumerate(Y):
        q = qs[i]
        chain.append(dict(year=y, model=r4(q["chain_share"]), main_2pct=r4(qd[i]["chain_share"]),
                          record=r4(B[str(y)]["comp_share_of_total_comp_domp"]) if str(y) in B else None,
                          repl_model=r4(q["inv_income"] / (1 + q["inv_income"])),
                          repl_record=r4(N["cfc"][y] / N["gdp"][y]) if y in N["gdp"] and y in N["cfc"] else None))
    out["chain"] = chain

    # a machine's cost: the model's split by year, and the record's (domestic basis) 1997-2023
    cost = []
    for i, y in enumerate(Y):
        q = qs[i]
        cost.append(dict(year=y, pay=r4(q["theta_V"]), machines=r4(q["kappa_V"]), imported=r4(q["phi"]), land=r4(q["sigma_V"])))
    out["cost"] = cost
    out["cost_record"] = [dict(year=int(y), pay=r4(v["theta_domp"]), imported=r4(v["imports_domp"]),
                               surplus_depreciation=r4(v["gos_domp"]), taxes=r4(v["tax_domp"]))
                          for y, v in sorted(B.items(), key=lambda kv: int(kv[0])) if 1997 <= int(y) <= 2023]

    # tasks done by machines, and hours of the machine chain per unit of task capacity (1950 = 1)
    hp0, hd0 = lam[0] * eta_g[0], lam[0] * eta_d[0]
    out["tasks"] = [dict(year=y, other=r4(qs[i]["xg"]), durables=r4(qs[i]["xd"]),
                         hours_other=r4(lam[i] * eta_g[i] / hp0), hours_durables=r4(lam[i] * eta_d[i] / hd0))
                    for i, y in enumerate(Y)]

    # who earns the income: pay, the return on machines, the payment for imported content, land rent
    inc = []
    for i, y in enumerate(Y):
        q, e = qs[i], es[i]
        total = q["income"]
        inc.append(dict(year=y, pay=r4(q["v"] * q["n"] / total), machines=r4(e.rho * q["Vm"] * q["K"] / total),
                        imported=r4(q["rent_income"]), land=r4(e.T / total), site_share=r4(q["sb"] / q["Ps"])))
    out["income"] = inc

    # held out: fitted on the early years only, scored on the rest (as code/stress_B.py scores it, the original five)
    def split_score(path, name):
        v = next(v for v in json.load(open(os.path.join(ROOT, "results", path)))["variants"] if v["name"] == name)
        return round(float(np.mean([x for x in v["by_series_out"].values() if x is not None])), 2)
    held = []
    for label, path in (("One good, return 2%", "stress_Bw.json"), ("Two goods, return 2%", "stress_Bd.json")):
        held.append(dict(model=label, until=1995, misfit=split_score(path, "fitted 1950-1995, read 1996-2024")))
        held.append(dict(model=label, until=1985, misfit=split_score(path, "fitted 1950-1985, read 1986-2024")))
    RS = json.load(open(os.path.join(ROOT, "playground", "record_split.json")))["fits"]
    for label, lab in (("Set from the record", "with the wave"), ("Set from the record, no wave", "without the wave")):
        for r in RS:
            if r["label"] == lab:
                held.append(dict(model=label, until=r["fit_years"][1], misfit=round(r["out5"], 2)))
    out["held_out"] = held

    # the return: the six series barely move with it; the chain's measured size pins it
    prof_file = os.path.join(ROOT, "results", "doc_profile.json")
    if "--profile" in sys.argv:
        with Pool(4) as pool:
            prof = pool.map(profile_fit, [(meta, par, rho) for rho in (0.04, 0.06, 0.10, 0.12)])
        q23 = qs[Y.index(2023)]
        prof.append(dict(rho=par["rho"], misfit=R["best"]["misfit"], chain_2023=q23["chain_share"],
                         repl_2023=q23["inv_income"] / (1 + q23["inv_income"])))
        prof.sort(key=lambda r: r["rho"])
        json.dump(prof, open(prof_file, "w"), indent=1)
    if os.path.exists(prof_file):
        out["profile"] = [{k: r4(v) for k, v in r.items()} for r in json.load(open(prof_file))]
    out["sources"] = dict(nipa=NIPA_URL, chains="paths/results/chains.json (BEA input-output, paths/code/chains.py)",
                          panel="data/panel.csv (data/manifest.csv)")
    json.dump(out, open(os.path.join(ROOT, "results", "doc_data.json"), "w"), indent=1)
    print("results/doc_data.json written:", ", ".join(f"{k} {len(v)}" for k, v in out.items() if isinstance(v, list)))

    # the same rows as two long CSV files, the doc's charts read them (results/doc/): no empty cells, no commas in labels
    os.makedirs(os.path.join(ROOT, "results", "doc"), exist_ok=True)
    short = {"wage_goods": "goods", "wage_shelter": "shelter", "wage_durables": "durables", "labour_share_c": "labour",
             "prime_emp_rate": "employment", "theta_V": "machine"}
    with open(os.path.join(ROOT, "results", "doc", "six.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["series", "year", "kind", "value"])
        for r in out["six"]:
            for kind in ("record", "model"):
                if r[kind] is not None:
                    w.writerow([short[r["series"]], r["year"], kind, r[kind]])
    long = []
    for r in out["chain"]:
        for k, s in (("model", "chain_model"), ("main_2pct", "chain_2pct"), ("record", "chain_record"),
                     ("repl_model", "repl_model"), ("repl_record", "repl_record")):
            if r[k] is not None:
                long.append(("chain", s, r["year"], r[k]))
    for r in out["cost"]:
        for k in ("pay", "machines", "imported", "land"):
            long.append(("cost", k, r["year"], r[k]))
    for r in out["cost_record"]:
        for k in ("pay", "surplus_depreciation", "imported", "taxes"):
            long.append(("cost_record", k, r["year"], r[k]))
    for r in out["tasks"]:
        for k in ("other", "durables", "hours_other", "hours_durables"):
            long.append(("tasks", k, r["year"], r[k]))
    for r in out["income"]:
        for k in ("pay", "machines", "imported", "land"):
            long.append(("income", k, r["year"], r[k]))
    names = {"One good, return 2%": "One good at 2%", "Two goods, return 2%": "Two goods at 2%",
             "Set from the record": "Set from the record", "Set from the record, no wave": "Set from the record without the wave"}
    for r in out["held_out"]:
        long.append(("held", names[r["model"]], r["until"], r["misfit"]))
    for r in out.get("profile", []):
        for k, s in (("misfit", "misfit"), ("chain_2023", "chain"), ("repl_2023", "repl")):
            long.append(("profile", s, round(100 * r["rho"]), r[k]))
    with open(os.path.join(ROOT, "results", "doc", "rest.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["chart", "series", "x", "value"])
        w.writerows(long)
    print(f"results/doc/six.csv and rest.csv written ({len(long)} rows in rest.csv)")
