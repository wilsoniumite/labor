# eurostat.py — the one door to Eurostat for the participation study, with the blinding guard built in.
#
# get(code, filters, geos, half, since=None) fetches an annual dataset from the Eurostat dissemination API
# (JSON-stat 2.0) for an explicit list of countries, caches the raw response under data/raw/<half>/ (gitignored),
# appends each download to data/fetch_log.jsonl (PROTOCOL C10) and returns it in long format: geo, year (int),
# value (float, NaN if missing), flag (str, '' if none), then one column per other dimension (freq is checked to be
# annual and dropped). A cached response is re-read, not refetched, and not logged again.
#
# guard(half, geos, dataset, filters, since) runs inside get() before any cache read or network call, and enforces
# PROTOCOL section 4:
#   design  — only the design covariate named in section 4, the population of 1 January 2010: exactly the query in
#             DESIGN_QUERIES (demo_pjan, age TOTAL, sex T, unit NR, no time filter); any countries. Every other
#             demo_pjan query (the 2011 single-year structure of C-5 among them) is a regressor and waits for its half;
#   explore — tag participation-P-freeze exists and is an ancestor of HEAD; countries within data/split.json 'explore'
#             as committed in that tag (the working copy must agree with it);
#   confirm — tag participation-P-freeze exists and is an ancestor of the tag participation-E-freeze, which exists and
#             is an ancestor of HEAD; the working data/split.json equals the one frozen in the P tag;
#             `git status --porcelain -- participation/` is empty, bar the fetch log when its working copy is exactly
#             the committed log followed by the lines this process appended (the look fetches several datasets, and
#             the first fetch's log line must not lock out the second); participation/code unchanged since the E-freeze
#             tag; countries within the 31 of C1.
# Tags are resolved once to commit shas (refs/tags/<tag>^{commit}); every later git call uses the sha, so no other ref
# of the same name can stand in for a tag. Any violation raises BlindingError. The query itself is guarded too: an
# explicit, non-empty country list (an unfiltered query would return every country), no geo, time, period, format or
# lang keys hidden in the filters, for a dataset of data/manifest.json only its own dimensions, codes of plain
# characters, and the countries in the response a subset of those requested. A cached response is served only if
# the fetch log holds a (non-rejected) download of it with the same SHA-256, half and dataset; the log line is written
# before the cache file.
#
# Also: COUNTRIES (C1) and STRATA (section 4); is_break, is_unreliable, clean (C3, C4); break_years; parse (JSON-stat);
# frozen_split() (data/split.json as committed in the P-freeze tag).
#
# Library module (no run line); used by split.py, build.py and confirm.py. Checked by checks/check_guard.py.

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import truststore

truststore.inject_into_ssl()
import requests  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                                  # participation/
RAW = os.path.join(ROOT, "data", "raw")                       # raw responses, gitignored
LOG = os.path.join(ROOT, "data", "fetch_log.jsonl")           # committed (C10)
SPLIT = os.path.join(ROOT, "data", "split.json")
LOG_REL = "participation/data/fetch_log.jsonl"                # the fetch log as `git status --porcelain` names it
MANIFEST_JSON = os.path.join(ROOT, "data", "manifest.json")    # the pipeline's queries (written by build.py)
API = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
UA = {"User-Agent": "Mozilla/5.0 (research; laborformal)"}

HALVES = ("design", "explore", "confirm")
DESIGN_DATASETS = {"demo_pjan"}
# Section 4: the design covariate is the 2010 population; this is its one query (split.py), canonical form.
DESIGN_QUERIES = {("demo_pjan", (("age", ("TOTAL",)), ("sex", ("T",)), ("unit", ("NR",))), None)}
P_FREEZE, E_FREEZE = "participation-P-freeze", "participation-E-freeze"

# C1: EU27 + NO, IS, CH, UK (Eurostat geo codes: EL is Greece, UK the United Kingdom).
COUNTRIES = sorted("AT BE BG CY CZ DE DK EE EL ES FI FR HR HU IE IT LT LU LV MT NL PL PT RO SE SI SK "
                   "NO IS CH UK".split())
