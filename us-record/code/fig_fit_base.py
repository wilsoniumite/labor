# fig_fit_base.py — Phase 2's base fit against the data (for breakpoint B): the five targeted series, data and model,
# and the capability clock (the fitted smooth clock against the year-by-year accounting of the fork).
# Reads results/fit_base.json and data/panel.csv; writes figures/fig_fit_base.png.
# Run from us-record/:  python3 code/fig_fit_base.py

import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = json.load(open(os.path.join(ROOT, "results", "fit_base.json")))
YEARS = list(range(R["meta"]["years"][0], R["meta"]["years"][1] + 1))
M = pd.DataFrame(R["path"], index=YEARS)
D = pd.read_csv(os.path.join(ROOT, "data", "panel.csv")).set_index("year").loc[YEARS]
S1, S2 = "#2a78d6", "#eb6834"                     # data, model (categorical slots 1-2, validated on the light surface)
SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
plt.rcParams.update({"font.size": 9, "axes.edgecolor": GRID, "xtick.color": INK2, "ytick.color": INK2,
                     "axes.titlecolor": INK, "axes.titlesize": 9.5, "axes.titleweight": "bold",
                     "figure.facecolor": SURFACE, "axes.facecolor": SURFACE})
BY = R["best"]["by_series"]


def frame(ax, title, note):
    ax.set_title(title, loc="left")
    ax.grid(True, color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.set_xlim(1948, 2027)
    ax.text(0.0, -0.15, note, transform=ax.transAxes, fontsize=7.5, color=INK2, va="top")


def pair(ax, data, model, legend=True):
    ax.plot(data.index, data.values, color=S1, lw=1.8, label="data")
    ax.plot(model.index, model.values, color=S2, lw=1.8, label="base model")
    if legend:
        ax.legend(frameon=False, loc="best", fontsize=8)


fig, axes = plt.subplots(2, 3, figsize=(12.5, 7.0))
ax = axes[0, 0]
pair(ax, D["wage_goods"], M["wage_goods"])
ax.set_yscale("log"); ax.set_yticks([100, 200, 400, 600]); ax.set_yticklabels(["100", "200", "400", "600"])
ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
frame(ax, "Real wage in durables, 1950 = 100 (log)", f"Targeted. Misfit {BY['wage_goods']:.1f} (1 = one tolerance, "
      "0.05 log points).")
ax = axes[0, 1]
pair(ax, D["wage_shelter"], M["wage_shelter"])
frame(ax, "Real wage in shelter, 1950 = 100", f"Targeted; shelter read as pure site (no addition A). "
      f"Misfit {BY['wage_shelter']:.1f}.")
ax = axes[0, 2]
pair(ax, D["labour_share_c"], M["labour_share_c"])
frame(ax, "Labour's share of consumption", f"Targeted. Misfit {BY['labour_share_c']:.1f}.")
ax = axes[1, 0]
pair(ax, D["prime_emp_rate"], M["prime_emp_rate"])
frame(ax, "Prime-age employment rate", f"Targeted; support fixed at one basket. Misfit {BY['prime_emp_rate']:.1f}.")
ax = axes[1, 1]
tv = D["theta_V"].dropna()
ax.plot(tv.loc[:1992].index, tv.loc[:1992].values, color=S1, lw=0, marker="o", ms=5, markeredgecolor=SURFACE,
        markeredgewidth=1.5)
ax.plot(tv.loc[1997:].index, tv.loc[1997:].values, color=S1, lw=1.8, label="data")
ax.plot(M.index, M["theta_V"], color=S2, lw=1.8, label="base model")
ax.legend(frameon=False, loc="lower right", fontsize=8)
frame(ax, "Labour's share of a machine's build cost", f"Targeted where measured. Misfit {BY['theta_V']:.1f}.")
ax = axes[1, 2]
acc = pd.Series(R["accounting_eta"], index=YEARS, dtype=float)
ax.plot(YEARS, R["fitted_eta"], color=S2, lw=1.8, label="fitted clock")
ax.plot(acc.index, acc.values, color=S1, lw=0, marker="o", ms=3.5, label="accounting (the fork, year by year)")
ax.set_yscale("log")
ax.legend(frameon=False, loc="lower left", fontsize=8)
frame(ax, "Machine service needed per task (1950 = 1, log)", f"The fitted clock: {R['best']['par']['g_eta']:.1%} a "
      "year. Dots: the path that reproduces\nthe fork exactly in each year, all else at the fit.")
fig.suptitle(f"The base model against the US record, 1950–2024: misfit {R['best']['misfit']:.1f}", x=0.01, ha="left",
             fontsize=10.5, fontweight="bold", color=INK)
fig.tight_layout(h_pad=3.0, w_pad=2.0, rect=(0, 0, 1, 0.97))
os.makedirs(os.path.join(ROOT, "figures"), exist_ok=True)
fig.savefig(os.path.join(ROOT, "figures", "fig_fit_base.png"), dpi=150)
print("figures/fig_fit_base.png")
