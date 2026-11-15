# latent.py — the complete schedule's fourth category: latent goods, services nobody supplies because no buyer values
# them at cost, and reinstatement as a latent good switching on.
#
# A latent service j is one task with relative human productivity gamma_j and a reservation value R_j (baskets). Its
# cheapest route costs min(w, p_m gamma_j) (labor, or machines), so in units normalized by the margin,
#   g = gamma_j / gamma(x*)  and  rho = R_j P_s / w:   viable iff rho >= min(1, g);  labor-assigned iff g > 1.
# The two triggers of the session's discussion: freed labor (w falls against R: points with g > 1 cross rho = 1, which
# is reinstatement) and complementarity / cheaper machines (p_m gamma_j falls: points with g < 1 cross rho = g, which
# switch on already automated). General-purpose automation also moves latent points left (gamma_j falls with eta).
#
# Partial equilibrium on Appendix B's automation path (lambda 0, gamma x eta) at the calibrated members: prices from
# the equilibrium, the reservoir fixed (no invention), reservation values fixed in baskets, each latent service bought
# in the same small quantity once viable. Two reservoirs (latent tasks like the economy's tasks, or like labor's
# current tasks) x two automation reaches (latent tasks untouched by eta, or improved with everything else).
# Run from walls/:  python code/latent.py
import json
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import model as m  # noqa: E402

rcParams["font.family"] = "serif"
rcParams["font.serif"] = ["DejaVu Serif", "Georgia"]
rcParams["mathtext.fontset"] = "dejavuserif"
rcParams["font.size"] = 8.5
NAVY, BLUE, RED, GRAY, BROWN = "#1a1a3d", "#4878b8", "#8b2020", "#9a9a9a", "#8a6d3b"
X = m.margin_from_targets()
RNG = np.random.default_rng(20261116)


def member(sigma):
    k = brentq(lambda kk: m.sigma_margin(m.calibrate(m.power_family(kk)), X) - sigma, 3.95, 400.0, xtol=1e-8)
    return m.calibrate(m.power_family(k))


def path_prices(P, etas):
    """Equilibrium prices and incomes along Appendix B's path; interest = rho V_m X with V_m = p_m/(rho + delta)."""
    out = []
    for eta in etas:
        Q = {**P, "lam": 0.0, "sched": m.scaled(P["sched"], eta)}
        e = m.solve(Q)
        interest = Q["rho"] * e["pm"] / m.cpt(Q) * e["X"]
        income = e["v"] * e["n"] + Q["T"] + interest
        out.append(dict(eta=eta, w=e["v"], pm=e["pm"], Ps=e["Ps"], gstar=e["v"] / e["pm"], x=e["x"],
                        n=e["n"], wage_share=e["v"] * e["n"] / income, real_wage=e["real_wage"]))
    return out


def reservoir(P, flavor, n=40_000):
    """Latent tasks' base gammas: like the economy's tasks (positions uniform on [0, 1]) or like labor's current tasks
    (positions uniform on [x*, 1]); each latent service a random distance u in (0, 1) of the way to viability at the
    path's start, R_j = u_j min(w, p_m gamma_j)/P_s there."""
    lo = 0.0 if flavor == "like the economy" else X
    pos = RNG.uniform(lo, 1.0, n)
    return P["sched"]["g"](pos), RNG.uniform(0.0, 1.0, n)


def activation(prices, gam, u, reach):
    p0 = prices[0]
    R = u * np.minimum(p0["w"], p0["pm"] * gam) / p0["Ps"]
    rows = []
    for p in prices:
        gj = gam * (p["eta"] if reach == "general purpose" else 1.0)
        cost = np.minimum(p["w"], p["pm"] * gj)
        on = R * p["Ps"] >= cost
        labor = on & (gj > p["gstar"])
        rows.append(dict(eta=p["eta"], active=on.mean(), labor=labor.mean(),
                         labor_share_of_active=labor.sum() / max(on.sum(), 1)))
    return rows


