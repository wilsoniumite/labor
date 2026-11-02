# lvt_us.py - question 1, US: a land-value tax funding the same flat dividend, run through the rebuilt VAT-bridge
# machinery (consumption/rebuild/code/bridge.py, imported unchanged) beside the VAT bridge itself.
#
# The tax: a credible, permanent tax taking a share phi of land rent, levied on announcement-date (pre-tax) land
# values: bill_i = phi * r * L_i, with r the rent-to-value rate implied by one of the paper's four land-rent
# measures (pinning/code/feasibility_kappa.py). Revenue funds a flat dividend per payment share (adult 1, child 0.3)
# on the CE 2024 population, the VAT bridge's payment rule. Land by household comes from the SCF (2025 main, income
# year 2024; 2022 robustness), calibrated to the Z.1 land residuals. Incidence is by SCF pretax-income decile,
# converted to CE 2024 payment shares exactly as the VAT accounting does, so both instruments land on one population.
#
# Plain functions plus constants (no classes); a "model" is bridge.py's plain dict. Units: dollars; SCF values are
# in 2024 dollars after load_scf(); land and bills per SCF family; everything the bridge sees is dollars per payment
# share per month. Every judgment input is a named constant below, with its band; run_lvt_us.py varies each one.

# %% setup
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent                     # consumption/lvt/code
LVT = HERE.parent                                          # consumption/lvt
THREAD = LVT.parent                                        # consumption
REPO = THREAD.parent
sys.path.insert(0, str(THREAD / "rebuild" / "code"))

import numpy as np
import pandas as pd

import bridge as B

TIDY = B.TIDY
OUT = LVT / "out"
FIG = LVT / "figures"
DEC = [f"d{i:02d}" for i in range(1, 11)]

# %% constants: accounting (identities and published inputs)
YEAR = 2024                       # flow year: CE 2024, SCF 2025 income year, Z.1 2024 land
# SCF macro CPILAG for 2025 (README_fed): the extract's 2025 dollars per 2024 dollar. It restates INCOME (income year
# 2024) exactly; balance-sheet items are interview-date (2025) values, so their "2024 dollars" are a CPI deflation of
# 2025 values, not a 2024 valuation. Ratios (LTVs, HtM flags, decile shares) do not depend on it; the calibrated s does.
CPI_25_TO_24 = 4750.0 / 4625.0
SCF22_CPIADJ = 4789.0 / 4376.0    # the 2022 extract's 2022 -> 2025 dollar factor (README_fed item 5); for reference
PHI_FULL = 0.98                   # full capture (design memo 1.1: the 2% is an assessment-error buffer)
GAMMA, DELTA = 0.02, 0.05         # T4's dial: rent growth / discount, the parameters of the repo's price-path table below
LEVY_AK = 0.08                    # the post's Auerbach-Kotlikoff levy: "every unit of wealth ... buys about 8% less"
LAMBDAS = (0.0, 0.35, 1.0)        # the post's levy-perception scenarios (flow only, central, full A-K)
GS10_FILE = REPO / "pinning" / "cache" / "GS10.csv"        # the paper's vendored FRED copy (monthly, %)
# T11 / memo 7.1 price paths at phi = 0.98 (three-taxes/code/fiscal_napkin.py: gamma 2%, delta 5%, discrete annual timing).
# One convention for every design: the phase-ins AND increment-only grandfathering are read from this table (0.404 at
# phi = 0.98); the continuous approximation phi * gamma / delta (0.392) is not used.
SHOCK_FILE = REPO / "three-taxes" / "data" / "lvt_shock.csv"
SHOCK_INCREMENT = "increment-only (grandfather r0)"

# %% constants: judgment inputs (each is varied in run_lvt_us.py; bands in the comments)
# Wealth-effect propensity per dollar of wealth per year: the post's fn 31 range 2-5 cents; central = midpoint.
MPW = {"low": 0.02, "mid": 0.035, "high": 0.05}
# Housing-collateral consumption response per dollar per year, applied to owners whose LTV crosses a borrowing
# threshold. The literature (published abstracts): low 4.7c, Aladangady (2017 AER): "$1 increase in home values leads
# to a $0.047 increase in spending for homeowners", driven by credit-constrained households; mid 6c and lit_high 7c,
# Mian, Rao and Sufi (2013 QJE): average MPC out of housing wealth "5-7 cents" (midpoint, top), higher where
# households are poorer and more levered. stress 10c: the unit's own stress value for levered owners losing access to
# equity (judgment; no source gives a number for the levered tail). Those estimates come from house-price changes
# that carry no tax bill. Under an LVT an owner-occupier's capitalized land loss IS the present value of the bill
# (T4), and the flow already charges the bill at the owner's MPC, so the clean collateral concept is the crossers'
# lost borrowing capacity (a credit effect on top of the bill); applied to their lost equity the same cents count the
# bill twice ("includes the T4 overlap"), a band edge only. Berger, Guerrieri, Lorenzoni and Vavra (2018) supply the
# mechanism: the response to a permanent house-price shock is about the MPC out of transitory income times the
# housing value, so it concentrates on constrained, levered owners; whether all crossers respond or only the
# hand-to-mouth ones (KVW) is a judgment call, reported both ways.
MPC_COLL = {"low": 0.047, "mid": 0.06, "lit_high": 0.07, "stress": 0.10}
LTV_THRESHOLDS = (0.80, 0.90, 1.00)   # cash-out refinance limit (80%), high-LTV lending (90%), negative equity (100%)
# KVW (2014) hand-to-mouth: liquid wealth at or below half of per-pay-period income. biweekly pay = annual/52 (KVW's
# pay period, main); monthly = annual/24 (the Fed's 2026 FEDS note on the SCF windfall question).
HTM_DIVISOR = {"biweekly": 52.0, "monthly": 24.0}
# Land share of residential property value: uniform s calibrated to Z.1 (main); band 0.30-0.60 at a fixed aggregate
# property value; "rising" variant: s = 0.30 + 0.30 * F(V), F the weighted CDF of owners' home values, rescaled to
# the Z.1 aggregate (judgment: expensive homes are expensive mostly for their location).
S_BAND = (0.30, 0.60)
S_RISING = (0.30, 0.30)          # intercept, slope on the home-value percentile rank
# Land share of a change in rent (the loop): central 0.40 (between the paper's flow measures and the calibrated s),
# band 0.30-0.50 (the paper's 30% / 50% land shares of housing services).
LS_RENT = {"low": 0.30, "mid": 0.40, "high": 0.50}
# Nonfinancial-corporate land after 2020 (the Fed stopped publishing NFC current-cost structures): main = the NFC
# land share of NFC real estate held at its 2016-2020 mean (paper's conventions); low = NFC structures grown at the
# noncorporate structures' current-cost growth 2020-24 (the residual method with a proxy deflator); high = the 2020
# share. All three are labelled assumptions; BEA Fixed Assets Table 4.1/6.1 (corporate structures, current cost)
# would replace them and is not vendored.
NFC_RULES = ("share_2016_2020", "structures_proxy", "share_2020")
# Housing lines that are structural by tenure (CE Table 1710): renters pay rent, owners pay owner costs.
RENTER_ONLY = ["Rented dwellings"]
OWNER_ONLY = ["Mortgage interest and charges", "Property taxes", "Home maintenance, repairs & insurance"]

