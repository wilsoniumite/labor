# sectors.py — Question 2, sectors unit: has care absorbed US spending growth the way it absorbed job growth?
#
# What it does
#   1. Exact additive contributions to the growth of real PCE (BEA's chain-type Fisher quantity index), period by
#      period, from the 243 current leaf lines of NIPA Table 2.4.5U (current dollars) and Table 2.4.4U (price
#      indexes), with BEA's contributions formula (NIPA Handbook ch. 4, p. 4-28):
#          C_i,t = [(p_i,t / F_t) + p_i,t-1] (q_i,t - q_i,t-1) / sum_j [(p_j,t / F_t) + p_j,t-1] q_j,t-1
#      where q = value / price (signed: 'Less:' lines and the lines under them enter with -1) and F_t is the Fisher
#      price relative of PCE. The contributions add exactly to the Fisher quantity relative minus 1.
#   2. Windows: monthly contributions chained with the cumulative real index up to the previous month, so they add
#      to the window's real growth; the residual against BEA's own real PCE (2.4.6U line 1) is reported per window.
#   3. Groupings (functional partition of PCE; three care definitions with variants; imputed items), the
#      outside-care indexes beside real personal income excluding transfers, and the Medicare + Medicaid arithmetic;
#      care's share of PCE at both ends of each window in dollars and at start prices (and why its share of the dollar
#      increase sits below its share of real growth); when the spending-income gap opened; Table 4's BEA residuals.
#   4. Cross-checks against BEA's published contributions (Tables 2.8.2 monthly, 2.3.2 and 2.4.2 annual).
#   5. The jobs side, read from the vendored watch page, and the figures.
#
# Run from the repo root:  venv/bin/python -I consumption/recent/code/sectors.py      (about 25 s)
# Inputs (nothing is downloaded):
#   consumption/data/tidy/bea_pce_u_long.csv.gz, bea_pce_u_lines.csv, bea_pi_long.csv
#   consumption/data/raw/bea/nipa/xls_survey/Section2All_xls.xlsx   (published contributions, Tables 2.3.2/2.4.2/2.8.2)
#   consumption/data/raw/watch/jobs-outside-care.html               (the jobs series behind the watch page's chart)
# Outputs: consumption/recent/out/*.csv (+ out/notes_tables_sectors.md) and consumption/recent/figures/*.png (200 dpi).
# Plain functions and top-level code, so each '# %%' block can be pasted into a notebook cell.

# %% setup
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent                  # consumption/recent/code
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1] / "code"))       # consumption/code (common.py: paths)
import common                                           # noqa: E402

import functools                                        # noqa: E402
import json                                             # noqa: E402
import re                                               # noqa: E402
import numpy as np                                      # noqa: E402
import pandas as pd                                     # noqa: E402
import openpyxl                                         # noqa: E402
from tqdm.auto import tqdm                              # noqa: E402

RECENT = HERE.parent
OUT = RECENT / "out"
FIG = RECENT / "figures"
OUT.mkdir(exist_ok=True)
FIG.mkdir(exist_ok=True)
TIDY = common.TIDY
SURVEY_XLSX = common.RAW / "bea" / "nipa" / "xls_survey" / "Section2All_xls.xlsx"
WATCH_JOBS = common.RAW / "watch" / "jobs-outside-care.html"

# The windows. 'jobs' is the watch site's two-year jobs window, '6m' its spending-and-income window.
WINDOWS = [
    # key,   freq, start,     end,       label
    ("jobs", "M", "2024-08", "2026-08", "Aug 2024 to Aug 2026 (jobs window)"),
    ("12m", "M", "2025-09", "2026-09", "12 months to Sep 2026"),
    ("6m", "M", "2026-03", "2026-09", "6 months to Sep 2026 (watch window)"),
    ("4y", "M", "2022-09", "2026-09", "4 years to Sep 2026"),
    ("annual", "A", "2022", "2025", "2022 to 2025 (annual data)"),
]
WLABEL = {w[0]: w[4] for w in WINDOWS}


def window_tag(start, end):
    return f"{start}_{end}"


# %% load
lines = pd.read_csv(TIDY / "bea_pce_u_lines.csv")
lines["parent_line"] = lines["parent_line"].astype("Int64")
u = pd.read_csv(TIDY / "bea_pce_u_long.csv.gz", dtype={"table": str, "context": str})
pi_long = pd.read_csv(TIDY / "bea_pi_long.csv", dtype={"table": str, "context": str})


def wide(df, table, freq):
    x = df[(df["table"] == table) & (df["freq"] == freq)]
    return x.pivot(index="date", columns="line", values="value").sort_index()


V = {f: wide(u, "2.4.5U", f) for f in "MA"}     # current dollars (millions; monthly at SAAR)
P = {f: wide(u, "2.4.4U", f) for f in "MA"}     # price indexes, 2017=100
Q = {f: wide(u, "2.4.3U", f) for f in "MA"}     # quantity indexes, 2017=100
X = {f: wide(u, "2.4.6U", f) for f in "MA"}     # chained 2017 dollars (from 2007)
PI = {"M": wide(pi_long, "2.6", "M"), "A": wide(pi_long, "2.1", "A")}

# %% hierarchy helpers
main = lines[lines["section"] == "main"]
CHILDREN = {int(l): main.loc[main["parent_line"] == l, "line"].astype(int).tolist() for l in main["line"]}
PARENT = {int(r.line): (int(r.parent_line) if pd.notna(r.parent_line) else None) for r in main.itertuples()}
SIGN_ROOT = main.set_index("line")["sign_to_root"].astype(float)
SIGN = SIGN_ROOT.to_dict()
LABEL = lines.set_index("line")["label_short"]
LEVEL = lines.set_index("line")["level"]
NET_LINES = {145, 333}      # nets of two flows: BEA publishes no price or quantity index, so no real growth


@functools.lru_cache(maxsize=None)
def ancestors_incl(line):
    out = [line]
    while PARENT.get(out[-1]) is not None:
        out.append(PARENT[out[-1]])
    return tuple(out)


def is_under(line, top):
    """True if `line` is `top` or sits below it in the 2.4.5U hierarchy."""
    return top in ancestors_incl(line)


def partition(node, v0, v1):
    """Finest set of lines below `node` usable for a pair of periods (v0, v1: dicts of values by line, NaN = none).

    A node is split into its children only if the same children are published in both periods and they add up
    to the node (signed) within rounding; otherwise the node itself is the deflation-level component. This handles
    lines that start late (e.g. 10-11 from 2002-01) or stop (157-158 to 2001-12)."""
    kids = CHILDREN[node]
    k0 = [k for k in kids if v0[k] == v0[k]]
    k1 = [k for k in kids if v1[k] == v1[k]]
    if kids and k0 and k0 == k1:
        bound = (len(k0) + 1) / 2 + 1          # rounding bound in millions of dollars (README_bea.md)
        ok = all(abs(sum(SIGN[k] * SIGN[node] * vv[k] for k in k0) - vv[node]) <= bound for vv in (v0, v1))
        if ok:
            return [leaf for k in k0 for leaf in partition(k, v0, v1)]
    return [node]


# %% the Fisher engine (BEA level form, NIPA Handbook ch. 4)
def fisher_pair(v0, v1, p0, p1):
    """Fisher quantity and price relatives of the aggregate and each component's contribution (a fraction).

    v0, v1: signed current-dollar values of the components; p0, p1: their price indexes. q = v / p. The level
    form also handles a component whose earlier value is zero (line 289, Internet access, is 0 through 1987)."""
    q0, q1 = v0 / p0, v1 / p1
    LQ = (p0 * q1).sum() / (p0 * q0).sum()
    PQ = (p1 * q1).sum() / (p1 * q0).sum()
    LP = (p1 * q0).sum() / (p0 * q0).sum()
    PP = (p1 * q1).sum() / (p0 * q1).sum()
    FQ, FP = np.sqrt(LQ * PQ), np.sqrt(LP * PP)
    w = p1 / FP + p0
    C = w * (q1 - q0) / (w * q0).sum()
    return FQ, FP, C


def fisher_many(M, v0, v1, p0, p1):
    """Fisher quantity relatives of many sub-aggregates at once. M is an (aggregates x components) 0/1 matrix."""
    q0, q1 = v0 / p0, v1 / p1
    with np.errstate(divide="ignore", invalid="ignore"):
        LQ = (M @ (p0 * q1)) / (M @ (p0 * q0))
        PQ = (M @ (p1 * q1)) / (M @ (p1 * q0))
        prod = LQ * PQ
        return np.where(prod > 0, np.sqrt(np.where(prod > 0, prod, 1.0)), np.nan)


def membership(part, aggs):
    """(aggregates x components) matrix for a partition. An aggregate is (include tops, exclude tops); a component
    belongs if it is under an include top and not under an exclude top. If the partition is too coarse to separate
    an aggregate (a component is a strict ancestor of one of its tops), that aggregate's row is NaN."""
    M = np.zeros((len(aggs), len(part)))
    for i, (inc, exc) in enumerate(aggs.values()):
        tops = list(inc) + list(exc)
        if any(t != c and is_under(t, c) for t in tops for c in part):
            M[i, :] = np.nan
            continue
        for j, c in enumerate(part):
            M[i, j] = float(any(is_under(c, t) for t in inc) and not any(is_under(c, t) for t in exc))
    return M


def run_chain(freq, start, end, aggs):
    """Period-by-period contributions of every component, the PCE Fisher relatives, and each aggregate's own
    Fisher relative. Returns (C: periods x lines, FQ: Series, FP: Series, AGG: periods x aggregates, parts)."""
    v_, p_ = V[freq].loc[start:end], P[freq].loc[start:end]
    dates = v_.index.tolist()
    vd = {t: v_.loc[t].to_dict() for t in dates}
    C_rows, FQ, FP, A_rows, parts, cache = {}, {}, {}, {}, {}, {}
    for t0, t1 in tqdm(list(zip(dates[:-1], dates[1:])), desc=f"Fisher chain {freq} {start}..{end}",
                       mininterval=2.0):
        part = tuple(partition(1, vd[t0], vd[t1]))
        pl = list(part)
        if p_.loc[[t0, t1], pl].isna().any().any():
            raise ValueError(f"missing price index for a component in {t0}->{t1}")
        sg = SIGN_ROOT[pl].values
        v0, v1 = v_.loc[t0, pl].values * sg, v_.loc[t1, pl].values * sg
        p0, p1 = p_.loc[t0, pl].values, p_.loc[t1, pl].values
        fq, fp, c = fisher_pair(v0, v1, p0, p1)
        if abs(c.sum() - (fq - 1)) > 1e-12:
            raise AssertionError(f"contributions do not add up in {t1}: {c.sum()} vs {fq - 1}")
        if part not in cache:
            cache[part] = membership(part, aggs)
        M = cache[part]
        bad = np.isnan(M).any(axis=1)
        C_rows[t1] = pd.Series(c, index=pl)
        FQ[t1], FP[t1] = fq, fp
        A_rows[t1] = pd.Series(np.where(bad, np.nan, fisher_many(np.nan_to_num(M, nan=0.0), v0, v1, p0, p1)),
                               index=list(aggs))
        parts[t1] = part
    return (pd.DataFrame(C_rows).T, pd.Series(FQ), pd.Series(FP), pd.DataFrame(A_rows).T, parts)


def window_weights(FQ, a, b):
    """Weights I_{t-1} / I_a for the periods a < t <= b, from the Fisher relatives FQ (indexed by t)."""
    per = [t for t in FQ.index if a < t <= b]
    cum = FQ.loc[per].cumprod()
    return cum.shift(1).fillna(1.0)


def window_contrib(C, FQ, a, b):
    w = window_weights(FQ, a, b)
    return C.loc[w.index].fillna(0.0).mul(w, axis=0).sum()


def window_growth(F, a, b):
    """Growth over (a, b] from a Series of period relatives (NaN if any relative is missing)."""
    per = [t for t in F.index if a < t <= b]
    x = F.loc[per]
    return np.nan if x.isna().any() else float(x.prod() - 1)


