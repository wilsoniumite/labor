# skeleton.py — the coverage-skeleton simulation of longrun/PROTOCOL.md section 5 ('Size calibration, before the
# freeze' and 'MDEs and the reading table, before the freeze'), published with the L-freeze, before any value.
#
# The skeleton: each verdict test's frozen countries, eligible years and chosen q segments (data/coverage.json) and the
# segment table (data/segments.csv). On it, synthetic values by a DGP fixed here (no long-run value is used):
#   log q   a Gaussian random walk with drift over each country's q years; drift and innovation SD = the pooled mean and
#           SD of the annual change of European log q (CP041 / IGD_NNRG, C6) over the frozen European panel (seen);
#           terciles and knots from it by the rule of section 5 (specs.knots);
#   U       an AR(1) with the pooled mean, SD and autoregressive coefficient of the European U(25-54) (seen);
#   F       standard normal per country, split by specs.compute_H (top half high floor);
#   outcome country and year effects, country-specific linear trends, floor-group linear trends, g x U and AR(1) errors
#           with rho 0.5 and 0.9 (calibration) or 0.7 (MDEs); the trend slopes' variances are set so that, on the
#           European D1 full-sample rows, the trend components' variances relative to the error variance equal the
#           ratios found in the European look's D1 residuals (seen): ratio_c (country trends fitted to the residuals)
#           and ratio_H (an H x trend fitted to them, H from C9's F split at the median); the slope SDs divide by the
#           design variance of each component (within-country var(t) for country trends, var(h t) for the floor-group
#           trend); the error scale and g from the same D1 fit (C-6L and LR-C1: the error scale of C-6's and C-1's
#           residuals, the D1 ratios).
# Null worlds: no effect of q (or of U on school). R = 2000 per rho. For each verdict test and direction the null
# distribution of the verdict statistic (LR-K2: max(p_WCR, p_RI); others: p_WCR) is stored: specs.calibrated reads it.
# MDEs at rho = 0.7: MDE = inference.mde(SD of the tested estimate across the null replications, G), the SD-based
# t-formula figure (labelled so in the output); the power of the actual verdict procedure (max(p_WCR, p_RI),
# calibrated) at that MDE is published beside it. Standardised MDE = MDE x SD(residualised tested regressor) /
# SD(residualised outcome) (the replications' means). The European benchmarks are the same procedure, same rho, on the
# European skeletons (seen data's rows, with the segment dummies the European look's frames carried): D1's countries
# and the years used at the look (knots inside each country's longest European q piece, H from C9's F) for LR-K2 and
# LR-Y0, C-6's rows for C-6L, C-1's rows for LR-C1; each long-run test's own equation is applied to them.
# Also: power at a planted effect equal to the MDE (rho 0.7; calibrated verdict p), the calibrated size on held-out
# null replications in both directions (cross-fitted: each half calibrates the other, the mean reported), and each LR-K2 country's share of the identifying variation of DiD (its share
# of the squared residualised tested regressor, mean over the null replications).
# Reported beside the calibration, not part of it (the verdict rule is section 5's; folding these into the envelope
# would be a protocol amendment, her call): LR-K2's size (raw and calibrated by the table above) (a) at the protocol's
# expected floor split (section 2: high = the first of CL, CO, CR, MX, IL up to half the members), and (b) under two
# stress nulls the calibration DGP leaves out: country-specific logistic curves in calendar time whose timing follows
# the floor groups (the threat of section 2: women's entry and schooling running later in the high-floor Latin
# American windows; amplitude 10 points, midpoints 1975 (low floor) and 2000 or 2012 (high floor: early or late in its
# window), each country's midpoint shifted uniformly by up to 5 years, scale 8 years; set a priori from the disclosed
# prior knowledge of section 7), and AR(1) errors with rho 0.95.
# Seeds: each replication's world and its bootstrap/RI draws come from two children of SeedSequence(seed0 + i).
# The European frames are read from the European look's cache with every row of an observation year at or before
# fetch.EUROPEAN_LAST dropped at parse (those are long-run cells; the cache holds them, nothing reads them).
#
# Run from longrun/:  ../../venv/Scripts/python.exe code/skeleton.py [--quick] [--workers N]
# Out: data/skeleton.json (calibration tables, sizes, MDEs, benchmarks, power, identifying-variation shares, the DGP
#      parameters and the code's SHA-256). --quick: 60 replications per cell, B = 999 (for checks; never published).

from __future__ import annotations

import hashlib
import json
import math
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from datetime import date

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
LROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import fetch  # noqa: E402
import segments as sg  # noqa: E402
import specs  # noqa: E402

