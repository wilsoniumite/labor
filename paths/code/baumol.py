# baumol.py — where the jobs are going. Her question (2026-09-24): most job growth has been going to women, which
# sounds like care and other labour-intensive work — Baumol concentration? The paper grants the mechanism its own
# proposition (Appendix, "Human-required tasks", Proposition "Baumol concentration"): expenditure concentrating on the
# sector whose costs refuse to fall can hold labour's share up — if substitution away from it is weak (sigma_H < 1) —
# while the median wage falls ("aggregate rescue, median collapse"), and care in the subsistence bundle raises its
# cost. This module measures how far along that road the data are, and what it means for a bust:
#   1. where net job growth went: US payrolls by sector and sex, monthly to the latest release (BLS via FRED); the US,
#      Sweden and five euro-area countries by industry (ISIC) and sex, annual to 2025 (ILOSTAT, labour force surveys);
#      China (ILO modelled estimates);
#   2. whether care holds up in recessions (US 2001, 2008-10, 2020) and what austerity did to public employment
#      (US state and local government, 2008-13);
#   3. Baumol's premise, US: health care's price against goods and all consumer prices, and its share of consumer
#      spending, 1990-2026 (BEA via FRED); the elasticity the two imply, window by window — a descriptive ratio, not
#      an identified elasticity (ageing, insurance coverage and incomes move the share too);
#   4. what the absorbing sector pays: health and social work against the average, by country (ILOSTAT earnings by
#      industry); US education and health against all private hourly earnings, 2006-2026;
#   5. who pays for it: US Medicare and Medicaid benefits against consumer spending on health care (BEA via FRED);
#      the public share of employers in health and education (ILOSTAT, where published).
#
# Run from paths/:  ../venv/Scripts/python.exe code/baumol.py
# Out: results/baumol.json, figures/fig_baumol.png

from __future__ import annotations

import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(ROOT), "pinning", "code"))
import exposure as ex  # noqa: E402
import lambda_compute2 as _lc  # noqa: E402

_lc.CACHE = os.path.join(ROOT, "cache")
LFS = ("USA", "SWE", "DEU", "FRA", "ITA", "ESP", "NLD")
CARE = ("Q", "P")                      # health and social work; education
IN_PERSON = ("I", "R", "S", "T")       # accommodation and food; arts; other services; households as employers
COGNITIVE = ("J", "K", "M")            # information and communication; finance; professional and scientific


def fred(sid: str) -> pd.Series:
    s = _lc.pull_fred(sid)
    if s is None:
        raise SystemExit(f"FRED {sid}: not available")
    return s


