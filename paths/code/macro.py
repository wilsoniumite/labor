# macro.py — the macro block: the paper's Appendix B economy along a technology path, and the bridges
# from it to the curve layer.
#
# THE ECONOMY is the pinning model, ../pinning/code/pinning_model.py: the paper's Appendix B with Appendix A.4's
# capital (machines a stock priced at user cost, interest a third income), the machine chain's ceiling, the solve and
# the closed-form calibration from shares. The paper's instance solves with the same file; every name it defines
# (Economy, solve, NoEquilibrium, x_ceiling, ChainTargets, calibrate_c, rate_headroom, ...) is re-exported here, so
# macro.solve and the rest are what they were. At (rho, delta) = (0, 1) it is the flow benchmark; calibration (a) uses
# that, calibration (b) a 5.75% required return and 8% depreciation. With Bridges.capital_premium set, the required
# return follows the economy's own real rate, so rates feed back into automation. Gate: the SSRN version's instance
# (N 4, T 10, h 1, a .3, b .4, lambda .05, gamma .2 + .8x, chi ~ U[0,1]) solves to x* 0.86315, v 0.54344, Y 7.88061,
# n 1.34338 (checks/check_macro.py).
#
# (c) THE MACHINE CHAIN ON THE NATIONAL ACCOUNTS' BASIS (calibrate_c; code/calibration_c.py). Calibrations (a)
# and (b) put almost no labour in machine services (its full-chain share of machine cost 0.026 and ~0.002); BEA's
# input-output accounts put ~0.57 of a machine's build cost in full-chain compensation with imports priced at US cost
# shares, 0.47 counting US labour only (code/chains.py; ChainTargets says which basis each target is on). At that
# labour content Appendix B's standing assumption 1 - (rho + delta)(a + lambda gamma(1)) > 0 fails, and the model's
# ceiling binds: tasks past x_ceiling are closed to machines (pinning_model.py's header). Beyond a rate headroom
# (rate_headroom) there is no land-scarce equilibrium: the economy would enter a land-slack regime (r = 0, output
# labour-constrained) that the model does not have, and solve raises NoEquilibrium.
#
# THE CENTRAL CALIBRATION (her decision, 2026-09-30: the downstream modules run on (c), not (b)). central(root) is the
# one entry point: (c)'s central economy — the open (domp) reading, the low root in k (root "hi" is the sensitivity) —
# and its info (rho, the capital premium that starts a feedback path at that rho, multiplier, headroom). It returns the
# parameters stored in results/calibration_c.json after re-solving the stored central targets with calibrate_c (closed
# form) and checking that the re-solve agrees with them to a relative 1e-9 in every parameter (CENTRAL_RTOL); beyond
# that it refuses to run. The tolerance is for another platform's numpy/scipy builds (the website's builder), where a
# re-solve may differ in the last bits: the stored parameters are used either way, so they do not move. On the
# development machine the re-solve equals the stored parameters bit for bit, and checks/check_calibration_c.py (E1)
# gates that, and gates both equal to code/calibration_c.py's own.
# Provenance: the targets are BEA's (chains.py's bundle and cost split, WP2026-01's labour, Fixed Assets' delta), built
# and gated in code/calibration_c.py; reading its gated output keeps the BEA workbooks and the lambda cache out of every
# module that imports macro. Helpers so no module hard-codes (b)'s numbers: deep_tech(e) (recursive automation to a fifth
# of the economy's own lambda, not to (b)'s 0.01), hold_tech(e), capital_premium(e) (rho x 100 - r0_star, not (b)'s 5.0),
# feedback_bridges(e). calibrate(), CALIBRATION_BASE and CAPITAL_BASE stay for the (a)/(b) comparators; every helper
# reproduces (b)'s hard-coded values exactly on (b) (0.05 / 5 == 0.01 and 5.75 - 0.75 == 5.0 in floating point).
#
# DYNAMICS. The technology clock moves capability (gamma scaled by eta: task automation) and the
# labour embodied in machine services (lambda: recursive automation) along a path; each date is solved
# as an equilibrium (quasi-static: no build lags, no adjustment costs — a stated simplification).
#
# BRIDGES (behaviour, swappable; reduced forms with named coefficients). Refit on (c) against published evidence
# (2026-10-27, Log 46; decisions 72-75), revised 2026-10-28 (Log 54; her four calls, decisions 93-96, and four fixes, in 73, 75,
# 77 and 79): the neutral rate's channels on the evidence's coefficients per point of the model's income (the literature's are
# per point of GDP: GDP_OVER_INCOME), the fiscal start at Sweden's measured primary balance net of the state's asset income.
# The comparators (a) and (b) keep the bridges as tuned on (b) (BRIDGES_B), so they stay the pre-switch runs.
#   nominal — the central bank holds the basket's price on its target pi*, so goods, rents and wages
#             inflate at pi* plus the change in their real price against the basket: the fork appears
#             as goods deflation and shelter inflation around an on-target CPI;
#   fiscal  — a labour tax, a rent tax, spending, and a public share of dependants' support; the labour tax set so the start
#             runs the measured primary deficit, net of property income received since the model's government owns no
#             assets (deficit0, decision 95; solved on the economy the path starts at; BRIDGES_B: tau_w 0.40, on (c) a surplus
#             start); the debt pays r* + pi*, floored at the policy floor ELB (decision 75 corrected; BRIDGES_B unfloored);
#   neutral — r* moves with investment demand (replacement investment / income at Rachel and Smith's coefficient times its
#             pass-through, decision 93; BRIDGES_B: the pace of tasks moving to machines), down as income shifts to owners
#             who save more of it, up with primary deficits private saving does not offset (NEUTRAL_SCALE times each one's
#             pass-through); on feedback paths the bridges read at the start's required return (decision 96; BRIDGES_B along
#             the path);
#   policy  — the desired nominal rate r* + pi* (+ reaction to measured inflation under mandates that
#             exclude shelter); the curve layer's stepwise rule delivers it;
#   premia  — term premium and sovereign loss rate rise with debt above thresholds.

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass, field, replace

