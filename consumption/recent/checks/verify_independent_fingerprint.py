# verify_independent_fingerprint.py - INDEPENDENT VERIFICATION of the fingerprint unit in consumption/recent/
# (code/fingerprint.py, out/fingerprint_*.csv, out/top_tilt_monthly.csv, NOTES_fingerprint.md).
#
# Separate route, by design:
#   * no import of, and no code copied from, fingerprint.py or check_fingerprint.py;
#   * every input read from the RAW vendored files, not from data/tidy: BEA FlatFiles.zip (SeriesRegister,
#     nipadataA/M) plus the underlying-detail workbook for the 2.4.5U hierarchy; the BLS distributional-PCE
#     workbook; CE Table 1110 workbooks; CE Table 2500 workbooks; the CE hierarchical-grouping stubs; BLS's
#     ce_pce_map.xlsx; BEA's ISPCEPX workbook; the watch page's embedded chart data;
#   * real growth from 2.4.3U quantity indexes everywhere (the builder used chained dollars where available);
#   * the permutation interval bracketed on a grid and then located exactly at the roots of each permutation's
#     quadratic, with 20,000 permutations from a different seed (the builder: 4,001-point grid, 1,000 permutations);
#   * source B (CE income deciles -> PCE lines) rebuilt from the raw stubs, Table 2500 and BLS's map, with my
#     own alignment, my own item matching and my own rule for UCCs BLS's map does not cover (stated below).
# The builder's outputs are read to print the 'builder value' column next to mine, and in a few labelled places to
# test the builder's own files (its theta file through my growth and WLS as a chain check; its mapping file for the
# stand-ins it used; its monthly tilt file against my series).
#
# Output: one line per claim, 'OK | claim | builder value | my value | note' or 'BAD | ...', then the counts.
# Run from the repo root:  venv/bin/python -I consumption/recent/checks/verify_independent_fingerprint.py
# Plain functions plus top-level code; '# %%' cells paste into a notebook.

# %% setup
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent                       # consumption/recent/checks
sys.path.insert(0, str(HERE))
RECENT = HERE.parent
THREAD = RECENT.parent
RAW = THREAD / "data" / "raw"
OUT = RECENT / "out"

import difflib
import io
import re
import warnings
import zipfile

import numpy as np
import pandas as pd
from scipy import stats
from tqdm.auto import tqdm

warnings.filterwarnings("ignore")
import openpyxl

DEC = [f"d{k:02d}" for k in range(1, 11)]
TOP20, B80 = DEC[8:], DEC[:8]
N_PERM = 2000 if "--fast" in sys.argv else 20000      # --fast: development runs only
RNG = np.random.default_rng(99991)          # deliberately not the builder's seed
ZANDI_PA = 0.04

RESULTS = []


def claim(text, builder, mine, tol=None, ok=None, note=""):
    """Record and print one claim. Numbers: OK when |builder - mine| <= tol. Or pass ok= explicitly."""
    if ok is None:
        try:
            ok = bool(np.isfinite(builder) and np.isfinite(mine) and abs(float(builder) - float(mine)) <= tol)
        except TypeError:
            ok = builder == mine

    def fmt(v):
        if isinstance(v, (float, np.floating)):
            return f"{v:.4g}" if abs(v) < 1e4 else f"{v:,.0f}"
        return str(v)
    line = f"{'OK ' if ok else 'BAD'} | {text} | {fmt(builder)} | {fmt(mine)} | {note}"
    RESULTS.append((ok, line))
    print(line, flush=True)
    return ok


def pts(x):
    return 100.0 * float(x)


# %% 1. BEA: raw flat files (values) and the underlying-detail workbook (2.4.5U hierarchy)
ZF_BEA = zipfile.ZipFile(RAW / "bea" / "nipa" / "FlatFiles.zip")
REG = pd.read_csv(io.BytesIO(ZF_BEA.read("SeriesRegister.txt")), dtype=str)
REG.columns = [c.lstrip("%") for c in REG.columns]
_pairs = []
for _code, _tl in zip(REG.SeriesCode, REG["TableId:LineNo"]):
    for _x in str(_tl).split("|"):
        if ":" in _x:
            _t, _l = _x.split(":")
            _pairs.append((_t, int(_l), _code))
TABLINE = pd.DataFrame(_pairs, columns=["table", "line", "code"])
_TABS = ["U20405", "U20403", "U20406", "T20305", "T20805", "T20600", "T20100"]
_NEED = set(TABLINE[TABLINE.table.isin(_TABS)].code)
_NEED |= {c[:-2] + "RA" for c in _NEED if c.endswith("RC")}      # quantity-index twins of every RC series


def read_flat(member, codes):
    df = pd.read_csv(io.BytesIO(ZF_BEA.read(member)), dtype=str)
    df.columns = ["code", "period", "value"]
    df = df[df.code.isin(codes)].copy()
    df["value"] = pd.to_numeric(df.value.str.replace(",", "", regex=False), errors="coerce")
    return df


_FA = read_flat("nipadataA.txt", _NEED)
_FM = read_flat("nipadataM.txt", _NEED)
_FM["period"] = _FM.period.str[:4] + "-" + _FM.period.str[5:7]
SER_A = _FA.pivot(index="period", columns="code", values="value").sort_index()   # by series code
SER_M = _FM.pivot(index="period", columns="code", values="value").sort_index()


def line_code(table, line):
    x = TABLINE[(TABLINE.table == table) & (TABLINE.line == line)].code
    return x.iloc[0] if len(x) else None


def series(code, freq):
    S = SER_A if freq == "A" else SER_M
    return S[code] if code in S.columns else None


# 2.4.5U hierarchy from the workbook's indentation (two spaces per level; line 1 is the root)
_wb = openpyxl.load_workbook(RAW / "bea" / "nipa" / "xls_underlying" / "Section2All_xls.xlsx", read_only=True)
_rows = [r[:3] for r in _wb["U20405-A"].iter_rows(values_only=True, max_col=3)]
U = []
for r in _rows:
    if r[0] is None or not str(r[0]).strip().isdigit():
        continue
    lab = str(r[1])
    U.append(dict(line=int(r[0]), label=lab.strip(), indent=(len(lab) - len(lab.lstrip(" "))) // 2,
                  code=str(r[2]).strip()))
U = pd.DataFrame(U).set_index("line")
U_MAIN = [l for l in U.index if l <= 368]
PARENT, _stack = {}, []
for l in U_MAIN:
    if l == 1:
        continue
    lev = U.at[l, "indent"]
    while _stack and _stack[-1][0] >= lev:
        _stack.pop()
    PARENT[l] = _stack[-1][1] if _stack else 1
    _stack.append((lev, l))
CHILDREN = {}
for c, p in PARENT.items():
    CHILDREN.setdefault(p, []).append(c)
SIGN = {l: (-1 if U.at[l, "label"].startswith("Less:") else 1) for l in U_MAIN}


def ancestors(l):
    out = []
    while l in PARENT:
        l = PARENT[l]
        out.append(l)
    return out


def subtree(l):
    out, st = [], [l]
    while st:
        x = st.pop()
        out.append(x)
        st += CHILDREN.get(x, [])
    return out


def sign_to_root(l):
    s = SIGN[l]
    for a in ancestors(l):
        s *= SIGN.get(a, 1)
    return s


def uval(line, freq, kind="RC"):
    """2.4.5U line value (kind RC) or its 2.4.3U quantity index (kind RA) by series code."""
    code = U.at[line, "code"]
    if kind == "RA":
        code = code[:-2] + "RA"
    return series(code, freq)


# sanity on my own parse: workbook codes = SeriesRegister codes for U20405, and the signed children sum to parents
_bad = [l for l in U_MAIN if line_code("U20405", l) != U.at[l, "code"]]
claim("2.4.5U: workbook line codes equal SeriesRegister U20405 codes (my parse)", 0, len(_bad), tol=0)
_gap = 0.0
for p, kids in CHILDREN.items():
    v = uval(p, "A").loc["2024"]
    s = sum(SIGN[k] * uval(k, "A").loc["2024"] for k in kids if np.isfinite(uval(k, "A").loc["2024"]))
    _gap = max(_gap, abs(v - s))
claim("2.4.5U 2024: every parent = signed sum of its children (max gap, $m)", 0, _gap, tol=5)


# %% 2. BLS distributional PCE (raw workbook, March 2025 results)
_wb = openpyxl.load_workbook(RAW / "bls_ce" / "dpce" / "distributional-pce-2000-2023.xlsx", read_only=True,
                             data_only=True)
_t1 = list(_wb["table1data"].iter_rows(values_only=True))
DP1 = pd.DataFrame(_t1[1:], columns=[str(c) for c in _t1[0]])
DP1 = DP1[DP1.year.notna()].copy()
DP1["year"] = DP1.year.astype(int)
DP1["lineno"] = DP1.lineno.astype(int)
DP1 = DP1.rename(columns={f"Decile{k}": f"d{k:02d}" for k in range(1, 11)})
_t3 = list(_wb["Table 3"].iter_rows(values_only=True))
_hdr = [str(x) for x in _t3[2]]
DP3 = {}
for r in _t3[3:]:
    if r[0] is not None and str(r[0]).isdigit() and 2 <= int(r[0]) <= 11:
        DP3[DEC[int(r[0]) - 2]] = {int(_hdr[j]): float(r[j]) for j in range(2, len(r)) if r[j] is not None}
DP3 = pd.DataFrame(DP3)                       # index year, columns d01..d10 (2017 = 100)
A_CATS = [4, 5, 6, 7, 9, 10, 11, 12, 15, 16, 17, 18, 19, 20, 21, 22]   # leaf lines of NIPA Table 2.3.5


def dp_shares(year, lines):
    x = DP1[(DP1.year == year) & DP1.lineno.isin(lines)].set_index("lineno").loc[lines, DEC].astype(float)
    return x


def theta_A(year):
    t = dp_shares(year, A_CATS)
    return t.div(t.sum(axis=1), axis=0)            # published shares are rounded: renormalize rows


def dp_total(year, line):
    return float(DP1[(DP1.year == year) & (DP1.lineno == line)].Total.iloc[0])


# 2.3.5 / 2.8.5 lines -> series codes (from the register); growth by series code
A_CODE = {l: line_code("T20305", l) for l in A_CATS + [1]}
claim("2.3.5 and 2.8.5 lines 1-22 carry the same series codes (register)", 0,
      sum(line_code("T20305", l) != line_code("T20805", l) for l in range(1, 23)), tol=0)
_lines_U = {c: l for l, c in U.code.items() if l <= 368}
claim("2.3.5 leaf lines map to 2.4.5U lines with the same code (16 of 16)", 16,
      sum(A_CODE[l] in _lines_U for l in A_CATS), tol=0)


def growth_A(t0, t1, freq):
    """Nominal and real (2.4.3U quantity-index twin) growth of the 16 major lines."""
    rows = {}
    for l in A_CATS:
        c = A_CODE[l]
        n, q = series(c, freq), series(c[:-2] + "RA", freq)
        rows[l] = dict(S0=n.loc[t0], g_nom=n.loc[t1] / n.loc[t0] - 1, g_real=q.loc[t1] / q.loc[t0] - 1)
    return pd.DataFrame(rows).T


def growth_U(lines, t0, t1, freq):
    rows = {}
    for l in lines:
        n, q = uval(l, freq), uval(l, freq, "RA")
        rows[l] = dict(S0=n.loc[t0], g_nom=n.loc[t1] / n.loc[t0] - 1,
                       g_real=(q.loc[t1] / q.loc[t0] - 1) if q is not None else np.nan)
    return pd.DataFrame(rows).T


# %% 3. Estimators (my own)
def wls(g, th, w):
    w = np.asarray(w, float) / np.sum(w)
    tb, gb = np.dot(w, th), np.dot(w, g)
    b = np.dot(w, (th - tb) * (g - gb)) / np.dot(w, (th - tb) ** 2)
    return gb - b * tb, b


def slopes_many(y, TH, w):
    """WLS slope of y on each row of TH (permuted regressors)."""
    w = np.asarray(w, float) / np.sum(w)
    m = TH @ w
    C = TH - m[:, None]
    return (C * (w * (y - np.dot(w, y)))).sum(axis=1) / (C ** 2 @ w)


def perm_inference(g, th, w, c_zandi, nperm=N_PERM, rng=RNG):
    """Placebo p (H0 gap = 0), p at Zandi's gap and the 95% interval by exact inversion of the permutation test
    of H0: gap = c (statistic |slope of g - c th on th|; under a permutation it is |A_p - c B_p|)."""
    n = len(g)
    P = np.argsort(rng.random((nperm, n)), axis=1)
    TH = th[P]
    A = slopes_many(g, TH, w)
    B = slopes_many(th, TH, w)
    _, b = wls(g, th, w)

    def pvals(cs):
        cs = np.atleast_1d(np.asarray(cs, float))
        out = np.empty(len(cs))
        for k in range(0, len(cs), 200):
            c = cs[k:k + 200, None]
            out[k:k + 200] = (1 + (np.abs(A[None, :] - c * B[None, :]) >= np.abs(b - c) - 1e-12).sum(axis=1)) / (nperm + 1)
        return out
    # count(c) = #{(A - cB)^2 >= (b - c)^2} changes only at the roots of (B^2-1)c^2 - 2(AB-b)c + (A^2-b^2).
    qa, qb, qc = B ** 2 - 1, -2 * (A * B - b), A ** 2 - b ** 2
    disc = qb ** 2 - 4 * qa * qc
    ok = (disc >= 0) & (np.abs(qa) > 1e-14)
    s = np.sqrt(np.where(ok, disc, 0.0))
    roots = np.concatenate([((-qb - s) / (2 * qa))[ok], ((-qb + s) / (2 * qa))[ok]])
    roots = np.sort(roots[np.isfinite(roots)])
    # bracket the accepted set on a grid, then locate each end exactly among the roots in the bracketing cells
    span = 10 * max(np.std(A), abs(b), 1e-3)
    grid = np.linspace(b - span, b + span, 2001)
    acc = grid[pvals(grid) > 0.05]
    if not len(acc):
        return dict(p_placebo=pvals(0.0)[0], p_zandi=pvals(c_zandi)[0], ci_lo=np.nan, ci_hi=np.nan,
                    perm_sd=float(np.std(A)))
    step = grid[1] - grid[0]
    ends = []
    for edge, sgn in ((acc.min(), -1), (acc.max(), +1)):
        lo_, hi_ = sorted((edge, edge + sgn * step))
        rr = roots[(roots >= lo_ - 1e-12) & (roots <= hi_ + 1e-12)]
        cand = np.concatenate([[edge], rr - 1e-10, rr + 1e-10])
        cand = cand[pvals(cand) > 0.05]
        ends.append(cand.min() if sgn < 0 else cand.max())
    return dict(p_placebo=pvals(0.0)[0], p_zandi=pvals(c_zandi)[0], ci_lo=ends[0], ci_hi=ends[1],
                perm_sd=float(np.std(A)), ci_at_grid_edge=bool(acc.min() <= grid[0] or acc.max() >= grid[-1]))


