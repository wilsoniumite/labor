# us_modes.py — does a second, public hiking cycle run the same sequence? US Treasuries, FRED.
#
# The curve-layer reading says a cycle moves the curve in phases: a hump while the market prices the
# moves (policy pinned), the front catching up as policy delivers, level-like moves once the curve is
# flat, and a front-heavy near-parallel move over the whole cycle. The timing share
#     tau = (f(1,2) - y(1M)) / (f(5,10) - y(1M))
# tracks how much of the gap to the long-run level is priced to close within one to two years.
# This script measures both on the Fed's 2021-23 cycle and on the last twelve months.
#
# Data: FRED constant-maturity Treasury yields (DGS1MO .. DGS30) and the effective federal funds rate
# (DFF), daily, cached in paths/cache. Constant-maturity yields are par yields; they stand in for zero
# rates here, which is adequate for the shape of a move (a few basis points at the long end).
#
# Run from paths/:  ../venv/Scripts/python.exe code/us_modes.py
# Out: results/us_modes.json, figures/fig_us_cycle_modes.png

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
sys.path.insert(0, os.path.join(os.path.dirname(ROOT), "pinning", "code"))
import curve as cv  # noqa: E402
import lambda_compute2 as _lc  # noqa: E402

_lc.CACHE = os.path.join(ROOT, "cache")          # this thread's own FRED cache
os.makedirs(_lc.CACHE, exist_ok=True)

TENORS = [("DGS1MO", 1 / 12), ("DGS3MO", 0.25), ("DGS6MO", 0.5), ("DGS1", 1), ("DGS2", 2), ("DGS3", 3),
          ("DGS5", 5), ("DGS7", 7), ("DGS10", 10), ("DGS20", 20), ("DGS30", 30)]
T = np.array([t for _, t in TENORS])
LABELS = ["1M", "3M", "6M", "1Y", "2Y", "3Y", "5Y", "7Y", "10Y", "20Y", "30Y"]
PHASES = [("A", "Pricing the hikes", "2021-09-01", "2022-02-15", "Sep 21 → Feb 22 (policy at 0)"),
          ("B", "First hikes delivered", "2022-03-16", "2022-12-14", "Mar 22 → Dec 22"),
          ("C", "Hikes to the peak", "2022-12-14", "2023-07-26", "Dec 22 → Jul 23"),
          ("ABC", "Whole hiking cycle", "2021-09-01", "2023-07-26", "Sep 21 → Jul 23"),
          ("D", "Holding at the peak", "2023-07-26", "2024-09-17", "Jul 23 → Sep 24"),
          ("E", "Cutting", "2024-09-17", "2025-12-10", "Sep 24 → Dec 25"),
          ("F", "This year", "2025-09-24", None, "Sep 25 → latest")]


def load() -> pd.DataFrame:
    cols = {}
    for sid, _ in TENORS + [("DFF", None)]:
        s = _lc.pull_fred(sid)
        if s is None:
            raise SystemExit(f"FRED pull failed: {sid}")
        cols[sid] = s
    df = pd.DataFrame(cols).dropna(subset=[sid for sid, _ in TENORS])
    return df[df.index >= "2019-01-01"]


def fwd(row, a, b):
    ya, yb = row[a], row[b]
    ta, tb = dict(TENORS)[a], dict(TENORS)[b]
    return (tb * yb - ta * ya) / (tb - ta)


