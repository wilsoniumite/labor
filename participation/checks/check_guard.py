# check_guard.py — the blinding guard and loader (code/eurostat.py) and the split (code/split.py, data/split.json).
#   (a) explore and confirm reads are refused in the repository's real git state, before any network call or cache
#       read (before the P freeze: every explore read; after it: confirm countries in an explore read, and so on);
#   (b) half='design' serves the 2010 population query only (demo_pjan TOTAL; not the C-5 single-year structure, not
#       any other dataset);
#   (c) with the freeze tags simulated (the git helper monkeypatched): countries outside the half are refused; the
#       confirm half needs both tags in order (P an ancestor of E, both of HEAD), the frozen split, a clean tree (the
#       fetch log only as the committed log plus this process's own lines) and frozen code; tags are used through their
#       commit shas; the query guards hold (explicit countries, no geo/time keys or prefixes in the filters, only a
#       manifest dataset's own dimensions, annual only);
#   (d) data/split.json is reproduced by the code, halves 15 and 16, each pair split across the halves;
#   (e) the JSON-stat parser on synthetic payloads shaped like the real demo_pjan response: flags, missing cells,
#       several dimensions, dense and sparse forms, non-annual refused; and get()'s cache and log on a mocked download
#       (the log line first; a cache file without a matching log record is refused);
#   (f) clean() blanks u and c cells; is_break finds b, bd, bu.
# The network is blocked for the whole run (requests' adapter and sockets raise); a check that sees a call fails.
#
# Run from participation/:  ../venv/Scripts/python.exe checks/check_guard.py
# Exit status 0 only if every check passes.

from __future__ import annotations

import hashlib
import json
import os
import random
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
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "code"))
import eurostat as es  # noqa: E402
import split as sp  # noqa: E402
import requests  # noqa: E402  (eurostat injected truststore first)

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


# ---------------------------------------------------------------- the network, blocked

NET = []


class NetworkCalled(Exception):
    pass


def _blocked(*a, **k):
    NET.append(a[1:2] if len(a) > 1 else a)
    raise NetworkCalled("network call attempted")


requests.adapters.HTTPAdapter.send = _blocked
socket.create_connection = _blocked
socket.socket.connect = _blocked


def attempt(fn):
    """(exception type or None, message, network calls made) for one call."""
    n0 = len(NET)
    try:
        fn()
        return None, "", len(NET) - n0
    except Exception as e:  # noqa: BLE001
        return type(e), str(e), len(NET) - n0


def refused(fn):
    t, msg, n = attempt(fn)
    return t is es.BlindingError and n == 0, f"{t.__name__ if t else 'no error'}: {msg[:110]}; network calls {n}"


TMP = tempfile.mkdtemp(prefix="check_guard_")
LOG_BEFORE = open(es.LOG, "rb").read()
REAL = {"RAW": es.RAW, "LOG": es.LOG, "SPLIT": es.SPLIT, "_git": es._git, "_download": es._download}


def sandbox():
    """Point the cache and the log at a fresh temporary folder (the real split.json stays)."""
    d = tempfile.mkdtemp(dir=TMP)
    es.RAW, es.LOG = os.path.join(d, "raw"), os.path.join(d, "fetch_log.jsonl")
    return d


def restore():
    for k, v in REAL.items():
        setattr(es, k, v)
    es._APPENDED.clear()


SPLIT = json.load(open(os.path.join(ROOT, "data", "split.json"), encoding="utf-8"))
LFS = {"sex": "T", "age": "Y25-34", "unit": "PC", "citizen": "NAT"}


def git_tag(tag):
    return subprocess.run(["git", "rev-parse", "-q", "--verify", f"refs/tags/{tag}"], cwd=ROOT,
                          capture_output=True).returncode == 0


# ---------------------------------------------------------------- (a) the real git state

print("(a) the real git state")
sandbox()
p_tag, e_tag = git_tag(es.P_FREEZE), git_tag(es.E_FREEZE)
ex, cf = SPLIT["explore"][:3], SPLIT["confirm"][:3]
geos_a = cf if p_tag else ex
check(f"A1 explore read refused ({'P freeze tagged: confirm countries' if p_tag else 'no P freeze tag yet'})",
      *refused(lambda: es.get("lfsa_argan", LFS, geos_a, half="explore")))
geos_c = ["US"] if e_tag else cf
check(f"A2 confirm read refused ({'E freeze tagged: a country outside the 31' if e_tag else 'no E freeze tag yet'})",
      *refused(lambda: es.get("lfsa_argan", LFS, geos_c, half="confirm")))
