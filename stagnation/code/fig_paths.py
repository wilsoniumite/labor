# fig_paths.py — the paper's figure of Proposition 2: two economies with the same machines.
# Output per hour (left) and hours worked per person (right) along a path of machine progress, gamma_eta = eta gamma,
# capability 1/eta from 1 to 10^4, in the instance under four rules for who can leave work (model.REGIMES): funded,
# unconditional exit; a quarter of people with no support outside work; nobody with support outside work; support
# for everyone plus 0.3 baskets for working. Where some hours remain, output per hour levels off at T/(h N_inf);
# where none remain it rises with machine capability. Drawn at the width it prints (0.88 of the 16 cm text width),
# text at 7.5-8.5 pt; series colors from the validated categorical order (blue, orange, aqua, yellow), each regime
# keeping its color in every figure; direct labels at the line ends (aqua and yellow sit below 3:1 on white).
# Run from stagnation/:  ../venv/bin/python code/fig_paths.py
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

COLOR = {"funded": "#2a78d6", "quarter": "#eb6834", "enclosed": "#1baf7a", "conditioned": "#eda100"}
NAME = {"funded": "Funded exit", "quarter": "Quarter enclosed", "enclosed": "All enclosed",
        "conditioned": "Conditioned support"}
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#e4e3df"
ORDER = ("funded", "conditioned", "quarter", "enclosed")

ETAS = np.logspace(0.0, -4.0, 161)
cap = 1.0 / ETAS
runs = {k: M.path(M.with_(M.BASE, **M.REGIMES[k]), ETAS) for k in ORDER}
pi = {k: np.array([q["pi"] for q in runs[k]]) for k in ORDER}
hours = {k: np.array([q["participation"] for q in runs[k]]) for k in ORDER}
ceil = {k: M.pi_ceiling(M.with_(M.BASE, **M.REGIMES[k])) for k in ORDER}

# the picture's claims, checked on the model
for k in ORDER:
    assert np.all(np.diff(pi[k]) > 0), k
    if np.isfinite(ceil[k]):
        assert np.all(pi[k] <= ceil[k] * (1 + 1e-12)) and pi[k][-1] > 0.98 * ceil[k], k
assert abs(np.log(pi["funded"][-1] / pi["funded"][-2]) / np.log(cap[-1] / cap[-2]) - 1) < 0.01
assert hours["enclosed"].min() > 1 - 1e-9 and hours["funded"][-1] < 0.01
assert abs(hours["quarter"][-1] - 0.25) < 0.01 and abs(hours["conditioned"][-1] - M.N_inf(
    M.with_(M.BASE, **M.REGIMES["conditioned"]))) < 0.01

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(PRINT_W, PRINT_W / 2.05), layout="constrained",
                               gridspec_kw=dict(width_ratios=[1.5, 1.0]))
for k in ORDER:
    ax1.plot(cap, pi[k], color=COLOR[k], lw=1.4, solid_capstyle="round", label=NAME[k])
    ax2.plot(cap, hours[k], color=COLOR[k], lw=1.4, solid_capstyle="round", label=NAME[k])
    if np.isfinite(ceil[k]):
        ax1.axhline(ceil[k], color=COLOR[k], lw=0.5, alpha=0.45, zorder=0)
# direct labels in clear space beside each line's flat end (text in ink, the line beside it carries the color):
# conditioned above its line, the two enclosed below theirs, funded above-left of its rising stretch
for k, dy, va in (("conditioned", 1.32, "center"), ("quarter", 0.70, "center"), ("enclosed", 0.70, "center")):
    ax1.annotate(NAME[k], xy=(cap[-1], pi[k][-1] * dy), ha="right", va=va, fontsize=7.5, color=INK)
x_f = 350.0
ax1.annotate(NAME["funded"], xy=(x_f, pi["funded"][np.searchsorted(cap, x_f)] * 1.5), ha="right", va="bottom",
             fontsize=7.5, color=INK)
ax1.set_xscale("log"); ax1.set_yscale("log")
ax1.set_xlim(1, 1e4); ax1.set_ylim(2, 6e3)
ax1.set_ylabel("Output per hour (baskets)")
ax2.set_xscale("log")
ax2.set_xlim(1, 1e4); ax2.set_ylim(0, 1.05)
ax2.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
ax2.set_ylabel("Hours worked per person")
fig.supxlabel("Machine capability at every task (baseline = 1)", fontsize=8.5)
for ax, tag in ((ax1, "(a)"), (ax2, "(b)")):
    ax.grid(True, which="major", color=GRID, lw=0.5)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(colors=MUTED, labelcolor=INK)
    ax.text(0.0, 1.02, tag, transform=ax.transAxes, ha="left", va="bottom", fontsize=8.5, color=INK)
leg = fig.legend(*ax2.get_legend_handles_labels(), loc="outside upper center", ncol=4, frameon=False, fontsize=7.5,
                 handlelength=1.6, columnspacing=1.2)
OUT = Path(__file__).resolve().parents[1] / "paper" / "figures" / "fig_paths.png"
fig.savefig(OUT, dpi=300)
fig.savefig(OUT.with_suffix(".pdf"), metadata={"CreationDate": None})
print(f"wrote {OUT} and {OUT.with_suffix('.pdf').name}")