import numpy as np
from scipy.optimize import brentq

# ------------------------------------------------------------------ the structural core: the pinning model (header)
_PINNING_CODE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "pinning", "code")
if _PINNING_CODE not in sys.path:
    sys.path.append(_PINNING_CODE)
from pinning_model import (ChainTargets, Economy, NoEquilibrium, _chain_ratio, _parts, calibrate_c,  # noqa: E402,F401
                           rate_headroom, solve, target_residuals, x_ceiling)


# ------------------------------------------------------------------ the technology clock
@dataclass(frozen=True)
class TechPath:
    """eta and lambda move from their start values toward targets along a logistic in time: centred at
    t_mid (years), with `width` years from 12% to 88% of the move. eta scales capability (task
    automation); lambda is the labour in a machine-service hour (recursive automation)."""
    eta_end: float = 1.0
    lam_end: float = 0.05
    t_mid: float = 5.0
    width: float = 4.0

    def at(self, t, base: Economy):
        s = 1.0 / (1.0 + np.exp(-(t - self.t_mid) / (self.width / 4.0)))
        s0 = 1.0 / (1.0 + np.exp(self.t_mid / (self.width / 4.0)))
        w = (s - s0) / (1.0 - s0)                                   # 0 at t = 0, -> 1
        return replace(base, eta=base.eta + (self.eta_end - base.eta) * w,
                       lam=base.lam + (self.lam_end - base.lam) * w)


# ------------------------------------------------------------------ the bridges (behaviour; swappable)
# THE REFIT ON (c) (Log 46; decisions 72-75), revised 2026-10-28 (Log 54; decisions 93-96). The three neutral-rate channels
# share one scale: r* moves NEUTRAL_SCALE pp per pp of income by which desired saving falls short of desired investment, so the
# owners' and deficits channels' coefficients are that scale times how much of their shift reaches net saving — income moved
# from wages to owners by the gap between their saving rates (alpha_rent), a primary deficit by the part private saving does
# not offset (alpha_fiscal); investment demand (alpha_inv) at Rachel and Smith's own coefficient times its pass-through
# (decision 93). The evidence for each number is in code/macro_scenarios.py's EVIDENCE and results/macro_scenarios.json.
# UNITS (decision 73 corrected, Log 54). The literature's coefficients are per point of GDP; the model's shifts are per point of
# its income (net of replacement investment, the chain's imported content counted as rent). One conversion constant,
# GDP_OVER_INCOME: (c)'s start GDP net of the chain's imported content over income (results/calibration_c.json's central,
# labor_share / comp_gdp_net = 1.14517; the ratio macro_scenarios.fiscal_start_evidence uses, gated equal to it). Every evidence
# number is stored in GDP units under a _GDP name and converted once, here. Until the revision the GDP numbers were applied per
# point of income unconverted. Not converted: tp_per_debt, debt_threshold and loss_per_debt (Bridges), illustrative defaults
# stated per point of income since the macro block's first commit and never sourced in GDP units.
GDP_OVER_INCOME = 1.1452       # GDP net of the chain's imported content over the model's income, at (c)'s start
NEUTRAL_SCALE_GDP = 0.3        # pp of r* per pp of GDP in desired saving net of investment (Rachel and Smith 2015: 0.20-0.25;
NEUTRAL_SCALE_GDP_RANGE = (0.2, 0.5)  # Rachel and Summers 2019: 0.33, 0.25-0.5)
NEUTRAL_SCALE = NEUTRAL_SCALE_GDP / GDP_OVER_INCOME                         # pp of r* per pp of income: 0.262
NEUTRAL_SCALE_RANGE = tuple(x / GDP_OVER_INCOME for x in NEUTRAL_SCALE_GDP_RANGE)   # 0.175-0.437 per pp of income
# The investment key (decision 93, her call of 2026-10-28: "R&S's own 0.2 + dial"): Rachel and Smith's own coefficient for a fall in
# investment (2015, BoE SWP 571: a 4 pp fall in investment ~80 bp, their short-termism upper bound), times the share of the fall that
# counts as excess saving — the pass-through: 1 gross (Rachel and Smith read gross investment against gross saving; the central), 0
# the fall netted against capital consumption (the reading the model's net income implies). The envelope draws it over 0-1.
INVESTMENT_KEY_GDP = 0.2       # pp of r* per pp of GDP of investment (Rachel and Smith 2015)
INVESTMENT_PASS_THROUGH = 1.0  # the share of the investment fall that counts as excess saving: 1 gross (the central), 0 netted
INVESTMENT_PASS_THROUGH_RANGE = (0.0, 1.0)


def investment_key(pass_through: float) -> float:
    """alpha_inv at a given pass-through of the investment fall: pp of r* per pp of investment / income (Rachel and Smith's
    coefficient per point of GDP, times the pass-through, converted to the model's income)."""
    return INVESTMENT_KEY_GDP * pass_through / GDP_OVER_INCOME


INVESTMENT_KEY = investment_key(INVESTMENT_PASS_THROUGH)          # the central (gross)
OWNERS_SAVING_GAP = 0.3       # owners' saving out of a marginal unit of income less wage earners', retained earnings included
OWNERS_SAVING_GAP_RANGE = (0.15, 0.45)   # (Kaleckian estimates, short-run: US 0.14-0.43, Sweden 0.39; Mian, Straub and Sufi 2021:
                                         # ~0.20; the horizon caveat in macro_scenarios.EVIDENCE)
