# build.py — the variables of PROTOCOL.md sections 3 and 5, built from Eurostat through the guarded loader
# (code/eurostat.py). Every query the pipeline makes is in MANIFEST below; `main` writes it to data/manifest.json.
#
# country_year(half) -> DataFrame indexed by (geo, year): the panel variables (VARIABLES) and, for each, a companion
#   '<var>__breaks' holding the country's list of break years (C3: every year whose flag contains 'b' in any cell
#   that enters the variable; for a variable lagged one year the break years move one year later, for a lead one
#   year earlier). Rules applied here, so no test can forget them:
#   C2  2020 and 2021 dropped (lags and leads are taken on the full annual grid first); C1 the UK capped at 2019: its
#       raw cells after 2019 are removed before any variable, lag or lead is built (so no UK 2020 value reaches the
#       UK's 2019 lead), and its rows after 2019 leave the panel;
#   C4  cells flagged u or c are missing (eurostat.clean), with no interpolation;
#   C5  a band is the equal-weight mean of its five-year sub-bands and of the male and female rates, missing if any of
#       its cells is missing; LFS rates for nationals (citizen=NAT), all residents (TOTAL) as '<var>_all';
#   C6  q = log(HICP CP041 / HICP IGD_NNRG), INX_A_AVG, lagged one year ('logq_l1'); the lead 'logq_f1'; the
#       robustness measures log(HPI / CP00) ('logq_hpi_l1': prc_hpi_a TOTAL I15_A_AVG, I25_A_AVG for a country with
#       no I15 values (CH); tipsho20 I15_A_AVG for Greece), log(CP041 / CP00) ('logq_cp00_l1'),
#       log(CP041 / compensation per employee, D1_SAL_PER NAC) ('logq_comp_l1');
#   C7  U = unemployment rate 25-74, both sexes: une_rt_a (PC_ACT) for a country it covers, else lfsa_urgan Y25-74
#       citizen TOTAL for the whole series of that country (une_rt_a has no UK). Never spliced within a country.
#       U2554 (C-6) and U1529 (C-1 secondary) follow the same rule.
# country_level(half) -> DataFrame indexed by geo: stratum; F_raw (C9: ilc_lvps08 25-34 sex T, mean of the first three
#   available years within 2003-2008, in points; NaN if none); X_c (C-4: 100 x OC4 / TOTAL employed at 15-24,
#   lfsa_egais, mean of the available years of 2018-2019); aging_pred (C-5: the 2011 single-year structure aged eight
#   years, no migration or mortality: pop(48+)/pop(13-47) minus pop(56+)/pop(21-55), all of 2011); routine_change
#   (C-5: 100 x (OC4+OC7+OC8) / TOTAL at 15-64, 2019 minus 2011, points) with routine_breaks (the years in 2012-2019
#   with a 'b' flag on any of those cells: a break inside the window that the change spans; recorded and reported,
#   PROTOCOL C3 being written for panels, see specs.py); student_indep (C-6 secondary: 1 - ilc_lvps09
#   EDUC 18-24 / 100, first three years within 2003-2008); owner_outright_5564 (C-1 secondary: ilc_lvps05 OWN_NL
#   55-64 sex T, mean of 2015-2017, points; not predetermined).
#   F_c (also a column here, standardised over the countries loaded, for convenience) is standardised for the tests in
#   specs.py from F_raw, with the constants of the run. During exploration that is the explore half's mean and sd; at the look,
#   confirm.py computes the full-sample (31-country) mean and sd once and uses them for the full sample and the
#   confirm half alike. A linear rescaling of F changes b2's units but neither its t statistic nor any p-value.
#
# half: 'explore' reads the explore countries of data/split.json; 'confirm' reads all 31 countries in one vintage (the
# look's full sample; confirm.py takes the confirm half from it). The guard in eurostat.get decides whether either is
# open. Nothing here writes a file except through eurostat's cache and log.
#
# Run from participation/:  ../venv/Scripts/python.exe code/build.py      (writes data/manifest.json; fetches nothing)
# Out: data/manifest.json

from __future__ import annotations

import json
import os
import sys
from datetime import date

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import eurostat as es  # noqa: E402

MANIFEST_PATH = os.path.join(ROOT, "data", "manifest.json")
YEARS = list(range(1995, 2026))              # the annual grid before C2's drop
DROP_YEARS = (2020, 2021)                    # C2
UK_LAST = 2019                               # C1

