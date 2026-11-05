# fig_compare.py — a candidate change against the model it extends and the data (decision 13: she judges better or worse;
# Claude does not look at a variant's fit). The five targeted series and the capability clock, each panel with the data,
# the reference model (dashed) and the variant, and both misfits. For the split, a third row: computing's clock, and the
# two checks the split's data give (the pay gap and the production group's share of jobs), never targeted.
# Run from us-record/:  python3 code/fig_compare.py fit_A A                       (against the base model)
#                       python3 code/fig_compare.py fit_split "A + split" --ref fit_A --ref-label A
# (reads results/<name>.json and the reference's; writes figures/fig_<name>.png)

import json
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker  # noqa: E402
import pandas as pd  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARGS = sys.argv[1:]
REF = ARGS[ARGS.index("--ref") + 1] if "--ref" in ARGS else "fit_base"
REF_LABEL = ARGS[ARGS.index("--ref-label") + 1] if "--ref-label" in ARGS else "base"
POS = [a for i, a in enumerate(ARGS) if not a.startswith("--") and (i == 0 or not ARGS[i - 1].startswith("--"))]
NAME = POS[0]
LABEL = POS[1] if len(POS) > 1 else NAME
B = json.load(open(os.path.join(ROOT, "results", f"{REF}.json")))
V = json.load(open(os.path.join(ROOT, "results", f"{NAME}.json")))
SPLIT = V["meta"].get("split_from") is not None
BASKET = V["meta"].get("sigma") is not None
YEARS = list(range(B["meta"]["years"][0], B["meta"]["years"][1] + 1))
MB, MV = pd.DataFrame(B["path"], index=YEARS), pd.DataFrame(V["path"], index=YEARS)
D = pd.read_csv(os.path.join(ROOT, "data", "panel.csv")).set_index("year").loc[YEARS]
S1, S2 = "#2a78d6", "#eb6834"                     # data, variant (categorical slots 1-2, validated); reference: muted ink
SURFACE, INK, INK2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e3df"
plt.rcParams.update({"font.size": 9, "axes.edgecolor": GRID, "xtick.color": INK2, "ytick.color": INK2,
                     "axes.titlecolor": INK, "axes.titlesize": 9.5, "axes.titleweight": "bold",
                     "figure.facecolor": SURFACE, "axes.facecolor": SURFACE})
BB, BV = B["best"]["by_series"], V["best"]["by_series"]
DASH = (0, (4, 3))


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
    ax.plot(MB.index, MB[s].values, color=INK2, lw=1.2, ls=DASH, label=REF_LABEL)
    ax.plot(MV.index, MV[s].values, color=S2, lw=1.8, label=LABEL)
    if legend:
        ax.legend(frameon=False, loc=loc, fontsize=8)


def note(s, extra=""):
    return f"{extra}Misfit: {REF_LABEL} {BB[s]:.1f}, {LABEL} {BV[s]:.1f} (1 = one tolerance)."


rows = 3 if SPLIT or BASKET else 2
fig, axes = plt.subplots(rows, 3, figsize=(12.5, 3.5 * rows))
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
CAP = V["meta"].get("cap")
if CAP is not None:                               # the cap, set from the data (not fitted)
    ax.axhline(CAP, color=INK2, lw=0.9, ls=":")
    ax.text(1949, CAP + 0.006, f"cap {CAP:.3f}", fontsize=7.5, color=INK2, va="bottom")
frame(ax, "Prime-age employment rate", note("prime_emp_rate"))
ax = axes[1, 1]
tv = D["theta_V"].dropna()
ax.plot(tv.loc[:1992].index, tv.loc[:1992].values, color=S1, lw=0, marker="o", ms=5, markeredgecolor=SURFACE,
        markeredgewidth=1.5)
ax.plot(tv.loc[1997:].index, tv.loc[1997:].values, color=S1, lw=1.8)
ax.plot(MB.index, MB["theta_V"], color=INK2, lw=1.2, ls=DASH)
ax.plot(MV.index, MV["theta_V"], color=S2, lw=1.8)
frame(ax, "Labour's share of a machine's build cost", note("theta_V"))
ax = axes[1, 2]
ax.plot(YEARS, B["fitted_eta"], color=INK2, lw=1.2, ls=DASH, label=f"{REF_LABEL} clock")
ax.plot(YEARS, V["fitted_eta"], color=S2, lw=1.8, label=f"{LABEL} clock")
ax.set_yscale("log")
ax.legend(frameon=False, loc="lower left", fontsize=8)
frame(ax, "Machine service needed per task (1950 = 1, log)", f"The fitted clocks: {REF_LABEL} "
      f"{B['best']['par']['g_eta']:.1%}, {LABEL} {V['best']['par']['g_eta']:.1%} a year.")

