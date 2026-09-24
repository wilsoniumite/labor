# macro.py — the macro block: the paper's Appendix B economy along a technology path, and the bridges
# from it to the curve layer.
#
# STRUCTURE (the paper, SSRN version of 2026-09-23, Appendix B — not the repository's older pinning/
# copy, whose Appendix B is a different formulation). N potential workers; one supporting household
# owns T units of land, provides one basket to each worker in work and exit, and spends the rest in
# the basket's proportions. A basket is one unit of the final good and h units of space. Rent r = 1
# (numeraire), v = w/r. The final good needs one unit of each task on [0, 1]; gamma_L = 1,
# gamma_M = 1/gamma(x), gamma increasing. A unit of machine service needs a units of machine service,
# lambda hours and b land. At an interior threshold x (machines below, people above):
#     J(x) = ∫0^x gamma,  v(x) = b gamma(x) / (1 - a - lambda gamma(x)),  p_m(x) = b / (1 - a - lambda gamma(x)),
#     p(x) = v(1 - x) + p_m J,  P_s = p + h,  Y = T / (h + b J/(1 - a)),  X = Y J/(1 - a),
#     n_D = Y [1 - x + lambda J/(1 - a)],  n_S = N F(log(1 + v/P_s)),  F uniform on [0, chi_max].
# Equilibrium: n_D(x*) = n_S(x*). Income I = v n + T (Appendix C). Gate: the paper's numerical
# instance (N 4, T 10, h 1, a .3, b .4, lambda .05, gamma .2 + .8x, chi ~ U[0,1]) solves to
# x* 0.86315, v 0.54344, Y 7.88061, n 1.34338 (checks/check_macro.py).
#
# CAPITAL (the paper's Appendix A.4). Machines as a stock priced at user cost: a service unit costs
# (rho + delta) times a machine's build cost, so interest on machine capital becomes a third income. At
# (rho, delta) = (0, 1) the core is Appendix B exactly; calibration (a) uses that, calibration (b) a 5.75%
# required return and 8% depreciation. With Bridges.capital_premium set, the required return follows the
# economy's own real rate, so rates feed back into automation.
#
# DYNAMICS. The technology clock moves capability (gamma scaled by eta: task automation) and the
# labour embodied in machine services (lambda: recursive automation) along a path; each date is solved
# as an equilibrium (quasi-static: no build lags, no adjustment costs — a stated simplification).
#
# BRIDGES (behaviour, swappable; every coefficient is a named default to be varied, not an estimate):
#   nominal — the central bank holds the basket's price on its target pi*, so goods, rents and wages
#             inflate at pi* plus the change in their real price against the basket: the fork appears
#             as goods deflation and shelter inflation around an on-target CPI;
#   fiscal  — a labour tax, a rent tax, spending, and a public share of dependants' support;
#   neutral — r* moves up with the machine build-out (capex), down as income shifts to rent owners
#             who save more, up with fiscal deficits;
#   policy  — the desired nominal rate r* + pi* (+ reaction to measured inflation under mandates that
#             exclude shelter); the curve layer's stepwise rule delivers it;
#   premia  — term premium and sovereign loss rate rise with debt above thresholds.

from __future__ import annotations

from dataclasses import dataclass, field, replace

import numpy as np
from scipy.optimize import brentq


# ------------------------------------------------------------------ the structural core (Appendix B, with A.4's capital)
@dataclass(frozen=True)
class Economy:
    N: float = 4.0
    T: float = 10.0
    h: float = 1.0
    a: float = 0.3
    b: float = 0.4
    lam: float = 0.05
    g0: float = 0.2          # gamma(x) = eta * (g0 + g1 x^k); k = 1 is the paper's schedule, k > 1 the
    g1: float = 0.8          # convex schedules of its eras figure (human advantage concentrated near the wall)
    k: float = 1.0
    eta: float = 1.0
    chi_max: float = 1.0     # work cost chi ~ U[0, chi_max]
    rho: float = 0.0         # required return on machine capital (a year) — Appendix A.4's interest
    delta: float = 1.0       # depreciation (a year). (rho, delta) = (0, 1) is Appendix B's flow benchmark exactly

    def gamma(self, x):
        return self.eta * (self.g0 + self.g1 * x ** self.k)

    def J(self, x):
        return self.eta * (self.g0 * x + self.g1 * x ** (self.k + 1.0) / (self.k + 1.0))


