# s02_rents.py — women's (and men's) prime-age participation and q = CP041 / IGD_NNRG, lagged.
# Replicates the frozen C-3 legs on the explore half, then varies the window (long window with the lfsa_urgan cycle),
# the age band, and looks at what drives the sign (country trends in q vs in women's participation).
# Out: s02_rents.txt, fig04_q_and_women.png
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
B = 9999
df = cm.panel()
out = []


def run(*a, **k):
    r = cm.reg(df, *a, B=B, **k)
    out.append(cm.fmt(r))
    print(out[-1])
    return r


Q = "logq_l1"
# frozen replication (should match results/specs_explore.json C3a/C3b)
run([(1, "AW2554"), (-1, "AM2554")], Q, ["U"], label="C3a frozen: W-M 25-54 on q, U(une_rt_a)")
run("AW2554", Q, ["U"], label="C3b frozen: W 25-54 on q")
run("AM2554", Q, ["U"], label="men 25-54 on q, U")
# long window: lfsa_urgan cycle for all countries, 1997-2025
run([(1, "AW2554"), (-1, "AM2554")], Q, ["U_lfs"], label="W-M 25-54 on q, U_lfs, 1997-2025")
run("AW2554", Q, ["U_lfs"], label="W 25-54 on q, U_lfs, 1997-2025")
run("AM2554", Q, ["U_lfs"], label="M 25-54 on q, U_lfs, 1997-2025")
# by age band (women), long window
for b in ("2534", "3544", "4554"):
    run(f"AF{b}", Q, ["U_lfs"], label=f"W {b} on q, U_lfs")
    run(f"AM{b}", Q, ["U_lfs"], label=f"M {b} on q, U_lfs")
# with country trends (does the sign come from differential trends?)
run("AW2554", Q, ["U_lfs"], trends=True, label="W 25-54 on q, U_lfs, country trends")
run([(1, "AW2554"), (-1, "AM2554")], Q, ["U_lfs"], trends=True, label="W-M on q, U_lfs, country trends")

open(os.path.join(cm.HERE, "s02_rents.txt"), "w").write("\n".join(out) + "\n")

# descriptive: long change in q vs long change in women's participation, 2005 -> 2019
d = df.reset_index()
rows = []
for g in cm.GEOS:
    x = d[d.geo == g].set_index("year")
    def ch(c, a, b):
        return x[c].get(b, np.nan) - x[c].get(a, np.nan)
    rows.append(dict(geo=g, dq=ch("logq", 2005, 2019), dAW=ch("AW2554", 2006, 2019), dAM=ch("AM2554", 2006, 2019),
                     AW2006=x["AW2554"].get(2006, np.nan)))
C = pd.DataFrame(rows).set_index("geo")
print(C.round(3).to_string())
c = C.dropna()
print("corr(dq, dAW)", np.corrcoef(c.dq, c.dAW)[0, 1].round(2), "corr(dq, AW2006)", np.corrcoef(c.dq, c.AW2006)[0, 1].round(2),
      "corr(dAW, AW2006)", np.corrcoef(c.dAW, c.AW2006)[0, 1].round(2))
fig, ax = plt.subplots(1, 2, figsize=(10, 4))
for g in cm.GEOS:
    x = d[d.geo == g].sort_values("year")
    ax[0].plot(x.year, x.logq - x.logq[x.year == 2015].mean(), color=GREY, lw=0.9)
    ax[0].annotate(g, (x.year.max(), (x.logq - x.logq[x.year == 2015].mean()).dropna().iloc[-1]), fontsize=6.5,
                   color=MUTED, xytext=(2, 0), textcoords="offset points")
ax[0].axhline(0, color="#c9c8c2", lw=0.8)
ax[0].set_title("log q (rents / non-energy goods), 2015 = 0", fontsize=9, loc="left", color=INK)
ax[1].scatter(c.dq, c.dAW, color=W, s=30, edgecolor="white", label="women")
ax[1].scatter(c.dq, c.dAM, color=M, s=30, edgecolor="white", label="men")
for g, r in c.iterrows():
    ax[1].annotate(g, (r.dq, r.dAW), fontsize=6.5, color=MUTED, xytext=(3, 2), textcoords="offset points")
ax[1].axhline(0, color="#c9c8c2", lw=0.8)
ax[1].set_xlabel("change in log q, 2005-2019")
ax[1].set_ylabel("change in activity 25-54, 2006-2019 (pp)")
ax[1].legend(frameon=False, fontsize=8)
ax[1].set_title("Long changes: q against participation", fontsize=9, loc="left", color=INK)
fig.tight_layout()
fig.savefig(os.path.join(cm.HERE, "fig04_q_and_women.png"), dpi=150)
