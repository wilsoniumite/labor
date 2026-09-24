# se_1990s.py — an extreme in the record: Sweden 1990-95, against the curve layer and against today.
#
# Three kinds of extreme in one public record: the currency defence of September 1992 (the
# marginal rate to 500 percent), the float of 19 November 1992 and the collapse after it, and the
# fiscal bond crash of 1994. For each episode: the move by maturity, the closest supervisory (SOT)
# shape, the Sweden–Germany ten-year spread (the part of the long end that is not a common global
# rate), the krona. Then speed: daily moves in 1990-95 against 2021-26 on the same public series.
# Then which curve-layer pieces survive: can the one-speed curve with the policy rate observed
# describe the crisis days, and what drove the 1994 move — timing, or the destination?
#
# Data: the Riksbank's public SWEA API (no key) — marginal rate (to 1994-05) and repo/policy rate
# (from 1994-06), Treasury bills 1M/3M/6M/12M, government bonds 2/5/7/10Y, German 10Y, the TCW
# krona index. Bills are money-market yields and bonds par yields; both stand in for zero rates,
# which is adequate for the shape of a move. Cached in paths/cache/riksbank/.
#
# Run from paths/:  ../venv/Scripts/python.exe code/se_1990s.py
# Out: results/se_1990s.json, figures/fig_se_1990s.png

from __future__ import annotations

import json
import os
import sys
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import requests  # noqa: E402
from scipy.optimize import least_squares  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import curve as cv  # noqa: E402

CACHE = os.path.join(ROOT, "cache", "riksbank")
API = "https://api.riksbank.se/swea/v1/Observations/{sid}/{a}/{b}"
ERAS = {"1990s": ("1989-01-01", "1996-12-31"), "now": ("2019-01-01", "2026-09-24")}
TENORS = [("SETB1MBENCHC", 1 / 12, "1M"), ("SETB3MBENCH", 0.25, "3M"), ("SETB6MBENCH", 0.5, "6M"),
          ("SETB12MBENCH", 1.0, "12M"), ("SEGVB2YC", 2.0, "2Y"), ("SEGVB5YC", 5.0, "5Y"),
          ("SEGVB7YC", 7.0, "7Y"), ("SEGVB10YC", 10.0, "10Y")]
OTHER = ["SECBMARGEFF", "SECBREPOEFF", "DEGVB10Y", "SEKTCW92"]
EPISODES = [("E1", "Defending the krona", "1992-09-08", "1992-09-18", "8 → 18 Sep 1992: marginal rate 16 → 500%"),
            ("E2", "The retreat", "1992-09-18", "1992-10-30", "18 Sep → 30 Oct 1992"),
            ("E3", "The float", "1992-11-13", "1992-12-30", "13 Nov → 30 Dec 1992 (float 19 Nov)"),
            ("E4", "Collapse after the float", "1992-12-30", "1993-12-30", "30 Dec 1992 → 30 Dec 1993"),
            ("E5", "The fiscal bond crash", "1994-01-31", "1994-09-30", "31 Jan → 30 Sep 1994"),
            ("ALL", "Before the crisis to after the crash", "1992-06-30", "1995-06-30", "30 Jun 1992 → 30 Jun 1995")]


def fetch(sid: str, a: str, b: str) -> pd.Series:
    os.makedirs(CACHE, exist_ok=True)
    fp = os.path.join(CACHE, f"{sid}_{a}_{b}.json")
    if not os.path.exists(fp):
        for wait in (0, 20, 60, 120):
            if wait:
                time.sleep(wait)
            r = requests.get(API.format(sid=sid, a=a, b=b), timeout=60)
            if r.status_code in (200, 204):                  # 204: no observations in the window
                open(fp, "w", encoding="utf-8").write(r.text if r.status_code == 200 else "[]")
                break
            if r.status_code not in (429, 503):
                raise SystemExit(f"Riksbank API {sid}: HTTP {r.status_code}")
        else:
            raise SystemExit(f"Riksbank API {sid}: gave up after retries")
        time.sleep(6)                                     # courtesy spacing between live calls
    obs = [o for o in json.load(open(fp, encoding="utf-8")) if o.get("value") is not None]
    return pd.Series([float(o["value"]) for o in obs], index=pd.DatetimeIndex([o["date"] for o in obs]), name=sid,
                     dtype=float)


