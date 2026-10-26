# global_crash.py — could an AI shock become a Great Depression, and a systemic one? Four economies — the US, the euro
# area, Sweden, China — with the euro area in two regions since 2026-10-27, France and the rest of the union (decision
# 70), each with the demand and household machinery of demand.py / households.py in reduced form, and the four
# amplifiers the single-country layers leave out:
#   1. recessions trigger adoption: a share of cyclical job loss becomes permanent each quarter (firms that cut in a
#      downturn automate rather than rehire — the "jobless recovery" pattern since the 1980s), on top of a slow
#      structural displacement drift;
#   2. banks: credit losses above normal deplete capital; lost capital widens credit spreads, which cut demand; without
#      deposit insurance, lost capital also runs the money stock down (1930-33); a backstop (lender of last resort,
#      recapitalisation) caps the spread and floors capital;
#   3. trade and a shared risk mood: exports follow partners' output (imports fall about twice as fast as output in a
#      slump); tariffs cut them; the size-weighted bank stress of the four adds to every region's spreads;
#   4. rules that change under pressure: the policy rule (a Taylor rule with a floor, or the 1930s' gold-standard
#      passivity), unemployment support, discretionary fiscal response or austerity, deposit insurance, tariffs, and
#      how firmly expectations are anchored.
# Plus debt deflation (fixed money debts against a price level falling below the one the debts were written for) and
# the relief floating-rate borrowers get when rates fall.
#
# Two waves (her call, 2026-09-24: robotics is a year or two out at least). By default every job is exposed from the
# start at average pay (the uniform case, as fitted). With the split (Waves), work is grouped by occupation
# (exposure.py, ILOSTAT): cognitive (ISCO 1-4) exposed now; physical (6-9) only once robotics arrives, after a lag;
# in-person services (5) in neither. The drift and the adoption in recessions act only on work that can be automated
# at the time: recessions cut physical work two to three times as fast as the whole (US 2007-10), so before robotics
# most of a recession's job loss is rehired rather than automated. The displaced carry their group's pay (cognitive
# work pays 1.1-1.2 times the average) and support capped near average pay; spending, bank losses and an income
# guarantee weigh each group's unemployed by that, normalised so a recession's usual mix weighs what the fit assumed.
#
# Care as the absorber (her calls, 2026-09-24: care as the absorber; "there must be a limit to how much care can
# absorb"). Under the split, the displaced can move into health and social work (exposure.care), within three limits:
#   the pace     care's own trend growth (2019-25, acyclical through 2008-10), and under the rules "expand into care"
#                a funded build-out of up to a point of employment a year (approximate: Sweden's municipal build-out
#                of care in the 1970s-80s); eroding and 1930s rules hire none of the displaced;
#   the gate     who moves: displaced women as fast as care can train and hire them, men at their measured propensity
#                to work in care against women's (a quarter of it); so the physical wave, mostly men, moves slowest;
#   the ceiling  care, trend and build-out together, never past the largest share any rich economy employs today
#                (Norway, 20.1% of employment; the US and Sweden stand at 15%).
# Care's trend jobs exist anyway: a displaced worker who takes one takes it from someone who would have entered work,
# so unemployment falls but spending does not (the displaced lose their support, the other person the job). A funded
# build-out adds jobs: its care purchases are output, its workers earn care pay (service and care workers', ISCO 5),
# its cost is net of the support it saves, and Okun's law applies to the rest of output.
#
# The participation margin (her call, 2026-09-25, after decoupling.py): in the US the displaced have been leaving the
# labour force rather than showing up as unemployed (94% of the prime-age fall in employment since its 2024 peak, against
# 12% in 2007-10). A region's exit share of structural displacement (the drift and adoption in recessions) goes out of the
# labour force; cyclical job loss stays unemployment, as measured in recessions. The exits lose the same income: spending,
# bank losses and an income guarantee count everyone not working; measured unemployment and the fiscal triggers keyed to
# it do not (a variant keys them to non-employment). The US AI build-out is measured too (decoupling.py, on information
# processing equipment since 2026-10-26: net of computer imports 0.42 points of GDP below its 2015-22 trend, so the US
# capex leg is zero; the 1.5% assumed at first, then 0.3% on all equipment).
#
# The financing limit (her call, 2026-09-24, after financing.py: the ceiling is financing, not need). The build-out is
# paid for from one source, each with its own limit and its own drag on demand:
#   borrowing       no limit on quantity; a price: the region's long rate rises with the debt the build-out and an
#                   income guarantee add (measured: 15 bp per 10 points of net debt in the euro area, 30 when its banks
#                   are under stress; under 1 bp with a central bank of one's own), passed to private borrowers' spreads;
#   labour taxes    up to the highest take on labour income in the OECD (Austria, 27.9% of GDP), on a wage base that
#                   displacement shrinks; the workers taxed spend half of what they pay (approximate);
#   a levy on AI    a share of the pay the displaced lost, which now accrues to owners (the paper's shift from wages to
#   income          capital); owners spend as the representative household does, so the levy costs no demand here.
# What a source cannot cover is borrowed. Norway's share of employment becomes a marker, and a variant that keeps it.
#
# The dating (decision 43, adopted 2026-10-01): quarter_label(k) — index 0 is the state measured on data to September 2026,
# the end of 2026Q3 (START), so the first simulated quarter, index 1, the quarter of the bust's peak in ai_shock (its first
# losses there, share prices falling from the next quarter on the default dating), is 2026Q4, and index 9 is 2028Q4. One dating. Before 2026-10-01 the labels ran one quarter late (log 29's START = 2026Q4 at index 0, case.py's
# "quarter 1 = 2026Q4" since log 28); labels only: the dynamics never depended on them.
#
# Two additions for the October bust (her request, 2026-09-30; october.py, a record at the tag paths-pre-signfix since
# 2026-10-26), each off by default:
#   energy term  decision 27's condition (as amended 2026-10-01: dated Brent at least 1.25 times its three-year average on a
#                day a bust rule is active; off by default until then). An exogenous oil price by region (Shock.oil,
#                quarterly averages; Shock.oil_before, the quarter before index 0). The model's pi is core inflation (the
#                2007-10 fit targets core PCE); headline pi_h = pi + energy's share of spending x the pass-through of crude
#                to consumer energy prices, this quarter and the next (energy_inflation; measured in october.py at the tag). The higher
#                energy bill is a tax on consumers' other spending (Region.energy_income, approximate). Rules.react_to
#                ("core" | "headline": hands tied) is what the policy rule reacts to, the last quarter's reading
#                (annualised); "headline4" | "core4" read the average of the last four quarters instead (y/y-like; before
#                the start, index 0's reading, which is measured y/y). Rules.expect_from is what expectations adapt to.
#   spread0      Shock.spread0: a spread already present at the start (index 0), so it reaches spending in the first quarter.
#
# The monetary union and France's sovereign (her suggestion, 2026-10-26: France as its own region, "since that seems to
# be where some of the action is happening"; decision 70). The euro area outside France (EA) and France (FR) share one
# policy rate, set by the union's rule on its members' size-weighted expected inflation, inflation and gap (with one
# member the rule is the region's own, so nothing else moves). France's government has a spread over the union's
# benchmark (its ten-year over Germany's): at the start as measured, plus the price of the debt it adds (the euro area's
# measured slope, financing.py) and any premium the run sets; a share of its rise above its calm level reaches French
# private borrowers; French banks hold its debt, marked to the spread; and with a backstop, recapitalising the banks is
# public debt, so the banks' losses raise the spread (the doom loop, at the measured price of debt). The union's central
# bank can cap the spread (Rules.tpi: the ECB's Transmission Protection Instrument; off unless a run sets it).
#
# Each quarter, region r:
#   policy       i = max(floor, s i_1 + (1-s) [r* + pie + phi_pi (pi_1 - pi*) + phi_y y_1])   (modern; pi_1 headline if
#                react_to is "headline"; the four-quarter average of headline or core if "headline4" or "core4"; in a
#                union, on its members' size-weighted pie, pi_1 and y_1)
#   expectations pie = anchor pi* + (1 - anchor) pi_1
#   demand level D = wealth + capex + unemployed + rate relief + debt deflation + credit + money + trade + fiscal
#                    (+ the energy bill, when the energy term is on)
#   output gap   y = a1 y_1 - a_r (i - pie - r*) + D - a1 D_1
#   inflation    pi = pie + kappa y + tariff pass-through (core); headline pi_h = pi + the energy term (= pi when off)
#   unemployment u moves toward u* - okun y at a regional speed; u* ratchets up by eta x (u - u*) and the drift
#   banks        capital falls by losses above normal (a base rate plus unemployment, the gap, and shock add-ons)
#   spreads      s = s0 + sigma x (capital lost) + global mood, capped under a backstop (France: + the pass-through
#                of its sovereign's spread above its calm level)
#
# VALIDATION FIRST: the same equations, with only the institutions and the shocks changed, must reproduce the US
# 1929-33 (the 1930s settings: gold-standard policy, no deposit insurance, no unemployment support, austerity,
# Smoot-Hawley) and 2007-10 (modern settings), as PATHS: 1930-33 year by year (output, prices, unemployment) and
# 2008-10 quarter by quarter (output gap, unemployment, core inflation). Measured shocks: the stock market, US exports
# (the rest of the world's slump), and in 2007-09 the housebuilding collapse and housing wealth. Seven parameters are
# fitted jointly by a global search: spread per unit of capital lost, the money channel of bank runs, the
# debt-deflation coefficient, the 1930s Phillips slope, the US Okun coefficient, the size of 1930's post-crash spending
# collapse (Romer's; the propagation to 1933 is what is tested), and the rate transmission a_r (bounded to the
# literature's 0.03-0.15). Everything else is fixed from data or the literature, stated. Known bias: unemployment recovers
# from 2009 (and from 2001) faster than the US's did, so it is optimistic about how long joblessness lasts (V3, V4).
# Data (FRED): real GDP annual from 1929 (GDPCA), CPI from 1913 (CPIAUCNS), unemployment from 1948 (UNRATE), real GDP
# and CBO potential quarterly (GDPC1, GDPPOT), core PCE (PCEPILFE), policy rates (DFF, ECBDFR), euro-area HICP and
# unemployment, China CPI, BIS credit to households and to the private non-financial sector (Q..HAM770A, Q..PAM770A);
# France and the rest of the euro area from Eurostat, the BIS, the ECB and the Riksbank (vintage.py). 1933 unemployment 24.9% (Lebergott, the standard series; not on FRED). Region parameters not measured here are
# marked approximate in REGIONS.
#
# Run from paths/:  ../venv/Scripts/python.exe code/global_crash.py
# Out: results/global_crash.json, figures/fig_global_crash.png, figures/fig_global_crash_validation.png,
#      figures/fig_global_crash_waves.png, figures/fig_global_crash_care.png, figures/fig_global_crash_financing.png

from __future__ import annotations

import functools
import json
import os
import sys
from dataclasses import dataclass, field, replace

import numpy as np
import pandas as pd
from scipy.optimize import differential_evolution

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(ROOT), "pinning", "code"))
import lambda_compute2 as _lc  # noqa: E402

_lc.CACHE = os.path.join(ROOT, "cache")
DT = 0.25
R = ("US", "EA", "FR", "SE", "CN")     # EA: the euro area outside France since 2026-10-27 (decision 70)
START = "2026Q3"    # index 0, the start: the regions as measured on data to the end of 2026Q3 (the dated vintage,
                    # cache/start/: monthly series to August or September, quarterly to 2026Q2); index 1, the first
                    # simulated quarter, is 2026Q4 (decision 43)


def quarter_label(k: int) -> str:
    """The calendar quarter of index k: index 0 is START, the quarter the start state is measured on, so index 1 — the
    first simulated quarter, the quarter of ai_shock's peak — is 2026Q4, and index 9 is 2028Q4."""
    return str(pd.Period(START, "Q") + int(k))


def quarter_mid(k):
    """The middle of index k's quarter, in years (for figures): 2026.625 for index 0 (2026Q3), 2026.875 for index 1."""
    p = pd.Period(START, "Q")
    return p.year + (p.quarter - 1) / 4 + 0.125 + np.asarray(k, float) / 4


def fred(sid: str) -> pd.Series:
    s = _lc.pull_fred(sid)
    if s is None:
        raise SystemExit(f"FRED {sid}: not available")
    return s


