# check_case.py — her case (code/case.py): the model's additions change nothing when off, the settings trace to their
# sources, the start is the dated vintage, the bust is the 2000-02 bust's measured path from the quarter of today's peak,
# the dating is one and the 73-month horizon changes nothing before it, the levers are dated, and the findings, stated as
# found.
#
# Rebuilt 2026-10-26 with the case (STATE Log 42): the case runs on the start's dated vintage (vintage.py, cache/start/)
# and its bust on the 2000-02 bust's measured path (global_crash.bust_2000), at her 1.5x size, from 2026Q4 (the quarter
# of the Nasdaq's and the S&P's high, 6 Oct). The findings below are stated as found on that day (FOUND), every number in
# one place; the bust as first built (ai_shock's ramps, held) is gated to reproduce exactly (K1), and the 8 Oct case it
# carried reproduces at the tag paths-pre-signfix. K4 and V1-V2 are new; K7-K11 restate the case's findings.
#
# Restated 2026-10-28 on the adopted monthly fit (decision 91): the case runs by month (73 months, to the end of 2032Q3),
# its quarter-named readings the quarters' averages, its fiscal levers on dates set by the case's own runs (K13), the fit's
# debt deflation reported (K14). Every value in K1, K3, K4, K6-K14 and A1-A3 was restated after seeing the run, as found,
# and each says so; the values before stand beside them.
#
# Restated again the same day on the refit of decision 92 (the 1929-33 bank runs measured, debt deflation levelling off)
# and the review's fix to the bust's loss flows (_spread, decision 91): every value in K1, K4, K6-K12, K14 and A1-A2 was
# restated after seeing that run, as found, the first pass's beside it (RESTATED2); K8's bounds and K14's ceiling were set
# after seeing it, and say so; K3, K13 and A3 found the same values, and say so. The verdict reads the unrounded readings
# since then (case.verdict).
#
# Run from paths/:  ../venv/Scripts/python.exe checks/check_case.py
# Exit status 0 only if every check passes.

from __future__ import annotations

import hashlib
import inspect
import json
import os
import sys
from dataclasses import fields

import numpy as np
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "code"))
import case  # noqa: E402
import global_crash as gc  # noqa: E402
import vintage  # noqa: E402

RESULTS = []
RESTATED = "Restated 2026-10-28 on the adopted monthly fit (decision 91), as found after seeing the run"
RESTATED2 = ("Restated again 2026-10-28 on the refit (decision 92: the bank runs measured, debt deflation levelling off; "
             "the loss flows on the levels' clock), as found after seeing its run")

# the findings as found on 2026-10-28 (high end unless stated; US out of work = unemployed + left the workforce, %)
FOUND = {}


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


C = json.load(open(os.path.join(ROOT, "results", "case.json"), encoding="utf-8"))
G = json.load(open(os.path.join(ROOT, "results", "global_crash.json"), encoding="utf-8"))
P = json.load(open(os.path.join(ROOT, "results", "pace.json"), encoding="utf-8"))
cm, regs, pdates = case.stored()
st = C["settings"]
DT = gc.DT
N70 = gc.months(24)                         # global_crash's stored runs: 70 months, to the end of 2032Q2

print("K — the model's additions, the settings, the bust")
rg, o = case.reference(cm, regs, pdates, N70)      # K12: the case's last three months change none of these
key = "modern rules | bust + displacement | two waves, robotics in 2 years, care absorbs"
same = json.loads(json.dumps({"year4": gc.summary(o, rg, 16, DT), "year6": gc.summary(o, rg, None, DT)})) == G["scenarios"][key]
a = gc.ai_shock(N70, dt=DT)
m = gc.bust_2000()["measured"]
L = gc.quarter_steps(DT)                    # 3: the onset (index 1, the peak's quarter) is the end of December 2026
read_at = lambda arr, after: np.array([0.0 if s < L else float(np.interp((s - L) / L, np.arange(len(arr)), arr, right=after))  # noqa: E731
                                       for s in range(N70)])
cum = np.concatenate([[0.0], np.cumsum(gc.bust_2000()["losses"])])
cum_at = lambda x: np.interp(x, np.arange(len(cum)), cum, left=0.0, right=cum[-1])  # noqa: E731
# month s's flow: the measured losses between the level legs' readings at months s - 1 and s (quarter (s - L) / L at
# month s; the flow of measured quarter j running from j - 1 to j)
flow = np.array([cum_at((s - L) / L + 1) - cum_at((s - 1 - L) / L + 1) for s in range(N70)])
shock_same = (np.allclose(a.equity["US"], read_at(m["equity_fall"], 0.0), atol=1e-12)
              and np.allclose(a.equity["EA"], 0.25 / 0.40 * read_at(m["equity_fall"], 0.0), atol=1e-12)
              and np.allclose(a.capex["US"], read_at(m["capex_share_lost"], m["capex_share_lost"][-1]), atol=1e-12)
              and np.allclose(a.losses["US"], 1.5 * flow / DT, atol=1e-12))
aq = gc.ai_shock(24, dt=gc.Q)
ends_same = (all(np.allclose(getattr(a, leg)["US"][::L], getattr(aq, leg)["US"], atol=1e-12) for leg in ("equity", "capex"))
             and np.allclose(np.cumsum(a.losses["US"] * DT)[::L], np.cumsum(aq.losses["US"] * gc.Q), atol=1e-12))
rp = gc.ai_shock(N70, shape="ramp", dt=DT)
ramp_same = (np.allclose(rp.equity["US"][:19:3], [0, 0.1, 0.2, 0.3, 0.4, 0.4, 0.4])
             and np.allclose(rp.capex["US"][:19:3], [0, 0.15, 0.3, 0.45, 0.6, 0.6, 0.6])
             and np.allclose(rp.losses["US"][:31], [0.0] * 4 + [0.75] * 24 + [0.0] * 3))