# a planted cache file must not be served either: the guard runs before the cache
for half, geos in (("explore", geos_a), ("confirm", geos_c)):
    q = json.dumps({"dataset": "lfsa_argan", "filters": {k: [v] for k, v in LFS.items()}, "geos": sorted(geos),
                    "since": None}, sort_keys=True, separators=(",", ":"))
    os.makedirs(os.path.join(es.RAW, half), exist_ok=True)
    open(os.path.join(es.RAW, half, f"lfsa_argan__{hashlib.sha1(q.encode()).hexdigest()[:12]}.json"), "w").write("{}")
ok1, d1 = refused(lambda: es.get("lfsa_argan", LFS, geos_a, half="explore"))
ok2, d2 = refused(lambda: es.get("lfsa_argan", LFS, geos_c, half="confirm"))
check("A3 a planted cache file is not served: the guard runs before the cache read", ok1 and ok2, f"{d1} | {d2}")
check("A4 nothing was logged by the refused reads", not os.path.exists(es.LOG))
restore()

# ---------------------------------------------------------------- (b) design serves demo_pjan only

print("(b) half='design'")
sandbox()
POP2010 = {"age": "TOTAL", "sex": "T", "unit": "NR"}
bad = ["lfsa_argan", "lfsa_ergan", "prc_hicp_aind", "ilc_lvps08", "une_rt_a", "demo_pjanind", "demo_pjangroup",
       "demo_pjan/../lfsa_argan", "demo_pjan?x=1", "demo_pjan&geo=US", "demo_pjan\n"]
res = {c: refused(lambda c=c: es.get(c, {"sex": "T"}, ["SE"], half="design")) for c in bad}
check("B1 every dataset other than demo_pjan refused, with no network call", all(ok for ok, _ in res.values()),
      "; ".join(f"{c}: {'ok' if ok else d}" for c, (ok, d) in res.items() if not ok) or f"{len(bad)} refused")
t, msg, n = attempt(lambda: es.guard("design", list(es.COUNTRIES), "demo_pjan"))
t2, msg2, _ = attempt(lambda: es.guard("design", ["SE"], "DEMO_PJAN"))
outside = {g: refused(lambda g=g: es.guard("design", ["SE", g], "demo_pjan")) for g in ("US", "TR", "EU27_2020")}
check("B2 demo_pjan passes the design guard for the 31 countries, and only for them",
      t is None and t2 is None and n == 0 and all(ok for ok, _ in outside.values()),
      msg or msg2 or "; ".join(f"{g}: {d}" for g, (ok, d) in outside.items() if not ok))
check("B3 DESIGN_DATASETS is exactly {'demo_pjan'}", es.DESIGN_DATASETS == {"demo_pjan"}, str(es.DESIGN_DATASETS))
sys.path.insert(0, os.path.join(ROOT, "code"))
import build  # noqa: E402
pop = build.BY_ID["pop"]
dbad = {
    "the C-5 regressor query (build.MANIFEST 'pop': 2011 single-year ages)":
        lambda: es.get(pop["dataset"], pop["filters"], es.COUNTRIES, half="design", since=pop.get("since")),
    "one single-year age": lambda: es.get("demo_pjan", {**POP2010, "age": "Y20"}, ["SE"], half="design"),
    "TOTAL plus another age": lambda: es.get("demo_pjan", {**POP2010, "age": ["TOTAL", "Y_OPEN"]}, ["SE"], half="design"),
    "by sex": lambda: es.get("demo_pjan", {**POP2010, "sex": ["M", "F"]}, ["SE"], half="design"),
    "a filter left out": lambda: es.get("demo_pjan", {"age": "TOTAL", "sex": "T"}, ["SE"], half="design"),
    "a time filter (since)": lambda: es.get("demo_pjan", POP2010, ["SE"], half="design", since=2011),
}
res = {k: refused(f) for k, f in dbad.items()}
check("B4 half='design' refuses every demo_pjan query but the 2010 population one: " + ", ".join(dbad),
      all(ok for ok, _ in res.values()), "; ".join(f"{k}: {d}" for k, (ok, d) in res.items() if not ok))
t, msg, n = attempt(lambda: es.guard("design", es.COUNTRIES, "demo_pjan", {"age": ["TOTAL"], "sex": ["T"], "unit": ["NR"]}))
check("B5 the 2010 population query (split.py's) passes the design guard, keys in any order",
      t is None and n == 0 and es.DESIGN_QUERIES == {("demo_pjan", (("age", ("TOTAL",)), ("sex", ("T",)),
                                                                    ("unit", ("NR",))), None)}, msg)
