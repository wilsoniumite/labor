# common.py — shared helpers for the consumption thread: paths, polite downloads, per-source manifests.
# Plain functions only, so each piece can be pasted into a notebook cell.
#
# Download rules (fixed here so every script follows them):
#   * bls.gov hosts get a User-Agent with Stella's contact address: BLS asks scripted requests to carry
#     one, and she approved its use for BLS on 2026-11-02. No other host receives it.
#   * every other host gets a plain research User-Agent; never a browser imitation, never a bot-check
#     workaround. A 403 or a block is a stop-and-report, not something to route around.
#   * a vendored file is never re-downloaded unless force=True, so everything reruns offline.
#   * each source folder keeps its own MANIFEST.csv: file, url, what_it_is, date_pulled, sha256, bytes, used_for.
import csv
import datetime as dt
import hashlib
import time
from pathlib import Path
from urllib.parse import urlparse

import requests

THREAD = Path(__file__).resolve().parents[1]        # consumption/
REPO = THREAD.parent
RAW = THREAD / "data" / "raw"
TIDY = THREAD / "data" / "tidy"
UA_PLAIN = "Mozilla/5.0 (research; labor repo)"
UA_BLS = "Mozilla/5.0 (research; labor repo; wilsontomass@gmail.com)"
MANIFEST_COLS = ["file", "url", "what_it_is", "date_pulled", "sha256", "bytes", "used_for"]


def ua_for(url):
    host = urlparse(url).hostname or ""
    return UA_BLS if host == "bls.gov" or host.endswith(".bls.gov") else UA_PLAIN


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def http_get(url, tries=4, timeout=120, **kw):
    """GET with backoff on 429/5xx and network errors. Raises on 4xx other than 429 (stop-and-report)."""
    last = None
    for k in range(tries):
        try:
            r = requests.get(url, headers={"User-Agent": ua_for(url)}, timeout=timeout, **kw)
            if r.status_code == 429 or r.status_code >= 500:
                last = f"HTTP {r.status_code}"
                time.sleep(5 * (k + 1))
                continue
            r.raise_for_status()
            return r
        except requests.RequestException as e:
            if isinstance(e, requests.HTTPError):
                raise
            last = repr(e)
            time.sleep(5 * (k + 1))
    raise RuntimeError(f"GET failed after {tries} tries: {url} ({last})")


def manifest_row(source, rel_file, url, what, used_for, date_pulled=None):
    """Append (or replace) the manifest row for one vendored file in RAW/source/MANIFEST.csv."""
    folder = RAW / source
    path = folder / rel_file
    mpath = folder / "MANIFEST.csv"
    rows = []
    if mpath.exists():
        with open(mpath, newline="", encoding="utf-8") as fh:
            rows = [r for r in csv.DictReader(fh) if r["file"] != rel_file]
    rows.append({"file": rel_file, "url": url, "what_it_is": what,
                 "date_pulled": date_pulled or dt.date.today().isoformat(),
                 "sha256": sha256_of(path), "bytes": path.stat().st_size, "used_for": used_for})
    rows.sort(key=lambda r: r["file"])
    with open(mpath, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=MANIFEST_COLS)
        w.writeheader()
        w.writerows(rows)
    return path


def fetch(source, rel_file, url, what, used_for, force=False):
    """Vendor url into RAW/source/rel_file (skip if present) and record it in that source's manifest."""
    path = RAW / source / rel_file
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not force:
        return path
    r = http_get(url)
    path.write_bytes(r.content)
    manifest_row(source, rel_file, url, what, used_for)
    return path