check("K1 the model's central run (today's rules on their stored dates) reproduces its stored scenario exactly at the "
      "monthly step; its default bust is the 2000-02 bust's measured legs from the end of 2026Q4 (US household equity's "
      "fall as measured, read at each month's end, the euro area at 0.25/0.40 of it, the build-out's share lost as "
      "measured, 1.5% of US loans spread on the measured losses, each month's flow the measured losses between the level "
      "legs' readings at the month's start and end, from October 2026), built here independently, and at each quarter's "
      "end the legs, and the losses to date, are the quarterly model's; and the bust as first built (shape='ramp': "
      "straight-line falls over four quarters, held; the losses evenly over eight, from January 2027) is kept exactly. "
      + RESTATED + ". " + RESTATED2 + ": each month's flow was the measured quarter's from the month's end, two months "
      "behind the levels, before the review's fix (_spread); the quarter ends' losses to date are new",
      same and shock_same and ends_same and ramp_same, f"{key}; reproduces {same}, legs {shock_same}, quarter ends {ends_same}, ramp {ramp_same}")

seen = P["paces"]["multiples_of_the_papers"]["trend + 2 s.e."]
cap_ok = all(abs(st["care_cap"][r] - (regs[r].care_share + max(regs[r].care_trend, 0.0))) < 0.006 for r in gc.R)
union_in = {r: sum(v for q, v in regs[r].trade.items() if regs[r].union and q in regs and q != r and regs[q].union == regs[r].union)
            for r in gc.R}
tar_ok = st["tariff"]["US"] == 25.0 and all(abs(st["tariff"][r] * (1 - union_in[r]) - 25.0 * regs[r].trade.get("US", 0.0)) < 0.006
                                            for r in ("EA", "FR", "SE", "CN")) and union_in["FR"] > 0.4 and union_in["SE"] == 0
ig = vintage.read("BAMLC0A0CM").loc[:case.INDEX0_END]
s0_ok = abs(st["spread0"]["US"] - round(float(ig.iloc[-1] - ig.iloc[-64]), 4)) < 1e-9 and ig.index[-1] <= pd.Timestamp(case.INDEX0_END)
check("K2 the settings trace to their sources: the starting pace is pace.py's upper bound on what has been seen; each care "
      "ceiling is today's share plus one year of its trend (today's share where care is shrinking: France); the tariff "
      "each region's exports face is 25 points times its export share to the US (the US: 25), as a tariff on what it sells "
      "outside its union (the model's tariffs spare trade inside the euro area: decision 70); the spread already present at the start is the US corporate OAS's rise over "
      "the 63 prints to 30 Sep (decision 47; index 0 is measured on data to September)",
      st["pace"]["seen"] == seen and cap_ok and tar_ok and s0_ok,
      f"seen {st['pace']['seen']}; caps {st['care_cap']}; tariffs {st['tariff']}; spread0 {st['spread0']} (to {ig.index[-1]:%Y-%m-%d})")
lp = case.logistic_pace(1.0, seen, st["pace"]["mid_quarter"], st["pace"]["width_quarters"])
k_mid = int(round(st["pace"]["mid_quarter"] * gc.Q / DT))           # month 21, the end of 2028Q2
half = (lp[k_mid] - seen) / (1 - seen)
check("K3 the pace, by month, starts at the upper bound seen, rises monotonically, is half-way at the end of 2028Q2 (month "
      "21, June 2028) and within 5% of the paper's pace by the last month (September 2032). " + RESTATED + " (index 7, a "
      "quarter, before); the same on the refit (decision 92), from its lower pace seen", abs(lp[0] - seen) < 1e-9 and np.all(np.diff(lp) > 0) and abs(half - 0.5) < 0.05
      and lp[-1] > 0.95 and len(lp) == case.N == 73 and gc.month_label(k_mid) == "2028-06"
      and gc.quarter_label(st["pace"]["mid_quarter"]) == "2028Q2",
      f"start {lp[0]:.3f}, {gc.month_label(k_mid)} {lp[k_mid]:.3f} (half-way {half:.2f}), {gc.month_label(len(lp) - 1)} {lp[-1]:.3f}")

