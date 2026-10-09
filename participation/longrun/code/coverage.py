# coverage.py — coverage decisions from metadata only (PROTOCOL section 3 'Testability, from coverage alone'; L2).
#
# Steps (each from metadata, documentation or a values-free availability probe; no value is fetched, read or printed):
#   probe     — OECD SDMX per-year availability probes (fetch.availability, mode=exact, startPeriod = endPeriod = year)
#               for every key a verdict test uses: activity rates F/M x Y25T29/Y30T34, U 25-54 (DF_LFS_INDIC); RPI
#               (DF_HOUSE_PRICES); all-items CPI (DF_PRICES_ALL, DF_PRICES_C2018_ALL). One probe per key and year returns
#               the REF_AREAs with an observation in that year; range queries are not used (they hide gaps).
#   ipums     — the frozen IPUMS-I sample list, parsed from the public sample list and the RELATE availability page (doc
#               door): F_L samples (census samples of members, 1955-1975, with RELATE) and Extract B samples (census
#               samples, 1976+, with RELATE, inside the unseen window), each with its public notes (persons not organised
#               into households; age grouped). Surveys (the survey list, and samples noted 'Household survey') excluded.
#   documented— coverage of the sources that publish no values-free availability, from their documentation as
#               transcribed in docs/data_inventory.md and PROTOCOL L6: JST (q rung 1) and ILOSTAT (C-6L). PROTOCOL
#               section 3 asks for values-dropping masks of these two files at L2; mask_jst/mask_ilostat below implement
#               them, but they download the value files, so they run only with --masks (her go-ahead), never by default.
#   eligibility — from the cube and data/segments.csv: q availability by the source ladder (L6, 'extend, don't fill'),
#               each country's chosen q segment (section 5), eligible observation years per verdict test, the test
#               memberships and family sizes (testability rules of section 3).
# Outputs: data/coverage.json (the availability cube: country x year x series, with each source's provenance) and
#          data/coverage_l2.csv (per country and test: eligible years, count, chosen q segment, member or not);
#          data/ipums_samples.json (the frozen sample list with its public notes); data/seen.json (every country x series
#          already on disk in the repository's caches and fetch logs, section 7).
#
# Run from longrun/:  ../../venv/Scripts/python.exe code/coverage.py [probe] [ipums] [seen] [eligibility]
#                     (no argument: all four; probes are cached and logged under half 'meta', so a rerun is offline)

from __future__ import annotations

import glob
import html
import json
import os
import re
import sys
import time
from datetime import date

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
LROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import fetch  # noqa: E402

DATA = os.path.join(LROOT, "data")
CUBE = os.path.join(DATA, "coverage.json")
L2CSV = os.path.join(DATA, "coverage_l2.csv")
SAMPLES = os.path.join(DATA, "ipums_samples.json")
SEEN = os.path.join(DATA, "seen.json")

LFS_FLOW = fetch.SOURCES["oecd_lfs"]["flow"]
RPI_FLOW = fetch.SOURCES["oecd_rpi"]["flow"]
CPI_FLOW = fetch.SOURCES["oecd_cpi"]["flow"]
C18_FLOW = fetch.SOURCES["oecd_cpi2018"]["flow"]
# series id -> (flow, key with REF_AREA left empty, first and last year probed)
PROBES = {
    "act_F_Y25T29": (LFS_FLOW, ".LF_RATE.PT_POP_SUB.F.Y25T29.LF", 1960, 2025),
    "act_F_Y30T34": (LFS_FLOW, ".LF_RATE.PT_POP_SUB.F.Y30T34.LF", 1960, 2025),
    "act_M_Y25T29": (LFS_FLOW, ".LF_RATE.PT_POP_SUB.M.Y25T29.LF", 1960, 2025),
    "act_M_Y30T34": (LFS_FLOW, ".LF_RATE.PT_POP_SUB.M.Y30T34.LF", 1960, 2025),
    "une_T_Y25T54": (LFS_FLOW, ".UNE_RATE.PT_LF_SUB._T.Y25T54.UNE", 1960, 2025),
    "rpi": (RPI_FLOW, ".A.RPI.IX", 1955, 2025),
    "cpi": (CPI_FLOW, ".A.N.CPI.IX._T.N._Z", 1955, 2025),
    "cpi2018": (C18_FLOW, ".A.N.CPI.IX._T.N._Z", 1955, 2025),
}
A2534_CELLS = ["act_F_Y25T29", "act_F_Y30T34", "act_M_Y25T29", "act_M_Y30T34"]

