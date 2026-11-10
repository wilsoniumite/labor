# check_essay.py — the numbers essay/essay.md prints are the ones the scripts produce.
#
# The same test as check_draft.py, on the essay. Each `says` line is a sentence or table row of the essay with its numbers
# filled in from the stored tables and the scripts, formatted as the essay prints them: it passes when the filled text is
# in the essay, so it fails if the data move and it fails if a number in the essay is changed. Numbers the essay gives in
# words (two-thirds, about a seventh, a hundredfold) are held by `band` lines, each inside a stated range.
#   A  what we buy is made of and paid for by (the dollar, the two counts, Keynes's forecast)
#   B  who gets which kind of income
#   C  what has changed so far
#   D  the model economy: the path, what incomes buy, the door, the tax and the stake
#   E  land
#   F  the program for the United States
#   G  the dividend and a basic income
#   H  fairness
#   T  the worth of time: the experiment's figures, as its summary prints them
#   Q  quotations and outside facts: transcriptions, each read at the source named beside it
#   N  not held on this branch: listed, and held when their inputs are given
# The wage figures need the backward model's panel, which is on another branch; give its path to hold those lines too:
#   python3 checks/check_essay.py PATH/TO/us-record/data/panel.csv
# Run from provisioning/:  python3 checks/check_essay.py      Exit 0 only if every check passes.
import math
import os
import re
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "code"))
import exposure as ex  # noqa: E402
import one_basis_tables as obt  # noqa: E402
import paper_path as pp  # noqa: E402
import program as pg  # noqa: E402
import rent_base as rb  # noqa: E402
import wage_shortfall as ws  # noqa: E402

RESULTS = []
TEXT = re.sub(r"\s+", " ", open(os.path.join(ROOT, "essay", "essay.md")).read())


def check(name, ok, detail=""):
    RESULTS.append(bool(ok))
    print(("PASS " if ok else "FAIL ") + name + (f" — {detail}" if detail else ""))


def says(name, text):
    """The essay carries this text, whose numbers were filled in from the data."""
    text = re.sub(r"\s+", " ", text)
    check(name, text in TEXT, "" if text in TEXT else "not in the essay: " + text)


def band(name, value, low, high):
    """A number the essay gives in words lies in the range the words allow."""
    check(name, low <= value <= high, f"{value:.4f} in [{low}, {high}]")


d0, d1 = (lambda x: f"{x:.0f}"), (lambda x: f"{x:.1f}")
p0, p1 = (lambda x: f"{100 * x:.0f}"), (lambda x: f"{100 * x:.1f}")
usd = lambda x: f"${x:,.0f}"   # noqa: E731

# ---------------------------------------------------------------------------------------------------------------- A
made, fin = obt.made(), obt.financing()
r, f23 = made.loc[2023], fin.loc[2023]
lab = made.labour_factor_psi38
years = [y for y in fin.index if y in made.index]
diff = (lab - fin.fin_labour).loc[years]
owning_cents = r.comp + r.nos - r.labour_dollar_psi38

says("A1 the dollar",
     f"{p0(r.imports)} cents leaves the country for imports, {p0(r.tax)} cents is tax on the product, {p0(r.labour_dollar_psi38)} cents is "
     f"pay for work, and 27 and a half cents goes to the owners of machines and land")