bp = gc.bust_2000()
stored_bp = C["bust_path"]["from_the_2000_02_bust"]
bp_same = all(np.allclose(np.round(bp[k], 4), stored_bp[k], atol=1e-9) for k in ("equity", "capex", "losses"))
bs = case.bust_shock(case.N, st["bust"])
eq_us = bs.equity["US"]
eq_q = gc.to_quarters(eq_us, DT)
k_tr, q_tr = int(np.argmax(eq_us)), int(np.argmax(eq_q))
obs = C["vintage"]["observed"]
hi_q = gc.quarter_label(st["bust"]["onset"]) == str(pd.Period(obs["nasdaq_high"][0], "Q"))
# the losses the runs read (from index 1, the first simulated month: simulate never reads index 0), at the case's dating,
# by month and by quarter; and the whole 2.25 kept where the dating starts the path after the start (the default's)
bq = case.bust_shock(case.NQ, st["bust"], dt=gc.Q)
run_losses = (float((bs.losses["US"][1:] * DT).sum()), float((bq.losses["US"][1:] * gc.Q).sum()))
all_losses = float((gc.ai_shock(case.N, 1.5, dt=DT).losses["US"] * DT).sum())
check("K4 the bust is the 2000-02 bust at 1.5 times its measured size, dated from today's peak (the Nasdaq's 52-week high, "
      "6 Oct 2026, 0.71 of a quarter later in its quarter than 10 Mar 2000 was in its own): US household equity at most "
      "0.668 down at a month's end (1.5 times the measured 44.7%, read between quarters), in April 2029; the largest "
      "quarterly average 0.649, in 2029Q2; the build-out's excess over its trend at most 1.14 lost (1.5 times 76%); the "
      "losses 2.25% of US loans in all (the default's dating), of which the case's runs read 2.23 from the first simulated "
      "month, the same by month as by quarter: the peak's measured quarter begins before the start, and what falls before "
      "it is not in the run. What the vintage says, so far: it rules out the 8 Oct timing's fall "
      "(equity -30% at the end of 2026Q4, the speed-2 ramp), with the Nasdaq's 2026Q4 average to date 2.6% above its "
      "2026Q3 average; the case's fall is 2.5% on 2026Q4's average and 4.7% at its end. " + RESTATED + " (at the "
      "quarterly step: 0.645 at most, in 2029Q3; the 2026Q4 fall 4.7%, the quarter's end). " + RESTATED2 + ": the losses "
      "were '2.25 in all, at any dating', the sum of the monthly path; with the flows on the levels' clock the path at the "
      "case's dating holds 2.24 (0.01 before the first month's start is dropped, where the quarterly path keeps it at "
      "index 0, which no run reads), so the check now reads what the runs read. Restated 2026-10-26 with the "
      "review's fixes (Log 44: the measured sizes, dated from the peak, the US premium an alternative)",
      bp_same and abs(eq_us.max() - 0.6676) < 5e-5 and gc.month_label(k_tr) == "2029-04"
      and abs(eq_q.max() - 0.6494) < 5e-5 and gc.quarter_label(q_tr) == "2029Q2"
      and abs(bs.capex["EA"].max() / 1.5 - 0.762) < 5e-3
      and abs(all_losses - 2.25) < 1e-9 and abs(run_losses[0] - run_losses[1]) < 1e-9 and round(run_losses[0], 2) == 2.23
      and hi_q and abs(case.peak_shift(st["bust"]) - 0.712) < 1e-3
      and obs["nasdaq_q4_to_date_vs_q3_avg_pct"] > -10 and round(float(eq_q[1]), 3) == 0.025 and round(float(eq_us[L]), 3) == 0.047
      and abs(gc.ai_shock(case.N, 1.5, 2.0, shape="ramp", dt=DT).equity["US"][L] - 0.30) < 1e-12,
      f"trough {eq_us.max():.4f} in {gc.month_label(k_tr)} ({eq_q.max():.4f}, {gc.quarter_label(q_tr)}); build-out "
      f"{bs.capex['EA'].max():.3f}; losses {all_losses:.2f} in all, the runs' {run_losses[0]:.4f} by month, "
      f"{run_losses[1]:.4f} by quarter (the monthly path {float((bs.losses['US'] * DT).sum()):.4f}); 2026Q4 fall {eq_q[1]:.3f} "
      f"(its end {eq_us[L]:.3f}); Nasdaq Q4 to date vs Q3 {obs['nasdaq_q4_to_date_vs_q3_avg_pct']:+.2f}%, high {obs['nasdaq_high']}")

print("V — the start is the dated vintage")
man = vintage.manifest()
hashes = all(hashlib.sha256(open(os.path.join(vintage.START, f"{sid}.csv"), encoding="utf-8").read().encode()).hexdigest() == v["sha256"]
             for sid, v in man["series"].items())
fresh = gc.regions_today()
fresh.pop("_notes")
flds = ("u0", "i0", "pi0", "equity_wealth", "ai_capex", "hh_debt", "priv_debt")
start_same = all(abs(getattr(fresh[r], f) - G["regions"][r][f]) < 1e-12 for r in gc.R for f in flds)
check("V1 the start is the vintage: every file in cache/start/ has the hash its manifest records, and the stored regions "
      "(global_crash.json, which the case and the website's model read) are regions_today() on it",
      hashes and start_same, {r: {f: round(G["regions"][r][f], 3) for f in ("u0", "i0", "pi0", "equity_wealth", "ai_capex")} for r in ("US", "EA", "SE")})
end = pd.Period(gc.START, "Q").end_time
real_read = vintage.read


def poisoned(sid):
    """The series with every reading after the start's quarter replaced by a value no start could take, and one added."""
    x = real_read(sid).copy()
    x[x.index > end] = 9999.0
    return pd.concat([x, pd.Series([9999.0], index=[end + pd.Timedelta(days=15)])]).sort_index()


vintage.read = poisoned
try:
    fresh_p = gc.regions_today()
    fresh_p.pop("_notes")
    st_p = case.settings(regs, st["pace"]["seen"])
    rg_e, _ = case.build(cm, regs, st, sens={"energy": True})
    rg_ep = {r: rg_e[r].pi_h0 for r in case.ENERGY}
    poisoned_ok = True
except Exception:  # noqa: BLE001 — a start that reads past September may fail on the planted readings: that is a fail
    poisoned_ok = False
finally:
    vintage.read = real_read
rg_e2, _ = case.build(cm, regs, st, sens={"energy": True})
unmoved = poisoned_ok and (all(abs(getattr(fresh_p[r], f) - getattr(fresh[r], f)) < 1e-12 for r in gc.R for f in flds)
                           and st_p["spread0"] == st["spread0"] and all(abs(rg_ep[r] - rg_e2[r].pi_h0) < 1e-12 for r in case.ENERGY))
lag_ok = {sid: vintage.read(sid).loc[:end].index[-1] for sid in ("UNRATE", "PCEPILFE", "00XEFDEZ19M086NEST", "00XEFDSEM086NEST",
                                                                  "EA_UNEMPLOYMENT", "SEUNRATE", "PCEPI", "CP0000EZ19M086NEST")}
q_ok = {sid: vintage.read(sid).loc[:end].index[-1] for sid in ("BOGZ1LM153064475Q", "GDP")}
d_ok = {sid: vintage.read(sid).loc[:end].index[-1] for sid in ("DFF", "ECBDFR", "SECBREPOEFF", "BAMLC0A0CM")}
fresh_enough = (all(t >= pd.Timestamp("2026-08-01") for t in lag_ok.values()) and all(t >= pd.Timestamp("2026-04-01") for t in q_ok.values())
                and all(t >= pd.Timestamp("2026-09-25") for t in d_ok.values()))