SCF_DOLLARS = ["HOUSES", "ORESRE", "NNRESRE", "BUS", "ACTBUS", "NONACTBUS", "FARMBUS", "EQUITY", "DEQ", "RETEQ",
               "STOCKS", "NMMF", "BOND", "LIQ", "CCBAL", "RETQLIQ", "CASHLI", "CDS", "SAVBND", "OTHMA", "HOMEEQ",
               "MRTHEL", "HELOC", "NH_MORT", "RESDBT", "NETWORTH", "ASSET", "DEBT", "INCOME", "NORMINC", "WAGEINC",
               "SSRETINC", "TOTSPENDNH", "VEHIC", "FIN", "NFIN", "RENT", "KGHOUSE"]


# %% loading: SCF
def load_scf(year=2025):
    """SCF summary extract (all five implicates pooled, weight WGT), dollar variables restated in 2024 dollars
    (both extracts are published in 2025 dollars; README_fed items 5 and 7; for balance sheets this is a CPI deflation
    of interview-date values, see CPI_25_TO_24), income decile from the Fed's own pooled
    weighted percentile groups of INCOME (INCPCTLECAT 1-9, and 10-12 merged), IMPLICATE recomputed from Y1."""
    s = pd.read_csv(TIDY / f"scf{year}_summary.csv.gz")
    s["IMPLICATE"] = s["Y1"] - 10 * s["YY1"]
    for v in SCF_DOLLARS:
        if v in s.columns:
            s[v] = s[v].astype(float) / CPI_25_TO_24
    decile = np.minimum(s["INCPCTLECAT"].astype(int), 10)
    extra = pd.DataFrame({"decile": decile, "dec": decile.map(lambda d: f"d{d:02d}"),
                          "owner": (s["HOUSES"] > 0).astype(int), "age65": (s["AGE"] >= 65).astype(int),
                          "year": year}, index=s.index)
    return pd.concat([s, extra], axis=1)


def weighted_decile(x, w, n=10):
    """Weighted quantile group (1..n) of x, ties kept together by a stable sort; used to verify INCPCTLECAT."""
    x, w = np.asarray(x, float), np.asarray(w, float)
    o = np.argsort(x, kind="stable")
    cw = np.cumsum(w[o]) / w.sum()
    g = np.empty(len(x), int)
    g[o] = np.minimum(np.floor(cw * n - 1e-12).astype(int) + 1, n)
    return g


def scf2022_units():
    """SCF 2022 adults and minors in the primary economic unit, from the full public data (scf2022_xvars), merged on
    Y1. Early builds of the tidy file had IMPLICATE wrong for YY1 >= 3277 (a 16-bit overflow, fixed and regenerated on
    2026-11-02); the merge key stays Y1 and IMPLICATE is recomputed as Y1 - 10*YY1, which is right either way."""
    x = pd.read_csv(TIDY / "scf2022_xvars.csv.gz")
    x["IMPLICATE"] = x["Y1"] - 10 * x["YY1"]
    return x[["Y1", "N_ADULTS_PEU", "N_MINORS_PEU", "X42001", "X414"]]


def kids_bucket(k):
    return np.minimum(np.asarray(k, int), 3)


