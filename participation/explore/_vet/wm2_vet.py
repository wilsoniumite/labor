# wm2_vet.py — adversarial checks of candidate WM-2 (gap W-M 25-54 countercyclical). Explore half only, manifest data.
from __future__ import annotations
import os, sys, itertools
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "women_men"))
import common as cm  # read-only reuse of the explorer's loader
N = [0]
def _count(n=1, what=""):  # do not write to the explorer's ledger
    N[0] += n
cm.count = _count

df = cm.panel()
GAP = [(1, "AW2554"), (-1, "AM2554")]
out = []
def run(*a, **k):
    r = cm.reg(df, *a, **k); out.append(cm.fmt(r)); print(out[-1]); return r

run(GAP, "U2554_lfs", side=+1, label="base")
# sample of the 'with q' run, without q
d_q = df[np.isfinite(df["logq_l1"])]
r = cm.reg(d_q, GAP, "U2554_lfs", side=+1, label="base on q-sample, no q"); out.append(cm.fmt(r)); print(out[-1])
r = cm.reg(d_q, GAP, "U2554_lfs", side=+1, extra_breaks=["logq_l1"], label="q-sample, q breaks, no q"); out.append(cm.fmt(r)); print(out[-1])
run(GAP, "U2554_lfs", side=+1, use_breaks=False, label="no break dummies")
for yrs in ((1997, 2008), (2009, 2019), (2009, 2025), (2005, 2025), (2000, 2025), (1997, 2019)):
    run(GAP, "U2554_lfs", side=+1, years=yrs, label=f"window {yrs}")
# first differences (within country, consecutive years only)
d = df.reset_index().sort_values(["geo", "year"])
d["gap"] = d.AW2554 - d.AM2554
for c in ("gap", "U2554_lfs", "AW2554", "AM2554"):
    d["d_" + c] = d.groupby("geo")[c].diff()
d["dy"] = d.groupby("geo")["year"].diff()
d.loc[d.dy != 1, ["d_gap", "d_U2554_lfs", "d_AW2554", "d_AM2554"]] = np.nan
d["gap__breaks"] = [sorted(set(a) | set(b)) for a, b in zip(d["AW2554__breaks"], d["AM2554__breaks"])]
for c in ("gap", "U2554_lfs", "AW2554", "AM2554"):
    d["d_" + c + "__breaks"] = d[c + "__breaks"]
dd = d.set_index(["geo", "year"])
r = cm.reg(dd, "d_gap", "d_U2554_lfs", side=+1, label="first differences gap on dU"); out.append(cm.fmt(r)); print(out[-1])
r = cm.reg(dd, "d_AM2554", "d_U2554_lfs", side=-1, label="FD men on dU"); out.append(cm.fmt(r)); print(out[-1])
r = cm.reg(dd, "d_AW2554", "d_U2554_lfs", side=+1, label="FD women on dU"); out.append(cm.fmt(r)); print(out[-1])
# per-country time-series slopes (gap on U, own trend removed)
rows = []
for g, x in d.dropna(subset=["gap", "U2554_lfs"]).groupby("geo"):
    X = np.column_stack([np.ones(len(x)), x.year - 2010, x.U2554_lfs])
    b = np.linalg.lstsq(X, x.gap.to_numpy(), rcond=None)[0]
    X0 = np.column_stack([np.ones(len(x)), x.U2554_lfs]); b0 = np.linalg.lstsq(X0, x.gap.to_numpy(), rcond=None)[0]
    rows.append(dict(geo=g, n=len(x), slope_raw=round(b0[1], 3), slope_detrended=round(b[2], 3),
                     yrs=f"{x.year.min()}-{x.year.max()}", sdU=round(x.U2554_lfs.std(), 2)))
T = pd.DataFrame(rows); out.append(T.to_string()); print(T.to_string())
out.append(f"positive raw {int((T.slope_raw>0).sum())}/16; positive detrended {int((T.slope_detrended>0).sum())}/16")
print(out[-1])
# leave-two-out max p
G = cm.GEOS; worst = (0, None)
for a, b in itertools.combinations(G, 2):
    r = cm.reg(df, GAP, "U2554_lfs", side=+1, geos=[x for x in G if x not in (a, b)], B=999)
    if r["p"] > worst[0]: worst = (r["p"], (a, b), r["beta"])
out.append(f"leave-two-out worst: p={worst[0]:.3f} drop {worst[1]} beta={worst[2]:.3f}"); print(out[-1])
# MDE on 15: random 15-of-16 subsets
ses = []
for g in G:
    r = cm.reg(df, GAP, "U2554_lfs", side=+1, geos=[x for x in G if x != g], B=199)
    ses.append(r["se"])
from inference import mde
out.append(f"LOO se median {np.median(ses):.3f} max {np.max(ses):.3f}; MDE(15, a=.05) median {mde(np.median(ses),15):.3f}; "
           f"MDE(15, a=.01 Holm-first) {mde(np.median(ses),15,alpha=0.01):.3f}; MDE(15,a=.0125) {mde(np.median(ses),15,alpha=0.0125):.3f}")
print(out[-1])
from scipy import stats
for beta in (0.231, 0.15, 0.10):
    se = np.median(ses); t = beta / se
    for a in (0.05, 0.01):
        pw = 1 - stats.t.cdf(stats.t.ppf(1 - a, 14) - t, 14)
        out.append(f"power beta={beta} alpha={a}: {pw:.2f}"); print(out[-1])
out.append(f"specifications estimated in this vet (incl. LOO/L2O): {N[0]}")
open(os.path.join(HERE, "wm2_vet.txt"), "w").write("\n".join(out) + "\n")