restore()

# ---------------------------------------------------------------- (c) tags simulated

print("(c) freeze tags simulated")


SHA = {es.P_FREEZE: "a" * 40, es.E_FREEZE: "b" * 40}
NAME = {v: k for k, v in SHA.items()}
P, E = es.P_FREEZE, es.E_FREEZE


class FakeGit:
    """Answers the git calls of eurostat.guard. Tags resolve only as refs/tags/<tag>^{commit}, to fixed shas; every
    other call must use the sha (a bare tag name gets the answer of a different, hostile ref)."""

    def __init__(self, tags=(P, E), not_ancestor=(), status="", diff_rc=0, frozen_split=None, committed_log=""):
        self.tags, self.not_ancestor, self.status, self.diff_rc = set(tags), set(not_ancestor), status, diff_rc
        self.frozen_split = SPLIT if frozen_split is None else frozen_split   # {} = not in the tag
        self.committed_log = committed_log

    def __call__(self, *args):
        if args[0] == "show":
            if args[1] == f"{SHA[P]}:./data/split.json" and P in self.tags:
                return (0, json.dumps(self.frozen_split)) if self.frozen_split else (128, "")
            if args[1] == "HEAD:./data/fetch_log.jsonl":
                return 0, self.committed_log
            return 128, ""
        if args[:3] == ("rev-parse", "-q", "--verify"):
            m = re.fullmatch(r"refs/tags/(.+)\^\{commit\}", args[3])
            return (0, SHA[m.group(1)] + "\n") if m and m.group(1) in self.tags else (1, "")
        if args[:2] == ("merge-base", "--is-ancestor"):
            if args[2] in (P, E) or args[3] in (P, E):
                return 0, ""                          # a bare tag name: a hostile ref of that name says yes
            a, b = NAME.get(args[2], args[2]), NAME.get(args[3], args[3])
            return (1 if (a, b) in self.not_ancestor else 0), ""
        if args[0] == "status":
            return 0, self.status
        if args[0] == "diff":
            if args[2] in (P, E):
                return 0, ""                          # a bare tag name: the hostile ref says unchanged
            return self.diff_rc, ""
        if args == ("rev-parse", "HEAD"):
            return 0, "f" * 40 + "\n"
        return 1, ""


def passes(fn):
    t, msg, n = attempt(fn)
    return t is None and n == 0, f"{t.__name__ if t else 'passed'} {msg[:100]}"


sandbox()
es._git = FakeGit()
EX, CF = SPLIT["explore"], SPLIT["confirm"]
check("C1 explore: the explore countries pass the guard", *passes(lambda: es.guard("explore", EX, "lfsa_argan")))
res = [refused(lambda c=c: es.guard("explore", EX[:2] + [c]))[0] for c in CF + ["US", "EU27_2020"]]
check("C2 explore: each confirm country (and any country outside the 31) is refused", all(res),
      f"{sum(res)}/{len(res)} refused")
check("C3 explore: get() with a confirm country is refused before the network",
      *refused(lambda: es.get("lfsa_argan", LFS, [EX[0], CF[0]], half="explore")))
t, msg, n = attempt(lambda: es.get("lfsa_argan", LFS, EX[:2], half="explore"))
check("C4 explore: with the tag in place, an allowed get() goes through to the network (here blocked)",
      t is NetworkCalled and n == 1, f"{t.__name__ if t else 'no error'}; calls {n}")
check("C5 confirm: the 31 countries pass the guard on a clean, frozen tree",
      *passes(lambda: es.guard("confirm", es.COUNTRIES, "lfsa_argan")))
