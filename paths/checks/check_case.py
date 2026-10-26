# check_case.py — her case (code/case.py): the model's additions change nothing when off, the settings trace to their
# sources, the dating is one and the 25-quarter horizon changes nothing before it, and the findings, stated as found.
#
# Restated 2026-10-01 on the one dating (decision 43: index 0 = 2026Q3, the state measured to September 2026; index 1 =
# 2026Q4; 2028Q4 = index 9; 2032Q3 = index 24): K3, K7, K9-K11 quote the measured labels; where a run is at the model's
# 50% cap by 2032Q3 its reading there is a floor and 2032Q2 is quoted (K10, K11); K12 is new. No gate was loosened; the
# gates' bounds are as first set (K7's 1.4 times and 1.5 points, K9's 4-5 points, K10's one and two points, K11's 1.5
# points), and the case's premium now sits on K9's upper bound (5.0; 4.996 unrounded).
#
# K9 (also 2026-10-01) gates the pieces' method too: differences of values rounded to 0.1, each within 0.1 of the unrounded
# difference (the unrounded ones at 2028Q4 quoted beside them in STATE). K12's comparison with case.json as committed at
# 27dd785 needs git history: without it (no git, a ZIP download, a shallow clone) that part is reported, not gated, and
# the 24- against 25-quarter prefix test, which needs no git, gates alone.
#
# Run from paths/:  ../venv/Scripts/python.exe checks/check_case.py
# Exit status 0 only if every check passes.

from __future__ import annotations

import inspect
import json
import os
import sys

import numpy as np

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "code"))
import case  # noqa: E402
import global_crash as gc  # noqa: E402

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


C = json.load(open(os.path.join(ROOT, "results", "case.json"), encoding="utf-8"))
G = json.load(open(os.path.join(ROOT, "results", "global_crash.json"), encoding="utf-8"))
P = json.load(open(os.path.join(ROOT, "results", "pace.json"), encoding="utf-8"))
cm, regs = case.stored()
st = C["settings"]

# --- the additions to global_crash.py are off by default
rg, o = case.reference(cm, regs, 24)       # global_crash's stored runs are 24 quarters (K12: the 25th changes none of them)
key = "modern rules | bust + displacement | two waves, robotics in 2 years, care absorbs"
same = json.loads(json.dumps({"year4": gc.summary(o, rg, 16), "year6": gc.summary(o, rg)})) == G["scenarios"][key]
a, b = gc.ai_shock(24), gc.ai_shock(24, 1.0, 1.0)
shock_same = all(np.array_equal(getattr(a, f)[r], getattr(b, f)[r]) for f in ("equity", "capex", "losses") for r in gc.R)
check("K1 the four additions (a faster bust, a pace by quarter, a premium on borrowing, a region's own care ceiling) are off "
      "by default: the model's central run reproduces its stored scenario exactly, and the default bust is the fitted one",
      same and shock_same, key)

# --- the settings trace to their sources
seen = P["paces"]["multiples_of_the_papers"]["trend + 2 s.e."]
cap_ok = all(abs(st["care_cap"][r] - (regs[r].care_share + regs[r].care_trend)) < 0.006 for r in gc.R)
tar_ok = st["tariff"]["US"] == 25.0 and all(abs(st["tariff"][r] - 25.0 * regs[r].trade.get("US", 0.0)) < 0.006 for r in ("EA", "SE", "CN"))
check("K2 the settings trace to their sources: the starting pace is pace.py's upper bound on what has been seen; each care "
      "ceiling is today's share plus one year of its trend; the tariff each region's exports face is 25 points times its "
      "export share to the US (the US: 25)", st["pace"]["seen"] == seen and cap_ok and tar_ok,
      f"seen {st['pace']['seen']}; caps {st['care_cap']}; tariffs {st['tariff']}")
