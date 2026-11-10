# check_paper_path.py — code/paper_path.py against the numbers "What Machines Cannot Make" (October 2026) prints, and
# the numbers SKETCH.md quotes from it.
#   A  the baseline of its Appendix C and Table 1
#   B  its Table 2 (the calibrated schedule) and the path's dated readings in Section 8.4
#   C  Sections 8.3, 8.5 and 8.7: the margin absorbing, the refuge's capacity, cheaper finance
#   D  the accounts add up at every point used
#   E  what the sketch quotes: who is paid, what the claims cost, who bears a tax on interest, what a common share pays
#   F  a cash-flow tax leaves a machine's user cost where it was and pays the state its share of the interest
# A printed number passes if the re-derivation rounds to it (half a unit in its last digit, with a little room because
# the parameters themselves are printed to six digits).
# Run from provisioning/:  python3 checks/check_paper_path.py      Exit 0 only if every check passes.
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "code"))
import paper_path as pp  # noqa: E402

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append(bool(ok))
    print(("PASS " if ok else "FAIL ") + name + (f" — {detail}" if detail else ""))


def prints(value, printed, decimals):
    """Does value round to the printed number?"""
    return abs(value - printed) <= 0.5 * 10.0 ** (-decimals) * 1.05 + 2e-5 * abs(printed)


def rows(pairs):
    return all(prints(v, q, d) for v, q, d in pairs), "; ".join(f"{v:.5g} for {q}" for v, q, d in pairs)


P = pp.PAR
u = P["rho"] + P["delta"]
e0 = pp.equilibrium(1.0, P["lam"], P)
b0 = pp.readout(e0, P)

# ---- A. the baseline
check("A1 Appendix C's baseline prices and stocks (w = p_m 11.0106, V 64.7685, p 18.9597, Y 11.0106, K 34.0426)",
      *rows([(e0["w"], 11.0106, 4), (e0["pm"], 11.0106, 4), (e0["pm"] / u, 64.7685, 3), (e0["p"], 18.9597, 4),
             (e0["Y"], 11.0106, 4), (e0["K"], 34.0426, 3)]))
check("A2 Table 1's shares and margin (labour 0.60, interest 0.31, land 0.09, margin 0.10, capital over income 3.1, "
      "machine building 20% of hours)",
      *rows([(b0["labour"], 0.60, 2), (b0["interest"], 0.31, 2), (b0["rent"], 0.09, 2), (b0["x"], 0.10, 2),
             (e0["K"] / e0["Y"], 3.1, 1), (b0["building"], 0.20, 2)]))
check("A3 the bound is idle: human advantage reaches 166 and replacing the hardest hour embodies 152",
      *rows([(b0["gamma_bar"], 166, 0), (b0["lam_bar"], 152, 0)]))
check("A4 total requirements of machine services (hours 0.916667, land 0.917553)",
      *rows([(u * P["lam"] / (1 - u * P["a"]), 0.916667, 6), (u * P["b"] / (1 - u * P["a"]), 0.917553, 5)]))


def ratio(t, **kw):
    r = pp.point(t, **kw)
    return (r["wage_rent"] / b0["wage_rent"], r["wage_good"] / b0["wage_good"], r["real_wage"] / b0["real_wage"],
            r["real_income"] / b0["real_income"], r["labour"], r["building"])


def table2(name, t, printed, decs, **kw):
    got = ratio(t, **kw)
    check(name, *rows([(g, q, d) for g, q, d in zip(got, printed, decs)]))


# ---- B. Table 2, the calibrated schedule (w/r, w/p, real wage, income per person: ratios; labour's share, hours building)
table2("B1 t = 1, task automation only", 1.0, (0.52, 12.6, 9.8, 15.4, 0.38, 0.47), (2, 1, 1, 1, 2, 2), recursive=False)
table2("B2 t = 1, recursive automation only", 1.0, (0.32, 1.9, 1.7, 2.2, 0.46, 0.00), (2, 1, 1, 1, 2, 2), task=False)
table2("B3 t = 1, both", 1.0, (0.087, 13.8, 9.2, 32.1, 0.17, 0.00), (3, 1, 1, 1, 2, 2))
table2("B4 t = 2, task automation only (the corner: every worker builds machines)", 2.0,
       (0.11, 771.9, 381.4, 1507.2, 0.15, 1.00), (2, 1, 1, 1, 2, 2), recursive=False)
