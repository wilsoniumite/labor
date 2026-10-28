# recognition_scenarios.py — when does the market wake up, what does the curve do, and a false dawn.
#
# The two worlds of recognition.worlds(): the status quo and medium deep automation, on calibration (c)'s central economy
# (her decision, 2026-09-30; macro.central(): the open (domp) reading, the low root in k), the required return following
# r* from its own rho (macro.feedback_bridges) and lambda falling to a fifth of its own start (macro.deep_tech). The market
# watches labour's share each quarter with noise sigma (pp) — all wages over income (solve's labor_share; labour_share_pp),
# not the paper's Figure 7 basis (labour_share_bea, (c)'s 0.47 target; labour_share_fig7_pp beside it). The two coincide on
# (b) and differ on (c), so sensitivity_signal_fig7 re-runs the noiseless recognition dates with the Figure 7 basis as the
# signal, on (c), (b) and (c)'s high root.
# Outputs: recognition dates by noise and prior; a Monte Carlo over noise draws (sigma 1 pp, 500 seeds)
# for both truths — how late recognition can be, and how often noise alone makes the market believe in
# a new world that is not coming; the market curve through recognition; the jump still waiting; and a
# narrative shock (+3 log odds at year 1.5) under each truth. The same outputs for calibration (b), the pre-switch default
# (comparator_b: bit-identical to the pre-switch results/recognition.json's numbers, which it reproduces), and for (c)'s
# high root (sensitivity_c_hi). (c) on the bridges refit on (c) (Log 46, revised in Log 54: the bridges read at the start's
# required return, decision 96), (b) on the bridges as tuned on (b).
#
# Provenance: the economy from results/calibration_c.json (BEA; code/calibration_c.py, gated by
# checks/check_calibration_c.py). Gated by checks/check_recognition.py.
# Run from paths/:  ../venv/Scripts/python.exe code/recognition_scenarios.py
# Out: results/recognition.json, figures/fig_recognition.png

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
import recognition as rc  # noqa: E402
import regimes as rg  # noqa: E402

T = np.array([1 / 12, 0.25, 0.5, 1, 2, 3, 5, 7, 10, 20, 30])
NL = chr(10)


def worlds_label(name: str) -> str:
    """What the worlds are, for one calibration (the premium and lambda read from the economy)."""
    e, br = rc.economy(name)
    tech = m.deep_tech(e)
    common = (f"the required return following r* from its own rho (premium {br.capital_premium:.2f} pp); status quo vs medium deep "
              f"automation (eta 1 -> {tech.eta_end:g}, lambda {e.lam:.4g} -> {tech.lam_end:.4g}, a fifth of its start)")
    return {"c": "calibration (c) central (the open reading, low root in k), ",
            "b": "calibration (b), the pre-switch default (the comparator), ",
            "c_hi": "calibration (c) central, high root in k (the sensitivity), "}[name] + common


