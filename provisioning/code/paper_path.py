# paper_path.py — the companion paper's calibrated economy, re-derived, and three readings P2 takes from it.
#
# The economy is Section 8 and Appendix C of "What Machines Cannot Make" (the October 2026 rewrite of the pinning paper;
# its source is not in this repository). Everything here is written from that version's printed equations and its
# printed parameters, as an independent re-derivation: one good made by tasks on (-inf, 1], human advantage
# gamma(x) = eta (1 - x + zeta)^(-theta), durable machines built from a machine services, lam hours and b land, rented at
# the user cost (rho + delta) V, land the numeraire (r = 1), Cobb-Douglas preferences with land's share alpha of
# spending, hours fixed at Na. Gated by checks/check_paper_path.py on the numbers that version prints.
#
# What P2 reads from it:
#   mix(t)           who is paid along the automation path: labour, interest and rent as shares of income
#   claims(t)        what the claims on interest and rent cost, in years of the whole wage bill (the window)
#   interest_tax(tau) the long-run incidence of a tax on interest, the required return after tax held at rho
#
# Plain functions, no dependencies, bisection by hand. Run from provisioning/:  python3 code/paper_path.py

PAR = dict(theta=2.21694, zeta=0.0997862, a=2.35294, lam=3.23529, b=3.23842,   # Appendix C, as printed
           alpha=0.08, rho=0.10, delta=0.07, T=1.0, Na=0.6)


def gamma(x, eta, p):
    return eta * (1.0 - x + p["zeta"]) ** (-p["theta"])


def J(x, eta, p):
    """Machine services the good needs when machines do every task below x."""
    return eta * (1.0 - x + p["zeta"]) ** (1.0 - p["theta"]) / (p["theta"] - 1.0)


def state(x, eta, lam, p, w_corner=None):
    """Prices and quantities at the task margin x; with w_corner, at the corner x = 1 where the wage is free."""
    u = p["rho"] + p["delta"]
    g, j = gamma(x, eta, p), J(x, eta, p)
    if w_corner is None:
        pm = u * p["b"] / (1.0 - u * p["a"] - u * lam * g)          # the closure, rent 1
        w = g * pm
    else:
        w = w_corner
        pm = u * (lam * w + p["b"]) / (1.0 - u * p["a"])
    price = w * (1.0 - x) + pm * j
    ad = 1.0 - p["a"] * p["delta"]
    Y = p["T"] / (p["alpha"] + (1.0 - p["alpha"]) * p["b"] * p["delta"] * j / (price * ad))   # land clearing
    G = (1.0 - p["alpha"]) * Y / price
    M = j * G / ad
    build = lam * p["delta"] * M                                     # hours spent building machines
    return dict(x=x, w=w, pm=pm, p=price, Y=Y, K=(pm / u) * M, hours=(1.0 - x) * G + build, build=build, gamma=g)


def bisect(f, lo, hi, n=200):
    flo = f(lo)
    for _ in range(n):
        mid = 0.5 * (lo + hi)
        fm = f(mid)
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return 0.5 * (lo + hi)


def equilibrium(eta, lam, p):
    """The stationary equilibrium: an interior margin where hours demanded equal hours supplied, or the corner where
    every final task is automated and labour only builds machines (Lemma 1)."""
    u = p["rho"] + p["delta"]
    gbar = eta * p["zeta"] ** (-p["theta"])
    lam_bar = gbar * u * lam / (1.0 - u * p["a"])                    # hours embodied in replacing the hardest hour
    if lam_bar >= 1.0:                                               # the margin stops short of the hardest task
        top = 1.0 + p["zeta"] - (eta * u * lam / (1.0 - u * p["a"])) ** (1.0 / p["theta"]) - 1e-13
    else:
        top = 1.0
        if state(1.0, eta, lam, p)["hours"] > p["Na"]:
            w0 = gbar * u * p["b"] / (1.0 - u * p["a"] - u * lam * gbar)
            w = bisect(lambda w: state(1.0, eta, lam, p, w)["hours"] - p["Na"], w0, w0 * 1e12)
            return dict(state(1.0, eta, lam, p, w), corner=True, lam_bar=lam_bar, gamma_bar=gbar)
    x = bisect(lambda x: state(x, eta, lam, p)["hours"] - p["Na"], -60.0, top)
    return dict(state(x, eta, lam, p), corner=False, lam_bar=lam_bar, gamma_bar=gbar)


def readout(e, p):
    """Shares of income and what each income buys; P = p^(1 - alpha) is the households' price index with rent 1."""
    P = e["p"] ** (1.0 - p["alpha"])
    return dict(x=e["x"], corner=e["corner"], lam_bar=e["lam_bar"], gamma_bar=e["gamma_bar"],
                wage_rent=e["w"], wage_good=e["w"] / e["p"], real_wage=e["w"] / P, real_rent=1.0 / P,
                real_income=e["Y"] / P, real_capital=e["K"] / P,
                labour=e["w"] * p["Na"] / e["Y"], rent=p["T"] / e["Y"], interest=p["rho"] * e["K"] / e["Y"],
                building=e["build"] / p["Na"], gamma=e["gamma"],
                identity=e["w"] * p["Na"] + p["T"] + p["rho"] * e["K"] - e["Y"])


