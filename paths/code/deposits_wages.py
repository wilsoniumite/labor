# deposits_wages.py — do Swedish households' bank deposits follow the wage sum, or income and wealth
# more broadly? The deposit franchise is where the paper's mechanism meets a bank's net interest income:
# if salary and savings balances are a wage franchise, a falling wage bill shrinks the cheapest funding a
# bank has; if they follow household income and wealth, the owners' side of the same economy refills them.
#
# Public data only. Statistics Sweden: financial accounts (FM0103, households S14 — transferable deposits
# F.22, other deposits F.29, equity F.51, investment fund shares F.52; quarterly balances 1996-2026);
# household disposable income by transaction item (NR0103, S14 — wages and salaries D.11, property income
# D.4, social benefits D.62, disposable income B.6n; quarterly 1980-2026); banks' deposit rates for
# households (FM5001C RantaT05, via floor_margins.py). Sveriges Riksbank: the policy rate (SWEA).
#
# The questions, stated before the data were fitted (a stock of deposits against the flows that feed it):
#   1. growth — does a year's deposit growth follow that year's wage growth?
#   2. stock and flow — deposits accumulate saving; does wage growth add anything once saving is in?
#   3. the wage share — relative to household income, are deposits higher or lower when wages are a larger
#      share of that income? (A wage franchise says higher.)
#   4. rates — how much do deposits fall, relative to income, when holding them costs more (the policy rate
#      over the rate on demand deposits)? The 2022-24 hikes are the one large up-move in the sample.
#   5. for a model whose income shifts from wages to owners: what share of the economy's non-wage income
#      (net operating surplus and mixed income, sector accounts S1) reaches households (their own surplus and
#      mixed income plus net property income, S14)?
# Standard errors Newey-West (4 quarters). Saving is disposable income less consumption, before the
# adjustment for pension entitlements (D.8), so it runs negative before ~2009; its level is not the point.
#
# Run from paths/:  ../venv/Scripts/python.exe code/deposits_wages.py
# Out: results/deposits_wages.json, figures/fig_deposits_wages.png

from __future__ import annotations

import json
import os
import sys
import time

import numpy as np
import pandas as pd
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import floor_margins as fm  # noqa: E402
import se_1990s as rb  # noqa: E402
from regime_digestion import ols_hac  # noqa: E402

API = "https://api.scb.se/OV0104/v1/doris/en/ssd/"
H = {"User-Agent": "Mozilla/5.0 (research; laborformal)"}


def scb_table(table: str, query: dict, name: str) -> pd.DataFrame:
    """A Statistics Sweden table (all periods), one column per value of the one variable listed with several
    values; cached as JSON in cache/scb."""
    path = os.path.join(ROOT, "cache", "scb", f"{name}.json")
    if not os.path.exists(path):
        body = {"query": [{"code": k, "selection": {"filter": "item", "values": v if isinstance(v, list) else [v]}} for k, v in query.items()],
                "response": {"format": "json"}}
        for wait in (0, 5, 20, 60):
            time.sleep(wait)
            try:
                r = requests.post(API + table, json=body, timeout=120, headers=H)
                r.raise_for_status()
                break
            except requests.RequestException:
                if wait == 60:
                    raise
        os.makedirs(os.path.dirname(path), exist_ok=True)
        json.dump(r.json(), open(path, "w", encoding="utf-8"))
    js = json.load(open(path, encoding="utf-8"))
    multi = [k for k, v in query.items() if isinstance(v, list) and len(v) > 1]
    pos = [c["code"] for c in js["columns"] if c["type"] == "d"].index(multi[0]) if multi else None
    rows = {}
    for d in js["data"]:
        per, col = d["key"][-1], (d["key"][pos] if multi else name)
        v = d["values"][0]
        rows.setdefault(pd.Period(per.replace("K", "Q"), "Q"), {})[col] = float(v) if v not in ("..", "", "-") else np.nan
    return pd.DataFrame.from_dict(rows, orient="index").sort_index()