res = [refused(lambda c=c: es.guard("confirm", ["SE", c]))[0] for c in ["US", "TR", "RS", "EU27_2020", "EA20"]]
check("C6 confirm: countries outside the 31 refused", all(res), f"{sum(res)}/{len(res)} refused")
cases = {
    "a modified code file": FakeGit(status=" M participation/code/specs.py\n"),
    "an untracked data file": FakeGit(status="?? participation/data/extra.csv\n"),
    "the code changed since the E freeze": FakeGit(diff_rc=1),
    "the E tag not an ancestor of HEAD": FakeGit(not_ancestor={(E, "HEAD")}),
    "only the P tag": FakeGit(tags=(P,)),
    "only the E tag (no P freeze)": FakeGit(tags=(E,)),
    "the P tag not an ancestor of the E tag": FakeGit(not_ancestor={(P, E)}),
    "the P tag not an ancestor of HEAD": FakeGit(not_ancestor={(P, "HEAD")}),
    "the working split.json differs from the frozen one":
        FakeGit(frozen_split=dict(SPLIT, explore=sorted(SPLIT["explore"][1:] + SPLIT["confirm"][:1]),
                                  confirm=sorted(SPLIT["confirm"][1:] + SPLIT["explore"][:1]))),
    "the split not in the P-freeze commit": FakeGit(frozen_split={}),
    "the fetch log modified by someone else": FakeGit(status=" M participation/data/fetch_log.jsonl\n"),
}
res = {}
for name, g in cases.items():
    es._git = g
    res[name] = refused(lambda: es.guard("confirm", ["SE"]))
check("C7 confirm refused for: " + ", ".join(cases), all(ok for ok, _ in res.values()),
      "; ".join(f"{k}: {d}" for k, (ok, d) in res.items() if not ok))
COMMITTED = '{"dataset": "x", "n": 1}\n{"dataset": "x", "n": 2}\n'
OWN = '{"dataset": "y", "n": 3}\n'
LOGST = " M participation/data/fetch_log.jsonl\n"


def with_log(text, appended, git):
    open(es.LOG, "w", encoding="utf-8", newline="\n").write(text)
    es._APPENDED[:] = appended
    es._git = git


with_log(COMMITTED + OWN, [OWN], FakeGit(status=LOGST, committed_log=COMMITTED))
ok_own = passes(lambda: es.guard("confirm", ["SE"]))
with_log(COMMITTED + OWN, [OWN], FakeGit(status=LOGST + " M participation/code/build.py\n", committed_log=COMMITTED))
ok_more = refused(lambda: es.guard("confirm", ["SE"]))
with_log(COMMITTED.replace('"n": 1', '"n": 9') + OWN, [OWN], FakeGit(status=LOGST, committed_log=COMMITTED))
ok_edit = refused(lambda: es.guard("confirm", ["SE"]))
with_log(COMMITTED.split("\n")[1] + "\n" + OWN, [OWN], FakeGit(status=LOGST, committed_log=COMMITTED))
ok_del = refused(lambda: es.guard("confirm", ["SE"]))
with_log(COMMITTED + OWN + OWN, [OWN], FakeGit(status=LOGST, committed_log=COMMITTED))
ok_extra = refused(lambda: es.guard("confirm", ["SE"]))
es._APPENDED.clear()
check("C8 confirm: a fetch log that is the committed log plus this process's own lines does not lock out the next "
      "fetch; another changed file, an edited or deleted committed line, or a line this process did not write does",
      ok_own[0] and ok_more[0] and ok_edit[0] and ok_del[0] and ok_extra[0],
      f"own {ok_own[1]}; more {ok_more[1]}; edit {ok_edit[1]}; deleted {ok_del[1]}; extra {ok_extra[1]}")
res = {}
for name, g in {"no P tag": FakeGit(tags=()), "P tag not an ancestor": FakeGit(not_ancestor={(P, "HEAD")})}.items():
    es._git = g
    res[name] = refused(lambda: es.guard("explore", EX[:2]))
es._git = FakeGit(frozen_split={})
res["split.json not in the P-freeze commit"] = refused(lambda: es.guard("explore", EX[:2]))
moved = dict(SPLIT, explore=sorted(EX[1:] + CF[:1]), confirm=sorted(CF[1:] + EX[:1]))
es._git = FakeGit(frozen_split=moved)
res["the working split.json differs from the frozen one"] = refused(lambda: es.guard("explore", EX[1:3]))
check("C9 explore refused for: " + ", ".join(res), all(ok for ok, _ in res.values()),
      "; ".join(f"{k}: {d}" for k, (ok, d) in res.items() if not ok))
es.SPLIT = os.path.join(TMP, "no_working_copy.json")
es._git = FakeGit(frozen_split=moved)
ok_f = passes(lambda: es.guard("explore", [CF[0]]))[0] and refused(lambda: es.guard("explore", [EX[0]]))[0]
es.SPLIT = REAL["SPLIT"]
check("C10 explore: the allowed countries are those of the frozen split.json, not of the working copy", ok_f)
es._git = FakeGit(not_ancestor={(P, "HEAD"), (E, "HEAD")})
ok_sha = refused(lambda: es.guard("explore", EX[:2]))[0] and refused(lambda: es.guard("confirm", ["SE"]))[0]
es._git = FakeGit(diff_rc=1)
ok_sha = ok_sha and refused(lambda: es.guard("confirm", ["SE"]))[0]
check("C10b tags are used through their commit shas: a hostile ref with a tag's bare name (answering 'ancestor' and "
      "'unchanged') cannot stand in for the tag", ok_sha)