def main() -> None:
    df = load()
    df["f1y1y"] = fwd(df, "DGS1", "DGS2")
    df["f5y5y"] = fwd(df, "DGS5", "DGS10")
    gap = df["f5y5y"] - df["DGS1MO"]
    df["tau"] = ((df["f1y1y"] - df["DGS1MO"]) / gap).where(gap.abs() >= 0.30)
    last = df.index.max()
    print(f"{len(df)} days, {df.index.min().date()} .. {last.date()}")

    sh = cv.sot_shapes(T)
    out = {"source": "FRED DGS1MO..DGS30, DFF; constant-maturity par yields as zero proxies",
           "latest": str(last.date()), "phases": []}
    for key, name, a, b, _ in PHASES:
        ra = df[df.index <= a].iloc[-1]
        rb = df[df.index <= (b or last)].iloc[-1]
        dz = np.array([(rb[s] - ra[s]) * 100 for s, _ in TENORS])
        r2 = {k: float(cv.fit_share(dz, sh[k][:, None])[1]) for k in ("parallel", "short", "steepener", "flattener")}
        best, best_r2, _ = cv.best_sot(dz, T)
        _, r2span = cv.fit_share(dz, np.column_stack([sh["S_short"], sh["S_long"]]))
        rec = {"key": key, "name": name, "from": str(ra.name.date()), "to": str(rb.name.date()),
               "dz_bp": dz.round(1).tolist(), "peak_tenor": LABELS[int(np.argmax(np.abs(dz)))],
               "best_sot": best, "best_r2": round(best_r2, 3), "parallel_r2": round(r2["parallel"], 3),
               "sot_span_r2": round(float(r2span), 3), "dff_change_bp": round((rb["DFF"] - ra["DFF"]) * 100, 1),
               "tau_from": None if pd.isna(ra["tau"]) else round(float(ra["tau"]), 3),
               "tau_to": None if pd.isna(rb["tau"]) else round(float(rb["tau"]), 3)}
        out["phases"].append(rec)
        print(f"\n{key} {name}: {rec['from']} -> {rec['to']}   fed funds {rec['dff_change_bp']:+.0f} bp")
        print("   " + "  ".join(f"{l} {v:+.0f}" for l, v in zip(LABELS, dz)))
        print(f"   largest move at {rec['peak_tenor']}; closest SOT shape {best} (R² {best_r2:.2f}); "
              f"parallel R² {r2['parallel']:.2f}; SOT-span R² {r2span:.2f}; tau {rec['tau_from']} -> {rec['tau_to']}")
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    with open(os.path.join(ROOT, "results", "us_modes.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
    figure(df, out)


def figure(df, out):
    S1, S2 = "#2a78d6", "#eb6834"
    INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9.5, "axes.edgecolor": GRID,
                         "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
                         "axes.titlesize": 10.5, "axes.titleweight": "bold", "axes.titlecolor": INK,
                         "axes.titlelocation": "left"})
    fig, ax = plt.subplots(2, 4, figsize=(15, 7.6), facecolor=SURF)
    for a in ax.flat:
        a.set_facecolor(SURF); a.grid(True, color=GRID, lw=0.8); a.set_axisbelow(True)
        for sp in ("top", "right"):
            a.spines[sp].set_visible(False)
    sub = {k: s for k, _, _, _, s in PHASES}
    for a, rec in zip(list(ax.flat)[:7], out["phases"]):
        dz = np.array(rec["dz_bp"])
        a.axhline(0, color=INK2, lw=0.8)
        a.plot(T, dz, color=S1, lw=2, marker="o", ms=4.5)
        a.set_xscale("log"); a.set_xticks([1 / 12, 1, 5, 30]); a.set_xticklabels(["1M", "1Y", "5Y", "30Y"])
        a.set_title(f"{rec['key']}. {rec['name']}\n{sub[rec['key']]}")
        label = rec["best_sot"].replace(" (not", "\n(not")
        a.text(0.98, 0.04, f"closest SOT shape: {label}\nfit R² {rec['best_r2']:.2f}", transform=a.transAxes,
               ha="right", va="bottom", fontsize=8.5, color=INK2)
        lo, hi = min(dz.min(), 0), max(dz.max(), 0); pad = 0.15 * (hi - lo)
        a.set_ylim(lo - pad * 2.2, hi + pad)
    ax[0, 0].set_ylabel("Change in Treasury yield, bp"); ax[1, 0].set_ylabel("Change in Treasury yield, bp")
    a = ax[1, 3]
    tv = df["tau"].clip(-0.5, 2.5)
    a.plot(tv.index, tv.values, color=S2, lw=1.4)
    a.axhline(1, color=INK2, lw=0.8, ls=":"); a.axhline(0, color=INK2, lw=0.8)
    a.set_title("Timing share: gap priced to close\nwithin 1–2 yrs (1 = fully)")
    a.xaxis.set_major_locator(mdates.YearLocator(2)); a.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    lastv = tv.dropna()
    a.annotate(f"{lastv.iloc[-1]:.2f} latest", (lastv.index[-1], lastv.iloc[-1]),
               (pd.Timestamp("2024-06-01"), 2.05), fontsize=8.5, color=INK, arrowprops=dict(arrowstyle="-", color=INK2, lw=0.8))
    fig.text(0.01, 0.005, "Source: FRED, constant-maturity Treasury yields DGS1MO–DGS30 (par yields as zero proxies). "
             "Timing share = (1y1y fwd − 1M) / (5y5y fwd − 1M), shown where |5y5y − 1M| ≥ 30 bp, clipped to [−0.5, 2.5]. "
             "SOT shapes: BCBS d368 §132.", fontsize=8, color=INK2)
    fig.tight_layout(rect=(0, 0.02, 1, 1))
    os.makedirs(os.path.join(ROOT, "figures"), exist_ok=True)
    p = os.path.join(ROOT, "figures", "fig_us_cycle_modes.png")
    fig.savefig(p, dpi=150, facecolor=SURF)
    print("\n" + p)


if __name__ == "__main__":
    main()