def data() -> pd.DataFrame:
    """Quarterly, 1996Q1 onward: household balances (SEK bn, end of quarter), income flows over the last four
    quarters (SEK bn a year), and quarter-average rates (%)."""
    fa = scb_table("FM/FM0103/FM0103A/FirENS2010ofKv",
                   {"Sektor": "S14", "Kontopost": ["FA2200", "FA2900", "FA5100", "FA5200", "FA0100"], "Motsektor": "S0",
                    "ContentsCode": "FM0103AS"}, "fa_households") / 1e3
    fa.columns = [{"FA2200": "dep_transferable", "FA2900": "dep_other", "FA5100": "equity", "FA5200": "funds",
                   "FA0100": "fin_assets"}[c] for c in fa.columns]
    inc = scb_table("NR/NR0103/NR0103C/HusDispInkENS2010Kv",
                    {"Transaktionspost": ["D11.REC", "D4.REC", "D62.REC", "B6n", "P31.PAY"], "ContentsCode": "NR0103DV"},
                    "income_households") / 1e3
    inc.columns = [{"D11.REC": "wages", "D4.REC": "property_income", "D62.REC": "benefits", "B6n": "disposable",
                    "P31.PAY": "consumption"}[c] for c in inc.columns]
    inc = inc.rolling(4).sum()
    rates = pd.DataFrame({"dep_demand": fm.scb("RantaT05", {"Referenssektor": "1.1b", "Motpartssektor": "2", "Avtal": "0200", "Rantebindningstid": "3"}, "dep_hh_demand_stock"),
                          "dep_all": fm.scb("RantaT05", {"Referenssektor": "1.1b", "Motpartssektor": "2", "Avtal": "0200", "Rantebindningstid": "1"}, "dep_hh_all_stock")})
    pol = rb.fetch("SECBREPOEFF", "1994-01-01", "2026-09-24")
    pol.index = pd.to_datetime(pol.index)
    rates["policy"] = pol.groupby(pol.index.to_period("M")).mean()
    rates = rates.groupby(rates.index.asfreq("Q")).mean()
    df = fa.join(inc, how="left").join(rates, how="left")
    df["deposits"] = df.dep_transferable + df.dep_other
    df["wealth_market"] = df.equity + df.funds
    return df.loc["1996Q1":]


def nonwage_share_to_households() -> pd.Series:
    """Households' own net operating surplus and mixed income plus their net property income, over the whole
    economy's net operating surplus and mixed income; four-quarter sums."""
    t = {sec: scb_table("NR/NR0103/NR0103C/SektorENS2010Kv", {"Sektor": sec, "Transaktionspost": ["B2+B3n", "D4.REC", "D4.PAY", "D11.REC", "B5g"],
                                                            "ContentsCode": "NR0103DT"}, f"sector_{sec}").rolling(4).sum() for sec in ("S1", "S14")}
    return ((t["S14"]["B2+B3n"] + t["S14"]["D4.REC"] - t["S14"]["D4.PAY"]) / t["S1"]["B2+B3n"]).dropna()


LAGS = 4


def fit(y, cols: dict) -> dict:
    X = np.column_stack(list(cols.values()))
    b, se = ols_hac(np.asarray(y, float), X, LAGS)
    e = np.asarray(y, float) - np.column_stack([np.ones(len(y)), X]) @ b
    out = {"n": int(len(y)), "r2": round(float(1 - e.var() / np.var(y)), 3), "const": round(float(b[0]), 4)}
    for k, (bb, ss) in zip(cols, zip(b[1:], se[1:])):
        out[k] = {"coef": round(float(bb), 4), "se": round(float(ss), 4)}
    return out


def analyse(d: pd.DataFrame) -> dict:
    d = d.dropna(subset=["deposits", "wages", "disposable", "consumption", "policy", "dep_demand"]).copy()
    L = np.log
    d["oc"] = d.policy - d.dep_demand
    d["saving"] = d.disposable - d.consumption
    d["t"] = np.arange(len(d)) / 4.0
    g = pd.DataFrame({"dep": L(d.deposits).diff(4), "w": L(d.wages).diff(4), "y": L(d.disposable).diff(4)}).dropna()
    f = pd.DataFrame({"dD": d.deposits.diff(4), "S": d.saving, "dW": d.wages.diff(4), "doc": d.oc.diff(4), "DW": (d.deposits / d.wages).shift(4)}).dropna()
    dy = L(d.deposits / d.disposable)
    out = {"sample": [str(d.index[0]), str(d.index[-1])],
           "levels_sek_bn": {str(k): {"deposits": round(float(r.deposits), 1), "wages": round(float(r.wages), 1), "disposable": round(float(r.disposable), 1)}
                             for k, r in d.loc[[d.index[0], pd.Period("2002Q1", "Q"), pd.Period("2022Q1", "Q"), d.index[-1]]].iterrows()},
           "deposits_over_disposable": {str(k): round(float(v), 3) for k, v in (d.deposits / d.disposable).loc[["1996Q1", "2002Q1", "2012Q1", "2022Q1", "2024Q2", str(d.index[-1])]].items()},
           "wage_share_of_disposable_range": [round(float((d.wages / d.disposable).min()), 3), round(float((d.wages / d.disposable).max()), 3)]}
    out["1_growth_on_wage_growth"] = fit(g.dep, {"wage growth": g.w})
    out["1b_growth_on_income_growth"] = fit(g.dep, {"income growth": g.y})
    sf = fit(f.dD, {"saving": f.S, "wage change": f.dW, "cost change": f.doc})
    DW = float(f.DW.mean())
    sf["wage_franchise_implies_wage_change_coef"] = round(DW, 3)
    sf["t_against_wage_franchise"] = round((sf["wage change"]["coef"] - DW) / sf["wage change"]["se"], 2)
    out["2_stock_flow"] = sf
    out["3_wage_share_levels"] = fit(dy, {"log wage share": L(d.wages / d.disposable), "cost": d.oc, "trend": d.t})
    out["3b_wage_share_no_trend"] = fit(dy, {"log wage share": L(d.wages / d.disposable), "cost": d.oc})
    out["4_cost_no_trend"] = fit(dy, {"cost": d.oc})
    out["4b_cost_with_trend"] = fit(dy, {"cost": d.oc, "trend": d.t})
    a, b = pd.Period("2021Q4", "Q"), pd.Period("2024Q2", "Q")
    ep = {"cost_pp": [round(float(d.oc[a]), 2), round(float(d.oc[b]), 2)], "deposits_over_disposable": [round(float(np.exp(dy[a])), 3), round(float(np.exp(dy[b])), 3)]}
    ep["semi_elasticity_per_pp"] = round(float((dy[b] - dy[a]) / (d.oc[b] - d.oc[a])), 4)
    out["4c_hikes_2021Q4_2024Q2"] = ep
    th = nonwage_share_to_households()
    out["5_nonwage_share_to_households"] = {"mean_1996_2025": round(float(th.loc["1996Q4":"2025Q4"].mean()), 3),
                                            "mean_2015_2025": round(float(th.loc["2015Q4":"2025Q4"].mean()), 3),
                                            "min": round(float(th.min()), 3), "max": round(float(th.max()), 3)}
    return out, d


