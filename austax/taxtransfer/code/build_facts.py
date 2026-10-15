"""Australia's tax and transfer facts for the Austaxpolicy article (mirror of the paper's Appendix D table).

Reads only the vendored files in ../data/raw and writes ../out/facts.csv plus two supporting tables:
  out/tax_shares.csv      shares of all-levels taxation revenue, 2000-01, 2009-10, 2015-16 ... 2024-25
  out/income_shares.csv   compensation of employees and dwellings' gross operating surplus as shares of
                          total factor income, financial years 1959-60 ... 2025-26
Run (from austax/taxtransfer):  ..\\..\\venv\\Scripts\\python.exe -I code\\build_facts.py
"""
import csv
import html
import re
from pathlib import Path

import openpyxl
import pandas as pd
import xlrd

HERE = Path(__file__).resolve().parent.parent
RAW = HERE / "data" / "raw"
OUT = HERE / "out"
OUT.mkdir(exist_ok=True)

URL = {
    "tax2425_page": "https://www.abs.gov.au/statistics/economy/government/taxation-revenue-australia/2024-25",
    "tax2425_do001": "https://www.abs.gov.au/statistics/economy/government/taxation-revenue-australia/2024-25/55060DO001_202425.xlsx",
    "tax2425_do002": "https://www.abs.gov.au/statistics/economy/government/taxation-revenue-australia/2024-25/55060DO002_202425.xlsx",
    "tax0910_cube": "https://www.abs.gov.au/ausstats/subscriber.nsf/log?openagent&55060do001_200910.xls&5506.0&Data%20Cubes&4F1736E61FDD622CCA25786F0013D73C&0&2009-10&12.04.2011&Latest",
    "tax0910_page": "https://www.abs.gov.au/ausstats/abs@.nsf/Previousproducts/5506.0Main%20Features72009-10?opendocument&tabname=Summary&prodno=5506.0&issue=2009-10&num=&view=",
    "tax0506_page": "https://www.abs.gov.au/AUSSTATS/abs@.nsf/Lookup/5506.0Main+Features12005-06?OpenDocument",
    "na_t7": "https://www.abs.gov.au/statistics/economy/national-accounts/australian-national-accounts-national-income-expenditure-and-product/jun-2026/5206007_Income_From_GDP.xlsx",
    "oecd": "https://www.oecd.org/en/publications/the-future-of-social-protection_9789264306943-en/full-report/component-5.html",
    "dss_4213": "https://guides.dss.gov.au/social-security-guide/4/2/1/10",
    "dss_422": "https://guides.dss.gov.au/social-security-guide/4/2/2",
    "dss_423": "https://guides.dss.gov.au/social-security-guide/4/2/3",
    "fred": "https://fred.stlouisfed.org/graph/fredgraph.csv?id=",
}


# ---------------------------------------------------------------- readers
def xlsx_rows(path, sheet):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    return [list(r) for r in wb[sheet].iter_rows(values_only=True)]


def xls_rows(path, sheet):
    s = xlrd.open_workbook(path).sheet_by_name(sheet)
    return [s.row_values(i) for i in range(s.nrows)]


def year_header(rows):
    """Return (row index, {column: 'YYYY-YY'}) for the row holding the financial-year labels."""
    for i, r in enumerate(rows):
        cols = {j: str(v).strip() for j, v in enumerate(r) if isinstance(v, str) and re.fullmatch(r"\s*\d{4}-\d{2}\s*", v)}
        if len(cols) >= 5:
            return i, cols
    raise ValueError("no year header")


def row_values(rows, label, start=0, occurrence=1):
    """Values by financial year for the n-th row (from `start`) whose first cell equals `label`."""
    _, cols = year_header(rows)
    seen = 0
    for r in rows[start:]:
        if r and isinstance(r[0], str) and r[0].strip() == label:
            seen += 1
            if seen == occurrence:
                return {y: float(r[j]) for j, y in cols.items()}
    raise KeyError(label)


def page_lines(path):
    t = path.read_text(encoding="utf-8", errors="replace")
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", t, flags=re.S)
    txt = html.unescape(re.sub(r"<[^>]+>", "\n", t))
    return [ln.strip() for ln in txt.split("\n") if ln.strip()]


def page_text(path):
    return " ".join(page_lines(path))


