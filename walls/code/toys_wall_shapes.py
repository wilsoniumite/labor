# asymptote_toys.py — scratch mock-ups for the pinning paper's schedule figures (not part of the paper).
# 1. Figure 1 three ways: as printed (finite top, jump), an asymptote at the wall, a curve that bends up to a finite top.
# 2. Figure 4 with asymptotic schedules: every dot becomes an interior margin, so every trained worker needs a schedule.
# 3. Where the model itself has an asymptote: the schedule in rent units through equation (5), v = g b/(1 - g lam),
#    which blows up where g lam = 1 (the machine chain's ceiling), and Appendix B's printed economy, whose ceiling is 0.946.
# Run from walls/:  python code/toys_wall_shapes.py
import sys
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.lines import Line2D

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "pinning" / "code"))
import appendix_b as ab  # noqa: E402

rcParams["font.family"] = "serif"
rcParams["font.serif"] = ["DejaVu Serif", "Georgia"]
rcParams["mathtext.fontset"] = "dejavuserif"
rcParams["font.size"] = 8.5
rcParams["xtick.labelsize"] = rcParams["ytick.labelsize"] = 8
rcParams["axes.linewidth"] = 0.52
for _ax in ("xtick", "ytick"):
    rcParams[f"{_ax}.major.width"] = 0.52
    rcParams[f"{_ax}.major.size"] = 2.3

PRINT_W = 0.88 * 16 / 2.54
NAVY, BLUE, RED, GRAY, BROWN = "#1a1a3d", "#4878b8", "#8b2020", "#c8c8c8", "#8a6d3b"


def grid(m, n=4000):
    """Points on [0, m), packed toward m so a curve with an asymptote at m draws smoothly."""
    s = np.linspace(0, 1, n, endpoint=False)
    return m * (1 - (1 - s) ** 3)


def tail(u, c, eta=0.0):
    """c (1/(1 - u + eta) - 1/(1 + eta)): zero at u = 0; an asymptote at u = 1 when eta = 0, a finite top otherwise."""
    return c * (1 / (1 - u + eta) - 1 / (1 + eta))


# ------------------------------------------------------------------ 1. Figure 1 three ways
M, YTOP, WC, W_HI = 0.70, 5.2, 2.0, 4.6        # wall, chart top, the printed w/p_m, a higher w/p_m
XSTAR = M * ((WC - 0.4) / 3.6) ** (1 / 1.8)    # the printed margin, 0.447; every variant keeps it


def g_printed(x):
    return 0.4 + 3.6 * (x / M) ** 1.8


def g_asymptote(x, c=0.04):
    """The printed body plus a hyperbolic tail with an asymptote at the wall; through (x*, 2.0)."""
    us = XSTAR / M
    b = (WC - 0.4 - tail(us, c)) / us ** 1.8
    return 0.4 + b * (x / M) ** 1.8 + tail(x / M, c)


def g_bent(x, top=4.0, k=1.3, eta=0.03):
    """A flatter body and a tail that bends up hard near the wall but stops at a finite top; through (x*, 2.0)."""
    us = XSTAR / M
    b, c = np.linalg.solve([[1.0, tail(1.0, 1.0, eta)], [us ** k, tail(us, 1.0, eta)]], [top - 0.4, WC - 0.4])
    return 0.4 + b * (x / M) ** k + tail(x / M, c, eta)


