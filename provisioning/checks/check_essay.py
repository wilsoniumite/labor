# check_essay.py — the numbers essay/essay.md prints are the ones the scripts produce.
#
# The same test as check_draft.py, on the essay ("Why Are We Still Working This Hard?", third version). Each `says` line is
# a sentence of the essay with its numbers filled in from the stored tables and the scripts, formatted as the essay prints
# them: it passes when the filled text is in the essay, so it fails if the data move and it fails if a number in the essay
# is changed. Numbers the essay gives in words (sixteen hours, two and a half times, about a seventh) are held by `band`
# and `check` lines, each inside a stated range.
#   A  the opening: output per hour and hours for each head of population since 1973; output a person since 1930
#   B  how much rides on the wage: the consumer's dollar, who lives on what, the tax base
#   C  the eighteen hours: output per hour against ordinary pay (the pay figures are in N)
#   D  the model economy
#   E  what would fix it: the tax and the stake, land
#   F  what it would take: the dividend, the saving, the price of ownership
#   G  fairness and the grounds for hope
#   T  the experiment's figures, as its summary prints them
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
make = 40.0 / since
a_head = (hours[2024] / hours[1973]) / (people[2024] / people[1973]) - 1.0
check("A1 'what a forty-hour week of work produced in 1973 takes sixteen hours to produce today'", d0(make) == "16", f"{make:.1f} hours")
band("A2 'an hour of work in American business now makes two and a half times what it made in 1973'", float(since), 2.4, 2.6)
check("A3 'for every forty hours that used to be needed, twenty-four have been freed'", d0(40.0 - make) == "24", f"{40.0 - make:.1f} hours")
says("A4 hours worked for each head of population", f"the hours worked in American business in 2024 were {p0(a_head)} percent higher than in 1973")
check("A4b 'we took the whole of fifty years' progress as more output and none of it as time': hours a head did not fall", a_head > 0)
says("A5 Keynes's first forecast", f"Output per person in the United States in 2024 was {d1(per[2024] / per[1930])} times its level in 1930")
check("A5b his range was four to eight times, and 'a society eight times as rich' is its upper end", 4.0 <= per[2024] / per[1930] <= 8.0)

# ---------------------------------------------------------------------------------------------------------------- B
made = obt.made()
lab = made.labour_factor_psi38
tabs = ex.inputs()
a23 = ex.amounts(tabs, 2023)
work = a23.comp + ex.PSI * a23.prop
owning = (1.0 - ex.PSI) * a23.prop + a23.rent + a23.interest + a23.dividends + a23.accrued
of_market = work / (work + owning)
tau = float(tabs["tax"].loc[2023, "lamR_med"])
held, s_now = ex.market_shares(tabs, 2023)
bh, nf, tt = held["bottom half"], held["next four tenths"], held["top tenth"]
share = ex.income_share

says("B1 the dollar", f"{p0(lab[2023])} percent is pay for work and {p0(1 - lab[2023])} percent goes to owners")
band("B1b 'a third of the economy ... already pays people for owning things'; 'two-thirds of what Americans buy is paid for by work'", float(lab[2023]), 0.64, 0.69)
band("B2 'the poorest tenth ... lives mostly on government benefits': their share of its income", float(a23.benefits.iloc[0] / (work + owning + a23.benefits).iloc[0]), 0.5, 1.0)
band("B3 'from the second tenth to the ninth, about four-fifths ... is pay for work': the lowest of the eight", float(of_market.iloc[1:9].min()), 0.76, 0.84)
band("B3b the highest of the eight", float(of_market.iloc[1:9].max()), 0.76, 0.84)
band("B4 'in the richest tenth ... pay and ownership are about half and half': pay's part of its market income", float(of_market.iloc[9]), 0.47, 0.53)
band("B5 'that one tenth receives two-thirds of all the income from ownership'", float(tt["capital"]), 0.64, 0.69)
says("B6 the tax base", f"{p0(tau)} cents of every tax dollar in America is raised from pay for work")
check("B7 'nine households in ten are living on each other's wages': pay's part of market income is above all households' in each of the "
      "first nine tenths and below it in the richest", bool((of_market.iloc[:9] > work.sum() / (work.sum() + owning.sum())).all())
      and of_market.iloc[9] < work.sum() / (work.sum() + owning.sum()))
says("B8 the gauge to watch", f"was {p0(lab.max())} percent in {int(lab.idxmax())} and {p0(lab[2023])} in 2023")

