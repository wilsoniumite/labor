# probe_urls.py — resolve real URLs before hardcoding them (house probe-first rule).
# HEAD (fall back to 1-byte ranged GET) each candidate; print a resolution table.
# Windows TLS note: truststore injects the OS cert store (ddorn.net serves an
# incomplete chain that browsers repair via AIA; this is the no-bypass fix).
import time

import truststore
truststore.inject_into_ssl()
import requests

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "academic research; contact wilsontomass@gmail.com"}


def alive(url):
    try:
        r = requests.head(url, headers=UA, timeout=25, allow_redirects=True)
        if r.status_code == 200:
            return True, r.headers.get("Content-Length", "?")
        if r.status_code in (403, 405):  # some servers reject HEAD
            r = requests.get(url, headers={**UA, "Range": "bytes=0-0"}, timeout=25)
            return r.status_code in (200, 206), r.headers.get("Content-Range", "?")
        return False, r.status_code
    except requests.RequestException as e:
        return False, type(e).__name__


CANDIDATES = []

# O*NET 30.3 text database
CANDIDATES.append(("onet_30_3", ["https://www.onetcenter.org/dl_files/database/db_30_3_text.zip"]))

# OEWS national files: May-reference 2003+, Nov/annual patterns before
for y in range(1997, 2026):
    yy = f"{y % 100:02d}"
    CANDIDATES.append((f"oews_{y}", [
        f"https://www.bls.gov/oes/special-requests/oesm{yy}nat.zip",
        f"https://www.bls.gov/oes/special-requests/oesn{yy}nat.zip",
        f"https://www.bls.gov/oes/special-requests/oes{yy}nat.zip",
    ]))

# BLS SOC revision crosswalks
CANDIDATES.append(("soc_2010_2018", [
    "https://www.bls.gov/soc/2018/soc_2010_to_2018_crosswalk.xlsx",
    "https://www.bls.gov/soc/soc_2010_to_2018_crosswalk.xlsx",
]))
CANDIDATES.append(("soc_2000_2010", [
    "https://www.bls.gov/soc/soc_2000_to_2010_crosswalk.xls",
    "https://www.bls.gov/soc/2010/soc_2000_to_2010_crosswalk.xls",
]))

if __name__ == "__main__":
    for name, urls in CANDIDATES:
        line = None
        for u in urls:
            ok, info = alive(u)
            if ok:
                line = f"{name:15s} OK   {u}  ({info})"
                break
            time.sleep(0.4)
        print(line or f"{name:15s} MISS {urls[0]} (+{len(urls)-1} alternates)")
        time.sleep(0.6)
