# october.py — the October bust. Her request (2026-09-30): "I do want to consider a bust case in October, i.e. within a
# month, is that possible?" Her case (case.py: the bust 1.5x the dot-com one over two quarters, the premium on borrowing,
# US tariffs, care capping out, European austerity, the pace rising from the bound seen, adoption as a band) run with its
# first falls in 2026Q4, from a start measured to 30 Sep 2026, with the energy term that decision 27 held back.
#
# Decision 27, as amended (2026-10-01, Claude on her delegation): the energy term is switched on in the main case when dated
# Brent is at or above 1.25 times its three-year average on a day a bust rule (bust.us.equity, bust.credit.us or
# crash.joint) is active. Until then it stays off by default: the main case (case.py) and the October central here carry
# none, and the runs with it are scenarios beside the central. Whether the condition is met is read from the runs (section
# 5: the watcher's rules replayed day by day), not assumed. On 1 Oct no bust rule is active, so it is not met. In the
# replay of the October-bust run it is met from 27 Nov 2026 (when the Nasdaq rule and crash.joint fire) to 30 Sep 2027 under
# "stays high" (dated Brent at its late-September level, $117.66), and not if oil collapses; held from 30 Sep, it needs
# $101.12, and is met at the futures strip ($102-107) (section 5, oil_threshold). The first wording, superseded ("add one
# only if the oil rule and a bust fire together"), was a knife-edge on the price: under "stays high" or "held high" the oil
# rule, active since September, goes off on 21 Oct 2026 (its three-month base reaches late July's spike, its six-month
# base April's highs) and fires again on 18 Dec 2026 (its six-month base reaches late June's lows) while the Nasdaq rule
# and crash.joint are active: met, on 20 weekdays (17 Brent prints) to 14 Jan 2027, but only if dated Brent holds at
# $109.65 or more from 30 Sep through late December; at the futures strip ($102-107) the rule goes off on 9-16 Oct and
# does not come back on, so the first wording is not met.
#
# Structure:
#   1. the dating, one       global_crash's index 0 is the state measured on data to September 2026, the end of 2026Q3
#                            (gc.START); the first simulated quarter (index 1, where ai_shock's falls begin) is 2026Q4,
#                            and 2028Q4 is index 9 (decision 43, adopted 2026-10-01; from log 28 to then the labels ran
#                            one quarter late). Her case is read from case.json, on the same dating and horizon: 25
#                            quarters (case.N), so that 2032Q3 (index 24) exists (extending the horizon changes nothing
#                            before it: check O2).
#   2. the energy term       measured: headline minus core inflation, quarterly (annualised log changes), on crude's change
#                            times energy's share of spending, this quarter and last (Newey-West errors; US PCE 1990-2026,
#                            the euro area's and Sweden's HICP 2000-2026 with quarter dummies, Brent in each currency; the
#                            US also on WTI, its own crude); a cross-check on consumer energy prices themselves. The energy
#                            bill as a tax on consumers' other spending: approximate (spending falls 0.8 of the bill; in the
#                            US half of that is spent back by domestic producers, a net petroleum exporter; the euro area
#                            and Sweden import). China: no energy term (regulated fuel prices; no measure in these sources).
#                            Oil paths (quarterly averages; the euro area and Sweden in their own currencies, exchange rates
#                            held at their last value):
#                              "stays high"  dated Brent held at its late-September level (the last five EIA prints) for
#                                            four quarters, above the futures strip, then its three-year average (the
#                                            watcher's reference) after a quarter at the geometric midpoint;
#                              "held high"   the late-September level throughout (a sensitivity);
#                              "US on WTI"   as "stays high", with the US's energy term on WTI (its level, its three-year
#                                            average, its own pass-through): dated Brent sits $17-31 over WTI in late
#                                            September against a 2015-25 median of about $4;
#                              "collapses"   2008's quarterly path after 2008Q3 (2008Q4-2010Q3 over 2008Q3), in each
#                                            currency's own 2008 prices, applied to 2026Q3's average (the alignment);
#                                            variants anchored on the late-September spot (2008's quarters over the last
#                                            five prints of September 2008, applied to the last five of September 2026)
#                                            and with the dollar's ratios in every currency (as first built).
#                            Policy: "looking through" reacts to core on the last quarter's reading (annualised: the
#                            model's rule as fitted), with four quarters' core a matched variant; "hands tied" reacts to
#                            headline on the average of the last four quarters (y/y-like: the main reading, decision 48
#                            as decided 2026-10-01), the last quarter's (annualised) a sensitivity.
#   3. the start             measured to 30 Sep 2026 for these runs only (regions_today() and the stored runs untouched):
#                            the model's pi is core inflation (regions_today reads core PCE; the 2007-10 fit targets core
#                            PCE), so every region starts on core, with headline beside it for the energy term (Sweden's:
#                            core plus the energy term at the start; CPIF, the Riksbank's target, is lowered by the food VAT
#                            cut and is run as a variant). The spread already present is a treatment, not data: the
#                            central carries the corporate spread's rise over the last three months alone (decision 47 as
#                            decided 2026-10-01); the ten-year term premium's rise, routed through the private
#                            credit-spread channel as well, is a named sensitivity, since it would double count the
#                            case's premium, which decision 23 and case.py size as "another move the size of the ten-year
#                            term premium's rise since 2019" (decision 25 says the case carries it). Both are split out
#                            in the attribution.
#   4. the runs              each at both ends of the adoption band; attribution by differences of the unrounded runs
#                            (rounded once, to 0.01).
#   5. what would show it    the path against the watcher's rules (watch/watch/tripwires.py, read-only): month by month
#                            (Nasdaq drawdown, high-yield spreads, financial stress, the Sahm rule (US, Sweden), claims,
#                            crash.joint; banks' loans to non-banks is not in the model), and day by day for the oil rule
#                            (tripwires.Board's fire / stay active / clear / armed logic, ported; check W1 runs the
#                            watcher's own code against it) and the bust rules it would coincide with. The oil rule joined
#                            the watcher on 25 Sep (STATE decision 27: "the watcher's wider rules, 2026-09-25") and fired on
#                            its first run; the replay's earlier fires (14 and 24 Sep) are what it would have done, and
#                            entering with no memory on any print from 22 Sep to the last changes no later date. The
#                            thresholds: the level, held from 30 Sep, at which each wording is still met (a grid to $0.10,
#                            then to the cent). Mappings measured on FRED (the ICE series there cover only the last three
#                            years; stated). The Swedish Sahm reading's daily date is approximate (the first Friday of the
#                            next month stands in for Statistics Sweden's calendar; for December's data that is 1 Jan).
#
# Provenance (public; cached under cache/october/, a vintage of 30 Sep 2026 apart from the stored runs' cache; DFF, BAA10Y,
# NASDAQCOM and STLFSI4 refreshed on 1 Oct, one print more each):
#   FRED: EIA Brent and WTI (DCOILBRENTEU, DCOILWTICO); BEA PCE prices (PCEPI, PCEPILFE), energy goods and services
#   (DNRGRC1M027SBEA, DNRGRG3M086SBEA), PCE, GDP, and the build-out series (decoupling.build_out); the Fed (DFF, DFEDTARU,
#   H.10 DEXUSEU and DEXSDUS, H.8 LNFACBW027SBOG, Kim-Wright THREEFYTP10); BLS via FRED (UNRATE), DOL claims (ICSA); ICE
#   BofA option-adjusted spreads (BAMLH0A0HYM2, BAMLC0A0CM, BAMLHE00EHYIOAS); Moody's (BAA10Y); Nasdaq (NASDAQCOM); St Louis
#   Fed (STLFSI4); the ECB deposit rate (ECBDFR); Eurostat HICP via FRED (CP0000EZ19M086NEST, 00XEFDEZ19M086NEST,
#   ENRGY0EZ19M086NEST, CP0000SEM086NEST, 00XEFDSEM086NEST, ENRGY0SEM086NEST). ECB Data Portal: HICP energy weights
#   (ICP.A.U2.N.NRGY00.4.INW, ICP.A.SE.N.NRGY00.4.INW) and euro-area unemployment (LFSI.M.I9.S.UNEHRT.TOTAL0.15_74.T, the
#   euro area as it is now: 21 countries from 2026). Eurostat: une_rt_m for EA21, the cross-check (EA20 queries now return
#   nothing). Statistics Sweden: CPIF (PR0101G/KPIF2020), the labour force survey (AM0401A/AKURLBefM).
#   Approximate, stated: consumption's share of GDP in the euro area (0.52) and Sweden (0.45); the spending lost per unit of
#   energy bill (0.8) and the US producers' offset (0.5). Stored, stated: Sweden's policy rate, China.
#
# Run from paths/:  ../venv/Scripts/python.exe code/october.py
# Out: results/october.json, figures/fig_october.png

from __future__ import annotations

import json
import os
import statistics
import sys
import time
from contextlib import contextmanager
from dataclasses import replace

import numpy as np
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import global_crash as gc  # noqa: E402
import case  # noqa: E402
import decoupling  # noqa: E402
import lambda_compute2 as _lc  # noqa: E402  (on the path through global_crash)

CACHE = os.path.join(ROOT, "cache", "october")
UA = {"User-Agent": "laborformal-paths (public-data research)"}
N = case.N                           # 2026Q3 (index 0, the start) .. 2032Q3 (index 24): the case's horizon
Q27, Q28, Q32Q2, Q32 = 4, case.END_2028, 23, 24   # 2027Q3, 2028Q4, 2032Q2 and 2032Q3 (gc.quarter_label)
REPORT = list(range(1, Q28 + 1)) + [Q32Q2, Q32]
CAP = case.CAP                       # the model's ceiling on non-employment (u + out), %
E2 = ("low", "high")                 # the ends of the adoption band
MPC_BILL = 0.8                       # spending lost per unit of a higher energy bill (approximate)
US_OFFSET = 0.5                      # the share of that the US spends back through its own producers (approximate)
CONSUMPTION = {"EA": 0.52, "SE": 0.45}   # household consumption, share of GDP (approximate)
ENERGY_REGIONS = ("US", "EA", "SE")


def label(k: int) -> str:
    return gc.quarter_label(k)


# ------------------------------------------------------------------ data
def _https():
    import truststore
    truststore.inject_into_ssl()


@contextmanager
def vintage():
    """The October vintage for the reads inside (FRED through lambda_compute2, decoupling.build_out), and the stored
    runs' cache back afterwards: importing or running october leaves lambda_compute2 reading where the stored runs do."""
    saved = _lc.CACHE
    _lc.CACHE = CACHE
    try:
        yield
    finally:
        _lc.CACHE = saved


def fred(sid: str) -> pd.Series:
    with vintage():
        if not os.path.exists(os.path.join(CACHE, f"{sid}.csv")):
            _https()
        s = _lc.pull_fred(sid)
    if s is None:
        raise SystemExit(f"FRED {sid}: not available")
    return s


def build_out() -> dict:
    with vintage():
        return decoupling.build_out()


def ecb(key: str, monthly: bool = False) -> pd.Series:
    """An ECB Data Portal series (annual, or monthly), cached as its CSV."""
    fp = os.path.join(CACHE, "ecb_" + key.replace("/", "_") + ".csv")
    if not os.path.exists(fp):
        _https()
        import requests
        r = requests.get(f"https://data-api.ecb.europa.eu/service/data/{key}?format=csvdata", headers=UA, timeout=60)
        r.raise_for_status()
        open(fp, "w", encoding="utf-8").write(r.text)
    df = pd.read_csv(fp)
    idx = pd.PeriodIndex(df["TIME_PERIOD"].astype(str), freq="M") if monthly else df["TIME_PERIOD"].astype(int)
    return pd.Series(df["OBS_VALUE"].values, index=idx).sort_index()


def eurostat_unemployment(geo: str) -> pd.Series:
    """Eurostat une_rt_m (seasonally adjusted, 15-74, % of the labour force), monthly, cached as JSON; empty if the
    geography returns nothing."""
    fp = os.path.join(CACHE, f"eurostat_une_rt_m_{geo}.json")
    if not os.path.exists(fp):
        _https()
        import requests
        r = requests.get("https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/une_rt_m"
                         f"?geo={geo}&s_adj=SA&age=TOTAL&sex=T&unit=PC_ACT&sinceTimePeriod=2025-01", headers=UA, timeout=60)
        r.raise_for_status()
        json.dump(r.json(), open(fp, "w", encoding="utf-8"))
    js = json.load(open(fp, encoding="utf-8"))
    if not js.get("value"):
        return pd.Series(dtype=float)
    inv = {v: k for k, v in js["dimension"]["time"]["category"]["index"].items()}
    return pd.Series({pd.Period(inv[int(k)], "M"): float(v) for k, v in js["value"].items()}).sort_index()


def scb(table: str, query: dict, name: str) -> pd.Series:
    """A Statistics Sweden monthly series, cached as JSON."""
    fp = os.path.join(CACHE, f"scb_{name}.json")
    if not os.path.exists(fp):
        _https()
        import requests
        body = {"query": [{"code": k, "selection": {"filter": "item", "values": v if isinstance(v, list) else [v]}}
                          for k, v in query.items()], "response": {"format": "json"}}
        for wait in (0, 5, 20):
            time.sleep(wait)
            r = requests.post("https://api.scb.se/OV0104/v1/doris/en/ssd/" + table, json=body, headers=UA, timeout=120)
            if r.status_code == 200:
                break
        r.raise_for_status()
        json.dump(r.json(), open(fp, "w", encoding="utf-8"))
    js = json.load(open(fp, encoding="utf-8"))
    s = {pd.Period(d["key"][-1].replace("M", "-"), "M"): float(d["values"][0]) for d in js["data"] if d["values"][0] not in ("..", "")}
    return pd.Series(s).sort_index()


def aku() -> pd.Series:
    return scb("AM/AM0401/AM0401A/AKURLBefM", {"Arbetskraftstillh": "ALÖSP", "TypData": "SR_DATA", "Kon": "1+2",
                                               "Alder": "tot15-74", "ContentsCode": "000007L9"}, "aku_unemployment_sa")


def quarterly(s: pd.Series) -> pd.Series:
    return s.groupby(s.index.to_period("Q")).mean()


def ann(s: pd.Series) -> pd.Series:
    return 400 * np.log(s / s.shift(1))


def yoy(s: pd.Series) -> float:
    return float((s.iloc[-1] / s.iloc[-13] - 1) * 100)


def ols_hac(y: np.ndarray, X: np.ndarray, lags: int) -> tuple:
    """Least squares with Newey-West (Bartlett) errors; R-squared."""
    XtX = np.linalg.inv(X.T @ X)
    b = XtX @ X.T @ y
    u = y - X @ b
    Xu = X * u[:, None]
    S = Xu.T @ Xu
    for lag in range(1, lags + 1):
        G = Xu[lag:].T @ Xu[:-lag]
        S += (1 - lag / (lags + 1)) * (G + G.T)
    return b, np.sqrt(np.diag(XtX @ S @ XtX)), float(1 - u @ u / ((y - y.mean()) @ (y - y.mean())))


def oow(o: dict, r: str = "US") -> np.ndarray:
    return o[r]["u"] + o[r]["out"]


# ------------------------------------------------------------------ 1. the dating, and her case on it
DATING_NOTE = ("One dating (decision 43, adopted 2026-10-01): global_crash's index 0 is the state measured on data to September "
               "2026 (unemployment in August, inflation to August, the policy rate at end-September, the gap at zero): the end "
               "of 2026Q3, gc.START. Each index after it is one simulated quarter, and ai_shock's falls begin at index 1 "
               "(delay 0), so the bust's first falls are in 2026Q4 and 2028Q4 is index 9. Until 2026-10-01 the labels ran one "
               "quarter late, since log 28: case.py's END_2028 = 8 and its header's 'quarter 1 = 2026Q4' (counted from 1) were "
               "in place at log 28's commit, and log 29's START = 2026Q4 at index 0 kept them. So her case was already an "
               "October bust; case.py, case.json and STATE now carry the measured labels (the values quoted before are in "
               "STATE's log). On it her case's pace is half-way in 2028Q2, its tariffs arrive in 2027Q1, its premium builds "
               "over 2026Q4-2027Q3, and robotics begins in 2028Q4 and is complete by 2029Q3.")


