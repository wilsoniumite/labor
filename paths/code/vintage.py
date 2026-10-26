# vintage.py — the start, as a dated vintage: the series the crash model's start (index 0, decision 43) is measured on,
# frozen in cache/start/ with a manifest of where each came from, its last observation and its hash. Next 11 as amended
# 2026-10-26: a vintage is frozen and committed before the prints it is scored on, and a print is not folded into a run
# that makes a claim about it. The fit's history (1929-33, 2000-03, 2007-10) stays in cache/ and is not refreshed here.
#
# Sources, in order of preference for each series: FRED itself; the watcher's copy of FRED (the private watch repository's
# state branch, fetched on its server every 15 minutes: market/<id>.json); FRED as cached on 30 Sep 2026 (cache/october,
# after BEA's annual update of 25 Sep); the publisher's own file where FRED republishes it. Non-FRED: euro-area
# unemployment (ECB LFSI, 15-74, seasonally adjusted), Swedish unemployment (Statistics Sweden's labour force survey,
# seasonally adjusted, as the watcher copies it: SEUNRATE) and the Riksbank's policy rate (its SWEA series SECBREPOEFF,
# as the watcher copies it). The manifest names the source of every file.
#
# Run from paths/:  ../venv/Scripts/python.exe code/vintage.py [--refresh]
# Out: cache/start/*.csv, cache/start/MANIFEST.json

from __future__ import annotations

import datetime as dt
import hashlib
import io
import json
import os
import subprocess
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
START = os.path.join(ROOT, "cache", "start")
OCT = os.path.join(ROOT, "cache", "october")
WATCH = os.path.join(os.path.dirname(os.path.dirname(ROOT)), "watch")
UA = {"User-Agent": "laborformal-paths (public-data research)"}
FRED_CSV = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={sid}"
FROM = "2023-01-01"        # enough for a year-on-year change and a three-month rise at the start

# id: what it is for (the start value it measures)
SERIES = {
    "UNRATE": "US u0 (BLS via FRED)",
    "DFF": "US i0, the effective funds rate",
    "PCEPILFE": "US pi0, core PCE prices (y/y)",
    "PCEPI": "US headline PCE prices (y/y), for the energy term",
    "GDP": "US nominal GDP, for equity wealth over GDP",
    "BOGZ1LM153064475Q": "US household corporate equities, directly and indirectly held (Fed Z.1), for equity_wealth",
    "BAMLC0A0CM": "US investment-grade OAS, its 63-print rise: the spread already present at the start (decision 47)",
    "ECBDFR": "euro-area i0, the ECB deposit rate",
    "00XEFDEZ19M086NEST": "euro-area pi0, HICP excluding energy, food, alcohol and tobacco (y/y)",
    "CP0000EZ19M086NEST": "euro-area headline HICP (y/y)",
    "00XEFDSEM086NEST": "Sweden pi0, HICP excluding energy, food, alcohol and tobacco (y/y)",
    "DCOILBRENTEU": "dated Brent, for decision 27's price leg",
    "NASDAQCOM": "the Nasdaq composite, for the pop so far and the watcher's equity rule",
    "DGS10": "the US ten-year Treasury yield, for the premium's test: its move since the start (decision 69)",
    "THREEFYTP10": "the US ten-year term premium (Kim-Wright, the Fed Board), likewise",
    "BAA10Y": "Moody's Baa over the ten-year, likewise",
}
# the AI build-out (decoupling.build_out) and nominal GDP from BEA's own bulk NIPA file, as FRED republishes them (FRED id:
# BEA code; millions in the file, billions here); from 2014 for the 2015-22 trend
BEA_URL = "https://apps.bea.gov/national/Release/TXT/NipaDataQ.txt"
BEA = {"Y034RC1Q027SBEA": "Y034RC", "B985RC1Q027SBEA": "B985RC", "W003RC1Q027SBEA": "W003RC", "B852RC1Q027SBEA": "B852RC",
       "GDP": "A191RC"}
BEA_FROM = "2014-01-01"
NON_FRED = {
    "EA_UNEMPLOYMENT": ("euro-area u0, ECB LFSI M.I9.S.UNEHRT.TOTAL0.15_74.T", "ecb_LFSI_M.I9.S.UNEHRT.TOTAL0.15_74.T.csv"),
    "SEUNRATE": ("Sweden u0, Statistics Sweden's labour force survey, 15-74, seasonally adjusted", None),
    "SECBREPOEFF": ("Sweden i0, the Riksbank's policy rate (SWEA)", None),
    "FRGVB10Y": ("France's ten-year government bond yield (the Riksbank's SWEA), for France's spread over Germany", None),
    "DEGVB10Y": ("Germany's ten-year government bond yield (the Riksbank's SWEA), likewise", None),
}