# %% definitions: functional groups (a partition of PCE), care, imputed items
# Each definition is (include tops, exclude tops) in 2.4.5U lines. Lines 357, 363 and the other lines under 356
# enter PCE with sign -1, so "344 - 357" is written as include (344, 357).
FUNC = {
    "Durable goods": ([3], []),
    "Nondurable goods excl. energy": ([72], [113]),
    "Gasoline and other energy goods": ([113], []),
    "Housing and utilities excl. imputed rent": ([152], [160]),
    "Imputed rent of owner-occupied housing (160)": ([160], []),
    "Health care (172)": ([172], []),
    "Transportation services": ([190], []),
    "Recreation services": ([209], []),
    "Food services and accommodations": ([234], []),
    "Financial services and insurance excl. FSFWP": ([252], [254]),
    "Financial services furnished without payment (254)": ([254], []),
    "Other services excl. net foreign travel": ([280], [333]),
    "Net foreign travel (333)": ([333], []),
    "NPISH final consumption (342)": ([342], []),
}
CARE_TOPS = {
    "A": [172],                                         # (a) health care services, households
    "A+": [172, 344, 357],                              # (a) + NPISH health (344 - 357)
    "B": [172, 344, 357, 121, 66, 275],                 # (b) = A+ + pharma and medical products + therapeutic
                                                        #     appliances + net health insurance
    "C": [172, 344, 357, 121, 66, 275, 316, 317],      # (c) = B + child care + social assistance
    "C+": [172, 344, 357, 121, 66, 275, 316, 317, 350, 363],   # (c) + NPISH social services (350 - 363)
    "S": [172, 344, 357, 316, 317, 350, 363],           # care services only (not asked for; closest to NAICS 62)
}
CARE_LABEL = {
    "A": "(a) Health care services, households (172)",
    "A+": "(a+) Health care services incl. NPISH health (172 + 344 - 357)",
    "B": "(b) (a+) + medical products, appliances, net health insurance (121, 66, 275)",
    "C": "(c) (b) + child care and social assistance (316, 317)",
    "C+": "(c+) (c) + NPISH social services (350 - 363)",
    "S": "(s) Care services only: (a+) + 316 + 317 + (350 - 363)",
}
CARE_PARTS = {   # the increments between variants, for reading the tables
    "NPISH health (344 - 357)": ([344, 357], []),
    "Medical products, appliances, net health insurance (121, 66, 275)": ([121, 66, 275], []),
    "Child care (316)": ([316], []),
    "Social assistance (317)": ([317], []),
    "NPISH social services (350 - 363)": ([350, 363], []),
    "Day care and nursery schools (296, education; not in any care variant)": ([296], []),
}
IMPUTED_TOPS = [160, 163, 254, 342]                    # imputed rent (nonfarm, farm), FSFWP, NPISH
# A second partition of PCE for the contribution charts: care (c) in its parts, everything else by function.
CARE_FIRST = {
    "care: Health care services (172)": ([172], []),
    "care: NPISH health (344 - 357)": ([344, 357], []),
    "care: Medical products and appliances (121, 66)": ([121, 66], []),
    "care: Net health insurance (275)": ([275], []),
    "care: Child care and social assistance (316, 317)": ([316, 317], []),
    "Durable goods excl. therapeutic appliances": ([3], [66]),
    "Nondurable goods excl. energy and medical products": ([72], [113, 121]),
    "Gasoline and other energy goods": ([113], []),
    "Housing and utilities excl. imputed rent": ([152], [160]),
    "Imputed rent of owner-occupied housing": ([160], []),
    "Transportation services": ([190], []),
    "Recreation services": ([209], []),
    "Food services and accommodations": ([234], []),
    "Financial services and insurance excl. FSFWP and health insurance": ([252], [254, 275]),
    "Financial services furnished without payment": ([254], []),
    "Other services excl. net foreign travel, child care, social assistance": ([280], [333, 316, 317]),
    "Net foreign travel": ([333], []),
    "NPISH final consumption excl. health": ([342], [344, 357]),
}
NET_AGGS_NOTE = {   # aggregates that are a small net of two large flows: their own real growth is not robust
    "Net foreign travel (333)": "net of two flows; BEA publishes no index; real growth not defined",
    "NPISH health (344 - 357)": "net of gross output and sales (about 5% of either); real growth not robust",
    "NPISH social services (350 - 363)": "net of gross output and sales; real growth not robust",
    "NPISH final consumption (342)": "net of gross output and sales (BEA publishes an index for it)",
}

AGGS = {f"line {l}": ([l], []) for l in main["line"].astype(int)}
AGGS.update({f"func: {g}": d for g, d in FUNC.items()})
AGGS["func: Goods"] = ([2], [])
AGGS["func: Services"] = ([150], [])
for k, tops in CARE_TOPS.items():
    AGGS[f"care {k}"] = (tops, [])
    AGGS[f"outside care {k}"] = ([1], tops)
    AGGS[f"outside care {k} and imputed"] = ([1], tops + IMPUTED_TOPS)
AGGS.update({f"care part: {g}": d for g, d in CARE_PARTS.items()})
AGGS.update({f"care-first: {g}": d for g, d in CARE_FIRST.items()})
AGGS["imputed"] = (IMPUTED_TOPS, [])
AGGS["outside imputed"] = ([1], IMPUTED_TOPS)

# %% run the chains
# Monthly from 1959 (the full history exercises the late-start handling; outputs use 2007 on), annual from 1959.
C_M, FQ_M, FP_M, AGG_M, PARTS_M = run_chain("M", "1959-01", "2026-09", AGGS)
C_A, FQ_A, FP_A, AGG_A, PARTS_A = run_chain("A", "1959", "2025", AGGS)
CHAIN = {"M": (C_M, FQ_M, FP_M, AGG_M, PARTS_M), "A": (C_A, FQ_A, FP_A, AGG_A, PARTS_A)}

# The current partition: the 243 current leaves; it is the partition of every pair from 2007-02 (annual: 2008).
CUR = list(PARTS_M["2026-09"])
assert len(CUR) == 243, len(CUR)
assert all(PARTS_M[t] == PARTS_M["2026-09"] for t in PARTS_M if t >= "2007-02")
assert all(PARTS_A[t] == PARTS_M["2026-09"] for t in PARTS_A if t >= "2008")


def members_of(agg, part):
    inc, exc = AGGS[agg]
    return [c for c in part if any(is_under(c, t) for t in inc) and not any(is_under(c, t) for t in exc)]


MEMBERS = {agg: members_of(agg, CUR) for agg in AGGS}           # current partition, computed once
MEMBER_SETS = {agg: set(ms) for agg, ms in MEMBERS.items()}
DESC_CUR = {int(l): [c for c in CUR if is_under(c, int(l))] for l in main["line"]}


def members(agg):
    return MEMBERS[agg]


# Every current leaf sits in exactly one functional group, and in exactly one care-first group.
for prefix, groups in [("func: ", FUNC), ("care-first: ", CARE_FIRST)]:
    seen = {}
    for g in groups:
        for c in members(prefix + g):
            assert c not in seen, (prefix, c, g, seen.get(c))
            seen[c] = g
    assert sorted(seen) == sorted(CUR), (prefix, set(CUR) ^ set(seen))
    if prefix == "func: ":
        FUNC_OF = seen
assert MEMBER_SETS["care C"] == set().union(*[MEMBER_SETS["care-first: " + g] for g in CARE_FIRST
                                               if g.startswith("care: ")])


# %% per-window tables
def nominal(freq, t, agg="line 1"):
    """Signed current-dollar value (as it enters PCE) of an aggregate: the signed sum of its current leaves."""
    ls = members(agg)
    return float((V[freq].loc[t, ls] * SIGN_ROOT[ls]).sum())


def nominal_series(freq, dates, agg):
    ls = members(agg)
    return V[freq].loc[dates, ls].mul(SIGN_ROOT[ls], axis=1).sum(axis=1)


def tag(line, agg):
    ls = DESC_CUR[line]
    k = sum(c in MEMBER_SETS[agg] for c in ls)
    return "yes" if k == len(ls) and k > 0 else ("part" if k > 0 else "no")


def func_tag(line):
    gs = {FUNC_OF[c] for c in DESC_CUR[line]}
    return gs.pop() if len(gs) == 1 else ("mixed" if gs else "")


def bea_growth(freq, line, a, b, table="Q"):
    src = Q[freq] if table == "Q" else X[freq]
    if (line not in src.columns or a not in src.index or b not in src.index
            or pd.isna(src.loc[a, line]) or pd.isna(src.loc[b, line])):     # 2.4.6U starts in 2007
        return np.nan
    return float(src.loc[b, line] / src.loc[a, line] - 1)


def months_between(a, b):
    return (int(b[:4]) - int(a[:4])) * 12 + (int(b[5:]) - int(a[5:]))


def annualize(g, freq, a, b):
    n = months_between(a, b) if freq == "M" else (int(b) - int(a)) * 12
    return (1 + g) ** (12 / n) - 1 if pd.notna(g) else np.nan


