# check_essay.py — the numbers essay/essay.md prints are the ones the scripts produce.
#
# The same test as check_draft.py, on the essay ("Why Are We Still Working This Hard?"). Each `says` line is a sentence or
# table row of the essay with its numbers filled in from the stored tables and the scripts, formatted as the essay prints
# them: it passes when the filled text is in the essay, so it fails if the data move and it fails if a number in the essay
# is changed. Numbers the essay gives in words (two and a half times, sixteen hours, about a seventh) are held by `band`
# and `check` lines, each inside a stated range.
#   A  the opening (output a person since 1930; output per hour and hours a head since 1973) and the consumer's dollar
#   B  who lives on what
#   C  where the gain went: output per hour against ordinary pay
#   D  the model economy: the path, what incomes buy, the tax and the stake, the price of ownership
#   E  land
#   F  the program for the United States
#   G  the dividend and the cost of a floor
#   H  fairness
#   T  the worth of time: the experiment's figures, as its summary prints them
#   Q  quotations and outside facts: transcriptions, each read at the source named beside it
#   N  not held on this branch: listed, and held when their inputs are given
# The figures for ordinary pay need the backward model's panel, which is on another branch; give its path to hold them too:
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
real_gdp, people = rb.annual("paths/cache/GDPCA.csv"), rb.annual(pg.POPULATION)
per = real_gdp / people
oph, hours = ws.annual("paths/cache/OPHNFB.csv"), ws.annual("paths/cache/HOANBS.csv")
since = oph[2024] / oph[1973]
a_head = (hours[2024] / hours[1973]) / (people[2024] / people[1973]) - 1.0
says("A1 Keynes's first forecast", f"Output per person in the United States in 2024 was {d1(per[2024] / per[1930])} times its level in 1930")
check("A1b 'at the top of his range with six years still to run': between four and eight times, nearer eight, and 2030 less 2024",
      7.0 < per[2024] / per[1930] <= 8.0 and 1930 + 100 - 2024 == 6)
band("A2 'an hour of work in American business in 2024 produced two and a half times what an hour produced in 1973'", float(since), 2.4, 2.6)
check("A3 'what took a forty-hour week to make then takes sixteen hours now'", d0(40.0 / since) == "16", f"{40.0 / since:.1f} hours")
says("A4 hours worked for each head of population", f"the hours worked in American business in 2024 were {p0(a_head)} percent higher than in 1973")
check("A4b 'we took the whole of that half-century's progress as more output and none of it as time': hours a head did not fall", a_head > 0)

made, fin = obt.made(), obt.financing()
r, f23 = made.loc[2023], fin.loc[2023]
lab = made.labour_factor_psi38
owning_cents = r.comp + r.nos - r.labour_dollar_psi38
says("A5 the dollar",
     f"{p0(r.imports)} cents leaves the country for imports, {p0(r.tax)} cents is tax on the product, {p0(r.labour_dollar_psi38)} cents is "
     f"pay for work, and 27 and a half cents goes to the owners of machines and land")
band("A5b '27 and a half cents'", float(owning_cents), 0.2725, 0.2775)
check("A5c the four parts of the dollar add to one (1e-6)", abs(r.imports + r.tax + r.labour_dollar_psi38 + owning_cents - 1) < 1e-6)
says("A6 the part paid at home", f"Work gets {p0(lab[2023])} percent of it and ownership gets {p0(1 - lab[2023])}.")
says("A7 the second count", f"I get the same {p0(f23.fin_labour)} percent a second way")
check("A7b the two counts print the same whole percent", p0(f23.fin_labour) == p0(lab[2023]))
band("A8 'two-thirds of what we buy is paid for by work, and one-third is paid to people for owning things'", float(lab[2023]), 0.64, 0.69)
says("A9 the gauge to watch", f"which was {p0(lab.max())} percent in {int(lab.idxmax())} and {p0(lab[2023])} in 2023")
says("A10 shelter and the rest",
     f"Work makes {p0(r.rest_labour_factor_psi38)} percent of everything else in the household budget and {p0(r.shelter_labour_factor)} "
     f"percent of shelter.")
says("A11 what a tax on spending would rest on today", f"because pay for work covers {p0(f23.fin_labour)} percent of what households buy")