DEFICIT_PASS_THROUGH = 0.6     # the share of a primary deficit not offset by private saving (1 - the Ricardian offset, 0.4:
DEFICIT_PASS_THROUGH_RANGE = (0.5, 1.0)  # Gale and Orszag 2004 0.2-0.5, Röhn 2010 ~0.4); 1.0: no offset — beyond the offset
                                         # estimates (a pass-through of at most 0.8), on the direct yield evidence only
START_DEFICIT = 2.06           # % of income: the primary deficit at the start, net of property income received (decision 95: the
                               # model's government has gross debt and no assets): Sweden 2021-25, -(B9 + D41PAY - D4REC), 1.80% of
                               # GDP (Eurostat gov_10a_main; macro_scenarios.fiscal_start_evidence)
START_DEFICIT_ASSET_INCOME = 0.16   # the alternative: the same with the state's property income in revenue, -(B9 + D41PAY) (Log 46)
ELB = -0.5                     # % a year: the effective lower bound — the policy floor (Recognition.elb) and the floor on the debt's rate


@dataclass(frozen=True)
class Bridges:
    pi_star: float = 2.0            # % a year: the basket's price on target
    tau_w: float | None = None      # tax on wage income; None: set at the path's start so that it runs deficit0 (fiscal_start)
    deficit0: float | None = START_DEFICIT   # % of income: the primary deficit at the start (with tau_w None)
    tau_r: float = 0.10             # tax on non-wage income (land rent; in this benchmark also standing in for capital income)
    gov_share: float = 0.20         # spending, share of income
    public_support: float = 0.30    # public share of dependants' baskets
    r0_star: float = 0.75           # % real neutral rate at the start
    capex_key: str = "investment"   # "investment": r* moves with replacement investment / income (alpha_inv); "pace": with
                                    # the pace of tasks moving to machines (alpha_capex; the key as tuned on (b))
    alpha_inv: float = INVESTMENT_KEY  # pp of r* per pp of investment / income (the investment key at its central pass-through)
    alpha_capex: float = 0.25       # pp of r* per pp a year of tasks moving to machines (the pace key)
    alpha_rent: float = NEUTRAL_SCALE * OWNERS_SAVING_GAP      # pp of r* per pp rise in the non-wage share of income
    alpha_fiscal: float = NEUTRAL_SCALE * DEFICIT_PASS_THROUGH  # pp of r* per pp of deficit / income
    tp0: float = 0.30               # % term premium at the start
    # tp_per_debt, debt_threshold and loss_per_debt: illustrative defaults since the macro block's first commit (b3a4c6a, 24 Sep
    # 2026), stated per point of income and never sourced, so not converted (no GDP number to convert). Read as GDP-based for
    # comparison only: the 60%-of-GDP reference is ~69% of income; Laubach's (2009) 3-4 bp per pp of debt / GDP is 0.026-0.035
    # per pp of income, on long nominal yields (r* and expected inflation included). The envelope draws 40-90 and 0-0.05.
    tp_per_debt: float = 0.02       # pp of term premium per pp of debt/income above the threshold
    debt_threshold: float = 60.0    # % of income
    loss_per_debt: float = 0.015    # pp of long-run sovereign loss rate per pp of debt above the threshold
    debt0: float = 40.0             # % of income at the start
    mandate: str = "headline"       # "headline" | "goods" (a core measure excluding shelter)
    phi_pi: float = 1.5             # reaction to measured inflation off target under the goods mandate
    capital_premium: float | None = None   # pp over the real neutral rate: the required return on machine capital.
                                           # None: rho stays at the economy's own value (no feedback)
    rho_shift: float = 0.0          # pp added to the required return (a sustained rate shock)
    rho_halflife: float = 1.0       # years: the required return follows r* with partial adjustment (0: at once, last quarter's r*)
    debt_rate_floor: float | None = ELB   # % a year: the debt pays max(r* + pi*, this) (decision 75 corrected, Log 54: a debt rate
                                          # cannot fall below the policy floor); None: unfloored (the comparators, BRIDGES_B)
    bridges_at: str = "start"       # feedback paths (capital_premium set): "start" r*'s bridges read at the start's required
                                    # return (decision 96: the rate's own effect left to the scale); "path" read along the path
                                    # (the comparators, BRIDGES_B). Fixed-return paths are the same either way


BRIDGES_B = Bridges(tau_w=0.40, deficit0=None, capex_key="pace", alpha_rent=0.05, alpha_fiscal=0.10, debt_rate_floor=None,
                    bridges_at="path")
# The bridges as tuned on (a)/(b): the pace key, the wage tax at 0.40 (on (c) a surplus start), owners' saving 0.05, deficits
# 0.10; the debt's rate unfloored and, on feedback paths, the bridges read along the path, as before the revision (Log 54). Only
# the named comparators (a) and (b) run on them, so that they stay the pre-switch runs array for array.

# The two branches a bank is shown (bank_scenarios, demand, households, speed, regime_digestion, export_paths): the two
# direction bridges at the ends of their evidence ranges, each against the other's opposite end, the scale and the
# investment key held. BRANCHES_B: the same two as set on (b), for the comparators.
BRANCHES = {"deficits dominate": dict(alpha_rent=NEUTRAL_SCALE * OWNERS_SAVING_GAP_RANGE[0],
                                      alpha_fiscal=NEUTRAL_SCALE * DEFICIT_PASS_THROUGH_RANGE[1]),
            "owners' saving dominates": dict(alpha_rent=NEUTRAL_SCALE * OWNERS_SAVING_GAP_RANGE[1],
                                             alpha_fiscal=NEUTRAL_SCALE * DEFICIT_PASS_THROUGH_RANGE[0])}
