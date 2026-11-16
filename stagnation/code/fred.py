# fred.py — FRED series for M1, M3 and M5, pulled once into cache/fred/ and read from there afterwards.
# fetch(id) returns a pandas Series indexed by date. A series not yet cached is pulled from the public graph endpoint
# (fredgraph.csv), validated (the header names the series, values parse as numbers, at least one observation in the
# last two years) and written as pulled; cache/fred/MANIFEST.csv records when, how many rows, the first and last
# dates and the SHA-256. Nothing is substituted: a failed pull raises.
# Run from stagnation/:  ../venv/bin/python code/fred.py     (pulls every series in SERIES that is not cached)
import csv
import hashlib
import io
from datetime import date, datetime, timezone
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / "cache" / "fred"
MANIFEST = CACHE / "MANIFEST.csv"
URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={}"

SERIES = {
    # M1, the eras
    "OPHNFB": "Nonfarm business: labor productivity (output per hour), all workers, index 2017=100, Q, SA",
    "HOANBS": "Nonfarm business: hours worked, all workers, index 2017=100, Q, SA",
    "PRS85006173": "Nonfarm business: labor share, all workers, index 2017=100, Q, SA",
    "REAINTRATREARAT10Y": "10-year real interest rate (Cleveland Fed), percent, M",
    "DFII10": "10-year Treasury inflation-indexed security, constant maturity, percent, D",
    "HOOREVLMHMV": "Households; owner-occupied real estate including vacant land and mobile homes at market value, Q",
    "BOGZ1LM155012665Q": "Households and nonprofits; residential structures (households) at current cost, Q",
    "CNP16OV": "Civilian noninstitutional population 16 and over, thousands, M",
    "EMRATIO": "Employment-population ratio, percent, M, SA",
    # M3, pay against productivity
    "HCOMPBS": "Nonfarm business: hourly compensation, all workers, index 2017=100, Q, SA",
    "IPDNBS": "Nonfarm business: implicit price deflator, index 2017=100, Q, SA",
    "COMPRNFB": "Nonfarm business: real hourly compensation, all workers, index 2017=100, Q, SA",
    "CPIAUCSL": "CPI-U all items, 1982-84=100, M, SA",
    "CUUR0000SA0L2": "CPI-U all items less shelter, 1982-84=100, M, NSA",
    "CPILEGSL": "CPI-U all items less energy, 1982-84=100, M, SA",
    "CUUR0000SA0L5": "CPI-U all items less medical care, 1982-84=100, M, NSA",
    # M5, 2019 onward
    "AHETPI": "Average hourly earnings, production and nonsupervisory employees, total private, dollars, M, SA",
    "CES0500000003": "Average hourly earnings, all employees, total private, dollars, M, SA",
}


def _write_manifest_row(sid, n, first, last, sha):
    new = not MANIFEST.exists()
    with MANIFEST.open("a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["series", "pulled_utc", "rows", "first", "last", "sha256", "description"])
        w.writerow([sid, datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), n, first, last, sha,
                    SERIES.get(sid, "")])


def pull(sid):
    r = requests.get(URL.format(sid), timeout=60)
    r.raise_for_status()
    text = r.text
    head = text.splitlines()[0]
    if sid not in head or "observation_date" not in head:
        raise ValueError(f"{sid}: unexpected header {head[:80]!r}")
    d = pd.read_csv(io.StringIO(text), parse_dates=["observation_date"])
    v = pd.to_numeric(d[sid], errors="coerce")
    if v.notna().sum() < 10 or d.observation_date.max().date() < date(date.today().year - 2, 1, 1):
        raise ValueError(f"{sid}: too few or too old observations")
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / f"{sid}.csv"
    path.write_text(text)
    _write_manifest_row(sid, int(v.notna().sum()), d.observation_date.min().date(), d.observation_date.max().date(),
                        hashlib.sha256(text.encode()).hexdigest())
    return path


def fetch(sid):
    path = CACHE / f"{sid}.csv"
    if not path.exists():
        pull(sid)
    d = pd.read_csv(path, parse_dates=["observation_date"])
    return pd.to_numeric(d[sid], errors="coerce").set_axis(d.observation_date).dropna().rename(sid)


def annual(s, how="mean", complete=True):
    """Calendar-year averages (or the year's last value); with complete=True only years with every period present."""
    g = s.groupby(s.index.year)
    out = getattr(g, how)()
    if complete:
        per_year = {"QS-OCT": 4}.get(pd.infer_freq(s.index[:12]) or "", None)
        counts = g.count()
        need = counts.max() if per_year is None else per_year
        out = out[counts >= min(need, counts.mode().iloc[0])]
    return out


if __name__ == "__main__":
    for sid in SERIES:
        s = fetch(sid)
        print(f"{sid:20s} {len(s):6d} obs  {s.index.min().date()} .. {s.index.max().date()}  last {s.iloc[-1]:.4g}")