def fig1_panel(ax, g, title, kind):
    xs = grid(M)
    ys = g(xs)
    assert np.all(np.diff(ys) > 0)
    top = float(g(M)) if kind != "asymptote" else np.inf
    xstar = float(np.interp(WC, ys, xs))
    assert abs(xstar - XSTAR) < 1e-6
    yc = np.minimum(ys, YTOP + 1)
    ax.plot(xs, yc, color=NAVY, lw=1.7, zorder=3)
    if kind == "asymptote":
        ax.plot([M, M], [0, YTOP], color=NAVY, lw=0.8, ls=(0, (4, 2.5)), zorder=2)   # the wall is the asymptote
    else:
        ax.annotate("", xy=(M, YTOP), xytext=(M, top),
                    arrowprops=dict(arrowstyle="-|>", color=NAVY, lw=1.05, ls="--",
                                    shrinkA=0, shrinkB=0, mutation_scale=7.8))
    ax.axhline(WC, color=RED, lw=1.05, ls="--")
    ax.axvline(xstar, color="#666666", lw=0.65, ls=":")
    ax.fill_between(xs, 0, yc, where=xs <= xstar, color=GRAY, alpha=0.35, lw=0)
    ax.fill_between(xs, 0, yc, where=xs >= xstar, color=BLUE, alpha=0.18, lw=0)
    ax.axvspan(M, 1.0, color=BLUE, alpha=0.10, lw=0)
    # a higher wage ratio: above a finite top it meets the wall; under an asymptote it still meets the curve
    ax.axhline(W_HI, color=RED, lw=0.8, ls=":")
    ax.annotate(r"higher $w/p_m$", xy=(0.025, W_HI + 0.12), color=RED, fontsize=7.5)
    if kind == "asymptote":
        xh = float(np.interp(W_HI, ys, xs))
        ax.plot(xh, W_HI, "o", ms=4.3, color=RED, zorder=5)
        ax.annotate(f"still an interior margin,\nat $x$ = {xh:.3f}", xy=(xh, W_HI), xytext=(0.47, 3.55),
                    fontsize=7.5, color=RED, ha="center", va="top",
                    arrowprops=dict(arrowstyle="->", color=RED, lw=0.59, mutation_scale=5.8, shrinkB=3))
    else:
        ax.plot(M, W_HI, "o", ms=4.6, mfc="white", mec=RED, mew=1.1, zorder=5)
        ax.annotate("labor holds\nonly $H$", xy=(M, W_HI), xytext=(0.535, 4.25), fontsize=7.5, color=RED,
                    ha="center", va="top",
                    arrowprops=dict(arrowstyle="->", color=RED, lw=0.59, mutation_scale=5.8, shrinkB=3))
    if kind == "bent":   # the band of wage ratios at which labor holds only H, marked on the wall
        ax.plot([M + 0.007] * 2, [top, YTOP], color=RED, lw=3.2, alpha=0.30, solid_capstyle="butt", zorder=1)
    ax.annotate("$w/p_m$", xy=(0.025, WC + 0.12), color=RED, fontsize=8)
    ax.annotate("$x^*$", xy=(xstar + 0.008, 0.18), color="#444444", fontsize=8)
    ax.annotate(r"Machines: $\gamma(x) < w/p_m$", xy=(0.235, 0.16), ha="center", fontsize=8, color="#555555")
    ax.annotate(r"Labor: $\gamma(x) > w/p_m$", xy=(0.575, 0.95), ha="center", fontsize=8, color=NAVY)
    ax.annotate("$H$: tasks closed\nto machines", xy=(0.85, 2.55), ha="center", fontsize=8, color="#555555")
    ax.set_title(title, loc="left", fontsize=8.5, color="#333333")
    ax.set_xlabel(r"Tasks $x$, ordered by increasing $\gamma$; closed tasks last")
    ax.set_ylabel(r"Relative human productivity $\gamma(x)$")
    ax.set_xlim(0, 1.0)
    ax.set_ylim(0, YTOP)
    ax.grid(alpha=0.25, lw=0.33)
    ax.spines[["top", "right"]].set_visible(False)
    return top


fig, axs = plt.subplots(3, 1, figsize=(PRINT_W, 3 * (PRINT_W / 1.894 + 0.22)), layout="constrained")
fig1_panel(axs[0], g_printed, "(a) As printed: the schedule stops at a finite top, then γ jumps to ∞", "printed")
fig1_panel(axs[1], g_asymptote, "(b) Asymptote: γ → ∞ as x approaches the wall", "asymptote")
top_b = fig1_panel(axs[2], g_bent, "(c) Bending up to a finite top; the band above it marked", "bent")
fig.savefig(HERE.parent / "figures" / "toy_fig1_variants.png", dpi=200)
plt.close(fig)
print("1. wrote toy_fig1_variants.png")