check("V2 index 0 reads data to September only (decision 43): with every reading after 30 Sep replaced by an impossible "
      "value, and one added, the start the model and the case build (regions_today, the spread already present, the "
      "energy run's headline) is unchanged; each start series is fresh for its publication lag (monthly to August or "
      "September, quarterly to 2026Q2, daily to late September); and the vintage was built before the prints it is scored "
      "on (the FOMC of 28 Oct, the Riksbank of 4 Nov, October employment on 6 Nov; Next 11 as amended). Restated 2026-10-26 "
      "after the review found the first V2 could not fail",
      unmoved and fresh_enough and man["vintage"] < "2026-10-28",
      f"vintage {man['vintage']}; last reads {({k: f'{v:%Y-%m-%d}' for k, v in {**lag_ok, **q_ok, **d_ok}.items()})}")

print("K — the case reproduces, its pieces act as stated, and the findings")
rg_h, o_h = case.build(cm, regs, st, adoption="high")
rd = case.read(rg_h, o_h)
check("K5 the case reproduces from code (its verdict too, since 2026-10-28)", rd["us_out_of_work_peak"] == C["case"]["high"]["us_out_of_work_peak"]
      and rd["four_output_worst"] == C["case"]["high"]["four_output_worst"] and rd["verdict"] == C["case"]["high"]["verdict"],
      f"{rd['us_out_of_work_peak']}, {rd['four_output_worst']}, {rd['verdict']}")
_, o_np = case.build(cm, regs, st, drop="premium")
K12M = int(round(4 * gc.Q / DT))            # month 12, the end of 2027Q3: France's premium in full
fr_extra = float((o_h["FR"]["s"][K12M:] - o_np["FR"]["s"][K12M:]).min())
fr_sov = float((o_h["FR"]["sov"][K12M:] - o_np["FR"]["sov"][K12M:]).min())
ea_moves = float(np.abs(o_h["EA"]["s"] - o_np["EA"]["s"]).max())
care_ok = all(float(o_h[r]["care"].max()) <= st["care_cap"][r] + 1e-9 for r in gc.R)
check("K6 the premium reaches private borrowers: France's government a point more from the end of 2027Q3 (month 12) on, "
      "half of it reaching French firms and households (decision 71; the euro area's half point on all its borrowers before "
      "2026-10-27), none in the rest of the union or the US but through the shared mood (under 0.05; 0.028 found) (Log 44); "
      "and no region's care passes its own ceiling. " + RESTATED + " (from the fourth quarter before). " + RESTATED2 + ", "
      "the bound unchanged: the rest of the union's spread moves 0.020",
      fr_extra >= 0.5 - 1e-9 and fr_sov >= 1.0 - 1e-9 and ea_moves < 0.05 and care_ok,
      f"France's extra private spread {fr_extra:.2f}, its sovereign's +{fr_sov:.2f}; the rest of the union's spread moves "
      f"{ea_moves:.3f} (through the shared mood); care max {({r: round(float(o_h[r]['care'].max()), 2) for r in gc.R})}")

lo, hi, ref = C["case"]["low"], C["case"]["high"], C["reference_central_run"]
po = {e: C["paths"][e]["US"]["out_of_work"] for e in ("low", "high", "reference")}
pq = {e: gc.to_quarters(v, DT) for e, v in po.items()}
ratio = [pq[e][case.END_2028] / pq["reference"][case.END_2028] for e in ("low", "high")]
FOUND.update(us28=[7.7, 8.1, 6.5], ratio=[1.17, 1.24], peak=[22.7, 31.9], us32=[21.6, 29.9], cap_gap=17.4, four=[-14.1, -16.9],
             se_cap=[None, "2032Q1"])
check("K7 through 2028 the case is well defined and a sixth to a quarter above the model's central run (the same measured "
      "bust at the dot-com size, today's rules on their stored dates): US out of work 7.7-8.1% on 2028Q4's average against "
      "6.5% (1.17-1.24 times), the band under 1.5 points wide; by 2032Q3 22.7-31.9% (21.6-29.9% at 2032Q2), still rising at "
      "both ends, the high end 17.4 under the model's 50% cap at the last month; Sweden at the cap from 2032Q1 at the high "
      "end, not at the low (46.5% at its peak). " + RESTATED2 + ": at the first pass 7.4-7.8% (1.15-1.20), 23.2-32.1%, "
      "21.8-29.7%, 17.1 under the cap, Sweden capped from 2032Q1 (low) and 2031Q4 (high). " + RESTATED + ": 8.1-8.5% "
      "against 6.5% (1.25-1.32), 17.4-23.6%, 16.9-22.6%, 26.4 under the cap, no region capped before. Restated 2026-10-27 with France a region of its own (Log 45; decisions "
      "70-71): 8.2-8.6, 17.5-23.8, 17.0-22.8, 26.2 before. Restated 2026-10-26 with the review's fixes (Log 44: the measured "
      "sizes, dated from the peak, the US premium an alternative): in Log 42 8.6-9.1% against 6.5%; on the corrected fit "
      "with the ramp and the stored start 11.0-12.0% against 7.6%; at the tag paths-pre-signfix 14.4-15.7% against 10.1%",
      hi["us_out_of_work_end_2028"] - lo["us_out_of_work_end_2028"] < 1.5
      and [lo["us_out_of_work_end_2028"], hi["us_out_of_work_end_2028"], ref["us_out_of_work_end_2028"]] == FOUND["us28"]
      and [round(x, 2) for x in ratio] == FOUND["ratio"]
      and [lo["us_out_of_work_peak"], hi["us_out_of_work_peak"]] == FOUND["peak"] and lo["still_rising_at_end"] and hi["still_rising_at_end"]
      and [lo["us_out_of_work_2032Q2"], hi["us_out_of_work_2032Q2"]] == FOUND["us32"]
      and lo["us_at_the_models_cap_from"] is None and hi["us_at_the_models_cap_from"] is None
      and round(case.CAP - po["high"][-1], 1) == FOUND["cap_gap"]
      and [lo["regions"]["SE"]["at_the_models_cap_from"], hi["regions"]["SE"]["at_the_models_cap_from"]] == FOUND["se_cap"],
      f"2028Q4 {lo['us_out_of_work_end_2028']}-{hi['us_out_of_work_end_2028']} vs {ref['us_out_of_work_end_2028']} "
      f"(x{ratio[0]:.2f}-{ratio[1]:.2f}); 2032Q3 {lo['us_out_of_work_peak']}-{hi['us_out_of_work_peak']}; "
      f"2032Q2 {lo['us_out_of_work_2032Q2']}-{hi['us_out_of_work_2032Q2']}; capped {({e: {r: C['case'][e]['regions'][r]['at_the_models_cap_from'] for r in gc.R} for e in ('low', 'high')})}")
