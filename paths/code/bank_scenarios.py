# bank_scenarios.py — the stylised bank (bank.py) on four paths: the status quo; a pure tightening (no
# automation: announced at year 1, policy +250 bp over a year, held two years, then back — the first half of her question in
# isolation); deep automation with deficits dominating (real rates rise); deep automation with owners'
# saving dominating (rates fall — her second half, the interest income flowing back as saving).
#
# The bank's rates come from the market's curve (the belief-weighted mixture, recognition.py); its
# borrowers and tenants live in the true world's macro path. Commercial rents follow the site (the
# model's single land market) or, as the alternative, the wage bill.
#
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
SCEN = {"status quo": (dict(), "old"),
        "deficits dominate": (dict(alpha_fiscal=0.25, alpha_rent=0.02), "new"),
        "owners' saving dominates": (dict(alpha_rent=0.12), "new")}
HORIZON = 15.0
TIGHTEN = ((0.0, 2.75), (1.0, 2.75), (2.0, 5.25), (4.0, 5.25), (5.5, 2.75), (25.0, 2.75))   # (year, policy %)


def path(e, bridges, truth, lr=rc.Learning(sigma=1.0, p0=0.05)):
    br = m.Bridges(capital_premium=5.0, **bridges)
    old = m.macro_path(e, m.TechPath(eta_end=1.0, lam_end=e.lam), br, 25.0, 0.25)
    new = m.macro_path(e, m.TechPath(eta_end=0.04, lam_end=0.01, t_mid=6, width=6), br, 25.0, 0.25)
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


def main():
    e, _, _, _ = m.calibrate(base=m.CAPITAL_BASE)
    out, runs = {"bank": "illustrative Nordic-style balance sheet (bank.Bank defaults); not any bank's"}, {}
    old, new, p, pol, zeros = path(e, {}, "old")
    t = old["t"]
    pol_t = np.interp(t, [a for a, _ in TIGHTEN], [b_ for _, b_ in TIGHTEN])
    r = bk.run(t, pol_t, bk.expectation_zeros(t, pol_t, known_from=1.0), np.zeros_like(t), old, new, truth="old")   # a surprise at year 1
    runs["a pure tightening"] = (t, r, np.zeros_like(t))
    out["a pure tightening"] = summary(t, r)
    for name, (bridges, truth) in SCEN.items():
        old, new, p, pol, zeros = path(e, bridges, truth)
        t = old["t"]
        for inc in ("site", "employment"):
            if name == "status quo" and inc == "employment":
                continue
            b = bk.Bank(cre_income=inc)
            r = bk.run(t, pol, zeros, p, old, new, truth=truth, b=b)
            key = name if inc == "site" else f"{name}, office rents follow the wage bill"
            runs[key] = (t, r, p)
            out[key] = summary(t, r)
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, "results", "bank.json"), "w", encoding="utf-8"), indent=1)
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
    a.set_ylabel("%"); a.set_xlabel("years"); a.legend(frameon=False, fontsize=8, labelcolor=INK, loc="upper right")
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
    a.set_xlabel("years"); a.legend(frameon=False, fontsize=8, labelcolor=INK, loc="upper left")
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
            a.plot(t[w], r["cre"]["share_below_line"][w] * 100, color=COL[k], lw=2, ls=ls,
                   label=f"{k}" + (" (rents: wage bill)" if suffix else " (rents: site)"))
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
    a.set_ylabel("% of assets"); a.set_xlabel("years"); a.legend(frameon=False, fontsize=8, labelcolor=INK, loc="lower left")
    fig.text(0.01, 0.005, "Illustrative bank (bank.Bank): not any bank's balance sheet. Calibration (b); medium deep automation; market beliefs by Bayesian "
             "learning; house prices = belief-weighted expected site rents at the real 10Y + 2.5 pp.", fontsize=8, color=INK2)
    pth = os.path.join(ROOT, "figures", "fig_bank.png"); fig.savefig(pth, dpi=150, facecolor=SURF); print(pth)


if __name__ == "__main__":
    main()