# ------------------------------------------------------------------ 2. Figure 4 with asymptotes
# The printed eras (code/fig_eras_workers.py), each schedule given a hyperbolic tail with an asymptote at its wall.
# No dot can stand on a wall above a schedule's top any more, so each trained worker gets a schedule of their own
# (dashed), weakly above the entrant's, and both dots are interior margins.
YTOP4 = 3.4
COLOR = {"pre": BROWN, "ind": NAVY, "comp": BLUE, "ai": RED}
ERAS = [  # key, wall, printed body, entrant w/p_m, trained w/p_m, trained body (scale of the entrant's, or the AI one)
    ("pre", 0.06, lambda x: 0.03 + 0.5 * (x / 0.06) ** 3, 1.5, 1.9, None),
    ("ind", 0.45, lambda x: 0.02 + 2.5 * (x / 0.45) ** 2.5, 1.5, 2.85, None),
    ("comp", 0.75, lambda x: 0.008 + 1.70 * (x / 0.75) ** 1.65, 0.93, 2.0, None),
    ("ai", 0.94, lambda x: 0.004 + 1.25 * (x / 0.94) ** 1.50, 0.80, 1.10, lambda x: 0.004 + 1.60 * (x / 0.94) ** 1.45),
]
C_TAIL, TRAINED_SCALE = 0.012, 1.15

fig, ax = plt.subplots(figsize=(PRINT_W, 3.6), layout="constrained")
prev = None
for key, m, body, we, wt, tbody in ERAS:
    xs = grid(m)
    ye = body(xs) + tail(xs / m, C_TAIL)
    yt = (tbody(xs) if tbody else TRAINED_SCALE * body(xs)) + tail(xs / m, 1.5 * C_TAIL)
    assert np.all(np.diff(ye) > 0) and np.all(np.diff(yt) > 0) and np.all(yt >= ye)
    if prev is not None:   # nesting: each era's schedule weakly below the previous one where both are open
        pm, pxs, pys = prev
        common = xs < pm
        assert np.all(ye[common] <= np.interp(xs[common], pxs, pys) + 1e-9), key
    prev = (m, xs, ye)
    col = COLOR[key]
    ax.plot(xs, np.minimum(ye, YTOP4 + 1), color=col, lw=1.58)
    ax.plot(xs, np.minimum(yt, YTOP4 + 1), color=col, lw=1.1, ls=(0, (4, 1.6)))
    ax.plot([m, m], [0, YTOP4], color=col, lw=0.7, ls=(0, (2, 2)), alpha=0.8)
    xe, xt = float(np.interp(we, ye, xs)), float(np.interp(wt, yt, xs))
    ax.plot(xe, we, "o", ms=4.3, color=col, zorder=5)
    ax.plot(xt, wt, "o", ms=4.6, mfc="white", mec=col, mew=1.1, zorder=5)
    print(f"   {key}: wall {m}, entrant x* {xe:.4f} (w/p_m {we}), trained x* {xt:.4f} (w/p_m {wt}); "
          f"trained margin {m - xt:.4f} short of the wall")
ax.set_xlim(-0.02, 1.04)
ax.set_ylim(0, YTOP4)
ax.set_xlabel(r"Tasks $x$, each schedule ordered by its worker's $\gamma$; closed tasks last")
ax.set_ylabel(r"Relative human productivity $\gamma(x)$")
ax.grid(alpha=0.25, lw=0.33)
ax.spines[["top", "right"]].set_visible(False)
ax.set_title("Figure 4 with asymptotes: every dot is now an interior margin, and each trained worker\n"
             "needs a schedule of their own (dashed) in every era; nothing can sit on a wall",
             loc="left", fontsize=8, color="#333333")
