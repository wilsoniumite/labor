"""Independent, adversarial re-derivation of the Australian "paycheck" headline numbers.

Written by a separate verifier, not by the builder. It imports nothing from code/ or checks/check.py and
reads none of the builder's intermediate outputs except out/headline.csv, which it only compares against.

1. Re-downloads every source from the publisher (ABS Data API, ABS website spreadsheets, FRED) into a cache
   directory (default: a fresh temporary directory; pass --cache DIR to keep the files), and compares each
   fresh file with the vendored copy in data/raw/ observation by observation.
2. Recomputes every headline number from the FRESH downloads (falling back to the vendored raw file only if a
   download fails, which it reports), with its own parsing and its own annual-average and chaining code.
3. Cross-checks the WPI against a second publication route (the ABS 6345.0 Table 1 spreadsheet), and labels
   every SDMX code used against the dataflow's own codelists.
4. Runs extra robustness tests the builder did not report (ratio ranges in the US-comparison window, the
   cross-country ratio without audio/visual/computing, electricity after rebates).

Run:  venv/Scripts/python.exe -I austax/paycheck/checks/verify_independent.py [--cache DIR] [--offline]
Exit 0 if every headline matches within rounding, 1 otherwise.
"""
import argparse
import csv
import io
import math
import sys
import tempfile
import xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import openpyxl

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RAW = ROOT / "data" / "raw"
HEADLINE = ROOT / "out" / "headline.csv"

API = "https://data.api.abs.gov.au/rest"
ACCEPT = {"Accept": "application/vnd.sdmx.data+csv"}
CODES = ["10001", "20001", "30014", "97559", "40055", "115524", "40081", "40080", "40058", "131185",
         "40060", "115484", "40098"]
DUR = ["40058", "131185", "40060", "115484", "40098", "40080"]
ENE = ["40055", "115524", "40081"]
RPPI = ("https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/"
        "residential-property-price-indexes-eight-capital-cities/dec-2021/")

