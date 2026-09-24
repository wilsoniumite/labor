# households.py — who carries the people who leave work: the state, families and friends, their own savings, or
# nobody. A household layer on the demand layer (demand.py), for her question (2026-09-24): a surge in dependence,
# emergency policy such as stimulus checks, and debt deflation.
#
# The paper's economy pools everything: one owning household gives every member a basket whether they work or not,
# so people leaving work never cuts spending. That is the benchmark the macro block and its neutral rate stand on.
# This layer measures the departures from it that a representative household cannot see, as the extra demand of
# budget-constrained groups (their spending out of a krona, less a representative household's):
#   people who lose work    their net wage is replaced by public support (the state's replacement rate, falling
#                           after the first year), private support from family and friends (a share of what the
#                           state leaves uncovered), and their own savings while they last; the rest is a spending cut;
#   their supporters        pay the private support and cut their own spending by part of it;
#   borrowers               owe fixed money debts; debt service = (mortgage rate + amortisation) x debt, the mortgage
#                           rate following policy on the floating share and repricing over three years on the rest;
#                           debt service above its starting share of income squeezes spending (a fall in rates
#                           relieves it; falling money incomes against fixed debts tighten it: debt deflation);
#   emergency checks        a temporary transfer to every household, part spent, part saved.
# Their sum is a demand level (% of GDP) that feeds the demand layer each quarter, and the gap it moves feeds back:
# cyclical job loss adds to the people out of work, and inflation sets money wages and prices.
#
# Money wages follow the macro block's real wage and the demand layer's inflation. At the automation peak that asks
# for money-wage CUTS of 10-15% a year; the "rigid wages" variant floors money-wage growth at zero, holds wages flat
# until market wage growth catches up, and sends the adjustment into job loss meanwhile.
#
# Calibration. Measured (Statistics Sweden, 2026): household debt 1.74 x disposable income; 76.8% of housing loans
# repricing within three months; mortgage rates 1.05 points over policy; deposits 0.91 x income; wages 0.84 of
# disposable income; GDP (current prices, last four quarters). Not measured here, stated: the state's net replacement
# rate for a person out of work (0.65 in the first year, 0.50 after — OECD-style net replacement rates for Sweden,
# approximate); what families and friends cover (0.10 of the uncovered income under today's Swedish state support —
# no Swedish measure; a dial); savings of new job losers (3 months of net wage); the share of a loss drawn from
# savings while they last (0.5); spending per krona — job losers 0.8, supporters 0.5, borrowers squeezed 0.6, checks
# 0.4, a representative household 0.05 (Nordic lottery studies put the average near 0.5 in the first year and higher
# for households with little cash; approximate); the tax on wages 0.30; amortisation 2% of the debt a year; the
# labour-demand elasticity for rigid wages 0.4 (the literature's range 0.25-0.5). Debts follow income up (new borrowing
# keeps the debt-to-income ratio) and only amortise down: money debts are fixed, which is what debt deflation needs.
#
# Public data only. Run from paths/:  ../venv/Scripts/python.exe code/households.py
# Out: results/households.json, figures/fig_households.png

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass, replace

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bank_scenarios as bs  # noqa: E402
import demand as dm  # noqa: E402
import deposits_wages as dw  # noqa: E402
import floor_margins as fm  # noqa: E402


def sweden_start() -> dict:
    """The Swedish household sector at the start, from public data (SEK bn; incomes a year)."""
    d = dw.data()
    fl = dw.scb_table("FM/FM0103/FM0103A/FirENS2010ofKv", {"Sektor": "S14", "Kontopost": ["FL4000", "FA2200"], "Motsektor": "S0",
                                                          "ContentsCode": "FM0103AS"}, "fa_households_loans") / 1e3
    fix = dw.scb_table("FM/FM5001/FM5001A/FM5001bostadRteBind", {"Referenssektor": "1.1", "Motpartssektor": "2c",
                                                                 "Rantebindningstid": ["2.0", "2.1", "2.2"], "ContentsCode": "000007MV"}, "housing_loans_fixation")
    gdp = dw.scb_table("NR/NR0103/NR0103B/NR0103ENS2010T10SKv", {"Anvandningstyp": "BNPM", "ContentsCode": "NR0103CG"}, "gdp_current_sa").iloc[:, 0]
    x = fm.data()
    last = d.index[-1]
    return {"date": str(last), "disposable": float(d.disposable.iloc[-1]), "wages_gross": float(d.wages.iloc[-1]),
            "deposits": float(d.deposits.iloc[-1]), "debt": float(fl["FL4000"].dropna().iloc[-1]),
            "gdp": float(gdp.iloc[-4:].sum() / 1e3),
            "floating_share": float(fix["2.1"].iloc[-1] / fix["2.0"].iloc[-1]),
            "mortgage_margin": float(x.mortgage_all_stock.iloc[-1] - x.policy.iloc[-1])}