def _parts(e: Economy, x):
    """Prices and quantities at threshold x. Machines are a stock K, one service unit a year each; a new
    machine costs Vm = a p_m + lambda v + b (machine services, hours, land), so the user cost is
    p_m = (rho + delta) Vm (Appendix A.4) and, at the margin v = p_m gamma(x*),
        Vm = b / (1 - (rho + delta)(a + lambda gamma)),   p_m = (rho + delta) Vm.
    Replacement of delta K a year uses a delta K services, lambda delta K hours and b delta K land:
        K = Y J / (1 - a delta),  Y = T / (h + b delta J / (1 - a delta)),  n = Y (1 - x) + lambda delta K.
    Income: I = v n + T + rho Vm K (wages, land rent, interest). At (0, 1) all of this is Appendix B."""
    g, J = e.gamma(x), e.J(x)
    cpt = e.rho + e.delta
    den = 1.0 - cpt * (e.a + e.lam * g)
    Vm = e.b / den
    pm = cpt * Vm
    v = g * pm
    p = v * (1.0 - x) + pm * J
    Ps = p + e.h
    Y = e.T / (e.h + e.b * e.delta * J / (1.0 - e.a * e.delta))
    K = Y * J / (1.0 - e.a * e.delta)
    final_hours = Y * (1.0 - x)
    machine_hours = e.lam * e.delta * K
    nD = final_hours + machine_hours
    z = np.log1p(v / Ps)
    nS = e.N * min(max(z / e.chi_max, 0.0), 1.0)
    return dict(x=x, gamma=g, J=J, v=v, pm=pm, Vm=Vm, p=p, Ps=Ps, Y=Y, X=K, K=K, final_hours=final_hours,
                machine_hours=machine_hours, nD=nD, nS=nS)


def solve(e: Economy):
    """The interior equilibrium n_D(x*) = n_S(x*). Raises if Lemma B.1's conditions fail."""
    assert 1.0 - (e.rho + e.delta) * (e.a + e.lam * e.gamma(1.0)) > 0, "machine-service cost undefined at x = 1"
    f = lambda x: _parts(e, x)["nD"] - _parts(e, x)["nS"]  # noqa: E731
    lo, hi = 1e-12, 1.0
    if f(lo) <= 0 or f(hi) >= 0:
        raise ValueError(f"no interior equilibrium: nD - nS = {f(lo):.4g} at 0, {f(hi):.4g} at 1")
    x = brentq(f, lo, hi, xtol=1e-15)
    q = _parts(e, x)
    n = q["nD"]
    interest = e.rho * q["Vm"] * q["K"]
    income = q["v"] * n + e.T + interest
    q.update(n=n, participation=n / e.N, income=income, labor_share=q["v"] * n / income,
             capital_share=interest / income, capital_output=q["Vm"] * q["K"] / income,
             real_wage=q["v"] / q["Ps"], goods_to_space=q["p"] / 1.0,
             support_cost=e.N * q["Ps"], funded=e.T + interest > e.N * q["Ps"])
    return q


# ------------------------------------------------------------------ the technology clock
@dataclass(frozen=True)
class TechPath:
    """eta and lambda move from their start values toward targets along a logistic in time: centred at
    t_mid (years), with `width` years from 12% to 88% of the move. eta scales capability (task
    automation); lambda is the labour in a machine-service hour (recursive automation)."""
    eta_end: float = 1.0
    lam_end: float = 0.05
    t_mid: float = 5.0
    width: float = 4.0

    def at(self, t, base: Economy):
        s = 1.0 / (1.0 + np.exp(-(t - self.t_mid) / (self.width / 4.0)))
        s0 = 1.0 / (1.0 + np.exp(self.t_mid / (self.width / 4.0)))
        w = (s - s0) / (1.0 - s0)                                   # 0 at t = 0, -> 1
        return replace(base, eta=base.eta + (self.eta_end - base.eta) * w,
                       lam=base.lam + (self.lam_end - base.lam) * w)