table2("B5 t = 2, both", 2.0, (0.0014, 20.9, 9.7, 1821.7, 0.0032, 0.00), (4, 1, 1, 1, 4, 2))

ts = np.linspace(0.0, 2.0, 2001)
lam_bar = np.array([pp.point(t)["lam_bar"] for t in ts])
rw = np.array([pp.point(t)["real_wage"] for t in ts]) / b0["real_wage"]
corner = [t for t in ts if pp.point(t, recursive=False)["corner"]]
check("B6 the bound acquires content at t = 0.77; the real wage peaks at 11.1 times baseline at t = 1.42",
      *rows([(ts[np.argmax(lam_bar < 1.0)], 0.77, 2), (rw.max(), 11.1, 1), (ts[rw.argmax()], 1.42, 2)]))
check("B7 with task automation alone the corner begins at t = 1.22", *rows([(corner[0], 1.22, 2)]))
r2 = pp.point(2.0)
check("B8 shares of income at t = 2 (labour 0.003, rent 0.35, interest 0.65)",
      *rows([(r2["labour"], 0.003, 3), (r2["rent"], 0.35, 2), (r2["interest"], 0.65, 2)]))

# ---- C. Sections 8.3, 8.5, 8.7
e10 = pp.equilibrium(0.9, P["lam"], P)
held = 0.9 * (u * P["b"] / (1 - u * P["a"])) / (1 - 0.9 * u * P["lam"] / (1 - u * P["a"]))   # the closure at the old margin
check("C1 the margin absorbs: human advantage 10% lower cuts w/r 57% at the old margin, 0.2% in equilibrium, margin 0.15",
      *rows([(100 * (held / e0["w"] - 1), -57, 0), (100 * (e10["w"] / e0["w"] - 1), -0.2, 1), (e10["x"], 0.15, 2)]))
ad = 1 - P["a"] * P["delta"]
Lstar = ((1 - P["alpha"]) * P["T"] * P["lam"] * P["delta"] / ad
         / (P["alpha"] * u * P["b"] / (1 - u * P["a"]) + (1 - P["alpha"]) * P["b"] * P["delta"] / ad))
check("C2 the refuge in building machines could employ 0.77 hours, 1.29 times the hours supplied",
      *rows([(Lstar, 0.77, 2), (Lstar / P["Na"], 1.29, 2)]))
half = dict(P, rho=0.05)
eh = pp.equilibrium(1.0, P["lam"], half)
bh = pp.readout(eh, half)
uh = half["rho"] + half["delta"]
old_margin = pp.state(e0["x"], 1.0, P["lam"], half)
check("C3 Section 8.7, the interest rate halved: w/r 89% lower and 2.81 hours demanded at the old margin; then margin "
      "0.31, an hour worth 1.70 machine services, w/r 5% higher, the wage in goods 29% higher, labour 0.68, interest 0.22",
      *rows([(100 * (old_margin["w"] / e0["w"] - 1), -89, 0), (old_margin["hours"], 2.81, 2), (bh["x"], 0.31, 2),
             (bh["gamma"], 1.70, 2), (100 * (bh["wage_rent"] / b0["wage_rent"] - 1), 5, 0),
             (100 * (bh["wage_good"] / b0["wage_good"] - 1), 29, 0), (bh["labour"], 0.68, 2), (bh["interest"], 0.22, 2)]))

# ---- D. the accounts
worst = max(abs(pp.point(t, **kw)["identity"]) / 1.0 for t in (0.0, 0.25, 0.5, 0.77, 1.0, 1.5, 2.0)
            for kw in ({}, {"recursive": False}, {"task": False}))
check("D1 income is wages, rent and interest at every point used (to 1e-9 of the rent bill)", worst < 1e-9, f"{worst:.1e}")
z = pp.interest_tax(0.0)
check("D2 a zero tax changes nothing", max(abs(z[k]) for k in ("wages", "rents", "owners", "revenue", "lost")) < 1e-12)
gaps = []
for tau in (0.1, 0.2, 0.3, 0.5):
    r = pp.interest_tax(tau)
    gaps.append(abs(r["wages"] + r["rents"] + r["owners"] + r["revenue"] - (r["real_income"] - 1.0)))