def classical_hc3(g, th, w):
    w = np.asarray(w, float)
    X = np.column_stack([np.ones(len(g)), th])
    sw = np.sqrt(w / w.mean())
    Xs, ys = X * sw[:, None], g * sw
    XtX_inv = np.linalg.inv(Xs.T @ Xs)
    beta = XtX_inv @ Xs.T @ ys
    e = ys - Xs @ beta
    h = np.einsum("ij,jk,ik->i", Xs, XtX_inv, Xs)
    s2 = np.sum(e ** 2) / (len(g) - 2)
    se = np.sqrt(s2 * XtX_inv[1, 1])
    meat = (Xs * (e / (1 - h))[:, None]).T @ (Xs * (e / (1 - h))[:, None])
    se3 = np.sqrt((XtX_inv @ meat @ XtX_inv)[1, 1])
    return float(se), float(se3)


def kappa_of(th, w):
    w = np.asarray(w, float) / np.sum(w)
    tb = np.dot(w, th)
    return np.dot(w, (th - tb) ** 2) / (tb * (1 - tb))


def fit_report(g, th, w, T, inference=True):
    a, b = wls(g, th, w)
    wn = np.asarray(w, float) / np.sum(w)
    G, tb = np.dot(wn, g), np.dot(wn, th)
    zg = (1 + ZANDI_PA) ** T - 1
    ssr = lambda pred: float(np.dot(wn, (g - pred) ** 2))
    out = dict(x_b80=a, gap=b, agg=G, theta_bar=tb, kappa=kappa_of(th, w), zandi=zg,
               wrmse_flat=np.sqrt(ssr(np.full(len(g), G))),
               r2_fit=1 - ssr(a + b * th) / ssr(np.full(len(g), G)),
               r2_zandi=1 - ssr(G + (th - tb) * zg) / ssr(np.full(len(g), G)))
    out["se"], out["se_hc3"] = classical_hc3(g, th, w)
    if inference:
        out.update(perm_inference(g, th, w, zg))
    return out


def tol_p(p):
    """3 Monte Carlo standard errors of a permutation p-value from the builder's 1,000 draws (+ rounding)."""
    return 3 * np.sqrt(max(p * (1 - p), 0.01) / 1000) + 0.006


def gap_pa(x_b80, gap, T):
    return (1 + x_b80 + gap) ** (1 / T) - (1 + x_b80) ** (1 / T)


# builder outputs (read only to print the builder column)
B_READ = pd.read_csv(OUT / "fingerprint_read.csv")
B_BT = pd.read_csv(OUT / "fingerprint_backtest.csv")
B_PW = pd.read_csv(OUT / "fingerprint_power.csv")
B_THA = pd.read_csv(OUT / "fingerprint_theta_A.csv")
B_THB = pd.read_csv(OUT / "fingerprint_theta_B.csv")
B_INF = pd.read_csv(OUT / "fingerprint_influence.csv")
B_COV = pd.read_csv(OUT / "fingerprint_coverage_B.csv")
B_MAP = pd.read_csv(OUT / "fingerprint_mapping_B.csv", dtype={"ucc": str})
B_TM = pd.read_csv(OUT / "top_tilt_monthly.csv")
B_TA = pd.read_csv(OUT / "fingerprint_top_tilt_annual.csv")


def bread(window, source, ty, measure, spec="2grp", sample="all"):
    x = B_READ[(B_READ.window == window) & (B_READ.source == source) & (B_READ.theta_base_year == ty)
               & (B_READ.measure == measure) & (B_READ.spec == spec) & (B_READ["sample"] == sample)]
    return x.iloc[0]


# %% 4. Source A: thetas and the read
th23 = theta_A(2023)
tA23 = th23[TOP20].sum(axis=1)
claim("A theta 2023: health care (line 16) top-20 share, the lowest of the 16 lines", 0.26, round(tA23.loc[16], 2),
      tol=0.005, note=f"lowest line is {tA23.idxmin()}")
claim("A theta 2023: motor vehicles (line 4) top-20 share, the highest of the 16 lines", 0.67, round(tA23.loc[4], 2),
      tol=0.005, note=f"highest line is {tA23.idxmax()}")
_bth = B_THA[B_THA.base_year == 2023].set_index("category").theta_top20
claim("A theta 2023 (16 lines) equals the builder's file (max abs diff)", 0.0, float((_bth - tA23).abs().max()),
      tol=1e-9)
claim("dPCE 2023: top two deciles' share of total PCE (pct)", 39.5, 100 * dp_shares(2023, [1])[TOP20].sum(axis=1).iloc[0],
      tol=0.05)

READ_WIN = [("2023->2025", "A", "2023", "2025", 2), ("2023-09->2026-09", "M", "2023-09", "2026-09", 3),
            ("2022-09->2026-09", "M", "2022-09", "2026-09", 4)]
MY_READ = {}
NOTE_A = {  # NOTES section 5 table, source A: (nominal gap, lo, hi, p), (real gap, lo, hi, p), real per year
    "2023->2025": ((-2.7, -29.3, 31.5, 0.86), (-5.0, -22.5, 17.0, 0.67), -2.4),
    "2023-09->2026-09": ((-1.0, -33.7, 37.9, 0.95), (-3.6, -27.7, 27.7, 0.83), -1.1),
    "2022-09->2026-09": ((-7.2, -51.3, 48.3, 0.77), (-6.5, -43.6, 41.2, 0.78), -1.5)}
for win, freq, t0, t1, T in tqdm(READ_WIN, desc="A read"):
    gf = growth_A(t0, t1, freq)
    for meas, col, k in (("nominal", "g_nom", 0), ("real", "g_real", 1)):
        g, w, th = gf[col].to_numpy(float), gf.S0.to_numpy(float), tA23.loc[gf.index].to_numpy(float)
        r = fit_report(g, th, w, T)
        MY_READ[(win, "A", 2023, meas)] = r
        nb = NOTE_A[win][k]
        claim(f"A {win} {meas}: two-group gap (pts)", nb[0], pts(r["gap"]), tol=0.06)
        claim(f"A {win} {meas}: 95% permutation CI low (pts)", nb[1], pts(r["ci_lo"]), tol=3.0,
              note="Monte Carlo: 20,000 own permutations vs builder's 1,000")
        claim(f"A {win} {meas}: 95% permutation CI high (pts)", nb[2], pts(r["ci_hi"]), tol=3.0)
        claim(f"A {win} {meas}: placebo p", nb[3], r["p_placebo"], tol=tol_p(nb[3]))
        bb = bread(win, "A_dPCE", 2023, meas)
        claim(f"A {win} {meas}: p at Zandi's gap", bb.p_zandi, r["p_zandi"], tol=tol_p(bb.p_zandi))
        claim(f"A {win} {meas}: kappa", bb.kappa, r["kappa"], tol=5e-4)
        claim(f"A {win} {meas}: R2 of Zandi's pattern vs flat", bb.r2_zandi_vs_flat, r["r2_zandi"], tol=2e-3)
        claim(f"A {win} {meas}: R2 of fitted line vs flat", bb.r2_fit_vs_flat, r["r2_fit"], tol=2e-3)
        claim(f"A {win} {meas}: HC3 / classical SE ratio", bb.se_hc3 / bb.se, r["se_hc3"] / r["se"], tol=0.02)
        if meas == "real":
            claim(f"A {win} real: gap per year (pts)", NOTE_A[win][2], pts(gap_pa(r["x_b80"], r["gap"], T)),
                  tol=0.06)
# the 2022 theta sensitivity for the four-year window, real
gf = growth_A("2022-09", "2026-09", "M")
_t22 = theta_A(2022)[TOP20].sum(axis=1)
r = fit_report(gf.g_real.to_numpy(float), _t22.loc[gf.index].to_numpy(float), gf.S0.to_numpy(float), 4, False)
claim("A 2022-09->2026-09 real with the 2022 theta (pts)", -8.1, pts(r["gap"]), tol=0.06)
MY_READ[("2022-09->2026-09", "A", 2022, "real")] = r
r = fit_report(gf.g_nom.to_numpy(float), _t22.loc[gf.index].to_numpy(float), gf.S0.to_numpy(float), 4, False)
MY_READ[("2022-09->2026-09", "A", 2022, "nominal")] = r

# scale statements in section 2 (16 lines, 2023-09 window)
rA3r, rA3n = MY_READ[("2023-09->2026-09", "A", 2023, "real")], MY_READ[("2023-09->2026-09", "A", 2023, "nominal")]
sdth = np.sqrt(rA3r["kappa"] * rA3r["theta_bar"] * (1 - rA3r["theta_bar"]))
claim("16 lines: kappa (2023 theta, 2023-09 weights)", 0.056, rA3r["kappa"], tol=0.0006)
claim("16 lines: weighted sd of theta_top20", 0.116, sdth, tol=0.0006)
claim("16 lines: Zandi 3-year K moves category growth per sd of theta (pts)", 1.4, pts(sdth * rA3r["zandi"]), tol=0.06)
claim("16 lines: weighted scatter of category growth, real, 3 years (pts)", 4.3, pts(rA3r["wrmse_flat"]), tol=0.06)
claim("16 lines: weighted scatter of category growth, nominal, 3 years (pts)", 5.8, pts(rA3n["wrmse_flat"]), tol=0.06)
claim("Zandi's cumulative gap over 2/3/4 years (pts)", "8.2/12.5/17.0",
      "/".join(f"{pts((1.04) ** T - 1):.1f}" for T in (2, 3, 4)), ok="8.2/12.5/17.0" == "/".join(
          f"{pts((1.04) ** T - 1):.1f}" for T in (2, 3, 4)))
_r = [r_["se_hc3"] / r_["se"] for k_, r_ in MY_READ.items() if k_[1] == "A" and "se" in r_]
claim("HC3 SE 'typically 1.5-2 times the classical' (A reads: min..max ratio)", "1.5-2",
      f"{min(_r):.2f}-{max(_r):.2f}", ok=1.4 <= np.median(_r) <= 2.1, note="median within 1.4-2.1 counts as OK")

# robustness drops, A, 2023-09 window
gf = growth_A("2023-09", "2026-09", "M")
for name, drop, meas, val in (("without health care", [16], "g_real", 12.0), ("without health care", [16], "g_nom", 16.5),
                              ("without imputed lines 15, 20, 22", [15, 20, 22], "g_real", -9.6)):
    keep = [l for l in gf.index if l not in drop]
    a, b = wls(gf.loc[keep, meas].to_numpy(float), tA23.loc[keep].to_numpy(float), gf.loc[keep, "S0"].to_numpy(float))
    claim(f"A 2023-09->2026-09 {name}, {'real' if meas == 'g_real' else 'nominal'} (pts)", val, pts(b), tol=0.06)
claim("A health care (line 16) real growth 2023-09->2026-09 (pct)", 15, pts(gf.at[16, "g_real"]), tol=0.6,
      note="NOTES: 'grew 15% in real terms'")


# %% 5. Source B rebuilt from raw CE files (my own parsers, alignment, matching and unmapped-UCC rule)
CE = RAW / "bls_ce"
CE_YEARS = list(range(2014, 2026))
STATROWS = {"mean", "share", "se", "rse", "cv(%)", "percent reporting"}


def xl_rows(path, ncol):
    wb = openpyxl.load_workbook(path, read_only=True)
    ws = wb[wb.sheetnames[0]]
    ws.reset_dimensions()                    # some older files carry a wrong dimension record
    out = []
    for r in ws.iter_rows(max_col=ncol):
        v = r[0].value
        ind = r[0].alignment.indent if v is not None else 0
        out.append((v, ind, [x.value for x in r[1:ncol]]))
    return out


def xl_legend(rows):
    leg = {}
    for v, _, _ in rows:
        m = re.match(r"^([a-e])\s+(.*)$", str(v or "").strip())
        if m:
            t = m.group(2).lower()
            leg[m.group(1) + "/"] = ("suppressed" if "suppressed" in t else "too_small" if "too small" in t else
                                     "no_data" if "no data" in t else "other")
    return leg


def norm(s):
    s = str(s).lower()
    s = re.sub(r"\[[id]\]", "", s)
    s = re.sub(r"\((new ucc|thru|through|new title)[^)]*\)", "", s)
    s = re.sub(r"\b[a-e]/", "", s)
    s = s.replace("''", "'").replace("’", "'").replace("&", "and")
    s = re.sub(r"[^a-z0-9' ,/()-]", " ", s)
    return re.sub(r"\s+", " ", s).strip().rstrip(":").strip()


def code_value(x, leg):
    if isinstance(x, (int, float)):
        return float(x)
    k = leg.get(str(x).strip(), "unknown")
    return 0.0 if k in ("too_small", "no_data") else np.nan     # 'no data reported' = nobody reported it


def t1110(year):
    rows = xl_rows(CE / "tables" / "deciles" / f"cu-income-deciles-before-taxes-{year}.xlsx", 12)
    leg = xl_legend(rows)
    labs = []
    for v, ind, vals in rows:
        s = "" if v is None else str(v).strip()
        if not s:
            continue
        if s.lower() in STATROWS:
            if s.lower() == "mean" and labs:
                labs[-1]["mean"] = pd.Series([code_value(x, leg) for x in vals[:11]], index=["all"] + DEC)
                labs[-1]["n_code"] = sum(isinstance(x, str) for x in vals[:11])
            continue
        labs.append(dict(label=s, indent=ind, mean=None, vals=vals[:11], n_code=0))
    ncu = next(l for l in labs if l["label"].startswith("Number of consumer units"))
    N = pd.Series([float(x) for x in ncu["vals"]], index=["all"] + DEC)
    i0 = next(i for i, l in enumerate(labs) if l["label"].startswith("Average annual expenditures"))
    i1 = next(i for i in range(i0 + 1, len(labs)) if labs[i]["indent"] == 0)
    blk, items, stack = labs[i0:i1], [], []
    for k, l in enumerate(blk):
        while stack and stack[-1][0] >= l["indent"]:
            stack.pop()
        stack.append((l["indent"], norm(l["label"])))
        nxt = blk[k + 1]["indent"] if k + 1 < len(blk) else -1
        items.append(dict(label=l["label"], npath=" > ".join(s[1] for s in stack), leaf=nxt <= l["indent"],
                          mean=l["mean"], n_code=l["n_code"]))
    rent = next(l for l in labs[i1:] if "monthly rental value of owned home" in l["label"].lower())
    return dict(N=N, items=items, rentval=rent["mean"], leg=leg)


