# confirm.py — the one look (PROTOCOL.md section 1, tier 3). Runs once, after the E freeze, and reports:
#   - P on the full sample, all 31 countries (primary; the verdicts and the model-level verdict);
#   - P on the confirm half (the clean-room replication; labels shown for information, no verdict);
#   - E on the confirm half (code/e_specs.py, the only valid test of E; Holm within E), if e_specs.py exists.
# F_c is standardised once with the full-sample mean and sd, and those constants serve both P runs (build.py).
# All 31 countries are downloaded in one vintage (C10). For every manifest query whose explore-half response is still in
# the local cache, the cached file's SHA-256 is matched against the fetch log and its explore-country values and flags
# are compared with the new vintage; differences are reported, not acted on. The minimum detectable effects of the
# explore-half run (results/specs_explore.json, committed before the look) are carried into the report, each with its
# projection to the full sample, (t_.95 + t_.80 with G_full - 1 df) x se_explore x sqrt(G_explore / G_full), labelled
# as projected; C-3 reports the MDE of each leg.
# The halves are those of data/split.json as frozen in the participation-P-freeze tag (eurostat.frozen_split).
# Bug policy (PROTOCOL section 7): for a test in specs.DEVIATED, the primary result is the confirm-half run's, the
# full-sample result is kept and labelled exploratory, and Holm runs over the family with the substituted p-values.
#
# Refuses (BlindingError), before any download:
#   - unless eurostat.guard('confirm') passes: tags participation-P-freeze and participation-E-freeze exist, in that
#     order, as ancestors of HEAD; the split is the frozen one; the participation/ tree is clean; participation/code
#     unchanged since the E tag;
#   - if a results/confirm_*.json is already committed (the look happened; later runs are post-look, by hand);
#   - unless results/specs_explore.json is committed (the explore-half MDEs must exist before the look);
#   - if results/confirm_<HEAD>.json exists.
# e_specs.py contract: run(cy, cl, geos, fstd) -> {id: result}, at most five, each result with keys p, p_opposite
# (one-sided, predicted and opposite direction), G_star, and whatever else it reports; 'varies' names the P an E varies.
#
# Run from participation/:  ../venv/Scripts/python.exe code/confirm.py
# Out: results/confirm_<HEAD short>.json

from __future__ import annotations

import hashlib
import importlib
import json
import os
import sys
from datetime import datetime, timezone

import numpy as np
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import build  # noqa: E402
import eurostat as es  # noqa: E402
import specs  # noqa: E402

RESULTS = os.path.join(ROOT, "results")
E_MAX = 5


def committed_results() -> list[str]:
    rc, out = es._git("ls-files", "--", "results/confirm_*.json")
    if rc != 0:
        raise es.BlindingError("git ls-files failed; cannot tell whether the look already happened")
    return [ln.strip() for ln in out.splitlines() if ln.strip()]


def explore_results_committed() -> bool:
    rc, out = es._git("ls-files", "--", "results/specs_explore.json")
    return rc == 0 and bool(out.strip()) and os.path.exists(os.path.join(RESULTS, "specs_explore.json"))


def mde_report(explore: dict, full: dict) -> dict:
    """The explore-half MDE of each test (C-3: of each leg) and its projection to the full sample."""
    out = {}
    for k in specs.PRIMARY:
        legs = ["C3a", "C3b"] if k == "C3" else [k]
        rows = {}
        for leg in legs:
            e, f = explore.get(leg, {}), full["tests"].get(leg, {})
            ge, gf, se = e.get("G"), f.get("G"), e.get("se_hc2", e.get("se")) if leg == "C5" else e.get("se")
            proj = (float((stats.t.ppf(0.95, gf - 1) + stats.t.ppf(0.80, gf - 1)) * se * np.sqrt(ge / gf))
                    if ge and gf and se is not None and gf > 1 else None)
            rows[leg] = {"mde_explore_half": e.get("mde"), "G_explore": ge, "se_explore": se,
                         "mde_full_sample_projected": proj, "G_full": gf}
        out[k] = rows if k == "C3" else rows[k]
    return out


def primary(full: dict, rep: dict, deviated=None) -> dict:
    """The primary results and verdicts: full sample, except tests in DEVIATED, which fall back to the confirm half."""
    deviated = set(specs.DEVIATED if deviated is None else deviated)
    tests = {k: (rep["tests"][k] if k in deviated else full["tests"][k]) for k in specs.PRIMARY}
    labels, model = specs.verdicts(tests)
    loo = {k: (rep if k in deviated else full)["leave_one_out"][k] for k in specs.PRIMARY}
    quals = specs.qualify(labels, loo)
    return {"source": {k: ("confirm half (deviated, PROTOCOL section 7)" if k in deviated else "full sample")
                       for k in specs.PRIMARY},
            "full_sample_exploratory": sorted(deviated), "tests": tests, "verdicts": labels, "leave_one_out": loo,
            "qualifiers": quals, "model_verdict": model, "model_qualifier": specs.model_qualifier(labels, quals)}


def head_short() -> str:
    rc, out = es._git("rev-parse", "--short", "HEAD")
    if rc != 0 or not out.strip():
        raise es.BlindingError("no HEAD commit")
    return out.strip()


def code_hash() -> dict:
    h = hashlib.sha256()
    files = sorted(f for f in os.listdir(HERE) if f.endswith(".py"))
    for f in files:
        h.update(f.encode() + b"\0" + open(os.path.join(HERE, f), "rb").read() + b"\0")
    rc, tree = es._git("rev-parse", "HEAD:./code")
    return {"sha256_code_py": h.hexdigest(), "files": files, "git_tree_code": tree.strip() if rc == 0 else None}


