# households.py — who carries the people who leave work: the state, families and friends, their own savings, or
# nobody. A household layer on the demand layer (demand.py), for her question (2026-09-24): a surge in dependence,
# emergency policy such as stimulus checks, and debt deflation.
#
# The paper's economy pools everything: one owning household gives every member a basket whether they work or not,
# so people leaving work never cuts spending. That is the benchmark the macro block and its neutral rate stand on.
# This layer measures the departures from it that a representative household cannot see, as the extra demand of
# budget-constrained groups (their spending out of a krona, less a representative household's):
#   people who lose work    their net wage is replaced by public support (Sweden's rules: the a-kassa on their own
#                           money wage at exit for the first year, then a price-indexed floor), private support from
#                           family and friends (a share of what the state leaves uncovered), and their own savings
#                           while they last; the rest is a spending cut;
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
# for money-wage CUTS of up to about 20% a year (deficits) and 29% (owners' saving), and money wages fall 71-84% by year 15;
# the "rigid wages" variant lets money wages fall no faster than 4% a year (a calibration choice: Schmitt-Grohé and Uribe
# 2016's loose bound, gamma 0.99 a quarter, from Lithuania's 5.1% fall over 13 quarters, pegged, not in the euro; Greece's
# compensation per employee fell about 20% over 2009-15, 8.3% in 2013 alone), closes the gap to the market wage as fast as
# that allows, and sends the rest into job loss: log employment falls by the labour-demand elasticity times the log excess
# of the wage over its market level (tracked in logs), a share of the jobs still there; rigid money wages end about 2.3x the
# market wage at year 15 when deficits dominate, 4.2x when owners' saving does.
#
# Calibration. Measured (Statistics Sweden, 2026): household debt 1.74 x disposable income; 76.8% of housing loans
# repricing within three months; mortgage rates 1.05 points over policy; deposits 0.91 x income; wages 0.84 of
# disposable income; GDP (current prices, last four quarters). Public support on Sweden's rules (decision 94; the primary
# sources in benefit_evidence, stored under "evidence"): 0.65 of the net money wage at exit in the first year (the layer's
# rate since September; the a-kassa's aggregate gross rate under its 34,000 SEK ceiling is about 0.51, a sensitivity), then
# a floor of 0.36 of the start's mean net wage indexed to prices (the riksnorm plus a one-room rent, 10,860 SEK a month, over
# SCB's 2025 mean net wage; 0.27 and 0.43 sensitivities); the 'wage' alternative's 0.50 after the first year (OECD-style net
# replacement rates for Sweden, approximate). Not measured here, stated: what families and friends cover (0.10 of the uncovered income under today's Swedish state support —
# no Swedish measure; a dial); savings of new job losers (3 months of net wage); the share of a loss drawn from
# savings while they last (0.5); spending per krona — job losers 0.8, supporters 0.5, borrowers squeezed 0.6, checks
# 0.4, a representative household 0.05 (Nordic lottery studies put the average near 0.5 in the first year and higher
# for households with little cash; approximate); the tax on wages 0.30; amortisation 2% of the debt a year; the
# labour-demand elasticity for rigid wages 0.4 (Lichter, Peichl and Siegloch 2015: median across studies 0.39, their
# bias-corrected long-run estimate 0.25). Debts follow income up (new borrowing
# keeps the debt-to-income ratio) and only amortise down: money debts are fixed, which is what debt deflation needs.
#
# The worlds (her decision, 2026-09-30): calibration (c)'s central economy, macro.central() — the open (domp) reading, the
# low root — through demand.world (the bridges refit on (c), Log 46, revised in Log 54, in bank_scenarios' two branches; on
# its feedback paths the bridges read at the start's required return, decision 96). The high root (the sensitivity) and (b)
# (the comparator, on its own bridges) are stored beside it; the household rules apply to (b)'s runs too, so its central rows
# move with them (its family rows run on the pinned 'wage' rule).
#
# The two rules, for money wages that fall 71-84% by year 15 (decisions 78-79, revised 2026-10-28: decision 94, Log 54):
#   benefits — Sweden's rules (benefit_base 'sweden', her call of 2026-10-28): the first year on the person's own net money
#     wage at exit, fixed for the spell (the a-kassa: Lag 2024:506 sets the base at 1/12 of the year before the claim; 80/70/65%
#     over 300 days; the 34,000 SEK ceiling a fixed sum, not modelled), then a floor indexed to prices (social assistance: the
#     riksnorm plus reasonable housing). Once money wages fall far enough the floor exceeds the wage lost, so coverage passes
#     100% and the job losers' drag goes to zero: a consequence of the price-indexed floor, not an artefact. The named
#     alternative, 'wage' (the rule from the refit to the revision): the replacement rate on the current net money wage, so
#     benefits follow wages (minimum benefits follow wages in the Netherlands and Denmark; in about 35 US jurisdictions the
#     maximum weekly benefit, a ceiling, is indexed to the state average wage). The a-kassa and the OECD's net replacement
#     rates set the base on the person's own wage at exit, which supports the exit-based rules, not re-basing on the current
#     wage. Kept as sensitivities: each cohort's real wage at exit ('exit') and the start's real wage indexed to prices
#     ('start', the rule before the refit). The family-based regime stays on 'wage' (pinned) until her call;
#   rigid wages — money wages fall at most wage_fall_max a year, and log employment falls by the elasticity times the log
#     excess (above), tracked in logs since the revision (decision 79 corrected: it was summed linearly, which understated
#     job loss by about 2% of the remaining jobs at the owners'-saving low). The elasticity is estimated on small wage changes;
#     here it is applied to log excesses of 0.8-1.5, an extrapolation. Before the refit wages could not fall at all and job
#     loss was linear in the summed refused cut, a share of the START's employment, which took employment to the layer's
#     floor (5% of the start's) from year 10.5; the floor stays as a guard and does not bind.
#
# Public data only: Statistics Sweden (above); the economy from results/calibration_c.json (BEA; code/calibration_c.py).
# Run from paths/:  ../venv/Scripts/python.exe code/households.py
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
    replacement_later: float = 0.50     # after the first year (the 'wage', 'exit' and 'start' rules)
    floor_share: float = 0.36           # 'sweden': the price-indexed floor after the first year, a share of the start's mean net wage
                                        # (the riksnorm plus a one-room rent over SCB's mean net wage: benefit_evidence)
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
    wage_fall_max: float = 4.0          # % a year: under rigid wages, the fastest money wages fall (a limit on the pace of cuts)
    labour_demand_elasticity: float = 0.4   # log employment lost per log point of wage held above its market level
    check_size: float = 0.0             # % of household disposable income a year, paid while the check runs
    check_quarters: int = 4
    check_trigger: float = 3.0          # checks start when unemployment is this many points above the start
    private_cap: float = 1.0            # most that family and friends can give, share of the net wages of those in work
    benefit_base: str = "sweden"        # "sweden" (decision 94, her call of 2026-10-28): Sweden's rules — the first year on the
                                        # person's own net money wage at exit, fixed for the spell (the a-kassa), then a floor of
                                        # floor_share of the start's mean net wage indexed to prices (the riksnorm plus rent);
                                        # "wage": the current net money wage (benefits follow wages; the rule from the refit to the
                                        # revision, the named alternative); "exit": each cohort's real net wage when it left work,
                                        # indexed to prices after; "start": the start's real net wage, indexed to prices (the rule
                                        # before the refit) — sensitivities


