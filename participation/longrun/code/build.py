# build.py — the variables of longrun/PROTOCOL.md section 3 (L3-L12), built from the guarded doors of fetch.py and
# ipums.py. Every query the pipeline makes is in MANIFEST; `main` writes it to data/manifest.json.
#
# The order of each opening (L14) is the order of the functions: fetch_regressors(half) (q's sources) -> the knots
# (specs.knots, recorded in the fetch log) -> ipums.F_L(half) (recorded) -> fetch_outcomes(half) (the LFS cells, U,
# school; the outcome doors refuse before the two records exist) -> fetch_controls(half).
#
# panel(raw, geos, seg) -> DataFrame indexed (geo, year) over each country's unseen observation years (L1, L2: the
#   rows outside fetch.window(c) are dropped after lags are taken on the full annual grid), with, for every variable,
#   a companion '<var>__breaks' listing the observation years at which a new segment starts (L7): the documented rows
#   of data/segments.csv for the series the variable carries, the q ladder's source switches, and the rules applied as
#   values arrive (OECD OBS_STATUS B; an ILOSTAT source change; a JST interpolated capital-gain year). For a lagged
#   regressor every break moves one year later. Variables:
#   A2534      (L4) equal-weight mean of F/M x Y25T29/Y30T34 activity rates; missing if any cell is missing
#   A2534_M/_F the same for one sex (the men-only and women-only robustness runs)
#   A5564      F/M x Y55T59/Y60T64; AW2554, AM2554: the six five-year bands 25-29 ... 50-54 of one sex
#   U          (L5) the unemployment rate 25-54, both sexes, same flow, observation year
#   logq_l1    (L6) log q of year t-1 by the FROZEN ladder (data/coverage.json 'q_ladder', fixed at L2 from
#              availability): each q year takes the source the frozen ladder names; a value that is missing or flagged
#              under L3 is NaN inside the run and never moves a run, a source or a membership (section 3, 'Frozen
#              membership'); 'qseg_l1' the q segment (its first q year) of that q year; 'qsrc_l1' its source
#   logq_hpi_l1 the house-price robustness q: JST hpnom (or cumulated capital gains) over cpi where the frozen ladder
#              names JST, else OECD HPI over the CPI the frozen ladder names; 'qseg_hpi_l1'
#   school2024 (L11) attending / (attending + not attending), 20-24, both sexes (ILOSTAT)
#   cohort     (L12) population 25-34 / population 35-64 (WPP2024; the L3 exception), observation year
#   strict     (L12) 1 for a Kholodilin first-generation strict-control country-year, 0 for a covered year without it,
#              NaN where the coding does not cover the country (those keep all their years; kholodilin_uncovered()
#              lists them for the report). fetch.kholodilin returns geo, year, strict once L2 confirms the file.
# L3 at the door of each value: OECD OBS_STATUS E, F, M -> missing; JST rent_ipolated = 1 -> missing; for ES, IT, PT
#   (whose rent index uses cumulated housing_capgain) housing_capgain_ipol = 1 -> missing, and the next measured year
#   starts a new q segment (the cumulated level links across an interpolated growth: a splice, so a fixed effect); the
#   years the R6 documentation says were missing (coverage.JST_R6_MISSING) -> missing; ILOSTAT obs_status E, F, I or a
#   source code starting 'EA' -> missing. No interpolation, backcast or ratio-link anywhere.
# country_level(fl, gn, geos) -> DataFrame indexed by geo: stratum, F_L (25-34, percent), F_L_2029, F_L_1970 (sample
#   nearest 1970) with its year, F_L_flagged (the frozen record carries a flag), GN (Giuliano-Nunn, robustness only).
#
# Run from longrun/:  ../../venv/Scripts/python.exe code/build.py   (writes data/manifest.json; fetches nothing)

from __future__ import annotations

import json
import os
import sys
from datetime import date

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
LROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import coverage as cv  # noqa: E402
import fetch  # noqa: E402
import segments as sg  # noqa: E402

