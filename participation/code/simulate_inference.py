# simulate_inference.py — validates code/inference.py on synthetic country-year panels before any data are seen
# (docs/design_review.md, 'Inference method' step 8). The panels mimic the protocol's: country and year fixed effects,
# years 1997-2025 without 2020-2021, unbalanced (random start 1997-2001, 3% of cells missing; T about 25), a serially
# correlated regressor with a common year component, a cycle control correlated with it, mechanical break dummies, and
# errors AR(1) with rho = 0.7 within country and country-specific variances (lognormal, sd 0.5 in logs).
#   (i)   size: 1000 panels under H0 at G = 15 and G = 31; one-sided 5% WCR test (B = 999), rejection rate;
#   (ii)  power: the same panels with a planted effect of 1, 2 and 3 mean CR1 standard errors;
#   (iii) randomisation inference under a sharp null, regressor at the unit level, the protocol's strata: a C-4-style
#         panel (X_c x 1[year >= 2023], CR1, G = 31), a C-5-style cross-section (stratum FE, HC2, G = 31), and an
#         exactly enumerated case (G = 8, strata 3/3/2, 72 assignments); 1000 draws each, R = 999;
#   (iv)  ci() coverage of the true beta over 1000 panels at G = 15 and G = 31 (two-sided 95%, B = 999);
#   (v)   one panel: wcr's beta and CR1 se against a direct dummy-variable least-squares fit; a rank-deficient Z; the
#         cluster-score bootstrap against the literal N x B form; ri's statistic against wcr's; HC2 against direct;
#   (vi)  the designs the D verdicts rest on, 1000 panels each at G = 15 and G = 31 (B = 999): D1-like, the tested term
#         log q x F_c with log q in Z, F_c a standardised country moderator and one dominant country (its q variance
#         five times the others'); D2-like, the tested term (log q - m_c)^2 with log q in Z. Size in both directions,
#         the naive CR1 t, G* (mean and share below 8), and power at 3 mean CR1 se.
# Also times the production calls (B = R = 9999), and records the SHA-256 of code/inference.py and of this file, so
# checks/check_inference.py can refuse results computed by other code (line endings normalised to LF first, so a
# checkout under core.autocrlf hashes the same).
#
# Run from participation/:  ../venv/Scripts/python.exe code/simulate_inference.py
# Out: results/simulate_inference.json

from __future__ import annotations

import hashlib
import json
import math
import os
import sys
import time

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import inference as inf  # noqa: E402

SEED = 20261008
YEARS = np.array([y for y in range(1997, 2026) if y not in (2020, 2021)])
STRATA31 = [5, 7, 2, 6, 11]               # Nordic, Continental, Anglo, South, CEE
B_SIM, R_SIM, N_SIZE, N_CI = 999, 999, 1000, 1000


def code_hashes() -> dict:
    return {f: hashlib.sha256(open(os.path.join(HERE, f), "rb").read().replace(b"\r\n", b"\n")).hexdigest()
            for f in ("inference.py", "simulate_inference.py")}


def panel(G: int, seed: int, beta: float = 0.0, years=YEARS, unbalanced: bool = True):
    """One synthetic country-year panel. Returns (df, Z) with df columns geo, year, y, x, U; Z = [country FE,
    year FE, U, break dummies]. The draws do not depend on beta, which multiplies x at the end."""
    rng = np.random.default_rng(seed)
    Y = len(years)
    t = (years - 2010) / 10
    common = np.cumsum(rng.normal(0, 0.03, Y))
    ar = np.zeros((G, Y))
    scale = rng.uniform(0.5, 2.0, G)
    ar[:, 0] = rng.normal(0, 0.05, G) * scale / math.sqrt(1 - 0.81)
    for j in range(1, Y):
        ar[:, j] = 0.9 * ar[:, j - 1] + rng.normal(0, 0.05, G) * scale
    x = rng.normal(0, 0.3, G)[:, None] + rng.normal(0, 0.1, G)[:, None] * t + common + ar
    cyc = np.zeros((G, Y))
    cyc[:, 0] = rng.normal(0, 1 / math.sqrt(1 - 0.64), G)
    for j in range(1, Y):
        cyc[:, j] = 0.8 * cyc[:, j - 1] + rng.normal(0, 1, G)
    U = 7 + cyc + 10 * ar + rng.normal(0, 1, Y)
    sig = np.exp(rng.normal(0, 0.5, G))
    e = np.zeros((G, Y))
    e[:, 0] = rng.normal(0, 1, G) * sig / math.sqrt(1 - 0.49)
    for j in range(1, Y):
        e[:, j] = 0.7 * e[:, j - 1] + rng.normal(0, 1, G) * sig
    has_break = rng.random(G) < 0.3
    tau = rng.integers(2003, 2020, G)
    brk = (has_break[:, None] & (years[None, :] >= tau[:, None])).astype(float)
    shift = rng.normal(0, 2, G)[:, None] * brk
    y = rng.normal(0, 5, G)[:, None] + np.cumsum(rng.normal(0, 1, Y)) + 0.5 * U + shift + e + beta * x
    start = rng.integers(1997, 2002, G)
    keep = (years[None, :] >= start[:, None]) & (rng.random((G, Y)) >= 0.03) if unbalanced else np.ones((G, Y), bool)
    gi, yi = np.nonzero(keep)
    df = pd.DataFrame({"geo": gi, "year": years[yi], "y": y[gi, yi], "x": x[gi, yi], "U": U[gi, yi]})
    bcols = [brk[gi, yi][:, None] * (gi == c)[:, None] for c in np.flatnonzero(has_break)]
    bd = np.column_stack(bcols) if bcols else np.zeros((len(df), 0))
    bd = bd[:, bd.std(0) > 0] if bd.size else bd                # a break before a country's start is no break
    Z = np.column_stack([inf.fe_matrix(df, ["geo", "year"]), df["U"].to_numpy(), bd])
    return df, Z


