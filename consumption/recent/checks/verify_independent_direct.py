# verify_independent_direct.py - INDEPENDENT VERIFICATION of the direct-reads unit in consumption/recent/
# (code/direct.py, out/direct_*.csv, NOTES_direct.md).
#
# Separate route, by design:
#   * no import of, and no code copied from, direct.py or check_direct.py;
#   * every input read from the RAW vendored files, never from data/tidy:
#       - CE Tables 1110 / 1101 and the aggregate-share tables: the .xlsx parsed with zipfile + xml.etree, the
#         hierarchy taken from the label cells' indent in styles.xml;
#       - BLS distributional PCE workbook, BEA-BLS joint workbook, ISPCEPX workbook (same raw reader);
#       - BEA distribution of personal income: summary-file.csv and the nowcast <table> in the HTML page;
#       - NIPA FlatFiles.zip (nipadataA/M); DFA dfa.zip; Z.1 z1_csv_files.zip (S1M.b, S1M.r);
#       - SCF 2025 and 2022 summary extracts straight from the Fed zips; percentile groups rebuilt from the
#         SCF macro's own rule (bulletin.macro.txt, %PCTL) and checked against the published categories;
#       - FEDS Note (accessible version) tables and the 2026 Bulletin's Box 1 text; the post text for its c_w
#         and MPC parameters; the dPCE methods page for Table 3.1 and Figure 3.1;
#   * my own SCF family bootstrap (1,000 replicates, different seed; --fast: 200).
# The builder's NOTES numbers are hard-coded below as a reader would quote them; for whole tables its CSVs are
# read only to print the 'builder value' column next to mine.
#
# Output: one line per claim, 'OK | claim | builder value | my value | note' or 'BAD | ...', then the counts and
# the BAD lines again. Run from the repo root:
#     venv/bin/python -I consumption/recent/checks/verify_independent_direct.py          # about 15 s
# Plain functions plus top-level code; '# %%' cells paste into a notebook.

# %% setup
import html
import io
import re
import sys
import warnings
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from tqdm.auto import tqdm

warnings.filterwarnings("ignore")

HERE = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd() / "consumption/recent/checks"
RECENT = HERE.parent
THREAD = RECENT.parent
RAW = THREAD / "data" / "raw"
OUT = RECENT / "out"
NOTES = (RECENT / "NOTES_direct.md").read_text(encoding="utf-8")

FAST = "--fast" in sys.argv
N_BOOT = 200 if FAST else 1000
RNG = np.random.default_rng(73019)        # deliberately not the builder's seed
ZANDI_TOP, ZANDI_B80 = 0.04, 0.0

RESULTS = []


def fmt(v):
    if isinstance(v, (float, np.floating)):
        if not np.isfinite(v):
            return "nan"
        return f"{v:.4g}" if abs(v) < 1e4 else f"{v:,.0f}"
    return str(v)


def claim(text, builder, mine, tol=None, ok=None, note=""):
    """Record and print one claim. Numbers: OK when |builder - mine| <= tol. Or pass ok= explicitly."""
    if ok is None:
        try:
            b, m = float(builder), float(mine)
            ok = bool(np.isfinite(b) and np.isfinite(m) and abs(b - m) <= tol)
        except (TypeError, ValueError):
            ok = builder == mine
    line = f"{'OK ' if ok else 'BAD'} | {text} | {fmt(builder)} | {fmt(mine)} | {note}"
    RESULTS.append((ok, line))
    print(line, flush=True)
    return ok


def claim_vec(text, builder, mine, tol, note=""):
    """Element-wise comparison of two equal-length sequences: OK when the largest |difference| <= tol."""
    b = np.asarray(builder, float)
    m = np.asarray(mine, float)
    assert b.shape == m.shape, (text, b.shape, m.shape)
    d = np.abs(b - m)
    worst = int(np.nanargmax(d))
    ok = bool(np.all(np.isfinite(d)) and d.max() <= tol)
    return claim(text, f"{len(b)} values", f"max |diff| {d.max():.3g}", ok=ok,
                 note=(note + "; " if note else "") + f"worst: builder {b[worst]:.4g} vs mine {m[worst]:.4g}")


def r1(x):
    return float(np.round(x, 1))


# %% raw readers: xlsx (zipfile + xml.etree)
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
      "pr": "http://schemas.openxmlformats.org/package/2006/relationships"}


def col_index(ref):
    n = 0
    for ch in re.match(r"[A-Z]+", ref).group(0):
        n = n * 26 + (ord(ch) - 64)
    return n - 1


def read_xlsx(path):
    """{sheet: {(row0, col0): (value, indent)}} from the raw XML; strings resolved, numbers as float."""
    z = zipfile.ZipFile(path)
    names = set(z.namelist())
    ss = []
    if "xl/sharedStrings.xml" in names:
        for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
            ss.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
    indents = []
    if "xl/styles.xml" in names:
        for xf in ET.fromstring(z.read("xl/styles.xml")).find("m:cellXfs", NS).findall("m:xf", NS):
            al = xf.find("m:alignment", NS)
            indents.append(int(al.get("indent", 0)) if al is not None else 0)
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = {r.get("Id"): r.get("Target")
            for r in ET.fromstring(z.read("xl/_rels/workbook.xml.rels")).findall("pr:Relationship", NS)}
    out = {}
    for sh in wb.find("m:sheets", NS).findall("m:sheet", NS):
        target = rels[sh.get("{%s}id" % NS["r"])].lstrip("/")
        target = target if target.startswith("xl/") else "xl/" + target
        cells = {}
        for c in ET.fromstring(z.read(target)).iter("{%s}c" % NS["m"]):
            ref = c.get("r")
            r0, c0 = int(re.search(r"\d+", ref).group(0)) - 1, col_index(ref)
            t, s, v = c.get("t", "n"), int(c.get("s", 0)), c.find("m:v", NS)
            if t == "s":
                val = ss[int(v.text)] if v is not None else None
            elif t == "inlineStr":
                val = "".join(x.text or "" for x in c.iter("{%s}t" % NS["m"]))
            elif t in ("str", "e"):
                val = v.text if v is not None else None
            else:
                val = float(v.text) if v is not None and v.text not in (None, "") else None
            cells[(r0, c0)] = (val, indents[s] if s < len(indents) else 0)
        out[sh.get("name")] = cells
    return out


def sheet_rows(cells, ncol=None):
    nr = max(r for r, _ in cells) + 1
    nc = ncol or max(c for _, c in cells) + 1
    return [[cells.get((r, c), (None, 0))[0] for c in range(nc)] for r in range(nr)]


# %% A0. CE tables: parse every year (label hierarchy from the indent of the label cells)
DEC = [f"d{k:02d}" for k in range(1, 11)]
QUI = [f"q{k}" for k in range(1, 6)]
B80Q = QUI[:4]
STATS = {"Mean": "mean", "Share": "share", "SE": "se", "RSE": "rse", "CV(%)": "rse"}
AAE = "Average annual expenditures"


def clean_label(s):
    s = re.sub(r"\s+", " ", str(s)).strip()
    s = re.sub(r"(\s+[a-e]/)+$", "", s)
    return re.sub(r"\s*#$", "", s).strip()


def parse_ce(path, cols):
    cells = next(iter(read_xlsx(path).values()))
    nrow = max(r for r, _ in cells) + 1
    hdr = next(r for r in range(nrow) if cells.get((r, 0), (None,))[0] == "Item")
    stack, data, cur = [], {}, None
    for r in range(hdr + 1, nrow):
        a = cells.get((r, 0))
        if a is None or a[0] in (None, ""):
            continue
        vals = []
        for c in range(1, len(cols) + 1):
            v = cells.get((r, c), (None,))[0]
            vals.append(v if isinstance(v, float) else np.nan)      # codes (b/, c/, n.a.) -> NaN
        lab = str(a[0]).strip()
        if lab in STATS:
            if cur is not None:
                data.setdefault(cur, {})[STATS[lab]] = pd.Series(vals, index=cols)
            continue
        while stack and stack[-1][0] >= a[1]:
            stack.pop()
        stack.append((a[1], clean_label(lab)))
        cur = " > ".join(x for _, x in stack)
        if not all(np.isnan(vals)):
            data.setdefault(cur, {})["value"] = pd.Series(vals, index=cols)
    return data


CE = {}
for kind, years, grp in (("deciles", range(2014, 2026), DEC), ("quintiles", range(2019, 2026), QUI)):
    for y in years:
        d = parse_ce(RAW / f"bls_ce/tables/{kind}/cu-income-{kind}-before-taxes-{y}.xlsx", ["all"] + grp)
        N = d[next(k for k in d if k.startswith("Number of consumer units"))]["value"] * 1e3
        CE[(kind, y)] = dict(d=d, N=N, tot=d[AAE]["mean"], se=d[AAE]["se"], grp=grp,
                             pip=d[AAE + " > Personal insurance and pensions"]["mean"],
                             cash=d[AAE + " > Cash contributions"]["mean"],
                             owned=d[AAE + " > Housing > Shelter > Owned dwellings"]["mean"],
                             rented=d[AAE + " > Housing > Shelter > Rented dwellings"]["mean"])


def fill_identity(N, m, grp):
    """Suppressed group cells from N_all m_all = sum_g N_g m_g: exact if one is missing; if several, only their
    sum is identified and it is spread in proportion to CU counts (used only where the split cannot matter much)."""
    m = m.copy()
    miss = [g for g in grp if not np.isfinite(m[g])]
    if miss:
        known = [g for g in grp if g not in miss]
        resid = N["all"] * m["all"] - (N[known] * m[known]).sum()
        for g in miss:
            m[g] = resid / N[miss].sum()
    return m, miss


def ce_mean(kind, y, concept="tot"):
    c = CE[(kind, y)]
    m = c["tot"].copy()
    parts = {"tot": [], "excl": ["pip", "cash"], "scf": ["pip", "cash", "owned", "rented"]}[concept]
    for p in parts:
        m = m - fill_identity(c["N"], c[p], c["grp"])[0]
    return m


def ce_share(kind, y, top, concept="tot"):
    c = CE[(kind, y)]
    m = ce_mean(kind, y, concept)
    A = c["N"][c["grp"]] * m[c["grp"]]
    return 100 * A[top].sum() / A.sum()


def ce_share_se(kind, y, top):
    """delta method, group means independent, BLS's published SEs of 'Average annual expenditures'"""
    c = CE[(kind, y)]
    g = c["grp"]
    A = c["N"][g] * c["tot"][g]
    T, s = A.sum(), A[top].sum() / A.sum()
    ind = pd.Series([1.0 if x in top else 0.0 for x in g], index=g)
    return 100 * np.sqrt((((c["N"][g] * (ind - s) / T) ** 2) * c["se"][g] ** 2).sum())


# %% A1. CE: release reproduction, top shares and their SEs (NOTES section 1)
c25 = CE[("quintiles", 2025)]
claim("CE 2025 all-CU mean expenditure and CU count reproduce the 2025 release ($81,905; 137,994k)", "81905 / 137994",
      f"{c25['tot']['all']:.0f} / {c25['N']['all'] / 1e3:.0f}", ok=(c25["tot"]["all"] == 81905 and c25["N"]["all"] == 137994e3))
claim_vec("CE quintile means 2019/2022/2023/2024/2025, $ (NOTES section 2 levels table, nominal columns)",
          [28672, 32612, 33776, 35046, 37935, 40472, 47657, 48923, 50054, 51405, 53045, 61950, 65487, 66900, 68983,
           71173, 81957, 87922, 89972, 92250, 121571, 140654, 150093, 150342, 159512],
          [CE[("quintiles", y)]["tot"][q] for q in QUI for y in (2019, 2022, 2023, 2024, 2025)], tol=0.5)

YRS = list(range(2019, 2026))
claim_vec("CE top 10% share of spending 2019-2025, % (income before taxes, CU count x mean)",
          [23.4, 22.3, 23.4, 22.9, 23.5, 22.9, 23.6], [ce_share("deciles", y, ["d10"]) for y in YRS], tol=0.0501)
claim_vec("CE top 20% share 2019-2025, % (Table 1101 quintiles)",
          [38.7, 37.3, 38.5, 38.5, 38.9, 38.5, 38.9], [ce_share("quintiles", y, ["q5"]) for y in YRS], tol=0.0501)
_t20d = [ce_share("deciles", y, ["d09", "d10"]) for y in range(2014, 2019)]
claim("CE top 20% 2014-2018 (deciles d09+d10) lies in 38.8-39.6%", "38.8-39.6", f"{min(_t20d):.2f}-{max(_t20d):.2f}",
      ok=(round(min(_t20d), 1) == 38.8 and round(max(_t20d), 1) == 39.6))
_dq = max(abs(ce_share("deciles", y, ["d09", "d10"]) - ce_share("quintiles", y, ["q5"])) for y in YRS)
claim("Judgment call 2: d09+d10 and q5 top-20 shares agree within 0.01 point in 2019-2025", 0.01, _dq, ok=_dq <= 0.01)

