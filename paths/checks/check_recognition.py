# check_recognition.py — the recognition clock as a mixture: Bayes, the market curve, resolution, narrative.
#
# The worlds are recognition.worlds()'s default: calibration (c)'s central economy (her decision, 2026-09-30), the return
# following r* from its own rho. B1 gates the comparators: (b) and (a) are the pre-switch worlds bit for bit. R1 gates
# results/recognition.json against a rebuild. Findings (S) are stated as found on the central; restated at the switch
# (the old -> new table is in the switch's report). The market's signal is all wages over income (solve's labor_share,
# machine-chain labour included), not the paper's Figure 7 basis (labour_share_bea): S3 names the basis and gates the
# Figure 7 sensitivity (results/recognition.json sensitivity_signal_fig7) by re-running it here.
# Thresholds set after seeing (c)'s numbers: S3's 0.05 years for "the bases coincide on (b)" (flagged here).
# Restated at the refit (2026-10-27, Log 46; the bridges refit on (c), (b) and (a) on their own), as found: M3 compares policy with
# the desired rate where the lower bound lets it follow (the refit's desired rate falls below the floor); S4's bull flattening is
# now of about two points at the long end (before the refit under 25 bp), its threshold (-100 bp at 10Y) set after seeing it.
# Numbers updated at the revision (2026-10-28, Log 54; decisions 93-96), no gate moved: across the window 3M -5, 2Y -57, 10Y -141,
# 30Y -179 bp [Log 46 -5 / -70 / -177 / -227]; S4's label "about 1.4 points" [nearly two]; its -100 bp gate holds by 41 bp.
#
# Run from paths/:  ../venv/Scripts/python.exe checks/check_recognition.py
# Exit status 0 only if every check passes.

from __future__ import annotations

import json
import os
import sys
from dataclasses import replace

import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "code"))
import curve as cv  # noqa: E402
import macro as m  # noqa: E402
import recognition as rc  # noqa: E402
import recognition_scenarios as rs  # noqa: E402
import regimes as rg  # noqa: E402

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


e, old, new = rc.worlds()
t = old["t"]
logit = lambda p: np.log(p / (1 - p))  # noqa: E731

print("L — learning")
p_same = rc.learn(old, old, rc.Learning(sigma=1.0, p0=0.05))
check("L1 two worlds with the same signal teach nothing: the probability stays at the prior", np.allclose(p_same, 0.05))
lr = rc.Learning(sigma=1.0, p0=0.05)
p = rc.learn(old, new, lr)
d = (new["labor_share"] - old["labor_share"]) * 100
closed = logit(0.05) + np.concatenate([[0.0], np.cumsum(d[1:] ** 2 / 2.0)])
_, lo = rc.learn(old, new, lr, return_logodds=True)
check("L2 noiseless learning is the closed form: log odds = logit(p0) + sum (s_new - s_old)^2 / (2 sigma^2)",
      np.max(np.abs(lo - closed)) < 1e-9 * max(1.0, np.max(np.abs(closed))), f"final log odds {lo[-1]:.1f}")
p_old = rc.learn(old, new, replace(lr, truth="old"))
check("L3 if the data come from the status quo, the probability of the new world only falls",
      np.all(np.diff(p_old) <= 1e-15) and p_old[-1] < 1e-6)
cross = [rc.crossing(t, rc.learn(old, new, replace(lr, sigma=s)), 0.5) for s in (0.5, 1.0, 2.0, 4.0)]
check("L4 noisier data mean later recognition: the date the probability crosses one half rises with sigma",
      all(c is not None for c in cross) and np.all(np.diff(cross) > 0), "sigma 0.5/1/2/4 pp: " + " ".join(f"{c:.2f}" for c in cross))
pj = rc.learn(old, old, rc.Learning(sigma=1.0, p0=0.05, jumps=((2.0, 3.0),)))
i2 = int(np.argmin(np.abs(t - 2.0)))
check("L5 a narrative shock moves the log odds by exactly its size, with no new data",
      abs((logit(pj[i2]) - logit(pj[i2 - 1])) - 3.0) < 1e-12 and np.allclose(pj[:i2], 0.05))

print("M — the market curve")
mixes, olds, news, pol = rc.market_curves(old, new, p)
T = np.array([1 / 12, 0.25, 1, 2, 5, 10, 30])
err = max(np.max(np.abs(rg.zero(T, mx) - ((1 - p[i]) * cv.zero(T, olds[i]) + p[i] * cv.zero(T, news[i]))))
          for i, mx in enumerate(mixes))
