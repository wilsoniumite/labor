# floor_margins.py — what Swedish banks did at the floor: lending margins and deposit rates, 2005-2026.
#
# The bank-side question: when the policy rate went below zero (Feb 2015 -> Dec 2019, down to -0.5%),
# deposit rates stuck at zero — did banks widen lending margins to make up for it, and by how much per
# point below zero? And the other open assumption: how fast do deposit rates follow the policy rate on
# the way up (2022-23) compared with the way down (2024-26)?
#
# Public data only. Statistics Sweden (SCB), MFI interest rate statistics (monthly): RantaT04N household
# mortgage rates by fixation (MFI, new and outstanding agreements); RantaT05 bank deposit rates
# (households and non-financial corporations; on-demand and all accounts); RantaT01N lending rates to
# non-financial corporations (banks, floating). Sveriges Riksbank SWEA API: the policy rate (SECBREPOEFF),
# STIBOR 3M (to 2020-07, when publication moved), mortgage-bond yields 2Y/5Y (SEMB2YCACOMB, SEMB5YCACOMB).
#
# Margins are measured over the monthly-average policy rate. The confound, stated: FI's mortgage
# risk-weight floors (15% in 2013, 25% in 2014) raised margins before rates went negative; so the clean
# contrast is -0.5% (2016-18) against about 0% (2020-21) under the same capital rules.
#
# Run from paths/:  ../venv/Scripts/python.exe code/floor_margins.py
# Out: results/floor_margins.json, figures/fig_floor_margins.png

from __future__ import annotations

import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import requests  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import se_1990s as rb  # noqa: E402  (the Riksbank SWEA fetcher, cached in cache/riksbank)

NL = chr(10)
SCB = "https://api.scb.se/OV0104/v1/doris/en/ssd/FM/FM5001/FM5001C/"
H = {"User-Agent": "Mozilla/5.0 (research; laborformal)"}
EPISODES = {"positive, 2012-14": ("2012-01", "2014-12"), "negative, 2016-18": ("2016-03", "2018-12"),
            "zero, 2020-21": ("2020-04", "2021-12"), "hikes, 2022-23": ("2022-04", "2023-12"), "cuts, 2024-26": ("2024-05", "2026-07")}


def scb(table: str, query: dict, name: str) -> pd.Series:
    """One SCB series (monthly), cached as JSON in cache/scb."""
    path = os.path.join(ROOT, "cache", "scb", f"{table}_{name}.json")
    if os.path.exists(path):
        js = json.load(open(path, encoding="utf-8"))
    else:
        body = {"query": [{"code": k, "selection": {"filter": "item", "values": [v]}} for k, v in query.items()],
                "response": {"format": "json"}}
        r = requests.post(SCB + table, json=body, timeout=60, headers=H)
        r.raise_for_status()
        js = r.json()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        json.dump(js, open(path, "w", encoding="utf-8"))
    rows = [(d["key"][-1], d["values"][0]) for d in js["data"]]
    s = pd.Series({pd.Period(k.replace("M", "-"), "M"): (float(v) if v not in ("..", "") else np.nan) for k, v in rows}, name=name)
    return s.sort_index()


def riksbank_monthly(sid: str) -> pd.Series:
    s = rb.fetch(sid, "2005-01-01", "2026-09-24")
    s.index = pd.to_datetime(s.index)
    return s.groupby(s.index.to_period("M")).mean().rename(sid)


