# specs.py — the tests of PROTOCOL.md section 5, one primary specification each, with their verdicts.
#
# TESTS is the coded form of section 5 (checks/check_protocol.py compares it line by line with its own transcription).
# Every panel regression has country and year fixed effects and the break dummies of C3 (1[geo = c, year >= tau] for
# every break year of every series in the regression: outcome, regressor and controls; dummies constant within their
# country are dropped as collinear with its fixed effect), plus the controls listed. Countries weigh equally; the
# cluster is the country (C8). Inference: the restricted wild cluster bootstrap-t (inference.wcr, Webb weights,
# B = 9999, CR1), one-sided in the predicted direction; for C-4 and C-5 randomisation inference within strata is
# primary (inference.ri; CR1 for C-4, HC2 for C-5) and the WCR is reported alongside. Every test reports beta, the CR1
# se, the one-sided p, the p of the opposite sign (same draws), two intervals by inverting the WCR test (inference.ci):
# 'ci_one_sided' at 95%, [lo, inf) or (-inf, hi] in the predicted direction, the interval that matches the one-sided 5%
# test and its verdict, and 'ci', the two-sided 95% interval (which can cover 0 while the one-sided test rejects);
# the country-years n, G, G* and the MDE (inference.mde from this run's se; the run on the explore half before the
# look gives the MDE the protocol asks for, and confirm.py projects it to the full sample).
#
# Choices the protocol leaves to the code, fixed here:
# - D2's m_c is the country's mean of log q_{c,t-1} over the D2 estimation sample (rows with every variable present).
# - F_c is standardised (mean 0, sd 1 with ddof 0) over the countries given: by default those of the run with a raw F;
#   confirm.py passes the full-sample constants to both of its P runs (see build.py). p-values do not depend on it.
# - C-3 is an intersection-union test: p = max of the two legs' p, p_opposite = max of their opposite p (both legs
#   significantly negative), G* = min of the legs'.
# - C-6's regressor is the cycle itself (U 25-54), so U 25-74 is not added as a further control (PROTOCOL section 5,
#   C-6). The C-6 secondary keeps the whole C-6 equation (U 25-54 included) and adds log q and log q x I.
# - C3 dummies come from every series in the regression: outcome, tested regressor, other terms and controls (U_ct is a
#   regressor of every equation it enters; C3 says 'outcome or regressor series').
# - C-4: U_ct is included (section 5's default; C-4 states no exception). The UK is excluded: it has no post-2019
#   data (PROTOCOL section 5, C-4).
# - C-5 is a cross-section: C3's dummies 1[geo = c, year >= tau] have no panel to act on. The break years inside its
#   2011-2019 window are reported per country ('routine_breaks_2012_2019'); the robustness run 'drop_routine_breaks'
#   drops those countries (PROTOCOL section 5, C-5).
# - Holm runs over the whole family (D: 2, C: 6). A test is 'supported' if its p survives Holm, 'contradicted' if its
#   p_opposite survives Holm on the opposite p-values, 'inconclusive' otherwise. G* is reported, not acted on: the
#   pre-freeze simulations held the bootstrap's size at G* well below 8. Instead every primary test is rerun leaving
#   out each country in turn (leave_one_out); a supported or contradicted verdict whose one-sided p in its own
#   direction exceeds 0.10 with some single country left out carries the qualifier 'rests on one country (XX)', and
#   the model-level verdict carries the qualifiers of the D tests it rests on (PROTOCOL section 5, Verdicts).
# - D1's 'top-quartile F' is the 75th percentile (numpy's linear interpolation) of standardised F over the D1 sample's
#   countries.
# - C-6's window is C2's LFS window, 1997-2025 (what exists inside it, as an unbalanced panel).
# - Only primary tests carry verdict_eligible=True; C-3's legs, the secondaries and the robustness runs carry False.
# - DEVIATED (PROTOCOL section 7): tests whose content changed between the P and E freezes. Empty at the P freeze; it
#   may be edited only before the E freeze (confirm.py runs only code unchanged since that tag). For each, confirm.py
#   takes the primary result from the confirm half, labels the full-sample result exploratory, and runs Holm over the
#   family with the substituted p-values.
# - Secondaries with no registered sign (D1's top-quartile slope, C-1 x outright owners) are two-sided (side 0).
# - Long differences: non-overlapping five-year differences on the grid 1997, 2002, ..., 2022 (no grid year falls in
#   2020-2021), end-year fixed effects, break dummies differenced (1[t-5 < tau <= t]).
#
# run(half) -> every test, secondary and robustness result, the verdicts and the model-level verdict.
# Run from participation/:  ../venv/Scripts/python.exe code/specs.py explore
# Out: results/specs_<half>.json (explore only after the P freeze: the loader refuses before it)

