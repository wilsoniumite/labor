# report_misses.py — her question of 2026-11-06 about the main case (B with the 1948 wave, results/fit_Bw.json): how
# bad are the misses? Is there an easy extension, are the data not fit for purpose, or do they kill the fit? Gathers
# what report/misses.html shows:
#   the machine chain   the model's share of pay, replacement over gross output and a machine's cost split, against BEA
#                       input-output and NIPA; the return walked up (playground/misses.json); the chain's measured share
#                       added as a sixth target (playground/chain_target.json)
#   the waterline       the six measures of companion/data/wc_grid.csv, computer prices apart from broad equipment
#   the coverage ratio  its members (pinning/data/kappa_results.csv): rent flows against Z.1 land values; the model on
#                       housing land (site in baskets) and on all land
#   housing's share     the model's site share at the basket's elasticity read against durables and against everything
#                       but shelter
#   out of sample       results/stress_Bw.json's splits
# Run from us-record/:  python3 code/report_misses.py      (writes report/misses.json and, from report/misses_page.html,
#                                                            report/misses.html)

import json
import os
import sys

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "code"))
import fit_base as F  # noqa: E402
import report_B as RB  # noqa: E402

YEARS = F.YEARS
num, nums = RB.num, RB.nums


def insides_at(meta, par):
    """The model's insides at a fit's settings and numbers."""
    F.configure(meta)
    p2, p_ref = RB.setup(par)
    d = RB.insides(RB.solve_all(F.economies(p2, p_ref=p_ref)))
    m = F.model_path(par)
    by = F.misfit_by_series(m)
    keep = ("x", "x_ceiling", "chain_share", "cfc_gross", "kappa_V", "theta_V", "sigma_V", "waterline", "coverage_idx",
            "coverage_homes_idx", "site_share", "land_homes", "wage_goods", "wage_shelter", "labour_share_c",
            "prime_emp_rate")
    return dict(by=by, misfit=float(np.mean(list(by.values()))), par={k: float(v) for k, v in p2.items()},
                series={k: nums(d[k].values) for k in keep})