# ---------------------------------------------------------------------------------------------------------------- C
check("C1 between 1950 and 1973 what an hour of work produced 'rose by 81 percent'", p0(oph[1973] / oph[1950] - 1) == "81")

# ---------------------------------------------------------------------------------------------------------------- D
start, one, two = pp.point(0.0), pp.point(1.0), pp.point(2.0)
m0, mten, m1, m2 = pp.mix(0.0), pp.mix(0.5), pp.mix(1.0), pp.mix(2.0)
c0, c1 = pp.claims(0.0), pp.claims(1.0)
tax = pp.interest_tax(0.20)
fifth = 0.2 * m0["interest"]
g5, _ = pg.gaps(tabs, 2023, pg.THETA)
N = "next four tenths"
short = g5[N]["short"]
later = pg.gaps(tabs, 2023, pg.THETA, m1["labour"])[0][N]["short"]
yrs = pg.years_to_match
owners = (one["real_income"] * (1 - one["labour"])) / (start["real_income"] * (1 - start["labour"]))
grown = one["real_income"] / start["real_income"]

says("D1 the model economy today",
     f"this economy pays {p0(m0['labour'])} percent of its income for work, {p0(m0['interest'])} percent to the owners of machines and "
     f"{p0(m0['rent'])} percent to the owners of land")
says("D2 at ten times", f"When machines are ten times better, work is still paid {p0(mten['labour'])} percent of all income")
band("D3 'at about 35 times': a hundred to the power 0.77", 100 ** 0.77, 33.0, 37.0)
check("D3b the threshold: the hours of work inside the machines that replace the hardest hour fall below one between 0.76 and 0.78",
      pp.point(0.76)["lam_bar"] > 1.0 > pp.point(0.78)["lam_bar"])
says("D4 at a hundred and at ten thousand times",
     f"By the hundredfold point work is paid {p0(m1['labour'])} percent of all income. At ten thousand times it is paid less than 1 percent.")
band("D4b 'less than 1 percent'", float(m2["labour"]), 0.0, 0.0099)
says("D5 what incomes buy at the hundredfold point",
     f"At the hundredfold point total income is {d0(grown)} times what it was, and an hour of work buys "
     f"{d0(one['wage_good'] / start['wage_good'])} times as many goods as it does today.")
band("D6 'an hour's pay rents about a twelfth of the land it does now'", float(start["wage_rent"] / one["wage_rent"]), 11.0, 13.0)
says("D7 the owners' income", f"the income of those who own machines and land is {d0(owners)} times what it was")
band("D8 'it delivers a sixth of the income'", float(m1["labour"]), 0.15, 0.185)
says("D9 who would receive the income",
     f"the richest tenth of American households would receive {p0(share(tt, 0.17))} percent of all market income, up from {p0(share(tt, s_now))}. "
     f"The poorer half would go from 14 and a half percent to {p0(share(bh, 0.17))}.")
band("D9b '14 and a half percent'", float(share(bh, s_now)), 0.1425, 0.1475)
says("D10 how long a hundredfold takes",
     f"a hundredfold improvement takes {d0(math.log(100) / math.log(1.04))} years at 4 percent a year, the pace at which machinery improved "
     f"for its price after the Second World War, and {d0(math.log(100) / math.log(1.20))} years at 20 percent")
PRINTED = dict(no_ceiling=0.48)   # Båge and Wilson (2026), Section 8.4, as printed: the same path with no limit on people's advantage
says("D11 without a ceiling on human advantage, as that paper prints it", f"the same dial stops with work at {p0(PRINTED['no_ceiling'])} percent")
says("D12 the richer world", f"That world is {d0(grown)} times richer than ours")
band("D13 'a tenth of the households receive three-fifths of the income'", float(share(tt, 0.17)), 0.58, 0.64)

# ---------------------------------------------------------------------------------------------------------------- E
says("E1 a benefit out of today's taxes", f"for {p0(tau)} cents in the dollar, wage earners paying each other")
says("E2 the tax on what machines earn",
     f"a 20 percent tax on what machines earn their owners raises {p1(tax['revenue'])} percent of national income, and wages fall by "
     f"{p1(-tax['wages'])} percent of national income")
