"""Australian mirror of the paper's coverage ratio (Section 9, Figure 6).

Coverage = (land rent per year) / (population x annual cost of a basic living standard for one person).
Financial years ending 30 June (FY2025 = 2024-25). Everything is read from the vendored files in data/raw/.

Numerator grid (six members, $ per year):
  land_res_y      ABS 5204.0 Table 61 residential land value at 30 June  x  FY-average 10-year bond yield
  land_res_y150   same, yield + 1.5 percentage points
  land_all_y      ABS 5204.0 Table 61 total land value (residential, commercial, rural, other) x yield
  land_all_y150   same, yield + 1.5 percentage points
  rent_ls30       0.30 x household final consumption expenditure on actual + imputed rent (5204.0 Table 42)
  rent_ls50       0.50 x the same
Denominator grid (three members, $ per person per year), each a time-weighted FY average:
  henderson       Henderson poverty line, single adult, head in workforce, including housing (Melbourne Institute)
  jobseeker       JobSeeker (Newstart before 20 Mar 2020) single, no children, maximum basic rate
                  + Energy Supplement (Clean Energy Supplement before 20 Sep 2014) + maximum Rent Assistance,
                  single, no children (DSS Guide to Social Security Law historical rate tables)
  age_pension     Age Pension single maximum basic rate + maximum pension supplement + Energy Supplement;
                  before 20 Sep 2009 the four payments the pension supplement absorbed (GST supplement,
                  pharmaceutical allowance, utilities allowance, telephone allowance at the higher rate)
Population: ABS estimated resident population, mean of the four quarter-end values in the FY.

Annualisation follows the official conventions: 52 weeks, 26 fortnights, published p.a. rates as printed.
Run:  venv\\Scripts\\python.exe austax\\coverage\\code\\build_coverage.py
"""
import csv
import datetime as dt
import re
import statistics
import sys
from pathlib import Path

import openpyxl
import pypdf

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RAW = ROOT / "data" / "raw"
OUT = ROOT / "out"
sys.dont_write_bytecode = True   # keep code/ free of __pycache__
sys.path.insert(0, str(HERE))
from htmltables import tables  # noqa: E402

LATEST_FY = 2025          # 2024-25, the latest year with ABS land values (ASNA 2024-25, 30 June 2025)
FIRST_FY = 1991           # 1990-91, the first FY in which every grid member is defined (Rent Assistance table starts 13 Jun 1990)
LAND_SHARES = (0.30, 0.50)
PREMIUM = 1.5             # percentage points
US_KAPPA_2025 = (0.33, 0.18, 0.59)   # paper, Section 9: median [min, max], 2025


# ----------------------------------------------------------------------------- generic readers
def abs_series(fname, sid):
    """ABS time-series workbook -> {date: float} for one series ID (sheet Data1)."""
    wb = openpyxl.load_workbook(RAW / fname, read_only=True, data_only=True)
    rows = list(wb["Data1"].iter_rows(values_only=True))
    ids = next(r for r in rows if r[0] == "Series ID")
    j = list(ids).index(sid)
    out = {}
    for r in rows:
        if isinstance(r[0], dt.datetime) and r[j] is not None:
            out[r[0].date()] = float(r[j])
    return out


def fy_of(d):
    return d.year + 1 if d.month >= 7 else d.year


def fy_days(fy):
    return (dt.date(fy, 6, 30) - dt.date(fy - 1, 7, 1)).days + 1


def num(s):
    return float(re.sub(r"[^\d.]", "", s.split(" Note")[0]))


def ddmmyyyy(s):
    m = re.match(r"(\d{2})/(\d{2})/(\d{4})", s.strip())
    return dt.date(int(m.group(3)), int(m.group(2)), int(m.group(1))) if m else None


