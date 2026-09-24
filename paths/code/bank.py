# bank.py — a stylised bank on the paths: net interest income, deposits, house prices, borrowers.
#
# Her question (2026-09-24): with significant real rate rises, net interest income goes up first —
# floating mortgages reprice, cash at the central bank earns more — then tightening lowers house and
# asset prices, and then the interest income flows back into assets. This block puts a bank on the
# model's paths to see the sequence. Everything here is illustrative and public: the balance sheet is
# a round-number Nordic-style bank, not any bank's; the bank's own numbers belong on the internal side.
#
# Pieces, each a named, swappable behaviour:
#   - Deposits. Transaction accounts pay (almost) nothing; savings accounts catch up with the policy
#     rate less a spread, with a lag; depositors migrate from transaction to savings accounts as rates
#     rise, with a lag. So the deposit windfall is largest early and decays the longer rates stay high
#     — the effective pass-through (deposit beta) rises with both the level and the duration of rates.
#   - Mortgages reprice with the bank's floating funding (policy rate + covered-bond spread) plus a
#     margin, catching up with a lag: margins are squeezed while funding costs rise and widen while
#     they fall. Below zero, where deposit rates are stuck, banks widen mortgage margins about one-for-one
#     — measured on Sweden 2015-21 (floor_margins.py) — `margin_comp`. Reserves at the central bank earn a share of the policy rate (a political dial).
#     Securities are a ladder bought at the 2Y yield. Corporate and commercial-property loans float.
#   - House prices: the value of a unit of site — its expected real rent path, weighted by the market's
#     belief in each world, discounted at the market's real 10Y rate plus a premium. In the paper's
#     world the site takes the gains, so house prices can rise while wages fall.
#   - Borrowers (wage earners): debt-to-income spread lognormally; the debt-service ratio of each is
#     (mortgage rate + amortisation) x debt / wage income; the share over a stress line, and the share
#     of borrowers no longer working (the model's exit), drive default; loss given default falls as
#     collateral values rise (loan-to-value).
#   - Commercial property: interest cover (net operating income / interest) spread lognormally; debt
#     refinanced at the 3Y yield plus a spread over a few years; income following the site rent, or —
#     since offices need workers, and the model's single land market cannot say so — the wage bill.
# Units: rates in % a year; balance-sheet items as shares of total assets; income and losses in % of
# total assets a year. Nominal values carry the basket's target inflation.

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.stats import norm


@dataclass(frozen=True)
class Bank:
    # balance sheet, shares of total assets (illustrative)
    mortgages: float = 0.35
    cre: float = 0.10
    corporate: float = 0.30
    reserves: float = 0.10
    securities: float = 0.15
    deposits: float = 0.45
    covered: float = 0.25
    wholesale: float = 0.24
    equity: float = 0.06
    # pricing
    covered_spread: float = 0.40        # pp over the policy rate (swapped to floating)
    wholesale_spread: float = 0.80
    mortgage_margin: float = 1.30       # pp over covered funding, once passed through
    mortgage_lag: float = 0.25          # years: half-life of mortgage rates catching up with funding
    margin_comp: float = 1.0            # pp of extra mortgage margin per pp the policy rate sits below margin_from:
    margin_from: float = 0.0            #   measured, Sweden 2015-21: +1.03 per point below zero (floor_margins.py)
    corporate_spread: float = 1.50
    cre_spread: float = 2.00
    reserve_pay: float = 1.00           # share of the policy rate paid on reserves
    securities_tenor: float = 2.0       # years: a ladder bought at the 2Y yield
    # deposits
    tx_share0: float = 0.65             # share of deposits in transaction accounts at a zero policy rate
    tx_beta: float = 0.0                # pass-through to transaction accounts
    tx_semi: float = 0.08               # target transaction share s0 exp(-tx_semi x policy rate)
    tx_halflife: float = 1.0            # years: migration toward the target share
    sav_beta: float = 0.80              # savings accounts pay sav_beta x (policy rate - sav_spread), once caught up
    sav_spread: float = 1.25            # pp
    sav_halflife: float = 0.5           # years
    # borrowers
    dti_mean: float = 3.0               # mortgage debt / gross wage income, mean across borrowers
    dti_logsd: float = 0.5
    amortisation: float = 2.0           # % of the original loan a year
    dsr_line: float = 0.35              # debt service / income above which a borrower is stressed
    ltv0: float = 0.55                  # average loan-to-value at the start
    ltv_logsd: float = 0.35             # spread of loan-to-value across borrowers
    pd_base: float = 0.001              # annual default probabilities
    pd_stressed: float = 0.03
    pd_exited: float = 0.05             # a borrower no longer working
    sale_haircut: float = 0.20          # forced-sale discount on collateral
    house_premium: float = 2.5          # pp over the real 10Y rate in the housing discount rate
    house_floor: float = 1.0            # % : the housing discount rate never below this (a guard, stated)
    # commercial property
    icr_mean: float = 2.5
    icr_logsd: float = 0.35
    icr_line: float = 1.5
    cre_refi_years: float = 3.0
    cre_income: str = "site"            # "site": rents follow the site; "employment": the wage bill
    cre_rate_floor: float = 0.25        # % : property companies' funding rate never below this
    pd_cre_base: float = 0.003
    pd_cre_stressed: float = 0.08
    lgd_cre: float = 0.35
    loss_corporate: float = 0.20        # % a year on the corporate book (held flat)

    def check(self):
        assert abs(self.mortgages + self.cre + self.corporate + self.reserves + self.securities - 1) < 1e-12
        assert abs(self.deposits + self.covered + self.wholesale + self.equity - 1) < 1e-12