# ------------------------------------------------------------------ the pieces
@dataclass(frozen=True)
class Region:
    name: str
    size: float                 # share of the four economies' GDP (market exchange rates, approximate)
    u0: float                   # unemployment at the start, %
    i0: float                   # policy rate at the start, %
    pi0: float                  # inflation at the start, % a year
    floor: float                # the lowest policy rate the central bank will set, %
    okun: float                 # unemployment points per point of output gap
    speed: float                # share of the gap between unemployment and its target closed each quarter
    replacement: float          # share of a lost wage public support replaces
    hh_debt: float              # household debt, % of GDP (BIS)
    priv_debt: float            # private non-financial debt, % of GDP (BIS)
    floating: float             # share of household debt repricing with policy within a year
    equity_wealth: float        # household equity and fund holdings, x GDP (approximate)
    ai_capex: float             # AI build-out investment, % of GDP (approximate)
    bank_capital: float         # bank equity, % of GDP (approximate)
    loans: float                # bank loans to the private sector, % of GDP (approximate)
    exports: float              # exports, share of GDP (approximate)
    trade: dict                 # export shares by destination (US, EA, SE, CN, RoW; approximate)
    stimulus: float             # discretionary fiscal response when triggered, % of GDP a year (approximate)
    spread_cap: float           # the most a backstop lets credit spreads widen, points
    eta: float                  # share of cyclical unemployment turning structural each quarter (AI available)
    drift: float                # structural displacement, points of unemployment a year (the paper's slow channel)
    # the two-wave split (exposure.py); unused in the uniform case
    groups: dict = field(default_factory=lambda: {"cognitive": 1 / 3, "in_person": 1 / 3, "physical": 1 / 3})   # employment shares
    premium: dict = field(default_factory=lambda: {"cognitive": 1.0, "in_person": 1.0, "physical": 1.0})       # pay against the average
    benefit_cap: float = 99.0   # pay (x the average) above which unemployment support stops rising (approximate)
    # care as the absorber (exposure.care): share of employment, its pace of growth, and who can move into it
    care_share: float = 0.0     # health and social work, % of employment
    care_trend: float = 0.0     # its growth, points of employment a year (2019-25), acyclical in an ordinary recession
    gate: dict = field(default_factory=lambda: {"cognitive": 1.0, "in_person": 1.0, "physical": 1.0})   # relative entry into care
    # financing (financing.py): taxes on labour income today, % of GDP; the price of added debt, bp per 10 points
    labour_tax: float = 0.0
    debt_slope: float = 0.0
    debt_slope_crisis: float = 0.0
    exit_share: float = 0.0     # share of structural displacement that leaves the labour force (decoupling.py; US measured)
    # the energy term (used only when Shock.oil carries the region): energy's share of consumer spending, the
    # pass-through of crude to consumer energy prices (this quarter, the next; measured), household consumption's share of
    # GDP, spending lost per unit of a higher energy bill (approximate), and headline inflation at the start (None: pi0)
    energy_weight: float = 0.0
    energy_pass: tuple = (0.0, 0.0)
    consumption_share: float = 0.0
    energy_income: float = 0.0
    pi_h0: float | None = None
    # a currency union and a sovereign of its own (decision 70; France): the union whose central bank sets the rate; the
    # government's spread over the union's benchmark at the start and in calm years (points), its debt (% of GDP), its
    # banks' holdings of it (% of GDP), the share of the spread's rise passed to private borrowers, and the capital the
    # banks lose per point of it per unit of holdings (duration times the share held at market value)
    union: str = ""
    sov0: float = 0.0
    sov_calm: float = 0.0
    sov_debt: float = 0.0
    sov_banks: float = 0.0
    sov_pass: float = 0.0
    sov_mtm: float = 0.0


@dataclass(frozen=True)
class Common:
    a1: float = 0.94            # the gap's own persistence a quarter (Laubach-Williams, approximate)
    a_r: float = 0.10           # gap per point of real-rate gap a quarter (Laubach-Williams, approximate)
    r_star: float = 0.75        # neutral real rate, %
    phi_pi: float = 1.5
    phi_y: float = 0.5
    smooth: float = 0.7
    mpc_u: float = 0.8          # spending per krona of lost income, the unemployed
    mpc_rep: float = 0.05
    mpc_b: float = 0.5          # borrowers' spending per krona of debt service relieved
    labour_share: float = 0.6
    wealth_mpc: float = 0.03    # spending per krona of equity wealth, a year
    trade_elasticity: float = 2.0
    tariff_net: float = 0.3     # share of a tariff's export loss not offset by switching to home goods (approximate)
    a_s: float = 1.0            # demand level per point of credit spread (Gilchrist-Zakrajsek range 1-2)
    loss_base: float = 0.4      # normal credit losses, % of loans a year
    loss_u: float = 0.35        # extra losses per point of unemployment above the start, % of loans a year
    loss_y: float = 0.10        # extra losses per point of negative gap
    global_mood: float = 1.0    # spread points per unit of the four's size-weighted capital lost
    kappa: float = 0.15         # modern Phillips slope, % a year per point of gap (Swedish measure 0.13; US similar)
    # fitted jointly on 1929-33 and 2007-09 (fit() below)
    sigma: float = 6.0          # spread points per unit of bank capital lost
    money: float = 8.0          # demand level per unit of capital lost when deposits are uninsured (bank runs)
    debt_deflation: float = 0.15   # demand level per unit of (expected / actual price level - 1) x private debt
    kappa_1930: float = 0.5     # the 1930s Phillips slope (flexible prices and wages)
    # each group's employment change in a recession over all employment's (US 2007-10, exposure.py)
    beta: dict = field(default_factory=lambda: {"cognitive": 0.58, "in_person": 0.27, "physical": 2.34})
    # care as the absorber
    care_ceiling: float = 20.1  # the most care any rich economy employs today, % of employment (Norway 2025, exposure.care)
    care_hire: float = 0.25     # share of the displaced willing to enter care (the gate) trained and hired a quarter: about a
                                # year on average for entry-level care (approximate; 0.10 and 0.50 tested in the checks)
    care_labour_cost: float = 0.75   # pay's share of what care costs (approximate)
    # financing the build-out
    tax_max: float = 27.9       # the highest take on labour income in the OECD, % of GDP (Austria 2024, financing.py)
    mpc_taxed: float = 0.5      # workers' spending per krona of extra tax (approximate; as supporters' in households.py)
    ai_levy: float = 0.5        # share of the displaced's former pay, now owners' income, levied (approximate; a dial)
    stress_crisis: float = 0.2  # bank capital lost above which the crisis price of debt applies


@dataclass(frozen=True)
class Waves:
    """Which work AI can take, and when. split=False is the uniform case: every job exposed from the start."""
    split: bool = False
    robot_lag: float = 2.0      # years until robotics can take physical work
    robot_ramp: float = 1.0     # years over which it arrives in full
    absorb: bool = False        # care takes in the displaced (under the split; how much is the rules' care setting)


UNIFORM = Waves()
GROUPS = ("cognitive", "in_person", "physical")


@dataclass(frozen=True)
class Rules:
    """Institutions — what changes between the 1930s and now, and what pressure could change again."""
    name: str = "modern"
    policy: str = "taylor"      # "taylor" (with the floor) | "gold" (passive; no reflation)
    gold_hike: tuple = ()       # (quarter, points) raises to defend the parity
    anchor: float = 0.9         # weight of the target in expected inflation
    pi_star: float = 2.0
    insured: bool = True        # deposit insurance: no money channel from bank runs
    backstop: bool = True       # lender of last resort, recapitalisation: spreads capped, capital floored
    capital_floor: float = 0.6  # share of capital a recapitalisation restores to, under a backstop
    support: bool = True        # unemployment support at the region's replacement rate
    fiscal: str = "stimulus"    # "stimulus" | "none" | "austerity" | "guarantee"
    guarantee: float = 0.9      # under "guarantee": the share of lost labour income the state replaces, with no time limit
    trigger: float = 2.0        # unemployment points above the start that trigger the fiscal response
    fiscal_quarters: int = 8
    tariff: float = 0.0         # points of tariff everyone raises on everyone
    tariff_q: int = 2           # quarter the tariffs arrive
    kappa_1930s: bool = False
    # care: "trend" (keeps hiring at its pace, as through 2008-10 — the jobs exist anyway, so the displaced take them
    # from people who would have entered work), "cut" (no hiring from the displaced; austerity is in fiscal), "expand"
    # (the state funds new care jobs on top, at up to care_pace points of employment a year, once unemployment is
    # trigger points up, until care reaches the ceiling)
    care: str = "trend"
    care_pace: float = 1.0      # approximate: Sweden's municipal build-out of care in the 1970s-80s ran near a point a year
    care_finance: str = "borrowing"   # "borrowing" | "labour taxes" | "ai levy"
    care_cap: float | None = None     # the region's own ceiling for care, % of employment (None: the common ceiling);
                                      # a financing limit reached before Norway's share (case.py: care capping out)
    trigger_on: str = "unemployment"  # what the fiscal triggers watch: "unemployment" | "non-employment" (incl. exits)
    react_to: str = "core"            # what the policy rule reacts to: "core" (the model's pi) | "headline" (hands tied);
                                      # "headline4" | "core4": the average of the last four quarters (y/y-like)
    expect_from: str = "core"         # what expectations adapt to: "core" | "headline" (second-round effects)
    tpi: float | None = None          # the union's central bank caps a member's sovereign spread this many points above
                                      # its start (the ECB's Transmission Protection Instrument); None: not activated


MODERN = Rules()
THIRTIES = Rules(name="1930s", policy="gold", anchor=0.2, pi_star=0.0, insured=False, backstop=False, support=False,
                 fiscal="austerity", tariff=15.0, tariff_q=3, kappa_1930s=True, care="cut")
ERODED = Rules(name="rules erode under pressure", anchor=0.6, backstop=False, fiscal="austerity", tariff=20.0, tariff_q=3, care="cut")
EXPANDED = Rules(name="rules expand under pressure", fiscal="guarantee", trigger=1.5)   # an income guarantee: the deficits branch
CARE = Rules(name="rules expand into care", care="expand", trigger=1.5)                # today's rules plus a funded care build-out
CARE_TAX = replace(CARE, name="care financed by labour taxes", care_finance="labour taxes")
CARE_LEVY = replace(CARE, name="care financed by a levy on AI income", care_finance="ai levy")


@dataclass
class Shock:
    """Exogenous paths, per region: equity decline (share), AI capex decline (share), extra credit losses (% of loans
    a year), each as a function of the quarter."""
    equity: dict = field(default_factory=dict)
    capex: dict = field(default_factory=dict)
    losses: dict = field(default_factory=dict)
    demand: dict = field(default_factory=dict)       # other exogenous demand level, % of GDP
    drift: dict = field(default_factory=dict)        # the displacement pace by quarter, points of the labour force a year,
                                                     # in place of the region's constant drift (case.py: a pace that rises)
    spread: dict = field(default_factory=dict)       # an exogenous premium on borrowing by quarter, points, passed to private
                                                     # borrowers (case.py: deficit and sovereign worry)
    spread0: dict = field(default_factory=dict)      # a spread already present at the start (index 0), points
    oil: dict = field(default_factory=dict)          # the energy term: the oil price by quarter, quarterly averages in the
                                                     # region's currency, index 0 = the start's quarter
    oil_before: dict = field(default_factory=dict)   # the quarter before index 0 (for crude's change into it)


def ramp(total: float, start: int, quarters: int, n: int, hold: bool = True) -> np.ndarray:
    x = np.zeros(n)
    for k in range(n):
        f = min(max((k - start + 1) / quarters, 0.0), 1.0)
        x[k] = total * f if (hold or k < start + quarters) else 0.0
    return x


def pulse(total_pct_loans: float, start: int, quarters: int, n: int) -> np.ndarray:
    x = np.zeros(n)
    x[start:start + quarters] = total_pct_loans / (quarters * DT)       # % of loans a year while it lasts
    return x


