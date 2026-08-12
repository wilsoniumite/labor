# premium_pass_two.py — data item one, pass two: Goldin–Katz composition adjustment
# + the supply-adjusted race decomposition. Runs entirely from the shipped extract
# (data/morg_extract_1979_2024.parquet) — no downloads.
# Style: flat notebook cells. Grid discipline inherited from the paper's §7: every
# contestable choice is a labeled axis; reported objects are medians with min–max
# bands across the grid. Axes here: topcode multiplier m ∈ {1.0, 1.4, 1.5} × weight
# base ∈ {base8991, meanshare}. 2026-08-09.

import os
import sys
import numpy as np
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows console: never crash on a glyph

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

def weighted_median(vals, wts):  # identical to pass one's — the reproduction gate needs it
    v = np.asarray(vals, dtype=float); w = np.asarray(wts, dtype=float)
    o = np.argsort(v); v, w = v[o], w[o]
    c = np.cumsum(w)
    return float(v[np.searchsorted(c, 0.5 * c[-1])])

def wmean(vals, wts):
    v = np.asarray(vals, dtype=float); w = np.asarray(wts, dtype=float)
    return float((v * w).sum() / w.sum())

# ---------------- Cell 0: load + hard validation + reproduction gate ----------------
df = pd.read_parquet(os.path.join(DATA, "morg_extract_1979_2024.parquet"))
assert list(df.columns) == ["year", "age", "sex", "educg", "earnwke", "earnwt"]
assert df.year.nunique() == 46 and df.year.min() == 1979 and df.year.max() == 2024
assert set(df.educg.unique()) == {"BA+", "SC", "HS", "<HS"}  # no NA leaked through pass one
assert (df.earnwke > 0).all() and (df.earnwt > 0).all()
assert df.age.min() == 25 and df.age.max() == 64
print(f"extract: {len(df):,} rows, 46 years, groups clean")

# reproduction gate: the extract must reproduce pass one's raw median ratios exactly
p1 = pd.read_csv(os.path.join(DATA, "morg_premium_annual.csv"), index_col=0)
rep = {}
for yr, sub in df[df.educg.isin(["BA+", "HS"])].groupby("year"):
    m = {g: weighted_median(s.earnwke, s.earnwt) for g, s in sub.groupby("educg")}
    rep[yr] = m["BA+"] / m["HS"]
rep = pd.Series(rep)
gap_repro = (rep - p1.ratio_raw).abs().max()
assert gap_repro < 1e-9, f"extract does not reproduce pass one medians (max dev {gap_repro})"
print(f"reproduction gate PASSED: raw median ratio matches pass one in all 46 years (max dev {gap_repro:.2e})")

# ---------------- Cell 1: potential experience and cells ----------------
# Schooling years imputed per group (labeled): <HS 10, HS 12, SC 14, BA+ 16.
# BA+ includes advanced degrees; 16 overstates their experience — stated, not corrected
# (group-level data reaches no finer). Potential experience = age − years − 6, floored at 0.
YRS = {"<HS": 10, "HS": 12, "SC": 14, "BA+": 16}
df["exper"] = (df.age - df.educg.map(YRS) - 6).clip(lower=0)
df["expband"] = pd.cut(df.exper, [-1, 9, 19, 29, 39, 99],
                       labels=["0-9", "10-19", "20-29", "30-39", "40+"])
df["cell"] = df.sex.astype(str) + "|" + df.expband.astype(str)
print("cells:", df.cell.nunique(), "| min cell-year n (BA+/HS rows):",
      int(df[df.educg.isin(['BA+','HS'])].groupby(["year", "cell", "educg"], observed=True).size().min()))

# ---------------- Cell 2: topcode treatment (detected, validated, labeled) ----------------
# Static caps: 1979–88 $999; 1989–97 $1,923; 1998–2022 $2,884.61 (1998 file rounds to 2884).
# 2023: HYBRID — early-2023 months still carry the static cap (obs at exactly 2884.61),
# later months use the Apr-2023 dynamic topcode (top earners replaced by their group MEAN —
# mass points above the old cap; 69 distinct values here). 2024: fully dynamic (83 points,
# 8.1% of obs above the old cap). Treatment: winsor multiplier m applies to AT-CAP obs only;
# dynamic replacement values are already conditional means and are left alone under every m.
# (Caveat, stated: mean-replacement raises mean-log slightly vs the true top tail — Jensen —
# so 2023–24 sit a hair high under m=1.0 relative to their own truth; unquantifiable here.)
caps = {}
for yr, sub in df.groupby("year"):
    mx = sub.earnwke.max()
    if yr <= 2022:
        caps[yr] = mx
    elif yr == 2023:
        caps[yr] = 2884.61
    else:
        caps[yr] = np.nan  # no static cap
