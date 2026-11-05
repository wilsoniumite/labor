# fig_compare.py — a candidate change against the base fit and the data (decision 13: she judges better or worse; Claude
# does not look at a variant's fit). The five targeted series and the capability clock, each panel with the data, the
# base model (dashed) and the variant, and both misfits.
# Run from us-record/:  python3 code/fig_compare.py fit_A      (reads results/fit_A.json; writes figures/fig_fit_A.png)

import json
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = sys.argv[1]
LABEL = sys.argv[2] if len(sys.argv) > 2 else NAME
B = json.load(open(os.path.join(ROOT, "results", "fit_base.json")))
V = json.load(open(os.path.join(ROOT, "results", f"{NAME}.json")))
YEARS = list(range(B["meta"]["years"][0], B["meta"]["years"][1] + 1))
MB, MV = pd.DataFrame(B["path"], index=YEARS), pd.DataFrame(V["path"], index=YEARS)
D = pd.read_csv(os.path.join(ROOT, "data", "panel.csv")).set_index("year").loc[YEARS]
S1, S2 = "#2a78d6", "#eb6834"                     # data, variant (categorical slots 1-2, validated); base: muted ink
SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
plt.rcParams.update({"font.size": 9, "axes.edgecolor": GRID, "xtick.color": INK2, "ytick.color": INK2,
                     "axes.titlecolor": INK, "axes.titlesize": 9.5, "axes.titleweight": "bold",
                     "figure.facecolor": SURFACE, "axes.facecolor": SURFACE})
BB, BV = B["best"]["by_series"], V["best"]["by_series"]


def frame(ax, title, note):
    ax.set_title(title, loc="left")
    ax.grid(True, color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.set_xlim(1948, 2027)
    ax.text(0.0, -0.15, note, transform=ax.transAxes, fontsize=7.5, color=INK2, va="top")


def three(ax, s, legend=False, loc="best"):
    ax.plot(D.index, D[s].values, color=S1, lw=1.8, label="data")
    ax.plot(MB.index, MB[s].values, color=INK2, lw=1.2, ls=(0, (4, 3)), label="base")
    ax.plot(MV.index, MV[s].values, color=S2, lw=1.8, label=LABEL)
    if legend:
        ax.legend(frameon=False, loc=loc, fontsize=8)


def note(s, extra=""):
    return f"{extra}Misfit: base {BB[s]:.1f}, {LABEL} {BV[s]:.1f} (1 = one tolerance)."


fig, axes = plt.subplots(2, 3, figsize=(12.5, 7.0))
ax = axes[0, 0]
three(ax, "wage_goods", legend=True, loc="upper left")
ax.set_yscale("log"); ax.set_yticks([100, 200, 400, 600]); ax.set_yticklabels(["100", "200", "400", "600"])
ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
frame(ax, "Real wage in durables, 1950 = 100 (log)", note("wage_goods"))
ax = axes[0, 1]
three(ax, "wage_shelter")
frame(ax, "Real wage in shelter, 1950 = 100", note("wage_shelter"))
ax = axes[0, 2]
three(ax, "labour_share_c")
frame(ax, "Labour's share of consumption", note("labour_share_c"))
ax = axes[1, 0]
three(ax, "prime_emp_rate")
frame(ax, "Prime-age employment rate", note("prime_emp_rate"))
ax = axes[1, 1]
tv = D["theta_V"].dropna()
ax.plot(tv.loc[:1992].index, tv.loc[:1992].values, color=S1, lw=0, marker="o", ms=5, markeredgecolor=SURFACE,
        markeredgewidth=1.5)
ax.plot(tv.loc[1997:].index, tv.loc[1997:].values, color=S1, lw=1.8)
ax.plot(MB.index, MB["theta_V"], color=INK2, lw=1.2, ls=(0, (4, 3)))
ax.plot(MV.index, MV["theta_V"], color=S2, lw=1.8)
frame(ax, "Labour's share of a machine's build cost", note("theta_V"))
ax = axes[1, 2]
ax.plot(YEARS, B["fitted_eta"], color=INK2, lw=1.2, ls=(0, (4, 3)), label="base clock")
ax.plot(YEARS, V["fitted_eta"], color=S2, lw=1.8, label=f"{LABEL} clock")
ax.set_yscale("log")
ax.legend(frameon=False, loc="lower left", fontsize=8)
frame(ax, "Machine service needed per task (1950 = 1, log)", f"The fitted clocks: base {B['best']['par']['g_eta']:.1%}, "
      f"{LABEL} {V['best']['par']['g_eta']:.1%} a year.")
fig.suptitle(f"{LABEL} against the base model and the US record, 1950–2024: misfit base {B['best']['misfit']:.1f}, "
             f"{LABEL} {V['best']['misfit']:.1f}", x=0.01, ha="left", fontsize=10.5, fontweight="bold", color=INK)
fig.tight_layout(h_pad=3.0, w_pad=2.0, rect=(0, 0, 1, 0.97))
os.makedirs(os.path.join(ROOT, "figures"), exist_ok=True)
out = os.path.join(ROOT, "figures", f"fig_{NAME}.png")
fig.savefig(out, dpi=150)
print(os.path.relpath(out, ROOT))