def her_case(C: dict, st: dict) -> dict:
    """Her case as stored (case.json, on the one dating): US out of work at 2028Q4 (index 9), 2032Q2 and 2032Q3 against the
    model's central run, output, what each piece adds (case.py's piece-by-piece runs), and when each piece arrives."""
    ref = C["paths"]["reference"]["US"]["out_of_work"]
    res = {"note": DATING_NOTE, "labels": {str(k): label(k) for k in (0, 1, 2, 7, 8, 9, 23, 24)}}
    for end in E2:
        p = C["paths"][end]
        q = p["US"]["out_of_work"]
        res[end] = {"us_out_of_work": {"2028Q4": q[Q28], "2032Q2": q[Q32Q2], "2032Q3": q[Q32]},
                    "us_output_2028Q4": p["US"]["output"][Q28], "four_output_2028Q4": p["four_output"][Q28],
                    "four_output_worst": {"value": min(p["four_output"]), "quarter": label(int(np.argmin(p["four_output"])))},
                    "ratio_to_central_2028Q4": round(q[Q28] / ref[Q28], 3),
                    "2032Q3_below_the_cap_by": round(CAP - q[Q32], 2)}
    res["central_run_us_out_of_work"] = {"2028Q4": ref[Q28], "2032Q2": ref[Q32Q2], "2032Q3": ref[Q32]}
    res["piece_by_piece_us_out_of_work"] = {
        d: {"adds_2028Q4": v["adds_to_us_out_of_work_end_2028"], "adds_2032Q2": v["adds_to_us_out_of_work_2032Q2"],
            "adds_by_2032Q3": v["adds_to_us_out_of_work"], "without_it_at_the_cap_from": v["us_at_the_models_cap_from"]}
        for d, v in C["piece_by_piece"].items() if d != "note"}
    w = gc.Waves(split=True, robot_lag=st["robot_lag_years"], absorb=True)
    rob = [gc.robots(k, w) for k in range(N)]
    res["dates"] = {"bust_first_falls": label(1), "tariffs": label(st["tariff_quarter"]),
                    "premium_builds": f"{label(1)}-{label(st['premium_quarters'])}",
                    "pace_half_way": label(st["pace"]["mid_quarter"]),
                    "robotics_begins": label(next(k for k in range(N) if rob[k] > 0)),
                    "robotics_complete": label(next(k for k in range(N) if rob[k] >= 1.0))}
    return res


# ------------------------------------------------------------------ 2. the energy term
PT = {"US": {"head": "PCEPI", "core": "PCEPILFE", "energy": "DNRGRG3M086SBEA", "window": ("1990Q1", "2026Q2"), "dummies": False},
      "EA": {"head": "CP0000EZ19M086NEST", "core": "00XEFDEZ19M086NEST", "energy": "ENRGY0EZ19M086NEST", "fx": "DEXUSEU",
             "weights": "ICP/A.U2.N.NRGY00.4.INW", "window": ("2000Q1", "2026Q2"), "dummies": True},
      "SE": {"head": "CP0000SEM086NEST", "core": "00XEFDSEM086NEST", "energy": "ENRGY0SEM086NEST", "fx": "DEXSDUS",
             "weights": "ICP/A.SE.N.NRGY00.4.INW", "window": ("2000Q1", "2026Q2"), "dummies": True}}
CRUDE = {"brent": "DCOILBRENTEU", "wti": "DCOILWTICO"}


def brent_in(r: str, crude: str = "brent") -> pd.Series:
    """Crude, daily, in region r's currency (EIA spot in dollars; the Fed's H.10 rates)."""
    b = fred(CRUDE[crude])
    if r == "US":
        return b
    fx = fred(PT[r]["fx"]).reindex(b.index).ffill()
    return (b / fx if r == "EA" else b * fx).dropna()


def energy_share(r: str) -> pd.Series:
    """Energy's share of consumer spending by quarter: US PCE (monthly, nominal); the euro area's and Sweden's HICP item
    weights (annual, per mille), each quarter taking its year's weight."""
    if r == "US":
        return quarterly(fred("DNRGRC1M027SBEA") / fred("PCE"))
    wy = ecb(PT[r]["weights"]) / 1000
    idx = pd.period_range(f"{wy.index.min()}Q1", "2026Q4", freq="Q")
    return pd.Series([float(wy.get(p.year, wy.iloc[-1])) for p in idx], index=idx)


def pt_data(r: str, crude: str = "brent") -> pd.DataFrame:
    """The regression's data: y = headline minus core inflation (points a year), g = crude's change (annualised log %),
    wl = energy's share the quarter before, x = wl g and its lag; en = consumer energy prices' own inflation."""
    s = PT[r]
    oil = quarterly(brent_in(r, crude))
    d = pd.DataFrame({"y": ann(quarterly(fred(s["head"]))) - ann(quarterly(fred(s["core"]))), "oil": oil, "g": ann(oil),
                      "w": energy_share(r), "en": ann(quarterly(fred(s["energy"])))})
    d["oil_before"] = d["oil"].shift(1)
    d["wl"] = d["w"].shift(1)
    d["x"] = d["wl"] * d["g"]
    d["xl"] = d["x"].shift(1)
    d["gl"] = d["g"].shift(1)
    for q in (1, 2, 3):
        d[f"q{q}"] = (d.index.quarter == q).astype(float)
    return d.loc[s["window"][0]:s["window"][1]].dropna(subset=["y", "x", "xl", "en", "gl"])


def pt_fit(r: str, crude: str = "brent") -> dict:
    d = pt_data(r, crude)
    dum = ["q1", "q2", "q3"] if PT[r]["dummies"] else []
    X = np.column_stack([np.ones(len(d))] + [d[c] for c in dum] + [d["x"], d["xl"]])
    b, se, r2 = ols_hac(d["y"].values, X, 4)
    Xe = np.column_stack([np.ones(len(d))] + [d[c] for c in dum] + [d["g"], d["gl"]])
    be, see, r2e = ols_hac(d["en"].values, Xe, 4)
    k = len(dum)
    return {"crude": crude, "window": f"{d.index[0]}-{d.index[-1]}", "n": len(d), "quarter_dummies": bool(dum),
            "b0": float(b[k + 1]), "b1": float(b[k + 2]), "se_b0": float(se[k + 1]), "se_b1": float(se[k + 2]),
            "constant": float(b[0]), "dummies": [float(v) for v in b[1:k + 1]], "r2": r2,
            "cross_check_consumer_energy_on_crude": {"c0": float(be[k + 1]), "c1": float(be[k + 2]), "se_c0": float(see[k + 1]),
                                                     "se_c1": float(see[k + 2]), "r2": r2e},
            "energy_share_latest": float(energy_share(r).loc[:"2026Q3"].iloc[-1])}


OIL_LABELS = {
    "high": "stays high: dated Brent held at its late-September level for four quarters, above the futures strip, then its "
            "three-year average",
    "held": "held high: dated Brent at its late-September level throughout",
    "high_wti": "stays high, the US on WTI: as 'stays high', with the US's energy term on WTI (its late-September level for "
                "four quarters, then its own three-year average)",
    "collapse": "collapses as in 2008, anchored on 2026Q3's average: each currency's own 2008Q4-2010Q3 quarterly averages over "
                "its 2008Q3 average, times 2026Q3's",
    "collapse_spot": "collapses as in 2008, anchored on the late-September spot: each currency's own 2008Q4-2010Q3 quarterly "
                     "averages over the last five prints of September 2008, times the last five of September 2026",
    "collapse_usd": "collapses as in 2008, the dollar's ratios over 2008Q3 in every currency, anchored on 2026Q3's average (as "
                    "first built)",
}


def oil_paths(n: int = N) -> dict:
    """Crude by quarter (averages), index 0 = 2026Q3, in each region's currency, with the quarter before (2026Q2)."""
    b, wti = fred("DCOILBRENTEU"), fred("DCOILWTICO")
    q = quarterly(b)
    end_sep, trend = float(b.iloc[-5:].mean()), float(b.iloc[-757:-1].mean())     # the last five prints; three years, as
    w_end, w_trend = float(wti.iloc[-5:].mean()), float(wti.iloc[-757:-1].mean())  # the watcher's oil rule reads them
    mid = lambda a, c: float(np.exp(0.5 * (np.log(a) + np.log(c))))  # noqa: E731
    high = np.array([end_sep] * 4 + [mid(end_sep, trend)] + [trend] * (n - 6))
    high_w = np.array([w_end] * 4 + [mid(w_end, w_trend)] + [w_trend] * (n - 6))
    fx_last = {"US": 1.0, "EA": 1 / float(fred("DEXUSEU").iloc[-1]), "SE": float(fred("DEXSDUS").iloc[-1])}
    q08 = pd.Period("2008Q3", "Q")
    ratios_usd = [float(q[q08 + j] / q[q08]) for j in range(1, 9)]
    out = {"usd": {"2026Q2": float(q["2026Q2"]), "2026Q3": float(q["2026Q3"]), "end_september_last5": end_sep,
                   "three_year_average": trend, "last": float(b.iloc[-1]), "last_date": str(b.index[-1].date()),
                   "september_average": float(b.loc["2026-09"].mean()),
                   "wti": {"2026Q2": float(quarterly(wti)["2026Q2"]), "2026Q3": float(quarterly(wti)["2026Q3"]),
                           "end_september_last5": w_end, "three_year_average": w_trend, "last": float(wti.iloc[-1])},
                   "brent_over_wti_september": float((b - wti).dropna().loc["2026-09"].mean()),
                   "brent_over_wti_last5": [round(float(x), 2) for x in (b - wti).dropna().iloc[-5:]],
                   "brent_over_wti_median_2015_25": float((b - wti).dropna().loc["2015":"2025"].median()),
                   "analogue_2008": {str(q08 + j): round(float(q[q08 + j]), 2) for j in range(0, 9)},
                   "analogue_ratios_over_2008Q3": [round(x, 4) for x in ratios_usd]},
           "labels": OIL_LABELS, "alignment": {},
           "paths": {k: {} for k in ("high", "held", "high_wti", "collapse", "collapse_spot", "collapse_usd", "flat")}}
    for r in ENERGY_REGIONS:
        own = brent_in(r)
        qr = quarterly(own)
        before, p0 = float(qr["2026Q2"]), float(qr["2026Q3"])
        spot = end_sep * fx_last[r]
        spot08 = float(own.loc[:"2008-09-30"].iloc[-5:].mean())
        r_q3 = [float(qr[q08 + j] / qr[q08]) for j in range(1, 9)]
        r_spot = [float(qr[q08 + j] / spot08) for j in range(1, 9)]
        hold = lambda x: np.array(x + [x[-1]] * (n - 1 - len(x)))  # noqa: E731
        out["paths"]["high"][r] = (before, np.concatenate([[p0], high * fx_last[r]]))
        out["paths"]["held"][r] = (before, np.concatenate([[p0], np.full(n - 1, spot)]))
        out["paths"]["high_wti"][r] = out["paths"]["high"][r]
        out["paths"]["collapse"][r] = (before, np.concatenate([[p0], hold([p0 * x for x in r_q3])]))
        out["paths"]["collapse_spot"][r] = (before, np.concatenate([[p0], hold([spot * x for x in r_spot])]))
        out["paths"]["collapse_usd"][r] = (before, np.concatenate([[p0], hold([p0 * x for x in ratios_usd])]))
        out["paths"]["flat"][r] = (p0, np.full(n, p0))           # no change into or after the start: the term is zero
        out["alignment"][r] = {"ratios_over_2008Q3": [round(x, 4) for x in r_q3], "ratios_over_late_september_2008": [round(x, 4) for x in r_spot],
                               "2008Q3_over_late_september_2008": round(float(qr[q08] / spot08), 4),
                               "2026Q3_over_late_september_2026": round(p0 / spot, 4),
                               "first_quarter_over_late_september_2026": {"collapse": round(p0 * r_q3[0] / spot, 4),
                                                                           "collapse_spot": round(r_spot[0], 4),
                                                                           "2008's own (2008Q4 over late September 2008)": round(r_spot[0], 4)}}
    wq = quarterly(wti)
    out["paths"]["high_wti"]["US"] = (float(wq["2026Q2"]), np.concatenate([[float(wq["2026Q3"])], high_w]))
    for k in ("high", "held", "high_wti", "collapse", "collapse_spot", "collapse_usd"):
        out["usd"][f"{k}_path"] = [round(float(x), 2) for x in out["paths"][k]["US"][1][:12]]
    return out


# ------------------------------------------------------------------ 3. the start, measured to 30 Sep 2026
def spreads_present() -> dict:
    """The last three months' rise (63 observations, the watcher's window) in the ten-year term premium and the broad
    corporate spread (ICE BofA US corporate OAS): the moves the model's one-quarter lag passes to spending in 2026Q4."""
    tp, ig, hy, baa = fred("THREEFYTP10"), fred("BAMLC0A0CM"), fred("BAMLH0A0HYM2"), fred("BAA10Y")
    d = lambda s: float(s.iloc[-1] - s.iloc[-64])  # noqa: E731
    since = lambda s: float(s.iloc[-1] - s.loc[:"2026-08-28"].iloc[-1])  # noqa: E731
    return {"term_premium": float(tp.iloc[-1]), "term_premium_date": str(tp.index[-1].date()), "term_premium_3m": d(tp),
            "ig_oas": float(ig.iloc[-1]), "ig_oas_3m": d(ig), "hy_oas": float(hy.iloc[-1]), "hy_oas_3m": d(hy),
            "hy_oas_since_28_aug": since(hy), "baa_10y": float(baa.iloc[-1]), "baa_10y_date": str(baa.index[-1].date()),
            "baa_10y_3m": d(baa), "us_spread0_central": d(ig), "us_spread0_with_the_term_premium": d(tp) + d(ig)}


