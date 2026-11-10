# check_program.py — code/program.py, the sizes behind the draft's Section 9.
#   I  identities: the gaps cancel across groups; each group's `needs` matches it exactly; saving at the stated rate
#      builds the stated holding; a common share moves no income in or out of the total
#   Q  the numbers SKETCH.md and the draft quote
# Reads only files in the repository. Run from provisioning/:  python3 checks/check_program.py
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "code"))
import exposure as ex  # noqa: E402
import paper_path as pp  # noqa: E402
import program as pg  # noqa: E402

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append(bool(ok))
    print(("PASS " if ok else "FAIL ") + name + (f" — {detail}" if detail else ""))


def prints(value, printed, decimals):
    return abs(value - printed) <= 0.5 * 10.0 ** (-decimals) * 1.05


def rows(pairs):
    return all(prints(v, q, d) for v, q, d in pairs), "; ".join(f"{v:.4f} for {q}" for v, q, d in pairs)


tabs, Y = ex.inputs(), 2023
g0, matched = pg.gaps(tabs, Y)
g5, _ = pg.gaps(tabs, Y, pg.THETA)
bh, nf, tt = "bottom half", "next four tenths", "top tenth"

# ---- I. identities
check("I1 the shares of the claims that the groups lack cancel, with nothing held in common and with a fifth (1e-12)",
      abs(sum(v["gap"] for v in g0.values())) < 1e-12 and abs(sum(v["gap"] for v in g5.values())) < 1e-12)
worst = max(abs(pg.gaps(tabs, Y, g0[k]["needs"])[0][k]["gap"]) for k in g0)
check("I2 a common share of `needs` leaves the group lacking nothing (1e-12)", worst < 1e-12, f"{worst:.1e}")
held, s = ex.market_shares(tabs, Y)
moved = max(abs(ex.income_share(held[k], x, pg.THETA) - (held[k]["labour"] * x + g5[k]["claims"] * (1 - x))) for k in held for x in (s, 0.17, 0.0))
check("I3 a group's share of market income with a fifth in common is its labour share and its claims, each at what it is paid (1e-12)",
      moved < 1e-12, f"{moved:.1e}")
short, rate, ret = g5[nf]["short"], 0.05, 0.05
n = pg.years_to_match(short, rate, ret)
built = rate * ((1 + ret) ** n - 1) / ret
check("I4 saving 5% of wages for the stated years at 5% builds a holding of short / 0.05 years of wages (1e-9)",
      abs(built - short / ret) < 1e-9, f"{built:.4f} years of wages")
check("I5 a matched group has what everyone has: capital and land over labour income, the top tenth above it and the others below",
      g0[tt]["per_dollar"] > matched > g0[nf]["per_dollar"] > g0[bh]["per_dollar"] > 0)

# ---- Q. quoted
check("Q1 2023, income from capital and land per dollar of labour income: bottom half 0.24, next four tenths 0.27, top tenth 0.96; matched 0.51",
      *rows([(g0[bh]["per_dollar"], 0.24, 2), (g0[nf]["per_dollar"], 0.27, 2), (g0[tt]["per_dollar"], 0.96, 2), (matched, 0.51, 2)]))
nine_l = held[bh]["labour"] + held[nf]["labour"]
nine_k = held[bh]["capital"] + held[nf]["capital"]
check("Q2 the bottom nine tenths hold 0.645 of labour income and 0.328 of the claims, about half of what would match them; they lack "
      "0.317 of all the claims: the bottom half 0.094 and the next four tenths 0.223",
      *rows([(nine_l, 0.645, 3), (nine_k, 0.328, 3), (nine_k / nine_l, 0.51, 2), (-g0[tt]["gap"], 0.317, 3), (g0[bh]["gap"], 0.094, 3),
             (g0[nf]["gap"], 0.223, 3)]))
