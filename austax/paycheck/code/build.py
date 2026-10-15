"""What an hour's (or a week's) pay buys in Australia, by price category: the Australian mirror of the
paper's Figure 5 (US hourly earnings deflated by the CPI for durables, food, energy and shelter).

Wages (both reported):
  wpi  ABS Wage Price Index, total hourly rates of pay excluding bonuses, all sectors and industries, original.
       MAIN series: hourly, fixed job composition, the ABS measure of wage change; 1998 first complete year.
  awe  ABS Average Weekly Earnings, full-time adult ordinary time earnings, persons, original (May and
       November). Starts Nov 1994 (1995 first complete year): only three years longer than the WPI, and the
       ABS says AWE "is not designed to produce movement in earnings data", so it is the comparison series.
Deflators: ABS CPI, weighted average of eight capital cities, original, by group / expenditure class.
Annual averages of complete calendar years; each wage's lines are indexed to 100 in the first year in
which that wage and all four main deflators exist.

Run:  venv/Scripts/python.exe austax/paycheck/code/build.py   (after code/fetch.py)
Writes out/annual.csv, out/headline.csv, out/composite_weights.csv, out/figure_au_paycheck.png (WPI) and
out/figure_au_paycheck_awe.png (AWE alternative).
"""
import csv
import math
import re
from pathlib import Path

import matplotlib
import openpyxl
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
RAW = HERE.parent / "data" / "raw"
OUT = HERE.parent / "out"
OUT.mkdir(exist_ok=True)

LAST_YEAR = 2025           # last complete calendar year in every Australian source (pulled 2026-10-15)
WEIGHT_PERIOD = "2018-Q3"  # earliest ABS CPI weight vector in the API; the six later ones are sensitivity
MAIN_WAGE = "wpi"

CLASS = {  # ABS CPI codes -> names (abs_cpi_v2_structure.xml, codelist CL_CPI_INDEX)
    "10001": "All groups CPI",
    "20001": "Food and non-alcoholic beverages",
    "30014": "Rents",
    "97559": "New dwelling purchase by owner-occupiers",
    "40055": "Electricity",
    "115524": "Gas and other household fuels",
    "40081": "Automotive fuel",
    "40080": "Motor vehicles",
    "40058": "Furniture",
    "131185": "Carpets and other floor coverings",
    "40060": "Major household appliances",
    "115484": "Small electric household appliances",
    "40098": "Audio, visual and computing equipment",
}
DURABLES = ["40058", "131185", "40060", "115484", "40098", "40080"]
ENERGY = ["40055", "115524", "40081"]
HOUSEHOLD_ENERGY = ["40055", "115524"]
MAIN = ["Durable goods", "Food", "Energy", "Rents"]

SRC_CPI = "ABS CPI (dataflow CPI v2.0.0, weighted average of eight capital cities, original)"
WAGES = {
    "wpi": {"name": "Wage Price Index (total hourly rates of pay excl. bonuses)",
            "src": "ABS WPI (dataflow WPI v1.2.0, THRPEB, private and public, all industries, original)",
            "unit": "an hour's pay", "fig": "figure_au_paycheck.png",
            "ylabel": "What an hour's pay buys, indexed to 100 in {base}"},
    "awe": {"name": "Average Weekly Earnings (full-time adult ordinary time earnings, persons)",
            "src": "ABS AWE (dataflow AWE, MEASURE 3, persons, private and public, original)",
            "unit": "a full-time week's ordinary pay", "fig": "figure_au_paycheck_awe.png",
            "ylabel": "What a full-time week's pay buys, indexed to 100 in {base}"},
}


def slug(s):
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


# ---------------------------------------------------------------- loaders
def sdmx(fname):
    return pd.read_csv(RAW / fname, dtype={"INDEX": str, "TIME_PERIOD": str})


def annual_complete(df, n_per_year, keep=None):
    """Mean of OBS_VALUE by calendar year, keeping only years with all n_per_year observations.
    keep: optional set of period suffixes to use (e.g. {"Q1", "Q2", "Q3"}), for the seam test."""
    df = df.dropna(subset=["OBS_VALUE"]).copy()
    if keep:
        df = df[df["TIME_PERIOD"].str[-2:].isin(keep)]
        n_per_year = len(keep)
    df["year"] = df["TIME_PERIOD"].str[:4].astype(int)
    g = df.groupby("year")["OBS_VALUE"].agg(["mean", "count"])
    return g.loc[g["count"] == n_per_year, "mean"]


