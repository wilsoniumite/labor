# check_case.py — her case (code/case.py): the model's additions change nothing when off, the settings trace to their
# sources, the start is the dated vintage, the bust is the 2000-02 bust's measured path from the quarter of today's peak,
# the dating is one and the 25-quarter horizon changes nothing before it, and the findings, stated as found.
#
# Rebuilt 2026-10-26 with the case (STATE Log 42): the case runs on the start's dated vintage (vintage.py, cache/start/)
# and its bust on the 2000-02 bust's measured path (global_crash.bust_2000), at her 1.5x size, from 2026Q4 (the quarter
# of the Nasdaq's and the S&P's high, 6 Oct). The findings below are stated as found on that day (FOUND), every number in
# one place; the bust as first built (ai_shock's ramps, held) is gated to reproduce exactly (K1), and the 8 Oct case it
# carried reproduces at the tag paths-pre-signfix. K4 and V1-V2 are new; K7-K11 restate the case's findings.
#
# Run from paths/:  ../venv/Scripts/python.exe checks/check_case.py
# Exit status 0 only if every check passes.

from __future__ import annotations

import hashlib
import inspect
import json
import os
import sys

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

# the findings as found on 2026-10-26 (high end unless stated; US out of work = unemployed + left the workforce, %)
FOUND = {}


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


C = json.load(open(os.path.join(ROOT, "results", "case.json"), encoding="utf-8"))
G = json.load(open(os.path.join(ROOT, "results", "global_crash.json"), encoding="utf-8"))
P = json.load(open(os.path.join(ROOT, "results", "pace.json"), encoding="utf-8"))
cm, regs = case.stored()
st = C["settings"]

print("K — the model's additions, the settings, the bust")
rg, o = case.reference(cm, regs, 24)       # global_crash's stored runs are 24 quarters (K12: the 25th changes none of them)
key = "modern rules | bust + displacement | two waves, robotics in 2 years, care absorbs"
same = json.loads(json.dumps({"year4": gc.summary(o, rg, 16), "year6": gc.summary(o, rg)})) == G["scenarios"][key]
a, b = gc.ai_shock(24), gc.ai_shock(24, 1.0, 1.0)
shock_same = all(np.array_equal(getattr(a, f)[r], getattr(b, f)[r]) for f in ("equity", "capex", "losses") for r in gc.R)
rp = gc.ai_shock(24, shape="ramp")
ramp_same = (np.allclose(rp.equity["US"][:6], [0, 0.1, 0.2, 0.3, 0.4, 0.4]) and np.allclose(rp.capex["US"][:6], [0, 0.15, 0.3, 0.45, 0.6, 0.6])
             and np.allclose(rp.losses["US"][:11], [0, 0, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0]))
check("K1 the model's central run reproduces its stored scenario exactly, its default bust is ai_shock's own, and the bust "
      "as first built (shape='ramp': straight-line falls over four quarters, held; the losses evenly over eight) is kept "
      "exactly", same and shock_same and ramp_same, key)

seen = P["paces"]["multiples_of_the_papers"]["trend + 2 s.e."]
cap_ok = all(abs(st["care_cap"][r] - (regs[r].care_share + regs[r].care_trend)) < 0.006 for r in gc.R)
tar_ok = st["tariff"]["US"] == 25.0 and all(abs(st["tariff"][r] - 25.0 * regs[r].trade.get("US", 0.0)) < 0.006 for r in ("EA", "SE", "CN"))
ig = vintage.read("BAMLC0A0CM").loc[:case.INDEX0_END]
s0_ok = abs(st["spread0"]["US"] - round(float(ig.iloc[-1] - ig.iloc[-64]), 4)) < 1e-9 and ig.index[-1] <= pd.Timestamp(case.INDEX0_END)
check("K2 the settings trace to their sources: the starting pace is pace.py's upper bound on what has been seen; each care "
      "ceiling is today's share plus one year of its trend; the tariff each region's exports face is 25 points times its "
      "export share to the US (the US: 25); the spread already present at the start is the US corporate OAS's rise over "
      "the 63 prints to 30 Sep (decision 47; index 0 is measured on data to September)",
      st["pace"]["seen"] == seen and cap_ok and tar_ok and s0_ok,
      f"seen {st['pace']['seen']}; caps {st['care_cap']}; tariffs {st['tariff']}; spread0 {st['spread0']} (to {ig.index[-1]:%Y-%m-%d})")