def panel(era: str) -> pd.DataFrame:
    a, b = ERAS[era]
    cols = {sid: fetch(sid, a, b) for sid, _, _ in TENORS}
    for sid in OTHER:
        s = fetch(sid, a, b)
        if len(s):
            cols[sid] = s
    df = pd.DataFrame(cols)
    df.index = pd.DatetimeIndex(df.index)
    df = df.sort_index()
    pol = df.get("SECBMARGEFF", pd.Series(dtype=float)).combine_first(df.get("SECBREPOEFF", pd.Series(dtype=float)))
    df["policy"] = pol.ffill()
    return df


def fwd(df, a, b, ta, tb):
    return (tb * df[b] - ta * df[a]) / (tb - ta)


def episode_table(df):
    Tg = np.array([t for _, t, _ in TENORS])
    rows = []
    for key, name, a, b, sub in EPISODES:
        ra = df.loc[:a].dropna(subset=[s for s, _, _ in TENORS]).iloc[-1]
        rb = df.loc[:b].dropna(subset=[s for s, _, _ in TENORS]).iloc[-1]
        dz = np.array([(rb[s] - ra[s]) * 100 for s, _, _ in TENORS])
        label, r2, _ = cv.best_sot(dz, Tg)
        sh = cv.sot_shapes(Tg)
        _, r2span = cv.fit_share(dz, np.column_stack([sh["S_short"], sh["S_long"]]))
        win = df.loc[a:b]
        d1 = win["SETB1MBENCHC"].diff().abs().max() * 100
        d10 = win["SEGVB10YC"].diff().abs().max() * 100
        spread = lambda r: (r["SEGVB10YC"] - r["DEGVB10Y"]) * 100  # noqa: E731
        rows.append({"key": key, "name": name, "sub": sub, "from": str(ra.name.date()), "to": str(rb.name.date()),
                     "policy_from": float(ra["policy"]), "policy_to": float(rb["policy"]),
                     "dz_bp": dz.round(1).tolist(), "closest_sot": label, "closest_r2": round(r2, 3),
                     "sot_span_r2": round(float(r2span), 3),
                     "spread_de10_from_bp": round(float(spread(ra)), 0), "spread_de10_to_bp": round(float(spread(rb)), 0),
                     "tcw_change_pct": round(float((rb["SEKTCW92"] / ra["SEKTCW92"] - 1) * 100), 1) if "SEKTCW92" in df else None,
                     "max_daily_1m_bp": round(float(d1), 0), "max_daily_10y_bp": round(float(d10), 0)})
    return rows


def speed(df, era):
    out = {}
    for sid, lab in (("SETB3MBENCH", "3M"), ("SEGVB2YC", "2Y"), ("SEGVB10YC", "10Y")):
        d = df[sid].dropna().diff().dropna() * 100
        out[lab] = {"p99_abs_bp": round(float(d.abs().quantile(0.99)), 1), "max_abs_bp": round(float(d.abs().max()), 0),
                    "max_monthly_vol_bp": round(float(d.groupby(d.index.to_period("M")).std().max() * np.sqrt(252)), 0)}
    return out


def one_speed_fit(row):
    """Fit rbar and k of the one-speed curve with the front observed (r0 := 1M bill); RMSE in bp."""
    t = np.array([t for _, t, _ in TENORS]); y = np.array([row[s] for s, _, _ in TENORS]); r0 = y[0]
    res = least_squares(lambda p: cv.zero(t, cv.CurveState.one_speed(r0, p[0], p[1])) - y, x0=[y[-1], 1.0],
                        bounds=([-5, 0.02], [60, 60]))
    return res.x, float(np.sqrt(np.mean(res.fun ** 2)) * 100)


def cascade_fit(row):
    """Fit the two-stage cascade with r0 free too (the 1M bill is itself a one-month average); RMSE in bp."""
    t = np.array([t for _, t, _ in TENORS]); y = np.array([row[s] for s, _, _ in TENORS])
    best = None
    for r00 in (y[0], 3 * y[0], 300.0, 500.0):
        for k10 in (5.0, 20.0, 60.0):
            f = lambda p: cv.zero(t, cv.CurveState(r0=p[0], m0=p[1], rbar=p[2], k1=np.exp(p[3]), k2=np.exp(p[4]))) - y  # noqa: E731
            r = least_squares(f, x0=[r00, y[2], y[-1], np.log(k10), np.log(0.5)],
                              bounds=([0, -5, -5, np.log(0.02), np.log(0.01)], [1000, 100, 40, np.log(500), np.log(20)]))
            if best is None or r.cost < best.cost:
                best = r
    q = best.x
    return {"r0": round(float(q[0]), 1), "m0": round(float(q[1]), 2), "rbar": round(float(q[2]), 2),
            "k1": round(float(np.exp(q[3])), 2), "k2": round(float(np.exp(q[4])), 2),
            "rmse_bp": round(float(np.sqrt(np.mean(best.fun ** 2)) * 100), 1),
            "at_bound": bool(q[1] <= -4.99 or q[2] >= 39.9 or np.exp(q[4]) <= 0.0101)}