# ----------------------------------------------------------------------------- numerator inputs
def land_values():
    res = abs_series("5204061_Land_Value_By_Use.xlsx", "A2423270K")    # Residential - Australia, $bn
    tot = abs_series("5204061_Land_Value_By_Use.xlsx", "A2423297K")    # Total - Australia, $bn
    bs = abs_series("5204010_National_Balance_Sheet.xlsx", "A2421132A")  # national balance sheet: land, $bn
    dw = abs_series("5204010_National_Balance_Sheet.xlsx", "A2421120T")  # dwellings, $bn (sensitivity only)
    for d, v in tot.items():   # Table 61 total must equal the balance-sheet land line
        assert abs(v - bs[d]) < 0.15, (d, v, bs[d])
    return ({d.year: v * 1e9 for d, v in res.items()}, {d.year: v * 1e9 for d, v in tot.items()},
            {d.year: v * 1e9 for d, v in dw.items()})


def housing_rent():
    act = abs_series("5204042_Household_FCE.xlsx", "A2422100A")   # actual rent for housing, $m, FY
    imp = abs_series("5204042_Household_FCE.xlsx", "A2422101C")   # imputed rent for owner-occupiers, $m, FY
    return {d.year: (act[d] + imp[d]) * 1e6 for d in act}


def bond_yield_fy():
    """FRED IRLTLT01AUM156N (OECD MEI, monthly) -> FY mean of the 12 months July..June, per cent."""
    months = {}
    with open(RAW / "IRLTLT01AUM156N.csv", newline="") as f:
        for row in csv.DictReader(f):
            d = dt.date.fromisoformat(row["observation_date"])
            months[d] = float(row["IRLTLT01AUM156N"])
    by_fy = {}
    for d, v in months.items():
        by_fy.setdefault(fy_of(d), []).append(v)
    return {fy: sum(v) / 12 for fy, v in by_fy.items() if len(v) == 12}, months


def rba_cross_check(months):
    """RBA F2.1 FCMYGBAG10 (monthly) must equal the FRED series in every overlapping month after the RBA table's
    first month (May 2013, 3.324 vs 3.225 in FRED; the RBA table's first observation appears to cover part of
    the month only). FRED is the series used; it runs unspliced from July 1969."""
    with open(RAW / "rba_f2.1-data.csv", encoding="utf-8-sig") as f:
        lines = [ln for ln in csv.reader(f) if ln]
    ids = next(ln for ln in lines if ln[0] == "Series ID")
    j = ids.index("FCMYGBAG10")
    n, worst = 0, 0.0
    for ln in lines:
        try:
            d = dt.datetime.strptime(ln[0], "%d-%b-%Y").date().replace(day=1)
        except ValueError:
            continue
        if d in months and ln[j] and d > dt.date(2013, 5, 1):
            worst = max(worst, abs(float(ln[j]) - months[d]))
            n += 1
    assert n > 100 and worst < 0.0015, (n, worst)
    return n, worst


def population_fy():
    erp = abs_series("310104.xlsx", "A2060842F")   # ERP, persons, Australia, quarterly (Jun/Sep/Dec/Mar)
    by_fy = {}
    for d, v in erp.items():   # quarter ends Sep and Dec belong to the FY ending the next June; Mar, Jun to this one
        by_fy.setdefault(fy_of(d), []).append(v)
    return {fy: sum(v) / 4 for fy, v in by_fy.items() if len(v) == 4}


# ----------------------------------------------------------------------------- denominators
def quarter_days(fy):
    """Days in each quarter of financial year fy (Sept quarter = Jul-Sep of fy-1, ..., Jun quarter = Apr-Jun of fy)."""
    b = [dt.date(fy - 1, 7, 1), dt.date(fy - 1, 10, 1), dt.date(fy, 1, 1), dt.date(fy, 4, 1), dt.date(fy, 7, 1)]
    return {q: (b[i + 1] - b[i]).days for i, q in enumerate(("Sept", "Dec", "Mar", "Jun"))}