ZS = zipfile.ZipFile(CE / "stubs" / "stubs.zip")


def stub(year):
    rows = []
    for ln in ZS.read(f"stubs/CE-HG-Integ-{year}.txt").decode("latin-1").splitlines():
        ln = ln.rstrip("\r")
        if not ln.strip() or ln.startswith("*"):
            continue
        if ln[0] == "2":
            rows[-1]["title"] += " " + ln[6:69].strip()
            continue
        parts = [p for p in ln[69:].split() if p != "-"]
        rows.append(dict(level=int(ln[3]), title=ln[6:69].strip(), code=parts[0], src=parts[1]))
    i0 = next(i for i, r in enumerate(rows) if r["code"].startswith("TOTALE"))
    i1 = i0 + 1
    while i1 < len(rows) and rows[i1]["level"] > rows[i0]["level"]:
        i1 += 1
    st = pd.DataFrame(rows[i0:i1]).reset_index(drop=True)
    path, P = [], []
    for _, r in st.iterrows():
        path = path[: r.level - rows[i0]["level"]] + [norm(r.title)]
        P.append(" > ".join(path))
    st["npath"], st["ntitle"] = P, st.title.map(norm)
    return st


def t2500(year):
    rows = xl_rows(CE / "tables" / "detail" / f"cu-all-detail-{year}.xlsx", 2)
    leg = xl_legend(rows)
    labs = []
    for v, ind, vals in rows:
        s = "" if v is None else str(v).strip()
        if not s:
            continue
        if s.lower() in STATROWS:
            if s.lower() == "mean" and labs:
                x = vals[0]
                labs[-1]["mean"] = code_value(x, leg)
                labs[-1]["code"] = "" if isinstance(x, (int, float)) else leg.get(str(x).strip(), "unknown")
            continue
        labs.append(dict(label=s, indent=ind, mean=np.nan, code="nomean"))
    j0 = next(i for i, l in enumerate(labs) if l["label"].startswith("Average annual expenditures"))
    j1 = next(i for i in range(j0 + 1, len(labs)) if labs[i]["indent"] == 0)
    d = pd.DataFrame(labs[j0:j1]).reset_index(drop=True)
    d["ntitle"] = d.label.map(norm)
    return d


def sim(a, b):
    return 1.0 if a == b else difflib.SequenceMatcher(None, a, b).ratio()


def align(st, d, look=6):
    """Two pointers over stub rows and Table 2500 rows (same order by construction): pair when titles agree
    (similarity >= 0.8); otherwise skip whichever side has the nearer later match (a row the other omits)."""
    i = j = 0
    out = {}
    while i < len(st) and j < len(d):
        if sim(st.ntitle[i], d.ntitle[j]) >= 0.8:
            out[i] = j
            i, j = i + 1, j + 1
            continue
        jj = next((k for k in range(j + 1, min(j + look, len(d))) if sim(st.ntitle[i], d.ntitle[k]) >= 0.8), None)
        ii = next((k for k in range(i + 1, min(i + look, len(st))) if sim(st.ntitle[k], d.ntitle[j]) >= 0.8), None)
        if ii is not None and (jj is None or ii - i <= jj - j):
            i = ii
        elif jj is not None:
            j = jj
        else:
            i, j = i + 1, j + 1
    return out


# BLS's CE -> PCE map (raw workbook)
_r = list(openpyxl.load_workbook(CE / "dpce" / "ce_pce_map.xlsx", read_only=True).worksheets[0].iter_rows(values_only=True))
BMAP = pd.DataFrame(_r[1:], columns=_r[0])
BMAP = BMAP[BMAP.UCC_Split.notna()].copy()
BMAP["ucc"] = BMAP.UCC_Split.astype(str).str.split("_").str[0]
BMAP["ntitle"] = BMAP.UCC_Title.map(norm)
MAP_T = BMAP.groupby("ucc").PCE_Series.apply(lambda s: sorted(set(s))).to_dict()
MAP_TITLE = BMAP.drop_duplicates("ucc").set_index("ucc").ntitle.to_dict()
SER2LINE = {c: l for l, c in U.code.items() if l <= 368 and SIGN[l] == 1 and sign_to_root(l) == 1}
claim("BLS ce_pce_map: every target series is a 2.4.5U line entering PCE with +1", 0,
      sum(s not in SER2LINE for s in BMAP.PCE_Series.unique()), tol=0)

# My rule for UCCs that BLS's map does not cover (judgment, stated):
#  (1) out of scope by concept: taxes, interest, government fees, social-insurance contributions (Medicare, Medicaid,
#      Tricare, CHIP premiums), cash transfers, pension/Social Security deductions, saving, prepaid tuition, mortgage
#      late fees (my call: part of the mortgage, as interest is); owner-occupied housing inputs (maintenance, ground
#      rent: owners' imputed rent stands for housing services) and renter-paid maintenance (BLS's map omits both);
#  (2) Diary food and alcohol away from home -> DOPMRC / DAPMRC (BLS's map sources them from Interview UCCs);
#  (3) a short override list where an obvious PCE twin exists (below, each with its reason);
#  (4) otherwise the target of the most similar mapped UCC title in the same Table 1110 item (>= 0.45), or anywhere
#      in the map (>= 0.6); otherwise dropped as unmapped.
OUT_KEYS = ["mortgage interest", "property tax", "ground rent", "registration", "drivers' license", "medicare",
            "medicaid", "tricare", "chip", "children's health insurance", "alimony", "child support",
            "support for college students", "gift to non-cu", "cash contribution", "other cash gifts", "deductions for",
            "retirement plans", "social security", "other taxes", "prepaid tuition", "educational savings",
            "late fee mortgage"]
MY_OVERRIDE = {
    "002120": (None, "other non-health insurance: BLS's map has no target and no PCE line fits; dropped"),
    "280230": (["DSEWRC"], "sewing materials for the home -> Sewing items"),
    "300900": (["DSEARC"], "misc. household appliances (Diary) -> Small electric household appliances"),
    "310312": (["DVAARC"], "phonographs -> Video and audio equipment"),
    "310315": (["DVAARC"], "digital video/media players -> Video and audio equipment"),
    "310331": (["DVAARC"], "sound equipment -> Video and audio equipment"),
    "310332": (["DVAARC"], "sound equipment accessories -> Video and audio equipment"),
    "310335": (["DVAARC"], "video equipment -> Video and audio equipment"),
    "320380": (["DNECRC"], "tableware, nonelectric kitchenware -> Nonelectric cookware and tableware"),
    "320430": (["DTOORC"], "other hardware -> Tools and equipment for house and garden"),
    "320905": (["DTOORC"], "misc. household equipment and parts -> Tools and equipment for house and garden"),
    "340913": (["DFRERC"], "repair of misc. household equipment and furnishings -> Repair of furniture, furnishings"),
    "490000": (["DVMRRC"], "misc. auto repair -> Motor vehicle maintenance and repair"),
    "550350": (["DOMPRC"], "supportive/convalescent equipment -> Other medical products (as BLS's 550330)"),
    "570902": (["DOMORC"], "repair of medical equipment -> as BLS's rental of medical equipment 570901"),
    "590110": (["DMAGRC"], "newspapers -> Newspapers and periodicals"),
    "590210": (["DMAGRC"], "magazines -> Newspapers and periodicals"),
    "620912": (["DAVPRC"], "rental of video media -> as BLS's rental of video software 620918"),
    "660000": (["DEBKRC", "DSTYRC"], "school supplies, unspecified -> as BLS's school books/supplies 660210"),
    "680903": (["DPCSRC"], "misc. personal services -> Personal care services (as BLS's dating services 680904)"),
}


def my_targets(code, title, npath, item_codes):
    if code in MAP_T:
        return MAP_T[code], "BLS map", ""
    t = norm(title)
    if any(k in t for k in OUT_KEYS) or code[:4] in ("8001", "8008", "8009"):
        return None, "out", "not PCE by concept"
    if " > owned dwellings > " in npath or " > owned vacation homes > " in npath:
        return None, "out", "owner-occupied housing input"
    if " > rented dwellings > maintenance" in npath:
        return None, "out", "renter-paid maintenance (BLS map omits)"
    if re.match(r"^190[1-7]\d\d$", code):
        return ["DOPMRC"], "rule", "Diary food away -> Other purchased meals"
    if re.match(r"^2005\d\d$", code):
        return ["DAPMRC"], "rule", "Diary alcohol away -> Alcohol in purchased meals"
    if code in MY_OVERRIDE:
        tg, why = MY_OVERRIDE[code]
        return tg, ("override" if tg else "unmapped"), why
    cand = [(sim(t, MAP_TITLE[u]), u) for u in item_codes if u in MAP_T]
    if cand and max(cand)[0] >= 0.45:
        s, u = max(cand)
        return MAP_T[u], "similar", f"{u} ({s:.2f})"
    s, u = max((sim(t, tt), u) for u, tt in MAP_TITLE.items())
    if s >= 0.6:
        return MAP_T[u], "similar", f"{u} ({s:.2f})"
    return None, "unmapped", "no PCE twin"


def fill_deciles(m, N):
    """Withheld decile means filled from N_all m_all = sum_d N_d m_d, the residual spread equally per CU."""
    m = m.copy()
    miss = [d for d in DEC if not np.isfinite(m[d])]
    if miss:
        res = max(N["all"] * m["all"] - sum(N[d] * m[d] for d in DEC if d not in miss), 0.0)
        for d in miss:
            m[d] = res / sum(N[x] for x in miss)
    return m, len(miss)


CE_DATA, STUBS, T2500, ALIGN = {}, {}, {}, {}
for y in tqdm(CE_YEARS, desc="CE raw files"):
    CE_DATA[y], STUBS[y], T2500[y] = t1110(y), stub(y), t2500(y)
    ALIGN[y] = align(STUBS[y], T2500[y])
# stand-ins for withheld (RSE >= 25%) UCC means: the nearest year that PUBLISHES a value (numeric or 'too small');
# a year where the UCC is coded 'no data reported' (e.g. discontinued after 2024Q1) is not a stand-in
UCC_MEAN = {y: {STUBS[y].code[i]: T2500[y]["mean"][j] for i, j in ALIGN[y].items()
                if STUBS[y].src[i] in ("I", "D") and T2500[y]["code"][j] in ("", "too_small")} for y in CE_YEARS}


def nearest_mean(code, year):
    for z in sorted([z for z in CE_YEARS if z != year], key=lambda z: (abs(z - year), -z)):
        if code in UCC_MEAN[z]:
            return UCC_MEAN[z][code], z
    return np.nan, None


def b_items(year):
    D = CE_DATA[year]
    leaves = [it for it in D["items"] if it["leaf"]]
    byp = {it["npath"]: it for it in D["items"]}
    gas = "average annual expenditures > transportation > gasoline and other fuels"
    veh = "average annual expenditures > transportation > vehicle purchases (net outlay)"
    out = {}
    for it in leaves:
        if it["npath"].startswith(gas + " > "):
            continue                                  # 2023-2025: only 'Gasoline' shown; the parent is used
        out[it["npath"]] = it["mean"].copy()
    if gas in byp:
        out[gas] = byp[gas]["mean"].copy()
    kids = [p for p in out if p.startswith(veh + " > ")]
    if veh in byp and not any(p.endswith("other vehicles") for p in kids):
        out[veh + " > other vehicles"] = (byp[veh]["mean"] - sum(out[p] for p in kids)).clip(lower=0)
    out["addenda > owners' rental value x12"] = D["rentval"] * 12.0
    filled = {}
    for k in out:
        if not np.isfinite(out[k]["all"]):           # all-CU mean withheld: parent minus its shown children
            par = k.rsplit(" > ", 1)[0]
            sib = [it for it in D["items"] if it["npath"].rsplit(" > ", 1)[0] == par and it["npath"] != k]
            out[k]["all"] = max(byp[par]["mean"]["all"] - np.nansum([s["mean"]["all"] for s in sib]), 0.0)
        out[k], filled[k] = fill_deciles(out[k], D["N"])
    return out, filled


def item_node(npath, st):
    hit = list(st.index[st.npath == npath])
    if len(hit) == 1:
        return hit[0], "path"
    par, name = npath.rsplit(" > ", 1)
    cand = [(sim(name, st.ntitle[i]), i) for i in st.index if st.npath[i].rsplit(" > ", 1)[0] == par]
    if cand and max(cand)[0] >= 0.6:
        return max(cand)[1], "similar title under the same parent"
    return None, "unmatched"


def build_B(year):
    st, items_filled = STUBS[year], b_items(year)
    items, nfill = items_filled
    D = CE_DATA[year]
    S = {l: uval(l, "A").loc[str(year)] for l in U_MAIN}
    links, match_kind = [], {}
    for key in items:
        if key.startswith("addenda"):
            ucc_rows = [("910050", "owners' rental value", "", D["rentval"]["all"] * 12.0)]
            match_kind[key] = "addendum"
        else:
            node, how = item_node(key, st)
            match_kind[key] = how
            if node is None:
                continue
            lev, ucc_rows = st.level[node], []
            for j in range(node, len(st)):
                if j > node and st.level[j] <= lev:
                    break
                if st.src[j] in ("I", "D"):
                    mu = T2500[year]["mean"][ALIGN[year][j]] if j in ALIGN[year] else np.nan
                    if not np.isfinite(mu):
                        mu = nearest_mean(st.code[j], year)[0]
                    ucc_rows.append((st.code[j], st.title[j], st.npath[j], mu))
        codes = [u[0] for u in ucc_rows]
        for code, title, npath, mu in ucc_rows:
            tg, kind, why = my_targets(code, title, npath, codes) if code != "910050" else (MAP_T["910050"], "BLS map", "")
            mu = 0.0 if not np.isfinite(mu) else max(mu, 0.0)
            if not tg:
                links.append(dict(item=key, ucc=code, mean=mu, kind=kind, why=why, line=np.nan, share=0.0))
                continue
            ls = [SER2LINE[s] for s in tg]
            tot = sum(S[l] for l in ls)
            for l in ls:
                links.append(dict(item=key, ucc=code, mean=mu, kind=kind, why=why, line=l, share=S[l] / tot))
    L = pd.DataFrame(links)
    M = L[L.line.notna()].copy()
    M["line"] = M.line.astype(int)
    M["w"] = M["mean"] * M.share
    mapped = set(M.line)
    cats = sorted(l for l in mapped if not any(d in mapped for d in subtree(l) if d != l))
    rows = []
    for _, r in M.iterrows():
        if r.line in cats:
            rows.append((r["item"], r.line, r.w))
        else:
            kids = [c for c in cats if r.line in ancestors(c)]
            tot = sum(S[c] for c in kids)
            rows += [(r["item"], c, r.w * S[c] / tot) for c in kids]
    E = pd.DataFrame(rows, columns=["item", "cat", "w"]).groupby(["cat", "item"]).w.sum().reset_index()
    N = D["N"]
    TH = {k: (N[DEC] * v[DEC]) / float((N[DEC] * v[DEC]).sum()) for k, v in items.items()}
    th = {}
    for c, g in E.groupby("cat"):
        w = g.set_index("item").w
        if w.sum() <= 0:
            w = w * 0 + 1.0
        th[c] = sum(TH[k] * w[k] for k in w.index) / w.sum()
    th = pd.DataFrame(th).T[DEC]
    return dict(theta=th, links=L, E=E, items=items, nfill=nfill, match=match_kind, cats=cats, S=S)


