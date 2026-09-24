# financing.py — is the most care a society employs set by need, or by what it can finance? Her observations
# (2026-09-24): the crash model's ceiling for care is Norway's share of employment, and "Norway also has their sovereign
# wealth fund, idk why but I think that is related"; then "even if they don't draw from the fund, the fund's existence
# may lower their borrowing costs". Three questions, stated before the data were fitted:
#   1. across OECD economies, what goes with care's share of employment (health and social work, ISIC Q; ILOSTAT):
#      public spending on long-term care (the labour-heavy part of care), public spending on health, total health
#      spending, income (GDP per capita, PPP), or need (the share of the population 65 and over)? Single-variable fits
#      and one joint fit; heteroskedasticity-robust t-statistics. For Norway both spending and income are also put on
#      mainland GDP (oil and gas production inflates GDP, not the economy that pays for care) — stated, and shown both ways;
#   2. the spending channel, Norway: what the fund transfers into the state budget each year (the state's net cash
#      flow from petroleum less its net transfer to the fund; Statistics Norway 11012 and 10486) against mainland GDP
#      and against public spending on health and long-term care (OECD health accounts);
#   3. the balance-sheet channel: does a government's long-term borrowing rate rise with its net debt (OECD Economic
#      Outlook: net financial liabilities, long- and short-term rates, 2010-24, with year effects), and does it rise more
#      without a central bank of one's own (the euro area) and in a crisis (2010-13)? Where does Norway stand?
# Data: OECD health accounts (SHA, via the OECD's public SDMX API: expenditure by financing scheme and function, % of
# GDP; the cached copy is trimmed to totals across provider and mode of provision), OECD Economic Outlook, ILOSTAT,
# World Bank (GDP per capita PPP, population 65+), Statistics Norway; for the crash model's financing limit, taxes on
# labour income by region (OECD Global Revenue Statistics). Cached under
# cache/oecd/, cache/ilo/, cache/worldbank/, cache/ssb_no/ (fetched with the Windows certificate store; see STATE.md).
#
# Run from paths/:  ../venv/Scripts/python.exe code/financing.py
# Out: results/financing.json, figures/fig_financing.png

from __future__ import annotations

import glob
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import exposure as ex  # noqa: E402

C = os.path.join(ROOT, "cache")
EURO = ("AUT", "BEL", "DEU", "ESP", "FIN", "FRA", "GRC", "IRL", "ITA", "NLD", "PRT", "SVK", "SVN", "EST", "LVA", "LTU", "LUX")
NOT_COUNTRIES = ("EA17", "OECD", "CHN", "IND", "BRA", "IDN", "ZAF", "ARG", "BGR", "HRV", "ROU", "PER", "THA")


def ols(y, cols) -> dict:
    """OLS with a constant; heteroskedasticity-robust (HC1) t-statistics."""
    X = np.column_stack([np.ones(len(y))] + [np.asarray(c, float) for c in cols])
    y = np.asarray(y, float)
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    e = y - X @ b
    n, k = X.shape
    XtXi = np.linalg.inv(X.T @ X)
    V = XtXi @ (X.T * e ** 2) @ X @ XtXi * n / (n - k)
    return {"b": b, "t": b / np.sqrt(np.diag(V)), "r2": float(1 - e @ e / ((y - y.mean()) @ (y - y.mean()))), "resid": e}


def jsonstat(fp: str) -> pd.Series:
    j = json.load(open(fp, encoding="utf-8"))
    cats = [list(j["dimension"][d]["category"]["index"]) for d in j["id"]]
    return pd.Series(j["value"], index=pd.MultiIndex.from_product(cats, names=j["id"]))


# ------------------------------------------------------------------ the pieces
def health_accounts() -> pd.DataFrame:
    s = pd.read_csv(os.path.join(C, "oecd", "sha_health_ltc_pct_gdp.csv"), low_memory=False)
    s = s[(s.MODE_PROVISION == "_T") & (s.PROVIDER == "_T") & (s.FINANCING_SCHEME_REV == "_Z")]
    return s.pivot_table(index=["REF_AREA", "TIME_PERIOD"], columns=["FINANCING_SCHEME", "FUNCTION"], values="OBS_VALUE")


