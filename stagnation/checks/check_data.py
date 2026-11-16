# check_data.py — the battery for the measurements (Sections 1 and 5-7 of "Understanding the Great Stagnation";
# docs/spec.md Section 6). H-X has its own battery (checks/check_hx.py); this one quotes its numbers in the text.
# Groups:
#   F  the cached pulls: every FRED file's SHA-256 equals cache/fred/MANIFEST.csv, all pulled 2026-11-16; the other
#      caches' SHA-256 prefixes equal cache/MANIFEST.md
#   J  every data/*.json the text draws on equals a fresh run of its script's functions on the cache
#   M1 the eras and hours per person recomputed by a second route (resampled annual means); the one known gap
#   M2 the industry panel: industries and sectors counted; the classification grid as the spec states it; the split
#      exact in every member and era; the annual identity; the 1997 splice; the frozen verdict recomputed
#   M3 the split of the gap exact; the BLS labor-share identity; the published share near the implied one; the verdict
#   M4 the Penn World Table values; the counterfactual arithmetic by a second route
#   M5 the verdict by the frozen rule
#   Q  every number in the paper's DATA-NUMBERS regions (the abstract and introduction; Sections 5-7) is printed inside
#      a phrase rebuilt here from recomputed values; no number in those regions left outside such a phrase (bar a
#      short list of inputs and citations); the words that carry a quantity ("about a third") are within their range;
#      the data figures exist, are included, and their captions end with the AI line
# Run from stagnation/:  ../venv/bin/python checks/check_data.py      Exit 0 only if every check passes.
import csv
import hashlib
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
import fred  # noqa: E402
import model as M  # noqa: E402
import m1_eras  # noqa: E402
import m2_industry as M2  # noqa: E402
import m3_gap  # noqa: E402
import m4_hours  # noqa: E402
import m5_recent  # noqa: E402

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok)))
    print(f"{'PASS' if ok else 'FAIL'} {name}" + (f" — {detail}" if detail else ""))


def same(a, b, tol=1e-9):
    """Recursive equality of JSON-like objects, floats to a relative tolerance."""
    if isinstance(a, dict) and isinstance(b, dict):
        return set(map(str, a)) == set(map(str, b)) and all(same(a[k], b[str(k)] if str(k) in b else b[k], tol)
                                                             for k in a)
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(same(x, y, tol) for x, y in zip(a, b))
    if isinstance(a, (bool, np.bool_)) or isinstance(b, (bool, np.bool_)):
        return bool(a) == bool(b)
    if isinstance(a, (int, float, np.floating, np.integer)) and isinstance(b, (int, float, np.floating, np.integer)):
        if np.isnan(a) and np.isnan(b):
            return True
        return abs(float(a) - float(b)) <= tol * max(1.0, abs(float(a)), abs(float(b)))
    return a == b


def jsonable(x):
    return json.loads(json.dumps(x, default=float))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


# ------------------------------------------------------------------------------------------------ F: the caches
rows = list(csv.DictReader((ROOT / "cache" / "fred" / "MANIFEST.csv").open()))
latest = {r["series"]: r for r in rows}                    # a series pulled twice keeps its last row
bad = [s for s, r in latest.items() if sha(ROOT / "cache" / "fred" / f"{s}.csv") != r["sha256"]]
check("F1 every FRED file's SHA-256 equals its manifest row", not bad and set(fred.SERIES) <= set(latest),
      f"{len(latest)} series" + (f"; mismatched {bad}" if bad else ""))
check("F2 every FRED series was pulled on 2026-11-16", all(r["pulled_utc"].startswith("2026-11-16")
                                                          for r in latest.values()))
man = (ROOT / "cache" / "MANIFEST.md").read_text()
others = ["oecd/pdb_raw.csv", "oecd/pop_raw.csv", "pwt/pwt110.xlsx", "bea/KLEMS-Research-Tables-Underlying-Data_0.xlsx",
          "bea/BEA-BLS-industry-level-production-account-1997-2024.xlsx"]
ok = all(re.search(r"`" + re.escape(f) + r"`.*?\| 2026-11-16 \|.*?SHA-256 " + sha(ROOT / "cache" / f)[:8], man)
         for f in others)
check("F3 the OECD, PWT and BEA caches match the SHA-256 prefixes and pull date in cache/MANIFEST.md", ok)

# --------------------------------------------------------------------------------- J: the results, recomputed
a1 = m1_eras.build()
n1 = jsonable(m1_eras.numbers(a1))
check("J1 data/m1_eras.json equals a fresh run of m1_eras.numbers()",
      same(n1, json.loads((ROOT / "data" / "m1_eras.json").read_text())))
p2 = M2.panel()
r2 = {m: M2.decompose(p2, m) for m in M2.GRID}
r2["verdict"] = M2.verdict(r2)
r2["facts"] = M2.facts(p2, r2)
r2["vintage"] = M2.vintage_check(p2)
for m, cls in M2.EXPLORE.items():
    M2.GRID[m] = cls
    r2[m] = M2.decompose(p2, m)
    del M2.GRID[m]