def start(regs: dict) -> tuple:
    """Fresh regions for the October runs (and the WTI and CPIF variants), the spreads at the start, the fits, and the
    table of what changed and from where."""
    pt = {r: pt_fit(r) for r in ENERGY_REGIONS}
    pt["US_wti"] = pt_fit("US", "wti")
    core_us, head_us = fred("PCEPILFE"), fred("PCEPI")
    bo = build_out()
    gdp, pce = fred("GDP"), quarterly(fred("PCE"))
    cy_us = float(pce[gdp.index[-1].to_period("Q")] / gdp.iloc[-1])
    ea_core, ea_head = fred("00XEFDEZ19M086NEST"), fred("CP0000EZ19M086NEST")
    se_core = fred("00XEFDSEM086NEST")
    cpif = scb("PR/PR0101/PR0101G/KPIF2020", {"ContentsCode": "000007ZM"}, "cpif_annual")
    se_u = aku()
    ea_u = ecb("LFSI/M.I9.S.UNEHRT.TOTAL0.15_74.T", monthly=True)
    ea_u_es = eurostat_unemployment("EA21")
    ea20 = eurostat_unemployment("EA20")
    sq = quarterly(brent_in("SE"))
    se_e0 = float(gc.energy_inflation([float(sq["2026Q3"])], float(sq["2026Q2"]), pt["SE"]["energy_share_latest"],
                                      (pt["SE"]["b0"], pt["SE"]["b1"]))[0])
    sp = spreads_present()
    tab = {"US": {"pi0 (core PCE, y/y)": (regs["US"].pi0, yoy(core_us), f"FRED PCEPILFE {core_us.index[-1]:%Y-%m}"),
                  "headline at the start (PCE, y/y)": (None, yoy(head_us), f"FRED PCEPI {head_us.index[-1]:%Y-%m}"),
                  "i0 (effective funds rate)": (regs["US"].i0, float(fred("DFF").iloc[-1]),
                                                f"FRED DFF {fred('DFF').index[-1]:%Y-%m-%d} (target 3.75-{fred('DFEDTARU').iloc[-1]:.2f})"),
                  "u0": (regs["US"].u0, float(fred("UNRATE").iloc[-1]), f"FRED UNRATE {fred('UNRATE').index[-1]:%Y-%m}"),
                  "ai_capex (build-out net of computer imports above its 2015-22 trend)":
                      (regs["US"].ai_capex, bo["net_above_2015_22_trend_pts"], f"decoupling.build_out on the October vintage ({bo['latest']})"),
                  "spread already present (the corporate OAS's 3-month rise; a treatment)": (0.0, sp["us_spread0_central"], "FRED BAMLC0A0CM"),
                  "the term premium's 3-month rise (added in the sensitivity only)": (0.0, sp["term_premium_3m"], "FRED THREEFYTP10"),
                  "energy share of spending": (None, pt["US"]["energy_share_latest"], "FRED DNRGRC1M027SBEA / PCE, 2026Q3"),
                  "consumption share of GDP": (None, cy_us, "FRED PCE / GDP, latest quarter")},
           "EA": {"pi0 (HICP excl. energy, food, alcohol, tobacco, y/y)": (regs["EA"].pi0, yoy(ea_core), f"FRED 00XEFDEZ19M086NEST {ea_core.index[-1]:%Y-%m}"),
                  "headline at the start (HICP, y/y)": (None, yoy(ea_head), f"FRED CP0000EZ19M086NEST {ea_head.index[-1]:%Y-%m}"),
                  "i0 (deposit rate)": (regs["EA"].i0, float(fred("ECBDFR").iloc[-1]), f"FRED ECBDFR {fred('ECBDFR').index[-1]:%Y-%m-%d}"),
                  "u0 (15-74, seasonally adjusted, the euro area of 21)": (regs["EA"].u0, float(ea_u.iloc[-1]),
                      f"ECB LFSI M.I9 {ea_u.index[-1]}; Eurostat une_rt_m EA21 {ea_u_es.index[-1] if len(ea_u_es) else 'n/a'}: "
                      f"{float(ea_u_es.iloc[-1]) if len(ea_u_es) else 'n/a'} (EA20 queries now return {len(ea20)} observations)"),
                  "energy share of spending": (None, pt["EA"]["energy_share_latest"], "ECB HICP energy weight, 2025"),
                  "consumption share of GDP": (None, CONSUMPTION["EA"], "approximate")},
           "SE": {"pi0 (HICP excl. energy, food, alcohol, tobacco, y/y)": (regs["SE"].pi0, yoy(se_core), f"FRED 00XEFDSEM086NEST {se_core.index[-1]:%Y-%m}"),
                  "headline at the start (core + the energy term at the start)": (None, yoy(se_core) + se_e0,
                      f"core plus the energy term into 2026Q3 ({se_e0:+.3f}: Brent in kronor fell from 2026Q2's average)"),
                  "headline at the start, variant (CPIF, y/y, the Riksbank's target; lowered by the food VAT cut)": (None, float(cpif.iloc[-1]), f"SCB KPIF2020 {cpif.index[-1]}"),
                  "i0 (policy rate)": (regs["SE"].i0, regs["SE"].i0, "stored; unchanged since (the Riksbank's minutes of 30 Sep lean to a November hike)"),
                  "u0 (LFS 15-74, seasonally adjusted)": (regs["SE"].u0, float(se_u.iloc[-1]), f"SCB AKURLBefM {se_u.index[-1]}"),
                  "energy share of spending": (None, pt["SE"]["energy_share_latest"], "ECB HICP energy weight, 2025"),
                  "consumption share of GDP": (None, CONSUMPTION["SE"], "approximate")},
           "CN": {"all": (None, None, "stored: China's CPI on FRED ends 2025-04 (the stored pi0 is that reading, headline); no energy term")}}
    us = replace(regs["US"], pi0=yoy(core_us), u0=float(fred("UNRATE").iloc[-1]), i0=float(fred("DFF").iloc[-1]),
                 ai_capex=max(bo["net_above_2015_22_trend_pts"], 0.0), pi_h0=yoy(head_us),
                 energy_weight=pt["US"]["energy_share_latest"], energy_pass=(pt["US"]["b0"], pt["US"]["b1"]),
                 consumption_share=cy_us, energy_income=MPC_BILL * (1 - US_OFFSET))
    ea = replace(regs["EA"], pi0=yoy(ea_core), u0=float(ea_u.iloc[-1]), i0=float(fred("ECBDFR").iloc[-1]), pi_h0=yoy(ea_head),
                 energy_weight=pt["EA"]["energy_share_latest"], energy_pass=(pt["EA"]["b0"], pt["EA"]["b1"]),
                 consumption_share=CONSUMPTION["EA"], energy_income=MPC_BILL)
    se = replace(regs["SE"], pi0=yoy(se_core), u0=float(se_u.iloc[-1]), pi_h0=yoy(se_core) + se_e0,
                 energy_weight=pt["SE"]["energy_share_latest"], energy_pass=(pt["SE"]["b0"], pt["SE"]["b1"]),
                 consumption_share=CONSUMPTION["SE"], energy_income=MPC_BILL)
    fresh = {"US": us, "EA": ea, "SE": se, "CN": regs["CN"]}
    sets = {"stored": regs, "fresh": fresh,
            "wti": {**fresh, "US": replace(us, energy_weight=pt["US_wti"]["energy_share_latest"],
                                           energy_pass=(pt["US_wti"]["b0"], pt["US_wti"]["b1"]))},
            "cpif": {**fresh, "SE": replace(se, pi_h0=float(cpif.iloc[-1]))}}
    spreads = {"corporate": {"US": sp["us_spread0_central"]}, "term_premium": {"US": sp["term_premium_3m"]},
               "both": {"US": sp["us_spread0_with_the_term_premium"]}}
    table = {r: {k: {"stored": None if v[0] is None else round(float(v[0]), 3), "october": None if v[1] is None else round(float(v[1]), 3),
                     "source": v[2]} for k, v in t.items()} for r, t in tab.items()}
    return sets, spreads, pt, sp, table


# ------------------------------------------------------------------ 4. the runs
def build(cm, regs: dict, st: dict, *, n: int = N, delay: int = 0, bust: dict | None = None, adoption: str = "high",
          oil: dict | None = None, react: str = "core", expect: str = "core", spread0: dict | None = None):
    """Her case (case.build's settings) with the October options: the horizon, the bust's delay and size, the oil path
    (None: no energy term), what policy reacts to and expectations adapt to, a spread already present at the start."""
    b = bust or st["bust"]
    shock = gc.ai_shock(n, b["scale"], b["speed"], delay)
    pace = st["pace"]
    shock.drift = {r: case.logistic_pace(regs[r].drift, pace["seen"], pace["mid_quarter"], pace["width_quarters"], n) for r in gc.R}
    shock.spread = {r: case.ramp_to(v, st["premium_quarters"], n) for r, v in st["premium"].items() if v}
    for r, v in (spread0 or {}).items():                    # present from the start and held
        shock.spread[r] = shock.spread.get(r, np.zeros(n)) + v
        shock.spread0[r] = v
    for r, (before, path) in (oil or {}).items():
        shock.oil[r], shock.oil_before[r] = np.asarray(path, float)[:n], before
    rg = {r: replace(g, eta=g.eta * st["adoption_multiple"][adoption]) for r, g in regs.items()}
    rules = {r: replace(gc.MODERN, tariff=st["tariff"][r], tariff_q=st["tariff_quarter"], fiscal=st["fiscal"][r],
                        care_cap=st["care_cap"][r], react_to=react, expect_from=expect) for r in gc.R}
    waves = gc.Waves(split=True, robot_lag=st["robot_lag_years"], absorb=True)
    return rg, gc.simulate(rg, rules, shock, cm, n, waves=waves), shock


def four(rg: dict, o: dict) -> np.ndarray:
    size = {r: rg[r].size for r in gc.R}
    return sum(size[r] * o[r]["y"] for r in gc.R) / sum(size.values())


def fed_cuts(i: np.ndarray) -> dict:
    """When the policy rate first falls, from what peak, how far it goes (to 2032Q3), and whether it rises again (by more
    than half a basis point) before its low, and above the earlier peak."""
    first = next((k for k in range(1, len(i)) if i[k] < i[k - 1] - 1e-9), None)
    if first is None:
        return {"first_cut": None}
    peak = float(i[:first].max())
    low = int(np.argmin(i[first:])) + first
    again = next((k for k in range(first + 1, low + 1) if i[k] > i[k - 1] + 0.005), None)   # by more than half a basis point
    return {"first_cut": label(first), "peak_before": round(peak, 2), "peak_quarter": label(int(np.argmax(i[:first]))),
            "low": round(float(i[low]), 2), "low_quarter": label(low), "cut_points": round(peak - float(i[low]), 2),
            "raised_again": None if again is None else label(again),
            "raised_again_to": None if again is None else round(float(i[again]), 2),
            "raised_again_above_earlier_peak": None if again is None else bool(i[again] > peak + 1e-9)}


def readout(rg: dict, o: dict) -> dict:
    f = four(rg, o)
    res = {"by_quarter": {}, "four_output_worst_to_2028Q4": round(float(f[:Q28 + 1].min()), 2),
           "four_output_worst_to_2028Q4_quarter": label(int(np.argmin(f[:Q28 + 1]))),
           "four_output_worst": round(float(f.min()), 2), "four_output_worst_quarter": label(int(np.argmin(f))), "regions": {}}
    for k in REPORT:
        res["by_quarter"][label(k)] = {r: {"out_of_work": round(float(o[r]["u"][k] + o[r]["out"][k]), 2),
                                           "unemployed": round(float(o[r]["u"][k]), 2), "left_workforce": round(float(o[r]["out"][k]), 2),
                                           "output": round(float(o[r]["y"][k]), 2), "core": round(float(o[r]["pi"][k]), 2),
                                           "headline": round(float(o[r]["pi_h"][k]), 2), "rate": round(float(o[r]["i"][k]), 2),
                                           "spread": round(float(o[r]["s"][k]), 2), "capital_lost": round(float(o[r]["stress"][k] * 100), 1)}
                                       for r in gc.R}
        res["by_quarter"][label(k)]["four_output"] = round(float(f[k]), 2)
    for r in gc.R:
        x = o[r]
        ow_ = x["u"] + x["out"]
        cap = next((k for k in range(len(ow_)) if ow_[k] >= CAP - 1e-9), None)
        res["regions"][r] = {"out_of_work_2027Q3": round(float(ow_[Q27]), 1), "out_of_work_2028Q4": round(float(ow_[Q28]), 1),
                             "out_of_work_2032Q2": round(float(ow_[Q32Q2]), 1), "out_of_work_2032Q3": round(float(ow_[Q32]), 1),
                             "at_the_models_cap_from": None if cap is None else label(cap),
                             "output_worst": round(float(x["y"].min()), 1), "output_worst_quarter": label(int(np.argmin(x["y"]))),
                             "headline_max": round(float(x["pi_h"][1:].max()), 2), "headline_max_quarter": label(int(np.argmax(x["pi_h"][1:])) + 1),
                             "headline_min": round(float(x["pi_h"][1:].min()), 2), "core_min": round(float(x["pi"][1:].min()), 2),
                             "rate_max": round(float(x["i"].max()), 2), "rate_min": round(float(x["i"].min()), 2),
                             "spread_max": round(float(x["s"].max()), 2), "capital_lost_max": round(float(x["stress"].max() * 100), 1),
                             "policy": fed_cuts(x["i"])}
    return res


def paths_of(rg: dict, o: dict) -> dict:
    out = {"four_output": [round(float(v), 3) for v in four(rg, o)]}
    for r in gc.R:
        x = o[r]
        out[r] = {k: [round(float(v), 3) for v in arr] for k, arr in
                  (("out_of_work", x["u"] + x["out"]), ("unemployed", x["u"]), ("left_workforce", x["out"]), ("output", x["y"]),
                   ("core", x["pi"]), ("headline", x["pi_h"]), ("rate", x["i"]), ("spread", x["s"]), ("capital_lost", x["stress"] * 100),
                   ("energy_inflation", x["e_pi"]), ("energy_bill", x["e_bill"]), ("energy_demand", x["d_energy"]))}
    return out


CS = "her case as stored (stored start)"
NE = "October bust, no energy term"
JAN = "bust in 2027Q1 instead (delay 1), no energy term"
TPR = "October bust, no energy term, the term premium's rise routed as a spread at the start too (a sensitivity)"
LOOK = "October bust, oil stays high, looking through (policy on core)"
LOOK4 = "October bust, oil stays high, looking through on four-quarter core"
TIED = "October bust, oil stays high, hands tied (policy on four-quarter headline)"
TIEDQ = "October bust, oil stays high, hands tied on quarterly headline (a sensitivity)"
COL = "October bust, oil collapses as in 2008, hands tied"
COLQ = "October bust, oil collapses as in 2008, hands tied on quarterly headline"
COLL = "October bust, oil collapses as in 2008, looking through"
COLS = "October bust, oil collapses (anchored on the late-September spot), hands tied"
COLSQ = "October bust, oil collapses (anchored on the late-September spot), hands tied on quarterly headline"
COLU = "October bust, oil collapses (the dollar's 2008 path in every currency), hands tied"
COLUQ = "October bust, oil collapses (the dollar's 2008 path in every currency), hands tied on quarterly headline"
DOT = "October bust at dot-com size, oil stays high, hands tied"
DOTQ = "October bust at dot-com size, oil stays high, hands tied on quarterly headline"
WTIT = "October bust, oil stays high with the US on WTI, hands tied"
WTITQ = "October bust, oil stays high with the US on WTI, hands tied on quarterly headline"
WTIL = "October bust, oil stays high with the US on WTI, looking through"
HELDT = "October bust, oil held high throughout, hands tied"
HELDTQ = "October bust, oil held high throughout, hands tied on quarterly headline"
HELDL = "October bust, oil held high throughout, looking through"
HER_SIZE = (NE, TPR, LOOK, LOOK4, TIED, TIEDQ, COL, COLQ, COLL, COLS, COLSQ, COLU, COLUQ, WTIT, WTITQ, WTIL, HELDT, HELDTQ,
            HELDL)                                       # 1.5x, October
TIED_READING = "headline4"   # hands tied: four quarters' headline, the main reading (decision 48, 2026-10-01); "headline" the
                             # quarterly sensitivity


def run_set(oils: dict, spreads: dict) -> dict:
    """name -> (region set, keyword arguments). Every October run carries the fresh start and the corporate spread's rise
    already present at the start (decision 47, 2026-10-01); the term-premium routing (TPR) adds the term premium's rise."""
    s0 = spreads["corporate"]
    tied, tiedq, look4 = {"react": TIED_READING}, {"react": "headline"}, {"react": "core4"}
    dot = {"scale": 1.0, "speed": 1.0}
    o = oils
    return {
        CS: ("stored", {}),
        NE: ("fresh", {"spread0": s0}),
        JAN: ("fresh", {"spread0": s0, "delay": 1}),
        TPR: ("fresh", {"spread0": spreads["both"]}),
        LOOK: ("fresh", {"spread0": s0, "oil": o["high"]}),
        LOOK4: ("fresh", {"spread0": s0, "oil": o["high"], **look4}),
        TIED: ("fresh", {"spread0": s0, "oil": o["high"], **tied}),
        TIEDQ: ("fresh", {"spread0": s0, "oil": o["high"], **tiedq}),
        COL: ("fresh", {"spread0": s0, "oil": o["collapse"], **tied}),
        COLQ: ("fresh", {"spread0": s0, "oil": o["collapse"], **tiedq}),
        COLL: ("fresh", {"spread0": s0, "oil": o["collapse"]}),
        COLS: ("fresh", {"spread0": s0, "oil": o["collapse_spot"], **tied}),
        COLSQ: ("fresh", {"spread0": s0, "oil": o["collapse_spot"], **tiedq}),
        COLU: ("fresh", {"spread0": s0, "oil": o["collapse_usd"], **tied}),
        COLUQ: ("fresh", {"spread0": s0, "oil": o["collapse_usd"], **tiedq}),
        DOT: ("fresh", {"spread0": s0, "oil": o["high"], "bust": dot, **tied}),
        DOTQ: ("fresh", {"spread0": s0, "oil": o["high"], "bust": dot, **tiedq}),
        WTIT: ("wti", {"spread0": s0, "oil": o["high_wti"], **tied}),
        WTITQ: ("wti", {"spread0": s0, "oil": o["high_wti"], **tiedq}),
        WTIL: ("wti", {"spread0": s0, "oil": o["high_wti"]}),
        HELDT: ("fresh", {"spread0": s0, "oil": o["held"], **tied}),
        HELDTQ: ("fresh", {"spread0": s0, "oil": o["held"], **tiedq}),
        HELDL: ("fresh", {"spread0": s0, "oil": o["held"]}),
    }


