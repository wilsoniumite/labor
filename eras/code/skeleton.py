# skeleton.py — the measurable frame around the margin through time: the ceiling's height over the margin, 1/theta, and
# the width of the contestable band, the share of the tasks labor holds that lie between the margin and the ceiling.
#
# From the paper (Section 3.3, Appendix B): theta = gamma(x*) lambda_m is labor's full-chain share of machine-service
# cost, the ceiling sits where gamma(x_c) = gamma(x*)/theta, and, to first order, the contestable share of labor's tasks
# is (x_c - x*)/(1 - x*) = s_M sigma ln(1/theta), with s_M the machines' share of final-task cost and sigma the
# elasticity of substitution at the margin. In labor-share coordinates the schedule's log-slope at the margin is
# 1/(s_M sigma), so the band is the ceiling's log-height times s_M sigma.
# theta, by source:
#   US 1967-1992: the lambda thread's century arc (../progress_and_prosperity/lambda/data/lambda_us_century.csv), BEA
#     benchmark IO tables, machinery's vertically integrated labor-compensation share, raw and spliced members.
#   US 1997-2023: the lambda thread's family A, 'tot' members (narrow, medium, broad machinery sets), the same members
#     the walls thread used (../walls/REPORT.md, section 1).
#   UK 1855-2016: no input-output tables; proxy: the Bank of England millennium dataset's labour share of the whole
#     economy excluding rents. Where the US has both (1967-1992), machinery's share runs 0.02-0.14 above the
#     economy-wide compensation share, so the proxy is rough, likely low.
# Assumed bands (not data): sigma 0.3 / 0.6 / 0.9 (the aggregate literature runs about 0.3-0.7; Chirinko 2008, Oberfield
# and Raval 2021), s_M 0.35 / 0.45 / 0.55.
# Run from eras/:  ../venv/Scripts/python.exe code/skeleton.py
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
LAM = ROOT.parent / "progress_and_prosperity" / "lambda" / "data"
SIGMA = dict(low=0.3, central=0.6, high=0.9)
S_M = dict(low=0.35, central=0.45, high=0.55)

cen = pd.read_csv(LAM / "lambda_us_century.csv").dropna(subset=["lam"])
fam = pd.read_csv(LAM / "lambda_us_family_a.csv")
us = pd.concat([cen.melt(id_vars="year", value_vars=["lam", "lam_spliced"], var_name="member", value_name="theta"),
                fam.melt(id_vars="year", value_vars=["lam_narrow_tot", "lam_medium_tot", "lam_broad_tot"],
                         var_name="member", value_name="theta")]).dropna()
uk = pd.read_csv(ROOT / "data" / "boe_uk_1700_2016.csv").dropna(subset=["labour_share_ex_rents"])
uk = uk[["year", "labour_share_ex_rents"]].rename(columns={"labour_share_ex_rents": "theta"})
gap = (cen.set_index("year").lam - cen.set_index("year").comp_share_of_va).agg(["min", "max"])
print(f"US machinery theta less economy-wide compensation share, 1967-1992: {gap['min']:+.3f} to {gap['max']:+.3f}")


def band(theta):
    """Contestable share of labor's tasks, s_M sigma ln(1/theta), at the low, central and high assumptions."""
    lt = np.log(1.0 / np.asarray(theta, dtype=float))
    return {k: S_M[k] * SIGMA[k] * lt for k in ("low", "central", "high")}


us_y = us.groupby("year").theta.agg(["min", "median", "max"])
for y in (1967, 1982, 1997, 2023):
    t = us_y.loc[y]
    b = band(t["median"])
    print(f"US {y}: theta {t['min']:.2f}-{t['max']:.2f}, ceiling {1 / t['max']:.2f}-{1 / t['min']:.2f} x the margin; "
          f"contestable share of labor's tasks {band(t['max'])['low']:.1%}-{band(t['min'])['high']:.1%} "
          f"(central {b['central']:.1%})")
for y in (1855, 1870, 1900, 1950, 1970, 2000, 2016):
    t = float(uk.set_index("year").theta[y])
    b = band(t)
    print(f"UK {y}: proxy theta {t:.2f}, ceiling {1 / t:.2f} x the margin; contestable {b['low']:.1%}-{b['high']:.1%} "
          f"(central {b['central']:.1%})")
pd.concat([us.assign(country="US", source="BEA IO, machinery (lambda thread)"),
           uk.assign(country="UK", member="labour share ex rents", source="BoE millennium dataset (proxy)")]) \
  .to_csv(ROOT / "data" / "theta.csv", index=False)

# %% figure
NAVY, BLUE, RED, GRAY, GOLD = "#1a1a3d", "#4878b8", "#8b2020", "#777777", "#a07a2a"
fig, (a, c) = plt.subplots(1, 2, figsize=(11, 4.2), layout="constrained")
a.plot(uk.year, 1 / uk.theta, color=GOLD, lw=1.3, label="UK, proxy: 1 / labour share excluding rents (BoE)")
for m, g in us.groupby("member"):
    a.plot(g.year, 1 / g.theta, "o-", color=NAVY, lw=0.8, ms=2.5, alpha=0.75)
a.plot([], [], "o-", color=NAVY, ms=2.5, label="US: 1 / machinery's full-chain labor share (BEA IO)")
a.axhline(1.708, color=RED, lw=0.8, ls="--")
a.text(1858, 1.73, "Appendix B's instance, 1.71", color=RED, fontsize=7.5)
a.set(xlim=(1850, 2025), ylim=(1.0, 2.2), xlabel="Year", ylabel=r"Ceiling height over the margin, $1/\theta$",
      title="(a) How far above the margin the ceiling sits\n(where a machine would embody as much labor as it saves)")
a.legend(loc="upper left", fontsize=7.5, frameon=False)
for tbl, colr, lab in ((uk.set_index("year").theta, GOLD, "UK (proxy)"),
                       (us_y["median"], NAVY, "US (machinery, median member)")):
    b = band(tbl.values)
    c.fill_between(tbl.index, b["low"], b["high"], color=colr, alpha=0.18, lw=0)
    c.plot(tbl.index, b["central"], "o-" if colr == NAVY else "-", color=colr, lw=1.3, ms=2.5, label=lab)
c.set(xlim=(1850, 2025), ylim=(0, 0.35), xlabel="Year", ylabel="Share of labor's tasks",
      title=r"(b) The contestable band, $s_M\,\sigma\,\ln(1/\theta)$" + "\n"
      r"(central $s_M$ 0.45, $\sigma$ 0.6; band $s_M$ 0.35-0.55, $\sigma$ 0.3-0.9)")
c.legend(loc="upper left", fontsize=7.5, frameon=False)
for ax in (a, c):
    ax.title.set_fontsize(9)
    ax.grid(alpha=0.25, lw=0.33)
    ax.spines[["top", "right"]].set_visible(False)
fig.savefig(ROOT / "figures" / "skeleton.png", dpi=200)
print("wrote figures/skeleton.png and data/theta.csv")
