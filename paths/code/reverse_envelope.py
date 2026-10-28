# reverse_envelope.py — reverse stress testing, part 1: 4,000 draws over the dials.
#
# Latin-hypercube draws over reverse.RANGES (broad stated ranges, not estimates; scale dials in logs). For each draw: the
# two-world recognition model. Reported: the envelope of curve moves — across the recognition window and over ten years —
# and of macro outcomes; which dials drive them (Spearman rank correlations); the extreme draws; and the most plausible
# draws (nearest the defaults in the unit cube) that reach a +100 bp or a -100 bp move in the 10Y at any point. Each
# most-plausible pick lists the dials it moves by more than 0.15 of their range (a description of the draw) and, separately,
# what its breach needs, found by re-running it with dial subsets (reverse.attribute) — a dial moved by less than the
# listing's 0.15 can carry the breach, so the listing is never read as the cause.
#
# CALIBRATION (her decision, 2026-09-30). The draws run on calibration (c)'s central economy, macro.central() — the open
# (domp) reading, the low root in k — and the same draws on (b), the pre-switch calibration, as the comparator
# (comparator_b: the pre-switch results/reverse_envelope.json, the premium dial renamed; reverse.py's header says how the
# dials are relative to the economy). The capital-premium dial is a shift of +-2 pp from the economy's own premium (6.80 pp
# on the central, 5.0 on (b)). Since the refit (2026-10-27, Log 46; decision 77) the central's bridge dials are the refit's
# (rv.Dials: alpha_inv, owners' saving and deficits over the evidence's ranges), (b)'s stay its own (rv.DialsB, the ranges
# set around (b)'s defaults): the same unit draws, so comparator_b is the pre-refit envelope exactly. Revised 2026-10-28 (Log 54;
# decision 93): alpha_inv draws the investment key's pass-through, netted (0) to gross (1, the default); the central's block alone
# also stores the shares by thirds of the pass-through (shares_by_investment_pass_through) and the required return's peak above
# the economy's own rho (rho_above_economy), so comparator_b keeps its keys. A draw whose required return climbs past the central's rate headroom has a date with no
# land-scarce equilibrium: it is caught (macro.NoEquilibrium), counted, dated (reverse.first_failure) and its dials
# profiled against the solved draws — not dropped silently — and the envelope is stated as conditional on solving. Any other
# failure is counted separately.
#
# Provenance: the economy from results/calibration_c.json (BEA; code/calibration_c.py, gated by
# checks/check_calibration_c.py). Gated by checks/check_reverse.py.
# Run from paths/:  ../venv/Scripts/python.exe code/reverse_envelope.py   (about five minutes: 2 x 4,000 draws)
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
ENVELOPE = ("recog_2Y", "recog_10Y", "recog_30Y", "ten_year_3M", "ten_year_2Y", "ten_year_10Y", "max_up_10Y", "max_down_10Y",
            "max_jump_10Y", "c50", "debt_max", "real_wage_min_rel", "shelter_infl_max", "policy_min", "policy_max", "rho_rise_max_pp")
FLOOR = m.ELB                     # the effective lower bound (macro.ELB: macro.Recognition.elb)
LISTED = 0.15                     # a pick lists the dials it moves by more than this share of their range: a listing, not the cause
PICKS_NOTE = ("dials_moved_default_to_draw lists the dials a pick moves by more than 0.15 of their range: a description of the "
              "draw, not the cause of its outcome. cause_by_subset (reverse.attribute) re-runs the draw with dial subsets: only the "
              "two direction bridges (alpha_rent, alpha_fiscal) moved from the defaults, those two reset to the defaults in the draw, "
              "only the listed dials moved, each dial reset alone; 'needed' names the dials whose reset alone loses the breach.")


def draws(e, U, cls=rv.Dials):
    """Run every draw in dial space cls (rv.Dials, the refit's; rv.DialsB, (b)'s); (rows of the solved draws, their unit
    points, the failures)."""
    rows, ok, no_eq, other = [], [], [], []
    for j, u in enumerate(U):
        d = rv.from_unit(u, cls)
        try:
            rows.append(rv.run(e, d))
            ok.append(j)
        except m.NoEquilibrium:
            f = rv.first_failure(e, d)
            no_eq.append({"draw": j, "world": f["world"] if f else None, "year": f["year"] if f else None})
        except (ValueError, AssertionError) as ex:
            other.append({"draw": j, "error": f"{type(ex).__name__}: {ex}"})
    return rows, np.array(ok, dtype=int), no_eq, other


