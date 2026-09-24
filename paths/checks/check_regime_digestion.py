# check_regime_digestion.py — the forward-rate test: the estimators, the findings, the model's catch-up.
#
# Run from paths/:  ../venv/Scripts/python.exe checks/check_regime_digestion.py
# Exit status 0 only if every check passes.

from __future__ import annotations

import json
import os
import sys

import numpy as np
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "code"))
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
R = json.load(open(os.path.join(ROOT, "results", "regime_digestion.json"), encoding="utf-8"))
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
check("F6 in the model, with people digesting regime news over 3 years, adopting AI moves the 10Y far more in its year than "
      "the news does",
      cu[k1]["10Y_move_years_4.5_to_5.5_bp"] > 2 * max(cu[k0]["10Y_move_years_4.5_to_5.5_bp"], cu["instant (the evidence)"]["10Y_move_years_4.5_to_5.5_bp"]),
      f"adoption year: {cu[k1]['10Y_move_years_4.5_to_5.5_bp']:+.0f} bp with AI, {cu[k0]['10Y_move_years_4.5_to_5.5_bp']:+.0f} without, "
      f"{cu['instant (the evidence)']['10Y_move_years_4.5_to_5.5_bp']:+.0f} in the evidence")

n_ok = sum(ok for _, ok, _ in RESULTS)
print(f"\n{n_ok}/{len(RESULTS)} checks passed")
sys.exit(0 if n_ok == len(RESULTS) else 1)