# Section 4, in the protocol's order (split.py draws in this order).
STRATA = {
    "Nordic": ["DK", "FI", "SE", "NO", "IS"],
    "Continental": ["AT", "BE", "CH", "DE", "FR", "LU", "NL"],
    "Anglo": ["IE", "UK"],
    "South": ["CY", "EL", "ES", "IT", "MT", "PT"],
    "CEE": ["BG", "CZ", "EE", "HR", "HU", "LT", "LV", "PL", "RO", "SI", "SK"],
}
assert len(COUNTRIES) == 31 and sorted(c for s in STRATA.values() for c in s) == COUNTRIES

FORBIDDEN_KEYS = {"geo", "time", "format", "lang"}            # countries and years are arguments of get()
FORBIDDEN_PREFIXES = ("geo", "time")                           # geolevel, geocode, timeperiod, ...
_CODE = re.compile(r"[a-z][a-z0-9_]*")                        # matched with fullmatch: no trailing newline
_VALUE = re.compile(r"[A-Za-z0-9_.\-]+")
_GEO = re.compile(r"[A-Z]{2}[A-Z0-9_]{0,10}")

_APPENDED: list[str] = []                                     # the exact lines this process appended to the log


class BlindingError(Exception):
    """A request the pre-registration does not allow at this point."""


# ---------------------------------------------------------------- the guard

def _git(*args: str) -> tuple[int, str]:
    """Run git in participation/; (return code, stdout). Monkeypatched by the checks to simulate tags."""
    r = subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.returncode, r.stdout


def _tag_sha(tag: str) -> str:
    """The commit a freeze tag points to; BlindingError if the tag does not exist."""
    rc, out = _git("rev-parse", "-q", "--verify", f"refs/tags/{tag}^{{commit}}")
    sha = out.strip()
    if rc != 0 or not re.fullmatch(r"[0-9a-f]{40,64}", sha):
        raise BlindingError(f"tag {tag} does not exist: this half is closed until that freeze is committed and tagged")
    return sha


def _is_ancestor(a: str, b: str) -> bool:
    return _git("merge-base", "--is-ancestor", a, b)[0] == 0


def _tag_is_ancestor(tag: str) -> str:
    sha = _tag_sha(tag)
    if not _is_ancestor(sha, "HEAD"):
        raise BlindingError(f"tag {tag} is not an ancestor of HEAD: check out a descendant of the freeze")
    return sha


def frozen_split(p_sha: str | None = None) -> dict:
    """data/split.json as committed in the P-freeze tag; the working copy, if present, must agree with it."""
    p_sha = _tag_sha(P_FREEZE) if p_sha is None else p_sha
    rc, out = _git("show", f"{p_sha}:./data/split.json")
    if rc != 0:
        raise BlindingError(f"data/split.json is not in the {P_FREEZE} commit; the split is frozen with the protocol")
    frozen = json.loads(out)
    if os.path.exists(SPLIT):
        here = json.load(open(SPLIT, encoding="utf-8"))
        if (here.get("explore"), here.get("confirm")) != (frozen["explore"], frozen["confirm"]):
            raise BlindingError("data/split.json differs from its frozen copy; the split never changes after the freeze")
    return frozen


def _explore_set(p_sha: str | None = None) -> set[str]:
    """The explore half as frozen in the P-freeze commit."""
    return set(frozen_split(p_sha)["explore"])


def _porcelain_path(line: str) -> str:
    p = line[3:].split(" -> ")[-1].strip().strip('"')
    return p.replace("\\", "/")


def _log_is_own_appends() -> bool:
    """The working fetch log is exactly the committed one followed by the lines this process appended."""
    if not _APPENDED:
        return False
    rc, out = _git("show", "HEAD:./data/fetch_log.jsonl")
    committed = out.splitlines() if rc == 0 else []
    try:
        working = open(LOG, encoding="utf-8").read().splitlines()
    except OSError:
        return False
    return working == committed + [ln.rstrip("\n") for ln in _APPENDED]