def point(t, p=PAR, task=True, recursive=True):
    """The economy at technology index t: human advantage 0.01^t of baseline at every task (task automation) and the
    hours to build a machine falling linearly to zero at t = 1 (recursive automation)."""
    eta = 0.01 ** t if task else 1.0
    lam = p["lam"] * max(0.0, 1.0 - t) if recursive else p["lam"]
    return readout(equilibrium(eta, lam, p), p)


def mix(t, p=PAR):
    r = point(t, p)
    return dict(labour=r["labour"], interest=r["interest"], rent=r["rent"])


def claims(t, p=PAR):
    """The claims on interest and on rent, each valued at the return rho, in years of the whole wage bill."""
    r = point(t, p)
    return dict(capital=r["interest"] / r["labour"] / p["rho"], land=r["rent"] / r["labour"] / p["rho"],
                both=(1.0 - r["labour"]) / r["labour"] / p["rho"])


def interest_tax(tau, p=PAR, t=0.0):
    """A tax at rate tau on interest, long run. Owners still require rho after tax (Assumption A4), so the return before
    tax is rho / (1 - tau) and machines rent at (rho / (1 - tau) + delta) V. Returns the taxed economy against the
    untaxed one: what the wage, the rent and the owners' interest buy, the capital stock, and the revenue."""
    eta, lam = 0.01 ** t, p["lam"] * max(0.0, 1.0 - t)
    q = dict(p, rho=p["rho"] / (1.0 - tau))
    e0, e1 = equilibrium(eta, lam, p), equilibrium(eta, lam, q)
    P0, P1 = e0["p"] ** (1.0 - p["alpha"]), e1["p"] ** (1.0 - p["alpha"])
    y0 = e0["Y"] / P0                                                 # the untaxed economy's real income: the yardstick
    wages = (e1["w"] * p["Na"] / P1 - e0["w"] * p["Na"] / P0) / y0
    rents = (p["T"] / P1 - p["T"] / P0) / y0
    owners = (p["rho"] * e1["K"] / P1 - p["rho"] * e0["K"] / P0) / y0   # interest kept after tax
    revenue = (q["rho"] - p["rho"]) * e1["K"] / P1 / y0
    return dict(tau=tau, real_wage=(e1["w"] / P1) / (e0["w"] / P0), real_rent=P0 / P1,
                real_capital=(e1["K"] / P1) / (e0["K"] / P0), real_income=(e1["Y"] / P1) / y0,
                labour_share=e1["w"] * p["Na"] / e1["Y"], labour_share_before=e0["w"] * p["Na"] / e0["Y"],
                wages=wages, rents=rents, owners=owners, revenue=revenue,
                lost=wages + rents + owners + revenue,                # the change in real income: all four add to it
                wage_earner=(wages + revenue) / (e0["w"] * p["Na"] / P0 / y0))   # wages plus the whole revenue, over wages


if __name__ == "__main__":
    base = point(0.0)
    print("baseline: margin %.4f, labour %.3f, interest %.3f, rent %.3f; hours to replace the hardest hour %.0f"
          % (base["x"], base["labour"], base["interest"], base["rent"], base["lam_bar"]))
    print("\nwho is paid, and what the claims cost in years of the wage bill")
    for t in (0.0, 0.25, 0.5, 0.77, 1.0, 1.5, 2.0):
        m, c = mix(t), claims(t)
        print("  t %.2f  labour %.3f  interest %.3f  rent %.3f | capital %7.1f  land %6.1f  both %7.1f"
              % (t, m["labour"], m["interest"], m["rent"], c["capital"], c["land"], c["both"]))
    print("\na tax on interest, long run, at today's technology (changes as shares of untaxed real income)")
    for tau in (0.1, 0.2, 0.3, 0.5):
        r = interest_tax(tau)
        print("  tau %.1f  real wage x%.3f  real rent x%.3f  capital x%.3f  income x%.3f | wages %+.3f  rents %+.3f  "
              "owners %+.3f  revenue %+.3f  lost %+.3f | a wage earner given all the revenue: %+.1f%%"
              % (tau, r["real_wage"], r["real_rent"], r["real_capital"], r["real_income"], r["wages"], r["rents"],
                 r["owners"], r["revenue"], r["lost"], 100 * r["wage_earner"]))
    print("\nthe same tax later on the path")
    for t in (0.5, 1.0):
        r = interest_tax(0.2, t=t)
        print("  t %.1f, tau 0.2  real wage x%.3f  capital x%.3f  income x%.3f | wages %+.3f  rents %+.3f  owners %+.3f  "
              "revenue %+.3f" % (t, r["real_wage"], r["real_capital"], r["real_income"], r["wages"], r["rents"],
                                 r["owners"], r["revenue"]))