es._git = FakeGit()
qbad = {
    "empty country list": lambda: es.get("demo_pjan", {"sex": "T"}, [], half="design"),
    "a bare string for geos": lambda: es.get("demo_pjan", {"sex": "T"}, "SE", half="design"),
    "geo inside the filters": lambda: es.get("lfsa_argan", {"geo": CF[:1]}, EX[:1], half="explore"),
    "time inside the filters": lambda: es.get("demo_pjan", {"time": "2010"}, ["SE"], half="design"),
    "a period key": lambda: es.get("demo_pjan", {"untiltimeperiod": "2010"}, ["SE"], half="design"),
    "freq other than A": lambda: es.get("lfsa_argan", {"freq": "Q"}, EX[:1], half="explore"),
    "a value with URL characters": lambda: es.get("lfsa_argan", {"sex": "T&geo=AT"}, EX[:1], half="explore"),
    "a country code with a trailing newline": lambda: es.get("demo_pjan", {"sex": "T"}, ["SE\n"], half="design"),
    "an unknown half": lambda: es.get("demo_pjan", {"sex": "T"}, ["SE"], half="all"),
    "a geo-prefixed key (geolevel)": lambda: es.get("lfsa_argan", {**LFS, "geolevel": "country"}, EX[:1], half="explore"),
    "a geo-prefixed key (geocode)": lambda: es.get("lfsa_argan", {**LFS, "geocode": CF[0]}, EX[:1], half="explore"),
    "a time-prefixed key": lambda: es.get("lfsa_argan", {**LFS, "timeframe": "x"}, EX[:1], half="explore"),
    "a key that is not a dimension of the manifest dataset":
        lambda: es.get("lfsa_argan", {**LFS, "nuts": "x"}, EX[:1], half="explore"),
}
res = {k: refused(f) for k, f in qbad.items()}
check("C11 query guards refuse: " + ", ".join(qbad), all(ok for ok, _ in res.values()),
      "; ".join(f"{k}: {d}" for k, (ok, d) in res.items() if not ok))
restore()

# ---------------------------------------------------------------- (d) the split

print("(d) the split")
C1 = sorted("AT BE BG CY CZ DE DK EE EL ES FI FR HR HU IE IT LT LU LV MT NL PL PT RO SE SI SK NO IS CH UK".split())
STRATA = {"Nordic": "DK FI SE NO IS", "Continental": "AT BE CH DE FR LU NL", "Anglo": "IE UK",
          "South": "CY EL ES IT MT PT", "CEE": "BG CZ EE HR HU LT LV PL RO SI SK"}
STRATA = {k: v.split() for k, v in STRATA.items()}
check("D1 COUNTRIES and STRATA as PROTOCOL C1 and section 4",
      es.COUNTRIES == C1 and es.STRATA == STRATA and SPLIT["countries"] == C1 and SPLIT["strata"] == STRATA)
check("D2 split.json has exactly the keys {seed, countries, strata, population_2010, pairs, explore, confirm}",
      list(SPLIT) == ["seed", "countries", "strata", "population_2010", "pairs", "explore", "confirm"], list(SPLIT))
seed = int(hashlib.sha256(b"participation-split-v1|" + ",".join(C1).encode()).hexdigest()[:16], 16)
check("D3 the seed is the protocol's formula of the sorted country list", SPLIT["seed"] == seed, str(seed))
again = json.loads(json.dumps(sp.assign(SPLIT["population_2010"])))
check("D4 split.assign() on the recorded 2010 populations reproduces split.json exactly", again == SPLIT)
codes = C1[:]
random.Random(7).shuffle(codes)
pop_shuffled = {c: SPLIT["population_2010"][c] for c in codes}
again2 = json.loads(json.dumps(sp.assign(pop_shuffled, countries=codes)))
check("D5 the split does not depend on the order the countries are listed in", again2 == SPLIT)
sandbox()
es.RAW, es.LOG = REAL["RAW"], REAL["LOG"]  # the real design cache and its log record, read only (a hit is not logged)
cache = os.path.join(REAL["RAW"], "design")
if os.path.isdir(cache) and any(f.startswith("demo_pjan__") for f in os.listdir(cache)):
    t, msg, n = attempt(lambda: sp.build())
    full = json.loads(json.dumps(sp.build())) if t is None else None
    check("D6 the whole pipeline (cached demo_pjan through the guarded loader, then assign) reproduces split.json",
          t is None and n == 0 and full == SPLIT, f"{t.__name__ if t else 'ok'} {msg[:100]}; network calls {n}")
