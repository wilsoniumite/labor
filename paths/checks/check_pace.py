# check_pace.py — the pace of displacement against what has been seen (code/pace.py): the findings, stated as found.
#
# Run from paths/:  ../venv/Scripts/python.exe checks/check_pace.py
# Exit status 0 only if every check passes.

from __future__ import annotations

import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


P = json.load(open(os.path.join(ROOT, "results", "pace.json"), encoding="utf-8"))
D = json.load(open(os.path.join(ROOT, "results", "decoupling.json"), encoding="utf-8"))
ob = P["observed"]
ends, trends = ob["endpoints_from"], ob["trends"]
peak = ends["the peak (3-month average)"]
dec = D["where_the_displaced_go"]["prime_age_25_54"]["since_the_employment_peak"]

check("A1 the endpoints from the peak reproduce decoupling.py's measure (the exit share the crash model uses)",
      abs(peak["exit_share"] - dec["exit_share"]) <= 0.01, f"pace {peak}; decoupling {dec}")
tp = trends["since the peak"]
check("A2 on trends, since the peak: non-employment within two standard errors of zero; prime-age unemployment rising, "
      "significantly; participation not falling (exits within two standard errors of zero or negative)",
      abs(tp["non_employment"]["pts_a_year"]) < 2 * tp["non_employment"]["se"]
      and tp["unemployment"]["pts_a_year"] > 2 * tp["unemployment"]["se"]
      and tp["exits"]["pts_a_year"] < 2 * tp["exits"]["se"], tp)
shares = [v["exit_share"] for v in ends.values() if v["exit_share"] is not None]
check("A3 the exit share is not robust: from the three bases it spans more than half the range (from the peak it is over "
      "0.9, from the 2023-24 average under 0.3); June 2026 alone moved participation by half a point or more; on trends it "
      "is negative from both starts (the displaced, if any, show up as unemployment)",
      max(shares) - min(shares) > 0.5 and max(shares) > 0.9 and min(shares) < 0.3
      and ob["prime_age_participation_june_2026_change"] <= -0.5
      and all(v["exit_share"] is None or v["exit_share"] < 0 for v in trends.values()),
      f"endpoints {ends}; June {ob['prime_age_participation_june_2026_change']}; trends {[v['exit_share'] for v in trends.values()]}")
pm, tg, paces = P["window_model_at_the_papers_pace"], P["non_employment_targets_lf_pts"], P["paces"]["multiples_of_the_papers"]
check("A4 the paper's pace runs far ahead of what has been seen: over the window it would have raised US non-employment by "
      "over three times the endpoint measure and over five times the trend's upper bound; the trend's upper bound allows at "
      "most a fifth of the paper's pace, the endpoint under a third",
      pm["non_employment_lf_pts"] > 3 * tg["endpoint"] and pm["non_employment_lf_pts"] > 5 * tg["trend + 2 s.e."]
      and paces["trend + 2 s.e."] <= 0.2 and paces["endpoint"] < 1 / 3,
      f"paper's {pm}; targets {tg}; paces {paces}")
rw = P["rows"]
b = rw["pace: trend + 2 s.e."]
check("A5 the bust, not the pace seen so far, carries the danger: at the trend's upper bound a dot-com-sized bust under today's "
      "rules still takes US out of work above 15%, and above 40% when the rules erode; displacement without a bust stays "
      "under 8%",
      b["modern rules | bust + displacement"]["us_out_of_work_peak"] > 15
      and b["rules erode under pressure | bust + displacement"]["us_out_of_work_peak"] > 40
      and b["modern rules | displacement without a bust"]["us_out_of_work_peak"] < 8,
      {k: v["us_out_of_work_peak"] for k, v in b.items()})
wt, wm = P["window_model_at_each_pace"]["trend"], P["window_model_at_each_pace"]["trend + 2 s.e."]
cbo = ob["cbo_output_gap"]["to"][1] - ob["cbo_output_gap"]["from"][1]
check("A6 the spending loop is not identified on this window: across the paces the data allow, the model's own output gap "
      "accounts for between under a third (the trend) and under two-thirds (its upper bound) of the fall in the CBO gap, which "
      "started from an overheated +1 or more; the rest may be that unwinding",
      abs(wt["output_gap_change"]) < abs(cbo) / 3 and abs(wm["output_gap_change"]) < 2 * abs(cbo) / 3 and cbo < 0
      and ob["cbo_output_gap"]["from"][1] > 1,
      f"model at the trend {wt['output_gap_change']}, at its upper bound {wm['output_gap_change']}; CBO change {cbo:+.2f} from {ob['cbo_output_gap']['from']}")
sv = P["sensitivity"]
check("A8 care's hiring above its trend, counted as displaced people it took in (an upper bound on what it hides), leaves the "
      "data allowing under half the paper's pace on every measure; the build-out's own jobs are too few to matter: all of "
      "construction's gain is under 0.1 points of the labour force, and manufacturing lost more",
      sv["care"]["above_trend_pts_a_year"] > 0 and max(sv["care"]["paces_with_above_trend_care"].values()) < 0.5
      and sv["build_out"]["construction_added_lf_pts"] < 0.1
      and sv["build_out"]["manufacturing_added_lf_pts"] < -sv["build_out"]["construction_added_lf_pts"],
      sv)
rs = P["reproduces_stored"]
check("A7 the reconstruction from the stored regions reproduces the model's own stored run (displacement without a bust, "
      "year 4, US)", all(abs(a - b) <= 0.011 for a, b in rs.values()), rs)

n_ok = sum(ok for _, ok, _ in RESULTS)
print(f"\n{n_ok}/{len(RESULTS)} checks passed")
sys.exit(0 if n_ok == len(RESULTS) else 1)
