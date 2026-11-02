# lvt_fi.py - question 1, Finland: a land-value tax funding the same flat dividend, run through the rebuilt VAT-bridge
# machinery (consumption/rebuild/code/bridge.py, imported unchanged) beside the Finnish VAT bridge itself.
#
# The tax: a credible, permanent charge tau on announcement-date land values, tau = phi * r, with r the land
# rent-to-value rate (the 10-year government bond yield, the paper's measure; +1.5 points as its band) and phi the
# share of land rent taken. Revenue funds a flat dividend per payment share (adult 1, child 0.3) on the HBS 2022
# population, the VAT bridge's payment rule. There is no household microdata here: land, liquidity and mortgage
# debt come from the published wealth-survey tables (vtutk 151u by income decile, 151z by tenure, 2023 wave),
# calibrated to the household balance sheet (rtp 11zx: N211 land, N111 residential buildings) and carried to 2022
# with the N211 land series. Deciles are paired into quintiles to meet the HBS 2022 household quintiles.
#
# Plain functions plus constants (no classes); a "model" is bridge.py's plain dict. Units: euros; land values per
# household (annual amounts per household) until the bridge converts them to euros per payment share per month.
# Every judgment input is a named constant below, with its band; run_lvt_fi.py varies each one.

# %% setup
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent                     # consumption/lvt/code
LVT = HERE.parent                                          # consumption/lvt
THREAD = LVT.parent                                        # consumption
REPO = THREAD.parent
sys.path.insert(0, str(THREAD / "rebuild" / "code"))
sys.path.insert(0, str(THREAD / "code"))

import numpy as np
import pandas as pd
from scipy.stats import norm

import bridge as B
import common

TIDY = B.TIDY
OUT = LVT / "out"
FIG = LVT / "figures"
DEC = [f"d{i:02d}" for i in range(1, 11)]
Q = list(B.FI_Q)

# %% constants: accounting (identities and published inputs)
YEAR_FLOW = 2022                 # HBS 2022: the post's Finnish flow year
YEAR_SURVEY = 2023               # wealth survey wave (vtutk 151u/151z), end-of-year values
PHI_FULL = 0.98                  # full capture (design memo 1.1: the 2% is an assessment-error buffer)
GAMMA, DELTA = 0.02, 0.05        # T4's dial: increment-only capture = phi * gamma / delta
YIELD_SPREAD = 1.5               # the paper's band on the yield measure (feasibility_kappa.py: gs10 + 1.5)
LAMBDAS = (0.0, 0.35, 1.0)       # the post's levy-perception scenarios
PASS_THROUGH = {"low": 0.8, "mid": 0.9, "high": 1.0}     # post: 80-100% pass-through of the VAT step
# T11 / memo 7.1 price paths at phi = 0.98 (three-taxes/code/fiscal_napkin.py: gamma 2%, delta 5%, discrete annual
# timing); one convention for every design, as the US unit: phase-ins AND increment-only grandfathering read from it.
SHOCK_FILE = REPO / "three-taxes" / "data" / "lvt_shock.csv"
SHOCK_INCREMENT = "increment-only (grandfather r0)"
HW_ITEMS = ["main_residence", "other_residential_property", "free_time_residences"]
FFB_ITEM = "forest_farmland_business"
# The ten-year yield: Eurostat's EMU convergence-criterion series (10-year benchmark, Maastricht definition) for
# Finland, annual and monthly, and the ECB's identical statistic as a second publisher. Fetched only through
# consumption/code/common.py's fetch() (vendored once, then offline); FRED is not used.
YIELD_FILES = {
    "eurostat_annual": ("eurostat", "data/irt_lt_mcby_a_FI.json",
                        "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/irt_lt_mcby_a?format=JSON&lang=EN&geo=FI",
                        "Eurostat irt_lt_mcby_a (JSON-stat 2.0), geo FI: EMU convergence criterion series, long-term government "
                        "bond yields (Maastricht definition, 10-year benchmark), annual average, percent",
                        "consumption/lvt (lvt_fi.py): Finnish 10-year yield for the land rent-to-value rate"),
    "eurostat_monthly": ("eurostat", "data/irt_lt_mcby_m_FI.json",
                         "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/irt_lt_mcby_m?format=JSON&lang=EN&geo=FI",
                         "Eurostat irt_lt_mcby_m (JSON-stat 2.0), geo FI: EMU convergence criterion series, long-term "
                         "government bond yields (Maastricht definition, 10-year benchmark), monthly average, percent",
                         "consumption/lvt (lvt_fi.py): monthly check of the annual mean"),
    "ecb_monthly": ("ecb", "data/IRS_M.FI.L.L40.CI.0000.EUR.N.Z.csv",
                    "https://data-api.ecb.europa.eu/service/data/IRS/M.FI.L.L40.CI.0000.EUR.N.Z?format=csvdata",
                    "ECB Data Portal, dataset IRS, series M.FI.L.L40.CI.0000.EUR.N.Z (CSV): long-term interest rate for "
                    "convergence purposes, Finland, 10 years, monthly average, percent per annum",
                    "consumption/lvt (lvt_fi.py): cross-check of the Eurostat series (same statistic, second publisher)"),
}