else:
    check("D6 the whole pipeline reproduces split.json — demo_pjan cache absent (gitignored); populations checked "
          "against split.json only; run code/split.py to refetch", True)
restore()
E, Cf = set(SPLIT["explore"]), set(SPLIT["confirm"])
check("D7 halves of 15 and 16, disjoint, covering the 31",
      sorted([len(E), len(Cf)]) == [15, 16] and not E & Cf and sorted(E | Cf) == C1, f"{len(E)}/{len(Cf)}")
pairs = SPLIT["pairs"]
check("D8 each pair has one member in each half", all(len({a in E, b in E}) == 2 for a, b in pairs),
      f"{len(pairs)} pairs")
pop = SPLIT["population_2010"]
adj, left = True, []
for name, members in STRATA.items():
    ranked = sorted(members, key=lambda c: -pop[c])
    want = [[ranked[i], ranked[i + 1]] for i in range(0, len(ranked) - 1, 2)]
    adj &= all(p in pairs for p in want)
    if len(ranked) % 2:
        left.append(ranked[-1])
in_pairs = {c for p in pairs for c in p}
check("D9 pairs are adjacent by 2010 population within each stratum; the leftovers are the smallest of the odd strata",
      adj and len(pairs) == 14 and sorted(set(C1) - in_pairs) == sorted(left), f"leftovers {left}")
check("D10 every country has a positive 2010 population", all(pop[c] > 0 for c in C1))

# ---------------------------------------------------------------- (e) the JSON-stat parser

print("(e) JSON-stat parsing")


def jsonstat(dims, value, status=None, index_as_list=()):
    """A payload shaped like the Eurostat response (keys, extension, index dicts in Eurostat order)."""
    dim = {}
    for d, cs in dims:
        idx = list(cs) if d in index_as_list else {c: i for i, c in enumerate(cs)}
        dim[d] = {"label": d, "category": {"index": idx, "label": {c: c for c in cs}}}
    p = {"version": "2.0", "class": "dataset", "label": "synthetic", "source": "ESTAT", "updated": "2026-01-01",
         "value": value, "status": status if status is not None else {}, "id": [d for d, _ in dims],
         "size": [len(cs) for _, cs in dims], "dimension": dim,
         "extension": {"lang": "EN", "id": "SYN", "agencyId": "ESTAT", "version": "1.0",
                       "status": {"label": {"b": "break in time series"}},
                       "positions-with-no-data": {d: [] for d, _ in dims}}}
    return p


DIMS = [("freq", ["A"]), ("unit", ["PC"]), ("sex", ["F", "M"]), ("age", ["Y25-29", "Y30-34"]),
        ("geo", ["SE", "BE", "EL"]), ("time", ["2010", "2011", "2012", "2013"])]
sizes = [len(c) for _, c in DIMS]
N = int(np.prod(sizes))
MISSING = {5, 17, 30, 47}
VAL = {str(i): 100 + i / 4 for i in range(N) if i not in MISSING}
STAT = {"3": "b", "4": "u", "5": "c", "9": "bu", "10": "bd", "20": "e", "21": "p", "33": "bep"}


def cell(i):
    """Row-major decoding written out by hand (independent of numpy)."""
    out = {}
    for (d, cs), s in zip(reversed(DIMS), reversed(sizes)):
        out[d] = cs[i % s]
        i //= s
    return out


df = es.parse(jsonstat(DIMS, VAL, STAT))
check("E1 long format: columns geo, year, value, flag, then the other dimensions (freq dropped); one row per cell",
      list(df.columns) == ["geo", "year", "value", "flag", "unit", "sex", "age"] and len(df) == N, list(df.columns))
check("E2 dtypes: year int, value float, flag str", df["year"].dtype.kind == "i" and df["value"].dtype == float
      and all(isinstance(f, str) for f in df["flag"]))
ix = df.set_index(["sex", "age", "geo", "year"])
bad = []
for i in range(N):
    c = cell(i)
    r = ix.loc[(c["sex"], c["age"], c["geo"], int(c["time"]))]
    want_v, want_f = VAL.get(str(i), np.nan), STAT.get(str(i), "")
    if not ((np.isnan(want_v) and np.isnan(r["value"])) or r["value"] == want_v) or r["flag"] != want_f:
        bad.append(i)
