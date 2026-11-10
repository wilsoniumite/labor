# exposure.py — who holds which claim: each income decile's income against what consumption is made of
# (assembly 2 of SKETCH.md, first cut).
#
# The exposure identity: a household's real income moves with the wage, relative to the other factor payments, by
#     exposure = (labour's share of its income) - (labour's share of what it buys).
# The second term is code/one_basis.py's (labour's share of the net domestic factor cost of consumption, replacement
# traced back). This script builds the first from BEA's distribution of personal income by decile of equivalized
# disposable income (the file the financing account is built on), 2004-2023:
#     labour            compensation of employees, and the share psi of proprietors' income (0.38, the financing account's)
#     capital and land  the rest of proprietors' income, rental income (mostly owner-occupiers' own housing), interest,
#                       dividends
#     accrued           corporate income households do not receive: undistributed profits and taxes on corporate income
#                       (NIPA), given to deciles in proportion to dividends. Without it households' incomes leave out
#                       about a quarter of capital's income and every decile looks more dependent on labour than it is.
#     transfers         government social benefits, counted as a claim on the taxes that fund them: tau of each dollar is
#                       labour's (the paper's share of tax revenue raised from labour-income bases, 0.68 in 2023)
# Taxes are taken to fall on each decile's sources in proportion. Everything is before tax.
#
# WHAT IT DOES NOT DO YET. Every decile is given the average basket; renters and owners are not told apart (the survey
# data for that are on the consumption branch). The stylised rows at the end say how much that matters: shelter is made
# of very little labour, so a household that rents and spends a third of its budget on shelter buys a basket with much
# less labour in it than the average one.
#
# Reads only files in the repository. Run from provisioning/:  python3 code/exposure.py
# Writes data/exposure_deciles.csv and data/exposure_groups.csv. Gated by checks/check_exposure.py.

import os

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REPO = os.path.dirname(ROOT)
DF = os.path.join(REPO, "pinning", "effort", "archive_v28", "inputs", "df")
DECILES = [f"{i * 10}-{(i + 1) * 10}%" for i in range(10)]
RANKING = "Equivalized Disposable Personal Income"
CONCEPTS = {"Compensation of employees": "comp", "Proprietors' income with inventory valuation": "prop",
            "Rental income of households with capital consumption adjustment": "rent", "Household interest income": "interest",
            "Household dividend income": "dividends", "Government social benefits": "benefits",
            "Disposable personal income": "dpi"}
GROUPS = {"bottom half": DECILES[:5], "next four tenths": DECILES[5:9], "top tenth": DECILES[9:]}
YEARS = list(range(2004, 2024))
PSI = 0.38


def inputs():
    bea = pd.read_csv(os.path.join(DF, "BEA_distribution_summary-file.csv"), low_memory=False)
    bea.columns = ["year", "ranking", "concept", "line", "metric", "value"]
    pce = pd.read_csv(os.path.join(DF, "bea_sharp_intertemporal_bound_decile_2000_2023.csv"))
    made = pd.read_csv(os.path.join(ROOT, "data", "one_basis.csv"))
    made = made[(made.basis == "domp") & (made.depreciation == "central")].set_index("year")
    corp = pd.read_csv(os.path.join(ROOT, "data", "nipa_corporate.csv")).set_index("year")
    tax = pd.read_csv(os.path.join(REPO, "pinning", "data", "lambda_results.csv")).set_index("year")
    return dict(bea=bea, pce=pce, made=made, corp=corp, tax=tax)


def amounts(tabs, y):
    """Each decile's income by source and its consumption, $ billions."""
    b = tabs["bea"][tabs["bea"].year == y]
    total = {CONCEPTS[c]: float(str(v).replace(",", "")) for c, v in b[b.metric == "Total ($Billions)"][["concept", "value"]].values
             if c in CONCEPTS}
    sh = b[(b.ranking == RANKING) & b.metric.isin(DECILES)].pivot_table(index="metric", columns="concept", values="value",
                                                                        aggfunc="first").astype(float).loc[DECILES]
    sh = sh.rename(columns=CONCEPTS)[list(CONCEPTS.values())]
    a = sh / sh.sum() * pd.Series(total)                               # the published shares are rounded: made to add to one
    c = tabs["corp"].loc[y]
    a["accrued"] = sh["dividends"] / sh["dividends"].sum() * (c["undistributed_profits"] + c["taxes_on_corporate_income"])
    a["pce"] = tabs["pce"][tabs["pce"].Year == y].set_index("decile").loc[DECILES, "pce_amount_b"].values
    return a