# the verdict reads the unrounded readings: a run on a line is named by where it is (since 2026-10-28)
on_line = (case.verdict(-19.994, 32.0), case.verdict(-20.0, 32.0), case.verdict(-9.96, 15.0), case.verdict(-6.0, 14.96))
check("K8 both ends are a labour depression (US out of work past 15%, the four economies' output 14.1% and 16.9% below "
      "capacity at worst, more than 10 and short of 20); the verdict reads the unrounded readings (an output 19.994% below "
      "is not a depression, 20.0 is; a peak of 14.96 is not a labour depression). " + RESTATED2 + ": at the first pass "
      "the low end a labour depression (-16.9), the high end a depression on the rounded -20.0 (-19.99 unrounded); the "
      "verdict's reading of the unrounded values, and its test here, set 2026-10-28 after seeing that run. " + RESTATED
      + ": both a labour depression with output held, -6.0 and -6.3. "
      "Restated 2026-10-27 with France a region of its own (Log 45; decisions 70-71): -6.2 and -6.5 before",
      lo["verdict"] == "a labour depression" and hi["verdict"] == "a labour depression"
      and [lo["four_output_worst"], hi["four_output_worst"]] == FOUND["four"]
      and on_line == ("a labour depression", "a depression", "a labour depression, output held", "a 2008-scale recession"),
      f"{lo['verdict']} {lo['four_output_worst']}; {hi['verdict']} {hi['four_output_worst']}; on the lines {on_line}")
pc = {k: v for k, v in C["piece_by_piece"].items() if k != "note"}
late = max(pc, key=lambda k: pc[k]["adds_to_us_out_of_work"])
oow_h = case.out_of_work(o_h)
unr = {}
for p_ in case.PIECES:
    _, o_p = case.build(cm, regs, st, drop=p_)
    unr[p_] = round(float(oow_h[case.END_2028] - case.out_of_work(o_p)[case.END_2028]), 1)
early = sorted(pc, key=lambda k: -pc[k]["adds_to_us_out_of_work_end_2028"])[:2]
check("K9 which piece matters depends on when: by 2028Q4 the bust and the tariffs add most (1.2 and 1.1 points of US out "
      "of work), by 2032Q3 adoption (9.2); the tariffs add 4.0 by 2032Q3; the premium, France's alone, 0.2 to the US. Each "
      "piece is the case minus the run without it, the difference of the unrounded runs' quarterly averages rounded once; "
      "the bust's is its size alone (the run without it keeps the dot-com bust on the same dating). " + RESTATED2 + ": at "
      "the first pass 1.1 and 1.0, adoption 8.9, the tariffs 4.1, the premium 0.3. " + RESTATED + ": the "
      "bust and the tariffs 1.4 each by 2028Q4, adoption 6.2, the tariffs 3.7, the premium 0.0 (Restated 2026-10-27 with "
      "France a region of its own (Log 45; decisions 70-71): adoption 6.3, the euro area's premium 0.2, before). Restated "
      "2026-10-26 with the review's fixes (Log 44: the measured sizes, dated from the peak, the US premium an alternative): "
      "in Log 42 the premium 1.4, the tariffs 1.2, the bust 1.1 by 2028Q4, adoption 7.4",
      set(early) == {"bust", "tariffs"} and late == "adoption"
      and [pc[k]["adds_to_us_out_of_work_end_2028"] for k in ("bust", "tariffs")] == [1.2, 1.1]
      and pc["adoption"]["adds_to_us_out_of_work"] == 9.2 and pc["tariffs"]["adds_to_us_out_of_work"] == 4.0
      and pc["premium"]["adds_to_us_out_of_work"] == 0.2
      and all(unr[k] == pc[k]["adds_to_us_out_of_work_end_2028"] for k in case.PIECES),
      {k: (v["adds_to_us_out_of_work_end_2028"], v["adds_to_us_out_of_work_2032Q2"], v["adds_to_us_out_of_work"]) for k, v in pc.items()})
aus = pc["austerity"]
check("K10 the case's rising pace is milder than the model's central assumption (the paper's pace from today): taking it back "
      "adds to US out of work, 1.4 points at 2028Q4, 3.6 by 2032Q2 and 3.8 by 2032Q3; care capping out adds under a point to "
      "the US and under two to the euro area outside France, France and Sweden; Europe's and Sweden's cuts add 2.1 to the "
      "US's peak, 8.3 to the rest of the union's, 8.2 to France's and 5.4 to Sweden's (44.6% without them, at the cap with "
      "them); no US run reaches the model's 50% cap. " + RESTATED2 + ": at the first pass the pace 1.4, 3.9 and 4.2; the "
      "cuts 2.7, 10.4, 11.2 and 0.5 (Sweden at the cap with or without them). " + RESTATED + ": the pace 1.2, 2.6 and "
      "2.7; austerity under a point to the US and under two to the others",
      (pc["pace"]["adds_to_us_out_of_work_end_2028"], pc["pace"]["adds_to_us_out_of_work_2032Q2"], pc["pace"]["adds_to_us_out_of_work"]) == (-1.4, -3.6, -3.8)
      and all(pc[k]["us_at_the_models_cap_from"] is None for k in case.PIECES)
      and pc["care"]["adds_to_us_out_of_work"] < 1 and all(pc["care"][f"adds_to_{r}_out_of_work"] < 2 for r in ("ea", "fr", "se"))
      and (aus["adds_to_us_out_of_work"], aus["adds_to_ea_out_of_work"], aus["adds_to_fr_out_of_work"], aus["adds_to_se_out_of_work"]) == (2.1, 8.3, 8.2, 5.4)
      and aus["se_out_of_work_peak"] == 44.6,
      {k: pc[k] for k in ("pace", "austerity", "care")})