check("E3 every cell lands at its row-major position: values, NaN for missing cells, flags ('' where none)",
      not bad, f"wrong cells {bad[:5]}" if bad else f"{N} cells, {len(MISSING)} missing, {len(STAT)} flagged")
check("E4 a flagged cell without a value (confidential) is NaN with its flag", np.isnan(df["value"].iloc[5])
      and df["flag"].iloc[5] == "c")
dense = es.parse(jsonstat(DIMS, [VAL.get(str(i)) for i in range(N)], [STAT.get(str(i)) for i in range(N)]))
check("E5 the dense form (value and status as lists with nulls) parses to the same frame", dense.equals(df))
shuffled = jsonstat(DIMS, VAL, STAT)
t_idx = shuffled["dimension"]["time"]["category"]["index"]
shuffled["dimension"]["time"]["category"]["index"] = dict(reversed(list(t_idx.items())))
lst = jsonstat(DIMS, VAL, STAT, index_as_list=("geo", "age"))
nolabel = jsonstat(DIMS, VAL, STAT)
del nolabel["dimension"]["unit"]["category"]["index"]       # a single-category dimension may give labels only
check("E6 index given as a dict in any key order, as a list, or omitted for a single category: same frame",
      es.parse(shuffled).equals(df) and es.parse(lst).equals(df) and es.parse(nolabel).equals(df))
one = es.parse(jsonstat(DIMS, VAL, "p"))
check("E7 a status given as one string flags every cell", (one["flag"] == "p").all())
q = jsonstat([("freq", ["Q"]), ("geo", ["SE"]), ("time", ["2010-Q1"])], {"0": 1.0})
q2 = jsonstat([("freq", ["A"]), ("geo", ["SE"]), ("time", ["2010-Q1"])], {"0": 1.0})
res = [attempt(lambda p=p: es.parse(p))[0] for p in (q, q2, {"error": [{"status": 400, "label": "bad"}]})]
check("E8 quarterly frequency, non-year time codes and an API error payload are refused (ValueError)",
      res == [ValueError] * 3, str(res))
empty = es.parse(jsonstat([("freq", ["A"]), ("geo", []), ("time", [])], {}))
check("E9 an empty dataset gives an empty frame with the long columns", len(empty) == 0
      and list(empty.columns)[:4] == ["geo", "year", "value", "flag"])

# get() end to end, on a mocked download, in a sandbox
d = sandbox()
CALLS = []
PAY = json.dumps(jsonstat(DIMS, VAL, STAT)).encode()


def fake_download(url):
    CALLS.append(url)
    return PAY


es._download = fake_download
geos = ["SE", "BE", "EL"]
g1 = es.get("demo_pjan", {"unit": "NR", "sex": "T", "age": "TOTAL"}, geos, half="design")
files = [os.path.join(dp, f) for dp, _, fs in os.walk(es.RAW) for f in fs]
log = [json.loads(x) for x in open(es.LOG, encoding="utf-8")]
check("E10 get(): one download, the raw response cached under raw/design/<code>__<sha1[:12]>.json, one log line",
      len(CALLS) == 1 and len(files) == 1 and os.path.basename(os.path.dirname(files[0])) == "design"
      and os.path.basename(files[0]).startswith("demo_pjan__") and len(os.path.basename(files[0])) == 28
      and len(log) == 1 and g1.equals(df), os.path.relpath(files[0], d) if files else "no file")
e = log[0] if log else {}
check("E11 the log line holds dataset, url, utc, half, geos, sha256 (of the cached bytes) and head_commit",
      set(e) == {"dataset", "url", "utc", "half", "geos", "sha256", "head_commit"}
      and e["sha256"] == hashlib.sha256(open(files[0], "rb").read()).hexdigest() and e["half"] == "design"
      and e["geos"] == sorted(geos) and "geo=SE" in e["url"] and "age=TOTAL" in e["url"], str(e)[:160])
g2 = es.get("demo_pjan", {"age": ["TOTAL"], "sex": "T", "unit": ["NR"]}, geos[::-1], half="design")
check("E12 the same query in another order is a cache hit: no download, no new log line, same frame",
      len(CALLS) == 1 and len(open(es.LOG, encoding="utf-8").readlines()) == 1 and g2.equals(g1))
