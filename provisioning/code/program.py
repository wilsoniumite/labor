# program.py — the sizes behind the draft's Section 9, a program for the United States.
#
# Everything here is arithmetic on tables the other scripts make and their checks hold: who holds the claims
# (exposure.py), site rent and the poverty-line bundle (rent_base.py), the model economy (paper_path.py), and four
# national-accounts series already in the repository:
#   ../pinning/cache/A061RC1A027NBEA.csv   contributions for government social insurance, $bn
#   ../pinning/cache/W054RC1A027NBEA.csv   government current tax receipts, $bn
#   ../pinning/cache/B230RC0A052NBEA.csv   population, thousands
#   data/nipa_corporate.csv                taxes on corporate income, $bn
#
# A group is matched when its share of the claims on capital and land equals its share of labour income: then its share
# of market income does not move when payments move between the claims (the identity of the draft's Section 2.2).
#
# Run from provisioning/:  python3 code/program.py      Gated by checks/check_program.py.

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import exposure as ex  # noqa: E402
import paper_path as pp  # noqa: E402
import rent_base as rb  # noqa: E402

THETA = 0.2          # the common holding the draft uses throughout: a fifth of the claims on capital and land
POPULATION = "pinning/cache/B230RC0A052NBEA.csv"


def incomes(tabs, y):
    """Labour income and the income of capital and land (received and accrued), by decile, $bn."""
    a = ex.amounts(tabs, y)
    return a.comp + ex.PSI * a.prop, (1.0 - ex.PSI) * a.prop + a.rent + a.interest + a.dividends + a.accrued


def gaps(tabs, y, theta=0.0, labour_share=None):
    """How far each group is from a matched position when a share theta of the claims on capital and land is held in
    common, equally a head: the share of the claims it then holds, its income from capital and land per dollar of its
    labour income, how far that is short of a matched group's, and the share of all the claims it still lacks. `needs`
    is the common share that would match the group by itself. With labour_share given, the holdings are the year's and
    labour is paid that share of market income. Returns the groups and the matched ratio."""
    held, s = ex.market_shares(tabs, y)
    s = s if labour_share is None else labour_share
    matched = (1.0 - s) / s
    out = {}
    for g, h in held.items():
        claims = (1.0 - theta) * h["capital"] + theta * h["people"]
        per_dollar = claims * (1.0 - s) / (h["labour"] * s)
        out[g] = dict(claims=claims, per_dollar=per_dollar, short=matched - per_dollar, gap=h["labour"] - claims,
                      needs=(h["labour"] - h["capital"]) / (h["people"] - h["capital"]))
    return out, matched


def years_to_match(short, rate, ret):
    """Years of saving `rate` of wages, the returns reinvested at `ret`, until the claims held pay `short` of wages a
    year. Claims are valued at their income over `ret`, so the holding needed is short / ret years of wages."""
    return math.log(1.0 + short / rate) / math.log(1.0 + ret)


def dividend(tabs, y, theta=THETA):
    """What a common holding of theta pays: $bn, dollars a person a year, and its share of a poverty-line bundle priced
    for one member of a family of four and for a person living alone."""
    _, capital = incomes(tabs, y)
    people = rb.annual(POPULATION)[y] * 1e3
    cpi = rb.annual("pinning/cache/CPIAUCSL.csv", full=12)
    total = theta * capital.sum()
    each = total * 1e9 / people
    return dict(total=total, a_person=each, **{k: each / (v * cpi[y] / cpi[1963]) for k, v in rb.BUNDLES_1963.items()})


def public_claims(tabs, y, growth=0.02, years=25):
    """Two claims the public could hold without buying anything, as shares of the income of capital and land: the
    corporate income tax (the scale of a stake taken through a cash-flow tax at the same rate) and the growth of
    residential site rent (what a tax on growth alone collects after `years` of growth at `growth` a year), with land
    at 30 and at 50 percent of housing services."""
    _, capital = incomes(tabs, y)
    k = capital.sum()
    people = rb.annual(POPULATION)[y] * 1e3
    corporate = float(tabs["corp"].loc[y, "taxes_on_corporate_income"])
    row = rb.table().loc[y]
    site = [row[f"rent_pp_{s}"] * people / 1e9 for s in ("30", "50")]
    grown = 1.0 - (1.0 + growth) ** (-years)
    return dict(corporate=corporate, corporate_share=corporate / k, corporate_a_person=corporate * 1e9 / people,
                site_share=[x / k for x in site], grown=grown, growth_share=[grown * x / k for x in site],
                together=[corporate / k + grown * x / k for x in site])


