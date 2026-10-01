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
# The required return is held at the economy's own (no rate feedback, as before). Bridges at their defaults — illustrative
# coefficients set on (a)/(b), not estimates, not retuned for (c). The curves come from macro.curve_path: a stepwise central
# bank, a market learning the destination with a one-year half-life. Labour's share is reported on the basis each
# calibration targets, the paper's Figure 7 object: v n / income in (a)'s flow benchmark, labour_share_bea = v (1 - x) / Ps
# under A.4's capital ((b), (c)); all wages over income (v n / income) beside it.
#
# THE NEUTRAL RATE'S CAPEX CHANNEL, A SENSITIVITY. The default channel is keyed to the pace of tasks moving to machines
# (alpha_capex, 0.25 pp of r* per pp of tasks a year), a proxy for the build-out's investment demand. Under (c) investment
# goes the other way: machine services cheapen as lambda falls and the stock the economy needs shrinks, so investment /
# income (delta Vm K / income, the model's replacement investment at current cost) falls from 0.178 toward 0.05 along the
# medium path. The readout r_star_capex_on_investment keys the channel to that ratio instead: alpha_inv pp of r* per pp of
# investment / income times its change from the start, the owners' and fiscal channels as macro_path's — at the same two
# scales as demand.py and bank_scenarios.py, read from demand.py (one source): the bridge's own scale (alpha_capex converted
# at (b)'s start, where it was set: 0.25 over the 6.35% of income in net investment that moving 1 pp of tasks a year needs,
# 0.039; demand.alpha_inv_bridge) and the demand layer's (1 - a1)/a_r = 0.6 (an upper end; demand.alpha_inv_is). The first
# switch report reused alpha_capex's 0.25 unconverted (per pp of tasks a year, not per pp of investment / income); it lies
# between the two, and the investment term is linear in the coefficient, so its move scales with it. A readout, not a new
# default: nothing downstream reads it, and debt and policy stay on the default r*. The readouts store the end gap to the
# pace-keyed r* (the difference, not only the two ends).
#
# THE FISCAL START, A SENSITIVITY. The fiscal bridges were set on (a)/(b) and are not retuned; on the central the wage tax
# (0.40) applies to all wages, 0.554 of income, so the start is a surplus (-2.61% of income against (b)'s -0.10) and debt
# first falls. sensitivity_fiscal_start re-centres the wage tax so the central starts at (b)'s deficit and re-runs debt.
#
# CAPITAL (capital(); results/capital_feedback.json, figures/fig_capital_feedback.png). Along the medium path on the central:
# the income split (labour, the housing site, the machine chains' land — under the open reading including the chain's
# imported content, which it models as land — and interest), a sustained +200 bp on the required return, and the loop (the
# return following r* against a fixed return), with (b) as the comparator. No dial here moves the required return beyond
# +200 bp; each run's largest rise in it is stored against the central's rate headroom (7.18 pp), and a date with no
# land-scarce equilibrium is recorded — the error, the years the run solves (its longest solved prefix,
# calibration_c.path_prefix) and the first failing date — not dropped. The loop's lag phase (automation behind the
# fixed-return path) is stored as its dates and its depth. Labour's share in capital_feedback.json is all wages over income
# (solve's labor_share) unless a key says _bea (the Figure 7 basis); the +200 bp readout gives both.
#
# Provenance: the central economy from results/calibration_c.json (BEA; code/calibration_c.py, gated by
# checks/check_calibration_c.py). Gated by checks/check_macro_scenarios.py; checks/check_macro.py gates (a) and (b)
# themselves and is unchanged.
# Run from paths/:  ../venv/Scripts/python.exe code/macro_scenarios.py
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


def r_star_capex_on_investment(e: m.Economy, mp: dict, alpha_invest: float, br: m.Bridges = m.Bridges()):
    """The neutral rate with the capex channel keyed to investment spending — alpha_invest pp of r* per pp change in
    investment / income from the start — in place of the pace of tasks moving; the owners' and fiscal channels as
    macro_path's (fixed-return paths)."""
    inv = investment_income(e, mp) * 100
    return (br.r0_star + alpha_invest * (inv - inv[0]) - br.alpha_rent * (mp["nonwage_share"] - mp["nonwage_share"][0])
            + br.alpha_fiscal * (mp["deficit"] - mp["deficit"][0]))


def first_year(t, mask):
    idx = np.nonzero(mask)[0]
    return float(t[idx[0]]) if len(idx) else None