def scenarios(old, new, base=rc.Learning(sigma=1.0, p0=0.05), seeds: int = 500):
    """Every output of the unit for one pair of worlds; returns (out, the arrays the figure draws)."""
    t = old["t"]
    at = [(y, int(np.argmin(np.abs(t - y)))) for y in (0, 2, 3, 4, 5, 6, 8)]
    out = {"labour_share_pp": {str(y): [round(float(old['labor_share'][i] * 100), 1), round(float(new['labor_share'][i] * 100), 1)]
                               for y, i in at},
           "labour_share_pp_basis": "all wages over income (solve's labor_share), %: [status quo, new world] — the market's signal",
           "labour_share_fig7_pp": {str(y): [round(float(old['labour_share_bea'][i] * 100), 1), round(float(new['labour_share_bea'][i] * 100), 1)]
                                    for y, i in at}}
    # 1. recognition dates, noiseless, by noise and prior
    table = {}
    for sig in (0.5, 1.0, 2.0, 4.0):
        for p0 in (0.01, 0.05, 0.2):
            p = rc.learn(old, new, replace(base, sigma=sig, p0=p0))
            c = [rc.crossing(t, p, L) for L in (0.1, 0.5, 0.9)]
            done = None if c[1] is None else float((new["labor_share"][0] - np.interp(c[1], t, new["labor_share"]))
                                                   / (new["labor_share"][0] - new["labor_share"][-1]))
            table[f"sigma {sig}, p0 {p0}"] = {"p_0.1": c[0], "p_0.5": c[1], "p_0.9": c[2], "fall_done_at_0.5": done}
    out["recognition_noiseless"] = table
    # 2. Monte Carlo over noise draws
    cross_new, false_dawn = [], 0
    for seed in range(seeds):
        pn = rc.learn(old, new, replace(base, seed=seed))
        cross_new.append(rc.crossing(t, pn, 0.5))
        po = rc.learn(old, new, replace(base, seed=10_000 + seed, truth="old"))
        false_dawn += bool(np.max(po) >= 0.5)
    cn = np.array([c for c in cross_new if c is not None])
    out["monte_carlo_sigma1"] = {"new_world_p50_date_percentiles_10_50_90": [round(float(q), 2) for q in np.percentile(cn, [10, 50, 90])],
                                 "never_crossed": seeds - len(cn),
                                 "status_quo_false_dawn_share": false_dawn / seeds}
    # 3. the market curve through recognition
    p = rc.learn(old, new, base)
    mixes, olds, news, pol = rc.market_curves(old, new, p)
    zmix = np.array([rg.zero(T, mx) for mx in mixes])
    znew = np.array([cv.zero(T, s) for s in news])
    c10, c90 = rc.crossing(t, p, 0.1), rc.crossing(t, p, 0.9)
    if c10 is None or c90 is None:                      # never recognised within the run (none of the worlds here)
        out["recognition_window"] = {"from_year": None if c10 is None else round(c10, 2), "to_year": None, "curve_move_bp": None}
    else:
        i10, i90 = int(np.searchsorted(t, c10)), int(np.searchsorted(t, c90))
        out["recognition_window"] = {"from_year": round(c10, 2), "to_year": round(c90, 2),
                                     "curve_move_bp": {lab: round(float((zmix[i90, k] - zmix[max(i10 - 1, 0), k]) * 100), 1)
                                                       for lab, k in (("3M", 1), ("2Y", 4), ("10Y", 8), ("30Y", 10))}}
    jump = (znew - zmix) * 100
    out["jump_waiting_bp_max"] = {lab: round(float(jump[:, k][np.argmax(np.abs(jump[:, k]))]), 1) for lab, k in (("2Y", 4), ("10Y", 8), ("30Y", 10))}
    # 4. a narrative shock under each truth
    nar = {}
    for truth in ("new", "old"):
        pj = rc.learn(old, new, replace(base, truth=truth, jumps=((1.5, 3.0),)))
        mj, _, _, _ = rc.market_curves(old, new, pj)
        z10 = np.array([rg.zero(np.array([10.0]), mx)[0] for mx in mj])
        nar[truth] = {"p": pj, "z10": z10}
    i15 = int(np.argmin(np.abs(t - 1.5)))
    pk = int(np.argmax(nar["old"]["p"][i15:])) + i15
    back = rc.crossing(t[pk:], 1 - nar["old"]["p"][pk:], 0.9)
    out["narrative_shock"] = {"p_after_jump": round(float(nar["old"]["p"][i15]), 3),
                              "status_quo_10Y_move_at_peak_bp": round(float((nar["old"]["z10"][pk] - nar["old"]["z10"][i15 - 1]) * 100), 1),
                              "status_quo_p_back_below_0.1_year": back}
    return out, dict(zmix=zmix, jump=jump, p=p, cn=cn, nar=nar)


def signal_fig7(old, new, base=rc.Learning(sigma=1.0, p0=0.05)):
    """The noiseless recognition dates with the paper's Figure 7 basis (labour_share_bea) as the signal, beside the default
    all-wages signal; and labour's share fall at year 3 on each basis (pp)."""
    t = old["t"]
    i3 = int(np.argmin(np.abs(t - 3.0)))
    out = {}
    for sig, lab in (("labor_share", "all wages (the default signal)"), ("labour_share_bea", "Figure 7 basis")):
        p = rc.learn(old, new, replace(base, signal=sig))
        out[lab] = {"p_0.1": rc.crossing(t, p, 0.1), "p_0.5": rc.crossing(t, p, 0.5), "p_0.9": rc.crossing(t, p, 0.9),
                    "fall_pp_at_year3": round(float((new[sig][i3] - new[sig][0]) * 100), 2)}
    return out