def adult_cells(s22):
    """Calibration of the 2025 adult and minor counts on the 2022 roster: weighted means of (adults beyond the
    reference person and partner) and (minors in the PEU) by AGECL x MARRIED x min(KIDS, 3), with AGECL x MARRIED
    as the fallback for cells under 40 records. MARRIED and KIDS exist in both years; the roster only in 2022."""
    d = s22.assign(oth=s22["N_ADULTS_PEU"] - 1 - (s22["MARRIED"] == 1), kb=kids_bucket(s22["KIDS"]))
    fine = d.groupby(["AGECL", "MARRIED", "kb"]).apply(
        lambda q: pd.Series({"oth": np.average(q["oth"], weights=q["WGT"]), "minors": np.average(q["N_MINORS_PEU"], weights=q["WGT"]),
                             "n": len(q)}), include_groups=False)
    coarse = d.groupby(["AGECL", "MARRIED"]).apply(
        lambda q: pd.Series({"oth": np.average(q["oth"], weights=q["WGT"]), "minors": np.average(q["N_MINORS_PEU"], weights=q["WGT"]),
                             "n": len(q)}), include_groups=False)
    return fine, coarse


def predict_units(s, fine, coarse, min_n=40):
    """Adults = 1 + partner + predicted other PEU adults; minors = predicted PEU minors (cell means from adult_cells)."""
    key = list(zip(s["AGECL"], s["MARRIED"], kids_bucket(s["KIDS"])))
    oth, mn = np.empty(len(s)), np.empty(len(s))
    for j, (a, mr, kb) in enumerate(key):
        if (a, mr, kb) in fine.index and fine.loc[(a, mr, kb), "n"] >= min_n:
            r = fine.loc[(a, mr, kb)]
        else:
            r = coarse.loc[(a, mr)]
        oth[j], mn[j] = r["oth"], r["minors"]
    adults = 1.0 + (s["MARRIED"].values == 1) + oth
    return adults, mn


def add_payment_units(s, year, cells=None):
    """Raw SCF payment shares per family: adults + 0.3 x minors (2022: roster counts; 2025: MARRIED/KIDS with the
    2022 roster calibration)."""
    s = s.copy()
    if year == 2022:
        u = scf2022_units()
        s = s.merge(u, on="Y1", how="left", validate="one_to_one")
        assert s["N_ADULTS_PEU"].notna().all()
        s["adults"] = s["N_ADULTS_PEU"].astype(float)
        s["minors"] = s["N_MINORS_PEU"].astype(float)
    else:
        fine, coarse = cells
        s["adults"], s["minors"] = predict_units(s, fine, coarse)
    s["shares_raw"] = B.ADULT_W * s["adults"] + B.CHILD_W * s["minors"]
    return s


def calibrate_units_to_ce(m, s):
    """Scale SCF payment shares within each income decile so the decile's total equals CE 2024's (N_d x shares_d):
    c_d = N_d^CE * shares_d^CE / sum_{i in d} w_i shares_i. CE consumer units include related adults outside the
    SCF family (README_fed: 23.7 million listed adults outside PEUs in 2022) and the CE count is 0.6% larger. With
    this scaling, household-level aggregates reproduce the decile-netted VAT/LVT accounting exactly."""
    u = m["units"]
    ce_tot = u["N_thousand"] * 1000.0 * u["shares"]
    scf_tot = s.groupby("dec").apply(lambda d: (d["WGT"] * d["shares_raw"]).sum(), include_groups=False)
    c = (ce_tot / scf_tot.reindex(u.index)).rename("c_d")
    s = s.copy()
    s["c_d"] = s["dec"].map(c)
    s["shares"] = s["shares_raw"] * s["c_d"]
    return s, c


# %% loading: Z.1 land, yields, PCE housing
def z1_value(z, sid, freq, year):
    r = z[(z["series_id"] == sid) & (z["freq"] == freq) & (z["date"] == str(year))]
    if r.empty:
        return np.nan
    return float(r["value"].iloc[0])


def z1_targets(year=YEAR, nfc_rule="share_2016_2020"):
    """Z.1 land residuals in $bn (2026:Q2 vintage, the paper's construction): household land (LAND_HH_PAPER),
    noncorporate business land (paper's conventions), and nonfinancial-corporate land under a labelled assumption
    (published only to 2020). Also the aggregates used for ratios and LTVs."""
    z = pd.read_csv(TIDY / "z1_land.csv", dtype={"date": str})
    t = dict(year=year,
             L_hh=z1_value(z, "LAND_HH_PAPER", "A_paper", year),
             L_nnb=z1_value(z, "LAND_NNB_PAPERCONV", "A_paper", year),
             re_hh=z1_value(z, "LM155035005", "A_mean", year),
             str_hh=z1_value(z, "LM155012665", "A_mean", year),
             re_ownocc=z1_value(z, "LM155035015", "A_mean", year),
             mortg=z1_value(z, "LA153165105", "A_mean", year),
             re_nfc=z1_value(z, "LM105035005", "A_eop", year),
             re_nnb=z1_value(z, "LM115035005", "A_eop", year))
    t["L_hh_ownocc"] = t["re_ownocc"] - t["str_hh"]          # households-only owner-occupied land (concept variant)
    t["land_share_re"] = t["L_hh"] / t["re_hh"]
    # NFC land, paper's conventions, 2016-2020
    hist = {y: (z1_value(z, "LAND_NFC_PAPERCONV", "A_paper", y), z1_value(z, "LM105035005", "A_eop", y)) for y in range(2010, 2021)}
    ratio = {y: a / b for y, (a, b) in hist.items()}
    t["nfc_share_2016_2020"] = float(np.mean([ratio[y] for y in range(2016, 2021)]))
    t["nfc_share_2020"] = ratio[2020]
    t["nfc_land_2020"] = hist[2020][0]
    s20 = z1_value(z, "LM105012665", "A_mean", 2020) + z1_value(z, "LM105013665", "A_eop", 2020)
    g_nnb = (z1_value(z, "FL115012665", "A_mean", year) + z1_value(z, "FL115013665", "A_eop", year)) / \
            (z1_value(z, "FL115012665", "A_mean", 2020) + z1_value(z, "FL115013665", "A_eop", 2020))
    t["nfc_structures_proxy"] = s20 * g_nnb
    t["nnb_structures_growth_2020"] = g_nnb
    opts = {"share_2016_2020": t["nfc_share_2016_2020"] * t["re_nfc"],
            "structures_proxy": t["re_nfc"] - t["nfc_structures_proxy"],
            "share_2020": t["nfc_share_2020"] * t["re_nfc"]}
    t.update({f"L_nfc_{k}": v for k, v in opts.items()})
    t["nfc_rule"] = nfc_rule
    t["L_nfc"] = opts[nfc_rule]
    return t


