# slopes.py — the D1 picture: each explore country's own slope of A(25-34) on log q_{t-1}, from one pooled
# regression with common year effects, the cycle control, C3 break dummies and q x country interactions; with and
# without country linear trends; long window (lfsa_urgan U, 1997+) and the frozen window (une_rt_a U).
# The country slopes are descriptive (no bootstrap; se = within-country HC1 of the pooled fit, indicative only).
# Out: fig/country_slopes.png, slopes.json

import json
import os

import numpy as np
import pandas as pd

import common as C

raw, cy, cl = C.load()
cyl = C.with_lfs_cycle(raw, cy)
plt = C.style()
geos = sorted(set(cy.index.get_level_values(0)))
fstd = C.specs.f_constants(cl, geos)
ctx = C.specs.Ctx(cl, fstd)
spec = dict(C.specs.TESTS["D2"])           # A2534 on Q with U; all 16 countries (HR has no F)


def country_slopes(frame, trends, years=None, ycol=None, label=""):
    s = dict(spec)
    if years:
        s["years"] = years
    if ycol:
        s["outcome"] = [(1, ycol)]
    fr = C.specs.frame(frame, s, ctx, geos)
    M = fr["M"]
    q = M["z0"].to_numpy(float)                      # D2's z0 is log q_{t-1}
    G = sorted(set(M.geo))
    Xq = np.column_stack([(M.geo.to_numpy() == g) * q for g in G])
    blocks = [C.inf.fe_matrix(M, ["geo", "year"]), M[["c0"]].to_numpy(float),
              C.specs.break_dummies(M, fr["breaks"])]
    if trends:
        t = (M.year.to_numpy(float) - 2010) / 10
        blocks.append(np.column_stack([(M.geo.to_numpy() == g) * t for g in G]))
    X = np.column_stack([np.ones(len(M)), Xq] + blocks)
    y = M["y"].to_numpy(float)
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    e = y - X @ b
    XtXi = np.linalg.pinv(X.T @ X)
    V = XtXi @ (X.T * e ** 2) @ X @ XtXi * len(y) / (len(y) - np.linalg.matrix_rank(X))
    res = {}
    for i, g in enumerate(G):
        res[g] = dict(slope=float(b[1 + i]), se=float(np.sqrt(V[1 + i, 1 + i])), n=int((M.geo == g).sum()),
                      years=[int(M.year[M.geo == g].min()), int(M.year[M.geo == g].max())])
    C.log_spec(f"country slopes {label}", dict(beta=np.nan, se=np.nan, p=np.nan, p_opposite=np.nan, n=len(y),
                                               G=len(G), G_star=np.nan, years_used=list(M.year), geos_used=G))
    return res


runs = {
    "long, no trends": country_slopes(cyl, False, label="long no trends"),
    "long, country trends": country_slopes(cyl, True, label="long trends"),
    "frozen window, no trends": country_slopes(cy, False, label="frozen no trends"),
    "frozen window, country trends": country_slopes(cy, True, label="frozen trends"),
}
for k, r in runs.items():
    print(k)
    rows = sorted(r.items(), key=lambda kv: cl.loc[kv[0], "F_raw"] if np.isfinite(cl.loc[kv[0], "F_raw"]) else 99)
    for g, v in rows:
        print(f"   {g} F={cl.loc[g, 'F_raw']:5.1f} slope={v['slope']:+7.2f} se={v['se']:5.2f} n={v['n']} {v['years']}")
    F = np.array([cl.loc[g, "F_raw"] for g in r])
    sl = np.array([r[g]["slope"] for g in r])
    ok = np.isfinite(F)
    w = ok & (np.abs(sl) < 100)
    print("   corr(slope, F) =", round(float(np.corrcoef(F[ok], sl[ok])[0, 1]), 3),
          " Spearman =", round(float(pd.Series(F[ok]).corr(pd.Series(sl[ok]), method="spearman")), 3))
json.dump(runs, open(os.path.join(C.HERE, "slopes.json"), "w"), indent=1)

fig, axs = plt.subplots(1, 2, figsize=(10, 4.2))
for ax, k in zip(axs, ("long, no trends", "long, country trends")):
    r = runs[k]
    for g, v in r.items():
        F = cl.loc[g, "F_raw"]
        if not np.isfinite(F):
            continue
        col = C.ORANGE if g in C.CEE else C.BLUE
        ax.errorbar(F, v["slope"], yerr=1.0 * v["se"], fmt="o", color=col, ms=5, lw=1, capsize=0)
        ax.annotate(g, (F, v["slope"]), xytext=(4, 3), textcoords="offset points", fontsize=7, color=C.INK)
    ax.axhline(0, color=C.GRAY, lw=0.8)
    ax.set_xlabel("F_raw: % of 25-34 living with parents, first SILC years 2003-2008")
    ax.set_ylabel("slope of activity 25-34 on log q (pp per log point)")
    ax.set_title(f"Country slopes, 1997-2025, lfsa_urgan U ({k.split(', ')[1]})", loc="left")
axs[0].plot([], [], "o", color=C.BLUE, label="West/South/Nordic")
axs[0].plot([], [], "o", color=C.ORANGE, label="CEE")
axs[0].legend(loc="upper left")
fig.tight_layout()
fig.savefig(os.path.join(C.FIG, "country_slopes.png"), dpi=130)