says("E3 the stake", f"which is {p1(fifth)} percent of national income in the model")
band("E3b the tax and the stake raise almost the same: the difference, as a share of income", float(tax["revenue"] - fifth), 0.0, 0.002)
t = rb.table()
b, c = t.loc[2024], t.loc[1955]
says("E4 the rent of the ground under homes",
     f"came in 2024 to between {p1(b.share_dpi_30)} and {p1(b.share_dpi_50)} percent of households' disposable income, or between "
     f"{usd(b.rent_pp_30_last)} and {usd(b.rent_pp_50_last)} a year for every person in the country")
band("E5 'in the model, land's share of income more than triples'", float(m1["rent"] / m0["rent"]), 3.0, 4.0)

# ---------------------------------------------------------------------------------------------------------------- F
div, pub_claims = pg.dividend(tabs, 2023), pg.public_claims(tabs, 2023)
says("F1 the dividend", f"would have paid {usd(div['a_person'])} a person in 2023, or {usd(div['a_person'] / 12)} a month")
check("F2 the profits tax as a stake and the growth in land rent 'together come to about a seventh of all ownership income': a seventh lies "
      "between the two ends", pub_claims["together"][0] < 1 / 7 < pub_claims["together"][1],
      f"{pub_claims['together'][0]:.3f} to {pub_claims['together'][1]:.3f}")
check("F2b 'most of that fifth is within reach without buying anything'", pub_claims["together"][0] > 0.5 * pg.THETA)
says("F3 what paying out the profits tax would cost", f"so paying it out means finding ${pub_claims['corporate']:.0f} billion a year somewhere else")
band("F4 'a common share of about a seventh would be enough to keep the poorer half of households whole, even if wages went to nothing'",
     float(ex.holding_share(bh, s_now, 0.0)), 0.125, 0.16)
band("F4b the same if work is paid 17 percent", float(ex.holding_share(bh, s_now, 0.17)), 0.125, 0.16)
band("F5 'the comfortable middle, who earn nearly half of all the pay in the country'", float(nf["labour"]), 0.45, 0.50)
says("F6 saving out of wages",
     f"saving 5 percent of pay and reinvesting what it earns at 5 percent a year would do it in {d0(yrs(short, 0.05, 0.05))} years, which is a "
     f"working life")
says("F7 the size of the dividend", f"A dividend of {usd(div['a_person'] / 12)} a month is {p0(div['single'])} percent of the poverty line for a person living alone.")
says("F8 the dividend along the path",
     f"the income of a common fifth is {p0(pg.path_dividend(0.0)['of_wages'])} percent of all wages today and "
     f"{p0(pg.path_dividend(1.0)['of_wages'])} percent of all wages at the hundredfold point")
says("F9 what ownership costs", f"is worth about {d1(c0['both'])} years of the whole country's wages")
says("F9b at the hundredfold point", f"At the hundredfold point it is {d0(c1['both'])} years.")
says("F10 the deadline",
     f"The saving that takes a household in the comfortable middle {d0(yrs(short, 0.05, 0.05))} years today takes "
     f"{d0(yrs(later, 0.05, 0.05))} years there.")

# ---------------------------------------------------------------------------------------------------------------- G
k0, k1, k2 = pg.common_income(0.0), pg.common_income(1.0), pg.common_income(2.0)
says("G1 what America taxes", f"It raises {p0(tau)} percent of its revenue from pay for work")
says("G2 who is paid for what under the program",
     f"pay for work goes from {p0(k0['work'])} percent of all income today to {p0(k1['work'])} at the hundredfold point and to less than 1 in "
     f"the end. What is held in common, the public's fifth of the machines plus the growth in land rent, goes from {p0(k0['common'])} percent of "
     f"all income today to {p0(k1['common'])} at the hundredfold point and {p0(k2['common'])} in the end.")
band("G3 'that is about half'", float(k2["common"]), 0.45, 0.55)
says("G4 the cost of a floor in 1955",
     f"would have cost between {p0(c.floor_gdp_family4)} and {p0(c.floor_gdp_single)} percent of everything the country produced")
says("G5 and in 2024", f"In 2024 it would cost between {p0(b.floor_gdp_family4)} and {p0(b.floor_gdp_single)} percent.")

# ---------------------------------------------------------------------------------------------------------------- T
VIVALT = dict(monthly=1000, comparison=50, less_income=1900)   # Vivalt and others, NBER Working Paper 32719, abstract as revised August 2026
more = 12 * (VIVALT["monthly"] - VIVALT["comparison"])
says("T1 what the experiment's participants received and what happened to their other income",
     f"They received {usd(more)} a year more than a comparison group, and their other income ended up about {usd(VIVALT['less_income'])} a year "
     f"lower.")