from __future__ import annotations

import json
import math
import os
import sys

import numpy as np
import pandas as pd
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import build  # noqa: E402
import eurostat as es  # noqa: E402
import inference as inf  # noqa: E402

ALPHA = 0.05
LOO_P = 0.10                          # leave-one-country-out: the qualifier threshold
LFS_Q = (1997, 2025)                  # C2: LFS years with q
SILC = (2005, 2025)                   # C2: SILC specifications
LFS = (1997, 2025)                    # C-6: LFS, no q (same window)
C4_YEARS = [2016, 2017, 2018, 2019, 2022, 2023, 2024, 2025]
LD_GRID = [1997, 2002, 2007, 2012, 2017, 2022]
EXCLUDED = (2020, 2021)

# outcome: list of (sign, variable); x: the tested term; z: other non-fixed-effect terms; controls: panel variables.
TESTS = {
    "D1": dict(family="D", outcome=[(1, "A2534")], x="Q*F", z=["Q"], controls=["U"], years=LFS_Q, side=-1,
               inference="wcr", fe=["geo", "year"], what="floor kink across countries: b2 on log q x F_c"),
    "D2": dict(family="D", outcome=[(1, "A2534")], x="sqdev(Q)", z=["Q"], controls=["U"], years=LFS_Q, side=-1,
               inference="wcr", fe=["geo", "year"], what="floor kink over time: the square (log q - m_c)^2"),
    "C1": dict(family="C", outcome=[(1, "coresid2534")], x="Q", z=[], controls=["U"], years=SILC, side=1,
               inference="wcr", fe=["geo", "year"], what="coresidence 25-34 absorbs rents"),
    "C2": dict(family="C", outcome=[(1, "A2534"), (-1, "A5564")], x="Q", z=[], controls=["U"], years=LFS_Q,
               side=1, inference="wcr", fe=["geo", "year"], what="young against old"),
    "C3a": dict(family="C", outcome=[(1, "AW2554"), (-1, "AM2554")], x="Q", z=[], controls=["U"], years=LFS_Q,
                side=1, inference="wcr", fe=["geo", "year"], what="second earners, leg 1: women minus men 25-54"),
    "C3b": dict(family="C", outcome=[(1, "AW2554")], x="Q", z=[], controls=["U"], years=LFS_Q, side=1,
                inference="wcr", fe=["geo", "year"], what="second earners, leg 2: women 25-54"),
    "C4": dict(family="C", outcome=[(1, "E2024"), (-1, "E2554")], x="X*post2023", z=[], controls=["U"],
               years=C4_YEARS, side=-1, inference="ri", studentize="CR1", fe=["geo", "year"], exclude=["UK"],
               what="entrants first: employment 20-24 minus 25-54 on X_c x 1[year>=2023]"),
    "C5": dict(family="C", outcome=[(1, "routine_change")], x="aging_pred", z=[], controls=[], years=(2011, 2019),
               side=-1, inference="ri", studentize="HC2", fe=["stratum"], cross_section=True,
               what="aging pulls the margin: change in routine share 2011-2019 on predicted aging"),
    "C6": dict(family="C", outcome=[(1, "educ2024")], x="U2554", z=[], controls=[], years=LFS, side=1,
               inference="wcr", fe=["geo", "year"], what="school as a paid exit: formal education 20-24 on U 25-54"),
}
PRIMARY = ["D1", "D2", "C1", "C2", "C3", "C4", "C5", "C6"]       # C3 = intersection of C3a and C3b
DEVIATED: frozenset = frozenset()                                 # section 7; see the header
assert DEVIATED <= set(PRIMARY)
FAMILIES = {"D": ["D1", "D2"], "C": ["C1", "C2", "C3", "C4", "C5", "C6"]}

