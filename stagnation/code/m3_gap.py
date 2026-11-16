# m3_gap.py — M3 of docs/spec.md: pay against productivity, U.S. nonfarm business sector, from the dated FRED pull.
# Identity (Lemma 2, eq. 13): real pay per hour / output per hour = labor's share x P_Y / P_C, with
#   output per hour OPHNFB, hourly compensation HCOMPBS, the sector's price deflator IPDNBS (P_Y), labor's share
#   PRS85006173 (BLS: compensation over current-dollar output, so LS = HCOMPBS / (IPDNBS x OPHNFB) up to the index base),
#   consumer prices CPIAUCSL (P_C) or CPI less shelter CUUR0000SA0L2; descriptive: CPI less energy CPILEGSL, less
#   medical care CUUR0000SA0L5.
# Over a window, the log gap between output per hour and real pay splits exactly into labor's share (-dlog LS) and
# the price wedge (dlog P_C/P_Y), with LS the share implied by the series compared, HCOMPBS / (IPDNBS x OPHNFB).
# BLS's published labor share drifts from it by about 6.5 log points over 1948-2000 (about 1 over each window), so
# its change is reported alongside, not used in the split. Windows as frozen: 1973-2024 and 1983-2024 (the CPI's owner-occupied housing method
# changed in 1983). Prediction as frozen: the wedge rises, and CPI less shelter removes at least a third of the rise
# (a tenth or less counts against; between, partial). Writes data/m3_gap.json, draws Figure 5
# (paper/figures/fig_gap.pdf, .png).
# Run from stagnation/:  ../venv/bin/python code/m3_gap.py
import json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams

import m1_eras

ROOT = Path(__file__).resolve().parents[1]
WINDOWS = ((1973, 2024), (1983, 2024))
SIDS = ("OPHNFB", "HCOMPBS", "IPDNBS", "PRS85006173", "CPIAUCSL", "CUUR0000SA0L2", "CPILEGSL", "CUUR0000SA0L5")


def build():
    return pd.DataFrame({s: m1_eras.annual(s) for s in SIDS})


def identity_gap(a):
    """max |log LS - log(HCOMPBS / (IPDNBS x OPHNFB)) - const| over 1948-2024: the BLS identity, to rounding."""
    r = np.log(a.PRS85006173) - np.log(a.HCOMPBS / (a.IPDNBS * a.OPHNFB))
    r = r.loc[1948:2024]
    return float((r - r.mean()).abs().max())


def split(a, y0, y1):
    d = lambda s: 100 * (np.log(s[y1]) - np.log(s[y0]))  # noqa: E731  (log points)
    out = dict(productivity=d(a.OPHNFB), real_pay_cpi=d(a.HCOMPBS / a.CPIAUCSL),
               real_pay_ex_shelter=d(a.HCOMPBS / a.CUUR0000SA0L2), product_wage=d(a.HCOMPBS / a.IPDNBS),
               share_term=-d(a.HCOMPBS / (a.IPDNBS * a.OPHNFB)), share_term_published=-d(a.PRS85006173),
               wedge_cpi=d(a.CPIAUCSL / a.IPDNBS),
               wedge_ex_shelter=d(a.CUUR0000SA0L2 / a.IPDNBS), wedge_ex_energy=d(a.CPILEGSL / a.IPDNBS),
               wedge_ex_medical=d(a.CUUR0000SA0L5 / a.IPDNBS))
    out["gap_cpi"] = out["productivity"] - out["real_pay_cpi"]
    out["split_residual"] = out["gap_cpi"] - out["share_term"] - out["wedge_cpi"]      # zero by construction
    out["removed_by_ex_shelter"] = 1 - out["wedge_ex_shelter"] / out["wedge_cpi"]
    out["removed_by_ex_energy"] = 1 - out["wedge_ex_energy"] / out["wedge_cpi"]
    out["removed_by_ex_medical"] = 1 - out["wedge_ex_medical"] / out["wedge_cpi"]
    rem = out["removed_by_ex_shelter"]
    out["verdict"] = ("supports" if out["wedge_cpi"] > 0 and rem >= 1 / 3 else
                      "counts against" if out["wedge_cpi"] <= 0 or rem <= 0.1 else "partial")
    out["wedge_share_of_gap"] = out["wedge_cpi"] / out["gap_cpi"]
    return out