def cpi_annual(fname, keep=None):
    d = sdmx(fname)
    d = d[(d["MEASURE"] == 1) & (d["TSEST"] == 10) & (d["REGION"] == 50) & (d["FREQ"] == "Q")]
    return {code: annual_complete(d[d["INDEX"] == code], 4, keep) for code in CLASS}


def awe_annual(keep=None):
    d = sdmx("abs_awe_api.csv")
    d = d[(d["MEASURE"] == 3) & (d["ESTIMATE_TYPE"] == 1) & (d["SEX"] == 3) & (d["SECTOR"] == 7)
          & (d["INDUSTRY"] == "TOT") & (d["TSEST"] == 10) & (d["REGION"] == "AUS") & (d["FREQ"] == "S")]
    return annual_complete(d, 2, keep)  # May (S1) and November (S2)


def wpi_annual(keep=None):
    d = sdmx("abs_wpi_api.csv")
    d = d[(d["MEASURE"] == 1) & (d["INDEX"] == "THRPEB") & (d["SECTOR"] == 7) & (d["INDUSTRY"] == "TOT")
          & (d["TSEST"] == 10) & (d["REGION"] == "AUS") & (d["FREQ"] == "Q")]
    return annual_complete(d, 4, keep)


def weights():
    d = sdmx("abs_cpi_weights.csv")
    d = d[(d["MEASURE"] == 1) & (d["REGION"] == 50)]
    return d.pivot_table(index="TIME_PERIOD", columns="INDEX", values="OBS_VALUE")


def abs_xlsx_annual(fname, series_id):
    """Complete-year means of one quarterly series in an ABS time-series workbook (sheet Data1, IDs row 10)."""
    wb = openpyxl.load_workbook(RAW / fname, read_only=True, data_only=True)
    rows = list(wb["Data1"].iter_rows(values_only=True))
    j = rows[9].index(series_id)
    obs = [(r[0], r[j]) for r in rows[10:] if r[0] is not None and r[j] is not None]
    s = pd.DataFrame(obs, columns=["date", "v"])
    s["year"] = [x.year for x in s["date"]]
    g = s.groupby("year")["v"].agg(["mean", "count"])
    return g.loc[g["count"] == 4, "mean"]


def res_dwell_annual():
    d = sdmx("abs_res_dwell_mean_price.csv")
    d = d[(d["MEASURE"] == 5) & (d["REGION"] == "AUS") & (d["FREQ"] == "Q")]
    return annual_complete(d, 4)


def fred_annual(sid):
    d = pd.read_csv(RAW / f"fred_{sid}.csv")
    d.columns = ["date", "v"]
    d["v"] = pd.to_numeric(d["v"], errors="coerce")
    d = d.dropna()
    d["year"] = d["date"].str[:4].astype(int)
    g = d.groupby("year")["v"].agg(["mean", "count"])
    return g.loc[g["count"] == 12, "mean"]


# ---------------------------------------------------------------- composites
def chain(classes, ann, shares, geometric=False):
    """Annually chained composite with fixed expenditure shares: growth = sum_i s_i * (P_i,t / P_i,t-1)
    (or the share-weighted geometric mean when geometric=True). 100 in the first year all classes exist."""
    years = sorted(set.intersection(*(set(ann[c].index) for c in classes)))
    assert years == list(range(years[0], years[-1] + 1)), "gap in a class series"
    level = {years[0]: 100.0}
    for y in years[1:]:
        rel = {c: ann[c][y] / ann[c][y - 1] for c in classes}
        if geometric:
            g = math.exp(sum(shares[c] * math.log(rel[c]) for c in classes))
        else:
            g = sum(shares[c] * rel[c] for c in classes)
        level[y] = level[y - 1] * g
    return pd.Series(level)


def shares_at(W, period, classes):
    w = {c: float(W.loc[period, c]) for c in classes}
    tot = sum(w.values())
    return {c: w[c] / tot for c in classes}


def pay_buys(wage, price, base, end=LAST_YEAR):
    """What the wage buys of a category, indexed to 100 in `base`, through `end`."""
    yrs = [y for y in wage.index if y in price.index and base <= y <= end]
    r = pd.Series({y: wage[y] / price[y] for y in yrs})
    return 100 * r / r[base]


