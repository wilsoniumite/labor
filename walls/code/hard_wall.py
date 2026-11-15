# hard_wall.py — a hard wall H = [xH, 1] (law, preference or capability) on the calibrated economy: invisible to the
# backward calibration, decisive along Appendix B's automation path (lambda 0, gamma x eta). On the low root and at
# literature sigma. The participation floor as eta -> 0 is |H| times the baskets a person that land allows once machine
# work is free, T/h (output is land-limited; every basket needs |H| of human time with tasks in fixed proportion).
# Run from walls/:  python code/hard_wall.py
import json
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import model as m  # noqa: E402

X = m.margin_from_targets()


def member(sigma):
    k = brentq(lambda kk: m.sigma_margin(m.calibrate(m.power_family(kk)), X) - sigma, 3.95, 400.0, xtol=1e-8)
    return m.calibrate(m.power_family(k))


etas = [1.0, 0.3, 0.1, 0.03, 0.01, 0.001]
record = {}
for name, P in (("low root (sigma 2.29)", member(2.2932)), ("sigma 0.6", member(0.6))):
    print(f"--- {name}: T/h = {P['T'] / P['h']:.3f} baskets a person once machine work is free")
    record[name] = {}
    for H in (0.0, 0.02, 0.05, 0.10, 0.15):
        row = []
        for eta in etas:
            Q = {**P, "lam": 0.0, "sched": m.scaled(P["sched"], eta), "xH": 1.0 - H}
            e = m.solve(Q)
            row.append((eta, e["participation"], e["real_wage"], e["regime"]))
        record[name][H] = row
        print(f"    |H| {H:.2f}: " + "; ".join(f"{eta:g}: {n:.3f}/{w:.2f}{'*' if r == 'only H' else ''}"
                                         for eta, n, w, r in row) + f"   floor (T/h)|H| = {P['T'] / P['h'] * H:.3f}")
json.dump(record, open(HERE.parent / "results" / "hard_wall.json", "w"), indent=1, default=str)
print("participation / w/P_s at each eta; * = labor holds only H. Wrote results/hard_wall.json")