# ---------------------------------------------------------------------------------------------------------------- B
tabs = ex.inputs()
a23 = ex.amounts(tabs, 2023)
work = a23.comp + ex.PSI * a23.prop
owning = (1.0 - ex.PSI) * a23.prop + a23.rent + a23.interest + a23.dividends + a23.accrued
of_market = work / (work + owning)
tau = float(tabs["tax"].loc[2023, "lamR_med"])
held, s_now = ex.market_shares(tabs, 2023)
bh, nf, tt = held["bottom half"], held["next four tenths"], held["top tenth"]
g5, _ = pg.gaps(tabs, 2023, pg.THETA)
N = "next four tenths"
share = ex.income_share

band("B1 'the poorest tenth lives mostly on government benefits': their share of its income", float(a23.benefits.iloc[0] / (work + owning + a23.benefits).iloc[0]), 0.5, 1.0)
band("B2 'from the second tenth to the ninth ... about four-fifths is pay for work': the lowest of the eight", float(of_market.iloc[1:9].min()), 0.76, 0.84)
band("B2b the highest of the eight", float(of_market.iloc[1:9].max()), 0.76, 0.84)
band("B3 'in the richest tenth pay and ownership are about half and half': pay's part of its market income", float(of_market.iloc[9]), 0.47, 0.53)
band("B4 'that tenth earns a bit over a third of all the pay for work'", float(tt["labour"]), 0.34, 0.37)
band("B5 'and receives two-thirds of all the income from ownership'", float(tt["capital"]), 0.64, 0.69)
check("B6 'nine households in ten' against one: pay's part of market income is above all households' in each of the first nine tenths "
      "and below it in the richest", bool((of_market.iloc[:9] > work.sum() / (work.sum() + owning.sum())).all())
      and of_market.iloc[9] < work.sum() / (work.sum() + owning.sum()))
says("B7 the tax base",
     f"{p0(tau)} cents of every tax dollar in America is raised from pay for work (somewhere between "
     f"{p0(float(tabs['tax'].loc[2023, 'lamR_min']))} and {p0(float(tabs['tax'].loc[2023, 'lamR_max']))}")
check("B8 'sixty-eight cents of every tax dollar is raised from pay'", p0(tau) == "68")

# ---------------------------------------------------------------------------------------------------------------- C
_, s0, s1 = ex.shift_share(tabs, 2004, 2023)
check("C1 'what an hour of work produced rose by 81 percent' from 1950 to 1973", p0(oph[1973] / oph[1950] - 1) == "81")
says("C2 the last twenty years", f"that is pay for work fell from {p0(s0)} percent to {p0(s1)}.")

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
     f"{d0(one['wage_good'] / start['wage_good'])} times as many goods as it does today.")
band("D6 'the rent of land rises about a hundredfold'", float(one["real_rent"] / start["real_rent"]), 95.0, 115.0)
band("D7 'an hour's pay rents about a twelfth of the land it does now'", float(start["wage_rent"] / one["wage_rent"]), 11.0, 13.0)
says("D8 the owners' income", f"The income of those who own machines and land is {d0(owners)} times what it was.")
for t in (1.25, 1.5, 2.0):
    band(f"D9 'the hourly wage levels off at around ten times today's': when machines are {100 ** t:,.0f} times better",
         float(pp.point(t)["real_wage"] / start["real_wage"]), 9.0, 11.5)
band("D10 'the economy goes on to grow more than fiftyfold again': income at ten thousand times over income at a hundred",
     float(two["real_income"] / one["real_income"]), 50.0, 60.0)
band("D10b 'it delivers a sixth of the income at the hundredfold point'", float(m1["labour"]), 0.15, 0.185)
band("D11 'its share of income more than triples': land", float(m1["rent"] / m0["rent"]), 3.0, 4.0)
says("D12 the owners of machines", f"whose share goes from {p0(m0['interest'])} percent to {p0(m1['interest'])} and then to {p0(m2['interest'])}")
band("D13 'over fifty times as many' machines at the hundredfold point", float(one["real_capital"] / start["real_capital"]), 50.0, 60.0)
low = pp.point(1.0, dict(pp.PAR, rho=0.05))
check("D14 'if investors came to accept 5 percent ... land the larger share and machines the smaller. The share paid for work comes out "
      "about the same'", low["rent"] > low["interest"] and abs(low["labour"] - m1["labour"]) < 0.02,
      f"at 5 percent: work {low['labour']:.3f}, machines {low['interest']:.3f}, land {low['rent']:.3f}")
