# episodes.py — the history the crash model is fitted on and checked against, by month (decision 82, her call of
# 2026-10-27: "refit monthly, with policy dated in the model instead of triggers, matching each target at the frequency
# it is measured. Keep the dot-com bust as the held-out check, and add the crashes you listed").
#
# Each episode is the model's machinery (global_crash.simulate at a monthly step, decision 80) on the economy of the
# time, with its measured shocks and its policy dated to what governments did (decision 81), and its targets compared
# with the model at the frequency each is measured: a monthly series month by month, a quarterly one against the
# model's three months, an annual one against twelve. Each series counts by its years (a squared error weighs one over
# its observations a year), so a monthly series counts no more than an annual one over the same span.
#
# The inputs are monthly where they are measured monthly (the Dow-Jones index for 1929-33, the NBER's), and read between
# measured points in time where not (household equity at each quarter's end, Fed Z.1; a quarter's average placed in its
# middle month), as stated by each episode.
#
# The episodes (decision 82's list): the US 1929-33, 1937-38, 1973-75, 1981-82, 1990-91 and 2008-10, Sweden 1990-93,
# the euro area 2011-13, Japan 1991-95; the dot-com bust (2000-03) held out. On the model extended for them (decisions
# 84-88, her call of 2026-10-27: "Extend the model first ... Then fit all the crashes"): rate-sensitive spending, relief
# from the rate debts paid before the start, oil's effect on capacity, expectations on the past year's inflation, and
# each era's neutral rate (the New York Fed's HLW estimates where they exist). Abroad, each economy is one region, its
# central bank's rate as set, its fiscal stance the OECD's measured underlying primary balance (decision 89).
#
# Run from paths/:  ../venv/Scripts/python.exe code/episodes.py     (fits the model: results/episodes.json, figures/fig_episodes.png)

from __future__ import annotations

import functools
import json
import os
import sys
from dataclasses import dataclass, field, replace

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import global_crash as gc  # noqa: E402

M = 1 / 12            # the step: a month
YEAR = 365.25


def years_after(start: str, day: str) -> float:
    """Years from the end of month `start` ('1929-09', index 0's end) to the day `day`: a lever's date (decision 81)."""
    end = pd.Period(start, "M").end_time.normalize()
    return (pd.Timestamp(day) - end).days / YEAR


@dataclass
class Target:
    """A measured series the model is compared with: `model` names the model's series (see Episode.series); `freq` is
    the data's frequency ("M", "Q" or "Y"); `points` [(period, value)] with periods as pandas Periods of that frequency;
    `scale` the error that counts as one standard error."""
    name: str
    model: str
    freq: str
    points: list
    scale: float


@dataclass
class Episode:
    name: str
    start: str                       # index 0's month ('1929-09': the state at its end)
    months: int                      # steps simulated after index 0
    regions: dict
    rules: dict
    shock: gc.Shock
    targets: list
    fitted: bool = True
    active: list = field(default_factory=lambda: ["US"])
    region: str = "US"
    before: dict = field(default_factory=dict)    # the price level before index 0, by month offset (twelve-month inflation)
    notes: str = ""

    def months_index(self) -> list:
        p0 = pd.Period(self.start, "M")
        return [p0 + k for k in range(self.months + 1)]

    def run(self, cm: gc.Common) -> dict:
        """The model on the episode. The rest of the world's slump is measured (each episode's exports), so the model's own
        trade channel is off: with the other regions passive, its 'rest of the world' (the regions' size-weighted gap)
        is the episode's own economy at size 1, and read the region's slump back to it as its partners' (in Sweden's
        1990-93, exports 30% of GDP, it multiplied the slump about 2.2 times; in 1929-33 and 2008-10 it fed back 0.07
        and 0.16 of the gap; found 2026-10-27). The tariffs' export loss is in the measured exports too (retaliation
        included), so the region's exports are zero for the model's tariff term, whose net effect would count it again;
        what that term nets out, the switch from imports to home goods, enters 1929-33 as a dated input (e1929). The
        shared risk mood is off for the same reason as trade: the four economies' size-weighted bank stress is the
        episode's own at size 1, which added the mood's coefficient to the fitted spread per unit of capital lost
        (decision 90)."""
        regions = {**self.regions, self.region: replace(self.regions[self.region], trade={}, exports=0.0)}
        return gc.simulate(regions, self.rules, self.shock, replace(cm, global_mood=0.0), self.months + 1,
                           active=self.active, dt=M)[self.region]

    def series(self, o: dict, name: str) -> np.ndarray:
        """The model's series by month: u, the gap y, the price level P relative to index 0, output relative to index 0
        on a 2% trend ("output"), twelve-month inflation ("yoy", the months before index 0 from the data)."""
        if name == "output":
            return (1 + o["y"] / 100) * 1.02 ** (np.arange(len(o["y"])) * M)
        if name == "yoy":
            P = o["P"]
            past = lambda j: P[j] if j >= 0 else self.before[j]  # noqa: E731
            return np.array([(P[k] / past(k - 12) - 1) * 100 for k in range(len(P))])
        return o[name]

    def where(self) -> list:
        """Each target point's months in the run (built once): the model is averaged over them."""
        if getattr(self, "_where", None) is None:
            months = self.months_index()
            self._where = []
            for t in self.targets:
                for per, val in t.points:
                    ks = [k for k, m in enumerate(months) if (m.asfreq(t.freq) if t.freq != "M" else m) == per]
                    if len(ks) != {"M": 1, "Q": 3, "Y": 12}[t.freq]:
                        raise ValueError(f"{self.name} {t.name}: {per} not covered whole by the run")
                    self._where.append((t, per, np.array(ks), float(val)))
        return self._where

    def compare(self, o: dict) -> list:
        """(target, period, model, data) for every point, the model taken at the data's frequency."""
        xs = {}
        out = []
        for t, per, ks, val in self.where():
            if t.model not in xs:
                xs[t.model] = self.series(o, t.model)
            out.append((t, per, float(np.mean(xs[t.model][ks])), val))
        return out

    def errors(self, o: dict) -> np.ndarray:
        """Standardised errors, each weighted so that a series counts by its years."""
        per_year = {"M": 12, "Q": 4, "Y": 1}
        return np.array([(m - d) / t.scale / np.sqrt(per_year[t.freq]) for t, _, m, d in self.compare(o)])


# ------------------------------------------------------------------ data
def monthly(sid: str) -> pd.Series:
    s = gc.fred(sid)
    return s.groupby(s.index.to_period("M")).mean()


def quarterly(sid: str, end: bool = False) -> pd.Series:
    s = gc.fred(sid)
    g = s.groupby(s.index.to_period("Q"))
    return g.last() if end else g.mean()


def year_before(rate: pd.Series, start: str) -> float:
    """A monthly policy rate's average over the year to the end of month `start` (Region.i_norm: the rate floating-rate
    debt was paying at the start, repricing within a year; decision 85)."""
    p0 = pd.Period(start, "M")
    return float(np.mean([rate[p0 - j] for j in range(12)]))


HLW = os.path.join(gc.ROOT, "cache", "fed", "Holston_Laubach_Williams_current_estimates.xlsx")
HLW_URL = ("https://www.newyorkfed.org/medialibrary/media/research/economists/williams/data/"
           "Holston_Laubach_Williams_current_estimates.xlsx")


@functools.lru_cache(maxsize=None)
def hlw() -> pd.DataFrame:
    """The natural rate of interest by quarter, % (Holston, Laubach and Williams, the New York Fed's current estimates,
    one-sided; final data point 2026Q2): columns US and EA (the euro area, from 1972)."""
    if not os.path.exists(HLW):
        import requests
        r = requests.get(HLW_URL, timeout=60)
        r.raise_for_status()
        open(HLW, "wb").write(r.content)
    df = pd.read_excel(HLW, sheet_name="HLW Estimates", header=None, skiprows=6)
    df = df[[0, 10, 12]].dropna(subset=[0])
    df.columns = ["date", "US", "EA"]
    return df.set_index(pd.PeriodIndex(pd.to_datetime(df["date"]), freq="Q"))[["US", "EA"]].astype(float)