band("A1b '27 and a half cents'", float(owning_cents), 0.2725, 0.2775)
check("A1c the four parts of the dollar add to one (1e-6)", abs(r.imports + r.tax + r.labour_dollar_psi38 + owning_cents - 1) < 1e-6)
says("A2 the part paid at home", f"Work gets {p0(lab[2023])} percent of it and ownership gets {p0(1 - lab[2023])}.")
band("A3 'two-thirds and one-third'; 'about a third of what Americans are paid for making the things we buy'", float(lab[2023]), 0.64, 0.69)
says("A4 the second count", f"pay for work turns out to cover {p0(f23.fin_labour)} percent of what households buy")
says("A5 its bounds", f"gives anything from {p0(f23.fin_lower)} to {p0(f23.fin_upper)} percent")
check("A6 'the twenty years in which both exist': 2004 to 2023", years[0] == 2004 and years[-1] == 2023 and len(years) == 20)
band("A7 'they differ by one cent in the dollar on average'", float(diff.abs().mean()), 0.005, 0.015)
band("A8 'and never by more than two and a half'", float(diff.abs().max()), 0.0, 0.0255)
says("A9 the drift", f"work's share was {p0(lab[1997])} percent in 1997, {p0(lab.max())} at its peak in {int(lab.idxmax())}, and {p0(lab[2023])} in 2023")
says("A10 the gauge to watch", f"which was {p0(lab.max())} percent in {int(lab.idxmax())} and {p0(lab[2023])} in 2023")
says("A11 shelter and the rest",
     f"Work makes {p0(r.rest_labour_factor_psi38)} percent of everything else in the household budget and {p0(r.shelter_labour_factor)} "
     f"percent of shelter")
says("A12 what a tax on spending would rest on today", f"pay for work covers {p0(f23.fin_labour)} percent of what households buy, so a tax on spending")
real_gdp, people = rb.annual("paths/cache/GDPCA.csv"), rb.annual("pinning/cache/B230RC0A052NBEA.csv")
per = real_gdp / people
says("A13 Keynes's first forecast", f"output per person in the United States stood at {d1(per[2024] / per[1930])} times its level in 1930")
check("A14 '2024, with six years still to run' of the hundred from 1930", 1930 + 100 - 2024 == 6)

# ---------------------------------------------------------------------------------------------------------------- B
tabs = ex.inputs()
a23 = ex.amounts(tabs, 2023)
work = a23.comp + ex.PSI * a23.prop
owning = (1.0 - ex.PSI) * a23.prop + a23.rent + a23.interest + a23.dividends + a23.accrued
of_market = work / (work + owning)
tau = float(tabs["tax"].loc[2023, "lamR_med"])
held, s_now = ex.market_shares(tabs, 2023)
bh, nf, tt = held["bottom half"], held["next four tenths"], held["top tenth"]
g0, matched = pg.gaps(tabs, 2023)
g5, _ = pg.gaps(tabs, 2023, pg.THETA)
P, N, R = "bottom half", "next four tenths", "top tenth"
share = ex.income_share

band("B1 'the poorest tenth lives mostly on government benefits': their share of its income", float(a23.benefits.iloc[0] / (work + owning + a23.benefits).iloc[0]), 0.5, 1.0)
band("B2 'from the second tenth to the ninth ... about four-fifths is pay for work': the lowest of the eight", float(of_market.iloc[1:9].min()), 0.76, 0.84)
band("B2b the highest of the eight", float(of_market.iloc[1:9].max()), 0.76, 0.84)
band("B3 'in the richest tenth pay and ownership are about half and half': pay's part of its market income", float(of_market.iloc[9]), 0.47, 0.53)
says("B4 income from owning for every dollar of pay",
     f"For every dollar the poorer half of households earns by working, it receives {p0(g0[P]['per_dollar'])} cents from owning things. For "
     f"the four tenths above them, the comfortable middle, it's {p0(g0[N]['per_dollar'])} cents. A balanced household would have "
     f"{p0(matched)}. The richest tenth has {p0(g0[R]['per_dollar'])}.")
band("B5 'earns a bit over a third of all the pay'", float(tt["labour"]), 0.34, 0.37)
band("B6 'receives two-thirds of all the income from ownership'", float(tt["capital"]), 0.64, 0.69)
per_dollar = owning / work
check("B7 'nine households in ten are on one side and one in ten on the other': each of the first nine tenths has less from owning for every "
      "dollar of pay than would balance it, and the richest tenth more", bool((per_dollar.iloc[:9] < matched).all()) and per_dollar.iloc[9] > matched,
      f"highest of the nine {per_dollar.iloc[:9].max():.2f}, the richest tenth {per_dollar.iloc[9]:.2f}, balanced {matched:.2f}")
says("B8 the tax base",
     f"{p0(tau)} cents of every tax dollar in America is raised from pay for work (somewhere between "
     f"{p0(float(tabs['tax'].loc[2023, 'lamR_min']))} and {p0(float(tabs['tax'].loc[2023, 'lamR_max']))}")