BRANCHES_B = {"deficits dominate": dict(alpha_fiscal=0.25, alpha_rent=0.02), "owners' saving dominates": dict(alpha_rent=0.12)}


def _deficit(br, e: Economy, q: dict):
    """Deficit, % of income: spending plus the public share of dependants' baskets, less a wage tax and a
    tax on non-wage income (land rent and interest)."""
    interest = e.rho * q["Vm"] * q["K"]
    revenue = br.tau_w * q["v"] * q["n"] + br.tau_r * (e.T + interest)
    spending = br.gov_share * q["income"] + br.public_support * (e.N - q["n"]) * q["Ps"]
    return (spending - revenue) / q["income"] * 100, br.tau_w * q["v"] * q["n"] / revenue


def fiscal_start(br: Bridges, e: Economy) -> Bridges:
    """br with its wage tax set: unchanged when br.tau_w is given; otherwise the tau_w at which economy e's own
    equilibrium (its start) runs the primary deficit br.deficit0 (% of income; the deficit is linear in tau_w). macro_path
    passes the economy the path starts at (start_economy): on a feedback path base at its starting required return, so every
    path — a reverse draw with its premium shifted included — starts at the measured deficit; a sustained rate shock
    (rho_shift) keeps the tax solved before the shock, so its start departs from it."""
    if br.tau_w is not None:
        if br.deficit0 is not None:
            raise ValueError("Bridges: give tau_w or deficit0, not both")
        return br
    if br.deficit0 is None:
        raise ValueError("Bridges: give tau_w or deficit0")
    q = solve(e)
    d0, d1 = (_deficit(replace(br, tau_w=tw), e, q)[0] for tw in (0.0, 1.0))
    return replace(br, tau_w=float((br.deficit0 - d0) / (d1 - d0)), deficit0=None)


def start_economy(base: Economy, br: Bridges) -> Economy:
    """The economy whose equilibrium starts a path on br, before any sustained rate shock: base at a fixed return; on a
    feedback path base at the required return the path starts at, rho = max(r0* + premium, 0) (a reverse draw's shifted
    premium included). rho_shift is excluded: a shock run keeps the wage tax and the bridges set before the shock."""
    if br.capital_premium is None:
        return base
    rho = max(br.r0_star + br.capital_premium, 0.0) / 100
    return base if rho == base.rho else replace(base, rho=rho)