def gs10_annual(year):
    """Annual mean of the monthly 10-year Treasury yield (GS10), the paper's annualize() of its vendored FRED copy."""
    g = pd.read_csv(GS10_FILE, parse_dates=["observation_date"])
    g = g[g["observation_date"].dt.year == year]
    assert len(g) == 12, (year, len(g))
    return float(g["GS10"].mean())


def pce_housing(year):
    """PCE housing services (Table 2.4.5U line 153, DHSGRC), $bn, October 2026 vintage."""
    d = pd.read_csv(TIDY / "bea_pce_u_long.csv.gz", low_memory=False,
                    usecols=["table", "freq", "line", "series_code", "date", "value"])
    r = d[(d["table"] == "2.4.5U") & (d["freq"] == "A") & (d["series_code"] == "DHSGRC") & (d["date"].astype(str) == str(year))]
    return float(r["value"].iloc[0]) / 1000.0


def pce_total(year):
    d = pd.read_csv(TIDY / "bea_pce_u_long.csv.gz", low_memory=False,
                    usecols=["table", "freq", "line", "series_code", "date", "value"])
    r = d[(d["table"] == "2.4.5U") & (d["freq"] == "A") & (d["series_code"] == "DPCERC") & (d["date"].astype(str) == str(year))]
    return float(r["value"].iloc[0]) / 1000.0


def rent_measures(z1, year=YEAR):
    """The paper's four land-rent measures (feasibility_kappa.py GRID_RENT, household scope): rT in $bn/yr and the
    rent-to-value rate r = rT / household land residual that each implies."""
    g10 = gs10_annual(year)
    ph = pce_housing(year)
    L = z1["L_hh"]
    rows = [dict(measure="m1_z1hh_x_gs10", label="household land x 10y yield", rT=L * g10 / 100.0),
            dict(measure="m2_z1hh_x_gs10p150", label="household land x (10y yield + 1.5)", rT=L * (g10 + 1.5) / 100.0),
            dict(measure="m3_pce_housing_x_0.30", label="30% of PCE housing services", rT=0.30 * ph),
            dict(measure="m4_pce_housing_x_0.50", label="50% of PCE housing services", rT=0.50 * ph)]
    out = pd.DataFrame(rows).set_index("measure")
    out["r"] = out["rT"] / L
    out["gs10"], out["pce_housing"], out["L_hh"] = g10, ph, L
    return out


# %% land by household
def weighted_cdf(values, weights, at):
    """F(at) = weighted share of `values` at or below `at`."""
    v, w = np.asarray(values, float), np.asarray(weights, float)
    o = np.argsort(v)
    cw = np.cumsum(w[o]) / w.sum()
    return np.interp(np.asarray(at, float), v[o], cw, left=0.0, right=1.0)


def land_holdings(s, z1, s_rule="uniform", s_level=None, nnb_key=("NNRESRE", "BUS")):
    """Land held by each SCF family, dollars (2024):
    L_own = s x HOUSES (primary residence), L_ore = s x ORESRE (other residential real estate) -> base L1;
    L_nnb = Z.1 noncorporate business land x (NNRESRE + BUS) share; L_nfc = Z.1 NFC land x EQUITY share -> L2 adds.
    s_rule 'uniform': s calibrated so sum_i w_i (L_own + L_ore) = Z.1 household land residual (s_level=None), or a
    fixed s (the 0.30-0.60 band, aggregate land then = s x SCF property value); 'rising': s = 0.30 + 0.30 F(V) by the
    property's value rank among owners' homes, rescaled to the Z.1 aggregate. Returns (s with columns, info dict)."""
    s = s.copy()
    w = s["WGT"].values
    P_own, P_ore = s["HOUSES"].clip(lower=0).values, s["ORESRE"].clip(lower=0).values
    prop = float((w * (P_own + P_ore)).sum())
    if s_rule == "uniform":
        sh = z1["L_hh"] * 1e9 / prop if s_level is None else float(s_level)
        s_own, s_ore = np.full(len(s), sh), np.full(len(s), sh)
        k = 1.0
    elif s_rule == "rising":
        own = P_own > 0
        a, b = S_RISING
        raw_own = a + b * weighted_cdf(P_own[own], w[own], P_own)
        raw_ore = a + b * weighted_cdf(P_own[own], w[own], P_ore)
        k = z1["L_hh"] * 1e9 / float((w * (raw_own * P_own + raw_ore * P_ore)).sum())
        s_own, s_ore = k * raw_own, k * raw_ore
        sh = z1["L_hh"] * 1e9 / prop
    else:
        raise ValueError(s_rule)
    s["s_own"], s["s_ore"] = s_own, s_ore
    s["L_own"], s["L_ore"] = s_own * P_own, s_ore * P_ore
    key_nnb = sum(s[c].clip(lower=0) for c in nnb_key).values
    key_nfc = s["EQUITY"].clip(lower=0).values
    s["L_nnb"] = z1["L_nnb"] * 1e9 * key_nnb / float((w * key_nnb).sum())
    s["L_nfc"] = z1["L_nfc"] * 1e9 * key_nfc / float((w * key_nfc).sum())
    s["L1"] = s["L_own"] + s["L_ore"]
    s["L2"] = s["L1"] + s["L_nnb"] + s["L_nfc"]
    info = dict(s_rule=s_rule, s_uniform=sh, s_rising_scale=k, scf_property_total_bn=prop / 1e9,
                L1_total_bn=float((w * s["L1"]).sum()) / 1e9, L2_total_bn=float((w * s["L2"]).sum()) / 1e9,
                L_nnb_total_bn=float((w * s["L_nnb"]).sum()) / 1e9, L_nfc_total_bn=float((w * s["L_nfc"]).sum()) / 1e9)
    return s, info


