# check_guard.py — the long-run doors (code/fetch.py, code/ipums.py) and the split (code/split.py, data/split.json).
#   (a) in the repository's real git state (no participation-L-freeze tag yet) every value door refuses before any
#       network call or cache read, and nothing is logged; a planted cache file is not served;
#   (b) the meta door serves OECD structure and availability endpoints only (never /data/; a data message is refused
#       and logged as rejected); the doc door serves its allowlist only;
#   (c) the design door returns the 1960 WPP totals of the requested members and nothing else; aggregates and
#       non-members are refused;
#   (d) with the tags simulated (fetch._git monkeypatched): explore serves the frozen explore countries only; confirm
#       needs both tags in order, the frozen split, a clean tree bar this process's own log lines, longrun/code
#       unchanged since the LE tag and participation/code unchanged since the European E tag; aggregates refused;
#       both halves refuse a premature L tag (no production skeleton, unfilled forecast sheets, no European run, the
#       scouts' move unrecorded) and a working copy whose frozen inputs (segments.csv, coverage.json, skeleton.json,
#       split.json, ipums_samples.json, PROTOCOL.md) differ from the L tag, or whose FORECASTS.md changed other than
#       by added E-L rows;
#   (e) L14's order: outcome doors refuse until the half has a logged q download, then a knots record by the opening
#       covering the requested countries, then an F_L record by the IPUMS loader; stray records open nothing; the
#       look keeps the FIRST explore knots record, and a half's knots are recorded once;
#   (f) L1: European members' OECD queries end at 1994 (q flows 1993); a response with later years, or with areas not
#       requested, is refused and never cached;
#   (g) single-file loaders (JST, ILOSTAT, WPP by age) return only the allowed countries' rows, cut at L1, and only
#       the named columns, from a file that holds every country;
#   (h) the IPUMS loader refuses a closed half and any column outside the whitelist (labour, education, income,
#       marital status, tenure), and reads only the purpose's samples of open countries; it refuses while microdata
#       lies outside data/ipums/, an extract whose DDI lists a sample outside the frozen list, a row aged outside 20-34,
#       and a CSV without its DDI; it reads Extract A and B as one or two extracts; a grouped-age sample with no L2
#       record of its intervals is unusable alone (the others still compute);
#   (i) the log line comes before the cache file; a cache file without its log record is refused;
#   (j) participation/code has the SHA-256 it had at participation-E-freeze (imported unedited);
#   (k) no long-run script (code/ and checks/, this check excepted) but fetch.py and ipums.py names the long-run raw
#       or ipums data folders;
#   (l) data/split.json: reproduced by split.assign from its recorded populations; seed formula; US in explore and its
#       pair partner in confirm; halves differ by at most one; each pair split; strata as section 4.
#   (m) L1's European cut lies before the European panel grid's first year and before every year of the European
#       exploration's committed outputs; the skeleton drops every European raw row at or before the cut at parse; the
#       European real-data run (europe_run) gets knots for the European countries.
# The network is blocked for the whole run.
#
# Run from longrun/:  ../../venv/Scripts/python.exe checks/check_guard.py      Exit status 0 only if all pass.

from __future__ import annotations

import glob
import gzip
import hashlib
import io
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import tempfile

import numpy as np
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
LROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(LROOT, "code"))
import fetch  # noqa: E402
import ipums  # noqa: E402
import opening  # noqa: E402
import split as sp  # noqa: E402
import requests  # noqa: E402

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


NET = []


def _blocked(*a, **k):
    NET.append(1)
    raise RuntimeError("network call attempted")


requests.adapters.HTTPAdapter.send = _blocked
socket.create_connection = _blocked
socket.socket.connect = _blocked


def attempt(fn):
    n0 = len(NET)
    try:
        fn()
        return None, "", len(NET) - n0
    except Exception as e:  # noqa: BLE001
        return type(e), str(e), len(NET) - n0


def refused(fn, exc=fetch.BlindingError):
    t, msg, n = attempt(fn)
    return t is exc and n == 0, f"{t.__name__ if t else 'no error'}: {msg[:120]}; network {n}"


REAL = {k: getattr(fetch, k) for k in ("_git", "LOG", "RAW", "IPUMS_DIR", "SPLIT", "_download", "FORECASTS_PATH")}
TMP = tempfile.mkdtemp(prefix="lr_check_guard_")
LOG_BEFORE = open(fetch.LOG, "rb").read() if os.path.exists(fetch.LOG) else b""


def sandbox():
    d = tempfile.mkdtemp(dir=TMP)
    fetch.RAW, fetch.LOG = os.path.join(d, "raw"), os.path.join(d, "fetch_log.jsonl")
    fetch.IPUMS_DIR = os.path.join(d, "ipums")
    return d


def restore():
    for k, v in REAL.items():
        setattr(fetch, k, v)
    fetch._APPENDED.clear()
    fetch._READY.clear()


def has_tag(tag):
    return subprocess.run(["git", "rev-parse", "-q", "--verify", f"refs/tags/{tag}"], cwd=LROOT,
                          capture_output=True).returncode == 0