# ---------------------------------------------------------------- documented coverage (no values-free availability)

# JST R6, q rung 1: years with housing_rent_yd, the house-price leg and cpi, as documented (PROTOCOL L6;
# docs/data_inventory.md 'macrohistory': complete 1950-2020 for 13 countries; BEL 1965-1975 missing (rent_ipolated);
# DEU from 1962; JPN from 1960). Only q years 1949-2020 matter here.
JST_DOC = {c: (1950, 2020, []) for c in "AU CH DK ES FI FR UK IT NL NO PT SE US".split()}
JST_DOC.update({"BE": (1950, 2020, list(range(1965, 1976))), "DE": (1962, 2020, []), "JP": (1960, 2020, [])})
# L3: years the R6 documentation says were missing in its 2016-2020 rent update (JST_RORE_Documentation_R6.pdf,
# Table 3 notes: '*Data is missing for 2020' FI, NO, SE; '** Data is missing for 2019 and 2020' ES).
JST_R6_MISSING = {"FI": [2020], "NO": [2020], "SE": [2020], "ES": [2019, 2020]}
JST_CITE = ("JST R6 coverage as documented: PROTOCOL L6 and docs/data_inventory.md (macrohistory); R6 Table 3 notes "
            "(JST_RORE_Documentation_R6.pdf p. 9)")
# ILOSTAT POP_3WAP_SEX_AGE_STU_NB_A (C-6L): documented first years among members (docs/data_inventory.md,
# ilo_un_hist: 'Before 1997 among OECD: BEL, DNK, FRA, GBR, IRL, LUX 1983-; ITA 1983-; NLD 1983-; DEU 1983-; GRC
# 1987-; ESP, PRT 1986-; CAN 1976-; CHL 1990-; CHE 1991-; USA 1994-; AUT, ISL, SWE 1995-; FIN, HUN, SVN 1996-.
# Absent for JPN, ISR and NZL; most others start after 2000'). Annual runs to 2025 assumed, no gaps known. Members whose
# start is only 'after 2000' are not counted here: their per-country years are unknown until the L2 mask.
ILO_DOC_START = {"BE": 1983, "DK": 1983, "FR": 1983, "UK": 1983, "IE": 1983, "LU": 1983, "IT": 1983, "NL": 1983,
                 "DE": 1983, "EL": 1987, "ES": 1986, "PT": 1986, "CA": 1976, "CL": 1990, "CH": 1991, "US": 1994,
                 "AT": 1995, "IS": 1995, "SE": 1995, "FI": 1996, "HU": 1996, "SI": 1996}
ILO_CITE = "ILOSTAT YOUTHSTATS first years as documented in docs/data_inventory.md (ilo_un_hist); to 2025 assumed"


# ---------------------------------------------------------------- probes