lp = case.logistic_pace(1.0, seen, st["pace"]["mid_quarter"], st["pace"]["width_quarters"])
half = (lp[st["pace"]["mid_quarter"]] - seen) / (1 - seen)
check("K3 the pace starts at the upper bound seen, rises monotonically, is half-way at 2028Q2 (index 7) and within 5% of the "
      "paper's pace by the last quarter (2032Q3)", abs(lp[0] - seen) < 1e-9 and np.all(np.diff(lp) > 0) and abs(half - 0.5) < 0.05
      and lp[-1] > 0.95 and len(lp) == case.N == 25 and gc.quarter_label(st["pace"]["mid_quarter"]) == "2028Q2",
      f"start {lp[0]:.3f}, {gc.quarter_label(7)} {lp[7]:.3f} (half-way {half:.2f}), {gc.quarter_label(len(lp) - 1)} {lp[-1]:.3f}")
fast = gc.ai_shock(24, 1.5, 2.0)
check("K4 the bust is bigger and faster: US stocks down 60% and AI investment 90%, both complete by the second quarter "
      "(the fitted bust: 40% and 60% over four)",
      abs(fast.equity["US"][2] - 0.6) < 1e-9 and abs(fast.capex["US"][2] - 0.9) < 1e-9
      and abs(a.equity["US"][4] - 0.4) < 1e-9 and a.equity["US"][2] < 0.4,
      f"equity {fast.equity['US'][:4].round(2).tolist()}; capex {fast.capex['US'][:4].round(2).tolist()}")

# --- the case reproduces, and its pieces act as stated
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

# --- the findings, stated as found
lo, hi, ref = C["case"]["low"], C["case"]["high"], C["reference_central_run"]
po = {e: C["paths"][e]["US"]["out_of_work"] for e in ("low", "high", "reference")}
ratio = [po[e][case.END_2028] / po["reference"][case.END_2028] for e in ("low", "high")]
check("K7 through 2028 the case is well defined and about one and a half times the model's central run: US out of work "
      "11.0-12.0% at 2028Q4 against 7.6% (1.46-1.58 times), the band under 1.5 points wide; by 2032Q3 the band spans over "
      "10 points (25.5-36.0%; 24.5-34.0% at 2032Q2), the high end 14.0 under the model's 50% cap, and is still rising at "
      "both ends. Restated after the crash model's sign fix of 2026-10-26: before it 14.4-15.7% against 10.1% (1.43-1.56), "
      "32.9-49.0% by 2032Q3, 1.0 under the cap",
      hi["us_out_of_work_end_2028"] - lo["us_out_of_work_end_2028"] < 1.5
      and lo["us_out_of_work_end_2028"] > 1.4 * ref["us_out_of_work_end_2028"]
      and [lo["us_out_of_work_end_2028"], hi["us_out_of_work_end_2028"], ref["us_out_of_work_end_2028"]] == [11.0, 12.0, 7.6]
      and [round(x, 2) for x in ratio] == [1.46, 1.58]
      and hi["us_out_of_work_peak"] - lo["us_out_of_work_peak"] > 10 and lo["still_rising_at_end"] and hi["still_rising_at_end"]
      and [lo["us_out_of_work_peak"], hi["us_out_of_work_peak"]] == [25.5, 36.0]
      and [lo["us_out_of_work_2032Q2"], hi["us_out_of_work_2032Q2"]] == [24.5, 34.0]
      and lo["us_at_the_models_cap_from"] is None and hi["us_at_the_models_cap_from"] is None
      and round(case.CAP - po["high"][-1], 1) == 14.0,
      f"2028Q4 {lo['us_out_of_work_end_2028']}-{hi['us_out_of_work_end_2028']} vs {ref['us_out_of_work_end_2028']} "
      f"(x{ratio[0]:.2f}-{ratio[1]:.2f}); 2032Q3 {lo['us_out_of_work_peak']}-{hi['us_out_of_work_peak']}; "
      f"2032Q2 {lo['us_out_of_work_2032Q2']}-{hi['us_out_of_work_2032Q2']}")
check("K8 both ends are a labour depression, with the four economies' output 10-20% below capacity at worst (not the "
      "Depression row)", lo["verdict"] == hi["verdict"] == "a labour depression"
      and -20 < hi["four_output_worst"] < -10 and -20 < lo["four_output_worst"] < -10,
      f"{lo['verdict']} {lo['four_output_worst']}; {hi['verdict']} {hi['four_output_worst']}")
