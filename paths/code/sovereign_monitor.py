# sovereign_monitor.py — is the anchor failing now? Public sovereign spreads, 2019–2026, and Sweden 1994.
#
# Within the euro area a spread over Germany is as close to a pure sovereign spread as public data
# gets: one currency, one central bank, so the policy path is common and the gap is credit, fiscal
# and liquidity premium (France, the Netherlands, Finland). Over other currencies the gap also carries
# policy and currency (Sweden, the UK, the US) and is shown as such. For each: the level now, the
# change over three and twelve months, and whether the last year's widening sat at the long end
# (10Y widening more than 5Y: the slow-erosion signature of sovereign.py) or at the front (a crunch).
# Then Sweden 1994 at 5Y and 10Y: the term structure of the one anchor failure in the record.
#
# Data: the Riksbank's public SWEA API (government bond benchmarks), cached in cache/riksbank/.
# Run from paths/:  ../venv/Scripts/python.exe code/sovereign_monitor.py
# Out: results/sovereign_monitor.json, figures/fig_sovereign_monitor.png

from __future__ import annotations

import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from se_1990s import ERAS, fetch  # noqa: E402

EURO = {"France": ("FRGVB5Y", "FRGVB10Y"), "Netherlands": ("NLGVB5Y", "NLGVB10Y"), "Finland": (None, "FIGVB10Y")}
OTHER = {"Sweden": ("SEGVB5YC", "SEGVB10YC"), "UK": ("GBGVB5Y", "GBGVB10Y"), "US": ("USGVB5Y", "USGVB10Y")}
DE = ("DEGVB5Y", "DEGVB10Y")


def series(sid, era="now"):
    a, b = ERAS[era]
    return fetch(sid, a, b)


def on_or_before(s, d):
    return float(s.loc[:d].dropna().iloc[-1])


def stats(sp: pd.Series, last):
    return {"now_bp": round(on_or_before(sp, last), 0),
            "chg_3m_bp": round(on_or_before(sp, last) - on_or_before(sp, last - pd.DateOffset(months=3)), 0),
            "chg_12m_bp": round(on_or_before(sp, last) - on_or_before(sp, last - pd.DateOffset(months=12)), 0),
            "max_since_2019_bp": round(float(sp.max()), 0), "max_date": str(sp.idxmax().date())}


def main():
    de5, de10 = series(DE[0]), series(DE[1])
    last = de10.dropna().index.max()
    out = {"source": "Riksbank SWEA API (public), government bond benchmarks", "latest": str(last.date()), "spreads_over_germany": {}}
    frames = {}
    for group, table in (("euro", EURO), ("other", OTHER)):
        for name, (s5, s10) in table.items():
            rec = {"group": group}
            sp10 = ((series(s10) - de10) * 100).dropna()
            frames[name] = sp10
            rec["10Y"] = stats(sp10, last)
            if s5:
                sp5 = ((series(s5) - de5) * 100).dropna()
                rec["5Y"] = stats(sp5, last)
                rec["long_minus_short_widening_12m_bp"] = rec["10Y"]["chg_12m_bp"] - rec["5Y"]["chg_12m_bp"]
            out["spreads_over_germany"][name] = rec
    print(f"latest {last.date()} — spreads over Germany (bp): now / 3m change / 12m change")
    for name, rec in out["spreads_over_germany"].items():
        line = f"  {name:12s} [{rec['group']}]  10Y {rec['10Y']['now_bp']:+5.0f} / {rec['10Y']['chg_3m_bp']:+4.0f} / {rec['10Y']['chg_12m_bp']:+4.0f}"
        if "5Y" in rec:
            line += (f"   5Y {rec['5Y']['now_bp']:+5.0f} / {rec['5Y']['chg_3m_bp']:+4.0f} / {rec['5Y']['chg_12m_bp']:+4.0f}"
                     f"   10Y-5Y widening {rec['long_minus_short_widening_12m_bp']:+.0f}")
        line += f"   (max since 2019 {rec['10Y']['max_since_2019_bp']:+.0f} on {rec['10Y']['max_date']})"
        print(line)

    se5o, se10o, de5o, de10o = (series(s, "1990s") for s in ("SEGVB5YC", "SEGVB10YC", "DEGVB5Y", "DEGVB10Y"))
    s94_5 = ((se5o - de5o) * 100).dropna().loc["1993":"1995"]
    s94_10 = ((se10o - de10o) * 100).dropna().loc["1993":"1995"]
    a, b = pd.Timestamp("1994-01-31"), pd.Timestamp("1994-09-30")
    out["sweden_1994"] = {"5Y_from_to_bp": [round(on_or_before(s94_5, a)), round(on_or_before(s94_5, b))],
                          "10Y_from_to_bp": [round(on_or_before(s94_10, a)), round(on_or_before(s94_10, b))]}
    print("\nSweden over Germany, 31 Jan -> 30 Sep 1994: 5Y", out["sweden_1994"]["5Y_from_to_bp"], " 10Y", out["sweden_1994"]["10Y_from_to_bp"])
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, "results", "sovereign_monitor.json"), "w", encoding="utf-8"), indent=1)
    figure(frames, out, s94_5, s94_10)


