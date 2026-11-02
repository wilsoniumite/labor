# acquire_fin.py — vendor the Finnish and European tables for the consumption thread, then build tidy long files
# from the raw files only:
#   * Statistics Finland (StatFin PxWeb API): Household Budget Survey 2022 by income quintile (ktutk 14pg, 14qa),
#     income-distribution household composition (tjt 12ew, 152w, 128c, 14ya), the 2023 wealth survey by income
#     decile and by tenure (vtutk 151u, 151z), land in the national balance sheet (rtp 11zx), plot and dwelling
#     prices by plot ownership (kihi 11jc, ashi 12de, 13mw), national-accounts household consumption by COICOP 2018
#     (ntp 15ag), plus documentation and release pages from stat.fi;
#   * Eurostat (dissemination API, JSON-stat): nama_10_co3_p3 (COICOP 1999) and its COICOP 2018 successor
#     nama_10_cp18 for FI, SE, DK, DE, EU27_2020, 2015 onward; Finland's non-financial balance sheets
#     (nama_10_nfa_bs) for the land search.
# PxWeb status symbols kept in the tidy files: '.' missing, '..' not applicable, '...' confidential,
# '.....' not asked. Documentation of every output: consumption/data/tidy/README_fin.md.
#
# Run from the repo root:  venv/bin/python -I consumption/code/acquire_fin.py
# Downloads skip files already vendored, so a rerun is offline and rebuilds every tidy file from raw.
# Plain functions and top-level code (notebook-cell friendly). No modelling here.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import fetch, manifest_row, ua_for, RAW, TIDY

import itertools
import json
import re
import time
from urllib.parse import quote, urlencode

import numpy as np
import pandas as pd
import requests
from tqdm.auto import tqdm

SF = "statfin"
ES = "eurostat"
PX = "https://pxdata.stat.fi/PxWeb/api/v1/en"
ESTAT = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data"
PAUSE = 1.6        # StatFin PxWeb allows 40 calls per 60 s (api/v1/en/?config: maxCalls 40, timeWindow 60)
TIDY.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------------------------------------
# 1. Download helpers. GETs go through common.fetch(); PxWeb data queries are POSTs, sent here with the same
#    User-Agent rule (common.ua_for) and recorded with common.manifest_row(). Both skip vendored files.
# ---------------------------------------------------------------------------------------------------------
def get(source, rel, url, what, used_for):
    """common.fetch() plus a pause after a real download (StatFin rate limit)."""
    fresh = not (RAW / source / rel).exists()
    path = fetch(source, rel, url, what, used_for)
    if fresh:
        time.sleep(PAUSE)
    return path


def px_post(source, rel, url, query, what, used_for, tries=4, timeout=180):
    """POST a PxWeb query, vendor the response body, record it (with the POST body) in the manifest."""
    path = RAW / source / rel
    if path.exists():
        return path
    path.parent.mkdir(parents=True, exist_ok=True)
    last = None
    for k in range(tries):
        try:
            r = requests.post(url, json=query, headers={"User-Agent": ua_for(url)}, timeout=timeout)
        except requests.RequestException as e:
            last = repr(e)
            time.sleep(5 * (k + 1))
            continue
        if r.status_code == 429 or r.status_code >= 500:
            last = f"HTTP {r.status_code}"
            time.sleep(5 * (k + 1))
            continue
        if not r.ok:   # 4xx other than 429: stop and report, never retry around it
            raise RuntimeError(f"POST {url} -> HTTP {r.status_code}: {r.text[:300]}")
        path.write_bytes(r.content)
        body = json.dumps(query, separators=(",", ":"))
        manifest_row(source, rel, url, f"{what} | POST body: {body}", used_for)
        time.sleep(PAUSE)
        return path
    raise RuntimeError(f"POST failed after {tries} tries: {url} ({last})")


def px_query(meta, overrides=None):
    """PxWeb JSON-stat2 query selecting every value of every variable, except overrides {code: [values]}.
    Every variable is listed explicitly: a variable left out of the query is eliminated to its total."""
    overrides = overrides or {}
    codes = {v["code"]: v["values"] for v in meta["variables"]}
    for c, vals in overrides.items():
        assert c in codes, f"override variable {c} not in table"
        missing = [x for x in vals if x not in codes[c]]
        assert not missing, f"override values {missing} not in variable {c}"
    q = []
    for v in meta["variables"]:
        if v["code"] in overrides:
            q.append({"code": v["code"], "selection": {"filter": "item", "values": overrides[v["code"]]}})
        else:
            q.append({"code": v["code"], "selection": {"filter": "all", "values": ["*"]}})
    return {"query": q, "response": {"format": "json-stat2"}}


# ---------------------------------------------------------------------------------------------------------
# 2. Download lists
# ---------------------------------------------------------------------------------------------------------
# 2a. StatFin database listings and table searches (provenance: what exists, what was looked for)
LISTINGS = ["", "ktutk", "tjt", "vtutk", "rtp", "kihi", "ashi", "ntp"]
SEARCHES = ["land", "plot", "plots", "property tax", "real estate tax", "taxable value", "building land",
            "land area", "forest", "dwelling stock"]

# 2b. StatFin tables: (db, table, overrides, what_it_is, used_for). Metadata (GET) and data (POST, JSON-stat2).
PX_TABLES = [
    ("ktutk", "14pg", {},
     "HBS (Households' consumption) table 14pg: household consumption expenditure by income quintile, COICOP2018, "
     "2012/2016/2022, per household and per consumption unit, year and month, current and 2022 prices, shares",
     "fi_hbs2022_long.csv"),
    ("ktutk", "14qa", {},
     "HBS table 14qa: background information by income quintile (households in sample and population, average "
     "household size, average OECD-modified consumption units, disposable income per household), 2012/2016/2022",
     "fi_hh_composition.csv"),
    ("tjt", "12ew", {},
     "Income distribution statistics (sample data) table 12ew: households and persons by income decile and "
     "household's stage in life, 1989-2024", "fi_hh_composition.csv"),
    ("tjt", "152w", {},
     "Income distribution statistics (sample data) table 152w: housing costs and indicators by income quintile "
     "(households, persons, size, floor area, disposable money income per consumption unit), 2002-2024",
     "fi_hh_composition.csv"),
    ("tjt", "128c", {},
     "Income distribution statistics (register-based total data) table 128c: income and income structure of "
     "household-dwelling units by income decile (units, persons, size, consumption units, income items), 1995-2024",
     "fi_hh_composition.csv"),
    ("tjt", "14ya", {},
     "Income distribution statistics (register-based total data) table 14ya: persons by income decile, age group "
     "(0-17, 18-64, 65-) and origin, 1995-2024", "fi_hh_composition.csv"),
    ("vtutk", "151u", {},
     "Households' assets (wealth survey) table 151u: assets, liabilities and income of households by income decile, "
     "waves 1987-2023", "fi_wealth_2023_deciles.csv; fi_hh_composition.csv"),
    ("vtutk", "151z", {},
     "Households' assets (wealth survey) table 151z: assets, liabilities and income of households by housing tenure, "
     "waves 1987-2023", "fi_wealth_2023_tenure.csv"),
    ("rtp", "11zx", {},
     "Financial accounts table 11zx: non-financial assets by sector and instrument (incl. N111 residential "
     "buildings, N211 land), stocks and changes, 1995-2025", "fi_nonfin_assets_long.csv"),
    ("kihi", "11jc", {},
     "Real estate prices table 11jc: price index, prices per m2, quartiles, average area and number of sales of "
     "single-family house plots, yearly, 2015-2025", "fi_land_indicators_long.csv"),
    ("ashi", "12de", {},
     "Prices of dwellings in housing companies table 12de: prices per m2 of new dwellings by form of ownership of "
     "plot (own/rented), 2015-2025", "fi_land_indicators_long.csv"),
    ("ashi", "13mw", {"alue_43_20220407": ["ksu", "pks", "msu", "kas", "muu"]},
     "Prices of dwellings in housing companies table 13mw: prices per m2 of old dwellings by form of ownership of "
     "plot (own/rented), 2009-2025; national and aggregate regions only (whole country, Greater Helsinki, "
     "country excl. Greater Helsinki, major cities, country excl. major cities)", "fi_land_indicators_long.csv"),
    ("ntp", "15ag", {"kestavyys_1_20180101": ["SSS"],
                     "timeperiod_y": [str(y) for y in range(2015, 2026)],
                     "contentscode": ["ntp-cp", "ntp-fp", "ntp-vv_hinta_uusin_kul"]},
     "Annual national accounts table 15ag: household final consumption expenditure by COICOP2018 (all levels) and "
     "transaction (domestic, national, residents abroad, non-residents), durability total, 2015-2025; current "
     "prices, previous-year prices, volume series reference year 2025",
     "fi_na_hfce_coicop2018_long.csv; Eurostat FI cross-check"),
]