if __name__ == "__main__":
    etas = np.geomspace(1.0, 0.01, 41)
    record = {}
    for name, sig in (("sigma 0.6", 0.6), ("low root (sigma 2.29)", 2.2932)):
        P = member(sig)
        prices = path_prices(P, etas)
        record[name] = dict(prices=prices)
        print(f"--- {name}: along the path w/P_s {prices[0]['real_wage']:.2f} -> {prices[-1]['real_wage']:.2f}, wage "
              f"share of income {prices[0]['wage_share']:.2f} -> {prices[-1]['wage_share']:.2f}")
        for flavor in ("like the economy", "like labor's tasks"):
            gam, u = reservoir(P, flavor)
            for reach in ("untouched", "general purpose"):
                rows = activation(prices, gam, u, reach)
                record[name][f"{flavor} / {reach}"] = rows
                pick = [rows[i] for i in (10, 20, 30, 40)]
                print(f"    {flavor:18s} {reach:15s}: " + "; ".join(
                    f"eta {r['eta']:.2g}: {r['active']:.2f} on, {r['labor']:.2f} with labor"
                    f" ({r['labor_share_of_active']:.0%})" for r in pick))
    json.dump(record, open(HERE.parent / "results" / "latent.json", "w"), indent=1, default=float)

    # ---------------------------------------------------------------- figure: the switch-on plane and the path
    fig, axs = plt.subplots(1, 2, figsize=(0.88 * 16 / 2.54 * 1.3, 3.1), layout="constrained")
    ax = axs[0]
    g = np.geomspace(0.05, 20, 400)
    ax.fill_between(g, np.minimum(1, g), 3.0, color=BLUE, alpha=0.10, lw=0)
    ax.plot(g, np.minimum(1, g), color=NAVY, lw=1.6)
    ax.axvline(1.0, color="#666666", lw=0.6, ls=":")
    ax.annotate("produced", xy=(0.07, 1.9), fontsize=8, color=NAVY)
    ax.annotate("latent: no buyer at cost", xy=(5.0, 0.15), fontsize=8, color="#555555", ha="center")
    ax.annotate("machines would\ndo it", xy=(0.11, 0.55), fontsize=7.5, color="#555555")
    ax.annotate("people would\ndo it", xy=(1.35, 1.35), fontsize=7.5, color="#555555")
    ax.annotate("", xy=(6.0, 1.15), xytext=(6.0, 0.55), arrowprops=dict(arrowstyle="-|>", color=RED, lw=1.1))
    ax.annotate("freed labor: w falls\nagainst R, so it switches\non with people", xy=(5.6, 0.36), fontsize=7,
                color=RED, ha="center")
    ax.annotate("", xy=(0.28, 0.22), xytext=(0.75, 0.22), arrowprops=dict(arrowstyle="-|>", color=BROWN, lw=1.1))
    ax.annotate("machines get better at it\nwhile it is still latent:\nborn automated", xy=(0.42, 0.10),
                fontsize=7, color=BROWN, ha="center")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(0.05, 20)
    ax.set_ylim(0.05, 3.0)
    ax.set_xlabel(r"latent task's $\gamma_j$ over the margin's, $\gamma_j/\gamma(x^*)$")
    ax.set_ylabel(r"reservation value over the wage, $R_jP_s/w$")
    ax.set_title("(a) When a latent good switches on", loc="left", fontsize=8.5, color="#333333")
    ax.grid(alpha=0.25, lw=0.33)
    ax.spines[["top", "right"]].set_visible(False)
    ax = axs[1]
    rec = record["sigma 0.6"]
    et = [r["eta"] for r in rec["like labor's tasks / untouched"]]
    un = rec["like labor's tasks / untouched"]
    gp = rec["like labor's tasks / general purpose"]
    ax.plot(et, [r["labor"] for r in un], color=RED, lw=1.5, label="AI can't touch them: switched on, with people")
    ax.plot(et, [r["labor"] for r in gp], color=NAVY, lw=1.5, label="improved with everything: switched on, with people")
    ax.plot(et, [r["active"] - r["labor"] for r in gp], color=NAVY, lw=1.3, ls="--",
            label="improved with everything: switched on, born automated")
    ax2 = ax.twinx()
    ax2.plot(et, [p["wage_share"] for p in rec["prices"]], color=GRAY, lw=1.0, ls=":")
    ax2.set_ylim(0, 1.02)
    ax2.set_ylabel("wage share of income (dotted)", color="#777777", fontsize=7.5)
    ax2.tick_params(axis="y", colors="#777777", labelsize=7)
    ax2.spines[["top"]].set_visible(False)
    ax.set_xscale("log")
    ax.set_xlim(1.0, 0.01)
    ax.set_ylim(0, 1.02)
    ax.set_xlabel(r"Appendix B's automation path: $\gamma\times\eta$, $\widetilde\lambda_m = 0$")
    ax.set_ylabel("share of the latent reservoir\n(tasks like labor's current ones)")
    ax.legend(loc="upper left", fontsize=6.6, frameon=False)
    ax.set_title(r"(b) Along the path, at $\sigma = 0.6$", loc="left", fontsize=8.5, color="#333333")
    ax.grid(alpha=0.25, lw=0.33)
    ax.spines[["top"]].set_visible(False)
    fig.savefig(HERE.parent / "figures" / "latent.png", dpi=200)
    print("wrote figures/latent.png and results/latent.json")
