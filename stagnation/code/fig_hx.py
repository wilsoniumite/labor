# fig_hx.py — the figure of H-X, the pre-registered cross-country test (code/hx_test.py, data/hx_results.json).
# (a) Across countries, 1995-2019: growth of output per hour against growth of hours per person aged 15-64, both
#     net of log output per hour in 1995 (the primary regression's control), so the fitted line's slope is the
#     primary coefficient. (b) Within countries: five-year growth rates net of country and period effects, so the
#     fitted line's slope is the panel coefficient. Percent per year. Same typography as the theory figures.
# Run from stagnation/:  ../venv/bin/python code/fig_hx.py
import json
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

import hx_test as H

rcParams["font.family"] = "serif"
rcParams["font.serif"] = ["DejaVu Serif"]
rcParams["mathtext.fontset"] = "dejavuserif"
rcParams["pdf.fonttype"] = 42
PRINT_W = 0.88 * 16 / 2.54
rcParams["font.size"] = 8.5
rcParams["xtick.labelsize"] = rcParams["ytick.labelsize"] = 7.5
rcParams["axes.linewidth"] = 0.53
for _ax in ("xtick", "ytick"):
    rcParams[f"{_ax}.major.width"] = 0.45
    rcParams[f"{_ax}.major.size"] = 2.3
DOT, INK, MUTED, GRID = "#2a78d6", "#0b0b0b", "#52514e", "#e4e3df"

ROOT = Path(__file__).resolve().parents[1]
res = json.loads((ROOT / "data" / "hx_results.json").read_text())
gdph, hrs, pop, pwt_h = H.load()
countries = H.sample(gdph, hrs, pop)
df = H.build(gdph, hrs, pop, countries)


def residualize(v, Z):
    return v - Z @ np.linalg.lstsq(Z, v, rcond=None)[0]


Z = np.column_stack([np.ones(len(df)), df.log_pi0.values])
ry, rx = residualize(df.g_pi.values, Z) * 100, residualize(df.g_h.values, Z) * 100
slope_a = np.polyfit(rx, ry, 1)[0]
assert abs(slope_a - res["primary"]["beta"]) < 1e-10      # Frisch-Waugh: the slope is the primary coefficient

pf = H.panel_frame(gdph, hrs, pop, countries)
cty, per = pf.country.to_numpy(dtype=object), pf.period.to_numpy(dtype=object)
Zp = np.column_stack([(cty[:, None] == np.array(sorted(set(cty)), dtype=object)[None, :]).astype(float),
                      (per[:, None] == np.array(sorted(set(per)), dtype=object)[None, 1:]).astype(float)])
py, px = residualize(pf.g_pi.to_numpy(float), Zp) * 100, residualize(pf.g_h.to_numpy(float), Zp) * 100
slope_b = np.polyfit(px, py, 1)[0]
assert abs(slope_b - res["panel"]["beta"]) < 1e-10

fig, (a1, a2) = plt.subplots(1, 2, figsize=(PRINT_W, PRINT_W / 2.25), layout="constrained")
for ax, x, y, s, tag in ((a1, rx, ry, slope_a, "(a)"), (a2, px, py, slope_b, "(b)")):
    ax.axhline(0, color=GRID, lw=0.6, zorder=0)
    ax.axvline(0, color=GRID, lw=0.6, zorder=0)
    ax.scatter(x, y, s=16 if ax is a1 else 9, color=DOT, edgecolors="white", linewidths=0.6, zorder=3)
    xs = np.linspace(x.min(), x.max(), 2)
    ax.plot(xs, s * xs, color=INK, lw=1.0, zorder=2)
    ax.grid(True, color=GRID, lw=0.5)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(colors=MUTED, labelcolor=INK)
    ax.text(0.0, 1.02, tag, transform=ax.transAxes, ha="left", va="bottom", fontsize=8.5, color=INK)
    left = ax is a2      # panel (b): the lower left is empty; panel (a): the lower right
    ax.text(0.03 if left else 0.98, 0.04, f"slope {s:+.2f}".replace("-", "\u2212"), transform=ax.transAxes, ha="left" if left else "right",
            va="bottom", fontsize=7.5, color=INK)
# label the countries at the edges of panel (a): the three largest residual hours changes each way, and the US
order = np.argsort(rx)
for i in set(order[:3]) | set(order[-3:]) | {list(df.index).index("USA")}:
    if df.index[i] == "USA":     # a crowded spot: a thin leader line from clear space above
        a1.annotate("USA", xy=(rx[i], ry[i]), xytext=(rx[i] - 0.1, ry[i] + 0.45), fontsize=6.5, color=MUTED,
                    ha="center", arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.5, shrinkA=1, shrinkB=3))
    else:
        a1.annotate(df.index[i], xy=(rx[i], ry[i]), xytext=(3, 2), textcoords="offset points", fontsize=6.5,
                    color=MUTED)
a1.set_xlabel("Hours per person 15–64 (% a year)", fontsize=7.5)
a1.set_ylabel("Output per hour (% a year)", fontsize=7.5)
a2.set_xlabel("Hours per person 15–64 (% a year)", fontsize=7.5)
a2.set_ylabel("Output per hour (% a year)", fontsize=7.5)
OUT = ROOT / "paper" / "figures" / "fig_hx.png"
fig.savefig(OUT, dpi=300)
fig.savefig(OUT.with_suffix(".pdf"), metadata={"CreationDate": None})
print(f"wrote {OUT} and {OUT.with_suffix('.pdf').name}")
