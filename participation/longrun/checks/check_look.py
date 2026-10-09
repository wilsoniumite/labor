# check_look.py — the synthetic end-to-end look (code/simulate.py -> results/simulate.json): the explore opening and
# confirm.py run on synthetic worlds through the real guarded doors, with the freeze tags simulated.
#   (a) the results come from the current code (SHA-256 recorded by simulate.py);
#   (b) planted world (DiD = -40 with a falling high-floor top slope): LR-K2 supported, the drop condition holds, the
#       model-level reading 'favours the floor mechanism ...' with the Kaplan/Ermisch sentence; LR-Y0 and C-6L
#       supported (their planted effects);
#   (c) opposite world (DiD = +40): LR-K2 contradicted; 'against the floor mechanism together with its stated regime
#       placement and auxiliaries 1-3'; the joint reading names the long-run regime placement;
#   (d) null world: LR-K2 not supported;
#   (e) in every world: no network call; every door call went through the guard for an open half and its countries
#       (explore opening: explore countries only); every outcome call came after that half's knots and F_L records;
#       H was recorded at the look and equals the rule applied to the synthetic F_L; the explore countries' knots at
#       the look are the explore opening's; the ten robustness rows (the strict-control rows run, not errors, on the
#       synthetic Kholodilin coding, with the uncovered countries listed), the no-verdict list (D2-L with its placebo,
#       the pooled D1) and the confirm-half replication (LR-K2 for information) are reported; LR-K2's five qualifiers
#       were run, the control-era one on the strict years.
#
# Run from longrun/:  ../../venv/Scripts/python.exe checks/check_look.py      Exit status 0 only if all pass.

from __future__ import annotations

import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
LROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(LROOT, "code"))
import simulate  # noqa: E402
import specs  # noqa: E402

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


S = json.load(open(simulate.OUT, encoding="utf-8"))
check("A1 results/simulate.json was computed by the current code", S.get("code_sha256") == simulate.code_sha(),
      str([f for f, h in simulate.code_sha().items() if S.get("code_sha256", {}).get(f) != h]))
W = S["worlds"]
P, O, N = W["planted"], W["opposite"], W["null"]
print("(b) planted")
check("B1 LR-K2 supported, drop condition held, model 'favours ...' with the Kaplan/Ermisch sentence",
      P["verdicts"].get("LR-K2") == "supported" and P["k2"].get("drop_condition") is True
      and P["model_verdict"] == specs.MODEL_READINGS["favours"] and "Kaplan" in P["model_sentence"],
      f"{P['verdicts']}; {P['model_verdict']}")
check("B2 LR-Y0 and C-6L supported (planted g1 = 20, school on U = 2.0)",
      P["verdicts"].get("LR-Y0") == "supported" and P["verdicts"].get("C-6L") == "supported", str(P["verdicts"]))
check("B3 the joint reading: supported in the long run, not in 2009-2025 Europe",
      P["joint_reading"].startswith("supported in the long run"), P["joint_reading"])
print("(c) opposite")
check("C1 LR-K2 contradicted; model 'against the floor mechanism together with its stated regime placement and "
      "auxiliaries 1-3'", O["verdicts"].get("LR-K2") == "contradicted"
      and O["model_verdict"] == specs.MODEL_READINGS["against"], f"{O['verdicts']}; {O['model_verdict']}")
check("C2 the joint reading names the long-run regime placement", "long-run regime placement" in O["joint_reading"],
      O["joint_reading"])
