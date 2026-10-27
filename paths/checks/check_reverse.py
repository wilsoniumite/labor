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
# Restated at the refit (2026-10-27, Log 46; decision 77), as found. The central's draws run in the refit's dial space (rv.Dials:
# the investment key's alpha_inv in place of alpha_capex, the bridges' ranges the evidence's), (b)'s in its own (rv.DialsB, the
# pre-refit ranges): the same unit draws, so (b)'s envelope is the pre-refit one exactly. R3 reads the direction bridges through
# the recognition window (over ten years the lower bound binds in both); R5 keeps its draw on (b) in (b)'s space, R5c on the
# central maps it to the refit's; R6 states that on the investment key no draw cycles even undamped (the cycling was the pace
# key's, still gated on (b)'s dials); F1-F6 restated: the sign is now nearly pinned, downward; the fall side dominates the tails;
# a +100 bp rise needs fiscal strain as well as the two direction bridges; the largest rise in the required return stays inside
# the headroom. Thresholds set after seeing the refit's numbers (flagged): F1's 0.9 shares, F2's bands, R3's dial values (the
# branches' ends).
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
D0, D0B = rv.Dials(), rv.DialsB()
with open(os.path.join(os.path.dirname(HERE), "results", "reverse_envelope.json"), encoding="utf-8") as fh:
    E = json.load(fh)
EB = E["comparator_b"]
U4 = rv.sample(E["draws"])

print("U — the dial space and the sampler")
ok_u1, txt_u1 = True, []
for cls, d0_ in ((rv.Dials, D0), (rv.DialsB, D0B)):
    names_ = rv.space(cls)[0]
    u0 = rv.to_unit(d0_)
    back = rv.from_unit(u0, cls)
    ok_u1 &= bool(np.all((u0 > 0) & (u0 < 1))) and all(abs(getattr(back, k) - getattr(d0_, k)) < 1e-12 for k in names_)
    txt_u1.append(f"{cls.__name__}: " + " ".join(f"{k} {x:.2f}" for k, x in zip(names_, u0)))
check("U1 in both dial spaces (the refit's and (b)'s) the defaults sit inside the ranges, and unit -> dials -> unit is the identity "
      "(log dials included); the two spaces differ only in the bridge dials (the refit's capex dial is alpha_inv)",
      ok_u1 and [k for k in rv.NAMES if k not in rv.NAMES_B] == ["alpha_inv"] and len(rv.NAMES) == len(rv.NAMES_B)
      and all(rv.RANGES[k] == rv.RANGES_B[k] for k in rv.NAMES if k not in ("alpha_inv", "alpha_rent", "alpha_fiscal")),
      "; ".join(txt_u1))
ok_u2 = True
for cls in (rv.Dials, rv.DialsB):
    names_, ranges_ = rv.space(cls)
    mid = rv.from_unit(np.full(len(names_), 0.5), cls)
    ok_u2 &= all(abs(getattr(mid, k) - (np.sqrt(lo * hi) if k in rv.LOG else (lo + hi) / 2)) < 1e-12 for k, (lo, hi) in ranges_.items())
check("U2 a log dial's midpoint is the geometric mean of its range, a linear dial's the arithmetic mean (both spaces)", ok_u2)
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
BR = m.BRANCHES
ar_, af_ = (BR["deficits dominate"]["alpha_rent"], BR["owners' saving dominates"]["alpha_rent"]), \
    (BR["owners' saving dominates"]["alpha_fiscal"], BR["deficits dominate"]["alpha_fiscal"])
lo_rent, hi_rent = rv.run(e, replace(D0, alpha_rent=ar_[0])), rv.run(e, replace(D0, alpha_rent=ar_[1]))
lo_fis, hi_fis = rv.run(e, replace(D0, alpha_fiscal=af_[0])), rv.run(e, replace(D0, alpha_fiscal=af_[1]))
check("R3 [restated at the refit] the two bridges that decide direction move the 10Y as their sign says through the recognition window: "
      "owners' saving down, deficits up, each across its branches' ends (over ten years the lower bound binds in both, so the 10Y ends "
      "near the floor either way); the neutral rate's low moves the same way",
      hi_rent["recog_10Y"] < lo_rent["recog_10Y"] and hi_fis["recog_10Y"] > lo_fis["recog_10Y"]
      and hi_rent["r_star_min"] < lo_rent["r_star_min"] and hi_fis["r_star_min"] > lo_fis["r_star_min"],
      f"alpha_rent {ar_[0]:.3f} -> {ar_[1]:.3f}: {lo_rent['recog_10Y']:+.0f} -> {hi_rent['recog_10Y']:+.0f} bp (over ten years "
      f"{lo_rent['ten_year_10Y']:+.0f} -> {hi_rent['ten_year_10Y']:+.0f}); alpha_fiscal {af_[0]:.3f} -> {af_[1]:.3f}: {lo_fis['recog_10Y']:+.0f} -> "
      f"{hi_fis['recog_10Y']:+.0f} bp ({lo_fis['ten_year_10Y']:+.0f} -> {hi_fis['ten_year_10Y']:+.0f})")