def panel_moderated(G: int, seed: int, kind: str, beta: float = 0.0):
    """D1-like (kind 'D1': x = q F_c, one dominant country) or D2-like (kind 'D2': x = (q - m_c)^2) on the panel above,
    q = its regressor, which joins Z; y also loads on q (b1 = 0.5). Returns (y, x, Z, clusters)."""
    df, Z = panel(G, seed)
    q = df["x"].to_numpy().copy()
    g = df["geo"].to_numpy()
    if kind == "D1":
        m0 = q[g == 0].mean()
        q[g == 0] = m0 + math.sqrt(5) * (q[g == 0] - m0)          # one dominant country
        F = np.random.default_rng(seed + 1).normal(0, 1, G)
        F = (F - F.mean()) / F.std()
        x = q * F[g]
    else:
        m = np.bincount(g, q, G) / np.bincount(g, None, G)
        x = (q - m[g]) ** 2
    y = df["y"].to_numpy() + 0.5 * q + beta * x
    return y, x, np.column_stack([Z, q]), g


def size_moderated(G: int, kind: str) -> dict:
    seeds = [SEED * 100 + 7000000 + (1 if kind == "D1" else 2) * 100000 + G * 1000 + i for i in range(N_SIZE)]
    se = [inf._Fit(*panel_moderated(G, s, kind)).se for s in seeds]
    se_bar = float(np.mean(se))
    crit = inf.stats.t.ppf(0.95, G - 1)
    rej, opp, naive, gs, pw = [], [], [], [], []
    for i, s in enumerate(seeds):
        w = inf.wcr(*panel_moderated(G, s, kind), beta0=0.0, side=-1, B=B_SIM, seed=i)
        rej.append(w["p"] <= 0.05), opp.append(w["p_opposite"] <= 0.05), naive.append(w["t"] <= -crit)
        gs.append(w["G_star"])
        wp = inf.wcr(*panel_moderated(G, s, kind, beta=-3 * se_bar), beta0=0.0, side=-1, B=B_SIM, seed=i)
        pw.append(wp["p"] <= 0.05)
    return {"G": G, "panels": N_SIZE, "B": B_SIM, "side": -1, "mean_cr1_se": se_bar,
            "reject_one_sided_5pct": float(np.mean(rej)), "reject_opposite_side_5pct": float(np.mean(opp)),
            "reject_naive_cr1_t": float(np.mean(naive)), "mean_G_star": float(np.mean(gs)),
            "share_G_star_below_8": float(np.mean(np.array(gs) < 8)), "power_3se": float(np.mean(pw))}


def strata_of(G: int, sizes) -> np.ndarray:
    return np.repeat(np.arange(len(sizes)), sizes)[:G]