print("(d) null")
check("D1 LR-K2 not supported in the null world", N["verdicts"].get("LR-K2") != "supported", str(N["verdicts"]))
print("(e) every world")
check("E1 no network call was attempted", S["network_calls"] == 0)
for name, w in W.items():
    calls = w["calls"]
    ex = [c for c in calls if c["half"] == "explore"]
    cf = [c for c in calls if c["half"] == "confirm"]
    outcome = [c for c in calls if c["source"] in ("ilostat",) or (c["source"] == "oecd_lfs")]
    order_ok = all({"knots", "F_L"} <= set(c["records"]) for c in outcome)
    check(f"E2 {name}: every outcome door call came after its half's knots and F_L records", order_ok and outcome,
          f"{len(outcome)} outcome calls")
    split = json.load(open(os.path.join(LROOT, "data", "split.json"), encoding="utf-8"))
    check(f"E3 {name}: the explore opening asked for explore countries only; the look for the split's countries",
          all(set(c["geos"]) <= set(split["explore"]) for c in ex)
          and all(set(c["geos"]) <= set(split["countries"]) for c in cf) and ex and cf)
    recs = [(r["record"], r["half"]) for r in w["records"]]
    check(f"E4 {name}: records in L14's order: explore knots, explore F_L, then confirm knots, F_L, H",
          recs == [("knots", "explore"), ("F_L", "explore"), ("knots", "confirm"), ("F_L", "confirm"),
                   ("H", "confirm")], str(recs))
    check(f"E5 {name}: H at the look = the L9 rule applied to the synthetic F_L", w["H_look"] == w["H_world"])
    vin = w["vintage"] or {}
    rows_v = [v for key in ("q", "q_hpi") for v in (vin.get(key) or {}).values()]
    check(f"E6 {name}: the explore countries' q and q_hpi knots at the look are the explore opening's, and their q "
          f"paths hash the same (one vintage: no difference reported)",
          vin.get("q") and vin.get("q_hpi") and not any(v["differ"] for v in rows_v)
          and all(v["q_path_changed"] is False for v in rows_v), str({k: len(v or {}) for k, v in vin.items()}))
    rob = {r.split(".")[0] for r in w["robustness_ids"]}
    check(f"E7 {name}: the ten robustness rows (post-freeze segments only if they exist), the no-verdict list, the "
          f"replication and LR-K2's five qualifiers", rob >= set(specs.ROBUSTNESS) - {"post_freeze_segments"}
          and {"D1-L", "D2-L", "C-2L", "C-3L.diff", "C-3L.women", "E-SCH1-L"} <= set(w["no_verdict_ids"])
          and w["replication_labels"] is not None and set(w["k2_qualifiers"]) == set(specs.K2_QUALIFIERS),
          f"{sorted(rob)}")
    strict_rows = {k: v for k, v in w["robustness"].items() if k.startswith("strict_control_dropped.LR-")}
    check(f"E8 {name}: the strict-control rows ran on the Kholodilin coding (no error entry), the control-era "
          f"qualifier ran, and the uncovered countries are listed",
          strict_rows and all(isinstance(v, dict) and "error" not in v for v in strict_rows.values())
          and (w["control_era"] or {}).get("run") is not None
          and w["kholodilin_uncovered"] and "US" not in w["kholodilin_uncovered"],
          str({k: (v.get("error") if isinstance(v, dict) else v) for k, v in strict_rows.items()}))
    check(f"E9 {name}: LR-K2's confirm-half replication is reported for information; D2-L's placebo and the pooled D1 "
          f"are reported (LR-K2 needs 2 countries per floor group, else the reason)",
          w["replication_k2"] and ("beta" in w["replication_k2"]
                                   or (min(sum(w["replication_k2"]["H"].values()),
                                           len(w["replication_k2"]["H"]) - sum(w["replication_k2"]["H"].values())) < 2
                                       and "error" in w["replication_k2"]))
          and (w["d2_placebo"] or {}).get("draws", 0) > 100 and "beta" in (w["pooled_d1"] or {}),
          str(w["replication_k2"])[:200])

n_fail = sum(1 for _, ok, _ in RESULTS if not ok)
print(f"\n{len(RESULTS) - n_fail}/{len(RESULTS)} checks pass")
sys.exit(1 if n_fail else 0)
