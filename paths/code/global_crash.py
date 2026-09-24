# global_crash.py — could an AI shock become a Great Depression, and a systemic one? Four regions — the US, the euro
# area, Sweden, China — each with the demand and household machinery of demand.py / households.py in reduced form, and
# the four amplifiers the single-country layers leave out:
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
# Each quarter, region r:
#   policy       i = max(floor, s i_1 + (1-s) [r* + pie + phi_pi (pi_1 - pi*) + phi_y y_1])   (modern)
#   expectations pie = anchor pi* + (1 - anchor) pi_1
#   demand level D = wealth + capex + unemployed + rate relief + debt deflation + credit + money + trade + fiscal
#   output gap   y = a1 y_1 - a_r (i - pie - r*) + D - a1 D_1
#   inflation    pi = pie + kappa y + tariff pass-through
#   unemployment u moves toward u* - okun y at a regional speed; u* ratchets up by eta x (u - u*) and the drift
#   banks        capital falls by losses above normal (a base rate plus unemployment, the gap, and shock add-ons)
#   spreads      s = s0 + sigma x (capital lost) + global mood, capped under a backstop
#
# VALIDATION FIRST: the same equations, with only the institutions and the shocks changed, must reproduce the US
# 1929-33 (the 1930s settings: gold-standard policy, no deposit insurance, no unemployment support, austerity,
# Smoot-Hawley) and 2007-10 (modern settings), as PATHS: 1930-33 year by year (output, prices, unemployment) and
# 2008-10 quarter by quarter (output gap, unemployment, core inflation). Measured shocks: the stock market, US exports
# (the rest of the world's slump), and in 2007-09 the housebuilding collapse and housing wealth. Seven parameters are
# fitted jointly by a global search: spread per unit of capital lost, the money channel of bank runs, the
# debt-deflation coefficient, the 1930s Phillips slope, the US Okun coefficient, the size of 1930's post-crash spending
# collapse (Romer's; the propagation to 1933 is what is tested), and the rate transmission a_r (bounded to the
# literature's 0.03-0.15). Everything else is fixed from data or the literature, stated. Known bias: the model recovers
# from 2009 faster than the US did, so it is optimistic about how long a crisis lasts.
# Data (FRED): real GDP annual from 1929 (GDPCA), CPI from 1913 (CPIAUCNS), unemployment from 1948 (UNRATE), real GDP
# and CBO potential quarterly (GDPC1, GDPPOT), core PCE (PCEPILFE), policy rates (DFF, ECBDFR), euro-area HICP and
# unemployment, China CPI, BIS credit to households and to the private non-financial sector (Q..HAM770A, Q..PAM770A).
# 1933 unemployment 24.9% (Lebergott, the standard series; not on FRED). Region parameters not measured here are
# marked approximate in REGIONS.
#
# Run from paths/:  ../venv/Scripts/python.exe code/global_crash.py
# Out: results/global_crash.json, figures/fig_global_crash.png, figures/fig_global_crash_validation.png,
#      figures/fig_global_crash_waves.png, figures/fig_global_crash_care.png

from __future__ import annotations

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
R = ("US", "EA", "SE", "CN")


def fred(sid: str) -> pd.Series:
    s = _lc.pull_fred(sid)
    if s is None:
        raise SystemExit(f"FRED {sid}: not available")
    return s


# ------------------------------------------------------------------ the pieces
@dataclass(frozen=True)
class Region:
    name: str
    size: float                 # share of the four's GDP (market exchange rates, approximate)
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


MODERN = Rules()
THIRTIES = Rules(name="1930s", policy="gold", anchor=0.2, pi_star=0.0, insured=False, backstop=False, support=False,
                 fiscal="austerity", tariff=15.0, tariff_q=3, kappa_1930s=True, care="cut")
ERODED = Rules(name="rules erode under pressure", anchor=0.6, backstop=False, fiscal="austerity", tariff=20.0, tariff_q=3, care="cut")
EXPANDED = Rules(name="rules expand under pressure", fiscal="guarantee", trigger=1.5)   # an income guarantee: the deficits branch
CARE = Rules(name="rules expand into care", care="expand", trigger=1.5)                # today's rules plus a funded care build-out


@dataclass
class Shock:
    """Exogenous paths, per region: equity decline (share), AI capex decline (share), extra credit losses (% of loans
    a year), each as a function of the quarter."""
    equity: dict = field(default_factory=dict)
    capex: dict = field(default_factory=dict)
    losses: dict = field(default_factory=dict)
    demand: dict = field(default_factory=dict)       # other exogenous demand level, % of GDP


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
    f = max(o["u"][j] - g.u0, 0.0) / st if st > 1e-12 else 0.0
    return {q: struct[q] * f for q in GROUPS}