SPLIT = json.load(open(os.path.join(LROOT, "data", "split.json"), encoding="utf-8"))
EX, CF = SPLIT["explore"], SPLIT["confirm"]
LFS_KEY = {"MEASURE": "LF_RATE", "UNIT_MEASURE": "PT_POP_SUB", "SEX": ["F", "M"], "AGE": "Y25T29",
           "LABOUR_FORCE_STATUS": "LF"}

# ---------------------------------------------------------------- (a) real state
print("(a) the real git state")
sandbox()
l_tag = has_tag(fetch.L_FREEZE)
check("A0 no participation-L-freeze tag exists yet (the long run is unfrozen)", not l_tag)
doors = {
    "oecd LFS": lambda: fetch.oecd("oecd_lfs", LFS_KEY, EX[:2], "explore"),
    "oecd RPI": lambda: fetch.oecd("oecd_rpi", {"FREQ": "A", "MEASURE": "RPI", "UNIT_MEASURE": "IX"}, EX[:2], "explore"),
    "jst": lambda: fetch.jst(["US"], "explore"),
    "ilostat": lambda: fetch.ilostat(["US"], "explore"),
    "wpp_age": lambda: fetch.wpp_age(["US"], "explore"),
    "giuliano_nunn": lambda: fetch.giuliano_nunn(["US"], "explore"),
    "kholodilin": lambda: fetch.kholodilin(["US"], "explore"),
    "dbnomics": lambda: fetch.dbnomics("BLS/ln/LNU01300164", "explore"),
    "census_us": lambda: fetch.census_us("ad1", "explore"),
    "ipums F_L": lambda: ipums.F_L("explore"),
    "confirm oecd": lambda: fetch.oecd("oecd_lfs", LFS_KEY, CF[:2], "confirm"),
}
res = {k: refused(f) for k, f in doors.items()}
check("A1 every value door refuses explore and confirm reads before the L-freeze, with no network call: "
      + ", ".join(res), all(ok for ok, _ in res.values()), "; ".join(f"{k}: {d}" for k, (ok, d) in res.items() if not ok))
os.makedirs(os.path.join(fetch.RAW, "explore"), exist_ok=True)
q = {"source": "oecd_lfs", "key": "x", "end": 2025}
open(fetch._cache_path("explore", "oecd_lfs", q, ".csv"), "w").write("REF_AREA,TIME_PERIOD,OBS_VALUE\nUSA,1970,1\n")
ok, d = refused(lambda: fetch.oecd("oecd_lfs", LFS_KEY, ["US"], "explore"))
check("A2 a planted cache file is not served: the guard runs first", ok, d)
check("A3 nothing was logged by the refused reads", not os.path.exists(fetch.LOG))
restore()

# ---------------------------------------------------------------- (b) meta and doc
print("(b) the meta and doc doors")
sandbox()
bad_urls = ["https://sdmx.oecd.org/public/rest/data/OECD.ELS.SAE,DSD_LFS@DF_LFS_INDIC,1.1/USA..../",
            "https://example.org/availableconstraint/x", "https://sdmx.oecd.org/public/rest/availableconstraint/a/"
            "data/b", "http://sdmx.oecd.org/public/rest/dataflow/OECD.ELS.SAE/DSD_LFS@DF_LFS_INDIC/1.1"]
res = [refused(lambda u=u: fetch.meta(u)) for u in bad_urls]
check("B1 the meta door refuses data endpoints, other hosts and plain http", all(ok for ok, _ in res),
      "; ".join(d for ok, d in res if not ok))
fetch._download = lambda url, headers=None, timeout=300: json.dumps(
    {"data": {"dataSets": [{"observations": {"0": [1.0]}}]}}).encode()
t, msg, n = attempt(lambda: fetch.meta("https://sdmx.oecd.org/public/rest/availableconstraint/OECD.X,Y,1.0/.A/all/"
                                       "REF_AREA?mode=exact"))
logged = [json.loads(ln) for ln in open(fetch.LOG)] if os.path.exists(fetch.LOG) else []
meta_dir = os.path.join(fetch.RAW, "meta")
check("B2 a metadata request that returns a data message is refused, logged as rejected and not cached",
      t is fetch.BlindingError and bool(logged) and "rejected" in logged[-1]
      and (not os.path.exists(meta_dir) or not os.listdir(meta_dir)), f"{t.__name__ if t else None}: {msg[:80]}")
check("B3 the doc door refuses ids outside its allowlist", refused(lambda: fetch.doc("anything"))[0])
fetch._download = REAL["_download"]
restore()

# ---------------------------------------------------------------- (c) design
print("(c) the design half")
sandbox()
rows = []
for iso in ["USA", "GBR", "DEU", "BRA", "OWID_WRL"]:
    for t in (1950, 1960, 1961):
        rows.append(dict(ISO3_code=iso, Time=t, Variant="Medium", PopTotal=1000.0 + t))
        rows.append(dict(ISO3_code=iso, Time=t, Variant="High", PopTotal=9.0))
buf = io.BytesIO()
with gzip.GzipFile(fileobj=buf, mode="wb") as g:
    g.write(pd.DataFrame(rows).to_csv(index=False).encode())
fetch._download = lambda url, headers=None, timeout=300: buf.getvalue()
pop = fetch.population_1960(["US", "UK", "DE"])
check("C1 population_1960 returns the 1960 Medium totals (persons) of the requested members only",
      pop == {"US": 2960000.0, "UK": 2960000.0, "DE": 2960000.0}, str(pop))
