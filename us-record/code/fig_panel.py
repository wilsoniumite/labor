# fig_panel.py — the us-record panel at a glance (for breakpoint A): the four targeted facts and the measured inputs,
# 1950–2024, one axis per panel. Reads data/panel.csv; writes figures/fig_panel.png.
# Run from us-record/:  python3 code/fig_panel.py

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = pd.read_csv(os.path.join(ROOT, "data", "panel.csv")).set_index("year")
S1, S2 = "#2a78d6", "#eb6834"                     # categorical slots 1-2 (validated, light surface)
SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
plt.rcParams.update({"font.size": 9, "axes.edgecolor": GRID, "axes.labelcolor": INK2, "xtick.color": INK2,
                     "ytick.color": INK2, "axes.titlecolor": INK, "axes.titlesize": 9.5, "axes.titleweight": "bold",
                     "figure.facecolor": SURFACE, "axes.facecolor": SURFACE})


def frame(ax, title, note=None):
    ax.set_title(title, loc="left")
    ax.grid(True, color=GRID, linewidth=0.6)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.set_xlim(1948, 2026)
    if note:
        ax.text(0.0, -0.17, note, transform=ax.transAxes, fontsize=7.5, color=INK2, va="top")


def end_label(ax, s, text, dy=0):
    s = s.dropna()
    ax.annotate(text, (s.index[-1], s.iloc[-1]), xytext=(4, dy), textcoords="offset points", fontsize=8, color=INK,
                va="center")


fig, axes = plt.subplots(2, 3, figsize=(12.5, 7.0))
ax = axes[0, 0]
ax.plot(P.index, P["wage_goods"], color=S1, lw=1.8, label="in durables")
ax.plot(P.index, P["wage_shelter"], color=S2, lw=1.8, label="in shelter")
ax.set_yscale("log")
ax.set_yticks([100, 200, 400, 600]); ax.set_yticklabels(["100", "200", "400", "600"])
ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
end_label(ax, P["wage_goods"], "durables"); end_label(ax, P["wage_shelter"], "shelter")
ax.legend(frameon=False, loc="upper left", fontsize=8)
frame(ax, "Real hourly wage, 1950 = 100 (log scale)", "Targeted. The deflator fork: x4.8 over 1964–2024.")

ax = axes[0, 1]
weak = P["labour_share_c_tier"] == "WEAK"
ax.fill_between(P.index, P["labour_share_c_lo"], P["labour_share_c_hi"], where=weak, color=S1, alpha=0.15, lw=0)
ax.plot(P.index, P["labour_share_c"], color=S1, lw=1.8)
frame(ax, "Labour's share of consumption, full chain", "Targeted. Shaded: the regression band (no band 1997–2023,\n"
      "measured from annual input-output tables).")

ax = axes[0, 2]
ax.plot(P.index, P["emp_rate"], color=S1, lw=1.8, label="16+ (targeted)")
ax.plot(P.index, P["prime_emp_rate"], color=S2, lw=1.8, label="25–54 (a check)")
end_label(ax, P["emp_rate"], "16+"); end_label(ax, P["prime_emp_rate"], "25–54")
ax.legend(frameon=False, loc="upper left", fontsize=8)
frame(ax, "Employment rate", "Targeted: 16+. 2025 missing (October 2025 never published).")

ax = axes[1, 0]
ax.axhline(0, color=INK2, lw=0.8)
ax.plot(P.index, P["real_rate"], color=S1, lw=1.8)
frame(ax, "Real long rate", "Input. Moody's Aaa yield less the mean CPI inflation\nof the five years to t.")

ax = axes[1, 1]
ax.plot(P.index, P["delta"], color=S1, lw=1.8)
frame(ax, "Depreciation rate, all fixed assets", "Input. BEA Fixed Assets: depreciation over the\naverage net stock "
      "(0.0522 in 2023, as calibration (c)).")

ax = axes[1, 2]
tv = P["theta_V"].dropna()
bench, annual = tv.loc[:1992], tv.loc[1997:]
ax.plot(annual.index, annual, color=S1, lw=1.8)
ax.plot(bench.index, bench, color=S1, lw=0, marker="o", ms=5, markeredgecolor=SURFACE, markeredgewidth=1.5)
frame(ax, "Labour's share of a machine's build cost", "Input. Annual 1997–2023 on calibration (c)'s basis; dots: "
      "benchmark\nyears 1967–1992, linked at 1997. Nothing before 1967.")
ax.set_ylim(0.40, 0.62)

fig.tight_layout(h_pad=3.2, w_pad=2.0)
os.makedirs(os.path.join(ROOT, "figures"), exist_ok=True)
fig.savefig(os.path.join(ROOT, "figures", "fig_panel.png"), dpi=150)
print("figures/fig_panel.png")
