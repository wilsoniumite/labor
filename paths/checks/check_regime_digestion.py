# check_regime_digestion.py — the forward-rate test: the estimators, the findings, the model's catch-up.
#
# Layer 3 (the model's catch-up) runs on calibration (c)'s central economy since her decision of 2026-09-30, with (b), the
# pre-switch calibration, stored beside it; M1 rebuilds both and gates the comparator as the pre-switch run. Layers 1 and 2
# are data (F1-F5) and do not depend on the calibration.
# Restated at the refit (2026-10-27, Log 46; the central on the bridges refit on (c), its "deficits dominate" branch; (b) on its
# own), as found: F6 compares sizes (the catch-up is now down), F7 states the catch-up running the other way from (b)'s.
#
# Run from paths/:  ../venv/Scripts/python.exe checks/check_regime_digestion.py
# Exit status 0 only if every check passes.

from __future__ import annotations

import json
import os
import sys

from dataclasses import replace

import numpy as np
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "code"))
import macro as m  # noqa: E402
import regime_digestion as rd  # noqa: E402

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


print("E — the estimators")
rng = np.random.default_rng(7)
x = rng.normal(size=4000)
y = 0.3 + 0.8 * x + rng.normal(size=4000) * (1 + 0.5 * np.abs(x))
b, se = rd.ols_hac(y, x, 0)
X = np.column_stack([np.ones_like(x), x])
bo = np.linalg.lstsq(X, y, rcond=None)[0]
u = y - X @ bo
XtXi = np.linalg.inv(X.T @ X)
white = np.sqrt(np.diag(XtXi @ (X.T * u ** 2) @ X @ XtXi))
check("E1 the regression is OLS, and with no lags its standard errors are White's", np.allclose(b, bo) and np.allclose(se, white))
lam, n = 0.4, 20000
target = np.cumsum(rng.normal(size=n + 1))                      # a random walk; its next value is the forecast target
info = target[:-1] + 0.0                                         # full information: the current level
F = np.empty(n); F[0] = info[0]
for t_ in range(1, n):
    F[t_] = lam * F[t_ - 1] + (1 - lam) * info[t_]              # sticky information: a share lam of last period's forecast survives
err = pd.Series(target[1:] - F)
rev = pd.Series(F - np.concatenate([[np.nan], F[:-1]]))
bb, _, _ = rd.cg(err, rev, 2)
check("E2 on a sticky-information forecaster the CG slope is lam/(1 - lam), and the half-life inverts it",
      abs(bb - lam / (1 - lam)) < 0.05 and abs(rd.half_life(bb, 1.0) - np.log(0.5) / np.log(lam)) < 0.1,
      f"slope {bb:.3f} (theory {lam / (1 - lam):.3f})")
yrs = np.arange(1990, 2031)
real = pd.Series(np.where(yrs < 2008, 5.0, 0.5), index=yrs)
g_true = 0.12
anc = [4.0]
for yr in yrs[1:]:
    anc.append(anc[-1] + g_true * (real.loc[yr - 1] - anc[-1]))
g_hat, rmse = rd.gain_fit(pd.Series(anc, index=yrs), real)
check("E3 the constant-gain fit recovers a known gain", abs(g_hat - g_true) < 1e-3 and rmse < 1e-3, f"{g_hat:.4f}")

print("F — the findings (stated as found; results/regime_digestion.json, rebuilt by code/regime_digestion.py)")
with open(os.path.join(ROOT, "results", "regime_digestion.json"), encoding="utf-8") as fh:
    R = json.load(fh)
sv = R["layer1_next_year"]["survey"]["1981-2026"]
mk = R["layer1_next_year"]["market_kw"]["1990-2025"]["1y ahead"]
check("F1 forecasters under-react to news about the next year: positive, significant CG slopes 2 and 3 quarters ahead",
      all(sv[h]["b"] / sv[h]["se"] > 2 for h in ("2q ahead", "3q ahead")),
      " ".join(f"{h}: {sv[h]['b']:+.2f} ({sv[h]['se']:.2f}), half-life {sv[h]['half_life_months']} months" for h in sv))
check("F2 so do market forwards a year ahead, net of the Kim–Wright term premium",
      mk["b"] / mk["se"] > 2, f"{mk['b']:+.2f} ({mk['se']:.2f}), half-life {mk['half_life_months']} months")
eras = [R["layer1_next_year"]["survey"][e]["3q ahead"]["b"] for e in ("1981-1994", "1995-2007", "2008-2026")]
check("F3 unlike prices, surveyed forecasters show no sign of speeding up across eras (3 quarters ahead)",
      eras[-1] >= eras[0], " -> ".join(f"{v:+.2f}" for v in eras))
gf = R["layer2_regime_anchor"]["gain_fits"]
hls = [v["half_life_years"] for d in gf.values() for v in d.values()]
check("F4 the regime anchors — survey and market — adjust with half-lives of years in every span",
      all(h is not None and h > 2 for h in hls), f"{min(hls):.1f} to {max(hls):.1f} years")