sv = {k: v for k, v in C["sensitivities"].items() if k != "note"}
anchor = sv["fiscal dominance: the US anchor loosens to the eroding rules' 0.6"]
rate = sv["rates bite harder: a_r 0.079 (Holston-Laubach-Williams, US)"]
nodd = sv["no debt deflation: the fit's 0.5 (at its bound) set to 0"]
moved = {k: (v["change_in_us_out_of_work"], v["change_in_us_out_of_work_2032Q2"]) for k, v in sv.items()}
FOUND.update(sens={"fiscal dominance: the US anchor loosens to the eroding rules' 0.6": (1.8, 1.5),
                   "fiscal dominance: the US anchor loosens to 0.6 and the Fed tolerates 3% inflation": (1.4, 1.2),
                   "Germany's spending offsets the periphery's cuts: the euro area neither stimulates nor cuts": (-1.0, -0.9),
                   "the euro area stimulates": (-2.0, -1.8),
                   "the US exit share at decision 21's proposal (0.36)": (-0.8, -0.7),
                   "rates bite harder: a_r 0.079 (Holston-Laubach-Williams, US)": (-5.5, -5.0),
                   "no debt deflation: the fit's 0.5 (at its bound) set to 0": (-9.4, -8.4)})
check("K11 of the settings the case leaves out, debt deflation and the rate channel move US out of work most: with the fit's "
      "debt deflation off it is 9.4 points lower at the peak (8.4 at 2032Q2); with a_r at the Holston-Laubach-Williams "
      "estimate (0.079, against the fit's bound of 0.03) 5.5 lower (5.0); the euro area stimulating takes 2.0 off (1.8), a "
      "looser US anchor adds 1.8 (1.5) and lowers US inflation's low (-2.4% against -0.8%) rather than raising inflation; "
      "Germany's spending and the exit share move it under 1.5; no run reaches the model's cap. The differences of the "
      "unrounded runs' quarterly averages, rounded once (since the review of 2026-10-26). " + RESTATED2 + ": at the first "
      "pass debt deflation 11.0 (9.5), the rate channel 5.8 (5.1), the euro area stimulating 2.5 (2.2), the anchor 2.8 (2.3) "
      "and with the 3% target 2.8 (2.2), Germany 1.2 (1.1), the anchor's low -3.1% against -1.2%. " + RESTATED + ": only "
      "the rate channel moved it more than 1.5 points, 3.2 and 2.9 (3.3 and 3.0 before Log 45); the anchor's low -0.3% "
      "against 0.5%; the non-employment trigger sensitivity is gone with the triggers, the debt-deflation one new",
      moved == FOUND["sens"] and all(v["us_at_the_models_cap_from"] is None for v in sv.values())
      and (anchor["us_inflation_min"], hi["regions"]["US"]["inflation_min"]) == (-2.4, -0.8)
      and anchor["us_inflation_max"] - hi["regions"]["US"]["inflation_max"] < 0.5,
      moved)

print("A — the alternatives and what the watcher would see")
al = {k: v for k, v in C["alternatives"].items() if k != "note"}
octo = al["the 8 Oct case's timing: equity and the build-out at full size within two quarters from 2026Q4 and held, the losses over 2027"]
prem = al["deficit worry priced in the US: a point more on US borrowing over the first year (her leaning; the 8 Oct case's setting)"]
check("A1 on 2026Q4's average the case has US unemployment at 4.34% (4.36% out of work), above the 4.2 that claims to 17 "
      "Oct point to (Log 40) but well short of the 8 Oct timing's 4.96%; the 8 Oct timing also puts US out of work 3.9 "
      "points higher at 2028Q4. Her deficit-worry premium, an alternative, would add 1.4 points at 2028Q4 and 5.3 by "
      "2032Q2. " + RESTATED2 + ": at the first pass 4.33% (4.36%), the 8 Oct timing 4.91% and +3.6, the premium +1.3 "
      "and +5.9. " + RESTATED + ": 4.49% (4.53%) at the quarter's end, the 8 Oct timing 5.60% and +2.8, the premium +1.2 "
      "and +3.8",
      (hi["us_unemployment_2026Q4"], hi["us_out_of_work_2026Q4"]) == (4.34, 4.36) and octo["us_unemployment_2026Q4"] == 4.96
      and octo["change_in_us_out_of_work_end_2028"] == 3.9
      and (prem["change_in_us_out_of_work_end_2028"], prem["change_in_us_out_of_work_2032Q2"]) == (1.4, 5.3),
      f"case {hi['us_unemployment_2026Q4']} ({hi['us_out_of_work_2026Q4']}); 8 Oct timing {octo['us_unemployment_2026Q4']}; "
      f"premium +{prem['change_in_us_out_of_work_end_2028']} / +{prem['change_in_us_out_of_work_2032Q2']}")