# A family-based regime: the state replaces less, family and friends cover half of the rest — but a network can carry a
# few people, not a mass exit, so what it gives is capped at a share of the net wages of those still in work; and the
# supporters include households with mortgages and little cash, so they cut their own spending by more of each krona.
# The lean replacement rates (0.40, then 0.25) stand roughly where the leanest OECD systems do against Sweden's
# (approximate); the half, the 10% cap and the 0.6 are assumptions — there is no Swedish measure of private support.
# Its benefits follow the current money wage (benefit_base "wage", pinned): her call of 2026-10-28 put Sweden's rules in the
# central run only, so every family variant keeps the rule it was set on until she decides otherwise (decision 94); the
# alternative, the lean state on Sweden's structure (a-kassa at exit, then a floor at its own later rate, 0.25), is stored as
# a sensitivity — under it the networks' cap binds only a few years before the floor outruns the wage.
FAMILY = dict(name="family-based support", replacement_first=0.40, replacement_later=0.25, benefit_base="wage", private=0.5,
              private_cap=0.10, mpc_supporter=0.6)

# Sweden's rules (decision 94): the primary sources, each read on 28 Oct 2026, and the numbers taken from them.
AKASSA = {"law": "Lag (2024:506) om arbetslöshetsförsäkring (decisions from 1 Oct 2025): 5 kap. 2 § and 3 kap. 12 § — the base is 1/12 of "
                 "earned income in the 12 months before the claim month (the person's own money wage at exit), set once for the "
                 "benefit period; 5 kap. 4-6 §§ — 80% for a member of at least 12 months (60% for 6-11, 50% otherwise); 5 kap. 10 § — "
                 "down 10 pp after 100 benefit days and 5 pp more after 200; 4 kap. 4 § — at most 300 days. "
                 "https://www.riksdagen.se/sv/dokument-och-lagar/dokument/svensk-forfattningssamling/lag-2024506-om-arbetsloshetsforsakring_sfs-2024-506/",
          "ceiling": "Förordning (2024:1350) om arbetslöshetsförsäkring 7 §: the highest income base 34,000 SEK (a month: IAF, "
                     "'Högsta ersättningsgrundande inkomst är 34 000 kronor i månaden'), a fixed sum. "
                     "https://www.riksdagen.se/sv/dokument-och-lagar/dokument/svensk-forfattningssamling/forordning-20241350-om-arbetsloshetsforsakring_sfs-2024-1350/ ; "
                     "https://www.iaf.se/lag-ratt/ny-arbetsloshetsforsakring-fran-1-oktober/",
          "ceiling_sek_month": 34000, "rates_pct": (80, 70, 65), "days": (100, 100, 60)}   # the model's first year: ~260 benefit days