SECONDARY = {
    "D1.slope_top_quartile": dict(base="D1", x="Q", z=["Q*(F-F75)"], side=0,
                                  what="implied slope b1 + b2 F at the top-quartile F (no verdict)"),
    "C1.youth_unemployment": dict(base="C1", controls=["U", "U1529"], what="with youth unemployment 15-29 added"),
    "C1.outright_owners": dict(base="C1", x="Q*O", z=["Q"], side=0,
                               what="log q x outright-owner share 55-64 (2015-2017 mean, not predetermined)"),
    "C6.student_independence": dict(base="C6", x="Q*I", z=["Q", "U2554"], side=-1,
                                    what="the C-6 equation plus log q and log q x (1 - share of students 18-24 "
                                         "living with parents)"),
}
ROBUSTNESS = {
    "all_residents": ["D1", "D2", "C2", "C3a", "C3b", "C4"],
    "q_hpi": ["D1", "D2", "C1", "C2", "C3a", "C3b"],
    "q_cp00": ["D1", "D2", "C1", "C2", "C3a", "C3b"],
    "q_comp": ["D1", "D2", "C1", "C2", "C3a", "C3b"],
    "country_trends": ["D1", "D2", "C1", "C2", "C3a", "C3b", "C4", "C6"],
    "long_differences": ["D1", "D2", "C1", "C2", "C3a", "C3b", "C6"],
    "excl_2008_2013": ["D1", "D2", "C1", "C2", "C3a", "C3b", "C6"],
    "lead": ["D1", "D2", "C1", "C2", "C3a", "C3b"],
    "drop_routine_breaks": ["C5"],
}
Q_ALT = {"q_hpi": "logq_hpi_l1", "q_cp00": "logq_cp00_l1", "q_comp": "logq_comp_l1"}


# ---------------------------------------------------------------- terms

class Ctx:
    """What the terms need: the q column, and the country-level moderators as Series by geo."""

    def __init__(self, cl: pd.DataFrame, fstd: tuple[float, float], q: str = "logq_l1"):
        self.q = q
        self.F = (cl["F_raw"] - fstd[0]) / fstd[1]
        self.O = cl["owner_outright_5564"]
        self.I = cl["student_indep"]
        self.X = cl["X_c"]


def _term_needs(term: str, q: str) -> tuple[list[str], list[str]]:
    """(panel columns, country-level moderators) a term needs."""
    if term in ("Q", "sqdev(Q)"):
        return [q], []
    if term.startswith("Q*"):
        return [q], [{"Q*F": "F", "Q*(F-F75)": "F", "Q*O": "O", "Q*I": "I"}[term]]
    if term == "X*post2023":
        return [], ["X"]
    return [term], []


def _term(term: str, d: pd.DataFrame, ctx: Ctx, q: str, extra: dict) -> np.ndarray:
    geo = d["geo"]
    if term == "Q":
        return d[q].to_numpy(float)
    if term == "sqdev(Q)":
        return ((d[q] - d.groupby("geo")[q].transform("mean")) ** 2).to_numpy(float)
    if term == "Q*F":
        return (d[q] * geo.map(ctx.F)).to_numpy(float)
    if term == "Q*(F-F75)":
        return (d[q] * (geo.map(ctx.F) - extra["F75"])).to_numpy(float)
    if term == "Q*O":
        return (d[q] * (geo.map(ctx.O) - extra["O_mean"])).to_numpy(float)
    if term == "Q*I":
        return (d[q] * geo.map(ctx.I)).to_numpy(float)
    if term == "X*post2023":
        return (geo.map(ctx.X) * (d["year"] >= 2023)).to_numpy(float)
    return d[term].to_numpy(float)


# ---------------------------------------------------------------- the estimation frame