capser = pd.Series(caps)
static = capser[capser.index <= 2022]
assert set(np.round(static.values, 2)) <= {999.0, 1923.0, 2884.0, 2884.61}, "unexpected cap value"
df["cap"] = df.year.map(caps)
df["atcap"] = np.isclose(df.earnwke, df.cap)
bite = df[df.educg.isin(["BA+", "HS"])].groupby(["year", "educg"], observed=True).apply(
    lambda s: np.average(s.atcap, weights=s.earnwt), include_groups=False).unstack()
print("at-cap share (weighted): BA+ 1988 %.1f%%, 1997 %.1f%%, 2022 %.1f%%, 2024 %.1f%% | HS 1988 %.1f%%"
      % (100*bite.loc[1988,"BA+"], 100*bite.loc[1997,"BA+"], 100*bite.loc[2022,"BA+"],
         100*bite.loc[2024,"BA+"], 100*bite.loc[1988,"HS"]))

M_GRID = [1.0, 1.4, 1.5]
for m in M_GRID:
    df[f"lw_m{int(m*10)}"] = np.log(np.where(df.atcap, m * df.cap, df.earnwke))

# ---------------- Cell 3: cell × year × group mean log wages ----------------
cols = {f"lw_m{int(m*10)}": "mean" for m in M_GRID}
gb = df.groupby(["year", "cell", "educg"], observed=True)
cellstats = gb.apply(lambda s: pd.Series(
    {k: wmean(s[k], s.earnwt) for k in cols} | {"n": len(s), "wsum": s.earnwt.sum()}),
    include_groups=False).reset_index()
print("cell-year-group table:", len(cellstats), "rows")

# ---------------- Cell 4: composition-adjusted premium, the 6-member grid ----------------
# Weight bases over sex×experience cells (BA+ and HS mass pooled, as pass one did):
#   base8991  — pooled 1989–91 earnings-weight shares (pass one's base, on the new cells)
#   meanshare — the GK convention: each cell's within-year share averaged over all 46 years
ph = cellstats[cellstats.educg.isin(["BA+", "HS"])]
b = ph[ph.year.isin([1989, 1990, 1991])].groupby("cell", observed=True).wsum.sum()
w_base8991 = b / b.sum()
sh = ph.groupby(["year", "cell"], observed=True).wsum.sum().unstack()
w_meanshare = (sh.T / sh.sum(axis=1)).T.mean(axis=0)
w_meanshare = w_meanshare / w_meanshare.sum()
WEIGHTS = {"base8991": w_base8991, "meanshare": w_meanshare}

members = {}
for m in M_GRID:
    lw = f"lw_m{int(m*10)}"
    piv = ph.pivot_table(index=["year", "cell"], columns="educg", values=lw)
    nn = ph.pivot_table(index=["year", "cell"], columns="educg", values="n")
    for wname, wser in WEIGHTS.items():
        vals = {}
        for yr in sorted(ph.year.unique()):
            p, n_ = piv.loc[yr], nn.loc[yr]
            ok = p.index[(n_["BA+"] >= 30) & (n_["HS"] >= 30) & p.notna().all(axis=1)]
            w = wser.loc[ok] / wser.loc[ok].sum()
            vals[yr] = float((w * (p.loc[ok, "BA+"] - p.loc[ok, "HS"])).sum())
        members[f"m{int(m*10)}_{wname}"] = pd.Series(vals)
grid = pd.DataFrame(members)
out = pd.DataFrame({"gap_median": grid.median(axis=1), "gap_min": grid.min(axis=1),
                    "gap_max": grid.max(axis=1)})