# 2c. stat.fi documentation and release pages (English paths; robots.txt excludes /tilasto/dokumentaatio/)
SF_DOCS = [
    ("docs/pxweb_api_config.json", f"{PX}/?config", "StatFin PxWeb API configuration (query limits)",
     "rate limit used by this script"),
    ("docs/stat.fi_robots.txt", "https://stat.fi/robots.txt", "stat.fi robots.txt",
     "which stat.fi paths scripts should not fetch (Finnish documentation path, search)"),
    ("docs/documentation_ktutk_en.html", "https://stat.fi/en/statistics/documentation/ktutk",
     "Households' consumption (HBS): documentation of statistics (SIMS quality report, concepts)",
     "definitions (README_fin.md)"),
    ("docs/documentation_tjt_en.html", "https://stat.fi/en/statistics/documentation/tjt",
     "Income distribution statistics: documentation of statistics (concepts incl. income deciles)",
     "decile definition (README_fin.md)"),
    ("docs/documentation_vtutk_en.html", "https://stat.fi/en/statistics/documentation/vtutk",
     "Households' assets: documentation of statistics (asset items, valuation methods)",
     "wealth definitions and valuation (README_fin.md)"),
    ("docs/documentation_rtp_en.html", "https://stat.fi/en/statistics/documentation/rtp",
     "Financial accounts: documentation of statistics", "non-financial assets context (README_fin.md)"),
    ("docs/release_ktutk_2022_2024-04-11.html", "https://stat.fi/en/publication/clmyi6vct7jjp0cutgh4ngdsb",
     "Release 'Nearly one-fifth of lowest-income households' consumption expenditure was spent on food in 2022' "
     "(Households' consumption 2022, 11/04/2024)", "headline cross-checks (fi_checks.csv)"),
    ("docs/release_ktutk_2022_preliminary_2023-12-28.html", "https://stat.fi/en/publication/cl8mrlcn2z9uh0dut08bwq5qf",
     "Release 'Consumption expenditure of childless couples aged under 65 highest in 2022' (preliminary data, "
     "28/12/2023)", "vintage note: preliminary totals (fi_checks.csv)"),
    ("docs/change_ktutk_2024-04-11.html",
     "https://stat.fi/en/documentation/changes-in-statistics/clus80hzl971j07w7cxjobw3g",
     "Change notice: HBS new database tables published, old tables archived (11/04/2024)",
     "table lineage (14pg replaces archived 007)"),
    ("docs/release_vtutk_2023_2025-03-12.html", "https://stat.fi/en/publication/cm1hek7m45vlf07vxdwvayu3c",
     "Release 'One-half of households had a net wealth of over EUR 96 000 in 2023' (Households' assets 2023, "
     "12/03/2025)", "headline cross-checks (fi_checks.csv)"),
    ("docs/article_2008-03-12_kulutuserot_fi.html", "https://stat.fi/artikkelit/2008/art_2008-03-12_003.html",
     "Statistics Finland article (2008, Finnish) on HBS 2006 consumption by income decile; states how HBS income "
     "groups were formed (household disposable income per consumption unit; households ranked, equal-size groups)",
     "quintile-definition evidence (README_fin.md)"),
    ("docs/tietotrendit_2022_lapsiperheiden_kulutusmenot_fi.html",
     "https://stat.fi/tietotrendit/artikkelit/2022/elaman-perusasiat-korostuvat-lapsiperheiden-kulutusmenoissa",
     "Statistics Finland Tieto&trendit article (2022, Finnish) on families' consumption; states that its income "
     "fifths have equal numbers of households", "quintile-definition evidence (README_fin.md)"),
]

# 2d. Eurostat: two datasets x five geos, 2015 onward, current prices, chain-linked volumes (reference year 2020,
#     the current one) and implicit deflators, each in euro and national currency.
EU_DATASETS = ["nama_10_co3_p3", "nama_10_cp18"]
EU_GEOS = ["FI", "SE", "DK", "DE", "EU27_2020"]
EU_UNITS = ["CP_MEUR", "CP_MNAC", "CLV20_MEUR", "CLV20_MNAC", "PD20_EUR", "PD20_NAC"]
EU_SINCE = "2015"
ES_DOCS = [
    ("docs/nama10_esms.htm", "https://ec.europa.eu/eurostat/cache/metadata/en/nama10_esms.htm",
     "Eurostat ESMS metadata for annual national accounts (nama10), linked from both datasets",
     "definitions (README_fin.md)"),
    ("docs/eurostat_toc_en.txt", "https://ec.europa.eu/eurostat/api/dissemination/catalogue/toc/txt?lang=en",
     "Eurostat catalogue table of contents (dataset codes, titles, last update, data start/end)",
     "provenance: nama_10_cp18 is the COICOP 2018 dataset; last-update dates"),
]


# ---------------------------------------------------------------------------------------------------------
# 3. Downloads (skipped when vendored)
# ---------------------------------------------------------------------------------------------------------
for db in tqdm(LISTINGS, desc="StatFin listings"):
    url = f"{PX}/StatFin/{db + '/' if db else ''}"
    get(SF, f"listing/StatFin_{db or 'root'}.json", url,
        f"StatFin database listing ({db or 'all databases'})", "provenance: which tables exist")
for q in tqdm(SEARCHES, desc="StatFin searches"):
    get(SF, f"search/StatFin_query_{q.replace(' ', '_')}.json", f"{PX}/StatFin/?query={quote(q)}",
        f"StatFin table search, query '{q}'", "provenance: search for land / property-tax data (README_fin.md)")
for db, tab, over, what, used in tqdm(PX_TABLES, desc="StatFin tables"):
    url = f"{PX}/StatFin/{db}/{tab}.px"
    mpath = get(SF, f"meta/{db}_{tab}.meta.json", url, f"Table metadata (variables and value lists): {what}", used)
    meta = json.loads(mpath.read_text(encoding="utf-8"))
    px_post(SF, f"data/{db}_{tab}.json", url, px_query(meta, over), f"Table data (JSON-stat2): {what}", used)
for rel, url, what, used in tqdm(SF_DOCS, desc="stat.fi pages"):
    get(SF, rel, url, what, used)
for ds in EU_DATASETS:
    for geo in tqdm(EU_GEOS, desc=f"Eurostat {ds}"):
        qs = urlencode([("format", "JSON"), ("lang", "EN"), ("geo", geo)] + [("unit", u) for u in EU_UNITS]
                       + [("sinceTimePeriod", EU_SINCE)])
        get(ES, f"data/{ds}_{geo}.json", f"{ESTAT}/{ds}?{qs}",
            f"Eurostat {ds} (JSON-stat 2.0), geo {geo}, units {', '.join(EU_UNITS)}, all COICOP codes, "
            f"{EU_SINCE} onward", "eurostat_coicop_long.csv" if ds == "nama_10_co3_p3" else
            "eurostat_coicop2018_long.csv")
for rel, url, what, used in ES_DOCS:
    get(ES, rel, url, what, used)
# Eurostat non-financial balance sheets for Finland: which land codes Finland reports (land search, item 4)
get(ES, "data/nama_10_nfa_bs_FI.json",
    f"{ESTAT}/nama_10_nfa_bs?" + urlencode([("format", "JSON"), ("lang", "EN"), ("geo", "FI"), ("unit", "CP_MEUR"),
                                             ("sinceTimePeriod", EU_SINCE)]),
    "Eurostat nama_10_nfa_bs (capital stocks by sector and detailed asset type, JSON-stat 2.0), geo FI, CP_MEUR, "
    f"all sectors and assets reported, {EU_SINCE} onward",
    "land search (README_fin.md): land detail Finland transmits; cross-check of StatFin 11zx N211")
print("downloads complete")


# ---------------------------------------------------------------------------------------------------------
# 4. Parsing helpers (JSON-stat 2.0 is what both StatFin PxWeb and the Eurostat API return)
# ---------------------------------------------------------------------------------------------------------
def jsonstat(path):
    """Read a JSON-stat 2.0 dataset into a long DataFrame: one column per dimension (codes), value, status."""
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    ids, sizes = d["id"], d["size"]
    cats = []
    for k in ids:
        idx = d["dimension"][k]["category"]["index"]
        cats.append(sorted(idx, key=idx.get) if isinstance(idx, dict) else list(idx))
    n = int(np.prod(sizes))
    vals = d["value"]
    v = np.full(n, np.nan)
    for i, x in (vals.items() if isinstance(vals, dict) else enumerate(vals)):
        if x is not None:
            v[int(i)] = x
    status = [""] * n
    st = d.get("status") or {}
    for i, x in (st.items() if isinstance(st, dict) else enumerate(st)):
        status[int(i)] = x or ""
    df = pd.DataFrame(list(itertools.product(*cats)), columns=ids)
    df["value"] = v
    df["status"] = status
    labels = {k: d["dimension"][k]["category"].get("label", {}) for k in ids}
    return df, d, labels


def sf(table):
    return jsonstat(RAW / SF / "data" / f"{table}.json")


def write_tidy(df, name):
    path = TIDY / name
    df.to_csv(path, index=False, lineterminator="\n", float_format="%.10g")
    print(f"wrote {name}: {len(df):,} rows")
    return path


CHECKS = []


def check(check_id, kind, table, description, value, reference, tol, note=""):
    """Record one verification number. kind: consistency (must pass), crosscheck (publisher headline), info."""
    diff = None if (value is None or reference is None) else float(value) - float(reference)
    passed = "" if (kind == "info" or diff is None) else bool(abs(diff) <= tol)
    CHECKS.append({"check_id": check_id, "kind": kind, "table": table, "description": description,
                   "value": value, "reference": reference, "diff": diff, "tolerance": tol if kind != "info" else None,
                   "passed": passed, "note": note})


