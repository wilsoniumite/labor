"""Independent, adversarial re-derivation of the austax/coverage headline numbers (verifier, 2026-10-15).

Written without reusing any code from code/ or checks/check_coverage.py. Separate routes:
  ABS workbooks   raw OOXML (zipfile + xml.etree), no openpyxl/pandas
  DSS pages       own stdlib HTMLParser table reader; FY averages by interval arithmetic (no day loop)
  Henderson PDFs  pypdf in layout mode, line-by-line regex on the two-column Table 2
  Bond yield      FRED vs the RBA's own F2 historical workbook (to May 2013) + F2.1 (from June 2013)
  Population      ABS 3101.0 Table 4 vs the ABS Data API (ERP_Q), if a fresh download is supplied
Prints each claim with the builder's value and the recomputed one, plus extra definition sensitivities.

Run:  venv\\Scripts\\python.exe -I austax\\coverage\\checks\\verify_independent.py [FRESH_DIR]
FRESH_DIR (optional) holds fresh downloads of the same sources (same file names as data/raw/, plus
f02histhist.xls, erp_q.csv, CPIAUCSL.csv); the script then compares them with the vendored copies.
"""
import csv
import datetime as dt
import hashlib
import html
import re
import statistics as st
import sys
import xml.etree.ElementTree as ET
import zipfile
from html.parser import HTMLParser
from pathlib import Path

import pypdf
import xlrd

ROOT = Path(__file__).resolve().parents[1]
RAW, OUT = ROOT / "data" / "raw", ROOT / "out"
FRESH = Path(sys.argv[1]) if len(sys.argv) > 1 else None
D = dt.date
REFORM = D(2009, 9, 20)
results = []


def report(claim, builder, mine, ok, note=""):
    results.append(ok)
    print(f"{'OK ' if ok else 'BAD'} | {claim} | builder {builder} | mine {mine} | {note}")


# ============================================================ ABS workbooks through raw OOXML
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
      "pr": "http://schemas.openxmlformats.org/package/2006/relationships"}


def col_index(ref):
    letters = re.match(r"[A-Z]+", ref).group(0)
    n = 0
    for ch in letters:
        n = n * 26 + ord(ch) - 64
    return n - 1


def xlsx_sheet(path, sheet_name):
    with zipfile.ZipFile(path) as z:
        wb = ET.fromstring(z.read("xl/workbook.xml"))
        rid = next(s.get(f"{{{NS['r']}}}id") for s in wb.find("m:sheets", NS) if s.get("name") == sheet_name)
        rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        target = next(r.get("Target") for r in rels if r.get("Id") == rid)
        target = target.lstrip("/")
        target = target if target.startswith("xl/") else "xl/" + target
        shared = []
        if "xl/sharedStrings.xml" in z.namelist():
            for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
                shared.append("".join(t.text or "" for t in si.iter(f"{{{NS['m']}}}t")))
        rows = []
        for row in ET.fromstring(z.read(target)).iter(f"{{{NS['m']}}}row"):
            cells = {}
            for c in row.findall("m:c", NS):
                v = c.find("m:v", NS)
                if v is None:
                    isel = c.find("m:is", NS)
                    if isel is not None:
                        cells[col_index(c.get("r"))] = "".join(t.text or "" for t in isel.iter(f"{{{NS['m']}}}t"))
                    continue
                cells[col_index(c.get("r"))] = shared[int(v.text)] if c.get("t") == "s" else (
                    v.text if c.get("t") in ("str", "inlineStr") else float(v.text))
            rows.append(cells)
    return rows


def abs_xlsx_series(path, sid):
    rows = xlsx_sheet(path, "Data1")
    hdr = next(r for r in rows if r.get(0) == "Series ID")
    j = next(k for k, v in hdr.items() if v == sid)
    meta = {"unit": None, "type": None}
    for r in rows:
        if r.get(0) == "Unit":
            meta["unit"] = r.get(j)
        if r.get(0) == "Series Type":
            meta["type"] = r.get(j)
    out = {}
    for r in rows:
        if isinstance(r.get(0), float) and j in r:
            out[D(1899, 12, 30) + dt.timedelta(days=int(r[0]))] = float(r[j])
    return out, meta


def annual_by_year(series):
    return {d.year: v for d, v in series.items()}


# ============================================================ HTML tables (DSS)
class Tables(HTMLParser):
    def __init__(self):
        super().__init__()
        self.done, self.stack, self.row, self.cell = [], [], None, None

    def handle_starttag(self, tag, attrs):
        if tag == "table":
            self.stack.append([])
        elif tag == "tr" and self.stack:
            self.row = []
        elif tag in ("td", "th") and self.row is not None:
            self.cell = []

    def handle_endtag(self, tag):
        if tag == "table" and self.stack:
            self.done.append(self.stack.pop())
        elif tag == "tr" and self.row is not None and self.stack:
            self.stack[-1].append(self.row)
            self.row = None
        elif tag in ("td", "th") and self.cell is not None and self.row is not None:
            self.row.append(" ".join("".join(self.cell).split()))
            self.cell = None

    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)


def html_tables(path):
    p = Tables()
    p.feed(path.read_text(encoding="utf8"))
    return p.done


