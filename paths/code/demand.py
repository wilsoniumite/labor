# demand.py — a demand gap for the macro block: when policy is set on a lagging estimate of the neutral rate, or
# pinned at the floor, output leaves capacity; unemployment and inflation follow.
#
# The macro block (macro.py) is quasi-static: every date is an equilibrium at capacity, and the central bank is
# assumed to deliver the neutral rate r* plus the target at once. So it cannot produce a recession, a boom or a
# deflation. This layer adds the missing step, in the smallest standard form (a reduced-form IS curve, an
# expectations-augmented Phillips curve, a Taylor rule with smoothing and a floor), with one feature that carries
# the paper's question: the central bank learns r* with a lag. Automation moves r* (down when owners' saving
# dominates, up when deficits do); a policymaker whose estimate trails the truth sets policy too tight on the way
# down and too loose on the way up.
#
# Each quarter:
#   the central bank's r* estimate    rhat_t = rhat_{t-1} + (1 - 0.5^(dt/h)) (r*_t - rhat_{t-1})     h: half-life (years)
#   expected inflation                pie_t  = anchor pi* + (1 - anchor) pi_{t-1}
#   policy                            i_t    = max(elb, s i_{t-1} + (1-s) [rhat_t + pie_t + phi_pi (pi_{t-1} - pi*) + phi_y gap_{t-1}])
#   output gap (% of capacity)        gap_t  = a1 gap_{t-1} - a_r (i_t - pie_t - r*_t)
#   headline inflation (% a year)     pi_t   = pie_t + kappa gap_t
#   unemployment above structural     du_t   = -okun gap_t
# The equilibrium's relative prices ride on top: goods, shelter and wage inflation are the macro block's (which
# hold the basket on target) shifted by pi_t - pi*. Actual output = capacity x (1 + gap/100).
#
# Calibration. okun and kappa are MEASURED on Swedish public data, 2001-2026 (sweden_cycle below): Okun from
# unemployment changes on GDP growth over four quarters; the Phillips slope from core inflation (CPIF excluding
# energy) against the unemployment gap (unemployment less its Hodrick-Prescott trend), then kappa = slope x okun.
# a1 and a_r are the literature's (Laubach and Williams 2003, US: the gap's own persistence ~0.94 a quarter and
# ~0.1 of a point per point of real-rate gap; approximate), with a range run. The r* learning half-life is the dial
# the forward-rate test measured (results/regime_digestion.json): regime anchors 7-11 years before 2021, 2-3 since.
#
# The worlds (her decision, 2026-09-30): calibration (c)'s central economy, macro.central() — the open (domp) reading, low
# root — through bank_scenarios.path (the required return following r* from the economy's own rho; deep automation to a
# fifth of its own lambda). The high root (the sensitivity) and (b) (the comparator; bit-identical to the pre-switch runs)
# are stored beside it for the central learning variant.
#
# THE NEUTRAL RATE. r* is the macro block's bridge, refit on (c) (Log 46): its capex channel keyed to investment spending
# (delta Vm K / income) at the common scale (macro.NEUTRAL_SCALE, 0.3 pp of r* per pp of income), owners' saving and deficits
# on the same scale. A readout, not the default: the same r* with the capex term keyed to the pace of tasks moving instead
# (alpha_capex 0.25 pp of r* per pp a year, the key as tuned on (b)). On the comparator (b), keyed to the pace, the readout
# before the refit stays: the capex term keyed to investment at two scales —
#   the bridge's own scale — alpha_capex converted at (b)'s start, where it was set: moving 1 pp of tasks a year at
#     (b)'s prices needs net investment of Vm dK/dx x 0.01 / income (6.35% of income), so alpha_inv = 0.25 / 6.35 = 0.039;
#   the demand layer's scale — investment spending not replaced by other spending is a demand level, and the IS curve
#     above closes a held level L with a real rate L (1 - a1)/a_r higher: alpha_inv = 0.06 / 0.10 = 0.6 (an upper end).
# The readouts do not feed back into the required return (the macro path is unchanged); the demand layer is run on them.
# The series keyed to is replacement investment, the only investment in the quasi-static accounts. Net investment, Vm dK/dt
# / income, is stored beside it as a diagnostic: on every deep path, (b) included, the machine stock K falls (capability
# makes each machine do more tasks), so net investment is negative — keying to it would lower r* further, not less.
#
# Public data only: Statistics Sweden (GDP volume, seasonally adjusted; labour force survey, quarterly, seasonally
# adjusted; CPIF excluding energy); the economy from results/calibration_c.json (BEA; code/calibration_c.py).
# Run from paths/:  ../venv/Scripts/python.exe code/demand.py
# Out: results/demand.json, figures/fig_demand.png

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass, replace

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bank_scenarios as bs  # noqa: E402
import deposits_wages as dw  # noqa: E402
import macro as m  # noqa: E402
from regime_digestion import ols_hac  # noqa: E402