inf, pspecs = specs.inf, specs.pspecs
OUT = os.path.join(LROOT, "data", "skeleton.json")
CUBE = os.path.join(LROOT, "data", "coverage.json")
SEED = inf.SEED
RHOS_CAL = (0.5, 0.9)
RHO_MDE = 0.7
R_CAL, R_MDE, R_POWER = 2000, 2000, 400
TESTS = ("LR-K2", "LR-Y0", "C-6L", "LR-C1")
R_EXTRA = 1000                                   # the expected-split and stress-null runs (reported, LR-K2 only)
RHO_STRESS = 0.95
STRESS = dict(amp=10.0, mid_low=1975.0, mid_high=2000.0, jitter=5.0, scale=8.0)
STRESS_LATE = dict(STRESS, mid_high=2012.0)      # the high-floor curve late in its 1990s-2020s window
EXPECTED_HIGH = ["CL", "CO", "CR", "MX", "IL"]   # section 2's expectation, in its order


# ---------------------------------------------------------------- the European parameters (seen data)

def european_frames():
    """The European look's panel from its cached confirm-half responses (seen; read directly, not through the European
    guard, which keeps unseen data closed): (cy, cl, fstd)."""
    eb, es = pspecs.build, pspecs.es
    raw = {}
    for m in eb.MANIFEST:
        g = eb.query_geos(m, es.COUNTRIES)
        code, filters, geos, since = es._check_query(m["dataset"], m["filters"], g, m.get("since"))
        q = json.dumps({"dataset": code, "filters": filters, "geos": geos, "since": since}, sort_keys=True,
                       separators=(",", ":"))
        path = os.path.join(es.RAW, "confirm", f"{code}__{hashlib.sha1(q.encode()).hexdigest()[:12]}.json")
        df = es.parse(json.load(open(path, encoding="utf-8")))
        if len(df) and "year" in df:                           # long-run cells: dropped at parse, never used
            df = df[pd.to_numeric(df["year"], errors="coerce") > fetch.EUROPEAN_LAST].reset_index(drop=True)
        raw[m["id"]] = df
    cy = eb.country_year("confirm", raw=raw, geos=es.COUNTRIES)
    cl = eb.country_level("confirm", raw=raw, geos=es.COUNTRIES)
    return cy, cl, pspecs.f_constants(cl, es.COUNTRIES)


def _resid(y, X):
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    return y - X @ b, b


def trend_ratios(M: pd.DataFrame, e: np.ndarray, H: dict) -> dict:
    """Variance of country-trend and H x trend components fitted to residuals e, relative to what is left."""
    t = (M["year"].to_numpy(float) - M.groupby("geo")["year"].transform("mean").to_numpy(float)) / 10
    D = np.column_stack([(M["geo"].to_numpy() == c) * t for c in sorted(set(M["geo"]))])
    e1, bc = _resid(e, D)
    tc = D @ bc
    h = M["geo"].map(H).fillna(0).to_numpy(float)
    e2, bh = _resid(e, (h * t)[:, None])
    s2 = float(np.var(e1))
    return dict(ratio_c=float(np.var(tc)) / s2, ratio_H=float(np.var((h * t) * bh[0])) / s2, sigma_e=math.sqrt(s2),
                slope_var_c=float(np.var(bc)), var_t=float(np.mean([np.var(t[M["geo"].to_numpy() == c])
                                                                     for c in sorted(set(M["geo"]))])),
                var_ht=float(np.var(h * t)))