MANIFEST_PATH = os.path.join(LROOT, "data", "manifest.json")
GRID = list(range(fetch.FIRST_YEAR - 2, fetch.LAST_YEAR + 1))     # the annual grid before the window cut
AGES_PRIME = ["Y25T29", "Y30T34", "Y35T39", "Y40T44", "Y45T49", "Y50T54"]
AGES_OLD = ["Y55T59", "Y60T64"]
CAPGAIN_Q = ("ES", "IT", "PT")                                     # L6: rent index = yield x cumulated capital gains
CPI_KEY = {"FREQ": "A", "METHODOLOGY": "N", "MEASURE": "CPI", "UNIT_MEASURE": "IX", "EXPENDITURE": "_T",
           "ADJUSTMENT": "N", "TRANSFORMATION": "_Z"}
# Every query of the pipeline. 'key' pins every dimension but REF_AREA; codes verified 2026-10-09 against the SDMX
# structure (fetch.meta, dataflow ?references=all; DF_LFS_INDIC's content constraint lists every code used here).
MANIFEST = [
    dict(id="act", source="oecd_lfs", role="outcome",
         key={"MEASURE": "LF_RATE", "UNIT_MEASURE": "PT_POP_SUB", "SEX": ["F", "M"], "AGE": AGES_PRIME + AGES_OLD,
              "LABOUR_FORCE_STATUS": "LF"}, use="activity rates (L4): A2534, A2534_M/_F, A5564, AW2554, AM2554"),
    dict(id="une", source="oecd_lfs", role="outcome",
         key={"MEASURE": "UNE_RATE", "UNIT_MEASURE": "PT_LF_SUB", "SEX": "_T", "AGE": "Y25T54",
              "LABOUR_FORCE_STATUS": "UNE"}, use="the cycle U 25-54 (L5)"),
    dict(id="house", source="oecd_rpi", role="regressor",
         key={"FREQ": "A", "MEASURE": ["RPI", "HPI"], "UNIT_MEASURE": "IX"},
         use="q rung 2 numerator (RPI) and the q_hpi robustness numerator (HPI)"),
    dict(id="cpi", source="oecd_cpi", role="regressor", key=CPI_KEY, use="all-items CPI (L6 rung 2)"),
    dict(id="cpi2018", source="oecd_cpi2018", role="regressor", key=CPI_KEY, absent=["AT", "CO", "DE", "IL", "KR", "NZ",
                                                                                       "PL", "SK", "UK", "US"],
         use="all-items CPI, COICOP 2018, extending DF_PRICES_ALL after its last year (L6)"),
    dict(id="jst", source="jst", role="regressor", only=sorted(cv.JST_DOC), use="JST R6 rent index and CPI (L6 rung 1)"),
    dict(id="school", source="ilostat", role="outcome", use="school attendance 20-24 (L11)"),
    dict(id="cohort", source="wpp_age", role="control", use="relative cohort size (L12)"),
    dict(id="gn", source="giuliano_nunn", role="moderator", use="Giuliano-Nunn F (robustness)"),
    dict(id="kholodilin", source="kholodilin", role="control", use="strict rent control (L12)"),
]
BY_ID = {m["id"]: m for m in MANIFEST}
REGRESSOR_IDS = ["house", "cpi", "cpi2018", "jst"]
OUTCOME_IDS = ["act", "une", "school"]
CONTROL_IDS = ["cohort", "gn", "kholodilin"]
VARIABLES = {
    "A2534": "activity rate 25-34: mean of F/M x 25-29, 30-34 (pp)", "A2534_M": "men 25-34", "A2534_F": "women 25-34",
    "A5564": "activity rate 55-64", "AW2554": "women 25-54", "AM2554": "men 25-54", "U": "unemployment rate 25-54",
    "logq_l1": "log q, year t-1 (L6 ladder)", "logq_hpi_l1": "log house prices over CPI, t-1",
    "school2024": "share of 20-24 attending school (pp)", "cohort": "population 25-34 / 35-64",
    "strict": "Kholodilin strict (first-generation) rent control",
}


def query_geos(m: dict, geos) -> list[str]:
    g = [c for c in sorted(geos) if c not in m.get("absent", [])]
    return [c for c in g if c in m["only"]] if "only" in m else g


