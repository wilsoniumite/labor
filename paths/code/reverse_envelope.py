# reverse_envelope.py — reverse stress testing, part 1: 4,000 draws over the dials.
#
# Latin-hypercube draws over reverse.RANGES (broad stated ranges, not estimates; scale dials in logs). For each draw: the
# two-world recognition model on calibration (b). Reported: the envelope of curve moves — across the
# recognition window and over ten years — and of macro outcomes; which dials drive them (Spearman rank
# correlations); the extreme draws; and the most plausible draws (nearest the defaults in the unit cube)
# that reach a +100 bp or a -100 bp move in the 10Y at any point.
#
# Run from paths/:  ../venv/Scripts/python.exe code/reverse_envelope.py
# Out: results/reverse_envelope.json, figures/fig_reverse_envelope.png

from __future__ import annotations

import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import macro as m  # noqa: E402
import reverse as rv  # noqa: E402

N = 4000
NL = chr(10)
OUTCOMES = ("recog_10Y", "max_up_10Y", "max_down_10Y", "ten_year_2Y", "debt_max", "real_wage_min_rel")


def main():
    e, _, _, _ = m.calibrate(base=m.CAPITAL_BASE)
    U = rv.sample(N)
    rows, ok = [], []
    for u in U:
        try:
            rows.append(rv.run(e, rv.from_unit(u)))
            ok.append(True)
        except (ValueError, AssertionError):
            ok.append(False)
    ok = np.array(ok)
    U = U[ok]
    R = {k: np.array([r[k] if r[k] is not None else np.nan for r in rows]) for k in rows[0]}
    du = rv.to_unit(rv.Dials())
    out = {"draws": N, "solved": int(ok.sum()), "ranges": rv.RANGES}
    out["envelope"] = {k: {"p5": round(float(np.nanpercentile(R[k], 5)), 2), "p50": round(float(np.nanpercentile(R[k], 50)), 2),
                           "p95": round(float(np.nanpercentile(R[k], 95)), 2), "min": round(float(np.nanmin(R[k])), 2),
                           "max": round(float(np.nanmax(R[k])), 2)}
                       for k in ("recog_2Y", "recog_10Y", "recog_30Y", "ten_year_3M", "ten_year_2Y", "ten_year_10Y",
                                 "max_up_10Y", "max_down_10Y", "max_jump_10Y", "c50", "debt_max", "real_wage_min_rel",
                                 "shelter_infl_max", "policy_min", "policy_max")}
    drivers = {}
    for o in OUTCOMES:
        y = R[o]
        good = np.isfinite(y)
        drivers[o] = {k: round(rv.rank_corr(U[good, j], y[good]), 2) for j, k in enumerate(rv.NAMES)}
    out["drivers_rank_corr"] = drivers
    picks = {}
    for name, key, thr in (("most plausible +100 bp 10Y", "max_up_10Y", 100.0), ("most plausible -100 bp 10Y", "max_down_10Y", -100.0),
                           ("most plausible +50 bp 10Y in the recognition window", "recog_10Y", 50.0)):
        j, dist = rv.nearest_breach(U, np.nan_to_num(R[key]), thr, du)
        if j is not None:
            d = rv.from_unit(U[j])
            moved = {k: [round(getattr(rv.Dials(), k), 3), round(getattr(d, k), 3)] for k in rv.NAMES
                     if abs(U[j][rv.NAMES.index(k)] - du[rv.NAMES.index(k)]) > 0.15}
            picks[name] = {"distance": round(dist, 3), "value": round(float(R[key][j]), 1), "dials_moved_default_to_draw": moved, "_j": j}
        else:
            picks[name] = None
    jb, jl = int(np.nanargmax(R["max_up_10Y"])), int(np.nanargmin(R["max_down_10Y"]))
    picks["largest 10Y rise"] = {"value": round(float(R["max_up_10Y"][jb]), 1), "_j": jb}
    picks["largest 10Y fall"] = {"value": round(float(R["max_down_10Y"][jl]), 1), "_j": jl}
    out["picks"] = {k: ({kk: vv for kk, vv in v.items() if kk != "_j"} if v else None) for k, v in picks.items()}
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, "results", "reverse_envelope.json"), "w", encoding="utf-8"), indent=1, default=str)
    print(f"solved {out['solved']}/{N}")
    for k in ("recog_10Y", "ten_year_10Y", "max_up_10Y", "max_down_10Y", "max_jump_10Y", "c50", "debt_max", "real_wage_min_rel"):
        print(f"  {k:18s}", out["envelope"][k])
    for o in OUTCOMES:
        top = sorted(drivers[o].items(), key=lambda kv: -abs(kv[1]))[:4]
        print(f"  drivers of {o:18s}", top)
    for k, v in out["picks"].items():
        print(" ", k, v)
    figure(e, U, R, drivers, picks)


