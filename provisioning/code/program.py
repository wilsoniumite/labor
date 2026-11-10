# program.py — the sizes behind the draft's Section 9, a program for the United States.
#
# Everything here is arithmetic on tables the other scripts make and their checks hold: who holds the claims
# (exposure.py), site rent and the poverty-line bundle (rent_base.py), the model economy (paper_path.py), what the
# United States taxes and pays out (data/nipa_fiscal.csv, written by nipa_fiscal.py from BEA's Tables 3.1, 3.5 and
# 3.12), and population (../pinning/cache/B230RC0A052NBEA.csv, thousands).
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
import nipa_fiscal as nf  # noqa: E402
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
    corporate = float(nf.stored().loc[y, "corporate_taxes"])            # received by federal, state and local governments
    row = rb.table().loc[y]
    site = [row[f"rent_pp_{s}"] * people / 1e9 for s in ("30", "50")]
    grown = 1.0 - (1.0 + growth) ** (-years)
    return dict(corporate=corporate, corporate_share=corporate / k, corporate_a_person=corporate * 1e9 / people,
                site_share=[x / k for x in site], grown=grown, growth_share=[grown * x / k for x in site],
                together=[corporate / k + grown * x / k for x in site])


def receipts(y):
    """What the United States raises, by kind, as shares of all taxes and contributions for social insurance; and the
    total, $bn. Sales and property taxes are parts of the taxes on production and imports, shown apart."""
    r = nf.stored().loc[y]
    total = r.tax_receipts + r.contributions
    other = r.production_taxes - r.sales_taxes - r.property_taxes
    return dict(total=total, personal=r.personal_taxes / total, contributions=r.contributions / total,
                sales=r.sales_taxes / total, property=r.property_taxes / total, other_production=other / total,
                corporate=r.corporate_taxes / total, abroad=r.taxes_from_abroad / total, property_bn=r.property_taxes)


def benefits(y):
    """What the United States pays to persons in social benefits, $bn, and the largest programmes as shares of it."""
    r = nf.stored().loc[y]
    named = ("social_security", "medicare", "medicaid", "veterans", "refundable_credits", "snap", "unemployment")
    out = {k: r[k] / r.benefits for k in named}
    return dict(total=r.benefits, other=1.0 - sum(out.values()), social_security_bn=r.social_security, **out)


def common_income(t, stake=THETA):
    """Along the model's path, who is paid for what under the program, as shares of income: work; saving (the return to
    capital less the public's stake); and what is held in common, which is the public's stake in the return to capital
    and the rent of land above what it paid at the start (what a tax on the growth of rent collects)."""
    start, now = pp.point(0.0), pp.point(t)
    grown = max(0.0, 1.0 - start["real_rent"] / now["real_rent"])
    public_stake, public_rent = stake * now["interest"], grown * now["rent"]
    return dict(work=now["labour"], saving=(1.0 - stake) * now["interest"], owners_rent=(1.0 - grown) * now["rent"],
                stake=public_stake, rent=public_rent, common=public_stake + public_rent)


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
    rc, bn = receipts(y), benefits(y)
    print("taxes and contributions $%.0fbn: personal %.3f, contributions %.3f, sales %.3f, property %.3f ($%.0fbn), other on production %.3f, "
          "corporate %.3f" % (rc["total"], rc["personal"], rc["contributions"], rc["sales"], rc["property"], rc["property_bn"],
                              rc["other_production"], rc["corporate"]))
    print("social benefits to persons $%.0fbn: social security %.3f, medicare %.3f, medicaid %.3f, other %.3f"
          % (bn["total"], bn["social_security"], bn["medicare"], bn["medicaid"], bn["other"]))
    for t in (0.0, 0.5, 1.0, 2.0):
        c = common_income(t)
        print("the model economy at t = %.1f under the program: work %.3f, saving %.3f, held in common %.3f (stake %.3f, rent %.3f), "
              "rent left to owners %.3f" % (t, c["work"], c["saving"], c["common"], c["stake"], c["rent"], c["owners_rent"]))
    for t in (0.0, 1.0):
        v = path_dividend(t)
        print("the model economy at t = %.0f: a common fifth pays %.3f of the wage bill, %.3f of income" % (t, v["of_wages"], v["of_income"]))
    print("the claims cost %.2f times as many years of wages at t = 1 as at the start" % (pp.claims(1.0)["both"] / pp.claims(0.0)["both"]))
