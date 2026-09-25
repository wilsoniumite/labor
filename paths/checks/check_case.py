# check_case.py — her case (code/case.py): the model's additions change nothing when off, the settings trace to their
# sources, and the findings, stated as found.
#
# Run from paths/:  ../venv/Scripts/python.exe checks/check_case.py
# Exit status 0 only if every check passes.

from __future__ import annotations

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
rg, o = case.reference(cm, regs)
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
check("K3 the pace starts at the upper bound seen, rises monotonically, is half-way at 2028Q3 and within 5% of the paper's "
      "pace by the last quarter", abs(lp[0] - seen) < 1e-9 and np.all(np.diff(lp) > 0) and abs(half - 0.5) < 0.05 and lp[-1] > 0.95,
      f"start {lp[0]:.3f}, 2028Q3 {lp[7]:.3f} (half-way {half:.2f}), end {lp[-1]:.3f}")
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
check("K7 through 2028 the case is well defined and half as bad again as the model's central run: US out of work 13.8-14.8% "
      "at 2028Q4 against 9.2%, the band under 1.5 points wide; by 2032Q3 the band spans over 10 points (31.5-46.2%) and is "
      "still rising at both ends",
      hi["us_out_of_work_end_2028"] - lo["us_out_of_work_end_2028"] < 1.5
      and lo["us_out_of_work_end_2028"] > 1.4 * ref["us_out_of_work_end_2028"]
      and hi["us_out_of_work_peak"] - lo["us_out_of_work_peak"] > 10 and lo["still_rising_at_end"] and hi["still_rising_at_end"],
      f"2028Q4 {lo['us_out_of_work_end_2028']}-{hi['us_out_of_work_end_2028']} vs {ref['us_out_of_work_end_2028']}; "
      f"2032Q3 {lo['us_out_of_work_peak']}-{hi['us_out_of_work_peak']}")
check("K8 both ends are a labour depression, with the four economies' output 10-20% below capacity at worst (not the "
      "Depression row)", lo["verdict"] == hi["verdict"] == "a labour depression"
      and -20 < hi["four_output_worst"] < -10 and -20 < lo["four_output_worst"] < -10,
      f"{lo['verdict']} {lo['four_output_worst']}; {hi['verdict']} {hi['four_output_worst']}")
pc = {k: v for k, v in C["piece_by_piece"].items() if k != "note"}
late = max(pc, key=lambda k: pc[k]["adds_to_us_out_of_work"])
early = max(pc, key=lambda k: pc[k]["adds_to_us_out_of_work_end_2028"])
check("K9 which piece matters depends on when: by 2028Q4 the bust adds most to US out of work, by 2032Q3 adoption; the "
      "premium and the tariffs each add 4-5 points by 2032Q3", early == "bust" and late == "adoption"
      and 4 <= pc["premium"]["adds_to_us_out_of_work"] <= 5 and 4 <= pc["tariffs"]["adds_to_us_out_of_work"] <= 5,
      {k: (v["adds_to_us_out_of_work_end_2028"], v["adds_to_us_out_of_work"]) for k, v in pc.items()})
check("K10 the case's rising pace is milder than the model's central assumption (the paper's pace from today): taking it back "
      "adds to US out of work; austerity and care capping out each add under a point to the US, and under two points to "
      "the euro area and Sweden",
      pc["pace"]["adds_to_us_out_of_work"] < 0 and all(pc[k]["adds_to_us_out_of_work"] < 1 for k in ("austerity", "care"))
      and all(pc[k][f"adds_to_{r}_out_of_work"] < 2 for k in ("austerity", "care") for r in ("ea", "se")),
      {k: pc[k] for k in ("pace", "austerity", "care")})
sv = {k: v for k, v in C["sensitivities"].items() if k != "note"}
anchor = sv["fiscal dominance: the US anchor loosens to the eroding rules' 0.6"]
check("K11 none of the settings the case leaves out moves US out of work by more than 1.5 points; a looser US anchor deepens "
      "the bust's deflation (US inflation's low 2 points lower) rather than raising inflation",
      all(abs(v["change_in_us_out_of_work"]) <= 1.5 for v in sv.values())
      and anchor["us_inflation_min"] <= hi["regions"]["US"]["inflation_min"] - 1.5
      and anchor["us_inflation_max"] - hi["regions"]["US"]["inflation_max"] < 0.5,
      {k: v["change_in_us_out_of_work"] for k, v in sv.items()})

n_ok = sum(ok for _, ok, _ in RESULTS)
print(f"\n{n_ok}/{len(RESULTS)} checks passed")
sys.exit(0 if n_ok == len(RESULTS) else 1)