@dataclass(frozen=True)
class Support:
    """How people out of work are carried. Central: today's Swedish state support."""
    name: str = "today's Swedish state support"
    replacement_first: float = 0.65     # public support / previous net wage, first year out of work
    replacement_later: float = 0.50     # after the first year
    private: float = 0.10               # share of the income the state leaves uncovered that family and friends cover
    buffer_months: float = 3.0          # savings of a new job loser, months of net wage
    draw: float = 0.5                   # share of the remaining loss drawn from savings while they last
    mpc_out: float = 0.8
    mpc_supporter: float = 0.5
    mpc_borrower: float = 0.6
    mpc_check: float = 0.4
    mpc_rep: float = 0.05
    tax: float = 0.30
    amort: float = 2.0                  # % of the debt a year
    refix_years: float = 3.0            # the fixed-rate share reprices over this many years
    rigid_wages: bool = False
    labour_demand_elasticity: float = 0.4   # employment lost per unit of wage held above its market level (literature 0.25-0.5)
    check_size: float = 0.0             # % of household disposable income a year, paid while the check runs
    check_quarters: int = 4
    check_trigger: float = 3.0          # checks start when unemployment is this many points above the start
    private_cap: float = 1.0            # most that family and friends can give, share of the net wages of those in work


# A family-based regime: the state replaces less, family and friends cover half of the rest — but a network can carry a
# few people, not a mass exit, so what it gives is capped at a share of the net wages of those still in work; and the
# supporters include households with mortgages and little cash, so they cut their own spending by more of each krona.
# The lean replacement rates (0.40, then 0.25) stand roughly where the leanest OECD systems do against Sweden's
# (approximate); the half, the 10% cap and the 0.6 are assumptions — there is no Swedish measure of private support.
FAMILY = dict(name="family-based support", replacement_first=0.40, replacement_later=0.25, private=0.5, private_cap=0.10,
              mpc_supporter=0.6)