def energy_inflation(oil, before: float, w, passthrough: tuple) -> np.ndarray:
    """Headline minus core from crude oil, points a year, by quarter: energy's share of spending w times the pass-through of
    crude's change (quarterly averages, annualised log %) to consumer energy prices, this quarter (b0) and the next (b1).
    oil[j] is quarter j's price and `before` the quarter before index 0; w a number, or one per quarter (the share when the
    change comes). Index 0 carries the change into it only (its own lag lies before the data)."""
    g = 400 * np.diff(np.log(np.concatenate([[float(before)], np.asarray(oil, float)])))
    w = np.broadcast_to(np.asarray(w, float), g.shape)
    b0, b1 = passthrough
    e = b0 * w * g
    e[1:] += b1 * w[:-1] * g[:-1]
    return e


def energy_paths(oil, before: float, g: Region, n: int) -> tuple:
    """The energy term for region g: headline minus core (points a year) and the rise in consumers' energy bill since the
    start, % of GDP (consumption's share of GDP x energy's share of spending x consumer energy prices' log change)."""
    e = energy_inflation(np.asarray(oil, float)[:n], before, g.energy_weight, g.energy_pass)
    bill = np.zeros(n)
    bill[1:] = g.consumption_share * np.cumsum(e[1:]) * DT
    return e, bill


# ------------------------------------------------------------------ the simulation
def wave_weights(g: Region, rl: Rules, cm: Common, waves: Waves) -> dict | None:
    """Under the split: a recession's usual job-loss mix by group, and each group's weight per point of unemployment
    for spending (lost net pay), bank losses (debt, taken proportional to pay) and an income guarantee (pay) — relative
    to that mix, so a recession's usual unemployment weighs what the fit assumed. None in the uniform case."""
    if not waves.split:
        return None
    rep = g.replacement if rl.support else 0.0
    z = sum(g.groups[q] * cm.beta[q] for q in GROUPS)
    mix = {q: g.groups[q] * cm.beta[q] / z for q in GROUPS}
    rep_q = {q: rep * min(1.0, g.benefit_cap / g.premium[q]) for q in GROUPS}
    net = {q: g.premium[q] * (1 - rep_q[q]) for q in GROUPS}
    net_mix = sum(mix[q] * net[q] for q in GROUPS)
    pay_mix = sum(mix[q] * g.premium[q] for q in GROUPS)
    w_care = g.premium["in_person"]          # what the displaced earn in care: service and care workers' pay (ISCO 5)
    return {"mix": mix, "rep": rep_q, "spend": {q: net[q] / net_mix * (1 - rep) for q in GROUPS},
            "pay": {q: g.premium[q] / pay_mix for q in GROUPS}, "w_care": w_care,
            # in care's existing jobs: the displaced's pay gap plus the care pay of the person who would have been
            # hired instead, and who stays out of work — their whole previous pay, with no support
            "spend_trend": {q: g.premium[q] / net_mix * (1 - rep) for q in GROUPS},
            # in newly funded care jobs: the pay gap only
            "spend_care": {q: max(g.premium[q] - w_care, 0.0) / net_mix * (1 - rep) for q in GROUPS},
            "pay_care": {q: max(g.premium[q] - w_care, 0.0) / pay_mix for q in GROUPS}}


ABSORBED = (("cognitive", "s_cog", "at_cog", "ax_cog"), ("physical", "s_phys", "at_phys", "ax_phys"))


def robots(k: int, waves: Waves) -> float:
    """The share of physical work robotics can take at quarter k (1 in the uniform case)."""
    if not waves.split:
        return 1.0
    t = k * DT
    if waves.robot_ramp <= 0:
        return float(t >= waves.robot_lag)
    return min(max((t - waves.robot_lag) / waves.robot_ramp, 0.0), 1.0)


def displaced(o: dict, j: int, g: Region, w: dict) -> dict:
    """Points of unemployment above the start at quarter j, by group: the structural additions by wave, plus the
    cyclical part in a recession's usual mix."""
    struct = {"cognitive": o["s_cog"][j], "in_person": 0.0, "physical": o["s_phys"][j]}
    cy = o["u"][j] - o["u_star"][j]
    if cy >= 0:
        return {q: struct[q] + w["mix"][q] * cy for q in GROUPS}
    st = sum(struct.values())
    f = max(o["u"][j] - g.u0 + o["out"][j], 0.0) / st if st > 1e-12 else 0.0
    return {q: struct[q] * f for q in GROUPS}


def financing_room(o: dict, j: int, g: Region, rl: Rules, cm: Common) -> float:
    """What the build-out's source can pay for at quarter j, % of GDP a year (unlimited when borrowing)."""
    if rl.care_finance == "labour taxes":
        # the highest take on a wage base the displaced have left (pay-weighted), less what labour already pays
        return cm.tax_max * (1 - o["pay_weighted"][j] / 100) - g.labour_tax
    if rl.care_finance == "ai levy":
        lost = sum((o[s][j] + o[at][j] + o[ax][j]) * g.premium[q] for q, s, at, ax in ABSORBED)
        return cm.ai_levy * cm.labour_share * lost
    return float("inf")