def probe(sleep: float = 0.4) -> dict:
    """{series: {year: [members with an observation]}} from per-year availability probes (cached, logged)."""
    back = {}
    for c in fetch.COUNTRIES:
        back[fetch.ref_area(c, "oecd_lfs")] = c
        back[fetch.ISO3[c]] = c
    out = {}
    for sid, (flow, key, y0, y1) in PROBES.items():
        out[sid] = {}
        for y in range(y0, y1 + 1):
            for attempt in range(6):
                try:
                    areas = fetch.availability(flow, key, y)
                    break
                except RuntimeError as e:
                    if "HTTP 429" in str(e) or "HTTP 5" in str(e):
                        time.sleep(30 * (attempt + 1))
                        continue
                    raise
            else:
                raise RuntimeError(f"probe {sid} {y} failed repeatedly")
            # DE's outcome and cycle come from DEU_F only (L4); its prices from DEU
            keep = []
            for a in areas:
                if sid.startswith(("act", "une")):
                    if a == "DEU":
                        continue
                    if a in back and (a != "DEU_F"):
                        keep.append(back[a])
                    elif a == "DEU_F":
                        keep.append("DE")
                elif a in back and a != "DEU_F":
                    keep.append(back[a])
            out[sid][str(y)] = sorted(set(keep))
            time.sleep(sleep)
        print(f"  probed {sid}: {y0}-{y1}", flush=True)
    return out


# ---------------------------------------------------------------- IPUMS sample list (public metadata)

IPUMS_PREFIX = {"at": "AT", "au": "AU", "be": "BE", "ca": "CA", "ch": "CH", "cl": "CL", "co": "CO", "cr": "CR",
                "cz": "CZ", "de": "DE", "dk": "DK", "ee": "EE", "gr": "EL", "es": "ES", "fi": "FI", "fr": "FR",
                "hu": "HU", "ie": "IE", "il": "IL", "is": "IS", "it": "IT", "jp": "JP", "kr": "KR", "lt": "LT",
                "lu": "LU", "lv": "LV", "mx": "MX", "nl": "NL", "no": "NO", "nz": "NZ", "pl": "PL", "pt": "PT",
                "se": "SE", "si": "SI", "sk": "SK", "tr": "TR", "uk": "UK", "us": "US"}
# Flags expected from the IPUMS-I comparability pages (PROTOCOL L9); confirmed or extended at L2 by reading each
# sample's codebook. 'child' = the child category includes children-in-law or grandchildren or uses a combined code;
# 'family' = household is the census family; 'unknown' = persons outside the primary family coded unknown.
EXPECTED_FLAGS = {"de1970a": ["child includes children-in-law"], "at1971a": ["child includes children-in-law"],
                  "ch1970a": ["child includes children-in-law"], "fr1962a": ["child includes grandchildren"],
                  "co1964a": ["household = census family"], "ie1971a": ["outside primary family coded unknown"],
                  "hu1970a": ["outside primary family coded unknown"],
                  "nl1960a": ["coarse coding: flag if the child category is affected (L2)"],
                  "nl1971a": ["coarse coding: flag if the child category is affected (L2)"],
                  "cr1963a": ["coarse coding: flag if the child category is affected (L2)"]}
# Grouped ages (PROTOCOL L9): selected by interval; the intervals are recorded at L2 from each codebook.
GROUPED_AGE = {"nl1960a", "nl1971a", "il1972a", "ie1971a"}
# Census, count or survey (L10 admits census samples only; surveys are excluded). The IPUMS-I sample page groups
# samples but does not say which are sample surveys; the kinds below are recorded from each sample's IPUMS description
# at L2. Known before L2: Mexico 2015 is the Encuesta Intercensal, a sample survey; Mexico 1995 and 2005 are the Conteos
# (counts that IPUMS groups with the censuses), kept as censuses until the L2 reading says otherwise.
SAMPLE_KIND = {"mx2015a": "survey (Encuesta Intercensal 2015)", "mx1995a": "count (Conteo 1995; confirm at L2)",
               "mx2005a": "count (Conteo 2005; confirm at L2)"}