def c4_panel(sizes, seed):
    """C-4 style: unit-level exposure X_c (iid within stratum, stratum-specific mean), outcome independent of it."""
    G = sum(sizes)
    rng = np.random.default_rng(seed)
    years = np.array([2016, 2017, 2018, 2019, 2022, 2023, 2024, 2025])
    st = strata_of(G, sizes)
    X = rng.normal(0, 1, len(sizes))[st] + rng.normal(0, 1, G)
    sig = np.exp(rng.normal(0, 0.5, G))
    e = np.zeros((G, len(years)))
    e[:, 0] = rng.normal(0, 1, G) * sig / math.sqrt(1 - 0.49)
    for j in range(1, len(years)):
        e[:, j] = 0.7 * e[:, j - 1] + rng.normal(0, 1, G) * sig
    y = rng.normal(0, 3, G)[:, None] + rng.normal(0, 1, len(years)) + e
    gi, yi = np.nonzero(rng.random((G, len(years))) >= 0.03)
    df = pd.DataFrame({"geo": gi, "year": years[yi], "y": y[gi, yi]})
    return df, X, st, inf.fe_matrix(df, ["geo", "year"]), (df["year"] >= 2023).to_numpy(float)


def c5_cross(sizes, seed):
    """C-5 style: one observation per country, stratum fixed effects, heteroskedastic errors, outcome independent of X."""
    G = sum(sizes)
    rng = np.random.default_rng(seed)
    st = strata_of(G, sizes)
    X = rng.normal(0, 1, len(sizes))[st] + rng.normal(0, 1, G)
    y = rng.normal(0, 1, len(sizes))[st] + rng.normal(0, 1, G) * np.exp(rng.normal(0, 0.5, G))
    return y, X, st, inf.fe_matrix(pd.DataFrame({"s": st}), "s")


def literal_tstar(y, x, Z, clusters, beta0, V):
    """The design review's N x B form, written independently: M_Z = I - Z pinv(Z) with a constant in Z."""
    n = len(y)
    Zc = np.column_stack([np.ones(n), Z])
    M = np.eye(n) - Zc @ np.linalg.pinv(Zc)
    _, g = np.unique(clusters, return_inverse=True)
    G = g.max() + 1
    xt, yt = M @ x, M @ y
    xx = xt @ xt
    ur = M @ (y - beta0 * x)
    E = M @ (ur[:, None] * V[g, :])
    d = (xt @ E) / xx
    Us = E - xt[:, None] * d
    D = np.zeros((n, G))
    D[np.arange(n), g] = 1
    sc = D.T @ (xt[:, None] * Us)
    k = np.linalg.matrix_rank(Zc) + 1
    c = G / (G - 1) * (n - 1) / (n - k)
    return d / np.sqrt(c * (sc ** 2).sum(0) / xx ** 2)


def direct_checks() -> dict:
    df, Z = panel(31, SEED + 7, beta=0.4)
    y, x, cl = df["y"].to_numpy(), df["x"].to_numpy(), df["geo"].to_numpy()
    n = len(y)
    w = inf.wcr(y, x, Z, cl, beta0=0.1, side=+1, B=999, seed=1)
    X = np.column_stack([x, np.ones(n), Z])                     # the direct dummy-variable fit
    K = np.linalg.matrix_rank(X)
    assert K == X.shape[1]
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    u = y - X @ b
    XtXi = np.linalg.inv(X.T @ X)
    G = len(np.unique(cl))
    meat = sum(np.outer(X[cl == g].T @ u[cl == g], X[cl == g].T @ u[cl == g]) for g in np.unique(cl))
    se = math.sqrt((G / (G - 1) * (n - 1) / (n - K) * XtXi @ meat @ XtXi)[0, 0])
    # rank-deficient Z: every country and year dummy (no level dropped), a duplicated column, a constant
    ctl = Z[:, inf.fe_matrix(df, ["geo", "year"]).shape[1]:]
    Zd = np.column_stack([pd.get_dummies(df["geo"], dtype=float), pd.get_dummies(df["year"], dtype=float),
                          np.ones(n), ctl, ctl[:, :1]])
    wd = inf.wcr(y, x, Zd, cl, beta0=0.1, side=+1, B=999, seed=1)
    # the cluster-score bootstrap against the literal N x B form
    f = inf._Fit(y, x, Z, cl)
    V = inf.webb(f.G, 999, 1)
    lit = np.max(np.abs(f.tstar(0.1, V) - literal_tstar(y, x, Z, cl, 0.1, V)))
    lit3 = np.max(np.abs(f.tstar(-2.0, V) - literal_tstar(y, x, Z, cl, -2.0, V)))
    # ri's observed statistic (x = X_c x post) against wcr's at beta0 = 0
    d4, X4, st4, Z4, post = c4_panel(STRATA31, SEED + 8)
    r4 = inf.ri(d4["y"], X4, d4["geo"], st4, Z4, side=-1, R=99, studentize="CR1", x_mult=post)
    w4 = inf.wcr(d4["y"], X4[d4["geo"]] * post, Z4, d4["geo"], beta0=0.0, side=-1, B=99)
    # HC2 against direct
    y5, X5, st5, Z5 = c5_cross(STRATA31, SEED + 9)
    r5 = inf.ri(y5, X5, np.arange(31), st5, Z5, side=-1, R=99, studentize="HC2")
    X5d = np.column_stack([X5, np.ones(31), Z5])
    A = np.linalg.inv(X5d.T @ X5d)
    b5 = A @ X5d.T @ y5
    u5 = y5 - X5d @ b5
    h = np.einsum("ij,jk,ik->i", X5d, A, X5d)
    se5 = math.sqrt((A @ (X5d.T * (u5 ** 2 / (1 - h))) @ X5d @ A)[0, 0])
    return {"panel": {"N": n, "G": G, "K_direct": int(K)},
            "beta_wcr": w["beta"], "beta_direct": float(b[0]), "abs_diff_beta": abs(w["beta"] - b[0]),
            "se_wcr": w["se"], "se_direct": se, "abs_diff_se": abs(w["se"] - se),
            "t_wcr": w["t"], "t_direct": (b[0] - 0.1) / se,
            "rank_deficient_abs_diff_beta": abs(wd["beta"] - w["beta"]), "rank_deficient_abs_diff_se": abs(wd["se"] - w["se"]),
            "rank_deficient_same_p": wd["p"] == w["p"],
            "literal_bootstrap_max_abs_diff_tstar": float(max(lit, lit3)),
            "ri_vs_wcr_abs_diff_t": abs(r4["t"] - w4["t"]), "ri_vs_wcr_abs_diff_beta": abs(r4["beta"] - w4["beta"]),
            "hc2_abs_diff_t": abs(r5["t"] - b5[0] / se5)}


