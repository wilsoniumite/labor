# check_hx.py — the battery for H-X (code/hx_test.py). Recomputes the test independently (statsmodels for the
# regressions, a second bootstrap seed), checks the data against the frozen specification (docs/spec.md Section 7)
# and checks every H-X number quoted in paper/main.tex.
# Run from stagnation/:  ../venv/bin/python checks/check_hx.py      Exit 0 only if every check passes.
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
import hx_test as H  # noqa: E402

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok)))
    print(f"{'PASS' if ok else 'FAIL'} {name}" + (f" — {detail}" if detail else ""))


gdph, hrs, pop, pwt_h = H.load()
countries = H.sample(gdph, hrs, pop)
df = H.build(gdph, hrs, pop, countries)
res = json.loads((ROOT / "data" / "hx_results.json").read_text())

# ---------------------------------------------------------------------------------------- the frozen specification
spec = (ROOT / "docs" / "spec.md").read_text()
check("S1 the spec's H-X section is the frozen text (sample, years, exclusions, estimators, decision rule)",
      all(s in spec for s in ("complete annual data 1995–2019, excluding Ireland", "HC1 standard errors",
                              "wild cluster bootstrap, Webb weights, 9,999 draws",
                              "Consistent: β < 0 with two-sided p < 0.05 in the primary and the same sign")))
check("S2 38 members; Ireland and Luxembourg excluded; non-members (BGR, HRV, PER, ROU) and aggregates not used",
      len(H.MEMBERS) == 38 and len(set(H.MEMBERS)) == 38 and not set(countries) & {"IRL", "LUX", "BGR", "HRV", "PER",
                                                                                   "ROU", "OECD", "EA20", "EU27_2020"})
years = range(1995, 2020)
check("S3 every country in the sample has all 25 years of all three series; every member left out lacks one",
      all(np.isfinite(d.loc[c, y]) for c in countries for d in (gdph, hrs, pop) for y in years)
      and all(any(c not in d.index or any(y not in d.columns or not np.isfinite(d.loc[c, y]) for y in years)
                  for d in (gdph, hrs, pop)) for c in res["dropped_incomplete"]),
      f"{len(countries)} kept; dropped {res['dropped_incomplete']}")
hpp = hrs / pop * 1e6
check("S4 magnitudes: GDP per hour 10-130 USD (constant PPP), hours per person 15-64 between 700 and 2,000 a year",
      all(10 < gdph.loc[c, y] < 130 and 700 < hpp.loc[c, y] < 2000 for c in countries for y in (1995, 2019)))
pdb = pd.read_csv(ROOT / "cache" / "oecd" / "pdb_raw.csv")
u = pdb[(pdb.REF_AREA == "USA") & (pdb.MEASURE == "GDPHRS") & (pdb.UNIT_MEASURE == "USD_PPP_H") &
        (pdb.PRICE_BASE == "LR") & (pdb.TRANSFORMATION == "N")]
check("S5 the series is GDP per hour at constant PPPs: the US value in the base year 2020 equals current-price USD",
      abs(u[u.TIME_PERIOD == 2020].OBS_VALUE.iloc[0] - pdb[(pdb.REF_AREA == "USA") & (pdb.MEASURE == "GDPHRS") &
          (pdb.UNIT_MEASURE == "USD_PPP_H") & (pdb.PRICE_BASE == "V") & (pdb.TIME_PERIOD == 2020)].OBS_VALUE.iloc[0])
      < 1e-6 * u[u.TIME_PERIOD == 2020].OBS_VALUE.iloc[0])

# ------------------------------------------------------------------------------------- the primary, recomputed
X = sm.add_constant(df[["g_h", "log_pi0"]])
m = sm.OLS(df.g_pi, X).fit(cov_type="HC1")
pr = res["primary"]
check("P1 primary OLS with HC1 recomputed by statsmodels: beta, se, p", abs(m.params["g_h"] - pr["beta"]) < 1e-10
      and abs(m.bse["g_h"] - pr["se"]) < 1e-10, f"beta {m.params['g_h']:+.4f}, se {m.bse['g_h']:.4f}")
# statsmodels' HC1 p-value uses the normal; the spec's uses t with n - k df: both reported, the decision is the same
p_t = 2 * __import__("scipy").stats.t.sf(abs(m.tvalues["g_h"]), m.df_resid)
check("P2 the p-value with n - k degrees of freedom", abs(p_t - pr["p"]) < 1e-10,
      f"t-based {p_t:.4f}, normal-based {m.pvalues['g_h']:.4f}")