def main():
    old, new = panel("1990s"), panel("now")
    full = old.dropna(subset=[s for s, _, _ in TENORS])
    print(f"1990s panel: {len(full)} days with the full curve, {full.index.min().date()} .. {full.index.max().date()}")
    rows = episode_table(old)
    labels = [l for _, _, l in TENORS]
    for r in rows:
        print(f"\n{r['key']} {r['name']}: {r['from']} -> {r['to']}   policy {r['policy_from']:g} -> {r['policy_to']:g}%")
        print("   " + "  ".join(f"{l} {v:+.0f}" for l, v in zip(labels, r["dz_bp"])))
        print(f"   closest SOT {r['closest_sot']} (R² {r['closest_r2']:.2f}); SOT span R² {r['sot_span_r2']:.2f}; "
              f"SE-DE 10Y spread {r['spread_de10_from_bp']:+.0f} -> {r['spread_de10_to_bp']:+.0f} bp; krona TCW {r['tcw_change_pct']}%; "
              f"largest day: 1M {r['max_daily_1m_bp']:.0f} bp, 10Y {r['max_daily_10y_bp']:.0f} bp")

    sp = {"1990-95": speed(old.loc["1990":"1995"], "1990s"), "2021-26": speed(new.loc["2021":], "now")}
    print("\n== speed: daily moves, government bills and bonds (bp)")
    for era, d in sp.items():
        print("   " + era + "  " + "  ".join(f"{k}: p99 {v['p99_abs_bp']}, max {v['max_abs_bp']:.0f}, worst month vol {v['max_monthly_vol_bp']:.0f}" for k, v in d.items()))

    fits = {}
    calm = [one_speed_fit(r)[1] for _, r in full.loc["1991-01":"1992-06"].iterrows()]
    fits["calm_1991_92_median_rmse_bp"] = round(float(np.median(calm)), 1)
    for d in ("1992-09-17", "1992-09-18", "1992-11-19", "1994-09-30"):
        row = full.loc[:d].iloc[-1]
        (rb, k), rmse = one_speed_fit(row)
        fits[str(row.name.date())] = {"r0_1m": float(row["SETB1MBENCHC"]), "rbar": round(float(rb), 2), "k": round(float(k), 2),
                                      "rmse_bp": round(rmse, 1), "curve": [float(row[s]) for s, _, _ in TENORS],
                                      "cascade": cascade_fit(row)}
    print("\n== can the one-speed curve (front observed) describe it?  median RMSE on calm days 1991-92:",
          fits["calm_1991_92_median_rmse_bp"], "bp")
    for k, v in fits.items():
        if isinstance(v, dict):
            c = v["cascade"]
            print(f"   {k}: curve {v['curve']}")
            print(f"      one speed: rbar {v['rbar']}, k {v['k']}/yr, RMSE {v['rmse_bp']} bp")
            print(f"      two-stage: r0 {c['r0']}, m0 {c['m0']}, rbar {c['rbar']}, k1 {c['k1']}, k2 {c['k2']}, "
                  f"RMSE {c['rmse_bp']} bp" + ("  (a parameter at its bound)" if c["at_bound"] else ""))

    out = {"source": "Riksbank SWEA API (public): SECBMARGEFF, SECBREPOEFF, SETB*, SEGVB*, DEGVB10Y, SEKTCW92",
           "episodes": rows, "speed": sp, "one_speed_fits": fits}
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, "results", "se_1990s.json"), "w", encoding="utf-8"), indent=1)
    figure(old, rows, sp)