lp = case.logistic_pace(1.0, seen, st["pace"]["mid_quarter"], st["pace"]["width_quarters"])
half = (lp[st["pace"]["mid_quarter"]] - seen) / (1 - seen)
check("K3 the pace starts at the upper bound seen, rises monotonically, is half-way at 2028Q2 (index 7) and within 5% of the "
      "paper's pace by the last quarter (2032Q3)", abs(lp[0] - seen) < 1e-9 and np.all(np.diff(lp) > 0) and abs(half - 0.5) < 0.05
      and lp[-1] > 0.95 and len(lp) == case.N == 25 and gc.quarter_label(st["pace"]["mid_quarter"]) == "2028Q2",
      f"start {lp[0]:.3f}, {gc.quarter_label(7)} {lp[7]:.3f} (half-way {half:.2f}), {gc.quarter_label(len(lp) - 1)} {lp[-1]:.3f}")

bp = gc.bust_2000()
stored_bp = C["bust_path"]["from_the_2000_02_bust"]
bp_same = all(np.allclose(np.round(bp[k], 4), stored_bp[k], atol=1e-9) for k in ("equity", "capex", "losses"))
bs = case.bust_shock(case.N, st["bust"])
eq_us = bs.equity["US"]
k_tr = int(np.argmax(eq_us))
obs = C["vintage"]["observed"]
hi_q = gc.quarter_label(st["bust"]["onset"]) == str(pd.Period(obs["nasdaq_high"][0], "Q"))
check("K4 the bust is the 2000-02 bust's measured path (recomputed from the cache: Z.1 household equity, BEA's build-out "
      "above its 1990-94 trend, the Fed Board's C&I charge-offs) at 1.5 times its size, from the quarter of today's peak: "
      "US household equity 0.60 down at its trough, ten quarters after the onset; the losses 2.25% of US loans in all; at "
      "index 1 (2026Q4) equity has not yet fallen, as the data so far say (the Nasdaq's 2026Q4 average to date within 5% "
      "of its 2026Q3 average); the onset is the quarter of the Nasdaq's 52-week high",
      bp_same and abs(eq_us.max() - 0.60) < 1e-9 and k_tr - st["bust"]["onset"] == 10 and eq_us[1] == 0.0
      and abs(float((bs.losses["US"] * gc.DT).sum()) - 2.25) < 1e-9 and abs(obs["nasdaq_q4_to_date_vs_q3_avg_pct"]) < 5 and hi_q,
      f"trough {eq_us.max():.2f} at {gc.quarter_label(k_tr)}; losses {float((bs.losses['US'] * gc.DT).sum()):.2f}; index-1 equity "
      f"{eq_us[1]}; Nasdaq Q4 to date vs Q3 {obs['nasdaq_q4_to_date_vs_q3_avg_pct']:+.2f}%, high {obs['nasdaq_high']}")

print("V — the start is the dated vintage")
man = vintage.manifest()
hashes = all(hashlib.sha256(open(os.path.join(vintage.START, f"{sid}.csv"), encoding="utf-8").read().encode()).hexdigest() == v["sha256"]
             for sid, v in man["series"].items())
fresh = gc.regions_today()
fresh.pop("_notes")
fields = ("u0", "i0", "pi0", "equity_wealth", "ai_capex", "hh_debt", "priv_debt")
start_same = all(abs(getattr(fresh[r], f) - G["regions"][r][f]) < 1e-12 for r in gc.R for f in fields)
check("V1 the start is the vintage: every file in cache/start/ has the hash its manifest records, and the stored regions "
      "(global_crash.json, which the case and the website's model read) are regions_today() on it",
      hashes and start_same, {r: {f: round(G["regions"][r][f], 3) for f in ("u0", "i0", "pi0", "equity_wealth", "ai_capex")} for r in ("US", "EA", "SE")})
end = pd.Period(gc.START, "Q").end_time
reads = {sid: vintage.read(sid).loc[:end].index[-1] for sid in ("UNRATE", "DFF", "PCEPILFE", "ECBDFR", "00XEFDEZ19M086NEST",
                                                                 "00XEFDSEM086NEST", "EA_UNEMPLOYMENT", "SEUNRATE", "SECBREPOEFF")}
check("V2 index 0 reads data to September only (decision 43), and the vintage was built before the prints it is scored on "
      "(the FOMC of 28 Oct, the Riksbank of 4 Nov, October employment on 6 Nov; Next 11 as amended)",
      all(t <= end for t in reads.values()) and man["vintage"] < "2026-10-28",
      f"vintage {man['vintage']}; last reads {({k: f'{v:%Y-%m-%d}' for k, v in reads.items()})}")

