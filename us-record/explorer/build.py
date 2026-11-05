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
PRESETS = [("kept", "Kept model: cap, basket, pinned start", "fit_capbasket_pin"),
           ("capbasket", "Cap and basket, start not pinned", "fit_capbasket"),
           ("turn1990", "Utility turning in 1990", "fit_kink90"),
           ("base", "The paper's model alone", "fit_base"),
           ("A", "With A (shelter as building and site)", "fit_A"),
           ("Acapbasket", "A, cap and basket", "fit_basket")]


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
               real_rate=[float(x) for x in D["real_rate"]])
    for s in ("wage_goods", "wage_shelter", "labour_share_c", "prime_emp_rate", "theta_V"):
        out[s] = [num(x) for x in D[s]]
    return out, rw


def settings(meta, rw):
    u = meta.get("utility") or {}
    knots = u.get("knots", [1950, u["until"]] if "until" in u else [1950, 1970])
    return dict(cap=meta.get("cap"), sigma=meta.get("sigma"), pin=bool(meta.get("pin_start")),
                shelterW=meta.get("shelter_land_share"), clock=None,
                utility=[[int(k), float(rw.loc[k])] for k in knots])


def presets(rw):
    out = []
    for pid, label, name in PRESETS:
        R = json.load(open(os.path.join(ROOT, "results", f"{name}.json")))
        out.append(dict(id=pid, label=label, source=f"results/{name}.json", settings=settings(R["meta"], rw),
                        params={k: float(v) for k, v in R["best"]["par"].items() if k != "g_c"},
                        misfit=float(R["best"]["misfit"]), by_series={k: float(v) for k, v in R["best"]["by_series"].items()},
                        locked=[] if not R["meta"].get("pin_start") else ["chi_max"]))
    return out


PLAY = [("tilt", "Play: tastes tilt from land after 1995", "playground/round3.json", "internet: tastes tilt from land after 1995"),
        ("Aprime", "Play: building priced like building work (A′)", "playground/results.json",
         "A' (shelter's building priced at the wage, site 0.4)"),
        ("rho5", "Play: required return fixed at 5%", "playground/round4.json", "return 5% (kept model otherwise)")]


def play_presets():
    """Playground fits the page can express (explorer/model.js only; checks/check_explorer.py has no Python twin)."""
    out = []
    for pid, label, path, key in PLAY:
        full = os.path.join(ROOT, path)
        if not os.path.exists(full):
            continue
        r = json.load(open(full))[key]
        out.append(dict(id=pid, label=label, source=f"{path}#{key}", settings=r["S"], params=r["par"], misfit=r["misfit"],
                        by_series=r["by"], locked=["chi_max"] + (["rho"] if pid == "rho5" else [])))
    return out


def build():
    D, rw = data()
    meta = json.load(open(os.path.join(ROOT, "results", "fit_capbasket_pin.json")))["meta"]
    doc = dict(data=D, presets=presets(rw) + play_presets(), set_values=dict(cap=meta["cap"], sigma=meta["sigma"], shelterW=0.4,
                                                            utility=[[1950, 1.0], [1970, float(rw.loc[1970])]]))
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
