# check_draft.py — the numbers paper/draft.md prints are the ones the scripts produce.
#
# Each `says` line is a sentence, clause or table row of the draft with its numbers filled in from the stored tables and
# the scripts, formatted as the draft prints them. It passes when the filled text is in the draft, so it fails if the
# data move and it fails if a number in the draft is changed. Numbers the draft gives in words (a tenth, two-thirds, a
# seventh) are held by `band` lines, each inside a stated range.
#   A  what consumption is made of and what pays for it (the abstract, Sections 1 and 3)
#   B  who holds the claims (Sections 2, 4, 5 and 6)
#   C  land and the cost of a floor (Sections 7 and 8)
#   D  the companion paper's economy (Sections 6 and 8)
#   E  what the companion paper and its September version print
#   N  not held on this branch: listed, and held when their inputs are given
# The wage accounting of Section 5 needs the backward model's panel, which is on another branch; give its path to hold
# those lines too:   python3 checks/check_draft.py PATH/TO/us-record/data/panel.csv
# Run from provisioning/:  python3 checks/check_draft.py      Exit 0 only if every check passes.
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
import rent_base as rb  # noqa: E402
import wage_shortfall as ws  # noqa: E402

RESULTS = []
TEXT = re.sub(r"\s+", " ", open(os.path.join(ROOT, "paper", "draft.md")).read().replace("\\ ", " "))


def check(name, ok, detail=""):
    RESULTS.append(bool(ok))
    print(("PASS " if ok else "FAIL ") + name + (f" — {detail}" if detail else ""))


def says(name, text):
    """The draft carries this text, whose numbers were filled in from the data."""
    text = re.sub(r"\s+", " ", text)
    check(name, text in TEXT, "" if text in TEXT else "not in the draft: " + text)


def band(name, value, low, high):
    """A number the draft gives in words lies in the range the words allow."""
    check(name, low <= value <= high, f"{value:.4f} in [{low}, {high}]")


d0, d1, d2, d3 = (lambda x: f"{x:.0f}"), (lambda x: f"{x:.1f}"), (lambda x: f"{x:.2f}"), (lambda x: f"{x:.3f}")
p0, p1 = (lambda x: f"{100 * x:.0f}"), (lambda x: f"{100 * x:.1f}")
sign = lambda x, f=d3: ("+" if x >= 0 else "−") + f(abs(x))   # noqa: E731

# ---------------------------------------------------------------------------------------------------------------- A
made, fin, pub = obt.made(), obt.financing(), obt.published()
r = made.loc[2023]
lab = made.labour_factor_psi38
years = [y for y in fin.index if y in made.index]
diff = (lab - fin.fin_labour).loc[years]
worn = r.worn_housing + r.worn_public + r.worn_business

says("A1 abstract: labour makes and pays for the same share in 2023",
     f"labour makes {p0(r.labour_factor_psi38)} percent of what consumption buys in 2023 and pays for {p0(fin.fin_labour[2023])} percent of it")
says("A2 introduction: the same",
     f"labour makes {p0(r.labour_factor_psi38)} percent of what consumption buys and pays for {p0(fin.fin_labour[2023])} percent of it")
band("A3 'differ by one point on average': the mean absolute difference, 2004-2023", float(diff.abs().mean()), 0.005, 0.015)
check("A4 the two accounts are compared over twenty years, 2004 to 2023", years[0] == 2004 and years[-1] == 2023 and len(years) == 20)
says("A5 the Bureau's reading", f"of each dollar of consumption in 2023, {p0(pub.human_effort_share[2023])} cents is the work of people in the United States")
says("A6 the dollar as counted",
     f"Of the consumer's dollar, {p1(r.gross_comp)} cents is employees' pay. Wear on machines and buildings takes {p1(worn)} cents. The "
     f"surplus left to owners after that wear takes {p1(r.gross_nos)} cents. Taxes on production take {p1(r.gross_tax)} cents and "
     f"imports {p1(r.gross_imports)} cents.")