RIKSNORM_2026 = {"single_sek_month": 5220, "cohabiting_sek_month": 8510,
                 "source": "Regeringen, 'Riksnorm för 2026 fastställd' (13 Nov 2025): every item +0.7% on 2025, set on Konsumentverket's "
                           "price and consumption surveys; housing, electricity, work travel, home insurance and union / a-kassa fees are "
                           "paid separately at reasonable cost. https://www.regeringen.se/artiklar/2025/11/riksnorm-for-2026-faststalld/ ; "
                           "https://www.socialstyrelsen.se/kunskapsstod-och-regler/omraden/ekonomiskt-bistand/riksnormen/"}
RENT_2026 = {"one_room_sek_month": 5640, "two_rooms_sek_month": 7742,
             "source": "SCB, Hyror i bostadslägenheter 2026 (2 Oct 2026), nationwide means. https://www.scb.se/hitta-statistik/"
                       "statistik-efter-amne/boende-bebyggelse-och-mark/bostader-och-boende/hyror-i-bostadslagenheter/pong/"
                       "statistiknyhet/hyror-i-bostadslagenheter-2026"}
WAGES_2025 = {"mean_sek_month": 42900, "median_sek_month": 38300,
              "source": "SCB, Lönespridning efter sektor och kön 2025, whole economy. https://www.scb.se/hitta-statistik/statistik-efter-"
                        "amne/arbetsmarknad/loner-och-arbetskostnader/lonestrukturstatistik-hela-ekonomin/pong/tabell-och-diagram/"
                        "lonespridning-efter-sektor-och-kon-2024/"}
EMPLOYMENT_THS = {"employed_15_74": 5277.8, "employees_15_74": 4776.4,
                  "source": "Eurostat lfsq_egaps (SE, total, 15-74, EMP / SAL, thousand persons; updated 2026-09-11), the mean of "
                            "2025Q3-2026Q2 (the quarters of sweden_start's wage bill), read 28 Oct 2026"}