def _canon_design(dataset, filters, since):
    return (dataset, tuple(sorted((k, tuple(v)) for k, v in filters.items())), since)


def guard(half: str, geos: list[str] | None = None, dataset: str | None = None, filters: dict | None = None,
          since: int | None = None) -> None:
    """Raise BlindingError unless `half` may be read now (and, if given, these countries, this dataset and, for the
    design half, this query: filters as canonicalised by _check_query)."""
    if half not in HALVES:
        raise BlindingError(f"half must be one of {HALVES}, not {half!r}")
    allowed: set[str] | None = None
    if half == "design":
        if dataset is not None and dataset.lower() not in DESIGN_DATASETS:
            raise BlindingError(f"half='design' serves only the design covariates {sorted(DESIGN_DATASETS)}, "
                                f"not {dataset!r}")
        if filters is not None and _canon_design(str(dataset).lower(), filters, since) not in DESIGN_QUERIES:
            raise BlindingError(f"half='design' serves only the 2010 population query {sorted(DESIGN_QUERIES)}, not "
                                f"{dataset} {filters} since={since}: any other demo_pjan query waits for its half")
        allowed = set(COUNTRIES)                              # the design covariate covers the 31 countries only
    elif half == "explore":
        p_sha = _tag_is_ancestor(P_FREEZE)
        allowed = _explore_set(p_sha)
    else:
        p_sha = _tag_is_ancestor(P_FREEZE)
        e_sha = _tag_is_ancestor(E_FREEZE)
        if not _is_ancestor(p_sha, e_sha):
            raise BlindingError(f"tag {P_FREEZE} is not an ancestor of {E_FREEZE}: P is frozen before E")
        frozen_split(p_sha)
        rc, out = _git("status", "--porcelain", "--untracked-files=all", "--", ".")
        if rc != 0:
            raise BlindingError("git status failed; the confirm half needs a clean, committed participation/")
        dirty = [ln for ln in out.splitlines() if ln.strip()]
        if any(_porcelain_path(ln) == LOG_REL for ln in dirty) and _log_is_own_appends():
            dirty = [ln for ln in dirty if _porcelain_path(ln) != LOG_REL]
        if dirty:
            raise BlindingError("participation/ has uncommitted changes; the confirm half needs a clean tree: "
                                + "; ".join(dirty[:5]))
        if _git("diff", "--quiet", e_sha, "HEAD", "--", "code")[0] != 0:
            raise BlindingError(f"participation/code differs from {E_FREEZE}; the look runs the frozen code only")
        allowed = set(COUNTRIES)
    if geos is not None:
        if len(geos) == 0:
            raise BlindingError("geos must be an explicit, non-empty list (an unfiltered query returns every country)")
        if allowed is not None:
            outside = sorted(set(geos) - allowed)
            if outside:
                raise BlindingError(f"half={half!r} may not read {outside}")


def _manifest_dimensions(code: str) -> set[str] | None:
    """The dimensions data/manifest.json records for this dataset (None if the dataset is not in it)."""
    try:
        entries = json.load(open(MANIFEST_JSON, encoding="utf-8"))["entries"]
    except (OSError, ValueError, KeyError):
        return None
    dims = [set(m["dimensions"]) for m in entries if m.get("dataset") == code]
    return set().union(*dims) if dims else None


