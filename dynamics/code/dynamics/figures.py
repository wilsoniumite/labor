# figures.py — the §8 figure set, regenerated from one entry point.
# Runs the gate, the validation ladder, and all four experiments (solve.py),
# then draws. Nothing here computes economics — every number is solve.py's.
#
# Run: ../venv/Scripts/python.exe code/dynamics/figures.py  (from dynamics/)

import os
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))                # dynamics/
sys.path.insert(0, HERE)
import solve  # noqa: E402

FIGDIR = os.path.join(os.path.dirname(os.path.dirname(HERE)), "figures")
GRID = dict(alpha=0.25, linewidth=0.6)


def save(fig, name):
    path = os.path.join(FIGDIR, name)
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  wrote {path}")


def fig_windfall(out, t1, Tshow=25):
    t = np.arange(Tshow)
    fig, ax = plt.subplots(1, 3, figsize=(12.5, 3.4))
    fig.subplots_adjust(wspace=0.28)
    ax[0].plot(t, out["pi"][:Tshow], color="tab:blue")
    ax[0].axhline(t1["pi_old"], color="gray", lw=0.8, ls=":")
    ax[0].axhline(t1["pi_new"], color="gray", lw=0.8, ls="--")
    ax[0].set_title("quasi-rent π$_t$ (rectangle, then user cost)")
    ax[0].annotate(f"Q$_0$ = {t1['Q0']:.3f}\nvs (1+ρ)$^{{J-1}}$ = {t1['Q_ss_benchmark']:.3f}",
                   xy=(0.42, 0.72), xycoords="axes fraction", fontsize=9)
    ax[1].plot(t, out["r"][:Tshow], color="tab:green")
    ax[1].axhline(t1["r_old"], color="gray", lw=0.8, ls=":")
    ax[1].axhline(t1["r_new"], color="gray", lw=0.8, ls="--")
    ax[1].set_title("land rent r$_t$")
    ax[2].plot(t, out["w"][:Tshow] / out["w"][0], color="tab:red", label="w/p (CM on the path)")
    wr = out["w"][:Tshow] / out["r"][:Tshow]
    ax[2].plot(t, wr / wr[0], color="tab:purple", label="w/r (the land claim)")
    ax[2].set_title("the wage, two numeraires (t=0 = 1)")
    ax[2].legend(fontsize=8, frameon=False)
    for a in ax:
        a.grid(**GRID)
        a.set_xlabel("t (periods after the γ̄ shock)")
    fig.suptitle("T1 — the windfall: an unanticipated γ̄ fall with build lag J = 3", y=1.03)
    save(fig, "fig_dyn_windfall.png")


def fig_waterfall(t2, Tshow=14):
    t = np.arange(Tshow)
    pi_c = np.array(t2["pi_c"][:Tshow]); pi_p = np.array(t2["pi_p"][:Tshow])
    r = np.array(t2["r"][:Tshow])
    fig, ax = plt.subplots(1, 2, figsize=(9.2, 3.4))
    ax[0].plot(t, pi_c / t2["pi_c_new"], marker="o", ms=3, color="tab:blue",
               label=f"J = {t2['J_c']} input (rent / its new SS rent)")
    ax[0].plot(t, pi_p / t2["pi_p_new"], marker="s", ms=3, color="tab:orange",
               label=f"J = {t2['J_p']} input")
    ax[0].axhline(1.0, color="gray", lw=0.8, ls="--")
    ax[0].axvspan(0, t2["J_c"], color="tab:blue", alpha=0.06)
    ax[0].axvspan(t2["J_c"], t2["J_p"], color="tab:orange", alpha=0.06)
    ax[0].set_title("rent / own new-SS rent, per input")
    ax[0].legend(fontsize=8, frameon=False)
    ax[1].plot(t, r, color="tab:green", marker="o", ms=3)
    ax[1].axhline(t2["r_old"], color="gray", lw=0.8, ls=":")
    ax[1].axhline(t2["r_new"], color="gray", lw=0.8, ls="--")
    ax[1].set_title("land rent: permanent holder from t ≈ J$_p$")
    for a in ax:
        a.grid(**GRID)
        a.set_xlabel("t")
    fig.suptitle("T2 — the waterfall: value passes through produced inputs in J-order", y=1.03)
    save(fig, "fig_dyn_waterfall.png")


def fig_speedlag(t3):
    speeds = ["fast (1 period)", "medium (4)", "slow (12)"]
    Js = [1, 2, 4]
    fig, ax = plt.subplots(figsize=(5.6, 3.6))
    xs = np.arange(len(speeds))
    for j, mk in zip(Js, ("o", "s", "^")):
        ys = [t3["windfall_pv"][f"J={j} | {s}"] for s in speeds]
        ax.plot(xs, ys, marker=mk, label=f"J = {j}")
    ax.set_xticks(xs, ["fast\n(1 period)", "medium\n(4)", "slow\n(12)"])
    ax.set_ylabel("PV of the windfall on capital in place")
    ax.set_title("T3 — transitional value to produced capital:\nspeed of the shock × gestation lag")
    ax.grid(**GRID)
    ax.legend(frameon=False, fontsize=9)
    save(fig, "fig_dyn_speedlag.png")


def fig_sloped(outs5, t5, Tshow=30):
    out_c, out_m = outs5
    t = np.arange(Tshow)
    fe = t5["frontier_extension"]
    fig, ax = plt.subplots(1, 2, figsize=(9.2, 3.4))
    ax[0].plot(t, out_c["w"][:Tshow], color="tab:red",
               label=f"frontier extension (cap {t5['cap']})")
    ax[0].plot(t, out_m["w"][:Tshow], color="tab:red", ls="--",
               label=f"efficiency deepening (×{t5['mult']})")
    ax[0].axhline(fe["w_goods_old"], color="gray", lw=0.8, ls=":")
    ax[0].set_title("goods wage w$_t$: falls at RELEASE and is pinned\nby the cap; rises under deepening")
    ax[0].legend(fontsize=8, frameon=False)
    ax[1].plot(t, out_c["w"][:Tshow] / out_c["r"][:Tshow], color="tab:purple",
               label="frontier extension")
    ax[1].plot(t, out_m["w"][:Tshow] / out_m["r"][:Tshow], color="tab:purple", ls="--",
               label="efficiency deepening")
    ax[1].axhline(fe["w_over_r_old"], color="gray", lw=0.8, ls=":")
    ax[1].set_title("the land claim w$_t$/r$_t$: falls with the BUILDOUT\nunder both shocks")
    ax[1].legend(fontsize=8, frameon=False)
    for a in ax:
        a.grid(**GRID)
        a.set_xlabel("t (periods after the schedule shock)")
    fig.suptitle("T5 — sloped case: which shock moves the wage, and in which numeraire", y=1.06)
    save(fig, "fig_dyn_sloped.png")


if __name__ == "__main__":
    res = solve.run_all()
    print("\ndrawing …")
    out1, t1 = res["T1"]
    fig_windfall(out1, t1)
    fig_waterfall(res["T2"])
    fig_speedlag(res["T3"])
    fig_sloped(res["T5"][0], res["T5"][1])
    print("done — all four §8 figures regenerated from one entry point.")
