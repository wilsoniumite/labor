# europe_run.py — 'The European real-data run of LR-K2 and LR-Y0 (exploratory, no verdict)' (PROTOCOL section 5, L3).
#
# The two long-run specifications run ONCE on the frozen European panel (data already seen: the European look's
# confirm-half cache, read by skeleton.european_frames), from a commit in which longrun/code/specs.py and
# longrun/PROTOCOL.md are committed and unchanged; their SHA-256 and the commit are written to the output, and the
# output's existence is checked so that a second run needs --amendment (a recorded pre-freeze amendment: every run is
# reported). European q is C6's log(CP041 / IGD_NNRG) lagged; F is C9's F split at the median by specs.compute_H; the
# knots lie inside each country's longest European q piece (C3's q breaks), on the rows D1 used at the look (1997 on;
# these are seen cells, so the knots are computed with unseen_only=False: the long-run unseen-cell filter would
# otherwise leave every European country without knots).
# The point estimates are committed with the freeze, labelled exploratory and no-verdict, and both forecasters see them.
#
# Run from longrun/ (after committing specs.py and PROTOCOL.md):  ../../venv/Scripts/python.exe code/europe_run.py
# Out: results/europe_run_<HEAD short>.json

from __future__ import annotations

import glob
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
LROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import fetch  # noqa: E402
import skeleton  # noqa: E402
import specs  # noqa: E402

RESULTS = os.path.join(LROOT, "results")
EUROPE_FIRST = 1997                      # the European look's first observation year (its q from 1996, lagged)


def sha(path: str) -> str:
    return hashlib.sha256(open(path, "rb").read().replace(b"\r\n", b"\n")).hexdigest()


def committed_unchanged() -> str:
    """The HEAD commit, if code/specs.py and PROTOCOL.md are committed and unchanged; else refuse."""
    for p in ("code/specs.py", "PROTOCOL.md"):
        rc, out = fetch._git("ls-files", "--", p)
        if rc != 0 or not out.strip():
            raise SystemExit(f"{p} is not committed: commit it first (PROTOCOL section 5)")
        if fetch._git("diff", "--quiet", "HEAD", "--", p)[0] != 0:
            raise SystemExit(f"{p} has uncommitted changes: commit them first")
    rc, out = fetch._git("rev-parse", "--short", "HEAD")
    return out.strip()


def european_data() -> specs.Data:
    cy, cl, _ = skeleton.european_frames()
    par = skeleton.european_parameters()
    esk = skeleton.european_skeleton(par)
    d = cy.reset_index()
    d = d[[c in esk["countries"] for c in d["geo"]]].copy()
    rows = []
    for c, v in esk["countries"].items():
        e = d[(d["geo"] == c)].copy()
        e["qseg_l1"] = [v["chosen"][0] if v["chosen"] and t in set(v["ranking"]) else -1 for t in e["year"]]
        e["A2534__breaks"] = e["A2534__breaks"]
        e["U"] = e["U"]
        rows.append(e)
    e = pd.concat(rows, ignore_index=True)
    e = e[e["year"] >= EUROPE_FIRST].set_index(["geo", "year"])     # the European look's D1 rows only (seen)
    kn = specs.knots(e[["logq_l1", "qseg_l1"]], {c: tuple(v["chosen"]) for c, v in esk["countries"].items()
                                                if v["chosen"]}, unseen_only=False)
    for col in ("A2534_M", "A2534_F", "strict", "cohort", "school2024"):
        if col not in e:
            e[col] = np.nan
            e[col + "__breaks"] = [[] for _ in range(len(e))]
    cl2 = pd.DataFrame(index=sorted(esk["countries"]))
    cl2["F_L"] = [float(cl.loc[c, "F_raw"]) if c in cl.index else np.nan for c in cl2.index]
    return specs.Data(e, cl2, {"q": kn}, esk["H_fixed"], {"K2": esk["members"]["K2"], "Y0": esk["members"]["Y0"]})


def main() -> None:
    head = committed_unchanged()
    prior = sorted(glob.glob(os.path.join(RESULTS, "europe_run_*.json")))
    if prior and "--amendment" not in sys.argv:
        raise SystemExit(f"the European run exists ({prior}); a rerun is a recorded pre-freeze amendment: --amendment")
    data = european_data()
    M = specs.basis_frame(data, sorted(data.H), "A2534")
    k2 = specs.k2_core(M, data.H, R=9999)
    y0 = specs.simple_test(data, "LR-Y0", data.members["Y0"])
    out = {"what": "European real-data run of LR-K2 and LR-Y0: exploratory, no verdict (PROTOCOL section 5)",
           "head": head, "utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
           "sha256": {"code/specs.py": sha(os.path.join(HERE, "specs.py")),
                      "PROTOCOL.md": sha(os.path.join(LROOT, "PROTOCOL.md"))},
           "amendment": bool(prior), "previous_runs": [os.path.basename(p) for p in prior],
           "LR-K2": specs.clean_json({k: v for k, v in k2.items() if k != "country_fits"}),
           "LR-Y0": specs.clean_json(y0), "H": data.H}
    os.makedirs(RESULTS, exist_ok=True)
    path = os.path.join(RESULTS, f"europe_run_{head}.json")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(out, f, indent=1)
    print(f"LR-K2 DiD {k2['beta']:.3f} (p {k2['p_stat']:.3f}); LR-Y0 g1 {y0['beta']:.3f} (p {y0['p']:.3f}); "
          f"wrote {path} — exploratory, no verdict; commit it with the freeze")


if __name__ == "__main__":
    main()