says("D15 who would receive the income",
     f"the richest tenth of American households would receive {p0(share(tt, 0.17))} percent of all market income, up from {p0(share(tt, s_now))}. "
     f"The four tenths below them would go from {p0(share(nf, s_now))} percent to {p0(share(nf, 0.17))}, and the poorer half from 14 and a half "
     f"to {p0(share(bh, 0.17))}.")
band("D15b '14 and a half'", float(share(bh, s_now)), 0.1425, 0.1475)
says("D16 how long a hundredfold takes", f"A hundredfold improvement takes {d0(math.log(100) / math.log(1.04))} years at 4 percent a year")
says("D16b at faster paces", f"At 10 percent a year it takes {d0(math.log(100) / math.log(1.10))} years, and at 20 percent, {d0(math.log(100) / math.log(1.20))}.")
PRINTED = dict(no_ceiling=0.48)   # Båge and Wilson (2026), Section 8.4, as printed: the same path with no limit on people's advantage
says("D17 without a ceiling on human advantage, as that paper prints it", f"lowers work's share to {p0(PRINTED['no_ceiling'])} percent and stops there")
says("D18 the tax on what machines earn",
     f"the tax raises {p1(tax['revenue'])} percent of national income. Wages fall by {p1(-tax['wages'])} percent of national income. The "
     f"economy as a whole is {p1(1 - tax['real_income'])} percent smaller. If every dollar the tax raised were handed straight to wage earners, "
     f"they would end up {p1(tax['wage_earner'])} percent better off")
band("D19 'a smaller pile, about a fifth smaller'", float(1 - tax["real_capital"]), 0.17, 0.22)
band("D20 a fifth of the machines 'costs about a year of the whole country's wages'", 0.2 * c0["capital"], 0.95, 1.10)
says("D21 the stake", f"which is {p1(fifth)} percent of national income in the model")
band("D21b the tax and the stake raise 'almost the same money': the difference, as a share of income", float(tax["revenue"] - fifth), 0.0, 0.002)
says("D22 what the stake undoes",
     f"an economy {p1(1 - tax['real_income'])} percent smaller and wages lower by {p1(-tax['wages'])} percent of national income")
says("D23 what ownership costs", f"is worth about {d1(c0['both'])} years of the whole country's wages")
says("D23b at the threshold and at the hundredfold point", f"At the threshold it is {d0(cth['both'])} years. At the hundredfold point it is {d0(c1['both'])}.")
says("D24 the door",
     f"The saving that takes a household in the comfortable middle {d0(yrs(short, 0.05, 0.05))} years today takes "
     f"{d0(yrs(later, 0.05, 0.05))} years there.")

# ---------------------------------------------------------------------------------------------------------------- E
t = rb.table()
b, c = t.loc[2024], t.loc[1955]
says("E1 the rent of the ground under homes",
     f"came in 2024 to between {p1(b.share_dpi_30)} and {p1(b.share_dpi_50)} percent of households' disposable income, which is between "
     f"{usd(b.rent_pp_30_last)} and {usd(b.rent_pp_50_last)} a year for every person in the country")
band("E2 'by the usual arithmetic is about 40 percent of the land's value': growth of 2 percent over a discount rate of 5", 0.02 / 0.05, 0.3999, 0.4001)
says("E3 what that is of a house", f"For a house whose value is three-tenths to a half land, that is {p0(0.4 * 0.3)} to {p0(0.4 * 0.5)} percent off the price.")

# ---------------------------------------------------------------------------------------------------------------- F
STATUTE = dict(corporate=0.21, oasdi_each=0.062)   # 26 U.S.C. 11(b), 3101(a) and 3111(a), read at law.cornell.edu on 2026-11-10
div, pub_claims, rc, bn = pg.dividend(tabs, 2023), pg.public_claims(tabs, 2023), pg.receipts(2023), pg.benefits(2023)
head = people[2023] * 1e3
says("F1 the table, company profits",
     f"| Company profits | Taxed at {p0(STATUTE['corporate'])} percent by the federal government. All levels of government raised "
     f"${pub_claims['corporate']:.0f} billion from them in 2023")