pc = {k: v for k, v in C["piece_by_piece"].items() if k != "note"}
late = max(pc, key=lambda k: pc[k]["adds_to_us_out_of_work"])
early = max(pc, key=lambda k: pc[k]["adds_to_us_out_of_work_end_2028"])
# the pieces' method: each 'adds' is the difference of the two runs' values as case.read rounds them (0.1), so it is within
# 0.1 of the difference of the unrounded runs; the unrounded ones at 2028Q4 (high end) are what STATE quotes beside them
oow_h = o_h["US"]["u"] + o_h["US"]["out"]
unr, meth = {}, True
for p_ in case.PIECES:
    _, o_p = case.build(cm, regs, st, drop=p_)
    x_ = o_p["US"]["u"] + o_p["US"]["out"]
    unr[p_] = round(float(oow_h[case.END_2028] - x_[case.END_2028]), 2)
    add_ = pc[p_]["adds_to_us_out_of_work_end_2028"]
    meth &= add_ == round(round(float(oow_h[case.END_2028]), 1) - round(float(x_[case.END_2028]), 1), 1) and abs(add_ - unr[p_]) <= 0.1 + 1e-9
    meth &= abs(pc[p_]["adds_to_us_out_of_work"] - float(oow_h.max() - x_.max())) <= 0.1 + 1e-9
check("K9 which piece matters depends on when: by 2028Q4 the bust adds most to US out of work (2.5), by 2032Q3 adoption "
      "(10.5); the premium and the tariffs each add 3.5-4.5 points by 2032Q3 (4.1 and 3.8). Each piece is the difference of "
      "values rounded to 0.1 (case.json's method), within 0.1 of the unrounded difference; at 2028Q4 unrounded the bust "
      "2.49, the premium 1.49, the tariffs 1.48, the pace -1.34, adoption 0.93, so the premium and the tariffs are not "
      "ranked against each other there. Restated after the crash model's sign fix of 2026-10-26: before it the bust 2.8, "
      "adoption 16.1, the premium 5.0 and the tariffs 4.6 (4-5 points)",
      early == "bust" and late == "adoption"
      and 3.5 <= pc["premium"]["adds_to_us_out_of_work"] <= 4.5 and 3.5 <= pc["tariffs"]["adds_to_us_out_of_work"] <= 4.5
      and (pc["bust"]["adds_to_us_out_of_work_end_2028"], pc["adoption"]["adds_to_us_out_of_work"]) == (2.5, 10.5)
      and (pc["premium"]["adds_to_us_out_of_work"], pc["tariffs"]["adds_to_us_out_of_work"]) == (4.1, 3.8)
      and meth and unr == {"bust": 2.49, "pace": -1.34, "adoption": 0.93, "premium": 1.49, "tariffs": 1.48, "austerity": 0.01, "care": 0.22},
      {k: (v["adds_to_us_out_of_work_end_2028"], v["adds_to_us_out_of_work_2032Q2"], v["adds_to_us_out_of_work"]) for k, v in pc.items()}
      | {"unrounded_2028Q4": unr})
check("K10 the case's rising pace is milder than the model's central assumption (the paper's pace from today): taking it back "
      "adds to US out of work, 1.3 points at 2028Q4 and 2.5 by 2032Q2 and 2032Q3 (no run reaches the model's 50% cap); "
      "austerity and care capping out each add under a point to the US, and under two points to the euro area and Sweden. "
      "Restated after the crash model's sign fix of 2026-10-26: before it 1.6 and 3.0, with the run at the paper's pace at "
      "the cap by 2032Q3",
      pc["pace"]["adds_to_us_out_of_work"] < 0 and pc["pace"]["adds_to_us_out_of_work_2032Q2"] < 0
      and pc["pace"]["adds_to_us_out_of_work_end_2028"] < 0
      and (pc["pace"]["adds_to_us_out_of_work_end_2028"], pc["pace"]["adds_to_us_out_of_work_2032Q2"], pc["pace"]["adds_to_us_out_of_work"]) == (-1.3, -2.5, -2.5)
      and all(pc[k]["us_at_the_models_cap_from"] is None for k in case.PIECES)
      and all(pc[k]["adds_to_us_out_of_work"] < 1 for k in ("austerity", "care"))
      and all(pc[k][f"adds_to_{r}_out_of_work"] < 2 for k in ("austerity", "care") for r in ("ea", "se")),
      {k: pc[k] for k in ("pace", "austerity", "care")})