check("M1 the market curve is the probability-weighted mix of the two worlds' curves", err < 1e-12, f"max err {err:.1e}")
jumps = [cv.zero(T, news[j]) - rg.zero(T, mixes[j]) for j in range(len(t))]
i = int(np.nonzero(p >= 0.5)[0][0])                              # the first date the market is past one half
jump = jumps[i]
check("M2 revealing the truth jumps the curve by (1 - p)(z_new - z_old) — at every date",
      max(np.max(np.abs(jumps[j] - (1 - p[j]) * (cv.zero(T, news[j]) - cv.zero(T, olds[j])))) for j in range(len(t))) < 1e-12,
      f"at year {t[i]:g} (p {p[i]:.2f}): 2Y {jump[3]*100:+.1f}, 10Y {jump[5]*100:+.1f}, 30Y {jump[6]*100:+.1f} bp")
desired = (1 - p) * old["desired"] + p * new["desired"]
floor_ = m.Recognition().elb
check("M3 [restated at the refit] the policy rate is common to both worlds' curves, sits on the 25 bp grid, and tracks the "
      "probability-weighted desired rate down to the lower bound (-0.5%), below which it holds there",
      all(o.r0 == n.r0 for o, n in zip(olds, news)) and np.allclose(pol / 0.25, np.round(pol / 0.25))
      and np.max(np.abs(pol - np.maximum(desired, floor_))) < 0.5 and pol.min() >= floor_ - 1e-12,
      f"max gap to the desired rate floored at {floor_:g}: {np.max(np.abs(pol - np.maximum(desired, floor_))):.2f} pp; the desired rate's "
      f"low {desired.min():+.2f}%, policy's {pol.min():+.2f}%")

print("B — the comparators")
eb, _, _, _ = m.calibrate(base=m.CAPITAL_BASE)
ea, _, _, _ = m.calibrate()
arr = lambda d: {k: v for k, v in d.items() if isinstance(v, np.ndarray)}  # noqa: E731
same = lambda a, b: all(np.array_equal(a[k], b[k]) for k in arr(a)) and arr(a).keys() == arr(b).keys()  # noqa: E731
brb = replace(m.BRIDGES_B, capital_premium=5.0)
old_b = m.macro_path(eb, m.TechPath(eta_end=1.0, lam_end=eb.lam), brb, 15.0, 0.25)
new_b = m.macro_path(eb, m.TechPath(eta_end=0.04, lam_end=0.01, t_mid=6, width=6), brb, 15.0, 0.25)
old_a = m.macro_path(ea, m.TechPath(eta_end=1.0, lam_end=ea.lam), m.BRIDGES_B, 15.0, 0.25)
new_a = m.macro_path(ea, m.TechPath(eta_end=0.04, lam_end=0.01, t_mid=6, width=6), m.BRIDGES_B, 15.0, 0.25)
_, o_b, n_b = rc.worlds(calibration="b")
_, o_a, n_a = rc.worlds(capital=False)
ec, info = m.central()
check("B1 the default worlds are the central (c); calibration='b' is the pre-switch (b) worlds and capital=False the (a) worlds, "
      "array for array", e == ec and same(o_b, old_b) and same(n_b, new_b) and same(o_a, old_a) and same(n_a, new_a),
      f"central rho {ec.rho:.4f}, premium {info['capital_premium']:.2f} pp; (b) premium {m.capital_premium(eb):.2f}")

print("R — the unit's results (results/recognition.json, rebuilt by code/recognition_scenarios.py)")
with open(os.path.join(os.path.dirname(HERE), "results", "recognition.json"), encoding="utf-8") as f:
    R = json.load(f)
rebuilt = json.loads(json.dumps(rs.results()[0], default=str))
check("R1 the stored results equal a rebuild: the central, (b) the comparator and (c)'s high root", R == rebuilt,
      f"{len(json.dumps(R))} characters; blocks: central, " + ", ".join(k for k in R if k in ("comparator_b", "sensitivity_c_hi")))

print("S — the baseline scenario (default bridges; scenario-dependent, stated as found)")
ls_done = (new["labor_share"][0] - np.interp(cross[1], t, new["labor_share"])) / (new["labor_share"][0] - new["labor_share"][-1])
check("S1 with noiseless data and sigma 1 pp, the market is past one half before a tenth of the labour-share fall has happened",
      ls_done < 0.1, f"crosses 1/2 at year {cross[1]:.2f}, with {ls_done*100:.1f}% of the fall done")