gross_gap = (made.labour_gross_psi38 - pub.human_effort_share).dropna()
band("A7 'within two and a half points of the Bureau's in every year': the largest difference", float(gross_gap.abs().max()), 0.0, 0.025)
check("A8 the tables run from 1997 to 2023", int(made.index.min()) == 1997 and int(made.index.max()) == 2023)
says("A9 Table 1, pay", f"| Employees' pay | {d3(r.gross_comp)} | {d3(r.comp)} |")
says("A10 Table 1, wear", f"| Wear on machines and buildings | {d3(worn)} | — |")
says("A11 Table 1, net surplus", f"| Net surplus | {d3(r.gross_nos)} | {d3(r.nos)} |")
says("A12 Table 1, taxes", f"| Taxes on production | {d3(r.gross_tax)} | {d3(r.tax)} |")
says("A13 Table 1, imports", f"| Imports | {d3(r.gross_imports)} | {d3(r.imports)} |")
check("A14 Table 1's columns each add to one (1e-6)", abs(r.gross_comp + worn + r.gross_nos + r.gross_tax + r.gross_imports - 1) < 1e-6
      and abs(r.comp + r.nos + r.tax + r.imports - 1) < 1e-6)
says("A15 what a dollar of wear pays employees", f"each dollar of wear has paid {p0((r.comp - r.gross_comp) / worn)} cents to employees")
says("A16 the dollar with wear traced back",
     f"{p1(r.comp)} cents of employees' pay and {p1(r.nos)} cents of net surplus. Adding the working share of self-employment income to "
     f"pay, labour receives {p1(r.labour_dollar_psi38)} cents and capital and land {p1(r.comp + r.nos - r.labour_dollar_psi38)}. Labour's "
     f"share of the two is {d3(r.labour_factor_psi38)}. The share is {d3(r.labour_factor_psi00)} if none of the income of the self-employed "
     f"is counted as labour and {d3(r.labour_factor_psi67)} if two-thirds is. It is {d3(obt.made('tot').labour_factor_psi38[2023])} if "
     f"imports are treated as though they had been made at home, and {d3(obt.made('domp', 'economywide').labour_factor_psi38[2023])} if wear")
says("A17 the financing account in 2023",
     f"Its answer for 2023 is {d3(fin.fin_labour[2023])}, inside bounds of {d3(fin.fin_lower[2023])} and {d3(fin.fin_upper[2023])}")
says("A18 the difference between the two accounts",
     f"From 2004 to 2023 the difference between them averages {d3(abs(diff.mean()))}. It is never larger than {d3(diff.abs().max())} in "
     f"either direction, and its average size is {d3(diff.abs().mean())}.")
band("A19 'twelve points below its centre': the lower bound's average distance", float((fin.fin_labour - fin.fin_lower).mean()), 0.115, 0.125)
band("A20 'fourteen above': the upper bound's average distance", float((fin.fin_upper - fin.fin_labour).mean()), 0.135, 0.145)
says("A21 where the nineteen points go",
     f"Starting from the Bureau's {d3(pub.human_effort_share[2023])}: our count of labour before any adjustment is "
     f"{d3(pub.human_effort_share[2023] - r.labour_gross_psi38)} lower. Tracing wear back adds {d3(r.labour_dollar_psi38 - r.labour_gross_psi38)}. "
     f"Leaving taxes and imports aside adds {d3(r.labour_factor_psi38 - r.labour_dollar_psi38)}. The result is {d3(r.labour_factor_psi38)}.")
band("A22 'nineteen points' between the financing account and the Bureau's reading in 2023",
     float(fin.fin_labour[2023] - pub.human_effort_share[2023]), 0.18, 0.195)
current = fin.fin_labour / (1 - fin.fin_beyond_income)
says("A23 spending beyond income",
     f"{p1(fin.fin_beyond_income[2023])} percent of it in 2023, on the financing account's count. If that part is set aside, labour pays for "
     f"{p1(current[2023])} percent of what is bought out of current income. That is {p0(current[2023] - lab[2023])} points more than labour's "
     f"share of what is made, and {p0((current - lab).loc[years].mean())} points more on average over the twenty years.")
says("A24 the trend", f"was {d3(lab[1997])} in 1997, reached {d3(lab.max())} in {int(lab.idxmax())}, and was {d3(lab[2023])} in 2023")
band("A25 'five and a half points' since the peak", float(lab.max() - lab[2023]), 0.05, 0.06)
says("A26 the average basket in Section 4.1", f"the average basket, of which labour makes {d3(r.labour_factor_psi38)}")
says("A27 shelter and the rest",
     f"Shelter is {p1(r.shelter_share)} percent of consumer spending. Labour makes only {p0(r.shelter_labour_factor)} percent of it, because "
     f"most of the cost of shelter is the return on the building and the site. Labour makes {p0(r.rest_labour_factor_psi38)} percent of everything else.")
