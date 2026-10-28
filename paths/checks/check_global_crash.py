# check_global_crash.py — the crash model (code/global_crash.py: four economies, the euro area as France and the rest of
# the union since 2026-10-27), on the episodes' fit at a monthly step since 2026-10-28 (decision 91), refitted the same
# day on the measured bank runs and a debt deflation that levels off (decision 92): the fit is what it says and
# reproduces, the mechanics are what they say, the presets' dates are what the triggers would have set, and the findings,
# stated as found.
#
# Run from paths/:  ../venv/Scripts/python.exe checks/check_global_crash.py
# Exit status 0 only if every check passes.

from __future__ import annotations

import dataclasses
import json
import os
import sys
from dataclasses import replace

import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "code"))
import global_crash as gc  # noqa: E402
import episodes as ep  # noqa: E402

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


J = json.load(open(os.path.join(ROOT, "results", "global_crash.json"), encoding="utf-8"))
V, S = J["validation"], J["scenarios"]
cm, regs, fp, notes = gc.stored_model()          # the fit (results/episodes.json) at today's start
th = fp["fitted"]
DATES = {name: {r: (None if d is None else d["years"]) for r, d in ds.items()} for name, ds in J["preset_dates"].items()}
P = lambda name, rl=None: gc.dated(gc.PRESETS[name] if rl is None else rl, DATES[name])  # noqa: E731
N = gc.months(24)                                # 70 monthly steps, to the end of 2032Q2

print("D — the fit adopted at a monthly step (decision 91)")
check("D1 the step is a month: index 0 the end of September 2026, index k the end of the k-th month after; 24 quarterly "
      "indices are 70 steps (to June 2032, the end of 2032Q2) and 25 are 73; the stored results say so",
      gc.DT == 1 / 12 and J["step"] == "month" and gc.months(24) == 70 and gc.months(25) == 73
      and gc.month_label(0) == "2026-09" and gc.month_label(1) == "2026-10" and gc.month_label(N - 1) == "2032-06"
      and gc.quarter_label(23) == "2032Q2",
      f"step {J['step']}; months(24) {gc.months(24)}, the last {gc.month_label(N - 1)}")