def r_star(area: str, start: str) -> float:
    """The era's neutral real rate for an episode starting at the end of month `start` (decision 88): HLW's estimate for
    the start's quarter, as it read before the episode (the one-sided estimate falls within a slump, reading part of it as
    a lower neutral rate; the start's value is kept through the episode)."""
    return float(hlw().loc[pd.Period(start, "M").asfreq("Q"), area])


def at_quarter_ends(q: pd.Series, start: str, n: int) -> np.ndarray:
    """A quarter-end level read at each month's end from index 0, linearly between quarter ends (held beyond them)."""
    months = [pd.Period(start, "M") + k for k in range(n)]
    xs = [p.to_timestamp(how="end").normalize().value for p in q.index]
    return np.interp([m.to_timestamp(how="end").normalize().value for m in months], xs, q.values)


def at_mid_quarter(q: pd.Series, start: str, n: int) -> np.ndarray:
    """A quarter's average placed in its middle month and read at each month from index 0, linearly between."""
    months = [pd.Period(start, "M") + k for k in range(n)]
    xs = [(p.asfreq("M", "start") + 1).ordinal for p in q.index]
    return np.interp([m.ordinal for m in months], xs, q.values)


def spread_target(start: str, n: int) -> Target:
    """The credit spread, measured (decision 90): Moody's seasoned Baa corporate yield over Aaa (FRED BAA, AAA, monthly
    averages from 1919), its change from the month of the start, against the model's credit spread (s, which starts at
    zero) by month; one standard error is half a point (set before the fit). The US only: no series abroad."""
    p0 = pd.Period(start, "M")
    sp = monthly("BAA") - monthly("AAA")
    return Target("credit spread", "s", "M", [(p0 + k, float(sp[p0 + k] - sp[p0])) for k in range(1, n + 1)], 0.5)


# ------------------------------------------------------------------ 1929-33
LEBERGOTT = gc.LEBERGOTT


def conf_profile(n: int) -> np.ndarray:
    """The post-crash spending collapse per point of its size: full for the first half-year, gone two years later."""
    t = np.arange(n + 1) * M
    return np.array([max(0.0, 1 - max(x - 0.5, 0) / 2.0) if k >= 1 else 0.0 for k, x in enumerate(t)])


def bank_runs(start: str, n: int) -> np.ndarray:
    """The bank runs of 1930-33, measured (decision 92): the money stock's fall from the month of the start (commercial
    banks' deposits plus currency held by the public, Friedman and Schwartz's, seasonally adjusted, monthly: NBER
    macrohistory, FRED M1444AUSM027SNBR), over its largest fall in the episode (35.8%, April 1933), so that the trough
    reads as all the banks' capital lost, where the model's own stress stands by then. The money channel reads it in
    place of the model's stress (which rises in a straight line from the crash, the money stock late and in steps:
    a seventh of its fall by December 1930, half by December 1931, three-quarters by August 1932, the last quarter in
    the 1933 panic and holiday, February to April)."""
    p0 = pd.Period(start, "M")
    m = monthly("M1444AUSM027SNBR")
    lost = np.array([max(0.0, 1 - float(m[p0 + k]) / float(m[p0])) for k in range(n + 1)])
    return lost / lost.max()


def us_1929(okun: float) -> gc.Region:
    return gc.us_1929(okun)


def e1929(okun: float, impulse: float) -> Episode:
    """The US, September 1929 to December 1933, with the 1930s' rules (gold-standard policy, no deposit insurance, no
    support, no rescues) dated as they came: Smoot-Hawley signed 17 June 1930 (15 points), the Fed's defence of gold in
    October 1931 (the discount rate from 1.5% to 3.5% on 9 and 16 October), the Revenue Act signed 6 June 1932 (the
    consolidation). Measured, monthly: the Dow-Jones index's fall from September 1929 (NBER macrohistory, FRED
    M1109BUSM293NNBR; −87% by June 1932). The rest of the world's slump: US real exports against 1929, % of 1929 GDP
    (FRED EXPGSCA / GDPCA), annual values placed mid-year and read by month. The post-crash collapse of spending on
    durables and building (Romer 1990) as a demand level fading over two years from the first half-year: its size is
    fitted. The bank runs measured, by month (bank_runs: the money stock's fall), as the money channel's driver.
    Smoot-Hawley's switch from imports to home goods from its date, (1 - tariff_net) x the tariff x exports'
    share of GDP (the model's own split of a tariff; its export loss is in the measured exports). Targets: annual output
    (FRED GDPCA, against the model's year on a 2% trend) and unemployment (Lebergott, the standard series) for 1930-33;
    the consumer price level by month (FRED CPIAUCNS, against September 1929); the credit spread by month
    (spread_target)."""
    start, n = "1929-09", 51
    t = np.arange(n + 1) * M
    dow = monthly("M1109BUSM293NNBR")
    p0 = pd.Period(start, "M")
    eq = np.array([max(0.0, 1 - float(dow[p0 + k]) / float(dow[p0])) for k in range(n + 1)])
    conf = -impulse * conf_profile(n)
    e, g = gc.fred("EXPGSCA"), gc.fred("GDPCA")
    ex = {d.year: float((e[d] - e.iloc[0]) / g.iloc[0] * 100) for d in e.index if d.year <= 1934}
    exm = np.interp(1929.75 + t, [y + 0.5 for y in sorted(ex)], [ex[y] for y in sorted(ex)])
    regs = {"US": us_1929(okun), "EA": gc.passive("EA"), "SE": gc.passive("SE"), "CN": gc.passive("CN")}
    rl = replace(gc.THIRTIES, gold_hike=((9, 2.0),), tariff_at=years_after(start, "1930-06-17"),
                 fiscal_at=years_after(start, "1932-06-06"))
    switch = ((1 - gc.Common().tariff_net) * rl.tariff * regs["US"].exports
              * np.array([gc.after(rl.tariff_at, k, M) if k >= 1 else 0.0 for k in range(n + 1)]))
    runs = bank_runs(start, n)
    gdp = gc.fred("GDPCA")
    ga = {d.year: float(v) for d, v in gdp.items()}
    cpi = monthly("CPIAUCNS")
    tg = [Target("output", "output", "Y", [(pd.Period(str(y), "Y"), ga[y] / ga[1929]) for y in (1930, 1931, 1932, 1933)], 0.03),
          Target("unemployment", "u", "Y", [(pd.Period(str(y), "Y"), LEBERGOTT[y]) for y in (1930, 1931, 1932, 1933)], 2.0),
          Target("prices", "P", "M", [(p0 + k, float(cpi[p0 + k] / cpi[p0])) for k in range(1, n + 1)], 0.03),
          spread_target(start, n)]
    return Episode("1929-33", start, n, regs, {r: rl for r in regs},
                   gc.Shock(equity={"US": eq}, demand={"US": conf + exm + switch}, runs={"US": runs}), tg)