def figure(d: pd.DataFrame, r: dict):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams["axes.titlesize"] = 10
    fig, ax = plt.subplots(1, 3, figsize=(16, 5.2), layout="constrained")
    fig.get_layout_engine().set(rect=(0, 0.04, 1, 0.96))
    a = ax[0]
    for col, lab in (("deposits", "household deposits"), ("wages", "wages and salaries (a year)"), ("disposable", "disposable income (a year)")):
        a.plot(d.index.to_timestamp(), d[col] / d[col].iloc[0], label=lab)
    a.set_yscale("log"); a.set_yticks([1, 2, 3, 4, 6]); a.set_yticklabels(["1", "2", "3", "4", "6"]); a.minorticks_off()
    a.set_title("1. Deposits outgrew wages and income\nindex, 1996Q1 = 1, log scale"); a.legend(fontsize=8)
    a = ax[1]
    g = pd.DataFrame({"dep": np.log(d.deposits).diff(4) * 100, "w": np.log(d.wages).diff(4) * 100}).dropna()
    a.scatter(g.w, g.dep, s=10, alpha=0.7)
    c = r["1_growth_on_wage_growth"]
    xs = np.linspace(g.w.min(), g.w.max(), 10)
    a.plot(xs, c["const"] * 100 + c["wage growth"]["coef"] * xs, color="k", lw=1)
    a.set_xlabel("wage growth over the year, %"); a.set_ylabel("deposit growth over the year, %")
    a.set_title(f"2. Deposit growth does not follow wage growth\nslope {c['wage growth']['coef']:.2f} (s.e. {c['wage growth']['se']:.2f}), R² {c['r2']:.2f}")
    a = ax[2]
    t = d.index.to_timestamp()
    a.plot(t, d.deposits / d.disposable, color="C0", label="deposits / disposable income")
    a.set_ylabel("ratio", color="C0")
    b2 = a.twinx()
    b2.plot(t, d.policy - d.dep_demand, color="C3", lw=1, label="cost of holding: policy rate - demand deposit rate")
    b2.set_ylabel("pp", color="C3")
    h1, l1 = a.get_legend_handles_labels()
    h2, l2 = b2.get_legend_handles_labels()
    a.legend(h1 + h2, l1 + l2, fontsize=8, loc="upper left")
    a.set_title("3. Relative to income, deposits fall\nwhen holding them costs more (2022-24)")
    fig.text(0.01, 0.005, "Sources: Statistics Sweden (financial accounts FM0103, household income NR0103, deposit rates FM5001C), Sveriges Riksbank (SWEA). Households S14; income over the last four quarters.", fontsize=7)
    os.makedirs(os.path.join(ROOT, "figures"), exist_ok=True)
    fig.savefig(os.path.join(ROOT, "figures", "fig_deposits_wages.png"), dpi=130)


def main():
    r, d = analyse(data())
    r["sources"] = "SCB FM0103 FirENS2010ofKv (S14: FA2200, FA2900, FA5100, FA5200, FA0100), NR0103 HusDispInkENS2010Kv (S14: D11, D4, D62, B6n, P31), FM5001C RantaT05; Riksbank SWEA SECBREPOEFF"
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    json.dump(r, open(os.path.join(ROOT, "results", "deposits_wages.json"), "w", encoding="utf-8"), indent=1)
    print(json.dumps(r, indent=1))
    figure(d, r)


if __name__ == "__main__":
    main()