def web_table(lines, anchor, label, years):
    """Read a row from an archived ABS web table: values follow the label one per line, '214 264' style."""
    i = lines.index(anchor)
    j = lines.index(label, i)
    vals = [float(v.replace(" ", "").replace("\xa0", "")) for v in lines[j + 1 : j + 1 + len(years)]]
    return dict(zip(years, vals))


facts = []


def fact(name, value, unit, period, url, series, how):
    facts.append(dict(fact=name, value=value, unit=unit, period=period, source_url=url, table_series_id=series,
                      quote_or_computation=how))


# ---------------------------------------------------------------- 1. taxation revenue, 2015-16 to 2024-25 (2024-25 release)
d2 = xlsx_rows(RAW / "55060DO002_202425.xlsx", "Table_2")
d1c = xlsx_rows(RAW / "55060DO001_202425.xlsx", "Table_1")
d1s = xlsx_rows(RAW / "55060DO001_202425.xlsx", "Table_10")

T = {}  # all levels, $m, by year
T["total"] = row_values(d2, "Total taxation revenue")
T["indiv_incl_fbt"] = row_values(d2, "Income taxes levied on individuals")
T["payroll_tax"] = row_values(d2, "Payroll taxes")
T["payroll_labour_total"] = row_values(d2, "Total taxes on employers payroll and labour force")
T["land_tax"] = row_values(d2, "Land taxes")
T["rates"] = row_values(d2, "Municipal rates")
T["gst"] = row_values(d2, "Goods and services tax (GST)")
T["pit"] = row_values(d1c, "Personal income tax")
T["medicare"] = row_values(d1c, "Government health insurance levy")
T["fbt"] = row_values(d1c, "Fringe benefits tax")
T["company"] = row_values(d1c, "Company income tax")
T["conveyances"] = row_values(d1s, "Stamp duties on conveyances")
years_new = list(T["total"].keys())
LATEST = years_new[-1]
assert LATEST == "2024-25", LATEST

for y in years_new:
    # (i) individuals' income tax excluding FBT = personal income tax + Medicare levy (ABS 'Government health insurance levy')
    T.setdefault("indiv_excl_fbt", {})[y] = T["pit"][y] + T["medicare"][y]
    # composite (i)+(ii)+(iii): ABS 'Income taxes levied on individuals' already includes FBT
    T.setdefault("labour_mainly", {})[y] = T["indiv_incl_fbt"][y] + T["payroll_labour_total"][y]
    T.setdefault("recurrent_land", {})[y] = T["land_tax"][y] + T["rates"][y]

# ---------------------------------------------------------------- 2. 2000-01 and 2009-10 (archived releases)
o1 = xls_rows(RAW / "55060do001_200910.xls", "Table_1")     # Commonwealth, 2000-01 .. 2009-10
o18 = xls_rows(RAW / "55060do001_200910.xls", "Table_18")   # all states, state and local, 2000-01 .. 2009-10
OLD = {}
OLD["indiv_incl_fbt"] = row_values(o1, "Total", occurrence=1)      # first 'Total' = income taxes levied on individuals
OLD["fbt"] = row_values(o1, "Fringe benefits tax")
OLD["company"] = row_values(o1, "Company income tax")
OLD["gst"] = row_values(o1, "Goods and services tax (GST)")
OLD["land_tax"] = row_values(o18, "Land taxes")
OLD["rates"] = row_values(o18, "Municipal rates")
OLD["conveyances"] = row_values(o18, "Stamp duties on conveyances")
for yy in ("2000-01", "2009-10"):   # components add to the 'Total' row up to ABS rounding
    assert abs(row_values(o1, "Personal income tax")[yy] + row_values(o1, "Prescribed payments by individuals")[yy]
               + OLD["fbt"][yy] - OLD["indiv_incl_fbt"][yy]) <= 2

