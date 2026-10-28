# case.py — her case: what we think is happening, as runs of the crash model. Her call (2026-09-25): pin down a
# "this is what we think is happening" case across the model, the watcher and the website. Her leanings: deficit worries,
# perhaps sovereign default worries; recession and consumption-demand worries; a stock bust bigger than the dot-com one;
# care capping out as an absorber; reckless tariffs from the US and something more sensible but still austere from
# Europe; the process under way for two to four years, accelerating as AI companies behave differently. Where she left it
# open, the settings are Claude's best guesses, each stated, and each a decision in STATE.md's veto window (23-27).
#
# Redone 2026-10-26 on her delegation (STATE Log 42: well calibrated, on new data, fitting the path of the bubble pop now
# seen): one start for the case and the model (gc.regions_today on the dated vintage in cache/start/, vintage.py), and
# the bust's three legs timed and shaped as the 2000-02 bust measured them, from the quarter of today's peak.
#
# Restated 2026-10-28 on the adopted monthly fit (decision 91): the model runs by month. Index 0 is the state measured on
# data to September 2026 (the end of 2026Q3); index k the end of the k-th month after; 73 months, to the end of 2032Q3.
# Every input is built by month; every reading named by a quarter is that quarter's average of its months
# (gc.to_quarters), as quarterly data are measured, on the one quarterly dating (gc.quarter_label: quarter 1 is 2026Q4,
# quarter 9 2028Q4, quarter 24 2032Q3). The case, in the model's terms:
#   the bust        1.5x the dot-com bust's size (ai_shock's US equity 0.40 -> 0.60 at the trough, 60% of the above-trend
#                   build-out -> 90%, 1.5x its losses on AI lending), on the 2000-02 bust's measured path (global_crash.bust_2000:
#                   household equity, the build-out, bank losses, each by quarter from the quarter of the equity peak,
#                   read at each month's end), starting in the quarter of today's peak (the Nasdaq's and the S&P's high,
#                   6 Oct 2026: 2026Q4). The 8 Oct case ran ai_shock's ramps instead: all three legs at full size within
#                   two quarters, held forever; that timing is an alternative here. October's data fit the measured path's
#                   first quarter (US equity at about its Q3 level, the periphery and the lowest credit tier breaking, the
#                   build-out still rising) and not the ramp's (equity -30% in 2026Q4);
#   the pace        displacement starts at the upper bound seen so far (pace.py) and rises on a logistic to the paper's
#                   pace, half the rise by the end of 2028Q2 (quarter 7; month 21);
#   adoption        a range: firms automate the usual share of the jobs they cut in the downturn (the low end) or twice
#                   it (the high end, the case as quoted); the model's largest single lever, so the case is a band;
#   robotics        two years out (her call, 2026-09-24);
#   care            caps out: every region's own ceiling one year of trend above today's share (today's where care is
#                   shrinking: France);
#   the US          tariffs of 25 points from the second simulated quarter (2027Q1), read as the model's symmetric tariff;
#                   today's fiscal response, rescues and benefits; no premium on borrowing since 2026-10-26 (decision 69:
#                   US long rates fell in October; her deficit-worry point a year is an alternative); the corporate
#                   spread's three-month rise already present at the start (decision 47);
#   Europe, Sweden  no tariffs of their own; spending cuts as unemployment rises; the euro area as France and the rest
#                   of the union since 2026-10-27 (decision 70): France's government a point more over the first year on
#                   top of the spread already there at the start, half of it reaching French borrowers, none elsewhere
#                   (decision 71); the ECB capping it (TPI) an alternative;
#   China           the US tariff through its exports to the US; today's response (stimulus);
#   the levers      policy dated, not triggered (decisions 81 and 91): each region's fiscal lever (the US's and China's
#                   stimulus, Europe's and Sweden's cuts) starts the month after its unemployment first reads two
#                   points above its start (acting from the next month, as a trigger did), found by gc.trigger_dates on the case's low end and on its high end; the case's date
#                   is the midpoint of the two, to the month; the same dates in every piece, sensitivity and alternative;
#                   either end's dates are alternatives (lever_dates).
# The energy term (decision 27) is off until its condition is met (dated Brent at least 1.25 times its three-year average
# on a day a bust rule is active); its run is an alternative, on the pass-through measured at the tag paths-pre-signfix.
# The attribution runs take one piece of the case back to the model's central setting at a time; the sensitivities change
# one setting the case does not carry; the alternatives change the bust.
#
# Run from paths/:  ../venv/Scripts/python.exe code/case.py
# Out: results/case.json, figures/fig_case.png

from __future__ import annotations

import json
import os
import sys
from dataclasses import replace

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import global_crash as gc  # noqa: E402
import vintage  # noqa: E402

DT = gc.DT            # the model's step: a month (decision 91)
NQ = 25               # quarterly indices: 2026Q3 (index 0, the start) .. 2032Q3 (24): six years of simulated quarters
N = gc.months(NQ)     # 73 months: index 0 the start (the end of September 2026) .. 72 (the end of September 2032)
START = gc.START
END_2028 = 9          # the quarter index of 2028Q4 (gc.quarter_label(9)): its reading is October-December 2028's average
Q2032Q2 = NQ - 2      # 2032Q2, quoted where a run is at the model's cap by 2032Q3
CAP = 50.0            # the model's ceiling on non-employment (u + out), %
US_TARIFF = 25.0
PIECES = ("bust", "pace", "adoption", "premium", "tariffs", "austerity", "care")
INDEX0_END = "2026-09-30"                # index 0 is measured on data to September (decision 43): what the start reads
                                         # stops here; October's moves belong to index 1, the bust's first month
