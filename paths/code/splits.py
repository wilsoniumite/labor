# splits.py — the splits tracker (her request, 2026-10-12): headline US statistics that only make sense split into a
# machine/owner side and a human/wage side, watched every quarter on rules fixed before the data that judge them.
# The protocol is SPLITS.md; this file is its code. Twelve judged measures, each with the paper's call and one named
# rival's call; a watch list reported and never judged; one statistic, E, for every measure:
#   E = (change in the gap over the latest 12 months or 4 quarters − the mean of such changes over 1990-2019 windows
#        that contain no recession month) / their standard deviation, signed toward the paper's call.
# E ≥ +1 moved the paper's way, E ≤ −1 the other way, otherwise no clear change. Measure 2 (payroll dispersion over all
# 2,047 two-way cuts of the payroll supersectors, 12-month growth) is judged on its level against the normal months'
# 95th percentile.
#
# Freeze: when the git tag `paths-splits-freeze` exists together with a committed results/splits_baseline.json (read
# from the tagged commit, not the working copy), only windows that start at the baseline's last observation are judged
# (non-overlapping, one after another), with the references, fitted coefficients and dispersion moments frozen in the
# baseline. Until then every reading is labelled "starting point (already seen; not judged)". `--write-baseline`
# writes the baseline (the main session runs it when she says freeze; then commit, then tag). Once tagged, a working
# copy of this file that differs from the tagged one is run beside the tagged one: the judged readings are the tagged
# code's, and any difference is labelled a deviation. The yearly look (`--refresh --look`) writes
# results/splits_look_<year>.json, which is committed and tagged `paths-splits-look-<year>`; that verdict stands, and
# later runs report the same window on revised data beside it.
#
# Public US data only (FRED: BLS, BEA, Federal Reserve Z.1 and DFA, Indeed, Nasdaq, NBER, Cleveland Fed) and, on the
# watch list, Statistics Sweden's household sector accounts (NR0103, cached; national accounts, not labour-force
# data). A guard refuses any series not in the manifest and any Eurostat, ILO or Statistics Sweden labour-force
# (AKU/LFS) identifier: the participation thread's European tests are blind.
#
# Run from paths/:  ../venv/Scripts/python.exe code/splits.py [--refresh] [--write-baseline] [--look]
# Out: results/splits.json, figures/fig_splits.png (with --write-baseline also results/splits_baseline.json; with
# --look also results/splits_look_<year>.json)

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import inspect
import json
import math
import os
import re
import subprocess
import sys
import types

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REPO = os.path.dirname(ROOT)
sys.path.insert(0, os.path.join(REPO, "pinning", "code"))
import lambda_compute2 as _lc  # noqa: E402

CACHE = os.path.join(ROOT, "cache", "splits")
SCB = os.path.join(ROOT, "cache", "scb")
VINTAGES = os.path.join(CACHE, "vintages.json")
RESULTS = os.path.join(ROOT, "results", "splits.json")
BASELINE = os.path.join(ROOT, "results", "splits_baseline.json")
LOOK_FILE = os.path.join(ROOT, "results", "splits_look_{year}.json")
PROTOCOL = os.path.join(ROOT, "SPLITS.md")
FIGURE = os.path.join(ROOT, "figures", "fig_splits.png")
TAG = "paths-splits-freeze"
LOOK_TAG = "paths-splits-look-{year}"
REF = ("1990-01-01", "2019-12-31")
SCHEMA_VERSION = 1
UNFROZEN_LABEL = "starting point (already seen; not judged)"
FROZEN_LABEL = "judged windows use only data published after the fixed date; the latest rolling readings are not judged"

# ---------------------------------------------------------------------------------------------------------------------
# The manifest: every series the tracker may fetch (an allowlist), with FRED's own title and the publisher.

MANIFEST = {
    # 1 care
    "CES6562000001": ("All Employees, Health Care and Social Assistance", "BLS"),
    "PAYEMS": ("All Employees, Total Nonfarm", "BLS"),
    "CES6500000008": ("Average Hourly Earnings of Production and Nonsupervisory Employees, Private Education and Health Services", "BLS"),
    "AHETPI": ("Average Hourly Earnings of Production and Nonsupervisory Employees, Total Private", "BLS"),
    # 2 payroll dispersion: the twelve supersector units (CES6562000001 above)
    "USMINE": ("All Employees, Mining and Logging", "BLS"),
    "USCONS": ("All Employees, Construction", "BLS"),
    "MANEMP": ("All Employees, Manufacturing", "BLS"),
    "USTPU": ("All Employees, Trade, Transportation, and Utilities", "BLS"),
    "USINFO": ("All Employees, Information", "BLS"),
    "USFIRE": ("All Employees, Financial Activities", "BLS"),
    "USPBS": ("All Employees, Professional and Business Services", "BLS"),
    "CES6561000001": ("All Employees, Private Educational Services", "BLS"),
    "USLAH": ("All Employees, Leisure and Hospitality", "BLS"),
    "USSERV": ("All Employees, Other Services", "BLS"),
    "USGOVT": ("All Employees, Government", "BLS"),
    # 3 graduates
    "LNS14027662": ("Unemployment Rate - Bachelor's Degree and Higher, 25 Yrs. & over", "BLS"),
    "LNS14027660": ("Unemployment Rate - High School Graduates, No College, 25 Yrs. & over", "BLS"),
    # 4 software postings
    "IHLIDXUSTPSOFTDEVE": ("Software Development Job Postings on Indeed in the United States", "Indeed"),
    "IHLIDXUS": ("Job Postings on Indeed in the United States", "Indeed"),
    # 5 hiring
    "JTSHIR": ("Hires: Total Nonfarm", "BLS"),
    "UNRATE": ("Unemployment Rate", "BLS"),
    # 6 output per hour
    "OUTNFB": ("Nonfarm Business Sector: Real Value-Added Output for All Workers", "BLS"),
    "HOANBS": ("Nonfarm Business Sector: Hours Worked for All Workers", "BLS"),
    # 7 labour share
    "A460RC1Q027SBEA": ("Net value added of nonfinancial corporate business: Compensation of employees", "BEA"),
    "A455RC1Q027SBEA": ("Gross value added of nonfinancial corporate business", "BEA"),
    # 8 asset income
    "PDI": ("Personal Income Receipts on Assets: Personal Dividend Income", "BEA"),
    "PII": ("Personal Income Receipts on Assets: Personal Interest Income", "BEA"),
    "W209RC1": ("Compensation of employees, received", "BEA"),
    "RENTIN": ("Rental Income of Persons with Capital Consumption Adjustment (CCAdj)", "BEA"),
    # 9 produced-input shortage premium (both not seasonally adjusted: 12-month changes remove the season)
    "PCU335311335311": ("Producer Price Index by Industry: Electric Power and Specialty Transformer Manufacturing", "BLS"),
    "WPUFD49207": ("Producer Price Index by Commodity: Final Demand: Finished Goods", "BLS"),
    # 10 site rent (Fed Z.1)
    "BOGZ1FL155035015Q": ("Households; Owner-Occupied Real Estate Including Vacant Land and Mobile Homes at Market Value, Level", "Federal Reserve Z.1"),
    "RCVSHNWBSHNO": ("Households; Residential Structures, Current Cost Basis, Level", "Federal Reserve Z.1"),
    "BOGZ1FL105010005Q": ("Nonfinancial Corporate Business; Land at Market Value, Level", "Federal Reserve Z.1"),
    "BOGZ1FL115010005Q": ("Nonfinancial Noncorporate Business; Land at Market Value, Level", "Federal Reserve Z.1"),
    # 11 build-out against housing (chain-type quantity indexes)
    "B679RA3Q086SBEA": ("Real private fixed investment, chained quantity index: Private fixed investment in information processing equipment and software", "BEA"),
    "A011RA3Q086SBEA": ("Real gross private domestic investment: Fixed investment: Residential (chain-type quantity index)", "BEA"),
    # 12 saving
    "PSAVERT": ("Personal Saving Rate", "BEA"),
    "BOGZ1LM153064475Q": ("Households and Nonprofit Organizations; Directly and Indirectly Held Corporate Equities; Asset, Market Value Levels", "Federal Reserve Z.1"),
    "DSPI": ("Disposable Personal Income", "BEA"),
    # recession dating
    "USREC": ("NBER based Recession Indicators for the United States from the Period following the Peak through the Trough", "NBER via FRED"),
    "SAHMREALTIME": ("Real-time Sahm Rule Recession Indicator", "FRED (Sahm)"),
    # conditions on the rivals' calls (SPLITS.md section 2): rate cuts (5, 11) and the real interest rate (10)
    "DFEDTAR": ("Federal Funds Target Rate (DISCONTINUED)", "Federal Reserve"),
    "DFEDTARU": ("Federal Funds Target Range - Upper Limit", "Federal Reserve"),
    "REAINTRATREARAT10Y": ("10-Year Real Interest Rate", "Federal Reserve Bank of Cleveland"),
    # watch list
    "NASDAQ100": ("NASDAQ-100", "Nasdaq"),
    "NASDAQNDXE": ("NASDAQ-100 Equal Weighted", "Nasdaq"),
    "NASDAQNQUSL": ("NASDAQ US Large Cap Index", "Nasdaq"),
    "NASDAQNQUSS": ("NASDAQ US Small Cap Index", "Nasdaq"),
    "B852RC1Q027SBEA": ("Imports of goods: Capital goods, except automotive: Computers, peripherals, and parts", "BEA"),
    "Y034RC1Q027SBEA": ("Gross Private Domestic Investment: Fixed Investment: Nonresidential: Equipment: Information Processing Equipment", "BEA"),
    "CUSR0000SEHF01": ("Consumer Price Index for All Urban Consumers: Electricity in U.S. City Average", "BLS"),
    "CPIAUCSL": ("Consumer Price Index for All Urban Consumers: All Items in U.S. City Average", "BLS"),
    "PCEC": ("Personal Consumption Expenditures", "BEA"),
    "GDP": ("Gross Domestic Product", "BEA"),
    # context for the website's spending section (reported, never judged): the Fed's distributional accounts
    "WFRBST01134": ("Share of Net Worth Held by the Top 1% (99th to 100th Wealth Percentiles)", "Federal Reserve DFA"),
    "WFRBSN09161": ("Share of Net Worth Held by the 90th to 99th Wealth Percentiles", "Federal Reserve DFA"),
}
# Swedish household sector accounts on the watch list: Statistics Sweden table NR0103 (national accounts), cached.
SCB_FILES = {"sector_S14.json": "NR0103", "gdp_current_sa.json": "NR0103"}

# What had been seen before the freeze: the last observation of every series in the tracker's vintage of 2026-10-13
# (the day after the panel). The baseline lists every series whose starting point is later than this, so releases that
# arrived between the panel and the freeze are named as seen (SPLITS.md section 9).
SEEN_BY_2026_10_13 = {
    "CES6562000001": "2026-09-01", "PAYEMS": "2026-09-01", "CES6500000008": "2026-09-01", "AHETPI": "2026-09-01",
    "USMINE": "2026-09-01", "USCONS": "2026-09-01", "MANEMP": "2026-09-01", "USTPU": "2026-09-01",
    "USINFO": "2026-09-01", "USFIRE": "2026-09-01", "USPBS": "2026-09-01", "CES6561000001": "2026-09-01",
    "USLAH": "2026-09-01", "USSERV": "2026-09-01", "USGOVT": "2026-09-01", "LNS14027662": "2026-09-01",
    "LNS14027660": "2026-09-01", "IHLIDXUSTPSOFTDEVE": "2026-10-02", "IHLIDXUS": "2026-10-02", "JTSHIR": "2026-08-01",
    "UNRATE": "2026-09-01", "OUTNFB": "2026-04-01", "HOANBS": "2026-04-01", "A460RC1Q027SBEA": "2026-04-01",
    "A455RC1Q027SBEA": "2026-04-01", "PDI": "2026-08-01", "PII": "2026-08-01", "W209RC1": "2026-08-01",
    "RENTIN": "2026-04-01", "PCU335311335311": "2026-08-01", "WPUFD49207": "2026-08-01",
    "BOGZ1FL155035015Q": "2026-04-01", "RCVSHNWBSHNO": "2026-04-01", "BOGZ1FL105010005Q": "2026-04-01",
    "BOGZ1FL115010005Q": "2026-04-01", "B679RA3Q086SBEA": "2026-04-01", "A011RA3Q086SBEA": "2026-04-01",
    "PSAVERT": "2026-08-01", "BOGZ1LM153064475Q": "2026-04-01", "DSPI": "2026-08-01", "USREC": "2026-09-01",
    "SAHMREALTIME": "2026-09-01", "DFEDTAR": "2008-12-15", "DFEDTARU": "2026-10-12",
    "REAINTRATREARAT10Y": "2026-09-01", "NASDAQ100": "2026-10-09", "NASDAQNDXE": "2026-10-09",
    "NASDAQNQUSL": "2026-10-09", "NASDAQNQUSS": "2026-10-09", "B852RC1Q027SBEA": "2026-04-01",
    "Y034RC1Q027SBEA": "2026-04-01", "CUSR0000SEHF01": "2026-08-01", "CPIAUCSL": "2026-08-01", "PCEC": "2026-04-01",
    "GDP": "2026-04-01", "WFRBST01134": "2026-04-01", "WFRBSN09161": "2026-04-01",
}

# Blinding guard: European labour-force identifiers, refused even if someone adds them to the manifest.
EU = ("SE|SWE|DE|DEU|FR|FRA|IT|ITA|ES|ESP|NL|NLD|EU|EZ|EA|EA19|EA20|EU27|EU28|GB|GBR|UK|DK|DNK|FI|FIN|NO|NOR|AT|AUT|BE|BEL|"
      "IE|IRL|PT|PRT|GR|GRC|EL|PL|POL|CZ|CZE|HU|HUN|SK|SVK|SI|SVN|EE|EST|LV|LVA|LT|LTU|LU|LUX|BG|BGR|RO|ROU|HR|HRV|CY|CYP|"
      "MT|MLT|IS|ISL|CH|CHE|OE|OECD")
DENY = [
    r"(?i)eurostat", r"(?i)ilostat", r"(?i)(^|[^a-z])ilo([^a-z]|$)", r"(?i)aku", r"(?i)(^|[^a-z])lfs", r"(?i)lfsa_|lfsq_|lfsi_",
    r"(?i)une_rt|^une_", r"(?i)^am0[0-9]", r"(?i)arbetskraft", r"(?i)emp_temp|emp_2emp",
    rf"^(LR|LF|LM|SLUEM|SLEMP|SLTLF|ELAB)[A-Z0-9]*({EU})[A-Z0-9]*$",
]


def guard(name: str) -> str:
    """Refuse anything not in the manifest, and any European labour-force identifier or file (blinding)."""
    base = os.path.basename(str(name))
    if re.search(r"(?i)(^|[\/])(ilo|eurostat)([\/]|$)", str(name)):
        raise PermissionError(f"refused (blinding: European labour-force data): {name}")
    for pat in DENY:
        if re.search(pat, base):
            raise PermissionError(f"refused (blinding: European labour-force data): {name}")
    if base.endswith(".json") or base.endswith(".csv"):
        if base not in SCB_FILES:
            raise PermissionError(f"refused (not in the manifest): {name}")
    elif base not in MANIFEST:
        raise PermissionError(f"refused (not in the manifest): {name}")
    return base


# ---------------------------------------------------------------------------------------------------------------------
# Fetching, with a per-series vintage log (download date, hash, revisions against the previous download).

REFRESH_FAILED: list = []          # series whose refresh failed in this run (the previous vintage was kept)