line_tables, group_tables, headline_rows = {}, {}, []
for key, freq, a, b, wlabel in tqdm(WINDOWS, desc="windows"):
    C, FQ, FP, AGG, PARTS = CHAIN[freq]
    wc = window_contrib(C, FQ, a, b)                     # contributions, fractions, by component
    total = window_growth(FQ, a, b)
    assert abs(wc.sum() - total) < 1e-12
    pce_a = V[freq].loc[a, 1]
    bea_x = bea_growth(freq, 1, a, b, "X")               # BEA real PCE, chained dollars (2.4.6U line 1)
    resid = bea_x - total

    # --- every line of the main hierarchy
    rows = []
    for l in main["line"].astype(int):
        if pd.isna(V[freq].loc[a, l]) or pd.isna(V[freq].loc[b, l]):
            continue
        contrib = float(wc.reindex(DESC_CUR[l]).fillna(0.0).sum())
        g_ours = np.nan if l in NET_LINES else window_growth(AGG[f"line {l}"], a, b)
        rows.append({
            "window": key, "start": a, "end": b, "line": l, "label": LABEL[l], "level": int(LEVEL[l]),
            "parent_line": PARENT[l], "is_leaf": l in CUR, "sign_to_root": int(SIGN_ROOT[l]),
            "func_group": func_tag(l),
            **{f"care_{k}": tag(l, f"care {k}") for k in CARE_TOPS},
            "imputed": tag(l, "imputed"),
            "start_nominal_musd_signed": SIGN_ROOT[l] * V[freq].loc[a, l],
            "start_nominal_share_pct": 100 * SIGN_ROOT[l] * V[freq].loc[a, l] / pce_a,
            "end_nominal_musd_signed": SIGN_ROOT[l] * V[freq].loc[b, l],
            "real_growth_pct": 100 * g_ours,
            "real_growth_pct_bea_2_4_3U": 100 * bea_growth(freq, l, a, b, "Q"),
            "contribution_pp": 100 * contrib,
            "share_of_growth_pct": 100 * contrib / total,
        })
    lt = pd.DataFrame(rows)
    line_tables[key] = lt
    lt.to_csv(OUT / f"sector_contributions_{window_tag(a, b)}.csv", index=False, float_format="%.12g")

    # --- groups
    grows = []

    def add_group(kind, name, agg, definition, note=""):
        ms = members(agg)
        s0, s1 = nominal(freq, a, agg=agg), nominal(freq, b, agg=agg)
        g = np.nan if AGGS[agg] == ([333], []) else window_growth(AGG[agg], a, b)    # a net: no real growth
        contrib = float(wc.reindex(ms).fillna(0.0).sum())
        grows.append({
            "window": key, "start": a, "end": b, "kind": kind, "group": name, "definition": definition,
            "n_leaves": len(ms), "start_nominal_musd": s0, "start_share_pct": 100 * s0 / pce_a,
            "end_nominal_musd": s1, "nominal_growth_pct": 100 * (s1 / s0 - 1) if s0 != 0 else np.nan,
            "real_growth_pct": 100 * g, "real_growth_annualized_pct": 100 * annualize(g, freq, a, b),
            "contribution_pp": 100 * contrib, "share_of_growth_pct": 100 * contrib / total, "note": note,
        })

    def defn(agg):
        inc, exc = AGGS[agg]
        return "+".join(map(str, inc)) + ("" if not exc else " excl. " + "+".join(map(str, exc)))

    add_group("total", "PCE (leaf Fisher, 243 leaves)", "line 1", "1")
    for g in ["Goods", "Services"]:
        add_group("subtotal", g, f"func: {g}", defn(f"func: {g}"))
    for g in FUNC:
        add_group("functional", g, f"func: {g}", defn(f"func: {g}"), NET_AGGS_NOTE.get(g, ""))
    for k in CARE_TOPS:
        add_group("care", CARE_LABEL[k], f"care {k}", defn(f"care {k}"))
    for g in CARE_PARTS:
        add_group("care part", g, f"care part: {g}", defn(f"care part: {g}"), NET_AGGS_NOTE.get(g, ""))
    for k in CARE_TOPS:
        add_group("outside care", f"Outside care {k}", f"outside care {k}", defn(f"outside care {k}"))
        add_group("outside care and imputed", f"Outside care {k} and imputed items",
                  f"outside care {k} and imputed", defn(f"outside care {k} and imputed"))
    add_group("imputed", "Imputed and non-cash items (160 + 163 + 254 + 342)", "imputed", defn("imputed"))
    add_group("imputed", "Outside imputed items", "outside imputed", defn("outside imputed"))
    for g in CARE_FIRST:
        add_group("care-first partition", g, f"care-first: {g}", defn(f"care-first: {g}"))
    gt = pd.DataFrame(grows)
    # BEA's own real PCE and the residual, as rows
    extra = pd.DataFrame([
        {"window": key, "start": a, "end": b, "kind": "bea", "group": "PCE, BEA chained dollars (2.4.6U line 1)",
         "definition": "2.4.6U line 1", "real_growth_pct": 100 * bea_x,
         "real_growth_annualized_pct": 100 * annualize(bea_x, freq, a, b)},
        {"window": key, "start": a, "end": b, "kind": "residual",
         "group": "Residual: BEA real PCE growth minus leaf-Fisher growth", "definition": "",
         "real_growth_pct": 100 * resid},
    ])
    gt = pd.concat([gt, extra], ignore_index=True)
    group_tables[key] = gt
    gt.to_csv(OUT / f"sector_groups_{window_tag(a, b)}.csv", index=False, float_format="%.12g")

    # --- real personal income excluding transfers (Table 2.6 / 2.1 line 36) over the same window
    pix = PI[freq][36]
    g_pix = float(pix[b] / pix[a] - 1)
    for k in CARE_TOPS:
        row = gt[gt["group"] == CARE_LABEL[k]].iloc[0]
        out_row = gt[gt["group"] == f"Outside care {k}"].iloc[0]
        oi_row = gt[gt["group"] == f"Outside care {k} and imputed items"].iloc[0]
        headline_rows.append({
            "window": key, "label": wlabel, "start": a, "end": b, "care_variant": k, "care_label": CARE_LABEL[k],
            "real_pce_growth_pct_leaf": 100 * total, "real_pce_growth_pct_bea": 100 * bea_x,
            "residual_pp": 100 * resid,
            "care_start_share_of_pce_pct": row["start_share_pct"],
            "care_contribution_pp": row["contribution_pp"],
            "care_share_of_growth_pct": row["share_of_growth_pct"],
            "care_growth_share_over_level_share": row["share_of_growth_pct"] / row["start_share_pct"],
            "care_share_of_nominal_increase_pct": 100 * (row["end_nominal_musd"] - row["start_nominal_musd"])
            / (V[freq].loc[b, 1] - V[freq].loc[a, 1]),
            "care_real_growth_pct": row["real_growth_pct"],
            "care_nominal_growth_pct": row["nominal_growth_pct"],
            "care_implicit_price_change_pct": 100 * ((1 + row["nominal_growth_pct"] / 100)
                                                     / (1 + row["real_growth_pct"] / 100) - 1),
            "pce_implicit_price_change_pct": 100 * ((V[freq].loc[b, 1] / V[freq].loc[a, 1])
                                                    / (X[freq].loc[b, 1] / X[freq].loc[a, 1]) - 1),
            "outside_care_contribution_pp": out_row["contribution_pp"],
            "outside_care_real_growth_pct": out_row["real_growth_pct"],
            "outside_care_real_growth_annualized_pct": out_row["real_growth_annualized_pct"],
            "outside_care_and_imputed_real_growth_pct": oi_row["real_growth_pct"],
            "outside_care_and_imputed_real_growth_annualized_pct": oi_row["real_growth_annualized_pct"],
            "real_pi_ex_transfers_growth_pct": 100 * g_pix,
            "real_pi_ex_transfers_growth_annualized_pct": 100 * annualize(g_pix, freq, a, b),
        })

headline = pd.DataFrame(headline_rows)

# %% the jobs side: the watch page's own chart data (twelve-month changes, thousands), vendored 2026-11-02
html = WATCH_JOBS.read_text(encoding="utf-8")
plot = json.loads(re.search(r'<script type="application/json" id="plot-1">(.*?)</script>', html, re.S).group(1))
JOBS12 = {s["name"]: pd.Series(dict(s["points"])) for s in plot["series"]}   # keys 'YYYY-MM-01'