# ------------------------------------------------------------------ Sweden's cycle, measured
def hp_trend(y: np.ndarray, lam: float = 1600.0) -> np.ndarray:
    n = len(y)
    D = np.zeros((n - 2, n))
    for i in range(n - 2):
        D[i, i:i + 3] = (1.0, -2.0, 1.0)
    return np.linalg.solve(np.eye(n) + lam * D.T @ D, y)


def sweden_cycle() -> dict:
    """Okun's coefficient and the Phillips slope on Swedish data, 2001Q1 onward (quarterly)."""
    gdp = dw.scb_table("NR/NR0103/NR0103B/NR0103ENS2010T10SKv", {"Anvandningstyp": "BNPM", "ContentsCode": "NR0103CE"}, "gdp_volume_sa").iloc[:, 0]
    lfs = dw.scb_table("AM/AM0401/AM0401A/AKURLBefK", {"Arbetskraftstillh": "ALÖSP", "TypData": "SR_DATA", "Kon": "1+2", "Alder": "tot15-74",
                                                       "ContentsCode": "000007V3"}, "lfs_unemp_q_sa").iloc[:, 0]
    cpi = dw.scb_table("PR/PR0101/PR0101J/KPIFXE2020", {"ContentsCode": "000007ZW"}, "kpifxe_index").iloc[:, 0]
    cpi_q = cpi.groupby(cpi.index.asfreq("Q")).mean()
    d = pd.DataFrame({"g": np.log(gdp).diff(4) * 100, "du": lfs.diff(4), "u": lfs, "pi": np.log(cpi_q).diff(4) * 100}).dropna()
    d["ugap"] = d.u - hp_trend(d.u.values)
    ok_b, ok_se = ols_hac(d.du.values, d.g.values, 4)
    # Phillips: core inflation off target on the unemployment gap, with last year's inflation off target (persistence)
    d["pi_dev"] = d.pi - 2.0
    d["pi_dev_lag"] = d.pi_dev.shift(4)
    p = d.dropna()
    ph_b, ph_se = ols_hac(p.pi_dev.values, np.column_stack([p.ugap.values, p.pi_dev_lag.values]), 4)
    okun = -float(ok_b[1])
    return {"sample": [str(d.index[0]), str(d.index[-1])], "okun_du_per_pp_growth": {"coef": round(float(ok_b[1]), 3), "se": round(float(ok_se[1]), 3)},
            "okun": round(okun, 3),
            "phillips_per_pp_unemployment_gap": {"coef": round(float(ph_b[1]), 3), "se": round(float(ph_se[1]), 3)},
            "phillips_persistence_4q": {"coef": round(float(ph_b[2]), 3), "se": round(float(ph_se[2]), 3)},
            "kappa_per_pp_output_gap": round(float(-ph_b[1] * okun), 3),
            "ugap_range": [round(float(d.ugap.min()), 2), round(float(d.ugap.max()), 2)]}