def envelope(e, U, cls=rv.Dials):
    """The envelope's JSON block for one economy in dial space cls, and what the figure draws."""
    NAMES = rv.space(cls)[0]
    rows, ok, no_eq, other = draws(e, U, cls)
    Uk = U[ok]
    R = {k: np.array([r[k] if r[k] is not None else np.nan for r in rows]) for k in rows[0]}
    du = rv.to_unit(cls())
    out = {"draws": len(U), "solved": int(len(ok)), "no_equilibrium": len(no_eq), "other_failures": len(other)}
    fail = np.zeros(len(U), dtype=bool)
    fail[[f["draw"] for f in no_eq]] = True
    out["no_equilibrium_detail"] = {
        "draws": no_eq, "other": other,
        "within_reported_horizon": int(sum(1 for f in no_eq if f["year"] is not None and f["year"] <= 15.0)),
        "dial_mean_unit_failed_vs_all": ({k: [round(float(U[fail, j].mean()), 3), round(float(U[:, j].mean()), 3)] for j, k in enumerate(NAMES)}
                                         if fail.any() else None),
        "dial_rank_corr_with_failure": ({k: round(rv.rank_corr(U[:, j], fail.astype(float)), 3) for j, k in enumerate(NAMES)}
                                        if fail.any() else None),
        "note": "the envelope below is over the solved draws only (conditional on a land-scarce equilibrium at every date)"}
    out["envelope"] = {k: {"p5": round(float(np.nanpercentile(R[k], 5)), 2), "p50": round(float(np.nanpercentile(R[k], 50)), 2),
                           "p95": round(float(np.nanpercentile(R[k], 95)), 2), "min": round(float(np.nanmin(R[k])), 2),
                           "max": round(float(np.nanmax(R[k])), 2)} for k in ENVELOPE}
    up, dn = R["max_up_10Y"], R["max_down_10Y"]
    out["shares"] = {"10Y_never_rises": round(float(np.mean(up <= 0.5)), 4), "10Y_never_falls": round(float(np.mean(dn >= -0.5)), 4),
                     "policy_reaches_floor": round(float(np.mean(R["policy_min"] <= FLOOR + 1e-9)), 4),
                     "ten_year_10Y_negative": round(float(np.mean(R["ten_year_10Y"] < 0)), 4),
                     "never_recognised_c50": round(float(np.mean(~np.isfinite(R["c50"]))), 4)}
    if cls is rv.Dials:          # the refit's space only, so comparator_b keeps its keys (decision 93; Log 54)
        u = Uk[:, NAMES.index("alpha_inv")]                    # the investment key's pass-through: its unit draw (0 netted, 1 gross)
        thirds = {"0 to 1/3": u < 1 / 3, "1/3 to 2/3": (u >= 1 / 3) & (u < 2 / 3), "2/3 to 1": u >= 2 / 3}
        out["shares_by_investment_pass_through"] = {
            "note": "the shares of the solved draws by thirds of the investment key's pass-through (the alpha_inv dial's unit draw: "
                    "0 the investment fall netted against capital consumption, 1 gross): the 10Y lower after ten years, lower across "
                    "the recognition window, and never rising (largest rise at most 0.5 bp)",
            **{k: {"draws": int(msk.sum()), "ten_year_10Y_negative": round(float(np.mean(R["ten_year_10Y"][msk] < 0)), 4),
                   "recog_10Y_negative": round(float(np.mean(R["recog_10Y"][msk] < 0)), 4),
                   "10Y_never_rises": round(float(np.mean(up[msk] <= 0.5)), 4)} for k, msk in thirds.items()}}
        ra = R["rho_above_economy_max_pp"]
        ja = int(np.nanargmax(ra))
        da = rv.from_unit(Uk[ja], cls)
        out["rho_above_economy"] = {
            "note": "the required return's peak over the 15 years above the economy's own rho (reverse.run's rho_above_economy_max_pp: "
                    "a draw's own rise plus its premium_shift), against the central's rate headroom at its start; draw: the index in "
                    "rv.sample(N)",
            "max": round(float(ra[ja]), 2), "p95": round(float(np.nanpercentile(ra, 95)), 2), "draw": int(ok[ja]),
            "premium_shift": round(float(da.premium_shift), 3), "rise_above_own_start": round(float(R["rho_rise_max_pp"][ja]), 2)}
    drivers = {}
    for o in OUTCOMES:
        y = R[o]
        good = np.isfinite(y)
        drivers[o] = {k: round(rv.rank_corr(Uk[good, j], y[good]), 2) for j, k in enumerate(NAMES)}
    out["drivers_rank_corr"] = drivers
    picks = {}
    for name, key, thr in (("most plausible +100 bp 10Y", "max_up_10Y", 100.0), ("most plausible -100 bp 10Y", "max_down_10Y", -100.0),
                           ("most plausible +50 bp 10Y in the recognition window", "recog_10Y", 50.0)):
        j, dist = rv.nearest_breach(Uk, np.nan_to_num(R[key]), thr, du)
        if j is not None:
            d = rv.from_unit(Uk[j], cls)
            moved = {k: [round(getattr(cls(), k), 3), round(getattr(d, k), 3)] for k in NAMES
                     if abs(Uk[j][NAMES.index(k)] - du[NAMES.index(k)]) > LISTED}
            picks[name] = {"distance": round(dist, 3), "value": round(float(R[key][j]), 1), "dials_moved_default_to_draw": moved,
                           "cause_by_subset": rv.attribute(e, d, key, thr, listed=tuple(moved)), "_j": j}
        else:
            picks[name] = None
    jb, jl = int(np.nanargmax(R["max_up_10Y"])), int(np.nanargmin(R["max_down_10Y"]))
    dials = lambda j: {k: round(getattr(rv.from_unit(Uk[j], cls), k), 3) for k in NAMES}  # noqa: E731
    picks["largest 10Y rise"] = {"value": round(float(R["max_up_10Y"][jb]), 1), "dials": dials(jb),
                                 "debt_max": round(float(R["debt_max"][jb]), 1), "r_star_max": round(float(R["r_star_max"][jb]), 2), "_j": jb}
    picks["largest 10Y fall"] = {"value": round(float(R["max_down_10Y"][jl]), 1), "dials": dials(jl),
                                 "r_star_min": round(float(R["r_star_min"][jl]), 2), "_j": jl}
    jr = int(np.nanargmax(R["rho_rise_max_pp"]))
    picks["largest rise in the required return"] = {"value_pp": round(float(R["rho_rise_max_pp"][jr]), 2), "dials": dials(jr), "_j": jr}
    out["picks"] = {k: ({kk: vv for kk, vv in v.items() if kk != "_j"} | {"draw": int(ok[v["_j"]])} if v else None)
                    for k, v in picks.items()}             # draw: the index in rv.sample(N), so a check can re-run it
    out["picks_note"] = PICKS_NOTE
    base = rv.run(e, cls())
    out["default_dials"] = {k: round(float(base[k]), 2) if base[k] is not None else None
                            for k in ("recog_10Y", "ten_year_10Y", "max_up_10Y", "max_down_10Y", "c50", "debt_max", "real_wage_min_rel",
                                      "policy_min", "policy_max", "rho_rise_max_pp")}
    return out, (Uk, R, drivers, picks)


