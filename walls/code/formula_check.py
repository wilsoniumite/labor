# formula_check.py — is "labor sits just short of the soft wall" a power-family artifact? To first order the share of
# labor's tasks still contestable (between the margin and the soft wall) is
#     (x_c - x*)/(1 - x*)  ~  s_M * sigma * ln(1/theta),      s_M = R/(1 + R), the machine share of final-task cost,
# because the soft wall sits ln(1/theta) above the margin in log gamma, the schedule's log-slope there is gamma'/gamma,
# and sigma = (1 + 1/R)(gamma/gamma')/(1 - x*) at the calibration. Three measurable numbers. Checked here on the power
# family (results/sigma_family.json) and on a second family, gamma = c + exp(beta x), calibrated the same way.
# Run from walls/:  python code/formula_check.py
import json
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import model as m  # noqa: E402

X, R = m.margin_from_targets(), m.R_of()
THETA = 1 / m.soft_wall_multiple()
SM = R / (1 + R)


def predicted(sigma):
    return SM * sigma * np.log(1 / THETA)


fam = json.load(open(HERE.parent / "results" / "sigma_family.json"))
print("power family: sigma, contestable share actual vs s_M sigma ln(1/theta)")
for r in fam["family"][::12]:
    print(f"   sigma {r['sigma']:.3f}: actual {1 - r['share_behind']:.3f}, formula {predicted(r['sigma']):.3f}")


def exp_family(beta):
    """gamma = c + exp(beta x) with the c that meets the calibration condition (None if c <= 0)."""
    e = np.exp(beta * X)
    c = (R * e * (1 - X) - (e - 1) / beta) / (X - R * (1 - X))
    if c <= 0:
        return None
    return dict(g=lambda x: c + np.exp(beta * np.asarray(x)), J=lambda x: c * x + (np.exp(beta * np.asarray(x)) - 1) / beta,
                dg=lambda x: beta * np.exp(beta * np.asarray(x)), name=f"c + exp({beta:.3g} x), c = {c:.4g}")


betas = [b for b in np.linspace(1.0, 120.0, 2000) if exp_family(b) is not None]
print(f"exponential family: c > 0 for beta in [{betas[0]:.2f}, {betas[-1]:.2f}] on the grid")
rows = []
for target in (0.3, 0.6, 0.9, 1.25, 2.0):
    sig = lambda b: m.sigma_margin(m.calibrate(exp_family(b)), X) - target
    lo = [b for b in betas if sig(b) * sig(betas[-1]) < 0]
    try:
        b = brentq(sig, betas[0], betas[-1], xtol=1e-9)
    except ValueError:
        print(f"   sigma {target}: not reached in this family")
        continue
    P = m.calibrate(exp_family(b))
    q = m.solve(P)
    actual = (q["x_c"] - q["x"]) / (1 - q["x"])
    tu = m.solve({**P, "sched": m.scaled(P["sched"], 0.5)})["real_wage"] / q["real_wage"] - 1
    rows.append(dict(sigma=target, beta=b, contestable=actual, formula=predicted(target), task_uniform=tu))
    print(f"   sigma {target}: beta {b:.2f}, contestable share actual {actual:.3f}, formula {predicted(target):.3f};"
          f" Figure 3's uniform task automation {tu:+.1%}")
json.dump(rows, open(HERE.parent / "results" / "formula_check.json", "w"), indent=1)
