# speed_scenarios.py — markets at machine speed: earlier, more abrupt, more fragile.
#
# Her point (2026-09-24): markets run on cognitive labour at a human speed; if AI comes to be trusted
# to guide investment decisions, that bottleneck lifts. Two channels, run separately (recognition.py):
# how much the market reads (capacity: recognition comes earlier) and how fast it prices what it has
# read (digestion: news gaps instead of drifting). Plus a failure mode: readings that share one model's
# error, which a market unaware of it takes for independent confirmation.
#
# Worlds: calibration (c)'s central economy (her decision, 2026-09-30; macro.central(): the open (domp) reading, the low
# root in k), the return following r* from its own rho (macro.feedback_bridges; the bridges read at the start's required
# return, decision 96), status quo (macro.hold_tech) vs medium
# deep automation relative to its own lambda (macro.deep_tech), on a weekly grid; bridges refit on (c) (Log 46), in the two
# branches of the reverse stress's finding that two bridges decide direction (macro.BRANCHES: "deficits dominate" and
# "owners' saving dominates", the direction bridges at the ends of their evidence ranges). The same unit on (b), the
# pre-switch calibration, is stored as comparator_b (the pre-switch results/speed.json: on macro.BRIDGES_B and BRANCHES_B,
# the branches as set on (b), the helpers give (b)'s hard-coded objects exactly). 0_worlds records each world pair's recognition window, the 10Y's move through it and the
# largest rise in the required return against the central's rate headroom (beyond it solve raises NoEquilibrium; no run
# here comes near it). Today's market: sigma 1 pp per quarterly reading, prior 5%. Digestion: for news
# about a regime — a judgement, not a number — a human market's half-life is assumed a quarter (0.1 and
# 0.5 shown); for comparison, the one rung measured (code/digestion_history.py): US 10Y rate news in
# 1982–94, three quarters priced at once and the rest with a half-life of about two weeks; since 1995
# rate news shows no drift at all.
#
# Provenance: the economy from results/calibration_c.json (BEA; code/calibration_c.py, gated by
# checks/check_calibration_c.py). Gated by checks/check_speed.py.
# Run from paths/:  ../venv/Scripts/python.exe code/speed_scenarios.py   (about three minutes: the central and (b))
# Out: results/speed.json, figures/fig_speed.png

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
import macro as m  # noqa: E402
import recognition as rc  # noqa: E402
import regimes as rg  # noqa: E402

NL = chr(10)
DT = 1 / 52
T = np.array([0.25, 2.0, 10.0, 30.0])
LAB = ("3M", "2Y", "10Y", "30Y")
HUMAN = rc.Learning(sigma=1.0, p0=0.05, digest=0.25)
CAPS = (1, 3, 10, 30, 100)
SCEN = m.BRANCHES                    # the two branches on the refit; (b)'s comparator runs m.BRANCHES_B on m.BRIDGES_B
EVENT_T, EVENT_D = 1.5, 4.0          # a lump of evidence: +4 log odds at year 1.5 (a demonstration, a data revision)
MEASURED_H, MEASURED_SHARE = 9.8 / 252, 0.25    # US 10Y, 1982-94 (results/digestion_history.json)


def worlds(e, base=None, **bridges):
    br = m.feedback_bridges(e, base=base, **bridges)
    old = m.macro_path(e, m.hold_tech(e), br, 25.0, 0.25)
    new = m.macro_path(e, m.deep_tech(e), br, 25.0, 0.25)
    return rc.refine(old, DT), rc.refine(new, DT)


def curves(ow, nw, p):
    mixes, _, _, pol = rc.market_curves(ow, nw, p)
    return np.array([rg.zero(T, mx) for mx in mixes]) * 100, pol


def after(t, z, t0, weeks):
    """The curve's move from the week before t0 to `weeks` weeks after it (bp, per maturity)."""
    i0 = int(np.searchsorted(t, t0)) - 1
    return z[i0 + weeks] - z[i0]


def r2(x, nd: int = 2):
    """round(x, nd), or None if x is None (a belief that never crosses the level)."""
    return None if x is None else round(x, nd)