def jobs_change(name, a, b):
    """Change in jobs over a window that is a whole number of years, as a sum of twelve-month changes."""
    n = months_between(a, b)
    if n % 12:
        return np.nan
    ends = [f"{int(b[:4]) - k}-{b[5:]}-01" for k in range(n // 12)]
    return float(sum(JOBS12[name][e] for e in ends))


jobs_rows = []
JOB_CONTEXT = [("pre4y", "M", "2015-09", "2019-09", "4 years to Sep 2019 (pre-pandemic)"),
               ("covid4y", "M", "2018-09", "2022-09", "4 years to Sep 2022")]
for key, freq, a, b, wlabel in WINDOWS + JOB_CONTEXT:
    if freq != "M" or months_between(a, b) % 12:
        continue
    ch = {nm: jobs_change(nm, a, b) for nm in JOBS12}
    tot = sum(ch.values())
    jobs_rows.append({"window": key, "start": a, "end": b,
                      **{f"jobs_change_k: {nm}": v for nm, v in ch.items()},
                      "jobs_change_k: total": tot,
                      "care_share_of_net_job_growth_pct": 100 * ch["Health care and social assistance"] / tot,
                      "care_share_of_private_job_growth_pct": 100 * ch["Health care and social assistance"]
                      / (ch["Health care and social assistance"] + ch["Private jobs outside care"])})
jobs = pd.DataFrame(jobs_rows)
jobs.to_csv(OUT / "jobs_watch_windows.csv", index=False, float_format="%.12g")
headline = headline.merge(jobs[["window", "care_share_of_net_job_growth_pct",
                                "care_share_of_private_job_growth_pct"]], on="window", how="left")
headline.to_csv(OUT / "headline_sectors.csv", index=False, float_format="%.12g")

# %% monthly series: real PCE, outside care, outside care and imputed, beside real income excl. transfers
BASE = "2022-09"


def index_from(F, start="2007-01"):
    per = [t for t in F.index if t > start]
    return pd.concat([pd.Series({start: 1.0}), F.loc[per].cumprod()])


series = {
    "real_pce_bea": ("Real PCE, BEA chained 2017 dollars (2.4.6U line 1)", X["M"][1].loc["2007-01":], None),
    "real_pce_leaf": ("Real PCE, Fisher index from the 243 leaves", index_from(FQ_M), "line 1"),
}
for k in CARE_TOPS:
    series[f"care_{k}"] = (f"Real care spending, variant {k}", index_from(AGG_M[f"care {k}"]), f"care {k}")
    series[f"outside_care_{k}"] = (f"Real PCE outside care, variant {k}", index_from(AGG_M[f"outside care {k}"]),
                                   f"outside care {k}")
    series[f"outside_care_{k}_and_imputed"] = (f"Real PCE outside care ({k}) and imputed items",
                                               index_from(AGG_M[f"outside care {k} and imputed"]),
                                               f"outside care {k} and imputed")
series["imputed"] = ("Real imputed and non-cash items", index_from(AGG_M["imputed"]), "imputed")
series["real_pi_ex_transfers"] = ("Real personal income excl. current transfer receipts (Table 2.6 line 36)",
                                  PI["M"][36].loc["2007-01":], None)
mon = []
for name, (lab, s, agg) in series.items():
    s = s.loc["2007-01":]
    df = pd.DataFrame({"date": s.index, "series": name, "label": lab,
                       "index_2022_09_100": (100 * s / s[BASE]).values,
                       "pct_change_1m": (100 * s.pct_change()).values,
                       "pct_change_6m": (100 * (s / s.shift(6) - 1)).values,
                       "pct_change_12m": (100 * (s / s.shift(12) - 1)).values})
    if agg is not None:
        df["nominal_musd_saar"] = nominal_series("M", list(s.index), agg).values
    elif name == "real_pce_bea":
        df["nominal_musd_saar"] = V["M"].loc[s.index, 1].values
    else:
        df["nominal_musd_saar"] = (PI["M"].loc[s.index, 1] - PI["M"].loc[s.index, 16]).values
    mon.append(df)
monthly = pd.concat(mon, ignore_index=True)
monthly.to_csv(OUT / "outside_care_monthly.csv", index=False, float_format="%.12g")

# %% financing: care spending against Medicare + Medicaid, and the spending-over-income gap
fin = []
HEALTH = ["A", "A+", "B", "C", "C+", "S"]
PIX = "Personal income excl. transfers (PI - line 16)"
MM = "Medicare + Medicaid (19 + 20)"
OTHER_TR = "Other social benefits (21-23) and transfers from business (24)"


def pi_level(freq, item, t):
    pi_ = PI[freq]
    if item.startswith("care "):
        return nominal(freq, t, agg=item)
    return {
        "PCE": V[freq].loc[t, 1],
        PIX: pi_.loc[t, 1] - pi_.loc[t, 16],
        "Personal current transfer receipts (16)": pi_.loc[t, 16],
        "Government social benefits (17)": pi_.loc[t, 17],
        "Social security (18)": pi_.loc[t, 18],
        "Medicare (19)": pi_.loc[t, 19],
        "Medicaid (20)": pi_.loc[t, 20],
        MM: pi_.loc[t, 19] + pi_.loc[t, 20],
        OTHER_TR: pi_.loc[t, 16] - pi_.loc[t, 18] - pi_.loc[t, 19] - pi_.loc[t, 20],
        "Personal current taxes (26)": pi_.loc[t, 26],
        "Personal interest payments (30)": pi_.loc[t, 30],
        "Personal current transfer payments (31)": pi_.loc[t, 31],
        "Personal saving (34)": pi_.loc[t, 34],
    }[item]


for key, freq, a, b, wlabel in WINDOWS:
    def lvl(item, t):
        return pi_level(freq, item, t)

    def d(item):
        return lvl(item, b) - lvl(item, a)

    base = {"window": key, "start": a, "end": b}
    items = (["PCE"] + [f"care {k}" for k in HEALTH] +
             [PIX, "Personal current transfer receipts (16)", "Government social benefits (17)",
              "Social security (18)", "Medicare (19)", "Medicaid (20)", MM, OTHER_TR, "Personal current taxes (26)",
              "Personal interest payments (30)", "Personal current transfer payments (31)", "Personal saving (34)"])
    gY = lvl(PIX, b) / lvl(PIX, a) - 1                  # nominal growth of income excl. transfers
    c0, c1 = lvl("PCE", a), lvl("PCE", b)
    excess_total = c1 - c0 * (1 + gY)                   # spending above what it would be at the income growth rate
    for it in items:
        s0, s1 = lvl(it, a), lvl(it, b)
        name = CARE_LABEL[it.split(" ", 1)[1]] if it.startswith("care ") else it
        spend_like = it == "PCE" or it.startswith("care ") or it.startswith("Medic")
        fin.append({**base, "block": "levels", "item": name, "start_musd": s0, "end_musd": s1,
                    "increment_musd": s1 - s0, "growth_pct": 100 * (s1 / s0 - 1),
                    "share_of_pce_at_start_pct": 100 * s0 / c0,
                    "excess_over_income_growth_musd": s1 - s0 * (1 + gY),
                    "share_of_spending_excess_pct": 100 * (s1 - s0 * (1 + gY)) / excess_total if spend_like
                    else np.nan})
    # the identity behind the gap: dPCE = dY + dTransfers - dTaxes - dInterest - dTransfer payments - dSaving
    dC = c1 - c0
    bridge = {
        "Personal income excl. transfers": d(PIX),
        "+ Medicare + Medicaid": d(MM),
        "+ Social security": d("Social security (18)"),
        "+ Other transfer receipts": d(OTHER_TR),
        "- Personal current taxes": -d("Personal current taxes (26)"),
        "- Interest and transfer payments": -(d("Personal interest payments (30)")
                                              + d("Personal current transfer payments (31)")),
        "- Personal saving": -d("Personal saving (34)"),
    }
    bsum = sum(bridge.values())
    for it, val in bridge.items():
        fin.append({**base, "block": "bridge", "item": it, "increment_musd": val,
                    "share_of_pce_increment_pct": 100 * val / dC})
    fin.append({**base, "block": "bridge", "item": "= Change in PCE (sum of the above)", "increment_musd": bsum,
                "share_of_pce_increment_pct": 100 * bsum / dC})
    fin.append({**base, "block": "bridge", "item": "Change in PCE (published)", "increment_musd": dC,
                "share_of_pce_increment_pct": 100.0})
    # gap decomposition: g_C - g_Y = s_M (g_M - g_Y) + (1 - s_M)(g_R - g_Y), nominal; shares are deflator-free
    gC = c1 / c0 - 1
    gx = bea_growth(freq, 1, a, b, "X")
    gyr = float(PI[freq][36][b] / PI[freq][36][a] - 1)
    gap_rows = [("Real PCE growth, % (2.4.6U line 1)", 100 * gx),
                ("Real personal income excl. transfers growth, % (line 36)", 100 * gyr),
                ("Real gap, pp", 100 * (gx - gyr)),
                ("Nominal PCE growth, %", 100 * gC),
                ("Nominal personal income excl. transfers growth, %", 100 * gY),
                ("Nominal gap, pp", 100 * (gC - gY)),
                ("Spending excess over income growth, $mn SAAR: C1 - C0(1 + gY)", excess_total)]
    # shares of the gap are only meaningful when spending clearly outgrew income (2022-2025 annual: it did not)
    share_ok = (gC - gY) > 0.0025 and (gx - gyr) > 0.0025
    for it in [MM] + [f"care {k}" for k in HEALTH]:
        s0, s1 = lvl(it, a), lvl(it, b)
        part_pp = (s0 / c0) * (s1 / s0 - 1 - gY)
        name = CARE_LABEL[it.split(" ", 1)[1]] if it.startswith("care ") else it
        gap_rows += [(f"Part of nominal gap from {name}: s0 (g - gY), pp", 100 * part_pp),
                     (f"Share of the nominal gap from {name}, %", 100 * part_pp / (gC - gY) if share_ok else np.nan)]
    gap_rows.append(("Gross upper bound: increase in Medicare + Medicaid / (increase in PCE - increase in income "
                     "excl. transfers), %", 100 * d(MM) / (dC - d(PIX)) if share_ok else np.nan))
    # care's part of the real gap, from the Fisher contributions: contribution - start share x real income growth
    gt = group_tables[key]
    gap_leaf = 100 * window_growth(CHAIN[freq][1], a, b) - 100 * gyr
    for k in HEALTH:
        row = gt[gt["group"] == CARE_LABEL[k]].iloc[0]
        part_r = row["contribution_pp"] - row["start_share_pct"] * gyr
        gap_rows += [(f"Part of real gap from {CARE_LABEL[k]}: contribution - s0 x real income growth, pp", part_r),
                     (f"Share of the real gap from {CARE_LABEL[k]}, % (gap on the leaf Fisher)",
                      100 * part_r / gap_leaf if share_ok else np.nan)]
    for it, val in gap_rows:
        fin.append({**base, "block": "gap", "item": it, "value": val})
financing = pd.DataFrame(fin)
financing.to_csv(OUT / "care_financing.csv", index=False, float_format="%.12g")

# %% cross-checks against BEA's published contributions
wb = openpyxl.load_workbook(SURVEY_XLSX, read_only=True, data_only=True)


def published(sheet):
    """Rows of a published contributions sheet: {line: (label, code, Series by period)}."""
    rows = list(wb[sheet].iter_rows(values_only=True))
    hdr = [str(h) for h in rows[7]]
    per = [h.replace("M", "-") if re.fullmatch(r"\d{4}M\d{2}", h) else h for h in hdr[3:]]
    out = {}
    for r in rows[8:]:
        if r[0] is None or not str(r[0]).strip().isdigit():
            continue
        lab = re.sub(r"\\\d+\\", "", str(r[1])).strip()
        out[int(r[0])] = (lab, r[2], pd.to_numeric(pd.Series(list(r[3:]), index=per), errors="coerce"))
    return out


T282, T232, T242 = published("T20802-M"), published("T20302-A"), published("T20402-A")


def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", str(s).lower()).strip()


def map_published(pub):
    """Map published lines to 2.4.5U lines by label, in table order (labels repeat in the U table only where
    the order disambiguates them)."""
    ulab = {int(l): norm(LABEL[l]) for l in main["line"]}
    out, last = {}, 0
    for pl, (lab, code, ser) in pub.items():
        n = norm(lab).replace("personal consumption expenditures pce", "personal consumption expenditures")
        cands = sorted(l for l, s in ulab.items() if s == n)
        pick = [l for l in cands if l > last] or cands
        if pick:
            out[pl] = pick[0]
            last = pick[0]
    return out


comp_rows, conventions = [], {}
for sheet, pub, freq, lo, hi in [("T20802-M", T282, "M", "2022-01", "2026-09"),
                                  ("T20302-A", T232, "A", "1960", "2025"),
                                  ("T20402-A", T242, "A", "1960", "2025")]:
    mp = map_published(pub)
    C = CHAIN[freq][0]
    for pl, ul in mp.items():
        if pl == 1:
            continue
        lab, code, ser = pub[pl]
        ls = [c for c in C.columns if is_under(c, ul)]
        ours = 100 * C.loc[lo:hi, ls].fillna(0.0).sum(axis=1)
        pubv = ser.reindex(ours.index)
        # BEA prints some 'Less:' lines unsigned (receipts of nonprofits) and others signed (nonresidents' spending)
        conv = "signed"
        if SIGN_ROOT[ul] < 0 and (pubv + ours).abs().max() < (pubv - ours).abs().max():
            conv = "unsigned"
            ours = -ours
        conventions[(sheet, pl)] = conv
        parts = CHAIN[freq][4]
        for t in ours.index:
            # skip periods whose partition cannot resolve this line (a coarser line is the component, e.g. 281 in
            # 1987 when 289 starts): there the line's own contribution is not identified from the published detail
            if any(c != ul and is_under(ul, c) for c in parts[t]):
                continue
            if pd.notna(pubv.get(t)):
                comp_rows.append({"table": sheet, "period": t, "pub_line": pl, "u_line": ul, "label": lab,
                                  "code": code, "convention": conv, "ours_pp": ours[t], "published_pp": pubv[t],
                                  "diff_pp": ours[t] - pubv[t]})
comp = pd.DataFrame(comp_rows)
comp.to_csv(OUT / "published_comparison.csv", index=False, float_format="%.12g")
UNMAPPED = {sheet: sorted(set(pub) - set(map_published(pub)))
            for sheet, pub in [("T20802-M", T282), ("T20302-A", T232), ("T20402-A", T242)]}

# window-level: BEA's published monthly (2.8.2) and annual (2.3.2) contributions chained with BEA's own index
wrows = []
for key, freq, a, b, wlabel in WINDOWS:
    sheet, pub = ("T20802-M", T282) if freq == "M" else ("T20302-A", T232)
    bx = X[freq][1]
    per = [t for t in bx.index if a < t <= b]
    w = (bx.loc[per] / bx[a]).shift(1).fillna(1.0)
    wc = window_contrib(CHAIN[freq][0], CHAIN[freq][1], a, b)
    for pl, ul in map_published(pub).items():
        if pl == 1:
            continue
        lab, code, ser = pub[pl]
        sgn = -1 if conventions.get((sheet, pl)) == "unsigned" else 1
        ours = 100 * float(wc.reindex(DESC_CUR[ul]).fillna(0).sum())
        pubw = float((ser.reindex(per) * w).sum())
        wrows.append({"window": key, "start": a, "end": b, "table": sheet, "pub_line": pl, "u_line": ul,
                      "label": lab, "ours_pp": sgn * ours, "published_chained_pp": pubw,
                      "diff_pp": sgn * ours - pubw, "n_periods": len(per)})
wcomp = pd.DataFrame(wrows)
wcomp.to_csv(OUT / "published_comparison_windows.csv", index=False, float_format="%.12g")

# %% the leaf-Fisher index against BEA, period by period (for the residual discussion)
res_rows = []
for freq in "MA":
    F, parts = CHAIN[freq][1], CHAIN[freq][4]
    for t in F.index:
        prev = Q[freq].index[Q[freq].index.get_loc(t) - 1]
        xch = (100 * (X[freq].loc[t, 1] / X[freq].loc[prev, 1] - 1)
               if prev in X[freq].index and t in X[freq].index else np.nan)
        res_rows.append({"freq": freq, "period": t, "leaf_fisher_pct": 100 * (F[t] - 1),
                         "bea_quantity_index_pct": 100 * (Q[freq].loc[t, 1] / Q[freq].loc[prev, 1] - 1),
                         "bea_chained_dollars_pct": xch, "n_components": len(parts[t])})
resid_tab = pd.DataFrame(res_rows)
resid_tab["diff_vs_chained_pp"] = resid_tab["leaf_fisher_pct"] - resid_tab["bea_chained_dollars_pct"]
resid_tab["diff_vs_qindex_pp"] = resid_tab["leaf_fisher_pct"] - resid_tab["bea_quantity_index_pct"]
resid_tab.to_csv(OUT / "leaf_fisher_vs_bea.csv", index=False, float_format="%.12g")

# %% context: care's share of real PCE growth before the four-year window (annual data from 1990; two
# pre-pandemic monthly windows). Uses each period's own partition; a care variant is skipped in a period whose
# partition cannot separate it (never the case from 1988 on).
def care_contrib_period(freq, t, tops):
    part = CHAIN[freq][4][t]
    if any(tp != c and is_under(tp, c) for tp in tops for c in part):
        return np.nan
    ms = [c for c in part if any(is_under(c, tp) for tp in tops)]
    return float(CHAIN[freq][0].loc[t, ms].sum())


def care_level(freq, t, tops):
    ls = [c for c in CUR if any(is_under(c, tp) for tp in tops)]
    vals = V[freq].loc[t, ls]
    return np.nan if vals.isna().any() else float((vals * SIGN_ROOT[ls]).sum() / V[freq].loc[t, 1])


hist = []
years = [str(y) for y in range(1990, 2026)]
for y in years:
    prev = str(int(y) - 1)
    row = {"period": y, "kind": "year", "real_pce_growth_pct": 100 * (FQ_A[y] - 1),
           "real_pi_ex_transfers_growth_pct": 100 * (PI["A"].loc[y, 36] / PI["A"].loc[prev, 36] - 1)}
    for k in ["A+", "B", "C"]:
        c = care_contrib_period("A", y, CARE_TOPS[k])
        row[f"care_{k}_share_of_level_pct"] = 100 * care_level("A", prev, CARE_TOPS[k])
        row[f"care_{k}_contribution_pp"] = 100 * c
        row[f"care_{k}_share_of_growth_pct"] = 100 * c / (FQ_A[y] - 1)
        row[f"care_{k}_share_of_nominal_increase_pct"] = 100 * (care_level("A", y, CARE_TOPS[k]) * V["A"].loc[y, 1]
                                                               - care_level("A", prev, CARE_TOPS[k])
                                                               * V["A"].loc[prev, 1]) / (V["A"].loc[y, 1]
                                                                                         - V["A"].loc[prev, 1])
        row[f"outside_care_{k}_real_growth_pct"] = 100 * (AGG_A.loc[y, f"outside care {k}"] - 1)
    hist.append(row)
for kind, freq, a, b in [("window", "A", "2010", "2019"), ("window", "A", "2015", "2019"),
                         ("window", "M", "2015-09", "2019-09"), ("window", "M", "2018-09", "2022-09"),
                         ("window", "M", "2022-09", "2026-09")]:
    C, FQ = CHAIN[freq][0], CHAIN[freq][1]
    wc = window_contrib(C, FQ, a, b)
    tot = window_growth(FQ, a, b)
    row = {"period": f"{a} to {b}", "kind": kind, "real_pce_growth_pct": 100 * tot,
           "real_pi_ex_transfers_growth_pct": 100 * (PI[freq].loc[b, 36] / PI[freq].loc[a, 36] - 1)}
    for k in ["A+", "B", "C"]:
        # window contributions summed over each period's own care components (partitions are constant here)
        per = [t for t in FQ.index if a < t <= b]
        assert len({CHAIN[freq][4][t] for t in per}) == 1 or freq == "A"
        ms = [c for c in CHAIN[freq][4][per[-1]] if any(is_under(c, tp) for tp in CARE_TOPS[k])]
        c = float(wc.reindex(ms).fillna(0.0).sum())
        row[f"care_{k}_share_of_level_pct"] = 100 * care_level(freq, a, CARE_TOPS[k])
        row[f"care_{k}_contribution_pp"] = 100 * c
        row[f"care_{k}_share_of_growth_pct"] = 100 * c / tot
        row[f"care_{k}_share_of_nominal_increase_pct"] = 100 * (care_level(freq, b, CARE_TOPS[k]) * V[freq].loc[b, 1]
                                                               - care_level(freq, a, CARE_TOPS[k])
                                                               * V[freq].loc[a, 1]) / (V[freq].loc[b, 1]
                                                                                       - V[freq].loc[a, 1])
        row[f"outside_care_{k}_real_growth_pct"] = 100 * window_growth(CHAIN[freq][3][f"outside care {k}"], a, b)
    hist.append(row)
history = pd.DataFrame(hist)
history.to_csv(OUT / "care_share_history.csv", index=False, float_format="%.12g")


# The same periods against BEA's own real PCE (2.4.6U chained dollars, from 2007): the residual of the leaf Fisher and
# care's share of growth on BEA's total. The monthly context windows are unadjusted chains, like the five windows, and
# across 2020 they drift (Table 4's last columns). A separate file, so care_share_history.csv keeps its columns.
def period_bounds(per_):
    if " to " not in per_:
        return "A", str(int(per_) - 1), per_
    a, b = per_.split(" to ")
    return ("M" if len(a) == 7 else "A"), a, b


hb_rows = []
for r in history.itertuples():
    freq, a, b = period_bounds(r.period)
    bea = bea_growth(freq, 1, a, b, "X")
    leaf = r.real_pce_growth_pct / 100
    row = {"period": r.period, "kind": r.kind, "freq": freq, "start": a, "end": b,
           "real_pce_growth_pct_leaf": 100 * leaf, "real_pce_growth_pct_bea": 100 * bea,
           "residual_pp": 100 * (bea - leaf)}
    for k in ["A+", "B", "C"]:
        row[f"care_{k}_share_of_bea_growth_pct"] = (history.loc[r.Index, f"care_{k}_contribution_pp"] / bea
                                                    if pd.notna(bea) else np.nan)
    hb_rows.append(row)
history_bea = pd.DataFrame(hb_rows)
history_bea.to_csv(OUT / "care_share_history_bea.csv", index=False, float_format="%.12g")


# %% care in dollars: its share of the PCE level at both ends of a window, in current dollars and at start-of-window
# prices, and why its share of the dollar increase sits below its share of real growth. A share of a dollar increase
# contains the price increase on everything, which accrues to each item in proportion to its level and so pulls the
# dollar share toward the level share. The counterfactual "care prices rose as fast as all PCE prices" (care's own real
# growth, BEA's implicit PCE deflator, everything else as published) splits
#     share of real growth - share of the dollar increase = (general inflation) + (relative prices).
def care_dollar_split(freq, a, b, k):
    C, FQ, FP, AGG, PARTS = CHAIN[freq]
    G = window_growth(FQ, a, b)
    contrib = float(window_contrib(C, FQ, a, b).reindex(members(f"care {k}")).fillna(0.0).sum())
    g_c = window_growth(AGG[f"care {k}"], a, b)
    p0, p1 = V[freq].loc[a, 1], V[freq].loc[b, 1]
    c0, c1 = nominal(freq, a, f"care {k}"), nominal(freq, b, f"care {k}")
    px = (p1 / p0) / (X[freq].loc[b, 1] / X[freq].loc[a, 1]) - 1          # BEA's implicit PCE price change
    c1_eq = c0 * (1 + g_c) * (1 + px)                                    # care's end value at all-PCE price growth
    real_share, nom_share = 100 * contrib / G, 100 * (c1 - c0) / (p1 - p0)
    eq_share = 100 * (c1_eq - c0) / (p1 - p0 + c1_eq - c1)
    s0, s1 = 100 * c0 / p0, 100 * c1 / p1
    s1v = s0 * (1 + g_c) / (1 + G)                                       # end volumes, both at start-of-window prices
    return {"start_share_of_pce_pct": s0, "end_share_of_pce_pct": s1, "share_change_pp": s1 - s0,
            "end_share_at_start_prices_pct": s1v, "share_change_at_start_prices_pp": s1v - s0,
            "share_of_real_growth_pct": real_share, "share_of_nominal_increase_pct": nom_share,
            "share_of_nominal_increase_if_care_prices_as_pce_pct": eq_share,
            "real_minus_nominal_share_pp": real_share - nom_share,
            "of_which_general_inflation_pp": real_share - eq_share,
            "of_which_relative_prices_pp": eq_share - nom_share,
            "care_real_growth_pct": 100 * g_c, "care_price_change_pct": 100 * ((c1 / c0) / (1 + g_c) - 1),
            "pce_price_change_pct": 100 * px, "real_pce_growth_pct_leaf": 100 * G}


DOLLAR_WINDOWS = WINDOWS + JOB_CONTEXT + [("7y", "M", "2019-09", "2026-09", "7 years to Sep 2026 (from pre-pandemic)")]
dollar_rows = [{"window": key, "label": wlabel, "start": a, "end": b, "care_variant": k, "care_label": CARE_LABEL[k],
                **care_dollar_split(freq, a, b, k)}
               for key, freq, a, b, wlabel in DOLLAR_WINDOWS for k in CARE_TOPS]
dollar_split = pd.DataFrame(dollar_rows)
dollar_split.to_csv(OUT / "care_dollar_shares.csv", index=False, float_format="%.12g")


# %% when the spending-income gap opened, care (c): Sep 2022 to Mar 2026, the watch window, and the four years. Same
# arithmetic as the gap block above: in volumes, care's part is its contribution minus its start share times real
# income growth (gap on the leaf Fisher); in dollars, s0 (g_care - g_Y).
GAP_TIMING = [("pre", "2022-09", "2026-03", "Sep 2022 to Mar 2026"),
              ("6m", "2026-03", "2026-09", "Mar 2026 to Sep 2026 (watch window)"),
              ("4y", "2022-09", "2026-09", "Sep 2022 to Sep 2026 (4 years)")]
gt_rows = []
for key, a, b, plabel in GAP_TIMING:
    C, FQ, FP, AGG, PARTS = CHAIN["M"]
    G = window_growth(FQ, a, b)
    contrib = float(window_contrib(C, FQ, a, b).reindex(members("care C")).fillna(0.0).sum())
    p0, p1 = V["M"].loc[a, 1], V["M"].loc[b, 1]
    c0, c1 = nominal("M", a, "care C"), nominal("M", b, "care C")
    s0 = c0 / p0
    gx = bea_growth("M", 1, a, b, "X")
    gyr = float(PI["M"].loc[b, 36] / PI["M"].loc[a, 36] - 1)
    y0, y1 = PI["M"].loc[a, 1] - PI["M"].loc[a, 16], PI["M"].loc[b, 1] - PI["M"].loc[b, 16]
    gY, gC = y1 / y0 - 1, p1 / p0 - 1
    care_r, care_n = contrib - s0 * gyr, s0 * (c1 / c0 - 1 - gY)
    ok = (gC - gY) > 0.0025 and (gx - gyr) > 0.0025                     # the same rule as Table 9
    gt_rows.append({"period": key, "label": plabel, "start": a, "end": b,
                    "real_pce_growth_pct_bea": 100 * gx, "real_pce_growth_pct_leaf": 100 * G,
                    "real_pi_ex_transfers_growth_pct": 100 * gyr, "real_gap_pp_bea": 100 * (gx - gyr),
                    "real_gap_pp_leaf": 100 * (G - gyr), "care_C_part_of_real_gap_pp": 100 * care_r,
                    "outside_care_C_part_of_real_gap_pp": 100 * (G - gyr - care_r),
                    "care_C_share_of_real_gap_pct": 100 * care_r / (G - gyr) if ok else np.nan,
                    "nominal_pce_growth_pct": 100 * gC, "nominal_pi_ex_transfers_growth_pct": 100 * gY,
                    "nominal_gap_pp": 100 * (gC - gY), "care_C_part_of_nominal_gap_pp": 100 * care_n,
                    "outside_care_C_part_of_nominal_gap_pp": 100 * (gC - gY - care_n),
                    "care_C_share_of_nominal_gap_pct": 100 * care_n / (gC - gY) if ok else np.nan,
                    "care_C_real_growth_pct": 100 * window_growth(AGG["care C"], a, b),
                    "outside_care_C_real_growth_pct": 100 * window_growth(AGG["outside care C"], a, b)})
gap_timing = pd.DataFrame(gt_rows)
gap_timing.to_csv(OUT / "gap_timing.csv", index=False, float_format="%.12g")
GAP_PATH = (X["M"][1] / X["M"].loc["2022-09", 1] - PI["M"][36] / PI["M"].loc["2022-09", 36]).loc["2022-09":]
GAP_MIN = (GAP_PATH.idxmin(), 100 * GAP_PATH.min())                    # income furthest ahead of spending


# %% leaves: the quantity relative implied by 2.4.5U / 2.4.4U against BEA's 2.4.3U relative, month by month
# (BEA's monthly detail indexes carry the temporal adjustment, and the published values and prices are rounded)
def vp_vs_q(freq, lo):
    dates = V[freq].index.tolist()
    rows = []
    for t0, t1 in zip(dates[:-1], dates[1:]):
        if t1 < lo:
            continue
        v0, v1 = V[freq].loc[t0, CUR], V[freq].loc[t1, CUR]
        rel = (v1 / v0) / (P[freq].loc[t1, CUR] / P[freq].loc[t0, CUR]) / (Q[freq].loc[t1, CUR] / Q[freq].loc[t0, CUR])
        rows.append((100 * (rel - 1).abs()).where(v0 != 0).rename(t1))
    return pd.DataFrame(rows)


vq22, vq07 = vp_vs_q("M", "2022-01"), vp_vs_q("M", "2007-02")
leaf_vq = pd.DataFrame({"line": CUR, "label": [LABEL[c] for c in CUR],
                        "max_gap_pct_monthly_since_2022_01": vq22.max().values,
                        "month_of_max_since_2022_01": vq22.idxmax().values,
                        "max_gap_pct_monthly_since_2007_02": vq07.max().values,
                        "month_of_max_since_2007_02": vq07.idxmax().values})
leaf_vq = leaf_vq.sort_values("max_gap_pct_monthly_since_2022_01", ascending=False)
leaf_vq.to_csv(OUT / "leaf_vp_vs_q.csv", index=False, float_format="%.12g")

# %% figures (dataviz skill: reference palette, light surface, hairline grid, thin marks, legend + direct labels)
import matplotlib                                       # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt                         # noqa: E402
from matplotlib.lines import Line2D                     # noqa: E402
from matplotlib.patches import PathPatch, Patch         # noqa: E402
from matplotlib.path import Path as MPath               # noqa: E402

SURFACE, INK, INK2, MUTED = "#fcfcfb", "#0b0b0b", "#52514e", "#898781"
GRID, AXIS, BAND, GRAYBAR = "#e1e0d9", "#c3c2b7", "#f0efec", "#b5b3ab"
SLOT = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]      # categorical slots 1-4 (validated, adjacent pairs)
DPI = 200
PX = DPI / 96                                            # one CSS pixel in device pixels at this dpi
plt.rcParams.update({"font.family": "sans-serif", "font.size": 8.5, "axes.edgecolor": AXIS,
                     "axes.labelcolor": INK2, "xtick.color": MUTED, "ytick.color": INK2,
                     "axes.titlecolor": INK, "figure.facecolor": SURFACE, "axes.facecolor": SURFACE,
                     "savefig.facecolor": SURFACE, "legend.frameon": False, "figure.dpi": DPI})
SRC_BEA = "Source: BEA NIPA Tables 2.4.3U-2.4.6U and 2.6, September 2026 data released 2026-10-29."


def style(ax, grid_axis="y"):
    ax.set_facecolor(SURFACE)
    for s in ["top", "right", "left"]:
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(AXIS)
    ax.spines["bottom"].set_linewidth(0.75)
    ax.grid(axis=grid_axis, color=GRID, linewidth=0.6, linestyle="-")
    ax.set_axisbelow(True)
    ax.tick_params(length=0)


def fig_text(fig, x, y, s, right=0.985, **kw):
    """Left-aligned figure text, word-wrapped against its rendered width so it never runs off the figure."""
    r = fig.canvas.get_renderer()
    out = []
    for para in s.split("\n"):
        cur = ""
        for w in para.split(" "):
            trial = (cur + " " + w).strip()
            t = fig.text(x, y, trial, **kw)
            wide_ = t.get_window_extent(renderer=r).width / fig.bbox.width > right - x
            t.remove()
            if wide_ and cur:
                out.append(cur)
                cur = w
            else:
                cur = trial
        out.append(cur)
    return fig.text(x, y, "\n".join(out), ha="left", va="top", **kw)


def header(fig, blocks, x=0.012, top=0.975, gap=0.012):
    """Stack text blocks [(text, kwargs), ...] from the top of the figure; returns the bottom (figure fraction)."""
    r = fig.canvas.get_renderer()
    y = top
    for s_, kw in blocks:
        t = fig_text(fig, x, y, s_, **kw)
        y = t.get_window_extent(renderer=r).y0 / fig.bbox.height - gap
    return y


def rounded_hbar(ax, y, x, h, color, r_css=4):
    """Horizontal bar from 0 to x, height h (data units), rounded data end (r_css CSS px), square at the baseline.
    The figure must be drawn at its save dpi before this is called, so the pixel transforms are the final ones."""
    t = ax.transData
    ppx = abs(t.transform((1, 0))[0] - t.transform((0, 0))[0])      # device px per x unit
    ppy = abs(t.transform((0, 1))[1] - t.transform((0, 0))[1])
    rx, ry = min(r_css * PX / ppx, abs(x) / 2), min(r_css * PX / ppy, h / 2)
    s = 1 if x >= 0 else -1
    y0, y1 = y - h / 2, y + h / 2
    verts = [(0, y0), (x - s * rx, y0), (x, y0), (x, y0 + ry), (x, y1 - ry), (x, y1), (x - s * rx, y1),
             (0, y1), (0, y0)]
    codes = [MPath.MOVETO, MPath.LINETO, MPath.CURVE3, MPath.CURVE3, MPath.LINETO, MPath.CURVE3, MPath.CURVE3,
             MPath.LINETO, MPath.CLOSEPOLY]
    ax.add_patch(PathPatch(MPath(verts, codes), facecolor=color, edgecolor="none"))


# Figure 1: care's share of real spending growth against its share of spending, by window and definition
ROWS = ["pre4y", "4y", "annual", "jobs", "12m", "6m"]
ROWLAB = {"pre4y": "4 years to Sep 2019 (pre-pandemic)", "4y": "4 years to Sep 2026",
          "annual": "2022 to 2025 (annual)", "jobs": "Aug 2024 to Aug 2026 (jobs)",
          "12m": "12 months to Sep 2026", "6m": "6 months to Sep 2026 (watch)"}
hz_ = history.set_index("period")


def fig1_values(k, w):
    """(share of level, share of growth) for care variant k in row w; the pre-pandemic row comes from history."""
    if w == "pre4y":
        r = hz_.loc["2015-09 to 2019-09"]
        return r[f"care_{k}_share_of_level_pct"], r[f"care_{k}_share_of_growth_pct"]
    h_ = headline[(headline.care_variant == k) & (headline.window == w)].iloc[0]
    return h_["care_start_share_of_pce_pct"], h_["care_share_of_growth_pct"]


PANELS = [("A+", "(a+) Health care services\nincl. NPISH health"),             # the NOTES' names: (a) is 172 alone
          ("B", "(b) (a+) + medical goods\nand net health insurance"),
          ("C", "(c) (b) + child care\nand social assistance")]
fig, axes = plt.subplots(1, 3, figsize=(10.4, 5.5), sharey=True)
fig.subplots_adjust(left=0.215, right=0.985, top=0.64, bottom=0.15, wspace=0.10)   # top is reset below the header
jobs_share = jobs.set_index("window")["care_share_of_net_job_growth_pct"]
for ax, (k, ttl) in zip(axes, PANELS):
    style(ax, grid_axis="x")
    for i, w in enumerate(ROWS):
        y = len(ROWS) - 1 - i + (0.35 if w == "pre4y" else 0.0)     # set the pre-pandemic row slightly apart
        lv, gr = fig1_values(k, w)
        ax.plot([lv, gr], [y, y], color=AXIS, linewidth=1.5, solid_capstyle="round", zorder=2)
        ax.plot(lv, y, "o", ms=6.5, color=MUTED, mec=SURFACE, mew=1.2, zorder=3)
        ax.plot(gr, y, "o", ms=6.5, color=SLOT[0], mec=SURFACE, mew=1.2, zorder=4)
        ax.annotate(f"{lv:.0f}%", (lv, y), xytext=(0, -9), textcoords="offset points", ha="center", va="top",
                    fontsize=7.0, color=MUTED)
        jv = jobs_share[w] if (w in jobs_share.index and pd.notna(jobs_share[w])) else None
        close = jv is not None and abs(jv - gr) < 12          # labels would collide: split them left and right
        g_dx, g_ha = ((4, "left") if gr >= jv else (-4, "right")) if close else (0, "center")
        ax.annotate(f"{gr:.0f}%", (gr, y), xytext=(g_dx, 6), textcoords="offset points", ha=g_ha, va="bottom",
                    fontsize=7.8, color=INK)
        if jv is not None:
            ax.plot(jv, y, "D", ms=6, color=SLOT[1], mec=SURFACE, mew=1.2, zorder=4)
            j_dx, j_ha = ((4, "left") if jv > gr else (-4, "right")) if close else (0, "center")
            ax.annotate(f"{jv:.0f}%", (jv, y), xytext=(j_dx, 6), textcoords="offset points",
                        ha=j_ha, va="bottom", fontsize=7.8, color=INK)
    ax.set_xlim(0, 118)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xticklabels(["0%", "25%", "50%", "75%", "100%"])
    ax.set_ylim(-0.7, len(ROWS) - 0.05)
    ax.axhline(len(ROWS) - 1.5 + 0.15, color=GRID, linewidth=0.6)
    ax.set_title(ttl, loc="left", fontsize=8.6, color=INK, pad=6)
axes[0].set_yticks([len(ROWS) - 1 - i + (0.35 if w == "pre4y" else 0.0) for i, w in enumerate(ROWS)])
axes[0].set_yticklabels([ROWLAB[w] for w in ROWS], fontsize=8.2)
hC = headline[headline.care_variant == "C"].set_index("window")
js = jobs.set_index("window")["care_share_of_net_job_growth_pct"]
pre_c = hz_.loc["2015-09 to 2019-09", "care_C_share_of_growth_pct"]
y_head = header(fig, [
    (f"Care's share of real spending growth rose from {pre_c:.0f}% before the pandemic to about 40%; its share "
     "of job growth rose much further", dict(fontsize=11, color=INK, fontweight="bold")),
    (f"Under definition (c) care was {hC['care_start_share_of_pce_pct'].min():.0f}-"
     f"{hC['care_start_share_of_pce_pct'].max():.0f}% of PCE at the start of each recent window and took "
     f"{hC['care_share_of_growth_pct'].min():.0f}-{hC['care_share_of_growth_pct'].max():.0f}% of real PCE "
     f"growth, against {pre_c:.0f}% in the four years to Sep 2019. Health care and social assistance took "
     f"{js['pre4y']:.0f}% of net job growth in the four years to Sep 2019, {js['4y']:.0f}% in the four years to "
     f"Sep 2026 and {js['jobs']:.0f}% in the two years to Aug 2026.", dict(fontsize=8.4, color=INK2))])
handles = [Line2D([], [], marker="o", ls="", ms=6.5, color=MUTED, mec=SURFACE,
                  label="Care's share of PCE at the start of the window (current dollars)"),
           Line2D([], [], marker="o", ls="", ms=6.5, color=SLOT[0], mec=SURFACE,
                  label="Care's share of real PCE growth (exact Fisher contributions)"),
           Line2D([], [], marker="D", ls="", ms=6, color=SLOT[1], mec=SURFACE,
                  label="Health care and social assistance share of net job growth (watch site; BLS)")]
leg = fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.005, y_head), ncol=2, fontsize=7.8,
                 handletextpad=0.3, columnspacing=1.6, labelcolor=INK2)