if SPLIT:
    start = V["meta"]["split_from"]
    ax = axes[2, 0]
    ax.plot(YEARS, MV["comp"], color=S2, lw=1.8)
    ax.set_yscale("log")
    ax.yaxis.set_major_locator(matplotlib.ticker.LogLocator(subs=(1.0, 2.0, 5.0)))
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda y, _: f"{y:g}"))
    ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    frame(ax, "Computing at the production group's tasks (log)",
          f"Machine service needed there beyond the clock: 1 before {start},\nthen falling "
          f"{V['best']['par']['g_c']:.1%} a year.")
    ax = axes[2, 1]
    ax.plot(D.index, D["pay_gap"].values, color=S1, lw=1.8)
    ax.axhline(1.0, color=INK2, lw=1.2, ls=DASH)
    ax.plot(MV.index, MV["pay_gap"].values, color=S2, lw=1.8)
    frame(ax, "Check: the pay gap, 1964 = 1",
          f"Not targeted: all employees' average hourly wage over the production\ngroup's. {REF_LABEL} has one group, "
          f"so no gap (dashed).")
    ax = axes[2, 2]
    ax.plot(D.index, D["pns_share"].values, color=S1, lw=1.8)
    ax.plot(MV.index, MV["routine_share"].values, color=S2, lw=1.8)
    frame(ax, "Check: the production group's share of jobs",
          f"Not targeted. The groups' sizes are set at the data's 1964–2024\nmean, {1.0 - V['meta']['s_n']:.3f}.")

if BASKET:
    sg, ug = V["meta"]["sigma"], V["meta"]["utility"]
    ax = axes[2, 0]
    ax.plot(YEARS, MV["goods_basket"] / MV["goods_basket"].iloc[0], color=S2, lw=1.8, label="goods")
    ax.plot(YEARS, MV["site_basket"] / MV["site_basket"].iloc[0], color=S2, lw=1.8, ls=(0, (1, 1.5)), label="land")
    ax.set_yscale("log")
    ax.yaxis.set_major_locator(matplotlib.ticker.LogLocator(subs=(1.0, 2.0, 5.0)))
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda y, _: f"{y:g}"))
    ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax.legend(frameon=False, loc="upper left", fontsize=8)
    frame(ax, f"{LABEL}: one person's basket, 1950 = 1 (log)",
          f"Goods and land substitute with elasticity {sg:.3f}, set from the data\n(next panel); "
          f"{REF_LABEL}'s basket is fixed at one unit and the same plot.")
    ax = axes[2, 1]
    hs = D["housing_share_pce"]
    ax.plot(D.index, hs / hs.iloc[0], color=S1, lw=1.8, label="housing's share of spending")
    ax.plot(MV.index, MV["site_share"] / MV["site_share"].iloc[0], color=S2, lw=1.8, label="land's share of the basket")
    ax.legend(frameon=False, loc="upper left", fontsize=8)
    frame(ax, "Shares of spending, 1950 = 1",
          "Not targeted, but not independent: housing's share against shelter's\nprice set the elasticity.")
    ax = axes[2, 2]
    rw = D["real_wage_cpi"]
    ax.plot(D.index, rw / rw.iloc[0], color=S1, lw=1.8, label="real hourly wage (CPI)")
    ax.plot(MV.index, MV["utility"], color=S2, lw=1.8, label="the basket's utility (set)")
    ax.legend(frameon=False, loc="lower right", fontsize=8)
    frame(ax, "The basket's utility, 1950 = 1",
          f"Set: rising {ug['growth']:.1%} a year to {ug['until']}, as the production\nworker's real wage did; "
          "held after.")

fig.suptitle(f"{LABEL} against {REF_LABEL} and the US record, 1950–2024: misfit {REF_LABEL} {B['best']['misfit']:.1f}, "
             f"{LABEL} {V['best']['misfit']:.1f}", x=0.01, ha="left", fontsize=10.5, fontweight="bold", color=INK)
fig.tight_layout(h_pad=3.0, w_pad=2.0, rect=(0, 0, 1, 0.97 if rows == 2 else 0.98))
os.makedirs(os.path.join(ROOT, "figures"), exist_ok=True)
out = os.path.join(ROOT, "figures", f"fig_{NAME}.png")
fig.savefig(out, dpi=150)
print(os.path.relpath(out, ROOT))