# ------------------------------------------------------------------ 1-2. the US, monthly
def us_payrolls() -> dict:
    pay, women, care = fred("PAYEMS"), fred("CES0000000010"), fred("CES6562000001")
    educ, gov = fred("CES6561000001"), fred("USGOVT")
    state, local = fred("CES9092000001"), fred("CES9093000001")
    sup = {s: fred(s) for s in ("USMINE", "USCONS", "MANEMP", "USTPU", "USINFO", "USFIRE", "USPBS", "USEHS", "USLAH", "USSERV", "USGOVT")}
    end = pay.index[-1]
    windows = {}
    for label, start in (("12 months", end - pd.DateOffset(months=12)), ("24 months", end - pd.DateOffset(months=24)),
                         ("36 months", end - pd.DateOffset(months=36)), ("since 2022", pd.Timestamp("2022-01-01")),
                         ("since the pre-pandemic peak", pd.Timestamp("2019-12-01"))):
        d = lambda s: float(s[end] - s[start])  # noqa: E731
        net = d(pay)
        windows[label] = {"from": str(start.date())[:7], "to": str(end.date())[:7], "net_thousands": round(net),
                          "health_and_social_thousands": round(d(care)), "health_and_social_pct_of_net": round(100 * d(care) / net, 1),
                          "women_thousands": round(d(women)), "women_pct_of_net": round(100 * d(women) / net, 1),
                          "outside_health_and_social_thousands": round(net - d(care)),
                          "outside_health_social_education_state_local_thousands": round(net - d(care) - d(educ) - d(state) - d(local)),
                          "by_supersector_thousands": {k: round(d(v)) for k, v in sorted(sup.items(), key=lambda kv: -d(kv[1]))}}
    rec = {}
    for name, a, b in (("2001", "2001-03-01", "2001-11-01"), ("2008-10", "2007-12-01", "2010-02-01"), ("2020", "2020-02-01", "2020-04-01")):
        a, b = pd.Timestamp(a), pd.Timestamp(b)
        g = lambda s: round(100 * float(s[b] / s[a] - 1), 1)  # noqa: E731
        rec[name] = {"payrolls_pct": g(pay), "health_and_social_pct": g(care), "state_and_local_pct": g(state + local),
                     "women_pct": g(women), "men_pct": g(pay - women)}
    a, b = pd.Timestamp("2008-08-01"), pd.Timestamp("2013-02-01")
    austerity = {"window": "2008-08 to 2013-02", "state_and_local_thousands": round(float((state + local)[b] - (state + local)[a])),
                 "state_and_local_pct": round(100 * float((state + local)[b] / (state + local)[a] - 1), 1)}
    exp = {}
    for a, b in (("1991-03-01", "2001-03-01"), ("2001-11-01", "2007-12-01"), ("2010-02-01", "2020-02-01"), ("2020-04-01", str(end.date()))):
        a, b = pd.Timestamp(a), pd.Timestamp(b)
        exp[f"{str(a.date())[:7]} to {str(b.date())[:7]}"] = {"health_and_social_pct_of_net": round(100 * float((care[b] - care[a]) / (pay[b] - pay[a])), 1),
                                                              "health_and_social_share_at_start_pct": round(100 * float(care[a] / pay[a]), 1)}
    level = {"payrolls_thousands": round(float(pay[end])), "health_and_social_share_pct": round(100 * float(care[end] / pay[end]), 1),
             "women_share_pct": round(100 * float(women[end] / pay[end]), 1)}
    roll = pd.DataFrame({"net": pay.diff(12), "care": care.diff(12)}).dropna()
    return {"latest": str(end.date())[:7], "level": level, "windows": windows, "recessions": rec, "austerity_2008_13": austerity,
            "expansions": exp, "_roll": roll}


# ------------------------------------------------------------------ 1. by industry and sex, ILOSTAT
def lfs_panel() -> pd.DataFrame:
    rows = []
    for a in LFS:
        d = ex.ilo("EMP_TEMP_SEX_ECO_NB_A", a, tag="_all", t0=2008, sex=None)
        d = d[d.classif1.str.startswith("ECO_ISIC4_")].copy()
        d["sec"], d["a"] = d.classif1.str[10:], a
        rows.append(d)
    return pd.concat(rows).pivot_table(index=["a", "sex", "sec"], columns="time", values="obs_value")