check("D3 under the tax, the changes in wages, rents and owners' interest and the revenue add to the change in real income",
      max(gaps) < 1e-12, f"{max(gaps):.1e}")

# ---- E. what SKETCH.md quotes
m0, m1 = pp.mix(0.0), pp.mix(1.0)
check("E1 who is paid (labour, interest, rent): 60/31/9 today, 17/53/30 at t = 1",
      *rows([(100 * m0["labour"], 60, 0), (100 * m0["interest"], 31, 0), (100 * m0["rent"], 9, 0),
             (100 * m1["labour"], 17, 0), (100 * m1["interest"], 53, 0), (100 * m1["rent"], 30, 0)]))
c = {t: pp.claims(t) for t in (0.0, 0.5, 0.77, 1.0)}
check("E2 the claims on interest and rent in years of the wage bill: 6.7 today (capital 5.2, land 1.5), 9.1 at t = 0.5, "
      "19 at the threshold, 48 at t = 1",
      *rows([(c[0.0]["both"], 6.7, 1), (c[0.0]["capital"], 5.2, 1), (c[0.0]["land"], 1.5, 1), (c[0.5]["both"], 9.1, 1),
             (c[0.77]["both"], 19, 0), (c[1.0]["both"], 48, 0)]))
x = pp.interest_tax(0.2)
check("E3 a 20% tax on interest, long run, today: the real wage 10% lower, capital 19% lower, real income 6.5% lower; "
      "wages -6.1, owners -5.9, rents -0.8, revenue +6.3 points of income; a wage earner given all of it: +0.3%",
      *rows([(100 * (x["real_wage"] - 1), -10, 0), (100 * (x["real_capital"] - 1), -19, 0),
             (100 * (x["real_income"] - 1), -6.5, 1), (100 * x["wages"], -6.1, 1), (100 * x["owners"], -5.9, 1),
             (100 * x["rents"], -0.8, 1), (100 * x["revenue"], 6.3, 1), (100 * x["wage_earner"], 0.3, 1)]))
y = pp.interest_tax(0.2, t=1.0)
check("E4 the same tax at t = 1: wages untouched, rents -5.9, revenue +10.9 points of income, capital 17% lower",
      *rows([(100 * y["wages"], 0.0, 1), (100 * y["rents"], -5.9, 1), (100 * y["revenue"], 10.9, 1),
             (100 * (y["real_capital"] - 1), -17, 0)]))

share = 0.2
check("E5 a fifth of capital's claim: 6.2% of income; the stake is 1.0 year of the wage bill today and 6.1 at t = 1",
      *rows([(100 * share * m0["interest"], 6.2, 1), (share * c[0.0]["capital"], 1.0, 1), (share * c[1.0]["capital"], 6.1, 1)]))
check("E6 a common fifth of both claims pays everyone 8% of mean income today and 17% at t = 1",
      *rows([(100 * share * (1 - m0["labour"]), 8, 0), (100 * share * (1 - m1["labour"]), 17, 0)]))

# ---- F. the cash-flow tax: the state expenses its share t of every machine built and takes t of every rental
V0, M0 = e0["pm"] / u, e0["K"] / (e0["pm"] / u)
worst = 0.0
for tshare in (0.1, 0.2, 0.5):
    owner = (1 - tshare) * e0["pm"] - u * (1 - tshare) * V0                       # the owner's return on what the owner paid
    state_take = tshare * (e0["pm"] * M0 - P["delta"] * V0 * M0)                  # rentals less its share of replacement
    worst = max(worst, abs(owner), abs(state_take - tshare * P["rho"] * e0["K"]))
check("F1 with expensing at any share t the owner still earns rho on what the owner paid, so the user cost is unchanged, "
      "and the state's stationary take is t of the interest", worst < 1e-12, f"{worst:.1e}")

n_ok = sum(RESULTS)
print(f"\n{n_ok}/{len(RESULTS)} checks green")
sys.exit(0 if n_ok == len(RESULTS) else 1)