def european_parameters() -> dict:
    cy, cl, fstd = european_frames()
    d = cy.reset_index().sort_values(["geo", "year"])
    dq = d.groupby("geo")["logq"].diff()
    dq = dq[np.isfinite(dq) & (d["year"].diff() == 1)]
    u = d[["geo", "year", "U2554"]].dropna()
    um = u.groupby("geo")["U2554"].transform("mean")
    dev = u["U2554"] - um
    lag = dev.groupby(u["geo"]).shift(1)
    ok = np.isfinite(lag)
    rho_u = float(np.sum(dev[ok] * lag[ok]) / np.sum(lag[ok] ** 2))
    ctx = pspecs.Ctx(cl, fstd)
    Fraw = cl["F_raw"].dropna()
    H_eu = specs.compute_H(Fraw.to_dict(), list(Fraw.index))
    out = dict(q_drift=float(dq.mean()), q_sd=float(dq.std(ddof=1)), U_mean=float(u["U2554"].mean()),
               U_sd=float(u["U2554"].std(ddof=1)), U_rho=rho_u, H_europe=H_eu)
    for name, test in (("D1", "D1"), ("C6", "C6"), ("C1", "C1")):
        fr = pspecs.frame(cy, pspecs.TESTS[test], ctx, pspecs.es.COUNTRIES)
        y, x, Z, g, M = pspecs.design(fr, pspecs.TESTS[test]["fe"])
        X = np.column_stack([np.ones(len(y)), x, Z])
        ok = np.isfinite(y) & np.isfinite(X).all(1)
        e, b = _resid(y[ok], X[ok])
        tr = trend_ratios(M[ok].reset_index(drop=True), e, H_eu)
        out[name] = dict(tr, n=int(ok.sum()), G=int(len(set(g))))
        if name == "D1":                                       # g: D1's coefficient on U (Z = [FE, names, breaks])
            names = fr["names"]
            n_fe = inf.fe_matrix(M, list(pspecs.TESTS[test]["fe"])).shape[1]
            iu = names.index("c0") if "c0" in names else None
            out["g_U"] = float(b[2 + n_fe + iu]) if iu is not None else 0.0
        out[name]["rows"] = [[str(a), int(t)] for a, t in zip(M["geo"][ok], M["year"][ok])]
        out[name]["frame_breaks"] = [[str(a), int(t)] for a, t in fr["breaks"]]   # observation years, all variables
        out[name]["q_breaks"] = {c: sorted({int(t) for t in bl}) for c, bl in
                                 zip(cy.reset_index()["geo"], cy.reset_index()["logq_l1__breaks"]) if len(bl)}
    return out


# ---------------------------------------------------------------- skeletons

def longrun_skeleton(cube: dict, seg: pd.DataFrame) -> dict:
    """From data/coverage.json: per test, the member countries and the observation years with data."""
    fam = cube["families"]
    C = cube["countries"]
    sk = {"members": fam["members"], "testable": fam["testable"], "countries": {}}
    for c, v in C.items():
        sk["countries"][c] = dict(
            q_years=sorted(int(y) for y in v["q_ladder"]),
            chosen=v["chosen_q_segment"],
            ranking=v["ranking_years"], eligible=v["eligible_K2_Y0"], school=v["school_years"],
            census=[y for y in v["extract_B_censuses"] if str(y - 1) in v["q_ladder"]],
            window=fetch.window(c))
    sk["breaks"] = {s: {c: sorted(int(t) for t in seg[(seg["geo"] == c) & (seg["series"] == s)]["tau"])
                        for c in fetch.COUNTRIES} for s in ("lfs", "q", "school", "coresid")}
    return sk


def european_skeleton(par: dict) -> dict:
    """The European benchmark skeletons: D1's rows (LR-K2, LR-Y0), C-6's (C-6L), C-1's (LR-C1)."""
    sk = {"countries": {}, "breaks": {"lfs": {}, "q": {}, "school": {}, "coresid": {}}}
    # the segment dummies the European look's frames carried (observation years, every variable of the frame): D1's
    # act on the A2534 rows, C-6's on school, C-1's on coresidence (no lag shift: already observation years)
    for key, ser in (("D1", "lfs"), ("C6", "school"), ("C1", "coresid")):
        for g, t in par[key].get("frame_breaks", []):
            sk["breaks"][ser].setdefault(g, []).append(int(t))
    rows = {k: pd.DataFrame(par[k]["rows"], columns=["geo", "year"]) for k in ("D1", "C6", "C1")}
    d1 = rows["D1"]
    for c in sorted(set(d1["geo"]) | set(rows["C6"]["geo"]) | set(rows["C1"]["geo"])):
        yrs = sorted(d1.loc[d1["geo"] == c, "year"])
        qb = [t for t in par["D1"]["q_breaks"].get(c, [])]
        cuts = [min(yrs + [9999])] + [t for t in qb if yrs and min(yrs) < t <= max(yrs)] + [10000]
        pieces = [[y for y in yrs if a <= y < b] for a, b in zip(cuts[:-1], cuts[1:])]
        piece = sorted(pieces, key=lambda p: (len(p), p[0] if p else 0))[-1] if pieces else []
        all_y = sorted(set(yrs) | set(rows["C6"].loc[rows["C6"]["geo"] == c, "year"])
                       | set(rows["C1"].loc[rows["C1"]["geo"] == c, "year"]))
        sk["countries"][c] = dict(q_years=list(range(min(all_y) - 1, max(all_y) + 1)) if all_y else [],
                                  chosen=[piece[0] - 1, piece[-1] - 1] if piece else None,
                                  ranking=piece, eligible=piece,
                                  school=sorted(rows["C6"].loc[rows["C6"]["geo"] == c, "year"]),
                                  census=sorted(rows["C1"].loc[rows["C1"]["geo"] == c, "year"]),
                                  window=all_y)
    H = par["H_europe"]
    k2 = sorted(c for c, v in sk["countries"].items() if len(v["eligible"]) >= 6 and c in H)
    sk["members"] = {"K2": k2, "Y0": sorted(c for c, v in sk["countries"].items() if len(v["eligible"]) >= 6),
                     "C6L": sorted(set(rows["C6"]["geo"])), "C1": sorted(set(rows["C1"]["geo"]))}
    sk["testable"] = {"K2": True, "Y0": True, "C6L": True, "C1": True}
    sk["H_fixed"] = {c: H[c] for c in k2}
    sk["european"] = True
    return sk