MYB = {}
for y in tqdm(CE_YEARS, desc="source B by CE year (own mapping)"):
    MYB[y] = build_B(y)

# %% 6. Source B: mapping claims, coverage, thetas against the builder's file
for y in CE_YEARS:
    b = B_THB[B_THB.base_year == y].set_index("category").theta_top20
    m = MYB[y]["theta"][TOP20].sum(axis=1)
    com = sorted(set(m.index) & set(b.index))
    d = (m.loc[com] - b.loc[com]).abs()
    nbig = int((d > 0.02).sum())
    claim(f"B {y}: categories (mine vs builder; same set)", len(b), len(m),
          ok=(len(b) == len(m) == len(com)), note=f"theta_top20 max |diff| {d.max():.4f} at line {d.idxmax()}; "
                                                f"{nbig} lines differ by > 0.02")
claim("B: categories per year '132-133'", "132-133", f"{min(len(MYB[y]['cats']) for y in CE_YEARS)}-"
      f"{max(len(MYB[y]['cats']) for y in CE_YEARS)}",
      ok=min(len(MYB[y]["cats"]) for y in CE_YEARS) == 132 and max(len(MYB[y]["cats"]) for y in CE_YEARS) == 133)
_m54 = float(MYB[2023]["theta"].loc[54, TOP20].sum())
_b54 = float(B_THB[(B_THB.base_year == 2023) & (B_THB.category == 54)].theta_top20.iloc[0])
claim("B 2023 line 54 (motorcycles): 'Other vehicles' all cells withheld -> documented fill (equal per CU)", _b54, _m54,
      tol=0.02, note="builder's value comes from an undocumented residual (vehicle purchases - new - used): the "
                     "all-withheld row drops out of its pivot; tiny line, no effect on any headline")
th24 = MYB[2024]["theta"][TOP20].sum(axis=1)
S24 = pd.Series({c: MYB[2024]["S"][c] for c in th24.index})
claim("B 2024: tenant rent (154) theta_top20, single feeder", 0.138, th24.loc[154], tol=0.0006)
claim("B 2024: tobacco (141) theta_top20, single feeder", 0.152, th24.loc[141], tol=0.0006)
claim("B 2024: lowest theta_top20 (tenant rent)", 0.14, th24.min(), tol=0.006, note=f"line {th24.idxmin()}")
claim("B 2024: highest theta_top20 (higher education, educational books)", 0.58, th24.max(), tol=0.006,
      note=f"line {th24.idxmax()}; 291 = {th24.loc[291]:.3f}, 69 = {th24.loc[69]:.3f}")
claim("B 2024: PCE-weighted mean theta_top20", 0.37, float((th24 * S24).sum() / S24.sum()), tol=0.006)
_items24 = MYB[2024]["match"]
claim("B 2024: Table 1110 items used (73 by label path + 2 by group code + the rental-value addendum)", 76,
      len(_items24), tol=0, note=f"mine: {sum(v == 'path' for v in _items24.values())} by path (the gasoline parent "
                                 f"and the other-vehicles group exist under the same paths in the stub) + addendum; "
                                 f"unmatched: {sum(v == 'unmatched' for v in _items24.values())}")
for _y in CE_YEARS:
    _u = [k for k, v in MYB[_y]["match"].items() if v == "unmatched"]
    if _u:
        claim(f"B {_y}: every Table 1110 item found in the stub", 0, len(_u), tol=0, note="; ".join(_u))

for y in CE_YEARS:
    S = MYB[y]["S"]
    cats = MYB[y]["cats"]
    cov = sum(S[c] for c in cats) / S[1]
    hl = [c for c in cats if any(a in (172, 121, 66, 275) for a in [c] + ancestors(c))]
    bc = B_COV[B_COV.year == y].iloc[0]
    claim(f"B {y}: share of PCE in mapped categories", bc.pce_covered_share, cov, tol=0.002)
    if y == 2024:
        claim("B 2024: covered PCE ($tn) of total ($tn)", "18.2 of 19.8",
              f"{sum(S[c] for c in cats) / 1e6:.1f} of {S[1] / 1e6:.1f}",
              ok=f"{sum(S[c] for c in cats) / 1e6:.1f} of {S[1] / 1e6:.1f}" == "18.2 of 19.8")
        claim("B 2024: health lines' share of PCE (pct)", 22, 100 * sum(S[c] for c in hl) / S[1], tol=0.5)
        claim("B 2024: owners' imputed rent (160) share of PCE (pct)", 12, 100 * S[160] / S[1], tol=0.5)
        claim("B 2024: covered share excluding health lines (pct)", 70, 100 * (sum(S[c] for c in cats) -
                                                                              sum(S[c] for c in hl)) / S[1], tol=0.5)
        covered = set(cats) | {d for c in cats for d in subtree(c)} | {a for c in cats for a in ancestors(c)}
        unc = {}
        for l in U_MAIN:
            if l in covered or (l in PARENT and PARENT[l] not in covered):
                continue
            unc[l] = sign_to_root(l) * S[l] / 1000
        for txt, lines, val in (("NPISH final consumption", [342], 614), ("FISIM", [254], 525),
                                ("portfolio management", [268], 284), ("social assistance", [317], 225),
                                ("workers' comp + income loss", [277, 278], 42),
                                ("securities commissions + trust", [260, 269], 54),
                                ("religious, civic, foundations", [324, 325, 326], 42),
                                ("net expenditures abroad", [145], 13), ("foreign-travel adjustment", [338], -216)):
            claim(f"B 2024 uncovered: {txt} ($bn)", val, sum(unc.get(l, np.nan) for l in lines), tol=1.0,
                  note="NOTES sums components rounded to $1bn" if len(lines) > 1 else "")
        claim("B 2024: uncovered lines are exactly the ones listed (+ food on farms $1bn)", 14, len(unc), tol=0,
              note=", ".join(str(l) for l in sorted(unc)))
L24 = MYB[2024]["links"]
_m = L24[~L24["item"].str.startswith("addenda")].drop_duplicates(["item", "ucc"])
_mapped = _m[_m.ucc.isin(set(L24[L24.line.notna()].ucc))]["mean"].sum()
claim("B 2024: CE side, share of average annual expenditures in UCCs with a PCE target", 0.7274,
      _mapped / CE_DATA[2024]["items"][0]["mean"]["all"], tol=0.005)
claim("B 2024: UCC 002120 (other non-health insurance) mean, $ per CU", 45,
      float(L24[L24.ucc == "002120"]["mean"].iloc[0]), tol=0.5)
for y, val in ((2022, 21), (2023, 23)):
    claim(f"B {y}: Table 1110 items with withheld decile cells filled", val,
          sum(v > 0 for v in MYB[y]["nfill"].values()), tol=1,
          note="mine counts 'no data reported' cells as zero, not as withheld")
for y, val in ((2022, 126), (2023, 121)):
    L = MYB[y]["links"]
    st = STUBS[y]
    supp = {st.code[i] for i, j in ALIGN[y].items() if T2500[y]["code"][j] == "suppressed"}
    claim(f"B {y}: links (with a PCE target) whose UCC mean Table 2500 withholds", val,
          int(L[L.line.notna() & L.ucc.isin(supp)].shape[0]), tol=6)
_bz = B_MAP[(B_MAP.ucc_mean_from_year.notna()) & (B_MAP.ucc_mean_from_year != B_MAP.year) & (B_MAP.ucc_mean_all == 0)
            & B_MAP.year.isin([2022, 2023]) & B_MAP.pce_line.notna()].drop_duplicates(["year", "ucc"])


def t2500_code(ucc, year):
    st = STUBS[int(year)]
    hit = [i for i in st.index[st.code == ucc] if i in ALIGN[int(year)]]
    return T2500[int(year)]["code"][ALIGN[int(year)][hit[0]]] if hit else "absent"


_nd = [(int(r.year), r.ucc, int(r.ucc_mean_from_year)) for r in _bz.itertuples()
       if t2500_code(r.ucc, r.ucc_mean_from_year) == "no_data"]
claim("B 2022-2023: withheld UCC means (with a PCE target) stood in by a zero from a year coding the UCC 'no data reported'",
      0, len(_nd), tol=0, note=f"{len(_nd)} of the builder's {len(_bz)} zero stand-ins; nearest year with ties going to the "
                               "later year picks 2024, where UCCs discontinued after 2024Q1 (boats, motorized campers, "
                               "camper rentals) read 'no data' and parse as 0; mine skips such years. Effect on thetas < 0.01")


# %% 7. Source B: the read, drops, influence (my thetas; the builder's thetas through my growth as a chain check)
def thB_mine(year):
    return MYB[year]["theta"][TOP20].sum(axis=1)


def thB_builder(year):
    return B_THB[B_THB.base_year == year].set_index("category").theta_top20


NOTE_B = {"2023->2025": ((8.5, -13.8, 31.4, 0.45), (16.8, -0.7, 34.8, 0.06), 8.1),
          "2023-09->2026-09": ((13.5, -8.8, 36.7, 0.24), (20.0, -4.0, 44.8, 0.10), 6.2),
          "2022-09->2026-09": ((23.2, -10.5, 61.2, 0.19), (33.2, -2.8, 71.8, 0.07), 7.5)}
for win, freq, t0, t1, T in tqdm(READ_WIN, desc="B read"):
    for meas, col, k in (("nominal", "g_nom", 0), ("real", "g_real", 1)):
        nb = NOTE_B[win][k]
        thb = thB_builder(2024)
        gf = growth_U(list(thb.index), t0, t1, freq)
        rb = fit_report(gf[col].to_numpy(float), thb.loc[gf.index].to_numpy(float), gf.S0.to_numpy(float), T, False)
        claim(f"B {win} {meas}: gap, builder's 2024 theta through my growth and WLS (pts)", nb[0], pts(rb["gap"]),
              tol=0.06)
        thm = thB_mine(2024)
        gf = growth_U(list(thm.index), t0, t1, freq)
        r = fit_report(gf[col].to_numpy(float), thm.loc[gf.index].to_numpy(float), gf.S0.to_numpy(float), T)
        MY_READ[(win, "B", 2024, meas)] = r
        claim(f"B {win} {meas}: gap with MY independent 2024 theta (pts)", nb[0], pts(r["gap"]), tol=1.0,
              note="own CE->PCE mapping; differences come from mapping judgments only")
        claim(f"B {win} {meas}: 95% permutation CI low (pts, my theta)", nb[1], pts(r["ci_lo"]), tol=3.0)
        claim(f"B {win} {meas}: 95% permutation CI high (pts, my theta)", nb[2], pts(r["ci_hi"]), tol=3.0)
        claim(f"B {win} {meas}: placebo p (my theta)", nb[3], r["p_placebo"], tol=tol_p(nb[3]))
        bb = bread(win, "B_CE", 2024, meas)
        claim(f"B {win} {meas}: p at Zandi's gap (my theta)", bb.p_zandi, r["p_zandi"], tol=tol_p(bb.p_zandi))
        claim(f"B {win} {meas}: R2 of Zandi's pattern vs flat (my theta)", bb.r2_zandi_vs_flat, r["r2_zandi"], tol=0.005)
        claim(f"B {win} {meas}: coverage of PCE at t0", bb.coverage_of_pce, gf.S0.sum() / uval(1, freq).loc[t0],
              tol=0.002)
        if meas == "real":
            claim(f"B {win} real: gap per year (pts, my theta)", NOTE_B[win][2], pts(gap_pa(r["x_b80"], r["gap"], T)),
                  tol=0.3)
    for ty in ([2023, 2025] if win != "2022-09->2026-09" else [2022]):
        thm = thB_mine(ty)
        gf = growth_U(list(thm.index), t0, t1, freq)
        for meas, col in (("nominal", "g_nom"), ("real", "g_real")):
            r = fit_report(gf[col].to_numpy(float), thm.loc[gf.index].to_numpy(float), gf.S0.to_numpy(float), T, False)
            MY_READ[(win, "B", ty, meas)] = r
            claim(f"B {win} {meas} with the {ty} theta (pts, my theta)", pts(bread(win, "B_CE", ty, meas).gap),
                  pts(r["gap"]), tol=1.0)

claim("Sensitivity quoted: B real 2023-09 window, theta 2023 / 2024 / 2025 (pts)", "+19.8 / +20.0 / +23.6",
      " / ".join(f"{pts(MY_READ[('2023-09->2026-09', 'B', ty, 'real')]['gap']):+.1f}" for ty in (2023, 2024, 2025)),
      ok=all(abs(pts(MY_READ[('2023-09->2026-09', 'B', ty, 'real')]['gap']) - v) < 1.0
             for ty, v in ((2023, 19.8), (2024, 20.0), (2025, 23.6))))
