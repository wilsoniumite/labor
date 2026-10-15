"""Independent re-computation of every headline number in out/headline.csv (and the grid in out/coverage.csv).

Deliberately a different code path from code/build_coverage.py:
  ABS workbooks    pandas.read_excel (build: openpyxl cell loop)
  FRED / ERP       pandas resampling by financial year (build: dict loops)
  Henderson PDFs   pdfplumber, page-by-page (build: pypdf, whole document)
  DSS rate pages   regular expressions on the flattened page text (build: an HTML table parser)
  FY averages      pandas daily index + forward fill (build: a Step class evaluated day by day)
  Units            JobSeeker weekly/fortnightly decided by date (build: by the in-table header row)
Prints PASS/FAIL per check and exits non-zero on any FAIL.
Run:  venv\\Scripts\\python.exe austax\\coverage\\checks\\check_coverage.py
"""
import html
import re
import statistics
import sys
from pathlib import Path

import pandas as pd
import pdfplumber

ROOT = Path(__file__).resolve().parents[1]
RAW, OUT = ROOT / "data" / "raw", ROOT / "out"
results = []


def check(name, ok, detail=""):
    results.append(ok)
    print(f"{'PASS' if ok else 'FAIL'}  {name}  {detail}")


def close(a, b, rel=1e-6):
    return abs(a - b) <= rel * max(1.0, abs(b))


# ------------------------------------------------------------------ ABS workbooks via pandas
def abs_frame(fname):
    df = pd.read_excel(RAW / fname, sheet_name="Data1", header=None)
    ids = df.iloc[9].tolist()                  # row 10 holds the Series IDs in ABS time-series workbooks
    assert ids[0] == "Series ID", ids[0]
    data = df.iloc[10:].copy()
    data.columns = ids
    data = data.set_index("Series ID")
    data.index = pd.to_datetime(data.index)
    return data.astype(float)


land = abs_frame("5204061_Land_Value_By_Use.xlsx")
bs = abs_frame("5204010_National_Balance_Sheet.xlsx")
hfce = abs_frame("5204042_Household_FCE.xlsx")
erp = abs_frame("310104.xlsx")["A2060842F"].dropna()


def at_june(series, fy):
    return float(series[series.index == pd.Timestamp(fy, 6, 1)].iloc[0])


fyidx = lambda idx: (idx + pd.DateOffset(months=6)).year     # month >= July -> next year's FY
pop_fy = erp.groupby(fyidx(erp.index)).agg(["mean", "count"])
fred = pd.read_csv(RAW / "IRLTLT01AUM156N.csv", parse_dates=["observation_date"]).set_index("observation_date")
y_fy = fred["IRLTLT01AUM156N"].groupby(fyidx(fred.index)).agg(["mean", "count"])


def numerators(fy):
    res, tot = at_june(land["A2423270K"], fy) * 1e9, at_june(land["A2423297K"], fy) * 1e9
    assert y_fy.loc[fy, "count"] == 12
    yy = y_fy.loc[fy, "mean"] / 100
    rent = (at_june(hfce["A2422100A"], fy) + at_june(hfce["A2422101C"], fy)) * 1e6
    return {"land_res_y": res * yy, "land_res_y150": res * (yy + 0.015), "land_all_y": tot * yy,
            "land_all_y150": tot * (yy + 0.015), "rent_ls30": 0.3 * rent, "rent_ls50": 0.5 * rent}, res, tot, rent


def population(fy):
    assert pop_fy.loc[fy, "count"] == 4
    return pop_fy.loc[fy, "mean"]


# ------------------------------------------------------------------ Henderson via pdfplumber
def hend_pdf(fname):
    with pdfplumber.open(RAW / "henderson" / fname) as pdf:
        return [p.extract_text() for p in pdf.pages]