DUR = re.compile(r"\s*\((ND|SD|D|S)\)\s*$", re.IGNORECASE)   # NA labels have one "(Nd)"


def clean_label(lab):
    """'01.1.1 Cereals and cereal products (ND)' -> ('Cereals and cereal products', 'ND')."""
    m = DUR.search(lab)
    dur = m.group(1).upper() if m else ""
    lab = DUR.sub("", lab)
    lab = re.sub(r"^\d+(\.\d+)*\s+", "", lab).strip()
    return lab, dur


QGROUP = {"SS": "total", "1": "q1", "2": "q2", "3": "q3", "4": "q4", "5": "q5"}
DGROUP = {"SS": "total", **{str(i): f"d{i:02d}" for i in range(1, 11)}}
FGROUP = {"SS": "total", "110": "d01", "1120": "d02", "2130": "d03", "3140": "d04", "4150": "d05", "5160": "d06",
          "6170": "d07", "7180": "d08", "8190": "d09", "91100": "d10"}


# ---------------------------------------------------------------------------------------------------------
# 5. fi_hbs2022_long.csv — HBS 2022, table 14pg, every COICOP code x total and quintiles
# ---------------------------------------------------------------------------------------------------------
hbs, hbs_d, hbs_lab = sf("ktutk_14pg")
HC, HQ, HM = "coicop_46_20231201", "tuloviidennes_2_20140501", "contentscode"
HBS_MEASURES = {   # 2022-price variants are identical to current prices in 2022 (checked below) and are left out
    "kulu_kt_hk_1_1": ("per_household_year", "EUR per household per year, current prices"),
    "kulu_kt_hk_2_1": ("per_cu_year", "EUR per consumption unit per year, current prices"),
    "kulukk_kt_hk_1_1": ("per_household_month", "EUR per household per month, current prices"),
    "kulukk_kt_hk_2_1": ("per_cu_month", "EUR per consumption unit per month, current prices"),
    "kulu_pro_kt_hk_1_1": ("share_household_pct", "percent of the group's total consumption expenditure "
                                                  "(per-household basis; code 0 = 100)"),
    "kulu_pro_kt_hk_2_1": ("share_cu_pct", "percent of the group's total consumption expenditure "
                                           "(per-consumption-unit basis; code 0 = 100)"),
}
HBS_OUTSIDE_TOTAL = {"99"}   # 'Items outside consumption expenditure' (DIMNOTE: total excludes them)
hbs_codes = list(hbs_lab[HC])


def hbs_parent(c):
    if c == "0" or c in HBS_OUTSIDE_TOTAL:
        return ""
    if len(c) == 2:          # divisions 01-13 and 77 'Total consumption abroad' add up to code 0 (checked)
        return "0"
    return c[:-1]


hbs_kids = {}
for c in hbs_codes:
    if hbs_parent(c):
        hbs_kids.setdefault(hbs_parent(c), []).append(c)
h22 = hbs[hbs.timeperiod_y == "2022"]
rows = []
for r in h22.itertuples(index=False):
    meas = getattr(r, HM)
    if meas not in HBS_MEASURES:
        continue
    c = getattr(r, HC)
    lab, dur = clean_label(hbs_lab[HC][c])
    rows.append({"coicop_code": c, "label": lab, "level": 0 if c == "0" else len(c) - 1, "parent_code": hbs_parent(c),
                 "group": QGROUP[getattr(r, HQ)], "measure": HBS_MEASURES[meas][0], "value": r.value,
                 "unit": HBS_MEASURES[meas][1], "status": r.status, "durability": dur,
                 "is_leaf": c not in hbs_kids, "in_total": c not in HBS_OUTSIDE_TOTAL, "measure_code": meas,
                 "label_published": hbs_lab[HC][c]})
fi_hbs = pd.DataFrame(rows)
# publisher's code order, then measure order as listed above, then total, q1..q5
fi_hbs["_c"] = fi_hbs.coicop_code.map({c: i for i, c in enumerate(hbs_codes)})
fi_hbs["_m"] = fi_hbs.measure.map({v[0]: i for i, v in enumerate(HBS_MEASURES.values())})
fi_hbs["_g"] = fi_hbs.group.map({g: i for i, g in enumerate(QGROUP.values())})
fi_hbs = fi_hbs.sort_values(["_c", "_m", "_g"]).drop(columns=["_c", "_m", "_g"]).reset_index(drop=True)
write_tidy(fi_hbs, "fi_hbs2022_long.csv")

# checks on the HBS
def tree_check(values, parent_of):
    """values: DataFrame indexed by code, one column per cut (group, geo-year, ...); parent_of: {code: parent}.
    Returns (max abs diff parent - sum of children over complete sets, n complete sets, n skipped sets).
    A set is skipped when the parent or any child has no value (suppressed or not published)."""
    kids = pd.Series(parent_of)
    kids = kids[kids != ""]
    kv = values.reindex(kids.index)
    ksum = kv.groupby(kids.values).sum()
    kmiss = kv.isna().groupby(kids.values).any()
    pv = values.reindex(ksum.index)
    diff = (pv - ksum).abs().where(~kmiss & pv.notna())
    n_ok = int(diff.notna().sum().sum())
    return (float(diff.max().max()) if n_ok else np.nan), n_ok, int(diff.size - n_ok)


hw = h22.pivot(index=[HC, HQ], columns=HM, values="value")   # keeps fully suppressed codes
for meas in ["kulu_kt_hk_1_1", "kulu_kt_hk_2_1", "kulukk_kt_hk_1_1", "kulukk_kt_hk_2_1"]:
    worst, n_ok, n_skip = tree_check(hw[meas].unstack(HQ), {c: hbs_parent(c) for c in hbs_codes})
    check(f"hbs_tree_{HBS_MEASURES[meas][0]}", "consistency", "ktutk 14pg",
          f"2022, {HBS_MEASURES[meas][0]}: every parent = sum of its children (code 0 = divisions 01-13 + 77; "
          f"04 includes 04.6 interest on housing loans); max abs diff over {n_ok} complete sets "
          f"({n_skip} sets skipped: a child suppressed)", worst, 0, 3, "whole-euro rounding")
for meas in ["kulu_pro_kt_hk_1_1", "kulu_pro_kt_hk_2_1"]:
    tot = hw.xs("0", level=HC)[meas]
    check(f"hbs_share_total_{HBS_MEASURES[meas][0]}", "consistency", "ktutk 14pg",
          f"2022 {HBS_MEASURES[meas][0]} of code 0, max abs deviation from 100", float((tot - 100).abs().max()), 0, 0)
    divs = hw.loc[[(c, q) for c in [f"{i:02d}" for i in range(1, 14)] + ["77"] for q in QGROUP], meas]
    s = divs.groupby(level=HQ).sum()
    check(f"hbs_share_divsum_{HBS_MEASURES[meas][0]}", "consistency", "ktutk 14pg",
          f"2022 {HBS_MEASURES[meas][0]}: divisions 01-13 + 77 sum to 100 (max abs deviation over groups)",
          float((s - 100).abs().max()), 0, 0.5, "one-decimal rounding of 14 shares")
dev = np.abs(hw[["kulukk_kt_hk_1_1", "kulukk_kt_hk_2_1"]].values * 12 - hw[["kulu_kt_hk_1_1", "kulu_kt_hk_2_1"]].values)
check("hbs_month_x12_vs_year", "consistency", "ktutk 14pg",
      "2022: |12 x monthly - yearly|, max over all codes, groups, per household and per consumption unit (EUR)",
      float(np.nanmax(dev)), 0, 6.5, "monthly figures are rounded to whole euros: 12 x 0.5 + 0.5")
same = True
for a, b in [("kulu_kt_hk_1_1", "kulu_kt_hk_1_2"), ("kulu_kt_hk_2_1", "kulu_kt_hk_2_2"),
             ("kulukk_kt_hk_1_1", "kulukk_kt_hk_1_2"), ("kulukk_kt_hk_2_1", "kulukk_kt_hk_2_2")]:
    same &= bool(((hw[a] == hw[b]) | (hw[a].isna() & hw[b].isna())).all())
check("hbs_2022prices_eq_current", "consistency", "ktutk 14pg",
      "2022: every 2022-prices cell equals the current-prices cell (1 = true)", int(same), 1, 0)
check("hbs_no_unflagged_missing", "consistency", "ktutk 14pg",
      "2022: cells with no value and no status symbol", int(((h22.value.isna()) & (h22.status == "")).sum()), 0, 0)
check("hbs_codes_with_empty_cu_cell", "info", "ktutk 14pg", "2022: COICOP codes with at least one empty per-CU-year "
      "cell (any group; suppressed, not asked, missing or not applicable)",
      int(h22[(h22[HM] == "kulu_kt_hk_2_1") & h22.value.isna()][HC].nunique()), None, None)

# HBS release cross-checks (docs/release_ktutk_2022_2024-04-11.html; preliminary release and documentation pages)
REL = "release 2024-04-11"
check("hbs_rel_food_share_q1", "crosscheck", "ktutk 14pg", "Q1 share of 01 food in consumption (per-household "
      "basis), release: '18 per cent'", hw.loc[("01", "1"), "kulu_pro_kt_hk_1_1"], 18, 0.5, REL)
check("hbs_rel_food_share_q5", "crosscheck", "ktutk 14pg", "Q5 share of 01 food, release: '12 per cent'",
      hw.loc[("01", "5"), "kulu_pro_kt_hk_1_1"], 12, 0.5, REL)