check("R4 more public support means more public debt; shallower automation means a higher real-wage low point",
      rv.run(e, replace(D0, public_support=0.5))["debt_max"] > o1["debt_max"]
      and rv.run(e, replace(D0, eta_end=0.3))["real_wage_min_rel"] > o1["real_wage_min_rel"])
deep = rv.DialsB(eta_end=0.037, width=1.42, t_mid=7.83, alpha_capex=0.985, alpha_rent=0.192, alpha_fiscal=0.367,
                 tp_per_debt=0.004, debt_threshold=83.0, public_support=0.515, premium_shift=3.98 - m.capital_premium(eb), sigma=1.79,
                 p0=0.107)                     # picked on (b) with its capital premium at 3.98 pp: the shift that gives it there
deep_c = rv.from_unit(rv.to_unit(deep), rv.Dials)   # the same unit point in the refit's dial space
od = rv.run(eb, deep, keep_paths=True)
check("R5 in a draw that drives the neutral rate far below zero, policy stops at the lower bound and the 10Y stops falling",
      od["policy_min"] >= -0.5 - 1e-12 and od["r_star_min"] + 2.0 < -0.5
      and np.ptp(od["_paths"]["z"][-12:, 2]) * 100 < 10.0,
      f"r* low {od['r_star_min']:+.1f}%, policy low {od['policy_min']:+.2f}%, 10Y range over the last 3 years "
      f"{np.ptp(od['_paths']['z'][-12:, 2]) * 100:.1f} bp")
jf = E["picks"]["largest 10Y fall"]["draw"]
oc = rv.run(e, rv.from_unit(U4[jf]), keep_paths=True)
oc_d = rv.run(e, deep_c, keep_paths=True)
stops = lambda o_: float(np.min(o_["_paths"]["z"][-12:, 2]) - np.min(o_["_paths"]["z"][:-12, 2])) * 100 >= -1.0  # noqa: E731
check("R5c [restated at the refit] on the central the same holds in R5's draw taken to the refit's dial space and in the envelope's "
      "largest-fall draw: policy stops at the lower bound and the 10Y falls no further over the last three years (in R5's draw it is "
      "flat; in the largest-fall draw it has turned up from its low)",
      all(o_["policy_min"] >= -0.5 - 1e-12 and o_["r_star_min"] + 2.0 < -0.5 and stops(o_) for o_ in (oc, oc_d))
      and np.ptp(oc_d["_paths"]["z"][-12:, 2]) * 100 < 10.0,
      f"draw {jf}: r* low {oc['r_star_min']:+.2f}%, policy low {oc['policy_min']:+.2f}%, 10Y over the last 3 years "
      f"{np.min(oc['_paths']['z'][-12:, 2]) * 100 - oc['_paths']['z'][0, 2] * 100:+.1f} to {np.max(oc['_paths']['z'][-12:, 2]) * 100 - oc['_paths']['z'][0, 2] * 100:+.1f} bp from the start; "
      f"R5's draw on the central: r* low {oc_d['r_star_min']:+.2f}%, policy low {oc_d['policy_min']:+.2f}%, 10Y range over the last 3 years "
      f"{np.ptp(oc_d['_paths']['z'][-12:, 2]) * 100:.1f} bp")


def flips(rs, thr=0.25):
    d = np.diff(rs)
    return int(np.sum((d[1:] * d[:-1] < 0) & (np.minimum(np.abs(d[1:]), np.abs(d[:-1])) > thr)))


def rstar(d, hl):
    return m.macro_path(e, rv.techs(e, d)[1], rv.bridges(e, d, rho_halflife=hl), 25, 0.25)["r_star"]


