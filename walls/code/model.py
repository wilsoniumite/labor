# model.py — Appendix B's economy (pinning/code/appendix_b.py) with the schedule as a plug-in and an optional hard
# wall H, plus the backward calibration in closed form. Plain functions on dicts, as in appendix_b.
#
# A schedule is a dict of callables on [0, 1]: g(x) = gamma(x), J(x) = integral of gamma over [0, x], dg(x) = gamma'(x).
# An economy is appendix_b's parameter dict minus the schedule keys (N, T, h, a, b, lam, chi_max, rho, delta), plus
# 'sched' (a schedule) and 'xH' (tasks [xH, 1] closed to machines outright; 1.0 = no hard wall).
#
# THE MODEL (rent r = 1; v = w/r), as appendix_b: D(x) = 1 - (rho+delta)(a + lam gamma(x)) > 0 where machines can take
# task x; p_m = (rho+delta) b / D; v = gamma p_m; p = v (1 - x) + p_m J; P_s = p + h; Y = T / (h + b delta J/(1 - a delta));
# X = Y J / (1 - a delta); n_D = Y (1 - x) + lam delta X; n_S = N F(log(1 + v/P_s)), F uniform on [0, chi_max].
# The soft wall x_c: first task with D <= 0. With a hard wall at xH < x_c and labor demand still above supply there,
# labor holds only H: x* = xH, p_m = (rho+delta)(lam v + b)/(1 - (rho+delta) a), v from n_S = n_D(xH).
#
# THE BACKWARD CALIBRATION (pinning/STATE.md, Log 2026-11-03; targets unrounded): theta_V = lam v / V_m = 0.47,
# machines = (rho+delta) a = 0.20, labor = v (1 - x*)/P_s = 0.47, site = h/P_s = 0.06, chain = chain hours / n = 0.15,
# participation 0.60, Y/N = 3; fixed N 1, b 0.4, delta 0.05. In closed form:
#   1 - x* = participation (1 - chain) / (Y/N)                         (0.17)
#   rho + delta = machines delta + theta_V delta R (1 - chain)/chain,    R = (1 - labor - site)/labor
#   the schedule's one condition: J(x*) = R gamma(x*) (1 - x*)
#   the soft wall: gamma(x_c)/gamma(x*) = (1 - machines)/theta_V         (1.70, whatever the schedule)
#   sigma at the margin = d ln(machine-hours / human-hours in final tasks) / d ln(w/p_m)
#                       = (gamma/J + 1/(1 - x*)) gamma/gamma'            (= 2 gamma / (gamma' (1 - x*)) when R = 1)
import numpy as np
from scipy.optimize import brentq

TARGETS = dict(theta_V=0.47, machines=0.20, labor=0.47, site=0.06, chain=0.15, part=0.60, Y=3.0)
FIXED = dict(N=1.0, b=0.4, delta=0.05)


# ---------------------------------------------------------------- schedules
def power(g0, g1, k, eta=1.0):
    """gamma = eta (g0 + g1 x^k): appendix_b's family."""
    return dict(g=lambda x: eta * (g0 + g1 * np.power(x, k)),
                J=lambda x: eta * (g0 * x + g1 * np.power(x, k + 1) / (k + 1)),
                dg=lambda x: eta * g1 * k * np.power(x, k - 1),
                name=f"power(g0={g0:.4g}, g1={g1:.4g}, k={k:.4g}, eta={eta:.3g})")


def scaled(s, eta):
    """Task automation as Figure 3 has it: gamma halved (eta = 0.5) at every task."""
    return dict(g=lambda x: eta * s["g"](x), J=lambda x: eta * s["J"](x), dg=lambda x: eta * s["dg"](x),
                name=f"{s['name']} x {eta:.3g}")


def flattened(s, x0, eta):
    """Automation that lands on the tasks above x0: gamma(x) -> gamma(x0) + eta (gamma(x) - gamma(x0)) for x > x0, the
    schedule's upper part compressed toward the level at x0 (order kept). eta = 1 is the base, eta -> 0 flat above x0."""
    g0, J0 = float(s["g"](x0)), float(s["J"](x0))

    def g(x):
        x = np.asarray(x, dtype=float)
        return np.where(x <= x0, s["g"](x), g0 + eta * (s["g"](x) - g0))

    def J(x):
        x = np.asarray(x, dtype=float)
        above = J0 + g0 * (x - x0) + eta * (s["J"](x) - J0 - g0 * (x - x0))
        return np.where(x <= x0, s["J"](x), above)

    def dg(x):
        x = np.asarray(x, dtype=float)
        return np.where(x <= x0, s["dg"](x), eta * s["dg"](x))

    return dict(g=g, J=J, dg=dg, name=f"{s['name']} flattened above {x0:.3f} by {eta:.3g}")