def decompose(P: pd.DataFrame, areas, y0: int, y1: int) -> dict:
    T = sum(P.loc[(a, "SEX_T")].fillna(0) for a in areas)
    F = sum(P.loc[(a, "SEX_F")].fillna(0) for a in areas)
    ch = T[y1] - T[y0]
    net = float(ch["TOTAL"])
    grp = lambda secs: float(sum(ch.get(s, 0.0) for s in secs))  # noqa: E731
    lvl = lambda secs, y: float(sum(T[y].get(s, 0.0) for s in secs))  # noqa: E731
    top = ch.drop(index="TOTAL").dropna().sort_values(ascending=False)
    return {"window": f"{y0}-{y1}", "net_thousands": round(net),
            "women_pct_of_net": round(100 * float(F[y1]["TOTAL"] - F[y0]["TOTAL"]) / net, 1),
            "health_and_social_pct_of_net": round(100 * grp(("Q",)) / net, 1),
            "care_and_teaching_pct_of_net": round(100 * grp(CARE) / net, 1),
            "in_person_services_pct_of_net": round(100 * grp(IN_PERSON) / net, 1),
            "cognitive_services_pct_of_net": round(100 * grp(COGNITIVE) / net, 1),
            "manufacturing_thousands": round(grp(("C",))),
            "health_and_social_share_of_employment_pct": {y0: round(100 * lvl(("Q",), y0) / float(T[y0]["TOTAL"]), 1),
                                                          y1: round(100 * lvl(("Q",), y1) / float(T[y1]["TOTAL"]), 1)},
            "health_and_social_women_pct": round(100 * float(F[y1]["Q"] / T[y1]["Q"]), 1),
            "largest_gains": {k: round(float(v)) for k, v in top.head(3).items()},
            "largest_losses": {k: round(float(v)) for k, v in top.tail(2).items()}}


def china() -> dict:
    c = ex.ilo("EMP_2EMP_SEX_ECO_NB_A", "CHN", tag="_all", t0=2008, sex=None)
    c = c[c.sex == "SEX_T"].pivot_table(index="classif1", columns="time", values="obs_value")
    tot = c.loc["ECO_ISIC4_TOTAL"]
    return {"health_and_social_share_2025_pct": round(100 * float(c.loc["ECO_ISIC4_Q", 2025] / tot[2025]), 1),
            "education_share_2025_pct": round(100 * float(c.loc["ECO_ISIC4_P", 2025] / tot[2025]), 1),
            "net_2019_2025_thousands": round(float(tot[2025] - tot[2019])),
            "agriculture_2019_2025_thousands": round(float(c.loc["ECO_ISIC4_A", 2025] - c.loc["ECO_ISIC4_A", 2019])),
            "health_and_social_2019_2025_thousands": round(float(c.loc["ECO_ISIC4_Q", 2025] - c.loc["ECO_ISIC4_Q", 2019]))}


# ------------------------------------------------------------------ 3. Baumol's premise, US
def premise() -> dict:
    hc_n, pce, hc_p, g_p, pce_p = fred("DHLCRC1Q027SBEA"), fred("PCE"), fred("DHLCRG3Q086SBEA"), fred("DGDSRG3Q086SBEA"), fred("PCEPI")
    share = (hc_n / pce.resample("QS").mean()).dropna()
    rel_all = (hc_p / pce_p.resample("QS").mean()).dropna()
    rel_goods = (hc_p / g_p).dropna()
    yr = lambda s, y: float(s[s.index.year == y].mean())  # noqa: E731
    last = int(share.index[-1].year)
    table = {y: {"health_care_share_of_consumer_spending_pct": round(100 * yr(share, y), 2),
                 "price_vs_goods_1990_1": round(yr(rel_goods, y) / yr(rel_goods, 1990), 3),
                 "price_vs_all_consumer_prices_1990_1": round(yr(rel_all, y) / yr(rel_all, 1990), 3)} for y in (1990, 2000, 2008, 2019, last)}
    odds = np.log(share / (1 - share))
    lq = np.log(rel_all)
    impl = {}
    for a, b in ((1990, 2008), (2008, last), (1990, last)):
        dq, ds = yr(lq, b) - yr(lq, a), yr(odds, b) - yr(odds, a)
        impl[f"{a}-{b}"] = {"relative_price_log_points": round(100 * dq, 1), "share_odds_log_points": round(100 * ds, 1),
                            "implied_sigma": round(1 - ds / dq, 2) if abs(dq) > 0.02 else None}
    return {"by_year": table, "implied_sigma": impl, "_series": (share, rel_goods / yr(rel_goods, 1990), rel_all / yr(rel_all, 1990))}


