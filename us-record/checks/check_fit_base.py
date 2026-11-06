# check_fit_base.py — Phase 2's fit (results/fit_base.json, from code/fit_base.py), checked for breakpoint B:
#   T  the tolerances and targets are the ones committed before the first fit ran (commit 72adc83), unchanged
#   R  the stored fit reproduces: re-solving every year at the stored parameters gives the stored path, and its misfit
#   E  every year of the fit is an interior equilibrium of the pinning model (labour demand equals supply)
#   S  the search: every start ended in a convergence status, and the reported best is the least misfit of them all; a
#      variant that nests the model it extends (the split at g_c = 0) is no worse than it, or its search failed
#   A  the accounting diagnostic: where it found a capability path, it reproduces the fork in that year
# A variant (decision 13, the blind protocol): python3 checks/check_fit_base.py --results fit_A --blind prints PASS or FAIL
# only, no fit numbers; the variant's settings (A's shelter, the split and its free numbers) are read from its results
# file. For the split, E1 asks both groups' markets to clear. Model B's switches (the goods deflator, women's entry, the
# set return, waves) are read from the results file too (fit_base.configure).
# Run from us-record/:  python3 checks/check_fit_base.py      Exit 0 only if every check passes.

import json
import os
import re
import subprocess
import sys

import numpy as np
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(ROOT)
sys.path.insert(0, os.path.join(ROOT, "code"))
import fit_base as F  # noqa: E402

ARGS = sys.argv[1:]
NAME = ARGS[ARGS.index("--results") + 1] if "--results" in ARGS else "fit_base"
BLIND = "--blind" in ARGS
R = json.load(open(os.path.join(ROOT, "results", f"{NAME}.json")))
F.configure(R["meta"])                                      # every setting from the stored run (fit_base.configure)
RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok)))
    print(f"{'PASS' if ok else 'FAIL'} {name}" + (f" — {detail}" if detail and not BLIND else ""))


# ---- T: the tolerances as committed before the fit
src = subprocess.run(["git", "show", "72adc83:us-record/code/fit_base.py"], cwd=REPO, capture_output=True,
                     text=True).stdout
pre = {name: re.search(rf"^{name} = (.+)$", src, re.M).group(1) for name in ("SERIES", "TOL_LOG", "TOL_LEVEL", "YEARS")}
now = {name: re.search(rf"^{name} = (.+)$", open(os.path.join(ROOT, "code", "fit_base.py")).read(), re.M).group(1)
       for name in pre}
check("T1 the targets, years and tolerances are byte for byte those committed before the first fit (72adc83)",
      pre == now, "; ".join(f"{k} = {v}" for k, v in now.items()))
check("T2 the stored run used them", R["meta"]["tol_log"] == F.TOL_LOG and R["meta"]["tol_level"] == F.TOL_LEVEL
      and R["meta"]["series"] == F.SERIES)

# ---- R: reproduction
par = R["best"]["par"]
m = F.model_path(par)
stored = pd.DataFrame(R["path"], index=F.YEARS)
gap = max(float(np.nanmax(np.abs(m[c].values - stored[c].values) / np.maximum(np.abs(stored[c].values), 1e-12)))
          for c in stored.columns)
check("R1 re-solving every year at the stored parameters gives the stored path (relative 1e-9)", gap < 1e-9, f"{gap:.1e}")
mis = float(np.sum(F.residuals(F.pack(par)) ** 2))
check("R2 the stored misfit recomputes (1e-9)", abs(mis - R["best"]["misfit"]) < 1e-9 * max(1.0, mis),
      f"{mis:.6f} vs {R['best']['misfit']:.6f}")
by = F.misfit_by_series(m)
check("R3 the misfit is the mean of the five series' misfits", abs(np.mean(list(by.values())) - mis) < 1e-9 * max(1, mis),
      ", ".join(f"{k} {v:.2f}" for k, v in by.items()))

# ---- E: equilibria
worst = 0.0
if F.SPLIT_FROM is None:
    p_ref = None if F.SIGMA is None else F.pm.solve(F.economies(par)[0])["p"]   # as model_path finds it
    for e in F.economies(par, p_ref=p_ref):
        q = F.pm.solve(e)
        worst = max(worst, abs(q["nD"] - q["nS"]) / q["nD"])
else:
    for i, e in enumerate(F.economies(par)):                 # the stored margins, put back into the split's equations
        comp = float(np.exp(-par["g_c"] * max(0.0, F.YEARS[i] - F.SPLIT_FROM)))
        q = F.sm.parts(e, F.S_N, comp, stored["x"].iloc[i], stored["xn"].iloc[i])
        worst = max(worst, abs(q["ndr"] - q["nsr"]) / q["ndr"], abs(q["ndn"] - q["nsn"]) / q["ndn"])
check("E1 every year is an interior equilibrium: labour demand equals supply (relative 1e-9)", worst < 1e-9, f"{worst:.1e}")

# ---- S: the search
check("S1 every start ended in a convergence status (scipy least_squares status 1-4)",
      all(s["status"] in (1, 2, 3, 4) for s in R["starts"]), str(sorted({s["status"] for s in R["starts"]})))
check("S2 the reported best is the least misfit of all starts", R["best"]["misfit"] == min(s["misfit"] for s in R["starts"]),
      f"{len(R['starts'])} starts")

if R["meta"].get("ref") and F.SPLIT_FROM is not None:     # the split nests the model it extends (at g_c = 0)
    REF = json.load(open(os.path.join(ROOT, "results", f"{R['meta']['ref']}.json")))
    check(f"S3 the best is no worse than {R['meta']['ref']}, the model it extends and nests (relative 1e-6)",
          R["best"]["misfit"] <= REF["best"]["misfit"] * (1.0 + 1e-6))

# ---- A: the accounting diagnostic
if R["accounting_eta"] is None:
    print("---- A1 not run: the accounting diagnostic reads the base model's mapping of shelter, not this variant's")
else:
    acc = pd.Series(R["accounting_eta"], index=F.YEARS, dtype=float)
    fork = (F.D["wage_goods"] / F.D["wage_shelter"])
    p1950 = m.loc[1950, "p"]
    err = []
    for y in acc.dropna().index:
        e = F.economies(par)[F.YEARS.index(y)]
        q = F.pm.solve(F.replace(e, eta=float(acc[y])))
        err.append(abs(np.log(p1950 / q["p"]) - np.log(fork[y])))
    check("A1 where the accounting found a capability path, it reproduces that year's fork (log 1e-9)",
          max(err) < 1e-9, f"{acc.notna().sum()} of {len(acc)} years; worst {max(err):.1e}")

n_fail = sum(not ok for _, ok in RESULTS)
print(f"\n{'ALL GREEN' if not n_fail else f'{n_fail} FAILED'} ({len(RESULTS)} checks)")
sys.exit(1 if n_fail else 0)