en = al["oil stays high and policy reads four quarters' headline (decision 27's run)"]
no_oil = all(not np.any(o_h[r]["d_energy"]) and not np.any(o_h[r]["e_pi"]) for r in gc.R)
check("A2 decision 27: the case's own runs carry no energy term, and its run is an alternative; its price leg is met on the "
      "vintage (dated Brent's last five prints 121.25 against 1.25 times its three-year average, 100.89), its bust leg is "
      "not: the Nasdaq is 6.0% under its 52-week high against the rule's 20%; in that run the Fed's 2026Q4 average is 4.14 "
      "against the case's 3.87, and US out of work 0.5 higher at 2028Q4. " + RESTATED2 + ": +0.4 at the first pass, the "
      "rates the same. " + RESTATED + ": 4.21 against 4.02, +0.0",
      no_oil and obs["brent_last5"] >= 1.25 * obs["brent_three_year_average"] and obs["nasdaq_off_its_high_pct"] > -20
      and (en["us_policy_rate_2026Q4"], hi["regions"]["US"]["policy_rate_2026Q4"]) == (4.14, 3.87)
      and en["change_in_us_out_of_work_end_2028"] == 0.5,
      f"Brent {obs['brent_last5']} vs {1.25 * obs['brent_three_year_average']:.2f}; Nasdaq {obs['nasdaq_off_its_high_pct']}%; "
      f"rates {en['us_policy_rate_2026Q4']} / {hi['regions']['US']['policy_rate_2026Q4']}")
sg = C["signals"]
rate_m = C["paths"]["high"]["US"]["rate"]
se_m = C["paths"]["high"]["SE"]["rate"]
check("A3 what the watcher would see at the high end: the Nasdaq rule (20% under its high) by 30 Oct 2026 on the 2000 Nasdaq's "
      "own daily path at the case's size (24 days after the high; at the dot-com size 33 days, 8 Nov), the late bounds by "
      "month January 2027 (the 2000-02 ratio) and July 2027 (one for one); the US Sahm rule, as the watcher reads it on "
      "the model's months after the measured ones, in February 2027; the model's spread, fitted to Baa over Aaa (decision "
      "90), never rises 0.56 in three months; the Fed raises in October (3.96 against 3.88; a new registration beside Log 40's FOMC test) and "
      "cuts by December (3.78; 3.87 on 2026Q4's average), the Riksbank cuts (1.63 in October, 1.66 in November, against "
      "1.75). " + RESTATED + ": 2027Q1 and 2027Q3 by quarter, the Sahm rule 2027Q1 on quarters, the Baa rule unmeasured, "
      "the Fed 4.02 and the Riksbank 1.63 at the end of 2026Q4; the same on the refit (decision 92), after seeing its run. "
      "Restated 2026-10-26 after the review found the quarterly Nasdaq date read from the wrong base",
      sg["bust.us.equity, on the 2000 Nasdaq's daily path"]["dates_from_the_2026_high"] == ["2026-10-30", "2026-11-08"]
      and sg["bust.us.equity, by month, the 2000-02 ratio (a late bound)"] == "2027-01"
      and sg["bust.us.equity, by month, one for one (a late bound)"] == "2027-07"
      and sg["labour.us.sahm"] == "2027-02" and sg["bust.credit.baa (the model's spread, fitted to Baa over Aaa)"] is None
      and rate_m[1] == 3.96 > regs["US"].i0 and hi["regions"]["US"]["policy_rate_2026Q4"] == 3.87 and rate_m[3] < regs["US"].i0
      and max(se_m[1:3]) < regs["SE"].i0 and hi["regions"]["SE"]["policy_rate_2026Q4"] < regs["SE"].i0,
      {**{k: v for k, v in sg.items() if not k.startswith("nasdaq")}, "US rate Oct-Dec": rate_m[1:4], "SE rate Oct-Dec": se_m[1:4]})

print("K — one dating, the horizon, the levers, debt deflation")
_, o70 = case.build(cm, regs, st, adoption="high", n=N70)
same70 = all(np.array_equal(o70[r][k], o_h[r][k][:N70], equal_nan=True) for r in gc.R for k in o70[r])
D = C["dates"]
check("K12 one dating (decisions 43 and 91): at the model's monthly step (gc.DT = 1/12) gc.month_label names index 0 2026-09 "
      "(the end of the state measured to September 2026), index 1 2026-10 and the last (72) 2032-09; gc.quarter_label takes "
      "no second dating and names the quarterly readings' index 0 2026Q3, 1 — the quarter of the peak, where the bust "
      "begins — 2026Q4, END_2028 (9) 2028Q4 and 24 2032Q3, a 73-month run reading as 25 quarters; the dates: the bust from "
      "the 6 Oct 2026 peak (equity falling from 2026Q4, its trough quarter 2029Q2, the losses heaviest in 2029Q1, the "
      "build-out above its start through 2027Q3), the tariffs 2027Q1, the premium over 2026Q4-2027Q3, the pace half-way in "
      "2028Q2, robotics from 2028Q4, the levers from 2027-08 (US), 2028-02 (the rest of the union), 2027-12 (France), "
      "2027-10 (Sweden), 2030-03 (China); extending the case from 70 to 73 months changes nothing before it (the comparison "
      "with 27dd785 is the record's, at the tag paths-pre-signfix). " + RESTATED2 + ": the losses heaviest in 2029Q2 at the "
      "first pass, two months late; the rest the same. " + RESTATED + ": 25 quarters; the trough 2029Q3 and "
      "the losses 2029Q1 at the quarterly step, the levers on triggers",
      list(inspect.signature(gc.quarter_label).parameters) == ["k"] and not hasattr(gc, "MEASURED") and DT == 1 / 12
      and [gc.month_label(k) for k in (0, 1, case.N - 1)] == ["2026-09", "2026-10", "2032-09"]
      and [gc.quarter_label(k) for k in (0, 1, case.END_2028, case.NQ - 1)] == ["2026Q3", "2026Q4", "2028Q4", "2032Q3"]
      and len(gc.to_quarters(np.zeros(case.N), DT)) == case.NQ == 25
      and C["start"] == gc.START == "2026Q3" and (C["step"], C["steps"], C["quarters"]) == ("month", 73, 25)
      and D == {"bust_onset": "2026Q4", "peak": "2026-10-06", "peak_shift_quarters": 0.712, "equity_first_falls": "2026Q4",
                "equity_trough": "2029Q2", "losses_peak": "2029Q1", "build_out_last_above_its_start": "2027Q3", "tariffs": "2027Q1",
                "premium_builds": "2026Q4-2027Q3", "pace_half_way": "2028Q2", "robotics_begins": "2028Q4",
                "levers_from": {"US": "2027-08", "EA": "2028-02", "FR": "2027-12", "SE": "2027-10", "CN": "2030-03"}} and same70,
      D)