def henderson():
    """Single person, head in workforce, including housing, $ per week, every quarter since Sept 1973.
    Melbourne Institute method (p. 2 of the release): line(q) = line(current) x HDI(q) / HDI(current)."""
    pdf = pypdf.PdfReader(RAW / "henderson" / "Poverty-Lines-Australia-June-Quarter-2026.pdf")
    text = " ".join(p.extract_text() for p in pdf.pages)
    t1 = text[text.index("Table 1: Poverty Lines"):]
    t1 = t1[t1.index("Head in workforce"):]
    single_now = num(re.search(r"Single person\s+([\d,]+\.\d\d)", t1).group(1))
    i2 = text.index("Table 2: Seasonally adjusted")
    t2 = text[i2:text.index("Sources:", i2)]          # stop before Table 3, whose rows share the year format
    hdi = {}
    for m in re.finditer(r"(\d{4})/(\d{2})\s+([\d,.]+)\s+([\d,.]+)\s+([\d,.]+)\s+([\d,.]+)", t2):
        fy = int(m.group(1)) + 1
        for k, q in enumerate(("Sept", "Dec", "Mar", "Jun")):
            hdi[(fy, q)] = num(m.group(3 + k))
    hdi_now = hdi[(2026, "Jun")]
    note = re.search(r"June quarter\s+2026 of \$([\d,]+\.\d\d)", text)
    assert note and abs(num(note.group(1)) - hdi_now) < 0.005, "Table 2 June 2026 HDI != note (a)"
    assert len(hdi) == 4 * (2026 - 1973), len(hdi)
    assert hdi[(1974, "Sept")] == 53.43 and hdi[(2025, "Jun")] == 1090.69, "Table 2 parse"
    weekly = {k: single_now * v / hdi_now for k, v in hdi.items()}
    return weekly, single_now, hdi


def henderson_fy(weekly, fy):
    qd = quarter_days(fy)
    assert sum(qd.values()) == fy_days(fy)
    return sum(52 * weekly[(fy, q)] * n for q, n in qd.items()) / fy_days(fy)


class Step:
    """A step function of annual amounts by effective date; value(d) = amount at the latest date <= d."""

    def __init__(self, pts, start=None, end=None):
        self.pts = sorted(pts)
        self.start, self.end = start, end   # active window [start, end), else zero

    def value(self, d):
        if (self.start and d < self.start) or (self.end and d >= self.end):
            return 0.0
        v = None
        for when, amt in self.pts:
            if when <= d:
                v = amt
        if v is None:
            raise ValueError(f"no rate in force on {d}")
        return v


def fy_average(steps, fy):
    """Time-weighted FY average of the sum of several annual-rate step functions (weights = days)."""
    d, end, tot = dt.date(fy - 1, 7, 1), dt.date(fy, 6, 30), 0.0
    while d <= end:
        tot += sum(s.value(d) for s in steps)
        d += dt.timedelta(days=1)
    return tot / fy_days(fy)


def dss_table(page, header_start):
    for t in tables(RAW / "dss" / page):
        if t and t[0] and t[0][0].startswith(header_start[0]) and all(h in " ".join(t[0]) for h in header_start[1:]):
            yield t


def jobseeker_steps():
    # 5.2.1.20 Table 5: over 21 single UB/SB, NSA, JSP - Dec 1987 to present; $ pw until the in-table header
    # "From 20 March 2020, rates are in dollars per fortnight", $ pf after it.
    page = "g_5_2_1_20.html"
    t = next(t for t in tables(RAW / "dss" / page) if len(t) > 1 and t[1][0] == "13/12/1987")
    pts, per = [], 52
    for r in t[1:]:
        if r[0].startswith("Date") and "fortnight" in " ".join(r):
            per = 26
            continue
        d = ddmmyyyy(r[0])
        if d and len(r) > 1:
            pts.append((d, per * num(r[1])))
    base = Step(pts)
    # 5.2.6.10 Table 1: maximum RA, single, no children ($ pf), from 13 Jun 1990
    t = next(t for t in tables(RAW / "dss" / "g_5_2_6_10.html") if len(t) > 2 and t[2][0] == "13/06/1990")
    ra = Step([(ddmmyyyy(r[0]), 26 * num(r[1])) for r in t[2:] if ddmmyyyy(r[0])])
    # 5.2.9.30 Clean Energy Supplement (allowances, single no children, $ p.a.) then 5.1.10.20 ES ($ p.a.)
    ces = ces_rates("Allowance rates")
    es_now = es_current("JSP")
    es = Step(ces + [(dt.date(2014, 9, 20), es_now)], start=dt.date(2013, 3, 20))
    return {"base": base, "ra": ra, "es": es}


