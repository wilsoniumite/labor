# wm1_vet.py — adversarial checks of candidate WM-1 (women_men): AW2554 on logq_l1 x O_c (outright owners 55-64),
# country trends. Explore half only, via the explorer's common.py loader (read-only; its spec counter is disabled
# here so their ledger is untouched). Out: wm1_vet.txt
import os, sys, warnings
warnings.filterwarnings('ignore')
import numpy as np, pandas as pd
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "explore", "women_men"))
import common as cm
NV = [0]
def _count(n=1, what=""):
    NV[0] += n
cm.count = _count

df = cm.panel()
cl = cm.data.panel()[1]
geo = df.index.get_level_values(0)
yr = df.index.get_level_values(1)
def zs(s): return (s - s.mean()) / s.std(ddof=0)
O = zs(cl["owner_outright_5564"])
for qn in ("logq_l1", "logq_f1", "logq_cp00_l1", "logq_hpi_l1", "logq_comp_l1"):
    df["X_" + qn] = df[qn].to_numpy() * geo.map(O).to_numpy(float)
Obin = (cl["owner_outright_5564"] > cl["owner_outright_5564"].median()).astype(float)
df["QxObin"] = df["logq_l1"].to_numpy() * geo.map(Obin).to_numpy(float)
Orank = zs(cl["owner_outright_5564"].rank())
df["QxOrank"] = df["logq_l1"].to_numpy() * geo.map(Orank).to_numpy(float)
cee = {"BG", "EE", "HR", "HU", "LV", "PL"}
df["QxCEE"] = df["logq_l1"].to_numpy() * np.isin(geo, list(cee)).astype(float)
# stratum x year FE column
strat = cl["stratum"]
df["sy"] = [f"{strat[g]}_{y}" for g, y in zip(geo, yr)]
df["t"] = (yr.to_numpy(float) - 2010) / 10

out = []
def say(s):
    out.append(str(s)); print(s, flush=True)
def run(y, x, ctrl=("U_lfs",), side=-1, **k):
    r = cm.reg(df, y, x, list(ctrl), side=side, **k)
    say(cm.fmt(r)); return r

say(cl[["stratum", "owner_outright_5564"]].assign(O=O).round(2).to_string())
say("\n== base and the trend choice")
run("AW2554", ["X_logq_l1", "logq_l1"], label="base (trends)", trends=True)
run("AW2554", ["X_logq_l1", "logq_l1"], label="no trends (protocol's main form)")
run("AW2554", ["X_logq_l1", "logq_l1"], label="no trends, 2005-2025", years=(2005, 2025))

say("\n== region: is it a CEE x q term?")
run("AW2554", ["QxCEE", "logq_l1"], label="q x CEE dummy, trends", trends=True)
run("AW2554", ["QxObin", "logq_l1"], label="q x 1[O > median], trends", trends=True)
run("AW2554", ["QxOrank", "logq_l1"], label="q x rank(O) sd, trends", trends=True)
nc = [g for g in cm.GEOS if g not in cee]
run("AW2554", ["X_logq_l1", "logq_l1"], label="base within non-CEE only (10 countries)", trends=True, geos=nc)
run("AW2554", ["X_logq_l1", "logq_l1"], label="base within CEE only (6 countries)", trends=True, geos=sorted(cee))

say("\n== timing: lead of q x O added (placebo; should be ~0)")
r = cm.reg(df, "AW2554", ["X_logq_l1", "logq_l1"], ["U_lfs", "X_logq_f1", "logq_f1"], side=-1, trends=True,
           label="base + lead q_{t+1} and lead x O")
say(cm.fmt(r))
r = cm.reg(df, "AW2554", ["X_logq_f1", "logq_f1"], ["U_lfs", "X_logq_l1", "logq_l1"], side=-1, trends=True,
           label="  -> coefficient on lead x O")
say(cm.fmt(r))
run("AW2554", ["X_logq_f1", "logq_f1"], label="lead x O alone (instead of lag), trends", trends=True)

say("\n== alternative q measures (C6 robustness)")
for qn in ("logq_cp00_l1", "logq_hpi_l1", "logq_comp_l1"):
    run("AW2554", ["X_" + qn, qn], label=f"q={qn}, trends", trends=True)

say("\n== windows")
d0 = df.copy()
keep = ~np.isin(yr, list(range(2008, 2014)))
_df = df
df = _df[keep]
run("AW2554", ["X_logq_l1", "logq_l1"], label="excl 2008-2013, trends", trends=True)
df = _df
run("AW2554", ["X_logq_l1", "logq_l1"], label="2009-2025 (frozen U window), U_lfs, trends", trends=True, years=(2009, 2025))
run("AW2554", ["X_logq_l1", "logq_l1"], label="1997-2015 , trends", trends=True, years=(1997, 2015))

say("\n== trend flexibility")
df["t2"] = df["t"] ** 2
Mg = pd.get_dummies(pd.Series(geo), dtype=float).to_numpy()
for j, g in enumerate(sorted(set(geo))):
    df[f"tq_{g}"] = (geo == g) * df["t2"].to_numpy()
qtr = [f"tq_{g}" for g in sorted(set(geo))][1:]
run("AW2554", ["X_logq_l1", "logq_l1"], ctrl=["U_lfs"] + qtr, label="country quadratic trends", trends=True)
SY = pd.get_dummies(df["sy"], dtype=float)
SY = SY.loc[:, [c for c in SY.columns if not c.startswith("CEE")]]  # CEE x year as the base within each year
sycols = []
for c in SY.columns:
    df["sy_" + c] = SY[c].to_numpy(); sycols.append("sy_" + c)
run("AW2554", ["X_logq_l1", "logq_l1"], ctrl=["U_lfs"] + sycols, label="stratum x year FE, no trends")
run("AW2554", ["X_logq_l1", "logq_l1"], ctrl=["U_lfs"] + sycols, label="stratum x year FE + trends", trends=True)

say("\n== outcomes")
run("AW2554_all", ["X_logq_l1", "logq_l1"], label="all residents, trends", trends=True)
for a in ("2534", "3544", "4554"):
    run(f"AF{a}", ["X_logq_l1", "logq_l1"], label=f"women {a}, trends", trends=True)
run("AM2554", ["X_logq_l1", "logq_l1"], label="men 25-54, trends", trends=True)
run([(1, "AW2554"), (-1, "AM2554")], ["X_logq_l1", "logq_l1"], label="W-M, trends", trends=True)

say("\n== leave-two-out (worst pairs, B=999)")
res = []
G = cm.GEOS
for i in range(len(G)):
    for j in range(i + 1, len(G)):
        gg = [g for g in G if g not in (G[i], G[j])]
        r = cm.reg(df, "AW2554", ["X_logq_l1", "logq_l1"], ["U_lfs"], side=-1, trends=True, geos=gg, B=999,
                   label=f"L2O {G[i]}{G[j]}")
        res.append((G[i] + "-" + G[j], round(r["beta"], 2), round(r["p"], 3)))
res.sort(key=lambda t: -t[2])
say("worst 10 by p: " + str(res[:10]))
say(f"share of pairs with p > 0.10: {np.mean([t[2] > 0.10 for t in res]):.2f}")

say(f"\nvet specs estimated: {NV[0]}")
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "wm1_vet.txt"), "w").write("\n".join(out) + "\n")