def size_power(G: int) -> dict:
    seeds = [SEED * 100 + G * 10000 + i for i in range(N_SIZE)]
    se, beta, T, N = [], [], [], []
    for s in seeds:                                         # pass 1: CR1 se under H0, to scale the planted effects
        df, Z = panel(G, s)
        f = inf._Fit(df["y"], df["x"], Z, df["geo"])
        se.append(f.se), beta.append(f.beta), N.append(f.n), T.append(f.n / G)
    se_bar = float(np.mean(se))
    rej = {k: [] for k in (0, 1, 2, 3)}
    rej_opp, rej_naive, gstar = [], [], []
    crit = inf.stats.t.ppf(0.95, G - 1)
    for i, s in enumerate(seeds):
        for k in (0, 1, 2, 3):
            df, Z = panel(G, s, beta=k * se_bar)
            w = inf.wcr(df["y"], df["x"], Z, df["geo"], beta0=0.0, side=+1, B=B_SIM, seed=i)
            rej[k].append(w["p"] <= 0.05)
            if k == 0:
                rej_opp.append(w["p_opposite"] <= 0.05)
                rej_naive.append(w["t"] >= crit)
                gstar.append(w["G_star"])
    return {"G": G, "panels": N_SIZE, "B": B_SIM, "mean_T": float(np.mean(T)), "mean_N": float(np.mean(N)),
            "mean_cr1_se": se_bar, "sd_beta_hat": float(np.std(beta)), "mean_G_star": float(np.mean(gstar)),
            "reject_one_sided_5pct": float(np.mean(rej[0])), "reject_opposite_side_5pct": float(np.mean(rej_opp)),
            "reject_naive_cr1_t": float(np.mean(rej_naive)),
            "power": {str(k): float(np.mean(rej[k])) for k in (1, 2, 3)}}


def ri_size() -> dict:
    out = {}
    hits, info = [], None
    for i in range(N_SIZE):
        d, X, st, Z, post = c4_panel(STRATA31, SEED + 30000 + i)
        r = inf.ri(d["y"], X, d["geo"], st, Z, side=-1, R=R_SIM, seed=i, studentize="CR1", x_mult=post)
        hits.append(r["p"] <= 0.05)
        info = r
    out["panel_c4_G31_CR1"] = {"draws": N_SIZE, "R": R_SIM, "exact": info["exact"], "n_perm": info["n_perm"],
                               "reject_5pct": float(np.mean(hits))}
    hits = []
    for i in range(N_SIZE):
        y, X, st, Z = c5_cross(STRATA31, SEED + 40000 + i)
        r = inf.ri(y, X, np.arange(31), st, Z, side=-1, R=R_SIM, seed=i, studentize="HC2")
        hits.append(r["p"] <= 0.05)
        info = r
    out["cross_section_c5_G31_HC2"] = {"draws": N_SIZE, "R": R_SIM, "exact": info["exact"], "n_perm": info["n_perm"],
                                       "reject_5pct": float(np.mean(hits))}
    hits = []
    for i in range(N_SIZE):
        d, X, st, Z, post = c4_panel([3, 3, 2], SEED + 50000 + i)
        r = inf.ri(d["y"], X, d["geo"], st, Z, side=+1, R=R_SIM, seed=i, studentize="CR1", x_mult=post)
        hits.append(r["p"] <= 0.05)
        info = r
    out["exact_G8_CR1"] = {"draws": N_SIZE, "exact": info["exact"], "n_perm": info["n_perm"],
                           "reject_5pct": float(np.mean(hits)), "attainable_size": math.floor(0.05 * 72) / 72}
    return out