# ------------------------------------------------------------------ the layer
@dataclass(frozen=True)
class Demand:
    a1: float = 0.94          # the gap's own persistence, per quarter [literature, approximate]
    a_r: float = 0.10         # gap response per point of real-rate gap, per quarter [literature, approximate]
    kappa: float = 0.15       # headline inflation (% a year) per point of output gap [replaced by the measured value]
    okun: float = 0.4         # unemployment points per point of output gap [replaced by the measured value]
    anchor: float = 0.9       # weight of the target in expected inflation
    phi_pi: float = 1.5
    phi_y: float = 0.5
    smooth: float = 0.7       # policy smoothing per quarter
    h: float = 3.0            # years: half-life of the central bank's r* learning
    elb: float = -0.5


def run(mp: dict, dm: Demand = Demand(), shock: np.ndarray | None = None, i0: float | None = None, extra=None) -> dict:
    """shock: an exogenous demand shock added to the gap each quarter (% of capacity) — a crash, a wealth or
    confidence shock. i0: the policy rate at the start (default: neutral, r*_0 + pi*); below neutral means the
    economy starts with less room to the floor. extra: a function (k, state) -> a demand LEVEL (% of capacity) that
    other layers compute from the state so far (households.py). Spending moves output at once: the gap less that
    level follows the IS dynamics, i.e. gap_t = a1 gap_{t-1} - a_r (real-rate gap) + level_t - a1 level_{t-1}; a level
    held for good moves the gap by its size before policy responds, a temporary one (a check) while it lasts."""
    t, dt = mp["t"], float(mp["t"][1] - mp["t"][0])
    rs, pis = mp["r_star"], float(mp["pi_star"])
    n = len(t)
    sh = np.zeros(n) if shock is None else np.asarray(shock, float)
    rhat, i_, gap, pi, pie, rr, lvl = (np.zeros(n) for _ in range(7))
    rhat[0], pi[0], pie[0] = rs[0], pis, pis
    i_[0] = max(rs[0] + pis if i0 is None else i0, dm.elb)
    w = 1.0 - 0.5 ** (dt / dm.h) if dm.h > 0 else 1.0
    for k in range(1, n):
        rhat[k] = rhat[k - 1] + w * (rs[k] - rhat[k - 1])
        pie[k] = dm.anchor * pis + (1 - dm.anchor) * pi[k - 1]
        target = rhat[k] + pie[k] + dm.phi_pi * (pi[k - 1] - pis) + dm.phi_y * gap[k - 1]
        i_[k] = max(dm.elb, dm.smooth * i_[k - 1] + (1 - dm.smooth) * target)
        rr[k] = i_[k] - pie[k]
        lvl[k] = 0.0 if extra is None else extra(k, {"policy": i_, "gap": gap, "inflation": pi, "t": t})
        gap[k] = dm.a1 * gap[k - 1] - dm.a_r * (rr[k] - rs[k]) + sh[k] + lvl[k] - dm.a1 * lvl[k - 1]
        pi[k] = pie[k] + dm.kappa * gap[k]
    rr[0] = i_[0] - pie[0]
    shift = pi - pis
    return {"t": t, "policy": i_, "r_star": rs, "r_star_cb": rhat, "real_rate": rr, "gap": gap, "inflation": pi,
            "pi_goods": mp["pi_goods"] + shift, "pi_shelter": mp["pi_shelter"] + shift, "pi_wage": mp["pi_wage"] + shift,
            "unemployment_up": -dm.okun * gap, "at_floor": i_ <= dm.elb + 1e-9,
            "output": (mp["Y"] / mp["Y"][0]) * (1 + gap / 100), "capacity": mp["Y"] / mp["Y"][0],
            "participation": mp["participation"] / mp["participation"][0]}