band("T2 'those people took roughly a sixth of the money as time'", VIVALT["less_income"] / more, 0.15, 0.18)

# ---------------------------------------------------------------------------------------------------------------- Q
# Quotations and outside facts. Each was read on 2026-11-10 at the source named; the pages are not stored in the repository, so
# these lines hold only that the essay still prints what was read.
QUOTED = [
    ("Keynes, Economic Possibilities for our Grandchildren (1930), read at marxists.org",
     ['"the standard of life in progressive countries one hundred years hence will be between four and eight times as high as it is to-day."',
      '"Three-hour shifts or a fifteen-hour week"']),
    ("29 U.S.C. 207(a)(1), from the Fair Labor Standards Act of 1938, section 7, read at law.cornell.edu",
     ["The forty-hour week was written into American law by an act of 1938, and the law still says forty."]),
    ("nobelprize.org, economic sciences, 2024", ["Daron Acemoglu, who shared the Nobel prize in economics in 2024"]),
    ("Acemoglu and Restrepo (2022), abstract, from Crossref (10.3982/ecta19815)",
     ["between 50 and 70 percent of the change in America's wage structure",
      '"relative wage declines of worker groups specialized in routine tasks in industries experiencing rapid automation."']),
    ("Vivalt and others, NBER Working Paper 32719, abstract as revised August 2026, read at nber.org",
     ["gave 1,000 low-income people $1,000 a month for three years, with no conditions", '"a moderate labor supply effect."']),
    ("Paine, Agrarian Justice (1797), read at en.wikisource.org", ['"Man did not make the earth,"', '"It is not charity but a right,"']),
    ("Alaska Department of Revenue, Summary of Dividend Applications and Payments, pfd.alaska.gov; Alaska Permanent Fund Corporation, apfc.org",
     ["Since 1982 the state of Alaska has paid every resident a yearly dividend out of a fund built from its oil revenues.",
      "Alaska's dividend paid $1,312 a person in 2023 and $1,702 in 2024, to more than 600,000 people each year, and the fund behind it is "
      "worth $88 billion."]),
    ("Norges Bank Investment Management, About the fund, nbim.no", ['"almost 1.5 percent of all shares in the world\'s listed companies."']),
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
    buy = 40.0 / pay
    gap = np.log(since) - np.log(pay)                                  # how far ordinary pay fell behind output per hour, in logs
    spreading, ownership = np.log(spread[2024] / spread[1973]) / gap, -np.log(ls[2024] / ls[1973]) / gap
    check("N1 'to buy what forty hours of ordinary pay bought in 1973 now takes thirty-four hours'", d0(buy) == "34", f"{buy:.1f} hours")
    check("N2 'eighteen of the hours never reached ordinary paychecks'; 'the eighteen in between'", d0(buy - make) == "18", f"{buy - make:.1f} hours")
    check("N3 'the other six'; 'six hours off the week at the same standard of living'", d0(40.0 - buy) == "6", f"{40.0 - buy:.1f} hours")
    says("N4 from 1950 to 1973, with the panel given",
         f"Between 1950 and 1973 the first rose by {p0(oph[1973] / oph[1950] - 1)} percent and the second by {p0(w[1973] / w[1950] - 1)} percent.")
    says("N5 since 1973, with the panel given",
         f"Since 1973 the output of an hour has risen two and a half times, and an hour of ordinary pay buys {p0(pay - 1)} percent more.")
    band("N6 'about a fifth of the gap did' go to the owners of machines", float(ownership), 0.17, 0.23)
    band("N7 'about two-fifths of it is pay spreading out among workers'", float(spreading), 0.35, 0.42)
    check("N8 'the largest piece' named is the spreading-out, which is larger than the part that went to owners", spreading > ownership)
    band("N9 'ordinary pay did rise, by a fifth'; 'an hour of ordinary pay buys a fifth more'", float(pay - 1), 0.17, 0.22)
else:
    print("NOT HELD  the figures for ordinary pay (thirty-four, eighteen and six hours; 66 and 19 percent; a fifth and two-fifths of the gap): give "
          "the backward model's panel as an argument to hold them")

n_ok = sum(RESULTS)
print(f"\n{n_ok}/{len(RESULTS)} checks green")
sys.exit(0 if n_ok == len(RESULTS) else 1)
