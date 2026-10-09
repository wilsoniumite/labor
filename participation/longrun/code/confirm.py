# confirm.py — the one long-run look (longrun/PROTOCOL.md section 1, tier 3; L5). Runs once, after the LE-freeze, and
# reports:
#   - P-L on every unseen country-year of every member (primary; the verdicts, qualifiers, readings, the long-run
#     model-level verdict and the joint reading with the European look);
#   - P-L on the confirm half (replication; labels for information, no verdict; LR-K2's H is the look's, restricted;
#     LR-K2 is reported for information whenever each floor group has at least 2 countries, section 3);
#   - E-L on the confirm half (code/e_specs.py, at most three, Holm within E-L), if e_specs.py exists;
#   - the no-verdict pointer check (IPUMS MOMLOC/POPLOC against RELATE);
#   - the forecast sheets (FORECASTS.md) beside the results, each verdict (P-L and E-L) marked 'as forecast' when
#     every forecaster gave it at least 0.5;
#   - the no-verdict run 'with post-freeze segments' whenever data/segments_postfreeze.csv holds rows (section 8): the
#     rows reach only that run (specs.Data.post_seg), never a primary frame;
#   - Holm over the families frozen at L2 (data/coverage.json), LR-C1 only with Extract B.
# It opens the confirm half through opening.open_half in L14's order (q, knots recorded, F_L recorded, H recorded,
# outcomes), on one vintage of all the split's countries.
# Refuses (BlindingError), before any download:
#   - unless the confirm guard passes (fetch.allowed_countries('confirm'): both tags in order, clean longrun/ tree,
#     longrun/code unchanged since the LE tag, participation/code unchanged since the European E tag);
#   - if a results/confirm_*.json is already committed (the look happened);
#   - unless data/skeleton.json (the pre-look calibration and MDEs) is committed;
#   - unless the explore opening's knots are in the fetch log (L14: explore countries keep them);
#   - if results/confirm_<HEAD>.json exists.
# Bug policy (section 8): DEVIATED lists P-L tests whose rule changed after the L-freeze (empty at the freeze). A
# deviated C-L test whose confirm half passes the testability rule takes its primary from the confirm half; LR-K2 (whose
# confirm half fails it) keeps the frozen specification as primary, the deviated version reported beside it.
# e_specs.py contract: run(data) -> {id: result}, at most three, each with p and p_opposite (one-sided, predicted and
# opposite) and 'varies' naming the P-L test it varies, if any.
#
# Run from longrun/:  ../../venv/Scripts/python.exe code/confirm.py
# Out: results/confirm_<HEAD short>.json

from __future__ import annotations

import hashlib
import importlib
import json
import os
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
LROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import pandas as pd  # noqa: E402

import fetch  # noqa: E402
import ipums  # noqa: E402
import opening  # noqa: E402
import segments as sg  # noqa: E402
import specs  # noqa: E402

RESULTS = os.path.join(LROOT, "results")
SKELETON = os.path.join(LROOT, "data", "skeleton.json")
E_MAX = 3
DEVIATED: frozenset = frozenset()


def committed(path_glob: str) -> list[str]:
    rc, out = fetch._git("ls-files", "--", path_glob)
    if rc != 0:
        raise fetch.BlindingError("git ls-files failed")
    return [ln.strip() for ln in out.splitlines() if ln.strip()]


def head_short() -> str:
    rc, out = fetch._git("rev-parse", "--short", "HEAD")
    if rc != 0 or not out.strip():
        raise fetch.BlindingError("no HEAD commit")
    return out.strip()


def code_hash() -> dict:
    h = hashlib.sha256()
    files = sorted(f for f in os.listdir(HERE) if f.endswith(".py"))
    for f in files:
        h.update(f.encode() + b"\0" + open(os.path.join(HERE, f), "rb").read().replace(b"\r\n", b"\n") + b"\0")
    rc, tree = fetch._git("rev-parse", "HEAD:./code")
    return {"sha256_code_py": h.hexdigest(), "files": files, "git_tree_code": tree.strip() if rc == 0 else None}


def preconditions() -> None:
    fetch.allowed_countries("confirm")                        # the guard, before anything else
    done = committed("results/confirm_*.json")
    if done:
        raise fetch.BlindingError(f"the look already happened ({done}); a later run is post-look and labelled so")
    if not committed("data/skeleton.json"):
        raise fetch.BlindingError("data/skeleton.json is not committed: calibration and MDEs come before the look")
    if not fetch.recorded("knots", "explore"):
        raise fetch.BlindingError("the explore opening's knots are not in the fetch log (L14)")
    path = os.path.join(RESULTS, f"confirm_{head_short()}.json")
    if os.path.exists(path):
        raise fetch.BlindingError(f"{path} exists")


def members_in(members: dict, countries) -> dict:
    s = set(countries)
    return {k: [c for c in v if c in s] for k, v in members.items()}


FORECASTS = os.path.join(LROOT, "FORECASTS.md")
FORECAST_ROWS = {"LR-K2": "| LR-K2", "LR-Y0": "| LR-Y0", "C-6L": "| C-6L", "LR-C1": "| LR-C1"}