def simulate(regions: dict, rules: dict, shock: Shock, cm: Common = Common(), n: int = 24, active=None,
             waves: Waves = UNIFORM) -> dict:
    """regions: {code: Region}; rules: {code: Rules}; active: regions simulated (others held at zero gap)."""
    active = active or list(regions)
    names = list(regions)
    out = {r: {k: np.zeros(n) for k in ("y", "u", "u_star", "pi", "P", "Pexp", "i", "k", "s", "D", "stress", "stim",
                                        "d_wealth", "d_capex", "d_unemp", "d_relief", "d_debt", "d_credit", "d_money",
                                        "d_trade", "d_fiscal", "loss", "deficit_extra", "s_cog", "s_phys", "pay_weighted",
                                        "at_cog", "at_phys", "ax_cog", "ax_phys", "d_care", "care_cost", "care",
                                        "debt_extra", "premium", "d_fin", "room", "out",
                                        "pi_h", "e_pi", "e_bill", "d_energy", "sov")} for r in names}
    W = {r: wave_weights(regions[r], rules[r], cm, waves) for r in names}
    for r in names:
        g, rl = regions[r], rules[r]
        o = out[r]
        o["u"][0] = o["u_star"][0] = g.u0
        o["pi"][0] = g.pi0
        o["pi_h"][0] = g.pi0
        o["P"][0] = o["Pexp"][0] = 1.0
        o["i"][0] = g.i0
        o["k"][0] = g.bank_capital
        o["s"][0] = 0.0
        o["care"][0] = g.care_share
        if r in shock.spread0:                      # a spread already present at the start
            o["s"][0] = shock.spread0[r]
        o["sov"][0] = g.sov0
        if g.sov_debt > 0:                          # its sovereign's spread above its calm level, passed to borrowers
            o["s"][0] += g.sov_pass * (g.sov0 - g.sov_calm)
        if r in shock.oil:                          # the energy term: headline minus core, and the energy bill
            o["e_pi"][:], o["e_bill"][:] = energy_paths(shock.oil[r], shock.oil_before[r], g, n)
            if g.pi_h0 is not None:
                o["pi_h"][0] = g.pi_h0
    fiscal_left = {r: 0 for r in names}
    fiscal_on = {r: False for r in names}

    def partner(r, q):
        """Whether q is another member of region r's currency union."""
        return bool(regions[r].union) and q != r and q in regions and regions[q].union == regions[r].union

    def inside(r):
        """The share of region r's exports that go to the other members of its union (no tariffs inside it)."""
        return sum(v for q, v in regions[r].trade.items() if partner(r, q))

    def expected(r, k):
        rl = rules[r]
        return rl.anchor * rl.pi_star + (1 - rl.anchor) * (out[r]["pi_h"] if rl.expect_from == "headline" else out[r]["pi"])[k - 1]

    def seen(r, k):
        """The inflation the policy rule reacts to (core, the model's pi; headline when the rules say hands are tied)."""
        rl, o = rules[r], out[r]
        if rl.react_to in ("headline4", "core4"):   # four quarters' average; before the start, index 0's (y/y)
            src = o["pi_h"] if rl.react_to == "headline4" else o["pi"]
            return sum(src[max(j, 0)] for j in range(k - 4, k)) / 4
        return (o["pi_h"] if rl.react_to == "headline" else o["pi"])[k - 1]

    for k in range(1, n):
        mood = cm.global_mood * sum(regions[r].size * out[r]["stress"][k - 1] for r in names)
        rate = {}                                   # a currency union: one rate on its members' size-weighted readings
        for u in {regions[r].union for r in names if regions[r].union}:
            m = [r for r in names if regions[r].union == u and r in active and rules[r].policy == "taylor"]
            wt = sum(regions[r].size for r in m)
            if not m or wt <= 0:
                continue
            lead = rules[u] if u in m else rules[m[0]]
            avg = lambda f: sum(regions[q].size * f(q) for q in m) / wt  # noqa: E731
            target = (cm.r_star + avg(lambda q: expected(q, k)) + cm.phi_pi * (avg(lambda q: seen(q, k)) - lead.pi_star)
                      + cm.phi_y * avg(lambda q: out[q]["y"][k - 1]))
            rate[u] = max(min(regions[q].floor for q in m), cm.smooth * out[m[0]]["i"][k - 1] + (1 - cm.smooth) * target)
        for r in names:
            g, rl, o = regions[r], rules[r], out[r]
            if r not in active:
                o["u"][k], o["u_star"][k], o["pi"][k], o["i"][k], o["k"][k] = g.u0, g.u0, g.pi0, g.i0, g.bank_capital
                o["pi_h"][k] = g.pi0
                o["care"][k] = g.care_share
                o["P"][k] = o["P"][k - 1] * (1 + g.pi0 / 100 * DT)
                o["Pexp"][k] = o["P"][k]
                continue
            pis = rl.pi_star
            pie = expected(r, k)
            # policy (on core inflation, the model's pi; on headline when the rules say hands are tied; a union's rate)
            if rl.policy == "taylor":
                if g.union in rate:
                    i = rate[g.union]
                else:
                    target = cm.r_star + pie + cm.phi_pi * (seen(r, k) - pis) + cm.phi_y * o["y"][k - 1]
                    i = max(g.floor, cm.smooth * o["i"][k - 1] + (1 - cm.smooth) * target)
            else:                                   # gold: rates drift down only as far as the market takes them; no reflation
                i = max(0.0, o["i"][k - 1] - 0.25 * max(o["i"][k - 1] - 1.0, 0.0))
                for (q, pts) in rl.gold_hike:
                    if k == q:
                        i += pts
            o["i"][k] = i
            rgap = i - pie - cm.r_star
            # demand levels (% of GDP)
            eq = shock.equity.get(r, np.zeros(n))[k]
            cx = shock.capex.get(r, np.zeros(n))[k]
            d_wealth = -cm.wealth_mpc * g.equity_wealth * eq * 100
            d_capex = -g.ai_capex * cx
            rep = g.replacement if rl.support else 0.0
            if W[r] is None:
                d_unemp = -(cm.mpc_u - cm.mpc_rep) * cm.labour_share * max(o["u"][k - 1] - g.u0 + o["out"][k - 1], 0.0) * (1 - rep)
                owed = max(o["u"][k - 1] - g.u0 + o["out"][k - 1], 0.0) * max(rl.guarantee - rep, 0.0)
            else:
                du = displaced(o, k - 1, g, W[r])
                lost = sum(du[q] * W[r]["spend"][q] for q in GROUPS)
                lost += sum(o[at][k - 1] * W[r]["spend_trend"][q] + o[ax][k - 1] * W[r]["spend_care"][q] for q, _, at, ax in ABSORBED)
                d_unemp = -(cm.mpc_u - cm.mpc_rep) * cm.labour_share * lost
                owed = sum(du[q] * W[r]["pay"][q] * max(rl.guarantee - W[r]["rep"][q], 0.0) for q in GROUPS)
            # a funded care build-out buys care: its pay and other costs are output (its jobs are counted directly below)
            built = o["ax_cog"][k - 1] + o["ax_phys"][k - 1]
            d_care = cm.labour_share * W[r]["w_care"] * built / cm.care_labour_cost if W[r] is not None else 0.0
            if W[r] is not None:
                o["care_cost"][k] = cm.labour_share * (W[r]["w_care"] * built / cm.care_labour_cost
                                                       - sum(o[ax][k - 1] * g.premium[q] * W[r]["rep"][q] for q, _, _, ax in ABSORBED))
            # how the build-out is paid for: what a source cannot cover is borrowed
            cost = max(o["care_cost"][k], 0.0)
            room = financing_room(o, k - 1, g, rl, cm) if W[r] is not None else float("inf")
            covered = min(cost, max(room, 0.0))
            o["room"][k] = room
            d_fin = -(cm.mpc_taxed - cm.mpc_rep) * covered if rl.care_finance == "labour taxes" else 0.0
            o["d_fin"][k] = d_fin
            d_relief = (cm.mpc_b - cm.mpc_rep) * g.floating * g.hh_debt / 100 * (g.i0 - i)
            d_debt = -cm.debt_deflation * g.priv_debt / 100 * max(o["Pexp"][k - 1] / o["P"][k - 1] - 1, 0.0) * 100
            d_credit = -cm.a_s * o["s"][k - 1]
            d_money = 0.0 if rl.insured else -cm.money * o["stress"][k - 1]
            partners = {q: out[q]["y"][k - 1] for q in names}
            partners["RoW"] = sum(regions[q].size * partners[q] for q in names)
            tariff = rl.tariff if k >= rl.tariff_q else 0.0
            # a tariff point cuts exports about a point (short-run trade elasticity ~1); imports fall too, so only part
            # of it (tariff_net, uncertainty and broken supply chains) is lost to demand rather than switched home.
            # Exports inside a union pay none (the EU's single market: decision 70); rl.tariff is on the rest. And a
            # union partner's slump reaches a member only as far as it differs from the member's own: each part keeps
            # the whole's own dynamics, which held the union's internal trade (so a shock to all of it moves it as the
            # one region did, E2), while a shock to one part spills over to the other
            spill = sum(g.trade[q] * (partners[q] - o["y"][k - 1] if partner(r, q) else partners[q]) for q in g.trade)
            d_trade = g.exports * (cm.trade_elasticity * spill - cm.tariff_net * tariff * (1 - inside(r)))
            unemp_up = o["u"][k - 1] - g.u0 + (o["out"][k - 1] if rl.trigger_on == "non-employment" else 0.0)
            if not fiscal_on[r] and unemp_up >= rl.trigger:
                fiscal_on[r], fiscal_left[r] = True, rl.fiscal_quarters
            d_fiscal = 0.0
            if rl.fiscal == "stimulus" and fiscal_on[r] and fiscal_left[r] > -4:
                d_fiscal = 0.8 * g.stimulus * min(1.0, (fiscal_left[r] + 4) / 4)       # full for the programme, tapered over a year
                fiscal_left[r] -= 1
            elif rl.fiscal == "guarantee" and unemp_up >= rl.trigger:
                d_fiscal = (cm.mpc_u - cm.mpc_rep) * cm.labour_share * owed
                o["deficit_extra"][k] = cm.labour_share * owed
            elif rl.fiscal == "austerity" and unemp_up >= rl.trigger:
                d_fiscal = -0.8 * min(0.5 * unemp_up / 5, 2.0)          # consolidation as deficits grow, up to 2% of GDP
            d_other = shock.demand.get(r, np.zeros(n))[k]
            D = d_wealth + d_capex + d_unemp + d_relief + d_debt + d_credit + d_money + d_trade + d_fiscal + d_other + d_care + d_fin
            if r in shock.oil:                      # the energy bill: a tax on consumers' other spending
                o["d_energy"][k] = -g.energy_income * o["e_bill"][k]
                D += o["d_energy"][k]
            for key, v in (("d_wealth", d_wealth), ("d_capex", d_capex), ("d_unemp", d_unemp), ("d_relief", d_relief),
                           ("d_debt", d_debt), ("d_credit", d_credit), ("d_money", d_money), ("d_trade", d_trade), ("d_fiscal", d_fiscal),
                           ("d_care", d_care)):
                o[key][k] = v
            o["D"][k] = D
            y = cm.a1 * o["y"][k - 1] - cm.a_r * rgap + D - cm.a1 * o["D"][k - 1]
            y = max(y, -60.0)
            o["y"][k] = y
            kap = cm.kappa_1930 if rl.kappa_1930s else cm.kappa
            pi = pie + kap * y + (0.03 * tariff if k == rl.tariff_q else 0.0) / DT
            o["pi"][k] = pi
            o["pi_h"][k] = pi + o["e_pi"][k] if r in shock.oil else pi
            o["P"][k] = o["P"][k - 1] * (1 + pi / 100 * DT)
            o["Pexp"][k] = o["Pexp"][k - 1] * (1 + pis / 100 * DT)
            # unemployment: the drift and adoption in recessions act only on work that can be automated at the time
            ap = robots(k, waves)
            if W[r] is None:
                m_drift = m_eta = 1.0
            else:
                sh, mix = g.groups, W[r]["mix"]
                m_drift = (sh["cognitive"] + sh["physical"] * ap) / (sh["cognitive"] + sh["physical"])
                m_eta = (mix["cognitive"] + mix["physical"] * ap) / (mix["cognitive"] + mix["physical"])
            add_eta = g.eta * m_eta * max(o["u"][k - 1] - o["u_star"][k - 1], 0.0)
            add_drift = (shock.drift[r][k] if r in shock.drift else g.drift) * m_drift * DT
            # structural displacement: the exit share leaves the labour force, the rest stays unemployed
            x = g.exit_share
            add = min(add_eta + add_drift, max(45.0 - o["u_star"][k - 1] - o["out"][k - 1], 0.0))    # structural non-employment <= 45
            o["u_star"][k] = o["u_star"][k - 1] + (1 - x) * add
            o["out"][k] = o["out"][k - 1] + x * add
            o["s_cog"][k], o["s_phys"][k] = o["s_cog"][k - 1], o["s_phys"][k - 1]
            if W[r] is not None and add_eta + add_drift > 0:
                inc = o["u_star"][k] - o["u_star"][k - 1] + o["out"][k] - o["out"][k - 1]     # after the cap
                p_eta = mix["physical"] * ap / (mix["cognitive"] + mix["physical"] * ap)
                p_drift = sh["physical"] * ap / (sh["cognitive"] + sh["physical"] * ap)
                dp = inc * (add_eta * p_eta + add_drift * p_drift) / (add_eta + add_drift)
                o["s_cog"][k] += inc - dp
                o["s_phys"][k] += dp
            # care takes in the displaced: at its trend pace (jobs that exist anyway) unless the rules cut it, plus a
            # funded build-out under "expand"; limited by the pace, by who moves (the gate), and by the ceiling
            for _, _, at, ax in ABSORBED:
                o[at][k], o[ax][k] = o[at][k - 1], o[ax][k - 1]
            # care's level (% of employment): its trend and any build-out, together never past the ceiling
            ceiling = cm.care_ceiling if rl.care_cap is None else rl.care_cap
            grow = 0.0 if rl.care == "cut" else min(g.care_trend * DT, max(ceiling - o["care"][k - 1], 0.0))
            o["care"][k] = o["care"][k - 1] + grow
            if W[r] is not None and waves.absorb and rl.care != "cut":
                weight = {q: o[s][k] * g.gate[q] for q, s, _, _ in ABSORBED}
                pool = sum(weight.values())
                potential = cm.care_hire * pool
                a_t = max(min(grow, potential), 0.0)   # a care sector that is shrinking (France, 2019-25) takes in nobody
                a_x = 0.0
                if rl.care == "expand" and unemp_up >= rl.trigger:
                    built = o["ax_cog"][k - 1] + o["ax_phys"][k - 1]
                    per_point = cm.labour_share * (W[r]["w_care"] / cm.care_labour_cost
                                                   - sum(weight[q] / pool * g.premium[q] * W[r]["rep"][q] for q, _, _, _ in ABSORBED)) if pool > 0 else 1.0
                    afford = financing_room(o, k - 1, g, rl, cm) / per_point - built if per_point > 0 else float("inf")
                    a_x = max(min(rl.care_pace * DT, potential - a_t, ceiling - o["care"][k], afford), 0.0)
                o["care"][k] += a_x
                if pool > 0:
                    for q, s, at, ax in ABSORBED:
                        f = weight[q] / pool
                        o[s][k] -= (a_t + a_x) * f
                        o[at][k] += a_t * f
                        o[ax][k] += a_x * f
                    o["u_star"][k] -= (1 - x) * (a_t + a_x)
                    o["out"][k] -= x * (a_t + a_x)
            # Okun's law for the rest of output: the build-out's own jobs are counted directly
            target = max(o["u_star"][k] - g.okun * (y - d_care), 1.5)
            o["u"][k] = min(o["u"][k - 1] + g.speed * (target - o["u"][k - 1]), 50.0 - o["out"][k])
            if W[r] is None:
                debt_up = max(o["u"][k] - g.u0 + o["out"][k], 0.0)
            else:
                du = displaced(o, k, g, W[r])
                debt_up = sum(du[q] * W[r]["pay"][q] for q in GROUPS)     # debts taken proportional to pay
                debt_up += sum((o[at][k] + o[ax][k]) * W[r]["pay_care"][q] for q, _, at, ax in ABSORBED)
            o["pay_weighted"][k] = debt_up
            # banks
            loss = cm.loss_base + cm.loss_u * debt_up + cm.loss_y * max(-y, 0.0) + shock.losses.get(r, np.zeros(n))[k]
            o["loss"][k] = loss
            kk = o["k"][k - 1] - (loss - cm.loss_base) * g.loans / 100 * DT
            if g.sov_debt > 0 and k >= 2:           # the banks' holdings of their sovereign, marked to its spread
                kk -= g.sov_banks * g.sov_mtm * (o["sov"][k - 1] - o["sov"][k - 2]) / 100
            recap = 0.0
            if rl.backstop:
                recap = max(rl.capital_floor * g.bank_capital - kk, 0.0)
                kk = max(kk, rl.capital_floor * g.bank_capital)
            o["k"][k] = max(kk, 0.0)
            o["stress"][k] = max(0.0, 1.0 - o["k"][k] / g.bank_capital)
            s = cm.sigma * o["stress"][k] + mood
            if rl.backstop:
                s = min(s, g.spread_cap)
            # the price of the debt a guarantee and a borrowed build-out add, passed to private borrowers
            cost = max(o["care_cost"][k], 0.0)
            borrowed = o["deficit_extra"][k] + (cost if rl.care_finance == "borrowing" else max(cost - max(o["room"][k], 0.0), 0.0))
            # with its sovereign modelled, recapitalising the banks is public debt (the doom loop's bank-to-state leg)
            o["debt_extra"][k] = o["debt_extra"][k - 1] + borrowed * DT + (recap if g.sov_debt > 0 else 0.0)
            slope = g.debt_slope_crisis if o["stress"][k] > cm.stress_crisis else g.debt_slope
            o["premium"][k] = slope / 100 * o["debt_extra"][k] / 10
            if g.sov_debt > 0:                      # the sovereign's spread: at the start, plus the price of the debt added
                sov = g.sov0 + o["premium"][k] + (shock.spread[r][k] if r in shock.spread else 0.0)
                if rl.tpi is not None:              # the union's central bank caps it (the ECB's TPI)
                    sov = min(sov, g.sov0 + rl.tpi)
                o["sov"][k] = sov
                s += g.sov_pass * (sov - g.sov_calm)
            else:
                s += o["premium"][k]
                if r in shock.spread:
                    s += shock.spread[r][k]
            o["s"][k] = s
            o["stim"][k] = d_fiscal
    return out