SOURCES = {  # name -> (url, headers, vendored file)
    "cpi": (f"{API}/data/ABS,CPI,2.0.0/1.{'+'.join(CODES)}.10.50.Q", ACCEPT, "abs_cpi_v2_index_q.csv"),
    "wpi": (f"{API}/data/ABS,WPI,1.2.0/1.THRPEB.7.TOT.10.AUS.Q", ACCEPT, "abs_wpi_api.csv"),
    "awe": (f"{API}/data/ABS,AWE,1.0.0/3.1.3.7.TOT.10.AUS.S", ACCEPT, "abs_awe_api.csv"),
    "wts": (f"{API}/data/ABS,CPI_WEIGHTS,1.0.0/1.{'+'.join(CODES)}.50.", ACCEPT, "abs_cpi_weights.csv"),
    "mdp": (f"{API}/data/ABS,RES_DWELL_ST,1.0.0/5.AUS.Q", ACCEPT, "abs_res_dwell_mean_price.csv"),
    "mdp_structure": (f"{API}/dataflow/ABS/RES_DWELL_ST/1.0.0?references=all", {}, None),
    "ehpi": (RPPI + "641602.xlsx", {}, "abs_641602_established_house_price_index.xlsx"),
    "ehpi_old": (RPPI + "641608.xlsx", {}, "abs_641608_established_house_price_index_pre2005.xlsx"),
    **{f"fred_{s}": (f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={s}", {}, f"fred_{s}.csv")
       for s in ("AHETPI", "CUSR0000SAD", "CPIUFDNS", "CPIENGNS", "CUSR0000SAH1", "CUUR0000SEHA")},
}
# second publication route for the WPI: ABS 6345.0 Table 1 spreadsheet (tried newest release first)
WPI_XLSX = ["https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/wage-price-index-australia/"
            f"{r}/634501.xlsx" for r in ("jun-2026", "mar-2026", "dec-2025")]

FAILS, LOG = [], []


def say(msg):
    print(msg)
    LOG.append(msg)


def verdict(name, ok, detail=""):
    say(f"{'OK  ' if ok else 'DIFF'}  {name}  {detail}")
    if not ok:
        FAILS.append(name)


# ------------------------------------------------------------------ download
def fetch_all(cache, offline):
    got = {}
    if not offline:
        import requests
        import truststore
        truststore.inject_into_ssl()  # corporate proxy re-signs TLS; verification stays on
        s = requests.Session()
    for name, (url, hdr, vend) in SOURCES.items():
        path = cache / (name + (".xlsx" if url.endswith(".xlsx") else ".xml" if "dataflow" in url else ".csv"))
        if not offline:
            try:
                r = s.get(url, headers=hdr, timeout=180)
                r.raise_for_status()
                path.write_bytes(r.content)
                got[name] = ("fresh", path)
                continue
            except Exception as e:  # noqa: BLE001
                say(f"WARN  download failed for {name}: {e!r}; falling back to vendored file")
        got[name] = ("vendored", RAW / vend) if vend else ("missing", None)
    if not offline:
        for u in WPI_XLSX:
            try:
                r = s.get(u, timeout=180)
                if r.status_code == 200 and r.content[:2] == b"PK":
                    p = cache / "wpi_634501.xlsx"
                    p.write_bytes(r.content)
                    got["wpi_xlsx"] = ("fresh " + u, p)
                    break
            except Exception as e:  # noqa: BLE001
                say(f"WARN  {u}: {e!r}")
    return got


# ------------------------------------------------------------------ parsers (own code)
def sdmx_rows(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def quarterly(rows, **flt):
    """{(year, q): value} from SDMX CSV rows matching every filter (string compare)."""
    out = {}
    for r in rows:
        if all(r[k] == v for k, v in flt.items()) and r["OBS_VALUE"] not in ("", "NaN"):
            tp = r["TIME_PERIOD"]
            out[(int(tp[:4]), tp[5:])] = float(r["OBS_VALUE"])
    return out


def year_means(obs, need):
    """Calendar-year means over complete years: `need` is the set of sub-period labels a year must have."""
    by = defaultdict(dict)
    for (y, p), v in obs.items():
        by[y][p] = v
    return {y: sum(d[p] for p in need) / len(need) for y, d in by.items() if set(need) <= set(d)}


def xlsx_quarterly(path, sid):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb["Data1"]
    rows = list(ws.iter_rows(values_only=True))
    hdr = {i: rows[r] for i, r in enumerate(range(10))}
    j = list(hdr[9]).index(sid)
    meta = [hdr[i][j] for i in range(10)]
    obs = {}
    for r in rows[10:]:
        if isinstance(r[0], datetime) and r[j] is not None:
            obs[(r[0].year, f"Q{(r[0].month - 1) // 3 + 1}")] = float(r[j])
    return obs, meta


def fred(path):
    out = {}
    with open(path, newline="") as f:
        rd = csv.reader(f)
        next(rd)
        for d, v in rd:
            if v not in ("", "."):
                out[(int(d[:4]), d[5:7])] = float(v)
    return out


# ------------------------------------------------------------------ measures
def chain(ann, classes, shares, geometric=False):
    yrs = sorted(set.intersection(*(set(ann[c]) for c in classes)))
    lvl = {yrs[0]: 1.0}
    for a, b in zip(yrs, yrs[1:]):
        assert b == a + 1
        if geometric:
            g = math.exp(sum(shares[c] * math.log(ann[c][b] / ann[c][a]) for c in classes))
        else:
            g = sum(shares[c] * ann[c][b] / ann[c][a] for c in classes)
        lvl[b] = lvl[a] * g
    return lvl


def buys(wage, price, y0, y1):
    """Per cent change in wage/price from y0 to y1."""
    return 100 * ((wage[y1] / price[y1]) / (wage[y0] / price[y0]) - 1)


def growth(s, y0, y1):
    return s[y1] / s[y0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default=None)
    ap.add_argument("--offline", action="store_true", help="use vendored data/raw only")
    a = ap.parse_args()
    cache = Path(a.cache) if a.cache else Path(tempfile.mkdtemp(prefix="paycheck_verify_"))
    cache.mkdir(parents=True, exist_ok=True)
    say(f"cache: {cache}")
    got = fetch_all(cache, a.offline)
    for k, (how, p) in got.items():
        say(f"source {k:22s} {how.split()[0]:9s} {p}")

    # ---------------- 1. fresh vs vendored, observation by observation
    say("\n== 1. fresh downloads vs vendored raw files")
    for name, (url, hdr, vend) in SOURCES.items():
        how, p = got[name]
        if not vend or how != "fresh":
            continue
        if vend.endswith(".csv") and vend.startswith("abs"):
            def keyed(path):
                out = {}
                for r in sdmx_rows(path):
                    key = tuple(v for k, v in r.items() if k not in ("OBS_VALUE", "DATAFLOW", "OBS_STATUS",
                                                                      "OBS_COMMENT", "DECIMALS", "UNIT_MULT",
                                                                      "BASE_PERIOD", "UNIT_MEASURE"))
                    out[key] = r["OBS_VALUE"]
                return out
            fv, vv = keyed(p), keyed(RAW / vend)
        elif vend.startswith("fred"):
            fv, vv = fred(p), fred(RAW / vend)
        else:
            continue
        common = set(fv) & set(vv)
        diff = [k for k in common if abs(float(fv[k] or "nan") - float(vv[k] or "nan")) > 1e-9
                and not (fv[k] in ("", None) and vv[k] in ("", None))]
        verdict(f"{name}: fresh == vendored on common observations", not diff,
                f"[{len(common)} common, {len(fv) - len(common)} only fresh, {len(vv) - len(common)} only vendored, "
                f"{len(diff)} differ{': ' + str(sorted(diff)[:5]) if diff else ''}]")
    for name in ("ehpi", "ehpi_old"):
        how, p = got[name]
        if how == "fresh":
            sid = "A83728456R" if name == "ehpi" else "A2333613R"
            f1, _ = xlsx_quarterly(p, sid)
            f2, _ = xlsx_quarterly(RAW / SOURCES[name][2], sid)
            verdict(f"{name}: fresh == vendored", f1 == f2, f"[{len(f1)} obs]")

    # ---------------- 2. code labels
    say("\n== 2. what the series are")
    how, p = got["mdp_structure"]
    if p:
        root = ET.parse(p).getroot()
        S = "{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/structure}"
        C = "{http://www.sdmx.org/resources/sdmxml/schemas/v2_1/common}"
        for cl in root.iter(S + "Codelist"):
            if "MEASURE" in cl.get("id"):
                for c in cl.findall(S + "Code"):
                    if c.get("id") == "5":
                        say(f"RES_DWELL_ST {cl.get('id')} code 5 = {c.find(C + 'Name').text}")
    for name, sid in (("ehpi", "A83728456R"), ("ehpi_old", "A2333613R")):
        _, meta = xlsx_quarterly(got[name][1], sid)
        say(f"{sid}: {meta[0]!r} | type {meta[2]!r} | unit {meta[3]!r} | freq {meta[4]!r}")

    # ---------------- 3. load (fresh) and annualise
    cpi_rows = sdmx_rows(got["cpi"][1])
    cpiq = {c: quarterly(cpi_rows, MEASURE="1", INDEX=c, TSEST="10", REGION="50", FREQ="Q") for c in CODES}
    Q4 = {"Q1", "Q2", "Q3", "Q4"}
    cpi = {c: year_means(cpiq[c], Q4) for c in CODES}
    wpiq = quarterly(sdmx_rows(got["wpi"][1]), MEASURE="1", INDEX="THRPEB", SECTOR="7", INDUSTRY="TOT",
                     TSEST="10", REGION="AUS", FREQ="Q")
    wpi = year_means(wpiq, Q4)
    awes = quarterly(sdmx_rows(got["awe"][1]), MEASURE="3", ESTIMATE_TYPE="1", SEX="3", SECTOR="7",
                     INDUSTRY="TOT", TSEST="10", REGION="AUS", FREQ="S")
    awe = year_means(awes, {"S1", "S2"})
    say(f"WPI first obs {min(wpiq)}, last {max(wpiq)}; complete years {min(wpi)}-{max(wpi)}")
    say(f"AWE first obs {min(awes)}, last {max(awes)}; complete years {min(awe)}-{max(awe)}")
    for c in CODES:
        say(f"CPI {c:>6s} first {min(cpiq[c])} last {max(cpiq[c])}; complete years {min(cpi[c])}-{max(cpi[c])}")
    wrows = sdmx_rows(got["wts"][1])
    W = defaultdict(dict)
    for r in wrows:
        if r["MEASURE"] == "1" and r["REGION"] == "50" and r["OBS_VALUE"] != "":
            W[r["TIME_PERIOD"]][r["INDEX"]] = float(r["OBS_VALUE"])
    periods = sorted(W)
    say(f"weight vectors: {periods}")

    def shares(period, cl):
        t = sum(W[period][c] for c in cl)
        return {c: W[period][c] / t for c in cl}

    sd, se = shares("2018-Q3", DUR), shares("2018-Q3", ENE)
    say("2018-Q3 durables shares " + ", ".join(f"{c}:{v:.3f}" for c, v in sd.items()))
    say("2018-Q3 energy shares   " + ", ".join(f"{c}:{v:.3f}" for c, v in se.items()))
    dur, ene = chain(cpi, DUR, sd), chain(cpi, ENE, se)
    food, rent, nd, allg = cpi["20001"], cpi["30014"], cpi["97559"], cpi["10001"]
    ehpi_q, _ = xlsx_quarterly(got["ehpi"][1], "A83728456R")
    old_q, _ = xlsx_quarterly(got["ehpi_old"][1], "A2333613R")
    ehpi, old = year_means(ehpi_q, Q4), year_means(old_q, Q4)
    mdp = year_means(quarterly(sdmx_rows(got["mdp"][1]), MEASURE="5", REGION="AUS", FREQ="Q"), Q4)
    say(f"established house complete years {min(ehpi)}-{max(ehpi)}; pre-2005 {min(old)}-{max(old)}; "
        f"mean price {min(mdp)}-{max(mdp)}")

    # ---------------- 4. headline numbers
    say("\n== 3. headline numbers, recomputed from the fresh downloads")
    mine = {}
    for w, s, b in (("wpi", wpi, 1998), ("awe", awe, 1995)):
        mine[f"{w}_pay_buys_change_durable_goods"] = buys(s, dur, b, 2025)
        mine[f"{w}_pay_buys_change_food"] = buys(s, food, b, 2025)
        mine[f"{w}_pay_buys_change_energy"] = buys(s, ene, b, 2025)
        mine[f"{w}_pay_buys_change_rents"] = buys(s, rent, b, 2025)
        mine[f"{w}_pay_buys_change_all_groups_cpi"] = buys(s, allg, b, 2025)
        for c, nm in (("40055", "electricity"), ("115524", "gas_and_other_household_fuels"),
                      ("40081", "automotive_fuel")):
            mine[f"{w}_pay_buys_change_{nm}"] = buys(s, cpi[c], b, 2025)
        mine[f"{w}_ratio_durables_to_rents"] = growth(rent, b, 2025) / growth(dur, b, 2025)
        mine[f"{w}_nominal_growth"] = 100 * (growth(s, b, 2025) - 1)
        alt = [buys(s, chain(cpi, DUR, shares(p, DUR), g), b, 2025) for p in periods for g in (False, True)]
        mine[f"{w}_durables_composite_sensitivity_min"] = min(alt)
        mine[f"{w}_durables_composite_sensitivity_max"] = max(alt)
        nav = [c for c in DUR if c != "40098"]
        mine[f"{w}_durables_excluding_audio_visual_computing"] = buys(s, chain(cpi, nav, shares("2018-Q3", nav)),
                                                                      b, 2025)
        mine[f"{w}_pay_buys_change_new_dwellings_excl_land"] = buys(s, nd, 1999, 2025)
        mine[f"{w}_pay_buys_change_rents_1999_2025"] = buys(s, rent, 1999, 2025)
        mine[f"{w}_pay_buys_change_established_houses"] = buys(s, ehpi, 2002, 2021)
        mine[f"{w}_pay_buys_change_rents_2002_2021"] = buys(s, rent, 2002, 2021)
        for link, tag in ((2002, ""), (2004, "_link2004")):
            spl = {y: (old[y] * ehpi[link] / old[link] if y < link else ehpi[y])
                   for y in range(b, 2022)}
            mine[f"{w}_pay_buys_change_established_houses_spliced{tag}"] = buys(s, spl, b, 2021)
        mine[f"{w}_pay_buys_change_rents_{b}_2021"] = buys(s, rent, b, 2021)
        mine[f"{w}_pay_buys_change_mean_dwelling_price"] = buys(s, mdp, 2012, 2025)
        mine[f"{w}_pay_buys_change_rents_2012_2025"] = buys(s, rent, 2012, 2025)
        mine[f"{w}_window_price_change_audio_visual_computing"] = 100 * (growth(cpi["40098"], b, 2025) - 1)
    mine["awe_nominal_growth_1998_2025"] = 100 * (growth(awe, 1998, 2025) - 1)
    for k, p in (("durable_goods", dur), ("food", food), ("energy", ene), ("rents", rent)):
        mine[f"awe_pay_buys_change_{k}_1998_2025"] = buys(awe, p, 1998, 2025)
    mine["established_houses_splice_seam_2002_2004"] = 100 * (growth(ehpi, 2002, 2004) / growth(old, 2002, 2004) - 1)

    # US, the paper's Figure 5 series, plus rent of primary residence
    def fred_annual(n):
        return year_means(fred(got[f"fred_{n}"][1]), {f"{m:02d}" for m in range(1, 13)})
    ahe = fred_annual("AHETPI")
    us = {k: fred_annual(v) for k, v in (("durables", "CUSR0000SAD"), ("food", "CPIUFDNS"),
                                         ("energy", "CPIENGNS"), ("shelter", "CUSR0000SAH1"),
                                         ("rent_of_primary_residence", "CUUR0000SEHA"))}
    us_last = min(max(ahe), *(max(v) for v in us.values()))
    say(f"US last complete year in every series: {us_last}")
    for k, p in us.items():
        mine[f"us_pay_buys_change_{k}"] = buys(ahe, p, 1998, 2024)
    mine["us_ratio_durables_to_shelter"] = growth(us["shelter"], 1998, 2024) / growth(us["durables"], 1998, 2024)
    mine["us_ratio_durables_to_rent"] = (growth(us["rent_of_primary_residence"], 1998, 2024)
                                         / growth(us["durables"], 1998, 2024))
    mine["ratio_durables_to_rents_1998_2024"] = growth(rent, 1998, 2024) / growth(dur, 1998, 2024)
    anchor_d, anchor_s = 100 + buys(ahe, us["durables"], 1964, 2024), 100 + buys(ahe, us["shelter"], 1964, 2024)
    verdict("US loader: paper's Figure 5 anchors 1964-2024 (durables 376.8, shelter 78.6)",
            abs(anchor_d - 376.8) < 1 and abs(anchor_s - 78.6) < 0.5, f"[{anchor_d:.1f}, {anchor_s:.1f}]")

    # compare
    with open(HEADLINE, newline="", encoding="utf-8") as f:
        H = {r["metric"]: r for r in csv.DictReader(f)}
    for k, v in mine.items():
        if k not in H:
            verdict(f"{k} present in headline.csv", False)
            continue
        bv = float(H[k]["value"])
        dec = 2 if H[k]["unit"] in ("ratio", "points") else 1
        ok = abs(round(v, dec) - bv) <= 10 ** -dec + 1e-9
        verdict(f"{k}", ok, f"[builder {bv}  mine {v:.3f}  {H[k]['period']}]")

    # ---------------- 5. second route for the WPI
    say("\n== 4. WPI through a second publication route (ABS 6345.0 Table 1 spreadsheet)")
    if "wpi_xlsx" in got:
        wb = openpyxl.load_workbook(got["wpi_xlsx"][1], read_only=True, data_only=True)
        rows = list(wb["Data1"].iter_rows(values_only=True))
        cands = [j for j in range(1, len(rows[0])) if rows[0][j] and "Total hourly rates of pay excluding bonuses"
                 in str(rows[0][j]) and "Private and Public" in str(rows[0][j]) and "All industries" in str(rows[0][j])
                 and str(rows[2][j]).strip() == "Original"]
        if cands:
            j = cands[0]
            say(f"spreadsheet series {rows[9][j]}: {rows[0][j]!r}")
            xo = {(r[0].year, f"Q{(r[0].month - 1) // 3 + 1}"): float(r[j]) for r in rows[10:]
                  if isinstance(r[0], datetime) and r[j] is not None}
            common = set(xo) & set(wpiq)
            bad = [k for k in common if abs(xo[k] - wpiq[k]) > 1e-9]
            verdict("WPI API == WPI spreadsheet (original, total hourly excl. bonuses, private+public, all ind.)",
                    not bad and len(common) > 100, f"[{len(common)} common quarters, {len(bad)} differ]")
        else:
            say("WARN  could not identify the original all-sector THRPEB column in 634501.xlsx")
    else:
        say("WARN  634501.xlsx not reachable; second route not tested")

    # ---------------- 6. robustness the builder did not report
    say("\n== 5. extra robustness (not in the builder's report)")
    nav = [c for c in DUR if c != "40098"]
    dur_nav = chain(cpi, nav, shares("2018-Q3", nav))
    r_all = [growth(rent, 1998, 2024) / growth(chain(cpi, DUR, shares(p, DUR), g), 1998, 2024)
             for p in periods for g in (False, True)]
    say(f"AU durables-to-rents ratio 1998-2024: main {mine['ratio_durables_to_rents_1998_2024']:.2f}; "
        f"range over 7 weight vectors x 2 formulas {min(r_all):.2f}-{max(r_all):.2f}; "
        f"without audio/visual/computing {growth(rent, 1998, 2024) / growth(dur_nav, 1998, 2024):.2f}")
    say(f"AU durables-to-rents ratio 1998-2025 without audio/visual/computing: "
        f"{growth(rent, 1998, 2025) / growth(dur_nav, 1998, 2025):.2f}")
    say(f"Motor vehicles alone, rents/motor vehicles 1998-2024: "
        f"{growth(rent, 1998, 2024) / growth(cpi['40080'], 1998, 2024):.2f}")
    say(f"Price changes 1998-2025: rents {100 * (growth(rent, 1998, 2025) - 1):+.1f}%, durables composite "
        f"{100 * (growth(dur, 1998, 2025) - 1):+.1f}%, relative price of durables to rents "
        f"{100 * (growth(dur, 1998, 2025) / growth(rent, 1998, 2025) - 1):+.1f}%")
    say(f"WPI growth 1998-2025 {100 * (growth(wpi, 1998, 2025) - 1):.1f}%; All groups CPI "
        f"{100 * (growth(allg, 1998, 2025) - 1):.1f}%")
    say("Electricity (40055) quarterly index, 2022-Q1..2025-Q4 (rebates from Jul 2023): "
        + ", ".join(f"{y}-{q}:{cpiq['40055'][(y, q)]:.1f}" for (y, q) in sorted(cpiq["40055"]) if y >= 2022))
    say(f"Electricity annual 2023 {cpi['40055'][2023]:.2f}, 2024 {cpi['40055'][2024]:.2f}, 2025 {cpi['40055'][2025]:.2f}")
    say(f"Energy line 1998-2023 (before most rebates hit annual averages): WPI {buys(wpi, ene, 1998, 2023):+.1f}%")
    say(f"AWE and WPI 1998-2025 gap: AWE/WPI growth ratio {growth(awe, 1998, 2025) / growth(wpi, 1998, 2025):.3f}")
    for y0 in (1998, 1995):
        rr = [growth(rent, y0, 2025) / growth(chain(cpi, DUR, shares(p, DUR), g), y0, 2025)
              for p in periods for g in (False, True)]
        say(f"AU durables-to-rents ratio {y0}-2025: range over weight vectors x formulas {min(rr):.2f}-{max(rr):.2f}; "
            f"without audio/visual/computing {growth(rent, y0, 2025) / growth(dur_nav, y0, 2025):.2f}")
    say(f"Established houses, WPI, 2002-2020 (end before the 2021 boom year): {buys(wpi, ehpi, 2002, 2020):+.1f}%; "
        f"2002-2021 {buys(wpi, ehpi, 2002, 2021):+.1f}%")
    # Electricity rebates: ABS (Monthly CPI indicator, June 2025): since June 2023 electricity +0.7% including
    # rebates, +17.4% excluding them, i.e. a level effect of about 1.174/1.007 - 1 = 16.6% at mid-2025.
    # Illustrative only: scale the 2025 electricity annual average up by 10% and by 16.6% and redo the energy line.
    for bump in (0.10, 0.166):
        c2 = dict(cpi)
        c2["40055"] = {y: v * (1 + bump if y == 2025 else 1) for y, v in cpi["40055"].items()}
        say(f"Energy line 1998-2025 with 2025 electricity +{bump:.1%} (rebate-free illustration): "
            f"WPI {buys(wpi, chain(c2, ENE, se), 1998, 2025):+.1f}%; AWE 1995-2025 "
            f"{buys(awe, chain(c2, ENE, se), 1995, 2025):+.1f}%")
    say(f"Energy line by end year (WPI from 1998): " + ", ".join(f"{y} {buys(wpi, ene, 1998, y):+.1f}%"
                                                                 for y in range(2019, 2026)))

    say(f"\n{len(FAILS)} differences: {FAILS}")
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