check("hbs_rel_housing_share_q1", "crosscheck", "ktutk 14pg", "Q1 share of 04 housing and energy, release: "
      "'39 per cent'", hw.loc[("04", "1"), "kulu_pro_kt_hk_1_1"], 39, 0.5, REL)
check("hbs_rel_food_housing_share_q1", "crosscheck", "ktutk 14pg", "Q1 share of 01 + 04, release: '56 per cent'",
      hw.loc[("01", "1"), "kulu_pro_kt_hk_1_1"] + hw.loc[("04", "1"), "kulu_pro_kt_hk_1_1"], 56, 0.5, REL)
check("hbs_rel_housing_eur_q1", "crosscheck", "ktutk 14pg", "Q1 04 housing and energy, EUR per consumption unit "
      "per month, release: 'approximately EUR 560'", hw.loc[("04", "1"), "kulukk_kt_hk_2_1"], 560, 5, REL)
check("hbs_rel_housing_eur_q5", "crosscheck", "ktutk 14pg", "Q5 04 housing and energy, EUR per consumption unit "
      "per month, release: 'approximately EUR 1,100'", hw.loc[("04", "5"), "kulukk_kt_hk_2_1"], 1100, 50, REL)
h16 = hbs[(hbs.timeperiod_y == "2016") & (hbs[HC] == "01") & (hbs[HQ] == "SS") & (hbs[HM] == "kulu_pro_kt_hk_1_1")]
check("hbs_rel_food_share_change", "crosscheck", "ktutk 14pg", "all households, share of 01 food 2022 minus 2016 "
      "(pp), release: 'grew ... by one percentage point'",
      hw.loc[("01", "SS"), "kulu_pro_kt_hk_1_1"] - h16.value.iloc[0], 1, 0.5, REL)
check("hbs_prelim_per_cu", "info", "ktutk 14pg", "all households, EUR per consumption unit per year, final table "
      "vs preliminary release 2023-12-28 ('EUR 27,800')", hw.loc[("0", "SS"), "kulu_kt_hk_2_1"], 27800, None,
      "preliminary vintage; the final figure is 2.0% higher")
check("hbs_prelim_per_hh", "info", "ktutk 14pg", "all households, EUR per household per year, final table vs "
      "preliminary release ('EUR 39,000')", hw.loc[("0", "SS"), "kulu_kt_hk_1_1"], 39000, None, "preliminary vintage")


# ---------------------------------------------------------------------------------------------------------
# 6. fi_hh_composition.csv — households, persons, consumption units, ages, by income group, from every table
#    that has them (HBS quintiles, sample and register income deciles/quintiles, wealth-survey deciles)
# ---------------------------------------------------------------------------------------------------------
comp = []


def add(source_table, year, grouping, group, subgroup, measure, value, unit, derived=False, measure_label="",
        subgroup_label="", note="", low=None, high=None):
    comp.append({"source_table": source_table, "year": year, "grouping": grouping, "group": group,
                 "subgroup": subgroup, "measure": measure, "value": value, "unit": unit, "derived": derived,
                 "bound_low": low, "bound_high": high, "measure_label": measure_label,
                 "subgroup_label": subgroup_label, "note": note})


# 6a. HBS 2022 quintiles (ktutk 14qa): published means, plus counts and an age split derived from them
qa, _, qa_lab = sf("ktutk_14qa")
QA_MEAS = {"oklkm_sum": ("households_in_sample", "households (unweighted sample count)"),
           "pklkm_sum": ("households", "households (population estimate)"),
           "jlkm_mean": ("avg_household_size", "persons per household (mean)"),
           "oecdmod_mean": ("avg_consumption_units", "OECD-modified consumption units per household (mean)"),
           "Kaytetmk_1_mean": ("disposable_income_per_household", "EUR per household per year, nominal")}
q22 = qa[qa.timeperiod_y == "2022"]
for r in q22.itertuples(index=False):
    if r.contentscode in QA_MEAS:
        m, u = QA_MEAS[r.contentscode]
        add("ktutk 14qa", 2022, "hbs_household_quintile", QGROUP[getattr(r, HQ)], "all", m, r.value, u,
            measure_label=qa_lab["contentscode"][r.contentscode])
qw = q22.pivot(index=HQ, columns="contentscode", values="value")
check("hbs_14qa_income_2022eur_eq_nominal", "consistency", "ktutk 14qa", "2022: disposable income in 2022 euros "
      "equals nominal (max abs diff)", float((qw.Kaytetmk_1_mean - qw.Kaytetmk_2_mean).abs().max()), 0, 0)
check("hbs_14qa_households_sum", "consistency", "ktutk 14qa", "2022: quintile households sum to the total",
      float(qw.loc[["1", "2", "3", "4", "5"], "pklkm_sum"].sum()), float(qw.loc["SS", "pklkm_sum"]), 5)
check("hbs_household_quintiles", "consistency", "ktutk 14qa", "2022: each income quintile holds 20% of households "
      "(max abs deviation, pp)", float((qw.loc[["1", "2", "3", "4", "5"], "pklkm_sum"] / qw.loc["SS", "pklkm_sum"] * 100
                                        - 20).abs().max()), 0, 0.1,
      "the HBS quintiles are quintiles of households, unlike the person quintiles and deciles of tjt")
check("hbs_households_vs_documentation", "crosscheck", "ktutk 14qa", "2022 households in population vs "
      "documentation 'In 2022, there were 2.919 million households'", float(qw.loc["SS", "pklkm_sum"]), 2919000, 500)
# Age split from the OECD-modified scale (documented weights: first person 1, others aged 14+ 0.5, under 14 0.3):
# mean CU = 1 + 0.5 (a - 1) + 0.3 c and mean size n = a + c give a = (CU - 0.5 - 0.3 n) / 0.2, c = n - a.
# Exact in means; the bounds carry the publisher's 2-decimal rounding of n and CU (+-0.005 each).
DA = (0.005 + 0.3 * 0.005) / 0.2
for q, g in QGROUP.items():
    hh, n, cu = qw.loc[q, "pklkm_sum"], qw.loc[q, "jlkm_mean"], qw.loc[q, "oecdmod_mean"]
    a, c = (cu - 0.5 - 0.3 * n) / 0.2, n - (cu - 0.5 - 0.3 * n) / 0.2
    note = "derived from 14qa means via the OECD-modified scale; bounds = publisher rounding of the means"
    add("ktutk 14qa", 2022, "hbs_household_quintile", g, "all", "persons", hh * n, "persons", True,
        note="households x mean household size", low=hh * (n - 0.005), high=hh * (n + 0.005))
    add("ktutk 14qa", 2022, "hbs_household_quintile", g, "all", "consumption_units", hh * cu,
        "OECD-modified consumption units", True, note="households x mean consumption units",
        low=hh * (cu - 0.005), high=hh * (cu + 0.005))
    add("ktutk 14qa", 2022, "hbs_household_quintile", g, "all", "avg_persons_14plus", a,
        "persons aged 14+ per household (mean)", True, note=note, low=a - DA, high=a + DA)
    add("ktutk 14qa", 2022, "hbs_household_quintile", g, "all", "avg_children_under14", c,
        "persons aged 0-13 per household (mean)", True, note=note, low=c - 0.005 - DA, high=c + 0.005 + DA)
    add("ktutk 14qa", 2022, "hbs_household_quintile", g, "all", "persons_14plus", hh * a, "persons aged 14+", True,
        note=note, low=hh * (a - DA), high=hh * (a + DA))
    add("ktutk 14qa", 2022, "hbs_household_quintile", g, "all", "children_under14", hh * c, "persons aged 0-13",
        True, note=note, low=hh * (c - 0.005 - DA), high=hh * (c + 0.005 + DA))
hb = hw.xs("0", level=HC)
for q in QGROUP:
    check(f"hbs_hh_over_cu_vs_14qa_{QGROUP[q]}", "info", "ktutk 14pg/14qa",
          f"{QGROUP[q]}: per-household / per-consumption-unit total consumption vs 14qa mean consumption units per "
          f"household", float(hb.loc[q, "kulu_kt_hk_1_1"] / hb.loc[q, "kulu_kt_hk_2_1"]),
          float(qw.loc[q, "oecdmod_mean"]), None, "not equal: per-CU figures are not per-household figures divided "
          "by the mean CU (method not documented)")

TJT_YEARS = ["2022", "2023", "2024"]
# 6b. income distribution statistics, sample data: deciles of persons by stage in life (tjt 12ew)
ew, _, ew_lab = sf("tjt_12ew")
EW_MEAS = {"ykor_sumwgt": ("households", "households"), "ykorpop_sumwgt": ("persons", "persons"),
           "desiprosentti": ("share_of_decile_households_pct", "percent of the decile's households"),
           "ryhmaprosentti": ("share_of_stage_households_pct", "percent of the stage's households")}
ES_ = "elinvaihe_5_20200201"
for r in ew[ew.timeperiod_y.isin(TJT_YEARS)].itertuples(index=False):
    st = getattr(r, ES_)
    m, u = EW_MEAS[r.contentscode]
    add("tjt 12ew", int(r.timeperiod_y), "tjt_sample_person_decile", DGROUP[getattr(r, "desiilit_2_20120101")],
        "all" if st == "SS" else f"stage_{st}", m, r.value, u, measure_label=ew_lab["contentscode"][r.contentscode],
        subgroup_label=ew_lab[ES_][st])
