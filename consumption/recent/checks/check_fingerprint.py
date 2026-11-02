# check_fingerprint.py - checks for consumption/recent/code/fingerprint.py (run that first).
# Independent re-implementations (own WLS, permutation and leave-one-out code), applied to the script's outputs
# and to synthetic data with a known gap. Prints PASS / FAIL / INFO per check and exits 1 on any FAIL.
# Run from the repo root:  venv/bin/python -I consumption/recent/checks/check_fingerprint.py

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
RECENT = HERE.parent
THREAD = RECENT.parent
OUT = RECENT / "out"
TIDY = THREAD / "data" / "tidy"

import numpy as np
import pandas as pd

SEED = 20261102
DEC = [f"d{k:02d}" for k in range(1, 11)]
results = []


def check(name, ok, detail="", info=False):
    status = "INFO" if info else ("PASS" if ok else "FAIL")
    results.append((status, name, detail))
    print(f"[{status}] {name}: {detail}")


def close(a, b, rel=1e-8, abs_=1e-10):
    """Equality up to the outputs' storage precision (CSV files carry 10 significant digits)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    return bool(np.all(np.abs(a - b) <= abs_ + rel * np.maximum(np.abs(a), np.abs(b))))


def wls_line(y, x, w):
    w = np.asarray(w, float) / np.sum(w)
    xm, ym = np.sum(w * x), np.sum(w * y)
    b = np.sum(w * (x - xm) * (y - ym)) / np.sum(w * (x - xm) ** 2)
    return ym - b * xm, b


def perms_like_script(n, k=1000):
    r = np.random.default_rng(SEED + 7919 * n)
    return np.array([r.permutation(n) for _ in range(k)])


def slope_rows(y, X, w):
    w = np.asarray(w, float) / np.sum(w)
    out = []
    for x in X:
        out.append(wls_line(y, x, w)[1])
    return np.array(out)


thA = pd.read_csv(OUT / "fingerprint_theta_A.csv")
thB = pd.read_csv(OUT / "fingerprint_theta_B.csv")
mapB = pd.read_csv(OUT / "fingerprint_mapping_B.csv", dtype={"ucc": str})
read = pd.read_csv(OUT / "fingerprint_read.csv")
cats = pd.read_csv(OUT / "fingerprint_read_categories.csv")
bt = pd.read_csv(OUT / "fingerprint_backtest.csv")
tilt_m = pd.read_csv(OUT / "top_tilt_monthly.csv")
tilt_a = pd.read_csv(OUT / "fingerprint_top_tilt_annual.csv")
cov = pd.read_csv(OUT / "fingerprint_coverage_B.csv")

# 1. theta rows sum to one ----------------------------------------------------------------------------------
for name, t in (("A", thA), ("B", thB)):
    dev = (t[[f"theta_{d}" for d in DEC]].sum(axis=1) - 1).abs().max()
    check(f"theta {name}: decile shares sum to 1 in every category-year", dev < 1e-9, f"max |sum-1| = {dev:.2e}")
    g = (t.theta_top20 + t.theta_b80 - 1).abs().max()
    q = (t[["theta_q1", "theta_q2", "theta_q3", "theta_q4", "theta_q5"]].sum(axis=1) - 1).abs().max()
    f = (t[["theta_b50", "theta_p50_80", "theta_p80_90", "theta_top10"]].sum(axis=1) - 1).abs().max()
    check(f"theta {name}: group thetas sum to 1 (2, 4 and 5 groups)", max(g, q, f) < 1e-9,
          f"max deviation {max(g, q, f):.2e}")
dp = pd.read_csv(TIDY / "bls_dpce_long.csv")
dp = dp[(dp.vintage == "2025-03") & (dp.table == "T1") & (dp.measure == "decile_share_of_category")]
raw = dp.groupby(["year", "nipa_2_3_5_line"]).value.sum()
check("dPCE raw decile shares sum to 1 before renormalization (published rounding)", (raw - 1).abs().max() < 5e-4,
      f"max |sum-1| = {(raw - 1).abs().max():.5f}")

# 2. mapped coverage (B) --------------------------------------------------------------------------------------
c24 = cov[cov.year == 2024].iloc[0]
check("B coverage of PCE, 2024 base (all mapped categories)", 0.85 <= c24.pce_covered_share <= 1.0,
      f"{100 * c24.pce_covered_share:.1f}% of PCE; excluding health lines {100 * c24.pce_covered_share_ex_health:.1f}%;"
      f" CE spending mapped {100 * c24.ce_spending_mapped_share:.1f}%")
check("B coverage, all CE years", cov.pce_covered_share.between(0.85, 1.0).all(),
      "; ".join(f"{int(r.year)} {100 * r.pce_covered_share:.1f}%" for _, r in cov.iterrows()))
m24 = mapB[mapB.year == 2024]
unmatched = m24[m24["match"] == "unmatched"]
check("B mapping: every Table 1110 item found in the integrated stub (2024)", len(unmatched) == 0,
      f"{len(unmatched)} unmatched")
mapped = m24[m24.pce_line.notna()]
L = pd.read_csv(TIDY / "bea_pce_u_lines.csv")
main_lines = set(L[L.section == "main"].line)
check("B mapping: every PCE target is a 2.4.5U main-hierarchy line", set(mapped.pce_line.astype(int)) <= main_lines,
      f"{mapped.pce_line.nunique()} distinct target lines")
oos = m24[m24.map_source == "out_of_scope"]
check("B mapping: every out-of-scope UCC carries a reason", oos.reason.notna().all() and (oos.reason != "").all(),
      f"{oos.ucc.nunique()} out-of-scope UCCs (2024)")
ce = pd.read_csv(TIDY / "ce_income_deciles_long.csv")
Nd = ce[(ce.year == 2024) & (ce.path == "Number of consumer units (in thousands)")].set_index("group").value[DEC]
for item, cat in (("Rented dwellings", 154), ("Tobacco products and smoking supplies", 141)):
    mm = ce[(ce.year == 2024) & (ce.item_clean == item) & (ce.stat == "mean")].set_index("group").value[DEC]
    agg = Nd * mm
    own = agg[["d09", "d10"]].sum() / agg.sum()
    fil = thB[(thB.base_year == 2024) & (thB.category == cat)].theta_top20.iloc[0]
    check(f"B theta of single-feeder line {cat} recomputed from Table 1110 ('{item}', 2024)", close(own, fil),
          f"{own:.6f} vs file {fil:.6f}")
um = m24[m24.map_source == "unmapped"]
check("B mapping: unmapped in-scope UCCs (dropped), 2024", True,
      ", ".join(f"{r.ucc} {r.ucc_title} (${r.ucc_mean_all:.0f})" for _, r in um.drop_duplicates("ucc").iterrows()),
      info=True)

# 3. NIPA line correspondence and real-growth sources ---------------------------------------------------------
maj = pd.read_csv(TIDY / "bea_pce_major_long.csv", dtype={"table": str, "date": str})
codes = maj.drop_duplicates(["table", "line"]).pivot(index="line", columns="table", values="series_code")
ok = all(codes.at[l, "2.3.5"] == codes.at[l, "2.8.5"] for l in range(1, 23))
check("2.3.5 and 2.8.5 lines 1-22 carry the same series codes", ok)
u = pd.read_csv(TIDY / "bea_pce_u_long.csv.gz", dtype={"table": str, "date": str})
m = maj[(maj.table == "2.8.5")][["line", "series_code", "date", "value"]]
uu = u[(u.table == "2.4.5U") & (u.freq == "M")][["series_code", "date", "value"]]
j = m.merge(uu, on=["series_code", "date"], suffixes=("", "_u"))
check("2.8.5 values equal the 2.4.5U values of the same series (monthly)", (j.value - j.value_u).abs().max() == 0,
      f"{len(j)} cells, max |diff| = {(j.value - j.value_u).abs().max()}")
ch = u[(u.table == "2.4.6U") & (u.freq == "A")].pivot(index="date", columns="line", values="value")
qi = u[(u.table == "2.4.3U") & (u.freq == "A")].pivot(index="date", columns="line", values="value")
gch = ch.loc["2025"] / ch.loc["2023"] - 1
gqi = qi.loc["2025"] / qi.loc["2023"] - 1
d = (gch - gqi.reindex(gch.index)).abs()
d = d[(ch.loc["2023"] > 1000)]                # lines above $1bn (chained-dollar rounding on tiny lines)
check("chained-dollar growth equals quantity-index growth, 2023->2025 (2.4.6U vs 2.4.3U, lines > $1bn)",
      d.max() < 5e-4, f"max |diff| = {d.max():.2e} over {len(d)} lines")

# 4. the read reproduces with an independent implementation ---------------------------------------------------
for (win, src, meas), x in cats.groupby(["window", "source", "measure"]):
    yb = 2023 if src == "A_dPCE" else 2024
    x = x[x.theta_base_year == yb]
    rr = read[(read.window == win) & (read.source == src) & (read.measure == meas) & (read.theta_base_year == yb)
              & (read["sample"] == "all") & (read.spec == "2grp")].iloc[0]
    a, b = wls_line(x.g.to_numpy(), x.theta_top20.to_numpy(), x.S0.to_numpy())
    P = perms_like_script(len(x))
    ap = slope_rows(x.g.to_numpy(), x.theta_top20.to_numpy()[P], x.S0.to_numpy())
    p0 = (1 + np.sum(np.abs(ap) >= abs(b) - 1e-12)) / (len(P) + 1)
    ok = close(b, rr.gap, rel=1e-7) and close(a, rr.x_b80, rel=1e-7) and abs(p0 - rr.p_placebo) <= 1.0 / (len(P) + 1)
    check(f"read {win} {src} {meas}: gap and placebo p reproduced independently", ok,
          f"gap {b:+.4f} (file {rr.gap:+.4f}), p {p0:.3f} (file {rr.p_placebo:.3f})")
    G = np.sum(x.S0 * x.g) / x.S0.sum()
    check(f"read {win} {src} {meas}: weighted mean of fitted values = aggregate growth of covered categories",
          close(a + b * np.sum(x.S0 * x.theta_top20) / x.S0.sum(), G) and close(G, rr.agg_growth, rel=1e-7),
          f"{100 * G:.2f}%")
ra = read[(read.source == "A_dPCE") & (read["sample"] == "all") & (read.spec == "2grp") & (read.measure == "nominal")
          & (read.theta_base_year == 2023)]
pce = u[(u.table == "2.4.5U") & (u.line == 1)].set_index(["freq", "date"]).value
for _, r in ra.iterrows():
    f = "A" if r.freq == "A" else "M"
    tot = pce[(f, r.t1)] / pce[(f, r.t0)] - 1
    check(f"A {r.window}: the 16 lines' aggregate nominal growth equals PCE growth", abs(r.agg_growth - tot) < 2e-5,
          f"{100 * r.agg_growth:.3f}% vs PCE {100 * tot:.3f}%")

# 5. synthetic: a known K pushed through the 2023/2024 thetas is recovered ------------------------------------
rng = np.random.default_rng(SEED)
for src, yb, win in (("A_dPCE", 2023, "2023-09->2026-09"), ("B_CE", 2024, "2023-09->2026-09")):
    x = cats[(cats.window == win) & (cats.source == src) & (cats.theta_base_year == yb) & (cats.measure == "real")]
    th, w = x.theta_top20.to_numpy(), x.S0.to_numpy()
    xt, xb = 1.04 ** 3 - 1, 0.0                       # Zandi's split over three years
    g = th * xt + (1 - th) * xb
    a, b = wls_line(g, th, w)
    check(f"synthetic Zandi split through {src} {yb} thetas, no noise: gap recovered exactly",
          abs(b - (xt - xb)) < 1e-12 and abs(a - xb) < 1e-12, f"true {xt - xb:.6f}, recovered {b:.6f}")
    # with noise: residuals of the actual fit resampled; bias and coverage of the t interval
    a0, b0 = wls_line(x.g.to_numpy(), th, w)
    res = x.g.to_numpy() - a0 - b0 * th
    est, cover = [], []
    from scipy import stats as st
    for _ in range(2000):
        e = rng.choice(res, size=len(res), replace=True)
        gg = g + e
        aa, bb = wls_line(gg, th, w)
        rr_ = gg - aa - bb * th
        wn = w / w.mean()
        se = np.sqrt(np.sum(wn * rr_ ** 2) / (len(th) - 2) / np.sum(wn * (th - np.sum(wn * th) / wn.sum()) ** 2))
        tc = st.t.ppf(0.975, len(th) - 2)
        est.append(bb)
        cover.append(bb - tc * se <= xt - xb <= bb + tc * se)
    est = np.array(est)
    check(f"synthetic with resampled real-data noise ({src}): estimator unbiased",
          abs(est.mean() - (xt - xb)) < 3 * est.std() / np.sqrt(len(est)) + 1e-3,
          f"mean {est.mean():+.4f} vs true {xt - xb:+.4f}; sd of estimate {est.std():.4f} "
          f"(= {est.std() / (xt - xb):.1f}x Zandi's gap); t-interval coverage {np.mean(cover):.3f}")
# multi-group: OLS recovers quintile growths exactly without noise; closed-form LOO equals brute force
x = cats[(cats.window == "2023-09->2026-09") & (cats.source == "B_CE") & (cats.theta_base_year == 2024)
         & (cats.measure == "real")]
tb = thB[thB.base_year == 2024].set_index("category")
TH = tb.loc[x.category, ["theta_q1", "theta_q2", "theta_q3", "theta_q4", "theta_q5"]].to_numpy()
w = x.S0.to_numpy() / x.S0.sum()
xq = np.array([0.0, 0.0, 0.0, 0.0, 0.1249])
g = TH @ xq
A = TH.T @ (w[:, None] * TH)
sol = np.linalg.solve(A, TH.T @ (w * g))
check("synthetic quintile growths recovered exactly by unconstrained WLS (B 2024 thetas)",
      np.abs(sol - xq).max() < 1e-8, f"max |error| {np.abs(sol - xq).max():.1e}; cond(TH'WTH) = {np.linalg.cond(A):.1e}")
pi = TH.T @ w
D = np.eye(5) - np.outer(np.ones(5), pi)
Pm = D.T @ np.diag(pi) @ D
gg = x.g.to_numpy()
lam = 1e-3
M = np.linalg.inv(A + lam * Pm)
e = gg - TH @ (M @ (TH.T @ (w * gg)))
h = w * np.einsum("ij,jk,ik->i", TH, M, TH)
cf = np.sum(w * (e / (1 - h)) ** 2)
bf = 0.0
for i in range(len(gg)):
    k = np.arange(len(gg)) != i
    wk = w[k]
    xk = np.linalg.solve(TH[k].T @ (wk[:, None] * TH[k]) + lam * Pm, TH[k].T @ (wk * gg[k]))
    bf += w[i] * (gg[i] - TH[i] @ xk) ** 2
check("closed-form leave-one-out CV equals brute force (ridge, lambda=1e-3)", abs(cf - bf) < 1e-12 * max(1, bf),
      f"closed form {cf:.10f}, brute force {bf:.10f}")

# 6. identities: basket gap = kappa x slope; tilt = kappa x implied gap ---------------------------------------
r = read[(read.spec == "2grp")]
check("basket gap = kappa x two-group slope (every 2grp row)", close(r.basket_gap, r.kappa * r.gap),
      f"kappa range {r.kappa.min():.3f}-{r.kappa.max():.3f}")
check("top tilt: tilt = kappa x implied gap (monthly)", close(tilt_m.tilt_12m, tilt_m.kappa * tilt_m.implied_gap_12m),
      f"{len(tilt_m)} months")
check("top tilt: tilt = top20 basket - bottom80 basket",
      close(tilt_m.tilt_12m, tilt_m.top20_basket_12m - tilt_m.b80_basket_12m, rel=1e-7))
check("top tilt annual: chained index levels consistent with yearly basket growth",
      np.allclose(tilt_a.top20_index.to_numpy(), 100 * np.cumprod(1 + tilt_a.top20_basket.to_numpy())))

# 7. backtest: the dPCE 'actual' recomputed from leaf categories ----------------------------------------------
pce_dp = pd.read_csv(TIDY / "bls_dpce_long.csv")
pce_dp = pce_dp[(pce_dp.vintage == "2025-03") & (pce_dp.table == "T1")]
sh = pce_dp[pce_dp.measure == "decile_share_of_category"].pivot_table(index=["year", "nipa_2_3_5_line"],
                                                                      columns="group", values="value")
tot = pce_dp[pce_dp.measure == "pce"].pivot_table(index="year", columns="nipa_2_3_5_line", values="value")
leaves = [4, 5, 6, 7, 9, 10, 11, 12, 15, 16, 17, 18, 19, 20, 21, 22]
devs = []
for y in range(2000, 2024):
    top_line1 = (sh.loc[(y, 1), ["d09", "d10"]].sum()) * tot.at[y, 1]
    top_leaf = sum(sh.loc[(y, l), ["d09", "d10"]].sum() * tot.at[y, l] for l in leaves)
    devs.append(top_leaf / top_line1 - 1)
check("dPCE top-20 spending: line-1 shares x total vs sum over the 16 leaves", max(map(abs, devs)) < 3e-3,
      f"max relative gap {max(map(abs, devs)):.4f} (published rounding of shares and totals)")
a2 = bt[(bt.source == "A_dPCE") & (bt.spec == "2grp")]
check("backtest error = estimate - actual", close(a2.gap_error, a2.gap - a2.gap_actual, rel=1e-7))
check("backtest: actual gaps inside the estimator's 95% interval (A, 2grp)", True,
      f"{int(a2.actual_inside_ci.sum())} of {len(a2)}", info=True)

# 8. power and benchmarks -------------------------------------------------------------------------------------
pw = pd.read_csv(OUT / "fingerprint_power.csv", dtype={"t0": str, "t1": str})
rows = pw[~pw.kind.str.startswith("summary")]
summ = pw[pw.kind.str.startswith("summary")]
for kind, src, start in (("B_rolling_36m", "B_CE", "2014"), ("A_rolling_36m", "A_dPCE", "2010")):
    for meas in ("nominal", "real"):
        x = rows[(rows.kind == kind) & (rows.measure == meas)]
        calm = x[(x.t0.str[:4] >= start) & (x.t1 <= "2019-12")]
        sm = summ[(summ.kind == "summary:" + kind) & (summ.measure == meas)].iloc[0]
        ok = close(calm.gap.mean(), sm.calm_mean) and close(calm.gap.std(), sm.calm_sd)
        check(f"calm-period norm recomputed ({kind}, {meas})", ok,
              f"{len(calm)} windows, mean {100 * calm.gap.mean():+.1f} pts, sd {100 * calm.gap.std():.1f}")
r2 = read[(read.spec == "2grp") & read.calm_norm_mean.notna()]
check("read: excess over calm norm = gap - norm, and Zandi's z = (excess - Zandi gap) / sd",
      close(r2.excess_over_calm, r2.gap - r2.calm_norm_mean, rel=1e-7) and
      close(r2.zandi_z_vs_calm, (r2.excess_over_calm - r2.zandi_gap_cum) / r2.calm_norm_sd, rel=1e-7),
      f"{len(r2)} rows")
rr = read[read.spec.str.endswith("ridge")]
check("ridge rows: lambda chosen on the grid for every fit", rr.lam.notna().all(),
      f"{int(rr.lam_at_grid_max.sum())} of {len(rr)} fits at the largest lambda (data prefer equal growth)", info=False)

nfail = sum(1 for s, _, _ in results if s == "FAIL")
print(f"\n{sum(1 for s, _, _ in results if s == 'PASS')} PASS, {nfail} FAIL, "
      f"{sum(1 for s, _, _ in results if s == 'INFO')} INFO")
sys.exit(1 if nfail else 0)
