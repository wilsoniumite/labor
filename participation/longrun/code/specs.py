# specs.py — the tests of longrun/PROTOCOL.md section 5, one primary specification each, with their verdicts.
#
# Inference is the frozen participation/code/inference.py (wcr, ci, ri, g_star, mde) and the verdict helpers of the
# frozen participation/code/specs.py (break_dummies, holm, holm_reject, qualify), imported unedited; inference_l.py adds
# the contrast rewrite and LR-K2's H-permutation randomisation inference.
#
# TESTS is the coded form of section 5 (checks/check_protocol.py compares it line by line with its own transcription
# of PROTOCOL.md). Every panel regression has country and year fixed effects, the segment dummies of L7 (every
# '<var>__breaks' year of every variable in it: outcome, tested regressor, controls; 1[geo = c, year >= tau], dummies
# constant within c dropped, as the frozen break_dummies does) and the cycle U, unless stated. Countries weigh equally
# (L13); the cluster is the country; B = 9999.
#
# The piecewise basis (section 5): per country, the ranking set is every observation year in the unseen window whose
# lagged q lies in the country's chosen q segment (the piece of it with the most ranking years, ties the later, if
# B flags split it when the values arrived), known from q alone; ranked by x (ties by the earlier year), rank r of n
# falls in tercile ceil(3r/n); k1 is the midpoint between tercile 1's largest x and tercile 2's smallest, k2 likewise;
# P1 = min(x, k1), P2 = min(max(x - k1, 0), k2 - k1), P3 = max(x - k2, 0). Fewer than 6 ranked years: the country leaves
# LR-K2 and LR-Y0. knots() runs at each opening on q alone and its result is recorded in the fetch log before any
# outcome is fetched; the explore countries keep their explore-opening knots at the look.
#
# Choices the protocol leaves to the code, fixed here:
# - H (L9): countries ordered by F_L descending, ties by country code ascending; the first floor(n/2) are high floor
#   (so with an odd count the middle country is low floor). Computed once (at the look), never recomputed: LOO,
#   qualifiers and the robustness rows that keep F_L hold it fixed; the three robustness rows that define another F
#   (Giuliano-Nunn, ages 20-29, the sample nearest 1970) split that F by the same rule over their own countries, since
#   that is what the row varies (L9 as settled on 2026-10-09).
# - LR-K2's DiD is the coefficient of H*P3 after the contrast rewrite (inference_l.contrast) of the six slopes
#   [(1-H)P1, (1-H)P2, (1-H)P3, H P1, H P2, H P3] with c = (1, 0, -1, -1, 0, 1).
# - The verdict statistic of LR-K2 is max(p_WCR, p_RI) in each direction; every test's verdict p is max(raw p,
#   calibrated p), the calibrated p being the share of the skeleton's null replications (at the rho that gives the
#   larger share) whose statistic is at or below the observed one (data/skeleton.json; without it the p is raw and the
#   result says 'uncalibrated'). The leave-one-out and qualifier runs use the same statistic, calibrated the same way.
# - The C-L tests' qualifier is the frozen leave-one-out one; for the US it reads 'rests on the US, a partly seen
#   country' (L13).
# - E-SCH1-L's U_{t-1} is the previous calendar year's U of the same country (missing if that year is missing).
# - LR-C1's census round is the decade 1975-84, 1985-94, ...; its q segment dummies are the lagged q's breaks.
# - D2-L's m_cs is the mean of x within country x q segment over the D2-L estimation rows.
# - Time terciles (the curvature qualifier): each country's ranking-set years (the knots' years, from q alone) in
#   calendar order, rank r of n in tercile ceil(3r/n); estimation rows take their year's tercile.
# - Holm runs over the families frozen at L2 (data/coverage.json 'families', LR-C1 only with Extract B): a frozen member
#   whose run errors at the look, or whose verdict statistic is not finite, takes p = 1 in both directions inside its
#   family (it is never dropped, which would make Holm easier). LR-K2 failing testability at the look is 'not testable'.
# - Every qualifier, leave-one-out and robustness run is guarded on its own: a design that cannot be estimated is
#   reported as that run's error and never stops the others.
# - Leave-one-out: every country's run is reported for every verdict test; the US row is reported by name, and whenever
#   it alone pushes the own-direction p above 0.10 (or flips the sign) the qualifier reads 'rests on the US, a partly
#   seen country' (L13), whichever country is worst.
# - Post-freeze segments (section 8) never enter a primary frame: they are passed as data.post_seg and used only by
#   the robustness row 'with post-freeze segments' (post=True).
# - The confirm-half replication (run(..., replication=True)) reports LR-K2 for information whenever each floor group
#   has at least 2 countries, without the testability gate of the primary.
# - The series-permutation placebo: 999 derangements (seed inference.SEED); a derangement is redrawn until no country
#   keeps its own path.
#
# run(data, ...) -> every test, the verdicts, qualifiers, no-verdict quantities and robustness runs.

from __future__ import annotations

import importlib.util
import json
import math
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
LROOT = os.path.dirname(HERE)
PCODE = os.path.join(os.path.dirname(LROOT), "code")                # participation/code (frozen)
sys.path.insert(0, HERE)
if PCODE not in sys.path:
    sys.path.append(PCODE)
import inference as inf  # noqa: E402  (participation/code/inference.py)
import inference_l as infl  # noqa: E402
import fetch  # noqa: E402
import segments as sg  # noqa: E402


def _load_frozen_specs():
    """participation/code/specs.py, imported under another name (this module is also called specs)."""
    spec = importlib.util.spec_from_file_location("participation_specs", os.path.join(PCODE, "specs.py"))
    mod = importlib.util.module_from_spec(spec)
    saved = sys.path[:]
    clash = {k: sys.modules.pop(k) for k in ("build", "specs") if k in sys.modules}   # the long run's own modules
    sys.path.insert(0, PCODE)
    try:
        spec.loader.exec_module(mod)
    finally:
        sys.path[:] = saved
        for k in ("build", "specs"):                       # the European build stays reachable as mod.build only
            sys.modules.pop(k, None)
        sys.modules.update(clash)
    return mod


pspecs = _load_frozen_specs()
break_dummies, holm, holm_reject, frozen_qualify = pspecs.break_dummies, pspecs.holm, pspecs.holm_reject, pspecs.qualify

ALPHA = 0.05
LOO_P = pspecs.LOO_P                         # 0.10, as frozen
B_DEFAULT = 9999
MIN_RANKED = 6
MIN_K2_COUNTRIES, MIN_K2_GROUP = 8, 3
DROP_SIG = 0.05                              # the drop condition: gamma3^H not significantly positive at 5%
PLACEBO_DRAWS = 999
DID = (1, 0, -1, -1, 0, 1)                   # (g1L, g2L, g3L, g1H, g2H, g3H)
FIT_ERRORS = (ValueError, ZeroDivisionError, np.linalg.LinAlgError, KeyError)
SKELETON = os.path.join(LROOT, "data", "skeleton.json")
EUROPE_LOOK = os.path.join(os.path.dirname(LROOT), "results", "confirm_8623706.json")

TESTS = {
    "LR-K2": dict(family="K", outcome="A2534", tested="DiD = (g3H - g1H) - (g3 - g1)", basis=True, controls=["U"],
                  fe=["geo", "year"], side=-1, inference="wcr + ri (co-primary)", members="K2",
                  what="regime-aware floor kink: the fall in the young's q slope from bottom to top tercile, high F "
                       "minus low F"),
    "LR-Y0": dict(family="C-L", outcome="A2534", tested="g1 (bottom-tercile slope)", basis=True, controls=["U"],
                  fe=["geo", "year"], side=1, inference="wcr", members="Y0",
                  what="the young respond positively before enclosure"),
    "C-6L": dict(family="C-L", outcome="school2024", tested="U", basis=False, controls=[], fe=["geo", "year"],
                 side=1, inference="wcr", members="C6L", what="school as a paid exit: attending 20-24 on U 25-54"),
    "LR-C1": dict(family="C-L", outcome="R", tested="logq", basis=False, controls=[], fe=["geo", "round"], side=1,
                  inference="wcr", members="C1", census=True,
                  what="coresidence 25-34 absorbs rents (Extract B censuses 1976+)"),
}
FAMILIES = {"K": ["LR-K2"], "C-L": ["LR-Y0", "C-6L", "LR-C1"]}
NO_VERDICT = {
    "D1-L": dict(outcome="A2534", x="Q*F", z=["Q"], controls=["U"], what="b2 on log q x F (F = standardised F_L)"),
    "D2-L": dict(outcome="A2534", x="sqdev(Q)", z=["Q"], controls=["U"], what="(x - m_cs)^2, m_cs within country x "
                                                                                 "q segment"),
    "C-2L": dict(outcome="A2534-A5564", x="Q", z=[], controls=["U"], what="young minus old on log q"),
    "C-3L.diff": dict(outcome="AW2554-AM2554", x="Q", z=[], controls=["U"], what="women minus men 25-54 on log q"),
    "C-3L.women": dict(outcome="AW2554", x="Q", z=[], controls=["U"], what="women 25-54 on log q"),
    "E-SCH1-L": dict(outcome="school2024", x="U_l1", z=[], controls=[], what="school on last year's U"),
}
ROBUSTNESS = {
    "giuliano_nunn": ["LR-K2", "D1-L"],
    "F_L_2029": ["LR-K2"],
    "F_L_continuous": ["LR-K2"],
    "men_only": ["LR-K2", "LR-Y0"],
    "women_only": ["LR-K2", "LR-Y0"],
    "strict_control_dropped": ["LR-K2", "LR-Y0", "LR-C1"],
    "q_hpi": ["LR-K2", "LR-Y0", "LR-C1"],
    "F_L_1970_later_years": ["LR-K2", "D1-L"],
    "flagged_samples_dropped": ["LR-K2", "D1-L"],
    "post_freeze_segments": ["LR-K2", "LR-Y0", "C-6L", "LR-C1"],
}
K2_QUALIFIERS = ["rests on one country", "rests on floor-group trends", "rests on cohort size",
                 "rests on control-era years", "indistinguishable from time curvature"]
