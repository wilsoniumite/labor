# check_rewrite_numbers.py — recompute every number printed in Sections 5, 6 and 7, Table 2, Figure 3's caption and Appendix D of
# the rewrite (paper/main_rewrite.tex) from the repository's code/appendix_b.py (imported read-only), and compare it
# with the printed value. Tasks 2 and 3 of the numbers check. Run from pinning/:  python3 checks/check_rewrite_numbers.py
# Prints one line per number: OK or MISMATCH, printed vs recomputed.

import math
import re
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
import appendix_b as B  # noqa: E402

REWRITE = ROOT / "paper" / "main_rewrite.tex"
RAW = REWRITE.read_text(encoding="utf-8")
LINES = RAW.split("\n")
OUT = []


def line_of(snippet):
    hits = [i + 1 for i, l in enumerate(LINES) if snippet in l and not l.lstrip().startswith("%")]
    return hits


def report(label, printed, value, ok, where):
    lines = line_of(where) if where else []
    s = f"{'OK      ' if ok else 'MISMATCH'} L{','.join(map(str, lines)) or '?'}: {label}: printed {printed}, recomputed {value}"
    OUT.append((ok, s))
    print(s)


def rounds_to(printed, value, places=None):
    """True if value rounds to the printed decimal string (half-up at the printed number of places)."""
    p = printed.strip()
    places = len(p.split(".")[1]) if "." in p else 0 if places is None else places
    return abs(value - float(p)) <= 0.5 * 10 ** (-places) + 1e-12


P = B.PRINTED
q = B.solve(P)
sh = B.shares(P, q)
cpt = P["rho"] + P["delta"]

# ------------------------------------------------------------------ Table 2: parameters against PRINTED
print("== Table 2 parameters against code/appendix_b.py PRINTED")
tab = {"N": ("1", P["N"]), "T": ("0.01", P["T"]), "h": ("0.0017", P["h"]), "a": ("1.4", P["a"]), "lam": ("7.3", P["lam"]),
       "b": ("0.4", P["b"]), "delta": ("0.05", P["delta"]), "rho": ("0.09", P["rho"]), "g0": ("0.01", P["g0"] * P["eta"]),
       "g1": ("0.99", P["g1"] * P["eta"]), "k": ("4.4", P["k"]), "chi_max": ("2.2", P["chi_max"])}
for k_, (pr, val) in tab.items():
    report(f"Table 2 parameter {k_}", pr, val, float(pr) == val, None)
report("Table 2 caption: gamma(0) and gamma(1) are set (gamma(0) = g0, gamma(1) = g0 + g1)", "0.01; 1",
       f"{B.gamma(P, 0.0):.6g}; {B.gamma(P, 1.0):.6g}", B.gamma(P, 0.0) == 0.01 and abs(B.gamma(P, 1.0) - 1.0) < 1e-15, None)
report("eta (Table 2 has no eta row; gamma is printed with eta = 1)", "1 (implicit)", P["eta"], P["eta"] == 1.0, None)
report("Table 2's twelve parameters are all of PRINTED's thirteen keys but eta", "12 + eta",
       sorted(P), set(P) == set(tab) | {"eta"}, None)

# ------------------------------------------------------------------ Table 2: the last column at the rounded parameters
print("== Table 2 'at the rounded parameters'")
col = [("labor's share of a machine's cost", "0.456", sh["theta_V"], "labor's share of a machine's cost & $0.47$ & $0.456$"),
       ("machine services' share of a machine's cost", "0.196", sh["machines"], "& $0.20$ & $0.196$"),
       ("final-task labor's share of a basket's cost", "0.469", sh["labor"], "& $0.47$ & $0.469$"),
       ("site's share of a basket's cost", "0.065", sh["site"], "& $0.06$ & $0.065$"),
       ("machine production's share of hours", "0.148", sh["chain"], "& $0.15$ & $0.148$"),
       ("participation N_a/N", "0.602", q["participation"], "& $0.60$ & $0.602$"),
       ("baskets per worker Y/N", "3.01", q["Y"] / P["N"], "& $3$ & $3.01$")]
for lab, pr, val, where in col:
    report(lab, pr, f"{val:.6f}", rounds_to(pr, val), where)
