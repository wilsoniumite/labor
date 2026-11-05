# check_pinning_model.py — the pinning model (code/pinning_model.py) as the paper uses it (2026-11-05): the printed instance
# is the calibration of its shares, rounded, and code/appendix_b.py solves with the model rather than beside it.
#   K  the seven shares (appendix_b.SHARES) have exactly two roots in the schedule's convexity k, and each root's solved
#      equilibrium hits all seven
#   R  PRINTED is the low root, each parameter rounded to the digits printed; the set parameters equal exactly
#   S  appendix_b.solve and pinning_model.solve find the same threshold, bit for bit, on every economy the paper and its
#      checks use: the printed instance, Figure 3's economies, the automation path, the test economies
#   H  what the two roots do under task automation (gamma halved): the low root lowers w/P_s and participation, the high
#      root raises both (the reason the low root is the reading; Appendix B's comment)
#   Q  the rounded instance's shares as appendix_b.py's comment quotes them
# Run from pinning/:  python3 checks/check_pinning_model.py      Exit 0 only if every check passes.

import sys
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
import appendix_b as B  # noqa: E402
import pinning_model  # noqa: E402

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok)))
    print(f"{'PASS' if ok else 'FAIL'} {name}" + (f" — {detail}" if detail else ""))


def half_unit(printed):
    """Half a unit in the last digit printed: 0.0017 -> 0.00005, 7.3 -> 0.05, 0.09 -> 0.005."""
    return 0.5 * 10.0 ** Decimal(repr(printed)).as_tuple().exponent


roots = B.calibrated()
check("K1 the seven shares have exactly two roots in k, 4.36 and 15.5 to the digits appendix_b.py quotes",
      len(roots) == 2 and round(roots[0][0].k, 2) == 4.36 and round(roots[1][0].k, 1) == 15.5,
      ", ".join(f"k {e.k:.6f}" for e, _ in roots))
for e, info in roots:
    res = pinning_model.target_residuals(e, B.SHARES)
    check(f"K2[k {e.k:.2f}] its solved equilibrium hits all seven shares (largest miss below 1e-10)",
          max(abs(v) for v in res.values()) < 1e-10, ", ".join(f"{k} {v:.1e}" for k, v in res.items()))

lo = roots[0][0]
SET = ("N", "b", "delta", "g0", "g1", "eta")
for key in B.KEYS:
    want = getattr(lo, key)
    if key in SET:
        check(f"R1[{key}] set, not solved: PRINTED's {B.PRINTED[key]} is the calibration's", B.PRINTED[key] == want)
    else:
        gap = abs(B.PRINTED[key] - want)
        check(f"R2[{key}] PRINTED's {B.PRINTED[key]} is the low root's {want:.6g} rounded to the digits printed",
              gap <= half_unit(B.PRINTED[key]), f"|gap| {gap:.3g} <= {half_unit(B.PRINTED[key]):.3g}")

economies = {"printed": B.PRINTED, **{f"fig3 {s}": B.scenario(B.PRINTED, s) for s, _ in B.SCENARIOS},
             "path eta 1": B.sequence(B.PRINTED, 1.0), "path eta 0.01": B.sequence(B.PRINTED, 0.01),
             **{f"test {k}": P for k, P in B.TEST_ECONOMIES.items()},
             **{f"root k {e.k:.2f}": {k: getattr(e, k) for k in B.KEYS} for e, _ in roots}}
for name, P in economies.items():
    a, b = B.solve(P), pinning_model.solve(B.economy(P))
    check(f"S1[{name}] appendix_b.solve and pinning_model.solve: the same threshold, bit for bit, and the same "
          f"participation", a["x"] == b["x"] and a["participation"] == b["participation"], f"x* {a['x']:.12f}")

for e, _ in roots:
    P = {k: getattr(e, k) for k in B.KEYS}
    base, task = B.solve(P), B.solve(B.scenario(P, "task"))
    up = task["real_wage"] > base["real_wage"] and task["participation"] > base["participation"]
    down = task["real_wage"] < base["real_wage"] and task["participation"] < base["participation"]
    want = "lowers" if e is lo else "raises"
    check(f"H1[k {e.k:.2f}] task automation {want} w/P_s and participation",
          down if e is lo else up,
          f"w/P_s {base['real_wage']:.4f} -> {task['real_wage']:.4f}, N_a/N {base['participation']:.4f} -> "
          f"{task['participation']:.4f}")

q = B.solve(B.PRINTED)
sh = B.shares(B.PRINTED, q)
quoted = dict(theta_V=("0.456", sh["theta_V"]), machines=("0.196", sh["machines"]), labor=("0.469", sh["labor"]),
              site=("0.065", sh["site"]), chain=("0.148", sh["chain"]), participation=("0.602", q["participation"]),
              baskets=("3.01", q["Y"] / B.PRINTED["N"]))
for name, (text, value) in quoted.items():
    digits = len(text.split(".")[1])
    check(f"Q1[{name}] the rounded instance's {name} reads {text}", f"{value:.{digits}f}" == text, f"{value:.6f}")

n_fail = sum(not ok for _, ok in RESULTS)
print(f"\n{'ALL GREEN' if not n_fail else f'{n_fail} FAILED'} ({len(RESULTS)} checks)")
sys.exit(1 if n_fail else 0)