def summary(out: dict, regions: dict, horizon_q: int | None = None) -> dict:
    res = {}
    for r, o in out.items():
        n = len(o["y"]) if horizon_q is None else horizon_q
        res[r] = {"gap_min": round(float(o["y"][:n].min()), 2), "gap_min_quarter": int(np.argmin(o["y"][:n])),
                  "unemployment_max": round(float(o["u"][:n].max()), 2), "structural_unemployment_end": round(float(o["u_star"][n - 1]), 2),
                  "inflation_min": round(float(o["pi"][:n].min()), 2), "inflation_max": round(float(o["pi"][:n].max()), 2),
                  "price_level_end": round(float(o["P"][n - 1]), 3), "bank_capital_lost_max": round(float(o["stress"][:n].max()), 3),
                  "spread_max": round(float(o["s"][:n].max()), 2), "quarters_at_floor": int(sum(o["i"][:n] <= regions[r].floor + 1e-9)),
                  "policy_min": round(float(o["i"][:n].min()), 2), "no_bottom": bool(o["y"][:n].min() <= -59.99),
                  "guarantee_cost_max_pct_gdp": round(float(o["deficit_extra"][:n].max()), 2),
                  "unemployment_max_quarter": int(np.argmax(o["u"][:n])),
                  "unemployment_year2": round(float(o["u"][min(8, n - 1)]), 2),
                  "displaced_cognitive_end": round(float(o["s_cog"][n - 1]), 2), "displaced_physical_end": round(float(o["s_phys"][n - 1]), 2),
                  "pay_weighted_rise_max": round(float(o["pay_weighted"][:n].max()), 2),
                  "absorbed_into_existing_care_jobs_end": round(float(o["at_cog"][n - 1] + o["at_phys"][n - 1]), 2),
                  "absorbed_into_new_care_jobs_end": round(float(o["ax_cog"][n - 1] + o["ax_phys"][n - 1]), 2),
                  "absorbed_physical_share_end": round(float((o["at_phys"][n - 1] + o["ax_phys"][n - 1])
                                                             / max(o["at_cog"][n - 1] + o["at_phys"][n - 1] + o["ax_cog"][n - 1] + o["ax_phys"][n - 1], 1e-12)), 3),
                  "care_share_end": round(float(o["care"][n - 1]), 2),
                  "care_cost_max_pct_gdp": round(float(o["care_cost"][:n].max()), 2),
                  "debt_added_end_pct_gdp": round(float(o["debt_extra"][n - 1]), 2),
                  "out_of_labour_force_end": round(float(o["out"][n - 1]), 2),
                  "not_working_rise_max": round(float((o["u"][:n] - regions[r].u0 + o["out"][:n]).max()), 2),
                  "debt_premium_max_bp": round(float(100 * o["premium"][:n].max()), 1),
                  "financing_room_start_pct_gdp": None if not np.isfinite(o["room"][1]) else round(float(o["room"][1]), 2),
                  "financing_room_end_pct_gdp": None if not np.isfinite(o["room"][n - 1]) else round(float(o["room"][n - 1]), 2),
                  "sovereign_spread_max": round(float(o["sov"][:n].max()), 2)}
    w = {r: regions[r].size for r in out}
    tot = sum(w.values())
    nn = len(out["US"]["y"]) if horizon_q is None else horizon_q
    res["four_weighted_gap_min"] = round(float(min(sum(w[r] * out[r]["y"][k] for r in out) / tot for k in range(nn))), 2)
    return res


# ------------------------------------------------------------------ the regions today (2026) and the US of 1929 / 2007
def yoy(s: pd.Series, periods: int) -> float:
    return float((s.iloc[-1] / s.iloc[-1 - periods] - 1) * 100)


def regions_today() -> dict:
    """The regions at the start (index 0, 2026Q3), measured on the dated vintage in cache/start/ (vintage.py; its manifest
    names each source) where a public series exists: unemployment, the policy rate and core inflation (the model's pi
    is core: the 2007-10 fit targets core PCE) for the US, the euro area and Sweden, and US household equity over GDP (Fed
    Z.1); household and private debt from BIS (FRED; the BIS itself for France and the rest of the euro area); France
    and the rest of the union split from the euro area by difference (decision 70). Approximate and stated: sizes, Okun
    slopes and speeds, the other regions' equity wealth and build-out, bank capital and loans, trade, China's start."""
    import vintage
    end = pd.Period(START, "Q").end_time                   # index 0 is measured on data to the end of its quarter
    at = lambda sid: vintage.read(sid).loc[:end]  # noqa: E731
    v = lambda sid: float(at(sid).iloc[-1])  # noqa: E731
    cn_cpi = fred("CHNCPIALLMINMEI")
    last = lambda sid: float(fred(sid).iloc[-1])  # noqa: E731
    se = json.load(open(os.path.join(ROOT, "results", "households.json"), encoding="utf-8"))["sweden_start"]
    sw_cyc = json.load(open(os.path.join(ROOT, "results", "demand.json"), encoding="utf-8"))["sweden_cycle"]
    z1, gdp = at("BOGZ1LM153064475Q"), at("GDP")
    q = min(z1.index[-1], gdp.index[-1])
    us_equity = float(z1[q] / 1000 / gdp[q])                    # Z.1 levels in millions, GDP in billions (annual rate)
    # France and the rest of the euro area (decision 70): Eurostat's unemployment, the rest of the union by difference
    # (August, the last month both have); France's core HICP, the rest's by France's weight in the euro area's HICP
    # (approximate: the headline basket's weight, applied to the euro area-19 core); the BIS's credit, the rest by GDP
    # weights; the two sizes the euro area's quarter of the four economies split by GDP (2025)
    fu, eu, fn, en = (at(x) for x in ("FR_UNEMPLOYMENT", "EA21_UNEMPLOYMENT", "FR_UNEMPLOYED", "EA21_UNEMPLOYED"))
    mq = min(x.index[-1] for x in (fu, eu, fn, en))
    rest_u = float((en[mq] - fn[mq]) / (en[mq] / eu[mq] - fn[mq] / fu[mq]))
    gfr, gea = at("FR_GDP_MEUR"), at("EA21_GDP_MEUR")
    y_ = min(gfr.index[-1], gea.index[-1])
    share_fr = float(gfr[y_] / gea[y_])
    w_fr = v("FR_HICP_WEIGHT") / 1000
    fr_pi = vintage.yoy(at("FR_HICP_CORE"))
    rest_pi = (vintage.yoy(at("00XEFDEZ19M086NEST")) - w_fr * fr_pi) / (1 - w_fr)
    rest = lambda xm, fr: (v(xm) - share_fr * v(fr)) / (1 - share_fr)  # noqa: E731
    sov = (at("FRGVB10Y") - at("DEGVB10Y")).dropna()                      # France's ten-year over Germany's, daily
    fr_banks = 100 * v("FR_MFI_GOV_SECURITIES") / float(gfr[y_])
    us = Region("US", 0.44, v("UNRATE"), v("DFF"), vintage.yoy(at("PCEPILFE")), 0.0, 0.6, 0.9, 0.35, last("QUSHAM770A"),
                last("QUSPAM770A"), 0.10, us_equity, 1.5, 8.0, 45.0, 0.11,
                {"EA": 0.155, "FR": 0.025, "CN": 0.07, "SE": 0.005, "RoW": 0.745}, 2.5, 3.0, 0.05, 1.0)
    # the rest of the union: its exports now include those to France (about 4% of its GDP: approximate)
    ea = Region("EA", round(0.25 * (1 - share_fr), 4), rest_u, v("ECBDFR"), rest_pi, -0.5, 0.4, 0.35,
                0.60, rest("XM_BIS_HH", "FR_BIS_HH"), rest("XM_BIS_PNF", "FR_BIS_PNF"), 0.40, 0.6, 0.3, 10.0, 90.0, 0.246,
                {"US": 0.168, "FR": 0.16, "CN": 0.067, "SE": 0.034, "RoW": 0.571}, 1.5, 3.0, 0.03, 0.5, union="EA")
    # France (approximate and stated: mortgages almost all fixed, so a small floating share; the big banks' CET1 about
    # EUR 0.4tn, loans to households and firms about GDP; exports a third of GDP, about half of them to the rest of the
    # union; a smaller discretionary response under the EU's excessive deficit procedure; half of its sovereign's spread
    # rise passed on to private borrowers; the banks' holdings about seven years' duration, 40% of them at market value)
    fr = Region("FR", round(0.25 * share_fr, 4), float(fu[mq]), v("ECBDFR"), fr_pi, -0.5, 0.4, 0.35, 0.65, v("FR_BIS_HH"),
                v("FR_BIS_PNF"), 0.05, 0.6, 0.3, 13.0, 100.0, 0.32, {"US": 0.08, "EA": 0.47, "SE": 0.01, "CN": 0.04, "RoW": 0.40},
                1.0, 3.0, 0.03, 0.5, union="EA", sov0=float(sov.iloc[-1]),
                sov_calm=float(sov.loc["2025-07-01":"2026-06-30"].mean()), sov_debt=v("FR_GOV_DEBT"), sov_banks=fr_banks,
                sov_pass=0.5, sov_mtm=7 * 0.4)
    sw = Region("SE", 0.01, v("SEUNRATE"), v("SECBREPOEFF"), vintage.yoy(at("00XEFDSEM086NEST")), -0.5, 0.4, 0.4, 0.65,
                last("QSEHAM770A"), last("QSEPAM770A"), se["floating_share"], 1.4, 0.4, 15.0, 130.0, 0.50,
                {"US": 0.09, "EA": 0.355, "FR": 0.045, "CN": 0.04, "RoW": 0.47}, 2.0, 3.0, 0.03, 0.6)
    cn = Region("CN", 0.30, 5.2, 1.4, yoy(cn_cpi, 12), 0.0, 0.25, 0.3, 0.15, last("QCNHAM770A"), last("QCNPAM770A"),
                0.8, 0.3, 1.0, 20.0, 180.0, 0.19, {"US": 0.15, "EA": 0.13, "FR": 0.02, "SE": 0.005, "RoW": 0.695}, 3.0, 1.5, 0.04, 0.8)
    # the two-wave split: occupations and pay measured (exposure.py); where support stops rising, approximate — the US
    # (half of pay up to state maxima, near 0.9 of average pay), the euro area (Germany's ceiling near 1.8, France's
    # far higher, Italy's and Spain's below average: about 1.5 weighted), Sweden (the unemployment fund's cap sits near
    # 0.85 of average pay, but most white-collar workers carry union income insurance above it for the first months:
    # 1.5), China (support too thin for a cap to matter). Since France is its own region (decision 70): France 3.0 (its
    # cap sits far above average pay), the rest of the union 1.3
    fin = json.load(open(os.path.join(ROOT, "results", "financing.json"), encoding="utf-8"))
    tax = {r: v["labour_taxes_pct_gdp"] for r, v in fin["labour_taxes"]["regions"].items()}
    sl = fin["borrowing"]["slopes"]
    own = sl["own central bank 2010-24"]["long_rate"]["bp_per_10_points_net_debt"]       # China: taken as own central bank
    euro = (sl["euro area 2010-24"]["long_rate"]["bp_per_10_points_net_debt"], sl["euro area crisis 2010-13"]["long_rate"]["bp_per_10_points_net_debt"])
    slope = {"US": (own, own), "SE": (own, own), "CN": (own, own), "EA": euro, "FR": euro}
    # the US build-out and where its displaced go, measured (decoupling.py); the other regions' approximate, as stated
    dec = json.load(open(os.path.join(ROOT, "results", "decoupling.json"), encoding="utf-8"))
    us_capex = max(dec["ai_build_out"]["net_above_2015_22_trend_pts"], 0.0)
    us_exit = min(max(dec["where_the_displaced_go"]["prime_age_25_54"]["since_the_employment_peak"]["exit_share"], 0.0), 1.0)
    us = replace(us, ai_capex=us_capex, exit_share=us_exit)
    exj = json.load(open(os.path.join(ROOT, "results", "exposure.json"), encoding="utf-8"))
    ex, cr = exj["regions"], exj["care"]["regions"]
    caps = {"US": 0.9, "EA": 1.3, "FR": 3.0, "SE": 1.5, "CN": 1.0}
    regs = {r: replace(g, groups=ex[r]["share"], premium=ex[r]["premium"], benefit_cap=caps[r], care_share=cr[r]["care_share_pct"],
                       care_trend=cr[r]["care_trend_pts_a_year"], gate=cr[r]["gate"], labour_tax=tax[r],
                       debt_slope=slope[r][0], debt_slope_crisis=slope[r][1])
            for r, g in (("US", us), ("EA", ea), ("FR", fr), ("SE", sw), ("CN", cn))}
    return {**regs, "_notes": {"SE_okun_measured_on_growth_changes": sw_cyc["okun"], "SE_start": se}}


def us_1929(cm_okun: float) -> Region:
    return Region("US", 1.0, 3.2, 5.0, 0.0, 0.0, cm_okun, 0.9, 0.0, 70.0, 150.0, 0.2, 0.8, 0.0, 12.0, 60.0, 0.05,
                  {"EA": 0.3, "CN": 0.0, "SE": 0.0, "RoW": 0.7}, 0.0, 99.0, 0.0, 0.0)