def _fetch(ids, half: str, geos) -> dict:
    out = {}
    for i in ids:
        m = BY_ID[i]
        g = query_geos(m, geos)
        if not g:
            out[i] = pd.DataFrame()
            continue
        if m["source"].startswith("oecd_"):
            out[i] = fetch.oecd(m["source"], m["key"], g, half)
        elif m["source"] == "jst":
            out[i] = fetch.jst(g, half)
        elif m["source"] == "ilostat":
            out[i] = fetch.ilostat(g, half)
        elif m["source"] == "wpp_age":
            out[i] = fetch.wpp_age(g, half)
        elif m["source"] == "giuliano_nunn":
            out[i] = fetch.giuliano_nunn(g, half)
        elif m["source"] == "kholodilin":
            try:
                out[i] = fetch.kholodilin(g, half)
            except RuntimeError:
                out[i] = pd.DataFrame()                       # not confirmed at L2: 'control-era years not separable'
    return out


def fetch_regressors(half: str, geos) -> dict:
    return _fetch(REGRESSOR_IDS, half, geos)


def fetch_outcomes(half: str, geos) -> dict:
    return _fetch(OUTCOME_IDS, half, geos)


def fetch_controls(half: str, geos) -> dict:
    return _fetch(CONTROL_IDS, half, geos)


# ---------------------------------------------------------------- cells

def _flagged(df: pd.DataFrame) -> pd.DataFrame:
    """L3: a copy with value NaN where OBS_STATUS is E, F or M (flags kept for the break rule)."""
    out = df.copy()
    if len(out):
        out.loc[out["flag"].map(fetch.is_not_measured).astype(bool), "value"] = np.nan
    return out


def cell(df: pd.DataFrame, **sel) -> tuple[pd.Series, dict]:
    """One OECD cell series: (values indexed (geo, year), {geo: [B-flag years]})."""
    d = df
    for k, v in sel.items():
        d = d[d[k] == v]
    d = _flagged(d)
    s = pd.Series(pd.to_numeric(d["value"], errors="coerce").to_numpy(float),
                  index=pd.MultiIndex.from_arrays([d["geo"].astype(str), d["year"].astype(int)], names=["geo", "year"]))
    s = s[~s.index.duplicated()]
    b = d[d["flag"].map(fetch.is_break).astype(bool)]
    return s, {g: sorted(int(y) for y in set(v)) for g, v in b.groupby("geo")["year"]}


def _union(*bs) -> dict:
    out: dict = {}
    for b in bs:
        for g, ys in b.items():
            out.setdefault(g, set()).update(int(y) for y in ys)
    return {g: sorted(v) for g, v in out.items()}


def band(df: pd.DataFrame, cells: list[dict]) -> tuple[pd.Series, dict]:
    """Equal-weight mean of the cells (C5's rule); missing where any cell is missing."""
    parts = [cell(df, **c) for c in cells]
    frame = pd.concat([p[0] for p in parts], axis=1) if parts else pd.DataFrame()
    return frame.mean(axis=1, skipna=False), _union(*[p[1] for p in parts])


def _doc_breaks(seg: pd.DataFrame, series: list[str]) -> dict:
    d = seg[seg["series"].isin(series)]
    return {g: sorted(int(t) for t in v) for g, v in d.groupby("geo")["tau"]}


# ---------------------------------------------------------------- q (L6)

def _series(df, geo_col, year_col, val_col) -> pd.Series:
    if not len(df):
        return pd.Series(dtype=float)
    return pd.Series(pd.to_numeric(df[val_col], errors="coerce").to_numpy(float),
                     index=pd.MultiIndex.from_arrays([df[geo_col].astype(str), df[year_col].astype(int)],
                                                     names=["geo", "year"]))