f1 = np.array([flips(rstar(rv.from_unit(u), 1.0)) for u in U[:300]])
f1u = np.array([flips(rstar(rv.from_unit(u), 0.0)) for u in U[:100]])
f0 = flips(rstar(deep, 0.0))
check("R6 [restated at the refit] with the required return adjusting (half-life 1 year) no draw cycles quarter to quarter; on the refit's "
      "investment key none does even following last quarter's r* at once — the cycling was the pace key's (the pace swings near full "
      "automation): on (b)'s dials the deep draw, undamped, still cycles",
      f1.max() <= 1 and f1u.max() <= 1 and f0 >= 10,
      f"300 draws damped / 100 undamped: at most {f1.max()} / {f1u.max()} reversal(s) of more than 25 bp; the deep draw on (b)'s dials undamped: {f0}")

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
br_up = m.Bridges(rho_shift=5.0)                      # the refit's bridges at a fixed return
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
    """The pre-switch run's bridges: the capital premium a dial of its own (3-7 pp), on the bridges as tuned on (b)."""
    return replace(m.BRIDGES_B, capital_premium=cp, alpha_capex=d.alpha_capex, alpha_rent=d.alpha_rent, alpha_fiscal=d.alpha_fiscal,
                   tp_per_debt=d.tp_per_debt, debt_threshold=d.debt_threshold, public_support=d.public_support, r0_star=0.75)


def pre_techs(d):
    """The pre-switch run's technology paths: lambda to (b)'s 0.01, hard-coded."""
    return m.TechPath(eta_end=1.0, lam_end=eb.lam), m.TechPath(eta_end=d.eta_end, lam_end=0.01, t_mid=d.t_mid, width=d.width)


jp = rv.NAMES_B.index("premium_shift")
gap, rest_same = 0.0, True
for u in U4[:200]:
    d = rv.from_unit(u, rv.DialsB)
    bn, bo = rv.bridges(eb, d), pre_bridges(d, 3.0 + float(u[jp]) * (7.0 - 3.0))   # the pre-switch dial, from the same unit point
    gap = max(gap, abs(bn.capital_premium - bo.capital_premium))
    rest_same &= replace(bn, capital_premium=bo.capital_premium) == bo and rv.techs(eb, d) == pre_techs(d)
lo_s, hi_s = rv.RANGES_B["premium_shift"]
ob0 = rv.run(eb, D0B, lookahead=0.0)
check("B1 on (b) the run's inputs are the pre-switch run's: at the default dials its bridges and technology paths are identical "
      "(premium 5.0 + 0.0), and over 200 of the envelope's draws the shifted premium is the pre-switch 3-7 pp dial to rounding, "
      "every other input identical",
      rv.bridges(eb, D0B) == pre_bridges(D0B, 5.0) and rv.techs(eb, D0B) == pre_techs(D0B) and rest_same and gap < 1e-12
      and (m.capital_premium(eb) + lo_s, m.capital_premium(eb) + hi_s) == (3.0, 7.0),
      f"largest premium gap {gap:.1e} pp; (b) at the default dials: 10Y over the recognition window {ob0['recog_10Y']:+.2f} bp")

print("E — the envelope as stored (results/reverse_envelope.json, written by code/reverse_envelope.py)")
KEYS = {"most plausible +100 bp 10Y": ("max_up_10Y", "value", 1), "most plausible -100 bp 10Y": ("max_down_10Y", "value", 1),
        "most plausible +50 bp 10Y in the recognition window": ("recog_10Y", "value", 1), "largest 10Y rise": ("max_up_10Y", "value", 1),
        "largest 10Y fall": ("max_down_10Y", "value", 1), "largest rise in the required return": ("rho_rise_max_pp", "value_pp", 2)}
ok_e, n_re = True, 0
for econ, blk, cls in ((e, E, rv.Dials), (eb, EB, rv.DialsB)):
    base = rv.run(econ, cls())
    ok_e &= all(blk["default_dials"][k] == (round(float(base[k]), 2) if base[k] is not None else None) for k in blk["default_dials"])
    ok_e &= blk["solved"] + blk["no_equilibrium"] + blk["other_failures"] == blk["draws"] == len(U4)
    ok_e &= set(blk["picks"]) == set(KEYS)
    for name, pk in blk["picks"].items():
        if pk is None:
            continue
        key, field, nd = KEYS[name]
        o = rv.run(econ, rv.from_unit(U4[pk["draw"]], cls))
        ok_e &= round(float(o[key]), nd) == pk[field]
        n_re += 1