print("K — the case reproduces, its pieces act as stated, and the findings")
rg_h, o_h = case.build(cm, regs, st, adoption="high")
rd = case.read(rg_h, o_h)
check("K5 the case reproduces from code", rd["us_out_of_work_peak"] == C["case"]["high"]["us_out_of_work_peak"]
      and rd["four_output_worst"] == C["case"]["high"]["four_output_worst"], f"{rd['us_out_of_work_peak']}, {rd['four_output_worst']}")
_, o_np = case.build(cm, regs, st, drop="premium")
extra = o_h["US"]["s"][4:] - o_np["US"]["s"][4:]
care_ok = all(float(o_h[r]["care"].max()) <= st["care_cap"][r] + 1e-9 for r in gc.R)
check("K6 the premium reaches private borrowers (US spreads at least a point higher from the fourth quarter on) and no "
      "region's care passes its own ceiling", float(extra.min()) >= 1.0 - 1e-9 and care_ok,
      f"US extra spread {extra.min():.2f}..{extra.max():.2f}; care max {({r: round(float(o_h[r]['care'].max()), 2) for r in gc.R})}")

lo, hi, ref = C["case"]["low"], C["case"]["high"], C["reference_central_run"]
po = {e: C["paths"][e]["US"]["out_of_work"] for e in ("low", "high", "reference")}
ratio = [po[e][case.END_2028] / po["reference"][case.END_2028] for e in ("low", "high")]
FOUND.update(us28=[8.6, 9.1, 6.5], ratio=[1.31, 1.39], peak=[19.5, 26.9], us32=[19.0, 25.7], cap_gap=23.1, four=[-7.0, -7.7])
check("K7 through 2028 the case is well defined and about a third above the model's central run (which now carries the same "
      "measured bust at the dot-com size): US out of work 8.6-9.1% at 2028Q4 against 6.5% (1.31-1.39 times), the band under "
      "1.5 points wide; by 2032Q3 19.5-26.9% (19.0-25.7% at 2032Q2), still rising at both ends, the high end 23.1 under the "
      "model's 50% cap. Restated 2026-10-26 with the case (Log 42): on the corrected fit with the ramp and the stored start "
      "11.0-12.0% against 7.6%; at the tag paths-pre-signfix 14.4-15.7% against 10.1%",
      hi["us_out_of_work_end_2028"] - lo["us_out_of_work_end_2028"] < 1.5
      and [lo["us_out_of_work_end_2028"], hi["us_out_of_work_end_2028"], ref["us_out_of_work_end_2028"]] == FOUND["us28"]
      and [round(x, 2) for x in ratio] == FOUND["ratio"]
      and [lo["us_out_of_work_peak"], hi["us_out_of_work_peak"]] == FOUND["peak"] and lo["still_rising_at_end"] and hi["still_rising_at_end"]
      and [lo["us_out_of_work_2032Q2"], hi["us_out_of_work_2032Q2"]] == FOUND["us32"]
      and lo["us_at_the_models_cap_from"] is None and hi["us_at_the_models_cap_from"] is None
      and round(case.CAP - po["high"][-1], 1) == FOUND["cap_gap"],
      f"2028Q4 {lo['us_out_of_work_end_2028']}-{hi['us_out_of_work_end_2028']} vs {ref['us_out_of_work_end_2028']} "
      f"(x{ratio[0]:.2f}-{ratio[1]:.2f}); 2032Q3 {lo['us_out_of_work_peak']}-{hi['us_out_of_work_peak']}; "
      f"2032Q2 {lo['us_out_of_work_2032Q2']}-{hi['us_out_of_work_2032Q2']}")
check("K8 both ends are a labour depression with output held: US out of work past 15% while the four economies' output stays "
      "within 10% of capacity at worst (-7.0 and -7.7)", lo["verdict"] == hi["verdict"] == "a labour depression, output held"
      and [lo["four_output_worst"], hi["four_output_worst"]] == FOUND["four"],
      f"{lo['verdict']} {lo['four_output_worst']}; {hi['verdict']} {hi['four_output_worst']}")
pc = {k: v for k, v in C["piece_by_piece"].items() if k != "note"}
late = max(pc, key=lambda k: pc[k]["adds_to_us_out_of_work"])
oow_h = o_h["US"]["u"] + o_h["US"]["out"]
unr = {}
for p_ in case.PIECES:
    _, o_p = case.build(cm, regs, st, drop=p_)
    unr[p_] = round(float(oow_h[case.END_2028] - (o_p["US"]["u"] + o_p["US"]["out"])[case.END_2028]), 1)
