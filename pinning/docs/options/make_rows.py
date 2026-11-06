"""make_rows.py — merge drafted options into the rows files of Part 2 (the model at three levels) and Part 3.1 (the
introduction).

    python3 -B make_rows.py part2 SKELETON.json SIMPLE.json MEDIUM.json DIFFS.json OUT.json
    python3 -B make_rows.py intro PILOT.json INTRO.json OUT.json

Part 2 rows print Simple, Medium, Complex left to right. A level that keeps the Complex text (same_as "C") joins
its cell, so a row whose levels all agree prints once, with room for comments.
Part 3.1 rows print R, O, then the new options; the new related-literature row goes before the roadmap.
"""
import json
import sys

COMPLEX_M1 = ("The rewrite's Sections 2--6, about 20 pages: Section 2 describes the economy in words; Section 3 states "
              "Assumptions 1--5, the cost system, workers, the owner, the government and Definitions 1--3, with a "
              "notation table; Section 4 gives Lemma 1, Propositions 1--3 with their proofs, Lemma 2, Theorem 1 "
              "(existence and uniqueness) and Corollary 1; Sections 5 and 6 give Propositions 4--6 and Corollaries "
              "2--3. Durable machines, the owner's discounting and the return on machines run throughout.")
COMPLEX_M32 = ("Appendix A: the owner's problem (Lemma A.1) and the proofs not given in the text. Appendix B: production "
               "networks, several non-produced inputs, machine types and trade, worker types, ideas and institutional "
               "rents, task-level costs. Appendices C--F: expenditure shares, the fiscal transition, human-required "
               "tasks, and the financing and production accounts.")
LEVEL_REASON = "the text does not depend on the level of mathematics"


def load(p):
    return json.load(open(p, encoding="utf-8"))


def level_option(cell, key, label):
    if cell is None:
        return {"key": key, "label": label, "where": "", "tex": "\\emph{(missing)}"}
    if cell.get("same_as"):
        return {"key": key, "label": label, "where": cell.get("where", ""), "same_as": cell["same_as"]}
    tex = cell.get("tex") or "\\emph{Nothing at this level.}"
    where = cell.get("where", "")
    if cell.get("reuses"):
        where = (where + "; " if where else "") + "reuses O " + cell["reuses"]
    return {"key": key, "label": label, "where": where, "tex": tex}


def part2(skel_p, simple_p, medium_p, diffs_p, out_p):
    skel, S, M, D = load(skel_p), load(simple_p), load(medium_p), load(diffs_p)
    srows = {r["id"]: r for r in S["rows"]}
    mrows = {r["id"]: r for r in M["rows"]}
    rows = []
    for r in skel["rows"]:
        rid = r["id"]
        c = dict(r["options"][0])
        if rid == "M.1":
            c = {"key": "C", "label": "Complex", "where": "rewrite \\S\\S2--6", "tex": COMPLEX_M1}
        elif rid == "M.32":
            c = {"key": "C", "label": "Complex", "where": "rewrite appendices", "tex": COMPLEX_M32}
        opts = [level_option(srows.get(rid), "S", "Simple"), level_option(mrows.get(rid), "M", "Medium"), c]
        row = {"id": rid, "title": r["title"], "diff": D.get(rid, ""), "options": opts}
        if all(o.get("same_as") == "C" for o in opts[:2]):
            row["reason"] = LEVEL_REASON
        rows.append(row)
    outline = lambda X: "; ".join(f"{o['number']} {o['title']}" for o in X.get("outline", []))
    spec = {"part": "2", "title": "Part 2 — The model at three levels",
            "subtitle": "Simple (S), Medium (M) and Complex (C, the rewrite): how much mathematics the main text carries",
            "preface": ("Each row is one piece of the model or its results. S, M and C are three versions of the "
                        "main text, left to right; in every version the appendix carries the full Complex treatment, "
                        "so a lower level moves material to the appendix and loses nothing. Cells that two levels "
                        "share print once. Each column read top to bottom is a complete main text at its level."
                        "\\par\\smallskip{\\small\\textbf{Simple, sections:} " + outline(S) + " (about " +
                        str(S.get("pages", "?")) + " pages).\\par\\textbf{Medium, sections:} " + outline(M) +
                        " (about " + str(M.get("pages", "?")) + " pages).\\par\\textbf{Complex, sections:} 2 "
                        "Description of the economy; 3 Definition of equilibrium; 4 Equilibrium; 5 Purchasing power "
                        "and income; 6 Distribution: rent taxation and a uniform transfer (about 20 pages).}"),
            "rows": rows}
    json.dump(spec, open(out_p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("wrote", out_p, len(rows), "rows")


def intro(pilot_p, intro_p, out_p):
    pilot, I = load(pilot_p), load(intro_p)
    by = {r["id"]: r for r in I["rows"]}
    rows = []
    for r in pilot["rows"]:
        new = by.get(r["id"], {})
        row = dict(r)
        row["diff"] = new.get("diff", r.get("diff", ""))
        row["options"] = list(r["options"]) + [
            {"key": o["key"], "label": o.get("label", "New"), "where": o.get("where", ""), "tex": o["tex"]}
            for o in new.get("new", [])]
        if new.get("reason"):
            row["reason"] = new["reason"]
        rows.append(row)
    added = I.get("added_rows", [])
    # the related-literature row goes before the roadmap; renumber so the ids run in order
    roadmap = next(i for i, r in enumerate(rows) if r["title"] == "Roadmap")
    for k, a in enumerate(added):
        a = dict(a)
        a["options"] = [{"key": o["key"], "label": o.get("label", "New"), "where": o.get("where", ""), "tex": o["tex"]}
                        for o in a["options"]]
        rows.insert(roadmap + k, a)
    for i, r in enumerate(rows):
        r["id"] = f"T.1.{i + 1}"
    spec = dict(pilot)
    spec["rows"] = rows
    json.dump(spec, open(out_p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("wrote", out_p, len(rows), "rows")


if __name__ == "__main__":
    if sys.argv[1] == "part2":
        part2(*sys.argv[2:7])
    else:
        intro(*sys.argv[2:5])