def frame(cy: pd.DataFrame, spec: dict, ctx: Ctx, geos, variant: str | None = None) -> dict:
    """The rows and regressors of one panel specification: dict(M, terms, breaks, lead_terms, meta)."""
    q = Q_ALT.get(variant, "logq_l1")
    lo, hi = (min(spec["years"]), max(spec["years"])) if isinstance(spec["years"], list) else spec["years"]
    years = spec["years"] if isinstance(spec["years"], list) else list(range(lo, hi + 1))
    years = [y for y in years if y not in EXCLUDED and not (variant == "excl_2008_2013" and 2008 <= y <= 2013)]
    outcome = [(s, v + "_all" if variant == "all_residents" else v) for s, v in spec["outcome"]]
    terms = [spec["x"]] + list(spec["z"])
    lead = variant == "lead"
    cols, levels = [v for _, v in outcome] + list(spec["controls"]), []
    for t in terms:
        c, lv = _term_needs(t, q)
        cols += c
        levels += lv
    if lead:
        cols.append("logq_f1")
    d = cy.reset_index()
    d = d[d["geo"].isin([g for g in geos if g not in spec.get("exclude", [])]) & d["year"].isin(years)]
    ok = np.isfinite(d[sorted(set(cols))].to_numpy(float)).all(1)
    for lv in set(levels):
        ok &= np.isfinite(d["geo"].map(getattr(ctx, lv)).to_numpy(float))
    d = d[ok].reset_index(drop=True)
    extra = {}
    if "Q*(F-F75)" in terms:
        extra["F75"] = float(np.percentile(ctx.F.reindex(sorted(set(d["geo"]))).to_numpy(float), 75))
    if "Q*O" in terms:
        extra["O_mean"] = float(ctx.O.reindex(sorted(set(d["geo"]))).mean())
    M = pd.DataFrame({"geo": d["geo"].to_numpy(), "year": d["year"].to_numpy(int)})
    M["y"] = sum(s * d[v].to_numpy(float) for s, v in outcome)
    M["x"] = _term(spec["x"], d, ctx, q, extra)
    names = []
    for i, t in enumerate(spec["z"]):
        M[f"z{i}"] = _term(t, d, ctx, q, extra)
        names.append(f"z{i}")
    for i, c in enumerate(spec["controls"]):
        M[f"c{i}"] = d[c].to_numpy(float)
        names.append(f"c{i}")
    lead_names = []
    if lead:                                  # the lead of every q term, the tested one first
        for i, t in enumerate(terms):
            if _term_needs(t, q)[0] == [q]:
                M[f"lead{i}"] = _term(t, d, ctx, "logq_f1", extra)
                lead_names.append(f"lead{i}")
        names += lead_names
    breaks = set()
    for c in set(cols):
        bc = c + "__breaks"
        if bc in d:
            for g, bl in zip(d["geo"], d[bc]):
                breaks.update((g, int(t)) for t in bl)
    return dict(M=M, names=names, lead=lead_names, breaks=sorted(breaks), years=years, outcome=outcome, q=q)


def break_dummies(M: pd.DataFrame, breaks) -> np.ndarray:
    """C3: 1[geo = c, year >= tau], dropping columns constant within c's rows and duplicate columns."""
    cols, seen = [], set()
    geo, year = M["geo"].to_numpy(), M["year"].to_numpy()
    for g, t in breaks:
        m = geo == g
        if not m.any():
            continue
        col = (m & (year >= t)).astype(float)
        if col[m].min() == col[m].max():
            continue
        key = col.tobytes()
        if key not in seen:
            seen.add(key)
            cols.append(col)
    return np.column_stack(cols) if cols else np.zeros((len(M), 0))


def design(fr: dict, fe=("geo", "year"), trends: bool = False) -> tuple:
    """(y, x, Z, clusters, M) for the annual specification."""
    M = fr["M"]
    blocks = [inf.fe_matrix(M, list(fe)), M[fr["names"]].to_numpy(float).reshape(len(M), -1),
              break_dummies(M, fr["breaks"])]
    if trends:
        t = (M["year"].to_numpy(float) - 2010) / 10
        blocks.append(np.column_stack([(M["geo"].to_numpy() == g) * t for g in sorted(set(M["geo"]))]))
    return M["y"].to_numpy(float), M["x"].to_numpy(float), np.column_stack(blocks), M["geo"].to_numpy(), M


def long_differences(fr: dict) -> tuple:
    """Stacked non-overlapping five-year differences on LD_GRID; end-year fixed effects; differenced breaks."""
    M = fr["M"].set_index(["geo", "year"])
    cols = ["y", "x"] + fr["names"]
    rows, keys = [], []
    for g in sorted(set(M.index.get_level_values(0))):
        for t in LD_GRID[1:]:
            if (g, t) in M.index and (g, t - 5) in M.index:
                rows.append(M.loc[(g, t), cols].to_numpy(float) - M.loc[(g, t - 5), cols].to_numpy(float))
                keys.append((g, t))
    if not rows:
        raise ValueError("no five-year differences")
    D = pd.DataFrame(rows, columns=cols)
    D["geo"] = [k[0] for k in keys]
    D["year"] = [k[1] for k in keys]
    br = []
    for g, tau in fr["breaks"]:
        col = ((D["geo"] == g) & (D["year"] - 5 < tau) & (tau <= D["year"])).to_numpy(float)
        if col.any():
            br.append(col)
    Z = np.column_stack([inf.fe_matrix(D, "year"), D[fr["names"]].to_numpy(float).reshape(len(D), -1)]
                        + ([np.column_stack(br)] if br else []))
    return D["y"].to_numpy(float), D["x"].to_numpy(float), Z, D["geo"].to_numpy(), D