def receipts(y):
    """Contributions for social insurance as a share of all taxes and contributions."""
    c = rb.annual("pinning/cache/A061RC1A027NBEA.csv")[y]
    t = rb.annual("pinning/cache/W054RC1A027NBEA.csv")[y]
    return c / (c + t)


def path_dividend(t, theta=THETA):
    """The income of a common holding of theta in the model economy, over the wage bill and over all income."""
    m = pp.mix(t)
    return dict(of_wages=theta * (1.0 - m["labour"]) / m["labour"], of_income=theta * (1.0 - m["labour"]))


if __name__ == "__main__":
    tabs, y = ex.inputs(), 2023
    labour, capital = incomes(tabs, y)
    print(f"{y}: labour income ${labour.sum():,.0f}bn, the income of capital and land ${capital.sum():,.0f}bn")
    for theta in (0.0, THETA):
        g, matched = gaps(tabs, y, theta)
        print(f"\na common holding of {theta:.2f}; a matched group has {matched:.3f} from capital and land per dollar of labour income")
        for name, v in g.items():
            print("  %-17s holds %.3f of the claims  %.3f a dollar  short %.3f  lacks %+.3f of the claims  (alone it would need %.2f in common)"
                  % (name, v["claims"], v["per_dollar"], v["short"], v["gap"], v["needs"]))
    short = gaps(tabs, y, THETA)[0]["next four tenths"]["short"]
    print("\nthe next four tenths, after a common fifth: short %.3f of wages; a holding of %.1f years of wages at 5%%, %.1f at 10%%"
          % (short, short / 0.05, short / 0.10))
    for rate in (0.05, 0.10):
        print("  saving %.0f%% of wages: %.1f years at a return of 5%%, %.1f at 10%%"
              % (100 * rate, years_to_match(short, rate, 0.05), years_to_match(short, rate, 0.10)))
    later = gaps(tabs, y, THETA, pp.mix(1.0)["labour"])[0]["next four tenths"]["short"]
    print("  with labour paid what it is paid at t = 1 in the model economy: short %.3f of wages; saving 5%% takes %.1f years at 5%%, %.1f at 10%%"
          % (later, years_to_match(later, 0.05, 0.05), years_to_match(later, 0.05, 0.10)))
    d = dividend(tabs, y)
    print("\na common fifth pays $%.0fbn: $%.0f a person a year ($%.0f a month), %.2f of a poverty-line bundle for one of a family of four, %.2f alone"
          % (d["total"], d["a_person"], d["a_person"] / 12, d["family4"], d["single"]))
    p = public_claims(tabs, y)
    print("the corporate income tax: $%.0fbn, %.3f of the income of capital and land, $%.0f a person" % (p["corporate"], p["corporate_share"], p["corporate_a_person"]))
    print("residential site rent: %.3f to %.3f of the income of capital and land; a tax on its growth collects %.3f of it after 25 years at 2%%: %.3f to %.3f"
          % (*p["site_share"], p["grown"], *p["growth_share"]))
    print("together: %.3f to %.3f of the income of capital and land" % tuple(p["together"]))
    print("contributions for social insurance: %.3f of taxes and contributions" % receipts(y))
    for t in (0.0, 1.0):
        v = path_dividend(t)
        print("the model economy at t = %.0f: a common fifth pays %.3f of the wage bill, %.3f of income" % (t, v["of_wages"], v["of_income"]))
    print("the claims cost %.2f times as many years of wages at t = 1 as at the start" % (pp.claims(1.0)["both"] / pp.claims(0.0)["both"]))