def measures(a, tau, made, psi=PSI):
    labour = a.comp + psi * a.prop
    capital = (1.0 - psi) * a.prop + a.rent + a.interest + a.dividends
    everything = labour + capital + a.accrued + a.benefits
    out = pd.DataFrame({"labour_of_market_income": labour / (labour + capital),
                        "labour_with_transfers": (labour + tau * a.benefits) / (labour + capital + a.benefits),
                        "labour_of_income": (labour + tau * a.benefits) / everything,
                        "transfers_of_income": a.benefits / everything,
                        "share_of_labour_income": labour / labour.sum(),
                        "share_of_capital_and_land": (capital + a.accrued) / (capital + a.accrued).sum(),
                        "share_of_transfers": a.benefits / a.benefits.sum(),
                        "share_of_consumption": a.pce / a.pce.sum()})
    out["made_by_labour"] = made
    out["exposure"] = out["labour_of_income"] - made
    out["exposure_market_income"] = labour / (labour + capital + a.accrued) - made
    return out, dict(labour=labour, capital=capital + a.accrued, benefits=a.benefits, pce=a.pce, everything=everything)


def tables(tabs, psi=PSI, tau_col="lamR_med"):
    dec, grp = [], []
    for y in YEARS:
        a = amounts(tabs, y)
        tau, made = float(tabs["tax"].loc[y, tau_col]), float(tabs["made"].loc[y, "labour_factor_psi38"])
        m, parts = measures(a, tau, made, psi)
        m.insert(0, "year", y)
        dec.append(m.reset_index().rename(columns={"metric": "decile"}))
        rows = dict(GROUPS, everyone=DECILES)
        for name, members in rows.items():
            s = {k: v.loc[members].sum() for k, v in parts.items()}
            grp.append(dict(year=y, group=name, labour_of_income=(s["labour"] + tau * s["benefits"]) / s["everything"],
                            made_by_labour=made, exposure=(s["labour"] + tau * s["benefits"]) / s["everything"] - made,
                            share_of_labour_income=s["labour"] / parts["labour"].sum(),
                            share_of_capital_and_land=s["capital"] / parts["capital"].sum(),
                            share_of_transfers=s["benefits"] / parts["benefits"].sum(),
                            share_of_consumption=s["pce"] / parts["pce"].sum(), tau=tau))
    return pd.concat(dec, ignore_index=True), pd.DataFrame(grp)


def market_shares(tabs, y, psi=PSI):
    """Who holds the claims, apart from transfers: each group's share of labour income and of the income of capital and
    land (received and accrued), and labour's share of the two together."""
    a = amounts(tabs, y)
    labour = a.comp + psi * a.prop
    capital = (1.0 - psi) * a.prop + a.rent + a.interest + a.dividends + a.accrued
    held = {g: dict(labour=float(labour.loc[m].sum() / labour.sum()), capital=float(capital.loc[m].sum() / capital.sum()),
                    people=len(m) / 10.0) for g, m in GROUPS.items()}
    return held, float(labour.sum() / (labour.sum() + capital.sum()))


def income_share(h, labour_share, theta=0.0):
    """A group's share of market income when labour is paid labour_share of it and a share theta of the claims on capital
    and land is held in common, equally a head. An identity: its share of each claim, weighted by what the claim is paid."""
    return h["labour"] * labour_share + ((1.0 - theta) * h["capital"] + theta * h["people"]) * (1.0 - labour_share)


def holding_share(h, labour_share_now, labour_share_then):
    """The common share theta at which a group's share of market income is the same at labour_share_then as it is today."""
    now = income_share(h, labour_share_now)
    return (now - h["labour"] * labour_share_then - h["capital"] * (1.0 - labour_share_then)) / (
        (h["people"] - h["capital"]) * (1.0 - labour_share_then))


def shift_share(tabs, y0, y1):
    """The change in each group's share of market income between two years, split exactly into payments moving between
    the claims (at the mean of its holdings) and its holdings of each claim changing (at the mean of the payments)."""
    h0, s0 = market_shares(tabs, y0)
    h1, s1 = market_shares(tabs, y1)
    out = {}
    for g in GROUPS:
        between = 0.5 * ((h0[g]["labour"] - h0[g]["capital"]) + (h1[g]["labour"] - h1[g]["capital"])) * (s1 - s0)
        within = (0.5 * (s0 + s1) * (h1[g]["labour"] - h0[g]["labour"])
                  + (1.0 - 0.5 * (s0 + s1)) * (h1[g]["capital"] - h0[g]["capital"]))
        out[g] = dict(before=income_share(h0[g], s0), after=income_share(h1[g], s1), between=between, within=within)
    return out, s0, s1


