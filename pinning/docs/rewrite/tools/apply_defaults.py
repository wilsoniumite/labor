"""apply_defaults.py — the mechanical review edits (ASSEMBLY.md §5 decisions taken by default), applied to
main_rewrite.tex in place. Each old string must occur exactly once (or the stated number of times); each edit
leaves a "% Review edit (Dn): ..." comment before its paragraph, so the provenance stays readable.

    python3 -B apply_defaults.py REWRITE.tex
"""
import re
import sys

PATH = sys.argv[1]
src = open(PATH, encoding="utf-8").read()


def para_start(text, pos):
    """Index of the first line of the paragraph containing pos (after its provenance comments)."""
    lines_before = text[:pos].split("\n")
    i = len(lines_before) - 1
    while i > 0:
        prev = lines_before[i - 1]
        if not prev.strip() or prev.lstrip().startswith("%"):
            break
        i -= 1
    return sum(len(L) + 1 for L in lines_before[:i])


def edit(tag, old, new, note, count=1, region=None):
    global src
    lo, hi = (0, len(src)) if region is None else region_bounds(*region)
    seg = src[lo:hi]
    n = seg.count(old)
    assert n == count, f"{tag}: expected {count} occurrence(s), found {n}: {old[:80]!r}"
    first = lo + seg.find(old)
    seg = seg.replace(old, new)
    src = src[:lo] + seg + src[hi:]
    if note:
        ps = para_start(src, first)
        src = src[:ps] + f"% Review edit ({tag}): {note}\n" + src[ps:]
    print(f"{tag}: {count} replaced")


def region_bounds(start_marker, end_marker):
    a = src.index(start_marker)
    b = src.index(end_marker, a)
    return a, b


# D6: the owner's two sentences that also print in Section 2 (the design's gloss and L268 sentence 3)
edit("D6", "The owner stands for whoever sustains a person outside paid work.\n", "",
     None)
edit("D6",
     "Our participation benchmark focuses on dependence: a household or public institution provides the living "
     "standard available outside employment. For example, an adult may live with parents who provide housing and "
     "basic consumption while the adult decides whether to take paid work. If support continues",
     "Our participation benchmark focuses on dependence: a household or public institution provides the living "
     "standard available outside employment. If support continues",
     "the design's gloss \"The owner stands for whoever sustains a person outside paid work.\" and L268's sentence 3 "
     "(the parents) are dropped here, since both print in Section 2's description of the owner")

# D7: L74 sentence 6 (the grid connection) prints in Section 1, where L74 is whole
edit("D7",
     "% from main.tex L74, sentence 6, verbatim (as in the design; the sentence also stands in Section 1, where L74 "
     "is whole)\nA grid connection or fabrication bottleneck can occupy the same position over a horizon on which "
     "its capacity is fixed.\n",
     "% Review edit (D7): main.tex L74 sentence 6 (the grid connection), which the design repeated here, is "
     "dropped; it prints in Section 1, where L74 is whole\n",
     None)

# D30: F5's plain sentence prints after Definition 1 and, with its reason, after Lemma A.1
edit("D30",
     " When support absorbs all the owner's income, its first-order condition (Lemma~\\ref{lem:owner}) does not "
     "bind, and the clause selects the user cost at~$\\rho$.",
     "",
     "F5's plain sentence is dropped from this remark; it prints after Definition 1 and, with its reason, in the "
     "remark after Lemma A.1")

# D25: the indifferent workers (math check C4, condition 3)
edit("D25", "Up to the choice of numeraire and sets of tasks of measure zero,",
     "Up to the choice of numeraire and sets of tasks and of workers of measure zero,",
     "\"and of workers\" added: workers indifferent between work and exit have measure zero (math check C4, "
     "condition 3)")

# D73: the model is stationary
edit("D73", "The static model describes prices and limiting configurations.",
     "The stationary model describes prices and limiting configurations.",
     "L553: \"static\" -> \"stationary\" (Section 3 defines a stationary equilibrium with an infinitely lived owner)")

# D74: the vanishing participation claim is Corollary 2's
edit("D74", "tends to zero as wages buy vanishing additional consumption.",
     "tends to zero as wages buy vanishing additional consumption (Corollary~\\ref{cor:vanishing}).",
     "L542 sentence 2: pointer to Corollary 2 added")