SENS = {  # one change each (high end)
    "expectations adapt to headline (second-round effects)": (TIED, {"expect": "headline"}, None),
    "no bill (headline and policy only; the energy bill's tax off)": (TIED, {"_no_bill": True}, None),
    "hands tied, rate transmission a_r 0.10 (Laubach-Williams; fitted 0.03, the fit's lower bound)": (TIED, {"_a_r": 0.10}, None),
    "hands tied on quarterly headline, a_r 0.10": (TIEDQ, {"_a_r": 0.10}, None),
    "looking through, rate transmission a_r 0.10": (LOOK, {"_a_r": 0.10}, None),
    "looking through on four-quarter core, a_r 0.10": (LOOK4, {"_a_r": 0.10}, None),
    "Sweden's start headline at CPIF (0.7), hands tied": (TIED, {}, "cpif"),
    "Sweden's start headline at CPIF (0.7), hands tied on quarterly headline": (TIEDQ, {}, "cpif"),
}


def run_one(cm, regs, st, kw: dict, adoption: str):
    kw = dict(kw)
    c = replace(cm, a_r=kw.pop("_a_r")) if "_a_r" in kw else cm
    if kw.pop("_no_bill", False):
        regs = {r: replace(g, energy_income=0.0) for r, g in regs.items()}
    return build(c, regs, st, adoption=adoption, **kw)


def sensitivity(cm, sets: dict, st: dict, runs: dict, M: dict, sname: str) -> dict:
    """One sensitivity (high end) against its base run; changes from the unrounded runs, rounded once."""
    base, change, set_ = SENS[sname]
    set0, kw = runs[base]
    rg, o, _ = run_one(cm, sets[set_ or set0], st, {**kw, **change}, "high")
    x, m, b = readout(rg, o), metrics(rg, o), M[base]["high"]
    d = lambda k: round(m[k] - b[k], 2) + 0.0  # noqa: E731  (+ 0.0: no negative zero)
    return {"base": base, "us_out_of_work_2028Q4": x["regions"]["US"]["out_of_work_2028Q4"],
            "us_out_of_work_2028Q4_unrounded": m["us_out_of_work_2028Q4"],
            "change_us_out_of_work_2028Q4": d("us_out_of_work_2028Q4"), "change_us_out_of_work_2032Q2": d("us_out_of_work_2032Q2"),
            "change_four_output_worst_to_2028Q4": d("four_output_worst_to_2028Q4"),
            "us_rate_max": x["regions"]["US"]["rate_max"], "change_us_rate_max": d("us_rate_max"),
            "us_policy": x["regions"]["US"]["policy"], "us_core_min": x["regions"]["US"]["core_min"],
            "rates_2026Q4_2027Q2": {r: [x["by_quarter"][q][r]["rate"] for q in ("2026Q4", "2027Q1", "2027Q2")] for r in ("US", "EA", "SE")},
            "change_ea_out_of_work_2028Q4": d("ea_out_of_work_2028Q4"), "change_se_out_of_work_2028Q4": d("se_out_of_work_2028Q4")}


FS_CORP = "new data + the corporate spread's rise (as run: the central)"
FS_TP = "new data + the term premium's rise alone as a spread at the start"
FS_BOTH = "new data + both (the term-premium routing: the sensitivity)"
FS_NEW = "new data: the fresh start without a spread at the start"


def fresh_split(cm, sets: dict, st: dict, spreads: dict) -> dict:
    """The fresh start against the stored start, one input at a time (no energy term, both ends): what is new data (the
    build-out, the core starts, the re-measured unemployment) and what is a new treatment (the spread already present: the
    corporate spread's rise, as run; the term premium's rise routed through the private credit-spread channel at a_s, the
    sensitivity)."""
    regs, fresh = sets["stored"], sets["fresh"]

    def one(**fields):
        return {r: replace(regs[r], **{f: getattr(fresh[r], f) for f in fields.get(r, ())}) for r in gc.R}
    cases = {"the build-out (decoupling.build_out on the new vintage)": (one(US=("ai_capex",)), None),
             "the core starts (US core PCE; euro-area and Swedish core HICP)": (one(US=("pi0",), EA=("pi0",), SE=("pi0",)), None),
             "the US funds rate and unemployment (unchanged)": (one(US=("i0", "u0")), None),
             "euro-area unemployment (6.3 -> 6.4)": (one(EA=("u0",)), None),
             "Sweden's unemployment (8.5 -> 8.9)": (one(SE=("u0",)), None),
             FS_NEW: (fresh, None),
             FS_CORP: (fresh, spreads["corporate"]),
             FS_TP: (fresh, spreads["term_premium"]),
             FS_BOTH: (fresh, spreads["both"])}
    out = {"note": "each row minus the stored start (her case's settings, October timing, no energy term); points of out of work",
           "overlap": "the term premium's routing is a sensitivity, not the central (decision 47, 2026-10-01): it may double "
                      "count the case's premium on borrowing, which decision 23 and case.py size as 'another move the size "
                      "of the ten-year term premium's rise since 2019' (decision 25 says the case carries decision 23's "
                      "premium)"}
    for end in E2:
        _, base, _ = build(cm, regs, st, adoption=end)
        out[end] = {}
        for name, (rg, s0) in cases.items():
            _, o, _ = build(cm, rg, st, adoption=end, spread0=s0)
            out[end][name] = {"us_2027Q3": round(float(oow(o)[Q27] - oow(base)[Q27]), 3),
                              "us_2028Q4": round(float(oow(o)[Q28] - oow(base)[Q28]), 3),
                              "ea_2028Q4": round(float(oow(o, "EA")[Q28] - oow(base, "EA")[Q28]), 3),
                              "se_2028Q4": round(float(oow(o, "SE")[Q28] - oow(base, "SE")[Q28]), 3)}
        x = out[end]
        nd = x[FS_NEW]["us_2028Q4"]
        out[end]["summary_us_2028Q4"] = {"new data": round(nd, 3),
                                         "the corporate spread's rise (as run)": round(x[FS_CORP]["us_2028Q4"] - nd, 3),
                                         "the term premium's rise alone": round(x[FS_TP]["us_2028Q4"] - nd, 3),
                                         "the term-premium routing on top of the central (the sensitivity)": round(x[FS_BOTH]["us_2028Q4"] - x[FS_CORP]["us_2028Q4"], 3)}
    return out


METRICS = ("us_out_of_work_2027Q3", "us_out_of_work_2028Q4", "us_out_of_work_2032Q2", "us_out_of_work_2032Q3", "four_output_2027Q3",
           "ea_output_2027Q3", "us_rate_2026Q4", "us_rate_2027Q1", "ea_rate_2026Q4", "ea_rate_2027Q1", "se_rate_2026Q4", "se_rate_2027Q1",
           "us_headline_2026Q4", "four_output_worst_to_2028Q4", "us_rate_max", "us_headline_max", "ea_out_of_work_2027Q3",
           "ea_out_of_work_2028Q4", "se_out_of_work_2028Q4", "ea_rate_max", "se_rate_max")


def metrics(rg: dict, o: dict) -> dict:
    """The attribution's quantities from a run's own arrays, unrounded (differences are taken from these and rounded once,
    so a row is never the difference of two values already rounded to 0.1)."""
    f = four(rg, o)
    v = {"us_out_of_work_2027Q3": oow(o)[Q27], "us_out_of_work_2028Q4": oow(o)[Q28], "us_out_of_work_2032Q2": oow(o)[Q32Q2],
         "us_out_of_work_2032Q3": oow(o)[Q32], "four_output_2027Q3": f[Q27], "ea_output_2027Q3": o["EA"]["y"][Q27],
         "us_headline_2026Q4": o["US"]["pi_h"][1], "four_output_worst_to_2028Q4": f[:Q28 + 1].min(),
         "us_rate_max": o["US"]["i"].max(), "us_headline_max": o["US"]["pi_h"][1:].max(), "ea_out_of_work_2027Q3": oow(o, "EA")[Q27],
         "ea_out_of_work_2028Q4": oow(o, "EA")[Q28], "se_out_of_work_2028Q4": oow(o, "SE")[Q28],
         "ea_rate_max": o["EA"]["i"].max(), "se_rate_max": o["SE"]["i"].max()}
    for r in ("US", "EA", "SE"):
        for k, qq in ((1, "2026Q4"), (2, "2027Q1")):
            v[f"{r.lower()}_rate_{qq}"] = o[r]["i"][k]
    return {m: float(v[m]) for m in METRICS}


P_FRESH = "the fresh start (30 Sep) against the stored start, same timing"
P_TIME = "October against a bust in 2027Q1 (one quarter earlier)"
P_TPR = "the term premium's rise routed as a spread too (the sensitivity) against the central (no energy term)"
P_EN = "the energy term, oil stays high, looking through"
P_ENH = "the energy term, oil held high throughout, looking through"
P_ENW = "the energy term, oil stays high with the US on WTI, looking through"
P_TL = "hands tied (four-quarter headline) against looking through (quarterly core): the main runs"
P_TL4 = "hands tied against looking through, both on four quarters"
P_TLQ = "hands tied against looking through, both quarterly"
P_TLW = "hands tied against looking through, both quarterly, the US on WTI"
P_TLH = "hands tied against looking through, both quarterly, oil held high throughout"
P_READ = "hands tied on quarterly headline against four quarters' (the reading)"
P_COL = "oil collapsing as in 2008 against staying high (hands tied)"
P_COLS = "oil collapsing, anchored on the late-September spot, against staying high (hands tied)"
P_COLU = "oil collapsing, the dollar's 2008 path in every currency, against staying high (hands tied)"
P_COLQ = "oil collapsing against staying high, hands tied on quarterly headline"
P_COLSQ = "oil collapsing (late-September spot) against staying high, hands tied on quarterly headline"
P_COLUQ = "oil collapsing (the dollar's 2008 path) against staying high, hands tied on quarterly headline"
P_COLL = "oil collapsing against staying high, looking through"
P_SIZE = "her bust (1.5x, two quarters) against a dot-com-sized one (both hands tied, oil high)"
P_SIZEQ = "her bust against a dot-com-sized one, both hands tied on quarterly headline"
PAIRS = {P_FRESH: (NE, CS), P_TIME: (NE, JAN), P_TPR: (TPR, NE), P_EN: (LOOK, NE), P_ENH: (HELDL, NE), P_ENW: (WTIL, NE),
         P_TL: (TIED, LOOK), P_TL4: (TIED, LOOK4), P_TLQ: (TIEDQ, LOOK), P_TLW: (WTITQ, WTIL), P_TLH: (HELDTQ, HELDL),
         P_READ: (TIEDQ, TIED), P_COL: (COL, TIED), P_COLS: (COLS, TIED), P_COLU: (COLU, TIED), P_COLQ: (COLQ, TIEDQ),
         P_COLSQ: (COLSQ, TIEDQ), P_COLUQ: (COLUQ, TIEDQ), P_COLL: (COLL, LOOK), P_SIZE: (TIED, DOT), P_SIZEQ: (TIEDQ, DOTQ)}


def attribution(M: dict) -> dict:
    """Differences between runs (high and low ends), from the unrounded runs (M: name -> end -> metrics()), rounded once."""
    out = {"note": "each row: the first run minus the second, from the unrounded runs, rounded once to 0.01; points (rates "
                   "and inflation: points a year)"}
    for k, (a, b) in PAIRS.items():
        out[k] = {end: {m: round(M[a][end][m] - M[b][end][m], 2) + 0.0 for m in METRICS} for end in E2}
    return out


RATE_RUNS = (NE, TPR, LOOK, LOOK4, TIED, TIEDQ, COL, COLQ, COLS, COLSQ, COLU, COLUQ, COLL, WTIL, WTIT, WTITQ, HELDT, HELDTQ,
             DOT, DOTQ, JAN, CS)


def rates(P: dict) -> dict:
    """The policy rates by quarter, 2026Q3 (the start) to 2028Q4, high end (as stored in the paths, three decimals). Quote
    two decimals rounded once from the unrounded runs (headline: fed_2026Q4), not from these: the Fed's 2026Q4 4.025 here
    is 4.0246, so 4.02."""
    return {r: {n: P[n]["high"][r]["rate"][:Q28 + 1] for n in RATE_RUNS} for r in ("US", "EA", "SE")}


# ------------------------------------------------------------------ 5. what would show it
def mid_quarter_monthly(vals: np.ndarray, last: pd.Period) -> pd.Series:
    """Quarter values placed at each simulated quarter's middle month (index 1 = 2026Q4 -> November 2026), linear between,
    from September 2026 at the start's value (the bust begins in October, so September's data cannot show it), to `last`."""
    pts = {pd.Period("2026-09", "M"): float(vals[0]), **{pd.Period("2026-11", "M") + 3 * (k - 1): float(v) for k, v in enumerate(vals) if k}}
    idx = pd.period_range("2026-09", last, freq="M")
    x = np.array([(p - idx[0]).n for p in pts])
    return pd.Series(np.interp([(p - idx[0]).n for p in idx], x, list(pts.values())), index=idx)


def end_quarter_monthly(vals: np.ndarray, last: pd.Period) -> pd.Series:
    """Quarter-end levels (index 0 = end of September 2026), linear between month-ends."""
    pts = {pd.Period("2026-09", "M") + 3 * k: float(v) for k, v in enumerate(vals)}
    idx = pd.period_range("2026-09", last, freq="M")
    x = np.array([(p - idx[0]).n for p in pts])
    return pd.Series(np.interp([(p - idx[0]).n for p in idx], x, list(pts.values())), index=idx)


def month_end(s: pd.Series) -> pd.Series:
    return s.groupby(s.index.to_period("M")).last()


def mappings() -> dict:
    """The measured links from the model's paths to the watcher's series (FRED, daily or weekly, overlapping 63-day changes
    with Newey-West errors where changes)."""
    hy, ehy, nq, baa, st_ = fred("BAMLH0A0HYM2"), fred("BAMLHE00EHYIOAS"), fred("NASDAQCOM"), fred("BAA10Y"), fred("STLFSI4")
    d = pd.DataFrame({"hy": hy, "ehy": ehy, "baa": baa, "nq": 100 * np.log(nq)}).dropna()
    d3 = (d - d.shift(63)).dropna()
    one = lambda y, x: ols_hac(d3[y].values, np.column_stack([np.ones(len(d3)), d3[x].values]), 63)  # noqa: E731
    (a1, b1), (_, s1), r1 = one("hy", "nq")
    (a2, b2), (_, s2), r2 = one("ehy", "nq")
    (a3, b3), (_, s3), r3 = one("hy", "baa")
    w = pd.DataFrame({"st": st_, "hy": hy.reindex(st_.index, method="ffill")}).dropna()
    (a4, b4), (_, s4), r4 = ols_hac(w["st"].values, np.column_stack([np.ones(len(w)), w["hy"].values]), 13)
    ic, u = fred("ICSA"), fred("UNRATE")
    a4w = ic.rolling(4).mean()
    c = month_end((a4w / a4w.rolling(52).min().shift(1) - 1) * 100)
    um = u.copy()
    um.index = um.index.to_period("M")
    gap = um - um.rolling(12).min().shift(1)
    cc = pd.DataFrame({"c": c, "gap": gap}).dropna()
    cc = cc[(cc.index < pd.Period("2020-03", "M")) | (cc.index > pd.Period("2021-12", "M"))]
    (a5, b5), (_, s5), r5 = ols_hac(cc["c"].values, np.column_stack([np.ones(len(cc)), cc["gap"].values]), 12)
    return {"window_ice": f"{d.index[0].date()} to {d.index[-1].date()} (FRED carries three years of ICE data)",
            "hy_3m_per_nasdaq_3m_log_pct": {"a": a1, "b": b1, "se_b": s1, "r2": r1},
            "euro_hy_3m_per_nasdaq_3m_log_pct": {"a": a2, "b": b2, "se_b": s2, "r2": r2},
            "hy_3m_per_baa_3m": {"a": a3, "b": b3, "se_b": s3, "r2": r3},
            "stlfsi_per_hy_level": {"a": a4, "b": b4, "se_b": s4, "r2": r4, "window": f"{w.index[0].date()} to {w.index[-1].date()}"},
            "claims_pct_over_52wk_low_per_u_over_12m_low": {"a": a5, "b": b5, "se_b": s5, "r2": r5,
                                                            "window": f"{cc.index[0]} to {cc.index[-1]}, without 2020-03..2021-12",
                                                            "anchor": "the path starts from the actual reading (the regression's slope "
                                                                      "times the unemployment gap over its 12-month low, which is 0 in "
                                                                      "August and September), not from the intercept"}}


