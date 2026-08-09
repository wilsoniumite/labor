# fetch.py — download-and-cache layer for the companion panel (house pattern:
# lambda_compute2's pull/cache/courtesy machinery, adapted from FRED-CSV to
# arbitrary files). Every URL here was probed live 2026-08-06 (probe_urls.py +
# session log). Validation: HTTP 200 is NOT trusted — zip files must open and
# list members; xls/xlsx must carry their magic bytes. A file that fails
# validation is deleted from cache and reported, never silently kept.
#
# Windows TLS note: truststore injects the OS certificate stack. ddorn.net
# serves an incomplete TLS chain that browsers repair via AIA chasing; the OS
# stack does this, Python's bundled certifi does not. No verification is
# disabled anywhere.
import os
import time
import zipfile

import truststore
truststore.inject_into_ssl()
import requests

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "academic research; contact wilsontomass@gmail.com"}
HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.normpath(os.path.join(HERE, "..", "cache"))
os.makedirs(CACHE, exist_ok=True)

DDORN = "https://www.ddorn.net/data/{f}"
BLS_OES = "https://www.bls.gov/oes/special-requests/{f}"
CENSUS = "https://www2.census.gov/programs-surveys/demo/guidance/industry-occupation/{f}"

# name -> (url, kind) ; kind drives validation: "zip" | "xls" | "xlsx"
MANIFEST = {}

# --- ddorn.net: task measures + occ crosswalks (cite Autor-Dorn 2013 AER) ---
for f in ["occ1990dd_task_alm.zip", "occ1990dd_task_offshore.zip",
          "occ1950_occ1990dd.zip", "occ1960_occ1990dd.zip",
          "occ1970_occ1990dd.zip", "occ1980_occ1990dd.zip",
          "occ1990_occ1990dd.zip", "occ2000_occ1990dd.zip",
          "occ2005_occ1990dd.zip", "occ2010_occ1990dd.zip",
          "subfile_occ1990dd_occgroups.zip"]:
    MANIFEST[f] = (DDORN.format(f=f), "zip")

# --- O*NET 30.3 text database (CC-BY 4.0) ---
MANIFEST["db_30_3_text.zip"] = (
    "https://www.onetcenter.org/dl_files/database/db_30_3_text.zip", "zip")

# --- OEWS national files: Nov-era 1997-2002 (oesYYnat), May-era 2003+ (oesmYYnat).
#     The oesmYYnat pattern for 1997-2002 returns a 20-byte HTML stub — wrong-era
#     pattern, discovered at probe time; do not "fix" back. ---
for y in range(1997, 2003):
    MANIFEST[f"oes{y % 100:02d}nat.zip"] = (BLS_OES.format(f=f"oes{y % 100:02d}nat.zip"), "zip")
for y in range(2003, 2026):
    MANIFEST[f"oesm{y % 100:02d}nat.zip"] = (BLS_OES.format(f=f"oesm{y % 100:02d}nat.zip"), "zip")

# --- SOC revision crosswalks (BLS) ---
MANIFEST["soc_2000_to_2010_crosswalk.xls"] = (
    "https://www.bls.gov/soc/soc_2000_to_2010_crosswalk.xls", "xls")
MANIFEST["soc_2010_to_2018_crosswalk.xlsx"] = (
    "https://www.bls.gov/soc/2018/soc_2010_to_2018_crosswalk.xlsx", "xlsx")

# --- Census occupation code lists (Census occ <-> SOC, by vintage) ---
MANIFEST["2002-census-occupation-codes.xls"] = (
    CENSUS.format(f="2002-census-occupation-codes.xls"), "xls")
MANIFEST["2010-occ-codes-with-crosswalk-from-2002-2011.xls"] = (
    CENSUS.format(f="2010-occ-codes-with-crosswalk-from-2002-2011.xls"), "xls")
MANIFEST["2018-occupation-code-list-and-crosswalk.xlsx"] = (
    CENSUS.format(f="2018-occupation-code-list-and-crosswalk.xlsx"), "xlsx")

# --- family B (unit 3): capability sources, URLs resolved live 2026-08-06 ---
MANIFEST["epoch_benchmark_data.zip"] = ("https://epoch.ai/data/benchmark_data.zip", "zip")
MANIFEST["epoch_ai_models.zip"] = ("https://epoch.ai/data/ai_models.zip", "zip")
RAW_GH = "https://raw.githubusercontent.com/{repo}/main/{path}"
MANIFEST["metr_runs_1_1.jsonl"] = (
    RAW_GH.format(repo="METR/eval-analysis-public",
                  path="reports/time-horizon-1-1/data/raw/runs.jsonl"), "jsonl")
MANIFEST["metr_README.md"] = (
    RAW_GH.format(repo="METR/eval-analysis-public", path="README.md"), "text")