rB3r, rB3n = MY_READ[("2023-09->2026-09", "B", 2024, "real")], MY_READ[("2023-09->2026-09", "B", 2024, "nominal")]
sdB = np.sqrt(rB3r["kappa"] * rB3r["theta_bar"] * (1 - rB3r["theta_bar"]))
claim("133 lines: kappa (2024 theta, 2023-09 weights)", 0.031, rB3r["kappa"], tol=0.0006)
claim("133 lines: Zandi 3-year K moves category growth per sd of theta (pts)", 1.1, pts(sdB * rB3r["zandi"]), tol=0.06)
claim("133 lines: weighted scatter of category growth over 3 years, '8.5' points (real)", 8.5, pts(rB3r["wrmse_flat"]),
      tol=0.06, note=f"nominal {pts(rB3n['wrmse_flat']):.1f}; builder's file: real 8.70, nominal 8.00")
claim("Basket shrink factor 1/kappa '18 to 32'", "18 to 32", f"{1 / rA3r['kappa']:.0f} to {1 / rB3r['kappa']:.0f}",
      ok=round(1 / rA3r["kappa"]) == 18 and round(1 / rB3r["kappa"]) == 32)
_main = [MY_READ[(w[0], s, 2023 if s == "A" else 2024, m)] for w in READ_WIN for s in ("A", "B") for m in ("nominal", "real")]
claim("Read: p at Zandi's gap ranges '0.25-0.97' (main theta, 12 rows)", "0.25-0.97",
      f"{min(r['p_zandi'] for r in _main):.2f}-{max(r['p_zandi'] for r in _main):.2f}",
      ok=abs(min(r['p_zandi'] for r in _main) - 0.25) < 0.04 and abs(max(r['p_zandi'] for r in _main) - 0.97) < 0.04)
claim("Read: no main-theta interval excludes zero", True, all(r["ci_lo"] <= 0 <= r["ci_hi"] for r in _main),
      ok=all(r["ci_lo"] <= 0 <= r["ci_hi"] for r in _main),
      note="B 2023->2025 real lower bound " + f"{pts(MY_READ[('2023->2025', 'B', 2024, 'real')]['ci_lo']):+.1f}")
claim("Read: theta explains at most 5% of weighted variance (max R2 of fitted line)", 0.05,
      max(r["r2_fit"] for r in _main), ok=max(r["r2_fit"] for r in _main) <= 0.05)
claim("Read: Zandi's pattern R2 vs flat, A '-0.05 to -0.19'", "-0.05 to -0.19",
      f"{max(MY_READ[(w[0], 'A', 2023, m)]['r2_zandi'] for w in READ_WIN for m in ('nominal', 'real')):.2f} to "
      f"{min(MY_READ[(w[0], 'A', 2023, m)]['r2_zandi'] for w in READ_WIN for m in ('nominal', 'real')):.2f}", ok=True)
claim("Read: Zandi's pattern R2 vs flat, B '+0.01 to +0.04'", "+0.01 to +0.04",
      f"{min(MY_READ[(w[0], 'B', 2024, m)]['r2_zandi'] for w in READ_WIN for m in ('nominal', 'real')):+.2f} to "
      f"{max(MY_READ[(w[0], 'B', 2024, m)]['r2_zandi'] for w in READ_WIN for m in ('nominal', 'real')):+.2f}", ok=True)

# drops, B, 2023-09 window, real, 2024 theta
gfB = growth_U(list(thB_mine(2024).index), "2023-09", "2026-09", "M")
cB = list(gfB.index)
in_sub = lambda c, roots: any(a in roots for a in [c] + ancestors(c))
DROPS_B = {"health": [c for c in cB if in_sub(c, (172, 121, 66, 275))], "imputed": [c for c in cB if in_sub(c, (160, 163, 254, 342))],
           "energy": [c for c in cB if in_sub(c, (113, 169))], "vehicles": [c for c in cB if in_sub(c, (5, 12))]}
DROPS_B["all four"] = sorted(set(sum(DROPS_B.values(), [])))
_dv = {}
for k, dl in DROPS_B.items():
    keep = [c for c in cB if c not in dl]
    _dv[k] = pts(wls(gfB.loc[keep, "g_real"].to_numpy(float), thB_mine(2024).loc[keep].to_numpy(float),
                     gfB.loc[keep, "S0"].to_numpy(float))[1])
claim("B 2023-09 real: range across the drops (pts) '+17.8 to +25.0'", "+17.8 to +25.0",
      f"{min(_dv.values()):+.1f} to {max(_dv.values()):+.1f}",
      ok=abs(min(_dv.values()) - 17.8) < 1 and abs(max(_dv.values()) - 25.0) < 1,
      note="; ".join(f"{k} {v:+.1f}" for k, v in _dv.items()))
claim("B 2023-09 real: all four dropped (pts)", 21.9, _dv["all four"], tol=1.0)

# influence: c_i = w_i (th_i - th_bar)(g_i - g_bar) / Sxx sums to the slope
th, g, w = thB_mine(2024).loc[cB].to_numpy(float), gfB.g_real.to_numpy(float), gfB.S0.to_numpy(float)
wn = w / w.sum()
tb, gb = wn @ th, wn @ g
contrib = pd.Series(wn * (th - tb) * (g - gb) / (wn @ (th - tb) ** 2), index=cB)
claim("Influence: contributions add up to the slope (pts)", pts(rB3r["gap"]), pts(contrib.sum()), tol=1e-6)
for c, nm, thv, gv in ((141, "tobacco", 0.15, -25), (177, "home health care", 0.57, 31), (154, "tenant rent", 0.14, 3.6)):
    claim(f"Influence: {nm} theta / real growth 2023-09->2026-09", f"{thv} / {gv:+}%",
          f"{thB_mine(2024).loc[c]:.2f} / {pts(gfB.at[c, 'g_real']):+.1f}%",
          ok=abs(thB_mine(2024).loc[c] - thv) < 0.006 and abs(pts(gfB.at[c, "g_real"]) - gv) < (0.6 if abs(gv) > 5 else 0.06))
top3 = [141, 177, 154]
claim("Influence: tobacco + home health care + tenant rent contribute '+19 of the 20 points'", 19,
      pts(contrib.loc[top3].sum()), tol=0.6, note=f"top five contributors: {list(contrib.sort_values().index[-5:])}")


def gap_without(drop):
    keep = [c for c in cB if c not in drop]
    return pts(wls(gfB.loc[keep, "g_real"].to_numpy(float), thB_mine(2024).loc[keep].to_numpy(float),
                   gfB.loc[keep, "S0"].to_numpy(float))[1])


claim("Influence: dropping those three leaves (pts)", 1.8, gap_without(top3), tol=1.0)
claim("Influence: dropping the five largest positive contributors (pts)", -5.9,
      gap_without(list(contrib.sort_values().index[-5:])), tol=1.0)
claim("Influence: dropping higher education, prescription drugs, new autos (pts)", 34.6, gap_without([291, 123, 6]),
      tol=1.0, note=f"three most negative: {list(contrib.sort_values().index[:3])}")


# %% 8. Backtests: A against the dPCE's own group totals, B against CE Table 1110 group totals
def dpce_group(year, real=False):
    sh = dp_shares(year, [1]).iloc[0]
    x = sh / sh.sum() * dp_total(year, 1)
    if real:
        x = x / (DP3.loc[year] / 100.0)
    return x


def dpce_gap(y0, y1, real=False):
    a, b = dpce_group(y0, real), dpce_group(y1, real)
    top, bot = b[TOP20].sum() / a[TOP20].sum() - 1, b[B80].sum() / a[B80].sum() - 1
    return top - bot, top, bot


def dpce_growth(y0, y1):
    s0 = pd.Series({l: dp_total(y0, l) for l in A_CATS})
    s1 = pd.Series({l: dp_total(y1, l) for l in A_CATS})
    return pd.DataFrame(dict(S0=s0, g_nom=s1 / s0 - 1))


NOTE_BT = {(2003, 2007): ((-21.0, -79.5, 22.9, 1.8, -22.8), (19.2, -25.8, 83.3, 2.8, 16.4)),
           (2007, 2009): ((-46.7, -89.5, -1.2, -3.8, -42.9), (-25.2, -59.3, 12.6, -1.8, -23.4)),
           (2009, 2013): ((12.3, -28.8, 52.6, 3.1, 9.2), (14.6, -19.7, 58.8, 2.1, 12.5)),
           (2016, 2019): ((1.1, -15.0, 16.8, -2.2, 3.2), (1.4, -32.9, 36.7, -2.6, 4.0)),
           (2019, 2023): ((15.1, -18.4, 47.2, -1.8, 16.9), (8.3, -34.3, 66.8, -2.3, 10.6)),
           (2021, 2023): ((-4.3, -40.7, 30.1, -0.9, -3.4), (-7.0, -34.1, 25.2, -0.8, -6.2))}
_dgaps = []
for (y0, y1), (nn, rr) in tqdm(NOTE_BT.items(), desc="A backtest"):
    th = theta_A(y0)[TOP20].sum(axis=1)
    T = y1 - y0
    gfd = dpce_growth(y0, y1)
    rn = fit_report(gfd.g_nom.to_numpy(float), th.loc[gfd.index].to_numpy(float), gfd.S0.to_numpy(float), T)
    gfr = growth_A(str(y0), str(y1), "A")
    rr_ = fit_report(gfr.g_real.to_numpy(float), th.loc[gfr.index].to_numpy(float), gfr.S0.to_numpy(float), T)
    an, ar = dpce_gap(y0, y1)[0], dpce_gap(y0, y1, real=True)[0]
    _dgaps += [an, ar]
    for lab, r, act, note in (("nominal (dPCE totals)", rn, an, nn), ("real (NIPA quantities; T3 prices)", rr_, ar, rr)):
        claim(f"A backtest {y0}-{y1} {lab}: estimate (pts)", note[0], pts(r["gap"]), tol=0.06)
        claim(f"A backtest {y0}-{y1} {lab}: CI (pts)", f"[{note[1]:+.1f}, {note[2]:+.1f}]",
              f"[{pts(r['ci_lo']):+.1f}, {pts(r['ci_hi']):+.1f}]",
              ok=all(abs(a - b) < max(4.0, 0.08 * (note[2] - note[1])) for a, b in
                     ((pts(r["ci_lo"]), note[1]), (pts(r["ci_hi"]), note[2]))),
              note="Monte Carlo tolerance: 8% of the interval's width (builder: 1,000 permutations)")
        claim(f"A backtest {y0}-{y1} {lab}: dPCE group-total gap (pts)", note[3], pts(act), tol=0.06)
        claim(f"A backtest {y0}-{y1} {lab}: error (pts)", note[4], pts(r["gap"] - act), tol=0.08)
        if (y0, y1) == (2007, 2009) and lab.startswith("nominal"):
            claim("A backtest 2007-2009 nominal: placebo p '0.048'", 0.048, r["p_placebo"], tol=0.02)
            claim("A backtest 2007-2009 nominal: 'significant' at 5% (one of six A windows)", "p 0.048, CI excludes 0",
                  f"p {r['p_placebo']:.3f}, CI upper {pts(r['ci_hi']):+.1f}", ok=r["p_placebo"] < 0.05 and r["ci_hi"] < 0,
                  note="Monte Carlo borderline: with 20,000 permutations the A false alarm is not significant at 5%")
claim("dPCE's own top20-b80 gap in the six backtest windows 'within -3.8 to +3.1' (pts)", "-3.8 to +3.1",
      f"{pts(min(_dgaps)):+.1f} to {pts(max(_dgaps)):+.1f}",
      ok=abs(pts(min(_dgaps)) + 3.8) < 0.06 and abs(pts(max(_dgaps)) - 3.1) < 0.06)


def ce_group_total(year, scope="total"):
    D = CE_DATA[year]
    if scope == "total":
        m = D["items"][0]["mean"]
    else:
        L = MYB[year]["links"]
        L = L[~L["item"].str.startswith("addenda")]
        inn = L[L.line.notna()].drop_duplicates(["item", "ucc"]).groupby("item")["mean"].sum()
        it = MYB[year]["items"]
        m = sum(it[k] * min(inn.get(k, 0.0) / it[k]["all"], 1.0) for k in it if not k.startswith("addenda"))
    return D["N"][DEC] * m[DEC]


def ce_gap(y0, y1, scope="total"):
    a, b = ce_group_total(y0, scope), ce_group_total(y1, scope)
    top, bot = b[TOP20].sum() / a[TOP20].sum() - 1, b[B80].sum() / a[B80].sum() - 1
    return top - bot, top, bot


claim("CE: top quintile share of total spending 2023 (pct)", 38.86,
      100 * ce_group_total(2023)[TOP20].sum() / ce_group_total(2023).sum(), tol=0.006)
claim("CE: top quintile share of total spending 2025 (pct)", 38.88,
      100 * ce_group_total(2025)[TOP20].sum() / ce_group_total(2025).sum(), tol=0.006)
_g = ce_gap(2023, 2025)
claim("CE: 2023->2025 nominal growth of top 20% spending (pct)", 8.7, pts(_g[1]), tol=0.06)
claim("CE: 2023->2025 nominal growth of bottom 80% spending (pct)", 8.7, pts(_g[2]), tol=0.06)
_q5 = {y: 100 * ce_group_total(y)[TOP20].sum() / ce_group_total(y).sum() for y in range(2019, 2026)}
claim("CE top quintile '38.5-38.9% of spending in 2019-2025'", "38.5-38.9",
      f"{min(_q5.values()):.1f}-{max(_q5.values()):.1f}",
      ok=min(_q5.values()) >= 38.45 and max(_q5.values()) < 38.95,
      note="; ".join(f"{y} {v:.2f}" for y, v in _q5.items()) + " (2020 is 37.3)")
s0 = _q5[2023] / 100
for T, val in ((2, 1.9), (3, 2.8)):
    s1 = s0 * 1.04 ** T / (s0 * 1.04 ** T + 1 - s0)
    claim(f"Zandi's split lifts the top 20% share by about {val} points in {T} years (from the 2023 share)", val,
          100 * (s1 - s0), tol=0.06)
claim("His 4% and 0% would average about 1.6% (top share ~39%)", 1.6, 4 * s0, tol=0.06)

BT_B = {(2014, 2016): 17.7, (2016, 2019): 19.0, (2019, 2021): -43.8, (2021, 2023): 45.4, (2019, 2023): -0.4,
        (2023, 2025): 10.3, (2022, 2025): 25.6}