RULES = {  # (series, trigger, on, near, sign): from watch/watch/tripwires.py
    "bust.us.equity": ("nasdaq_drawdown", -20, -15, -12, -1),
    "bust.credit.us": ("hy_3m", 1.5, 1.0, 1.0, 1),
    "bust.credit.eu": ("euro_hy_3m", 1.5, 1.0, 1.0, 1),
    "bust.stress": ("stlfsi", 1.0, 0.5, 0.5, 1),
    "labour.us.sahm": ("us_sahm", 0.5, 0.4, 0.3, 1),
    "labour.se.sahm": ("se_sahm", 0.6, 0.5, 0.4, 1),
    "labour.us.claims": ("claims", 25, 20, 15, 1),
}
BUSTS, LABOURS = ("bust.us.equity", "bust.credit.us", "bust.credit.eu", "bust.stress"), ("labour.us.sahm", "labour.se.sahm", "labour.us.claims")
KNIFE = 0.05                         # a reading within 5% of its bar the month before it fires, or in the month it fires


def claims_actual() -> pd.Series:
    a4 = fred("ICSA").rolling(4).mean()
    return month_end((a4 / a4.rolling(52).min().shift(1) - 1) * 100)


def watcher_series(o: dict, shock, mp: dict, last: str = "2028-12") -> dict:
    """The watcher's series month by month: measured to August (September for the market series), then the run."""
    L = pd.Period(last, "M")
    nq = fred("NASDAQCOM")
    high = float(nq.iloc[-252:].max())
    nq_m = month_end(nq)
    path_nq = end_quarter_monthly(1 - np.asarray(shock.equity["US"]), L) * float(nq.iloc[-1])
    nq_all = pd.concat([nq_m.loc[:"2026-08"], path_nq])
    s = {"nasdaq_drawdown": (nq_all / high - 1) * 100}
    lnq = 100 * np.log(nq_all / float(nq.iloc[-1]))
    for key, sid, m in (("hy", "BAMLH0A0HYM2", "hy_3m_per_nasdaq_3m_log_pct"), ("euro_hy", "BAMLHE00EHYIOAS", "euro_hy_3m_per_nasdaq_3m_log_pct")):
        act = month_end(fred(sid))
        lvl = pd.concat([act.loc[:"2026-08"], float(act.iloc[-1]) + mp[m]["b"] * lnq.loc["2026-09":]])
        s[key] = lvl
        s[key + "_3m"] = lvl - lvl.shift(3)
    # the model's own route: its credit spread (bank stress, mood, debt premium; the exogenous premia removed), via the
    # measured high-yield-to-Baa ratio
    credit = o["US"]["s"] - np.array([shock.spread.get("US", np.zeros(len(o["US"]["s"])))[k] if k else shock.spread0.get("US", 0.0)
                                      for k in range(len(o["US"]["s"]))])
    hy_model = float(month_end(fred("BAMLH0A0HYM2")).iloc[-1]) + mp["hy_3m_per_baa_3m"]["b"] * (mid_quarter_monthly(credit, L) - credit[0])
    hy_model_all = pd.concat([month_end(fred("BAMLH0A0HYM2")).loc[:"2026-08"], hy_model])
    s["hy_model_route_3m"] = hy_model_all - hy_model_all.shift(3)
    stl = month_end(fred("STLFSI4"))
    s["stlfsi"] = pd.concat([stl.loc[:"2026-08"], float(stl.iloc[-1]) + mp["stlfsi_per_hy_level"]["b"] * (s["hy"].loc["2026-09":] - float(s["hy"].loc["2026-09"]))])
    # unemployment: the measured months (to August), September held at August's (the bust begins in October), then the
    # model's quarters at their middle months; so 2026Q4's rise comes over October-November
    ur = fred("UNRATE")
    ur.index = ur.index.to_period("M")
    us_u = pd.concat([ur.loc[:"2026-08"], float(ur.iloc[-1]) + mid_quarter_monthly(o["US"]["u"] - o["US"]["u"][0], L)])
    se_a = aku()
    se_u = pd.concat([se_a.loc[:"2026-08"], float(se_a.iloc[-1]) + mid_quarter_monthly(o["SE"]["u"] - o["SE"]["u"][0], L)])

    def sahm(u):
        a = u.rolling(3).mean()
        return a - a.shift(1).rolling(12).min()
    s["us_sahm"], s["se_sahm"] = sahm(us_u), sahm(se_u)
    gap = us_u - us_u.shift(1).rolling(12).min()
    ca = claims_actual()
    s["claims"] = pd.concat([ca.loc[:"2026-08"], float(ca.iloc[-1]) + mp["claims_pct_over_52wk_low_per_u_over_12m_low"]["b"] * gap.loc["2026-09":]])
    s["_us_u"], s["_se_u"], s["_nq_level"] = us_u, se_u, nq_all
    return s


def watcher(o: dict, shock, mp: dict, last: str = "2028-12") -> dict:
    """The run's path month by month against the watcher's rules: when each would arm (near) and fire (trigger), whether it
    stays on, and when crash.joint fires."""
    L = pd.Period(last, "M")
    s = watcher_series(o, shock, mp, last)
    months = pd.period_range("2026-10", L, freq="M")
    res, active = {}, {}
    for rid, (key, trig, on, near, sign) in RULES.items():
        v = s[key].reindex(months)
        t = v * sign >= trig * sign
        o_ = v * sign >= on * sign
        n_ = v * sign >= near * sign
        fired = next((m for m in months if t[m]), None)
        act = set()
        if fired is not None:
            for m in months[months >= fired]:
                if not o_[m]:
                    break
                act.add(m)
        active[rid] = act
        before = None if fired is None else float(s[key].reindex([fired - 1]).iloc[0])
        res[rid] = {"series": key, "now": round(float(s[key].reindex([pd.Period("2026-09", "M")]).iloc[0]), 2) if pd.Period("2026-09", "M") in s[key].index else None,
                    "armed": str(next((m for m in months if n_[m]), None)), "fires": str(fired),
                    "reading_when_fired": None if fired is None else round(float(v[fired]), 2),
                    "reading_the_month_before": None if before is None else round(before, 2),
                    "knife_edge": None if before is None else bool(abs(before - trig) <= KNIFE * abs(trig)
                                                                   or abs(float(v[fired]) - trig) <= KNIFE * abs(trig)),
                    "active_months": len(act), "seen": None if fired is None else
                    (f"{fired} (daily/weekly data)" if key not in ("us_sahm", "se_sahm") else f"early {fired + 1} (the {fired} release)")}
    joint = next((m for m in months if any(m in active[b] for b in BUSTS) and any(m in active[x] for x in LABOURS)), None)
    res["crash.joint"] = {"fires": str(joint), "note": "a bust rule and a labour rule active together"}
    res["labour.us.claims"]["actual_now"] = round(float(claims_actual().iloc[-1]), 2)
    res["bust.stress"]["note"] = (f"on its measured link (STLFSI4 on the high-yield level, R2 {mp['stlfsi_per_hy_level']['r2']:.2f}, "
                                  f"{mp['stlfsi_per_hy_level']['window']}) the index stays under its bar: understated on this weak link")
    if res["bust.credit.us"]["knife_edge"]:
        res["bust.credit.us"]["note"] = (f"knife-edge: {res['bust.credit.us']['reading_the_month_before']:.2f} the month before "
                                         f"against the bar of 1.50, so November or December")
    res["model_route_hy"] = {"fires": str(next((m for m in months if s["hy_model_route_3m"].reindex(months)[m] >= 1.5), None)),
                             "on": str(next((m for m in months if s["hy_model_route_3m"].reindex(months)[m] >= 1.0), None)),
                             "note": "high yield from the model's own credit spread (bank losses) at the measured HY/Baa ratio: "
                                     "slower than the market route, which moves with stocks"}
    res["credit.nonbank.us"] = {"fires": None, "note": "not in the model: banks pulling lines from non-bank lenders would show "
                                "in the Fed's weekly H.8 within weeks (fires at -3% in 13 weeks; only 2020 since 2015); the model's "
                                "losses on AI lending begin in " + label(2)}
    res["unemployment_placement"] = ("u0 is August's reading, held through September (the bust begins in October); the model's "
                                     "2026Q4 average is placed at November, so the quarter's rise shows over October-November and "
                                     "the Sahm and claims dates inherit the model's US adjustment speed (0.9 a quarter)")
    res["monthly"] = {k: {str(m): round(float(x), 2) for m, x in s[k].reindex(pd.period_range("2026-06", "2027-12", freq="M")).items()
                          if pd.notna(x)} for k in ("nasdaq_drawdown", "hy_3m", "euro_hy_3m", "stlfsi", "us_sahm", "se_sahm", "claims",
                                                    "hy_model_route_3m")}
    return res


# --- day by day: the oil rule and the bust rules it would coincide with
ENGLAND_HOLIDAYS = ("2026-12-25", "2026-12-28", "2027-01-01", "2027-03-26", "2027-03-29", "2027-05-03", "2027-05-31",
                    "2027-08-30", "2027-12-27", "2027-12-28", "2028-01-03", "2028-04-14", "2028-04-17", "2028-05-01",
                    "2028-05-29", "2028-08-28", "2028-12-25", "2028-12-26")   # the days EIA's Brent series skips (all of them in 2023-25)
DAILY_END = "2028-12-29"
REPLAY_FROM = "2024-01-02"          # the replay's first day, with no memory (the oil rule is off then and for months after)


def board(trigger, on, near, level, escalate) -> list:
    """tripwires.Board.check for one rule, run on consecutive days (watch/watch/tripwires.py, read-only): fire when the
    trigger holds and the rule is not active; while active, stay so while `on` holds (firing again only if the level has
    moved `escalate` beyond the level it last fired at, stored rounded to 3 places); clear when `on` fails; armed when not
    active, not firing, and `near` holds."""
    out, prev = [], None
    for t, o_, n_, lv in zip(trigger, on, near, level):
        if prev is not None and o_:
            if t and escalate is not None and abs(lv) >= abs(prev) + escalate:
                prev = round(lv, 3)
                out.append("fired")
            else:
                out.append("active")
        elif t:
            prev = round(lv, 3)
            out.append("fired")
        else:
            prev = None
            out.append("armed" if n_ else "clear")
    return out


def brent_daily(path_usd, b: pd.Series, rest_of_q3: float | None = None) -> pd.Series:
    """EIA Brent to its last print, then the path held daily: weekdays without England's bank holidays; the rest of 2026Q3
    at the last print (or at rest_of_q3), each later quarter at its level (path_usd by model index, 0 = 2026Q3)."""
    days = pd.bdate_range(b.index[-1] + pd.Timedelta(days=1), DAILY_END)
    days = days[~days.isin(pd.to_datetime(list(ENGLAND_HOLIDAYS)))]
    k = np.array([(d.to_period("Q") - pd.Period(gc.START, "Q")).n for d in days])
    p = np.asarray(path_usd, float)
    q3 = float(b.iloc[-1]) if rest_of_q3 is None else float(rest_of_q3)
    lv = np.where(k == 0, q3, p[np.minimum(np.maximum(k, 0), len(p) - 1)])
    return pd.concat([b, pd.Series(lv, index=days)])


def oil_rule_days(s: pd.Series, from_: str | None = None) -> pd.DataFrame:
    """tripwires.py's energy.oil.surge (lines 484-492) on each day from REPLAY_FROM (or from_), with no memory before it:
    lvl the day's price, p3 and p6 its change over 63 and 126 observations, avg3y the mean of the 756 before it; trigger:
    lvl >= 1.25 avg3y and (p3 >= 40 or p6 >= 60); on and near: lvl >= 1.1 avg3y and (p3 >= 25 or p6 >= 40); level p3,
    escalate 20."""
    v = [float(x) for x in s.values]
    i0 = s.index.get_loc(pd.Timestamp(from_ or REPLAY_FROM))
    rows = []
    for i in range(i0, len(v)):
        lvl = v[i]
        p3, p6 = (lvl / v[i - 63] - 1) * 100, (lvl / v[i - 126] - 1) * 100
        avg3 = statistics.fmean(v[max(i - 756, 0):i])
        rows.append((lvl, p3, p6, avg3, lvl >= 1.25 * avg3 and (p3 >= 40 or p6 >= 60), lvl >= 1.1 * avg3 and (p3 >= 25 or p6 >= 40)))
    d = pd.DataFrame(rows, index=s.index[i0:], columns=["lvl", "p3", "p6", "avg3y", "trigger", "on"])
    d["status"] = board(d["trigger"], d["on"], d["on"], d["p3"], 20)
    d["active"] = d["status"].isin(["fired", "active"])
    d["level_rule"] = d["lvl"] >= 1.25 * d["avg3y"]       # decision 27 as amended (2026-10-01): the level bar
    return d


def spells(flag: pd.Series) -> list:
    """Runs of consecutive True days: [first, last]."""
    out, startd, prevd = [], None, None
    for d, f in flag.items():
        if f and startd is None:
            startd = d
        if not f and startd is not None:
            out.append([str(startd.date()), str(prevd.date())])
            startd = None
        prevd = d
    if startd is not None:
        out.append([str(startd.date()), str(prevd.date())])
    return out


