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
# Run from paths/:  ../venv/Scripts/python.exe code/episodes.py     (prints each episode's fit at the stored parameters)

from __future__ import annotations

import functools
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
        return gc.simulate(self.regions, self.rules, self.shock, cm, self.months + 1, active=self.active, dt=M)[self.region]

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


# ------------------------------------------------------------------ 1929-33
LEBERGOTT = gc.LEBERGOTT


def conf_profile(n: int) -> np.ndarray:
    """The post-crash spending collapse per point of its size: full for the first half-year, gone two years later."""
    t = np.arange(n + 1) * M
    return np.array([max(0.0, 1 - max(x - 0.5, 0) / 2.0) if k >= 1 else 0.0 for k, x in enumerate(t)])


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
    fitted. Targets: annual output (FRED GDPCA, against the model's year on a 2% trend) and unemployment (Lebergott,
    the standard series) for 1930-33; the consumer price level by month (FRED CPIAUCNS, against September 1929)."""
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
    gdp = gc.fred("GDPCA")
    ga = {d.year: float(v) for d, v in gdp.items()}
    cpi = monthly("CPIAUCNS")
    tg = [Target("output", "output", "Y", [(pd.Period(str(y), "Y"), ga[y] / ga[1929]) for y in (1930, 1931, 1932, 1933)], 0.03),
          Target("unemployment", "u", "Y", [(pd.Period(str(y), "Y"), LEBERGOTT[y]) for y in (1930, 1931, 1932, 1933)], 2.0),
          Target("prices", "P", "M", [(p0 + k, float(cpi[p0 + k] / cpi[p0])) for k in range(1, n + 1)], 0.03)]
    return Episode("1929-33", start, n, regs, {r: rl for r in regs}, gc.Shock(equity={"US": eq}, demand={"US": conf + exm}), tg)


# ------------------------------------------------------------------ 2008-10
def e2007(okun: float, drop: tuple = ()) -> Episode:
    """The US, December 2007 to December 2010, with today's rules, the stimulus dated at the Recovery Act (signed 17
    February 2009; the model's US response, 2.5% of GDP a year for two years, tapered over a third). Measured: household
    equity's fall from 2007Q4 (Fed Z.1, end of quarter, read by month); the housebuilding collapse (residential
    investment's share of GDP, FRED PRFI / GDP) and the rest of the world's slump (US real exports against 2007Q4, FRED
    EXPGSC1 / GDPC1), each a quarter's average in its middle month. As stated: housing wealth −30% over eighteen months
    (x1.5 GDP, 0.05 a krona a year), held; mortgage-related losses 3.5% of loans over two years from April 2008.
    Targets: unemployment by month (FRED UNRATE), core PCE prices' twelve-month inflation by month (PCEPILFE; the months
    before December 2007 from the data), the output gap by quarter (GDPC1 / GDPPOT, its change from 2007Q4)."""
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
    regs = {"US": gc.us_2007(okun), "EA": gc.passive("EA"), "SE": gc.passive("SE"), "CN": gc.passive("CN")}
    rl = replace(gc.MODERN, fiscal_at=years_after(start, "2009-02-17"))
    u, core = monthly("UNRATE"), monthly("PCEPILFE")
    gap = (quarterly("GDPC1") / quarterly("GDPPOT") - 1) * 100
    p0 = pd.Period(start, "M")
    before = {j: float(core[p0 + j] / core[p0]) for j in range(-12, 0)}
    yoy = (core / core.shift(12) - 1) * 100
    tg = [Target("unemployment", "u", "M", [(p0 + k, float(u[p0 + k])) for k in range(1, n + 1)], 0.75),
          Target("core inflation", "yoy", "M", [(p0 + k, float(yoy[p0 + k])) for k in range(1, n + 1)], 0.75),
          Target("output gap", "y", "Q", [(q0 + k, float(gap[q0 + k] - gap[q0])) for k in range(1, 13)], 1.0)]
    sh = gc.Shock(equity={"US": eq}, losses={"US": gc.pulse(3.5, 4, 24, n + 1, M)}, demand={"US": dem})
    return Episode("2008-10", start, n, regs, {r: rl for r in regs}, sh, tg, before=before)


# ------------------------------------------------------------------ 2000-03, held out
def e2000(okun: float, fiscal: str = "stimulus") -> Episode:
    """Out of sample: the dot-com bust, March 2000 to December 2003, today's rules, the stimulus dated at the 2001 tax
    cut (signed 7 June 2001) at the model's US size (2.5% of GDP a year: larger than 2001's; `fiscal="none"` the other
    end). Measured: household equity's fall from 2000Q1 (Z.1, by month between quarter ends); equipment investment's
    share of GDP (Y033RC1Q027SBEA / GDP) and real exports against 2000Q1 (EXPGSC1 / GDPC1) in their middle months; the
    start's unemployment, funds rate, core inflation, debts, equity wealth and exports measured (as run_2000). No
    exogenous credit losses. Targets: unemployment by month and the output gap's change by quarter."""
    start, n = "2000-03", 45
    q0 = pd.Period("2000Q1", "Q")
    gdp, z1 = quarterly("GDP"), quarterly("BOGZ1LM153064475Q", end=True)
    core = quarterly("PCEPILFE")
    hh, biz = quarterly("CMDEBT")[q0] / 1000, quarterly("BCNSDODNS")[q0] / 1000
    um = monthly("UNRATE")
    p0 = pd.Period(start, "M")
    us = gc.Region("US", 1.0, float(um[p0]), float(monthly("DFF")[p0]), float((core[q0] / core[q0 - 4] - 1) * 100), 0.0,
                   okun, 0.9, 0.35, float(hh / gdp[q0] * 100), float((hh + biz) / gdp[q0] * 100), 0.25,
                   float(z1[q0] / 1000 / gdp[q0]), 0.0, 10.0, 65.0, float(quarterly("EXPGSC1")[q0] / quarterly("GDPC1")[q0]),
                   {"EA": 0.2, "CN": 0.02, "SE": 0.005, "RoW": 0.775}, 2.5, 3.0, 0.0, 0.0)
    zq = (1 - z1.loc[q0:] / z1[q0]).clip(lower=0.0)
    eq = at_quarter_ends(zq, start, n + 1)
    eqp = quarterly("Y033RC1Q027SBEA") / gdp * 100
    x, g = quarterly("EXPGSC1"), quarterly("GDPC1")
    dem = at_mid_quarter((eqp - eqp[q0]).loc[q0:], start, n + 1) + at_mid_quarter(((x - x[q0]) / g[q0] * 100).loc[q0:], start, n + 1)
    regs = {"US": us, "EA": gc.passive("EA"), "SE": gc.passive("SE"), "CN": gc.passive("CN")}
    rl = replace(gc.MODERN, fiscal=fiscal, fiscal_at=years_after(start, "2001-06-07"))
    gap = (quarterly("GDPC1") / quarterly("GDPPOT") - 1) * 100
    tg = [Target("unemployment", "u", "M", [(p0 + k, float(um[p0 + k])) for k in range(1, n + 1)], 0.75),
          Target("output gap", "y", "Q", [(q0 + k, float(gap[q0 + k] - gap[q0])) for k in range(1, 16)], 1.0)]
    return Episode("2000-03", start, n, regs, {r: rl for r in regs},
                   gc.Shock(equity={"US": eq}, demand={"US": dem}), tg, fitted=False)