def from_values(gvals, name="resorted"):
    """The schedule of a set of task-level gammas (equal task weights): sort them, gamma as the quantile function on a
    uniform grid, J by the cumulative trapezoid, gamma' by differences of a lightly smoothed quantile function."""
    gv = np.sort(np.asarray(gvals, dtype=float))
    n = gv.size
    xs = (np.arange(n) + 0.5) / n
    xs = np.concatenate([[0.0], xs, [1.0]])
    gv = np.concatenate([[gv[0]], gv, [gv[-1]]])
    Jc = np.concatenate([[0.0], np.cumsum(0.5 * (gv[1:] + gv[:-1]) * np.diff(xs))])
    w = max(5, n // 2000)
    sm = np.convolve(gv, np.ones(w) / w, mode="same")
    dgv = np.gradient(sm, xs)
    return dict(g=lambda x: np.interp(x, xs, gv), J=lambda x: np.interp(x, xs, Jc), dg=lambda x: np.interp(x, xs, dgv),
                name=name)


def resorted(s, multiplier, n=400_000, name=None):
    """Automation that lands on chosen tasks: each task keeps its identity, its gamma is multiplied by multiplier(x)
    (x the task's position in the base schedule s), and the schedule is the new gammas sorted. Machines gain at the
    tasks where the multiplier is below one."""
    x = (np.arange(n) + 0.5) / n
    return from_values(s["g"](x) * multiplier(x), name=name or f"{s['name']} resorted")


# ---------------------------------------------------------------- the economy
def cpt(P):
    return P["rho"] + P["delta"]


def denominator(P, x):
    return 1.0 - cpt(P) * (P["a"] + P["lam"] * P["sched"]["g"](x))


def ceiling(P):
    """x_c, the soft wall: the first task closed to machines at every wage (D = 0), or 1."""
    if denominator(P, 1.0) > 0.0:
        return 1.0
    return brentq(lambda x: float(denominator(P, x)), 0.0, 1.0, xtol=1e-15)


def real_wage(P, x):
    """v / P_s at an interior threshold x, finite at the soft wall."""
    c, g, j = cpt(P), P["sched"]["g"](x), P["sched"]["J"](x)
    return c * P["b"] * g / (c * P["b"] * (g * (1.0 - x) + j) + P["h"] * denominator(P, x))


def demand(P, x):
    ad = P["a"] * P["delta"]
    j = P["sched"]["J"](x)
    Y = P["T"] / (P["h"] + P["b"] * P["delta"] * j / (1.0 - ad))
    X = Y * j / (1.0 - ad)
    return Y, X, Y * (1.0 - x), P["lam"] * P["delta"] * X


def n_demand(P, x):
    Y, X, final, chain = demand(P, x)
    return final + chain


def n_supply_at(P, real):
    return P["N"] * min(max(np.log1p(real) / P["chi_max"], 0.0), 1.0)


def excess(P, x):
    return n_demand(P, x) - n_supply_at(P, real_wage(P, x))


def interior(P, x):
    c, D = cpt(P), float(denominator(P, x))
    g, j = float(P["sched"]["g"](x)), float(P["sched"]["J"](x))
    pm = c * P["b"] / D
    v = g * pm
    Ps = v * (1.0 - x) + pm * j + P["h"]
    Y, X, final, chain = demand(P, x)
    n = final + chain
    return dict(x=x, regime="interior", gamma=g, J=j, D=D, pm=pm, v=v, Ps=Ps, real_wage=v / Ps, Y=Y, X=X,
                final_hours=final, chain_hours=chain, n=n, participation=n / P["N"],
                labor_share_basket=v * (1.0 - x) / Ps, machine_task_share=pm * j / Ps, site_share=P["h"] / Ps,
                theta_V=P["lam"] * v * D / P["b"], chain_share=chain / n)


def boundary(P, xH):
    """Labor holds only H = [xH, 1]: the wage clears n_S(v/P_s) = n_D(xH); the rental is the user cost on that wage."""
    c = cpt(P)
    Y, X, final, chain = demand(P, xH)
    n = final + chain
    j = float(P["sched"]["J"](xH))
    need = np.expm1(P["chi_max"] * n / P["N"])                      # the real wage at which n_S = n_D (F uniform)

    def real(v):
        pm = c * (P["lam"] * v + P["b"]) / (1.0 - c * P["a"])
        return v / (v * (1.0 - xH) + pm * j + P["h"])

    v0 = float(P["sched"]["g"](xH)) * c * P["b"] / float(denominator(P, xH))   # the wage that puts the margin at xH
    top = 1.0 / ((1.0 - xH) + c * P["lam"] * j / (1.0 - c * P["a"]))           # sup of v/P_s as v grows
    if not (real(v0) <= need < top):
        raise ValueError(f"no boundary equilibrium at xH {xH}: need {need:.4g}, from {real(v0):.4g} below {top:.4g}")
    v = brentq(lambda t: real(t) - need, v0, v0 * 1e15, xtol=1e-14, rtol=1e-14)
    pm = c * (P["lam"] * v + P["b"]) / (1.0 - c * P["a"])
    Ps = v * (1.0 - xH) + pm * j + P["h"]
    return dict(x=xH, regime="only H", v=v, pm=pm, Ps=Ps, real_wage=v / Ps, Y=Y, X=X, final_hours=final,
                chain_hours=chain, n=n, participation=n / P["N"], labor_share_basket=v * (1.0 - xH) / Ps)


def solve(P):
    """Equilibrium: the interior margin below min(x_c, xH) (Lemma B.1's crossing), or labor holding only H."""
    xc = ceiling(P)
    xH = P.get("xH", 1.0)
    up = min(xc, xH)
    if up < xc and excess(P, up) >= 0.0:
        q = boundary(P, up)
    else:
        f0 = excess(P, 1e-12)
        if not f0 > 0.0:
            raise ValueError("no interior crossing: labor demand below supply even with labor on every task")
        x = brentq(lambda t: excess(P, t), 1e-12, up * (1 - 1e-13) if up == xc else up, xtol=1e-15, maxiter=500)
        q = interior(P, x)
    q.update(x_c=xc, xH=xH)
    return q


def sigma_margin(P, x):
    """Elasticity of substitution between machine services and labor in final tasks at the margin x."""
    s = P["sched"]
    g, j, dg = float(s["g"](x)), float(s["J"](x)), float(s["dg"](x))
    return (g / j + 1.0 / (1.0 - x)) * g / dg


# ---------------------------------------------------------------- the backward calibration
def margin_from_targets(tg=TARGETS, N=1.0):
    return 1.0 - tg["part"] * N * (1.0 - tg["chain"]) / tg["Y"]


def R_of(tg=TARGETS):
    return (1.0 - tg["labor"] - tg["site"]) / tg["labor"]


def soft_wall_multiple(tg=TARGETS):
    return (1.0 - tg["machines"]) / tg["theta_V"]


def calibrate(sched, tg=TARGETS, fx=FIXED):
    """The economy that hits the seven targets with the given schedule, which must satisfy J(x*) = R g(x*)(1 - x*)."""
    x, d, R = margin_from_targets(tg, fx["N"]), fx["delta"], R_of(tg)
    g, j = float(sched["g"](x)), float(sched["J"](x))
    assert abs(j - R * g * (1 - x)) < 1e-9 * max(1.0, j), "schedule misses the calibration condition"
    c = tg["machines"] * d + tg["theta_V"] * d * R * (1 - tg["chain"]) / tg["chain"]
    a = tg["machines"] / c
    lam = tg["theta_V"] / (c * g)
    D = 1 - tg["machines"] - tg["theta_V"]
    pm = c * fx["b"] / D
    v = g * pm
    Ps = v * (1 - x) / tg["labor"]
    h = tg["site"] * Ps
    T = tg["Y"] * fx["N"] * (h + fx["b"] * d * j / (1 - a * d))
    return dict(N=fx["N"], T=T, h=h, a=a, b=fx["b"], lam=lam, chi_max=np.log1p(v / Ps) / tg["part"], rho=c - d,
                delta=d, sched=sched, xH=1.0)


def power_c_of_k(k, tg=TARGETS):
    """In the scale-free power family gamma = c + x^k, the c that meets the calibration condition at x* (None if c <= 0)."""
    x, R = margin_from_targets(tg), R_of(tg)
    c = (R * x ** k * (1 - x) - x ** (k + 1) / (k + 1)) / (x - R * (1 - x))
    return c if c > 0 else None


def power_family(k, tg=TARGETS):
    """The calibrated power schedule with exponent k, normalized so gamma(1) = 1."""
    c = power_c_of_k(k, tg)
    return power(c / (1 + c), 1 / (1 + c), k)


def appendix_b_economy(P_ab):
    """An appendix_b parameter dict as an economy here (for the equivalence check)."""
    P = {k: v for k, v in P_ab.items() if k not in ("g0", "g1", "k", "eta")}
    P["sched"] = power(P_ab["g0"], P_ab["g1"], P_ab["k"], P_ab.get("eta", 1.0))
    P["xH"] = 1.0
    return P