def simulate(regions: dict, rules: dict, shock: Shock, cm: Common = Common(), n: int = 24, active=None,
             waves: Waves = UNIFORM) -> dict:
    """regions: {code: Region}; rules: {code: Rules}; active: regions simulated (others held at zero gap)."""
    active = active or list(regions)
    names = list(regions)
    out = {r: {k: np.zeros(n) for k in ("y", "u", "u_star", "pi", "P", "Pexp", "i", "k", "s", "D", "stress", "stim",
                                        "d_wealth", "d_capex", "d_unemp", "d_relief", "d_debt", "d_credit", "d_money",
                                        "d_trade", "d_fiscal", "loss", "deficit_extra", "s_cog", "s_phys", "pay_weighted",
                                        "at_cog", "at_phys", "ax_cog", "ax_phys", "d_care", "care_cost", "care")} for r in names}
    W = {r: wave_weights(regions[r], rules[r], cm, waves) for r in names}
    for r in names:
        g, rl = regions[r], rules[r]
        o = out[r]
        o["u"][0] = o["u_star"][0] = g.u0
        o["pi"][0] = g.pi0
        o["P"][0] = o["Pexp"][0] = 1.0
        o["i"][0] = g.i0
        o["k"][0] = g.bank_capital
        o["s"][0] = 0.0
        o["care"][0] = g.care_share
    fiscal_left = {r: 0 for r in names}
    fiscal_on = {r: False for r in names}
    for k in range(1, n):
        mood = cm.global_mood * sum(regions[r].size * out[r]["stress"][k - 1] for r in names)
        for r in names:
            g, rl, o = regions[r], rules[r], out[r]
            if r not in active:
                o["u"][k], o["u_star"][k], o["pi"][k], o["i"][k], o["k"][k] = g.u0, g.u0, g.pi0, g.i0, g.bank_capital
                o["care"][k] = g.care_share
                o["P"][k] = o["P"][k - 1] * (1 + g.pi0 / 100 * DT)
                o["Pexp"][k] = o["P"][k]
                continue
            pis = rl.pi_star
            pie = rl.anchor * pis + (1 - rl.anchor) * o["pi"][k - 1]
            # policy
            if rl.policy == "taylor":
                target = cm.r_star + pie + cm.phi_pi * (o["pi"][k - 1] - pis) + cm.phi_y * o["y"][k - 1]
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
                d_unemp = -(cm.mpc_u - cm.mpc_rep) * cm.labour_share * max(o["u"][k - 1] - g.u0, 0.0) * (1 - rep)
                owed = max(o["u"][k - 1] - g.u0, 0.0) * max(rl.guarantee - rep, 0.0)
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
            d_relief = (cm.mpc_b - cm.mpc_rep) * g.floating * g.hh_debt / 100 * (g.i0 - i)
            d_debt = -cm.debt_deflation * g.priv_debt / 100 * max(o["Pexp"][k - 1] / o["P"][k - 1] - 1, 0.0) * 100
            d_credit = -cm.a_s * o["s"][k - 1]
            d_money = 0.0 if rl.insured else -cm.money * o["stress"][k - 1]
            partners = {"US": out["US"]["y"][k - 1], "EA": out["EA"]["y"][k - 1], "SE": out["SE"]["y"][k - 1], "CN": out["CN"]["y"][k - 1]}
            partners["RoW"] = sum(regions[q].size * partners[q] for q in names)
            tariff = rl.tariff if k >= rl.tariff_q else 0.0
            # a tariff point cuts exports about a point (short-run trade elasticity ~1); imports fall too, so only part
            # of it (tariff_net, uncertainty and broken supply chains) is lost to demand rather than switched home
            d_trade = g.exports * (cm.trade_elasticity * sum(g.trade[q] * partners[q] for q in g.trade) - cm.tariff_net * tariff)
            unemp_up = o["u"][k - 1] - g.u0
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
            D = d_wealth + d_capex + d_unemp + d_relief + d_debt + d_credit + d_money + d_trade + d_fiscal + d_other + d_care
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
            add_drift = g.drift * m_drift * DT
            o["u_star"][k] = min(o["u_star"][k - 1] + add_eta + add_drift, 45.0)
            o["s_cog"][k], o["s_phys"][k] = o["s_cog"][k - 1], o["s_phys"][k - 1]
            if W[r] is not None and add_eta + add_drift > 0:
                inc = o["u_star"][k] - o["u_star"][k - 1]            # after the cap
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
            grow = 0.0 if rl.care == "cut" else min(g.care_trend * DT, max(cm.care_ceiling - o["care"][k - 1], 0.0))
            o["care"][k] = o["care"][k - 1] + grow
            if W[r] is not None and waves.absorb and rl.care != "cut":
                weight = {q: o[s][k] * g.gate[q] for q, s, _, _ in ABSORBED}
                pool = sum(weight.values())
                potential = cm.care_hire * pool
                a_t = min(grow, potential)
                a_x = 0.0
                if rl.care == "expand" and unemp_up >= rl.trigger:
                    a_x = max(min(rl.care_pace * DT, potential - a_t, cm.care_ceiling - o["care"][k]), 0.0)
                o["care"][k] += a_x
                if pool > 0:
                    for q, s, at, ax in ABSORBED:
                        f = weight[q] / pool
                        o[s][k] -= (a_t + a_x) * f
                        o[at][k] += a_t * f
                        o[ax][k] += a_x * f
                    o["u_star"][k] -= a_t + a_x
            # Okun's law for the rest of output: the build-out's own jobs are counted directly
            target = max(o["u_star"][k] - g.okun * (y - d_care), 1.5)
            o["u"][k] = min(o["u"][k - 1] + g.speed * (target - o["u"][k - 1]), 50.0)
            if W[r] is None:
                debt_up = max(o["u"][k] - g.u0, 0.0)
            else:
                du = displaced(o, k, g, W[r])
                debt_up = sum(du[q] * W[r]["pay"][q] for q in GROUPS)     # debts taken proportional to pay
                debt_up += sum((o[at][k] + o[ax][k]) * W[r]["pay_care"][q] for q, _, at, ax in ABSORBED)
            o["pay_weighted"][k] = debt_up
            # banks
            loss = cm.loss_base + cm.loss_u * debt_up + cm.loss_y * max(-y, 0.0) + shock.losses.get(r, np.zeros(n))[k]
            o["loss"][k] = loss
            kk = o["k"][k - 1] - (loss - cm.loss_base) * g.loans / 100 * DT
            if rl.backstop:
                kk = max(kk, rl.capital_floor * g.bank_capital)
            o["k"][k] = max(kk, 0.0)
            o["stress"][k] = max(0.0, 1.0 - o["k"][k] / g.bank_capital)
            s = cm.sigma * o["stress"][k] + mood
            if rl.backstop:
                s = min(s, g.spread_cap)
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
                  "care_cost_max_pct_gdp": round(float(o["care_cost"][:n].max()), 2)}
    w = {r: regions[r].size for r in out}
    tot = sum(w.values())
    nn = len(out["US"]["y"]) if horizon_q is None else horizon_q
    res["four_weighted_gap_min"] = round(float(min(sum(w[r] * out[r]["y"][k] for r in out) / tot for k in range(nn))), 2)
    return res


