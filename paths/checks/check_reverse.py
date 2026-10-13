# check_reverse.py — reverse stress testing, part 1: the dial space, the sampler, the statistics, the run, the envelope.
#
# Since her decision of 2026-09-30 the run (R) is checked on calibration (c)'s central economy (macro.central(): the open
# (domp) reading, the low root in k), the economy of recognition.worlds()'s default worlds. R5 keeps its draw on (b), where
# it was picked — a test of the lower bound, unchanged — and R5c tests the bound on the central with the envelope's own
# largest-fall draw. N1 gates the guard (a run with no land-scarce equilibrium is caught, dated and counted). B1 gates the
# (b) comparator as the pre-switch run (the capital premium dial re-expressed as a shift from the economy's own premium). E1 re-runs the stored envelope's default dials and picks (results/reverse_envelope.json);
# the percentiles over 2 x 4,000 draws are not rebuilt here (about five minutes; code/reverse_envelope.py is their only
# source). The findings (F) are stated as found, the central against (b). F5 gates what a pick needs by re-running its draw
# with dial subsets (reverse.attribute) here, and the stored cause_by_subset against that re-run; the 0.15 listing of dials
# moved far is a description of the draw and is never read as the cause (restated: the first switch report read it so).
# Thresholds set after seeing (c)'s numbers: F2's "more than twice" (both 95th percentiles) and its +0.05 on the never-falls
# share (flagged here). F5 has no new numeric threshold (its 100 and 50 bp are the picks' own; 0.15 is the listing's).
#
# Run from paths/:  ../venv/Scripts/python.exe checks/check_reverse.py
# Exit status 0 only if every check passes.

from __future__ import annotations

import json
import os
import sys
from dataclasses import replace

import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "code"))
import macro as m  # noqa: E402
import recognition as rc  # noqa: E402
import regimes as rg  # noqa: E402
import reverse as rv  # noqa: E402
import reverse_envelope as rve  # noqa: E402

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


e, info = m.central()
eb, _, _, _ = m.calibrate(base=m.CAPITAL_BASE)
D0 = rv.Dials()
with open(os.path.join(os.path.dirname(HERE), "results", "reverse_envelope.json"), encoding="utf-8") as fh:
    E = json.load(fh)
EB = E["comparator_b"]
U4 = rv.sample(E["draws"])

print("U — the dial space and the sampler")
u0 = rv.to_unit(D0)
back = rv.from_unit(u0)
check("U1 the defaults sit inside the ranges, and unit -> dials -> unit is the identity (log dials included)",
      np.all((u0 > 0) & (u0 < 1)) and all(abs(getattr(back, k) - getattr(D0, k)) < 1e-12 for k in rv.NAMES),
      "defaults in the unit cube: " + " ".join(f"{k} {x:.2f}" for k, x in zip(rv.NAMES, u0)))
mid = rv.from_unit(np.full(len(rv.NAMES), 0.5))
check("U2 a log dial's midpoint is the geometric mean of its range, a linear dial's the arithmetic mean",
      all(abs(getattr(mid, k) - (np.sqrt(lo * hi) if k in rv.LOG else (lo + hi) / 2)) < 1e-12 for k, (lo, hi) in rv.RANGES.items()))
n = 500
U = rv.sample(n)
strata = np.floor(U * n).astype(int)
check("U3 the Latin hypercube puts exactly one draw in each 1/n stratum of every dial",
      all(np.array_equal(np.sort(strata[:, j]), np.arange(n)) for j in range(U.shape[1])))

print("S — the statistics")
rng = np.random.default_rng(1)
x = rng.normal(size=2000)
check("S1 rank correlation is +1 under any increasing transform, -1 under a decreasing one, near 0 for independent draws",
      abs(rv.rank_corr(x, np.exp(3 * x)) - 1) < 1e-12 and abs(rv.rank_corr(x, -x ** 3) + 1) < 1e-12
      and abs(rv.rank_corr(x, rng.normal(size=2000))) < 0.1)
