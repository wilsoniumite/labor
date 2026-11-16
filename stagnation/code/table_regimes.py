# table_regimes.py — Table B.1: the instance under the four rules for who can leave work, from code/model.py.
# Writes paper/tables/tab_regimes.tex (a tabular, \input by main.tex); checks/check_theory.py rebuilds the text with
# rows() and compares it with the file.
# Run from stagnation/:  ../venv/bin/python code/table_regimes.py
from pathlib import Path

import numpy as np

import model as M

ORDER = (("funded", "Funded exit"), ("conditioned", "Conditioned support"), ("quarter", "Quarter enclosed"),
         ("enclosed", "All enclosed"))
OUT = Path(__file__).resolve().parents[1] / "paper" / "tables" / "tab_regimes.tex"


def ceiling_text(c):
    return r"$\infty$" if not np.isfinite(c) else (f"{c:.2f}" if c < 10 else f"{c:.1f}")


def rows(P=M.BASE):
    out = []
    for key, name in ORDER:
        PP = M.with_(P, **M.REGIMES[key])
        q = M.solve(PP)
        out.append(" & ".join([
            name, f"{PP['theta']:g}", f"{PP['Delta']:g}", f"{q['x']:.3f}", f"{q['participation']:.2f}",
            f"{q['Y']:.2f}", f"{q['pi']:.2f}", f"{q['omega']:.2f}", f"{q['labor_share']:.2f}",
            ceiling_text(M.pi_ceiling(PP)), f"{q['support'] / q['provider_income']:.2f}"]) + r" \\")
    return out


def table_text(P=M.BASE):
    head = (r"{\footnotesize\setlength{\tabcolsep}{4.5pt}" "\n" r"\begin{tabular}{l c c c c c c c c c c}" "\n"
            r"\toprule" "\n"
            r"Rule & $\theta$ & $\Delta$ & $x^*$ & $N_a/N$ & $Y$ & $Y/N_a$ & $w/P_s$ & \shortstack{Labor's\\share} & "
            r"\shortstack{Ceiling\\$T/(hN_\infty)$} & \shortstack{Support/\\income} \\" "\n" r"\midrule")
    foot = (r"\bottomrule" "\n" r"\end{tabular}" "\n"
            r"\par\smallskip\parbox{0.95\linewidth}{\footnotesize Output $Y$ in baskets; $Y/N_a$ is output per hour;"
            r" labor's share is $wN_a/(P_sY)$; $T/(hN_\infty)$ is the ceiling of Proposition~\ref{prop:2}; the last"
            r" column is the cost of support, $P_s[(1-\theta)N+\Delta N_a]$, over the provider's rent and interest,"
            r" $rT+\rho V_mX$ (funded when at most one).}" "\n" r"}")
    return "\n".join([head, *rows(P), foot]) + "\n"


if __name__ == "__main__":
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(table_text())
    print(OUT.read_text())
