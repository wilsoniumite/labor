"""Independent verification of austax/taxtransfer, written by a separate verifier (not the builder).

What it does
  1. Downloads the sources again (ABS spreadsheets and archived pages, ABS Data API, FRED, OECD and DSS pages) into
     a temporary folder; if a download fails it falls back to the vendored copy in ../data/raw and says so. Reports
     whether each fresh file is byte-identical to the vendored one.
  2. Recomputes every headline number from those files with its own parsing (row labels located by scanning, not
     the builder's helpers), and compares with ../out/facts.csv. Flags any difference beyond rounding.
  3. Prints the context a referee would want: the full yearly series of the tax shares where ABS publishes them
     (2000-01 to 2009-10, 2011-12 to 2024-25), base-year sensitivity, and the labour-share and dwellings series.
  4. Confirms every quoted sentence on the freshly downloaded OECD and DSS pages.

Run (from austax/taxtransfer):  ..\\..\\venv\\Scripts\\python.exe -I checks\\verify_independent.py
Exit code 1 if any recomputed headline differs from facts.csv beyond rounding or a quote is missing.
"""
import csv
import hashlib
import html
import re
import sys
import tempfile
from pathlib import Path

import shutil
import subprocess

import openpyxl
import pandas as pd
import xlrd

HERE = Path(__file__).resolve().parent.parent
RAW = HERE / "data" / "raw"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}
ABS_T = "https://www.abs.gov.au/statistics/economy/government/taxation-revenue-australia"
SOURCES = {  # local name -> (url, vendored name or None)
    "do001_2425.xlsx": (f"{ABS_T}/2024-25/55060DO001_202425.xlsx", "55060DO001_202425.xlsx"),
    "do002_2425.xlsx": (f"{ABS_T}/2024-25/55060DO002_202425.xlsx", "55060DO002_202425.xlsx"),
    "do002_2021.xlsx": (f"{ABS_T}/2020-21/55060DO002_202021.xlsx", None),   # extra: fills 2011-12 .. 2014-15
    "cube_0910.xls": ("https://www.abs.gov.au/ausstats/subscriber.nsf/log?openagent&55060do001_200910.xls&5506.0&Data%20Cubes&"
                      "4F1736E61FDD622CCA25786F0013D73C&0&2009-10&12.04.2011&Latest", "55060do001_200910.xls"),
    "mf_0506.html": ("https://www.abs.gov.au/AUSSTATS/abs@.nsf/Lookup/5506.0Main+Features12005-06?OpenDocument",
                     "5506.0_2005-06_main_features.html"),
    "mf_0910_7.html": ("https://www.abs.gov.au/ausstats/abs@.nsf/Previousproducts/5506.0Main%20Features72009-10?opendocument&"
                       "tabname=Summary&prodno=5506.0&issue=2009-10&num=&view=", "5506.0_2009-10_main_features7_all_levels.html"),
    "na_t7.xlsx": ("https://www.abs.gov.au/statistics/economy/national-accounts/australian-national-accounts-national-income-"
                   "expenditure-and-product/jun-2026/5206007_Income_From_GDP.xlsx", "5206007_Income_From_GDP.xlsx"),
    "ana_inc.csv": ("https://data.api.abs.gov.au/rest/data/ABS,ANA_INC,1.0.0/C.COE+GPF+GMI+GOS.SSS+PHD.10.AUS.Q?startPeriod=1959-Q3",
                    None),
    "W055.csv": ("https://fred.stlouisfed.org/graph/fredgraph.csv?id=W055RC1A027NBEA", "FRED_W055RC1A027NBEA.csv"),
    "A061.csv": ("https://fred.stlouisfed.org/graph/fredgraph.csv?id=A061RC1A027NBEA", "FRED_A061RC1A027NBEA.csv"),
    "W054.csv": ("https://fred.stlouisfed.org/graph/fredgraph.csv?id=W054RC1A027NBEA", "FRED_W054RC1A027NBEA.csv"),
    "oecd.html": ("https://www.oecd.org/en/publications/the-future-of-social-protection_9789264306943-en/full-report/component-5.html",
                  "oecd_2018_future_social_protection_ch2_australia.html"),
    "dss_422.html": ("https://guides.dss.gov.au/social-security-guide/4/2/2", "dss_ssguide_4.2.2_benefits_income_test.html"),
    "dss_423.html": ("https://guides.dss.gov.au/social-security-guide/4/2/3", "dss_ssguide_4.2.3_assets_tests.html"),
    "dss_42110.html": ("https://guides.dss.gov.au/social-security-guide/4/2/1/10", "dss_ssguide_4.2.1.10_pensions_income_test.html"),
}