# ------------------------------------------------------------------ the post-war US recessions (decision 82's additions)
# the energy term for the US (case.ENERGY: the pass-through of crude to consumer energy prices, this quarter and the next,
# measured on 1990Q1-2026Q2 at the tag paths-pre-signfix; consumption's share of GDP; spending lost per unit of a higher
# energy bill), carried back to earlier decades as approximate; energy's share of spending measured at each start
US_ENERGY = (0.2308, 0.0986, 0.675, 0.4)


def us_state(start: str, okun: float, stimulus: float) -> gc.Region:
    """The US at the end of month `start`, measured where a public series exists (FRED): unemployment (UNRATE), the funds
    rate (FEDFUNDS), core PCE prices' twelve-month inflation (PCEPILFE), household and business debt over GDP (CMDEBT,
    BCNSDODNS), household equity over GDP (Z.1), real exports over real GDP; the quarterly ones at the start's quarter.
    Approximate, as for 2000-03: speed 0.9, replacement 0.35, floating share 0.25, bank capital 10% and loans 65% of
    GDP, trade, the spread cap; the discretionary response `stimulus`, % of GDP a year."""
    p0 = pd.Period(start, "M")
    q0 = p0.asfreq("Q")
    gdp, z1 = quarterly("GDP"), quarterly("BOGZ1LM153064475Q", end=True)
    core = monthly("PCEPILFE")
    hh, biz = quarterly("CMDEBT")[q0] / 1000, quarterly("BCNSDODNS")[q0] / 1000
    return gc.Region("US", 1.0, float(monthly("UNRATE")[p0]), float(monthly("FEDFUNDS")[p0]),
                     float((core[p0] / core[p0 - 12] - 1) * 100), 0.0, okun, 0.9, 0.35, float(hh / gdp[q0] * 100),
                     float((hh + biz) / gdp[q0] * 100), 0.25, float(z1[q0] / 1000 / gdp[q0]), 0.0, 10.0, 65.0,
                     float(quarterly("EXPGSC1")[q0] / quarterly("GDPC1")[q0]),
                     {"EA": 0.2, "CN": 0.02, "SE": 0.005, "RoW": 0.775}, stimulus, 3.0, 0.0, 0.0)