def run(mp: dict, dmp: dm.Demand, sp: Support, s0: dict) -> dict:
    """The demand layer with the household sector feeding it. mp: the true world's macro path."""
    t = mp["t"]
    dt = float(t[1] - t[0])
    n = len(t)
    part = mp["participation"] / mp["participation"][0]
    real_w = mp["real_wage"] / mp["real_wage"][0]
    net0 = s0["wages_gross"] * (1 - sp.tax)                   # net wage bill at the start (SEK bn a year)
    other0 = s0["disposable"] - net0                          # the rest of disposable income (transfers, capital income, net)
    fl, marg = s0["floating_share"], s0["mortgage_margin"]
    rec = {k: np.zeros(n) for k in ("P", "W", "employed", "out_new", "loss", "public_new", "private", "draw", "buffer",
                                    "debt", "ds", "ds_ref", "income", "mort_rate", "check", "d_out", "d_sup", "d_debt",
                                    "d_check", "level", "deposits", "extra_job_loss", "covered", "burden", "cap_binds")}
    rec["P"][0] = rec["W"][0] = rec["employed"][0] = 1.0
    rec["debt"][0] = s0["debt"]
    rec["income"][0] = s0["disposable"]
    i_start = None
    state = {"check_left": 0, "check_on": False, "fixed_rate": None, "wage_excess": 0.0}
    # new-exit cohorts by quarter of exit (for the first-year / later replacement split)
    cohorts = np.zeros(n)

    def extra(k: int, st: dict) -> float:
        nonlocal i_start
        pol, gap, pi = st["policy"], st["gap"], st["inflation"]
        if i_start is None:
            i_start = float(pol[0])
            state["fixed_rate"] = i_start + marg
        # prices and money wages: the macro block's real wage, carried by the demand layer's inflation
        rec["P"][k] = rec["P"][k - 1] * (1 + pi[k - 1] / 100 * dt)
        pw = float(mp["pi_wage"][k] + (pi[k - 1] - mp["pi_star"]))
        if sp.rigid_wages:
            if pw < 0:                                              # a cut is refused: the wage stays above its market level ...
                state["wage_excess"] += -pw / 100 * dt
                pw = 0.0
            elif state["wage_excess"] > 0:                          # ... until market wage growth catches up, wages flat meanwhile
                use = min(state["wage_excess"], pw / 100 * dt)
                state["wage_excess"] -= use
                pw -= use / dt * 100
        rec["W"][k] = rec["W"][k - 1] * (1 + pw / 100 * dt)
        rec["extra_job_loss"][k] = sp.labour_demand_elasticity * state["wage_excess"]   # ... and costs employment meanwhile
        du = -dmp.okun * gap[k - 1] / 100                            # cyclical job loss, share of the labour force
        emp = max(part[k] - du - rec["extra_job_loss"][k], 0.05)
        rec["employed"][k] = emp
        out_new = max(1.0 - emp, 0.0)                                # out of work since the start, share of start employment
        cohorts[k] = max(out_new - rec["out_new"][k - 1], 0.0)
        rec["out_new"][k] = out_new
        net_w = net0 * rec["W"][k]                                   # a year's net wage bill if everyone still worked
        lost_wage = net_w * out_new
        first = cohorts[max(0, k - int(round(1 / dt)) + 1): k + 1].sum()
        public = net0 * rec["P"][k] * (sp.replacement_first * min(first, out_new) + sp.replacement_later * max(out_new - first, 0.0))
        uncovered = max(lost_wage - public, 0.0)
        private = min(sp.private * uncovered, sp.private_cap * net0 * rec["W"][k] * emp)   # a network's capacity is finite
        # savings: each new exit brings buffer_months of net wage; draw a share of the remaining loss while they last
        rec["buffer"][k] = rec["buffer"][k - 1] + cohorts[k] * net_w * sp.buffer_months / 12
        need = uncovered - private
        draw = min(sp.draw * need * dt, rec["buffer"][k]) / dt
        rec["buffer"][k] -= draw * dt
        loss = need - draw                                           # the spending cut's base, SEK bn a year
        # borrowers' income: net wages of those in work, public support to those out of it, and the rest of today's
        # disposable income (transfers, net) at prices — not the owners' growing capital income, which borrowers do not get
        income = net0 * rec["W"][k] * emp + public + other0 * rec["P"][k]
        rec["income"][k] = income
        # money debts: new borrowing keeps pace with income on the way up; on the way down they only amortise
        rec["debt"][k] = max(s0["debt"] * income / s0["disposable"], rec["debt"][k - 1] * (1 - sp.amort / 100 * dt))
        pol_k = float(pol[k])
        state["fixed_rate"] += (pol_k + marg - state["fixed_rate"]) * dt / sp.refix_years
        mr = fl * (pol_k + marg) + (1 - fl) * state["fixed_rate"]
        rec["mort_rate"][k] = mr
        rec["ds"][k] = (mr + sp.amort) / 100 * rec["debt"][k]
        ds0 = (fl * (i_start + marg) + (1 - fl) * (i_start + marg) + sp.amort) / 100 * s0["debt"]
        rec["ds_ref"][k] = ds0 * income / s0["disposable"]
        # emergency checks: triggered by unemployment
        if sp.check_size > 0 and not state["check_on"] and out_new * 100 >= sp.check_trigger:
            state["check_on"], state["check_left"] = True, sp.check_quarters
        check = 0.0
        if state["check_left"] > 0:
            check = sp.check_size / 100 * income
            state["check_left"] -= 1
        rec["check"][k] = check
        gdp_k = s0["gdp"] * rec["P"][k] * float(mp["Y"][k] / mp["Y"][0])
        rec["d_out"][k] = -(sp.mpc_out - sp.mpc_rep) * loss / gdp_k * 100
        rec["d_sup"][k] = -(sp.mpc_supporter - sp.mpc_rep) * private / gdp_k * 100
        rec["d_debt"][k] = -(sp.mpc_borrower - sp.mpc_rep) * (rec["ds"][k] - rec["ds_ref"][k]) / gdp_k * 100
        rec["d_check"][k] = (sp.mpc_check - sp.mpc_rep) * check / gdp_k * 100
        rec["level"][k] = rec["d_out"][k] + rec["d_sup"][k] + rec["d_debt"][k] + rec["d_check"][k]
        rec["public_new"][k], rec["private"][k], rec["draw"][k], rec["loss"][k] = public, private, draw, loss
        rec["covered"][k] = (public + private + draw) / lost_wage * 100 if lost_wage > 1e-9 else 100.0        # % of the lost net wage
        rec["burden"][k] = private / (net0 * rec["W"][k] * emp) * 100                                         # % of supporters' net wages
        rec["cap_binds"][k] = float(sp.private * uncovered > sp.private_cap * net0 * rec["W"][k] * emp + 1e-9)
        # deposits beyond what income alone would hold (deposits_wages.py): savings drawn down by people out of work,
        # plus the checks not spent (cumulative, SEK bn)
        rec["deposits"][k] = rec["deposits"][k - 1] - draw * dt + (1 - sp.mpc_check) * check * dt
        return rec["level"][k]

    r = dm.run(mp, dmp, extra=extra)
    rec["ds"][0] = rec["ds_ref"][0] = (i_start + marg + sp.amort) / 100 * s0["debt"] if i_start is not None else 0.0
    gdp = s0["gdp"] * rec["P"] * mp["Y"] / mp["Y"][0]
    r.update({"households": rec, "support_cost_pct_gdp": (rec["public_new"] + rec["check"]) / gdp * 100,
              "dsr": rec["ds"] / np.maximum(rec["income"], 1e-9) * 100, "dti": rec["debt"] / np.maximum(rec["income"], 1e-9),
              "deposit_change_pct": rec["deposits"] / s0["deposits"] * 100,
              "unemployment_up_total": rec["out_new"] * 100})
    return r