# ------------------------------------------------------------------ 2008-10
def e2007(okun: float, drop: tuple = ()) -> Episode:
    """The US, December 2007 to December 2010, with today's rules, the stimulus dated at the Recovery Act (signed 17
    February 2009; the model's US response, 2.5% of GDP a year for two years, tapered over a third). Measured: household
    equity's fall from 2007Q4 (Fed Z.1, end of quarter, read by month); the housebuilding collapse (residential
    investment's share of GDP, FRED PRFI / GDP) and the rest of the world's slump (US real exports against 2007Q4, FRED
    EXPGSC1 / GDPC1), each a quarter's average in its middle month. The start measured at the end of December 2007 as
    every post-war episode's is (us_state; before 2026-10-27 the stated averages of 2007Q4, gc.us_2007), the Fed's floor
    0.125. As stated: housing wealth −30% over eighteen months (x1.5 GDP, 0.05 a krona a year), held; mortgage-related
    losses 3.5% of loans over two years from April 2008. Targets: unemployment by month (FRED UNRATE), core PCE prices'
    twelve-month inflation by month (PCEPILFE; the months before December 2007 from the data), the output gap by quarter
    (GDPC1 / GDPPOT, its change from 2007Q4), the credit spread by month (spread_target)."""
    start, n = "2007-12", 36
    q0 = pd.Period("2007Q4", "Q")
    z1 = quarterly("BOGZ1LM153064475Q", end=True)
    zq = (1 - z1.loc[q0:] / z1[q0]).clip(lower=0.0)
    eq = at_quarter_ends(zq, start, n + 1)
    house = -0.05 * 1.5 * gc.ramp(0.30, 1, 18, n + 1) * 100
    res = quarterly("PRFI") / quarterly("GDP") * 100
    build = at_mid_quarter((res - res[q0]).loc[q0:], start, n + 1)
    xq, gq = quarterly("EXPGSC1"), quarterly("GDPC1")
    exm = at_mid_quarter(((xq - xq[q0]) / gq[q0] * 100).loc[q0:], start, n + 1)
    parts = {"housing wealth": house, "housebuilding": build, "exports": exm}
    dem = sum(v for k, v in parts.items() if k not in drop)
    us = replace(us_state(start, okun, 2.5), floor=0.125)
    regs = {"US": us, "EA": gc.passive("EA"), "SE": gc.passive("SE"), "CN": gc.passive("CN")}
    rl = replace(gc.MODERN, fiscal_at=years_after(start, "2009-02-17"))
    u, core = monthly("UNRATE"), monthly("PCEPILFE")
    gap = (quarterly("GDPC1") / quarterly("GDPPOT") - 1) * 100
    p0 = pd.Period(start, "M")
    before = {j: float(core[p0 + j] / core[p0]) for j in range(-12, 0)}
    yoy = (core / core.shift(12) - 1) * 100
    tg = [Target("unemployment", "u", "M", [(p0 + k, float(u[p0 + k])) for k in range(1, n + 1)], 0.75),
          Target("core inflation", "yoy", "M", [(p0 + k, float(yoy[p0 + k])) for k in range(1, n + 1)], 0.75),
          Target("output gap", "y", "Q", [(q0 + k, float(gap[q0 + k] - gap[q0])) for k in range(1, 13)], 1.0),
          spread_target(start, n)]
    sh = gc.Shock(equity={"US": eq}, losses={"US": gc.pulse(3.5, 4, 24, n + 1, M)}, demand={"US": dem})
    return Episode("2008-10", start, n, regs, {r: rl for r in regs}, sh, tg, before=before)


# ------------------------------------------------------------------ 2000-03, held out
def e2000(okun: float, fiscal: str = "stimulus") -> Episode:
    """Out of sample: the dot-com bust, March 2000 to December 2003, today's rules, the stimulus dated at the 2001 tax
    cut (signed 7 June 2001) at the model's US size (2.5% of GDP a year: larger than 2001's; `fiscal="none"` the other
    end). Measured: household equity's fall from 2000Q1 (Z.1, by month between quarter ends); equipment investment's
    share of GDP (Y033RC1Q027SBEA / GDP) and real exports against 2000Q1 (EXPGSC1 / GDPC1) in their middle months; the
    start's unemployment, funds rate, core inflation, debts, equity wealth and exports measured (as run_2000). No
    exogenous credit losses. Targets: unemployment by month, the output gap's change by quarter, the credit spread by
    month (spread_target)."""
    start, n = "2000-03", 45
    q0 = pd.Period("2000Q1", "Q")
    gdp, z1 = quarterly("GDP"), quarterly("BOGZ1LM153064475Q", end=True)
    core = quarterly("PCEPILFE")
    hh = quarterly("CMDEBT")[q0] / 1000
    um = monthly("UNRATE")
    p0 = pd.Period(start, "M")
    us = gc.Region("US", 1.0, float(um[p0]), float(monthly("DFF")[p0]), float((core[q0] / core[q0 - 4] - 1) * 100), 0.0,
                   okun, 0.9, 0.35, float(hh / gdp[q0] * 100), float(quarterly("QUSPAM770A")[q0]), 0.25,
                   float(z1[q0] / 1000 / gdp[q0]), 0.0, 10.0, 65.0, float(quarterly("EXPGSC1")[q0] / quarterly("GDPC1")[q0]),
                   {"EA": 0.2, "CN": 0.02, "SE": 0.005, "RoW": 0.775}, 2.5, 3.0, 0.0, 0.0,
                   i_norm=year_before(monthly("DFF"), start), r_star=r_star("US", start))
    zq = (1 - z1.loc[q0:] / z1[q0]).clip(lower=0.0)
    eq = at_quarter_ends(zq, start, n + 1)
    eqp = quarterly("Y033RC1Q027SBEA") / gdp * 100
    x, g = quarterly("EXPGSC1"), quarterly("GDPC1")
    dem = at_mid_quarter((eqp - eqp[q0]).loc[q0:], start, n + 1) + at_mid_quarter(((x - x[q0]) / g[q0] * 100).loc[q0:], start, n + 1)
    regs = {"US": us, "EA": gc.passive("EA"), "SE": gc.passive("SE"), "CN": gc.passive("CN")}
    rl = replace(gc.MODERN, fiscal=fiscal, fiscal_at=years_after(start, "2001-06-07"))
    gap = (quarterly("GDPC1") / quarterly("GDPPOT") - 1) * 100
    tg = [Target("unemployment", "u", "M", [(p0 + k, float(um[p0 + k])) for k in range(1, n + 1)], 0.75),
          Target("output gap", "y", "Q", [(q0 + k, float(gap[q0 + k] - gap[q0])) for k in range(1, 16)], 1.0),
          spread_target(start, n)]
    return Episode("2000-03", start, n, regs, {r: rl for r in regs},
                   gc.Shock(equity={"US": eq}, demand={"US": dem}), tg, fitted=False)


# ------------------------------------------------------------------ the post-war US recessions (decision 82's additions)
# the energy term for the US (case.ENERGY: the pass-through of crude to consumer energy prices, this quarter and the next,
# measured on 1990Q1-2026Q2 at the tag paths-pre-signfix; consumption's share of GDP; spending lost per unit of a higher
# energy bill), carried back to earlier decades as approximate; energy's share of spending measured at each start
US_ENERGY = (0.2308, 0.0986, 0.675, 0.4)
POSTWAR_HOUSING = True      # housebuilding among the post-war recessions' measured inputs, as in 2008-10 (decision 84)


def z1_at(z1: pd.Series, start: str) -> float:
    """A quarter-end level (Z.1) at the end of month `start`, read between the quarter ends either side."""
    q0 = pd.Period(start, "M").asfreq("Q")
    return float(at_quarter_ends(z1.loc[q0 - 1:], start, 1)[0])


def equity_fall(z1: pd.Series, start: str, n: int) -> np.ndarray:
    """Household equity's fall from the end of month `start` by month (Z.1 read between quarter ends): from the start
    quarter's end on, against the level at index 0, clipped at zero; to it, linear from zero. For a start at a quarter's
    end, the quarter-end reading as before; for 1981-07 the fall from the end of July (before 2026-10-27 measured from
    the end of September, two months and most of the fall late)."""
    p0 = pd.Period(start, "M")
    q0 = p0.asfreq("Q")
    lv0 = z1_at(z1, start)
    eq = at_quarter_ends((1 - z1.loc[q0:] / lv0).clip(lower=0.0), start, n)
    k1 = (q0.asfreq("M", "end") - p0).n
    eq[:k1 + 1] = np.linspace(0.0, eq[k1], k1 + 1)
    return eq