# %% constants: judgment inputs (each is varied in run_lvt_fi.py; bands in the comments)
# Land share of dwelling values (main residence, other residential property, free-time residences). Central: the
# paper's residual construction (market value of household dwellings minus their structures at current cost),
# with the survey's market values and the balance sheet's N111 (computed, not set here). Band: 0.13 = the
# own-plot vs rented-plot price gap of old housing-company dwellings within region groups (a lower bound: municipal
# ground rents sit below market, and rented plots cluster in high-price cities); 0.24 = N211 / (N211 + N111) in
# 2023 (an upper bound: N211 also holds forest and farmland). Within the band the N211 total is held, so the
# forest/farmland/business share moves the other way.
S_D_BAND = (0.13, 0.24)
# Land share of the survey's forest + farmland + business item. Central: the residual N211 leaves after dwelling
# land (computed). Band 0.5-1.5 at a fixed dwelling share (the total then departs from N211): the item mixes forest
# at the bare-land taxation value (below market, per the publisher), farmland at purchase prices, and business net
# wealth (mostly not land); forest at market would also carry standing timber, which is not land.
S_F_BAND = (0.5, 1.5)
# Wealth-effect propensity per euro of wealth per year (the post's fn 31 range 2-5 cents; central = midpoint).
MPW = {"low": 0.02, "mid": 0.035, "high": 0.05}
# Housing-collateral response per euro per year for mortgaged owners whose LTV crosses a borrowing threshold, the US
# unit's band after its T4-overlap fix: low 4.7c (Aladangady 2017), mid 6c and lit_high 7c (Mian-Rao-Sufi 2013: 5-7c),
# stress 10c (judgment, no source). Those estimates come from house-price changes that carry no tax bill. Under an LVT
# an owner-occupier's capitalized land loss IS the present value of the bill (T4), which the flow already charges at
# the owner's MPC, so the clean concept is the crossers' lost BORROWING CAPACITY (a credit effect on top of the bill);
# applied to their lost equity the same cents count the bill twice ("includes the T4 overlap"), a band edge only.
MPC_COLL = {"low": 0.047, "mid": 0.06, "lit_high": 0.07, "stress": 0.10}
LTV_THRESHOLDS = (0.80, 0.90, 1.00)
# Within-decile LTV of mortgaged owners: log-normal, median = LTV_MEDIAN_RATIO x the decile's aggregate LTV
# (sum of loans / sum of values), dispersion LTV_SIGMA. No Finnish microdata; the pair (1.1, 0.6) is the one that
# best reproduces the US unit's microdata crossers when run on US decile aggregates (out/fi_lvt_collateral_method
# _check.csv: lost equity within -3% to -17%, counts -14% to -33%), so it is a borrowed shape. Band 0.5-0.8.
LTV_MEDIAN_RATIO = 1.1
LTV_SIGMA = {"low": 0.5, "mid": 0.6, "high": 0.8}
# Hand-to-mouth (KVW 2014): liquid assets at or below half a pay period's income. Finnish pay is monthly, so the
# main threshold is income/24 (half a month); income/52 (the US unit's biweekly main) and income/12 are the band.
# Liquid assets = deposits (the survey's only liquid item with quartiles); median disposable income of the decile
# (or tenure group) as each household's income. Judgment: owners' HtM rate inside a decile = the decile's rate
# scaled by the national owner/all ratio for its outright/mortgaged mix (151z), since 151u does not cross tenure.
HTM_DIVISOR = {"half_month": 24.0, "half_biweekly": 52.0, "one_month": 12.0}
# MPC of payers who are not liquidity-constrained, in the variant where they draw on wealth whatever their income
# (the verifier's point: the post's schedule was pinned where VAT payers sit, at the top). mid = the schedule's own
# top-quintile value (they behave like the top); low = 0.25 (judgment: below Fagereng-Holm-Natvik's first-year
# average of about one-half, which falls with liquid assets); high = the high schedule's top value.
MPC_UNCONSTRAINED = {"low": 0.25, "mid": None, "high": None}       # mid/high filled from bridge.fi_mpc_schedules()
# VAT payers inside a quintile (for the household-level grades): VAT-able consumption per share log-normal around
# the quintile mean with dispersion SIGMA_C (no HBS microdata here; judgment), band 0.3-0.6.
SIGMA_C = {"low": 0.30, "mid": 0.45, "high": 0.60}
# The loop (T5): land share of a rent change (central = the calibrated dwelling land share, band 0.13-0.30) and the
# share of rental land that household landlords hold (the rest belongs to corporations, municipalities and
# non-profits, outside a household-land tax): central 0.55 from the balance sheet (survey other residential
# property against S11 + S15 residential buildings), band 0.4-0.7.
LS_RENT_BAND = (0.13, 0.30)
HH_LANDLORD_SHARE = {"low": 0.40, "mid": 0.55, "high": 0.70}
# Tenure-aware baskets: lines that are structural by tenure (renters pay rent; owners carry imputed rent, interest on
# housing loans and housing-company maintenance charges). No HBS tenure-by-quintile table exists, so the split is
# structural (0/100), the US unit's CE ratios being 0.8% and 0.6%.
RENTER_ONLY = ["04.1 Actual rents"]
OWNER_ONLY = ["04.2 Imputed rentals (off-chart)", "04.6 Interest on housing loans (off-chart)"]
OWNER_PART = {"04.4 Water & misc. dwelling services": "maintenance charges of housing companies"}


# %% loading: wealth survey, balance sheet, national accounts, yields
def wealth_long(table="deciles"):
    f = {"deciles": "fi_wealth_2023_deciles.csv", "tenure": "fi_wealth_2023_tenure.csv"}[table]
    return pd.read_csv(TIDY / f)


def wv(component, measure="mean", table="deciles", df=None):
    """One wealth-survey item as a Series indexed by decile (d01..d10, total) or tenure group. Means are per
    household over ALL households of the group; median/p25/p75 are conditional on holding (table notes)."""
    d = wealth_long(table) if df is None else df
    key = "decile" if table == "deciles" else "tenure"
    s = d[(d["component"] == component) & (d["measure"] == measure)].set_index(key)["value"].astype(float)
    if s.empty:
        raise KeyError((component, measure, table))
    return s


def balance_sheet(sector="S14", instrument="N211", year=YEAR_FLOW, measure="stock"):
    """Statistics Finland financial accounts table 11zx: non-financial assets, EUR million, end of year."""
    d = pd.read_csv(TIDY / "fi_nonfin_assets_long.csv")
    r = d[(d["sector"] == sector) & (d["instrument"] == instrument) & (d["year"] == year) & (d["measure"] == measure)]
    if len(r) != 1:
        raise KeyError((sector, instrument, year, measure))
    return float(r["value"].iloc[0])


def na_consumption(code="0", year=YEAR_FLOW, measure="current_prices", transaction="P31DCK"):
    """Statistics Finland annual national accounts (ntp 15ag), household consumption by COICOP 2018, EUR million."""
    d = pd.read_csv(TIDY / "fi_na_hfce_coicop2018_long.csv", dtype={"coicop_code": str})
    r = d[(d["transaction"] == transaction) & (d["coicop_code"] == code) & (d["year"] == year) & (d["measure"] == measure)]
    if len(r) != 1:
        raise KeyError((code, year, measure))
    return float(r["value"].iloc[0])


def consumption_deflator(year):
    """Household consumption deflator change in `year` (current / previous-year prices, P31DCK total)."""
    return na_consumption("0", year, "current_prices") / na_consumption("0", year, "previous_year_prices")


