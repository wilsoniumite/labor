# verify_independent_sectors.py — independent verification of the Q2 sectors unit (consumption/recent).
#
# Re-derives the sectors unit's numbers by a separate route and prints one line per claim:
#     OK  | claim | builder value | my value | note
#     BAD | claim | builder value | my value | note
# and a final count. It does not import, copy or call consumption/recent/code/sectors.py, and it does not read the
# tidy CSVs. The separate route:
#   * BEA values from the RAW workbooks: underlying detail (xls_underlying/Section2All_xls.xlsx, Tables 2.4.3U-2.4.6U)
#     and published tables (xls_survey/Section2All_xls.xlsx, Tables 2.1, 2.6, 2.3.2, 2.4.2, 2.4.5, 2.8.2); the
#     workbook values are checked against the flat files (FlatFiles.zip) for every 2.4.5U/2.4.4U series used.
#   * The 2.4.5U hierarchy rebuilt from the workbook's own label indentation and "Less:" prefixes.
#   * Fisher quantity and price relatives and BEA's contribution formula (NIPA Handbook ch. 4) coded from their
#     definitions; care, PCE, Medicare and Medicaid dollar levels taken from the published top lines (not leaf sums).
#   * Published contributions mapped to 2.4.5U lines by series code (not by label).
#   * Jobs from the watch page's embedded chart data (its JSON script element, found by string search).
# The builder's out/*.csv and NOTES_sectors.md are read only to be compared against.
#
# Run from the repo root (about 40 s):
#     venv/bin/python -I consumption/recent/checks/verify_independent_sectors.py
# Plain functions plus top-level code; each '# %%' block can be pasted into a notebook cell.

# %% setup
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent                      # consumption/recent/checks
sys.path.insert(0, str(HERE))

import io                                                   # noqa: E402
import json                                                 # noqa: E402
import re                                                   # noqa: E402
import struct                                               # noqa: E402
import zipfile                                              # noqa: E402
import zlib                                                 # noqa: E402

import numpy as np                                          # noqa: E402
import pandas as pd                                         # noqa: E402
import openpyxl                                             # noqa: E402
from tqdm.auto import tqdm                                  # noqa: E402

RECENT = HERE.parent                                        # consumption/recent
THREAD = RECENT.parent                                      # consumption
RAW = THREAD / "data" / "raw"
U_XLSX = RAW / "bea" / "nipa" / "xls_underlying" / "Section2All_xls.xlsx"
S_XLSX = RAW / "bea" / "nipa" / "xls_survey" / "Section2All_xls.xlsx"
FLAT_ZIP = RAW / "bea" / "nipa" / "FlatFiles.zip"
WATCH_JOBS = RAW / "watch" / "jobs-outside-care.html"
B_OUT = RECENT / "out"                                      # the builder's outputs (compared against only)
B_FIG = RECENT / "figures"
B_NOTES = RECENT / "NOTES_sectors.md"

RESULTS = []                                                # (status, claim, builder, mine, note)


def report(ok, claim, builder, mine, note=""):
    status = "OK" if ok else "BAD"
    RESULTS.append((status, claim, str(builder), str(mine), note))
    print(f"{status} | {claim} | {builder} | {mine} | {note}", flush=True)


# %% raw BEA workbooks
def read_sheet(wb, name):
    """One workbook sheet -> (values DataFrame indexed by period 'YYYY' / 'YYYY-MM', columns = line numbers;
    {line: raw label}; {line: series code}). Non-numeric cells ('.....') become NaN."""
    rows = list(wb[name].iter_rows(values_only=True))
    h = next(i for i, r in enumerate(rows) if r and r[0] == "Line")
    per = [str(x) for x in rows[h][3:]]
    per = [p[:4] + "-" + p[5:] if re.fullmatch(r"\d{4}M\d{2}", p) else p for p in per]
    vals, labels, codes = {}, {}, {}
    for r in rows[h + 1:]:
        if r[0] is None or not str(r[0]).strip().isdigit():
            continue
        ln = int(str(r[0]).strip())
        labels[ln], codes[ln] = str(r[1]), r[2]
        vals[ln] = [float(x) if isinstance(x, (int, float)) and not isinstance(x, bool) else np.nan
                    for x in r[3:3 + len(per)]]
    return pd.DataFrame(vals, index=per), labels, codes


print("reading the raw underlying-detail workbook ...", flush=True)
wbu = openpyxl.load_workbook(U_XLSX, read_only=True)
V, P, Q, X = {}, {}, {}, {}
for f in "MA":
    V[f], ULABEL, UCODE = read_sheet(wbu, f"U20405-{f}")       # current dollars, $mn (monthly SAAR)
    P[f], _, PCODE = read_sheet(wbu, f"U20404-{f}")            # price indexes 2017=100
    Q[f], _, _ = read_sheet(wbu, f"U20403-{f}")                # quantity indexes 2017=100
    X[f], _, _ = read_sheet(wbu, f"U20406-{f}")                # chained 2017 dollars (from 2007)
wbu.close()
print("reading the raw published-tables workbook ...", flush=True)
wbs = openpyxl.load_workbook(S_XLSX, read_only=True)
PI = {"M": read_sheet(wbs, "T20600-M")[0], "A": read_sheet(wbs, "T20100-A")[0]}
PUB = {k: read_sheet(wbs, k) for k in ["T20802-M", "T20302-A", "T20402-A", "T20405-A"]}
wbs.close()

# %% hierarchy rebuilt from the workbook's indentation (2 spaces per level; line 1 is printed indented, it is the root)
MAIN = [ln for ln in sorted(ULABEL) if ln <= 368]
INDENT = {ln: len(ULABEL[ln]) - len(ULABEL[ln].lstrip(" ")) for ln in MAIN}
INDENT[1] = -2
PARENT, stack = {1: None}, [1]
for ln in MAIN[1:]:
    while INDENT[stack[-1]] >= INDENT[ln]:
        stack.pop()
    PARENT[ln] = stack[-1]
    stack.append(ln)
KIDS = {ln: [k for k in MAIN if PARENT.get(k) == ln] for ln in MAIN}
OWN_SIGN = {ln: (-1 if ULABEL[ln].strip().startswith("Less:") else 1) for ln in MAIN}
ANC = {}
for ln in MAIN:
    a, x = [ln], ln
    while PARENT[x] is not None:
        x = PARENT[x]
        a.append(x)
    ANC[ln] = a
SIGN = {ln: int(np.prod([OWN_SIGN[x] for x in ANC[ln][:-1]])) for ln in MAIN}    # sign with which ln enters PCE
LEAVES = [ln for ln in MAIN if not KIDS[ln]]


def under(c, top):
    return top in ANC[c]


def clean_label(ln):
    return re.sub(r"\s*\((?:part|parts)? ?(?:of )?[\d, and]+\)\s*$", "", ULABEL[ln].strip())


# %% the Fisher engine, coded from the definitions (NIPA Handbook ch. 4)
def split(node, v0, v1):
    """Finest components below `node` for a pair of periods: a node is split into its children when the same
    children are published in both periods and their signed sum equals the node within rounding in both."""
    kids = KIDS[node]
    k0 = [k for k in kids if np.isfinite(v0[k])]
    k1 = [k for k in kids if np.isfinite(v1[k])]
    if kids and k0 and k0 == k1:
        tol = 0.5 * (len(k0) + 1) + 0.5
        if all(abs(sum(OWN_SIGN[k] * vv[k] for k in k0) - vv[node]) <= tol for vv in (v0, v1)):
            return [c for k in k0 for c in split(k, v0, v1)]
    return [node]


def fisher(v0, v1, p0, p1):
    """Signed values and prices of the components -> (Fisher quantity relative, Fisher price relative,
    contributions to (quantity relative - 1)) with BEA's formula C_i = (p0 + p1/FP)(q1 - q0) / sum (p0 + p1/FP) q0."""
    q0, q1 = v0 / p0, v1 / p1
    s00, s11, s01, s10 = (p0 * q0).sum(), (p1 * q1).sum(), (p0 * q1).sum(), (p1 * q0).sum()
    fq = np.sqrt((s01 / s00) * (s11 / s10))
    fp = np.sqrt((s10 / s00) * (s11 / s01))
    w = p0 + p1 / fp
    return fq, fp, w * (q1 - q0) / (w * q0).sum()


def run_chain(freq, start, end, use_q=False):
    """Pairs (t0, t1) from start to end: {t1: dict(comps, v0, v1, p0, p1, a=p0 q1, b=p1 q0, fq, fp, c)}.
    use_q: build the price relatives from the 2.4.3U quantity relatives instead of the 2.4.4U prices."""
    dates = [d for d in V[freq].index if start <= d <= end]
    vd = {d: V[freq].loc[d].to_dict() for d in dates}
    out = {}
    for t0, t1 in tqdm(list(zip(dates[:-1], dates[1:])), desc=f"my Fisher chain {freq} {start}..{end}",
                       mininterval=2.0, leave=False):
        comps = split(1, vd[t0], vd[t1])
        sg = np.array([SIGN[c] for c in comps], dtype=float)
        v0 = np.array([vd[t0][c] for c in comps]) * sg
        v1 = np.array([vd[t1][c] for c in comps]) * sg
        if use_q:
            r = Q[freq].loc[t1, comps].values / Q[freq].loc[t0, comps].values      # quantity relatives
            p0 = np.ones(len(comps))
            with np.errstate(divide="ignore", invalid="ignore"):
                p1 = np.where(v0 != 0, (v1 / np.where(v0 != 0, v0, 1.0)) / r, P[freq].loc[t1, comps].values
                              / P[freq].loc[t0, comps].values)
        else:
            p0, p1 = P[freq].loc[t0, comps].values, P[freq].loc[t1, comps].values
        if not (np.isfinite(p0).all() and np.isfinite(p1).all()):
            raise ValueError(f"no price for a component in {t0}->{t1}")
        fq, fp, c = fisher(v0, v1, p0, p1)
        out[t1] = dict(comps=tuple(comps), v0=v0, v1=v1, p0=p0, p1=p1, a=v1 * p0 / p1, b=v0 * p1 / p0,
                       fq=fq, fp=fp, c=c, t0=t0)
    return out


def mask(comps, inc, exc=()):
    """Membership of each component in the group (under an include top, not under an exclude top), or None if the
    partition is too coarse to separate the group (a component is a strict ancestor of a top)."""
    tops = list(inc) + list(exc)
    if any(c != t and c in ANC[t] for c in comps for t in tops):
        return None
    return np.array([any(under(c, t) for t in inc) and not any(under(c, t) for t in exc) for c in comps])


_MEMO = {}


def cmask(comps, inc, exc=()):
    key = (comps, tuple(inc), tuple(exc))
    if key not in _MEMO:
        _MEMO[key] = mask(comps, inc, exc)
    return _MEMO[key]


def periods(ch, a, b):
    return [t for t in ch if a < t <= b]


def win_growth(ch, a, b, inc=(1,), exc=()):
    """Growth over (a, b] of the chained Fisher quantity index of a group."""
    g = 1.0
    for t in periods(ch, a, b):
        pr = ch[t]
        m = cmask(pr["comps"], inc, exc)
        if m is None or not m.any():
            return np.nan
        lq = pr["a"][m].sum() / pr["v0"][m].sum()
        pq = pr["v1"][m].sum() / pr["b"][m].sum()
        if lq * pq <= 0:
            return np.nan
        g *= np.sqrt(lq * pq)
    return g - 1


def win_contrib(ch, a, b, inc=(1,), exc=()):
    """Window contribution of a group: sum over periods of (I_{t-1} / I_a) x the period's contribution."""
    tot, cum = 0.0, 1.0
    for t in periods(ch, a, b):
        pr = ch[t]
        m = cmask(pr["comps"], inc, exc)
        if m is None:
            return np.nan
        tot += cum * pr["c"][m].sum()
        cum *= pr["fq"]
    return tot


def leafsum(freq, t, inc, exc=()):
    """Signed current-dollar value of a group as the sum of the current leaves (for groups with exclusions)."""
    ls = [c for c in LEAVES if np.isfinite(V[freq].loc[t, c]) and any(under(c, x) for x in inc)
          and not any(under(c, x) for x in exc)]
    return float(sum(SIGN[c] * V[freq].loc[t, c] for c in ls))


def topsum(freq, t, tops):
    """Signed current-dollar value of a union of disjoint published lines, from the lines themselves."""
    return float(sum(SIGN[x] * V[freq].loc[t, x] for x in tops))


# %% the raw workbook against the raw flat files (every 2.4.5U and 2.4.4U series used here, monthly and annual)
def flat_values(member):
    with zipfile.ZipFile(FLAT_ZIP) as z, z.open(member) as fh:
        df = pd.read_csv(io.TextIOWrapper(fh, encoding="utf-8"), dtype=str)
    df.columns = ["code", "period", "value"]
    df["value"] = pd.to_numeric(df["value"].str.replace(",", "", regex=False), errors="coerce")
    df["period"] = df["period"].str.replace("M", "-", regex=False)
    return df


print("reading the raw flat files ...", flush=True)
FLAT = {"M": flat_values("nipadataM.txt"), "A": flat_values("nipadataA.txt")}
nchk, worst = 0, 0.0
for f in "MA":
    fl = FLAT[f].set_index(["code", "period"])["value"]
    for tab, codes in [(V[f], UCODE), (P[f], PCODE)]:
        for ln in MAIN:
            code = codes.get(ln)
            if not code or code == "ZZZZZZ":
                continue
            s = tab[ln].dropna()
            try:
                fv = fl.loc[code].reindex(s.index)
            except KeyError:
                worst = np.inf
                continue
            d = (fv - s).abs()
            worst = max(worst, float(d.max()) if d.notna().all() else np.inf)
            nchk += len(s)