# D76: the wedge is in Section 9.2
edit("D76", "are set aside until Section~\\ref{sec:history},", "are set aside until Section~\\ref{sec:stabilizers},",
     "pointer narrowed from Section 9 to Section 9.2, where the wedge is")

# D91: one name for the margin (Definition 2's "interior margin")
for old, new in [
    ("An active contestable margin can coexist with human-required tasks in $H$.",
     "An interior margin can coexist with human-required tasks in $H$."),
    ("An active contestable margin prices each type's wage against machine services.",
     "An interior margin prices each type's wage against machine services."),
    ("If replacement at the active margin drives", "If replacement at the interior margin drives"),
    ("At an active margin against machine $m$, the replacement closure is",
     "At an interior margin against machine $m$, the replacement closure is"),
    ("an active margin satisfies $w/\\gamma_L(x^*)", "an interior margin satisfies $w/\\gamma_L(x^*)"),
    ("replacement applies at each type's active contestable margin.",
     "replacement applies at each type's interior margin."),
]:
    edit("D91", old, new, "\"active (contestable) margin\" -> \"interior margin\", the name Definition 2 gives it")

# D101: D.2's added pair; its second sentence repeats D.2's own
edit("D101",
     "Payroll incidence: the quasi-experimental literature (Gruber 1997; Kugler and Kugler 2009; Saez, Schoefer, and "
     "Seim 2019) provides evidence about labor-demand and participation elasticities. Interpreting incidence in terms "
     "of schedule slope requires accounting for responses in machine prices, output, and participation.",
     "The quasi-experimental literature (Gruber 1997; Kugler and Kugler 2009; Saez, Schoefer, and Seim 2019) "
     "provides evidence about labor-demand and participation elasticities.",
     "the run-in \"Payroll incidence:\" and the second sentence (which repeats D.2's paragraph above) are dropped")

# D102: the CES elasticity no longer shares sigma with the support indicator
appC = ("\\section{Expenditure shares under substitution}", "\\section{Fiscal transition")
seg_a, seg_b = region_bounds(*appC)
n_sig = src[seg_a:seg_b].count("\\sigma")
edit("D102", "\\sigma", "\\varepsilon", None, count=n_sig, region=appC)
edit("D102", "elasticity $\\varepsilon$", "elasticity $\\varepsilon$",
     "the CES elasticity sigma renamed epsilon (sigma is the support indicator of Table 1)")
appE = ("\\section{Human-required tasks}", "\\section{The financing and production accounts}")
seg_a, seg_b = region_bounds(*appE)
n_sigH = src[seg_a:seg_b].count("\\sigma _H")
edit("D102", "\\sigma _H", "\\varepsilon _H", None, count=n_sigH, region=appE)
edit("D102", "Under CES substitution $\\varepsilon _H$", "Under CES substitution $\\varepsilon _H$",
     "the CES elasticity sigma_H renamed epsilon_H, as in Appendix C")

# D106: D.1's comparison sets the instruments of (8) other than the program to zero
edit("D106", "Under \\eqref{eq:utility} and \\eqref{eq:budget}, the utility comparison is",
     "Under \\eqref{eq:utility} and \\eqref{eq:budget} with $\\tau_w=d=0$, the utility comparison is",
     "\"with tau_w = d = 0\" added: the display omits the wage tax and the uniform transfer of (8)")

# D103: the two-item basket's quantities no longer read like payments (g_s beside g_w, g_e)
d3 = ("For a two-item illustration, let the basket contain", "\\subsection{Dependence and fiscal coverage}")
seg_a, seg_b = region_bounds(*d3)
for old, new in [("g_s", "z_g"), ("h_s", "z_h")]:
    n = src[seg_a:seg_b].count(old)
    edit("D103", old, new, None, count=n, region=d3)
    seg_a, seg_b = region_bounds(*d3)
edit("D103", "let the basket contain $z_g>0$ units", "let the basket contain $z_g>0$ units",
     "the basket quantities g_s, h_s renamed z_g, z_h (g_s read like a payment beside g_w, g_e; z is the basket)")
edit("D103", "adding $n_s$ hours of care priced at $w_H$ to the two-item basket gives $P_s=pg_s+rh_s+w_Hn_s$",
     "adding $z_H$ hours of care priced at $w_H$ to the two-item basket gives $P_s=pz_g+rz_h+w_Hz_H$",
     "n_s, g_s, h_s renamed z_H, z_g, z_h, as in Appendix D.3")

open(PATH, "w", encoding="utf-8").write(src)
print("written", PATH)