AGES_PRIME = ["Y25-29", "Y30-34", "Y35-39", "Y40-44", "Y45-49", "Y50-54"]
AGES_OLD = ["Y55-59", "Y60-64"]
AGES_POP = [f"Y{a}" for a in range(13, 100)] + ["Y_OPEN"]

# Every Eurostat query of the pipeline. 'dimensions' were verified on 2026-10-08 against the SDMX structure endpoint
# (https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/dataflow/ESTAT/<CODE>/latest?references=descendants
# &detail=referencepartial; metadata only), as were the codes in 'filters' and 'absent' (countries of C1 missing from
# the dataset's geo codelist, left out of the query). 'only': the query is made for these countries alone.
MANIFEST = [
    dict(id="act", dataset="lfsa_argan", dimensions=["freq", "unit", "sex", "age", "citizen", "geo"],
         filters={"unit": "PC", "sex": ["M", "F"], "age": AGES_PRIME + AGES_OLD, "citizen": ["NAT", "TOTAL"]},
         use="activity rates (C5): A2534, A5564, AW2554, AM2554 and their all-residents twins"),
    dict(id="emp", dataset="lfsa_ergan", dimensions=["freq", "unit", "sex", "age", "citizen", "geo"],
         filters={"unit": "PC", "sex": ["M", "F"], "age": ["Y20-24"] + AGES_PRIME, "citizen": ["NAT", "TOTAL"]},
         use="employment rates (C5): E2024, E2554 and their all-residents twins"),
    dict(id="une", dataset="une_rt_a", dimensions=["freq", "age", "unit", "sex", "geo"], absent=["UK"],
         filters={"unit": "PC_ACT", "sex": "T", "age": ["Y25-74", "Y25-54", "Y15-29"]},
         use="unemployment rates (C7): U, U2554, U1529"),
    dict(id="une_lfs", dataset="lfsa_urgan", dimensions=["freq", "unit", "sex", "age", "citizen", "geo"],
         filters={"unit": "PC", "sex": "T", "age": ["Y25-74", "Y25-54", "Y15-29"], "citizen": "TOTAL"},
         use="unemployment rates, C7's fallback for a country une_rt_a does not cover"),
    dict(id="hicp", dataset="prc_hicp_aind", dimensions=["freq", "unit", "coicop", "geo"],
         filters={"unit": "INX_A_AVG", "coicop": ["CP041", "IGD_NNRG", "CP00"]},
         use="q (C6) and the alternatives log(CP041/CP00), the HICP deflator of log(HPI/HICP)"),
    dict(id="hpi", dataset="prc_hpi_a", dimensions=["freq", "purchase", "unit", "geo"], absent=["EL"],
         filters={"purchase": "TOTAL", "unit": ["I15_A_AVG", "I25_A_AVG"]},
         use="house price index for the robustness q log(HPI/HICP)"),
    dict(id="hpi_el", dataset="tipsho20", dimensions=["freq", "unit", "geo"], only=["EL"],
         filters={"unit": "I15_A_AVG"},
         use="house price index of Greece (C6)"),
    dict(id="comp", dataset="nama_10_lp_ulc", dimensions=["freq", "unit", "na_item", "geo"],
         filters={"na_item": "D1_SAL_PER", "unit": "NAC"},
         use="compensation per employee for the robustness q log(CP041/compensation)"),
    dict(id="cores", dataset="ilc_lvps08", dimensions=["freq", "age", "sex", "unit", "geo"],
         filters={"age": "Y25-34", "sex": "T", "unit": "PC"},
         use="coresidence 25-34 (C-1 outcome) and F_c (C9)"),
    dict(id="tenure", dataset="ilc_lvps05", dimensions=["freq", "tenure", "sex", "age", "unit", "geo"],
         filters={"tenure": "OWN_NL", "sex": "T", "age": "Y55-64", "unit": "PC"},
         use="outright-owner share 55-64 (C-1 secondary)"),
    dict(id="stud", dataset="ilc_lvps09", dimensions=["freq", "wstatus", "age", "unit", "geo"],
         filters={"wstatus": "EDUC", "age": "Y18-24", "unit": "PC"},
         use="students 18-24 living with their parents (C-6 secondary)"),
    dict(id="educ", dataset="edat_lfse_19", dimensions=["freq", "sex", "age", "wstatus", "training", "unit", "geo"],
         filters={"sex": "T", "age": "Y20-24", "wstatus": "POP", "training": "FE", "unit": "PC"},
         use="share of 20-24 in formal education (C-6 outcome)"),
    dict(id="occ", dataset="lfsa_egais", dimensions=["freq", "unit", "sex", "age", "wstatus", "isco08", "geo"],
         filters={"unit": "THS_PER", "sex": "T", "age": ["Y15-24", "Y15-64"], "wstatus": "EMP",
                  "isco08": ["OC4", "OC7", "OC8", "TOTAL"]},
         use="clerical exposure X_c at 15-24 (C-4); routine share change at 15-64 (C-5)"),
    dict(id="pop", dataset="demo_pjan", dimensions=["freq", "unit", "age", "sex", "geo"], since=2011,
         filters={"unit": "NR", "sex": "T", "age": AGES_POP},
         use="2011 single-year population for predicted aging (C-5)"),
]
BY_ID = {m["id"]: m for m in MANIFEST}

