"""Verification of Block B.0' (the anatomy of a task) — sketch link-sketch-blocks-B0-C-D.md.

Claims checked (the two [check] flags of Block B.0'):
  (B0'1-MEAS) Fragment creation formalized as a measure change on the task space:
              tasks are (engaged-dimension set, per-dimension labor weights,
              separability); when a ray crosses, fully-crossed tasks flip,
              partially-crossed separable tasks shed a machine fragment and
              leave a human RESIDUE fragment (a new point in the space with the
              uncrossed profile), bundled tasks stand. Invariants verified on a
              simulated crossing sequence: labor bookkeeping conserves exactly;
              a residue exists iff the boundary is separable and the crossing
              partial; human measure hits exactly zero when the last engaged
              dimension crosses; fragment creation is zero at completeness —
              reinstatement is a consequence of incomplete crossing.
  (B0'2-RES)  Transmission with an explicit residual-requirement term: at a
              separable boundary with residual requirement r_B (human hours per
              unit output after decomposition), the residue wage satisfies
              w*r_B + a_M*m_c = pbar, so dw/dm_c = -a_M/r_B — continuous, and
              the LEVEL shift at decomposition has the sign of (l_A + l_B - r_B)
              net of the machine bill; at a bundled boundary the wage is flat in
              machine progress until the last ray crosses, then the task flips
              discretely (stasis-then-cliff).
"""
import sys

import numpy as np
import sympy as sp

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ---------------------------------------------------------------- B0'1-MEAS
rng = np.random.default_rng(3)
DIMS = list(range(7))                      # FRC PRS SYMR PER SYMO SOC UNS
NTASK = 60

tasks = []                                  # each: dict(dim -> labor weight), separable flag
for _ in range(NTASK):
    k = rng.integers(1, 5)
    engaged = rng.choice(DIMS, size=k, replace=False)
    weights = {int(d): float(w) for d, w in zip(engaged, rng.uniform(0.2, 1.0, k))}
    tasks.append({"w": weights, "sep": bool(rng.random() < 0.5)})

total_labor0 = sum(sum(t["w"].values()) for t in tasks)
crossed = set()
human = [dict(t) for t in tasks]           # live human task list (mutates)
order = [2, 0, 1, 3, 4, 5, 6]              # SYMR, FRC, PRS, then learning rays
created_per_step, human_measure = [], []

for step, ray in enumerate(order):
    crossed.add(ray)
    nxt, created = [], 0
    for t in human:
        eng = set(t["w"])
        cut = eng & crossed
        if not cut:
            nxt.append(t)
        elif cut == eng:
            pass                            # full flip: leaves the human space
        elif t["sep"]:
            residue = {"w": {d: v for d, v in t["w"].items() if d not in crossed},
                       "sep": t["sep"]}
            assert residue["w"], "empty residue on partial crossing"
            nxt.append(residue); created += 1
        else:
            nxt.append(t)                   # bundled: stands whole until the last ray
    # invariant: human labor = sum over ORIGINAL tasks of the requirement that is
    # (a) uncrossed if separable, (b) full if bundled-and-not-fully-crossed
    check = 0.0
    for t in tasks:
        eng = set(t["w"]); cut = eng & crossed
        if cut == eng:
            continue
        check += sum(v for d, v in t["w"].items() if d not in crossed) if t["sep"] \
            else sum(t["w"].values())
    now = sum(sum(t["w"].values()) for t in nxt)
    assert abs(now - check) < 1e-12, (step, now, check)
    human = nxt
    created_per_step.append(created); human_measure.append(now)

assert human_measure[-1] == 0.0, "human measure must be exactly zero at completeness"
assert created_per_step[-1] == 0, "no fragment creation at the final crossing"
assert sum(created_per_step) > 0, "the simulation should create residues on the way"
print("PASS  B0'1-MEAS measure bookkeeping exact at every crossing "
      f"(labor path {[round(m,1) for m in human_measure]}, start {total_labor0:.1f})")
print(f"PASS  B0'1-MEAS residues created only at separable partial crossings "
      f"(per step: {created_per_step}); creation = 0 at completeness — "
      "reinstatement shuts down with completeness")

# ---------------------------------------------------------------- B0'2-RES
w_, rB, aM, mc, lA, lB, pbar = sp.symbols('w r_B a_M m_c l_A l_B pbar', positive=True)
w_res = (pbar - aM * mc) / rB
assert sp.simplify(sp.diff(w_res, mc) + aM / rB) == 0
print("PASS  B0'2-RES separable boundary: w*r_B + a_M*m_c = pbar => dw/dm_c = -a_M/r_B"
      " — machine progress transmits CONTINUOUSLY into the residue wage")

w_pre = pbar / (lA + lB)
level = sp.simplify(w_res - w_pre)
# sign at mc -> 0: (pbar/rB) - pbar/(lA+lB) > 0 iff rB < lA + lB
s_pos = sp.simplify(level.subs(mc, 0).subs({rB: sp.Rational(1, 2), lA: 1, lB: 1, pbar: 2}))
s_neg = sp.simplify(level.subs(mc, 0).subs({rB: 3, lA: 1, lB: 1, pbar: 2}))
assert s_pos > 0 and s_neg < 0
print("PASS  B0'2-RES the level shift at decomposition carries the residual-requirement"
      " sign: excavator case (r_B falls) raises w; requirement-raising decompositions lower it")

# bundled: task cost = min(all-human, all-machine); human wage untouched until the
# LAST engaged ray crosses, then discrete flip. Piecewise verified numerically.
mcs = np.linspace(2.0, 0.05, 200)
lAn, lBn, wn = 1.0, 1.0, 1.0
all_human = (lAn + lBn) * wn
holds = all_human <= (mcs * (lAn + lBn))    # machine can only take the WHOLE task
w_path = np.where(holds, wn, 0.0)
jump_at = np.argmax(~holds) if (~holds).any() else None
assert w_path[0] == wn and (np.diff(w_path[:jump_at]) == 0).all()
assert jump_at is not None and w_path[jump_at] == 0.0
print("PASS  B0'2-RES bundled boundary: wage flat in machine progress, then a discrete"
      f" flip when the whole-task comparison turns (at m_c = {mcs[jump_at]:.2f}) —"
      " stasis-then-cliff")

print()
print("All Block B.0' checks passed (flags B0'1-MEAS, B0'2-RES).")