Us = np.array([[0.5, 0.5], [0.9, 0.9], [0.6, 0.5], [0.1, 0.1], [0.45, 0.2]])
vals = np.array([0.0, 150.0, 120.0, -200.0, -90.0])
j_up, d_up = rv.nearest_breach(Us, vals, 100.0, np.array([0.5, 0.5]))
j_dn, d_dn = rv.nearest_breach(Us, vals, -100.0, np.array([0.5, 0.5]))
j_no, _ = rv.nearest_breach(Us, vals, 500.0, np.array([0.5, 0.5]))
check("S2 nearest breach: the closest draw among those reaching the threshold, by sign; none if nothing reaches it",
      j_up == 2 and abs(d_up - 0.1) < 1e-12 and j_dn == 3 and j_no is None)

print("R — the run (calibration (c), central; R5 on (b), where its draw was picked)")
o0 = rv.run(e, D0, lookahead=0.0)
e_w, old, new = rc.worlds()
p = rc.learn(old, new, rc.Learning(sigma=D0.sigma, p0=D0.p0))
mixes, _, _, _ = rc.market_curves(old, new, p)
z = np.array([rg.zero(np.array([10.0]), mx)[0] for mx in mixes])
t = old["t"]
i10, i90 = max(int(np.searchsorted(t, rc.crossing(t, p, 0.1))) - 1, 0), int(np.searchsorted(t, rc.crossing(t, p, 0.9)))
check("R1 at the default dials (no look-ahead) the run is the recognition model: the same 10Y move over the window",
      e_w == e and abs(o0["recog_10Y"] - (z[i90] - z[i10]) * 100) < 1e-9, f"{o0['recog_10Y']:+.2f} bp")
o1 = rv.run(e, D0)
check("R2 simulating ten years past the horizon changes the default run little (its new world has settled by year 15)",
      abs(o1["recog_10Y"] - o0["recog_10Y"]) < 1.0 and abs(o1["ten_year_10Y"] - o0["ten_year_10Y"]) < 10.0,
      f"10Y over ten years {o0['ten_year_10Y']:+.1f} -> {o1['ten_year_10Y']:+.1f} bp")
lo_rent, hi_rent = rv.run(e, replace(D0, alpha_rent=0.02)), rv.run(e, replace(D0, alpha_rent=0.15))
lo_fis, hi_fis = rv.run(e, replace(D0, alpha_fiscal=0.0)), rv.run(e, replace(D0, alpha_fiscal=0.3))
check("R3 the two bridges that decide direction move the 10Y as their sign says: owners' saving down, deficits up",
      hi_rent["ten_year_10Y"] < lo_rent["ten_year_10Y"] and hi_fis["ten_year_10Y"] > lo_fis["ten_year_10Y"],
      f"alpha_rent .02 -> .15: {lo_rent['ten_year_10Y']:+.0f} -> {hi_rent['ten_year_10Y']:+.0f} bp; "
      f"alpha_fiscal 0 -> .3: {lo_fis['ten_year_10Y']:+.0f} -> {hi_fis['ten_year_10Y']:+.0f} bp")
check("R4 more public support means more public debt; shallower automation means a higher real-wage low point",
      rv.run(e, replace(D0, public_support=0.5))["debt_max"] > o1["debt_max"]
      and rv.run(e, replace(D0, eta_end=0.3))["real_wage_min_rel"] > o1["real_wage_min_rel"])
deep = rv.Dials(eta_end=0.037, width=1.42, t_mid=7.83, alpha_capex=0.985, alpha_rent=0.192, alpha_fiscal=0.367,
                tp_per_debt=0.004, debt_threshold=83.0, public_support=0.515, premium_shift=3.98 - m.capital_premium(eb), sigma=1.79,
                p0=0.107)                      # picked on (b) with its capital premium at 3.98 pp: the shift that gives it there