def bust_days(o: dict, shock, mp: dict, s: dict) -> pd.DataFrame:
    """The bust and labour rules day by day (weekdays; the watcher runs daily): the Nasdaq linear between quarter-end
    levels (index 0 = the last print), high yield from it at the measured slope (63-observation changes), claims weekly
    (Thursdays) from the monthly mapping placed mid-month, the Sahm readings from the first Friday of the next month (the
    US release day; for Statistics Sweden a stand-in, so the Swedish dates are approximate)."""
    nq = fred("NASDAQCOM")
    days = pd.bdate_range(nq.index[-1] + pd.Timedelta(days=1), DAILY_END)
    t_q = [nq.index[-1]] + [(pd.Period(gc.START, "Q") + k).end_time.normalize() for k in range(1, N)]
    lv_q = (1 - np.asarray(shock.equity["US"])) * float(nq.iloc[-1])
    tn = lambda ix: np.asarray((ix - pd.Timestamp("2026-01-01")).days, float)  # noqa: E731
    nq_all = pd.concat([nq, pd.Series(np.interp(tn(days), tn(pd.DatetimeIndex(t_q)), lv_q), index=days)])
    dd = (nq_all / nq_all.rolling(252, min_periods=1).max() - 1) * 100
    out = pd.DataFrame(index=days)
    out["nasdaq_drawdown"] = dd.reindex(days)
    for key, sid, m in (("hy_3m", "BAMLH0A0HYM2", "hy_3m_per_nasdaq_3m_log_pct"), ("euro_hy_3m", "BAMLHE00EHYIOAS", "euro_hy_3m_per_nasdaq_3m_log_pct")):
        h = fred(sid)
        ref = float(nq_all.loc[:h.index[-1]].iloc[-1])
        fut = nq_all.loc[nq_all.index > h.index[-1]]
        lvl = pd.concat([h, float(h.iloc[-1]) + mp[m]["b"] * 100 * np.log(fut / ref)])
        out[key] = (lvl - lvl.shift(63)).reindex(days)
    tm = lambda p: pd.Timestamp(p.start_time) + pd.Timedelta(days=14)  # noqa: E731
    cl = s["claims"].dropna()
    cl_d = pd.Series(np.interp(tn(days), tn(pd.DatetimeIndex([tm(p) for p in cl.index])), cl.values), index=days)
    thu = cl_d.where(days.weekday == 3).ffill()
    out["claims"] = thu.fillna(float(claims_actual().iloc[-1]))
    for key in ("us_sahm", "se_sahm"):
        m = s[key].dropna()
        rel = {}
        for p, v in m.items():
            fst = pd.Timestamp((p + 1).start_time)
            rel[fst + pd.Timedelta(days=(4 - fst.weekday()) % 7)] = float(v)
        out[key] = pd.Series(rel).reindex(days.union(pd.DatetimeIndex(list(rel)))).sort_index().ffill().reindex(days)
    spec = {"bust.us.equity": ("nasdaq_drawdown", -20, -15, -12, -1, 10), "bust.credit.us": ("hy_3m", 1.5, 1.0, 1.0, 1, 0.75),
            "bust.credit.eu": ("euro_hy_3m", 1.5, 1.0, 1.0, 1, 0.75), "labour.us.sahm": ("us_sahm", 0.5, 0.4, 0.3, 1, 0.25),
            "labour.se.sahm": ("se_sahm", 0.6, 0.5, 0.4, 1, 0.25), "labour.us.claims": ("claims", 25, 20, 15, 1, 10)}
    for rid, (key, trig, on, near, sg, esc) in spec.items():
        v = out[key]
        out[rid] = board(v * sg >= trig * sg, v * sg >= on * sg, v * sg >= near * sg, v, esc)
        out[rid + ".active"] = out[rid].isin(["fired", "active"])
    b_any = out[[f"{x}.active" for x in ("bust.us.equity", "bust.credit.us", "bust.credit.eu")]].any(axis=1)
    l_any = out[[f"{x}.active" for x in ("labour.us.sahm", "labour.se.sahm", "labour.us.claims")]].any(axis=1)
    j = b_any & l_any
    out["crash.joint"] = board(j, j, j, (b_any.astype(int) + l_any.astype(int)), 2)
    out["crash.joint.active"] = out["crash.joint"].isin(["fired", "active"])
    return out


BUST_FOR_27 = ("bust.us.equity", "bust.credit.us", "crash.joint")
FUTURES_STRIP = (102.0, 107.0)      # front-month Brent futures in late September (the reviews' news check; not a series here)
TABLE_LEVELS = (100.0, 102.0, 103.0, 105.0, 107.0, 107.5, 109.5, 110.0, 113.0, 115.0, 116.0, 120.0)


def together(d: pd.DataFrame, bd: pd.DataFrame) -> dict:
    """Decision 27's condition on one oil replay (d, Brent prints) against one run's daily bust rules (bd, weekdays): the
    weekdays on which Brent is at its level bar (level-based: the condition as amended 2026-10-01) or the oil rule is active
    (the first wording, superseded), each carried over the weekdays EIA skips, while bust.us.equity, bust.credit.us or
    crash.joint is active; and the Brent prints among them."""
    bust = bd[[f"{x}.active" for x in BUST_FOR_27]].any(axis=1)
    ix = bd.index.union(d.index)
    act = d["active"].reindex(ix).ffill().reindex(bd.index).fillna(False).astype(bool)
    lvl = d["level_rule"].reindex(ix).ffill().reindex(bd.index).fillna(False).astype(bool)
    both = act & bust
    prints = both.reindex(d.index[d.index.isin(bd.index)])
    return {"oil_and_a_bust_rule_active_together": spells(both), "weekdays_together": int(both.sum()),
            "brent_prints_together": int(prints.sum()), "condition_met_first_wording": bool(both.any()),
            "level_based_together": spells(lvl & bust), "level_based_days": int((lvl & bust).sum()),
            "condition_met_level_based": bool((lvl & bust).any())}


def held_path(level: float, oils: dict) -> np.ndarray:
    """The 'stays high' shape at a given level (dollars): the level for the four quarters from 2026Q4, the geometric
    midpoint with the three-year average, then the three-year average (index 0, 2026Q3, as measured)."""
    p = np.array(oils["paths"]["high"]["US"][1], float)
    tr = oils["usd"]["three_year_average"]
    p[1:5] = level
    p[5] = float(np.exp(0.5 * (np.log(level) + np.log(tr))))
    return p


def oil_threshold(oils: dict, runs_daily: dict) -> dict:
    """Decision 27's condition against the level oil holds at: dated Brent held at L from 30 Sep (the 'stays high' shape at
    L), the oil rule replayed daily, against the bust rules of the 'stays high', hands-tied run at both ends (the Nasdaq and
    high-yield rules come from the equity path, which oil does not move). A grid of L from $95 to $130 in $0.10, then the
    lowest cent at which each wording is met; the same with 30 Sep at the last print (the main replays' convention)."""
    b = fred("DCOILBRENTEU")
    bds = {end: runs_daily[(TIED, end)] for end in ("high", "low")}
    last = b.index[-1]

    def ev(L: float, at_l: bool = True) -> tuple:
        d = oil_rule_days(brent_daily(held_path(L, oils), b, L if at_l else None))
        return d, {end: together(d, bd) for end, bd in bds.items()}

    def flags(L: float, at_l: bool = True) -> dict:
        _, t = ev(L, at_l)
        return {"first_wording": all(t[e]["condition_met_first_wording"] for e in t),
                "level_based": all(t[e]["condition_met_level_based"] for e in t),
                "ends_agree": len({(t[e]["condition_met_first_wording"], t[e]["condition_met_level_based"]) for e in t}) == 1}

    def row(L: float, at_l: bool = True) -> dict:
        d, t = ev(L, at_l)
        after = d.loc[d.index > last]
        return {"level": round(L, 2), "fired_after_the_last_print": [str(x.date()) for x in after.index[after["status"] == "fired"]],
                "first_off": next((str(x.date()) for x, a in after["active"].items() if not a), None),
                "active_spells_after_the_last_print": spells(after["active"]),
                "together": t["high"]["oil_and_a_bust_rule_active_together"], "weekdays_together": t["high"]["weekdays_together"],
                "brent_prints_together": t["high"]["brent_prints_together"], "met_first_wording": [t[e]["condition_met_first_wording"] for e in ("low", "high")],
                "level_based_together": t["high"]["level_based_together"], "level_based_days": t["high"]["level_based_days"],
                "met_level_based": [t[e]["condition_met_level_based"] for e in ("low", "high")]}

    grid = [c / 10 for c in range(950, 1301)]
    fl = {at_l: {L: flags(L, at_l) for L in grid} for at_l in (True, False)}
    res = {"definition": "dated Brent held at L from 30 Sep 2026 through 2027Q3 (the 'stays high' shape: then the geometric "
                         "midpoint with the three-year average, then the three-year average), the oil rule replayed daily; "
                         "met = Brent at least 1.25 times its three-year average (level-based: decision 27 as amended "
                         "2026-10-01), or the oil rule active (the first wording, superseded), on a day bust.us.equity, "
                         "bust.credit.us or crash.joint is active, at both ends",
           "grid": "$95.00 to $130.00 in $0.10",
           "ends_agree_on_the_grid": all(v["ends_agree"] for f_ in fl.values() for v in f_.values())}
    for kind in ("first_wording", "level_based"):
        x = {}
        for at_l, key in ((True, "threshold"), (False, "threshold_with_30_sep_at_the_last_print")):
            f = [fl[at_l][L][kind] for L in grid]
            switches = [grid[i] for i in range(1, len(grid)) if f[i] != f[i - 1]]
            mono = len(switches) == 1 and f[-1] and not f[0]
            x[key + "_monotone_on_the_grid"], x[key + "_switches_on_the_grid"] = mono, switches
            if mono:          # not met at the grid point below the switch, met at it: the lowest cent met between them
                lo, hi = int(round(switches[0] * 100)) - 10, int(round(switches[0] * 100))
                while hi - lo > 1:
                    mid = (lo + hi) // 2
                    if flags(mid / 100, at_l)[kind]:
                        hi = mid
                    else:
                        lo = mid
                x[key] = hi / 100
                x[key + "_confirmed"] = bool(flags(hi / 100, at_l)[kind] and not flags(lo / 100, at_l)[kind])
        if "threshold" in x:
            x["at_the_threshold"] = row(x["threshold"])
        res[kind] = x
    end_sep = oils["usd"]["end_september_last5"]
    thr = res["first_wording"].get("threshold")
    res["futures_strip"] = {"levels": list(FUTURES_STRIP), "source": "front-month Brent futures in late September (the reviews' "
                            "news check; not a series in these sources)", "rows": [row(L) for L in FUTURES_STRIP]}
    res["table"] = [row(L) for L in TABLE_LEVELS] + [row(end_sep)]
    res["knife_edge"] = thr is not None and thr > FUTURES_STRIP[1]
    res["note"] = (None if thr is None else
                   f"decision 27 as amended (2026-10-01, level-based) needs "
                   f"${res['level_based'].get('threshold', float('nan')):.2f} held from 30 Sep, and is met at the futures strip. "
                   f"The first wording (superseded) was a knife-edge: met only if dated Brent holds at ${thr:.2f} or more from "
                   f"30 Sep through late December; 'stays high' (${end_sep:.2f}) is {100 * (end_sep / thr - 1):.1f}% above that "
                   f"and the last print (${float(b.iloc[-1]):.2f}) {100 * (float(b.iloc[-1]) / thr - 1):.1f}%; at the futures strip "
                   f"(${FUTURES_STRIP[0]:.0f}-{FUTURES_STRIP[1]:.0f}) the oil rule goes off in mid-October and does not come back "
                   f"on, so the first wording is not met there.")
    return res


def entering(oils: dict) -> dict:
    """The oil rule joined the watcher on 25 Sep (STATE decision 27) and fired on its first run, so the replay's earlier
    fires are what it would have done. Replayed with no memory from each print from 22 Sep to the last (whichever data the
    first run read), on each path: its first status, and whether every status after the last print equals the replay from
    REPLAY_FROM (whose memory, from the 24 Sep escalation, differs)."""
    b = fred("DCOILBRENTEU")
    days = [str(t.date()) for t in b.loc["2026-09-22":].index]
    out = {"note": "the rule joined the watcher on 25 Sep and fired on its first run; the replay's earlier fires are what it "
                   "would have done, and the difference in memory does not change any later date",
           "entry_days": days, "paths": {}}
    for name in ("high", "held", "collapse", "collapse_spot"):
        s = brent_daily(oils["paths"][name]["US"][1], b)
        full = oil_rule_days(s)
        ref = full["status"][full.index > b.index[-1]]
        x = {}
        for t in days:
            d = oil_rule_days(s, t)
            x[t] = {"first_status": str(d["status"].iloc[0]), "level_stored": round(float(d["p3"].iloc[0]), 2),
                    "same_after_the_last_print": bool((d["status"][d.index > b.index[-1]] == ref).all())}
        out["paths"][name] = x
    out["fires_on_entry_every_day"] = all(v["first_status"] == "fired" for x in out["paths"].values() for v in x.values())
    out["no_later_date_changes"] = all(v["same_after_the_last_print"] for x in out["paths"].values() for v in x.values())
    return out


def oil_rule(oils: dict, runs_daily: dict) -> dict:
    """The oil rule day by day on each Brent path, its on / armed / fired dates, and the days it is active while a bust
    rule (bust.us.equity, bust.credit.us, crash.joint) is active: decision 27's condition as amended (level-based) and its
    first wording (superseded); the level each needs; and the replay's memory against the watcher's."""
    b = fred("DCOILBRENTEU")
    res = {"rule": "watch/watch/tripwires.py lines 484-492 and Board.check, replayed daily from " + REPLAY_FROM +
                   " (no memory) on EIA Brent (FRED DCOILBRENTEU, to " + str(b.index[-1].date()) + "), then each path held "
                   "daily (weekdays without England's bank holidays; 30 Sep at the last print)",
           "condition": "decision 27 as amended (2026-10-01): dated Brent at or above 1.25 times its three-year average (the "
                        "oil rule's own level bar) on a day a bust rule (bust.us.equity, bust.credit.us or crash.joint) is "
                        "active; the first wording (the oil rule and a bust rule active together) is superseded",
           "paths": {}}
    for name, run in (("high", TIED), ("held", HELDT), ("collapse", COL), ("collapse_spot", COLS)):
        d = oil_rule_days(brent_daily(oils["paths"][name]["US"][1], b))
        after = d.loc[d.index > b.index[-1]]
        lp = d.loc[b.index[-1]]
        x = {"label": OIL_LABELS[name], "run_for_the_bust_rules": run,
             "fired": [str(t.date()) for t in d.index[d["status"] == "fired"] if t >= pd.Timestamp("2026-01-01")],
             "active_spells_from_2026": [sp_ for sp_ in spells(d["active"]) if sp_[1] >= "2026-01-01"],
             "armed_spells_after_the_last_print": spells(after["status"] == "armed"),
             "on_days_after_the_last_print": int(after["on"].sum()),
             "first_off_after_the_last_print": next((str(t.date()) for t, a in after["active"].items() if not a), None),
             "level_rule_spells_after_the_last_print": spells(after["level_rule"]),
             "readings": {str(t.date()): {"why": why, "lvl": round(float(d.loc[t, "lvl"]), 2), "p3": round(float(d.loc[t, "p3"]), 1),
                                          "p6": round(float(d.loc[t, "p6"]), 1), "avg3y": round(float(d.loc[t, "avg3y"]), 2)}
                          for t, why in ([(next(t for t, a in after["active"].items() if not a), "first off")]
                                         + [(t, "fires again") for t in after.index[after["status"] == "fired"]]
                                         + [(t, "clears again") for t in after.index[1:][after["active"].values[:-1] & ~after["active"].values[1:]]][1:])},
             "at_the_last_print": {"date": str(b.index[-1].date()), "lvl": round(float(lp["lvl"]), 2), "p3": round(float(lp["p3"]), 2),
                                   "p6": round(float(lp["p6"]), 2), "avg3y": round(float(lp["avg3y"]), 2),
                                   "trigger": bool(lp["trigger"]), "on": bool(lp["on"]), "status": str(lp["status"])},
             "by_end": {}}
        for end in ("high", "low"):
            bd = runs_daily[(run, end)]
            fires = {rid: next((str(t.date()) for t, v in bd[rid].items() if v == "fired"), None)
                     for rid in ("bust.us.equity", "bust.credit.us", "bust.credit.eu", "labour.us.claims", "labour.us.sahm",
                                 "labour.se.sahm", "crash.joint")}
            x["by_end"][end] = {"bust_rules_fire": fires,
                                "approximate": {"labour.se.sahm": None if fires["labour.se.sahm"] is None else
                                                f"{fires['labour.se.sahm']} is approximate: the first Friday of the next month "
                                                "stands in for Statistics Sweden's release calendar"
                                                + (" and falls on New Year's Day, when nothing is released"
                                                   if fires["labour.se.sahm"][5:] == "01-01" else "")},
                                "bust_rules_active_spells": {rid: spells(bd[rid + ".active"]) for rid in BUST_FOR_27},
                                **together(d, bd)}
        res["paths"][name] = x
    # the monthly mapping's months, for comparison (the rule's month-end readings, the quarter's level held in the quarter)
    res["note"] = ("the watcher's rule is on daily data; the earlier month-end reading ('clears 2026-10') missed that it comes "
                   "back on in November (armed) and fires in December under 'stays high' or 'held high'; 'together' (the "
                   "first wording) and 'level_based_together' (the condition as amended) count weekdays (the bust rules' "
                   "calendar), with the Brent prints among them beside the first")
    res["memory"] = entering(oils)
    res["threshold"] = oil_threshold(oils, runs_daily)
    return res


# ------------------------------------------------------------------ main
def stored_regions():
    return case.stored()