def ipums_samples() -> dict:
    """The frozen sample lists (F_L: 1955-1975; Extract B: 1976+ inside the unseen window), from public metadata."""
    page = fetch.doc("ipums_samples").decode("utf-8", "replace")
    groups = {}
    for m in re.finditer(r'name="([a-z_]+)_all" id="[a-z_]+" value="Check All" class="parent-checkbox" '
                         r'data-dependent-samples="([^"]*)"', page):
        groups[m.group(1)] = set(m.group(2).split())
    census_like = groups.get("all_regions", set())
    surveys = groups.get("survey_samples", set())
    if not census_like:
        raise RuntimeError("could not read the IPUMS-I sample groups from the sample page")
    info = {}
    for m in re.finditer(r'<abbr title="([^"]+)" class="[a-z ]*"><input type="checkbox" name="selectedSamples\[\]" '
                         r'id="sample_([a-z]{2}\d{4}[a-z])"', page):
        sid, title = m.group(2), html.unescape(m.group(1))
        tail = page[m.end():m.end() + 900]
        note = re.search(r'<span>([^<]*)</span><span class="icon info">', tail.split("sample-item")[0])
        info[sid] = {"title": title, "note": note.group(1).strip() if note else ""}
    relate_page = fetch.doc("ipums_relate").decode("utf-8", "replace")
    i = relate_page.find('id="availability"')
    avail = {}
    for name, years in re.findall(r"<li>\s*([^:<]+):\s*([^<]*)</li>", relate_page[i:i + 40000]):
        avail[html.unescape(name).strip()] = {y.strip() for y in years.split(",") if y.strip()}
    out = {"F_L": [], "extract_B": [], "excluded": []}
    for sid in sorted(census_like | surveys):
        pre, year = sid[:2], int(sid[2:6])
        if pre not in IPUMS_PREFIX:
            continue
        c = IPUMS_PREFIX[pre]
        meta = info.get(sid, {"title": "", "note": ""})
        name = re.sub(r"\s+\d{4}.*$", "", meta["title"]).strip()
        has_relate = str(year) in avail.get(name, set()) or f"{year}{sid[-1]}" in avail.get(name, set())
        kind = SAMPLE_KIND.get(sid, "survey" if (sid in surveys or "survey" in meta["note"].lower())
                               else "census (IPUMS census group; kind confirmed at L2)")
        rec = {"sample": sid, "country": c, "year": year, "title": meta["title"], "note": meta["note"],
               "relate": bool(has_relate),
               "households": "not organized into households" not in meta["note"].lower(),
               "grouped_age": ("grouped" in meta["note"].lower()) or sid in GROUPED_AGE,
               "flags": EXPECTED_FLAGS.get(sid, []), "kind": kind}
        is_survey = kind.startswith("survey")
        if is_survey:
            out["excluded"].append({**rec, "why": "survey sample"})
        elif 1955 <= year <= 1975:
            out["F_L"].append(rec)
        elif year >= 1976 and fetch.is_unseen(c, year):
            out["extract_B"].append(rec)
        elif year >= 1976:
            out["excluded"].append({**rec, "why": "census year outside the unseen window (L1, L2)"})
    # which sample sets F_L (earliest with RELATE) and the robustness one (nearest 1970, ties earlier)
    by_c: dict = {}
    for r in out["F_L"]:
        by_c.setdefault(r["country"], []).append(r)
    roles = {}
    for c, rs in by_c.items():
        rel = sorted([r for r in rs if r["relate"]], key=lambda r: (r["year"], r["sample"]))
        if c == "DE":                                      # the West German 1970 sample only (L9 territory; L2)
            rel = [r for r in rel if "west" in r["title"].lower() or "west" in r["note"].lower()]
        if not rel:
            continue
        near = sorted(rel, key=lambda r: (abs(r["year"] - 1970), r["year"]))[0]
        roles[c] = {"F_L": rel[0]["sample"], "F_L_1970": near["sample"]}
    for r in out["F_L"]:
        r["role"] = [k for k, v in roles.get(r["country"], {}).items() if v == r["sample"]]
    out["roles"] = roles
    out["source"] = {"samples": fetch.DOCS["ipums_samples"]["url"], "relate": fetch.DOCS["ipums_relate"]["url"],
                     "read": str(date.today())}
    out["to_confirm_at_L2"] = ["RELATE detailed codes per sample", "household concept", "GQ coding",
                               "age intervals of grouped samples", "the flags above, from the comparability pages",
                               "the loader's variable whitelist against the extract builder",
                               "each sample's kind (census, count or survey) from its IPUMS description"]
    return out