def results():
    """The JSON: the central's envelope at the top level (the pre-switch keys), (b)'s beside it."""
    ec, info = m.central()
    eb, _, _, _ = m.calibrate(base=m.CAPITAL_BASE)
    U = rv.sample(N)
    out, fig_c = envelope(ec, U, rv.Dials)
    res = {"calibration": {k: info[k] for k in ("tag", "root", "rho", "capital_premium", "headroom_pp", "k", "source")},
           "ranges": rv.RANGES,
           "ranges_note": "the refit's (Log 46), revised 2026-10-28 (Log 54; decision 93): the capex dial is the investment key's "
                          "alpha_inv, Rachel and Smith's coefficient (macro.INVESTMENT_KEY_GDP) times the pass-through over "
                          "macro.INVESTMENT_PASS_THROUGH_RANGE (0 netted against capital consumption, 1 gross: the default, at the "
                          "range's top), per point of income; owners' saving and deficits over macro.NEUTRAL_SCALE_RANGE times the "
                          "evidence's ranges of the saving gap and the deficit's pass-through; comparator_b keeps (b)'s dials and "
                          "ranges (ranges_b)",
           "ranges_b": rv.RANGES_B,
           "premium_dial": f"premium_shift: pp added to the economy's own capital premium (central {info['capital_premium']:.2f}, (b) "
                           f"{m.capital_premium(eb):.2f}); on (b) the pre-switch capital_premium dial's "
                           f"{m.capital_premium(eb) + rv.RANGES['premium_shift'][0]:g}-{m.capital_premium(eb) + rv.RANGES['premium_shift'][1]:g} pp",
           **out}
    outb, fig_b = envelope(eb, U, rv.DialsB)
    res["comparator_b"] = {"calibration": {"tag": "b", "rho": eb.rho, "capital_premium": m.capital_premium(eb), "k": eb.k,
                                           "source": "macro.calibrate(base=macro.CAPITAL_BASE)"}, **outb}
    return res, (ec, U, fig_c, eb, fig_b)