r2 = jsonable(r2)
check("J2 data/m2_decomp.json equals a fresh run of m2_industry (grid, verdict, facts, vintage, X1)",
      same(r2, json.loads((ROOT / "data" / "m2_decomp.json").read_text())))
a3 = m3_gap.build()
r3 = jsonable({"identity_max_dev": m3_gap.identity_gap(a3),
               **{f"{y0}-{y1}": m3_gap.split(a3, y0, y1) for y0, y1 in m3_gap.WINDOWS}})
check("J3 data/m3_gap.json equals a fresh run of m3_gap", same(r3, json.loads((ROOT / "data" / "m3_gap.json").read_text())))
h4 = m4_hours.load()
r4 = jsonable(m4_hours.envelope(h4)[0])
check("J4 data/m4_hours.json equals a fresh run of m4_hours",
      same(r4, json.loads((ROOT / "data" / "m4_hours.json").read_text())))
r5 = jsonable(m5_recent.run())
check("J5 data/m5_recent.json equals a fresh run of m5_recent",
      same(r5, json.loads((ROOT / "data" / "m5_recent.json").read_text())))
hx = json.loads((ROOT / "data" / "hx_results.json").read_text())   # recomputed by checks/check_hx.py
NUM = M.numbers()

# ------------------------------------------------------------------------------- M1: a second route to the eras
def annual_second_route(sid):
    s = pd.read_csv(ROOT / "cache" / "fred" / f"{sid}.csv", parse_dates=["observation_date"]).set_index(
        "observation_date")[sid]
    y = s.resample("YS")
    mean, cnt = y.mean(), y.count()
    mean.index = mean.index.year
    cnt.index = cnt.index.year
    return mean, cnt


op, opn = annual_second_route("OPHNFB")
gr = lambda s, y0, y1: 100 * (np.log(s[y1]) - np.log(s[y0])) / (y1 - y0)  # noqa: E731
check("M1.1 the eras of output per hour by a second route (resampled means of the raw CSV)",
      all(opn[y] == 4 for y in range(1948, 2026)) and
      all(abs(gr(op, y0, y1) - n1["output_per_hour"][f"{y0}-{y1}"]) < 1e-10 for y0, y1 in m1_eras.ERAS))
hb, hbn = annual_second_route("HOANBS")
pop, popn = annual_second_route("CNP16OV")
hpp = hb / pop
check("M1.2 hours per person by a second route", all(abs(gr(hpp, y0, y1) - n1["hours_per_person"][f"{y0}-{y1}"]) < 1e-10
                                                    for y0, y1 in m1_eras.ERAS))
s_pop = fred.fetch("CNP16OV")
miss = sorted(set(pd.period_range("1948-01", "2025-12", freq="M").astype(str)) - set(s_pop.index.strftime("%Y-%m")))
check("M1.3 the population series lacks one month in 1948-2025, October 2025 (the shutdown), and 2025 averages 11",
      miss == ["2025-10"] and popn[2025] == 11, f"missing {miss}")
rr = a1.REAINTRATREARAT10Y.dropna()
tips = a1.DFII10.dropna()
land = a1.land_share.dropna()
check("M1.4 first years: the Cleveland Fed rate 1982, TIPS 2003, land's share 1952 (Figure 3's caption)",
      int(rr.index.min()) == 1982 and int(tips.index.min()) == 2003 and int(land.index.min()) == 1952)

# ----------------------------------------------------------------------------------------- M2: the industry panel
ra, rb = M2.research()
n_ind = (ra.indnum.nunique(), rb.indnum.nunique())
check("M2.1 44 industries in the 1947-63 sheet, 63 after; 20 sectors in the panel", n_ind == (44, 63)
      and p2.sector.nunique() == 20 == len(M2.NAMES), f"{n_ind}, {p2.sector.nunique()} sectors")
G1 = M2.G1
spec_ok = (set(G1) == {"mfg", "whl", "trn", "inf", "fin", "pro", "mgt", "ret", "adm", "agr", "min", "utl", "con", "edu",
                       "hea", "art", "acc", "oth"}
           and [k for k, v in G1.items() if v == "S"] == ["agr", "min", "utl", "con"]
           and sorted(k for k, v in G1.items() if v == "H") == ["acc", "art", "edu", "hea", "oth"]
           and M2.GRID["G2"] == {**G1, "ret": "H", "adm": "H"} and M2.GRID["G3"] == {**G1, "utl": "M"}
           and M2.GRID["G4"] == {**G1, "gov": "H"} and M2.GRID["G5"] == {**G1, "rea": "S"}
           and M2.GRID["G6"] == {**G1, "acc": "S"} and set(M2.EXPLORE["X1"]) == set(G1) - {"agr"})
