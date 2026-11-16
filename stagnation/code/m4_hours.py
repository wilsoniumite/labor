# m4_hours.py — M4 of docs/spec.md: the hours that did not fall. Penn World Table 11.0 (cache/pwt/pwt110.xlsx):
# average annual hours worked per person engaged (avh), U.S. against Germany, France, the U.K., the Netherlands and
# Sweden, 1950 to 2023. One mapping, labeled an unattributed envelope: the level of U.S. output per hour that Lemma 1's
# elasticity (technology, land and basket fixed) implies had U.S. hours per worker since 1980 followed (a) their own
# 1950-80 trend or (b) the average path of the five European countries, with employment as it was. Elasticity from
# the instance (-0.59) and the range [-1, -0.4]. Writes data/m4_hours.json, draws Figure 6
# (paper/figures/fig_hours.pdf, .png).
# Run from stagnation/:  ../venv/bin/python code/m4_hours.py
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
import model as M  # noqa: E402
import eras  # noqa: E402

EUROPE = ("DEU", "FRA", "GBR", "NLD", "SWE")
NAMES = {"USA": "United States", "DEU": "Germany", "FRA": "France", "GBR": "United Kingdom", "NLD": "Netherlands",
         "SWE": "Sweden"}
ELASTICITIES = (-1.0, M.numbers()["eps_base"], -0.4)


def load():
    pwt = pd.read_excel(ROOT / "cache" / "pwt" / "pwt110.xlsx", sheet_name="Data")
    return pwt.pivot_table(index="year", columns="countrycode", values="avh")[["USA", *EUROPE]]


def envelope(h, y0=1950, y1=1980, yend=None):
    yend = yend or int(h.USA.dropna().index.max())
    us = h.USA
    g_us = (np.log(us[y1]) - np.log(us[y0])) / (y1 - y0)
    trend = us[y1] * np.exp(g_us * (yend - y1))                                   # (a) the U.S. 1950-80 trend
    eu = np.exp(np.log(h[list(EUROPE)]).mean(axis=1))                             # geometric mean of the five
    europe_path = us[y1] * eu[yend] / eu[y1]                                      # (b) the European path since 1980
    out = dict(year_end=yend, us_1950=us[y0], us_1980=us[y1], us_end=us[yend],
               us_rate_1950_1980=100 * g_us, us_rate_1980_end=100 * (np.log(us[yend]) - np.log(us[y1])) / (yend - y1),
               eu_rate_1950_1980=100 * (np.log(eu[y1]) - np.log(eu[y0])) / (y1 - y0),
               eu_rate_1980_end=100 * (np.log(eu[yend]) - np.log(eu[y1])) / (yend - y1),
               eu_1980=eu[y1], eu_end=eu[yend], cf_trend=trend, cf_europe=europe_path)
    for tag, cf in (("trend", trend), ("europe", europe_path)):
        dlogh = np.log(cf) - np.log(us[yend])                                         # hours lower by this (< 0)
        out[f"hours_gap_pct_{tag}"] = 100 * (1 - cf / us[yend])
        for name, eps in zip(("lo", "mid", "hi"), ELASTICITIES):
            dpi = eps * dlogh                                                         # log change in output per hour
            out[f"pi_level_pct_{tag}_{name}"] = 100 * (np.exp(dpi) - 1)
            out[f"pi_growth_pp_{tag}_{name}"] = 100 * dpi / (yend - y1)               # per year, over 1980-end
    a = eras.annual()
    g = lambda y0_, y1_: 100 * (np.log(a[y1_]) - np.log(a[y0_])) / (y1_ - y0_)  # noqa: E731
    out["ophnfb_rate_1948_1973"], out["ophnfb_rate_1980_end"] = g(1948, 1973), g(y1, yend)
    out["slowdown_1980_end"] = out["ophnfb_rate_1948_1973"] - out["ophnfb_rate_1980_end"]
    for tag in ("trend", "europe"):
        for name in ("lo", "mid", "hi"):
            out[f"envelope_share_{tag}_{name}"] = out[f"pi_growth_pp_{tag}_{name}"] / out["slowdown_1980_end"]
    # the share depends on the windows set against each other (a sensitivity, added after the data were seen):
    # against output per hour in 1950-80, the hours trend's own window; and with hours and output per hour both
    # broken at 1973 (hours 1950-73 against 1973-end, output per hour 1948-73 against 1973-end)
    out["ophnfb_rate_1950_1980"] = g(y0, y1)
    out["envelope_share_matched_1950_1980"] = out["pi_growth_pp_trend_mid"] / (g(y0, y1) - g(y1, yend))
    h73 = 100 * ((np.log(us[yend]) - np.log(us[1973])) / (yend - 1973) - (np.log(us[1973]) - np.log(us[y0])) / (1973 - y0))
    out["envelope_pp_break_1973"] = -ELASTICITIES[1] * h73        # hours fell more slowly after 1973: h73 > 0
    out["envelope_share_break_1973"] = out["envelope_pp_break_1973"] / (g(1948, 1973) - g(1973, yend))
    return out, eu