# ---------------------------------------------------------------- seen (section 7)

def seen() -> dict:
    """Every file on disk in the repository's caches that holds series values, by country and series name (file names
    only; nothing is opened but the fetch logs, read for their URLs)."""
    repo = os.path.dirname(os.path.dirname(LROOT))
    out = {"caches": {}, "fetch_logs": {}}
    for d in ("paths/cache", "pinning/cache", "participation/data/raw"):
        for f in sorted(glob.glob(os.path.join(repo, d, "**", "*"), recursive=True)):
            if os.path.isfile(f):
                out["caches"].setdefault(d, []).append(os.path.relpath(f, os.path.join(repo, d)).replace("\\", "/"))
    for f in glob.glob(os.path.join(repo, "**", "fetch_log*.jsonl"), recursive=True):
        if "longrun" in f.replace("\\", "/"):
            continue
        urls = []
        for ln in open(f, encoding="utf-8"):
            if ln.strip():
                urls.append(json.loads(ln).get("url"))
        out["fetch_logs"][os.path.relpath(f, repo).replace("\\", "/")] = urls
    out["note"] = ("US long series (paths/, pinning/) and the European Eurostat panel (participation/) are seen "
                   "(PROTOCOL section 7): its observation years 1995-2025, since the European panel grid starts in "
                   "1995 and the European exploration's committed outputs hold 1995-1996 rows, so the long run's "
                   "European cells end at 1994 (L1). The European raw cache (participation/data/raw) also holds "
                   "pre-1995 values of the long-run outcome and cycle (lfsa_argan, lfsa_urgan, lfsa_ergan) and of "
                   "prc_hicp_aind, never viewed; the skeleton drops them at parse. The scouts' working folders are "
                   "listed in 'scouts_folders' when they are moved (her choice of location; PROTOCOL section 7).")
    out["scouts_folders"] = {"moved_to": None, "files": [],
                             "status": "not yet moved: before the freeze every file is hashed and listed here and the "
                                       "folders are moved to a location she chooses (PROTOCOL section 7)"}
    try:                                                   # a recorded move is kept when seen.json is rewritten
        old = json.load(open(SEEN, encoding="utf-8")).get("scouts_folders") or {}
        if old.get("moved_to"):
            out["scouts_folders"] = old
    except (OSError, ValueError):
        pass
    out["incidents"] = [
        "2026-10-09: an IPUMS-International extract (ipumsi_00001.csv.gz, 1,565,024,917 bytes, written 10:37-11:08) "
        "was found directly in longrun's data folder, not in its ipums subfolder, before the L-freeze tag, with no DDI "
        "beside it and no "
        "fetch-log record; no agent opened it (the reviews read its size and times only); the loader refuses while it "
        "lies there (ipums.stray_microdata). Where it goes is her call (PROTOCOL section 7)."]
    out["european_outputs_before_cut"] = EUROPEAN_PRE_CUT
    out["written"] = str(date.today())
    return out


# Committed outputs of the European exploration (participation/explore, explore countries) whose rows reach back
# before the long run's European cut (L1, 1994). None holds a verdict test's variable (the activity rates 25-29 and
# 30-34, the unemployment rate 25-54, school attendance 20-24); they are disclosed prior knowledge (section 7).
# checks/check_guard.py M1 requires every such output to be listed here.
EUROPEAN_PRE_CUT = {
    "explore/aging_retirement/inactive_5564_want.csv":
        "inactive persons 55-64 by wish to work, counts and shares of population, 1983 on, BE CH FI FR HU IE IT LU PT SE: "
        "an inactivity rate 55-64 (both sexes) is derivable; A5564 enters only C-2L (no verdict)",
    "explore/occupations_ai/gap_young_minus_2564.csv":
        "occupation-share gaps, young minus 25-64 (ISCO groups), 1983 on, same countries: not a long-run variable",
    "explore/occupations_ai/shares_T.csv":
        "occupation shares by age (ISCO groups), 1983 on, same countries: not a long-run variable",
}


