"""apply_round3.py — the fixes from round 3 (a third read of the model sections and proofs,
build/checks/round3_results.json), applied after apply_round2.py.

    python3 -B apply_round3.py REWRITE.tex
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


edit("R3-1", "Machines cannot perform the tasks in $H$.",
     "Machines do not perform the tasks in $H$, which are closed to them by capability or by rule.",
     "H includes tasks reserved by rule, which machines could perform (Assumption 1)")
edit("R3-2", "The government can tax land rents and wages and pay transfers.",
     "The government can tax the rental value of land and wages, pay transfers, and provide the basket of support "
     "in the owner's place.",
     "Section 2 names all the government's instruments (Section 3.5), including public provision of the basket "
     "(sigma = 0), and the tax is on the rental value of land, owed whether or not the land is used")
edit("R3-3", "In matrix form, condition~(i) is~\\eqref{eq:3}",
     "In matrix form, the price equations of condition~(i) are~\\eqref{eq:3}",
     "(3) holds condition (i)'s price equations; its assignment half (each task to the cheaper input) is not a "
     "matrix equation")
edit("R3-4", "uses only cost minimization at the user cost and market clearing.",
     "uses only cost minimization at the user cost, market clearing, and, for the identity in~(iii), $Y>0$, which "
     "the support basket ensures.",
     "the identity in (iii) divides by Y, and Y = C >= N > 0 comes from the support basket in the workers' budget")

open(PATH, "w", encoding="utf-8").write(src)
print("written", PATH)