pages = hend_pdf("Poverty-Lines-Australia-June-Quarter-2026.pdf")
single_now = float(re.search(r"Single person ([\d,]+\.\d\d)", pages[1]).group(1).replace(",", ""))
hdi = {}
for m in re.finditer(r"(\d{4})/(\d{2}) ([\d,.]+) ([\d,.]+) ([\d,.]+) ([\d,.]+)", pages[2]):
    for k, q in enumerate((9, 12, 3, 6)):           # quarter-ending month
        year = int(m.group(1)) + (q <= 6)
        hdi[pd.Timestamp(year, q, 1)] = float(m.group(3 + k).replace(",", ""))
hdi = pd.Series(hdi).sort_index()
hdi_now = hdi[pd.Timestamp(2026, 6, 1)]


def fy_days_index(fy):
    return pd.date_range(f"{fy - 1}-07-01", f"{fy}-06-30", freq="D")


def quarterly_to_fy(qseries, fy):
    """52 x weekly value, each day carrying the value of the quarter it falls in."""
    days = fy_days_index(fy)
    qend = (days + pd.offsets.QuarterEnd(0)).to_period("M").to_timestamp()
    return float((52 * qseries.reindex(qend).to_numpy()).mean())


def henderson(fy):
    return quarterly_to_fy(single_now * hdi / hdi_now, fy)


# ------------------------------------------------------------------ DSS pages via regex on flattened text
def flat(page):
    t = (RAW / "dss" / page).read_text(encoding="utf8")
    t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t)))


DATE = r"(\d\d/\d\d/\d{4})"
NOTES = r"(?:\s*\(?Note [A-Z]+\)?)*"
NUM = r"([\d,]+\.\d\d)"


def pairs(text, start_marker, end_marker, k_numbers=1, pick=0):
    seg = text[text.index(start_marker):]
    seg = seg[:seg.index(end_marker)]
    pat = DATE + NOTES + "".join(r"\s+" + NUM for _ in range(k_numbers))
    out = {}
    for m in re.finditer(pat, seg):
        out[pd.Timestamp(pd.to_datetime(m.group(1), dayfirst=True))] = float(m.group(2 + pick).replace(",", ""))
    return pd.Series(out).sort_index()


def daily(steps, start=None, end=None):
    """Annual-rate step series -> function of a FY giving the day-weighted mean (zero outside [start, end))."""
    def f(fy):
        days = fy_days_index(fy)
        s = steps.reindex(steps.index.union(days)).ffill().reindex(days)
        if start is not None:
            s[days < pd.Timestamp(start)] = 0.0
        if end is not None:
            s[days >= pd.Timestamp(end)] = 0.0
        assert not s.isna().any(), ("rate missing", fy)
        return s
    return f


t = flat("g_5_2_1_20.html")
jsp = pairs(t, "13/12/1987 108.40", "Note Explanation J")
jsp = jsp * [26 if d >= pd.Timestamp(2020, 3, 20) else 52 for d in jsp.index]
t = flat("g_5_2_6_10.html")
ra = pairs(t, "13/06/1990", "Notes for Table 1", k_numbers=4, pick=0) * 26
t_ces = flat("g_5_2_9_30.html")
ces_dates = [pd.Timestamp(2013, 3, 20), pd.Timestamp(2013, 9, 20), pd.Timestamp(2014, 3, 20)]
pen_nums = [float(x) for x in re.findall(NUM, t_ces[t_ces.index("Pensions (including"):t_ces.index("Seniors supplement")])]
alw_nums = [float(x) for x in re.findall(NUM, t_ces[t_ces.index("Allowance rates"):t_ces.index("Parenting payments")])]
t_es = flat("g_5_1_10_20.html")
es_pen = float(re.search(r"Pensions \(other than.*?\$([\d,]+\.\d\d)", t_es).group(1))
es_jsp = float(re.search(r"JSP single - no children.*?\$([\d,]+\.\d\d)", t_es).group(1))
es_alw = pd.Series([alw_nums[0], alw_nums[5], alw_nums[10], es_jsp], index=ces_dates + [pd.Timestamp(2014, 9, 20)])
es_pens = pd.Series([pen_nums[0], pen_nums[2], pen_nums[4], es_pen], index=ces_dates + [pd.Timestamp(2014, 9, 20)])