# published aggregate-share tables (Table 1110/1101 'shares of annual aggregate expenditures')
_agg_dev = []
for kind, top in (("deciles", "Highest"), ("quintiles", "Highest")):
    for y in YRS:
        rows = sheet_rows(next(iter(read_xlsx(RAW / f"bls_ce/tables/aggshare/cu-income-{kind}-before-taxes-{y}.xlsx").values())))
        hdr_i = next(i for i, r in enumerate(rows) if r and r[0] == "Item")
        row = next(r for r in rows[hdr_i:] if r and isinstance(r[0], str) and r[0].strip().startswith("Annual aggregate expenditures"))
        pub = float(row[-1])
        mine = ce_share(kind, y, ["d10"] if kind == "deciles" else ["q5"])
        _agg_dev.append(abs(pub - mine))
claim("Section 1: published aggregate-share tables agree with CU count x mean within 0.08 point (top 10%, top 20%)",
      0.08, max(_agg_dev), ok=max(_agg_dev) <= 0.0801, note="14 table-years, raw aggshare workbooks")

_ch10 = ce_share("deciles", 2025, ["d10"]) - ce_share("deciles", 2022, ["d10"])
_se10 = np.hypot(ce_share_se("deciles", 2025, ["d10"]), ce_share_se("deciles", 2022, ["d10"]))
_ch20 = ce_share("quintiles", 2025, ["q5"]) - ce_share("quintiles", 2022, ["q5"])
_se20 = np.hypot(ce_share_se("quintiles", 2025, ["q5"]), ce_share_se("quintiles", 2022, ["q5"]))
claim("CE top 10% change 2022->2025, pts", 0.8, _ch10, tol=0.0501)
claim("CE top 10% approx. SE of the change, pts (delta method, BRR SEs; Fay's BRR in 2025)", 0.68, _se10, tol=0.0051)
claim("CE top 20% change 2022->2025, pts", 0.3, _ch20, tol=0.0501)
claim("CE top 20% approx. SE of the change, pts", 0.63, _se20, tol=0.0051)
_lv = [ce_share_se("quintiles", y, ["q5"]) for y in YRS]
claim("Evidence table: CE top-20 share 'approx. SE 0.4-0.5'", "0.4-0.5", f"{min(_lv):.2f}-{max(_lv):.2f}",
      ok=(round(min(_lv), 1) >= 0.3 and round(max(_lv), 1) <= 0.5))

claim_vec("CE excl. pensions/SS/contributions: top 20% 2019-2025, %", [36.1, 34.7, 35.5, 35.7, 36.1, 35.7, 36.3],
          [ce_share("quintiles", y, ["q5"], "excl") for y in YRS], tol=0.0501,
          note="2022 Q2 cash contributions suppressed: filled from the all-CU identity")
claim("CE excl. variant top 20% change 2022->2025, pts", 0.7,
      ce_share("quintiles", 2025, ["q5"], "excl") - ce_share("quintiles", 2022, ["q5"], "excl"), tol=0.0501)
claim_vec("CE SCF-like scope: top 10% 2019-2025, %", [21.8, 20.4, 21.7, 21.0, 22.0, 21.5, 22.3],
          [ce_share("deciles", y, ["d10"], "scf") for y in YRS], tol=0.0501,
          note="2022 d02/d03/d06 and 2023 d09 cash contributions suppressed: only their sum matters for d10's share")
claim_vec("CE SCF-like scope: top 20% 2019-2025, %", [36.7, 35.3, 36.4, 36.4, 37.1, 36.7, 37.3],
          [ce_share("quintiles", y, ["q5"], "scf") for y in YRS], tol=0.0651,
          note="the builder divides this variant by the all-CU count x mean, not the sum over groups the NOTES "
               "states for CE shares (2021: 36.353 vs 36.343, a rounding-edge 0.01)")
claim("CE SCF-like top 10% change 2022->2025 (+1.3) and top 20% (+0.9)", "1.3 / 0.9",
      f"{ce_share('deciles', 2025, ['d10'], 'scf') - ce_share('deciles', 2022, ['d10'], 'scf'):.2f} / "
      f"{ce_share('quintiles', 2025, ['q5'], 'scf') - ce_share('quintiles', 2022, ['q5'], 'scf'):.2f}",
      ok=(r1(ce_share('deciles', 2025, ['d10'], 'scf') - ce_share('deciles', 2022, ['d10'], 'scf')) == 1.3 and
          r1(ce_share('quintiles', 2025, ['q5'], 'scf') - ce_share('quintiles', 2022, ['q5'], 'scf')) == 0.9))
_agg = c25["N"]["all"] * c25["tot"]["all"] / 1e12
_aggscf = (c25["N"][QUI] * ce_mean("quintiles", 2025, "scf")[QUI]).sum() / 1e12
claim("CE 2025 aggregate expenditure $tn (11.30) and SCF-like scope (7.35)", "11.30 / 7.35", f"{_agg:.2f} / {_aggscf:.2f}",
      ok=(round(_agg, 2) == 11.30 and round(_aggscf, 2) == 7.35))
_pip5 = 100 * (c25["N"]["q5"] * c25["pip"]["q5"]) / (c25["N"][QUI] * c25["pip"][QUI]).sum()
claim("Top quintile's share of CE personal insurance and pensions, 2025 (55.5%)", 55.5, _pip5, tol=0.0501)

# %% A2. deflators: ISPCEPX (raw workbook) and the current-vintage PCE price index (raw flat files)
_isp_rows = sheet_rows(next(iter(read_xlsx(RAW / "bea/distribution/ispcepx/ispecpx_table.xlsx").values())))
ISP = pd.DataFrame(_isp_rows[1:], columns=_isp_rows[0]).dropna(subset=["Year"])
ISP["Year"] = ISP.Year.astype(int)
ISP = ISP.set_index("Year")
ZNIPA = zipfile.ZipFile(RAW / "bea/nipa/FlatFiles.zip")


def nipa(fname):
    df = pd.read_csv(io.BytesIO(ZNIPA.read(fname)), thousands=",", dtype={"Period": str})
    df.columns = ["code", "period", "value"]
    return df


NA, NM = nipa("nipadataA.txt"), nipa("nipadataM.txt")


def nipa_a(code):
    x = NA[NA.code == code]
    return pd.Series(x.value.values, index=x.period.astype(int))


def nipa_m(code):
    x = NM[NM.code == code]
    return pd.Series(x.value.values, index=x.period.values)


PCEPI = nipa_a("DPCERG")
CARRY = PCEPI[2025] / PCEPI[2024]
claim("Aggregate PCE price index 2024->2025, current vintage (+2.59%)", 2.59, 100 * (CARRY - 1), tol=0.0051)


def isp_label(g):
    if g.startswith("d"):
        k = int(g[1:])
        return f"ISPCEPX: {10 * (k - 1)}-{10 * k}%"
    k = int(g[1:])
    return f"ISPCEPX: {20 * (k - 1)}-{20 * k}%"


def P(g, y):
    lab = isp_label(g)
    return ISP.loc[y, lab] if y <= 2024 else ISP.loc[2024, lab] * CARRY


_inf = {q: 100 * (P(q, 2024) / P(q, 2019) - 1) for q in QUI}
claim("ISPCEPX 2019-2024: top quintile +19.9%, the others 19.1-19.5%", "19.9 / 19.1-19.5",
      f"{_inf['q5']:.2f} / {min(_inf[q] for q in B80Q):.2f}-{max(_inf[q] for q in B80Q):.2f}",
      ok=(r1(_inf["q5"]) == 19.9 and r1(min(_inf[q] for q in B80Q)) == 19.1 and r1(max(_inf[q] for q in B80Q)) == 19.5))


# %% A3. CE real growth by group, gaps and their SEs (NOTES section 2)
def agg_nom(kind, groups, y, concept="tot"):
    c = CE[(kind, y)]
    m = ce_mean(kind, y, concept)
    return sum(c["N"][g] * m[g] for g in groups)


def agg_real(kind, groups, y, concept="tot"):
    c = CE[(kind, y)]
    m = ce_mean(kind, y, concept)
    return sum(c["N"][g] * m[g] * P(g, 2024) / P(g, y) for g in groups)


def rel_var(kind, groups, y):
    """relative sampling variance of a (real or nominal) group aggregate; the deflator is a constant here"""
    c = CE[(kind, y)]
    var = sum((c["N"][g] * c["se"][g] * P(g, 2024) / P(g, y)) ** 2 for g in groups)
    return var / agg_real(kind, groups, y) ** 2


def growth(kind, groups, y0, y1, concept="tot", real=True):
    f = agg_real if real else agg_nom
    G = f(kind, groups, y1, concept) / f(kind, groups, y0, concept)
    se = G * np.sqrt(rel_var(kind, groups, y0) + rel_var(kind, groups, y1))   # SE of the growth actually reported
    return 100 * (G - 1), 100 * se


def mean_real_growth(kind, groups, y0, y1):
    n0 = sum(CE[(kind, y0)]["N"][g] for g in groups)
    n1 = sum(CE[(kind, y1)]["N"][g] for g in groups)
    return 100 * ((agg_real(kind, groups, y1) / n1) / (agg_real(kind, groups, y0) / n0) - 1)


# quintile levels table: real 2025 (2024 $), real mean and aggregate growth, excl. variant
NOTES_Q = {  # group: (2025 real, mean 22-25, agg 22-25, mean 23-25, agg 23-25, agg excl 22-25)
    "q1": (36977, 6.5, 10.1, 6.8, 11.0, 9.8), "q2": (50107, -1.2, 1.5, -0.1, 2.0, 2.9),
    "q3": (67241, 2.1, 6.2, 0.2, 2.9, 5.6), "q4": (89920, 3.2, 5.0, -0.2, 1.5, 5.3),
    "q5": (155484, 3.4, 6.3, 0.7, 3.1, 8.1), "b80": (60975, 2.3, 5.3, 0.7, 3.3, 5.6),
    "all": (79836, 2.7, 5.7, 0.7, 3.2, 6.5)}
_b, _m = [], []
for g, row in NOTES_Q.items():
    grp = {"b80": B80Q, "all": QUI}.get(g, [g])
    n25 = sum(CE[("quintiles", 2025)]["N"][x] for x in grp)
    mine = (agg_real("quintiles", grp, 2025) / n25, mean_real_growth("quintiles", grp, 2022, 2025),
            growth("quintiles", grp, 2022, 2025)[0], mean_real_growth("quintiles", grp, 2023, 2025),
            growth("quintiles", grp, 2023, 2025)[0], growth("quintiles", grp, 2022, 2025, "excl")[0])
    _b += [row[0] / 1000] + list(row[1:])
    _m += [mine[0] / 1000] + list(mine[1:])
claim_vec("Section 2 quintile table: 2025 real ($k, 2024 $) and real growth columns (Q1-Q5, bottom 80%, all CUs)",
          _b, _m, tol=0.0501, note="ISPCEPX of the same rank, 2025 carried by the aggregate PCE price index")
_b80n = [agg_nom("quintiles", B80Q, y) / sum(CE[("quintiles", y)]["N"][q] for q in B80Q) for y in (2019, 2022, 2023, 2024, 2025)]
claim_vec("Section 2: bottom-80% mean nominal $ 2019/2022/2023/2024/2025", [48350, 56045, 59070, 60496, 62555], _b80n, tol=0.5)

# headline gaps (the brief and the gaps table)
GAPS = {  # (kind, window): (top real, rest real, gap, SE, gap excl, Zandi)
    ("quintiles", (2019, 2025)): (10.7, 10.5, 0.2, 3.4, 0.3, 26.5), ("quintiles", (2019, 2022)): (4.2, 4.9, -0.8, 2.9, -2.1, 12.5),
    ("quintiles", (2022, 2025)): (6.3, 5.3, 1.0, 3.1, 2.5, 12.5), ("quintiles", (2023, 2025)): (3.1, 3.3, -0.2, 2.9, 0.6, 8.2),
    ("quintiles", (2024, 2025)): (4.5, 2.6, 1.9, 2.8, 3.0, 4.0), ("deciles", (2019, 2025)): (11.1, 10.4, 0.6, 4.8, 0.7, 26.5),
    ("deciles", (2022, 2025)): (8.6, 4.8, 3.8, 4.5, 6.1, 12.5), ("deciles", (2023, 2025)): (3.7, 3.1, 0.6, 4.2, 0.6, 8.2)}
MYGAP = {}
for (kind, (y0, y1)), row in GAPS.items():
    top, rest = (["q5"], B80Q) if kind == "quintiles" else (["d10"], DEC[:9])
    gt, st = growth(kind, top, y0, y1)
    gb, sb = growth(kind, rest, y0, y1)
    gtx, gbx = growth(kind, top, y0, y1, "excl")[0], growth(kind, rest, y0, y1, "excl")[0]
    # the builder's SE: the relative SE scaled by the NOMINAL growth factor, then applied to the real gap
    nt = growth(kind, top, y0, y1, real=False)[0]
    nb = growth(kind, rest, y0, y1, real=False)[0]
    se_nomfactor = np.hypot(st * (1 + nt / 100) / (1 + gt / 100), sb * (1 + nb / 100) / (1 + gb / 100))
    MYGAP[(kind, (y0, y1))] = dict(top=gt, rest=gb, gap=gt - gb, se=np.hypot(st, sb), gapx=gtx - gbx,
                                   zandi=100 * ((1 + ZANDI_TOP) ** (y1 - y0) - (1 + ZANDI_B80) ** (y1 - y0)),
                                   se_nom=se_nomfactor)