# ---------------------------------------------------------------- eligibility

def _years(d: dict, c: str) -> set[int]:
    return {int(y) for y, cs in d.items() if c in cs}


def cube_for(c: str, raw: dict) -> dict:
    """{series: sorted years} for one member: probes, JST documented, ILO documented."""
    s = {sid: sorted(_years(raw[sid], c)) for sid in PROBES}
    if c in JST_DOC:
        lo, hi, gaps = JST_DOC[c]
        miss = set(gaps) | set(JST_R6_MISSING.get(c, []))
        s["jst"] = [y for y in range(lo, hi + 1) if y not in miss]
    else:
        s["jst"] = []
    s["school"] = list(range(ILO_DOC_START[c], fetch.LAST_YEAR + 1)) if c in ILO_DOC_START else []
    return s


def q_ladder(c: str, s: dict) -> dict:
    """L6: {q year: source} by the ladder. Rung 1 (JST) over its longest contiguous run overlapping the window
    (counted inside it, ties the later); rung 2 (RPI over CPI) only extends that run, backwards from JST's first year
    or forwards from JST's last (documented) year, never into a gap next to the run; without JST, rung 2 throughout.
    The CPI is DF_PRICES_ALL, extended from DF_PRICES_C2018_ALL after its last year."""
    qwin = {t - 1 for t in fetch.window(c)}
    cpi, c18, rpi = set(s["cpi"]), set(s["cpi2018"]), set(s["rpi"])
    last_all = max(cpi) if cpi else None

    def r2(y):
        if y not in rpi:
            return None
        if y in cpi:
            return "rpi/cpi"
        if last_all is not None and y > last_all and y in c18:
            return "rpi/cpi2018"
        return None
    out = {}
    jst = sorted(s["jst"])
    if jst:
        runs, cur = [], [jst[0]]
        for y in jst[1:]:
            if y == cur[-1] + 1:
                cur.append(y)
            else:
                runs.append(cur)
                cur = [y]
        runs.append(cur)
        runs = [r for r in runs if set(r) & qwin]
        if runs:
            run = sorted(runs, key=lambda r: (len(set(r) & qwin), r[0]))[-1]
            for y in run:
                out[y] = "jst"
            # rung 2 only extends beyond rung 1's coverage: backwards if the run starts at JST's first year, forwards
            # if it ends at JST's last (documented) year; a gap next to the run is never filled
            if run[0] == jst[0]:
                y = run[0] - 1
                while r2(y):
                    out[y] = r2(y)
                    y -= 1
            if run[-1] == jst[-1]:
                y = run[-1] + 1
                while r2(y):
                    out[y] = r2(y)
                    y += 1
            return dict(sorted(out.items()))
    for y in sorted(rpi):
        if r2(y):
            out[y] = r2(y)
    return dict(sorted(out.items()))


def q_segments(c: str, ladder: dict, seg: pd.DataFrame) -> list[tuple[int, int]]:
    """The q segments of a member: [start, end] q-year spans cut at every documented q segment start (segments.csv,
    series q) and every source switch of the ladder (rung or CPI flow)."""
    if not ladder:
        return []
    ys = sorted(ladder)
    starts = {ys[0]}
    for a, b in zip(ys[:-1], ys[1:]):
        if ladder[a] != ladder[b]:
            starts.add(b)
    doc = seg[(seg["geo"] == c) & (seg["series"] == "q")]["tau"].astype(int).tolist() if len(seg) else []
    starts |= {t for t in doc if ys[0] < t <= ys[-1]}
    starts = sorted(starts)
    ends = [s - 1 for s in starts[1:]] + [ys[-1]]
    return list(zip(starts, ends))


def chosen_segment(c: str, ladder: dict, segs: list) -> tuple[int, int] | None:
    """Section 5: the longest q segment by its count of q years t-1 whose observation year t is in the window (ties:
    the later segment)."""
    win = set(fetch.window(c))
    best, key = None, None
    for a, b in segs:
        n = sum(1 for y in ladder if a <= y <= b and (y + 1) in win)
        k = (n, a)
        if n > 0 and (key is None or k > key):
            best, key = (a, b), k
    return best