def coverage(G: int, beta: float = 1.0) -> dict:
    cov, width = [], []
    for i in range(N_CI):
        df, Z = panel(G, SEED + 60000 + G * 1000 + i, beta=beta)
        lo, hi = inf.ci(df["y"], df["x"], Z, df["geo"], alpha=0.05, side=0, B=B_SIM, seed=i)
        cov.append(lo <= beta <= hi)
        width.append(hi - lo)
    return {"G": G, "panels": N_CI, "B": B_SIM, "true_beta": beta, "coverage": float(np.mean(cov)),
            "mean_width": float(np.mean(width))}


def timed(fn, *a, **k):
    t0 = time.perf_counter()
    out = fn(*a, **k)
    return out, time.perf_counter() - t0


def production_timings() -> dict:
    df, Z = panel(31, SEED + 1, beta=0.5)
    args = (df["y"], df["x"], Z, df["geo"])
    _, t_wcr = timed(inf.wcr, *args, B=9999)
    (lo, hi), t_ci = timed(inf.ci, *args, B=9999)
    d, X, st, Z4, post = c4_panel(STRATA31, SEED + 2)
    _, t_ri = timed(inf.ri, d["y"], X, d["geo"], st, Z4, side=-1, R=9999, x_mult=post)
    y5, X5, st5, Z5 = c5_cross(STRATA31, SEED + 3)
    _, t_ri5 = timed(inf.ri, y5, X5, np.arange(31), st5, Z5, side=-1, R=9999, studentize="HC2")
    return {"wcr_G31_B9999_s": t_wcr, "wcr_N": len(df), "ci_G31_B9999_s": t_ci, "ri_c4_G31_R9999_s": t_ri,
            "ri_c4_N": len(d), "ri_c5_G31_R9999_HC2_s": t_ri5}


def main():
    t0 = time.perf_counter()
    res = {"settings": {"seed": SEED, "B_sim": B_SIM, "R_sim": R_SIM, "size_panels": N_SIZE, "ci_panels": N_CI,
                        "dgp": "country + year FE, years 1997-2025 without 2020-2021, random start 1997-2001, 3% cells "
                               "missing; x = country level + country trend + common random walk + AR(1) rho 0.9 with "
                               "country scale U(0.5, 2); cycle control AR(1) 0.8 correlated with x; breaks in 30% of "
                               "countries (dummy in Z, level shift in y); errors AR(1) rho 0.7, country sd lognormal(0, 0.5)",
                        "strata_G31": STRATA31},
           "code_sha256": code_hashes()}
    res["direct"], res.setdefault("timings_s", {})["direct"] = timed(direct_checks)
    print("direct", json.dumps(res["direct"], default=float))
    for G in (15, 31):
        res.setdefault("size_power", {})[f"G{G}"], res["timings_s"][f"size_power_G{G}"] = timed(size_power, G)
        print(G, res["size_power"][f"G{G}"])
    res["ri"], res["timings_s"]["ri"] = timed(ri_size)
    print(res["ri"])
    for G in (15, 31):
        res.setdefault("ci", {})[f"G{G}"], res["timings_s"][f"ci_G{G}"] = timed(coverage, G)
        print(res["ci"][f"G{G}"])
    for kind in ("D1", "D2"):
        for G in (15, 31):
            key = f"{kind}_like_G{G}"
            res.setdefault("moderated", {})[key], res["timings_s"][key] = timed(size_moderated, G, kind)
            print(key, res["moderated"][key])
    res["timings_s"]["production"] = production_timings()
    res["timings_s"]["total"] = time.perf_counter() - t0
    print(res["timings_s"])
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    with open(os.path.join(ROOT, "results", "simulate_inference.json"), "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))


if __name__ == "__main__":
    main()