lv = st["levers"]
again = json.loads(json.dumps(case.lever_dates(cm, regs, st))) == lv
first_rise = True                          # each end's dates: where its unemployment first rose the trigger, on its own run
for e in ("low", "high"):
    _, o_e = case.build(cm, regs, st, adoption=e, sens={"levers": e})
    for r in gc.R:
        k0 = round(lv[e][r]["years"] / DT) + 1
        rise = o_e[r]["u"] - regs[r].u0
        first_rise &= bool(rise[k0 - 1] >= lv["trigger"] and rise[:k0 - 1].max() < lv["trigger"])
mid_ok = all(abs(lv["case"][r]["years"] - np.floor((lv["low"][r]["years"] + lv["high"][r]["years"]) / 2 / DT + 0.5) * DT) < 1e-12
             for r in gc.R)
on_dates = True                            # no lever before its month, the lever from it, in the case and in a piece
_, o_aus = case.build(cm, regs, st, drop="austerity")
for o_x in (o_h, o_aus):
    for r in gc.R:
        k0 = round(lv["case"][r]["years"] / DT) + 1
        on_dates &= bool(not np.any(o_x[r]["stim"][:k0]) and o_x[r]["stim"][k0] != 0)
no_trigger = ("trigger_on" not in {f.name for f in fields(gc.Rules)}
              and not any("trigger" in k for k in C["sensitivities"]))
check("K13 the levers are dated (decisions 81 and 91): each region's fiscal lever starts the month after its unemployment "
      "first reads two points above its start in the case's own runs (gc.trigger_dates on the low end and on the high end, each "
      "reproduced here and checked on its own run), the case's the midpoint of the two to the month: the US's stimulus from "
      "2027-08, Sweden's cuts from 2027-10, France's from 2027-12, the rest of the union's from 2028-02, China's stimulus "
      "from 2030-03 (2030-03 at the low end, 2030-02 at the high); no lever before its month, in the case and in a piece "
      "(Europe's cuts taken back to stimulus on the same dates); the model has no trigger, and the non-employment trigger "
      "sensitivity is gone. Stated as found 2026-10-28 after seeing the run (new with decision 91; the triggers before); "
      "every date the same on the refit (decision 92), after seeing its run",
      again and first_rise and mid_ok and on_dates and no_trigger
      and {r: (lv["low"][r]["from"], lv["high"][r]["from"], lv["case"][r]["from"]) for r in gc.R}
      == {"US": ("2027-08",) * 3, "EA": ("2028-02",) * 3, "FR": ("2027-12",) * 3, "SE": ("2027-10",) * 3,
          "CN": ("2030-03", "2030-02", "2030-03")},
      {r: (lv["low"][r]["from"], lv["high"][r]["from"], lv["case"][r]["from"]) for r in gc.R})

drag = {r: hi["regions"][r]["debt_deflation_drag_max_pct_gdp"] for r in gc.R}
# the levelled form's largest drag, % of GDP: the slope times private debt times the shortfall it levels off at
ceiling = {r: cm.debt_deflation * regs[r].priv_debt / 100 * cm.dd_sat * 100 for r in gc.R}
monthly = {r: max(0.0, -float(o_h[r]["d_debt"].min())) for r in gc.R}
check("K14 the fit's debt deflation (slope 0.5, at its bound, levelling off at a shortfall of 11.4%: decision 92) acts in "
      "the case wherever the price level runs below the path expected at the region's target (decision 91): its largest "
      "drag on demand at the high end, on the quarters' averages, is 3.79% of GDP in the US, 4.04 in the rest of the union, "
      "6.72 in France, 10.22 in Sweden and 4.44 in China, each under its levelled form's ceiling (the slope times its "
      "private debt times 11.4%: 8.0, 8.0, 12.2, 13.1, 11.5) by month too; with it off the high end's US peak is 22.5% (9.4 "
      "lower), the four economies' output 7.5% below capacity at worst (against 16.9), Sweden's out of work 31.3% (against "
      "the cap). Stated as found 2026-10-28 after seeing the run (new: the stored quarterly fit's debt deflation was 0, so "
      "before the restatement it did not act in the case). " + RESTATED2 + ", the ceiling new and set after seeing it: at "
      "the first pass, on the linear form, 5.25, 6.06, 10.74, 23.32 and 6.0; with it off 21.1, -7.2 and 30.3",
      drag == {"US": 3.79, "EA": 4.04, "FR": 6.72, "SE": 10.22, "CN": 4.44}
      and all(monthly[r] <= ceiling[r] for r in gc.R)
      and (nodd["us_out_of_work_peak"], nodd["four_output_worst"], nodd["se_out_of_work_peak"]) == (22.5, -7.5, 31.3)
      and cm.debt_deflation == 0.5 and cm.dd_sat == G["common"]["dd_sat"] and abs(cm.dd_sat - 0.1143) < 5e-5,
      {"drag": drag, "by month": {r: round(v, 2) for r, v in monthly.items()}, "ceiling": {r: round(v, 2) for r, v in ceiling.items()},
       "off": (nodd["us_out_of_work_peak"], nodd["four_output_worst"], nodd["se_out_of_work_peak"])})

n_ok = sum(ok for _, ok, _ in RESULTS)
print(f"\n{n_ok}/{len(RESULTS)} checks passed")
print(f"ALL GREEN ({len(RESULTS)})" if n_ok == len(RESULTS) else "FAILURES: " + "; ".join(n.split(" ")[0] for n, ok, _ in RESULTS if not ok))
sys.exit(0 if n_ok == len(RESULTS) else 1)