def _check_query(code, filters, geos, since):
    if not isinstance(code, str) or not _CODE.fullmatch(code.lower()):
        raise BlindingError(f"dataset code {code!r} is not a plain Eurostat code")
    if isinstance(geos, str) or not all(isinstance(g, str) and _GEO.fullmatch(g) for g in geos):
        raise BlindingError(f"geos must be a list of Eurostat geo codes, not {geos!r}")
    canon = {}
    for k, v in filters.items():
        if (not isinstance(k, str) or not _CODE.fullmatch(k) or k in FORBIDDEN_KEYS or "period" in k.lower()
                or k.lower().startswith(FORBIDDEN_PREFIXES)):
            raise BlindingError(f"filter key {k!r} not allowed (geo and years are arguments of get)")
        vals = [v] if isinstance(v, str) else list(v)
        if not vals or not all(isinstance(x, str) and _VALUE.fullmatch(x) for x in vals):
            raise BlindingError(f"filter {k}={v!r} is not a list of plain codes")
        if k == "freq" and vals != ["A"]:
            raise BlindingError(f"annual data only, not freq={v!r}")
        canon[k] = sorted(set(vals))
    dims = _manifest_dimensions(code.lower())
    if dims is not None:
        extra = sorted(set(canon) - (dims - {"geo"}))
        if extra:
            raise BlindingError(f"filter keys {extra} are not dimensions of {code} (data/manifest.json: {sorted(dims)})")
    if since is not None and (isinstance(since, bool) or not isinstance(since, (int, np.integer))):
        raise BlindingError(f"since must be an int year or None, not {since!r}")
    return code.lower(), canon, sorted(set(geos)), (None if since is None else int(since))


# ---------------------------------------------------------------- JSON-stat

def parse(payload: dict) -> pd.DataFrame:
    """JSON-stat 2.0 dataset -> long frame: geo, year, value, flag + the other dimensions (annual only)."""
    if not isinstance(payload, dict) or "id" not in payload or "value" not in payload:
        raise ValueError(f"not a JSON-stat dataset: {str(payload)[:300]}")
    ids, size = list(payload["id"]), [int(s) for s in payload["size"]]
    if len(ids) != len(size) or "geo" not in ids or "time" not in ids:
        raise ValueError(f"unexpected dimensions {ids} / sizes {size}")
    codes = []
    for d, n in zip(ids, size):
        cat = payload["dimension"][d]["category"]
        idx = cat.get("index", list(cat.get("label", {})))
        if isinstance(idx, dict):
            order = [None] * len(idx)
            for c, i in idx.items():
                order[int(i)] = c
        else:
            order = list(idx)
        if len(order) != n or any(c is None for c in order):
            raise ValueError(f"dimension {d}: {len(order)} categories for size {n}")
        codes.append(np.array(order, dtype=object))
    n = int(np.prod(size))
    value = np.full(n, np.nan)
    flag = np.full(n, "", dtype=object)
    v = payload["value"]
    for k, x in (v.items() if isinstance(v, dict) else enumerate(v)):
        if x is not None:
            value[int(k)] = float(x)
    s = payload.get("status") or {}
    if isinstance(s, str):
        flag[:] = s.strip()
    else:
        for k, x in (s.items() if isinstance(s, dict) else enumerate(s)):
            if x is not None:
                flag[int(k)] = str(x).strip()
    pos = np.unravel_index(np.arange(n), size) if n else [np.array([], dtype=int)] * len(ids)
    df = pd.DataFrame({d: codes[j][pos[j]] for j, d in enumerate(ids)})
    if "freq" in df and not (df["freq"] == "A").all():
        raise ValueError(f"annual data only; freq {sorted(set(df['freq']))}")
    times = df["time"].astype(str)
    if not times.str.fullmatch(r"\d{4}").all():
        raise ValueError(f"annual data only; time codes such as {sorted(set(times))[:3]}")
    out = pd.DataFrame({"geo": df["geo"].astype(str), "year": times.astype(int), "value": value,
                        "flag": pd.Series(flag, dtype=object).astype(str)})
    for d in ids:
        if d not in ("geo", "time", "freq"):
            out[d] = df[d].astype(str)
    return out


# ---------------------------------------------------------------- fetch

def _url(code, filters, geos, since) -> str:
    params = [("format", "JSON"), ("lang", "EN")] + [(k, x) for k in sorted(filters) for x in filters[k]]
    params += [("geo", g) for g in geos] + ([("sinceTimePeriod", str(since))] if since is not None else [])
    return requests.Request("GET", API + code, params=params).prepare().url


