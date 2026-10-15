"""Download every raw source for the Australian paycheck measure into data/raw/ and write MANIFEST.csv.

Run:  venv/Scripts/python.exe austax/paycheck/code/fetch.py
Everything comes from official public sources: the ABS Data API (SDMX), ABS website time-series
spreadsheets, and (for the same-window US comparison only) FRED. Files are saved byte-for-byte.
"""
import csv
import datetime as dt
import sys
import time
from pathlib import Path

import requests
import truststore

# The corporate proxy re-signs TLS; truststore makes Python use the Windows certificate store
# (verification stays on), as elsewhere in this repository (companion/code/fetch.py).
truststore.inject_into_ssl()

HERE = Path(__file__).resolve().parent
RAW = HERE.parent / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)

API = "https://data.api.abs.gov.au/rest"
SDMX_CSV = {"Accept": "application/vnd.sdmx.data+csv"}

# CPI codes (ABS CPI classification; labels in abs_cpi_v2_structure.xml, codelist CL_CPI_INDEX)
CPI_ITEMS = [
    "10001",   # All groups CPI
    "20001",   # Food and non-alcoholic beverages (group)
    "30014",   # Rents (expenditure class)
    "97559",   # New dwelling purchase by owner-occupiers (class; excludes land)
    "40055",   # Electricity
    "115524",  # Gas and other household fuels
    "40081",   # Automotive fuel
    "40080",   # Motor vehicles
    "40058",   # Furniture
    "131185",  # Carpets and other floor coverings
    "131184",  # Furniture and furnishings (sub-group = 40058 + 131185)
    "40060",   # Major household appliances
    "115484",  # Small electric household appliances
    "40098",   # Audio, visual and computing equipment
]
ITEMS = "+".join(CPI_ITEMS)

AWE_XLSX = ("https://www.abs.gov.au/statistics/labour/earnings-and-working-conditions/"
            "average-weekly-earnings-australia/may-2026/6302003.xlsx")
RPPI = ("https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/"
        "residential-property-price-indexes-eight-capital-cities/dec-2021/")

