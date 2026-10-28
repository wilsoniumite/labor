# bank_scenarios.py — the stylised bank (bank.py) on four paths: the status quo; a pure tightening (no
# automation: announced at year 1, policy +250 bp over a year, held two years, then back — the first half of her question in
# isolation); deep automation with deficits dominating and with owners' saving dominating (her second half, the interest
# income flowing back as saving). At the central reading of the investment key rates fall in both branches; in the deficits
# branch they rise once little of the investment fall counts as excess saving (decision 93: the pass-through readout).
#
# The bank's rates come from the market's curve (the belief-weighted mixture, recognition.py); its
# borrowers and tenants live in the true world's macro path. Commercial rents follow the site (the
# model's single land market) or, as the alternative, the wage bill.
#
# CALIBRATION (her decision, 2026-09-30): the worlds run on calibration (c)'s central economy, macro.central() — the open
# (domp) reading, the low root in k — with the required return following r* from that economy's own rho
# (macro.feedback_bridges: premium rho x 100 - 0.75 = 6.80 pp, not (b)'s 5.0) and deep automation relative to its own
# lambda (macro.deep_tech: lambda to a fifth of its start, not (b)'s absolute 0.01). The bridges are the refit on (c)
# (macro.Bridges(); Log 46, revised in Log 54): r* keyed to replacement investment / income at Rachel and Smith's coefficient
# times its pass-through (decision 93), owners' saving and deficits on one scale from published evidence (per point of the
# model's income), the fiscal start at Sweden's measured primary deficit net of the state's asset income (decision 95), the
# debt's rate floored at the policy floor, and on these feedback paths the bridges read at the start's required return
# (decision 96). SCEN's two branches are macro.BRANCHES: the two
# direction bridges at the ends of their evidence ranges, each against the other's opposite end (deficits dominate: owners'
# saving gap 0.15, no Ricardian offset; owners' saving dominates: gap 0.45, offset 0.5), the scale and the investment key
# held. Also stored: the high root (the sensitivity) and (b) (the comparator, on macro.BRIDGES_B and SCEN_B, the branches as
# set on (b): bit-identical to the pre-switch runs). No dial here moves the required return; each world's largest rise in it
# is stored against the central's rate headroom (beyond it solve raises NoEquilibrium) and checked. A readout, not a
# finding: the two automated branches with the new world's r* keyed to the pace of tasks instead (demand.py's
# r_star_pace_keyed, alpha_capex 0.25, the key as tuned on (b)). A second readout (pass_through_readout): the deficits branch
# with the investment key's pass-through at 1 / 0.6 / 0.4 / 0, on both roots.
#
# Provenance: the economy from results/calibration_c.json (BEA; code/calibration_c.py, gated by
# checks/check_calibration_c.py); the bank is illustrative (bank.Bank defaults), not any bank's.
# Run from paths/:  ../venv/Scripts/python.exe code/bank_scenarios.py
# Out: results/bank.json, figures/fig_bank.png

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
import bank as bk  # noqa: E402
import macro as m  # noqa: E402
import recognition as rc  # noqa: E402
import regimes as rg  # noqa: E402

NL = chr(10)
T = np.array([2.0, 3.0, 10.0])
SCEN = {"status quo": (dict(), "old"), **{k: (v, "new") for k, v in m.BRANCHES.items()}}       # on the refit (macro.Bridges())
SCEN_B = {"status quo": (dict(), "old"), **{k: (v, "new") for k, v in m.BRANCHES_B.items()}}   # (b)'s, on macro.BRIDGES_B
HORIZON = 15.0
TIGHTEN = ((0.0, 2.75), (1.0, 2.75), (2.0, 5.25), (4.0, 5.25), (5.5, 2.75), (25.0, 2.75))   # (year, policy %)


def base_bridges(which: str = "lo"):
    """(base bridges, branches) for 'lo' / 'hi' (the refit: macro.Bridges(), SCEN) or 'b' (macro.BRIDGES_B, SCEN_B)."""
    return (m.BRIDGES_B, SCEN_B) if which == "b" else (m.Bridges(), SCEN)