def explore_cache_path(m: dict, explore: list[str]) -> str | None:
    """Where eurostat.get cached this manifest query for the explore half (the same recipe as eurostat.get)."""
    g = build.query_geos(m, explore)
    if not g:
        return None
    code, filters, geos, since = es._check_query(m["dataset"], m["filters"], g, m.get("since"))
    query = json.dumps({"dataset": code, "filters": filters, "geos": geos, "since": since},
                       sort_keys=True, separators=(",", ":"))
    return os.path.join(es.RAW, "explore", f"{code}__{hashlib.sha1(query.encode()).hexdigest()[:12]}.json")


def vintage(raw_full: dict, explore: list[str]) -> dict:
    """C10: the explore countries' cells of the new vintage against the cached explore responses."""
    logged = set()
    if os.path.exists(es.LOG):
        for ln in open(es.LOG, encoding="utf-8"):
            if ln.strip():
                e = json.loads(ln)
                if e.get("half") == "explore" and "rejected" not in e:
                    logged.add(e.get("sha256"))
    out = {}
    for m in build.MANIFEST:
        path = explore_cache_path(m, explore)
        if path is None or not os.path.exists(path):
            out[m["id"]] = {"explore_cache": "absent"}
            continue
        blob = open(path, "rb").read()
        old = es.parse(json.loads(blob))
        new = raw_full[m["id"]]
        new = new[new["geo"].isin(set(old["geo"]))]
        keys = [c for c in old.columns if c not in ("value", "flag")]
        j = old.merge(new, on=keys, how="outer", suffixes=("_old", "_new"), indicator=True)
        both = j[j["_merge"] == "both"]
        vo, vn = both["value_old"].to_numpy(float), both["value_new"].to_numpy(float)
        same = (np.isnan(vo) & np.isnan(vn)) | (np.abs(vo - vn) <= 1e-9 * np.maximum(1, np.abs(vo)))
        out[m["id"]] = {"explore_cache": os.path.basename(path),
                        "sha256_in_fetch_log": hashlib.sha256(blob).hexdigest() in logged,
                        "cells_compared": int(len(both)), "values_differ": int((~same).sum()),
                        "flags_differ": int((both["flag_old"].astype(str) != both["flag_new"].astype(str)).sum()),
                        "cells_only_in_explore_vintage": int((j["_merge"] == "left_only").sum()),
                        "cells_only_in_new_vintage": int((j["_merge"] == "right_only").sum())}
    return out


def run_e(cy, cl, geos, fstd) -> dict | None:
    if not os.path.exists(os.path.join(HERE, "e_specs.py")):
        return None
    e_specs = importlib.import_module("e_specs")
    res = e_specs.run(cy, cl, geos, fstd)
    if len(res) > E_MAX:
        raise ValueError(f"{len(res)} E-hypotheses; the protocol allows at most {E_MAX}")
    return {"tests": res, "verdicts": specs.holm(res) if res else {}}


def look() -> dict:
    es.guard("confirm")                                       # before anything else
    done = committed_results()
    if done:
        raise es.BlindingError(f"the look already happened ({done}); a later run is post-look and labelled so")
    head = head_short()
    path = os.path.join(RESULTS, f"confirm_{head}.json")
    if os.path.exists(path):
        raise es.BlindingError(f"{path} exists")
    if not explore_results_committed():
        raise es.BlindingError("results/specs_explore.json is not committed: the explore-half MDEs come before the look")
    split = es.frozen_split()                                 # the halves as frozen in the P tag
    raw = build.fetch("confirm")                              # all 31 countries, one vintage
    cy, cl = build.country_year("confirm", raw=raw), build.country_level("confirm", raw=raw)
    fstd = specs.f_constants(cl, es.COUNTRIES)
    full = specs.run("confirm", cy, cl, geos=es.COUNTRIES, fstd=fstd)
    rep = specs.run("confirm", cy, cl, geos=split["confirm"], fstd=fstd)
    prim = primary(full, rep)
    rep["labels_for_information"] = rep.pop("verdicts")
    rep.pop("model_verdict")
    rep.pop("model_qualifier")
    if prim["full_sample_exploratory"]:                       # section 7: the full sample's labels are not the verdicts
        full["labels_exploratory"] = full.pop("verdicts")
        full.pop("model_verdict")
        full.pop("model_qualifier")
    pre = os.path.join(RESULTS, "specs_explore.json")         # the MDE the protocol asks for: explore half, pre-look
    mde = mde_report(json.load(open(pre, encoding="utf-8"))["tests"], full)
    out = {"what": "the one look (PROTOCOL.md section 1)", "head": head, "mde": mde,
           "utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "code": code_hash(),
           "F_standardisation_full_sample": {"mean": fstd[0], "sd": fstd[1]},
           "primary": prim, "P_full_sample": full, "P_confirm_half_replication": rep,
           "E_confirm_half": run_e(cy, cl, split["confirm"], fstd), "vintage_vs_explore": vintage(raw, split["explore"])}
    os.makedirs(RESULTS, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(specs.clean_json(out), f, indent=1)
    out["path"] = path
    return out


def main() -> None:
    out = look()
    prim = out["primary"]
    for k in specs.PRIMARY:
        r = prim["tests"][k]
        print(f"  {k:3s} p {r['p']:.4f}  p_opp {r['p_opposite']:.4f}  G* {r['G_star']:.1f}  {prim['verdicts'][k]}"
              f" {prim['qualifiers'][k]}  ({prim['source'][k]})")
    print(f"model: {prim['model_verdict']} {prim['model_qualifier']}\nwrote {out['path']} — commit it now; this was the one look")


if __name__ == "__main__":
    main()
