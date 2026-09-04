# split_determinants.py — what determines the use split (design memo §4b, T10c).
# (A) the replacement floor: consumption of fixed capital / GDP, 1950–2025, total and by
#     sector where the series gate; net investment = gross private investment − private CFC;
# (B) the market's price of uncertainty, latest vs history: 10y term premium (Kim–Wright),
#     10y breakeven inflation, Baa credit spread, VIX, 10y TIPS real yield;
# (C) the build-lag markup on the investment share, (g+δ)·v·(1+g)^J, tabulated.
# Outputs ../data/split_determinants_*.csv. Run from three-taxes/:
#   ../venv/Scripts/python.exe code/split_determinants.py
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUTER = os.path.dirname(ROOT)
LINKREPO = os.path.join(OUTER, "link-repo")
DATA = os.path.join(ROOT, "data")
os.chdir(LINKREPO)
sys.path.insert(0, os.path.join(LINKREPO, "code"))
from lambda_compute2 import pull_fred, annualize   # noqa: E402
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ---------------- (A) the replacement floor ----------------
SER = {   # concept: (FRED id, $B divisor, sanity band at 2023 in $B)
    "gdp":      ("GDPA",            1.0, (25000, 32000)),
    "gpdi":     ("GPDIA",           1.0, (4000, 6500)),
    "cfc":      ("COFC",            1.0, (3800, 5800)),     # total CFC, quarterly SAAR
    "cfc_priv": ("A024RC1A027NBEA", 1.0, (3200, 5000)),     # private CFC, annual
    "cfc_gov":  ("A264RC1A027NBEA", 1.0, (500, 900)),       # government CFC, annual
    "gov_inv":  ("A782RC1A027NBEA", 1.0, (900, 1400)),      # government gross investment, annual
}
S = {}
for k, (sid, div, (lo, hi)) in SER.items():
    s = pull_fred(sid)
    if s is None:
        print(f"{k:9s} {sid:18s} FAIL: no series"); continue
    a = annualize(s) / div
    chk = min(2023, int(a.index.max()))
    v = float(a.loc[chk])
    if not (lo <= v <= hi):
        print(f"{k:9s} {sid:18s} FAIL sanity: {chk}={v:,.0f} not in [{lo},{hi}]"); continue
    print(f"{k:9s} {sid:18s} OK {chk}={v:,.0f} last={int(a.index.max())}")
    S[k] = a
df = pd.DataFrame({k: v for k, v in S.items()}).dropna(subset=["gdp", "cfc"])
df = df[(df.index >= 1950) & (df.index <= 2025)]
df["cfc_share"] = df["cfc"] / df["gdp"]
if "gpdi" in df:
    df["gpdi_share"] = df["gpdi"] / df["gdp"]
if "cfc_priv" in df and "gpdi" in df:
    df["net_private_inv_share"] = (df["gpdi"] - df["cfc_priv"]) / df["gdp"]
if "gov_inv" in df and "cfc_gov" in df:
    df["net_gov_inv_share"] = (df["gov_inv"] - df["cfc_gov"]) / df["gdp"]
if "gov_inv" in df:
    df["gross_inv_share_total"] = (df["gpdi"] + df["gov_inv"]) / df["gdp"]
    df["net_inv_share_total"] = (df["gpdi"] + df["gov_inv"] - df["cfc"]) / df["gdp"]
df.round(4).to_csv(os.path.join(DATA, "split_determinants_replacement.csv"))
print("\n=== replacement floor and net investment (shares of GDP) ===")
cols = [c for c in ["cfc_share", "gpdi_share", "gross_inv_share_total", "net_inv_share_total",
                    "net_private_inv_share", "net_gov_inv_share"] if c in df]
for y in (1950, 1960, 1970, 1980, 1990, 2000, 2007, 2010, 2019, 2023, 2025):
    if y in df.index:
        print(y, {c: round(float(df.loc[y, c]), 3) for c in cols})
dec = df[cols].groupby((df.index // 10) * 10).mean().round(3)
print("\ndecade means:\n", dec.to_string())

# ---------------- (B) the market's price of uncertainty ----------------
MKT = {   # id: (label, units)
    "THREEFYTP10": ("10y term premium (Kim-Wright)", "pct"),
    "T10YIE":      ("10y breakeven inflation", "pct"),
    "DFII10":      ("10y TIPS real yield", "pct"),
    "BAA10Y":      ("Baa spread over 10y Treasury", "pct"),
    "VIXCLS":      ("VIX", "index"),
    "DGS30":       ("30y Treasury", "pct"),
}
rows = []
print("\n=== market premia: latest, 2021 mean, 2010-2019 mean, full-sample mean ===")
for sid, (label, unit) in MKT.items():
    s = pull_fred(sid)
    if s is None:
        print(f"{sid:12s} FAIL: no series"); continue
    s = s.dropna()
    latest_d, latest = s.index[-1], float(s.iloc[-1])
    m21 = float(s[s.index.year == 2021].mean()) if (s.index.year == 2021).any() else np.nan
    m1019 = float(s[(s.index.year >= 2010) & (s.index.year <= 2019)].mean())
    mall = float(s.mean())
    first = int(s.index.year.min())
    rows.append(dict(series=sid, label=label, unit=unit, latest_date=str(latest_d.date()), latest=round(latest, 2),
                     mean_2021=round(m21, 2), mean_2010_2019=round(m1019, 2), mean_full=round(mall, 2), sample_from=first))
    print(f"{sid:12s} {label:32s} latest {latest:6.2f} ({latest_d.date()}) | 2021 {m21:6.2f} | 2010-19 {m1019:6.2f} | since {first} {mall:6.2f}")
pd.DataFrame(rows).to_csv(os.path.join(DATA, "split_determinants_market.csv"), index=False)

# ---------------- (C) the build-lag markup ----------------
print("\n=== investment share (g + delta) * v * (1+g)^J : growth g, depreciation delta, capital-output v, build lag J ===")
rows = []
for g in (0.02, 0.05, 0.08):
    for J in (0, 2, 5, 10):
        for v, d, kind in ((3.0, 0.055, "economy-wide (v=3, delta=5.5%)"), (12.0, 0.015, "structures-heavy conversion (v=12, delta=1.5%)"),
                           (1.0, 0.25, "short-lived IT/AI capital (v=1, delta=25%)")):
            share = (g + d) * v * (1 + g) ** J
            rows.append(dict(g=g, J=J, v=v, delta=d, kind=kind, inv_share=round(share, 3), pipeline_stock_over_Y=round(J * share, 3)))
tab = pd.DataFrame(rows)
tab.to_csv(os.path.join(DATA, "split_determinants_buildlag.csv"), index=False)
print(tab[tab.J.isin([0, 5])].pivot_table(index=["kind", "g"], columns="J", values="inv_share").round(3).to_string())
