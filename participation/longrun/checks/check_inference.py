# check_inference.py — the long run's inference (code/inference_l.py, code/specs.py) and the skeleton simulation
# (code/skeleton.py, data/skeleton.json).
#   (a) the RI check of PROTOCOL section 5: on a design with one interaction (x = H_c x m_i) and 7 units, the H
#       permutation RI (inference_l.ri_generic, combinations) equals the frozen inference.ri (permutations of the unit
#       values), to 1e-10 in p, in both directions; the fast LR-K2 RI (ContrastT, inference_l.ri_h) equals the full
#       refit (ri_generic) on a LR-K2-shaped design, to 1e-10;
#   (b) ContrastT's CR1 t of the DiD contrast equals the frozen inference.wcr's t on the rewritten regression;
#   (c) Newey-West with 0 lags equals the HC0 sandwich;
#   (d) the skeleton (data/skeleton.json): computed by the current code (SHA-256 recorded); not a --quick run; for every
#       verdict test the calibrated size on held-out null replications (cross-fitted, both directions) is within the
#       protocol's bound (0.05 plus two Monte Carlo standard errors of a held-out size, which carries the noise of
#       both halves), so the size-corrected (calibrated) p is what the verdicts use; the raw sizes are
#       reported; MDEs and standardised MDEs finite and positive, with the European benchmarks; power at the MDE
#       reported; LR-K2's identifying-variation shares sum to one;
#   (e) calibration only ever makes a verdict harder: the calibrated p is never below the raw p.
#
# Run from longrun/:  ../../venv/Scripts/python.exe checks/check_inference.py      Exit status 0 only if all pass.

from __future__ import annotations

import hashlib
import json
import math
import os
import sys

import numpy as np
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
LROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(LROOT, "code"))
import inference_l as infl  # noqa: E402
import skeleton  # noqa: E402
import specs  # noqa: E402

inf = specs.inf
RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


# ---------------------------------------------------------------- (a) RI against the frozen inference.ri
print("(a) randomisation inference")
rng = np.random.default_rng(7)
units = [f"U{i}" for i in range(7)]
T = 12
geo = np.repeat(units, T)
year = np.tile(np.arange(T), 7)
m = rng.normal(size=len(geo))
Hobs = np.array([1, 0, 1, 0, 0, 1, 0], float)
hmap = dict(zip(units, Hobs))
y = 0.4 * np.array([hmap[g] for g in geo]) * m + rng.normal(size=len(geo)) + 0.3 * m
df = pd.DataFrame({"geo": geo, "year": year})
Z = np.column_stack([inf.fe_matrix(df, ["geo", "year"]), m])
ok_all, det = True, []
for side in (-1, 1):
    a = inf.ri(y, pd.Series(hmap), geo, pd.Series({u: "s" for u in units}), Z, side=side, x_mult=m)

    def build(hv):
        hh = dict(zip(units, hv))
        return y, np.array([hh[g] for g in geo]) * m, Z, geo
    b = infl.ri_generic(build, Hobs, side=side)
    ok_all &= a["exact"] and b["exact"] and abs(a["p"] - b["p"]) <= 1e-10
    det.append(f"side {side}: {a['p']:.6f} vs {b['p']:.6f}")
check("A1 H-permutation RI equals the frozen inference.ri on a one-interaction design with 7 units (exact, 1e-10)",
      ok_all, "; ".join(det))

# a LR-K2-shaped design: 8 countries, 15 years, basis terms
G, T = 8, 15
cs = [f"C{i}" for i in range(G)]
rows = []
for c in cs:
    xs = np.cumsum(rng.normal(0.03, 0.06, T))
    k1, k2 = np.quantile(xs, [1 / 3, 2 / 3])
    P = specs.basis(xs, k1, k2)
    for t in range(T):
        rows.append(dict(geo=c, year=2000 + t, P1=P[t, 0], P2=P[t, 1], P3=P[t, 2], U=rng.normal(6, 1),
                         y=rng.normal()))
M = pd.DataFrame(rows)
M.attrs["breaks"] = []
H = {c: int(i < 4) for i, c in enumerate(cs)}
Zc = specs._Z(M, ["geo", "year"], ["U"])
ct = infl.ContrastT(M["y"], M[["P1", "P2", "P3"]].to_numpy(float), Zc, M["geo"])
fast = infl.ri_h(ct, np.array([H[u] for u in ct.labels], float), specs.DID)


def build2(hv):
    hh = dict(zip(ct.labels, hv))
    x, Zr = infl.contrast(specs._k2_X(M, hh), specs.DID)
    return M["y"].to_numpy(float), x, np.column_stack([Zc, Zr]), M["geo"].to_numpy()


slow = infl.ri_generic(build2, np.array([H[u] for u in ct.labels], float), side=-1)
check("A2 the fast LR-K2 RI (residualised country blocks) equals the full refit for every assignment (1e-10)",
      abs(fast["p_lower"] - slow["p_lower"]) <= 1e-10 and abs(fast["p_upper"] - slow["p_upper"]) <= 1e-10
      and fast["n_perm"] == math.comb(8, 4), f"{fast['p_lower']:.6f}/{slow['p_lower']:.6f}, "
                                              f"{fast['p_upper']:.6f}/{slow['p_upper']:.6f}, n {fast['n_perm']}")