BASE_COLS = {"L1": ["L_own", "L_ore"], "L2": ["L_own", "L_ore", "L_nnb", "L_nfc"]}
NONOCC_COLS = {"L1": ["L_ore"], "L2": ["L_ore", "L_nnb", "L_nfc"]}


# %% hand-to-mouth (Kaplan-Violante-Weidner 2014)
def htm_flags(s, band="biweekly"):
    """liquid = LIQ + STOCKS + BOND + NMMF - CCBAL; HtM if liquid <= INCOME / divisor (half a pay period's income);
    wealthy HtM if also illiquid > 0, illiquid = HOMEEQ + (ORESRE - RESDBT) + NNRESRE + RETQLIQ + CASHLI + CDS +
    SAVBND + OTHMA (README_fed's KVW list; business equity excluded, as KVW do). Without the credit limit (not in the
    2025 extract) a negative liquid position counts as HtM."""
    liquid = s["LIQ"] + s["STOCKS"] + s["BOND"] + s["NMMF"] - s["CCBAL"]
    illiquid = s["HOMEEQ"] + (s["ORESRE"] - s["RESDBT"]) + s["NNRESRE"] + s["RETQLIQ"] + s["CASHLI"] + s["CDS"] + s["SAVBND"] + s["OTHMA"]
    htm = liquid <= s["INCOME"].clip(lower=0) / HTM_DIVISOR[band]
    out = pd.DataFrame({"liquid": liquid, "illiquid": illiquid, "htm": htm.astype(int),
                        "whtm": (htm & (illiquid > 0)).astype(int), "phtm": (htm & (illiquid <= 0)).astype(int)}, index=s.index)
    return out


# %% accounting
def decile_sum(s, x):
    """sum_{i in d} w_i x_i by decile (index d01..d10)."""
    t = pd.Series(np.asarray(x, float) * s["WGT"].values, index=s.index).groupby(s["dec"]).sum()
    return t.reindex(DEC)


def scf_to_per_share_monthly(m, s, x_annual):
    """Annual dollars per SCF family -> the bridge's unit, dollars per CE payment share per month, by decile: the
    decile's SCF total spread over its CE consumer units (per CU), then bridge.per_share_monthly."""
    per_cu = decile_sum(s, x_annual) / (m["units"]["N_thousand"] * 1000.0)
    return B.per_share_monthly(m, per_cu)


def total_shares(m):
    u = m["units"]
    return float((u["N_thousand"] * 1000.0 * u["shares"]).sum())


def lvt_accounting(m, s, base, phi, r):
    """Decile-netted accounting (the post's method) through bridge.net_from_base: the per-share land-rent base
    r * L_d, taxed at phi, funds the flat dividend; net_d = dividend - phi r L_d. Returns the bridge's frame plus
    revenue ($bn/yr) and the dividend."""
    L = s[BASE_COLS[base]].sum(axis=1).values
    rent_ps = scf_to_per_share_monthly(m, s, r * L)            # land rent per share per month, by decile
    acc = B.net_from_base(rent_ps, m["w"], phi, m["budget"])
    acc = acc.rename(columns={"base": "land_rent", "tax": "bill", "base_pct_budget": "land_rent_pct_budget"})
    acc["revenue_bn"] = phi * r * float((s["WGT"] * L).sum()) / 1e9
    acc["land_share"] = decile_sum(s, L) / float((s["WGT"] * L).sum())
    return acc


def lvt_household(s, base, phi, r, dividend, defer=None):
    """Household-level monthly cash flows per family: dividend x calibrated shares, the bill on each land component,
    the deferred part (owner-occupied land of the eligible), the cash net, and the net per payment share."""
    h = pd.DataFrame(index=s.index)
    h["div"] = dividend * s["shares"]
    for c in BASE_COLS[base]:
        h[f"bill_{c}"] = phi * r * s[c] / 12.0
    h["bill"] = h[[f"bill_{c}" for c in BASE_COLS[base]]].sum(axis=1)
    h["bill_nonocc"] = h[[f"bill_{c}" for c in NONOCC_COLS[base]]].sum(axis=1)
    h["deferred"] = 0.0 if defer is None else h["bill_L_own"] * np.asarray(defer, float)
    h["net"] = h["div"] - h["bill"]
    h["cash_net"] = h["net"] + h["deferred"]
    h["net_ps"] = h["net"] / s["shares"]
    return h