# the energy term's run (decision 27), on the pass-through measured at the tag paths-pre-signfix (october.json, Brent,
# US PCE 1990Q1-2026Q2, euro-area and Swedish HICP 2000Q1-2026Q2; not refitted): b0, b1, energy's share of spending,
# household consumption over GDP, the spending lost per unit of a higher energy bill (0.8; the US spends half back).
# Measured on quarterly averages: by month the term reads three-month averages (oil_high), whose monthly changes over a
# quarter sum to its average's, and the next quarter's pass-through comes three months later (gc.energy_inflation)
ENERGY = {"US": (0.2308, 0.0986, 0.0385, 0.675, 0.4), "EA": (0.1707, 0.0834, 0.094, 0.52, 0.8),
          "FR": (0.1707, 0.0834, 0.094, 0.52, 0.8), "SE": (0.1425, 0.0148, 0.0781, 0.45, 0.8)}   # France: the euro area's
                                                                                               # (approximate)


def stored():
    """The crash model as stored (results/global_crash.json): the common, the regions, and the presets' dates by region
    (years after index 0's end; None: never)."""
    j = json.load(open(os.path.join(ROOT, "results", "global_crash.json"), encoding="utf-8"))
    dates = {nm: {r: None if d is None else d["years"] for r, d in ds.items()} for nm, ds in j["preset_dates"].items()}
    return gc.Common(**j["common"]), {r: gc.Region(**j["regions"][r]) for r in gc.R}, dates


def logistic_pace(paper: float, seen: float, mid_q: float, width_q: float, n: int = N, dt: float = DT) -> np.ndarray:
    """From `seen` x the paper's pace now to the paper's pace, half the rise by quarter mid_q; by step, each step at its
    end (mid_q and width_q in quarters)."""
    k = np.arange(n) * dt / gc.Q                     # quarters after index 0's end
    w = 1 / (1 + np.exp(-(k - mid_q) / (width_q / 4)))
    w0 = 1 / (1 + np.exp(mid_q / (width_q / 4)))
    return paper * (seen + (1 - seen) * (w - w0) / (1 - w0))


def ramp_to(total: float, quarters: int, n: int = N, dt: float = DT) -> np.ndarray:
    """`total` reached in a straight line over `quarters` quarters from index 0's end, by step."""
    return np.array([total * min(k * dt / (quarters * gc.Q), 1.0) for k in range(n)])


# ------------------------------------------------------------------ the bust
def _q(sid: str, end: bool = False) -> pd.Series:
    s = gc.fred(sid)
    g = s.groupby(s.index.to_period("Q"))
    return g.last() if end else g.mean()


def peak_shift(b: dict) -> float:
    """How much later in its quarter today's peak came than the 2000 peak did in its own (quarters): the 2000-02 path's
    k = 0 is 2000Q1's end, 21 days after the Nasdaq's high of 10 Mar 2000; 2026Q4's end is 86 days after the high of
    6 Oct 2026, so on the peak's own date the path runs about 0.7 of a quarter ahead of the quarter it is read in."""
    q = lambda d: pd.Timestamp(d).to_period("Q").end_time.normalize()  # noqa: E731
    days = lambda d: (q(d) - pd.Timestamp(d)).days  # noqa: E731
    return (days(b["peak"]) - days(b["peak_2000"])) / (365.25 / 4)


def bust_delay(b: dict) -> float:
    """gc.ai_shock's delay for the case's bust, in quarters at any step: its onset quarter, read on the peak's own date
    (peak_shift)."""
    return b["onset"] - 1 - (peak_shift(b) if b.get("peak") else 0.0)


def bust_shock(n: int, b: dict, dt: float = DT) -> gc.Shock:
    """The case's bust: gc.ai_shock at b["scale"] times the 2000-02 bust's measured sizes, on its measured path, dated
    from the peak (bust_delay); with b["ramp"] = (scale, speed), the bust as first built (the 8 Oct case's timing).
    b["held"]: equity never recovers from any low it reaches (a running maximum of the fall); b["no_equity"]: the core
    holds (no fall in household equity; the build-out and the losses only)."""
    if "ramp" in b:
        return gc.ai_shock(n, *b["ramp"], shape="ramp", dt=dt)
    sh = gc.ai_shock(n, b["scale"], delay=bust_delay(b), dt=dt)
    if b.get("held"):
        sh.equity = {r: np.maximum.accumulate(v) for r, v in sh.equity.items()}
    if b.get("no_equity"):
        sh.equity = {r: np.zeros(n) for r in sh.equity}
    return sh


# ------------------------------------------------------------------ the settings
def observed() -> dict:
    """What the vintage says about the pop so far, for the record (case.json `vintage`)."""
    nq = vintage.read("NASDAQCOM")
    q3 = nq[(nq.index >= "2026-07-01") & (nq.index <= "2026-09-30")]
    q4 = nq[nq.index >= "2026-10-01"]
    hi = nq[nq.index >= nq.index[-1] - pd.Timedelta(days=365)]
    br = vintage.read("DCOILBRENTEU")
    days = (nq.index[-1] - hi.idxmax()).days
    h0 = _q2000_daily()
    then = h0[h0.index <= pd.Timestamp("2000-03-10") + pd.Timedelta(days=days)]
    return {"nasdaq_q4_to_date_vs_q3_avg_pct": round(float((q4.mean() / q3.mean() - 1) * 100), 2),
            "nasdaq_off_its_high_pct": round(float((nq.iloc[-1] / hi.max() - 1) * 100), 2),
            "days_after_the_high": days,
            "nasdaq_2000_off_its_high_pct_same_days": round(float((then.iloc[-1] / h0.loc["2000-03-10"] - 1) * 100), 2),
            "nasdaq_high": [f"{hi.idxmax():%Y-%m-%d}", round(float(hi.max()), 2)], "nasdaq_last": f"{nq.index[-1]:%Y-%m-%d}",
            "brent_last5": round(float(br.iloc[-5:].mean()), 2),
            "brent_three_year_average": round(float(br.iloc[-757:-1].mean()), 2) if len(br) > 757 else None,
            "ig_oas_63_print_rise": round(vintage.rise(vintage.read("BAMLC0A0CM")), 3),
            # the premium's test (decision 69): each at the start (the last reading to 30 Sep) and its latest, with its date
            **{k: since(v) for k, v in (("us_10y", "DGS10"), ("us_term_premium_10y", "THREEFYTP10"), ("baa_over_10y", "BAA10Y"))},
            "france_over_germany_10y": since(None)}