# ---------------------------------------------------------------- one test

def _wcr_block(y, x, Z, g, side, B, seed, with_ci):
    r = inf.wcr(y, x, Z, g, side=side, B=B, seed=seed)
    r["ci"] = list(inf.ci(y, x, Z, g, side=0, B=B, seed=seed)) if with_ci else None
    r["ci_one_sided"] = list(inf.ci(y, x, Z, g, side=side, B=B, seed=seed)) if with_ci and side else None
    return r


def estimate(cy, cl, spec: dict, ctx: Ctx, geos, variant=None, B=9999, R=9999, seed=inf.SEED,
             with_ci=True) -> dict:
    side = spec["side"]
    out = dict(family=spec.get("family"), side=side, inference=spec["inference"], variant=variant,
               outcome=" - ".join(v for _, v in spec["outcome"]), regressor=spec["x"], z=list(spec["z"]),
               controls=list(spec["controls"]), fe=list(spec["fe"]))
    if spec.get("cross_section"):
        return {**out, **_cross(cl, spec, geos, B, R, seed, with_ci, variant)}
    fr = frame(cy, spec, ctx, geos, variant)
    if variant == "long_differences":
        y, x, Z, g, M = long_differences(fr)
    else:
        y, x, Z, g, M = design(fr, spec["fe"], trends=(variant == "country_trends"))
    r = _wcr_block(y, x, Z, g, side if side else 0, B, seed, with_ci)
    out.update(beta=r["beta"], se=r["se"], t=r["t"], p=r["p"], p_opposite=r["p_opposite"], ci=r["ci"],
               ci_one_sided=r["ci_one_sided"], n=r["n"], G=r["G"], G_star=r["G_star"],
               n_clusters_varying=r["n_clusters_varying"], n_clusters_varying_raw=r["n_clusters_varying_raw"],
               mde=inf.mde(r["se"], r["G"]), q=fr["q"], years_used=sorted(int(v) for v in set(M["year"])),
               geos_used=sorted(set(M["geo"])), n_break_dummies=int(len(fr["breaks"])))
    if spec["inference"] == "ri" and variant != "long_differences":
        Zr = Z
        mult = (M["year"].to_numpy() >= 2023).astype(float)
        strata = cl["stratum"]
        ri = inf.ri(y, ctx.X, g, strata, Zr, side=side, R=R, seed=seed, studentize=spec["studentize"], x_mult=mult)
        ro = inf.ri(y, ctx.X, g, strata, Zr, side=-side, R=R, seed=seed, studentize=spec["studentize"], x_mult=mult)
        out.update(p_wcr=r["p"], p_wcr_opposite=r["p_opposite"], p=ri["p"], p_opposite=ro["p"],
                   n_perm=ri["n_perm"], exact=ri["exact"], t_ri=ri["t"])
    if fr["lead"]:                            # the lead of the tested term, everything else held as in the run
        cols = [c for c in fr["names"] if c != fr["lead"][0]]
        Zl = np.column_stack([inf.fe_matrix(M, list(spec["fe"])), M[["x"] + cols].to_numpy(float),
                              break_dummies(M, fr["breaks"])])
        rl = inf.wcr(y, M[fr["lead"][0]].to_numpy(float), Zl, g, side=0, B=B, seed=seed)
        out["lead_coefficient"] = dict(beta=rl["beta"], se=rl["se"], p_two_sided=rl["p"])
    return out


