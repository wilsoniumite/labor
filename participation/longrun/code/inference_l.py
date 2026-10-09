# inference_l.py — the long run's additions to the frozen participation/code/inference.py (imported, never edited):
#   contrast(X, c)      — rewrite a regression on the columns X so that one coefficient is the linear contrast c'gamma
#                         (x = X_j / c_j, Z gets X_i - (c_i / c_j) X_j), so the frozen WCR can test a contrast;
#   ContrastT           — the CR1-studentised t of a contrast in a regression whose H-dependent regressors are linear
#                         combinations of country-specific columns, built once (the FWL residuals of every
#                         country x basis column on the common Z); every H assignment then costs a few small products;
#   ri_h(...)           — randomisation inference for LR-K2 (PROTOCOL section 5): H permuted across all the test's
#                         countries with the number of high-floor countries fixed, every H-interaction rebuilt, the
#                         CR1 t recomputed; exact enumeration when C(G, h) <= inference.EXACT_MAX, else R draws;
#                         p = #{side t_perm >= side t - tol} / n (exact) or (1 + #) / (R + 1), tol as inference.ri.
#                         The t of the contrast is computed from the rewritten regression by partialling out (an SVD
#                         basis, as inference._Fit), so a nuisance slope that one assignment leaves unidentified does
#                         not matter; an observed t that is not finite gives p = NaN with the reason, never 0; the
#                         number of assignments whose t is not finite is reported, and in exact mode any such
#                         assignment makes p NaN (the enumeration is no longer the full distribution);
#   newey_west(...)     — OLS with Newey-West (Bartlett) standard errors for the US deep study (section 6).
# The RI check of PROTOCOL section 5 (agreement with inference.ri on a one-interaction design with at most 7 units, to
# 1e-10 in p) is checks/check_inference.py's.

from __future__ import annotations

import itertools
import math
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
PCODE = os.path.join(os.path.dirname(os.path.dirname(HERE)), "code")       # participation/code (frozen)
if PCODE not in sys.path:
    sys.path.append(PCODE)                                       # after longrun/code: its names win
import inference as inf  # noqa: E402

EXACT_MAX = inf.EXACT_MAX


def contrast(X: np.ndarray, c) -> tuple[np.ndarray, np.ndarray]:
    """(x, Zc): regressing y on [x, Zc] gives c'gamma as x's coefficient, where gamma are y's coefficients on X."""
    X = np.asarray(X, float)
    c = np.asarray(c, float)
    j = int(np.flatnonzero(np.abs(c) > 0)[-1])
    x = X[:, j] / c[j]
    Zc = np.column_stack([X[:, i] - (c[i] / c[j]) * X[:, j] for i in range(X.shape[1]) if i != j]) \
        if X.shape[1] > 1 else np.zeros((len(X), 0))
    return x, Zc