def jst_q(jst: pd.DataFrame, numerator: str = "rent") -> tuple[pd.Series, dict]:
    """log(rent index / cpi) (numerator 'rent') or log(house price / cpi) ('hpi') from JST, with L3 applied; the
    second item lists, per country, the q years that start a new segment because an interpolated capital gain was
    cumulated across them."""
    if not len(jst):
        return pd.Series(dtype=float), {}
    out, starts = [], {}
    for g, d in jst.groupby("geo"):
        d = d.sort_values("year").set_index("year")
        yd = pd.to_numeric(d["housing_rent_yd"], errors="coerce")
        cpi = pd.to_numeric(d["cpi"], errors="coerce")
        ipol_rent = pd.to_numeric(d["rent_ipolated"], errors="coerce").fillna(0) == 1
        new_seg = []
        if g in CAPGAIN_Q:
            gain = pd.to_numeric(d["housing_capgain"], errors="coerce")
            ipol = pd.to_numeric(d["housing_capgain_ipol"], errors="coerce").fillna(0) == 1
            level, lv, prev_ipol = [], np.nan, False
            for y in d.index:
                if not np.isfinite(gain.get(y, np.nan)):
                    lv = np.nan
                elif not np.isfinite(lv):
                    lv = 1.0
                else:
                    lv = lv * (1.0 + gain[y])
                level.append(lv)
                if prev_ipol and not ipol.get(y, False):
                    new_seg.append(int(y))
                prev_ipol = bool(ipol.get(y, False))
            hp = pd.Series(level, index=d.index)
            bad = ipol
        else:
            hp = pd.to_numeric(d["hpnom"], errors="coerce")
            bad = pd.Series(False, index=d.index)
        num = yd * hp if numerator == "rent" else hp
        with np.errstate(divide="ignore", invalid="ignore"):
            q = np.log(num / cpi)
        if numerator == "rent":
            q[ipol_rent] = np.nan
        q[bad] = np.nan
        for y in cv.JST_R6_MISSING.get(g, []):
            if y in q.index:
                q[y] = np.nan
        q = q.replace([np.inf, -np.inf], np.nan)
        out.append(pd.Series(q.to_numpy(float), index=pd.MultiIndex.from_arrays(
            [[g] * len(q), q.index.astype(int)], names=["geo", "year"])))
        if new_seg:
            starts[g] = new_seg
    return (pd.concat(out) if out else pd.Series(dtype=float)), starts


def ladder_q(c: str, jstq: pd.Series, num: pd.Series, cpi: pd.Series, c18: pd.Series,
             frozen: dict | None = None) -> tuple[dict, dict]:
    """({q year: value or NaN}, {q year: source}) for one country. frozen: the L2 ladder {q year: source} from
    data/coverage.json, which the openings always pass: sources and runs come from it, and a value that is missing or
    flagged is NaN inside its run. Without it (tests only) the ladder is computed from the values' availability."""
    def years(s):
        if not len(s) or c not in set(s.index.get_level_values(0)):
            return set(), pd.Series(dtype=float)
        x = s.xs(c, level=0)
        x = x[np.isfinite(x.to_numpy(float))]
        return set(int(y) for y in x.index), x
    jy, js = years(jstq)
    ry, rs = years(num)
    cy, cs = years(cpi)
    ky, ks = years(c18)
    if frozen is not None:
        lad = {int(y): str(src) for y, src in frozen.items()}
    else:
        lad = cv.q_ladder(c, {"jst": sorted(jy), "rpi": sorted(ry), "cpi": sorted(cy), "cpi2018": sorted(ky)})
    vals = {}
    for y, src in sorted(lad.items()):
        if src == "jst":
            vals[y] = float(js[y]) if y in jy else np.nan
        elif src == "rpi/cpi":
            vals[y] = float(np.log(rs[y] / cs[y])) if (y in ry and y in cy) else np.nan
        else:
            vals[y] = float(np.log(rs[y] / ks[y])) if (y in ry and y in ky) else np.nan
        if not np.isfinite(vals[y]):
            vals[y] = np.nan
    return vals, lad


