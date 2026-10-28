# check_speed.py — markets at machine speed: the learner's capacity, trust, shared error and digestion;
# the variance-ratio estimators behind the digestion history; and the findings, stated as found.
#
# The worlds run on calibration (c)'s central economy since her decision of 2026-09-30 (macro.central(), the return
# following r* from its own rho, lambda to a fifth of its own start); W1 gates the (b) comparator as the pre-switch worlds
# and results/speed.json's world readouts against a rebuild, W2 the whole of results/speed.json (about two minutes).
# The market's signal is all wages over income (recognition.Learning's default), not the paper's Figure 7 basis; on (c) the
# two differ (check_recognition S3), on (b) they coincide.
# Thresholds set after seeing (c)'s numbers: F4's "more than a year earlier" (1.0) and "under half the rate headroom" (0.5)
# (flagged here). F1's 0.2, F3's five times and 1%, L- and H-tolerances predate the switch.
# Restated at the refit (2026-10-27, Log 46; the central on the bridges refit on (c) in macro.BRANCHES, (b) on its own), as
# found: F2 reads the ladder in size (the news world's 10Y now falls); F4 states that the two branches no longer split the
# direction on the central — both move the 10Y down through recognition. Unflagged at the refit (checks:T1, S1): F2's "x100 as
# far as instant" read |x100 - instant| < 0.1 bp, and its world was not the stored deficits branch but the refit's base with
# (b)'s deficits dials (alpha_fiscal 0.25, alpha_rent 0.02), a ladder about half the branch's (-0.8 ... -14.7 against -1.5 ...
# -28.1 bp); on the branch the 0.1 bp clause failed (0.136).
# Restated at the revision (2026-10-28, Log 54; decisions 93-96): F2 is rebuilt on the stored deficits branch
# (speed_scenarios.SCEN, macro.BRANCHES) and gated equal to speed.json's first-week 10Y (to its 0.1 bp rounding); its "x100 as far
# as instant" is the digestion rung's arithmetic, set in advance — in its first week the x100 market prices 1 - 0.5^((1/52)/0.0025)
# = 99.52% of the news, and the 10Y's move is proportional to the belief's (L6 carried to the curve) — replacing the 0.1 bp
# tolerance; its sign (down) and the strict rise of |the move| along the ladder were seen in the revision's planning run (flagged:
# -0.87 / -6.96 / -13.85 / -16.76 / -16.84 bp; at the refit, on the hybrid world, -0.8 / -6.1 / -12.1 / -14.7 / -14.7). On the
# revision's hybrid world the move turned up (+0.2 ... +4.0 bp): the old construction no longer read the branch's direction. F4's
# headroom clause holds vacuously on the refit (no world's required return rises, 0.00 pp): a regression guard (checks:V1); the
# headroom's live tests on (c) are check_reverse F6 and check_macro_scenarios R3.
# Restated at the verification (2026-10-28, Log 54's last bullet; the verifiers' finding that her call (1) wants every claim that
# rests on the investment key's pass-through stated conditionally, and that F4 stated the deficits branch's direction outright while
# gating only the gross reading; flagged): F4's label says "at the gross reading of the investment key (the central)", its gate
# unchanged; F5 new, set after seeing, a readout as bank R7 is: the deficits branch through recognition at a pass-through of 1 / 0.6
# / 0.4 / 0, its 10Y -25.9 / -0.2 / +12.8 / +38.8 bp (over ten years -64 / +22 / +65 / +151), its r* peaking at its start (0.75%) at
# gross and at 0.79 / 1.11 / 2.04% below it, the required return up 0.00 / 0.03 / 0.36 / 1.30 pp; the owners'-saving branch -158 bp
# netted. Gated on the found direction: the 10Y's move rising as the pass-through falls, down at gross, up at 0.4 and below.
#
# Run from paths/:  ../venv/Scripts/python.exe checks/check_speed.py
# Exit status 0 only if every check passes.

from __future__ import annotations

import os
import sys
from dataclasses import replace

import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "code"))
import json  # noqa: E402

