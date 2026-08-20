# pull_family_a.py — λ assembly, Family A pull (BEA IO + SUT + GDPxInd cross-checks)
# Route note (unit 2, 2026-08-20): local curl fails (proxy, code 000) and plain
# requests fails (TLS interception); truststore.inject_into_ssl() fixes requests
# on this machine (house precedent: link-repo truststore for ddorn.net).
# Rule: live public data only; BLOCKED-and-stop, no substitution.

import os, sys, zipfile
import truststore
truststore.inject_into_ssl()
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "..", "data", "cache")
os.makedirs(CACHE, exist_ok=True)

MEMBERS = {
    # requirements tables (direct/total/domestic; the Leontief inverses, official)
    "AllTablesIO.zip":  "https://apps.bea.gov/industry/iTables%20Static%20Files/AllTablesIO.zip",
    # supply-use tables (use table carries V001/V002/V003 VA rows + final-demand cols)
    "AllTablesSUP.zip": "https://apps.bea.gov/industry/iTables%20Static%20Files/AllTablesSUP.zip",
    # GDP-by-Industry cross-check members (independent of SUT files)
    "GrossOutput.xlsx": "https://apps.bea.gov/industry/Release/XLS/GDPxInd/GrossOutput.xlsx",
    "ValueAdded.xlsx":  "https://apps.bea.gov/industry/Release/XLS/GDPxInd/ValueAdded.xlsx",
}

def pull(name, url):
    fp = os.path.join(CACHE, name)
    if os.path.exists(fp) and os.path.getsize(fp) > 0:
        return fp, "cached", os.path.getsize(fp)
    r = requests.get(url, timeout=300)
    if r.status_code != 200 or len(r.content) < 1000:
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
        print(f"{name:22s} {status:8s} {size/1e6:8.1f} MB")
    if blocked:
        print(f"\nBLOCKED: {blocked} unreachable — stopping, no substitution.")
        sys.exit(1)
    for z in ("AllTablesIO.zip", "AllTablesSUP.zip"):
        with zipfile.ZipFile(os.path.join(CACHE, z)) as zf:
            names = zf.namelist()
            print(f"\n=== {z}: {len(names)} entries ===")
            for n in names:
                print("  ", n)