def since(sid: str | None) -> list:
    """[at the start, latest, its date]: a vintage series, or (None) France's ten-year yield over Germany's on the days
    both have."""
    s = (vintage.read("FRGVB10Y") - vintage.read("DEGVB10Y")).dropna() if sid is None else vintage.read(sid).dropna()
    return [round(float(s.loc[:INDEX0_END].iloc[-1]), 2), round(float(s.iloc[-1]), 2), f"{s.index[-1]:%Y-%m-%d}"]


def _q2000_daily() -> pd.Series:
    """The Nasdaq composite, daily, from the 2000 high (FRED NASDAQCOM, as cached)."""
    s = gc.fred("NASDAQCOM")
    return s[(s.index >= "2000-03-10") & (s.index <= "2002-12-31")]


def settings(regs, pace_seen: float) -> dict:
    """The case's settings, piece by piece, so that each can be taken back to the model's central setting (the levers'
    dates are set on the case's runs: lever_dates)."""
    # care capped one year of its trend above today's share; a care sector that is shrinking (France) at today's
    care_cap = {r: round(regs[r].care_share + max(regs[r].care_trend, 0.0), 2) for r in gc.R}
    # the US tariff on what each region sells to the US, as a tariff on what it sells outside its union (the model's
    # tariffs spare trade inside the euro area: decision 70), so that its effect on all its exports is 25 x its US share
    inside = lambda r: sum(v for q, v in regs[r].trade.items() if regs[r].union and q in regs and q != r  # noqa: E731
                           and getattr(regs[q], "union", "") == regs[r].union)
    tariff_hit = {"US": US_TARIFF, **{r: round(US_TARIFF * regs[r].trade.get("US", 0.0) / (1 - inside(r)), 2)
                                      for r in ("EA", "FR", "SE", "CN")}}
    return {
        "bust": {"scale": 1.5, "onset": 1, "peak": "2026-10-06", "peak_2000": "2000-03-10",
                 "path": "the 2000-02 bust, measured (global_crash.bust_2000), dated from the peak"},
        "pace": {"seen": pace_seen, "mid_quarter": 7, "width_quarters": 8},
        "adoption_multiple": {"low": 1.0, "high": 2.0},
        "robot_lag_years": 2.0,
        "care_cap": care_cap,
        "tariff": tariff_hit, "tariff_quarter": 2,
        "fiscal": {"US": "stimulus", "EA": "austerity", "FR": "austerity", "SE": "austerity", "CN": "stimulus"},
        # the premium on borrowing (decisions 25, 69, 71): France's government, a point more over the first year, on top
        # of the half point above its calm level already there at the start (half of each reaching French borrowers);
        # none in the US (decision 69) or the rest of the euro area (its spreads did not move)
        "premium": {"US": 0.0, "EA": 0.0, "FR": 1.0, "SE": 0.0, "CN": 0.0}, "premium_quarters": 4,
        "spread0": {"US": round(vintage.rise(vintage.read("BAMLC0A0CM").loc[:INDEX0_END]), 4)},
    }


# the sensitivities: one setting the case does not carry, on the case at its high end
SENSITIVITIES = {
    "fiscal dominance: the US anchor loosens to the eroding rules' 0.6": {"rules": {"US": {"anchor": 0.6}}},
    "fiscal dominance: the US anchor loosens to 0.6 and the Fed tolerates 3% inflation":
        {"rules": {"US": {"anchor": 0.6, "pi_star": 3.0}}},
    "Germany's spending offsets the periphery's cuts: the euro area neither stimulates nor cuts":
        {"rules": {"EA": {"fiscal": "none"}, "FR": {"fiscal": "none"}}},
    "the euro area stimulates": {"rules": {"EA": {"fiscal": "stimulus"}, "FR": {"fiscal": "stimulus"}}},
    "the US exit share at decision 21's proposal (0.36)": {"regions": {"US": {"exit_share": 0.36}}},
    "rates bite harder: a_r 0.079 (Holston-Laubach-Williams, US)": {"common": {"a_r": 0.079}},
    # the fit's debt deflation (slope 0.5, at its bound, levelling off at a shortfall of 11.4%: decision 92) acts wherever
    # the price level runs below the path expected at the region's target (decision 91): how much of the case is its drag
    "no debt deflation: the fit's 0.5 (at its bound) set to 0": {"common": {"debt_deflation": 0.0}},
}
# the alternatives: the bust changed, on the case at its high end (paths for the watcher's vocabulary; not scored)
ALTERNATIVES = {
    "deficit worry priced in the US: a point more on US borrowing over the first year (her leaning; the 8 Oct case's setting)":
        {"premium": {"US": 1.0}},
    "the ECB caps France's spread half a point above its start (the Transmission Protection Instrument)":
        {"rules": {"FR": {"tpi": 0.5}}},
    "France's spread rises two points more over the first year, not one": {"premium": {"FR": 2.0}},
    "the 8 Oct case's timing: equity and the build-out at full size within two quarters from 2026Q4 and held, the losses over 2027":
        {"bust": {"ramp": (1.5, 2.0)}},
    "equity never recovers from any low (a running maximum of the fall; as the bust was first built)": {"bust": {"held": True}},
    "the core holds: no fall in household equity, the build-out and its lenders only": {"bust": {"no_equity": True}},
    "the bust a quarter later (from 2027Q1)": {"bust": {"onset": 2}},
    "the bust dated by its quarter, not the peak's day (k = 0 at 2026Q4's end)": {"bust": {"peak": None}},
    "oil stays high and policy reads four quarters' headline (decision 27's run)": {"energy": True},
    "the levers on the low end's dates (where its unemployment first rose two points), not the midpoint": {"levers": "low"},
    "the levers on the high end's dates (where its unemployment first rose two points), not the midpoint": {"levers": "high"},
}