rec = R["layer2_regime_anchor"]["survey_anchor_record"]
check("F5 the survey anchor was too high in over 90% of surveys 1992–2016 and did worse than 'no change'",
      rec["too_high_share"] > 0.9 and rec["rmse_pp"]["survey anchor"] > rec["rmse_pp"]["no change (last year's rate)"],
      f"{rec['too_high_share']:.0%}; RMSE {rec['rmse_pp']}")
cu = R["layer3_model_catch_up"]
k0, k1 = "human regime digestion 3y", "human regime digestion 3y, AI adopted around year 5 (x30)"
check("F6 [restated at the refit] in the model, with people digesting regime news over 3 years, adopting AI moves the 10Y far more "
      "in its year than the news does — in size; on the refit the move is down (before the refit, up)",
      abs(cu[k1]["10Y_move_years_4.5_to_5.5_bp"]) > 2 * max(abs(cu[k0]["10Y_move_years_4.5_to_5.5_bp"]),
                                                            abs(cu["instant (the evidence)"]["10Y_move_years_4.5_to_5.5_bp"]))
      and cu[k1]["10Y_move_years_4.5_to_5.5_bp"] < 0,
      f"adoption year: {cu[k1]['10Y_move_years_4.5_to_5.5_bp']:+.0f} bp with AI, {cu[k0]['10Y_move_years_4.5_to_5.5_bp']:+.0f} without, "
      f"{cu['instant (the evidence)']['10Y_move_years_4.5_to_5.5_bp']:+.0f} in the evidence")
cb = R["layer3_model_catch_up_comparator_b"]
hls = (1, 3, 5)
ai = lambda d, h: d[f"human regime digestion {h}y, AI adopted around year 5 (x30)"]["10Y_move_years_4.5_to_5.5_bp"]  # noqa: E731
check("F7 [restated at the refit] on the central the catch-up runs the other way from (b)'s, the pre-switch run: down at every human "
      "half-life, where (b)'s is up, and smaller in size — even with deficits dominating, the refit's new world never raises r* above its "
      "start ((b)'s rises to 2.5%), so its required return never rises (before the refit the central's catch-up was larger than (b)'s "
      "and up)",
      all(ai(cu, h) < 0 < ai(cb, h) and abs(ai(cu, h)) < ai(cb, h) for h in hls)
      and cu["worlds"]["new_world_r_star_start_max_year15"][1] == cu["worlds"]["new_world_r_star_start_max_year15"][0]
      and cb["worlds"]["new_world_r_star_start_max_year15"][1] > cb["worlds"]["new_world_r_star_start_max_year15"][0] + 1
      and cu["worlds"]["new_world_required_return_rise_max_pp"] < cu["worlds"]["rate_headroom_pp"],
      "adoption year with AI, half-life 1/3/5 years: " + " / ".join(f"{ai(cu, h):+.0f}" for h in hls) + " bp ((b) "
      + " / ".join(f"{ai(cb, h):+.0f}" for h in hls) + f"); r* start/peak (to year 15)/year 15 {cu['worlds']['new_world_r_star_start_max_year15']} "
      f"((b) {cb['worlds']['new_world_r_star_start_max_year15']}); required return up to {cu['worlds']['new_world_required_return_rise_max_pp']:+.2f} pp "
      f"of headroom {cu['worlds']['rate_headroom_pp']:.2f}")

print("M — layer 3 on the central, (b) the comparator")
ec, _ = m.central()
eb, _, _, _ = m.calibrate(base=m.CAPITAL_BASE)
rt = lambda o: json.loads(json.dumps(o, default=str))  # noqa: E731
same_objects = (m.feedback_bridges(eb, base=m.BRIDGES_B, **m.BRANCHES_B["deficits dominate"])
                == replace(m.BRIDGES_B, capital_premium=5.0, alpha_fiscal=0.25, alpha_rent=0.02)
                and m.deep_tech(eb) == m.TechPath(eta_end=0.04, lam_end=0.01, t_mid=6, width=6)
                and m.hold_tech(eb) == m.TechPath(eta_end=1.0, lam_end=eb.lam))
check("M1 layer 3 as stored equals a rebuild on the central and on (b), and (b)'s runs use the pre-switch objects exactly "
      "(Bridges(capital_premium=5.0, ...), TechPath(0.04, 0.01, 6, 6))",
      rt(rd.layer3(ec)[0]) == cu and rt(rd.layer3(eb, m.BRIDGES_B, m.BRANCHES_B)[0]) == cb and same_objects
      and R["layer3_calibration"]["tag"] == "c_central_lo",
      f"central rho {ec.rho:.4f}, premium {m.capital_premium(ec):.2f} pp; (b) premium {m.capital_premium(eb):.2f} pp")

fails = [n for n, ok, _ in RESULTS if not ok]
print(f"\n{len(RESULTS) - len(fails)}/{len(RESULTS)} checks passed")
print(f"ALL GREEN ({len(RESULTS)})" if not fails else "FAILURES: " + "; ".join(n.split(' ')[0] for n in fails))
sys.exit(0 if not fails else 1)