y_leg = leg.get_window_extent(renderer=fig.canvas.get_renderer()).y0 / fig.bbox.height
fig.subplots_adjust(top=y_leg - 0.105)
fig_text(fig, 0.012, 0.072, SRC_BEA + " Shares of growth are exact contributions to the Fisher index computed "
         "from the 243 detail lines. Jobs: shares computed from the watch.wilsoniumite.com chart data (BLS via FRED), "
         "page as of 2026-11-02; the page does not print them. Two- and four-year changes are sums of its "
         "twelve-month changes, exact only if the chart is a single data vintage.", fontsize=6.4, color=MUTED)
fig.savefig(FIG / "fig_care_share_of_growth.png", dpi=DPI)
plt.close(fig)

# Figure 2: indexes from 2022-09: outside care (c), real income excl. transfers, real PCE, outside care and imputed
F2 = [("outside_care_C", "Real PCE outside care (c)", "Outside care (c)"),
      ("real_pi_ex_transfers", "Real personal income excl. current transfer receipts", "Income excl. transfers"),
      ("real_pce_bea", "Real PCE (BEA chained dollars)", "Real PCE"),
      ("outside_care_C_and_imputed", "Real PCE outside care (c) and imputed items", "Outside care and imputed")]
m2 = monthly[monthly.date >= BASE]
g12 = monthly.pivot(index="date", columns="series", values="pct_change_12m")
fig, ax = plt.subplots(figsize=(9.6, 5.6))
fig.subplots_adjust(left=0.075, right=0.775, top=0.74, bottom=0.14)
style(ax, grid_axis="y")
dates2 = sorted(m2.date.unique())
xpos = {d_: i for i, d_ in enumerate(dates2)}
ax.axvspan(xpos["2026-03"], xpos["2026-09"], color=BAND, zorder=0, linewidth=0)
ax.text(xpos["2026-03"] + 0.3, 99.3, "watch\nwindow", fontsize=7, color=MUTED, ha="left", va="bottom")
ends = []
for (name, lab, short), col in zip(F2, SLOT):
    s = m2[m2.series == name].set_index("date")["index_2022_09_100"]
    ax.plot([xpos[d_] for d_ in s.index], s.values, color=col, linewidth=1.5, solid_joinstyle="round",
            solid_capstyle="round", zorder=3)
    ax.plot(xpos[s.index[-1]], s.iloc[-1], "o", ms=5, color=col, mec=SURFACE, mew=1.2, zorder=4)
    ends.append((s.iloc[-1], short, col))
