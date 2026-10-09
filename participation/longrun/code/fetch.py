# fetch.py — the one door to long-run data (longrun/PROTOCOL.md L14), with the blinding guard built in.
#
# Every download of the long-run study goes through this module and is logged in longrun/data/fetch_log.jsonl (source,
# url, UTC time, half, countries, SHA-256 of the bytes, HEAD commit). Raw files are cached under longrun/data/raw/<half>/
# (gitignored); a cached file is served only if the log holds a non-rejected download of it with the same SHA-256, half
# and source, and the log line is written before the cache file. The IPUMS extract is not downloaded: she places it in
# longrun/data/ipums/ (gitignored) and code/ipums.py is its only reader, under the same guard (guard() below).
#
# Halves (what each door may serve, and when):
#   meta    — OECD SDMX structure and availability messages (dataflow, datastructure, codelist, availableconstraint):
#             no values, no observation flags. Any time. The URL is checked to be one of those endpoints, and the
#             response to be a structure message (a data message is refused and logged as rejected).
#   doc     — documentation from the allowlist DOCS (PDF/HTML notes, sample lists, codebooks). Any time.
#   design  — the design covariate of section 4, exactly one: UN WPP2024 total population on 1 July 1960 of the 38
#             members (L12, the stated L3 exception). The WPP file covers every country and year; the loader returns
#             the 1960 totals of the members and nothing else.
#   explore — tag participation-L-freeze exists and is an ancestor of HEAD; countries within data/split.json 'explore'
#             as committed in that tag (the working copy must agree).
#   confirm — tags participation-L-freeze and participation-LE-freeze exist, L an ancestor of LE, both of HEAD; the frozen
#             split; `git status --porcelain -- longrun/` clean bar this process's own fetch-log lines; longrun/code
#             unchanged since the LE tag; participation/code unchanged since participation-E-freeze; countries within
#             the 38 members (aggregates and non-members refused).
# Value doors (explore/confirm): OECD SDMX data (oecd), the JST file (jst), ILOSTAT (ilostat), WPP by age (wpp_age),
# Giuliano-Nunn (giuliano_nunn), Kholodilin (kholodilin; its file is confirmed at L2), DBnomics and Census for the US
# deep study (dbnomics, census_us; US only). Rules applied at the door, before any network call or cache read:
#   - unseen cells only (L1): a European country's rows end at 1994 (outcome) or 1993 (q, which enters lagged); the
#     European study's 1995-1996 rows were seen (its panel grid starts in 1995 and its exploration outputs hold
#     1995-1996 rows: the review of 2026-10-09), so they are not long-run cells. The OECD query carries endPeriod
#     accordingly, and single-file loaders cut their rows the same way;
#   - L2 is applied in build.py (it drops observation years; the q of 1990 is needed for 1991);
#   - single-file sources (JST, ILOSTAT, WPP, Giuliano-Nunn, Kholodilin): the loader parses the file and returns only
#     the rows of the half's countries (row-level guard, L14) and only the named columns;
#   - order at each opening (L14): an outcome door (OECD LFS, ILOSTAT school) opens only after (1) a logged download
#     of a q source for that half, (2) then a knots record for that half written by opening.open_half whose payload
#     lists the requested countries, (3) then an F_L record for that half written by ipums.F_L (record(..., by=...));
#     a stray record without these marks opens nothing;
#   - pinned inputs (both halves): data/segments.csv, data/coverage.json, data/skeleton.json, data/split.json,
#     data/ipums_samples.json and PROTOCOL.md in the working copy equal their copies in the L-freeze commit, and
#     FORECASTS.md differs from its L copy only by added E-L rows;
#   - a ready freeze (both halves): the L-freeze commit holds a production data/skeleton.json (quick false), filled
#     forecast sheets for every participant, a results/europe_run_*.json, data/segments.csv and a data/seen.json that
#     records where the scouts' folders were moved (PROTOCOL section 7); a premature tag opens nothing.
#
# Library module (no run line). Checked by checks/check_guard.py.

from __future__ import annotations

import gzip
import hashlib
import io
import json
import os
import re
import subprocess
from datetime import datetime, timezone
from urllib.parse import urlencode, urlparse

import numpy as np
import pandas as pd
import truststore

truststore.inject_into_ssl()
import requests  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
LROOT = os.path.dirname(HERE)                                  # participation/longrun/
PROOT = os.path.dirname(LROOT)                                 # participation/
RAW = os.path.join(LROOT, "data", "raw")                       # gitignored
IPUMS_DIR = os.path.join(LROOT, "data", "ipums")               # gitignored; her extract
LOG = os.path.join(LROOT, "data", "fetch_log.jsonl")           # committed (L14)
SPLIT = os.path.join(LROOT, "data", "split.json")
LOG_REL = "participation/longrun/data/fetch_log.jsonl"
UA = {"User-Agent": "Mozilla/5.0 (research; laborformal)"}
OECD_REST = "https://sdmx.oecd.org/public/rest/"

L_FREEZE, LE_FREEZE = "participation-L-freeze", "participation-LE-freeze"
E_FREEZE = "participation-E-freeze"                            # the European freeze: participation/code frozen there
HALVES = ("meta", "doc", "design", "explore", "confirm")

# ---------------------------------------------------------------- countries (L1, L2, section 4)

# The 38 OECD members of 2026, in the European protocol's two-letter codes (EL Greece, UK United Kingdom).
ISO3 = {"AT": "AUT", "AU": "AUS", "BE": "BEL", "CA": "CAN", "CH": "CHE", "CL": "CHL", "CO": "COL", "CR": "CRI",
        "CZ": "CZE", "DE": "DEU", "DK": "DNK", "EE": "EST", "EL": "GRC", "ES": "ESP", "FI": "FIN", "FR": "FRA",
        "HU": "HUN", "IE": "IRL", "IL": "ISR", "IS": "ISL", "IT": "ITA", "JP": "JPN", "KR": "KOR", "LT": "LTU",
        "LU": "LUX", "LV": "LVA", "MX": "MEX", "NL": "NLD", "NO": "NOR", "NZ": "NZL", "PL": "POL", "PT": "PRT",
        "SE": "SWE", "SI": "SVN", "SK": "SVK", "TR": "TUR", "UK": "GBR", "US": "USA"}