res = [refused(lambda c=c: fetch.population_1960([c])) for c in ("BR", "OECD", "EU27")]
check("C2 non-members and aggregates are refused by the design door", all(ok for ok, _ in res))
fetch._download = REAL["_download"]
restore()

# ---------------------------------------------------------------- (d) simulated tags


FILLED = ("## Stella\n| Test | Model's sign | Expected sign | P(model's sign) | P(supported) | P(contradicted) | Note |\n"
          "|---|---|---|---|---|---|---|\n| LR-K2: x | < 0 | - | 0.5 | 0.3 | 0.1 | |\n| LR-Y0: x | > 0 | + | 0.6 | 0.2 | 0.1 |"
          " |\n| C-6L: x | > 0 | + | 0.7 | 0.4 | 0.0 | |\n| LR-C1: x | > 0 | | | | | dropped |\n\n## Claude\n"
          "| Test | a | b | c | d | e | f |\n|---|---|---|---|---|---|---|\n| LR-K2: x | < 0 | - | 0.5 | 0.3 | 0.1 | |\n"
          "| LR-Y0: x | > 0 | + | 0.6 | 0.2 | 0.1 | |\n| C-6L: x | > 0 | + | 0.7 | 0.4 | 0.0 | |\n"
          "| LR-C1: x | > 0 | + | 0.5 | 0.1 | 0.1 | |\n\n## E-L (added before the LE tag)\n\n"
          "| Participant | E-L | Predicted sign | Expected sign | P(predicted sign) | P(supported) | P(contradicted) | Note |\n"
          "|---|---|---|---|---|---|---|---|\n| | | | | | | | |\n")
FC_DIR = tempfile.mkdtemp(dir=TMP)


class Git:
    def __init__(self, tags=("L", "LE", "E"), not_ancestor=(), status="", diff_code=0, diff_pcode=0, split=None,
                 skeleton=None, forecasts=FILLED, europe_run=True, seen=None, pinned_diff=0, forecasts_now=None):
        self.t = {"participation-L-freeze": "1" * 40, "participation-LE-freeze": "2" * 40,
                  "participation-E-freeze": "3" * 40}
        self.t = {k: v for k, v in self.t.items() if k.split("-")[1] in tags}
        self.not_anc, self.status, self.dc, self.dp = set(not_ancestor), status, diff_code, diff_pcode
        self.split = split or SPLIT
        self.skeleton = json.dumps({"quick": False}) if skeleton is None else skeleton
        self.forecasts, self.europe_run, self.pinned_diff = forecasts, europe_run, pinned_diff
        self.seen = json.dumps({"scouts_folders": {"moved_to": "D:/elsewhere"}}) if seen is None else seen
        self.fc_path = os.path.join(FC_DIR, f"fc_{id(self)}.md")
        open(self.fc_path, "w", encoding="utf-8").write(forecasts if forecasts_now is None else forecasts_now)

    def __call__(self, *a):
        fetch.FORECASTS_PATH = self.fc_path               # this fake's working copy of the forecast sheets
        a = list(a)
        if a[:2] == ["rev-parse", "-q"]:
            tag = a[3].replace("refs/tags/", "").replace("^{commit}", "")
            return (0, self.t[tag] + "\n") if tag in self.t else (1, "")
        if a[0] == "merge-base":
            return (1, "") if (a[2], a[3]) in self.not_anc else (0, "")
        if a[0] == "show":
            for suffix, val in (("data/split.json", json.dumps(self.split)), ("data/fetch_log.jsonl", ""),
                                ("data/skeleton.json", self.skeleton), ("FORECASTS.md", self.forecasts),
                                ("data/seen.json", self.seen), ("data/segments.csv", "geo,series,tau,reason,citation\n"),
                                ("data/ipums_samples.json", json.dumps(SAMPLES_NOW))):
                if a[1].endswith(suffix):
                    return (0, val) if val is not None else (1, "")
            return 1, ""
        if a[0] == "ls-tree":
            return 0, ("results/europe_run_abc1234.json\n" if self.europe_run else "results/simulate.json\n")
        if a[0] == "status":
            return 0, self.status
        if a[0] == "diff":
            if "--quiet" in a and a[-1] in fetch.PINNED:
                return self.pinned_diff, ""
            return (self.dc, "") if a[-1] == "code" else (self.dp, "")
        if a[:1] == ["rev-parse"]:
            return 0, "9" * 40 + "\n"
        return 1, ""


SAMPLES_NOW = json.load(open(ipums.SAMPLES, encoding="utf-8"))


def passes(fn):
    t, msg, n = attempt(fn)
    return t is None, f"{t.__name__ if t else 'ok'}: {msg[:100]}"


print("(d) the guard with simulated tags")
sandbox()
fetch._git = Git()
check("D1 explore: the frozen explore countries pass", *passes(lambda: fetch.guard("explore", EX, "oecd_rpi")))
res = [refused(lambda c=c: fetch.guard("explore", [c], "oecd_rpi")) for c in CF + ["BR", "OECD"]]
check("D2 explore: every confirm country, a non-member and an aggregate are refused", all(ok for ok, _ in res),
      f"{sum(ok for ok, _ in res)}/{len(res)}")