# end labels: spread at least `gap` index points apart around their mean, leader lines back to the line ends
gap = 0.55
ends_sorted = sorted(ends, key=lambda e: e[0])
ys = [e[0] for e in ends_sorted]
for i in range(1, len(ys)):
    ys[i] = max(ys[i], ys[i - 1] + gap)
ys = [y + np.mean([e[0] for e in ends_sorted]) - np.mean(ys) for y in ys]
for i in range(1, len(ys)):
    ys[i] = max(ys[i], ys[i - 1] + gap)
xe = xpos[dates2[-1]]
for (v, short, col), yl in zip(ends_sorted, ys):
    ax.annotate(f"{short}  {v:.1f}", (xe, v), xytext=(xe + 2.0, yl), textcoords="data", fontsize=7.6, color=INK,
                va="center", ha="left", annotation_clip=False,
                arrowprops=dict(arrowstyle="-", color=AXIS, linewidth=0.6, shrinkA=0, shrinkB=3))
ticks = [d_ for d_ in dates2 if d_.endswith("-09") or d_.endswith("-03")]
ax.set_xticks([xpos[d_] for d_ in ticks])
ax.set_xticklabels([("Sep " if d_.endswith("-09") else "Mar ") + d_[:4] for d_ in ticks], fontsize=7.6)
ax.set_xlim(-0.5, xe + 0.5)
ax.set_ylabel("Index, Sep 2022 = 100", fontsize=8, color=INK2)
yrs = ["2023-09", "2024-09", "2025-09", "2026-09"]
y_head = header(fig, [
    (f"Real non-transfer income slowed from {g12.loc['2023-09', 'real_pi_ex_transfers']:.1f}% to "
     f"{g12.loc['2026-09', 'real_pi_ex_transfers']:.1f}% a year; spending outside care held near 2%",
     dict(fontsize=10.5, color=INK, fontweight="bold")),
    ("Twelve-month growth to each September 2023-2026: outside care (c) " +
     ", ".join(f"{g12.loc[y_, 'outside_care_C']:.1f}%" for y_ in yrs) + "; real income excluding transfers " +
     ", ".join(f"{g12.loc[y_, 'real_pi_ex_transfers']:.1f}%" for y_ in yrs) + ". Care (c) is health care "
     "services incl. NPISH health, medical goods, net health insurance, child care and social assistance. "
     "Imputed items are imputed rent (owner-occupied and farm), financial services furnished without payment "
     "and NPISH final consumption; taking them out as well barely moves the outside-care line.",
     dict(fontsize=7.9, color=INK2))])