def care_shares() -> pd.Series:
    out = {}
    for f in glob.glob(os.path.join(C, "ilo", "EMP_TEMP_SEX_ECO_NB_A_*.csv")):
        a = os.path.basename(f).replace("EMP_TEMP_SEX_ECO_NB_A_", "").replace("_all.csv", "").replace(".csv", "")
        try:
            d = pd.read_csv(f, encoding="utf-8-sig")
        except pd.errors.EmptyDataError:
            continue
        if d.empty or "classif1" not in d:
            continue
        d = d[(d.sex == "SEX_T") & d.classif1.isin(["ECO_ISIC4_Q", "ECO_ISIC4_TOTAL"])].dropna(subset=["obs_value"])
        if d.empty:
            continue
        x = d[d.time == d.time.max()].set_index("classif1").obs_value
        if "ECO_ISIC4_Q" in x:
            out[a] = float(100 * x["ECO_ISIC4_Q"] / x["ECO_ISIC4_TOTAL"])
    return pd.Series(out)


def world_bank(ind: str) -> pd.Series:
    j = json.load(open(os.path.join(C, "worldbank", f"{ind}.json"), encoding="utf-8"))[1]
    df = pd.DataFrame([(r["countryiso3code"], int(r["date"]), r["value"]) for r in j if r["value"] is not None], columns=["a", "y", "v"])
    return df.sort_values("y").groupby("a").v.last()


def norway() -> dict:
    """The fund's transfer into the state budget, mainland GDP, and public health and long-term care spending, NOK bn."""
    fisc = jsonstat(os.path.join(C, "ssb_no", "10486_fiscal_account.json")).droplevel("ContentsCode")
    pet = jsonstat(os.path.join(C, "ssb_no", "11012_petroleum_cash_flow.json"))
    gdp = jsonstat(os.path.join(C, "ssb_no", "09189_gdp_mainland.json")).droplevel("ContentsCode")
    ha = health_accounts()
    years = [str(y) for y in range(2010, 2026)]
    out = {}
    for y in years:
        cash = float(pet[("StatensNettoKont", y)]) / 1000
        to_fund = float(fisc[("PETROL_FOND", y)]) / 1000
        g, gm = float(gdp[("bnpb.nr23_9", y)]) / 1000, float(gdp[("bnpb.nr23_9fn", y)]) / 1000
        row = {"petroleum_cash_flow": round(cash, 1), "net_transfer_to_fund": round(to_fund, 1), "fund_to_budget": round(cash - to_fund, 1),
               "gdp": round(g, 1), "mainland_gdp": round(gm, 1), "fund_to_budget_pct_mainland_gdp": round(100 * (cash - to_fund) / gm, 2)}
        key = ("NOR", int(y))
        if key in ha.index and pd.notna(ha.loc[key, ("HF1", "_T")]):
            hcr1 = ha.loc[key].get(("HF1", "HCR1"))
            pub = float(ha.loc[key, ("HF1", "_T")]) + (float(hcr1) if pd.notna(hcr1) else 0.0)     # health (incl. its LTC) + social LTC
            row["public_health_and_ltc_nok_bn"] = round(pub / 100 * g, 1)
            row["public_health_and_ltc_pct_mainland_gdp"] = round(pub * g / gm, 2)
            row["fund_to_budget_vs_public_health_and_ltc"] = round((cash - to_fund) / (pub / 100 * g), 2)
        out[y] = row
    return out