for y in TJT_YEARS:
    e = ew[ew.timeperiod_y == y]
    h = e[e.contentscode == "ykor_sumwgt"].pivot(index=ES_, columns="desiilit_2_20120101", values="value")
    p = e[e.contentscode == "ykorpop_sumwgt"].pivot(index=ES_, columns="desiilit_2_20120101", values="value")
    dcols = [str(i) for i in range(1, 11)]
    check(f"tjt12ew_decile_sum_{y}", "consistency", "tjt 12ew", f"{y}: deciles sum to total (households and persons,"
          f" every stage; max abs diff)", float(max((h[dcols].sum(axis=1) - h["SS"]).abs().max(),
                                                  (p[dcols].sum(axis=1) - p["SS"]).abs().max())), 0, 3)
    check(f"tjt12ew_stage_sum_{y}", "consistency", "tjt 12ew", f"{y}: stages 1-4 sum to all households (max abs "
          f"diff)", float((h.loc[["1", "2", "3", "4"]].sum() - h.loc["SS"]).abs().max()), 0, 3)
    sh = p.loc["SS", dcols] / p.loc["SS", "SS"] * 100
    check(f"tjt12ew_person_deciles_{y}", "consistency", "tjt 12ew", f"{y}: each decile holds 10% of persons (max abs "
          f"deviation, pp)", float((sh - 10).abs().max()), 0, 0.1, "deciles are formed among persons")
    pub = e[e.contentscode == "desiprosentti"].pivot(index=ES_, columns="desiilit_2_20120101", values="value")
    check(f"tjt12ew_pct_meaning_{y}", "consistency", "tjt 12ew", f"{y}: 'desiprosentti' = 100 x stage households / "
          f"decile households (max abs diff, pp)", float((pub - h / h.loc["SS"] * 100).abs().max().max()), 0, 0.06)
    pub = e[e.contentscode == "ryhmaprosentti"].pivot(index=ES_, columns="desiilit_2_20120101", values="value")
    check(f"tjt12ew_grouppct_meaning_{y}", "consistency", "tjt 12ew", f"{y}: 'ryhmaprosentti' = 100 x decile "
          f"households / stage households (max abs diff, pp)",
          float((pub - h.div(h["SS"], axis=0) * 100).abs().max().max()), 0, 0.06)
    pph = p / h
    check(f"tjt12ew_one_person_{y}", "consistency", "tjt 12ew", f"{y}: persons per household in stages 1, 1.1-1.3 "
          f"(one-person households), max abs deviation from 1, every decile",
          float((pph.loc[["1", "10", "11", "12"]] - 1).abs().max().max()), 0, 0.001)
    check(f"tjt12ew_couples_{y}", "consistency", "tjt 12ew", f"{y}: persons per household in stages 2, 2.1-2.3 "
          f"(childless couples), max abs deviation from 2, every decile",
          float((pph.loc[["2", "21", "22", "23"]] - 2).abs().max().max()), 0, 0.001)
    for st in ["31", "32", "4"]:
        check(f"tjt12ew_pph_stage{st}_{y}", "info", "tjt 12ew", f"{y}: persons per household, stage {st} "
              f"({ew_lab[ES_][st]}), all deciles", float(pph.loc[st, "SS"]), None, None)
check("tjt12ew_households_vs_hbs_2022", "crosscheck", "tjt 12ew / ktutk 14qa", "2022 households: income "
      "distribution sample vs HBS", float(ew[(ew.timeperiod_y == "2022") & (ew[ES_] == "SS") &
                                              (ew.desiilit_2_20120101 == "SS") &
                                              (ew.contentscode == "ykor_sumwgt")].value.iloc[0]),
      float(qw.loc["SS", "pklkm_sum"]), 500)

# 6c. sample data: quintiles of persons (tjt 152w), composition and income columns only
w52, _, w52_lab = sf("tjt_152w")
W52_MEAS = {"tjt-kotital": ("households", "households"), "phenkiloita": ("persons", "persons"),
            "kokonum_mean": ("avg_household_size", "persons per household (mean, published to 1 decimal)"),
            "halpinta": ("floor_area_per_household", "m2 per household (mean)"),
            "kvkturahamodm": ("disp_money_income_per_cu_mean", "EUR per consumption unit per year, mean, prices of the "
                              "latest statistical year"),
            "kvkturahamod": ("disp_money_income_per_cu_median", "EUR per consumption unit per year, median, prices of "
                             "the latest statistical year")}
for r in w52[w52.timeperiod_y.isin(TJT_YEARS) & w52.contentscode.isin(list(W52_MEAS))].itertuples(index=False):
    m, u = W52_MEAS[r.contentscode]
    add("tjt 152w", int(r.timeperiod_y), "tjt_sample_person_quintile", QGROUP[getattr(r, HQ)], "all", m, r.value, u,
        measure_label=w52_lab["contentscode"][r.contentscode])
for y in TJT_YEARS:
    e = w52[(w52.timeperiod_y == y) & (w52.contentscode == "phenkiloita")].set_index(HQ).value
    check(f"tjt152w_person_quintiles_{y}", "consistency", "tjt 152w", f"{y}: each quintile holds 20% of persons (max "
          f"abs deviation, pp)", float((e[["1", "2", "3", "4", "5"]] / e["SS"] * 100 - 20).abs().max()), 0, 0.1)

# 6d. register-based total data: deciles of persons, household-dwelling units (tjt 128c) and ages (tjt 14ya)
c8, _, c8_lab = sf("tjt_128c")
C8_MEAS = {"asuntok": ("household_dwelling_units", "household-dwelling units"),
           "tjt-henkiloita": ("persons", "persons (dwelling population)"),
           "kokonum_mean": ("avg_household_size", "persons per household-dwelling unit (mean)"),
           "modoecd_mean": ("avg_consumption_units", "OECD-modified consumption units per household-dwelling unit "
                            "(mean)"),
           "tjt-ekvikturaha_mean": ("disp_money_income_per_cu_mean", "EUR per consumption unit per year, mean, value "
                                    "of the latest statistical year"),
           "tjt-ekvikturaha_med": ("disp_money_income_per_cu_median", "EUR per consumption unit per year, median, "
                                   "value of the latest statistical year"),
           "kturaha": ("disp_money_income_per_unit_mean", "EUR per household-dwelling unit per year, mean, value of "
                       "the latest statistical year")}
for r in c8[c8.timeperiod_y.isin(TJT_YEARS) & c8.contentscode.isin(list(C8_MEAS))].itertuples(index=False):
    m, u = C8_MEAS[r.contentscode]
    add("tjt 128c", int(r.timeperiod_y), "tjt_register_person_decile", DGROUP[getattr(r, "desiilit_2_20120101")],
        "all", m, r.value, u, measure_label=c8_lab["contentscode"][r.contentscode])
ya, _, ya_lab = sf("tjt_14ya")
AGE = {"SSS": "all", "0-17": "age_0_17", "18-64": "age_18_64", "65-": "age_65plus"}
yap = ya[ya.timeperiod_y.isin(TJT_YEARS) & (ya.syntypera_101_20180101 == "SSS") & (ya.contentscode == "tjt-henkiloita")]
for r in yap.itertuples(index=False):
    a = getattr(r, "ikaryhma_22_20191201")
    add("tjt 14ya", int(r.timeperiod_y), "tjt_register_person_decile", FGROUP[getattr(r, "fraktiili_3_20221219")],
        AGE[a], "persons", r.value, "persons (dwelling population)",
        measure_label=ya_lab["contentscode"]["tjt-henkiloita"], subgroup_label=ya_lab["ikaryhma_22_20191201"][a])
for (y, f), g in yap.groupby(["timeperiod_y", "fraktiili_3_20221219"]):
    s = g.set_index("ikaryhma_22_20191201").value
    add("tjt 14ya", int(y), "tjt_register_person_decile", FGROUP[f], "age_18plus", "persons",
        s["18-64"] + s["65-"], "persons (dwelling population)", True, subgroup_label="18 and over",
        note="sum of the published 18-64 and 65- counts")
for y in TJT_YEARS:
    g = yap[yap.timeperiod_y == y].pivot(index="ikaryhma_22_20191201", columns="fraktiili_3_20221219", values="value")
    check(f"tjt14ya_age_sum_{y}", "consistency", "tjt 14ya", f"{y}: age groups sum to all persons, every decile (max "
          f"abs diff)", float((g.loc[["0-17", "18-64", "65-"]].sum() - g.loc["SSS"]).abs().max()), 0, 3)
    dec = [k for k in FGROUP if k != "SS"]
    check(f"tjt14ya_decile_sum_{y}", "consistency", "tjt 14ya", f"{y}: deciles sum to total persons",
          float(g.loc["SSS", dec].sum()), float(g.loc["SSS", "SS"]), 5)
    p8 = c8[(c8.timeperiod_y == y) & (c8.contentscode == "tjt-henkiloita")].set_index("desiilit_2_20120101").value
    check(f"tjt128c_vs_14ya_persons_{y}", "consistency", "tjt 128c / 14ya", f"{y}: register persons per decile equal "
          f"in 128c and 14ya (max abs diff)", float(max(abs(p8[k] - g.loc["SSS", fk]) for k, fk in
                                                        zip([str(i) for i in range(1, 11)], dec))), 0, 0)