def q_panel(raw: dict, geos, seg: pd.DataFrame, which: str = "rent",
            ladders: dict | None = None) -> tuple[pd.DataFrame, dict]:
    """Per country and q year: log q, its source and its segment (first q year of the segment), and the breaks of
    the lagged regressor in observation years. which='rent' (logq) or 'hpi' (logq_hpi). ladders: the frozen L2
    ladders {country: {q year: source}} (data/coverage.json); q_hpi takes the same sources (JST hpnom where the ladder
    names JST, OECD HPI over the named CPI elsewhere)."""
    house = raw.get("house", pd.DataFrame())
    meas = "RPI" if which == "rent" else "HPI"
    num, nb = cell(house, MEASURE=meas) if len(house) else (pd.Series(dtype=float), {})
    cpi, cb = cell(raw["cpi"]) if len(raw.get("cpi", [])) else (pd.Series(dtype=float), {})
    c18, kb = cell(raw["cpi2018"]) if len(raw.get("cpi2018", [])) else (pd.Series(dtype=float), {})
    jq, jstarts = jst_q(raw.get("jst", pd.DataFrame()), which)
    rows, breaks = [], {}
    doc_series = "q" if which == "rent" else "q_hpi"
    for c in sorted(geos):
        fz = None if ladders is None else (ladders.get(c) or {})
        vals, lad = ladder_q(c, jq, num, cpi, c18, fz)
        if not lad:
            continue
        segs = cv.q_segments(c, lad, seg[seg["series"] == doc_series].assign(series="q"))
        starts = {a for a, _ in segs}
        # values-arriving rules: B flags of the sources used (rung 2) and interpolated capital gains (JST)
        arriving = set(jstarts.get(c, []))
        for b in (nb, cb, kb):
            arriving |= {y for y in b.get(c, []) if y in lad and lad[y] != "jst"}
        starts |= {y for y in arriving if min(lad) < y <= max(lad)}
        starts = sorted(starts)
        for y in sorted(lad):
            s0 = max(s for s in starts if s <= y)
            rows.append(dict(geo=c, qyear=y, logq=vals[y], src=lad[y], seg=s0))
        breaks[c] = [s + 1 for s in starts[1:]]                # lagged: from observation year tau + 1
    return pd.DataFrame(rows, columns=["geo", "qyear", "logq", "src", "seg"]), breaks


# ---------------------------------------------------------------- school (L11)

def school(ilo: pd.DataFrame, seg: pd.DataFrame) -> tuple[pd.Series, dict]:
    if not len(ilo):
        return pd.Series(dtype=float), {}
    d = ilo.copy()
    d["time"] = pd.to_numeric(d["time"], errors="coerce").astype("Int64")
    d["obs_value"] = pd.to_numeric(d["obs_value"], errors="coerce")
    bad = d.get("obs_status", pd.Series("", index=d.index)).fillna("").astype(str).str.upper().isin(["E", "F", "I"])
    bad |= d.get("source", pd.Series("", index=d.index)).fillna("").astype(str).str.upper().str.startswith("EA")
    d.loc[bad, "obs_value"] = np.nan
    d = d[d["sex"].astype(str).isin(["SEX_T"]) & d["classif1"].astype(str).eq("AGE_YTHBANDS_Y20-24")]
    out, br = [], {}
    for g, e in d.groupby("geo"):
        p = e.pivot_table(index="time", columns="classif2", values="obs_value", aggfunc="first")
        yes = p.get("STU_EDU_YES", pd.Series(np.nan, index=p.index))
        no = p.get("STU_EDU_NO", pd.Series(np.nan, index=p.index))
        v = 100.0 * yes / (yes + no)
        out.append(pd.Series(v.to_numpy(float), index=pd.MultiIndex.from_arrays(
            [[g] * len(v), v.index.astype(int)], names=["geo", "year"])))
        src = e.dropna(subset=["obs_value"]).groupby("time")["source"].first().sort_index()
        sw = [int(y) for y, a, b in zip(src.index[1:], src.to_numpy()[:-1], src.to_numpy()[1:]) if a != b]
        flags = e[e.get("obs_status", pd.Series("", index=e.index)).fillna("").astype(str).str.upper() == "B"]
        br[g] = sorted(set(sw) | {int(y) for y in flags["time"].dropna()})
    s = pd.concat(out) if out else pd.Series(dtype=float)
    return s, _union(br, _doc_breaks(seg, ["school"]))


def cohort(wpp: pd.DataFrame) -> pd.Series:
    if not len(wpp):
        return pd.Series(dtype=float)
    d = wpp.copy()
    d["young"] = d["AgeGrpStart"].between(25, 30)
    d["mid"] = d["AgeGrpStart"].between(35, 60)
    g = d.groupby(["geo", "Time"])
    r = g.apply(lambda e: e.loc[e["young"], "PopTotal"].sum() / e.loc[e["mid"], "PopTotal"].sum(), include_groups=False)
    r.index = r.index.set_names(["geo", "year"])
    return r.astype(float)


# ---------------------------------------------------------------- the panel