def economy(which: str = "lo"):
    """(Economy, calibration record) for 'lo' (the central (c)), 'hi' (its high root, the sensitivity) or 'b' (the
    pre-switch calibration, the comparator)."""
    if which == "b":
        e, _, _, _ = m.calibrate(base=m.CAPITAL_BASE)
        return e, {"tag": "b", "root": "lo", "rho": e.rho, "capital_premium": m.capital_premium(e), "k": e.k,
                   "headroom_pp": m.rate_headroom(e), "source": "macro.calibrate(base=macro.CAPITAL_BASE): the comparator "
                   "(headroom 20.0 is rate_headroom's cap: at least 20 pp)"}
    e, info = m.central(which)
    return e, {k: info[k] for k in ("tag", "root", "rho", "capital_premium", "multiplier", "headroom_pp", "k", "x",
                                    "participation", "labour_share_bea", "source")}


def path(e, bridges, truth, lr=rc.Learning(sigma=1.0, p0=0.05), base=None):
    br = m.feedback_bridges(e, base=base, **bridges)
    old = m.macro_path(e, m.hold_tech(e), br, 25.0, 0.25)
    new = m.macro_path(e, m.deep_tech(e), br, 25.0, 0.25)
    return market(old, new, truth, lr)


def market(old, new, truth, lr=rc.Learning(sigma=1.0, p0=0.05)):
    """The market on two worlds: its belief, policy rate and zero rates (2Y, 3Y, 10Y)."""
    p = rc.learn(old, new, replace(lr, truth=truth))
    mixes, _, _, pol = rc.market_curves(old, new, p)
    z = np.array([rg.zero(T, mx) for mx in mixes])                 # zero rates, %
    return old, new, p, pol, {"2Y": z[:, 0], "3Y": z[:, 1], "10Y": z[:, 2]}


def at(t, x, yr):
    return float(x[int(np.argmin(np.abs(t - yr)))])


def summary(t, r):
    w = t <= HORIZON + 1e-9
    nii, res, loss = r["nii"][w], r["result"][w], r["losses"][w]
    dep0 = r["rates"]["deposit_rate"][0]
    i_pk = int(np.argmax(np.abs(r["policy"][w] - r["policy"][0])))
    dpol = r["policy"][w][i_pk] - r["policy"][0]
    return {
        "policy_start_peak_end": [round(float(r["policy"][0]), 2), round(float(r["policy"][w][i_pk]), 2), round(float(r["policy"][w][-1]), 2)],
        "nii_start": round(float(nii[0]), 2), "nii_max": round(float(nii.max()), 2), "nii_max_year": round(float(t[w][np.argmax(nii)]), 2),
        "nii_min": round(float(nii.min()), 2), "nii_min_year": round(float(t[w][np.argmin(nii)]), 2),
        "deposit_spread_start_max": [round(float(r["nii_lines"]["deposit spread"][0]), 2), round(float(r["nii_lines"]["deposit spread"][w].max()), 2)],
        "mortgage_margin_min": round(float(r["nii_lines"]["mortgage margin"][w].min()), 2),
        "deposit_beta_at_policy_extreme": None if abs(dpol) < 0.5 else round(float((r["rates"]["deposit_rate"][w][i_pk] - dep0) / dpol), 2),
        "deposit_beta_year_after": None if abs(dpol) < 0.5 else round(float((at(t, r["rates"]["deposit_rate"], t[w][i_pk] + 1) - dep0)
                                                                            / (at(t, r["policy"], t[w][i_pk] + 1) - r["policy"][0] + 1e-12)), 2),
        "house_real_y5_y10_y15": [round(at(t, r["house_real"], y), 2) for y in (5, 10, 15)],
        "house_real_min_and_year": [round(float(r["house_real"][w].min()), 3), round(float(t[w][np.argmin(r["house_real"][w])]), 2)],
        "wage_real_y5_y10_y15": [round(at(t, r["wage"] / np.exp(0.02 * t), y), 2) for y in (5, 10, 15)],
        "employed_y5_y10_y15": [round(at(t, r["employed"], y), 2) for y in (5, 10, 15)],
        "dsr_mean_max": round(float(r["borrowers"]["dsr_mean"][w].max()), 3),
        "share_over_dsr_line_max": round(float(r["borrowers"]["share_over_line"][w].max()), 3),
        "ltv_y10": round(at(t, r["borrowers"]["ltv"], 10), 3),
        "mortgage_loss_rate_max_pct": round(float(r["borrowers"]["loss_rate"][w].max()), 3),
        "cre_icr_min": round(float(r["cre"]["icr_mean"][w].min()), 2),
        "cre_share_below_line_max": round(float(r["cre"]["share_below_line"][w].max()), 3),
        "losses_max": round(float(loss.max()), 3), "losses_max_year": round(float(t[w][np.argmax(loss)]), 2),
        "result_start_max_min": [round(float(res[0]), 2), round(float(res.max()), 2), round(float(res.min()), 2)],
        "result_max_year_min_year": [round(float(t[w][np.argmax(res)]), 2), round(float(t[w][np.argmin(res)]), 2)],
    }