# Panel variables: name -> (manifest ids it is built from, what it is).
VARIABLES = {
    "A2534": (["act"], "activity rate 25-34, nationals: mean of M/F x 25-29, 30-34 (pp)"),
    "A5564": (["act"], "activity rate 55-64, nationals: mean of M/F x 55-59, 60-64"),
    "AW2554": (["act"], "activity rate of women 25-54, nationals: mean of the six five-year bands"),
    "AM2554": (["act"], "activity rate of men 25-54, nationals: mean of the six five-year bands"),
    "A2534_all": (["act"], "A2534, all residents (citizen TOTAL)"),
    "A5564_all": (["act"], "A5564, all residents"),
    "AW2554_all": (["act"], "AW2554, all residents"),
    "AM2554_all": (["act"], "AM2554, all residents"),
    "E2024": (["emp"], "employment rate 20-24, nationals: mean of M/F"),
    "E2554": (["emp"], "employment rate 25-54, nationals: mean of M/F x six bands"),
    "E2024_all": (["emp"], "E2024, all residents"),
    "E2554_all": (["emp"], "E2554, all residents"),
    "U": (["une", "une_lfs"], "unemployment rate 25-74, both sexes (C7)"),
    "U2554": (["une", "une_lfs"], "unemployment rate 25-54, both sexes"),
    "U1529": (["une", "une_lfs"], "unemployment rate 15-29, both sexes"),
    "logq": (["hicp"], "log(CP041 / IGD_NNRG), year t"),
    "logq_l1": (["hicp"], "q of C6: log(CP041 / IGD_NNRG) of year t-1"),
    "logq_f1": (["hicp"], "the lead: log(CP041 / IGD_NNRG) of year t+1"),
    "logq_hpi_l1": (["hpi", "hpi_el", "hicp"], "log(HPI / CP00), t-1"),
    "logq_cp00_l1": (["hicp"], "log(CP041 / CP00), t-1"),
    "logq_comp_l1": (["hicp", "comp"], "log(CP041 / compensation per employee), t-1"),
    "coresid2534": (["cores"], "share of 25-34 living with their parents, sex T (pp)"),
    "educ2024": (["educ"], "share of 20-24 in formal education (pp)"),
}
LEVEL = {
    "F_raw": (["cores"], "C9 floor availability, raw (pp)"),
    "X_c": (["occ"], "C-4 clerical exposure at 15-24 (pp)"),
    "aging_pred": (["pop"], "C-5 predicted aging"),
    "routine_change": (["occ"], "C-5 change in routine share 2011-2019 (pp)"),
    "student_indep": (["stud"], "C-6 secondary: 1 - share of students 18-24 living with parents"),
    "owner_outright_5564": (["tenure"], "C-1 secondary: outright-owner share 55-64 (pp)"),
}

_RAW: dict = {}                               # half -> {manifest id: long frame}; one fetch per half per process


def reset() -> None:
    _RAW.clear()


def geos_for(half: str) -> list[str]:
    if half == "explore":
        return sorted(json.load(open(os.path.join(ROOT, "data", "split.json"), encoding="utf-8"))["explore"])
    if half == "confirm":
        return list(es.COUNTRIES)
    raise ValueError(f"build reads half 'explore' or 'confirm', not {half!r}")


def query_geos(m: dict, geos: list[str]) -> list[str]:
    g = [c for c in geos if c not in m.get("absent", [])]
    return [c for c in g if c in m["only"]] if "only" in m else g