FROM_ISO3 = {v: k for k, v in ISO3.items()}
COUNTRIES = sorted(ISO3)
# L1: the members among the European protocol's 31 (BG, HR, CY, MT, RO are not members and never enter).
EUROPEAN = sorted("AT BE CZ DE DK EE EL ES FI FR HU IE IT LT LU LV NL PL PT SE SI SK NO IS CH UK".split())
NON_EUROPEAN = sorted(set(COUNTRIES) - set(EUROPEAN))
# L2: the state-socialist administered-rent years, observation years up to 1990 (East Germany: DE uses DEU_F, L4).
TRANSITION = sorted("CZ SK HU PL EE LV LT SI".split())
TRANSITION_LAST = 1990
EUROPEAN_LAST = 1994                                           # L1 (1995-1996 were seen by the European study)
FIRST_YEAR, LAST_YEAR = 1950, 2025
DROPPED_YEARS = (2020, 2021)                                   # L1 (as C2)
# Section 4, in the protocol's order (split.py draws in this order); 'Other' takes any other member that enters.
STRATA = {
    "Nordic": ["DK", "FI", "NO", "SE", "IS"],
    "Continental": ["AT", "BE", "CH", "DE", "FR", "LU", "NL"],
    "Anglo": ["IE", "UK", "US", "CA", "AU", "NZ"],
    "South": ["ES", "IT", "PT", "EL"],
    "Asia": ["JP", "KR"],
    "Latin America": ["MX", "CL", "CO", "CR"],
    "Other": ["IL", "TR"],
}
FORCED_EXPLORE = "US"                                          # section 4
assert len(COUNTRIES) == 38 and len(EUROPEAN) == 26 and len(NON_EUROPEAN) == 12
assert set(EUROPEAN) | set(NON_EUROPEAN) == set(COUNTRIES)


def stratum_of(c: str) -> str:
    for s, cs in STRATA.items():
        if c in cs:
            return s
    return "Other"


def last_obs_year(c: str) -> int:
    """L1: the last observation year a country may contribute."""
    return EUROPEAN_LAST if c in EUROPEAN else LAST_YEAR


def is_unseen(c: str, year: int) -> bool:
    """L1 and L2: whether observation year `year` of country c is an unseen, admissible cell."""
    if c not in ISO3 or not (FIRST_YEAR <= year <= last_obs_year(c)):
        return False
    if c in NON_EUROPEAN and year in DROPPED_YEARS:
        return False
    if c in TRANSITION and year <= TRANSITION_LAST:
        return False
    return True


def window(c: str) -> list[int]:
    """The country's admissible observation years (L1, L2)."""
    return [y for y in range(FIRST_YEAR, LAST_YEAR + 1) if is_unseen(c, y)]


# ---------------------------------------------------------------- the guard

_APPENDED: list[str] = []


class BlindingError(Exception):
    """A request the long-run pre-registration does not allow at this point."""