def ces_rates(row_start):
    t = next(t for t in tables(RAW / "dss" / "g_5_2_9_30.html") if t and t[0][0] == "Qualifying payment type")
    dates = [dt.datetime.strptime(x, "%d/%m/%Y" if len(x) == 10 else "%d/%m/%y").date() for x in t[1]]
    row = next(r for r in t if r[0].startswith(row_start))
    first = [num(cell.split()[0]) for cell in row[1:]]   # first figure in each cell = single (no children)
    return list(zip(dates, first))


def es_current(row_start):
    t = next(t for t in tables(RAW / "dss" / "g_5_1_10_20.html") if t and t[0][0] == "Qualifying payment type")
    row = next(r for r in t if r[0].startswith(row_start))
    return num(row[1].split()[0])      # first figure = single (no children) / single pensioner


def age_pension_steps():
    reform = dt.date(2009, 9, 20)
    t = next(t for t in tables(RAW / "dss" / "g_5_2_2_10.html") if t and "Standard rate" in " ".join(t[0]))
    basic = Step([(ddmmyyyy(r[0]), num(r[1])) for r in t[1:] if ddmmyyyy(r[0])])
    ps_tabs = [t for t in tables(RAW / "dss" / "g_5_2_8_10.html") if t and t[0][0] == "Date"]
    gst = Step([(ddmmyyyy(r[0]), num(r[1])) for r in ps_tabs[0][1:] if ddmmyyyy(r[0])],
               start=dt.date(2000, 7, 1), end=reform)
    ps = Step([(ddmmyyyy(r[0]), num(r[1])) for r in ps_tabs[1][2:] if ddmmyyyy(r[0])], start=reform)
    t = next(t for t in tables(RAW / "dss" / "g_5_2_6_50.html") if t and t[0][0] == "Date")
    pha = Step([(ddmmyyyy(r[0]), 26 * num(r[1])) for r in t[1:] if ddmmyyyy(r[0])],
               start=dt.date(1990, 11, 1), end=reform)
    t = next(t for t in tables(RAW / "dss" / "g_5_2_6_100.html") if t and t[0][0] == "Date")
    ua = Step([(ddmmyyyy(r[0]), num(r[1])) for r in t[1:] if ddmmyyyy(r[0])],
              start=dt.date(2005, 3, 20), end=reform)
    tal_tabs = [t for t in tables(RAW / "dss" / "g_5_2_6_40.html") if t and t[0][0] == "Date"]
    std = next(t for t in tal_tabs if len(t[0]) == 3 and t[1][0] == "01/07/1992" and "Rate per annum" in t[0][1])
    hi = next(t for t in tal_tabs if len(t[0]) == 5)
    tal_pts = [(ddmmyyyy(r[0]), num(r[1])) for r in std[1:] if ddmmyyyy(r[0])]
    tal_pts += [(ddmmyyyy(r[0]), num(r[3])) for r in hi[1:] if ddmmyyyy(r[0])]   # higher rate from 20 Mar 2008
    tal = Step(tal_pts, start=dt.date(1992, 7, 1), end=reform)
    ces = ces_rates("Pensions")
    es = Step(ces + [(dt.date(2014, 9, 20), es_current("Pensions"))], start=dt.date(2013, 3, 20))
    return {"basic": basic, "gst_supp": gst, "pension_supp": ps, "pharm": pha, "utilities": ua,
            "telephone": tal, "es": es}