# --------------------------------------------------------------------------------------- the panel, recomputed
pf = H.panel_frame(gdph, hrs, pop, countries)
D = pd.get_dummies(pf[["country", "period"]], drop_first=False, dtype=float)
D = D.drop(columns=[c for c in D.columns if c.startswith("period_")][0])
Xp = pd.concat([pf[["g_h"]], D], axis=1)
mp = sm.OLS(pf.g_pi, Xp).fit(cov_type="cluster", cov_kwds={"groups": pd.factorize(pf.country)[0]})
pa = res["panel"]
check("P3 panel with country and period effects recomputed: beta and the CR1 t-statistic",
      abs(mp.params["g_h"] - pa["beta"]) < 1e-10 and abs(mp.tvalues["g_h"] - pa["t"]) < 1e-8,
      f"beta {mp.params['g_h']:+.4f}, t {mp.tvalues['g_h']:+.3f}")
pa2 = H.panel(pf, draws=9999, seed=7)
check("P4 the bootstrap p-value is stable across seeds (within Monte Carlo error)",
      abs(pa2["p_boot"] - pa["p_boot"]) < 0.01, f"{pa['p_boot']:.4f} and {pa2['p_boot']:.4f}")
check("P5 the panel has 5 periods per country", len(pf) == 5 * len(countries) and pa["n"] == len(pf))

# ------------------------------------------------------------------------------------ the IV and leave-one-out
iv = res["iv_pwt"]
d = df.copy()
d["g_h_pwt"] = [(np.log(pwt_h.loc[c, 2019] * 1e6 / pop.loc[c, 2019]) - np.log(pwt_h.loc[c, 1995] * 1e6 /
                                                                               pop.loc[c, 1995])) / 24 for c in d.index]
fs = sm.OLS(d.g_h, sm.add_constant(d[["g_h_pwt", "log_pi0"]])).fit()
ss = sm.OLS(d.g_pi, sm.add_constant(pd.DataFrame({"g_h_hat": fs.fittedvalues, "log_pi0": d.log_pi0}))).fit()
check("I1 2SLS coefficient by two OLS stages equals the script's", abs(ss.params["g_h_hat"] - iv["beta"]) < 1e-10,
      f"{ss.params['g_h_hat']:+.4f}")
check("I2 every sample country is in PWT 11.0 with hours in 1995 and 2019", iv["n"] == len(countries))
loo = H.leave_one_out(df)
check("L1 leave-one-out recomputed: range of beta and the largest p", abs(min(r["beta"] for r in loo.values()) -
      res["loo_beta_range"][0]) < 1e-12 and abs(max(r["p"] for r in loo.values()) - res["loo_p_max"]) < 1e-12)

# ---------------------------------------------------------------------------------------------- the decision
rule = ("consistent" if pr["beta"] < 0 and pr["p"] < 0.05 and pa["beta"] < 0 else
        "counts against" if pr["beta"] > 0 and pr["p"] < 0.05 else "uninformative")
check("D1 the decision follows the frozen rule", rule == res["decision"], res["decision"])

# ------------------------------------------------------------------------------------------ the text, if written
TEX = ROOT / "paper" / "main.tex"
tex = TEX.read_text()
sec = tex[tex.find(r"\label{sec:5}"):tex.find(r"\label{sec:6}")]
if "H-X" in sec and "draftnote" not in sec[:400]:
    quotes = [(f"{pr['beta']:+.2f}".replace("+", ""), "cross-section|across countries"),
              (f"{pr['p']:.2f}", "cross-section|across countries"), (f"{pa['beta']:.2f}".replace("-", ""), "within"),
              (f"{pa['p_boot']:.3f}", "within|bootstrap"), (str(res["n"]), "countries")]
    for s, anchor in quotes:
        hits = [mm.start() for mm in re.finditer(r"(?<![\d.])" + re.escape(s) + r"(?![\d])", sec)]
        check(f"Q1 '{s}' printed in Section 5 near /{anchor}/", any(re.search(anchor, sec[max(0, h - 400):h + 400])
                                                                   for h in hits), f"{len(hits)} hit(s)")
    check("Q2 Section 5 states the frozen decision", res["decision"] in sec)

n_fail = sum(1 for _, ok in RESULTS if not ok)
print(f"\n{len(RESULTS) - n_fail}/{len(RESULTS)} checks passed")
sys.exit(1 if n_fail else 0)