# the shares as the paper defines them, recomputed from first principles (not from shares())
Vm = q["Vm"]
report("labor's share of a machine's cost = lambda w / V_m (V_m = a p_m + lambda w + b r)", "0.456",
       f"{P['lam'] * q['v'] / (P['a'] * q['pm'] + P['lam'] * q['v'] + P['b']):.6f}",
       rounds_to("0.456", P['lam'] * q['v'] / (P['a'] * q['pm'] + P['lam'] * q['v'] + P['b'])), "& $0.47$ & $0.456$")
report("machine services' share of a machine's cost = a p_m / V_m", "0.196", f"{P['a'] * q['pm'] / Vm:.6f}",
       rounds_to("0.196", P['a'] * q['pm'] / Vm), "& $0.20$ & $0.196$")
report("final-task labor's share of a basket's cost = w(1 - x*)/P_s", "0.469", f"{q['v'] * (1 - q['x']) / q['Ps']:.6f}",
       rounds_to("0.469", q['v'] * (1 - q['x']) / q['Ps']), "& $0.47$ & $0.469$")
report("site's share of a basket's cost = h r / P_s", "0.065", f"{P['h'] / q['Ps']:.6f}", rounds_to("0.065", P['h'] / q['Ps']),
       "& $0.06$ & $0.065$")
report("machine production's share of hours = lambda delta X / N_a", "0.148",
       f"{P['lam'] * P['delta'] * q['X'] / q['n']:.6f}", rounds_to("0.148", P['lam'] * P['delta'] * q['X'] / q['n']),
       "& $0.15$ & $0.148$")

# ------------------------------------------------------------------ Table 2: the targets and the calibration
print("== Table 2 targets: calibrate the seven free parameters to the seven targets (independent of the code's notes)")
TGT = dict(theta=0.47, mach=0.20, lab=0.47, site=0.06, chain=0.15, part=0.60, ypn=3.0)
SET = dict(N=1.0, b=0.4, delta=0.05, g0=0.01, g1=0.99, eta=1.0)       # gamma(0) = 0.01, gamma(1) = 1


def calibrate(kroot):
    """Closed-form calibration given the curvature root k. From the targets: the chain share, participation and Y/N give
    1 - x = (n/Y)(1 - chain) = 0.2 * 0.85; the basket shares give J(x) = gamma(x)(1 - x); the build-cost shares give
    V_m = b/(1 - mach - theta); the chain share gives rho + delta; then a, lambda, h, T, chi_max follow."""
    N, b, d = SET["N"], SET["b"], SET["delta"]
    npy = TGT["part"] * N / (TGT["ypn"] * N)           # N_a / Y
    x = 1 - npy * (1 - TGT["chain"])
    g = SET["g0"] + SET["g1"] * x ** kroot
    J = SET["g0"] * x + SET["g1"] * x ** (kroot + 1) / (kroot + 1)
    Vm = b / (1 - TGT["mach"] - TGT["theta"])
    # lambda delta J/(1 - a delta) = npy * chain; lambda = theta Vm / v, v = g (rho+delta) Vm; a = mach/(rho+delta)
    # => theta delta J / (g ((rho+delta) - mach delta)) = npy chain
    c = TGT["theta"] * d * J / (g * npy * TGT["chain"]) + TGT["mach"] * d       # = rho + delta
    rho = c - d
    a = TGT["mach"] / c
    v = g * c * Vm
    lam = TGT["theta"] * Vm / v
    Ps = v * (1 - x) / TGT["lab"]
    h = TGT["site"] * Ps
    Bs = h + b * d * J / (1 - a * d)
    T = TGT["ypn"] * N * Bs
    chi = math.log1p(v / Ps) / TGT["part"]
    return dict(N=N, T=T, h=h, a=a, b=b, lam=lam, g0=SET["g0"], g1=SET["g1"], k=kroot, eta=1.0, chi_max=chi, rho=rho, delta=d), \
        dict(x=x, J_minus_g1mx=J - g * (1 - x))


def root_eq(kk):
    x = 1 - (TGT["part"] / TGT["ypn"]) * (1 - TGT["chain"])
    g = SET["g0"] + SET["g1"] * x ** kk
    J = SET["g0"] * x + SET["g1"] * x ** (kk + 1) / (kk + 1)
    return J - g * (1 - x)