def fetch(half: str) -> dict:
    """All manifest queries for this half through eurostat.get (guarded, cached, logged); memoised per process."""
    if half not in _RAW:
        geos, out = geos_for(half), {}
        for m in MANIFEST:
            g = query_geos(m, geos)
            out[m["id"]] = (es.get(m["dataset"], m["filters"], g, half=half, since=m.get("since")) if g
                            else pd.DataFrame(columns=["geo", "year", "value", "flag"]))
        _RAW[half] = out
    return _RAW[half]


# ---------------------------------------------------------------- cells, bands, breaks

def cap_uk(raw: dict) -> dict:
    """C1: the raw frames without the UK's cells after 2019 (values and flags), before anything is built from them."""
    out = {}
    for k, df in raw.items():
        if len(df) and "geo" in df and "year" in df:
            df = df[~((df["geo"] == "UK") & (pd.to_numeric(df["year"], errors="coerce") > UK_LAST))]
        out[k] = df
    return out


def cell(df: pd.DataFrame, **sel) -> tuple[pd.Series, dict]:
    """One cell series: (clean values indexed by (geo, year), {geo: [break years]}). C4 applied, flags kept for C3."""
    d = df
    for k, v in sel.items():
        d = d[d[k] == v]
    d = d.dropna(subset=["year"])
    idx = pd.MultiIndex.from_arrays([d["geo"].astype(str), d["year"].astype(int)], names=["geo", "year"])
    c = es.clean(d)
    s = pd.Series(c["value"].to_numpy(float), index=idx)
    s = s[~s.index.duplicated()]
    return s, es.break_years(d)


def _union(*bs: dict) -> dict:
    out: dict = {}
    for b in bs:
        for g, ys in b.items():
            out.setdefault(g, set()).update(int(y) for y in ys)
    return {g: sorted(v) for g, v in out.items()}


def band(df: pd.DataFrame, cells: list[dict]) -> tuple[pd.Series, dict]:
    """Equal-weight mean of the cells (C5); missing where any cell is missing; breaks the union over the cells."""
    parts = [cell(df, **c) for c in cells]
    if not parts:
        raise ValueError("a band needs cells")
    frame = pd.concat([p[0] for p in parts], axis=1)
    return frame.mean(axis=1, skipna=False), _union(*[p[1] for p in parts])


def _shift(s: pd.Series, b: dict, k: int) -> tuple[pd.Series, dict]:
    """The series of year t-k placed at year t (k=1: lag; k=-1: lead); break years move by k."""
    s2 = s.copy()
    if not len(s):
        return s2, {g: sorted(y + k for y in ys) for g, ys in b.items()}
    s2.index = pd.MultiIndex.from_arrays([s.index.get_level_values(0), s.index.get_level_values(1) + k],
                                         names=["geo", "year"])
    return s2, {g: sorted(y + k for y in ys) for g, ys in b.items()}


def _by_country(primary: tuple, fallback: tuple, geos) -> tuple[pd.Series, dict]:
    """C7's rule: the primary source for a country it covers (any finite value), else the fallback, whole series."""
    (s1, b1), (s2, b2) = primary, fallback
    have = set(s1[np.isfinite(s1)].index.get_level_values(0))
    parts, br = [], {}
    for g in geos:
        s, b = (s1, b1) if g in have else (s2, b2)
        if g in set(s.index.get_level_values(0)):
            parts.append(s.xs(g, level=0, drop_level=False))
        if g in b:
            br[g] = b[g]
    return (pd.concat(parts) if parts else pd.Series(dtype=float)), br


def _ratio_log(num: tuple, den: tuple) -> tuple[pd.Series, dict]:
    if not len(num[0]) or not len(den[0]):
        return pd.Series(dtype=float), _union(num[1], den[1])
    a, b = num[0].align(den[0], join="outer")
    with np.errstate(divide="ignore", invalid="ignore"):
        v = np.log(a.to_numpy(float)) - np.log(b.to_numpy(float))
    return pd.Series(np.where(np.isfinite(v), v, np.nan), index=a.index), _union(num[1], den[1])


def _per_country_unit(df: pd.DataFrame, units: list[str], **sel) -> tuple[pd.Series, dict]:
    """The first unit (in order) a country has any finite value in, for that country's whole series."""
    out = None
    for u in reversed(units):
        s = cell(df, unit=u, **sel)
        out = s if out is None else _by_country(s, out, sorted(set(df["geo"])))
    return out