def chg(wage, price, b, e=LAST_YEAR):
    return pay_buys(wage, price, b, e)[e] - 100


# ---------------------------------------------------------------- build
def main():
    cpi = cpi_annual("abs_cpi_v2_index_q.csv")
    cpi_v1 = cpi_annual("abs_cpi_v1_index_q.csv")
    wage = {"wpi": wpi_annual(), "awe": awe_annual()}
    W = weights()
    sh_dur, sh_en, sh_he = (shares_at(W, WEIGHT_PERIOD, c) for c in (DURABLES, ENERGY, HOUSEHOLD_ENERGY))

    def deflators(ann):
        return {
            "Durable goods": chain(DURABLES, ann, sh_dur),
            "Food": ann["20001"],
            "Energy": chain(ENERGY, ann, sh_en),
            "Rents": ann["30014"],
            "Household energy (electricity and gas)": chain(HOUSEHOLD_ENERGY, ann, sh_he),
            **{CLASS[c]: ann[c] for c in DURABLES + ENERGY},
            "All groups CPI": ann["10001"],
        }

    D, D1 = deflators(cpi), deflators(cpi_v1)
    # Seam: the current CPI's quarterly series are the former quarterly CPI (rebased) through Sep qtr 2025
    # and averages of the new complete monthly CPI from Dec qtr 2025. Only Dec qtr 2025 enters the 2025
    # average. Seam test: rerun on January-September averages (CPI and WPI Q1-Q3, AWE May only), which use
    # no quarter of the new measure, and compare.
    D_js = deflators(cpi_annual("abs_cpi_v2_index_q.csv", keep={"Q1", "Q2", "Q3"}))
    wage_js = {"wpi": wpi_annual(keep={"Q1", "Q2", "Q3"}), "awe": awe_annual(keep={"S1"})}
    ND = cpi["97559"]  # New dwelling purchase by owner-occupiers (excludes land), from Jun qtr 1998
    assert all(LAST_YEAR in s.index for s in list(D.values()) + [ND] + list(wage.values()))

    # base year per wage: first year in which that wage and all four main deflators exist (complete years)
    base = {w: max(min(s.index), *(min(D[k].index) for k in MAIN)) for w, s in wage.items()}
    assert base == {"wpi": 1998, "awe": 1995}, base
    b_nd = min(ND.index)
    assert b_nd == 1999

    # house prices: separate comparison, NOT CPI lines
    ehpi = abs_xlsx_annual("abs_641602_established_house_price_index.xlsx", "A83728456R")      # 2002-2021
    ehpi_old = abs_xlsx_annual("abs_641608_established_house_price_index_pre2005.xlsx", "A2333613R")  # 1987-2004
    mp = res_dwell_annual()                                                                  # 2012-2025
    b_e, e_e, e_o, b_m = min(ehpi.index), max(ehpi.index), max(ehpi_old.index), min(mp.index)

    def spliced(link):
        return pd.concat([ehpi_old[ehpi_old.index < link] * ehpi[link] / ehpi_old[link], ehpi[ehpi.index >= link]])

    H = []

    def add(metric, value, period, definition, source, unit="per cent"):
        H.append({"metric": metric, "value": round(float(value), 1 if unit == "per cent" else 2),
                  "unit": unit, "period": period, "definition": definition, "source": source})

    for w, s in wage.items():
        b, info = base[w], WAGES[w]
        src = info["src"] + "; " + SRC_CPI
        per = f"{b}-{LAST_YEAR}"
        tag = "MAIN. " if w == MAIN_WAGE else "Comparison wage. "
        for k in D:
            add(f"{w}_pay_buys_change_{slug(k)}", chg(s, D[k], b), per,
                f"{tag}Change in what {info['unit']} buys of {k}: {info['name']} / CPI({k}), annual averages, "
                f"{LAST_YEAR} vs {b}", src)
        add(f"{w}_ratio_durables_to_rents", pay_buys(s, D["Durable goods"], b)[LAST_YEAR]
            / pay_buys(s, D["Rents"], b)[LAST_YEAR], per,
            f"{tag}Durables-deflated over rents-deflated pay in {LAST_YEAR}, both {b}=100. Equals rents price "
            "growth over durables price growth: the wage cancels", SRC_CPI, unit="ratio")
        add(f"{w}_nominal_growth", 100 * (s[LAST_YEAR] / s[b] - 1), per, f"Nominal growth of the {info['name']}",
            info["src"])
        # durables composite sensitivity: all seven ABS weight vectors, arithmetic and geometric chaining
        alt = [chg(s, chain(DURABLES, cpi, shares_at(W, p, DURABLES), g), b) for p in W.index for g in (False, True)]
        add(f"{w}_durables_composite_sensitivity_min", min(alt), per,
            "Lowest durables result across the seven ABS weight vectors (2018-Q3..2024-Q4), arithmetic and geometric "
            "chaining", src + "; ABS CPI_WEIGHTS")
        add(f"{w}_durables_composite_sensitivity_max", max(alt), per, "Highest durables result, same variants",
            src + "; ABS CPI_WEIGHTS")
        nav = [c for c in DURABLES if c != "40098"]
        add(f"{w}_durables_excluding_audio_visual_computing", chg(s, chain(nav, cpi, shares_at(W, WEIGHT_PERIOD, nav)), b),
            per, "Durables composite without the audio, visual and computing equipment class", src)
        # new dwellings: the CPI class prices the building only, it EXCLUDES land
        add(f"{w}_pay_buys_change_new_dwellings_excl_land", chg(s, ND, b_nd), f"{b_nd}-{LAST_YEAR}",
            f"{info['name']} / CPI(New dwelling purchase by owner-occupiers). The class EXCLUDES land", src)
        add(f"{w}_pay_buys_change_rents_{b_nd}_{LAST_YEAR}", chg(s, D["Rents"], b_nd), f"{b_nd}-{LAST_YEAR}",
            "Rents over the same window as the new-dwelling class", src)
        # CPI vintage tests: (a) history = former quarterly CPI (v1.1.0) rebased, so results to 2024 agree;
        # (b) seam at Dec qtr 2025: January-September result minus full-year result
        for k in MAIN:
            add(f"{w}_rebase_test_{slug(k)}_v2_minus_v1_2024", chg(s, D[k], b, 2024) - chg(s, D1[k], b, 2024),
                f"{b}-2024", "Current CPI minus former quarterly CPI result for 2024, percentage points",
                src + "; ABS CPI v1.1.0", unit="points")
            add(f"{w}_seam_test_{slug(k)}_jan_sep_minus_full_year", chg(wage_js[w], D_js[k], b) - chg(s, D[k], b),
                per, "Result from January-September averages (no quarter of the new monthly-based CPI) minus the "
                "full-year result, percentage points", src, unit="points")
        # house prices
        hsrc = info["src"] + "; ABS 6416.0 "
        add(f"{w}_pay_buys_change_established_houses", chg(s, ehpi, b_e, e_e), f"{b_e}-{e_e}",
            f"{info['name']} / ABS Established House Price Index, eight capitals (houses incl. land; index "
            "discontinued after Dec qtr 2021)", hsrc + "Table 2, A83728456R")
        add(f"{w}_pay_buys_change_rents_{b_e}_{e_e}", chg(s, D["Rents"], b_e, e_e), f"{b_e}-{e_e}",
            "Rents over the same window as the established-house index", src)
        add(f"{w}_pay_buys_change_established_homes_pre2005_method", chg(s, ehpi_old, b, e_o), f"{b}-{e_o}",
            f"{info['name']} / ABS Price Index of Established Homes, pre-Sep 2005 methodology, eight capitals",
            hsrc + "Table 8, A2333613R")
        add(f"{w}_pay_buys_change_established_houses_spliced", chg(s, spliced(2002), b, e_e), f"{b}-{e_e}",
            "SPLICED: pre-2005-method index linked to the current index at the 2002 annual average",
            hsrc + "Tables 2 and 8")
        add(f"{w}_pay_buys_change_established_houses_spliced_link2004", chg(s, spliced(2004), b, e_e), f"{b}-{e_e}",
            "SPLICED as above, linked at the 2004 annual average instead (seam sensitivity)", hsrc + "Tables 2 and 8")
        add(f"{w}_pay_buys_change_rents_{b}_{e_e}", chg(s, D["Rents"], b, e_e), f"{b}-{e_e}",
            "Rents over the same window as the spliced house series", src)
        add(f"{w}_pay_buys_change_mean_dwelling_price", chg(s, mp, b_m), f"{b_m}-{LAST_YEAR}",
            f"{info['name']} / ABS mean price of residential dwellings, Australia (all dwellings incl. land; "
            "not quality adjusted)", info["src"] + "; ABS RES_DWELL_ST measure 5")
        add(f"{w}_pay_buys_change_rents_{b_m}_{LAST_YEAR}", chg(s, D["Rents"], b_m), f"{b_m}-{LAST_YEAR}",
            "Rents over the same window as the mean dwelling price", src)

    # the two wages over the same (WPI) window
    bw = base["wpi"]
    for k in MAIN:
        add(f"awe_pay_buys_change_{slug(k)}_{bw}_{LAST_YEAR}", chg(wage["awe"], D[k], bw), f"{bw}-{LAST_YEAR}",
            f"AWE over the WPI window, for a like-for-like comparison of the two wages: AWE / CPI({k})",
            WAGES["awe"]["src"] + "; " + SRC_CPI)
    add(f"awe_nominal_growth_{bw}_{LAST_YEAR}", 100 * (wage["awe"][LAST_YEAR] / wage["awe"][bw] - 1),
        f"{bw}-{LAST_YEAR}", "Nominal AWE growth over the WPI window", WAGES["awe"]["src"])
    for w in ("wpi", "awe"):
        av = cpi["40098"]
        add(f"{w}_window_price_change_audio_visual_computing", 100 * (av[LAST_YEAR] / av[base[w]] - 1),
            f"{base[w]}-{LAST_YEAR}", "Change in the CPI price index for audio, visual and computing equipment",
            SRC_CPI)
    add("established_houses_splice_seam_2002_2004", 100 * ((ehpi[2004] / ehpi[2002]) / (ehpi_old[2004] / ehpi_old[2002]) - 1),
        "2002-2004", "Seam test: 2002->2004 growth of the current established-house index relative to the "
        "pre-2005-method index, per cent", "ABS 6416.0 Tables 2 and 8")

    # US context with the paper's own Figure 5 series. The FRED CPI files have no October 2025 observation
    # (empty value), so 2025 is not a complete US year: compare over the main window to 2024.
    ahe = fred_annual("AHETPI")
    us = {"durables": "CUSR0000SAD", "food": "CPIUFDNS", "energy": "CPIENGNS", "shelter": "CUSR0000SAH1",
          "rent_of_primary_residence": "CUUR0000SEHA"}
    us_p = {n: fred_annual(sid) for n, sid in us.items()}
    us_end = min(max(ahe.index), *(max(p.index) for p in us_p.values()))
    assert us_end == 2024, us_end
    per_us = f"{bw}-{us_end}"
    us_leg = {n: pay_buys(ahe, p, bw, us_end)[us_end] for n, p in us_p.items()}
    for n, sid in us.items():
        add(f"us_pay_buys_change_{n}", us_leg[n] - 100, per_us,
            f"US context: average hourly earnings of production and nonsupervisory workers / CPI {n}",
            f"FRED AHETPI / {sid}")
    add("us_ratio_durables_to_shelter", us_leg["durables"] / us_leg["shelter"], per_us,
        "US context: durables-deflated over shelter-deflated pay (= shelter over durables price growth)",
        "FRED", unit="ratio")
    add("us_ratio_durables_to_rent", us_leg["durables"] / us_leg["rent_of_primary_residence"], per_us,
        "US context: durables-deflated over rent-of-primary-residence-deflated pay", "FRED", unit="ratio")
    for w in ("wpi", "awe"):
        for k in MAIN:
            add(f"{w}_pay_buys_change_{slug(k)}_{bw}_{us_end}", chg(wage[w], D[k], bw, us_end), per_us,
                f"Australia over the US comparison window: {WAGES[w]['name']} / CPI({k})",
                WAGES[w]["src"] + "; " + SRC_CPI)
    add(f"ratio_durables_to_rents_{bw}_{us_end}", pay_buys(wage["wpi"], D["Durable goods"], bw, us_end)[us_end]
        / pay_buys(wage["wpi"], D["Rents"], bw, us_end)[us_end], per_us,
        "Australia over the US comparison window: durables-deflated over rents-deflated pay (wage cancels)",
        SRC_CPI, unit="ratio")
    # loader gate: the paper's anchors for 1964-2024 (durables 376.8, shelter 78.6)
    g_d = pay_buys(ahe, us_p["durables"], 1964, 2024)[2024]
    g_s = pay_buys(ahe, us_p["shelter"], 1964, 2024)[2024]
    assert abs(g_d - 376.8) <= 3.0 and abs(g_s - 78.6) <= 1.5, (g_d, g_s)

    with open(OUT / "headline.csv", "w", newline="", encoding="utf-8") as f:
        wr = csv.DictWriter(f, fieldnames=["metric", "value", "unit", "period", "definition", "source"])
        wr.writeheader()
        wr.writerows(H)

    # ------------- annual table
    rows = []
    for y in range(min(base.values()), LAST_YEAR + 1):
        row = {"year": y, "awe_dollars_per_week": round(wage["awe"][y], 2),
               "wpi_index": round(wage["wpi"][y], 3) if y in wage["wpi"].index else ""}
        for k in D:
            row[f"cpi: {k}"] = round(D[k][y], 4)
        row["cpi: New dwelling purchase (excludes land)"] = round(ND[y], 4) if y in ND.index else ""
        for w in ("wpi", "awe"):
            for k in D:
                v = pay_buys(wage[w], D[k], base[w])
                row[f"{w} pay buys ({base[w]}=100): {k}"] = round(v[y], 3) if y in v.index else ""
        rows.append(row)
    pd.DataFrame(rows).to_csv(OUT / "annual.csv", index=False)

    with open(OUT / "composite_weights.csv", "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["composite", "cpi_code", "class", "abs_weight_pct_of_all_groups", "share_in_composite",
                     "weight_period"])
        for comp, cl, sh in [("Durable goods", DURABLES, sh_dur), ("Energy", ENERGY, sh_en),
                             ("Household energy", HOUSEHOLD_ENERGY, sh_he)]:
            for c in cl:
                wr.writerow([comp, c, CLASS[c], W.loc[WEIGHT_PERIOD, c], round(sh[c], 4), WEIGHT_PERIOD])

    for r in H:
        print(f"{r['metric']:66s} {r['value']:>8} {r['unit']:9s} {r['period']}")
    for w in ("wpi", "awe"):
        legs = {k: pay_buys(wage[w], D[k], base[w]) for k in MAIN}
        figure(legs, list(range(base[w], LAST_YEAR + 1)), WAGES[w]["ylabel"].format(base=base[w]), WAGES[w]["fig"])