def oil_high(n: int = N) -> tuple:
    """Decision 27's oil path, "stays high", by month: dated Brent held at its last five prints for four quarters from
    October 2026, a quarter at the geometric midpoint, then its three-year average (the watcher's reference); the months
    to September as measured. Each step reads the average of its three months, as the pass-through was measured on
    quarterly averages (index 0 is 2026Q3's average, index 3 2026Q4's); before index 0, the three months to August. In
    dollars for every region, the exchange rates held (crude enters through its log change)."""
    br = vintage.read("DCOILBRENTEU")
    ma = br.groupby(br.index.to_period("M")).mean()
    hold, avg = float(br.iloc[-5:].mean()), float(br.iloc[-757:-1].mean())
    sep = pd.Period("2026-09", "M")
    price = [float(ma[sep - j]) for j in (3, 2, 1, 0)] + [hold] * 12 + [float(np.sqrt(hold * avg))] * 3 + [avg] * n
    m3 = np.convolve(price, np.ones(3) / 3, "valid")         # m3[i]: the average of months i .. i + 2 (from June)
    return float(m3[0]), m3[1:1 + n]


def setup(cm, regs, st: dict, drop: str | None = None, adoption: str = "high", sens: dict | None = None, n: int = N):
    """The case's run before its levers are dated: (regions, rules, shock, common, waves) for the case, or the case with
    one piece (`drop`) taken back to the model's central setting, or with one sensitivity or alternative (`sens`)."""
    sens = sens or {}
    central = {"adoption_multiple": 1.0}
    b = {**st["bust"], **sens.get("bust", {})}
    shock = gc.ai_shock(n, delay=bust_delay(b), dt=DT) if drop == "bust" else bust_shock(n, b)   # the piece: the size alone
    pace = st["pace"]
    if drop != "pace":
        shock.drift = {r: logistic_pace(regs[r].drift, pace["seen"], pace["mid_quarter"], pace["width_quarters"], n) for r in gc.R}
    if drop != "premium":
        prem = {**st["premium"], **sens.get("premium", {})}
        shock.spread = {r: ramp_to(v, st["premium_quarters"], n) for r, v in prem.items() if v}
    for r, v in st["spread0"].items():                  # present from the start and held (decision 47)
        shock.spread[r] = shock.spread.get(r, np.zeros(n)) + v
        shock.spread0[r] = v
    adopt = central["adoption_multiple"] if drop == "adoption" else st["adoption_multiple"][adoption]
    rg = {r: replace(g, eta=g.eta * adopt, **sens.get("regions", {}).get(r, {})) for r, g in regs.items()}
    react = "core"
    if sens.get("energy"):
        before, path = oil_high(n)
        for r, (b0, b1, w, cons, inc) in ENERGY.items():
            shock.oil[r], shock.oil_before[r] = path, before
            # headline at the start, to the end of 2026Q3; Sweden on core (no headline in the vintage; the October
            # unit added the energy term into 2026Q3, about -0.3, at the tag)
            ph = (vintage.yoy(vintage.read({"US": "PCEPI", "EA": "CP0000EZ19M086NEST", "FR": "FR_HICP"}[r]).loc[:INDEX0_END])
                  if r in ("US", "EA", "FR") else rg[r].pi0)
            rg[r] = replace(rg[r], energy_weight=w, energy_pass=(b0, b1), consumption_share=cons, energy_income=inc, pi_h0=ph)
        react = "headline4"
    rules = {}
    for r in gc.R:
        rl = replace(gc.MODERN, react_to=react if r in ENERGY else "core")
        if drop != "tariffs":
            rl = replace(rl, tariff=st["tariff"][r], tariff_q=st["tariff_quarter"])
        if drop != "austerity":
            rl = replace(rl, fiscal=st["fiscal"][r])
        if drop != "care":
            rl = replace(rl, care_cap=st["care_cap"][r])
        rules[r] = replace(rl, **sens.get("rules", {}).get(r, {}))
    waves = gc.Waves(split=True, robot_lag=st["robot_lag_years"], absorb=True)
    return rg, rules, shock, replace(cm, **sens.get("common", {})), waves


def years(levers: dict, which: str = "case") -> dict:
    """The levers' dates by region, years after index 0's end (None: never), from settings["levers"]."""
    return {r: None if d is None else d["years"] for r, d in levers[which].items()}


def build(cm, regs, st: dict, drop: str | None = None, adoption: str = "high", sens: dict | None = None, n: int = N):
    """The case (setup) with its levers on the case's dates (settings["levers"]; sens["levers"]: either end's), run by
    month."""
    sens = sens or {}
    rg, rules, shock, cm_, waves = setup(cm, regs, st, drop, adoption, sens, n)
    rules = gc.dated(rules, years(st["levers"], sens.get("levers", "case")))
    return rg, gc.simulate(rg, rules, shock, cm_, n, waves=waves, dt=DT)