def benefit_evidence(s0: dict) -> dict:
    """Decision 94's evidence: the rules and the numbers behind Support's floor_share and replacement_first, with the derivations
    (the floor as the riksnorm plus a one-room rent over the mean net wage, cross-checked on the layer's own wage bill; the
    a-kassa's aggregate first-year rate under its ceiling, on a lognormal fitted to SCB's mean and median)."""
    from scipy.stats import norm
    tax = Support().tax
    net_mean = WAGES_2025["mean_sek_month"] * (1 - tax)
    floor_sek = RIKSNORM_2026["single_sek_month"] + RENT_2026["one_room_sek_month"]
    net0_month = s0["wages_gross"] * (1 - tax) * 1e9 / 12                               # SEK a month, the layer's net wage bill
    per = {k: net0_month / (v * 1e3) for k, v in (("per employed person", EMPLOYMENT_THS["employed_15_74"]),
                                                   ("per employee", EMPLOYMENT_THS["employees_15_74"]))}
    rate = sum(r * d for r, d in zip(AKASSA["rates_pct"], AKASSA["days"])) / sum(AKASSA["days"]) / 100
    mu, mean = np.log(WAGES_2025["median_sek_month"]), WAGES_2025["mean_sek_month"]
    sig = float(np.sqrt(2 * np.log(mean / WAGES_2025["median_sek_month"])))
    c = AKASSA["ceiling_sek_month"]
    capped = (mean * norm.cdf((np.log(c) - mu - sig ** 2) / sig) + c * (1 - norm.cdf((np.log(c) - mu) / sig))) / mean
    return {"note": "decision 94 (her call of 2026-10-28: 'Sweden's rules'): the first year out of work on the person's own net money wage "
                    "at exit, fixed for the spell (the a-kassa); after it a floor indexed to prices (social assistance: the riksnorm plus "
                    "reasonable housing). The layer pays support on net0 (the aggregate net wage bill) times the share out of work, so a "
                    "share acts on the MEAN net wage; the floor is flat, so its bill does not depend on whom it replaces",
            "a_kassa": AKASSA, "riksnorm_2026": RIKSNORM_2026, "rent_2026": RENT_2026, "wages_2025": WAGES_2025,
            "employment_ths": EMPLOYMENT_THS,
            "floor_share": {"central": Support().floor_share,
                            "riksnorm_plus_one_room_sek_month": floor_sek, "mean_net_wage_sek_month": round(net_mean, 1),
                            "derived": round(floor_sek / net_mean, 4),
                            "cross_checks_on_the_layer_s_wage_bill": {k: round(floor_sek / v, 4) for k, v in per.items()},
                            "net_wage_bill_per_person_sek_month": {k: round(v, 0) for k, v in per.items()},
                            "sensitivity": {"0.27": "a cohabiting couple's per-person norm sharing a two-room flat: "
                                                    f"{(RIKSNORM_2026['cohabiting_sek_month'] + RENT_2026['two_rooms_sek_month']) / 2 / net_mean:.4f}",
                                            "0.43": "a single adult in a two-room flat: "
                                                    f"{(RIKSNORM_2026['single_sek_month'] + RENT_2026['two_rooms_sek_month']) / net_mean:.4f}"},
                            "note": "fixed from this evidence, not tuned on results; the median earner's 0.41 would overstate the flat "
                                    "floor's aggregate bill"},
            "replacement_first": {"central": Support().replacement_first,
                                  "a_kassa_mean_rate_first_260_days": round(rate, 4),
                                  "lognormal_sigma": round(sig, 4), "capped_base_over_mean_wage": round(float(capped), 4),
                                  "aggregate_gross_rate_under_the_ceiling": round(float(rate * capped), 4),
                                  "note": "0.65 kept (her call set the base, not the rate); the a-kassa's aggregate gross rate under "
                                          "today's 34,000 SEK ceiling is about 0.51 (net a few points lower: benefits get no earned-"
                                          "income tax credit), so 0.65 overstates the start's first-year bill by about a quarter; the "
                                          "fixed ceiling binds less as money wages fall (the effective rate rises toward 0.73). The "
                                          "ceiling is not modelled; the sensitivity runs 0.51"},
            "caveats": ["social assistance is means-tested by household (a partner's income, assets); the layer pays the floor to "
                        "everyone out of work after the first year",
                        "aktivitetsstöd (activity support within programmes) is ignored",
                        "the first year is 4 quarters against the a-kassa's 300 days (about 60 weeks)",
                        "electricity and insurance are left out of the floor",
                        "the a-kassa's nominal ceiling is not modelled",
                        "the support bill is reported, not financed: support_cost_pct_gdp feeds neither the macro block's deficit nor "
                        "the layer's 0.30 tax (the macro block's own fiscal bridge pays dependants 0.30 of a support basket in real "
                        "terms)"]}


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
    rec = {k: np.zeros(n) for k in ("P", "W", "W_market", "wage_excess", "employed", "out_new", "loss", "public_new", "private",
                                    "draw", "buffer", "debt", "ds", "ds_ref", "income", "mort_rate", "check", "d_out", "d_sup",
                                    "d_debt", "d_check", "level", "deposits", "extra_job_loss", "covered", "burden", "cap_binds")}
    rec["P"][0] = rec["W"][0] = rec["W_market"][0] = rec["employed"][0] = 1.0
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
        rec["W_market"][k] = rec["W_market"][k - 1] * (1 + pw / 100 * dt)       # the market money wage
        if sp.rigid_wages:
            # money wages close the gap to their market level as fast as they may, but fall no faster than wage_fall_max a year;
            # the excess, log(actual / market), grows while the market falls faster and closes once it does not — tracked in logs
            # (decision 79 corrected, Log 54: until the revision it was summed linearly, a first-order approximation)
            gm = np.log1p(pw * dt / 100)                                    # the market wage's log change this quarter
            pa = max((np.exp(gm - state["wage_excess"]) - 1) * 100 / dt, -sp.wage_fall_max)
            state["wage_excess"] += np.log1p(pa * dt / 100) - gm          # log(actual / market)
            pw = pa
        rec["wage_excess"][k] = state["wage_excess"]
        rec["W"][k] = rec["W"][k - 1] * (1 + pw / 100 * dt)
        du = -dmp.okun * gap[k - 1] / 100                            # cyclical job loss, share of the labour force
        base_emp = part[k] - du
        rigid = np.exp(-sp.labour_demand_elasticity * state["wage_excess"])   # the excess costs a share of the jobs left
        rec["extra_job_loss"][k] = base_emp * (1.0 - rigid)
        emp = max(base_emp * rigid, 0.05)
        rec["employed"][k] = emp
        out_new = max(1.0 - emp, 0.0)                                # out of work since the start, share of start employment
        cohorts[k] = max(out_new - rec["out_new"][k - 1], 0.0)
        rec["out_new"][k] = out_new
        net_w = net0 * rec["W"][k]                                   # a year's net wage bill if everyone still worked
        lost_wage = net_w * out_new
        first = cohorts[max(0, k - int(round(1 / dt)) + 1): k + 1].sum()
        if sp.benefit_base == "exit":                               # each cohort on its own real wage at exit (scaled to out_new)
            c_, tot = cohorts[: k + 1], cohorts[: k + 1].sum()
            rep = np.where(np.arange(k + 1) > k - int(round(1 / dt)), sp.replacement_first, sp.replacement_later)
            wr = rec["W"][: k + 1] / rec["P"][: k + 1]
            public = net0 * rec["P"][k] * float(np.sum(c_ * wr * rep)) * out_new / tot if tot > 1e-15 else 0.0
        elif sp.benefit_base == "sweden":                           # the a-kassa on the money wage at exit, then a price-indexed floor
            k1 = max(0, k - int(round(1 / dt)) + 1)                  # the cohorts still in their first year out of work
            c1 = cohorts[k1: k + 1]
            exit_money = float(np.sum(c1 * rec["W"][k1: k + 1])) / c1.sum() if c1.sum() > 1e-15 else rec["W"][k]
            public = net0 * (sp.replacement_first * min(first, out_new) * exit_money
                             + sp.floor_share * rec["P"][k] * max(out_new - first, 0.0))
        elif sp.benefit_base == "start":                            # the start's real net wage, indexed to prices
            public = net0 * rec["P"][k] * (sp.replacement_first * min(first, out_new) + sp.replacement_later * max(out_new - first, 0.0))
        elif sp.benefit_base == "wage":                             # the current net money wage: benefits follow wages
            public = net_w * (sp.replacement_first * min(first, out_new) + sp.replacement_later * max(out_new - first, 0.0))
        else:
            raise ValueError(f"benefit_base {sp.benefit_base!r}: 'sweden', 'wage', 'exit' or 'start'")
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