def macro_path(base: Economy, tech: TechPath, br: Bridges = Bridges(), years: float = 15.0, dt: float = 0.25):
    """Quasi-static macro path: an equilibrium each date, then the bridges. Returns a dict of arrays;
    rates and inflation in % a year, fiscal quantities in % of income.
    With br.capital_premium set, the required return on machine capital follows the economy's own real
    rate — rho(t) = rbar(t - dt) + premium (+ rho_shift), rbar following r* with half-life rho_halflife —
    so rates feed back into automation. On such a feedback path the bridges are read where br.bridges_at says:
    "start" (the refit, decision 96: her call "Strip all three") — r*'s three bridges at the start's required return,
    i.e. r* is the fixed-return r* at the economy the path starts at (start_economy), so the loop runs one way, from r*
    through the required return to automation; the actual path (x, wages, the deficit that accumulates into debt, the
    term premium) is still solved at the feedback rho; "path" (the comparators, BRIDGES_B) — the bridges read along the
    path itself, so the rate's own effect on investment, owners' income and the deficit feeds back into r*. (Following
    last quarter's r* at once can cycle on "path": near full automation a small change in rho moves x a lot, the
    quarterly pace swings and r* with it.) On a "path" feedback path the pace of automation uses backward differences,
    as it must when r* at t depends on the past; on a fixed-return or "start" path central differences.
    Also returned: r* = r0* + r_star_capex + r_star_owners + r_star_fiscal (the three terms as added) and pace_key, the
    pace the pace key would use — on a "start" path all four the start's fixed-return path's.
    With br.tau_w None the wage tax is solved on the economy the path starts at (start_economy: on a feedback path, base at
    the starting required return), so the path starts at br.deficit0 whatever its premium; a sustained rate shock (rho_shift)
    keeps the tax and the bridges set before the shock (decision 77 corrected, Log 54)."""
    if br.capex_key not in ("investment", "pace"):
        raise ValueError(f"capex_key {br.capex_key!r}: 'investment' or 'pace'")
    if br.bridges_at not in ("start", "path"):
        raise ValueError(f"bridges_at {br.bridges_at!r}: 'start' or 'path'")
    e0 = start_economy(base, br)
    br = fiscal_start(br, e0)          # the wage tax solved on the path's own start (decision 77 corrected): a shock run keeps it
    t = np.arange(0.0, years + 1e-9, dt)
    feedback = br.capital_premium is not None
    key = (macro_path(e0, tech, replace(br, capital_premium=None, rho_shift=0.0), years, dt)
           if feedback and br.bridges_at == "start" else None)   # the bridges at the start's required return (decision 96)
    econ, sol, r_seq, terms = [], [], [], []
    if not feedback:
        econ = [tech.at(ti, base) for ti in t]
        if br.rho_shift:
            econ = [replace(e, rho=e.rho + br.rho_shift / 100) for e in econ]
        sol = [solve(e) for e in econ]
    else:
        r_prev = r_req = br.r0_star
        w = 1.0 - 0.5 ** (dt / br.rho_halflife) if br.rho_halflife > 0 else 1.0
        nw0 = d0 = None
        for i, ti in enumerate(t):
            r_req += w * (r_prev - r_req)
            e = replace(tech.at(ti, base), rho=max(r_req + br.capital_premium + br.rho_shift, 0.0) / 100)   # a required return is not negative
            q = solve(e)
            econ.append(e); sol.append(q)
            if key is not None:                       # r* read at the start's required return: the fixed-return r* there
                r_prev = float(key["r_star"][i])
            else:                                     # the bridges read along the path (the comparators)
                nonwage = (1.0 - q["labor_share"]) * 100
                dfc, _ = _deficit(br, e, q)
                if i == 0:
                    nw0, d0, inv0, pace = nonwage, dfc, q["inv_income"] * 100, 0.0
                else:
                    pace = (q["x"] - sol[i - 1]["x"]) / dt * 100
                capex = br.alpha_capex * pace if br.capex_key == "pace" else br.alpha_inv * (q["inv_income"] * 100 - inv0)
                owners = br.alpha_rent * (nonwage - nw0)
                fiscal = br.alpha_fiscal * (dfc - d0)
                r_prev = br.r0_star + capex - owners + fiscal
                terms.append((capex, -owners, fiscal, pace))
            r_seq.append(r_prev)
    get = lambda k: np.array([q[k] for q in sol])  # noqa: E731
    v, Ps, p, n, inc, X, Y, x = get("v"), get("Ps"), get("p"), get("n"), get("income"), get("X"), get("Y"), get("x")
    ls = get("labor_share")
    grad = lambda y: np.gradient(np.log(y), t) * 100  # noqa: E731
    # nominal: the basket on target; everything else at pi* plus its real change against the basket
    pi_goods = br.pi_star + grad(p / Ps)
    pi_shelter = br.pi_star + grad(1.0 / Ps)
    pi_wage = br.pi_star + grad(v / Ps)
    # fiscal
    fis = [_deficit(br, e, q) for e, q in zip(econ, sol)]
    deficit = np.array([f[0] for f in fis])
    wage_tax_share = np.array([f[1] for f in fis])
    growth = br.pi_star + grad(Y)
    # neutral real rate
    automation_pace = np.gradient(x, t) * 100                    # pp of tasks moving to machines, a year
    nonwage_share = (1.0 - ls) * 100
    inv_income = get("inv_income")
    if feedback:
        r_star = np.array(r_seq)
        if key is not None:
            r_capex, r_owners, r_fiscal, pace_key = (key[k] for k in ("r_star_capex", "r_star_owners", "r_star_fiscal", "pace_key"))
        else:
            r_capex, r_owners, r_fiscal, pace_key = (np.array(c) for c in zip(*terms))
    else:
        capex = (br.alpha_capex * automation_pace if br.capex_key == "pace"
                 else br.alpha_inv * (inv_income * 100 - inv_income[0] * 100))
        owners = br.alpha_rent * (nonwage_share - nonwage_share[0])
        fiscal = br.alpha_fiscal * (deficit - deficit[0])
        r_star = br.r0_star + capex - owners + fiscal
        r_capex, r_owners, r_fiscal, pace_key = capex, -owners, fiscal, automation_pace
    # debt and premia
    debt = np.empty_like(t)
    debt[0] = br.debt0
    for i in range(1, len(t)):
        rate = r_star[i - 1] + br.pi_star                         # the debt's nominal rate, floored at the policy floor (decision 75)
        if br.debt_rate_floor is not None:
            rate = max(rate, br.debt_rate_floor)
        debt[i] = debt[i - 1] + dt * (deficit[i - 1] + (rate - growth[i - 1]) / 100 * debt[i - 1])
    over = np.maximum(debt - br.debt_threshold, 0.0)
    tp = br.tp0 + br.tp_per_debt * over
    loss_longrun = br.loss_per_debt * over
    # the desired policy rate
    desired = r_star + br.pi_star
    if br.mandate == "goods":
        desired = desired + br.phi_pi * (pi_goods - br.pi_star)
    return dict(t=t, eta=np.array([e.eta for e in econ]), lam=np.array([e.lam for e in econ]),
                rho=np.array([e.rho for e in econ]) * 100, x=x, v=v, Ps=Ps, p=p, n=n,
                participation=get("participation"), income=inc, labor_share=ls, capital_share=get("capital_share"),
                capital_output=get("capital_output"), real_wage=get("real_wage"), X=X, Y=Y, funded=get("funded"),
                pi_goods=pi_goods, pi_shelter=pi_shelter, pi_wage=pi_wage, deficit=deficit,
                wage_tax_share=wage_tax_share, debt=debt, r_star=r_star, tp=tp, loss_longrun=loss_longrun,
                desired=desired, automation_pace=automation_pace, nonwage_share=nonwage_share, pi_star=br.pi_star,
                tau_w=br.tau_w, inv_income=inv_income,
                # r*'s three bridge terms as added (r* = r0* + the three) and the pace the pace key would use (decision 96)
                r_star_capex=r_capex, r_star_owners=r_owners, r_star_fiscal=r_fiscal, pace_key=pace_key,
                # (c) additions: the machine chain along the path (BEA basis; see solve)
                labour_share_bea=get("labour_share_bea"), chain_share=get("chain_share"), theta_V=get("theta_V"),
                sigma_V=get("sigma_V"), multiplier=get("multiplier"), x_ceiling=get("x_ceiling"),
                final_hours=get("final_hours"), machine_hours=get("machine_hours"), Vm=get("Vm"), K=get("K"))