fig.subplots_adjust(top=y_head - 0.035)
handles = [Line2D([], [], color=col, linewidth=1.5, label=lab) for (name, lab, short), col in zip(F2, SLOT)]
ax.legend(handles=handles, loc="upper left", fontsize=7.4, ncol=1, labelcolor=INK2, handlelength=1.6)
fig_text(fig, 0.012, 0.045, SRC_BEA + " Outside-care indexes are Fisher chains of the 2.4.5U detail lines; real "
         "income excluding transfers is Table 2.6 line 36.", fontsize=6.4, color=MUTED)
fig.savefig(FIG / "fig_outside_care.png", dpi=DPI)
plt.close(fig)


# Figure 3: contributions by sector, care (c) in its parts first, everything else by function
def fig_contributions(key):
    gt = group_tables[key]
    cf = gt[gt.kind == "care-first partition"][["group", "contribution_pp"]].copy()
    cf["care"] = cf.group.str.startswith("care: ")
    cf["name"] = cf.group.str.replace("care: ", "", regex=False)
    cf = pd.concat([cf[cf.care].sort_values("contribution_pp", ascending=False),
                    cf[~cf.care].sort_values("contribution_pp", ascending=False)])
    total = gt.loc[gt.kind == "total", "contribution_pp"].iloc[0]
    care = cf.loc[cf.care, "contribution_pp"].sum()
    n = len(cf)
    a, b = gt.start.iloc[0], gt.end.iloc[0]
    share0 = gt.loc[gt.group == CARE_LABEL["C"], "start_share_pct"].iloc[0]
    resid_ = gt.loc[gt.kind == "residual", "real_growth_pct"].iloc[0]
    fig, ax = plt.subplots(figsize=(8.6, 6.6))
    fig.subplots_adjust(left=0.43, right=0.93, top=0.80, bottom=0.12)
    y_head = header(fig, [
        (f"{WLABEL[key].split(' (')[0]}: care (c) contributed {care:.2f} of {total:.2f} points of real PCE "
         f"growth ({100 * care / total:.0f}%)", dict(fontsize=10.5, color=INK, fontweight="bold")),
        (f"Exact contributions to the growth of real PCE, {a} to {b}, from the 243 detail lines of Table 2.4.5U. "
         f"Care (c) was {share0:.1f}% of PCE at the start. The grey bars partition the rest of PCE by function. "
         f"BEA's published real PCE grew {resid_:.3f} points more than the bars add up to.",
         dict(fontsize=7.8, color=INK2))])
    fig.subplots_adjust(top=y_head - 0.03)
    style(ax, grid_axis="x")
    ys = [n - 1 - i + (0.0 if c else -0.6) for i, c in enumerate(cf.care)]   # a gap between the two blocks
    lo, hi = min(0.0, cf.contribution_pp.min()), cf.contribution_pp.max()
    ax.set_xlim(lo - (0.12 * (hi - lo) if lo < 0 else 0.0), hi + 0.18 * (hi - lo))
    ax.set_ylim(min(ys) - 0.7, max(ys) + 0.7)
    fig.canvas.draw()
    for y, (_, r) in zip(ys, cf.iterrows()):
        rounded_hbar(ax, y, r.contribution_pp, 0.62, SLOT[0] if r.care else GRAYBAR)
        ax.annotate(f"{r.contribution_pp:+.2f}", (r.contribution_pp, y),
                    xytext=(4 if r.contribution_pp >= 0 else -4, 0), textcoords="offset points",
                    ha="left" if r.contribution_pp >= 0 else "right", va="center", fontsize=7.4, color=INK2)
    ax.axvline(0, color=AXIS, linewidth=0.75, zorder=1)
    ax.set_yticks(ys)
    ax.set_yticklabels(cf.name.tolist(), fontsize=7.6)
    ax.set_xlabel("Contribution to real PCE growth over the window, percentage points", fontsize=7.8, color=INK2)
    ax.legend(handles=[Patch(color=SLOT[0], label="Care (c), by part"),
                       Patch(color=GRAYBAR, label="Outside care, by function")],
              loc="lower right", fontsize=7.6, labelcolor=INK2)
    fig_text(fig, 0.012, 0.04, "Source: BEA NIPA Tables 2.4.4U and 2.4.5U, September 2026 data released "
             "2026-10-29; contributions formula from the NIPA Handbook, ch. 4.", fontsize=6.4, color=MUTED)
    fig.savefig(FIG / f"fig_contributions_{window_tag(a, b)}.png", dpi=DPI)
    plt.close(fig)


for key in ["jobs", "4y"]:
    fig_contributions(key)

# %% results tables for NOTES_sectors.md (written to out/; the notes embed them verbatim, checks verify that)
def md(df):
    cols = list(df.columns)
    out = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for _, r in df.iterrows():
        out.append("| " + " | ".join(str(r[c]) for c in cols) + " |")
    return "\n".join(out)


def f1(x):
    return "" if pd.isna(x) else f"{x + 0.0:.1f}".replace("-0.0", "0.0") if abs(x) < 0.05 else f"{x:.1f}"


def f2(x):
    return "" if pd.isna(x) else (f"{0.0:.2f}" if abs(x) < 0.005 else f"{x:.2f}")


def f3(x):
    return "" if pd.isna(x) else f"{x:+.3f}"


WORDER = ["jobs", "12m", "6m", "4y", "annual"]
tabs = {}
h = headline.set_index(["window", "care_variant"])
tabs["T1"] = pd.DataFrame([{
    "Window": WLABEL[w],
    "Real PCE growth, % (BEA)": f2(h.loc[(w, "C"), "real_pce_growth_pct_bea"]),
    "Care (c) share of PCE at start, %": f1(h.loc[(w, "C"), "care_start_share_of_pce_pct"]),
    "Care (c) contribution, pp": f2(h.loc[(w, "C"), "care_contribution_pp"]),
    "Care (c) share of real growth, %": f1(h.loc[(w, "C"), "care_share_of_growth_pct"]),
    "Care (c) share of the nominal increase, %": f1(h.loc[(w, "C"), "care_share_of_nominal_increase_pct"]),
    "Care (c) real growth, %": f2(h.loc[(w, "C"), "care_real_growth_pct"]),
    "Prices: care (c) / all PCE, %": f"{f2(h.loc[(w, 'C'), 'care_implicit_price_change_pct'])} / "
    f"{f2(h.loc[(w, 'C'), 'pce_implicit_price_change_pct'])}",
    "Outside care (c) real growth, % (annualized)": f"{f2(h.loc[(w, 'C'), 'outside_care_real_growth_pct'])} "
    f"({f1(h.loc[(w, 'C'), 'outside_care_real_growth_annualized_pct'])})",
    "Outside care (c) and imputed, %": f2(h.loc[(w, "C"), "outside_care_and_imputed_real_growth_pct"]),
    "Real income excl. transfers, %": f2(h.loc[(w, "C"), "real_pi_ex_transfers_growth_pct"]),
    "Care share of net job growth, % (watch)": f1(h.loc[(w, "C"), "care_share_of_net_job_growth_pct"]),
} for w in WORDER])
tabs["T2"] = pd.DataFrame([{"Care definition": CARE_LABEL[k],
                            **{WLABEL[w]: f"{f1(h.loc[(w, k), 'care_share_of_growth_pct'])} "
                               f"({f1(h.loc[(w, k), 'care_start_share_of_pce_pct'])})" for w in WORDER}}
                           for k in CARE_TOPS])
tabs["T3"] = pd.DataFrame([{"Care definition": CARE_LABEL[k],
                            **{WLABEL[w]: f"{f2(h.loc[(w, k), 'outside_care_real_growth_pct'])} / "
                               f"{f2(h.loc[(w, k), 'outside_care_and_imputed_real_growth_pct'])}" for w in WORDER}}
                           for k in CARE_TOPS])
res = []
for w in WORDER:
    gt = group_tables[w]
    res.append({"Window": WLABEL[w],
                "Leaf Fisher, %": f"{gt.loc[gt.kind == 'total', 'real_growth_pct'].iloc[0]:.4f}",
                "BEA chained dollars, %": f"{gt.loc[gt.kind == 'bea', 'real_growth_pct'].iloc[0]:.4f}",
                "Residual (BEA minus leaf), pp": f"{gt.loc[gt.kind == 'residual', 'real_growth_pct'].iloc[0]:+.4f}",
                "Largest gap to chained published 2.8.2/2.3.2 contributions, pp":
                    f"{wcomp.loc[wcomp.window == w, 'diff_pp'].abs().max():.3f}"})
tabs["T4"] = pd.DataFrame(res)
fun = []
for g in ["Goods", "Services"] + list(FUNC):
    row = {"Group": g}
    for w in WORDER:
        gt = group_tables[w][group_tables[w].kind.isin(["subtotal", "functional"])].set_index("group")
        row[WLABEL[w]] = f"{f2(gt.loc[g, 'contribution_pp'])} ({f1(gt.loc[g, 'share_of_growth_pct'])})"
    g4 = group_tables["4y"]
    row["Share of PCE, Sep 2022, %"] = f1(g4[g4.kind.isin(["subtotal", "functional"])].set_index("group")
                                          .loc[g, "start_share_pct"])
    fun.append(row)
tot = {"Group": "PCE (sum of the 243 leaves)"}
for w in WORDER:
    gt = group_tables[w]
    tot[WLABEL[w]] = f"{f2(gt.loc[gt.kind == 'total', 'contribution_pp'].iloc[0])} (100.0)"