# 6e. wealth survey 2023 (vtutk 151u): households per income decile
wu, _, wu_lab = sf("vtutk_151u")
WA, WD = "vtutk_varlaji_6_20200101", "desiilit_2_20120101"
w23 = wu[wu.timeperiod_y == "2023"]
for code, (m, u) in {"vtutk_kotitalouksia_perusjoukko": ("households", "households"),
                     "vtutk_kotitalouksia_keskikoko": ("avg_household_size", "persons per household (mean)"),
                     "vtutk_kotitalouksia_otoskoko": ("households_in_sample", "households (sample count)")}.items():
    s = w23[w23.contentscode == code]
    check(f"vtutk151u_same_across_items_{m}", "consistency", "vtutk 151u", f"2023 {m}: identical for every asset type "
          f"(number of distinct values per decile, max)", int(s.groupby(WD).value.nunique().max()), 1, 0)
    for r in s[s[WA] == "nettoae_DN3001"].itertuples(index=False):
        add("vtutk 151u", 2023, "vtutk_household_decile", DGROUP[getattr(r, WD)], "all", m, r.value, u,
            measure_label=wu_lab["contentscode"][code])
hh23 = w23[(w23.contentscode == "vtutk_kotitalouksia_perusjoukko") & (w23[WA] == "nettoae_DN3001")].set_index(WD).value
check("vtutk151u_household_deciles", "consistency", "vtutk 151u", "2023: each income decile holds 10% of households "
      "(max abs deviation, pp)", float((hh23[[str(i) for i in range(1, 11)]] / hh23["SS"] * 100 - 10).abs().max()), 0,
      0.1, "the wealth-survey deciles are deciles of households, unlike the person deciles of tjt")
fi_comp = pd.DataFrame(comp)
write_tidy(fi_comp, "fi_hh_composition.csv")


# ---------------------------------------------------------------------------------------------------------
# 7. fi_wealth_2023_deciles.csv and fi_wealth_2023_tenure.csv — wealth survey 2023 (vtutk 151u, 151z)
# ---------------------------------------------------------------------------------------------------------
WEALTH_ITEMS = {
    "nettoae_DN3001": "net_wealth", "nettoae_DN3001_2": "net_wealth_excl_insurance_crypto",
    "nettoae_suppea": "net_wealth_narrow", "bruttoae_DA1000": "total_assets",
    "bruttoae_DA1000_2": "total_assets_excl_insurance_crypto", "bruttoae_suppea": "total_assets_narrow",
    "realvar2": "real_wealth", "realvar": "real_wealth_narrow", "finan": "financial_assets",
    "finan2": "financial_assets_excl_insurance_crypto", "kturaha": "disposable_income",
    "asvara": "housing_wealth", "asarav": "main_residence", "vaarvy": "free_time_residences",
    "asaram": "other_residential_property", "kulku": "vehicles", "muurealvar": "forest_farmland_business",
    "talle": "deposits", "pymar": "listed_shares_and_mutual_funds", "sirave": "mutual_funds",
    "porsosa": "listed_shares", "muosa": "unlisted_shares", "elavak": "private_pension_wealth",
    "vaksak": "savings_investment_insurance", "muufinan": "other_financial_assets", "luototy": "debt_total",
    "asuntm": "housing_loans", "muutvelat": "consumer_and_other_loans", "asarav_netto": "main_residence_net_value"}
WEALTH_MEAS = {
    "vtutk_keskiarvo_n": ("mean", "EUR per household, mean over all households in the group"),
    "vtutk_mediaani_n": ("median", "EUR per household holding the item (median conditional on holding)"),
    "vtutk_alakvartiili_n": ("p25", "EUR per household holding the item (lower quartile conditional on holding)"),
    "vtutk_ylakvartiili_n": ("p75", "EUR per household holding the item (upper quartile conditional on holding)"),
    "vtutk_kotitalousomistajia": ("households_holding", "households holding the item"),
    "vtutk_kotitalousosuus": ("participation_rate_pct", "percent of the group's households holding the item")}
TENURE = {"SS": "all", "1": "outright_owner", "2": "owner_with_mortgage", "3": "renter_or_other"}


def wealth_long(df, lab, gvar, gmap, gname):
    out = []
    for r in df[df.contentscode.isin(list(WEALTH_MEAS))].itertuples(index=False):
        item = getattr(r, WA)
        lab_item = lab[WA][item]
        m = re.match(r"^(\d+(?:\.\d+)?)\.?\s", lab_item)
        out.append({"component": WEALTH_ITEMS[item], gname: gmap[getattr(r, gvar)],
                    "measure": WEALTH_MEAS[r.contentscode][0], "value": r.value,
                    "unit": WEALTH_MEAS[r.contentscode][1], "status": r.status, "component_code": item,
                    "item_no": m.group(1) if m else "", "component_label": lab_item})
    out = pd.DataFrame(out)
    out["_c"] = out.component_code.map({c: i for i, c in enumerate(lab[WA])})
    out["_g"] = out[gname].map({g: i for i, g in enumerate(gmap.values())})
    out["_m"] = out.measure.map({v[0]: i for i, v in enumerate(WEALTH_MEAS.values())})
    return out.sort_values(["_c", "_m", "_g"]).drop(columns=["_c", "_g", "_m"]).reset_index(drop=True)


write_tidy(wealth_long(w23, wu_lab, WD, DGROUP, "decile"), "fi_wealth_2023_deciles.csv")
wz, _, wz_lab = sf("vtutk_151z")
write_tidy(wealth_long(wz[wz.timeperiod_y == "2023"], wz_lab, "hallintaperuste_1_20150401", TENURE, "tenure"),
           "fi_wealth_2023_tenure.csv")

# checks: identities on the means (means are over all households, so they add), real = nominal in 2023,
# release headlines (docs/release_vtutk_2023_2025-03-12.html)
IDENT = [("asvara", ["asarav", "vaarvy", "asaram"], []), ("realvar2", ["asvara", "kulku", "muurealvar"], []),
         ("realvar", ["asvara", "kulku"], []), ("finan", ["talle", "pymar", "muosa", "elavak", "vaksak", "muufinan"], []),
         ("pymar", ["sirave", "porsosa"], []), ("luototy", ["asuntm", "muutvelat"], []),
         ("bruttoae_DA1000", ["realvar2", "finan"], []), ("nettoae_DN3001", ["bruttoae_DA1000"], ["luototy"]),
         ("asarav_netto", ["asarav"], ["asuntm"]), ("bruttoae_suppea", ["realvar", "finan2"], []),
         ("nettoae_suppea", ["bruttoae_suppea"], ["luototy"]), ("nettoae_DN3001_2", ["bruttoae_DA1000_2"], ["luototy"])]
for tab, frame, gvar in [("vtutk 151u", w23, WD), ("vtutk 151z", wz[wz.timeperiod_y == "2023"],
                                                     "hallintaperuste_1_20150401")]:
    mm = frame[frame.contentscode == "vtutk_keskiarvo_n"].pivot(index=WA, columns=gvar, values="value")
    for lhs, plus, minus in IDENT:
        diff = (mm.loc[lhs] - mm.loc[plus].sum() + (mm.loc[minus].sum() if minus else 0)).abs().max()
        check(f"wealth_{tab[-4:]}_{WEALTH_ITEMS[lhs]}", "consistency", tab, f"2023 means: {WEALTH_ITEMS[lhs]} = "
              f"{' + '.join(WEALTH_ITEMS[x] for x in plus)}{''.join(' - ' + WEALTH_ITEMS[x] for x in minus)} "
              f"(max abs diff over groups, EUR)", float(diff), 0, 3, "whole-euro rounding")
    nom = frame[frame.contentscode.str.endswith("_n")].sort_values([WA, gvar, "contentscode"]).value.values
    real = frame[frame.contentscode.str.endswith("_r")].sort_values([WA, gvar, "contentscode"]).value.values
    check(f"wealth_{tab[-4:]}_real_eq_nominal", "consistency", tab, "2023: real-terms values equal nominal values "
          "(cells that differ)", int(np.sum(~((nom == real) | (np.isnan(nom) & np.isnan(real))))), 0, 0)
mm = w23[w23.contentscode == "vtutk_keskiarvo_n"].pivot(index=WA, columns=WD, values="value")
REL = "release 2025-03-12"
check("wealth_rel_mean_net", "crosscheck", "vtutk 151u", "all households, mean net wealth, release: 'EUR 228,700'",
      mm.loc["nettoae_DN3001", "SS"], 228700, 50, REL)
check("wealth_rel_median_net", "crosscheck", "vtutk 151u", "all households, median net wealth, release: "
      "'EUR 96,000'", w23[(w23.contentscode == "vtutk_mediaani_n") & (w23[WA] == "nettoae_DN3001") &
                         (w23[WD] == "SS")].value.iloc[0], 96000, 50, REL)
check("wealth_rel_main_residence_share", "crosscheck", "vtutk 151u", "main residence as % of total assets, release: "
      "'45 per cent'", 100 * mm.loc["asarav", "SS"] / mm.loc["bruttoae_DA1000", "SS"], 45, 0.5, REL)