ks = np.exp(np.linspace(np.log(1e-3), np.log(1e4), 200001))
fv = np.array([root_eq(kk) for kk in ks])
sign_changes = np.flatnonzero(np.diff(np.sign(fv)) != 0)
roots = [brentq(root_eq, ks[i], ks[i + 1], xtol=1e-14) for i in sign_changes]
report("number of curvatures k in [1e-3, 1e4] that match the targets ('the two curvatures')", "2", len(roots),
       len(roots) == 2, "Of the two curvatures")
report("the lower root, printed in Table 2 as k = 4.4 (two significant figures)", "4.4", f"{roots[0]:.6f}",
       f"{roots[0]:.2g}" == "4.4", None)
report("the other root, 'about 15.5'", "15.5", f"{roots[1]:.6f}", rounds_to("15.5", roots[1]), "about $15.5$")
cal, aux = calibrate(roots[0])
qc = B.solve(cal)
shc = B.shares(cal, qc)
hit = dict(theta=shc["theta_V"], mach=shc["machines"], lab=shc["labor"], site=shc["site"], chain=shc["chain"],
           part=qc["participation"], ypn=qc["Y"] / cal["N"])
report("the calibrated economy (lower root) hits all seven targets (1e-9)", str(TGT), {k_: round(v_, 10) for k_, v_ in hit.items()},
       all(abs(hit[k_] - TGT[k_]) < 1e-9 for k_ in TGT), None)
print("   calibrated (unrounded):", {k_: (round(v_, 7) if isinstance(v_, float) else v_) for k_, v_ in cal.items()})
for k_ in ("T", "h", "a", "lam", "k", "chi_max"):
    pr = {"T": "0.01", "h": "0.0017", "a": "1.4", "lam": "7.3", "k": "4.4", "chi_max": "2.2"}[k_]
    report(f"calibrated {k_} rounds to Table 2's {pr} at two significant figures", pr, f"{cal[k_]:.6g}",
           float(f"{cal[k_]:.2g}") == float(pr), None)
report("calibrated rho rounds to Table 2's 0.09 at two decimal places (caption: 'rho to two decimal places')", "0.09",
       f"{cal['rho']:.6g}", round(cal["rho"], 2) == 0.09, None)
report("calibrated rho at two significant figures would print as 0.093 (why the caption's parenthesis is needed)", "0.093",
       f"{cal['rho']:.2g}", f"{cal['rho']:.2g}" == "0.093", None)

# the other root: does task automation (gamma halved) raise w/P_s there?
cal2, _ = calibrate(roots[1])
for tag, PP in (("unrounded", cal2),
                ("rounded to two significant figures, rho to two decimals",
                 {**cal2, **{k_: float(f"{cal2[k_]:.2g}") for k_ in ("T", "h", "a", "lam", "k", "chi_max")},
                  "rho": round(cal2["rho"], 2)})):
    try:
        b0, b1 = B.solve(PP), B.solve({**PP, "eta": 0.5})
        rise = b1["real_wage"] / b0["real_wage"] - 1
        report(f"at the other root ({tag}), halving gamma raises w/P_s", "raises", f"{100 * rise:+.2f} percent",
               rise > 0, "task automation raises $w/P_s$")
    except ValueError as e:
        report(f"at the other root ({tag}), halving gamma raises w/P_s", "raises", f"no interior equilibrium: {e}", False, None)
b0, b1 = B.solve(cal), B.solve({**cal, "eta": 0.5})
report("at the lower root (unrounded), halving gamma lowers w/P_s (so the choice matters)", "lowers",
       f"{100 * (b1['real_wage'] / b0['real_wage'] - 1):+.2f} percent", b1["real_wage"] < b0["real_wage"], None)

# ------------------------------------------------------------------ Section 7: the instance
print("== Section 7, the instance")
for lab, pr, val, where in (
        ("site rent percent of the basket", "6.5", 100 * sh["site"], "site rent is 6.5 percent"),
        ("participation percent", "60", 100 * q["participation"], "participation is 60 percent"),
        ("x*", "0.82987", q["x"], "x^*\\simeq0.82987"), ("x_c", "0.94634", q["x_ceiling"], "x_c\\simeq0.94634"),
        ("v", "0.07165", q["v"], "v\\simeq0.07165"), ("Y", "3.01320", q["Y"], "Y\\simeq3.01320"),
        ("N_a", "0.60165", q["n"], "N_a\\simeq0.60165"), ("final-task hours", "0.51264", q["final_hours"], "0.51264"),
        ("machine-production hours", "0.08902", q["chain_hours"], "0.08902"),
        ("N P_s", "0.02599", q["support"], "NP_s\\simeq0.02599"), ("owner's rent and interest", "0.03520", q["provider_income"], "0.03520")):
    report(lab, pr, f"{val:.6f}", rounds_to(pr, val), where)