check("D3 confirm: all members pass on a clean, frozen tree", *passes(lambda: fetch.guard("confirm", fetch.COUNTRIES,
                                                                                          "oecd_rpi")))
res = [refused(lambda c=c: fetch.guard("confirm", [c], "oecd_rpi")) for c in ("BR", "OECD", "EU27", "BG", "RO")]
check("D4 confirm: aggregates and non-members (BG, RO among them) are refused", all(ok for ok, _ in res))
cases = {"no LE tag": Git(tags=("L", "E")), "no L tag": Git(tags=("LE", "E")),
         "L not before LE": Git(not_ancestor={("1" * 40, "2" * 40)}),
         "dirty tree": Git(status=" M code/specs.py\n"), "code changed since LE": Git(diff_code=1),
         "participation/code changed since E": Git(diff_pcode=1), "no European E tag": Git(tags=("L", "LE")),
         "split differs": Git(split={**SPLIT, "explore": SPLIT["confirm"], "confirm": SPLIT["explore"]})}
res = {}
for k, g in cases.items():
    fetch._git = g
    fetch._READY.clear()
    res[k] = refused(lambda: fetch.guard("confirm", ["US"], "oecd_rpi"))
check("D5 confirm refused for: " + ", ".join(res), all(ok for ok, _ in res.values()),
      "; ".join(f"{k}: {d}" for k, (ok, d) in res.items() if not ok))
unfilled = FILLED.replace("| LR-Y0: x | > 0 | + | 0.6 | 0.2 | 0.1 |", "| LR-Y0: x | > 0 | | | | |")
ready_cases = {"no skeleton in the L commit": None,
               "a --quick skeleton": Git(skeleton=json.dumps({"quick": True})),
               "unfilled forecast sheets": Git(forecasts=unfilled),
               "no European run in the L commit": Git(europe_run=False),
               "the scouts' move unrecorded": Git(seen=json.dumps({"scouts_folders": {"moved_to": None}})),
               "a frozen input changed since L (segments, coverage, skeleton, split, samples, protocol)":
                   Git(pinned_diff=1),
               "FORECASTS.md edited outside the E-L table":
                   Git(forecasts_now=FILLED.replace("| 0.3 | 0.1 |", "| 0.9 | 0.0 |", 1))}
g0 = Git()
g0.skeleton = None
ready_cases["no skeleton in the L commit"] = g0
res = {}
for k, g in ready_cases.items():
    fetch._git = g
    for half, geos in (("explore", EX), ("confirm", ["US"])):
        fetch._READY.clear()
        res[f"{half}: {k}"] = refused(lambda: fetch.guard(half, geos, "oecd_rpi"))
check("D7 a premature L tag or a changed frozen input opens neither half: " + "; ".join(ready_cases),
      all(ok for ok, _ in res.values()), "; ".join(f"{k}: {d}" for k, (ok, d) in res.items() if not ok))
added = FILLED.rstrip("\n") + "\n| Stella | E-L1 | > 0 | + | 0.6 | 0.3 | 0.1 | |\n"
fetch._git = Git(forecasts_now=added)
fetch._READY.clear()
check("D8 FORECASTS.md may gain E-L rows after the L tag", passes(lambda: fetch.guard("confirm", ["US"], "oecd_rpi"))[0]
      and passes(lambda: fetch.guard("explore", EX, "oecd_rpi"))[0])
fetch._git = Git(tags=("L", "E"))
check("D6 explore needs only the L tag; confirm then stays closed",
      passes(lambda: fetch.guard("explore", EX, "jst"))[0] and refused(lambda: fetch.guard("confirm", CF, "jst"))[0])
restore()

# ---------------------------------------------------------------- (e) order
print("(e) L14's order")


def open_order(half, geos, by=True, q_first=True, cover=None):
    """Write the opening's records in the sandbox log: a q download, knots (by the opening), F_L (by the loader)."""
    if q_first:
        fetch._log({"source": "oecd_rpi", "url": "x", "half": half, "sha256": "s", "geos": sorted(geos)})
    fetch.record("knots", half, {"q": {}, "geos": sorted(cover or geos)}, by=fetch.KNOTS_BY if by else None)
    fetch.record("F_L", half, {}, by=fetch.F_L_BY if by else None)


sandbox()
fetch._git = Git()
ok1 = refused(lambda: fetch.guard("explore", EX, "oecd_lfs"))[0]
ok2 = refused(lambda: fetch.guard("explore", EX, "ilostat"))[0]
fetch.record("knots", "explore", {"q": {}})
fetch.record("F_L", "explore", {})
ok3 = refused(lambda: fetch.guard("explore", EX, "oecd_lfs"))[0]               # stray records: no 'by', no q first
open_order("explore", EX, q_first=False)
ok3b = refused(lambda: fetch.guard("explore", EX, "oecd_lfs"))[0]              # knots before any q download
restore()
sandbox()
fetch._git = Git()
open_order("explore", EX, cover=EX[:2])
ok3c = refused(lambda: fetch.guard("explore", EX, "oecd_lfs"))[0]              # knots that do not cover the request
restore()
sandbox()
fetch._git = Git()
open_order("explore", EX)
ok4 = passes(lambda: fetch.guard("explore", EX, "oecd_lfs"))[0]
ok5 = refused(lambda: fetch.guard("confirm", CF, "oecd_lfs"))[0]
ok6 = passes(lambda: fetch.guard("explore", EX, "oecd_rpi"))[0]
check("E1 outcome doors refuse until the half has a q download, then the opening's knots covering the request, then "
      "the loader's F_L; stray records, knots before q and knots not covering the request open nothing (regressor "
      "doors do not wait); the explore records do not open the confirm half",
      all([ok1, ok2, ok3, ok3b, ok3c, ok4, ok5, ok6]), str([ok1, ok2, ok3, ok3b, ok3c, ok4, ok5, ok6]))
