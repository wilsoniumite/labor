# record_plot.py — the record-set fit by eye (2026-11-06): the six targets and the machine chain's share of pay (not
# targeted), the record against the two-good main case (results/fit_Bd.json) and the record-set fit (set_from_record.py
# D2, its best from record_starts.py) with and without the 1948 wave. Writes playground/record_case.png.
# Run from us-record/:  python3 playground/record_plot.py
import json
import sys

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker as mt  # noqa: E402

sys.path.insert(0, "code")
sys.path.insert(0, "playground")
import fit_base as F  # noqa: E402
import record_case as RC  # noqa: E402  (BASE, NOWAVE; sets land in use growing with adults)

INK, MUTED, GRID, SURFACE = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
C_MAIN, C_REC, C_NOWAVE = "#2a78d6", "#eb6834", "#1baf7a"          # categorical slots 1-3 (validated, all pairs)
Y = np.array(F.YEARS)
BUN = json.load(open("../paths/results/chains.json"))["bundles"]["equipment_ipp_structures"]
CHAIN = np.array([BUN[str(y)]["comp_share_of_total_comp_domp"] if str(y) in BUN else np.nan for y in F.YEARS])


def path(meta, par):
    F.configure(meta)
    return F.model_path(par)


if __name__ == "__main__":
    R = json.load(open("results/fit_Bd.json"))
    RS = json.load(open("playground/record_starts.json"))["fits"]
    wave = min([r for r in RS if r["group"] == "starts" and r["misfit"] < 10], key=lambda r: r["misfit"])
    nowave = min([r for r in RS if r["group"] == "wave" and r["misfit"] < 10], key=lambda r: r["misfit"])
    F.configure(R["meta"])
    record = {s: F.target(s).values for s in ["wage_goods", "wage_shelter", "wage_durables", "labour_share_c",
                                               "prime_emp_rate", "theta_V"]}
    cases = [("Main case (two goods, return 2%)", C_MAIN, "-", path(R["meta"], R["best"]["par"]), R["best"]["misfit"]),
             ("Set from the record, with the wave", C_REC, "-", path(RC.BASE, wave["par"]), wave["misfit"]),
             ("Set from the record, without the wave", C_NOWAVE, (0, (4, 2)), path(RC.NOWAVE, nowave["par"]), nowave["misfit"])]
    panels = [("wage_goods", "Wage over goods (all but shelter)", True), ("wage_shelter", "Wage over shelter", True),
              ("wage_durables", "Wage over durables", True), ("labour_share_c", "Labour's share", False),
              ("prime_emp_rate", "Prime-age employment rate", False), ("theta_V", "Pay's share of a machine's cost", False),
              ("chain_share", "Machine chain's share of pay (not targeted)", False)]
    plt.rcParams.update({"font.size": 9, "axes.edgecolor": MUTED, "axes.labelcolor": MUTED, "xtick.color": MUTED,
                         "ytick.color": MUTED, "axes.titlesize": 10, "axes.titlecolor": INK, "font.family": "DejaVu Sans"})
    fig, axes = plt.subplots(2, 4, figsize=(15, 7.2), facecolor=SURFACE)
    for ax, (key, title, log) in zip(axes.flat, panels):
        ax.set_facecolor(SURFACE)
        rec = CHAIN if key == "chain_share" else record[key]
        ok = ~np.isnan(rec)
        ax.plot(Y[ok], rec[ok], color=INK, lw=0, marker="o", ms=2.6, label="Record", zorder=3)
        for label, color, ls, m, _ in cases:
            ax.plot(Y, m[key].values, color=color, lw=2, ls=ls, label=label, zorder=2)
        if log:
            ax.set_yscale("log")
            plain = mt.FuncFormatter(lambda v, _: f"{v:.0f}")
            ax.yaxis.set_major_formatter(plain)
            ax.yaxis.set_minor_formatter(plain)
        ax.set_title(title, loc="left")
        ax.grid(True, color=GRID, lw=0.6)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
        ax.set_xlim(1948, 2026)
    leg = axes.flat[7]
    leg.axis("off")
    handles, labels = axes.flat[0].get_legend_handles_labels()
    labels = [lab if lab == "Record" else f"{lab}: {c[4]:.2f}" for lab, c in zip(labels, [None] + cases)]
    leg.legend(handles, labels, loc="upper left", frameon=False, fontsize=9, title="Six-target misfit", title_fontsize=9,
               alignment="left")
    leg.text(0.0, 0.32, "Set from the record: the return 8% (NIPA's split),\nimported content 20% of a machine's cost,\n"
             "land in use growing with adults.\nWages are indices over their price; log scale.",
             transform=leg.transAxes, fontsize=8.5, color=MUTED, va="top")
    fig.suptitle("The US record, 1950-2024: the main case and the fit set from the record", x=0.01, ha="left",
                 fontsize=12, color=INK)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig("playground/record_case.png", dpi=200, facecolor=SURFACE)
    print("playground/record_case.png written")