# ------------------------------------------------------------------ 4-5. pay and who pays
def pay() -> dict:
    out = {}
    for a in LFS:
        d = ex.ilo("EAR_EMTA_SEX_ECO_NB_A", a, tag="_all", t0=2019, sex=None)
        d = d[(d.sex == "SEX_T")].dropna(subset=["obs_value"])
        if not (d.classif1 == "ECO_ISIC4_Q").any():
            continue
        y = int(d[d.classif1 == "ECO_ISIC4_Q"].time.max())
        x = d[d.time == y].set_index("classif1").obs_value
        out[a] = {"year": y, "health_and_social_vs_average": round(float(x["ECO_ISIC4_Q"] / x["ECO_ISIC4_TOTAL"]), 2),
                  "education_vs_average": round(float(x["ECO_ISIC4_P"] / x["ECO_ISIC4_TOTAL"]), 2) if "ECO_ISIC4_P" in x else None,
                  "finance_vs_average": round(float(x["ECO_ISIC4_K"] / x["ECO_ISIC4_TOTAL"]), 2) if "ECO_ISIC4_K" in x else None}
    r = (fred("CES6500000003") / fred("CES0500000003")).dropna()
    us = {y: round(float(r[r.index.year == y].mean()), 3) for y in (2007, 2010, 2015, 2019, 2023, int(r.index[-1].year))}
    return {"health_and_social_by_country": out, "us_education_and_health_vs_private_hourly": us, "_us_ratio": r}


def who_pays() -> dict:
    hc = fred("DHLCRC1Q027SBEA")
    med = fred("W824RC1Q027SBEA") + fred("W729RC1Q027SBEA")
    t = hc.index.intersection(med.index)[-1]
    public_emp = {}
    for a in ("USA", "FRA"):
        d = ex.ilo("EMP_TEMP_SEX_ECO_INS_NB_A", a, tag="_all", t0=2019, sex=None)
        d = d[(d.sex == "SEX_T") & d.classif1.isin(["ECO_ISIC4_Q", "ECO_ISIC4_P", "ECO_ISIC4_TOTAL"])].dropna(subset=["obs_value"])
        y = int(d.time.max())
        p = d[d.time == y].pivot_table(index="classif1", columns="classif2", values="obs_value")
        public_emp[a] = {"year": y, **{k[10:]: round(float(p.loc[k, "INS_SECTOR_PUB"] / p.loc[k, "INS_SECTOR_TOTAL"]), 2) for k in p.index}}
    return {"us_medicare_medicaid_vs_health_care_spending": round(float(med[t] / hc[t]), 2), "quarter": str(t.date())[:7],
            "public_employer_share": public_emp}


def main():
    us = us_payrolls()
    P = lfs_panel()
    lfs = {}
    for name, areas in [("US", ("USA",)), ("SE", ("SWE",)), ("EA5", ex.EA)] + [(a, (a,)) for a in ex.EA]:
        lfs[name] = {w: decompose(P, areas, y0, 2025) for w, y0 in (("2019-2025", 2019), ("2022-2025", 2022))}
    pr, py, wp = premise(), pay(), who_pays()
    out = {"us_payrolls": {k: v for k, v in us.items() if not k.startswith("_")}, "labour_force_surveys": lfs, "china": china(),
           "premise_us": {k: v for k, v in pr.items() if not k.startswith("_")}, "pay": {k: v for k, v in py.items() if not k.startswith("_")},
           "who_pays": wp}
    json.dump(out, open(os.path.join(ROOT, "results", "baumol.json"), "w", encoding="utf-8"), indent=1, default=str)
    print(json.dumps({k: out[k] for k in ("us_payrolls",)}, indent=1)[:4000])
    for n, v in lfs.items():
        for w, x in v.items():
            print(n, w, {k: x[k] for k in ("net_thousands", "women_pct_of_net", "health_and_social_pct_of_net", "care_and_teaching_pct_of_net",
                                           "in_person_services_pct_of_net", "cognitive_services_pct_of_net", "manufacturing_thousands")})
    print(json.dumps({k: out[k] for k in ("china", "premise_us", "pay", "who_pays")}, indent=1))
    figure(us, lfs, pr, py)