early = sorted(pc, key=lambda k: -pc[k]["adds_to_us_out_of_work_end_2028"])[:3]
check("K9 which piece matters depends on when: by 2028Q4 no single piece dominates (the premium 1.4, the tariffs 1.2, the "
      "bust 1.1 points of US out of work), by 2032Q3 adoption (7.4); the premium and the tariffs each add about 4 points by "
      "2032Q3 (4.0 and 3.9). Each piece is the case minus the run without it, the difference of the unrounded runs rounded "
      "once (since 2026-10-26; before, the difference of rounded values). Restated 2026-10-26 with the case (Log 42): "
      "before it the bust added most by 2028Q4 (2.5; at the tag 2.8) on the ramp",
      set(early) == {"premium", "tariffs", "bust"} and late == "adoption"
      and [pc[k]["adds_to_us_out_of_work_end_2028"] for k in ("premium", "tariffs", "bust")] == [1.4, 1.2, 1.1]
      and pc["adoption"]["adds_to_us_out_of_work"] == 7.4
      and (pc["premium"]["adds_to_us_out_of_work"], pc["tariffs"]["adds_to_us_out_of_work"]) == (4.0, 3.9)
      and all(unr[k] == pc[k]["adds_to_us_out_of_work_end_2028"] for k in case.PIECES),
      {k: (v["adds_to_us_out_of_work_end_2028"], v["adds_to_us_out_of_work_2032Q2"], v["adds_to_us_out_of_work"]) for k, v in pc.items()})
check("K10 the case's rising pace is milder than the model's central assumption (the paper's pace from today): taking it back "
      "adds to US out of work, 1.3 points at 2028Q4 and 2.5 by 2032Q2 and 2032Q3; austerity and care capping out each add "
      "under a point to the US, and under two points to the euro area and Sweden; no run reaches the model's 50% cap",
      (pc["pace"]["adds_to_us_out_of_work_end_2028"], pc["pace"]["adds_to_us_out_of_work_2032Q2"], pc["pace"]["adds_to_us_out_of_work"]) == (-1.3, -2.5, -2.5)
      and all(pc[k]["us_at_the_models_cap_from"] is None for k in case.PIECES)
      and all(pc[k]["adds_to_us_out_of_work"] < 1 for k in ("austerity", "care"))
      and all(pc[k][f"adds_to_{r}_out_of_work"] < 2 for k in ("austerity", "care") for r in ("ea", "se")),
      {k: pc[k] for k in ("pace", "austerity", "care")})
sv = {k: v for k, v in C["sensitivities"].items() if k != "note"}
anchor = sv["fiscal dominance: the US anchor loosens to the eroding rules' 0.6"]
rate = sv["rates bite harder: a_r 0.079 (Holston-Laubach-Williams, US)"]
check("K11 of the settings the case leaves out, only a stronger rate channel moves US out of work by more than 1.5 points: "
      "a_r at the Holston-Laubach-Williams estimate (0.079, against the fit's bound of 0.03) takes 3.7 off the peak and 3.4 "
      "off 2032Q2; a looser US anchor lowers US inflation's low (-0.9% against 0.2%) rather than raising inflation; no run "
      "reaches the model's cap. Restated 2026-10-26 with the case (Log 42; the a_r row new)",
      all(abs(v["change_in_us_out_of_work"]) <= 1.5 and abs(v["change_in_us_out_of_work_2032Q2"]) <= 1.5 for v in sv.values() if v is not rate)
      and (rate["change_in_us_out_of_work"], rate["change_in_us_out_of_work_2032Q2"]) == (-3.7, -3.4)
      and all(v["us_at_the_models_cap_from"] is None for v in sv.values())
      and (anchor["us_inflation_min"], hi["regions"]["US"]["inflation_min"]) == (-0.9, 0.2)
      and anchor["us_inflation_max"] - hi["regions"]["US"]["inflation_max"] < 0.5,
      {k: (v["change_in_us_out_of_work_2032Q2"], v["change_in_us_out_of_work"]) for k, v in sv.items()})

print("A — the alternatives and what the watcher would see")
al = {k: v for k, v in C["alternatives"].items() if k != "note"}
octo = al["the 8 Oct case's timing: all three legs at full size within two quarters from 2026Q4, held"]
check("A1 the data so far pick the measured path over the 8 Oct case's timing: in 2026Q4 the case has US out of work at 4.32% "
      "(claims to 17 Oct put October's unemployment near 4.2, STATE Log 40), the 8 Oct timing at 5.64% (and 12.8% at "
      "2028Q4, 3.7 above the case)",
      po["high"][1] == 4.32 and octo["us_out_of_work_2026Q4"] == 5.64 and octo["change_in_us_out_of_work_end_2028"] == 3.7,
      f"case {po['high'][1]}; 8 Oct timing {octo['us_out_of_work_2026Q4']} ({octo['us_out_of_work_end_2028']} at 2028Q4)")