def results():
    """The unit's JSON: the central's outputs at the top level (the pre-switch keys), (b) and (c)'s high root beside them."""
    e, old, new = rc.worlds()
    out, arrays = scenarios(old, new)
    _, info = m.central()
    res = {"worlds": worlds_label("c"),
           "calibration": {k: info[k] for k in ("tag", "root", "rho", "capital_premium", "multiplier", "headroom_pp", "k")}
                          | {"labor_share_start": float(old["labor_share"][0]), "labour_share_bea_start": float(old["labour_share_bea"][0]),
                             "signal": "labor_share (all wages over income, the machine chain's labour included)",
                             "source": info["source"]},
           **out}
    fig7 = {"note": "noiseless, sigma 1 pp, prior 5%: the market watching the paper's Figure 7 labour share (labour_share_bea) "
                    "instead of all wages over income; a sensitivity of the signal's basis, not a new default",
            "c": signal_fig7(old, new)}
    for name, key in (("b", "comparator_b"), ("c_hi", "sensitivity_c_hi")):
        _, o2, n2 = rc.worlds(calibration=name)
        res[key] = {"worlds": worlds_label(name), **scenarios(o2, n2)[0]}
        fig7[name] = signal_fig7(o2, n2)
    res["sensitivity_signal_fig7"] = fig7
    return res, (old, new, arrays)