import digestion_history as dh  # noqa: E402
import macro as m  # noqa: E402
import recognition as rc  # noqa: E402
import regimes as rg  # noqa: E402
import speed_scenarios as ss  # noqa: E402

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


logit = lambda p: np.log(p / (1 - p))  # noqa: E731
e, _ = m.central()


def worlds(dt=0.25, **bridges):
    br = m.feedback_bridges(e, **bridges)
    old = m.macro_path(e, m.hold_tech(e), br, 25.0, 0.25)
    new = m.macro_path(e, m.deep_tech(e), br, 25.0, 0.25)
    return (old, new) if dt == 0.25 else (rc.refine(old, dt), rc.refine(new, dt))


oq, nq = worlds()
ow, nw = worlds(1 / 52)
tq, tw = oq["t"], ow["t"]
base = rc.Learning(sigma=1.0, p0=0.05)

print("L — the learner at machine speed")
same = all(np.array_equal(rc.learn(oq, nq, replace(base, seed=3)), rc.learn(oq, nq, replace(base, seed=3, trust=tr)))
           for tr in (1.0, (2.0, 3.0), "technology"))
check("L1 at capacity 1 trust changes nothing: the learner is today's, noise draws included", same)
c = 7.0
a1 = rc.learn(oq, nq, replace(base, seed=5, trust=1.0, capacity_end=c))
a2 = rc.learn(oq, nq, replace(base, seed=5, sigma=1.0 / np.sqrt(c)))
check("L2 a constant capacity c is a learner with noise sigma/sqrt(c), draw for draw (to rounding)",
      np.max(np.abs(a1 - a2)) < 1e-12, f"max difference {np.max(np.abs(a1 - a2)):.1e}")
lr = replace(base, capacity_end=30.0, trust_lead=3.0)
_, lo = rc.learn(ow, nw, lr, return_logodds=True)
cap = rc.capacity_path(ow, nw, lr)
d = (nw["labor_share"] - ow["labor_share"]) * 100
closed = logit(0.05) + np.concatenate([[0.0], np.cumsum(cap[1:] * (np.diff(tw) / 0.25) * d[1:] ** 2 / 2.0)])
check("L3 with capacity growing along the path, noiseless log odds = logit(p0) + sum c (dt/0.25) (s_new - s_old)^2 / (2 sigma^2)",
      np.max(np.abs(lo - closed)) < 1e-9 * max(1.0, np.max(np.abs(closed))))
_, lo_big = rc.learn(oq, nq, replace(base, trust=1.0, capacity_end=1e12, common=0.5), return_logodds=True)
_, lo_floor = rc.learn(oq, nq, replace(base, sigma=0.5), return_logodds=True)
check("L4 a shared error is a floor: aware, unlimited capacity learns exactly as fast as a learner whose only noise is the shared part",
      np.max(np.abs(lo_big - lo_floor)) < 1e-6 * np.max(np.abs(lo_floor)))
_, lo_aw = rc.learn(oq, nq, replace(base, trust=1.0, capacity_end=10.0, common=0.5), return_logodds=True)
_, lo_un = rc.learn(oq, nq, replace(base, trust=1.0, capacity_end=10.0, common=0.5, aware=False), return_logodds=True)
_, lo_un0 = rc.learn(oq, nq, replace(base, trust=1.0, capacity_end=10.0, aware=False), return_logodds=True)
_, lo_aw0 = rc.learn(oq, nq, replace(base, trust=1.0, capacity_end=10.0), return_logodds=True)
check("L5 unaware of the shared error, the market over-updates (larger steps); with no shared error the two coincide",
      np.all(np.diff(lo_un) >= np.diff(lo_aw) - 1e-12) and lo_un[-1] > lo_aw[-1] and np.array_equal(lo_un0, lo_aw0))