def main():
    R = json.load(open(os.path.join(ROOT, "results", "fit_Bw.json")))
    META = R["meta"]
    out = dict(years=YEARS, models={})
    out["models"]["main"] = insides_at(META, R["best"]["par"])
    MS = json.load(open(os.path.join(ROOT, "playground", "misses.json")))
    out["rho_walk"] = [dict(rho=r["rho"], misfit=r["misfit"], by=r["by"], chain=r["chain_2023"], cfc=r["cfc_gross_2023"],
                            a=r["a"]) for r in [MS["main"]] + MS["rho"]]
    r5 = max(MS["rho"], key=lambda r: r["rho"])
    out["models"]["rho_top"] = insides_at(dict(META, rho_fixed=r5["rho"]), r5["par"])
    sg = [r for r in MS.get("sigma", []) if abs(r["sigma"] - 0.636) < 0.01]
    if sg:
        out["models"]["sigma_ex"] = insides_at(dict(META, sigma=sg[0]["sigma"]), sg[0]["par"])
    ct = os.path.join(ROOT, "playground", "chain_target.json")
    if os.path.exists(ct):
        runs = [r for r in json.load(open(ct)) if r.get("misfit6") is not None]
        out["chain_target"] = [dict(label=r["label"], misfit6=r["misfit6"], misfit5=r["misfit5"], by=r["by"], rho_free=r.get("rho_free"),
                                    chain_misfit=r["chain_misfit"], rho=r["par"]["rho"], g_eta=r["par"]["g_eta"],
                                    a=r["par"]["a"], sigma_V_2023=r["sigma_V_2023"]) for r in runs]
        if runs:
            best = min(runs, key=lambda r: r["misfit6"])
            meta6 = dict(META, rho_fixed=None, names=META["names"] + ["rho"]) if best.get("rho_free") else dict(META)
            out["models"]["sixth"] = insides_at(meta6, best["par"])
            out["models"]["sixth"]["label"] = best["label"]
    # off the ceiling (playground/off_ceiling.py, rent_floor.py): the seven-target fit and the five targets' cost of a
    # floor under fixed rents in a machine's cost
    oc = os.path.join(ROOT, "playground", "off_ceiling.json")
    if os.path.exists(oc):
        runs = [r for r in json.load(open(oc)) if r.get("misfit7") is not None]
        b7 = min(runs, key=lambda r: r["misfit7"])
        out["off_ceiling"] = dict(misfit7=b7["misfit7"], misfit5=b7["misfit5"], by=b7["by"], chain_misfit=b7["chain_misfit"],
                                  sigma_misfit=b7["sigma_misfit"], sigma_V=b7["sigma_V"], rho=b7["par"]["rho"],
                                  g_eta=b7["par"]["g_eta"], same=sum(abs(r["misfit7"] - b7["misfit7"]) < 1e-3 for r in runs),
                                  starts=len(runs) + sum(1 for r in json.load(open(oc)) if r.get("misfit7") is None))
        out["models"]["off"] = insides_at(dict(META, rho_fixed=None, names=META["names"] + ["rho"]), b7["par"])
    rf = os.path.join(ROOT, "playground", "rent_floor.json")
    if os.path.exists(rf):
        rows = [r for r in json.load(open(rf)) if r.get("misfit5") is not None]
        best = {}
        for r in rows:
            if r["floor"] not in best or r["misfit5"] < best[r["floor"]]["misfit5"]:
                best[r["floor"]] = r
        out["rent_floor"] = [dict(floor=0.0, misfit5=float(R["best"]["misfit"]), sigma_min=None, rho=0.02, by=R["best"]["by_series"])] + \
            [dict(floor=f, misfit5=r["misfit5"], sigma_min=r["sigma_min_1997_2023"], rho=r["rho"], by=r["by"], g_eta=r["g_eta"])
             for f, r in sorted(best.items())]
    F.configure(META)
    # the record
    P = F.PANEL.loc[YEARS]
    rec = dict(chain_tot=[None] * len(YEARS), chain_domp=[None] * len(YEARS))
    eco = json.load(open(os.path.join(F.REPO, "paths", "results", "chains.json")))
    for b in ("tot", "domp"):
        rec[f"chain_{b}"] = [num(eco["economy"][str(y)][f"inv_equipment_ipp_structures_comp_{b}_share_of_total_comp"])
                             if str(y) in eco["economy"] else None for y in YEARS]
    g1 = eco["targets_for_macro"]["g1_equipment_ipp_structures_full_chain"]
    rec["cost_split_2023"] = {k: g1[f"{k}_tot"]["2023"] for k in ("theta", "cfc", "tax", "nos")}
    # the domestic-labour basis, on which the panel's theta_V (the target) is read: imported content apart
    rec["cost_split_2023_domp"] = {k: g1[f"{k}_domp"]["2023"] for k in ("theta", "cfc", "tax", "nos", "imports")}
    rec["cfc_over_gdp_2023"] = eco["targets_for_macro"]["c_nipa"]["cfc_over_gdp"]["2023"]
    rec["nos_over_gdp_2023"] = eco["targets_for_macro"]["c_nipa"]["nos_over_gdp"]["2023"]
    wc = pd.read_csv(os.path.join(F.REPO, "companion", "data", "wc_grid.csv")).set_index("year")
    rec["waterline"] = {c: [num(wc[c].get(y, np.nan)) for y in YEARS] for c in wc.columns}
    k = pd.read_csv(os.path.join(F.REPO, "pinning", "data", "kappa_results.csv")).set_index("year")
    for c, name in (("k_flow_ls30_pc4", "coverage_flow"), ("k_z1_hh_gs10_pc4", "coverage_z1_households"),
                    ("kappa_med", "coverage_median")):
        rec[name] = [num(k[c].get(y, np.nan) / k[c].loc[1953]) for y in YEARS]
    rec["housing_share_pce"] = nums(P["housing_share_pce"].values)
    rec["delta"] = nums(P["delta"].values)
    rec["wage_durables"] = nums(P["wage_goods"].values)
    rec["wage_exshelter"] = nums(P["wage_exshelter"].values)
    rec["wage_shelter"] = nums(P["wage_shelter"].values)
    rec["labour_share_c"] = nums(P["labour_share_c"].values)
    out["record"] = rec
    S = json.load(open(os.path.join(ROOT, "results", "stress_Bw.json")))
    out["splits"] = [dict(name=v["name"], until=v["settings"]["fit_years"][1], path=v["path"], by_in=v["by_series_in"],
                          by_out=v["by_series_out"], g_eta=v["par"]["g_eta"]) for v in S["variants"] if v["group"] == "split"]
    out["base_path"] = S["base"]["path"]
    with open(os.path.join(ROOT, "report", "misses.json"), "w") as f:
        json.dump(out, f, separators=(",", ":"))
    page = os.path.join(ROOT, "report", "misses_page.html")
    if os.path.exists(page):
        with open(os.path.join(ROOT, "report", "misses.html"), "w") as f:
            kit = open(os.path.join(ROOT, "report", "chartkit.js")).read()
            f.write(open(page).read().replace("/*CHARTKIT_JS*/", kit).replace("/*DATA_JSON*/", json.dumps(out, separators=(",", ":"))))
        print("report/misses.html written")
    return out


if __name__ == "__main__":
    o = main()
    for k, m in o["models"].items():
        s = m["series"]
        i23 = YEARS.index(2023)
        print(f"{k:9s} misfit {m['misfit']:.3f} rho {m['par']['rho']:.3f} | chain {s['chain_share'][i23]:.3f} cfc {s['cfc_gross'][i23]:.3f}"
              f" kV {s['kappa_V'][i23]:.3f} sV {s['sigma_V'][i23]:.4f} water {s['waterline'][i23]:.2f}"
              f" cov(homes) {s['coverage_homes_idx'][-1]:.2f} site {s['site_share'][0]:.4f}->{s['site_share'][-1]:.4f}")
    print("report/misses.json written")
