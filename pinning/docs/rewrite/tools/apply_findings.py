"""apply_findings.py — the fixes from the checks workflow (build/checks/journal_results.json), applied after
apply_defaults.py. Each edit leaves a "% Review edit (<id>): ..." comment before its paragraph.

    python3 -B apply_findings.py REWRITE.tex
"""
import re
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


def edit(tag, old, new, note, regex=False):
    """Replace exactly one occurrence of old (a literal, or a regex if regex=True) and note it."""
    global src
    if regex:
        ms = list(re.finditer(old, src))
        assert len(ms) == 1, f"{tag}: expected 1 match, found {len(ms)}: {old[:80]!r}"
        m = ms[0]
        first = m.start()
        src = src[:m.start()] + m.expand(new) + src[m.end():]
    else:
        n = src.count(old)
        assert n == 1, f"{tag}: expected 1 occurrence, found {n}: {old[:80]!r}"
        first = src.find(old)
        src = src.replace(old, new)
    if note:
        ps = para_start(src, first)
        src = src[:ps] + f"% Review edit ({tag}): {note}\n" + src[ps:]
    print(f"{tag}: done")


# ---- math checks
edit("mathA-1", "the owner's first-order condition (Lemma~\\ref{lem:owner}).",
     "the owner's first-order condition whenever it consumes and holds machines (Lemma~\\ref{lem:owner}(c)).",
     "the user cost is the owner's first-order condition only when it consumes and holds machines (Lemma A.1(c)); "
     "the sentence no longer says so unconditionally, which contradicted F5's sentences")
edit("mathA-2", "the constant plan is the owner's only feasible plan, since any departure from it leaves",
     "the owner has no feasible plan with other consumption or stock, since any such departure leaves",
     "at zero rent the owner can vary the land it rents out, so the constant plan is not its only feasible plan; "
     "what the shortfall argument proves is that no feasible plan has other consumption or stock")
edit("mathA-3", "are no larger than the price coefficients (Lemma~\\ref{lem:prices}).",
     "are no larger than the price coefficients (Lemma~\\ref{lem:prices}(iii) for the basket; "
     "Proposition~\\ref{prop:network}(a) for every good).",
     "pointer completed: Lemma 1(iii) compares the basket only; Proposition B.1(a) compares every good")
edit("mathA-4", "final-task labor demand is $Y\\int_{x^*}^1dx/\\gamma_L(x)$",
     "final-task labor demand is $N_F=Y\\int_{x^*}^1dx/\\gamma_L(x)$",
     "L627: the symbol N_F, used in the next sentence, is attached to final-task labor demand (it was undefined, "
     "as in main.tex)")
edit("mathB-1", "The minimum is one on human-required tasks.",
     "The minimum is taken to be one on human-required tasks, including tasks reserved by rule.",
     "L663: tasks reserved by rule can have a finite gamma, so the minimum is one there by convention, not by "
     "arithmetic")
edit("mathB-2", "Proposition~\\ref{prop:4} gives $r/p\\ge1/[(w/r)\\bar\\lambda_0]$",
     "\\eqref{eq:13} gives $r/p\\ge1/[(w/r)\\bar\\lambda_0]$",
     "L763: the pointer moves from Proposition 4, which now states only the final good's bound, to (13), the "
     "general human-method bound")
edit("mathB-3", "When the funded-support conditions for \\eqref{eq:14} also hold",
     "When the conditions for \\eqref{eq:14} also hold",
     "L393: \"funded-support\" dropped; Corollary 2 no longer has a funding hypothesis (funding is in Definition 1)")
edit("mathB-4", "Let the government tax the rental value of land at $\\tau_R\\in[0,1]$ and pay $d=\\tau_RrT/N$ to every worker,",
     "Let the government tax the rental value of land, $R=rT$, at $\\tau_R\\in[0,1]$ and pay $d=\\tau_RR/N$ to every "
     "worker,",
     "R is defined where it is first used (it was defined only in Corollary 3)")