check("Q3 the common share that alone would match the bottom half is 0.22; none can match the next four tenths (1.44 of everything)",
      *rows([(g0[bh]["needs"], 0.22, 2), (g0[nf]["needs"], 1.44, 2)]))
check("Q4 with a fifth in common: the bottom half holds 0.166 of the claims and 0.48 a dollar, lacking 0.010; the next four tenths "
      "0.276 and 0.30, lacking 0.192, or 0.21 a dollar of wages; the top tenth 0.558 and 0.80",
      *rows([(g5[bh]["claims"], 0.166, 3), (g5[bh]["per_dollar"], 0.48, 2), (g5[bh]["gap"], 0.010, 3), (g5[nf]["claims"], 0.276, 3),
             (g5[nf]["per_dollar"], 0.30, 2), (g5[nf]["gap"], 0.192, 3), (g5[nf]["short"], 0.21, 2), (g5[tt]["claims"], 0.558, 3),
             (g5[tt]["per_dollar"], 0.80, 2)]))
check("Q5 the next four tenths after a common fifth: a holding of 4.2 years of wages at 5% and 2.1 at 10%; saving 5% of wages takes "
      "34 years at 5% and 17 at 10%; saving 10% takes 23 and 12",
      *rows([(short / 0.05, 4.2, 1), (short / 0.10, 2.1, 1), (pg.years_to_match(short, 0.05, 0.05), 34, 0), (pg.years_to_match(short, 0.05, 0.10), 17, 0),
             (pg.years_to_match(short, 0.10, 0.05), 23, 0), (pg.years_to_match(short, 0.10, 0.10), 12, 0)]))
later = pg.gaps(tabs, Y, pg.THETA, pp.mix(1.0)["labour"])[0][nf]["short"]
check("Q6 with labour paid what it is paid at t = 1 in the model economy the same 5% takes 76 years at 5% and 39 at 10%; the claims "
      "cost 7.2 times as many years of wages there",
      *rows([(pg.years_to_match(later, 0.05, 0.05), 76, 0), (pg.years_to_match(later, 0.05, 0.10), 39, 0),
             (pp.claims(1.0)["both"] / pp.claims(0.0)["both"], 7.2, 1)]))
d = pg.dividend(tabs, Y)
check("Q7 a common fifth pays $4,493 a person a year in 2023, $374 a month: 0.58 of a poverty-line bundle for one of a family of "
      "four, 0.29 for a person alone",
      *rows([(d["a_person"], 4493, 0), (d["a_person"] / 12, 374, 0), (d["family4"], 0.58, 2), (d["single"], 0.29, 2)]))
p = pg.public_claims(tabs, Y)
check("Q8 the corporate income tax raised $621bn in 2023, 0.08 of the income of capital and land; residential site rent is 0.12 to "
      "0.19 of it; a tax on its growth collects 0.39 of the rent after 25 years at 2%, so 0.05 to 0.08; together 0.13 to 0.16",
      *rows([(p["corporate"], 621, 0), (p["corporate_share"], 0.08, 2), (p["site_share"][0], 0.12, 2), (p["site_share"][1], 0.19, 2),
             (p["grown"], 0.39, 2), (p["growth_share"][0], 0.05, 2), (p["growth_share"][1], 0.08, 2), (p["together"][0], 0.13, 2),
             (p["together"][1], 0.16, 2)]))
check("Q9 contributions for social insurance were 0.25 of all taxes and contributions in 2023", prints(pg.receipts(Y), 0.25, 2),
      f"{pg.receipts(Y):.4f}")
check("Q10 in the model economy the income of a common fifth is 0.13 of the wage bill at the start of the path and 0.96 at t = 1",
      *rows([(pg.path_dividend(0.0)["of_wages"], 0.13, 2), (pg.path_dividend(1.0)["of_wages"], 0.96, 2)]))

n_ok = sum(RESULTS)
print(f"\n{n_ok}/{len(RESULTS)} checks green")
sys.exit(0 if n_ok == len(RESULTS) else 1)
