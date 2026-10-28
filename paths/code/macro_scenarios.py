# macro_scenarios.py — the macro block run through to curves: deep automation at three speeds, and capital's part.
#
# CALIBRATION (her decision, 2026-09-30). The deep-automation scenarios run on calibration (c)'s central economy,
# macro.central() — the open (domp) reading, the low root in k: the machine chain at BEA's measured labour content (theta_V
# 0.470, chain share 0.151, sigma_V 0.330, depreciation 0.052; the return rho 0.0755 an outcome) with her four targets
# (labour 0.47 on the paper's Figure 7 basis, employment 0.60, 3 baskets per person, site 13% of the basket; g0 0.01). The
# pre-switch runs are kept by name, for old against new: (a), the flow benchmark (macro.calibrate()), which the three speeds
# used, and (b), produced capital (macro.calibrate(base=CAPITAL_BASE)), which capital's part used — each bit-identical to
# its pre-switch run, since the helpers give the old hard-coded TechPath(0.04, 0.01, ...) and Bridges(capital_premium=5.0)
# exactly. (b) also runs at the three speeds; (c)'s high root in k is the sensitivity.
#
# THE SCENARIOS (main). A technology path takes capability eta from 1 to 0.04 and the labour in a machine-service hour to a
# fifth of its start (macro.deep_tech: 0.05 -> 0.01 in (a)/(b), 10.36 -> 2.07 in (c)'s model units) over 15 years, at the
# three speeds of macro.TECH_SPEEDS: slow (centred year 10, 12 years wide), medium (year 6, 6 wide), fast (year 3, 2 wide).
# The required return is held at the economy's own (no rate feedback, as before). Bridges: the refit on (c) (macro.Bridges();
# Log 46, decisions 72-75, revised in Log 54, decisions 93-96) on the central and its high root; the comparators (a) and (b)
# on the bridges as tuned on (b)
# (macro.BRIDGES_B), so they stay the pre-switch runs. The curves come from macro.curve_path: a stepwise central
# bank, a market learning the destination with a one-year half-life. Labour's share is reported on the basis each
# calibration targets, the paper's Figure 7 object: v n / income in (a)'s flow benchmark, labour_share_bea = v (1 - x) / Ps
# under A.4's capital ((b), (c)); all wages over income (v n / income) beside it.
#
# THE REFIT, BRIDGE BY BRIDGE (refit_steps; the evidence in EVIDENCE and fiscal_start_evidence, stored under "evidence").
# The literature's coefficients are per point of GDP and the model's shifts per point of its income: each is divided once by
# macro.GDP_OVER_INCOME (1.1452; decision 73's units, corrected in Log 54 — until then applied per point of income
# unconverted). The capex channel is keyed to replacement investment / income (delta Vm K / income) at Rachel and Smith's
# coefficient, 0.2 per pp of GDP, times the share of the investment fall that counts as excess saving (the pass-through: 1
# gross, the central; 0 netted against capital consumption; decision 93): 0.175 per pp of income. Owners' saving and
# deficits share one scale, macro.NEUTRAL_SCALE (0.3 pp of r* per pp of GDP of desired saving net of investment, 0.262 per pp
# of income): owners' saving at the scale times the gap between owners' and wage earners' saving rates (0.30); deficits at
# the scale times the share of a primary deficit private saving does not offset (0.6). The fiscal start: the wage tax set so
# the start runs Sweden's 2021-25 mean primary deficit net of property income received (Eurostat, cached in cache/fiscal/;
# 2.06% of income; decision 95: the model's government has gross debt and no assets); with the state's asset income in revenue
# it is 0.16 (the alternative). The debt's rate is floored at the policy floor (decision 75 corrected), and on feedback paths
# the bridges read at the start's required return (decision 96). refit_steps applies them one at a time on the central: steps
# 0-4 the refit as first run (Log 46), steps 5-9 its revision (Log 54). The readout r_star_capex_on_pace keys the capex
# channel back to the pace of tasks moving (alpha_capex 0.25, as tuned on (b)); on the comparators the old readout
# r_star_capex_on_investment stays, at the two scales demand.py and bank_scenarios.py used (the bridge's 0.039, the demand
# layer's 0.6). sensitivity_fiscal_start: the refit with the wage tax at 0.40 as tuned on (b) (a surplus start);
# sensitivity_investment_pass_through: the investment key at the pass-through's three readings (1 / 0.4 / 0).
#
# CAPITAL (capital(); results/capital_feedback.json, figures/fig_capital_feedback.png). Along the medium path on the central:
# the income split (labour, the housing site, the machine chains' land — under the open reading including the chain's
# imported content, which it models as land — and interest), a sustained +200 bp on the required return, and the loop (the
# return following r* against a fixed return), with (b) as the comparator. No dial here moves the required return beyond
# +200 bp; each run's largest rise in it is stored against the central's rate headroom (7.18 pp), and a date with no
# land-scarce equilibrium is recorded — the error, the years the run solves (its longest solved prefix,
# calibration_c.path_prefix) and the first failing date — not dropped. The loop's lag phase (automation behind the
# fixed-return path) is stored as its dates and its depth. Since the revision (decision 96) the refit's bridges read at the
# start's required return, so r* along the loop is the fixed-return r* and the loop runs one way, from r* through the
# required return to automation; loop_bridges_at_path stores the same path with the bridges read along it (as the
# comparators read them), against it. Labour's share in capital_feedback.json is all wages over income (solve's labor_share)
# unless a key says _bea (the Figure 7 basis); the +200 bp readout gives both.
#
# Provenance: the central economy from results/calibration_c.json (BEA; code/calibration_c.py, gated by
# checks/check_calibration_c.py); the fiscal start from Eurostat (gov_10a_main: B9, D41PAY, D4REC; gov_10dd_edpt1), cached in
# cache/fiscal/eurostat_gov.json and fetched again only with --refresh-fiscal. Gated by checks/check_macro_scenarios.py;
# checks/check_macro.py gates (a) and (b) themselves and is unchanged.
# Run from paths/:  ../venv/Scripts/python.exe code/macro_scenarios.py [--refresh-fiscal]
# Out: results/macro_scenarios.json, figures/fig_macro_scenarios.png, results/capital_feedback.json,
#      figures/fig_capital_feedback.png

from __future__ import annotations

import json
import os
import sys
from dataclasses import replace

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import curve as cv  # noqa: E402
import macro as m  # noqa: E402
import sovereign as sv  # noqa: E402

SPEEDS = m.TECH_SPEEDS
T = np.array([1 / 12, 0.25, 0.5, 1, 2, 3, 5, 7, 10, 20, 30])
DATES = (0.0, 3.0, 6.0, 10.0, 15.0)
ALPHA_UNCONVERTED = 0.25         # alpha_capex's number, the first switch report's coefficient: kept only to say where it lies
NL = chr(10)
LABELS = {"c": "calibration (c), central: the open (domp) reading, low root in k",
          "c_hi": "calibration (c), high root in k: the sensitivity",
          "b": "calibration (b): produced capital at a 5.75% return, 8% depreciation (the pre-switch capital runs)",
          "a": "calibration (a): the flow benchmark (the pre-switch three speeds)"}


def economy(name: str):
    """(Economy, record) for 'c' (the central), 'c_hi' (its high root), 'b' or 'a' (the pre-switch comparators)."""
    if name in ("c", "c_hi"):
        e, info = m.central("hi" if name == "c_hi" else "lo")
        rec = {k: info[k] for k in ("tag", "root", "rho", "capital_premium", "multiplier", "headroom_pp", "k", "x", "x_ceiling",
                                    "theta_V", "sigma_V", "chain_share", "source")}
    elif name in ("b", "a"):
        e, _, _, _ = m.calibrate(base=m.CAPITAL_BASE if name == "b" else m.CALIBRATION_BASE)
        rec = {"tag": name, "rho": e.rho, "capital_premium": m.capital_premium(e) if name == "b" else None, "k": e.k,
               "source": "macro.calibrate(base=macro.CAPITAL_BASE)" if name == "b" else "macro.calibrate()"}
    else:
        raise ValueError(f"economy {name!r}: one of {tuple(LABELS)}")
    return e, rec