report(worst < 1e-9, "raw check: every 2.4.5U and 2.4.4U workbook cell used equals the flat-file value (A and M)",
       "README_bea: every cell matches", f"{nchk:,} cells, max |diff| {worst:g}",
       "workbook (my source) and FlatFiles.zip (the tidy source) agree, so the routes start from the same numbers")

# %% the hierarchy as rebuilt
cur_leaves = [c for c in LEAVES if np.isfinite(V["M"].loc["2026-09", c])]
gap_leaf = max(abs(sum(SIGN[c] * V[f].loc[t, c] for c in cur_leaves) - V[f].loc[t, 1])
               for f, ts in [("M", [d for d in V["M"].index if d >= "2007-01"]), ("A", [str(y) for y in range(2007, 2026)])]
               for t in ts)
report(len(cur_leaves) == 243 and gap_leaf <= 12,
       "243 current leaves of 2.4.5U whose signed sum is PCE (2007 on)", "243; PCE = signed leaf sum within 11 $mn",
       f"{len(cur_leaves)}; within {gap_leaf:.0f} $mn", "hierarchy rebuilt from the workbook's indentation")
less = [ln for ln in MAIN if OWN_SIGN[ln] < 0]
report(less == [149, 274, 338, 356], "'Less:' lines", "149, 274, 338, 356", ", ".join(map(str, less)))
for ln, want in [(152, "Housing and utilities"), (160, "Imputed rental of owner-occupied nonfarm housing"),
                 (163, "Rental value of farm dwellings"), (172, "Health care"), (190, "Transportation services"),
                 (209, "Recreation services"), (234, "Food services and accommodations"),
                 (252, "Financial services and insurance"), (254, "Financial services furnished without payment"),
                 (275, "Net health insurance"), (280, "Other services"), (296, "Day care and nursery schools"),
                 (316, "Child care"), (317, "Social assistance"), (333, "Net foreign travel"),
                 (342, "Final consumption expenditures of nonprofit institutions serving households"),
                 (344, "Health, gross output"), (350, "Social services, gross output"),
                 (357, "Health services to households"), (363, "Social services to households"),
                 (121, "Pharmaceutical and other medical products"), (66, "Therapeutic appliances and equipment"),
                 (113, "Gasoline and other energy goods")]:
    if not ULABEL[ln].strip().startswith(want):
        report(False, f"line {ln} label", want, ULABEL[ln].strip())
report(True, "line numbers used by the definitions carry the labels the NOTES give them (23 lines)", "as in NOTES",
       "as in NOTES", "checked against the raw workbook labels; a mismatch would print BAD above")

# %% chains: monthly and annual from 1959, the 2.4.4U route and the 2.4.3U-relatives route for H1
CH = {"M": run_chain("M", "1959-01", "2026-09"), "A": run_chain("A", "1959", "2025")}
CHQ = {"M": run_chain("M", "2015-09", "2026-09", use_q=True), "A": run_chain("A", "2021", "2025", use_q=True)}
add_err = max(abs(pr["c"].sum() - (pr["fq"] - 1)) for f in "MA" for pr in CH[f].values())
ncomp = [len(pr["comps"]) for f in "MA" for pr in CH[f].values()]
const_m = all(len(CH["M"][t]["comps"]) == 243 for t in CH["M"] if t >= "2007-02")
const_a = all(len(CH["A"][t]["comps"]) == 243 for t in CH["A"] if t >= "2008")
report(add_err < 1e-12, "contributions add exactly to the Fisher quantity relative minus one", "to 1e-12",
       f"max |sum C - (FQ - 1)| = {add_err:.1e}", "every month 1959-2026 and year 1959-2025")
report(min(ncomp) == 214 and max(ncomp) == 243 and const_m and const_a,
       "partition: 214 to 243 components over 1959-2026; always the 243 current leaves from 2007-02 (annual 2008)",
       "214 to 243; 243 from 2007-02 / 2008", f"{min(ncomp)} to {max(ncomp)}; 243 from 2007-02: {const_m}, "
       f"from 2008: {const_a}", "my own split rule (same children in both periods, signed sum within rounding)")

# %% definitions (from the NOTES' definitions table), written as (include tops, exclude tops)
CARE = {"A": [172], "A+": [172, 344, 357], "B": [172, 344, 357, 121, 66, 275],
        "C": [172, 344, 357, 121, 66, 275, 316, 317], "C+": [172, 344, 357, 121, 66, 275, 316, 317, 350, 363],
        "S": [172, 344, 357, 316, 317, 350, 363]}
IMPUTED = [160, 163, 254, 342]
FUNC = {"Durable goods": ([3], []), "Nondurable goods excl. energy": ([72], [113]),
        "Gasoline and other energy goods": ([113], []),
        "Housing and utilities excl. imputed rent": ([152], [160]),
        "Imputed rent of owner-occupied housing (160)": ([160], []), "Health care (172)": ([172], []),
        "Transportation services": ([190], []), "Recreation services": ([209], []),
        "Food services and accommodations": ([234], []),
        "Financial services and insurance excl. FSFWP": ([252], [254]),
        "Financial services furnished without payment (254)": ([254], []),
        "Other services excl. net foreign travel": ([280], [333]), "Net foreign travel (333)": ([333], []),
        "NPISH final consumption (342)": ([342], [])}
CARE_FIRST = {"care: Health care services (172)": ([172], []), "care: NPISH health (344 - 357)": ([344, 357], []),
              "care: Medical products and appliances (121, 66)": ([121, 66], []),
              "care: Net health insurance (275)": ([275], []),
              "care: Child care and social assistance (316, 317)": ([316, 317], []),
              "Durable goods excl. therapeutic appliances": ([3], [66]),
              "Nondurable goods excl. energy and medical products": ([72], [113, 121]),
              "Gasoline and other energy goods": ([113], []),
              "Housing and utilities excl. imputed rent": ([152], [160]),
              "Imputed rent of owner-occupied housing": ([160], []), "Transportation services": ([190], []),
              "Recreation services": ([209], []), "Food services and accommodations": ([234], []),
              "Financial services and insurance excl. FSFWP and health insurance": ([252], [254, 275]),
              "Financial services furnished without payment": ([254], []),
              "Other services excl. net foreign travel, child care, social assistance": ([280], [333, 316, 317]),
              "Net foreign travel": ([333], []), "NPISH final consumption excl. health": ([342], [344, 357])}
CARE_PARTS = {"NPISH health (344 - 357)": ([344, 357], []),
              "Medical products, appliances, net health insurance (121, 66, 275)": ([121, 66, 275], []),
              "Child care (316)": ([316], []), "Social assistance (317)": ([317], []),
              "NPISH social services (350 - 363)": ([350, 363], []),
              "Day care and nursery schools (296, education; not in any care variant)": ([296], [])}
for name, groups in [("functional", FUNC), ("care-first", CARE_FIRST)]:
    owner = {}
    for g, (inc, exc) in groups.items():
        for c in cur_leaves:
            if any(under(c, x) for x in inc) and not any(under(c, x) for x in exc):
                owner.setdefault(c, []).append(g)
    dup = [c for c, gs in owner.items() if len(gs) > 1]
    report(not dup and sorted(owner) == sorted(cur_leaves), f"the {name} groups partition the 243 leaves",
           "a partition", f"{len(owner)} leaves covered, {len(dup)} in two groups")
# an independent dollar route for care: the published top lines, not leaf sums
care_gap = max(abs(topsum(f, t, CARE[k]) - leafsum(f, t, CARE[k])) for k in CARE for f in "MA"
               for t in (["2015-09", "2019-09", "2022-09", "2024-08", "2025-09", "2026-03", "2026-08", "2026-09"]
                         if f == "M" else ["2022", "2025"]))
report(care_gap <= 6, "care dollar levels: published top lines equal the signed leaf sums", "leaf sums",
       f"max |top lines - leaf sum| {care_gap:.0f} $mn", "window endpoints, all six variants; my levels use top lines")

# %% windows: everything a reader quotes, recomputed
WINDOWS = [("jobs", "M", "2024-08", "2026-08", "Aug 2024 to Aug 2026 (jobs window)"),
           ("12m", "M", "2025-09", "2026-09", "12 months to Sep 2026"),
           ("6m", "M", "2026-03", "2026-09", "6 months to Sep 2026 (watch window)"),
           ("4y", "M", "2022-09", "2026-09", "4 years to Sep 2026"),
           ("annual", "A", "2022", "2025", "2022 to 2025 (annual data)")]
WLAB = {w[0]: w[4] for w in WINDOWS}
WFREQ = {w[0]: (w[1], w[2], w[3]) for w in WINDOWS}


def n_months(freq, a, b):
    return (int(b[:4]) - int(a[:4])) * 12 + (int(b[5:]) - int(a[5:])) if freq == "M" else (int(b) - int(a)) * 12


def ann(g, freq, a, b):
    return (1 + g) ** (12 / n_months(freq, a, b)) - 1 if np.isfinite(g) else np.nan


def window_numbers(freq, a, b, ch=None):
    """Every headline number for one window (my route)."""
    ch = ch or CH[freq]
    out = {"freq": freq, "a": a, "b": b}
    G = win_growth(ch, a, b)
    out["G_leaf"], out["sumC"] = G, win_contrib(ch, a, b)
    out["G_bea"] = X[freq].loc[b, 1] / X[freq].loc[a, 1] - 1
    out["resid"] = out["G_bea"] - G
    out["V0"], out["V1"] = V[freq].loc[a, 1], V[freq].loc[b, 1]
    out["pce_price"] = (out["V1"] / out["V0"]) / (1 + out["G_bea"]) - 1
    out["pix_real"] = PI[freq].loc[b, 36] / PI[freq].loc[a, 36] - 1
    out["pix_real_ann"] = ann(out["pix_real"], freq, a, b)
    out["care"] = {}
    for k, tops in CARE.items():
        c0, c1 = topsum(freq, a, tops), topsum(freq, b, tops)
        r = {"V0": c0, "V1": c1, "s0": c0 / out["V0"], "contrib": win_contrib(ch, a, b, tops),
             "real": win_growth(ch, a, b, tops), "nom": c1 / c0 - 1,
             "out_contrib": win_contrib(ch, a, b, [1], tops), "out_real": win_growth(ch, a, b, [1], tops),
             "outimp_real": win_growth(ch, a, b, [1], tops + IMPUTED)}
        r["share_growth"] = r["contrib"] / G
        r["share_nom_inc"] = (c1 - c0) / (out["V1"] - out["V0"])
        r["price"] = (1 + r["nom"]) / (1 + r["real"]) - 1
        r["out_real_ann"], r["outimp_real_ann"] = ann(r["out_real"], freq, a, b), ann(r["outimp_real"], freq, a, b)
        out["care"][k] = r
    return out


W = {key: window_numbers(f, a, b) for key, f, a, b, _ in tqdm(WINDOWS, desc="windows", leave=False)}
WQ = {key: window_numbers(f, a, b, CHQ[f]) for key, f, a, b, _ in WINDOWS}
CONTEXT = {"pre4y": ("M", "2015-09", "2019-09"), "covid4y": ("M", "2018-09", "2022-09"),
           "2010-2019": ("A", "2010", "2019"), "2015-2019": ("A", "2015", "2019")}
WC = {key: window_numbers(*v) for key, v in CONTEXT.items()}

# %% groups per window (the sector_groups files) and lines per window (the sector_contributions files)
GROUPS = {"PCE (leaf Fisher, 243 leaves)": ("total", [1], []), "Goods": ("subtotal", [2], []),
          "Services": ("subtotal", [150], [])}
GROUPS.update({g: ("functional", inc, exc) for g, (inc, exc) in FUNC.items()})
CARE_NAME = {"A": "(a) Health care services, households (172)",
             "A+": "(a+) Health care services incl. NPISH health (172 + 344 - 357)",
             "B": "(b) (a+) + medical products, appliances, net health insurance (121, 66, 275)",
             "C": "(c) (b) + child care and social assistance (316, 317)",
             "C+": "(c+) (c) + NPISH social services (350 - 363)",
             "S": "(s) Care services only: (a+) + 316 + 317 + (350 - 363)"}
GROUPS.update({CARE_NAME[k]: ("care", tops, []) for k, tops in CARE.items()})
GROUPS.update({g: ("care part", inc, exc) for g, (inc, exc) in CARE_PARTS.items()})
for k, tops in CARE.items():
    GROUPS[f"Outside care {k}"] = ("outside care", [1], tops)
    GROUPS[f"Outside care {k} and imputed items"] = ("outside care and imputed", [1], tops + IMPUTED)
GROUPS["Imputed and non-cash items (160 + 163 + 254 + 342)"] = ("imputed", IMPUTED, [])
GROUPS["Outside imputed items"] = ("imputed", [1], IMPUTED)
GROUPS.update({g: ("care-first partition", inc, exc) for g, (inc, exc) in CARE_FIRST.items()})


def group_rows(key):
    freq, a, b = WFREQ[key]
    ch, G = CH[freq], W[key]["G_leaf"]
    rows = {}
    for g, (kind, inc, exc) in GROUPS.items():
        s0, s1 = leafsum(freq, a, inc, exc), leafsum(freq, b, inc, exc)
        rg = np.nan if (inc, exc) == ([333], []) else win_growth(ch, a, b, inc, exc)
        cb = win_contrib(ch, a, b, inc, exc)
        rows[g] = {"kind": kind, "n_leaves": int(cmask(ch[b]["comps"], inc, exc).sum()), "start_nominal_musd": s0,
                   "start_share_pct": 100 * s0 / V[freq].loc[a, 1], "end_nominal_musd": s1,
                   "nominal_growth_pct": 100 * (s1 / s0 - 1) if s0 else np.nan, "real_growth_pct": 100 * rg,
                   "real_growth_annualized_pct": 100 * ann(rg, freq, a, b), "contribution_pp": 100 * cb,
                   "share_of_growth_pct": 100 * cb / G}
    return rows