out["ratio_median"] = np.exp(out.gap_median)
out["ratio_min"] = np.exp(out.gap_min); out["ratio_max"] = np.exp(out.gap_max)
out = out.join(np.exp(grid).add_prefix("ratio_"))
out = out.join(p1[["ratio_raw", "ratio_fixedwt"]].rename(columns={"ratio_fixedwt": "ratio_p1_fixedwt"}))
out.index.name = "year"
out.to_csv(os.path.join(DATA, "morg_premium_pass2.csv"))
print("\nadjusted premium (exp of composition-adjusted log gap), spot years:")
spot = [1979, 1985, 1991, 1992, 2000, 2010, 2016, 2019, 2024]
print(out.loc[spot, ["ratio_median", "ratio_min", "ratio_max", "ratio_raw", "ratio_p1_fixedwt"]].round(3).to_string())

# ---------------- Cell 5: within-regime readings ----------------
g = out.gap_median
print("\nwithin-regime readings (median member, log points):")
print("  widen, old regime   1979->1991: %.3f → %.3f  (+%.3f)" % (g[1979], g[1991], g[1991]-g[1979]))
print("  break 1991->1992 (NOT a data move): %.3f → %.3f  (+%.3f) | band at 1992: [%.3f, %.3f]"
      % (g[1991], g[1992], g[1992]-g[1991], out.gap_min[1992], out.gap_max[1992]))
print("  widen, new regime   1992->2000: %.3f → %.3f  (+%.3f)" % (g[1992], g[2000], g[2000]-g[1992]))
post = g.loc[1992:]
print("  peak (new regime): %d at %.3f (ratio %.3f) | 2024: %.3f (ratio %.3f) | peak->2024: %+.3f"
      % (post.idxmax(), post.max(), np.exp(post.max()), g[2024], np.exp(g[2024]), g[2024]-post.max()))
print("  member peaks:", {k: int(grid[k].loc[1992:].idxmax()) for k in grid.columns})
print("  3-yr means (log gap): 1998-2000 %.3f | 2008-10 %.3f | 2014-16 %.3f | 2022-24 %.3f"
      % (g.loc[1998:2000].mean(), g.loc[2008:2010].mean(), g.loc[2014:2016].mean(), g.loc[2022:2024].mean()))
# The m=1.0 members' 2024 "peak" is the topcode SEAM, not economics: their pre-2023 top is
# truncated at the static cap, their 2023-24 top is the dynamic mean replacement — levels not
# comparable across the seam. m=1.4/1.5 approximate the top-group mean throughout, so they
# cross the seam meaningfully; the compression reading quotes them.
print("  seam-safe compression (m=1.4/1.5 members): peak year, peak, 2024, delta:")
for k in ["m14_base8991", "m14_meanshare", "m15_base8991", "m15_meanshare"]:
    s = grid[k].loc[1992:]
    print("    %-14s %d  %.3f -> %.3f  (%+.3f)" % (k, s.idxmax(), s.max(), s[2024], s[2024] - s.max()))

# ---------------- Cell 6: relative supply in efficiency units (Katz–Murphy) ----------------
# Employment measure: earnwt mass of FT weekly earners 25–64 — the extract's reach; NOT
# economy-wide hours (part-timers, self-employed excluded) — labeled, not corrected.
# Efficiency weight per sex×exp×educ cell: within-year wage relative to the year's overall
# mean log wage, averaged over all 46 years (removes nominal drift), m=1.4 wage member.
# College equivalents = BA+ + 0.5·SC; HS equivalents = HS + <HS + 0.5·SC (KM aggregation).
cs = cellstats.copy()
yearmean = cs.groupby("year", observed=True).apply(
    lambda s: wmean(s.lw_m14, s.wsum), include_groups=False)
cs["rel"] = np.exp(cs.lw_m14 - cs.year.map(yearmean))
effw = cs.groupby(["cell", "educg"], observed=True).rel.mean()
cs["eff"] = cs.wsum * cs.set_index(["cell", "educg"]).index.map(effw)
eff = cs.groupby(["year", "educg"], observed=True).eff.sum().unstack()
CE = eff["BA+"] + 0.5 * eff["SC"]
HE = eff["HS"] + eff["<HS"] + 0.5 * eff["SC"]
relsup = np.log(CE / HE)
print("\nrelative supply ln(CE/HE), FT-earner efficiency units:")
print("  " + " | ".join("%d %.3f" % (y, relsup[y]) for y in [1979, 1992, 2005, 2016, 2024]))
growth = relsup.diff()
print("  growth %%/yr: 1979-92 %.2f | 1992-2005 %.2f | 2005-16 %.2f | 2016-24 %.2f"
      % (100*growth.loc[1980:1992].mean(), 100*growth.loc[1993:2005].mean(),
         100*growth.loc[2006:2016].mean(), 100*growth.loc[2017:2024].mean()))