def forecasts(text: str) -> dict:
    """{participant: {test or E-L id: (P(supported), P(contradicted))}} from the filled sheets: the participant tables
    (P-L) and the E-L table (participant, E-L id, ..., P(supported), P(contradicted)); blank cells are skipped."""
    out, who, in_el = {}, None, False
    for ln in text.splitlines():
        if ln.startswith("## "):
            in_el = ln.startswith("## E-L")
            who = None if in_el else ln[3:].strip()
            continue
        if in_el and ln.startswith("|"):
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if len(cells) >= 7 and cells[0] and cells[1] and not set(cells[0]) <= set("-: "):
                try:
                    out.setdefault(cells[0], {})[cells[1]] = (float(cells[5]), float(cells[6]))
                except ValueError:
                    pass
            continue
        if who is None:
            continue
        for t, pre in FORECAST_ROWS.items():
            if ln.startswith(pre):
                cells = [c.strip() for c in ln.strip().strip("|").split("|")]
                try:
                    out.setdefault(who, {})[t] = (float(cells[4]), float(cells[5]))
                except (ValueError, IndexError):
                    pass
    return out


def as_forecast(labels: dict, fc: dict) -> dict:
    """Section 5: a verdict to which every forecaster gave at least 0.5 is marked 'as forecast'."""
    out = {}
    for t, lab in labels.items():
        ps = []
        for who, rows in fc.items():
            if t not in rows:
                ps = None
                break
            sup, con = rows[t]
            ps.append({"supported": sup, "contradicted": con}.get(lab, 1 - sup - con))
        out[t] = bool(ps) and all(p >= 0.5 for p in ps)
    return out


def run_e(data: specs.Data) -> dict | None:
    if not os.path.exists(os.path.join(HERE, "e_specs.py")):
        return None
    e_specs = importlib.import_module("e_specs")
    res = e_specs.run(data)
    if len(res) > E_MAX:
        raise ValueError(f"{len(res)} E-L hypotheses; the protocol allows at most {E_MAX}")
    return {"tests": res, "verdicts": specs.holm(res) if res else {}}


def post_freeze_rows() -> pd.DataFrame | None:
    """data/segments_postfreeze.csv (section 8), validated; None when it holds no rows."""
    if not sg.has_post_freeze():
        return None
    df = pd.read_csv(sg.POST, dtype={"tau": int}, keep_default_na=False)
    bad = sg.validate(df)
    if bad:
        raise ValueError("post-freeze segments table: " + "; ".join(bad[:5]))
    return df


def frozen_families(cube: dict) -> dict:
    fam = cube["families"]
    return {"K": list(fam.get("K", [])), "C-L": list(fam.get("C-L", []))}


def look(extract_b: bool = False) -> dict:
    preconditions()
    split = fetch.frozen_split()
    countries = split["countries"]
    op = opening.open_half("confirm", countries, extract_b=extract_b)
    sk = json.load(open(SKELETON, encoding="utf-8"))
    cal = sk.get("calibration")
    std = {t: v["std_mde"] for t, v in sk.get("mde", {}).items()}
    bench = {t: v["std_mde"] for t, v in sk.get("benchmark", {}).items()}
    members = op["cube"]["families"]["members"]
    fams = frozen_families(op["cube"])
    post = post_freeze_rows()
    data = specs.Data(op["cy"], op["cl"], op["knots"], op["H"], members, op["census"], cal, post_seg=post,
                      families=fams, kh_uncovered=op.get("kholodilin_uncovered"))
    full = specs.run(data, std_mde=std, bench=bench, extract_b=extract_b)
    conf = split["confirm"]
    data_c = specs.Data(op["cy"], op["cl"], op["knots"], {c: h for c, h in op["H"].items() if c in conf},
                        members_in(members, conf), op["census"], cal, families=fams,
                        kh_uncovered=op.get("kholodilin_uncovered"))
    rep = specs.run(data_c, qualifiers=False, robust=False, extract_b=extract_b, replication=True)
    rep["labels_for_information"] = rep.pop("verdicts")
    for k in ("model_verdict", "model_sentence", "joint_reading"):
        rep.pop(k, None)
    try:
        pointer = ipums.pointer_check("confirm")
    except ipums.ExtractError as e:
        pointer = {"error": str(e)}
    head = head_short()
    out = {"what": "the one long-run look (longrun/PROTOCOL.md section 1)", "head": head,
           "utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "code": code_hash(),
           "deviated": sorted(DEVIATED), "H": op["H"], "pre_look_mde": sk.get("mde"), "benchmark": sk.get("benchmark"),
           "primary": full, "P_confirm_half_replication": rep, "E_confirm_half": run_e(data_c),
           "pointer_check": pointer, "vintage_knots_vs_explore": op["vintage_knots"]}
    fc = forecasts(open(FORECASTS, encoding="utf-8").read()) if os.path.exists(FORECASTS) else {}
    out["forecasts"] = fc
    out["as_forecast"] = as_forecast(full["verdicts"], fc)
    if out["E_confirm_half"]:
        out["E_as_forecast"] = as_forecast(out["E_confirm_half"]["verdicts"], fc)
    os.makedirs(RESULTS, exist_ok=True)
    path = os.path.join(RESULTS, f"confirm_{head}.json")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(specs.clean_json(out), f, indent=1)
    out["path"] = path
    return out


def main() -> None:
    out = look(extract_b="--extract-b" in sys.argv)
    p = out["primary"]
    for t, lab in p["verdicts"].items():
        print(f"  {t:6s} {lab:13s} p {p['verdict_p'][t]['p']:.4f}  p_opp {p['verdict_p'][t]['p_opposite']:.4f}  "
              f"{p['qualifiers'].get(t, '')}  reading: {p['readings'].get(t)}")
    print(f"model: {p['model_sentence']}\njoint: {p['joint_reading']}\nwrote {out['path']} — commit it now; this was "
          "the one look")


if __name__ == "__main__":
    main()