en = al["oil stays high and policy reads four quarters' headline (decision 27's run)"]
bs_case = case.bust_shock(case.N, st["bust"])
check("A2 decision 27: the energy term is off in the case (its runs carry no oil) and its run is an alternative; its price leg "
      "is met on the vintage (dated Brent's last five prints 121.25 against 1.25 times its three-year average, 100.89), its "
      "bust leg is not (no bust rule active); in that run the Fed's 2026Q4 rate is 4.21 against the case's 4.02",
      not bs_case.oil and obs["brent_last5"] >= 1.25 * obs["brent_three_year_average"]
      and (en["us_policy_rate_2026Q4"], hi["regions"]["US"]["policy_rate_2026Q4"]) == (4.21, 4.02),
      f"Brent {obs['brent_last5']} vs {1.25 * obs['brent_three_year_average']:.2f}; rates {en['us_policy_rate_2026Q4']} / {hi['regions']['US']['policy_rate_2026Q4']}")
sg = C["signals"]
check("A3 what the watcher would see, by quarter, at the high end (a late bound): the Nasdaq rule (20% under its high) in "
      "2027Q2 on the 2000-02 bust's ratio of the Nasdaq's fall to household equity's (2027Q3 one for one), the US Sahm "
      "rule in 2027Q1; the model's spread never rises 0.56 in a quarter (unmeasured: not validated against Baa); the Fed "
      "raises in 2026Q4 (4.02 against 3.88; the FOMC test, Log 40), the Riksbank cuts (1.65 against 1.75)",
      sg["bust.us.equity, the 2000-02 ratio"] == "2027Q2" and sg["bust.us.equity, one for one"] == "2027Q3"
      and sg["labour.us.sahm"] == "2027Q1" and sg["bust.credit.baa (unmeasured)"] is None
      and hi["regions"]["US"]["policy_rate_2026Q4"] > regs["US"].i0 and hi["regions"]["SE"]["policy_rate_2026Q4"] < regs["SE"].i0,
      {k: v for k, v in sg.items() if not k.startswith("nasdaq")})

print("K — one dating, and the horizon")
_, o24 = case.build(cm, regs, st, adoption="high", n=24)
_, o25 = case.build(cm, regs, st, adoption="high")
same24 = all(np.array_equal(o24[r][k], o25[r][k][:24], equal_nan=True) for r in gc.R for k in o24[r])
D = C["dates"]
check("K12 one dating (decision 43): gc.quarter_label takes no second dating and names index 0 2026Q3 (the state measured to "
      "September 2026), index 1 — the quarter of the peak, where the bust begins — 2026Q4, END_2028 (9) 2028Q4 and the "
      "last index (24) 2032Q3; the dates: the bust from 2026Q4 (equity first falls in 2027Q1, its trough in 2029Q2), the "
      "tariffs 2027Q1, the premium over 2026Q4-2027Q3, the pace half-way in 2028Q2, robotics from 2028Q4; extending the "
      "case from 24 to 25 quarters changes nothing before it (the comparison with 27dd785 is the record's, at the tag "
      "paths-pre-signfix)",
      list(inspect.signature(gc.quarter_label).parameters) == ["k"] and not hasattr(gc, "MEASURED")
      and [gc.quarter_label(k) for k in (0, 1, case.END_2028, case.N - 1)] == ["2026Q3", "2026Q4", "2028Q4", "2032Q3"]
      and C["start"] == gc.START == "2026Q3" and C["quarters"] == 25
      and D == {"bust_onset": "2026Q4", "equity_first_falls": "2027Q1", "equity_trough": "2029Q2", "tariffs": "2027Q1",
                "premium_builds": "2026Q4-2027Q3", "pace_half_way": "2028Q2", "robotics_begins": "2028Q4"} and same24,
      D)

n_ok = sum(ok for _, ok, _ in RESULTS)
print(f"\n{n_ok}/{len(RESULTS)} checks passed")
print(f"ALL GREEN ({len(RESULTS)})" if n_ok == len(RESULTS) else "FAILURES: " + "; ".join(n.split(" ")[0] for n, ok, _ in RESULTS if not ok))
sys.exit(0 if n_ok == len(RESULTS) else 1)