def _now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _today() -> dt.date:
    return dt.datetime.now(dt.timezone.utc).date()


def _sha(txt: str) -> str:
    return hashlib.sha256(txt.encode("utf-8")).hexdigest()


def _load_vintages() -> dict:
    try:
        return json.load(open(VINTAGES, encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _parse(txt: str, sid: str) -> pd.Series:
    import io
    df = pd.read_csv(io.StringIO(txt))
    idx = pd.to_datetime(df["observation_date"], errors="coerce")
    return pd.Series(pd.to_numeric(df[sid], errors="coerce").values, index=idx).dropna()


def fetch(sid: str, refresh: bool = False, vint: dict | None = None) -> pd.Series:
    """A manifest series from the tracker's cache, downloaded from FRED when missing or when `refresh` is set. A failed
    refresh keeps the previous file and its vintage record (marked `refresh_failed_utc`, and listed in REFRESH_FAILED,
    with a warning): a kept file is never logged as a fresh download."""
    guard(sid)
    os.makedirs(CACHE, exist_ok=True)
    fp = os.path.join(CACHE, sid + ".csv")
    had_file = os.path.exists(fp)
    old_txt = open(fp).read() if had_file else None
    if refresh and had_file:
        os.remove(fp)
    downloading = refresh or not had_file
    prev = _lc.CACHE
    _lc.CACHE = CACHE
    try:
        s = _lc.pull_fred(sid)
    finally:
        _lc.CACHE = prev
    failed = False
    if s is None:
        if old_txt is None:
            raise SystemExit(f"FRED {sid}: not available")
        open(fp, "w").write(old_txt)                 # keep the previous vintage
        s = _parse(old_txt, sid)
        failed = True
    if vint is not None:
        rec = vint.get(sid)
        if failed:
            if rec is None:
                rec = {"downloaded_utc": None, "sha256": _sha(old_txt), "first": str(s.index[0].date()),
                       "last": str(s.index[-1].date()), "n": int(len(s)), "title": MANIFEST[sid][0], "source": MANIFEST[sid][1]}
                vint[sid] = rec
            rec["refresh_failed_utc"] = _now()
            REFRESH_FAILED.append(sid)
            print(f"warning: FRED {sid}: refresh failed; the previous vintage is kept", file=sys.stderr)
            return s
        txt = open(fp).read()
        if downloading or rec is None or rec.get("sha256") != _sha(txt):
            new = {"downloaded_utc": _now() if downloading else
                   dt.datetime.fromtimestamp(os.path.getmtime(fp), dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                   "sha256": _sha(txt), "first": str(s.index[0].date()), "last": str(s.index[-1].date()), "n": int(len(s)),
                   "title": MANIFEST[sid][0], "source": MANIFEST[sid][1]}
            if old_txt is not None and rec is not None and rec.get("sha256") != new["sha256"]:
                o = _parse(old_txt, sid)
                common = o.index.intersection(s.index)
                d = (s[common] - o[common]).abs()
                new["revision_vs_previous"] = {"previous_downloaded_utc": rec.get("downloaded_utc"), "observations_changed": int((d > 0).sum()),
                                               "max_abs_change": float(d.max()) if len(d) else 0.0,
                                               "new_observations": int(len(s.index.difference(o.index)))}
            vint[sid] = new
    elif failed:
        REFRESH_FAILED.append(sid)
        print(f"warning: FRED {sid}: refresh failed; the previous vintage is kept", file=sys.stderr)
    return s


def read_scb(fn: str, key: tuple) -> pd.Series:
    """A Statistics Sweden NR0103 series from the cache (sector accounts only; labour-force files refused by name)."""
    guard(fn)
    d = json.load(open(os.path.join(SCB, fn), encoding="utf-8"))
    if d["metadata"][0]["infofile"] != SCB_FILES[fn]:
        raise PermissionError(f"refused: {fn} is not table {SCB_FILES[fn]}")
    rows = [(r["key"][-1], float(r["values"][0])) for r in d["data"] if tuple(r["key"][:-1]) == key and r["values"][0] not in ("..", "")]
    return pd.Series({pd.Period(t.replace("K", "Q"), "Q").start_time: v for t, v in rows}).sort_index()


# ---------------------------------------------------------------------------------------------------------------------
# Frequencies, windows, recessions.

def month_mean(s: pd.Series) -> pd.Series:
    """Monthly means of a daily series, complete months only (last observation within four days of the month's end)."""
    p = s.index.to_period("M")
    g = s.groupby(p)
    m, last = g.mean(), g.apply(lambda x: x.index.max())
    keep = [q for q in m.index if last[q] >= q.end_time.normalize() - pd.Timedelta(days=4)]
    out = m[keep]
    out.index = out.index.to_timestamp()
    return out


def q_mean(s: pd.Series) -> pd.Series:
    """Quarterly means of a monthly series: complete quarters, and interior quarters with one month never published
    (October 2025, the shutdown) on their other two; never a partial latest quarter."""
    p = s.index.to_period("Q")
    g = s.groupby(p)
    m, c = g.mean(), g.count()
    m = m[(c == 3) | ((c == 2) & (m.index < m.index[-1]))]
    m.index = m.index.to_timestamp()
    return m


def regular(s: pd.Series, freq: str) -> pd.Series:
    s = s.dropna()
    return s.reindex(pd.date_range(s.index[0], s.index[-1], freq=freq))


FREQ_MONTHS = {"MS": 1, "QS": 3}


def window_months(t, freq: str, k: int) -> pd.DatetimeIndex:
    """Calendar months over which the change from t−k to t accrues."""
    f = FREQ_MONTHS[freq]
    t = pd.Timestamp(t)
    return pd.date_range(t - pd.DateOffset(months=(k - 1) * f), t + pd.DateOffset(months=f - 1), freq="MS")


def touches(t, freq: str, k: int, months: set) -> bool:
    return any(m in months for m in window_months(t, freq, k))


def recession_months(usrec: pd.Series) -> set:
    return {pd.Timestamp(t) for t, v in usrec.items() if v >= 0.5}


def zone(e) -> str | None:
    if e is None or not np.isfinite(e):
        return None
    return "+" if e >= 1 else ("-" if e <= -1 else "0")


READING = {"+": "moved the paper's way", "-": "moved against the paper's call", "0": "no clear change", None: "not available"}


def reference(ch: pd.Series, freq: str, k: int, rec: set, min_n: int, upto=None) -> dict:
    """Mean and sd of the window changes over 1990-2019 windows with no recession month; the longest available
    non-recession history when 1990-2019 holds fewer than `min_n` windows (flagged as its own history), ending at
    `upto` (the window before the latest, so the latest reading is not in its own benchmark)."""
    ch = ch.dropna()
    cand = ch[(ch.index >= REF[0]) & (ch.index <= REF[1])]
    ok = [t for t in cand.index if not touches(t, freq, k, rec)]
    own = len(ok) < min_n
    if own:
        cand = ch if upto is None else ch[ch.index <= pd.Timestamp(upto)]
        ok = [t for t in cand.index if not touches(t, freq, k, rec)]
    v = ch[ok]
    return {"mean": float(v.mean()), "sd": float(v.std(ddof=1)), "n": int(len(v)), "from": str(v.index[0].date())[:7],
            "to": str(v.index[-1].date())[:7], "own_history": bool(own), "_index": v.index}


def e_series(ch: pd.Series, ref: dict, direction: int = 1) -> pd.Series:
    return direction * (ch - ref["mean"]) / ref["sd"]


def judged_windows(gap: pd.Series, base_date, k: int, ref: dict, direction: int = 1) -> list:
    """Non-overlapping windows on the calendar from the baseline's last observation: [b, b+k], [b+k, b+2k], ... (k
    observations of the gap's frequency). Only windows whose end has been published count; a window whose end is
    missing while later observations exist (a month never collected, as in the 2025 shutdown) is listed without an E.
    Nothing before the baseline observation enters except its value as the first window's starting point."""
    g = gap.dropna()
    if not len(g):
        return []
    b = pd.Timestamp(base_date)
    if b not in g.index:
        return []
    step = 3 if (len(g.index) > 1 and pd.Series(g.index).diff().dt.days.median() > 40) else 1
    out = []
    j = 1
    while True:
        s_ = b + pd.DateOffset(months=step * k * (j - 1))
        e_ = b + pd.DateOffset(months=step * k * j)
        if e_ > g.index[-1]:
            break
        if s_ in g.index and e_ in g.index:
            c = float(g[e_] - g[s_])
            E = direction * (c - ref["mean"]) / ref["sd"]
            out.append({"start": str(s_.date()), "end": str(e_.date()), "change": c, "E_signed": float(E), "zone": zone(E)})
        else:
            out.append({"start": str(s_.date()), "end": str(e_.date()), "change": None, "E_signed": None, "zone": None,
                        "note": "an end point was never published"})
        j += 1
    return out


def fifteenth_november_after(d: dt.date) -> dt.date:
    """The first 15 November at least twelve months after d (SPLITS.md section 7)."""
    y = d.year + 1
    try:
        a = d.replace(year=y)
    except ValueError:            # 29 February
        a = dt.date(y, 3, 1)
    nov = dt.date(y, 11, 15)
    return nov if a <= nov else dt.date(y + 1, 11, 15)


def look_date(fixed: dt.date, j: int) -> dt.date:
    """The yearly look for judged window j (1, 2, ...): the first 15 November at least a year after the fixed date,
    then every 15 November after it."""
    f = fifteenth_november_after(fixed)
    return dt.date(f.year + j - 1, 11, 15)


# ---------------------------------------------------------------------------------------------------------------------
# The twelve judged measures. Each spec is plain data (hashed into the baseline with the code that computes them).

L = lambda s: 100 * np.log(s)  # noqa: E731

SPECS = [
    {"id": 1, "key": "care", "name": "Care: jobs and relative pay",
     "series": ["CES6562000001", "PAYEMS", "CES6500000008", "AHETPI"], "freq": "MS", "k": 12, "direction": -1,
     "gap": "100*log(CES6500000008/AHETPI): care's relative pay (production workers, education and health), log points",
     "legs": {"jobs": "100*log(CES6562000001/(PAYEMS-CES6562000001)): care's jobs against all other jobs, log points"},
     "paper": "crowding: care's share of jobs rises faster than usual while its relative pay falls (E on pay, signed down, >= +1)",
     "rival_name": "ageing demand", "rival": "care's jobs and its relative pay both rise (pay E <= -1 signed)",
     "fits": "only while care's share of jobs rises faster than usual (jobs E > 0): pay + paper, pay - rival; otherwise neither"},
    {"id": 2, "key": "payroll_dispersion", "name": "Payroll dispersion across all 2,047 cuts",
     "series": ["USMINE", "USCONS", "MANEMP", "USTPU", "USINFO", "USFIRE", "USPBS", "CES6561000001", "CES6562000001", "USLAH",
                "USSERV", "USGOVT"], "freq": "MS", "k": 12, "direction": 1,
     "gap": "share (%) of all 2,047 two-way cuts of the 12 payroll supersectors whose 12-month relative growth is beyond "
            "2 sd of its own 1990-2019 non-recession distribution",
     "legs": {},
     "paper": "stays above the normal months' 95th percentile without a recession",
     "rival_name": "cycle and the over-hiring unwind", "rival": "falls back below the 95th percentile",
     "fits": "level >= p95: paper (+); fell below p95 within the window: rival (-, a signed call); below at both ends: "
             "rival holds (0, nothing unusual)"},
    {"id": 3, "key": "graduates", "name": "Graduates against high-school leavers, unemployment",
     "series": ["LNS14027662", "LNS14027660"], "freq": "MS", "k": 12, "direction": 1,
     "gap": "100*log(3-month avg LNS14027662 / 3-month avg LNS14027660), log points", "legs": {},
     "paper": "the ratio rises without a recession", "rival_name": "an ordinary slowdown",
     "rival": "the ratio falls (the less educated are more cyclical)",
     "fits": "+ paper; - rival; 0 neither. Judged in recession windows too (the rival's sharpest call)"},
    {"id": 4, "key": "software_postings", "name": "Software postings against all postings",
     "series": ["IHLIDXUSTPSOFTDEVE", "IHLIDXUS"], "freq": "MS", "k": 12, "direction": -1,
     "gap": "100*log(monthly mean IHLIDXUSTPSOFTDEVE / monthly mean IHLIDXUS), complete months, log points", "legs": {},
     "paper": "keeps falling", "rival_name": "the 2022 over-hiring and the R&D-expensing rule (restored July 2025)",
     "rival": "recovers", "fits": "+ paper; - rival; 0 neither. History from 2020: benchmark is its own history to the "
                                  "window before the latest (flagged); reported beside the count, not in it"},
    {"id": 5, "key": "hiring", "name": "Hiring against what unemployment implies",
     "series": ["JTSHIR", "UNRATE"], "freq": "MS", "k": 12, "direction": -1,
     "gap": "JTSHIR minus its 2001-2019 least-squares fit on UNRATE (coefficients frozen at the freeze), percentage points",
     "legs": {},
     "paper": "stays below the fit (or falls further)", "rival_name": "interest rates and uncertainty",
     "rival": "the gap closes within four quarters of rate cuts",
     "fits": "+ paper; 0 with the gap below zero paper (stays below); - rival only when the window holds a rate cut (the "
             "fed funds target at its end at least 50 bp below its level 12 months earlier), otherwise neither; 0 at or "
             "above zero neither"},
    {"id": 6, "key": "output_per_hour", "name": "Output per hour",
     "series": ["OUTNFB", "HOANBS"], "freq": "QS", "k": 4, "direction": 1,
     "gap": "100*log(OUTNFB/HOANBS), log points (4-quarter change = output-per-hour growth)", "legs": {},
     "paper": "grows faster than its usual range (E >= +1)", "rival_name": "lower immigration",
     "rival": "hours slow while output per hour grows at its usual pace", "fits": "+ paper; 0 rival (nothing unusual); - neither"},
    {"id": 7, "key": "labour_share", "name": "Labour's share of corporate value added, adjusted for the unemployment rate",
     "series": ["A460RC1Q027SBEA", "A455RC1Q027SBEA", "UNRATE"], "freq": "QS", "k": 4, "direction": -1,
     "gap": "100*A460RC1Q027SBEA/A455RC1Q027SBEA minus its 1948-2019 least-squares fit on the level of UNRATE "
            "(quarterly mean; coefficients frozen at the freeze), points. Over a year the adjustment is small (the "
            "unemployment rate moves little); the raw share's E is reported beside it",
     "legs": {}, "paper": "falls", "rival_name": "the cycle", "rival": "moves only with unemployment (rises when it is low)",
     "fits": "+ paper; 0 rival (nothing unusual); - neither. Judged in recession windows too"},
    {"id": 8, "key": "asset_income", "name": "Dividends and interest against pay",
     "series": ["PDI", "PII", "W209RC1", "RENTIN"], "freq": "MS", "k": 12, "direction": 1,
     "gap": "100*log(PDI/W209RC1), log points",
     "legs": {"interest": "100*log(PII/W209RC1), log points",
              "rent": "100*log(RENTIN/quarterly mean W209RC1), log points (quarterly; reported)"},
     "paper": "dividends (and rent) rise relative to pay", "rival_name": "higher interest rates",
     "rival": "only interest rises relative to pay", "fits": "dividends + paper; else interest leg E >= +1 rival; else neither"},
    {"id": 9, "key": "transformer_premium", "name": "Transformer prices against finished goods",
     "series": ["PCU335311335311", "WPUFD49207"], "freq": "MS", "k": 12, "direction": -1,
     "gap": "100*log(PCU335311335311/WPUFD49207), log points (both not seasonally adjusted)", "legs": {},
     "paper": "a temporary premium on produced capital: falls back by 2028 as capacity is built",
     "rival_name": "lasting scarcity (rents migrating to power equipment)", "rival": "keeps rising",
     "fits": "+ paper; - rival; 0 neither; at the second judged window (ending 24 months after the baseline, August 2028 "
             "for a baseline in August 2026) the relative price below its baseline level fits the paper, above it the rival"},
    {"id": 10, "key": "site_rent", "name": "Land values against pay",
     "series": ["BOGZ1FL155035015Q", "RCVSHNWBSHNO", "BOGZ1FL105010005Q", "BOGZ1FL115010005Q", "W209RC1"], "freq": "QS", "k": 4,
     "direction": 1,
     "gap": "100*log(land / annual pay): land = (BOGZ1FL155035015Q - RCVSHNWBSHNO) + BOGZ1FL105010005Q + BOGZ1FL115010005Q "
            "(households' owner-occupied real estate less its structures at current cost, plus business land at market "
            "value), pay = quarterly mean W209RC1, log points", "legs": {},
     "paper": "rises", "rival_name": "high real interest rates", "rival": "falls as the real interest rate rises",
     "fits": "+ paper; - rival only when the 10-year real interest rate (REAINTRATREARAT10Y, quarterly mean) rose over "
             "the window, otherwise neither; 0 neither"},
    {"id": 11, "key": "build_out", "name": "Information technology investment against housing",
     "series": ["B679RA3Q086SBEA", "A011RA3Q086SBEA"], "freq": "QS", "k": 4, "direction": 1,
     "gap": "100*log(B679RA3Q086SBEA/A011RA3Q086SBEA), real quantity indexes, log points", "legs": {},
     "paper": "widens (the neutral rate's rising phase)", "rival_name": "interest rates", "rival": "narrows after rate cuts",
     "fits": "+ paper; - rival only when the window holds a rate cut (as for 5), otherwise neither; 0 neither"},
    {"id": 12, "key": "saving", "name": "Saving net of the stock-market wealth effect",
     "series": ["PSAVERT", "BOGZ1LM153064475Q", "DSPI"], "freq": "QS", "k": 4, "direction": 1,
     "gap": "PSAVERT (quarterly mean) minus its 1960-2019 least-squares fit on household equities / disposable income "
            "(BOGZ1LM153064475Q / (1000 * quarterly mean DSPI); coefficients frozen at the freeze), points", "legs": {},
     "paper": "the residual rises (owners save; the paper's later phase)", "rival_name": "the wealth effect",
     "rival": "no residual: saving moves with equity wealth",
     "fits": "+ paper; 0 rival (nothing unusual) only once measure 11 has turned (its same window reads -), otherwise "
             "neither (the paper's call is for after the build-out); - neither"},
]
SPEC = {s["key"]: s for s in SPECS}
ID = {s["id"]: s["key"] for s in SPECS}
# The combined reading counts the eleven measures with 1990-2019 history; measure 4 (history from 2020) is reported
# beside the count, never in it, so the count and its benchmark hold the same measures.
BESIDE = ("software_postings",)
COUNT_KEYS = tuple(s["key"] for s in SPECS if s["key"] not in BESIDE)
# A recession voids every measure's window for the paper against the cycle, except these two, where the rival is the
# cycle itself: they are judged in a downturn; the combined verdict is still void.
KEEP_IN_RECESSION = ("graduates", "labour_share")
# Rivals whose call is "nothing unusual": their fit at zone 0 is not a signed call.
NULL_RIVAL = ("output_per_hour", "labour_share", "saving")
# Measures that move together through one channel (SPLITS.md section 6): the verdict is recomputed without each, and a
# verdict that flips is labelled as resting on that channel.
CHANNELS = {"rates": [5, 8, 10, 11, 12], "tech unwind": [2, 3, 4, 5, 11], "price shock": [1, 8, 9]}
DEADLINE_WINDOW = {"transformer_premium": 2}    # "falls back by 2028": judged on its level at the second window
RATE_CUT_BP = 50

UNITS = {"mining": "USMINE", "construction": "USCONS", "manufacturing": "MANEMP", "trade_transport_utilities": "USTPU",
         "information": "USINFO", "financial": "USFIRE", "professional_business": "USPBS", "education": "CES6561000001",
         "health_social": "CES6562000001", "leisure_hospitality": "USLAH", "other_services": "USSERV", "government": "USGOVT"}
DISPERSION = {"window_months": 12, "z": 2.0,
              "reference": "1991-2019 months whose 12-month window holds no NBER recession month (from 1992-03)",
              "threshold": "95th percentile of the share in those months",
              "panel_window_months": 24}
WATCH_SPECS = [
    {"key": "big_vs_rest", "name": "Big stocks against the rest (Nasdaq-100 cap-weighted against equal-weighted)",
     "series": ["NASDAQ100", "NASDAQNDXE"],
     "note": "a proxy for 'the big ten up, the rest down': the cap-weighted Nasdaq-100 over its equal-weighted version "
             "(price indexes, monthly means). The S&P 500 equal-weight index is not on FRED. A price split measures "
             "expectations and discount rates; the paper makes no call on whether the largest firms keep their gains."},
    {"key": "large_vs_small", "name": "US large caps against small caps (Nasdaq)", "series": ["NASDAQNQUSL", "NASDAQNQUSS"],
     "note": "second proxy; small firms carry more floating-rate debt, so rates move this split directly."},
    {"key": "computer_imports", "name": "Computer imports against investment in information processing equipment",
     "series": ["B852RC1Q027SBEA", "Y034RC1Q027SBEA"], "note": "per cent, nominal; information processing equipment "
                                                                   "excludes software."},
    {"key": "electricity", "name": "Electricity prices against all consumer prices", "series": ["CUSR0000SEHF01", "CPIAUCSL"],
     "note": "electricity is a produced output; grid connections are scarce only until more are built."},
    {"key": "consumption_share", "name": "Consumer spending, share of GDP", "series": ["PCEC", "GDP"],
     "note": "spending is outrunning income in 2026; the paper puts owners' saving after the build-out."},
    {"key": "se_property_income", "name": "Sweden: household property income net of property income paid, % of GDP",
     "series": ["sector_S14.json", "gdp_current_sa.json"],
     "note": "Statistics Sweden NR0103 household sector accounts (D4 received less D4 paid, 4-quarter sums) over GDP; "
             "national accounts, not labour-force data."},
]


# ---------------------------------------------------------------------------------------------------------------------
# Building the gaps.

def build(data: dict, fits: dict | None = None) -> dict:
    """The gap (and legs) of every judged measure as regular series at the measure's frequency. `fits` (the baseline's
    frozen coefficients) replaces the re-estimated ones for measures 5, 7 and 12; the current vintage's estimates are
    returned beside them either way."""
    f = data
    fits = fits or {}
    out = {}
    pay, care = f["PAYEMS"], f["CES6562000001"]
    out["care"] = {"gap": regular(L(f["CES6500000008"] / f["AHETPI"]), "MS"),
                   "legs": {"jobs": regular(L(care / (pay - care)), "MS")}}
    a3 = regular(f["LNS14027662"], "MS").rolling(3, min_periods=2).mean()
    b3 = regular(f["LNS14027660"], "MS").rolling(3, min_periods=2).mean()
    gr = L(a3 / b3).dropna()   # October 2025 (never collected): the 3-month average of August and September
    out["graduates"] = {"gap": regular(gr, "MS"), "legs": {}}
    sw = L(month_mean(f["IHLIDXUSTPSOFTDEVE"]) / month_mean(f["IHLIDXUS"])).dropna()
    out["software_postings"] = {"gap": regular(sw, "MS"), "legs": {}}
    d = pd.concat([f["JTSHIR"], f["UNRATE"]], axis=1, sort=True).dropna()
    d.columns = ["h", "u"]
    fit = d["2001-01-01":"2019-12-31"]
    b1, b0 = np.polyfit(fit.u, fit.h, 1)
    cur = {"intercept": float(b0), "slope_on_unrate": float(b1), "period": "2001-01 to 2019-12"}
    use = fits.get("hiring") or cur
    out["hiring"] = {"gap": regular(d.h - (use["intercept"] + use["slope_on_unrate"] * d.u), "MS"), "legs": {}, "fit": use,
                     "fit_current_vintage": cur}
    out["output_per_hour"] = {"gap": regular(L(f["OUTNFB"] / f["HOANBS"]), "QS"), "legs": {}}
    ls = (100 * f["A460RC1Q027SBEA"] / f["A455RC1Q027SBEA"]).dropna()
    uq = q_mean(f["UNRATE"])
    d = pd.concat([ls, uq], axis=1, sort=True).dropna()
    d.columns = ["s", "u"]
    fit = d[:"2019-12-31"]
    c1, c0 = np.polyfit(fit.u, fit.s, 1)
    cur = {"intercept": float(c0), "slope_on_unrate": float(c1), "period": f"{str(fit.index[0].date())[:7]} to 2019-12"}
    use = fits.get("labour_share") or cur
    out["labour_share"] = {"gap": regular(d.s - (use["intercept"] + use["slope_on_unrate"] * d.u), "QS"), "legs": {},
                           "level": regular(ls, "QS"), "fit": use, "fit_current_vintage": cur}
    comp_q = q_mean(f["W209RC1"])
    out["asset_income"] = {"gap": regular(L(f["PDI"] / f["W209RC1"]), "MS"),
                           "legs": {"interest": regular(L(f["PII"] / f["W209RC1"]), "MS"),
                                    "rent": regular(L(f["RENTIN"] / comp_q).dropna(), "QS")}}
    out["transformer_premium"] = {"gap": regular(L(f["PCU335311335311"] / f["WPUFD49207"]), "MS"), "legs": {}}
    land = (f["BOGZ1FL155035015Q"] - f["RCVSHNWBSHNO"]) + f["BOGZ1FL105010005Q"] + f["BOGZ1FL115010005Q"]
    out["site_rent"] = {"gap": regular(L(land / (1000 * comp_q)).dropna(), "QS"), "legs": {},
                        "land_tn": regular(land / 1e6, "QS")}
    out["build_out"] = {"gap": regular(L(f["B679RA3Q086SBEA"] / f["A011RA3Q086SBEA"]), "QS"), "legs": {}}
    sv = q_mean(f["PSAVERT"])
    eq = (f["BOGZ1LM153064475Q"] / (1000 * q_mean(f["DSPI"]))).dropna()
    d = pd.concat([sv, eq], axis=1, sort=True).dropna()
    d.columns = ["s", "x"]
    fit = d["1960-01-01":"2019-12-31"]
    e1, e0 = np.polyfit(fit.x, fit.s, 1)
    cur = {"intercept": float(e0), "slope_on_equity_to_income": float(e1), "period": "1960-01 to 2019-12",
           "equity_to_income_range_in_fit": [float(fit.x.min()), float(fit.x.max())]}
    use = fits.get("saving") or cur
    out["saving"] = {"gap": regular(d.s - (use["intercept"] + use["slope_on_equity_to_income"] * d.x), "QS"), "legs": {},
                     "level": regular(sv, "QS"), "equity_to_income": regular(d.x, "QS"), "fit": use, "fit_current_vintage": cur}
    return out


def dispersion(data: dict, rec: set, panel_rec: list | None = None, H: int | None = None, moments: dict | None = None) -> dict:
    """All 2,047 two-way cuts of the 12 payroll supersectors (government always on side B), their H-month relative
    growth (pp a year; H = 12 for the tracker, 24 for the panel's benchmark), z against each cut's own 1990-2019
    non-recession windows, and the share beyond 2 sd. A window is a recession window when any of its H months is an
    NBER recession month (USREC). `moments` (the baseline's frozen per-cut means and sds) replaces the re-estimated
    ones. `panel_rec` replays the panel's 2026-10-12 rule instead (window end t within [peak, trough + 24 months], peaks
    typed by hand), for the check that reproduces its numbers."""
    H = H or DISPERSION["window_months"]
    U = pd.concat({k: data[v] for k, v in UNITS.items()}, axis=1, sort=True).dropna()
    U = U[U.index >= "1990-01-01"]
    pay = data["PAYEMS"].reindex(U.index)
    names = list(UNITS)
    n, X = len(names), U.values
    R = []
    for mask in range(1, 2 ** (n - 1)):
        a = np.array([(mask >> i) & 1 for i in range(n)], bool)
        g = 100 * (np.log(X[:, a].sum(1)) - np.log(X[:, ~a].sum(1)))
        R.append((g[H:] - g[:-H]) / (H / 12))
    R = np.array(R)
    idx = U.index[H:]
    pre = np.asarray(idx <= REF[1])
    if panel_rec is None:
        recw = np.array([touches(t, "MS", H, rec) for t in idx])
    else:
        recw = np.array([any(pd.Timestamp(a) <= t <= pd.Timestamp(b) + pd.DateOffset(months=24) for a, b in panel_rec) for t in idx])
    ref = pre & ~recw
    mu_c, sd_c = R[:, ref].mean(1, keepdims=True), R[:, ref].std(1, keepdims=True)
    if moments is not None:
        mu, sd = np.array(moments["mean"]).reshape(-1, 1), np.array(moments["sd"]).reshape(-1, 1)
    else:
        mu, sd = mu_c, sd_c
    Z = (R - mu) / sd
    share = pd.Series((np.abs(Z) > DISPERSION["z"]).mean(0) * 100, idx)
    ci = sum(1 << i for i, k in enumerate(names) if k == "health_social") - 1
    p95 = float(share[ref].quantile(0.95))
    top = np.argsort(-np.abs(Z[:, -1]))[:5]
    refidx = share.index[ref]
    return {"share": share, "ref_mask": pd.Series(ref, idx), "rec_mask": pd.Series(recw, idx), "window_months": H,
            "n_cuts": int(R.shape[0]), "sum_vs_payems_max_abs_pct": round(float((U.sum(axis=1) / pay - 1).abs().max() * 100), 2),
            "normal_median": float(share[ref].median()), "normal_p95": p95, "normal_p90": float(share[ref].quantile(0.90)),
            "normal_max": [str(share[ref].idxmax().date())[:7], float(share[ref].max())],
            "normal_from": str(refidx[0].date())[:7], "normal_to": str(refidx[-1].date())[:7],
            "recession_median_pre2020": float(share[pre & recw].median()), "n_normal_months": int(ref.sum()),
            "latest": [str(idx[-1].date())[:7], float(share.iloc[-1])],
            "moments_frozen": moments is not None,
            "_moments": {"mean": [float(x) for x in mu_c.ravel()], "sd": [float(x) for x in sd_c.ravel()]},
            "care_vs_rest": {"pp_a_year": float(R[ci, -1]), "z": float(Z[ci, -1]),
                             "rank_of_2047_by_abs_z": int((np.abs(Z[:, -1]) >= abs(Z[ci, -1])).sum())},
            "top5_cuts_now": [{"side_a": [names[i] for i in range(n) if ((m + 1) >> i) & 1], "z": round(float(Z[m, -1]), 2),
                               "pp_a_year": round(float(R[m, -1]), 2)} for m in top]}


def dispersion_recovery_effect(D: dict) -> dict:
    """How much of measure 2's 95th percentile is the first year after a recession's exclusion ends (the recovery):
    the normal months at or above it that fall within the 12 months after the exclusion, and the percentile without
    those months (reported; the threshold keeps them, as the judged windows are not voided in a recovery either)."""
    share, ref = D["share"], D["ref_mask"]
    H = D["window_months"]
    refidx = [t for t in share.index if ref[t]]
    rec_ends = [t for t in D["rec_mask"].index if D["rec_mask"][t] and not D["rec_mask"].get(t + pd.DateOffset(months=1), True)]
    recovery = {t for t in refidx if any(e < t <= e + pd.DateOffset(months=12) for e in rec_ends)}
    above = [t for t in refidx if share[t] >= D["normal_p95"]]
    rest = [t for t in refidx if t not in recovery]
    return {"normal_months_at_or_above_p95": len(above),
            "of_which_in_the_year_after_a_recession_exclusion": sum(t in recovery for t in above),
            "months_at_or_above": [str(t.date())[:7] for t in above],
            "p95_without_those_recovery_years": float(share[rest].quantile(0.95)), "n_without": len(rest),
            "window_months": H}


# ---------------------------------------------------------------------------------------------------------------------
# Conditions on the rivals' calls.

def fed_target(data: dict) -> pd.Series:
    """The fed funds target at the end of each month: the single target (DFEDTAR) to 15 December 2008, then the
    range's upper limit (DFEDTARU)."""
    a, b = data["DFEDTAR"], data["DFEDTARU"]
    s = pd.concat([a[a.index < "2008-12-16"], b[b.index >= "2008-12-16"]]).sort_index()
    m = s.groupby(s.index.to_period("M")).last()
    m.index = m.index.to_timestamp()
    return m


def rate_cut(fed: pd.Series, t, freq: str) -> bool | None:
    """A rate cut in the window ending at t: the target at the window's last month at least RATE_CUT_BP below its level
    twelve months earlier."""
    end = pd.Timestamp(t) + pd.DateOffset(months=FREQ_MONTHS[freq] - 1)
    a, b = end, end - pd.DateOffset(months=12)
    if a not in fed.index or b not in fed.index:
        return None
    return bool(fed[a] <= fed[b] - RATE_CUT_BP / 100 + 1e-9)


def real_rate_rose(rr: pd.Series, t, freq: str, k: int) -> bool | None:
    """The 10-year real interest rate (monthly) averaged over the window's last period, against the period before
    the window (quarterly windows: quarterly means)."""
    f = FREQ_MONTHS[freq]
    t = pd.Timestamp(t)
    s0 = t - pd.DateOffset(months=f * k)
    m1 = [rr.get(t + pd.DateOffset(months=i)) for i in range(f)]
    m0 = [rr.get(s0 + pd.DateOffset(months=i)) for i in range(f)]
    if any(v is None for v in m1 + m0):
        return None
    return bool(np.mean(m1) > np.mean(m0))


# ---------------------------------------------------------------------------------------------------------------------
# Readings.

def fits_of(key: str, r: dict) -> list:
    z = r.get("zone")
    c = r.get("cond") or {}
    if key == "care":
        if not (r["legs"]["jobs"]["E"] is not None and r["legs"]["jobs"]["E"] > 0):
            return []
        return ["paper"] if z == "+" else (["rival"] if z == "-" else [])
    if key == "payroll_dispersion":
        return ["paper"] if z == "+" else ["rival"]
    if key == "hiring":
        if z == "+" or (z == "0" and r["gap"] < 0):
            return ["paper"]
        return ["rival"] if z == "-" and c.get("rate_cut") else []
    if key in ("output_per_hour", "labour_share"):
        return ["paper"] if z == "+" else (["rival"] if z == "0" else [])
    if key == "saving":
        return ["paper"] if z == "+" else (["rival"] if z == "0" and c.get("build_out_turned") else [])
    if key == "asset_income":
        if z == "+":
            return ["paper"]
        ie = r["legs"]["interest"]["E"]
        return ["rival"] if ie is not None and ie >= 1 else []
    if key == "transformer_premium" and c.get("deadline"):
        dl = c["deadline"]
        return ["paper"] if dl["level"] < dl["base"] else ["rival"]
    if key == "site_rent":
        return ["paper"] if z == "+" else (["rival"] if z == "-" and c.get("real_rate_rose") else [])
    if key == "build_out":
        return ["paper"] if z == "+" else (["rival"] if z == "-" and c.get("rate_cut") else [])
    return ["paper"] if z == "+" else (["rival"] if z == "-" else [])


def rival_signed(key: str, r: dict) -> bool:
    """Whether a rival's fit is its signed call (something moved its way) rather than 'nothing unusual'."""
    if "rival" not in r.get("fits", []):
        return False
    if key in NULL_RIVAL:
        return False
    if key == "payroll_dispersion":
        return r.get("zone") == "-"
    return True


def counted_zone(key: str, r: dict) -> str | None:
    """The zone that enters the combined count; care counts only while its jobs leg is above its usual pace."""
    if key == "care" and not (r["legs"]["jobs"]["E"] is not None and r["legs"]["jobs"]["E"] > 0):
        return "0"
    return r.get("zone")


def _at(s: pd.Series, t) -> float | None:
    t = pd.Timestamp(t)
    if s is None or t not in s.index:
        return None
    x = s[t]
    return float(x) if np.isfinite(x) else None


def reading_at(key: str, t, ctx: dict, deadline_base: float | None = None) -> dict | None:
    """The reading of one measure for the window ending at t: zone, counted zone, conditions, which explanation it
    fits, whether a recession touches it and whether that voids it. None when t's change was never published."""
    sp = SPEC[key]
    t = pd.Timestamp(t)
    anyrec = ctx["anyrec"]
    if key == "payroll_dispersion":
        s, p95 = ctx["D"]["share"], ctx["p95"]
        prev = t - pd.DateOffset(months=12)
        if t not in s.index or prev not in s.index:
            return None
        z = "+" if s[t] >= p95 else ("-" if s[prev] >= p95 else "0")
        rec_ = touches(t, "MS", 12, anyrec) or (z == "-" and touches(prev, "MS", 12, anyrec))
        r = {"zone": z, "gap": float(s[t]), "level_start": float(s[prev]), "E_signed": None, "legs": {}, "cond": {}}
    else:
        m = ctx["S"][key]
        e = _at(m["E"], t)
        if e is None:
            return None
        legs = {lk: {"E": _at(lv["E"], t)} for lk, lv in m["legs"].items() if lv["freq"] == sp["freq"]}
        cond = {}
        if key in ("hiring", "build_out"):
            cond["rate_cut"] = rate_cut(ctx["fed"], t, sp["freq"])
        if key == "site_rent":
            cond["real_rate_rose"] = real_rate_rose(ctx["rr"], t, sp["freq"], sp["k"])
        if key == "saving":
            cond["build_out_turned"] = zone(_at(ctx["S"]["build_out"]["E"], t)) == "-"
        if deadline_base is not None:
            cond["deadline"] = {"base": float(deadline_base), "level": _at(m["gap"], t)}
        rec_ = touches(t, sp["freq"], sp["k"], anyrec)
        r = {"zone": zone(e), "gap": _at(m["gap"], t), "E_signed": e, "legs": legs, "cond": cond}
    r["fits"] = fits_of(key, r)
    r["counted_zone"] = counted_zone(key, r)
    r["rival_signed"] = rival_signed(key, r)
    r["recession_in_window"] = bool(rec_)
    r["void"] = bool(rec_) and key not in KEEP_IN_RECESSION
    return r


def base_rates(E: pd.Series, ref_idx, k: int) -> dict:
    """Over reference windows: when |E| >= 1, how often the next non-overlapping window's E has the same sign (the excess
    continues) and is again beyond 1 in that direction (stays clear); the regression of next E on this E (carry-over
    slope, intercept and residual sd), from which the chance that persistence alone gives a reading is computed."""
    pairs = []
    ref_set = set(ref_idx)
    idx = list(E.index)
    pos = {t: i for i, t in enumerate(idx)}
    for t in ref_idx:
        i = pos[t]
        if i + k < len(idx) and idx[i + k] in ref_set:
            pairs.append((E[t], E[idx[i + k]]))
    p = np.array(pairs) if pairs else np.zeros((0, 2))
    vis = np.abs(p[:, 0]) >= 1 if len(p) else np.array([], bool)
    cont = np.sign(p[vis, 0]) == np.sign(p[vis, 1])
    clear = (np.sign(p[vis, 0]) == np.sign(p[vis, 1])) & (np.abs(p[vis, 1]) >= 1)
    slope = icpt = rsd = None
    if len(p) > 5:
        slope, icpt = (float(x) for x in np.polyfit(p[:, 0], p[:, 1], 1))
        rsd = float(np.std(p[:, 1] - (icpt + slope * p[:, 0]), ddof=2))
    return {"n_pairs": int(len(p)), "n_visible": int(vis.sum()),
            "p_continue_when_visible": float(cont.mean()) if vis.sum() else None,
            "p_stays_clear_when_visible": float(clear.mean()) if vis.sum() else None, "carryover_slope": slope,
            "carryover_intercept": icpt, "carryover_residual_sd": rsd}


def _ncdf(x: float) -> float:
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def p_same_zone(br: dict, e: float) -> float | None:
    """The chance that the next window reads the same zone from persistence alone: next E ~ normal(intercept + slope*E,
    residual sd), the carry-over regression over 1990-2019 (or the measure's own history)."""
    if br.get("carryover_slope") is None or br.get("carryover_residual_sd") in (None, 0) or e is None:
        return None
    mu, sd = br["carryover_intercept"] + br["carryover_slope"] * e, br["carryover_residual_sd"]
    z = zone(e)
    if z == "+":
        return 1 - _ncdf((1 - mu) / sd)
    if z == "-":
        return _ncdf((-1 - mu) / sd)
    return _ncdf((1 - mu) / sd) - _ncdf((-1 - mu) / sd)


def leg_frequency(key: str, lk: str, freq: str) -> tuple:
    lfreq = "QS" if (key == "asset_income" and lk == "rent") else freq
    return lfreq, (4 if lfreq == "QS" else 12)


def measure_series(key: str, sp: dict, b: dict, rec: set, frozen: dict | None) -> dict:
    """A measure's window changes and E series. The reference is the 1990-2019 non-recession windows (measure 4: its
    own history to the window before the latest); `frozen` (the baseline's entry) replaces it, and its legs', once the
    tracker is fixed."""
    gap, freq, k, dirn = b["gap"], sp["freq"], sp["k"], sp["direction"]
    ch = gap - gap.shift(k)
    min_n = 120 if freq == "MS" else 40
    t = ch.dropna().index[-1]
    ref = reference(ch, freq, k, rec, min_n, upto=t - pd.DateOffset(months=FREQ_MONTHS[freq] * k))
    use = dict(frozen["reference"]) if frozen else ref
    out = {"gap": gap, "ch": ch, "ref": ref, "use": use, "E": e_series(ch, use, dirn), "latest": t, "legs": {}}
    for lk, ls_ in b["legs"].items():
        lfreq, lk_k = leg_frequency(key, lk, freq)
        lch = ls_ - ls_.shift(lk_k)
        lt = lch.dropna().index[-1]
        lref = reference(lch, lfreq, lk_k, rec, 120 if lfreq == "MS" else 40,
                         upto=lt - pd.DateOffset(months=FREQ_MONTHS[lfreq] * lk_k))
        luse = dict(frozen["legs"][lk]["reference"]) if frozen and lk in frozen.get("legs", {}) else lref
        out["legs"][lk] = {"series": ls_, "ch": lch, "ref": lref, "use": luse, "freq": lfreq, "latest": lt,
                           "E": (lch - luse["mean"]) / luse["sd"]}
    return out


def measure_reading(key: str, sp: dict, b: dict, rec: set, sahm: set, frozen: dict | None = None) -> dict:
    """One measure's latest reading on its own (no conditions from other measures or rates): for the checks."""
    S_ = {key: measure_series(key, sp, b, rec, frozen)}
    ctx = {"S": S_, "D": None, "p95": None, "rec": rec, "sahm": sahm, "anyrec": rec | sahm,
           "fed": pd.Series(dtype=float), "rr": pd.Series(dtype=float)}
    lr = latest_reading(key, sp, ctx)
    return {"ref": S_[key]["ref"], "E": S_[key]["E"], "reading": lr["reading"], "base_rates": lr["base_rates"]}


def latest_reading(key: str, sp: dict, ctx: dict) -> dict:
    """The latest rolling window's reading, with its legs, its starting-point comparisons and the naive forecasts."""
    m = ctx["S"][key]
    gap, ch, use, freq, k = m["gap"], m["ch"], m["use"], sp["freq"], sp["k"]
    t = m["latest"]
    r = reading_at(key, t, ctx)
    r.update({"date": str(t.date()), "change": float(ch[t]), "E": float(sp["direction"] * r["E_signed"])})
    b19 = pd.Timestamp("2019-12-01" if freq == "MS" else "2019-10-01")
    r["change_since_2019"] = float(gap[t] - gap[b19]) if b19 in gap.index and np.isfinite(gap[b19]) else None
    legs = {}
    for lk, lv in m["legs"].items():
        lt = lv["latest"]
        legs[lk] = {"date": str(lt.date()), "level": float(lv["series"][lt]), "change": float(lv["ch"][lt]),
                    "E": float(lv["E"][lt]), "reference": {x: lv["use"][x] for x in lv["use"] if not x.startswith("_")}}
    r["legs"] = legs
    br = base_rates(e_series(ch, m["ref"], sp["direction"]), m["ref"]["_index"], k)
    r["carry_forward"] = {"E_if_the_last_window_repeats": r["E_signed"],
                          "E_expected_from_persistence": (br["carryover_intercept"] + br["carryover_slope"] * r["E_signed"])
                          if br["carryover_slope"] is not None else None,
                          "p_same_zone_from_persistence": p_same_zone(br, r["E_signed"])}
    return {"reading": r, "base_rates": br}


def thresholds_plain(key: str, use: dict, sp: dict) -> dict:
    """The ±1 thresholds in the measure's own units: the change over the window at which it reads the paper's way or
    the other way (log-point gaps as % changes of the ratio)."""
    lo, hi = use["mean"] - use["sd"], use["mean"] + use["sd"]
    paper, other = (hi, lo) if sp["direction"] > 0 else (lo, hi)
    log = "log points" in sp["gap"]
    conv = (lambda x: 100 * (math.exp(x / 100) - 1)) if log else (lambda x: x)
    rel = ">=" if sp["direction"] > 0 else "<="
    orel = "<=" if sp["direction"] > 0 else ">="
    return {"units": "% change of the ratio over the window" if log else "points over the window",
            "paper_if_change": f"{rel} {conv(paper):+.2f}", "other_way_if_change": f"{orel} {conv(other):+.2f}",
            "paper_at": float(conv(paper)), "other_at": float(conv(other))}


# ---------------------------------------------------------------------------------------------------------------------
# The combined reading.

def verdict(count: int, tc: dict, normal: dict, recession: bool) -> str:
    """SPLITS.md section 6: supports the paper / favours the rivals / nothing unusual / inconclusive; a recession voids
    the window."""
    if recession:
        return "void for the paper against the cycle: a recession touches the window"
    p, r, rs = tc.get("paper", 0), tc.get("rival", 0), tc.get("rival_signed", 0)
    if count > normal["p90"] and p >= 2 * r and p > 0:
        return "supports the paper"
    if rs >= 2 * p and rs > 0:
        return "favours the rivals"
    if count <= normal["median"] or (p == 0 and rs == 0):
        return "nothing unusual"
    return "inconclusive"


RETIRING = ("favours the rivals", "nothing unusual")


def tally_of(readings: dict, keys) -> tuple:
    """The count (+ minus -, counted zones) and the tally (which explanation each fits) over `keys`."""
    cz = [readings[k]["counted_zone"] for k in keys]
    count = sum(z == "+" for z in cz) - sum(z == "-" for z in cz)
    tally = {"paper": [], "rival": [], "both": [], "neither": [], "rival_signed": []}
    for k in keys:
        f = readings[k]["fits"]
        tally["both" if len(f) == 2 else (f[0] if f else "neither")].append(SPEC[k]["id"])
        if readings[k].get("rival_signed"):
            tally["rival_signed"].append(SPEC[k]["id"])
    return int(count), tally, {k: len(v) for k, v in tally.items()}


def benchmark_stats(by_year: dict, ids: list) -> dict:
    """The count over `ids` in every benchmark year (1990-2019, all eleven measures available, no recession or Sahm
    month in any window): its median, 90th percentile and range."""
    counts = []
    for y, v in sorted(by_year.items()):
        if not v["in_benchmark"]:
            continue
        zs = [v["zones"][str(i)] for i in ids]
        counts.append(sum(z == "+" for z in zs) - sum(z == "-" for z in zs))
    if not counts:
        return {"n": 0, "median": float("nan"), "p90": float("nan"), "min": None, "max": None, "years": []}
    return {"n": len(counts), "median": float(np.median(counts)), "p90": float(np.quantile(counts, 0.9)),
            "min": int(min(counts)), "max": int(max(counts)),
            "years": [int(y) for y, v in sorted(by_year.items()) if v["in_benchmark"]]}


def combined_reading(readings: dict, keys: list, by_year: dict, recession: bool) -> dict:
    """Count, tally and verdict over `keys` against the benchmark over the same measures, with each channel left out in
    turn (a verdict that flips without a channel rests on it)."""
    ids = [SPEC[k]["id"] for k in keys]
    normal = benchmark_stats(by_year, ids)
    count, tally, tc = tally_of(readings, keys)
    v = verdict(count, tc, normal, recession)
    loo = {}
    for ch, chids in CHANNELS.items():
        k2 = [k for k in keys if SPEC[k]["id"] not in chids]
        n2 = benchmark_stats(by_year, [SPEC[k]["id"] for k in k2])
        c2, _t2, tc2 = tally_of(readings, k2)
        loo[ch] = {"count": c2, "normal_p90": n2["p90"], "normal_median": n2["median"], "verdict": verdict(c2, tc2, n2, recession)}
    return {"count": count, "tally": tally, "tally_counts": tc, "normal": normal, "verdict": v, "leave_one_channel_out": loo,
            "rests_on_channel": [ch for ch, x in loo.items() if x["verdict"] != v]}


def history_table(ctx: dict, month_of: dict, years=range(1990, 2026)) -> dict:
    """Every year's readings with each measure's window ending in the calendar month its judged windows end in (the
    baseline's month; before the freeze, its latest month): zones and fits per measure, whether a recession or a Sahm
    month touches any window (void), whether all eleven counted measures exist, and whether it enters the benchmark
    (1990-2019, complete, not void)."""
    out = {}
    for y in years:
        rd = {}
        for k in SPEC:
            r = reading_at(k, pd.Timestamp(year=y, month=month_of[k], day=1), ctx)
            if r is not None:
                rd[k] = r
        complete = all(k in rd for k in COUNT_KEYS)
        nber = any(touches(pd.Timestamp(year=y, month=month_of[k], day=1), SPEC[k]["freq"], SPEC[k]["k"], ctx["rec"])
                   for k in COUNT_KEYS)
        void = any(rd[k]["recession_in_window"] for k in rd if k in COUNT_KEYS)
        row = {"complete": complete, "recession": bool(nber), "void": bool(void),
               "in_benchmark": bool(complete and not void and y <= 2019),
               "n_measures": sum(k in rd for k in COUNT_KEYS),
               "zones": {str(SPEC[k]["id"]): rd[k]["counted_zone"] for k in rd},
               "fits": {str(SPEC[k]["id"]): rd[k]["fits"] for k in rd},
               "rival_signed": [SPEC[k]["id"] for k in rd if rd[k]["rival_signed"]]}
        if complete:
            c, _t, tc = tally_of(rd, COUNT_KEYS)
            row.update({"count": c, "paper": sum(rd[k]["counted_zone"] == "+" for k in COUNT_KEYS),
                        "other": sum(rd[k]["counted_zone"] == "-" for k in COUNT_KEYS), "tally_counts": tc})
        out[str(y)] = row
    return out


def historical_verdicts(by_year: dict) -> dict:
    """The rules applied to every year (SPLITS.md section 5): the verdicts in the benchmark years, how many pairs of
    consecutive non-void years would have met the retirement rule, and the verdicts of 2020-2025 (the explore years)."""
    ids = [SPEC[k]["id"] for k in COUNT_KEYS]
    normal = benchmark_stats(by_year, ids)
    v = {}
    for y, row in sorted(by_year.items()):
        if not row["complete"]:
            continue
        v[y] = verdict(row["count"], row["tally_counts"], normal, row["void"])
    bench = [y for y in sorted(by_year) if by_year[y]["in_benchmark"]]
    counts = {k: sum(v[y] == k for y in bench) for k in ("supports the paper", "favours the rivals", "nothing unusual", "inconclusive")}
    pairs = list(zip(bench, bench[1:]))
    retire = [p for p in pairs if v[p[0]] in RETIRING and v[p[1]] in RETIRING]
    retire_signed = [p for p in pairs if v[p[0]] == v[p[1]] == "favours the rivals"]
    return {"benchmark_years": counts, "n_benchmark_years": len(bench),
            "consecutive_pairs": len(pairs), "pairs_meeting_the_retirement_rule": len(retire),
            "pairs_both_favouring_the_rivals": len(retire_signed),
            "by_year": {y: v[y] for y in v}}


def judged_dispersion(share: pd.Series, base_date, p95: float) -> list:
    """Measure 2's judged windows: non-overlapping 12-month windows from the baseline's last observation; the share at
    each end is 12-month growth, so it holds no data from before the window's start; the zone is + when the window ends
    at or above the frozen 95th percentile, - when it started at or above and ended below."""
    b0 = pd.Timestamp(base_date)
    out, j = [], 1
    while b0 + pd.DateOffset(months=12 * j) <= share.index[-1]:
        a_, e_ = b0 + pd.DateOffset(months=12 * (j - 1)), b0 + pd.DateOffset(months=12 * j)
        if a_ in share.index and e_ in share.index:
            zz = "+" if share[e_] >= p95 else ("-" if share[a_] >= p95 else "0")
            out.append({"start": str(a_.date()), "end": str(e_.date()), "level": float(share[e_]), "zone": zz})
        else:
            out.append({"start": str(a_.date()), "end": str(e_.date()), "level": None, "zone": None,
                        "note": "an end point was never published"})
        j += 1
    return out


def judged_measure(key: str, sp: dict, ctx: dict, fb: dict) -> list:
    """Every judged window of a measure after the fixed date, enriched with its reading (fits, conditions, recession)."""
    b = pd.Timestamp(fb["last_obs"])
    if key == "payroll_dispersion":
        jw = judged_dispersion(ctx["D"]["share"], b, ctx["p95"])
    else:
        m = ctx["S"][key]
        jw = judged_windows(m["gap"], b, sp["k"], fb["reference"], sp["direction"])
    for j, w in enumerate(jw, 1):
        if w["zone"] is None:
            w.update({"legs_E": {}, "fits": [], "counted_zone": None, "rival_signed": False, "recession_in_window": False,
                      "void": False, "cond": {}})
            continue
        base = None
        if DEADLINE_WINDOW.get(key) == j:
            base = _at(ctx["S"][key]["gap"], b)
        r = reading_at(key, w["end"], ctx, base)
        w.update({"legs_E": {lk: v["E"] for lk, v in r["legs"].items()}, "fits": r["fits"], "counted_zone": r["counted_zone"],
                  "rival_signed": r["rival_signed"], "recession_in_window": r["recession_in_window"], "void": r["void"],
                  "cond": r["cond"]})
        if key != "payroll_dispersion":
            w["zone_check"] = r["zone"] == w["zone"]
    return jw


def combined_judged(jws: dict, by_year: dict, fixed: dt.date | None, today: dt.date, looks: dict | None) -> list:
    """The combined reading over judged windows: window j across the eleven counted measures (measure 4 beside). A
    window is complete when every counted measure's window end has passed; an end that was never published is left out
    of the count and of the benchmark. The verdict waits for the yearly look; a look that has been tagged stands, and
    the same window on revised data is reported beside it."""
    out = []
    n = max((len(v) for v in jws.values() if v), default=0)
    for j in range(1, n + 1):
        have = {k: jws[k][j - 1] for k in COUNT_KEYS if jws.get(k) and len(jws[k]) >= j}
        complete = len(have) == len(COUNT_KEYS)
        keys = [k for k in COUNT_KEYS if k in have and have[k]["zone"] is not None]
        missing = [SPEC[k]["id"] for k in COUNT_KEYS if k in have and have[k]["zone"] is None]
        rec = any(w.get("recession_in_window") for w in have.values())
        cr = combined_reading(have, keys, by_year, rec) if keys else None
        ld = look_date(fixed, j) if fixed else None
        row = {"window": j, "n_measures": len(have), "complete": complete, "missing_ends": missing,
               "look_date": str(ld) if ld else None, "recession": rec,
               "count": cr["count"] if cr else None, "tally": cr["tally"] if cr else None,
               "tally_counts": cr["tally_counts"] if cr else None, "normal": cr["normal"] if cr else None,
               "leave_one_channel_out": cr["leave_one_channel_out"] if cr else None,
               "rests_on_channel": cr["rests_on_channel"] if cr else []}
        b4 = (jws.get("software_postings") or [])
        row["beside_the_count"] = {"id": 4, "zone": b4[j - 1]["counted_zone"] if len(b4) >= j else None,
                                   "fits": b4[j - 1]["fits"] if len(b4) >= j else []}
        if not complete:
            row["verdict"] = "not all measures complete"
        elif ld is not None and today < ld:
            row["verdict"] = "awaiting the yearly look"
        else:
            row["verdict"] = cr["verdict"] if cr else "not all measures complete"
        lk = (looks or {}).get(j)
        if lk:
            row["verdict_on_revised_data"] = row["verdict"]
            row["verdict"] = lk["combined"]["verdict"]
            row["look"] = {"tag": lk.get("tag"), "written_utc": lk.get("written_utc"), "count": lk["combined"].get("count")}
        out.append(row)
    return out


def _v(s: pd.Series, d) -> float | None:
    """A series' value at a date, or None when that date was never published (October 2025's household survey and CPI)."""
    d = pd.Timestamp(d)
    if d not in s.index:
        return None
    x = s[d]
    return float(x) if np.isfinite(x) else None


def _pct(s: pd.Series, a, b) -> float | None:
    x, y = _v(s, a), _v(s, b)
    return None if x is None or y is None else 100 * (x / y - 1)


def _diff(s: pd.Series, a, b) -> float | None:
    x, y = _v(s, a), _v(s, b)
    return None if x is None or y is None else x - y


def plain_facts(key: str, f: dict, B: dict, t: str) -> dict:
    """The underlying numbers behind each reading, in their own units, for plain statements (number and date first).
    A value whose date was never published is None."""
    t = pd.Timestamp(t)
    y = t - pd.DateOffset(years=1)
    d19 = pd.Timestamp("2019-12-01")
    if key == "care":
        care, pay = f["CES6562000001"], f["PAYEMS"]
        return {"care_jobs_change_12m_thousands": _diff(care, t, y), "other_jobs_change_12m_thousands": _diff(pay - care, t, y),
                "care_relative_pay_change_12m_pct": _pct(f["CES6500000008"] / f["AHETPI"], t, y),
                "care_hourly_pay_usd": _v(f["CES6500000008"], t), "all_private_hourly_pay_usd": _v(f["AHETPI"], t)}
    if key == "graduates":
        a = regular(f["LNS14027662"], "MS").rolling(3, min_periods=2).mean()
        b = regular(f["LNS14027660"], "MS").rolling(3, min_periods=2).mean()
        r = a / b
        return {"bachelors_plus_rate_3m": _v(a, t), "high_school_rate_3m": _v(b, t), "ratio": _v(r, t), "ratio_12m_earlier": _v(r, y)}
    if key == "software_postings":
        a, b = month_mean(f["IHLIDXUSTPSOFTDEVE"]), month_mean(f["IHLIDXUS"])
        return {"software_index": _v(a, t), "all_postings_index": _v(b, t), "software_index_12m_earlier": _v(a, y),
                "all_postings_index_12m_earlier": _v(b, y), "software_peak": [str(a.idxmax().date())[:7], float(a.max())],
                "software_low": [str(a.idxmin().date())[:7], float(a.min())], "index_base": "1 Feb 2020 = 100"}
    if key == "hiring":
        fit = B["hiring"]["fit"]
        u = _v(f["UNRATE"], t)
        return {"hires_rate": _v(f["JTSHIR"], t), "unemployment_rate": u,
                "hires_rate_implied": None if u is None else fit["intercept"] + fit["slope_on_unrate"] * u}
    if key == "output_per_hour":
        g = f["OUTNFB"] / f["HOANBS"]
        g8 = _v(g, t - pd.DateOffset(months=24))
        avg = 100 * ((_v(g, "2019-10-01") / _v(g, "1990-01-01")) ** (1 / 29.75) - 1)
        return {"growth_4q_pct": _pct(g, t, y), "growth_8q_pct_a_year": None if g8 is None else 100 * ((_v(g, t) / g8) ** 0.5 - 1),
                "average_1990_2019_pct_a_year": avg, "output_growth_4q_pct": _pct(f["OUTNFB"], t, y), "hours_growth_4q_pct": _pct(f["HOANBS"], t, y)}
    if key == "labour_share":
        ls = (100 * f["A460RC1Q027SBEA"] / f["A455RC1Q027SBEA"]).dropna()
        lower = ls[:t][ls[:t] <= ls[t]]
        gp = B["labour_share"]["gap"]
        return {"share_pct": _v(ls, t), "share_pct_12m_earlier": _v(ls, y), "share_pct_2019q4": _v(ls, "2019-10-01"),
                "share_change_12m_pts": _diff(ls, t, y), "adjusted_change_12m_pts": _diff(gp, t, y),
                "earlier_quarters_at_or_below": [str(x.date())[:7] for x in lower.index[:-1]][-5:],
                "lowest_in_series_since": str(ls.index[0].date())[:7] if len(lower) == 1 else None}
    if key == "asset_income":
        c = f["W209RC1"]
        return {"dividends_pct_of_pay": _v(100 * f["PDI"] / c, t), "dividends_pct_of_pay_12m_earlier": _v(100 * f["PDI"] / c, y),
                "interest_pct_of_pay": _v(100 * f["PII"] / c, t), "interest_pct_of_pay_12m_earlier": _v(100 * f["PII"] / c, y)}
    if key == "transformer_premium":
        a, b = f["PCU335311335311"], f["WPUFD49207"]
        return {"transformer_ppi_change_12m_pct": _pct(a, t, y), "finished_goods_ppi_change_12m_pct": _pct(b, t, y),
                "relative_change_since_2019_12_pct": _pct(a / b, t, d19), "transformer_ppi_change_since_2019_12_pct": _pct(a, t, d19)}
    if key == "site_rent":
        land = B["site_rent"]["land_tn"]
        ratio = np.exp(B["site_rent"]["gap"] / 100)
        return {"land_value_tn_usd": _v(land, t), "land_value_tn_usd_12m_earlier": _v(land, y),
                "land_to_annual_pay": _v(ratio, t), "land_to_annual_pay_12m_earlier": _v(ratio, y)}
    if key == "build_out":
        return {"it_investment_real_growth_4q_pct": _pct(f["B679RA3Q086SBEA"], t, y),
                "housing_investment_real_growth_4q_pct": _pct(f["A011RA3Q086SBEA"], t, y)}
    if key == "saving":
        sv, gp, x = B["saving"]["level"], B["saving"]["gap"], B["saving"]["equity_to_income"]
        rng = B["saving"]["fit_current_vintage"]["equity_to_income_range_in_fit"]
        xt = _v(x, t)
        return {"saving_rate_pct": _v(sv, t), "saving_rate_pct_12m_earlier": _v(sv, y),
                "fitted_from_equity_wealth_pct": _v(sv - gp, t), "residual_pts": _v(gp, t),
                "equity_to_income": xt, "equity_to_income_12m_earlier": _v(x, y), "equity_to_income_range_in_fit": rng,
                "equity_to_income_outside_fit_range": None if xt is None else bool(xt > rng[1] or xt < rng[0])}
    return {}


def saving_alternatives(B: dict, rec: set) -> dict:
    """Measure 12's latest E under other wealth slopes (reported; the choice of slope is hers before the freeze): the
    1990-2019 fit, about one cent of spending per dollar of equity wealth (slope -1 point per unit of the
    equity-to-income ratio), and no wealth term (the saving rate itself)."""
    sv, x = B["saving"]["level"], B["saving"]["equity_to_income"]
    d = pd.concat([sv, x], axis=1, sort=True).dropna()
    d.columns = ["s", "x"]
    f9 = d["1990-01-01":"2019-12-31"]
    s9 = float(np.polyfit(f9.x, f9.s, 1)[0])
    out = {}
    for name, slope in (("as built", B["saving"]["fit"]["slope_on_equity_to_income"]), ("1990-2019 fit", s9),
                        ("slope -1 (about 1 cent per dollar of equity wealth)", -1.0), ("no wealth term", 0.0)):
        g = regular(d.s - slope * d.x, "QS")
        ch = g - g.shift(4)
        ref = reference(ch, "QS", 4, rec, 40)
        t = ch.dropna().index[-1]
        out[name] = {"slope": slope, "E": float((ch[t] - ref["mean"]) / ref["sd"]), "date": str(t.date())[:7]}
    return out


def labour_share_raw_E(B: dict, rec: set) -> dict:
    """Measure 7's latest E on the raw share (no unemployment adjustment), reported beside the adjusted one."""
    ls = B["labour_share"]["level"]
    ch = ls - ls.shift(4)
    ref = reference(ch, "QS", 4, rec, 40)
    t = ch.dropna().index[-1]
    return {"E_signed": float(-(ch[t] - ref["mean"]) / ref["sd"]), "change_pts": float(ch[t]), "date": str(t.date())[:7]}


def fred_titles(refresh: bool = False) -> dict:
    """FRED's own title for every manifest series (the series page), cached; the checks confirm each ID against it."""
    import requests
    fp = os.path.join(CACHE, "titles.json")
    try:
        T = json.load(open(fp, encoding="utf-8"))
    except (OSError, ValueError):
        T = {}
    for sid in MANIFEST:
        if sid in T and T[sid].get("title") and not refresh:
            continue
        try:
            r = requests.get(f"https://fred.stlouisfed.org/series/{sid}", timeout=30)
            m = re.search(r"<title>(.*?)</title>", r.text, re.S)
            title = re.sub(r"\s+", " ", m.group(1)).strip() if m else ""
            title = re.sub(r"\s*\(" + re.escape(sid) + r"\)\s*\|\s*FRED\s*\|\s*St\. Louis Fed\s*$", "", title)
            T[sid] = {"title": title.replace("&amp;", "&").replace("&#39;", "'"), "status": r.status_code, "checked_utc": _now()}
        except Exception as e:  # noqa: BLE001
            T[sid] = {"title": None, "status": f"error: {e}"[:80], "checked_utc": _now()}
    T = {sid: T[sid] for sid in MANIFEST if sid in T}
    json.dump(T, open(fp, "w", encoding="utf-8"), indent=1)
    return T


# ---------------------------------------------------------------------------------------------------------------------
# Watch list and context.

def watch(data: dict) -> list:
    out = []
    d19 = pd.Timestamp("2019-12-01")
    for w in WATCH_SPECS:
        key = w["key"]
        if key in ("big_vs_rest", "large_vs_small"):
            a, b = (month_mean(data[s]) for s in w["series"])
            g = L(a / b).dropna()
            t = g.index[-1]
            item = {"date": str(t.date())[:7], "level": float(g[t]), "units": "log points (cap-weighted over equal-weighted)"
                    if key == "big_vs_rest" else "log points (large over small)",
                    "change_12m": _diff(g, t, t - pd.DateOffset(months=12)), "change_since_2019_12": _diff(g, t, d19),
                    "level_2019_12": _v(g, d19), "level_2022_12": _v(g, "2022-12-01"),
                    "change_since_2022_12": _diff(g, t, "2022-12-01"),
                    "path_since_2025_12": [[str(x.date())[:7], round(float(v), 2)] for x, v in g["2025-12-01":].items()],
                    "_series": g}
        elif key == "computer_imports":
            g = (100 * data["B852RC1Q027SBEA"] / data["Y034RC1Q027SBEA"]).dropna()
            t = g.index[-1]
            item = {"date": str(t.date())[:7], "level": float(g[t]), "units": "% of investment in information processing equipment",
                    "change_4q": _diff(g, t, t - pd.DateOffset(months=12)), "max_before_2020": float(g[:"2019-12-31"].max()),
                    "avg_2015_2019": float(g["2015":"2019"].mean()), "_series": g}
        elif key == "electricity":
            g = L(data["CUSR0000SEHF01"] / data["CPIAUCSL"]).dropna()
            t = g.index[-1]
            item = {"date": str(t.date())[:7], "level": float(g[t]), "units": "log points (relative price)",
                    "change_12m": _diff(g, t, t - pd.DateOffset(months=12)), "change_since_2019_12": _diff(g, t, d19), "_series": g}
        elif key == "consumption_share":
            g = (100 * data["PCEC"] / data["GDP"]).dropna()
            t = g.index[-1]
            item = {"date": str(t.date())[:7], "level": float(g[t]), "units": "% of GDP", "change_4q": _diff(g, t, t - pd.DateOffset(months=12)),
                    "avg_2015_2019": float(g["2015":"2019"].mean()), "_series": g}
        elif key == "se_property_income":
            rec = read_scb("sector_S14.json", ("S14", "D4.REC")).rolling(4).sum()
            pay = read_scb("sector_S14.json", ("S14", "D4.PAY")).rolling(4).sum()
            gdp = read_scb("gdp_current_sa.json", ("BNPM",)).rolling(4).sum()
            g = (100 * (rec - pay) / gdp).dropna()
            gr = (100 * rec / gdp).dropna()
            t = g.index[-1]
            upd = json.load(open(os.path.join(SCB, "sector_S14.json"), encoding="utf-8"))["metadata"][0].get("updated")
            item = {"date": str(t.date())[:7], "level": float(g[t]), "units": "% of GDP, 4-quarter sums",
                    "received_pct_gdp": float(gr[t]), "change_4q": _diff(g, t, t - pd.DateOffset(months=12)),
                    "avg_2015_2019": float(g["2015":"2019"].mean()), "max": [str(g.idxmax().date())[:7], float(g.max())],
                    "vintage": f"Statistics Sweden NR0103, cached (table updated {upd})", "_series": g}
        out.append({"key": key, "name": w["name"], "series": w["series"], "note": w["note"], **item})
    return out


def context(data: dict) -> dict:
    """Reported, never judged: the wealth shares of the richest 1% and 10% of US households (Federal Reserve
    Distributional Financial Accounts, quarterly from 1989Q3), for the website's spending section."""
    t1 = data["WFRBST01134"].dropna()
    t10 = (data["WFRBST01134"] + data["WFRBSN09161"]).dropna()
    t = t1.index[-1]
    prev = t1[t1.index < t]
    return {"wealth": {
        "source": "Federal Reserve Distributional Financial Accounts (FRED WFRBST01134, WFRBSN09161)",
        "series_start": str(t1.index[0].date())[:7], "date": str(t.date())[:7],
        "top1_pct": float(t1[t]), "top1_previous_high": [str(prev.idxmax().date())[:7], float(prev.max())],
        "top1_is_series_high": bool(t1[t] > prev.max()),
        "top10_pct": float(t10[t]), "top10_peak": [str(t10.idxmax().date())[:7], float(t10.max())],
        "top10_is_series_high": bool(t10[t] >= t10.max())}}


# ---------------------------------------------------------------------------------------------------------------------
# The freeze.

def _git(*args) -> str | None:
    try:
        r = subprocess.run(["git", "-C", REPO, *args], capture_output=True, text=True, timeout=30)
        return r.stdout.strip() if r.returncode == 0 else None
    except (OSError, subprocess.SubprocessError):
        return None


BASELINE_IN_REPO = "paths/results/splits_baseline.json"   # the baseline's path in the tagged commit
CODE_IN_REPO = "paths/code/splits.py"
LOOK_IN_REPO = "paths/results/splits_look_{year}.json"


def _read_json(fp: str) -> dict | None:
    try:
        return json.load(open(fp, encoding="utf-8"))
    except (OSError, ValueError):
        return None


def file_hash(fp: str) -> str | None:
    """SHA-256 of a text file with line endings normalised (a checkout with LF or CRLF hashes the same)."""
    try:
        return hashlib.sha256(open(fp, "rb").read().replace(b"\r\n", b"\n")).hexdigest()
    except OSError:
        return None


# The code that defines and judges the measures: its source enters the definitions hash, so a change to any of it
# after the freeze is labelled a deviation (plumbing — fetching, parsing, output — lives outside these functions).
DEFINING = ("month_mean", "q_mean", "regular", "window_months", "touches", "recession_months", "zone", "reference",
            "e_series", "judged_windows", "fifteenth_november_after", "look_date", "build", "dispersion", "fed_target",
            "rate_cut", "real_rate_rose", "fits_of", "rival_signed", "counted_zone", "reading_at", "measure_series",
            "verdict", "tally_of", "benchmark_stats", "combined_reading", "history_table", "judged_dispersion",
            "judged_measure", "combined_judged")


def definitions_hash() -> str:
    g = globals()
    src = {name: inspect.getsource(g[name]).replace("\r\n", "\n") for name in DEFINING}
    d = {"specs": SPECS, "units": UNITS, "dispersion": DISPERSION, "reference": REF,
         "watch": [w["series"] for w in WATCH_SPECS], "count_keys": COUNT_KEYS, "keep_in_recession": KEEP_IN_RECESSION,
         "null_rival": NULL_RIVAL, "channels": CHANNELS, "deadline": DEADLINE_WINDOW, "rate_cut_bp": RATE_CUT_BP,
         "code": src}
    return _sha(json.dumps(d, sort_keys=True))


def _days_between(a: str | None, b: str | None) -> float | None:
    try:
        ta, tb = pd.Timestamp(a), pd.Timestamp(b)
        if ta.tzinfo is None:
            ta = ta.tz_localize("UTC")
        if tb.tzinfo is None:
            tb = tb.tz_localize("UTC")
        return float((ta - tb).total_seconds() / 86400)
    except (ValueError, TypeError):
        return None


def freeze_state(tag_exists: bool | None = None, baseline: dict | None = None, tag_date: str | None = None,
                 previous: dict | None = None) -> tuple:
    """Whether the tracker is fixed. Once the tag exists, the baseline is the one committed in the tagged commit
    (`git show <tag>:paths/results/splits_baseline.json`), never the working copy; a working copy that differs is
    flagged. A tag whose commit holds no baseline judges nothing. The tagged commit's SHA is recorded (and a tag that
    has moved since the previous run is flagged), and a tag made more than a day after the baseline was written is
    flagged (data published in between were seen). Passing `tag_exists`/`baseline` bypasses git (tests)."""
    source = "given" if baseline is not None else None
    working = _read_json(BASELINE) if os.path.exists(BASELINE) else None
    tag_commit = None
    if tag_exists is None:
        tag_exists = bool(_git("tag", "-l", TAG))
        if tag_exists:
            tag_commit = _git("rev-list", "-n", "1", TAG)
            tag_date = (_git("for-each-ref", f"refs/tags/{TAG}", "--format=%(taggerdate:iso-strict)") or
                        _git("log", "-1", "--format=%cI", TAG))
        if tag_exists and baseline is None:
            txt = _git("show", f"{TAG}:{BASELINE_IN_REPO}")
            try:
                baseline = json.loads(txt) if txt else None
            except ValueError:
                baseline = None
            source = "tagged commit" if baseline is not None else None
    if baseline is None and not tag_exists and working is not None:
        baseline, source = working, "working copy"
    st = {"tag": TAG, "tag_exists": bool(tag_exists), "tag_date": tag_date, "tag_commit": tag_commit,
          "baseline_exists": baseline is not None, "baseline_source": source, "frozen": bool(tag_exists and baseline is not None),
          "definitions_match": None, "protocol_match": None, "code_matches_baseline": None,
          "baseline_working_copy_differs": None, "tag_days_after_baseline": None, "tag_moved_since_last_run": None,
          "flags": []}
    if baseline is not None:
        st["definitions_match"] = baseline.get("definitions_sha256") == definitions_hash()
        st["protocol_match"] = baseline.get("protocol_sha256") == file_hash(PROTOCOL)
        st["code_matches_baseline"] = baseline.get("code_sha256") == file_hash(os.path.abspath(__file__))
        st["baseline_written_utc"] = baseline.get("written_utc")
        if source == "tagged commit":
            st["baseline_working_copy_differs"] = working != baseline
    if st["frozen"]:
        gap = _days_between(tag_date, baseline.get("written_utc"))
        st["tag_days_after_baseline"] = gap
        if gap is not None and gap > 1.0:
            st["flags"].append(f"the tag was made {gap:.1f} days after the baseline was written: data published in "
                               "between were seen before the freeze")
        old = ((previous or {}).get("status") or {}).get("tag_commit")
        if tag_commit and old and old != tag_commit:
            st["tag_moved_since_last_run"] = True
            st["flags"].append(f"the tag has moved since the last run (from {old[:12]} to {tag_commit[:12]})")
        st["label"] = FROZEN_LABEL
        if not (st["definitions_match"] and st["protocol_match"]):
            st["label"] += " (deviation: definitions changed since the fixed date)"
        if st["code_matches_baseline"] is False:
            st["label"] += " (the code has changed since the fixed date; the tagged code's judged readings are used)"
        if st["baseline_working_copy_differs"]:
            st["label"] += " (the working copy of the baseline differs from the tagged one; the tagged one is used)"
        if st["flags"]:
            st["label"] += " (" + "; ".join(st["flags"]) + ")"
    elif tag_exists:
        st["label"] = "tag without a committed baseline file: not judged"
    elif baseline is not None:
        st["label"] = "baseline written, not yet tagged: " + UNFROZEN_LABEL
    else:
        st["label"] = UNFROZEN_LABEL
    return st, baseline


def tagged_code():
    """The tagged commit's copy of this file as a module (run beside the working copy when the two differ), or None."""
    src = _git("show", f"{TAG}:{CODE_IN_REPO}")
    if not src:
        return None
    import linecache
    fn = os.path.abspath(__file__) + " (tagged)"
    src = src.replace(chr(13) + chr(10), chr(10)) + chr(10)
    linecache.cache[fn] = (len(src), None, src.splitlines(True), fn)    # so inspect.getsource works on it
    mod = types.ModuleType("splits_tagged")
    mod.__file__ = os.path.abspath(__file__)
    exec(compile(src, fn, "exec"), mod.__dict__)  # noqa: S102
    return mod


def read_looks(fixed: dt.date | None, today: dt.date) -> dict:
    """The yearly looks that have been tagged (`paths-splits-look-<year>`), read from their tagged commits."""
    out = {}
    if fixed is None:
        return out
    j = 1
    while look_date(fixed, j) <= today:
        y = look_date(fixed, j).year
        tag = LOOK_TAG.format(year=y)
        if _git("tag", "-l", tag):
            txt = _git("show", f"{tag}:{LOOK_IN_REPO.format(year=y)}")
            try:
                lk = json.loads(txt) if txt else None
            except ValueError:
                lk = None
            if lk:
                lk["tag"] = tag
                out[j] = lk
        j += 1
    return out


def write_baseline(X: dict, vint: dict, data: dict, titles: dict | None = None) -> dict:
    """At the freeze: last observation per series (and those published after the 2026-10-13 vintage), per measure (and
    leg) its last observation, starting value and the reference E will use, the fitted coefficients, the dispersion
    moments, the benchmark years, the base rates, FRED's titles, and hashes of SPLITS.md, of the measure definitions
    (with their code) and of this file."""
    if _git("tag", "-l", TAG):
        raise SystemExit(f"refused: the tag {TAG} exists; the baseline is frozen")
    clean = lambda r: {x: r[x] for x in r if not x.startswith("_")}  # noqa: E731
    B, D, S = X["B"], X["D"], X["S"]
    bl = {"schema_version": SCHEMA_VERSION, "written_utc": _now(), "protocol_sha256": file_hash(PROTOCOL),
          "definitions_sha256": definitions_hash(), "code_sha256": file_hash(os.path.abspath(__file__)),
          "combined_benchmark": {"by_year": X["by_year"], "normal": X["normal"]},
          "base_rates": X["rates"],
          "fits": {k: B[k]["fit"] for k in ("hiring", "labour_share", "saving")},
          "dispersion_moments": D["_moments"],
          "dispersion_moments_sha256": _sha(json.dumps(D["_moments"], sort_keys=True)),
          "series": {sid: {"last_obs": str(data[sid].index[-1].date()), "downloaded_utc": vint.get(sid, {}).get("downloaded_utc"),
                           "sha256": vint.get(sid, {}).get("sha256"),
                           "fred_title": ((titles or {}).get(sid) or {}).get("title")} for sid in sorted(data) if sid in MANIFEST},
          "published_after_the_2026_10_13_vintage": sorted(sid for sid in data if sid in SEEN_BY_2026_10_13
                                                           and str(data[sid].index[-1].date()) > SEEN_BY_2026_10_13[sid]),
          "measures": {}}
    for sp in SPECS:
        key = sp["key"]
        if key == "payroll_dispersion":
            bl["measures"][key] = {"last_obs": str(D["share"].index[-1].date()), "start_value": float(D["share"].iloc[-1]),
                                   "normal_p95": D["normal_p95"], "normal_median": D["normal_median"]}
            continue
        m = S[key]
        g = m["gap"].dropna()
        bl["measures"][key] = {"last_obs": str(g.index[-1].date()), "start_value": float(g.iloc[-1]), "reference": clean(m["ref"]),
                               "legs": {lk: {"last_obs": str(lv["series"].dropna().index[-1].date()), "reference": clean(lv["ref"])}
                                        for lk, lv in m["legs"].items()}}
    os.makedirs(os.path.dirname(BASELINE), exist_ok=True)
    json.dump(bl, open(BASELINE, "w", encoding="utf-8"), indent=1)
    return bl


# ---------------------------------------------------------------------------------------------------------------------

def history_points(s: pd.Series, start="2000-01-01", every=1) -> dict:
    s = s.dropna()
    s = s[s.index >= start].iloc[::every]
    return {"dates": [str(t.date())[:7] for t in s.index], "values": [round(float(v), 3) for v in s.values]}


def evaluate(data: dict, st: dict, baseline: dict | None, looks: dict | None = None, today: dt.date | None = None) -> tuple:
    """Every reading from the data, the freeze state and the baseline: no fetching, no git, no files written (so the
    tagged code can be run on the same inputs). Returns the results and the internals the figure and the baseline use."""
    today = today or _today()
    frozen = bool(st["frozen"])
    bl = baseline if frozen else None
    rec = recession_months(data["USREC"])
    sahm = {pd.Timestamp(t) for t, v in data["SAHMREALTIME"].items() if v >= 0.5}
    B = build(data, (bl or {}).get("fits"))
    D = dispersion(data, rec, moments=(bl or {}).get("dispersion_moments"))
    fb_all = (bl or {}).get("measures", {})
    S = {key: measure_series(key, SPEC[key], B[key], rec, fb_all.get(key)) for key in SPEC if key != "payroll_dispersion"}
    p95 = fb_all["payroll_dispersion"]["normal_p95"] if "payroll_dispersion" in fb_all else D["normal_p95"]
    rr = data["REAINTRATREARAT10Y"].copy()
    rr.index = rr.index.to_period("M").to_timestamp()
    ctx = {"S": S, "D": D, "p95": p95, "rec": rec, "sahm": sahm, "anyrec": rec | sahm, "fed": fed_target(data), "rr": rr}
    fixed = dt.date.fromisoformat(st["tag_date"][:10]) if frozen and st.get("tag_date") else None

    readings, measures, jws = {}, [], {}
    for sp in SPECS:
        key = sp["key"]
        fb = fb_all.get(key)
        if key == "payroll_dispersion":
            t = D["share"].index[-1]
            r = reading_at(key, t, ctx)
            prev = t - pd.DateOffset(months=12)
            r.update({"date": str(t.date()), "change": float(D["share"][t] - D["share"][prev]), "E": None,
                      "level_vs_p95": float(D["share"][t] - p95), "share_12_months_earlier": float(D["share"][prev]),
                      "change_since_2019": float(D["share"][t] - D["share"][pd.Timestamp("2019-12-01")])})
            share, refm = D["share"], D["ref_mask"]
            refidx = [x for x in share.index if refm[x]]
            hit = [(share[x] >= p95, share[x + pd.DateOffset(months=12)] >= p95) for x in refidx
                   if (x + pd.DateOffset(months=12)) in share.index and refm.get(x + pd.DateOffset(months=12), False)]
            vis = [h for h in hit if h[0]]
            ps = (sum(h[1] for h in vis) / len(vis)) if vis else None
            br = {"n_pairs": len(hit), "n_visible": len(vis), "p_stays_clear_when_visible": ps, "p_continue_when_visible": ps,
                  "carryover_slope": None}
            r["carry_forward"] = {"E_if_the_last_window_repeats": None,
                                  "share_if_the_last_12_months_repeat": float(2 * share[t] - share[prev]),
                                  "p_same_zone_from_persistence": (ps if r["zone"] == "+" else None)}
            refd = {"normal_median": D["normal_median"], "normal_p95": p95, "normal_p90": D["normal_p90"],
                    "recession_median_pre2020": D["recession_median_pre2020"], "n_normal_months": D["n_normal_months"],
                    "from": D["normal_from"], "to": D["normal_to"], "own_history": False, "window_months": D["window_months"]}
            if fb:
                refd["current_vintage"] = {"normal_p95": D["normal_p95"]}
            gap_hist = D["share"]
        else:
            m = S[key]
            lr = latest_reading(key, sp, ctx)
            r, br = lr["reading"], lr["base_rates"]
            refd = {x: m["use"][x] for x in m["use"] if not x.startswith("_")}
            if fb:
                refd["current_vintage"] = {x: m["ref"][x] for x in m["ref"] if not x.startswith("_")}
            gap_hist = m["gap"]
        jw = judged_measure(key, sp, ctx, fb) if (frozen and fb) else None
        if frozen and fb:
            last_new = r["date"] > fb["last_obs"]
            status = ("judged" if jw else ("after the fixed date; first window not complete" if last_new else "no data since the fixed date"))
        else:
            status = st["label"]
        readings[key] = r
        jws[key] = jw
        extra = {}
        for x in ("fit", "fit_current_vintage", "level", "land_tn"):
            if x in B.get(key, {}):
                v = B[key][x]
                if isinstance(v, pd.Series):
                    vv = v.dropna()
                    extra[x] = {"date": str(vv.index[-1].date())[:7], "value": float(vv.iloc[-1])}
                else:
                    extra[x] = v
        if key == "saving":
            extra["alternatives"] = saving_alternatives(B, rec)
        if key == "labour_share":
            extra["raw_share"] = labour_share_raw_E(B, rec)
        label = (UNFROZEN_LABEL if not frozen else
                 ("latest 12 months, not judged" if sp["freq"] == "MS" else "latest 4 quarters, not judged"))
        measures.append({
            "id": sp["id"], "key": key, "name": sp["name"], "paper_call": sp["paper"], "rival_name": sp["rival_name"],
            "rival_call": sp["rival"], "fits_rule": sp["fits"], "series": sp["series"], "transformation": sp["gap"],
            "legs_defined": sp["legs"], "frequency": "monthly" if sp["freq"] == "MS" else "quarterly",
            "window": "12 months" if sp["freq"] == "MS" else "4 quarters",
            "direction_toward_paper": sp["direction"], "status": status, "in_count": key in COUNT_KEYS,
            "judged_in_recessions": key in KEEP_IN_RECESSION,
            "latest": {**{x: r[x] for x in r if x not in ("legs", "carry_forward")}, "reading": READING[r["counted_zone"]],
                       "label": label, "recession_in_window": r.get("recession_in_window", False)},
            "legs": r["legs"], "reference": refd, "base_rates": br, "carry_forward": r["carry_forward"], "judged_windows": jw,
            "thresholds_plain": thresholds_plain(key, S[key]["use"], sp) if key != "payroll_dispersion" else
            {"units": "% of the 2,047 cuts", "paper_if_level": f">= {p95:.2f}", "paper_at": p95},
            "extra": extra, "plain": plain_facts(key, data, B, r["date"]) if key != "payroll_dispersion" else
            {"share_pct": r["gap"], "normal_p95_pct": refd["normal_p95"], "normal_median_pct": refd["normal_median"],
             "recession_median_pct": refd["recession_median_pre2020"], "share_12m_earlier_pct": r["share_12_months_earlier"],
             "care_vs_rest_z": D["care_vs_rest"]["z"], "care_vs_rest_rank_of_2047": D["care_vs_rest"]["rank_of_2047_by_abs_z"],
             "normal_from": D["normal_from"], "window_months": D["window_months"]},
            "history": history_points(gap_hist, "2000-01-01", 1 if sp["freq"] == "QS" else 3)})

    # the benchmark years: each measure's window ending in the calendar month its judged windows end in
    month_of = {}
    for sp in SPECS:
        key = sp["key"]
        d0 = pd.Timestamp(fb_all[key]["last_obs"]) if key in fb_all else pd.Timestamp(readings[key]["date"])
        month_of[key] = d0.month
    by_year_current = history_table(ctx, month_of)
    by_year = (bl or {}).get("combined_benchmark", {}).get("by_year") or by_year_current
    hist_ids = [SPEC[k]["id"] for k in COUNT_KEYS]
    normal = benchmark_stats(by_year, hist_ids)
    normal_current = benchmark_stats(by_year_current, hist_ids)
    rec_today = any(readings[k].get("recession_in_window") for k in COUNT_KEYS)
    today_cr = combined_reading(readings, list(COUNT_KEYS), by_year, rec_today)
    cz_all = [readings[k]["counted_zone"] for k in SPEC]
    _c, tally_all, tc_all = tally_of(readings, list(SPEC))
    comb = {"count_definition": "measures moved the paper's way minus measures moved the other way (counted zones), over "
                                "the eleven measures with 1990-2019 history; measure 4 is reported beside the count",
            "today_all_12": int(sum(z == "+" for z in cz_all) - sum(z == "-" for z in cz_all)),
            "today_with_1990_2019_history": today_cr["count"],
            "measures_with_1990_2019_history": hist_ids,
            "beside_the_count": {"id": 4, "zone": readings["software_postings"]["counted_zone"],
                                 "fits": readings["software_postings"]["fits"]},
            "today": {**today_cr, "verdict_if_judged": today_cr["verdict"], "recession": rec_today,
                      "note": "the starting point: the rules applied to the latest windows; already seen, not judged"},
            "normal_years": {**normal, "share_at_or_above_today": float(np.mean([c >= today_cr["count"] for c in
                                                                                 [by_year[str(y)]["count"] for y in normal["years"]]]))
                             if normal["n"] else None,
                             "benchmark_months": {str(SPEC[k]["id"]): month_of[k] for k in SPEC},
                             "rule": "1990-2019 years in which all eleven counted measures exist and no window touches an "
                                     "NBER recession month or a real-time Sahm reading >= 0.5"},
            "normal_years_current_vintage": normal_current,
            "by_year": by_year_current,
            "historical_verdicts": historical_verdicts(by_year_current),
            "tally": tally_all, "tally_counts": tc_all}
    judged = combined_judged(jws, by_year, fixed, today, looks) if frozen else []

    pooled = [m["base_rates"] for m in measures if m["in_count"] and m["key"] != "payroll_dispersion" and m["base_rates"]["n_visible"]]
    nv = sum(b["n_visible"] for b in pooled)
    pooled_cont = sum(b["p_continue_when_visible"] * b["n_visible"] for b in pooled) / nv
    pooled_clear = sum(b["p_stays_clear_when_visible"] * b["n_visible"] for b in pooled) / nv
    meas_by = {m["key"]: m for m in measures}
    W = watch(data)
    rec_now = {"usrec_last": [str(data["USREC"].index[-1].date())[:7], float(data["USREC"].iloc[-1])],
               "sahm_realtime_last": [str(data["SAHMREALTIME"].index[-1].date())[:7], float(data["SAHMREALTIME"].iloc[-1])],
               "any_latest_window_touches_recession": any(m["latest"]["recession_in_window"] for m in measures)}
    res = {
        "schema_version": SCHEMA_VERSION, "generated_utc": _now(), "protocol": "paths/SPLITS.md",
        "definitions_sha256": definitions_hash(), "protocol_sha256": file_hash(PROTOCOL),
        "status": st, "recession": rec_now,
        "statistic": {"E": "(change over the latest 12 months or 4 quarters - mean of such changes over 1990-2019 windows with no "
                            "NBER recession month) / their sd, signed toward the paper's call",
                      "thresholds": {"paper": 1.0, "other": -1.0}, "reference_period": list(REF),
                      "short_history_rule": "fewer than 120 monthly (40 quarterly) reference windows: the longest available "
                                            "non-recession history to the window before the latest, flagged own_history"},
        "measures": measures,
        "dispersion_benchmark": {k: v for k, v in D.items() if not k.startswith("_") and k not in ("share", "ref_mask", "rec_mask")},
        "dispersion_recovery_effect": dispersion_recovery_effect(D),
        "dispersion_path": history_points(D["share"], "2019-01-01", 1),
        "combined": comb,
        "judged": judged,
        "base_rates": {"pooled_p_continue_when_visible": pooled_cont, "pooled_p_stays_clear_when_visible": pooled_clear,
                       "n_visible_windows": nv, "pooled_over": [m["id"] for m in measures if m["in_count"] and m["key"] != "payroll_dispersion"],
                       "panel_reference_2026_10_12": {"excess_continues": 0.64,
                                                      "note": "12 gaps, 8-quarter slope in its top quarter"},
                       "dispersion_p_stays_above_p95": meas_by["payroll_dispersion"]["base_rates"]["p_stays_clear_when_visible"],
                       "by_measure": {m["key"]: {"p_continue_when_visible": m["base_rates"]["p_continue_when_visible"],
                                                 "p_stays_clear_when_visible": m["base_rates"]["p_stays_clear_when_visible"],
                                                 "n_visible": m["base_rates"]["n_visible"],
                                                 "p_same_zone_from_persistence": m["carry_forward"].get("p_same_zone_from_persistence")}
                                      for m in measures}},
        "channels": CHANNELS,
        "watch": [{k: v for k, v in w.items() if not k.startswith("_")} for w in W],
        "context": context(data),
    }
    X = {"B": B, "D": D, "S": S, "W": W, "rec": rec, "by_year": by_year_current, "normal": normal_current,
         "rates": {"pooled": res["base_rates"], "by_measure": {m["key"]: m["base_rates"] for m in measures}}}
    return res, X


def compare_judged(a: dict, b: dict) -> list:
    """Where two runs' judged readings differ (E, zone, fits, counted zone per measure and window; verdicts)."""
    diffs = []
    ma, mb = {m["key"]: m for m in a["measures"]}, {m["key"]: m for m in b["measures"]}
    for k in ma:
        wa, wb = ma[k].get("judged_windows") or [], (mb.get(k) or {}).get("judged_windows") or []
        if len(wa) != len(wb):
            diffs.append(f"measure {ma[k]['id']}: {len(wa)} judged windows against {len(wb)}")
            continue
        for x, y in zip(wa, wb):
            for f in ("E_signed", "zone", "counted_zone", "fits", "void"):
                u, v = x.get(f), y.get(f)
                same = (abs(u - v) < 1e-9) if isinstance(u, float) and isinstance(v, float) else u == v
                if not same:
                    diffs.append(f"measure {ma[k]['id']} window ending {x.get('end')}: {f} {u!r} against {v!r}")
    for x, y in zip(a.get("judged", []), b.get("judged", [])):
        if x.get("verdict") != y.get("verdict") or x.get("count") != y.get("count"):
            diffs.append(f"window {x.get('window')}: verdict {x.get('verdict')!r} (count {x.get('count')}) against "
                         f"{y.get('verdict')!r} (count {y.get('count')})")
    return diffs


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true", help="re-download every manifest series (new vintage)")
    ap.add_argument("--write-baseline", action="store_true", help="write results/splits_baseline.json (at the freeze)")
    ap.add_argument("--look", action="store_true", help="the yearly look: write results/splits_look_<year>.json (needs --refresh)")
    args = ap.parse_args(argv)
    if args.write_baseline and _git("tag", "-l", TAG):
        raise SystemExit(f"refused: the tag {TAG} exists; the baseline is frozen (nothing written)")
    if args.look and not args.refresh:
        raise SystemExit("refused: the yearly look runs once, on a fresh vintage (--refresh --look)")
    REFRESH_FAILED.clear()
    vint = {k: v for k, v in _load_vintages().items() if k in MANIFEST}
    data = {sid: fetch(sid, args.refresh, vint) for sid in MANIFEST}
    titles = fred_titles(args.refresh)
    for sid in vint:
        if sid in titles:
            vint[sid]["fred_title"] = titles[sid]["title"]
    json.dump(vint, open(VINTAGES, "w", encoding="utf-8"), indent=1)
    if REFRESH_FAILED and (args.write_baseline or args.look):
        raise SystemExit(f"refused: the refresh failed for {REFRESH_FAILED}; the baseline and the look need a complete "
                         "fresh vintage (nothing written)")
    previous = _read_json(RESULTS)
    st, baseline = freeze_state(previous=previous)
    frozen = st["frozen"]
    today = _today()
    fixed = dt.date.fromisoformat(st["tag_date"][:10]) if frozen and st.get("tag_date") else None
    looks = read_looks(fixed, today) if frozen else {}
    res, X = evaluate(data, st, baseline, looks, today)
    if frozen and st["code_matches_baseline"] is False:
        try:
            T = tagged_code()
            if T is None:
                raise RuntimeError("the tagged code is not readable")
            res_t, _X = T.evaluate(data, st, baseline, looks, today)
            diffs = compare_judged(res_t, res)
            st["code_deviation"] = diffs
            if diffs:
                st["label"] += " (deviation: the working code judges differently; both are reported)"
                res["judged_working_code"] = res["judged"]
                res["judged"] = res_t["judged"]
                tj = {m["key"]: m.get("judged_windows") for m in res_t["measures"]}
                for m in res["measures"]:
                    m["judged_windows_working_code"] = m["judged_windows"]
                    m["judged_windows"] = tj.get(m["key"])
            else:
                st["label"] += " (the working code's changes leave every judged reading unchanged)"
        except Exception as e:  # noqa: BLE001
            st["code_deviation"] = [f"the tagged code could not be run: {e!r}"[:200]]
            st["label"] += " (deviation: the tagged code could not be run; the working code's readings are shown)"
        res["status"] = st
    res["refresh_failed"] = list(REFRESH_FAILED)
    res["vintages"] = {sid: vint[sid] for sid in sorted(MANIFEST) if sid in vint}
    os.makedirs(os.path.dirname(RESULTS), exist_ok=True)
    json.dump(res, open(RESULTS, "w", encoding="utf-8"), indent=1)
    if args.write_baseline:
        bl = write_baseline(X, vint, data, titles)
        print(f"baseline written: {BASELINE} (definitions {bl['definitions_sha256'][:12]}, protocol {str(bl['protocol_sha256'])[:12]}); "
              f"published after the 2026-10-13 vintage: {bl['published_after_the_2026_10_13_vintage'] or 'nothing'}")
    if args.look:
        write_look(res, today)
    figure(X["B"], X["D"], res["measures"], X["W"], rec_spans(X["rec"]), frozen)
    summary(res)
    return res


def write_look(res: dict, today: dt.date) -> dict:
    """The yearly look: the judged window whose look date has come, complete and not yet tagged, with its per-measure
    readings and the vintage it was judged on. The main session commits it with results/splits.json and
    cache/splits/*.csv and tags `paths-splits-look-<year>`; that verdict stands."""
    if not res["status"]["frozen"]:
        raise SystemExit("refused: the tracker is not fixed; there is nothing to look at")
    due = [j for j in res["judged"] if j.get("look_date") and dt.date.fromisoformat(j["look_date"]) <= today and "look" not in j]
    if not due:
        raise SystemExit("refused: no judged window is due for its look (or its look is already tagged)")
    j = due[0]
    if not j["complete"] or j["verdict"] in ("not all measures complete", "awaiting the yearly look"):
        raise SystemExit(f"refused: window {j['window']} is not complete (the look waits until every window is published)")
    year = dt.date.fromisoformat(j["look_date"]).year
    out = {"window": j["window"], "look_date": j["look_date"], "written_utc": _now(), "combined": j,
           "measures": {m["key"]: (m["judged_windows"] or [None] * j["window"])[j["window"] - 1] for m in res["measures"]},
           "status": res["status"], "vintages": res["vintages"]}
    fp = LOOK_FILE.format(year=year)
    json.dump(out, open(fp, "w", encoding="utf-8"), indent=1)
    print(f"look written: {fp}. Commit it with results/splits.json and cache/splits/*.csv, tag {LOOK_TAG.format(year=year)}, "
          "and push the tag the same day.")
    return out


def summary(res: dict):
    print(f"status: {res['status']['label']}")
    print(f"{'#':>2} {'measure':52s} {'date':10s} {'change':>8s} {'E':>6s}  reading / fits")
    for m in res["measures"]:
        la = m["latest"]
        e = "" if la["E_signed"] is None else f"{la['E_signed']:+.2f}"
        c = "" if la["change"] is None else f"{la['change']:+.2f}"
        print(f"{m['id']:>2} {m['name'][:52]:52s} {la['date']:10s} {c:>8s} {e:>6s}  {la['reading']} / {','.join(la['fits']) or 'neither'}"
              + ("  [own history]" if m["reference"].get("own_history") else "") + ("" if m["in_count"] else "  [beside the count]"))
    c = res["combined"]
    t = c["today"]
    print(f"count today {c['today_with_1990_2019_history']} (eleven), {c['today_all_12']} (all 12); benchmark years "
          f"{c['normal_years']['n']}: median {c['normal_years']['median']}, p90 {c['normal_years']['p90']}, range "
          f"{c['normal_years']['min']} to {c['normal_years']['max']}; tally {t['tally_counts']}; the rules would read "
          f"{t['verdict_if_judged']!r}" + (f" (rests on {t['rests_on_channel']})" if t["rests_on_channel"] else ""))
    hv = c["historical_verdicts"]
    print(f"the rules in the benchmark years: {hv['benchmark_years']}; retirement rule met in {hv['pairs_meeting_the_retirement_rule']} "
          f"of {hv['consecutive_pairs']} consecutive pairs")
    d = res["dispersion_benchmark"]
    print(f"dispersion ({d['window_months']} months): normal median {d['normal_median']:.1f}%, p95 {d['normal_p95']:.1f}%, "
          f"recessions {d['recession_median_pre2020']:.1f}%, latest {d['latest']}")
    if res.get("refresh_failed"):
        print(f"warning: refresh failed for {res['refresh_failed']}")


FIG_CALLS = {  # short labels for the figure only (the calls themselves are in SPECS and SPLITS.md)
    "care": "paper: pay down as care jobs rise | ageing: both up",
    "payroll_dispersion": "paper: stays above the 95th pct | cycle: falls back",
    "graduates": "paper: rises | ordinary slowdown: falls",
    "software_postings": "paper: keeps falling | unwind, expensing: recovers",
    "hiring": "paper: stays below | rates: closes after cuts",
    "output_per_hour": "paper: above usual range | immigration: usual",
    "labour_share": "paper: falls | cycle: moves with unemployment",
    "asset_income": "paper: dividends up | rates: only interest up",
    "transformer_premium": "paper: falls back by 2028 | scarcity: keeps rising",
    "site_rent": "paper: rises | rising real rates: falls",
    "build_out": "paper: widens | rates: narrows after cuts",
    "saving": "paper (later phase): rises | wealth effect: flat",
}
FIG_NAMES = {"labour_share": "Labour's share of corporate value added, adjusted"}
FIG_WATCH = {"big_vs_rest": ("Big stocks against the rest\n(Nasdaq-100, cap- over equal-weighted)", "log points"),
             "large_vs_small": ("Large against small caps\n(Nasdaq US indexes)", "log points"),
             "computer_imports": ("Computer imports, % of investment\nin information processing equipment", "%"),
             "electricity": ("Electricity prices against\nall consumer prices", "log points"),
             "consumption_share": ("Consumer spending,\n% of GDP", "%"),
             "se_property_income": ("Sweden: household property income\nnet of property income paid, % of GDP", "%")}


def figure(B, D, measures, W, spans, frozen=False):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=(16, 15), layout="constrained")
    fig.get_layout_engine().set(rect=(0, 0.02, 1, 0.98))
    gs = fig.add_gridspec(4, 12)
    axes = [fig.add_subplot(gs[i // 4, 3 * (i % 4):3 * (i % 4) + 3]) for i in range(12)]
    waxes = [fig.add_subplot(gs[3, 2 * j:2 * j + 2]) for j in range(6)]
    by = {m["key"]: m for m in measures}
    for a, sp in zip(axes, SPECS):
        key, m = sp["key"], by[sp["key"]]
        la = m["latest"]
        if key == "payroll_dispersion":
            s = D["share"]
            ref = m["reference"]
            a.plot(s.index, s.values, color="C0", lw=1)
            a.axhline(ref["normal_p95"], color="C3", lw=0.9, ls="--")
            a.axhline(D["normal_median"], color="grey", lw=0.8, ls=":")
            a.set_ylabel(f"% of cuts beyond 2 sd ({D['window_months']} months)", fontsize=8)
            where = ("above the normal 95th percentile" if la["zone"] == "+" else
                     "fell below the normal 95th percentile" if la["zone"] == "-" else "below the normal 95th percentile")
            txt = (f"{la['gap']:.1f}% ({la['date'][:7]}): {where}\n"
                   f"dashed: normal months' 95th pct ({ref['normal_p95']:.1f}%, {ref['from'][:4]}-{ref['to'][:4]}); dotted: median")
        else:
            ch = (B[key]["gap"] - B[key]["gap"].shift(sp["k"])).dropna()
            ref = m["reference"]
            ch = ch[ch.index >= "1990-01-01"]
            a.plot(ch.index, ch.values, color="C0", lw=1)
            a.axhspan(ref["mean"] - ref["sd"], ref["mean"] + ref["sd"], color="grey", alpha=0.2, lw=0)
            a.axhline(ref["mean"], color="grey", lw=0.8)
            lo = min(np.nanquantile(ch.values, 0.01), ref["mean"] - 1.5 * ref["sd"], ch.iloc[-1])
            hi = max(np.nanquantile(ch.values, 0.99), ref["mean"] + 1.5 * ref["sd"], ch.iloc[-1])
            pad = 0.08 * (hi - lo)
            a.set_ylim(lo - pad, hi + pad)
            arrow = "↑" if sp["direction"] > 0 else "↓"
            a.set_ylabel(("12-month" if sp["freq"] == "MS" else "4-quarter") + f" change (paper's way {arrow})", fontsize=8)
            band = (f"own history {ref['from'][:4]}-{ref['to'][:4]}" if ref.get("own_history") else
                    f"{ref['from'][:4]}-{ref['to'][:4]}")
            txt = f"E = {la['E_signed']:+.1f} ({la['date'][:7]}): {la['reading']}\nshaded: usual range ({band}, mean ± 1 sd)"
        for s0, e0 in spans:
            a.axvspan(s0, e0, color="C1", alpha=0.15, lw=0)
        a.set_title(f"{sp['id']}. {FIG_NAMES.get(key, sp['name'])}\n{FIG_CALLS[key]}", fontsize=8.6)
        a.text(0.02, 0.97, txt, transform=a.transAxes, ha="left", va="top", fontsize=7.2,
               bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="0.7", alpha=0.9))
        a.tick_params(labelsize=7.5)
    for a, w in zip(waxes, W):
        s = w["_series"]
        s = s[s.index >= "2005-01-01"]
        a.plot(s.index, s.values, color="C2", lw=1)
        t, u = FIG_WATCH[w["key"]]
        a.set_title(t, fontsize=8)
        a.set_ylabel(u, fontsize=7.5)
        a.tick_params(labelsize=7)
        a.xaxis.set_major_locator(mdates.YearLocator(5))
        a.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    fig.suptitle("The splits tracker: twelve judged measures, each as its change over the window against its usual range "
                 "(NBER recessions shaded); bottom row, the watch list (reported, never judged)", fontsize=11)
    fig.text(0.01, 0.004, "FRED: BLS, BEA, Federal Reserve, Cleveland Fed, Indeed, Nasdaq, NBER; Statistics Sweden NR0103 (household "
             "sector accounts). E is signed toward the paper's call. Axes clipped at the 1st and 99th percentiles (2020). "
             + ("Panels show the latest rolling window (not judged); judged windows start at the fixed date (results/splits.json)."
                if frozen else "Every reading is a starting point, already seen and not judged, until the tracker is fixed."),
             fontsize=7.5)
    os.makedirs(os.path.dirname(FIGURE), exist_ok=True)
    fig.savefig(FIGURE, dpi=110)
    plt.close(fig)


def rec_spans(rec: set) -> list:
    """NBER recession months (USREC) as (start, end) spans for shading."""
    ms = sorted(m for m in rec if m >= pd.Timestamp("1990-01-01"))
    spans = []
    for m in ms:
        if spans and m == spans[-1][1] + pd.DateOffset(months=1):
            spans[-1][1] = m
        else:
            spans.append([m, m])
    return [(a, b + pd.DateOffset(months=1)) for a, b in spans]


if __name__ == "__main__":
    main()