check("E1 the stored envelope re-runs: the default-dial outcomes and every pick reproduce from their draws, on the central and "
      "on (b); the draws add up; the ranges and the calibration are the code's",
      ok_e and E["ranges"] == {k: list(v) for k, v in rv.RANGES.items()} and E["ranges_b"] == {k: list(v) for k, v in rv.RANGES_B.items()}
      and E["calibration"]["tag"] == info["tag"]
      and E["calibration"]["rho"] == e.rho and EB["calibration"]["rho"] == eb.rho,
      f"{n_re} picks re-run; draws {E['draws']} each")

print("F — the findings (the envelope on the refit, the central against (b) on its own dials; stated as found)")
ev, evb = E["envelope"], EB["envelope"]
CURVE = ("recog_10Y", "max_up_10Y", "max_down_10Y", "ten_year_2Y")
dr, drb = E["drivers_rank_corr"], EB["drivers_rank_corr"]
top2 = lambda d, o: [k for k, _ in sorted(d[o].items(), key=lambda kv: -abs(kv[1]))[:2]]  # noqa: E731
q3 = lambda d, k, f="+.0f": " / ".join(format(d[k][q], f) for q in ("p5", "p50", "p95"))  # noqa: E731
sh, shb = E["shares"], EB["shares"]
check("F1 [restated at the refit] the sign of the curve's move is nearly pinned on the refit, downward: the 10Y falls through the "
      "recognition window in 95% of draws (its 95th percentile below zero) and over ten years in more than nine in ten, where on (b) and "
      "before the refit the sign was open; owners' saving still drives every curve outcome most (down), deficits push the other way "
      "(up) — second in three of the four, behind the market's prior for the largest fall; the investment key's scale ranks below both",
      ev["recog_10Y"]["p95"] < 0 < evb["recog_10Y"]["p95"] and sh["ten_year_10Y_negative"] > 0.9 and evb["ten_year_10Y"]["p5"] < 0 < evb["ten_year_10Y"]["p95"]
      and all(top2(dr, o)[0] == "alpha_rent" and dr[o]["alpha_rent"] < 0 < dr[o]["alpha_fiscal"] for o in CURVE)
      and sum(top2(dr, o)[1] == "alpha_fiscal" for o in CURVE) == 3
      and all(abs(dr[o]["alpha_inv"]) < min(abs(dr[o]["alpha_rent"]), abs(dr[o]["alpha_fiscal"])) for o in CURVE),
      f"10Y over ten years 5/50/95%: {q3(ev, 'ten_year_10Y')} bp ((b) {q3(evb, 'ten_year_10Y')}); recognition window "
      f"{q3(ev, 'recog_10Y')} ((b) {q3(evb, 'recog_10Y')}); falls over ten years in {sh['ten_year_10Y_negative']:.0%} ((b) "
      f"{shb['ten_year_10Y_negative']:.0%}); rank corr. in the window: owners' saving {dr['recog_10Y']['alpha_rent']:+.2f} ((b) "
      f"{drb['recog_10Y']['alpha_rent']:+.2f}), deficits {dr['recog_10Y']['alpha_fiscal']:+.2f} ({drb['recog_10Y']['alpha_fiscal']:+.2f}), "
      f"investment {dr['recog_10Y']['alpha_inv']:+.2f} ((b)'s pace key {drb['recog_10Y']['alpha_capex']:+.2f}); second for the largest fall: "
      f"{top2(dr, 'max_down_10Y')[1]}")