def housing_services(year=YEAR_FLOW):
    """National-accounts housing services: actual (04.1) plus imputed (04.2) rentals, EUR million."""
    return na_consumption("041", year) + na_consumption("042", year)


def jsonstat_series(path):
    """A one-series JSON-stat 2.0 file (Eurostat) as a Series indexed by its time codes."""
    j = json.loads(Path(path).read_text())
    t = j["dimension"]["time"]["category"]["index"]
    inv = {v: k for k, v in t.items()}
    return pd.Series({inv[int(k)]: float(v) for k, v in j["value"].items()}).sort_index()


def fi_yields():
    """Finland's 10-year government bond yield, % a year, by year: Eurostat annual series, the mean of Eurostat's
    monthly series, and the mean of the ECB's monthly series (each with its month count)."""
    p = {k: common.fetch(*v) for k, v in YIELD_FILES.items()}
    a = jsonstat_series(p["eurostat_annual"])
    mo = jsonstat_series(p["eurostat_monthly"])
    e = pd.read_csv(p["ecb_monthly"], usecols=["TIME_PERIOD", "OBS_VALUE"])
    e = pd.Series(e["OBS_VALUE"].astype(float).values, index=e["TIME_PERIOD"].astype(str))
    ym = mo.groupby(mo.index.str[:4]).agg(["mean", "count"])
    ye = e.groupby(e.index.str[:4]).agg(["mean", "count"])
    out = pd.DataFrame({"eurostat_annual": a, "eurostat_monthly_mean": ym["mean"], "eurostat_months": ym["count"],
                        "ecb_monthly_mean": ye["mean"], "ecb_months": ye["count"]})
    out.index = out.index.astype(int)
    out.index.name = "year"
    return out.sort_index()


def yield_of(year, spread=0.0, ylds=None):
    """Annual yield (Eurostat annual series), in decimal, plus a spread in points."""
    y = fi_yields() if ylds is None else ylds
    return (float(y.loc[year, "eurostat_annual"]) + spread) / 100.0


# %% land: shares, calibration, holdings by decile and quintile
def survey_totals(df=None):
    """Households per decile and the survey's mean values of the land-bearing items (2023 euros, per household);
    totals in EUR million over the survey population."""
    d = wealth_long("deciles") if df is None else df
    N = wv("net_wealth", "households_holding", df=d).reindex(DEC)
    comps = {c: wv(c, df=d).reindex(DEC) for c in HW_ITEMS + [FFB_ITEM]}
    tot = {c: float((v * N).sum()) / 1e6 for c, v in comps.items()}
    return N, comps, tot


def land_shares(rule="residual", s_d=None, s_f=None, year=YEAR_SURVEY):
    """Land shares of the survey items (accounting with judgment inputs):
    'residual'  s_d = 1 - N111 / (survey dwelling value): the paper's land residual (market value of dwellings minus
                structures at current cost); s_f = (N211 - s_d x dwellings) / forest-farmland-business, so the total
                equals the balance sheet's household land N211 in the survey year.
    'fix_sd'    s_d given, s_f from N211 (the total held at N211).
    'fixed'     both given (the total departs from N211)."""
    _, _, tot = survey_totals()
    HW = sum(tot[c] for c in HW_ITEMS)
    FFB = tot[FFB_ITEM]
    n211, n111 = balance_sheet("S14", "N211", year), balance_sheet("S14", "N111", year)
    if rule == "residual":
        s_d = 1.0 - n111 / HW
        s_f = (n211 - s_d * HW) / FFB
    elif rule == "fix_sd":
        s_f = (n211 - s_d * HW) / FFB
    elif rule != "fixed":
        raise ValueError(rule)
    land = s_d * HW + s_f * FFB
    return dict(rule=rule, s_d=float(s_d), s_f=float(s_f), dwellings_meur=HW, ffb_meur=FFB, n211_meur=n211,
                n111_meur=n111, land_meur=land, land_over_n211=land / n211, year=year)


def carry_factor(rule="end2022"):
    """2023 survey land -> 2022 with the balance-sheet land series (S14 N211): end-2022 / end-2023 stock (main),
    or the mean of end-2021 and end-2022 (a mid-2022 level) / end-2023."""
    n23 = balance_sheet("S14", "N211", YEAR_SURVEY)
    if rule == "end2022":
        return balance_sheet("S14", "N211", 2022) / n23
    if rule == "mid2022":
        return 0.5 * (balance_sheet("S14", "N211", 2021) + balance_sheet("S14", "N211", 2022)) / n23
    raise ValueError(rule)


def land_by_decile(sh, carry):
    """Land per household by wealth-survey income decile, euros of the flow year: each item x its land share x the
    carry factor. B1 = residential land (main residence, other residential property, free-time residences),
    B2 = B1 + forest, farmland and business land = all household land (N211 by construction in the survey year)."""
    N, comps, _ = survey_totals()
    df = pd.DataFrame(index=DEC)
    df.index.name = "decile"
    df["households"] = N
    df["L_main"] = sh["s_d"] * comps["main_residence"] * carry
    df["L_ore"] = sh["s_d"] * comps["other_residential_property"] * carry
    df["L_ftr"] = sh["s_d"] * comps["free_time_residences"] * carry
    df["L_ffb"] = sh["s_f"] * comps[FFB_ITEM] * carry
    df["B1"] = df["L_main"] + df["L_ore"] + df["L_ftr"]
    df["B2"] = df["B1"] + df["L_ffb"]
    return df


BASE_COLS = {"B1": ["L_main", "L_ore", "L_ftr"], "B2": ["L_main", "L_ore", "L_ftr", "L_ffb"]}
NONOCC_COLS = {"B1": ["L_ore", "L_ftr"], "B2": ["L_ore", "L_ftr", "L_ffb"]}


def pair_quintiles(x):
    """Decile values (per household) -> quintile values: the mean of each decile pair (D1, D2 -> q1, ...). The
    survey deciles hold equal households (294,751-295,368), so the pair mean equals the pooled pair within 0.1%."""
    x = pd.Series(x, dtype=float).reindex(DEC)
    return pd.Series([(x[DEC[2 * i]] + x[DEC[2 * i + 1]]) / 2.0 for i in range(5)], index=Q)