# ------------------------------------------------------------------ the regions today (2026) and the US of 1929 / 2007
def yoy(s: pd.Series, periods: int) -> float:
    return float((s.iloc[-1] / s.iloc[-1 - periods] - 1) * 100)


def regions_today() -> dict:
    core = fred("PCEPILFE")
    hicp = fred("CP0000EZ19M086NEST")
    cn_cpi = fred("CHNCPIALLMINMEI")
    last = lambda sid: float(fred(sid).iloc[-1])  # noqa: E731
    se = json.load(open(os.path.join(ROOT, "results", "households.json"), encoding="utf-8"))["sweden_start"]
    sw_cyc = json.load(open(os.path.join(ROOT, "results", "demand.json"), encoding="utf-8"))["sweden_cycle"]
    us = Region("US", 0.44, last("UNRATE"), last("DFF"), yoy(core, 12), 0.0, 0.6, 0.9, 0.35, last("QUSHAM770A"), last("QUSPAM770A"),
                0.10, 1.9, 1.5, 8.0, 45.0, 0.11, {"EA": 0.18, "CN": 0.07, "SE": 0.005, "RoW": 0.745}, 2.5, 3.0, 0.05, 1.0)
    ea = Region("EA", 0.25, 6.3, last("ECBDFR"), yoy(hicp, 12), -0.5, 0.4, 0.35, 0.60, last("QXMHAM770A"), last("QXMPAM770A"),
                0.35, 0.6, 0.3, 10.0, 90.0, 0.20, {"US": 0.20, "CN": 0.08, "SE": 0.04, "RoW": 0.68}, 1.5, 3.0, 0.03, 0.5)
    sw = Region("SE", 0.01, 8.5, 1.75, 0.7, -0.5, 0.4, 0.4, 0.65, last("QSEHAM770A"), last("QSEPAM770A"),
                se["floating_share"], 1.4, 0.4, 15.0, 130.0, 0.50, {"US": 0.09, "EA": 0.40, "CN": 0.04, "RoW": 0.47}, 2.0, 3.0, 0.03, 0.6)
    cn = Region("CN", 0.30, 5.2, 1.4, yoy(cn_cpi, 12), 0.0, 0.25, 0.3, 0.15, last("QCNHAM770A"), last("QCNPAM770A"),
                0.8, 0.3, 1.0, 20.0, 180.0, 0.19, {"US": 0.15, "EA": 0.15, "SE": 0.005, "RoW": 0.695}, 3.0, 1.5, 0.04, 0.8)
    # the two-wave split: occupations and pay measured (exposure.py); where support stops rising, approximate — the US
    # (half of pay up to state maxima, near 0.9 of average pay), the euro area (Germany's ceiling near 1.8, France's
    # far higher, Italy's and Spain's below average: about 1.5 weighted), Sweden (the unemployment fund's cap sits near
    # 0.85 of average pay, but most white-collar workers carry union income insurance above it for the first months:
    # 1.5), China (support too thin for a cap to matter)
    exj = json.load(open(os.path.join(ROOT, "results", "exposure.json"), encoding="utf-8"))
    ex, cr = exj["regions"], exj["care"]["regions"]
    caps = {"US": 0.9, "EA": 1.5, "SE": 1.5, "CN": 1.0}
    regs = {r: replace(g, groups=ex[r]["share"], premium=ex[r]["premium"], benefit_cap=caps[r], care_share=cr[r]["care_share_pct"],
                       care_trend=cr[r]["care_trend_pts_a_year"], gate=cr[r]["gate"])
            for r, g in (("US", us), ("EA", ea), ("SE", sw), ("CN", cn))}
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