def _lag(target, t, halflife, start=None):
    """Partial adjustment toward a target path with the given half-life (0: at once)."""
    out = np.empty_like(target)
    out[0] = target[0] if start is None else start
    for i in range(1, len(t)):
        w = 1.0 if halflife <= 0 else 1.0 - 0.5 ** ((t[i] - t[i - 1]) / halflife)
        out[i] = out[i - 1] + w * (target[i] - out[i - 1])
    return out


def _ladder(rate, t, tenor):
    """The average rate on a book rolled evenly over `tenor` years (the rate before the start held)."""
    out = np.empty_like(rate)
    for i, ti in enumerate(t):
        s = np.linspace(ti - tenor, ti, 41)
        out[i] = float(np.mean(np.interp(s, t, rate)))
    return out


def deposits(policy, t, b: Bank = Bank()):
    tx_rate = np.maximum(b.tx_beta * policy, 0.0)
    sav_rate = _lag(b.sav_beta * np.maximum(policy - b.sav_spread, 0.0), t, b.sav_halflife)
    tx_share = _lag(b.tx_share0 * np.exp(-b.tx_semi * np.maximum(policy, 0.0)), t, b.tx_halflife)   # starts settled
    rate = tx_share * tx_rate + (1.0 - tx_share) * sav_rate
    return {"tx_share": tx_share, "sav_rate": sav_rate, "deposit_rate": rate}


def nii(policy, z2, t, b: Bank = Bank()):
    """Net interest income by line, % of total assets a year."""
    b.check()
    dep = deposits(policy, t, b)
    funding = policy + b.covered_spread
    margin = b.mortgage_margin + b.margin_comp * np.maximum(b.margin_from - policy, 0.0)
    mort_rate = _lag(funding + margin, t, b.mortgage_lag)
    sec_rate = _ladder(z2, t, b.securities_tenor)
    # an exact decomposition of sum(asset x rate) - sum(liability x rate): every rate as the policy rate
    # plus a spread; assets sum to 1 and debt to 1 - equity, so the policy rate itself earns only on equity
    lines = {
        "deposit spread": b.deposits * (policy - dep["deposit_rate"]),
        "mortgage margin": b.mortgages * (mort_rate - funding),
        "loan spreads": np.full_like(policy, b.corporate * b.corporate_spread + b.cre * b.cre_spread),
        "securities vs policy": b.securities * (sec_rate - policy),
        "reserves unpaid": b.reserves * (b.reserve_pay - 1.0) * policy,
        "equity (free funds)": b.equity * policy,
        "market funding": np.full_like(policy, -(b.covered - b.mortgages) * b.covered_spread - b.wholesale * b.wholesale_spread),
    }
    total = (b.mortgages * mort_rate + b.cre * (policy + b.cre_spread) + b.corporate * (policy + b.corporate_spread)
             + b.reserves * b.reserve_pay * policy + b.securities * sec_rate
             - b.deposits * dep["deposit_rate"] - b.covered * funding - b.wholesale * (policy + b.wholesale_spread))
    return total, lines, {"mortgage_rate": mort_rate, "securities_rate": sec_rate, **dep}


def house_price(t, p, rent_old, rent_new, z10, pi_star, b: Bank = Bank()):
    """Real value of a unit of site: the belief-weighted expected real rent path, discounted at the real
    10Y rate plus a premium; the rent path's last value holds beyond its end. Normalised to 1 at t=0."""
    out = np.empty_like(t)
    for i, ti in enumerate(t):
        u = max(z10[i] - pi_star + b.house_premium, b.house_floor) / 100.0
        s = t[i:] - ti
        exp_rent = (1.0 - p[i]) * rent_old[i:] + p[i] * rent_new[i:]
        disc = np.exp(-u * s)
        pv = np.sum(0.5 * (exp_rent[:-1] + exp_rent[1:]) * (disc[:-1] - disc[1:]) / u)   # each interval exactly
        pv += exp_rent[-1] * disc[-1] / u
        out[i] = pv
    return out / out[0]