def decile_to_quintile_key():
    return pd.Series(np.repeat(Q, 2), index=DEC)


def plot_gap_evidence(year=YEAR_FLOW):
    """Own-plot vs rented-plot price gap per m2 (ashi 12de new and 13mw old dwellings in housing companies): a buyer
    on a rented plot does not buy the land and pays ground rent instead, so 1 - rented/own measures the capitalized
    plot. Confounded by location and building differences (the publisher warns m2 prices describe price levels)."""
    d = pd.read_csv(TIDY / "fi_land_indicators_long.csv")
    rows = []
    for st in ["ashi 13mw", "ashi 12de"]:
        x = d[(d["source_table"] == st) & (d["year"] == year) & d["measure"].str.startswith("Price")]
        if st == "ashi 12de":
            x = x[x["rooms"] == "Total"]
        n = d[(d["source_table"] == st) & (d["year"] == year) & d["measure"].str.startswith("Number")]
        if st == "ashi 12de":
            n = n[n["rooms"] == "Total"]
        pv = x.pivot_table(index=["region", "building_type"], columns="plot_ownership", values="value", aggfunc="first")
        nv = n.pivot_table(index=["region", "building_type"], columns="plot_ownership", values="value", aggfunc="first")
        for (reg, bt), r in pv.iterrows():
            if pd.isna(r.get("Own plot")) or pd.isna(r.get("Rented plot")):
                continue
            nn = nv.loc[(reg, bt)] if (reg, bt) in nv.index else pd.Series(dtype=float)
            rows.append(dict(source_table=st, year=year, region=reg, building_type=bt, own_plot_eur_m2=r["Own plot"],
                             rented_plot_eur_m2=r["Rented plot"], gap=1.0 - r["Rented plot"] / r["Own plot"],
                             sales_own=nn.get("Own plot", np.nan), sales_rented=nn.get("Rented plot", np.nan),
                             sales_total=nn.get("Plot forms in total", np.nan)))
    return pd.DataFrame(rows)


def plot_price_evidence(years=(2021, 2022, 2023)):
    """Single-family house plots (kihi 11jc): mean EUR/m2, mean plot area and the implied mean plot price by region."""
    d = pd.read_csv(TIDY / "fi_land_indicators_long.csv")
    x = d[(d["source_table"] == "kihi 11jc") & d["year"].isin(years)]
    pv = x.pivot_table(index=["region", "year"], columns="measure", values="value", aggfunc="first")
    out = pd.DataFrame({"eur_m2_mean": pv["Price per square meter (EUR/m2)"], "eur_m2_median": pv["Medianprice"],
                        "plot_m2_mean": pv["Average area m2"], "sales": pv["Number"]})
    out["plot_price_mean_eur"] = out["eur_m2_mean"] * out["plot_m2_mean"]
    return out.reset_index()


# %% tier 1: accounting through bridge.net_from_base
def land_per_share_month(m, land_q_hh):
    """Annual land value per household by quintile -> land value per payment share, divided by 12 (the bridge's
    per_share_monthly unit), so that tau x this = euros per share per month at an annual rate tau on land value."""
    return B.per_share_monthly(m, land_q_hh)


def mean_land_ps(m, land_q_hh):
    """Population-mean land value per payment share (euros), under the model dict's own weights."""
    return 12.0 * float((m["w"] * land_per_share_month(m, land_q_hh)).sum())


def tau_for_dividend(m, land_q_hh, dividend):
    """Annual charge on land value (tau = phi x r) that funds `dividend` euros per share per month."""
    return 12.0 * dividend / mean_land_ps(m, land_q_hh)


def lvt_accounting(m, land_q_hh, tau):
    """The post's accounting tier with land value as the base: bill_q = tau x land per share, dividend =
    sum_q w_q bill_q, net_q = dividend - bill_q (bridge.net_from_base; balanced under the dict's weights)."""
    acc = B.net_from_base(land_per_share_month(m, land_q_hh), m["w"], tau, m["budget"])
    acc = acc.rename(columns={"base": "land_value_ps_over12", "tax": "bill", "base_pct_budget": "land_value_ps_over12_pct_budget"})
    acc["land_value_ps"] = 12.0 * acc["land_value_ps_over12"]
    acc["tau"] = tau
    return acc


# %% inside the deciles: owners pay, non-owners receive (a parametric split, no microdata)
def owner_model(land_dec_hh, shares_dec, mean_ps, p_own, sigma):
    """Within each wealth decile, owners of a main residence (share p_own) hold all of the decile's land, log-normally
    spread with dispersion sigma (from the main-residence quartiles of holders). Per payment share the net is
    tau x (mean land per share - land per share), so a household pays net iff its land exceeds L* = mean_ps x shares
    (rate-invariant). Returns per household of the decile, in LAND units (multiply by tau for euros a year):
    receipts of non-owners, net receipts of owner-recipients, net payments of owner-payers, and the payer shares.
    Approximation: renters' own land (2.5% of household land nationally, 151z) is assigned to the decile's owners."""
    L = pd.Series(land_dec_hh, dtype=float).reindex(DEC)
    p = pd.Series(p_own, dtype=float).reindex(DEC)
    sg = pd.Series(sigma, dtype=float).reindex(DEC)
    Ls = mean_ps * pd.Series(shares_dec, dtype=float).reindex(DEC)
    Lown = L / p
    mu = np.log(Lown) - sg ** 2 / 2.0
    z = (np.log(Ls) - mu) / sg
    P_pay = 1.0 - norm.cdf(z)
    E_above = Lown * (1.0 - norm.cdf(z - sg))               # E[L 1{L > L*}] per owner
    pay = E_above - Ls * P_pay                               # E[(L - L*) 1{L > L*}]
    recv_own = Ls * (1.0 - P_pay) - (Lown - E_above)         # E[(L* - L) 1{L < L*}]
    out = pd.DataFrame({"p_own": p, "sigma": sg, "L_hh": L, "L_per_owner": Lown, "L_star": Ls,
                        "payer_share_of_owners": P_pay, "payer_share_of_households": p * P_pay,
                        "recv_nonowner": (1.0 - p) * Ls, "recv_owner": p * recv_own, "pay_owner": p * pay}, index=DEC)
    out["net"] = out["recv_nonowner"] + out["recv_owner"] - out["pay_owner"]
    out["net_check"] = Ls - L                               # identity: equals net
    return out