def vat_household(m, s, acc_vat):
    """The VAT bill by SCF family: each decile's VAT total (tax per share x the decile's CE payment shares, monthly)
    shared out within the decile in proportion to TOTSPENDNH (2025 SCF non-housing spending; judgment: a uniform
    VAT-able share of non-housing spending within a decile). Decile aggregates reproduce the rebuild exactly."""
    u = m["units"]
    T_d = acc_vat["tax"] * u["N_thousand"] * 1000.0 * u["shares"]          # $ per month, decile total
    sp = s["TOTSPENDNH"].clip(lower=0)
    den = decile_sum(s, sp)
    h = pd.DataFrame(index=s.index)
    h["div"] = float(acc_vat["dividend"].iloc[0]) * s["shares"]
    h["bill"] = s["dec"].map(T_d / den).values * sp.values
    h["net"] = h["div"] - h["bill"]
    h["cash_net"] = h["net"]
    h["deferred"] = 0.0
    h["bill_nonocc"] = 0.0
    h["net_ps"] = h["net"] / s["shares"]
    return h


def household_to_decile(m, s, x_month):
    """Monthly dollars per family -> dollars per CE payment share per month by decile (exact: the calibrated shares
    sum to the CE decile's shares)."""
    u = m["units"]
    return decile_sum(s, x_month) / (u["N_thousand"] * 1000.0 * u["shares"])


# %% MPCs
def post_schedules():
    """The rebuilt schedules by decile: mid / low / high (bridge constants) and the monotone per-decile diagnostic
    fitted to Fig 5 bars + Fig 6 segments (consumption/rebuild/out/us_mpc_schedules.csv; not adopted there)."""
    sc = B.mpc_schedules()
    out = pd.DataFrame({k: sc[k].values for k in ["mid", "low", "high"]}, index=DEC)
    diag = pd.read_csv(B.REBUILD / "out" / "us_mpc_schedules.csv").set_index("decile")
    out["mono"] = diag.loc[DEC, "mpc_mid_monotone_fig5_fig6_diagnostic"].values
    return out


def measured_mpc(s, htm, min_n=30):
    """SCF 2025 windfall question (MPSPEND: percent of a one-month-income windfall spent over 12 months), weighted
    means by income decile, and by decile x HtM status (cells under min_n records fall back to the decile mean)."""
    d = s.assign(mp=s["MPSPEND"] / 100.0, htm=htm["htm"].values)
    by_d = d.groupby("dec").apply(lambda q: np.average(q["mp"], weights=q["WGT"]), include_groups=False).reindex(DEC)
    rows = []
    for dec in DEC:
        for hv in (0, 1):
            q = d[(d["dec"] == dec) & (d["htm"] == hv)]
            val = np.average(q["mp"], weights=q["WGT"]) if len(q) >= min_n else by_d[dec]
            rows.append(dict(dec=dec, htm=hv, mpc=val, n=len(q), fallback=len(q) < min_n,
                             pop_share=float(q["WGT"].sum() / d.loc[d["dec"] == dec, "WGT"].sum())))
    return by_d, pd.DataFrame(rows)


def household_mpc(rule, s, cash_net, htm, sched, meas_dh=None):
    """MPC per family under a grade:
    'liq_<sch>'     recipients: the post's <sch> schedule by decile; payers: 1.0 if hand-to-mouth, else <sch>_d
    'liqsym_<sch>'  1.0 for every HtM family (recipient or payer), else <sch>_d
    '<sch>'         <sch>_d for everyone (household-level twin of the decile-netted grade)
    'meas_htm'      the measured windfall MPC of the family's decile x HtM cell
    sch in {mid, low, high, mono}."""
    dd = s["dec"].values
    hm = htm["htm"].values.astype(bool)
    if rule == "meas_htm":
        t = meas_dh.set_index(["dec", "htm"])["mpc"]
        return np.array([t[(d_, int(h_))] for d_, h_ in zip(dd, hm)])
    kind, _, sch = rule.partition("_") if rule.startswith(("liq_", "liqsym_")) else ("plain", "", rule)
    base = sched[sch].reindex(dd).values
    if kind == "liq":
        return np.where((np.asarray(cash_net) < 0) & hm, 1.0, base)
    if kind == "liqsym":
        return np.where(hm, 1.0, base)
    return base


def shock_from_household(m, s, dC_month):
    """dC_d / C_d by decile from household-level monthly consumption changes."""
    per_share = household_to_decile(m, s, dC_month)
    return (per_share / m["budget"]).rename("shock")


# %% stock channel
def loss_fraction(phi, design="immediate", shock_table=None):
    """Share of announcement-date land value lost at announcement. 'immediate': credible permanent capture at phi
    (T4). 'phasein_<T>y' (a T-year phase-in) and 'increment' (increment-only grandfathering: only rent above the
    announcement-date level is taxed): the price drop in the repo's table (lvt_shock.csv, at phi = 0.98), scaled by
    phi/0.98 (the PV is linear in phi). One convention for every design; the continuous approximation of the
    increment-only drop, phi x gamma/delta, would give 0.339 instead of 0.349 at the bridge rate."""
    if design == "immediate":
        return phi
    t = pd.read_csv(SHOCK_FILE) if shock_table is None else shock_table
    if design == "increment":
        row = t[t["design"] == SHOCK_INCREMENT]
    elif design.startswith("phasein_"):
        row = t[t["design"] == f"phase-in {design.split('_')[1]}"]
    else:
        raise ValueError(design)
    assert len(row) == 1, design
    return float(row["price_drop"].iloc[0]) * phi / PHI_FULL