def us_episode(name: str, start: str, months: int, okun: float, *, rules: gc.Rules, stimulus: float = 2.5,
               energy: bool = False, path: bool = True, fitted: bool = True, notes: str = "") -> Episode:
    """A post-war US recession from the end of month `start`, by month, on the measured state (us_state) and measured
    shocks: household equity's fall from the start's quarter (Z.1, read by month between quarter ends), the change in
    residential investment's share of GDP and in real exports against the start's quarter (each a quarter's average in its
    middle month), and with `energy` the oil price (FRED WTISPLC, its three-month average by month: the pass-through
    was measured on quarters' averages), energy's share of consumer spending at the
    start (PCE energy goods and services over PCE) and headline PCE's twelve-month inflation at the start. With `path`
    the Fed's rate is the funds rate as set (FRED FEDFUNDS; Rules.policy "path"). No exogenous credit losses (the
    model's own loss rule only). Targets: unemployment and core PCE's twelve-month inflation by month (the months before
    the start from the data), the output gap's change from the start's quarter by quarter (GDPC1 / GDPPOT)."""
    p0 = pd.Period(start, "M")
    q0 = p0.asfreq("Q")
    us = us_state(start, okun, stimulus)
    z1 = quarterly("BOGZ1LM153064475Q", end=True)
    zq = (1 - z1.loc[q0:] / z1[q0]).clip(lower=0.0)
    eq = at_quarter_ends(zq, start, months + 1)
    res = quarterly("PRFI") / quarterly("GDP") * 100
    xq, gq = quarterly("EXPGSC1"), quarterly("GDPC1")
    dem = (at_mid_quarter((res - res[q0]).loc[q0:], start, months + 1)
           + at_mid_quarter(((xq - xq[q0]) / gq[q0] * 100).loc[q0:], start, months + 1))
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
          Target("output gap", "y", "Q", [(q, float(gap[q] - gap[q0])) for q in full], 1.0)]
    return Episode(name, start, months, regs, {r: rl for r in regs}, sh, tg, fitted=fitted, before=before, notes=notes)


def e1973(okun: float) -> Episode:
    """1973-75: the oil embargo (from 17 October 1973) and the Fed's rate as set; expectations largely adaptive
    (anchor 0.2 on the start's own core inflation, formed on headline: second-round effects; approximate); the Tax
    Reduction Act of 1975 (signed 29 March 1975; about 1.4% of GDP, mostly within the year: approximate) as a one-year
    stimulus. Price controls (Phase IV ended in April 1974) are not modelled."""
    us = us_state("1973-09", okun, 1.4)
    rl = replace(gc.MODERN, anchor=0.2, pi_star=us.pi0, expect_from="headline", fiscal_quarters=4,
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
    core inflation (0.6, the eroded rules' weight: approximate); the 1990 budget agreement (signed 5 November 1990) as
    consolidation (the model's rule: cuts growing with unemployment's rise)."""
    us = us_state("1990-06", okun, 2.5)
    rl = replace(gc.MODERN, anchor=0.6, pi_star=us.pi0, fiscal="austerity", fiscal_at=years_after("1990-06", "1990-11-05"))
    return us_episode("1990-91", "1990-06", 30, okun, rules=rl, energy=True)


# ------------------------------------------------------------------ the fit
PARAMS = ("sigma", "money", "debt_deflation", "kappa_1930", "okun_us", "impulse_1930_pct_gdp", "a_r")
BOUNDS = [(0, 15), (0, 15), (0, 0.5), (0.03, 1.0), (0.4, 1.0), (0, 10), (0.03, 0.15)]


@functools.lru_cache(maxsize=1)
def _base() -> tuple:
    """The episodes with their measured parts, built once at unit Okun and no impulse."""
    return e1929(0.7, 0.0), e2007(0.7), e2000(0.7), e1973(0.7), e1981(0.7), e1990(0.7)


def episodes(theta) -> list:
    """The episodes at the fit's parameters: the US Okun slope and 1930's spending collapse are the episodes' own."""
    sigma, money, dd, k30, okun, imp, ar = theta
    out = []
    for ep in _base():
        regs = {**ep.regions, "US": replace(ep.regions["US"], okun=okun)}
        shock = ep.shock
        if ep.name == "1929-33":
            shock = replace(shock, demand={"US": shock.demand["US"] - imp * conf_profile(ep.months)})
        e = replace(ep, regions=regs, shock=shock)
        e._where = ep.where()
        out.append(e)
    return out


def common(theta, cm0: gc.Common = gc.Common()) -> gc.Common:
    sigma, money, dd, k30, okun, imp, ar = theta
    return replace(cm0, sigma=sigma, money=money, debt_deflation=dd, kappa_1930=k30, a_r=ar)


def loss(theta, build=episodes) -> float:
    sigma, money, dd, k30, okun, imp, ar = theta
    if min(sigma, money, dd, k30, imp) < 0 or not 0.3 <= okun <= 1.0:
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


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    import json
    fp = json.load(open(os.path.join(gc.ROOT, "results", "global_crash.json"), encoding="utf-8"))["validation"]["fitted"]
    theta = [fp[k] for k in PARAMS]
    print("the quarterly fit's parameters, run monthly:", dict(zip(PARAMS, theta)), "loss", round(loss(theta), 2))
    report(theta)


def fit():
    """The monthly fit: the quarterly fit's search (global_crash.fit) on the episodes marked fitted."""
    from scipy.optimize import differential_evolution
    best = differential_evolution(loss, BOUNDS, seed=7, popsize=20, maxiter=150, tol=1e-7, polish=True)
    n = sum(len(ep.where()) for ep in episodes(best.x) if ep.fitted)
    return best.x, float(best.fun), n