def us_2007(cm_okun: float) -> Region:
    return Region("US", 1.0, 4.8, 4.25, 2.2, 0.125, cm_okun, 0.9, 0.35, 98.0, 170.0, 0.25, 1.4, 0.0, 10.0, 65.0, 0.11,
                  {"EA": 0.2, "CN": 0.05, "SE": 0.005, "RoW": 0.745}, 2.5, 3.0, 0.0, 0.0)


def passive(r: str) -> Region:
    return Region(r, 0.0, 5.0, 2.0, 2.0, 0.0, 0.4, 0.5, 0.5, 50, 100, 0.3, 0.5, 0.0, 10, 80, 0.1, {"US": 1.0}, 0, 3, 0, 0)


LEBERGOTT = {1929: 3.2, 1930: 8.7, 1931: 15.9, 1932: 23.6, 1933: 24.9}     # US unemployment, % (the standard series)


def validation_targets() -> dict:
    gdp = fred("GDPCA")
    cpi = fred("CPIAUCNS")
    cpi_a = cpi.groupby(cpi.index.year).mean()
    g = gdp.copy(); g.index = g.index.year
    q = fred("GDPC1"); pot = fred("GDPPOT"); u = fred("UNRATE"); core = fred("PCEPILFE")
    gap = (q / pot.reindex(q.index) - 1) * 100
    gap0 = float(gap.loc["2007-10-01"])
    gq = (gap.loc["2008-01-01":"2010-12-31"] - gap0)
    uq = u.groupby(u.index.to_period("Q")).mean().loc["2008Q1":"2010Q4"]
    core_q = core.groupby(core.index.to_period("Q")).mean()
    core_yoy = ((core_q / core_q.shift(4) - 1) * 100).loc["2008Q1":"2010Q4"]
    return {"1929-33": {"years": [1930, 1931, 1932, 1933],
                        "output_over_1929": [round(float(g[y] / g[1929]), 4) for y in (1930, 1931, 1932, 1933)],
                        "prices_over_1929": [round(float(cpi_a[y] / cpi_a[1929]), 4) for y in (1930, 1931, 1932, 1933)],
                        "unemployment": [LEBERGOTT[y] for y in (1930, 1931, 1932, 1933)]},
            "2007-09": {"quarters": [str(x) for x in uq.index],
                        "gap_change": [round(float(x), 2) for x in gq.values], "unemployment": [round(float(x), 2) for x in uq.values],
                        "core_inflation": [round(float(x), 2) for x in core_yoy.values]}}


def run_1929(cm: Common, okun: float, impulse: float = 0.0) -> dict:
    n = 18                                                   # 1929Q3 .. 1933Q4
    regs = {"US": us_1929(okun), "EA": passive("EA"), "SE": passive("SE"), "CN": passive("CN")}
    rules = {r: replace(THIRTIES, gold_hike=((9, 2.0),)) for r in regs}          # autumn 1931: raised to defend gold
    # the Dow: -40% by Nov 1929, -86% by mid-1932; and the post-crash collapse of spending on durables and building
    # (Romer 1990) as a demand level that fades over two years: its size is fitted; what is tested is the propagation
    conf = np.array([-impulse * max(0.0, 1 - max(k - 2, 0) / 8) if k >= 1 else 0.0 for k in range(n)])
    # the rest of the world's slump, measured: US real exports against 1929, % of 1929 GDP (FRED EXPGSCA / GDPCA),
    # annual values placed mid-year and interpolated by quarter
    e, g = fred("EXPGSCA"), fred("GDPCA")
    ex = {d.year: float((e[d] - e.iloc[0]) / g.iloc[0] * 100) for d in e.index if d.year <= 1934}
    tq = 1929.5 + np.arange(n) * DT
    exq = np.interp(tq, [y + 0.5 for y in sorted(ex)], [ex[y] for y in sorted(ex)])
    sh = Shock(equity={"US": np.minimum(ramp(0.40, 1, 1, n) + ramp(0.45, 3, 10, n), 0.86)}, demand={"US": conf + exq})
    return simulate(regs, rules, sh, cm, n, active=["US"])["US"]


def demand_2007(n: int = 13) -> dict:
    """run_2007's exogenous demand levels, % of GDP, each with the sign of its own measured change (a fall is a drag):
    housing wealth -30% (x1.5 GDP, 0.05 a krona a year) staying down; the housebuilding collapse, measured as residential
    investment's share of GDP from 2007Q4 on (FRED PRFI / GDP); the rest of the world's slump, measured as US real exports
    against 2007Q4, % of 2007Q4 GDP (FRED EXPGSC1 / GDPC1). check_global_crash S1 tests the signs."""
    house = -0.05 * 1.5 * ramp(0.30, 1, 6, n) * 100
    res = fred("PRFI") / fred("GDP").reindex(fred("PRFI").index) * 100
    res = res.loc["2007-10-01":].values[:n]
    build = res - res[0]           # entered as -(res - res[0]), a stimulus, until 2026-10-26 (STATE Log 40-41)
    ex = ((fred("EXPGSC1") - fred("EXPGSC1").loc["2007-10-01"]) / fred("GDPC1").loc["2007-10-01"] * 100).loc["2007-10-01":].values[:n]
    return {"housing wealth": house, "housebuilding": build, "exports": ex}


def run_2007(cm: Common, okun: float, drop: tuple = ()) -> dict:
    """`drop`: demand_2007 components left out (check_global_crash S2)."""
    n = 13                                                   # 2007Q4 .. 2010Q4
    regs = {"US": us_2007(okun), "EA": passive("EA"), "SE": passive("SE"), "CN": passive("CN")}
    rules = {r: replace(MODERN, fiscal_quarters=8) for r in regs}
    # equity -50% by 2009Q1, back to -20% by 2010Q2; mortgage-related credit losses ~ 3.5% of loans over two years
    eq = np.interp(np.arange(n), [0, 5, 10, 12], [0.0, 0.5, 0.2, 0.2])
    dem = sum(v for k, v in demand_2007(n).items() if k not in drop)
    sh = Shock(equity={"US": eq}, losses={"US": pulse(3.5, 2, 8, n)}, demand={"US": dem})
    return simulate(regs, rules, sh, cm, n, active=["US"])["US"]


def _q(sid: str) -> pd.Series:
    """A FRED series as quarterly averages, indexed by quarter."""
    s = fred(sid)
    return s.groupby(s.index.to_period("Q")).mean()


def run_2000(cm: Common, okun: float) -> dict:
    """Out of sample (not in the fit): the dot-com bust, 2000Q1 .. 2003Q4, with today's rules and measured shocks — US
    household equity (Fed Z.1, directly and indirectly held, BOGZ1LM153064475Q) as the fall from 2000Q1; equipment
    investment's share of GDP (Y033RC1Q027SBEA / GDP) and real exports against 2000Q1 (EXPGSC1 / GDPC1) as demand levels,
    each with the sign of its own change. Start values measured (FRED): unemployment, the funds rate, core PCE inflation,
    household and business debt (CMDEBT, BCNSDODNS), equity wealth and exports over GDP. No exogenous credit losses (the
    model's own loss rule only). check_global_crash V4 compares it with the data."""
    n, q0 = 16, pd.Period("2000Q1", "Q")
    gdp, z1 = _q("GDP"), _q("BOGZ1LM153064475Q")
    core = _q("PCEPILFE")
    hh, biz = _q("CMDEBT")[q0] / 1000, _q("BCNSDODNS")[q0] / 1000             # Z.1 levels are in millions; GDP in billions
    us = Region("US", 1.0, float(_q("UNRATE")[q0]), float(_q("DFF")[q0]), float((core[q0] / core[q0 - 4] - 1) * 100), 0.0, okun,
                0.9, 0.35, float(hh / gdp[q0] * 100), float((hh + biz) / gdp[q0] * 100),
                0.25, float(z1[q0] / 1000 / gdp[q0]), 0.0, 10.0, 65.0, float(_q("EXPGSC1")[q0] / _q("GDPC1")[q0]),
                {"EA": 0.2, "CN": 0.02, "SE": 0.005, "RoW": 0.775}, 2.5, 3.0, 0.0, 0.0)
    regs = {"US": us, "EA": passive("EA"), "SE": passive("SE"), "CN": passive("CN")}
    rules = {r: replace(MODERN, fiscal_quarters=8) for r in regs}
    qs = [q0 + k for k in range(n)]
    eq = np.maximum(1 - np.array([z1[q] for q in qs]) / z1[q0], 0.0)
    eqp = _q("Y033RC1Q027SBEA") / gdp * 100
    x, g = _q("EXPGSC1"), _q("GDPC1")
    dem = np.array([eqp[q] - eqp[q0] for q in qs]) + np.array([(x[q] - x[q0]) / g[q0] * 100 for q in qs])
    return simulate(regs, rules, Shock(equity={"US": eq}, demand={"US": dem}), cm, n, active=["US"])["US"]


def targets_2000() -> dict:
    """The data run_2000 is compared with: quarterly US unemployment and the change in the output gap (GDPC1 / GDPPOT) from
    2000Q1, 2000Q2 .. 2003Q4."""
    q0 = pd.Period("2000Q1", "Q")
    u, gap = _q("UNRATE"), (_q("GDPC1") / _q("GDPPOT") - 1) * 100
    qs = [q0 + k for k in range(1, 16)]
    return {"quarters": [str(q) for q in qs], "unemployment": [round(float(u[q]), 2) for q in qs],
            "gap_change": [round(float(gap[q] - gap[q0]), 2) for q in qs]}


def annual(x, first_q_of_1930: int = 2) -> list:
    return [float(np.mean(x[first_q_of_1930 + 4 * j: first_q_of_1930 + 4 * j + 4])) for j in range(4)]


def fit_loss(theta, tg, cm0):
    sigma, money, dd, k30, okun, imp, ar = theta
    if min(sigma, money, dd, k30, imp) < 0 or not 0.3 <= okun <= 1.0:
        return 1e6
    cm = replace(cm0, sigma=sigma, money=money, debt_deflation=dd, kappa_1930=k30, a_r=ar)
    a = run_1929(cm, okun, imp)
    b = run_2007(cm, okun)
    kk = np.arange(len(a["y"])) * DT
    outp = annual((1 + a["y"] / 100) * 1.02 ** kk)
    t1, t2 = tg["1929-33"], tg["2007-09"]
    e = list((np.array(outp) - t1["output_over_1929"]) / 0.03) + list((np.array(annual(a["P"])) - t1["prices_over_1929"]) / 0.03)
    e += list((np.array(annual(a["u"])) - t1["unemployment"]) / 2.0)
    w = 1 / np.sqrt(3)                                       # twelve quarters count about as much as four years
    e += list(w * (b["y"][1:13] - np.array(t2["gap_change"])) / 1.0) + list(w * (b["u"][1:13] - np.array(t2["unemployment"])) / 0.75)
    e += list(w * (b["pi"][1:13] - np.array(t2["core_inflation"])) / 0.75)
    return float(np.sum(np.square(e)))


def fit(tg: dict):
    cm0 = Common()
    bounds = [(0, 15), (0, 15), (0, 0.5), (0.03, 1.0), (0.4, 1.0), (0, 10), (0.03, 0.15)]   # + a_r, the rate transmission
    best = differential_evolution(fit_loss, bounds, args=(tg, cm0), seed=7, popsize=20, maxiter=150, tol=1e-7, polish=True)
    sigma, money, dd, k30, okun, imp, ar = best.x
    cm = replace(cm0, sigma=sigma, money=money, debt_deflation=dd, kappa_1930=k30, a_r=ar)
    a, b = run_1929(cm, okun, imp), run_2007(cm, okun)
    kk = np.arange(len(a["y"])) * DT
    got = {"1929-33": {"output_over_1929": [round(v, 4) for v in annual((1 + a["y"] / 100) * 1.02 ** kk)],
                       "prices_over_1929": [round(v, 4) for v in annual(a["P"])], "unemployment": [round(v, 1) for v in annual(a["u"])],
                       "bank_capital_lost": round(float(a["stress"].max()), 3)},
           "2007-09": {"gap_change": [round(float(v), 2) for v in b["y"][1:13]], "unemployment": [round(float(v), 2) for v in b["u"][1:13]],
                       "core_inflation": [round(float(v), 2) for v in b["pi"][1:13]], "bank_capital_lost": round(float(b["stress"].max()), 3)}}
    n_obs = 12 + 36
    params = {"sigma": round(sigma, 3), "money": round(money, 3), "debt_deflation": round(dd, 4), "kappa_1930": round(k30, 3),
              "okun_us": round(okun, 3), "impulse_1930_pct_gdp": round(imp, 2), "a_r": round(ar, 4), "loss": round(float(best.fun), 2),
              "rms_standardised_error": round(float(np.sqrt(best.fun / n_obs)), 3)}
    return cm, okun, {"fitted": params, "model": got, "targets": tg, "runs": (a, b)}