report("'about half' of build cost (0.4-0.6)", "about half", f"{sh['theta_V']:.4f}", 0.4 <= sh["theta_V"] <= 0.6, "about half")
report("'about half' of the cost of a basket at final tasks (0.4-0.6)", "about half", f"{sh['labor']:.4f}",
       0.4 <= sh["labor"] <= 0.6, "about half")
report("'about a fifth' of build cost (0.15-0.25)", "about a fifth", f"{sh['machines']:.4f}", 0.15 <= sh["machines"] <= 0.25,
       "about a fifth")
report("x* below the ceiling", "x* < x_c", f"{q['x']:.5f} < {q['x_ceiling']:.5f}", q["x"] < q["x_ceiling"], None)
report("support funded at the instance (NP_s <= rent + interest)", "funded", q["funded"], q["funded"], None)
fullchain = q["v"] * q["L_s"] / q["Ps"]
print(f"   (for reference: labor's full-chain share of a basket's cost on physical requirements, w L_s/P_s = {fullchain:.4f};"
      f" on price coefficients, w lambda~_s/P_s = {q['v'] * (1 - q['x'] + cpt * P['lam'] * q['J'] / (1 - cpt * P['a'])) / q['Ps']:.4f})")

# ------------------------------------------------------------------ Figure 3 caption
print("== Figure 3 caption")
f3 = B.figure3(P)
for s, wp, na in (("baseline", "2.76", "0.60"), ("recursive", "2.46", "0.56"), ("task", "2.66", "0.59")):
    report(f"{s} w/P_s", wp, f"{f3[s]['real_wage']:.6f}", rounds_to(wp, f3[s]["real_wage"]), None)
    report(f"{s} N_a/N", na, f"{f3[s]['participation']:.6f}", rounds_to(na, f3[s]["participation"]), None)
report("participation curve divisor = chi_max", "2.2", P["chi_max"], P["chi_max"] == 2.2, None)
report("both channels lower w/P_s and N_a/N ('In that example, both automation channels lower ...')", "both lower",
       {s: (round(f3[s]["real_wage"], 4), round(f3[s]["participation"], 4)) for s in f3},
       all(f3[s]["real_wage"] < f3["baseline"]["real_wage"] and f3[s]["participation"] < f3["baseline"]["participation"]
           for s in ("recursive", "task")), "both automation channels lower")

# ------------------------------------------------------------------ Section 7, the path
print("== Section 7, the automation path (lambda = 0, gamma scaled by eta)")
pi = cpt * P["b"] / (1 - cpt * P["a"])
report("pi = (rho+delta) b/[1-(rho+delta)a] (= sequence_bound)", "(symbol)", f"{pi:.7f}", abs(pi - B.sequence_bound(P)) < 1e-15, None)
eta_star = (P["T"] - P["N"] * P["h"]) / (P["N"] * pi)
report("(T - Nh)/(N pi), 'about 0.12 here'", "0.12", f"{eta_star:.6f}", rounds_to("0.12", eta_star), "about $0.12$ here")
path = {e: B.solve(B.sequence(P, e)) for e in (1.0, 0.01, 0.001, 1e-4)}
for e, pr, where in ((1.0, "0.56", "it is $0.56$ at $\\eta=1$"), (0.01, "0.13", "$0.13$ at $\\eta=0.01$"),
                     (0.001, "0.018", "At $\\eta=0.001$ it is $0.018$")):
    report(f"participation at eta = {e}", pr, f"{path[e]['participation']:.6f}", rounds_to(pr, path[e]["participation"]), where)
r_wp = (path[0.001]["v"] / path[0.001]["p"]) / (path[1.0]["v"] / path[1.0]["p"])
r_wr = path[1.0]["v"] / path[0.001]["v"]
report("w/p from eta = 1 to 0.001: '1.8 times as much of the final good'", "1.8", f"{r_wp:.5f}", rounds_to("1.8", r_wp),
       "1.8$ times")