def data() -> pd.DataFrame:
    mort = {"mortgage_float_new": ("0100", "1.1.1"), "mortgage_float_stock": ("0200", "1.1.1"),
            "mortgage_1_5y_new": ("0100", "1.1.2.2"), "mortgage_all_stock": ("0200", "1")}
    cols = [scb("RantaT04N", {"Referenssektor": "1.1", "Motpartssektor": "2c", "Avtal": a, "Rantebindningstid": f}, n)
            for n, (a, f) in mort.items()]
    dep = {"dep_hh_demand_stock": ("2", "0200", "3"), "dep_hh_all_stock": ("2", "0200", "1"), "dep_hh_all_new": ("2", "0100", "1"),
           "dep_nfc_demand_stock": ("1", "0200", "3"), "dep_nfc_all_stock": ("1", "0200", "1")}
    cols += [scb("RantaT05", {"Referenssektor": "1.1b", "Motpartssektor": c, "Avtal": a, "Rantebindningstid": f}, n)
             for n, (c, a, f) in dep.items()]
    cols.append(scb("RantaT01N", {"Referenssektor": "1.1.1", "Motpartssektor": "1", "Avtal": "0100", "Rantebindningstid": "1.1.1"}, "nfc_float_new"))
    df = pd.concat(cols, axis=1)
    for sid, name in (("SECBREPOEFF", "policy"), ("SEDP3MSTIBORDELAYC", "stibor3m"), ("SEMB2YCACOMB", "mb2y"), ("SEMB5YCACOMB", "mb5y")):
        df[name] = riksbank_monthly(sid)
    return df.loc["2005-09":"2026-07"]


def episode_table(df: pd.DataFrame) -> dict:
    out = {}
    for name, (a, b) in EPISODES.items():
        w = df.loc[a:b]
        out[name] = {"policy": round(float(w.policy.mean()), 2),
                     "mortgage_float_new_over_policy": round(float((w.mortgage_float_new - w.policy).mean()), 2),
                     "mortgage_float_stock_over_policy": round(float((w.mortgage_float_stock - w.policy).mean()), 2),
                     "mortgage_1_5y_new_over_mb2y": round(float((w.mortgage_1_5y_new - w.mb2y).mean()), 2),
                     "nfc_float_new_over_policy": round(float((w.nfc_float_new - w.policy).mean()), 2),
                     "dep_hh_demand": round(float(w.dep_hh_demand_stock.mean()), 2), "dep_hh_all": round(float(w.dep_hh_all_stock.mean()), 2),
                     "dep_nfc_demand": round(float(w.dep_nfc_demand_stock.mean()), 2),
                     "stibor_over_policy": round(float((w.stibor3m - w.policy).mean()), 2) if w.stibor3m.notna().any() else None}
    return out


def floor_compensation(df: pd.DataFrame) -> dict:
    """The mortgage margin at -0.5% (2016-18) against about 0% (2020-21), same capital rules; and a
    regression over 2015-2021 (one capital regime) of the floating margin on the policy rate's distance
    below zero, with the deposit rate floor as the reason."""
    neg, zero = df.loc["2016-03":"2018-12"], df.loc["2020-04":"2021-12"]
    dm = float((neg.mortgage_float_new - neg.policy).mean() - (zero.mortgage_float_new - zero.policy).mean())
    dp = float(neg.policy.mean() - zero.policy.mean())
    w = df.loc["2015-01":"2021-12"].dropna(subset=["mortgage_float_new", "policy"])
    x = np.maximum(-w.policy.values, 0.0)
    X = np.column_stack([np.ones(len(x)), x])
    y = (w.mortgage_float_new - w.policy).values
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ b
    se = float(np.sqrt(resid @ resid / (len(y) - 2) / ((x - x.mean()) @ (x - x.mean()))))
    ws = w.dropna(subset=["stibor3m"])
    xs = np.maximum(-ws.policy.values, 0.0)
    bs, *_ = np.linalg.lstsq(np.column_stack([np.ones(len(xs)), xs]), (ws.mortgage_float_new - ws.stibor3m).values, rcond=None)
    return {"contrast_margin_change_pp": round(dm, 2), "contrast_policy_change_pp": round(dp, 2),
            "contrast_per_point_below_zero": round(dm / -dp, 2),
            "regression_2015_2021_per_point_below_zero": round(float(b[1]), 2), "regression_se": round(se, 2),
            "regression_margin_at_zero": round(float(b[0]), 2),
            "over_stibor_per_point_below_zero": round(float(bs[1]), 2),
            "deposit_floor": {"hh_demand_min": round(float(neg.dep_hh_demand_stock.min()), 2),
                              "hh_all_min": round(float(neg.dep_hh_all_stock.min()), 2),
                              "nfc_demand_min": round(float(neg.dep_nfc_demand_stock.min()), 3)}}