od = rv.run(eb, deep, keep_paths=True)
check("R5 in a draw that drives the neutral rate far below zero, policy stops at the lower bound and the 10Y stops falling",
      od["policy_min"] >= -0.5 - 1e-12 and od["r_star_min"] + 2.0 < -0.5
      and np.ptp(od["_paths"]["z"][-12:, 2]) * 100 < 10.0,
      f"r* low {od['r_star_min']:+.1f}%, policy low {od['policy_min']:+.2f}%, 10Y range over the last 3 years "
      f"{np.ptp(od['_paths']['z'][-12:, 2]) * 100:.1f} bp")
oc_deep = rv.run(e, deep)
jf = E["picks"]["largest 10Y fall"]["draw"]
oc = rv.run(e, rv.from_unit(U4[jf]), keep_paths=True)
check("R5c on the central the same holds in the envelope's largest-fall draw (R5's (b) draw does not take the central's r* "
      "far enough below zero to reach the floor): policy stops at the lower bound and the 10Y stops falling",
      oc["policy_min"] >= -0.5 - 1e-12 and oc["r_star_min"] + 2.0 < -0.5 and np.ptp(oc["_paths"]["z"][-12:, 2]) * 100 < 10.0,
      f"draw {jf}: r* low {oc['r_star_min']:+.2f}%, policy low {oc['policy_min']:+.2f}%, 10Y range over the last 3 years "
      f"{np.ptp(oc['_paths']['z'][-12:, 2]) * 100:.1f} bp; R5's draw on the central: r* low {oc_deep['r_star_min']:+.2f}%, policy low "
      f"{oc_deep['policy_min']:+.2f}%")


def flips(rs, thr=0.25):
    d = np.diff(rs)
    return int(np.sum((d[1:] * d[:-1] < 0) & (np.minimum(np.abs(d[1:]), np.abs(d[:-1])) > thr)))


def rstar(d, hl):
    return m.macro_path(e, rv.techs(e, d)[1], rv.bridges(e, d, rho_halflife=hl), 25, 0.25)["r_star"]


f1 = np.array([flips(rstar(rv.from_unit(u), 1.0)) for u in U[:300]])
f0 = flips(rstar(deep, 0.0))
check("R6 with the required return adjusting (half-life 1 year) no draw cycles quarter to quarter; following last quarter's r* at once can",
      f1.max() <= 1 and f0 >= 10, f"300 draws: at most {f1.max()} reversal(s) of more than 25 bp; the deep draw undamped: {f0}")

print("N — the guard: a run with no land-scarce equilibrium is caught, dated and counted, not dropped")
d8 = rv.Dials(premium_shift=8.0)                     # past the central's rate headroom at its start
try:
    rv.run(e, d8)
    raised = False
except m.NoEquilibrium:
    raised = True
f8 = rv.first_failure(e, d8)
rows_, ok_, noeq_, other_ = rve.draws(e, np.array([rv.to_unit(D0), rv.to_unit(d8)]))
tp_up = m.TechPath(eta_end=1.0, lam_end=e.lam * 1.5, t_mid=6, width=6)   # lambda rising: the machine chain's ceiling falls
br_up = m.Bridges(rho_shift=5.0)
fy = rv.failure_year(e, tp_up, br_up, 25.0)
scan = None
for j in range(1, 101):
    try:
        m.macro_path(e, tp_up, br_up, j * 0.25, 0.25)
    except m.NoEquilibrium:
        scan = j * 0.25
        break
check("N1 past the rate headroom run() raises NoEquilibrium, first_failure dates it (the status quo, year 0) and the envelope's "
      "draws() counts it beside the solved draw; on a path that loses its equilibrium mid-way, failure_year's bisection finds the "
      "same first date as a scan of every prefix",
      raised and f8 is not None and (f8["world"], f8["year"]) == ("status quo", 0.0) and list(ok_) == [0] and len(rows_) == 1
      and noeq_ == [{"draw": 1, "world": "status quo", "year": 0.0}] and other_ == [] and fy is not None and fy[0] == scan,
      f"premium +8 pp: {f8['world']}, year {f8['year']:g}; lambda x1.5 with +5 pp on the return: first failing date {fy[0]:g} "
      f"(scan {scan:g})")

print("B — the (b) comparator: the pre-switch run")