check("B9 'sixty-eight cents of every tax dollar'", p0(tau) == "68")

# ---------------------------------------------------------------------------------------------------------------- C
ss, s0, s1 = ex.shift_share(tabs, 2004, 2023)
top = ss["top tenth"]
says("C1 the last twenty years",
     f"fell from {p0(s0)} percent to {p0(s1)}. That shift, taken alone, moved {d1(100 * top['between'])} percent of all market income to the "
     f"richest tenth of households. In the same years that tenth gained twice as much again, {d1(100 * top['within'])} percent")
band("C2 'twice as much again'", float(top["within"] / top["between"]), 1.8, 2.3)

# ---------------------------------------------------------------------------------------------------------------- D
start, one, two = pp.point(0.0), pp.point(1.0), pp.point(2.0)
m0, mten, m1, m2 = pp.mix(0.0), pp.mix(0.5), pp.mix(1.0), pp.mix(2.0)
c0, cth, c1 = pp.claims(0.0), pp.claims(0.77), pp.claims(1.0)
tax = pp.interest_tax(0.20)
fifth = 0.2 * m0["interest"]
short = g5[N]["short"]
later = pg.gaps(tabs, 2023, pg.THETA, m1["labour"])[0][N]["short"]
yrs = pg.years_to_match
owners = (one["real_income"] * (1 - one["labour"])) / (start["real_income"] * (1 - start["labour"]))
grown = one["real_income"] / start["real_income"]

says("D1 the model economy today",
     f"this economy pays {p0(m0['labour'])} percent of its income for work, {p0(m0['interest'])} percent to the owners of machines and "
     f"{p0(m0['rent'])} percent to the owners of land")
says("D2 at ten times", f"When machines are ten times better, work is still paid {p0(mten['labour'])} percent of all income")
band("D3 'when machines are about 35 times better': a hundred to the power 0.77", 100 ** 0.77, 33.0, 37.0)
check("D3b the threshold: the hours of work inside the machines that replace the hardest hour fall below one between 0.76 and 0.78",
      pp.point(0.76)["lam_bar"] > 1.0 > pp.point(0.78)["lam_bar"])
says("D4 at a hundred and at ten thousand times",
     f"By the hundredfold point work is paid {p0(m1['labour'])} percent of all income. At ten thousand times it is paid less than 1 percent, "
     f"with {p0(m2['interest'])} percent going to the owners of machines and {p0(m2['rent'])} to the owners of land.")
band("D4b 'less than 1 percent'", float(m2["labour"]), 0.0, 0.0099)
says("D5 what incomes buy at the hundredfold point",
     f"At the hundredfold point total income is {d0(grown)} times what it was. An hour of work buys "
     f"{d0(one['wage_good'] / start['wage_good'])} times as many goods as it does today. Counting everything a household buys, land included, "
     f"an hour's pay goes {d0(one['real_wage'] / start['real_wage'])} times as far.")
band("D6 'the rent of land rises about a hundredfold'", float(one["real_rent"] / start["real_rent"]), 95.0, 115.0)
band("D7 'an hour's pay rents about a twelfth of the land it does now'", float(start["wage_rent"] / one["wage_rent"]), 11.0, 13.0)
says("D8 the owners' income", f"the income of those who own machines and land is {d0(owners)} times what it was")
for t in (1.25, 1.5, 2.0):
    band(f"D9 'the hourly wage levels off at around ten times today's': when machines are {100 ** t:,.0f} times better",
         float(pp.point(t)["real_wage"] / start["real_wage"]), 9.0, 11.5)
band("D10 'the economy goes on to grow more than fiftyfold again': income at ten thousand times over income at a hundred",
     float(two["real_income"] / one["real_income"]), 50.0, 60.0)
