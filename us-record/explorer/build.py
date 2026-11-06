# build.py — the explorer page (explorer/index.html): the panel's series and the stored fits as presets
# (explorer/data.json), inlined with the model (explorer/model.js) into the page template (explorer/page.html), so the
# page is one self-contained file. checks/check_explorer.py holds model.js to the Python model on every preset.
# Run from us-record/:  python3 explorer/build.py

import json
import os

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.join(ROOT, "explorer")
YEARS = list(range(1950, 2025))
# The explorer's fourth version (her ask, 2026-11-06: cleaner, around the main case): the main case and model B from
# results/, and two variants of the main case from the stress tests and the misses (playground: no Python twin).
PRESETS = [("main", "Main case: B with the 1948 wave", "fit_Bw"),
           ("B", "Model B, no wave", "fit_B")]
HELD = ["utility:1", "utility:2", "utility:3", "rho", "chi_max"]   # set from data or by choice: the fitter leaves them


def num(x):
    return None if x is None or not np.isfinite(x) else float(x)


def data():
    P = pd.read_csv(os.path.join(ROOT, "data", "panel.csv")).set_index("year")
    D = P.loc[YEARS]
    weak = (D["labour_share_c_tier"] == "WEAK").values
    ls_tol = np.where(weak, (D["labour_share_c_hi"] - D["labour_share_c_lo"]).values / 2.0, 0.01)
    rw = D["real_wage_cpi"] / D.loc[1950, "real_wage_cpi"]
    out = dict(years=YEARS, N=[float(x) for x in D["adults"] / D.loc[1950, "adults"]], delta=[float(x) for x in D["delta"]],
               ls_tol=[float(x) for x in ls_tol], weak=[bool(x) for x in weak],
               ls_lo=[num(x) for x in D["labour_share_c_lo"]], ls_hi=[num(x) for x in D["labour_share_c_hi"]],
               real_wage_cpi=[float(x) for x in rw], housing_share_pce=[num(x) for x in D["housing_share_pce"]],
               real_rate=[float(x) for x in D["real_rate"]], wage_exshelter=[float(x) for x in D["wage_exshelter"]])
    for s in ("wage_goods", "wage_shelter", "labour_share_c", "prime_emp_rate", "theta_V"):
        out[s] = [num(x) for x in D[s]]
    # the machine chain's share of all pay, BEA input-output at US cost shares (../paths/results/chains.json), 1997-2023
    eco = json.load(open(os.path.join(os.path.dirname(ROOT), "paths", "results", "chains.json")))["economy"]
    key = "inv_equipment_ipp_structures_comp_tot_share_of_total_comp"
    out["chain_share"] = [num(eco[str(y)][key]) if str(y) in eco else None for y in YEARS]
    return out, rw


def settings(meta, rw, par):
    """The page's settings for a stored fit: its switches, and model B's paths (women's entry, waves) from its numbers."""
    u = meta.get("utility") or {}
    knots = u.get("knots", [1950, u["until"]] if "until" in u else [1950, 1970])
    S = dict(cap=meta.get("cap"), sigma=meta.get("sigma"), pin=bool(meta.get("pin_start")),
             shelterW=meta.get("shelter_land_share"), clock=None, utility=[[int(k), float(rw.loc[k])] for k in knots])
    if meta.get("goods") == "exshelter":
        S["goods"] = "exshelter"
    if meta.get("women"):
        S["chi"] = [[1950, 0.0], [int(meta["women"]), float(par["chi_w"])]]
    if meta.get("waves"):
        S["waves"] = [dict(year=int(y), size=float(par[f"w{i}_size"]), tau=float(par[f"w{i}_tau"]))
                      for i, y in enumerate(meta["waves"])]
    return S


BASE_NAMES = ("T", "h", "a", "k", "chi_max", "rho", "g_eta", "lam0", "g_lam")


def presets(rw):
    out = []
    for pid, label, name in PRESETS:
        R = json.load(open(os.path.join(ROOT, "results", f"{name}.json")))
        par = R["best"]["par"]
        out.append(dict(id=pid, label=label, source=f"results/{name}.json", settings=settings(R["meta"], rw, par),
                        params={k: float(v) for k, v in par.items() if k in BASE_NAMES},
                        misfit=float(R["best"]["misfit"]), by_series={k: float(v) for k, v in R["best"]["by_series"].items()},
                        held=list(HELD)))
    return out


PLAY = [("tied", "Main case, hours per task tied to the clock", "results/stress_Bw.json", "hours per unit of task capacity steady"),
        ("rho5", "Main case, return 5%", "playground/misses.json", "rho:0.05")]


def play_presets(rw):
    """Variants of the main case the page can express (explorer/model.js only; checks/check_explorer.py has no Python
    twin): a stress-test variant (its settings and numbers) or a point of the misses' return walk."""
    out = []
    main = json.load(open(os.path.join(ROOT, "results", "fit_Bw.json")))
    for pid, label, path, key in PLAY:
        full = os.path.join(ROOT, path)
        if not os.path.exists(full):
            continue
        doc = json.load(open(full))
        if key.startswith("rho:"):
            r = next((x for x in doc.get("rho", []) if abs(x["rho"] - float(key[4:])) < 1e-9), None)
            if r is None:
                continue
            meta, par, misfit, by = main["meta"], r["par"], r["misfit"], r["by"]
        else:
            r = next(x for x in doc["variants"] if x["name"] == key)
            meta, par, misfit, by = r["settings"], r["par"], r["misfit"], r["by_series"]
        out.append(dict(id=pid, label=label, source=f"{path}#{key}", settings=settings(meta, rw, par),
                        params={k: float(v) for k, v in par.items() if k in BASE_NAMES}, misfit=float(misfit),
                        by_series={k: float(v) for k, v in by.items()},
                        held=list(HELD) + (["g_lamTask"] if pid == "tied" else [])))
    return out


def build():
    D, rw = data()
    doc = dict(data=D, presets=presets(rw) + play_presets(rw))
    with open(os.path.join(HERE, "data.json"), "w") as f:
        json.dump(doc, f, separators=(",", ":"))
    page = open(os.path.join(HERE, "page.html")).read()
    model = open(os.path.join(HERE, "model.js")).read()
    page = page.replace("/*MODEL_JS*/", model).replace("/*DATA_JSON*/", json.dumps(doc, separators=(",", ":")))
    with open(os.path.join(HERE, "index.html"), "w") as f:
        f.write(page)
    return doc


if __name__ == "__main__":
    doc = build()
    print("explorer/data.json and explorer/index.html written:", len(doc["presets"]), "presets")
