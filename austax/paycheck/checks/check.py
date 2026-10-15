"""Independent checks for the Australian paycheck measure.

Re-reads every raw file with the csv module / openpyxl (no pandas, nothing imported from code/), recomputes
every number in out/headline.csv along its own code path, and asserts the build's values. Also checks the
raw-data facts the build relies on. Prints PASS/FAIL per check and exits 1 on any failure.

Run:  venv/Scripts/python.exe austax/paycheck/checks/check.py
"""
import csv
import math
import struct
import sys
from collections import defaultdict
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parent.parent
RAW, OUT = ROOT / "data" / "raw", ROOT / "out"
RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append(ok)
    print(f"{'PASS' if ok else 'FAIL'}  {name}" + (f"  [{detail}]" if detail else ""))


# ------------------------------------------------------------------ independent readers
def read_sdmx(fname, **filters):
    """{period: value} for rows matching every filter column (compared as strings)."""
    out = {}
    with open(RAW / fname, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            if all(row[k] == str(v) for k, v in filters.items()) and row["OBS_VALUE"].strip():
                assert row["TIME_PERIOD"] not in out, ("duplicate", fname, row["TIME_PERIOD"])
                out[row["TIME_PERIOD"]] = float(row["OBS_VALUE"])
    return out


def yearly(obs, per_year):
    """Calendar-year means over years with exactly per_year observations; obs keys start with YYYY."""
    acc = defaultdict(list)
    for k, v in obs.items():
        acc[int(k[:4])].append(v)
    return {y: sum(v) / len(v) for y, v in acc.items() if len(v) == per_year}


def cpi(code, version="2.0.0", quarters=("Q1", "Q2", "Q3", "Q4")):
    f = "abs_cpi_v2_index_q.csv" if version == "2.0.0" else "abs_cpi_v1_index_q.csv"
    obs = read_sdmx(f, MEASURE=1, INDEX=code, TSEST=10, REGION=50, FREQ="Q")
    return yearly({k: v for k, v in obs.items() if k[-2:] in quarters}, len(quarters))


def xlsx_series(fname, sid):
    wb = openpyxl.load_workbook(RAW / fname, read_only=True, data_only=True)
    rows = list(wb["Data1"].iter_rows(values_only=True))
    hdr = next(r for r in rows if r and r[0] == "Series ID")
    j = list(hdr).index(sid)
    start = rows.index(hdr) + 1
    return {(r[0].year, r[0].month): float(r[j]) for r in rows[start:] if r[0] is not None and r[j] is not None}


def fred(sid):
    obs = {}
    with open(RAW / f"fred_{sid}.csv", newline="") as f:
        for row in csv.reader(f):
            if row[0][:1].isdigit() and row[1].strip() not in ("", "."):
                obs[row[0]] = float(row[1])
    return yearly(obs, 12)


# ------------------------------------------------------------------ independent composite
def composite(codes, ann, shares, geometric=False):
    """Chained fixed-share index written from scratch: log/levels accumulated in a dict."""
    common = sorted(set.intersection(*(set(ann[c]) for c in codes)))
    lvl, prev = {common[0]: 1.0}, common[0]
    for y in common[1:]:
        assert y == prev + 1
        if geometric:
            step = math.exp(sum(shares[c] * math.log(ann[c][y] / ann[c][prev]) for c in codes))
        else:
            step = sum(shares[c] * ann[c][y] / ann[c][prev] for c in codes)
        lvl[y] = lvl[prev] * step
        prev = y
    return lvl


def change(wage, price, y0, y1):
    """Per cent change in wage/price between y0 and y1."""
    return 100 * ((wage[y1] / price[y1]) / (wage[y0] / price[y0]) - 1)


def main():
    E = {}  # metric -> independently recomputed value

    # ---- wage: API series, cross-checked against the ABS 6302.0 spreadsheet observation by observation
    awe_obs = read_sdmx("abs_awe_api.csv", MEASURE=3, ESTIMATE_TYPE=1, SEX=3, SECTOR=7, INDUSTRY="TOT",
                        TSEST=10, REGION="AUS", FREQ="S")
    xl = xlsx_series("abs_6302003_awe_original.xlsx", "A85002148L")
    mapped = {(int(p[:4]), 5 if p.endswith("S1") else 11): v for p, v in awe_obs.items()}
    diffs = [k for k in set(mapped) | set(xl) if abs(mapped.get(k, -1) - xl.get(k, -2)) > 1e-9]
    check("AWE API equals ABS 6302.0 Table 3 series A85002148L at every observation", not diffs,
          f"{len(mapped)} obs, mismatches {sorted(diffs)[:4]}")
    check("AWE first observation is November 1994", min(mapped) == (1994, 11), str(min(mapped)))
    awe = yearly(awe_obs, 2)
    wpi = yearly(read_sdmx("abs_wpi_api.csv", MEASURE=1, INDEX="THRPEB", SECTOR=7, INDUSTRY="TOT", TSEST=10,
                           REGION="AUS", FREQ="Q"), 4)

    # ---- CPI classes
    codes = ["10001", "20001", "30014", "97559", "40055", "115524", "40081", "40080", "40058", "131185",
             "40060", "115484", "40098"]
    P = {c: cpi(c) for c in codes}
    P1 = {c: cpi(c, "1.1.0") for c in codes}
    dur = ["40058", "131185", "40060", "115484", "40098", "40080"]
    en = ["40055", "115524", "40081"]
    he = ["40055", "115524"]

    # sub-group identity: Furniture and furnishings (131184) should move like the weighted 40058+131185
    # (tested loosely: both rise over 1995-2025 within 3 points of each other)
    ff = cpi("131184")

    # weights
    W = defaultdict(dict)
    with open(RAW / "abs_cpi_weights.csv", newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            if row["MEASURE"] == "1" and row["REGION"] == "50" and row["OBS_VALUE"].strip():
                W[row["TIME_PERIOD"]][row["INDEX"]] = float(row["OBS_VALUE"])

    def shares(period, cl):
        t = sum(W[period][c] for c in cl)
        return {c: W[period][c] / t for c in cl}

    D = composite(dur, P, shares("2018-Q3", dur))
    EN = composite(en, P, shares("2018-Q3", en))
    HE = composite(he, P, shares("2018-Q3", he))
    defl = {"durable_goods": D, "food": P["20001"], "energy": EN, "rents": P["30014"]}

    # ---- window rules
    last = 2025
    wages = {"wpi": wpi, "awe": awe}
    base = {w: max(min(s), *(min(d) for d in defl.values())) for w, s in wages.items()}
    check("first year the wage and all four deflators exist: WPI 1998 (main), AWE 1995",
          base == {"wpi": 1998, "awe": 1995}, str(base))
    check("2025 complete in every Australian series used; 2026 excluded",
          all(last in s for s in [awe, wpi, *defl.values()]) and all(2026 not in s for s in [awe, wpi, *P.values()]))
    gaps = []
    for c in codes:
        q = read_sdmx("abs_cpi_v2_index_q.csv", MEASURE=1, INDEX=c, TSEST=10, REGION=50, FREQ="Q")
        yrs = range(max(min(base.values()), min(P[c])), last + 1)
        gaps += [(c, y) for y in yrs if not all(f"{y}-Q{k}" in q for k in range(1, 5))]
    check("every CPI class has all four quarters in every year of its window", not gaps, str(gaps[:3]))
    check("seven ABS weight vectors available (2018-Q3..2024-Q4)", len(W) == 7, ",".join(sorted(W)))
    b_nd = min(P["97559"])
    check("New dwelling purchase class first complete year is 1999 (class starts Jun qtr 1998)", b_nd == 1999)

    D1 = composite(dur, P1, shares("2018-Q3", dur))
    EN1 = composite(en, P1, shares("2018-Q3", en))
    defl1 = {"durable_goods": D1, "food": P1["20001"], "energy": EN1, "rents": P1["30014"]}
    js = ("Q1", "Q2", "Q3")
    Pjs = {c: cpi(c, quarters=js) for c in codes}
    defl_js = {"durable_goods": composite(dur, Pjs, shares("2018-Q3", dur)), "food": Pjs["20001"],
               "energy": composite(en, Pjs, shares("2018-Q3", en)), "rents": Pjs["30014"]}
    wpi_q = read_sdmx("abs_wpi_api.csv", MEASURE=1, INDEX="THRPEB", SECTOR=7, INDUSTRY="TOT", TSEST=10,
                      REGION="AUS", FREQ="Q")
    wages_js = {"wpi": yearly({k: v for k, v in wpi_q.items() if k[-2:] in js}, 3),
                "awe": yearly({k: v for k, v in awe_obs.items() if k.endswith("S1")}, 1)}

    def xq_year(fname, sid):
        acc = defaultdict(list)
        for (y, m), v in xlsx_series(fname, sid).items():
            acc[y].append(v)
        return {y: sum(v) / 4 for y, v in acc.items() if len(v) == 4}

    eh = xq_year("abs_641602_established_house_price_index.xlsx", "A83728456R")
    eo = xq_year("abs_641608_established_house_price_index_pre2005.xlsx", "A2333613R")
    check("established house index complete years 2002-2021", (min(eh), max(eh)) == (2002, 2021), f"{min(eh)}-{max(eh)}")
    check("pre-2005-method index complete years 1987-2004", (min(eo), max(eo)) == (1987, 2004), f"{min(eo)}-{max(eo)}")
    mp = yearly(read_sdmx("abs_res_dwell_mean_price.csv", MEASURE=5, REGION="AUS", FREQ="Q"), 4)
    check("mean dwelling price first complete year 2012", min(mp) == 2012, str(min(mp)))

    names = {"40058": "furniture", "131185": "carpets_and_other_floor_coverings", "40060": "major_household_appliances",
             "115484": "small_electric_household_appliances", "40098": "audio_visual_and_computing_equipment",
             "40080": "motor_vehicles", "40055": "electricity", "115524": "gas_and_other_household_fuels",
             "40081": "automotive_fuel", "10001": "all_groups_cpi"}
    nav = [c for c in dur if c != "40098"]

    # ---- every headline number, per wage
    for w, s in wages.items():
        b = base[w]
        for k, d in defl.items():
            E[f"{w}_pay_buys_change_{k}"] = change(s, d, b, last)
        E[f"{w}_pay_buys_change_household_energy_electricity_and_gas"] = change(s, HE, b, last)
        for c, n in names.items():
            E[f"{w}_pay_buys_change_{n}"] = change(s, P[c], b, last)
        E[f"{w}_ratio_durables_to_rents"] = (P["30014"][last] / P["30014"][b]) / (D[last] / D[b])
        E[f"{w}_nominal_growth"] = 100 * (s[last] / s[b] - 1)
        variants = [change(s, composite(dur, P, shares(p, dur), g), b, last) for p in W for g in (False, True)]
        E[f"{w}_durables_composite_sensitivity_min"] = min(variants)
        E[f"{w}_durables_composite_sensitivity_max"] = max(variants)
        E[f"{w}_durables_excluding_audio_visual_computing"] = change(s, composite(nav, P, shares("2018-Q3", nav)), b, last)
        E[f"{w}_pay_buys_change_new_dwellings_excl_land"] = change(s, P["97559"], b_nd, last)
        E[f"{w}_pay_buys_change_rents_{b_nd}_{last}"] = change(s, P["30014"], b_nd, last)
        for k in defl:
            E[f"{w}_rebase_test_{k}_v2_minus_v1_2024"] = change(s, defl[k], b, 2024) - change(s, defl1[k], b, 2024)
            E[f"{w}_seam_test_{k}_jan_sep_minus_full_year"] = (change(wages_js[w], defl_js[k], b, last)
                                                              - change(s, defl[k], b, last))
        E[f"{w}_pay_buys_change_established_houses"] = change(s, eh, 2002, 2021)
        E[f"{w}_pay_buys_change_rents_2002_2021"] = change(s, P["30014"], 2002, 2021)
        E[f"{w}_pay_buys_change_established_homes_pre2005_method"] = change(s, eo, b, 2004)
        # spliced price growth b->2021 = old(link)/old(b) * new(2021)/new(link)
        for link, key in [(2002, "spliced"), (2004, "spliced_link2004")]:
            growth = (eo[link] / eo[b]) * (eh[2021] / eh[link])
            E[f"{w}_pay_buys_change_established_houses_{key}"] = 100 * ((s[2021] / s[b]) / growth - 1)
        E[f"{w}_pay_buys_change_rents_{b}_2021"] = change(s, P["30014"], b, 2021)
        E[f"{w}_pay_buys_change_mean_dwelling_price"] = change(s, mp, 2012, last)
        E[f"{w}_pay_buys_change_rents_2012_{last}"] = change(s, P["30014"], 2012, last)
    for k, d in defl.items():
        E[f"awe_pay_buys_change_{k}_1998_{last}"] = change(awe, d, 1998, last)
    E[f"awe_nominal_growth_1998_{last}"] = 100 * (awe[last] / awe[1998] - 1)
    for w in wages:
        E[f"{w}_window_price_change_audio_visual_computing"] = 100 * (P["40098"][last] / P["40098"][base[w]] - 1)

    # current CPI vintage: quarterly = former quarterly CPI rebased through Sep qtr 2025 (within 0.1 index
    # points, the former series' last decimal), and = mean of the new monthly CPI from Dec qtr 2025
    off_rebase, off_monthly, n_monthly = [], [], 0
    for c in codes:
        m = read_sdmx("abs_cpi_v2_index_m.csv", MEASURE=1, INDEX=c, TSEST=10, REGION=50, FREQ="M")
        q2 = read_sdmx("abs_cpi_v2_index_q.csv", MEASURE=1, INDEX=c, TSEST=10, REGION=50, FREQ="Q")
        q1 = read_sdmx("abs_cpi_v1_index_q.csv", MEASURE=1, INDEX=c, TSEST=10, REGION=50, FREQ="Q")
        ratios = sorted(q2[p] / q1[p] for p in q1 if p in q2 and q1[p] >= 50)
        r = ratios[len(ratios) // 2]
        off_rebase += [(c, p) for p in q1 if p in q2 and abs(q2[p] / r - q1[p]) > 0.1]
        check_q = [p for p in q2 if p >= "2025-Q4"]
        for per in check_q:
            y, k = int(per[:4]), int(per[-1])
            months = [f"{y}-{3 * k - 2 + i:02d}" for i in range(3)]
            n_monthly += 1
            if not all(mm in m for mm in months) or abs(sum(m[mm] for mm in months) / 3 - q2[per]) > 0.0067:
                off_monthly.append((c, per))
        if max(q1) != "2025-Q3":
            off_rebase.append((c, "v1 ends " + max(q1)))
    check("current CPI quarterly = former quarterly CPI rebased (within 0.1 index points, its last decimal) to 2025-Q3",
          not off_rebase, str(off_rebase[:3]))
    check("current CPI quarterly = mean of the new monthly CPI from Dec qtr 2025", not off_monthly and n_monthly > 0,
          f"{n_monthly} quarters, off {off_monthly[:3]}")
    E["established_houses_splice_seam_2002_2004"] = 100 * ((eh[2004] / eh[2002]) / (eo[2004] / eo[2002]) - 1)

    # ---- US context (paper's series), 1998-2024
    ahe = fred("AHETPI")
    us = {"durables": "CUSR0000SAD", "food": "CPIUFDNS", "energy": "CPIENGNS", "shelter": "CUSR0000SAH1",
          "rent_of_primary_residence": "CUUR0000SEHA"}
    U = {k: fred(s) for k, s in us.items()}
    check("US CPI 2025 incomplete (no October 2025 observation in FRED), so the US window ends 2024",
          all(2025 not in u and 2024 in u for u in U.values()))
    for k, u in U.items():
        E[f"us_pay_buys_change_{k}"] = change(ahe, u, 1998, 2024)
    lvl = {k: 1 + E[f"us_pay_buys_change_{k}"] / 100 for k in us}
    E["us_ratio_durables_to_shelter"] = lvl["durables"] / lvl["shelter"]
    E["us_ratio_durables_to_rent"] = lvl["durables"] / lvl["rent_of_primary_residence"]
    pd64 = 100 + change(ahe, U["durables"], 1964, 2024)
    ps64 = 100 + change(ahe, U["shelter"], 1964, 2024)
    check("US loader reproduces the paper's Figure 5 anchors (1964-2024: durables 376.8, shelter 78.6, ratio 4.8)",
          abs(pd64 - 376.8) <= 3.0 and abs(ps64 - 78.6) <= 1.5 and abs(pd64 / ps64 - 4.8) < 0.05,
          f"{pd64:.1f}, {ps64:.1f}, {pd64 / ps64:.2f}")
    for w, s in wages.items():
        for k, d in defl.items():
            E[f"{w}_pay_buys_change_{k}_1998_2024"] = change(s, d, 1998, 2024)
    E["ratio_durables_to_rents_1998_2024"] = (P["30014"][2024] / P["30014"][1998]) / (D[2024] / D[1998])

    # ---- compare with out/headline.csv: every row must be recomputed here, and agree
    with open(OUT / "headline.csv", newline="", encoding="utf-8") as f:
        H = list(csv.DictReader(f))
    missing = [r["metric"] for r in H if r["metric"] not in E]
    check("every headline metric is recomputed independently", not missing, ", ".join(missing))
    extra = [k for k in E if k not in {r["metric"] for r in H}]
    check("no recomputed metric is missing from headline.csv", not extra, ", ".join(extra))
    for r in H:
        if r["metric"] not in E:
            continue
        tol = 0.051 if r["unit"] in ("per cent", "points") else 0.0051
        got, exp = float(r["value"]), E[r["metric"]]
        check(f"{r['metric']} = {got} ({r['period']})", abs(got - exp) <= tol, f"independent {exp:.3f}")

    # ---- sanity facts the write-up relies on
    check("durables/rents ratio is wage-free: identical for WPI and AWE over the same window",
          abs((1 + E["wpi_pay_buys_change_durable_goods"] / 100) / (1 + E["wpi_pay_buys_change_rents"] / 100)
              - (1 + E["awe_pay_buys_change_durable_goods_1998_2025"] / 100)
              / (1 + E["awe_pay_buys_change_rents_1998_2025"] / 100)) < 1e-9)
    check("CPI seam (current vs former quarterly CPI, to 2024) under 0.5 points for all four lines, both wages",
          all(abs(E[f"{w}_rebase_test_{k}_v2_minus_v1_2024"]) < 0.5 for w in wages for k in defl))
    check("CPI seam at Dec qtr 2025: January-September results within 2 points of full-year results",
          all(abs(E[f"{w}_seam_test_{k}_jan_sep_minus_full_year"]) < 2 for w in wages for k in defl))
    check("established-house splice seam under 5 per cent over 2002-2004",
          abs(E["established_houses_splice_seam_2002_2004"]) < 5)
    ff_change = 100 * (ff[last] / ff[1995] - 1)
    w2 = composite(["40058", "131185"], P, shares("2018-Q3", ["40058", "131185"]))
    check("Furniture and furnishings sub-group (131184) close to own two-class composite, 1995-2025",
          abs(ff_change - 100 * (w2[last] / w2[1995] - 1)) < 3.0,
          f"{ff_change:.1f} vs {100 * (w2[last] / w2[1995] - 1):.1f}")

    # ---- annual.csv agrees with the independent pay-buys series for the four lines, every year, both wages
    with open(OUT / "annual.csv", newline="", encoding="utf-8") as f:
        A = {int(r["year"]): r for r in csv.DictReader(f)}
    col = {"durable_goods": "Durable goods", "food": "Food", "energy": "Energy", "rents": "Rents"}
    bad = [(w, y, k) for w, s in wages.items() for y in range(base[w], last + 1) for k, d in defl.items()
           if abs(float(A[y][f"{w} pay buys ({base[w]}=100): {col[k]}"]) - (100 + change(s, d, base[w], y))) > 0.002]
    check("annual.csv four lines match the independent recomputation in every year, both wages", not bad, str(bad[:3]))

    # ---- figures
    for fn in ("figure_au_paycheck.png", "figure_au_paycheck_awe.png"):
        png = OUT / fn
        ok = png.exists() and png.read_bytes()[:8] == bytes([137, 80, 78, 71, 13, 10, 26, 10])
        dpi = None
        if ok:
            b = png.read_bytes()
            i = b.find(b"pHYs")
            if i > 0:
                dpi = round(struct.unpack(">I", b[i + 4:i + 8])[0] * 0.0254)
        check(f"{fn} exists and is a 200 dpi PNG", ok and dpi == 200, f"dpi={dpi}")

    n_fail = RESULTS.count(False)
    print(f"\n{len(RESULTS) - n_fail} PASS, {n_fail} FAIL")
    print("OVERALL:", "PASS" if n_fail == 0 else "FAIL")
    sys.exit(1 if n_fail else 0)


if __name__ == "__main__":
    main()