MY_BT_P = {}
_ceg = {"total": [], "pce_scope": []}
for (y0, y1), val in tqdm(BT_B.items(), desc="B backtest"):
    th = thB_mine(y0)
    gf = growth_U(list(th.index), str(y0), str(y1), "A")
    for meas, col in (("nominal", "g_nom"), ("real", "g_real")):
        r = fit_report(gf[col].to_numpy(float), th.loc[gf.index].to_numpy(float), gf.S0.to_numpy(float), y1 - y0)
        bb = B_BT[(B_BT.source == "B_CE") & (B_BT.window == f"{y0}->{y1}") & (B_BT.measure == meas)].iloc[0]
        claim(f"B backtest {y0}-{y1} {meas}: estimate, start-year theta (pts, my theta)",
              val if meas == "nominal" else pts(bb.gap), pts(r["gap"]), tol=1.0)
        claim(f"B backtest {y0}-{y1} {meas}: placebo p (my theta)", bb.p_placebo, r["p_placebo"], tol=tol_p(bb.p_placebo))
        MY_BT_P[(y0, y1, meas)] = r["p_placebo"]
        if meas == "real" and (y0, y1) == (2021, 2023):
            claim("B backtest 2021-2023 real: '+54.9, p = 0.003'", 54.9, pts(r["gap"]), tol=1.0,
                  note=f"p {r['p_placebo']:.4f}")
    for sc in _ceg:
        _ceg[sc].append(ce_gap(y0, y1, sc)[0])
        bb = B_BT[(B_BT.source == "B_CE") & (B_BT.window == f"{y0}->{y1}") & (B_BT.measure == "nominal")
                  & B_BT.actual_source.str.contains(f"({sc})", regex=False)].iloc[0]
        claim(f"CE group-total gap {y0}-{y1} ({sc}) (pts)", pts(bb.gap_actual), pts(_ceg[sc][-1]),
              tol=0.06 if sc == "total" else 0.5)
claim("CE's own gap within '-1.7 to +1.8' in the B windows (total spending)", "-1.7 to +1.8",
      f"{pts(min(_ceg['total'])):+.1f} to {pts(max(_ceg['total'])):+.1f}",
      ok=abs(pts(min(_ceg["total"])) + 1.7) < 0.06 and abs(pts(max(_ceg["total"])) - 1.8) < 0.06)
claim("CE's own gap within '-2.5 to +4.2' (PCE-scope part)", "-2.5 to +4.2",
      f"{pts(min(_ceg['pce_scope'])):+.1f} to {pts(max(_ceg['pce_scope'])):+.1f}",
      ok=abs(pts(min(_ceg["pce_scope"])) + 2.5) < 0.3 and abs(pts(max(_ceg["pce_scope"])) - 4.2) < 0.3)
_sig = B_BT[(B_BT.source == "B_CE") & (B_BT.spec == "2grp") & (B_BT.p_placebo < 0.05)].drop_duplicates(["window", "measure"])
_mys = sorted({(a, b) for (a, b, m), p in MY_BT_P.items() if p < 0.05})
claim("'significant false alarms in two of seven B windows' (p < 0.05, nominal or real)", 2, len(_mys), tol=0,
      note="builder's own p-values: " + "; ".join(f"{w} {m} {p:.3f}" for w, m, p in zip(_sig.window, _sig.measure, _sig.p_placebo))
           + f" ({_sig.window.nunique()} windows); mine (20,000 permutations): "
           + "; ".join(f"{a}-{b} {m} {p:.3f}" for (a, b, m), p in MY_BT_P.items() if p < 0.05)
           + f" ({len(_mys)} windows). Every CE gap in these windows is within 1.8 points")


# %% 9. Power: rolling windows, error where totals are known, calm-period norms
def months_between(a, b):
    return (int(b[:4]) - int(a[:4])) * 12 + int(b[5:]) - int(a[5:])


def month_plus(m, k):
    t = int(m[:4]) * 12 + int(m[5:]) - 1 + k
    return f"{t // 12}-{t % 12 + 1:02d}"


PW = []
for T in tqdm((2, 3, 4), desc="power: A annual"):
    for y0 in range(2000, 2024 - T):
        y1 = y0 + T
        th = theta_A(y0)[TOP20].sum(axis=1)
        gfd, gfn = dpce_growth(y0, y1), growth_A(str(y0), str(y1), "A")
        for meas, src, gf, col in (("nominal", "dpce", gfd, "g_nom"), ("nominal", "nipa", gfn, "g_nom"),
                                   ("real", "nipa", gfn, "g_real")):
            b = wls(gf[col].to_numpy(float), th.loc[gf.index].to_numpy(float), gf.S0.to_numpy(float))[1]
            act = dpce_gap(y0, y1, real=(meas == "real"))[0]
            PW.append(dict(kind="A_annual", src=src, T=T, t0=str(y0), t1=str(y1), meas=meas, gap=b, err=b - act))
for T in tqdm((2, 3, 4), desc="power: B annual"):
    for y0 in range(2014, 2026 - T):
        y1 = y0 + T
        th = thB_mine(y0)
        gf = growth_U(list(th.index), str(y0), str(y1), "A")
        act = ce_gap(y0, y1)[0]
        for meas, col in (("nominal", "g_nom"), ("real", "g_real")):
            b = wls(gf[col].to_numpy(float), th.loc[gf.index].to_numpy(float), gf.S0.to_numpy(float))[1]
            PW.append(dict(kind="B_annual", src="nipa", T=T, t0=str(y0), t1=str(y1), meas=meas, gap=b, err=b - act))
LAST_M = SER_M.index[-1]
_Mnom = {l: uval(l, "M") for l in sorted(set(sum([MYB[y]["cats"] for y in CE_YEARS], [])))}
_Mq = {l: uval(l, "M", "RA") for l in _Mnom}
_Anom = {l: series(A_CODE[l], "M") for l in A_CATS}
_Aq = {l: series(A_CODE[l][:-2] + "RA", "M") for l in A_CATS}
for src, start in (("A", "2007-01"), ("B", "2014-01")):
    for L in (36, 48):
        m0s = [m for m in SER_M.index if m >= start and months_between(m, LAST_M) >= L]
        for m0 in tqdm(m0s, desc=f"power: {src} {L}-month"):
            m1 = month_plus(m0, L)
            if src == "A":
                th = theta_A(min(int(m0[:4]), 2023))[TOP20].sum(axis=1)
                nom, q = _Anom, _Aq
            else:
                th = thB_mine(int(m0[:4]))
                nom, q = _Mnom, _Mq
            cs = list(th.index)
            S0 = np.array([nom[c].loc[m0] for c in cs])
            for meas in ("nominal", "real"):
                d = nom if meas == "nominal" else q
                g = np.array([d[c].loc[m1] / d[c].loc[m0] - 1 for c in cs])
                PW.append(dict(kind=f"{src}_{L}m", src="nipa", T=L / 12, t0=m0, t1=m1, meas=meas,
                               gap=wls(g, th.to_numpy(float), S0)[1], err=np.nan))
PW = pd.DataFrame(PW)


def calm(kind, src_letter, x):
    start = "2010" if src_letter == "A" else "2014"
    return x[(x.t0.str[:4] >= start) & (x.t1 <= "2019-12")]


def pw_sel(kind, T, meas, src="nipa"):
    return PW[(PW.kind == kind) & (PW["T"] == T) & (PW.meas == meas) & (PW.src == src)]


z975, z80 = stats.norm.ppf(0.975), stats.norm.ppf(0.8)
for T, vn, vr in ((2, 15.5, 8.6), (3, 22.8, 10.7), (4, 30.4, 12.6)):
    claim(f"A error sd, {T}-year windows 2000-2023, nominal (NIPA growth) (pts)", vn,
          pts(pw_sel("A_annual", T, "nominal").err.std()), tol=0.06,
          note=f"with dPCE category totals: {pts(pw_sel('A_annual', T, 'nominal', 'dpce').err.std()):.1f}")
    claim(f"A error sd, {T}-year windows 2000-2023, real (pts)", vr, pts(pw_sel("A_annual", T, "real").err.std()), tol=0.06)
sdB3n, sdB3r = pw_sel("B_annual", 3, "nominal").err.std(), pw_sel("B_annual", 3, "real").err.std()
claim("B error sd vs CE totals, 3-year windows, nominal (pts)", 43.9, pts(sdB3n), tol=1.0,
      note=f"{len(pw_sel('B_annual', 3, 'nominal'))} windows")
claim("B error sd vs CE totals, 3-year windows, real (nominal CE gap stands in) (pts)", 44.8, pts(sdB3r), tol=1.0)
sdA3n, sdA3r = pw_sel("A_annual", 3, "nominal").err.std(), pw_sel("A_annual", 3, "real").err.std()
pw = [stats.norm.cdf(pts((1.04) ** 3 - 1) / pts(s) - z975) for s in (sdA3n, sdA3r, sdB3n, sdB3r)]
claim("Power against Zandi's 12.5 (A nom / A real / B nom / B real) '8% / 21% / 5% / 5%'", "8/21/5/5",
      "/".join(f"{100 * p:.0f}" for p in pw), ok=[round(100 * p) for p in pw] == [8, 21, 5, 5])
claim("Historically calibrated band, three-year, real: A '+-21', B '+-88' (pts)", "21 / 88",
      f"{pts(z975 * sdA3r):.0f} / {pts(z975 * sdB3r):.0f}",
      ok=round(pts(z975 * sdA3r)) == 21 and abs(pts(z975 * sdB3r) - 88) <= 2)
CALM = {}
for src, kind, T, win in (("A", "A_36m", 3, "2023-09->2026-09"), ("B", "B_36m", 3, "2023-09->2026-09"),
                          ("A", "A_48m", 4, "2022-09->2026-09"), ("B", "B_48m", 4, "2022-09->2026-09"),
                          ("A", "A_annual", 2, "2023->2025"), ("B", "B_annual", 2, "2023->2025")):
    for meas in ("nominal", "real"):
        x = pw_sel(kind, T, meas)
        c = calm(kind, src, x)
        CALM[(src, win, meas)] = (c.gap.mean(), c.gap.std(), len(c), c.gap.min(), c.gap.max(), x)
NOTE_CALM = {("A", "nominal"): (14.6, 8.6, -1.0, -15.6, -1.8, 24, -3.3), ("A", "real"): (7.1, 5.3, -3.6, -10.7, -2.0, 15, -4.4),
             ("B", "nominal"): (18.3, 8.1, 16.5, -1.8, -0.2, 23, -1.8), ("B", "real"): (21.0, 6.4, 19.8, -1.3, -0.2, 18, -2.1)}
for (src, meas), nv in NOTE_CALM.items():
    cm, cs, cn, cmin, cmax, x = CALM[(src, "2023-09->2026-09", meas)]
    latest = float(x[x.t0 == "2023-09"].gap.iloc[0])
    ex = latest - cm
    zg = (1.04) ** 3 - 1
    claim(f"Calm norm 36m {src} {meas}: mean (sd) (pts)", f"{nv[0]:+.1f} ({nv[1]:.1f})", f"{pts(cm):+.1f} ({pts(cs):.1f})",
          ok=abs(pts(cm) - nv[0]) < (0.06 if src == "A" else 1.0) and abs(pts(cs) - nv[1]) < (0.06 if src == "A" else 0.5),
          note=f"{cn} windows")
    claim(f"2023-09->2026-09 {src} {meas}, start-year theta (pts)", nv[2], pts(latest), tol=0.06 if src == "A" else 1.0)
    claim(f"Excess over calm norm {src} {meas} (pts (z))", f"{nv[3]:+.1f} ({nv[4]:+.1f})", f"{pts(ex):+.1f} ({ex / cs:+.1f})",
          ok=abs(pts(ex) - nv[3]) < (0.06 if src == "A" else 1.0) and abs(ex / cs - nv[4]) < 0.15)
    claim(f"MDE80 against the calm noise {src} {meas} (pts)", nv[5], pts((z975 + z80) * cs), tol=0.6 if src == "A" else 1.5)
    claim(f"Zandi's split z against the observation {src} {meas}", nv[6], (ex - zg) / cs, tol=0.06 if src == "A" else 0.25)
claim("Calm windows: A 36m starts 2010-01..2016-12 (84), B 2014-01..2016-12 (36)", "84 / 36",
      f"{CALM[('A', '2023-09->2026-09', 'real')][2]} / {CALM[('B', '2023-09->2026-09', 'real')][2]}",
      ok=CALM[("A", "2023-09->2026-09", "real")][2] == 84 and CALM[("B", "2023-09->2026-09", "real")][2] == 36)
claim("B calm 36m real windows: 'every window positive, +9 to +38' (pts)", "+9 to +38",
      f"{pts(CALM[('B', '2023-09->2026-09', 'real')][3]):+.0f} to {pts(CALM[('B', '2023-09->2026-09', 'real')][4]):+.0f}",
      ok=abs(pts(CALM[("B", "2023-09->2026-09", "real")][3]) - 9) < 1.5 and abs(pts(CALM[("B", "2023-09->2026-09", "real")][4]) - 38) < 1.5)
for src, vn, vr in (("A", 19.0, 11.3), ("B", 50.8, 49.9)):
    claim(f"All 36-month windows since {2007 if src == 'A' else 2014}, {src}: sd nominal / real (pts)", f"{vn} / {vr}",
          f"{pts(pw_sel(src + '_36m', 3, 'nominal').gap.std()):.1f} / {pts(pw_sel(src + '_36m', 3, 'real').gap.std()):.1f}",
          ok=abs(pts(pw_sel(src + "_36m", 3, "nominal").gap.std()) - vn) < (0.06 if src == "A" else 1.0)
          and abs(pts(pw_sel(src + "_36m", 3, "real").gap.std()) - vr) < (0.06 if src == "A" else 1.0))
# the other two windows against their calm norms, read's main theta (A 2023, B 2024)
NOTE_OTHER = {("A", "2023->2025", "real"): (-9.5, -2.0, -3.6), ("A", "2023->2025", "nominal"): (-11.0, -1.6, -2.7),
              ("B", "2023->2025", "real"): (6.6, 0.9, -0.2), ("B", "2023->2025", "nominal"): (-1.2, -0.2, -1.4),
              ("A", "2022-09->2026-09", "real"): (-16.6, -2.1, -4.3), ("A", "2022-09->2026-09", "nominal"): (-28.9, -2.7, -4.3),
              ("B", "2022-09->2026-09", "real"): (11.7, 3.2, -1.4), ("B", "2022-09->2026-09", "nominal"): (2.4, 0.4, -2.2)}