says("F2 the table, land", f"through property taxes, which raised ${rc['property_bn']:.0f} billion.")
says("F3 the table, saving for old age", f"| Saving for old age | {p1(2 * STATUTE['oasdi_each'])} percent of wages goes to Social Security")
says("F4 the table, taxes on work",
     f"| Taxes on work | {p0(tau)} percent of all tax revenue is raised from pay. Payroll contributions alone are a quarter of everything collected.")
band("F4b 'a quarter of everything collected' is payroll contributions", float(rc["contributions"]), 0.24, 0.26)
says("F5 the dividend", f"In 2023 it would have paid {usd(div['a_person'])} a person, or {usd(div['a_person'] / 12)} a month")
check("F5b 'more than Social Security pays out per head of population'", div["a_person"] > bn["social_security_bn"] * 1e9 / head,
      f"{div['a_person']:,.0f} against {bn['social_security_bn'] * 1e9 / head:,.0f}")
says("F6 the tax on profits as a stake", f"is worth {p0(pub_claims['corporate_share'])} percent of all ownership income")
band("F7 'about two-fifths of the rent after twenty-five years of growth at 2 percent a year'", float(pub_claims["grown"]), 0.38, 0.41)
says("F8 the growth of land rent", f"which comes to another {p0(pub_claims['growth_share'][0])} to {p0(pub_claims['growth_share'][1])} percent")
check("F9 'together that is about a seventh of all ownership income': a seventh lies between the two ends",
      pub_claims["together"][0] < 1 / 7 < pub_claims["together"][1], f"{pub_claims['together'][0]:.3f} to {pub_claims['together'][1]:.3f}")
check("F9b 'most of that fifth is within reach without buying anything'", pub_claims["together"][0] > 0.5 * pg.THETA)
says("F10 what paying out the profits tax would cost", f"so paying it out means finding ${pub_claims['corporate']:.0f} billion a year somewhere else")
band("F11 'about a seventh held in common is enough ... even if wages went to nothing': the poorer half", float(ex.holding_share(bh, s_now, 0.0)), 0.125, 0.16)
band("F11b the same if work is paid 17 percent", float(ex.holding_share(bh, s_now, 0.17)), 0.125, 0.16)
band("F12 'they earn nearly half of all the pay in the country'", float(nf["labour"]), 0.45, 0.50)
band("F13 'no common share short of six-sevenths of everything would keep them whole'", float(ex.holding_share(nf, s_now, 0.17)), 0.85, 0.87)
says("F14 saving out of wages",
     f"saving 5 percent of pay and reinvesting what it earns at 5 percent a year would do it in {d0(yrs(short, 0.05, 0.05))} years, which is a "
     f"working life")
says("F15 Social Security's tax", f"far more than that from wages for retirement, {p1(2 * STATUTE['oasdi_each'])} percent, for Social Security")
band("F16 'at the hundredfold point in the model, five-sixths of a tax on spending would be paid out of ownership income'", float(1 - m1["labour"]), 0.81, 0.85)
says("F17 the hard case",
     f"the richest tenth's share of market income goes from {p0(share(tt, s_now))} percent to {p0(share(tt, 0.17))}. With a fifth held in common "
     f"it goes to {p0(share(tt, 0.17, 0.2))}, and the poorer half ends up with {p0(share(bh, 0.17, 0.2))} percent, which is more than it has now. "
     f"The comfortable middle still falls, from {p0(share(nf, s_now))} percent to {p0(share(nf, 0.17, 0.2))}")
check("F17b 'which is more than it has now'", share(bh, 0.17, 0.2) > share(bh, s_now))

# ---------------------------------------------------------------------------------------------------------------- G
says("G1 a benefit out of today's taxes", f"for {p0(tau)} cents in the dollar, wage earners paying each other")
says("G2 the size of the dividend",
     f"A dividend of {usd(div['a_person'] / 12)} a month is {p0(div['family4'])} percent of the poverty line for one member of a family of four "
     f"and {p0(div['single'])} percent for a person living alone.")