says("A28 net surplus in the consumer's dollar, Section 8.1", f"Net surplus is {p1(r.nos)} cents of the consumer's dollar")
band("A29 'five to eight cents': site rent at 30% of shelter's part of the dollar", float(0.30 * r.shelter_share), 0.045, 0.055)
band("A30 'five to eight cents': site rent at 50%", float(0.50 * r.shelter_share), 0.075, 0.085)

# ---------------------------------------------------------------------------------------------------------------- B
tabs = ex.inputs()
dec, grp = ex.tables(tabs)
g = grp.set_index(["group", "year"])
q = grp[grp.year == 2023].set_index("group")
d23 = dec[dec.year == 2023].set_index("decile")
tau = float(tabs["tax"].loc[2023, "lamR_med"])
everyone = g.loc["everyone", "exposure"]
held, s_now = ex.market_shares(tabs, 2023)
held04, s_then = ex.market_shares(tabs, 2004)
bh, nf, tt = held["bottom half"], held["next four tenths"], held["top tenth"]
share = ex.income_share

for key, label in (("bottom half", "Poorer half"), ("next four tenths", "Next four tenths"), ("top tenth", "Richest tenth")):
    x = q.loc[key]
    says(f"B1 Table 2, {label.lower()}",
         f"| {label} | {d3(x.labour_of_income)} | {sign(x.exposure)} | {p1(x.share_of_labour_income)}% | {p1(x.share_of_capital_and_land)}% | "
         f"{p1(x.share_of_transfers)}% | {p1(x.share_of_consumption)}% |")
says("B2 Table 2, everyone", f"| Everyone | {d3(q.loc['everyone', 'labour_of_income'])} | {sign(q.loc['everyone', 'exposure'])} | 100% |")
says("B3 Table 2's caption", f"labour's share of what consumption is made of ({d3(q.loc['everyone', 'made_by_labour'])})")
says("B4 the three groups in the text",
     f"labour accounts for {p1(q.loc['bottom half', 'labour_of_income'])} percent of income, directly or through the taxes behind their "
     f"benefits. For the next four tenths it is {p1(q.loc['next four tenths', 'labour_of_income'])} percent.")
band("B5 'ten ... points above': the poorer half's exposure", float(q.loc["bottom half", "exposure"]), 0.095, 0.105)
band("B6 'eleven and a half points above': the next four tenths'", float(q.loc["next four tenths", "exposure"]), 0.11, 0.12)
says("B7 the richest tenth in the text",
     f"For the richest tenth labour is {p1(q.loc['top tenth', 'labour_of_income'])} percent of income, fourteen points below. That tenth "
     f"receives {p1(q.loc['top tenth', 'share_of_labour_income'])} percent of all labour income, "
     f"{p1(q.loc['top tenth', 'share_of_capital_and_land'])} percent of the income of capital and land, and does "
     f"{p1(q.loc['top tenth', 'share_of_consumption'])} percent of the consuming.")
band("B8 'fourteen points below'", float(-q.loc["top tenth", "exposure"]), 0.135, 0.145)
says("B9 introduction: the richest tenth",
     f"by {p0(-q.loc['top tenth', 'exposure'])} percent of income, and that group holds {p0(q.loc['top tenth', 'share_of_capital_and_land'])} "
     f"percent of the claims on capital and land")
band("B10 'two-thirds of the claims on capital and land'", float(q.loc["top tenth", "share_of_capital_and_land"]), 0.64, 0.69)
nine = d23.loc[ex.DECILES[:9]]
check("B11 'nine households in ten are paid more by labour than their purchases are made by it': each of the first nine tenths, 2023",
      bool((nine.exposure > 0).all()) and float(d23.loc["90-100%", "exposure"]) < 0, f"lowest {nine.exposure.min():+.3f}")
a23 = ex.amounts(tabs, 2023)
m23, _ = ex.measures(a23, tau, float(r.labour_factor_psi38))
band("B12 'by about a tenth of their income': the least and the most exposed of the two groups below the richest tenth",
     float(min(q.loc["bottom half", "exposure"], q.loc["next four tenths", "exposure"])), 0.09, 0.12)