_b, _m = [], []
for k, row in GAPS.items():
    g = MYGAP[k]
    _b += [row[0], row[1], row[2], row[4], row[5]]
    _m += [g["top"], g["rest"], g["gap"], g["gapx"], g["zandi"]]
claim_vec("Section 2 gaps table: top/rest real growth, gap, gap excl. pensions/contrib., Zandi's 1.04^T-1 (8 rows)",
          _b, _m, tol=0.0501)
_g = MYGAP[("quintiles", (2022, 2025))]
claim("Brief 2: CE real 2022->2025: top fifth +6.3%, bottom 80% +5.3%, gap +1.0 (excl. +2.5; 2023->2025 -0.2)",
      "6.3 / 5.3 / +1.0 / +2.5 / -0.2",
      f"{_g['top']:.2f} / {_g['rest']:.2f} / {_g['gap']:+.2f} / {_g['gapx']:+.2f} / {MYGAP[('quintiles', (2023, 2025))]['gap']:+.2f}",
      ok=(r1(_g["top"]) == 6.3 and r1(_g["rest"]) == 5.3 and r1(_g["gap"]) == 1.0 and r1(_g["gapx"]) == 2.5
          and r1(MYGAP[("quintiles", (2023, 2025))]["gap"]) == -0.2))
claim("Brief 2 / evidence table: approx. SE of the 2022->2025 top20-bottom80 real gap, pts", 3.1, _g["se"], tol=0.051,
      note=f"BAD: the builder scales the relative SE by the NOMINAL growth factor (1+g_nom); for a real gap the factor is "
           f"(1+g_real). Reproducing its error gives {_g['se_nom']:.2f}. Conservative (SE too large), conclusions unchanged; "
           f"Zandi's +12.5 is {(12.4864 - _g['gap']) / _g['se']:.1f} SEs from the CE gap, not 3.7")
_g10 = MYGAP[("deciles", (2022, 2025))]
claim("Brief 2: top tenth vs bottom 90%, 2022->2025: gap +3.8, SE 4.5", "+3.8 (SE 4.5)", f"{_g10['gap']:+.2f} (SE {_g10['se']:.2f})",
      ok=(r1(_g10["gap"]) == 3.8 and abs(_g10["se"] - 4.5) <= 0.051),
      note=f"gap OK; SE BAD for the same nominal-factor slip (builder's formula reproduces {_g10['se_nom']:.2f})")
claim_vec("Gaps table SE column (8 rows, pts) against SEs of the REAL growth actually tabulated",
          [r[3] for r in GAPS.values()], [MYGAP[k]["se"] for k in GAPS], tol=0.051,
          note="builder's formula reproduced to "
               f"{max(abs(MYGAP[k]['se_nom'] - GAPS[k][3]) for k in GAPS):.2f} by using (1+g_nom); overstatement 4-25%")

# decile table: nominal $ and growth, plus SE columns
NOTES_D = {  # 2022 $, 2025 $, mean 22-25, agg 22-25, SE 22-25, mean 23-25, agg 23-25, SE 23-25
    "d01": (31039, 35986, 6.1, 9.4, 6.3, 7.3, 12.5, 6.5), "d02": (34192, 39875, 6.8, 10.7, 4.2, 6.5, 9.6, 4.0),
    "d03": (44698, 46003, -5.7, -2.4, 7.2, -4.4, -3.1, 3.8), "d04": (50578, 56794, 2.9, 4.7, 3.6, 3.5, 6.5, 3.6),
    "d05": (57057, 65312, 4.9, 9.0, 3.7, 1.9, 4.4, 3.6), "d06": (66831, 72639, -0.3, 3.8, 3.4, -1.4, 1.7, 3.1),
    "d07": (76275, 86767, 4.4, 5.3, 4.1, 2.9, 4.4, 3.7), "d08": (87675, 97689, 2.1, 4.7, 3.2, -2.8, -1.0, 2.8),
    "d09": (114182, 125226, 0.4, 2.9, 3.3, -0.2, 2.1, 3.4), "d10": (167200, 193649, 5.4, 8.6, 4.3, 1.4, 3.7, 4.0),
    "b90": (62512, 69494, 1.9, 4.8, 1.4, 0.5, 3.1, 1.3)}
_b, _m, _bs, _ms = [], [], [], []
for g, row in NOTES_D.items():
    grp = DEC[:9] if g == "b90" else [g]
    n22 = sum(CE[("deciles", 2022)]["N"][x] for x in grp)
    n25 = sum(CE[("deciles", 2025)]["N"][x] for x in grp)
    a, sa = growth("deciles", grp, 2022, 2025)
    b, sb = growth("deciles", grp, 2023, 2025)
    _b += [row[0] / 1e3, row[1] / 1e3, row[2], row[3], row[5], row[6]]
    _m += [agg_nom("deciles", grp, 2022) / n22 / 1e3, agg_nom("deciles", grp, 2025) / n25 / 1e3,
           mean_real_growth("deciles", grp, 2022, 2025), a, mean_real_growth("deciles", grp, 2023, 2025), b]
    _bs += [row[4], row[7]]
    _ms += [sa, sb]
claim_vec("Section 2 decile table: nominal means ($k) and real growth columns (D01-D10, bottom 90%)", _b, _m, tol=0.0501)
claim_vec("Section 2 decile table: approx. SE columns, pts", _bs, _ms, tol=0.051,
          note="same nominal-factor slip as the gaps table (e.g. D01 2022-2025 6.3 vs 5.8)")

# %% A4. Zandi's implied top-20 share (NOTES section 2)
ZS = {2022: (38.5, 41.4, 41.5, 2.6, 0.63, 38.5, 36.3), 2023: (38.9, 40.7, 40.8, 1.9, 0.63, 38.0, 36.3)}
for base, row in ZS.items():
    T = 2025 - base
    s0 = agg_nom("quintiles", ["q5"], base) / agg_nom("quintiles", QUI, base)
    s25 = agg_nom("quintiles", ["q5"], 2025) / agg_nom("quintiles", QUI, 2025)
    z = (1 + ZANDI_TOP) ** T
    pt = P("q5", 2025) / P("q5", base)
    pb = (agg_nom("quintiles", B80Q, 2025) / agg_nom("quintiles", B80Q, base)) / \
         (agg_real("quintiles", B80Q, 2025) / agg_real("quintiles", B80Q, base))     # implicit deflator of the b80 aggregate
    real = s0 * z / (s0 * z + (1 - s0))
    nom = s0 * z * pt / (s0 * z * pt + (1 - s0) * pb)
    se = np.hypot(ce_share_se("quintiles", base, ["q5"]), ce_share_se("quintiles", 2025, ["q5"]))
    s0x = agg_nom("quintiles", ["q5"], base, "excl") / agg_nom("quintiles", QUI, base, "excl")
    s25x = agg_nom("quintiles", ["q5"], 2025, "excl") / agg_nom("quintiles", QUI, 2025, "excl")
    nomx = s0x * z * pt / (s0x * z * pt + (1 - s0x) * pb)
    claim_vec(f"Zandi-implied top-20 share from {base}: base, real, nominal, minus observed, SE, excl. Zandi/observed",
              list(row), [100 * s0, 100 * real, 100 * nom, 100 * (nom - s25), se, 100 * nomx, 100 * s25x], tol=0.0501)
claim("Brief 1: Zandi's 41.5% is 'about four standard errors of the change' above the observed 38.9%", "about 4",
      (41.4858 - 38.8791) / np.hypot(ce_share_se("quintiles", 2022, ["q5"]), ce_share_se("quintiles", 2025, ["q5"])),
      ok=True, note="4.2 SE; with the 2023 base (closer to Zandi's mid-2023 to mid-2026 window) 3.1 SE")

# %% A5. CE budget composition, Q1 and Q5, 2022 -> 2025 (28 items)
ITEMS = [("Food at home", ["Food > Food at home"]), ("Food away from home", ["Food > Food away from home"]),
         ("Alcoholic beverages", ["Alcoholic beverages"]), ("Owned dwellings", ["Housing > Shelter > Owned dwellings"]),
         ("Rented dwellings", ["Housing > Shelter > Rented dwellings"]), ("Other lodging", ["Housing > Shelter > Other lodging"]),
         ("Utilities", ["Housing > Utilities, fuels, and public services"]),
         ("Household operations", ["Housing > Household operations"]), ("Housekeeping supplies", ["Housing > Housekeeping supplies"]),
         ("Furnishings", ["Housing > Household furnishings and equipment"]), ("Apparel", ["Apparel and services"]),
         ("Vehicle purchases", ["Transportation > Vehicle purchases (net outlay)"]),
         ("Gasoline", ["Transportation > Gasoline, other fuels, and motor oil", "Transportation > Gasoline and other fuels"]),
         ("Other vehicle expenses", ["Transportation > Other vehicle expenses"]),
         ("Public transport", ["Transportation > Public and other transportation"]),
         ("Health insurance", ["Healthcare > Health insurance"]), ("Medical services", ["Healthcare > Medical services"]),
         ("Drugs", ["Healthcare > Drugs"]), ("Medical supplies", ["Healthcare > Medical supplies"]),
         ("Entertainment", ["Entertainment"]), ("Personal care", ["Personal care products and services"]),
         ("Reading", ["Reading"]), ("Education", ["Education"]), ("Tobacco", ["Tobacco products and smoking supplies"]),
         ("Miscellaneous", ["Miscellaneous"]), ("Cash contributions", ["Cash contributions"]),
         ("Life insurance", ["Personal insurance and pensions > Life and other personal insurance"]),
         ("Pensions and SS", ["Personal insurance and pensions > Pensions and Social Security",
                              "Personal insurance and pensions > Retirement, pensions, and Social Security"])]


def composition(y):
    c = CE[("quintiles", y)]
    rows, filled = {}, []
    for nm, paths in ITEMS:
        p = next(AAE + " > " + x for x in paths if AAE + " > " + x in c["d"])
        v, miss = fill_identity(c["N"], c["d"][p]["mean"], QUI)
        filled += [(nm, g) for g in miss]
        rows[nm] = v
    return pd.DataFrame(rows).T, filled, c


C22, F22, _c22 = composition(2022)
C25, F25, _c25 = composition(2025)
claim("Composition: suppressed cells filled from the identity are drugs Q3 and cash contributions Q2 (2022 only)",
      "[('Drugs','q3'), ('Cash contributions','q2')]", str(F22 + F25),
      ok=(sorted(F22) == sorted([("Drugs", "q3"), ("Cash contributions", "q2")]) and not F25))
_dev = max(abs(C.sum()[QUI] - c["tot"][QUI]).max() for C, c in ((C22, _c22), (C25, _c25)))
claim("Composition: the 28 items add to the published totals within $4", 4, _dev, ok=_dev <= 4.0)
COMP_B = pd.read_csv(OUT / "direct_ce_groups.csv")
COMP_B = COMP_B[COMP_B.block == "composition"]
_b, _m = [], []
for g in ("q1", "q5"):
    s22, s25 = 100 * C22[g] / C22[g].sum(), 100 * C25[g] / C25[g].sum()
    gr = 100 * (C25[g] / C22[g] - 1)
    bb = COMP_B[COMP_B.group == g]
    for i, (nm, _) in enumerate(ITEMS):
        r = bb.iloc[i]
        _b += [r.share_start_pct, r.share_end_pct, r.change_share_pts, r.growth_nominal_pct]
        _m += [s22[nm], s25[nm], s25[nm] - s22[nm], gr[nm]]
claim_vec("Composition table, Q1 and Q5 x 28 items: shares 2022/2025, change, nominal growth (builder CSV)", _b, _m, tol=0.006)

# %% A6. the hidden top (NOTES section 2): needs SCF shares, computed in section G; deferred to G4

