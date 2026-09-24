# check_speed.py — markets at machine speed: the learner's capacity, trust, shared error and digestion;
# the variance-ratio estimators behind the digestion history; and the findings, stated as found.
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
import digestion_history as dh  # noqa: E402
import macro as m  # noqa: E402
import recognition as rc  # noqa: E402
import regimes as rg  # noqa: E402

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


logit = lambda p: np.log(p / (1 - p))  # noqa: E731
e, _, _, _ = m.calibrate(base=m.CAPITAL_BASE)


def worlds(dt=0.25, **bridges):
    br = m.Bridges(capital_premium=5.0, **bridges)
    old = m.macro_path(e, m.TechPath(eta_end=1.0, lam_end=e.lam), br, 25.0, 0.25)
    new = m.macro_path(e, m.TechPath(eta_end=0.04, lam_end=0.01, t_mid=6, width=6), br, 25.0, 0.25)
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
_, lo_d = rc.learn(ow, ow, replace(base, digest=h, digest_share=f, jumps=((tj, dj),)), return_logodds=True)
j = int(np.nonzero(tw >= tj)[0][0])
k = np.arange(len(tw) - j) + 1
expect = logit(0.05) + (1 - f) * dj + f * dj * (1 - 0.5 ** (k * (1 / 52) / h))
check("L6 digestion: news is priced (1 - share) at once and the rest with the stated half-life, exactly",
      np.max(np.abs(lo_d[j:] - expect)) < 1e-9 and np.allclose(lo_d[:j], logit(0.05)),
      f"in the week of the news {1 - f + f * (1 - 0.5 ** (1 / 52 / h)):.2f} of it; after one half-life {1 - f + f / 2:.2f}")
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
od, nd = worlds(1 / 52, alpha_fiscal=0.25, alpha_rent=0.02)
T10 = np.array([10.0])
week = []
for hh, sh in ((0.25, 1.0), (0.025, 1.0), (9.8 / 252, 0.25), (0.0025, 1.0), (0.0, 1.0)):
    lj = replace(base, digest=hh, digest_share=sh)
    z1 = np.array([rg.zero(T10, mx)[0] for mx in rc.market_curves(od, nd, rc.learn(od, nd, replace(lj, jumps=((1.5, 4.0),))))[0]])
    z0 = np.array([rg.zero(T10, mx)[0] for mx in rc.market_curves(od, nd, rc.learn(od, nd, lj))[0]])
    i0 = int(np.searchsorted(tw, 1.5)) - 1
    week.append(float(((z1 - z0)[i0 + 1] - (z1 - z0)[i0]) * 100))
check("F2 the week after a lump of news, the 10Y's move rises along the ladder: human regime news, x10, 1980s rate news, x100, instant",
      np.all(np.diff(week) > 0), " ".join(f"{x:.1f}" for x in week) + " bp")
fd = {}
for aware in (True, False):
    for cc in (1, 30):
        lf = replace(base, digest=0.25, trust=1.0, capacity_end=cc, common=0.5, aware=aware, truth="old")
        fd[(aware, cc)] = np.mean([rc.learn(ow, nw, replace(lf, seed=10_000 + s))[tw <= 15.0 + 1e-9].max() >= 0.5 for s in range(150)])
check("F3 fast and unaware of its shared error, the market sees false dawns far more often than today's or an aware one",
      fd[(False, 30)] > 5 * max(fd[(True, 30)], fd[(True, 1)], 0.01),
      f"150 draws: today {fd[(True, 1)]:.0%}, x30 aware {fd[(True, 30)]:.0%}, x30 unaware {fd[(False, 30)]:.0%}")

n_ok = sum(ok for _, ok, _ in RESULTS)
print(f"\n{n_ok}/{len(RESULTS)} checks passed")
sys.exit(0 if n_ok == len(RESULTS) else 1)