h, f, dj, tj = 0.1, 0.6, 3.0, 2.0
p_d = rc.learn(ow, ow, replace(base, digest=h, digest_share=f, jumps=((tj, dj),)))
j = int(np.nonzero(tw >= tj)[0][0])
k = np.arange(len(tw) - j) + 1
p1 = 1 / (1 + np.exp(-(logit(0.05) + dj)))
expect = 0.05 + (p1 - 0.05) * ((1 - f) + f * (1 - 0.5 ** (k * (1 / 52) / h)))
check("L6 digestion acts on the belief: news is priced (1 - share) at once and the rest with the stated half-life, exactly",
      np.max(np.abs(p_d[j:] - expect)) < 1e-12 and np.allclose(p_d[:j], 0.05),
      f"in the week of the news {1 - f + f * (1 - 0.5 ** (1 / 52 / h)):.2f} of the move; after one half-life {1 - f + f / 2:.2f}")
tr_old = rc.trust_path(ow, nw, replace(base, truth="old"))
tr_new = rc.trust_path(ow, nw, replace(base, trust_lead=2.0))
prog = (nw["eta"][0] - nw["eta"]) / (nw["eta"][0] - nw["eta"][-1])
check("L7 trust that follows the technology never arrives in the status quo, and in the new world is its automation progress, led",
      np.all(tr_old == 0) and np.allclose(tr_new, np.clip(np.interp(tw + 2.0, tw, prog), 0, 1))
      and np.all(np.diff(tr_new) >= -1e-12))
check("L8 refine keeps every original date exactly and is linear between them",
      np.allclose(np.interp(tq, tw, ow["labor_share"]), oq["labor_share"], atol=1e-12)
      and abs(ow["labor_share"][6] - np.interp(tw[6], tq, oq["labor_share"])) < 1e-12)
dates = [rc.crossing(tw, rc.learn(ow, nw, replace(base, digest=0.25, capacity_end=cc, trust_lead=3.0)), 0.5) for cc in (1, 3, 10, 30, 100)]
check("L9 more capacity, earlier recognition: the one-half date falls with capacity", np.all(np.diff(dates) < 0),
      "capacity 1/3/10/30/100: " + " ".join(f"{x:.2f}" for x in dates))

print("H — the digestion-history estimators")
rng = np.random.default_rng(11)
iid = rng.normal(size=60_000)
ar = np.empty(60_000); ar[0] = 0.0
phi = 0.3
eps = rng.normal(size=60_000)
for i in range(1, len(ar)):
    ar[i] = phi * ar[i - 1] + eps[i]
vr_ar = lambda q: 1 + 2 * np.sum((1 - np.arange(1, q) / q) * phi ** np.arange(1, q))  # noqa: E731
check("H1 the variance ratio is 1 for independent changes and matches the AR(1) formula for persistent ones",
      all(abs(dh.variance_ratio(iid, q) - 1) < 0.05 for q in (5, 21)) and all(abs(dh.variance_ratio(ar, q) - vr_ar(q)) < 0.06 for q in (5, 21)),
      f"AR(0.3): VR(21) {dh.variance_ratio(ar, 21):.3f} vs {vr_ar(21):.3f}")
f0, h0 = 0.75, 10.0
lam = 1 - 0.5 ** (1 / h0)
news = rng.normal(size=200_000)
# the partial-digestion process: each shock priced f at once, the rest drifting in with half-life h
pending = 0.0
dp = np.empty_like(news)
for i in range(len(news)):
    pending += (1 - f0) * news[i]
    drift = lam * pending
    pending -= drift
    dp[i] = f0 * news[i] + drift
Qs = dh.Q
sim = np.array([dh.variance_ratio(dp, q) for q in Qs])
model = dh.vr_partial(Qs, f0, h0)
fh = dh.fit_partial(sim)
check("H2 the partial-digestion model's variance ratios match a simulated series, and the fit recovers its share and half-life",
      np.max(np.abs(sim - model)) < 0.06 and abs(fh[0] - f0) < 0.05 and abs(fh[1] - h0) / h0 < 0.3,
      f"fit: {fh[0]:.2f} at once, half-life {fh[1]:.1f} days (true 0.75, 10)")