# All-levels totals and payroll (net of intergovernmental taxes) come from the ABS web tables of the same era.
l0506 = page_lines(RAW / "5506.0_2005-06_main_features.html")
yrs0506 = ["2000-01", "2001-02", "2002-03", "2003-04", "2004-05", "2005-06"]
tot0506 = web_table(l0506, "ALL LEVELS OF GOVERNMENT", "Total taxation revenue", yrs0506)
pay0506 = web_table(l0506, "ALL LEVELS OF GOVERNMENT", "Employers' payroll taxes", yrs0506)
l0910 = page_lines(RAW / "5506.0_2009-10_main_features7_all_levels.html")
yrs0910 = ["2004-05", "2005-06", "2006-07", "2007-08", "2008-09", "2009-10"]
i_pay = l0910.index("Employers' payroll taxes")
pay0910 = web_table(l0910[i_pay:], "Employers' payroll taxes", "Total", yrs0910)
i_last = len(l0910) - 1 - l0910[::-1].index("Total")       # the grand total is the last 'Total' row
tot0910 = dict(zip(yrs0910, [float(v.replace(" ", "")) for v in l0910[i_last + 1 : i_last + 7]]))
for y, tot, pay in (("2000-01", tot0506, pay0506), ("2009-10", tot0910, pay0910)):
    T["total"][y] = tot[y]
    T["payroll_labour_total"][y] = pay[y]
    for k in ("indiv_incl_fbt", "fbt", "company", "gst", "land_tax", "rates", "conveyances"):
        T[k][y] = OLD[k][y]
    T["indiv_excl_fbt"][y] = OLD["indiv_incl_fbt"][y] - OLD["fbt"][y]
    T["labour_mainly"][y] = OLD["indiv_incl_fbt"][y] + pay[y]
    T["recurrent_land"][y] = OLD["land_tax"][y] + OLD["rates"][y]

# ---------------------------------------------------------------- 3. tax shares table
order = ["2000-01", "2009-10"] + years_new
items = ["indiv_excl_fbt", "fbt", "indiv_incl_fbt", "payroll_tax", "payroll_labour_total", "labour_mainly", "company",
         "gst", "land_tax", "rates", "recurrent_land", "conveyances"]