report("w/r from eta = 1 to 0.001: '1/426 as much space'", "1/426", f"1/{r_wr:.3f}", round(r_wr) == 426, "1/426")
etas = np.exp(np.linspace(np.log(1e-4), 0.0, 2001))
ok_ps = ok_x = ok_fund = ok_rent = ok_v = ok_c = True
RI, LS = [], []
for e in etas:
    Pe = B.sequence(P, e)
    qe = B.solve(Pe)
    ok_ps &= qe["Ps"] <= (e * pi + P["h"]) * (1 + 1e-12) and qe["Ps"] >= P["h"]
    ok_x &= qe["X"] <= e * P["T"] / (P["h"] * (1 - P["a"] * P["delta"])) * (1 + 1e-12)
    ok_fund &= bool(qe["funded"])
    ok_v &= 0 < qe["v"] <= e * pi * (1 + 1e-12)
    ok_c &= qe["x_ceiling"] == 1.0 and qe["nS_ceiling"] > qe["nD_ceiling"] == 0.0
    if e <= eta_star:
        ok_rent &= P["T"] >= P["N"] * qe["Ps"]
    RI.append(P["T"] / qe["income"])
    LS.append(qe["wages"] / qe["income"])
report("P_s <= (eta pi + h) r and P_s >= h on 2,001 points of [1e-4, 1]", "holds", ok_ps, ok_ps, "P_s\\le(\\eta\\pi+h)r")
report("rent alone funds the support at every grid eta <= (T - Nh)/(N pi)", "holds", ok_rent, ok_rent, None)
report("rent and the return on machines fund the support at every grid eta in [1e-4, 1]", "holds", ok_fund, ok_fund, None)
report("X <= eta T/[h(1 - a delta)] on the grid", "holds", ok_x, ok_x, "X\\le\\eta T/[h(1-a\\delta)]")
report("0 < v <= eta pi on the grid", "holds", ok_v, ok_v, None)
report("(25) on the grid: x_c = 1, N_S(1) > N_D(1) = 0", "holds", ok_c, ok_c, None)
report("R/I -> 1 along the path (R/I at eta = 1 and 1e-4)", "-> 1", f"{RI[-1]:.4f} -> {RI[0]:.5f}", RI[0] > RI[-1] and RI[0] > 0.999,
       "R/I\\to1")
report("labor's share still tends to zero (at eta = 1 and 1e-4)", "-> 0", f"{LS[-1]:.4f} -> {LS[0]:.6f}", LS[0] < 1e-3, None)
report("relative capability gamma_eta(1)/gamma_eta(0)", "a hundred", (P["g0"] + P["g1"]) / P["g0"],
       abs((P["g0"] + P["g1"]) / P["g0"] - 100) < 1e-9, "a hundred times")
report("gamma_eta <= eta (since g0 + g1 = 1)", "holds", P["g0"] + P["g1"], P["g0"] + P["g1"] <= 1.0, "Since $\\gamma_\\eta\\le\\eta$")

# ------------------------------------------------------------------ Section 5.2
print("== Section 5.2, the instance's income")
I = q["income"]
for lab, pr, val in (("wages / income", "0.55", q["wages"] / I), ("rent / income", "0.13", P["T"] / I),
                     ("return on machines / income", "0.32", q["interest"] / I), ("labor's share", "0.55", q["wages"] / I)):
    report(lab, pr, f"{val:.6f}", rounds_to(pr, val), "income is $0.55$ wages")
bound = q["v"] * q["n"] / (q["v"] * q["n"] + P["T"])
report("(15)'s bound (w/r)N_a/[(w/r)N_a + T]", "0.81", f"{bound:.6f}", rounds_to("0.81", bound), "against the $0.81$")
report("income identity P_s Y = w N_a + r T + rho V_m X (1e-12)", "identity", f"{q['Ps'] * q['Y']:.10f} vs {I:.10f}",
       abs(q["Ps"] * q["Y"] - I) <= 1e-12 * I, None)
report("printed shares sum to one", "0.55+0.13+0.32", 0.55 + 0.13 + 0.32, abs(0.55 + 0.13 + 0.32 - 1) < 1e-12, None)