def lognormal_split(mean, threshold, sigma):
    """For x log-normal with the given mean and dispersion: E[(x - t) 1{x > t}], E[(t - x) 1{x < t}], P(x > t)."""
    mean, threshold = np.asarray(mean, float), np.asarray(threshold, float)
    mu = np.log(mean) - sigma ** 2 / 2.0
    z = (np.log(threshold) - mu) / sigma
    p = 1.0 - norm.cdf(z)
    above = mean * (1.0 - norm.cdf(z - sigma)) - threshold * p
    below = threshold * (1.0 - p) - (mean - mean * (1.0 - norm.cdf(z - sigma)))
    return above, below, p


# %% liquidity: hand-to-mouth shares from the published quartiles
def lognormal_cdf_from_quartiles(x, p25, p50, p75):
    s = (np.log(p75) - np.log(p25)) / (2.0 * norm.ppf(0.75))
    return norm.cdf((np.log(x) - np.log(p50)) / s), s


def htm_by_decile(divisor=24.0):
    """Share of households whose deposits are at or below disposable income / divisor, by decile: deposits
    log-normal through the published quartiles (holders), non-holders counted as hand-to-mouth, the decile's
    median disposable income as the income. Also the mean liquid assets (deposits + listed shares and funds + other
    financial assets) in months of mean disposable income."""
    q = {k: wv("deposits", k).reindex(DEC) for k in ("p25", "median", "p75")}
    part = wv("deposits", "participation_rate_pct").reindex(DEC) / 100.0
    inc_med = wv("disposable_income", "median").reindex(DEC)
    cdf, s = lognormal_cdf_from_quartiles(inc_med / divisor, q["p25"], q["median"], q["p75"])
    h = (1.0 - part) + part * cdf
    liq = (wv("deposits") + wv("listed_shares_and_mutual_funds") + wv("other_financial_assets")).reindex(DEC)
    inc = wv("disposable_income").reindex(DEC)
    return pd.DataFrame({"htm_share": h, "deposit_sigma": s, "deposits_median_holders": q["median"],
                         "income_median": inc_med, "deposit_months_at_median": 12.0 * q["median"] / inc_med,
                         "liquid_mean": liq, "income_mean": inc, "liquid_months_of_mean_income": 12.0 * liq / inc}, index=DEC)


def htm_by_tenure(divisor=24.0):
    rows = {}
    for ten in ["all", "outright_owner", "owner_with_mortgage", "renter_or_other"]:
        q = {k: wv("deposits", k, "tenure")[ten] for k in ("p25", "median", "p75")}
        part = wv("deposits", "participation_rate_pct", "tenure")[ten] / 100.0
        inc = wv("disposable_income", "median", "tenure")[ten]
        cdf, s = lognormal_cdf_from_quartiles(inc / divisor, q["p25"], q["median"], q["p75"])
        rows[ten] = dict(htm_share=(1.0 - part) + part * float(cdf), deposit_sigma=float(s), deposits_median=q["median"],
                         income_median=inc, households=wv("disposable_income", "households_holding", "tenure")[ten])
    return pd.DataFrame(rows).T


def owner_counts():
    """Owners of a main residence, owners with a housing loan (= households with housing loans: only owners have
    them, per the documentation; the counts agree with 151z exactly) and outright owners, by decile."""
    n_own = wv("main_residence", "households_holding").reindex(DEC)
    n_mort = wv("housing_loans", "households_holding").reindex(DEC)
    return pd.DataFrame({"n_households": wv("net_wealth", "households_holding").reindex(DEC), "n_owners": n_own,
                         "n_mortgaged": n_mort, "n_outright": n_own - n_mort})


def htm_owners(divisor=24.0):
    """Owners' hand-to-mouth share by decile (judgment): the decile's share scaled by the national ratio of owners'
    to all households' shares for the decile's own outright/mortgaged mix (151z), capped at 1."""
    hd = htm_by_decile(divisor)["htm_share"]
    ht = htm_by_tenure(divisor)["htm_share"]
    c = owner_counts()
    mix = (c["n_outright"] * ht["outright_owner"] + c["n_mortgaged"] * ht["owner_with_mortgage"]) / c["n_owners"]
    return (hd * mix / ht["all"]).clip(upper=1.0)


# %% MPC grades: decile-netted (the post's method) and household-level splits inside the quintiles
def graded_dC(net, recv, pay, mpc, h_pay, grade, m_u=None):
    """Consumption change per share per month by quintile (arrays over q1..q5):
    'post'    mpc_q x net_q (decile-netted: every flow in the quintile at the schedule's value)
    'liq'     recipients at the schedule; payers at 1.0 if hand-to-mouth, else at the schedule
    'wealth'  recipients at the schedule; payers at 1.0 if hand-to-mouth, else at m_u whatever their income
              (unconstrained payers draw on wealth)"""
    net, recv, pay = (np.asarray(v, float) for v in (net, recv, pay))
    mpc, h = np.asarray(mpc, float), np.asarray(h_pay, float)
    if grade == "post":
        return mpc * net
    if grade == "liq":
        return mpc * recv - (h + (1.0 - h) * mpc) * pay
    if grade == "wealth":
        return mpc * recv - (h + (1.0 - h) * m_u) * pay
    raise ValueError(grade)


def shock_of(m, dC):
    return pd.Series(np.asarray(dC, float) / m["budget"].values, index=m["budget"].index)


# %% tenure-aware baskets (an extension, as in the US unit)
def fi_tenure_model(m, p_owner_q, food_map="F3"):
    """Owner and renter baskets per share inside each quintile: renter-only lines with renters, owner-only lines
    (and the housing-company charges inside 04.4) with owners, every other line at the quintile mean, so that
    p C^o + (1 - p) C^r = C. Elasticities re-evaluated at each basket with bridge.fi_eta_table (Working model at the
    basket's own shares). Returns {'owner': (C, eta), 'renter': (C, eta)}."""
    C = m["C"]
    po = pd.Series(np.asarray(p_owner_q, float), index=C.columns)
    pr = 1.0 - po
    Co, Cr = C.copy(), C.copy()
    for g in RENTER_ONLY:
        Cr.loc[g] = C.loc[g] / pr
        Co.loc[g] = 0.0
    for g in OWNER_ONLY:
        Co.loc[g] = C.loc[g] / po
        Cr.loc[g] = 0.0
    for g, line in OWNER_PART.items():
        part = m["lines"].loc[line, C.columns]
        Co.loc[g] = C.loc[g] - part + part / po
        Cr.loc[g] = C.loc[g] - part
    out = {}
    for name, Ct in [("owner", Co), ("renter", Cr)]:
        mt = dict(m, C=Ct, budget=Ct.sum())
        eta_t, _ = B.fi_eta_table(mt, food_map)
        out[name] = (Ct, eta_t)
    return out