def _fred_live(sid: str) -> str | None:
    try:
        import requests
        import truststore
        truststore.inject_into_ssl()
        r = requests.get(FRED_CSV.format(sid=sid), headers=UA, timeout=20)
        if r.status_code == 200 and "observation_date" in r.text[:100]:
            return r.text
    except Exception:  # noqa: BLE001 — any failure falls through to the next source, which the manifest names
        return None
    return None


def _watcher(sid: str) -> pd.Series | None:
    try:
        out = subprocess.run(["git", "-C", WATCH, "show", f"origin/claude/state:market/{sid}.json"], capture_output=True,
                             text=True, encoding="utf-8")
    except OSError:
        return None
    if out.returncode != 0 or not out.stdout:
        return None
    d = json.loads(out.stdout)
    s = pd.Series({pd.Timestamp(k): float(v) for k, v in d.items() if v is not None}).sort_index()
    return s if len(s) else None


def _watcher_commit() -> str | None:
    out = subprocess.run(["git", "-C", WATCH, "log", "-1", "--format=%h %cI", "origin/claude/state"], capture_output=True,
                         text=True, encoding="utf-8")
    return out.stdout.strip() or None if out.returncode == 0 else None


def _bea() -> tuple[dict, str]:
    """BEA's quarterly NIPA bulk file: the BEA series, as FRED-dated quarterly series in billions, and its Last-Modified."""
    import tempfile
    import requests
    import truststore
    truststore.inject_into_ssl()
    want = set(BEA.values())
    rows = {c: {} for c in want}
    with tempfile.TemporaryFile() as f:
        r = requests.get(BEA_URL, headers=UA, timeout=120, stream=True)
        r.raise_for_status()
        modified = r.headers.get("Last-Modified", "")
        for chunk in r.iter_content(1 << 20):
            f.write(chunk)
        f.seek(0)
        for line in io.TextIOWrapper(f, encoding="utf-8"):
            code, _, rest = line.partition(",")
            if code in want:
                period, _, value = rest.strip().partition(",")
                q = pd.Period(period, "Q")
                rows[code][q.start_time] = float(value.strip('"').replace(",", "")) / 1000
    return {sid: pd.Series(rows[c]).sort_index() for sid, c in BEA.items()}, modified


def _csv(s: pd.Series, sid: str, start: str = FROM) -> str:
    s = s[s.index >= pd.Timestamp(start)]
    return "observation_date," + sid + "\n" + "".join(f"{t:%Y-%m-%d},{v:.10g}\n" for t, v in s.items())


def _read_fred_text(txt: str, sid: str) -> pd.Series:
    df = pd.read_csv(io.StringIO(txt))
    return pd.Series(pd.to_numeric(df[sid], errors="coerce").values, index=pd.to_datetime(df["observation_date"])).dropna()


# HICP from Eurostat itself (prc_hicp_minr, 2025 = 100, the dataset FRED's copies follow), used whole for a series when
# it reaches further than every FRED source: FRED's id -> (coicop18, geo)
EUROSTAT = {"00XEFDEZ19M086NEST": ("TOT_X_NRG_FOOD", "EA19"), "CP0000EZ19M086NEST": ("TOTAL", "EA19"),
            "00XEFDSEM086NEST": ("TOT_X_NRG_FOOD", "SE")}
EUROSTAT_URL = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/prc_hicp_minr"