problems = []


def flag(msg):
    problems.append(msg)
    print("  ** " + msg)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


# ------------------------------------------------------------------ 0. fetch
tmp = Path(tempfile.mkdtemp(prefix="tt_verify_"))
F = {}
print("== sources (fresh download vs vendored copy)")
for name, (url, vend) in SOURCES.items():
    dest = tmp / name
    try:  # curl: uses the system certificate store, which the corporate TLS proxy needs
        cmd = [shutil.which("curl"), "-sS", "-L", "--fail", "--max-time", "180", "-o", str(dest)]
        if "fred.stlouisfed.org" not in url:          # FRED refuses the browser user agent; ABS pages need one
            cmd += ["-A", UA["User-Agent"]]
        if name == "ana_inc.csv":
            cmd += ["-H", "Accept: application/vnd.sdmx.data+csv"]
        subprocess.run(cmd + [url], check=True, capture_output=True)
        how = "fresh"
    except Exception as e:  # fall back to the vendored copy
        if vend is None:
            print(f"  {name:16s} download failed ({type(e).__name__}); no vendored copy")
            continue
        dest = RAW / vend
        how = f"VENDORED (download failed: {type(e).__name__})"
    same = ""
    if vend and how == "fresh":
        same = "identical to vendored" if sha(dest) == sha(RAW / vend) else "DIFFERS from vendored"
    F[name] = dest
    print(f"  {name:16s} {how:8s} {same}")


# ------------------------------------------------------------------ helpers (own parsing)
def grid_xlsx(path, sheet):
    ws = openpyxl.load_workbook(path, read_only=True, data_only=True)[sheet]
    return [list(r) for r in ws.iter_rows(values_only=True)]


def grid_xls(path, sheet):
    s = xlrd.open_workbook(path).sheet_by_name(sheet)
    return [s.row_values(i) for i in range(s.nrows)]


def by_year(grid):
    """{label_occurrence_key: {year: value}}: labels stripped; duplicate labels get '#2', '#3' suffixes."""
    hdr = next(r for r in grid if sum(bool(isinstance(v, str) and re.fullmatch(r"\d{4}-\d{2}", v.strip())) for v in r) >= 2)
    cols = {j: v.strip() for j, v in enumerate(hdr) if isinstance(v, str) and re.fullmatch(r"\d{4}-\d{2}", v.strip())}
    out, seen = {}, {}
    for r in grid:
        lab = str(r[0]).strip() if r and r[0] is not None else ""
        if not lab:
            continue
        vals = {y: r[j] for j, y in cols.items() if isinstance(r[j], (int, float))}
        if not vals:
            continue
        seen[lab] = seen.get(lab, 0) + 1
        out[lab if seen[lab] == 1 else f"{lab}#{seen[lab]}"] = {y: float(v) for y, v in vals.items()}
    return out


def text_lines(path):
    t = Path(path).read_text(encoding="utf-8", errors="replace")
    t = re.sub(r"(?is)<(script|style).*?</\1>", "", t)
    t = re.sub(r"(?i)<br\s*/?>|</(td|th|tr|p|div|li|h\d)>", "\n", t)
    t = html.unescape(re.sub(r"<[^>]+>", " ", t))
    return [ln.strip() for ln in t.split("\n") if ln.strip()]


def flat(path):
    return re.sub(r"\s+", " ", " ".join(text_lines(path)))