def us_state(start: str, okun: float, stimulus: float) -> gc.Region:
    """The US at the end of month `start`, measured where a public series exists (FRED): unemployment (UNRATE), the funds
    rate (FEDFUNDS), core PCE prices' twelve-month inflation (PCEPILFE), household debt over GDP (CMDEBT), private
    non-financial debt over GDP (BIS, QUSPAM770A, as the 2026 region's; before 2026-10-27 household plus corporate
    debt, CMDEBT + BCNSDODNS, which leaves out noncorporate business: 19-29 points of GDP short), household equity
    over GDP (Z.1, at the end of the start month, read between quarter ends), real exports
    over real GDP, the quarterly ones at the start's quarter; the funds rate's average over the year to the start
    (relief's norm, decision 85); the era's neutral rate (decision 88).
    Approximate, as for 2000-03: speed 0.9, replacement 0.35, floating share 0.25, bank capital 10% and loans 65% of
    GDP, trade, the spread cap; the discretionary response `stimulus`, % of GDP a year."""
    p0 = pd.Period(start, "M")
    q0 = p0.asfreq("Q")
    gdp, z1 = quarterly("GDP"), quarterly("BOGZ1LM153064475Q", end=True)
    core = monthly("PCEPILFE")
    hh = quarterly("CMDEBT")[q0] / 1000
    return gc.Region("US", 1.0, float(monthly("UNRATE")[p0]), float(monthly("FEDFUNDS")[p0]),
                     float((core[p0] / core[p0 - 12] - 1) * 100), 0.0, okun, 0.9, 0.35, float(hh / gdp[q0] * 100),
                     float(quarterly("QUSPAM770A")[q0]), 0.25, z1_at(z1, start) / 1000 / float(gdp[q0]), 0.0, 10.0, 65.0,
                     float(quarterly("EXPGSC1")[q0] / quarterly("GDPC1")[q0]),
                     {"EA": 0.2, "CN": 0.02, "SE": 0.005, "RoW": 0.775}, stimulus, 3.0, 0.0, 0.0,
                     i_norm=year_before(monthly("FEDFUNDS"), start), r_star=r_star("US", start))