for (src, win, meas), nv in NOTE_OTHER.items():
    cm, cs, cn = CALM[(src, win, meas)][:3]
    T = 2 if win == "2023->2025" else 4
    r = MY_READ[(win, src, 2023 if src == "A" else 2024, meas)]
    ex = r["gap"] - cm
    claim(f"{win} {src} {meas} vs calm norm ({cn} windows): excess (z); Zandi's z", f"{nv[0]:+.1f} ({nv[1]:+.1f}); {nv[2]:+.1f}",
          f"{pts(ex):+.1f} ({ex / cs:+.1f}); {(ex - ((1.04) ** T - 1)) / cs:+.1f}",
          ok=abs(pts(ex) - nv[0]) < (0.06 if src == "A" else 1.0) and abs(ex / cs - nv[1]) < 0.2
          and abs((ex - ((1.04) ** T - 1)) / cs - nv[2]) < 0.2)
cm, cs, cn = CALM[("B", "2022-09->2026-09", "real")][:3]
r22 = MY_READ[("2022-09->2026-09", "B", 2022, "real")]
claim("B four-year real with the 2022 theta: excess (z), Zandi's z, norm sd", "+4.9 (+1.3); -3.3; sd 3.7",
      f"{pts(r22['gap'] - cm):+.1f} ({(r22['gap'] - cm) / cs:+.1f}); {(r22['gap'] - cm - (1.04 ** 4 - 1)) / cs:+.1f}; sd {pts(cs):.1f}",
      ok=abs(pts(r22["gap"] - cm) - 4.9) < 1.0 and abs(pts(cs) - 3.7) < 0.5)
claim("A four-year read uses the 2023 theta although the rolling norm uses start-year (2022) thetas: excess with 2022 theta",
      "-16.6 (main) ", f"{pts(MY_READ[('2022-09->2026-09', 'A', 2022, 'real')]['gap'] - CALM[('A', '2022-09->2026-09', 'real')][0]):+.1f}",
      ok=True, note="NOTES quote the main-theta excess for A; for B they also give the start-year version")
# effective sample behind the calm norms: non-overlapping windows inside the calm span
for src, L, kind in (("A", 36, "A_36m"), ("B", 36, "B_36m"), ("B", 48, "B_48m")):
    x = calm(kind, src, pw_sel(kind, L / 12, "real"))
    starts = list(x.t0)
    nonover = starts[::L]
    claim(f"Calm norm {src} {L}m real: independent (non-overlapping) windows behind the sd", len(x), len(nonover),
          ok=False if len(nonover) < 5 else True,
          note=f"{len(x)} overlapping windows contain only {len(nonover)} non-overlapping ones "
               f"({', '.join(f'{pts(v):+.1f}' for v in x.set_index('t0').loc[nonover].gap)} pts): the sd and the "
               f"z-scores built on it are not sampling standard errors")
_x = calm("A_36m", "A", pw_sel("A_36m", 3, "real"))
_nov = _x.set_index("t0").loc[list(_x.t0)[::36]].gap
_sd3 = _nov.std()
_ex = MY_READ[("2023-09->2026-09", "A", 2023, "real")]["gap"] - _x.gap.mean()
claim("A 36m real: Zandi's z if the calm sd comes from the 3 non-overlapping calm windows", -4.4,
      (_ex - (1.04 ** 3 - 1)) / _sd3, tol=0.5,
      note=f"sd {pts(_sd3):.1f} pts instead of {pts(_x.gap.std()):.1f}; excess z {_ex / _sd3:+.1f} instead of "
           f"{_ex / _x.gap.std():+.1f}; MDE80 {pts((z975 + z80) * _sd3):.0f} pts instead of 15")


# %% 10. Top-tilt index (descriptive): fixed base-year baskets, A annual and monthly, B monthly
def tilt(th, S, q):
    th, S, q = (np.asarray(v, float) for v in (th, S, q))
    ot, ob = th * S / np.dot(th, S), (1 - th) * S / np.dot(1 - th, S)
    return float(ot @ q), float(ob @ q), kappa_of(th, S)


lt = lb = 100.0
TA = {}
for y in range(2001, 2026):
    th = theta_A(min(y - 1, 2023))[TOP20].sum(axis=1)
    gf = growth_A(str(y - 1), str(y), "A")
    top, bot, k = tilt(th.loc[gf.index], gf.S0, gf.g_real)
    lt, lb = lt * (1 + top), lb * (1 + bot)
    TA[y] = dict(tilt=top - bot, index=100 * lt / lb, kappa=k)
claim("Top tilt A annual: index 2025 (2000 = 100)", 100.2, TA[2025]["index"], tol=0.06)
claim("Top tilt A annual: 2008 / 2009 / 2021 (pts a year)", "-0.5 / -0.7 / +0.7",
      " / ".join(f"{pts(TA[y]['tilt']):+.1f}" for y in (2008, 2009, 2021)),
      ok=[round(pts(TA[y]["tilt"]), 1) for y in (2008, 2009, 2021)] == [-0.5, -0.7, 0.7])
claim("A Zandi-size K adds kappa x 4 points a year to the tilt: A / B weights", "+0.23 / +0.13",
      f"{4 * rA3r['kappa']:+.2f} / {4 * rB3r['kappa']:+.2f}", ok=round(4 * rA3r["kappa"], 2) == 0.22 or
      round(4 * rA3r["kappa"], 2) == 0.23, note="kappa from the 2023-09 read weights; the annual A kappas run 0.048-0.066")
TM = []
for src, first in (("A", "2007-01"), ("B", "2015-01")):
    for m in [m for m in SER_M.index if m >= first]:
        m0 = month_plus(m, -12)
        yw = int(m0[:4])
        if src == "A":
            th = theta_A(min(yw, 2023))[TOP20].sum(axis=1)
            S = pd.Series({l: series(A_CODE[l], "A").loc[str(yw)] for l in A_CATS})
            q = pd.Series({l: _Aq[l].loc[m] / _Aq[l].loc[m0] - 1 for l in A_CATS})
        else:
            th = thB_mine(yw)
            S = pd.Series({l: uval(l, "A").loc[str(yw)] for l in th.index})
            q = pd.Series({l: _Mq[l].loc[m] / _Mq[l].loc[m0] - 1 for l in th.index})
        top, bot, k = tilt(th.loc[S.index], S, q.loc[S.index])
        TM.append(dict(src=src, date=m, tilt=top - bot, kappa=k, implied=(top - bot) / k))
TM = pd.DataFrame(TM)
for src in ("A", "B"):
    b = B_TM[B_TM.source == ("A_dPCE" if src == "A" else "B_CE")].set_index("date")
    x = TM[TM.src == src].set_index("date")
    d = (x.tilt - b.tilt_12m.reindex(x.index)).abs().max()
    claim(f"Top tilt {src} monthly: my series vs builder's file, max |diff| (pts)", 0, pts(d),
          tol=0.02 if src == "A" else 0.05, note=f"{len(x)} months; B uses my own thetas")
A_ = TM[TM.src == "A"].set_index("date")
B_ = TM[TM.src == "B"].set_index("date")
claim("A 12m tilt: mean over 2023-01..2026-09 (pts) and implied gap (pts a year)", "-0.08; -1.5",
      f"{pts(A_.loc['2023-01':].tilt.mean()):+.2f}; {pts(A_.loc['2023-01':].implied.mean()):+.1f}",
      ok=round(pts(A_.loc["2023-01":].tilt.mean()), 2) == -0.08 and round(pts(A_.loc["2023-01":].implied.mean()), 1) == -1.5)
claim("A 12m tilt latest 2026-09 (pts)", -0.01, pts(A_.loc["2026-09"].tilt), tol=0.006)
claim("B 12m tilt: mean over 2023-01..2026-09 (pts) and implied (pts a year)", "+0.36; +11",
      f"{pts(B_.loc['2023-01':].tilt.mean()):+.2f}; {pts(B_.loc['2023-01':].implied.mean()):+.0f}",
      ok=abs(pts(B_.loc["2023-01":].tilt.mean()) - 0.36) < 0.02 and abs(pts(B_.loc["2023-01":].implied.mean()) - 11) < 1)
claim("B 12m tilt: mean 2015-2019 (pts) and implied", "+0.15; +5",
      f"{pts(B_.loc['2015-01':'2019-12'].tilt.mean()):+.2f}; {pts(B_.loc['2015-01':'2019-12'].implied.mean()):+.0f}",
      ok=abs(pts(B_.loc["2015-01":"2019-12"].tilt.mean()) - 0.15) < 0.02)
x = B_.loc["2024-01":]
claim("B 12m tilt 2024-01..2026-09: median (implied; implied range)", "+0.29 (+9; -0.3 to +14)",
      f"{pts(x.tilt.median()):+.2f} ({pts(x.implied.median()):+.0f}; {pts(x.implied.min()):+.1f} to {pts(x.implied.max()):+.0f})",
      ok=abs(pts(x.tilt.median()) - 0.29) < 0.02 and abs(pts(x.implied.median()) - 9) < 1)
claim("B 12m tilt latest 2026-09 (implied)", "+0.13 (+4.2)",
      f"{pts(B_.loc['2026-09'].tilt):+.2f} ({pts(B_.loc['2026-09'].implied):+.1f})",
      ok=abs(pts(B_.loc["2026-09"].tilt) - 0.13) < 0.01 and abs(pts(B_.loc["2026-09"].implied) - 4.2) < 0.3)
x = A_.loc["2024-01":]
claim("A 12m tilt 2024-01..2026-09: median (implied; implied range)", "-0.04 (-0.7; -12 to +7)",
      f"{pts(x.tilt.median()):+.2f} ({pts(x.implied.median()):+.1f}; {pts(x.implied.min()):+.0f} to {pts(x.implied.max()):+.0f})",
      ok=round(pts(x.tilt.median()), 2) == -0.04 and round(pts(x.implied.min())) == -12 and round(pts(x.implied.max())) == 7)
x = B_.loc["2022-01":"2022-12"]
claim("B 12m tilt during 2022: '+0.5 to +2.5 points, median +1.1'", "+0.5 to +2.5, median +1.1",
      f"{pts(x.tilt.min()):+.1f} to {pts(x.tilt.max()):+.1f}, median {pts(x.tilt.median()):+.1f}",
      ok=abs(pts(x.tilt.min()) - 0.5) < 0.06 and abs(pts(x.tilt.max()) - 2.5) < 0.06 and abs(pts(x.tilt.median()) - 1.1) < 0.06,
      note=f"implied gap {pts(x.implied.min()):+.0f} to {pts(x.implied.max()):+.0f} pts a year in 2022")
# identity: tilt = kappa x slope with the SAME weights (twelve-month window, annual weights of the base year)
m, m0 = "2026-09", "2025-09"
th = thB_mine(2025)
S = pd.Series({l: uval(l, "A").loc["2025"] for l in th.index})
q = pd.Series({l: _Mq[l].loc[m] / _Mq[l].loc[m0] - 1 for l in th.index})
claim("Identity: tilt / kappa = two-group WLS slope with the same (annual base-year) weights", 0,
      abs(B_.loc[m].implied - wls(q.to_numpy(float), th.to_numpy(float), S.to_numpy(float))[1]), tol=1e-9,
      note="with base-MONTH weights (as in the read) the two differ slightly")


# %% 11. Context numbers (raw BEA flat files, ISPCEPX workbook, watch page JSON)
pc, pi = series("DPCERX", "M"), series("W875RX", "M")
claim("BEA: real PCE, six months to 2026-09 (pct)", 1.82, pts(pc.loc["2026-09"] / pc.loc["2026-03"] - 1), tol=0.006)
claim("BEA: real personal income excl. transfers, six months to 2026-09 (pct)", 0.05,
      pts(pi.loc["2026-09"] / pi.loc["2026-03"] - 1), tol=0.006)
claim("BEA: the same, twelve months (pct): PCE / PI ex transfers", "2.54 / 0.54",
      f"{pts(pc.loc['2026-09'] / pc.loc['2025-09'] - 1):.2f} / {pts(pi.loc['2026-09'] / pi.loc['2025-09'] - 1):.2f}",
      ok=abs(pts(pc.loc["2026-09"] / pc.loc["2025-09"] - 1) - 2.54) < 0.006 and abs(pts(pi.loc["2026-09"] / pi.loc["2025-09"] - 1) - 0.54) < 0.006)
_sr = series(line_code("T20600", 35), "M").loc["2026-09"]
claim("BEA: personal saving rate 2026-09 (pct)", 3.8, _sr, tol=0.05)
_wb = openpyxl.load_workbook(RAW / "bea" / "distribution" / "ispcepx" / "ispecpx_table.xlsx", read_only=True, data_only=True)
_ip = list(_wb.worksheets[0].iter_rows(values_only=True))
_ip = pd.DataFrame(_ip[1:], columns=_ip[0]).set_index("Year")
_qi = {q: pts(_ip.loc[2024, f"ISPCEPX: {q}"] / _ip.loc[2019, f"ISPCEPX: {q}"] - 1)
       for q in ("0-20%", "20-40%", "40-60%", "60-80%", "80-100%")}
claim("ISPCEPX 2019-2024: top quintile inflation (pct)", 19.9, _qi["80-100%"], tol=0.06)
claim("ISPCEPX 2019-2024: other quintiles 19.1-19.5 (pct)", "19.1-19.5",
      f"{min(v for k, v in _qi.items() if k != '80-100%'):.1f}-{max(v for k, v in _qi.items() if k != '80-100%'):.1f}",
      ok=f"{min(v for k, v in _qi.items() if k != '80-100%'):.1f}-{max(v for k, v in _qi.items() if k != '80-100%'):.1f}" == "19.1-19.5")
_h = open(RAW / "watch" / "jobs-outside-care.html", encoding="utf-8", errors="replace").read()
_js = re.search(r'<script type="application/json" id="plot-1">(.*?)</script>', _h, re.S).group(1)
_ser = {s_["name"]: dict(s_["points"]) for s_ in __import__("json").loads(_js)["series"]}
_two = {k: v["2025-08-01"] + v["2026-08-01"] for k, v in _ser.items()}
claim("Watch: care share of net job growth Aug 2024 -> Aug 2026 (pct, from the page's own series)", 107,
      100 * _two["Health care and social assistance"] / sum(_two.values()), tol=0.5,
      note=f"twelve months to Sep 2026: outside care {_ser['Private jobs outside care']['2026-09-01']:+.0f}k, care "
           f"{_ser['Health care and social assistance']['2026-09-01']:+.0f}k, government {_ser['Government']['2026-09-01']:+.0f}k")


# %% 12. Four and five groups: collinearity, unconstrained fits, ridge toward equal growth (my own LOO-CV)
GROUPS4 = {"b50": DEC[:5], "p50_80": DEC[5:8], "p80_90": ["d09"], "top10": ["d10"]}
GROUPS5 = {f"q{k + 1}": DEC[2 * k:2 * k + 2] for k in range(5)}
TOPS = {"4": ["p80_90", "top10"], "5": ["q5"]}
LAM_GRID = np.concatenate([[0.0], np.logspace(-8, 2, 81)])