with open(OUT / "tax_shares.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["financial_year", "total_taxation_revenue_m"] + [f"{k}_m" for k in items] + [f"{k}_share" for k in items])
    for y in order:
        lv = [T[k].get(y) for k in items]
        w.writerow([y, T["total"][y]] + lv + [None if v is None else round(v / T["total"][y], 6) for v in lv])


def sh(k, y):
    return T[k][y] / T["total"][y]


def pct(x):
    return round(100 * x, 1)


y = LATEST
src_new = f"{URL['tax2425_do002']} ; {URL['tax2425_do001']}"
fact("Total taxation revenue, all levels of government", T["total"][y], "$m", y, URL["tax2425_do002"],
     "5506.0 2024-25, 55060DO002 Table 2 'Total taxation revenue'",
     "Release page: 'In the year 2024-25 across all levels of government, total taxation revenue was: $839.0 billion'")
fact("(i) Taxes on income of individuals (personal income tax + Medicare levy, excluding FBT), share of total",
     pct(sh("indiv_excl_fbt", y)), "% of total tax", y, src_new,
     "55060DO001 Table 1 rows 'Personal income tax' + 'Government health insurance levy'; denominator 55060DO002 Table 2",
     f"({T['pit'][y]:,.0f} + {T['medicare'][y]:,.0f}) / {T['total'][y]:,.0f}. Includes tax on individuals' capital income "
     "(interest, dividends, rent, capital gains) as well as on wages")
fact("(i') ABS category 'Income taxes levied on individuals' (includes FBT), share of total", pct(sh("indiv_incl_fbt", y)),
     "% of total tax", y, URL["tax2425_do002"], "55060DO002 Table 2 and Table 3 'Income taxes levied on individuals'",
     f"{T['indiv_incl_fbt'][y]:,.0f} / {T['total'][y]:,.0f}")
fact("(ii) Payroll taxes (state payroll tax), share of total", pct(sh("payroll_tax", y)), "% of total tax", y,
     URL["tax2425_do002"], "55060DO002 Table 2 'Payroll taxes'", f"{T['payroll_tax'][y]:,.0f} / {T['total'][y]:,.0f}")
fact("(ii') All taxes on employers' payroll and labour force (payroll tax + other, e.g. superannuation guarantee charge), share of total",
     pct(sh("payroll_labour_total", y)), "% of total tax", y, URL["tax2425_do002"],
     "55060DO002 Table 2 'Total taxes on employers payroll and labour force'",
     f"{T['payroll_labour_total'][y]:,.0f} / {T['total'][y]:,.0f}")
fact("(iii) Fringe benefits tax, share of total", pct(sh("fbt", y)), "% of total tax", y, URL["tax2425_do001"],
     "55060DO001 Table 1 'Fringe benefits tax'", f"{T['fbt'][y]:,.0f} / {T['total'][y]:,.0f}")
fact("Taxes mainly on labour = (i) + (ii') + (iii), share of total", pct(sh("labour_mainly", y)), "% of total tax", y,
     URL["tax2425_do002"], "55060DO002 Table 2 'Income taxes levied on individuals' + 'Total taxes on employers payroll and labour force'",
     f"({T['indiv_incl_fbt'][y]:,.0f} + {T['payroll_labour_total'][y]:,.0f}) / {T['total'][y]:,.0f}; with payroll tax only (ii): "
     f"{pct((T['indiv_incl_fbt'][y] + T['payroll_tax'][y]) / T['total'][y])}%. Upper side: (i) includes tax on capital income; "
     "lower side: no labour slice of GST, company tax or superannuation-fund tax is counted")
fact("(iv) Company income tax, share of total", pct(sh("company", y)), "% of total tax", y, URL["tax2425_do001"],
     "55060DO001 Table 1 'Company income tax' (excludes tax paid by superannuation funds)",
     f"{T['company'][y]:,.0f} / {T['total'][y]:,.0f}")
T["super_funds"] = row_values(d1c, "Income tax paid by superannuation funds")
fact("Not counted as labour: income tax paid by superannuation funds, share of total", pct(T["super_funds"][y] / T["total"][y]),
     "% of total tax", y, URL["tax2425_do001"], "55060DO001 Table 1 'Income tax paid by superannuation funds'",
     f"{T['super_funds'][y]:,.0f} / {T['total'][y]:,.0f}. Part of this taxes employer contributions paid on wages, part taxes fund earnings")
fact("(v) Goods and services tax, share of total", pct(sh("gst", y)), "% of total tax", y, URL["tax2425_do002"],
     "55060DO002 Table 2 'Goods and services tax (GST)'", f"{T['gst'][y]:,.0f} / {T['total'][y]:,.0f}")
fact("(vi) Land taxes, share of total", pct(sh("land_tax", y)), "% of total tax", y, URL["tax2425_do002"],
     "55060DO002 Table 2 'Land taxes'", f"{T['land_tax'][y]:,.0f} / {T['total'][y]:,.0f}")
fact("(vi) Municipal rates, share of total", pct(sh("rates", y)), "% of total tax", y, URL["tax2425_do002"],
     "55060DO002 Table 2 'Municipal rates'", f"{T['rates'][y]:,.0f} / {T['total'][y]:,.0f}")
fact("Recurrent taxes on land = land taxes + municipal rates, share of total", pct(sh("recurrent_land", y)), "% of total tax",
     y, URL["tax2425_do002"], "55060DO002 Table 2 'Land taxes' + 'Municipal rates'",
     f"({T['land_tax'][y]:,.0f} + {T['rates'][y]:,.0f}) / {T['total'][y]:,.0f}. Rates are levied on land or on land plus buildings, depending on the council")
fact("(vii) Stamp duties on conveyances (property transfers), share of total", pct(sh("conveyances", y)), "% of total tax", y,
     URL["tax2425_do001"], "55060DO001 Table 10 'Stamp duties on conveyances' (state and local, before netting intergovernmental taxes)",
     f"{T['conveyances'][y]:,.0f} / {T['total'][y]:,.0f}")

# history
src_old = f"{URL['tax0910_cube']} ; {URL['tax0506_page']} ; {URL['tax0910_page']}"
for k, label in (("indiv_excl_fbt", "(i) Taxes on income of individuals excluding FBT"),
                 ("indiv_incl_fbt", "(i') ABS 'Income taxes levied on individuals' (includes FBT)"),
                 ("recurrent_land", "Recurrent taxes on land (land taxes + municipal rates)"),
                 ("labour_mainly", "Taxes mainly on labour (i)+(ii')+(iii)")):
    for yy in ("2000-01", "2009-10", "2015-16"):
        fact(f"{label}, share of total (history)", pct(sh(k, yy)), "% of total tax", yy,
             src_old if yy != "2015-16" else URL["tax2425_do002"],
             "2000-01/2009-10: 55060do001_200910 Tables 1 and 18 over the all-levels total of the 5506.0 2005-06 / 2009-10 web tables; "
             "2015-16: 2024-25 release" if yy != "2015-16" else "55060DO001/DO002 2024-25 release",
             f"{T[k][yy]:,.0f} / {T['total'][yy]:,.0f}")

# US comparison on the same simple definition (FRED, BEA NIPA, calendar 2025)
fred = {}
for sid in ("W055RC1A027NBEA", "A061RC1A027NBEA", "W054RC1A027NBEA"):
    s = pd.read_csv(RAW / f"FRED_{sid}.csv")
    s["year"] = s["observation_date"].str[:4].astype(int)
    fred[sid] = dict(zip(s["year"], s[sid]))
us = (fred["W055RC1A027NBEA"][2025] + fred["A061RC1A027NBEA"][2025]) / (fred["W054RC1A027NBEA"][2025] + fred["A061RC1A027NBEA"][2025])
fact("US comparison: (personal current taxes + social insurance contributions) / (current tax receipts + contributions)",
     round(us, 3), "share", "2025 (calendar)", URL["fred"] + "W055RC1A027NBEA ; A061RC1A027NBEA ; W054RC1A027NBEA",
     "BEA NIPA via FRED: W055RC1A027NBEA, A061RC1A027NBEA, W054RC1A027NBEA",
     f"({fred['W055RC1A027NBEA'][2025]:,.1f} + {fred['A061RC1A027NBEA'][2025]:,.1f}) / ({fred['W054RC1A027NBEA'][2025]:,.1f} + "
     f"{fred['A061RC1A027NBEA'][2025]:,.1f}) $bn. Same simple definition as the Australian 'taxes mainly on labour'; "
     "the paper's 0.68 is a different, model-based construction")

# ---------------------------------------------------------------- 4. labour's share of income (5206.0 Table 7, original, $m)
na = xlsx_rows(RAW / "5206007_Income_From_GDP.xlsx", "Data1")
ids = na[9]
col = {sid: ids.index(sid) for sid in ("A2302401K", "A2302411R", "A2302408A", "A2302410L", "A2302409C")}
q = pd.DataFrame([{**{"date": r[0]}, **{sid: r[c] for sid, c in col.items()}} for r in na[10:] if r[0] is not None])
q["date"] = pd.to_datetime(q["date"])
q["fy_end"] = q["date"].dt.year + (q["date"].dt.month >= 7).astype(int)    # quarter ending Sep..Jun -> FY ending June
g = q.groupby("fy_end")
fy = g[list(col)].sum()[g.size() == 4]
fy = fy.rename(columns={"A2302401K": "coe", "A2302411R": "tfi", "A2302408A": "gos_dwellings", "A2302410L": "gmi", "A2302409C": "gos_all"})
fy["coe_share_tfi"] = fy["coe"] / fy["tfi"]
fy["gos_dwellings_share_tfi"] = fy["gos_dwellings"] / fy["tfi"]
fy["coe_share_tfi_excl_gmi"] = fy["coe"] / (fy["tfi"] - fy["gmi"])
fy.index = [f"{e - 1}-{str(e)[2:]}" for e in fy.index]
fy.index.name = "financial_year"
fy.round(6).to_csv(OUT / "income_shares.csv")
LAST_FY = fy.index[-1]
assert LAST_FY == "2025-26", LAST_FY
peak = fy["coe_share_tfi"].idxmax()
low = fy["coe_share_tfi"].idxmin()
for yy in dict.fromkeys(("1959-60", "1974-75", "2000-01", LAST_FY, peak, low)):   # ordered, no duplicates
    fact("Compensation of employees as a share of total factor income", pct(fy.loc[yy, "coe_share_tfi"]), "%", yy, URL["na_t7"],
         "5206.0 Jun 2026 Table 7, original: A2302401K / A2302411R, sum of four quarters (financial year ending June)",
         f"{fy.loc[yy, 'coe']:,.0f} / {fy.loc[yy, 'tfi']:,.0f}" + (" (series peak)" if yy == peak else "") + (" (series low)" if yy == low else ""))
for yy in ("1959-60", "1974-75", "2000-01", LAST_FY):
    fact("Gross operating surplus of dwellings owned by persons as a share of total factor income",
         pct(fy.loc[yy, "gos_dwellings_share_tfi"]), "%", yy, URL["na_t7"],
         "5206.0 Jun 2026 Table 7, original: A2302408A / A2302411R, sum of four quarters",
         f"{fy.loc[yy, 'gos_dwellings']:,.0f} / {fy.loc[yy, 'tfi']:,.0f}. Actual and imputed rent less running costs, before interest and depreciation")
for yy in ("1974-75", "2000-01", LAST_FY):
    fact("Sensitivity: compensation of employees / (total factor income less gross mixed income)",
         pct(fy.loc[yy, "coe_share_tfi_excl_gmi"]), "%", yy, URL["na_t7"],
         "5206.0 Jun 2026 Table 7, original: A2302401K / (A2302411R - A2302410L)",
         f"{fy.loc[yy, 'coe']:,.0f} / ({fy.loc[yy, 'tfi']:,.0f} - {fy.loc[yy, 'gmi']:,.0f}); treats mixed income as split like the rest")

# ---------------------------------------------------------------- 5. means testing (quotes from vendored pages)
QUOTES = [
    ("OECD (Whiteford and Heron chapter): targeting of Australian social security", "oecd_2018_future_social_protection_ch2_australia.html",
     URL["oecd"], "OECD (2018) The Future of Social Protection, ch. 2 'Australia: Providing social protection to non-standard workers with tax financing' (P. Whiteford, A. Heron), published 7 November 2018, doi 10.1787/9789264306943-en",
     "the Australian social security system is highly income-tested, with spending being more targeted to the poor than any other OECD country", "2018 (publication)"),
    ("OECD: share of cash benefit spending that is income-tested", "oecd_2018_future_social_protection_ch2_australia.html", URL["oecd"],
     "same chapter, section on the Australian system",
     "It also has the highest share of cash spending devoted to income-tested payments – nearly 80% of total benefit spending in 2012.", "2012"),
    ("OECD: what the non-income-tested remainder is", "oecd_2018_future_social_protection_ch2_australia.html", URL["oecd"],
     "same chapter, note 3",
     "The main non-income-tested spending relates to state government schemes of workers’ compensation and pensions for retired public servants.", "2012"),
    ("OECD: income-tested spending as share of GDP", "oecd_2018_future_social_protection_ch2_australia.html", URL["oecd"], "same chapter",
     "it has the highest level of spending on income-tested benefits of any OECD country – 6.5% of GDP in 2012", "2012"),
    ("DSS: JobSeeker Payment is income tested", "dss_ssguide_4.2.2_benefits_income_test.html", URL["dss_422"],
     "DSS Social Security Guide 4.2.2 'Benefits income test & limits', last reviewed 1 July 2026",
     "The benefits income test applies to the following payments: jobseeker payment", "2026"),
    ("DSS: JobSeeker Payment is assets tested", "dss_ssguide_4.2.3_assets_tests.html", URL["dss_423"],
     "DSS Social Security Guide 4.2.3 'Pensions & benefits assets tests', last reviewed 12 August 2024",
     "The following payments are affected by the benefits assets test: jobseeker payment", "2024"),
    ("DSS: Age Pension is income tested", "dss_ssguide_4.2.1.10_pensions_income_test.html", URL["dss_4213"],
     "DSS Social Security Guide 4.2.1.10 'Pensions income test', last reviewed 11 May 2026 (rate calculator A: age pension)",
     "The pensions income test applies to all pensions. Pension entitlement is also assessed by the application of the pensions assets test.", "2026"),
    ("DSS: Age Pension is assets tested", "dss_ssguide_4.2.3_assets_tests.html", URL["dss_423"],
     "DSS Social Security Guide 4.2.3 'Pensions & benefits assets tests', last reviewed 12 August 2024",
     "The pensions assets test applies to all pensions.", "2024"),
]
for name, fname, url, ident, quote, period in QUOTES:
    txt = re.sub(r"\s+", " ", page_text(RAW / fname))
    assert re.sub(r"\s+", " ", quote) in txt, (fname, quote[:60])
    fact(name, "quote", "text", period, url, ident, f'"{quote}"')

with open(OUT / "facts.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(facts[0]))
    w.writeheader()
    w.writerows(facts)

print(f"latest tax year {LATEST}: total {T['total'][LATEST]:,.0f} $m")
for k in items:
    print(f"  {k:22s} " + "  ".join(f"{yy}:{pct(sh(k, yy)) if T[k].get(yy) is not None else '':>5}" for yy in ("2000-01", "2009-10", "2015-16", LATEST)))
print(f"US simple analog 2025: {us:.3f}")
print(f"income shares {LAST_FY}: COE/TFI {pct(fy.loc[LAST_FY, 'coe_share_tfi'])}%, dwellings GOS/TFI {pct(fy.loc[LAST_FY, 'gos_dwellings_share_tfi'])}%;"
      f" 1974-75 {pct(fy.loc['1974-75', 'coe_share_tfi'])}%, 2000-01 {pct(fy.loc['2000-01', 'coe_share_tfi'])}%, peak {peak}, low {low}")
print(f"wrote {len(facts)} facts to {OUT / 'facts.csv'}")