dy = dh._lc.pull_fred("DGS10").diff().dropna() * 100
vr21 = {a: dh.variance_ratio(dy[a:b].values, 21) for _, a, b in dh.ERAS}
z21 = {a: dh.variance_ratio_z(dy[a:b].values, 21) for _, a, b in dh.ERAS}
check("H3 found: before 1995 news drifted into the 10Y (21-day ratio above 1.2, z above 1.96); since 1995 it does not (0.85 to 1.1)",
      vr21["1962"] > 1.2 and vr21["1982"] > 1.2 and z21["1962"] > 1.96 and z21["1982"] > 1.96
      and 0.85 < vr21["1995"] < 1.1 and 0.85 < vr21["2009"] < 1.1,
      " ".join(f"{a}: {v:.2f} (z {z21[a]:+.1f})" for a, v in vr21.items()))

print("F — the findings (default worlds; stated as found)")
trust_at = []
for cc in (3, 10, 30, 100):
    lrc = replace(base, digest=0.25, capacity_end=cc)
    p = rc.learn(ow, nw, lrc)
    trust_at.append(float(rc.trust_path(ow, nw, lrc)[int(np.searchsorted(tw, rc.crossing(tw, p, 0.5)))]))
check("F1 with trust following the economy's own automation, the market is past one half while trust in AI is still below 0.2",
      max(trust_at) < 0.2, "trust at recognition, capacity 3/10/30/100: " + " ".join(f"{x:.2f}" for x in trust_at))
od, nd = worlds(1 / 52, **ss.SCEN["deficits dominate"])       # the stored deficits branch (macro.BRANCHES), not (b)'s dials
T10 = np.array([10.0])
week = []
RUNGS = (("human, regime news (assumed)", 0.25, 1.0), ("x10", 0.025, 1.0), ("1980s rate news (measured)", 9.8 / 252, 0.25),
         ("x100", 0.0025, 1.0), ("instant", 0.0, 1.0))
for _, hh, sh in RUNGS:
    lj = replace(base, digest=hh, digest_share=sh)
    z1 = np.array([rg.zero(T10, mx)[0] for mx in rc.market_curves(od, nd, rc.learn(od, nd, replace(lj, jumps=((1.5, 4.0),))))[0]])
    z0 = np.array([rg.zero(T10, mx)[0] for mx in rc.market_curves(od, nd, rc.learn(od, nd, lj))[0]])
    i0 = int(np.searchsorted(tw, 1.5)) - 1
    week.append(float(((z1 - z0)[i0 + 1] - (z1 - z0)[i0]) * 100))
with open(os.path.join(os.path.dirname(HERE), "results", "speed.json"), encoding="utf-8") as fh:
    LADDER = json.load(fh)["2_abrupt_event_effect_bp"]["deficits dominate"]
stored_w = [LADDER[r_[0]]["1w"]["10Y"] for r_ in RUNGS]
x100_share = 1 - 0.5 ** ((1 / 52) / 0.0025)              # the x100 rung's first week: the share of the news priced (L6)
check("F2 [restated at the revision] the week after a lump of news, on the stored deficits branch, the 10Y moves further along the ladder "
      "(down, on the refit): human regime news, x10, 1980s rate news, x100, instant — and the x100 market moves 1 - 0.5^((1/52)/0.0025) "
      "= 99.52% of the instant one's move within the week, the digestion rung's arithmetic (set in advance); the ladder equals "
      "speed.json's first-week 10Y (at the refit the check ran a hybrid world, the refit's base with (b)'s deficits dials, about half the "
      "branch's ladder, and read 'as far as' to 0.1 bp)",
      np.all(np.diff(np.abs(week)) > 0) and np.all(np.asarray(week) < 0) and abs(week[3] / week[4] - x100_share) < 1e-3
      and all(abs(w_ - s_) <= 0.05 + 1e-9 for w_, s_ in zip(week, stored_w)),
      " ".join(f"{x:.2f}" for x in week) + f" bp (stored {' '.join(f'{x:.1f}' for x in stored_w)}); x100 / instant {week[3] / week[4]:.5f} "
      f"against {x100_share:.5f}")