check("M2.2 the grid G1-G6 as docs/spec.md states it; X1 is G1 without agriculture", spec_ok)
check("M2.3 the era split is exact in every member and era (and in X1)",
      all(r2[m][e]["exact"] for m in list(M2.GRID) + ["X1"] for e in r2[m]))
q = M2.annual_terms(p2, list(G1))
lhs = q.groupby("year").apply(lambda d: (d.within + d.realloc).sum(), include_groups=False)
rhs = q.groupby("year").apply(lambda d: (d.s_bar * d.g_va).sum() - (d.h_bar * d.g_hours).sum(), include_groups=False)
check("M2.4 each year, within + reallocation = sum s g_Y - sum h g_H (the decomposition's identity)",
      float((lhs - rhs).abs().max()) < 1e-12)
h97 = rb[rb.yr == 1997].groupby("sector").hrs.sum()
check("M2.5 the splice: the panel's 1997 hours by sector are the research tables' (the release carries them forward)",
      all(abs(p2[(p2.year == 1997) & (p2.sector == s_)].hours.iloc[0] - h97[s_]) < 1e-9 * h97[s_] for s_ in h97.index))
ver = {}
for era in ("1973-1995", "2004-2019"):
    shares = [r2[m][era]["composition_share"] for m in M2.GRID]
    comps = [r2[m][era]["composition"] for m in M2.GRID]
    med = float(np.median(shares))
    ver[era] = ("supports" if np.median(comps) < 0 and med >= 0.25 else
                "counts against" if np.median(comps) >= 0 or med <= 0.10 else "partial")
check("M2.6 the frozen verdict recomputed on G1-G6 only (X1 excluded): supports in both eras",
      ver == {"1973-1995": "supports", "2004-2019": "supports"} == {e: r2["verdict"][e]["verdict"] for e in ver}
      and r2["verdict"]["overall"] == "supports")
x1 = {e: ("supports" if r2["X1"][e]["composition"] < 0 and r2["X1"][e]["composition_share"] >= 0.25 else
          "counts against" if r2["X1"][e]["composition"] >= 0 or r2["X1"][e]["composition_share"] <= 0.10 else
          "partial") for e in ("1973-1995", "2004-2019")}
x1_overall = "supports" if all(v == "supports" for v in x1.values()) else "partial"
check("M2.7 X1 read by the same thresholds: partial overall", x1_overall == "partial", str(x1))
check("M2.8 composition is negative in both slow eras in every member, and both of its terms in the baseline",
      all(r2[m][e]["composition"] < 0 for m in M2.GRID for e in ("1973-1995", "2004-2019"))
      and all(r2["G1"][e][k] < 0 for e in ("1973-1995", "2004-2019") for k in ("weight_shift", "realloc_change")))

# ------------------------------------------------------------------------------------------- M3: pay and prices
check("M3.1 the split of the gap is exact in both windows", all(abs(r3[w]["split_residual"]) < 1e-9
                                                                for w in ("1973-2024", "1983-2024")))
check("M3.2 BLS's labor share equals compensation over current-dollar output up to 0.07 log points over 1948-2024, and"
      " its change over each window is within 1.5 log points of the implied share's",
      r3["identity_max_dev"] < 0.07 and all(abs(r3[w]["share_term_published"] - r3[w]["share_term"]) < 1.5
                                            for w in ("1973-2024", "1983-2024")))
v3 = {w: ("supports" if r3[w]["wedge_cpi"] > 0 and r3[w]["removed_by_ex_shelter"] >= 1 / 3 else
          "counts against" if r3[w]["wedge_cpi"] <= 0 or r3[w]["removed_by_ex_shelter"] <= 0.1 else "partial")
      for w in ("1973-2024", "1983-2024")}
check("M3.3 the frozen verdict recomputed: supports in both windows", all(v == "supports" for v in v3.values())
      and all(r3[w]["verdict"] == v3[w] for w in v3))

# ----------------------------------------------------------------------------------------- M4: the hours per worker
pwt = pd.read_excel(ROOT / "cache" / "pwt" / "pwt110.xlsx", sheet_name="Data")
us = pwt[pwt.countrycode == "USA"].set_index("year").avh
check("M4.1 Penn World Table 11.0, U.S. average hours 1950, 1980, 2023 as quoted",
      all(abs(us[y] - r4[k]) < 1e-9 for y, k in ((1950, "us_1950"), (1980, "us_1980"), (2023, "us_end")))
      and r4["year_end"] == 2023)
eu = np.exp(np.log(pwt[pwt.countrycode.isin(m4_hours.EUROPE)].pivot_table(index="year", columns="countrycode",
                                                                         values="avh")).mean(axis=1))