band("D11 'land's share of income more than triples'", float(m1["rent"] / m0["rent"]), 3.0, 4.0)
says("D12 the owners of machines", f"whose share goes from {p0(m0['interest'])} percent to {p0(m1['interest'])} and then to {p0(m2['interest'])}")
band("D13 'over fifty times as many' machines at the hundredfold point", float(one["real_capital"] / start["real_capital"]), 50.0, 60.0)
low = pp.point(1.0, dict(pp.PAR, rho=0.05))
check("D14 'if investors came to accept 5 percent ... land the larger share and machines the smaller. The share paid for work comes out "
      "about the same'", low["rent"] > low["interest"] and abs(low["labour"] - m1["labour"]) < 0.02,
      f"at 5 percent: work {low['labour']:.3f}, machines {low['interest']:.3f}, land {low['rent']:.3f}")
says("D15 what ownership costs", f"is worth about {d1(c0['both'])} years of the whole country's wages")
says("D15b at the threshold and at the hundredfold point", f"At the threshold it is {d0(cth['both'])} years. At the hundredfold point it is {d0(c1['both'])}.")
says("D16 the door",
     f"it gets there in {d0(yrs(short, 0.05, 0.05))} years at today's prices. At the hundredfold point the same saving takes "
     f"{d0(yrs(later, 0.05, 0.05))} years.")
says("D17 how long a hundredfold takes",
     f"A hundredfold improvement takes {d0(math.log(100) / math.log(1.04))} years at 4 percent a year")
says("D17b at faster paces", f"At 10 percent a year it takes {d0(math.log(100) / math.log(1.10))} years, and at 20 percent, {d0(math.log(100) / math.log(1.20))}.")
says("D18 income at the hundredfold point again", f"In the model economy at the hundredfold point income is {d0(grown)} times larger")
says("D19 who would receive the income",
     f"the richest tenth of American households would receive {p0(share(tt, 0.17))} percent of all market income, up from {p0(share(tt, s_now))}. "
     f"The four tenths below them would go from {p0(share(nf, s_now))} percent to {p0(share(nf, 0.17))}, and the poorer half from 14 and a half "
     f"to {p0(share(bh, 0.17))}.")
band("D19b '14 and a half'", float(share(bh, s_now)), 0.1425, 0.1475)
says("D20 the tax on what machines earn",
     f"the tax raises {p1(tax['revenue'])} percent of national income. Wages fall by {p1(-tax['wages'])} percent of national income. The "
     f"economy as a whole is {p1(1 - tax['real_income'])} percent smaller. If every dollar the tax raised were handed straight to wage earners, "
     f"they would end up {p1(tax['wage_earner'])} percent better off")
band("D21 'a smaller pile, about a fifth smaller'", float(1 - tax["real_capital"]), 0.17, 0.22)
band("D22 'about a year of the whole country's wages for a fifth of all the machines'", 0.2 * c0["capital"], 0.95, 1.10)
says("D23 the stake", f"which is {p1(fifth)} percent of national income in the model")
band("D23b the tax and the stake raise 'almost the same money': the difference, as a share of income", float(tax["revenue"] - fifth), 0.0, 0.002)
says("D24 the tax the program leaves out", f"it costs wages {p1(-tax['wages'])} percent of national income for every {p1(tax['revenue'])} it raises")
says("D25 what the stake undoes",
     f"an economy {p1(1 - tax['real_income'])} percent smaller and wages lower by {p1(-tax['wages'])} percent of national income")
PRINTED = dict(no_ceiling=0.48)   # Båge and Wilson (2026), Section 8.4, as printed: the same path with no limit on people's advantage
says("D26 without a ceiling on human advantage, as that paper prints it", f"lowers work's share to {p0(PRINTED['no_ceiling'])} percent and stops there")

# ---------------------------------------------------------------------------------------------------------------- E
t = rb.table()
b, c = t.loc[2024], t.loc[1955]
says("E1 the rent of the ground under homes",
     f"it came to between {p1(b.share_dpi_30)} and {p1(b.share_dpi_50)} percent of households' disposable income, which is between "
     f"{usd(b.rent_pp_30_last)} and {usd(b.rent_pp_50_last)} a year for every person in the country")