def shifts_tenure_aware(m, tm, dc_owner, dc_renter, p_owner_q):
    """Category shifts (euros per share per month, population mean) with each tenure group's consumption change
    spread over its own basket: sum_q w_q [p_q dc_o,q eta^o C^o / B^o + (1 - p_q) dc_r,q eta^r C^r / B^r].
    dc_* are per share of the tenure group (payment shares split by tenure in proportion to households)."""
    po = pd.Series(np.asarray(p_owner_q, float), index=m["C"].columns)
    out = pd.Series(0.0, index=m["C"].index)
    for name, pt, dc in [("owner", po, dc_owner), ("renter", 1.0 - po, dc_renter)]:
        Ct, eta_t = tm[name]
        share = Ct.div(Ct.sum(), axis=1) * eta_t
        out = out + (share * (m["w"] * pt * pd.Series(np.asarray(dc, float), index=Ct.columns)).values).sum(axis=1)
    return out


# %% stock channel: capitalization, collateral, non-occupiers
def pv_share(design="immediate", shock_table=None):
    """Present value captured at announcement per unit of phi: 'immediate' 1 (credible permanent capture, T4);
    'increment' (increment-only grandfathering) and 'phasein_<T>y': the lvt_shock.csv price drop at phi = 0.98 divided
    by 0.98 (the PV is linear in phi; increment-only 0.404 / 0.98, against the continuous gamma/delta = 0.4)."""
    if design == "immediate":
        return 1.0
    t = pd.read_csv(SHOCK_FILE) if shock_table is None else shock_table
    if design == "increment":
        row = t[t["design"] == SHOCK_INCREMENT]
    elif design.startswith("phasein_"):
        row = t[t["design"] == f"phase-in {design.split('_')[1]}"]
    else:
        raise ValueError(design)
    assert len(row) == 1, design
    return float(row["price_drop"].iloc[0]) / PHI_FULL


def loss_fraction(phi, design="immediate"):
    """Share of announcement-date land value lost: phi x pv_share, capped at 1 (above phi = 1 the land is worthless
    and the rest of the charge falls on the holder, dwelling_value_loss)."""
    return min(phi * pv_share(design), 1.0)


def dwelling_value_loss(phi, s_d, design="immediate"):
    """Fall in a dwelling's value at announcement as a share of its value: phi x pv_share x s_d, the land loss, which
    when phi > 1 also counts the present value of the charge beyond the land's whole rent (T4: tau > 1 is a levy on
    the holder, not on the land); capped at the dwelling's whole value."""
    return min(phi * pv_share(design) * s_d, 1.0)


def mortgaged_by_decile():
    """Mortgaged owners by decile, 2023 survey: count, mean dwelling value and loans, aggregate LTV. 151u does not
    split main-residence value by tenure inside a decile; the split uses 151z's national mean values (mortgaged
    222,127 vs outright 170,510) and the decile's counts, then is scaled so the national mortgaged total matches
    151z exactly (judgment)."""
    c = owner_counts()
    N = c["n_households"]
    v_m = wv("main_residence", "mean", "tenure")["owner_with_mortgage"]
    v_o = wv("main_residence", "mean", "tenure")["outright_owner"]
    n_m_nat = wv("housing_loans", "households_holding", "tenure")["owner_with_mortgage"]
    k = c["n_mortgaged"] * v_m / (c["n_mortgaged"] * v_m + c["n_outright"] * v_o)
    MR_tot = wv("main_residence").reindex(DEC) * N
    V_m_tot = MR_tot * k
    scale = n_m_nat * v_m / float(V_m_tot.sum())
    V_m_tot = V_m_tot * scale
    HL_tot = wv("housing_loans").reindex(DEC) * N
    out = pd.DataFrame({"n_mortgaged": c["n_mortgaged"], "n_outright": c["n_outright"], "k_mortgaged_value_share": k * scale,
                        "value_mortgaged_meur": V_m_tot / 1e6, "loans_meur": HL_tot / 1e6,
                        "value_outright_meur": (MR_tot - V_m_tot) / 1e6,
                        "mean_value_mortgaged": V_m_tot / c["n_mortgaged"], "mean_loan": HL_tot / c["n_mortgaged"]})
    out["ltv_aggregate"] = out["loans_meur"] / out["value_mortgaged_meur"]
    out.attrs["scale"] = scale
    return out


def crossers_lognormal(A, Vbar, n, f, th, sigma, c=LTV_MEDIAN_RATIO):
    """Mortgaged owners crossing LTV threshold th when dwelling values fall by the fraction f: LTV log-normal with
    median c x A (A the group's aggregate LTV) and dispersion sigma; Vbar the group's mean value for every member.
    Returns (number crossing, their lost equity f x V, their lost borrowing capacity th V0 - M), per group."""
    A, Vbar, n = (np.asarray(v, float) for v in (A, Vbar, n))
    mu = np.log(c * A)
    if f >= 1.0:
        a = -np.inf
    else:
        a = np.log(th * (1.0 - f))
    b = np.log(th)
    P = norm.cdf((b - mu) / sigma) - (0.0 if a == -np.inf else norm.cdf((a - mu) / sigma))
    EL = np.exp(mu + sigma ** 2 / 2.0) * (norm.cdf((b - mu - sigma ** 2) / sigma) -
                                          (0.0 if a == -np.inf else norm.cdf((a - mu - sigma ** 2) / sigma)))
    n_cross = n * P
    lost_equity = n * P * f * Vbar
    lost_capacity = n * Vbar * (th * P - EL)
    return n_cross, lost_equity, lost_capacity