def _cross(cl, spec, geos, B, R, seed, with_ci, variant=None) -> dict:
    """C-5: one row per country, stratum fixed effects only; RI within strata (HC2) primary, WCR alongside."""
    if variant not in (None, "drop_routine_breaks"):
        raise ValueError(f"no {variant} variant for the cross-section")
    d = cl.loc[[g for g in geos if g in cl.index]]
    d = d[np.isfinite(d["routine_change"].to_numpy(float)) & np.isfinite(d["aging_pred"].to_numpy(float))]
    if variant == "drop_routine_breaks":
        d = d[[len(b) == 0 for b in d["routine_breaks"]]]
    D = d.reset_index()
    y, x = D["routine_change"].to_numpy(float), D["aging_pred"].to_numpy(float)
    Z = inf.fe_matrix(D, "stratum")
    g = D["geo"].to_numpy()
    r = _wcr_block(y, x, Z, g, spec["side"], B, seed, with_ci)
    ri = inf.ri(y, D.set_index("geo")["aging_pred"], g, D.set_index("geo")["stratum"], Z, side=spec["side"], R=R,
                seed=seed, studentize=spec["studentize"])
    ro = inf.ri(y, D.set_index("geo")["aging_pred"], g, D.set_index("geo")["stratum"], Z, side=-spec["side"], R=R,
                seed=seed, studentize=spec["studentize"])
    se_hc2 = ri["beta"] / ri["t"] if ri["t"] else math.nan
    brk = ({g: [int(t) for t in b] for g, b in zip(D["geo"], D["routine_breaks"]) if len(b)}
           if "routine_breaks" in D else None)
    return dict(beta=r["beta"], se=r["se"], se_hc2=se_hc2, t=r["t"], t_ri=ri["t"], p=ri["p"], p_opposite=ro["p"],
                p_wcr=r["p"], p_wcr_opposite=r["p_opposite"], ci=r["ci"], ci_one_sided=r["ci_one_sided"], n=r["n"],
                G=r["G"], G_star=r["G_star"], n_clusters_varying=r["n_clusters_varying"],
                n_clusters_varying_raw=r["n_clusters_varying_raw"], mde=inf.mde(se_hc2, r["G"]), n_perm=ri["n_perm"],
                exact=ri["exact"], years_used=[2011, 2019], geos_used=sorted(D["geo"]), routine_breaks_2012_2019=brk)


def intersection(a: dict, b: dict) -> dict:
    """C-3: both legs must reject."""
    return dict(family="C", side=1, inference="wcr (intersection-union)", legs=["C3a", "C3b"],
                p=max(a["p"], b["p"]), p_opposite=max(a["p_opposite"], b["p_opposite"]),
                G_star=min(a["G_star"], b["G_star"]), n=min(a["n"], b["n"]), G=min(a["G"], b["G"]),
                beta=None, se=None, ci=None, ci_one_sided=None, mde=None,
                mde_legs={"C3a": a.get("mde"), "C3b": b.get("mde")})


def event_study(cy, cl, ctx: Ctx, geos) -> dict:
    """C-4 pre-trend: X_c x 1[year = tau] for 2016-2019 and 2023-2025, 2022 the reference; the four pre-period
    coefficients' joint CR1 Wald test against F(4, G-1). Reported, no verdict; 'pre-trend' flagged at 10%."""
    spec = TESTS["C4"]
    fr = frame(cy, spec, ctx, geos)
    y, _, Z, g, M = design(fr, spec["fe"])
    taus = [2016, 2017, 2018, 2019, 2023, 2024, 2025]
    X = M["geo"].map(ctx.X).to_numpy(float)
    W = np.column_stack([X * (M["year"].to_numpy() == t) for t in taus])
    Q = inf._basis(Z)
    Wt, yt = W - Q @ (Q.T @ W), y - Q @ (Q.T @ y)
    A = np.linalg.pinv(Wt.T @ Wt)
    b = A @ Wt.T @ yt
    u = yt - Wt @ b
    labels, gi = np.unique(g, return_inverse=True)
    G, n, k = len(labels), len(y), Q.shape[1] + W.shape[1]          # Q spans [1, Z]: the constant is in it
    S = np.zeros((W.shape[1], W.shape[1]))
    for j in range(G):
        s = Wt[gi == j].T @ u[gi == j]
        S += np.outer(s, s)
    V = G / (G - 1) * (n - 1) / (n - k) * A @ S @ A
    pre = slice(0, 4)
    wald = float(b[pre] @ np.linalg.pinv(V[pre, pre]) @ b[pre]) / 4
    p = float(stats.f.sf(wald, 4, G - 1))
    return dict(coefficients={str(t): float(c) for t, c in zip(taus, b)},
                se={str(t): float(math.sqrt(max(V[i, i], 0))) for i, t in enumerate(taus)},
                joint_pre_F=wald, joint_pre_p=p, pre_trend_flag=bool(p < 0.10), n=n, G=G, verdict_eligible=False)


# ---------------------------------------------------------------- verdicts