class ContrastT:
    """The CR1 t of c'gamma in y = W(H) gamma + Z delta + e, clustered by unit, where every column of W(H) is
    sum_u w_u(H) B_u for country-specific blocks B_u (n x m: the basis columns times 1[unit = u]) and weights
    determined by H. Rows with a non-finite y, B or Z are dropped once, at construction."""

    def __init__(self, y, B: np.ndarray, Z, units):
        y = np.asarray(y, float)
        B = np.asarray(B, float)                       # n x m: the m basis columns (P1, P2, P3, ...)
        n = len(y)
        Z = np.zeros((n, 0)) if Z is None else np.asarray(Z, float).reshape(n, -1)
        units = np.asarray(units)
        ok = np.isfinite(y) & np.isfinite(B).all(1) & np.isfinite(Z).all(1) & ~pd.isna(units)
        self.y, self.B, self.Z, units = y[ok], B[ok], Z[ok], units[ok]
        self.labels, self.g = np.unique(units, return_inverse=True)
        self.G, self.n, self.m = len(self.labels), len(self.y), B.shape[1]
        Q = inf._basis(self.Z)
        self.Q = Q
        self.yt = self.y - Q @ (Q.T @ self.y)
        # residualised country blocks: R[u] is n x m, M_Z (1[unit = u] * B)
        self.R = np.zeros((self.G, self.n, self.m))
        for u in range(self.G):
            blk = self.B * (self.g == u)[:, None]
            self.R[u] = blk - Q @ (Q.T @ blk)
        self.k0 = Q.shape[1]

    def W(self, weights: np.ndarray) -> np.ndarray:
        """Residualised regressors for unit weights (G x p x m: column p = sum_u sum_j weights[u, p, j] R[u][:, j])."""
        return np.einsum("upj,unj->np", weights, self.R)

    def t(self, Wt: np.ndarray, c) -> tuple[float, float, float]:
        """(estimate, CR1 se, t) of c'gamma from residualised regressors Wt (n x p)."""
        c = np.asarray(c, float)
        A = Wt.T @ Wt
        rank = np.linalg.matrix_rank(A)
        if rank < A.shape[0]:
            return math.nan, math.nan, math.nan
        Ai = np.linalg.inv(A)
        b = Ai @ (Wt.T @ self.yt)
        u = self.yt - Wt @ b
        S = np.zeros((Wt.shape[1], Wt.shape[1]))
        for gi in range(self.G):
            s = Wt[self.g == gi].T @ u[self.g == gi]
            S += np.outer(s, s)
        k = self.k0 + Wt.shape[1]                     # as inference.wcr: rank of [1, Z] plus the tested block
        cc =self.G / (self.G - 1) * (self.n - 1) / (self.n - k)
        V = cc * Ai @ S @ Ai
        est, se = float(c @ b), float(math.sqrt(max(c @ V @ c, 0.0)))
        return est, se, (est / se if se > 0 else math.nan)

    def t_contrast(self, Wt: np.ndarray, c) -> tuple[float, float, float]:
        """(estimate, CR1 se, t) of c'gamma from the rewritten regression (x = column j / c_j, the other columns
        rewritten as nuisance regressors), partialled out with an SVD basis: identical to t() (and to inference.wcr on
        the rewritten regression) when every slope is identified, and still defined when only nuisance slopes are not.
        NaN when the contrast itself is not identified."""
        x, Zr = contrast(Wt, c)
        Qr = np.zeros((len(x), 0))
        if Zr.shape[1]:
            U, sv, _ = np.linalg.svd(Zr, full_matrices=False)
            if len(sv) and sv[0] > 0:
                Qr = U[:, sv > sv[0] * max(Zr.shape) * np.finfo(float).eps]
        xt = x - Qr @ (Qr.T @ x)
        yt = self.yt - Qr @ (Qr.T @ self.yt)
        xx = float(xt @ xt)
        if xx <= 1e-12 * max(float(x @ x), 1e-300):
            return math.nan, math.nan, math.nan
        b = float(xt @ yt) / xx
        u = yt - xt * b
        k = self.k0 + Qr.shape[1] + 1                  # as inference.wcr: rank of [1, Z, Zr] plus the tested column
        cc = self.G / (self.G - 1) * (self.n - 1) / (self.n - k)
        sg = np.bincount(self.g, xt * u, self.G)
        se = math.sqrt(cc * float(sg @ sg)) / xx
        return b, se, (b / se if se > 0 else math.nan)


def floor_weights(H: np.ndarray, m: int = 3) -> np.ndarray:
    """G x 2m x m weights: columns 0..m-1 are (1 - H) * P_j, columns m..2m-1 are H * P_j."""
    G = len(H)
    w = np.zeros((G, 2 * m, m))
    for j in range(m):
        w[:, j, j] = 1 - H
        w[:, m + j, j] = H
    return w


def assignments(G: int, h: int, R: int = 9999, seed: int = inf.SEED) -> tuple[np.ndarray, bool]:
    """All assignments of h high-floor units among G (exact) or R random ones; row 0 is not special."""
    count = math.comb(G, h)
    if count <= EXACT_MAX:
        out = np.zeros((count, G), int)
        for r, idx in enumerate(itertools.combinations(range(G), h)):
            out[r, list(idx)] = 1
        return out, True
    rng = np.random.default_rng(seed)
    out = np.zeros((R, G), int)
    for r in range(R):
        out[r, rng.choice(G, h, replace=False)] = 1
    return out, False