MANIFEST["eloundou_occ_level.csv"] = (
    RAW_GH.format(repo="openai/GPTs-are-GPTs", path="data/occ_level.csv"), "csv")
MANIFEST["eloundou_LICENSE.txt"] = (
    RAW_GH.format(repo="openai/GPTs-are-GPTs", path="LICENSE"), "text")

# --- family C (unit 4): wedge layer, URLs resolved live 2026-08-06 ---
for y in [1999, 2000, 2001, 2025]:
    MANIFEST[f"unionstats_occ_{y}.xlsx"] = (
        f"https://www.unionstats.com/occ/xls/occ_{y}.xlsx", "xlsx")
for n in range(49, 56):     # CPS certification/licensing tables; picked by title
    MANIFEST[f"cpsaat{n}.xlsx"] = (f"https://www.bls.gov/cps/cpsaat{n}.xlsx", "xlsx")

# --- unit 5: O*NET release archive (annual majors; URLs resolved live
#     2026-08-06 off db_releases.html — old-style through 20.0, text-style
#     after; 30.3 already in the manifest above) ---
ONET_OLD = ["5_1", "7_0", "9_0", "11_0", "13_0", "14_0", "15_0", "16_0",
            "17_0", "18_0", "19_0", "20_0"]
ONET_TXT = ["21_0", "22_0", "23_0", "24_0", "25_0", "26_0", "27_0",
            "28_0", "29_0", "30_0"]
for v in ONET_OLD:
    f = f"db_{v.replace('_0', '0').replace('_1', '1') if len(v) == 3 else v}.zip"
    MANIFEST[f"onet_{v}.zip"] = (f"https://www.onetcenter.org/dl_files/{f}", "zip")
for v in ONET_TXT:
    MANIFEST[f"onet_{v}.zip"] = (
        f"https://www.onetcenter.org/dl_files/database/db_{v}_text.zip", "zip")
MANIFEST["onet_releases_page.html"] = (
    "https://www.onetcenter.org/db_releases.html", "html")


def _valid(fp, kind):
    if not os.path.exists(fp) or os.path.getsize(fp) < 1024:
        return False
    head = open(fp, "rb").read(8)
    if kind == "zip" or kind == "xlsx":          # xlsx is a zip container
        if not head.startswith(b"PK"):
            return False
        if kind == "zip":
            try:
                if not zipfile.ZipFile(fp).namelist():
                    return False
            except zipfile.BadZipFile:
                return False
        return True
    if kind == "xls":                             # OLE compound document magic
        return head.startswith(b"\xd0\xcf\x11\xe0")
    if kind == "jsonl":                           # first line parses as a JSON object
        try:
            import json
            with open(fp, encoding="utf8") as fh:
                return isinstance(json.loads(fh.readline()), dict)
        except (ValueError, UnicodeDecodeError):
            return False
    if kind == "csv":
        with open(fp, encoding="utf8", errors="replace") as fh:
            first = fh.readline()
        return ("," in first) and not first.lstrip().startswith("<")
    if kind == "text":
        return not head.startswith(b"<")          # plain text, not an HTML stub
    if kind == "html":
        return head.lstrip().startswith(b"<")
    return True


def fetch(name):
    """Return cached path for a manifest entry, downloading if needed.
    Returns None (after reporting) if the source fails — caller decides
    whether that blocks, per the data rule."""
    url, kind = MANIFEST[name]
    fp = os.path.join(CACHE, name)
    if _valid(fp, kind):
        return fp
    for wait in (0, 8, 25):                       # patient retries
        if wait:
            time.sleep(wait)
        try:
            r = requests.get(url, headers=UA, timeout=120)
        except requests.RequestException:
            continue
        if r.status_code == 200:
            open(fp, "wb").write(r.content)
            if _valid(fp, kind):
                time.sleep(1.5)                   # courtesy delay between files
                return fp
            os.remove(fp)                         # 200 but not the real file
    print(f"FETCH FAIL: {name}  ({url})")
    return None


def fetch_all():
    ledger = []
    for name in MANIFEST:
        fp = fetch(name)
        ledger.append((name, "OK" if fp else "FAIL",
                       f"{os.path.getsize(fp):,}B" if fp else "-"))
    return ledger


if __name__ == "__main__":
    ledger = fetch_all()
    w = max(len(n) for n, *_ in ledger)
    for name, status, size in ledger:
        print(f"{name:{w}s} {status:4s} {size}")
    fails = [n for n, s, _ in ledger if s == "FAIL"]
    print(f"\n{len(ledger) - len(fails)}/{len(ledger)} fetched; "
          + ("ALL OK" if not fails else f"FAILED: {fails}"))
