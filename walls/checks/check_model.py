# check_model.py — gates for walls/code/model.py: the plug-in solver reproduces pinning/code/appendix_b.py on the
# printed instance, Figure 3's economies and the automation path; the closed-form calibration hits its seven targets
# on both roots of the power family; a hard wall above the margin leaves the calibrated equilibrium unchanged.
# Run from walls/:  python checks/check_model.py
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "code"))
sys.path.insert(0, str(HERE.parents[1] / "pinning" / "code"))
import appendix_b as ab  # noqa: E402
import model as m  # noqa: E402

ok = []


def gate(name, cond):
    ok.append(bool(cond))
    print(f"[{'PASS' if cond else 'FAIL'}] {name}")


# 1. equivalence with appendix_b
for label, Pab in (("printed", ab.PRINTED), ("recursive", {**ab.PRINTED, "lam": 0.0}),
                   ("task", {**ab.PRINTED, "eta": 0.5}), ("path eta 0.01", ab.sequence(ab.PRINTED, 0.01)),
                   ("ceiling test economy", ab.TEST_ECONOMIES["ceiling"])):
    a, b = ab.solve(Pab), m.solve(m.appendix_b_economy(Pab))
    gate(f"{label}: x*, x_c, v, w/P_s, participation match appendix_b",
         np.allclose([a["x"], a["x_ceiling"], a["v"], a["real_wage"], a["participation"]],
                     [b["x"], b["x_c"], b["v"], b["real_wage"], b["participation"]], rtol=1e-8, atol=1e-11))

# 2. the closed-form calibration
x = m.margin_from_targets()
gate("x* = 0.83 from participation, chain share and baskets", abs(x - 0.83) < 1e-12)
ks = np.linspace(3.9, 40, 4000)
cs = [m.power_c_of_k(k) for k in ks]
gate("the scale-free power family meets the condition for every k above 3.88", all(c is not None for c in cs))
for k in (4.355, 15.498):
    # appendix_b's family keeps g0 = 0.01, g1 = 0.99; find its k root near each value and compare
    from scipy.optimize import brentq
    f = lambda kk: (0.01 * x + 0.99 * x ** (kk + 1) / (kk + 1)) - (0.01 + 0.99 * x ** kk) * (1 - x)
    kr = brentq(f, k - 0.5, k + 0.5)
    P = m.calibrate(m.power(0.01, 0.99, kr))
    q = m.solve(P)
    hit = np.allclose([q["x"], q["theta_V"], cpt_a := m.cpt(P) * P["a"], q["labor_share_basket"], q["site_share"],
                       q["chain_share"], q["participation"], q["Y"]],
                      [0.83, 0.47, 0.20, 0.47, 0.06, 0.15, 0.60, 3.0], rtol=1e-7)
    gate(f"root k = {kr:.3f} (g0 0.01): the solved equilibrium hits all seven targets", hit)
    gate(f"root k = {kr:.3f}: soft wall at gamma(x_c)/gamma(x*) = 1.702",
         abs(float(P["sched"]["g"](q["x_c"])) / q["gamma"] - m.soft_wall_multiple()) < 1e-6)
    # 3. a hard wall above the margin changes nothing in the calibrated equilibrium
    for xH in (0.95, 0.9, 0.85):
        qH = m.solve({**P, "xH": xH})
        gate(f"root k = {kr:.3f}, hard wall at {xH}: same equilibrium", abs(qH["x"] - q["x"]) < 1e-10
             and abs(qH["real_wage"] - q["real_wage"]) < 1e-10)

# 4. the printed instance's rounded parameters sit next to the low root
q = m.solve(m.appendix_b_economy(ab.PRINTED))
gate("printed instance: x* 0.82987, x_c 0.94634 (Appendix B's numbers)",
     abs(q["x"] - 0.82987) < 5e-6 and abs(q["x_c"] - 0.94634) < 5e-6)

print(f"{sum(ok)}/{len(ok)} passed")
sys.exit(0 if all(ok) else 1)