# ---------------------------------------------------------------- the panel

def panel_variables(raw: dict, geos: list[str]) -> dict:
    """name -> (series indexed (geo, year), {geo: [break years]}) for every name in VARIABLES."""
    act, emp = raw["act"], raw["emp"]
    v = {}
    for suf, cz in (("", "NAT"), ("_all", "TOTAL")):
        v["A2534" + suf] = band(act, [dict(sex=s, age=a, citizen=cz) for s in "MF" for a in ("Y25-29", "Y30-34")])
        v["A5564" + suf] = band(act, [dict(sex=s, age=a, citizen=cz) for s in "MF" for a in AGES_OLD])
        v["AW2554" + suf] = band(act, [dict(sex="F", age=a, citizen=cz) for a in AGES_PRIME])
        v["AM2554" + suf] = band(act, [dict(sex="M", age=a, citizen=cz) for a in AGES_PRIME])
        v["E2024" + suf] = band(emp, [dict(sex=s, age="Y20-24", citizen=cz) for s in "MF"])
        v["E2554" + suf] = band(emp, [dict(sex=s, age=a, citizen=cz) for s in "MF" for a in AGES_PRIME])
    for name, age in (("U", "Y25-74"), ("U2554", "Y25-54"), ("U1529", "Y15-29")):
        v[name] = _by_country(cell(raw["une"], age=age), cell(raw["une_lfs"], age=age), geos)
    h = raw["hicp"]
    cp041, nnrg, cp00 = (cell(h, coicop=c) for c in ("CP041", "IGD_NNRG", "CP00"))
    q = _ratio_log(cp041, nnrg)
    v["logq"] = q
    v["logq_l1"] = _shift(*q, 1)
    v["logq_f1"] = _shift(*q, -1)
    hpi = _per_country_unit(raw["hpi"], ["I15_A_AVG", "I25_A_AVG"]) if len(raw["hpi"]) else (pd.Series(dtype=float), {})
    if len(raw["hpi_el"]):
        el = cell(raw["hpi_el"], unit="I15_A_AVG")
        hpi = (pd.concat([hpi[0], el[0]]), _union(hpi[1], el[1]))
    v["logq_hpi_l1"] = _shift(*_ratio_log(hpi, cp00), 1)
    v["logq_cp00_l1"] = _shift(*_ratio_log(cp041, cp00), 1)
    v["logq_comp_l1"] = _shift(*_ratio_log(cp041, cell(raw["comp"]) if len(raw["comp"]) else
                                           (pd.Series(dtype=float), {})), 1)
    v["coresid2534"] = cell(raw["cores"])
    v["educ2024"] = cell(raw["educ"])
    assert set(v) == set(VARIABLES)
    return v


def assemble(v: dict, geos: list[str]) -> pd.DataFrame:
    grid = pd.MultiIndex.from_product([sorted(geos), YEARS], names=["geo", "year"])
    df = pd.DataFrame(index=grid)
    for name, (s, b) in v.items():
        s = s[~s.index.duplicated()] if len(s) else s
        df[name] = s.reindex(grid).to_numpy(float) if len(s) else np.nan
        df[name + "__breaks"] = [list(b.get(g, [])) for g in grid.get_level_values(0)]
    yr, geo = grid.get_level_values(1), grid.get_level_values(0)
    keep = ~np.isin(yr, DROP_YEARS) & ~((geo == "UK") & (yr > UK_LAST))
    return df[keep]


def country_year(half: str, raw: dict | None = None, geos: list[str] | None = None) -> pd.DataFrame:
    """The panel of this half (see the header). raw/geos: for checks and simulations (raw frames by manifest id)."""
    geos = geos_for(half) if geos is None else geos
    raw = cap_uk(fetch(half) if raw is None else raw)
    return assemble(panel_variables(raw, geos), geos)


# ---------------------------------------------------------------- country level

def first_three(s: pd.Series, lo: int = 2003, hi: int = 2008) -> tuple[float, list[int]]:
    """C9: mean of the first three available (finite) years within [lo, hi]; NaN if none."""
    s = s[(s.index >= lo) & (s.index <= hi)].dropna().sort_index()
    yrs = [int(y) for y in s.index[:3]]
    return (float(s.iloc[:3].mean()) if yrs else np.nan), yrs