# ------------------------------------------------------------------ the AI crash
# the bust's sizes: the fall in household equity at the trough as first built (the US 0.40; since 2026-10-26 the US
# follows its measured 2000-02 fall, -44.7%, and the other regions keep these ratios to it: approximate, stated); the
# share of the above-trend build-out lost as first built (since 2026-10-26 the measured share, 76% at most); losses on
# AI-related lending, % of loans in all (assumed, not measured: the 2000-02 C&I charge-off excess came to 3.8% of C&I
# loans, and the model's own loss rule already produces most of a recession's bank losses: run_2000 makes 2.05% of loans)
BUST_EQUITY = {"US": 0.40, "EA": 0.25, "FR": 0.25, "SE": 0.30, "CN": 0.25}
BUST_CAPEX = 0.6
BUST_LOSSES = {"US": 1.5, "EA": 0.5, "FR": 0.5, "SE": 0.5, "CN": 1.0}
Q0_2000 = pd.Period("2000Q1", "Q")                                # the quarter of the 2000 equity peak (10 Mar 2000)
WINDOW_2000 = 24                                                  # 2000Q1-2005Q4: household equity back to its peak


@functools.lru_cache(maxsize=1)
def bust_2000() -> dict:
    """The legs of the 2000-02 bust, measured, by quarters k from the quarter of the equity peak (k = 0 = 2000Q1),
    k = 0 .. 23 (to 2005Q4; after it 2007's bust would enter the window), each normalised so that its largest value in
    the window is 1, the measured levels beside them (ai_shock runs on those; 2026-10-26, STATE Logs 42-44):
      equity  US household corporate equities, directly and indirectly held (Fed Z.1, BOGZ1LM153064475Q, end of quarter):
              the fall from 2000Q1, floored at zero (a fall from the peak; no rise above it); trough at k = 10 (2002Q3),
              -44.7%; back at the peak by 2005Q4;
      capex   the build-out as decoupling.py measures it (information processing equipment, software, power and
              communication structures, less imports of computers; BEA) over GDP, above its 1990-94 linear trend: the
              share of 2000Q1's excess lost (negative while it still grows: growing for three quarters, above the peak
              quarter's level for four; 76% lost at most, nineteen quarters after the peak);
      losses  the C&I loan charge-off rate above its 1997-99 mean (the Fed Board's release, all banks, SA; FRED
              CORBLACBS), as weights summing to one; peak at k = 10.
    The measured levels are returned beside the shapes (check_global_crash B1 recomputes them from the cache)."""
    qs = [Q0_2000 + k for k in range(WINDOW_2000)]
    qd = lambda sid, end=False: (lambda s: s.groupby(s.index.to_period("Q")).last() if end  # noqa: E731
                                 else s.groupby(s.index.to_period("Q")).mean())(fred(sid))
    z = qd("BOGZ1LM153064475Q", True)
    eq = np.array([max(0.0, 1 - float(z[q] / z[Q0_2000])) for q in qs])
    gdp = qd("GDP")
    net = sum(sign * qd(sid) / gdp * 100 for sid, sign in (("Y034RC1Q027SBEA", 1), ("B985RC1Q027SBEA", 1),
                                                          ("W003RC1Q027SBEA", 1), ("B852RC1Q027SBEA", -1))).dropna()
    yr = net.groupby(net.index.year).mean().loc[1990:1994]
    slope, icpt = np.polyfit(yr.index.values.astype(float), yr.values, 1)
    gap = np.array([float(net[q] - (slope * (q.year + (q.quarter - 1) / 4 + 0.125) + icpt)) for q in qs])
    cx = 1 - gap / gap[0]
    ci = qd("CORBLACBS")
    base = float(ci[(ci.index >= pd.Period("1997Q1", "Q")) & (ci.index <= pd.Period("1999Q4", "Q"))].mean())
    ex = np.array([max(0.0, float(ci[q]) - base) for q in qs])
    return {"equity": eq / eq.max(), "capex": cx / cx.max(), "losses": ex / ex.sum(),
            "measured": {"equity_fall": eq, "capex_share_lost": cx, "chargeoff_excess": ex, "capex_excess_2000Q1": float(gap[0]),
                         "chargeoff_base_1997_99": base}}


def _on(arr: np.ndarray, onset: float, n: int, speed: float, after: float) -> np.ndarray:
    """A measured level path from index `onset` (k = 0 there; it may be fractional, for a peak inside a quarter), time
    running `speed` times as fast, linearly between quarters; before the onset 0, after the window `after`."""
    k = (np.arange(n) - onset) * speed
    out = np.interp(k, np.arange(len(arr)), arr, left=0.0, right=after)
    return np.where(k < 0, 0.0, out)


def _spread(w: np.ndarray, onset: float, n: int, speed: float) -> np.ndarray:
    """Weights summing to one, spread over quarters from `onset` at `speed` through their cumulative path, so that the
    total is kept whatever the onset and the speed (exactly the weights at an integer onset and speed 1)."""
    cum = np.concatenate([[0.0], np.cumsum(w)])
    c = lambda x: np.interp(x, np.arange(len(cum)), cum, left=0.0, right=float(cum[-1]))  # noqa: E731
    i = np.arange(n)
    return c((i + 1 - onset) * speed) - c((i - onset) * speed)


def ai_shock(n: int, scale: float = 1.0, speed: float = 1.0, delay: float = 0, shape: str = "2000") -> Shock:
    """A dot-com-sized bust of the AI build-out, from the quarter of the peak (index 1 + delay; `delay` may be
    fractional): US household equity on its measured 2000-02 fall (-44.7% at the trough, ten quarters after the peak,
    then recovering; bust_2000), the other regions at the first build's ratios to the US; the build-out losing its
    measured share of the excess above trend (still growing for three quarters, 76% lost at most); losses on AI-related
    lending (private credit and its bank lenders) of BUST_LOSSES, assumed, spread on the measured path of 2000-02's bank
    losses. All times `scale`; `speed` runs the path faster. Since 2026-10-26 (STATE Logs 42-44). shape="ramp": the bust
    as first built (2026-09-24 to 2026-10-26): equity (US -40%) and the build-out (60%) down in a straight line over
    4 / speed quarters from 1 + delay and held there for good, the losses spread evenly over 8 / speed quarters from
    2 + delay."""
    eq, ls = BUST_EQUITY, BUST_LOSSES
    if shape == "ramp":
        qf, ql = max(1, round(4 / speed)), max(2, round(8 / speed))
        return Shock(equity={r: ramp(scale * v, 1 + delay, qf, n) for r, v in eq.items()},
                     capex={r: ramp(scale * 0.6 * 100, 1 + delay, qf, n) / 100 for r in eq},
                     losses={r: pulse(scale * v, 2 + delay, ql, n) for r, v in ls.items()})
    m = bust_2000()["measured"]
    onset = 1 + delay
    e = _on(m["equity_fall"], onset, n, speed, 0.0)                         # US household equity, measured
    c = _on(m["capex_share_lost"], onset, n, speed, float(m["capex_share_lost"][-1]))
    w = _spread(bust_2000()["losses"], onset, n, speed)
    return Shock(equity={r: scale * (v / eq["US"]) * e for r, v in eq.items()},
                 capex={r: scale * c for r in eq},
                 losses={r: scale * v * w / DT for r, v in ls.items()})


def scenarios(cm: Common, regions: dict) -> dict:
    """Three dials: the rules; displacement (the bust alone, or the bust with the paper's slow structural drift); and
    how much of each recession's job loss becomes permanent (as usual, or three times that)."""
    n = 24
    runs = {}
    regs = {r: regions[r] for r in R}
    rules_set = (("modern rules", MODERN), ("rules erode under pressure", ERODED), ("rules expand under pressure", EXPANDED),
                 ("the 1930s' rules", replace(THIRTIES, tariff=20.0, pi_star=2.0)))
    dials = (("bust only", 0.0, 1.0), ("bust + displacement", 1.0, 1.0), ("bust + displacement, recessions trigger adoption x3", 1.0, 3.0))
    waves = [("", UNIFORM)] + [(f"two waves, robotics in {lag} years", Waves(split=True, robot_lag=float(lag))) for lag in (1, 2, 3)]
    for rules_name, rl in rules_set:
        for dial, drift_mult, eta_mult in dials:
            rg = {r: replace(g, eta=g.eta * eta_mult, drift=g.drift * drift_mult) for r, g in regs.items()}
            for wl, wv in waves:
                runs[(rules_name, dial, wl)] = simulate(rg, {r: rl for r in R}, ai_shock(n), cm, n, waves=wv)
    # the participation margin: fiscal triggers that watch non-employment (exits included) rather than unemployment
    for dial, drift_mult, eta_mult in dials[1:]:
        rg = {r: replace(g, eta=g.eta * eta_mult, drift=g.drift * drift_mult) for r, g in regs.items()}
        for rules_name, rl in (("modern rules, triggers on non-employment", replace(MODERN, trigger_on="non-employment")),
                               ("rules expand under pressure, triggers on non-employment", replace(EXPANDED, trigger_on="non-employment"))):
            for wl, wv in waves[:1] + waves[2:3]:
                runs[(rules_name, dial, wl)] = simulate(rg, {r: rl for r in R}, ai_shock(n), cm, n, waves=wv)
    # displacement without a bust (where the US is): the paper's drift and adoption as usual, no AI crash
    for rules_name, rl in (("modern rules", MODERN), ("modern rules, triggers on non-employment", replace(MODERN, trigger_on="non-employment")),
                           ("rules expand under pressure", EXPANDED)):
        runs[(rules_name, "displacement without a bust", "")] = simulate(regs, {r: rl for r in R}, Shock(), cm, n)
    # care as the absorber: robotics two years out; how much care takes in is the rules' care setting (today's and the
    # guarantee's: its trend pace; eroding and 1930s rules: none; "expand into care": a funded build-out on top)
    absorb = Waves(split=True, robot_lag=2.0, absorb=True)
    wl = "two waves, robotics in 2 years, care absorbs"
    for dial, drift_mult, eta_mult in dials[1:]:
        rg = {r: replace(g, eta=g.eta * eta_mult, drift=g.drift * drift_mult) for r, g in regs.items()}
        for rules_name, rl in rules_set[:3] + (("rules expand into care", CARE),):
            runs[(rules_name, dial, wl)] = simulate(rg, {r: rl for r in R}, ai_shock(n), cm, n, waves=absorb)
        fast = {r: replace(CARE, care_pace=3.0) for r in R}
        runs[("rules expand into care", dial, "two waves, robotics in 2 years, care absorbs, three points a year, no ceiling")] = \
            simulate(rg, fast, ai_shock(n), replace(cm, care_ceiling=100.0), n, waves=absorb)
        open_gate = {r: replace(g, gate={q: 1.0 for q in GROUPS}) for r, g in rg.items()}
        runs[("rules expand into care", dial, "two waves, robotics in 2 years, care absorbs, men enter care as women do")] = \
            simulate(open_gate, {r: CARE for r in R}, ai_shock(n), cm, n, waves=absorb)
        runs[("rules expand into care", dial, "two waves, robotics in 2 years, care absorbs, three points a year")] = \
            simulate(rg, fast, ai_shock(n), cm, n, waves=absorb)
        # the financing limit in place of the ceiling: what pays for the build-out
        for rl in (CARE, CARE_TAX, CARE_LEVY):
            rn = "care financed by borrowing" if rl is CARE else rl.name
            for pace, tag in ((1.0, ""), (3.0, ", three points a year")):
                runs[(rn, dial, "two waves, robotics in 2 years, care absorbs, financing limit" + tag)] = \
                    simulate(rg, {r: replace(rl, care_pace=pace) for r in R}, ai_shock(n), replace(cm, care_ceiling=100.0), n, waves=absorb)
    return runs