says("B13 the tax base", f"{p0(tau)} percent of tax revenue in 2023 was raised from labour income, so {p0(tau)} cents of each dollar")
says("B14 introduction: the tax base", f"because {p0(tau)} percent of the taxes that fund them are levied on labour")
band("B15 'a third of the taxes behind benefits fall on capital and land'", 1 - tau, 0.30, 0.36)
mid = d23.loc[ex.DECILES[1:9]]
says("B16 the second to the ninth tenths",
     f"labour is between {p0(mid.labour_of_market_income.min())} and {p0(mid.labour_of_market_income.max())} percent of market income, and "
     f"between {p0(mid.labour_of_income.min())} and {p0(mid.labour_of_income.max())} percent of all income")
says("B17 the poorest tenth",
     f"The poorest tenth is the least exposed of the nine, at {sign(d23.loc['0-10%', 'exposure'], d2)}. This is because "
     f"{p0(d23.loc['0-10%', 'transfers_of_income'])} percent of its income is benefits")
check("B18 the poorest tenth is the least exposed of the nine", d23.loc["0-10%", "exposure"] == nine.exposure.min())
says("B19 everyone together",
     f"the exposure is {sign(everyone[2023])} in 2023 and {sign(everyone.mean())} on average over the twenty years")
says("B20 the third account, Section 3.3",
     f"labour is {d3(q.loc['everyone', 'labour_of_income'])} of all households' income in 2023, and over 2004–2023 it differs from what "
     f"consumption is made of by {d3(everyone.mean())} on average")
band("B21 'two and a half points in any one year': the household account against what consumption is made of", float(everyone.abs().max()), 0.0, 0.0255)
band("B22 'two and a half points in any one year': what is made against what is financed", float(diff.abs().max()), 0.0, 0.0255)
band("B23 'about one point', Section 2.4: everyone's exposure on average", float(everyone.mean()), 0.005, 0.015)

signs, spans = [], {"bottom half": [], "next four tenths": [], "top tenth": []}
for psi in (0.0, 0.38, 0.67):
    for tau_col in ("lamR_min", "lamR_med", "lamR_max"):
        col = f"labour_factor_psi{int(round(100 * psi)):02d}"
        t2 = dict(tabs, made=tabs["made"].assign(labour_factor_psi38=tabs["made"][col]))
        _, gv = ex.tables(t2, psi=psi, tau_col=tau_col)
        x = gv.set_index(["group", "year"])["exposure"].unstack(0)
        signs.append(bool((x["bottom half"] > 0).all() and (x["next four tenths"] > 0).all() and (x["top tenth"] < 0).all()))
        for k in spans:
            spans[k].append(float(x.loc[2023, k]))
check("B24 'in all nine combinations, and in every year' the signs hold", all(signs) and len(signs) == 9)
says("B25 the ranges across the judgments",
     f"the exposure of the poorer half ranges from {sign(min(spans['bottom half']), d2)} to {sign(max(spans['bottom half']), d2)}, that of the "
     f"next four tenths from {sign(min(spans['next four tenths']), d2)} to {sign(max(spans['next four tenths']), d2)}, and that of the richest "
     f"tenth from {sign(min(spans['top tenth']), d2)} to {sign(max(spans['top tenth']), d2)}")
m_recv, _ = ex.measures(a23.assign(accrued=0.0), tau, float(r.labour_factor_psi38))
says("B26 without the corporate income that is not paid out",
     f"Without it, labour is {p1(m_recv.loc['90-100%', 'labour_of_income'])} percent of the richest tenth's income; with it, "
     f"{p1(d23.loc['90-100%', 'labour_of_income'])} percent.")
avg = ex.basket(tabs, 2023, float(r.shelter_share))
says("B27 a household on wages alone",
     f"its exposure to labour is {d2(1 - avg)}. If it spends 30 percent of its budget on rent, its exposure is {d2(1 - ex.basket(tabs, 2023, 0.30))}, "
     f"and at 40 percent it is {d2(1 - ex.basket(tabs, 2023, 0.40))}")
says("B28 Section 2.2's example",
     f"the poorer half of households held {p1(bh["labour"])} percent of labour income and {p1(bh["capital"])} percent of the income of capital and land. Each "
     f"point that moves from labour to the other claims therefore costs that half {d3(bh["labour"] - bh["capital"])} points of all market income")
check("B29 the holdings behind the identity are Table 2's (1e-12)",
      max(abs(h["labour"] - q.loc[k, "share_of_labour_income"]) + abs(h["capital"] - q.loc[k, "share_of_capital_and_land"]) for k, h in held.items()) < 1e-12)