cf_trend = us[1980] * (us[1980] / us[1950]) ** ((2023 - 1980) / 30)
cf_eu = us[1980] * eu[2023] / eu[1980]
eps = NUM["eps_base"]
check("M4.2 the counterfactuals and the envelope by a second route",
      abs(cf_trend - r4["cf_trend"]) < 1e-8 and abs(cf_eu - r4["cf_europe"]) < 1e-8
      and abs(100 * ((us[2023] / cf_trend) ** (-eps) - 1) - r4["pi_level_pct_trend_mid"]) < 1e-9
      and m4_hours.ELASTICITIES == (-1.0, eps, -0.4))

# ------------------------------------------------------------------------------------------------- M5: since 2019
holds = r5["faster"] and not r5["rising_hours"] and r5["compressed"]
against = r5["faster"] and r5["rising_hours"] and not r5["compressed"]
check("M5.1 by the frozen rule the prediction holds and nothing counts against it",
      holds and not against and r5["prediction_holds"] and not r5["counts_against"])

# --------------------------------------------------------------------------------------------- Q: the text
TEX = ROOT / "paper" / "main.tex"
tex = TEX.read_text()
regions = re.findall(r"% DATA-NUMBERS-BEGIN(.*?)% DATA-NUMBERS-END", tex, flags=re.S)
check("Q0 the data regions are marked (the abstract and introduction; Sections 5-7)",
      len(regions) == 2 and r"\begin{abstract}" in regions[0] and r"\section{Measurement}" in regions[1]
      and r"\section{Conclusion}" in regions[1])
text = re.sub(r"\s+", " ", " %%%% ".join(regions))

f0 = lambda x: f"{x:.0f}"          # noqa: E731
f1 = lambda x: f"{x:.1f}"          # noqa: E731
f2 = lambda x: f"{x:.2f}"          # noqa: E731
pc = lambda x: f"{100 * x:.0f}"    # noqa: E731
th = lambda x: f"{x:,.0f}"         # noqa: E731
e = n1["output_per_hour"]
hp = n1["hours_per_person"]
G = r2["G1"]
V = r2["verdict"]
F = r2["facts"]
X1 = r2["X1"]
W1, W2 = r3["1973-2024"], r3["1983-2024"]
pr, pa, iv = hx["primary"], hx["panel"], hx["iv_pwt"]
LS, RR, LA = n1["labor_share"], n1["real_rate"], n1["land_share"]
VI = r2["vintage"]
assert RR["min_value"] < 0 and RR["tips_2020"] < 0 and pr["beta"] > 0 and pa["beta"] < 0 and iv["beta"] > 0
assert all(hp[k] < 0 for k in ("1948-1973", "1995-2004", "2004-2019", "2019-2025")) and hp["1973-1995"] > 0
assert all(F["sector_productivity"][k]["con"] < 0 for k in ("1973-1995", "2004-2019"))
assert r4["us_rate_1950_1980"] < 0 and r4["us_rate_1980_end"] < 0 and r4["eu_rate_1950_1980"] < 0
assert r5["hours_pp_2019_2025"] < 0 and W2["removed_by_ex_energy"] < 0 < W1["removed_by_ex_energy"]

