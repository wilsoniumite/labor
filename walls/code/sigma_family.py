# sigma_family.py — the backward calibration leaves the schedule's shape one degree of freedom: in the scale-free
# power family gamma = c + x^k, every k above 3.88 meets the calibration condition with its own c (Appendix B's two
# roots are the two k where c/(1 + c) = 0.01). Along the family: sigma at the margin, the distance to the soft wall, and
# what Figure 3's experiments do. Then the family member at each literature value of sigma.
# Run from walls/:  python code/sigma_family.py
import json
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq
from tqdm.auto import tqdm

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import model as m  # noqa: E402

X = m.margin_from_targets()


def experiments(k):
    """Calibrate the family member k and run Figure 3's experiments plus automation landing on labor's tasks."""
    s = m.power_family(k)
    P = m.calibrate(s)
    q = m.solve(P)
    out = dict(k=k, c=float(s["g"](0.0)), ratio=float(s["g"](1.0) / s["g"](0.0)), sigma=m.sigma_margin(P, q["x"]),
               x_c=q["x_c"], gap=q["x_c"] - q["x"], share_behind=(1 - q["x_c"]) / (1 - q["x"]), w0=q["real_wage"])
    runs = {"task_uniform": {**P, "sched": m.scaled(s, 0.5)},              # Figure 3: gamma halved everywhere
            "recursive": {**P, "lam": 0.0},                                # Figure 3: no labor in the machine chain
            "task_labor": {**P, "sched": m.flattened(s, q["x"], 0.5)}}     # gamma halved above the margin only
    for name, Q in runs.items():
        e = m.solve(Q)
        out[name] = e["real_wage"] / q["real_wage"] - 1
        out[name + "_part"] = e["participation"]
    return out


if __name__ == "__main__":
    # a numerical check of the closed-form sigma on one member: d ln(J/(1-x)) / d ln gamma(x) at the margin
    s = m.power_family(10.0)
    h = 1e-6
    lnML = lambda x: np.log(s["J"](x) / (1 - x))
    num = (lnML(X + h) - lnML(X - h)) / (np.log(s["g"](X + h)) - np.log(s["g"](X - h)))
    print(f"sigma check (k 10): closed form {m.sigma_margin(m.calibrate(s), X):.6f}, numerical {num:.6f}")

    ks = np.concatenate([np.linspace(3.95, 10, 40), np.linspace(10.2, 60, 60)])
    rows = [experiments(k) for k in tqdm(ks, desc="family")]
    for r in rows[::10]:
        print(f"k {r['k']:6.2f}  c {r['c']:.5f}  ratio {r['ratio']:8.1f}  sigma {r['sigma']:.3f}  gap to soft wall "
              f"{r['gap']:.3f} ({r['share_behind']:.0%} of labor's tasks behind it)  task uniform {r['task_uniform']:+.1%}"
              f"  task on labor {r['task_labor']:+.1%}  recursive {r['recursive']:+.1%}")
    # where uniform task automation changes sign
    f = lambda k: experiments(k)["task_uniform"]
    k0 = brentq(f, 4.0, 40.0, xtol=1e-6)
    print(f"uniform task automation leaves w/P_s unchanged at k {k0:.3f}, sigma {experiments(k0)['sigma']:.3f}")

    # the member at each literature value of sigma
    sig = lambda k: experiments(k)["sigma"]
    lit = {"Gechert et al. corrected mean": 0.3, "Chirinko low": 0.4, "Chirinko high / O&R low": 0.6,
           "Oberfield-Raval high": 0.7, "Gechert et al. raw mean": 0.9, "Karabarbounis-Neiman": 1.25}
    picks = {}
    for name, target in lit.items():
        k = brentq(lambda kk: sig(kk) - target, 3.95, 400.0, xtol=1e-6)
        r = experiments(k)
        picks[name] = r
        print(f"sigma {target:4.2f} ({name}): k {k:7.2f}, ratio {r['ratio']:9.1f}, gap {r['gap']:.4f}, "
              f"{r['share_behind']:.0%} of labor's tasks behind the soft wall; task uniform {r['task_uniform']:+.1%}, "
              f"task on labor {r['task_labor']:+.1%}, recursive {r['recursive']:+.1%}")
    (HERE.parent / "results").mkdir(exist_ok=True)
    json.dump(dict(family=rows, literature=picks, sign_change_k=k0), open(HERE.parent / "results" / "sigma_family.json", "w"),
              indent=1, default=float)
    print("wrote results/sigma_family.json")