def eligibility(raw: dict, samples: dict, seg: pd.DataFrame) -> tuple[dict, pd.DataFrame]:
    """The cube and the per-country eligibility table (section 3's testability rules)."""
    cube, rows = {}, []
    fl_countries = set(samples["roles"])
    def rows_of(series):
        return ({c: sorted(seg[(seg["geo"] == c) & (seg["series"] == series)]["tau"].astype(int).tolist())
                 for c in fetch.COUNTRIES} if len(seg) else {c: [] for c in fetch.COUNTRIES})
    lfs_seg, school_seg, cor_seg = rows_of("lfs"), rows_of("school"), rows_of("coresid")
    for c in fetch.COUNTRIES:
        s = cube_for(c, raw)
        ladder = q_ladder(c, s)
        segs = q_segments(c, ladder, seg)
        ch = chosen_segment(c, ladder, segs)
        win = fetch.window(c)
        a2534 = set.intersection(*[set(s[k]) for k in A2534_CELLS])
        u = set(s["une_T_Y25T54"])
        qy = set(ladder)
        in_ch = {y for y in qy if ch and ch[0] <= y <= ch[1]}
        rank = sorted(t for t in win if (t - 1) in in_ch)                       # ranking set (q alone)
        elig = sorted(t for t in rank if t in a2534 and t in u)                 # LR-K2 / LR-Y0 eligible years
        # C-6L: school and U both available, counted inside one segment of the outcome (documented school rows) and
        # of the regressor (lfs rows for U); ILOSTAT source changes arriving with the values cut further, by rule
        school = sorted(t for t in win if t in set(s["school"]) and t in u)
        cuts = sorted({fetch.FIRST_YEAR, 9999} | set(lfs_seg[c]) | set(school_seg[c]))
        c6_best = max((sum(1 for t in school if a <= t < b) for a, b in zip(cuts[:-1], cuts[1:])), default=0)
        # LR-C1: Extract B censuses with x available, within one q segment and one outcome (coresid) segment
        eb = [r for r in samples["extract_B"] if r["country"] == c and r["relate"]]
        ccuts = sorted({fetch.FIRST_YEAR, 9999} | set(cor_seg[c]))
        by_seg = {}
        for r in eb:
            y = r["year"]
            oseg = max(a for a in ccuts if a <= y)
            for a, b in segs:
                if a <= y - 1 <= b and (y - 1) in qy:
                    by_seg.setdefault((a, b, oseg), []).append(y)
        c1_best = max((len(v) for v in by_seg.values()), default=0)
        cube[c] = {"series": {k: v for k, v in s.items()}, "q_ladder": {str(k): v for k, v in ladder.items()},
                   "q_segments": [list(x) for x in segs], "chosen_q_segment": list(ch) if ch else None,
                   "ranking_years": rank, "eligible_K2_Y0": elig, "school_years": school,
                   "extract_B_censuses": [r["year"] for r in eb],
                   "window": [win[0], win[-1]] if win else None}
        rows.append(dict(geo=c, stratum=fetch.stratum_of(c), european=c in fetch.EUROPEAN,
                         window=f"{win[0]}-{win[-1]}" if win else "",
                         chosen_q_segment=f"{ch[0]}-{ch[1]}" if ch else "", q_sources="+".join(sorted(set(ladder.values()))),
                         n_ranked=len(rank), n_eligible=len(elig),
                         eligible_years=" ".join(map(str, elig)),
                         F_L_sample=samples["roles"].get(c, {}).get("F_L", ""),
                         K2=bool(c in fl_countries and len(elig) >= 9),
                         Y0=bool(len(elig) >= 9),
                         C6L_n_in_one_segment=c6_best, C6L=bool(c6_best >= 2),
                         C1_n_in_one_q_segment=c1_best, C1=bool(c1_best >= 2)))
    return cube, pd.DataFrame(rows)


