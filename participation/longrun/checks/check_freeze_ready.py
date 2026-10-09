# check_freeze_ready.py — what must hold before the tag participation-L-freeze (PROTOCOL sections 3, 7 and 9, L2-L3),
# on the real repository. Unlike the other checks it is EXPECTED TO FAIL until her L2/L3 steps are done: each failing
# line is a to-do, not a bug. fetch.freeze_ready() enforces the committed part of this list at every value door (a
# premature tag opens nothing); this script also covers the working tree.
#   R1  no IPUMS microdata or codebook under longrun/ outside the extract folder (fetch.IPUMS_DIR) (names only; nothing is opened);
#   R2  nothing in the extract folder while the L tag does not exist (the extract is made after the tag, L9);
#   R3  the frozen IPUMS-I list is complete: every grouped-age sample with RELATE has its recorded age intervals, every
#       sample's kind (census, count, survey) is confirmed, and nothing is left in 'to_confirm_at_L2';
#   R4  the Kholodilin file is confirmed (fetch.SOURCES['kholodilin'] has its URL) or her decision to drop the run and
#       the qualifier before the freeze is recorded in data/decisions.json;
#   R5  the JST and ILOSTAT values-dropping masks have run (data/coverage.json no longer says they were not run);
#   R6  segments_documented.csv holds the school (ILO notes) and coresidence (RELATE scheme) rows, or data/decisions.json
#       records that the documentation names none;
#   R7  data/seen.json records where the scouts' folders were moved, with their files hashed;
#   R8  FORECASTS.md is filled by every participant;
#   R9  results/europe_run_*.json exists (the European real-data run, once, from a commit holding specs.py and
#       PROTOCOL.md);
#   R10 data/skeleton.json is a production run computed by the current code; results/simulate.json likewise;
#   R11 her Extract B decision is recorded in data/decisions.json ('extract_b': true or false).
#
# Run from longrun/:  ../../venv/Scripts/python.exe checks/check_freeze_ready.py   Exit status 0 only when ready.

from __future__ import annotations

import glob
import json
import os
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
LROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(LROOT, "code"))
import fetch  # noqa: E402
import ipums  # noqa: E402

RESULTS = []
DECISIONS = os.path.join(LROOT, "data", "decisions.json")


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    print(f"  [{'READY' if ok else 'TO DO'}] {name}" + (f" — {detail}" if detail else ""))


def jload(path):
    try:
        return json.load(open(path, encoding="utf-8"))
    except (OSError, ValueError):
        return None


dec = jload(DECISIONS) or {}
has_l = subprocess.run(["git", "rev-parse", "-q", "--verify", f"refs/tags/{fetch.L_FREEZE}"], cwd=LROOT,
                       capture_output=True).returncode == 0
stray = ipums.stray_microdata()
check("R1 no IPUMS microdata under longrun/ outside the extract folder (fetch.IPUMS_DIR) (names only)", not stray,
      f"{stray}: move it out of the repository (her call where; PROTOCOL section 7)" if stray else "")
inside = glob.glob(os.path.join(fetch.IPUMS_DIR, "*")) if os.path.isdir(fetch.IPUMS_DIR) else []
check("R2 nothing in the extract folder before the L tag", has_l or not inside, f"{len(inside)} files" if inside else "")
smp = jload(ipums.SAMPLES) or {}
recs = smp.get("F_L", []) + smp.get("extract_B", [])
no_iv = [r["sample"] for r in recs if r.get("grouped_age") and r.get("relate") and not r.get("age_intervals")]
unconf = [r["sample"] for r in recs if "confirm" in str(r.get("kind", "confirm"))]
check("R3 the frozen IPUMS-I list is complete (age intervals, kinds, the L2 records)",
      not no_iv and not unconf and not smp.get("to_confirm_at_L2"),
      f"no intervals: {no_iv}; kind unconfirmed: {len(unconf)} samples; to confirm: {smp.get('to_confirm_at_L2')}")
check("R4 the Kholodilin file confirmed, or its run dropped by her decision",
      bool(fetch.SOURCES["kholodilin"].get("url")) or dec.get("kholodilin") == "dropped")
cube = jload(os.path.join(LROOT, "data", "coverage.json")) or {}
check("R5 the JST and ILOSTAT values-dropping masks have run", "not run" not in str(cube.get("status", "not run")),
      str(cube.get("status", ""))[:120])
doc = open(os.path.join(LROOT, "data", "segments_documented.csv"), encoding="utf-8").read()
check("R6 school and coresidence segment rows transcribed (or none named, recorded)",
      (",school," in doc or dec.get("school_segments") == "none named")
      and (",coresid," in doc or dec.get("coresid_segments") == "none named"))
seen = jload(os.path.join(LROOT, "data", "seen.json")) or {}
sf = seen.get("scouts_folders") or {}
check("R7 the scouts' folders moved and their files hashed (data/seen.json)", bool(sf.get("moved_to") and sf.get("files")))
ok, why = fetch.forecasts_filled(open(fetch.FORECASTS_PATH, encoding="utf-8").read())
check("R8 FORECASTS.md filled by every participant", ok, why)
check("R9 the European real-data run exists", bool(glob.glob(os.path.join(LROOT, "results", "europe_run_*.json"))))
sys.path.insert(0, os.path.join(LROOT, "code"))
import skeleton  # noqa: E402
import simulate  # noqa: E402
sk = jload(skeleton.OUT) or {}
sm = jload(simulate.OUT) or {}
check("R10 data/skeleton.json and results/simulate.json are production runs of the current code",
      sk.get("quick") is False and sk.get("code_sha256") == skeleton.code_sha()
      and sm.get("code_sha256") == simulate.code_sha())
check("R11 her Extract B decision recorded", isinstance(dec.get("extract_b"), bool))
n_todo = sum(1 for _, ok, _ in RESULTS if not ok)
print(f"\n{len(RESULTS) - n_todo}/{len(RESULTS)} ready; {n_todo} to do before the L-freeze tag")
sys.exit(1 if n_todo else 0)