check("wealth_crypto_implied_total", "info", "vtutk 151u", "2023 all households: financial_assets - "
      "financial_assets_excl_insurance_crypto - savings_investment_insurance (implied crypto-assets, EUR mean)",
      float(mm.loc["finan", "SS"] - mm.loc["finan2", "SS"] - mm.loc["vaksak", "SS"]), None, None,
      "crypto-assets have no line of their own")


# ---------------------------------------------------------------------------------------------------------
# 8. eurostat_coicop_long.csv (nama_10_co3_p3, COICOP 1999) and eurostat_coicop2018_long.csv (nama_10_cp18)
# ---------------------------------------------------------------------------------------------------------
def eu_parent(c, ds):
    if c == "TOTAL":
        return ""
    if ds == "nama_10_co3_p3" and c in ("CP122", "CP127"):
        return "CP122_127"        # 'Prostitution; other services n.e.c.' = CP122 + CP127 (checked)
    if c == "CP122_127":
        return "CP12"
    return "TOTAL" if len(c) == 4 else c[:4]


def eu_level(c, ds):
    p = eu_parent(c, ds)
    return 0 if not p else 1 + eu_level(p, ds)


eu = {}
for ds, cc, name in [("nama_10_co3_p3", "coicop", "eurostat_coicop_long.csv"),
                     ("nama_10_cp18", "coicop18", "eurostat_coicop2018_long.csv")]:
    frames = []
    for geo in EU_GEOS:
        e, d, lab = jsonstat(RAW / ES / "data" / f"{ds}_{geo}.json")
        e = e[e.value.notna() | (e.status != "")].copy()
        e["label"] = e[cc].map(lab[cc])
        e["unit_label"] = e.unit.map(lab["unit"])
        e["code_order"] = e[cc].map({c: i for i, c in enumerate(lab[cc])})
        frames.append(e)
    e = pd.concat(frames, ignore_index=True)
    e["level"] = e[cc].map(lambda c: eu_level(c, ds))
    e["parent_coicop"] = e[cc].map(lambda c: eu_parent(c, ds))
    e["_u"] = e.unit.map({u: i for i, u in enumerate(EU_UNITS)})
    e["_g"] = e.geo.map({g: i for i, g in enumerate(EU_GEOS)})
    e = e.sort_values(["_g", "code_order", "_u", "time"])
    out = pd.DataFrame({"geo": e.geo.values, "coicop": e[cc].values, "label": e.label.values, "unit": e.unit.values,
                        "year": e.time.astype(int).values, "value": e.value.values, "flag": e.status.values,
                        "level": e.level.values, "parent_coicop": e.parent_coicop.values,
                        "unit_label": e.unit_label.values})
    write_tidy(out, name)
    eu[ds] = out

# checks: additivity of current-price values, deflator identity, latest years, Finland vs Statistics Finland
for ds, out in eu.items():
    codes = list(dict.fromkeys(out.coicop))
    for unit in ["CP_MEUR", "CP_MNAC"]:
        v = out[out.unit == unit].pivot(index="coicop", columns=["geo", "year"], values="value")
        worst, n_ok, n_skip = tree_check(v, {c: eu_parent(c, ds) for c in codes})
        check(f"eu_tree_{ds}_{unit}", "consistency", ds, f"{unit}: every parent = sum of its children, all geos and "
              f"years; max abs diff over {n_ok} complete sets ({n_skip} skipped: a child not published)", worst, 0, 0.5,
              "values published to 1 decimal")
    for cur, cp, clv, pd_ in [("EUR", "CP_MEUR", "CLV20_MEUR", "PD20_EUR"), ("NAC", "CP_MNAC", "CLV20_MNAC", "PD20_NAC")]:
        w = out[out.unit.isin([cp, clv, pd_])].pivot_table(index=["geo", "coicop", "year"], columns="unit",
                                                           values="value")
        w = w.dropna()
        w = w[w[clv] >= 1000]   # tiny aggregates make the rounded ratio noisy
        dev = (100 * w[cp] / w[clv] - w[pd_]).abs()
        check(f"eu_deflator_{ds}_{cur}", "consistency", ds, f"{pd_} = 100 x {cp} / {clv} (max abs diff, index "
              f"points, cells with volume >= 1000 million)", float(dev.max()), 0, 0.1)
    for geo in EU_GEOS:
        o = out[(out.geo == geo) & (out.unit == "CP_MEUR") & (out.coicop == "TOTAL") & out.value.notna()]
        check(f"eu_latest_{ds}_{geo}", "info", ds, f"{geo}: latest year with CP_MEUR TOTAL", int(o.year.max()), None,
              None)
na, na_d, na_lab = sf("ntp_15ag")
NC, NT = "coicop_45_20231201", "taloustoimi_1_20180101"
nat = na[(na.contentscode == "ntp-cp") & (na[NC] == "SSS")].pivot(index="timeperiod_y", columns=NT, values="value")
for ds in eu:
    o = eu[ds]
    o = o[(o.geo == "FI") & (o.unit == "CP_MEUR") & (o.coicop == "TOTAL")].set_index("year").value
    for y, v in o.items():
        check(f"eu_fi_total_vs_statfin_{ds}_{y}", "crosscheck", f"{ds} / ntp 15ag", f"FI {y} TOTAL CP_MEUR vs "
              f"Statistics Finland 15ag P31DCK (domestic concept), current prices", v, nat.loc[str(y), "P31DCK"], 0.5,
              "15ag vintage 2026-09-18")


# ---------------------------------------------------------------------------------------------------------
# 9. fi_na_hfce_coicop2018_long.csv — Finnish national accounts household consumption, COICOP 2018 (ntp 15ag)
# ---------------------------------------------------------------------------------------------------------
NA_MEAS = {"ntp-cp": ("current_prices", "EUR million, current prices"),
           "ntp-fp": ("previous_year_prices", "EUR million, at previous year's prices"),
           "ntp-vv_hinta_uusin_kul": ("volume_ref2025", "EUR million, chain-linked volume, reference year 2025 "
                                                        "(not additive)")}
na_codes = list(na_lab[NC])
na_set = {("0" if c == "SSS" else c) for c in na_codes}


def na_parent(c):
    if c == "0":
        return ""
    if len(c) == 2:
        return "0"
    assert c[:-1] in na_set, c
    return c[:-1]


nrows = na[na.value.notna() | ~na.status.isin(["", "."])].copy()
nrows["code"] = nrows[NC].map(lambda c: "0" if c == "SSS" else c)
lab_clean = {c: clean_label(na_lab[NC][c]) for c in na_codes}
fi_na = pd.DataFrame({
    "transaction": nrows[NT].values, "coicop_code": nrows.code.values,
    "label": [lab_clean[c][0] for c in nrows[NC]], "level": [0 if c == "0" else len(c) - 1 for c in nrows.code],
    "parent_code": [na_parent(c) for c in nrows.code], "year": nrows.timeperiod_y.astype(int).values,
    "measure": nrows.contentscode.map(lambda m: NA_MEAS[m][0]).values, "value": nrows.value.values,
    "unit": nrows.contentscode.map(lambda m: NA_MEAS[m][1]).values, "status": nrows.status.values,
    "preliminary": nrows.timeperiod_y.isin(["2024", "2025"]).values,
    "durability": [lab_clean[c][1] for c in nrows[NC]], "transaction_label": nrows[NT].map(na_lab[NT]).values,
    "label_published": nrows[NC].map(na_lab[NC]).values})
write_tidy(fi_na, "fi_na_hfce_coicop2018_long.csv")
cpw = fi_na[(fi_na.transaction == "P31DCK") & (fi_na.measure == "current_prices")]
worst, n_ok, n_skip = tree_check(cpw.pivot(index="coicop_code", columns="year", values="value"),
                                 {c: na_parent(c) for c in na_set})
check("na15ag_tree", "consistency", "ntp 15ag", f"P31DCK current prices: every parent = sum of its children, 2015-2025;"
      f" max abs diff over {n_ok} complete sets ({n_skip} skipped)", worst, 0, 3, "whole-million rounding")
check("na15ag_national_vs_domestic", "consistency", "ntp 15ag", "P31NCK = P31DCK + P33K - P34K, current prices "
      "(max abs diff over 2015-2025)", float((nat.P31NCK - nat.P31DCK - nat.P33K + nat.P34K).abs().max()), 0, 2)
hbs_agg = hw.loc[("0", "SS"), "kulu_kt_hk_1_1"] * qw.loc["SS", "pklkm_sum"] / 1e6
check("hbs_vs_na_2022", "info", "ktutk 14pg/14qa / ntp 15ag", "2022 HBS aggregate (EUR per household x households, "
      "EUR million) vs national accounts P31DCK", float(hbs_agg), float(nat.loc["2022", "P31DCK"]), None,
      f"HBS/NA = {hbs_agg / nat.loc['2022', 'P31DCK']:.3f}; concepts differ (HBS includes interest on housing loans "
      f"and excludes the institutional population; NA includes FISIM, non-profit services sold to households etc.)")