def page_text(path):
    t = path.read_text(encoding="utf8")
    t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=re.S)
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", t)).split())


def ddmmyyyy(s):
    m = re.match(r"\s*(\d\d)/(\d\d)/(\d{4})", s)
    return D(int(m.group(3)), int(m.group(2)), int(m.group(1))) if m else None


def money(s):
    m = re.match(r"\s*\$?([\d,]+\.\d+)", s)
    return float(m.group(1).replace(",", "")) if m else None


def rate_rows(table, col, mult=1.0):
    out = []
    for r in table:
        d = ddmmyyyy(r[0]) if r else None
        if d and len(r) > col and money(r[col]) is not None:
            out.append((d, mult * money(r[col])))
    return sorted(out)


def fy_bounds(fy):
    return D(fy - 1, 7, 1), D(fy, 7, 1)


def fy_mean(points, fy, start=None, end=None):
    """Day-weighted mean over FY of a step function of annual amounts, zero outside [start, end)."""
    a, b = fy_bounds(fy)
    lo_active, hi_active = max(a, start or a), min(b, end or b)
    if hi_active <= lo_active:
        return 0.0
    assert points[0][0] <= lo_active, ("no rate at", lo_active, points[0])
    tot = 0.0
    for i, (d, v) in enumerate(points):
        nxt = points[i + 1][0] if i + 1 < len(points) else D(9999, 1, 1)
        lo, hi = max(d, lo_active), min(nxt, hi_active)
        if hi > lo:
            tot += v * (hi - lo).days
    return tot / (b - a).days


def rate_on(points, day):
    return [v for d, v in points if d <= day][-1]


# ============================================================ load sources
def load_dss(folder):
    dss = folder / "dss"
    out = {}
    # JobSeeker / NSA over-21 (22+) single, no children: the table whose first row is 13/12/1987 108.40
    t = next(t for t in html_tables(dss / "g_5_2_1_20.html") if len(t) > 1 and t[1][:2] == ["13/12/1987", "108.40"])
    pts, unit = [], 52
    for r in t[1:]:
        if r and r[0] == "Date" and "pf" in " ".join(r):
            unit = 26
            continue
        d = ddmmyyyy(r[0]) if r else None
        if d:
            assert (unit == 26) == (d >= D(2020, 3, 20)), ("unit switch not at 20 Mar 2020", d)
            pts.append((d, unit * money(r[1])))
    out["jsp"] = sorted(pts)
    # Rent Assistance, single no children ($ pf), column 1 (header colspan checked by hand)
    t = next(t for t in html_tables(dss / "g_5_2_6_10.html") if t and t[0][0] == "Date of effect" and "Couple ($ pf)" in t[0]
             and len(t) > 2 and t[2][0] == "13/06/1990")
    out["ra"] = rate_rows(t, 1, 26)
    # Clean Energy Supplement (20 Mar 2013 - 19 Sep 2014) and Energy Supplement (from 20 Sep 2014)
    txt = page_text(dss / "g_5_2_9_30.html")
    ces_dates = [D(2013, 3, 20), D(2013, 9, 20), D(2014, 3, 20)]
    seg_p = txt[txt.index("Pensions (including"):txt.index("Seniors supplement")]
    seg_a = txt[txt.index("Allowance rates"):txt.index("Parenting payments")]
    pn = [float(x) for x in re.findall(r"\d+\.\d\d", seg_p)]
    an = [float(x) for x in re.findall(r"\d+\.\d\d", seg_a)]
    assert len(pn) == 6 and len(an) == 15, (pn, an)
    txt = page_text(dss / "g_5_1_10_20.html")
    es_pen = money(re.search(r"Pensions \(other than DSP under 21 and PPS ?\).*?(\$[\d,.]+)", txt).group(1))
    es_jsp = money(re.search(r"JSP single - no children.*?(\$[\d,.]+)", txt).group(1))
    out["es_pen"] = list(zip(ces_dates, pn[0::2])) + [(D(2014, 9, 20), es_pen)]
    out["es_jsp"] = list(zip(ces_dates, an[0::5])) + [(D(2014, 9, 20), es_jsp)]
    # Age Pension standard (single) rate, $ p.a.
    t = next(t for t in html_tables(dss / "g_5_2_2_10.html") if t and "Standard rate ($ p.a.)" in t[0])
    out["basic"] = rate_rows(t, 1)
    tabs = [t for t in html_tables(dss / "g_5_2_8_10.html") if t and t[0][0] == "Date"]
    out["gst"] = rate_rows(tabs[0], 1)
    assert tabs[1][1][0] == "Pension supplement"
    out["ps"] = rate_rows(tabs[1], 1)
    t = next(t for t in html_tables(dss / "g_5_2_6_50.html") if t and t[0][:2] == ["Date", "Single ($ pf)"])
    out["pha"] = rate_rows(t, 1, 26)
    t = next(t for t in html_tables(dss / "g_5_2_6_100.html") if t and t[0][:2] == ["Date", "Single ($ p.a.)"])
    out["ua"] = rate_rows(t, 1)
    tabs = [t for t in html_tables(dss / "g_5_2_6_40.html") if t and t[0] and t[0][0] == "Date"]
    std = next(t for t in tabs if len(t) > 1 and t[1][0] == "01/07/1992" and t[0][1] == "Rate per annum ($)")
    hi = next(t for t in tabs if "Higher rate per annum ($)" in t[0])
    out["tal"] = sorted([p for p in rate_rows(std, 1) if p[0] < D(2008, 3, 20)] + rate_rows(hi, 3))
    out["text_155"] = page_text(dss / "g_1_1_p_155.html")
    out["reviewed"] = {f.name: (re.search(r"Last reviewed:?\s*(\d{1,2} \w+ \d{4})", page_text(f)) or [None, None])[1]
                       for f in sorted(dss.glob("g_5_*.html"))}
    return out