def cross_section(nor: dict) -> dict:
    ha = health_accounts()
    last = lambda col: ha[col].dropna().groupby(level=0).last()  # noqa: E731
    last_year = lambda col: ha[col].dropna().reset_index().groupby("REF_AREA").TIME_PERIOD.last()  # noqa: E731
    D = pd.DataFrame({"care": care_shares(), "pub_ltc": last(("HF1", "LTC_TOT")), "pub_health": last(("HF1", "_T")),
                      "tot_health": last(("_T", "_T")), "gdp_pc": world_bank("NY.GDP.PCAP.PP.KD"), "old65": world_bank("SP.POP.65UP.TO.ZS")}).dropna()
    # Norway on mainland GDP, each figure with its own year's ratio of GDP to mainland GDP
    ratio = lambda y: nor[str(y)]["gdp"] / nor[str(y)]["mainland_gdp"]  # noqa: E731
    ltc_year, health_year = int(last_year(("HF1", "LTC_TOT"))["NOR"]), int(last_year(("HF1", "_T"))["NOR"])
    wb = json.load(open(os.path.join(C, "worldbank", "NY.GDP.PCAP.PP.KD.json"), encoding="utf-8"))[1]
    wb_year = max(int(r["date"]) for r in wb if r["countryiso3code"] == "NOR" and r["value"] is not None)
    Dm = D.copy()
    Dm.loc["NOR", "pub_ltc"] *= ratio(ltc_year)
    Dm.loc["NOR", "pub_health"] *= ratio(health_year)
    Dm.loc["NOR", "gdp_pc"] /= ratio(wb_year)
    single, single_rich = {}, {}
    for v in ("pub_ltc", "pub_health", "tot_health", "gdp_pc", "old65"):
        for tag, df, store in (("all", Dm, single), ("rich", Dm[Dm.gdp_pc > 45000], single_rich)):
            x = np.log(df[v]) if v == "gdp_pc" else df[v]
            r = ols(df.care, [x])
            store[v] = {"r2": round(r["r2"], 2), "slope": round(float(r["b"][1]), 2), "t": round(float(r["t"][1]), 1)}
    joint = {}
    for tag, df in (("GDP", D), ("Norway on mainland GDP", Dm)):
        r = ols(df.care, [df.pub_ltc, np.log(df.gdp_pc), df.old65])
        res = pd.Series(r["resid"], index=df.index)
        joint[tag] = {"public_ltc": {"slope": round(float(r["b"][1]), 2), "t": round(float(r["t"][1]), 1)},
                      "log_gdp_pc": {"slope": round(float(r["b"][2]), 2), "t": round(float(r["t"][2]), 1)},
                      "old65": {"slope": round(float(r["b"][3]), 2), "t": round(float(r["t"][3]), 1)},
                      "r2": round(r["r2"], 2), "residual": {k: round(float(res[k]), 2) for k in ("NOR", "DNK", "SWE", "FIN", "NLD", "USA", "DEU")}}
    top = Dm.sort_values("pub_ltc", ascending=False).head(6)
    return {"countries": len(D), "rich_countries": int((Dm.gdp_pc > 45000).sum()), "rich_threshold_gdp_pc_ppp": 45000,
            "single": single, "single_rich": single_rich, "joint": joint,
            "norway_gdp_over_mainland": {"long-term care, " + str(ltc_year): round(ratio(ltc_year), 3), "health, " + str(health_year): round(ratio(health_year), 3),
                                          "income, " + str(wb_year): round(ratio(wb_year), 3)},
            "highest_public_ltc_pct_gdp": {k: round(float(v), 2) for k, v in top.pub_ltc.items()},
            "_D": D, "_Dm": Dm}