# ---------------------------------------------------------------- (b) ContrastT t = wcr t
print("(b) the contrast t")
x, Zr = infl.contrast(specs._k2_X(M, H), specs.DID)
w = inf.wcr(M["y"].to_numpy(float), x, np.column_stack([Zc, Zr]), M["geo"].to_numpy(), side=-1, B=999)
est, se, t = ct.t(ct.W(infl.floor_weights(np.array([H[u] for u in ct.labels], float))), specs.DID)
check("B1 ContrastT's DiD estimate, CR1 se and t equal the frozen wcr's on the rewritten regression",
      math.isclose(est, w["beta"], rel_tol=1e-8) and math.isclose(se, w["se"], rel_tol=1e-8)
      and math.isclose(t, w["t"], rel_tol=1e-8), f"{t:.6f} vs {w['t']:.6f}")
est2, se2, t2 = ct.t_contrast(ct.W(infl.floor_weights(np.array([H[u] for u in ct.labels], float))), specs.DID)
check("B2 the partialled-out contrast t (the RI's) equals the frozen wcr's as well",
      math.isclose(est2, w["beta"], rel_tol=1e-8) and math.isclose(se2, w["se"], rel_tol=1e-8)
      and math.isclose(t2, w["t"], rel_tol=1e-8), f"{t2:.6f} vs {w['t']:.6f}")

# ---------------------------------------------------------------- (c) Newey-West
print("(c) Newey-West")
X = rng.normal(size=(60, 2))
yy = X @ [1, -1] + rng.normal(size=60)
nw = infl.newey_west(yy, X, lags=0)
Xc = np.column_stack([np.ones(60), X])
b = np.linalg.lstsq(Xc, yy, rcond=None)[0]
u = yy - Xc @ b
A = np.linalg.inv(Xc.T @ Xc)
V = A @ (Xc.T * u ** 2) @ Xc @ A
check("C1 Newey-West with 0 lags equals HC0", np.allclose(nw["se"], np.sqrt(np.diag(V))[1:]))

# ---------------------------------------------------------------- (d) the skeleton
print("(d) the skeleton simulation")
S = json.load(open(skeleton.OUT, encoding="utf-8")) if os.path.exists(skeleton.OUT) else None
check("D0 data/skeleton.json exists", S is not None)
if S:
    now = skeleton.code_sha()
    check("D1 data/skeleton.json was computed by the current code (SHA-256 of the files it records)",
          S.get("code_sha256") == now, "; ".join(f for f in now if S.get("code_sha256", {}).get(f) != now[f]))
    check("D2 production settings: not a --quick run; B = 9999; 2000 null replications per rho",
          not S["quick"] and S["B"] == 9999 and S["replications"]["calibration_per_rho"] == 2000)
    for t in S["tests"]:
        raw = S["size_uncalibrated"][t]
        hold = S["size_calibrated_holdout"][t]
        n = min(v["n"] for v in raw.values()) // 2
        # the held-out size carries the Monte Carlo noise of the calibrating half and of the tested half
        bound = 0.05 + 2 * math.sqrt(2 * 0.05 * 0.95 / max(n, 1))
        hold_o = S.get("size_calibrated_holdout_opposite", {}).get(t, {})
        check(f"D3 {t}: calibrated size on held-out null replications within the bound ({bound:.3f}) at both rho, in "
              "both directions; the verdicts use the calibrated p",
              all(v <= bound for v in hold.values()) and hold_o and all(v <= bound for v in hold_o.values()),
              f"held-out {hold}; opposite {hold_o}; raw (reported) {raw}")
        mde, bm = S["mde"].get(t, {}), S["benchmark"].get(t, {})
        check(f"D4 {t}: MDE and standardised MDE finite and positive, with the European benchmark",
              all(np.isfinite(v) and v > 0 for v in (mde.get("mde", np.nan), mde.get("std_mde", np.nan),
                                                     bm.get("std_mde", np.nan))),
              f"MDE {mde.get('mde')}, std {mde.get('std_mde')}, Europe {bm.get('std_mde')}")
        pw = S["power_at_mde"].get(t, {})
        check(f"D5 {t}: power at the MDE reported (raw and calibrated) and published beside the MDE, which is labelled "
              "as the SD-based t-formula figure", "power_raw" in pw and "power_calibrated" in pw
              and mde.get("power_at_mde_calibrated") == pw.get("power_calibrated")
              and "t-formula" in S.get("mde_kind", ""), str(pw))
    sh = S["mde"].get("LR-K2", {}).get("identifying_variation_share")
    if sh:
        check("D6 LR-K2's identifying-variation shares by country sum to one (published before the look, L13)",
              abs(sum(sh.values()) - 1) < 1e-6, f"US {sh.get('US')}")
    ex = S.get("expected_split", {})
    st = S.get("stress_nulls", {})
    check("D7 reported beside the calibration (not in it): LR-K2's size at the protocol's expected split (both rho) and "
          "under the stress nulls (logistic curves by floor group; rho 0.95), raw and calibrated",
          bool(ex.get("H")) and all(f"rho{r}" in ex for r in skeleton.RHOS_CAL)
          and "logistic_by_floor_group_rho0.7" in st and f"rho{skeleton.RHO_STRESS}" in st,
          f"expected split {ex.get('H')}; " + "; ".join(f"{k}: {v}" for k, v in {**ex, **st}.items()
                                                       if isinstance(v, dict) and "n" in v))
    # (e) calibration is monotone and never below raw
    t0 = S["tests"][0]
    ps = np.linspace(0, 1, 41)
    cp = [specs.calibrated(t0, p, "pred", S["calibration"])[0] for p in ps]
    check("E1 the calibrated p is never below the raw p and is non-decreasing in it",
          all(c >= p - 1e-12 for c, p in zip(cp, ps)) and all(b >= a - 1e-12 for a, b in zip(cp[:-1], cp[1:])))

n_fail = sum(1 for _, ok, _ in RESULTS if not ok)
print(f"\n{len(RESULTS) - n_fail}/{len(RESULTS)} checks pass")
sys.exit(1 if n_fail else 0)