covers = [float(b[f"cover_{k}_{s}"]) for k in ("family4", "single") for s in ("30", "50")]
says("E2 what it would cover", f"it would cover between {p0(min(covers))} and {p0(max(covers))} percent of a bare poverty-line budget")
band("E3 'by the usual arithmetic is about 40 percent of the land's value': growth of 2 percent over a discount rate of 5", 0.02 / 0.05, 0.3999, 0.4001)
says("E4 what that is of a house", f"For a house whose value is three-tenths to a half land, that is {p0(0.4 * 0.3)} to {p0(0.4 * 0.5)} percent off the price.")

# ---------------------------------------------------------------------------------------------------------------- F
STATUTE = dict(corporate=0.21, oasdi_each=0.062)   # 26 U.S.C. 11(b), 3101(a) and 3111(a), read at law.cornell.edu on 2026-11-10
div, pub_claims, rc, bn = pg.dividend(tabs, 2023), pg.public_claims(tabs, 2023), pg.receipts(2023), pg.benefits(2023)
head = rb.annual(pg.POPULATION)[2023] * 1e3
says("F1 the table, company profits",
     f"| Company profits | Taxed at {p0(STATUTE['corporate'])} percent by the federal government. All levels of government raised "
     f"${pub_claims['corporate']:.0f} billion from them in 2023")
says("F2 the table, land", f"through property taxes, which raised ${rc['property_bn']:.0f} billion.")
says("F3 the table, saving for old age", f"| Saving for old age | {p1(2 * STATUTE['oasdi_each'])} percent of wages goes to Social Security")
says("F4 the table, taxes on work",
     f"| Taxes on work | {p0(tau)} percent of all tax revenue is raised from pay. Payroll contributions alone are a quarter of everything collected.")
band("F4b 'a quarter of everything collected is payroll contributions'", float(rc["contributions"]), 0.24, 0.26)
says("F5 the table, money paid to everyone", f"| Money paid to everyone | None. Benefits of ${bn['total']:,.0f} billion a year are tied")
says("F6 the dividend", f"In 2023 it would have paid {usd(div['a_person'])} a person, or {usd(div['a_person'] / 12)} a month")
check("F6b 'more than Social Security pays out per head of population'", div["a_person"] > bn["social_security_bn"] * 1e9 / head,
      f"{div['a_person']:,.0f} against {bn['social_security_bn'] * 1e9 / head:,.0f}")
says("F6c what paying out the profits tax would cost", f"so paying it out means finding ${pub_claims['corporate']:.0f} billion a year somewhere else")
says("F7 the tax on profits as a stake", f"is worth {p0(pub_claims['corporate_share'])} percent of all ownership income")
band("F8 'about two-fifths of the rent after twenty-five years of growth at 2 percent a year'", float(pub_claims["grown"]), 0.38, 0.41)
says("F9 the growth of land rent", f"which comes to another {p0(pub_claims['growth_share'][0])} to {p0(pub_claims['growth_share'][1])} percent")
check("F10 'together that is about a seventh of all ownership income': a seventh lies between the two ends",
      pub_claims["together"][0] < 1 / 7 < pub_claims["together"][1], f"{pub_claims['together'][0]:.3f} to {pub_claims['together'][1]:.3f}")
check("F10b 'most of that fifth is within reach without buying anything'", pub_claims["together"][0] > 0.5 * pg.THETA)
band("F11 'a common share of about a seventh ... keeps the poorer half whole ... even if wages went to nothing'", float(ex.holding_share(bh, s_now, 0.0)), 0.125, 0.16)
band("F11b the same if work is paid 17 percent", float(ex.holding_share(bh, s_now, 0.17)), 0.125, 0.16)
says("F12 the poorer half with a common fifth",
     f"the poorer half would have {p0(g5[P]['per_dollar'])} cents of ownership income for every dollar of pay, against the {p0(matched)} that "
     f"would balance them exactly")
band("F13 'they earn nearly half of all the pay in the country'", float(nf["labour"]), 0.45, 0.50)
band("F14 'no common share short of six-sevenths of everything would keep them whole'", float(ex.holding_share(nf, s_now, 0.17)), 0.85, 0.87)
says("F15 what the middle still lacks", f"they would still be {p0(short)} cents short, for every dollar of pay")
says("F16 saving out of wages",
     f"the holding they need is worth {d1(short / 0.05)} years of their pay. Saving 5 percent of pay and reinvesting what it earns builds that "
     f"in {d0(yrs(short, 0.05, 0.05))} years, which is a working life. Wait until the hundredfold point and it takes {d0(yrs(later, 0.05, 0.05))}.")