def borrowing() -> dict:
    e = pd.read_csv(os.path.join(C, "oecd", "eo_debt_rates.csv"), low_memory=False)
    w = e.pivot_table(index=["REF_AREA", "TIME_PERIOD"], columns="MEASURE", values="OBS_VALUE").reset_index()
    w = w[~w.REF_AREA.isin(NOT_COUNTRIES)]
    w["term"] = w.IRL - w.IRS

    def fe(df, y):
        d = df.dropna(subset=[y, "GNFLQ"]).copy()
        yd = d[y] - d.groupby("TIME_PERIOD")[y].transform("mean")
        xd = d.GNFLQ - d.groupby("TIME_PERIOD").GNFLQ.transform("mean")
        b = float((xd * yd).sum() / (xd ** 2).sum())
        return {"bp_per_10_points_net_debt": round(100 * 10 * b, 1), "observations": len(d), "countries": int(d.REF_AREA.nunique())}
    cases = {"OECD 2010-24": w[w.TIME_PERIOD.between(2010, 2024)],
             "own central bank 2010-24": w[~w.REF_AREA.isin(EURO) & w.TIME_PERIOD.between(2010, 2024)],
             "euro area 2010-24": w[w.REF_AREA.isin(EURO) & w.TIME_PERIOD.between(2010, 2024)],
             "euro area crisis 2010-13": w[w.REF_AREA.isin(EURO) & w.TIME_PERIOD.between(2010, 2013)],
             "euro area calm 2015-19": w[w.REF_AREA.isin(EURO) & w.TIME_PERIOD.between(2015, 2019)]}
    out = {k: {"long_rate": fe(df, "IRL"), "long_less_short": fe(df, "term")} for k, df in cases.items()}
    nor = w[w.REF_AREA == "NOR"].set_index("TIME_PERIOD")
    peers = w[w.REF_AREA.isin(["NOR", "SWE", "DNK", "CHE", "DEU", "USA", "ITA", "JPN"]) & w.TIME_PERIOD.between(2010, 2024)]
    avg = peers.groupby("REF_AREA")[["GNFLQ", "GGFLQ", "term"]].mean().round(2)
    return {"slopes": out, "norway_net_financial_liabilities_pct_gdp": {int(y): round(float(v), 1) for y, v in nor.GNFLQ.dropna().items() if y >= 2008},
            "norway_gross_liabilities_pct_gdp": {int(y): round(float(v), 1) for y, v in nor.GGFLQ.dropna().items() if y >= 2008},
            "peers_2010_24_mean": avg.to_dict(orient="index"), "_w": w}


REGIONS = {"US": ("USA",), "EA": ("DEU", "FRA", "ITA", "ESP", "NLD"), "SE": ("SWE",), "CN": ("CHN",)}
OECD = ("AUS", "AUT", "BEL", "CAN", "CHE", "CHL", "COL", "CRI", "CZE", "DEU", "DNK", "ESP", "EST", "FIN", "FRA", "GBR", "GRC", "HUN",
        "IRL", "ISL", "ISR", "ITA", "JPN", "KOR", "LTU", "LUX", "LVA", "MEX", "NLD", "NOR", "NZL", "POL", "PRT", "SVK", "SVN", "SWE", "TUR", "USA")


def labour_taxes() -> dict:
    """Taxes that fall on labour income, % of GDP (OECD Global Revenue Statistics, general government, latest year):
    taxes on individuals' income (which include their capital income: an upper bound on the labour part), social
    security contributions, payroll taxes. For the crash model's financing limit: how far each region's take could rise
    before it reaches the highest in the OECD, on a wage base that displacement shrinks."""
    r = pd.read_csv(os.path.join(C, "oecd", "revenue_by_tax_pct_gdp.csv"), low_memory=False)
    r = r[r.CTRY_SPECIFIC_REVENUE == "_T"]
    p = r.pivot_table(index=["REF_AREA", "TIME_PERIOD"], columns="STANDARD_REVENUE", values="OBS_VALUE").reset_index()
    p = p.dropna(subset=["_T"]).sort_values("TIME_PERIOD").groupby("REF_AREA").last()
    p["labour"] = p[["T_1100", "T_2000", "T_3000"]].fillna(0).sum(axis=1)
    o = p.loc[[c for c in OECD if c in p.index]]
    top = o.labour.idxmax()
    out = {"oecd_highest": {"country": top, "labour_taxes_pct_gdp": round(float(o.labour.max()), 1), "year": int(o.loc[top, "TIME_PERIOD"])}, "regions": {}}
    for reg, cs in REGIONS.items():
        w = {c: sum(ex.shares(c)["employment"].values()) for c in cs}           # euro area: employment weights
        tot = sum(w.values())
        val = lambda col: sum(w[c] * float(p.loc[c, col]) for c in cs) / tot  # noqa: E731
        out["regions"][reg] = {"labour_taxes_pct_gdp": round(val("labour"), 2), "all_taxes_pct_gdp": round(val("_T"), 2),
                               "corporate_pct_gdp": round(val("T_1200"), 2), "year": int(max(p.loc[c, "TIME_PERIOD"] for c in cs))}
    out["norway"] = {"labour_taxes_pct_gdp": round(float(p.loc["NOR", "labour"]), 1), "corporate_pct_gdp": round(float(p.loc["NOR", "T_1200"]), 1)}
    return out