def main():
    out, (e, U, (Uk, R, drivers, picks), eb, (Ub, Rb, _, _)) = results()
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    with open(os.path.join(ROOT, "results", "reverse_envelope.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, default=str)
    for label, o in (("central (c)", out), ("comparator (b)", out["comparator_b"])):
        print(f"{label}: solved {o['solved']}/{o['draws']}, no equilibrium {o['no_equilibrium']}, other failures {o['other_failures']}")
        for k in ("recog_10Y", "ten_year_10Y", "max_up_10Y", "max_down_10Y", "max_jump_10Y", "c50", "debt_max", "real_wage_min_rel",
                  "rho_rise_max_pp"):
            print(f"  {k:18s}", o["envelope"][k])
        print("  shares", o["shares"])
        for oc in OUTCOMES:
            top = sorted(o["drivers_rank_corr"][oc].items(), key=lambda kv: -abs(kv[1]))[:4]
            print(f"  drivers of {oc:18s}", top)
        for k, v in o["picks"].items():
            print(" ", k, v)
        print("  default dials", o["default_dials"])
    figure(e, Uk, R, drivers, picks, Rb)


def figure(e, U, R, drivers, picks, Rb):
    INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
    BLUE, RED, NEUTRAL = "#2a78d6", "#e34948", "#f0efec"
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9.5, "axes.edgecolor": GRID,
                         "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
                         "axes.titlesize": 10.5, "axes.titleweight": "bold", "axes.titlecolor": INK,
                         "axes.titlelocation": "left"})
    fig = plt.figure(figsize=(17.5, 10.2), facecolor=SURF, layout="constrained")
    fig.get_layout_engine().set(rect=(0, 0.035, 1, 0.965), h_pad=0.12, w_pad=0.1)
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
    x, xb = R["recog_10Y"][np.isfinite(R["recog_10Y"])], Rb["recog_10Y"][np.isfinite(Rb["recog_10Y"])]
    bins = np.linspace(min(x.min(), xb.min()), max(x.max(), xb.max()), 61)
    a.hist(x, bins=bins, color=BLUE, edgecolor=SURF, linewidth=0.6, label="(c) central")
    a.hist(xb, bins=bins, histtype="step", color=INK2, lw=1.2, label="(b), the same draws")
    a.axvline(0, color=INK2, lw=0.8)
    a.set_title("1. The 10Y move while the market wakes up" + NL + f"{len(x):,} draws over the dials"); a.set_xlabel("bp"); a.set_ylabel("draws")
    a.legend(frameon=False, fontsize=8.5, labelcolor=INK)
    a = ax2
    up, dn = R["max_up_10Y"], R["max_down_10Y"]
    a.hist(up[up > 0.5], bins=50, color=RED, edgecolor=SURF, linewidth=0.6, alpha=0.9, label="largest rise")
    a.hist(dn[dn < -0.5], bins=50, color=BLUE, edgecolor=SURF, linewidth=0.6, alpha=0.9, label="largest fall")
    a.axvline(0, color=INK2, lw=0.8)
    a.set_title("2. The 10Y's largest rise and fall, 15 years" + NL
                + f"never rises: {np.mean(up <= 0.5) * 100:.0f}% ((b) {np.mean(Rb['max_up_10Y'] <= 0.5) * 100:.0f}%); "
                  f"never falls: {np.mean(dn >= -0.5) * 100:.0f}% ((b) {np.mean(Rb['max_down_10Y'] >= -0.5) * 100:.0f}%)")
    a.set_xlabel("bp"); a.set_ylabel("draws")
    a.legend(frameon=False, fontsize=8.5, labelcolor=INK)
    a = ax3
    M = np.array([[drivers[o][k] for o in OUTCOMES] for k in rv.NAMES])
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list("div", [BLUE, NEUTRAL, RED])
    a.imshow(M, cmap=cmap, vmin=-1, vmax=1, aspect="auto")
    a.set_xticks(range(len(OUTCOMES)))
    a.set_xticklabels([f"10Y{NL}recog.", f"10Y{NL}max rise", f"10Y{NL}max fall", f"2Y{NL}10 yrs", f"debt{NL}peak", f"wage{NL}low"], fontsize=8.5)
    a.set_yticks(range(len(rv.NAMES)))
    a.set_yticklabels(["automation depth (eta end)", "automation width (yrs)", "automation midpoint (yr)", "investment -> r*",
                       "owners' saving -> r*", "deficits -> r*", "term premium per debt", "debt threshold",
                       "public support share", "capital premium (shift)", "data noise", "prior belief"], fontsize=8.5)
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            a.text(j, i, f"{M[i, j]:+.2f}", ha="center", va="center", fontsize=8, color=INK)
    a.set_title("3. What drives the outcomes" + NL + "rank correlation, dial against outcome; (c) central")
    a.yaxis.tick_right()
    a.tick_params(length=0)
    for sp in a.spines.values():
        sp.set_visible(False)
    a = ax4
    Cs = {"most plausible +100 bp 10Y": RED, "most plausible -100 bp 10Y": BLUE, "largest 10Y rise": "#eb6834", "largest 10Y fall": "#104281"}
    lo_, hi_ = 0.0, 0.0
    for name, c in Cs.items():
        pk = picks.get(name)
        if not pk:
            continue
        o = rv.run(e, rv.from_unit(U[pk["_j"]]), keep_paths=True)["_paths"]
        y = (o["z"][:, 2] - o["z"][0, 2]) * 100
        lo_, hi_ = min(lo_, y.min()), max(hi_, y.max())
        a.plot(o["t"], y, color=c, lw=2, label=f"{name} ({pk['value']:+.0f})")
    base = rv.run(e, rv.Dials(), keep_paths=True)["_paths"]
    a.plot(base["t"], (base["z"][:, 2] - base["z"][0, 2]) * 100, color=INK2, lw=1.6, ls="--", label="default dials")
    a.axhline(0, color=INK2, lw=0.8)
    a.set_title("4. The 10Y path in selected draws" + NL + "change from the start"); a.set_xlabel("years"); a.set_ylabel("bp")
    a.set_ylim(lo_ - 40, hi_ + 0.45 * (hi_ - lo_))
    a.legend(frameon=False, fontsize=8, labelcolor=INK, loc="upper left", ncol=2)
    a = ax5
    sc = a.scatter(R["real_wage_min_rel"], R["debt_max"], c=np.clip(R["ten_year_10Y"], -200, 200), cmap=cmap, vmin=-200, vmax=200, s=6, lw=0)
    a.set_title("5. The macro envelope" + NL + "colour: the 10Y's move over ten years"); a.set_xlabel("real wage low point, share of start")
    a.set_ylabel("public debt peak, % of income")
    cb = fig.colorbar(sc, ax=a, fraction=0.05, pad=0.02); cb.set_label("bp", color=INK2); cb.outline.set_visible(False)
    s_lo, s_hi = rv.RANGES["premium_shift"]
    fig.text(0.01, 0.005, "Two-world recognition model on calibration (c)'s central economy (open reading, low root); the capital premium dial is a shift of "
             f"{s_lo:+g} to {s_hi:+g} pp from its own {m.capital_premium(e):.2f} pp. Dials drawn by Latin hypercube over broad stated ranges (reverse.RANGES), "
             "not estimates;" + NL
             + "'most plausible' = nearest the defaults in the unit cube among draws reaching the threshold. The pile at the left of panel 2 is the "
             "lower bound: expected policy cannot go below -0.5%. Bridge ranges from the refit's evidence (Log 46); (b) on its own dials.", fontsize=8, color=INK2)
    pth = os.path.join(ROOT, "figures", "fig_reverse_envelope.png"); fig.savefig(pth, dpi=150, facecolor=SURF); print(pth)


if __name__ == "__main__":
    main()