def figure(frames, out, s94_5, s94_10):
    COUNTRY = {"France": "#2a78d6", "Netherlands": "#eb6834", "Finland": "#1baf7a",     # one colour per country,
               "Sweden": "#eda100", "UK": "#e87ba4", "US": "#008300"}                  # fixed across panels
    M5, M10 = "#aeada7", "#52514e"                                                    # maturities: light / dark
    INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9.5, "axes.edgecolor": GRID,
                         "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
                         "axes.titlesize": 10.5, "axes.titleweight": "bold", "axes.titlecolor": INK,
                         "axes.titlelocation": "left"})
    fig, ax = plt.subplots(2, 2, figsize=(13, 8.6), facecolor=SURF)
    for a in ax.flat:
        a.set_facecolor(SURF); a.grid(True, color=GRID, lw=0.8); a.set_axisbelow(True)
        for s in ("top", "right"):
            a.spines[s].set_visible(False)
    for a, names, title in ((ax[0, 0], ("France", "Netherlands", "Finland"),
                             "1. Euro-area spreads over Germany, 10Y\none currency, one central bank: the sovereign part"),
                            (ax[0, 1], ("Sweden", "UK", "US"),
                             "2. Other currencies over Germany, 10Y\nthese also carry policy and currency")):
        for n in names:
            c = COUNTRY[n]
            s = frames[n].rolling(5, min_periods=1).mean()
            a.plot(s.index, s.values, color=c, lw=1.6, label=n)
            a.annotate(f"{frames[n].iloc[-1]:+.0f}", (s.index[-1], s.iloc[-1]), (5, 0), textcoords="offset points",
                       fontsize=8.5, color=INK, va="center")
        a.axhline(0, color=INK2, lw=0.8)
        a.set_title(title); a.set_ylabel("bp (5-day mean)")
        a.xaxis.set_major_locator(mdates.YearLocator(2)); a.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
        a.legend(frameon=False, fontsize=8.5, labelcolor=INK, loc="upper left" if "France" in names else "lower left")
    a = ax[1, 0]
    rows = [(n, r) for n, r in out["spreads_over_germany"].items() if "5Y" in r]
    x = np.arange(len(rows)); w = 0.38
    v5 = [r["5Y"]["chg_12m_bp"] for _, r in rows]; v10 = [r["10Y"]["chg_12m_bp"] for _, r in rows]
    a.bar(x - w / 2 - 0.01, v5, w, color=M5, label="5Y", edgecolor=SURF, linewidth=1)
    a.bar(x + w / 2 + 0.01, v10, w, color=M10, label="10Y", edgecolor=SURF, linewidth=1)
    for xi, v in zip(x - w / 2, v5):
        a.text(xi, v, f"{v:+.0f}", ha="center", va="bottom" if v >= 0 else "top", fontsize=8.5, color=INK)
    for xi, v in zip(x + w / 2, v10):
        a.text(xi, v, f"{v:+.0f}", ha="center", va="bottom" if v >= 0 else "top", fontsize=8.5, color=INK)
    a.axhline(0, color=INK2, lw=0.8)
    a.set_xticks(x); a.set_xticklabels([n for n, _ in rows])
    a.set_title("3. Change over the last 12 months, over Germany\n10Y above 5Y: widening from the back (erosion)")
    a.set_ylabel("bp"); a.legend(frameon=False, fontsize=8.5, labelcolor=INK)
    a = ax[1, 1]
    for s, c, lab in ((s94_5, M5, "5Y"), (s94_10, M10, "10Y")):
        a.plot(s.index, s.values, color=c, lw=1.6, label=lab)
    a.axvspan(pd.Timestamp("1994-01-31"), pd.Timestamp("1994-09-30"), color=GRID, alpha=0.6, lw=0)
    a.set_title("4. Sweden over Germany, 1993–95\nthe 1994 crash (shaded), at 5Y and 10Y")
    a.set_ylabel("bp"); a.legend(frameon=False, fontsize=8.5, labelcolor=INK, loc="upper left")
    a.xaxis.set_major_locator(mdates.YearLocator(1)); a.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    fig.text(0.01, 0.005, "Source: Sveriges Riksbank, SWEA API (government bond benchmark yields). Spreads are yield differences "
             "over the German benchmark of the same maturity.", fontsize=8, color=INK2)
    fig.tight_layout(rect=(0, 0.02, 1, 1))
    p = os.path.join(ROOT, "figures", "fig_sovereign_monitor.png"); fig.savefig(p, dpi=150, facecolor=SURF); print(p)


if __name__ == "__main__":
    main()