def _eurostat(coicop: str, geo: str) -> pd.Series | None:
    try:
        import requests
        import truststore
        truststore.inject_into_ssl()
        r = requests.get(EUROSTAT_URL, params={"geo": geo, "coicop18": coicop, "unit": "I25", "sinceTimePeriod": "2022-01"},
                         headers=UA, timeout=60)
        if r.status_code != 200:
            return None
        js = r.json()
        ids, size = js["id"], js["size"]
        cats = {d: {v: k for k, v in js["dimension"][d]["category"]["index"].items()} for d in ids}
        strides = [int(np.prod(size[i + 1:])) for i in range(len(ids))]
        out = {}
        for k, v in js["value"].items():
            key = {d: cats[d][(int(k) // strides[i]) % size[i]] for i, d in enumerate(ids)}
            out[pd.Timestamp(key["time"] + "-01")] = float(v)
        return pd.Series(out).sort_index() if out else None
    except Exception:  # noqa: BLE001
        return None


def refresh(live: bool = True) -> dict:
    """Build the vintage from the best source reachable for each series, in a folder beside cache/start/, and put it in
    place only once every series and the manifest are written (a failed refresh leaves the frozen vintage as it was).
    Fails if a series has no source at all."""
    import shutil
    import tempfile
    tmp = tempfile.mkdtemp(prefix="start-", dir=os.path.dirname(START))
    wc = _watcher_commit()
    man = {"vintage": dt.date.today().isoformat(), "built_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
           "watcher_state_commit": wc, "series": {}}

    def put(sid, s, src, what, start=FROM):
        body = _csv(s, sid, start)
        open(os.path.join(tmp, f"{sid}.csv"), "w", encoding="utf-8", newline="\n").write(body)
        man["series"][sid] = {"for": what, "source": src, "last": f"{s.index[-1]:%Y-%m-%d}", "value": float(s.iloc[-1]),
                              "sha256": hashlib.sha256(body.encode()).hexdigest()}
    try:
        for sid, what in SERIES.items():
            txt = _fred_live(sid) if live else None
            if txt is not None:
                s, src = _read_fred_text(txt, sid), "FRED"
            else:
                s = _watcher(sid)
                src = f"FRED via the watcher's copy (state {wc})" if s is not None else None
                for folder, what_ in ((OCT, "FRED as cached on 30 Sep 2026 (cache/october)"),
                                      (os.path.join(ROOT, "cache"), "FRED as cached in cache/")):
                    fp = os.path.join(folder, f"{sid}.csv")
                    if os.path.exists(fp):
                        o = _read_fred_text(open(fp, encoding="utf-8").read(), sid)
                        if s is None or o.index[-1] > s.index[-1]:
                            s, src = o, what_
            if sid in EUROSTAT and live:
                e = _eurostat(*EUROSTAT[sid])
                if e is not None and (s is None or e.index[-1] > s.index[-1]):
                    s, src = e, f"Eurostat, prc_hicp_minr ({EUROSTAT[sid][1]}, {EUROSTAT[sid][0]}, 2025 = 100)"
            if s is None:
                raise SystemExit(f"{sid}: no source reachable")
            put(sid, s, src, what)
        # BEA: the build-out and nominal GDP (GDP replaces any FRED copy above: one source for the build-out's shares)
        bea, modified = _bea()
        for sid, s in bea.items():
            put(sid, s, f"BEA, NipaDataQ.txt ({BEA[sid]}; Last-Modified {modified})",
                "the AI build-out (decoupling.build_out)" if sid != "GDP" else SERIES["GDP"], BEA_FROM)
        # non-FRED
        for key, (what, oct_file) in NON_FRED.items():
            s, src = (_watcher(key), None) if oct_file is None else (None, None)
            if s is not None:
                src = f"{'Statistics Sweden' if key == 'SEUNRATE' else 'the Riksbank (SWEA)'} via the watcher's copy (state {wc})"
            if oct_file is not None:
                s = _ecb_lfsi(live)
                src = "ECB Data Portal" if s is not None else None
                if s is None:
                    d = pd.read_csv(os.path.join(OCT, oct_file))
                    s = pd.Series(pd.to_numeric(d.iloc[:, 1], errors="coerce").values, index=pd.to_datetime(d.iloc[:, 0])).dropna()
                    src = "ECB Data Portal as cached on 30 Sep 2026 (cache/october)"
            if s is None:
                raise SystemExit(f"{key}: no source reachable")
            put(key, s, src, what)
        json.dump(man, open(os.path.join(tmp, "MANIFEST.json"), "w", encoding="utf-8"), indent=1)
    except BaseException:
        shutil.rmtree(tmp, ignore_errors=True)
        raise
    if os.path.exists(START):
        shutil.rmtree(START)
    os.replace(tmp, START)
    return man


def _ecb_lfsi(live: bool) -> pd.Series | None:
    if not live:
        return None
    try:
        import requests
        import truststore
        truststore.inject_into_ssl()
        url = "https://data-api.ecb.europa.eu/service/data/LFSI/M.I9.S.UNEHRT.TOTAL0.15_74.T?format=csvdata"
        r = requests.get(url, headers=UA, timeout=30)
        if r.status_code != 200:
            return None
        d = pd.read_csv(io.StringIO(r.text))
        return pd.Series(pd.to_numeric(d["OBS_VALUE"], errors="coerce").values,
                         index=pd.to_datetime(d["TIME_PERIOD"])).dropna().sort_index()
    except Exception:  # noqa: BLE001
        return None


FRB_CHARGEOFF = "https://www.federalreserve.gov/releases/chargeoff/chgallsa.htm"


def history() -> dict:
    """The two history series the measured 2000-02 bust shapes need (case.shapes) that the history cache lacked, written
    once into cache/ in FRED's own format, from the publishers FRED republishes: information processing equipment
    (BEA Y034RC, as FRED's Y034RC1Q027SBEA, billions) and the C&I loan charge-off rate (the Fed Board's charge-off
    release, all banks, seasonally adjusted, as FRED's CORBLACBS). Existing files are left alone."""
    import re
    import requests
    import truststore
    truststore.inject_into_ssl()
    out, cache = {}, os.path.join(ROOT, "cache")
    fp = os.path.join(cache, "Y034RC1Q027SBEA.csv")
    if not os.path.exists(fp):
        bea, modified = _bea()
        open(fp, "w", encoding="utf-8", newline="\n").write(_csv(bea["Y034RC1Q027SBEA"], "Y034RC1Q027SBEA", "1900-01-01"))
        out["Y034RC1Q027SBEA"] = f"BEA NipaDataQ.txt Y034RC (Last-Modified {modified})"
    fp = os.path.join(cache, "CORBLACBS.csv")
    if not os.path.exists(fp):
        t = requests.get(FRB_CHARGEOFF, headers=UA, timeout=60).text
        rows = {}
        for m in re.finditer(r'<th id="date\d+">(\d{4}):(\d)</th>(.*?)</tr>', t, re.S):
            cells = dict((h.split()[-2], v) for h, v in re.findall(r'headers="([^"]*)">([^<&]*)', m.group(3)))
            if cells.get("CI", "").strip() not in ("", "n.a."):
                rows[pd.Period(f"{m.group(1)}Q{m.group(2)}", "Q").start_time] = float(cells["CI"])
        s = pd.Series(rows).sort_index()
        open(fp, "w", encoding="utf-8", newline="\n").write(_csv(s, "CORBLACBS", "1900-01-01"))
        out["CORBLACBS"] = f"Federal Reserve Board, charge-off rates, all banks, SA ({FRB_CHARGEOFF}), column C&I"
    if out:
        hp = os.path.join(cache, "HISTORY_SOURCES.json")
        rec = json.load(open(hp, encoding="utf-8")) if os.path.exists(hp) else {}
        for sid, src in out.items():
            body = open(os.path.join(cache, f"{sid}.csv"), encoding="utf-8").read()
            rec[sid] = {"source": src, "written": dt.date.today().isoformat(), "sha256": hashlib.sha256(body.encode()).hexdigest(),
                        "note": "in FRED's format and under FRED's id, from the publisher FRED republishes (FRED was unreachable)"}
        json.dump(rec, open(hp, "w", encoding="utf-8"), indent=1)
    return out


def read(sid: str) -> pd.Series:
    """A series of the frozen vintage (cache/start/<sid>.csv); never fetches."""
    fp = os.path.join(START, f"{sid}.csv")
    if not os.path.exists(fp):
        raise SystemExit(f"{sid}: not in the vintage (cache/start/); run code/vintage.py --refresh")
    return _read_fred_text(open(fp, encoding="utf-8").read(), sid)


def manifest() -> dict:
    return json.load(open(os.path.join(START, "MANIFEST.json"), encoding="utf-8"))


def yoy(s: pd.Series) -> float:
    """The latest year-on-year change, %, on the same month a year before."""
    last = s.index[-1]
    return float((s.iloc[-1] / s[last - pd.DateOffset(years=1)] - 1) * 100)


def rise(s: pd.Series, prints: int = 63) -> float:
    """The change over the last `prints` observations (the watcher's three-month window for daily series)."""
    return float(s.iloc[-1] - s.iloc[-1 - prints])


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if "--history" in sys.argv:
        print(json.dumps(history(), indent=1))
    if "--refresh" in sys.argv:
        m = refresh()
        for k, v in m["series"].items():
            print(f"{k:22s} {v['last']} {v['value']:>12.4f}  {v['source']}")
    else:
        print(json.dumps(manifest(), indent=1))