def collateral(s, loss_frac, thresholds=LTV_THRESHOLDS, groups=None):
    """LTVs of mortgaged owners (primary-residence debt incl. HELOCs, MRTHEL, over HOUSES) before and after the land
    price falls by loss_frac of the home's land value, and the owners who cross each borrowing threshold. groups =
    {name: boolean array over families}: who responds; each summary row then also gives the crossers, their lost
    equity and their lost borrowing capacity inside each group (e.g. the hand-to-mouth crossers).
    Returns (per-family frame, summary rows, aggregates)."""
    V0 = s["HOUSES"].values
    M = s["MRTHEL"].values
    loss = loss_frac * s["L_own"].values
    V1 = V0 - loss
    mort = (V0 > 0) & (M > 0)
    ltv0 = np.where(mort, M / np.where(V0 > 0, V0, 1), np.nan)
    ltv1 = np.where(mort, M / np.where(V1 > 0, V1, 1e-9), np.nan)
    f = pd.DataFrame({"ltv0": ltv0, "ltv1": ltv1, "loss": loss, "mort": mort.astype(int)}, index=s.index)
    rows = []
    w = s["WGT"].values
    for th in thresholds:
        cross = mort & (ltv0 <= th) & (ltv1 > th)
        lost_cap = np.maximum(0, th * V0 - M) - np.maximum(0, th * V1 - M)
        f[f"cross_{th:.2f}"] = cross.astype(int)
        f[f"lostcap_{th:.2f}"] = np.where(cross, lost_cap, 0.0)
        row = dict(threshold=th, n_cross_m=float((w * cross).sum()) / 1e6,
                   share_of_mortgaged=float((w * cross).sum() / (w * mort).sum()),
                   above_before_m=float((w * (mort & (ltv0 > th))).sum()) / 1e6,
                   above_after_m=float((w * (mort & (ltv1 > th))).sum()) / 1e6,
                   lost_equity_crossers_bn=float((w * np.where(cross, loss, 0)).sum()) / 1e9,
                   lost_capacity_crossers_bn=float((w * np.where(cross, lost_cap, 0)).sum()) / 1e9)
        for g, mk in (groups or {}).items():
            cg = cross & np.asarray(mk, bool)
            row[f"n_cross_{g}_m"] = float((w * cg).sum()) / 1e6
            row[f"lost_equity_crossers_{g}_bn"] = float((w * np.where(cg, loss, 0)).sum()) / 1e9
            row[f"lost_capacity_crossers_{g}_bn"] = float((w * np.where(cg, lost_cap, 0)).sum()) / 1e9
        rows.append(row)
    agg = dict(ltv_aggregate_before=float((w * M).sum() / (w * V0).sum()),
               ltv_aggregate_after=float((w * M).sum() / (w * np.maximum(V1, 0)).sum()),
               ltv_mortgaged_before=float((w * M * mort).sum() / (w * V0 * mort).sum()),
               ltv_mortgaged_after=float((w * M * mort).sum() / (w * V1 * mort).sum()),
               median_ltv_before=float(np.nanmedian(ltv0[mort])), n_mortgaged_m=float((w * mort).sum()) / 1e6,
               underwater_after_m=float((w * (mort & (ltv1 > 1))).sum()) / 1e6)
    return f, pd.DataFrame(rows), agg


def crossers_bill_flow(s, h, cross, mpc_i):
    """The T4 overlap in dollars: the crossers' own-home LVT bills at the full rate ($bn/yr) and the response to those
    bills that the flow impulse already contains (mpc_i x bill, $bn/yr). Under the immediate design their lost equity
    is exactly these bills capitalized (bill / r); under a phase-in or increment-only design it is less."""
    w = s["WGT"].values
    b = h["bill_L_own"].values * np.asarray(cross, bool) * 12.0
    return float((w * b).sum()) / 1e9, float((w * np.asarray(mpc_i, float) * b).sum()) / 1e9


def vat_levy_impact(m, s, lambdas=LAMBDAS, mpw=MPW, levy=LEVY_AK):
    """The post's levy channel, impact version on the SCF 2025 balance sheets: dC = -mpw x lambda x levy x net worth
    (per year), aggregated and by decile, in $bn and % of CE consumption (and of PCE)."""
    C_tot = m["budget_bar"] * total_shares(m) * 12.0
    rows = []
    NW = s["NETWORTH"].values
    for lam in lambdas:
        for k, v in mpw.items():
            dC = -v * lam * levy * NW
            tot = float((s["WGT"] * dC).sum())
            rows.append(dict(lam=lam, mpw=k, mpw_value=v, dC_bn=tot / 1e9, pct_ce_consumption=100 * tot / C_tot))
    return pd.DataFrame(rows)


# %% the loop (T5)
def rent_bar(m, shock):
    """The 'Rented dwellings' bar ($ per share per month) for a budget-shock vector."""
    return float(B.decompose(m, shock).loc["Rented dwellings"].sum())


def loop_fixed_point(m, shock0, phi, ls, key_share, mpc, tol=1e-12, max_iter=200):
    """Under the LVT the round-0 rent bar raises land rent by ls x bar; at phi that increment is taxed back and paid
    out as a flat extra dividend, financed by the holders of rental land (key_share: decile shares of that land).
    Each round is a balanced-budget transfer run through the bridge with the decile MPC schedule; iterate to the fixed
    point. Returns (total extra dividend $/share/month, rounds frame, ratio q = rent bar per $ of round transfer)."""
    R = rent_bar(m, shock0)
    rounds, total = [], 0.0
    for k in range(1, max_iter + 1):
        ddiv = phi * ls * R
        net = ddiv - ddiv * key_share.reindex(DEC).values / m["w"].values
        shock = B.budget_shock(net, mpc, m["budget"])
        R_next = rent_bar(m, shock)
        rounds.append(dict(round=k, extra_dividend=ddiv, rent_bar_in=R, rent_bar_out=R_next))
        total += ddiv
        if abs(ddiv) < tol:
            break
        R = R_next
    df = pd.DataFrame(rounds)
    q = df["rent_bar_out"].iloc[0] / df["extra_dividend"].iloc[0] if len(df) and df["extra_dividend"].iloc[0] != 0 else np.nan
    return total, df, q