fetch.record("knots", "explore", {"q": {"US": {"k1": 9.0}}, "geos": EX}, by=fetch.KNOTS_BY)
check("E2 the look keeps the FIRST explore knots record (a later explore record never replaces it)",
      opening.logged_knots("explore").get("q") == {})
ok = refused(lambda: opening.open_half("explore", EX))[0]
check("E3 a half's knots are recorded once: a second opening with record=True is refused before any door", ok)
restore()

# ---------------------------------------------------------------- (f) L1 caps and responses
print("(f) unseen cells at the door")
sandbox()
fetch._git = Git()
open_order("confirm", ["FR", "US"])
urls = []


def fake(url, headers=None, timeout=300):
    urls.append(url)
    return b"REF_AREA,TIME_PERIOD,OBS_VALUE,OBS_STATUS,MEASURE,UNIT_MEASURE,SEX,AGE,LABOUR_FORCE_STATUS\n"


fetch._download = fake
fetch.oecd("oecd_lfs", LFS_KEY, ["FR", "US"], "confirm")
fetch.oecd("oecd_rpi", {"FREQ": "A", "MEASURE": "RPI", "UNIT_MEASURE": "IX"}, ["FR", "US"], "confirm")
ends = sorted(re.findall(r"endPeriod=(\d{4})", u)[0] + ":" + u.split("/")[-1].split(".")[0] for u in urls)
check("F1 European members' queries end at 1994 (outcome) and 1993 (lagged q); others at 2025 and 2024",
      ends == ["1993:FRA", "1994:FRA", "2024:USA", "2025:USA"], str(ends))


def late(url, headers=None, timeout=300):
    return (b"REF_AREA,TIME_PERIOD,OBS_VALUE,OBS_STATUS,MEASURE,UNIT_MEASURE,SEX,AGE,LABOUR_FORCE_STATUS\n"
            b"FRA,1999,70,,LF_RATE,PT_POP_SUB,F,Y25T29,LF\n")


def other(url, headers=None, timeout=300):
    return (b"REF_AREA,TIME_PERIOD,OBS_VALUE,OBS_STATUS,MEASURE,UNIT_MEASURE,SEX,AGE,LABOUR_FORCE_STATUS\n"
            b"OECD,1990,70,,LF_RATE,PT_POP_SUB,F,Y25T29,LF\n")


n_cached0 = len(os.listdir(os.path.join(fetch.RAW, "confirm")))
fetch._download = late
ok_a = refused(lambda: fetch.oecd("oecd_lfs", {**LFS_KEY, "AGE": "Y30T34"}, ["FR"], "confirm"))[0]
fetch._download = other
ok_b = refused(lambda: fetch.oecd("oecd_lfs", {**LFS_KEY, "AGE": "Y55T59"}, ["FR"], "confirm"))[0]
rej = [json.loads(ln) for ln in open(fetch.LOG) if "rejected" in ln]
cached = os.listdir(os.path.join(fetch.RAW, "confirm"))
check("F2 a response with years after the cap, or with an area not requested (an aggregate), is refused, logged as "
      "rejected, never cached", ok_a and ok_b and len(rej) == 2 and len(cached) == n_cached0, f"{ok_a} {ok_b} {len(rej)} "
      f"cached {len(cached)}")
check("F3 the key must pin every dimension but REF_AREA", refused(lambda: fetch.oecd("oecd_lfs", {"MEASURE": "LF_RATE"},
                                                                                      ["FR"], "confirm"))[0])
restore()

# ---------------------------------------------------------------- (g) single-file loaders
print("(g) single-file loaders")
sandbox()
fetch._git = Git()
jrows = []
for iso in ["USA", "FRA", "ESP", "AUS", "CAN", "IRL"]:
    for t in (1960, 1995, 1996, 2000):
        jrows.append(dict(year=t, country=iso, iso=iso, hpnom=1.0, housing_rent_yd=0.05, housing_capgain=0.02,
                          housing_capgain_ipol=0, rent_ipolated=0, cpi=100.0, stir=3.0, ltrate=4.0))