def figure(us, lfs, pr, py):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams["axes.titlesize"] = 10
    fig, ax = plt.subplots(2, 2, figsize=(14, 9), layout="constrained")
    fig.get_layout_engine().set(rect=(0, 0.03, 1, 0.97))
    r = us["_roll"].loc["2015-01-01":]
    a = ax[0, 0]
    a.plot(r.index, r["net"], color="k", lw=1.6, label="all payrolls")
    a.plot(r.index, r["care"], color="C3", lw=1.6, label="health care and social assistance")
    a.plot(r.index, r["net"] - r["care"], color="C0", lw=1.2, ls="--", label="everything else")
    a.axhline(0, color="grey", lw=0.8)
    a.set_ylim(-2500, 7000)
    a.set_title(f"US payrolls: change over 12 months, thousands (to {us['latest']};\n2020-21 off the scale)")
    a.legend(fontsize=8)
    a = ax[0, 1]
    names = ["US", "SE", "EA5", "DEU", "FRA", "ITA", "ESP", "NLD"]
    x = np.arange(len(names))
    w = lfs
    a.bar(x - 0.27, [w[n]["2022-2025"]["health_and_social_pct_of_net"] for n in names], 0.27, color="C3", label="health and social work")
    a.bar(x, [w[n]["2022-2025"]["care_and_teaching_pct_of_net"] for n in names], 0.27, color="C1", label="health, social work and education")
    a.bar(x + 0.27, [w[n]["2022-2025"]["women_pct_of_net"] for n in names], 0.27, color="C4", label="women")
    a.axhline(100, color="grey", lw=0.8, ls=":")
    a.set_xticks(x, names)
    a.set_title("Share of net employment growth 2022-2025, % (labour force surveys, ILOSTAT)")
    a.legend(fontsize=8)
    share, rg, ra = pr["_series"]
    a = ax[1, 0]
    a.plot(rg.index, rg, color="C3", label="health care price / goods prices (1990 = 1)")
    a.plot(ra.index, ra, color="C1", label="health care price / all consumer prices (1990 = 1)")
    a.set_xlim(pd.Timestamp("1990-01-01"), rg.index[-1])
    a.set_ylim(0.9, 2.1)
    b = a.twinx()
    b.plot(share.index, 100 * share, color="k", lw=1.2, ls="--", label="health care, % of consumer spending (right)")
    b.set_ylim(12, 18)
    a.set_title("Baumol's premise, US: the price that refuses to fall, and the spending share")
    h1, l1 = a.get_legend_handles_labels(); h2, l2 = b.get_legend_handles_labels()
    a.legend(h1 + h2, l1 + l2, fontsize=8, loc="upper left")
    a = ax[1, 1]
    c = py["health_and_social_by_country"]
    ks = list(c)
    a.bar(np.arange(len(ks)), [c[k]["health_and_social_vs_average"] for k in ks], color="C3")
    a.axhline(1, color="grey", lw=0.8)
    a.set_xticks(np.arange(len(ks)), [f"{k}\n{c[k]['year']}" for k in ks])
    a.set_ylim(0.6, 1.2)
    a.set_title("Pay in health and social work against the average (ILOSTAT monthly earnings)")
    fig.text(0.01, 0.005, "BLS payrolls and BEA consumer spending via FRED (PAYEMS, CES6562000001, DHLCRC1Q027SBEA, PCE, DHLCRG3Q086SBEA, "
             "DGDSRG3Q086SBEA, PCEPI); ILOSTAT employment and earnings by industry and sex. EA5: DEU, FRA, ITA, ESP, NLD.", fontsize=7)
    fig.savefig(os.path.join(ROOT, "figures", "fig_baumol.png"), dpi=120)


if __name__ == "__main__":
    main()