x7 = np.arange(7.0)
qa = gc.to_quarters(x7, 1 / 12)
o = gc.simulate(regs, P("modern rules"), gc.ai_shock(N), cm, N)
qav = lambda x: np.array([x[0]] + [x[3 * j - 2:3 * j + 1].mean() for j in range(1, (len(x) - 1) // 3 + 1)])  # noqa: E731
oq = {r: {k: qav(v) for k, v in o[r].items()} for r in gc.R}            # the quarters' averages, taken here
gq = gc.quarterly_out(o)
sm = gc.summary(o, regs, 16)
four = min(sum(regs[r].size * oq[r]["y"][k] for r in gc.R) / sum(regs[r].size for r in gc.R) for k in range(16))
check("D2 the quarterly readings are the quarters' averages: index 0 the start's value and quarter j the average of its "
      "months 3j-2..3j (at a quarter's step the path itself), and the summary reads them, its '_quarter' fields and year "
      "4 (16 quarterly indices) on the quarters",
      np.array_equal(qa, [0.0, 2.0, 5.0]) and np.array_equal(gc.to_quarters(x7, gc.Q), x7)
      and all(np.allclose(gq[r][k], oq[r][k], atol=1e-12, rtol=0) for r in gc.R for k in o[r])
      and all(sm[r]["gap_min"] == round(float(oq[r]["y"][:16].min()), 2) and sm[r]["gap_min_quarter"] == int(np.argmin(oq[r]["y"][:16]))
              and sm[r]["unemployment_year2"] == round(float(oq[r]["u"][8]), 2)
              and sm[r]["unemployment_max_quarter"] == int(np.argmax(oq[r]["u"][:16])) for r in gc.R)
      and sm["four_weighted_gap_min"] == round(float(four), 2) and len(oq["US"]["y"]) == 24,
      f"US year 4: gap {sm['US']['gap_min']} in {gc.quarter_label(sm['US']['gap_min_quarter'])}, unemployment at its peak "
      f"{sm['US']['unemployment_max']} in {gc.quarter_label(sm['US']['unemployment_max_quarter'])}")
cm_j = gc.Common(**J["common"])
check("D3 the stored model is the fit: global_crash.json's common is episodes.stored_common (sigma 2.687, money 6.92, "
      "debt_deflation 0.5 at its bound, dd_sat 0.114, kappa_1930 0.195, a_r 0.03, a_f 0, f_speed 0.425, cap_oil 2.497; "
      "reprice and expect_over a year, fixed), its regions today's with the fitted Okun slopes, its validation the "
      "episodes' record. Restated 2026-10-28 after seeing the refit's run (decision 92; dd_sat added): at the first pass "
      "sigma 2.665, money 0, kappa_1930 0.137, f_speed 0.315, cap_oil 2.674",
      cm_j == cm and cm == ep.stored_common()
      and all(abs(getattr(cm, k) - th[k]) < 1e-12 for k in ("sigma", "money", "debt_deflation", "kappa_1930", "a_r", "a_f", "f_speed", "cap_oil", "dd_sat"))
      and cm.reprice == fp["fixed"]["reprice"] == 1.0 and cm.expect_over == fp["fixed"]["expect_over"] == 1.0
      and all({k: (list(v) if isinstance(v, tuple) else v) for k, v in regs[r].__dict__.items()} == J["regions"][r] for r in gc.R)
      and all(V[k] == fp[k] for k in ("fitted", "fixed", "bounds", "loss", "points", "housing"))
      and all(V["episodes"][nm] == {"fitted": e["fitted"], "loss": e["loss"], "rms": {t: x["rms"] for t, x in e["targets"].items()}}
              for nm, e in fp["episodes"].items()) and set(V["episodes"]) == set(fp["episodes"]),
      {k: round(float(getattr(cm, k)), 3) for k in ("sigma", "money", "debt_deflation", "dd_sat", "kappa_1930", "a_r", "a_f", "f_speed", "cap_oil", "reprice", "expect_over")})
import vintage  # noqa: E402
import pandas as pd  # noqa: E402
yr = lambda sid: float(vintage.read(sid).loc["2025-10-01":"2026-09-30"].mean())  # noqa: E731
h = ep.hlw()
check("D4 the regions' measured relief norm and neutral rate (decisions 85, 88 and 91): i_norm each central bank's rate "
      "averaged over the year to the start, recomputed here from the dated vintage (the Fed's effective funds rate, the "
      "ECB's deposit rate for the rest of the union and France, the Riksbank's policy rate; China none); r_star HLW's "
      "latest, 2026Q2 (the US 1.01, the euro area 0.09, France and Sweden the euro area's: no Swedish estimate; China the "
      "model's 0.75)",
      all(abs(regs[r].i_norm - yr(sid)) < 1e-12 for r, sid in (("US", "DFF"), ("EA", "ECBDFR"), ("FR", "ECBDFR"), ("SE", "SECBREPOEFF")))
      and regs["CN"].i_norm is None and notes["neutral_rate_HLW_quarter"] == "2026Q2" == str(h.index[-1])
      and regs["US"].r_star == float(h.loc["2026Q2", "US"]) and regs["EA"].r_star == regs["FR"].r_star == regs["SE"].r_star == float(h.loc["2026Q2", "EA"])
      and regs["CN"].r_star is None and cm.r_star == 0.75
      and round(regs["US"].r_star, 2) == 1.01 and round(regs["EA"].r_star, 2) == 0.09,
      {r: (None if regs[r].i_norm is None else round(regs[r].i_norm, 3), regs[r].i0,
           None if regs[r].r_star is None else round(regs[r].r_star, 3)) for r in gc.R})
check("D5 the Okun slopes abroad are the fit's (decision 91): the US its own episodes', Sweden its 1990-93, the rest of "
      "the union and France the euro area's 2011-13 (one episode for the whole area); China keeps its stated 0.25 (no "
      "episode). Restated 2026-10-28 after seeing the refit's run (decision 92): the US 0.681, Sweden 0.953, the euro "
      "area 1.226 (at the first pass 0.639, 0.931 and 1.225)",
      regs["US"].okun == th["okun_us"] and regs["SE"].okun == th["okun_se"] and regs["EA"].okun == regs["FR"].okun == th["okun_ea"]
      and regs["CN"].okun == 0.25 and round(th["okun_us"], 3) == 0.681 and round(th["okun_se"], 3) == 0.953 and round(th["okun_ea"], 3) == 1.226,
      {r: round(regs[r].okun, 3) for r in gc.R})
again = gc.preset_dates(cm, regs)
check("D6 the presets' dates reproduce: trigger_dates on each preset's central run (the dot-com-sized bust from the "
      "central day, drift and adoption as stored, robotics two years out, care absorbing, 70 monthly steps) gives the "
      "stored dates, month for month, and the stored labels name the month each lever starts",
      again == DATES and set(DATES) == set(gc.PRESETS)
      and all(J["preset_dates"][nm][r] is None or J["preset_dates"][nm][r]["from"] == gc.month_label(round(d / gc.DT) + 1)
              for nm, ds in DATES.items() for r, d in ds.items()),
      {nm: {r: (None if d is None else J["preset_dates"][nm][r]["from"]) for r, d in ds.items()} for nm, ds in DATES.items()})
first_ok = {}
for nm, rl in gc.PRESETS.items():
    oc = gc.simulate(regs, P(nm), gc.ai_shock(N), cm, N, waves=gc.CENTRAL_WAVES)
    for r in gc.R:
        ks = [k for k in range(1, N) if oc[r]["u"][k - 1] - regs[r].u0 >= rl.trigger]
        d = DATES[nm][r]
        first_ok[(nm, r)] = (d is None and not ks) or (d is not None and ks and abs(d - (ks[0] - 1) * gc.DT) < 1e-12)
check("D7 policy dated, not triggered (decisions 81 and 91): in each preset's central run on its stored dates, every "
      "region's lever starts at the end of the first month its unemployment reads the preset's trigger above the start "
      "(2 points; 1.5 for the guarantee and care), acting from the next month, and where a region never reads it, no "
      "lever starts",
      all(first_ok.values()), [k for k, v in first_ok.items() if not v])
undated = {nm: gc.simulate(regs, {r: replace(rl, fiscal_at=None, care_at=None) for r in gc.R}, gc.ai_shock(N), cm, N,
                           waves=gc.CENTRAL_WAVES) for nm, rl in gc.PRESETS.items()}


def apart_by(a, b) -> float:
    """The largest difference between two paths, equal infinities (a financing room without limit) and NaN pairs equal;
    NaN where only one is NaN, so that it fails a comparison (a bare max skipped NaN until 2026-10-28)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    same = (a == b) | (np.isnan(a) & np.isnan(b))
    with np.errstate(invalid="ignore"):            # inf - inf where both are inf: counted as same above
        return float(np.max(np.where(same, 0.0, np.abs(a - b)), initial=0.0))


moved = []
for nm, rl in gc.PRESETS.items():
    a_ = gc.simulate(regs, gc.dated(replace(rl, trigger=0.1), DATES[nm]), gc.ai_shock(N), cm, N, waves=gc.CENTRAL_WAVES)
    b_ = gc.simulate(regs, gc.dated(replace(rl, trigger=9.0), DATES[nm]), gc.ai_shock(N), cm, N, waves=gc.CENTRAL_WAVES)
    moved += [apart_by(a_[r][k], b_[r][k]) for r in gc.R for k in a_[r]]
moved = float(np.max(moved))                       # NaN if any path differs by NaN
past = all(float(o_[r]["u"].max() - regs[r].u0) >= gc.PRESETS[nm].trigger for nm, o_ in undated.items() for r in gc.R)
rise = {nm: round(float(o_["US"]["u"].max() - regs["US"].u0), 2) for nm, o_ in undated.items()}
check("D8 the model has no trigger branch: the trigger setting moves nothing in a run (it only sets dates); with no "
      "date, no discretionary lever starts — no stimulus, guarantee or cuts, no care build-out — though every region's "
      "unemployment rises past the trigger; and the rules have no 'what governments watch' (trigger_on is gone). Every "
      "path compared, the financing room's infinities included (until 2026-10-28 they made NaN, which the comparison "
      "skipped)",
      moved == 0.0 and all(not o_[r]["stim"].any() and not o_[r]["deficit_extra"].any() and not o_[r]["ax_cog"].any()
                           and not o_[r]["ax_phys"].any() for o_ in undated.values() for r in gc.R)
      and past and "trigger_on" not in {f.name for f in dataclasses.fields(gc.Rules)},
      f"largest change from the trigger setting {moved:.1e}; undated, US unemployment still rises {rise} points")
alone = {"US": regs["US"], **{r: gc.passive(r) for r in ("EA", "FR", "SE", "CN")}}
oa = gc.simulate(alone, {r: gc.MODERN for r in alone}, gc.ai_shock(N), cm, N, active=["US"])["US"]
oe = gc.simulate(alone, {r: gc.ERODED for r in alone}, gc.ai_shock(N), cm, N, active=["US"])["US"]
check("D9 no feedback from a region to itself (decision 91): the US alone with passive partners (size 0, as in the "
      "episodes), its trade on, gets nothing through the rest of the world (its own gap was the rest of the world's "
      "before) and nothing through the shared mood (its own stress was in it, on top of sigma): its trade term is zero "
      "(under eroding rules, until its tariffs arrive) and its spread sigma x capital lost (capped under the backstop), "
      "under today's rules and eroding ones",
      not oa["d_trade"].any() and oa["stress"].max() > 0.05 and np.allclose(oa["s"], np.minimum(cm.sigma * oa["stress"], regs["US"].spread_cap) + oa["premium"], atol=1e-12, rtol=0)
      and not oe["d_trade"][:gc.step_index(gc.ERODED.tariff_q, gc.DT)].any()
      and np.allclose(oe["s"], cm.sigma * oe["stress"] + oe["premium"], atol=1e-12, rtol=0),
      f"US capital lost {oa['stress'].max():.3f} (today's rules), {oe['stress'].max():.3f} (eroding); spread at most {oe['s'].max():.2f}")
om = gc.simulate(regs, P("modern rules"), gc.ai_shock(N), cm, N)
oe5 = gc.simulate(regs, P("rules erode under pressure"), gc.ai_shock(N), cm, N)
res_t, res_m = 0.0, 0.0
for r in gc.R:
    g = regs[r]
    union = lambda q: bool(g.union) and q != r and regs[q].union == g.union  # noqa: E731
    others = [q for q in gc.R if q != r and not union(q)]       # outside the region and its union
    wo = sum(regs[q].size for q in others)
    for k in range(1, N):
        y_ = {q: om[q]["y"][k - 1] for q in gc.R}
        y_["RoW"] = sum(regs[q].size * om[q]["y"][k - 1] for q in others) / wo
        spill = sum(v * (y_[q] - om[r]["y"][k - 1] if q != "RoW" and union(q) else y_[q]) for q, v in g.trade.items())
        res_t = max(res_t, abs(om[r]["d_trade"][k] - g.exports * cm.trade_elasticity * spill))
        mood = cm.global_mood * sum(regs[q].size * oe5[q]["stress"][k - 1] for q in others)
        outside_ = g.sov_pass * (oe5[r]["sov"][k] - g.sov_calm) if g.sov_debt > 0 else oe5[r]["premium"][k]
        res_m = max(res_m, abs(oe5[r]["s"][k] - (cm.sigma * oe5[r]["stress"][k] + mood + outside_)))
check("D10 and in the five regions together: each region's trade term reads its partners' gaps and, for the rest of the "
      "world, the size-weighted gap of the regions outside it and its union (renormalised); its spread, without a "
      "backstop, the shared mood of those regions' size-weighted capital lost (decision 91; recomputed here from the run, "
      "France's sovereign spread passed on included). Restated 2026-10-28 for the engine fix that leaves union partners "
      "out of both as well (E2's exact nesting back): at the first pass only the region itself was left out",
      res_t < 1e-12 and res_m < 1e-12, f"largest residuals: trade {res_t:.1e}, mood {res_m:.1e}")
bonly = {r: replace(g, drift=0.0) for r, g in regs.items()}
nodd = replace(cm, debt_deflation=0.0)
quiet = gc.simulate({r: replace(g, drift=0.0, eta=0.0) for r, g in regs.items()}, {r: gc.MODERN for r in gc.R}, gc.Shock(), cm, N)
drag0 = {r: round(-float(quiet[r]["d_debt"].min()), 2) for r in gc.R}
dd = {}
for lab_, rg, wv in (("the bust alone", bonly, gc.UNIFORM), ("the central run", regs, gc.CENTRAL_WAVES)):
    on_ = gc.simulate(rg, P("modern rules"), gc.ai_shock(N), cm, N, waves=wv)
    s_on, s_off = gc.summary(on_, regs), gc.summary(gc.simulate(rg, P("modern rules"), gc.ai_shock(N), nodd, N, waves=wv), regs)
    dd[lab_] = {"drag": {r: round(-float(on_[r]["d_debt"].min()), 2) for r in gc.R},
                "gap": {r: (s_on[r]["gap_min"], s_off[r]["gap_min"]) for r in gc.R},
                "four": (s_on["four_weighted_gap_min"], s_off["four_weighted_gap_min"])}
cr = dd["the central run"]
check("D11 the debt-deflation drag, a known consequence of adopting the fit (debt_deflation 0.5, at its bound, levelling "
      "off at an 11.4% shortfall, decision 92): it acts wherever the price level falls below the path at the region's "
      "target, so with no shock, no displacement and no lever France (core 1.77% at the start), Sweden (1.12%) and China "
      "(-0.07%) carry over half a point of GDP of it and the US and the rest of the union (above 2%) under a fifth; a bust "
      "deepens it, and it deepens the bust: by year 6 every region's trough is deeper with it than without, in the "
      "central run the four together's about twice as deep (over 1.9 times) and Sweden's over two and a half times. "
      "Stated as found 2026-10-28 after seeing the run (the worst drag, % of GDP; year-6 troughs with the drag and with "
      "debt_deflation 0); restated after seeing the refit's run (decision 92): the four's 1.99 times, at the first pass "
      "over twice (-9.09 against -4.20)",
      all(drag0[r] > 0.5 for r in ("FR", "SE", "CN")) and all(drag0[r] < 0.2 for r in ("US", "EA"))
      and all(v["gap"][r][0] < v["gap"][r][1] for v in dd.values() for r in gc.R)
      and cr["four"][0] < 1.9 * cr["four"][1] and cr["gap"]["SE"][0] < 2.5 * cr["gap"]["SE"][1],
      {"no shock": drag0, **dd})

print("V — history: the episodes' fit by month (results/episodes.json, decision 91)")
E = fp["episodes"]
theta = [th[k] for k in ep.PARAMS]
bd = fp["bounds"]
at_bound = sorted(k for k in ep.PARAMS if min(abs(th[k] - b) for b in bd[k]) < 1e-12)
loss_now = ep.loss(theta)
fitted_sum = sum(e["loss"] for e in E.values() if e["fitted"])
pts = sum(len(t["data"]) for e in E.values() if e["fitted"] for t in e["targets"].values())
check("V1 one parameter set for every crash: fourteen parameters (dd_sat the fourteenth, decision 92) fitted jointly by a "
      "global search on nine episodes by month, reprice and expect_over fixed at a year; the loss recomputes from the "
      "stored parameters (424.54 on 966 points), is the fitted episodes' sum and leaves the dot-com bust out; stated as "
      "found 2026-10-28 after seeing the run: three parameters at a bound (a_r and a_f at their floors, debt_deflation "
      "at its ceiling). Restated after seeing the refit's run: at the first pass thirteen parameters, loss 452.0, five at "
      "a bound (money at its floor and 1930's spending collapse at its ceiling as well)",
      list(th) == list(ep.PARAMS) and len(th) == 14 and all(bd[k][0] <= th[k] <= bd[k][1] for k in ep.PARAMS) and abs(loss_now - fp["loss"]) < 1e-3
      and abs(fitted_sum - fp["loss"]) < 0.01 and pts == fp["points"] == 966 and not E["2000-03"]["fitted"]
      and round(fp["loss"], 2) == 424.54
      and sum(e["fitted"] for e in E.values()) == 9 and at_bound == sorted(["a_r", "a_f", "debt_deflation"]),
      f"loss {loss_now:.3f} (stored {fp['loss']}), {pts} points; at a bound {at_bound}; by episode "
      + ", ".join(f"{nm} {e['loss']:.1f}" for nm, e in E.items()))
tg = lambda nm, t: (np.array(E[nm]["targets"][t]["model"]), np.array(E[nm]["targets"][t]["data"]), E[nm]["targets"][t]["periods"])  # noqa: E731
mo, do, _ = tg("1929-33", "output")
mu, du, _ = tg("1929-33", "unemployment")
mp, dp, pp = tg("1929-33", "prices")
ms, ds_, ps = tg("1929-33", "credit spread")
check("V2 1929-33 by month, the 1930s' rules dated as they came, the bank runs measured (R1): annual output within 5% "
      "and unemployment within 4 points each year; the model's slump runs ahead of the data's in 1930 and behind it in "
      "1932, and does not turn in 1933 (it has no end of the gold standard): its price level falls between 5 and 12 points "
      "further than the data's, still falling in December 1933 where the data's turned in March; all bank capital is "
      "lost, so the spread peaks at sigma, under the data's. Restated 2026-10-28 after seeing the refit's run (decision "
      "92; these bounds set then): at the first pass output within 9%, unemployment within 7 points and the price "
      "level's trough within 2% of the data's",
      np.abs(mo - do).max() < 0.05 and np.abs(mu - du).max() < 4 and 0.05 < dp.min() - mp.min() < 0.12
      and int(np.argmin(mp)) == len(mp) - 1 and pp[int(np.argmin(dp))] == "1933-03"
      and mu[0] > du[0] and mu[2] < du[2] and mo[3] < do[3] and E["1929-33"]["bank_capital_lost_max"] == 1.0
      and abs(ms.max() - cm.sigma) < 1e-3 and ms.max() < ds_.max(),
      f"output {np.round(mo, 3).tolist()} against {np.round(do, 3).tolist()}; unemployment {np.round(mu, 1).tolist()} against "
      f"{du.tolist()}; prices at the trough {mp.min():.3f} ({pp[int(np.argmin(mp))]}) against {dp.min():.3f} "
      f"({pp[int(np.argmin(dp))]}); spread at most {ms.max():.2f} against {ds_.max():.2f} ({ps[int(np.argmax(ds_))]})")
mu, du, pu = tg("2008-10", "unemployment")
my, dy, py = tg("2008-10", "output gap")
check("V3 2008-10 by month, today's rules, the Recovery Act on its date: the output gap's trough within 1.5 points of the "
      "data's and unemployment's peak within 1.5 points; the stated bias holds on the monthly fit — unemployment recovers "
      "from 2009 faster than the US's did (end-2010 more than a point below the data) while the gap does not (within a "
      "point): optimistic about how long joblessness lasts. Stated as found 2026-10-28 after seeing the run: the trough on the data's, the peak "
      "under a point short and eight months early (restated after seeing the refit's run: at the first pass a point "
      "short)",
      abs(my.min() - dy.min()) < 1.5 and abs(mu.max() - du.max()) < 1.5 and mu[-1] < du[-1] - 1.0 and abs(my[-1] - dy[-1]) < 1.0,
      f"trough {my.min():.2f} ({py[int(np.argmin(my))]}) against {dy.min():.2f} ({py[int(np.argmin(dy))]}); peak {mu.max():.2f} "
      f"({pu[int(np.argmax(mu))]}) against {du.max():.2f} ({pu[int(np.argmax(du))]}); end-2010 unemployment {mu[-1]:.2f} against "
      f"{du[-1]:.2f}, gap {my[-1]:.2f} against {dy[-1]:.2f}; core inflation RMS {E['2008-10']['targets']['core inflation']['rms']:.2f}")
mu, du, pu = tg("2000-03", "unemployment")
my, dy, py = tg("2000-03", "output gap")
check("V4 out of sample, the dot-com bust (March 2000 to December 2003, today's rules, the 2001 tax cut on its date, "
      "measured equity, equipment and exports; not in the fit): the unemployment peak and the output trough within 1.5 "
      "points of the data, as V3 asks of 2008-10, and unemployment's RMS error under 0.75 (by month since 2026-10-28; by "
      "quarter before). Stated as found 2026-10-28 after seeing the run: RMS 0.50, the gap's 1.24; the peak three months "
      "before the data's (the quarterly fit's came seven quarters early; restated after seeing the refit's run, at the "
      "first pass RMS 0.55 and 1.26)",
      abs(mu.max() - du.max()) < 1.5 and abs(my.min() - dy.min()) < 1.5 and E["2000-03"]["targets"]["unemployment"]["rms"] < 0.75
      and not E["2000-03"]["fitted"],
      f"peak {mu.max():.2f} ({pu[int(np.argmax(mu))]}) against {du.max():.2f} ({pu[int(np.argmax(du))]}); trough {my.min():.2f} "
      f"({py[int(np.argmin(my))]}) against {dy.min():.2f}; RMS unemployment {E['2000-03']['targets']['unemployment']['rms']:.2f}, "
      f"gap {E['2000-03']['targets']['output gap']['rms']:.2f}")
pk = {nm: (round(float(tg(nm, "unemployment")[0].max()), 2), round(float(tg(nm, "unemployment")[1].max()), 2)) for nm in ("1937-38", "1973-75", "1981-82", "1990-91")}
gp = {nm: (round(float(tg(nm, "output gap")[0].min()), 2), round(float(tg(nm, "output gap")[1].min()), 2)) for nm in ("1973-75", "1981-82", "1990-91")}
check("V5 the other US recessions, stated as found 2026-10-28 after seeing the run: 1973-75 close (unemployment's peak within half a point, "
      "the gap's trough within 1.5 points); 1990-91 a milder slump than the data's (the peak within 1.5 points); the "
      "fit misses 1981-82 (the Volcker recession barely appears: the peak over 3 points short, the gap over 4 points "
      "short) and 1937-38 (the peak over 7 points short), and those two carry over half of the fit's loss",
      abs(pk["1973-75"][0] - pk["1973-75"][1]) < 0.5 and abs(gp["1973-75"][0] - gp["1973-75"][1]) < 1.5
      and abs(pk["1990-91"][0] - pk["1990-91"][1]) < 1.5 and pk["1981-82"][1] - pk["1981-82"][0] > 3
      and gp["1981-82"][0] - gp["1981-82"][1] > 4 and pk["1937-38"][1] - pk["1937-38"][0] > 7
      and E["1981-82"]["loss"] + E["1937-38"]["loss"] > fp["loss"] / 2,
      f"unemployment peaks (model, data) {pk}; gap troughs {gp}; losses 1981-82 {E['1981-82']['loss']}, 1937-38 {E['1937-38']['loss']} of {fp['loss']}")
ab = {nm: (E[nm]["targets"]["unemployment"]["rms"], round(float(tg(nm, "unemployment")[0].max() - tg(nm, "unemployment")[1].max()), 2),
           round(float(tg(nm, "output gap")[0].min() - tg(nm, "output gap")[1].min()), 2)) for nm in ("Sweden 1990-93", "euro area 2011-13", "Japan 1991-95")}
check("V6 abroad, each economy one region with its central bank's rate as set and its fiscal stance as measured (decision "
      "89), stated as found 2026-10-28 after seeing the run: unemployment's RMS under 0.55 points and its peak within half a point of the "
      "data's in each; the output gap's trough within 2.5 points (Sweden's deeper than the data's, the euro area's and "
      "Japan's shallower)",
      all(v[0] < 0.55 and abs(v[1]) < 0.5 and abs(v[2]) < 2.5 for v in ab.values())
      and ab["Sweden 1990-93"][2] < 0 < ab["euro area 2011-13"][2] and ab["Japan 1991-95"][2] > 0,
      f"(unemployment RMS, peak against the data's, trough against the data's): {ab}")
okun = th["okun_us"]
b0 = {e.name: e for e in ep.episodes(theta)}
qrun = {"1929-33": gc.run_1929(cm, okun, th["impulse_1930_pct_gdp"]), "2008-10": gc.run_2007(cm, okun), "2000-03": gc.run_2000(cm, okun)}
mq = {nm: gc.quarterly_out({"US": b0[nm].run(cm)}, ep.M)["US"] for nm in qrun}
dif = {nm: (round(float(np.abs(qrun[nm]["u"] - mq[nm]["u"][:len(qrun[nm]["u"])]).max()), 2),
            round(float(np.abs(qrun[nm]["y"] - mq[nm]["y"][:len(qrun[nm]["y"])]).max()), 2)) for nm in qrun}
check("V7 the quarterly check of the monthly fit: run_2007 and run_2000 at a quarter's step, on the same parameters and "
      "the same dated levers, stay within half a point of the monthly episodes' unemployment and within a point of their "
      "gap, quarter by quarter (the monthly read as quarterly averages); stated as found 2026-10-28 after seeing the run",
      all(dif[nm][0] < 0.5 and dif[nm][1] < 1.0 for nm in ("2008-10", "2000-03")),
      f"largest differences (unemployment, gap): {dif}")
u29, y29 = qrun["1929-33"]["u"], qrun["1929-33"]["y"]
mu29, my29 = mq["1929-33"]["u"][:18], mq["1929-33"]["y"][:18]
check("V8 and run_1929, on the Dow as first stylised (-40% by November 1929, -86% by mid-1932), its own profile of "
      "1930's spending collapse and the run channel on the model's stress (it carries no measured runs, R2): within 1.2 "
      "points of the monthly episode's unemployment and 2.5 of its gap in every quarter to 1933Q4, a little milder "
      "through 1932 (less unemployment in each of its quarters) and level by 1933Q4 (within a tenth of a point). Restated "
      "2026-10-28 after seeing the refit's run (decision 92; these bounds set then): at the first pass (the run "
      "channel's coefficient 0) within 2 points through 1931 and milder from 1932, by 1933Q4 over 4 points less "
      "unemployment and a gap over 7 points smaller (26.71 against 32.13)",
      np.abs(u29 - mu29).max() < 1.2 and np.abs(y29 - my29).max() < 2.5 and bool(np.all(u29[10:14] < mu29[10:14]))
      and abs(u29[17] - mu29[17]) < 0.1,
      f"largest differences {np.abs(u29 - mu29).max():.2f} (unemployment, {pd.Period('1929Q3', 'Q') + int(np.argmax(np.abs(u29 - mu29)))}) "
      f"and {np.abs(y29 - my29).max():.2f} (gap); 1933Q4 {u29[17]:.2f} against {mu29[17]:.2f}, gap {y29[17]:.2f} against {my29[17]:.2f}")
# the 1929-33 quarterly run's demand inputs, recomputed: exports on the calendar (index 0 the end of September 1929), the
# post-crash collapse, and Smoot-Hawley's switch to home goods, which is the only place the tariff reaches demand
o29 = qrun["1929-33"]
comp = ("d_wealth", "d_capex", "d_unemp", "d_relief", "d_debt", "d_credit", "d_money", "d_trade", "d_fiscal", "d_care")
other29 = o29["D"] - sum(o29[c] for c in comp) - o29["d_fin"] - o29["d_rate"]
e_, g_ = gc.fred("EXPGSCA"), gc.fred("GDPCA")
exa = {d.year: float((e_[d] - e_.iloc[0]) / g_.iloc[0] * 100) for d in e_.index if d.year <= 1934}
exp_at = lambda t: np.interp(t, [y + 0.5 for y in sorted(exa)], [exa[y] for y in sorted(exa)])  # noqa: E731
n29 = len(o29["y"])
imp = th["impulse_1930_pct_gdp"]
conf29 = np.array([-imp * max(0.0, 1 - max(k - 2, 0) / 8) if k >= 1 else 0.0 for k in range(n29)])
t_sh = gc.years_after_q("1929Q3", "1930-06-17")
sw29 = (1 - cm.tariff_net) * 15.0 * 0.05 * np.array([gc.after(t_sh, k, gc.Q) if k >= 1 else 0.0 for k in range(n29)])
e29 = ep.e1929(okun, 0.0)
sw_m = (1 - cm.tariff_net) * 15.0 * 0.05 * np.array([gc.after(ep.years_after("1929-09", "1930-06-17"), k, ep.M) if k >= 1 else 0.0 for k in range(e29.months + 1)])
mood_off = all(np.array_equal(qrun[nm]["s"], cm.sigma * qrun[nm]["stress"]) for nm in qrun)
check("V9 the quarterly check runs as the monthly episodes run (decision 91): the US's own trade and exports off and the "
      "shared mood off, so its trade term is zero and its spread sigma x capital lost; Smoot-Hawley counted once, as the "
      "switch from imports to home goods from 17 June 1930 ((1 - tariff_net) x 15 points x exports' 5% of GDP), its export "
      "loss in the measured exports; and those exports on the calendar, at each quarter's end the monthly episode's at "
      "that month's end (before 2026-10-28 read a quarter early, the tariff counted twice and the mood and trade on)",
      all(not qrun[nm]["d_trade"].any() for nm in qrun) and mood_off
      and np.allclose(other29[1:], (exp_at(1929.75 + np.arange(n29) * gc.Q) + conf29 + sw29)[1:], atol=1e-12, rtol=0)
      and np.allclose(e29.shock.demand["US"] - sw_m, exp_at(1929.75 + np.arange(e29.months + 1) * ep.M), atol=1e-12, rtol=0)
      and sw29[2] == 0.0 and 0 < sw29[3] < 0.525 and np.allclose(sw29[4:], 0.525, atol=1e-12, rtol=0),
      f"the switch by quarter from 1930Q1 {np.round(sw29[2:6], 3).tolist()} % of GDP; exports 1930Q4 "
      f"{exp_at(1929.75 + 5 * gc.Q):.2f}, 1932Q4 {exp_at(1929.75 + 13 * gc.Q):.2f} % of 1929 GDP")

print("R — the refit (decision 92): the bank runs measured, debt deflation levelling off")
mcsv = pd.read_csv(os.path.join(ROOT, "cache", "M1444AUSM027SNBR.csv"), index_col=0, parse_dates=True).iloc[:, 0]
mmo = mcsv.groupby(mcsv.index.to_period("M")).mean()
p29 = pd.Period("1929-09", "M")
fall29 = np.array([max(0.0, 1 - float(mmo[p29 + k]) / float(mmo[p29])) for k in range(52)])   # to December 1933
runs29 = fall29 / fall29.max()
eps_ = {e.name: e for e in ep.episodes(theta)}
o29m = eps_["1929-33"].run(cm)
k_tr = int(np.argmax(fall29))
check("R1 the 1930-33 bank runs read the money stock's measured fall, recomputed here from the cached file (Friedman and "
      "Schwartz's money stock, FRED M1444AUSM027SNBR, monthly): its fall from September 1929 over its largest in the "
      "episode is the 1929-33 episode's Shock.runs (episodes.bank_runs); the fitted run's money channel reads it, -money "
      "x the runs a month before, in place of the model's stress, which rose earlier (at December 1930 about twice the "
      "runs'). Stated as found 2026-10-28 after seeing the run: the largest fall 35.8%, in April 1933 (March 1933's own "
      "fall 35.3%), a seventh of it by December 1930 and "
      "over half by December 1931; the channel's coefficient 6.92 (0 at the first pass)",
      np.allclose(eps_["1929-33"].shock.runs["US"], runs29, atol=1e-12, rtol=0)
      and np.allclose(ep.bank_runs("1929-09", 51), runs29, atol=1e-12, rtol=0)
      and round(float(fall29.max()), 3) == 0.358 and str(p29 + k_tr) == "1933-04" and 1 / 8 < runs29[15] < 1 / 6
      and 0.5 < runs29[27] < 0.6 and np.allclose(o29m["d_money"][1:], -cm.money * runs29[:-1], atol=1e-12, rtol=0)
      and o29m["stress"][15] > 1.8 * runs29[15] and round(th["money"], 2) == 6.92,
      f"largest fall {fall29.max():.4f} ({p29 + k_tr}; March 1933 {fall29[42]:.4f}); runs at December 1930 "
      f"{runs29[15]:.3f}, December 1931 {runs29[27]:.3f}; the model's stress then {o29m['stress'][15]:.3f}, "
      f"{o29m['stress'][27]:.3f}; money {th['money']:.3f}")
o30 = gc.simulate(regs, P("the 1930s' rules"), gc.ai_shock(N), cm, N, waves=gc.CENTRAL_WAVES)
q29 = qrun["1929-33"]
carry = [e.name for e in ep.episodes(theta) if e.shock.runs]
check("R2 and only that episode carries them: of the ten episodes only 1929-33's shock has measured runs, the forward "
      "bust none, nor the quarterly check run_1929; elsewhere and forward the run channel reads the model's stress, -money "
      "x the capital lost a step before, so its coefficient means the same thing: in run_1929 and, forward, in every "
      "region under the 1930s' rules (deposits uninsured: up to the full 6.92% of GDP, all capital lost); under today's "
      "rules (insured) it is nothing. Stated as found 2026-10-28 after seeing the run",
      carry == ["1929-33"] and not gc.ai_shock(N).runs
      and np.allclose(q29["d_money"][1:], -cm.money * q29["stress"][:-1], atol=1e-12, rtol=0)
      and all(np.allclose(o30[r]["d_money"][1:], -cm.money * o30[r]["stress"][:-1], atol=1e-12, rtol=0) for r in gc.R)
      and all(not om[r]["d_money"].any() for r in gc.R) and all(o30[r]["d_money"].min() < -6.9 for r in gc.R),
      f"carrying runs: {carry}; the 1930s' rules forward, the channel at most {-min(o30[r]['d_money'].min() for r in gc.R):.2f}% of GDP")
lin = replace(cm, dd_sat=None)
o29l = eps_["1929-33"].run(lin)
oc_s = gc.simulate(regs, P("modern rules"), gc.ai_shock(N), cm, N, waves=gc.CENTRAL_WAVES)
oc_l = gc.simulate(regs, P("modern rules"), gc.ai_shock(N), lin, N, waves=gc.CENTRAL_WAVES)
pd29 = eps_["1929-33"].regions["US"].priv_debt
cases = ([("1929-33", o29m, pd29, cm.dd_sat), ("1929-33, linear", o29l, pd29, None)]
         + [(f"central {r}", oc_s[r], regs[r].priv_debt, cm.dd_sat) for r in gc.R]
         + [(f"central {r}, linear", oc_l[r], regs[r].priv_debt, None) for r in gc.R]
         + [(f"1930s' rules {r}", o30[r], regs[r].priv_debt, cm.dd_sat) for r in gc.R])
res_dd, slope_lo, n_small, over = 0.0, 1.0, 0, 0.0
for lab_, o_, debt_, s_ in cases:
    x = np.maximum(o_["Pexp"][:-1] / o_["P"][:-1] - 1, 0.0)        # the shortfall each step reads, a step before
    form = x if s_ is None else s_ * (1 - np.exp(-x / s_))
    res_dd = max(res_dd, float(np.abs(o_["d_debt"][1:] + cm.debt_deflation * debt_ * form).max()))
    if s_ is not None:
        small = (x > 0) & (x < 1e-3)
        n_small += int(small.sum())
        if small.any():
            slope_lo = min(slope_lo, float((-o_["d_debt"][1:][small] / (cm.debt_deflation * debt_ * x[small])).min()))
        over = max(over, float((-o_["d_debt"]).max() / (cm.debt_deflation * debt_ * s_)))
x29 = float((o29m["Pexp"] / o29m["P"] - 1).max())
cap29 = cm.debt_deflation * pd29 * cm.dd_sat
check("R3 debt deflation levels off (decision 92): in the fitted 1929-33 run, the central run and every region under the "
      "1930s' rules forward, the drag recomputes as debt_deflation x private debt x dd_sat (1 - exp(-shortfall / "
      "dd_sat)), the shortfall the price level's below the path at the target a step before; it has the linear form's "
      "slope at a small shortfall (under 0.1%: within 0.5% of the linear drag, as 1 - shortfall / (2 dd_sat) bounds it) "
      "and never passes debt_deflation x private debt x dd_sat, though 1929-33's shortfall reaches five times dd_sat and "
      "the 1930s' rules' forward over ten times; with dd_sat None (Common's default) it is the linear form, recomputed "
      "the same way, whose own 1929-33 run drags at over six times the cap (60% of GDP against 8.6). The multiples "
      "stated as found 2026-10-28 after seeing the run",
      res_dd < 1e-12 and n_small > 0 and 0.995 < slope_lo <= 1.0 and over <= 1.0 + 1e-12
      and x29 > 5 * cm.dd_sat and all(float((o30[r]["Pexp"] / o30[r]["P"] - 1).max()) > 10 * cm.dd_sat for r in gc.R)
      and float(-o29l["d_debt"].min()) > 6 * cap29 and gc.Common().dd_sat is None,
      f"largest residual {res_dd:.1e}; at {n_small} small shortfalls the drag at least {slope_lo:.4f} of the linear; at "
      f"most {over:.3f} of the cap; 1929-33's shortfall at most {x29:.3f} (dd_sat {cm.dd_sat:.4f}), its drag at most "
      f"{-o29m['d_debt'].min():.2f}% of GDP (cap {cap29:.2f}), linear {-o29l['d_debt'].min():.2f}; the 1930s' rules forward, "
      f"shortfalls at least {min(float((o30[r]['Pexp'] / o30[r]['P'] - 1).max()) for r in gc.R):.2f}")
from scipy.optimize import minimize_scalar  # noqa: E402
s_fit, b_s = th["dd_sat"], fp["bounds"]["dd_sat"]
at_ = lambda **kw: ep.loss([kw.get(k, th[k]) for k in ep.PARAMS])  # noqa: E731
l_lo, l_hi, l_up = at_(dd_sat=0.9 * s_fit), at_(dd_sat=1.1 * s_fit), at_(debt_deflation=0.55)
ridge = minimize_scalar(lambda s: at_(debt_deflation=1.0, dd_sat=s), bounds=tuple(b_s), method="bounded",
                        options={"xatol": 1e-3})
check("R4 the fit's dd_sat and its bound: fitted 0.114 (debt deflation levels off at an 11.4% shortfall), inside its "
      "bounds (0.01 to 1), with the slope at its bound (0.5); the loss rises moving dd_sat a tenth either way (the rest "
      "held). Weakly identified, as decision 92 states: the slope's bound binds (a slope of 0.55 lowers the loss at the "
      "same dd_sat), and at a slope of 1 with dd_sat chosen again the loss is lower still at a dd_sat under 0.05, the "
      "pair sliding toward a fixed drag from a small shortfall; the bounds are a judgement, kept. Stated as found "
      "2026-10-28 after seeing the run (the rest held at the fit, not refitted)",
      b_s == [0.01, 1.0] and b_s[0] < s_fit < b_s[1] and round(s_fit, 3) == 0.114
      and th["debt_deflation"] == fp["bounds"]["debt_deflation"][1] == 0.5 and cm.dd_sat == s_fit
      and l_lo > loss_now and l_hi > loss_now and l_up < loss_now and ridge.fun < l_up and ridge.x < 0.05,
      f"loss {loss_now:.2f}; dd_sat x0.9 {l_lo - loss_now:+.2f}, x1.1 {l_hi - loss_now:+.2f}; slope 0.55 {l_up - loss_now:+.2f}; "
      f"slope 1, dd_sat {ridge.x:.4f}: {ridge.fun - loss_now:+.2f}")
by_ep = lambda c: {e.name: float(np.sum(np.square(e.errors(e.run(c))))) for e in ep.episodes(theta) if e.fitted}  # noqa: E731
l_fit, l_off, l_lin = by_ep(cm), by_ep(replace(cm, debt_deflation=0.0)), by_ep(lin)
up_off = {k: round(l_off[k] - l_fit[k], 1) for k in l_fit}
up_lin = {k: round(l_lin[k] - l_fit[k], 1) for k in l_fit}
check("R5 what the record says of the form, at the fit's other parameters (not refitted): without debt deflation the "
      "record fits worse, 1929-33 most and Japan 1991-95 next, 2008-10 and Sweden 1990-93 too (debt deflation at small "
      "shortfalls); the linear form fits worse still, all of it in 1929-33 (its large shortfall), every other episode's "
      "loss within 1.5 of the fit's or lower. Stated as found 2026-10-28 after seeing the run (decision 92's "
      "alternatives speak of refits; these are not)",
      sorted(up_off, key=lambda k: -up_off[k])[:2] == ["1929-33", "Japan 1991-95"]
      and all(up_off[k] > 5 for k in ("2008-10", "Sweden 1990-93")) and sum(l_lin.values()) > sum(l_off.values()) > sum(l_fit.values())
      and up_lin["1929-33"] > 100 and all(v < 1.5 for k, v in up_lin.items() if k != "1929-33")
      and abs(sum(l_fit.values()) - fp["loss"]) < 0.01,
      f"loss {sum(l_fit.values()):.1f}; without debt deflation {sum(l_off.values()):.1f} {up_off}; linear "
      f"{sum(l_lin.values()):.1f} {up_lin}")

print("B — the 2000-02 bust, measured")
qd = lambda sid, end=False: (lambda x: x.groupby(x.index.to_period("Q")).last() if end else x.groupby(x.index.to_period("Q")).mean())(gc.fred(sid))  # noqa: E731
qs = [pd.Period("2000Q1", "Q") + k for k in range(24)]
z = qd("BOGZ1LM153064475Q", True)
eqm = np.array([max(0.0, 1 - z[q] / z[qs[0]]) for q in qs])
g = qd("GDP")
net = (qd("Y034RC1Q027SBEA") + qd("B985RC1Q027SBEA") + qd("W003RC1Q027SBEA") - qd("B852RC1Q027SBEA")) / g * 100
yr_ = net.dropna().groupby(net.dropna().index.year).mean().loc[1990:1994]
sl, ic = np.polyfit(yr_.index.values.astype(float), yr_.values, 1)
gp_ = np.array([net[q] - (sl * (q.year + (q.quarter - 1) / 4 + 0.125) + ic) for q in qs])
ci = qd("CORBLACBS")
base = ci[(ci.index >= pd.Period("1997Q1", "Q")) & (ci.index <= pd.Period("1999Q4", "Q"))].mean()
ex = np.array([max(0.0, ci[q] - base) for q in qs])
b2 = gc.bust_2000()
hist = json.load(open(os.path.join(ROOT, "cache", "HISTORY_SOURCES.json"), encoding="utf-8"))
import hashlib  # noqa: E402
hashes = all(hashlib.sha256(open(os.path.join(ROOT, "cache", f"{sid}.csv"), encoding="utf-8").read().encode()).hexdigest() == v["sha256"]
             for sid, v in hist.items())
check("B1 the 2000-02 bust's three legs, recomputed here from the cached files (Z.1 household equity; BEA's information "
      "processing equipment, software and power structures less computer imports, over GDP, against their 1990-94 trend; "
      "the Fed Board's C&I charge-offs over their 1997-99 mean), equal bust_2000's; the history files written from the "
      "publishers carry the hashes their record names (cache/HISTORY_SOURCES.json); household equity -44.7% at the trough "
      "ten quarters after the peak, the build-out's excess 76% lost at most, the losses peaking ten quarters after",
      np.allclose(eqm, b2["measured"]["equity_fall"], atol=1e-12) and np.allclose(1 - gp_ / gp_[0], b2["measured"]["capex_share_lost"], atol=1e-12)
      and np.allclose(ex / ex.sum(), b2["losses"], atol=1e-12) and hashes
      and round(eqm.max(), 3) == 0.447 and int(np.argmax(eqm)) == 10 and round((1 - gp_ / gp_[0]).max(), 3) == 0.762
      and int(np.argmax(ex)) == 10,
      f"equity trough {eqm.max():.3f} at k={int(np.argmax(eqm))}; build-out lost at most {(1 - gp_ / gp_[0]).max():.3f}; losses peak k={int(np.argmax(ex))}")

print("S — the measured shocks enter with the sign of their own change (a fall is a drag)")
d07 = gc.demand_2007()
res = gc.fred("PRFI") / gc.fred("GDP").reindex(gc.fred("PRFI").index) * 100
dres = res.loc["2007-10-01":].values[:13] - float(res.loc["2007-10-01"])
xq = gc.fred("EXPGSC1")
dex = ((xq - xq.loc["2007-10-01"]) / gc.fred("GDPC1").loc["2007-10-01"] * 100).loc["2007-10-01":].values[:13]
check("S1 2008-10: housebuilding enters as residential investment's change in share of GDP (it fell, so a drag every quarter), exports "
      "as their own change, housing wealth as a fall; each with the sign of the measured change, quarter by quarter",
      np.array_equal(np.sign(d07["housebuilding"]), np.sign(dres)) and (d07["housebuilding"][1:] < 0).all()
      and np.array_equal(np.sign(d07["exports"]), np.sign(dex)) and (d07["housing wealth"] <= 0).all(),
      {k: [round(float(x), 2) for x in v[[1, 4, 8, 12]]] for k, v in d07.items()})
full, nob, noh = (gc.run_2007(cm, okun, drop=dr) for dr in ((), ("housebuilding",), ("housing wealth",)))
mfull, mnob, mnoh = (ep.e2007(okun, drop=dr).run(cm) for dr in ((), ("housebuilding",), ("housing wealth",)))
check("S2 and in the runs: leaving out the housebuilding collapse or the fall in housing wealth makes 2008-10 milder (a higher "
      "trough), in the fitted monthly episode and in its quarterly check",
      nob["y"].min() > full["y"].min() and noh["y"].min() > full["y"].min()
      and mnob["y"].min() > mfull["y"].min() and mnoh["y"].min() > mfull["y"].min(),
      f"monthly: trough {mfull['y'].min():.2f}; without housebuilding {mnob['y'].min():.2f}; without housing wealth "
      f"{mnoh['y'].min():.2f}. Quarterly: {full['y'].min():.2f}, {nob['y'].min():.2f}, {noh['y'].min():.2f}")

print("M — the mechanics, at the monthly step")
n = gc.months(16)
calm = {r: replace(g, eta=0.0, drift=0.0, pi0=2.0, i0=(cm.r_star if g.r_star is None else g.r_star) + 2.0, i_norm=None,
                   sov0=g.sov_calm) for r, g in regs.items()}
o = gc.simulate(calm, {r: gc.MODERN for r in gc.R}, gc.Shock(), cm, n)
check("M1 no shock, no drift, policy at each region's neutral rate and inflation on target: every region stays at capacity",
      all(np.abs(o[r]["y"]).max() < 1e-9 and np.ptp(o[r]["u"]) < 1e-9 and np.abs(o[r]["pi"] - 2.0).max() < 1e-9 for r in gc.R))
us_only = gc.Shock(demand={"US": gc.ramp(-5.0, 1, 6, n)})
o = gc.simulate(calm, {r: gc.MODERN for r in gc.R}, us_only, cm, n)
check("M2 trade carries a US slump abroad: every other region's gap falls, Sweden's (exports half of GDP) the most",
      all(o[r]["y"].min() < -0.05 for r in ("EA", "FR", "SE", "CN"))
      and o["SE"]["y"].min() < min(o["EA"]["y"].min(), o["FR"]["y"].min(), o["CN"]["y"].min()),
      {r: round(float(o[r]["y"].min()), 2) for r in gc.R})
o = gc.simulate(regs, P("modern rules"), gc.ai_shock(N), cm, N)
outside = {r: (regs[r].sov_pass * (o[r]["sov"] - regs[r].sov_calm) if regs[r].sov_debt > 0 else o[r]["premium"]) for r in gc.R}
check("M3 under the backstop, the banks' part of spreads stays under each region's cap (the price of debt and France's "
      "sovereign spread are added outside it), and capital above the recapitalisation floor",
      all((o[r]["s"] - outside[r]).max() <= regs[r].spread_cap + 1e-9
          and o[r]["k"].min() >= gc.MODERN.capital_floor * regs[r].bank_capital - 1e-9 for r in gc.R))
flat = {r: replace(g, groups=g.groups, premium={q: 1.0 for q in gc.GROUPS}, benefit_cap=99.0) for r, g in regs.items()}
now = gc.Waves(split=True, robot_lag=0.0, robot_ramp=0.0)
worst = {r: replace(g, eta=3 * g.eta) for r, g in flat.items()}
diffs = []
for nm in ("modern rules", "rules expand under pressure", "rules erode under pressure"):
    a = gc.simulate(worst, P(nm), gc.ai_shock(N), cm, N)
    b = gc.simulate(worst, P(nm), gc.ai_shock(N), cm, N, waves=now)
    diffs.append(max(float(np.abs(a[r][k] - b[r][k]).max()) for r in gc.R for k in ("y", "u", "u_star", "k", "deficit_extra")))
check("M4 the split nests the uniform case: every group paid the average, support uncapped and robotics from the start reproduce "
      "the uniform runs exactly (today's, expanding and eroding rules, each on its dates)", max(diffs) < 1e-9, f"largest difference {max(diffs):.1e}")
lag3 = gc.Waves(split=True, robot_lag=3.0)
o = gc.simulate({r: replace(g, eta=3 * g.eta) for r, g in regs.items()}, P("modern rules"), gc.ai_shock(N), cm, N, waves=lag3)
before = round(3.0 / gc.DT)
check("M5 before robotics arrives (three years out: September 2029), nobody in physical work is displaced; after it, they are",
      all(o[r]["s_phys"][:before + 1].max() == 0 and o[r]["s_phys"][-1] > 0 for r in gc.R),
      {r: (float(o[r]["s_phys"][before]), round(float(o[r]["s_phys"][-1]), 2)) for r in gc.R})
w = {r: gc.wave_weights(regs[r], gc.MODERN, cm, lag3) for r in gc.R}
check("M6 a recession's usual mix of job losers weighs what the fit assumed (lost net pay per point = 1 - replacement); a "
      "displaced cognitive worker weighs more",
      all(abs(sum(w[r]["mix"][q] * w[r]["spend"][q] for q in gc.GROUPS) - (1 - regs[r].replacement)) < 1e-9
          and w[r]["spend"]["cognitive"] > 1 - regs[r].replacement for r in gc.R),
      {r: {q: round(w[r]["spend"][q] / (1 - regs[r].replacement), 2) for q in gc.GROUPS} for r in gc.R})
row_ = "modern rules | bust only"
ob = gc.simulate(bonly, P("modern rules"), gc.ai_shock(N), cm, N)
fresh = {"year4": gc.summary(ob, regs, 16), "year6": gc.summary(ob, regs)}
row2 = "rules expand into care | bust + displacement, recessions trigger adoption x3 | two waves, robotics in 2 years, care absorbs"
rg3x = {r: replace(g, eta=3 * g.eta) for r, g in regs.items()}
oc2 = gc.simulate(rg3x, P("rules expand into care"), gc.ai_shock(N), cm, N, waves=gc.Waves(split=True, robot_lag=2.0, absorb=True))
fresh2 = {"year4": gc.summary(oc2, regs, 16), "year6": gc.summary(oc2, regs)}
check("M7 the stored scenarios are the model's: a run made here at the monthly step, on the stored presets' dates, gives the "
      "stored rows exactly (the bust alone under today's rules; the care build-out in the labour-depression row)",
      json.loads(json.dumps(fresh)) == S[row_] and json.loads(json.dumps(fresh2)) == S[row2],
      f"US year-4 gap {fresh['year4']['US']['gap_min']} (stored {S[row_]['year4']['US']['gap_min']})")

print("F — the findings (year 4, stated as found; 'non-employment' is unemployment plus those who left the labour force)")
NW = lambda x, r="US": x[r]["not_working_rise_max"]  # noqa: E731
y4 = lambda k: S[k]["year4"]  # noqa: E731
bo = y4("modern rules | bust only")
check("F1 today's rules, the bust alone (dot-com size): a world recession, smaller than 2008's — the four together 2-4% below "
      "capacity, the US 2% or more, about the model's own dot-com bust (-2.78, V4; -2.73 at the first pass). Restated "
      "2026-10-28 after seeing the run (decision 91): before it the US 3% or more (-3.18; the four -2.08)",
      -4.0 < bo["four_weighted_gap_min"] <= -2.0 and bo["US"]["gap_min"] <= -2.0, f"four together {bo['four_weighted_gap_min']}%; US {bo['US']['gap_min']}%")
lab = y4("modern rules | bust + displacement, recessions trigger adoption x3")
check("F2 today's rules with displacement and recessions triggering adoption: a jobs crisis larger than the output one — US "
      "non-employment up 10 points or more while output stays within 10% of capacity; measured unemployment shows under half of "
      "it. Restated 2026-10-28 after seeing the run (the words, not the bounds): the gap now about 2008-10's, so 'without an "
      "output one' went; before it +10.48 with the gap at -4.82%",
      NW(lab) >= 10 and lab["US"]["gap_min"] > -10 and lab["US"]["unemployment_max"] - regs["US"].u0 < NW(lab) / 2,
      f"US non-employment +{NW(lab)} (unemployment {lab['US']['unemployment_max']}%, {lab['US']['out_of_labour_force_end']} points out of the labour force), gap {lab['US']['gap_min']}%")
er = y4("rules erode under pressure | bust + displacement")
check("F3 when the rules erode (austerity, no backstop, tariffs, looser anchoring): a world depression, over twice 2008's "
      "(2008-10's US trough was 6.3%) — the four together 15% or more below capacity, US non-employment up 15 points or "
      "more, most of US banks' capital gone. Restated 2026-10-28 after seeing the run (decision 91; the debt-deflation drag, "
      "D11): before it about twice 2008's, the four 8% or more below and non-employment 12 points or more (-9.38%, +14.43, 0.728)",
      er["four_weighted_gap_min"] <= -15.0 and NW(er) >= 15 and er["US"]["bank_capital_lost_max"] >= 0.6,
      f"four together {er['four_weighted_gap_min']}%, US non-employment +{NW(er)}, capital lost {er['US']['bank_capital_lost_max']}")
ex = y4("rules expand under pressure | bust + displacement")
ex6, md6 = S["rules expand under pressure | bust + displacement"]["year6"], S["modern rules | bust + displacement"]["year6"]
md = y4("modern rules | bust + displacement")
check("F4 when the rules expand (an income guarantee, from its dates): the guarantee holds demand, not jobs — by year 6, "
      "after today's stimulus has run out, every region's output is closer to capacity than under today's rules, at no "
      "more than 3% of US GDP a year by year 4 (under 4% by year 6), but US non-employment is still up more than 7 points "
      "by year 4; at year 4, with today's stimulus still running, output no better than under today's rules (within a "
      "point outside Sweden, two in Sweden) and within 10% of capacity. Restated 2026-10-28 after seeing the run "
      "(decision 91: policy dated; the debt-deflation drag, D11): before it output held within 5% everywhere by year 4 "
      "(2.55% of GDP, +8.0)",
      all(ex6[r]["gap_min"] > md6[r]["gap_min"] for r in gc.R) and all(abs(ex[r]["gap_min"] - md[r]["gap_min"]) < 1.0 for r in gc.R if r != "SE")
      and abs(ex["SE"]["gap_min"] - md["SE"]["gap_min"]) < 2.0 and all(ex[r]["gap_min"] > -10 for r in gc.R)
      and ex["US"]["guarantee_cost_max_pct_gdp"] <= 3 and ex6["US"]["guarantee_cost_max_pct_gdp"] < 4 and NW(ex) > 7,
      f"year-4 gaps {[ex[r]['gap_min'] for r in gc.R]} against today's rules' {[md[r]['gap_min'] for r in gc.R]}; year 6 "
      f"{[ex6[r]['gap_min'] for r in gc.R]} against {[md6[r]['gap_min'] for r in gc.R]}; US guarantee at most "
      f"{ex['US']['guarantee_cost_max_pct_gdp']}% of GDP by year 4, {ex6['US']['guarantee_cost_max_pct_gdp']}% by year 6; "
      f"US non-employment +{NW(ex)}")
th3 = y4("the 1930s' rules | bust + displacement")
check("F5 the 1930s' rules on today's economy are worse still than eroded rules", th3["four_weighted_gap_min"] < er["four_weighted_gap_min"],
      f"{th3['four_weighted_gap_min']} against {er['four_weighted_gap_min']}")
check("F6 the US and Sweden lead: the two largest rises in non-employment of the four under today's rules, within half a "
      "point of each other (the US's mostly exits from the labour force, Sweden's all unemployment). Restated 2026-10-28 "
      "after seeing the run (decision 91; Sweden's debt deflation, D11, and its fitted Okun slope): before it the US alone "
      "led (+7.32, the others +2.3 to +3.2)",
      sorted(gc.R, key=lambda r: -NW(md, r))[:2] in (["US", "SE"], ["SE", "US"]) and abs(NW(md) - NW(md, "SE")) < 0.5
      and md["US"]["out_of_labour_force_end"] > NW(md) / 2 and md["SE"]["out_of_labour_force_end"] == 0,
      {r: (NW(md, r), md[r]["out_of_labour_force_end"]) for r in gc.R})

print("X — the participation margin and the measured build-out (decoupling.py), stated as found")
dec = json.load(open(os.path.join(ROOT, "results", "decoupling.json"), encoding="utf-8"))
check("X1 the inputs are the measured ones: the US build-out net of computer imports above its 2015-22 trend (floored at zero: "
      "it sits below its trend, -0.42 points, since decoupling.py reads information processing equipment, not all "
      "equipment; Log 42), and the US exit share since the prime-age employment peak; the other regions keep the "
      "displaced in the labour force (not measured)",
      abs(regs["US"].ai_capex - max(dec["ai_build_out"]["net_above_2015_22_trend_pts"], 0.0)) < 1e-9
      and abs(regs["US"].exit_share - dec["where_the_displaced_go"]["prime_age_25_54"]["since_the_employment_peak"]["exit_share"]) < 1e-9
      and all(regs[r].exit_share == 0 for r in ("EA", "FR", "SE", "CN")),
      f"US build-out {regs['US'].ai_capex}% of GDP (measured {dec['ai_build_out']['net_above_2015_22_trend_pts']}; assumed 1.5 before), "
      f"exit share {regs['US'].exit_share}")
old_us = {r: (replace(g, ai_capex=1.5, drift=0.0) if r == "US" else replace(g, drift=0.0)) for r, g in regs.items()}
new_us = {r: replace(g, drift=0.0) for r, g in regs.items()}
a = gc.summary(gc.simulate(old_us, P("modern rules"), gc.ai_shock(N), cm, N), regs, 16)
b = gc.summary(gc.simulate(new_us, P("modern rules"), gc.ai_shock(N), cm, N), regs, 16)
nof = {r: replace(gc.MODERN, fiscal="none") for r in gc.R}
a0 = gc.summary(gc.simulate(old_us, nof, gc.ai_shock(N), cm, N), regs, 16)
b0_ = gc.summary(gc.simulate(new_us, nof, gc.ai_shock(N), cm, N), regs, 16)
check("X2 measured, the US build-out has nothing above its trend, so the bust's capex leg is zero in the US. Had it been "
      "the 1.5% of GDP assumed before, the bust would cut deeper: by over a point at year 4, with today's stimulus on its "
      "dates and without discretionary fiscal policy alike (policy dated, not triggered: the deeper bust no longer fires "
      "the stimulus earlier). Restated 2026-10-28 after seeing the run (decision 91): before it the triggered run was "
      "asked only to cut deeper, by less than the one with no fiscal response, for that reason",
      regs["US"].ai_capex == 0.0 and a0["US"]["gap_min"] <= b0_["US"]["gap_min"] - 1.0 and a["US"]["gap_min"] <= b["US"]["gap_min"] - 1.0,
      f"US gap, no fiscal response: {a0['US']['gap_min']} assumed -> {b0_['US']['gap_min']} measured; with the dated stimulus "
      f"{a['US']['gap_min']} -> {b['US']['gap_min']}")
dep6 = S["modern rules | bust + displacement, recessions trigger adoption x3 | two waves, robotics in 2 years"]["year6"]["US"]
check("X3 exits hide a jobs depression from the unemployment rate: by year 6 (robotics two years out) US unemployment reads under "
      "15% while more points have left the labour force than unemployment has risen. Restated after the sign fix of 2026-10-26: "
      "before it, under 20% with more than 20 points out (19.71%, 22.96)",
      dep6["unemployment_max"] < 15 and dep6["out_of_labour_force_end"] > dep6["unemployment_max"] - regs["US"].u0,
      f"unemployment {dep6['unemployment_max']}%, out of the labour force {dep6['out_of_labour_force_end']}, non-employment +{dep6['not_working_rise_max']}")
nb = lambda rn, hz: S[f"{rn} | displacement without a bust"][hz]["US"]  # noqa: E731
check("X4 displacement without a bust (where the US is), the presets' levers on the dates their central run set (decision "
      "81: governments act on the dates whatever the shock): by year 4 US output within 1.5% of capacity under today's "
      "rules and the guarantee alike; by year 6 today's stimulus has run out and output is over 4% below capacity, the "
      "guarantee's under 3%; non-employment up 8-9.5 points by year 6 either way. Stated as found 2026-10-28 after seeing "
      "the run; it replaces the comparison of triggers keyed to unemployment and to non-employment, retired with the "
      "triggers (decision 91), as is the old X5 (in a bust the triggers fired either way)",
      all(nb(k, "year4")["gap_min"] > -1.5 for k in ("modern rules", "rules expand under pressure"))
      and nb("modern rules", "year6")["gap_min"] < -4 < -3 < nb("rules expand under pressure", "year6")["gap_min"]
      and all(8 <= nb(k, "year6")["not_working_rise_max"] <= 9.5 for k in ("modern rules", "rules expand under pressure")),
      {k: {"gap": (nb(k, "year4")["gap_min"], nb(k, "year6")["gap_min"]), "non-employment": (nb(k, "year4")["not_working_rise_max"],
           nb(k, "year6")["not_working_rise_max"])} for k in ("modern rules", "rules expand under pressure")})

print("W — two waves (cognitive now, physical once robotics arrives), stated as found")
row = "modern rules | bust + displacement, recessions trigger adoption x3"
wv = lambda L, hz="year4": S[f"{row} | two waves, robotics in {L} years"][hz]  # noqa: E731
u4 = [NW(lab)] + [NW(wv(L)) for L in (1, 2, 3)]
check("W1 the robotics lag holds the jobs crisis back: US year-4 non-employment falls with every year of lag, and with robotics "
      "three years out it is at least 2.5 points below the uniform case. Restated 2026-10-26 after the bust moved to the 2000-02 bust's measured path and the start to the dated vintage (Log 42): before it at least 3.5 (13.2 -> "
      "9.26); before the sign fix at least 5 (21.03 -> 14.71)",
      all(a_ >= b_ for a_, b_ in zip(u4, u4[1:])) and u4[0] - u4[3] >= 2.5, f"uniform, 1, 2, 3 years: {u4}")
d2 = S["modern rules | bust + displacement | two waves, robotics in 2 years"]["year6"]
check("W2 it delays, it does not prevent: with robotics two years out, US non-employment by year 6 is above the uniform case's at "
      "year 4, in this row and with displacement alone",
      NW(wv(2, "year6")) > NW(lab) and NW(d2) > NW(md), f"{NW(wv(2, 'year6'))} against {NW(lab)}; displacement alone {NW(d2)} against {NW(md)}")
per = lambda x: x["US"]["gap_min"] / NW(x)  # noqa: E731
check("W3 the first wave costs more per job: with robotics three years out, US output falls further per point of non-employment "
      "than in the uniform case (the displaced earn 1.2 times the average, with support capped)",
      per(wv(3)) < per(lab), f"{per(wv(3)):.3f} against {per(lab):.3f} points of output per point of non-employment")
cn = [NW(lab, "CN"), NW(wv(3), "CN")]
check("W4 China waits for robotics: with robotics three years out, its year-4 non-employment rise is at least 1 point below the uniform "
      "case and its displaced are mostly in physical work once robotics arrives",
      cn[0] - cn[1] >= 1 and wv(3, "year6")["CN"]["displaced_physical_end"] > wv(3, "year6")["CN"]["displaced_cognitive_end"],
      f"{cn}; year 6 displaced cognitive {wv(3, 'year6')['CN']['displaced_cognitive_end']}, physical {wv(3, 'year6')['CN']['displaced_physical_end']}")
nofisc = {r: replace(gc.MODERN, fiscal="none") for r in gc.R}
rg3 = {r: replace(g, eta=3 * g.eta) for r, g in regs.items()}
a = gc.summary(gc.simulate(rg3, nofisc, gc.ai_shock(N), cm, N), regs, 16)
b = gc.summary(gc.simulate(rg3, nofisc, gc.ai_shock(N), cm, N, waves=lag3), regs, 16)
check("W5 and with no discretionary fiscal response at all: the lag still cuts US non-employment, the first wave still costs "
      "more output per point of it, and China's output is better with the lag, not worse",
      NW(b) < NW(a) and per(b) < per(a) and b["CN"]["gap_min"] > a["CN"]["gap_min"],
      f"US non-employment +{NW(a)} -> +{NW(b)}; per point {per(a):.3f} -> {per(b):.3f}; China gap {a['CN']['gap_min']} -> {b['CN']['gap_min']}")

print("C — care as the absorber (robotics two years out), stated as found")
ab_ = gc.Waves(split=True, robot_lag=2.0, absorb=True)
nab = gc.Waves(split=True, robot_lag=2.0)
diffs = []
for rl in (P("rules erode under pressure"), P("modern rules", replace(gc.MODERN, care="cut"))):
    a = gc.simulate(rg3, rl, gc.ai_shock(N), cm, N, waves=nab)
    b = gc.simulate(rg3, rl, gc.ai_shock(N), cm, N, waves=ab_)
    diffs.append(max(float(np.abs(a[r][k] - b[r][k]).max()) for r in gc.R for k in ("y", "u", "u_star", "k", "out")))
check("C1 the absorber nests the split: when the rules hire none of the displaced into care, the runs are the split's exactly",
      max(diffs) < 1e-9, f"largest difference {max(diffs):.1e}")
runs_c = {lab_: gc.simulate(rg3, rl, gc.ai_shock(N), c, N, waves=ab_) for lab_, rl, c in
          (("build", P("rules expand into care"), cm), ("fast", P("rules expand into care", replace(gc.CARE, care_pace=3.0)), cm),
           ("fast, no ceiling", P("rules expand into care", replace(gc.CARE, care_pace=3.0)), replace(cm, care_ceiling=100.0)),
           ("trend", P("modern rules"), cm))}
check("C2 care never passes the ceiling (Norway's 20.1% of employment), trend and build-out together",
      all(runs_c[k][r]["care"].max() <= cm.care_ceiling + 1e-9 for k in ("build", "fast", "trend") for r in gc.R),
      {r: round(float(runs_c["fast"][r]["care"].max()), 2) for r in gc.R})
o = runs_c["build"]
phys_pool = {r: float((o[r]["s_phys"][-1] + o[r]["at_phys"][-1] + o[r]["ax_phys"][-1])
                      / (o[r]["s_cog"][-1] + o[r]["s_phys"][-1] + o[r]["at_cog"][-1] + o[r]["at_phys"][-1] + o[r]["ax_cog"][-1] + o[r]["ax_phys"][-1])) for r in gc.R}
phys_abs = {r: float((o[r]["at_phys"][-1] + o[r]["ax_phys"][-1]) / (o[r]["at_cog"][-1] + o[r]["at_phys"][-1] + o[r]["ax_cog"][-1] + o[r]["ax_phys"][-1])) for r in gc.R}
check("C3 the gate: the physical wave, mostly men, is under-represented among those care takes in",
      all(phys_abs[r] < phys_pool[r] for r in gc.R), {r: (round(phys_abs[r], 2), round(phys_pool[r], 2)) for r in gc.R})
y6 = lambda rn, dial, wl: S[f"{rn} | {dial} | two waves, robotics in 2 years{wl}"]["year6"]  # noqa: E731
row3 = "bust + displacement, recessions trigger adoption x3"
row1 = "bust + displacement"
none_, trend_, build_ = y6("modern rules", row3, ""), y6("modern rules", row3, ", care absorbs"), y6("rules expand into care", row3, ", care absorbs")
check("C4 care's trend jobs exist anyway: taking them lowers US non-employment a little but does not raise output (the displaced "
      "take them from people who would have entered work)",
      NW(trend_) < NW(none_) and trend_["US"]["gap_min"] <= none_["US"]["gap_min"],
      f"non-employment +{NW(none_)} -> +{NW(trend_)}; gap {none_['US']['gap_min']} -> {trend_['US']['gap_min']}")
check("C5 a funded build-out, a point of employment a year from its dates: in the labour-depression row, US year-6 "
      "non-employment at least 4 points lower, at about a point of GDP a year (no more than 1.1%); US care within half a "
      "point of the ceiling by year 6, short of it. Restated 2026-10-28 after seeing the run (decision 91): before it at no "
      "more than 1% of GDP with care over half a point short of the ceiling (+17.9 -> +12.63, 0.9%, 19.31%)",
      NW(none_) - NW(build_) >= 4 and build_["US"]["care_cost_max_pct_gdp"] <= 1.1
      and cm.care_ceiling - 0.5 < build_["US"]["care_share_end"] < cm.care_ceiling,
      f"+{NW(none_)} -> +{NW(build_)}; cost {build_['US']['care_cost_max_pct_gdp']}% of GDP; care {build_['US']['care_share_end']}%")
fast_, open_ = y6("rules expand into care", row3, ", care absorbs, three points a year"), y6("rules expand into care", row3, ", care absorbs, three points a year, no ceiling")
check("C6 in the US the ceiling binds before the pace: three points a year reaches the ceiling and gains under a point by "
      "year 6; without the ceiling it gains over two points more. Restated 2026-10-28 after seeing the run (decision 91): "
      "before it both bound, three points a year gaining over a point (a point a year +12.63, three +11.31, three without "
      "the ceiling +9.05)",
      0 < NW(build_) - NW(fast_) < 1 and abs(fast_["US"]["care_share_end"] - cm.care_ceiling) < 1e-6 and NW(fast_) - NW(open_) > 2,
      f"a point a year +{NW(build_)}, three +{NW(fast_)} (care {fast_['US']['care_share_end']}%), three without the ceiling "
      f"+{NW(open_)} (care {open_['US']['care_share_end']}%)")
struct = build_["US"]["displaced_cognitive_end"] + build_["US"]["displaced_physical_end"]
room = cm.care_ceiling - regs["US"].care_share
check("C7 care cannot rescue the jobs crisis: the US displaced still out of work at year 6 exceed the room care had (Norway's "
      "share less today's), and US non-employment stays up more than 8 points even without a ceiling. Restated 2026-10-26 after the bust moved to the 2000-02 bust's measured path and the start to the dated vintage (Log 42): "
      "before it about twice the room and more than 12 points (10.4 against 5.3; +13.65)",
      struct >= room and NW(open_) > 8, f"still displaced {struct:.1f} points against room {room:.1f}; without a ceiling +{NW(open_)}")
se1, se0 = y6("rules expand into care", row1, ", care absorbs")["SE"], y6("modern rules", row1, "")["SE"]
check("C8 Sweden, displacement alone: the build-out takes year-6 unemployment down at least 2 points and care stays under the "
      "ceiling — there the gate and the pace of training bind, not the ceiling. Restated 2026-10-26 after the bust moved to the 2000-02 bust's measured path and the start to the dated vintage (Log 42): before it at least 2.5",
      se0["unemployment_max"] - se1["unemployment_max"] >= 2.0 and se1["care_share_end"] < cm.care_ceiling - 1,
      f"{se0['unemployment_max']} -> {se1['unemployment_max']}; care {se1['care_share_end']}%")
g_ = y6("rules expand under pressure", row3, "")
per_c = (NW(none_) - NW(build_)) / build_["US"]["care_cost_max_pct_gdp"]
per_g = (NW(none_) - NW(g_)) / g_["US"]["guarantee_cost_max_pct_gdp"]
check("C9 care buys jobs, the guarantee buys demand: per point of GDP a year, the build-out takes more off US non-employment than "
      "the income guarantee, and the guarantee holds output closer to capacity. Restated 2026-10-26 after the bust moved to the 2000-02 bust's measured path and the start to the dated vintage (Log 42): before it over 4 points "
      "closer (-9.1 against -4.44)",
      per_c > per_g and g_["US"]["gap_min"] > build_["US"]["gap_min"],
      f"points of non-employment per % of GDP: care {per_c:.1f}, guarantee {per_g:.1f}; gap: care {build_['US']['gap_min']}, guarantee {g_['US']['gap_min']}")
er_ = y6("rules erode under pressure", row3, ", care absorbs")
check("C10 when the rules erode, care takes in nobody and stops growing",
      all(er_[r]["absorbed_into_existing_care_jobs_end"] + er_[r]["absorbed_into_new_care_jobs_end"] == 0
          and abs(er_[r]["care_share_end"] - regs[r].care_share) < 1e-6 for r in gc.R), {r: er_[r]["care_share_end"] for r in gc.R})
sens = {}
for hh in (0.10, 0.50):
    o = gc.summary(gc.simulate(rg3, P("rules expand into care"), gc.ai_shock(N), replace(cm, care_hire=hh), N, waves=ab_), regs)
    sens[hh] = (NW(o), o["US"]["care_share_end"], o["SE"]["unemployment_max"])
check("C11 how fast care trains and hires (0.10 or 0.50 of the willing a quarter, against 0.25): US non-employment stays up more than "
      "10 points with the build-out either way; Sweden's result moves with it (there it binds). Restated 2026-10-26 after the bust moved to the 2000-02 bust's measured path and the start to the dated vintage (Log 42): before it "
      "more than 15 (19.84, 17.65)",
      all(v[0] > 10 for v in sens.values()) and abs(sens[0.10][2] - sens[0.50][2]) > 1, sens)

print("K — the financing limit (what pays for the build-out), stated as found")
fin = json.load(open(os.path.join(ROOT, "results", "financing.json"), encoding="utf-8"))
check("K1 the inputs are the measured ones: taxes on labour and the highest take (Austria), and the price of debt with and without "
      "a central bank of one's own",
      abs(cm.tax_max - fin["labour_taxes"]["oecd_highest"]["labour_taxes_pct_gdp"]) < 1e-9
      and all(abs(regs[r].labour_tax - fin["labour_taxes"]["regions"][r]["labour_taxes_pct_gdp"]) < 1e-9 for r in gc.R)
      and regs["EA"].debt_slope_crisis > regs["EA"].debt_slope > 10 > 1 > regs["US"].debt_slope,
      {r: (regs[r].labour_tax, regs[r].debt_slope, regs[r].debt_slope_crisis) for r in gc.R})
flat_price = {r: replace(g, eta=3 * g.eta, debt_slope=0.0, debt_slope_crisis=0.0) for r, g in regs.items()}
nc = replace(cm, care_ceiling=100.0)
dc = DATES["rules expand into care"]
a = gc.simulate(flat_price, gc.dated(gc.CARE, dc), gc.ai_shock(N), nc, N, waves=ab_)
b = gc.simulate(flat_price, gc.dated(gc.CARE_LEVY, dc), gc.ai_shock(N), replace(nc, ai_levy=1e6), N, waves=ab_)
d = max(float(np.abs(a[r][k] - b[r][k]).max()) for r in gc.R for k in ("y", "u", "care", "out"))
check("K2 the source changes only the limit, the drag and the price: with debt free and the levy unlimited, borrowing and the levy "
      "give the same paths (on the same dates)", d < 1e-9, f"largest difference {d:.1e}")
fl = lambda rn, dial, fast=True: S[f"{rn} | {dial} | two waves, robotics in 2 years, care absorbs, financing limit" + (", three points a year" if fast else "")]["year6"]  # noqa: E731
tx, lv, bo = fl("care financed by labour taxes", row3), fl("care financed by a levy on AI income", row3), fl("care financed by borrowing", row3)
check("K3 taxes on labour lose room as displacement shrinks the wage base: the US room falls by over a quarter by year 6; "
      "Sweden's, already near the top, runs out (below zero by year 6), and its build-out ends over 3 points of employment "
      "short of the levy's. Restated 2026-10-28 after seeing the run (decision 91): before it Sweden's room fell by over "
      "two-fifths (2.36 -> 1.12) and its build-out ended level with the levy's (18.05% against 18.03%)",
      tx["US"]["financing_room_end_pct_gdp"] < tx["US"]["financing_room_start_pct_gdp"] * 0.75
      and tx["SE"]["financing_room_end_pct_gdp"] < 0 < tx["SE"]["financing_room_start_pct_gdp"]
      and lv["SE"]["care_share_end"] - tx["SE"]["care_share_end"] > 3,
      f"US room {tx['US']['financing_room_start_pct_gdp']} -> {tx['US']['financing_room_end_pct_gdp']}; Sweden {tx['SE']['financing_room_start_pct_gdp']} -> "
      f"{tx['SE']['financing_room_end_pct_gdp']}; Swedish care {tx['SE']['care_share_end']}% against {lv['SE']['care_share_end']}% with the levy")
check("K4 a levy on AI income gains room as displacement grows, and in the US, the euro area and Sweden it never binds: the same "
      "jobs as borrowing, with no debt for the build-out (France's debt carries its banks' recapitalisation as well, "
      "decision 70: the levy adds none to it)",
      all(lv[r]["financing_room_end_pct_gdp"] > lv[r]["financing_room_start_pct_gdp"] for r in ("US", "EA", "SE"))
      and all(abs(NW(lv, r) - NW(bo, r)) < 0.05 for r in ("US", "EA", "SE"))
      and all(lv[r]["debt_added_end_pct_gdp"] == 0 for r in gc.R if regs[r].sov_debt == 0)
      and lv["FR"]["debt_added_end_pct_gdp"] <= bo["FR"]["debt_added_end_pct_gdp"],
      {r: (lv[r]["financing_room_start_pct_gdp"], lv[r]["financing_room_end_pct_gdp"], NW(lv, r), NW(bo, r)) for r in ("US", "EA", "SE")})
check("K5 taxing workers to pay for it costs jobs: financed by labour taxes, US year-6 non-employment is at least a point above "
      "the levy's, and Sweden's at least 0.2. Restated 2026-10-26 after the bust moved to the 2000-02 bust's measured path and the start to the dated vintage (Log 42): before it at least 1.5 and 0.3 (15.33 against 13.65; 4.71 "
      "against 4.37)",
      NW(tx) - NW(lv) >= 1.0 and NW(tx, "SE") - NW(lv, "SE") >= 0.2, {r: (NW(tx, r), NW(lv, r)) for r in gc.R})
check("K6 the price of debt does not bind at a build-out's size: under 5 bp in every region outside France, the rest of the "
      "euro area included, with at most 5% of GDP added over six years; in France the build-out adds under 5 bp and a point "
      "of GDP to what its banks' recapitalisation adds (the levy's run, which borrows nothing for the build-out: decision "
      "70). Restated 2026-10-28 after seeing the run (decision 91): before it France too under 5 bp, 0.26% of GDP added",
      all(bo[r]["debt_premium_max_bp"] < 5 and bo[r]["debt_added_end_pct_gdp"] <= 5 for r in gc.R if r != "FR")
      and bo["FR"]["debt_premium_max_bp"] - lv["FR"]["debt_premium_max_bp"] < 5
      and bo["FR"]["debt_added_end_pct_gdp"] - lv["FR"]["debt_added_end_pct_gdp"] < 1,
      {r: (bo[r]["debt_premium_max_bp"], bo[r]["debt_added_end_pct_gdp"]) for r in gc.R} | {"FR, the levy's": (lv["FR"]["debt_premium_max_bp"], lv["FR"]["debt_added_end_pct_gdp"])})
slow = fl("care financed by borrowing", row3, fast=False)
check("K7 with a point a year the pace binds before any financing limit (borrowing without a cap within half a point of the capped "
      "build-out); with three points a year, financing decides: taxes on labour leave US non-employment's rise at least a "
      "point above the levy's and borrowing's. Restated 2026-10-26 after the bust moved to the 2000-02 bust's measured path and the start to the dated vintage (Log 42): before it at least 1.5 (15.33 against 13.65)",
      abs(NW(slow) - NW(build_)) < 0.5 and NW(tx) - max(NW(lv), NW(bo)) >= 1.0,
      f"a point a year +{NW(slow)} (capped +{NW(build_)}); three: levy +{NW(lv)}, borrowing +{NW(bo)}, labour taxes +{NW(tx)}")

print("E — the euro area in two: France and the rest of the union (decision 70)")
end = pd.Period(gc.START, "Q").end_time
at = lambda sid: vintage.read(sid).loc[:end]  # noqa: E731
fu, eu, fn, en = (at(x) for x in ("FR_UNEMPLOYMENT", "EA21_UNEMPLOYMENT", "FR_UNEMPLOYED", "EA21_UNEMPLOYED"))
lf_fr, lf_ea = fn.iloc[-1] / fu.iloc[-1], en.iloc[-1] / eu.iloc[-1]
merged_u = (regs["EA"].u0 * (lf_ea - lf_fr) + regs["FR"].u0 * lf_fr) / lf_ea
w_fr = float(at("FR_HICP_WEIGHT").iloc[-1]) / 1000
merged_pi = (1 - w_fr) * regs["EA"].pi0 + w_fr * regs["FR"].pi0
spr = (at("FRGVB10Y") - at("DEGVB10Y")).dropna()
check("E1 the start measured: the two halves' unemployment recombine, on Eurostat's labour forces, into the euro area's; "
      "their core inflation, at France's HICP weight, into the euro area's; their sizes into the euro area's quarter, split "
      "by GDP; France's spread over Germany at 30 Sep against its mean from July 2025 to June 2026; its debt (Eurostat) "
      "and its banks' holdings of euro-area government debt (the ECB) over GDP",
      abs(merged_u - float(eu.iloc[-1])) < 1e-9 and abs(merged_pi - vintage.yoy(at("00XEFDEZ19M086NEST"))) < 1e-9
      and abs(regs["EA"].size + regs["FR"].size - 0.25) < 1e-3 and regs["EA"].union == regs["FR"].union == "EA"
      and abs(regs["FR"].sov0 - float(spr.iloc[-1])) < 1e-12 and f"{spr.index[-1]:%Y-%m-%d}" == "2026-09-30"
      and regs["FR"].sov0 > regs["FR"].sov_calm and regs["FR"].sov_debt > 100 and 10 < regs["FR"].sov_banks < 20,
      f"u: France {regs['FR'].u0}, the rest {regs['EA'].u0:.2f} -> {merged_u:.2f} (the euro area {float(eu.iloc[-1])}); "
      f"core: France {regs['FR'].pi0:.2f}, the rest {regs['EA'].pi0:.2f}; sizes {regs['FR'].size} + {regs['EA'].size}; "
      f"France's spread {regs['FR'].sov0:.2f} (calm {regs['FR'].sov_calm:.2f}), debt {regs['FR'].sov_debt}% of GDP, "
      f"its banks' holdings {regs['FR'].sov_banks:.1f}%")
# two identical halves in a union, trading with the world as the whole did, against the one region
def split_test(rl) -> tuple:
    whole = {r: g for r, g in regs.items() if r != "FR"}
    whole["EA"] = replace(whole["EA"], size=0.25, union="", trade={q: v for q, v in regs["EA"].trade.items() if q != "FR"})
    whole = {r: (replace(g, trade={**{q: v for q, v in g.trade.items() if q != "FR"}, "EA": g.trade.get("EA", 0) + g.trade.get("FR", 0)})
                 if r != "EA" else g) for r, g in whole.items()}
    tw = sum(whole["EA"].trade.values())
    whole["EA"] = replace(whole["EA"], trade={q: v / tw for q, v in whole["EA"].trade.items()})
    mutual = 0.3                                   # each half sends 30% of its exports to the other, tariff-free
    half_trade = lambda other: {**{q: v * (1 - mutual) for q, v in whole["EA"].trade.items()}, other: mutual}  # noqa: E731
    halves = {**{r: replace(g, trade={**{q: v for q, v in g.trade.items() if q != "EA"}, "EA": g.trade["EA"] / 2, "FR": g.trade["EA"] / 2})
                 for r, g in whole.items() if r != "EA"},
              "EA": replace(whole["EA"], size=0.125, union="EA", exports=whole["EA"].exports / (1 - mutual), trade=half_trade("FR")),
              "FR": replace(whole["EA"], name="FR", size=0.125, union="EA", exports=whole["EA"].exports / (1 - mutual), trade=half_trade("EA"))}
    a_ = gc.simulate(whole, {r: rl for r in whole}, gc.ai_shock(N), cm, N)
    b_ = gc.simulate(halves, {r: rl for r in halves}, gc.ai_shock(N), cm, N)
    d_ = max(float(np.abs(a_[r][k] - b_[q][k]).max()) for r, q in (("US", "US"), ("SE", "SE"), ("CN", "CN"), ("EA", "EA"), ("EA", "FR"))
             for k in ("y", "u", "i", "k", "s"))
    return d_, halves, a_, b_


d, halves, _, _ = split_test(gc.MODERN)
d_e, _, a_e, b_e = split_test(gc.ERODED)
apart = gc.simulate(halves, {r: gc.MODERN for r in halves}, gc.Shock(demand={"FR": gc.ramp(-3.0, 1, 6, N)}), cm, N)
check("E2 the union's arithmetic nests the one euro area: two identical halves in a union, each half the size and trading "
      "with each other tariff-free, reproduce the single region and every other region's path exactly, the rest of the "
      "world and the shared mood in play (a union partner's slump reaches a member only as far as it differs from its "
      "own, one rate is set on the members' readings, and the rest of the world's gap and the mood leave out a region's "
      "union partners as well as itself, decision 91), under today's rules and under eroding ones (no backstop: the "
      "halves' banks lose all their capital, so the mood is at its largest); a shock to one half alone spills over to the "
      "other. Restated 2026-10-28 for the engine fix that put the full setting back: at the first pass the nesting held "
      "only with the rest of the world and the mood out of play, and E7 stated the departure (0.21 points); E7 is retired",
      d < 1e-9 and d_e < 1e-9 and b_e["FR"]["stress"].max() > 0.5 and apart["EA"]["y"].min() < -0.01,
      f"largest difference {d:.1e} (today's rules), {d_e:.1e} (eroding: the halves' capital lost up to "
      f"{b_e['FR']['stress'].max():.2f}); a French-only shock moves the rest {apart['EA']['y'].min():.2f} (France "
      f"{apart['FR']['y'].min():.2f})")
o = gc.simulate(regs, P("modern rules"), gc.ai_shock(N), cm, N)
oe = gc.simulate(regs, P("rules erode under pressure"), gc.ai_shock(N), cm, N)
check("E3 one policy rate: in the union the rest of the euro area and France have the same rate every month, under "
      "today's rules and eroding ones",
      np.allclose(o["EA"]["i"], o["FR"]["i"], atol=0) and np.allclose(oe["EA"]["i"], oe["FR"]["i"], atol=0))
# the doom loop: extra French bank losses, with and without the two links (the recapitalisation's debt, the holdings)
hit = gc.ai_shock(N)
hit.losses["FR"] = hit.losses["FR"] + gc.pulse(4.0, gc.step_index(2, gc.DT), 4 * gc.quarter_steps(gc.DT), N)
loop = gc.simulate(regs, P("modern rules"), hit, cm, N)
cut = gc.simulate({**regs, "FR": replace(regs["FR"], sov_banks=0.0, debt_slope=0.0, debt_slope_crisis=0.0)},
                  P("modern rules"), hit, cm, N)
rise_loop = float(loop["FR"]["sov"].max() - regs["FR"].sov0)
check("E4 the doom loop, at the measured price of debt: with French banks losing 4% of their loans more over 2027, the state's "
      "recapitalisation raises France's spread and French output falls further than without the loop; stated as found "
      "(the loop is weak at these sizes: what moves France's spread is a premium, not its banks)",
      rise_loop > 0 and loop["FR"]["y"].min() < cut["FR"]["y"].min() and rise_loop < 0.5,
      f"France's spread +{rise_loop:.3f} at most; French output {loop['FR']['y'].min():.2f} against {cut['FR']['y'].min():.2f} "
      f"without the loop; capital lost {loop['FR']['stress'].max():.2f}")
prem = gc.ai_shock(N)
prem.spread = {"FR": np.minimum(np.arange(N) * gc.DT, 1.0) * 2.0}
mod = P("modern rules")
free = gc.simulate(regs, mod, prem, cm, N)
capped = gc.simulate(regs, {r: (replace(rl, tpi=0.5) if r == "FR" else rl) for r, rl in mod.items()}, prem, cm, N)
nw = lambda o_, r: float((o_[r]["u"] + o_[r]["out"]).max())  # noqa: E731
check("E5 the ECB's backstop for France (TPI): capped half a point above its start, France's spread never passes the cap, "
      "and with a two-point premium France's output falls less and fewer are out of work than uncapped",
      capped["FR"]["sov"].max() <= regs["FR"].sov0 + 0.5 + 1e-12 and free["FR"]["sov"].max() > regs["FR"].sov0 + 1.9
      and capped["FR"]["y"].min() > free["FR"]["y"].min() and nw(capped, "FR") < nw(free, "FR"),
      f"spread {free['FR']['sov'].max():.2f} uncapped, {capped['FR']['sov'].max():.2f} capped; French output "
      f"{free['FR']['y'].min():.2f} -> {capped['FR']['y'].min():.2f}; out of work {nw(free, 'FR'):.2f} -> {nw(capped, 'FR'):.2f}")
check("E6 France's spread already present at the start reaches its borrowers: the private spread at index 0 is half of "
      "its excess over the calm level, and nowhere else in the union",
      abs(o["FR"]["s"][0] - regs["FR"].sov_pass * (regs["FR"].sov0 - regs["FR"].sov_calm)) < 1e-12 and o["EA"]["s"][0] == 0,
      f"France {o['FR']['s'][0]:.3f}, the rest {o['EA']['s'][0]}")

print("T — the step and the extensions (decisions 80 and 84-88), each on the Common it needs")
# at a quarter every per-step coefficient is returned untouched; at a month each is carried over
c_m, g_m, r_m = gc.step_common(cm, 1 / 12), gc.step_region(regs["US"], 1 / 12), gc.step_rules(gc.MODERN, 1 / 12)
check("T1 at a quarter the step changes nothing: the coefficients come back as the same objects; at a month each does "
      "over a quarter what it did (a share closed, compounded; a persistence, to the power of the step; the rate's "
      "long-run effect on the gap kept), and the quarter's counts are counted in steps",
      gc.step_common(cm, gc.Q) is cm and gc.step_region(regs["US"], gc.Q) is regs["US"] and gc.step_rules(gc.MODERN, gc.Q) is gc.MODERN
      and abs(1 - (1 - g_m.speed) ** 3 - regs["US"].speed) < 1e-12 and abs(c_m.a1 ** 3 - cm.a1) < 1e-12
      and abs(c_m.a_r / (1 - c_m.a1) - cm.a_r / (1 - cm.a1)) < 1e-12 and r_m.fiscal_quarters == 3 * gc.MODERN.fiscal_quarters
      and r_m.tariff_q == 3 * (gc.MODERN.tariff_q - 1) + 1,
      f"speed {regs['US'].speed} a quarter, {g_m.speed:.4f} a month; a1 {cm.a1} -> {c_m.a1:.4f}; a_r {cm.a_r:.4f} -> {c_m.a_r:.4f}")
sh_q, sh_m = gc.ai_shock(28, 1.3, 0.8, delay=2.4, dt=gc.Q), gc.ai_shock(82, 1.3, 0.8, delay=2.4, dt=1 / 12)
rq, rm = gc.ai_shock(28, 1.2, 1.6, delay=3, shape="ramp", dt=gc.Q), gc.ai_shock(82, 1.2, 1.6, delay=3, shape="ramp", dt=1 / 12)
check("T3 the bust at a monthly step is the quarterly bust read by month: at each quarter's end the measured path's "
      "equity and build-out are the quarterly ones, and the loan losses total the same; the straight-line fall reaches "
      "the same depth in the same quarter",
      np.allclose(sh_m.equity["US"][::3], sh_q.equity["US"], atol=1e-12) and np.allclose(sh_m.capex["EA"][::3], sh_q.capex["EA"], atol=1e-12)
      and abs((sh_m.losses["US"] / 12).sum() - (sh_q.losses["US"] / 4).sum()) < 1e-9
      and np.allclose(rm.equity["US"][::3], rq.equity["US"], atol=1e-12)
      and abs((rm.losses["US"] / 12).sum() - (rq.losses["US"] / 4).sum()) < 1e-9,
      f"losses {(sh_q.losses['US'] / 4).sum():.4f} and {(sh_m.losses['US'] / 12).sum():.4f} % of loans")
# the bust's loan losses on the level paths' clock (_spread, fixed 2026-10-28: decision 91, found by review)
so_far = lambda sh, dt: np.cumsum(sh.losses["US"] * dt)                 # % of loans lost so far  # noqa: E731
lag = {}
for sp_, dl_ in ((1.0, 0.0), (1.0, 2.4), (1.3, 2.4), (0.7, 1.0)):
    lq = so_far(gc.ai_shock(24, speed=sp_, delay=dl_, dt=gc.Q), gc.Q)
    lm = so_far(gc.ai_shock(N, speed=sp_, delay=dl_, dt=1 / 12), 1 / 12)
    lag[(sp_, dl_)] = max(abs(lm[3 * j] - lq[j]) for j in range(24) if 3 * j < N)
check("T12 the bust's loan losses at a month are the quarterly model's read by month: at every quarter's end the losses "
      "so far (% of loans) equal the quarterly run's at that quarter, for the central bust (speed 1, no delay) and for "
      "delayed, faster and slower ones (added 2026-10-28 with the fix: before it the monthly losses landed two months "
      "late, up to 0.12% of loans behind at a quarter's end of the US's 1.5%, found by a probe of the old form)",
      max(lag.values()) < 1e-12, "largest difference (speed, delay): " + ", ".join(f"{k} {v:.1e}" for k, v in lag.items()))
wq, eqf = gc.bust_2000()["losses"], gc.bust_2000()["measured"]["equity_fall"]
clock = {}
for sp_, dt_ in ((2.0, gc.Q), (0.5, gc.Q), (1.5, 1 / 12), (0.75, 1 / 12)):
    sh_ = gc.ai_shock(60, speed=sp_, dt=dt_)
    on_, per = (1, sp_) if dt_ == gc.Q else (3, sp_ / 3)                    # the peak's quarter's end; quarters a step
    lost = so_far(sh_, dt_) / gc.BUST_LOSSES["US"]
    pts = [(i, int(round((i - on_) * per))) for i in range(60)
           if (i - on_) * per >= 0 and abs((i - on_) * per - round((i - on_) * per)) < 1e-9 and round((i - on_) * per) < len(wq)]
    clock[(sp_, "quarter" if dt_ == gc.Q else "month")] = (
        max(abs(lost[i] - wq[:m + 1].sum()) for i, m in pts), max(abs(sh_.equity["US"][i] - eqf[m]) for i, m in pts), len(pts))
check("T13 and the flows keep the level paths' clock at a speed other than one: wherever the level paths read a measured "
      "quarter's end (US equity there the measured fall of that quarter), the losses so far are the measured weights "
      "through that quarter, at twice and half the speed by quarter and at 1.5 and 0.75 times by month (added 2026-10-28 "
      "with the fix: before it, at a speed other than one, the flows ran off that clock, 6-10% of the total out, found "
      "by a probe of the old form)",
      all(v[0] < 1e-12 and v[1] < 1e-12 and v[2] >= 12 for v in clock.values()),
      "(losses, equity, points) by (speed, step): " + ", ".join(f"{k} ({v[0]:.1e}, {v[1]:.1e}, {v[2]})" for k, v in clock.items()))

# the model's extensions for the monthly refit (decisions 84-88), each on its own: the US alone, its expectations pinned to
# the target (anchor 1), its rate as set, its neutral rate the model's and no year-before rate; each check's Common is the
# fit's with the four extensions off (rate-sensitive spending, repricing, oil's capacity, expectations on a window) and
# its own channel on, so a channel's arithmetic can be read off the run
ext_off = replace(cm, a_f=0.0, reprice=0.0, cap_oil=0.0, expect_over=0.0)
us1 = replace(regs["US"], pi0=2.0, i0=2.0 + cm.r_star + 1.0, r_star=None, i_norm=None)
pin = replace(gc.MODERN, policy="path", anchor=1.0, pi_star=2.0, fiscal="none")
rl1 = {r: pin for r in gc.R}
flat_ = lambda n_, x: np.full(n_, float(x))  # noqa: E731
r1 = {**regs, "US": us1}
sh1 = gc.Shock(rate={"US": flat_(41, us1.i0)})
cm5 = replace(ext_off, a_f=0.5, f_speed=0.35)
o5q = gc.simulate(r1, rl1, sh1, cm5, 41, active=["US"], dt=gc.Q)["US"]
o5m = gc.simulate(r1, rl1, gc.Shock(rate={"US": flat_(13, us1.i0)}), cm5, 13, active=["US"], dt=1 / 12)["US"]
check("T5 rate-sensitive spending (decision 84): at a real rate a point above neutral it goes the fitted share of the way "
      "to its long-run level a quarter (-a_f x 0.35 after one), reaches it in the long run, and a month's step compounds "
      "to the quarter's; off (a_f 0, as fitted) it is nothing",
      abs(o5q["d_rate"][1] + 0.5 * 0.35) < 1e-12 and abs(o5q["d_rate"][40] + 0.5) < 1e-6
      and abs(o5m["d_rate"][3] - o5q["d_rate"][1]) < 1e-12 and abs(o5m["d_rate"][12] - o5q["d_rate"][4]) < 1e-12
      and not gc.simulate(r1, rl1, sh1, ext_off, 41, active=["US"], dt=gc.Q)["US"]["d_rate"].any()
      and not gc.simulate(r1, rl1, sh1, cm, 41, active=["US"], dt=gc.Q)["US"]["d_rate"].any(),
      f"after a quarter {o5q['d_rate'][1]:.4f}, a year {o5q['d_rate'][4]:.4f}, ten years {o5q['d_rate'][40]:.5f}; "
      f"by month {o5m['d_rate'][3]:.4f} at three months")
c6 = (cm.mpc_b - cm.mpc_rep) * us1.floating * us1.hh_debt / 100
cut = gc.Shock(rate={"US": np.concatenate([[us1.i0], flat_(12, us1.i0 - 1.0)])})
on6 = replace(ext_off, reprice=1.0)
o6 = gc.simulate(r1, rl1, cut, on6, 13, active=["US"], dt=gc.Q)["US"]
o6b = gc.simulate({**r1, "US": replace(us1, i_norm=us1.i0 + 1.0)}, rl1, sh1, on6, 13, active=["US"], dt=gc.Q)["US"]
o6c = gc.simulate(r1, rl1, cut, ext_off, 13, active=["US"], dt=gc.Q)["US"]
o6d = gc.simulate({**r1, "US": replace(us1, i_norm=us1.i0 + 1.0)}, rl1, cut, ext_off, 13, active=["US"], dt=gc.Q)["US"]
check("T6 relief from the rate debts paid before the start (decision 85): with floating-rate debt repricing over a year, a "
      "cut of a point reaches a quarter of its relief in the first quarter and all of it after four; a start a point "
      "under the year's average rate is relief already owed, passed on as the debt reprices; off, the cut's relief is "
      "whole at once, from the start's rate, whatever the year before",
      abs(o6["d_relief"][1] - c6 / 4) < 1e-12 and abs(o6["d_relief"][4] - c6) < 1e-12 and abs(o6["d_relief"][8] - c6) < 1e-12
      and abs(o6b["d_relief"][1] - c6 / 4) < 1e-12 and abs(o6b["d_relief"][4] - c6) < 1e-12 and abs(o6c["d_relief"][1] - c6) < 1e-12
      and np.array_equal(o6d["d_relief"], o6c["d_relief"]),
      f"a point's relief {c6:.4f}: {o6['d_relief'][1]:.4f} after a quarter, {o6['d_relief'][4]:.4f} after a year")
us7 = replace(us1, i0=2.0 + cm.r_star, energy_weight=0.04, energy_pass=(0.23, 0.1), consumption_share=0.68, energy_income=0.4)
oil = gc.Shock(rate={"US": flat_(21, us7.i0)}, oil={"US": np.concatenate([[80.0], flat_(20, 120.0)])}, oil_before={"US": 80.0})
o7 = gc.simulate({**r1, "US": us7}, rl1, oil, replace(ext_off, cap_oil=2.0), 21, active=["US"], dt=gc.Q)["US"]
o7n = gc.simulate({**r1, "US": us7}, rl1, oil, ext_off, 21, active=["US"], dt=gc.Q)["US"]
kap = cm.kappa
check("T7 oil idles capacity (decision 86): with the energy term on, the capacity lost approaches cap_oil x the rise in "
      "consumers' energy bill at a quarter's share of 0.25, lowers the measured gap, and core inflation answers the gap "
      "against capacity (the measured gap plus the capacity lost); off, nothing moves",
      abs(o7["cap"][1] - 0.25 * 2.0 * o7["e_bill"][1]) < 1e-12 and bool(np.all(o7["y"][1:] < o7n["y"][1:]))
      and float(np.max(np.abs(o7["pi"][1:] - 2.0 - kap * (o7["y"][1:] + o7["cap"][1:])))) < 1e-12
      and not o7n["cap"].any() and o7["y"][20] < o7n["y"][20] - 1.0,
      f"energy bill +{o7['e_bill'][20]:.2f}% of GDP; capacity lost {o7['cap'][20]:.2f}; the gap {o7['y'][20]:.2f} against "
      f"{o7n['y'][20]:.2f} without")
ad = replace(gc.MODERN, policy="path", anchor=0.0, pi_star=2.0, fiscal="none")
spike = gc.Shock(rate={"US": flat_(13, us7.i0)}, oil={"US": np.concatenate([[80.0, 80.0, 160.0], flat_(10, 160.0)])},
                 oil_before={"US": 80.0})
o8 = gc.simulate({**r1, "US": replace(us7, pi_h0=2.0)}, {r: replace(ad, expect_from="headline") for r in gc.R}, spike,
                 replace(ext_off, expect_over=1.0), 13, active=["US"], dt=gc.Q)["US"]
pie8 = [np.mean([o8["pi_h"][max(j, 0)] for j in range(k - 4, k)]) for k in range(1, 13)]
check("T8 expectations on smoothed inflation (decision 87): adapting to the past year's inflation, a quarter's oil spike in "
      "headline moves expected inflation by a quarter of it the next quarter (core answers the past year's average, "
      "the months before the start at index 0's reading)",
      float(np.max(np.abs(o8["pi"][1:] - np.array(pie8) - kap * o8["y"][1:]))) < 1e-12,
      f"headline in the spike's quarter {o8['pi_h'][2]:.2f}; core the quarter after {o8['pi'][3]:.2f}")
r9 = {**regs, "US": replace(regs["US"], r_star=None)}
base9 = gc.simulate(r9, {r: gc.MODERN for r in gc.R}, gc.ai_shock(12, dt=gc.Q), ext_off, 12, dt=gc.Q)
same = gc.simulate({**r9, "US": replace(r9["US"], r_star=cm.r_star)}, {r: gc.MODERN for r in gc.R}, gc.ai_shock(12, dt=gc.Q), ext_off, 12, dt=gc.Q)
up = gc.simulate({**r9, "US": replace(r9["US"], r_star=cm.r_star + 1.0)}, {r: gc.MODERN for r in gc.R}, gc.ai_shock(12, dt=gc.Q), ext_off, 12, dt=gc.Q)
check("T9 a region's neutral rate (decision 88): set to the model's it changes nothing; a point higher, the policy rule's "
      "target is a point higher, so the first quarter's rate rises by the share the rule moves a quarter (1 - smoothing)",
      all(np.array_equal(same[r][k], base9[r][k]) for r in base9 for k in base9[r])
      and abs(up["US"]["i"][1] - base9["US"]["i"][1] - (1 - cm.smooth)) < 1e-12,
      f"the US rate in 2026Q4 {base9['US']['i'][1]:.3f}, {up['US']['i'][1]:.3f} with a neutral rate a point higher")

# expectations on a year's window at a shorter step: a deviation of 4 points, the rate held at neutral, no slope
dev = replace(us1, pi0=6.0, i0=2.0 + cm.r_star)
an = replace(gc.MODERN, policy="path", anchor=0.6, pi_star=2.0, fiscal="none")
c10 = replace(ext_off, expect_over=1.0, kappa=0.0)
path = {}
for name, dt in (("quarter", 0.25), ("month", 1 / 12), ("week", 1 / 52)):
    n10 = int(round(3 / dt)) + 1
    o10 = gc.simulate({**r1, "US": dev}, {r: an for r in gc.R}, gc.Shock(rate={"US": flat_(n10, dev.i0)}), c10, n10,
                      active=["US"], dt=dt)["US"]
    path[name] = np.array([o10["pi"][int(round(q * 0.25 / dt))] - 2.0 for q in (1, 4, 8, 12)])
gap_mq = np.abs(path["month"] - path["quarter"])
gap_wm = np.abs(path["week"] - path["month"])
check("T10 expectations on the past year's inflation keep their pace at any step (decision 87): with the quarter's anchor "
      "on a year's window, a deviation of inflation from the target decays to under a tenth of itself within three "
      "years by quarter, by month and by week, and the paths at each quarter's end converge as the step shrinks (the "
      "week nearer the month than the month the quarter); with the per-step anchor on the window a month kept 17% "
      "after three years and a shrinking step none (found 2026-10-27)",
      all(abs(path[k][-1]) < 0.4 for k in path) and bool(np.all(gap_wm < gap_mq)),
      "after a quarter, a year, two and three years: " + "; ".join(f"{k} " + "/".join(f"{x:.2f}" for x in v) for k, v in path.items()))

# and the slope: on the window at a month inflation is the expectation plus kappa x the gap, kappa unconverted
cs = replace(ext_off, expect_over=1.0)
n11 = 37
o11 = gc.simulate({**r1, "US": dev}, {r: an for r in gc.R},
                  gc.Shock(rate={"US": flat_(n11, dev.i0)}, demand={"US": np.r_[0.0, flat_(n11 - 1, -2.0)]}), cs, n11,
                  active=["US"], dt=1 / 12)["US"]
pie11 = [an.anchor * an.pi_star + (1 - an.anchor) * np.mean([o11["pi"][max(j, 0)] for j in range(k - 12, k)])
         for k in range(1, n11)]
res11 = float(np.max(np.abs(o11["pi"][1:] - np.array(pie11) - cs.kappa * o11["y"][1:])))
check("T11 on the window the Phillips slope is the quarter's at a month (decision 87): with a gap held open, inflation "
      "is the expectation (the quarter's anchor on the past year) plus kappa x the gap, kappa unconverted (added after "
      "a review found T10, run without a slope, could not catch the slope reverted)",
      bool(np.abs(o11["y"][1:]).max() > 0.5) and res11 < 1e-12, f"largest residual {res11:.2e}; gap at the end {o11['y'][-1]:.2f}")

n_ok = sum(ok for _, ok, _ in RESULTS)
print(f"\n{n_ok}/{len(RESULTS)} checks passed")
sys.exit(0 if n_ok == len(RESULTS) else 1)