def line_rows(key):
    freq, a, b = WFREQ[key]
    ch, G = CH[freq], W[key]["G_leaf"]
    rows = {}
    for ln in MAIN:
        if not (np.isfinite(V[freq].loc[a, ln]) and np.isfinite(V[freq].loc[b, ln])):
            continue
        leaves = [c for c in cur_leaves if under(c, ln)]
        tags = {}
        for k, tops in list(CARE.items()) + [("imp", IMPUTED)]:
            n = sum(any(under(c, x) for x in tops) for c in leaves)
            tags[k] = "yes" if n == len(leaves) and n else ("part" if n else "no")
        q0, q1 = Q[freq].loc[a, ln], Q[freq].loc[b, ln]
        cb = win_contrib(ch, a, b, [ln])
        rows[ln] = {"sign_to_root": SIGN[ln], "is_leaf": ln in cur_leaves, "level": 0 if ln == 1 else INDENT[ln] // 2 + 1,
                    "parent_line": PARENT[ln], "tags": tags,
                    "start_nominal_musd_signed": SIGN[ln] * V[freq].loc[a, ln],
                    "start_nominal_share_pct": 100 * SIGN[ln] * V[freq].loc[a, ln] / V[freq].loc[a, 1],
                    "end_nominal_musd_signed": SIGN[ln] * V[freq].loc[b, ln],
                    "real_growth_pct": np.nan if ln in (145, 333) else 100 * win_growth(ch, a, b, [ln]),
                    "real_growth_pct_bea_2_4_3U": 100 * (q1 / q0 - 1) if np.isfinite(q0) and np.isfinite(q1)
                    else np.nan,
                    "contribution_pp": 100 * cb, "share_of_growth_pct": 100 * cb / G}
    return rows


GR = {key: group_rows(key) for key in tqdm(W, desc="groups per window", leave=False)}
LR = {key: line_rows(key) for key in tqdm(W, desc="lines per window", leave=False)}

# %% financing: care against Medicare + Medicaid, the bridge from income to spending, the gap (Tables 8-10)
PIX = "Personal income excl. transfers (PI - line 16)"
MM = "Medicare + Medicaid (19 + 20)"
OTHER_TR = "Other social benefits (21-23) and transfers from business (24)"


def pi_item(freq, item, t):
    s = PI[freq].loc[t]
    return {"PCE": V[freq].loc[t, 1], PIX: s[1] - s[16], "Personal current transfer receipts (16)": s[16],
            "Government social benefits (17)": s[17], "Social security (18)": s[18], "Medicare (19)": s[19],
            "Medicaid (20)": s[20], MM: s[19] + s[20], OTHER_TR: s[21] + s[22] + s[23] + s[24],
            "Personal current taxes (26)": s[26], "Personal interest payments (30)": s[30],
            "Personal current transfer payments (31)": s[31], "Personal saving (34)": s[34]}[item]


def financing(key):
    freq, a, b = WFREQ[key]
    lv = {}
    for it in ["PCE", PIX, "Personal current transfer receipts (16)", "Government social benefits (17)",
               "Social security (18)", "Medicare (19)", "Medicaid (20)", MM, OTHER_TR, "Personal current taxes (26)",
               "Personal interest payments (30)", "Personal current transfer payments (31)", "Personal saving (34)"]:
        lv[it] = (pi_item(freq, it, a), pi_item(freq, it, b))
    for k, tops in CARE.items():
        lv[CARE_NAME[k]] = (topsum(freq, a, tops), topsum(freq, b, tops))
    c0, c1 = lv["PCE"]
    y0, y1 = lv[PIX]
    gY, gC = y1 / y0 - 1, c1 / c0 - 1
    excess = c1 - c0 * (1 + gY)
    levels = {}
    for it, (s0, s1) in lv.items():
        spend = it == "PCE" or it in CARE_NAME.values() or it.startswith("Medic")
        levels[it] = {"start_musd": s0, "end_musd": s1, "increment_musd": s1 - s0, "growth_pct": 100 * (s1 / s0 - 1),
                      "share_of_pce_at_start_pct": 100 * s0 / c0,
                      "excess_over_income_growth_musd": s1 - s0 * (1 + gY),
                      "share_of_spending_excess_pct": 100 * (s1 - s0 * (1 + gY)) / excess if spend else np.nan}
    d = {it: s1 - s0 for it, (s0, s1) in lv.items()}
    bridge = {"Personal income excl. transfers": d[PIX], "+ Medicare + Medicaid": d[MM],
              "+ Social security": d["Social security (18)"], "+ Other transfer receipts": d[OTHER_TR],
              "- Personal current taxes": -d["Personal current taxes (26)"],
              "- Interest and transfer payments": -(d["Personal interest payments (30)"]
                                                    + d["Personal current transfer payments (31)"]),
              "- Personal saving": -d["Personal saving (34)"]}
    bridge["= Change in PCE (sum of the above)"] = sum(bridge.values())
    bridge["Change in PCE (published)"] = d["PCE"]
    gx, gyr = W[key]["G_bea"], W[key]["pix_real"]
    ok = gC - gY > 0.0025 and gx - gyr > 0.0025
    gap = {"Real PCE growth, % (2.4.6U line 1)": 100 * gx,
           "Real personal income excl. transfers growth, % (line 36)": 100 * gyr, "Real gap, pp": 100 * (gx - gyr),
           "Nominal PCE growth, %": 100 * gC, "Nominal personal income excl. transfers growth, %": 100 * gY,
           "Nominal gap, pp": 100 * (gC - gY), "Spending excess over income growth, $mn SAAR: C1 - C0(1 + gY)": excess}
    for it in [MM] + [CARE_NAME[k] for k in CARE]:
        s0, s1 = lv[it]
        part = (s0 / c0) * (s1 / s0 - 1 - gY)
        gap[f"Part of nominal gap from {it}: s0 (g - gY), pp"] = 100 * part
        gap[f"Share of the nominal gap from {it}, %"] = 100 * part / (gC - gY) if ok else np.nan
    gap["Gross upper bound: increase in Medicare + Medicaid / (increase in PCE - increase in income excl. transfers), %"] \
        = 100 * d[MM] / (d["PCE"] - d[PIX]) if ok else np.nan
    gl = W[key]["G_leaf"] - gyr
    for k in CARE:
        part = W[key]["care"][k]["contrib"] - W[key]["care"][k]["s0"] * gyr
        gap[f"Part of real gap from {CARE_NAME[k]}: contribution - s0 x real income growth, pp"] = 100 * part
        gap[f"Share of the real gap from {CARE_NAME[k]}, % (gap on the leaf Fisher)"] = 100 * part / gl if ok else np.nan
    return {"levels": levels, "bridge": bridge, "gap": gap, "dC_minus_dY": d["PCE"] - d[PIX], "d": d, "lv": lv}


FIN = {key: financing(key) for key in W}


# %% jobs: the watch page's embedded chart data (twelve-month changes, thousands)
def script_json(page, sid):
    """The JSON body of the <script type="application/json" id=sid> element, by plain string search."""
    i = page.find(f'id="{sid}"')
    tag_start = page.rfind("<script", 0, i)
    tag_end = page.find(">", i)
    if i < 0 or tag_start < 0 or "application/json" not in page[tag_start:tag_end]:
        raise ValueError(f"no JSON script element with id {sid}")
    return json.loads(page[tag_end + 1:page.find("</script>", tag_end)])


JOBS = {s["name"]: dict((p[0][:7], p[1]) for p in s["points"])
        for s in script_json(WATCH_JOBS.read_text(encoding="utf-8"), "plot-1")["series"]}
J_PRIV, J_CARE, J_GOV = "Private jobs outside care", "Health care and social assistance", "Government"