def flow(e: m.Economy) -> bool:
    return e.rho == 0.0 and e.delta == 1.0


def fig7(e: m.Economy, mp: dict):
    """Labour's share on the basis the calibration targets (the paper's Figure 7 object)."""
    return mp["labor_share"] if flow(e) else mp["labour_share_bea"]


def investment_income(e: m.Economy, mp: dict):
    """Replacement investment at current cost over income, delta Vm K / income (solve's inv_income)."""
    return e.delta * mp["Vm"] * mp["K"] / mp["income"]


def invest_scales() -> dict:
    """The two scales of the investment-keyed readout, from demand.py (the one source; demand and bank use the same):
    {"bridge scale": alpha_capex converted at (b)'s start, "demand-layer scale": (1 - a1)/a_r}."""
    import demand as dmd             # local: demand imports bank_scenarios and the data layers, which this module does not need
    eb, _, _, _ = m.calibrate(base=m.CAPITAL_BASE)
    return {"bridge scale": float(dmd.alpha_inv_bridge(eb)["alpha_inv"]), "demand-layer scale": float(dmd.alpha_inv_is(dmd.Demand()))}


def r_star_capex_on_investment(e: m.Economy, mp: dict, alpha_invest: float, br: m.Bridges = m.BRIDGES_B):
    """The neutral rate with the capex channel keyed to investment spending — alpha_invest pp of r* per pp change in
    investment / income from the start — in place of the pace of tasks moving; the owners' and fiscal channels as
    macro_path's (fixed-return paths). The readout of a path keyed to the pace (the comparators')."""
    inv = investment_income(e, mp) * 100
    return (br.r0_star + alpha_invest * (inv - inv[0]) - br.alpha_rent * (mp["nonwage_share"] - mp["nonwage_share"][0])
            + br.alpha_fiscal * (mp["deficit"] - mp["deficit"][0]))


def r_star_capex_on_pace(e: m.Economy, mp: dict, br: m.Bridges, alpha_capex: float | None = None):
    """The neutral rate of an investment-keyed path with its capex channel keyed to the pace of tasks moving instead —
    alpha_capex (default br's, 0.25: the key as tuned on (b)) pp of r* per pp of tasks a year — the owners' and fiscal
    channels as macro_path's: r* less the capex term the bridge added, plus alpha_capex x the pace the pace key would use
    (macro_path's r_star_capex and pace_key). The readout of a path keyed to investment (the central's)."""
    a = br.alpha_capex if alpha_capex is None else alpha_capex
    return mp["r_star"] - mp["r_star_capex"] + a * mp["pace_key"]


# ------------------------------------------------------------------ the evidence behind the refit bridges (Log 46)
FISCAL_CACHE = os.path.join(ROOT, "cache", "fiscal", "eurostat_gov.json")
ES_API = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/"
FISCAL_GEOS = ("SE", "EA20", "FR", "DE")
FISCAL_YEARS = ("2021", "2022", "2023", "2024", "2025")     # the start's primary balance: the mean of the last five years