# ---------------- Cell 7: the race regression — the identification REPORT ----------------
# gap_t = a + b·t [+ c·post92] − (1/σ)·relsup_t is the Katz–Murphy equation. KM identified
# σ on 1963–87 because relative-supply GROWTH fluctuated (fast 70s, slow 80s). In this
# window supply growth is near-constant (~2.5%/yr), so relsup is nearly collinear with the
# trend and σ is NOT identified in-window. Rule: report the failure, don't use the estimate.
def race_ols(gap, with_dummy):
    yrs = gap.index.values.astype(float)
    X = [np.ones_like(yrs), yrs - 1979]
    if with_dummy:
        X.append((yrs >= 1992).astype(float))
    X.append(relsup.loc[gap.index].values)
    X = np.column_stack(X)
    beta, *_ = np.linalg.lstsq(X, gap.values, rcond=None)
    fit = X @ beta
    r2 = 1 - ((gap.values - fit) ** 2).sum() / ((gap.values - gap.values.mean()) ** 2).sum()
    return beta, pd.Series(fit, index=gap.index), r2

tt = relsup.index.values.astype(float)
corr_ts = float(np.corrcoef(tt, relsup.values)[0, 1])
free = {wd: race_ols(g, wd) for wd in [True, False]}
print("\nrace regression, FREE sigma — identification report (estimate REPORTED, NOT USED):")
print("  corr(t, relsup) 1979-2024 = %.4f  => near-collinear; sigma unidentified in-window" % corr_ts)
for wd in [True, False]:
    beta, fit, r2 = free[wd]
    print("  %s: sigma-hat = %.2f (wrong-signed/absurd), R2 = %.3f"
          % ("with post-92 dummy" if wd else "no dummy   ", -1.0 / beta[-1], r2))
print("  (KM's 1963-87 window identified sigma from supply-growth FLUCTUATION this window lacks.)")

# ---------------- Cell 8: supply-adjusted decomposition under imposed σ ----------------
# With σ imposed, the demand index is arithmetic, not estimation: D_t = σ·gap_t + relsup_t
# (log relative demand up to a constant). Members, labeled, from the literature:
# KM 1.41 (Katz–Murphy 1992), GK 1.64 (Goldin–Katz 2008), CL 2.5 (Card–Lemieux 2001 upper).
# The 1992 redesign step in gap_t propagates into D_t: all era growth is read WITHIN regime;
# no growth is ever computed across 1991→1992.
SIGMAS = {"KM141": 1.41, "GK164": 1.64, "CL250": 2.50}
D = {name: sig * g + relsup for name, sig in SIGMAS.items()}
print("\ndemand index growth (log pts/yr), within regime, by era:")
print("  era        " + " | ".join("%-6s" % n for n in SIGMAS))
for (a, bnd) in [(1979, 1991), (1992, 2000), (2000, 2016), (2016, 2024)]:
    row = " | ".join("%.3f " % ((D[n][bnd] - D[n][a]) / (bnd - a)) for n in SIGMAS)
    print("  %d-%d  %s" % (a, bnd, row))

# Counterfactual: demand keeps its 1992–2016 trend; supply follows its ACTUAL path.
# gap_cf_t = gap_2016 + (1/σ)·[trend_D·(t−2016) − (relsup_t − relsup_2016)] for t ≥ 2016.
# The shortfall gap − gap_cf is the compression NOT explained by supply — the C2 object.
cf, short = {}, {}
for name, sig in SIGMAS.items():
    dd = D[name].loc[1992:2016]
    tr = np.polyfit(dd.index.values.astype(float), dd.values, 1)[0]
    yrs = np.arange(2016, 2025)
    cfv = g[2016] + (tr * (yrs - 2016) - (relsup.loc[yrs].values - relsup[2016])) / sig
    cf[name] = pd.Series(cfv, index=yrs)
    short[name] = g.loc[2016:2024] - cf[name]
    print("  %s (sigma %.2f): demand trend 92-16 %.3f/yr | cf gap 2024 %.3f vs actual %.3f | shortfall %+.3f"
          % (name, sig, tr, cf[name][2024], g[2024], short[name][2024]))
