"""Independent checks for austax/taxtransfer. Re-reads the raw files by a different route from build_facts.py,
recomputes every headline number, compares with out/facts.csv and with ABS-published shares, prints PASS/FAIL.

Different routes: spreadsheets via pandas.read_excel (build uses openpyxl/xlrd row scans); labour share from the ABS
Data API CSV (build uses the 5206.0 Table 7 spreadsheet); pages via html.parser (build uses regex stripping).
Run (from austax/taxtransfer):  ..\\..\\venv\\Scripts\\python.exe -I checks\\check_facts.py
"""
import csv
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent.parent
RAW = HERE / "data" / "raw"
results = []


def check(name, ok, detail=""):
    results.append((name, bool(ok)))
    print(("PASS " if ok else "FAIL ") + name + (f"  [{detail}]" if detail else ""))


class Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts, self.skip = [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self.skip:
            self.skip -= 1

    def handle_data(self, data):
        if not self.skip and data.strip():
            self.parts.append(data.strip())


def page(fname):
    p = Text()
    p.feed((RAW / fname).read_text(encoding="utf-8", errors="replace"))
    return p.parts


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


facts = list(csv.DictReader(open(HERE / "out" / "facts.csv", encoding="utf-8")))


def fv(prefix, period):
    hits = [f for f in facts if f["fact"].startswith(prefix) and f["period"] == period]
    assert len(hits) == 1, (prefix, period, len(hits))
    return float(hits[0]["value"])


# ------------------------------------------------------------------ 1. taxation revenue 2024-25
def table(fname, sheet):
    df = pd.read_excel(RAW / fname, sheet_name=sheet, header=None)
    hdr = next(i for i in range(len(df)) if str(df.iloc[i, 1]).strip() == "2015-16")
    df.columns = ["label"] + [str(c).strip() for c in df.iloc[hdr, 1:]]
    df["label"] = df["label"].astype(str).str.strip()
    return df.iloc[hdr + 2:]


def get(df, label, year="2024-25", nth=0):
    return float(df.loc[df["label"] == label, year].iloc[nth])


t2 = table("55060DO002_202425.xlsx", "Table_2")
t3 = table("55060DO002_202425.xlsx", "Table_3")     # ABS-published distribution (proportions)
t5 = table("55060DO002_202425.xlsx", "Table_5")
c1 = table("55060DO001_202425.xlsx", "Table_1")
s10 = table("55060DO001_202425.xlsx", "Table_10")

total = get(t5, "Total all levels of government")
check("total 2024-25 = 838,974 $m in Table 5 and Table 2", total == 838974 == get(t2, "Total taxation revenue"), f"{total:,.0f}")
rel = norm(" ".join(page("5506.0_2024-25_release_page.html")))
check("release page states $839.0 billion for 2024-25", "total taxation revenue was: $839.0 billion" in rel)
check("facts total equals Table 5", fv("Total taxation revenue", "2024-25") == total)

pit, med, fbt = get(c1, "Personal income tax"), get(c1, "Government health insurance levy"), get(c1, "Fringe benefits tax")
indiv_t2 = get(t2, "Income taxes levied on individuals")
check("Commonwealth individuals' components add to all-levels category (+-2 rounding)", abs(pit + med + fbt - indiv_t2) <= 2,
      f"{pit + med + fbt:,.0f} vs {indiv_t2:,.0f}")
payroll = get(t2, "Payroll taxes")
payroll_all = get(t2, "Total taxes on employers payroll and labour force")
land, rates = get(t2, "Land taxes"), get(t2, "Municipal rates")
company, gst = get(c1, "Company income tax"), get(t2, "Goods and services tax (GST)")
conv = get(s10, "Stamp duties on conveyances")

recomputed = {
    "(i) Taxes on income of individuals": (pit + med) / total,
    "(i') ABS category": indiv_t2 / total,
    "(ii) Payroll taxes": payroll / total,
    "(ii') All taxes on employers": payroll_all / total,
    "(iii) Fringe benefits tax": fbt / total,
    "Taxes mainly on labour = ": (pit + med + fbt + payroll_all) / total,
    "(iv) Company income tax": company / total,
    "(v) Goods and services tax": gst / total,
    "(vi) Land taxes": land / total,
    "(vi) Municipal rates": rates / total,
    "Recurrent taxes on land = ": (land + rates) / total,
    "(vii) Stamp duties on conveyances": conv / total,
    "Not counted as labour: income tax paid by superannuation funds": get(c1, "Income tax paid by superannuation funds") / total,
}
for k, v in recomputed.items():
    got = fv(k, "2024-25")
    check(f"2024-25 {k.strip(' =')} recomputed {100 * v:.2f}% vs facts {got}", abs(round(100 * v, 1) - got) < 1e-9)

abs_pub = {  # ABS Table 3 proportions vs our shares
    "Income taxes levied on individuals": indiv_t2 / total,
    "Payroll taxes": payroll / total,
    "Total taxes on employers payroll and labour force": payroll_all / total,
    "Land taxes": land / total,
    "Municipal rates": rates / total,
    "Goods and services tax (GST)": gst / total,
}
for k, v in abs_pub.items():
    pub = get(t3, k)
    check(f"ABS Table 3 published share '{k}' {100 * pub:.2f}% matches", abs(pub - v) < 5e-5)

# ------------------------------------------------------------------ 2. history: 2000-01 and 2009-10, and the seams
o1 = pd.read_excel(RAW / "55060do001_200910.xls", sheet_name="Table_1", header=None, engine="xlrd")
o18 = pd.read_excel(RAW / "55060do001_200910.xls", sheet_name="Table_18", header=None, engine="xlrd")
for df in (o1, o18):
    df.columns = ["label"] + [str(c).strip() for c in df.iloc[4, 1:]]
    df["label"] = df["label"].astype(str).str.strip()


def oget(df, label, year, nth=0):
    return float(df.loc[df["label"] == label, year].iloc[nth])


p06 = page("5506.0_2005-06_main_features.html")
p10 = page("5506.0_2009-10_main_features7_all_levels.html")


def after(parts, anchor, label, n, start_at=0):
    i = parts.index(anchor, start_at)
    j = parts.index(label, i)
    return [float(x.replace(" ", "").replace("\xa0", "")) for x in parts[j + 1 : j + 1 + n]]


tot01 = after(p06, "ALL LEVELS OF GOVERNMENT", "Total taxation revenue", 6)[0]
pay01 = after(p06, "ALL LEVELS OF GOVERNMENT", "Employers' payroll taxes", 6)[0]
check("2000-01 all-levels total 214,264 (5506.0 2005-06)", tot01 == 214264)
indiv_pub01 = after(p06, "MAJOR COMPONENTS OF TOTAL TAXATION, All levels of government", "Income taxes levied on individuals", 6)[0]
immov_pub01 = after(p06, "MAJOR COMPONENTS OF TOTAL TAXATION, All levels of government", "Taxes on immovable property", 6)[0]
gpay_pub01 = after(p06, "MAJOR COMPONENTS OF TOTAL TAXATION, All levels of government", "General taxes (payroll tax)", 6)[0]
opay_pub01 = after(p06, "MAJOR COMPONENTS OF TOTAL TAXATION, All levels of government", "Other employers labour force taxes", 6)[0]

ind01 = oget(o1, "Total", "2000-01", 0)
fbt01 = oget(o1, "Fringe benefits tax", "2000-01")
land01 = oget(o18, "Land taxes", "2000-01") + oget(o18, "Municipal rates", "2000-01")
immov01 = land01 + oget(o18, "Other", "2000-01", 0)
check(f"2000-01 individuals' share {100 * ind01 / tot01:.2f}% matches ABS-published {indiv_pub01}% (2005-06 release)",
      abs(100 * ind01 / tot01 - indiv_pub01) <= 0.05)
check(f"2000-01 payroll share {100 * pay01 / tot01:.2f}% matches ABS-published {gpay_pub01}+{opay_pub01}%",
      abs(100 * pay01 / tot01 - (gpay_pub01 + opay_pub01)) <= 0.1)
check(f"2000-01 land+rates+other {100 * immov01 / tot01:.2f}% vs ABS-published immovable property {immov_pub01}% (vintage/netting seam <= 0.1 pp)",
      abs(100 * immov01 / tot01 - immov_pub01) <= 0.1)
check("facts 2000-01 (i) excl FBT", fv("(i) Taxes on income of individuals excluding FBT", "2000-01") == round(100 * (ind01 - fbt01) / tot01, 1))
check("facts 2000-01 (i') incl FBT", fv("(i') ABS 'Income taxes levied", "2000-01") == round(100 * ind01 / tot01, 1))
check("facts 2000-01 recurrent land", fv("Recurrent taxes on land (land taxes", "2000-01") == round(100 * land01 / tot01, 1))
check("facts 2000-01 taxes mainly on labour", fv("Taxes mainly on labour (i)", "2000-01") == round(100 * (ind01 + pay01) / tot01, 1))

i_pay = p10.index("Employers' payroll taxes")
pay10 = after(p10, "Employers' payroll taxes", "Total", 6, start_at=i_pay)[-1]
tot10 = [float(x.replace(" ", "")) for x in p10[len(p10) - 1 - p10[::-1].index("Total") + 1:][:6]][-1]
ind10_page = after(p10, "TAXATION, All levels of Government", "Income taxes levied on individuals", 6)[-1]
ind10 = oget(o1, "Total", "2009-10", 0)
land10 = oget(o18, "Land taxes", "2009-10") + oget(o18, "Municipal rates", "2009-10")
check("2009-10 total 332,602 and payroll 16,744 read from the 2009-10 web table", (tot10, pay10) == (332602, 16744))
check("2009-10 individuals: cube Table 1 equals web all-levels table (same release)", ind10 == ind10_page == 124784)
check("facts 2009-10 recurrent land", fv("Recurrent taxes on land (land taxes", "2009-10") == round(100 * land10 / tot10, 1))
check("facts 2009-10 (i') incl FBT", fv("(i') ABS 'Income taxes levied", "2009-10") == round(100 * ind10 / tot10, 1))

# seams between releases (revision size, reported; asserted small)
tot0506_a = after(p06, "ALL LEVELS OF GOVERNMENT", "Total taxation revenue", 6)[-1]          # 2005-06 in 2005-06 release
tot0506_b = [float(x.replace(" ", "")) for x in p10[len(p10) - 1 - p10[::-1].index("Total") + 1:][:6]][1]  # in 2009-10 release
check(f"seam: 2005-06 all-levels total revised {tot0506_a:,.0f} -> {tot0506_b:,.0f} ({100 * (tot0506_b / tot0506_a - 1):+.2f}%), |rev| < 0.5%",
      abs(tot0506_b / tot0506_a - 1) < 0.005)
c15 = table("55060DO001_202425.xlsx", "Table_1")
ind15 = get(t2, "Income taxes levied on individuals", "2015-16")
check("2015-16 individuals in 2024-25 release: DO001 components = DO002 category (+-2)",
      abs(get(c15, "Personal income tax", "2015-16") + get(c15, "Government health insurance levy", "2015-16")
          + get(c15, "Fringe benefits tax", "2015-16") - ind15) <= 2)

# ------------------------------------------------------------------ 3. US simple analog
fr = {}
for sid in ("W055RC1A027NBEA", "A061RC1A027NBEA", "W054RC1A027NBEA"):
    rows = list(csv.reader(open(RAW / f"FRED_{sid}.csv")))
    fr[sid] = {r[0][:4]: float(r[1]) for r in rows[1:] if r[1] not in ("", ".")}
us = (fr["W055RC1A027NBEA"]["2025"] + fr["A061RC1A027NBEA"]["2025"]) / (fr["W054RC1A027NBEA"]["2025"] + fr["A061RC1A027NBEA"]["2025"])
check(f"US 2025 simple analog {us:.4f} equals facts", round(us, 3) == fv("US comparison", "2025 (calendar)"))

# ------------------------------------------------------------------ 4. labour share from the ABS Data API (independent of Table 7 xlsx)
api = pd.read_csv(RAW / "ANA_INC_C_original_quarterly.csv")
api = api[(api["MEASURE"] == "C") & (api["TSEST"] == 10) & (api["FREQ"] == "Q")]


def series(item, sector):
    s = api[(api["DATA_ITEM"] == item) & (api["SECTOR"] == sector)].set_index("TIME_PERIOD")["OBS_VALUE"]
    return s


def fy_sum(s):
    yr = s.index.str[:4].astype(int)
    qn = s.index.str[-1].astype(int)
    fyend = yr + (qn >= 3).astype(int)          # Q3 (Sep) and Q4 (Dec) belong to the FY ending next June
    g = pd.Series(s.values, index=fyend).groupby(level=0)
    out = g.sum()[g.count() == 4]
    out.index = [f"{e - 1}-{str(e)[2:]}" for e in out.index]
    return out


coe, tfi = fy_sum(series("COE", "SSS")), fy_sum(series("GPF", "SSS"))
gos, gmi, dw = fy_sum(series("GOS", "SSS")), fy_sum(series("GMI", "SSS")), fy_sum(series("GOS", "PHD"))
check("national accounts identity: total factor income = COE + GOS + GMI, every financial year (+-3 $m)",
      (coe + gos + gmi - tfi).abs().max() <= 3, f"max gap {(coe + gos + gmi - tfi).abs().max():.0f}")
check("latest complete financial year in API is 2025-26", coe.index[-1] == "2025-26")
share = coe / tfi
for yy in ("1959-60", "1974-75", "2000-01", "2025-26", "2021-22"):
    check(f"COE/TFI {yy} API {100 * share[yy]:.2f}% vs facts", round(100 * share[yy], 1) == fv("Compensation of employees as a share", yy))
check("COE/TFI peak year is 1974-75 and low year is 2021-22 (API)", share.idxmax() == "1974-75" and share.idxmin() == "2021-22")
for yy in ("1959-60", "1974-75", "2000-01", "2025-26"):
    check(f"dwellings GOS/TFI {yy} API {100 * dw[yy] / tfi[yy]:.2f}% vs facts",
          round(100 * dw[yy] / tfi[yy], 1) == fv("Gross operating surplus of dwellings", yy))
for yy in ("1974-75", "2000-01", "2025-26"):
    check(f"COE/(TFI-GMI) {yy} API vs facts", round(100 * coe[yy] / (tfi[yy] - gmi[yy]), 1) == fv("Sensitivity: compensation", yy))
inc = pd.read_csv(HERE / "out" / "income_shares.csv", index_col=0)
common = inc.index.intersection(share.index)
check(f"Table 7 spreadsheet and Data API agree on COE/TFI in all {len(common)} financial years (< 0.01 pp)",
      (inc.loc[common, "coe_share_tfi"] - share[common]).abs().max() < 1e-4)

# ------------------------------------------------------------------ 5. quotes re-found in the vendored pages
for f in facts:
    if f["value"] != "quote":
        continue
    q = norm(f["quote_or_computation"].strip('"'))
    by_url = {"https://www.oecd.org/en/publications/the-future-of-social-protection_9789264306943-en/full-report/component-5.html":
              "oecd_2018_future_social_protection_ch2_australia.html",
              "https://guides.dss.gov.au/social-security-guide/4/2/2": "dss_ssguide_4.2.2_benefits_income_test.html",
              "https://guides.dss.gov.au/social-security-guide/4/2/3": "dss_ssguide_4.2.3_assets_tests.html",
              "https://guides.dss.gov.au/social-security-guide/4/2/1/10": "dss_ssguide_4.2.1.10_pensions_income_test.html"}
    txt = norm(" ".join(page(by_url[f["source_url"]])))
    check(f"quote found verbatim: {f['fact']}", q in txt)
dates = {"dss_ssguide_4.2.2_benefits_income_test.html": "Last reviewed: 1 July 2026",
         "dss_ssguide_4.2.3_assets_tests.html": "Last reviewed: 12 August 2024",
         "dss_ssguide_4.2.1.10_pensions_income_test.html": "Last reviewed: 11 May 2026",
         "oecd_2018_future_social_protection_ch2_australia.html": "7 November 2018"}
for fn, d in dates.items():
    check(f"date on page {fn}: '{d}'", d in norm(" ".join(page(fn))))
check("DSS 4.2.1.10: rate calculator A covers age pension", "A age pension disability support pension, or carer payment" in norm(" ".join(page("dss_ssguide_4.2.1.10_pensions_income_test.html"))))

n_fail = sum(1 for _, ok in results if not ok)
print(f"\n{len(results) - n_fail}/{len(results)} checks passed -> {'PASS' if n_fail == 0 else 'FAIL'}")
sys.exit(1 if n_fail else 0)