def passthrough(df: pd.DataFrame, series: str, a: str, b: str) -> float:
    w = df.loc[a:b]
    return float((w[series].iloc[-1] - w[series].iloc[0]) / (w.policy.iloc[-1] - w.policy.iloc[0]))


def asymmetry(df: pd.DataFrame) -> dict:
    """Deposit pass-through on the way up (2022-03 -> 2023-12) and down (2024-04 -> 2026-07): change in
    the rate over change in the policy rate, market-wide."""
    out = {}
    for s in ("dep_hh_demand_stock", "dep_hh_all_stock", "dep_nfc_demand_stock", "dep_nfc_all_stock", "mortgage_float_new"):
        up, dn = passthrough(df, s, "2022-03", "2023-12"), passthrough(df, s, "2024-04", "2026-07")
        out[s] = {"up_2022_23": round(up, 2), "down_2024_26": round(dn, 2), "up_over_down": round(up / dn, 2) if dn else None}
    lag = {}
    for s in ("dep_hh_all_stock", "dep_hh_demand_stock"):
        up = df.loc["2022-03":"2023-12"]
        # months until half the up-move had passed through
        tgt = up[s].iloc[0] + 0.5 * (up[s].iloc[-1] - up[s].iloc[0])
        pol_half = up.policy.iloc[0] + 0.5 * (up.policy.iloc[-1] - up.policy.iloc[0])
        m_rate = int(np.argmax(up[s].values >= tgt))
        m_pol = int(np.argmax(up.policy.values >= pol_half))
        lag[s] = {"months_to_half_of_its_rise": m_rate, "policy_months_to_half": m_pol, "lag_months": m_rate - m_pol}
    out["lag_on_the_way_up"] = lag
    # the floating mortgage margin on the way up and down: change in (rate - policy) per point of policy
    mm = df.mortgage_float_new - df.policy
    per = lambda a, b: float((mm.loc[b] - mm.loc[a]) / (df.policy.loc[b] - df.policy.loc[a]))
    out["mortgage_margin_per_point"] = {"up_2021_12_to_2023_12": round(per("2021-12", "2023-12"), 3),
                                        "down_2024_04_to_2026_07": round(per("2024-04", "2026-07"), 3),
                                        "level_2021H2": round(float(mm.loc["2021-07":"2021-12"].mean()), 2),
                                        "level_2023H2": round(float(mm.loc["2023-07":"2023-12"].mean()), 2),
                                        "level_2026H1": round(float(mm.loc["2026-01":"2026-07"].mean()), 2)}
    return out


def main():
    df = data()
    out = {"sources": "SCB FM5001C RantaT04N/RantaT05/RantaT01N; Riksbank SWEA SECBREPOEFF, SEDP3MSTIBORDELAYC, SEMB2YCACOMB, SEMB5YCACOMB",
           "episodes": episode_table(df), "floor": floor_compensation(df), "asymmetry": asymmetry(df)}
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, "results", "floor_margins.json"), "w", encoding="utf-8"), indent=1)
    print(json.dumps(out, indent=1))
    figure(df, out)