# ----------------------------------------------------------------------------- build
def main():
    res, tot, dwell = land_values()
    rent = housing_rent()
    y, months = bond_yield_fy()
    n_rba, worst = rba_cross_check(months)
    pop = population_fy()
    hw, single_now, hdi = henderson()
    js, ap = jobseeker_steps(), age_pension_steps()

    rows = []
    for fy in range(FIRST_FY, LATEST_FY + 1):
        r = {"fy_end": fy, "financial_year": f"{fy - 1}-{str(fy)[2:]}",
             "land_res_bn": res[fy] / 1e9, "land_all_bn": tot[fy] / 1e9, "bond10_pct": y[fy],
             "housing_rent_bn": rent[fy] / 1e9, "population": pop[fy]}
        num_ = {
            "land_res_y": res[fy] * y[fy] / 100, "land_res_y150": res[fy] * (y[fy] + PREMIUM) / 100,
            "land_all_y": tot[fy] * y[fy] / 100, "land_all_y150": tot[fy] * (y[fy] + PREMIUM) / 100,
            "rent_ls30": LAND_SHARES[0] * rent[fy], "rent_ls50": LAND_SHARES[1] * rent[fy],
        }
        den = {"henderson": henderson_fy(hw, fy), "jobseeker": fy_average(js.values(), fy),
               "age_pension": fy_average(ap.values(), fy)}
        for k, v in num_.items():
            r[f"rent_{k}_bn"] = v / 1e9
        for k, v in den.items():
            r[f"cost_{k}"] = v
        members = {}
        for nk, nv in num_.items():
            for dk, dv in den.items():
                members[f"k_{nk}__{dk}"] = nv / (pop[fy] * dv)
        vals = list(members.values())
        r.update({"coverage_min": min(vals), "coverage_median": statistics.median(vals),
                  "coverage_max": max(vals), "n_members": len(vals)})
        fam_land = [v for k, v in members.items() if "_land_" in k]
        fam_rent = [v for k, v in members.items() if "_rent_ls" in k]
        r["coverage_median_landvalue_family"] = statistics.median(fam_land)
        r["coverage_median_rentshare_family"] = statistics.median(fam_rent)
        r["rent_per_person_median"] = statistics.median(num_.values()) / pop[fy]
        # diagnostics: residential land rent at the bond yield relative to all housing rent (land + buildings);
        # household disposable income per head (Melbourne Institute Table 2, seasonally adjusted, ABS-derived)
        r["diag_res_land_at_yield_over_housing_rent"] = num_["land_res_y"] / rent[fy]
        hdi_fy = henderson_fy({k: v for k, v in hdi.items()}, fy)   # same day-weighting, 52 x weekly
        r["hdi_per_head_annual"] = hdi_fy
        r["rent_per_person_over_hdi_per_head"] = r["rent_per_person_median"] / hdi_fy
        for dk, dv in den.items():
            r[f"cost_{dk}_over_hdi_per_head"] = dv / hdi_fy
        r.update(members)
        rows.append(r)

    OUT.mkdir(exist_ok=True)
    cols = list(rows[0].keys())
    with open(OUT / "coverage.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({k: (f"{v:.10g}" if isinstance(v, float) else v) for k, v in r.items()})

    last, first = rows[-1], rows[0]
    # ---------------------------------------------------------------- sensitivities (not in the grid)
    sens = sensitivities(last, res, tot, dwell, rent, y, pop, hw, js, ap)

    head = headline_rows(last, first, single_now, sens)
    with open(OUT / "headline.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["id", "value", "claim", "definition", "period", "source", "produced_by"])
        w.writeheader()
        for h in head:
            w.writerow(h)

    print(f"RBA F2.1 = FRED in {n_rba} overlapping months (max abs diff {worst:.4f})")
    print(f"{last['financial_year']}: coverage median {last['coverage_median']:.3f} "
          f"[{last['coverage_min']:.3f}-{last['coverage_max']:.3f}]  (US 2025: 0.33 [0.18-0.59])")
    print(f"  land-value family median {last['coverage_median_landvalue_family']:.3f}; "
          f"rent-share family median {last['coverage_median_rentshare_family']:.3f}")
    print(f"  rent per person (median of six numerators) ${last['rent_per_person_median']:,.0f}")
    for k in ("henderson", "jobseeker", "age_pension"):
        print(f"  cost {k}: ${last['cost_' + k]:,.0f} per year")
    print(f"{first['financial_year']}: coverage median {first['coverage_median']:.3f} "
          f"[{first['coverage_min']:.3f}-{first['coverage_max']:.3f}]")
    for k, v in sens.items():
        print(f"  sensitivity {k}: {v if isinstance(v, str) else round(v, 4)}")
    print("wrote", OUT / "coverage.csv", "and", OUT / "headline.csv")


def sensitivities(last, res, tot, dwell, rent, y, pop, hw, js, ap):
    fy = last["fy_end"]
    s = {}
    # (1) average of opening and closing land stock instead of the 30 June closing stock
    avg = []
    for scope in (res, tot):
        stock = (scope[fy] + scope[fy - 1]) / 2
        avg += [stock * y[fy] / 100, stock * (y[fy] + PREMIUM) / 100]
    nums = avg + [LAND_SHARES[0] * rent[fy], LAND_SHARES[1] * rent[fy]]
    dens = [last["cost_henderson"], last["cost_jobseeker"], last["cost_age_pension"]]
    s["median_with_average_land_stock"] = statistics.median(n / (pop[fy] * d) for n in nums for d in dens)
    # (2) Australian land share of residential property value, applied to housing rent
    share = res[fy] / (res[fy] + dwell[fy])
    s["abs_residential_land_share_of_value"] = share
    s["rentshare_with_abs_land_share_median"] = statistics.median(share * rent[fy] / (pop[fy] * d) for d in dens)
    # (3) rates in force now (DSS rates from 20 Sep 2026; Henderson June quarter 2026) against 2024-25 rent
    now = dt.date(2026, 9, 20)
    cur = [52 * hw[(2026, "Jun")], sum(st.value(now) for st in js.values()), sum(st.value(now) for st in ap.values())]
    nums6 = [last[f"rent_{k}_bn"] * 1e9 for k in ("land_res_y", "land_res_y150", "land_all_y", "land_all_y150",
                                                    "rent_ls30", "rent_ls50")]
    s["median_latest_rates_vs_2024_25_rent"] = statistics.median(n / (pop[fy] * d) for n in nums6 for d in cur)
    s["cost_now_henderson"], s["cost_now_jobseeker"], s["cost_now_age_pension"] = cur
    # (4) Henderson line as published at the time (four 2024-25 releases) instead of the latest-vintage index
    pub = henderson_as_published()
    qd = quarter_days(fy)
    h_pub = sum(52 * pub[q] * n for q, n in qd.items()) / fy_days(fy)
    s["cost_henderson_as_published"] = h_pub
    dens_pub = [h_pub, last["cost_jobseeker"], last["cost_age_pension"]]
    s["median_with_henderson_as_published"] = statistics.median(n / (pop[fy] * d) for n in nums6 for d in dens_pub)
    return s


AS_PUBLISHED = {"Sept": "Poverty-Lines-Australia-September-2024.pdf",
                "Dec": "Poverty-Lines-Australia-December-Quarter-2024.pdf",
                "Mar": "Poverty-Lines-Australia-March-Quarter-2025.pdf",
                "Jun": "Poverty-Lines-Australia-June-Quarter-2025.pdf"}


def henderson_as_published():
    out = {}
    for q, fname in AS_PUBLISHED.items():
        text = " ".join(pg.extract_text() for pg in pypdf.PdfReader(RAW / "henderson" / fname).pages)
        t1 = text[text.index("Table 1: Poverty Lines"):]
        t1 = t1[t1.index("Head in workforce"):]
        out[q] = num(re.search(r"Single person\s+([\d,]+\.\d\d)", t1).group(1))
    return out


def argext(row, fn):
    members = {k: v for k, v in row.items() if k.startswith("k_")}
    return fn(members, key=members.get)[2:]


def headline_rows(last, first, single_now, sens):
    p = last["financial_year"]
    src_land = ("ABS 5204.0 Australian System of National Accounts 2024-25, Table 61 (A2423270K residential, "
                "A2423297K total) https://www.abs.gov.au/statistics/economy/national-accounts/"
                "australian-system-national-accounts/2024-25/5204061_Land_Value_By_Use.xlsx; 10-year bond yield "
                "FRED IRLTLT01AUM156N (= RBA F2.1 FCMYGBAG10); HFCE actual + imputed rent 5204.0 Table 42 "
                "(A2422100A + A2422101C); ERP 3101.0 Table 4 (A2060842F)")
    src_den = ("Melbourne Institute, Poverty Lines: Australia, June Quarter 2026 (Tables 1-2); DSS Guide to "
               "Social Security Law 5.2.1.20, 5.2.6.10, 5.2.2.10, 5.2.8.10, 5.2.6.50, 5.2.6.100, 5.2.6.40, "
               "5.2.9.30, 5.1.10.20 (historical and current rate tables, reviewed to 21 Sep 2026)")
    by = "austax/coverage/code/build_coverage.py main() -> out/coverage.csv"
    rows = [
        dict(id="coverage_median", value=f"{last['coverage_median']:.2f}",
             claim=(f"Taxing all Australian land rent in {p} could have funded about "
                    f"{last['coverage_median']:.2f} of a basic living standard for every resident "
                    f"(range {last['coverage_min']:.2f} to {last['coverage_max']:.2f} across 18 constructions)."),
             definition="median across 6 land-rent constructions x 3 basic-living-cost benchmarks of "
                        "land rent / (population x annual cost per person)",
             period=f"financial year {p} (land values at 30 June 2025)", source=src_land + "; " + src_den,
             produced_by=by + " column coverage_median, last row"),
        dict(id="coverage_min", value=f"{last['coverage_min']:.2f}", claim="lowest grid member",
             definition=f"grid member {argext(last, min)} (numerator__denominator)",
             period=p, source=src_land + "; " + src_den, produced_by=by + " column coverage_min"),
        dict(id="coverage_max", value=f"{last['coverage_max']:.2f}", claim="highest grid member",
             definition=f"grid member {argext(last, max)} (numerator__denominator)",
             period=p, source=src_land + "; " + src_den, produced_by=by + " column coverage_max"),
        dict(id="coverage_median_landvalue_family", value=f"{last['coverage_median_landvalue_family']:.2f}",
             claim="median of the 12 members that capitalise ABS land values at the bond yield",
             definition="land value x yield (or yield + 1.5) / (population x cost)", period=p, source=src_land,
             produced_by=by + " column coverage_median_landvalue_family"),
        dict(id="coverage_median_rentshare_family", value=f"{last['coverage_median_rentshare_family']:.2f}",
             claim="median of the 6 members that take 30 or 50 per cent of housing rents as land rent",
             definition="land share x (actual + imputed rent) / (population x cost)", period=p, source=src_land,
             produced_by=by + " column coverage_median_rentshare_family"),
        dict(id="rent_per_person", value=f"{last['rent_per_person_median']:.0f}",
             claim=f"Measured land rent was about ${last['rent_per_person_median']:,.0f} per resident in {p} "
                   "(median of the six constructions).",
             definition="median of six land-rent constructions / mean estimated resident population", period=p,
             source=src_land, produced_by=by + " column rent_per_person_median"),
        dict(id="cost_henderson", value=f"{last['cost_henderson']:.0f}",
             claim=f"Henderson poverty line, single adult in the workforce including housing: "
                   f"${last['cost_henderson']:,.0f} a year in {p} (${single_now:.2f} a week in the June quarter 2026).",
             definition="52 x weekly line, quarters weighted by days; latest-vintage income index", period=p,
             source=src_den, produced_by=by + " column cost_henderson"),
        dict(id="cost_jobseeker", value=f"{last['cost_jobseeker']:.0f}",
             claim=f"Maximum JobSeeker single (no children) + Energy Supplement + maximum Rent Assistance: "
                   f"${last['cost_jobseeker']:,.0f} a year in {p}.",
             definition="26 x fortnightly rates, rate periods weighted by days", period=p, source=src_den,
             produced_by=by + " column cost_jobseeker"),
        dict(id="cost_age_pension", value=f"{last['cost_age_pension']:.0f}",
             claim=f"Maximum single Age Pension with pension and energy supplements: "
                   f"${last['cost_age_pension']:,.0f} a year in {p}.",
             definition="published p.a. rates (26 fortnights), rate periods weighted by days", period=p,
             source=src_den, produced_by=by + " column cost_age_pension"),
        dict(id="coverage_median_first_year", value=f"{first['coverage_median']:.2f}",
             claim=(f"In {first['financial_year']} the same grid gave {first['coverage_median']:.2f} "
                    f"(range {first['coverage_min']:.2f} to {first['coverage_max']:.2f})."),
             definition="as coverage_median", period=f"financial year {first['financial_year']}",
             source=src_land + "; " + src_den, produced_by=by + " column coverage_median, first row"),
        dict(id="us_comparison", value="0.33 [0.18-0.59]",
             claim="The paper's US figure for 2025, against a much leaner basket (Orshansky 1963, CPI-updated).",
             definition="paper Section 9 / Figure 6", period="US 2025",
             source="Bage and Wilson (2026), SSRN 7226858, Section 9", produced_by="pinning/data/kappa_results.csv"),
        dict(id="sens_latest_rates", value=f"{sens['median_latest_rates_vs_2024_25_rent']:.2f}",
             claim="Sensitivity: the median if 2024-25 land rent is set against rates in force now "
                   "(DSS from 20 Sep 2026; Henderson June quarter 2026). Timing mismatch, lower bound.",
             definition="as coverage_median with current denominators", period="rent 2024-25; rates Sep 2026",
             source=src_den, produced_by="build_coverage.py sensitivities() (3)"),
        dict(id="sens_average_land_stock", value=f"{sens['median_with_average_land_stock']:.2f}",
             claim="Sensitivity: the median with the average of opening and closing land values.",
             definition="(land at 30 Jun 2024 + land at 30 Jun 2025)/2 in the four land-value members", period=p,
             source=src_land, produced_by="build_coverage.py sensitivities() (1)"),
        dict(id="sens_henderson_as_published", value=f"{sens['median_with_henderson_as_published']:.2f}",
             claim=(f"Sensitivity: with the Henderson line as published during 2024-25 "
                    f"(${sens['cost_henderson_as_published']:,.0f} a year rather than ${last['cost_henderson']:,.0f}; "
                    "later releases revised the income index) the median is this."),
             definition="as coverage_median, Henderson member from the four 2024-25 releases' Table 1", period=p,
             source="Melbourne Institute, Poverty Lines: Australia, Sept 2024, Dec 2024, Mar 2025, Jun 2025",
             produced_by="build_coverage.py sensitivities() (4)"),
        dict(id="diag_res_land_at_yield_over_housing_rent",
             value=f"{last['diag_res_land_at_yield_over_housing_rent']:.2f}",
             claim=("Diagnostic: residential land value times the bond yield exceeds all actual and imputed housing "
                    "rent (land and buildings together) by this factor, so the bond-yield constructions overstate "
                    "the current rent flow."),
             definition="A2423270K x FY-average 10-year yield / (A2422100A + A2422101C)", period=p,
             source="ABS 5204.0 Tables 42, 61; FRED IRLTLT01AUM156N",
             produced_by=by + " column diag_res_land_at_yield_over_housing_rent"),
        dict(id="sens_abs_land_share", value=f"{sens['rentshare_with_abs_land_share_median']:.2f}",
             claim=(f"Sensitivity: residential land is {sens['abs_residential_land_share_of_value']:.0%} of "
                    "residential property value in the ABS balance sheet; using that share of housing rents "
                    "instead of 30 or 50 per cent gives this median."),
             definition="A2423270K / (A2423270K + A2421120T) x housing rent / (population x cost)", period=p,
             source="ABS 5204.0 Tables 10, 42, 61", produced_by="build_coverage.py sensitivities() (2)"),
    ]
    return rows


if __name__ == "__main__":
    main()