xb = io.BytesIO()
pd.DataFrame(jrows).to_excel(xb, index=False)
fetch._download = lambda url, headers=None, timeout=300: xb.getvalue()
fetch._APPENDED.clear()
split_ex = [c for c in EX]
allowed_test = ["US", "FR"] if all(c in EX for c in ("US", "FR")) else [c for c in EX if c in ("US", "AU", "ES")][:2]
j = fetch.jst(allowed_test, "explore")
caps = {c: fetch.last_obs_year(c) - 1 for c in allowed_test}
ok = (set(j["geo"]) <= set(allowed_test) and all(y <= caps[g] for g, y in zip(j["geo"], j["year"]))
      and set(j.columns) == {"geo", "year", "hpnom", "housing_rent_yd", "housing_capgain", "housing_capgain_ipol",
                              "rent_ipolated", "cpi"})
check("G1 the JST loader returns only the requested open countries' rows, cut at L1 (European q to 1995), and only "
      "the q columns, from a file of every country", ok, f"{sorted(set(j['geo']))} cols {list(j.columns)}")
ilo = pd.DataFrame([dict(ref_area="USA", time="1990", obs_value="1"), dict(ref_area="CAN", time="1990",
                                                                              obs_value="1")]).to_csv(index=False)
fetch._download = lambda url, headers=None, timeout=300: ilo.encode()
open_order("explore", EX)
ok = refused(lambda: fetch.ilostat(["US"] if "US" in EX else EX[:1], "explore"))[0]
check("G2 an ILOSTAT answer holding another area is refused", ok)
restore()

# ---------------------------------------------------------------- (h) IPUMS
print("(h) the IPUMS loader")
bad = ["EMPSTAT", "LABFORCE", "SCHOOL", "EDATTAN", "INCTOT", "OWNERSHIP", "MARST", "OCC", "WHATEVER"]
res = [refused(lambda b=b: ipums.check_columns(ipums.HER_VARS + [b]), ipums.ExtractError) for b in bad]
check("H1 the loader refuses any column outside the whitelist: " + ", ".join(bad), all(ok for ok, _ in res))
check("H2 her variables, RELATED and the attached flags pass",
      attempt(lambda: ipums.check_columns(ipums.HER_VARS + ["RELATED", "QAGE", "QRELATE"]))[0] is None)
sandbox()
check("H3 the loader refuses before the L-freeze (real git state)", refused(lambda: ipums.F_L("explore"))[0])
restore()


def ddi_xml(samples: dict) -> str:
    cats = {"SAMPLE": samples, "RELATE": {1: "Head", 3: "Child", 9: "Unknown"}, "RELATED": {1000: "Head", 3000: "Child"},
            "GQ": {10: "Households", 20: "Group quarters"}}
    x = ['<?xml version="1.0"?><codeBook><dataDscr>']
    for v, cs in cats.items():
        x.append(f'<var name="{v}">' + "".join(f"<catgry><catValu>{k}</catValu><labl>{lab}</labl></catgry>"
                                            for k, lab in cs.items()) + "</var>")
    return "".join(x) + "</dataDscr></codeBook>"


def write_extract(folder, stem, rows, samples, ddi=True):
    os.makedirs(folder, exist_ok=True)
    pd.DataFrame(rows).to_csv(os.path.join(folder, stem + ".csv"), index=False)
    if ddi:
        open(os.path.join(folder, stem + ".xml"), "w", encoding="utf-8").write(ddi_xml(samples))


def persons(code, n=60, age=None, rel=3):
    return [dict(COUNTRY=1, YEAR=1970, SAMPLE=code, SERIAL=i, PERNUM=1, HHWT=1, PERWT=1,
                 AGE=age if age is not None else 20 + i % 15, SEX=1 + i % 2, RELATE=rel if i % 3 else 1,
                 RELATED=3000 if (rel == 3 and i % 3) else 1000, MOMLOC=0, POPLOC=0, GQ=10) for i in range(n)]


fl = {r["sample"]: r for r in SAMPLES_NOW["F_L"]}
ex_fl = sorted({SAMPLES_NOW["roles"][c]["F_L"] for c in EX if c in SAMPLES_NOW["roles"]})
plain = [s_ for s_ in ex_fl if not fl[s_]["grouped_age"]]
grouped = [s_ for s_ in ex_fl if fl[s_]["grouped_age"]]
labels = {100 + i: fl[s_]["title"] for i, s_ in enumerate(ex_fl)}
code_of = {s_: 100 + i for i, s_ in enumerate(ex_fl)}
rows = sum([persons(code_of[s_]) for s_ in ex_fl], [])


def ipums_try(setup):
    d = sandbox()
    fetch._git = Git()
    setup(fetch.IPUMS_DIR)
    open_order("explore", EX)
    t, msg, n = attempt(lambda: ipums.F_L("explore", record=False))
    out = None
    if t is None:
        out = ipums.F_L("explore", record=False)
    restore()
    return t, msg, out


real_stray = ipums.stray_microdata
ipums.stray_microdata = lambda root=None: []                       # the real tree is checked by check_freeze_ready
t, msg, out = ipums_try(lambda f: write_extract(f, "ipumsi_00009", rows, labels))
ok_plain = t is None and all(np.isfinite(out[fl[s_]["country"]]["25-34"]["value"]) for s_ in plain)
ok_grp = t is None and all(out[fl[s_]["country"]]["25-34"].get("unusable") == "no L2 record of its age intervals"
                           for s_ in grouped if not fl[s_].get("age_intervals"))