t = flat("g_5_2_2_10.html")
basic = pairs(t, "14/11/1963", "Note Explanation C", k_numbers=2, pick=0)
t = flat("g_5_2_8_10.html")
gst = pairs(t, "01/07/2000 387.40", "20/09/2009", k_numbers=2, pick=0)
psupp = pairs(t, "20/09/2009 1,458.60", "Last reviewed", k_numbers=8, pick=0)
pha = pairs(flat("g_5_2_6_50.html"), "01/11/1990", "Note Explanation", k_numbers=2, pick=0) * 26
ua = pairs(flat("g_5_2_6_100.html"), "20/03/2005", "Act reference", k_numbers=2, pick=0)
t = flat("g_5_2_6_40.html")
tal_std = pairs(t, "01/07/1992 51.80", "20/03/2008 88.00", k_numbers=2, pick=0)
tal_hi = pairs(t, "20/03/2008 88.00", "Note Explanation", k_numbers=4, pick=2)
tal = pd.concat([tal_std, tal_hi]).sort_index()

REFORM = "2009-09-20"
job_parts = [daily(jsp), daily(ra), daily(es_alw, start="2013-03-20")]
pen_parts = [daily(basic), daily(gst, start="2000-07-01", end=REFORM), daily(psupp, start=REFORM),
             daily(pha, start="1990-11-01", end=REFORM), daily(ua, start="2005-03-20", end=REFORM),
             daily(tal, start="1992-07-01", end=REFORM), daily(es_pens, start="2013-03-20")]


def fy_mean(parts, fy):
    return float(sum(p(fy) for p in parts).mean())


def costs(fy):
    return {"henderson": henderson(fy), "jobseeker": fy_mean(job_parts, fy), "age_pension": fy_mean(pen_parts, fy)}


def grid(fy):
    nums, res, tot, rent = numerators(fy)
    c, pop = costs(fy), population(fy)
    members = {f"{n}__{d}": nv / (pop * dv) for n, nv in nums.items() for d, dv in c.items()}
    return members, nums, c, pop, res, tot, rent


# ------------------------------------------------------------------ recompute and compare
cov = pd.read_csv(OUT / "coverage.csv").set_index("fy_end")
head = pd.read_csv(OUT / "headline.csv", dtype=str).set_index("id")["value"]


def hv(key):
    return head[key]