def basket(tabs, y, shelter_share, psi_tag="38"):
    """Labour's share of the net factor cost of a basket with the given share of spending on shelter."""
    r = tabs["made"].loc[y]
    prop_labour = r[f"labour_dollar_psi{psi_tag}"] - r["comp"]                       # proprietors' labour in the average dollar
    rest_labour = r["rest_comp"] + prop_labour / (1.0 - r["shelter_share"])
    labour = shelter_share * r["shelter_comp"] + (1.0 - shelter_share) * rest_labour
    cost = shelter_share * (r["shelter_comp"] + r["shelter_nos"]) + (1.0 - shelter_share) * (r["rest_comp"] + r["rest_nos"])
    return float(labour / cost)


if __name__ == "__main__":
    tabs = inputs()
    dec, grp = tables(tabs)
    dec.to_csv(os.path.join(ROOT, "data", "exposure_deciles.csv"), index=False)
    grp.to_csv(os.path.join(ROOT, "data", "exposure_groups.csv"), index=False)
    for y in (2004, 2023):
        d = dec[dec.year == y].set_index("decile")
        print(f"\n{y}: labour makes {d['made_by_labour'].iloc[0]:.3f} of what consumption buys. By decile of equivalized disposable income:")
        print("decile    labour's share of: market income, income with transfers and accrued | exposure | "
              "share held of: labour income, capital and land, transfers, consumption")
        for q in DECILES:
            r = d.loc[q]
            print("%-8s  %.3f  %.3f | %+.3f | %.3f  %.3f  %.3f  %.3f" % (q, r["labour_of_market_income"], r["labour_of_income"],
                  r["exposure"], r["share_of_labour_income"], r["share_of_capital_and_land"], r["share_of_transfers"],
                  r["share_of_consumption"]))
        g = grp[grp.year == y].set_index("group")
        for name in list(GROUPS) + ["everyone"]:
            r = g.loc[name]
            print("%-17s labour %.3f of income, exposure %+.3f | holds %.3f of labour income, %.3f of capital and land, "
                  "%.3f of transfers; does %.3f of consumption" % (name, r["labour_of_income"], r["exposure"],
                  r["share_of_labour_income"], r["share_of_capital_and_land"], r["share_of_transfers"], r["share_of_consumption"]))
    print("\n2023, what the basket does: labour's share of the factor cost of a basket by its share of spending on shelter")
    for s in (0.0, float(tabs["made"].loc[2023, "shelter_share"]), 0.30, 0.40):
        print("  shelter %.0f%% of spending: %.3f; a household living on wages alone is exposed by %+.3f"
              % (100 * s, basket(tabs, 2023, s), 1.0 - basket(tabs, 2023, s)))
    e = grp[grp.group == "everyone"].set_index("year")["exposure"]
    print("\neveryone together, 2004-2023: exposure mean %+.3f, from %+.3f to %+.3f (it should be near zero: the accounts add up)"
          % (e.mean(), e.min(), e.max()))
    for name in GROUPS:
        x = grp[grp.group == name].set_index("year")["exposure"]
        print("%-17s exposure 2004 %+.3f, 2023 %+.3f, mean %+.3f" % (name, x[2004], x[2023], x.mean()))

    held, s_now = market_shares(tabs, 2023)
    print("\n2023, market income (labour, and capital and land with accrued corporate income): labour is paid %.3f of it" % s_now)
    print("group              holds of labour, of capital and land | share of market income today, with labour paid 0.17, "
          "with labour paid nothing | the same with a fifth held in common | common share that holds today's share at 0.17, at nothing")
    for g in GROUPS:
        h = held[g]
        print("%-17s  %.3f  %.3f |  %.3f  %.3f  %.3f |  %.3f  %.3f |  %.3f  %.3f"
              % (g, h["labour"], h["capital"], income_share(h, s_now), income_share(h, 0.17), income_share(h, 0.0),
                 income_share(h, 0.17, 0.2), income_share(h, 0.0, 0.2), holding_share(h, s_now, 0.17), holding_share(h, s_now, 0.0)))
    ss, s0, s1 = shift_share(tabs, 2004, 2023)
    print("\n2004-2023: labour's share of market income went from %.3f to %.3f. Each group's share of market income:" % (s0, s1))
    for g in GROUPS:
        r = ss[g]
        print("%-17s  %.3f -> %.3f: %+.4f from payments moving between claims, %+.4f from its holdings changing"
              % (g, r["before"], r["after"], r["between"], r["within"]))