edit("mathB-5", "because $\\widetilde\\lambda_g\\ge0$",
     "because $p=w\\widetilde\\lambda_g+r\\widetilde b_g$ with $\\widetilde\\lambda_g=1-x^*+\\widetilde\\lambda_mJ(x^*)\\ge0$",
     "the final good's hour coefficient is defined where the proof uses it")
edit("mathB-6", "Automation can therefore change $\\mathbf{A}$, $\\bm{\\lambda}$, and $\\mathbf{b}$",
     "Automation can therefore change $\\mathbf{A}_\\rho$, $\\bm{\\lambda}$, and $\\mathbf{b}$",
     "L221: the input matrix is written A_rho, as everywhere else in the rewrite")

# ---- sources
edit("S1",
     "In these models machines are accumulated from output, so automating every task also automates the\nmaking of "
     "machines.",
     "In the first two of these models machines are accumulated from output, so automating every task also\n"
     "automates the making of machines; in the third the stock of machines is given.",
     "Korinek and Juelfs (2022) take the machine stock as given (w30172: \"a given amount of the other factors of "
     "the economy, here captured by machines m\"); only the first two papers accumulate machines from output")
edit("S2",
     "Restrepo (2025) finds that wages converge to the opportunity cost of computational resources required to "
     "reproduce human work.",
     "Restrepo (2025) finds that ``wages converge to the opportunity cost of computational resources required to "
     "reproduce human work''.",
     "quotation marks: the fourteen words are w34423's abstract, item (iv), verbatim")

# ---- numbers
edit("N1", r"as the task margin moves over the tasks open to machines\.",
     r"as the task margin moves over the tasks open to machines below the ceiling $x_c$.",
     "Figure 3's caption: the curves stop at the ceiling x_c; tasks above it are open to machines in the "
     "rewrite's terms (Assumption 1, Lemma 2)", regex=True)
edit("N2", "For a numerical instance, Table~\\ref{tab:instance} lists the parameters and the shares they are set to match.",
     "For a numerical instance, Table~\\ref{tab:instance} lists the parameters and the targets they are set to match.",
     "\"shares\" -> \"targets\": one of the seven, baskets per worker, is a level")

# R04: the NEW sentence moves after the shares sentence, so that "These values" again follows the parameters
block_re = re.compile(r"(% NEW: the primitives Table 2 does not list\..*?\nIn the instance, \$H\$ is empty \(\$x_H=1\$\), "
                      r"every instrument is zero, and the owner provides support\.\n)", re.S)
ms = list(block_re.finditer(src))
assert len(ms) == 1, "R04: block not found once"
block = ms[0].group(1)
src = src[:ms[0].start()] + src[ms[0].end():]
anchor = "site rent is 6.5 percent of the basket; participation is 60 percent.\n"
assert src.count(anchor) == 1, "R04: anchor"
src = src.replace(anchor, anchor + "% Review edit (R04): moved here from before \"These values are illustrative.\", so "
                  "that \"These values\" follows the parameters again\n" + block)
print("R04: done")

# ---- read-through
edit("R02", "If the interior conditions continue to hold", "If \\eqref{eq:25} and funding continue to hold",
     "L743: \"the interior conditions\" named Lemma B.1's hypotheses, now (22) and funding (Corollary 1(ii))")
edit("R08", "At given wages, rents, and total human requirements, a lower $\\widetilde b_i$ reduces the price.",
     "At given wages, rents, and $\\widetilde\\lambda_i$, a lower $\\widetilde b_i$ reduces the price.",
     "L351: \"total human requirements\" (a name the rewrite no longer defines) -> the symbol")
edit("R09", "final quantities when total human requirements fall;", "final quantities when $\\widetilde{\\bm{\\lambda}}$ falls;",
     "L908: \"total human requirements\" -> the symbol")
edit("R10", "The owner lives forever and\ndiscounts the future, so a machine must earn a return to be worth holding.",
     "The owner lives forever and\nmay discount the future, in which case a machine must earn a return to be worth "
     "holding.",
     "Assumption 5 admits beta = 1, at which a machine earns no return (the flow benchmark)")
edit("R11", "each inactive until Section~\\ref{sec:rent} or Appendix~\\ref{app:D} uses it",
     "each inactive until Corollary~\\ref{cor:vanishing}, Section~\\ref{sec:rent}, or Appendix~\\ref{app:D} uses it",
     "Corollary 2 already admits payments and the wage tax")