says("F17 Social Security's tax", f"a much larger slice of wages for retirement, {p1(2 * STATUTE['oasdi_each'])} percent, for Social Security")
band("F18 'at the hundredfold point in the model, five-sixths of a tax on spending would be paid out of ownership income'", float(1 - m1["labour"]), 0.81, 0.85)
says("F19 the hard case",
     f"the richest tenth's share of market income goes from {p0(share(tt, s_now))} percent to {p0(share(tt, 0.17))}. With a fifth held in common "
     f"it goes to {p0(share(tt, 0.17, 0.2))}, and the poorer half ends up with {p0(share(bh, 0.17, 0.2))} percent, which is more than it has now. "
     f"The comfortable middle still falls, from {p0(share(nf, s_now))} percent to {p0(share(nf, 0.17, 0.2))}.")
check("F19b 'which is more than it has now'", share(bh, 0.17, 0.2) > share(bh, s_now))

# ---------------------------------------------------------------------------------------------------------------- G
says("G1 a basic income out of today's taxes", f"for {p0(tau)} cents in the dollar, wage earners paying each other")
says("G2 the size of the dividend",
     f"Today that is {usd(div['a_person'] / 12)} a month, which is {p0(div['family4'])} percent of the poverty line for one member of a family "
     f"of four and {p0(div['single'])} percent for a person living alone.")
says("G3 the dividend along the path",
     f"the income of a common fifth is {p0(pg.path_dividend(0.0)['of_wages'])} percent of all wages today, and "
     f"{p0(pg.path_dividend(1.0)['of_wages'])} percent of all wages at the hundredfold point")
says("G4 the cost of a floor in 1955", f"In 1955 it would have cost between {p0(c.floor_gdp_family4)} and {p0(c.floor_gdp_single)} percent of everything America produced")
says("G5 and in 2024", f"In 2024 it would cost between {p0(b.floor_gdp_family4)} and {p0(b.floor_gdp_single)} percent.")
says("G5b the same again", f"But {p0(b.floor_gdp_family4)} to {p0(b.floor_gdp_single)} percent of the country's output raised through today's tax system")
for key in ("floor_gdp_family4", "floor_gdp_single"):
    band(f"G6 'would take about a third as much of its output as it would have seventy years ago': {key}, 2024 over 1955", float(b[key] / c[key]), 0.30, 0.38)
band("G7 '$1,000 a month ... more than two and a half times the dividend'", 1000.0 / (div["a_person"] / 12), 2.5, 3.0)

# ---------------------------------------------------------------------------------------------------------------- H
k0, k1, k2 = pg.common_income(0.0), pg.common_income(1.0), pg.common_income(2.0)
says("H1 what America taxes", f"It raises {p0(tau)} percent of its revenue from pay for work")
says("H2 who is paid for what under the program",
     f"Pay for work goes from {p0(k0['work'])} percent of all income today to {p0(k1['work'])} at the hundredfold point and to less than 1 in "
     f"the end. What is held in common, the public's fifth of the machines plus the growth in land rent, goes from {p0(k0['common'])} percent of "
     f"all income today to {p0(k1['common'])} at the hundredfold point and {p0(k2['common'])} in the end. The remaining {p0(k2['saving'])} "
     f"percent goes to those who saved.")
band("H3 'that is about half'", float(k2["common"]), 0.45, 0.55)
says("H4 the dividend in the limit", f"the dividend is {p0(k2['common'])} percent of the average income")
band("H5 'it costs more than twice as many years of saving'", yrs(later, 0.05, 0.05) / yrs(short, 0.05, 0.05), 2.0, 2.5)
band("H6 'a tenth of the households receive three-fifths of the income'", float(share(tt, 0.17)), 0.58, 0.64)
check("H7 'nine households in ten lean on pay more heavily than a balanced household would': pay's part of market income, each of "
      "the first nine tenths against all households'", bool((of_market.iloc[:9] > work.sum() / (work.sum() + owning.sum())).all()))