def figure(df, out):
    INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9.5, "axes.edgecolor": GRID, "axes.labelcolor": INK2,
                         "xtick.color": INK2, "ytick.color": INK2, "axes.titlesize": 10.5, "axes.titleweight": "bold",
                         "axes.titlecolor": INK, "axes.titlelocation": "left"})
    fig, ax = plt.subplots(1, 3, figsize=(17, 5.4), facecolor=SURF, layout="constrained")
    for a in ax:
        a.set_facecolor(SURF); a.grid(True, color=GRID, lw=0.8); a.set_axisbelow(True)
        for sp in ("top", "right"):
            a.spines[sp].set_visible(False)
    t = df.index.to_timestamp()
    neg = (df.policy < 0).values
    for a in ax[:2]:
        a.fill_between(t, 0, 1, where=neg, transform=a.get_xaxis_transform(), color=GRID, alpha=0.6, lw=0)
    a = ax[0]
    a.plot(t, df.policy, color=INK, lw=2, label="policy rate")
    a.plot(t, df.mortgage_float_new, color="#e34948", lw=1.8, label="new floating mortgages (households)")
    a.plot(t, df.dep_hh_demand_stock, color="#2a78d6", lw=1.8, label="household on-demand deposits")
    a.plot(t, df.dep_nfc_demand_stock, color="#6da7ec", lw=1.4, label="corporate on-demand deposits")
    a.axhline(0, color=INK2, lw=0.8)
    a.set_title("1. Rates, 2005-2026" + NL + "Sweden, market-wide; shaded: policy below zero"); a.set_ylabel("%"); a.legend(frameon=False, fontsize=8)
    a = ax[1]
    a.plot(t, df.mortgage_float_new - df.policy, color="#e34948", lw=2, label="floating mortgage margin over policy")
    a.plot(t, df.mortgage_float_new - df.stibor3m, color="#e34948", lw=1.2, ls="--", label="over STIBOR 3M (to 2020)")
    a.plot(t, df.nfc_float_new - df.policy, color="#1baf7a", lw=1.6, label="corporate floating margin over policy")
    for yr, lab in ((2013.4, "risk-weight" + NL + "floor 15%"), (2014.7, "25%")):
        x = pd.Timestamp(f"{int(yr)}-{int((yr % 1) * 12) + 1:02d}-01")
        a.axvline(x, color=INK2, lw=0.8, ls=":"); a.text(x, 0.45, lab, fontsize=7.5, color=INK2)
    fl = out["floor"]
    a.set_title("2. Mortgage margins widened at the floor" + NL + f"+{fl['regression_2015_2021_per_point_below_zero']:.2f} pp per point below zero, 2015-21")
    a.set_ylabel("pp"); a.legend(frameon=False, fontsize=8, loc="lower left")
    a = ax[2]
    asy = out["asymmetry"]
    names = [("dep_hh_demand_stock", "households," + NL + "on demand"), ("dep_hh_all_stock", "households," + NL + "all"),
             ("dep_nfc_demand_stock", "corporates," + NL + "on demand"), ("dep_nfc_all_stock", "corporates," + NL + "all")]
    x = np.arange(len(names))
    a.bar(x - 0.18, [asy[k]["up_2022_23"] for k, _ in names], 0.36, color="#e34948", label="up, 2022-23")
    a.bar(x + 0.18, [asy[k]["down_2024_26"] for k, _ in names], 0.36, color="#2a78d6", label="down, 2024-26")
    a.set_xticks(x); a.set_xticklabels([n for _, n in names], fontsize=8.5)
    a.set_title("3. Deposit pass-through, up against down" + NL + "change in the rate / change in the policy rate (stocks)")
    a.legend(frameon=False, fontsize=8)
    fig.text(0.01, 0.005, "Sources: Statistics Sweden (MFI interest rate statistics, FM5001C), Sveriges Riksbank (SWEA API). Margins over the monthly-average policy rate.",
             fontsize=8, color=INK2)
    fig.get_layout_engine().set(rect=(0, 0.04, 1, 0.96))
    pth = os.path.join(ROOT, "figures", "fig_floor_margins.png"); fig.savefig(pth, dpi=150, facecolor=SURF); print(pth)


if __name__ == "__main__":
    main()