SOURCES = [
    # (file, url, headers, description)
    ("abs_cpi_v2_index_q.csv",
     f"{API}/data/ABS,CPI,2.0.0/1.{ITEMS}.10.50.Q", SDMX_CSV,
     "ABS Consumer Price Index (dataflow CPI v2.0.0, current CPI, base Sep 2025=100): index numbers, original, "
     "weighted average of eight capital cities (REGION 50), quarterly, selected groups/classes"),
    ("abs_cpi_v2_index_m.csv",
     f"{API}/data/ABS,CPI,2.0.0/1.{ITEMS}.10.50.M", SDMX_CSV,
     "ABS Consumer Price Index (dataflow CPI v2.0.0): same classes, MONTHLY. Used only in the checks, to show "
     "that from Dec qtr 2025 the quarterly series are averages of the new monthly CPI"),
    ("abs_cpi_v1_index_q.csv",
     f"{API}/data/ABS,CPI,1.1.0/1.{ITEMS}.10.50.Q", SDMX_CSV,
     "ABS Consumer Price Index (dataflow CPI v1.1.0, the former quarterly CPI, ends Sep qtr 2025): same key; "
     "used only to test the seam where ABS links the new monthly-based CPI onto the quarterly history"),
    ("abs_cpi_weights.csv",
     f"{API}/data/ABS,CPI_WEIGHTS,1.0.0/1.{ITEMS}.50.", SDMX_CSV,
     "ABS CPI weights (dataflow CPI_WEIGHTS): percentage contribution to the All groups CPI, weighted average "
     "of eight capital cities, at each reweight (2018-Q3 to 2024-Q4)"),
    ("abs_cpi_v2_structure.xml",
     f"{API}/dataflow/ABS/CPI/2.0.0?references=all", {},
     "ABS SDMX structure for dataflow CPI v2.0.0 (code lists: CL_CPI_INDEX labels, regions, measures)"),
    ("abs_cpi_weights_structure.xml",
     f"{API}/dataflow/ABS/CPI_WEIGHTS/1.0.0?references=all", {},
     "ABS SDMX structure for dataflow CPI_WEIGHTS (code lists)"),
    ("abs_awe_api.csv",
     f"{API}/data/ABS,AWE,1.0.0/3.1.3.7.TOT.10.AUS.S", SDMX_CSV,
     "ABS Average Weekly Earnings (dataflow AWE): full-time adult average weekly ordinary time earnings "
     "(MEASURE 3), earnings (ESTIMATE_TYPE 1), persons (SEX 3), private and public (SECTOR 7), all industries, "
     "original, Australia, biannual (S1 = May, S2 = November), Nov 1994 onward"),
    ("abs_awe_structure.xml",
     f"{API}/dataflow/ABS/AWE/1.0.0?references=all", {},
     "ABS SDMX structure for dataflow AWE (code lists)"),
    ("abs_6302003_awe_original.xlsx", AWE_XLSX, {},
     "ABS 6302.0 Average Weekly Earnings, Australia, May 2026, Table 3 (original, dollars); series A85002148L "
     "= Earnings; Persons; Full Time; Adult; Ordinary time earnings. Used to cross-check the API series"),
    ("abs_wpi_api.csv",
     f"{API}/data/ABS,WPI,1.2.0/1.THRPEB.7.TOT.10.AUS.Q", SDMX_CSV,
     "ABS Wage Price Index (dataflow WPI v1.2.0): quarterly index, total hourly rates of pay excluding bonuses, "
     "private and public, all industries, original, Australia, Sep qtr 1997 onward"),
    ("abs_wpi_structure.xml",
     f"{API}/dataflow/ABS/WPI/1.2.0?references=all", {},
     "ABS SDMX structure for dataflow WPI (code lists)"),
    ("abs_641602_established_house_price_index.xlsx", RPPI + "641602.xlsx", {},
     "ABS 6416.0 Residential Property Price Indexes: Eight Capital Cities, Dec 2021 (final release), Table 2 "
     "Established House Price Index; series A83728456R = weighted average of eight capital cities, original, "
     "Mar qtr 2002 to Dec qtr 2021"),
    ("abs_641608_established_house_price_index_pre2005.xlsx", RPPI + "641608.xlsx", {},
     "ABS 6416.0 Dec 2021, Table 8 Established House Price Index, pre-September quarter 2005 methodology; "
     "series A2333613R = weighted average of 8 capital cities, Jun qtr 1986 to Jun qtr 2005"),
    ("abs_res_dwell_mean_price.csv",
     f"{API}/data/ABS,RES_DWELL_ST,1.0.0/5.AUS.Q", SDMX_CSV,
     "ABS Total Value of Dwellings (dataflow RES_DWELL_ST): mean price of residential dwellings, Australia, "
     "quarterly, $'000, Sep qtr 2011 onward (all dwellings incl. land; not quality adjusted)"),
]

FRED = "https://fred.stlouisfed.org/graph/fredgraph.csv?id="
for sid, what in [
    ("AHETPI", "US average hourly earnings of production and nonsupervisory employees, total private (BLS CES), SA"),
    ("CUSR0000SAD", "US CPI-U durables, SA (the paper's Figure 5 durables deflator)"),
    ("CPIUFDNS", "US CPI-U food, NSA (the paper's Figure 5 food deflator)"),
    ("CPIENGNS", "US CPI-U energy, NSA (the paper's Figure 5 energy deflator)"),
    ("CUSR0000SAH1", "US CPI-U shelter, SA (the paper's Figure 5 shelter deflator)"),
    ("CUUR0000SEHA", "US CPI-U rent of primary residence, NSA (like-for-like with the ABS CPI Rents class)"),
]:
    SOURCES.append((f"fred_{sid}.csv", FRED + sid, {},
                    f"FRED series {sid}: {what}. Used only for the same-window US comparison"))


def get(url, headers, tries=4):
    for k in range(tries):
        try:
            r = requests.get(url, headers=headers, timeout=180)
            if r.status_code == 200 and r.content:
                return r.content
            print(f"  HTTP {r.status_code} for {url}", file=sys.stderr)
        except requests.RequestException as e:
            print(f"  {type(e).__name__} for {url}: {e}", file=sys.stderr)
        time.sleep(3 * (k + 1))
    raise SystemExit(f"FAILED: {url}")


def main():
    today = dt.date.today().isoformat()
    rows = []
    for fname, url, headers, what in SOURCES:
        body = get(url, headers)
        (RAW / fname).write_bytes(body)
        print(f"{fname:58s} {len(body):>9,d} bytes")
        rows.append({"file": fname, "url": url, "what": what, "date_pulled": today})
    with open(RAW / "MANIFEST.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["file", "url", "what", "date_pulled"])
        w.writeheader()
        w.writerows(rows)
    print("wrote", RAW / "MANIFEST.csv")


if __name__ == "__main__":
    main()