# ---------------------------------------------------------------------------------------------------------------- T
VIVALT = dict(monthly=1000, comparison=50, less_income=1900)   # Vivalt and others, NBER Working Paper 32719, abstract as revised August 2026
more = 12 * (VIVALT["monthly"] - VIVALT["comparison"])
says("T1 what the experiment's participants received and what happened to their other income",
     f"Its participants received {usd(more)} a year more than the comparison group, and their other income ended up about "
     f"{usd(VIVALT['less_income'])} a year lower.")
band("T2 'they took roughly a sixth of the money as time'", VIVALT["less_income"] / more, 0.15, 0.18)

# ---------------------------------------------------------------------------------------------------------------- Q
# Quotations and outside facts. Each was read on 2026-11-10 at the source named; the pages are not stored in the repository, so
# these lines hold only that the essay still prints what was read.
QUOTED = [
    ("Keynes, Economic Possibilities for our Grandchildren (1930), read at marxists.org",
     ['"the standard of life in progressive countries one hundred years hence will be between four and eight times as high as it is to-day."',
      '"Three-hour shifts or a fifteen-hour week"', '"science and compound interest."']),
    ("Acemoglu and Restrepo (2018), abstract, from Crossref (10.1257/aer.20160696)",
     ['"reduces employment and the labor share, and may even reduce wages."', '"has the opposite effects."']),
    ("Acemoglu and Restrepo (2022), abstract, from Crossref (10.3982/ecta19815)",
     ["between 50 and 70 percent of the change in America's wage structure",
      '"relative wage declines of worker groups specialized in routine tasks in industries experiencing rapid automation."']),
    ("29 U.S.C. 207(a)(1), from the Fair Labor Standards Act of 1938, section 7, read at law.cornell.edu",
     ["The forty-hour week was written into American law by an act of 1938, and the law still says forty."]),
    ("nobelprize.org, economic sciences, 1973 and 2024",
     ["was given the Nobel prize in economics for it in 1973", "Daron Acemoglu, who shared the Nobel prize in economics in 2024"]),
    ("Norges Bank Investment Management, About the fund, nbim.no",
     ['"almost 1.5 percent of all shares in the world\'s listed companies."', "Less than half of the fund's value is oil money that was paid in.",
      '"still amounts to almost 20 percent of the government budget."']),
    ("Paine, Agrarian Justice (1797), read at en.wikisource.org",
     ['"Man did not make the earth,"', '"every proprietor therefore of cultivated land, owes to the community a ground-rent,"',
      '"It is not charity but a right,"', '"The fault, however, is not in the present possessors,"',
      "every person would receive a sum of money on turning twenty-one"]),
    ("George, Progress and Poverty (1879), Project Gutenberg 55308",
     ['"It is not necessary to confiscate land; it is only necessary to confiscate rent."']),
    ("Alaska Department of Revenue, Summary of Dividend Applications and Payments, pfd.alaska.gov; Alaska Permanent Fund Corporation, apfc.org",
     ["Since 1982 the state of Alaska has paid every resident a yearly dividend",
      "It paid $1,312 a person in 2023 and $1,702 in 2024, to more than 600,000 people each year, and the fund behind it is worth $88 billion."]),
    ("Swedish Pensions Agency, National public pension, pensionsmyndigheten.se",
     ["Of the 18.5 percent of pay that goes toward the public pension, 2.5 goes into what is called a premium pension"]),
    ("Jones and Marinescu (2022), abstract, from Crossref (10.1257/pol.20190299)",
     ['"had no effect on employment" and that part-time work rose by 1.8 percentage points']),
    ("Vivalt and others, NBER Working Paper 32719, abstract as revised August 2026, read at nber.org",
     ["gave 1,000 low-income people $1,000 a month for three years", "They worked one to two hours a week less than a comparison group, and about "
      "four in a hundred more of them were out of the labor force.", '"a moderate labor supply effect."',
      '"the greatest increase generated by the transfer was in time spent on leisure,"',
      "they found no improvement in the quality of the jobs people held"]),
    ("Caselli and Manning (2019) and Korinek and Suh (2024), abstracts, from Crossref",
     ["new technology is unlikely to lower the wages of all workers", "wages collapse if the tasks people can perform are bounded in difficulty"]),
]
ALASKA = dict(paid_2023=624_354, paid_2024=624_489, fund_bn=88.0454)   # as the two Alaskan pages print them
for source, passages in QUOTED:
    missing = [p for p in passages if re.sub(r"\s+", " ", p) not in TEXT]
    check(f"Q  as read: {source}", not missing, "" if not missing else "not in the essay: " + " | ".join(missing))