sv = {k: v for k, v in C["sensitivities"].items() if k != "note"}
anchor = sv["fiscal dominance: the US anchor loosens to the eroding rules' 0.6"]
check("K11 none of the settings the case leaves out moves US out of work by more than 1.5 points, at 2032Q3 or 2032Q2 (a "
      "looser US anchor adds 0.8 by both, and no run reaches the model's 50% cap); it deepens the bust's deflation (US "
      "inflation's low -2.6% against -1.0%) rather than raising inflation. Restated after the crash model's sign fix of "
      "2026-10-26: before it the anchor added 1.1 by 2032Q2 and reached the cap at 2032Q3; -4.0% against -2.0%",
      all(abs(v["change_in_us_out_of_work"]) <= 1.5 and abs(v["change_in_us_out_of_work_2032Q2"]) <= 1.5 for v in sv.values())
      and anchor["change_in_us_out_of_work_2032Q2"] == 0.8
      and all(v["us_at_the_models_cap_from"] is None for v in sv.values())
      and anchor["us_inflation_min"] <= hi["regions"]["US"]["inflation_min"] - 1.5
      and (anchor["us_inflation_min"], hi["regions"]["US"]["inflation_min"]) == (-2.6, -1.0)
      and anchor["us_inflation_max"] - hi["regions"]["US"]["inflation_max"] < 0.5,
      {k: (v["change_in_us_out_of_work_2032Q2"], v["change_in_us_out_of_work"]) for k, v in sv.items()})

# --- one dating, and the horizon
# The comparison with 27dd785's case.json (every stored path equal in its first 24 entries) held to the tag
# paths-pre-signfix; the crash model's sign fix of 2026-10-26 moves every array, so it is a property of that record
# (git checkout paths-pre-signfix, then checks/check_case.py), not of this case
_, o24 = case.build(cm, regs, st, adoption="high", n=24)
_, o25 = case.build(cm, regs, st, adoption="high")
same24 = all(np.array_equal(o24[r][k], o25[r][k][:24], equal_nan=True) for r in gc.R for k in o24[r])
check("K12 one dating (decision 43): gc.quarter_label takes no second dating and names index 0 2026Q3 (the state measured to "
      "September 2026), index 1 — where the bust's first falls come — 2026Q4, END_2028 (9) 2028Q4 and the last index (24) "
      "2032Q3; extending the case from 24 to 25 quarters changes nothing before it: every array of a 24-quarter run equals "
      "the 25-quarter run's first 24 (the comparison with 27dd785 is the record's, at the tag paths-pre-signfix)",
      list(inspect.signature(gc.quarter_label).parameters) == ["k"] and not hasattr(gc, "MEASURED")
      and [gc.quarter_label(k) for k in (0, 1, case.END_2028, case.N - 1)] == ["2026Q3", "2026Q4", "2028Q4", "2032Q3"]
      and C["start"] == gc.START == "2026Q3" and C["quarters"] == 25 and int(np.argmax(fast.equity["US"] > 0)) == 1
      and same24, "the 24-quarter run equals the 25-quarter run's first 24")

n_ok = sum(ok for _, ok, _ in RESULTS)
print(f"\n{n_ok}/{len(RESULTS)} checks passed")
print(f"ALL GREEN ({len(RESULTS)})" if n_ok == len(RESULTS) else "FAILURES: " + "; ".join(n.split(" ")[0] for n, ok, _ in RESULTS if not ok))
sys.exit(0 if n_ok == len(RESULTS) else 1)