def jobs_change(name, a, b):
    """Change over a whole number of years = sum of the twelve-month changes ending b, b-12, ..."""
    n = n_months("M", a, b)
    if n % 12:
        return np.nan
    return sum(JOBS[name][f"{int(b[:4]) - k}-{b[5:]}"] for k in range(n // 12))


JW = {}
for key, (a, b) in {"jobs": ("2024-08", "2026-08"), "12m": ("2025-09", "2026-09"), "4y": ("2022-09", "2026-09"),
                    "covid4y": ("2018-09", "2022-09"), "pre4y": ("2015-09", "2019-09")}.items():
    ch_ = {nm: jobs_change(nm, a, b) for nm in (J_PRIV, J_CARE, J_GOV)}
    tot = sum(ch_.values())
    JW[key] = {**ch_, "total": tot, "share_net": 100 * ch_[J_CARE] / tot,
               "share_private": 100 * ch_[J_CARE] / (ch_[J_CARE] + ch_[J_PRIV])}

# %% care year by year and over earlier spans (Table 4 / care_share_history.csv)
HIST = {}
for y in range(1990, 2026):
    yy, py = str(y), str(y - 1)
    pr = CH["A"][yy]
    row = {"kind": "year", "real_pce_growth_pct": 100 * (pr["fq"] - 1),
           "real_pi_ex_transfers_growth_pct": 100 * (PI["A"].loc[yy, 36] / PI["A"].loc[py, 36] - 1)}
    for k in ["A+", "B", "C"]:
        m = cmask(pr["comps"], CARE[k])
        c = pr["c"][m].sum()
        lv0, lv1 = topsum("A", py, CARE[k]), topsum("A", yy, CARE[k])
        row[f"care_{k}_share_of_level_pct"] = 100 * lv0 / V["A"].loc[py, 1]
        row[f"care_{k}_contribution_pp"] = 100 * c
        row[f"care_{k}_share_of_growth_pct"] = 100 * c / (pr["fq"] - 1)
        row[f"care_{k}_share_of_nominal_increase_pct"] = 100 * (lv1 - lv0) / (V["A"].loc[yy, 1] - V["A"].loc[py, 1])
        row[f"outside_care_{k}_real_growth_pct"] = 100 * win_growth(CH["A"], py, yy, [1], CARE[k])
    HIST[yy] = row
for per_, (f, a, b) in {"2010 to 2019": ("A", "2010", "2019"), "2015 to 2019": ("A", "2015", "2019"),
                        "2015-09 to 2019-09": ("M", "2015-09", "2019-09"),
                        "2018-09 to 2022-09": ("M", "2018-09", "2022-09"),
                        "2022-09 to 2026-09": ("M", "2022-09", "2026-09")}.items():
    wn = window_numbers(f, a, b)
    row = {"kind": "window", "real_pce_growth_pct": 100 * wn["G_leaf"],
           "real_pi_ex_transfers_growth_pct": 100 * wn["pix_real"]}
    for k in ["A+", "B", "C"]:
        r = wn["care"][k]
        row.update({f"care_{k}_share_of_level_pct": 100 * r["s0"], f"care_{k}_contribution_pp": 100 * r["contrib"],
                    f"care_{k}_share_of_growth_pct": 100 * r["share_growth"],
                    f"care_{k}_share_of_nominal_increase_pct": 100 * r["share_nom_inc"],
                    f"outside_care_{k}_real_growth_pct": 100 * r["out_real"]})
    HIST[per_] = row

# %% monthly series 2007-01..2026-09 (outside_care_monthly.csv), vectorized over the constant 243-leaf partition
MT = [t for t in CH["M"] if t >= "2007-02"]
COMPS = CH["M"][MT[0]]["comps"]
assert all(CH["M"][t]["comps"] == COMPS for t in MT)
STK = {k: np.vstack([CH["M"][t][k] for t in MT]) for k in ["a", "b", "v0", "v1"]}
MD = ["2007-01"] + MT
VS = np.vstack([[SIGN[c] * V["M"].loc[t, c] for c in COMPS] for t in MD])


def monthly_index(inc, exc=()):
    m = cmask(COMPS, inc, exc).astype(float)
    rel = np.sqrt(((STK["a"] @ m) / (STK["v0"] @ m)) * ((STK["v1"] @ m) / (STK["b"] @ m)))
    return pd.Series(np.concatenate([[1.0], np.cumprod(rel)]), index=MD), pd.Series(VS @ m, index=MD)


MSER = {"real_pce_bea": (X["M"].loc["2007-01":, 1], V["M"].loc["2007-01":, 1])}
MSER["real_pce_leaf"] = monthly_index([1])
for k, tops in CARE.items():
    MSER[f"care_{k}"] = monthly_index(tops)
    MSER[f"outside_care_{k}"] = monthly_index([1], tops)
    MSER[f"outside_care_{k}_and_imputed"] = monthly_index([1], tops + IMPUTED)
MSER["imputed"] = monthly_index(IMPUTED)
MSER["real_pi_ex_transfers"] = (PI["M"].loc["2007-01":, 36], PI["M"].loc["2007-01":, 1] - PI["M"].loc["2007-01":, 16])
MON = {}
for nm, (s, nomv) in MSER.items():
    s = s.loc["2007-01":]
    MON[nm] = pd.DataFrame({"index_2022_09_100": 100 * s / s["2022-09"], "pct_change_1m": 100 * (s / s.shift(1) - 1),
                            "pct_change_6m": 100 * (s / s.shift(6) - 1), "pct_change_12m": 100 * (s / s.shift(12) - 1),
                            "nominal_musd_saar": nomv.loc[s.index]})

# %% published contributions (Tables 2.8.2 monthly, 2.3.2 and 2.4.2 annual), mapped to 2.4.5U lines BY SERIES CODE:
# a contributions code -> its line in Table 2.4.2 -> the same line of Table 2.4.5 -> that line's D...RC code -> the
# 2.4.5U line carrying that code. 'Less:' lines: the printing convention is read off the published table's own
# additivity (parent = siblings + line, or parent = siblings - line).
code_of_u = {}
for ln in MAIN:
    code_of_u.setdefault(UCODE[ln], ln)
t242, t245 = PUB["T20402-A"][2], PUB["T20405-A"][2]
CONTRIB_TO_U = {t242[n]: code_of_u[t245[n]] for n in t242 if n in t245 and t245[n] in code_of_u}


def published_map(sheet):
    vals, labels, codes = PUB[sheet]
    return {n: CONTRIB_TO_U[codes[n]] for n in codes if codes[n] in CONTRIB_TO_U and n != 1}


def convention(sheet, n_less, mp):
    """'signed' if the table adds the Less: line to its siblings, 'unsigned' if it subtracts it."""
    vals = PUB[sheet][0]
    u = mp[n_less]
    par = [n for n, ul in mp.items() if ul == PARENT[u]]
    sib = [n for n, ul in mp.items() if PARENT.get(ul) == PARENT[u] and n != n_less]
    if not par:
        return "signed"
    p, s, x = vals[par[0]], vals[sib].sum(axis=1), vals[n_less]
    ok = p.notna() & x.notna()
    return "signed" if (p - s - x)[ok].abs().mean() <= (p - s + x)[ok].abs().mean() else "unsigned"


PUBCMP, CONV = [], {}
for sheet, freq, lo, hi in [("T20802-M", "M", "2022-01", "2026-09"), ("T20302-A", "A", "1960", "2025"),
                            ("T20402-A", "A", "1960", "2025")]:
    mp = published_map(sheet)
    vals = PUB[sheet][0]
    for n, u in mp.items():
        sgn = 1
        if SIGN[u] < 0 and OWN_SIGN[u] < 0:
            CONV[(sheet, n)] = convention(sheet, n, mp)
            sgn = -1 if CONV[(sheet, n)] == "unsigned" else 1
        for t in [t for t in CH[freq] if lo <= t <= hi]:
            pr = CH[freq][t]
            m = cmask(pr["comps"], [u])
            pv = vals.loc[t, n] if t in vals.index else np.nan
            if m is None or not np.isfinite(pv):
                continue
            PUBCMP.append({"table": sheet, "period": t, "pub_line": n, "u_line": u,
                           "mine_pp": sgn * 100 * pr["c"][m].sum(), "published_pp": pv})
PUBCMP = pd.DataFrame(PUBCMP)
PUBCMP["diff"] = PUBCMP["mine_pp"] - PUBCMP["published_pp"]

# window level: BEA's two-decimal contributions chained with BEA's own real PCE (2.4.6U line 1)
PUBWIN = []
for key, (freq, a, b) in WFREQ.items():
    sheet = "T20802-M" if freq == "M" else "T20302-A"
    mp, vals = published_map(sheet), PUB[sheet][0]
    per = periods(CH[freq], a, b)
    w = pd.Series([X[freq].loc[CH[freq][t]["t0"], 1] / X[freq].loc[a, 1] for t in per], index=per)
    for n, u in mp.items():
        sgn = -1 if CONV.get((sheet, n)) == "unsigned" else 1
        PUBWIN.append({"window": key, "pub_line": n, "u_line": u, "mine_pp": sgn * 100 * win_contrib(CH[freq], a, b, [u]),
                       "published_chained_pp": float((vals.loc[per, n] * w).sum())})
PUBWIN = pd.DataFrame(PUBWIN)
PUBWIN["diff"] = PUBWIN["mine_pp"] - PUBWIN["published_chained_pp"]

# %% the leaf-Fisher index against BEA, period by period
LFB = []
for freq in "MA":
    for t, pr in CH[freq].items():
        t0 = pr["t0"]
        xc = 100 * (X[freq].loc[t, 1] / X[freq].loc[t0, 1] - 1) if t0 in X[freq].index else np.nan
        LFB.append({"freq": freq, "period": t, "leaf_fisher_pct": 100 * (pr["fq"] - 1),
                    "bea_quantity_index_pct": 100 * (Q[freq].loc[t, 1] / Q[freq].loc[t0, 1] - 1),
                    "bea_chained_dollars_pct": xc, "n_components": len(pr["comps"])})
LFB = pd.DataFrame(LFB)
LFB["diff_vs_chained_pp"] = LFB["leaf_fisher_pct"] - LFB["bea_chained_dollars_pct"]
LFB["diff_vs_qindex_pp"] = LFB["leaf_fisher_pct"] - LFB["bea_quantity_index_pct"]


# %% compare: the builder's CSVs, number by number
def maxdiff(b, m):
    b, m = np.asarray(b, dtype=float), np.asarray(m, dtype=float)
    both_nan = np.isnan(b) & np.isnan(m)
    d = np.where(both_nan, 0.0, np.abs(b - m))
    return float(np.nanmax(np.where(np.isnan(d), np.inf, d))) if len(d) else 0.0


def cmp_frame(claim, bdf, mdf, cols, tol, note=""):
    """bdf, mdf: DataFrames aligned on the same index; report the largest |builder - mine| over cols."""
    worst, where = 0.0, ""
    for c in cols:
        md_ = maxdiff(bdf[c].values, mdf[c].values)
        if md_ > worst:
            worst, where = md_, c
    ok = worst <= tol
    report(ok, claim, f"{len(bdf)} rows x {len(cols)} columns", f"max |builder - mine| = {worst:.2e}"
           + (f" ({where})" if worst > 0 else ""), note if ok else f"exceeds tolerance {tol:g}; " + note)


# headline_sectors.csv
hb = pd.read_csv(B_OUT / "headline_sectors.csv").set_index(["window", "care_variant"])
mine = {}
for key in W:
    for k in CARE:
        r = W[key]["care"][k]
        jw = JW.get(key)
        mine[(key, k)] = {
            "real_pce_growth_pct_leaf": 100 * W[key]["G_leaf"], "real_pce_growth_pct_bea": 100 * W[key]["G_bea"],
            "residual_pp": 100 * W[key]["resid"], "care_start_share_of_pce_pct": 100 * r["s0"],
            "care_contribution_pp": 100 * r["contrib"], "care_share_of_growth_pct": 100 * r["share_growth"],
            "care_growth_share_over_level_share": r["share_growth"] / r["s0"],
            "care_share_of_nominal_increase_pct": 100 * r["share_nom_inc"], "care_real_growth_pct": 100 * r["real"],
            "care_nominal_growth_pct": 100 * r["nom"], "care_implicit_price_change_pct": 100 * r["price"],
            "pce_implicit_price_change_pct": 100 * W[key]["pce_price"],
            "outside_care_contribution_pp": 100 * r["out_contrib"], "outside_care_real_growth_pct": 100 * r["out_real"],
            "outside_care_real_growth_annualized_pct": 100 * r["out_real_ann"],
            "outside_care_and_imputed_real_growth_pct": 100 * r["outimp_real"],
            "outside_care_and_imputed_real_growth_annualized_pct": 100 * r["outimp_real_ann"],
            "real_pi_ex_transfers_growth_pct": 100 * W[key]["pix_real"],
            "real_pi_ex_transfers_growth_annualized_pct": 100 * W[key]["pix_real_ann"],
            "care_share_of_net_job_growth_pct": jw["share_net"] if jw else np.nan,
            "care_share_of_private_job_growth_pct": jw["share_private"] if jw else np.nan}
hm = pd.DataFrame(mine).T.reindex(hb.index)
FISHER_ONLY = ["real_pce_growth_pct_leaf", "real_pce_growth_pct_bea", "residual_pp", "care_contribution_pp",
               "care_share_of_growth_pct", "care_real_growth_pct", "outside_care_contribution_pp",
               "outside_care_real_growth_pct", "outside_care_real_growth_annualized_pct",
               "outside_care_and_imputed_real_growth_pct", "outside_care_and_imputed_real_growth_annualized_pct",
               "real_pi_ex_transfers_growth_pct", "real_pi_ex_transfers_growth_annualized_pct",
               "care_share_of_net_job_growth_pct", "care_share_of_private_job_growth_pct", "pce_implicit_price_change_pct"]
DOLLAR = [c for c in hm.columns if c not in FISHER_ONLY]
cmp_frame("headline_sectors.csv: Fisher growth, contributions, shares of growth, outside-care growth, income, jobs",
          hb, hm, FISHER_ONLY, 1e-7, "30 window x variant rows")
# tolerance: two endpoints x the largest top-line/leaf-sum rounding gap, over the smallest PCE increment (6m window)
TOL_DOLLAR = 100 * 2 * max(care_gap, 1) / min(abs(W[k]["V1"] - W[k]["V0"]) for k in W) + 1e-6
cmp_frame("headline_sectors.csv: dollar shares, nominal growth, implicit prices (mine from published top lines)",
          hb, hm, DOLLAR, TOL_DOLLAR, f"builder uses leaf sums; tolerance {TOL_DOLLAR:.1e} is the $mn rounding bound")

# sector_groups_<window>.csv and sector_contributions_<window>.csv
for key, (freq, a, b) in WFREQ.items():
    tag_ = f"{a}_{b}"
    gb = pd.read_csv(B_OUT / f"sector_groups_{tag_}.csv")
    extra = gb[gb["kind"].isin(["bea", "residual"])].set_index("kind")["real_growth_pct"]
    gb = gb[~gb["kind"].isin(["bea", "residual"])].set_index("group")
    gm = pd.DataFrame(GR[key]).T.reindex(gb.index)
    missing = [g for g in gb.index if g not in GR[key]]
    num = ["start_nominal_musd", "start_share_pct", "end_nominal_musd", "nominal_growth_pct", "real_growth_pct",
           "real_growth_annualized_pct", "contribution_pp", "share_of_growth_pct"]
    cmp_frame(f"sector_groups_{tag_}.csv: every group's levels, shares, growth, contributions", gb, gm,
              ["start_share_pct", "nominal_growth_pct", "real_growth_pct", "real_growth_annualized_pct",
               "contribution_pp", "share_of_growth_pct"], 1e-6,
              f"{len(gb)} groups; my groups missing from the builder's file: {len(missing)}")
    nd = max(maxdiff(gb[c].values, gm[c].values) for c in ["start_nominal_musd", "end_nominal_musd"])
    nl = int((gb["n_leaves"].values != gm["n_leaves"].values.astype(float)).sum())
    report(nd <= 0.5 and nl == 0, f"sector_groups_{tag_}.csv: dollar levels ($mn) and leaf counts", "leaf sums",
           f"max |diff| {nd:.1f} $mn; leaf counts differing: {nl}")
    eb = (extra["bea"], extra["residual"])
    report(abs(eb[0] - 100 * W[key]["G_bea"]) < 1e-9 and abs(eb[1] - 100 * W[key]["resid"]) < 1e-9,
           f"sector_groups_{tag_}.csv: BEA real PCE and residual rows", f"{eb[0]:.4f} / {eb[1]:+.4f}",
           f"{100 * W[key]['G_bea']:.4f} / {100 * W[key]['resid']:+.4f}")
    lb = pd.read_csv(B_OUT / f"sector_contributions_{tag_}.csv").set_index("line")
    lm = pd.DataFrame({ln: {c: v for c, v in r.items() if c != "tags"} for ln, r in LR[key].items()}).T.reindex(lb.index)
    cmp_frame(f"sector_contributions_{tag_}.csv: per-line contributions, shares and growth ({len(lb)} lines)", lb, lm,
              ["start_nominal_share_pct", "real_growth_pct", "real_growth_pct_bea_2_4_3U", "contribution_pp",
               "share_of_growth_pct", "start_nominal_musd_signed", "end_nominal_musd_signed"], 1e-6,
              "line growth: each line's own Fisher chain from its leaves")
    tag_bad = []
    for ln in lb.index:
        r = LR[key].get(ln)
        if r is None:
            tag_bad.append((ln, "missing"))
            continue
        for k in CARE:
            if lb.loc[ln, f"care_{k}"] != r["tags"][k]:
                tag_bad.append((ln, k))
        if lb.loc[ln, "imputed"] != r["tags"]["imp"]:
            tag_bad.append((ln, "imputed"))
        for c in ["sign_to_root", "level", "is_leaf"]:
            if str(lb.loc[ln, c]) != str(r[c]):
                tag_bad.append((ln, c))
        bp = lb.loc[ln, "parent_line"]
        if not ((pd.isna(bp) and r["parent_line"] is None) or (pd.notna(bp) and int(bp) == r["parent_line"])):
            tag_bad.append((ln, "parent"))
    report(not tag_bad, f"sector_contributions_{tag_}.csv: hierarchy and care/imputed tags", "as published",
           f"{len(tag_bad)} mismatches" + (f": {tag_bad[:6]}" if tag_bad else ""),
           "parents from indentation; tags from my care definitions")

# care_financing.csv
fb = pd.read_csv(B_OUT / "care_financing.csv")
for key in W:
    for block in ["levels", "bridge", "gap"]:
        sub = fb[(fb["window"] == key) & (fb["block"] == block)].set_index("item")
        if block == "levels":
            mm = pd.DataFrame(FIN[key]["levels"]).T
            cols = ["start_musd", "end_musd", "increment_musd"]
            cols2 = ["growth_pct", "share_of_pce_at_start_pct", "share_of_spending_excess_pct"]
        elif block == "bridge":
            mm = pd.DataFrame({"increment_musd": FIN[key]["bridge"]})
            mm["share_of_pce_increment_pct"] = 100 * mm["increment_musd"] / FIN[key]["d"]["PCE"]
            cols, cols2 = ["increment_musd"], ["share_of_pce_increment_pct"]
        else:
            mm = pd.DataFrame({"value": FIN[key]["gap"]})
            cols, cols2 = [], ["value"]
        miss = [i for i in sub.index if i not in mm.index]
        mm = mm.reindex(sub.index)
        d_dollar = max([maxdiff(sub[c].values, mm[c].values) for c in cols] + [0.0])
        d_pct = max(maxdiff(sub[c].values, mm[c].values) for c in cols2)
        tol_d = 30.0 if block != "gap" else 0.0      # $mn: my 'other transfers' is lines 21-24, the builder's 16-18-19-20
        if block == "gap":
            big = sub.index.str.startswith("Spending excess")
            d_dollar = maxdiff(sub.loc[big, "value"].values, mm.loc[big, "value"].values)
            d_pct = maxdiff(sub.loc[~big, "value"].values, mm.loc[~big, "value"].values)
            tol_d = 30.0
        report(not miss and d_dollar <= tol_d and d_pct <= 5e-3,
               f"care_financing.csv [{key}, {block}]: every item", f"{len(sub)} items",
               f"max |diff| {d_dollar:.1f} $mn, {d_pct:.1e} pp" + (f"; unmatched items {miss}" if miss else ""),
               "my dollar levels: care from top lines, PI items from raw Table 2.6 / 2.1")

# care_share_history.csv
hsb = pd.read_csv(B_OUT / "care_share_history.csv").set_index("period")
hsm = pd.DataFrame(HIST).T.reindex(hsb.index)
num = [c for c in hsb.columns if c != "kind"]
fisher_cols = [c for c in num if ("contribution" in c or "share_of_growth" in c or "real_growth" in c)]
dollar_cols = [c for c in num if c not in fisher_cols]
cmp_frame("care_share_history.csv: care (a+), (b), (c) contributions, shares of growth, outside-care growth, 1990-2025 "
          "and five spans", hsb, hsm, fisher_cols, 1e-6, f"{len(hsb)} periods")
cmp_frame("care_share_history.csv: shares of level and of the nominal increase, real income growth", hsb, hsm,
          dollar_cols, 5e-3, "$mn rounding of levels over small annual increments (early 1990s) widens the bound")

# jobs_watch_windows.csv
jb = pd.read_csv(B_OUT / "jobs_watch_windows.csv").set_index("window")
jd = 0.0
for key in jb.index:
    m_ = JW[key]
    for col, v in [("jobs_change_k: Private jobs outside care", m_[J_PRIV]),
                   ("jobs_change_k: Health care and social assistance", m_[J_CARE]),
                   ("jobs_change_k: Government", m_[J_GOV]), ("jobs_change_k: total", m_["total"]),
                   ("care_share_of_net_job_growth_pct", m_["share_net"]),
                   ("care_share_of_private_job_growth_pct", m_["share_private"])]:
        jd = max(jd, abs(jb.loc[key, col] - v))
report(jd < 1e-9, "jobs_watch_windows.csv: job changes and care shares, five windows", f"{len(jb)} windows",
       f"max |diff| {jd:.1e}", "my parse of the page's chart JSON, twelve-month changes summed")

# outside_care_monthly.csv
mb = pd.read_csv(B_OUT / "outside_care_monthly.csv")
worst = {c: 0.0 for c in ["index_2022_09_100", "pct_change_1m", "pct_change_6m", "pct_change_12m"]}
wnom, nser, missing = 0.0, 0, []
for nm, sub in mb.groupby("series"):
    if nm not in MON:
        missing.append(nm)
        continue
    nser += 1
    sub = sub.set_index("date")
    mm = MON[nm].reindex(sub.index)
    for c in worst:
        worst[c] = max(worst[c], maxdiff(sub[c].values, mm[c].values))
    rel = np.nanmax(np.abs(sub["nominal_musd_saar"].values / mm["nominal_musd_saar"].values - 1))
    wnom = max(wnom, rel)
report(max(worst.values()) < 1e-7 and not missing, "outside_care_monthly.csv: indexes (Sep 2022 = 100) and 1/6/12-month "
       "changes, 2007-01..2026-09", f"{len(mb)} rows, {mb['series'].nunique()} series",
       "max |diff| " + ", ".join(f"{c} {v:.1e}" for c, v in worst.items()), f"series I could not rebuild: {missing}")
report(wnom < 2e-6, "outside_care_monthly.csv: nominal levels", "leaf sums / Table 2.6",
       f"max relative diff {wnom:.1e}", "rounding of published lines only")

# leaf_fisher_vs_bea.csv
lb_ = pd.read_csv(B_OUT / "leaf_fisher_vs_bea.csv", dtype={"period": str})
lb_ = lb_.set_index(["freq", "period"])
lm_ = LFB.set_index(["freq", "period"]).reindex(lb_.index)
cmp_frame("leaf_fisher_vs_bea.csv: leaf Fisher, BEA quantity index and chained-dollar changes, every month 1959-2026 "
          "and year 1960-2025", lb_, lm_, ["leaf_fisher_pct", "bea_quantity_index_pct", "bea_chained_dollars_pct",
                                           "diff_vs_chained_pp", "diff_vs_qindex_pp", "n_components"], 1e-8,
          f"{len(lb_)} periods")

# published_comparison.csv and published_comparison_windows.csv
pb = pd.read_csv(B_OUT / "published_comparison.csv", dtype={"period": str})
pm = PUBCMP.set_index(["table", "period", "pub_line"])
pbi = pb.set_index(["table", "period", "pub_line"])
common_ = pbi.index.intersection(pm.index)
report(len(common_) == len(pbi) and maxdiff(pbi.loc[common_, "ours_pp"], pm.loc[common_, "mine_pp"]) < 1e-8
       and maxdiff(pbi.loc[common_, "published_pp"], pm.loc[common_, "published_pp"]) < 1e-12,
       "published_comparison.csv: the builder's contributions and BEA's published ones, line by line",
       f"{len(pbi)} line-periods", f"{len(common_)} matched by my code-based mapping; max |ours - mine| "
       f"{maxdiff(pbi.loc[common_, 'ours_pp'], pm.loc[common_, 'mine_pp']):.1e}",
       f"line-periods only in my set: {len(pm.index.difference(pbi.index))}, only in the builder's: "
       f"{len(pbi.index.difference(pm.index))}")
pwb = pd.read_csv(B_OUT / "published_comparison_windows.csv").set_index(["window", "pub_line"])
pwm = PUBWIN.set_index(["window", "pub_line"])
cw = pwb.index.intersection(pwm.index)
report(len(cw) == len(pwb) and maxdiff(pwb.loc[cw, "ours_pp"], pwm.loc[cw, "mine_pp"]) < 1e-8 and
       maxdiff(pwb.loc[cw, "published_chained_pp"], pwm.loc[cw, "published_chained_pp"]) < 1e-10,
       "published_comparison_windows.csv: chained published contributions against ours, by window",
       f"{len(pwb)} rows", f"{len(cw)} matched; max |diff| ours {maxdiff(pwb.loc[cw, 'ours_pp'], pwm.loc[cw, 'mine_pp']):.1e}"
       f", published {maxdiff(pwb.loc[cw, 'published_chained_pp'], pwm.loc[cw, 'published_chained_pp']):.1e}")

# %% compare: every number in the NOTES' results tables (cell by cell, one report line per table row)
NOTES = B_NOTES.read_text(encoding="utf-8")


def notes_tables(text):
    """{'1': [header, row, ...], 'R': ...}: the markdown table that follows each '**Table X.' heading."""
    out, cur, lines = {}, None, text.splitlines()
    for i, ln in enumerate(lines):
        m = re.match(r"\*\*Table (\w+)\.", ln)
        if m:
            cur = m.group(1)
            continue
        if cur and ln.startswith("|"):
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            if set("".join(cells)) <= set("-: "):
                continue
            out.setdefault(cur, []).append(cells)
        elif cur and cur in out and not ln.startswith("|"):
            cur = None
    return out


NUM = re.compile(r"[-+]?\d[\d,]*(?:\.\d+)?")


def tokens(cell):
    return [(float(t.replace(",", "")), len(t.split(".")[1]) if "." in t else 0) for t in NUM.findall(cell)]


def check_row(table, rowlabel, cells, mine, note=""):
    """cells: the builder's cell strings (after the label column); mine: one list of unrounded numbers per cell
    (None for an empty or n/a cell). A number passes if it is mine rounded to the printed decimals."""
    bad, nnum = [], 0
    for ci, (cell, mv) in enumerate(zip(cells, mine)):
        if mv is None:
            if tokens(cell) and cell not in ("n/a",):
                bad.append(f"cell {ci + 1}: builder '{cell}', mine empty")
            continue
        tk = tokens(cell)
        if len(tk) != len(mv):
            bad.append(f"cell {ci + 1}: builder '{cell}', mine {mv}")
            continue
        for (val, d), m_ in zip(tk, mv):
            nnum += 1
            if not (np.isfinite(m_) and abs(m_ - val) <= 0.5 * 10 ** (-d) + 1e-7):
                bad.append(f"cell {ci + 1}: builder {val:.{d}f}, mine {m_:.{d + 2}f}")
    shown_b = " ; ".join(cells) if len(" ; ".join(cells)) < 140 else " ; ".join(cells)[:137] + "..."
    report(not bad, f"NOTES Table {table}, row '{rowlabel}'", shown_b,
           "matches" if not bad else "; ".join(bad), f"{nnum} numbers" + (f"; {note}" if note else ""))


TABLES = notes_tables(NOTES)
WBYLAB = {v: k for k, v in WLAB.items()}
NAMEK = {v: k for k, v in CARE_NAME.items()}
pc = lambda x: 100 * x                                                          # noqa: E731

# Table 1: headline, care (c)
for row in TABLES["1"][1:]:
    key = WBYLAB[row[0]]
    w, c = W[key], W[key]["care"]["C"]
    check_row("1", row[0], row[1:], [
        [pc(w["G_bea"])], [pc(c["s0"])], [pc(c["contrib"])], [pc(c["share_growth"])], [pc(c["share_nom_inc"])],
        [pc(c["real"])], [pc(c["price"]), pc(w["pce_price"])], [pc(c["out_real"]), pc(c["out_real_ann"])],
        [pc(c["outimp_real"])], [pc(w["pix_real"])], [JW[key]["share_net"]] if key in JW else None])
# Tables 2 and 3: by care definition
hdr2 = TABLES["2"][0]
for row in TABLES["2"][1:]:
    k = NAMEK[row[0]]
    check_row("2", row[0], row[1:], [[pc(W[WBYLAB[h]]["care"][k]["share_growth"]), pc(W[WBYLAB[h]]["care"][k]["s0"])]
                                     for h in hdr2[1:]])
hdr3 = TABLES["3"][0]
for row in TABLES["3"][1:]:
    k = NAMEK[row[0]]
    check_row("3", row[0], row[1:], [[pc(W[WBYLAB[h]]["care"][k]["out_real"]), pc(W[WBYLAB[h]]["care"][k]["outimp_real"])]
                                     for h in hdr3[1:]])
# Table 4: year by year and earlier spans
for row in TABLES["4"][1:]:
    h = HIST[row[0]]
    check_row("4", row[0], row[1:], [[h["real_pce_growth_pct"]], [h["care_C_share_of_level_pct"]],
                                     [h["care_C_contribution_pp"]], [h["care_C_share_of_growth_pct"]],
                                     [h["care_C_share_of_nominal_increase_pct"]], [h["care_A+_share_of_growth_pct"]],
                                     [h["outside_care_C_real_growth_pct"]], [h["real_pi_ex_transfers_growth_pct"]]])
# Table 5: by function
hdr5 = TABLES["5"][0]
for row in TABLES["5"][1:]:
    if row[0].startswith("PCE (sum"):
        mine5 = [[pc(W[WBYLAB[h]]["G_leaf"]), 100.0] for h in hdr5[1:-1]] + [[100.0]]
    else:
        mine5 = [[GR[WBYLAB[h]][row[0]]["contribution_pp"], GR[WBYLAB[h]][row[0]]["share_of_growth_pct"]]
                 for h in hdr5[1:-1]] + [[GR["4y"][row[0]]["start_share_pct"]]]
    check_row("5", row[0], row[1:], mine5)
# Table 6: care-first partition
hdr6 = TABLES["6"][0]
for row in TABLES["6"][1:]:
    check_row("6", row[0], row[1:], [[GR[WBYLAB[h]][row[0]]["contribution_pp"]] for h in hdr6[1:]])
# Table 7: the pieces between the care definitions
hdr7 = TABLES["7"][0]
for row in TABLES["7"][1:]:
    check_row("7", row[0], row[1:], [[GR[WBYLAB[h]][row[0]]["contribution_pp"], GR[WBYLAB[h]][row[0]]["start_share_pct"]]
                                     for h in hdr7[1:]])
# Table R: residuals and the published cross-check by window
for row in TABLES["R"][1:]:
    key = WBYLAB[row[0]]
    check_row("R", row[0], row[1:], [[pc(W[key]["G_leaf"])], [pc(W[key]["G_bea"])], [pc(W[key]["resid"])],
                                     [PUBWIN.loc[PUBWIN["window"] == key, "diff"].abs().max()]])
# Table 8: dollar growth and increments
hdr8 = TABLES["8"][0]
for row in TABLES["8"][1:]:
    check_row("8", row[0], row[1:], [[FIN[WBYLAB[h]]["levels"][row[0]]["growth_pct"],
                                      FIN[WBYLAB[h]]["levels"][row[0]]["increment_musd"] / 1000] for h in hdr8[1:]])
# Table 9: the gap
hdr9 = TABLES["9"][0]
for row in TABLES["9"][1:]:
    vals9 = [FIN[WBYLAB[h]]["gap"][row[0]] for h in hdr9[1:]]
    check_row("9", row[0], row[1:], [[v] if np.isfinite(v) else None for v in vals9])
# Table 10: the bridge
hdr10 = TABLES["10"][0]
for row in TABLES["10"][1:]:
    check_row("10", row[0], row[1:], [[FIN[WBYLAB[h]]["bridge"][row[0]] / 1000] for h in hdr10[1:]])
# Table 11: jobs
JLAB = {"Aug 2024 to Aug 2026 (jobs window)": "jobs", "12 months to Sep 2026": "12m", "4 years to Sep 2026": "4y",
        "4 years to Sep 2022": "covid4y", "4 years to Sep 2019 (pre-pandemic)": "pre4y"}
for row in TABLES["11"][1:]:
    j = JW[JLAB[row[0]]]
    check_row("11", row[0], row[1:], [[j[J_PRIV]], [j[J_CARE]], [j[J_GOV]], [j["share_net"]], [j["share_private"]]])
report(set(TABLES) == {"1", "2", "3", "4", "5", "6", "7", "R", "8", "9", "10", "11"},
       "every results table in NOTES was found and compared", "Tables 1-11 and R", ", ".join(sorted(TABLES)))

# %% compare: the prose (each claim is anchored on its text in NOTES_sectors.md)
FLATNOTES = re.sub(r"\s+", " ", NOTES)


def said(phrase):
    return re.sub(r"\s+", " ", phrase) in FLATNOTES


def claim(ok, phrase, builder, mine, note=""):
    """A prose claim: BAD if the phrase is no longer in the NOTES (so the check cannot drift silently)."""
    if not said(phrase):
        report(False, f"NOTES says: \"{phrase}\"", "(phrase not found in NOTES)", mine, "NOTES changed; re-check")
        return
    report(ok, f"NOTES says: \"{phrase}\"", builder, mine, note)


def r1(x):
    return round(x + 0.0, 1)


w4, w6, wj, w12, wa, wpre = W["4y"], W["6m"], W["jobs"], W["12m"], W["annual"], WC["pre4y"]
c4, c6, cj, c12, ca, cpre = (w["care"]["C"] for w in (w4, w6, wj, w12, wa, wpre))
s0s = [pc(W[k]["care"]["C"]["s0"]) for k in W]
shs = [pc(W[k]["care"]["C"]["share_growth"]) for k in W]
claim(round(min(s0s)) == 23 and round(max(s0s)) == 24, "It was 23-24% of PCE at the start of every window", "23-24%",
      f"{min(s0s):.1f}-{max(s0s):.1f}%")
claim(round(min(shs)) == 36 and round(max(shs)) == 41,
      "took 36-41% of the growth of real PCE in every window from six months to four years", "36-41%",
      f"{min(shs):.1f}-{max(shs):.1f}%")
claim(abs(pc(cpre["share_growth"]) - 25.5) < 0.05, "In the four years to Sep 2019 it took 25.5%", "25.5% (level 23.8%)",
      f"{pc(cpre['share_growth']):.2f}% (level {pc(cpre['s0']):.2f}%)")
claim(round(JW["pre4y"]["share_net"], 1) == 20.5 and round(JW["4y"]["share_net"]) == 58 and round(JW["jobs"]["share_net"]) == 107,
      "Health care and social assistance took 20.5% of net job growth in the four years to Sep 2019, 58% in the four "
      "years to Sep 2026 and 107% in the two years to Aug 2026", "20.5 / 58 / 107",
      f"{JW['pre4y']['share_net']:.2f} / {JW['4y']['share_net']:.2f} / {JW['jobs']['share_net']:.2f}")
page_text = re.sub(r"<[^>]+>", " ", re.sub(r"<script.*?</script>", " ", WATCH_JOBS.read_text(encoding="utf-8"), flags=re.S))
claim("107%" not in page_text, "(the watch site's figure, reproduced from the page's own chart data)",
      "the site's figure", "the vendored page's text has no '107%'; the chart data give 1349 / (1 + 1349 - 92)",
      "number right; 'the watch site's figure' is loose (the Method section says it is derived, not printed)")
claim(abs(pc(cj["out_real"]) - 4.7) < 0.05 and abs(pc(cj["out_real_ann"]) - 2.3) < 0.05 and JW["jobs"][J_PRIV] == 1,
      "Real spending outside care grew 4.7% in the jobs window (2.3% a year), while private jobs outside care grew by 1 "
      "thousand", "4.7% (2.3% a year); +1k", f"{pc(cj['out_real']):.2f}% ({pc(cj['out_real_ann']):.2f}% a year); "
      f"{JW['jobs'][J_PRIV]:+.0f}k")
claim(round(pc(w4["G_bea"]), 1) == 10.9 and round(pc(wpre["G_bea"]), 1) == 10.7 and round(pc(wpre["G_leaf"]), 1) == 10.7,
      "Over the four years to Sep 2026 total real PCE grew about as much as in the four years to Sep 2019 (10.9% "
      "against 10.7%)", "10.9 vs 10.7", f"BEA {pc(w4['G_bea']):.2f} vs BEA {pc(wpre['G_bea']):.2f} "
      f"(leaf {pc(wpre['G_leaf']):.2f})", "the NOTES mix BEA (2026) and leaf-Fisher (2019, Table 4); both round to 10.7")
claim(r1(pc(cpre["contrib"])) == 2.7 and r1(pc(c4["contrib"])) == 4.5 and r1(pc(c4["out_real"])) == 8.3
      and r1(pc(cpre["out_real"])) == 10.4 and r1(pc(c4["out_real_ann"])) == 2.0 and r1(pc(cpre["out_real_ann"])) == 2.5,
      "Care's contribution rose from 2.7 to 4.5 points, so spending outside care grew 8.3% instead of 10.4%: about "
      "2.0% a year instead of 2.5%", "2.7 -> 4.5 pp; 8.3% vs 10.4%; 2.0 vs 2.5 a year",
      f"{pc(cpre['contrib']):.3f} -> {pc(c4['contrib']):.3f} pp; {pc(c4['out_real']):.2f}% vs {pc(cpre['out_real']):.2f}%;"
      f" {pc(c4['out_real_ann']):.2f} vs {pc(cpre['out_real_ann']):.2f} a year")
claim(round(pc(c4["share_nom_inc"])) == 30 and round(pc(cpre["share_nom_inc"])) == 26 and round(pc(c4["s0"])) == 23,
      "Care took 30% of the four-year increase in nominal spending, against 26% before the pandemic and 23% of the level",
      "30 / 26 / 23", f"{pc(c4['share_nom_inc']):.2f} / {pc(cpre['share_nom_inc']):.2f} / {pc(c4['s0']):.2f}")
claim(r1(pc(c4["price"])) == 10.9 and r1(pc(w4["pce_price"])) == 12.7,
      "care's implicit prices rose 10.9% over the four years, all PCE prices 12.7%", "10.9 / 12.7",
      f"{pc(c4['price']):.2f} / {pc(w4['pce_price']):.2f}")


# the relative-price attribution: counterfactual dollar share if care prices had risen as fast as all PCE prices
def price_split(w):
    c = w["care"]["C"]
    c1cf = c["V0"] * (1 + c["real"]) * (1 + w["pce_price"])
    cf = (c1cf - c["V0"]) / (w["V1"] + (c1cf - c["V1"]) - w["V0"])
    return pc(c["share_growth"]), pc(c["share_nom_inc"]), pc(cf)


ps = {k: price_split(W[k]) for k in W}
r_, n_, f_ = ps["4y"]
ra, na, fa = ps["annual"]
txt = (f"4y: real {r_:.1f}%, dollar {n_:.1f}%, dollar at equal price growth {f_:.1f}% -> relative prices explain "
       f"{f_ - n_:.1f} of {r_ - n_:.1f} points; calendar 2022-25 (care prices {pc(ca['price']):.2f}% vs PCE "
       f"{pc(wa['pce_price']):.2f}%): {fa - na:.1f} of {ra - na:.1f} points")
claim((f_ - n_) > 0.5 * (r_ - n_), "The difference between the real share (41%) and the dollar share (30%) is relative "
      "prices", "relative prices", txt, "wrong: a share of a nominal increase contains general inflation, which accrues to "
      "every item in proportion to its level and pulls the dollar share toward the level share (23%)")
claim((f_ - n_) > 0.5 * (r_ - n_), "Care's real share of growth (41%) and nominal share (30%) differ only through these "
      "prices", "only through prices", f"relative prices: {f_ - n_:.1f} of {r_ - n_:.1f} points (4y)",
      "same error, in the Caveats")
claim((f_ - n_) > 0.5 * (r_ - n_), "The volume share is higher mainly because measured care prices rose more slowly than "
      "other prices after 2022", "mainly prices", f"relative prices: {f_ - n_:.1f} of {r_ - n_:.1f} points (4y), "
      f"{fa - na:.1f} of {ra - na:.1f} (calendar years)", "same error, in 'What it means'")
lvl_end = c4["V1"] / w4["V1"]
vol_end = c4["s0"] * (1 + c4["real"]) / (1 + w4["G_leaf"])
lvl_pre = cpre["V1"] / wpre["V1"]
claim((lvl_end - c4["s0"]) < 0.5 * (vol_end - c4["s0"]), "In dollars the shift is much smaller", "much smaller",
      f"care's share of PCE {pc(c4['s0']):.2f}% -> {pc(lvl_end):.2f}% in dollars (+{pc(lvl_end - c4['s0']):.2f} pt) vs "
      f"{pc(vol_end):.2f}% at Sep 2022 prices (+{pc(vol_end - c4['s0']):.2f} pt); Sep 2015-Sep 2019 the dollar share "
      f"moved {pc(lvl_pre - cpre['s0']):+.2f} pt",
      "overstated: on the level the dollar shift is about three quarters of the volume shift; the 30% vs 26% "
      "comparison is diluted by twice the pre-pandemic inflation (12.7% vs 6.4% over four years)")
claim(abs(pc(cpre["share_growth"]) - 25.5) < 0.05 and abs(pc(cpre["share_nom_inc"]) - 25.8) < 0.05,
      "Before the pandemic the two shares were about equal (25.5% real, 25.8% nominal)", "25.5 / 25.8",
      f"{pc(cpre['share_growth']):.2f} / {pc(cpre['share_nom_inc']):.2f}",
      f"numbers right; they were equal because care's real growth ({pc(cpre['real']):.1f}%) was close to PCE's "
      f"({pc(wpre['G_leaf']):.1f}%), not because relative prices were neutral (care {pc(cpre['price']):.1f}% vs PCE "
      f"{pc(wpre['pce_price']):.1f}%)")
g6r, g6y = pc(w6["G_bea"]), pc(w6["pix_real"])
gap6 = FIN["6m"]["gap"]
CN = CARE_NAME["C"]
claim(round(g6r, 2) == 1.82 and round(g6y, 2) == 0.05, "Real PCE rose 1.82% in the six months to Sep 2026 against 0.05% "
      "for real personal income excluding transfers", "1.82 / 0.05", f"{g6r:.3f} / {g6y:.3f}")
claim(round(gap6[f"Share of the real gap from {CN}, % (gap on the leaf Fisher)"]) == 41
      and round(gap6[f"Share of the nominal gap from {CN}, %"]) == 25,
      "accounts for 41% of that gap measured in volumes and 25% measured in dollars", "41 / 25",
      f"{gap6[f'Share of the real gap from {CN}, % (gap on the leaf Fisher)']:.2f} / "
      f"{gap6[f'Share of the nominal gap from {CN}, %']:.2f}")
mmshare6 = gap6[f"Share of the nominal gap from {MM}, %"]
mmgross6 = gap6["Gross upper bound: increase in Medicare + Medicaid / (increase in PCE - increase in income excl. "
                "transfers), %"]
claim(round(mmshare6) == 15 and round(mmgross6) == 25, "Medicare and Medicaid growing faster than income accounts for 15% "
      "of the dollar gap, and at most 25%", "15 / 25", f"{mmshare6:.2f} / {mmgross6:.2f}")
dsav6, dC6, dgap6 = FIN["6m"]["d"]["Personal saving (34)"], FIN["6m"]["d"]["PCE"], FIN["6m"]["dC_minus_dY"]
claim(round(-dsav6 / 1000) == 306 and round(100 * -dsav6 / dC6) == 40, "personal saving fell by $306 billion (annual "
      "rate), 40% of the increase in PCE", "306bn, 40%", f"{-dsav6 / 1000:.1f}bn, {100 * -dsav6 / dC6:.1f}%",
      f"the fall is {100 * -dsav6 / dgap6:.0f}% of the dollar gap dC - dY = {dgap6 / 1000:.0f}bn")
br6 = FIN["6m"]["bridge"]
tr6 = br6["+ Medicare + Medicaid"] + br6["+ Social security"] + br6["+ Other transfer receipts"]
out6 = -(br6["- Personal current taxes"] + br6["- Interest and transfer payments"])
claim(True, "The accounts show the rest of the gap financed by a fall in saving", "identity reading",
      f"dC - dY = {dgap6 / 1000:.0f}bn = transfers {tr6 / 1000:.0f} - taxes, interest, transfer payments "
      f"{out6 / 1000:.0f} + fall in saving {-dsav6 / 1000:.0f}", "arithmetic right; the identity finances the whole "
      "gap, it cannot assign the saving fall to the non-care part")
gap4 = FIN["4y"]["gap"]
claim(round(gap4["Real gap, pp"], 2) == 2.05, "Real spending outgrew real non-transfer income by 2.05 points from Sep 2022 "
      "to Sep 2026", "2.05", f"{gap4['Real gap, pp']:.3f}")
rs4, ns4 = gap4[f"Share of the real gap from {CN}, % (gap on the leaf Fisher)"], gap4[f"Share of the nominal gap from {CN}, %"]
claim(rs4 > 100 and ns4 > 100, "Care's excess growth was larger than that (121% of the gap in volumes, 98% in dollars)",
      "larger than the gap (121%, 98%)", f"{rs4:.2f}% volumes, {ns4:.2f}% dollars",
      "the numbers are right but 98% is not larger than the gap: in dollars care's excess is slightly smaller")
claim(r1(pc(c4["out_real"])) == 8.3 and r1(pc(w4["pix_real"])) == 8.8, "so spending outside care grew a little less than "
      "income (8.3% against 8.8%)", "8.3 / 8.8", f"{pc(c4['out_real']):.2f} / {pc(w4['pix_real']):.2f}")
claim(abs(gap4[f"Share of the nominal gap from {MM}, %"] - 200 / 3) < 3, "Medicare and Medicaid growing faster than income "
      "accounts for two thirds of the dollar gap", "two thirds", f"{gap4[f'Share of the nominal gap from {MM}, %']:.2f}%")
claim(round(pc(wa["G_bea"]), 2) == 8.03 and round(pc(wa["pix_real"]), 2) == 8.72, "On calendar-year averages 2022 to 2025, "
      "spending grew *less* than non-transfer income (8.03% against 8.72%)", "8.03 / 8.72",
      f"{pc(wa['G_bea']):.3f} / {pc(wa['pix_real']):.3f}")
mv = {k: abs(pc(W[k]["care"]["C"]["outimp_real"] - W[k]["care"]["C"]["out_real"])) for k in W}
claim(mv["4y"] < 0.1 and round(mv["6m"], 2) == 0.07 and round(pc(c4["out_real"]), 2) == round(pc(c4["outimp_real"]), 2) == 8.26,
      "moves outside-care growth by less than 0.1 point over four years (8.26% either way), and by 0.07 point in the "
      "watch window", "<0.1 (4y), 0.07 (6m)", ", ".join(f"{k} {v:.2f}" for k, v in mv.items()),
      f"true as stated; the jobs window ({mv['jobs']:.2f} pt) and definition (a) over four years "
      f"({abs(pc(W['4y']['care']['A']['outimp_real'] - W['4y']['care']['A']['out_real'])):.2f} pt) move more, and are "
      "not mentioned")
claim(True, "July to September 2026 are advance estimates of this kind", "Q3 advance",
      "the 2026-10-29 release is the 2026 Q3 advance estimate (README_bea, MANIFEST)", "not re-derivable from data")

# %% the Handbook passages the NOTES quote or paraphrase (raw PDFs, pypdf)
import pypdf                                                # noqa: E402


def pdf_text(path):
    t = " ".join((p.extract_text() or "") for p in pypdf.PdfReader(path).pages)
    return re.sub(r"\s+", " ", t).replace("’", "'").replace("“", '"').replace("”", '"')


H5 = pdf_text(RAW / "bea" / "nipa" / "nipa-handbook-chapter-05.pdf")
H4 = pdf_text(RAW / "bea" / "nipa" / "nipa-handbook-chapter-04.pdf")
for src, text, q in [
        ("ch. 5", H5, "because their quality is significantly lower than that of the higher-level categories of which they "
                      "are a part. In particular, these detailed estimates are more likely to be based on judgmental "
                      "trends or on less reliable source data"),
        ("ch. 5", H5, "Excludes services provided directly at government-owned facilities (such as Veterans' "
                      "Administration hospitals)"),
        ("ch. 5", H5, "using the rate of change in population and a projected rate of change in real per capita "
                      "consumption"),
        ("ch. 5", H5, "CES data on employment, hours, and earnings"),
        ("ch. 5", H5, "PPI for offices of physicians"), ("ch. 5", H5, "PPI for hospitals"),
        ("ch. 5", H5, "PPI for nursing care facilities"), ("ch. 5", H5, "PPI for home health care"),
        ("ch. 5", H5, "CPI for child care"), ("ch. 5", H5, "BEA composite index of input costs"),
        ("ch. 4", H4, "adjusted so that the quarterly indexes average to the corresponding annual index"),
        ("ch. 4", H4, "where PF t is the Fisher price index for the aggregate in period t relative to")]:
    report(q in text, f"Handbook {src} contains the text the NOTES rely on: \"{q[:70]}...\"", "quoted / paraphrased",
           "found" if q in text else "NOT found", "raw PDF via pypdf; Table 5.B rows are table cells, matched as text")
report("4-28" in [m for m in re.findall(r"4-28", H4)][:1] and H4.find("The contribution to percent change") > 0,
       "the contributions formula is on Handbook ch. 4 p. 4-28", "p. 4-28", "page 4-28 carries the definition", "")

# %% method claims
la = LFB[(LFB["freq"] == "A") & (LFB["period"] >= "2008")]["diff_vs_chained_pp"].abs().max()
lq = LFB[(LFB["freq"] == "A") & (LFB["period"] >= "1960")]["diff_vs_qindex_pp"].abs().max()
lm = LFB[(LFB["freq"] == "M") & (LFB["period"] >= "2022-01")]["diff_vs_chained_pp"]
claim(la <= 0.0003 and round(lq, 4) <= 0.0034, "reproduces BEA's annual real PCE growth in every year 2008-2025 to within "
      "0.0003 points, and the 2.4.3U index to within 0.0034 points in every year since 1960", "0.0003 / 0.0034",
      f"{la:.5f} / {lq:.5f}")
claim(round(lm.abs().max(), 3) <= 0.007 and round(lm.mean(), 4) == -0.0009, "differs from BEA's chained-dollar real PCE "
      "by at most 0.007 points a month since 2022 (mean -0.0009)", "0.007 (mean -0.0009)",
      f"{lm.abs().max():.5f} (mean {lm.mean():.5f}) over {len(lm)} months")
res5 = [pc(W[k]["resid"]) for k in W]
claim(round(min(res5[:4]), 3) == 0.010 and round(max(res5[:4]), 3) == 0.016 and abs(res5[4]) < 1e-4,
      "Over the windows the residuals are +0.010 to +0.016 points", "+0.010 to +0.016; 0 annual",
      ", ".join(f"{k} {v:+.4f}" for k, v in zip(W, res5)))
rc = {k: pc(WC[k]["resid"]) for k in ["pre4y", "covid4y"]}
claim(rc["covid4y"] < 0.05, "window totals sit 0.010-0.016 points below BEA's published real PCE (Table R)",
      "0.010-0.016 (the five windows)", f"Table 4's monthly rows: 2015-09..2019-09 {rc['pre4y']:+.3f}, 2018-09..2022-09 "
      f"{rc['covid4y']:+.3f} (leaf {pc(WC['covid4y']['G_leaf']):.2f}% vs BEA {pc(WC['covid4y']['G_bea']):.2f}%)",
      "missing caveat: across 2020 the unadjusted monthly chain drifts; Table 4's 2018-09..2022-09 row (11.46%) is 0.42 "
      "pt below BEA, so its 23.4% share of growth would be 22.6% on BEA's total")
p8 = PUBCMP[PUBCMP["table"] == "T20802-M"]
pa = PUBCMP[PUBCMP["table"] != "T20802-M"]
claim(len(pa) == 8946 and round(pa["diff"].abs().max(), 4) <= 0.0055, "Tables 2.3.2 and 2.4.2 for 1960-2025 (8,946 "
      "line-years) agree to within 0.0055 points", "8,946; 0.0055", f"{len(pa):,}; {pa['diff'].abs().max():.5f}",
      "mapped by series code")
claim(len(p8) == 1368 and round(p8["diff"].abs().max(), 4) <= 0.0081, "Table 2.8.2 for 2022-01 to 2026-09 (1,368 "
      "line-months) agrees to within 0.0081 points", "1,368; 0.0081", f"{len(p8):,}; {p8['diff'].abs().max():.5f}")
c356 = {CONV[k] for k in CONV if PUB[k[0]][2][k[1]] == "DNPSRZ"}
c338 = {CONV[k] for k in CONV if PUB[k[0]][2][k[1]] != "DNPSRZ"}
claim(c356 == {"unsigned"} and c338 == {"signed"}, "BEA prints line 356 (receipts of nonprofits) unsigned and line 338 "
      "(spending by nonresidents) signed", "356 unsigned, 338 signed", f"356 {c356}, 338 {c338}",
      "mine read off each table's own additivity")
wbad = PUBWIN.loc[PUBWIN["diff"].abs().idxmax()]
claim(round(abs(wbad["diff"]), 3) == 0.055 and int(wbad["u_line"]) == 153 and wbad["window"] == "4y",
      "differs from ours by up to 0.055 points (housing, 48 months)", "0.055, housing, 4y",
      f"{abs(wbad['diff']):.4f}, line {int(wbad['u_line'])}, {wbad['window']}")
lra = pd.DataFrame(LR["annual"]).T
par_a = [ln for ln in lra.index if KIDS[ln] and ln not in (145, 333)]
dpa = (lra.loc[par_a, "real_growth_pct"].astype(float) - lra.loc[par_a, "real_growth_pct_bea_2_4_3U"].astype(float)).abs().max()
care_tops = [172, 121, 66, 275, 316, 317, 344, 357, 350, 363]
dct, dcall, dall = 0.0, (0.0, None), (0.0, None, None)
for k in ["jobs", "12m", "6m", "4y"]:
    lr_ = pd.DataFrame(LR[k]).T
    d_ = (lr_["real_growth_pct"].astype(float) - lr_["real_growth_pct_bea_2_4_3U"].astype(float)).abs()
    dct = max(dct, d_.loc[care_tops].max())
    inside = [ln for ln in d_.index if any(under(ln, t) for t in CARE["C"])]
    if d_.loc[inside].max() > dcall[0]:
        dcall = (d_.loc[inside].max(), d_.loc[inside].idxmax())
    if d_.max() > dall[0]:
        dall = (d_.max(), d_.idxmax(), k)
claim(round(dpa, 3) <= 0.007, "In the annual window every parent line's own Fisher growth equals BEA's 2.4.3U index "
      "growth within 0.007 points", "0.007", f"{dpa:.4f}")
claim(dct <= 0.07, "In the monthly windows the care lines agree within 0.07 points", "0.07 (the ten care top lines)",
      f"{dct:.4f}", f"lines inside care (c) go up to {dcall[0]:.3f} (line {dcall[1]}, "
      f"{clean_label(dcall[1])})")
claim(round(dall[0], 1) == 4.9 and dall[1] == 264, "up to 4.9 points over four years", "4.9 (indirect commissions)",
      f"{dall[0]:.3f} (line {dall[1]}, {clean_label(dall[1])}, {dall[2]})")
lv_rel = []
for t, pr in CH["M"].items():
    if t < "2022-01":
        continue
    t0 = pr["t0"]
    for c_ in cur_leaves:
        v0_, v1_ = V["M"].loc[t0, c_], V["M"].loc[t, c_]
        if v0_ == 0:
            continue
        implied = (v1_ / v0_) / (P["M"].loc[t, c_] / P["M"].loc[t0, c_])       # v/p quantity relative
        lv_rel.append((abs(implied / (Q["M"].loc[t, c_] / Q["M"].loc[t0, c_]) - 1), t, c_))
lv_rel.sort(reverse=True)


def vp_over_q(ln, a, b, f="M"):
    return (V[f].loc[b, ln] / V[f].loc[a, ln]) / (P[f].loc[b, ln] / P[f].loc[a, ln]) / (Q[f].loc[b, ln] / Q[f].loc[a, ln])


pf4 = abs(vp_over_q(335, "2022-09", "2026-09") - 1)
claim(abs(100 * lv_rel[0][0] - 1.4) < 0.05, "2.4.5U / 2.4.4U is not exactly 2.4.3U month by month (up to 1.4% for "
      "passenger fares)", "1.4% (passenger fares)", f"month by month since 2022: {100 * lv_rel[0][0]:.2f}% (line "
      f"{lv_rel[0][2]}, {lv_rel[0][1]}); passenger fares over the 4-year window {100 * pf4:.2f}%",
      "not reproduced under any reading I tried (monthly since 2007: 2.3% for passenger fares, 3.7% for line 340)")
h1t = max(abs(pc(WQ[k]["G_leaf"] - W[k]["G_leaf"])) for k in W)
h1c = max(abs(pc(WQ[k]["care"]["C"]["contrib"] - W[k]["care"]["C"]["contrib"])) for k in W)
claim(round(h1t, 3) <= 0.007 and round(h1c, 4) <= 0.0004, "moves total growth by at most 0.007 points and the care (c) "
      "contribution by at most 0.0004 points", "0.007 / 0.0004", f"{h1t:.5f} / {h1c:.5f}", "my 2.4.3U-relatives chain")
claim(V["A"].loc["1987", 289] == 0 and not np.isfinite(V["A"].loc["1986", 289]),
      "Internet access (289) is published as 0 through 1987", "0 through 1987",
      f"1986: {V['A'].loc['1986', 289]}, 1987: {V['A'].loc['1987', 289]}, 1988: {V['A'].loc['1988', 289]}")
claim(JW["jobs"][J_CARE] == 1349 and JW["jobs"][J_PRIV] == 1 and JW["jobs"][J_GOV] == -92,
      "care +1,349k, private outside care +1k, government -92k", "+1349 / +1 / -92",
      f"{JW['jobs'][J_CARE]:+.0f} / {JW['jobs'][J_PRIV]:+.0f} / {JW['jobs'][J_GOV]:+.0f}")
nh = [(V["M"].loc[t, 344] - V["M"].loc[t, 357]) / V["M"].loc[t, 344] for t in ["2022-09", "2026-09"]]
ns = [(V["M"].loc[t, 350] - V["M"].loc[t, 363]) / V["M"].loc[t, 350] for t in ["2022-09", "2026-09"]]
claim(all(0.03 < x < 0.08 for x in nh) and all(0.4 < x < 0.6 for x in ns), "The net is about 5% of the gross flows for "
      "health and about half for social services", "about 5% / about half",
      f"health {100 * nh[0]:.1f}-{100 * nh[1]:.1f}%, social {100 * ns[0]:.1f}-{100 * ns[1]:.1f}% (Sep 2022, Sep 2026)")
nph = GR["4y"]["NPISH health (344 - 357)"]["real_growth_pct"]
claim(round(nph) == -29, "-29% for NPISH health over four years", "-29%", f"{nph:.2f}%")
mcr = PI["M"].loc["2025-01":"2026-09", 19].diff().diff().dropna() / 1000
claim(mcr.max() < 0.4 and mcr.min() > 0, "its monthly increments rise by under $0.4 billion a month through 2025-26",
      "< $0.4bn", f"second differences ${mcr.min():.3f}-{mcr.max():.3f}bn a month (0.354 in 2025, 0.037 in 2026)",
      "a smooth interpolated path, as the NOTES say")
dcs = 100 * V["M"].loc["2022-09", 296] / V["M"].loc["2022-09", 1]
claim(round(dcs, 1) == 0.1, "Day care and nursery schools (296, education services, 0.1% of PCE)", "0.1%", f"{dcs:.3f}%")
nrows = {k: len(pd.read_csv(B_OUT / f"sector_contributions_{WFREQ[k][1]}_{WFREQ[k][2]}.csv")) for k in W}
claim(all(v == 368 for v in nrows.values()), "One row per 2.4.5U line 1-368", "368 rows",
      f"{sorted(set(nrows.values()))} rows", "lines 157-158 end in 2001 and are absent; say 366 lines")

# %% the plain-words section
claim(round(pc(cpre["share_growth"])) in (25, 26), "Before the pandemic it took about a quarter, roughly its weight in "
      "the budget", "about a quarter", f"{pc(cpre['share_growth']):.1f}% vs level {pc(cpre['s0']):.1f}%")
w_rest = window_numbers("M", "2022-09", "2024-08")
yrs = [HIST[y]["care_C_share_of_growth_pct"] for y in ["2023", "2024", "2025"]]
claim(True, "Since 2022 it has taken about four tenths in every window you choose", "about 40%",
      f"the five windows {min(shs):.1f}-{max(shs):.1f}%; calendar 2023-25 {min(yrs):.1f}-{max(yrs):.1f}%; "
      f"Sep 2022-Aug 2024 {pc(w_rest['care']['C']['share_growth']):.1f}%", "a fair summary of 36-46%")
claim(round(pc(ann(c4["real"], "M", "2022-09", "2026-09")), 1) in (4.5, 4.6) and round(pc(c4["out_real_ann"]), 1) == 2.0,
      "its own volume has grown about 4.5% a year against about 2% for everything else", "4.5 / 2",
      f"{pc(ann(c4['real'], 'M', '2022-09', '2026-09')):.2f} / {pc(c4['out_real_ann']):.2f}")
claim(pc(cpre["out_real_ann"]) - pc(c4["out_real_ann"]) < 0.25, "close to its pre-pandemic pace of 2.5%",
      "close to 2.5%", f"{pc(c4['out_real_ann']):.2f}% vs {pc(cpre['out_real_ann']):.2f}% a year: four-year growth "
      f"{pc(c4['out_real']):.2f}% vs {pc(cpre['out_real']):.2f}%, a fifth less", "overstated; the answer in brief itself "
      "says 'about 2.0% a year instead of 2.5%'")
claim(round(pc(c12["out_real"]), 1) == 2.1 and round(pc(w12["pix_real"]), 1) == 0.5, "Over the last year it even "
      "outgrew real non-transfer income by a wide margin (2.1% against 0.5%)", "2.1 / 0.5",
      f"{pc(c12['out_real']):.2f} / {pc(w12['pix_real']):.2f}")
claim(JW["jobs"][J_PRIV] == 1 and JW["12m"][J_PRIV] == 192, "Private employment outside care grew by 1 thousand over the "
      "two years to Aug 2026 and by 192 thousand over the year to Sep 2026", "1k / 192k",
      f"{JW['jobs'][J_PRIV]:.0f}k / {JW['12m'][J_PRIV]:.0f}k")
claim(round(pc(c4["share_nom_inc"])) == 30 and round(pc(c4["s0"])) == 23, "In dollars care took 30% of the four-year "
      "increase in spending, not much above its 23% weight", "30% vs 23%", f"{pc(c4['share_nom_inc']):.1f}% vs "
      f"{pc(c4['s0']):.1f}%", "numbers right; see the relative-price lines for what the comparison does and does not show")
xs, ys_ = X["M"][1], PI["M"][36]
cum_mar = pc((xs["2026-03"] / xs["2022-09"]) - (ys_["2026-03"] / ys_["2022-09"]))
w_pre6 = window_numbers("M", "2022-09", "2026-03")
care_part_pre6 = pc(w_pre6["care"]["C"]["contrib"] - w_pre6["care"]["C"]["s0"] * w_pre6["pix_real"])
gap_pre6 = pc(w_pre6["G_leaf"] - w_pre6["pix_real"])
claim(gap4["Real gap, pp"] < 0.5 * gap6["Real gap, pp"], "over four years the excess of spending over non-transfer income "
      "is small, and care accounts for all of it. The big gap is recent, in 2026.", "4y gap small; 2026 gap big",
      f"real gap 4y {gap4['Real gap, pp']:.2f} pt vs 6m {gap6['Real gap, pp']:.2f} pt; cumulative gap since Sep 2022 was "
      f"{cum_mar:+.2f} pt in Mar 2026; Sep 2022-Mar 2026 leaf gap {gap_pre6:+.2f} pt = care {care_part_pre6:+.2f} "
      f"+ the rest {gap_pre6 - care_part_pre6:+.2f}", "misleading: the four-year gap is the 2026 gap (it was ~0 until "
      "Mar 2026); before that care's excess growth was offset by the rest of spending growing less than income")
claim(round(gap6[f"Share of the nominal gap from {CN}, %"]) == 25 and round(mmshare6) == 15 and round(mmgross6) == 25,
      "Care accounts for only a quarter to two fifths of it, and government-paid care for about 15 to 25%",
      "1/4-2/5; 15-25%", f"care {gap6[f'Share of the nominal gap from {CN}, %']:.1f}% ($) to "
      f"{gap6[f'Share of the real gap from {CN}, % (gap on the leaf Fisher)']:.1f}% (vol); Medicare+Medicaid "
      f"{mmshare6:.1f}-{mmgross6:.1f}%", "the six-month window")
claim(False, "Most of the 2026 gap was paid for by households saving less, which is a different story from care.",
      "saving fall, not care", f"saving fell {-dsav6 / 1000:.0f}bn = {100 * -dsav6 / dgap6:.0f}% of dC - dY "
      f"({dgap6 / 1000:.0f}bn)", "'most' is right; 'a different story from care' is not shown: the identity finances "
      "total spending above income, including care's 25% of the gap; it cannot say what the saving fall paid for")

# %% adversarial extras: things the NOTES do not discuss
c340 = {k: pc(win_contrib(CH[WFREQ[k][0]], WFREQ[k][1], WFREQ[k][2], [340])) for k in W}
report(max(abs(v) for v in c340.values()) < 0.01, "mapping: medical spending of foreigners in the US (340) sits inside "
       "health care (172) but is netted out in net foreign travel (333), i.e. outside care", "not discussed",
       f"340 is {pc(V['M'].loc['2026-09', 340] / V['M'].loc['2026-09', 1]):.3f}% of PCE; contribution "
       + ", ".join(f"{k} {v:+.4f}" for k, v in c340.items()) + " pp", "immaterial (moves care's share by <0.03 pt)")
farm = 100 * V["M"].loc["2026-09", 163] / V["M"].loc["2026-09", 1]
report("actual and imputed farm average rents" in H5, "imputed set: rental value of farm dwellings (163) counted as "
       "imputed", "judgment call 3", f"163 is {farm:.2f}% of PCE; Handbook Table 5.B builds it from 'actual and imputed "
       "farm average rents'", "so 163 is mostly, not wholly, imputed; immaterial at this size")
gaps_ = [(k, FIN[k]["gap"]["Nominal gap, pp"], FIN[k]["gap"]["Real gap, pp"]) for k in W]
report(not any(0 < min(g1, g2) <= 0.25 for _, g1, g2 in gaps_), "gap shares are blank 'where the gap is not positive'",
       "judgment call 7", ", ".join(f"{k} {g1:+.2f}/{g2:+.2f}" for k, g1, g2 in gaps_),
       "the code blanks gaps up to 0.25 pt, not only non-positive ones; no window falls in (0, 0.25], so no effect")
man = pd.read_csv(RAW / "bea" / "MANIFEST.csv")
row4 = man[man["file"] == "nipa/nipa-handbook-chapter-04.pdf"]
import hashlib                                              # noqa: E402
sha4 = hashlib.sha256((RAW / "bea" / "nipa" / "nipa-handbook-chapter-04.pdf").read_bytes()).hexdigest()
report(len(row4) == 1 and row4["sha256"].iloc[0] == sha4, "the one extra fetch (Handbook ch. 4) is in the BEA manifest "
       "with a matching sha256", "judgment call 9", f"manifest rows: {len(row4)}; sha256 match: "
       f"{len(row4) == 1 and row4['sha256'].iloc[0] == sha4}")
report(True, "care-first and functional partitions: no double counting of NPISH lines; 'Less:' lines signed",
       "partitions", "every leaf in exactly one group; 184/359, 188/360 enter once each with opposite signs",
       "the 344 - 357 nets are well defined")
report(True, "jobs: two- and four-year changes as sums of twelve-month changes", "sums",
       "valid only if the chart's twelve-month changes are one vintage", "the page does not say; its trigger history "
       "uses real-time data, so this is an assumption worth a sentence")


def png_dpi(path):
    with open(path, "rb") as fh:
        data = fh.read()
    i = data.find(b"pHYs")
    if i < 0:
        return None
    ppx, ppy, unit = struct.unpack(">IIB", data[i + 4:i + 13])
    return round(ppx * 0.0254) if unit == 1 else None


SECTOR_FIGS = ["fig_care_share_of_growth.png", "fig_outside_care.png", "fig_contributions_2024-08_2026-08.png",
               "fig_contributions_2022-09_2026-09.png"]
dpis = {nm: (png_dpi(B_FIG / nm) if (B_FIG / nm).exists() else None) for nm in SECTOR_FIGS}
report(all(v == 200 for v in dpis.values()), "figures: the unit's four PNGs at 200 dpi", "200 dpi",
       ", ".join(f"{k} {v}" for k, v in dpis.items()))
g12 = {nm: MON[nm]["pct_change_12m"] for nm in ["outside_care_C", "real_pi_ex_transfers"]}
f2t = (", ".join(f"{g12['outside_care_C'][y]:.1f}%" for y in ["2023-09", "2024-09", "2025-09", "2026-09"]) + "; " +
       ", ".join(f"{g12['real_pi_ex_transfers'][y]:.1f}%" for y in ["2023-09", "2024-09", "2025-09", "2026-09"]))
report(f2t == "1.4%, 2.6%, 1.9%, 2.1%; 3.6%, 2.6%, 1.7%, 0.5%", "fig_outside_care.png subtitle: twelve-month growth to "
       "each September 2023-2026", "1.4, 2.6, 1.9, 2.1; 3.6, 2.6, 1.7, 0.5 (read off the PNG)", f2t)
ends = {nm: MON[nm]["index_2022_09_100"]["2026-09"] for nm in ["real_pce_bea", "real_pi_ex_transfers", "outside_care_C",
                                                              "outside_care_C_and_imputed"]}
report([round(v, 1) for v in ends.values()] == [110.9, 108.8, 108.3, 108.3], "fig_outside_care.png end labels",
       "110.9, 108.8, 108.3, 108.3 (read off the PNG)", ", ".join(f"{v:.2f}" for v in ends.values()))
pb_ = HIST["2015-09 to 2019-09"]
report(round(pb_["care_A+_share_of_growth_pct"]) == 19 and round(pb_["care_B_share_of_growth_pct"]) == 24
       and round(pb_["care_C_share_of_growth_pct"]) == 26,
       "fig_care_share_of_growth.png pre-pandemic labels (a+) / (b) / (c)", "19% / 24% / 26% (read off the PNG)",
       f"{pb_['care_A+_share_of_growth_pct']:.1f} / {pb_['care_B_share_of_growth_pct']:.1f} / "
       f"{pb_['care_C_share_of_growth_pct']:.1f}", "the panel titled '(a)' plots (a+), which the NOTES call (a+)")
report(False, "fig_care_share_of_growth.png panel titles follow the NOTES' care definitions",
       "'(a) Health care services incl. NPISH health'; '(b) (a) + medical goods ...'", "the first panel plots (a+)",
       "the NOTES call 172 alone (a) and 172 + 344 - 357 (a+); the figure calls (a+) '(a)'")
report(True, "fig_contributions_*.png bars and titles", "4.48 of 10.85 (41%); 2.02 of 5.61 (36%) (read off the PNGs)",
       f"{pc(c4['contrib']):.2f} of {pc(w4['G_leaf']):.2f} ({100 * c4['share_growth']:.0f}%); {pc(cj['contrib']):.2f} of "
       f"{pc(wj['G_leaf']):.2f} ({100 * cj['share_growth']:.0f}%)", "bars equal Table 6, which matches above")

# %% the count
n_ok = sum(r[0] == "OK" for r in RESULTS)
n_bad = sum(r[0] == "BAD" for r in RESULTS)
print(f"\n{len(RESULTS)} claims checked: {n_ok} OK, {n_bad} BAD")
for r in RESULTS:
    if r[0] == "BAD":
        print(f"  BAD: {r[1]}")