ss, s0, s1 = ex.shift_share(tabs, 2004, 2023)
top, nxt, low = ss["top tenth"], ss["next four tenths"], ss["bottom half"]
says("B30 the shift so far",
     f"labour's share of households' market income fell from {d3(s0)} to {d3(s1)}. Over the same years the richest tenth's share of market "
     f"income rose by {d1(100 * (top['after'] - top['before']))} points. Of that, {d1(100 * top['between'])} points came from payments moving "
     f"between claims. The other {d1(100 * top['within'])} points came from the richest tenth holding more of each claim: its share of labour "
     f"income rose from {p1(held04['top tenth']['labour'])} to {p1(tt["labour"])} percent, and its share of the income of capital and land from "
     f"{p1(held04['top tenth']['capital'])} to {p1(tt["capital"])} percent. The next four tenths lost {d1(100 * (nxt['before'] - nxt['after']))} points")
band("B31 'about 1 from the movement between claims'", float(-100 * nxt["between"]), 0.8, 1.2)
band("B32 'about 3 from holding less of each'", float(-100 * nxt["within"]), 2.8, 3.4)
band("B33 'the poorer half's share was almost unchanged': its change in points", float(abs(100 * (low["after"] - low["before"]))), 0.0, 0.2)
band("B34 'about four and a half points', introduction", float(100 * (s0 - s1)), 4.3, 4.7)
says("B35 introduction: the shift so far",
     f"That moved {d1(100 * top['between'])} points of market income to the richest tenth. The same group gained twice as much, "
     f"{d1(100 * top['within'])} points")
band("B36 'twice as much'", float(top["within"] / top["between"]), 1.8, 2.3)
check("B37 the split between claims and holdings is exact (1e-12)",
      max(abs(v["after"] - v["before"] - v["between"] - v["within"]) for v in ss.values()) < 1e-12)
says("B38 a larger shift",
     f"the richest tenth's share of market income would rise from {p1(share(tt, s_now))} to {p1(share(tt, 0.17))} percent. The next four "
     f"tenths would fall from {p1(share(nf, s_now))} to {p1(share(nf, 0.17))} percent, and the poorer half from {p1(share(bh, s_now))} to "
     f"{p1(share(bh, 0.17))} percent. In the limit, with nothing paid to labour, each group's share is simply its share of capital and land: "
     f"{p1(tt["capital"])}, {p1(nf["capital"])} and {p1(bh["capital"])} percent.")
says("B39 introduction: a larger shift",
     f"rise from {p0(share(tt, s_now))} to {p0(share(tt, 0.17))} percent. The share of the next four tenths would fall from "
     f"{p0(share(nf, s_now))} to {p0(share(nf, 0.17))} percent, and the poorer half's from {p1(share(bh, s_now))} to {p0(share(bh, 0.17))} percent")
says("B40 the upper middle's holdings",
     f"hold {p1(nf["labour"])} percent of labour income, more than any other group, and {p1(nf["capital"])} percent of the other claims")
check("B41 the next four tenths hold more labour income than either other group", nf["labour"] > tt["labour"] and nf["labour"] > bh["labour"])
band("B42 'nearly half of all labour income'", float(nf["labour"]), 0.45, 0.50)
says("B43 the common holding that keeps each group's share",
     f"For the poorer half the answer is {d2(ex.holding_share(bh, s_now, 0.17))} if labour is paid 17 percent, and "
     f"{d2(ex.holding_share(bh, s_now, 0.0))} if labour is paid nothing. A common holding of a fifth would raise the poorer half's share to "
     f"{p0(share(bh, 0.17, 0.2))} percent in either case. For the next four tenths the answer is {d2(ex.holding_share(nf, s_now, 0.17))} and "
     f"{d2(ex.holding_share(nf, s_now, 0.0))}.")
check("B44 'in either case': a common fifth takes the poorer half to the same whole percent with labour paid 0.17 and nothing",
      p0(share(bh, 0.17, 0.2)) == p0(share(bh, 0.0, 0.2)))
says("B45 the upper middle with a fifth in common",
     f"their share would be {p0(share(nf, 0.17, 0.2))} percent at a labour share of 0.17, against {p0(share(nf, s_now))} percent today")