def bank_runs(e, which: str = "lo"):
    """The bank on the four paths (and the wage-bill variants) on economy e ('lo', 'hi' or 'b': its bridges and branches,
    base_bridges): (summaries, runs, required-return rise)."""
    base, scen = base_bridges(which)
    out, runs, rise = {}, {}, {}
    old, new, p, pol, zeros = path(e, {}, "old", base=base)
    t = old["t"]
    pol_t = np.interp(t, [a for a, _ in TIGHTEN], [b_ for _, b_ in TIGHTEN])
    r = bk.run(t, pol_t, bk.expectation_zeros(t, pol_t, known_from=1.0), np.zeros_like(t), old, new, truth="old")   # a surprise at year 1
    runs["a pure tightening"] = (t, r, np.zeros_like(t))
    out["a pure tightening"] = summary(t, r)
    for name, (bridges, truth) in scen.items():
        old, new, p, pol, zeros = path(e, bridges, truth, base=base)
        t = old["t"]
        rise[name] = round(float(max(np.max(old["rho"]), np.max(new["rho"])) - old["rho"][0]), 4)   # pp, either world, 25 years
        for inc in ("site", "employment"):
            if name == "status quo" and inc == "employment":
                continue
            b = bk.Bank(cre_income=inc)
            r = bk.run(t, pol, zeros, p, old, new, truth=truth, b=b)
            key = name if inc == "site" else f"{name}, office rents follow the wage bill"
            runs[key] = (t, r, p)
            out[key] = summary(t, r)
    return out, runs, rise


IK_FIELDS = ("policy_start_peak_end", "nii_max", "nii_min", "nii_min_year", "house_real_y5_y10_y15", "dsr_mean_max",
             "share_over_dsr_line_max", "cre_share_below_line_max", "result_start_max_min")


def pace_keyed(e):
    """A readout, not a finding: the two automated branches with the new world's r* (and so its desired rate and the
    market's curve) keyed to the pace of tasks at alpha_capex 0.25 — the key as tuned on (b), the default before the refit —
    instead of investment spending (demand.r_star_pace_keyed); the macro path, the term premium and the required return are
    left as solved."""
    import demand as dmd   # local: demand imports this module
    out = {"note": "the bank on the new world's r* keyed to the pace of tasks (demand.py's readout; the key as tuned on (b)); the macro "
                   "path, term premium and required return as solved; office rents follow the site",
           "alpha_capex": m.Bridges().alpha_capex}
    for name in ("deficits dominate", "owners' saving dominates"):
        bridges, truth = SCEN[name]
        br = m.feedback_bridges(e, **bridges)
        old = m.macro_path(e, m.hold_tech(e), br, 25.0, 0.25)
        new = m.macro_path(e, m.deep_tech(e), br, 25.0, 0.25)
        rec = {}
        for k, a in (("investment keyed (the refit)", None), ("pace keyed (as tuned on (b))", br.alpha_capex)):
            nw = new
            if a is not None:
                alt = dmd.r_star_pace_keyed(new, e, br, a)
                nw = dict(new, r_star=alt, desired=new["desired"] - new["r_star"] + alt)
            o_, n_, p, pol, zeros = market(old, nw, truth)
            r = bk.run(o_["t"], pol, zeros, p, o_, n_, truth=truth, b=bk.Bank())
            sm = summary(o_["t"], r)
            rec[k] = {f: sm[f] for f in IK_FIELDS} | {"z10_y5_y10_y15": [round(at(o_["t"], zeros["10Y"], y), 2) for y in (5, 10, 15)]}
        out[name] = rec
    return out


PASS_THROUGHS = (1.0, 0.6, 0.4, 0.0)     # the investment key's pass-through: gross (the central) to netted


def pass_through_readout(e, which: str = "lo") -> dict:
    """The deficits branch with the investment key at each pass-through of the investment fall (decision 93: 1 gross, the
    central; 0 netted against capital consumption), on economy e with the refit's bridges ('lo' or 'hi'): the policy rate's
    start, peak and year 15, NII's low and high, the 10Y at years 5 / 10 / 15 and r* at year 15; office rents follow the site."""
    base, scen = base_bridges(which)
    bridges, truth = scen["deficits dominate"]
    out = {}
    for pt in PASS_THROUGHS:
        a = m.investment_key(pt)
        old, new, p, pol, zeros = path(e, dict(bridges, alpha_inv=a), truth, base=base)
        t = old["t"]
        sm = summary(t, bk.run(t, pol, zeros, p, old, new, truth=truth, b=bk.Bank()))
        out[f"{pt:g}"] = {"alpha_inv": a, "policy_start_peak_end": sm["policy_start_peak_end"], "nii_min": sm["nii_min"],
                          "nii_max": sm["nii_max"], "z10_y5_y10_y15": [round(at(t, zeros["10Y"], y), 2) for y in (5, 10, 15)],
                          "r_star_y15": round(at(t, new["r_star"], 15), 2)}
    return out