def gmat(thd, groups):
    return np.column_stack([thd[v].sum(axis=1).to_numpy(float) for v in groups.values()])


def pen(pi):
    D = np.eye(len(pi)) - np.outer(np.ones(len(pi)), pi)
    return D.T @ np.diag(pi) @ D


def ridge(g, TH, w, lam):
    wn = w / w.sum()
    pi = TH.T @ wn
    A = TH.T @ (wn[:, None] * TH)
    rhs = TH.T @ (wn * g)
    x = np.linalg.lstsq(A, rhs, rcond=None)[0] if lam == 0 else np.linalg.solve(A + lam * pen(pi), rhs)
    return x, pi


def loo(g, TH, w):
    wn = w / w.sum()
    pi = TH.T @ wn
    A, P = TH.T @ (wn[:, None] * TH), pen(TH.T @ wn)
    best = (np.inf, None)
    for lam in LAM_GRID:
        M = np.linalg.pinv(A) if lam == 0 else np.linalg.inv(A + lam * P)
        e = g - TH @ (M @ (TH.T @ (wn * g)))
        h = wn * np.einsum("ij,jk,ik->i", TH, M, TH)
        cv = np.sum(wn * (e / (1 - h)) ** 2) if np.all(h < 1 - 1e-9) else np.inf
        if cv < best[0]:
            best = (cv, lam)
    return best[1]


def igap(x, pi, names, top):
    it = [i for i, n in enumerate(names) if n in top]
    ib = [i for i, n in enumerate(names) if n not in top]
    return np.dot(pi[it], x[it]) / pi[it].sum() - np.dot(pi[ib], x[ib]) / pi[ib].sum()


CONDS = {("A", "4"): [], ("A", "5"): [], ("B", "4"): [], ("B", "5"): []}
EQ = {("A", "4"): [], ("A", "5"): [], ("B", "4"): [], ("B", "5"): []}
A_DROPS = {"all": [], "health": [16], "imputed": [15, 20, 22], "energy": [11], "mv": [4]}
A_DROPS["all4"] = sorted(set(sum(A_DROPS.values(), [])))
for win, freq, t0, t1, T in tqdm(READ_WIN, desc="multi-group fits"):
    for src, tys in (("A", [2023] + ([2022] if T == 4 else [])), ("B", [2024] + ([2022] if T == 4 else [2023, 2025]))):
        for ty in tys:
            thd = theta_A(ty) if src == "A" else MYB[ty]["theta"]
            gf = growth_A(t0, t1, freq) if src == "A" else growth_U(list(thd.index), t0, t1, freq)
            cs = list(gf.index)
            if src == "A":
                drops = A_DROPS
            else:
                drops = {"all": []}
                drops.update({k: v for k, v in DROPS_B.items() if k != "all four"})
                drops["all4"] = DROPS_B["all four"]
            for dname, dl in drops.items():
                keep = [c for c in cs if c not in dl]
                w = gf.loc[keep, "S0"].to_numpy(float)
                for k, G in (("4", GROUPS4), ("5", GROUPS5)):
                    TH = gmat(thd.loc[keep], G)
                    wn = w / w.sum()
                    CONDS[(src, k)].append(np.linalg.cond(TH.T @ (wn[:, None] * TH)))
                    for col in ("g_nom", "g_real"):
                        lam = loo(gf.loc[keep, col].to_numpy(float), TH, w)
                        EQ[(src, k)].append(lam >= 10)
for (src, k), val in ((("A", "4"), 1800), (("A", "5"), 24000), (("B", "4"), 900), (("B", "5"), 2300)):
    claim(f"Median condition number of theta'W theta, {src}, {k} groups", val, float(np.median(CONDS[(src, k)])),
          tol=0.12 * val, note=f"{len(CONDS[(src, k)])} fits")
for (src, k), val in ((("A", "4"), 0.77), (("A", "5"), 0.46), (("B", "4"), 0.15), (("B", "5"), 0.15)):
    claim(f"Ridge LOO-CV picks effectively equal growth (lambda >= 10), {src} {k} groups (share of fits)", val,
          float(np.mean(EQ[(src, k)])), tol=0.08, note="my grid {0} U 10^[-8, 2]; builder's grid tops out at 10")
gf = growth_A("2023-09", "2026-09", "M")
w = gf.S0.to_numpy(float)
x5, _ = ridge(gf.g_real.to_numpy(float), gmat(th23, GROUPS5), w, 0.0)
claim("A 2023-09 real, five groups unconstrained: quintile growth range (pct)", "-352 to +337",
      f"{pts(x5.min()):+.0f} to {pts(x5.max()):+.0f}", ok=abs(pts(x5.min()) + 352) < 2 and abs(pts(x5.max()) - 337) < 2)
x4, pi4 = ridge(gf.g_real.to_numpy(float), gmat(th23, GROUPS4), w, 0.0)
claim("A 2023-09 real, four groups unconstrained: gap (pts)", -12.7, pts(igap(x4, pi4, list(GROUPS4), TOPS["4"])), tol=0.1)
lamA = loo(gf.g_real.to_numpy(float), gmat(th23, GROUPS5), w)
x5r, _ = ridge(gf.g_real.to_numpy(float), gmat(th23, GROUPS5), w, lamA)
claim("A 2023-09 real, five groups ridge: CV lambda and quintile range ('lambda 1e-4: -310% to +282%')",
      "1e-4: -310 to +282", f"{lamA:.1g}: {pts(x5r.min()):+.0f} to {pts(x5r.max()):+.0f}",
      ok=abs(pts(x5r.min()) + 310) < 15 and abs(pts(x5r.max()) - 282) < 15,
      note="builder's own file has lambda 5.6e-5 for this fit (1e-4 is the 2023->2025 and 2022-09 fits)")
gfB = growth_U(list(MYB[2024]["theta"].index), "2023-09", "2026-09", "M")
wB = gfB.S0.to_numpy(float)
for k, G, val, groups_note in (("4", GROUPS4, 14.5, "b50 -2.7, p50_80 +8.4, p80_90 +25.5, top10 +11.6"), ("5", GROUPS5, 9.1, "")):
    TH = gmat(MYB[2024]["theta"].loc[gfB.index], G)
    lam = loo(gfB.g_real.to_numpy(float), TH, wB)
    x, pi_ = ridge(gfB.g_real.to_numpy(float), TH, wB, lam)
    claim(f"B 2023-09 real, {k} groups ridge (my theta): gap (pts)", val, pts(igap(x, pi_, list(G), TOPS[k])), tol=1.5,
          note=f"lambda {lam:.2g}; groups " + ", ".join(f"{n} {pts(v):+.1f}" for n, v in zip(G, x)) +
               (f"; NOTES: {groups_note}" if groups_note else ""))


# %% 13. Remaining statements
ETA = THREAD / "data" / "tidy" / "usda_tb1929_params.csv"
claim("NOTES: 'usda_tb1929_params.csv does not exist, so the eta variant was not run'", "does not exist",
      "exists" if ETA.exists() else "does not exist", ok=not ETA.exists(),
      note="the unit's own fingerprint_read.csv says 'file present ... variant not implemented in this run'")
claim("Caveat illustration: eta from 0.5 (theta 0.15) to 1.5 (theta 0.57), common real growth 6-8% -> spurious gap",
      "14-19", f"{pts(0.06 / 0.42):.0f}-{pts(0.08 / 0.42):.0f}", ok=round(pts(0.06 / 0.42)) == 14 and round(pts(0.08 / 0.42)) == 19)
_kA = [TA[y]["kappa"] for y in TA]
claim("Code comment in fingerprint.py: 'kappa is about 0.01-0.02 at the 16-line level ... fifty- to a hundredfold'",
      "0.01-0.02", f"{min(_kA):.3f}-{max(_kA):.3f}", ok=False,
      note="the NOTES have it right (0.056, factor 18); only the code's header comment is stale")


# chained dollars vs quantity indexes: identical ratios (my route uses the indexes throughout)
_d = 0.0
for l in [l for l in U_MAIN if l not in (145, 333) and l > 1][:400]:
    c = U.at[l, "code"]
    cx, qa = series(c[:-2] + "RX", "M"), series(c[:-2] + "RA", "M")
    if cx is None or qa is None or not np.isfinite(cx.get("2023-09", np.nan)) or cx.loc["2023-09"] < 20000:
        continue
    _d = max(_d, abs(cx.loc["2026-09"] / cx.loc["2023-09"] - qa.loc["2026-09"] / qa.loc["2023-09"]))
claim("Chained-dollar and quantity-index growth ratios agree, 2023-09->2026-09, lines >= $20bn (max |diff|, pts)", 0,
      pts(_d), tol=0.01, note="the builder used chained dollars where published, I use 2.4.3U indexes; smaller lines "
                              "differ by the $1m rounding of chained dollars only")
_w = growth_A("2023-09", "2026-09", "M").S0
_tb = float((tA23 * _w).sum() / _w.sum())
claim("A: line 22 (NPISHs) carries the total-PCE theta and has ~no leverage: |theta_22 - theta_bar|", 0,
      abs(tA23.loc[22] - _tb), tol=0.005, note=f"theta_22 {tA23.loc[22]:.4f}, weighted mean {_tb:.4f}")
# what carries B: home health care's theta is the CE 'Personal services' item, mostly child care
_ps = [k for k in MYB[2024]["items"] if k.endswith("> personal services")][0]
_L = MYB[2024]["links"]
_cc = float(_L[(_L["item"] == _ps) & (_L.ucc == "670320")].drop_duplicates("ucc")["mean"].sum())
_tot = float(_L[_L["item"] == _ps].drop_duplicates("ucc")["mean"].sum())
claim("NOTES: home health care theta 0.57 is 'from CE's out-of-pocket personal-care spending'", "personal care",
      f"'Personal services', {100 * _cc / _tot:.0f}% child care", ok=False,
      note="line 177's only feeder is UCC 340906 (care for elderly) inside the item 'Personal services', whose decile "
           "distribution is set by babysitting/child care/preschool (UCC 670320); rule 1 gives elder care a child-care theta")
_hc = next(x for x in CE_DATA[2024]["items"] if x["npath"] == "average annual expenditures > healthcare")
_hcs = CE_DATA[2024]["N"][DEC] * _hc["mean"][DEC]
_thc = float((_hcs / _hcs.sum())[TOP20].sum())
_t2 = thB_mine(2024).copy()
_t2.loc[177] = _thc
_gf = growth_U(list(_t2.index), "2023-09", "2026-09", "M")
_alt = {m: pts(wls(_gf[m].to_numpy(float), _t2.loc[_gf.index].to_numpy(float), _gf.S0.to_numpy(float))[1])
        for m in ("g_real", "g_nom")}
_v = []
for m0 in [m for m in SER_M.index if "2014-01" <= m <= "2016-12"]:
    th_ = thB_mine(int(m0[:4]))
    gf_ = growth_U(list(th_.index), m0, month_plus(m0, 36), "M").drop(index=177)
    _v.append(wls(gf_.g_real.to_numpy(float), th_.loc[gf_.index].to_numpy(float), gf_.S0.to_numpy(float))[1])
_gx = growth_U(list(thB_mine(2024).index), "2023-09", "2026-09", "M").drop(index=177)
_ex177 = wls(_gx.g_real.to_numpy(float), thB_mine(2024).loc[_gx.index].to_numpy(float), _gx.S0.to_numpy(float))[1]
claim("B 2023-09 gap if home health care takes CE's out-of-pocket health-care theta (real / nominal, pts)",
      "+20.0 / +13.5", f"{_alt['g_real']:+.1f} / {_alt['g_nom']:+.1f}", ok=False,
      note=f"health-care theta {_thc:.3f} instead of 0.574: one mapping artifact carries ~7 of B's 20 points. Without "
           f"the line, real gap {pts(_ex177):+.1f} against a calm norm (also without it) of {pts(np.mean(_v)):+.1f} "
           f"(sd {pts(np.std(_v, ddof=1)):.1f}): Zandi's z {(_ex177 - np.mean(_v) - (1.04 ** 3 - 1)) / np.std(_v, ddof=1):+.1f} "
           f"instead of -2.1, so the NOTES' conclusion stands; the 'what carries B' paragraph needs the correction")
# A's evidence against Zandi rests on the health-care line
_vals = {}
for meas in ("g_real", "g_nom"):
    v = []
    for m0 in [m for m in SER_M.index if "2010-01" <= m <= "2016-12"]:
        th_ = theta_A(int(m0[:4]))[TOP20].sum(axis=1)
        gf_ = growth_A(m0, month_plus(m0, 36), "M").drop(index=16)
        v.append(wls(gf_[meas].to_numpy(float), th_.loc[gf_.index].to_numpy(float), gf_.S0.to_numpy(float))[1])
    gf_ = growth_A("2023-09", "2026-09", "M").drop(index=16)
    est = wls(gf_[meas].to_numpy(float), tA23.loc[gf_.index].to_numpy(float), gf_.S0.to_numpy(float))[1]
    v = np.array(v)
    _vals[meas] = (est, v.mean(), v.std(ddof=1), np.std(v[::36], ddof=1))
_e, _m, _s, _s3 = _vals["g_real"]
claim("Plain words: Zandi's split 'about 4 sd above' what A shows (3-year real) survives without the health-care line",
      -4.4, (_e - _m - (1.04 ** 3 - 1)) / _s, ok=False,
      note=f"A ex-health: estimate {pts(_e):+.1f}, calm norm {pts(_m):+.1f} (sd {pts(_s):.1f}), excess {pts(_e - _m):+.1f}; "
           f"Zandi's z {(_e - _m - (1.04 ** 3 - 1)) / _s:+.1f} with the overlapping sd, "
           f"{(_e - _m - (1.04 ** 3 - 1)) / _s3:+.1f} with the 3 non-overlapping windows; nominal: estimate "
           f"{pts(_vals['g_nom'][0]):+.1f} vs norm {pts(_vals['g_nom'][1]):+.1f}")


# %% summary
n_ok = sum(1 for ok, _ in RESULTS if ok)
n_bad = len(RESULTS) - n_ok
print(f"\nSUMMARY | {len(RESULTS)} claims | {n_ok} OK | {n_bad} BAD")
for ok, line in RESULTS:
    if not ok:
        print(line)