def _git(*args: str) -> tuple[int, str]:
    """git in longrun/; (return code, stdout). Monkeypatched by the checks to simulate tags."""
    r = subprocess.run(["git", *args], cwd=LROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return r.returncode, r.stdout


def _tag_sha(tag: str) -> str:
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


def frozen_split(l_sha: str | None = None) -> dict:
    """longrun/data/split.json as committed in the L-freeze tag; the working copy, if present, must agree with it."""
    l_sha = _tag_sha(L_FREEZE) if l_sha is None else l_sha
    rc, out = _git("show", f"{l_sha}:./data/split.json")
    if rc != 0:
        raise BlindingError(f"data/split.json is not in the {L_FREEZE} commit; the split is frozen with the protocol")
    frozen = json.loads(out)
    if os.path.exists(SPLIT):
        here = json.load(open(SPLIT, encoding="utf-8"))
        if (here.get("explore"), here.get("confirm")) != (frozen["explore"], frozen["confirm"]):
            raise BlindingError("data/split.json differs from its frozen copy; the split never changes after the freeze")
    return frozen


def _porcelain_path(line: str) -> str:
    return line[3:].split(" -> ")[-1].strip().strip('"').replace("\\", "/")


def _log_is_own_appends() -> bool:
    if not _APPENDED:
        return False
    rc, out = _git("show", "HEAD:./data/fetch_log.jsonl")
    committed = out.splitlines() if rc == 0 else []
    try:
        working = open(LOG, encoding="utf-8").read().splitlines()
    except OSError:
        return False
    return working == committed + [ln.rstrip("\n") for ln in _APPENDED]


PINNED = ["data/segments.csv", "data/coverage.json", "data/skeleton.json", "data/split.json",
          "data/ipums_samples.json", "PROTOCOL.md"]
FORECASTS_REL = "FORECASTS.md"
FORECASTS_PATH = os.path.join(LROOT, FORECASTS_REL)               # the working copy (checks may point it elsewhere)
_READY: dict = {}


def _show(sha: str, rel: str) -> str | None:
    rc, out = _git("show", f"{sha}:./{rel}")
    return out if rc == 0 else None


def forecast_rows(text: str) -> dict:
    """{participant: {test id: cells}} from the forecast sheets (the participant sections, not the E-L table)."""
    out, who = {}, None
    for ln in text.splitlines():
        if ln.startswith("## "):
            who = None if ln.startswith("## E-L") else ln[3:].strip()
            continue
        if who and (ln.startswith("| LR-") or ln.startswith("| C-6L")):
            cells = [c.strip() for c in ln.strip().strip("|").split("|")]
            out.setdefault(who, {})[cells[0].split(":")[0].strip()] = cells
    return out


def forecasts_filled(text: str) -> tuple[bool, str]:
    """Every participant's rows carry numbers (P(model's sign), P(supported), P(contradicted)); LR-C1 may read
    'dropped' (no Extract B)."""
    rows = forecast_rows(text)
    if not rows:
        return False, "no participant sections"
    for who, r in rows.items():
        for t, cells in r.items():
            if t == "LR-C1" and any("dropped" in c.lower() for c in cells):
                continue
            try:
                [float(cells[i]) for i in (3, 4, 5)]
            except (ValueError, IndexError):
                return False, f"{who}: row {t} is not filled"
    return True, ""


def forecasts_append_only(frozen: str, now: str) -> bool:
    """FORECASTS.md may only gain E-L rows after the L-freeze: every frozen line stays, in order, and every added line
    is a table row inside the E-L section."""
    a = frozen.replace("\r\n", "\n").splitlines()
    b = now.replace("\r\n", "\n").splitlines()
    i, in_el = 0, False
    for ln in b:
        if i < len(a) and ln == a[i]:
            in_el = in_el or ln.startswith("## E-L")
            i += 1
            continue
        if not (in_el and ln.startswith("|")):
            return False
    return i == len(a)


def freeze_ready(l_sha: str) -> None:
    """A premature or incomplete L tag opens nothing (see the header)."""
    if _READY.get(l_sha):
        return
    sk = _show(l_sha, "data/skeleton.json")
    try:
        skj = json.loads(sk) if sk else None
    except ValueError:
        skj = None
    if not skj or skj.get("quick", True):
        raise BlindingError(f"the {L_FREEZE} commit holds no production data/skeleton.json (quick false)")
    ok, why = forecasts_filled(_show(l_sha, FORECASTS_REL) or "")
    if not ok:
        raise BlindingError(f"the {L_FREEZE} commit holds no filled forecast sheets ({why})")
    rc, out = _git("ls-tree", "--name-only", l_sha, "results/")
    if rc != 0 or not any(re.search(r"europe_run_[0-9a-f]+\.json$", ln) for ln in out.splitlines()):
        raise BlindingError(f"the {L_FREEZE} commit holds no results/europe_run_*.json (PROTOCOL section 5, L3)")
    if _show(l_sha, "data/segments.csv") is None:
        raise BlindingError(f"the {L_FREEZE} commit holds no data/segments.csv")
    seen = _show(l_sha, "data/seen.json")
    try:
        moved = ((json.loads(seen) or {}).get("scouts_folders") or {}).get("moved_to") if seen else None
    except ValueError:
        moved = None
    if not moved:
        raise BlindingError(f"the {L_FREEZE} commit's data/seen.json does not record where the scouts' folders were "
                            "moved (PROTOCOL section 7)")
    _READY[l_sha] = True


def pinned_unchanged(l_sha: str) -> None:
    """The frozen inputs in the working copy equal their L-freeze copies; FORECASTS.md only gains E-L rows."""
    if _git("diff", "--quiet", l_sha, "--", *PINNED)[0] != 0:
        raise BlindingError(f"a frozen input differs from its {L_FREEZE} copy ({', '.join(PINNED)}): the segment "
                            "table, coverage decisions, skeleton, split, sample list and protocol are frozen")
    frozen = _show(l_sha, FORECASTS_REL)
    path = FORECASTS_PATH
    now = open(path, encoding="utf-8").read() if os.path.exists(path) else None
    if frozen is None or now is None or not forecasts_append_only(frozen, now):
        raise BlindingError("FORECASTS.md may only gain E-L rows after the L-freeze")


def allowed_countries(half: str) -> set[str]:
    """The countries a value door may serve to this half now; BlindingError if the half is closed."""
    if half == "explore":
        l_sha = _tag_is_ancestor(L_FREEZE)
        freeze_ready(l_sha)
        pinned_unchanged(l_sha)
        return set(frozen_split(l_sha)["explore"])
    if half == "confirm":
        l_sha = _tag_is_ancestor(L_FREEZE)
        le_sha = _tag_is_ancestor(LE_FREEZE)
        if not _is_ancestor(l_sha, le_sha):
            raise BlindingError(f"tag {L_FREEZE} is not an ancestor of {LE_FREEZE}: L is frozen before LE")
        freeze_ready(l_sha)
        frozen_split(l_sha)
        rc, out = _git("status", "--porcelain", "--untracked-files=all", "--", ".")
        if rc != 0:
            raise BlindingError("git status failed; the confirm half needs a clean, committed longrun/")
        dirty = [ln for ln in out.splitlines() if ln.strip()]
        if any(_porcelain_path(ln) == LOG_REL for ln in dirty) and _log_is_own_appends():
            dirty = [ln for ln in dirty if _porcelain_path(ln) != LOG_REL]
        if dirty:
            raise BlindingError("longrun/ has uncommitted changes; the confirm half needs a clean tree: "
                                + "; ".join(dirty[:5]))
        pinned_unchanged(l_sha)
        if _git("diff", "--quiet", le_sha, "HEAD", "--", "code")[0] != 0:
            raise BlindingError(f"longrun/code differs from {LE_FREEZE}; the look runs the frozen code only")
        e_sha = _tag_sha(E_FREEZE)
        if _git("diff", "--quiet", e_sha, "HEAD", "--", "../code")[0] != 0:
            raise BlindingError(f"participation/code differs from {E_FREEZE}; it is imported unedited")
        return set(COUNTRIES)
    raise BlindingError(f"value doors serve 'explore' or 'confirm', not {half!r}")


def guard(half: str, geos: list[str] | None = None, source: str | None = None) -> set[str]:
    """Raise BlindingError unless this value source may be read now by this half, for these countries; returns the
    allowed set. Outcome sources also need the half's knots and F_L read recorded first (L14)."""
    if half not in ("explore", "confirm"):
        raise BlindingError(f"value doors serve 'explore' or 'confirm' (meta, doc and design have their own doors), "
                            f"not {half!r}")
    if source is not None and source not in SOURCES:
        raise BlindingError(f"unknown source {source!r}")
    allowed = allowed_countries(half)
    if geos is not None:
        if isinstance(geos, str) or len(geos) == 0:
            raise BlindingError("geos must be an explicit, non-empty list of member codes")
        outside = sorted(set(geos) - allowed)
        if outside:
            raise BlindingError(f"half={half!r} may not read {outside}")
        if source is not None and SOURCES[source].get("only") and set(geos) - set(SOURCES[source]["only"]):
            raise BlindingError(f"source {source} serves only {SOURCES[source]['only']}")
    if source is not None and SOURCES[source]["role"] == "outcome":
        why = order_open(half, geos)
        if why:
            raise BlindingError(f"L14: {why} (q first, knots from q alone, F_L, then outcomes)")
    return allowed


Q_SOURCES = ("oecd_rpi", "oecd_cpi", "oecd_cpi2018", "jst")
KNOTS_BY, F_L_BY = "opening.open_half", "ipums.F_L"


def order_open(half: str, geos=None) -> str:
    """'' if L14's order holds for this half (a logged q download, then a knots record by the opening covering these
    countries, then an F_L record by the IPUMS loader); else what is missing."""
    log = list(_entries())
    q_at = [i for i, e in enumerate(log) if e.get("half") == half and e.get("source") in Q_SOURCES
            and "rejected" not in e and "record" not in e]
    if not q_at:
        return f"no q download is logged for the {half} half"
    kn_at = [i for i, e in enumerate(log) if e.get("record") == "knots" and e.get("half") == half
             and e.get("by") == KNOTS_BY and i > q_at[0]
             and (geos is None or set(geos) <= set((e.get("payload") or {}).get("geos", [])))]
    if not kn_at:
        return (f"no knots record of the {half} half by {KNOTS_BY}, after its q download, covering "
                f"{sorted(geos) if geos else 'these countries'}")
    fl_at = [i for i, e in enumerate(log) if e.get("record") == "F_L" and e.get("half") == half
             and e.get("by") == F_L_BY and i > kn_at[0]]
    if not fl_at:
        return f"no F_L record of the {half} half by {F_L_BY} after its knots record"
    return ""


# ---------------------------------------------------------------- the log and the cache

def _head() -> str | None:
    rc, out = _git("rev-parse", "HEAD")
    return out.strip() if rc == 0 else None


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _log(entry: dict) -> None:
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    line = json.dumps(entry, sort_keys=True) + "\n"
    with open(LOG, "a", encoding="utf-8", newline="\n") as f:
        f.write(line)
    _APPENDED.append(line)


def _entries():
    if not os.path.exists(LOG):
        return
    for ln in open(LOG, encoding="utf-8"):
        if ln.strip():
            yield json.loads(ln)


def _logged(sha256: str, half: str, source: str) -> bool:
    return any((e.get("sha256"), e.get("half"), e.get("source")) == (sha256, half, source) and "rejected" not in e
               for e in _entries())


def record(kind: str, half: str, payload, by: str | None = None) -> str:
    """Write a record (knots, F_L, H) to the fetch log with the SHA-256 of its canonical JSON; returns the hash. `by`
    names the writer (the order guard counts only the opening's knots and the IPUMS loader's F_L)."""
    if kind not in ("knots", "F_L", "H"):
        raise ValueError(f"record kind {kind!r}")
    blob = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    sha = hashlib.sha256(blob).hexdigest()
    _log({"record": kind, "half": half, "sha256": sha, "utc": _now(), "head_commit": _head(), "payload": payload,
          "by": by})
    return sha


def recorded(kind: str, half: str) -> list[dict]:
    return [e for e in _entries() if e.get("record") == kind and e.get("half") == half]


def _recorded(kind: str, half: str) -> bool:
    return bool(recorded(kind, half))


def _cache_path(half: str, source: str, query: dict, ext: str) -> str:
    q = json.dumps(query, sort_keys=True, separators=(",", ":"))
    return os.path.join(RAW, half, f"{source}__{hashlib.sha1(q.encode()).hexdigest()[:12]}{ext}")


def _download(url: str, headers: dict | None = None, timeout: int = 300) -> bytes:
    r = requests.get(url, headers={**UA, **(headers or {})}, timeout=timeout)
    if r.status_code == 404 and url.startswith(OECD_REST + "data/"):
        return b""                                            # SDMX NoResultsFound: an empty answer, logged as such
    if r.status_code != 200:
        raise RuntimeError(f"HTTP {r.status_code} for {url}: {r.text[:300]}")
    return r.content


def _cached_or_fetch(half: str, source: str, query: dict, url: str, ext: str, validate, headers=None,
                     geos=None) -> bytes:
    """The bytes of this query: from the cache if its download is logged, else downloaded, validated, logged, cached."""
    path = _cache_path(half, source, query, ext)
    if os.path.exists(path):
        raw = open(path, "rb").read()
        if not _logged(hashlib.sha256(raw).hexdigest(), half, source):
            raise BlindingError(f"cached {os.path.relpath(path, LROOT)} has no matching download in the fetch log "
                                "(L14); delete it and fetch through this module")
        return raw
    raw = _download(url, headers)
    entry = {"source": source, "url": url, "utc": _now(), "half": half, "geos": sorted(geos) if geos else None,
             "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw), "head_commit": _head()}
    try:
        validate(raw)
    except Exception as e:                                    # downloaded but refused: logged, never cached
        _log({**entry, "rejected": f"{type(e).__name__}: {e}"[:500]})
        raise
    _log(entry)                                               # the log first: no cache file without its record
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        f.write(raw)
    return raw


# ---------------------------------------------------------------- meta and doc doors

_META = re.compile(r"https://sdmx\.oecd\.org/public/rest/(availableconstraint|dataflow|datastructure|codelist)/"
                   r"[A-Za-z0-9_.,@+/\-]*(\?[A-Za-z0-9_=&.\-]*)?")
STRUCTURE_ACCEPT = {"Accept": "application/vnd.sdmx.structure+json; charset=utf-8; version=1.0"}


def _is_structure(raw: bytes) -> None:
    d = json.loads(raw)
    data = d.get("data", {})
    if not isinstance(data, dict) or "dataSets" in data or "observations" in raw.decode("utf-8", "replace")[:100000]:
        raise BlindingError("a metadata request returned a data message")
    if not any(k in data for k in ("contentConstraints", "dataflows", "dataStructures", "codelists")):
        raise ValueError("not an SDMX structure message")


def meta(url: str) -> dict:
    """An OECD SDMX structure or availability message (no values). Cached and logged with half 'meta'."""
    if not isinstance(url, str) or not _META.fullmatch(url) or "/data/" in url:
        raise BlindingError(f"the meta door serves OECD structure and availability endpoints only, not {url!r}")
    raw = _cached_or_fetch("meta", "oecd_meta", {"url": url}, url, ".json", _is_structure, STRUCTURE_ACCEPT)
    return json.loads(raw)


def availability(flow: str, key: str, year: int | None = None, component: str = "REF_AREA") -> list[str]:
    """The codes of `component` that hold at least one observation for this key (one year if given): an
    availableconstraint probe (mode=exact). Returns [] when the probe finds nothing."""
    q = {"mode": "exact"}
    if year is not None:
        q.update(startPeriod=str(year), endPeriod=str(year))
    url = f"{OECD_REST}availableconstraint/{flow}/{key}/all/{component}?{urlencode(q)}"
    try:
        msg = meta(url)
    except RuntimeError as e:
        if "HTTP 404" in str(e):                              # NoResultsFound: nothing available
            return []
        raise
    out = []
    for cc in msg.get("data", {}).get("contentConstraints", []):
        for reg in cc.get("cubeRegions", []):
            for kv in reg.get("keyValues", []):
                if kv.get("id") == component:
                    out += list(kv.get("values", []))
    return sorted(set(out))


# Documentation, by id (the doc door serves these and nothing else). 'what' says what it is read for.
DOCS = {
    "lfsnotes": dict(url="https://www.oecd.org/content/dam/oecd/en/data/datasets/employability-data/"
                         "LFSNOTES_SOURCES.pdf", ext=".pdf",
                     what="OECD LFS sources, coverage and definitions; Table 6 breaks in series (L7)"),
    "jst_rore_r6": dict(url="https://www.macrohistory.net/app/download/9918957869/JST_RORE_Documentation_R6.pdf"
                            "?t=1658254098", ext=".pdf",
                        what="JST R6 documentation of the 2016-2020 RORE update, Table 3 and footnotes (L3, L7)"),
    "rore": dict(url="https://www.macrohistory.net/app/download/9834516469/RORE_documentation.pdf?t=1614633099",
                 ext=".pdf", what="RORE documentation, section 2.4 rent indices by country (L6, L7)"),
    "jst_r6": dict(url="https://www.macrohistory.net/app/download/9834516169/JST_documentationR6.pdf?t=1676279836",
                   ext=".pdf", what="JST R6 documentation (variables, territorial changes)"),
    "ipums_samples": dict(url="https://international.ipums.org/international-action/samples", ext=".html",
                          what="IPUMS-I public sample list (L9, L10)"),
    "ipums_relate": dict(url="https://international.ipums.org/international-action/variables/RELATE", ext=".html",
                         what="IPUMS-I RELATE availability by sample (L9, L10)"),
    # bls.gov answers 403 from this machine (2026-10-09); the Internet Archive's captures of the same pages are used.
    "bls_cps_doc": dict(url="https://web.archive.org/web/20251231021947id_/https://www.bls.gov/cps/documentation.htm",
                        ext=".html", what="BLS CPS documentation page, capture of 2025-12-31 (section 6 segments)"),
    "bls_cps_methods": dict(url="https://web.archive.org/web/20260104101616id_/https://www.bls.gov/cps/"
                                "eetech_methods.pdf", ext=".pdf",
                            what="BLS 'Household data: technical note / methods' incl. historical comparability "
                                 "(L7 for the US; section 6 segments)"),
    "census_adults": dict(url="https://www.census.gov/data/tables/time-series/demo/families/adults.html",
                          ext=".html", what="Census historical living arrangements of adults (AD tables) and notes"),
    "census_enroll": dict(url="https://www.census.gov/data/tables/time-series/demo/school-enrollment/"
                                "cps-historical-time-series.html", ext=".html",
                          what="Census CPS historical school enrolment tables and notes"),
}


def doc(doc_id: str) -> bytes:
    """A documentation file from DOCS, cached and logged with half 'doc'."""
    if doc_id not in DOCS:
        raise BlindingError(f"the doc door serves {sorted(DOCS)}, not {doc_id!r}")
    d = DOCS[doc_id]
    return _cached_or_fetch("doc", f"doc_{doc_id}", {"url": d["url"]}, d["url"], d["ext"], lambda raw: None)


# ---------------------------------------------------------------- the design half: WPP 1960 population

WPP_TOTAL_URL = ("https://population.un.org/wpp/assets/Excel%20Files/1_Indicator%20(Standard)/CSV_FILES/"
                 "WPP2024_TotalPopulationBySex.csv.gz")
DESIGN_YEAR = 1960


def _gz_csv(raw: bytes, usecols=None) -> pd.DataFrame:
    return pd.read_csv(io.BytesIO(gzip.decompress(raw)), usecols=usecols, low_memory=False)


def population_1960(countries: list[str] | None = None) -> dict[str, float]:
    """L12: UN WPP2024 total population on 1 July 1960 (persons), Medium variant (the estimates), for these members.
    The only design covariate. Nothing else of the file is returned."""
    countries = COUNTRIES if countries is None else countries
    bad = sorted(set(countries) - set(COUNTRIES))
    if bad:
        raise BlindingError(f"the design covariate covers the 38 members only, not {bad}")

    def validate(raw):
        cols = set(pd.read_csv(io.BytesIO(gzip.decompress(raw)), nrows=0).columns)
        need = {"ISO3_code", "Time", "Variant", "PopTotal"}
        if not need <= cols:
            raise ValueError(f"WPP total population file lacks {sorted(need - cols)}")
    raw = _cached_or_fetch("design", "wpp_total", {"url": WPP_TOTAL_URL}, WPP_TOTAL_URL, ".csv.gz", validate,
                           geos=countries)
    df = _gz_csv(raw, usecols=["ISO3_code", "Time", "Variant", "PopTotal"])
    df = df[(df["Time"] == DESIGN_YEAR) & (df["Variant"] == "Medium")
            & df["ISO3_code"].isin([ISO3[c] for c in countries])]
    out = {FROM_ISO3[i]: float(v) * 1000.0 for i, v in zip(df["ISO3_code"], df["PopTotal"])}
    missing = sorted(set(countries) - set(out))
    if missing:
        raise RuntimeError(f"no 1960 WPP population for {missing}")
    return {c: out[c] for c in countries}


# ---------------------------------------------------------------- value sources

# role: 'outcome' (opens only after knots and F_L are recorded), 'regressor', 'moderator', 'control', 'us'.
SOURCES = {
    "oecd_lfs": dict(role="outcome", flow="OECD.ELS.SAE,DSD_LFS@DF_LFS_INDIC,1.1",
                     dims=["REF_AREA", "MEASURE", "UNIT_MEASURE", "SEX", "AGE", "LABOUR_FORCE_STATUS"],
                     what="activity and unemployment rates by sex and five-year age (L4, L5)"),
    "oecd_rpi": dict(role="regressor", flow="OECD.ECO.MPD,DSD_AN_HOUSE_PRICES@DF_HOUSE_PRICES,1.0",
                     dims=["REF_AREA", "FREQ", "MEASURE", "UNIT_MEASURE"],
                     what="analytical house prices: RPI (q rung 2) and HPI (q_hpi robustness)"),
    "oecd_cpi": dict(role="regressor", flow="OECD.SDD.TPS,DSD_PRICES@DF_PRICES_ALL,1.0",
                     dims=["REF_AREA", "FREQ", "METHODOLOGY", "MEASURE", "UNIT_MEASURE", "EXPENDITURE", "ADJUSTMENT",
                           "TRANSFORMATION"], what="all-items CPI, the denominator of q rung 2 (L6)"),
    "oecd_cpi2018": dict(role="regressor", flow="OECD.SDD.TPS,DSD_PRICES_COICOP2018@DF_PRICES_C2018_ALL,1.0",
                         dims=["REF_AREA", "FREQ", "METHODOLOGY", "MEASURE", "UNIT_MEASURE", "EXPENDITURE",
                               "ADJUSTMENT", "TRANSFORMATION"], what="all-items CPI, COICOP 2018 extension (L6)"),
    "jst": dict(role="regressor", url="https://www.macrohistory.net/app/download/9834512569/JSTdatasetR6.xlsx"
                                      "?t=1763503850",
                columns=["iso", "year", "hpnom", "housing_rent_yd", "housing_capgain", "housing_capgain_ipol",
                         "rent_ipolated", "cpi"], what="JST R6: the rent index and CPI of q rung 1 (L6)"),
    "ilostat": dict(role="outcome", url="https://rplumber.ilo.org/data/indicator/",
                    indicator="POP_3WAP_SEX_AGE_STU_NB_A", what="population 20-24 by school attendance (L11)"),
    "wpp_age": dict(role="control", url="https://population.un.org/wpp/assets/Excel%20Files/1_Indicator%20"
                                        "(Standard)/CSV_FILES/WPP2024_PopulationByAge5GroupSex_Medium.csv.gz",
                    what="population by five-year age: relative cohort size (L12, the L3 exception)"),
    "giuliano_nunn": dict(role="moderator", url="https://www.anderson.ucla.edu/documents/sites/faculty/"
                                                "review%20publications/research/"
                                                "Ancestral_Characteristics_Database_Complete_Version_1_1.xlsx",
                          what="ancestral extended-family domestic organisation, v8 (robustness F)"),
    "kholodilin": dict(role="control", url=None,
                       what="Kholodilin rental-regulation coding (L12); file confirmed at L2"),
    "dbnomics": dict(role="us", url="https://api.db.nomics.world/v22/series/", only=["US"],
                     what="US deep study: CPS (BLS/ln) and BEA NIPA T2.4.4 via DBnomics (section 6)"),
    "census_us": dict(role="us", only=["US"],
                      tables={"ad1": "https://www2.census.gov/programs-surveys/demo/tables/families/time-series/"
                                     "adults/ad1.xls",
                              "ad3_25_34": "https://www2.census.gov/programs-surveys/demo/tables/families/"
                                           "time-series/adults/ad3-25-34.xls",
                              "enroll02": "https://www2.census.gov/programs-surveys/demo/tables/school-enrollment/"
                                          "time-series/cps-historical-time-series/hst_enroll02.xlsx"},
                      what="US deep study: Census AD-1, AD-3 (25-34) and CPS October enrolment (section 6)"),
}
_CODE = re.compile(r"[A-Z0-9_]+")
AGGREGATE_AREAS = re.compile(r"(OECD|EU|EA|G7|G20|WLD|OECD_REP|EU27_2020|EA20|OECDE|NMEC)\w*")


def ref_area(c: str, source: str) -> str:
    """The REF_AREA code of a member in a source: DEU_F (former Federal Republic) for DE in the LFS flow (L4)."""
    if source == "oecd_lfs" and c == "DE":
        return "DEU_F"
    return ISO3[c]


def _cap(c: str, role: str) -> int:
    """L1: the last year a door returns for country c: the last observation year, one less for a lagged regressor."""
    last = last_obs_year(c)
    return last - 1 if role == "regressor" else last


def parse_sdmx_csv(raw: bytes, source: str) -> pd.DataFrame:
    """SDMX-CSV (dimensionAtObservation=AllDimensions) -> geo, year, value, flag + the source's other dimensions."""
    if not raw.strip():                                       # an empty answer (no observations)
        return pd.DataFrame(columns=["geo", "year", "value", "flag"]
                            + [d for d in SOURCES[source]["dims"] if d not in ("REF_AREA", "FREQ")])
    df = pd.read_csv(io.BytesIO(raw), dtype=str, keep_default_na=False)
    need = {"REF_AREA", "TIME_PERIOD", "OBS_VALUE"}
    if not need <= set(df.columns):
        raise ValueError(f"not SDMX-CSV with {sorted(need)}: columns {list(df.columns)[:12]}")
    t = df["TIME_PERIOD"].astype(str)
    if len(df) and not t.str.fullmatch(r"\d{4}").all():
        raise ValueError(f"annual data only; time codes such as {sorted(set(t))[:3]}")
    if "FREQ" in df and len(df) and not (df["FREQ"] == "A").all():
        raise ValueError("annual data only")
    back = {ref_area(c, source): c for c in COUNTRIES}
    unknown = sorted(set(df["REF_AREA"]) - set(back))
    if unknown:
        raise BlindingError(f"the response holds areas that are not requested members: {unknown}")
    out = pd.DataFrame({"geo": df["REF_AREA"].map(back), "year": t.astype(int),
                        "value": pd.to_numeric(df["OBS_VALUE"].replace("", np.nan), errors="coerce"),
                        "flag": (df["OBS_STATUS"] if "OBS_STATUS" in df else pd.Series("", index=df.index))
                        .astype(str)})
    for d in SOURCES[source]["dims"]:
        if d not in ("REF_AREA", "FREQ") and d in df:
            out[d] = df[d].astype(str)
    return out


def oecd(source: str, key: dict, geos: list[str], half: str) -> pd.DataFrame:
    """Guarded, cached, logged OECD SDMX data query. `key` pins every dimension but REF_AREA (and FREQ = A): values are
    one code or a list of codes. One query per year cap (L1): European members to 1994 (q flows 1993), others to 2025.
    Long format: geo, year, value, flag (OBS_STATUS) + the other dimensions."""
    if source not in SOURCES or "flow" not in SOURCES[source]:
        raise BlindingError(f"{source!r} is not an OECD source")
    s = SOURCES[source]
    guard(half, geos, source)
    dims = [d for d in s["dims"] if d != "REF_AREA"]
    if set(key) != set(dims) - {"FREQ"} and set(key) != set(dims):
        raise BlindingError(f"the key must pin every dimension of {source} but REF_AREA: {dims}, got {sorted(key)}")
    parts = []
    for d in s["dims"]:
        if d == "REF_AREA":
            continue
        v = key.get(d, "A" if d == "FREQ" else None)
        vals = [v] if isinstance(v, str) else list(v)
        if d == "FREQ" and vals != ["A"]:
            raise BlindingError("annual data only")
        if not vals or not all(isinstance(x, str) and _CODE.fullmatch(x) for x in vals):
            raise BlindingError(f"{d}={v!r} is not a list of plain codes")
        parts.append("+".join(sorted(set(vals))))
    frames = []
    by_cap: dict[int, list[str]] = {}
    for c in sorted(set(geos)):
        by_cap.setdefault(_cap(c, s["role"]), []).append(c)
    for cap, cs in sorted(by_cap.items()):
        refs = "+".join(ref_area(c, source) for c in cs)
        k = ".".join([refs] + parts)
        url = (f"{OECD_REST}data/{s['flow']}/{k}?" +
               urlencode({"startPeriod": str(FIRST_YEAR - 2), "endPeriod": str(cap),
                          "dimensionAtObservation": "AllDimensions"}))
        query = {"source": source, "key": k, "end": cap}

        def validate(raw, cs=cs):
            df = parse_sdmx_csv(raw, source)
            extra = sorted(set(df["geo"]) - set(cs))
            if extra:
                raise BlindingError(f"the response holds countries that were not requested: {extra}")
            if len(df) and df["year"].max() > cap:
                raise BlindingError(f"the response holds years after {cap}")
        raw = _cached_or_fetch(half, source, query, url, ".csv", validate,
                               {"Accept": "application/vnd.sdmx.data+csv; charset=utf-8"}, cs)
        frames.append(parse_sdmx_csv(raw, source))
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(columns=["geo", "year", "value", "flag"])


def _restrict(df: pd.DataFrame, geo_col: str, year_col: str | None, allowed: set[str], role: str,
              to_geo=FROM_ISO3.get) -> pd.DataFrame:
    """Row-level guard of a single-file source: only the allowed members' rows, cut at their L1 cap."""
    g = df[geo_col].map(to_geo)
    keep = g.isin(allowed)
    if year_col is not None:
        yr = pd.to_numeric(df[year_col], errors="coerce")
        cap = g.map(lambda c: _cap(c, role) if isinstance(c, str) else -1)
        keep &= yr.le(cap)
    out = df[keep].copy()
    out.insert(0, "geo", g[keep].to_numpy())
    return out


def jst(geos: list[str], half: str) -> pd.DataFrame:
    """JST R6, the q columns only, for these countries (row-level guard; European rows to 1993)."""
    s = SOURCES["jst"]
    allowed = guard(half, geos, "jst") & set(geos)

    def validate(raw):
        cols = set(pd.read_excel(io.BytesIO(raw), nrows=0).columns)
        if not set(s["columns"]) <= cols:
            raise ValueError(f"JST file lacks {sorted(set(s['columns']) - cols)}")
    raw = _cached_or_fetch(half, "jst", {"url": s["url"]}, s["url"], ".xlsx", validate, geos=geos)
    df = pd.read_excel(io.BytesIO(raw), usecols=s["columns"])
    return _restrict(df, "iso", "year", allowed, "regressor").drop(columns=["iso"])


def ilostat(geos: list[str], half: str) -> pd.DataFrame:
    """ILOSTAT POP_3WAP_SEX_AGE_STU_NB_A, both sexes, 20-24, every attendance status, one request per country."""
    s = SOURCES["ilostat"]
    guard(half, geos, "ilostat")
    frames = []
    for c in sorted(set(geos)):
        q = {"id": s["indicator"], "ref_area": ISO3[c], "sex": "SEX_T", "classif1": "AGE_YTHBANDS_Y20-24",
             "timefrom": str(FIRST_YEAR - 1), "timeto": str(_cap(c, "outcome")), "type": "code", "format": ".csv"}
        url = s["url"] + "?" + urlencode(q)

        def validate(raw, c=c):
            df = pd.read_csv(io.BytesIO(raw), dtype=str)
            if len(df) and set(df["ref_area"]) - {ISO3[c]}:
                raise BlindingError(f"ILOSTAT returned other areas: {sorted(set(df['ref_area']) - {ISO3[c]})}")
        raw = _cached_or_fetch(half, "ilostat", q, url, ".csv", validate, geos=[c])
        df = pd.read_csv(io.BytesIO(raw), dtype=str)
        frames.append(_restrict(df, "ref_area", "time", {c}, "outcome"))
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def wpp_age(geos: list[str], half: str) -> pd.DataFrame:
    """WPP2024 population by five-year age group (Medium), ages 25-64, for these countries."""
    s = SOURCES["wpp_age"]
    allowed = guard(half, geos, "wpp_age") & set(geos)
    raw = _cached_or_fetch(half, "wpp_age", {"url": s["url"]}, s["url"], ".csv.gz", lambda r: None, geos=geos)
    df = _gz_csv(raw, usecols=["ISO3_code", "Time", "AgeGrp", "AgeGrpStart", "PopTotal", "Variant"])
    df = df[(df["Variant"] == "Medium") & df["AgeGrpStart"].between(25, 60)]
    return _restrict(df, "ISO3_code", "Time", allowed, "control").drop(columns=["ISO3_code"])


def giuliano_nunn(geos: list[str], half: str, column: str = "v8") -> pd.DataFrame:
    """The Ancestral Characteristics Database: country code and the baseline column only (codes confirmed at L2)."""
    s = SOURCES["giuliano_nunn"]
    allowed = guard(half, geos, "giuliano_nunn") & set(geos)
    raw = _cached_or_fetch(half, "giuliano_nunn", {"url": s["url"]}, s["url"], ".xlsx", lambda r: None, geos=geos)
    df = pd.read_excel(io.BytesIO(raw))
    iso = next((c for c in df.columns if str(c).lower() in ("isocode", "iso3", "iso", "country_code")), None)
    cols = [c for c in df.columns if str(c).lower().startswith(column.lower())]
    if iso is None or not cols:
        raise RuntimeError(f"Giuliano-Nunn file: no ISO column or no {column} column; confirm the codes at L2")
    return _restrict(df[[iso] + cols], iso, None, allowed, "moderator").drop(columns=[iso])


def kholodilin(geos: list[str], half: str) -> pd.DataFrame:
    guard(half, geos, "kholodilin")
    raise RuntimeError("the Kholodilin file, its country list and codes are confirmed at L2 (PROTOCOL L12); until "
                       "then the control-era run and qualifier read 'control-era years not separable'")


def dbnomics(series: str, half: str) -> pd.DataFrame:
    """One DBnomics series for the US deep study ('BLS/ln/LNU01300164', 'BEA/NIPA-T20404/DTENRG-A')."""
    guard(half, ["US"], "dbnomics")
    if not re.fullmatch(r"(BLS/ln/LN[US]\d{8}|BEA/NIPA-T20404/[A-Z]+-A)", series):
        raise BlindingError(f"the US door serves BLS/ln participation and unemployment series and BEA NIPA T2.4.4 "
                            f"annual lines, not {series!r}")
    url = SOURCES["dbnomics"]["url"] + series + "?observations=1"

    def validate(raw):
        d = json.loads(raw)
        if not d.get("series", {}).get("docs"):
            raise ValueError(f"DBnomics: no series {series}")
    raw = _cached_or_fetch(half, "dbnomics", {"series": series}, url, ".json", validate, geos=["US"])
    doc0 = json.loads(raw)["series"]["docs"][0]
    df = pd.DataFrame({"period": doc0["period"], "value": pd.to_numeric(pd.Series(doc0["value"]), errors="coerce")})
    df.attrs["indexed_at"] = doc0.get("indexed_at")
    return df


def census_us(table: str, half: str) -> bytes:
    """A US Census table (bytes) for the deep study."""
    guard(half, ["US"], "census_us")
    t = SOURCES["census_us"]["tables"]
    if table not in t:
        raise BlindingError(f"the Census door serves {sorted(t)}, not {table!r}")
    ext = os.path.splitext(t[table])[1]
    return _cached_or_fetch(half, "census_us", {"table": table}, t[table], ext, lambda r: None, geos=["US"])


# ---------------------------------------------------------------- flags (L3, L7)

def is_break(flag) -> bool:
    """OECD OBS_STATUS B: a break in series (L7)."""
    return str(flag or "").strip().upper() == "B"


def is_not_measured(flag) -> bool:
    """L3: estimated, forecast or missing-coded cells are missing (OECD OBS_STATUS E, F, M)."""
    return str(flag or "").strip().upper() in ("E", "F", "M")


__all__ = ["BlindingError", "COUNTRIES", "EUROPEAN", "NON_EUROPEAN", "TRANSITION", "STRATA", "ISO3", "SOURCES",
           "DOCS", "guard", "meta", "availability", "doc", "population_1960", "oecd", "jst", "ilostat", "wpp_age",
           "giuliano_nunn", "kholodilin", "dbnomics", "census_us", "record", "recorded", "window", "is_unseen",
           "frozen_split", "is_break", "is_not_measured", "ref_area"]