for fy in (2025, 1991):
    m, nums, c, pop, res, tot, rent = grid(fy)
    vals = list(m.values())
    row = cov.loc[fy]
    check(f"FY{fy} 18 members match coverage.csv", all(close(v, row[f"k_{k}"], 1e-8) for k, v in m.items()))
    check(f"FY{fy} population", close(pop, row["population"], 1e-8), f"{pop:,.0f}")
    for k, v in c.items():
        check(f"FY{fy} cost {k}", close(v, row[f"cost_{k}"], 1e-8), f"{v:,.2f}")
    if fy == 2025:
        check("coverage_median", f"{statistics.median(vals):.2f}" == hv("coverage_median"), f"{statistics.median(vals):.4f}")
        check("coverage_min", f"{min(vals):.2f}" == hv("coverage_min"), f"{min(vals):.4f}")
        check("coverage_max", f"{max(vals):.2f}" == hv("coverage_max"), f"{max(vals):.4f}")
        fl = statistics.median(v for k, v in m.items() if k.startswith("land_"))
        fr = statistics.median(v for k, v in m.items() if k.startswith("rent_"))
        check("coverage_median_landvalue_family", f"{fl:.2f}" == hv("coverage_median_landvalue_family"), f"{fl:.4f}")
        check("coverage_median_rentshare_family", f"{fr:.2f}" == hv("coverage_median_rentshare_family"), f"{fr:.4f}")
        rpp = statistics.median(nums.values()) / pop
        check("rent_per_person", f"{rpp:.0f}" == hv("rent_per_person"), f"{rpp:,.2f}")
        for k in c:
            check(f"cost_{k}", f"{c[k]:.0f}" == hv(f"cost_{k}"), f"{c[k]:,.2f}")
        diag = nums["land_res_y"] / rent
        check("diag_res_land_at_yield_over_housing_rent", f"{diag:.2f}" == hv("diag_res_land_at_yield_over_housing_rent"),
              f"{diag:.4f}")
        # sensitivities
        dens = list(c.values())
        avg_nums = []
        for code in ("A2423270K", "A2423297K"):
            stock = (at_june(land[code], 2025) + at_june(land[code], 2024)) / 2 * 1e9
            yy = y_fy.loc[2025, "mean"] / 100
            avg_nums += [stock * yy, stock * (yy + 0.015)]
        avg_nums += [nums["rent_ls30"], nums["rent_ls50"]]
        s1 = statistics.median(n / (pop * d) for n in avg_nums for d in dens)
        check("sens_average_land_stock", f"{s1:.2f}" == hv("sens_average_land_stock"), f"{s1:.4f}")
        share = res / (res + at_june(bs["A2421120T"], 2025) * 1e9)
        s2 = statistics.median(share * rent / (pop * d) for d in dens)
        check("sens_abs_land_share", f"{s2:.2f}" == hv("sens_abs_land_share"), f"share {share:.4f}, median {s2:.4f}")
        now = pd.Timestamp(2026, 9, 20)
        cur = [52 * single_now,
               jsp[jsp.index <= now].iloc[-1] + ra[ra.index <= now].iloc[-1] + es_jsp,
               basic[basic.index <= now].iloc[-1] + psupp[psupp.index <= now].iloc[-1] + es_pen]
        s3 = statistics.median(n / (pop * d) for n in nums.values() for d in cur)
        check("sens_latest_rates", f"{s3:.2f}" == hv("sens_latest_rates"),
              f"{s3:.4f}; rates now: Henderson {cur[0]:,.2f}, JobSeeker pkg {cur[1]:,.2f}, Age Pension {cur[2]:,.2f}")
        pub = {}
        for q, fname in ((9, "Poverty-Lines-Australia-September-2024.pdf"),
                         (12, "Poverty-Lines-Australia-December-Quarter-2024.pdf"),
                         (3, "Poverty-Lines-Australia-March-Quarter-2025.pdf"),
                         (6, "Poverty-Lines-Australia-June-Quarter-2025.pdf")):
            txt = " ".join(hend_pdf(fname))
            pub[pd.Timestamp(2024 + (q <= 6), q, 1)] = float(
                re.search(r"Single person ([\d,]+\.\d\d)", txt[txt.index("Head in workforce"):]).group(1).replace(",", ""))
        h_pub = quarterly_to_fy(pd.Series(pub), 2025)
        s4 = statistics.median(n / (pop * d) for n in nums.values() for d in [h_pub] + dens[1:])
        check("sens_henderson_as_published", f"{s4:.2f}" == hv("sens_henderson_as_published"),
              f"{s4:.4f}; as-published line {h_pub:,.2f} a year; quarters {list(pub.values())}")
    else:
        med = statistics.median(vals)
        check("coverage_median_first_year (1990-91)", f"{med:.2f}" == hv("coverage_median_first_year"),
              f"{med:.4f} [{min(vals):.4f}-{max(vals):.4f}]")

# whole history: medians in coverage.csv equal the independent grid in every year
bad = []
for fy in cov.index:
    vals = list(grid(fy)[0].values())
    if not (close(statistics.median(vals), cov.loc[fy, "coverage_median"], 1e-8)
            and close(min(vals), cov.loc[fy, "coverage_min"], 1e-8) and close(max(vals), cov.loc[fy, "coverage_max"], 1e-8)):
        bad.append(fy)
