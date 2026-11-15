# landing.py — where automation lands. Figure 3's task automation halves gamma at every task; machines can instead get
# better at the tasks they already hold, at labor's contestable band, or behind the soft wall. Each experiment
# multiplies chosen tasks' gamma by 0.5 and re-sorts the schedule (model.resorted). Run on the calibrated family members
# at the low root, at literature sigma, and at the high root. Then three long paths to eta -> 0.
# Run from walls/:  python code/landing.py
import json
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq
from tqdm.auto import tqdm

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import model as m  # noqa: E402


def member(sigma=None, k=None):
    if k is None:
        k = brentq(lambda kk: m.sigma_margin(m.calibrate(m.power_family(kk)), m.margin_from_targets()) - sigma,
                   3.95, 400.0, xtol=1e-8)
    s = m.power_family(k)
    P = m.calibrate(s)
    return P, m.solve(P)


def landing(P, q, eta=0.5):
    s, x0, xc = P["sched"], q["x"], q["x_c"]
    where = {"everywhere (Figure 3)": lambda x: np.full_like(x, eta),
             "machine tasks only": lambda x: np.where(x < x0, eta, 1.0),
             "labor's contestable band": lambda x: np.where((x >= x0) & (x < xc), eta, 1.0),
             "behind the soft wall": lambda x: np.where(x >= xc, eta, 1.0),
             "all of labor's tasks": lambda x: np.where(x >= x0, eta, 1.0)}
    out = {}
    base = m.solve({**P, "sched": m.resorted(s, lambda x: np.ones_like(x))})
    out["resort check (no change)"] = (base["real_wage"] / q["real_wage"] - 1, base["participation"], base["x"])
    for name, mult in where.items():
        e = m.solve({**P, "sched": m.resorted(s, mult)})
        out[name] = (e["real_wage"] / q["real_wage"] - 1, e["participation"], e["x"])
    return out


def path(P, q, kind, etas):
    """Long paths. 'paper': Appendix B's path (lambda 0, gamma scaled by eta). 'no recursive': gamma scaled by eta,
    lambda kept. 'labor tasks': machines improve only at the tasks labor held at the start, lambda kept."""
    s, x0 = P["sched"], q["x"]
    res = []
    for eta in etas:
        if kind == "paper":
            Q = {**P, "lam": 0.0, "sched": m.scaled(s, eta)}
        elif kind == "no recursive":
            Q = {**P, "sched": m.scaled(s, eta)}
        else:
            Q = {**P, "sched": m.resorted(s, lambda x: np.where(x >= x0, eta, 1.0))}
        e = m.solve(Q)
        res.append((eta, e["real_wage"], e["participation"], e["x"], e["x_c"]))
    return res


if __name__ == "__main__":
    members = {"low root (sigma 2.29)": member(k=None, sigma=2.2932),
               "sigma 1.25": member(sigma=1.25),
               "sigma 0.6": member(sigma=0.6),
               "high root (sigma 0.744)": member(sigma=0.7440),
               "sigma 0.3": member(sigma=0.3)}
    record = {}
    for name, (P, q) in members.items():
        print(f"--- {name}: x* {q['x']:.4f}, x_c {q['x_c']:.4f}, w/P_s {q['real_wage']:.3f}")
        out = landing(P, q)
        for k, (dw, part, x) in out.items():
            print(f"    {k:28s} w/P_s {dw:+7.1%}   participation {part:.3f}   x* {x:.4f}")
        record[name] = dict(landing=out)
    etas = [1.0, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01]
    for name in ("low root (sigma 2.29)", "sigma 0.6"):
        P, q = members[name]
        for kind in ("paper", "no recursive", "labor tasks"):
            res = path(P, q, kind, tqdm(etas, desc=f"{name}: {kind}", leave=False))
            print(f"    {name:22s} {kind:13s}: " + "; ".join(f"eta {e}: {w:.2f}/{n:.3f}" for e, w, n, x, xc in res)
                  + "   (w/P_s / participation)")
            record[name][f"path {kind}"] = res
    json.dump(record, open(HERE.parent / "results" / "landing.json", "w"), indent=1, default=float)
    print("wrote results/landing.json")