def borrowers(t, mortgage_rate, wage_index, employed, house_index, b: Bank = Bank()):
    """Stress, default and loss on the mortgage book. wage_index and house_index are nominal, 1 at t=0;
    employed is the share of the start's borrowers still working."""
    debt = np.maximum(1.0 - b.amortisation / 100.0 * t, 0.0)
    burden = (mortgage_rate / 100.0 + b.amortisation / 100.0) * debt / wage_index       # DSR per unit of DTI
    mu = np.log(b.dti_mean) - b.dti_logsd ** 2 / 2.0
    over = 1.0 - norm.cdf((np.log(b.dsr_line / np.maximum(burden, 1e-12)) - mu) / b.dti_logsd)
    exited = 1.0 - employed
    pd = b.pd_base + b.pd_stressed * over * employed + b.pd_exited * exited
    ltv = b.ltv0 * debt / house_index                                                   # the average
    # expected loss given default over a lognormal spread of loan-to-values: E[(1 - k/L)+], k = 1 - haircut
    k, sg = 1.0 - b.sale_haircut, b.ltv_logsd
    mu_l = np.log(np.maximum(ltv, 1e-300)) - sg ** 2 / 2.0
    lgd = norm.cdf((mu_l - np.log(k)) / sg) - k * np.exp(-mu_l + sg ** 2 / 2.0) * norm.cdf((mu_l - sg ** 2 - np.log(k)) / sg)
    return {"dsr_mean": burden * b.dti_mean, "share_over_line": over, "exited": exited, "pd": pd,
            "ltv": ltv, "lgd": lgd, "loss_rate": pd * lgd * 100.0}


def commercial(t, z3, income_index, b: Bank = Bank()):
    rate = _ladder(np.maximum(z3 + b.cre_spread, b.cre_rate_floor), t, b.cre_refi_years)
    cover = income_index / (rate / rate[0])                                              # ICR relative to the start
    mu = np.log(b.icr_mean) - b.icr_logsd ** 2 / 2.0
    below = norm.cdf((np.log(b.icr_line / cover) - mu) / b.icr_logsd)
    pd = b.pd_cre_base + b.pd_cre_stressed * below
    return {"icr_mean": b.icr_mean * cover, "share_below_line": below, "pd": pd, "loss_rate": pd * b.lgd_cre * 100.0,
            "funding_rate": rate}


def expectation_zeros(t, policy, maturities=(2.0, 3.0, 10.0), tp: float = 0.3, known_from: float = 0.0):
    """Zero rates when the policy path is known from `known_from` on (before it, the market expects the
    rate to stay where it is): the average expected policy rate over each maturity plus a term premium
    — the curve layer's identity; the path's last value holds after it."""
    out = {}
    for T in maturities:
        z = np.empty_like(t)
        for i, ti in enumerate(t):
            s = np.linspace(ti, ti + T, 81)
            z[i] = (float(np.mean(np.interp(s, t, policy))) if ti >= known_from else float(policy[i])) + tp
        out[f"{T:g}Y"] = z
    return out


def run(t, policy, zeros: dict, p, old: dict, new: dict, truth: str = "new", b: Bank = Bank()):
    """The bank on one path. zeros: {"2Y", "3Y", "10Y"} market zero rates (%), per date; p: the market's
    belief in the new world; old/new: the two worlds' macro paths on the same grid; truth: which world
    the borrowers and tenants live in."""
    pi = new["pi_star"]
    world = new if truth == "new" else old
    infl = np.exp(pi / 100.0 * t)
    total, lines, rates = nii(policy, zeros["2Y"], t, b)
    rent_old, rent_new = old["Ps"][0] / old["Ps"], new["Ps"][0] / new["Ps"]
    house_real = house_price(t, p, rent_old, rent_new, zeros["10Y"], pi, b)
    house = house_real * infl
    wage = world["real_wage"] / world["real_wage"][0] * infl
    employed = np.minimum(world["participation"] / world["participation"][0], 1.0)
    bor = borrowers(t, rates["mortgage_rate"], wage, employed, house, b)
    site_rent = world["Ps"][0] / world["Ps"] * infl
    wage_bill = wage * employed
    cre = commercial(t, zeros["3Y"], site_rent if b.cre_income == "site" else wage_bill, b)
    losses = b.mortgages * bor["loss_rate"] + b.cre * cre["loss_rate"] + b.corporate * b.loss_corporate
    return {"t": t, "policy": policy, "nii": total, "nii_lines": lines, "rates": rates, "house_real": house_real,
            "house": house, "wage": wage, "employed": employed, "borrowers": bor, "cre": cre, "losses": losses,
            "result": total - losses}