says("G3 the dividend along the path",
     f"the income of a common fifth is {p0(pg.path_dividend(0.0)['of_wages'])} percent of all wages today and "
     f"{p0(pg.path_dividend(1.0)['of_wages'])} percent of all wages at the hundredfold point")
says("G4 the cost of a floor in 1955",
     f"would have cost between {p0(c.floor_gdp_family4)} and {p0(c.floor_gdp_single)} percent of everything the country produced")
says("G5 and in 2024", f"In 2024 it would cost between {p0(b.floor_gdp_family4)} and {p0(b.floor_gdp_single)} percent.")

# ---------------------------------------------------------------------------------------------------------------- H
k0, k1, k2 = pg.common_income(0.0), pg.common_income(1.0), pg.common_income(2.0)
says("H1 what America taxes", f"It raises {p0(tau)} percent of its revenue from pay for work")
says("H2 who is paid for what under the program",
     f"pay for work goes from {p0(k0['work'])} percent of all income today to {p0(k1['work'])} at the hundredfold point and to less than 1 in "
     f"the end. What is held in common, the public's fifth of the machines plus the growth in land rent, goes from {p0(k0['common'])} percent of "
     f"all income today to {p0(k1['common'])} at the hundredfold point and {p0(k2['common'])} in the end. The remaining {p0(k2['saving'])} "
     f"percent goes to those who saved.")
band("H3 'that is about half'", float(k2["common"]), 0.45, 0.55)
band("H4 'it costs more than twice as many years of saving'", yrs(later, 0.05, 0.05) / yrs(short, 0.05, 0.05), 2.0, 2.5)
band("H5 'a tenth of the households receive three-fifths of the income'", float(share(tt, 0.17)), 0.58, 0.64)

# ---------------------------------------------------------------------------------------------------------------- T
VIVALT = dict(monthly=1000, comparison=50, less_income=1900)   # Vivalt and others, NBER Working Paper 32719, abstract as revised August 2026
more = 12 * (VIVALT["monthly"] - VIVALT["comparison"])
says("T1 what the experiment's participants received and what happened to their other income",
     f"Those people received {usd(more)} a year more than a comparison group, and their other income ended up about "
     f"{usd(VIVALT['less_income'])} a year lower.")
band("T2 'they took roughly a sixth of the money as time'", VIVALT["less_income"] / more, 0.15, 0.18)

