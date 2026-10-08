# inference.py — the inference of PROTOCOL.md section 5 (recipe: docs/design_review.md, 'Inference method'): the
# restricted wild cluster bootstrap-t (WCR) with Webb six-point weights and the CR1 statistic, one-sided in the predicted
# direction; confidence intervals by test inversion; randomisation inference for country-level regressors (C-4, C-5);
# the effective number of clusters G* (Carter, Schnepel and Steigerwald 2017); the minimum detectable effect.
#
# Import from code/:  import inference as inf
# No outputs of its own. Validated on synthetic panels by code/simulate_inference.py (results/simulate_inference.json),
# asserted by checks/check_inference.py.
#
# Conventions:
# - y and x are 1-d; x is the single tested regressor. Z holds every other regressor (fixed-effect dummies, controls,
#   break dummies). A constant is always added to Z here, so dummies that drop one level (fe_matrix) never lose the
#   intercept. Z may be rank deficient: its column space is taken from an SVD, and K in CR1 is its rank plus one.
# - Rows with a non-finite y, x or Z entry, or a missing cluster label, are dropped.
# - CR1: V = c * sum_g s_g^2 / (xt'xt)^2, s_g = sum_{i in g} xt_i u_i, c = G/(G-1) * (N-1)/(N-K); xt = M_Z x.
# - The bootstrap runs on cluster scores. With M_Z = I - QQ', each bootstrap score s*_g is linear in the G weights:
#   s* = S v - c_g delta*, S[g,h] = 1[g=h] sum_{i in g} xt_i ur_i - (sum_{i in g} xt_i Q_i).(sum_{j in h} Q_j ur_j).
#   That is algebraically the N x B form of the design review (simulate_inference.py checks the two agree to 1e-10);
#   B draws cost a G x G by G x B product, and since ur = yt - beta0 xt, S is linear in beta0, which makes test
#   inversion cheap. The same weight matrix (seed) serves every beta0: common random numbers.
# - p-values: side=+1 tests H1 beta > beta0, side=-1 H1 beta < beta0: p = (1 + #{side t* >= side t}) / (B + 1);
#   side=0 is the symmetric two-sided p, (1 + #{|t*| >= |t|}) / (B + 1).

from __future__ import annotations

import itertools
import math

import numpy as np
import pandas as pd
from scipy import stats

SEED = 20261008
WEBB = np.array([-math.sqrt(1.5), -1.0, -math.sqrt(0.5), math.sqrt(0.5), 1.0, math.sqrt(1.5)])
EXACT_MAX = 10000          # randomisation inference enumerates exactly when the permutation count is at most this


def webb(G: int, B: int, seed: int = SEED) -> np.ndarray:
    """G x B matrix of Webb six-point weights, one draw per cluster (clusters in sorted label order) and replication."""
    return WEBB[np.random.default_rng(seed).integers(0, 6, size=(B, G))].T


def _basis(Z: np.ndarray) -> np.ndarray:
    """Orthonormal basis Q of the column space of [1, Z], so M_Z v = v - Q (Q'v)."""
    Zc = np.column_stack([np.ones(len(Z)), Z])
    U, s, _ = np.linalg.svd(Zc, full_matrices=False)
    return U[:, s > s[0] * max(Zc.shape) * np.finfo(float).eps]


def _clean(y, x, Z, labels):
    y = np.asarray(y, float).ravel()
    x = np.asarray(x, float).ravel()
    n = len(y)
    Z = np.zeros((n, 0)) if Z is None else np.asarray(Z, float).reshape(n, -1)
    labels = np.asarray(labels)
    ok = np.isfinite(y) & np.isfinite(x) & np.isfinite(Z).all(1) & ~pd.isna(labels)
    return y[ok], x[ok], Z[ok], labels[ok]


def _onehot(g: np.ndarray, G: int) -> np.ndarray:
    D = np.zeros((len(g), G))
    D[np.arange(len(g)), g] = 1.0
    return D