def num(s):
    return float(s.replace("\xa0", "").replace(" ", "").replace(",", ""))


def web_row(lines, anchor, label, n, nth=1):
    """n numbers that follow the nth `label` after `anchor` in an archived ABS web table."""
    i = next(k for k, l in enumerate(lines) if l == anchor)
    hits = [k for k in range(i, len(lines)) if lines[k] == label]
    k = hits[nth - 1]
    return [num(x) for x in lines[k + 1:k + 1 + n]]


facts = list(csv.DictReader(open(HERE / "out" / "facts.csv", encoding="utf-8")))


def builder(prefix, period):
    hit = [f for f in facts if f["fact"].startswith(prefix) and f["period"] == period]
    return float(hit[0]["value"]) if len(hit) == 1 else None


rows = []


def compare(claim, mine, prefix, period, tol=0.051):
    b = builder(prefix, period)
    ok = b is not None and abs(round(mine, 1 if tol > 0.01 else 3) - b) < tol
    rows.append((claim, period, b, mine, ok))
    if not ok:
        flag(f"MISMATCH {claim} {period}: builder {b} vs verifier {mine:.3f}")


# ------------------------------------------------------------------ 1. tax 2024-25 release
t2 = by_year(grid_xlsx(F["do002_2425.xlsx"], "Table_2"))
t5 = by_year(grid_xlsx(F["do002_2425.xlsx"], "Table_5"))
c1 = by_year(grid_xlsx(F["do001_2425.xlsx"], "Table_1"))
s10 = by_year(grid_xlsx(F["do001_2425.xlsx"], "Table_10"))
TOT = t2["Total taxation revenue"]
assert TOT == t5["Total all levels of government"], "Table 2 and Table 5 totals differ"
Y = "2024-25"
new = {}
for y in TOT:
    new[y] = dict(
        total=TOT[y],
        indiv_excl=c1["Personal income tax"][y] + c1["Government health insurance levy"][y],
        indiv_incl=t2["Income taxes levied on individuals"][y],
        fbt=c1["Fringe benefits tax"][y],
        payroll=t2["Payroll taxes"][y],
        payroll_all=t2["Total taxes on employers payroll and labour force"][y],
        company=c1["Company income tax"][y],
        super=c1["Income tax paid by superannuation funds"][y],
        gst=t2["Goods and services tax (GST)"][y],
        land=t2["Land taxes"][y],
        rates=t2["Municipal rates"][y],
        conv=s10["Stamp duties on conveyances"][y],
    )
    d = new[y]
    d["labour"] = d["indiv_incl"] + d["payroll_all"]
    d["recurrent"] = d["land"] + d["rates"]
    # identity: Commonwealth PIT + Medicare + FBT = all-levels individuals category
    if abs(d["indiv_excl"] + d["fbt"] - d["indiv_incl"]) > 2:
        flag(f"{y}: PIT+Medicare+FBT {d['indiv_excl'] + d['fbt']:,.0f} != ABS individuals {d['indiv_incl']:,.0f}")


def s(d, k):
    return 100 * d[k] / d["total"]


d = new[Y]
print(f"\n== 2024-25 all-levels total ${d['total']:,.0f}m")
rel = flat(RAW / "5506.0_2024-25_release_page.html")
print("  release page '$839.0 billion':", "$839.0 billion" in rel)
compare("Total taxation revenue $m", d["total"], "Total taxation revenue", Y, tol=0.5)
for claim, k, pre in (("(i) PIT + Medicare levy, excl FBT", "indiv_excl", "(i) Taxes on income of individuals (personal"),
                      ("(i') ABS individuals incl FBT", "indiv_incl", "(i') ABS category"),
                      ("(ii) payroll tax", "payroll", "(ii) Payroll taxes"),
                      ("(ii') all employers' payroll and labour force", "payroll_all", "(ii') All taxes"),
                      ("(iii) FBT", "fbt", "(iii) Fringe"),
                      ("taxes mainly on labour", "labour", "Taxes mainly on labour = "),
                      ("(iv) company income tax", "company", "(iv) Company"),
                      ("super funds' income tax", "super", "Not counted as labour"),
                      ("(v) GST", "gst", "(v) Goods"),
                      ("land taxes", "land", "(vi) Land taxes"),
                      ("municipal rates", "rates", "(vi) Municipal"),
                      ("recurrent land + rates", "recurrent", "Recurrent taxes on land = "),
                      ("(vii) conveyancing duty", "conv", "(vii) Stamp duties")):
    compare(claim, s(d, k), pre, Y)