def main():
    nor = norway()
    cs = cross_section(nor)
    bw = borrowing()
    out = {"cross_section": {k: v for k, v in cs.items() if not k.startswith("_")}, "norway": nor,
           "borrowing": {k: v for k, v in bw.items() if not k.startswith("_")}, "labour_taxes": labour_taxes()}
    json.dump(out, open(os.path.join(ROOT, "results", "financing.json"), "w", encoding="utf-8"), indent=1)
    print(json.dumps(out["cross_section"], indent=1))
    for y in ("2019", "2022", "2023", "2024", "2025"):
        print(y, nor[y])
    print(json.dumps(out["borrowing"], indent=1))
    figure(cs, nor, bw)


def figure(cs, nor, bw):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams["axes.titlesize"] = 10
    fig, ax = plt.subplots(1, 3, figsize=(19, 5.6), layout="constrained")
    fig.get_layout_engine().set(rect=(0, 0.05, 1, 0.95))
    D, Dm = cs["_D"], cs["_Dm"]
    for a_, (x, lab) in zip(ax[:2], (("pub_ltc", "public spending on long-term care, % of GDP"), ("old65", "population 65 and over, %"))):
        a_.scatter(Dm[x], Dm.care, s=18, color="C0")
        for k in Dm.index:
            a_.annotate(k, (Dm.loc[k, x], Dm.care[k]), fontsize=7, xytext=(2, 2), textcoords="offset points")
        if x == "pub_ltc":
            a_.scatter([D.loc["NOR", x]], [D.care["NOR"]], s=18, facecolors="none", edgecolors="C3")
            a_.annotate("NOR on total GDP", (D.loc["NOR", x], D.care["NOR"]), fontsize=7, color="C3", xytext=(2, -9), textcoords="offset points")
        r = cs["single"][x]
        a_.set_xlabel(lab); a_.set_ylabel("health and social work, % of employment")
        a_.set_title(f"Care's share of jobs against {lab.split(',')[0]} (R² {r['r2']})")
    ys = [y for y in nor if "fund_to_budget_vs_public_health_and_ltc" in nor[y]]
    a_ = ax[2]
    a_.plot([int(y) for y in nor], [nor[y]["fund_to_budget_pct_mainland_gdp"] for y in nor], color="C3", marker="o", ms=3,
            label="the fund's transfer into the state budget")
    a_.plot([int(y) for y in ys], [nor[y]["public_health_and_ltc_pct_mainland_gdp"] for y in ys], color="C0", marker="o", ms=3,
            label="public spending on health and long-term care")
    a_.set_title("Norway, % of mainland GDP"); a_.legend(fontsize=8); a_.set_ylim(0, None)
    fig.text(0.01, 0.01, "OECD health accounts (government/compulsory schemes) and Economic Outlook; ILOSTAT (ISIC Q); World Bank; Statistics Norway "
             "(10486, 11012, 09189). Norway on mainland GDP in the scatter (oil and gas inflate GDP); the open marker is Norway on total GDP.", fontsize=7.5)
    fig.savefig(os.path.join(ROOT, "figures", "fig_financing.png"), dpi=120)


if __name__ == "__main__":
    main()