class _Fit:
    """The partialled-out regression of y on x given Z, with the pieces the restricted bootstrap needs."""

    def __init__(self, y, x, Z, clusters):
        y, x, Z, cl = _clean(y, x, Z, clusters)
        self.labels, self.g = np.unique(cl, return_inverse=True)
        self.n, self.G = len(y), len(self.labels)
        if self.G < 2:
            raise ValueError("fewer than two clusters")
        Q = _basis(Z)
        self.k = Q.shape[1] + 1
        self.x = x
        self.xt = x - Q @ (Q.T @ x)
        self.yt = y - Q @ (Q.T @ y)
        self.xx = float(self.xt @ self.xt)
        if self.xx <= 1e-12 * max(float(x @ x), 1e-300):
            raise ValueError("the tested regressor is collinear with Z")
        self.beta = float(self.xt @ self.yt) / self.xx
        self.u = self.yt - self.xt * self.beta
        self.c = self.G / (self.G - 1) * (self.n - 1) / (self.n - self.k)
        s = np.bincount(self.g, self.xt * self.u, self.G)
        self.se = math.sqrt(self.c * float(s @ s)) / self.xx
        D = _onehot(self.g, self.G)
        Xq = D.T @ (Q * self.xt[:, None])                     # G x r: sum_{i in g} xt_i Q_i
        Yq = D.T @ (Q * self.yt[:, None])
        self.cg = np.bincount(self.g, self.xt * self.xt, self.G)
        self.ay = np.bincount(self.g, self.xt * self.yt, self.G)
        self.Sx = np.diag(self.cg) - Xq @ Xq.T
        self.Sy = np.diag(self.ay) - Xq @ Yq.T

    def t(self, beta0: float) -> float:
        return (self.beta - beta0) / self.se

    def tstar(self, beta0: float, V: np.ndarray) -> np.ndarray:
        """Bootstrap t statistics (length B) under the restriction beta = beta0, for weights V (G x B)."""
        S = self.Sy - beta0 * self.Sx
        delta = ((self.ay - beta0 * self.cg) @ V) / self.xx
        sc = S @ V - self.cg[:, None] * delta
        return delta * self.xx / np.sqrt(self.c * np.einsum("gb,gb->b", sc, sc))


def _p(tstar: np.ndarray, t: float, side: int) -> float:
    if side == 0:
        return (1 + int(np.sum(np.abs(tstar) >= abs(t)))) / (len(tstar) + 1)
    return (1 + int(np.sum(side * tstar >= side * t))) / (len(tstar) + 1)


def g_star(x_tilde, clusters) -> float:
    """Effective number of clusters, scalar case with spherical within-cluster errors:
    G* = G / (1 + Var_g(gamma_g) / mean(gamma_g)^2), gamma_g = xt_g'xt_g / xt'xt (population variance)."""
    _, g = np.unique(np.asarray(clusters), return_inverse=True)
    xt = np.asarray(x_tilde, float)
    gam = np.bincount(g, xt * xt) / float(xt @ xt)
    return float(len(gam) / (1 + gam.var() / gam.mean() ** 2))


def _varying(xt, g, G) -> int:
    """Clusters with nonzero variation in xt, the tested regressor after partialling out Z (design review step 7):
    sum_{i in g} xt_i^2 > 1e-10 xt'xt. A cluster whose variation Z absorbs (break dummies, trends) does not count."""
    cg = np.bincount(g, xt * xt, G)
    return int(np.sum(cg > 1e-10 * float(xt @ xt)))


def _varying_raw(x, g, G) -> int:
    """Clusters in which the raw regressor is not constant (0 for a cross-section with one row per cluster)."""
    m = np.bincount(g, x, G) / np.bincount(g, None, G)
    dev = np.bincount(g, (x - m[g]) ** 2, G)
    return int(np.sum(dev > 1e-20 * max(float(x @ x), 1e-300)))