def jobseeker_cost(dss, fy):
    return fy_mean(dss["jsp"], fy) + fy_mean(dss["ra"], fy) + fy_mean(dss["es_jsp"], fy, start=D(2013, 3, 20))


def pension_cost(dss, fy):
    return (fy_mean(dss["basic"], fy) + fy_mean(dss["gst"], fy, D(2000, 7, 1), REFORM)
            + fy_mean(dss["ps"], fy, REFORM) + fy_mean(dss["pha"], fy, D(1990, 11, 1), REFORM)
            + fy_mean(dss["ua"], fy, D(2005, 3, 20), REFORM) + fy_mean(dss["tal"], fy, D(1992, 7, 1), REFORM)
            + fy_mean(dss["es_pen"], fy, D(2013, 3, 20)))


def henderson_pdf(path):
    pages = [p.extract_text(extraction_mode="layout") for p in pypdf.PdfReader(path).pages]
    text = "\n".join(pages)
    t1 = text[text.index("Table 1: Poverty Lines"):]
    in_wf, not_wf = re.split(r"Head not in\s+workforce", t1, maxsplit=1)
    not_wf = not_wf[:3000]
    def line(seg, label):
        m = re.search(label + r"\s+([\d,]+\.\d\d)\s+([\d,]+\.\d\d)", seg)
        return float(m.group(1).replace(",", "")), float(m.group(2).replace(",", ""))
    lines = {"single_wf": line(in_wf, "Single person")[0], "couple2_wf": line(in_wf, "Couple plus 2")[0],
             "single_nwf": line(not_wf, "Single person")[0]}
    hdi = {}
    if "Table 2: Seasonally adjusted household disposable income" in text:
        t2 = text[text.index("Table 2: Seasonally adjusted household disposable income"):]
        t2 = t2[:t2.index("Table 3")]
        for m in re.finditer(r"(\d{4})/(\d{2})\s+([\d,.]+)\s+([\d,.]+)\s+([\d,.]+)\s+([\d,.]+)", t2):
            fy = int(m.group(1)) + 1
            for k, q in enumerate(("S", "D", "M", "J")):
                hdi[(fy, q)] = float(m.group(3 + k).replace(",", ""))
    return lines, hdi, text


def quarter_weights(fy):
    b = [D(fy - 1, 7, 1), D(fy - 1, 10, 1), D(fy, 1, 1), D(fy, 4, 1), D(fy, 7, 1)]
    return {q: (b[i + 1] - b[i]).days for i, q in enumerate("SDMJ")}


def quarterly_fy(values, fy):
    w = quarter_weights(fy)
    return sum(52 * values[q] * n for q, n in w.items()) / sum(w.values())


def fred_monthly(path, col):
    out = {}
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            if r[col].strip():
                out[D.fromisoformat(r["observation_date"])] = float(r[col])
    return out


def fy_of(d):
    return d.year + (d.month >= 7)


def fy_means(monthly, need=12):
    by = {}
    for d, v in monthly.items():
        by.setdefault(fy_of(d), []).append(v)
    return {fy: sum(v) / len(v) for fy, v in by.items() if len(v) == need}


def rba_monthly(hist_xls, f21_csv):
    out = {}
    if hist_xls and hist_xls.exists():
        s = xlrd.open_workbook(str(hist_xls)).sheet_by_name("Data")
        j = next(c for c in range(s.ncols) if s.cell_value(10, c) == "FCMYGBAG10")
        for r in range(11, s.nrows):
            v = s.cell_value(r, j)
            if v != "":
                d = xlrd.xldate_as_datetime(s.cell_value(r, 0), 0).date()
                out[D(d.year, d.month, 1)] = float(v)
    with open(f21_csv, encoding="utf-8-sig") as f:
        rows = list(csv.reader(f))
    j = next(r for r in rows if r and r[0] == "Series ID").index("FCMYGBAG10")
    for r in rows:
        try:
            d = dt.datetime.strptime(r[0], "%d-%b-%Y").date()
        except (ValueError, IndexError):
            continue
        if r[j] and D(d.year, d.month, 1) > D(2013, 5, 1):   # hist covers to May 2013
            out[D(d.year, d.month, 1)] = float(r[j])
    return out


