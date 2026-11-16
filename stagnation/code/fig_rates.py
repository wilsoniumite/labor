# fig_rates.py — the paper's figure of Proposition 3: the required return.
# Along the required return rho from 0.01 to 0.10, in the instance with funded exit and with nobody supported outside
# work: (a) the wage-rent ratio w/r, (b) the price of land in hours of work, 1/(rho w/r), (c) output per hour, each
# relative to its value at the instance's rho = 0.09. Enclosed, the margin does not move: lower returns lower w/r
# and raise land's price in hours, and output per hour stays where it is; with funded exit, people leave work as the
# wage falls and output per hour rises. Same typography and series colors as fig_paths.py.
# Run from stagnation/:  ../venv/bin/python code/fig_rates.py
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

import model as M

rcParams["font.family"] = "serif"
rcParams["font.serif"] = ["DejaVu Serif"]
rcParams["mathtext.fontset"] = "dejavuserif"
rcParams["pdf.fonttype"] = 42
PRINT_W = 0.88 * 16 / 2.54
rcParams["font.size"] = 8.5
rcParams["xtick.labelsize"] = rcParams["ytick.labelsize"] = 7.5
rcParams["axes.linewidth"] = 0.53
for _ax in ("xtick", "ytick"):
    rcParams[f"{_ax}.major.width"] = rcParams[f"{_ax}.minor.width"] = 0.45
    rcParams[f"{_ax}.major.size"] = 2.3
    rcParams[f"{_ax}.minor.size"] = 1.3

COLOR = {"funded": "#2a78d6", "enclosed": "#1baf7a"}
NAME = {"funded": "Funded exit", "enclosed": "All enclosed"}
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#e4e3df"
RHO0 = M.BASE["rho"]

RHOS = np.linspace(0.01, 0.10, 91)
i0 = int(np.argmin(np.abs(RHOS - RHO0)))
assert abs(RHOS[i0] - RHO0) < 1e-12
runs = {k: M.rates(M.with_(M.BASE, **M.REGIMES[k]), RHOS) for k in COLOR}
ser = {}
for k in COLOR:
    v = np.array([q["v"] for q in runs[k]])
    land = np.array([q["land_price_hours"] for q in runs[k]])
    pi = np.array([q["pi"] for q in runs[k]])
    ser[k] = dict(v=v / v[i0], land=land / land[i0], pi=pi / pi[i0])

# the picture's claims, checked on the model
for k in COLOR:
    assert np.all(np.diff(ser[k]["v"]) > 0) and np.all(np.diff(ser[k]["land"]) < 0), k
assert np.max(np.abs(ser["enclosed"]["pi"] - 1)) < 1e-12
assert np.all(np.diff(ser["funded"]["pi"]) < 0)

fig, axes = plt.subplots(1, 3, figsize=(PRINT_W, PRINT_W / 2.75), layout="constrained")
panels = (("v", "Wage–rent ratio, $w/r$", "linear"), ("land", "Price of land in hours", "log"),
          ("pi", "Output per hour", "linear"))
for ax, (key, ylabel, scale), tag in zip(axes, panels, ("(a)", "(b)", "(c)")):
    for k in ("funded", "enclosed"):
        ax.plot(RHOS, ser[k][key], color=COLOR[k], lw=1.4, solid_capstyle="round", label=NAME[k])
    ax.set_yscale(scale)
    ax.set_xlim(0.0, 0.105)
    ax.set_xticks([0.0, 0.05, 0.10])
    ax.set_ylabel(ylabel)
    ax.grid(True, which="major", color=GRID, lw=0.5)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(colors=MUTED, labelcolor=INK)
    ax.text(0.0, 1.02, tag, transform=ax.transAxes, ha="left", va="bottom", fontsize=8.5, color=INK)
fig.supxlabel(r"Required return, $\rho$", fontsize=8.5)
top = max(ser[k]["v"].max() for k in COLOR)
axes[0].set_ylim(0, 1.06 * top)
axes[1].set_yticks([1, 3, 10, 30])
axes[1].yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{y:g}"))
axes[1].yaxis.set_minor_formatter(plt.NullFormatter())
lo, hi = min(ser[k]["pi"].min() for k in COLOR), max(ser[k]["pi"].max() for k in COLOR)
axes[2].set_ylim(lo - 0.006, hi + 0.008)
# direct labels on panel (c), where the two lines separate (ink text beside each line)
axes[2].annotate(NAME["funded"], xy=(0.030, float(np.interp(0.030, RHOS, ser["funded"]["pi"])) + 0.004), ha="left",
                 va="bottom", fontsize=7.5, color=INK)
axes[2].annotate(NAME["enclosed"], xy=(0.012, 1.0025), ha="left", va="bottom", fontsize=7.5, color=INK)
fig.legend(*axes[0].get_legend_handles_labels(), loc="outside upper center", ncol=2, frameon=False, fontsize=7.5,
           handlelength=1.6, columnspacing=1.5)
OUT = Path(__file__).resolve().parents[1] / "paper" / "figures" / "fig_rates.png"
fig.savefig(OUT, dpi=300)
fig.savefig(OUT.with_suffix(".pdf"), metadata={"CreationDate": None})
print(f"wrote {OUT} and {OUT.with_suffix('.pdf').name}")