def wcr(y, x, Z, clusters, beta0: float = 0.0, side: int = +1, B: int = 9999, seed: int = SEED) -> dict:
    """Restricted wild cluster bootstrap-t (Webb weights, CR1). Keys: beta, se (CR1), t, p (in direction side),
    p_opposite (the other direction, same draws), n, G, G_star, n_clusters_varying (clusters with nonzero variation in
    xt = M_Z x), n_clusters_varying_raw (clusters where the raw x is not constant; 0 for a cross-section with one
    observation per cluster), plus beta0, side, B."""
    if side not in (-1, 0, 1):
        raise ValueError("side must be +1, -1 or 0")
    f = _Fit(y, x, Z, clusters)
    ts, t = f.tstar(beta0, webb(f.G, B, seed)), f.t(beta0)
    return dict(beta=f.beta, se=f.se, t=t, p=_p(ts, t, side), p_opposite=_p(ts, t, -side), n=f.n, G=f.G,
                G_star=g_star(f.xt, f.g), n_clusters_varying=_varying(f.xt, f.g, f.G),
                n_clusters_varying_raw=_varying_raw(f.x, f.g, f.G), beta0=beta0, side=side, B=B)


def ci(y, x, Z, clusters, alpha: float = 0.05, side: int = 0, B: int = 9999, seed: int = SEED,
       tol: float = 1e-6) -> tuple[float, float]:
    """Confidence set {beta0: p(beta0) > alpha} by inverting the WCR test, with the same weights for every beta0
    (common random numbers); each end is bracketed by doubling steps of the CR1 se and found by bisection to tol*se.
    side=0: symmetric two-sided, level 1-alpha. side=+1: [lo, inf) (inverts H1 beta > beta0); side=-1: (-inf, hi]."""
    f = _Fit(y, x, Z, clusters)
    V = webb(f.G, B, seed)

    def p(b0):
        return _p(f.tstar(b0, V), f.t(b0), side)

    def end(d):
        inside, step = f.beta, f.se
        out = f.beta + d * step
        for _ in range(60):
            if p(out) <= alpha:
                break
            inside, step = out, 2 * step
            out = f.beta + d * step
        else:
            return d * math.inf
        while abs(out - inside) > tol * f.se:
            mid = 0.5 * (inside + out)
            if p(mid) <= alpha:
                out = mid
            else:
                inside = mid
        return 0.5 * (inside + out)

    lo = end(-1) if side in (0, 1) else -math.inf
    hi = end(+1) if side in (0, -1) else math.inf
    return lo, hi


def _by_unit(v, units: np.ndarray) -> np.ndarray:
    if isinstance(v, pd.Series):
        return v.reindex(units).to_numpy()
    if isinstance(v, dict):
        return np.array([v.get(u, np.nan) for u in units], dtype=object)
    v = np.asarray(v)
    if len(v) != len(units):
        raise ValueError("a unit-level array must align with np.unique(unit_of_obs)")
    return v