# %% tenure-aware baskets (an extension: the structural housing lines split by tenure inside each decile)
def tenure_ratios(year=YEAR):
    """CE Table 1710: owners' rented-dwelling spending relative to renters', and renters' owner-cost spending relative
    to owners', per CU (both near zero; the split is structural)."""
    t = pd.read_csv(TIDY / "ce_housing_tenure_long.csv", low_memory=False)
    x = t[(t["year"] == year) & (t["stat"] == "mean")].pivot_table(index="path", columns="group", values="value", aggfunc="first")
    E = B.EXP + " > Housing > Shelter > "
    rr = x.loc[E + "Rented dwellings", "owner"] / x.loc[E + "Rented dwellings", "renter"]
    ro = x.loc[E + "Owned dwellings", "renter"] / x.loc[E + "Owned dwellings", "owner"]
    return float(rr), float(ro)


def tenure_model(m, p_owner, ratios=None):
    """Owner and renter baskets per share inside each decile: renter-only lines (rent) sit with renters, owner-only
    lines (mortgage interest, property taxes, home maintenance/insurance) with owners, every other line at the decile
    mean; the split keeps p_o C^o + p_r C^r = C. Elasticities re-evaluated at each tenure basket with the bridge's own
    eta_table (Working model at the basket's shares). Returns {'owner': (C, eta), 'renter': (C, eta)}."""
    rr, ro = tenure_ratios() if ratios is None else ratios
    C = m["C"]
    po = pd.Series(np.asarray(p_owner, float), index=C.columns)
    pr = 1.0 - po
    Co, Cr = C.copy(), C.copy()
    for g in RENTER_ONLY:
        Cr.loc[g] = C.loc[g] / (pr + po * rr)
        Co.loc[g] = rr * Cr.loc[g]
    for g in OWNER_ONLY:
        Co.loc[g] = C.loc[g] / (po + pr * ro)
        Cr.loc[g] = ro * Co.loc[g]
    out = {}
    for name, Ct in [("owner", Co), ("renter", Cr)]:
        mt = dict(m, C=Ct, budget=Ct.sum())
        eta_t, _ = B.eta_table(mt, m["food_map"])
        out[name] = (Ct, eta_t)
    return out


def shifts_tenure_aware(m, s, dC_month, tm):
    """Category shifts ($ per share per month, population mean) with each family's consumption change spread over its
    tenure's basket in its decile: c_dg = sum_t dC_{d,t} eta^t_gd C^t_gd / C^t_d / S_CE."""
    S = total_shares(m)
    out = pd.Series(0.0, index=m["C"].index)
    own = s["owner"].values.astype(bool)
    for name, mask in [("owner", own), ("renter", ~own)]:
        Ct, eta_t = tm[name]
        tot_d = decile_sum(s[mask], np.asarray(dC_month)[mask]).fillna(0.0)          # $ per month by decile
        share = Ct.div(Ct.sum(), axis=1) * eta_t
        out = out + (share * tot_d.reindex(Ct.columns).values).sum(axis=1) / S
    return out


# %% who pays
def who_pays(s, h, htm, label):
    """By decile: share of families that are net payers; composition of payers (owners, renters, 65+, wealthy and
    poor HtM); share of the decile's net payments made by each group; percentiles of net per payment share."""
    rows = []
    net = h["net"].values
    nps = h["net_ps"].values
    for dec in DEC + ["all"]:
        mk = (s["dec"] == dec).values if dec != "all" else np.ones(len(s), bool)
        w = s["WGT"].values[mk]
        pay = net[mk] < 0
        payw = w * pay
        paid = -np.minimum(net[mk], 0) * w
        r = dict(scenario=label, dec=dec, payer_share=float(payw.sum() / w.sum()))
        for g, flag in [("owner", s["owner"].values[mk] == 1), ("renter", s["owner"].values[mk] == 0),
                        ("age65", s["age65"].values[mk] == 1), ("owner65", (s["owner"].values[mk] == 1) & (s["age65"].values[mk] == 1)),
                        ("htm", htm["htm"].values[mk] == 1), ("whtm", htm["whtm"].values[mk] == 1), ("phtm", htm["phtm"].values[mk] == 1)]:
            r[f"payers_{g}_share"] = float((payw * flag).sum() / payw.sum()) if payw.sum() > 0 else np.nan
            r[f"payments_{g}_share"] = float((paid * flag).sum() / paid.sum()) if paid.sum() > 0 else np.nan
            r[f"payer_rate_{g}"] = float((payw * flag).sum() / (w * flag).sum()) if (w * flag).sum() > 0 else np.nan
        o = np.argsort(nps[mk])
        cw = np.cumsum(w[o]) / w.sum()
        for q in (5, 10, 25, 50, 75, 90, 95):
            r[f"net_ps_p{q}"] = float(np.interp(q / 100.0, cw, nps[mk][o]))
        rows.append(r)
    return pd.DataFrame(rows)