# ------------------------------------------------------------------ from the macro path to the curve layer
@dataclass(frozen=True)
class Recognition:
    """How fast the market learns the destination the macro path is heading for (the recognition
    clock); the central bank delivers through curve.PolicyRule (the institutions clock)."""
    h_dest: float = 1.0             # half-life (years) of the market's learning of the neutral rate
    k2: float = 0.3                 # speed at which the cycle target returns to the destination
    elb: float = ELB                # effective lower bound: policy delivers the desired rate only down to here


def curve_path(mp: dict, rec: Recognition = Recognition(), rule=None):
    """CurveStates for the common (OIS) curve and SovereignStates for the government spread, one per date
    of the macro path. Policy steps toward the desired rate on the meeting calendar; the market's
    destination learns r* + pi* with half-life h_dest; the cycle target is the desired rate; the term
    premium and the sovereign long-run loss come from debt."""
    import curve as cv
    import sovereign as sv
    rule = rule or cv.PolicyRule()
    t, desired = mp["t"], mp["desired"]
    M = rule.meetings_per_year
    r = max(round(float(desired[0]) / rule.step) * rule.step, rec.elb)
    next_meet = 1.0 / M
    dest = float(mp["r_star"][0] + mp["pi_star"])
    states, sovs, policy = [], [], []
    for i, ti in enumerate(t):
        while ti + 1e-12 >= next_meet:
            r = max(rule.decide(r, max(float(np.interp(next_meet, t, desired)), rec.elb)), rec.elb)
            next_meet += 1.0 / M
        if i > 0:
            target = max(float(mp["r_star"][i] + mp["pi_star"]), rec.elb)      # expectations respect the lower bound
            dest += (target - dest) * (1.0 - 0.5 ** ((ti - t[i - 1]) / rec.h_dest))
        states.append(cv.CurveState(r0=r, m0=max(float(desired[i]), rec.elb), rbar=dest, k1=rule.implied_speed(), k2=rec.k2,
                                    tp=float(mp["tp"][i]), delay=next_meet - ti))
        lr = float(mp["loss_longrun"][i])
        sovs.append(sv.SovereignState(cv.CurveState(r0=0.0, m0=lr, rbar=lr, k1=0.5, k2=0.2, tp=0.0)))
        policy.append(r)
    return states, sovs, np.array(policy)


# ------------------------------------------------------------------ calibration of the normal case
CALIBRATION_BASE = Economy(g0=0.02, g1=0.98)     # machines up to 50x better than people on the easiest task


def calibrate(targets=None, base: Economy = CALIBRATION_BASE):
    """Choose T, h, chi_max and the schedule's convexity k (N = 1; a, b, lambda held at the paper's
    values; g0 = 0.02) so the starting equilibrium hits public targets:
      - labour share 0.47: the paper's full-chain human-effort share of consumed production (Figure 7, 2023);
      - participation 0.60: an employment rate;
      - 3 support baskets of output per person: the support basket as a subsistence bundle, a third of
        average consumption (the Orshansky construction the paper's coverage measure uses);
      - site share of the basket 0.13: the land part of a shelter share of about a third, at the 30-50%
        land shares of housing the paper's coverage measure uses. Appendix B's space is pure site.
    What the benchmark cannot separate: with two primary factors, everything not paid to hours is rent on
    non-produced inputs, so the machine chains' land (about 0.40 of income here) also stands in for what
    national accounts call capital income. History calibrates the normal case only."""
    from scipy.optimize import least_squares
    tg = {"labor_share": 0.47, "participation": 0.60, "baskets_per_person": 3.0, "site_share": 0.13, **(targets or {})}

    def build(q):
        return replace(base, N=1.0, T=float(np.exp(q[0])), h=float(np.exp(q[1])), chi_max=float(np.exp(q[2])),
                       k=float(np.exp(q[3])))

    def resid(q):
        e = build(q)
        try:
            s_ = solve(e)
        except (ValueError, AssertionError):
            return [10.0] * 4
        return [s_["labor_share"] - tg["labor_share"], s_["participation"] - tg["participation"],
                (s_["Y"] / e.N - tg["baskets_per_person"]) / tg["baskets_per_person"], e.h / s_["Ps"] - tg["site_share"]]
    best = None
    for q0 in ([0.0, np.log(0.5), np.log(2.0), np.log(6.0)], [np.log(3.0), np.log(1.0), np.log(1.0), np.log(3.0)],
               [np.log(0.5), np.log(0.2), np.log(2.0), np.log(10.0)], [np.log(1.5), np.log(0.4), np.log(3.0), np.log(5.0)]):
        r = least_squares(resid, q0, bounds=([np.log(1e-4)] * 3 + [np.log(0.2)], [np.log(1e3)] * 3 + [np.log(60.0)]))
        if best is None or r.cost < best.cost:
            best = r
    e = build(best.x)
    return e, solve(e), tg, float(np.max(np.abs(best.fun)))


def income_split(e: Economy, q: dict):
    """Shares of income: labour, the housing site, the machine chains' land, and interest on machine
    capital. With (rho, delta) = (0, 1) — calibration (a) — interest is zero and the machine chains'
    land also stands in for capital income; with capital (calibration (b)) the two are separate."""
    return {"labour": q["labor_share"], "housing_site": e.h * q["Y"] / q["income"],
            "machine_chain_land": e.b * e.delta * q["K"] / q["income"], "interest": q["capital_share"]}


CAPITAL_BASE = replace(CALIBRATION_BASE, rho=0.0575, delta=0.08)   # (b): return 0.75% real + 5% premium; 8% depreciation


# ------------------------------------------------------------------ (c): the machine chain on the national accounts' basis