check("F2 [restated at the refit] the tails turn: the fall side dominates — the 10Y never falls in under one draw in ten (on (b) a "
      "quarter; before the refit a third) and policy reaches the floor in more than half ((b) a fifth); the rise side is shorter than "
      "(b)'s at its 95th percentile, over ten years and at its largest move, though its single largest draw goes further",
      sh["10Y_never_falls"] < 0.1 < shb["10Y_never_falls"] and sh["policy_reaches_floor"] > 0.5 > shb["policy_reaches_floor"]
      and ev["ten_year_10Y"]["p95"] < evb["ten_year_10Y"]["p95"] and ev["max_up_10Y"]["p95"] < evb["max_up_10Y"]["p95"]
      and ev["max_up_10Y"]["max"] > evb["max_up_10Y"]["max"],
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
att = {(lab, nm): rv.attribute(econ, rv.from_unit(U4[blk[nm]["draw"]], cls), KEYS[nm][0], thr, listed=tuple(blk[nm]["dials_moved_default_to_draw"]))
       for lab, econ, blk, cls in (("c", e, pk, rv.Dials), ("b", eb, pkb, rv.DialsB)) for nm, thr in ((P100, 100.0), (M100, -100.0), (P50, 50.0))}
a1, a1b, am, a50 = att[("c", P100)], att[("b", P100)], att[("c", M100)], att[("c", P50)]
FISCAL = ("tp_per_debt", "public_support")
check("F5 [restated at the refit] a +100 bp rise lies farther from the defaults on the refit than on (b), and what it needs — found by "
      "re-running the draw with dial subsets, not by the listing of dials moved more than 0.15 of their range — is the two direction "
      "bridges together with fiscal strain: owners' saving below its default, deficits above it, and a larger term premium per point of "
      "debt and more public support; the direction bridges alone, or reset, give no rise, the listed dials alone give it. The +50 bp in "
      "the recognition window needs the investment key's scale below its default as well as the two bridges. A -100 bp fall needs "
      "nothing: the default dials already reach it, and its most plausible draw is the same as (b)'s",
      up["distance"] > upb["distance"] and a1["at_draw"] >= 100.0 and a1["direction_bridges_only"] < 100.0 and a1["direction_bridges_reset"] < 100.0
      and a1["listed_dials_only"] >= 100.0 and set(rv.DIRECTION) | set(FISCAL) <= set(a1["needed"])
      and a1["direction_bridges"]["alpha_rent"][1] < a1["direction_bridges"]["alpha_rent"][0]
      and a1["direction_bridges"]["alpha_fiscal"][1] > a1["direction_bridges"]["alpha_fiscal"][0]
      and a50["at_draw"] >= 50.0 and set(a50["needed"]) == {"alpha_inv", *rv.DIRECTION}
      and dn["draw"] == pkb[M100]["draw"] and am["needed"] == [] and E["default_dials"]["max_down_10Y"] <= -100.0
      and all(blk[nm]["cause_by_subset"] == att[(lab, nm)] for lab, blk in (("c", pk), ("b", pkb)) for nm in (P100, M100, P50)),
      f"+100: draw {up['draw']}, distance {up['distance']:.3f} ((b) {upb['distance']:.3f}), {a1['at_draw']:+.1f} bp; owners' saving "
      f"{a1['direction_bridges']['alpha_rent'][0]:g} -> {a1['direction_bridges']['alpha_rent'][1]:.3f}, deficits "
      f"{a1['direction_bridges']['alpha_fiscal'][0]:g} -> {a1['direction_bridges']['alpha_fiscal'][1]:.3f}; those two alone "
      f"{a1['direction_bridges_only']:+.1f}, reset {a1['direction_bridges_reset']:+.1f}, the listed alone {a1['listed_dials_only']:+.1f}; needed "
      f"{a1['needed']}. (b)'s +100 (draw {upb['draw']}, {a1b['at_draw']:+.1f}): needed {a1b['needed']}. +50 in the window: draw {pk[P50]['draw']}, "
      f"{a50['at_draw']:+.1f}, needed {a50['needed']}. -100: draw {dn['draw']}, {am['at_draw']:+.1f} bp ((b) {att[('b', M100)]['at_draw']:+.1f}); "
      f"default dials {E['default_dials']['max_down_10Y']:+.1f}")
rr, prr = ev["rho_rise_max_pp"], pk["largest rise in the required return"]
check("F6 [restated at the refit] every draw has a land-scarce equilibrium at every date, on the central and on (b): none is lost to "
      "NoEquilibrium, and the largest rise in the required return stays inside the central's headroom at its start (before the refit it "
      "went past it, solving because deep automation had moved the machine chain's ceiling out)",
      E["no_equilibrium"] == 0 and EB["no_equilibrium"] == 0 and E["other_failures"] == 0 and EB["other_failures"] == 0
      and E["solved"] == E["draws"] and prr["value_pp"] == rr["max"] and rr["max"] < info["headroom_pp"],
      f"solved {E['solved']}/{E['draws']} ((b) {EB['solved']}/{EB['draws']}); the largest rise in the required return {rr['max']:.2f} pp "
      f"(draw {prr['draw']}) against a headroom of {info['headroom_pp']:.2f} pp at the start")

fails = [nm for nm, ok, _ in RESULTS if not ok]
print(f"\n{len(RESULTS) - len(fails)}/{len(RESULTS)} checks passed")
print(f"ALL GREEN ({len(RESULTS)})" if not fails else "FAILURES: " + "; ".join(nm.split(' ')[0] for nm in fails))
sys.exit(0 if not fails else 1)