def figure(e, U, R, drivers, picks):
    INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
    BLUE, RED, NEUTRAL = "#2a78d6", "#e34948", "#f0efec"
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9.5, "axes.edgecolor": GRID,
                         "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
                         "axes.titlesize": 10.5, "axes.titleweight": "bold", "axes.titlecolor": INK,
                         "axes.titlelocation": "left"})
    fig = plt.figure(figsize=(17.5, 10.2), facecolor=SURF, layout="constrained")
    fig.get_layout_engine().set(rect=(0, 0.025, 1, 0.975), h_pad=0.12, w_pad=0.1)
    gs = fig.add_gridspec(2, 3, width_ratios=[1, 1, 1.35])
    ax1, ax2, ax3 = fig.add_subplot(gs[0, 0]), fig.add_subplot(gs[0, 1]), fig.add_subplot(gs[:, 2])
    ax4, ax5 = fig.add_subplot(gs[1, 0]), fig.add_subplot(gs[1, 1])
    for a in (ax1, ax2, ax3, ax4, ax5):
        a.set_facecolor(SURF)
        for sp in ("top", "right"):
            a.spines[sp].set_visible(False)
    for a in (ax1, ax2, ax4, ax5):
        a.grid(True, color=GRID, lw=0.8); a.set_axisbelow(True)
    a = ax1
    a.hist(R["recog_10Y"][np.isfinite(R["recog_10Y"])], bins=60, color=BLUE, edgecolor=SURF, linewidth=0.6)
    a.axvline(0, color=INK2, lw=0.8)
    a.set_title("1. The 10Y move while the market wakes up" + NL + "4,000 draws over the dials"); a.set_xlabel("bp"); a.set_ylabel("draws")
    a = ax2
    up, dn = R["max_up_10Y"], R["max_down_10Y"]
    a.hist(up[up > 0.5], bins=50, color=RED, edgecolor=SURF, linewidth=0.6, alpha=0.9, label="largest rise")
    a.hist(dn[dn < -0.5], bins=50, color=BLUE, edgecolor=SURF, linewidth=0.6, alpha=0.9, label="largest fall")
    a.axvline(0, color=INK2, lw=0.8)
    a.set_title("2. The 10Y's largest rise and fall over 15 years" + NL
                + f"never rises in {np.mean(up <= 0.5) * 100:.0f}% of draws, never falls in {np.mean(dn >= -0.5) * 100:.0f}%"); a.set_xlabel("bp"); a.set_ylabel("draws")
    a.legend(frameon=False, fontsize=8.5, labelcolor=INK)
    a = ax3
    M = np.array([[drivers[o][k] for o in OUTCOMES] for k in rv.NAMES])
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list("div", [BLUE, NEUTRAL, RED])
    a.imshow(M, cmap=cmap, vmin=-1, vmax=1, aspect="auto")
    a.set_xticks(range(len(OUTCOMES)))
    a.set_xticklabels([f"10Y{NL}recog.", f"10Y{NL}max rise", f"10Y{NL}max fall", f"2Y{NL}10 yrs", f"debt{NL}peak", f"wage{NL}low"], fontsize=8.5)
    a.set_yticks(range(len(rv.NAMES)))
    a.set_yticklabels(["automation depth (eta end)", "automation width (yrs)", "automation midpoint (yr)", "build-out -> r*",
                       "owners' saving -> r*", "deficits -> r*", "term premium per debt", "debt threshold",
                       "public support share", "capital premium", "data noise", "prior belief"], fontsize=8.5)
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            a.text(j, i, f"{M[i, j]:+.2f}", ha="center", va="center", fontsize=8, color=INK)
    a.set_title("3. What drives the outcomes" + NL + "rank correlation, dial against outcome")
    a.yaxis.tick_right()
    a.tick_params(length=0)
    for sp in a.spines.values():
        sp.set_visible(False)
    a = ax4
    Cs = {"most plausible +100 bp 10Y": RED, "most plausible -100 bp 10Y": BLUE, "largest 10Y rise": "#eb6834", "largest 10Y fall": "#104281"}
    for name, c in Cs.items():
        pk = picks.get(name)
        if not pk:
            continue
        o = rv.run(e, rv.from_unit(U[pk["_j"]]), keep_paths=True)["_paths"]
        a.plot(o["t"], (o["z"][:, 2] - o["z"][0, 2]) * 100, color=c, lw=2, label=f"{name} ({pk['value']:+.0f})")
    base = rv.run(e, rv.Dials(), keep_paths=True)["_paths"]
    a.plot(base["t"], (base["z"][:, 2] - base["z"][0, 2]) * 100, color=INK2, lw=1.6, ls="--", label="default dials")
    a.axhline(0, color=INK2, lw=0.8)
    a.set_title("4. The 10Y path in selected draws" + NL + "change from the start"); a.set_xlabel("years"); a.set_ylabel("bp")
    a.set_ylim(-380, 720)
    a.legend(frameon=False, fontsize=8, labelcolor=INK, loc="upper left", ncol=2)
    a = ax5
    sc = a.scatter(R["real_wage_min_rel"], R["debt_max"], c=np.clip(R["ten_year_10Y"], -200, 200), cmap=cmap, vmin=-200, vmax=200, s=6, lw=0)
    a.set_title("5. The macro envelope" + NL + "colour: the 10Y's move over ten years"); a.set_xlabel("real wage low point, share of start")
    a.set_ylabel("public debt peak, % of income")
    cb = fig.colorbar(sc, ax=a, fraction=0.05, pad=0.02); cb.set_label("bp", color=INK2); cb.outline.set_visible(False)
    fig.text(0.01, 0.005, "Two-world recognition model on calibration (b). Dials drawn by Latin hypercube over broad stated ranges (reverse.RANGES), "
             "not estimates; 'most plausible' = nearest the defaults in the unit cube among draws reaching the threshold. "
             "The pile near -325 bp in panel 2 is the lower bound: expected policy cannot go below -0.5%.", fontsize=8, color=INK2)
    pth = os.path.join(ROOT, "figures", "fig_reverse_envelope.png"); fig.savefig(pth, dpi=150, facecolor=SURF); print(pth)


if __name__ == "__main__":
    main()