def calibrate_roots(targets=None, base: Economy = CALIBRATION_BASE, site_basis: str = "basket"):
    """Every root in k of calibrate()'s four targets, in closed form (N = 1; a, b, lambda, rho, delta, g0, g1 held at
    base's), sorted by k. calibrate() is unchanged: its four-start search returns one root (the low one for (a) and (b));
    this finds the other too, so (c) can be compared root for root. At the targets, participation and output pin x*(k):
        participation / baskets = (1 - x) + lambda delta J(x) / (1 - a delta);
    income = Ps Y (an identity), so the labour share and the site share then need, one equation in k,
        (1 - x) + J(x) / gamma(x) = (1 - site) participation / (labour baskets);
    h = site Ps, T from the land market (h Y + b delta K) and chi_max from participation follow. Raises ValueError if no
    k in [0.05, 400] fits. site_basis "gdp" reads the site share as the measured flow h Y / (income + delta Vm K), as
    ChainTargets does (calibration (c)'s variant (ii)); the equation in k becomes
        (1 - x) + J(x) / gamma(x) (1 + site u / (1 - a delta)) = (1 - site) participation / (labour baskets),
    u = delta / (rho + delta), and Ps = (p + site delta Vm K / Y) / (1 - site). The default path is unchanged."""
    if site_basis not in ("basket", "gdp"):
        raise ValueError(f"site_basis {site_basis!r}: 'basket' or 'gdp'")
    tg = {"labor_share": 0.47, "participation": 0.60, "baskets_per_person": 3.0, "site_share": 0.13, **(targets or {})}
    L, P, B, s = tg["labor_share"], tg["participation"], tg["baskets_per_person"], tg["site_share"]
    c = base.lam * base.delta / (1.0 - base.a * base.delta)
    g0, g1 = base.g0, base.g1
    need = (1.0 - s) * P / (L * B)
    jm = 1.0 + s * base.delta / (base.rho + base.delta) / (1.0 - base.a * base.delta) if site_basis == "gdp" else None

    def x_of(k):
        return brentq(lambda x: (1.0 - x) + c * (g0 * x + g1 * x ** (k + 1.0) / (k + 1.0)) - P / B, 0.0, 1.0, xtol=1e-16)

    def F(k):
        x = x_of(k)
        if jm is not None:
            return (1.0 - x) + (g0 * x + g1 * x ** (k + 1.0) / (k + 1.0)) / (g0 + g1 * x ** k) * jm - need
        return (1.0 - x) + (g0 * x + g1 * x ** (k + 1.0) / (k + 1.0)) / (g0 + g1 * x ** k) - need

    ks = np.exp(np.linspace(np.log(0.05), np.log(400.0), 4001))
    lo, hi = np.zeros_like(ks), np.ones_like(ks)                      # x*(k) on the grid by vectorised bisection
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        up = (1.0 - mid) + c * (g0 * mid + g1 * mid ** (ks + 1.0) / (ks + 1.0)) - P / B > 0
        lo, hi = np.where(up, mid, lo), np.where(up, hi, mid)
    xg = 0.5 * (lo + hi)
    Fg = (1.0 - xg) + (g0 * xg + g1 * xg ** (ks + 1.0) / (ks + 1.0)) / (g0 + g1 * xg ** ks) - need
    if jm is not None:
        Fg = (1.0 - xg) + (g0 * xg + g1 * xg ** (ks + 1.0) / (ks + 1.0)) / (g0 + g1 * xg ** ks) * jm - need
    roots = [brentq(F, ks[i], ks[i + 1], xtol=1e-14) for i in range(len(ks) - 1) if Fg[i] * Fg[i + 1] < 0]
    if not roots:
        raise ValueError("no schedule convexity k in [0.05, 400] fits calibrate()'s targets")
    out = []
    for k in roots:
        x = x_of(k)
        e = replace(base, N=1.0, k=float(k), eta=1.0)
        gam, J = e.gamma(x), e.J(x)
        cpt = e.rho + e.delta
        pm = cpt * e.b / (1.0 - cpt * (e.a + e.lam * gam))
        v = gam * pm
        if jm is not None:                                   # the site as the measured flow: h Y / (income + delta Vm K)
            p_ = v * (1.0 - x) + pm * J
            Ps = (p_ + s * e.delta * (pm / cpt) * J / (1.0 - e.a * e.delta)) / (1.0 - s)
            h = Ps - p_
        else:
            Ps = (v * (1.0 - x) + pm * J) / (1.0 - s)
            h = s * Ps
        T = B * (h + e.b * e.delta * J / (1.0 - e.a * e.delta))
        e = replace(e, T=float(T), h=float(h), chi_max=float(np.log1p(v / Ps) / P))
        out.append((e, dict(k=float(k), x=float(x), need=need, **({"site_basis": "gdp"} if jm is not None else {}))))
    return sorted(out, key=lambda p: p[1]["k"])


# ------------------------------------------------------------------ the central calibration: (c), the open reading
CENTRAL_TAG = "c_central"                       # calibration_c.py's name for it
CENTRAL_ROOTS = ("lo", "hi")                    # "lo": the central (the low root in k, (a)/(b)'s branch); "hi": the sensitivity
CENTRAL_SOURCE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "results", "calibration_c.json")
TECH_SPEEDS = {"slow": dict(t_mid=10, width=12), "medium": dict(t_mid=6, width=6), "fast": dict(t_mid=3, width=2)}
DEEP_ETA_END = 0.04                             # capability's end point on the deep-automation path (macro_scenarios)
LAM_END_DIVISOR = 5.0                           # recursive automation: lambda ends at a fifth of the economy's own start
CENTRAL_RTOL = 1e-9                             # central(): the largest relative gap, in any parameter, between a re-solve
                                                # and the stored central it accepts (another platform's last bits)
_CENTRAL: dict = {}