def summary(r: dict, horizon: float = 15.0) -> dict:
    w = r["t"] <= horizon + 1e-9
    t = r["t"][w]
    at = lambda x, ys=(3, 5, 8, 10, 12, 15): [round(float(np.interp(y, r["t"], x)), 2) for y in ys]  # noqa: E731
    g, pi = r["gap"][w], r["inflation"][w]
    fl = r["at_floor"][w]
    return {"gap_min_and_year": [round(float(g.min()), 2), round(float(t[np.argmin(g)]), 2)],
            "gap_max_and_year": [round(float(g.max()), 2), round(float(t[np.argmax(g)]), 2)],
            "inflation_min_max": [round(float(pi.min()), 2), round(float(pi.max()), 2)],
            "unemployment_up_max": round(float(r["unemployment_up"][w].max()), 2),
            "years_at_floor": round(float(fl.sum() * (t[1] - t[0])), 2),
            "first_year_at_floor": round(float(t[np.argmax(fl)]), 2) if fl.any() else None,
            "y3_y5_y8_y10_y12_y15": {"policy": at(r["policy"]), "r_star": at(r["r_star"]), "r_star_cb": at(r["r_star_cb"]),
                                    "gap": at(r["gap"]), "inflation": at(r["inflation"]), "goods": at(r["pi_goods"]),
                                    "shelter": at(r["pi_shelter"]), "wages": at(r["pi_wage"]), "unemployment_up": at(r["unemployment_up"]),
                                    "output": at(r["output"]), "capacity": at(r["capacity"])}}


def world(bridges: dict, truth: str, fast: bool = False, e=None, base=None) -> dict:
    """The true world's macro path for one of the bank scenarios' bridge settings, on economy e (default: the central
    (c), macro.central()) and base bridges (default the refit; the comparator (b) passes macro.BRIDGES_B); fast:
    automation's midpoint at year 3 over a 2-year width, instead of year 6 over 6 years."""
    e = m.central()[0] if e is None else e
    if not fast:
        old, new, _, _, _ = bs.path(e, bridges, truth, base=base)
        return new if truth == "new" else old
    br = m.feedback_bridges(e, base=base, **bridges)
    tech = m.deep_tech(e, **m.TECH_SPEEDS["fast"]) if truth == "new" else m.hold_tech(e)
    return m.macro_path(e, tech, br, 25.0, 0.25)


# ------------------------------------------------------------------ the neutral rate with the capex channel keyed to investment
def investment_income(mp: dict, e) -> np.ndarray:
    """Investment spending over income along a macro path, % (delta Vm K / income: the quasi-static economy's gross
    investment, replacement at each date's stock; macro.solve's inv_income)."""
    return e.delta * mp["Vm"] * mp["K"] / mp["income"] * 100


def net_investment_income(mp: dict) -> np.ndarray:
    """Net investment over income along a macro path, % (Vm dK/dt / income, central differences): a diagnostic outside the
    quasi-static accounts, which carry replacement only."""
    return mp["Vm"] * np.gradient(mp["K"], mp["t"]) / mp["income"] * 100


def pace(mp: dict, br) -> np.ndarray:
    """The pace of tasks moving to machines (pp a year) as macro_path computes it — backward differences on a feedback path
    (Bridges.capital_premium set), central differences otherwise."""
    t = mp["t"]
    return np.r_[0.0, np.diff(mp["x"]) / np.diff(t) * 100] if br.capital_premium is not None else np.gradient(mp["x"], t) * 100


def capex_term(mp: dict, br) -> np.ndarray:
    """The capex channel as macro_path computes it: alpha_inv x the change in investment / income since the start (pp; the
    investment key, the refit's) or alpha_capex x the pace of tasks moving (the pace key, as tuned on (b))."""
    if br.capex_key == "pace":
        return br.alpha_capex * pace(mp, br)
    inv = mp["inv_income"] * 100
    return br.alpha_inv * (inv - inv[0])


def alpha_inv_bridge(e_b, alpha_capex: float = m.Bridges().alpha_capex) -> dict:
    """alpha_capex (pp of r* per pp a year of tasks moving) converted to pp of r* per pp of income in investment spending, at
    the start of economy e_b ((b), where the coefficient was set): moving 1 pp of tasks a year at fixed technology needs net
    investment Vm dK/dx x 0.01 / income (central difference, step 1e-6)."""
    q = m.solve(e_b)
    x, hstep = q["x"], 1e-6
    dKdx = (m._parts(e_b, x + hstep)["K"] - m._parts(e_b, x - hstep)["K"]) / (2 * hstep)
    per_pp = q["Vm"] * dKdx * 0.01 / q["income"] * 100
    return {"net_investment_pct_income_per_pp_tasks_a_year": per_pp, "alpha_inv": alpha_capex / per_pp}