def ri(y, x_unit, unit_of_obs, strata_of_unit, Z, side: int, R: int = 9999, seed: int = SEED,
       studentize: str = "CR1", x_mult=None) -> dict:
    """Randomisation inference for a unit-level regressor: the regressor of observation i is x_unit[unit_i] * x_mult_i
    (x_mult defaults to 1; C-4 passes 1[year >= 2023]). x_unit and strata_of_unit are dicts or Series keyed by unit, or
    arrays aligned with np.unique(unit_of_obs). The units' values are permuted within strata; for each assignment the
    regression on [x, Z] is refitted and the studentised t (CR1 clustered by unit, or HC2) recomputed. Exact
    enumeration when the product of stratum factorials is at most 10000, p = #{side t_perm >= side t} / n_perm (the
    identity included); otherwise R random draws, p = (1 + #{side t_perm >= side t}) / (R + 1)."""
    if side not in (-1, 1):
        raise ValueError("side must be +1 or -1")
    if studentize not in ("CR1", "HC2"):
        raise ValueError("studentize must be 'CR1' or 'HC2'")
    y = np.asarray(y, float).ravel()
    n0 = len(y)
    unit_of_obs = np.asarray(unit_of_obs)
    mult = np.ones(n0) if x_mult is None else np.asarray(x_mult, float).ravel()
    Z = np.zeros((n0, 0)) if Z is None else np.asarray(Z, float).reshape(n0, -1)
    units = np.unique(unit_of_obs[~pd.isna(unit_of_obs)])
    xu = np.asarray(_by_unit(x_unit, units), float)
    st = np.asarray(_by_unit(strata_of_unit, units))
    keep = np.isfinite(xu) & ~pd.isna(st)
    pos = {u: i for i, u in enumerate(units) if keep[i]}
    uidx = np.array([pos.get(u, -1) for u in unit_of_obs])
    ok = np.isfinite(y) & np.isfinite(mult) & np.isfinite(Z).all(1) & (uidx >= 0)
    y, mult, Z = y[ok], mult[ok], Z[ok]
    present, uidx = np.unique(uidx[ok], return_inverse=True)  # units with observations left
    xu, st = xu[present], st[present]
    U, n = len(xu), len(y)
    Q = _basis(Z)
    k = Q.shape[1] + 1
    yt = y - Q @ (Q.T @ y)
    D = _onehot(uidx, U)
    hz = np.einsum("ir,ir->i", Q, Q)
    c = U / (U - 1) * (n - 1) / (n - k)

    def tstats(P):                                            # P: m x U, row = an assignment of unit values
        Xp = (xu[P][:, uidx] * mult).T                        # n x m
        Xt = Xp - Q @ (Q.T @ Xp)
        xx = np.einsum("im,im->m", Xt, Xt)
        b = (Xt.T @ yt) / xx
        E = yt[:, None] - Xt * b
        if studentize == "CR1":
            sc = D.T @ (Xt * E)
            se = np.sqrt(c * np.einsum("gm,gm->m", sc, sc)) / xx
        else:
            h = hz[:, None] + Xt * Xt / xx
            w = np.where(1 - h > 1e-10, 1 / np.maximum(1 - h, 1e-10), 0.0)
            se = np.sqrt(np.einsum("im,im->m", Xt * Xt * E * E, w)) / xx
        return b, b / se

    ident = np.arange(U)
    b_obs, t_obs = (float(v[0]) for v in tstats(ident[None, :]))
    groups = [np.flatnonzero(st == s) for s in pd.unique(st)]
    count = math.prod(math.factorial(len(m)) for m in groups)
    exact = count <= EXACT_MAX
    if exact:
        perms = np.empty((count, U), int)
        for r, combo in enumerate(itertools.product(*[itertools.permutations(m) for m in groups])):
            for m, pm in zip(groups, combo):
                perms[r, m] = pm
        blocks = [perms[i:i + 1000] for i in range(0, count, 1000)]
    else:
        rng = np.random.default_rng(seed)

        def draw(m):
            P = np.tile(ident, (m, 1))
            for mem in groups:
                P[:, mem] = rng.permuted(np.tile(mem, (m, 1)), axis=1)
            return P
        blocks = (draw(min(1000, R - i)) for i in range(0, R, 1000))
    tol = 1e-9 * max(1.0, abs(t_obs))
    hits = sum(int(np.sum(side * tstats(P)[1] >= side * t_obs - tol)) for P in blocks)
    p = hits / count if exact else (1 + hits) / (R + 1)
    return dict(beta=b_obs, t=t_obs, p=p, n_perm=count if exact else R, exact=exact, n=n, G=U)


def mde(se: float, G: int, alpha: float = 0.05, power: float = 0.8) -> float:
    """Minimum detectable effect of a one-sided level-alpha test: (t_{1-alpha} + t_{power}) * se, t with G-1 df."""
    return float((stats.t.ppf(1 - alpha, G - 1) + stats.t.ppf(power, G - 1)) * se)


def fe_matrix(df: pd.DataFrame, cols) -> np.ndarray:
    """Dummies for each column in cols (one or a list), dropping the first level (sorted) of each. No constant:
    wcr, ci and ri add one."""
    cols = [cols] if isinstance(cols, str) else list(cols)
    blocks = [pd.get_dummies(df[c].astype("category"), drop_first=True, dtype=float).to_numpy() for c in cols]
    return np.column_stack(blocks) if blocks else np.zeros((len(df), 0))