def main():
    e, cal = economy("lo")
    out = {"bank": "illustrative Nordic-style balance sheet (bank.Bank defaults); not any bank's", "calibration": cal}
    res, runs, rise = bank_runs(e)
    out.update(res)
    out["sensitivity: r* keyed to the pace of tasks"] = pace_keyed(e)
    out["sensitivity: the investment key's pass-through"] = {
        "note": "the deficits branch with alpha_inv at Rachel and Smith's 0.2 per point of GDP times the pass-through of the investment "
                "fall, per point of income (macro.investment_key; decision 93): 1 gross (the central), 0 netted against capital "
                "consumption; the rest of the branch held; the central and its high root",
        "pass_throughs": list(PASS_THROUGHS), "central (c)": pass_through_readout(e, "lo"),
        "high root": pass_through_readout(economy("hi")[0], "hi")}
    out["required_return_rise_pp"] = {"note": "largest rise in the required return over 25 years (either world, pp), against the "
                                              "central's rate headroom at the start (beyond it solve raises NoEquilibrium)",
                                      "headroom_pp": cal["headroom_pp"], **rise}
    for which, key in (("hi", "sensitivity: the high root"), ("b", "comparator: calibration (b)")):
        e2, cal2 = economy(which)
        res2, _, rise2 = bank_runs(e2, which)
        out[key] = {"calibration": cal2, "required_return_rise_pp": rise2, **res2}
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    with open(os.path.join(ROOT, "results", "bank.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
    for k, v in out.items():
        print(k, v)
    figure(runs)


def figure(runs):
    INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
    COL = {"status quo": "#52514e", "a pure tightening": "#eb6834", "deficits dominate": "#e34948", "owners' saving dominates": "#2a78d6"}
    LINE_C = {"deposit spread": "#2a78d6", "mortgage margin": "#1baf7a", "equity (free funds)": "#eb6834",
              "securities vs policy": "#b9b8b3"}
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9.5, "axes.edgecolor": GRID,
                         "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
                         "axes.titlesize": 10.5, "axes.titleweight": "bold", "axes.titlecolor": INK,
                         "axes.titlelocation": "left"})
    fig, ax = plt.subplots(2, 3, figsize=(16, 9.4), facecolor=SURF, layout="constrained")
    fig.get_layout_engine().set(rect=(0, 0.03, 1, 0.97), h_pad=0.12, w_pad=0.1)
    for a in ax.flat:
        a.set_facecolor(SURF); a.grid(True, color=GRID, lw=0.8); a.set_axisbelow(True)
        for sp in ("top", "right"):
            a.spines[sp].set_visible(False)
    main_keys = [k for k in COL]
    t0 = runs["status quo"][0]
    w = t0 <= HORIZON + 1e-9
    # 1. rates
    a = ax[0, 0]
    for k in main_keys:
        t, r, _ = runs[k]
        a.plot(t[w], r["policy"][w], color=COL[k], lw=2, label=f"{k}: policy")
        a.plot(t[w], r["rates"]["deposit_rate"][w], color=COL[k], lw=1.3, ls="--")
    a.set_title("1. The policy rate, and what depositors are paid (dashed)" + NL + "the market's curve through recognition")
    a.set_ylim(bottom=a.get_ylim()[0] - 1.4)   # room under the lines for the legend
    a.set_ylabel("%"); a.set_xlabel("years"); a.legend(frameon=False, fontsize=8, labelcolor=INK, loc="lower left", ncol=2)
    # 2. NII decomposition, the pure tightening
    a = ax[0, 1]
    t, r, _ = runs["a pure tightening"]
    w8 = t <= 8.0 + 1e-9
    for ln, col in LINE_C.items():
        a.plot(t[w8], (r["nii_lines"][ln] - r["nii_lines"][ln][0])[w8], color=col, lw=2, label=ln)
    a.plot(t[w8], (r["nii"] - r["nii"][0])[w8], color=INK, lw=2.4, label="net interest income")
    a.axhline(0, color=INK2, lw=0.8)
    a2 = a.twinx(); a2.plot(t[w8], r["policy"][w8], color=COL["a pure tightening"], lw=1, ls=":"); a2.set_ylabel("policy rate, % (dotted)", color=INK2)
    a2.spines["top"].set_visible(False); a2.tick_params(colors=INK2)
    a.set_title("2. Where the NII gain comes from — a pure tightening" + NL + "+250 bp, no automation; change from the start, % of assets")
    a.set_ylabel("pp of assets"); a.set_xlabel("years"); a.legend(frameon=False, fontsize=8, labelcolor=INK, loc="upper right")
    # 3. house prices and wages
    a = ax[0, 2]
    for k in main_keys:
        t, r, _ = runs[k]
        a.plot(t[w], r["house_real"][w], color=COL[k], lw=2, label=f"{k}: house prices")
        a.plot(t[w], (r["wage"] / np.exp(0.02 * t))[w] * r["employed"][w], color=COL[k], lw=1.3, ls="--")
    a.set_yscale("log")
    a.set_title("3. Houses and wages part ways" + NL + "real, start = 1; dashed: the start's wage bill")
    a.set_xlabel("years"); a.legend(frameon=False, fontsize=8, labelcolor=INK, loc="lower left")   # clear of the early rise
    # 4. borrowers
    a = ax[1, 0]
    for k in main_keys:
        t, r, _ = runs[k]
        a.plot(t[w], r["borrowers"]["share_over_line"][w] * 100, color=COL[k], lw=2, label=f"{k}")
        a.plot(t[w], r["borrowers"]["exited"][w] * 100, color=COL[k], lw=1.3, ls=":")
    a.set_title("4. Borrowers over the debt-service line (solid)" + NL + "and no longer working (dotted), % of borrowers")
    a.set_ylabel("%"); a.set_xlabel("years"); a.legend(frameon=False, fontsize=8, labelcolor=INK, loc="upper left")
    # 5. commercial property
    a = ax[1, 1]
    for k in ("deficits dominate", "owners' saving dominates"):
        for suffix, ls in (("", "-"), (", office rents follow the wage bill", "--")):
            t, r, _ = runs[k + suffix]
            a.plot(t[w], r["cre"]["share_below_line"][w] * 100, color=COL[k], lw=2, ls=ls,   # short labels: the legend clears the curves
                   label={"deficits dominate": "deficits", "owners' saving dominates": "owners' saving"}[k] + (", wage-bill rents" if suffix else ", site rents"))
    for k in ("status quo", "a pure tightening"):
        t, r, _ = runs[k]
        a.plot(t[w], r["cre"]["share_below_line"][w] * 100, color=COL[k], lw=2, label=k)
    a.set_title("5. Commercial property: interest cover below 1.5x" + NL + "% of the book; rents follow the site or the wage bill")
    a.set_ylabel("%"); a.set_xlabel("years"); a.legend(frameon=False, fontsize=8, labelcolor=INK, loc="upper left")
    # 6. the P&L
    a = ax[1, 2]
    for k in main_keys:
        t, r, _ = runs[k]
        a.plot(t[w], r["nii"][w], color=COL[k], lw=1.3, ls="--")
        a.plot(t[w], r["result"][w], color=COL[k], lw=2.2, label=k)
    t, r, _ = runs["deficits dominate, office rents follow the wage bill"]
    a.plot(t[w], r["result"][w], color=COL["deficits dominate"], lw=1.6, ls=":", label="deficits dominate, office rents follow wages")
    a.set_title("6. NII (dashed) and NII less credit losses (solid)" + NL + "% of assets a year, before costs")
    a.set_ylim(bottom=min(0.0, a.get_ylim()[0]))   # room under the lines for the legend
    a.set_ylabel("% of assets"); a.set_xlabel("years"); a.legend(frameon=False, fontsize=8, labelcolor=INK, loc="lower left", ncol=2)
    fig.text(0.01, 0.005, "Illustrative bank (bank.Bank): not any bank's balance sheet. Calibration (c), the central (open reading, low root; "
             "bridges refit on (c), Logs 46 and 54); medium deep automation; market beliefs by Bayesian learning; house prices = belief-weighted expected "
             "site rents at the real 10Y + 2.5 pp.", fontsize=8, color=INK2)
    pth = os.path.join(ROOT, "figures", "fig_bank.png"); fig.savefig(pth, dpi=150, facecolor=SURF); print(pth)


if __name__ == "__main__":
    main()