# ---------------------------------------------------------------- figure
def figure(legs, years, ylabel, fname):
    """Blog figure in the style of the US one (drafts/figure/blog_fig_paycheck_plain.py): no title or notes in
    the image, direct end labels, reference palette slots 1-4 in fixed order, white background, 200 dpi."""
    COLORS = {"Durable goods": "#2a78d6", "Rents": "#eb6834", "Food": "#1baf7a", "Energy": "#eda100"}
    INK, MUTED = "#0b0b0b", "#52514e"
    fig, ax = plt.subplots(figsize=(10, 5.6))
    ends = {}
    for name in ("Durable goods", "Food", "Energy", "Rents"):
        ax.plot(years, [legs[name][y] for y in years], color=COLORS[name],
                linewidth=1.5 if name == "Energy" else 2.2, label=name, solid_capstyle="round")
        ends[name] = legs[name][years[-1]]
    top = max(ends.values())
    ymax = 50 * math.ceil((top + 20) / 50)
    gap = 0.032 * ymax  # minimum vertical gap between end labels, in data units
    pos, last = {}, -1e9
    for n in sorted(ends, key=ends.get):
        pos[n] = max(ends[n], last + gap)
        last = pos[n]
    for name, end in ends.items():
        pct = end - 100
        ax.annotate(f"{name} {'+' if pct >= 0 else '−'}{abs(pct):.0f}%", (years[-1], end),
                    xytext=(years[-1] + 0.6, pos[name]), textcoords="data", va="center", fontsize=10.5,
                    color=INK, annotation_clip=False)
    ax.axhline(100, color=MUTED, linewidth=0.8, linestyle=":")
    ax.set_xlim(years[0], years[-1])
    ax.set_ylim(0, ymax)
    ax.set_ylabel(ylabel, color=INK, fontsize=10.5)
    ax.tick_params(colors=MUTED, labelsize=10)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color("#c9c8c3")
    ax.grid(True, axis="y", color="#e6e5e0", linewidth=0.8)
    ax.legend(frameon=False, loc="upper left", fontsize=10)
    fig.tight_layout()
    fig.savefig(OUT / fname, dpi=200, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote", OUT / fname)


if __name__ == "__main__":
    main()
