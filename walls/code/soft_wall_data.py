# soft_wall_data.py — where the machine chain's soft wall has sat, from the lambda thread's measured full-chain
# labor-compensation share of machinery (../progress_and_prosperity/lambda/data). In the model the soft wall is at
# gamma(x_c) = gamma(x*)/theta, theta = gamma(x*) lam_m-tilde = the full-chain labor share of machine-service cost at
# the margin, which the lambda series measures as lambda-hat (compensation share of machinery final output, vertically
# integrated). So 1/lambda-hat is the soft wall's height over the margin, in relative-productivity units.
# Members: the century arc (1967-1992, spliced to the NAICS level) and family A (1997-2023: narrow, medium, broad
# machinery sets; tot = imports at US technology, dom = domestic content only).
# Run from walls/:  python code/soft_wall_data.py
import csv
import json
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

HERE = Path(__file__).resolve().parent
LAM = HERE.parents[1] / "progress_and_prosperity" / "lambda" / "data"
sys.path.insert(0, str(HERE))
import model as m  # noqa: E402

rcParams["font.family"] = "serif"
rcParams["font.serif"] = ["DejaVu Serif", "Georgia"]
rcParams["mathtext.fontset"] = "dejavuserif"
rcParams["font.size"] = 8.5
NAVY, BLUE, RED, GRAY = "#1a1a3d", "#4878b8", "#8b2020", "#9a9a9a"

century = [r for r in csv.DictReader(open(LAM / "lambda_us_century.csv")) if r["lam_spliced"]]
fam = list(csv.DictReader(open(LAM / "lambda_us_family_a.csv")))
cy = np.array([int(r["year"]) for r in century])
cl = np.array([float(r["lam_spliced"]) for r in century])
fy = np.array([int(r["year"]) for r in fam])
series = {f"{s} {t}": np.array([float(r[f"lam_{s}_{t}"]) for r in fam]) for s in ("narrow", "medium", "broad")
          for t in ("tot", "dom")}

calib = 1 / m.soft_wall_multiple()      # Appendix B's targets imply theta = 0.47/0.80
print(f"Appendix B's targets: theta {calib:.4f}, soft wall at {1 / calib:.3f} x gamma(x*)")
print("century arc (spliced): " + ", ".join(f"{y}: {l:.3f} -> {1 / l:.2f}" for y, l in zip(cy, cl)))
for k in ("narrow tot", "medium tot", "broad tot", "broad dom"):
    v = series[k]
    print(f"{k:10s}: 1997 {v[0]:.3f} ({1 / v[0]:.2f}), 2001 {v[4]:.3f} ({1 / v[4]:.2f}), 2010 {v[13]:.3f} "
          f"({1 / v[13]:.2f}), 2023 {v[-1]:.3f} ({1 / v[-1]:.2f})")
allv = np.concatenate([cl] + [series[k] for k in ("narrow tot", "medium tot", "broad tot")])
print(f"range over 1967-2023 (spliced + tot members): theta {allv.min():.3f}-{allv.max():.3f}, "
      f"soft wall {1 / allv.max():.2f}-{1 / allv.min():.2f} x gamma(x*)")
json.dump(dict(calibration_theta=calib, century={int(y): float(l) for y, l in zip(cy, cl)},
               family_a={k: {int(y): float(x) for y, x in zip(fy, v)} for k, v in series.items()}),
          open(HERE.parent / "results" / "soft_wall_data.json", "w"), indent=1)

fig, ax = plt.subplots(figsize=(0.88 * 16 / 2.54, 2.9), layout="constrained")
ax.plot(cy, 1 / cl, "o-", color=NAVY, lw=1.2, ms=3.5, label="century arc (BEA benchmarks, spliced), 1967–1992")
for k, col, ls in (("narrow tot", BLUE, "-"), ("medium tot", BLUE, "--"), ("broad tot", BLUE, ":"),
                   ("broad dom", GRAY, "-")):
    ax.plot(fy, 1 / series[k], color=col, ls=ls, lw=1.1, label=f"{k} machinery, 1997–2023")
ax.axhline(1 / calib, color=RED, lw=0.9, ls=(0, (5, 2)))
ax.annotate("Appendix B's targets (1.70)", xy=(1968, 1 / calib + 0.015), color=RED, fontsize=7.5)
ax.set_ylabel(r"soft wall height $\gamma(x_c)/\gamma(x^*) = 1/\hat\lambda$")
ax.set_xlabel("year")
ax.set_ylim(1.3, 2.3)
ax.legend(loc="upper left", fontsize=6.8, frameon=False, ncol=2)
ax.grid(alpha=0.25, lw=0.33)
ax.spines[["top", "right"]].set_visible(False)
ax.set_title("The machine chain's soft wall, from the measured labor content of machinery (US)", loc="left",
             fontsize=8.5, color="#333333")
fig.savefig(HERE.parent / "figures" / "soft_wall_data.png", dpi=200)
print("wrote figures/soft_wall_data.png and results/soft_wall_data.json")