def pre_bridges(d, cp):
    """The pre-switch run's bridges: the capital premium a dial of its own (3-7 pp)."""
    return m.Bridges(capital_premium=cp, alpha_capex=d.alpha_capex, alpha_rent=d.alpha_rent, alpha_fiscal=d.alpha_fiscal,
                     tp_per_debt=d.tp_per_debt, debt_threshold=d.debt_threshold, public_support=d.public_support, r0_star=0.75)


def pre_techs(d):
    """The pre-switch run's technology paths: lambda to (b)'s 0.01, hard-coded."""
    return m.TechPath(eta_end=1.0, lam_end=eb.lam), m.TechPath(eta_end=d.eta_end, lam_end=0.01, t_mid=d.t_mid, width=d.width)


jp = rv.NAMES.index("premium_shift")
gap, rest_same = 0.0, True
for u in U4[:200]:
    d = rv.from_unit(u)
    bn, bo = rv.bridges(eb, d), pre_bridges(d, 3.0 + float(u[jp]) * (7.0 - 3.0))   # the pre-switch dial, from the same unit point
    gap = max(gap, abs(bn.capital_premium - bo.capital_premium))
    rest_same &= replace(bn, capital_premium=bo.capital_premium) == bo and rv.techs(eb, d) == pre_techs(d)
lo_s, hi_s = rv.RANGES["premium_shift"]
ob0 = rv.run(eb, D0, lookahead=0.0)
check("B1 on (b) the run's inputs are the pre-switch run's: at the default dials its bridges and technology paths are identical "
      "(premium 5.0 + 0.0), and over 200 of the envelope's draws the shifted premium is the pre-switch 3-7 pp dial to rounding, "
      "every other input identical",
      rv.bridges(eb, D0) == pre_bridges(D0, 5.0) and rv.techs(eb, D0) == pre_techs(D0) and rest_same and gap < 1e-12
      and (m.capital_premium(eb) + lo_s, m.capital_premium(eb) + hi_s) == (3.0, 7.0),
      f"largest premium gap {gap:.1e} pp; (b) at the default dials: 10Y over the recognition window {ob0['recog_10Y']:+.2f} bp")

print("E — the envelope as stored (results/reverse_envelope.json, written by code/reverse_envelope.py)")
KEYS = {"most plausible +100 bp 10Y": ("max_up_10Y", "value", 1), "most plausible -100 bp 10Y": ("max_down_10Y", "value", 1),
        "most plausible +50 bp 10Y in the recognition window": ("recog_10Y", "value", 1), "largest 10Y rise": ("max_up_10Y", "value", 1),
        "largest 10Y fall": ("max_down_10Y", "value", 1), "largest rise in the required return": ("rho_rise_max_pp", "value_pp", 2)}
ok_e, n_re = True, 0
for econ, blk in ((e, E), (eb, EB)):
    base = rv.run(econ, D0)
    ok_e &= all(blk["default_dials"][k] == (round(float(base[k]), 2) if base[k] is not None else None) for k in blk["default_dials"])
    ok_e &= blk["solved"] + blk["no_equilibrium"] + blk["other_failures"] == blk["draws"] == len(U4)
    ok_e &= set(blk["picks"]) == set(KEYS)
    for name, pk in blk["picks"].items():
        if pk is None:
            continue
        key, field, nd = KEYS[name]
        o = rv.run(econ, rv.from_unit(U4[pk["draw"]]))
        ok_e &= round(float(o[key]), nd) == pk[field]
        n_re += 1
check("E1 the stored envelope re-runs: the default-dial outcomes and every pick reproduce from their draws, on the central and "
      "on (b); the draws add up; the ranges and the calibration are the code's",
      ok_e and E["ranges"] == {k: list(v) for k, v in rv.RANGES.items()} and E["calibration"]["tag"] == info["tag"]
      and E["calibration"]["rho"] == e.rho and EB["calibration"]["rho"] == eb.rho,
      f"{n_re} picks re-run; draws {E['draws']} each")

