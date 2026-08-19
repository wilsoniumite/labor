# census_symbols.py — defined-symbol census over paper/pinning.html for the
# SYMBOLS EARN THEIR INK rule (brief, 2026-08-19): every defined symbol's
# occurrence count, so single-use definitions are found mechanically, not by
# hand inventory (the ADDENDUM-7 lesson). Informational, not pass/fail:
# a low count is a flag to inline/rework, not automatically a defect —
# formula-bearing one-sentence symbols (v*f/(1-v), eps_D/(eps_D+eps_S)) stay.
# Run: ../venv/Scripts/python.exe checks/census_symbols.py  (from the-link-revision/)

import re, os

HERE = os.path.dirname(os.path.abspath(__file__))
PAPER = os.path.join(HERE, "..", "paper", "pinning.html")
html = open(PAPER, encoding="utf-8").read()
body = html[html.index("<body>"):html.index('<h2 style="page-break-before: auto;">References')]
# normalize away the italic-variable markup (2026-08-19) so patterns match
body = body.replace("<i>", "").replace("</i>", "")

def lineno(pos):
    return html[:html.index("<body>") + pos].count("\n") + 1

SYMBOLS = {
    "v (verification power, App G)":    [r"verification power v", r"v&middot;f", r"every v &lt; 1"],
    "f (fraud penalty, App G)":         [r"fraud penalty f", r"\bf &rarr; 0", r"v&middot;f"],
    "beta (broadcast fraction, App G)": [r"&beta;"],
    "k (measure of K, App G)":          [r"measure k\b", r"k&middot;w", r"at k = 0"],
    "w_K (K-wage)":                     [r"w<sub>K</sub>"],
    "eta (CES elasticity)":             [r"&eta;"],
    "Delta (conditionality, F.1)":      [r"&Delta;"],
    "eps_D/eps_S (elasticities, F.2)":  [r"&epsilon;<sub>D</sub>", r"&epsilon;<sub>S</sub>"],
    "t (wage tax rate, S8)":            [r"rate t\b", r"\(1&minus;t\)", r"t&middot;c"],
    "omega_ij (ownership shares, S8)":  [r"&omega;"],
    "tau (rent tax rate, S8)":          [r"&tau;"],
    "P (geometric index, Prop 4iii)":   [r"index P =", r"w/P\b"],
    "w_f (foreign wage, App H)":        [r"w<sub>f</sub>"],
    "rho_f (rel. prod. vs foreign, H)": [r"&rho;<sub>f</sub>"],
    "delta (time preference, App C)":   [r"&delta;"],
    "d (wear rate, App C)":             [r"rate d\b", r"&delta;\+d", r"&delta; \+ d"],
    "X (gross machine services, D.1)":  [r"X =", r"aX\b", r"&#8467;X"],
    "z (parcel index, D.1)":            [r"r\(z\)"],
    "n (participant count, App A)":     [r"\(n\)", r"with n the", r"in n\b", r"n &gt; 1"],
    "q_enc (F.4)":                      [r"q<sub>enc</sub>"],
    "q* (coverage threshold, F.3)":     [r"q\*"],
    "g_s (bundle goods, F.3)":          [r"g<sub>s</sub>"],
    "h_s (bundle land, F.3)":           [r"h<sub>s</sub>"],
    "P_s (bundle cost, F.3)":           [r"P<sub>s</sub>"],
    "kappa (coverage)":                 [r"&kappa;"],
    "lam_C (F.5)":                      [r"&lambda;<sub>C</sub>"],
    "lam_R (F.5)":                      [r"&lambda;<sub>R</sub>"],
    "s_0 (keep, S5)":                   [r"s<sub>0</sub>"],
    "s_d (dependency floor, S5)":       [r"s<sub>d</sub>"],
    "h_e (exit land, S5)":              [r"h<sub>e</sub>"],
    "s(q) (exit value, S5)":            [r"s\(q\)"],
    "L_bar (S7)":                       [r"L&#772;"],
    "rho_bar (S7)":                     [r"&rho;&#772;"],
    "rho* (S3)":                        [r"&rho;\*"],
    "x* (S3)":                          [r"x\*"],
    "gamma_L (S3)":                     [r"&gamma;<sub>L</sub>"],
    "gamma_M (S3)":                     [r"&gamma;<sub>M</sub>"],
    "p_g (goods price)":                [r"p<sub>g</sub>"],
    "mu (wedge, App B)":                [r"&micro;"],
    "rho_tilde (App B)":                [r"&rho;&#771;"],
    "sigma (expenditure share)":        [r"&sigma;"],
    "T_H / T_P (App D)":                [r"T<sub>H</sub>", r"T<sub>P</sub>"],
    "T_j / r_j (S8)":                   [r"T<sub>j</sub>", r"r<sub>j</sub>"],
    "K (task set)":                     [r"(?<![A-Za-z])K(?![A-Za-z])", r"K-"],
    "m_w/m_e (transfer pair, A/F.1)":   [r"m<sub>w</sub>", r"m<sub>e</sub>"],
    "k_s (bundle K-service, GxF)":      [r"k<sub>s</sub>"],
    # dead symbols — counts must stay ZERO (killed 2026-08-19; the transfer
    # pair m_w/m_e was killed then REVIVED same day with a defining home in
    # Appendix A's government block and a derivation in F.1)
    "DEAD m (per-task cost, was App G)":   [r"cost m &rarr;", r"as m &rarr;", r"vanishes with m", r"collapses with m"],
    "DEAD phi_H (was App G)":              [r"&phi;"],
    "DEAD b/b-prime (was F.1)":            [r"= b &gt; 0", r"part of b\b", r"&minus;b&prime;"],
    "DEAD y / s(y) (was F.1)":             [r"s\(y\)", r"cash y\b"],
}

print(f"{'symbol':<38} {'hits':>4}   lines")
print("-" * 72)
rows = []
for name, pats in SYMBOLS.items():
    spans = sorted({mt.start() for p in pats for mt in re.finditer(p, body)})
    lines = sorted({lineno(s) for s in spans})
    rows.append((len(spans), name, lines))
dead_fail = False
for nhits, name, lines in sorted(rows):
    listing = ",".join(map(str, lines[:8])) + ("..." if len(lines) > 8 else "")
    print(f"{name:<38} {nhits:>4}   {listing}")
    if name.startswith("DEAD") and nhits:
        dead_fail = True

print()
if dead_fail:
    print("FAIL: a killed symbol has returned to the body.")
    raise SystemExit(1)
print("dead symbols all zero; counts above are informational")