def run_2007(cm: Common, okun: float) -> dict:
    n = 13                                                   # 2007Q4 .. 2010Q4
    regs = {"US": us_2007(okun), "EA": passive("EA"), "SE": passive("SE"), "CN": passive("CN")}
    rules = {r: replace(MODERN, fiscal_quarters=8) for r in regs}
    # equity -50% by 2009Q1, back to -20% by 2010Q2; housing wealth -30% (x1.5 GDP, 0.05 a krona a year) staying down;
    # mortgage-related credit losses ~ 3.5% of loans over two years
    eq = np.interp(np.arange(n), [0, 5, 10, 12], [0.0, 0.5, 0.2, 0.2])
    house = -0.05 * 1.5 * ramp(0.30, 1, 6, n) * 100
    # the housebuilding collapse, measured: residential investment's share of GDP from 2007Q4 on (FRED PRFI / GDP)
    res = fred("PRFI") / fred("GDP").reindex(fred("PRFI").index) * 100
    res = res.loc["2007-10-01":].values[:n]
    build = -(res - res[0])
    # the rest of the world's slump, measured: US real exports against 2007Q4, % of 2007Q4 GDP (FRED EXPGSC1 / GDPC1)
    ex = ((fred("EXPGSC1") - fred("EXPGSC1").loc["2007-10-01"]) / fred("GDPC1").loc["2007-10-01"] * 100).loc["2007-10-01":].values[:n]
    sh = Shock(equity={"US": eq}, losses={"US": pulse(3.5, 2, 8, n)}, demand={"US": house + build + ex})
    return simulate(regs, rules, sh, cm, n, active=["US"])["US"]


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
def ai_shock(n: int, scale: float = 1.0) -> Shock:
    """A dot-com-shaped bust of the AI build-out: equity down over four quarters (the periphery collapses, the core
    reprices), AI investment down 60%, losses on AI-related lending (private credit and its bank lenders)."""
    eq = {"US": 0.40, "EA": 0.25, "SE": 0.30, "CN": 0.25}
    ls = {"US": 1.5, "EA": 0.5, "SE": 0.5, "CN": 1.0}
    return Shock(equity={r: ramp(scale * v, 1, 4, n) for r, v in eq.items()},
                 capex={r: ramp(scale * 0.6 * 100, 1, 4, n) / 100 for r in eq},
                 losses={r: pulse(scale * v, 2, 8, n) for r, v in ls.items()})


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
    fig, ax = plt.subplots(2, 4, figsize=(20, 8.6), layout="constrained")
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
    fig.text(0.01, 0.005, "global_crash.py: a dot-com-shaped bust of the AI build-out in four regions linked by trade and a shared risk mood; amplifiers fitted on 1929-33 and 2007-09.", fontsize=7.5)
    fig.savefig(os.path.join(ROOT, "figures", "fig_global_crash.png"), dpi=120)
    # the two waves: today's rules, displacement and recessions triggering adoption (the labour-depression row)
    fig, ax = plt.subplots(2, 4, figsize=(20, 8.6), layout="constrained")
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
    fig, ax = plt.subplots(2, 4, figsize=(20, 8.6), layout="constrained")
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


if __name__ == "__main__":
    main()