# ------------------------------------------------------------------ the bridges (behaviour; swappable)
@dataclass(frozen=True)
class Bridges:
    pi_star: float = 2.0            # % a year: the basket's price on target
    tau_w: float = 0.40             # tax on wage income
    tau_r: float = 0.10             # tax on non-wage income (land rent; in this benchmark also standing in for capital income)
    gov_share: float = 0.20         # spending, share of income
    public_support: float = 0.30    # public share of dependants' baskets
    r0_star: float = 0.75           # % real neutral rate at the start
    alpha_capex: float = 0.25       # pp of r* per pp a year of tasks moving to machines (the build-out's investment demand)
    alpha_rent: float = 0.05        # pp of r* per pp rise in the non-wage share of income (owners save more)
    alpha_fiscal: float = 0.10      # pp of r* per pp of deficit / income
    tp0: float = 0.30               # % term premium at the start
    tp_per_debt: float = 0.02       # pp of term premium per pp of debt/income above the threshold
    debt_threshold: float = 60.0    # % of income
    loss_per_debt: float = 0.015    # pp of long-run sovereign loss rate per pp of debt above the threshold
    debt0: float = 40.0             # % of income at the start
    mandate: str = "headline"       # "headline" | "goods" (a core measure excluding shelter)
    phi_pi: float = 1.5             # reaction to measured inflation off target under the goods mandate
    capital_premium: float | None = None   # pp over the real neutral rate: the required return on machine capital.
                                           # None: rho stays at the economy's own value (no feedback)
    rho_shift: float = 0.0          # pp added to the required return (a sustained rate shock)


def _deficit(br, e: Economy, q: dict):
    """Deficit, % of income: spending plus the public share of dependants' baskets, less a wage tax and a
    tax on non-wage income (land rent and interest)."""
    interest = e.rho * q["Vm"] * q["K"]
    revenue = br.tau_w * q["v"] * q["n"] + br.tau_r * (e.T + interest)
    spending = br.gov_share * q["income"] + br.public_support * (e.N - q["n"]) * q["Ps"]
    return (spending - revenue) / q["income"] * 100, br.tau_w * q["v"] * q["n"] / revenue