# %% A7. CE coverage facts from the BLS dPCE methods page (raw html)
_meth = (RAW / "bls_ce/dpce/pce-ce-distribution-methods.htm").read_text(encoding="utf-8", errors="replace")
_k = [m.start() for m in re.finditer("Table 3.1", _meth)][-1]
_row = None
for tr in re.findall(r"<tr.*?</tr>", _meth[_k:_k + 9000], re.S):
    cells = [html.unescape(re.sub(r"<[^>]+>", "", x)).strip() for x in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", tr, re.S)]
    if cells and cells[0].startswith("PCE less final consumption"):
        _row = [float(x) for x in cells[1:]]
claim("Caveats: CE covers 0.74-0.78 of comparable PCE (dPCE methods Table 3.1, 2019-2023)", "0.74-0.78",
      f"{min(_row):.2f}-{max(_row):.2f}", ok=(min(_row) == 0.74 and max(_row) == 0.78))
_fig_txt = re.sub(r"<[^>]*>|\s+", "", _meth[_meth.find("Figure 3.1: Shares of PCE within Equivalized PCE Deciles, 2019</span>"):][:6000])
_fig = re.search(r"90-100%(\d+)%(\d+)%(\d+)%(\d+)%", _fig_txt.replace("\\", ""))
claim("Section 1: Pareto adjustment supplies 9% of the top spending decile's PCE in 2019 (Figure 3.1)", 9,
      float(_fig.group(2)), tol=0)

# %% B. BLS distributional PCE (raw workbook, March 2025)
_dp = read_xlsx(RAW / "bls_ce/dpce/distributional-pce-2000-2023.xlsx")
_t1 = sheet_rows(_dp["table1data"])
T1 = pd.DataFrame(_t1[1:], columns=_t1[0]).dropna(subset=["year"])
T1 = T1[T1.lineno == 1].set_index(T1[T1.lineno == 1].year.astype(int))
_t2 = sheet_rows(_dp["Table 2"])
_t2h = _t2[2]
T2 = {int(r[0]): dict(zip(_t2h[2:], r[2:])) for r in _t2[3:] if isinstance(r[0], float)}
Y5 = [2019, 2020, 2021, 2022, 2023]
dp10 = [100 * T1.loc[y, "Decile10"] for y in Y5]
dp20 = [100 * T2[26][str(y)] for y in Y5]
dp1 = [100 * T2[28][str(y)] for y in Y5]
claim_vec("dPCE top 10% of PCE 2019-2023 (T1 line 1, decile 10)", [26.1, 25.0, 26.1, 26.4, 25.7], dp10, tol=0.0501)
claim_vec("dPCE top 20% 2019-2023 (T2 line 26, share of total PCE)", [39.8, 38.3, 39.7, 40.0, 39.5], dp20, tol=0.0501)
_d1210 = max(abs(100 * (T1.loc[y, "Decile9"] + T1.loc[y, "Decile10"]) - 100 * T2[26][str(y)]) for y in Y5)
claim("dPCE: T1 deciles 9+10 equal T2 line 26 (so 'top 20%' is a share of actual PCE)", 0.01, _d1210, ok=_d1210 <= 0.011)
claim_vec("dPCE top 1% 2019-2023 (T2 line 28, share of unequivalized PCE)", [6.9, 6.5, 6.8, 7.5, 6.6], dp1, tol=0.0501,
          note=f"line 28 is the right concept; line 11 (share of equivalized PCE) would give {100 * T2[11]['2023']:.1f} in 2023")
claim("dPCE changes 2022->2023: top 10% -0.6, top 20% -0.5, top 1% -0.9", "-0.6 / -0.5 / -0.9",
      f"{dp10[4] - dp10[3]:.2f} / {dp20[4] - dp20[3]:.2f} / {dp1[4] - dp1[3]:.2f}",
      ok=(r1(dp10[4] - dp10[3]) == -0.6 and r1(dp20[4] - dp20[3]) == -0.5 and r1(dp1[4] - dp1[3]) == -0.9))

# %% C. BEA-BLS joint distribution (raw workbook)
_jw = read_xlsx(RAW / "bea/distribution/joint_dpi_pce/joint_dist_summary.xlsx")
_js = sheet_rows(_jw["shares of NIPA totals"], 6)
J = pd.DataFrame(_js[1:], columns=["year", "ranking", "series", "line", "q", "value"]).dropna(subset=["year"])
J["year"] = J.year.astype(int)
_sr = sheet_rows(_jw["savings rates"])
SRP = pd.DataFrame(_sr[1:], columns=_sr[0]).dropna(subset=["Year"]).set_index("Year")
SRP.index = SRP.index.astype(int)
DL = ["0-10%", "10-20%", "20-30%", "30-40%", "40-50%", "50-60%", "60-70%", "70-80%", "80-90%", "90-100%"]


def jser(y, series):
    return J[(J.year == y) & (J.series == series)].set_index("q")["value"].astype(float)


def jrate(y, groups):
    s, d = jser(y, "Personal Saving"), jser(y, "Disposable Personal Income")
    return 100 * sum(s[g] for g in groups) * s["Total ($ Billions)"] / (sum(d[g] for g in groups) * d["Total ($ Billions)"])


def jpd(y, groups):
    p, d = jser(y, "Personal Consumption Expenditures"), jser(y, "Disposable Personal Income")
    return sum(p[g] for g in groups) * p["Total ($ Billions)"] / (sum(d[g] for g in groups) * d["Total ($ Billions)"])


_jp = {y: jser(y, "Personal Consumption Expenditures") for y in Y5}
claim_vec("Joint distribution: PCE shares of the top 10% / top 20% / top 1% by equivalized DPI, 2019-2023",
          [20.6, 19.6, 19.3, 20.4, 20.2, 34.3, 32.8, 32.8, 34.1, 33.9, 2.4, 2.4, 2.1, 2.3, 2.1],
          [100 * _jp[y]["90-100%"] for y in Y5] + [100 * (_jp[y]["80-90%"] + _jp[y]["90-100%"]) for y in Y5] +
          [100 * _jp[y]["Top 1%"] for y in Y5], tol=0.0501)
claim("Brief 1: dPCE and the joint distribution both put the top's share slightly lower in 2023 than in 2022",
      "lower in both", f"dPCE top20 {dp20[3]:.2f} -> {dp20[4]:.2f}; joint top20 {100 * (_jp[2022]['80-90%'] + _jp[2022]['90-100%']):.1f} -> "
                       f"{100 * (_jp[2023]['80-90%'] + _jp[2023]['90-100%']):.1f}",
      ok=(dp20[4] < dp20[3] and (_jp[2023]["80-90%"] + _jp[2023]["90-100%"]) < (_jp[2022]["80-90%"] + _jp[2022]["90-100%"])))
# saving-rate table: deciles and top groups as published, bottom 80% and all from shares
NOTES_SR = {"0-10%": (-126.2, -112.8, -101.5, -144.9, -134.2, 2.17, 2.29), "10-20%": (-48.7, -32.5, -38.2, -54.0, -50.4, 1.46, 1.44),
            "20-30%": (-35.4, -19.4, -26.2, -39.2, -35.8, 1.32, 1.32), "30-40%": (-26.5, -12.4, -17.4, -29.5, -27.8, 1.22, 1.22),
            "40-50%": (-16.9, -4.7, -10.8, -20.9, -21.6, 1.13, 1.17), "50-60%": (-10.0, 0.6, -5.5, -15.2, -16.0, 1.05, 1.12),
            "60-70%": (-3.6, 4.8, 1.0, -9.4, -8.0, 1.00, 1.04), "70-80%": (1.8, 11.9, 7.0, -3.5, -1.3, 0.94, 0.97),
            "80-90%": (7.6, 19.2, 11.2, 1.9, 5.0, 0.89, 0.91), "90-100%": (45.6, 50.1, 49.3, 44.3, 46.6, 0.52, 0.52),
            "80-100%": (34.9, 41.0, 38.4, 32.5, 35.1, 0.63, 0.62), "Top 5%": (58.9, 61.5, 62.6, 59.0, 61.4, 0.40, 0.37),
            "Top 1%": (83.0, 83.8, 85.8, 83.9, 85.7, 0.16, 0.14)}
_b, _m = [], []
for g, row in NOTES_SR.items():
    groups = DL[8:] if g == "80-100%" else [g]
    _b += list(row[:5]) + [row[5], row[6]]
    _m += [100 * SRP.loc[y, g] for y in Y5] + [jpd(2019, groups), jpd(2023, groups)]
claim_vec("Section 3 saving-rate table: published rates (deciles, top 20/5/1%) and PCE/DPI from shares", _b, _m, tol=0.0051 + 0.05)
_rec = max(abs(jrate(y, [g]) - 100 * SRP.loc[y, g]) for y in Y5 for g in DL[1:] + ["Top 5%", "Top 1%"])
claim("Check B5: share-based saving rates reproduce the published ones within the rounding of 3-decimal shares (D2-D10, top 5/1%)",
      "within rounding", f"max |diff| {_rec:.2f} pts", ok=_rec <= 2.0,
      note=f"D1 differs by up to {max(abs(jrate(y, ['0-10%']) - 100 * SRP.loc[y, '0-10%']) for y in Y5):.1f} pts (tiny DPI share)")
claim_vec("Bottom 80% saving rate from shares 2019-2023 and PCE/DPI 2019/2023", [-19.2, -7.5, -12.4, -24.5, -23.1, 1.15, 1.18],
          [jrate(y, DL[:8]) for y in Y5] + [jpd(2019, DL[:8]), jpd(2023, DL[:8])], tol=0.0501)
claim_vec("All households from shares: saving rate 2019-2023, PCE/DPI 2019/2023", [7.3, 15.3, 11.6, 3.3, 5.6, 0.89, 0.91],
          [jrate(y, DL) for y in Y5] + [jpd(2019, DL), jpd(2023, DL)], tol=0.0501)


def decomp(y0, y1):
    """change in the aggregate rate = within bottom 80 + within top 20 + DPI-share composition (midpoint weights)"""
    out = []
    for y in (y0, y1):
        d = jser(y, "Disposable Personal Income")
        wB = sum(d[g] for g in DL[:8]) / sum(d[g] for g in DL)
        out.append((wB, 1 - wB, jrate(y, DL[:8]), jrate(y, DL[8:])))
    (wb0, wt0, rb0, rt0), (wb1, wt1, rb1, rt1) = out
    return 0.5 * (wb0 + wb1) * (rb1 - rb0), 0.5 * (wt0 + wt1) * (rt1 - rt0), (wt1 - wt0) * 0.5 * (rt0 + rt1 - rb0 - rb1)


_wb, _wt, _cp = decomp(2019, 2023)
claim("Section 3: the 2019->2023 fall in the aggregate rate (7.3 -> 5.6) 'came from the bottom 80%'", "bottom 80%",
      f"within b80 {_wb:+.2f}, within top20 {_wt:+.2f}, composition {_cp:+.2f} pts", ok=(_wb < -1.5 and abs(_wt) < 0.3))
_dpi23 = jser(2023, "Disposable Personal Income")["Total ($ Billions)"]
_pce23 = jser(2023, "Personal Consumption Expenditures")["Total ($ Billions)"]
claim("Vintage: joint-file 2023 DPI $59bn below, PCE $61bn above the current NIPA vintage", "-59 / +61",
      f"{_dpi23 - nipa_a('A067RC')[2023] / 1e3:+.0f} / {_pce23 - nipa_a('DPCERC')[2023] / 1e3:+.0f}",
      ok=(round(_dpi23 - nipa_a("A067RC")[2023] / 1e3) == -59 and round(_pce23 - nipa_a("DPCERC")[2023] / 1e3) == 61))

# %% D. BEA distribution of personal income (raw summary-file.csv and the nowcast table in the html page)
SF = pd.read_csv(RAW / "bea/distribution/national/summary-file.csv", dtype=str)
SF.columns = ["year", "ranking", "concept", "line", "q", "value"]
QL = ["0-20%", "20-40%", "40-60%", "60-80%", "80-100%"]


def sf_share(concept, ranking, y, q):
    x = SF[(SF.year == str(y)) & (SF.concept == concept) & (SF.ranking == ranking) & (SF.q == q)].value
    return float(x.iloc[0])


def sf_total(concept, y):
    x = SF[(SF.year == str(y)) & (SF.concept == concept) & SF.ranking.isna() & SF.q.str.startswith("Total")].value
    return float(x.iloc[0])


_page = (RAW / "bea/distribution/distribution-of-personal-income.html").read_text(encoding="utf-8", errors="replace")
_tab = re.search(r"<table.*?Nowcast.*?</table>", _page, re.S).group(0)
_cells = [html.unescape(re.sub(r"<[^>]+>", "", x)).strip() for x in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", _tab, re.S)]
NOW = {}
for i, cc in enumerate(_cells):
    mm = re.match(r"Q(\d): ", cc)
    if mm:
        NOW[int(mm.group(1))] = (float(_cells[i + 1]), float(_cells[i + 2]), float(_cells[i + 3].rstrip("%")))
claim("Nowcast table read from the html: 2025 PI shares 5.2/9.6/13.4/19.1/52.7, growth 4.1/5.8/5.0/5.4/4.6",
      "5.2/9.6/13.4/19.1/52.7; 4.1/5.8/5.0/5.4/4.6",
      "/".join(f"{NOW[k][1]:g}" for k in range(1, 6)) + "; " + "/".join(f"{NOW[k][2]:g}" for k in range(1, 6)),
      ok=([NOW[k][1] for k in range(1, 6)] == [5.2, 9.6, 13.4, 19.1, 52.7] and
          [NOW[k][2] for k in range(1, 6)] == [4.1, 5.8, 5.0, 5.4, 4.6]))
RK_PI, RK_DPI = "Equivalized Personal Income", "Equivalized Disposable Personal Income"


def isp_q(k, y):
    return P(f"q{k}", y)


def inc_levels(concept, ranking, years):
    lv = {}
    for y in years:
        if y == 2025:
            lv[y] = {k: lv[2024][k] * (1 + NOW[k][2] / 100) for k in range(1, 6)}
        else:
            T = sf_total(concept, y)
            lv[y] = {k: sf_share(concept, ranking, y, QL[k - 1]) * T for k in range(1, 6)}
    return lv


def inc_growth(lv, ks, y0, y1, real=True):
    f = (lambda k, y: isp_q(k, 2024) / isp_q(k, y)) if real else (lambda k, y: 1.0)
    return 100 * (sum(lv[y1][k] * f(k, y1) for k in ks) / sum(lv[y0][k] * f(k, y0) for k in ks) - 1)


PI = inc_levels("Personal income", RK_PI, [2019, 2022, 2023, 2024, 2025])
NOTES_PI = {1: (15.7, 13.6, 4.5, 1.5, 4.1), 2: (14.9, 9.0, 5.1, 3.1, 5.8), 3: (13.0, 7.4, 5.4, 2.3, 5.0),
            4: (11.5, 8.1, 6.4, 2.7, 5.4), 5: (13.7, 7.3, 4.9, 2.0, 4.6), "b80": (13.0, 8.7, 5.7, 2.6, 5.2),
            "all": (13.4, 7.9, 5.3, 2.2, 4.9)}
_b, _m = [], []
for g, row in NOTES_PI.items():
    ks = {"b80": [1, 2, 3, 4], "all": [1, 2, 3, 4, 5]}.get(g, [g])
    _b += list(row)
    _m += [inc_growth(PI, ks, 2019, 2024), inc_growth(PI, ks, 2022, 2025), inc_growth(PI, ks, 2023, 2025),
           inc_growth(PI, ks, 2024, 2025), inc_growth(PI, ks, 2024, 2025, real=False)]
claim_vec("Section 3 PI table: real growth 2019-24, 2022-25, 2023-25, 2024-25 and nominal 2024-25 by quintile, b80, all",
          _b, _m, tol=0.0501, note="levels = 3-decimal shares x June-2026 totals; 2025 = 2024 x nowcast growth")
_b80alt = {y: (1 - sf_share("Personal income", RK_PI, y, "80-100%")) * sf_total("Personal income", y) for y in (2022, 2024)}
_b80alt[2025] = sum(PI[2025][k] for k in (1, 2, 3, 4)) * _b80alt[2024] / sum(PI[2024][k] for k in (1, 2, 3, 4))
_infl_b80 = (sum(PI[2022][k] for k in (1, 2, 3, 4)) / sum(PI[2022][k] * isp_q(k, 2024) / isp_q(k, 2022) for k in (1, 2, 3, 4)))
_g_alt = 100 * (_b80alt[2025] / CARRY / (_b80alt[2022] / _infl_b80) - 1)
claim("Brief 3: real PI 2022->2025: bottom 80% +8.7%, top 20% +7.3% (nominal 2024->2025: +5.2% vs +4.6%)",
      "8.7 / 7.3 (5.2 / 4.6)",
      f"{inc_growth(PI, [1, 2, 3, 4], 2022, 2025):.2f} / {inc_growth(PI, [5], 2022, 2025):.2f} "
      f"({inc_growth(PI, [1, 2, 3, 4], 2024, 2025, False):.2f} / {inc_growth(PI, [5], 2024, 2025, False):.2f})",
      ok=(r1(inc_growth(PI, [1, 2, 3, 4], 2022, 2025)) == 8.7 and r1(inc_growth(PI, [5], 2022, 2025)) == 7.3),
      note=f"rounding: with bottom 80% = 1 - top-20 share (2022 sum of quintiles is 0.999) it is {_g_alt:.1f}; sign survives")
# the concept the NOTES leaves out: disposable income (same file, 2000-2024, ranked by equivalized DPI)
DPI = inc_levels("Disposable personal income", RK_DPI, [2019, 2022, 2023, 2024])
_dt, _db = inc_growth(DPI, [5], 2022, 2024), inc_growth(DPI, [1, 2, 3, 4], 2022, 2024)
_dt3, _db3 = inc_growth(DPI, [5], 2023, 2024), inc_growth(DPI, [1, 2, 3, 4], 2023, 2024)
_pt, _pb = inc_growth(PI, [5], 2022, 2024), inc_growth(PI, [1, 2, 3, 4], 2022, 2024)
_tax = {y: (sf_share("Taxes", RK_DPI, y, "80-90%") + sf_share("Taxes", RK_DPI, y, "90-100%")) * sf_total("Taxes", y) for y in (2022, 2024)}
claim("Brief 3 / plain words: 'The income side has no K either' (PI, pre-tax, incl. in-kind transfers)",
      "no K", f"DPI 2022->2024 real: top20 {_dt:+.1f}% vs b80 {_db:+.1f}% (gap {_dt - _db:+.1f})", ok=False,
      note=f"material omission: BEA's DPI distribution (same summary file; the builder's own CSV carries it) shows the top fifth's "
           f"real disposable income outgrowing the bottom 80% by {_dt - _db:.1f} pts from 2022 (PI: {_pt:+.1f} vs {_pb:+.1f}); "
           f"top-two-decile taxes fell ${_tax[2022] - _tax[2024]:,.0f}bn from the top-heavy 2022 tax year. From 2023 the two match "
           f"({_dt3:+.1f} vs {_db3:+.1f}). Spending is paid from DPI and Zandi argued in DPI terms: say which concept, give both")
claim("Vintage: summary-file 2024 PI total $137bn below the current NIPA vintage", -137,
      sf_total("Personal income", 2024) - nipa_a("A065RC")[2024] / 1e3, tol=0.5)

# %% E. NIPA saving rate and the 2026 drawdown (raw flat files)
SRA, SRM = nipa_a("A072RC"), nipa_m("A072RC")
PCEM, SAVM, DPIM = nipa_m("DPCERC"), nipa_m("A071RC"), nipa_m("A067RC")
claim_vec("Saving rate, annual 2019-2025 (Table 2.1) and monthly 2026-01..09 (Table 2.6), % of DPI",
          [7.3, 15.3, 11.6, 3.5, 6.1, 6.3, 5.4, 5.6, 5.3, 5.1, 4.4, 4.4, 4.4, 4.5, 4.0, 3.8],
          [SRA[y] for y in range(2019, 2026)] + [SRM[f"2026M{m:02d}"] for m in range(1, 10)], tol=0.001)
_dsav = SAVM["2026M09"] - SAVM["2026M03"]
_dpce = PCEM["2026M09"] - PCEM["2026M03"]
claim("Mar->Sep 2026: the fall in personal saving equals 40% of the rise in PCE", 40, -100 * _dsav / _dpce, tol=0.5,
      note=f"saving {_dsav / 1e3:+,.0f}bn, PCE {_dpce / 1e3:+,.0f}bn (SAAR); an identity, not evidence of who drew down")
_sr2324 = (SRA[2023] + SRA[2024]) / 2
_sr26q3 = np.mean([SRM[f"2026M{m:02d}"] for m in (7, 8, 9)])
claim("Saving rate 2023-24 average 6.20, 2026Q3 average 4.10, change -2.10", "6.20 / 4.10 / -2.10",
      f"{_sr2324:.2f} / {_sr26q3:.2f} / {_sr26q3 - _sr2324:.2f}", ok=(abs(_sr2324 - 6.2) < 1e-9 and abs(_sr26q3 - 4.1) < 1e-9))
_pce25 = nipa_a("DPCERC")[2025] / 1e6
claim("Section 1 table: PCE 2025 (NIPA Table 2.1) $20.87tn", 20.87, _pce25, tol=0.005)
_pce_ref = PCEM.loc["2024M07":"2025M06"].mean() / 1e6
claim("Evidence table (SCF row): 'aggregate $6.6tn against $20.5tn of PCE'", 20.5, _pce25, tol=0.05,
      note=f"hard-coded string in the builder; calendar 2025 PCE is {_pce25:.2f}tn (as its own section 1 table says); the 12 "
           f"months to 2025-06 average {_pce_ref:.2f}tn. Use one figure and state its period")

# %% F. DFA by income group and the Z.1 revaluation share (raw zips)
ZD = zipfile.ZipFile(RAW / "fed/dfa/dfa.zip")
DFA = pd.read_csv(io.BytesIO(ZD.read("dfa-income-levels.csv")))
DFAD = pd.read_csv(io.BytesIO(ZD.read("dfa-income-levels-detail.csv")))
DFAW = pd.read_csv(io.BytesIO(ZD.read("dfa-networth-levels.csv")))
GI = ["pct00to20", "pct20to40", "pct40to60", "pct60to80", "pct80to99", "pct99to100"]
T20, B80I = GI[4:], GI[:4]
EQ = "Corporate equities and mutual fund shares"


def dfa(date, cat, df=DFA):
    return df[df.Date == date].set_index("Category")[cat].astype(float) / 1e3       # $bn


_lb = pd.read_csv(OUT / "direct_dfa_wealth.csv")
_lvb = _lb[_lb.block == "levels"]
_b, _m = [], []
for cat in ("Net worth", EQ, "Real estate", "Consumer credit"):
    for date in ("2019:Q4", "2022:Q3", "2026:Q2"):
        x = dfa(date, cat)
        for g, grp in [(g, [g]) for g in GI] + [("top20", T20), ("bottom80", B80I), ("all", GI)]:
            r = _lvb[(_lvb.category == cat) & (_lvb.date == date.replace(":", "")) & (_lvb.group == g)]
            if len(r):
                _b.append(float(r.level_bn.iloc[0]))
                _m.append(x[grp].sum())
claim_vec("Section 4 levels table: DFA $bn by income group, 4 items x 3 quarters (builder CSV)", _b, _m, tol=0.01)
_e0, _e1 = dfa("2022:Q3", EQ), dfa("2026:Q2", EQ)
_gain = _e1 - _e0
claim("Equity holdings rose $32.9tn (+103%), 2022Q3->2026Q2", "32.9tn / +103%",
      f"{_gain[GI].sum() / 1e3:.1f}tn / {100 * (_e1[GI].sum() / _e0[GI].sum() - 1):+.0f}%",
      ok=(round(_gain[GI].sum() / 1e3, 1) == 32.9 and round(100 * (_e1[GI].sum() / _e0[GI].sum() - 1)) == 103))
claim_vec("Shares of the equity gain: top 20% 88.1, 80-99 45.5, 99-100 42.5, bottom 80% 11.9 (%), bottom-80 base +90%",
          [88.1, 45.5, 42.5, 11.9, 90], [100 * _gain[T20].sum() / _gain[GI].sum(), 100 * _gain["pct80to99"] / _gain[GI].sum(),
                                        100 * _gain["pct99to100"] / _gain[GI].sum(), 100 * _gain[B80I].sum() / _gain[GI].sum(),
                                        100 * (_e1[B80I].sum() / _e0[B80I].sum() - 1)], tol=0.501)
_hh = DFAD[DFAD.Date == "2026:Q2"].set_index("Category")["Household count"].astype(float)
claim("Per household 2026Q2: top-1% net worth $34.6m, top-20% equities $2.09m", "34,635k / 2,085k",
      f"{dfa('2026:Q2', 'Net worth')['pct99to100'] * 1e6 / _hh['pct99to100']:,.0f}k / {_e1[T20].sum() * 1e6 / _hh[T20].sum():,.0f}k",
      ok=(round(dfa("2026:Q2", "Net worth")["pct99to100"] * 1e6 / _hh["pct99to100"]) == 34635 and
          round(_e1[T20].sum() * 1e6 / _hh[T20].sum()) == 2085))
ZZ = zipfile.ZipFile(RAW / "fed/z1/z1_csv_files.zip")
Z1B = pd.read_csv(io.BytesIO(ZZ.read("csv/S1M_b.csv")), na_values=["ND"]).set_index("date")
Z1R = pd.read_csv(io.BytesIO(ZZ.read("csv/S1M_r.csv")), na_values=["ND"]).set_index("date")
LEVC = ["LM153064105.Q", "LM153064205.Q", "LM153064705.Q", "LM153064505.Q"]
REVC = ["FR153064105.Q", "FR153064205.Q", "FR153064705.Q", "FR153064505.Q"]
QS = list(Z1B.index)


def z1_window(a, b):
    l0, l1 = Z1B.loc[a, LEVC].sum() / 1e3, Z1B.loc[b, LEVC].sum() / 1e3
    rv = Z1R.loc[QS[QS.index(a) + 1:QS.index(b) + 1], REVC].sum().sum() / 1e3
    return l0, l1, l1 - l0, rv, rv / (l1 - l0)


claim_vec("Z.1 revaluation table (S1M: equities, MF, hedge and private-debt funds): levels, change, revaluations, share",
          [35139, 69167, 34028, 31535, 0.927, 35139, 54629, 19490, 18505, 0.949, 31124, 69167, 38043, 33354, 0.877],
          list(z1_window("2022:Q3", "2026:Q2")) + list(z1_window("2022:Q3", "2025:Q2")) + list(z1_window("2019:Q4", "2026:Q2")),
          tol=0.6)

# %% F2. the wealth-effect bound (needs SCF 2025 spending shares by the DFA's income groups: computed here)
ZS25 = zipfile.ZipFile(RAW / "fed/scf/scfp2025excel.zip")
S = pd.read_csv(io.BytesIO(ZS25.read(ZS25.namelist()[0])))
ZS22 = zipfile.ZipFile(RAW / "fed/scf/scfp2022excel.zip")
S22 = pd.read_csv(io.BytesIO(ZS22.read(ZS22.namelist()[0])))


def pctl_cat(df, var, points):
    """The SCF macro's %PCTL rule: sort by var then Y1 over all implicate records pooled; cumulative WGT including
    the record itself; category k = largest k with cum/total >= points[k-1]/100."""
    d = df[[var, "Y1", "WGT"]].sort_values([var, "Y1"], kind="mergesort")
    cum = (d.WGT.cumsum() / d.WGT.sum()).values
    cat = np.ones(len(d), dtype=int)
    for k, p in enumerate(points[1:], start=2):
        cat[cum >= p / 100.0 - 1e-12] = k
    return pd.Series(cat, index=d.index).reindex(df.index).values


P12 = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 99]
SC = {}
for var, pub in (("INCOME", "INCPCTLECAT"), ("NORMINC", "NINCPCTLECAT"), ("NETWORTH", "NWPCTLECAT")):
    SC[var] = pctl_cat(S, var, P12)
    claim(f"SCF 2025: my %PCTL rebuild of the 12 {var} groups equals the published {pub}", "100%",
          f"{100 * np.mean(SC[var] == S[pub].values):.3f}%", ok=bool(np.all(SC[var] == S[pub].values)))
W = S.WGT.values.astype(float)
claim("SCF 2025 families = WGT summed over all implicate records (Bulletin 135.0m)", 135.0, W.sum() / 1e6, tol=0.05,
      note="WGT = X42001/5 in the extract, so the sum over all five implicates is the family count")
CDFA = pctl_cat(S, "INCOME", [0, 20, 40, 60, 80, 99])
SP = S.TOTSPENDNH.values.astype(float)
SCF_SH = pd.Series([(W[CDFA == k] * SP[CDFA == k]).sum() / (W * SP).sum() for k in range(1, 7)], index=GI)
_jp23 = jser(2023, "Personal Consumption Expenditures")
BEA_SH = pd.Series({"pct00to20": _jp23[DL[0]] + _jp23[DL[1]], "pct20to40": _jp23[DL[2]] + _jp23[DL[3]],
                    "pct40to60": _jp23[DL[4]] + _jp23[DL[5]], "pct60to80": _jp23[DL[6]] + _jp23[DL[7]],
                    "pct80to99": _jp23[DL[8]] + _jp23[DL[9]] - _jp23["Top 1%"], "pct99to100": _jp23["Top 1%"]})
PCE_Q = {"2025:Q2": PCEM.loc[["2025M04", "2025M05", "2025M06"]].mean() / 1e3,
         "2026:Q2": PCEM.loc[["2026M04", "2026M05", "2026M06"]].mean() / 1e3}
_web = _lb[(_lb.block == "wealth_effect_bound") & (_lb.base == "equities (revaluation share applied)")]
_b, _m = [], []
WE = {}
for end in ("2025:Q2", "2026:Q2"):
    rs = z1_window("2022:Q3", end)[4]
    gain = (dfa(end, EQ) - dfa("2022:Q3", EQ)) * rs
    for dname, sh, key in (("SCF", SCF_SH, "SCF 2025"), ("BEA", BEA_SH, "BEA-BLS")):
        spend = PCE_Q[end] * sh
        for cw in (0.02, 0.035, 0.05):
            for g, grp in [(g, [g]) for g in GI] + [("top20", T20), ("bottom80", B80I), ("all", GI)]:
                mine = 100 * cw * gain[grp].sum() / spend[grp].sum()
                WE[(end, dname, cw, g)] = mine
                r = _web[(_web.window == "2022Q3->" + end.replace(":", "")) & _web.denominator.str.startswith(key)
                         & (_web.c_w == cw) & (_web.group == g)]
                _b.append(float(r.pct_of_group_spending.iloc[0]))
                _m.append(mine)
claim_vec("Section 4 wealth-effect bound: % of group spending, 2 windows x 2 denominators x 3 c_w x 9 groups (builder CSV)",
          _b, _m, tol=0.001)
NOTES_GAP = {("2025:Q2", "reval"): (3.2, 5.6, 7.9, 4.2, 7.3, 10.4), ("2025:Q2", "level"): (3.3, 5.9, 8.4, 4.4, 7.7, 10.9),
             ("2025:Q2", "nw"): (4.7, 8.3, 11.8, 6.4, 11.2, 16.0), ("2026:Q2", "reval"): (5.1, 9.0, 12.8, 6.7, 11.7, 16.7),
             ("2026:Q2", "level"): (5.5, 9.7, 13.8, 7.2, 12.6, 18.1), ("2026:Q2", "nw"): (7.4, 12.9, 18.4, 9.9, 17.4, 24.9)}
_b, _m = [], []
for (end, kind), row in NOTES_GAP.items():
    rs = z1_window("2022:Q3", end)[4]
    item = "Net worth" if kind == "nw" else EQ
    gain = (dfa(end, item) - dfa("2022:Q3", item)) * (rs if kind == "reval" else 1.0)
    for sh in (SCF_SH, BEA_SH):
        spend = PCE_Q[end] * sh
        for cw in (0.02, 0.035, 0.05):
            _m.append(100 * cw * (gain[T20].sum() / spend[T20].sum() - gain[B80I].sum() / spend[B80I].sum()))
    _b += list(row)
claim_vec("Section 4 implied top20-minus-bottom80 gaps (6 rows x 6), pts", _b, _m, tol=0.0501)
claim("Brief 4: the bound lifts the top fifth 3-8% by mid-2025 and 5-13% by mid-2026 (SCF denominators)", "3-8 / 5-13",
      f"{WE[('2025:Q2', 'SCF', 0.02, 'top20')] - WE[('2025:Q2', 'SCF', 0.02, 'bottom80')]:.1f}-"
      f"{WE[('2025:Q2', 'SCF', 0.05, 'top20')] - WE[('2025:Q2', 'SCF', 0.05, 'bottom80')]:.1f} / "
      f"{WE[('2026:Q2', 'SCF', 0.02, 'top20')] - WE[('2026:Q2', 'SCF', 0.02, 'bottom80')]:.1f}-"
      f"{WE[('2026:Q2', 'SCF', 0.05, 'top20')] - WE[('2026:Q2', 'SCF', 0.05, 'bottom80')]:.1f}", ok=True,
      note="arithmetic on an assumption; with the BEA-BLS denominators 4-10 and 7-17: the brief quotes only the lower set")
claim("Section 4: top 1% at 3.5 cents by 2025Q2: 20% of its spending (61% with BEA-BLS denominators)", "20 / 61",
      f"{WE[('2025:Q2', 'SCF', 0.035, 'pct99to100')]:.1f} / {WE[('2025:Q2', 'BEA', 0.035, 'pct99to100')]:.1f}",
      ok=(round(WE[("2025:Q2", "SCF", 0.035, "pct99to100")]) == 20 and round(WE[("2025:Q2", "BEA", 0.035, "pct99to100")]) == 61))
# saving cross-check
_eqall = DFA[DFA.Category.isin(GI)].groupby("Date")[EQ].sum() / 1e3
_avg = _eqall.loc[[f"{y}:Q{q}" for y in (2023, 2024) for q in (1, 2, 3, 4)]].mean()
_rs_full = z1_window("2022:Q3", "2026:Q2")[4]
_gx = (_eqall.loc["2026:Q2"] - _avg) * _rs_full
_dpi_q2 = DPIM.loc[["2026M04", "2026M05", "2026M06"]].mean() / 1e3
_alt = (_eqall.loc["2026:Q2"] - _avg) * z1_window("2024:Q2", "2026:Q2")[4]
claim_vec("Saving cross-check: DFA equity 2023-24 average $bn, revaluation gain to 2026Q2, % of DPI at 2/3.5/5 cents",
          [41196, 21726, 1.81, 3.17, 4.53], [_avg, _gx] + [100 * cw * _gx / _dpi_q2 for cw in (0.02, 0.035, 0.05)], tol=0.6,
          note=f"the revaluation share used is the 2022Q3-2026Q2 one; the 2024Q2-2026Q2 share gives {100 * 0.02 * _alt / _dpi_q2:.2f}/"
               f"{100 * 0.035 * _alt / _dpi_q2:.2f}/{100 * 0.05 * _alt / _dpi_q2:.2f}: immaterial")

# DFA by wealth: top 10% share of equities; top 20% by income
_tw = {d: dfa(d, EQ, DFAW) for d in ("2022:Q3", "2025:Q3", "2026:Q2")}
claim_vec("DFA equities: top 10% by WEALTH 87.0/87.8/88.0 and top 20% by INCOME 86.4/87.0/87.2 (2022Q3/2025Q3/2026Q2)",
          [87.0, 87.8, 88.0, 86.4, 87.0, 87.2],
          [100 * _tw[d][["Next9", "RemainingTop1", "TopPt1"]].sum() / _tw[d].sum() for d in _tw] +
          [100 * dfa(d, EQ)[T20].sum() / dfa(d, EQ)[GI].sum() for d in _tw], tol=0.0501)


# %% F3. SCF vs DFA concentration (SCF 2022 and 2025 raw extracts)
def scf_conc(df):
    c6 = pctl_cat(df, "INCOME", [0, 20, 40, 60, 80, 99])
    w = df.WGT.values.astype(float)
    out = {}
    for nm, x in (("STOCKS+NMMF", df.STOCKS + df.NMMF), ("EQUITY", df.EQUITY), ("DEQ", df.DEQ), ("NETWORTH", df.NETWORTH)):
        x = x.values.astype(float)
        out[nm] = [100 * (w[c6 == k] * x[c6 == k]).sum() / (w * x).sum() for k in range(1, 7)]
        for lab, pts_ in (("top10", [0, 90]), ("top20", [0, 80]), ("top1", [0, 99])):
            cc = pctl_cat(df, "INCOME", pts_)
            out[(nm, lab)] = 100 * (w[cc == 2] * x[cc == 2]).sum() / (w * x).sum()
    return out


CONC = {2022: scf_conc(S22), 2025: scf_conc(S)}
claim_vec("Concentration table: SCF shares by income group, STOCKS+NMMF / EQUITY / NETWORTH, 2022 and 2025",
          [2.1, 0.8, 3.4, 5.4, 50.8, 37.5, 1.7, 1.5, 4.7, 8.6, 55.1, 28.4, 3.7, 3.7, 7.8, 11.3, 47.9, 25.7,
           0.7, 1.3, 2.7, 8.0, 50.8, 36.4, 0.8, 1.7, 4.4, 10.8, 56.5, 25.7, 2.4, 4.1, 7.5, 13.0, 48.9, 24.0],
          [v for y in (2022, 2025) for nm in ("STOCKS+NMMF", "EQUITY", "NETWORTH") for v in CONC[y][nm]], tol=0.0501)
claim_vec("Concentration table: DFA equities (net worth) shares by income group, 2022Q3 and 2025Q3",
          [1.9, 1.1, 4.0, 6.6, 49.8, 36.6, 3.1, 4.8, 8.9, 13.8, 47.2, 22.3, 1.6, 1.0, 3.5, 6.9, 48.1, 39.0, 2.9, 4.2, 7.8, 13.3, 47.4, 24.4],
          [v for d in ("2022:Q3", "2025:Q3") for cat in (EQ, "Net worth") for v in list(100 * dfa(d, cat)[GI] / dfa(d, cat)[GI].sum())],
          tol=0.0501)
claim_vec("SCF top-10/20/1 shares by income of EQUITY, DEQ, STOCKS+NMMF, 2022 and 2025 (%)",
          [70.8, 83.5, 28.4, 79.0, 87.9, 37.8, 79.4, 88.3, 37.5, 70.8, 82.3, 25.7, 79.6, 87.7, 35.7, 79.5, 87.2, 36.4],
          [CONC[y][(nm, lab)] for y in (2022, 2025) for nm in ("EQUITY", "DEQ", "STOCKS+NMMF") for lab in ("top10", "top20", "top1")],
          tol=0.0501)
_cw10 = pctl_cat(S, "NETWORTH", [0, 90])
_eqw = {nm: 100 * (W[_cw10 == 2] * x[_cw10 == 2]).sum() / (W * x).sum()
        for nm, x in (("EQUITY", S.EQUITY.values.astype(float)), ("STOCKS+NMMF", (S.STOCKS + S.NMMF).values.astype(float)))}
claim("Section 4: Zandi's '90% of equity, directly and indirectly held, by the top 10%' 'fits a ranking by wealth, not by income'",
      "fits wealth ranking", f"SCF 2025 top 10% by wealth: EQUITY {_eqw['EQUITY']:.1f}%, STOCKS+NMMF {_eqw['STOCKS+NMMF']:.1f}%",
      ok=False, note="only half right: for Zandi's own concept (direct + indirect, SCF EQUITY) the top 10% by wealth hold 81.5% "
                     "(by income 70.8%); 90% fits DIRECTLY held stocks and funds ranked by wealth (SCF 91.6%, DFA 88.0%, which "
                     "excludes DC pensions). Say so")

# %% G. SCF 2025: spending shares, windfall allocations, liquidity (raw extract)
CI, CN, CW = SC["INCOME"], SC["NORMINC"], SC["NETWORTH"]


def wmean(x, m=None):
    m = np.ones(len(W), bool) if m is None else np.asarray(m, bool)
    return (W[m] * x[m]).sum() / W[m].sum()


def tshare(x, m):
    return 100 * (W[m] * x[m]).sum() / (W * x).sum()


SH = {lab: (tshare(SP, np.isin(CI, cats)), tshare(SP, np.isin(CN, cats)))
      for lab, cats in (("top1", [12]), ("top5", [11, 12]), ("top10", [10, 11, 12]), ("top20", [9, 10, 11, 12]))}
claim_vec("SCF 2025 non-housing spending shares, income 2024 ranking: top 10% / top 20% / top 1%; usual income top 10%",
          [28.3, 42.8, 6.3, 28.4], [SH["top10"][0], SH["top20"][0], SH["top1"][0], SH["top10"][1]], tol=0.0501)
_ncat = S.NINCCAT.values
_bul = [(wmean(SP), 48700), (wmean(SP, _ncat == 1), 17600), (wmean(SP, _ncat == 5), 68700), (wmean(SP, _ncat == 6), 138800),
        (wmean(SP, CW <= 2), 23400), (wmean(SP, CW == 9), 68800), (wmean(SP, CW >= 10), 136000)]
claim_vec("SCF spending vs the 2026 Bulletin Box 1 (means: all, usual-income 0-20/80-90/90-100, wealth 0-20/80-90/90-100), $k",
          [b / 1e3 for _, b in _bul], [m / 1e3 for m, _ in _bul], tol=0.41,
          note="Bulletin uses internal data; extract within $0.4k")
claim("SCF aggregate non-housing spending $6.57tn (Bulletin $6.61tn) and Bulletin top-decile shares 28.5 (income) / 27.9 (wealth)",
      "6.57 / 28.4 / 27.9", f"{(W * SP).sum() / 1e12:.2f} / {tshare(SP, _ncat == 6):.2f} / {tshare(SP, CW >= 10):.2f}",
      ok=(round((W * SP).sum() / 1e12, 2) == 6.57 and r1(tshare(SP, _ncat == 6)) == 28.4 and r1(tshare(SP, CW >= 10)) == 27.9))

# hidden-top arithmetic (NOTES section 2): needs the SCF shares and the CE gaps
Z3 = 100 * ((1 + ZANDI_TOP) ** 3 - 1)
_ht_b = [79.7, 21.6, 70.7, 19.5, 28.3, 8.7, 26.2, 8.1, 18.4, 5.8, 17.6, 5.6]
_ht_m = []
for sh_h in (SH["top1"][0], SH["top5"][0], SH["top10"][0]):
    for gap_seen in (MYGAP[("quintiles", (2022, 2025))]["gap"], MYGAP[("quintiles", (2022, 2025))]["gapx"]):
        need = (Z3 * SH["top20"][0] - (SH["top20"][0] - sh_h) * gap_seen) / sh_h
        _ht_m += [need, 100 * ((1 + need / 100) ** (1 / 3) - 1)]
claim_vec("Section 2 hidden-top table: gap the missed group needs over 2022-2025 and per year (6 rows)", _ht_b, _ht_m, tol=0.0501,
          note="'per year' annualizes 1+gap, i.e. assumes a flat bottom 80%; CE's bottom 80% grew 5.3%")

_s20b, _s1b = 100 * (_jp23["80-90%"] + _jp23["90-100%"]), 100 * _jp23["Top 1%"]
_need_bea = (Z3 * _s20b - (_s20b - _s1b) * MYGAP[("quintiles", (2022, 2025))]["gap"]) / _s1b
claim("Brief 5 'far beyond even the assumed wealth effect' survives when the hidden-top weights and the bound use the SAME denominators",
      "need > bound", f"SCF: need {_ht_m[0]:.0f} vs bound {WE[('2025:Q2', 'SCF', 0.02, 'pct99to100')]:.0f}-"
                      f"{WE[('2025:Q2', 'SCF', 0.05, 'pct99to100')]:.0f}; BEA-BLS: need {_need_bea:.0f} vs bound "
                      f"{WE[('2025:Q2', 'BEA', 0.02, 'pct99to100')]:.0f}-{WE[('2025:Q2', 'BEA', 0.05, 'pct99to100')]:.0f}",
      ok=(_ht_m[0] > WE[("2025:Q2", "SCF", 0.05, "pct99to100")] and _need_bea > WE[("2025:Q2", "BEA", 0.05, "pct99to100")]),
      note="mixing them (BEA-BLS bound 87 at 5 cents vs the SCF-weighted need 80) would reverse it; the NOTES compares like with like")
_top10 = {"joint 2023": 100 * _jp23["90-100%"], "CE 2025": ce_share("deciles", 2025, ["d10"]), "dPCE 2023": dp10[-1],
          "SCF 2025": SH["top10"][0]}
claim("Brief 8: official top-decile shares 'run from 20% to 28%' depending on ranking and scope", "20-28",
      f"{min(_top10.values()):.1f}-{max(_top10.values()):.1f} ({', '.join(f'{k} {v:.1f}' for k, v in _top10.items())})",
      ok=(round(min(_top10.values())) == 20 and round(max(_top10.values())) == 28))

# windfall allocations
MS, MV, MD = S.MPSPEND.values.astype(float), S.MPSAVE.values.astype(float), S.MPDEBT.values.astype(float)
NI = S.NORMINC.values.astype(float)
claim("Windfall means, all families: spend/save/debt 22.35/47.31/30.30 (FEDS Note Figure 1)", "22.35/47.31/30.30",
      f"{wmean(MS):.2f}/{wmean(MV):.2f}/{wmean(MD):.2f}",
      ok=(round(wmean(MS), 2) == 22.35 and round(wmean(MV), 2) == 47.31 and round(wmean(MD), 2) == 30.30))
claim("Spend nothing 46% of families, spend all 4%; mean windfall $11,746", "46.3 / 4.1 / 11746",
      f"{100 * wmean((MS == 0).astype(float)):.1f} / {100 * wmean((MS == 100).astype(float)):.1f} / {wmean(NI / 12):,.0f}",
      ok=(r1(100 * wmean((MS == 0).astype(float))) == 46.3 and round(wmean(NI / 12)) == 11746),
      note="publisher (Figure 2): 47% at zero, 4% at 100")
# FEDS Note accessible tables (raw html)
_acc = (RAW / "fed/feds_notes/feds-note-mpc-heterogeneity-accessible-20261009.htm").read_text(encoding="utf-8", errors="replace")
_pubtabs = []
for tb in re.findall(r"<table.*?</table>", _acc, re.S):
    cells = [html.unescape(re.sub(r"<[^>]+>", "", x)).strip() for x in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", tb, re.S)]
    _pubtabs.append(cells)


def pub_rows(cells):
    rows, i = [], 0
    while i < len(cells):
        if cells[i] in ("Bottom 10%", "10-20%", "20-30%", "30-40%", "40-50%", "50-60%", "60-70%", "70-80%", "80-90%",
                        "Top 90-95%", "Top 95-99%", "Top 1%"):
            rows.append([float(cells[i + 1]), float(cells[i + 2]), float(cells[i + 3])])
            i += 4
        else:
            i += 1
    return np.array(rows)


PUB_INC = pub_rows(_pubtabs[2])
PUB_NW = pub_rows(_pubtabs[3])
MY_INC = np.array([[wmean(x, CN == k) for x in (MS, MV, MD)] for k in range(1, 13)])
MY_NW = np.array([[wmean(x, CW == k) for x in (MS, MV, MD)] for k in range(1, 13)])
_dlo, _dhi = np.abs(MY_INC - PUB_INC)[:6].max(), np.abs(MY_INC - PUB_INC)[6:].max()
claim("Section 5: extract vs FEDS Note Figure 3 (usual income): within 0.2 from the 60th percentile up, 0.7 below",
      "0.2 / 0.7", f"{_dhi:.2f} / {_dlo:.2f}", ok=(_dhi <= 0.25 and _dlo <= 0.75), note="spend, save and debt shares")
claim("Section 5: extract vs FEDS Note Figure 3 (net worth): within 0.3 point", 0.3, np.abs(MY_NW - PUB_NW).max(), tol=0.0051)
_wfb = pd.read_csv(OUT / "direct_scf2025_windfall.csv")
_wf = _wfb[_wfb.block == "windfall"]


def group_codes():
    """record-level group codes for every grouping the NOTES tabulates (mine), keyed like the builder's CSV"""
    htm_liq = (S.CHECKING + S.SAVING + S.MMA + S.CALL + S.PREPAID + S.CDS + S.NMMF + S.STOCKS + S.BOND).values.astype(float)
    htm = htm_liq < NI / 24
    nliq = (S.LIQ + S.NMMF + S.STOCKS + S.BOND - S.CCBAL).values.astype(float)
    illiq = (S.HOMEEQ + (S.ORESRE - S.RESDBT) + S.NNRESRE + S.RETQLIQ + S.CASHLI + S.CDS + S.SAVBND + S.OTHMA).values.astype(float)
    kh = nliq <= S.INCOME.values / 24
    months = np.where(NI > 0, htm_liq / np.where(NI > 0, NI, 1) * 12, np.where(htm_liq > 0, np.inf, 0.0))
    lab12 = ["0-10", "10-20", "20-30", "30-40", "40-50", "50-60", "60-70", "70-80", "80-90", "90-95", "95-99", "99-100"]
    G = {"usual income, 12 groups": np.array(lab12)[CN - 1], "income 2024, 12 groups": np.array(lab12)[CI - 1],
         "net worth, 12 groups": np.array(lab12)[CW - 1],
         "usual income, deciles": np.array([f"D{k}" for k in np.minimum(CN, 10)]),
         "income 2024, deciles": np.array([f"D{k}" for k in np.minimum(CI, 10)]),
         "net worth, deciles": np.array([f"D{k}" for k in np.minimum(CW, 10)]),
         "hand-to-mouth (FEDS Note definition)": np.where(htm, "hand-to-mouth", "not hand-to-mouth"),
         "hand-to-mouth (KVW-style, poor/wealthy)": np.where(~kh, "not hand-to-mouth",
                                                             np.where(illiq > 0, "wealthy hand-to-mouth", "poor hand-to-mouth")),
         "liquidity, months of usual income": pd.cut(months, [-np.inf, 0.5, 2, 6, 24, np.inf], right=False,
                                                     labels=["<0.5 month (hand-to-mouth)", "0.5-2 months", "2-6 months",
                                                             "6-24 months", "24+ months"]).astype(str),
         "hand-to-mouth x usual-income quintile": np.array([f"{'HtM' if h else 'not HtM'}, usual-income Q{min(q, 5)}"
                                                            for h, q in zip(htm, S.NINCCAT.values)]),
         "spending vs income last year (WSAVED)": pd.Series(S.WSAVED.values).map(
             {1: "spending exceeded income", 2: "spending equaled income", 3: "spending below income"}).values}
    return G, htm, htm_liq


GROUPS, HTM, LIQF = group_codes()
_b, _m, _bf, _mf = [], [], [], []
for gname, codes in GROUPS.items():
    for _, r in _wf[_wf.grouping == gname].iterrows():
        msk = codes == r.group
        _b += [r.spend_pct, r.save_pct, r.debt_pct, r.spend_income_weighted_pct, r.share_spend_none_pct]
        _m += [wmean(MS, msk), wmean(MV, msk), wmean(MD, msk), (W[msk] * NI[msk] * MS[msk]).sum() / (W[msk] * NI[msk]).sum(),
               100 * wmean((MS == 0).astype(float), msk)]
        _bf.append(r.families_m)
        _mf.append(W[msk].sum() / 1e6)
claim_vec("Section 5 windfall tables: spend/save/debt, income-weighted spend, % spending nothing (11 groupings, builder CSV)",
          _b, _m, tol=0.006, note="FEDS-Note hand-to-mouth = liquid assets incl. CDs and direct funds/stocks/bonds < NORMINC/24")
claim_vec("Section 5 windfall tables: families (m) per group", _bf, _mf, tol=0.0151,
          note="largest gap (0.01m) is the liquidity-months bins: the builder sums LIQ, which the extract sets to 1 for "
               "zero-balance account holders, so a few families with NORMINC <= 0 land in '24+' instead of '<0.5'")
_ra = _wfb[_wfb.block == "windfall"]
_rr = _ra[_ra.grouping == "hand-to-mouth, regression-adjusted (FEDS Note Fig. 4 recipe)"]
_ok_inc = NI > 0
_X = np.column_stack([np.ones(_ok_inc.sum()), HTM[_ok_inc].astype(float), np.log(NI[_ok_inc])])
_fit = sm.WLS(MS[_ok_inc], _X, weights=W[_ok_inc]).fit()
_ml = (W[_ok_inc] * np.log(NI[_ok_inc])).sum() / W[_ok_inc].sum()
claim("Regression-adjusted (FEDS Note Fig. 4 recipe): hand-to-mouth 23.7 vs not 21.7 (note: 22.9 vs 20.3)", "23.7 / 21.7",
      f"{_fit.params[0] + _fit.params[1] + _fit.params[2] * _ml:.2f} / {_fit.params[0] + _fit.params[2] * _ml:.2f}",
      ok=(r1(_fit.params[0] + _fit.params[1] + _fit.params[2] * _ml) == 23.7 and r1(_fit.params[0] + _fit.params[2] * _ml) == 21.7))
claim("Section 5 text: KVW illiquid wealth list (home equity, other RE net of debt, retirement, CV life insurance, CDs, "
      "savings bonds, other managed assets)", "list as printed", "builder also adds NNRESRE", ok=True,
      note="its 17.3m poor / 36.9m wealthy HtM need NNRESRE (without it 17.6m / 36.6m): add it to the printed list")

# %% G2. the gradient against the post, with my own family bootstrap
FAM = S.YY1.values
_ufam, _finv = np.unique(FAM, return_inverse=True)
NF = len(_ufam)


def boot_means(codes, labels, x=MS, reps=N_BOOT, chunk=100):
    """family bootstrap (all five implicates of a family move together), group membership fixed; returns reps x groups"""
    onehot = np.stack([(codes == l).astype(float) for l in labels], axis=1)
    out = []
    for start in tqdm(range(0, reps, chunk), desc="family bootstrap", leave=False):
        n = min(chunk, reps - start)
        draws = RNG.integers(0, NF, size=(n, NF))
        cnt = np.stack([np.bincount(d, minlength=NF) for d in draws])[:, _finv]       # n x records
        wt = cnt * W
        out.append((wt * x) @ onehot / (wt @ onehot))
    return np.vstack(out)


LAB12 = ["0-10", "10-20", "20-30", "30-40", "40-50", "50-60", "60-70", "70-80", "80-90", "90-95", "95-99", "99-100"]
LABD = [f"D{k}" for k in range(1, 11)]
BOOT = {g: boot_means(GROUPS[g], labs) for g, labs in (("usual income, 12 groups", LAB12), ("income 2024, 12 groups", LAB12),
                                                       ("usual income, deciles", LABD), ("income 2024, deciles", LABD))}
_grb = _wfb[_wfb.block == "gradient_vs_post"].set_index("grouping")
_b, _m = [], []
for gname, (t, bt) in (("usual income, deciles", ("D10", "D1")), ("income 2024, deciles", ("D10", "D1")),
                       ("usual income, 12 groups", ("99-100", "0-10")), ("income 2024, 12 groups", ("99-100", "0-10"))):
    labs = LABD if "deciles" in gname else LAB12
    mt, mb = GROUPS[gname] == t, GROUPS[gname] == bt
    ratio = wmean(MS, mt) / wmean(MS, mb)
    bs = BOOT[gname][:, labs.index(t)] / BOOT[gname][:, labs.index(bt)]
    lo, hi = np.percentile(bs, [2.5, 97.5])
    r = _grb.loc[gname]
    claim(f"Gradient {gname} {t}/{bt}: ratio, 95% bootstrap interval", f"{r.ratio_spend:.2f} ({r.ratio_spend_lo95:.2f}-{r.ratio_spend_hi95:.2f})",
          f"{ratio:.3f} ({lo:.2f}-{hi:.2f})",
          ok=(abs(ratio - r.ratio_spend) < 0.005 and abs(lo - r.ratio_spend_lo95) <= 0.04 and abs(hi - r.ratio_spend_hi95) <= 0.04),
          note=f"my {N_BOOT} replicates, other seed; spend+debt ratio {wmean(MS + MD, mt) / wmean(MS + MD, mb):.2f}, income-weighted "
               f"{((W[mt] * NI[mt] * MS[mt]).sum() / (W[mt] * NI[mt]).sum()) / ((W[mb] * NI[mb] * MS[mb]).sum() / (W[mb] * NI[mb]).sum()):.2f}")
    _b += [r.ratio_spend_plus_debt, r.ratio_income_weighted]
    _m += [wmean(MS + MD, mt) / wmean(MS + MD, mb),
           ((W[mt] * NI[mt] * MS[mt]).sum() / (W[mt] * NI[mt]).sum()) / ((W[mb] * NI[mb] * MS[mb]).sum() / (W[mb] * NI[mb]).sum())]
claim_vec("Gradient table: spend+debt and income-weighted ratios (4 rows)", _b, _m, tol=0.005)
_seb, _sem = [], []
for gname, labs in (("usual income, 12 groups", LAB12), ("income 2024, deciles", LABD), ("usual income, deciles", LABD)):
    for i, l in enumerate(labs):
        r = _wf[(_wf.grouping == gname) & (_wf.group == l)].iloc[0]
        _seb.append(r.se_spend_boot)
        _sem.append(BOOT[gname][:, i].std(ddof=1))
_rel = np.max(np.abs(np.array(_sem) / np.array(_seb) - 1))
claim("Bootstrap SEs of the spend share (32 groups) agree with mine within 15% (Monte Carlo noise of 400 vs my replicates)",
      "within 15%", f"max rel. diff {100 * _rel:.0f}%", ok=_rel <= 0.15)
_fn = (RAW / "fed/feds_notes/feds-note-mpc-heterogeneity-20261009.html").read_text(encoding="utf-8", errors="replace")
_fn_txt = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", _fn)))
_ci = re.search(r"conventional 95 percent confidence intervals for these estimates are \(([\d.]+),\s*([\d.]+)\)", _fn_txt)
_se1 = BOOT["usual income, 12 groups"][:, LAB12.index("99-100")].std(ddof=1)
claim("Section 5: the note's 'conventional' 95% interval for the top 1% (12.9-15.0) vs a family-bootstrap SE of about 2.7",
      "12.9-15.0 / 2.7", f"{_ci.group(1)}-{_ci.group(2)} / {_se1:.2f}",
      ok=(_ci.group(1) == "12.9" and _ci.group(2) == "15.0" and abs(_se1 - 2.73) <= 0.35),
      note="note uses the internal data and the SCF design; my SE ignores the design too, so 'much narrower' is about method")
_n1 = len(np.unique(FAM[CN == 12]))
claim("Section 5: the top-1% (usual income) group 'has 508 families'", 508, _n1, tol=0,
      note=f"distinct families with any implicate in the group; records/5 = {np.sum(CN == 12) / 5:.0f}")
claim("Brief 7: windfall top/bottom-decile ratio 0.62-0.69 (95% 0.51-0.83) vs post's 0.40-0.65; top 1% 0.49-0.61", "0.62-0.69",
      f"{wmean(MS, GROUPS['income 2024, deciles'] == 'D10') / wmean(MS, GROUPS['income 2024, deciles'] == 'D1'):.2f}-"
      f"{wmean(MS, GROUPS['usual income, deciles'] == 'D10') / wmean(MS, GROUPS['usual income, deciles'] == 'D1'):.2f}", ok=True,
      note="numbers hold; wording: a stated share of a one-off windfall sized at a month's income is not the post's MPC out of a "
           "permanent flow, so it bears on the ORDERING more than on the 'gradient' ('bears directly' in the brief is too strong; "
           "section 5 caveats it properly)")

# %% H. Zandi's arithmetic and the post's parameters
claim_vec("Zandi's cumulative gap 1.04^T - 1 for T = 1, 2, 3, 6 (pts)", [4.0, 8.2, 12.5, 26.5],
          [100 * (1.04 ** t - 1) for t in (1, 2, 3, 6)], tol=0.0501)
_aggz = [100 * (s * (1 + ZANDI_TOP) + (1 - s) * (1 + ZANDI_B80) - 1)
         for s in (ce_share("quintiles", 2025, ["q5"]) / 100, dp20[-1] / 100, SH["top20"][0] / 100)]
claim("Zandi's own numbers: top 20% at +4% and bottom 80% at 0% give the 2% aggregate he quotes only if the top fifth has half of spending",
      "2.0 % a year", f"{min(_aggz):.2f}-{max(_aggz):.2f} % a year with CE / dPCE / SCF top-20 shares", ok=True,
      note="not in NOTES_direct (it is in NOTES_fingerprint); worth one line: his split and his aggregate cannot both hold on "
           "official shares, while the CE's own aggregate (+1.9%/yr real 2022-25) matches his 2%")
_post = (RAW / "post/post.txt").read_text(encoding="utf-8")
_fn31 = re.search(r"\[\^31\]:\s*Wealth-effect propensities of ([^ ]+) cents", _post)
_body = re.search(r"wealth-effect propensities the literature estimates, ([a-z]+ to [a-z]+) cents", _post)
claim("Post: wealth-effect propensity 2-5 cents per dollar per year (footnote 31)", "2-5", _fn31.group(1).replace("–", "-"),
      ok=_fn31.group(1).replace("–", "-") == "2-5",
      note=f"the post's body text says '{_body.group(1)}' cents; the NOTES' '2-5' is the footnote/Fig 0 range")
_fn27 = re.search(r"run from (1\.0) in the bottom deciles to (0\.40)–(0\.65) at the top", _post)
claim("Post: MPC schedule 1.0 at the bottom to 0.40-0.65 at the top (footnote 27), so a top/bottom ratio of 0.40-0.65",
      "1.0 -> 0.40-0.65", f"{_fn27.group(1)} -> {_fn27.group(2)}-{_fn27.group(3)}", ok=_fn27 is not None)

# %% I. adversarial reading: conclusions against what the data can carry
EV = pd.read_csv(OUT / "direct_evidence_table.csv")
_top_sav = EV[EV.source.str.contains("saving rates \\(top\\)")].iloc[0]
_bot_sav = EV[EV.source.str.contains("saving rates \\(bottom 80%\\)")].iloc[0]
claim("Evidence table: joint-distribution saving rows scored 'no' (top) and 'yes' (bottom 80%) against Zandi's saving story",
      f"{_top_sav.consistent_with_zandi_split} / {_bot_sav.consistent_with_zandi_split}", "can't tell / can't tell", ok=False,
      note=f"material: the data end in 2023 ({jrate(2022, DL[:8]):.1f} -> {jrate(2023, DL[:8]):.1f}% for the bottom 80%, i.e. "
           f"IMPROVING in the last year; the 2019->2023 fall happened by 2022), while Zandi's claim is about 2025-26 saving after the "
           f"equity run-up. The row's own caveat says it 'does not show ... either way': score both 'can't tell'")
_g1 = MYGAP[("quintiles", (2024, 2025))]
claim("Brief 1 'the official spending distributions show no K after 2022' also holds in the latest CE year alone",
      "no K", f"2024->2025 gap {_g1['gap']:+.1f} (excl. {_g1['gapx']:+.1f}), SE {_g1['se']:.1f}, Zandi +4.0", ok=True,
      note="holds only in the sense 'not significant': the latest year is as close to Zandi's 4 points as to zero; the case "
           "against his split rests on the multi-year windows, and the equity run-up was largest after the CE window closes")
claim("Caveat: adjacent CE years share Interview CUs, so independence OVERstates the SE of a one-year change; no overlap beyond",
      "overstated", "overstated", ok=True, note="CE Interview CUs are interviewed for 4 consecutive quarters: positive correlation "
                                                 "between adjacent annual means; two-year windows share no CUs")
claim("Brief 6: 'aggregate saving rate fell from 6.2% (2023-24) to 3.8% (Sep 2026)'; the cross-check uses 4.1 (2026Q3)",
      "6.2 -> 3.8 (and 4.1)", f"{_sr2324:.1f} -> {SRM['2026M09']:.1f} (Q3 {_sr26q3:.1f})", ok=True,
      note="both stated; the 2.1-point fall is the like-with-like one")
claim("Brief 4 / section 4: DFA splits after 2022Q3 labelled as model extrapolations wherever used", "labelled",
      "labelled in brief, section 4, evidence table, caveats", ok=all(s in NOTES for s in ("model-based after 2022Q3", "model extrapolations")))
claim("Moody's top-decile ~49% treated as press figure, not data", "not used",
      "not used" if "It is not public data" in NOTES else "used", ok="It is not public data" in NOTES)

# %% summary
n_ok = sum(1 for ok, _ in RESULTS if ok)
n_bad = len(RESULTS) - n_ok
print(f"\nSUMMARY | {len(RESULTS)} claims | {n_ok} OK | {n_bad} BAD")
for ok, line in RESULTS:
    if not ok:
        print(line)