def holm_reject(pvals: dict, alpha: float = ALPHA) -> set:
    """Holm step-down over the family: the ids whose p survives at familywise alpha."""
    order = sorted(pvals, key=lambda k: (pvals[k], k))
    m, out = len(order), set()
    for i, k in enumerate(order):
        if pvals[k] <= alpha / (m - i):
            out.add(k)
        else:
            break
    return out


def holm(results: dict, alpha: float = ALPHA) -> dict:
    """Verdict labels of one family (PROTOCOL section 5)."""
    sup = holm_reject({k: r["p"] for k, r in results.items()}, alpha)
    con = holm_reject({k: r["p_opposite"] for k, r in results.items()}, alpha)
    out = {}
    for k, r in results.items():
        if k in sup:
            out[k] = "supported"
        elif k in con:
            out[k] = "contradicted"
        else:
            out[k] = "inconclusive"
    return out


def verdicts(tests: dict) -> tuple[dict, str]:
    """(labels of every primary test, Holm within each family; the model-level verdict)."""
    labels = {}
    for ids in FAMILIES.values():
        labels.update(holm({k: tests[k] for k in ids}))
    return labels, model_verdict(labels)


def model_verdict(labels: dict) -> str:
    d = [labels["D1"], labels["D2"]]
    if "contradicted" in d:
        return "against the floor mechanism"
    if "supported" in d:
        return "favours the model"
    return "inconclusive"


def leave_one_out(tid: str, cy, cl, geos, fstd, B=9999, R=9999, seed=inf.SEED) -> dict:
    """A primary test rerun leaving out each country it uses: the largest one-sided p in each direction and the
    country whose omission gives it."""
    full = test(tid, cy, cl, geos=geos, fstd=fstd, B=B, R=R, seed=seed, with_ci=False)
    used = full["C3a"]["geos_used"] if tid == "C3" else full["geos_used"]
    worst = dict(p=(full["p"], None), p_opposite=(full["p_opposite"], None))
    for g in used:
        r = test(tid, cy, cl, geos=[c for c in geos if c != g], fstd=fstd, B=B, R=R, seed=seed, with_ci=False)
        for key in worst:
            if r[key] > worst[key][0]:
                worst[key] = (r[key], g)
    return dict(max_p=worst["p"][0], max_p_left_out=worst["p"][1], max_p_opposite=worst["p_opposite"][0],
                max_p_opposite_left_out=worst["p_opposite"][1], n_left_out=len(used))


def qualify(labels: dict, loo: dict) -> dict:
    """'rests on one country (XX)' where a verdict's own-direction p exceeds LOO_P with country XX left out."""
    out = {}
    for k, lab in labels.items():
        key = {"supported": "max_p", "contradicted": "max_p_opposite"}.get(lab)
        out[k] = f"rests on one country ({loo[k][key + '_left_out']})" if key and loo[k][key] > LOO_P else ""
    return out


def model_qualifier(labels: dict, quals: dict) -> str:
    """The qualifiers of the D tests the model-level verdict rests on."""
    model = model_verdict(labels)
    rests = {"favours the model": "supported", "against the floor mechanism": "contradicted"}.get(model)
    return "; ".join(f"D{i}: {quals[f'D{i}']}" for i in (1, 2) if rests and labels[f"D{i}"] == rests
                     and quals[f"D{i}"])


# ---------------------------------------------------------------- run

def f_constants(cl: pd.DataFrame, geos) -> tuple[float, float]:
    f = cl.loc[[g for g in geos if g in cl.index], "F_raw"].astype(float).dropna()
    return float(f.mean()), float(f.std(ddof=0))


def _merge(base: dict, over: dict) -> dict:
    s = dict(base)
    s.update({k: v for k, v in over.items() if k not in ("base", "what")})
    return s


def test(tid: str, cy, cl, geos=None, fstd=None, B=9999, R=9999, seed=inf.SEED, with_ci=True) -> dict:
    """One primary test (C3: both legs and their intersection) on these frames."""
    geos = sorted(set(cy.index.get_level_values(0))) if geos is None else sorted(geos)
    ctx = Ctx(cl, f_constants(cl, geos) if fstd is None else tuple(fstd))
    kw = dict(B=B, R=R, seed=seed, with_ci=with_ci)
    if tid == "C3":
        a, b = ({"id": k, "verdict_eligible": False, **estimate(cy, cl, TESTS[k], ctx, geos, **kw)}
                for k in ("C3a", "C3b"))
        return {"id": "C3", "verdict_eligible": True, **intersection(a, b), "C3a": a, "C3b": b}
    return {"id": tid, "verdict_eligible": True, "what": TESTS[tid]["what"],
            **estimate(cy, cl, TESTS[tid], ctx, geos, **kw)}