def summary(r: dict, horizon: float = 15.0) -> dict:
    t = r["t"]
    w = t <= horizon + 1e-9
    h = r["households"]
    at = lambda x, ys=(5, 8, 10, 12, 15): [round(float(np.interp(y, t, x)), 2) for y in ys]  # noqa: E731
    return {"gap_min_max": [round(float(r["gap"][w].min()), 2), round(float(r["gap"][w].max()), 2)],
            "inflation_min_max": [round(float(r["inflation"][w].min()), 2), round(float(r["inflation"][w].max()), 2)],
            "years_at_floor": round(float(r["at_floor"][w].sum() * (t[1] - t[0])), 2),
            "y5_y8_y10_y12_y15": {"gap": at(r["gap"]), "policy": at(r["policy"]), "inflation": at(r["inflation"]),
                                  "out_of_work_pp": at(r["unemployment_up_total"]), "money_wage_index": at(h["W"]),
                                  "demand_level": at(h["level"]), "from_job_losers": at(h["d_out"]), "from_supporters": at(h["d_sup"]),
                                  "from_debt": at(h["d_debt"]), "from_checks": at(h["d_check"]),
                                  "debt_service_pct_income": at(r["dsr"]), "debt_over_income": at(r["dti"]),
                                  "deposits_drawn_or_added_pct": at(r["deposit_change_pct"]), "support_cost_pct_gdp": at(r["support_cost_pct_gdp"]),
                                  "lost_wage_covered_pct": at(h["covered"]), "supporters_burden_pct": at(h["burden"])},
            "years_network_cap_binds": round(float(h["cap_binds"][w].sum() * (t[1] - t[0])), 2)}


def main():
    s0 = sweden_start()
    cyc = json.load(open(os.path.join(ROOT, "results", "demand.json"), encoding="utf-8"))["sweden_cycle"]
    dmp = dm.Demand(kappa=cyc["kappa_per_pp_output_gap"], okun=cyc["okun"])
    worlds = {name: dm.world(br, truth) for name, (br, truth) in bs.SCEN.items()}
    central = Support()
    variants = {"central": central,
                "rigid money wages": replace(central, rigid_wages=True),
                "emergency checks (4% of income for a year)": replace(central, check_size=4.0),
                "rigid wages and checks": replace(central, rigid_wages=True, check_size=4.0),
                "no private support": replace(central, private=0.0),
                "family-based support": replace(central, **FAMILY),
                "family-based, no cap on what networks give": replace(central, **(FAMILY | {"private_cap": 1.0})),
                "family-based, rigid money wages": replace(central, **FAMILY, rigid_wages=True),
                "family-based, with emergency checks": replace(central, **FAMILY, check_size=4.0)}
    out = {"sweden_start": s0, "support": central.__dict__, "scenarios": {}}
    runs = {}
    for name, mp in worlds.items():
        for vn, sp in variants.items():
            r = run(mp, dmp, sp, s0)
            out["scenarios"][f"{name} | {vn}"] = summary(r)
            runs[(name, vn)] = r
        out["scenarios"][f"{name} | demand layer alone (full pooling)"] = dm.summary(dm.run(mp, dmp))
    json.dump(out, open(os.path.join(ROOT, "results", "households.json"), "w", encoding="utf-8"), indent=1)
    print(json.dumps(s0, indent=1))
    for k, v in out["scenarios"].items():
        if "y5_y8_y10_y12_y15" in v and "demand_level" in v["y5_y8_y10_y12_y15"]:
            y = v["y5_y8_y10_y12_y15"]
            print(f"{k:70s} gap {v['gap_min_max']} infl {v['inflation_min_max']} floor {v['years_at_floor']}y | level {y['demand_level']} | out {y['out_of_work_pp']} | DSR {y['debt_service_pct_income']} | W {y['money_wage_index']}")
        else:
            print(f"{k:70s} gap {v.get('gap_min_and_year')} {v.get('gap_max_and_year')} infl {v.get('inflation_min_max')}")
    figure(runs)