def ri_h(ct: ContrastT, H_obs: np.ndarray, c, weights_of=floor_weights, R: int = 9999, seed: int = inf.SEED) -> dict:
    """RI for a contrast whose regressors depend on a unit-level binary H (aligned with ct.labels): H permuted across
    all units, the count of ones fixed. Returns the observed t, p in both directions, the number of assignments."""
    H_obs = np.asarray(H_obs, float)
    est, se, t_obs = ct.t_contrast(ct.W(weights_of(H_obs)), c)
    P, exact = assignments(ct.G, int(H_obs.sum()), R, seed)
    ts_all = np.array([ct.t_contrast(ct.W(weights_of(p.astype(float))), c)[2] for p in P])
    ok = np.isfinite(ts_all)
    ts = ts_all[ok]
    n_bad = int((~ok).sum())
    out = dict(beta=est, se=se, t=t_obs, n_perm=int(len(ts)), n_nonfinite=n_bad, exact=exact)
    if not np.isfinite(t_obs):
        return {**out, "p_lower": math.nan, "p_upper": math.nan, "error": "the observed contrast t is not finite"}
    if exact and n_bad:
        return {**out, "p_lower": math.nan, "p_upper": math.nan,
                "error": f"{n_bad} of {len(ts_all)} enumerated assignments leave the contrast unidentified"}
    if not len(ts):
        return {**out, "p_lower": math.nan, "p_upper": math.nan, "error": "no assignment gives a finite t"}
    tol = 1e-9 * max(1.0, abs(t_obs))

    def pval(side):
        hits = int(np.sum(side * ts >= side * t_obs - tol))
        return hits / len(ts) if exact else (1 + hits) / (len(ts) + 1)
    return {**out, "p_lower": pval(-1), "p_upper": pval(+1)}


def ri_generic(build, units_H: np.ndarray, side: int = -1, R: int = 9999, seed: int = inf.SEED) -> dict:
    """RI by full refit: build(H) -> (y, x, Z, clusters); the CR1 t of x recomputed for every assignment of H
    (count fixed). Used by the RI check against inference.ri and for designs whose Z depends on H (the floor-group
    trend qualifier). p is in direction `side`; p_lower and p_upper are both directions from the same assignments."""
    def tstat(H):
        y, x, Z, g = build(H)
        f = inf._Fit(y, x, Z, g)
        return f.beta / f.se
    t_obs = tstat(np.asarray(units_H, float))
    P, exact = assignments(len(units_H), int(np.sum(units_H)), R, seed)
    ts = []
    n_bad = 0
    for p in P:
        try:
            v = tstat(p.astype(float))
        except ValueError:
            v = math.nan
        if np.isfinite(v):
            ts.append(v)
        else:
            n_bad += 1
    ts = np.asarray(ts, float)
    out = dict(t=t_obs, n_perm=int(len(ts)), n_nonfinite=n_bad, exact=exact)
    if not np.isfinite(t_obs) or (exact and n_bad) or not len(ts):
        why = ("the observed t is not finite" if not np.isfinite(t_obs) else
               f"{n_bad} enumerated assignments give no t" if (exact and n_bad) else "no finite t")
        return {**out, "p": math.nan, "p_lower": math.nan, "p_upper": math.nan, "error": why}
    tol = 1e-9 * max(1.0, abs(t_obs))

    def pval(sd):
        hits = int(np.sum(sd * ts >= sd * t_obs - tol))
        return hits / len(ts) if exact else (1 + hits) / (len(ts) + 1)
    return {**out, "p": pval(side), "p_lower": pval(-1), "p_upper": pval(+1)}


def newey_west(y, X, lags: int = 4) -> dict:
    """OLS of y on [1, X] with Newey-West (Bartlett kernel) standard errors; rows with a missing value dropped (the
    time order of the remaining rows is the order given)."""
    y = np.asarray(y, float)
    X = np.asarray(X, float).reshape(len(y), -1)
    ok = np.isfinite(y) & np.isfinite(X).all(1)
    y, X = y[ok], np.column_stack([np.ones(ok.sum()), X[ok]])
    XtX = np.linalg.pinv(X.T @ X)
    b = XtX @ X.T @ y
    u = y - X @ b
    Xu = X * u[:, None]
    S = Xu.T @ Xu
    for L in range(1, lags + 1):
        w = 1 - L / (lags + 1)
        G = Xu[L:].T @ Xu[:-L]
        S += w * (G + G.T)
    V = XtX @ S @ XtX
    se = np.sqrt(np.maximum(np.diag(V), 0))
    return dict(beta=b[1:].tolist(), se=se[1:].tolist(), n=int(ok.sum()), lags=lags)