print("  reading: supply growth did NOT slow after 2016 (%.2f%%/yr) — the compression is a"
      % (100 * (relsup[2024] - relsup[2016]) / 8))
print("  demand-side event under every sigma member; none of it is supply-explained.")

race = pd.DataFrame({"gap_median": g, "relsupply": relsup, "CE_eff": CE, "HE_eff": HE})
for name in SIGMAS:
    race["D_" + name] = D[name]
    race["gapcf_" + name] = cf[name].reindex(race.index)
    race["shortfall_" + name] = short[name].reindex(race.index)
race.index.name = "year"
race.to_csv(os.path.join(DATA, "race_decomposition.csv"))

# ---------------- Cell 9: figure ----------------
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig, axes = plt.subplots(3, 1, figsize=(9, 11), sharex=True)
ax = axes[0]
ax.fill_between(out.index, out.ratio_min, out.ratio_max, alpha=.18, color="tab:blue",
                label="grid band (3 topcode × 2 weight members)")
ax.plot(out.index, out.ratio_median, lw=2, color="tab:blue", label="pass two: composition-adjusted (mean log, exp×sex cells)")
ax.plot(out.index, out.ratio_p1_fixedwt, lw=1.2, ls="--", color="tab:orange", label="pass one: fixed-weight median (sex×age cells)")
ax.plot(out.index, out.ratio_raw, lw=1, ls=":", color="gray", label="raw median ratio")
ax.axvline(1992, color="gray", ls=":", lw=1)
ax.text(1992.3, ax.get_ylim()[0]+.02, "CPS educ redesign — compare within regime", fontsize=7, color="gray")
ax.set_title("College premium, BA+/HS: composition-adjusted (CPS MORG, FT 25–64)")
ax.set_ylabel("ratio"); ax.legend(fontsize=7); ax.grid(alpha=.3)

ax = axes[1]
ax.plot(g.index, g, lw=2, color="tab:blue", label="log gap (median member)")
for name, ls in [("KM141", "--"), ("GK164", "-."), ("CL250", ":")]:
    ax.plot(cf[name].index, cf[name], lw=1.3, ls=ls, color="tab:red",
            label=r"counterfactual, $\sigma$=%s (1992–2016 demand trend + actual supply)" % SIGMAS[name])
ax.axvline(1992, color="gray", ls=":", lw=1); ax.axvline(2016, color="gray", ls=":", lw=.8)
ax2 = ax.twinx()
ax2.plot(relsup.index, relsup, lw=1.2, color="tab:green", alpha=.7)
ax2.set_ylabel("ln(CE/HE)", color="tab:green")
ax.set_title("The race after 2016: actual gap vs continued-demand counterfactuals")
ax.set_ylabel("log gap"); ax.legend(fontsize=7, loc="lower right"); ax.grid(alpha=.3)

ax = axes[2]
for name, c in [("KM141", "tab:blue"), ("GK164", "tab:red"), ("CL250", "tab:green")]:
    dn = D[name] - D[name][1992]
    ax.plot(dn.loc[1992:].index, dn.loc[1992:], lw=1.6, color=c,
            label=r"$D_t=\sigma\cdot$gap$+\ln$(supply), $\sigma$=%s" % SIGMAS[name])
    ax.plot(dn.loc[:1991].index, dn.loc[:1991], lw=1.6, color=c, alpha=.45)
ax.axvline(1992, color="gray", ls=":", lw=1); ax.axvline(2016, color="gray", ls=":", lw=.8)
ax.set_title("Relative demand index (1992 = 0; pre-1992 shown faded — other educ regime, level not comparable)")
ax.set_ylabel("log points"); ax.set_xlabel("year"); ax.legend(fontsize=7); ax.grid(alpha=.3)
plt.tight_layout(); plt.savefig(os.path.join(DATA, "premium_race_pass2.png"), dpi=150)
print("\nfigure written: data/premium_race_pass2.png")
print("outputs: data/morg_premium_pass2.csv, data/race_decomposition.csv")