def main():
    _https()
    cm, regs = stored_regions()
    C = json.load(open(os.path.join(ROOT, "results", "case.json"), encoding="utf-8"))
    pace = json.load(open(os.path.join(ROOT, "results", "pace.json"), encoding="utf-8"))
    st = case.settings(regs, pace["paces"]["multiples_of_the_papers"]["trend + 2 s.e."])
    sets, spreads, pt, sp, table = start(regs)
    oils = oil_paths()
    runs = run_set(oils["paths"], spreads)
    R, P, S, M = {}, {}, {}, {}
    for name, (set_, kw) in runs.items():
        R[name], P[name], M[name] = {}, {}, {}
        for end in E2:
            rg, o, sh = run_one(cm, sets[set_], st, kw, end)
            R[name][end] = readout(rg, o)
            P[name][end] = paths_of(rg, o)
            M[name][end] = metrics(rg, o)
            S[(name, end)] = (o, sh)
    sens = {sname: sensitivity(cm, sets, st, runs, M, sname) for sname in SENS}
    mp = mappings()
    W = {end: watcher(*S[(TIED, end)], mp) for end in ("high", "low")}
    W["no energy term, high"] = watcher(*S[(NE, "high")], mp)
    daily = {}
    for run in (TIED, HELDT, COL, COLS):
        for end in ("high", "low"):
            o, sh = S[(run, end)]
            daily[(run, end)] = bust_days(o, sh, mp, watcher_series(o, sh, mp))
    res = {"dating": {"start": gc.START, "index_0": label(0), "first_simulated_quarter": label(1), "index_of_2028Q4": Q28,
                      "index_of_2032Q3": Q32, "decision": "43, adopted 2026-10-01: one dating"},
           "quarters": N, "her_case": her_case(C, st),
           "energy": {"passthrough": pt, "oil": oils["usd"], "oil_labels": oils["labels"], "oil_alignment": oils["alignment"],
                      "bill": {"mpc": MPC_BILL, "us_producers_offset": US_OFFSET, "consumption_share": {**CONSUMPTION, "US": sets["fresh"]["US"].consumption_share},
                               "energy_income": {r: sets["fresh"][r].energy_income for r in ENERGY_REGIONS}},
                      "oil_rule": oil_rule(oils, daily)},
           "start": {"table": table, "spreads": sp, "spread_variants": spreads,
                     "regions": {r: {k: (list(v) if isinstance(v, tuple) else v) for k, v in sets["fresh"][r].__dict__.items() if k not in ("trade", "groups", "premium", "gate")}
                                 for r in gc.R}},
           "settings": st, "hands_tied_reading": TIED_READING, "runs": R, "metrics_unrounded": M, "attribution": attribution(M),
           "fresh_start_split": fresh_split(cm, sets, st, spreads), "rates": rates(P), "sensitivities": sens,
           "what_would_show_it": {"run": TIED, "mappings": mp, **W}, "paths": P}
    res["headline"] = headline(res)
    json.dump(res, open(os.path.join(ROOT, "results", "october.json"), "w", encoding="utf-8"), indent=1, default=str)
    report(res)
    figure(res, oils)


def headline(res: dict) -> dict:
    """The numbers quoted in the findings, each read from the runs above (check R3 reads them back)."""
    R, A, F = res["runs"], res["attribution"], res["fresh_start_split"]
    g = lambda n, e, r, k: R[n][e]["regions"][r][k]  # noqa: E731
    E = E2
    a = lambda pair, m: [A[pair][e][m] for e in E]  # noqa: E731
    q = lambda n, qq, r, k, e="high": R[n][e]["by_quarter"][qq][r][k]  # noqa: E731
    HC = res["her_case"]
    orl = res["energy"]["oil_rule"]["paths"]
    TH = res["energy"]["oil_rule"]["threshold"]
    MU = res["metrics_unrounded"]
    PA = res["paths"]
    SV = res["sensitivities"]

    def span(t: str, l_: str, upto: int) -> list:
        """US out of work, run t minus run l_, at any quarter up to `upto`: [min low, min high, max low, max high]."""
        d = {e: np.array(PA[t][e]["US"]["out_of_work"][:upto]) - np.array(PA[l_][e]["US"]["out_of_work"][:upto]) for e in E}
        return [round(float(d[e].min()), 2) for e in E] + [round(float(d[e].max()), 2) for e in E]
    tied_pairs = (("main_runs", P_TL), ("four_quarter_both", P_TL4), ("quarterly", P_TLQ), ("wti_quarterly", P_TLW),
                  ("held_quarterly", P_TLH))
    a_r = lambda n: SV[n]["us_out_of_work_2028Q4_unrounded"]  # noqa: E731
    return {
        "case_2028Q4": [HC[e]["us_out_of_work"]["2028Q4"] for e in E],
        "case_2032Q2": [HC[e]["us_out_of_work"]["2032Q2"] for e in E],
        "case_2032Q3": [HC[e]["us_out_of_work"]["2032Q3"] for e in E],
        "case_central_run": HC["central_run_us_out_of_work"],
        "case_ratio_to_central_2028Q4": [HC[e]["ratio_to_central_2028Q4"] for e in E],
        "case_us_output_2028Q4": [HC[e]["us_output_2028Q4"] for e in E],
        "case_four_output_2028Q4": [HC[e]["four_output_2028Q4"] for e in E],
        "case_2032Q3_below_the_cap_by": [HC[e]["2032Q3_below_the_cap_by"] for e in E],
        "case_pieces_2028Q4_2032Q2_2032Q3": {d: [v["adds_2028Q4"], v["adds_2032Q2"], v["adds_by_2032Q3"]]
                                             for d, v in HC["piece_by_piece_us_out_of_work"].items()},
        "case_dates": HC["dates"],
        "october_us_2027Q3": [g(NE, e, "US", "out_of_work_2027Q3") for e in E],
        "october_us_2028Q4": [g(NE, e, "US", "out_of_work_2028Q4") for e in E],
        "october_us_2032Q2": [g(NE, e, "US", "out_of_work_2032Q2") for e in E],
        "october_us_2032Q3": [g(NE, e, "US", "out_of_work_2032Q3") for e in E],
        "term_premium_routing_us_2028Q4": [g(TPR, e, "US", "out_of_work_2028Q4") for e in E],
        "tied_us_2028Q4": [g(TIED, e, "US", "out_of_work_2028Q4") for e in E],
        "tiedq_us_2028Q4": [g(TIEDQ, e, "US", "out_of_work_2028Q4") for e in E],
        "look_us_2028Q4": [g(LOOK, e, "US", "out_of_work_2028Q4") for e in E],
        "collapse_us_2028Q4": [g(COL, e, "US", "out_of_work_2028Q4") for e in E],
        "dotcom_us_2028Q4": [g(DOT, e, "US", "out_of_work_2028Q4") for e in E],
        "jan_us_2028Q4": [g(JAN, e, "US", "out_of_work_2028Q4") for e in E],
        "case_stored_start_us_2028Q4": [g(CS, e, "US", "out_of_work_2028Q4") for e in E],
        "at_cap_2032Q3": {n: [R[n][e]["regions"]["US"]["at_the_models_cap_from"] for e in E] for n in R},
        "four_output_worst_to_2028Q4": {n: [R[n][e]["four_output_worst_to_2028Q4"] for e in E] for n in (CS, NE, TIED, COL, DOT)},
        "fresh_split_high": F["high"]["summary_us_2028Q4"], "fresh_split_low": F["low"]["summary_us_2028Q4"],
        "fresh_start_adds_us_2028Q4": a(P_FRESH, "us_out_of_work_2028Q4"),
        "term_premium_routing_adds_us": {m: a(P_TPR, m) for m in ("us_out_of_work_2027Q3", "us_out_of_work_2028Q4", "us_out_of_work_2032Q2")},
        "timing_adds_us_2027Q3": a(P_TIME, "us_out_of_work_2027Q3"),
        "timing_adds_us_2028Q4": a(P_TIME, "us_out_of_work_2028Q4"),
        "timing_adds_us_2032Q2": a(P_TIME, "us_out_of_work_2032Q2"),
        "timing_adds_us_2032Q3": a(P_TIME, "us_out_of_work_2032Q3"),
        "energy_adds_us_2027Q3": a(P_EN, "us_out_of_work_2027Q3"),
        "energy_adds_us_2028Q4": a(P_EN, "us_out_of_work_2028Q4"),
        "energy_adds_four_output_2027Q3": a(P_EN, "four_output_2027Q3"),
        "energy_adds_ea_output_2027Q3": a(P_EN, "ea_output_2027Q3"),
        "energy_held_adds_us_2028Q4": a(P_ENH, "us_out_of_work_2028Q4"),
        "energy_held_adds_ea_2028Q4": a(P_ENH, "ea_out_of_work_2028Q4"),
        "energy_wti_adds_us_2028Q4": a(P_ENW, "us_out_of_work_2028Q4"),
        "energy_effect_us_range_to_2032Q3_high": [span(LOOK, NE, N)[1], span(LOOK, NE, N)[3]],
        "energy_bill_max_tied_high": {r: round(max(PA[TIED]["high"][r]["energy_bill"]), 3) for r in ENERGY_REGIONS},
        "energy_demand_min_tied_high": {r: round(min(PA[TIED]["high"][r]["energy_demand"]), 3) for r in ENERGY_REGIONS},
        "tied_effect_us_range_to_2028Q4": {k: span(*PAIRS[p], Q28 + 1) for k, p in tied_pairs},
        "us_headline_2026Q4": {"brent": q(TIED, "2026Q4", "US", "headline"), "wti": q(WTIT, "2026Q4", "US", "headline"),
                               "core": q(TIED, "2026Q4", "US", "core")},
        "ea_headline_2026Q4": [q(TIED, "2026Q4", "EA", "headline"), q(TIED, "2026Q4", "EA", "core")],
        "fed_tied": {qq: {"four_quarter": q(TIED, qq, "US", "rate"), "quarterly": q(TIEDQ, qq, "US", "rate"),
                          "wti_four_quarter": q(WTIT, qq, "US", "rate"), "wti_quarterly": q(WTITQ, qq, "US", "rate")}
                     for qq in ("2026Q4", "2027Q1", "2027Q2")},
        "tied_adds_rate_2027Q1": {k: {r: A[p]["high"][f"{r}_rate_2027Q1"] for r in ("us", "ea", "se")} for k, p in tied_pairs[:4]},
        "tied_adds_us_2028Q4": {k: a(p, "us_out_of_work_2028Q4") for k, p in tied_pairs},
        "quarterly_reading_adds_us_2028Q4": a(P_READ, "us_out_of_work_2028Q4"),
        "tied_adds_us_2028Q4_at_a_r_010": {
            "main_runs": round(a_r("hands tied, rate transmission a_r 0.10 (Laubach-Williams; fitted 0.03, the fit's lower bound)")
                               - a_r("looking through, rate transmission a_r 0.10"), 2),
            "four_quarter_both": round(a_r("hands tied, rate transmission a_r 0.10 (Laubach-Williams; fitted 0.03, the fit's lower bound)")
                                       - a_r("looking through on four-quarter core, a_r 0.10"), 2),
            "quarterly": round(a_r("hands tied on quarterly headline, a_r 0.10") - a_r("looking through, rate transmission a_r 0.10"), 2)},
        "a_r_010_level_change_us_2028Q4_tied": SV["hands tied, rate transmission a_r 0.10 (Laubach-Williams; fitted 0.03, the fit's lower bound)"]["change_us_out_of_work_2028Q4"],
        "a_r_010_level_change_us_2028Q4": SV["looking through, rate transmission a_r 0.10"]["change_us_out_of_work_2028Q4"],
        "collapse_cushion": {k: {m: a(p, m) for m in ("us_out_of_work_2027Q3", "us_out_of_work_2028Q4", "four_output_2027Q3", "ea_output_2027Q3", "ea_out_of_work_2028Q4")}
                             for k, p in (("q3_average_own_currency", P_COL), ("late_september_spot_own_currency", P_COLS),
                                          ("dollar_ratios_everywhere", P_COLU), ("q3_average_quarterly", P_COLQ),
                                          ("late_september_spot_quarterly", P_COLSQ), ("dollar_ratios_quarterly", P_COLUQ),
                                          ("q3_average_looking_through", P_COLL))},
        "size_adds_us_2028Q4": a(P_SIZE, "us_out_of_work_2028Q4"),
        "size_adds_us_2032Q2": a(P_SIZE, "us_out_of_work_2032Q2"),
        "size_adds_us_2032Q3": a(P_SIZE, "us_out_of_work_2032Q3"),
        "size_adds_us_2028Q4_quarterly": a(P_SIZEQ, "us_out_of_work_2028Q4"),
        "policy": {n: R[n]["high"]["regions"]["US"]["policy"] for n in (NE, TPR, LOOK, LOOK4, TIED, TIEDQ, COL, COLQ, WTIT, WTITQ, HELDT, DOT, DOTQ, JAN, CS)},
        "rates_2026Q4_2028Q1": {k: {r: res["rates"][r][n][1:7] for r in ("US", "EA", "SE")} for k, n in
                                (("tied", TIED), ("tiedq", TIEDQ), ("look", LOOK), ("look4", LOOK4), ("no_energy", NE),
                                 ("collapse_tied", COL), ("collapse_tiedq", COLQ), ("wti_tied", WTIT), ("dot_tied", DOT), ("dot_tiedq", DOTQ))},
        "se_rate_tied_cpif": SV["Sweden's start headline at CPIF (0.7), hands tied"]["rates_2026Q4_2027Q2"]["SE"],
        "se_rate_tiedq_cpif": SV["Sweden's start headline at CPIF (0.7), hands tied on quarterly headline"]["rates_2026Q4_2027Q2"]["SE"],
        "fed_2026Q4": {k: round(MU[n]["high"]["us_rate_2026Q4"], 2) for k, n in (("no_energy", NE), ("look", LOOK), ("tied", TIED), ("tiedq", TIEDQ))},
        "se_rate_2026Q4_2027Q1": {n: [round(MU[n]["high"]["se_rate_2026Q4"], 2), round(MU[n]["high"]["se_rate_2027Q1"], 2),
                                      round(MU[n]["high"]["se_rate_2027Q1"] - MU[n]["high"]["se_rate_2026Q4"], 3)]
                                  for n in (NE, LOOK, COLL, WTIL, HELDL, LOOK4, TIED, WTIT, HELDT, COL, COLS, COLU, TIEDQ, WTITQ, HELDTQ, COLQ, COLSQ, COLUQ)},
        "regions_2028Q4": {n: {r: [g(n, e, r, "out_of_work_2028Q4") for e in E] for r in ("EA", "SE", "CN")}
                           for n in (CS, NE, TPR, TIED, LOOK, COL, DOT, HELDT, HELDL)},
        "oil_rule_threshold": {"level_based": TH["level_based"].get("threshold"), "first_wording": TH["first_wording"].get("threshold"),
                               "level_based_with_30_sep_at_the_last_print": TH["level_based"].get("threshold_with_30_sep_at_the_last_print"),
                               "first_wording_with_30_sep_at_the_last_print": TH["first_wording"].get("threshold_with_30_sep_at_the_last_print"),
                               "level_based_at_the_threshold": TH["level_based"]["at_the_threshold"]["level_based_together"],
                               "first_wording_at_the_threshold": {k: TH["first_wording"]["at_the_threshold"][k] for k in
                                                                  ("fired_after_the_last_print", "first_off", "together", "weekdays_together", "brent_prints_together")},
                               "futures_strip": {str(x["level"]): {k: x[k] for k in ("fired_after_the_last_print", "first_off", "met_first_wording",
                                                                                      "level_based_together", "met_level_based")}
                                                 for x in TH["futures_strip"]["rows"]},
                               "knife_edge": TH["knife_edge"], "note": TH["note"]},
        "oil_rule_memory": {k: res["energy"]["oil_rule"]["memory"][k] for k in ("fires_on_entry_every_day", "no_later_date_changes")},
        "watch_high": {k: res["what_would_show_it"]["high"][k]["fires"] for k in list(RULES) + ["crash.joint"]},
        "watch_seen_high": {k: res["what_would_show_it"]["high"][k]["seen"] for k in RULES},
        "watch_knife_edge_high": {k: res["what_would_show_it"]["high"][k]["knife_edge"] for k in RULES},
        "oil_rule": {p: {"fired_after_the_last_print": [d for d in orl[p]["fired"] if d > res["energy"]["oil"]["last_date"]],
                         "first_off": orl[p]["first_off_after_the_last_print"],
                         "active_spells": orl[p]["active_spells_from_2026"][-2:],
                         "met_level_based": [orl[p]["by_end"][e]["condition_met_level_based"] for e in E],
                         "level_based_together_high": orl[p]["by_end"]["high"]["level_based_together"],
                         "level_based_together_low": orl[p]["by_end"]["low"]["level_based_together"],
                         "met_first_wording": [orl[p]["by_end"][e]["condition_met_first_wording"] for e in E],
                         "first_wording_together_high": orl[p]["by_end"]["high"]["oil_and_a_bust_rule_active_together"],
                         "first_wording_together_low": orl[p]["by_end"]["low"]["oil_and_a_bust_rule_active_together"],
                         "weekdays_together": [orl[p]["by_end"][e]["weekdays_together"] for e in E],
                         "brent_prints_together": [orl[p]["by_end"][e]["brent_prints_together"] for e in E]} for p in orl},
    }