PHRASES = [
    # the abstract
    f"account for {pc(V['1973-1995']['median_share'])} and {pc(V['2004-2019']['median_share'])} percent of the "
    f"slowdowns of 1973--95 and 2004--19, though {pc(X1['1973-1995']['composition_share'])} and "
    f"{pc(X1['2004-2019']['composition_share'])} percent once the end of the farm exodus is set aside",
    # the introduction
    f"grew {f1(e['1948-1973'])} percent a year between 1948 and 1973. It grew {f1(e['1973-1995'])} percent a year "
    f"between 1973 and 1995 and, after a decade of {f1(e['1995-2004'])} percent during the spread of information "
    f"technology, {f1(e['2004-2019'])} percent a year between 2004 and 2019",
    f"fell {f0(-LS['pct_2000_2025'])} percent between 2000 and 2025, after falling {f1(-LS['pct_1948_2000'])} percent "
    f"over the half century before",
    f"which fell {f2(-r4['us_rate_1950_1980'])} percent a year between 1950 and 1980, have fallen "
    f"{f2(-r4['us_rate_1980_end'])} percent a year since",
    f"fell from {f1(RR['avg_1982_1984'])} percent in 1982--84 to below zero in {RR['min_year']}",
    f"{f0(LA['avg_1952_1972'])} percent of the value of households' owner-occupied real estate in 1952--72 and "
    f"{f0(LA['avg_2004_2019'])} percent in 2004--19",
    f"output per hour is {pc(NUM['pi_drop_enclosed'])} percent lower when nobody can leave work",
    f"account for {pc(V['1973-1995']['median_share'])} percent of the slowdown of 1973--95 against 1948--73 and "
    f"{pc(V['2004-2019']['median_share'])} percent of that of 2004--19",
    f"without agriculture the shares are {pc(X1['1973-1995']['composition_share'])} and "
    f"{pc(X1['2004-2019']['composition_share'])} percent",
    f"makes up {pc(W1['wedge_share_of_gap'])} percent of the gap between pay and productivity since 1973, and shelter "
    f"accounts for {pc(W1['removed_by_ex_shelter'])} percent of that rise",
    # 5.1
    f"Output per hour grew {f1(e['1948-1973'])} percent a year in 1948--73, {f1(e['1973-1995'])} in 1973--95, "
    f"{f1(e['1995-2004'])} in 1995--2004, {f1(e['2004-2019'])} in 2004--19 and {f1(e['2019-2025'])} in 2019--25",
    f"fell {f2(-hp['1948-1973'])} percent a year in 1948--73, rose {f2(hp['1973-1995'])} percent a year in 1973--95, "
    f"and fell in every era since: {f2(-hp['1995-2004'])} percent a year in 1995--2004, {f2(-hp['2004-2019'])} in "
    f"2004--19 and {f2(-hp['2019-2025'])} in 2019--25",
    f"at most {f2(n1['lemma1_hours_pp_1973_1995']['at_most'])} points a year of that era's slowdown of "
    f"{f1(n1['slowdown']['1973-1995'])} points against 1948--73, and for "
    f"{f2(n1['lemma1_hours_pp_1973_1995']['instance'])} at the instance's elasticity",
    f"fell {f1(-LS['pct_1948_2000'])} percent between 1948 and 2000 and {f0(-LS['pct_2000_2025'])} percent between "
    f"2000 and 2025, when it was at its lowest",
    f"averaged {f1(RR['avg_1982_1984'])} percent in 1982--84 and reached its low in {RR['min_year']}, "
    f"$-{f2(-RR['min_value'])}$ percent",
    f"was $-{f2(-RR['tips_2020'])}$ percent that year and {f2(RR['tips_2025'])} percent in 2025",
    f"averaged {f0(LA['avg_1952_1972'])} percent in 1952--72 and {f0(LA['avg_2004_2019'])} percent in 2004--19; it "
    f"peaked at {f0(LA['peak'])} percent in {LA['peak_year']} and was {f0(LA['y2025'])} percent in 2025",
    # 5.2
    f"for {n_ind[1]} industries ({n_ind[0]} before 1963",
    f"to {p2.sector.nunique()} sectors",
    f"grew {f2(G['1948-1973']['growth'])} percent a year in 1948--73, {f2(G['1973-1995']['growth'])} in 1973--95, "
    f"{f2(G['1995-2004']['growth'])} in 1995--2004, {f2(G['2004-2019']['growth'])} in 2004--19 and "
    f"{f2(G['2019-2024']['growth'])} in 2019--24",
    f"The slowdown of {f2(-G['1973-1995']['change'])} points a year in 1973--95 splits into "
    f"{f2(-G['1973-1995']['within_slowdown'])} within sectors, {f2(-G['1973-1995']['weight_shift'])} from the shift "
    f"of value added and {f2(-G['1973-1995']['realloc_change'])} from the reallocation of hours; the slowdown of "
    f"{f2(-G['2004-2019']['change'])} points in 2004--19 into {f2(-G['2004-2019']['within_slowdown'])}, "
    f"{f2(-G['2004-2019']['weight_shift'])} and {f2(-G['2004-2019']['realloc_change'])}",
    f"composition is {pc(V['1973-1995']['median_share'])} percent of the 1973--95 slowdown (the median; the range is "
    f"{pc(V['1973-1995']['min_share'])} to {pc(V['1973-1995']['max_share'])}) and "
    f"{pc(V['2004-2019']['median_share'])} percent of the 2004--19 slowdown ({pc(V['2004-2019']['min_share'])} to "
    f"{pc(V['2004-2019']['max_share'])}), and it is negative in every member",
    f"of {f2(VI['growth_1998_2016_newer'])} percent a year and the older {f2(VI['growth_1998_2016_older'])}. On the "
    f"older file alone, composition is {pc(VI['share_2004_2016_older']['median'])} percent of the 2004--16 slowdown "
    f"(the median over the grid; the range is {pc(VI['share_2004_2016_older']['min'])} to "
    f"{pc(VI['share_2004_2016_older']['max'])}), against {pc(VI['share_2004_2016_spliced']['median'])} percent "
    f"({pc(VI['share_2004_2016_spliced']['min'])} to {pc(VI['share_2004_2016_spliced']['max'])}) on the spliced panel",
    f"Agriculture held {f0(F['agr_hours_share']['1948'])} percent of the hours in scope in 1948 and "
    f"{f0(F['agr_hours_share']['1973'])} percent in 1973",
    f"the reallocation term added {f2(G['1948-1973']['growth_realloc'])} points a year to growth in 1948--73",
    f"Agriculture alone accounts for {f2(-F['realloc_change_by_sector']['1973-1995']['agr'])} of the "
    f"{f2(-G['1973-1995']['realloc_change'])} points by which the reallocation term fell in 1973--95, and for "
    f"{f2(-F['realloc_change_by_sector']['2004-2019']['agr'])} of the {f2(-G['2004-2019']['realloc_change'])} points "
    f"in 2004--19",
    f"composition is {pc(X1['1973-1995']['composition_share'])} percent of the 1973--95 slowdown and "
    f"{pc(X1['2004-2019']['composition_share'])} percent of the 2004--19 slowdown: partial by the same thresholds",
    f"within sectors: {pc(F['within_share_of_change']['1973-1995'])} percent in 1973--95 and "
    f"{pc(F['within_share_of_change']['2004-2019'])} percent in 2004--19 in the baseline, with manufacturing the "
    f"largest single piece in both",
    f"growth of output per hour of {f1(F['sector_productivity']['1948-1973']['con'])} percent a year in 1948--73 to "
    f"declines of {f1(-F['sector_productivity']['1973-1995']['con'])} percent a year in 1973--95 and "
    f"{f1(-F['sector_productivity']['2004-2019']['con'])} percent a year in 2004--19",
    f"growth within sectors added {f2(G['1995-2004']['within_slowdown'])} points a year more than in 1948--73, all of "
    f"it in the machine-contestable sectors, while composition took away {f2(-G['1995-2004']['composition'])} points, "
    f"as much as in the slow eras",
    f"share of hours rose from {f0(F['hours_share']['1948']['H'])} percent in 1948 to "
    f"{f0(F['hours_share']['2024']['H'])} percent in 2024, and their share of value added from "
    f"{f0(F['va_share']['1948']['H'])} to {f0(F['va_share']['2024']['H'])} percent",
    # 5.3
    f"rose {f0(W1['productivity'])} log points and hourly compensation deflated by the consumer price index (CPI) rose "
    f"{f0(W1['real_pay_cpi'])}, a gap of {f0(W1['gap_cpi'])} points",
    f"the fall in labor's share, {f0(W1['share_term'])} points, and the rise of consumer prices relative to the "
    f"sector's output prices, {f0(W1['wedge_cpi'])} points, or {pc(W1['wedge_share_of_gap'])} percent of the gap",
    f"The share BLS publishes falls {f0(W1['share_term_published'])} log points",
    f"the wedge is {f0(W1['wedge_ex_shelter'])} points, so shelter accounts for {pc(W1['removed_by_ex_shelter'])} "
    f"percent of it",
    f"the gap is {f0(W2['gap_cpi'])} points, the wedge {f0(W2['wedge_cpi'])}, or {pc(W2['wedge_share_of_gap'])} percent "
    f"of the gap, and shelter's part {pc(W2['removed_by_ex_shelter'])} percent",
    f"removing energy removes {pc(W1['removed_by_ex_energy'])} percent of the wedge over 1973--2024 and widens it by "
    f"{pc(-W2['removed_by_ex_energy'])} percent from 1983; removing medical care, a service that requires people, "
    f"removes {pc(W1['removed_by_ex_medical'])} percent in both windows",
    # 5.4
    f"fell from {th(r4['us_1950'])} in 1950 to {th(r4['us_1980'])} in 1980, or {f2(-r4['us_rate_1950_1980'])} percent "
    f"a year, and then to {th(r4['us_end'])} in 2023, or {f2(-r4['us_rate_1980_end'])} percent a year",
    f"they fell {f2(-r4['eu_rate_1950_1980'])} percent a year before 1980 and {f2(-r4['eu_rate_1980_end'])} percent a "
    f"year after",
    f"they would have been {th(r4['cf_trend'])} in 2023, {f1(r4['hours_gap_pct_trend'])} percent fewer than they were; "
    f"had they followed the European path from their 1980 level, {th(r4['cf_europe'])}, or "
    f"{f1(r4['hours_gap_pct_europe'])} percent fewer",
    f"At the instance's elasticity, $-{f2(-eps)}$, output per hour in 2023 would have been "
    f"{f1(r4['pi_level_pct_trend_mid'])} percent higher on the U.S. trend, or {f2(r4['pi_growth_pp_trend_mid'])} "
    f"points a year over 1980--2023, and between {f1(r4['pi_level_pct_trend_hi'])} and "
    f"{f1(r4['pi_level_pct_trend_lo'])} percent higher ({f2(r4['pi_growth_pp_trend_hi'])} to "
    f"{f2(r4['pi_growth_pp_trend_lo'])} points a year) for elasticities between $-0.4$ and $-1$; on the European "
    f"path, {f1(r4['pi_level_pct_europe_mid'])} percent higher ({f1(r4['pi_level_pct_europe_hi'])} to "
    f"{f1(r4['pi_level_pct_europe_lo'])})",
    f"output per hour grew {f2(r4['ophnfb_rate_1980_end'])} percent a year, against {f2(r4['ophnfb_rate_1948_1973'])} "
    f"in 1948--73: the {f2(r4['pi_growth_pp_trend_mid'])} points are {pc(r4['envelope_share_trend_mid'])} percent of "
    f"that slowdown of {f2(r4['slowdown_1980_end'])} points, and {pc(r4['envelope_share_trend_hi'])} to "
    f"{pc(r4['envelope_share_trend_lo'])} percent across the range of elasticities",
    # 5.5
    f"The sample has {hx['n']} countries; Colombia, Estonia and Korea lack some years",
    f"Across countries the coefficient is $+{f2(pr['beta'])}$ (standard error {f2(pr['se'])}, $p={f2(pr['p'])}$",
    f"Within countries it is $-{f2(-pa['beta'])}$, with a bootstrap $p$-value of {pa['p_boot']:.3f}",
    f"between {f2(hx['loo_beta_range'][0])} and {f2(hx['loo_beta_range'][1])}, never significant",
    f"gives $+{f2(iv['beta'])}$ ($p={f2(iv['p'])}$)",
    f"with a standard error of {f2(pr['se'])}, rules it out",
    f"aged 15--64, {hx['n']} OECD countries",
    f"(an added-variable plot; slope $+{f2(pr['beta'])}$)",
    f"net of country and period effects (slope $-{f2(-pa['beta'])}$)",
    # 5.6
    f"Output per hour grew {f2(r5['productivity_2019_2025'])} percent a year between 2019 and 2025, against "
    f"{f2(r5['productivity_2004_2019'])} in 2004--19, and {f2(r5['productivity_q4_2019_to_last'])} percent a year from "
    f"the fourth quarter of 2019 to the third quarter of 2026",
    f"Hours per person aged 16 and over fell {f2(-r5['hours_pp_2019_2025'])} percent a year, against "
    f"{f2(-r5['hours_pp_2004_2019'])} in 2004--19",
    f"rose from {r5['compression_level_2019']:.3f} to {r5['compression_level_2025']:.3f} of those of all private "
    f"employees, or {f2(r5['compression_2019_2025'])} percent a year, against {f2(r5['compression_2007_2019'])} percent "
    f"a year in 2007--19",
    # Section 6, Table 1
    f"{pc(V['1973-1995']['median_share'])} and {pc(V['2004-2019']['median_share'])} percent (medians over the grid; "
    f"ranges {pc(V['1973-1995']['min_share'])}--{pc(V['1973-1995']['max_share'])} and "
    f"{pc(V['2004-2019']['min_share'])}--{pc(V['2004-2019']['max_share'])}). Without agriculture, exploratory: "
    f"{pc(X1['1973-1995']['composition_share'])} and {pc(X1['2004-2019']['composition_share'])} percent",
    f"A wedge of {f0(W1['wedge_cpi'])} log points over 1973--2024 and {f0(W2['wedge_cpi'])} over 1983--2024; shelter is "
    f"{pc(W1['removed_by_ex_shelter'])} and {pc(W2['removed_by_ex_shelter'])} percent of it",
    f"Across countries $+{f2(pr['beta'])}$ ($p={f2(pr['p'])}$); within countries $-{f2(-pa['beta'])}$ (bootstrap "
    f"$p={pa['p_boot']:.3f}$)",
    f"Output per hour {f2(r5['productivity_2019_2025'])} percent a year against {f2(r5['productivity_2004_2019'])}; "
    f"hours per person falling {f2(-r5['hours_pp_2019_2025'])} percent a year; compression "
    f"{f2(r5['compression_2019_2025'])} percent a year",
    # Section 7
    f"Rent alone would pay for {f2(NUM['rent_cover_base'])} of a basket per person",
]
# inputs and citations that may stand alone in the regions: index bases, the PWT version, ages, the pull date, the
# bootstrap draws, the significance level, Lemma 1's bounds and the elasticity range, the fork and the coverage ratio
# cited from the companion paper
ALLOWED = {"100", "11.0", "16", "9,999", "0.05", "0.4", "1", "0", "4.8", "0.30"}