def lever_dates(cm, regs, st: dict, n: int = N) -> dict:
    """The levers' dates by region (decisions 81 and 91: policy dated, not triggered): gc.trigger_dates on the case's
    low end and on its high end (from the month after each region's unemployment first reads its rules' trigger, two
    points, above its start, the earlier responses' spillovers counted, as the triggered model started them), and the case's the
    midpoint of the two to the month (a half to the later month; where only one end reaches the trigger, that end's).
    Each {years after index 0's end, the month the lever starts in} or None (never)."""
    ends = {}
    for end in ("low", "high"):
        rg, rules, shock, cm_, waves = setup(cm, regs, st, adoption=end, n=n)
        ends[end] = gc.trigger_dates(rg, rules, shock, cm_, n, DT, waves)
    mid = {}
    for r in gc.R:
        d = [ends[e][r] for e in ("low", "high") if ends[e][r] is not None]
        mid[r] = None if not d else int(np.floor(sum(d) / len(d) / DT + 0.5)) * DT
    stamp = lambda ds: {r: None if d is None else {"years": d, "from": gc.month_label(round(d / DT) + 1)}  # noqa: E731
                        for r, d in ds.items()}
    return {"trigger": gc.MODERN.trigger, "low": stamp(ends["low"]), "high": stamp(ends["high"]), "case": stamp(mid),
            "note": "the month each region's fiscal lever starts: the month after its unemployment first reads two points "
                    "above its start in the case's low end and in its high end (gc.trigger_dates), the case's the midpoint to the "
                    "month; the same dates in every piece, sensitivity and alternative"}


def reference(cm, regs, dates: dict, n: int = N):
    """The model's central run: today's policies on their stored dates (preset_dates' "modern rules"), a dot-com-sized
    bust (ai_shock's default), the paper's pace, robotics in two years — the website's model page default (watch
    web/case.py checks they are the same path)."""
    return regs, gc.simulate(regs, gc.dated(gc.MODERN, dates["modern rules"]), gc.ai_shock(n, dt=DT), cm, n,
                             waves=gc.CENTRAL_WAVES, dt=DT)


# ------------------------------------------------------------------ readouts
def four(rg, o) -> np.ndarray:
    size = {r: rg[r].size for r in gc.R}
    return np.array([sum(size[r] * o[r]["y"][k] for r in gc.R) / sum(size.values()) for k in range(len(o["US"]["y"]))])


def out_of_work(o, r: str = "US") -> np.ndarray:
    """Region r's unemployed plus those who left the workforce, %, by quarter (its months' averages)."""
    return gc.to_quarters(o[r]["u"] + o[r]["out"], DT)