check("H5 a grouped-age sample with no L2 record of its intervals is unusable alone; the other samples compute",
      ok_plain and ok_grp, f"{t.__name__ if t else ''} {msg[:100]}; grouped {grouped}")
half_rows = [r for r in rows if r["SAMPLE"] == code_of[ex_fl[0]]]
rest_rows = [r for r in rows if r["SAMPLE"] != code_of[ex_fl[0]]]
t, msg, out = ipums_try(lambda f: (write_extract(f, "ipumsi_00010", half_rows, {code_of[ex_fl[0]]: labels[code_of[ex_fl[0]]]}),
                                   write_extract(f, "ipumsi_00011", rest_rows,
                                                 {k: v for k, v in labels.items() if k != code_of[ex_fl[0]]})))
check("H6 two extracts (A and B as separate files), each with its DDI, are read together", t is None, msg[:120])
t, msg, _ = ipums_try(lambda f: write_extract(f, "ipumsi_00012", rows, {**labels, 999: "Brazil 1970"}))
ok1 = t is ipums.ExtractError and "outside the frozen list" in msg
t, msg, _ = ipums_try(lambda f: write_extract(f, "ipumsi_00013", rows + persons(code_of[ex_fl[0]], 5, age=40), labels))
ok2 = t is ipums.ExtractError and "outside ages 20-34" in msg
t, msg, _ = ipums_try(lambda f: write_extract(f, "ipumsi_00014", rows, labels, ddi=False))
ok3 = t is ipums.ExtractError
check("H7 refused: a DDI listing a sample outside the frozen list, a row aged outside 20-34, a CSV without its DDI",
      ok1 and ok2 and ok3, f"{ok1} {ok2} {ok3}")
ipums.stray_microdata = real_stray
tree = tempfile.mkdtemp(dir=TMP)
os.makedirs(os.path.join(tree, "data", "ipums"))
open(os.path.join(tree, "data", "ipumsi_00001.csv.gz"), "wb").write(b"")
open(os.path.join(tree, "data", "ipums", "ipumsi_00002.csv.gz"), "wb").write(b"")
saved_dir = fetch.IPUMS_DIR
fetch.IPUMS_DIR = os.path.join(tree, "data", "ipums")
st = ipums.stray_microdata(tree)
fetch.IPUMS_DIR = saved_dir
check("H8 microdata outside data/ipums/ is found by name (never opened); the loader refuses while any lies there",
      st == ["data/ipumsi_00001.csv.gz"], str(st))
smp = json.load(open(ipums.SAMPLES, encoding="utf-8"))
recs = ipums.samples_for("F_L", smp, set(EX))
check("H4 a purpose reads only its samples of open countries: F_L samples of explore countries are earliest-with-"
      "RELATE samples of explore countries only", all(r["country"] in EX for r in recs)
      and all(smp["roles"][r["country"]]["F_L"] == r["sample"] for r in recs), str([r["sample"] for r in recs]))
restore()

# ---------------------------------------------------------------- (i) log and cache
print("(i) log and cache")
sandbox()
fetch._git = Git()
order = []
real_log = fetch._log


def spy(entry):
    order.append(("log", os.path.exists(fetch._cache_path("explore", "jst", {"url": fetch.SOURCES["jst"]["url"]},
                                                          ".xlsx"))))
    real_log(entry)


fetch._log = spy
fetch._download = lambda url, headers=None, timeout=300: xb.getvalue()
fetch.jst([c for c in EX if c in ("US", "AU", "ES", "FR")][:1] or EX[:1], "explore")
fetch._log = real_log
check("I1 the log line is written before the cache file", order == [("log", False)], str(order))
p = fetch._cache_path("explore", "jst", {"url": fetch.SOURCES["jst"]["url"]}, ".xlsx")
open(p, "ab").write(b"tampered")
check("I2 a cache file whose SHA-256 is not in the log is refused",
      refused(lambda: fetch.jst(EX[:1], "explore"))[0])
restore()

# ---------------------------------------------------------------- (j) frozen European code
print("(j) participation/code frozen")
pcode = os.path.join(os.path.dirname(LROOT), "code")
bad = []
for f in sorted(os.listdir(pcode)):
    if not f.endswith(".py"):
        continue
    r = subprocess.run(["git", "show", f"{fetch.E_FREEZE}:participation/code/{f}"], cwd=LROOT, capture_output=True)
    now = open(os.path.join(pcode, f), "rb").read().replace(b"\r\n", b"\n")
    if r.returncode != 0 or hashlib.sha256(r.stdout.replace(b"\r\n", b"\n")).digest() != hashlib.sha256(now).digest():
        bad.append(f)
check("J1 every participation/code/*.py has the SHA-256 it had at participation-E-freeze", not bad, str(bad))

# ---------------------------------------------------------------- (k) one door
print("(k) one door")
offenders = []
for sub in ("code", "checks"):
    for f in sorted(os.listdir(os.path.join(LROOT, sub))):
        if f.endswith(".py") and f not in ("fetch.py", "ipums.py", "check_guard.py"):
            txt = open(os.path.join(LROOT, sub, f), encoding="utf-8").read()
            if re.search(r"""["']data["'],\s*["'](raw|ipums)["']|(?<!participation/)data/(raw|ipums)(?=[/"'\s])""", txt):
                offenders.append(f"{sub}/{f}")
