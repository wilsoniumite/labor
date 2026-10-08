# s04_cycle.py — the added-worker effect: women's participation and the cycle, especially 2008-2013.
# In the model's household reading (App B, pooled household), a fall in the first earner's income (job loss, or
# lower w1) raises the second earner's participation: d threshold / d(A + w1) < 0. The standard unitary-household
# model says the same (added-worker effect). Discouraged-worker effects pull the other way.
# Out: s04_cycle.txt, fig06_added_worker.png
from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as cm  # noqa: E402

W, M, GREY, INK, MUTED = "#eb6834", "#2a78d6", "#8a8984", "#0b0b0b", "#52514e"
df = cm.panel()
um = cm.series_x("urgan", sex="M", age="Y25-54")      # X: men's unemployment 25-54 (understanding only)
uf = cm.series_x("urgan", sex="F", age="Y25-54")
df["UM2554_x"] = um.reindex(df.index).to_numpy(float)
df["UF2554_x"] = uf.reindex(df.index).to_numpy(float)
out = []


def run(*a, **k):
    r = cm.reg(df, *a, **k)
    out.append(cm.fmt(r))
    print(out[-1])
    return r


# participation on the cycle (U 25-54, lfsa_urgan, both sexes), FE + breaks, 1997-2025
run("AW2554", "U2554_lfs", side=+1, label="W 25-54 on U25-54 (all years)")
run("AM2554", "U2554_lfs", side=-1, label="M 25-54 on U25-54 (all years)")
run([(1, "AW2554"), (-1, "AM2554")], "U2554_lfs", side=+1, label="W-M 25-54 on U25-54 (all years)")
run([(1, "AW2554"), (-1, "AM2554")], "U2554_lfs", side=+1, years=(2005, 2016), label="W-M on U25-54, 2005-2016")
run("AW2554", "U2554_lfs", side=+1, years=(2005, 2016), label="W on U25-54, 2005-2016")
run("AW2554", "UM2554_x", side=+1, label="W 25-54 on men's U 25-54 (X)")
run("AW2554", "UM2554_x", ["UF2554_x"], side=+1, label="W 25-54 on men's U, women's U held (X)")
run([(1, "AW2554"), (-1, "AM2554")], "U2554_lfs", ["logq_l1"], side=+1, label="W-M on U25-54, with q")
for b in ("2534", "3544", "4554"):
    run([(1, f"AF{b}"), (-1, f"AM{b}")], "U2554_lfs", side=+1, label=f"W-M {b} on U25-54")

# long changes over the bust: 2008 -> 2013
d = df.reset_index().set_index(["geo", "year"])
rows = []
for g in cm.GEOS:
    def v(c, y):
        try:
            return d.loc[(g, y), c]
        except KeyError:
            return np.nan
    rows.append(dict(geo=g, dU=v("U2554_lfs", 2013) - v("U2554_lfs", 2008), dUM=v("UM2554_x", 2013) - v("UM2554_x", 2008),
                     dAW=v("AW2554", 2013) - v("AW2554", 2008), dAM=v("AM2554", 2013) - v("AM2554", 2008)))
C = pd.DataFrame(rows).set_index("geo")
C["dgap"] = C.dAW - C.dAM
out.append("\n2008->2013 changes (pp):\n" + C.round(2).to_string())
print(out[-1])
c = C.dropna()
s = np.polyfit(c.dUM, c.dgap, 1)
out.append(f"cross-section dgap on dUM: slope {s[0]:.3f}; corr {np.corrcoef(c.dUM, c.dgap)[0,1]:.2f}; "
           f"dAW on dUM corr {np.corrcoef(c.dUM, c.dAW)[0,1]:.2f}; dAM on dUM corr {np.corrcoef(c.dUM, c.dAM)[0,1]:.2f}")
print(out[-1])
open(os.path.join(cm.HERE, "s04_cycle.txt"), "w").write("\n".join(out) + "\n")

fig, ax = plt.subplots(1, 2, figsize=(10, 4))
for a, col, lab in ((ax[0], "dAM", "men"), (ax[1], "dAW", "women")):
    a.axhline(0, color="#c9c8c2", lw=0.8)
    a.scatter(c.dUM, c[col], color=M if lab == "men" else W, s=30, edgecolor="white")
    for g, r in c.iterrows():
        a.annotate(g, (r.dUM, r[col]), fontsize=6.5, color=MUTED, xytext=(3, 2), textcoords="offset points")
    a.set_xlabel("change in men's unemployment 25-54, 2008-2013 (pp)")
    a.set_ylabel(f"change in {lab}'s activity 25-54, 2008-2013 (pp)")
    a.set_ylim(-6, 12)
ax[0].set_title("Men: participation barely moves with the bust", fontsize=9, loc="left", color=INK)
ax[1].set_title("Women: participation rose most where men lost jobs", fontsize=9, loc="left", color=INK)
fig.tight_layout()
fig.savefig(os.path.join(cm.HERE, "fig06_added_worker.png"), dpi=150)