print("F — the findings (the envelope, the central against (b); bridge ranges set around (b)'s defaults; stated as found)")
ev, evb = E["envelope"], EB["envelope"]
CURVE = ("recog_10Y", "max_up_10Y", "max_down_10Y", "ten_year_2Y")
dr, drb = E["drivers_rank_corr"], EB["drivers_rank_corr"]
top2 = lambda d, o: [k for k, _ in sorted(d[o].items(), key=lambda kv: -abs(kv[1]))[:2]]  # noqa: E731
q3 = lambda d, k, f="+.0f": " / ".join(format(d[k][q], f) for q in ("p5", "p50", "p95"))  # noqa: E731
check("F1 the sign of the curve's move is still not pinned by the mechanism, and the same two bridges decide it: owners' saving "
      "first (down), deficits second (up) for every curve outcome; on the central deficits weigh more and the build-out less",
      all(ev[k]["p5"] < 0 < ev[k]["p95"] for k in ("recog_10Y", "ten_year_10Y"))
      and all(top2(dr, o) == ["alpha_rent", "alpha_fiscal"] and dr[o]["alpha_rent"] < 0 < dr[o]["alpha_fiscal"] for o in CURVE)
      and dr["recog_10Y"]["alpha_fiscal"] > drb["recog_10Y"]["alpha_fiscal"] and dr["recog_10Y"]["alpha_capex"] < drb["recog_10Y"]["alpha_capex"],
      f"10Y over ten years 5/50/95%: {q3(ev, 'ten_year_10Y')} bp ((b) {q3(evb, 'ten_year_10Y')}); recognition window "
      f"{q3(ev, 'recog_10Y')} ((b) {q3(evb, 'recog_10Y')}); rank corr. in the window: owners' saving "
      f"{dr['recog_10Y']['alpha_rent']:+.2f} ((b) {drb['recog_10Y']['alpha_rent']:+.2f}), deficits {dr['recog_10Y']['alpha_fiscal']:+.2f} "
      f"({drb['recog_10Y']['alpha_fiscal']:+.2f}), build-out {dr['recog_10Y']['alpha_capex']:+.2f} ({drb['recog_10Y']['alpha_capex']:+.2f})")
sh, shb = E["shares"], EB["shares"]
check("F2 the tails: the rise side is more than twice as long on the central (its 95th percentile over ten years and its largest "
      "rise), the 10Y never falls in a third of draws rather than a quarter, and policy reaches the floor more often",
      ev["ten_year_10Y"]["p95"] > 2 * evb["ten_year_10Y"]["p95"] and ev["max_up_10Y"]["p95"] > 2 * evb["max_up_10Y"]["p95"]
      and sh["10Y_never_falls"] > shb["10Y_never_falls"] + 0.05 and sh["policy_reaches_floor"] > shb["policy_reaches_floor"],
      f"10Y over ten years, 95%: {ev['ten_year_10Y']['p95']:+.0f} bp ((b) {evb['ten_year_10Y']['p95']:+.0f}); largest rise 95%: "
      f"{ev['max_up_10Y']['p95']:+.0f} ((b) {evb['max_up_10Y']['p95']:+.0f}), max {ev['max_up_10Y']['max']:+.0f} ({evb['max_up_10Y']['max']:+.0f}); "
      f"never rises {sh['10Y_never_rises']:.0%} ({shb['10Y_never_rises']:.0%}), never falls {sh['10Y_never_falls']:.0%} "
      f"({shb['10Y_never_falls']:.0%}); policy at the floor {sh['policy_reaches_floor']:.0%} ({shb['policy_reaches_floor']:.0%})")