def us_episode(name: str, start: str, months: int, okun: float, *, rules: gc.Rules, stimulus: float = 2.5,
               energy: bool = False, path: bool = True, fitted: bool = True, housing: bool | None = None,
               fiscal: bool = False, notes: str = "") -> Episode:
    """A post-war US recession from the end of month `start`, by month, on the measured state (us_state) and measured
    shocks: household equity's fall from the end of the start month (equity_fall), the change in real exports against
    the start's quarter (a quarter's average in its middle month), with `housing` (by default POSTWAR_HOUSING: on, as
    in 2008-10, decision 84) the change in residential investment's share of GDP too, and with `energy` the oil price (FRED WTISPLC, its three-month average by month: the pass-through
    was measured on quarters' averages), energy's share of consumer spending at the
    start (PCE energy goods and services over PCE) and headline PCE's twelve-month inflation at the start. With `path`
    the Fed's rate is the funds rate as set (FRED FEDFUNDS; Rules.policy "path"). No exogenous credit losses (the
    model's own loss rule only). Targets: unemployment and core PCE's twelve-month inflation by month (the months before
    the start from the data), the output gap's change from the start's quarter by quarter (GDPC1 / GDPPOT), the credit
    spread by month (spread_target)."""
    p0 = pd.Period(start, "M")
    q0 = p0.asfreq("Q")
    us = us_state(start, okun, stimulus)
    eq = equity_fall(quarterly("BOGZ1LM153064475Q", end=True), start, months + 1)
    res = quarterly("PRFI") / quarterly("GDP") * 100
    xq, gq = quarterly("EXPGSC1"), quarterly("GDPC1")
    dem = at_mid_quarter(((xq - xq[q0]) / gq[q0] * 100).loc[q0:], start, months + 1)
    if POSTWAR_HOUSING if housing is None else housing:
        dem = dem + at_mid_quarter((res - res[q0]).loc[q0:], start, months + 1)
    if fiscal:                                              # the fiscal stance measured (OECD, from 1985)
        dem = dem + fiscal_impulse("USA", start, months)
    sh = gc.Shock(equity={"US": eq}, demand={"US": dem})
    if energy:
        oil = monthly("WTISPLC").rolling(3).mean()          # a quarter's average, as the pass-through was measured on
        sh.oil = {"US": np.array([float(oil[p0 + k]) for k in range(months + 1)])}
        sh.oil_before = {"US": float(oil[p0 - 1])}
        b0, b1, cons, inc = US_ENERGY
        w = float(monthly("DNRGRC1M027SBEA")[p0] / monthly("PCE")[p0])
        head = monthly("PCEPI")
        us = replace(us, energy_weight=w, energy_pass=(b0, b1), consumption_share=cons, energy_income=inc,
                     pi_h0=float((head[p0] / head[p0 - 12] - 1) * 100))
    rl = rules
    if path:
        ff = monthly("FEDFUNDS")
        sh.rate = {"US": np.array([float(ff[p0 + k]) for k in range(months + 1)])}
        rl = replace(rl, policy="path")
    regs = {"US": us, "EA": gc.passive("EA"), "SE": gc.passive("SE"), "CN": gc.passive("CN")}
    u, core = monthly("UNRATE"), monthly("PCEPILFE")
    gap = (quarterly("GDPC1") / quarterly("GDPPOT") - 1) * 100
    yoy = (core / core.shift(12) - 1) * 100
    before = {j: float(core[p0 + j] / core[p0]) for j in range(-12, 0)}
    last_q = (p0 + months).asfreq("Q")
    full = [q for q in [q0 + k for k in range(1, 4 * (months // 12 + 2))]
            if q <= last_q and (q.asfreq("M", "end") <= p0 + months) and q.asfreq("M", "start") > p0]
    tg = [Target("unemployment", "u", "M", [(p0 + k, float(u[p0 + k])) for k in range(1, months + 1)], 0.75),
          Target("core inflation", "yoy", "M", [(p0 + k, float(yoy[p0 + k])) for k in range(1, months + 1)], 0.75),
          Target("output gap", "y", "Q", [(q, float(gap[q] - gap[q0])) for q in full], 1.0),
          spread_target(start, months)]
    return Episode(name, start, months, regs, {r: rl for r in regs}, sh, tg, fitted=fitted, before=before, notes=notes)


def e1973(okun: float) -> Episode:
    """1973-75: the oil embargo (from 17 October 1973) and the Fed's rate as set; expectations largely adaptive
    (anchor 0.2 on the start's own core inflation, formed on headline: second-round effects; approximate); the Tax
    Reduction Act of 1975 (signed 29 March 1975; about 1.4% of GDP, mostly within the year: approximate): in the
    model's form, half a year at its full rate and a year's taper: about 1.46% of GDP in all as the months count it,
    each taper month read at its start as in the triggered form (check T2); before 2026-10-27 a year at full rate,
    about 2.16% in all. Price controls (Phase IV ended in April 1974) are not modelled."""
    us = us_state("1973-09", okun, 1.4)
    rl = replace(gc.MODERN, anchor=0.2, pi_star=us.pi0, expect_from="headline", fiscal_quarters=2,
                 fiscal_at=years_after("1973-09", "1975-03-29"))
    return us_episode("1973-75", "1973-09", 39, okun, rules=rl, stimulus=1.4, energy=True)


def e1981(okun: float) -> Episode:
    """1981-82: the Fed's disinflation (the funds rate as set); expectations anchored weakly on the start's core
    inflation (0.3: approximate); the 1981 tax cut (signed 13 August 1981; about 1% of GDP a year as it phased in:
    approximate) as a stimulus over two years."""
    us = us_state("1981-07", okun, 1.0)
    rl = replace(gc.MODERN, anchor=0.3, pi_star=us.pi0, fiscal_at=years_after("1981-07", "1981-08-13"))
    return us_episode("1981-82", "1981-07", 29, okun, rules=rl, stimulus=1.0)


def e1990(okun: float) -> Episode:
    """1990-91: the oil shock of August-October 1990 and the Fed's rate as set; expectations anchored on the start's
    core inflation (0.6, the eroded rules' weight: approximate); the fiscal stance measured (the OECD's underlying
    primary balance: the budget agreement of 5 November 1990 tightened it 0.8 points of potential GDP in 1991)."""
    us = us_state("1990-06", okun, 2.5)
    rl = replace(gc.MODERN, anchor=0.6, pi_star=us.pi0, fiscal="none")
    return us_episode("1990-91", "1990-06", 30, okun, rules=rl, energy=True, fiscal=True)


# ------------------------------------------------------------------ measured fiscal stances (OECD), and the crashes abroad
EO_FILES = {"eo_episodes_annual_a.csv": "SWE+JPN+EA17+USA.GAP+GDPV+GDPVTR+UNR+NLGQ+NLGXQ.A",
            "eo_episodes_annual_b.csv": "SWE+JPN+EA17+USA.NLGXQU+NLGQU+NLGXQ+NLGQ.A",
            "eo_episodes_quarterly.csv": "SWE+JPN+EA17.XGSV+GDPV+IRS+CPI+PCORE.Q",
            "eo_episodes_quarterly_b.csv": "SWE+JPN+EA17.IBV+IHV+ITV+IGV+ITISKV+CPV.Q"}
EO_URL = "https://sdmx.oecd.org/public/rest/data/OECD.ECO.MAD,DSD_EO@DF_EO,1.5/{key}?startPeriod=1980&format=csvfile"


@functools.lru_cache(maxsize=1)
def eo() -> pd.DataFrame:
    """The OECD Economic Outlook (edition 119; the OECD's SDMX API, cached in cache/oecd/): real GDP (GDPV) and potential
    output (GDPVTR), the output gap (GAP), the government's underlying primary balance (NLGXQU, % of potential GDP:
    cyclically adjusted), real exports (XGSV), real business and housing investment (IBV, IHV), by area (SWE, JPN, EA17,
    USA)."""
    frames = []
    for f, key in EO_FILES.items():
        fp = os.path.join(gc.ROOT, "cache", "oecd", f)
        if not os.path.exists(fp):
            import requests
            r = requests.get(EO_URL.format(key=key), timeout=120)
            r.raise_for_status()
            open(fp, "w", encoding="utf-8").write(r.text)
        frames.append(pd.read_csv(fp, low_memory=False)[["REF_AREA", "MEASURE", "FREQ", "TIME_PERIOD", "OBS_VALUE"]])
    return pd.concat(frames).drop_duplicates(["REF_AREA", "MEASURE", "FREQ", "TIME_PERIOD"])


def eo_series(area: str, measure: str, freq: str) -> pd.Series:
    d = eo()
    d = d[(d.REF_AREA == area) & (d.MEASURE == measure) & (d.FREQ == freq)]
    idx = pd.PeriodIndex(d.TIME_PERIOD.astype(str).str.replace("-Q", "Q"), freq="Y" if freq == "A" else freq)
    return pd.Series(d.OBS_VALUE.astype(float).values, index=idx).sort_index()


def eo_gap(area: str) -> pd.Series:
    """The output gap by quarter, %: the OECD's quarterly real GDP against its annual potential output, each year's
    potential at mid-year and log-linear between (the report prints each year's average beside the annual gap the OECD
    publishes)."""
    y, pot, ya = eo_series(area, "GDPV", "Q"), eo_series(area, "GDPVTR", "A"), eo_series(area, "GDPV", "A")
    years = [p for p in ya.index if (y.index.year == p.year).sum() == 4]
    unit = float(np.mean([ya[p] / y[y.index.year == p.year].mean() for p in years]))     # annual against quarterly units
    t = [q.year + (q.quarter - 0.5) / 4 for q in y.index]
    lp = np.interp(t, [p.year + 0.5 for p in pot.index], np.log(pot.values))
    return pd.Series(100 * (y.values * unit / np.exp(lp) - 1), index=y.index)


def fiscal_impulse(area: str, start: str, n: int) -> np.ndarray:
    """The discretionary fiscal stance by month from index 0, as a demand level (% of GDP): the fall in the government's
    underlying primary balance since the start (OECD NLGXQU, % of potential GDP; cyclically adjusted, so the automatic
    stabilisers, which the model has, are left out), each year's value at mid-year and linear between, times the 0.8 the
    model gives a stimulus."""
    b = eo_series(area, "NLGXQU", "A")
    t = [m.year + m.month / 12 for m in (pd.Period(start, "M") + k for k in range(n + 1))]
    v = np.interp(t, [p.year + 0.5 for p in b.index], b.values)
    return -0.8 * (v - v[0])


def riksbank_monthly(sid: str) -> pd.Series:
    """A Riksbank series (the SWEA API, cached by se_1990s.py for 1989-96) as monthly averages."""
    fp = os.path.join(gc.ROOT, "cache", "riksbank", f"{sid}_1989-01-01_1996-12-31.json")
    obs = [o for o in json.load(open(fp, encoding="utf-8")) if o.get("value") is not None]
    x = pd.Series([float(o["value"]) for o in obs], index=pd.DatetimeIndex([o["date"] for o in obs]))
    return x.groupby(x.index.to_period("M")).mean()


def eurostat_ea(item: str) -> pd.Series:
    """The euro area's (EA19) quarterly national accounts in chained 2010 euros, seasonally and calendar adjusted
    (Eurostat namq_10_gdp, cached in cache/eurostat/): B1GQ (GDP) or P6 (exports, intra-area trade included)."""
    d = json.load(open(os.path.join(gc.ROOT, "cache", "eurostat", "namq_10_gdp_EA19_P6_B1GQ_CLV10.json"), encoding="utf-8"))
    ix = {k: d["dimension"][k]["category"]["index"] for k in d["id"]}
    times = sorted(ix["time"], key=ix["time"].get)
    j = ix["na_item"][item]
    vals = {t: d["value"].get(str(j * len(times) + i)) for i, t in enumerate(times)}
    return pd.Series({pd.Period(t.replace("-Q", "Q"), "Q"): float(v) for t, v in vals.items() if v is not None}).sort_index()


def episode_abroad(name: str, code: str, start: str, n: int, g: gc.Region, rl: gc.Rules, *, rate: pd.Series,
                   equity: pd.Series, unemp: pd.Series, core: pd.Series, gap: pd.Series, house: tuple | None = None,
                   exports: tuple | None = None, fiscal: np.ndarray | None = None, losses: np.ndarray | None = None,
                   spread: np.ndarray | None = None, invest: tuple | None = None, fitted: bool = True,
                   notes: str = "") -> Episode:
    """An economy from the end of month `start`, by month, as one region (`code`; the others passive), the central bank's
    rate as set (`rate`, monthly), on measured shocks: share prices' fall from the start (monthly); with `house` (real
    property prices by quarter, housing wealth x GDP) housing wealth's fall at 0.05 a krona a year, as 2008-10's; with
    `exports` (real exports and real GDP by quarter, the share of exports leaving the area) their change against the start's
    quarter, % of its GDP, each quarter's in its middle month; with `invest` (real private investment and real GDP by
    quarter) its change against the start's quarter likewise, the bust's own collapse as 2008-10's housebuilding and
    2000-03's equipment are; the fiscal stance (fiscal_impulse); stated credit losses and a spread passed to borrowers.
    With `invest` the model's own credit spread is off (a cap of zero under the backstop):
    with all private investment measured, the spread's effect on spending, mostly through investment, is in it (Sweden's
    and Japan's crunch counted twice otherwise; found 2026-10-27); bank capital and losses are still tracked. Targets:
    unemployment and core prices' twelve-month inflation by month (the months before the start from the data with its
    seasonal pattern taken out: the core indexes abroad are not seasonally adjusted), the output gap's change from the
    start's quarter by quarter."""
    p0 = pd.Period(start, "M")
    q0 = p0.asfreq("Q")
    eq = np.array([max(0.0, 1 - float(equity[p0 + k]) / float(equity[p0])) for k in range(n + 1)])
    dem = np.zeros(n + 1)
    if house is not None:
        hp, wealth = house
        dem += -0.05 * wealth * 100 * at_mid_quarter((1 - hp.loc[q0:] / hp[q0]).clip(lower=-1.0), start, n + 1)
    if exports is not None:
        x, gdp, share = exports
        dem += share * at_mid_quarter(((x - x[q0]) / gdp[q0] * 100).loc[q0:], start, n + 1)
    if invest is not None:
        iv, gdp = invest
        dem += at_mid_quarter(((iv - iv[q0]) / gdp[q0] * 100).loc[q0:], start, n + 1)
    if fiscal is not None:
        dem += fiscal
    sh = gc.Shock(equity={code: eq}, demand={code: dem}, rate={code: np.array([float(rate[p0 + k]) for k in range(n + 1)])})
    if losses is not None:
        sh.losses = {code: losses}
    if spread is not None:
        sh.spread = {code: spread}
    rl = replace(rl, policy="path")
    if invest is not None:
        g = replace(g, spread_cap=0.0)
    regs = {code: g, **{r: gc.passive(r) for r in ("US", "EA", "SE", "CN") if r != code}}
    yoy = (core / core.shift(12) - 1) * 100
    lg = np.log(core)              # calendar-month factors: the log index against its centred 2x12 average, six years
    dev = (lg - lg.rolling(12).mean().rolling(2).mean().shift(-6)).loc[p0 - 36:p0 + 36].dropna()
    sf = dev.groupby(dev.index.month).mean()
    before = {j: float(core[p0 + j] / core[p0] * np.exp(sf[p0.month] - sf[(p0 + j).month])) for j in range(-12, 0)}
    last = p0 + n
    full = [q for q in (q0 + k for k in range(1, 4 * (n // 12 + 2)))
            if q.asfreq("M", "start") > p0 and q.asfreq("M", "end") <= last and q in gap.index]
    tg = [Target("unemployment", "u", "M", [(p0 + k, float(unemp[p0 + k])) for k in range(1, n + 1)], 0.75),
          Target("core inflation", "yoy", "M", [(p0 + k, float(yoy[p0 + k])) for k in range(1, n + 1)], 0.75),
          Target("output gap", "y", "Q", [(q, float(gap[q] - gap[q0])) for q in full], 1.0)]
    return Episode(name, start, n, regs, {r: rl for r in regs}, sh, tg, fitted=fitted, active=[code], region=code,
                   before=before, notes=notes)


def e_se1990(okun: float = 0.4) -> Episode:
    """Sweden, June 1990 to December 1993: the property and bank crisis, the defence of the krona's peg and the float of
    19 November 1992. The rate as set: the Riksbank's three-month Treasury bill, monthly averages (22% in September 1992;
    the marginal rate's days at 500% were overnight). Measured (FRED: OECD and BIS series): unemployment (harmonised),
    core CPI (non-food non-energy), share prices, real residential property prices (BIS QSER628BIS; housing wealth 1.5x
    GDP, approximate), household and private credit; real exports, GDP and private investment (business and housing: down 10 points of GDP
    by 1993), the output gap and the fiscal stance from the OECD's Economic Outlook (the underlying primary balance fell
    4.8 points of potential GDP from 1990 to 1993). No credit losses beyond the model's own loss rule: with private
    investment measured, the credit crunch's effect on spending is in it (stated losses on top counted it twice, the gap
    reaching -22 against -8; found 2026-10-27). Stated, approximate: bank capital 7% and loans 100% of GDP, replacement 0.8, a floating share of 0.4, equity wealth 0.3x GDP; the backstop on throughout
    (the state took over Nordbanken in 1991-92 and guaranteed every bank's liabilities from 24 September 1992); the neutral
    rate the euro area's (HLW, 1990Q2: no estimate for Sweden); expectations anchored weakly (0.3) on the start's core
    inflation; the model's credit spread off with investment measured (episode_abroad)."""
    start, n = "1990-06", 42
    p0 = pd.Period(start, "M")
    q0 = p0.asfreq("Q")
    rate, core, u = riksbank_monthly("SETB3MBENCH"), monthly("SWECPICORMINMEI"), monthly("LRHUTTTTSEM156S")
    hh, pr = quarterly("QSEHAM770A"), quarterly("QSEPAM770A")
    g = gc.Region("SE", 1.0, float(u[p0]), float(rate[p0]), float((core[p0] / core[p0 - 12] - 1) * 100), 0.0, okun, 0.4,
                  0.8, float(hh[q0]), float(pr[q0]), 0.4, 0.3, 0.0, 7.0, 100.0, 0.30, {"US": 0.1, "RoW": 0.9}, 0.0, 3.0,
                  0.0, 0.0, i_norm=year_before(rate, start), r_star=r_star("EA", start))
    rl = replace(gc.MODERN, anchor=0.3, pi_star=g.pi0, fiscal="none")
    return episode_abroad("Sweden 1990-93", "SE", start, n, g, rl, rate=rate, equity=monthly("SPASTT01SEM661N"), unemp=u,
                          core=core, gap=eo_gap("SWE"), house=(quarterly("QSER628BIS"), 1.5),
                          exports=(eo_series("SWE", "XGSV", "Q"), eo_series("SWE", "GDPV", "Q"), 1.0),
                          invest=(eo_series("SWE", "IBV", "Q") + eo_series("SWE", "IHV", "Q"), eo_series("SWE", "GDPV", "Q")),
                          fiscal=fiscal_impulse("SWE", start, n))


# the euro area's periphery whose ten-year yields measured a borrowing cost through 2011-13, and their shares of the
# euro area's GDP (2011, approximate); Greece's after its restructuring (March 2012) price a defaulted claim: left out
PERIPHERY = {"IT": 0.17, "ES": 0.115, "PT": 0.018, "IE": 0.018}


def e_ea2011(okun: float = 0.4) -> Episode:
    """The euro area, March 2011 to December 2013: the sovereign debt crisis and the consolidation. The rate as set: EONIA
    (the ECB's rises of April and July 2011, the cuts from November). Measured: unemployment (harmonised), core HICP
    (excluding energy, food, alcohol and tobacco), share prices, real residential property prices (BIS QXMR628BIS;
    housing wealth 1.5x GDP, approximate), BIS credit (FRED); real exports (Eurostat, the euro area's, intra-area trade included, so 0.55 of
    the change counted: the part leaving the area, approximate); the output gap and the fiscal stance from the OECD (the
    underlying primary balance rose 1.9 points of potential GDP from 2011 to 2013); the periphery's sovereign stress, its
    ten-year spreads over Germany's (FRED, OECD) weighted by GDP, their rise since the start, half of it passed to private
    borrowers across the area (decision 70's pass-through). Stated, approximate: bank capital 8% and loans 100% of GDP,
    replacement 0.6, a floating share of 0.4, equity wealth 0.5x GDP; no credit losses beyond the model's rule; the
    neutral rate HLW's for the euro area (2011Q1); expectations anchored as today's (0.9 on 2%)."""
    start, n = "2011-03", 33
    p0 = pd.Period(start, "M")
    q0 = p0.asfreq("Q")
    rate, core, u = monthly("IRSTCI01EZM156N"), monthly("00XEFDEZ19M086NEST"), monthly("LRHUTTTTEZM156S")
    hh, pr = quarterly("QXMHAM770A"), quarterly("QXMPAM770A")
    g = gc.Region("EA", 1.0, float(u[p0]), float(rate[p0]), float((core[p0] / core[p0 - 12] - 1) * 100), -0.5, okun,
                  0.35, 0.6, float(hh[q0]), float(pr[q0]), 0.4, 0.5, 0.0, 8.0, 100.0, 0.25,
                  {"US": 0.15, "CN": 0.1, "RoW": 0.75}, 0.0, 3.0, 0.0, 0.0, i_norm=year_before(rate, start),
                  r_star=r_star("EA", start))
    de = monthly("IRLTLT01DEM156N")
    sp = sum(w * (monthly(f"IRLTLT01{c}M156N") - de) for c, w in PERIPHERY.items())
    spread = 0.5 * np.array([float(sp[p0 + k] - sp[p0]) for k in range(n + 1)])
    return episode_abroad("euro area 2011-13", "EA", start, n, g, replace(gc.MODERN, fiscal="none"), rate=rate,
                          equity=monthly("SPASTT01EZM661N"), unemp=u, core=core, gap=eo_gap("EA17"),
                          house=(quarterly("QXMR628BIS"), 1.5),
                          exports=(eurostat_ea("P6"), eurostat_ea("B1GQ"), 0.55),
                          fiscal=fiscal_impulse("EA17", start, n), spread=spread)


def e_jp1990(okun: float = 0.2) -> Episode:
    """Japan, December 1990 to December 1995: the bubble's collapse, from the Nikkei's fall and the land market's turn to
    the yen's peak. The rate as set: the call rate (8.2% to 0.5%). Measured: unemployment (harmonised), core CPI (non-food
    non-energy), the Nikkei 225 (monthly averages), real residential property prices (BIS QJPR628BIS; land and housing
    wealth 2x GDP, approximate), BIS credit (FRED); real exports, GDP and private investment (business and housing: business investment
    down 5 points of GDP by 1993), the output gap and the fiscal stance from the OECD (the underlying primary balance fell
    4.4 points of potential GDP from 1990 to 1995: the packages of 1992-95). Stated,
    approximate: Okun 0.2 (lifetime employment), speed 0.3, replacement 0.6, a floating share of 0.3, equity wealth 0.25x
    GDP, bank capital 6% and loans 120% of GDP, no credit losses beyond the model's rule (the banks wrote off some 4% of
    loans over fiscal 1992-95, about what the rule gives), the backstop on (the state stood behind the banks: the
    convoy system, then forbearance; the model books losses down to the backstop's floor, and its credit spread is off
    with investment measured), the neutral rate 3% (no HLW estimate; the Bank of Japan's staff put it near 3-4% around 1990),
    expectations anchored at 0.6 on the start's core inflation."""
    start, n = "1990-12", 60
    p0 = pd.Period(start, "M")
    q0 = p0.asfreq("Q")
    rate, core, u = monthly("IRSTCI01JPM156N"), monthly("JPNCPICORMINMEI"), monthly("LRHUTTTTJPM156S")
    hh, pr = quarterly("QJPHAM770A"), quarterly("QJPPAM770A")
    g = gc.Region("JP", 1.0, float(u[p0]), float(rate[p0]), float((core[p0] / core[p0 - 12] - 1) * 100), 0.0, okun, 0.3,
                  0.6, float(hh[q0]), float(pr[q0]), 0.3, 0.25, 0.0, 6.0, 120.0, 0.10, {"US": 0.3, "RoW": 0.7}, 0.0, 3.0,
                  0.0, 0.0, i_norm=year_before(rate, start), r_star=3.0)
    rl = replace(gc.MODERN, anchor=0.6, pi_star=g.pi0, fiscal="none")
    return episode_abroad("Japan 1991-95", "JP", start, n, g, rl, rate=rate, equity=monthly("NIKKEI225"), unemp=u,
                          core=core, gap=eo_gap("JPN"), house=(quarterly("QJPR628BIS"), 2.0),
                          exports=(eo_series("JPN", "XGSV", "Q"), eo_series("JPN", "GDPV", "Q"), 1.0),
                          invest=(eo_series("JPN", "IBV", "Q") + eo_series("JPN", "IHV", "Q"), eo_series("JPN", "GDPV", "Q")),
                          fiscal=fiscal_impulse("JPN", start, n))


def e1937(okun: float) -> Episode:
    """The US, May 1937 to December 1939: the recession within the recovery. Off gold since 1933-34, with deposit
    insurance (1934) and the RFC behind the banks; no unemployment insurance yet. The rate as set: the three-month
    Treasury bill (FRED TB3MS; the reserve requirement rises of March and May 1937 and the gold sterilisation from
    December 1936 have no channel of their own here). Measured, monthly: the Dow-Jones index (NBER, M1109BUSM293NNBR);
    the fiscal stance, the federal surplus over GDP (FRED FYFSD / GDPA, each fiscal year's at its middle, 1 January, and
    linear between: actual, not cyclically adjusted, so the tightening of fiscal 1938 is understated); the rest of the
    world's slump, US real exports against 1937 (EXPGSCA / GDPCA, annual, placed mid-year). Stated, approximate: household
    debt 40% and private debt 130% of GDP, equity wealth 0.6x GDP, bank capital 12% and loans 25% of GDP; the 1930s'
    Phillips slope and expectations (0.2 on stable prices); the model's neutral rate (no estimate before 1961). Targets:
    unemployment by month (the NBER's monthly estimate, M0892AUSM156SNBR, a point or two under Lebergott's annual series,
    its scale 1.0 for a rougher measure), the consumer price level by month (CPIAUCNS, against May 1937), annual output in
    1938 and 1939 against 1937 (GDPCA; the model's year on a 2% trend, against index 0), the credit spread by month
    (spread_target)."""
    start, n = "1937-05", 31
    p0 = pd.Period(start, "M")
    t = 1937 + 5 / 12 + np.arange(n + 1) * M
    dow, tb, u, cpi = monthly("M1109BUSM293NNBR"), monthly("TB3MS"), monthly("M0892AUSM156SNBR"), monthly("CPIAUCNS")
    eq = np.array([max(0.0, 1 - float(dow[p0 + k]) / float(dow[p0])) for k in range(n + 1)])
    e, gq = gc.fred("EXPGSCA"), gc.fred("GDPCA")
    ea, ga = ({d.year: float(v) for d, v in x.items()} for x in (e, gq))
    exm = np.interp(t, [y + 0.5 for y in range(1936, 1942)], [(ea[y] - ea[1937]) / ga[1937] * 100 for y in range(1936, 1942)])
    fy, gn = gc.fred("FYFSD"), gc.fred("GDPA")
    gna = {d.year: float(v) for d, v in gn.items()}
    bal = {d.year: float(v) / 1000 / ((gna[d.year - 1] + gna[d.year]) / 2) * 100 for d, v in fy.items()
           if 1935 <= d.year <= 1942}
    v = np.interp(t, [float(y) for y in sorted(bal)], [bal[y] for y in sorted(bal)])
    fis = -0.8 * (v - v[0])
    us = gc.Region("US", 1.0, float(u[p0]), float(tb[p0]), float((cpi[p0] / cpi[p0 - 12] - 1) * 100), 0.0, okun, 0.9, 0.0,
                   40.0, 130.0, 0.2, 0.6, 0.0, 12.0, 25.0, float(ea[1937] / ga[1937]), {"EA": 0.3, "RoW": 0.7}, 0.0, 99.0,
                   0.0, 0.0, i_norm=year_before(tb, start))
    rl = replace(gc.THIRTIES, policy="path", insured=True, backstop=True, fiscal="none", tariff=0.0)
    sh = gc.Shock(equity={"US": eq}, demand={"US": exm + fis}, rate={"US": np.array([float(tb[p0 + k]) for k in range(n + 1)])})
    regs = {"US": us, "EA": gc.passive("EA"), "SE": gc.passive("SE"), "CN": gc.passive("CN")}
    tg = [Target("unemployment", "u", "M", [(p0 + k, float(u[p0 + k])) for k in range(1, n + 1)], 1.0),
          Target("prices", "P", "M", [(p0 + k, float(cpi[p0 + k] / cpi[p0])) for k in range(1, n + 1)], 0.03),
          Target("output", "output", "Y", [(pd.Period(str(y), "Y"), ga[y] / ga[1937]) for y in (1938, 1939)], 0.03),
          spread_target(start, n)]
    return Episode("1937-38", start, n, regs, {r: rl for r in regs}, sh, tg)


# ------------------------------------------------------------------ the fit
PARAMS = ("sigma", "money", "debt_deflation", "kappa_1930", "okun_us", "impulse_1930_pct_gdp", "a_r", "a_f", "f_speed",
          "cap_oil", "okun_se", "okun_ea", "okun_jp", "dd_sat")
BOUNDS = [(0, 15), (0, 15), (0, 0.5), (0.03, 1.0), (0.4, 1.0), (0, 10), (0.03, 0.15), (0, 1.0), (0.1, 1.0), (0, 4.0),
          (0.1, 1.5), (0.1, 1.5), (0.05, 1.5), (0.01, 1.0)]
# dd_sat, the shortfall at which debt deflation levels off (decision 92), is weakly separated from its slope: with the
# slope's bound widened to 2 the search turns the pair into a fixed drag from a 1% shortfall (Log 53); the bounds stated
# here (the slope's 0.5, as since the quarterly fit) are a judgement, kept and stated
OKUN = {"SE": 10, "EA": 11, "JP": 12}       # each region's Okun slope, its own episode's (as the US's)
# the extensions' settings, not fitted (decisions 85 and 87): floating-rate debt reprices within a year, and expectations
# adapt to the past year's inflation
FIXED = {"reprice": 1.0, "expect_over": 1.0}


@functools.lru_cache(maxsize=1)
def _base() -> tuple:
    """The episodes with their measured parts, built once at unit Okun and no impulse."""
    return (e1929(0.7, 0.0), e2007(0.7), e2000(0.7), e1973(0.7), e1981(0.7), e1990(0.7), e1937(0.7), e_se1990(),
            e_ea2011(), e_jp1990())


def episodes(theta) -> list:
    """The episodes at the fit's parameters: the US Okun slope and 1930's spending collapse are the episodes' own."""
    okun, imp = theta[4], theta[5]
    out = []
    for ep in _base():
        regs = {**ep.regions, "US": replace(ep.regions["US"], okun=okun)}
        if ep.region in OKUN and len(theta) > OKUN[ep.region]:
            regs[ep.region] = replace(regs[ep.region], okun=theta[OKUN[ep.region]])
        shock = ep.shock
        if ep.name == "1929-33":
            shock = replace(shock, demand={"US": shock.demand["US"] - imp * conf_profile(ep.months)})
        e = replace(ep, regions=regs, shock=shock)
        e._where = ep.where()
        out.append(e)
    return out


def common(theta, cm0: gc.Common = gc.Common(), fixed: dict | None = None) -> gc.Common:
    sigma, money, dd, k30, okun, imp, ar = theta[:7]
    ext = dict(zip(PARAMS[7:10], theta[7:10]))
    ext.update(zip(PARAMS[13:], theta[13:]))       # any further Common field fitted by name (dd_sat; a variant: a_s)
    return replace(cm0, sigma=sigma, money=money, debt_deflation=dd, kappa_1930=k30, a_r=ar, **ext,
                   **(FIXED if fixed is None else fixed))


def loss(theta, build=episodes) -> float:
    sigma, money, dd, k30, okun, imp, ar = theta[:7]
    if min(sigma, money, dd, k30, imp, *theta[7:]) < 0 or not 0.3 <= okun <= 1.0:
        return 1e6
    cm = common(theta)
    e = np.concatenate([ep.errors(ep.run(cm)) for ep in build(theta) if ep.fitted])
    return float(np.sum(np.square(e)))


def report(theta) -> None:
    cm = common(theta)
    for ep in episodes(theta):
        cmp_ = ep.compare(ep.run(cm))
        print(f"{ep.name} ({'fitted' if ep.fitted else 'held out'}):")
        for t in ep.targets:
            pts = [(m, d) for tt, _, m, d in cmp_ if tt is t]
            rms = float(np.sqrt(np.mean([(m - d) ** 2 for m, d in pts])))
            print(f"   {t.name} ({t.freq}, {len(pts)}): RMS {rms:.3f}; model {[round(m, 2) for m, _ in pts][:6]}... "
                  f"data {[round(d, 2) for _, d in pts][:6]}...")


def fit():
    """The fit (decision 82; the model's since 2026-10-28, Log 52): a global search (differential evolution, seed 7) on the
    episodes marked fitted. Returns the parameters, the loss and the number of target points."""
    from scipy.optimize import differential_evolution
    best = differential_evolution(loss, BOUNDS, seed=7, popsize=20, maxiter=150, tol=1e-7, polish=True)
    n = sum(len(ep.where()) for ep in episodes(best.x) if ep.fitted)
    return best.x, float(best.fun), n


def fitted() -> dict:
    """The stored fit (results/episodes.json, written by main): the parameters by name, the fixed settings, the loss."""
    return json.load(open(os.path.join(gc.ROOT, "results", "episodes.json"), encoding="utf-8"))


def stored_common(fp: dict | None = None) -> gc.Common:
    """The model's common parameters at the stored fit: the fitted ones and the fixed settings (reprice, expect_over)."""
    fp = fitted() if fp is None else fp
    return common([fp["fitted"][k] for k in PARAMS], fixed=fp["fixed"])


def record(theta, loss_value: float, n_points: int) -> dict:
    """Each episode at the parameters: every target's model and data by period, its RMS error, the episode's loss."""
    cm = common(theta)
    eps = {}
    for ep in episodes(theta):
        o = ep.run(cm)
        cmp_ = ep.compare(o)
        tg = {}
        for t in ep.targets:
            pts = [(str(p), m, d) for tt, p, m, d in cmp_ if tt is t]
            tg[t.name] = {"freq": t.freq, "scale": t.scale, "periods": [p for p, _, _ in pts],
                          "model": [round(m, 4) for _, m, _ in pts], "data": [round(d, 4) for _, _, d in pts],
                          "rms": round(float(np.sqrt(np.mean([(m - d) ** 2 for _, m, d in pts]))), 4)}
        eps[ep.name] = {"fitted": ep.fitted, "start": ep.start, "months": ep.months, "region": ep.region,
                        "loss": round(float(np.sum(np.square(ep.errors(o)))), 3), "targets": tg,
                        "bank_capital_lost_max": round(float(o["stress"].max()), 3)}
    return {"fitted": dict(zip(PARAMS, [float(v) for v in theta])), "fixed": dict(FIXED),
            "bounds": dict(zip(PARAMS, [list(b) for b in BOUNDS])), "loss": round(float(loss_value), 3),
            "points": int(n_points), "housing": POSTWAR_HOUSING, "episodes": eps}


def figure(rec: dict) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    names = list(rec["episodes"])
    fig, axes = plt.subplots(len(names), 2, figsize=(12, 2.3 * len(names)), layout="constrained")
    for row, nm in zip(axes, names):
        e = rec["episodes"][nm]
        for ax, keys in zip(row, (("output gap", "output"), ("unemployment",))):
            t = next((e["targets"][k] for k in keys if k in e["targets"]), None)
            if t is None:
                ax.axis("off")
                continue
            x = np.arange(len(t["data"]))
            ax.plot(x, t["data"], color="0.2", lw=1.6, label="data")
            ax.plot(x, t["model"], color="#c0392b", lw=1.4, label="model")
            ax.set_title(f"{nm} ({'fitted' if e['fitted'] else 'held out'}): {next(k for k in keys if k in e['targets'])}"
                         f" by {dict(M='month', Q='quarter', Y='year')[t['freq']]}, RMS {t['rms']:.2f}", fontsize=9)
            ax.set_xticks(x[::max(1, len(x) // 6)])
            ax.set_xticklabels([t["periods"][i] for i in x[::max(1, len(x) // 6)]], fontsize=7)
    axes[0][0].legend(fontsize=8)
    fig.savefig(os.path.join(gc.ROOT, "figures", "fig_episodes.png"), dpi=110)


def main():
    """Fit the model on the episodes and store it: results/episodes.json (the model's fit, read by global_crash.main)
    and figures/fig_episodes.png."""
    x, f, n = fit()
    rec = record(x, f, n)
    json.dump(rec, open(os.path.join(gc.ROOT, "results", "episodes.json"), "w", encoding="utf-8"), indent=1)
    figure(rec)
    print(json.dumps({k: v for k, v in rec.items() if k != "episodes"}, indent=1))
    report(x)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