def param_gap(e: Economy, ref: Economy) -> float:
    """The largest relative gap between two economies' parameters, |e - ref| / |ref| (absolute where ref's is 0)."""
    gaps = []
    for k in Economy.__dataclass_fields__:
        a, b = float(getattr(e, k)), float(getattr(ref, k))
        gaps.append(abs(a - b) / abs(b) if b != 0.0 else abs(a - b))
    return max(gaps)


def central(root: str = "lo"):
    """(Economy, info) for calibration (c)'s central economy, the open (domp) reading: root "lo" (the central) or "hi" (the
    sensitivity). Built once and cached: the economy is the parameters stored in results/calibration_c.json, returned
    after the central ChainTargets stored there (theta_V, chain share, the fixed-point sigma_V, delta, labour 0.47, g0
    0.01, her other three) are re-solved by calibrate_c and the re-solve agrees with them to a relative CENTRAL_RTOL (1e-9)
    in every parameter (RuntimeError otherwise: rerun code/calibration_c.py). On the development machine the two are
    bit-identical (checks/check_calibration_c.py E1); the tolerance lets another platform's numpy/scipy differ in the last
    bits without moving the stored numbers.
    info: tag, root, rho; capital_premium — pp over Bridges().r0_star, so a feedback path (Bridges.capital_premium set)
    starts at this rho; multiplier (1 + theta_V/sigma_V at the start); headroom_pp (rate_headroom); k, x, x_ceiling,
    theta_V, sigma_V, chain_share, participation, labour_share_bea at the start; targets (the ChainTargets); resolve_gap
    (param_gap of the re-solve against the stored parameters: 0.0 when bit-identical); source.
    A module that sets its own r0_star takes the premium from capital_premium(e, br) or feedback_bridges(e, ...)."""
    if root not in CENTRAL_ROOTS:
        raise ValueError(f"root {root!r}: one of {CENTRAL_ROOTS}")
    if root not in _CENTRAL:
        tag = f"{CENTRAL_TAG}_{root}"
        with open(CENTRAL_SOURCE, encoding="utf-8") as f:
            stored = json.load(f)["calibrations"][tag]
        tg = ChainTargets(**stored["targets"])
        sols = calibrate_c(tg)
        if len(sols) != len(CENTRAL_ROOTS):
            raise RuntimeError(f"{tag}: calibrate_c finds {len(sols)} roots in k, not {len(CENTRAL_ROOTS)}")
        e = Economy(**stored["params"])
        gap = param_gap(sols[CENTRAL_ROOTS.index(root)][0], e)
        if not gap <= CENTRAL_RTOL:
            raise RuntimeError(f"{tag}: re-solved parameters differ from results/calibration_c.json by a relative {gap:.1e} "
                               f"(more than {CENTRAL_RTOL:.0e}); rerun code/calibration_c.py")
        q = solve(e)
        info = dict(tag=tag, root=root, rho=e.rho, capital_premium=capital_premium(e), multiplier=q["multiplier"],
                    headroom_pp=rate_headroom(e), k=e.k, x=q["x"], x_ceiling=q["x_ceiling"], theta_V=q["theta_V"],
                    sigma_V=q["sigma_V"], chain_share=q["chain_share"], participation=q["participation"],
                    labour_share_bea=q["labour_share_bea"], targets=tg, resolve_gap=gap,
                    source="results/calibration_c.json calibrations['" + tag + "']['targets'], re-solved by macro.calibrate_c; "
                           + ("equal to the stored params bit for bit" if gap == 0.0 else
                              f"the stored params, which the re-solve matches to a relative {gap:.1e} (accepted to "
                              f"{CENTRAL_RTOL:.0e})"))
        _CENTRAL[root] = (e, info)
    e, info = _CENTRAL[root]
    return e, dict(info)


def deep_tech(e: Economy, t_mid: float = 6, width: float = 6, eta_end: float = DEEP_ETA_END) -> TechPath:
    """Deep automation relative to the economy's own start: capability eta -> eta_end (0.04), and recursive automation
    lambda -> e.lam / 5 (a fifth of its own start; (b)'s 0.05 -> 0.01 exactly). The default clock is the medium speed;
    TECH_SPEEDS holds slow / medium / fast (macro_scenarios' three): deep_tech(e, **TECH_SPEEDS['fast'])."""
    return TechPath(eta_end=eta_end, lam_end=e.lam / LAM_END_DIVISOR, t_mid=t_mid, width=width)


def hold_tech(e: Economy) -> TechPath:
    """The status quo: capability and lambda held at the economy's own start (the old world of a two-world run)."""
    return TechPath(eta_end=1.0, lam_end=e.lam)


def capital_premium(e: Economy, br: Bridges | None = None) -> float:
    """The capital premium (pp) over br's starting neutral rate that makes a feedback path's required return start at the
    economy's own: rho(0) = (r0_star + premium) / 100 = e.rho. (b): 5.75 - 0.75 = 5.0; (c) central: rho x 100 - 0.75."""
    br = br if br is not None else Bridges()
    return e.rho * 100 - br.r0_star


def feedback_bridges(e: Economy, base: Bridges | None = None, **overrides) -> Bridges:
    """base (default Bridges(): the refit) with overrides, and the required return following r* from the economy's own rho
    (capital_premium against the result's own r0_star). The premium is computed, so it may not be passed. The named
    comparators (a) and (b) pass base=BRIDGES_B."""
    if "capital_premium" in overrides:
        raise TypeError("feedback_bridges computes capital_premium; pass Bridges(...) directly to set it by hand")
    br = replace(Bridges() if base is None else base, **overrides)
    return replace(br, capital_premium=capital_premium(e, br))
