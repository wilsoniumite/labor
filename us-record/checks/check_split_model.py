# check_split_model.py — the two-type economy (code/split_model.py), checked before anything is fitted with it. It reads
# no variant's fit: its economies are the base fit's (results/fit_base.json, seen at breakpoint B) and the fit's 1950
# starts.
#   N  nesting: without computing (comp = 1) the split economy is the pinning model, whatever the two groups' sizes: on
#      every economy, both margins equal pinning_model.solve's threshold and every reported number equals its own
#   U  from margins well away from the one-type solution, the solver still finds it (no second equilibrium nearby)
#   I  with computing on: both markets clear, and income (wages, land rent, interest) equals consumption P_s Y
#   D  the direction computing must push: the first group's margin above the second's, its wage below, so the pay gap
#      exceeds one and the group's share of employment falls below its share of people
# Tolerances set before the first run: relative 1e-10 for nesting (the two solvers stop at 1e-15 and 1e-14), 1e-12 for
# the income identity.
# Run from us-record/:  python3 checks/check_split_model.py      Exit 0 only if every check passes.

import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "code"))
import fit_base as F  # noqa: E402
import split_model as sm  # noqa: E402

pm = sm.pm
RESULTS = []
S_N = float(1.0 - F.PANEL.loc[1964:2024, "pns_share"].mean())


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok)))
    print(f"{'PASS' if ok else 'FAIL'} {name}" + (f" — {detail}" if detail else ""))


base = json.load(open(os.path.join(ROOT, "results", "fit_base.json")))
ECON = F.economies(base["best"]["par"])                           # the base fit's 75 years
for s in F.starts():                                              # and the fit's 1950 starts
    ECON.append(F.economies(s)[0])
SIZES = (S_N, 0.05, 0.5)


def rel(a, b):
    return abs(a - b) / max(abs(b), 1e-300)


# ---- N: nesting
KEYS = [("p", "p"), ("Ps", "Ps"), ("Y", "Y"), ("K", "K"), ("Vm", "Vm"), ("participation", "participation"),
        ("labour_share_bea", "labour_share_bea"), ("theta_V", "theta_V"), ("income", "income"), ("n", "n")]
worst, worst_x = 0.0, 0.0
for e in ECON:
    q1 = pm.solve(e)
    for s_n in SIZES:
        q2 = sm.solve(e, s_n, 1.0)
        worst_x = max(worst_x, rel(q2["xr"], q1["x"]), rel(q2["xn"], q1["x"]), rel(q2["vr"], q1["v"]),
                      rel(q2["vn"], q1["v"]))
        worst = max(worst, max(rel(q2[a], q1[b]) for a, b in KEYS))
check("N1 without computing both margins and both wages equal the pinning model's (relative 1e-10), on "
      f"{len(ECON)} economies at three group sizes", worst_x < 1e-10, f"worst {worst_x:.1e}")
check("N2 ... and so do prices, output, machines, employment, labour's share, θ_V and income (relative 1e-10)",
      worst < 1e-10, f"worst {worst:.1e}")

# ---- U: away from the one-type solution
worst = 0.0
for e in ECON[::7]:
    x0 = pm.solve(e)["x"]
    for g in ((0.5 * x0, 0.5 * x0), (x0, 0.5 * x0), (0.5 * x0, x0 + 0.5 * (1.0 - x0)), (x0 + 0.5 * (1.0 - x0),) * 2):
        q2 = sm.solve(e, S_N, 1.0, guess=g)
        worst = max(worst, rel(q2["xr"], x0), rel(q2["xn"], x0))
check("U1 started from margins halfway to 0 or to 1, the solver returns the pinning model's threshold (relative 1e-10)",
      worst < 1e-10, f"worst {worst:.1e}")

# ---- I and D: computing on
COMPS = (0.9, 0.5, 0.2)
gaps, ident, direction, solved = 0.0, 0.0, True, 0
for e in ECON:
    for c in COMPS:
        try:
            q = sm.solve(e, S_N, c)
        except pm.NoEquilibrium:
            continue
        solved += 1
        gaps = max(gaps, abs(q["ndr"] / q["nsr"] - 1.0), abs(q["ndn"] / q["nsn"] - 1.0))
        ident = max(ident, abs(q["income_identity"]))
        direction &= q["xr"] > q["xn"] and q["vr"] < q["vn"] and q["pay_gap"] > 1.0 and q["routine_share"] < 1.0 - S_N
n_cases = len(ECON) * len(COMPS)
check("I1 with computing (machines needing 0.9, 0.5 or 0.2 of their service at the first group's tasks) both markets "
      "clear (relative 1e-10)", gaps < 1e-10, f"{solved} of {n_cases} economies solved; worst {gaps:.1e}")
check("I2 ... and income equals consumption, P_s Y (relative 1e-12)", ident < 1e-12, f"worst {ident:.1e}")
check("I3 ... in at least nine in ten of them", solved >= 0.9 * n_cases, f"{solved} of {n_cases}")
check("D1 in every one solved, the first group's margin is above the second's and its wage below; the pay gap exceeds "
      "one and the group's share of employment is below its share of people", direction)

n_fail = sum(not ok for _, ok in RESULTS)
print(f"\n{'ALL GREEN' if not n_fail else f'{n_fail} FAILED'} ({len(RESULTS)} checks)")
sys.exit(1 if n_fail else 0)