READING = {"contradicted": "stands, whatever the data quality, with the auxiliaries its label names",
           "supported": "stands, with its qualifiers",
           "inconclusive_at_or_below": "no support", "inconclusive_above": "uninformative"}
MODEL_READINGS = {
    "favours": "favours the floor mechanism against the no-coresidence and attenuation accounts",
    "consistent": "consistent with the floor mechanism or with an attenuated response at high floor (carried by "
                  "low-floor convexity)",
    "against": "against the floor mechanism together with its stated regime placement and auxiliaries 1-3",
    "inconclusive": "inconclusive", "not testable": "not testable"}
KAPLAN_SENTENCE = ("It does not discriminate against life-cycle models with a below-market parental room (Kaplan 2012; "
                   "Ermisch): against them the kink is not distinctive, only against models without a coresidence "
                   "option.")


# ---------------------------------------------------------------- the data a run needs

class Data:
    """cy: panel (geo, year) from build.panel; cl: country level; census: LR-C1 frame; knots: {'q': {c: ...},
    'q_hpi': {...}}; H: {c: 0/1}; members: {'K2': [...], 'Y0': [...], 'C6L': [...], 'C1': [...]}; calibration optional;
    post_seg: the post-freeze segment rows (data/segments_postfreeze.csv; only the no-verdict run uses them);
    families: the families frozen at L2 ({'K': [...], 'C-L': [...]}); kh_uncovered: countries the Kholodilin coding
    does not cover."""

    def __init__(self, cy, cl, knots, H=None, members=None, census=None, calibration=None, post_seg=None,
                 families=None, kh_uncovered=None):
        self.cy = cy
        self.cl = cl
        self.knots = knots
        self.H = dict(H or {})
        self.members = members or {}
        self.census = census if census is not None else pd.DataFrame()
        self.calibration = calibration
        self.post_seg = post_seg if post_seg is not None else pd.DataFrame(columns=sg.COLUMNS)
        self.families = families
        self.kh_uncovered = kh_uncovered


# ---------------------------------------------------------------- knots and the basis

def knots(qf: pd.DataFrame, chosen: dict, col: str = "logq_l1", segcol: str = "qseg_l1",
          unseen_only: bool = True) -> dict:
    """{c: {k1, k2, n, years, terciles, piece}} from q alone (qf: index (geo, year) with the lagged q and its segment);
    chosen: {c: (first q year, last q year)} frozen at L2. A country with fewer than 6 ranked years gets n and no
    knots."""
    out = {}
    for c, span in chosen.items():
        if span is None or c not in set(qf.index.get_level_values(0)):
            continue
        d = qf.xs(c, level=0)
        if unseen_only:                                  # False only for the European benchmark skeleton (seen)
            d = d[[fetch.is_unseen(c, int(t)) for t in d.index]]
        x = pd.to_numeric(d[col], errors="coerce")
        seg = pd.to_numeric(d[segcol], errors="coerce")
        a, b = span
        qyear = d.index.to_numpy(int) - 1
        ok = np.isfinite(x.to_numpy(float)) & (qyear >= a) & (qyear <= b)
        d, x, seg = d[ok], x[ok], seg[ok]
        if not len(d):
            out[c] = dict(n=0, k1=None, k2=None, years=[], piece=None)
            continue
        pieces = {}
        for t, s in zip(d.index.astype(int), seg.astype(int)):
            pieces.setdefault(int(s), []).append(t)
        piece = sorted(pieces.items(), key=lambda kv: (len(kv[1]), kv[0]))[-1]
        yrs = sorted(piece[1])
        xs = {t: float(x[t]) for t in yrs}
        n = len(yrs)
        if n < MIN_RANKED:
            out[c] = dict(n=n, k1=None, k2=None, years=yrs, piece=piece[0])
            continue
        order = sorted(yrs, key=lambda t: (xs[t], t))
        terc = {t: math.ceil(3 * (r + 1) / n) for r, t in enumerate(order)}
        t1 = [xs[t] for t in yrs if terc[t] == 1]
        t2 = [xs[t] for t in yrs if terc[t] == 2]
        t3 = [xs[t] for t in yrs if terc[t] == 3]
        k1 = 0.5 * (max(t1) + min(t2))
        k2 = 0.5 * (max(t2) + min(t3))
        out[c] = dict(n=n, k1=k1, k2=k2, years=yrs, piece=piece[0], terciles={str(t): terc[t] for t in yrs})
    return out


def basis(x, k1: float, k2: float) -> np.ndarray:
    x = np.asarray(x, float)
    return np.column_stack([np.minimum(x, k1), np.clip(x - k1, 0, k2 - k1), np.maximum(x - k2, 0)])