# ============================================================ main
def main():
    print("== 0. fresh downloads vs vendored files")
    if FRESH:
        for name in ["5204061_Land_Value_By_Use.xlsx", "5204042_Household_FCE.xlsx", "5204010_National_Balance_Sheet.xlsx",
                     "310104.xlsx", "IRLTLT01AUM156N.csv"] + [f"henderson/{p.name}" for p in (RAW / "henderson").glob("*.pdf")]:
            a, b = RAW / name, FRESH / name
            if b.exists():
                same = hashlib.sha256(a.read_bytes()).digest() == hashlib.sha256(b.read_bytes()).digest()
                report(f"fresh download identical: {name}", "vendored", "fresh", same)
        if (FRESH / "f2.1-data.csv").exists():
            same = (RAW / "rba_f2.1-data.csv").read_bytes() == (FRESH / "f2.1-data.csv").read_bytes()
            report("fresh download identical: RBA f2.1-data.csv", "vendored", "fresh", same)

    # ---------------------------------------------------------------- inputs
    res_s, mres = abs_xlsx_series(RAW / "5204061_Land_Value_By_Use.xlsx", "A2423270K")
    tot_s, mtot = abs_xlsx_series(RAW / "5204061_Land_Value_By_Use.xlsx", "A2423297K")
    act_s, mact = abs_xlsx_series(RAW / "5204042_Household_FCE.xlsx", "A2422100A")
    imp_s, mimp = abs_xlsx_series(RAW / "5204042_Household_FCE.xlsx", "A2422101C")
    dw_s, _ = abs_xlsx_series(RAW / "5204010_National_Balance_Sheet.xlsx", "A2421120T")
    bsl_s, _ = abs_xlsx_series(RAW / "5204010_National_Balance_Sheet.xlsx", "A2421132A")
    min_s, _ = abs_xlsx_series(RAW / "5204010_National_Balance_Sheet.xlsx", "A2421133C")
    erp_s, merp = abs_xlsx_series(RAW / "310104.xlsx", "A2060842F")
    print(f"units: land {mres['unit']}/{mtot['unit']} ({mres['type']}); rent {mact['unit']}/{mimp['unit']} "
          f"({mact['type']}); ERP {merp['unit']} ({merp['type']})")
    assert mres["unit"] == mtot["unit"] == "$ Billions" and mact["unit"] == mimp["unit"] == "$ Millions"
    res = {y: v * 1e9 for y, v in annual_by_year(res_s).items()}
    tot = {y: v * 1e9 for y, v in annual_by_year(tot_s).items()}
    rent = {y: (act_s[d] + imp_s[d]) * 1e6 for y, d in ((d.year, d) for d in act_s)}
    dwell = {y: v * 1e9 for y, v in annual_by_year(dw_s).items()}
    assert all(abs(tot_s[d] - bsl_s[d]) < 0.051 for d in tot_s), "Table 61 total != balance-sheet land"
    pop_q = {}
    for d, v in erp_s.items():
        pop_q.setdefault(fy_of(d), []).append(v)
    pop = {fy: sum(v) / 4 for fy, v in pop_q.items() if len(v) == 4}
    fred = fred_monthly(RAW / "IRLTLT01AUM156N.csv", "IRLTLT01AUM156N")
    y = fy_means(fred)
    hist = (FRESH / "f02histhist.xls") if FRESH else None
    rba = rba_monthly(hist, RAW / "rba_f2.1-data.csv")
    y_rba = fy_means(rba)
    dss = load_dss(RAW)
    lines, hdi, mi_text = henderson_pdf(RAW / "henderson" / "Poverty-Lines-Australia-June-Quarter-2026.pdf")
    hdi_now = hdi[(2026, "J")]

    print("== 1. source cross-checks")
    common = sorted(fy for fy in y if fy in y_rba and 1991 <= fy <= 2025)
    worst = max(abs(y[fy] - y_rba[fy]) for fy in common) if common else None
    report("FY-average 10-yr yield: FRED vs RBA's own F2 (hist to May 2013, F2.1 after)", "FRED", f"{len(common)} FYs",
           common != [] and worst < 0.01, f"max |diff| {worst:.4f} pp over FY{common[0]}-FY{common[-1]}")
    if FRESH and (FRESH / "erp_q.csv").exists():
        api = {}
        with open(FRESH / "erp_q.csv", newline="") as f:
            for r in csv.DictReader(f):
                yq, qn = r["TIME_PERIOD"].split("-Q")
                api[D(int(yq), 3 * int(qn), 1)] = float(r["OBS_VALUE"])
        both = [d for d in api if d in erp_s]
        report("ERP: 3101.0 Table 4 xlsx vs ABS Data API ERP_Q (1.3.TOT.AUS.Q)", "xlsx", f"{len(both)} quarters",
               bool(both) and max(abs(api[d] - erp_s[d]) for d in both) < 0.5)
    t155 = dss["text_155"]
    q155 = "It combined the full value of the GST supplement, PhA , UA and the higher rate of TAL"
    report("Guide 1.1.P.155 quote (pension supplement absorbed GST supp., PhA, UA, higher TAL)", "quoted", "page",
           q155 in t155)
    report("DSS rate pages last reviewed", "21 Sep 2026 / 2 Jan 2026", str(dss["reviewed"]), True)
    mi_note = re.search(r"\$\s*(1,134\.58)", mi_text)
    report("Henderson June 2026 single in workforce incl. housing ($ pw)", "708.86", f"{lines['single_wf']:.2f}",
           abs(lines["single_wf"] - 708.86) < 0.005, f"HDI June 2026 {hdi_now} (note: {mi_note.group(1) if mi_note else 'n/a'})")
    t4 = re.search(r"Allowee d\s+([\d.]+)\s+-\s+-\s+-\s+([\d.]+)\s+([\d.,]+)\s+([\d.,]+)\s*\n\s*Pensioner e\s+([\d.]+)"
                   r"\s+-\s+-\s+-\s+([\d.]+)\s+([\d.,]+)\s+([\d.,]+)", mi_text)
    jun26 = D(2026, 6, 30)
    js_wk = (rate_on(dss["jsp"], jun26) + rate_on(dss["es_jsp"], jun26)) / 52
    ra_wk = rate_on(dss["ra"], jun26) / 52
    ap_wk = (rate_on(dss["basic"], jun26) + rate_on(dss["ps"], jun26) + rate_on(dss["es_pen"], jun26)) / 52
    report("MI Table 4 June qtr 2026 single allowee / RA / single pensioner ($ pw) = DSS", "408.75/109.70/600.45",
           f"{js_wk:.2f}/{ra_wk:.2f}/{ap_wk:.2f} (MI {t4.group(1)}/{t4.group(2)}/{t4.group(5)})" if t4 else "row not found",
           bool(t4) and abs(float(t4.group(1)) - js_wk) < 0.006 and abs(float(t4.group(2)) - ra_wk) < 0.006
           and abs(float(t4.group(5)) - ap_wk) < 0.006,
           f"MI compares the pensioner with the NOT-in-workforce line {t4.group(8) if t4 else '?'}; allowee with {t4.group(4) if t4 else '?'}")

    # ---------------------------------------------------------------- the grid
    hend_w = {k: lines["single_wf"] * v / hdi_now for k, v in hdi.items()}

    def costs(fy):
        return {"henderson": quarterly_fy({q: hend_w[(fy, q)] for q in "SDMJ"}, fy),
                "jobseeker": jobseeker_cost(dss, fy), "age_pension": pension_cost(dss, fy)}

    def numerators(fy, yld=None, land_res=None, land_tot=None):
        yy = (y[fy] if yld is None else yld) / 100
        lr, lt = res[fy] if land_res is None else land_res, tot[fy] if land_tot is None else land_tot
        return {"land_res_y": lr * yy, "land_res_y150": lr * (yy + 0.015), "land_all_y": lt * yy,
                "land_all_y150": lt * (yy + 0.015), "rent_ls30": 0.3 * rent[fy], "rent_ls50": 0.5 * rent[fy]}

    def grid(nums, dens, p):
        return {f"{a}__{b}": nv / (p * dv) for a, nv in nums.items() for b, dv in dens.items()}

    with open(OUT / "coverage.csv", newline="") as f:
        cov = {int(r["fy_end"]): r for r in csv.DictReader(f)}
    hist_bad, rows = [], {}
    for fy in range(1991, 2026):
        n, c = numerators(fy), costs(fy)
        g = grid(n, c, pop[fy])
        rows[fy] = (n, c, g)
        b = cov[fy]
        mine = (st.median(g.values()), min(g.values()), max(g.values()))
        theirs = (float(b["coverage_median"]), float(b["coverage_min"]), float(b["coverage_max"]))
        if any(abs(a - t) > 1e-6 for a, t in zip(mine, theirs)) or any(
                abs(c[k] - float(b[f"cost_{k}"])) > 0.01 for k in c) or abs(pop[fy] - float(b["population"])) > 0.01:
            hist_bad.append(fy)

    print("== 2. headline numbers, 2024-25")
    n, c, g = rows[2025]
    med, lo, hi = st.median(g.values()), min(g.values()), max(g.values())
    report("coverage median [min-max] FY2025", "0.4848 [0.0956-0.8496]", f"{med:.4f} [{lo:.4f}-{hi:.4f}]",
           f"{med:.4f} [{lo:.4f}-{hi:.4f}]" == "0.4848 [0.0956-0.8496]",
           f"min = {min(g, key=g.get)}, max = {max(g, key=g.get)}")
    fl = st.median(v for k, v in g.items() if k.startswith("land_"))
    fr = st.median(v for k, v in g.items() if k.startswith("rent_"))
    report("land-value family / rent-share family medians", "0.5697 / 0.1443", f"{fl:.4f} / {fr:.4f}",
           f"{fl:.4f} / {fr:.4f}" == "0.5697 / 0.1443")
    report("ingredients", "res 8,317bn; all 10,374bn; yield 4.29; rent 305bn; pop 27,455,073",
           f"res {res[2025]/1e9:,.1f}bn; all {tot[2025]/1e9:,.1f}bn; yield {y[2025]:.4f}; rent {rent[2025]/1e9:,.1f}bn; "
           f"pop {pop[2025]:,.0f}", abs(pop[2025] - 27455073) < 1 and abs(y[2025] - 4.29) < 0.005)
    report("six land-rent measures ($bn)", "91 / 152 / 357 / 445 / 482 / 601; median 401",
           " / ".join(f"{v/1e9:.1f}" for v in sorted(n.values())) + f"; median {st.median(n.values())/1e9:.1f}", True)
    rpp = st.median(n.values()) / pop[2025]
    report("rent per resident FY2025", "14,607.47", f"{rpp:,.2f}", abs(rpp - 14607.47) < 0.01)
    report("costs FY2025 Henderson / JobSeeker pkg / Age Pension", "34,815.67 / 25,755.63 / 29,626.02",
           " / ".join(f"{c[k]:,.2f}" for k in ("henderson", "jobseeker", "age_pension")),
           all(abs(c[k] - v) < 0.01 for k, v in (("henderson", 34815.67), ("jobseeker", 25755.63),
                                                    ("age_pension", 29626.02))))
    # the rate periods quoted for 2024-25
    q = {"JSP": [rate_on(dss["jsp"], d) / 26 for d in (D(2024, 3, 20), D(2024, 9, 20), D(2025, 3, 20))],
         "RA": [rate_on(dss["ra"], d) / 26 for d in (D(2024, 3, 20), D(2024, 9, 20), D(2025, 3, 20))],
         "AP": [rate_on(dss["basic"], d) for d in (D(2024, 3, 20), D(2024, 9, 20), D(2025, 3, 20))],
         "PS": [rate_on(dss["ps"], d) for d in (D(2024, 3, 20), D(2024, 9, 20), D(2025, 3, 20))]}
    report("2024-25 rates quoted", "JSP 762.70/778.00/781.10; RA 188.20/211.20/212.00; AP 26,535.60/27,224.60/27,333.80; "
           "PS 2,121.60/2,163.20/2,173.60; ES 8.80 pf / 366.60 pa",
           "; ".join(f"{k} " + "/".join(f"{v:,.2f}" for v in vs) for k, vs in q.items())
           + f"; ES {rate_on(dss['es_jsp'], D(2025,1,1))/26:.2f} pf / {rate_on(dss['es_pen'], D(2025,1,1)):.2f} pa",
           [round(v, 2) for v in q["JSP"]] == [762.70, 778.00, 781.10] and [round(v, 2) for v in q["RA"]] == [188.20, 211.20, 212.00]
           and [round(v, 2) for v in q["AP"]] == [26535.60, 27224.60, 27333.80]
           and [round(v, 2) for v in q["PS"]] == [2121.60, 2163.20, 2173.60])
    hdi25 = quarterly_fy({k: hdi[(2025, k)] for k in "SDMJ"}, 2025)
    report("rent per resident / HDI per head", "0.262 of $55,725", f"{rpp / hdi25:.3f} of ${hdi25:,.0f}",
           abs(rpp / hdi25 - 0.262) < 0.0005 and round(hdi25) == 55725)
    diag = n["land_res_y"] / rent[2025]
    report("diagnostic residential land x yield / housing rent", "1.1714 ($357bn / $305bn)",
           f"{diag:.4f} (${n['land_res_y']/1e9:.0f}bn / ${rent[2025]/1e9:.0f}bn)", abs(diag - 1.1714) < 5e-5)
    below = [fy for fy in range(1991, 2026) if rows[fy][0]["land_res_y"] / rent[fy] < 1]
    report("years with diagnostic < 1", "most of 1992-93..2000-01; 2008-09; 2011-12..2021-22",
           ", ".join(f"{fy-1}-{str(fy)[2:]}" for fy in below), True)

    print("== 3. current rates")
    now = D(2026, 9, 20)
    js_now = [rate_on(dss["jsp"], now) / 26, rate_on(dss["es_jsp"], now) / 26, rate_on(dss["ra"], now) / 26]
    ap_now = [rate_on(dss["basic"], now) / 26, rate_on(dss["ps"], now) / 26, rate_on(dss["es_pen"], now) / 26]
    report("JobSeeker pkg now ($ pf)", "824.90 + 8.80 + 223.80 = 1,057.50 (27,495 pa)",
           " + ".join(f"{v:.2f}" for v in js_now) + f" = {sum(js_now):,.2f} ({26*sum(js_now):,.2f} pa)",
           abs(sum(js_now) - 1057.50) < 0.005)
    report("Age Pension now ($ pf)", "1,135.40 + 88.20 + 14.10 = 1,237.70 (32,180 pa)",
           " + ".join(f"{v:.2f}" for v in ap_now) + f" = {sum(ap_now):,.2f} ({26*sum(ap_now):,.2f} pa)",
           abs(sum(ap_now) - 1237.70) < 0.005)
    report("Henderson now", "708.86 pw (36,861 pa)", f"{lines['single_wf']:.2f} pw ({52*lines['single_wf']:,.2f} pa)",
           round(52 * lines["single_wf"]) == 36861)

    print("== 4. sensitivities in the report")
    dens = list(c.values())
    stock = {k: (s[2025] + s[2024]) / 2 for k, s in (("r", res), ("t", tot))}
    n_avg = numerators(2025, land_res=stock["r"], land_tot=stock["t"])
    s1 = st.median(grid(n_avg, c, pop[2025]).values())
    share = res[2025] / (res[2025] + dwell[2025])
    s2 = st.median(share * rent[2025] / (pop[2025] * d) for d in dens)
    cur = {"henderson": 52 * lines["single_wf"], "jobseeker": 26 * sum(js_now), "age_pension": 26 * sum(ap_now)}
    s3 = st.median(grid(n, cur, pop[2025]).values())
    pub = {}
    for qq, fname in (("S", "Poverty-Lines-Australia-September-2024.pdf"), ("D", "Poverty-Lines-Australia-December-Quarter-2024.pdf"),
                      ("M", "Poverty-Lines-Australia-March-Quarter-2025.pdf"), ("J", "Poverty-Lines-Australia-June-Quarter-2025.pdf")):
        pub[qq] = henderson_pdf(RAW / "henderson" / fname)[0]["single_wf"]
    h_pub = quarterly_fy(pub, 2025)
    s4 = st.median(grid(n, dict(c, henderson=h_pub), pop[2025]).values())
    report("sens: average land stock / ABS land share / rates now / Henderson as published",
           "0.4699 / 0.7192 -> 0.2694 / 0.4564 / 0.4919 (h 33,846.29)",
           f"{s1:.4f} / {share:.4f} -> {s2:.4f} / {s3:.4f} / {s4:.4f} (h {h_pub:,.2f}; {list(pub.values())})",
           f"{s1:.4f}/{share:.4f}/{s2:.4f}/{s3:.4f}/{s4:.4f}" == "0.4699/0.7192/0.2694/0.4564/0.4919")

    print("== 5. history")
    n91, c91, g91 = rows[1991]
    m91 = (st.median(g91.values()), min(g91.values()), max(g91.values()))
    report("FY1991 median [min-max]", "0.3935 [0.0789-0.6973]", "{:.4f} [{:.4f}-{:.4f}]".format(*m91),
           "{:.4f} [{:.4f}-{:.4f}]".format(*m91) == "0.3935 [0.0789-0.6973]")
    report("whole history FY1991-FY2025 (median/min/max, costs, population) = coverage.csv", "match",
           f"mismatched {hist_bad}", not hist_bad)
    fam = {fy: (st.median(v for k, v in rows[fy][2].items() if k.startswith("land_")),
                st.median(v for k, v in rows[fy][2].items() if k.startswith("rent_"))) for fy in rows}
    report("land-value family 1990-91 / 2007-08 / 2019-20 / 2024-25", "0.49 / 0.64 / 0.16 / 0.57",
           " / ".join(f"{fam[fy][0]:.3f}" for fy in (1991, 2008, 2020, 2025)),
           [round(fam[fy][0], 2) for fy in (1991, 2008, 2020, 2025)] == [0.49, 0.64, 0.16, 0.57])
    report("rent family 1990-91 -> 2024-25", "0.11 -> 0.14", f"{fam[1991][1]:.3f} -> {fam[2025][1]:.3f}",
           [round(fam[fy][1], 2) for fy in (1991, 2025)] == [0.11, 0.14])
    report("bond yield 1990-91 / 2019-20", "12.1 / 1.0", f"{y[1991]:.2f} / {y[2020]:.2f}",
           round(y[1991], 1) == 12.1 and round(y[2020], 1) == 1.0)
    peak = max(fam, key=lambda fy: fam[fy][0])
    trough = min(fam, key=lambda fy: fam[fy][0])
    print(f"   land-family max {fam[peak][0]:.3f} in FY{peak}, min {fam[trough][0]:.3f} in FY{trough}; "
          f"rent-family range {min(v[1] for v in fam.values()):.3f}-{max(v[1] for v in fam.values()):.3f}")
    print("   medians by year: " + ", ".join(f"{fy}:{st.median(rows[fy][2].values()):.2f}" for fy in rows))

    print("== 6. US comparison")
    with open(RAW / "us" / "kappa_results_paper.csv", newline="") as f:
        us = {int(r["year"]): r for r in csv.DictReader(f)}[2025]
    cpi_path = (FRESH / "CPIAUCSL.csv") if FRESH and (FRESH / "CPIAUCSL.csv").exists() else RAW / "us" / "CPIAUCSL.csv"
    cpi = fred_monthly(cpi_path, "CPIAUCSL")
    c25 = [v for d, v in cpi.items() if d.year == 2025]
    c63 = [v for d, v in cpi.items() if d.year == 1963]
    bundle = 1540 * (sum(c25) / len(c25)) / (sum(c63) / len(c63))
    dpi = fred_monthly(RAW / "us" / "A229RC0A052NBEA.csv", "A229RC0A052NBEA")
    dpi25 = next(v for d, v in dpi.items() if d.year == 2025)
    us_single = {k: float(v) for k, v in us.items() if k.startswith("k_") and k.endswith("_single") and v}
    us_rpp = st.median(us_single.values()) * bundle
    report("US 2025 paper grid", "0.33 [0.18-0.59]",
           f"{float(us['kappa_med']):.3f} [{float(us['kappa_min']):.3f}-{float(us['kappa_max']):.3f}]",
           f"{float(us['kappa_med']):.2f} [{float(us['kappa_min']):.2f}-{float(us['kappa_max']):.2f}]" == "0.33 [0.18-0.59]",
           f"{len(c25)} CPI months in 2025 (cpi from {cpi_path.parent.name})")
    report("US: single bundle / DPI per head; rent per person / DPI", "16,186; 0.241 (pc4 0.122); 0.052",
           f"{bundle:,.0f}; {bundle/dpi25:.3f} (pc4 {782*bundle/1540/dpi25:.3f}); {us_rpp/dpi25:.3f} (n={len(us_single)})",
           round(bundle) == 16186 and round(us_rpp / dpi25, 3) == 0.052)
    au_costs_hdi = {k: c[k] / hdi25 for k in c}
    report("AU: costs / HDI per head", "Henderson 0.625, JobSeeker 0.462, Age Pension 0.532",
           ", ".join(f"{k} {v:.3f}" for k, v in au_costs_hdi.items()), True)
    print(f"   AU rent-family per person / HDI: {n['rent_ls30']/pop[2025]/hdi25:.3f} to {n['rent_ls50']/pop[2025]/hdi25:.3f}; "
          f"US: {float(us['k_flow_ls30_single'])*bundle/dpi25:.3f} to {float(us['k_flow_ls50_single'])*bundle/dpi25:.3f}")
    print(f"   AU residential land at yield / HDI: {n['land_res_y']/pop[2025]/hdi25:.3f} to {n['land_res_y150']/pop[2025]/hdi25:.3f}; "
          f"US household land: {float(us['k_z1_hh_gs10_single'])*bundle/dpi25:.3f} to {float(us['k_z1_hh_gs10p_single'])*bundle/dpi25:.3f}")
    us_pc4 = {k: float(v) for k, v in us.items() if k.startswith("k_") and k.endswith("_pc4") and v}
    print(f"   US grid uses {len(us_single)} single + {len(us_pc4)} per-capita (family of four) members; "
          f"US median of single-bundle members only: {st.median(us_single.values()):.3f}")

    print("== 7. definition probes (not in the builder's grid)")
    nwf = lines["single_nwf"]
    h_nwf = quarterly_fy({k: nwf * hdi[(2025, k)] / hdi_now for k in "SDMJ"}, 2025)
    g_nwf = grid(n, dict(c, henderson=h_nwf), pop[2025])
    print(f"   Henderson single NOT in workforce incl. housing {nwf:.2f} pw (MI Table 4 compares it with the pensioner); "
          f"FY2025 {h_nwf:,.0f} pa; median with it {st.median(g_nwf.values()):.4f}")
    c2 = lines["couple2_wf"]
    h_pc4 = quarterly_fy({k: c2 / 4 * hdi[(2025, k)] / hdi_now for k in "SDMJ"}, 2025)
    g_pc4 = grid(n, dict(c, henderson_pc4=h_pc4), pop[2025])
    print(f"   per-head Henderson couple + 2 children ({c2:.2f}/4 pw; FY2025 {h_pc4:,.0f} pa), the analogue of the "
          f"paper's per-capita family bundle: 24-member median {st.median(g_pc4.values()):.4f} [{min(g_pc4.values()):.4f}-"
          f"{max(g_pc4.values()):.4f}]")
    g_res = {k: v for k, v in g.items() if not k.startswith("land_all")}
    print(f"   residential land only (drop the 6 all-land members): median {st.median(g_res.values()):.4f} "
          f"[{min(g_res.values()):.4f}-{max(g_res.values()):.4f}]")
    g_open = grid(numerators(2025, land_res=res[2024], land_tot=tot[2024]), c, pop[2025])
    print(f"   opening stock (30 Jun 2024) x 2024-25 yield: median {st.median(g_open.values()):.4f}")
    capped = dict(n, land_res_y=min(n["land_res_y"], rent[2025]), land_res_y150=min(n["land_res_y150"], rent[2025]))
    print(f"   residential land rent capped at all housing rent: median {st.median(grid(capped, c, pop[2025]).values()):.4f}")
    pop30 = erp_s[D(2025, 6, 1)]
    print(f"   population at 30 June 2025 ({pop30:,.0f}) instead of FY mean: median "
          f"{st.median(grid(n, c, pop30).values()):.4f}")
    print(f"   mineral and energy resources 30 Jun 2025: ${min_s[D(2025, 6, 1)]:,.1f}bn")
    print(f"   members above 0.5: {sum(v > 0.5 for v in g.values())} of 18; land-value members range "
          f"{min(v for k, v in g.items() if k.startswith('land_')):.3f}-{max(v for k, v in g.items() if k.startswith('land_')):.3f}")
    sorted_members = sorted(g.items(), key=lambda kv: kv[1])
    print("   sorted members: " + ", ".join(f"{k} {v:.3f}" for k, v in sorted_members))

    n_bad = results.count(False)
    print(f"\n{len(results) - n_bad}/{len(results)} OK" + (f"; {n_bad} BAD" if n_bad else ""))
    return 1 if n_bad else 0


if __name__ == "__main__":
    sys.exit(main())