t, msg, _ = attempt(lambda: es.get("demo_pjan", POP2010, ["SE"], half="design"))
files2 = [f for _, _, fs in os.walk(es.RAW) for f in fs]
log2 = [json.loads(x) for x in open(es.LOG, encoding="utf-8")]
check("E13 a response holding countries that were not requested is refused, logged as rejected, never cached",
      t is es.BlindingError and len(files2) == 1 and len(log2) == 2 and "rejected" in log2[-1], msg[:100])
sandbox()                                     # a fresh cache and an empty log: a planted cache file has no record
planted = os.path.join(es.RAW, "design", os.path.basename(files[0]))
os.makedirs(os.path.dirname(planted), exist_ok=True)
open(planted, "wb").write(PAY)
n0 = len(CALLS)
ok_p, d_p = refused(lambda: es.get("demo_pjan", POP2010, geos, half="design"))
open(es.LOG, "w", encoding="utf-8").write(json.dumps({**log[0], "rejected": "x"}) + "\n")
ok_r, d_r = refused(lambda: es.get("demo_pjan", POP2010, geos, half="design"))
open(es.LOG, "w", encoding="utf-8").write(json.dumps({**log[0], "half": "explore"}) + "\n")
ok_h, d_h = refused(lambda: es.get("demo_pjan", POP2010, geos, half="design"))
open(es.LOG, "w", encoding="utf-8").write(json.dumps(log[0]) + "\n")
t, msg, _ = attempt(lambda: es.get("demo_pjan", POP2010, geos, half="design"))
check("E14 a cache file is served only with a matching log record (SHA-256, half, dataset, not rejected): a planted "
      "file, one recorded as rejected or under another half is refused, with no download; with its record it is served",
      ok_p and ok_r and ok_h and t is None and len(CALLS) == n0, f"{d_p} | {d_r} | {d_h} | {msg[:60]}")
es.LOG = os.path.join(TMP, "order", "fetch_log.jsonl")
es.RAW = os.path.join(TMP, "order", "raw")
seen = {}


def spy(entry, _real=es._log):
    seen["cache_at_log_time"] = any(fs for _, _, fs in os.walk(es.RAW)) if os.path.exists(es.RAW) else False
    _real(entry)


es._log = spy
es.get("demo_pjan", POP2010, ["SE", "BE", "EL"], half="design")
es._log = spy.__defaults__[0]
check("E15 the log line is written before the cache file (a crash between them leaves a record, not an orphan file)",
      seen.get("cache_at_log_time") is False and len(es._APPENDED) >= 1)
restore()

# ---------------------------------------------------------------- (f) flags

print("(f) flags")
check("F1 is_break: b, bd, bu, bep yes; '', d, u, e, p, c, None no",
      all(es.is_break(f) for f in ("b", "bd", "bu", "bep"))
      and not any(es.is_break(f) for f in ("", "d", "u", "e", "p", "c", None)))
check("F2 is_unreliable: u, c, bu yes; '', b, bd, e, p, bep, None no",
      all(es.is_unreliable(f) for f in ("u", "c", "bu"))
      and not any(es.is_unreliable(f) for f in ("", "b", "bd", "e", "p", "bep", None)))
before = df.copy()
cl = es.clean(df)
uc = df["flag"].isin(["u", "c", "bu"])
check("F3 clean() blanks the u, c and bu cells, keeps every other value and every flag, leaves its input alone",
      cl["value"][uc].isna().all() and cl["value"][~uc].equals(df["value"][~uc]) and cl["flag"].equals(df["flag"])
      and df.equals(before) and int(uc.sum()) == 3, f"{int(uc.sum())} cells blanked")
by = es.break_years(df)
want = {}
for k, f in STAT.items():
    if "b" in f:
        c = cell(int(k))
        want.setdefault(c["geo"], set()).add(int(c["time"]))
check("F4 break_years() lists each country's years with a b flag", by == {g: sorted(v) for g, v in want.items()},
      str(by))

# ---------------------------------------------------------------- summary

check("Z no network call was made by anything but the deliberate C4 probe", len(NET) == 1, f"{len(NET)} calls")
check("Z2 the real fetch log is untouched by the checks", open(REAL["LOG"], "rb").read() == LOG_BEFORE)
shutil.rmtree(TMP, ignore_errors=True)
n_fail = sum(not ok for _, ok, _ in RESULTS)
print(f"\n{len(RESULTS) - n_fail}/{len(RESULTS)} passed")
sys.exit(1 if n_fail else 0)