COMPARED = ("central", "rigid money wages", "no private support", "family-based support", "family-based, rigid money wages")
EXIT_COMPARED = ("central", "no private support", "family-based support", "family-based, no cap on what networks give")


def main():
    s0 = sweden_start()
    with open(os.path.join(ROOT, "results", "demand.json"), encoding="utf-8") as f:
        cyc = json.load(f)["sweden_cycle"]
    dmp = dm.Demand(kappa=cyc["kappa_per_pp_output_gap"], okun=cyc["okun"])
    e, cal = bs.economy("lo")
    worlds = {name: dm.world(br, truth, e=e) for name, (br, truth) in bs.SCEN.items()}
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
    out = {"sweden_start": s0, "support": central.__dict__, "evidence": benefit_evidence(s0), "calibration": cal, "scenarios": {}}
    runs = {}
    for name, mp in worlds.items():
        for vn, sp in variants.items():
            r = run(mp, dmp, sp, s0)
            out["scenarios"][f"{name} | {vn}"] = summary(r)
            runs[(name, vn)] = r
        out["scenarios"][f"{name} | demand layer alone (full pooling)"] = dm.summary(dm.run(mp, dmp))
    AUTOMATED = ("deficits dominate", "owners' saving dominates")
    # the named alternative to Sweden's rules (decision 94): benefits follow the current money wage, the layer's rule from the refit
    # (Log 46) to the revision (Log 54); the state-support variants (the family-based ones already run on it: FAMILY is pinned)
    out["alternative: benefits follow the current money wage"] = {
        "note": "benefit_base='wage': public support is the replacement rate (0.65 in the first year, 0.50 after) on the current net money "
                "wage, so benefits follow wages — the named alternative to Sweden's rules (decision 94), the default of 27-28 Oct 2026. "
                "The family-based variants are left out: they run on this rule already.",
        "scenarios": {f"{name} | {vn}": summary(run(worlds[name], dmp, replace(variants[vn], benefit_base="wage"), s0))
                      for name in AUTOMATED for vn in ("central", "rigid money wages", "no private support")}}
    # the evidence-set values' sensitivities, each fixed from the evidence (benefit_evidence), not tuned on results
    out["sensitivity: the floor's level"] = {
        "note": "Sweden's rules with the floor at 0.27 (a cohabiting couple's per-person riksnorm sharing a two-room flat) and 0.43 (a "
                "single adult in a two-room flat) of the start's mean net wage, against the central 0.36 (a single adult in a one-room "
                "flat). Not the default.",
        "scenarios": {f"{name} | {vn} | floor_share {fs:g}": summary(run(worlds[name], dmp, replace(variants[vn], floor_share=fs), s0))
                      for name in AUTOMATED for vn in ("central", "rigid money wages") for fs in (0.27, 0.43)}}
    out["sensitivity: the first year at the aggregate a-kassa rate"] = {
        "note": "Sweden's rules with the first year at 0.51, the a-kassa's aggregate gross rate under today's 34,000 SEK ceiling, against "
                "the layer's 0.65. Not the default.",
        "scenarios": {f"{name} | central": summary(run(worlds[name], dmp, replace(central, replacement_first=0.51), s0)) for name in AUTOMATED}}
    out["sensitivity: the family-based regime on Sweden's structure"] = {
        "note": "the family-based regime on Sweden's structure — its first year (0.40) on the money wage at exit, then a price-indexed floor "
                "at its own later rate (0.25) — in place of its pinned rule (benefits follow the current money wage): the open question "
                "for her under decision 94. Not the default.",
        "scenarios": {f"{name} | {vn}": summary(run(worlds[name], dmp, replace(variants[vn], benefit_base="sweden", floor_share=0.25), s0))
                      for name in AUTOMATED for vn in ("family-based support", "family-based, no cap on what networks give",
                                                       "family-based, rigid money wages")}}
    # the benefit rule's other alternatives (sensitivities, not defaults): each cohort's real wage at exit, and the start's real wage
    # (the rule before the refit, whose benefits outran the collapsing wage), the two automated worlds
    for base_, key, note in (
            ("exit", "sensitivity: benefits on the wage at exit",
             "benefit_base='exit': public support on each cohort's real net wage when it left work, indexed to prices after; the "
             "layer's rule (Sweden's, decision 94) pays the first year on the money wage at exit and then a price-indexed floor. "
             "Not the default."),
            ("start", "sensitivity: benefits on the start's real wage",
             "benefit_base='start': public support on the start's real net wage, indexed to prices — the rule before the refit, "
             "whose benefits exceed the wage lost once money wages fall far enough. Not the default.")):
        out[key] = {"note": note,
                    "scenarios": {f"{name} | {vn}": summary(run(worlds[name], dmp, replace(variants[vn], benefit_base=base_), s0))
                                  for name in ("deficits dominate", "owners' saving dominates") for vn in EXIT_COMPARED}}
    # rigid wages with no money-wage cut at all (the rule before the refit allowed none), the two automated worlds
    out["sensitivity: rigid wages, no money-wage cut"] = {
        "note": "wage_fall_max=0: money wages never fall (the rigidity before the refit), with the refit's job loss (log employment "
                "falls by the labour-demand elasticity times the log excess). Not the default.",
        "scenarios": {f"{name} | {vn}": summary(run(worlds[name], dmp, replace(variants[vn], wage_fall_max=0.0), s0))
                      for name in ("deficits dominate", "owners' saving dominates")
                      for vn in ("rigid money wages", "family-based, rigid money wages")}}
    # the high root (the sensitivity) and (b) (the comparator): the two automated worlds, the main variants
    for which, key in (("hi", "sensitivity: the high root"), ("b", "comparator: calibration (b)")):
        e2, cal2 = bs.economy(which)
        bb, scen = bs.base_bridges(which)
        sc = {}
        for name in ("deficits dominate", "owners' saving dominates"):
            br, truth = scen[name]
            mp = dm.world(br, truth, e=e2, base=bb)
            for vn in COMPARED:
                sc[f"{name} | {vn}"] = summary(run(mp, dmp, variants[vn], s0))
            sc[f"{name} | demand layer alone (full pooling)"] = dm.summary(dm.run(mp, dmp))
        out[key] = {"calibration": cal2, "scenarios": sc}
    with open(os.path.join(ROOT, "results", "households.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1)
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
    fig.get_layout_engine().set(rect=(0, 0.045, 1, 0.955))   # room for the two-line footer
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
    fig.text(0.01, 0.004, "households.py on the demand layer and the macro block's worlds on calibration (c), the central (open reading, low root; bridges refit on (c), Logs 46 and 54). "
             "Swedish household debt, fixation, margins, deposits and GDP from Statistics Sweden; replacement rates, private support and spending shares approximate or assumed.\n"
             "Benefits on Sweden's rules (the a-kassa on the money wage at exit, then a price-indexed floor; decision 94); under rigid wages money wages fall at most 4% a year and the log excess costs a share of the jobs left (decision 79; see the header).", fontsize=7.5)
    os.makedirs(os.path.join(ROOT, "figures"), exist_ok=True)
    fig.savefig(os.path.join(ROOT, "figures", "fig_households.png"), dpi=120)


if __name__ == "__main__":
    main()