def underwater_lognormal(A, n, f, sigma, c=LTV_MEDIAN_RATIO):
    """Mortgaged owners with LTV above 1 after the value fall f (all of them when f = 1)."""
    A, n = np.asarray(A, float), np.asarray(n, float)
    if f >= 1.0:
        return n
    mu = np.log(c * A)
    return n * (1.0 - norm.cdf((np.log(1.0 - f) - mu) / sigma))


def collateral_fi(f, sigma=LTV_SIGMA["mid"], thresholds=LTV_THRESHOLDS, carry=1.0):
    """Collateral channel by decile for a dwelling-value fall f: mortgaged owners' aggregate LTV before and after,
    owners crossing each threshold (log-normal LTV inside the decile), their lost equity and lost borrowing capacity
    (EUR million, carried to the flow year with `carry`). Returns (decile rows, total rows)."""
    mb = mortgaged_by_decile()
    rows = []
    for th in thresholds:
        nc, le, lc = crossers_lognormal(mb["ltv_aggregate"], mb["mean_value_mortgaged"], mb["n_mortgaged"], f, th, sigma)
        for i, dd in enumerate(DEC):
            rows.append(dict(decile=dd, threshold=th, f=f, sigma=sigma, n_mortgaged=mb["n_mortgaged"].iloc[i],
                             ltv_before=mb["ltv_aggregate"].iloc[i],
                             ltv_after=(mb["ltv_aggregate"].iloc[i] / (1.0 - f)) if f < 1.0 else np.inf,
                             n_cross=nc[i], lost_equity_meur=le[i] / 1e6 * carry, lost_capacity_meur=lc[i] / 1e6 * carry))
    d = pd.DataFrame(rows)
    uw = underwater_lognormal(mb["ltv_aggregate"], mb["n_mortgaged"], f, sigma)
    tot = d.groupby("threshold")[["n_cross", "lost_equity_meur", "lost_capacity_meur"]].sum().reset_index()
    tot["f"], tot["sigma"] = f, sigma
    tot["share_of_mortgaged"] = tot["n_cross"] / float(mb["n_mortgaged"].sum())
    tot["ltv_mortgaged_before"] = float(mb["loans_meur"].sum() / mb["value_mortgaged_meur"].sum())
    tot["ltv_mortgaged_after"] = tot["ltv_mortgaged_before"] / (1.0 - f) if f < 1.0 else np.inf
    owners_value = float(mb["value_mortgaged_meur"].sum() + mb["value_outright_meur"].sum())
    tot["ltv_owners_before"] = float(mb["loans_meur"].sum()) / owners_value
    tot["ltv_owners_after"] = float(mb["loans_meur"].sum()) / (owners_value * (1.0 - f)) if f < 1.0 else np.inf
    tot["underwater_after"] = float(np.sum(uw))
    return d, tot


# %% the VAT side's stock channel (the post's levy, impact version) and price step
def vat_price_step(m, pass_through):
    """VAT surcharge in the consumer price level: tau x aggregate VAT-able share x pass-through (Fig 7's channel 1)."""
    acc = B.fi_vat_accounting(m)
    share = float(acc["Cbar_v"].iloc[0]) / m["budget_bar"]
    return B.TAU * share * pass_through, share


def vat_levy_impact(nw_meur, consumption_meur, levy, lambdas=LAMBDAS, mpw=MPW):
    """The post's levy channel, impact version (as the US unit computes it): dC = -mpw x lambda x levy x net worth,
    per year; % of consumption."""
    rows = []
    for lam in lambdas:
        for k, v in mpw.items():
            dC = -v * lam * levy * nw_meur
            rows.append(dict(lam=lam, mpw=k, mpw_value=v, levy=levy, dC_meur=dC, pct_consumption=100.0 * dC / consumption_meur))
    return pd.DataFrame(rows)


# %% the loop (T5)
def rent_bar(m, shock):
    return float(B.decompose(m, shock).loc["04.1 Actual rents"].sum())


def loop_closed_form(m, R0, phi, ls, h_landlord, key_q, mpc, max_iter=200, tol=1e-12):
    """The dividend's rent bar R0 (euros per share-month) raises land rent by ls x R0; a household-land tax at phi
    takes the household landlords' part (h_landlord) back and pays it out as a flat extra dividend, financed by the
    holders of rental land (key_q: their quintile shares). Each round runs back through the bridge (decile-netted,
    the schedule's MPCs) to the next rent bar; iterate to the fixed point. Returns (extra dividend, leak to landlords,
    q = rent bar per euro of round transfer, rounds)."""
    R, total, leak, rounds = R0, 0.0, 0.0, []
    key = pd.Series(np.asarray(key_q, float), index=m["w"].index)
    for k in range(1, max_iter + 1):
        inc = ls * R
        ddiv = phi * h_landlord * inc
        leak += inc - ddiv
        net = ddiv - ddiv * key.values / m["w"].values
        R_next = rent_bar(m, B.budget_shock(net, mpc, m["budget"]))
        rounds.append(dict(round=k, rent_bar_in=R, land_rent_increment=inc, extra_dividend=ddiv, rent_bar_out=R_next))
        total += ddiv
        if abs(ddiv) < tol:
            break
        R = R_next
    df = pd.DataFrame(rounds)
    q = df["rent_bar_out"].iloc[0] / df["extra_dividend"].iloc[0] if len(df) and df["extra_dividend"].iloc[0] else np.nan
    return total, leak, q, df


# %% US side, read only (the US unit's outputs and the SCF for the method check)
def us_out(name):
    return pd.read_csv(OUT / name)


def us_scf_mortgaged(cpi_25_to_24=4750.0 / 4625.0):
    """SCF 2025 mortgaged owners (HOUSES > 0, MRTHEL > 0), 2024 dollars, by the Fed's income decile (INCPCTLECAT,
    10-12 merged): the US unit's own definitions, re-read here for the collateral method check."""
    s = pd.read_csv(TIDY / "scf2025_summary.csv.gz", usecols=["Y1", "YY1", "WGT", "HOUSES", "MRTHEL", "INCPCTLECAT"])
    for v in ["HOUSES", "MRTHEL"]:
        s[v] = s[v] / cpi_25_to_24
    s["decile"] = np.minimum(s["INCPCTLECAT"].astype(int), 10)
    return s[(s["HOUSES"] > 0) & (s["MRTHEL"] > 0)].copy()