def main():
    tg = validation_targets()
    cm, okun, val = fit(tg)
    regions = regions_today()
    notes = regions.pop("_notes")
    regions = {r: replace(g, okun=okun) if r == "US" else g for r, g in regions.items()}
    runs = scenarios(cm, regions)
    out = {"validation": {k: v for k, v in val.items() if k != "runs"}, "common": cm.__dict__,
           "regions": {r: {k: v for k, v in g.__dict__.items()} for r, g in regions.items()}, "notes": notes, "scenarios": {}}
    for (rn, an, wl), o in runs.items():
        out["scenarios"][f"{rn} | {an}" + (f" | {wl}" if wl else "")] = {"year4": summary(o, regions, 16), "year6": summary(o, regions)}
    json.dump(out, open(os.path.join(ROOT, "results", "global_crash.json"), "w", encoding="utf-8"), indent=1, default=str)
    print(json.dumps(out["validation"], indent=1))
    for k, v in out["scenarios"].items():
        print(k)
        for h in ("year4", "year6"):
            x6 = v[h]
            for r in R:
                x = x6[r]
                print(f"   {h} {r}: gap min {x['gap_min']} (q{x['gap_min_quarter']})  u max {x['unemployment_max']} (q{x['unemployment_max_quarter']}; yr2 {x['unemployment_year2']}; "
                      f"u* end {x['structural_unemployment_end']} = cog {x['displaced_cognitive_end']} + phys {x['displaced_physical_end']})  "
                      f"infl {x['inflation_min']}..{x['inflation_max']}  capital lost {x['bank_capital_lost_max']}  guarantee {x['guarantee_cost_max_pct_gdp']}  "
                      f"care absorbed {x['absorbed_into_existing_care_jobs_end']}+{x['absorbed_into_new_care_jobs_end']} (physical {x['absorbed_physical_share_end']}), "
                      f"care {x['care_share_end']}%, cost {x['care_cost_max_pct_gdp']}  {'NO BOTTOM' if x['no_bottom'] else ''}")
            print(f"   {h} four-weighted gap min", x6["four_weighted_gap_min"])
    figures(val, runs, regions)


def figures(val, runs, regions):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams["axes.titlesize"] = 10
    a29, b07 = val["runs"]
    fig, ax = plt.subplots(1, 2, figsize=(13, 4.6), layout="constrained")
    fig.get_layout_engine().set(rect=(0, 0.04, 1, 0.96))
    tg = val["targets"]["1929-33"]
    yrs = tg["years"]
    kk = np.arange(len(a29["y"])) * DT
    for key, lab, c, data in (("out", "output (1929 = 100)", "C0", [100 * v for v in tg["output_over_1929"]]),
                              ("P", "price level (1929 = 100)", "C1", [100 * v for v in tg["prices_over_1929"]]),
                              ("u", "unemployment, %", "C2", tg["unemployment"])):
        ser = (1 + a29["y"] / 100) * 1.02 ** kk * 100 if key == "out" else (a29["P"] * 100 if key == "P" else a29["u"])
        ax[0].plot(yrs, annual(ser), color=c, lw=1.8, label=f"{lab}, model")
        ax[0].scatter(yrs, data, color=c, zorder=5, s=22)
    ax[0].set_title("US 1929-33 with the 1930s' rules: model (lines) and data (dots), annual"); ax[0].legend(fontsize=8)
    t2 = val["targets"]["2007-09"]
    x = np.arange(1, 13)
    for key, lab, c, data in (("y", "output gap change", "C0", t2["gap_change"]), ("u", "unemployment, %", "C1", t2["unemployment"]),
                              ("pi", "core inflation, %", "C2", t2["core_inflation"])):
        ax[1].plot(2008 + (x - 1) / 4, b07[key][1:13], color=c, lw=1.8, label=f"{lab}, model")
        ax[1].scatter(2008 + (x - 1) / 4, data, color=c, s=16, zorder=5)
    ax[1].set_title("US 2008-10 with today's rules: model (lines) and data (dots), quarterly"); ax[1].legend(fontsize=8)
    fig.text(0.01, 0.005, "FRED (GDPCA, CPIAUCNS, GDPC1, GDPPOT, UNRATE, PCEPILFE); 1930-33 unemployment: Lebergott. One parameter set for both episodes.", fontsize=7.5)
    fig.savefig(os.path.join(ROOT, "figures", "fig_global_crash_validation.png"), dpi=130)
    fig, ax = plt.subplots(2, len(R), figsize=(5 * len(R), 8.6), layout="constrained")
    fig.get_layout_engine().set(rect=(0, 0.03, 1, 0.97))
    cases = [("modern rules", "bust only", "-"), ("modern rules", "bust + displacement", "--"),
             ("rules expand under pressure", "bust + displacement", ":"), ("rules erode under pressure", "bust + displacement", "-.")]
    for j, r in enumerate(R):
        for (rn, an, st) in cases:
            o = runs[(rn, an, "")][r]
            t = np.arange(len(o["y"])) * DT
            ax[0, j].plot(t, o["y"], ls=st, label=f"{rn}, {an}")
            ax[1, j].plot(t, o["u"], ls=st, label=f"{rn}, {an}")
        ax[0, j].set_title(f"{r}: output against capacity, %"); ax[1, j].set_title(f"{r}: unemployment, %")
        ax[0, j].axhline(0, color="grey", lw=0.8)
    ax[0, 0].legend(fontsize=7)
    for a in ax.flat:
        a.set_xlabel("years from the bust")
    fig.text(0.01, 0.005, "global_crash.py: a dot-com-shaped bust of the AI build-out in five regions (the euro area as France and the rest) linked by trade and a shared risk mood; amplifiers fitted on 1929-33 and 2007-09.", fontsize=7.5)
    fig.savefig(os.path.join(ROOT, "figures", "fig_global_crash.png"), dpi=120)
    # the two waves: today's rules, displacement and recessions triggering adoption (the labour-depression row)
    fig, ax = plt.subplots(2, len(R), figsize=(5 * len(R), 8.6), layout="constrained")
    fig.get_layout_engine().set(rect=(0, 0.03, 1, 0.97))
    rn, an = "modern rules", "bust + displacement, recessions trigger adoption x3"
    cases = [("", "every job exposed from the start", "k", "-")] + [(f"two waves, robotics in {L} years", f"two waves, robotics in {L} years", c, s)
                                                                  for L, c, s in ((1, "C0", "--"), (2, "C1", "-"), (3, "C2", ":"))]
    for j, r in enumerate(R):
        for wl, lab, c, st in cases:
            o = runs[(rn, an, wl)][r]
            t = np.arange(len(o["y"])) * DT
            ax[0, j].plot(t, o["u"], color=c, ls=st, label=lab)
            ax[1, j].plot(t, o["y"], color=c, ls=st, label=lab)
        ax[0, j].set_title(f"{r}: unemployment, %"); ax[1, j].set_title(f"{r}: output against capacity, %")
        ax[1, j].axhline(0, color="grey", lw=0.8)
    ax[0, 0].legend(fontsize=7.5)
    for a in ax.flat:
        a.set_xlabel("years from the bust")
    fig.text(0.01, 0.005, "global_crash.py, today's rules, the bust with displacement and recessions triggering adoption (x3). Two waves: cognitive work "
             "(ISCO 1-4) exposed now, physical work (6-9) once robotics arrives; in-person services (5) in neither. Occupations and pay: ILOSTAT (exposure.py).", fontsize=7.5)
    fig.savefig(os.path.join(ROOT, "figures", "fig_global_crash_waves.png"), dpi=120)
    # care as the absorber: the same row, robotics two years out
    fig, ax = plt.subplots(2, len(R), figsize=(5 * len(R), 8.6), layout="constrained")
    fig.get_layout_engine().set(rect=(0, 0.03, 1, 0.97))
    an = "bust + displacement, recessions trigger adoption x3"
    w2 = "two waves, robotics in 2 years"
    cases = [("modern rules", w2, "no absorber", "k", "-"),
             ("modern rules", w2 + ", care absorbs", "care at its trend pace (jobs that exist anyway)", "C0", "--"),
             ("rules expand into care", w2 + ", care absorbs", "a funded care build-out, a point a year, to the ceiling", "C3", "-"),
             ("rules expand into care", w2 + ", care absorbs, three points a year, no ceiling", "three points a year, no ceiling", "C3", ":"),
             ("rules expand under pressure", w2 + ", care absorbs", "an income guarantee (care at its trend pace)", "C2", "-.")]
    for j, r in enumerate(R):
        for rn, wl, lab, c, st in cases:
            o = runs[(rn, an, wl)][r]
            t = np.arange(len(o["y"])) * DT
            ax[0, j].plot(t, o["u"], color=c, ls=st, label=lab)
            ax[1, j].plot(t, o["care"], color=c, ls=st, label=lab)
        ax[1, j].axhline(Common().care_ceiling, color="grey", lw=0.8, ls="--")
        ax[0, j].set_title(f"{r}: unemployment, %"); ax[1, j].set_title(f"{r}: health and social work, % of employment (ceiling dashed)")
    ax[0, 0].legend(fontsize=7.5)
    for a in ax.flat:
        a.set_xlabel("years from the bust")
    fig.text(0.01, 0.005, "global_crash.py, the bust with displacement and recessions triggering adoption (x3), robotics two years out. Care takes in the displaced "
             "within its pace, the gate (men enter care at a quarter of women's rate) and the ceiling (Norway's 20.1% of employment). ILOSTAT (exposure.py).", fontsize=7.5)
    fig.savefig(os.path.join(ROOT, "figures", "fig_global_crash_care.png"), dpi=120)
    # the financing limit: the same row, a build-out of up to three points a year, no ceiling, three sources
    fig, ax = plt.subplots(3, len(R), figsize=(5 * len(R), 11.5), layout="constrained")
    fig.get_layout_engine().set(rect=(0, 0.025, 1, 0.975))
    wl = "two waves, robotics in 2 years, care absorbs, financing limit, three points a year"
    cases = [("modern rules", "two waves, robotics in 2 years, care absorbs", "no build-out (care at its trend)", "k", "-"),
             ("care financed by borrowing", wl, "financed by borrowing", "C0", "-"),
             ("care financed by labour taxes", wl, "financed by taxes on labour income", "C3", "--"),
             ("care financed by a levy on AI income", wl, "financed by a levy on AI income", "C2", ":")]
    for j, r in enumerate(R):
        for rn, wl_, lab, c, st in cases:
            o = runs[(rn, an, wl_)][r]
            t = np.arange(len(o["y"])) * DT
            ax[0, j].plot(t, o["u"], color=c, ls=st, label=lab)
            ax[1, j].plot(t, o["care"], color=c, ls=st, label=lab)
            if rn != "modern rules" and rn != "care financed by borrowing":
                ax[2, j].plot(t[1:], o["room"][1:], color=c, ls=st, label=f"room: {lab.split('by ')[-1]}")
            ax[2, j].plot(t[1:], o["care_cost"][1:], color=c, ls=st, lw=0.8, alpha=0.6) if rn != "modern rules" else None
        ax[1, j].axhline(Common().care_ceiling, color="grey", lw=0.8, ls="--")
        ax[2, j].axhline(0, color="grey", lw=0.8)
        ax[0, j].set_title(f"{r}: unemployment, %"); ax[1, j].set_title(f"{r}: care, % of employment (Norway dashed)")
        ax[2, j].set_title(f"{r}: room (thick) and cost (thin), % of GDP")
    ax[0, 0].legend(fontsize=7.5); ax[2, 0].legend(fontsize=7.5)
    for a in ax.flat:
        a.set_xlabel("years from the bust")
    fig.text(0.01, 0.005, "global_crash.py, the bust with displacement and recessions triggering adoption (x3), robotics two years out; a care build-out of up "
             "to three points a year with no ceiling, limited by what pays for it. Taxes on labour up to Austria's take on a shrinking wage base; a levy on half "
             "the pay the displaced lost; borrowing at the measured price of debt (financing.py).", fontsize=7.5)
    fig.savefig(os.path.join(ROOT, "figures", "fig_global_crash_financing.png"), dpi=120)


if __name__ == "__main__":
    main()
