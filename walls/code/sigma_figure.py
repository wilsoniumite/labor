# sigma_figure.py — the summary figure: along sigma (the shape the backward calibration leaves free), (a) where labor
# sits relative to the soft wall, with the first-order formula s_M sigma ln(1/theta) and the data's sigma ranges;
# (b) what automation does to w/P_s depending on where it lands, and recursive automation.
# Run from walls/:  python code/sigma_figure.py
import json
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from scipy.optimize import brentq
from tqdm.auto import tqdm

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import model as m  # noqa: E402

rcParams["font.family"] = "serif"
rcParams["font.serif"] = ["DejaVu Serif", "Georgia"]
rcParams["mathtext.fontset"] = "dejavuserif"
rcParams["font.size"] = 8.5
NAVY, BLUE, RED, GRAY, BROWN = "#1a1a3d", "#4878b8", "#8b2020", "#9a9a9a", "#8a6d3b"
X, R = m.margin_from_targets(), m.R_of()
THETA = 1 / m.soft_wall_multiple()


def k_for(sigma):
    return brentq(lambda kk: m.sigma_margin(m.calibrate(m.power_family(kk)), X) - sigma, 3.95, 400.0, xtol=1e-8)


OUT = HERE.parent / "results" / "sigma_figure.json"
if OUT.exists() and "--recompute" not in sys.argv:
    rows = json.load(open(OUT))
else:
    sigmas = np.geomspace(0.22, 2.4, 24)
    rows = []
    for sg in tqdm(sigmas, desc="sigma grid"):
        P = m.calibrate(m.power_family(k_for(sg)))
        q = m.solve(P)
        s, x0, xc = P["sched"], q["x"], q["x_c"]
        rw = lambda Q: m.solve(Q)["real_wage"] / q["real_wage"] - 1          # noqa: E731
        rows.append(dict(sigma=sg, contestable=(xc - x0) / (1 - x0),
                         uniform=rw({**P, "sched": m.scaled(s, 0.5)}),
                         machine=rw({**P, "sched": m.resorted(s, lambda x: np.where(x < x0, 0.5, 1.0))}),
                         band=rw({**P, "sched": m.resorted(s, lambda x: np.where((x >= x0) & (x < xc), 0.5, 1.0))}),
                         recursive=rw({**P, "lam": 0.0})))
    json.dump(rows, open(HERE.parent / "results" / "sigma_figure.json", "w"), indent=1)
sg = np.array([r["sigma"] for r in rows])
get = lambda k: np.array([r[k] for r in rows])  # noqa: E731

fig, axs = plt.subplots(1, 2, figsize=(0.88 * 16 / 2.54 * 1.3, 3.1), layout="constrained")
for ax in axs:
    ax.axvspan(0.3, 0.7, color=BLUE, alpha=0.12, lw=0)
    ax.axvspan(0.08, 0.76, ymin=0, ymax=0.04, color=BROWN, alpha=0.5, lw=0)
    for v, lab in ((2.293, "Appendix B\n(low root)"), (0.744, "high\nroot")):
        ax.axvline(v, color="#666666", lw=0.6, ls=":")
    ax.set_xscale("log")
    ax.set_xlim(0.2, 2.5)
    ax.set_xticks([0.25, 0.5, 1.0, 2.0])
    ax.set_xticklabels(["0.25", "0.5", "1", "2"])
    ax.xaxis.set_minor_formatter(plt.NullFormatter())
    ax.set_xlabel(r"$\sigma$ at the margin (machine services vs labor)")
    ax.grid(alpha=0.25, lw=0.33)
    ax.spines[["top", "right"]].set_visible(False)
ax = axs[0]
ax.plot(sg, get("contestable"), color=NAVY, lw=1.6, label="calibrated economy (power family)")
ax.plot(sg, R / (1 + R) * sg * np.log(1 / THETA), color=RED, lw=1.0, ls="--",
        label=r"$s_M\,\sigma\,\ln(1/\theta)$, first order")
ax.set_ylabel("share of labor's tasks still contestable\n(the rest are behind the soft wall)")
ax.set_ylim(0, 0.8)
ax.annotate("literature\n0.3–0.7", xy=(0.46, 0.40), ha="center", fontsize=7.5, color=BLUE)
ax.annotate("companion envelope 0.08–0.76", xy=(0.21, 0.045), fontsize=6.8, color=BROWN)
ax.annotate("Appendix B\n(low root)", xy=(2.2, 0.73), ha="right", fontsize=7, color="#555555")
ax.legend(loc="upper left", fontsize=6.8, frameon=False, bbox_to_anchor=(0.0, 0.97))
ax.set_title("(a) How close labor sits to the soft wall", loc="left", fontsize=8.5, color="#333333")
ax = axs[1]
ax.axhline(0, color="#888888", lw=0.6)
ax.plot(sg, get("uniform"), color=NAVY, lw=1.6, label=r"$\gamma$ halved everywhere (Figure 3)")
ax.plot(sg, get("machine"), color=GRAY, lw=1.3, label="... at machine tasks only")
ax.plot(sg, get("band"), color=RED, lw=1.6, label="... at labor's contestable band (Section 3.4)")
ax.plot(sg, get("recursive"), color=BROWN, lw=1.3, ls="--", label=r"recursive automation, $\widetilde\lambda_m = 0$")
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:+.0%}"))
ax.set_ylabel(r"change in $w/P_s$")
ax.legend(loc="upper right", fontsize=6.6, frameon=False)
ax.set_title("(b) What automation does, by where it lands", loc="left", fontsize=8.5, color="#333333")
fig.savefig(HERE.parent / "figures" / "sigma.png", dpi=200)
print("wrote figures/sigma.png and results/sigma_figure.json")
for r in rows[::4]:
    print(f"sigma {r['sigma']:.2f}: contestable {r['contestable']:.3f}; uniform {r['uniform']:+.1%}, machine "
          f"{r['machine']:+.1%}, band {r['band']:+.1%}, recursive {r['recursive']:+.1%}")