claimed = np.zeros(len(text), dtype=bool)
for ph in PHRASES:
    ph_n = re.sub(r"\s+", " ", ph)
    hits = [m.start() for m in re.finditer(re.escape(ph_n), text)]
    check(f"Q1 printed: \"{ph_n[:90]}{'…' if len(ph_n) > 90 else ''}\"", bool(hits), f"{len(hits)} hit(s)")
    for h in hits:
        claimed[h:h + len(ph_n)] = True

blank = lambda m: " " * len(m.group())  # noqa: E731
scan = text
for pat in (r"\\(label|ref|eqref|input)\{[^}]*\}", r"\\includegraphics\[[^\]]*\]\{[^}]*\}",
            r"\\begin\{tabular\}\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\}", r"\\renewcommand\{[^}]*\}\{[^}]*\}",
            r"\b(1[89]\d\d|20[0-3]\d)--(\d{2,4})\b", r"Section~\d+", r"15--64", r"JEL codes:[^\\]*", r"HC1"):
    scan = re.sub(pat, blank, scan)
unchecked = []
for m in re.finditer(r"\d{1,3}(?:,\d{3})+(?!\d)|\d+\.\d+|\d+", scan):
    t = m.group()
    if len(t) == 4 and t.isdigit() and 1900 <= int(t) <= 2030:
        continue                                            # a year
    if t in ALLOWED or claimed[m.start():m.end()].all():
        continue
    unchecked.append(f"{t} [{text[max(0, m.start() - 40):m.start()].strip()}]")