rcParams.update({"font.family": "serif", "font.serif": ["DejaVu Serif"], "mathtext.fontset": "dejavuserif",
                 "pdf.fonttype": 42, "font.size": 8.5, "xtick.labelsize": 7.5, "ytick.labelsize": 7.5,
                 "axes.linewidth": 0.53, "xtick.major.width": 0.45, "ytick.major.width": 0.45,
                 "xtick.major.size": 2.3, "ytick.major.size": 2.3})
PRINT_W = 0.88 * 16 / 2.54
BLUE, GREY, INK, MUTED, GRID = "#2a78d6", "#a9a8a2", "#0b0b0b", "#52514e", "#e4e3df"


def draw(h, out):
    fig, ax = plt.subplots(figsize=(PRINT_W, PRINT_W / 2.0), layout="constrained")
    yend = out["year_end"]
    for c in EUROPE:                       # context lines, one shared label (the caption names the five)
        s = h[c].dropna()
        ax.plot(s.index, s, color=GREY, lw=1.0, zorder=2)
    mid = float(np.exp(np.log(h[list(EUROPE)].loc[yend]).mean()))
    ax.annotate("Five European\ncountries", xy=(yend + 0.6, mid), ha="left", va="center", fontsize=6.5,
                color=MUTED)
    s = h.USA.dropna()
    ax.plot(s.index, s, color=BLUE, lw=1.8, zorder=3)
    ax.annotate(NAMES["USA"], xy=(s.index[-1] + 0.6, s.iloc[-1]), ha="left", va="center", fontsize=6.8, color=INK)
    yrs = np.arange(1980, yend + 1)
    g = out["us_rate_1950_1980"] / 100
    ax.plot(yrs, out["us_1980"] * np.exp(g * (yrs - 1980)), color=BLUE, lw=0.8, alpha=0.6, zorder=2)
    ax.annotate("U.S. 1950–80 trend", xy=(yend + 0.6, out["cf_trend"]), ha="left", va="center", fontsize=6.5,
                color=MUTED)
    ax.set_xlim(1950, yend + 16)
    ax.set_xticks([1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020])
    ax.spines["bottom"].set_bounds(1950, yend)
    ax.set_ylabel("Average annual hours\nper person engaged", fontsize=7.5)
    ax.grid(True, color=GRID, lw=0.5)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(colors=MUTED, labelcolor=INK)
    path = ROOT / "paper" / "figures" / "fig_hours.png"
    fig.savefig(path, dpi=300)
    fig.savefig(path.with_suffix(".pdf"), metadata={"CreationDate": None})
    return path


if __name__ == "__main__":
    h = load()
    out, eu = envelope(h)
    (ROOT / "data" / "m4_hours.json").write_text(json.dumps(out, indent=2, default=float))
    for k, v in out.items():
        print(f"  {k:30s} {v:.3f}" if isinstance(v, float) else f"  {k:30s} {v}")
    print("wrote", draw(h, out))