edit("R12", "An unconditional payment $g_w=g_e=d$ gives $\\Delta=0$ and the reservation wage $(e^\\chi-1)(P_s+d)$.",
     "An unconditional payment $g_w=g_e$ gives $\\Delta=0$ and the reservation wage $(e^\\chi-1)(P_s+g_e)$.",
     "L787: d is the uniform transfer of (8), set to zero above (D106), so the common payment is written g_e")
edit("R15", "Use the same basic living basket as in Section~\\ref{sec:workers}",
     "Use the same basket as in Section~\\ref{sec:workers}",
     "\"basic living basket\" was defined only in main.tex L913, which the rewrite cuts; Table 1 calls it the basket")
edit("R16", "Human-required services also enter the basic living basket through $\\mathbf{z}$.",
     "Human-required services also enter the basket through $\\mathbf{z}$.",
     "\"basic living basket\" -> \"basket\", as in D.3")
edit("R17", "Maintaining that support requires resources from the provider.",
     "Maintaining that support requires resources from the owner or the government.",
     "L296: \"the provider\" -> the two agents that can provide support in the rewrite")
edit("R18", "outside the two-factor flow benchmark.", "outside the flow benchmark.",
     "L257: \"two-factor\" dropped, the flow benchmark being defined in Section 3.1 (as at L393, D40)")
edit("R19", r"On the machine-contestable set,", "On the open tasks,",
     "Figure 1's caption: \"machine-contestable set/task\" -> \"open tasks/task\", Assumption 1's name")
edit("R19b", r"holds no machine-contestable task,", "holds no open task,", None)
edit("R20", "and space has $\\widetilde b_h=1$.", "and space, which rents at $r$, has $\\widetilde b=1$.",
     "the subscript h, defined only in Appendix B.1, is dropped")
edit("R21", "where $\\pi=(\\rho+\\delta)b/[1-(\\rho+\\delta)a]$", "where $\\pi=(\\rho+\\delta)b/[1-(\\rho+\\delta)a]=\\widetilde b_m$",
     "pi is identified with b~_m of (5)")
edit("R22", r"embodied rent costs\s+impose a ceiling", "embodied rent costs impose an upper bound",
     "abstract: \"a ceiling\" -> \"an upper bound\", since x_c is \"the ceiling\" in the body (Lemma 2)", regex=True)
edit("R23", " With payments, Appendix~\\ref{app:D.1} gives the reservation wage.", "",
     "the NEW pointer is dropped; the authors' paragraph below gives the same pointer")
edit("R24", "\\textbf{Land.}\n\n\\begin{assumption}[land]", "\\begin{assumption}[land]",
     "the run-in head \"Land.\" is dropped: it printed alone at a page foot, and the assumption is titled (land)")
edit("L1404", r"(?m)^If the trained worker and the entrant both held contestable margins against the same machine",
     "If the trained worker and the entrant both held interior margins against the same machine",
     "\"contestable margins\" -> \"interior margins\", as D91", regex=True)

# R25: Table 1 moves next to its first mention
tab_re = re.compile(r"\n% NEW \(design synthesis §2\.2\): Table 1\n\\begin\{table\}\[htbp\].*?\\end\{table\}\n", re.S)
ms = list(tab_re.finditer(src))
assert len(ms) == 1, "R25: table block"
tab = ms[0].group(0)
src = src[:ms[0].start()] + "\n" + src[ms[0].end():]
anchor = "Table~\\ref{tab:notation} collects the notation.\n"
assert src.count(anchor) == 1, "R25: anchor"
src = src.replace(anchor, anchor + "% Review edit (R25): Table 1 moved here from the end of Section 3.6, next to its "
                  "first mention" + tab.rstrip("\n").replace("\n% NEW (design synthesis §2.2): Table 1", "\n% NEW (design "
                  "synthesis §2.2): Table 1", 1) + "\n")
print("R25: done")

open(PATH, "w", encoding="utf-8").write(src)
print("written", PATH)
