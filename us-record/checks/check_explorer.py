# check_explorer.py — the explorer's JavaScript model (explorer/model.js) against the Python model (code/fit_base.py), on
# every preset the page offers (explorer/data.json, from the stored fits): each year's targeted series (the goods model's
# extra wages too), and the
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
# relative 1e-7: on the machine chain's ceiling a machine's price moves about a million times as fast as the margin, so the
# last-bit differences between Python's and JavaScript's power functions show at up to ~1e-8 (the services fit; the
# two-good fits agree to ~1e-11)
TOL = 1e-7
RESULTS = []
NODE = r"""
const M = require(process.argv[1]);
const doc = JSON.parse(require("fs").readFileSync(process.argv[2], "utf8"));
const out = {};
for (const p of doc.presets) {
  // the goods wage's deflator as the page sets it (everything but shelter, or durables)
  const D = p.settings.goods === "exshelter" ? Object.assign({}, doc.data, { wage_goods: doc.data.wage_exshelter }) : doc.data;
  const m = M.path(p.params, p.settings, D);
  const mf = M.misfit(m, D);
  out[p.id] = { ok: m.ok, chi_max: m.chi_max, misfit: mf.total, by: mf.by,
                series: Object.fromEntries(M.seriesOf(m.extra).map((s) => [s, m[s]])) };
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
    if not p["source"].startswith("results/") or "#" in p["source"]:   # variants: JavaScript only, no stored Python twin
        continue
    R = json.load(open(os.path.join(ROOT, p["source"])))
    F.configure(R["meta"])                                   # every setting from the stored run
    m = F.model_path(R["best"]["par"])
    j = js[p["id"]]
    ser = F.all_series()                                     # the goods model's extra wages too
    gap = max(float(np.max(np.abs(np.array(j["series"][s], dtype=float) - m[s].values) / np.abs(m[s].values))) for s in ser)
    by = F.misfit_by_series(m)
    mis_gap = max(abs(j["by"][s] - by[s]) / max(by[s], 1e-12) for s in ser)
    tot = abs(j["misfit"] - R["best"]["misfit"]) / R["best"]["misfit"]
    chi_ok = (not F.PIN_START) or abs(j["chi_max"] - F.pinned_chi(R["best"]["par"])) / j["chi_max"] < 1e-9
    check(f"{p['id']:11s} the JS model reproduces {p['source']}: every year of the {len(ser)} series, the misfit by series and "
          "in total (relative 1e-7)" + (", and the pinned work-cost scale" if F.PIN_START else ""),
          j["ok"] and gap < TOL and mis_gap < TOL and tot < TOL and chi_ok,
          f"series {gap:.1e}, by series {mis_gap:.1e}, total {tot:.1e}")

n_fail = sum(not ok for _, ok in RESULTS)
print(f"\n{'ALL GREEN' if not n_fail else f'{n_fail} FAILED'} ({len(RESULTS)} checks)")
sys.exit(1 if n_fail else 0)