rw, rwb, db, dbb = ev["real_wage_min_rel"], evb["real_wage_min_rel"], ev["debt_max"], evb["debt_max"]
check("F3 the real economy is harsher on the central and still set by the technology path: the real wage's low point is lower "
      "at every percentile and below its start in every draw, debt peaks higher; automation depth drives the wage's low, public "
      "support the debt",
      all(rw[q] < rwb[q] for q in ("p5", "p50", "p95", "max")) and rw["max"] < 1.0 and all(db[q] > dbb[q] for q in ("p50", "p95", "max"))
      and top2(dr, "real_wage_min_rel")[0] == "eta_end" and top2(dr, "debt_max")[0] == "public_support",
      f"real wage low 5/50/95%: {q3(ev, 'real_wage_min_rel', '.2f')} of its start ((b) {q3(evb, 'real_wage_min_rel', '.2f')}), highest "
      f"{rw['max']:.2f} ({rwb['max']:.2f}); debt peak 5/50/95%: {q3(ev, 'debt_max', '.0f')}% of income ((b) {q3(evb, 'debt_max', '.0f')})")
check("F4 the market wakes up earlier on the central: the date belief crosses one half is earlier at every percentile",
      all(ev["c50"][q] < evb["c50"][q] for q in ("p5", "p50", "p95")),
      f"5/50/95%: {q3(ev, 'c50', '.2f')} years ((b) {q3(evb, 'c50', '.2f')})")
pk, pkb = E["picks"], EB["picks"]
P100, M100, P50 = "most plausible +100 bp 10Y", "most plausible -100 bp 10Y", "most plausible +50 bp 10Y in the recognition window"
up, upb, dn = pk[P100], pkb[P100], pk[M100]
# the cause, re-run here by dial subsets (reverse.attribute), not read off the 0.15 listing of dials moved far
att = {(lab, nm): rv.attribute(econ, rv.from_unit(U4[blk[nm]["draw"]]), KEYS[nm][0], thr, listed=tuple(blk[nm]["dials_moved_default_to_draw"]))
       for lab, econ, blk in (("c", e, pk), ("b", eb, pkb)) for nm, thr in ((P100, 100.0), (M100, -100.0), (P50, 50.0))}
a1, a1b, am, a50 = att[("c", P100)], att[("b", P100)], att[("c", M100)], att[("c", P50)]
lu = U4[up["draw"]] - rv.to_unit(D0)
small = {k: float(abs(lu[rv.NAMES.index(k)])) for k in rv.DIRECTION}
LISTED_ = rve.LISTED
check("F5 a +100 bp rise lies nearer the defaults on the central, and what it needs — found by re-running the draw with dial subsets, "
      "not by the listing of dials moved more than 0.15 of their range — is the two neutral-rate bridges that decide direction: owners' "
      "saving below its default and deficits above it, each moved by less than the listing's 0.15 (so the listing misses them). Moved "
      "alone from the defaults they reach +100 bp; reset to their defaults in the draw, the rise is gone; the listed technology and "
      "fiscal dials alone give no rise and, with the bridges, damp it; resetting either bridge alone loses the breach and no other "
      "dial's reset does. The +50 bp in the recognition window is the same draw and needs the same two; the most plausible -100 bp "
      "is the same draw on both calibrations and needs deficits below their default",
      up["distance"] < upb["distance"] and all(v < LISTED_ for v in small.values())
      and set(up["dials_moved_default_to_draw"]).isdisjoint(rv.DIRECTION)
      and a1["at_draw"] >= 100.0 and a1["direction_bridges_only"] >= 100.0 and a1["direction_bridges_reset"] < 100.0
      and a1["listed_dials_only"] < 100.0 and a1["direction_bridges_only"] > a1["at_draw"] and a1["needed"] == list(rv.DIRECTION)
      and pk[P50]["draw"] == up["draw"] and a50["needed"] == list(rv.DIRECTION)
      and a1["direction_bridges"]["alpha_rent"][1] < a1["direction_bridges"]["alpha_rent"][0]
      and a1["direction_bridges"]["alpha_fiscal"][1] > a1["direction_bridges"]["alpha_fiscal"][0]
      and dn["draw"] == pkb[M100]["draw"] and "alpha_fiscal" in am["needed"] and att[("b", M100)]["needed"] == am["needed"]
      and am["direction_bridges"]["alpha_fiscal"][1] < am["direction_bridges"]["alpha_fiscal"][0]
      and all(blk[nm]["cause_by_subset"] == att[(lab, nm)] for lab, blk in (("c", pk), ("b", pkb)) for nm in (P100, M100, P50)),
      f"+100: draw {up['draw']}, distance {up['distance']:.3f} ((b) {upb['distance']:.3f}), {a1['at_draw']:+.1f} bp; owners' saving "
      f"{a1['direction_bridges']['alpha_rent'][0]:g} -> {a1['direction_bridges']['alpha_rent'][1]:.3f}, deficits "
      f"{a1['direction_bridges']['alpha_fiscal'][0]:g} -> {a1['direction_bridges']['alpha_fiscal'][1]:.3f} (moved {small['alpha_rent']:.3f} / "
      f"{small['alpha_fiscal']:.3f} of their range); those two alone {a1['direction_bridges_only']:+.1f}, reset {a1['direction_bridges_reset']:+.1f}, "
      f"the listed {sorted(up['dials_moved_default_to_draw'])} alone {a1['listed_dials_only']:+.1f}; needed {a1['needed']}. (b)'s +100 (draw "
      f"{upb['draw']}, {a1b['at_draw']:+.1f}): the two alone {a1b['direction_bridges_only']:+.1f}, reset {a1b['direction_bridges_reset']:+.1f}, "
      f"listed {sorted(upb['dials_moved_default_to_draw'])} alone {a1b['listed_dials_only']:+.1f}; needed {a1b['needed']}. +50 in the window: "
      f"{a50['at_draw']:+.1f}, the two alone {a50['direction_bridges_only']:+.1f}, reset {a50['direction_bridges_reset']:+.1f}. -100: draw "
      f"{dn['draw']}, {am['at_draw']:+.1f} bp ((b) {att[('b', M100)]['at_draw']:+.1f}); deficits {am['direction_bridges']['alpha_fiscal'][1]:.3f}; "
      f"the listed {sorted(dn['dials_moved_default_to_draw'])} alone {am['listed_dials_only']:+.1f}; needed {am['needed']}")