def figure(df, rows, sp):
    S1, S2, S3 = "#2a78d6", "#eb6834", "#1baf7a"
    INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9.5, "axes.edgecolor": GRID,
                         "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
                         "axes.titlesize": 10.5, "axes.titleweight": "bold", "axes.titlecolor": INK,
                         "axes.titlelocation": "left"})
    fig, ax = plt.subplots(2, 4, figsize=(15.5, 7.8), facecolor=SURF)
    for a in ax.flat:
        a.set_facecolor(SURF); a.grid(True, color=GRID, lw=0.8); a.set_axisbelow(True)
        for s in ("top", "right"):
            a.spines[s].set_visible(False)
    Tg = np.array([t for _, t, _ in TENORS])
    for a, r in zip(list(ax.flat)[:6], rows):
        dz = np.array(r["dz_bp"])
        a.axhline(0, color=INK2, lw=0.8)
        a.plot(Tg, dz, color=S1, lw=2, marker="o", ms=4.5)
        a.set_xscale("log"); a.set_xticks([1 / 12, 1, 2, 5, 10]); a.set_xticklabels(["1M", "1Y", "2Y", "5Y", "10Y"])
        a.set_title(f"{r['key']}. {r['name']}\n{r['sub']}")
        lab = r["closest_sot"].replace(" (not", "\n(not")
        a.text(0.98, 0.04, f"closest SOT shape: {lab}\nfit R² {r['closest_r2']:.2f}\n"
               f"SE–DE 10Y spread {r['spread_de10_from_bp']:+.0f} → {r['spread_de10_to_bp']:+.0f} bp",
               transform=a.transAxes, ha="right", va="bottom", fontsize=8.2, color=INK2)
        lo, hi = min(dz.min(), 0), max(dz.max(), 0); pad = 0.15 * (hi - lo)
        a.set_ylim(lo - pad * 3.2, hi + pad)
    ax[0, 0].set_ylabel("Change in yield, bp"); ax[1, 0].set_ylabel("Change in yield, bp")
    a = ax[1, 2]
    w = df.loc["1990":"1995"]
    a.plot(w.index, w["SETB1MBENCHC"], color=S1, lw=1.4, label="1M Treasury bill")
    a.plot(w.index, w["SEGVB10YC"], color=S2, lw=1.4, label="10Y government bond")
    a.plot(w.index, w["DEGVB10Y"], color=S3, lw=1.4, label="German 10Y")
    a.set_ylim(0, 30); a.set_ylabel("%")
    pk = w["SETB1MBENCHC"].idxmax()
    peak_note = f"1M bill peak {w['SETB1MBENCHC'].max():.0f}% ({pk:%d %b %Y})" + "\n" + "marginal rate 500%"
    a.text(pd.Timestamp("1993-03-01"), 28.8, peak_note, fontsize=8, color=INK, va="top")
    a.set_title("Levels, 1990–95 (1M clipped at 30%)")
    a.legend(frameon=False, fontsize=8.5, loc="lower left", labelcolor=INK)
    a.xaxis.set_major_locator(mdates.YearLocator(1)); a.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    a = ax[1, 3]
    labs = list(sp["1990-95"].keys()); x = np.arange(len(labs)); wdt = 0.38
    v90 = [sp["1990-95"][k]["p99_abs_bp"] for k in labs]; vnow = [sp["2021-26"][k]["p99_abs_bp"] for k in labs]
    a.bar(x - wdt / 2 - 0.01, v90, wdt, color=S1, label="1990–95", edgecolor=SURF, linewidth=1)
    a.bar(x + wdt / 2 + 0.01, vnow, wdt, color=S2, label="2021–26", edgecolor=SURF, linewidth=1)
    for xi, v in zip(x, v90):
        a.text(xi - wdt / 2, v, f"{v:.0f}", ha="center", va="bottom", fontsize=8.5, color=INK)
    for xi, v in zip(x, vnow):
        a.text(xi + wdt / 2, v, f"{v:.0f}", ha="center", va="bottom", fontsize=8.5, color=INK)
    a.set_xticks(x); a.set_xticklabels(labs); a.set_ylabel("bp")
    a.set_title("Speed: 99th pct of daily moves")
    a.legend(frameon=False, fontsize=8.5, labelcolor=INK)
    fig.text(0.01, 0.005, "Source: Sveriges Riksbank, SWEA API (Treasury bills, government bonds, marginal/policy rate, German 10Y). "
             "Bills and bonds stand in for zero rates. SOT shapes: BCBS d368 §132.", fontsize=8, color=INK2)
    fig.tight_layout(rect=(0, 0.02, 1, 1))
    os.makedirs(os.path.join(ROOT, "figures"), exist_ok=True)
    p = os.path.join(ROOT, "figures", "fig_se_1990s.png"); fig.savefig(p, dpi=150, facecolor=SURF); print("\n" + p)


if __name__ == "__main__":
    main()
