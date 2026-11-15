# flip_check.py — an independent read of sigma from the companion thread's revealed-adoption envelope
# (../companion/data). In the backward calibration (R = 1) the share of labor's employment that flips to machines per
# log point of w/p_m at the margin is (gamma/gamma')/(1 - x*) = sigma/2. The envelope reports the share of 1999
# employment flipped by 2025 under three share-decline rules and six w/c waterline members; mass over the waterline's
# log rise, times two, is a sigma. Caveats, both directions: occupational flips miss within-occupation automation (sigma
# read low); flips caused by gamma falling are charged to the waterline (sigma read high); w/c is not w/p_m.
# Run from walls/:  python code/flip_check.py
import csv
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
C = HERE.parents[1] / "companion" / "data"
grid = list(csv.DictReader(open(C / "wc_grid.csv")))
first, last = grid[0], grid[-1]
members = [k for k in first if k not in ("year",)]
mass = {}
for rule in ("d30", "d40", "d50"):
    rows = list(csv.DictReader(open(C / f"flips_{rule}.csv")))
    base = sum(float(r["emp_base"]) for r in rows)
    flipped = sum(float(r["emp_base"]) for r in rows if r["flipped"] == "True")
    mass[rule] = flipped / base
print("flipped share of 1999 employment by 2025: " + ", ".join(f"{k} {v:.3f}" for k, v in mass.items()))
out = {}
for mem in members:
    rise = np.log(float(last[mem]) / float(first[mem]))
    sig = {rule: 2 * mm / rise for rule, mm in mass.items()}
    out[mem] = dict(log_rise=rise, **sig)
    print(f"{mem:22s} w/c x{np.exp(rise):5.2f} (log {rise:.2f}): sigma " +
          ", ".join(f"{r} {s:.2f}" for r, s in sig.items()))
allsig = [v for d in out.values() for k, v in d.items() if k != "log_rise"]
print(f"range over 6 members x 3 rules: sigma {min(allsig):.2f}-{max(allsig):.2f}; median {np.median(allsig):.2f}")
json.dump(dict(mass=mass, members=out), open(HERE.parent / "results" / "flip_check.json", "w"), indent=1)