iy0, iy5 = 0, int(np.argmin(np.abs(t - 5.0)))
z0, z5 = rg.zero(T, mixes[iy0]), rg.zero(T, mixes[iy5])
check("S2 under the default bridges, waking up lowers the long end (the new world's future neutral rate averages lower)",
      z5[-1] < z0[-1] and z5[-2] < z0[-2], f"year 0 -> 5: 2Y {(z5[3]-z0[3])*100:+.0f}, 10Y {(z5[5]-z0[5])*100:+.0f}, 30Y {(z5[6]-z0[6])*100:+.0f} bp")
Rb = R["comparator_b"]
mc, mcb = R["monte_carlo_sigma1"]["new_world_p50_date_percentiles_10_50_90"], Rb["monte_carlo_sigma1"]["new_world_p50_date_percentiles_10_50_90"]
nl, nlb = R["recognition_noiseless"]["sigma 1.0, p0 0.05"]["p_0.5"], Rb["recognition_noiseless"]["sigma 1.0, p0 0.05"]["p_0.5"]
F7S = R["sensitivity_signal_fig7"]
AW, FB = "all wages (the default signal)", "Figure 7 basis"
o_c, n_c = old, new
fig7_c = rc.crossing(t, rc.learn(o_c, n_c, replace(lr, signal="labour_share_bea")), 0.5)
fig7_b = rc.crossing(o_b["t"], rc.learn(o_b, n_b, replace(lr, signal="labour_share_bea")), 0.5)
adv_aw, adv_f7 = nlb - nl, fig7_b - fig7_c
check("S3 on (c) the market wakes up earlier than on (b): (c)'s labour share falls faster early, so the worlds separate sooner "
      "(noiseless, and at the 10th, 50th and 90th percentiles of 500 noise draws) — on the market's signal, all wages over income. "
      "Part of the advance is the signal's basis: all wages include the machine chain's labour, the part deep automation removes "
      "fastest; watching the paper's Figure 7 basis the market still wakes up earlier on (c), by less; on (b) the two bases coincide",
      nl < nlb and all(x < y for x, y in zip(mc, mcb)) and fig7_c < fig7_b and adv_f7 < adv_aw
      and abs(fig7_c - F7S["c"][FB]["p_0.5"]) < 1e-12 and abs(fig7_b - F7S["b"][FB]["p_0.5"]) < 1e-12
      and abs(F7S["c"][AW]["p_0.5"] - nl) < 1e-12 and abs(F7S["b"][FB]["p_0.5"] - F7S["b"][AW]["p_0.5"]) < 0.05,
      f"one-half date, all wages {nl:.2f} vs {nlb:.2f} years ({adv_aw:.2f} earlier); Figure 7 basis {fig7_c:.2f} vs {fig7_b:.2f} "
      f"({adv_f7:.2f} earlier); 500 draws 10/50/90% (all wages): {mc} vs {mcb}; labour share year 3, all wages "
      f"{R['labour_share_pp']['3'][1] - R['labour_share_pp']['3'][0]:+.1f} vs {Rb['labour_share_pp']['3'][1] - Rb['labour_share_pp']['3'][0]:+.1f} pp, "
      f"Figure 7 basis {F7S['c'][FB]['fall_pp_at_year3']:+.2f} vs {F7S['b'][FB]['fall_pp_at_year3']:+.2f} pp")
cw, cwb = R["recognition_window"]["curve_move_bp"], Rb["recognition_window"]["curve_move_bp"]
check("S4 [restated at the refit; numbers updated at the revision] across the recognition window the whole curve falls, the long end "
      "most — a bull flattening of about 1.4 points at 10Y (at the refit nearly two; before the refit, on the bridges as tuned on (b), "
      "under 25 bp); on (b) the 2Y rose while the long end fell — the front's sign flips",
      all(cw[k] < 0 for k in ("2Y", "10Y", "30Y")) and cw["30Y"] <= cw["10Y"] <= cw["2Y"] and cw["10Y"] < -100
      and cwb["2Y"] > 0 > cwb["10Y"],
      "(c): " + " ".join(f"{k} {v:+.1f}" for k, v in cw.items()) + " bp; (b): " + " ".join(f"{k} {v:+.1f}" for k, v in cwb.items()) + " bp")

fails = [n for n, ok, _ in RESULTS if not ok]
print(f"\n{len(RESULTS) - len(fails)}/{len(RESULTS)} checks passed")
print(f"ALL GREEN ({len(RESULTS)})" if not fails else "FAILURES: " + "; ".join(n.split(' ')[0] for n in fails))
sys.exit(0 if not fails else 1)