# ---------------------------------------------------------------- one synthetic world

def ar1(rng, n, rho, sd):
    x = np.zeros(n)
    if n == 0:
        return x
    x[0] = rng.normal(0, sd)
    s = sd * math.sqrt(1 - rho * rho)
    for i in range(1, n):
        x[i] = rho * x[i - 1] + rng.normal(0, s)
    return x


def world(sk: dict, par: dict, rho: float, seed, plant: dict | None = None, scale: str = "D1",
          H_fixed: dict | None = None, stress: dict | None = None) -> specs.Data:
    """One synthetic world on the skeleton: a specs.Data with cy, knots, H, members and the census frame. seed: an int
    or a numpy SeedSequence. stress: country-specific logistic curves timed by floor group (STRESS)."""
    rng = np.random.default_rng(seed)
    plant = plant or {}
    D = par["D1"]
    sig = {"A2534": D["sigma_e"], "school2024": par["C6"]["sigma_e"], "R": par["C1"]["sigma_e"]}
    sd_c = math.sqrt(D["ratio_c"] * D["sigma_e"] ** 2 / max(D["var_t"], 1e-12))
    sd_h = math.sqrt(D["ratio_H"] * D["sigma_e"] ** 2 / max(D.get("var_ht", D["var_t"]), 1e-12))
    C = sk["countries"]
    k2m = sk["members"].get("K2", [])
    if H_fixed is not None:
        H = dict(H_fixed)
    else:
        F = {c: float(rng.normal()) for c in k2m}
        H = specs.compute_H(F, k2m)
    tau_h = rng.normal(0, sd_h)
    rows, cens = [], []
    qtab, segtab = {}, {}
    yeff = {}
    for c in sorted(C):
        v = C[c]
        win = v["window"]
        if not win:
            continue
        lo = min(min(win), min(v["q_years"]) + 1 if v["q_years"] else min(win))
        hi = max(win)
        years = np.arange(lo - 1, hi + 1)
        q = np.cumsum(rng.normal(par["q_drift"], par["q_sd"], len(years)))
        qy = dict(zip(years.tolist(), q.tolist()))
        U = par["U_mean"] + ar1(rng, len(years), par["U_rho"], par["U_sd"])
        Uy = dict(zip(years.tolist(), U.tolist()))
        tau_c = rng.normal(0, sd_c)
        a_c = rng.normal(0, 5)
        tbar = np.mean(win)
        e = {k: dict(zip(years.tolist(), ar1(rng, len(years), rho, sig[k]).tolist())) for k in sig}
        h = H.get(c, 0)
        qyears = set(v["q_years"])
        if stress:
            mid = (stress["mid_high"] if h else stress["mid_low"]) + rng.uniform(-stress["jitter"], stress["jitter"])
        for t in win:
            yeff.setdefault(t, rng.normal(0, 2))
            x = qy.get(t - 1) if (t - 1) in qyears else np.nan
            trend = (tau_c + tau_h * h) * (t - tbar) / 10
            if stress:
                trend += stress["amp"] / (1.0 + math.exp(-(t - mid) / stress["scale"]))
            base = a_c + yeff[t] + trend + par.get("g_U", 0.0) * Uy[t]
            rows.append(dict(geo=c, year=t, logq_l1=x, U=Uy[t], _base=base, _eA=e["A2534"][t],
                             _eS=e["school2024"][t], _h=h, in_elig=t in set(v["eligible"]),
                             in_school=t in set(v["school"]),
                             qseg_l1=(v["chosen"][0] if v["chosen"] and v["chosen"][0] <= t - 1 <= v["chosen"][1]
                                      else -1)))
        for t in v["census"]:
            xq = qy.get(t - 1, np.nan)
            cens.append(dict(geo=c, year=t, x=xq, _base=a_c + yeff.setdefault(t, rng.normal(0, 2)) + (tau_c) *
                             (t - tbar) / 10, _eR=e["R"].get(t, rng.normal(0, sig["R"]))))
    cy = pd.DataFrame(rows)
    # knots from q alone, then the outcomes (planted effects act through the basis, U or x)
    qf = cy.set_index(["geo", "year"])[["logq_l1", "qseg_l1"]]
    chosen = {c: tuple(v["chosen"]) for c, v in C.items() if v["chosen"]}
    kn = specs.knots(qf, chosen, unseen_only=not sk.get("european", False))
    P = np.full((len(cy), 3), np.nan)
    for c, k in kn.items():
        if k.get("k1") is None:
            continue
        m = (cy["geo"] == c).to_numpy() & cy["year"].isin(k["years"]).to_numpy()
        P[m] = specs.basis(cy.loc[m, "logq_l1"].to_numpy(float), k["k1"], k["k2"])
    yA = cy["_base"].to_numpy(float) + cy["_eA"].to_numpy(float)
    Pn = np.nan_to_num(P)
    yA = yA + plant.get("DiD", 0.0) * cy["_h"].to_numpy(float) * Pn[:, 2] + plant.get("g1", 0.0) * Pn[:, 0]
    cy["A2534"] = np.where(cy["in_elig"].to_numpy(bool), yA, np.nan)
    yS = cy["_base"].to_numpy(float) + cy["_eS"].to_numpy(float) + plant.get("school", 0.0) * cy["U"].to_numpy(float)
    cy["school2024"] = np.where(cy["in_school"].to_numpy(bool), yS, np.nan)
    br = sk["breaks"]
    cy["A2534__breaks"] = [br["lfs"].get(g, []) for g in cy["geo"]]
    cy["U__breaks"] = [br["lfs"].get(g, []) for g in cy["geo"]]
    cy["school2024__breaks"] = [br["school"].get(g, []) for g in cy["geo"]]
    cy["logq_l1__breaks"] = [[t + 1 for t in br["q"].get(g, [])] for g in cy["geo"]]
    for col in ("A5564", "AW2554", "AM2554", "A2534_M", "A2534_F", "cohort", "strict"):
        cy[col] = np.nan
        cy[col + "__breaks"] = [[] for _ in range(len(cy))]
    cy = cy.set_index(["geo", "year"])
    census = pd.DataFrame(cens, columns=["geo", "year", "x", "_base", "_eR"])
    if len(census):
        census["R"] = census["_base"] + census["_eR"] + plant.get("C1", 0.0) * census["x"]
        census["round"] = ((census["year"] - 1975) // 10) * 10 + 1975
        census["R__breaks"] = [br["coresid"].get(g, []) for g in census["geo"]]
    cl = pd.DataFrame({"geo": sorted(C), "F_L": [np.nan] * len(C)}).set_index("geo")
    members = {k: [c for c in v if c in C] for k, v in sk["members"].items()}
    return specs.Data(cy, cl, {"q": kn}, H={c: H[c] for c in k2m if kn.get(c, {}).get("k1") is not None},
                      members=members, census=census)


# ---------------------------------------------------------------- evaluating one world

def evaluate(data: specs.Data, B: int, R: int, seed: int, tests=TESTS, with_ri=True, residual_sd=False) -> dict:
    out = {}
    if "LR-K2" in tests and data.H:
        M = specs.basis_frame(data, sorted(data.H), "A2534")
        if not M.empty and specs.k2_testable(data.H)[0]:
            r = specs.k2_core(M, data.H, B, R, seed, with_ri=with_ri)
            if "error" not in r:
                o = dict(beta=r["beta"], p=r["p_stat"], po=r["p_stat_opposite"], p_wcr=r["p_wcr"],
                         p_ri=r.get("p_ri"), G=r["G"])
                if residual_sd:
                    o.update(_sds_k2(M, data.H))
                out["LR-K2"] = o
    for t, key in (("LR-Y0", "Y0"), ("C-6L", "C6L"), ("LR-C1", "C1")):
        if t not in tests:
            continue
        if t == "LR-C1" and not len(data.census):
            continue
        r = specs.simple_test(data, t, data.members.get(key, []), B=B, seed=seed)
        if "error" not in r:
            o = dict(beta=r["beta"], p=r["p_stat"], po=r["p_stat_opposite"], G=r["G"])
            if residual_sd:
                o.update(_sds_simple(data, t, key))
            out[t] = o
    return out


def _sds_k2(M, H) -> dict:
    X6 = specs._k2_X(M, H)
    x, Zr = specs.infl.contrast(X6, specs.DID)
    Z = np.column_stack([np.ones(len(M)), specs._Z(M, ["geo", "year"], ["U"]), Zr])
    Q = inf._basis(Z)
    xt = x - Q @ (Q.T @ x)
    y = M["y"].to_numpy(float)
    yt = y - Q @ (Q.T @ y)
    share = {c: float(np.sum(xt[(M["geo"] == c).to_numpy()] ** 2) / np.sum(xt ** 2)) for c in sorted(set(M["geo"]))}
    return dict(sd_x=float(np.std(xt)), sd_y=float(np.std(yt)), share=share)


def _sds_simple(data, t, key) -> dict:
    if t == "LR-Y0":
        M = specs.basis_frame(data, data.members.get(key, []), "A2534")
        x = M["P1"].to_numpy(float)
        Z = specs._Z(M, ["geo", "year"], ["U"], M[["P2", "P3"]].to_numpy(float))
    else:
        M = specs.linear_frame(data, t, data.members.get(key, []))
        x = (M["x"] if t == "LR-C1" else M["U"]).to_numpy(float)
        Z = specs._Z(M, ["geo", "round"] if t == "LR-C1" else ["geo", "year"], [])
    Q = inf._basis(Z)
    y = M["y"].to_numpy(float)
    return dict(sd_x=float(np.std(x - Q @ (Q.T @ x))), sd_y=float(np.std(y - Q @ (Q.T @ y))))


# ---------------------------------------------------------------- the simulation

def seeds(seed0: int, i: int):
    """Two independent children of SeedSequence(seed0 + i): the world's, and an int seed for the WCR/RI draws."""
    w, b = np.random.SeedSequence(seed0 + i).spawn(2)
    return w, int(b.generate_state(1)[0])


def _one(args) -> dict:
    sk, par, rho, i, B, R, seed0, plant, residual_sd, tests, with_ri, H_fixed, stress = args
    ws, bs = seeds(seed0, i)
    d = world(sk, par, rho, ws, plant, H_fixed=H_fixed, stress=stress)
    return evaluate(d, B, R, bs, tests, with_ri, residual_sd)


WORKERS = 1


def simulate(sk, par, rho, n, B, R, seed0, plant=None, residual_sd=False, tests=TESTS, with_ri=True,
             H_fixed=None, log=None, stress=None) -> list[dict]:
    """n replications; each depends only on (seed0, i), so the result is the same for any number of workers."""
    t0 = time.time()
    jobs = [(sk, par, rho, i, B, R, seed0, plant, residual_sd, tests, with_ri, H_fixed, stress) for i in range(n)]
    if WORKERS > 1:
        with ProcessPoolExecutor(max_workers=WORKERS) as ex:
            out = list(ex.map(_one, jobs, chunksize=max(1, n // (8 * WORKERS))))
    else:
        out = []
        for i, j in enumerate(jobs):
            out.append(_one(j))
            if log and (i + 1) % max(1, n // 10) == 0:
                print(f"    {log}: {i + 1}/{n} ({time.time() - t0:.0f}s)", flush=True)
    if log:
        print(f"    {log}: {n} replications in {time.time() - t0:.0f}s", flush=True)
    return out


def summarise_null(reps, tests=TESTS) -> dict:
    out = {}
    for t in tests:
        p = np.array([r[t]["p"] for r in reps if t in r])
        po = np.array([r[t]["po"] for r in reps if t in r])
        b = np.array([r[t]["beta"] for r in reps if t in r])
        if not len(p):
            continue
        out[t] = dict(n=int(len(p)), size_pred=float(np.mean(p <= 0.05)), size_opp=float(np.mean(po <= 0.05)),
                      pred=sorted(p.tolist()), opp=sorted(po.tolist()), sd_beta=float(np.std(b, ddof=1)))
    return out


def mde_table(reps, tests=TESTS) -> dict:
    out = {}
    for t in tests:
        rs = [r[t] for r in reps if t in r]
        if len(rs) < 3:
            continue
        sd = float(np.std([r["beta"] for r in rs], ddof=1))
        G = int(np.median([r["G"] for r in rs]))
        m = inf.mde(sd, G)
        sdx = float(np.mean([r["sd_x"] for r in rs]))
        sdy = float(np.mean([r["sd_y"] for r in rs]))
        o = dict(sd_beta=sd, G=G, mde=m, sd_x_resid=sdx, sd_y_resid=sdy, std_mde=m * sdx / sdy)
        if t == "LR-K2" and "share" in rs[0]:
            cs = sorted({c for r in rs for c in r["share"]})
            o["identifying_variation_share"] = {c: float(np.mean([r["share"].get(c, 0.0) for r in rs])) for c in cs}
        out[t] = o
    return out


def expected_split(members: list[str]) -> dict:
    """Section 2's expected floor split, fixed a priori: the first floor(n/2) of EXPECTED_HIGH among the members are
    high floor, everyone else low (n = the LR-K2 members)."""
    hi = [c for c in EXPECTED_HIGH if c in members][: len(members) // 2]
    return {c: int(c in hi) for c in members}


def size_with(reps, test: str, cal: dict) -> dict:
    """Raw and calibrated (by the main table) size of a set of null replications, both directions."""
    p = np.array([r[test]["p"] for r in reps if test in r], float)
    po = np.array([r[test]["po"] for r in reps if test in r], float)
    p, po = p[np.isfinite(p)], po[np.isfinite(po)]
    cp = np.array([specs.calibrated(test, x, "pred", cal)[0] for x in p])
    co = np.array([specs.calibrated(test, x, "opp", cal)[0] for x in po])
    return dict(n=int(len(p)), size_pred_raw=float(np.mean(p <= 0.05)) if len(p) else None,
                size_opp_raw=float(np.mean(po <= 0.05)) if len(po) else None,
                size_pred_calibrated=float(np.mean(cp < 0.05)) if len(cp) else None,
                size_opp_calibrated=float(np.mean(co < 0.05)) if len(co) else None)


def code_sha() -> dict:
    files = ["skeleton.py", "specs.py", "inference_l.py", "build.py", "coverage.py", "segments.py", "fetch.py"]
    return {f: hashlib.sha256(open(os.path.join(HERE, f), "rb").read().replace(b"\r\n", b"\n")).hexdigest()
            for f in files}


def main() -> None:
    global WORKERS
    quick = "--quick" in sys.argv
    if "--workers" in sys.argv:
        WORKERS = int(sys.argv[sys.argv.index("--workers") + 1])
    rc, rm, rp = (60, 60, 30) if quick else (R_CAL, R_MDE, R_POWER)
    B = 999 if quick else 9999
    cube = json.load(open(CUBE, encoding="utf-8"))
    seg = sg.load()
    print("European parameters (seen data) ...", flush=True)
    par = european_parameters()
    sk = longrun_skeleton(cube, seg)
    tests = tuple(t for t, k in (("LR-K2", "K2"), ("LR-Y0", "Y0"), ("C-6L", "C6L"), ("LR-C1", "C1"))
                  if sk["testable"].get(k))
    res = {"written": str(date.today()), "quick": quick, "B": B, "R_ri": 9999, "seed": SEED,
           "replications": {"calibration_per_rho": rc, "mde": rm, "power": rp}, "tests": list(tests),
           "dgp": {k: v for k, v in par.items() if k not in ("D1", "C6", "C1")} | {
               k: {kk: vv for kk, vv in par[k].items() if kk not in ("rows", "q_breaks")} for k in ("D1", "C6", "C1")},
           "code_sha256": code_sha()}
    cal, sizes, holdout = {}, {}, {}
    for j, rho in enumerate(RHOS_CAL):
        print(f"  null worlds, rho {rho}", flush=True)
        reps = simulate(sk, par, rho, rc, B, 9999, SEED + 100000 * (j + 1), tests=tests, log=f"rho {rho}")
        s = summarise_null(reps, tests)
        for t, v in s.items():
            cal.setdefault(t, {})[f"rho{rho}"] = {"pred": v["pred"], "opp": v["opp"]}
            sizes.setdefault(t, {})[f"rho{rho}"] = {"size_pred": v["size_pred"], "size_opp": v["size_opp"],
                                                    "n": v["n"]}
        # held-out check, cross-fitted: calibrate on one half, measure the calibrated size on the other, both ways,
        # and report the mean (one split alone mixes the two halves' Monte Carlo noise into the check)
        half = len(reps) // 2
        sa, sb = summarise_null(reps[:half], tests), summarise_null(reps[half:], tests)
        holdout_opp = res.setdefault("size_calibrated_holdout_opposite", {})
        for t in sb:
            if t not in sa:
                continue
            got = {"pred": [], "opp": []}
            for cal_on, test_on in ((sa, sb), (sb, sa)):
                tab = {t: {"x": {"pred": cal_on[t]["pred"], "opp": cal_on[t]["opp"]}}}
                for d in ("pred", "opp"):
                    ps = [specs.calibrated(t, p, d, tab)[0] for p in test_on[t][d]]
                    got[d].append(float(np.mean(np.array(ps) < 0.05)))
            holdout.setdefault(t, {})[f"rho{rho}"] = float(np.mean(got["pred"]))
            holdout_opp.setdefault(t, {})[f"rho{rho}"] = float(np.mean(got["opp"]))
            res.setdefault("size_calibrated_holdout_splits", {}).setdefault(t, {})[f"rho{rho}"] = got
    res["calibration"] = cal
    res["size_uncalibrated"] = sizes
    res["size_calibrated_holdout"] = holdout
    print(f"  MDE worlds, rho {RHO_MDE}", flush=True)
    reps = simulate(sk, par, RHO_MDE, rm, B, 9999, SEED + 900000, tests=tests, with_ri=False, residual_sd=True,
                    log="mde")
    mde = mde_table(reps, tests)
    res["mde"] = mde
    print("  European benchmarks", flush=True)
    esk = european_skeleton(par)
    breps = simulate(esk, par, RHO_MDE, rm, B, 9999, SEED + 700000, tests=tests, with_ri=False, residual_sd=True,
                     H_fixed=esk["H_fixed"], log="benchmark")
    bench = mde_table(breps, tests)
    res["benchmark"] = {t: {k: v for k, v in b.items() if k != "identifying_variation_share"} for t, b in bench.items()}
    res["mde_kind"] = ("SD-based t-formula MDE: inference.mde of the SD of the tested estimate across null "
                       "replications (80% power for a t test); the power of the actual verdict procedure (max(p_WCR, "
                       "p_RI), calibrated) at this MDE is power_at_mde, published beside it")
    res["reading_basis"] = {t: dict(std_mde=mde[t]["std_mde"], benchmark_std_mde=bench[t]["std_mde"],
                                    inconclusive_reads=("no support" if mde[t]["std_mde"] <= bench[t]["std_mde"]
                                                        else "uninformative"))
                            for t in mde if t in bench}
    print("  planted worlds (power at the MDE)", flush=True)
    plant = {"LR-K2": {"DiD": -mde.get("LR-K2", {}).get("mde", 0.0)}, "LR-Y0": {"g1": mde.get("LR-Y0", {}).get("mde", 0)},
             "C-6L": {"school": mde.get("C-6L", {}).get("mde", 0)}, "LR-C1": {"C1": mde.get("LR-C1", {}).get("mde", 0)}}
    power = {}
    for t in tests:
        preps = simulate(sk, par, RHO_MDE, rp, B, 9999, SEED + 500000, plant[t], tests=(t,), log=f"power {t}")
        ps = [specs.calibrated(t, r[t]["p"], "pred", cal)[0] for r in preps if t in r]
        raw = [r[t]["p"] for r in preps if t in r]
        power[t] = dict(planted=list(plant[t].values())[0], n=len(ps), power_calibrated=float(np.mean(np.array(ps) < .05)),
                        power_raw=float(np.mean(np.array(raw) < 0.05)))
    res["power_at_mde"] = power
    for t in mde:
        mde[t]["power_at_mde_calibrated"] = power.get(t, {}).get("power_calibrated")
    if "LR-K2" in tests:
        k2m = sk["members"].get("K2", [])
        Hx = expected_split(k2m)
        res["expected_split"] = dict(H=Hx, rule="first floor(n/2) of " + ", ".join(EXPECTED_HIGH) + " among the members")
        for rho in RHOS_CAL:
            reps = simulate(sk, par, rho, R_EXTRA if not quick else rc, B, 9999, SEED + 300000 + int(rho * 100),
                            tests=("LR-K2",), H_fixed=Hx, log=f"expected split rho {rho}")
            res["expected_split"][f"rho{rho}"] = size_with(reps, "LR-K2", cal)
        res["stress_nulls"] = dict(what="reported beside the calibration, not in it (folding them into the envelope "
                                        "is a protocol amendment)", logistic=dict(STRESS), rho_high=RHO_STRESS)
        res["stress_nulls"]["logistic_late"] = dict(STRESS_LATE)
        for key, st, sd in (("logistic_by_floor_group_rho0.7", STRESS, 410000),
                            ("logistic_late_high_floor_rho0.7", STRESS_LATE, 430000)):
            reps = simulate(sk, par, RHO_MDE, R_EXTRA if not quick else rc, B, 9999, SEED + sd, tests=("LR-K2",),
                            H_fixed=Hx, stress=st, log=f"stress: {key}")
            res["stress_nulls"][key] = size_with(reps, "LR-K2", cal)
        reps = simulate(sk, par, RHO_STRESS, R_EXTRA if not quick else rc, B, 9999, SEED + 420000, tests=("LR-K2",),
                        log=f"stress: rho {RHO_STRESS}")
        res["stress_nulls"][f"rho{RHO_STRESS}"] = size_with(reps, "LR-K2", cal)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(specs.clean_json(res), f)
    for t in tests:
        print(f"  {t}: size raw {sizes[t]}; calibrated holdout {holdout.get(t)}; MDE {mde.get(t, {}).get('mde')}; "
              f"std MDE {mde.get(t, {}).get('std_mde')} vs Europe {bench.get(t, {}).get('std_mde')}; power {power[t]}")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
