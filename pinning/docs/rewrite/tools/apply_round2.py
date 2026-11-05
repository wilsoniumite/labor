"""apply_round2.py — the fixes from round 2 (verification of the review edits and a second read-through,
build/checks/round2_results.json), applied after apply_findings.py.

    python3 -B apply_round2.py REWRITE.tex
"""
import sys

PATH = sys.argv[1]
src = open(PATH, encoding="utf-8").read()


def para_start(text, pos):
    lines_before = text[:pos].split("\n")
    i = len(lines_before) - 1
    while i > 0:
        prev = lines_before[i - 1]
        if not prev.strip() or prev.lstrip().startswith("%"):
            break
        i -= 1
    return sum(len(L) + 1 for L in lines_before[:i])


def edit(tag, old, new, note):
    global src
    n = src.count(old)
    assert n == 1, f"{tag}: expected 1 occurrence, found {n}: {old[:80]!r}"
    first = src.find(old)
    src = src.replace(old, new)
    if note:
        ps = para_start(src, first)
        src = src[:ps] + f"% Review edit ({tag}): {note}\n" + src[ps:]
    print(f"{tag}: done")


# V1 = X1: D6 dropped the parents example from Section 3.4; it prints in Section 2
edit("V1", "The parents (Section~\\ref{sec:owner}) may themselves",
     "The parents (Section~\\ref{sec:description}) may themselves",
     "the pointer follows the parents example to Section 2, where it now prints alone (D6)")

# V2: the remark's claim needs that no payment favors exit
edit("V2", "while every positive wage draws some workers when $F(z)>0$ for $z>0$, as in the instance,",
     "while, if no payment favors exit ($g_e\\le g_w$), every positive wage draws some workers when $F(z)>0$ for "
     "$z>0$, as in the instance,",
     "the claim holds when no payment favors exit; with g_e > g_w + (1 - tau_w)w nobody works at that wage")

# V3: the review note of mathB-4 misplaced R's earlier definition (a comment only)
edit("V3", "(it was defined only in Corollary 3)",
     "(it was defined only in the coverage paragraph after Proposition 6's remark)", None)

# X2: Table 1's gloss of the ceiling, with Lemma 2's case of no such task
edit("X2", "ceiling, the first open task at which machines cannot undercut labor (Lemma~\\ref{lem:ceiling})",
     "ceiling, the first open task at which machines cannot undercut labor, or $x_H$ if there is none "
     "(Lemma~\\ref{lem:ceiling})",
     "Table 1's gloss of x_c gains Lemma 2's case with no such task (Section 7's path has x_c = 1)")

# X4: Assumption B.1's finite set of methods, with the continuum of task assignments of (B.2)
edit("X4", "Each good $i\\ne m$ has a nonempty finite set of feasible methods;",
     "Each good $i\\ne m$ has a nonempty finite set of feasible methods, except that for a task-produced good the "
     "finite set lists combinations of its inputs other than tasks, each joined with any assignment of its tasks as "
     "in~\\eqref{eq:assignment};",
     "a task-produced good has a method for each assignment of its tasks (B.2, Definition B.1), so only its other "
     "inputs come from a finite set")

# Stale provenance after D6 (a comment only)
edit("D6-note", "% from main.tex L268, sentences 2-4, verbatim (sentence 1 is said",
     "% from main.tex L268, sentences 2 and 4, verbatim (sentence 3, the parents, was dropped here at review, D6; "
     "sentence 1 is said", None)

open(PATH, "w", encoding="utf-8").write(src)
print("written", PATH)