def D1(cy, cl, **kw):
    return test("D1", cy, cl, **kw)


def D2(cy, cl, **kw):
    return test("D2", cy, cl, **kw)


def C1(cy, cl, **kw):
    return test("C1", cy, cl, **kw)


def C2(cy, cl, **kw):
    return test("C2", cy, cl, **kw)


def C3(cy, cl, **kw):
    return test("C3", cy, cl, **kw)


def C4(cy, cl, **kw):
    return test("C4", cy, cl, **kw)


def C5(cy, cl, **kw):
    return test("C5", cy, cl, **kw)


def C6(cy, cl, **kw):
    return test("C6", cy, cl, **kw)


def run(half: str = "explore", cy=None, cl=None, geos=None, fstd=None, B=9999, R=9999, seed=inf.SEED,
        with_ci=True, secondary=True, robustness=True, loo=True) -> dict:
    """All tests of section 5 on this half (or the given frames and countries), with verdicts."""
    if cy is None:
        cy, cl = build.country_year(half), build.country_level(half)
    geos = sorted(set(cy.index.get_level_values(0))) if geos is None else sorted(geos)
    fstd = f_constants(cl, geos) if fstd is None else tuple(fstd)
    ctx = Ctx(cl, fstd)
    kw = dict(B=B, R=R, seed=seed, with_ci=with_ci)
    tests = {}
    for k, spec in TESTS.items():
        tests[k] = {"id": k, "verdict_eligible": k in PRIMARY, "what": spec["what"],
                    **estimate(cy, cl, spec, ctx, geos, **kw)}
    tests["C3"] = {"id": "C3", "verdict_eligible": True, "what": "second earners (intersection-union)",
                   **intersection(tests["C3a"], tests["C3b"])}
    labels, model = verdicts(tests)
    loo = {k: leave_one_out(k, cy, cl, geos, fstd, B=B, R=R, seed=seed) for k in PRIMARY} if loo else None
    quals = qualify(labels, loo) if loo else {k: "" for k in PRIMARY}  # loo=False only in simulation replications
    out = dict(half=half, geos=geos, F_standardisation=dict(mean=fstd[0], sd=fstd[1], ddof=0),
               tests={k: tests[k] for k in PRIMARY + ["C3a", "C3b"]}, verdicts=labels, leave_one_out=loo,
               qualifiers=quals, model_verdict=model, model_qualifier=model_qualifier(labels, quals),
               B=B, R=R, seed=seed)
    if secondary:
        sec = {}
        for k, s in SECONDARY.items():
            sec[k] = {"id": k, "verdict_eligible": False, "what": s["what"],
                      **estimate(cy, cl, _merge(TESTS[s["base"]], s), ctx, geos, **kw)}
        sec["C4.pretrend"] = {"id": "C4.pretrend", **event_study(cy, cl, ctx, geos)}
        out["secondary"] = sec
    if robustness:
        rob = {}
        for v, ids in ROBUSTNESS.items():
            for k in ids:
                rid = f"{k}.{v}"
                try:
                    rob[rid] = {"id": rid, "verdict_eligible": False,
                                **estimate(cy, cl, TESTS[k], Ctx(cl, fstd), geos, variant=v, **kw)}
                except ValueError as e:
                    rob[rid] = {"id": rid, "verdict_eligible": False, "error": str(e)}
        out["robustness"] = rob
    return out


def clean_json(o):
    """NaN and inf to None, numpy scalars to Python, recursively (for json.dump)."""
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


def main() -> None:
    half = sys.argv[1] if len(sys.argv) > 1 else "explore"
    if half != "explore":
        raise SystemExit("specs.py runs the explore half; the look is code/confirm.py")
    es.guard("explore")
    res = run("explore")
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    path = os.path.join(ROOT, "results", f"specs_{half}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(clean_json(res), f, indent=1)
    for k in PRIMARY:
        r = res["tests"][k]
        print(f"  {k:3s} p {r['p']:.4f}  p_opp {r['p_opposite']:.4f}  G* {r['G_star']:.1f}  {res['verdicts'][k]}"
              f"  {res['qualifiers'][k]}")
    print(f"model: {res['model_verdict']} {res['model_qualifier']}\nwrote {path}")


if __name__ == "__main__":
    main()