def ladders_of(cube: dict) -> dict:
    """The frozen L2 ladders {country: {q year: source}} from data/coverage.json."""
    return {c: {int(y): s for y, s in v.get("q_ladder", {}).items()} for c, v in cube["countries"].items()}


def kholodilin_frame(kh: pd.DataFrame) -> pd.Series:
    """L12: strict (1/0) by (geo, year) from the confirmed Kholodilin coding (columns geo, year, strict)."""
    if kh is None or not len(kh):
        return pd.Series(dtype=float)
    d = kh.dropna(subset=["geo", "year"])
    st = pd.to_numeric(d["strict"], errors="coerce")
    if not st.dropna().isin([0, 1]).all():
        raise ValueError("Kholodilin strict must be 0 or 1 (first-generation control, the L2 definition)")
    return pd.Series(st.to_numpy(float), index=pd.MultiIndex.from_arrays(
        [d["geo"].astype(str), d["year"].astype(int)], names=["geo", "year"]))


def kholodilin_uncovered(raw: dict, geos) -> list[str]:
    """The countries the Kholodilin coding does not cover (they keep all their years; L12 lists them)."""
    kh = raw.get("kholodilin")
    if kh is None or not len(kh):
        return sorted(geos)
    return sorted(set(geos) - set(kh["geo"].astype(str)))


def panel(raw: dict, geos, seg: pd.DataFrame, ladders: dict | None = None) -> pd.DataFrame:
    """The country-year panel of section 3 (see the header). ladders: the frozen L2 ladders (opening passes them)."""
    geos = sorted(geos)
    v: dict = {}
    lfs_doc = _doc_breaks(seg, ["lfs"])
    old_doc = _doc_breaks(seg, ["lfs", "lfs_A5564"])
    act = raw.get("act", pd.DataFrame())
    if len(act):
        v["A2534"] = band(act, [dict(SEX=s, AGE=a) for s in "FM" for a in ("Y25T29", "Y30T34")])
        v["A2534_M"] = band(act, [dict(SEX="M", AGE=a) for a in ("Y25T29", "Y30T34")])
        v["A2534_F"] = band(act, [dict(SEX="F", AGE=a) for a in ("Y25T29", "Y30T34")])
        v["A5564"] = band(act, [dict(SEX=s, AGE=a) for s in "FM" for a in AGES_OLD])
        v["AW2554"] = band(act, [dict(SEX="F", AGE=a) for a in AGES_PRIME])
        v["AM2554"] = band(act, [dict(SEX="M", AGE=a) for a in AGES_PRIME])
        for k in ("A2534", "A2534_M", "A2534_F", "AW2554", "AM2554"):
            v[k] = (v[k][0], _union(v[k][1], lfs_doc))
        v["A5564"] = (v["A5564"][0], _union(v["A5564"][1], old_doc))
    une = raw.get("une", pd.DataFrame())
    if len(une):
        s, b = cell(une)
        v["U"] = (s, _union(b, lfs_doc))
    if len(raw.get("school", [])):
        v["school2024"] = school(raw["school"], seg)
    if len(raw.get("cohort", [])):
        v["cohort"] = (cohort(raw["cohort"]), {})
    if raw.get("kholodilin") is not None and len(raw["kholodilin"]):
        v["strict"] = (kholodilin_frame(raw["kholodilin"]), {})
    qcols = {}
    for which, name in (("rent", "logq_l1"), ("hpi", "logq_hpi_l1")):
        qp, qb = q_panel(raw, geos, seg, which, ladders)
        if len(qp):
            idx = pd.MultiIndex.from_arrays([qp["geo"], qp["qyear"] + 1], names=["geo", "year"])
            v[name] = (pd.Series(qp["logq"].to_numpy(float), index=idx), qb)
            qcols[name] = (pd.Series(qp["seg"].to_numpy(int), index=idx), pd.Series(qp["src"].to_numpy(), index=idx))
    grid = pd.MultiIndex.from_tuples([(c, y) for c in geos for y in fetch.window(c)], names=["geo", "year"])
    df = pd.DataFrame(index=grid)
    for name in VARIABLES:
        if name in v:
            s, b = v[name]
            s = s[~s.index.duplicated()] if len(s) else s
            df[name] = s.reindex(grid).to_numpy(float) if len(s) else np.nan
            df[name + "__breaks"] = [list(b.get(g, [])) for g in grid.get_level_values(0)]
        else:
            df[name] = np.nan
            df[name + "__breaks"] = [[] for _ in range(len(grid))]
    for name, suffix in (("logq_l1", ""), ("logq_hpi_l1", "_hpi")):
        if name in qcols:
            sseg, ssrc = qcols[name]
            df[f"qseg{suffix}_l1"] = sseg.reindex(grid).to_numpy(float)
            df[f"qsrc{suffix}_l1"] = ssrc.reindex(grid).to_numpy(object)
        else:
            df[f"qseg{suffix}_l1"] = np.nan
            df[f"qsrc{suffix}_l1"] = None
    return df