# netting checks on the 2024-25 lines taken from level-of-government tables
fin_all = t2["Taxes on financial and capital transactions"][Y]
fin_sl = s10["Total taxes on financial and capital transactions"][Y]
print(f"  conveyancing: S&L financial-transactions total {fin_sl:,.0f} + Commonwealth 15 vs all-levels {fin_all:,.0f} "
      f"(no netting on this line: {abs(fin_sl + c1['Taxes on financial and capital transactions'][Y] - fin_all) < 1})")
loc = t5["Tax revenue net of intergovernmental taxes#3"][Y]
print(f"  municipal rates {d['rates']:,.0f} vs local-government tax total {loc:,.0f}: rates include the ACT government's "
      f"general rates ({d['rates'] - loc:,.0f}m more than all councils' taxes)")

# ------------------------------------------------------------------ 2. history 2000-01 .. 2009-10 (2011 cube + web tables)
o1 = by_year(grid_xls(F["cube_0910.xls"], "Table_1"))
o18 = by_year(grid_xls(F["cube_0910.xls"], "Table_18"))
L06 = text_lines(F["mf_0506.html"])
L10 = text_lines(F["mf_0910_7.html"])
y06 = ["2000-01", "2001-02", "2002-03", "2003-04", "2004-05", "2005-06"]
y10 = ["2004-05", "2005-06", "2006-07", "2007-08", "2008-09", "2009-10"]
tot = dict(zip(y06, web_row(L06, "ALL LEVELS OF GOVERNMENT", "Total taxation revenue", 6)))
pay = dict(zip(y06, web_row(L06, "ALL LEVELS OF GOVERNMENT", "Employers' payroll taxes", 6)))
pub_ind06 = dict(zip(y06, web_row(L06, "MAJOR COMPONENTS OF TOTAL TAXATION, All levels of government",
                                  "Income taxes levied on individuals", 6)))
a10 = "TAXATION, All levels of Government"
tot10 = dict(zip(y10, web_row(L10, a10, "Total", 6, nth=sum(1 for l in L10[L10.index(a10):] if l == "Total"))))
pay10 = dict(zip(y10, web_row(L10, a10, "Total", 6, nth=2)))      # 2nd 'Total' = employers' payroll taxes
assert web_row(L10, a10, "Other employers labour force taxes", 6)[-1] == 507
ind10 = dict(zip(y10, web_row(L10, a10, "Income taxes levied on individuals", 6)))
for y in y10:          # same release as the cube for 2004-05 onward
    tot[y], pay[y] = tot10[y], pay10[y]
ind_old = o1["Total"]              # first 'Total' row in Table 1 = income taxes levied on individuals
assert all(abs(ind_old[y] - ind10[y]) < 1 for y in y10), "cube individuals != 2009-10 web table"
old = {}
for y in y06 + y10[2:]:
    old[y] = dict(total=tot[y], indiv_incl=ind_old[y], fbt=o1["Fringe benefits tax"][y],
                  indiv_excl=ind_old[y] - o1["Fringe benefits tax"][y], payroll_all=pay[y],
                  land=o18["Land taxes"][y], rates=o18["Municipal rates"][y], conv=o18["Stamp duties on conveyances"][y])
    old[y]["labour"] = old[y]["indiv_incl"] + old[y]["payroll_all"]
    old[y]["recurrent"] = old[y]["land"] + old[y]["rates"]