tot["Share of PCE, Sep 2022, %"] = "100.0"
tabs["T5"] = pd.DataFrame(fun + [tot])
cfr = []
for g in CARE_FIRST:
    row = {"Group": g}
    for w in WORDER:
        gt = group_tables[w][group_tables[w].kind == "care-first partition"].set_index("group")
        row[WLABEL[w]] = f2(gt.loc[g, "contribution_pp"])
    cfr.append(row)
tabs["T6"] = pd.DataFrame(cfr)
parts = []
for g in CARE_PARTS:
    row = {"Part": g}
    for w in WORDER:
        gt = group_tables[w][group_tables[w].kind == "care part"].set_index("group")
        row[WLABEL[w]] = f"{f2(gt.loc[g, 'contribution_pp'])} ({f1(gt.loc[g, 'start_share_pct'])})"
    parts.append(row)
tabs["T7"] = pd.DataFrame(parts)
fz = financing.copy()
lv_items = [CARE_LABEL["A+"], CARE_LABEL["B"], CARE_LABEL["C"], "Medicare (19)", "Medicaid (20)", MM, "PCE", PIX]
finrows = []
for it in lv_items:
    row = {"Item": it}
    for w in WORDER:
        r = fz[(fz.window == w) & (fz.block == "levels") & (fz["item"] == it)].iloc[0]
        row[WLABEL[w]] = f"{r.growth_pct:.1f}% / {r.increment_musd / 1000:,.0f}"
    finrows.append(row)
tabs["T8"] = pd.DataFrame(finrows)
gap_items = ["Real gap, pp", "Nominal gap, pp", f"Part of nominal gap from {MM}: s0 (g - gY), pp",
             f"Share of the nominal gap from {MM}, %",
             "Gross upper bound: increase in Medicare + Medicaid / (increase in PCE - increase in income excl. "
             "transfers), %",
             f"Share of the nominal gap from {CARE_LABEL['C']}, %",
             f"Share of the real gap from {CARE_LABEL['C']}, % (gap on the leaf Fisher)"]
gaprows = []
for it in gap_items:
    row = {"Item": it}
    for w in WORDER:
        r = fz[(fz.window == w) & (fz.block == "gap") & (fz["item"] == it)].iloc[0]
        row[WLABEL[w]] = f2(r.value) if pd.notna(r.value) else "n/a"
    gaprows.append(row)
tabs["T9"] = pd.DataFrame(gaprows)
brows = []
for it in fz[fz.block == "bridge"]["item"].unique():
    row = {"Item": it}
    for w in WORDER:
        r = fz[(fz.window == w) & (fz.block == "bridge") & (fz["item"] == it)].iloc[0]
        row[WLABEL[w]] = f"{r.increment_musd / 1000:,.0f}"
    brows.append(row)
tabs["T10"] = pd.DataFrame(brows)
jz = jobs.set_index("window")
JLABEL = {**WLABEL, **{c[0]: c[4] for c in JOB_CONTEXT}}
tabs["T11"] = pd.DataFrame([{"Window": JLABEL[w],
                             "Private outside care, thousands": f"{jz.loc[w, 'jobs_change_k: Private jobs outside care']:+.0f}",
                             "Health care and social assistance, thousands":
                                 f"{jz.loc[w, 'jobs_change_k: Health care and social assistance']:+.0f}",
                             "Government, thousands": f"{jz.loc[w, 'jobs_change_k: Government']:+.0f}",
                             "Care share of net job growth, %": f1(jz.loc[w, "care_share_of_net_job_growth_pct"]),
                             "Care share of private job growth, %":
                                 f1(jz.loc[w, "care_share_of_private_job_growth_pct"])}
                            for w in ["jobs", "12m", "4y", "covid4y", "pre4y"]])
hz = history.set_index("period")
hbz = history_bea.set_index("period")


def fres(x):
    return "" if pd.isna(x) else ("0.000" if abs(x) < 0.0005 else f"{x:+.3f}")


tabs["T12"] = pd.DataFrame([{"Period": per_,
                             "Real PCE growth, %": f2(hz.loc[per_, "real_pce_growth_pct"]),
                             "Care (c) share of PCE at start, %": f1(hz.loc[per_, "care_C_share_of_level_pct"]),
                             "Care (c) contribution, pp": f2(hz.loc[per_, "care_C_contribution_pp"]),
                             "Care (c) share of real growth, %": f1(hz.loc[per_, "care_C_share_of_growth_pct"]),
                             "Care (c) share of the nominal increase, %":
                                 f1(hz.loc[per_, "care_C_share_of_nominal_increase_pct"]),
                             "Care (a+) share of real growth, %": f1(hz.loc[per_, "care_A+_share_of_growth_pct"]),
                             "Outside care (c) real growth, %": f2(hz.loc[per_, "outside_care_C_real_growth_pct"]),
                             "Real income excl. transfers, %": f2(hz.loc[per_, "real_pi_ex_transfers_growth_pct"]),
                             "BEA real PCE growth, % (residual, pp)":
                                 f"{f2(hbz.loc[per_, 'real_pce_growth_pct_bea'])} "
                                 f"({fres(hbz.loc[per_, 'residual_pp'])})",
                             "Care (c) share of BEA's real growth, %":
                                 f1(hbz.loc[per_, "care_C_share_of_bea_growth_pct"])}
                            for per_ in [str(y) for y in range(2011, 2026)]
                            + ["2010 to 2019", "2015 to 2019", "2015-09 to 2019-09", "2018-09 to 2022-09",
                               "2022-09 to 2026-09"]])
dz = dollar_split[dollar_split.care_variant == "C"].set_index("window")
DLABEL = {w[0]: w[4] for w in DOLLAR_WINDOWS}


def split_cell(r):
    rel = r.of_which_relative_prices_pp
    return (f"{r.real_minus_nominal_share_pp:.1f} = {r.of_which_general_inflation_pp:.1f} "
            f"{'+' if rel >= 0 else '-'} {abs(rel):.1f}")


tabs["T13"] = pd.DataFrame([{
    "Window": DLABEL[w],
    "Share of PCE at start, %": f2(dz.loc[w, "start_share_of_pce_pct"]),
    "Share of PCE at end, % (change, pt)": f"{f2(dz.loc[w, 'end_share_of_pce_pct'])} "
                                           f"({dz.loc[w, 'share_change_pp']:+.2f})",
    "Share at end at start-of-window prices, % (change, pt)": f"{f2(dz.loc[w, 'end_share_at_start_prices_pct'])} "
                                                              f"({dz.loc[w, 'share_change_at_start_prices_pp']:+.2f})",
    "Share of real growth, %": f1(dz.loc[w, "share_of_real_growth_pct"]),
    "Share of the nominal increase, %": f1(dz.loc[w, "share_of_nominal_increase_pct"]),
    "Same at all-PCE price growth, %": f1(dz.loc[w, "share_of_nominal_increase_if_care_prices_as_pce_pct"]),
    "Real minus nominal share, pp = general inflation + relative prices": split_cell(dz.loc[w]),
    "Prices: care (c) / all PCE, %": f"{f2(dz.loc[w, 'care_price_change_pct'])} / "
                                     f"{f2(dz.loc[w, 'pce_price_change_pct'])}",
} for w in WORDER + ["pre4y", "covid4y", "7y"]])
gz = gap_timing.set_index("period")
tabs["T14"] = pd.DataFrame([{
    "Period": gz.loc[p, "label"],
    "Real PCE growth, % (BEA)": f2(gz.loc[p, "real_pce_growth_pct_bea"]),
    "Real income excl. transfers, %": f2(gz.loc[p, "real_pi_ex_transfers_growth_pct"]),
    "Real gap, pp (BEA)": f2(gz.loc[p, "real_gap_pp_bea"]),
    "Real gap, pp (leaf Fisher)": f2(gz.loc[p, "real_gap_pp_leaf"]),
    "Care (c) part, volumes, pp": f2(gz.loc[p, "care_C_part_of_real_gap_pp"]),
    "Outside care part, volumes, pp": f2(gz.loc[p, "outside_care_C_part_of_real_gap_pp"]),
    "Care (c) share, volumes, %": f1(gz.loc[p, "care_C_share_of_real_gap_pct"]) if pd.notna(
        gz.loc[p, "care_C_share_of_real_gap_pct"]) else "n/a",
    "Nominal gap, pp": f2(gz.loc[p, "nominal_gap_pp"]),
    "Care (c) part, dollars, pp": f2(gz.loc[p, "care_C_part_of_nominal_gap_pp"]),
    "Outside care part, dollars, pp": f2(gz.loc[p, "outside_care_C_part_of_nominal_gap_pp"]),
    "Care (c) share, dollars, %": f1(gz.loc[p, "care_C_share_of_nominal_gap_pct"]) if pd.notna(
        gz.loc[p, "care_C_share_of_nominal_gap_pct"]) else "n/a",
} for p in ["pre", "6m", "4y"]])
with open(OUT / "notes_tables_sectors.md", "w", encoding="utf-8") as fh:
    for k, df in tabs.items():
        fh.write(f"<!-- {k} -->\n{md(df)}\n\n")

# %% print the headline
pd.set_option("display.width", 250)
cols = ["window", "real_pce_growth_pct_bea", "residual_pp", "care_start_share_of_pce_pct", "care_contribution_pp",
        "care_share_of_growth_pct", "outside_care_real_growth_pct", "outside_care_real_growth_annualized_pct",
        "outside_care_and_imputed_real_growth_pct", "real_pi_ex_transfers_growth_pct",
        "care_share_of_net_job_growth_pct"]
for k in CARE_TOPS:
    print(f"\nvariant {k}: {CARE_LABEL[k]}")
    print(headline[headline.care_variant == k][cols].round(3).to_string(index=False))
print("\npublished comparison, max |diff| pp by table:",
      comp.groupby("table")["diff_pp"].apply(lambda s: round(s.abs().max(), 4)).to_dict(),
      "| unmapped published lines:", UNMAPPED)
print("window comparison (chained published vs ours), max |diff| pp:",
      wcomp.groupby("window")["diff_pp"].apply(lambda s: round(s.abs().max(), 4)).to_dict())
print("\ncare (c) in dollars (care_dollar_shares.csv):")
print(dz[["start_share_of_pce_pct", "end_share_of_pce_pct", "share_change_pp", "share_change_at_start_prices_pp",
          "share_of_real_growth_pct", "share_of_nominal_increase_pct",
          "share_of_nominal_increase_if_care_prices_as_pce_pct", "of_which_general_inflation_pp",
          "of_which_relative_prices_pp"]].round(3).to_string())
print("\nwhen the gap opened (gap_timing.csv):")
print(gap_timing.set_index("period").drop(columns=["label", "start", "end"]).round(3).T.to_string())
print(f"cumulative real gap since Sep 2022 at its lowest: {GAP_MIN[1]:+.2f} pt in {GAP_MIN[0]}")
print("context residuals (care_share_history_bea.csv):",
      history_bea[history_bea.kind == "window"].set_index("period")[["residual_pp", "care_C_share_of_bea_growth_pct"]]
      .round(3).to_dict("index"))
v1_ = leaf_vq.iloc[0]
print(f"2.4.5U/2.4.4U vs 2.4.3U, monthly since 2022-01: max {v1_.max_gap_pct_monthly_since_2022_01:.3f}% (line "
      f"{v1_.line}, {v1_.label}, {v1_.month_of_max_since_2022_01})")
MINE = (["headline_sectors.csv", "jobs_watch_windows.csv", "outside_care_monthly.csv", "care_financing.csv",
         "notes_tables_sectors.md", "care_share_history.csv", "care_share_history_bea.csv", "care_dollar_shares.csv",
         "gap_timing.csv", "leaf_vp_vs_q.csv",
         "published_comparison.csv", "published_comparison_windows.csv", "leaf_fisher_vs_bea.csv"]
        + [f"sector_{k}_{window_tag(a, b)}.csv" for k in ("contributions", "groups") for _, _, a, b, _ in WINDOWS])
assert all((OUT / f).exists() for f in MINE)
print("wrote", len(MINE), "files in", OUT, "and", sorted(p.name for p in FIG.glob("fig_*.png")))