def read(rg, o) -> dict:
    """A monthly run's readings, each on quarterly averages (gc.to_quarters); the model's cap on the monthly path."""
    q = gc.quarterly_out(o, DT)
    f = four(rg, q)
    us = q["US"]
    oow = us["u"] + us["out"]
    k = int(np.argmax(oow))
    # the quarter of the first month a region's out of work is at the cap
    capped = lambda r: next((gc.quarter_label(-(-j // 3)) for j, v in enumerate(o[r]["u"] + o[r]["out"])  # noqa: E731
                             if v >= CAP - 1e-9), None)
    res = {"four_output_worst": round(float(f.min()), 1), "four_output_worst_year": round(float(f.argmin()) / 4, 2),
           "four_output_end_2028": round(float(f[END_2028]), 1),
           "us_out_of_work_peak": round(float(oow.max()), 1), "us_out_of_work_peak_year": round(k / 4, 2),
           "us_unemployment_at_peak": round(float(us["u"][k]), 1), "us_left_at_peak": round(float(us["out"][k]), 1),
           "us_out_of_work_2026Q4": round(float(oow[1]), 2), "us_unemployment_2026Q4": round(float(us["u"][1]), 2),
           "us_out_of_work_end_2028": round(float(oow[END_2028]), 1),
           "us_output_end_2028": round(float(us["y"][END_2028]), 1),
           "us_out_of_work_2032Q2": round(float(oow[Q2032Q2]), 1),
           "us_at_the_models_cap_from": capped("US"),
           "still_rising_at_end": bool(oow[-1] > oow[-2]),
           "regions": {}}
    for r in gc.R:
        x = q[r]
        res["regions"][r] = {"output_worst": round(float(x["y"].min()), 1),
                             "out_of_work_peak": round(float((x["u"] + x["out"]).max()), 1),
                             "out_of_work_end_2028": round(float((x["u"] + x["out"])[END_2028]), 1),
                             "at_the_models_cap_from": capped(r),
                             "unemployment_peak": round(float(x["u"].max()), 1),
                             "bank_capital_lost_max_pct": round(float(x["stress"].max()) * 100),
                             "inflation_min": round(float(x["pi"].min()), 1), "inflation_max": round(float(x["pi"].max()), 1),
                             "policy_rate_min": round(float(x["i"].min()), 2),
                             "policy_rate_2026Q4": round(float(x["i"][1]), 2),
                             "credit_spread_max": round(float(x["s"].max()), 2),
                             "care_end": round(float(x["care"][-1]), 1),
                             # debt deflation (the fit's slope 0.5, levelling off at a shortfall of 11.4%: decision 92):
                             # the largest drag on demand while the price level runs below the path expected at the
                             # target, % of GDP
                             "debt_deflation_drag_max_pct_gdp": round(max(0.0, -float(x["d_debt"].min())), 2)}
    res["verdict"] = verdict(float(f.min()), float(oow.max()))      # on the unrounded readings
    return res


def paths(rg, o) -> dict:
    """The run's paths by month (index 0 the start, index k the end of the k-th month)."""
    out = {"four_output": [round(float(v), 2) for v in four(rg, o)]}
    for r in gc.R:
        x = o[r]
        out[r] = {k: [round(float(v), 2) for v in arr] for k, arr in
                  (("out_of_work", x["u"] + x["out"]), ("unemployment", x["u"]), ("left_workforce", x["out"]),
                   ("output", x["y"]), ("inflation", x["pi"]), ("rate", x["i"]), ("spread", x["s"]),
                   ("capital_lost", x["stress"] * 100), ("care", x["care"]))}
    return out


def verdict(four_worst: float, us_peak: float) -> str:
    """The run's name, from the four economies' worst output against capacity and the US out-of-work peak (%, both on
    quarterly averages), read unrounded: a run on a line is named by where it is, not by its rounding (since
    2026-10-28: the high end's -19.99 read as the rounded -20.0 named it a depression)."""
    if four_worst <= -20:
        return "a depression"
    if us_peak >= 15:
        return "a labour depression, output held" if four_worst > -10 else "a labour depression"
    if four_worst <= -4:
        return "a 2008-scale recession"
    return "a recession" if four_worst <= -2 else "a slowdown"


def short(x: dict) -> dict:
    return {"us_out_of_work_end_2028": x["us_out_of_work_end_2028"], "us_out_of_work_peak": x["us_out_of_work_peak"],
            "us_out_of_work_2032Q2": x["us_out_of_work_2032Q2"], "us_at_the_models_cap_from": x["us_at_the_models_cap_from"],
            "four_output_worst": x["four_output_worst"], "ea_out_of_work_peak": x["regions"]["EA"]["out_of_work_peak"],
            "fr_out_of_work_peak": x["regions"]["FR"]["out_of_work_peak"],
            "se_out_of_work_peak": x["regions"]["SE"]["out_of_work_peak"],
            "us_inflation_min": x["regions"]["US"]["inflation_min"], "us_inflation_max": x["regions"]["US"]["inflation_max"]}


def sahm(u: np.ndarray) -> np.ndarray:
    """The Sahm rule by month, as the watcher reads it (watch/tripwires.sahm): the three-month average unemployment rate
    less its lowest over the twelve months before, on the model's US path (index 0, September 2026, the vintage's
    reading) after the vintage's fourteen readings before it."""
    h = vintage.read("UNRATE").loc[:INDEX0_END].dropna()
    x = np.concatenate([h.values[-15:-1], u])
    a = np.convolve(x, np.ones(3) / 3, "valid")                  # a[j]: readings j .. j + 2 of x
    return np.array([a[m + 12] - a[m:m + 12].min() for m in range(len(u))])


def signals(o, shock, onset: float, st_peak: str, scale: float) -> dict:
    """The case's high end against the watcher's rules, by month. bust.us.equity (the Nasdaq 20% under its 52-week high,
    daily): on the 2000 Nasdaq's own daily path from its high (10 Mar 2000), the day its drawdown, times the case's
    scale, first reaches 20%, counted from the 2026 high (6 Oct) — the reading the case's own dating implies; beside it
    two late bounds by month (the model's fall in household equity at a month's end read as the Nasdaq's on the 2000-02
    ratio of the two falls at the nearest quarter from the peak, 1.6 to 3.85 then, and one for one). labour.us.sahm: the
    watcher's Sahm rule on the model's monthly US unemployment, after the measured months (sahm). bust.credit.baa (Baa over the ten-year Treasury up 0.56 in 63 days): the model's US spread up 0.56 in
    three months; the spread is fitted to Moody's Baa over Aaa by month in the US episodes (decision 90), not to the
    rule's Baa over the Treasury, which moves with the Treasury's term premium too."""
    nq = _q("NASDAQCOM", end=True)
    eq_meas = gc.bust_2000()["measured"]["equity_fall"]
    ratio = [float((1 - nq[gc.Q0_2000 + k] / nq[gc.Q0_2000]) / eq_meas[k]) if eq_meas[k] > 0.03 else None
             for k in range(len(eq_meas))]
    eq = shock.equity["US"]
    first = lambda cond: next((gc.month_label(m) for m in range(len(eq)) if cond(m)), None)  # noqa: E731
    u = o["US"]["u"]
    s = o["US"]["s"]
    L = gc.quarter_steps(DT)

    def rk(m):
        """The 2000-02 ratio at month m: the nearest quarter of the measured path (onset in quarters)."""
        j = int(round(m * DT / gc.Q - onset))
        return ratio[j] if 0 <= j < len(ratio) and ratio[j] else None
    h0 = _q2000_daily()
    dd = 1 - h0 / h0.cummax()                         # the drawdown from the high to date (the high is 10 Mar 2000)
    day = lambda scale: int((dd[scale * dd >= 0.20].index[0] - pd.Timestamp("2000-03-10")).days)  # noqa: E731
    peak = pd.Timestamp(st_peak)
    sa = sahm(u)
    return {"bust.us.equity, on the 2000 Nasdaq's daily path": {
                "days_after_the_high_at_the_dot_com_size": day(1.0), "days_after_the_high_at_the_case_size": day(scale),
                "dates_from_the_2026_high": [f"{peak + pd.Timedelta(days=day(scale)):%Y-%m-%d}",
                                             f"{peak + pd.Timedelta(days=day(1.0)):%Y-%m-%d}"]},
            "bust.us.equity, by month, the 2000-02 ratio (a late bound)": first(lambda m: rk(m) is not None and rk(m) * eq[m] >= 0.20),
            "bust.us.equity, by month, one for one (a late bound)": first(lambda m: eq[m] >= 0.20),
            "labour.us.sahm": first(lambda m: m >= 1 and sa[m] >= 0.5),
            "bust.credit.baa (the model's spread, fitted to Baa over Aaa)": first(lambda m: m >= L and s[m] - s[m - L] >= 0.56),
            "nasdaq_over_household_equity_2000_02_by_quarter": [None if x is None else round(x, 2) for x in ratio[:17]]}


def run_all(cm, regs, pdates, st) -> dict:
    ends = {}
    for end in ("low", "high"):
        ends[end] = read(*build(cm, regs, st, adoption=end))
    ref = read(*reference(cm, regs, pdates))
    _, o_hi = build(cm, regs, st)
    q_hi = gc.quarterly_out(o_hi, DT)
    oow_hi = out_of_work(o_hi)
    drops = {}
    for d in PIECES:
        rg_d, o_d = build(cm, regs, st, d)
        x = short(read(rg_d, o_d))
        q_d = gc.quarterly_out(o_d, DT)
        oow = out_of_work(o_d)
        # each 'adds' is the difference of the unrounded runs' quarterly readings, rounded once
        x.update({"adds_to_us_out_of_work": round(float(oow_hi.max() - oow.max()), 1),
                  "adds_to_us_out_of_work_end_2028": round(float(oow_hi[END_2028] - oow[END_2028]), 1),
                  "adds_to_us_out_of_work_2032Q2": round(float(oow_hi[Q2032Q2] - oow[Q2032Q2]), 1),
                  "adds_to_four_output": round(float(four(regs, q_hi).min() - four(rg_d, q_d).min()), 1),
                  "adds_to_ea_out_of_work": round(float(out_of_work(o_hi, "EA").max() - out_of_work(o_d, "EA").max()), 1),
                  "adds_to_fr_out_of_work": round(float(out_of_work(o_hi, "FR").max() - out_of_work(o_d, "FR").max()), 1),
                  "adds_to_se_out_of_work": round(float(out_of_work(o_hi, "SE").max() - out_of_work(o_d, "SE").max()), 1)})
        drops[d] = x
    ea_hi, fr_hi = out_of_work(o_hi, "EA"), out_of_work(o_hi, "FR")
    sens = {}
    for name, s in SENSITIVITIES.items():
        rg_s, o_s = build(cm, regs, st, sens=s)
        x = short(read(rg_s, o_s))
        oow = out_of_work(o_s)
        # differences of the unrounded runs, rounded once (as the pieces)
        x["change_in_us_out_of_work"] = round(float(oow.max() - oow_hi.max()), 1)
        x["change_in_us_out_of_work_2032Q2"] = round(float(oow[Q2032Q2] - oow_hi[Q2032Q2]), 1)
        x["change_in_four_output"] = round(float(four(rg_s, gc.quarterly_out(o_s, DT)).min() - four(regs, q_hi).min()), 1)
        x["change_in_ea_out_of_work"] = round(float(out_of_work(o_s, "EA").max() - ea_hi.max()), 1)
        x["change_in_fr_out_of_work"] = round(float(out_of_work(o_s, "FR").max() - fr_hi.max()), 1)
        sens[name] = x
    alts = {}
    for name, s in ALTERNATIVES.items():
        rg_a, o_a = build(cm, regs, st, sens=s)
        x = short(read(rg_a, o_a))
        q_a = gc.quarterly_out(o_a, DT)
        oow = out_of_work(o_a)
        x["us_out_of_work_2026Q4"] = round(float(oow[1]), 2)
        x["us_unemployment_2026Q4"] = round(float(q_a["US"]["u"][1]), 2)
        x["us_out_of_work_2027Q3"] = round(float(oow[4]), 1)
        x["change_in_us_out_of_work_end_2028"] = round(float(oow[END_2028] - oow_hi[END_2028]), 1)
        x["change_in_us_out_of_work_2032Q2"] = round(float(oow[Q2032Q2] - oow_hi[Q2032Q2]), 1)
        x["us_policy_rate_2026Q4"] = round(float(q_a["US"]["i"][1]), 2)
        alts[name] = x
    return {"case": ends, "reference_central_run": ref,
            "piece_by_piece": {"note": "each row takes one piece of the case (at its high end) back to the model's central "
                                       "setting, the levers on the case's dates; 'adds' is the case minus that run, the "
                                       "difference of the unrounded runs' quarterly averages rounded once: at 2028Q4, at "
                                       "2032Q2, and at the peak (2032Q3 while still rising)", **drops},
            "sensitivities": {"note": "each changes one setting the case does not carry, on the case at its high end, the "
                                      "levers on the case's dates; at the peak and at 2032Q2", **sens},
            "alternatives": {"note": "each changes the bust (or switches decision 27's energy term on, or puts the levers "
                                     "on either end's dates), on the case at its high end; paths for the watcher's "
                                     "vocabulary, not scored", **alts}}


def main():
    cm, regs, pdates = stored()
    pace = json.load(open(os.path.join(ROOT, "results", "pace.json"), encoding="utf-8"))
    seen = pace["paces"]["multiples_of_the_papers"]["trend + 2 s.e."]
    st = settings(regs, seen)
    st["levers"] = lever_dates(cm, regs, st)
    bp = gc.bust_2000()
    rg_h, o_h = build(cm, regs, st)
    shock_h = bust_shock(N, st["bust"])
    eq_us = shock_h.equity["US"]
    eq_q = gc.to_quarters(eq_us, DT)
    qlab = lambda m: gc.quarter_label(-(-m // 3))      # the quarter month m falls in  # noqa: E731
    man = vintage.manifest()
    res = {"start": START, "step": "month", "steps": N, "quarters": NQ,
           "dating": f"index 0 = the end of {gc.month_label(0)} ({gc.quarter_label(0)}), the state measured on data to "
                     f"September 2026; index k = the end of the k-th month after (index 1 = {gc.month_label(1)}, the first "
                     f"simulated month); index {N - 1} = {gc.month_label(N - 1)}. A reading named by a quarter is its "
                     f"months' average (gc.to_quarters): quarter 1 = {gc.quarter_label(1)}, the first simulated quarter; "
                     f"quarter {END_2028} = {gc.quarter_label(END_2028)}; quarter {NQ - 1} = {gc.quarter_label(NQ - 1)} "
                     f"(decisions 43 and 91)",
           "vintage": {"date": man["vintage"], "built_utc": man["built_utc"], "watcher_state_commit": man["watcher_state_commit"],
                       "last_observations": {k: v["last"] for k, v in man["series"].items()}, "observed": observed()},
           "settings": st,
           "bust_path": {"from_the_2000_02_bust": {k: [round(float(x), 4) for x in bp[k]] for k in ("equity", "capex", "losses")},
                         "measured": {"equity_trough_fall_2000_02": round(float(bp["measured"]["equity_fall"][:17].max()), 3),
                                      "equity_trough_quarters_after_the_peak": int(np.argmax(bp["equity"])),
                                      "capex_trough_quarters_after_the_peak": int(np.argmax(bp["capex"])),
                                      "losses_peak_quarters_after_the_peak": int(np.argmax(bp["losses"])),
                                      "capex_excess_2000Q1_pts_of_gdp": round(bp["measured"]["capex_excess_2000Q1"], 2),
                                      "chargeoff_base_1997_99": round(bp["measured"]["chargeoff_base_1997_99"], 3)},
                         "us_equity_fall": [round(float(x), 4) for x in eq_us]},
           # by quarter (the quarterly averages; the levers by month)
           "dates": {"bust_onset": gc.quarter_label(st["bust"]["onset"]), "peak": st["bust"]["peak"],
                     "peak_shift_quarters": round(peak_shift(st["bust"]), 3),
                     "equity_first_falls": gc.quarter_label(int(np.argmax(eq_q > 0))),
                     "equity_trough": gc.quarter_label(int(np.argmax(eq_q))),
                     "losses_peak": gc.quarter_label(int(np.argmax(gc.to_quarters(shock_h.losses["US"], DT)))),
                     "build_out_last_above_its_start": gc.quarter_label(int(np.flatnonzero(gc.to_quarters(shock_h.capex["EA"], DT) < 0).max())),
                     "tariffs": gc.quarter_label(st["tariff_quarter"]),
                     "premium_builds": f"{gc.quarter_label(1)}-{gc.quarter_label(st['premium_quarters'])}",
                     "pace_half_way": gc.quarter_label(st["pace"]["mid_quarter"]),
                     "robotics_begins": qlab(next(m for m in range(N) if gc.robots(m, gc.Waves(split=True, robot_lag=st["robot_lag_years"]), DT) > 0)),
                     "levers_from": {r: None if d is None else d["from"] for r, d in st["levers"]["case"].items()}},
           **run_all(cm, regs, pdates, st),
           "signals": signals(o_h, shock_h, 1 + bust_delay(st["bust"]), st["bust"]["peak"], st["bust"]["scale"]),
           "paths": {end: paths(*build(cm, regs, st, adoption=end)) for end in ("low", "high")}}
    res["paths"]["reference"] = paths(*reference(cm, regs, pdates))
    json.dump(res, open(os.path.join(ROOT, "results", "case.json"), "w", encoding="utf-8"), indent=1)
    print(json.dumps({k: v for k, v in res.items() if k not in ("paths", "bust_path")}, indent=1))
    figure(res)


def figure(res):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams["axes.titlesize"] = 10
    p0 = pd.Period(START, "Q")
    t0 = p0.year + p0.quarter / 4                  # index 0: the end of the start's quarter, in years (2026.75)
    t = t0 + np.arange(N) * DT                     # each month at its end
    lo, hi, ref = res["paths"]["low"], res["paths"]["high"], res["paths"]["reference"]
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.6), layout="constrained")
    fig.get_layout_engine().set(rect=(0, 0.11, 1, 0.89))
    cols = {"US": "C0", "EA": "C1", "FR": "C4", "SE": "C2", "CN": "C3"}
    q28 = t0 + (END_2028 - 1) * gc.Q               # 2028Q4's months
    for a, key, title in ((ax[0], "out_of_work", "1. Out of work (unemployed + left the workforce), %"),
                          (ax[1], "output", "2. Output against capacity, %")):
        for r in gc.R:
            a.fill_between(t, lo[r][key], hi[r][key], color=cols[r], alpha=0.25, lw=0)
            a.plot(t, hi[r][key], color=cols[r], label=r)
            a.plot(t, lo[r][key], color=cols[r], lw=0.8)
        a.plot(t, ref["US"][key], color="C0", ls=":", label="US, the model's central run")
        a.axvspan(q28, q28 + gc.Q, color="grey", alpha=0.15, lw=0)
        a.set_title(title); a.legend(fontsize=8)
    lv = res["settings"]["levers"]["case"]
    for r in gc.R:                                 # each region's lever, from its month (at the panel's foot)
        if lv[r] is not None:
            ax[0].plot(t0 + lv[r]["years"], 0.03, marker="^", color=cols[r], ms=7, transform=ax[0].get_xaxis_transform())
    ax[1].axhline(0, color="grey", lw=0.8)
    a = ax[2]
    a.plot(t, [100 * x for x in res["bust_path"]["us_equity_fall"]], color="C0", label="US household equity, fall from the start, %")
    for r in gc.R:
        a.plot(t, hi[r]["spread"], color=cols[r], ls="--", lw=0.9, label=f"{r} credit spread, points" if r == "US" else None)
    a.set_title("3. The bust's path (equity) and the credit spread (high end)"); a.legend(fontsize=8)
    when = ", ".join(f"{r} {lv[r]['from']}" for r in gc.R if lv[r] is not None)
    fig.text(0.01, 0.01, "Her case, by month: a bust 1.5x the dot-com size on the 2000-02 bust's measured path from the quarter "
             "of today's peak (2026Q4); displacement rising from the pace seen so far to the paper's by 2029; care capping out;\n"
             "US tariffs 25 points; spending cuts in Europe and Sweden; France's government spread a point higher over the "
             "first year (half reaching French borrowers).\n"
             f"The fiscal levers from their months (triangles: {when}). Bands: firms automate the usual share of the jobs "
             "they cut in the downturn (lower line) or twice it (upper line).\nIndex 0 = the end of September 2026, the start "
             "measured to September 2026 (a dated vintage); shaded: 2028Q4, whose average the case quotes.", fontsize=8)
    p = os.path.join(ROOT, "figures", "fig_case.png"); fig.savefig(p, dpi=150); print(p)


if __name__ == "__main__":
    main()