band("B46 'about a seventh', low end", float(ex.holding_share(bh, s_now, 0.17)), 0.125, 0.16)
band("B47 'about a seventh', high end", float(ex.holding_share(bh, s_now, 0.0)), 0.125, 0.16)
band("B48 'nothing short of six-sevenths'", float(ex.holding_share(nf, s_now, 0.17)), 0.85, 0.87)

# ---------------------------------------------------------------------------------------------------------------- C
t = rb.table()
a, b, c = t.loc[1975], t.loc[2024], t.loc[1955]
says("C1 site rent against income",
     f"site rent was between {p1(b.share_dpi_30)} and {p1(b.share_dpi_50)} percent of disposable income in 2024, or between "
     f"{b.rent_pp_30_last:,.0f} and {b.rent_pp_50_last:,.0f} dollars per person. In 1975 it was between {p1(a.share_dpi_30)} and "
     f"{p1(a.share_dpi_50)} percent")
says("C2 abstract and introduction: site rent", f"rent is {p0(b.share_dpi_30)} to {p0(b.share_dpi_50)} percent of disposable income")
covers = [float(b[f"cover_{k}_{s}"]) for k in ("family4", "single") for s in ("30", "50")]
says("C3 what the rent would cover", f"On our four series for 2024 the answer runs from {p0(min(covers))} to {p0(max(covers))} percent")
says("C4 the floor against GDP",
     f"In 2024 it is between {p0(b.floor_gdp_family4)} and {p0(b.floor_gdp_single)} percent, depending on whether the bundle is priced for one "
     f"member of a family of four or for a person living alone. In 1975 it was between {p0(a.floor_gdp_family4)} and {p0(a.floor_gdp_single)} "
     f"percent, and in 1955 between {p0(c.floor_gdp_family4)} and {p0(c.floor_gdp_single)} percent")
pce, gdp = rb.annual("pinning/cache/PCECA.csv"), rb.annual("three-taxes/cache/GDPA.csv")
f23 = t.loc[2023]
says("C5 the floor against consumer spending",
     f"it costs {p0(f23.floor_gdp_family4 * gdp[2023] / pce[2023])} to {p0(f23.floor_gdp_single * gdp[2023] / pce[2023])} cents of the "
     f"consumer's dollar in 2023. Site rent is five to eight cents of that dollar, and net surplus is {p1(r.nos)}")
band("C6 'the growth rate of rent divided by the rate at which the future is discounted ... at 2 and 5 percent it is 40 percent'", 0.02 / 0.05, 0.3999, 0.4001)

# ---------------------------------------------------------------------------------------------------------------- D
m0, m1, m2 = pp.mix(0.0), pp.mix(1.0), pp.mix(2.0)
says("D1 labour's share along the path",
     f"labour's share of income is {p0(m0['labour'])} percent at the start, {p0(m1['labour'])} percent at a point it labels")
band("D2 'close to zero beyond': labour's share at t = 2", float(m2["labour"]), 0.0, 0.01)
says("D3 interest and rent along the path",
     f"interest is {p0(m0['interest'])} percent of income at the start, {p0(m1['interest'])} percent at $t = 1$ and {p0(m2['interest'])} "
     f"percent in the limit. Rent is {p0(m0['rent'])}, {p0(m1['rent'])} and {p0(m2['rent'])} percent")
c0, cth, c1 = pp.claims(0.0), pp.claims(0.77), pp.claims(1.0)
says("D4 what the claims cost",
     f"are worth {d1(c0['both'])} years of the economy's wage bill: {d1(c0['capital'])} years for capital and {d1(c0['land'])} for land")
says("D5 at the threshold and at t = 1", f"they are worth {d0(cth['both'])} years of wages. At $t = 1$ they are worth {d0(c1['both'])}.")
tax, later = pp.interest_tax(0.20), pp.interest_tax(0.20, t=1.0)
says("D6 Table 3, a tax on the return",
     f"| A 20 percent tax on the return to capital | {p1(tax['revenue'])}% of income | Wage earners: the wage bill falls by "
     f"{p1(-tax['wages'])}% of income and the real wage by {p0(1 - tax['real_wage'])}% | Capital is {p0(1 - tax['real_capital'])}% smaller and "
     f"real income {p1(1 - tax['real_income'])}% lower |")