check("Q2 'to more than 600,000 people each year' and a fund 'worth $88 billion'", min(ALASKA["paid_2023"], ALASKA["paid_2024"]) > 600_000
      and d0(ALASKA["fund_bn"]) == "88")

# ---------------------------------------------------------------------------------------------------------------- N
if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
    panel = pd.read_csv(sys.argv[1]).set_index("year")
    w = panel["wage_exshelter"]
    sf = ws.shortfall(panel, 1973, 2024)
    s_ = sf["shortfall"]
    says("N1 the wage, with the panel given",
         f"From 1950 to 1973 it grew by {d1(100 * ws.rate(w, 1950, 1973))} percent a year, and by 1973 an hour of work bought "
         f"{p0(w[1973] / w[1950] - 1)} percent more than it had in 1950. Then it stopped. From 1973 to 1995 it fell by "
         f"{d1(-100 * ws.rate(w, 1973, 1995))} percent a year. Since 1995 it has grown again, by {d1(100 * ws.rate(w, 1995, 2024))} percent a year. "
         f"In 2024 an hour of ordinary work bought {p0(w[2024] / w[1973] - 1)} percent more than it had in 1973, fifty-one years earlier. If the "
         f"earlier pace had held, it would have bought {d1(np.exp(s_))} times what it does.")
    says("N2 the gap divided, with the panel given",
         f"Slower growth in what an hour of work produces accounts for {p0(sf['output'] / s_)} percent of it. Pay spreading out among workers, so "
         f"that the average pulled away from the ordinary worker, accounts for {p0(sf['dispersion'] / s_)} percent. The shift of income from pay "
         f"to ownership accounts for {p0(sf['share'] / s_)} percent. The remaining {p0(sf['left_over'] / s_)} percent I can't assign. Count "
         f"housing costs in and the gap is a little wider, and the rising price of shelter is {p0(sf['shelter'] / sf['all_items'])} percent of "
         f"that wider gap.")
    band("N3 'the parts that are truly a move from work to ownership come to a little over a fifth'", float((sf["share"] + sf["shelter"]) / sf["all_items"]), 0.20, 0.24)
    band("N5 'an hour of ordinary work buys only a fifth more than it did fifty years ago': 2024 over 1973", float(w[2024] / w[1973] - 1), 0.17, 0.22)
    band("N6 'and housing costs more': the part of the gap on the all-items wage that the price of shelter adds", float(sf["shelter"]), 0.0001, 1.0)
    for part in (0.5, 0.7):
        band(f"N4 'about a third of the missing wage growth': the shift to ownership and {part:.0%} of the spreading-out",
             float((sf["share"] + part * sf["dispersion"]) / s_), 0.28, 0.38)
else:
    print("NOT HELD  the wage figures in 'Has anything changed yet?' (2.2, 0.6 and 1.1 percent a year; 66 and 19 percent; 2.6 times; 42, 30, "
          "16, 13 and 8 percent; a little over a fifth; about a third; only a fifth more than fifty years ago): give the backward model's panel as an argument to hold them")
print("NOT HELD  the land-tax figures in 'What about land?' (about $250 a month, 85 percent, 45 percent): they are the consumption branch's, "
      "consumption/lvt/NOTES_us.md, and provisional")

n_ok = sum(RESULTS)
print(f"\n{n_ok}/{len(RESULTS)} checks green")
sys.exit(0 if n_ok == len(RESULTS) else 1)