# ---------------------------------------------------------------------------------------------------------------- Q
# Quotations and outside facts. Each was read on 2026-11-10 at the source named; the pages are not stored in the repository, so
# these lines hold only that the essay still prints what was read.
QUOTED = [
    ("Keynes, Economic Possibilities for our Grandchildren (1930), read at marxists.org",
     ['"the standard of life in progressive countries one hundred years hence will be between four and eight times as high as it is to-day."',
      '"Three-hour shifts or a fifteen-hour week"']),
    ("29 U.S.C. 207(a)(1), from the Fair Labor Standards Act of 1938, section 7, read at law.cornell.edu",
     ["The forty-hour week was written into American law by an act of 1938, and the law still says forty."]),
    ("nobelprize.org, economic sciences, 1973 and 2024",
     ["was given the Nobel prize in economics for it in 1973", "Daron Acemoglu, who shared the Nobel prize in economics in 2024"]),
    ("Acemoglu and Restrepo (2018), abstract, from Crossref (10.1257/aer.20160696)",
     ['"reduces employment and the labor share, and may even reduce wages."', '"has the opposite effects."']),
    ("Acemoglu and Restrepo (2022), abstract, from Crossref (10.3982/ecta19815)",
     ["between 50 and 70 percent of the change in America's wage structure",
      '"relative wage declines of worker groups specialized in routine tasks in industries experiencing rapid automation."']),
    ("Alaska Department of Revenue, Summary of Dividend Applications and Payments, pfd.alaska.gov; Alaska Permanent Fund Corporation, apfc.org",
     ["since 1982 has paid every resident a yearly dividend out of a fund built from its oil revenues",
      "Alaska's dividend paid $1,312 a person in 2023 and $1,702 in 2024, to more than 600,000 people each year, and the fund behind it is "
      "worth $88 billion."]),
    ("Jones and Marinescu (2022), abstract, from Crossref (10.1257/pol.20190299)",
     ['"had no effect on employment" and that part-time work rose by 1.8 percentage points']),
    ("Vivalt and others, NBER Working Paper 32719, abstract as revised August 2026, read at nber.org",
     ["They gave 1,000 low-income people $1,000 a month for three years", "They worked one to two hours a week less",
      '"the greatest increase generated by the transfer was in time spent on leisure."', '"a moderate labor supply effect,"',
      "they found no improvement in the quality of the jobs people held"]),
    ("Caselli and Manning (2019) and Korinek and Suh (2024), abstracts, from Crossref",
     ["new technology is unlikely to lower the wages of all workers", "wages collapse if the tasks people can perform are bounded in difficulty"]),
    ("Paine, Agrarian Justice (1797), read at en.wikisource.org",
     ['"Man did not make the earth,"', '"every proprietor therefore of cultivated land, owes to the community a ground-rent,"',
      '"It is not charity but a right,"', '"The fault, however, is not in the present possessors,"',
      "every person would receive a sum of money on turning twenty-one"]),
    ("George, Progress and Poverty (1879), Project Gutenberg 55308",
     ['"It is not necessary to confiscate land; it is only necessary to confiscate rent."']),
    ("Norges Bank Investment Management, About the fund, nbim.no",
     ['"almost 1.5 percent of all shares in the world\'s listed companies,"', '"still amounts to almost 20 percent of the government budget."']),
    ("Swedish Pensions Agency, National public pension, pensionsmyndigheten.se",
     ["puts 2.5 of the 18.5 percent of pay that goes toward the public pension into invested accounts that belong to the worker"]),
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
    w, spread = panel["wage_exshelter"], panel["pay_gap"]
    ls = ws.annual("paths/cache/PRS85006173.csv")
    pay = w[2024] / w[1973]
    gap = np.log(since) - np.log(pay)                                  # how far ordinary pay fell behind output per hour, in logs
    parts = dict(spreading=np.log(spread[2024] / spread[1973]) / gap, ownership=-np.log(ls[2024] / ls[1973]) / gap)
    parts["rest"] = 1.0 - parts["spreading"] - parts["ownership"]
    check("N1 'to buy what forty hours of ordinary pay bought in 1973 ... has to work thirty-four hours'", d0(40.0 / pay) == "34", f"{40.0 / pay:.1f} hours")
    says("N2 from 1950 to 1973, with the panel given",
         f"What an hour of work produced rose by {p0(oph[1973] / oph[1950] - 1)} percent, and what an hour of ordinary pay could buy rose by "
         f"{p0(w[1973] / w[1950] - 1)} percent.")
    says("N3 from 1973 to 2024, with the panel given",
         f"Between 1973 and 2024 the output of an hour rose two and a half times, and an hour of ordinary pay came to buy {p0(pay - 1)} percent more.")
    band("N4 'about two-fifths of it is pay spreading out among workers'", float(parts["spreading"]), 0.35, 0.42)
    band("N5 'a fifth is income moving from pay to ownership'", float(parts["ownership"]), 0.17, 0.23)
    band("N6 'the remaining two-fifths I can't separate cleanly'", float(parts["rest"]), 0.38, 0.45)
    band("N7 'ordinary pay did rise, by a fifth'; 'an hour of ordinary pay buys a fifth more'", float(pay - 1), 0.17, 0.22)
    band("N8 'which could have been six hours off the week at the same standard of living'", float(40.0 - 40.0 / pay), 5.5, 6.7)
else:
    print("NOT HELD  the figures for ordinary pay (thirty-four hours; 66 and 19 percent; two-fifths, a fifth and two-fifths of the gap; six hours "
          "off the week): give the backward model's panel as an argument to hold them")
print("NOT HELD  the land-tax figures in 'What about land?' (about $250 a month, 85 percent, 45 percent): they are the consumption branch's, "
      "consumption/lvt/NOTES_us.md, and provisional")

n_ok = sum(RESULTS)
print(f"\n{n_ok}/{len(RESULTS)} checks green")
sys.exit(0 if n_ok == len(RESULTS) else 1)