era = [Line2D([], [], color=COLOR[k], lw=1.58) for k in COLOR]
keys = [Line2D([], [], color="0.3", marker="o", ls="none", ms=4.3),
        Line2D([], [], mec="0.3", mfc="white", marker="o", ls="none", ms=4.6, mew=1.1),
        Line2D([], [], color="0.3", lw=1.1, ls=(0, (4, 1.6)))]
blank = Line2D([], [], ls="none")
fig.legend([era[0], era[2], blank, era[1], era[3], blank] + keys,
           ["pre-industrial (to about 1780)", "computing (1970–2020)", "", "industrial (1780–1950)", "candidate AI", "",
            "entrant", "trained worker", "trained worker's schedule"],
           loc="outside lower center", ncol=3, fontsize=7.5, framealpha=0.95, handlelength=1.8, handletextpad=0.5,
           columnspacing=1.2)
fig.savefig(HERE.parent / "figures" / "toy_fig4_asymptotes.png", dpi=200)
plt.close(fig)
print("2. wrote toy_fig4_asymptotes.png")

# ------------------------------------------------------------------ 3. the model's own asymptote: rent units
# Equation (5) maps the schedule into the wage-rent ratio at which labor and machines tie at each task,
# v(x) = gamma(x) b_m / (1 - gamma(x) lam_m). With labor in the machine chain it blows up at x_c, where
# gamma(x_c) lam_m = 1: tasks beyond are closed to machines at every wage. With lam_m = 0 it is gamma(x) b_m.
LAM, B = 0.3, 1.0                               # Figure 2's full-chain labor and land in a machine-hour
XC = M * ((1 / LAM - 0.4) / 3.6) ** (1 / 1.8)  # g_printed(XC) = 1/LAM
VTOP = 30.0

fig, axs = plt.subplots(2, 1, figsize=(PRINT_W, 2 * (PRINT_W / 1.894 + 0.3)), layout="constrained")
ax = axs[0]
xs = grid(XC)
v = g_printed(xs) * B / (1 - g_printed(xs) * LAM)
ax.plot(xs, np.minimum(v, VTOP + 1), color=NAVY, lw=1.7, label=r"$\widetilde{\lambda}_m = 0.3$")
ax.plot([XC, XC], [0, VTOP], color=NAVY, lw=0.8, ls=(0, (4, 2.5)))
x0 = grid(M)
ax.plot(x0, g_printed(x0) * B, color=BLUE, lw=1.46, label=r"$\widetilde{\lambda}_m = 0$ (machines made by machines)")
ax.annotate("", xy=(M, VTOP), xytext=(M, float(g_printed(M))),
            arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.0, ls="--", shrinkA=0, shrinkB=0, mutation_scale=7.8))
ax.axvspan(XC, M, color=NAVY, alpha=0.07, lw=0)
ax.axvspan(M, 1.0, color=BLUE, alpha=0.10, lw=0)
ax.annotate("closed by the\nmachine chain when\n$\\widetilde{\\lambda}_m$ = 0.3 ($\\gamma\\widetilde{\\lambda}_m \\geq 1$)",
            xy=((XC + M) / 2, 21.0), xytext=(0.99, 23.5), ha="right", va="center", fontsize=7, color=NAVY,
            arrowprops=dict(arrowstyle="->", color=NAVY, lw=0.59, mutation_scale=5.8))
ax.annotate("$x_c$", xy=(XC + 0.006, 0.9), fontsize=8, color=NAVY)
ax.annotate("$H$: tasks closed\nto machines", xy=(0.85, 12.0), ha="center", fontsize=8, color="#555555")
ax.set_title("(a) Figure 1's schedule in rent units through equation (5), Figure 2's two chains",
             loc="left", fontsize=8.5, color="#333333")