def q_only(raw: dict, geos, seg: pd.DataFrame, ladders: dict | None = None) -> pd.DataFrame:
    """The q columns alone (the opening computes the knots from these before any outcome exists, L14)."""
    return panel({k: raw[k] for k in REGRESSOR_IDS if k in raw}, geos, seg, ladders)[
        ["logq_l1", "logq_l1__breaks", "qseg_l1", "qsrc_l1"]]


def census(R: pd.DataFrame, qp: pd.DataFrame, seg: pd.DataFrame) -> pd.DataFrame:
    """LR-C1's frame: Extract B census rows with x = log q of the census year's previous year, its q segment, the
    census round (decade 1975-84, 1985-94, ...) and the coresid segment breaks."""
    if not len(R):
        return pd.DataFrame(columns=["geo", "year", "R", "x", "qseg", "round"])
    q = qp.reset_index() if "geo" not in qp.columns else qp
    cols = ["geo", "year", "logq_l1", "qseg_l1"] + [c for c in ("logq_hpi_l1", "strict") if c in q]
    m = R.merge(q[cols], on=["geo", "year"], how="left")
    m["round"] = ((m["year"] - 1975) // 10) * 10 + 1975
    doc = _doc_breaks(seg, ["coresid"])
    m["R__breaks"] = [doc.get(g, []) for g in m["geo"]]
    if "strict" not in m:
        m["strict"] = np.nan
    return m.rename(columns={"logq_l1": "x", "qseg_l1": "qseg", "logq_hpi_l1": "x_hpi"})


# ---------------------------------------------------------------- country level

def country_level(fl: dict, fl1970: dict | None, gn: pd.DataFrame | None, samples: dict, geos) -> pd.DataFrame:
    recs = {r["sample"]: r for r in samples.get("F_L", [])}
    rows = []
    for c in sorted(geos):
        d = fl.get(c, {})
        a = d.get("25-34", {})
        b = d.get("20-29", {})
        e = (fl1970 or {}).get(c, {}).get("25-34", {})
        flags = recs.get(a.get("sample"), {}).get("flags", [])
        g = np.nan
        if gn is not None and len(gn) and c in set(gn["geo"]):
            g = float(pd.to_numeric(gn.loc[gn["geo"] == c].iloc[0, 1:], errors="coerce").iloc[0])
        rows.append(dict(geo=c, stratum=fetch.stratum_of(c), F_L=a.get("value", np.nan), F_L_2029=b.get("value", np.nan),
                         F_L_year=a.get("year"), F_L_sample=a.get("sample"), F_L_flagged=bool(flags),
                         F_L_unusable=a.get("unusable", ""), F_L_1970=e.get("value", np.nan),
                         F_L_1970_year=e.get("year"), GN=g))
    return pd.DataFrame(rows).set_index("geo")


# ---------------------------------------------------------------- manifest

def manifest() -> dict:
    return {"written": str(date.today()), "protocol": "longrun/PROTOCOL.md section 3",
            "rule": "each OECD query pins every dimension but REF_AREA; European members end at 1994 (q flows 1993); "
                    "single-file sources are cut to the half's countries by their loaders",
            "entries": MANIFEST, "variables": VARIABLES}


def main() -> None:
    with open(MANIFEST_PATH, "w", encoding="utf-8", newline="\n") as f:
        json.dump(manifest(), f, indent=1)
        f.write("\n")
    print(f"{len(MANIFEST)} queries, {len(VARIABLES)} variables; wrote {MANIFEST_PATH}")


if __name__ == "__main__":
    main()