def _eurostat_table(ds: str, params: list) -> tuple[dict, str]:
    """{(geo, na_item, year): value} and the dataset's update stamp, from Eurostat's JSON API."""
    import requests
    import truststore
    truststore.inject_into_ssl()
    r = requests.get(ES_API + ds, params=[("format", "JSON")] + params,
                     headers={"User-Agent": "laborformal-paths (public-data research)"}, timeout=60)
    r.raise_for_status()
    js = r.json()
    ids, size = js["id"], js["size"]
    cats = {d: {v: k for k, v in js["dimension"][d]["category"]["index"].items()} for d in ids}
    strides = [int(np.prod(size[i + 1:])) for i in range(len(ids))]
    out = {}
    for k, v in js["value"].items():
        key = {d: cats[d][(int(k) // strides[i]) % size[i]] for i, d in enumerate(ids)}
        out[f"{key['geo']}|{key['na_item']}|{key['time']}"] = float(v)
    return out, js.get("updated")


def fiscal_data(refresh: bool = False) -> dict:
    """General government (S13), % of GDP, 2015 on: net lending B9, interest payable D41PAY and property income received D4REC
    (gov_10a_main), gross debt GD (gov_10dd_edpt1), for Sweden, the euro area, France and Germany; cached in cache/fiscal/
    (fetched only with refresh)."""
    if refresh or not os.path.exists(FISCAL_CACHE):
        geo = [("geo", g) for g in FISCAL_GEOS]
        a, ua = _eurostat_table("gov_10a_main", [("unit", "PC_GDP"), ("sector", "S13"), ("na_item", "B9"), ("na_item", "D41PAY"),
                                                 ("na_item", "D4REC"), *geo, ("sinceTimePeriod", "2015")])
        d, ud = _eurostat_table("gov_10dd_edpt1", [("unit", "PC_GDP"), ("sector", "S13"), ("na_item", "GD"), *geo,
                                                   ("sinceTimePeriod", "2015")])
        os.makedirs(os.path.dirname(FISCAL_CACHE), exist_ok=True)
        with open(FISCAL_CACHE, "w", encoding="utf-8") as f:
            json.dump({"source": "Eurostat: gov_10a_main (B9, D41PAY, D4REC) and gov_10dd_edpt1 (GD), S13, PC_GDP",
                       "url": ES_API + "{gov_10a_main, gov_10dd_edpt1}", "updated": {"gov_10a_main": ua, "gov_10dd_edpt1": ud},
                       "values": {**a, **d}}, f, indent=1, sort_keys=True)
    with open(FISCAL_CACHE, encoding="utf-8") as f:
        return json.load(f)


def fiscal_start_evidence(e: m.Economy) -> dict:
    """The start's primary deficit (decision 95, her call of 2026-10-28: "No assets"): Sweden's general government primary deficit
    net of property income received, -(B9 + D41PAY - D4REC), % of GDP, its mean over FISCAL_YEARS, converted to % of the model's
    income (GDP net of the chain's imported content over income, from results/calibration_c.json's central). The model's government
    has gross debt and no assets, so the state's income from its assets is not revenue at the start. Beside it the same measure with
    that income in revenue, -(B9 + D41PAY) (the refit's first start, Log 46: the alternative), and the debt the model starts at
    against Sweden's (debt0 kept at 40)."""
    fd = fiscal_data()
    v = fd["values"]
    prim = {g: {y: round(-(v[f"{g}|B9|{y}"] + v[f"{g}|D41PAY|{y}"] - v[f"{g}|D4REC|{y}"]), 2) + 0.0 for y in FISCAL_YEARS}
            for g in FISCAL_GEOS}
    prim_a = {g: {y: round(-(v[f"{g}|B9|{y}"] + v[f"{g}|D41PAY|{y}"]), 2) + 0.0 for y in FISCAL_YEARS} for g in FISCAL_GEOS}
    d4 = {g: {y: v[f"{g}|D4REC|{y}"] for y in FISCAL_YEARS} for g in FISCAL_GEOS}
    debt = {g: {y: v[f"{g}|GD|{y}"] for y in FISCAL_YEARS} for g in FISCAL_GEOS}
    with open(m.CENTRAL_SOURCE, encoding="utf-8") as f:
        cal = json.load(f)["calibrations"][m.central()[1]["tag"]]
    gdp_over_income = cal["labor_share"] / cal["comp_gdp_net"]
    mean_se = float(np.mean(list(prim["SE"].values())))
    mean_se_a = float(np.mean(list(prim_a["SE"].values())))
    return {"primary_deficit_pct_gdp": prim, "primary_deficit_with_asset_income_pct_gdp": prim_a,
            "property_income_received_pct_gdp": d4, "gross_debt_pct_gdp": debt, "updated": fd["updated"],
            "sweden_mean_pct_gdp": round(mean_se, 3), "gdp_over_income": round(gdp_over_income, 4),
            "sweden_mean_pct_income": round(mean_se * gdp_over_income, 2), "start_deficit_default": m.START_DEFICIT,
            "sweden_mean_with_asset_income_pct_gdp": round(mean_se_a, 3),
            "sweden_mean_with_asset_income_pct_income": round(mean_se_a * gdp_over_income, 2),
            "start_deficit_alternative": m.START_DEFICIT_ASSET_INCOME,
            "sweden_latest_pct_income": round(prim["SE"][FISCAL_YEARS[-1]] * gdp_over_income, 2),
            "sweden_debt_latest_pct_income": round(debt["SE"][FISCAL_YEARS[-1]] * gdp_over_income, 1),
            "debt0_default": m.Bridges().debt0,
            "note": "the model's deficit is primary and net of property income received (decision 95): interest paid enters debt "
                    "through r* + pi* - growth, and the model's government has gross debt and no assets, so it receives none; the "
                    "alternative (start_deficit_alternative) keeps the state's asset income in revenue. In % of income (GDP net of "
                    "the chain's imported content and of replacement investment); the start is an equilibrium at capacity, so the "
                    "five-year mean stands in for a structural balance (2022's surplus and 2023-25's slowdown both in it)"}


REFIT_STEPS = ("0 as tuned on (b)", "1 the capex key on investment", "2 owners' saving", "3 deficits", "4 the fiscal start",
               "5 the investment key at Rachel and Smith's coefficient", "6 the scale per point of income",
               "7 the fiscal start with no assets", "8 the debt's rate at the lower bound",
               "9 the bridges at the start's required return")


def refit_bridges(step: int) -> m.Bridges:
    """The bridges after the refit's first `step` steps, in the order of the refit (Log 46) and its revision (Log 54): 0 the
    bridges as tuned on (b); 1 the capex key on replacement investment at the common scale; 2 owners' saving at the scale times
    the saving gap; 3 deficits at the scale times the pass-through; 4 the fiscal start at the measured primary deficit — the
    refit as first run (Log 46), each evidence number per point of GDP applied per point of income unconverted, as it then was;
    5 the investment key at Rachel and Smith's coefficient (decision 93), still unconverted; 6 the scale per point of income: all
    three coefficients divided by macro.GDP_OVER_INCOME (decision 73's units corrected), set to macro.Bridges()'s own floats;
    7 the fiscal start with no assets: the primary deficit net of property income received (decision 95); 8 the debt's rate
    floored at the policy floor, macro.ELB (decision 75 corrected); 9 on feedback paths the bridges read at the start's required
    return (decision 96) — on the fixed-return table identical to step 8; step 9 is macro.Bridges()."""
    br = m.BRIDGES_B
    if step >= 1:
        br = replace(br, capex_key="investment", alpha_inv=m.NEUTRAL_SCALE_GDP)             # 0.3, as first run
    if step >= 2:
        br = replace(br, alpha_rent=m.NEUTRAL_SCALE_GDP * m.OWNERS_SAVING_GAP)
    if step >= 3:
        br = replace(br, alpha_fiscal=m.NEUTRAL_SCALE_GDP * m.DEFICIT_PASS_THROUGH)
    if step >= 4:
        br = replace(br, tau_w=None, deficit0=m.START_DEFICIT_ASSET_INCOME)                 # 0.16: Log 46's start
    if step >= 5:
        br = replace(br, alpha_inv=m.INVESTMENT_KEY_GDP * m.INVESTMENT_PASS_THROUGH)          # 0.2, unconverted
    if step >= 6:
        b0 = m.Bridges()                     # Bridges()'s own floats, so the last step equals the refit exactly
        br = replace(br, alpha_inv=b0.alpha_inv, alpha_rent=b0.alpha_rent, alpha_fiscal=b0.alpha_fiscal)
    if step >= 7:
        br = replace(br, deficit0=m.START_DEFICIT)                                          # 2.06: no assets
    if step >= 8:
        br = replace(br, debt_rate_floor=m.ELB)
    if step >= 9:
        br = replace(br, bridges_at="start")
    return br


def refit_steps(e: m.Economy) -> dict:
    """Each step of the refit on the central, at the three speeds (fixed return): r* at the start, its peak and year 15, the
    year of its peak, policy's low point, debt at year 15 and its low point — one bridge at a time."""
    out = {}
    for j, name in enumerate(REFIT_STEPS):
        br = refit_bridges(j)
        rec = {}
        for k, kw in SPEEDS.items():
            mp = m.macro_path(e, m.deep_tech(e, **kw), br)
            _, _, pol = m.curve_path(mp)
            r, d, t = mp["r_star"], mp["debt"], mp["t"]
            rec[k] = {"r_star_start_peak_end": [round(float(r[0]), 2), round(float(r.max()), 2), round(float(r[-1]), 2)],
                      "r_star_peak_year": float(t[int(np.argmax(r))]), "policy_min": round(float(pol.min()), 2),
                      "debt_low_and_year15": [round(float(d.min()), 1), round(float(d[-1]), 1)],
                      "deficit_start_end": [round(float(mp["deficit"][0]), 2), round(float(mp["deficit"][-1]), 2)]}
        out[name] = rec
    return out


def evidence() -> dict:
    """The refit's evidence, bridge by bridge (Log 46; decisions 72-75, revised in Log 54; decisions 93-96): the literature's
    numbers behind each coefficient (EVIDENCE), the units they are applied in, and the measured fiscal start."""
    return {"bridges": {"neutral_scale": m.NEUTRAL_SCALE, "neutral_scale_range": list(m.NEUTRAL_SCALE_RANGE),
                        "owners_saving_gap": m.OWNERS_SAVING_GAP, "owners_saving_gap_range": list(m.OWNERS_SAVING_GAP_RANGE),
                        "deficit_pass_through": m.DEFICIT_PASS_THROUGH,
                        "deficit_pass_through_range": list(m.DEFICIT_PASS_THROUGH_RANGE),
                        "alpha_inv": m.Bridges().alpha_inv, "alpha_rent": m.Bridges().alpha_rent,
                        "alpha_fiscal": m.Bridges().alpha_fiscal, "branches": m.BRANCHES},
            "units": {"note": "the literature's coefficients are per point of GDP; the model applies them per point of its income, "
                              "divided once by gdp_over_income (decision 73's units, corrected in Log 54: until then the GDP numbers "
                              "were applied per point of income unconverted). Not converted: tp_per_debt, debt_threshold, "
                              "loss_per_debt (illustrative, per point of income since the macro block's first commit, never sourced)",
                      "gdp_over_income": m.GDP_OVER_INCOME, "scale_gdp": m.NEUTRAL_SCALE_GDP,
                      "scale_gdp_range": list(m.NEUTRAL_SCALE_GDP_RANGE), "scale_income": m.NEUTRAL_SCALE,
                      "scale_income_range": list(m.NEUTRAL_SCALE_RANGE), "investment_key_gdp": m.INVESTMENT_KEY_GDP,
                      "investment_pass_through": m.INVESTMENT_PASS_THROUGH,
                      "investment_pass_through_range": list(m.INVESTMENT_PASS_THROUGH_RANGE), "investment_key_income": m.INVESTMENT_KEY},
            "literature": EVIDENCE, "fiscal_start": fiscal_start_evidence(m.central()[0])}


EVIDENCE = {   # the published numbers behind macro.NEUTRAL_SCALE, OWNERS_SAVING_GAP and DEFICIT_PASS_THROUGH (Log 46), as read
    "neutral_scale": {
        "Rachel and Smith (2015), BoE Staff WP 571, Box D1 and pp. 34-48":
            "saving elasticity 0.5, investment -0.7 (-0.5 adjusted for the relative price of capital), calibrated: a 1 pp of GDP "
            "saving shift ~25 bp, 4 pp ~90 bp; a 4 pp fall in investment ~80 bp; A ~0.20-0.25",
        "Rachel and Summers (2019), NBER WP 26198 / BPEA, s. 3.3":
            "1 pp lower r widens the saving-investment gap by 2-4 pp of GDP (central 3): A ~0.33 (0.25-0.5)",
        "Holston, Laubach and Williams (2017), JIE 108, Table 1":
            "US IS curve a_y 0.942, a_r -0.071: (1 - a_y)/|a_r| 0.82 in output-gap units (multipliers included): an upper bound",
        "Eggertsson, Mehrotra and Robbins (2019), AEJ:Macro 11(1), Table 6":
            "a labour-share fall 72.4 -> 66.0% lowers r 0.52 pp (~8 bp per pp: compare alpha_rent); debt +76 pp of GDP raises r 2.11 pp"},
    "owners_saving_gap": {
        "Onaran and Galanis (2012), ILO, Table 3": "C/Y per +1 pp of profit share: US -0.43, euro area -0.44, France -0.31, Germany -0.50",
        "Hein and Vogel (2008), CJE 32(3)": "US -0.14, France -0.35, Germany -0.32",
        "Onaran and Obst (2016), CJE 40(6), Table 7": "Sweden -0.39, Finland -0.24, Denmark -0.16",
        "Stockhammer and Wildauer (2016), CJE 40(6), Table 5": "+1 pp wage share raises C 0.12 pp of GDP (household debt, property prices held)",
        "Mian, Straub and Sufi (2021), Jackson Hole, Table 1":
            "saving rates top 10% 25.3%, next 40% 8.2%, bottom 50% 2.6%; the top 10%'s income share +11.8 pp raised saving 2.4 pp of "
            "national income: ~0.20 per unit shifted (average group rates)",
        "Mian, Straub and Sufi (2025), NBER WP 26941":
            "top 1% saving rate over 40% of disposable income (retained earnings attributed; by wealth group), bottom 50% ~0",
        "Dynan, Skinner and Zeldes (2004), JPE 112(2), Fig. 3 and Table 9":
            "marginal saving between income quintiles 0.03-0.43: cross-section levels on the change in wealth, capital gains "
            "included, which they flag as biased up at the top; their time-series estimates (MPS Q5 0.25, change in wealth) put "
            "the gap between the top quintile and the bottom three at ~0.16-0.18, which supports the household-only end "
            "(0.15-0.20) rather than 0.30",
        "Fagereng, Holm, Moll and Natvik (2019), NBER WP 26588":
            "net saving rates flat at ~6-8% across wealth (retained earnings in capital gains, outside net saving): the household-only "
            "basis gives a smaller gap",
        "Di Maggio, Kermani and Majlesi (2020), JF 75(6), Table III": "Swedish MPC out of dividends 0.40-0.60; out of capital gains ~0.03 at the top",
        "basis": "the non-wage share includes all owners' income, retained earnings included: the gap on that basis 0.30 (0.15-0.45); "
                 "household-only 0.15-0.20; all local estimates, applied here to a ~50 pp shift. The horizon as well as the size: the "
                 "Kaleckian C/Y estimates above (Onaran and Galanis, Hein and Vogel, Onaran and Obst, Stockhammer and Wildauer) are "
                 "short-run first-difference responses, one on gross profits, whose authors found no long-run level relation; the "
                 "long-run evidence is mixed — Mian, Straub and Sufi 2021 (~0.20) and Dynan, Skinner and Zeldes's time-series gap "
                 "(~0.16-0.18) point lower, Mian, Straub and Sufi 2025's top-1% saving rates higher (corrected in Log 54, "
                 "evidence:A5-A6)"},
    "deficit_pass_through": {
        "Gale and Orszag (2004), BPEA 2004:2, pp. 102-103, 147":
            "$1 of deficit cuts national saving 50-80 cents (offset 0.2-0.5); a projected primary deficit raises long rates 40-70 bp per pp",
        "Röhn (2010), OECD ECO WP 762":
            "private saving offsets ~40% of a change in the budget balance on average; changes in current revenues almost fully, "
            "changes in current spending one third to one half; the offset is stronger the higher the government's debt",
        "de Mello, Kongsrud and Price (2004), OECD ECO WP 397": "offset one-third to one-half",
        "Laubach (2009), JEEA 7(4)": "~25 bp per pp of projected deficit / GDP, 3-4 bp per pp of debt, on 5-year-ahead long nominal rates",
        "Rachel and Summers (2019), Table 2": "literature averages 38 bp per pp of deficit, 3.5 bp per pp of debt",
        "note": "the common scale gives alpha_fiscal = 0.3 x 0.6 = 0.18 pp of r* per pp of GDP of primary deficit, 0.157 per pp of "
                "income: it rests on the saving-offset evidence alone (Gale and Orszag, Röhn, de Mello et al.: offsets of a fifth to "
                "a half). It lies below every direct long-yield estimate (0.25-0.70 per pp of GDP: Laubach ~25 bp, Rachel and "
                "Summers's average 38, Gale and Orszag 40-70), and the sources do not set those aside for carrying term premia and "
                "expected inflation: Rachel and Summers apply their 38 bp to R* directly (corrected in Log 54, evidence:A3: the note "
                "gave that reason); the direct estimates are decision 74's alternative (0.25-0.5 per pp of GDP). The model's term "
                "premium rises with debt above 60% of income on its own (tp_per_debt 0.02: illustrative defaults since the macro "
                "block's first commit, 24 Sep 2026, per point of income and never sourced; as the 60%-of-GDP reference the threshold "
                "would be ~69% of income, and Laubach's 3-4 bp per pp of debt / GDP is 0.026-0.035 per pp of income, on long nominal "
                "yields), which adds to the long-rate response once debt passes it. Röhn's composition and debt-level results pull "
                "the other way: this model's deficits are mostly revenue lost as the wage tax's base shrinks (at medium the wage tax's "
                "share of revenue falls 0.80 -> 0.11) while debt passes 100% of income, which those results offset more than the "
                "average: a pass-through below 0.6 (evidence:A4). The deficits leg is bounded by two strands pulling opposite ways, "
                "the yield evidence up and the offset evidence down, and pinned by neither. The deficits branch takes no offset at "
                "all (pass-through 1.0: 0.30 per pp of GDP, 0.262 per pp of income): beyond the saving-offset estimates, whose "
                "largest pass-through is 0.8 (Gale and Orszag's 80 cents), it stands on the direct yield evidence only"},
    "investment_key": {   # decision 93 (her call of 2026-10-28: "R&S's own 0.2 + dial"); Log 54
        "Rachel and Smith (2015), BoE Staff WP 571, Box D1":
            "a 4 pp of GDP fall in investment lowers the neutral rate ~80 bp: 0.2 pp of r* per pp of GDP — their short-termism "
            "scenario, an upper bound on what an investment fall alone does; they read gross investment against gross saving",
        "Rachel and Summers (2019), NBER WP 26198 / BPEA": "the saving-investment gap's scale, 1 pp lower r per 2-4 pp of GDP (A ~0.33)",
        "the model's fall": "replacement investment / income falls ~13 points by year 15 at the medium and fast speeds (17.8 -> 4.5 "
                            "and 4.4% of income) and ~7 at the slow (to 10.5%; 8 on the high root), far outside Rachel and Smith's "
                            "4 pp: the coefficient is extrapolated (a linear bridge far beyond its evidence)",
        "pass_through": "how much of the investment fall counts as excess saving: gross 1.0 (Rachel and Smith's reading, the "
                        "central), net for a growing stock ~0.4 (g / delta of replacement), netted against capital consumption 0 "
                        "(the model's income is net of replacement investment). The evidence does not pin it: the central is gross "
                        "and the reverse envelope draws it over 0-1 (macro.INVESTMENT_PASS_THROUGH_RANGE); "
                        "sensitivity_investment_pass_through runs 1 / 0.4 / 0 on the fixed-return table",
        "note": "alpha_inv = macro.INVESTMENT_KEY = 0.2 x the pass-through per point of GDP, 0.175 per point of the model's income at "
                "the central (gross); before the revision (Log 46) the investment key was the common scale, 0.3, applied per point "
                "of income unconverted"}}


def first_year(t, mask):
    idx = np.nonzero(mask)[0]
    return float(t[idx[0]]) if len(idx) else None


def block(e: m.Economy, mp: dict, extras: bool = True, scales: dict | None = None, br: m.Bridges = m.BRIDGES_B):
    """One scenario's outputs: the pre-switch keys (labour_share on the Figure 7 basis, real_wage, participation, r_star,
    policy, debt, the OIS curve and the government spread at DATES) and, if extras, the readouts added at the switch."""
    states, sovs, pol = m.curve_path(mp)
    t = mp["t"]
    at = {d: int(np.argmin(np.abs(t - d))) for d in DATES}
    ls = fig7(e, mp)
    out = {"labour_share": {d: round(float(ls[i]), 3) for d, i in at.items()},
           "real_wage": {d: round(float(mp["real_wage"][i]), 3) for d, i in at.items()},
           "participation": {d: round(float(mp["participation"][i]), 3) for d, i in at.items()},
           "r_star": {d: round(float(mp["r_star"][i]), 2) for d, i in at.items()},
           "policy": {d: round(float(pol[i]), 2) for d, i in at.items()},
           "debt": {d: round(float(mp["debt"][i]), 1) for d, i in at.items()},
           "ois_curve": {d: [round(float(z), 3) for z in cv.zero(T, states[i])] for d, i in at.items()},
           "gov_spread": {d: [round(float(z), 3) for z in sv.spread(T, sovs[i])] for d, i in at.items()}}
    if not extras:
        return out, states, pol
    rw, r = mp["real_wage"], mp["r_star"]
    ip, jr = int(np.argmax(rw)), int(np.argmax(r))
    jg, js = int(np.argmin(mp["pi_goods"])), int(np.argmax(mp["pi_shelter"]))
    out.update({
        "labour_share_basis": "labor_share (v n / income: the flow benchmark)" if flow(e) else "labour_share_bea (v (1 - x) / Ps)",
        "labour_share_all_wages": {d: round(float(mp["labor_share"][i]), 4) for d, i in at.items()},
        "labour_share_halves_year": first_year(t, ls <= 0.5 * ls[0]),
        "real_wage_peak": round(float(rw[ip]), 4), "real_wage_peak_year": float(t[ip]),
        "real_wage_peak_over_start": round(float(rw[ip] / rw[0]), 4), "real_wage_end_over_start": round(float(rw[-1] / rw[0]), 4),
        "pi_goods_min": round(float(mp["pi_goods"][jg]), 2), "pi_goods_min_year": float(t[jg]),
        "pi_shelter_max": round(float(mp["pi_shelter"][js]), 2), "pi_shelter_max_year": float(t[js]),
        "wage_tax_share_start_end": [round(float(mp["wage_tax_share"][0]), 3), round(float(mp["wage_tax_share"][-1]), 3)],
        "deficit_start_end": [round(float(mp["deficit"][0]), 2), round(float(mp["deficit"][-1]), 2)],
        "r_star_start_peak_end": [round(float(r[0]), 2), round(float(r[jr]), 2), round(float(r[-1]), 2)],
        "r_star_peak_year": float(t[jr]),
        "x_start_end": [round(float(mp["x"][0]), 4), round(float(mp["x"][-1]), 4)],
        "x_ceiling_start_end": [round(float(mp["x_ceiling"][0]), 4), round(float(mp["x_ceiling"][-1]), 4)]})
    if flow(e):          # machine services are a within-period intermediate: no investment to key the channel to
        out["r_star_capex_on_investment"] = None
        out["investment_note"] = "not defined in the flow benchmark (delta 1: machine services are a within-period intermediate)"
        return out, states, pol
    inv = investment_income(e, mp)
    jv = int(np.argmax(inv))
    out.update({"investment_income": {d: round(float(inv[i]), 4) for d, i in at.items()},
                "investment_income_peak_and_year": [round(float(inv[jv]), 4), float(t[jv])]})
    if br.capex_key == "investment":     # the central (the refit): the readout is the key as tuned on (b), the pace of tasks
        rp = r_star_capex_on_pace(e, mp, br)
        jp = int(np.argmax(rp))
        out.update({"capex_key": br.capex_key, "tau_w": round(float(mp["tau_w"]), 4),
                    "r_star_capex_on_pace": {d: round(float(rp[i]), 2) for d, i in at.items()},
                    "r_star_capex_on_pace_start_peak_end": [round(float(rp[0]), 2), round(float(rp[jp]), 2), round(float(rp[-1]), 2)],
                    "r_star_capex_on_pace_peak_year": float(t[jp]), "r_star_capex_on_pace_rise_bp": round(float(rp[jp] - rp[0]) * 100, 4),
                    "r_star_capex_on_pace_end_above_investment_keyed_pp": round(float(rp[-1] - r[-1]), 2)})
        return out, states, pol
    out.update({"r_star_capex_on_investment": {}, "r_star_capex_on_investment_start_peak_end": {},
                "r_star_capex_on_investment_peak_year": {}, "r_star_capex_on_investment_rise_bp": {},
                "r_star_capex_on_investment_end_below_pace_keyed_pp": {}})
    for sc, a in (scales or invest_scales()).items():
        ri = r_star_capex_on_investment(e, mp, a, br)
        jri = int(np.argmax(ri))
        out["r_star_capex_on_investment"][sc] = {d: round(float(ri[i]), 2) for d, i in at.items()}
        out["r_star_capex_on_investment_start_peak_end"][sc] = [round(float(ri[0]), 2), round(float(ri[jri]), 2), round(float(ri[-1]), 2)]
        out["r_star_capex_on_investment_peak_year"][sc] = float(t[jri])
        out["r_star_capex_on_investment_rise_bp"][sc] = round(float(ri[jri] - ri[0]) * 100, 4)
        out["r_star_capex_on_investment_end_below_pace_keyed_pp"][sc] = round(float(r[-1] - ri[-1]), 2)
    return out, states, pol


def bridges(name: str) -> m.Bridges:
    """The bridges an economy runs on: the refit (macro.Bridges()) for (c), the bridges as tuned on (b) for the comparators."""
    return m.BRIDGES_B if name in ("a", "b") else m.Bridges()


def speeds(name: str, extras: bool = True, scales: dict | None = None):
    e, rec = economy(name)
    br = bridges(name)
    runs, blocks = {}, {}
    for k, kw in SPEEDS.items():
        mp = m.macro_path(e, m.deep_tech(e, **kw), br)
        blocks[k], mp["_states"], mp["_policy"] = block(e, mp, extras, scales, br)
        runs[k] = mp
    cal = {k: float(getattr(e, k)) for k in ("T", "h", "chi_max", "k", "g0", "g1", "a", "b", "lam", "rho", "delta")}
    return e, rec, cal, runs, blocks


def fiscal_start_sensitivity(e: m.Economy) -> dict:
    """Debt on the central with the wage tax as tuned on (b) (0.40 on all wages: a surplus start), the rest of the refit held,
    at each speed (fixed return): the start the refit replaced (decision 74)."""
    br = replace(m.Bridges(), tau_w=m.BRIDGES_B.tau_w, deficit0=None)
    out = {"note": "the wage tax at 0.40 as tuned on (b) (on all wages, 0.554 of income: a surplus start), the rest of the refit held; "
                   "a sensitivity, not the default (the default starts at the measured primary deficit net of property income "
                   "received, macro.START_DEFICIT: decision 95); fixed return, the three speeds",
           "tau_w": m.BRIDGES_B.tau_w, "tau_w_default": round(float(m.fiscal_start(m.Bridges(), e).tau_w), 4),
           "start_deficit_default_pct": m.Bridges().deficit0, "scenarios": {}}
    for k, kw in SPEEDS.items():
        mp = m.macro_path(e, m.deep_tech(e, **kw), br)
        t = mp["t"]
        out["scenarios"][k] = {"deficit_start_end": [round(float(mp["deficit"][0]), 2), round(float(mp["deficit"][-1]), 2)],
                               "debt": {d: round(float(mp["debt"][int(np.argmin(np.abs(t - d)))]), 1) for d in DATES},
                               "r_star_start_end": [round(float(mp["r_star"][0]), 2), round(float(mp["r_star"][-1]), 2)]}
    return out


PASS_THROUGHS = (1.0, 0.4, 0.0)      # the investment key's three readings: gross (the central), net for a growing stock, netted


def sensitivity_investment_pass_through() -> dict:
    """The refit with the investment key at each of its three readings (decision 93): r* at year 15, its rise above the start
    (pp; positive only if it ever rises) and debt at year 15, on the central and its high root at the three speeds (fixed
    return), everything else held."""
    out = {"note": "alpha_inv = Rachel and Smith's 0.2 per point of GDP times the pass-through of the investment fall, per point "
                   "of income (macro.investment_key): 1 gross (the central), 0.4 net for a growing stock (g / delta), 0 netted "
                   "against capital consumption; the rest of the refit held; fixed return, the three speeds",
           "pass_throughs": list(PASS_THROUGHS)}
    for root in m.CENTRAL_ROOTS:
        e = m.central(root)[0]
        rec = {}
        for pt in PASS_THROUGHS:
            br = replace(m.Bridges(), alpha_inv=m.investment_key(pt))
            row = {"alpha_inv": br.alpha_inv}
            for k, kw in SPEEDS.items():
                mp = m.macro_path(e, m.deep_tech(e, **kw), br)
                r = mp["r_star"]
                row[k] = {"r_star_year15": round(float(r[-1]), 2), "r_star_rise_pp": round(float(r.max() - r[0]), 4),
                          "debt_year15": round(float(mp["debt"][-1]), 1)}
            rec[f"{pt:g}"] = row
        out["central (c)" if root == "lo" else "high root"] = rec
    return out


def results():
    """The scenarios' JSON: the central at the top level (the pre-switch keys), the comparators and the sensitivities beside."""
    scales = invest_scales()
    e, rec, cal, runs, blocks = speeds("c", scales=scales)
    out = {"calibration": cal | {"record": rec, "label": LABELS["c"]}, "scenarios": blocks,
           "labour_share_basis": "scenarios.*.labour_share is the basis each calibration targets: labour_share_bea (the paper's "
                                 "Figure 7 object, v (1 - x) / Ps) on (b) and (c), labor_share (v n / income) on the flow benchmark "
                                 "(a); labour_share_all_wages (v n / income) beside it on every calibration",
           "capex_on_investment": {"alpha_inv": dict(scales), "units": "pp of r* per pp of investment / income",
                                   "source": "demand.alpha_inv_bridge (calibration (b)'s start) and demand.alpha_inv_is (demand.Demand()); "
                                             "the same two scales demand.json and bank.json report",
                                   "unconverted_alpha_capex": ALPHA_UNCONVERTED,
                                   "note": "a sensitivity readout, not a new default: the capex channel keyed to investment / income "
                                           "(delta Vm K / income) in place of the pace of tasks moving; the investment term is linear "
                                           "in the coefficient (alpha_inv x the change in investment / income), so alpha_capex's 0.25 "
                                           "used unconverted (the first switch report) gives 0.25 / alpha_inv times each scale's term, "
                                           "between the two; debt and policy stay on the default r*"}}
    for name in ("a", "b"):
        _, rc_, cal_, _, bl_ = speeds(name, scales=scales)
        out.setdefault("comparators", {})[name] = {"label": LABELS[name], "calibration": cal_ | {"record": rc_}, "scenarios": bl_}
    _, rc_, cal_, _, bl_ = speeds("c_hi", scales=scales)
    out["sensitivity_c_hi"] = {"label": LABELS["c_hi"], "calibration": cal_ | {"record": rc_}, "scenarios": bl_}
    out["sensitivity_fiscal_start"] = fiscal_start_sensitivity(e)
    out["sensitivity_investment_pass_through"] = sensitivity_investment_pass_through()
    out["refit_steps"] = refit_steps(e)
    out["refit_steps_c_hi"] = refit_steps(m.central("hi")[0])
    out["evidence"] = evidence()
    return out, (e, runs)


def main():
    out, (e, runs) = results()
    for name, blocks in (("c", out["scenarios"]), ("a", out["comparators"]["a"]["scenarios"]), ("b", out["comparators"]["b"]["scenarios"]),
                         ("c_hi", out["sensitivity_c_hi"]["scenarios"])):
        for k, b in blocks.items():
            print(f"{name:4s} {k:7s} labour share " + " ".join(f"{v:.2f}" for v in b['labour_share'].values())
                  + " | real wage " + " ".join(f"{v:.2f}" for v in b['real_wage'].values())
                  + " | r* " + " ".join(f"{v:+.2f}" for v in b['r_star'].values())
                  + "".join(f" | r* (capex on inv., {sc}) " + " ".join(f"{v:+.2f}" for v in rs.values())
                            for sc, rs in (b.get('r_star_capex_on_investment') or {}).items())
                  + (" | r* (capex on the pace) " + " ".join(f"{v:+.2f}" for v in b['r_star_capex_on_pace'].values())
                     if 'r_star_capex_on_pace' in b else "")
                  + " | debt " + " ".join(f"{v:.0f}" for v in b['debt'].values()))
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    with open(os.path.join(ROOT, "results", "macro_scenarios.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
    _, _, _, runs_a, _ = speeds("a", extras=False)
    figure(e, runs, runs_a)


def figure(e, runs, runs_a):
    SPEED_C = {"slow": "#1baf7a", "medium": "#2a78d6", "fast": "#eb6834"}
    FORK_C = {"goods": "#008300", "shelter": "#e87ba4", "wages": "#eda100"}
    RAMP = ("#b7d3f6", "#6da7ec", "#2a78d6", "#104281", "#0b2750")
    INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9.5, "axes.edgecolor": GRID,
                         "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
                         "axes.titlesize": 10.5, "axes.titleweight": "bold", "axes.titlecolor": INK,
                         "axes.titlelocation": "left"})
    fig, ax = plt.subplots(2, 3, figsize=(15, 8.8), facecolor=SURF)
    for a in ax.flat:
        a.set_facecolor(SURF); a.grid(True, color=GRID, lw=0.8); a.set_axisbelow(True)
        for s in ("top", "right"):
            a.spines[s].set_visible(False)
    ea, _ = economy("a")
    panels = ((ax[0, 0], "labour", 100, "1. Labour's share of income" + NL + "the paper's Figure 7 basis", "%"),
              (ax[0, 1], "real_wage", 1, "2. What an hour's wage buys" + NL + "support baskets per hour, start = 1", "index"),
              (ax[1, 0], "r_star", 1, "4. The neutral real rate" + NL + "investment and owners' saving down, deficits up", "%"),
              (ax[1, 1], "debt", 1, "5. Public debt", "% of income"))
    for a, key, scale, title, unit in panels:
        for k, mp in runs.items():
            y = fig7(e, mp) if key == "labour" else mp[key] / mp[key][0] if key == "real_wage" else mp[key]
            a.plot(mp["t"], y * scale, color=SPEED_C[k], lw=2, label=f"{k} automation")
        ma = runs_a["medium"]
        ya = fig7(ea, ma) if key == "labour" else ma[key] / ma[key][0] if key == "real_wage" else ma[key]
        a.plot(ma["t"], ya * scale, color=INK2, lw=1.3, ls="--", label="pre-switch (a), medium")
        a.set_title(title); a.set_ylabel(unit); a.set_xlabel("years")
        if key == "labour":                              # one legend: the speed colours are the same in panels 1, 2, 4, 5
            a.legend(frameon=False, fontsize=8.5, labelcolor=INK)
    a = ax[1, 0]
    a.axhline(0, color=INK2, lw=0.8)
    mp = runs["medium"]
    a.plot(mp["t"], r_star_capex_on_pace(e, mp, m.Bridges()), color=SPEED_C["medium"], lw=1.4, ls=":",
           label=f"medium, capex on the pace of tasks ({m.Bridges().alpha_capex:g}, as tuned on (b))")
    a.legend(frameon=False, fontsize=8, labelcolor=INK, loc="lower left")
    a = ax[0, 2]
    for key, lab in (("pi_goods", "goods"), ("pi_shelter", "shelter"), ("pi_wage", "wages")):
        a.plot(mp["t"], mp[key], color=FORK_C[lab], lw=2, label=lab)
    a.axhline(mp["pi_star"], color=INK2, lw=1, ls="--")
    a.text(14.8, mp["pi_star"] + 0.6, "the basket, on target", ha="right", fontsize=8.5, color=INK2)
    a.set_title("3. The fork, medium speed" + NL + "inflation with the basket held on target"); a.set_ylabel("% a year"); a.set_xlabel("years")
    a.legend(frameon=False, fontsize=8.5, labelcolor=INK, loc="upper right")
    a = ax[1, 2]
    for d, c in zip(DATES, RAMP):
        i = int(np.argmin(np.abs(mp["t"] - d)))
        a.plot(T, cv.zero(T, mp["_states"][i]), color=c, lw=2, marker="o", ms=3.5, label=f"year {d:g}: policy {mp['_policy'][i]:.2f}%")
    a.set_xscale("log"); a.set_xticks([1 / 12, 1, 2, 5, 10, 30]); a.set_xticklabels(["1M", "1Y", "2Y", "5Y", "10Y", "30Y"])
    a.set_title("6. The OIS curve along the medium path"); a.set_ylabel("zero rate, %")
    a.legend(frameon=False, fontsize=8.5, labelcolor=INK)
    _, info = m.central()
    tg = info["targets"]
    fig.text(0.01, 0.005, f"Calibration (c), central: the machine chain at BEA's measured labour content (theta {info['theta_V']:.2f}, chain share "
             f"{info['chain_share']:.2f}, sigma {info['sigma_V']:.2f}), labour {tg.labour:.2f}, employment {tg.participation:.2f}, "
             f"{tg.baskets_per_person:g} baskets per person, site {tg.site * 100:.0f}% of the basket;" + NL + f"capability 1 → {m.DEEP_ETA_END:g}, labour per "
             "machine-service hour to a fifth of its start; required return fixed. Dashed: the pre-switch flow benchmark (a). Bridges refit on (c) "
             f"(Logs 46, 54): scale {m.NEUTRAL_SCALE_GDP:g} per pp of GDP ({m.NEUTRAL_SCALE:.3f} per pp of income), investment key "
             f"{m.INVESTMENT_KEY_GDP:g} x pass-through {m.INVESTMENT_PASS_THROUGH:g}, owners' saving gap {m.OWNERS_SAVING_GAP:g}, deficits' "
             f"pass-through {m.DEFICIT_PASS_THROUGH:g}, start deficit {m.START_DEFICIT:g}% of income.", fontsize=8, color=INK2)
    fig.tight_layout(rect=(0, 0.035, 1, 1))
    p = os.path.join(ROOT, "figures", "fig_macro_scenarios.png"); fig.savefig(p, dpi=150, facecolor=SURF); print(p)


# ------------------------------------------------------------------ capital's part: the split, a rate shock, the loop
def guarded(e, tech, br, years: float = 15.0, dt: float = 0.25):
    """(macro_path, None) if every date has a land-scarce equilibrium; otherwise (None, a record: the error, the years the
    run solves — its longest solved prefix, calibration_c.path_prefix: each date depends only on the past — and the first
    failing date). The prefix itself is not kept: no readout here is defined on a truncated run."""
    try:
        return m.macro_path(e, tech, br, years, dt), None
    except m.NoEquilibrium as ex:
        err = str(ex)
    import calibration_c as cc      # local: only a failing run needs it
    _, solved, _ = cc.path_prefix(e, tech, br, years, dt)
    return None, {"error": err, "solved_years": solved, "first_failing_year": (solved + dt) if solved is not None else 0.0}


def capital_runs(e, base: m.Bridges | None = None):
    """The medium path at a fixed return, with the return following r*, and with a sustained +200 bp, on base (default the
    refit; the comparator (b) passes macro.BRIDGES_B)."""
    tech = m.deep_tech(e)
    br = m.feedback_bridges(e, base=base)
    fixed = m.macro_path(e, tech, m.Bridges() if base is None else base)
    follow, err_f = guarded(e, tech, br)
    shock, err_s = guarded(e, tech, replace(br, rho_shift=2.0))
    return fixed, follow, shock, {"follow": err_f, "shock_200bp": err_s}


def split(e, mp):
    return {"labour": mp["labor_share"], "housing site": e.h * mp["Y"] / mp["income"],
            "machine-chain land": e.b * e.delta * mp["X"] / mp["income"], "interest": mp["capital_share"]}


def lag_phase(t, gap):
    """Automation behind the fixed-return path (gap = x following r* less x at a fixed return, < 0): the first and last
    date it lags, and the deepest lag (pp of tasks) and its date; None if it never lags."""
    lag = np.nonzero(gap[1:] < 0)[0] + 1
    if not len(lag):
        return None
    j = int(np.argmin(gap))
    return {"from_year": float(t[lag[0]]), "to_year": float(t[lag[-1]]), "deepest_tasks_pp": round(float(gap[j] * 100), 5),
            "deepest_year": float(t[j])}


def capital_block(e, fixed, follow, shock, errors):
    """The split along the medium path (return following r*), a sustained +200 bp and the loop — the pre-switch keys, and
    the readouts added at the switch. If a run has a date with no land-scarce equilibrium, only the errors are stored."""
    res = {"errors": errors}
    if follow is None or shock is None:
        res["not_computed"] = "a run has a date with no land-scarce equilibrium (errors); no readout is defined on a truncated run"
        return res
    t = follow["t"]
    x_mid = float(np.interp(6.0, t, follow["x"]))
    delay_weeks = (float(np.interp(x_mid, shock["x"], t)) - 6.0) * 52
    sp = split(e, follow)
    gap, r_dev = follow["x"] - fixed["x"], follow["rho"] - fixed["rho"]
    mask = np.abs(r_dev) > 0.05
    dx = (shock["x"] - follow["x"])[1:]
    land = sp["housing site"] + sp["machine-chain land"]
    res.update({"split_start": {k: round(float(v[0]), 3) for k, v in sp.items()},
                "split_year15": {k: round(float(v[-1]), 3) for k, v in sp.items()},
                "split_basis": "labour = all wages over income (solve's labor_share); housing site = h Y / income; machine-chain land = "
                               "b delta X / income; interest = capital_share",
                "chain_share_of_land_rent_start_year15": [round(float(sp["machine-chain land"][0] / land[0]), 3),
                                                          round(float(sp["machine-chain land"][-1] / land[-1]), 3)],
                "capital_output_start": round(float(m.solve(e)["capital_output"]), 2),
                "shock_200bp": {"max_labour_share_pp": round(float(np.max(shock["labor_share"] - follow["labor_share"]) * 100), 2),
                                "max_tasks_pp": round(float(np.min(shock["x"] - follow["x"]) * 100), 2),
                                "delay_at_year6_weeks": round(delay_weeks, 1),
                                "slows_every_date": bool(np.all(dx < 0)),
                                "raises_labour_share_every_date": bool(np.all((shock["labor_share"] - follow["labor_share"])[1:] > 0)),
                                "max_labour_share_bea_pp": round(float(np.max(shock["labour_share_bea"] - follow["labour_share_bea"]) * 100), 2),
                                "labour_basis": "max_labour_share_pp: all wages over income (solve's labor_share); "
                                                "max_labour_share_bea_pp: the paper's Figure 7 basis (labour_share_bea)"},
                "loop_year15_tasks_ahead_pp": round(float(gap[-1] * 100), 2),
                "loop_lag_phase": lag_phase(t, gap),
                "loop_corr_return_vs_tasks": round(float(np.corrcoef(r_dev[mask], gap[mask])[0, 1]), 3) if mask.sum() > 2 else None,
                "max_rho_rise_pp": {"follow": round(float(follow["rho"].max() - follow["rho"][0]), 3),
                                    "shock_200bp": round(float(shock["rho"].max() - follow["rho"][0]), 3)},
                "investment_income_start_year15": [round(float(investment_income(e, follow)[0]), 4),
                                                   round(float(investment_income(e, follow)[-1]), 4)]})
    return res


def import_share_of_sigma():
    """Imported content's share of sigma_V at the central's start (results/calibration_c.json, readouts.import_as_land)."""
    with open(m.CENTRAL_SOURCE, encoding="utf-8") as f:
        return float(json.load(f)["readouts"]["import_as_land"]["imports_share_of_sigma"])


def loop_bridges_at_path(e, fixed, follow) -> dict:
    """A readout, not a default (decision 96): the central's medium path with the return following r* and r*'s bridges read
    along the path (bridges_at "path", as the comparators read them) against the refit's (read at the start's required return,
    so r* is the fixed-return r*): the gap in r* between the two and year 15's tasks ahead of the fixed-return path on each."""
    path, err = guarded(e, m.deep_tech(e), replace(m.feedback_bridges(e), bridges_at="path"))
    if path is None or follow is None:
        return {"error": err, "not_computed": "a run has a date with no land-scarce equilibrium"}
    t = follow["t"]
    d = follow["r_star"] - path["r_star"]
    j = int(np.argmax(np.abs(d)))
    return {"note": "r* with the bridges read at the start's required return (the refit, decision 96) less r* with them read along "
                    "the path (the rate's own effect on investment, owners' income and the deficit fed back), the central's medium "
                    "path, the return following r*; tasks ahead: x less the fixed-return path's x, pp",
            "r_star_start_minus_path_max_abs_pp": round(float(abs(d[j])), 3), "r_star_start_minus_path_at_max_pp": round(float(d[j]), 3),
            "max_year": float(t[j]),
            "r_star_start_minus_path_y4_y6_y8_y10_y15_pp": [round(float(np.interp(y, t, d)), 3) for y in (4, 6, 8, 10, 15)],
            "tasks_ahead_year15_pp": {"start (the refit)": round(float((follow["x"][-1] - fixed["x"][-1]) * 100), 2),
                                      "path": round(float((path["x"][-1] - fixed["x"][-1]) * 100), 2)},
            "max_rho_rise_pp_path": round(float(path["rho"].max() - path["rho"][0]), 3)}


def capital_results():
    e, rec = economy("c")
    fixed, follow, shock, errors = capital_runs(e)
    out = {"calibration": {k: float(getattr(e, k)) for k in ("T", "h", "chi_max", "k", "rho", "delta", "b", "lam")} | {"record": rec},
           "split_note": "machine-chain land = b delta K / income; under the open reading b includes the chain's imported content "
                         f"({import_share_of_sigma():.3f} of sigma_V; results/calibration_c.json readouts.import_as_land), modelled as land",
           **capital_block(e, fixed, follow, shock, errors)}
    out["loop_bridges_at_path"] = loop_bridges_at_path(e, fixed, follow)
    eb, _ = economy("b")
    fb, wb, sb, errb = capital_runs(eb, m.BRIDGES_B)
    out["comparator_b"] = {"calibration_b": {k: float(getattr(eb, k)) for k in ("T", "h", "chi_max", "k", "rho", "delta", "b")},
                           **capital_block(eb, fb, wb, sb, errb)}
    return out, (e, fixed, follow, shock), (eb, fb, wb, sb)


def capital():
    """The central along the medium path: who is paid, a sustained +200 bp on the required return, and the loop between
    the economy's real rate and automation; (b) dashed, the comparator."""
    res, (e, fixed, follow, shock), (eb, fb, wb, sb) = capital_results()
    with open(os.path.join(ROOT, "results", "capital_feedback.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, indent=1)
    print("capital (c):", res.get("split_start"), "->", res.get("split_year15"), "| +200bp:", res.get("shock_200bp"),
          "| loop:", res.get("loop_year15_tasks_ahead_pp"), "| errors:", res["errors"])
    print("capital (b):", res["comparator_b"].get("split_start"), "->", res["comparator_b"].get("split_year15"), "| +200bp:",
          res["comparator_b"].get("shock_200bp"), "| loop:", res["comparator_b"].get("loop_year15_tasks_ahead_pp"))
    print("loop lag phase (c):", res.get("loop_lag_phase"), "| (b):", res["comparator_b"].get("loop_lag_phase"))
    if follow is None or shock is None:
        return
    C = {"labour": "#2a78d6", "housing site": "#1baf7a", "machine-chain land": "#eb6834", "interest": "#e87ba4",
         "tasks": "#008300", "return": "#e87ba4"}
    INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.9), facecolor=SURF)
    for a in ax:
        a.set_facecolor(SURF); a.grid(True, color=GRID, lw=0.8); a.set_axisbelow(True); a.set_xlabel("years")
        for sp_ in ("top", "right"):
            a.spines[sp_].set_visible(False)
    t = follow["t"]
    a = ax[0]
    sp, spb = split(e, follow), split(eb, wb)
    ends = {k: v[-1] * 100 for k, v in sp.items()}
    placed, gap_ = {}, 4.5                               # labels at the lines' ends, at least gap_ pp apart
    for k in sorted(ends, key=ends.get):
        placed[k] = max(ends[k], max(placed.values()) + gap_) if placed else ends[k]
    for k, v in sp.items():
        a.plot(t, v * 100, color=C[k], lw=2)
        a.plot(t, spb[k] * 100, color=C[k], lw=1.1, ls="--")
        a.annotate(k, (t[-1], v[-1] * 100), (t[-1] + 0.4, placed[k]), textcoords="data", fontsize=8.5, color=C[k], va="center",
                   arrowprops=dict(arrowstyle="-", color=C[k], lw=0.6, shrinkA=0, shrinkB=0))
    a.set_xlim(0, 19); a.set_xticks([0, 5, 10, 15])
    a.set_title("1. Who is paid, medium automation" + NL + "(c) central; dashed: (b)"); a.set_ylabel("% of income")
    a = ax[1]
    a.plot(t, (shock["labor_share"] - follow["labor_share"]) * 100, color=C["labour"], lw=2, label="labour's share (all wages)")
    a.plot(t, (shock["x"] - follow["x"]) * 100, color=C["tasks"], lw=2, label="tasks done by machines")
    a.plot(t, (sb["labor_share"] - wb["labor_share"]) * 100, color=C["labour"], lw=1.1, ls="--")
    a.plot(t, (sb["x"] - wb["x"]) * 100, color=C["tasks"], lw=1.1, ls="--", label="(b), dashed")
    a.axhline(0, color=INK2, lw=0.8)
    a.set_title("2. A sustained +200 bp on the required return" + NL
                + f"difference from no shock; delays automation ~{res['shock_200bp']['delay_at_year6_weeks']:.0f} weeks")
    a.set_ylabel("percentage points"); a.legend(frameon=False, fontsize=8.5, labelcolor=INK)
    a = ax[2]
    a.plot(t, follow["rho"] - fixed["rho"], color=C["return"], lw=2, label="required return, vs fixed")
    a.plot(t, (follow["x"] - fixed["x"]) * 100, color=C["tasks"], lw=2, label="tasks done by machines, vs fixed")
    a.plot(t, wb["rho"] - fb["rho"], color=C["return"], lw=1.1, ls="--")
    a.plot(t, (wb["x"] - fb["x"]) * 100, color=C["tasks"], lw=1.1, ls="--", label="(b), dashed")
    a.axhline(0, color=INK2, lw=0.8)
    rises = follow["rho"].max() > follow["rho"][0] + 0.01
    a.set_title("3. The loop: the return follows r*" + NL + ("up in the build-out, down after" if rises
                                                            else "r* never rises: the return only falls"))
    a.set_ylabel("percentage points"); a.legend(frameon=False, fontsize=8.5, labelcolor=INK)
    fig.text(0.01, 0.01, f"Calibration (c), central: required return {e.rho * 100:.2f}% (r0* {m.Bridges().r0_star:.2f}% + premium {m.capital_premium(e):.2f} pp), "
             f"depreciation {e.delta * 100:.1f}%, capital/income {res['capital_output_start']:.2f} (implied); machine-chain land includes the chain's "
             "imported content (modelled as land)." + NL + f"Dashed: calibration (b), return {eb.rho * 100:.2f}%, depreciation {eb.delta * 100:.0f}%. "
             "Bridges refit on (c) (Logs 46, 54); (b) on its own, as tuned.", fontsize=8, color=INK2)
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    p = os.path.join(ROOT, "figures", "fig_capital_feedback.png"); fig.savefig(p, dpi=150, facecolor=SURF); print(p)


if __name__ == "__main__":
    if "--refresh-fiscal" in sys.argv:
        fiscal_data(refresh=True)
    main()
    capital()