def report(res: dict):
    hc = res["her_case"]
    print("THE DATING AND HER CASE:", hc["note"][:300], "...")
    for e in E2:
        print(f"  her case ({e}):", hc[e])
    print("  central run:", hc["central_run_us_out_of_work"], "dates:", hc["dates"])
    print("  pieces:", hc["piece_by_piece_us_out_of_work"])
    print("\nTHE ENERGY TERM (headline minus core on energy share x crude's change, this quarter and last):")
    for r, p in res["energy"]["passthrough"].items():
        cx = p["cross_check_consumer_energy_on_crude"]
        print(f"  {r} ({p['crude']}) {p['window']} n={p['n']}: b0 {p['b0']:.3f} ({p['se_b0']:.3f}), b1 {p['b1']:.3f} ({p['se_b1']:.3f}), R2 {p['r2']:.2f}; "
              f"consumer energy on crude {cx['c0']:.3f}, {cx['c1']:.3f} (R2 {cx['r2']:.2f}); share now {p['energy_share_latest']:.4f}")
    print("  oil (USD):", {k: v for k, v in res["energy"]["oil"].items() if k not in ("analogue_2008",)})
    print("  alignment:", res["energy"]["oil_alignment"])
    print("\nTHE OIL RULE, DAY BY DAY (decision 27 as amended: level-based; the first wording beside it):")
    for p, x in res["energy"]["oil_rule"]["paths"].items():
        print(f"  {p}: fired {x['fired']}; active {x['active_spells_from_2026']}; armed after {x['armed_spells_after_the_last_print']}; "
              f"on days {x['on_days_after_the_last_print']}; first off {x['first_off_after_the_last_print']}; level rule {x['level_rule_spells_after_the_last_print']}")
        for e, y in x["by_end"].items():
            print(f"     {e}: busts fire {y['bust_rules_fire']}; level-based {y['level_based_together']} ({y['level_based_days']} weekdays); "
                  f"first wording {y['oil_and_a_bust_rule_active_together']} ({y['weekdays_together']} weekdays, {y['brent_prints_together']} Brent prints)")
    th = res["energy"]["oil_rule"]["threshold"]
    print("  THRESHOLDS:", th["note"])
    for kind in ("level_based", "first_wording"):
        print(f"    {kind}:", {k: v for k, v in th[kind].items() if k != "at_the_threshold"})
        print("      at the threshold:", th[kind].get("at_the_threshold"))
    for x in th["futures_strip"]["rows"] + th["table"]:
        print(f"    ${x['level']:.2f}: level-based {x['level_based_together']}; oil rule fired {x['fired_after_the_last_print']}, first off "
              f"{x['first_off']}; first wording {x['together']} ({x['weekdays_together']} weekdays, {x['brent_prints_together']} prints)")
    print("  MEMORY (entering with no memory, 22 Sep to the last print):",
          {k: v for k, v in res["energy"]["oil_rule"]["memory"].items() if k not in ("paths",)})
    print("\nTHE START (stored -> October):")
    for r, t in res["start"]["table"].items():
        for k, v in t.items():
            print(f"  {r} {k}: {v['stored']} -> {v['october']}  [{v['source']}]")
    print("  spreads:", {k: (round(v, 3) if isinstance(v, float) else v) for k, v in res["start"]["spreads"].items()})
    print("\nTHE RUNS (US out of work 2028Q4 / 2032Q2 / 2032Q3; four's output worst to 2028Q4; US rate max; Fed):")
    for n, x in res["runs"].items():
        for e in E2:
            u = x[e]["regions"]["US"]
            print(f"  {n[:70]:70s} {e:4s}: US {u['out_of_work_2028Q4']:5.1f} / {u['out_of_work_2032Q2']:5.1f} / {u['out_of_work_2032Q3']:5.1f}; "
                  f"EA {x[e]['regions']['EA']['out_of_work_2028Q4']:5.1f}; SE {x[e]['regions']['SE']['out_of_work_2028Q4']:5.1f}; "
                  f"CN {x[e]['regions']['CN']['out_of_work_2028Q4']:5.1f}; four {x[e]['four_output_worst_to_2028Q4']:6.2f}; "
                  f"US headline max {u['headline_max']:5.2f}; {u['policy']}")
    print("\nRATES (high end, 2026Q3..2028Q4):")
    for r, t in res["rates"].items():
        for n, v in t.items():
            print(f"  {r} {n[:70]:70s} {v}")
    print("\nATTRIBUTION (high):")
    for k, v in res["attribution"].items():
        if k != "note":
            print(f"  {k}: {v['high']}")
    print("\nFRESH START SPLIT:", json.dumps(res["fresh_start_split"], indent=0)[:3000])
    print("\nSENSITIVITIES:")
    for k, v in res["sensitivities"].items():
        print(f"  {k}: {v}")
    print("\nWHAT WOULD SHOW IT (high end):")
    for k, v in res["what_would_show_it"]["high"].items():
        if k != "monthly":
            print(f"  {k}: {v}")
    print("  monthly:", json.dumps(res["what_would_show_it"]["high"]["monthly"])[:2000])
    print("\nHEADLINE:", json.dumps(res["headline"], indent=0)[:9000])


def figure(res: dict, oils: dict):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams["axes.titlesize"] = 10
    P = res["paths"]
    t = gc.quarter_mid(np.arange(N))             # each quarter at its middle
    fig, ax = plt.subplots(2, 3, figsize=(18, 9.6), layout="constrained")
    fig.get_layout_engine().set(rect=(0, 0.07, 1, 0.93))
    runs = [(CS, "her case as stored", "grey", ":"), (JAN, "bust in 2027Q1, no energy term", "C7", "--"),
            (NE, "October, no energy term (the central)", "k", "-"), (TPR, "October, the term premium routed too", "C5", ":"),
            (LOOK, "October, oil high, looking through", "C0", "-"), (TIED, "October, oil high, hands tied", "C3", "-"),
            (COL, "October, oil collapses (2008), hands tied", "C2", "-"), (DOT, "October, dot-com size, hands tied", "C1", "--")]
    a = ax[0, 0]
    for n, lab, c, ls in runs:
        a.plot(t, P[n]["high"]["US"]["out_of_work"], color=c, ls=ls, label=lab)
        a.plot(t, P[n]["low"]["US"]["out_of_work"], color=c, ls=ls, lw=0.6, alpha=0.7)
    a.axvline(t[Q28], color="grey", lw=0.6, ls="--")
    a.axhline(CAP, color="grey", lw=0.6, ls=":")
    a.text(t[1], CAP + 0.6, "the model's cap on non-employment (50%): high ends there are floors", fontsize=7, color="grey")
    a.set_title("1. US out of work (unemployed + left the workforce), %\nthick: adoption at twice the usual share; thin: the usual share")
    a.legend(fontsize=7, loc="lower right")
    a = ax[0, 1]
    for r, c in zip(gc.R, ("C0", "C1", "C2", "C3")):
        a.plot(t, P[TIED]["high"][r]["output"], color=c, label=r)
        a.plot(t, P[NE]["high"][r]["output"], color=c, ls=":", lw=0.9)
    a.axhline(0, color="grey", lw=0.8)
    a.set_xlim(t[0], t[Q28 + 4])
    a.set_title("2. Output against capacity, %, to 2029Q4 (high end)\nsolid: oil stays high, hands tied; dotted: no energy term")
    a.legend(fontsize=8)
    a = ax[0, 2]
    for n, lab, c, ls in ((TIED, "Fed, oil high, tied (four-quarter headline)", "C3", "-"), (TIEDQ, "Fed, oil high, tied (quarterly headline)", "C3", "--"),
                          (LOOK, "Fed, looking through", "C0", "-"), (COL, "Fed, oil collapses, tied (four-quarter)", "C2", "-"),
                          (COLQ, "Fed, oil collapses, tied (quarterly)", "C2", "--")):
        a.plot(t, P[n]["high"]["US"]["rate"], color=c, ls=ls, label=lab)
    for n, lab, c, ls in ((COL, "ECB, oil collapses, tied (four-quarter)", "C4", "-"), (COLQ, "ECB, oil collapses, tied (quarterly)", "C4", "--")):
        a.plot(t, P[n]["high"]["EA"]["rate"], color=c, ls=ls, label=lab)
    a.set_xlim(t[0], t[Q28 + 4])
    a.set_title("3. Policy rates, % (high end), to 2029Q4: hands tied on four quarters' headline\n(y/y-like, solid; the main reading) or the last quarter's (annualised, dashed)")
    a.legend(fontsize=6.5)
    a = ax[1, 0]
    for n, lab, c, ls in ((TIED, "oil high (Brent), headline", "C3", "-"), (WTIT, "oil high (the US on WTI), headline", "C1", "-"),
                          (HELDT, "oil held high throughout, headline", "C5", "--"), (COL, "oil collapses, headline", "C2", "-")):
        a.plot(t, P[n]["high"]["US"]["headline"], color=c, ls=ls, label=lab)
    a.plot(t, P[NE]["high"]["US"]["core"], color="k", lw=0.8, ls=":", label="core (no energy term)")
    a.set_xlim(t[0], t[Q28 + 4])
    a.axhline(2, color="grey", lw=0.6)
    a.set_title("4. US inflation, % a year (PCE; the model's pi is core), hands tied")
    a.legend(fontsize=7)
    a = ax[1, 1]
    b = fred("DCOILBRENTEU")
    orl = res["energy"]["oil_rule"]["paths"]
    hb = b.loc["2025-07-01":]
    a.plot(hb.index, hb.values, color="k", lw=0.8, label="EIA Brent")
    short = {"high": "stays high", "held": "held high", "collapse": "collapses (2008), on 2026Q3's average",
             "collapse_spot": "collapses (2008), on the late-Sep spot"}
    for name, c, ls in (("high", "C3", "-"), ("held", "C5", "--"), ("collapse", "C2", "-"), ("collapse_spot", "C8", "-")):
        s = brent_daily(oils["paths"][name]["US"][1], b).loc[b.index[-1]:"2027-12-31"]
        a.plot(s.index, s.values, color=c, lw=1.1, ls=ls, label=short[name])
    d = oil_rule_days(brent_daily(oils["paths"]["high"]["US"][1], b)).loc["2025-07-01":"2027-12-31"]
    a.plot(d.index, 1.25 * d["avg3y"], color="grey", lw=0.7, ls="--", label="1.25 x 3-year average (stays high): decision 27's bar")
    a.plot(d.index, 1.1 * d["avg3y"], color="grey", lw=0.7, ls=":", label="1.1 x 3-year average")
    for sp_ in orl["high"]["active_spells_from_2026"]:
        a.axvspan(pd.Timestamp(sp_[0]), pd.Timestamp(sp_[1]), color="C3", alpha=0.12, lw=0)
    for sp_ in orl["high"]["by_end"]["high"]["bust_rules_active_spells"]["bust.us.equity"]:
        a.axvspan(pd.Timestamp(sp_[0]), pd.Timestamp(sp_[1]), ymin=0, ymax=0.06, color="C0", alpha=0.6, lw=0)
    th = res["energy"]["oil_rule"]["threshold"]
    x_th = [b.index[-1], pd.Timestamp("2027-09-30")]
    a.fill_between(x_th, *FUTURES_STRIP, color="C1", alpha=0.18, lw=0, label=f"futures strip, late Sep (${FUTURES_STRIP[0]:.0f}-{FUTURES_STRIP[1]:.0f})")
    if th["level_based"].get("threshold"):
        a.hlines(th["level_based"]["threshold"], *x_th, color="C0", lw=0.9, ls="-.",
                 label=f"decision 27 as amended (level-based): met from ${th['level_based']['threshold']:.2f}")
    if th["first_wording"].get("threshold"):
        a.hlines(th["first_wording"]["threshold"], *x_th, color="C3", lw=0.9, ls="-.",
                 label=f"its first wording (superseded): met from ${th['first_wording']['threshold']:.2f}")
    a.axvline(b.index[-1], color="k", lw=0.6)
    a.set_title("5. Brent, $ a barrel, daily (EIA via FRED to 29 Sep, then the paths)\nred shading: the oil rule active (stays high); "
                "blue bar: the Nasdaq rule active")
    a.set_ylim(30, 230)
    a.legend(fontsize=6.0, loc="upper right", ncol=2)
    a = ax[1, 2]
    wm = res["what_would_show_it"]["high"]["monthly"]
    ms = sorted(wm["nasdaq_drawdown"])
    xm = np.arange(len(ms))
    for key, bar_, lab, c in (("nasdaq_drawdown", -20, "Nasdaq from its 52-week high (bar -20%)", "C0"),
                              ("hy_3m", 1.5, "US high yield, 3-month change (bar +150 bp)", "C3"),
                              ("claims", 25, "US claims over their 52-week low (bar +25%)", "C1"),
                              ("us_sahm", 0.5, "US Sahm reading (bar 0.5)", "C2"),
                              ("se_sahm", 0.6, "Swedish Sahm reading (bar 0.6)", "C4")):
        a.plot(xm, [min(wm[key].get(m, np.nan) / bar_, 4) for m in ms], color=c, label=lab)
    a.axhline(1, color="k", lw=0.8, ls="--")
    a.axvline(ms.index("2026-10") - 0.5, color="grey", lw=0.6)
    a.set_ylim(-0.6, 4.1)
    a.set_xticks(xm[::3]); a.set_xticklabels(ms[::3], rotation=45, fontsize=7)
    a.set_title("6. The watcher's rules month by month: each reading over its firing bar\n(1 = fires; capped at 4; high end, oil high, hands tied)")
    a.legend(fontsize=7, loc="upper left")
    for a_ in (ax[0, 0], ax[0, 1], ax[0, 2], ax[1, 0]):
        a_.set_xlabel("year (index 0 = 2026Q3, the start measured to September 2026; the first simulated quarter is 2026Q4)", fontsize=7)
    fig.text(0.01, 0.005, "october.py: her case (a bust 1.5x the dot-com one over two quarters; the premium on borrowing; US tariffs; care capping out; "
             "European austerity; the pace rising from the bound seen) with its first falls in 2026Q4,\nfrom a start measured to 30 Sep 2026 with "
             "the corporate spread's three-month rise at the start. The energy term: headline = core + energy's share x the measured pass-through of "
             "crude (US PCE 1990-2026; euro-area and Swedish HICP 2000-2026).\nHands tied: central banks react to four quarters' headline (the last "
             "quarter's a sensitivity); looking through: to core. 'Stays high': dated Brent at its late-September level for four quarters, above the "
             "futures strip, then its three-year average.\nThe energy bill as a tax on consumers is approximate. Watcher mapping: linear within quarters; "
             "spreads from stocks at the 2023-26 relation (FRED's three years of ICE data); the oil rule replayed daily with tripwires.py's logic.",
             fontsize=7.5)
    p = os.path.join(ROOT, "figures", "fig_october.png")
    fig.savefig(p, dpi=130)
    print(p)


if __name__ == "__main__":
    main()