fd = {}
for aware in (True, False):
    for cc in (1, 30):
        lf = replace(base, digest=0.25, trust=1.0, capacity_end=cc, common=0.5, aware=aware, truth="old")
        fd[(aware, cc)] = np.mean([rc.learn(ow, nw, replace(lf, seed=10_000 + s))[tw <= 15.0 + 1e-9].max() >= 0.5 for s in range(150)])
check("F3 fast and unaware of its shared error, the market sees false dawns far more often than today's or an aware one",
      fd[(False, 30)] > 5 * max(fd[(True, 30)], fd[(True, 1)], 0.01),
      f"150 draws: today {fd[(True, 1)]:.0%}, x30 aware {fd[(True, 30)]:.0%}, x30 unaware {fd[(False, 30)]:.0%}")

print("W — the worlds: the central, (b) the comparator (results/speed.json, rebuilt by code/speed_scenarios.py)")
with open(os.path.join(os.path.dirname(HERE), "results", "speed.json"), encoding="utf-8") as fh:
    SJ = json.load(fh)
eb, _, _, _ = m.calibrate(base=m.CAPITAL_BASE)
arr = lambda d: {k: v for k, v in d.items() if isinstance(v, np.ndarray)}  # noqa: E731
same = lambda a, b: arr(a).keys() == arr(b).keys() and all(np.array_equal(a[k], b[k]) for k in arr(a))  # noqa: E731
pre_b = []
for bkw in m.BRANCHES_B.values():
    br = replace(m.BRIDGES_B, capital_premium=5.0, **bkw)
    o0 = rc.refine(m.macro_path(eb, m.TechPath(eta_end=1.0, lam_end=eb.lam), br, 25.0, 0.25), ss.DT)
    n0 = rc.refine(m.macro_path(eb, m.TechPath(eta_end=0.04, lam_end=0.01, t_mid=6, width=6), br, 25.0, 0.25), ss.DT)
    o1, n1 = ss.worlds(eb, m.BRIDGES_B, **bkw)
    pre_b.append(same(o0, o1) and same(n0, n1))
Wc = {k: ss.worlds(e, **v) for k, v in ss.SCEN.items()}
Wb = {k: ss.worlds(eb, m.BRIDGES_B, **v) for k, v in m.BRANCHES_B.items()}
rt = lambda o: json.loads(json.dumps(o))  # noqa: E731
wc, wb = rt(ss.world_readouts(e, Wc)), rt(ss.world_readouts(eb, Wb))
check("W1 the (b) comparator's worlds are the pre-switch worlds array for array (Bridges(capital_premium=5.0, ...), TechPath(0.04, "
      "0.01, 6, 6)); the stored world readouts equal a rebuild on the central and on (b)",
      all(pre_b) and SJ["calibration"]["tag"] == "c_central_lo" and SJ["0_worlds"] == wc and SJ["comparator_b"]["0_worlds"] == wb,
      "central: " + "; ".join(f"{k} window {v['window']}" for k, v in wc.items()))
_, info_c = m.central()
full_c, full_b = rt(ss.compute(e)[0]), rt(ss.compute(eb, m.BRIDGES_B, m.BRANCHES_B)[0])
check("W2 results/speed.json equals a rebuild by code/speed_scenarios.py, block for block, on the central and on (b)",
      {k: v for k, v in SJ.items() if k not in ("calibration", "comparator_b")} == full_c and SJ["comparator_b"] == full_b
      and SJ["calibration"] == rt({k: info_c[k] for k in ("tag", "root", "rho", "capital_premium", "headroom_pp", "k", "source")}),
      "blocks: " + ", ".join(full_c))