fifth = 0.2 * m0["interest"]
says("D7 Table 3, a tax on cash flow", f"with investment written off | {p1(fifth)}% of income | Today's owners, once: a fifth of the existing stock | Unchanged |")
says("D8 Table 3, a purchase", f"| Buying a fifth of the capital stock | {p1(fifth)}% of income | Whoever saves to buy it")
band("D9 'one year of the economy's whole wage bill': a fifth of the claim on capital", 0.2 * c0["capital"], 0.95, 1.10)
says("D10 the tax in the text",
     f"In the long run the tax raises {p1(tax['revenue'])} percent of income and wages fall by {p1(-tax['wages'])} percent of income. If every "
     f"dollar of the revenue were handed to wage earners they would be {p1(tax['wage_earner'])} percent better off than before the tax, and "
     f"the economy would be {p1(1 - tax['real_income'])} percent poorer.")
band("D11 'almost dollar for dollar': the fall in wages over the revenue", float(-tax["wages"] / tax["revenue"]), 0.90, 1.00)
check("D12 'later on the path the same tax falls on rent in place of wages, but it still shrinks the capital stock': at t = 1",
      abs(later["wages"]) < 0.005 and later["rents"] < -0.03 and later["real_capital"] < 0.90,
      f"wages {later['wages']:+.3f}, rents {later['rents']:+.3f}, capital x{later['real_capital']:.2f}")
check("D13 what the tax takes adds up: wages, rents, owners and revenue sum to the change in real income (1e-9)",
      abs(tax["wages"] + tax["rents"] + tax["owners"] + tax["revenue"] - (tax["real_income"] - 1)) < 1e-9)

# ---------------------------------------------------------------------------------------------------------------- E
REPO = os.path.dirname(ROOT)
PRINTED = dict(median=0.33, low=0.18, high=0.59)   # the companion paper's Section 10.1, October 2026: a transcription, its source is not here
says("E1 the companion paper's coverage, as it prints it",
     f"reports a median of {p0(PRINTED['median'])} percent for 2025, with a range from {p0(PRINTED['low'])} to {p0(PRINTED['high'])}")
earlier = re.sub(r"\s+", " ", open(os.path.join(REPO, "pinning", "paper", "main.tex")).read())
quote = "substantially more labor-financed than production is labor-intensive"
check("E2 the sentence quoted from the September version is in ../pinning/paper/main.tex and in the draft",
      quote in earlier and quote in TEXT and "a gap of about nineteen percentage points" in earlier)

# ---------------------------------------------------------------------------------------------------------------- N
if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
    panel = pd.read_csv(sys.argv[1]).set_index("year")
    w = panel["wage_exshelter"]
    sf = ws.shortfall(panel, 1973, 2024)
    s_ = sf["shortfall"]
    says("N1 the wage, with the panel given",
         f"grew by {d1(100 * ws.rate(w, 1950, 1973))} percent a year. From 1973 to 1995 it fell by {d1(-100 * ws.rate(w, 1973, 1995))} percent a "
         f"year, and since then it has grown by {d1(100 * ws.rate(w, 1995, 2024))} percent a year. By 2024 it stood at 1/{d1(np.exp(s_))} of what "
         f"the earlier pace would have made it.")
    says("N2 the shortfall divided, with the panel given",
         f"Slower growth of output per hour accounts for {p0(sf['output'] / s_)} percent of it. Average pay pulling away from the pay of "
         f"production workers accounts for {p0(sf['dispersion'] / s_)} percent. The fall in labour's share of income accounts for "
         f"{p0(sf['share'] / s_)} percent, and {p0(sf['left_over'] / s_)} percent is left over.")
    says("N3 shelter, with the panel given", f"the rising relative price of shelter is {p0(sf['shelter'] / sf['all_items'])} percent of it")
    band("N4 'a little over a fifth': the labour-share and shelter parts of the shortfall on the all-items wage",
         float((sf["share"] + sf["shelter"]) / sf["all_items"]), 0.20, 0.24)
else:
    print("NOT HELD  Section 5's wage accounting (2.2, 0.6 and 1.1 percent a year; 1/2.6; 42, 30, 16, 13 and 8 percent): give the "
          "backward model's panel as an argument to hold it")
print("NOT HELD  Section 7.4's land-tax figures (249 dollars a month, 85 percent, 16.8 million owners, 45 percent, 1 percent): they are "
      "the consumption branch's, consumption/lvt/NOTES_us.md")

n_ok = sum(RESULTS)
print(f"\n{n_ok}/{len(RESULTS)} checks green")
sys.exit(0 if n_ok == len(RESULTS) else 1)