def block(e: m.Economy, mp: dict, extras: bool = True, scales: dict | None = None):
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
                "investment_income_peak_and_year": [round(float(inv[jv]), 4), float(t[jv])],
                "r_star_capex_on_investment": {}, "r_star_capex_on_investment_start_peak_end": {},
                "r_star_capex_on_investment_peak_year": {}, "r_star_capex_on_investment_rise_bp": {},
                "r_star_capex_on_investment_end_below_pace_keyed_pp": {}})
    for sc, a in (scales or invest_scales()).items():
        ri = r_star_capex_on_investment(e, mp, a)
        jri = int(np.argmax(ri))
        out["r_star_capex_on_investment"][sc] = {d: round(float(ri[i]), 2) for d, i in at.items()}
        out["r_star_capex_on_investment_start_peak_end"][sc] = [round(float(ri[0]), 2), round(float(ri[jri]), 2), round(float(ri[-1]), 2)]
        out["r_star_capex_on_investment_peak_year"][sc] = float(t[jri])
        out["r_star_capex_on_investment_rise_bp"][sc] = round(float(ri[jri] - ri[0]) * 100, 4)
        out["r_star_capex_on_investment_end_below_pace_keyed_pp"][sc] = round(float(r[-1] - ri[-1]), 2)
    return out, states, pol


def speeds(name: str, extras: bool = True, scales: dict | None = None):
    e, rec = economy(name)
    runs, blocks = {}, {}
    for k, kw in SPEEDS.items():
        mp = m.macro_path(e, m.deep_tech(e, **kw))
        blocks[k], mp["_states"], mp["_policy"] = block(e, mp, extras, scales)
        runs[k] = mp
    cal = {k: float(getattr(e, k)) for k in ("T", "h", "chi_max", "k", "g0", "g1", "a", "b", "lam", "rho", "delta")}
    return e, rec, cal, runs, blocks


def fiscal_start(e: m.Economy, target: float, br: m.Bridges = m.Bridges()):
    """The wage tax that makes economy e's start deficit equal `target` (% of income; the deficit is linear in tau_w)."""
    q = m.solve(e)
    d0, d1 = (m._deficit(replace(br, tau_w=tw), e, q)[0] for tw in (0.0, 1.0))
    return float((target - d0) / (d1 - d0))


def fiscal_start_sensitivity(e: m.Economy, eb: m.Economy) -> dict:
    """Debt on the central with the wage tax re-centred so the start deficit is (b)'s, at each speed (fixed return)."""
    target = float(m._deficit(m.Bridges(), eb, m.solve(eb))[0])
    tw = fiscal_start(e, target)
    br = replace(m.Bridges(), tau_w=tw)
    out = {"note": "the wage tax re-centred so the central starts at (b)'s deficit (the bridges' tau_w 0.40 on all wages, 0.554 of "
                   "income, gives a surplus); a sensitivity, not a new default; fixed return, the three speeds",
           "target_start_deficit_pct": round(target, 4), "tau_w": round(tw, 4), "tau_w_default": m.Bridges().tau_w, "scenarios": {}}
    for k, kw in SPEEDS.items():
        mp = m.macro_path(e, m.deep_tech(e, **kw), br)
        t = mp["t"]
        out["scenarios"][k] = {"deficit_start_end": [round(float(mp["deficit"][0]), 2), round(float(mp["deficit"][-1]), 2)],
                               "debt": {d: round(float(mp["debt"][int(np.argmin(np.abs(t - d)))]), 1) for d in DATES}}
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
    eb, _ = economy("b")
    out["sensitivity_fiscal_start"] = fiscal_start_sensitivity(e, eb)
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
                            for sc, rs in (b['r_star_capex_on_investment'] or {}).items())
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
              (ax[1, 0], "r_star", 1, "4. The neutral real rate" + NL + "build-out up, owners' saving down, deficits up", "%"),
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
    for (sc, al), ls_ in zip(invest_scales().items(), (":", (0, (5, 2)))):
        a.plot(mp["t"], r_star_capex_on_investment(e, mp, al), color=SPEED_C["medium"], lw=1.4, ls=ls_,
               label=f"medium, capex on investment / income, {sc} ({al:.3g})")
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
             "machine-service hour to a fifth of its start; required return fixed. Dashed: the pre-switch flow benchmark (a). Bridge coefficients are "
             "illustrative defaults set on (a)/(b), not retuned.", fontsize=8, color=INK2)
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


def capital_runs(e):
    tech = m.deep_tech(e)
    br = m.feedback_bridges(e)
    fixed = m.macro_path(e, tech)
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


def capital_results():
    e, rec = economy("c")
    fixed, follow, shock, errors = capital_runs(e)
    out = {"calibration": {k: float(getattr(e, k)) for k in ("T", "h", "chi_max", "k", "rho", "delta", "b", "lam")} | {"record": rec},
           "split_note": "machine-chain land = b delta K / income; under the open reading b includes the chain's imported content "
                         f"({import_share_of_sigma():.3f} of sigma_V; results/calibration_c.json readouts.import_as_land), modelled as land",
           **capital_block(e, fixed, follow, shock, errors)}
    eb, _ = economy("b")
    fb, wb, sb, errb = capital_runs(eb)
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
             "Illustrative bridge defaults set on (b), not retuned.", fontsize=8, color=INK2)
    fig.tight_layout(rect=(0, 0.07, 1, 1))
    p = os.path.join(ROOT, "figures", "fig_capital_feedback.png"); fig.savefig(p, dpi=150, facecolor=SURF); print(p)


if __name__ == "__main__":
    main()
    capital()