dd, ds = "deficits dominate", "owners' saving dominates"
check("F4 [restated at the refit; its label at the revision and at the verification] at the gross reading of the investment key (the "
      "central) the two bridge settings no longer decide the direction: both move the 10Y down through recognition, the deficits branch "
      "least and owners' saving further than on (b), where they split (before the refit they split on the central too; below a "
      "pass-through of about 0.6 they split again: F5); the window opens more than a year earlier than (b)'s; no world's required return "
      "rises by half the rate headroom (at the gross reading none rises at all: a regression guard)",
      wc[ds]["10Y_through_recognition_bp"] < wc[dd]["10Y_through_recognition_bp"] < 0 < wb[dd]["10Y_through_recognition_bp"]
      and wc[ds]["10Y_through_recognition_bp"] < wb[ds]["10Y_through_recognition_bp"] < 0
      and all(wb[k]["window"][0] - wc[k]["window"][0] > 1.0 for k in (dd, ds))
      and max(v["required_return_rise_max_pp"] for v in wc.values()) < 0.5 * SJ["calibration"]["headroom_pp"],
      f"through recognition: deficits {wc[dd]['10Y_through_recognition_bp']:+.0f} bp ((b) {wb[dd]['10Y_through_recognition_bp']:+.0f}), saving "
      f"{wc[ds]['10Y_through_recognition_bp']:+.0f} ((b) {wb[ds]['10Y_through_recognition_bp']:+.0f}); windows {wc[dd]['window']} ((b) {wb[dd]['window']}); "
      f"required return up to {max(v['required_return_rise_max_pp'] for v in wc.values()):+.2f} pp of {SJ['calibration']['headroom_pp']:.2f}")

PTS = (1.0, 0.6, 0.4, 0.0)            # the investment key's pass-through (decision 93): 1 gross (the central) to 0 netted
pt_w = {p_: ss.worlds(e, **dict(ss.SCEN[dd], alpha_inv=m.investment_key(p_))) for p_ in PTS}
pt_r = {p_: rt(ss.world_readouts(e, {dd: pt_w[p_]}))[dd] for p_ in PTS}
k15 = int(round(15 / ss.DT))
pk_ = {p_: float(pt_w[p_][1]["r_star"][: k15 + 1].max()) for p_ in PTS}
r0_ = float(pt_w[1.0][1]["r_star"][0])
rec_ = [pt_r[p_]["10Y_through_recognition_bp"] for p_ in PTS]
rho_ = [pt_r[p_]["required_return_rise_max_pp"] for p_ in PTS]
os0 = rt(ss.world_readouts(e, {ds: ss.worlds(e, **dict(ss.SCEN[ds], alpha_inv=m.investment_key(0.0)))}))[ds]
check("F5 [new at the verification, set after seeing] readout, the investment key's pass-through (decision 93; as bank R7): the deficits "
      "branch's direction rests on it — through recognition its 10Y moves down at the gross reading (the central, F4, equal to the stored "
      "world), about nothing at 0.6 and up below it, rising as less of the investment fall counts, and once the pass-through is below gross "
      "its r* peaks above its start and its required return rises; the owners'-saving branch moves the 10Y down netted too",
      pt_r[1.0] == wc[dd] and np.all(np.diff(rec_) > 0) and rec_[0] < 0 < rec_[2]
      and abs(pk_[1.0] - r0_) < 1e-9 and all(pk_[p_] > r0_ for p_ in PTS[1:]) and np.all(np.diff([pk_[p_] for p_ in PTS]) > 0)
      and rho_[0] == 0 and all(x > 0 for x in rho_[1:]) and os0["10Y_through_recognition_bp"] < 0,
      "at a pass-through of 1 / 0.6 / 0.4 / 0: the deficits branch's 10Y through recognition " + " / ".join(f"{x:+.1f}" for x in rec_)
      + " bp, over ten years " + " / ".join(f"{pt_r[p_]['10Y_over_ten_years_bp']:+.0f}" for p_ in PTS) + "; its r* peak to year 15 "
      + " / ".join(f"{pk_[p_]:.2f}" for p_ in PTS) + f"% (start {r0_:.2f}); the required return up " + " / ".join(f"{x:.2f}" for x in rho_)
      + f" pp; owners' saving netted {os0['10Y_through_recognition_bp']:+.0f} bp")

fails = [n for n, ok, _ in RESULTS if not ok]
print(f"\n{len(RESULTS) - len(fails)}/{len(RESULTS)} checks passed")
print(f"ALL GREEN ({len(RESULTS)})" if not fails else "FAILURES: " + "; ".join(n.split(' ')[0] for n in fails))
sys.exit(0 if not fails else 1)