check("Q2 no number in the data regions left outside a recomputed phrase or the allowed inputs", not unchecked,
      "; ".join(unchecked[:8]))

# words that carry a quantity
order_pi = sorted(("1973-1995", "1995-2004", "2004-2019", "2019-2025"), key=lambda k: e[k])
order_h = sorted(("1973-1995", "1995-2004", "2004-2019", "2019-2025"), key=lambda k: hp[k])
within_by = F["within_by_sector"]
WORDS = [
    ("about a third of the rise of consumer relative to producer prices that makes up most of the gap",
     all(0.30 <= w["removed_by_ex_shelter"] < 0.40 for w in (W1, W2)) and W1["wedge_share_of_gap"] > 0.5),
    ("account for about a sixth of the slowdown over those years", 0.14 <= r4["envelope_share_trend_mid"] <= 0.20),
    ("Since 1973 the four eras rank in exactly opposite orders by the two measures", order_pi == order_h[::-1]),
    ("with the fastest growth of output per hour and nearly flat hours per person",
     e["1948-1973"] < max(e.values()) and abs(hp["1948-1973"]) < 0.1),
    ("removing energy from the CPI barely changes it, while removing shelter removes a third of it",
     all(abs(w["removed_by_ex_energy"]) < 0.1 and 0.30 <= w["removed_by_ex_shelter"] < 0.40 for w in (W1, W2))),
    ("The measurement supports the prediction, narrowly in the later window",
     1 / 3 <= W2["removed_by_ex_shelter"] < 0.35 and W1["removed_by_ex_shelter"] > W2["removed_by_ex_shelter"]),
    ("shelter is a third of the price wedge", all(0.30 <= w["removed_by_ex_shelter"] < 0.40 for w in (W1, W2))),
    ("Two support the account, one narrowly, and the composition result is partial",
     V["overall"] == "supports" and all(v == "supports" for v in v3.values()) and x1_overall == "partial"),
    ("By the rule fixed beforehand the test is uninformative", hx["decision"] == "uninformative"),
    ("positive, the opposite of the prediction, and far from significant", pr["beta"] > 0 and pr["p"] > 0.2),
    ("never significant", min(hx["loo_beta_range"]) > 0 and hx["loo_p_above_005"] == hx["sample"]),
    ("with manufacturing the largest single piece in both",
     all(min(within_by[k], key=within_by[k].get) == "mfg" for k in ("1973-1995", "2004-2019"))),
    ("all of it in the machine-contestable sectors",
     G["1995-2004"]["by_class"]["within_slowdown"]["M"] >= G["1995-2004"]["within_slowdown"] > 0),
    ("as much as in the slow eras", -G["1995-2004"]["composition"] >= max(-G[k]["composition"]
                                                                         for k in ("1973-1995", "2004-2019"))),
    ("real interest rates that fell for four decades", 35 <= RR["min_year"] - int(rr.index.min()) <= 45),
    ("Colombia, Estonia and Korea lack some years", hx["dropped_incomplete"] == ["COL", "EST", "KOR"]),
    ("the third quarter of 2026", r5["last_quarter"] == "2026-07-01"),
    ("The reading does not change", VI["share_2004_2016_older"]["median"] >= 0.25),
]
for phrase, ok in WORDS:
    check(f"Q3 \"{phrase}\" is printed and holds", phrase in text and ok)

# the data figures
FIGS = ("fig_eras", "fig_industry", "fig_gap", "fig_hours", "fig_hx")
check("Q4 the five data figures exist (PDF and PNG) and are included",
      all((ROOT / "paper" / "figures" / f"{f}.{x}").exists() for f in FIGS for x in ("pdf", "png"))
      and all(f"figures/{f}.pdf" in regions[1] for f in FIGS))
caps = re.findall(r"\\caption\{(.*?)\}\s*\\label\{fig", regions[1], flags=re.S)
check("Q4 their captions end with the AI line", len(caps) == 5 and all(
    c.rstrip().endswith("Drawn by code written with Claude (Anthropic).") for c in caps))

n_fail = sum(1 for _, okk in RESULTS if not okk)
print(f"\n{len(RESULTS) - n_fail}/{len(RESULTS)} checks passed")
sys.exit(1 if n_fail else 0)