# ------------------------------------------------------------------ Section 6
print("== Section 6")
report("rent covers this share of the instance's support, T/(N P_s)", "0.38", f"{P['T'] / q['support']:.6f}",
       rounds_to("0.38", P["T"] / q["support"]), "rent covers $0.38$")
report("the return on machines covers 'the rest' (rho V_m X >= N P_s - T)", "the rest",
       f"{q['interest']:.6f} >= {q['support'] - P['T']:.6f} (covers {q['interest'] / q['support']:.4f} of support)",
       q["interest"] >= q["support"] - P["T"], "and the return on machines the rest")
# lambda = 0, machines performing every task (x = 1), at the instance's other parameters
P0 = {**P, "lam": 0.0}
J1 = B.J(P0, 1.0)
pm = cpt * P0["b"] / (1 - cpt * P0["a"])
Ps1 = pm * J1 + P0["h"]
Bs1 = P0["h"] + P0["b"] * P0["delta"] * J1 / (1 - P0["a"] * P0["delta"])
Y1 = P0["T"] / Bs1
X1 = Y1 * J1 / (1 - P0["a"] * P0["delta"])
Vm1 = pm / cpt
report("lambda = 0, x = 1: full capture of rent and interest funds (T + rho V_m X)/(N P_s) baskets per person", "1.71",
       f"{(P0['T'] + P0['rho'] * Vm1 * X1) / (P0['N'] * Ps1):.6f} (= Y/N = T/(N B_s) = {Y1 / P0['N']:.6f})",
       rounds_to("1.71", (P0["T"] + P0["rho"] * Vm1 * X1) / (P0["N"] * Ps1)), "funds $1.71$ baskets")
report("lambda = 0, x = 1: rent alone funds T/(N P_s)", "0.66", f"{P0['T'] / (P0['N'] * Ps1):.6f}",
       rounds_to("0.66", P0["T"] / (P0["N"] * Ps1)), "rent alone funds $0.66$")
report("measured coverage 0.30 (Section 8: 'kappa=0.30 [0.15--0.59]')", "0.30", "Section 8 prints 0.30",
       "The 2025 estimate is $\\kappa=0.30$ [0.15--0.59]" in RAW, "The measured coverage, $0.30$")

# ------------------------------------------------------------------ Appendix D
print("== Appendix D")
for N_, q_, kap in ((50, 10 / 9, 20 / 19),):
    k_ = q_ * 100 / (N_ * (1 + q_ * 1))
    report("D.3: T = 100, g_s = h_s = 1, q = 10/9, fifty people: kappa", "20/19", f"{k_:.12f}", abs(k_ - kap) < 1e-12,
           "fifty people are covered")
report("D.3: fifty people covered with room to spare (kappa > 1)", "> 1", 20 / 19, 20 / 19 > 1, None)
report("D.3: eighty people need q >= q* = N g_s/(T - N h_s)", "4", 80 * 1 / (100 - 80), 80 / (100 - 80) == 4, "q\\ge4")
report("D.3: 120 people: direct space N h_s exceeds T", "120 > 100", 120 * 1, 120 > 100, "with 120 people")
for phi, kap, pr in ((0.64, 0.30, "0.31"), (0.50, 0.60, "0.08")):
    Dv = phi * (1 - kap) ** 2
    report(f"D.5: D = phi_C (1 - kappa)^2 at ({phi}, {kap})", pr, f"{Dv:.6f}", rounds_to(pr, Dv), "gives $D=0.31$")
kr = {int(l.split(",")[0]): [float(v) for v in l.split(",")[1:4]] for l in
      (ROOT / "data" / "kappa_results.csv").read_text().splitlines()[1:]}
report("Table D.1 / Section 8: kappa 2025 median [min--max] from data/kappa_results.csv", "0.30 [0.15--0.59]",
       f"{kr[2025][1]:.4f} [{kr[2025][0]:.4f}--{kr[2025][2]:.4f}]",
       rounds_to("0.30", kr[2025][1]) and rounds_to("0.15", kr[2025][0]) and rounds_to("0.59", kr[2025][2]), "0.30 [0.15--0.59]")
fifties = [kr[y][1] for y in range(1953, 1960)]
report("Table D.1: kappa approx 0.05 in the 1950s (medians 1953-59)", "0.05", f"{min(fifties):.4f}--{max(fifties):.4f}",
       0.035 <= np.mean(fifties) <= 0.065, "0.05$ in the 1950s")