check("K1 no long-run script (code/, checks/) but fetch.py and ipums.py names the long-run raw or ipums data folders",
      not offenders, str(offenders))

# ---------------------------------------------------------------- (l) the split
print("(l) the split")
again = sp.assign(SPLIT["population_1960"], SPLIT["countries"])
check("L1 split.assign on the recorded 1960 populations reproduces data/split.json",
      all(again[k] == SPLIT[k] for k in ("seed", "explore", "confirm", "pairs", "strata")))
check("L2 the seed is the protocol's formula of the sorted country list", SPLIT["seed"] == sp.seed_of(SPLIT["countries"]))
partner = [b if a == "US" else a for a, b in SPLIT["pairs"] if "US" in (a, b)]
check("L3 the US is in EXPLORE and its pair partner in CONFIRM", "US" in EX and all(p in CF for p in partner),
      f"partner {partner}")
check("L4 halves differ in size by at most one, are disjoint and cover the countries",
      abs(len(EX) - len(CF)) <= 1 and not set(EX) & set(CF) and sorted(EX + CF) == sorted(SPLIT["countries"]))
check("L5 each pair has one member in each half", all(len({a in EX, b in EX}) == 2 for a, b in SPLIT["pairs"]))
order_ok = all(list(SPLIT["strata"]).index(s) < list(SPLIT["strata"]).index(t)
               for s, t in zip(list(SPLIT["strata"])[:-1], list(SPLIT["strata"])[1:]))
known = {c: s for s, cs in fetch.STRATA.items() for c in cs}
check("L6 strata as section 4 (members of the listed strata where listed; any other member in Other)",
      all(known.get(c, "Other") == s for s, cs in SPLIT["strata"].items() for c in cs) and order_ok)
check("L7 the split's countries are the members entering a verdict test (data/coverage.json)",
      sorted(SPLIT["countries"]) == sp.entering(with_c1=("LR-C1" in SPLIT.get("membership_source", "")
                                                          and "left out" not in SPLIT.get("membership_source", ""))))

# ---------------------------------------------------------------- (m) the European cut
print("(m) the European cut (L1)")
import skeleton  # noqa: E402
pb = skeleton.pspecs.build
first_years = []
for f in glob.glob(os.path.join(os.path.dirname(LROOT), "explore", "**", "*.csv"), recursive=True):
    cols = list(pd.read_csv(f, nrows=0).columns)
    yc = [c for c in cols if c.lower() in ("year", "first_year", "time")]
    if yc:
        v = pd.to_numeric(pd.read_csv(f, usecols=yc)[yc[0]], errors="coerce").dropna()   # the year column only
        if len(v):
            first_years.append((int(v.min()), os.path.relpath(f, os.path.dirname(LROOT))))
import coverage as cv  # noqa: E402
early = sorted(f.replace("\\", "/") for y, f in first_years if y <= fetch.EUROPEAN_LAST)
undisclosed = [f for f in early if f not in cv.EUROPEAN_PRE_CUT]
seen_now = json.load(open(cv.SEEN, encoding="utf-8")) if os.path.exists(cv.SEEN) else {}
check("M1 L1's European cut lies before the European panel grid's first year; every committed European exploration "
      "output with a year at or before it is disclosed by name in data/seen.json (none holds a verdict test's "
      "variable; year columns only are read)",
      fetch.EUROPEAN_LAST < min(pb.YEARS) and not undisclosed
      and set(early) <= set(seen_now.get("european_outputs_before_cut", {})),
      f"cut {fetch.EUROPEAN_LAST}; grid from {min(pb.YEARS)}; at or before the cut: {early}; undisclosed {undisclosed}")
captured = {}
real_cy = pb.country_year


def spy_cy(half, raw=None, geos=None):
    captured.update({k: (int(pd.to_numeric(v["year"], errors="coerce").min()) if len(v) and "year" in v else None)
                     for k, v in raw.items()})
    return real_cy(half, raw=raw, geos=geos)


pb.country_year = spy_cy
try:
    skeleton.european_frames()
finally:
    pb.country_year = real_cy
low = {k: v for k, v in captured.items() if v is not None and v <= fetch.EUROPEAN_LAST}
check("M2 the skeleton's European frames hold no row at or before the cut (dropped at parse)", captured and not low,
      str(low))
import europe_run  # noqa: E402
ed = europe_run.european_data()
nk = sum(1 for k in ed.knots["q"].values() if k.get("k1") is not None)
check("M3 the European real-data run gets knots (seen rows, unseen_only off): most D1 countries have them",
      nk >= 20 and len(ed.H) >= 8, f"{nk} countries with knots; H over {len(ed.H)}")

check("Z1 no network call was attempted during the whole check", not NET, f"{len(NET)}")
check("Z2 the real fetch log is untouched by the check",
      (open(REAL["LOG"], "rb").read() if os.path.exists(REAL["LOG"]) else b"") == LOG_BEFORE)
shutil.rmtree(TMP, ignore_errors=True)
n_fail = sum(1 for _, ok, _ in RESULTS if not ok)
print(f"\n{len(RESULTS) - n_fail}/{len(RESULTS)} checks pass")
sys.exit(1 if n_fail else 0)