def alpha_inv_is(d: Demand) -> float:
    """The demand layer's scale: a held demand level L (% of capacity) is closed by a real rate L (1 - a1) / a_r higher."""
    return (1.0 - d.a1) / d.a_r


def r_star_invest_keyed(mp: dict, e, br, alpha_inv: float) -> np.ndarray:
    """r* with the capex channel keyed to investment spending: r* - capex_term + alpha_inv (inv/income - its start) (pp).
    A readout: the required return and every other series of the path are left as the macro block solved them."""
    inv = investment_income(mp, e)
    return mp["r_star"] - capex_term(mp, br) + alpha_inv * (inv - inv[0])


def r_star_pace_keyed(mp: dict, e, br, alpha_capex: float) -> np.ndarray:
    """r* with the capex channel keyed to the pace of tasks moving: r* - capex_term + alpha_capex x the pace (pp). A readout:
    the required return and every other series of the path are left as the macro block solved them."""
    return mp["r_star"] - capex_term(mp, br) + alpha_capex * pace(mp, br)


def crash(t: np.ndarray, at: float = 0.5, size: float = 4.0, quarters: int = 3) -> np.ndarray:
    """A demand shock of `size` % of capacity, spread evenly over `quarters` quarters from year `at` (Sweden's GDP
    fell about 5% in 2009; the gap's persistence carries it forward)."""
    s = np.zeros(len(t))
    k0 = int(np.searchsorted(t, at))
    s[k0:k0 + quarters] = -size / quarters
    return s


YEARS = (0, 3, 5, 6, 8, 10, 12, 15)
CENTRAL = "central (r* learned with a 3-year half-life)"
def readout_worlds(scen: dict) -> dict:
    return {"default bridges (the macro block's own r*)": ({}, "new"), "deficits dominate": scen["deficits dominate"][:2],
            "owners' saving dominates": scen["owners' saving dominates"][:2]}


def neutral_rate_readout(e, base: Demand, alphas: dict | None, which: str = "lo") -> dict:
    """Per automated world (medium and fast): investment / income, r* as the bridge sets it and with its capex channel on the
    other key — on the refit ('lo', 'hi': keyed to investment) the pace of tasks at alpha_capex 0.25, the key as tuned on (b);
    on the comparator ('b': keyed to the pace) investment spending at each scale in alphas — and the demand layer (base) on
    each r*."""
    bb, scen = bs.base_bridges(which)
    out = {}
    for name, (bridges, truth) in readout_worlds(scen).items():
        for fast in (False, True):
            mp = world(bridges, truth, fast=fast, e=e, base=bb)
            br = m.feedback_bridges(e, base=bb, **bridges)
            t = mp["t"]
            at = lambda x: {str(y): float(np.interp(y, t, x)) for y in YEARS}  # noqa: E731
            w = t <= 15.0 + 1e-9
            if br.capex_key == "investment":
                paths = {"investment keyed (the refit)": mp["r_star"],
                         "pace keyed (as tuned on (b))": r_star_pace_keyed(mp, e, br, br.alpha_capex)}
            else:
                paths = {"task keyed (the bridge as set)": mp["r_star"],
                         **{f"investment keyed, {k}": r_star_invest_keyed(mp, e, br, a) for k, a in alphas.items()}}
            net = net_investment_income(mp)
            rec = {"inv_income_pct": at(investment_income(mp, e)), "net_investment_pct_income_diagnostic": at(net),
                   "net_investment_min_and_year_to_15": [float(net[w].min()), float(t[w][np.argmin(net[w])])],
                   ("capex_term_task_keyed_pp" if br.capex_key == "pace" else "capex_term_pp"): at(capex_term(mp, br)),
                   "r_star": {}, "r_star_max_and_year_to_15": {}, "r_star_rise_above_start_to_15_pp": {}, "demand_layer": {}}
            for k, r_ in paths.items():
                rec["r_star"][k] = at(r_)
                i = int(np.argmax(r_[w]))
                rec["r_star_max_and_year_to_15"][k] = [float(r_[w][i]), float(t[w][i])]
                rec["r_star_rise_above_start_to_15_pp"][k] = float(r_[w].max() - r_[0])
                rec["demand_layer"][k] = summary(run(dict(mp, r_star=r_), base))
            out[name + (", fast automation" if fast else "")] = rec
    return out