def families(tab: pd.DataFrame) -> dict:
    """Section 3: a test is testable with at least 8 member countries; families from the testable tests."""
    n = {k: int(tab[k].sum()) for k in ("K2", "Y0", "C6L", "C1")}
    testable = {k: v >= 8 for k, v in n.items()}
    return {"members": {k: sorted(tab.loc[tab[k], "geo"]) for k in n}, "n": n, "testable": testable,
            "K": ["LR-K2"] if testable["K2"] else [],
            "C-L": [t for t, k in (("LR-Y0", "Y0"), ("C-6L", "C6L"), ("LR-C1", "C1")) if testable[k]],
            "note": "LR-C1 enters C-L only if she makes Extract B (her call, recorded in the freeze commit)"}


def main() -> None:
    steps = set(sys.argv[1:]) or {"probe", "ipums", "seen", "eligibility"}
    if "--masks" in steps:
        raise SystemExit("the JST and ILOSTAT values-dropping masks download value files: they wait for her go-ahead "
                         "(PROTOCOL section 3 and the blinding instruction of 2026-10-09)")
    os.makedirs(DATA, exist_ok=True)
    raw_path = os.path.join(DATA, "coverage_probes.json")
    if "probe" in steps:
        raw = probe()
        with open(raw_path, "w", encoding="utf-8") as f:
            json.dump({"written": str(date.today()), "probes": {k: list(v) for k, v in PROBES.items()},
                       "available": raw}, f, indent=0, sort_keys=True)
        print(f"wrote {raw_path}")
    if "ipums" in steps:
        smp = ipums_samples()
        with open(SAMPLES, "w", encoding="utf-8") as f:
            json.dump(smp, f, indent=1)
        print(f"F_L samples {len(smp['F_L'])}, Extract B samples {len(smp['extract_B'])}; wrote {SAMPLES}")
    if "seen" in steps:
        with open(SEEN, "w", encoding="utf-8") as f:
            json.dump(seen(), f, indent=1)
        print(f"wrote {SEEN}")
    if "eligibility" in steps:
        raw = json.load(open(raw_path, encoding="utf-8"))["available"]
        smp = json.load(open(SAMPLES, encoding="utf-8"))
        import segments as sg
        seg = sg.load()
        cube, tab = eligibility(raw, smp, seg)
        fam = families(tab)
        with open(CUBE, "w", encoding="utf-8") as f:
            json.dump({"written": str(date.today()),
                       "provenance": {"oecd": "per-year availableconstraint probes (data/coverage_probes.json)",
                                      "jst": JST_CITE, "school": ILO_CITE, "ipums": "data/ipums_samples.json",
                                      "segments": "data/segments.csv"},
                       "status": ("JST and ILOSTAT from documentation; PROTOCOL section 3 asks for values-dropping "
                                  "masks at L2 (not run: they download value files)"),
                       "families": fam, "countries": cube}, f, indent=1)
        tab.to_csv(L2CSV, index=False, lineterminator="\n")
        print(tab[["geo", "chosen_q_segment", "n_eligible", "F_L_sample", "K2", "Y0", "C6L", "C1"]].to_string())
        print(json.dumps({k: fam[k] for k in ("n", "testable", "K", "C-L")}))
        print(f"wrote {CUBE} and {L2CSV}")


def mask_jst() -> pd.DataFrame:
    """PROTOCOL section 3: the JST values-dropping mask (country, year, non-missingness and the L3 flags only). It
    downloads the value file, so it runs only on her go-ahead; nothing is printed or written but the mask."""
    raise SystemExit("not run: waits for her go-ahead (downloads the JST value file)")


def mask_ilostat() -> pd.DataFrame:
    """PROTOCOL section 3: the ILOSTAT values-dropping mask, as mask_jst."""
    raise SystemExit("not run: waits for her go-ahead (downloads ILOSTAT value files)")


if __name__ == "__main__":
    main()