def figure(runs):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams["axes.titlesize"] = 10
    fig, ax = plt.subplots(2, 4, figsize=(20, 8.8), layout="constrained")
    fig.get_layout_engine().set(rect=(0, 0.03, 1, 0.97))
    FAM = "family-based support"
    for row, name in enumerate(("deficits dominate", "owners' saving dominates")):
        r = runs[(name, "central")]
        t, h = r["t"], r["households"]
        w = t <= 15
        a = ax[row, 0]
        for key, lab, c in (("d_out", "people who lose work", "C3"), ("d_sup", "their supporters", "C1"), ("d_debt", "borrowers' debt service", "C0")):
            a.plot(t[w], h[key][w], color=c, lw=1.6, label=lab)
        a.plot(t[w], h["level"][w], color="k", lw=2.0, label="total, state support")
        a.plot(t[w], runs[(name, FAM)]["households"]["level"][w], color="k", lw=1.6, ls="--", label="total, family-based support")
        a.axhline(0, color="grey", lw=0.8)
        a.set_title(f"{name}:\nextra demand from constrained households, % of GDP"); a.legend(fontsize=7.5)
        a = ax[row, 1]
        for vn, c, st in (("central", "C2", "-"), (FAM, "C4", "-"), ("rigid money wages", "C2", "--"), ("family-based, rigid money wages", "C4", "--")):
            a.plot(t[w], runs[(name, vn)]["gap"][w], ls=st, color=c, label={"central": "state support", "rigid money wages": "state support, rigid money wages"}.get(vn, vn))
        a.axhline(0, color="grey", lw=0.8)
        a.set_title(f"{name}: output against capacity, %\nwho carries people out of work, and whether money wages can fall"); a.legend(fontsize=7.5)
        a = ax[row, 2]
        for vn, c in (("central", "C2"), (FAM, "C4")):
            hv = runs[(name, vn)]["households"]
            a.plot(t[w], np.where(t[w] >= 7, hv["covered"][w], np.nan), color=c, lw=1.6, label=f"lost net wage covered, % ({ {'central': 'state'}.get(vn, 'family') })")
            a.plot(t[w], hv["burden"][w] * 5, color=c, lw=1.2, ls=":", label=f"supporters' burden x5, % of their net wages ({ {'central': 'state'}.get(vn, 'family') })")
        a.set_title(f"{name}: who carries it\n(the network's cap: 10% of supporters' net wages = 50 on this scale)"); a.legend(fontsize=7)
        a = ax[row, 3]
        a.plot(t[w], r["dsr"][w], color="C0", lw=1.6, label="debt service, % of borrowers' income (state)")
        a.plot(t[w], runs[(name, FAM)]["dsr"][w], color="C0", ls="--", lw=1.4, label="debt service (family)")
        a.plot(t[w], r["unemployment_up_total"][w], color="C3", lw=1.6, label="out of work since the start, % of employment")
        a.plot(t[w], runs[(name, "rigid money wages")]["unemployment_up_total"][w], color="C3", ls="--", lw=1.4, label="out of work, rigid money wages")
        a.set_title(f"{name}: debt service and people out of work"); a.legend(fontsize=7.5)
    for a in ax.flat:
        a.set_xlabel("years")
    fig.text(0.01, 0.005, "households.py on the demand layer and the macro block's worlds. Swedish household debt, fixation, margins, deposits and GDP from Statistics Sweden; replacement rates, private support and spending shares approximate or assumed (see the header).", fontsize=7.5)
    os.makedirs(os.path.join(ROOT, "figures"), exist_ok=True)
    fig.savefig(os.path.join(ROOT, "figures", "fig_households.png"), dpi=120)


if __name__ == "__main__":
    main()
