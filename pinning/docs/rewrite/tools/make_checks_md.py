# make_checks_md.py — CHECKS.md from the checks workflows' results, with each finding's disposition.
import json, sys
R1 = json.load(open(sys.argv[1]))          # round 1: journal_results.json (five agents, in launch order)
OUT = sys.argv[2]
R2 = json.load(open(sys.argv[3])) if len(sys.argv) > 3 else None
R3 = json.load(open(sys.argv[4])) if len(sys.argv) > 4 else None
names = ["Math, Sections 3-4 and their proofs", "Math, Sections 5-6 and Appendices", "Sources and quotations",
         "Numbers against the code", "Read-through"]
disp = {
 "mathA-1": "applied", "mathA-2": "applied", "mathA-3": "applied", "mathA-4": "applied (one symbol added to the authors' sentence)",
 "mathB-1": "applied", "mathB-2": "applied (same as R01)", "mathB-3": "applied (same as R03)",
 "mathB-4": "applied, reworded: R is defined in the statement's first clause (\"the rental value of land, $R=rT$\")",
 "mathB-5": "applied in R14's wording", "mathB-6": "applied",
 "S1": "applied, reworded: \"In the first two of these models machines are accumulated from output, so automating every task also automates the making of machines; in the third the stock of machines is given.\"",
 "S2": "applied", "N1": "applied", "N2": "applied",
 "R01": "applied (as mathB-2)", "R02": "applied", "R03": "applied (as mathB-3)", "R04": "applied (the sentence moved, no words changed)",
 "R05": "applied through D91", "R06": "applied through D91", "R07": "applied through D91, with \"the\" kept",
 "R08": "applied", "R09": "applied",
 "R10": "applied, reworded: \"may discount the future, in which case a machine must earn a return to be worth holding\"",
 "R11": "applied", "R12": "applied", "R13": "applied (as mathA-4)", "R14": "applied", "R15": "applied", "R16": "applied",
 "R17": "applied", "R18": "applied", "R19": "applied", "R20": "applied, reworded: \"and space, which rents at $r$, has $\\widetilde b=1$\"",
 "R21": "applied", "R22": "applied (one word of the abstract)", "R23": "applied", "R24": "applied", "R25": "applied (Table 1 moved; it prints on p. 5)",
 "V1": "applied (the review's own D6 had broken this pointer)", "V2": "applied", "V3": "applied (a comment only)",
 "X1": "applied (as V1)", "X2": "applied",
 "X3": "not applied: the authors' sentence is true as written (the solved share is 0.0654), and Table 2 lists the 0.06 target and the 0.065 value separately",
 "X4": "applied, reworded: \"except that for a task-produced good the finite set lists combinations of its inputs other than tasks, each joined with any assignment of its tasks as in (B.2)\"",
}
import os
EXTRA = os.environ.get("CHECKS_EXTRA_DISP")
if EXTRA:
    disp.update(json.load(open(EXTRA)))
lines = ["# Checks of the rewrite", "",
         "Two rounds, no ranking. Round 1 checked the assembled rewrite; its fixes, with the defaults for the build's",
         "mechanical decisions (D6, D7, D25, D30, D73, D74, D76, D91, D101-D103, D106), were applied by",
         "`tools/apply_defaults.py` and `tools/apply_findings.py`. Every edit leaves a `% Review edit (<id>)` comment in",
         "`paper/main_rewrite.tex`. Round 2 verified those edits adversarially and read the paper a second time; its",
         "fixes are `tools/apply_round2.py`. Round 3 read the model sections and proofs a third time.", ""]
def section(title, results, labels):
    out = [f"## {title}", ""]
    for lab, d in zip(labels, results):
        r = d["result"] if "result" in d else d
        out += [f"### {lab}", ""]
        if not r["findings"]:
            out += ["No findings.", ""]
        for f in r["findings"]:
            out += [f"- **{f['id']}** ({f['severity']}; {f['location']}). {f['defect']}",
                    f"  - Fix: `{f['fix_old'][:300]}` -> `{f['fix_new'][:300]}`" if f['fix_old'] else f"  - Fix: {f['fix_new'][:300] or 'see the defect'}",
                    f"  - Disposition: {disp.get(f['id'], 'see the round-2 notes')}."]
        ok = r.get("passed") or r.get("verified_ok") or []
        if ok:
            out += ["", f"Passed ({len(ok)}):", ""] + [f"- {x}" for x in ok]
        nc = r.get("not_checked") or []
        if nc:
            out += ["", "Not checked:", ""] + [f"- {x}" for x in nc]
        out += [""]
    return out
lines += section("Round 1", R1, names)
if R2:
    lines += section("Round 2", [R2["verify"], R2["read2"]], ["Verification of the review edits", "Second read-through"])
if R3:
    lines += section("Round 3", [R3["round3"]], ["Third read: the model sections and proofs"])
open(OUT, "w").write("\n".join(lines) + "\n")
print("wrote", OUT, len(lines), "lines")