print("\n== seams")
print(f"  2000-01 individuals {s(old['2000-01'], 'indiv_incl'):.2f}% vs ABS-published (2005-06 release) {pub_ind06['2000-01']}%")
print(f"  2001-02 individuals {s(old['2001-02'], 'indiv_incl'):.2f}% vs ABS-published {pub_ind06['2001-02']}%")
t06a = web_row(L06, "ALL LEVELS OF GOVERNMENT", "Total taxation revenue", 6)[-1]
print(f"  2005-06 all-levels total: 2007 release {t06a:,.0f} -> 2011 release {tot10['2005-06']:,.0f} "
      f"({100 * (tot10['2005-06'] / t06a - 1):+.2f}%)")
last_total = lambda tab: tab[[k for k in tab if k == "Total" or k.startswith("Total#")][-1]]   # grand total row
cw01, sl01 = last_total(o1)["2000-01"], last_total(o18)["2000-01"]
ig01 = o18["Taxes received from other levels of government"]["2000-01"]
alt01 = cw01 + sl01 - ig01
print(f"  2000-01 all-levels total rebuilt from the 2011 cube (Cwlth {cw01:,.0f} + S&L {sl01:,.0f} - S&L taxes from other "
      f"levels {ig01:,.0f}) = {alt01:,.0f} vs 2007-release web total {tot['2000-01']:,.0f}; labour share on that base "
      f"{100 * (ind_old['2000-01'] + pay['2000-01']) / alt01:.2f}%")

for claim, k, pre in (("(i) excl FBT", "indiv_excl", "(i) Taxes on income of individuals excluding FBT"),
                      ("(i') incl FBT", "indiv_incl", "(i') ABS 'Income taxes levied"),
                      ("recurrent land + rates", "recurrent", "Recurrent taxes on land (land taxes"),
                      ("taxes mainly on labour", "labour", "Taxes mainly on labour (i)")):
    for y, dd in (("2000-01", old["2000-01"]), ("2009-10", old["2009-10"]), ("2015-16", new["2015-16"])):
        compare(f"history {claim}", s(dd, k), pre, y)

# 2011-12 .. 2014-15 from the 2020-21 release (only if downloaded)
mid = {}
if "do002_2021.xlsx" in F:
    m2 = by_year(grid_xlsx(F["do002_2021.xlsx"], "Table_2"))
    for y in ("2011-12", "2012-13", "2013-14", "2014-15"):
        mid[y] = dict(total=m2["Total taxation revenue"][y], indiv_incl=m2["Income taxes levied on individuals"][y],
                      payroll_all=m2["Total taxes on employers payroll and labour force"][y],
                      land=m2["Land taxes"][y], rates=m2["Municipal rates"][y])
        mid[y]["labour"] = mid[y]["indiv_incl"] + mid[y]["payroll_all"]
        mid[y]["recurrent"] = mid[y]["land"] + mid[y]["rates"]
    print(f"  2015-16 total: 2021 release {m2['Total taxation revenue']['2015-16']:,.0f} vs 2026 release {TOT['2015-16']:,.0f}")

allyrs = {**old, **mid, **new}
print("\n== yearly series, % of all-levels tax (2010-11 not published in the files used)")
print("  year     indiv_incl  indiv_excl  labour_mainly  recurrent_land")
for y in sorted(allyrs):
    dd = allyrs[y]
    ex = f"{s(dd, 'indiv_excl'):10.1f}" if "indiv_excl" in dd else "         -"
    print(f"  {y}  {s(dd, 'indiv_incl'):10.1f}  {ex}  {s(dd, 'labour'):13.1f}  {s(dd, 'recurrent'):14.1f}")