# ---------------------------------------------------------------------------------------------------------
# 10. fi_nonfin_assets_long.csv (rtp 11zx) and fi_land_indicators_long.csv (kihi 11jc, ashi 12de, 13mw)
# ---------------------------------------------------------------------------------------------------------
z, _, z_lab = sf("rtp_11zx")
ZS, ZI = "sektoriluokitus_7_20230101", "varojenluokitus_5_20180101"
fi_z = pd.DataFrame({"sector": z[ZS].values, "instrument": z[ZI].values, "year": z.timeperiod_y.astype(int).values,
                     "measure": z.contentscode.map({"KK": "stock", "VK": "change"}).values, "value": z.value.values,
                     "unit": z.contentscode.map({"KK": "EUR million, end-of-year stock, current prices",
                                                 "VK": "EUR million, change in the stock during the year"}).values,
                     "sector_label": z[ZS].map(z_lab[ZS]).values, "instrument_label": z[ZI].map(z_lab[ZI]).values})
write_tidy(fi_z, "fi_nonfin_assets_long.csv")
zk = z[z.contentscode == "KK"]
pv = zk.pivot_table(index=[ZI, "timeperiod_y"], columns=ZS, values="value")
check("rtp11zx_sector_sum", "consistency", "rtp 11zx", "stocks: S11+S12+S1311+S1313+S1314+S14+S15 = S0 (max abs diff)",
      float((pv[["S11", "S12", "S1311", "S1313", "S1314", "S14", "S15"]].sum(axis=1) - pv["S0"]).abs().max()), 0, 2)
pi = zk.pivot_table(index=[ZS, "timeperiod_y"], columns=ZI, values="value")
check("rtp11zx_instrument_sum", "consistency", "rtp 11zx", "stocks: N111+N112+N113+N114+N115_N116+N117+N12_N13+N211 "
      "= N0 (max abs diff)", float((pi[["N111", "N112", "N113", "N114", "N115_N116", "N117", "N12_N13", "N211"]]
                                   .sum(axis=1) - pi["N0"]).abs().max()), 0, 2)
for y in ["2022", "2023", "2025"]:
    s14 = pi.loc[("S14", y)]
    check(f"rtp11zx_s14_land_share_{y}", "info", "rtp 11zx", f"{y} households S14: N211 land / (N211 land + N111 "
          f"residential buildings)", float(s14.N211 / (s14.N211 + s14.N111)), None, None,
          "N211 covers all land owned by households (land use not split); an upper bound for land under dwellings")
# Eurostat nama_10_nfa_bs for Finland: which land codes are reported, and agreement with 11zx
nb, _, nb_lab = jsonstat(RAW / ES / "data" / "nama_10_nfa_bs_FI.json")
nb = nb[nb.value.notna()]
land_codes = sorted(c for c in set(nb.asset10) if c.startswith("N211"))
check("eu_nfa_fi_land_codes", "info", "nama_10_nfa_bs", "FI: land asset codes with data (ESA 2010 subdivides "
      "land AN.211 into AN.2111 land underlying buildings and structures, AN.2112 land under cultivation, AN.2113 "
      "recreational land, AN.2119 other land)", len(land_codes), None, None,
      "codes reported: " + ", ".join(land_codes))
for sec, parts in [("S1", ["S0"]), ("S14_S15", ["S14", "S15"])]:
    for y in ["2022", "2023", "2024"]:
        ev = nb[(nb.sector == sec) & (nb.asset10 == "N211N") & (nb.time == y)].value
        check(f"eu_nfa_fi_land_{sec}_{y}", "crosscheck", "nama_10_nfa_bs / rtp 11zx", f"FI {y} {sec} land N211N "
              f"(EUR million) vs StatFin 11zx N211 {' + '.join(parts)}", float(ev.iloc[0]) if len(ev) else None,
              float(sum(pi.loc[(p, y), "N211"] for p in parts)), 0.5)

land = []
k1, _, k1_lab = sf("kihi_11jc")
K1_UNIT = {"kihi-ketjutettu_lv": "index, 2015=100", "kihi-vmuut": "percent change on previous year",
           "realind_lv": "real price index, 2015=100 (deflated by CPI)", "vmuut_real": "percent change, real index",
           "kihi-keskihinta": "EUR per m2 (mean)", "alakvar_hinta": "EUR per m2 (lower quartile)",
           "medianhinta": "EUR per m2 (median)", "ylakvar_hinta": "EUR per m2 (upper quartile)",
           "keskiala": "m2 (mean plot area)", "lkm_julk": "number of sales"}
for r in k1[k1.value.notna()].itertuples(index=False):
    reg = getattr(r, "alue_21_20131212")
    land.append({"source_table": "kihi 11jc", "region_code": reg, "region": k1_lab["alue_21_20131212"][reg],
                 "building_type": "single-family house plot", "rooms": "", "plot_ownership": "",
                 "year": int(r.timeperiod_y), "measure": k1_lab["contentscode"][r.contentscode], "value": r.value,
                 "unit": K1_UNIT[r.contentscode]})
d12, _, d12_lab = sf("ashi_12de")
for r in d12[d12.value.notna()].itertuples(index=False):
    reg, bt, ro, pl = (getattr(r, "alue_3_20181009"), getattr(r, "talotyyppi_5_20111209"),
                       getattr(r, "huoneluku_1_20111212"), getattr(r, "vuokratontti_1_20191126"))
    land.append({"source_table": "ashi 12de", "region_code": reg, "region": d12_lab["alue_3_20181009"][reg],
                 "building_type": "new dwellings: " + d12_lab["talotyyppi_5_20111209"][bt],
                 "rooms": d12_lab["huoneluku_1_20111212"][ro], "plot_ownership": d12_lab["vuokratontti_1_20191126"][pl],
                 "year": int(r.timeperiod_y), "measure": d12_lab["contentscode"][r.contentscode], "value": r.value,
                 "unit": {"lkm_julk_uudet": "number of sales", "keskihinta_uudet": "EUR per m2 (mean)"}[r.contentscode]})
m13, _, m13_lab = sf("ashi_13mw")
for r in m13[m13.value.notna()].itertuples(index=False):
    reg, bt, pl = getattr(r, "alue_43_20220407"), getattr(r, "talotyyppi_6_20131021"), getattr(r, "vuokratontti_1_20191126")
    land.append({"source_table": "ashi 13mw", "region_code": reg, "region": m13_lab["alue_43_20220407"][reg],
                 "building_type": "old dwellings: " + m13_lab["talotyyppi_6_20131021"][bt], "rooms": "",
                 "plot_ownership": m13_lab["vuokratontti_1_20191126"][pl], "year": int(r.timeperiod_y),
                 "measure": m13_lab["contentscode"][r.contentscode], "value": r.value,
                 "unit": {"keskihinta_aritm": "EUR per m2 (mean)", "lkm_julk19": "number of sales",
                          "lkm_julk20": "number of sales"}[r.contentscode]})
write_tidy(pd.DataFrame(land), "fi_land_indicators_long.csv")

# Vintage check against the 2026-06-14 post (raw/post/post.txt), which used these same tables: its Figure 10 text
# gives the Finnish top quintile's net worth per consumption unit, built as its note 30 describes (151u deciles
# pair-averaged to quintiles, bridged to consumption units with the 14pg per-household/per-CU expenditure ratio).
top_q = (mm.loc["nettoae_DN3001", "9"] + mm.loc["nettoae_DN3001", "10"]) / 2
check("post_fig10_top_quintile_net_worth_per_cu", "crosscheck", "vtutk 151u / ktutk 14pg", "(D9 + D10)/2 mean net "
      "wealth per household / (Q5 per-household / per-CU total consumption), EUR; post: 'the Finnish top quintile "
      "holds EUR 391k per consumption unit'", float(top_q / (hb.loc["5", "kulu_kt_hk_1_1"] / hb.loc["5", "kulu_kt_hk_2_1"])),
      391000, 500, "post 2026-06-14, text before Figure 10 and note 30; reproduces, so the post used these vintages")
dec = [str(i) for i in range(1, 11)]
check("post_net_nominal_negative_max", "info", "vtutk 151u", "max over income deciles of mean (deposits + other "
      "financial assets - total debt), EUR; post: 'deposits and bonds minus debts - is negative in every Finnish "
      "income decile'", float((mm.loc["talle", dec] + mm.loc["muufinan", dec] - mm.loc["luototy", dec]).max()), None,
      None, "bonds have no line of their own in 151u (inside 9. other financial assets), so all of item 9 is counted "
      "here as an upper bound; negative in every decile")
check("wealth_to_na_consumption_2023", "info", "vtutk 151u / ntp 15ag", "2023 mean net wealth x households (EUR "
      "million) / national-accounts household consumption P31NCK 2023 (years of consumption)",
      float(mm.loc["nettoae_DN3001", "SS"] * hh23["SS"] / 1e6 / nat.loc["2023", "P31NCK"]), None, None,
      "the post says 'about 3.7 years'; this simple ratio gives about 5, so the post used another wealth or "
      "consumption concept (left to the rebuild step)")


# ---------------------------------------------------------------------------------------------------------
# 11. fi_checks.csv — every verification number; consistency checks must pass
# ---------------------------------------------------------------------------------------------------------
chk = pd.DataFrame(CHECKS)
write_tidy(chk, "fi_checks.csv")
bad = chk[(chk.kind == "consistency") & (chk.passed != True)]
cross_bad = chk[(chk.kind == "crosscheck") & (chk.passed != True)]
print(f"checks: {len(chk)} rows; consistency failures: {len(bad)}; crosscheck failures: {len(cross_bad)}")
for r in cross_bad.itertuples():
    print("  crosscheck not within tolerance:", r.check_id, r.value, r.reference)
assert bad.empty, bad[["check_id", "value", "reference"]].to_string()
