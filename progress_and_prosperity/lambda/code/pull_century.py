# pull_century.py — λ unit 3: historical members.
# BEA's own caveat, quoted for the ledger and the figure caption: the historical
# benchmark tables "should not be used as a time series" (classification changes,
# no comprehensive back-revision). We use them AS BENCHMARK POINTS with the
# splice and the caveat stated, never smoothed over.
# URL inventory harvested from bea.gov/industry/historical-benchmark-input-output-tables
# via the in-app browser, 2026-08-20 (page 403s nothing here; apps.bea.gov serves
# truststore-requests directly).

import os, sys, zipfile
import truststore
truststore.inject_into_ssl()
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "..", "data", "cache")
os.makedirs(CACHE, exist_ok=True)
BASE = "https://apps.bea.gov/industry/zip/"

MEMBERS = {
    # 85-industry-level benchmark packages (Excel), SIC era
    "47IOexcel.zip":            BASE + "47IOexcel.zip",
    "58IOexcel.zip":            BASE + "58IOexcel.zip",
    "58IOTRexcel.zip":          BASE + "58IOTRexcel.zip",
    "63IO85-levelexcel.zip":    BASE + "63IO85-levelexcel.zip",
    "67IO85-levelexcel.zip":    BASE + "67IO85-levelexcel.zip",
    "72IO85-levelexcel.zip":    BASE + "72IO85-levelexcel.zip",
    "77IO85-levelexcel.zip":    BASE + "77IO85-levelexcel.zip",
    # two-digit benchmark packages, late SIC era
    "ndn0125.zip":              BASE + "ndn0125.zip",   # 1982 two-digit
    "ndn0019.zip":              BASE + "ndn0019.zip",   # 1987 two-digit make and use
    "ndn0180.zip":              BASE + "ndn0180.zip",   # 1992 two-digit
    # historical GDP-by-industry (annual 1947–1997, NAICS-basis retrospective)
    "AllTablesHIST.zip":        "https://apps.bea.gov/industry/iTables%20Static%20Files/AllTablesHIST.zip",
}

def pull(name, url):
    fp = os.path.join(CACHE, name)
    if os.path.exists(fp) and os.path.getsize(fp) > 0:
        return fp, "cached", os.path.getsize(fp)
    r = requests.get(url, timeout=300)
    if r.status_code != 200 or len(r.content) < 500:
        return None, f"FAIL http={r.status_code} bytes={len(r.content)}", 0
    with open(fp, "wb") as f:
        f.write(r.content)
    return fp, "pulled", len(r.content)

if __name__ == "__main__":
    ledger, blocked = [], []
    for name, url in MEMBERS.items():
        fp, status, size = pull(name, url)
        ledger.append((name, status, size))
        if fp is None:
            blocked.append(name)
    print("=== pull ledger ===")
    for name, status, size in ledger:
        print(f"{name:26s} {status:8s} {size/1e6:7.2f} MB")
    if blocked:
        print(f"\nBLOCKED: {blocked} unreachable — stopping, no substitution.")
        sys.exit(1)
    for name, _, _ in ledger:
        if name.endswith(".zip"):
            with zipfile.ZipFile(os.path.join(CACHE, name)) as zf:
                print(f"\n=== {name} ===")
                for n in zf.namelist():
                    print("  ", n)