fw = {int(l.split(",")[0]): [float(v) for v in l.split(",")[1:]] for l in
      (ROOT / "data" / "four_way_split.csv").read_text().splitlines()[1:]}
tr = sum(fw[2025][1:4])
report("Figure D.1 caption: borrowing financed 19% of transfers in 2025", "19%", f"{100 * fw[2025][3] / tr:.2f}%",
       round(100 * fw[2025][3] / tr) == 19, "Borrowing financed 19")
zero = [y for y in sorted(fw) if fw[y][3] == 0.0]
report("Figure D.1 caption: borrowing zero only in 1960, 1963, 1999, 2000", "1960, 1963, 1999, 2000", zero,
       zero == [1960, 1963, 1999, 2000], None)
report("Figure D.1 caption: direct-wage share fell by about twenty points (1960 to 2025)", "about twenty",
       f"{100 * (fw[1960][0] - fw[2025][0]):.1f} points", 15 <= 100 * (fw[1960][0] - fw[2025][0]) <= 25, None)
report("Figure D.1 caption: about a fifth of transfers' financing from ownership-income taxes (2025)", "about a fifth",
       f"{fw[2025][2] / tr:.3f}", 0.15 <= fw[2025][2] / tr <= 0.25, None)

# Table D.1's other rows, against the repository's series (README, "Numbers in the text"; measurement, not appendix_b.py)
df21 = {int(l.split(",")[0]): [float(v) for v in l.split(",")[1:4]] for l in
        (ROOT / "effort" / "archive_v28" / "expected" / "DF21_FINAL_longrun_labor_origin_financing_1950_2025.csv")
        .read_text(encoding="utf-8").splitlines()[1:]}
report("Table D.1: phi_C 2025 central [lower--upper] (effort/.../DF21_...csv)", "0.64 [0.54--0.81]",
       f"{df21[2025][0]:.4f} [{df21[2025][1]:.4f}--{df21[2025][2]:.4f}]",
       all(rounds_to(p_, v_) for p_, v_ in zip(("0.64", "0.54", "0.81"), df21[2025])), "0.64 [0.54--0.81]")
report("Table D.1: phi_C 2023 source-profile window", "0.66 [0.53--0.80]",
       f"{df21[2023][0]:.4f} [{df21[2023][1]:.4f}--{df21[2023][2]:.4f}]",
       all(rounds_to(p_, v_) for p_, v_ in zip(("0.66", "0.53", "0.80"), df21[2023])), "0.66 [0.53--0.80]")
report("Table D.1: phi_C approx 0.74 in 1965", "0.74", f"{df21[1965][0]:.4f}", rounds_to("0.74", df21[1965][0]), None)
lr = {int(l.split(",")[0]): l.split(",") for l in (ROOT / "data" / "lambda_results.csv").read_text().splitlines()[1:]}
report("Table D.1: phi_G 2025 (lamR_med)", "0.68", f"{float(lr[2025][8]):.4f}", rounds_to("0.68", float(lr[2025][8])), "0.68 (2025)")
report("Table D.1: phi_G 1965 (lamR_med)", "0.64", f"{float(lr[1965][8]):.4f}", rounds_to("0.64", float(lr[1965][8])), None)
mid80 = [float(lr[y][8]) for y in range(1983, 1989)]
report("Table D.1: phi_G approx 0.70 by the mid-1980s", "0.70", f"{min(mid80):.4f}--{max(mid80):.4f}",
       all(rounds_to("0.70", v_) for v_ in mid80), None)
lb = {int(l.split(",")[0]): l.split(",") for l in (ROOT / "data" / "lambdaB_results.csv").read_text().splitlines()[1:]}
report("Table D.1: conditioned share of benefits >= 0.84 (2024, lamB_floor)", ">= 0.84", f"{float(lb[2024][9]):.4f}",
       float(lb[2024][9]) >= 0.84, None)
print(f"   (Table D.1's 'approx 0.99 by withdrawal rule (2024)': data/lambdaB_results.csv lamB_rule is {lb[2024][10]} in 2024 "
      f"and in every year; the README names this column as the source; the script that made it is not in the repository)")

bad = [s for ok, s in OUT if not ok]
print(f"\n{len(OUT)} numbers compared; {len(bad)} mismatches")
for s in bad:
    print("  ", s)