def compute_H(F: dict, countries) -> dict:
    """L9: H = 1 for the top half of F among these countries (ties by country code; odd count: the middle is low)."""
    cs = [c for c in sorted(countries) if c in F and np.isfinite(F[c])]
    order = sorted(cs, key=lambda c: (-F[c], c))
    hi = set(order[: len(order) // 2])
    return {c: int(c in hi) for c in cs}


def k2_testable(H: dict) -> tuple[bool, str]:
    n, h = len(H), sum(H.values())
    if n < MIN_K2_COUNTRIES or h < MIN_K2_GROUP or n - h < MIN_K2_GROUP:
        return False, f"not testable: {n} countries, {h} high and {n - h} low floor (needs >= 8 and >= 3 per group)"
    return True, ""


# ---------------------------------------------------------------- frames

def _outcome(d: pd.DataFrame, spec: str) -> np.ndarray:
    if "-" in spec:
        a, b = spec.split("-")
        return d[a].to_numpy(float) - d[b].to_numpy(float)
    return d[spec].to_numpy(float)


def _outcome_vars(spec: str) -> list[str]:
    return spec.split("-")


def _breaks(d: pd.DataFrame, variables) -> list[tuple[str, int]]:
    out = set()
    for v in variables:
        col = v + "__breaks"
        if col in d:
            for g, bl in zip(d["geo"], d[col]):
                out.update((g, int(t)) for t in bl)
    return sorted(out)


def _post_breaks(data: Data, geos, variables) -> list[tuple[str, int]]:
    """Segment starts from the post-freeze rows (section 8): the no-verdict run 'with post-freeze segments' only."""
    if data.post_seg is None or not len(data.post_seg):
        return []
    return sg.breaks(data.post_seg, geos, variables)


def basis_frame(data: Data, geos, outcome: str = "A2534", controls=("U",), knot_key: str = "q",
                qcol: str = "logq_l1", rows=None, post: bool = False) -> pd.DataFrame:
    """Rows of the piecewise tests: each country's ranking-set years (the knots' piece), outcome and controls present.
    post=True adds the post-freeze segments (the no-verdict run only; a primary frame never has them)."""
    kn = data.knots.get(knot_key, {})
    d = data.cy.reset_index()
    parts = []
    for c in sorted(geos):
        k = kn.get(c)
        if not k or k.get("k1") is None:
            continue
        e = d[(d["geo"] == c) & d["year"].isin(k["years"])].copy()
        P = basis(e[qcol].to_numpy(float), k["k1"], k["k2"])
        e["P1"], e["P2"], e["P3"] = P[:, 0], P[:, 1], P[:, 2]
        parts.append(e)
    if not parts:
        return pd.DataFrame()
    e = pd.concat(parts, ignore_index=True)
    e["y"] = _outcome(e, outcome)
    need = ["y", qcol] + list(controls)
    e = e[np.isfinite(e[need].to_numpy(float)).all(1)]
    if rows is not None:
        e = e[rows(e)]
    vars_ = _outcome_vars(outcome) + [qcol] + list(controls)
    e.attrs["breaks"] = sorted(set(_breaks(e, vars_)) | set(_post_breaks(data, set(e["geo"]), vars_) if post else []))
    return e.reset_index(drop=True)


def _Z(M: pd.DataFrame, fe, controls, extra=None) -> np.ndarray:
    blocks = [inf.fe_matrix(M, list(fe)), M[list(controls)].to_numpy(float).reshape(len(M), -1),
              break_dummies(M, M.attrs.get("breaks", []))]
    if extra is not None:
        blocks.append(extra)
    return np.column_stack(blocks)


# ---------------------------------------------------------------- LR-K2

def _k2_X(M: pd.DataFrame, H: dict) -> np.ndarray:
    h = M["geo"].map(H).to_numpy(float)
    P = M[["P1", "P2", "P3"]].to_numpy(float)
    return np.column_stack([(1 - h)[:, None] * P, h[:, None] * P])


def k2_safe(*a, **k) -> dict:
    """k2_core, with a design that cannot be estimated reported as an error (never stops the run)."""
    try:
        return k2_core(*a, **k)
    except FIT_ERRORS as e:
        return dict(error=f"{type(e).__name__}: {e}"[:300])


def identifying_shares(M: pd.DataFrame, x: np.ndarray, Zw: np.ndarray) -> dict:
    """Each country's share of the squared residualised tested regressor (L13), and the shares by stratum."""
    Q = inf._basis(Zw)
    xt = x - Q @ (Q.T @ x)
    tot = float(np.sum(xt ** 2))
    g = M["geo"].to_numpy()
    sh = {c: float(np.sum(xt[g == c] ** 2) / tot) if tot > 0 else math.nan for c in sorted(set(g))}
    st: dict = {}
    for c, v in sh.items():
        st[fetch.stratum_of(c)] = st.get(fetch.stratum_of(c), 0.0) + v
    return dict(by_country=sh, by_stratum=st)


def k2_core(M: pd.DataFrame, H: dict, B: int = B_DEFAULT, R: int = 9999, seed: int = inf.SEED, extra_Z=None,
            with_ri: bool = True, fe=("geo", "year"), controls=("U",), z_of_H=None, with_ci: bool = False) -> dict:
    """LR-K2 on a basis frame: DiD by WCR (both directions) and by RI over H; the slopes and the drop condition.
    z_of_H(M, H) -> extra regressors that depend on H (the floor-group trend qualifier): the RI then refits them for
    every assignment (inference_l.ri_generic)."""
    br = list(M.attrs.get("breaks", []))
    M = M[M["geo"].isin(list(H))].reset_index(drop=True)
    M.attrs = {"breaks": [b for b in br if b[0] in set(M["geo"])]}
    if M.empty or len(set(M["geo"])) < 4:
        return dict(error="too few countries")
    y = M["y"].to_numpy(float)
    X6 = _k2_X(M, H)
    if z_of_H is not None:
        extra_Z = z_of_H(M, H)
    Zc = _Z(M, fe, controls, extra_Z)
    g = M["geo"].to_numpy()
    x, Zr = infl.contrast(X6, DID)
    r = inf.wcr(y, x, np.column_stack([Zc, Zr]), g, side=-1, B=B, seed=seed)
    out = dict(beta=r["beta"], se=r["se"], t=r["t"], p_wcr=r["p"], p_wcr_opposite=r["p_opposite"], n=r["n"],
               G=r["G"], G_star=r["G_star"], n_high=int(sum(H[c] for c in set(g))),
               geos_used=sorted(set(g)), years_used=sorted(int(t) for t in set(M["year"])),
               n_segment_dummies=int(break_dummies(M, M.attrs.get("breaks", [])).shape[1]),
               mde=inf.mde(r["se"], r["G"]),
               identifying_variation_share=identifying_shares(M, x, np.column_stack([Zc, Zr])))
    if with_ci:                                       # intervals by inverting the WCR test (section 5)
        Zw = np.column_stack([Zc, Zr])
        out["ci"] = list(inf.ci(y, x, Zw, g, side=0, B=B, seed=seed))
        out["ci_one_sided"] = list(inf.ci(y, x, Zw, g, side=-1, B=B, seed=seed))
    ct = infl.ContrastT(y, M[["P1", "P2", "P3"]].to_numpy(float), Zc, g)
    Hv = np.array([H[u] for u in ct.labels], float)
    if with_ri and z_of_H is not None:
        labels = list(ct.labels)

        def build(hv):
            Hh = dict(zip(labels, hv))
            xx, Zrr = infl.contrast(_k2_X(M, Hh), DID)
            return y, xx, np.column_stack([_Z(M, fe, controls, z_of_H(M, Hh)), Zrr]), g
        rg = infl.ri_generic(build, Hv, side=-1, R=R, seed=seed)
        out.update(t_ri=rg["t"], p_ri=rg["p_lower"], p_ri_opposite=rg["p_upper"], n_perm=rg["n_perm"],
                   n_nonfinite=rg.get("n_nonfinite"), exact=rg["exact"])
        if "error" in rg:
            out["ri_error"] = rg["error"]
    elif with_ri:
        ri = infl.ri_h(ct, Hv, DID, R=R, seed=seed)
        out.update(t_ri=ri["t"], p_ri=ri["p_lower"], p_ri_opposite=ri["p_upper"], n_perm=ri["n_perm"],
                   n_nonfinite=ri.get("n_nonfinite"), exact=ri["exact"])
        if "error" in ri:
            out["ri_error"] = ri["error"]
    else:
        out.update(p_ri=math.nan, p_ri_opposite=math.nan)
    if with_ri:                                       # a co-primary that cannot be computed is never dropped silently
        ok = np.isfinite(out["p_ri"]) and np.isfinite(out["p_ri_opposite"])
        out["p_stat"] = max(out["p_wcr"], out["p_ri"]) if ok else math.nan
        out["p_stat_opposite"] = max(out["p_wcr_opposite"], out["p_ri_opposite"]) if ok else math.nan
    else:
        out["p_stat"], out["p_stat_opposite"] = out["p_wcr"], out["p_wcr_opposite"]
    # slopes from the full sandwich (no inference beyond their CR1 se), and the reported contrasts
    W = ct.W(infl.floor_weights(Hv))
    names = ["g1", "g2", "g3", "g1H", "g2H", "g3H"]
    sl = {}
    for i, nm in enumerate(names):
        e = np.zeros(6)
        e[i] = 1
        est, se, _ = ct.t(W, e)
        sl[nm] = dict(beta=est, se=se)
    out["slopes"] = sl
    x3, Z3 = infl.contrast(X6, (0, 0, 0, 0, 0, 1))
    r3 = inf.wcr(y, x3, np.column_stack([Zc, Z3]), g, side=1, B=B, seed=seed)
    xd, Zd = infl.contrast(X6, (0, 0, 0, -1, 0, 1))
    rd = inf.wcr(y, xd, np.column_stack([Zc, Zd]), g, side=-1, B=B, seed=seed)
    out["slope_top_high_F"] = dict(beta=r3["beta"], se=r3["se"], p_positive=r3["p"],
                                   what="gamma3^H, one-sided WCR p for gamma3^H > 0 (reported, not tested)")
    out["high_F_change"] = dict(beta=rd["beta"], se=rd["se"], p_negative=rd["p"], what="gamma3^H - gamma1^H")
    out["drop_condition"] = bool(rd["beta"] < 0 and r3["p"] >= DROP_SIG)
    g1, g3, g1h, g3h = (sl[k]["beta"] for k in ("g1", "g3", "g1H", "g3H"))
    out["scale_free_companion"] = dict(high=g3h / g1h if g1h else math.nan, low=g3 / g1 if g1 else math.nan,
                                       g1=sl["g1"], g1H=sl["g1H"],
                                       caveat="unstable where a bottom slope is near 0 (control eras, LR-RC)")
    return out


def country_fits(M: pd.DataFrame) -> dict:
    """Each country's own top-minus-bottom slope change (OLS on 1, P1-P3, U and its segment dummies; no inference)."""
    out = {}
    for c, e in M.groupby("geo"):
        e = e.copy()
        e.attrs = {"breaks": [b for b in M.attrs.get("breaks", []) if b[0] == c]}
        X = np.column_stack([np.ones(len(e)), e[["P1", "P2", "P3", "U"]].to_numpy(float),
                             break_dummies(e, e.attrs["breaks"])])
        try:
            b = np.linalg.lstsq(X, e["y"].to_numpy(float), rcond=None)[0]
            out[c] = dict(g1=float(b[1]), g3=float(b[3]), top_minus_bottom=float(b[3] - b[1]), n=int(len(e)))
        except np.linalg.LinAlgError:
            out[c] = dict(error="singular")
    return out


# ---------------------------------------------------------------- the linear tests

def _q(d):
    return d["logq_l1"].to_numpy(float)


def linear_frame(data: Data, test: str, geos, variant: str | None = None, post: bool = False) -> pd.DataFrame:
    """Rows of LR-Y0's companions and of the non-basis tests (C-6L, LR-C1, the no-verdict ones). post=True adds the
    post-freeze segments (the no-verdict run only)."""
    if test == "LR-C1":
        d = data.census.copy()
        if not len(d):
            return d
        d = d[d["geo"].isin(geos)]
        d = d[np.isfinite(d[["R", "x"]].to_numpy(float)).all(1)].reset_index(drop=True)
        br = set()
        for g, bl in zip(d["geo"], d.get("R__breaks", [[]] * len(d))):
            br.update((g, int(t)) for t in bl)
        qb = data.cy.reset_index()
        for g, bl in zip(qb["geo"], qb["logq_l1__breaks"]):
            if g in set(d["geo"]):
                br.update((g, int(t)) for t in bl)
        d["y"] = d["R"]
        if post:
            br |= set(_post_breaks(data, set(d["geo"]), ["R", "logq_l1"]))
        d.attrs["breaks"] = sorted(br)
        return d
    d = data.cy.reset_index()
    d = d[d["geo"].isin(geos)].copy()
    if test == "C-6L":
        need, vars_ = ["school2024", "U"], ["school2024", "U"]
        d["y"] = d["school2024"]
    elif test == "E-SCH1-L":
        d = d.sort_values(["geo", "year"])
        prev = d.set_index(["geo", "year"])["U"]
        d["U_l1"] = [prev.get((g, t - 1), np.nan) for g, t in zip(d["geo"], d["year"])]
        d["U_l1__breaks"] = [[b + 1 for b in bl] for bl in d["U__breaks"]]
        need, vars_ = ["school2024", "U_l1"], ["school2024", "U_l1"]
        d["y"] = d["school2024"]
    else:
        spec = NO_VERDICT[test]
        ovars = _outcome_vars(spec["outcome"])
        need = ovars + ["logq_l1"] + list(spec["controls"])
        vars_ = need
        d["y"] = _outcome(d, spec["outcome"])
    d = d[np.isfinite(d[need].to_numpy(float)).all(1)].reset_index(drop=True)
    sv = [{"U_l1": "U"}.get(v, v) for v in vars_]
    d.attrs["breaks"] = sorted(set(_breaks(d, vars_)) | (set(_post_breaks(data, set(d["geo"]), sv)) if post else set()))
    return d


def wcr_run(y, x, Z, g, side, B, seed, with_ci=False) -> dict:
    r = inf.wcr(y, x, Z, g, side=side, B=B, seed=seed)
    out = dict(beta=r["beta"], se=r["se"], t=r["t"], p=r["p"], p_opposite=r["p_opposite"], n=r["n"], G=r["G"],
               G_star=r["G_star"], mde=inf.mde(r["se"], r["G"]))
    if with_ci:
        out["ci"] = list(inf.ci(y, x, Z, g, side=0, B=B, seed=seed))
        out["ci_one_sided"] = list(inf.ci(y, x, Z, g, side=side, B=B, seed=seed)) if side else None
    return out


def simple_test(data: Data, test: str, geos, B=B_DEFAULT, seed=inf.SEED, with_ci=False, knot_key="q",
                qcol="logq_l1", outcome=None, rows=None, post: bool = False) -> dict:
    """LR-Y0, C-6L, LR-C1 (and their variants): one coefficient by WCR. A design that cannot be estimated (too few
    rows for its fixed effects, a collinear regressor, a missing column) is reported as an error."""
    try:
        return _simple_test(data, test, geos, B, seed, with_ci, knot_key, qcol, outcome, rows, post)
    except FIT_ERRORS as e:
        return dict(error=f"{type(e).__name__}: {e}"[:300])


def _simple_test(data, test, geos, B, seed, with_ci, knot_key, qcol, outcome, rows, post=False) -> dict:
    spec = TESTS[test]
    if test == "LR-Y0":
        M = basis_frame(data, geos, outcome or spec["outcome"], ("U",), knot_key, qcol, rows, post=post)
        if M.empty:
            return dict(error="no rows")
        Z = _Z(M, spec["fe"], ["U"], M[["P2", "P3"]].to_numpy(float))
        x = M["P1"].to_numpy(float)
    else:
        M = linear_frame(data, test, geos, post=post)
        if rows is not None and len(M):
            M = M[rows(M)].reset_index(drop=True)
        if M.empty or len(set(M["geo"])) < 2:
            return dict(error="no rows")
        if test == "LR-C1":
            x = M["x"].to_numpy(float) if qcol == "logq_l1" else M[qcol].to_numpy(float)
            Z = _Z(M, ["geo", "round"], [])
        else:
            x = M["U"].to_numpy(float)
            Z = _Z(M, spec["fe"], [])
    r = wcr_run(M["y"].to_numpy(float), x, Z, M["geo"].to_numpy(), spec["side"], B, seed, with_ci)
    r.update(geos_used=sorted(set(M["geo"])), years_used=sorted(int(t) for t in set(M["year"])),
             n_segment_dummies=int(break_dummies(M, M.attrs.get("breaks", [])).shape[1]))
    r["p_stat"], r["p_stat_opposite"] = r["p"], r["p_opposite"]
    return r


def no_verdict(data: Data, test: str, geos, F: dict | None = None, strata: dict | None = None, B=B_DEFAULT,
               R=9999, seed=inf.SEED) -> dict:
    """D1-L, D2-L, C-2L, C-3L, E-SCH1-L: estimates and p in both directions, no verdict. A degenerate design is
    reported as an error, never stops the run."""
    try:
        return _no_verdict(data, test, geos, F, strata, B, R, seed)
    except (ValueError, ZeroDivisionError, np.linalg.LinAlgError, KeyError) as e:
        return dict(error=f"{type(e).__name__}: {e}"[:300])


def _no_verdict(data, test, geos, F, strata, B, R, seed) -> dict:
    spec = NO_VERDICT[test]
    M = linear_frame(data, test, geos)
    if M.empty or len(set(M["geo"])) < 3:
        return dict(error="no rows")
    g = M["geo"].to_numpy()
    if test == "E-SCH1-L":
        r = wcr_run(M["y"].to_numpy(float), M["U_l1"].to_numpy(float), _Z(M, ["geo", "year"], []), g, 1, B, seed)
        return {**r, "geos_used": sorted(set(g))}
    q = _q(M)
    if test == "D1-L":
        Fs = {c: F[c] for c in set(g) if F and c in F and np.isfinite(F[c])}
        M = M[M["geo"].isin(list(Fs))].reset_index(drop=True)
        M.attrs["breaks"] = [b for b in _breaks(M, ["A2534", "logq_l1", "U"])]
        vals = np.array(list(Fs.values()))
        mu, sd = vals.mean(), vals.std(ddof=0)
        Fz = {c: (v - mu) / sd for c, v in Fs.items()}
        q = _q(M)
        f = M["geo"].map(Fz).to_numpy(float)
        Z = _Z(M, ["geo", "year"], ["U"], q[:, None])
        g = M["geo"].to_numpy()
        r = wcr_run(M["y"].to_numpy(float), q * f, Z, g, -1, B, seed)
        p75 = float(np.percentile(list(Fz.values()), 75))
        Z2 = _Z(M, ["geo", "year"], ["U"], (q * (f - p75))[:, None])
        top = wcr_run(M["y"].to_numpy(float), q, Z2, g, 0, B, seed)
        rr = {}
        if strata:
            for side in (-1, 1):
                rr[side] = inf.ri(M["y"].to_numpy(float), pd.Series(Fz), g, pd.Series(strata), Z, side=side, R=R,
                                  seed=seed, x_mult=q)["p"]
        return {**r, "p_ri_negative": rr.get(-1), "p_ri_positive": rr.get(1), "slope_at_F75": top["beta"],
                "slope_at_F75_se": top["se"], "geos_used": sorted(set(g))}
    if test == "D2-L":
        segc = M["qseg_l1"].to_numpy(float)
        key = pd.Series(list(zip(M["geo"], segc)))
        m = pd.Series(q).groupby(key).transform("mean").to_numpy(float)
        Z = _Z(M, ["geo", "year"], ["U"], q[:, None])
        r = wcr_run(M["y"].to_numpy(float), (q - m) ** 2, Z, g, -1, B, seed)
        return {**r, "geos_used": sorted(set(g))}
    Z = _Z(M, ["geo", "year"], list(spec["controls"]))
    r = wcr_run(M["y"].to_numpy(float), q, Z, g, 0, B, seed)
    rp = wcr_run(M["y"].to_numpy(float), q, Z, g, 1, B, seed)
    return {**r, "p_positive": rp["p"], "p_negative": rp["p_opposite"], "geos_used": sorted(set(g))}


# ---------------------------------------------------------------- calibration and verdicts

def calibrated(test: str, p: float, direction: str, calibration: dict | None) -> tuple[float, str]:
    """(verdict p, status): max(raw p, the share of null replications whose statistic is <= p, at the rho with the
    larger share). direction: 'pred' or 'opp'."""
    if not calibration or test not in calibration:
        return p, "uncalibrated"
    shares = []
    for rho, tab in calibration[test].items():
        arr = np.asarray(tab[direction], float)
        if len(arr):
            shares.append(float(np.mean(arr <= p + 1e-12)))
    if not shares:
        return p, "uncalibrated"
    return max(p, max(shares)), "calibrated"


def verdict_p(test: str, res: dict, calibration) -> dict:
    p, s1 = calibrated(test, res["p_stat"], "pred", calibration)
    po, s2 = calibrated(test, res["p_stat_opposite"], "opp", calibration)
    return dict(p=p, p_opposite=po, calibration=s1 if s1 == s2 else f"{s1}/{s2}")


def labels_for(results: dict, calibration, families: dict | None = None) -> tuple[dict, dict]:
    """Holm within each family on the verdict p's: (labels, the p's used). families: frozen at L2 (default: the
    protocol's). A frozen member that errored, or whose verdict statistic is not finite, takes p = 1 both ways inside
    its family; LR-K2 not testable at the look has no label (the model-level verdict is then 'not testable')."""
    used, labels = {}, {}
    for fam, ids in (families or FAMILIES).items():
        fam_res = {}
        for k in ids:
            r = results.get(k)
            if r is not None and r.get("testable", True) is False:
                continue
            if (r is None or "error" in r or not np.isfinite(r.get("p_stat", math.nan))
                    or not np.isfinite(r.get("p_stat_opposite", math.nan))):
                why = (r or {}).get("error") or (r or {}).get("ri_error") or "no result"
                vp = dict(p=1.0, p_opposite=1.0, calibration=f"error ({why}): p = 1 inside its frozen family")
            else:
                vp = verdict_p(k, r, calibration)
            used[k] = vp
            fam_res[k] = vp
        if fam_res:
            labels.update(holm(fam_res))
    return labels, used


def own_p(label: str, vp: dict) -> float | None:
    return {"supported": vp["p"], "contradicted": vp["p_opposite"]}.get(label)


def qualifier_fires(label: str, base_beta: float, run: dict, test: str, calibration) -> bool:
    """A qualifier run fires when it flips the estimate's sign or pushes the own-direction verdict p above 0.10."""
    if "error" in run or not np.isfinite(run.get("p_stat", math.nan)):
        return False
    vp = verdict_p(test, run, calibration)
    p = own_p(label, vp)
    return bool(p is not None and (np.sign(run["beta"]) != np.sign(base_beta) or p > LOO_P))


def model_verdict(k2_label: str | None, drop: bool | None, testable: bool) -> str:
    if not testable or k2_label is None:
        return MODEL_READINGS["not testable"]
    if k2_label == "supported":
        return MODEL_READINGS["favours"] if drop else MODEL_READINGS["consistent"]
    if k2_label == "contradicted":
        return MODEL_READINGS["against"]
    return MODEL_READINGS["inconclusive"]


def reading(label: str, test: str, std_mde: float | None, bench: float | None, y0_note: str | None = None) -> str:
    """The reading table of section 5."""
    if label in ("supported", "contradicted"):
        return READING[label]
    if test == "LR-Y0" and y0_note:
        return y0_note
    if std_mde is None or bench is None or not np.isfinite(std_mde) or not np.isfinite(bench):
        return "uninformative (no pre-look MDE)"
    return READING["inconclusive_at_or_below"] if std_mde <= bench else READING["inconclusive_above"]


def y0_reading_note(strict_run: dict | None, calibration, std_mde: float | None, bench: float | None) -> str:
    """Section 5's reading note for an inconclusive LR-Y0."""
    if not strict_run or "error" in strict_run:
        return "uninformative"
    vp = verdict_p("LR-Y0", strict_run, calibration)
    if vp["p"] < ALPHA:
        return "consistent with LR-RC attenuation"
    if std_mde is not None and bench is not None and std_mde <= bench:
        return "no support"
    return "uninformative"


def joint_reading(europe: dict, model: str) -> str:
    """Section 5's two-study table, rows in order."""
    eu = [europe.get("D1"), europe.get("D2")]
    if "contradicted" in eu:
        return "against the floor mechanism"
    if model == MODEL_READINGS["against"]:
        return ("against the floor mechanism together with its long-run regime placement and auxiliaries 1-3")
    if model == MODEL_READINGS["favours"]:
        return ("supported in the long run (against the no-coresidence and attenuation accounts only), not in "
                "2009-2025 Europe")
    if model == MODEL_READINGS["consistent"]:
        return ("consistent with the floor mechanism in the long run but not told apart from attenuation; not "
                "supported in 2009-2025 Europe")
    return "inconclusive"


def europe_labels() -> dict:
    try:
        return json.load(open(EUROPE_LOOK, encoding="utf-8"))["primary"]["verdicts"]
    except (OSError, KeyError, ValueError):
        return {}


# ---------------------------------------------------------------- LR-K2 qualifiers and placebo

def k2_loo(M, H, B, R, seed, calibration, label) -> dict:
    """Every country's leave-one-out run (H held fixed), the worst own-direction p and the US row by name."""
    worst = {"p": (-1.0, None), "p_opposite": (-1.0, None)}
    per = {}
    for c in sorted(set(M["geo"])):
        Hc = {k: v for k, v in H.items() if k != c}
        if sum(Hc.values()) < 2 or len(Hc) - sum(Hc.values()) < 2:
            per[c] = "not estimable"
            continue
        r = k2_safe(M[M["geo"] != c].reset_index(drop=True).pipe(_keep_attrs, M), Hc, B, R, seed)
        if "error" in r or not np.isfinite(r.get("p_stat", math.nan)):
            per[c] = r.get("error") or r.get("ri_error") or "not finite"
            continue
        vp = verdict_p("LR-K2", r, calibration)
        per[c] = dict(beta=r["beta"], p=vp["p"], p_opposite=vp["p_opposite"])
        for k in worst:
            if vp[k] > worst[k][0]:
                worst[k] = (vp[k], c)
    return dict(per_country=per, max_p=worst["p"][0], max_p_left_out=worst["p"][1],
                max_p_opposite=worst["p_opposite"][0], max_p_opposite_left_out=worst["p_opposite"][1],
                without_US=per.get("US"))


US_TEXT = "rests on the US, a partly seen country"


def us_crosses(label: str, base_beta: float, us_row) -> bool:
    """L13: the US row alone pushes the own-direction p above 0.10 (or flips the sign)."""
    key = {"supported": "p", "contradicted": "p_opposite"}.get(label)
    if not key or not isinstance(us_row, dict):
        return False
    return bool(us_row[key] > LOO_P or np.sign(us_row["beta"]) != np.sign(base_beta))


def _keep_attrs(df, src):
    df.attrs = dict(src.attrs)
    return df


def group_year_dummies(M: pd.DataFrame, H: dict) -> np.ndarray:
    """H x year dummies, dropped by rule in years with only one floor group observed (collinear with year effects)."""
    h = M["geo"].map(H).to_numpy(float)
    cols = []
    for t in sorted(set(M["year"])):
        m = (M["year"] == t).to_numpy()
        if len(set(h[m])) == 2:
            cols.append(h * m)
    return np.column_stack(cols) if cols else np.zeros((len(M), 0))


def time_tercile_t(M: pd.DataFrame, H: dict, knots_q: dict, qcol: str = "logq_l1") -> float:
    """The curvature qualifier's time-tercile run: x x 1[calendar tercile j] by floor group, country x tercile effects;
    the DiD t (CR1). The calendar terciles come from each country's ranking set (knots_q[c]['years'], from q alone):
    rank r of n in calendar order falls in tercile ceil(3r/n), before any outcome filter; each row takes its year's."""
    M = M.copy()
    pos = {}
    for c in set(M["geo"]):
        yrs = sorted(int(t) for t in knots_q[c]["years"])
        n = len(yrs)
        pos.update({(c, t): math.ceil(3 * (r + 1) / n) for r, t in enumerate(yrs)})
    terc = np.array([pos[(g, int(t))] for g, t in zip(M["geo"], M["year"])], int)
    x = M[qcol].to_numpy(float)
    h = M["geo"].map(H).to_numpy(float)
    X6 = np.column_stack([x * (terc == j) * (1 - h) for j in (1, 2, 3)] + [x * (terc == j) * h for j in (1, 2, 3)])
    M["geo_terc"] = M["geo"].astype(str) + "_" + terc.astype(str)
    Z = np.column_stack([inf.fe_matrix(M, ["geo_terc", "year"]), M[["U"]].to_numpy(float),
                         break_dummies(M, M.attrs.get("breaks", []))])
    xx, Zr = infl.contrast(X6, DID)
    f = inf._Fit(M["y"].to_numpy(float), xx, np.column_stack([Z, Zr]), M["geo"].to_numpy())
    return f.beta / f.se


def k2_t_only(M, H) -> float:
    X6 = _k2_X(M, H)
    x, Zr = infl.contrast(X6, DID)
    f = inf._Fit(M["y"].to_numpy(float), x, np.column_stack([_Z(M, ["geo", "year"], ["U"]), Zr]),
                 M["geo"].to_numpy())
    return f.beta / f.se


def derangement(rng, n: int) -> np.ndarray:
    while True:
        p = rng.permutation(n)
        if not np.any(p == np.arange(n)):
            return p


def d2_t(M: pd.DataFrame) -> float:
    """D2-L's t on a frame: A2534 on x and (x - m_c)^2, m_c the mean of x within country (the placebo's ranking sets
    lie in one q segment), FE, U and the frame's segment dummies."""
    q = M["logq_l1"].to_numpy(float)
    m = M.groupby("geo")["logq_l1"].transform("mean").to_numpy(float)
    Z = _Z(M, ["geo", "year"], ["U"], q[:, None])
    f = inf._Fit(M["y"].to_numpy(float), (q - m) ** 2, Z, M["geo"].to_numpy())
    return f.beta / f.se


def placebo_ts(data: Data, geos, H: dict | None, stat, draws: int = PLACEBO_DRAWS, seed: int = inf.SEED,
               outcome: str = "A2534") -> np.ndarray:
    """Series-permutation placebo: each country gets another country's x path over its ranking set (aligned at the
    start; years beyond the donor's length dropped); knots recomputed from the donor path; stat(M) per draw."""
    kn = data.knots["q"]
    cs = [c for c in sorted(geos) if kn.get(c, {}).get("k1") is not None]
    cy = data.cy.reset_index()
    paths = {c: cy[(cy["geo"] == c) & cy["year"].isin(kn[c]["years"])].sort_values("year")["logq_l1"]
             .to_numpy(float) for c in cs}
    rng = np.random.default_rng(seed)
    out = []
    if len(cs) < 2:                                   # no derangement exists
        return np.asarray(out, float)
    for _ in range(draws):
        perm = derangement(rng, len(cs))
        parts = []
        for i, c in enumerate(cs):
            donor = paths[cs[perm[i]]]
            yrs = sorted(kn[c]["years"])[: len(donor)]
            e = cy[(cy["geo"] == c) & cy["year"].isin(yrs)].sort_values("year").copy()
            e["logq_l1"] = donor[: len(e)]
            n = len(e)
            if n < MIN_RANKED:
                continue
            order = sorted(range(n), key=lambda j: (e["logq_l1"].iloc[j], e["year"].iloc[j]))
            terc = np.empty(n, int)
            for r, j in enumerate(order):
                terc[j] = math.ceil(3 * (r + 1) / n)
            xs = e["logq_l1"].to_numpy(float)
            k1 = 0.5 * (xs[terc == 1].max() + xs[terc == 2].min())
            k2 = 0.5 * (xs[terc == 2].max() + xs[terc == 3].min())
            P = basis(xs, k1, k2)
            e["P1"], e["P2"], e["P3"] = P[:, 0], P[:, 1], P[:, 2]
            parts.append(e)
        if not parts:
            continue
        M = pd.concat(parts, ignore_index=True)
        M["y"] = _outcome(M, outcome)
        M = M[np.isfinite(M[["y", "U", "logq_l1"]].to_numpy(float)).all(1)].reset_index(drop=True)
        M.attrs["breaks"] = _breaks(M, [outcome, "U"])
        try:
            out.append(stat(M))
        except FIT_ERRORS:
            continue
    return np.asarray(out, float)


def k2_qualifiers(data: Data, M: pd.DataFrame, H: dict, base: dict, label: str, B, R, seed, calibration) -> dict:
    """The five mechanical qualifiers of LR-K2 (section 5), each with its run and whether it fires. Each run is
    guarded on its own (an inestimable run is reported as its error and does not fire)."""
    out = {}
    loo = k2_loo(M, H, B, R, seed, calibration, label)
    key = {"supported": "max_p", "contradicted": "max_p_opposite"}.get(label)
    fires = bool(key and loo[key] > LOO_P)
    who = loo.get(key + "_left_out") if key else None
    text = (US_TEXT if who == "US" else f"rests on one country ({who})") if fires else ""
    flip = [c for c, v in loo["per_country"].items() if isinstance(v, dict) and np.sign(v["beta"]) != np.sign(base["beta"])]
    if key and flip and not fires:
        fires, text = True, (US_TEXT if flip[0] == "US" else f"rests on one country ({flip[0]})")
    if us_crosses(label, base["beta"], loo["per_country"].get("US")) and US_TEXT not in text:
        fires, text = True, "; ".join(t for t in (text, US_TEXT) if t)
    out["rests on one country"] = dict(run=loo, fires=fires, text=text)
    # floor-group trends: H x year effects (rebuilt for every H assignment of the RI)
    r = k2_safe(M, H, B, R, seed, z_of_H=group_year_dummies)
    out["rests on floor-group trends"] = dict(run=_brief(r), fires=qualifier_fires(label, base["beta"], r, "LR-K2",
                                                                                    calibration))
    # cohort size
    if "cohort" in M and np.isfinite(M["cohort"].to_numpy(float)).all():
        r = k2_safe(M, H, B, R, seed, controls=("U", "cohort"))
        out["rests on cohort size"] = dict(run=_brief(r), fires=qualifier_fires(label, base["beta"], r, "LR-K2",
                                                                                 calibration))
    else:
        out["rests on cohort size"] = dict(run=None, fires=False, text="not run: relative cohort size missing")
    # control-era years
    if "strict" in M and M["strict"].notna().any():
        Ms = M[M["strict"] != 1].reset_index(drop=True).pipe(_keep_attrs, M)
        r = k2_safe(Ms, H, B, R, seed)
        out["rests on control-era years"] = dict(run={**_brief(r), "n_strict_dropped": int((M["strict"] == 1).sum())},
                                                 fires=qualifier_fires(label, base["beta"], r, "LR-K2", calibration))
    else:
        out["rests on control-era years"] = dict(run=None, fires=False,
                                                 text="not run: control-era years not separable (no Kholodilin coding)")
    # time curvature: time terciles and the series-permutation placebo
    t_prim = base["t"]
    try:
        t_time = time_tercile_t(M, H, data.knots["q"])
    except FIT_ERRORS:
        t_time = math.nan
    pl = placebo_ts(data, list(H), H, lambda m: k2_t_only(m, H), seed=seed)
    lo, hi = (np.percentile(pl, [10, 90]) if len(pl) else (math.nan, math.nan))
    inside = bool(len(pl) and lo <= t_prim <= hi)
    tt_fire = bool(np.isfinite(t_time) and t_time <= t_prim)       # predicted direction is negative
    out["indistinguishable from time curvature"] = dict(
        run=dict(t_primary=t_prim, t_time_terciles=t_time, placebo_central80=[float(lo), float(hi)],
                 placebo_draws=int(len(pl))), fires=bool(tt_fire or inside))
    for k, v in out.items():
        if "text" not in v:
            v["text"] = k if v["fires"] else ""
    return out


def _brief(r: dict) -> dict:
    return {k: r.get(k) for k in ("beta", "se", "t", "p_wcr", "p_wcr_opposite", "p_ri", "p_ri_opposite", "p_stat",
                                  "p_stat_opposite", "G", "n", "error", "ri_error", "n_nonfinite") if k in r}


def leave_one_out(data: Data, test: str, geos, B, seed, calibration) -> dict:
    """Every country's leave-one-out run of a C-L test, the worst own-direction p, and the US row by name."""
    full = simple_test(data, test, geos, B=B, seed=seed)
    used = full.get("geos_used", [])
    worst = {"p": (-1.0, None), "p_opposite": (-1.0, None)}
    per = {}
    for c in used:
        r = simple_test(data, test, [g for g in geos if g != c], B=B, seed=seed)
        if "error" in r:
            per[c] = r["error"]
            continue
        vp = verdict_p(test, r, calibration)
        per[c] = dict(beta=r["beta"], p=vp["p"], p_opposite=vp["p_opposite"])
        for k in worst:
            if vp[k] > worst[k][0]:
                worst[k] = (vp[k], c)
    return dict(max_p=worst["p"][0], max_p_left_out=worst["p"][1], max_p_opposite=worst["p_opposite"][0],
                max_p_opposite_left_out=worst["p_opposite"][1], n_left_out=len(used), per_country=per,
                without_US=per.get("US"), base_beta=full.get("beta"))


def us_wording(q: str) -> str:
    return US_TEXT if q == "rests on one country (US)" else q


def cl_qualifier(label: str, loo: dict) -> str:
    """The frozen leave-one-out qualifier with the US wording, plus the US sentence whenever the US row alone crosses
    0.10 (L13)."""
    q = us_wording(frozen_qualify({"t": label}, {"t": loo})["t"])
    if loo.get("base_beta") is not None and us_crosses(label, loo["base_beta"], loo.get("without_US")) \
            and US_TEXT not in q:
        q = "; ".join(t for t in (q, US_TEXT) if t)
    return q


# ---------------------------------------------------------------- robustness

def robustness(data: Data, H: dict, members: dict, B, R, seed) -> dict:
    """The ten robustness runs (no verdict). Each run is guarded on its own: a run that cannot be estimated (or a
    missing column) is reported as that run's error and the others still run."""
    out = {}
    cl = data.cl
    k2 = sorted(H)

    def row(name, fn):
        try:
            out[name] = fn()
        except FIT_ERRORS as e:
            out[name] = dict(error=f"{type(e).__name__}: {e}"[:300])

    def k2run(Hr, outcome="A2534", knot_key="q", qcol="logq_l1", rows=None, ri=True, post=False):
        M = basis_frame(data, sorted(Hr), outcome, ("U",), knot_key, qcol, rows, post=post)
        if M.empty:
            return dict(error="no rows")
        return _brief(k2_safe(M, Hr, B, R, seed, with_ri=ri))

    def split_by(col, countries):
        F = {c: float(cl.loc[c, col]) for c in countries if c in cl.index and np.isfinite(cl.loc[c, col])}
        return compute_H(F, list(F))

    # 1. Giuliano-Nunn F, all countries with q (the Y0 membership is the set with q and the outcome); its own split
    gn_c = [c for c in members.get("Y0", []) if c in cl.index and np.isfinite(cl.loc[c, "GN"])] if "GN" in cl else []
    row("giuliano_nunn.LR-K2", lambda: k2run(split_by("GN", gn_c)) if len(gn_c) >= 8
        else dict(error="no Giuliano-Nunn F"))
    row("giuliano_nunn.D1-L", lambda: no_verdict(data, "D1-L", gn_c, F={c: float(cl.loc[c, "GN"]) for c in gn_c}, B=B,
                                                 R=R, seed=seed) if len(gn_c) >= 3 else dict(error="no Giuliano-Nunn F"))
    # 2. ages 20-29 (its own split)
    row("F_L_2029.LR-K2", lambda: k2run(split_by("F_L_2029", k2)))

    # 3. standardised F_L, continuous: slopes P_j and F*P_j; tested (g3F - g1F) < 0
    def cont():
        M = basis_frame(data, k2, "A2534")
        if M.empty:
            return dict(error="no rows")
        F = {c: float(cl.loc[c, "F_L"]) for c in k2}
        v = np.array(list(F.values()))
        f = M["geo"].map({c: (x - v.mean()) / v.std(ddof=0) for c, x in F.items()}).to_numpy(float)
        P = M[["P1", "P2", "P3"]].to_numpy(float)
        X6 = np.column_stack([P, f[:, None] * P])
        x, Zr = infl.contrast(X6, (0, 0, 0, -1, 0, 1))
        return wcr_run(M["y"].to_numpy(float), x, np.column_stack([_Z(M, ["geo", "year"], ["U"]), Zr]),
                       M["geo"].to_numpy(), -1, B, seed)
    row("F_L_continuous.LR-K2", cont)
    # 4-5. by sex (H held fixed)
    for sex, col in (("men_only", "A2534_M"), ("women_only", "A2534_F")):
        row(f"{sex}.LR-K2", lambda col=col: k2run(H, outcome=col))
        row(f"{sex}.LR-Y0", lambda col=col: simple_test(data, "LR-Y0", members.get("Y0", []), B=B, seed=seed,
                                                        outcome=col))
    # 6. strict control dropped (Kholodilin first-generation years; uncovered countries keep all their years)
    if "strict" in data.cy and data.cy["strict"].notna().any():
        keep = (lambda e: e["strict"] != 1)
        row("strict_control_dropped.LR-K2", lambda: k2run(H, rows=keep))
        row("strict_control_dropped.LR-Y0", lambda: simple_test(data, "LR-Y0", members.get("Y0", []), B=B, seed=seed,
                                                                rows=keep))
        row("strict_control_dropped.LR-C1", lambda: simple_test(data, "LR-C1", members.get("C1", []), B=B, seed=seed,
                                                                rows=keep) if len(data.census)
            else dict(error="no Extract B"))
    else:
        for t in ROBUSTNESS["strict_control_dropped"]:
            out[f"strict_control_dropped.{t}"] = dict(error="control-era years not separable (no Kholodilin coding)")
    out["strict_control_dropped.uncovered_countries"] = data.kh_uncovered
    # 7. q_hpi (knots from q_hpi alone, recorded at the opening)
    if data.knots.get("q_hpi"):
        row("q_hpi.LR-K2", lambda: k2run(H, knot_key="q_hpi", qcol="logq_hpi_l1"))
        row("q_hpi.LR-Y0", lambda: simple_test(data, "LR-Y0", members.get("Y0", []), B=B, seed=seed, knot_key="q_hpi",
                                               qcol="logq_hpi_l1"))
    else:
        out["q_hpi.LR-K2"] = out["q_hpi.LR-Y0"] = dict(error="no q_hpi knots")
    row("q_hpi.LR-C1", lambda: simple_test(data, "LR-C1", members.get("C1", []), B=B, seed=seed, qcol="x_hpi")
        if len(data.census) and "x_hpi" in data.census else dict(error="no Extract B or no q_hpi"))

    # 8. F_L nearest 1970, later years only (its own split)
    def f70():
        H70 = split_by("F_L_1970", k2)
        yr = {c: cl.loc[c, "F_L_1970_year"] for c in k2 if c in cl.index}
        later = (lambda e: e["year"] > e["geo"].map(yr).astype(float))
        return k2run(H70, rows=later) if len(H70) >= 4 else dict(error="too few")
    row("F_L_1970_later_years.LR-K2", f70)

    def f70d():
        F70 = {c: float(cl.loc[c, "F_L_1970"]) for c in k2 if c in cl.index and np.isfinite(cl.loc[c, "F_L_1970"])}
        return no_verdict(data, "D1-L", list(F70), F=F70, B=B, R=R, seed=seed)
    row("F_L_1970_later_years.D1-L", f70d)

    # 9. flagged samples dropped (H held fixed)
    def flagged_k2():
        keep = [c for c in k2 if not bool(cl.loc[c, "F_L_flagged"])]
        Hk = {c: H[c] for c in keep}
        return (k2run(Hk) if sum(Hk.values()) >= 2 and len(Hk) - sum(Hk.values()) >= 2
                else dict(error="a floor group falls below 2 countries"))
    row("flagged_samples_dropped.LR-K2", flagged_k2)

    def flagged_d1():
        keep = [c for c in k2 if not bool(cl.loc[c, "F_L_flagged"])]
        return no_verdict(data, "D1-L", keep, F={c: float(cl.loc[c, "F_L"]) for c in keep}, B=B, R=R, seed=seed)
    row("flagged_samples_dropped.D1-L", flagged_d1)
    # 10. post-freeze segments (run only if such segments exist; data.post_seg, never in a primary frame)
    if data.post_seg is not None and len(data.post_seg):
        for t in ROBUSTNESS["post_freeze_segments"]:
            key = TESTS[t]["members"]
            row(f"post_freeze_segments.{t}", lambda t=t, key=key: (
                k2run(H, post=True) if t == "LR-K2" else
                simple_test(data, t, members.get(key, []), B=B, seed=seed, post=True)
                if (t != "LR-C1" or len(data.census)) else dict(error="no Extract B")))
    return out


# ---------------------------------------------------------------- run

def pooled_d1(eu_look: dict | None, d1l: dict) -> dict:
    """Section 5 'Two studies, two verdicts': the inverse-variance pooled b2 of the European D1 and D1-L (no verdict)."""
    try:
        eu = eu_look["primary"]["tests"]["D1"]
        pairs = [(float(eu["beta"]), float(eu["se"])), (float(d1l["beta"]), float(d1l["se"]))]
    except (KeyError, TypeError, ValueError):
        return dict(error="the European D1 or D1-L estimate is missing")
    if not all(np.isfinite(b) and np.isfinite(s_) and s_ > 0 for b, s_ in pairs):
        return dict(error="a non-finite estimate")
    w = np.array([1 / s_ ** 2 for _, s_ in pairs])
    b = np.array([b for b, _ in pairs])
    return dict(beta=float(w @ b / w.sum()), se=float(1 / math.sqrt(w.sum())), europe=pairs[0], long_run=pairs[1],
                what="inverse-variance pooled b2 of the European D1 and D1-L; no verdict, no combination test")


def europe_look() -> dict | None:
    try:
        return json.load(open(EUROPE_LOOK, encoding="utf-8"))
    except (OSError, ValueError):
        return None


def blind(data: Data, seed: int) -> Data:
    """PROTOCOL section 8: a blinded debugging panel. Each country's q path (logq_l1 over its observation years) is
    given to another country by a derangement drawn from a seed the debugger does not look at; the knots are recomputed
    from the permuted paths by the frozen rule. For debugging before the look only; never for a reported result."""
    cy = data.cy.copy()
    geos = sorted(set(cy.index.get_level_values(0)))
    rng = np.random.default_rng(seed)
    perm = derangement(rng, len(geos)) if len(geos) > 1 else np.arange(len(geos))
    paths = {c: cy.xs(c, level=0)["logq_l1"].to_numpy(float) for c in geos}
    segs = {c: cy.xs(c, level=0)["qseg_l1"].to_numpy(float) for c in geos}
    for i, c in enumerate(geos):
        d = geos[perm[i]]
        n = len(paths[c])
        src, sg_ = paths[d], segs[d]
        cy.loc[c, "logq_l1"] = np.concatenate([src[:n], np.full(max(0, n - len(src)), np.nan)])
        cy.loc[c, "qseg_l1"] = np.concatenate([sg_[:n], np.full(max(0, n - len(sg_)), np.nan)])
    chosen = {}
    for c in geos:
        q = cy.xs(c, level=0)
        yrs = [int(t) for t, v in zip(q.index, q["logq_l1"]) if np.isfinite(v)]
        if yrs:
            chosen[c] = (min(yrs) - 1, max(yrs) - 1)
    kn = knots(cy[["logq_l1", "qseg_l1"]], chosen)
    return Data(cy, data.cl, {"q": kn}, data.H, data.members, data.census, data.calibration, data.post_seg,
                data.families, data.kh_uncovered)


def run(data: Data, B: int = B_DEFAULT, R: int = 9999, seed: int = inf.SEED, with_ci: bool = True,
        qualifiers: bool = True, robust: bool = True, extract_b: bool = True, std_mde: dict | None = None,
        bench: dict | None = None, replication: bool = False) -> dict:
    """Every test of section 5 on these data, with verdicts. data.H must already be computed (once, at the look).
    replication=True: the confirm-half replication (labels for information only; LR-K2 is reported whenever each
    floor group has at least 2 countries, without the primary's testability gate)."""
    cal = data.calibration
    mem = data.members
    H = dict(data.H)
    fams = data.families or FAMILIES
    if not extract_b:
        fams = {k: [t for t in v if t != "LR-C1"] for k, v in fams.items()}
    tests = {}
    testable_k2, why = k2_testable(H)
    M = basis_frame(data, sorted(H), "A2534") if H else pd.DataFrame()
    n_hi = sum(H.values())
    k2_ok = testable_k2 or (replication and n_hi >= 2 and len(H) - n_hi >= 2)
    if k2_ok and not M.empty:
        k = k2_safe(M, H, B, R, seed, with_ci=with_ci)
        tests["LR-K2"] = {"id": "LR-K2", **k, "testable": True, "H": H,
                          "country_fits": country_fits(M) if "error" not in k else None}
        if replication:
            tests["LR-K2"]["information_only"] = (
                "the confirm half fails the frozen testability rule; reported for information only (section 3)"
                if not testable_k2 else "replication: labels for information only")
    else:
        tests["LR-K2"] = {"id": "LR-K2", "testable": False, "error": why or "no rows", "H": H}
    tests["LR-Y0"] = {"id": "LR-Y0", **simple_test(data, "LR-Y0", mem.get("Y0", []), B=B, seed=seed, with_ci=with_ci)}
    tests["C-6L"] = {"id": "C-6L", **simple_test(data, "C-6L", mem.get("C6L", []), B=B, seed=seed, with_ci=with_ci)}
    if extract_b and len(data.census):
        tests["LR-C1"] = {"id": "LR-C1", **simple_test(data, "LR-C1", mem.get("C1", []), B=B, seed=seed,
                                                       with_ci=with_ci)}
    for k, v in tests.items():
        v["verdict_eligible"] = not replication
        v["what"] = TESTS[k]["what"]
        v["side"] = TESTS[k]["side"]
    labels, used = labels_for(tests, cal, fams)
    quals = {}
    if qualifiers:
        if "LR-K2" in labels and "error" not in tests["LR-K2"]:
            kq = k2_qualifiers(data, M, H, tests["LR-K2"], labels["LR-K2"], B, R, seed, cal)
            tests["LR-K2"]["qualifier_runs"] = kq
            quals["LR-K2"] = "; ".join(v["text"] for v in kq.values()
                                        if v["fires"] and labels["LR-K2"] in ("supported", "contradicted"))
        for t in ("LR-Y0", "C-6L", "LR-C1"):
            if t in labels and t in tests and "error" not in tests[t]:
                loo = leave_one_out(data, t, mem.get(TESTS[t]["members"], []), B, seed, cal)
                tests[t]["leave_one_out"] = loo
                quals[t] = cl_qualifier(labels[t], loo)
    drop = tests["LR-K2"].get("drop_condition")
    model = model_verdict(labels.get("LR-K2"), drop, tests["LR-K2"].get("testable", False))
    sentence = model
    if labels.get("LR-K2") == "supported":
        sentence += ". " + KAPLAN_SENTENCE
    if labels.get("LR-C1") == "contradicted":
        sentence += ". LR-C1 (coresidence on q, where parents own outright, if they do): contradicted"
    eu = europe_labels()
    readings = {}
    for t, lab in labels.items():
        sm = (std_mde or {}).get(t)
        bm = (bench or {}).get(t)
        note = None
        if t == "LR-Y0" and lab == "inconclusive":
            note = y0_reading_note(None, cal, sm, bm)
        readings[t] = reading(lab, t, sm, bm, note)
    out = dict(tests=tests, verdicts=labels, verdict_p=used, qualifiers=quals, model_verdict=model,
               model_sentence=sentence, model_qualifier=quals.get("LR-K2", ""), joint_reading=joint_reading(eu, model),
               europe_labels=eu, readings=readings, B=B, R=R, seed=seed,
               families={k: [t for t in v if t in labels] for k, v in fams.items()},
               families_frozen=fams, kholodilin_uncovered=data.kh_uncovered)
    nv = {}
    F = {c: float(data.cl.loc[c, "F_L"]) for c in data.cl.index if np.isfinite(data.cl.loc[c, "F_L"])} \
        if "F_L" in data.cl else {}
    strata = {c: fetch.stratum_of(c) for c in data.cl.index}
    geos_all = sorted(set(data.cy.index.get_level_values(0)))
    nv["D1-L"] = no_verdict(data, "D1-L", sorted(F), F=F, strata=strata, B=B, R=R, seed=seed)
    d2 = no_verdict(data, "D2-L", mem.get("Y0", geos_all), B=B, R=R, seed=seed)
    if "error" not in d2 and not replication:          # section 5: the series-permutation placebo applied to D2-L's t
        try:
            pl = placebo_ts(data, mem.get("Y0", geos_all), None, d2_t, seed=seed)
            lo, hi = (np.percentile(pl, [10, 90]) if len(pl) else (math.nan, math.nan))
            d2["placebo"] = dict(central80=[float(lo), float(hi)], draws=int(len(pl)), t_observed=d2.get("t"),
                                 inside_central80=bool(len(pl) and lo <= d2["t"] <= hi),
                                 share_at_or_below_observed=float(np.mean(pl <= d2["t"])) if len(pl) else None,
                                 note="donor paths on each country's ranking set; m_c recomputed from the donor path")
        except FIT_ERRORS as e:
            d2["placebo"] = dict(error=f"{type(e).__name__}: {e}"[:300])
    nv["D2-L"] = d2
    for t in ("C-2L", "C-3L.diff", "C-3L.women"):
        nv[t] = no_verdict(data, t, geos_all, B=B, R=R, seed=seed)
    nv["E-SCH1-L"] = no_verdict(data, "E-SCH1-L", mem.get("C6L", []), B=B, R=R, seed=seed)
    if not replication:
        nv["pooled_D1_two_studies"] = pooled_d1(europe_look(), nv["D1-L"])
    if k2_ok and not M.empty:
        nv["LR-K2.men_only (beside the primary)"] = _brief(k2_safe(basis_frame(data, sorted(H), "A2534_M"), H, B, R,
                                                                   seed))
        lso = {}
        for s_ in sorted({fetch.stratum_of(c) for c in H}):
            Hs = {c: v for c, v in H.items() if fetch.stratum_of(c) != s_}
            if sum(Hs.values()) < 2 or len(Hs) - sum(Hs.values()) < 2:
                lso[s_] = "not estimable"
            else:
                lso[s_] = _brief(k2_safe(M[M["geo"].isin(list(Hs))].reset_index(drop=True).pipe(_keep_attrs, M), Hs,
                                         B, R, seed, with_ri=False))
        nv["LR-K2.leave_one_stratum_out"] = lso
        if "identifying_variation_share" in tests["LR-K2"]:
            nv["LR-K2.identifying_variation_share"] = tests["LR-K2"]["identifying_variation_share"]
    for t in ("LR-Y0", "C-6L", "LR-C1"):                 # leave-one-stratum-out and G*, reported, not acted on
        if t in tests and "error" not in tests[t]:
            used_g = tests[t].get("geos_used", [])
            lso = {}
            for s_ in sorted({fetch.stratum_of(c) for c in used_g}):
                keep = [c for c in used_g if fetch.stratum_of(c) != s_]
                r_ = simple_test(data, t, keep, B=B, seed=seed) if len(keep) >= 3 else dict(error="not estimable")
                lso[s_] = {k_: r_.get(k_) for k_ in ("beta", "p", "p_opposite", "G", "error") if k_ in r_}
            nv[f"{t}.leave_one_stratum_out"] = lso
    out["no_verdict"] = nv
    if robust and H:
        out["robustness"] = robustness(data, H, mem, B, R, seed)
        if "LR-Y0" in labels and labels["LR-Y0"] == "inconclusive":
            sr = out["robustness"].get("strict_control_dropped.LR-Y0")
            sr = None if (sr is None or "error" in sr) else sr
            out["readings"]["LR-Y0"] = y0_reading_note(sr, cal, (std_mde or {}).get("LR-Y0"), (bench or {}).get("LR-Y0"))
    return out


def clean_json(o):
    if isinstance(o, dict):
        return {str(k): clean_json(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean_json(v) for v in o]
    if isinstance(o, (np.floating, float)):
        return float(o) if math.isfinite(float(o)) else None
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    return o