lab = {y: s(dd, "labour") for y, dd in allyrs.items()}
lo, hi = min(lab, key=lab.get), max(lab, key=lab.get)
print(f"  taxes mainly on labour: min {lab[lo]:.1f} ({lo}), max {lab[hi]:.1f} ({hi}); 2001-02 {lab['2001-02']:.1f}")
exl = {y: s(dd, "indiv_excl") for y, dd in allyrs.items() if "indiv_excl" in dd}
print(f"  individuals excl FBT: min {min(exl.values()):.1f} ({min(exl, key=exl.get)}), max {max(exl.values()):.1f} "
      f"({max(exl, key=exl.get)}); 2001-02 {exl['2001-02']:.1f}")
rec = {y: s(dd, "recurrent") for y, dd in allyrs.items()}
for nm, ser in (("taxes mainly on labour", lab), ("individuals excl FBT", exl), ("recurrent land + rates", rec)):
    a = [v for y, v in ser.items() if "2000-01" <= y <= "2009-10"]
    b = [v for y, v in ser.items() if "2015-16" <= y <= "2024-25"]
    print(f"  {nm}: mean 2000-01..2009-10 {sum(a) / len(a):.1f} ({len(a)} yrs) vs mean 2015-16..2024-25 {sum(b) / len(b):.1f} "
          f"({len(b)} yrs); endpoint change {ser['2024-25'] - ser['2000-01']:+.1f} pt, from 2001-02 {ser['2024-25'] - ser['2001-02']:+.1f} pt")

# ------------------------------------------------------------------ 3. US simple analog
fr = {}
for n in ("W055", "A061", "W054"):
    df = pd.read_csv(F[f"{n}.csv"])
    fr[n] = dict(zip(df.iloc[:, 0].str[:4], pd.to_numeric(df.iloc[:, 1], errors="coerce")))
us = (fr["W055"]["2025"] + fr["A061"]["2025"]) / (fr["W054"]["2025"] + fr["A061"]["2025"])
print(f"\n== US 2025: ({fr['W055']['2025']} + {fr['A061']['2025']}) / ({fr['W054']['2025']} + {fr['A061']['2025']}) = {us:.4f}")
compare("US simple analog", us, "US comparison", "2025 (calendar)", tol=0.0006)

# ------------------------------------------------------------------ 4. national accounts
g = grid_xlsx(F["na_t7.xlsx"], "Data1")
idrow = next(i for i, r in enumerate(g) if r[0] == "Series ID")
typerow = next(i for i, r in enumerate(g) if r[0] == "Series Type")
want = {"A2302401K": "coe", "A2302411R": "tfi", "A2302408A": "dw", "A2302410L": "gmi"}
cols = {want[v]: j for j, v in enumerate(g[idrow]) if v in want}
for k, j in cols.items():
    assert g[typerow][j] == "Original", (k, g[typerow][j])
recs = [dict(date=r[0], **{k: r[j] for k, j in cols.items()}) for r in g[idrow + 1:] if r[0] is not None]
q = pd.DataFrame(recs)
q["date"] = pd.to_datetime(q["date"])
q["fy"] = q["date"].dt.year.where(q["date"].dt.month <= 6, q["date"].dt.year + 1)
cnt = q.groupby("fy").size()
A = q.groupby("fy")[["coe", "tfi", "dw", "gmi"]].sum().loc[cnt[cnt == 4].index]
A.index = [f"{e - 1}-{str(e)[2:]}" for e in A.index]
share = 100 * A["coe"] / A["tfi"]
dws = 100 * A["dw"] / A["tfi"]
print(f"\n== labour share (Table 7 original, FY ending June), {A.index[0]} .. {A.index[-1]}")
api = pd.read_csv(F["ana_inc.csv"]) if "ana_inc.csv" in F else pd.read_csv(RAW / "ANA_INC_C_original_quarterly.csv")
api = api[(api["TSEST"] == 10) & (api["FREQ"] == "Q") & (api["MEASURE"] == "C")]


def apis(item, sector):
    x = api[(api["DATA_ITEM"] == item) & (api["SECTOR"] == sector)][["TIME_PERIOD", "OBS_VALUE"]].copy()
    x["fy"] = x["TIME_PERIOD"].str[:4].astype(int) + x["TIME_PERIOD"].str[-1].isin(["3", "4"]).astype(int)
    c = x.groupby("fy").size()
    out = x.groupby("fy")["OBS_VALUE"].sum().loc[c[c == 4].index]
    out.index = [f"{e - 1}-{str(e)[2:]}" for e in out.index]
    return out