rr, prr = ev["rho_rise_max_pp"], pk["largest rise in the required return"]
dr_ = rv.from_unit(U4[prr["draw"]])
nw_ = m.macro_path(e, rv.techs(e, dr_)[1], rv.bridges(e, dr_), 25.0, 0.25)
it = int(np.argmax(nw_["rho"][nw_["t"] <= 15.0 + 1e-9]))  # the run's reported horizon (rv.run keeps 15 of 25 years)
above = nw_["rho"][it] - e.rho * 100                      # pp above the central's own required return, at its peak
hr_t = m.rate_headroom(replace(rv.techs(e, dr_)[1].at(nw_["t"][it], e), rho=e.rho))   # that date's technology, from the central's rho
check("F6 every draw has a land-scarce equilibrium at every date, on the central and on (b): none is lost to NoEquilibrium, "
      "though the largest rise in the required return goes past the central's headroom at its start — by then deep automation has "
      "moved the machine chain's ceiling out",
      E["no_equilibrium"] == 0 and EB["no_equilibrium"] == 0 and E["other_failures"] == 0 and EB["other_failures"] == 0
      and E["solved"] == E["draws"] and abs(nw_["rho"][it] - nw_["rho"][0] - prr["value_pp"]) < 0.005
      and info["headroom_pp"] < above < hr_t,
      f"solved {E['solved']}/{E['draws']} ((b) {EB['solved']}/{EB['draws']}); draw {prr['draw']}: the return peaks {above:.2f} pp above the "
      f"central's in year {nw_['t'][it]:g}, against a headroom of {info['headroom_pp']:.2f} pp at the start and {'at least ' if hr_t >= 20.0 else ''}{hr_t:.2f} pp at that "
      "date's technology")

fails = [nm for nm, ok, _ in RESULTS if not ok]
print(f"\n{len(RESULTS) - len(fails)}/{len(RESULTS)} checks passed")
print(f"ALL GREEN ({len(RESULTS)})" if not fails else "FAILURES: " + "; ".join(nm.split(' ')[0] for nm in fails))
sys.exit(0 if not fails else 1)