def _download(url: str) -> bytes:
    r = requests.get(url, headers=UA, timeout=300)
    if r.status_code != 200:
        raise RuntimeError(f"Eurostat HTTP {r.status_code} for {url}: {r.text[:300]}")
    return r.content


def _log(entry: dict) -> None:
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    line = json.dumps(entry, sort_keys=True) + "\n"
    with open(LOG, "a", encoding="utf-8", newline="\n") as f:
        f.write(line)
    _APPENDED.append(line)


def _logged(sha256: str, half: str, dataset: str) -> bool:
    """A non-rejected download with this hash, half and dataset is in the fetch log (C10)."""
    if not os.path.exists(LOG):
        return False
    for ln in open(LOG, encoding="utf-8"):
        if ln.strip():
            e = json.loads(ln)
            if (e.get("sha256"), e.get("half"), e.get("dataset")) == (sha256, half, dataset) and "rejected" not in e:
                return True
    return False


def _frame(raw: bytes, geos: list[str]) -> pd.DataFrame:
    df = parse(json.loads(raw))
    extra = sorted(set(df["geo"]) - set(geos))
    if extra:
        raise BlindingError(f"the response holds countries that were not requested: {extra}")
    return df


def get(code: str, filters: dict, geos: list[str], half: str, since: int | None = None) -> pd.DataFrame:
    """Guarded, cached, logged fetch of an annual Eurostat dataset for these countries; long format."""
    code, filters, geos, since = _check_query(code, filters, geos, since)
    guard(half, geos, code, filters, since)
    query = json.dumps({"dataset": code, "filters": filters, "geos": geos, "since": since},
                       sort_keys=True, separators=(",", ":"))
    path = os.path.join(RAW, half, f"{code}__{hashlib.sha1(query.encode()).hexdigest()[:12]}.json")
    if os.path.exists(path):
        with open(path, "rb") as f:
            raw = f.read()
        if not _logged(hashlib.sha256(raw).hexdigest(), half, code):
            raise BlindingError(f"cached {os.path.relpath(path, ROOT)} has no matching download in the fetch log "
                                "(C10); delete it and fetch through get()")
        return _frame(raw, geos)
    url = _url(code, filters, geos, since)
    raw = _download(url)
    head = _git("rev-parse", "HEAD")
    entry = {"dataset": code, "url": url, "utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
             "half": half, "geos": geos, "sha256": hashlib.sha256(raw).hexdigest(),
             "head_commit": head[1].strip() if head[0] == 0 else None}
    try:
        df = _frame(raw, geos)
    except Exception as e:                                    # downloaded but refused: logged, never cached
        _log({**entry, "rejected": f"{type(e).__name__}: {e}"[:500]})
        raise
    _log(entry)                                               # the log first: no cache file without its record
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(raw)
    return df


# ---------------------------------------------------------------- flags (C3, C4)

def is_break(flag) -> bool:
    return "b" in str(flag or "")


def is_unreliable(flag) -> bool:
    f = str(flag or "")
    return "u" in f or "c" in f


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """C4: a copy with value NaN where the flag marks low reliability (u) or confidentiality (c); flags are kept,
    so a 'bu' cell still counts as a break under C3."""
    out = df.copy()
    out.loc[out["flag"].map(is_unreliable).astype(bool), "value"] = np.nan
    return out


def break_years(df: pd.DataFrame) -> dict[str, list[int]]:
    """C3: for each country, the sorted years with a break flag anywhere in this frame."""
    b = df[df["flag"].map(is_break).astype(bool)]
    return {g: sorted(int(y) for y in set(s)) for g, s in b.groupby("geo")["year"]}


__all__ = ["BlindingError", "COUNTRIES", "STRATA", "HALVES", "DESIGN_DATASETS", "DESIGN_QUERIES", "get", "guard",
           "parse", "is_break", "is_unreliable", "clean", "break_years", "frozen_split"]