api_share = 100 * apis("COE", "SSS") / apis("GPF", "SSS")
gap = (api_share - share).abs().max()
print(f"  Table 7 vs Data API, max gap in COE/TFI over {len(share)} years: {gap:.4f} pt")
if gap > 0.01:
    flag("Table 7 and Data API disagree on COE/TFI")
for y in ("1959-60", "1974-75", "2000-01", "2021-22", "2025-26"):
    compare("COE / TFI", share[y], "Compensation of employees as a share", y)
for y in ("1959-60", "1974-75", "2000-01", "2025-26"):
    compare("dwellings GOS / TFI", dws[y], "Gross operating surplus of dwellings", y)
for y in ("1974-75", "2000-01", "2025-26"):
    compare("COE / (TFI - GMI)", 100 * A["coe"][y] / (A["tfi"][y] - A["gmi"][y]), "Sensitivity: compensation", y)
srt = share.sort_values()
print(f"  peak {share.idxmax()} {share.max():.1f}; next highest {srt.index[-2]} {srt.iloc[-2]:.1f}")
print(f"  low  {share.idxmin()} {share.min():.1f}; next lowest {srt.index[1]} {srt.iloc[1]:.1f}")
print(f"  dwellings GOS share: max {dws.idxmax()} {dws.max():.1f}; 2019-20 {dws['2019-20']:.1f}; 2020-21 {dws['2020-21']:.1f};"
      f" 2024-25 {dws['2024-25']:.1f}; 2025-26 {dws['2025-26']:.1f}; 1959-60 {dws['1959-60']:.1f}")

# ------------------------------------------------------------------ 5. quotes on the fresh pages
print("\n== quotes on freshly downloaded pages")
Q = [("oecd.html", "the Australian social security system is highly income-tested, with spending being more targeted to the poor than any other OECD country"),
     ("oecd.html", "It also has the highest share of cash spending devoted to income-tested payments – nearly 80% of total benefit spending in 2012."),
     ("oecd.html", "The main non-income-tested spending relates to state government schemes of workers’ compensation and pensions for retired public servants."),
     ("oecd.html", "it has the highest level of spending on income-tested benefits of any OECD country – 6.5% of GDP in 2012"),
     ("oecd.html", "Peter Whiteford Alexandra Heron"),
     ("oecd.html", "7 November 2018"),
     ("dss_422.html", "The benefits income test applies to the following payments: jobseeker payment"),
     ("dss_422.html", "Last reviewed: 1 July 2026"),
     ("dss_423.html", "The following payments are affected by the benefits assets test: jobseeker payment"),
     ("dss_423.html", "The pensions assets test applies to all pensions."),
     ("dss_423.html", "Last reviewed: 12 August 2024"),
     ("dss_42110.html", "The pensions income test applies to all pensions. Pension entitlement is also assessed by the application of the pensions assets test."),
     ("dss_42110.html", "A age pension disability support pension, or carer payment."),
     ("dss_42110.html", "Last reviewed: 11 May 2026")]
for fn, quote in Q:
    ok = quote in flat(F[fn])
    print(f"  {'found  ' if ok else 'MISSING'} {fn}: {quote[:90]}")
    if not ok:
        flag(f"quote missing on {fn}: {quote[:60]}")

# ------------------------------------------------------------------ summary
print("\n== headline comparison (builder vs verifier)")
for claim, period, b, mine, ok in rows:
    print(f"  {'OK ' if ok else 'BAD'} {claim:45s} {period:16s} builder {b!s:>9}  verifier {mine:,.4f}")
n_bad = sum(1 for r in rows if not r[4])
print(f"\n{len(rows) - n_bad}/{len(rows)} headline values reproduced; {len(problems)} problem(s) flagged")
sys.exit(1 if problems else 0)