# ------------------------------------------------------------------------------------------------------------ figure
rcParams.update({"font.family": "serif", "font.serif": ["DejaVu Serif"], "mathtext.fontset": "dejavuserif",
                 "pdf.fonttype": 42, "font.size": 8.5, "xtick.labelsize": 7.5, "ytick.labelsize": 7.5,
                 "axes.linewidth": 0.53, "xtick.major.width": 0.45, "ytick.major.width": 0.45,
                 "xtick.major.size": 2.3, "ytick.major.size": 2.3})
PRINT_W = 0.88 * 16 / 2.54
COLORS = ("#2a78d6", "#eb6834", "#1baf7a", "#eda100")
INK, MUTED, GRID = "#0b0b0b", "#52514e", "#e4e3df"


def draw(a, y0=1973, y1=2024):
    s = a.loc[y0:y1]
    lines = (("Output per hour", s.OPHNFB),
             ("Pay deflated by output prices", s.HCOMPBS / s.IPDNBS),
             ("Pay deflated by CPI less shelter", s.HCOMPBS / s.CUUR0000SA0L2),
             ("Pay deflated by the CPI", s.HCOMPBS / s.CPIAUCSL))
    fig, ax = plt.subplots(figsize=(PRINT_W, PRINT_W / 2.0), layout="constrained")
    ends = []
    for (name, v), c in zip(lines, COLORS):
        idx = 100 * v / v.iloc[0]
        ax.plot(idx.index, idx, color=c, lw=1.4, label=name)
        ends.append((idx.iloc[-1], name))
    ax.set_yscale("log")
    ax.set_yticks([100, 125, 150, 175, 200, 225, 250])
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{y:g}"))
    ax.yaxis.set_minor_formatter(plt.NullFormatter())
    ax.set_xlim(y0, y1 + 16)                    # room for the end labels; the axis itself stops at the data
    ax.set_xticks([1980, 1990, 2000, 2010, 2020])
    ax.spines["bottom"].set_bounds(y0, y1)
    for val, name in ends:                      # direct labels at the line ends, in ink
        ax.annotate(f"{name}", xy=(y1 + 0.6, val), ha="left", va="center", fontsize=6.8, color=INK)
    ax.set_ylabel(f"Index, {y0} = 100 (log scale)", fontsize=7.5)
    ax.grid(True, color=GRID, lw=0.5)
    for gl in ax.get_xgridlines() + ax.get_ygridlines():
        gl.set_clip_box(None)
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(colors=MUTED, labelcolor=INK)
    ax.legend(frameon=False, fontsize=6.8, loc="upper left", handlelength=1.6)
    out = ROOT / "paper" / "figures" / "fig_gap.png"
    fig.savefig(out, dpi=300)
    fig.savefig(out.with_suffix(".pdf"), metadata={"CreationDate": None})
    return out


if __name__ == "__main__":
    a = build()
    res = {"identity_max_dev": identity_gap(a), **{f"{y0}-{y1}": split(a, y0, y1) for y0, y1 in WINDOWS}}
    (ROOT / "data" / "m3_gap.json").write_text(json.dumps(res, indent=2, default=float))
    print(f"BLS identity, max deviation in logs over 1948-2024: {res['identity_max_dev']:.2e}")
    for w in WINDOWS:
        r = res[f"{w[0]}-{w[1]}"]
        print(f"--- {w[0]}-{w[1]} (log points): productivity {r['productivity']:.1f}, real pay (CPI) {r['real_pay_cpi']:.1f},"
              f" gap {r['gap_cpi']:.1f} = share {r['share_term']:.1f} + wedge {r['wedge_cpi']:.1f}"
              f" (wedge {100 * r['wedge_share_of_gap']:.0f}% of the gap; residual {r['split_residual']:.1e};"
              f" published share falls {r['share_term_published']:.1f})")
        print(f"    wedge with CPI less shelter {r['wedge_ex_shelter']:.1f}: removes {100 * r['removed_by_ex_shelter']:.0f}%"
              f" -> {r['verdict']} | less energy removes {100 * r['removed_by_ex_energy']:.0f}%,"
              f" less medical care {100 * r['removed_by_ex_medical']:.0f}%")
    print("wrote", draw(a))