ax.set_ylabel(r"$w/r$ at which labor and machines tie")
ax.set_xlabel(r"Tasks $x$, ordered by increasing $\gamma$; closed tasks last")
ax.legend(loc="upper left", frameon=False, fontsize=7.5)
ax.set_xlim(0, 1.0)
ax.set_ylim(0, VTOP)
ax.grid(alpha=0.25, lw=0.33)
ax.spines[["top", "right"]].set_visible(False)

ax = axs[1]
P = ab.PRINTED
q = ab.solve(P)
xc = q["x_ceiling"]
xs = grid(xc)
cpt = P["rho"] + P["delta"]
v = ab.gamma(P, xs) * cpt * P["b"] / ab.denominator(P, xs)
VTOP_B = 0.5
ax.plot(xs, np.minimum(v, VTOP_B + 1), color=NAVY, lw=1.7)
ax.plot([xc, xc], [0, VTOP_B], color=NAVY, lw=0.8, ls=(0, (4, 2.5)))
ax.axvspan(xc, 1.0, color=NAVY, alpha=0.07, lw=0)
ax.axhline(q["v"], color=RED, lw=1.05, ls="--")
ax.axvline(q["x"], color="#666666", lw=0.65, ls=":")
ax.annotate("$w/r$", xy=(0.02, q["v"] + 0.012), color=RED, fontsize=8)
ax.annotate(f"$x^*$ = {q['x']:.3f}", xy=(q["x"] - 0.008, 0.40), ha="right", color="#444444", fontsize=8)
ax.annotate(f"$x_c$ = {xc:.3f}: tasks beyond are\nclosed to machines at every wage", xy=(xc, 0.33), xytext=(0.60, 0.33),
            ha="center", va="center", fontsize=7.5, color=NAVY,
            arrowprops=dict(arrowstyle="->", color=NAVY, lw=0.59, mutation_scale=5.8))
ax.set_title("(b) Appendix B's printed economy in rent units: its only wall is this asymptote",
             loc="left", fontsize=8.5, color="#333333")
ax.set_ylabel(r"$w/r$ at which labor and machines tie")
ax.set_xlabel(r"Tasks $x$, ordered by increasing $\gamma$")
ax.set_xlim(0, 1.0)
ax.set_ylim(0, VTOP_B)
ax.grid(alpha=0.25, lw=0.33)
ax.spines[["top", "right"]].set_visible(False)
fig.savefig(HERE.parent / "figures" / "toy_rent_units.png", dpi=200)
plt.close(fig)
gc = (1 / cpt - P["a"]) / P["lam"]
print(f"3. wrote toy_rent_units.png; Figure 1 + lam 0.3: x_c = {XC:.4f}; Appendix B: x* = {q['x']:.5f}, "
      f"w/r = {q['v']:.5f}, x_c = {xc:.5f}, gamma(x_c) = {gc:.4f} (the cap on w/p_m), gamma(x*) = {q['gamma']:.4f}")

# ------------------------------------------------------------------ 4. what the asymptote changes, in a toy equilibrium
# One good, Y = A/p (unit-elastic demand), N hours supplied inelastically, gamma_L = 1, the rental p_m given:
#   p = w (1 - x*) + p_m J(x*),  N = Y (1 - x*),  w = p_m gamma(x*) at an interior margin;
#   labor holding only H (finite top only): x* = M, w = (p - p_m J(M)) / (1 - M) with p = A (1 - M) / N.
# The response of the wage to the machine rental, d ln w / d ln p_m, as labor gets scarcer.
from scipy.optimize import brentq  # noqa: E402

A_DEM, C_ASY = 1.0, 0.04
_us = XSTAR / M
_b_asy = (WC - 0.4 - tail(_us, C_ASY)) / _us ** 1.8
J_printed = lambda x: 0.4 * x + 3.6 * M * (x / M) ** 2.8 / 2.8                     # noqa: E731
J_asymptote = lambda x: (0.4 * x + _b_asy * M * (x / M) ** 2.8 / 2.8               # noqa: E731
                         + C_ASY * (-M * np.log(1 - x / M) - x))