def us_collateral_check(f, th, sigma, c=LTV_MEDIAN_RATIO):
    """The log-normal decile method run on SCF 2025 decile aggregates against the SCF microdata itself (the US unit's
    collateral() logic: crossers of th when HOUSES falls by f). Returns dict of both."""
    s = us_scf_mortgaged()
    w, V0, M = s["WGT"].values, s["HOUSES"].values, s["MRTHEL"].values
    V1 = V0 * (1.0 - f)
    cr = (M / V0 <= th) & (M / V1 > th)
    lc = np.maximum(0.0, th * V0 - M) - np.maximum(0.0, th * V1 - M)
    micro = dict(n_cross_m=float((w * cr).sum()) / 1e6, lost_equity_bn=float((w * cr * f * V0).sum()) / 1e9,
                 lost_capacity_bn=float((w * cr * lc).sum()) / 1e9)
    g = s.groupby("decile").apply(lambda q: pd.Series({"n": q["WGT"].sum(), "Vbar": np.average(q["HOUSES"], weights=q["WGT"]),
                                                       "A": (q["MRTHEL"] * q["WGT"]).sum() / (q["HOUSES"] * q["WGT"]).sum()}),
                                  include_groups=False)
    nc, le, lcap = crossers_lognormal(g["A"], g["Vbar"], g["n"], f, th, sigma, c)
    param = dict(n_cross_m=float(nc.sum()) / 1e6, lost_equity_bn=float(le.sum()) / 1e9, lost_capacity_bn=float(lcap.sum()) / 1e9)
    return micro, param


def us_shape_population(mb=None):
    """Finland's mortgaged owners with the SCF's within-decile shape (judgment, the collateral channel's central
    method): every SCF 2025 mortgaged family in income decile d stands for Finnish mortgaged owners of decile d, its
    LTV scaled by A_FI,d / A_US,d and its home value by Vbar_FI,d / Vbar_US,d, its weight by n_FI,d / n_US,d. The
    Finnish decile aggregates (count, mean value, aggregate LTV, loans) are then reproduced exactly; the shape inside
    the decile (compressed top, long lower tail) is the US one. Returns the scaled population (2023 euros)."""
    mb = mortgaged_by_decile() if mb is None else mb
    s = us_scf_mortgaged()
    s["ltv"] = s["MRTHEL"] / s["HOUSES"]
    g = s.groupby("decile").apply(lambda q: pd.Series({"n": q["WGT"].sum(), "Vbar": np.average(q["HOUSES"], weights=q["WGT"]),
                                                       "A": (q["MRTHEL"] * q["WGT"]).sum() / (q["HOUSES"] * q["WGT"]).sum()}),
                                  include_groups=False)
    key = {i + 1: dd for i, dd in enumerate(DEC)}
    fi = mb.rename(index={v: k for k, v in key.items()})
    s["decile_fi"] = s["decile"].map(key)
    s["ltv_fi"] = s["ltv"] * s["decile"].map(fi["ltv_aggregate"] / g["A"])
    s["V_fi"] = s["HOUSES"] * s["decile"].map(fi["mean_value_mortgaged"] / g["Vbar"])
    s["w_fi"] = s["WGT"] * s["decile"].map(fi["n_mortgaged"] / g["n"])
    s["M_fi"] = s["ltv_fi"] * s["V_fi"]
    return s[["decile", "decile_fi", "w_fi", "V_fi", "M_fi", "ltv_fi"]].reset_index(drop=True)


def collateral_us_shape(f, pop, thresholds=LTV_THRESHOLDS, carry=1.0):
    """Collateral channel on the US-shape population for a dwelling-value fall f: by decile and in total, mortgaged
    owners crossing each threshold, their lost equity and lost borrowing capacity (EUR million, carried with
    `carry`), owners above each threshold before and after, and LTVs."""
    w, V0, M = pop["w_fi"].values, pop["V_fi"].values, pop["M_fi"].values
    V1 = V0 * (1.0 - f)
    l0 = M / V0
    l1 = M / np.where(V1 > 0, V1, 1e-9)
    rows = []
    for th in thresholds:
        cr = (l0 <= th) & (l1 > th)
        lc = np.maximum(0.0, th * V0 - M) - np.maximum(0.0, th * V1 - M)
        for dd in DEC + ["total"]:
            mk = (pop["decile_fi"] == dd).values if dd != "total" else np.ones(len(pop), bool)
            ww = w * mk
            rows.append(dict(decile=dd, threshold=th, f=f, n_mortgaged=float(ww.sum()), n_cross=float((ww * cr).sum()),
                             lost_equity_meur=float((ww * cr * f * V0).sum()) / 1e6 * carry,
                             lost_capacity_meur=float((ww * cr * lc).sum()) / 1e6 * carry,
                             crossers_value_meur=float((ww * cr * V0).sum()) / 1e6 * carry,
                             above_before=float((ww * (l0 > th)).sum()), above_after=float((ww * (l1 > th)).sum()),
                             ltv_before=float((ww * M).sum() / (ww * V0).sum()),
                             ltv_after=float((ww * M).sum() / (ww * V1).sum()) if f < 1.0 else np.inf))
    return pd.DataFrame(rows)


def weighted_quantiles(x, w, qs=(0.25, 0.5, 0.75)):
    x, w = np.asarray(x, float), np.asarray(w, float)
    o = np.argsort(x)
    cw = np.cumsum(w[o]) / w.sum()
    return [float(np.interp(q, cw, x[o])) for q in qs]


def us_wealth_concentration():
    """SCF 2025 shares of the top income decile and quintile (INCPCTLECAT) in financial assets, net worth, home
    value and other residential real estate: the US side of the concentration comparison."""
    s = pd.read_csv(TIDY / "scf2025_summary.csv.gz", usecols=["WGT", "FIN", "NETWORTH", "HOUSES", "ORESRE", "INCOME", "INCPCTLECAT"])
    s["decile"] = np.minimum(s["INCPCTLECAT"].astype(int), 10)
    out = {}
    for v in ["FIN", "NETWORTH", "HOUSES", "ORESRE", "INCOME"]:
        t = (s[v].clip(lower=0) * s["WGT"]).groupby(s["decile"]).sum()
        out[v] = dict(top_decile=float(t.loc[10] / t.sum()), top_quintile=float(t.loc[[9, 10]].sum() / t.sum()),
                      bottom_half=float(t.loc[1:5].sum() / t.sum()))
    return pd.DataFrame(out).T