check(f"history FY{cov.index.min()}-FY{cov.index.max()} median/min/max", not bad, f"mismatched years: {bad}")

# internal consistency of sources
check("Table 61 total land = national balance sheet land (every year)",
      bool((land["A2423297K"] - bs["A2421132A"]).abs().max() < 0.15),
      f"max abs diff {(land['A2423297K'] - bs['A2421132A']).abs().max():.2f} $bn")
erp_t1 = abs_frame("310101.xlsx")["A2133251W"].dropna()       # Table 1 ERP, thousands
both = erp.index.intersection(erp_t1.index)
check("ERP 3101.0 Table 4 persons = Table 1 ERP (thousands), every quarter",
      bool((erp[both] / 1000 - erp_t1[both]).abs().max() < 0.06), f"{len(both)} quarters")
rba = pd.read_csv(RAW / "rba_f2.1-data.csv", skiprows=lambda i: i < 10, header=None, encoding="utf-8-sig",
                  usecols=[0, 4], names=["d", "y10"]).dropna()
rba["d"] = pd.to_datetime(rba["d"], format="%d-%b-%Y", errors="coerce")   # header lines become NaT
rba = rba.dropna(subset=["d"])
rba["d"] = rba["d"].dt.to_period("M").dt.to_timestamp()
rba = rba.set_index("d")["y10"].astype(float)
ov = rba.index[(rba.index > "2013-05-01") & rba.index.isin(fred.index)]
check("RBA F2.1 10-year = FRED IRLTLT01AUM156N (Jun 2013 on)",
      bool((rba[ov] - fred.loc[ov, "IRLTLT01AUM156N"]).abs().max() < 0.0015), f"{len(ov)} months")
check("Henderson Table 2 note (a) matches HDI June 2026", f"{hdi_now:,.2f}" in " ".join(pages), f"{hdi_now}")
mi_t4 = re.search(r"Single adult\s+Allowee d ([\d.]+) - - - ([\d.]+) ([\d.]+) ([\d.,]+)\s+Pensioner e ([\d.]+)",
                  "\n".join(pages))
if mi_t4:
    # Melbourne Institute Table 4 compares the June-quarter-2026 line with maximum payments (per week)
    jun26 = pd.Timestamp(2026, 6, 30)
    js_wk = (jsp[jsp.index <= jun26].iloc[-1] + es_jsp) / 52
    ra_wk = ra[ra.index <= jun26].iloc[-1] / 52
    ap_wk = (basic[basic.index <= jun26].iloc[-1] + psupp[psupp.index <= jun26].iloc[-1] + es_pen) / 52
    check("MI Table 4 (June qtr 2026): single allowee payment, Rent Assistance, pensioner payment match DSS",
          abs(float(mi_t4.group(1)) - js_wk) < 0.01 and abs(float(mi_t4.group(2)) - ra_wk) < 0.01
          and abs(float(mi_t4.group(5)) - ap_wk) < 0.01 and float(mi_t4.group(4)) == single_now,
          f"MI {mi_t4.group(1)}/{mi_t4.group(2)}/{mi_t4.group(5)} vs DSS {js_wk:.2f}/{ra_wk:.2f}/{ap_wk:.2f} a week; "
          f"line {mi_t4.group(4)}")
else:
    check("MI Table 4 row found", False)
us = pd.read_csv(RAW / "us" / "kappa_results_paper.csv").set_index("year").loc[2025]
check("US paper 2025 = 0.33 [0.18-0.59]",
      f"{us['kappa_med']:.2f} [{us['kappa_min']:.2f}-{us['kappa_max']:.2f}]" == "0.33 [0.18-0.59]")

n_fail = results.count(False)
print(f"\n{len(results) - n_fail}/{len(results)} checks PASS" + ("" if not n_fail else f"; {n_fail} FAIL"))
sys.exit(1 if n_fail else 0)