def toy_wage(g, J, N, pm, asym):
    f = lambda x: pm * (g(x) + J(x) / (1 - x)) - A_DEM / N                            # noqa: E731
    if asym or f(M) >= 0:
        x = brentq(f, 0.0, M * (1 - 1e-15) if asym else M, xtol=1e-16)
        return pm * g(x), x, False
    return (A_DEM * (1 - M) / N - pm * J(M)) / (1 - M), M, True


def passthrough(g, J, N, asym, h=1e-4):
    w0, x0, only_h = toy_wage(g, J, N, 1.0, asym)
    w1, _, _ = toy_wage(g, J, N, 1.0 + h, asym)
    return np.log(w1 / w0) / np.log1p(h), x0, only_h


Ns = np.geomspace(0.6, 0.02, 600)
jump = [passthrough(g_printed, J_printed, n, False) for n in Ns]
asym = [passthrough(g_asymptote, J_asymptote, n, True) for n in Ns]
pt_j, onlyH = np.array([r[0] for r in jump]), np.array([r[2] for r in jump])
pt_a = np.array([r[0] for r in asym])
N_SWITCH = A_DEM / (4.0 + J_printed(M) / (1 - M))       # where labor starts holding only H under the jump
for n in (0.3, 0.15, 0.12, 0.09, 0.06, 0.04, 0.02):
    i = int(np.argmin(abs(Ns - n)))
    print(f"   N {Ns[i]:.3f}: jump {pt_j[i]:+.3f}{' (only H)' if onlyH[i] else ''}, asymptote {pt_a[i]:+.3f}")

fig, ax = plt.subplots(figsize=(PRINT_W, PRINT_W / 1.894), layout="constrained")
ax.axvspan(Ns.min(), N_SWITCH, color=BLUE, alpha=0.10, lw=0)
ax.axhline(0, color="#888888", lw=0.6)
ax.plot(Ns[~onlyH], pt_j[~onlyH], color=NAVY, lw=1.6, label="finite top, jump at the wall (as printed)")
ax.plot(Ns[onlyH], pt_j[onlyH], color=NAVY, lw=1.6)
ax.plot([N_SWITCH] * 2, [pt_j[~onlyH][-1], pt_j[onlyH][0]], color=NAVY, lw=0.7, ls=":")
ax.plot(Ns, pt_a, color=RED, lw=1.4, ls=(0, (5, 2)), label="asymptote at the wall")
ax.annotate("jump version:\nlabor holds only $H$", xy=(0.075, 0.52), ha="center", fontsize=7.5, color="#555555")
ax.set_xscale("log")
ax.set_xlim(0.6, 0.02)
ax.set_xticks([0.5, 0.3, 0.2, 0.1, 0.05, 0.03, 0.02])
ax.set_xticklabels(["0.5", "0.3", "0.2", "0.1", "0.05", "0.03", "0.02"])
ax.minorticks_off()
ax.set_xlabel(r"Hours available $N$ (labor scarcer to the right)")
ax.set_ylabel(r"$d\ln w\,/\,d\ln p_m$")
ax.set_ylim(-1.05, 0.75)
ax.legend(loc="lower left", frameon=False, fontsize=7.5)
ax.set_title("What the asymptote changes: the wage's response to the machine rental\n"
             r"(toy equilibrium: one good, $Y = A/p$, fixed hours, Figure 1's schedules)",
             loc="left", fontsize=8, color="#333333")
ax.grid(alpha=0.25, lw=0.33)
ax.spines[["top", "right"]].set_visible(False)
fig.savefig(HERE.parent / "figures" / "toy_passthrough.png", dpi=200)
plt.close(fig)
print(f"4. wrote toy_passthrough.png; the jump version switches to only-H at N = {N_SWITCH:.4f}")