def macro_path(base: Economy, tech: TechPath, br: Bridges = Bridges(), years: float = 15.0, dt: float = 0.25):
    """Quasi-static macro path: an equilibrium each date, then the bridges. Returns a dict of arrays;
    rates and inflation in % a year, fiscal quantities in % of income.
    With br.capital_premium set, the required return on machine capital follows the economy's own real
    rate — rho(t) = r*(t - dt) + premium (+ rho_shift) — so rates feed back into automation; the pace of
    automation then uses backward differences, as it must when r* at t depends on the past."""
    t = np.arange(0.0, years + 1e-9, dt)
    feedback = br.capital_premium is not None
    econ, sol, r_seq = [], [], []
    if not feedback:
        econ = [tech.at(ti, base) for ti in t]
        if br.rho_shift:
            econ = [replace(e, rho=e.rho + br.rho_shift / 100) for e in econ]
        sol = [solve(e) for e in econ]
    else:
        r_prev = br.r0_star
        nw0 = d0 = None
        for i, ti in enumerate(t):
            e = replace(tech.at(ti, base), rho=(r_prev + br.capital_premium + br.rho_shift) / 100)
            q = solve(e)
            econ.append(e); sol.append(q)
            nonwage = (1.0 - q["labor_share"]) * 100
            dfc, _ = _deficit(br, e, q)
            if i == 0:
                nw0, d0, pace = nonwage, dfc, 0.0
            else:
                pace = (q["x"] - sol[i - 1]["x"]) / dt * 100
            r_prev = br.r0_star + br.alpha_capex * pace - br.alpha_rent * (nonwage - nw0) + br.alpha_fiscal * (dfc - d0)
            r_seq.append(r_prev)
    get = lambda k: np.array([q[k] for q in sol])  # noqa: E731
    v, Ps, p, n, inc, X, Y, x = get("v"), get("Ps"), get("p"), get("n"), get("income"), get("X"), get("Y"), get("x")
    ls = get("labor_share")
    grad = lambda y: np.gradient(np.log(y), t) * 100  # noqa: E731
    # nominal: the basket on target; everything else at pi* plus its real change against the basket
    pi_goods = br.pi_star + grad(p / Ps)
    pi_shelter = br.pi_star + grad(1.0 / Ps)
    pi_wage = br.pi_star + grad(v / Ps)
    # fiscal
    fis = [_deficit(br, e, q) for e, q in zip(econ, sol)]
    deficit = np.array([f[0] for f in fis])
    wage_tax_share = np.array([f[1] for f in fis])
    growth = br.pi_star + grad(Y)
    # neutral real rate
    automation_pace = np.gradient(x, t) * 100                    # pp of tasks moving to machines, a year
    nonwage_share = (1.0 - ls) * 100
    if feedback:
        r_star = np.array(r_seq)
    else:
        r_star = (br.r0_star + br.alpha_capex * automation_pace - br.alpha_rent * (nonwage_share - nonwage_share[0])
                  + br.alpha_fiscal * (deficit - deficit[0]))
    # debt and premia
    debt = np.empty_like(t)
    debt[0] = br.debt0
    for i in range(1, len(t)):
        debt[i] = debt[i - 1] + dt * (deficit[i - 1] + (r_star[i - 1] + br.pi_star - growth[i - 1]) / 100 * debt[i - 1])
    over = np.maximum(debt - br.debt_threshold, 0.0)
    tp = br.tp0 + br.tp_per_debt * over
    loss_longrun = br.loss_per_debt * over
    # the desired policy rate
    desired = r_star + br.pi_star
    if br.mandate == "goods":
        desired = desired + br.phi_pi * (pi_goods - br.pi_star)
    return dict(t=t, eta=np.array([e.eta for e in econ]), lam=np.array([e.lam for e in econ]),
                rho=np.array([e.rho for e in econ]) * 100, x=x, v=v, Ps=Ps, p=p, n=n,
                participation=get("participation"), income=inc, labor_share=ls, capital_share=get("capital_share"),
                capital_output=get("capital_output"), real_wage=get("real_wage"), X=X, Y=Y, funded=get("funded"),
                pi_goods=pi_goods, pi_shelter=pi_shelter, pi_wage=pi_wage, deficit=deficit,
                wage_tax_share=wage_tax_share, debt=debt, r_star=r_star, tp=tp, loss_longrun=loss_longrun,
                desired=desired, automation_pace=automation_pace, nonwage_share=nonwage_share, pi_star=br.pi_star)


# ------------------------------------------------------------------ from the macro path to the curve layer
@dataclass(frozen=True)
class Recognition:
    """How fast the market learns the destination the macro path is heading for (the recognition
    clock); the central bank delivers through curve.PolicyRule (the institutions clock)."""
    h_dest: float = 1.0             # half-life (years) of the market's learning of the neutral rate
    k2: float = 0.3                 # speed at which the cycle target returns to the destination
    elb: float = -0.5               # effective lower bound: policy delivers the desired rate only down to here


def curve_path(mp: dict, rec: Recognition = Recognition(), rule=None):
    """CurveStates for the common (OIS) curve and SovereignStates for the government spread, one per date
    of the macro path. Policy steps toward the desired rate on the meeting calendar; the market's
    destination learns r* + pi* with half-life h_dest; the cycle target is the desired rate; the term
    premium and the sovereign long-run loss come from debt."""
    import curve as cv
    import sovereign as sv
    rule = rule or cv.PolicyRule()
    t, desired = mp["t"], mp["desired"]
    M = rule.meetings_per_year
    r = max(round(float(desired[0]) / rule.step) * rule.step, rec.elb)
    next_meet = 1.0 / M
    dest = float(mp["r_star"][0] + mp["pi_star"])
    states, sovs, policy = [], [], []
    for i, ti in enumerate(t):
        while ti + 1e-12 >= next_meet:
            r = max(rule.decide(r, max(float(np.interp(next_meet, t, desired)), rec.elb)), rec.elb)
            next_meet += 1.0 / M
        if i > 0:
            target = float(mp["r_star"][i] + mp["pi_star"])
            dest += (target - dest) * (1.0 - 0.5 ** ((ti - t[i - 1]) / rec.h_dest))
        states.append(cv.CurveState(r0=r, m0=max(float(desired[i]), rec.elb), rbar=dest, k1=rule.implied_speed(), k2=rec.k2,
                                    tp=float(mp["tp"][i]), delay=next_meet - ti))
        lr = float(mp["loss_longrun"][i])
        sovs.append(sv.SovereignState(cv.CurveState(r0=0.0, m0=lr, rbar=lr, k1=0.5, k2=0.2, tp=0.0)))
        policy.append(r)
    return states, sovs, np.array(policy)