def main():
    out, (old, new, arrays) = results()
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    with open(os.path.join(ROOT, "results", "recognition.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, default=str)
    for k, v in out.items():
        if k not in ("recognition_noiseless", "comparator_b", "sensitivity_c_hi"):
            print(k, v)
    for key in ("comparator_b", "sensitivity_c_hi"):
        print(key, {k: v for k, v in out[key].items() if k not in ("recognition_noiseless", "labour_share_pp", "worlds")})
    _, ob, nb = rc.worlds(calibration="b")
    figure(old["t"], old, new, rc.Learning(sigma=1.0, p0=0.05), arrays["zmix"], arrays["jump"], arrays["p"], arrays["cn"],
           arrays["nar"], (ob, nb))


def figure(t, old, new, base, zmix, jump, p, cn, nar, comp):
    ob, nb = comp                                          # calibration (b), the comparator (dashed)
    OLD_C, NEW_C, MARKET = "#52514e", "#eb6834", "#2a78d6"
    RAMP4 = ("#b7d3f6", "#6da7ec", "#2a78d6", "#104281")
    MAT = {"2Y": "#1baf7a", "10Y": "#2a78d6", "30Y": "#eb6834"}
    INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9.5, "axes.edgecolor": GRID,
                         "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
                         "axes.titlesize": 10.5, "axes.titleweight": "bold", "axes.titlecolor": INK,
                         "axes.titlelocation": "left"})
    fig, ax = plt.subplots(2, 3, figsize=(15.5, 8.8), facecolor=SURF)
    for a in ax.flat:
        a.set_facecolor(SURF); a.grid(True, color=GRID, lw=0.8); a.set_axisbelow(True)
        for sp in ("top", "right"):
            a.spines[sp].set_visible(False)
    w = t <= 8
    a = ax[0, 0]
    a.fill_between(t[w], new["labor_share"][w] * 100 - base.sigma, new["labor_share"][w] * 100 + base.sigma, color=NEW_C, alpha=0.15, lw=0)
    a.plot(t[w], old["labor_share"][w] * 100, color=OLD_C, lw=2, label="status quo")
    a.plot(t[w], new["labor_share"][w] * 100, color=NEW_C, lw=2, label="new world (the truth), ± 1 pp noise")
    a.plot(t[w], ob["labor_share"][w] * 100, color=OLD_C, lw=1.2, ls="--", label="calibration (b): status quo, new world")
    a.plot(t[w], nb["labor_share"][w] * 100, color=NEW_C, lw=1.2, ls="--")
    a.set_title("1. What the market watches" + NL + "labour's share of income, two worlds"); a.set_ylabel("%"); a.set_xlabel("years")
    a.legend(frameon=False, fontsize=8.5, labelcolor=INK, loc="lower left")
    a = ax[0, 1]
    for sig, c in zip((0.5, 1.0, 2.0, 4.0), RAMP4):
        a.plot(t[w], rc.learn(old, new, replace(base, sigma=sig))[w], color=c, lw=2, label=f"noise {sig:g} pp")
    a.plot(t[w], rc.learn(ob, nb, base)[w], color=INK2, lw=1.2, ls="--", label="calibration (b), noise 1 pp")
    a.set_title("2. When the market wakes up" + NL + "probability of the new world, prior 5%, noiseless data"); a.set_ylabel("probability"); a.set_xlabel("years")
    a.legend(frameon=False, fontsize=8.5, labelcolor=INK, loc="lower right")
    a = ax[0, 2]
    a.hist(cn, bins=np.arange(0, 8.01, 0.25), color=MARKET, edgecolor=SURF, linewidth=1)
    q = np.percentile(cn, [10, 50, 90])
    a.set_title("3. With noisy data: the date belief crosses one half" + NL + f"500 draws, noise 1 pp; 10/50/90%: {q[0]:.1f} / {q[1]:.1f} / {q[2]:.1f} yrs")
    a.set_xlabel("years"); a.set_ylabel("draws")
    a = ax[1, 0]
    c10, c90 = rc.crossing(t, p, 0.1), rc.crossing(t, p, 0.9)
    yrs = (0.0, np.floor(c10 * 4) / 4 if c10 is not None else 2.0, np.ceil(c90 * 4) / 4 if c90 is not None else 5.0, 10.0)  # around the window
    for yr, c in zip(yrs, RAMP4):
        i = int(np.argmin(np.abs(t - yr)))
        a.plot(T, zmix[i], color=c, lw=2, marker="o", ms=3.5, label=f"year {yr:g}: p = {p[i]:.2f}")
    a.set_xscale("log"); a.set_xticks([1 / 12, 1, 2, 5, 10, 30]); a.set_xticklabels(["1M", "1Y", "2Y", "5Y", "10Y", "30Y"])
    a.set_title("4. The market's curve through recognition" + NL + "noise 1 pp, prior 5%"); a.set_ylabel("zero rate, %")
    a.legend(frameon=False, fontsize=8.5, labelcolor=INK)
    a = ax[1, 1]
    for lab, k in (("2Y", 4), ("10Y", 8), ("30Y", 10)):
        a.plot(t[w], jump[w, k], color=MAT[lab], lw=2, label=lab)
    a.axhline(0, color=INK2, lw=0.8)
    a.set_title("5. The jump still waiting" + NL + "if the truth were revealed that day"); a.set_ylabel("bp"); a.set_xlabel("years")
    a.legend(frameon=False, fontsize=8.5, labelcolor=INK)
    a = ax[1, 2]
    a.plot(t[w], nar["new"]["p"][w], color=NEW_C, lw=2, label="truth: new world")
    a.plot(t[w], nar["old"]["p"][w], color=OLD_C, lw=2, label="truth: status quo — a false dawn")
    a.axvline(1.5, color=INK2, lw=0.8, ls=":")
    a.set_title("6. A narrative shock at year 1.5 (+3 log odds)" + NL + "probability of the new world under each truth"); a.set_ylabel("probability"); a.set_xlabel("years")
    a.legend(frameon=False, fontsize=8.5, labelcolor=INK, loc="center right")
    fig.text(0.01, 0.005, "Worlds: calibration (c) central (open reading, low root), required return following r* from its own rho; new world = capability "
             "1 → 0.04 and lambda to a fifth, medium speed; dashed: calibration (b)." + NL + "Bayesian learning on quarterly labour-share data "
             "(all wages over income). Bridges refit on (c) (Log 46).", fontsize=8, color=INK2)
    fig.tight_layout(rect=(0, 0.035, 1, 1))
    pth = os.path.join(ROOT, "figures", "fig_recognition.png"); fig.savefig(pth, dpi=150, facecolor=SURF); print(pth)


if __name__ == "__main__":
    main()