def main():
    cyc = sweden_cycle()
    base = Demand(kappa=cyc["kappa_per_pp_output_gap"], okun=cyc["okun"])
    e, cal = bs.economy("lo")
    worlds = {name: world(br, truth, e=e) for name, (br, truth) in bs.SCEN.items()}
    out = {"sweden_cycle": cyc, "central": {k: v for k, v in base.__dict__.items()}, "calibration": cal, "scenarios": {}, "runs": {}}
    variants = {CENTRAL: base,
                "fast learning (1 year)": replace(base, h=1.0),
                "slow learning (8 years, pre-2021 anchors)": replace(base, h=8.0),
                "weak anchor (expectations follow inflation)": replace(base, anchor=0.5),
                "no floor (counterfactual)": replace(base, elb=-99.0),
                "steeper IS (a_r 0.15)": replace(base, a_r=0.15),
                "flatter IS (a_r 0.05)": replace(base, a_r=0.05)}
    for name, mp in worlds.items():
        for vname, dm in variants.items():
            r = run(mp, dm)
            out["scenarios"][f"{name} | {vname}"] = summary(r)
            out["runs"][(name, vname)] = r
    # faster automation (the midpoint at year 3 over 2 years)
    for name in ("deficits dominate", "owners' saving dominates"):
        br, truth = bs.SCEN[name]
        mpf = world(br, truth, fast=True, e=e)
        for vname in (CENTRAL, "slow learning (8 years, pre-2021 anchors)", "weak anchor (expectations follow inflation)"):
            r = run(mpf, variants[vname])
            out["scenarios"][f"{name}, fast automation | {vname}"] = summary(r)
            out["runs"][(name + ", fast automation", vname)] = r
    # a 2009-size demand shock (4% of capacity over three quarters, from half a year). What differs between then and
    # now is the room to the floor: 5.25 points in 2008 (policy 4.75%) against 2.25 today (1.75%). Both start at
    # neutral with the floor set that far below it, so only the room differs. Two responses: the textbook rule, and
    # the Riksbank's 2008 strength (it cut 4.5 points in ten months for a gap of about 4-5%: output weight 1.0, less smoothing).
    responses = {"textbook rule": base, "the Riksbank's 2008 strength": replace(base, phi_y=1.0, smooth=0.5)}
    for name in ("status quo", "owners' saving dominates"):
        mp = worlds[name]
        neutral = float(mp["r_star"][0] + mp["pi_star"])
        for room_name, room in (("2008's room (5.25 points)", 5.25), ("today's room (2.25 points)", 2.25)):
            for resp, dm0 in responses.items():
                for anch, a in (("anchored", dm0.anchor), ("weak anchor", 0.5)):
                    dm = replace(dm0, elb=neutral - room, anchor=a)
                    r = run(mp, dm, shock=crash(mp["t"]))
                    key = f"{name} + a 2009-size demand shock, {room_name} | {resp}, {anch}"
                    out["scenarios"][key] = summary(r, horizon=6.0)
                    out["runs"][(name + " + shock, " + room_name, resp + ", " + anch)] = r
    # the high root (the sensitivity) and (b) (the comparator), central learning: the three worlds and fast automation
    for which, key in (("hi", "sensitivity: the high root"), ("b", "comparator: calibration (b)")):
        e2, cal2 = bs.economy(which)
        bb, scen = bs.base_bridges(which)
        sc = {}
        for name, (br, truth) in scen.items():
            sc[f"{name} | {CENTRAL}"] = summary(run(world(br, truth, e=e2, base=bb), base))
        for name in ("deficits dominate", "owners' saving dominates"):
            br, truth = scen[name]
            sc[f"{name}, fast automation | {CENTRAL}"] = summary(run(world(br, truth, fast=True, e=e2, base=bb), base))
        out[key] = {"calibration": cal2, "scenarios": sc}
    # the neutral rate with the capex channel on the other key (a readout, not the default): on the central, the pace of tasks
    # (the key as tuned on (b)); on the comparator (b), investment spending at two scales (as before the refit)
    eb, _ = bs.economy("b")
    ab = alpha_inv_bridge(eb)
    alphas = {"bridge scale": ab["alpha_inv"], "demand-layer scale": alpha_inv_is(Demand())}
    out["neutral_rate_rekeyed"] = {
        "note": "a readout, not the default: r* with its capex term on the other key; the macro path, and so the required return, "
                "is unchanged; the demand layer (the central variant) is run on each r*. On the central (the refit, keyed to "
                "replacement investment / income, alpha_inv = macro.NEUTRAL_SCALE) the term is replaced by alpha_capex 0.25 x the "
                "pace of tasks moving (the key as tuned on (b)). On the comparator (b) (keyed to the pace) by alpha_inv x the change "
                "in investment / income at two scales: the bridge's (alpha_capex converted at (b)'s start) and the demand layer's "
                "((1 - a1)/a_r of the IS curve). The series keyed to is replacement investment, the only investment in the "
                "quasi-static accounts; net investment (Vm dK/dt / income) is a diagnostic only: the machine stock falls on every "
                "deep path, (b) included, so keying to it would lower r* further.",
        "alpha_inv": {"central (c)": m.Bridges().alpha_inv, "bridge scale": ab,
                      "demand-layer scale": {"alpha_inv": alphas["demand-layer scale"], "a1": Demand().a1, "a_r": Demand().a_r}},
        "central (c)": neutral_rate_readout(e, base, None, "lo"),
        "comparator: calibration (b)": neutral_rate_readout(eb, base, alphas, "b")}
    runs = out.pop("runs")
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    with open(os.path.join(ROOT, "results", "demand.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
    print(json.dumps(cyc, indent=1))
    for k, v in out["scenarios"].items():
        print(f"{k:80s} gap min {v['gap_min_and_year']} max {v['gap_max_and_year']} infl {v['inflation_min_max']} u+ {v['unemployment_up_max']} floor {v['years_at_floor']}y from {v['first_year_at_floor']}")
    for which in ("sensitivity: the high root", "comparator: calibration (b)"):
        for k, v in out[which]["scenarios"].items():
            print(f"[{which[:14]}] {k:66s} gap min {v['gap_min_and_year']} max {v['gap_max_and_year']} infl {v['inflation_min_max']} floor {v['years_at_floor']}y")
    for cal_, rd in ((k, out["neutral_rate_rekeyed"][k]) for k in ("central (c)", "comparator: calibration (b)")):
        for wn, rec in rd.items():
            print(f"[r* readout, {cal_[:14]}] {wn:58s} inv/income {[round(rec['inv_income_pct'][str(y)], 1) for y in YEARS]}"
                  f" net (diagnostic) {[round(rec['net_investment_pct_income_diagnostic'][str(y)], 1) for y in YEARS]}")
            for k, v in rec["r_star"].items():
                g = rec["demand_layer"][k]
                print(f"      {k:40s} r* {[round(v[str(y)], 2) for y in YEARS]} max {[round(x, 2) for x in rec['r_star_max_and_year_to_15'][k]]}"
                      f" | gap {g['gap_min_and_year']} {g['gap_max_and_year']} infl {g['inflation_min_max']} floor {g['years_at_floor']}y")
    alt = {name: r_star_pace_keyed(worlds[name], e, m.feedback_bridges(e, **bs.SCEN[name][0]), m.Bridges().alpha_capex)
           for name in ("deficits dominate", "owners' saving dominates")}
    figure(runs, alt)


def figure(runs, alt=None):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams["axes.titlesize"] = 10
    fig, ax = plt.subplots(2, 3, figsize=(16, 8.6), layout="constrained")
    fig.get_layout_engine().set(rect=(0, 0.03, 1, 0.97))
    C = "central (r* learned with a 3-year half-life)"
    for row, name in enumerate(("deficits dominate", "owners' saving dominates")):
        r = runs[(name, C)]
        t = r["t"]
        w = t <= 15
        a = ax[row, 0]
        a.plot(t[w], r["r_star"][w], color="k", lw=1.6, label="r*, the true neutral real rate")
        a.plot(t[w], r["r_star_cb"][w], color="k", lw=1.2, ls="--", label="the central bank's estimate of r*")
        a.plot(t[w], r["real_rate"][w], color="C3", lw=1.6, label="the real policy rate")
        a.plot(t[w], r["policy"][w], color="C0", lw=1.2, label="the policy rate")
        if alt is not None:
            a.plot(t[w], alt[name][w], color="grey", lw=1.2, ls=":", label="r* with the capex channel keyed to the pace of tasks\n(a readout; the key as tuned on (b))")
        a.axhline(-0.5, color="grey", lw=0.8, ls=":")
        a.set_title(f"{name}: rates, %\nthe gap between the red and black lines drives demand")
        y0, y1 = a.get_ylim()
        a.set_ylim(y0, y1 + 0.5 * (y1 - y0))   # headroom above the rates for the legend
        a.legend(fontsize=7.5, loc="upper right")
        a = ax[row, 1]
        for vn, st in ((C, "-"), ("slow learning (8 years, pre-2021 anchors)", "--"), ("fast learning (1 year)", ":")):
            rv = runs[(name, vn)]
            a.plot(t[w], rv["gap"][w], color="C2", ls=st, label="output gap, " + vn.split(" (")[0])
        a.axhline(0, color="grey", lw=0.8)
        a.set_title(f"{name}: output against capacity, %\nhow fast the central bank learns r* sets the size"); a.legend(fontsize=7.5)
        a = ax[row, 2]
        a.plot(t[w], r["inflation"][w], color="k", lw=1.8, label="headline")
        a.plot(t[w], r["pi_goods"][w], color="C0", lw=1.2, label="goods")
        a.plot(t[w], r["pi_shelter"][w], color="C3", lw=1.2, label="housing and land")
        a.plot(t[w], r["pi_wage"][w], color="C1", lw=1.2, label="wages (money terms)")
        a.axhline(2.0, color="grey", lw=0.8, ls=":")
        a.set_title(f"{name}: inflation, % a year\nthe average hides the split"); a.legend(fontsize=7.5)
        lo_ = min(float(np.min(r[k][w])) for k in ("pi_goods", "pi_shelter", "pi_wage"))
        hi_ = max(float(np.max(r[k][w])) for k in ("pi_goods", "pi_shelter", "pi_wage"))
        a.set_ylim(min(-25.0, 5.0 * np.floor(lo_ / 5.0) - 2.0), max(35.0, 5.0 * np.ceil(hi_ / 5.0) + 2.0))   # the whole split in view
    for a in ax.flat:
        a.set_xlabel("years")
    fig.text(0.01, 0.005, "The macro block's worlds on calibration (c), the central (open reading, low root), with the bridges refit on (c) (Log 46) in bank_scenarios.py's two branches and the demand layer (demand.py). "
             "Okun and Phillips measured on Swedish data 2001-2026 (Statistics Sweden); IS slope from the literature.", fontsize=7.5)
    os.makedirs(os.path.join(ROOT, "figures"), exist_ok=True)
    fig.savefig(os.path.join(ROOT, "figures", "fig_demand.png"), dpi=130)


if __name__ == "__main__":
    main()