def world_readouts(e, W):
    """Each world pair under today's human market: the recognition window, the 10Y through it and over ten years, and the
    largest rise in the new world's required return (the headroom is the central's; (b) has 20 pp and more). A world pair
    the market never recognises within the run stores None for the window and the move through it."""
    out = {}
    for sname, (o, n) in W.items():
        t = o["t"]
        p = rc.learn(o, n, HUMAN)
        z, _ = curves(o, n, p)
        c10, c90 = rc.crossing(t, p, 0.1), rc.crossing(t, p, 0.9)
        through = None
        if c10 is not None and c90 is not None:
            i10, i90 = max(int(np.searchsorted(t, c10)) - 1, 0), int(np.searchsorted(t, c90))
            through = round(float(z[i90, 2] - z[i10, 2]), 1)
        w = t <= 15.0 + 1e-9
        out[sname] = {"window": [r2(c10), r2(c90)], "10Y_through_recognition_bp": through,
                      "10Y_over_ten_years_bp": round(float(z[int(np.argmin(np.abs(t - 10.0))), 2] - z[0, 2]), 1),
                      "10Y_max_rise_fall_15y_bp": [round(float((z[w, 2] - z[0, 2]).max()), 1), round(float((z[w, 2] - z[0, 2]).min()), 1)],
                      "required_return_rise_max_pp": round(float(n["rho"].max() - n["rho"][0]), 3)}
    return out