def _years_mean(s: pd.Series, years) -> float:
    s = s[s.index.isin(list(years))].dropna()
    return float(s.mean()) if len(s) else np.nan


def country_level(half: str, raw: dict | None = None, geos: list[str] | None = None) -> pd.DataFrame:
    geos = geos_for(half) if geos is None else geos
    raw = cap_uk(fetch(half) if raw is None else raw)
    stratum = {c: s for s, cs in es.STRATA.items() for c in cs}
    cores, _ = cell(raw["cores"])
    stud, _ = cell(raw["stud"])
    own, _ = cell(raw["tenure"])
    occ = raw["occ"]
    oc = {(a, i): cell(occ, age=a, isco08=i)[0] for a in ("Y15-24", "Y15-64") for i in ("OC4", "OC7", "OC8", "TOTAL")}
    rb = _union(*[cell(occ, age="Y15-64", isco08=i)[1] for i in ("OC4", "OC7", "OC8", "TOTAL")])
    pop = raw["pop"]
    rows = []
    for g in geos:
        def ser(s):
            return s.xs(g, level=0) if g in set(s.index.get_level_values(0)) else pd.Series(dtype=float)
        F, Fy = first_three(ser(cores))
        S, Sy = first_three(ser(stud))
        x = 100 * ser(oc[("Y15-24", "OC4")]) / ser(oc[("Y15-24", "TOTAL")])
        r = 100 * (ser(oc[("Y15-64", "OC4")]) + ser(oc[("Y15-64", "OC7")]) + ser(oc[("Y15-64", "OC8")])) \
            / ser(oc[("Y15-64", "TOTAL")])
        rows.append(dict(geo=g, stratum=stratum[g], F_raw=F, F_years=Fy,
                         X_c=_years_mean(x, (2018, 2019)),
                         aging_pred=aging(pop, g),
                         routine_change=(float(r.get(2019, np.nan) - r.get(2011, np.nan)) if len(r) else np.nan),
                         routine_breaks=[y for y in rb.get(g, []) if 2011 < y <= 2019],
                         student_indep=(1 - S / 100) if np.isfinite(S) else np.nan, student_years=Sy,
                         owner_outright_5564=_years_mean(ser(own), (2015, 2016, 2017))))
    out = pd.DataFrame(rows).set_index("geo")
    f = out["F_raw"].dropna()                 # convenience only: specs.py standardises F_raw with its run's constants
    out["F_c"] = (out["F_raw"] - f.mean()) / f.std(ddof=0) if len(f) > 1 else np.nan
    return out


def aging(pop: pd.DataFrame, g: str) -> float:
    """C-5 predicted aging from the 2011 single-year structure: aged 8 years, no migration, no mortality."""
    if not len(pop):
        return np.nan
    d = es.clean(pop[(pop["geo"] == g) & (pop["year"] == 2011)])
    n = {a: float(v) for a, v in zip(d["age"], d["value"])}
    if any(not np.isfinite(n.get(a, np.nan)) for a in AGES_POP):
        return np.nan
    age = {a: (100 if a == "Y_OPEN" else int(a[1:])) for a in AGES_POP}

    def tot(lo, hi=999):
        return sum(n[a] for a in AGES_POP if lo <= age[a] <= hi)
    return tot(48) / tot(13, 47) - tot(56) / tot(21, 55)


# ---------------------------------------------------------------- manifest

def manifest() -> dict:
    return {"written": str(date.today()), "protocol": "PROTOCOL.md sections 3 and 5",
            "structure_endpoint": "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1/dataflow/ESTAT/<CODE>/"
                                  "latest?references=descendants&detail=referencepartial (dimensions and codes "
                                  "verified 2026-10-08, metadata only)",
            "rule": "each query pins every dimension but freq and geo; geo is the half's countries minus 'absent' "
                    "(or only 'only'); no time filter except 'since'",
            "entries": MANIFEST,
            "variables": {k: {"from": v[0], "what": v[1]} for k, v in VARIABLES.items()},
            "country_level": {k: {"from": v[0], "what": v[1]} for k, v in LEVEL.items()}}


def main() -> None:
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest(), f, indent=1)
        f.write("\n")
    print(f"{len(MANIFEST)} queries, {len(VARIABLES)} panel variables, {len(LEVEL)} country-level variables")
    print(f"wrote {MANIFEST_PATH}")


if __name__ == "__main__":
    main()
