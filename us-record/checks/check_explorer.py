# check_explorer.py — the explorer's JavaScript model (explorer/model.js) against the Python model (code/fit_base.py), on
# every preset the page offers (explorer/data.json, from the stored fits): each year's five targeted series, and the
# misfit by series and in total, to a relative 1e-9; the pinned work-cost scale where the start is pinned. Needs Node.
# Run from us-record/:  python3 explorer/build.py && python3 checks/check_explorer.py      Exit 0 only if all pass.

import json
import os
import subprocess
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "code"))
import fit_base as F  # noqa: E402

DOC = json.load(open(os.path.join(ROOT, "explorer", "data.json")))
RESULTS = []
NODE = r"""
const M = require(process.argv[1]);
const doc = JSON.parse(require("fs").readFileSync(process.argv[2], "utf8"));
const out = {};
for (const p of doc.presets) {
  const m = M.path(p.params, p.settings, doc.data);
  const mf = M.misfit(m, doc.data);
  out[p.id] = { ok: m.ok, chi_max: m.chi_max, misfit: mf.total, by: mf.by,
                series: Object.fromEntries(M.SERIES.map((s) => [s, m[s]])) };
}
process.stdout.write(JSON.stringify(out));
"""


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok)))
    print(f"{'PASS' if ok else 'FAIL'} {name}" + (f" — {detail}" if detail else ""))


js = json.loads(subprocess.run(["node", "-e", NODE, os.path.join(ROOT, "explorer", "model.js"),
                                os.path.join(ROOT, "explorer", "data.json")],
                               capture_output=True, text=True, check=True).stdout)
for p in DOC["presets"]:
    if not p["source"].startswith("results/"):                  # playground presets: JavaScript only, no Python twin
        continue
    R = json.load(open(os.path.join(ROOT, p["source"])))
    meta = R["meta"]
    F.SHELTER_LAND_SHARE, F.CAP, F.SIGMA = meta.get("shelter_land_share"), meta.get("cap"), meta.get("sigma")
    F.PIN_START, F.SPLIT_FROM = bool(meta.get("pin_start")), None
    u = meta.get("utility") or {}
    F.UTILITY_KNOTS = u.get("knots", [1950, u["until"]] if "until" in u else [1950, 1970])
    m = F.model_path(R["best"]["par"])
    j = js[p["id"]]
    gap = max(float(np.max(np.abs(np.array(j["series"][s]) - m[s].values) / np.abs(m[s].values))) for s in F.SERIES)
    by = F.misfit_by_series(m)
    mis_gap = max(abs(j["by"][s] - by[s]) / max(by[s], 1e-12) for s in F.SERIES)
    tot = abs(j["misfit"] - R["best"]["misfit"]) / R["best"]["misfit"]
    chi_ok = (not F.PIN_START) or abs(j["chi_max"] - F.pinned_chi(R["best"]["par"])) / j["chi_max"] < 1e-9
    check(f"{p['id']:11s} the JS model reproduces {p['source']}: every year of the five series, the misfit by series and "
          "in total (relative 1e-9)" + (", and the pinned work-cost scale" if F.PIN_START else ""),
          j["ok"] and gap < 1e-9 and mis_gap < 1e-9 and tot < 1e-9 and chi_ok,
          f"series {gap:.1e}, by series {mis_gap:.1e}, total {tot:.1e}")

n_fail = sum(not ok for _, ok in RESULTS)
print(f"\n{'ALL GREEN' if not n_fail else f'{n_fail} FAILED'} ({len(RESULTS)} checks)")
sys.exit(1 if n_fail else 0)