def main():
    e, info = m.central()
    out, fig_in = compute(e)
    out = {"calibration": {k: info[k] for k in ("tag", "root", "rho", "capital_premium", "headroom_pp", "k", "source")}, **out}
    eb, _, _, _ = m.calibrate(base=m.CAPITAL_BASE)
    out["comparator_b"] = compute(eb, m.BRIDGES_B, m.BRANCHES_B)[0]
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    with open(os.path.join(ROOT, "results", "speed.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
    for k, v in out.items():
        print(k)
        if isinstance(v, dict):
            for kk, vv in v.items():
                print("  ", kk, vv if k != "comparator_b" else str(vv)[:300])
    figure(*fig_in, out["comparator_b"])


def compute(e, base=None, scen=None):
    """The unit's outputs on one economy (base bridges and branches: default the refit's; (b) passes macro.BRIDGES_B and
    macro.BRANCHES_B), and what the figure draws."""
    W = {k: worlds(e, base, **v) for k, v in (SCEN if scen is None else scen).items()}
    ow, nw = W["deficits dominate"]
    t = ow["t"]
    ls = nw["labor_share"]
    out = {"assumptions": {"sigma_pp_per_quarter": 1.0, "prior": 0.05, "human_digest_halflife_years": 0.25,
                           "grid": "weekly", "event": f"+{EVENT_D:g} log odds at year {EVENT_T:g}",
                           "signal": "labor_share: all wages over income (recognition.Learning's default), not the Figure 7 basis"}}
    out["0_worlds"] = world_readouts(e, W)
    # 1. earlier: capacity grows with trust; trust follows the economy's automation, or leads it
    earlier, beliefs = {}, {}
    for lead in (0.0, 3.0):
        for c in CAPS:
            lr = replace(HUMAN, capacity_end=c, trust_lead=lead)
            p = rc.learn(ow, nw, lr)
            cs = [rc.crossing(t, p, L) for L in (0.1, 0.5, 0.9)]
            i = int(np.searchsorted(t, cs[1])) if cs[1] is not None else None
            earlier[f"lead {lead:g}, capacity {c}"] = {
                "p_0.1": r2(cs[0]), "p_0.5": r2(cs[1]), "p_0.9": r2(cs[2]),
                "window_weeks": round((cs[2] - cs[0]) * 52, 1) if None not in (cs[0], cs[2]) else None,
                "fall_done_at_0.5": round(float((ls[0] - ls[i]) / (ls[0] - ls[-1])), 3) if i is not None else None,
                "trust_at_0.5": round(float(rc.trust_path(ow, nw, lr)[i]), 3) if i is not None else None,
                "capacity_at_0.5": round(float(rc.capacity_path(ow, nw, lr)[i]), 2) if i is not None else None}
            beliefs[(lead, c)] = p
    out["1_earlier"] = earlier
    # 2. abrupt: digestion alone (reading unchanged), a lump of evidence before recognition
    digests = {"human, regime news (assumed)": (0.25, 1.0), "1980s rate news (measured)": (MEASURED_H, MEASURED_SHARE),
               "x3": (0.25 / 3, 1.0), "x10": (0.25 / 10, 1.0), "x30": (0.25 / 30, 1.0), "x100": (0.25 / 100, 1.0),
               "instant": (0.0, 1.0)}
    abrupt, event_paths = {}, {}
    for sname, (o, n) in W.items():
        abrupt[sname] = {}
        for dname, (h, sh) in digests.items():
            p = rc.learn(o, n, replace(HUMAN, digest=h, digest_share=sh, jumps=((EVENT_T, EVENT_D),)))
            p0 = rc.learn(o, n, replace(HUMAN, digest=h, digest_share=sh))
            z, pol = curves(o, n, p)
            z0, _ = curves(o, n, p0)
            ev = z - z0                                   # the event's own effect, net of background learning
            abrupt[sname][dname] = {f"{w}w": {lab: round(float(after(t, ev, EVENT_T, w)[k]), 1) for k, lab in enumerate(LAB)}
                                    for w in (1, 4, 13)}
            event_paths[(sname, dname)] = (ev, pol)
    out["2_abrupt_event_effect_bp"] = abrupt
    # sensitivity of the human baseline
    sens = {}
    for h in (0.1, 0.25, 0.5):
        p = rc.learn(ow, nw, replace(HUMAN, digest=h, jumps=((EVENT_T, EVENT_D),)))
        p0 = rc.learn(ow, nw, replace(HUMAN, digest=h))
        ev = curves(ow, nw, p)[0] - curves(ow, nw, p0)[0]
        sens[f"digest {h:g}"] = {f"{w}w": round(float(after(t, ev, EVENT_T, w)[2]), 1) for w in (1, 4, 13)}
    out["2b_human_baseline_sensitivity_10Y_bp"] = sens
    # 3. fragile: AI in use whatever the world (trust 1), readings sharing an error of 0.5 pp
    seeds = range(300)
    horizon = t <= 15.0 + 1e-9
    fragile = {}
    for aware in (True, False):
        for c in CAPS:
            lr = replace(HUMAN, trust=1.0, capacity_end=c, common=0.5, aware=aware)
            fd, pmax, cross = 0, [], []
            for sd in seeds:
                po = rc.learn(ow, nw, replace(lr, truth="old", seed=10_000 + sd))[horizon]
                fd += bool(po.max() >= 0.5)
                pmax.append(po.max())
                pn = rc.learn(ow, nw, replace(lr, seed=sd))[horizon]
                cross.append(rc.crossing(t[horizon], pn, 0.5))
            cn = np.array([x for x in cross if x is not None])
            fragile[f"{'aware' if aware else 'unaware'}, capacity {c}"] = {
                "false_dawn_share": fd / len(seeds), "median_peak_belief_status_quo": round(float(np.median(pmax)), 3),
                "true_recognition_p0.5_10_50_90": [round(float(q), 2) for q in np.percentile(cn, [10, 50, 90])] if len(cn) else None}
    out["3_fragile"] = fragile
    return out, (t, ow, nw, beliefs, event_paths, abrupt, fragile)


def figure(t, ow, nw, beliefs, event_paths, abrupt, fragile, comp):
    INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
    RAMP = {1: "#b7d3f6", 3: "#6da7ec", 10: "#2a78d6", 30: "#1a5bb0", 100: "#104281"}
    DRAMP = {"human, regime news (assumed)": "#b7d3f6", "x10": "#6da7ec", "1980s rate news (measured)": "#b9b8b3",
             "x100": "#2a78d6", "instant": "#104281"}
    SHORT = {"human, regime news (assumed)": "human," + NL + "regime news", "1980s rate news (measured)": "1980s," + NL + "rate news",
             "x10": "x10", "x100": "x100", "instant": "instant"}
    MAT = {"3M": "#b9b8b3", "2Y": "#1baf7a", "10Y": "#2a78d6", "30Y": "#eb6834"}
    AWARE, UNAWARE = "#2a78d6", "#e34948"
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9.5, "axes.edgecolor": GRID,
                         "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
                         "axes.titlesize": 10.5, "axes.titleweight": "bold", "axes.titlecolor": INK,
                         "axes.titlelocation": "left"})
    fig, ax = plt.subplots(2, 3, figsize=(16, 9.4), facecolor=SURF, layout="constrained")
    fig.get_layout_engine().set(rect=(0, 0.04, 1, 0.96), h_pad=0.12, w_pad=0.1)
    for a in ax.flat:
        a.set_facecolor(SURF); a.grid(True, color=GRID, lw=0.8); a.set_axisbelow(True)
        for sp in ("top", "right"):
            a.spines[sp].set_visible(False)
    w = t <= 8
    # 1. trust and the labour share
    a = ax[0, 0]
    ls = nw["labor_share"]
    a.plot(t[w], (ls[0] - ls[w]) / (ls[0] - ls[-1]), color=INK2, lw=2, label="labour-share fall, share done")
    for lead, sty in ((0.0, "-"), (3.0, "--")):
        a.plot(t[w], rc.trust_path(ow, nw, replace(HUMAN, trust_lead=lead))[w], color="#eb6834", lw=2, ls=sty,
               label=f"trust in AI: {'with the economy' if lead == 0 else 'finance 3 years ahead'}")
    cx = {key: rc.crossing(t, beliefs[key], 0.5) for key in ((0.0, 1), (3.0, 100))}
    cx = {k: (v if v is not None else float(t[w][-1])) for k, v in cx.items()}     # never past one half: the panel's edge
    for c in cx.values():
        a.axvline(c, color=INK2, lw=0.8, ls=":")
    first, last = sorted(cx, key=cx.get)                  # one label, right of the later line, naming both
    name = {(0.0, 1): "today's market", (3.0, 100): "x100, finance ahead"}
    a.text(cx[last] + 0.08, 1.115, "dotted: belief crosses 1/2 —" + NL + f"{name[first]} (left), {name[last]} (right)", fontsize=8,
           color=INK2, va="top", ha="left")
    a.set_title("1. Recognition comes before the AI is trusted" + NL + "unless finance adopts ahead of the economy")
    a.set_xlabel("years"); a.set_ylim(-0.02, 1.12)                # headroom above 1 for the label
    a.legend(frameon=False, fontsize=8, labelcolor=INK, loc="upper left", bbox_to_anchor=(0.0, 0.82))
    # 2. beliefs
    a = ax[0, 1]
    for c in CAPS:
        a.plot(t[w], beliefs[(3.0, c)][w], color=RAMP[c], lw=2, label=f"capacity x{c}")
    a.plot(t[w], beliefs[(0.0, 100)][w], color=RAMP[100], lw=1.5, ls=":", label="x100, trust with the economy")
    a.set_title("2. More reading: recognition earlier, not sharper" + NL + "belief in the new world; finance 3 years ahead")
    a.set_xlabel("years"); a.set_ylabel("probability")
    a.legend(frameon=False, fontsize=8, labelcolor=INK, loc="lower right")
    # 3. the event, 10Y, by digestion speed
    a = ax[0, 2]
    i0 = int(np.searchsorted(t, EVENT_T)) - 1
    wk = np.arange(-4, 27)
    for dname, col in DRAMP.items():
        ev, _ = event_paths[("deficits dominate", dname)]
        a.plot(wk, ev[i0 + wk, 2] - ev[i0, 2], color=col, lw=2, label=dname, ls="--" if "1980s" in dname else "-")
    a.axvline(0, color=INK2, lw=0.8, ls=":")
    a.set_title("3. Faster digestion: the same news gaps" + NL + f"10Y, +{EVENT_D:g} log odds at year {EVENT_T:g}; deficits dominate")
    a.set_xlabel("weeks from the news"); a.set_ylabel("bp")
    a.legend(frameon=False, fontsize=8, labelcolor=INK, title="digestion speed", title_fontsize=8, loc="lower right")
    # 4. the week of the news, by maturity
    a = ax[1, 0]
    names = list(DRAMP)
    x = np.arange(len(names))
    for k, lab in enumerate(LAB):
        a.bar(x + (k - 1.5) * 0.2, [abrupt["deficits dominate"][d]["1w"][lab] for d in names], 0.19, color=MAT[lab], label=lab)
    a.axhline(0, color=INK2, lw=0.8)
    a.set_xticks(x); a.set_xticklabels([SHORT[d] for d in names], fontsize=8.5)
    a.set_title("4. In the week of the news the front waits" + NL + "policy moves at meetings: the long end gaps alone")
    a.set_ylabel("bp in one week"); a.legend(frameon=False, fontsize=8, labelcolor=INK, ncol=4, loc="upper left")
    # 5. hedging lag
    a = ax[1, 1]
    for k, (win, lab) in enumerate(((1, "1 week"), (4, "1 month"), (13, "1 quarter"))):
        for s, (sname, hatch) in enumerate((("deficits dominate", None), ("owners' saving dominates", "//"))):
            vals = [abs(abrupt[sname][d][f"{win}w"]["10Y"]) for d in names]
            a.bar(x + (k - 1) * 0.27 + (s - 0.5) * 0.12, vals, 0.12, color=("#b7d3f6", "#2a78d6", "#104281")[k],
                  hatch=hatch, edgecolor=SURF, label=f"within {lab}" if s == 0 else None)
    a.set_xticks(x); a.set_xticklabels([SHORT[d] for d in names], fontsize=8.5)
    a.set_title("5. What a bank deciding monthly must absorb" + NL + "|10Y move| within each window; hatched: saving dominates")
    a.set_ylabel("bp"); a.legend(frameon=False, fontsize=8, labelcolor=INK, loc="upper left")
    # 6. fragility
    a = ax[1, 2]
    for aware, col in ((True, AWARE), (False, UNAWARE)):
        fd = [fragile[f"{'aware' if aware else 'unaware'}, capacity {c}"]["false_dawn_share"] * 100 for c in CAPS]
        a.plot(CAPS, fd, color=col, lw=2, marker="o", ms=5,
               label="knows its readings share an error" if aware else "takes them for independent confirmation")
        fb = [comp["3_fragile"][f"{'aware' if aware else 'unaware'}, capacity {c}"]["false_dawn_share"] * 100 for c in CAPS]
        a.plot(CAPS, fb, color=col, lw=1.1, ls="--", label="calibration (b), the pre-switch run" if not aware else None)
    a.set_xscale("log"); a.set_xticks(CAPS); a.set_xticklabels([f"x{c}" for c in CAPS])
    a.set_title("6. Faster, and easier to fool" + NL + "false dawns under the status quo, 300 draws")
    a.set_xlabel("capacity (AI trusted throughout)"); a.set_ylabel("% of draws with belief ever past 1/2")
    a.legend(frameon=False, fontsize=8, labelcolor=INK, loc="upper left")
    fig.text(0.01, 0.005, "Calibration (c), central (open reading, low root), the return following r*; status quo vs medium deep automation; weekly grid. "
             "Today's market: 1 pp noise per quarterly reading, prior 5%;" + NL + "regime news digested with half-life a quarter (assumed); 1980s rate "
             "news as measured. Shared error 0.5 pp (panel 6; dashed: calibration (b)). Bridges refit on (c) (Log 46).", fontsize=8, color=INK2)
    pth = os.path.join(ROOT, "figures", "fig_speed.png"); fig.savefig(pth, dpi=150, facecolor=SURF); print(pth)


if __name__ == "__main__":
    main()