# ------------------------------------------------------------------ calibration of the normal case
CALIBRATION_BASE = Economy(g0=0.02, g1=0.98)     # machines up to 50x better than people on the easiest task


def calibrate(targets=None, base: Economy = CALIBRATION_BASE):
    """Choose T, h, chi_max and the schedule's convexity k (N = 1; a, b, lambda held at the paper's
    values; g0 = 0.02) so the starting equilibrium hits public targets:
      - labour share 0.47: the paper's full-chain human-effort share of consumed production (Figure 7, 2023);
      - participation 0.60: an employment rate;
      - 3 support baskets of output per person: the support basket as a subsistence bundle, a third of
        average consumption (the Orshansky construction the paper's coverage measure uses);
      - site share of the basket 0.13: the land part of a shelter share of about a third, at the 30-50%
        land shares of housing the paper's coverage measure uses. Appendix B's space is pure site.
    What the benchmark cannot separate: with two primary factors, everything not paid to hours is rent on
    non-produced inputs, so the machine chains' land (about 0.40 of income here) also stands in for what
    national accounts call capital income. History calibrates the normal case only."""
    from scipy.optimize import least_squares
    tg = {"labor_share": 0.47, "participation": 0.60, "baskets_per_person": 3.0, "site_share": 0.13, **(targets or {})}

    def build(q):
        return replace(base, N=1.0, T=float(np.exp(q[0])), h=float(np.exp(q[1])), chi_max=float(np.exp(q[2])),
                       k=float(np.exp(q[3])))

    def resid(q):
        e = build(q)
        try:
            s_ = solve(e)
        except (ValueError, AssertionError):
            return [10.0] * 4
        return [s_["labor_share"] - tg["labor_share"], s_["participation"] - tg["participation"],
                (s_["Y"] / e.N - tg["baskets_per_person"]) / tg["baskets_per_person"], e.h / s_["Ps"] - tg["site_share"]]
    best = None
    for q0 in ([0.0, np.log(0.5), np.log(2.0), np.log(6.0)], [np.log(3.0), np.log(1.0), np.log(1.0), np.log(3.0)],
               [np.log(0.5), np.log(0.2), np.log(2.0), np.log(10.0)], [np.log(1.5), np.log(0.4), np.log(3.0), np.log(5.0)]):
        r = least_squares(resid, q0, bounds=([np.log(1e-4)] * 3 + [np.log(0.2)], [np.log(1e3)] * 3 + [np.log(60.0)]))
        if best is None or r.cost < best.cost:
            best = r
    e = build(best.x)
    return e, solve(e), tg, float(np.max(np.abs(best.fun)))


def income_split(e: Economy, q: dict):
    """Shares of income: labour, the housing site, the machine chains' land, and interest on machine
    capital. With (rho, delta) = (0, 1) — calibration (a) — interest is zero and the machine chains'
    land also stands in for capital income; with capital (calibration (b)) the two are separate."""
    return {"labour": q["labor_share"], "housing_site": e.h * q["Y"] / q["income"],
            "machine_chain_land": e.b * e.delta * q["K"] / q["income"], "interest": q["capital_share"]}


CAPITAL_BASE = replace(CALIBRATION_BASE, rho=0.0575, delta=0.08)   # (b): return 0.75% real + 5% premium; 8% depreciation
