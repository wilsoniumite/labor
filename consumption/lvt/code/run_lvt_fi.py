# run_lvt_fi.py - question 1, Finland: an LVT-funded flat dividend through the rebuilt VAT-bridge machinery, beside
# the Finnish VAT bridge. Steps 1-5 of the task (land, rates, incidence and liquidity, demand, macro), the comparison
# with the US unit, robustness, then the figures. Every output is a CSV in consumption/lvt/out/ (fi_lvt_*.csv); the
# write-up is consumption/lvt/NOTES_fi.md; consumption/lvt/checks/check_lvt_fi.py re-derives the headline numbers.
#
# Run from the repo root:  venv/bin/python -I consumption/lvt/code/run_lvt_fi.py      (about half a minute)
# Plain functions plus top-level code; each %% block pastes into a notebook cell.

# %% setup
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import warnings

import numpy as np
import pandas as pd
from tqdm.auto import tqdm

import lvt_fi as F

B = F.B
OUT, FIG = F.OUT, F.FIG
OUT.mkdir(exist_ok=True)
FIG.mkdir(exist_ok=True)
DEC, Q = F.DEC, F.Q
CONVS = ["coherent", "post"]          # coherent = the main case (like with like); post = the published VAT side
pd.set_option("display.width", 230)
pd.set_option("display.max_columns", 40)
warnings.filterwarnings("ignore", category=pd.errors.PerformanceWarning)


def wcsv(df, name, index=False):
    df.to_csv(OUT / name, index=index, float_format="%.10g")


REV = []        # the numbers the independent review asked for, collected as they are computed (out/fi_lvt_review.csv)


def rev(item, value, unit, note=""):
    REV.append(dict(item=item, value=float(value), unit=unit, note=note))


# %% step 0: inputs - the rebuilt VAT bridge (both conventions), yields, balance sheet, consumption
M = {c: B.build_fi_model(convention=c) for c in CONVS}
ACC_V = {c: B.fi_vat_accounting(M[c]) for c in CONVS}
ACC_V_LAW = {c: B.fi_vat_accounting(M[c], flags=B.fi_vat_flags("law")) for c in CONVS}
DIV_V = {c: float(ACC_V[c]["dividend"].iloc[0]) for c in CONVS}
DIV_V_LAW = {c: float(ACC_V_LAW[c]["dividend"].iloc[0]) for c in CONVS}
U = M["coherent"]["units"]
HH = U.loc[Q, "households"]
SHARES_TOT = float((HH * U.loc[Q, "shares"]).sum())                 # HBS 2022 payment shares (equal-household design)
C_MEUR = M["coherent"]["budget_bar"] * SHARES_TOT * 12.0 / 1e6      # HBS 2022 consumption, EUR million a year
VAT_REV_MEUR = DIV_V["coherent"] * SHARES_TOT * 12.0 / 1e6
SCHED = B.fi_mpc_schedules()                                         # q1..q5 x low/mid/high (pair means of the US deciles)
MPC_U = {"low": F.MPC_UNCONSTRAINED["low"], "mid": float(SCHED.loc["q5", "mid"]), "high": float(SCHED.loc["q5", "high"])}
YLD = F.fi_yields()
Y22 = F.yield_of(2022, ylds=YLD)
Y22_DEC = F.yield_month("2022-12")                                   # the month the end-2022 land stock is dated
YEARS = (2022, 2023, 2024, 2025)
SH = F.land_shares("residual")
CARRY = F.carry_factor("end2022")
LD = F.land_by_decile(SH, CARRY)
LQ = {b: F.pair_quintiles(LD[b]) for b in ["B1", "B2"]}
N211_22, N211_23 = F.balance_sheet("S14", "N211", 2022), F.balance_sheet("S14", "N211", 2023)
N111_22, N111_23 = F.balance_sheet("S14", "N111", 2022), F.balance_sheet("S14", "N111", 2023)
HS_MEUR = F.housing_services(2022)
NA_C_MEUR = F.na_consumption("0", 2022)
DEFL23 = F.consumption_deflator(2023)
HBS_AGG = float(F.wv("net_wealth", "households_holding")["total"])   # survey households, 2023
print(f"HBS 2022: {SHARES_TOT / 1e6:.3f}m payment shares (coherent), consumption EUR {C_MEUR / 1e3:,.1f}bn "
      f"({100 * C_MEUR / NA_C_MEUR:.1f}% of NA P31DCK {NA_C_MEUR / 1e3:,.1f}bn); VAT dividend coherent EUR {DIV_V['coherent']:.2f} "
      f"(post {DIV_V['post']:.2f}; Finnish law {DIV_V_LAW['coherent']:.2f} / {DIV_V_LAW['post']:.2f}) = EUR {VAT_REV_MEUR / 1e3:,.2f}bn a year")
print(f"10-year yield 2022 {100 * Y22:.3f}% (Eurostat annual; monthly mean {YLD.loc[2022, 'eurostat_monthly_mean']:.4f}, "
      f"ECB {YLD.loc[2022, 'ecb_monthly_mean']:.4f}); 2023 {YLD.loc[2023, 'eurostat_annual']:.2f}, 2024 {YLD.loc[2024, 'eurostat_annual']:.2f}, "
      f"2025 {YLD.loc[2025, 'eurostat_annual']:.2f}")
print(f"land shares (residual): dwellings {SH['s_d']:.4f}, forest/farmland/business {SH['s_f']:.4f}; carry 2023->2022 {CARRY:.4f}; "
      f"household land 2022 EUR {N211_22 / 1e3:,.1f}bn (B1 {float((LD['B1'] * LD['households']).sum()) / 1e9:,.1f}bn)")

inputs = [
    dict(item="vat_dividend_coherent", value=DIV_V["coherent"], unit="EUR/share/month", source="bridge.fi_vat_accounting, convention='coherent'"),
    dict(item="vat_dividend_post", value=DIV_V["post"], unit="EUR/share/month", source="bridge.fi_vat_accounting, convention='post' (the published 193)"),
    dict(item="vat_dividend_law_coherent", value=DIV_V_LAW["coherent"], unit="EUR/share/month", source="Finnish law line by line (bridge.fi_vat_flags('law'))"),
    dict(item="vat_dividend_law_post", value=DIV_V_LAW["post"], unit="EUR/share/month", source="Finnish law line by line; rebuild NOTES_fi: 172.4"),
    dict(item="payment_shares_hbs_coherent", value=SHARES_TOT, unit="shares", source="HBS 2022 households x 12ew pair-mean shares (equal-household design)"),
    dict(item="consumption_hbs_meur", value=C_MEUR, unit="EUR million/yr", source="bridge budget x payment shares x 12 (= HBS 39,808 x 2,919,000)"),
    dict(item="vat_revenue_meur", value=VAT_REV_MEUR, unit="EUR million/yr", source="coherent dividend x payment shares x 12"),
    dict(item="na_consumption_2022_meur", value=NA_C_MEUR, unit="EUR million/yr", source="ntp 15ag P31DCK 2022"),
    dict(item="housing_services_2022_meur", value=HS_MEUR, unit="EUR million/yr", source="ntp 15ag 04.1 + 04.2, 2022"),
    dict(item="consumption_deflator_2023", value=DEFL23, unit="ratio", source="ntp 15ag P31DCK 2023 current / previous-year prices"),
    dict(item="yield_2022", value=100 * Y22, unit="% a year", source="Eurostat irt_lt_mcby_a FI (EMU convergence 10-year), annual 2022"),
    dict(item="yield_2023", value=float(YLD.loc[2023, "eurostat_annual"]), unit="% a year", source="same, 2023"),
    dict(item="yield_2024", value=float(YLD.loc[2024, "eurostat_annual"]), unit="% a year", source="same, 2024"),
    dict(item="yield_2025", value=float(YLD.loc[2025, "eurostat_annual"]), unit="% a year", source="same, 2025"),
    dict(item="yield_2022_12", value=100 * Y22_DEC, unit="% a year", source="Eurostat irt_lt_mcby_m FI, December 2022 (the month of the end-2022 land stock)"),
    dict(item="n211_s14_2022_meur", value=N211_22, unit="EUR million", source="rtp 11zx S14 N211 end-2022"),
    dict(item="n211_s14_2023_meur", value=N211_23, unit="EUR million", source="rtp 11zx S14 N211 end-2023"),
    dict(item="n111_s14_2022_meur", value=N111_22, unit="EUR million", source="rtp 11zx S14 N111 end-2022"),
    dict(item="n111_s14_2023_meur", value=N111_23, unit="EUR million", source="rtp 11zx S14 N111 end-2023"),
    dict(item="survey_dwellings_2023_meur", value=SH["dwellings_meur"], unit="EUR million", source="151u: main residence + other residential + free-time, mean x households"),
    dict(item="survey_ffb_2023_meur", value=SH["ffb_meur"], unit="EUR million", source="151u: forest, farmland and business"),
    dict(item="s_d_residual", value=SH["s_d"], unit="share", source="1 - N111_2023 / survey dwellings (the paper's residual construction)"),
    dict(item="s_f_residual", value=SH["s_f"], unit="share", source="(N211_2023 - s_d x dwellings) / survey forest-farmland-business"),
    dict(item="carry_2023_to_2022", value=CARRY, unit="ratio", source="N211 end-2022 / end-2023 (S14)"),
    dict(item="carry_mid2022_alt", value=F.carry_factor("mid2022"), unit="ratio", source="mean(N211 end-2021, end-2022) / end-2023"),
    dict(item="survey_households_2023", value=HBS_AGG, unit="households", source="151u"),
] + [dict(item=f"judgment_{k}", value=v, unit=u, source=s) for k, v, u, s in [
    ("s_d_band_low", F.S_D_BAND[0], "share", "own vs rented plot price gap within region groups, sales-weighted (0.150; lower bound)"),
    ("s_d_band_high", F.S_D_BAND[1], "share", "N211/(N211+N111) 2022, the flow year (0.259; upper bound; 0.239 in 2023)"),
    ("s_f_band_low", F.S_F_BAND[0], "share", "judgment"), ("s_f_band_high", F.S_F_BAND[1], "share", "judgment"),
    ("mpw_low", F.MPW["low"], "per EUR/yr", "post fn 31"), ("mpw_mid", F.MPW["mid"], "per EUR/yr", "midpoint"),
    ("mpw_high", F.MPW["high"], "per EUR/yr", "post fn 31"), ("mpc_coll_low", F.MPC_COLL["low"], "per EUR/yr", "Aladangady 2017"),
    ("mpc_coll_mid", F.MPC_COLL["mid"], "per EUR/yr", "Mian-Rao-Sufi 2013 midpoint"), ("mpc_coll_lit_high", F.MPC_COLL["lit_high"], "per EUR/yr", "Mian-Rao-Sufi 2013 top"),
    ("mpc_coll_stress", F.MPC_COLL["stress"], "per EUR/yr", "stress, judgment (no source)"),
    ("mpc_unconstrained_low", MPC_U["low"], "MPC", "judgment"), ("mpc_unconstrained_mid", MPC_U["mid"], "MPC", "schedule's q5 (mid)"),
    ("mpc_unconstrained_high", MPC_U["high"], "MPC", "high schedule's q5"), ("sigma_c_mid", F.SIGMA_C["mid"], "log sd", "judgment"),
    ("ltv_sigma_mid", F.LTV_SIGMA["mid"], "log sd", "US-calibrated log-normal (band method)"),
    ("phi_full", F.PHI_FULL, "share", "design memo 1.1"), ("gamma", F.GAMMA, "", "T4"), ("delta", F.DELTA, "", "T4"),
    ("hh_landlord_share_mid", F.HH_LANDLORD_SHARE["mid"], "share", "judgment from the balance sheet")]]
wcsv(pd.DataFrame(inputs), "fi_lvt_inputs.csv")
yl = YLD.copy()
yl["used_as"] = ["main (flow year)" if y == 2022 else ("sensitivity" if y in (2023, 2024, 2025) else "") for y in yl.index]
wcsv(yl.reset_index(), "fi_lvt_yields.csv")

# %% step 1: land - shares (evidence and calibration), holdings by decile and quintile, concentration
gap = F.plot_gap_evidence(2022)
plots = F.plot_price_evidence((2021, 2022, 2023))
bsr = pd.DataFrame([dict(year=y, n211_s14=F.balance_sheet("S14", "N211", y), n111_s14=F.balance_sheet("S14", "N111", y))
                    for y in range(2015, 2026)])
bsr["n211_over_n211_plus_n111"] = bsr["n211_s14"] / (bsr["n211_s14"] + bsr["n111_s14"])
# within-region gap: sales-weighted mean over the two complementary region groups (major cities / the rest)
gr = gap[(gap["source_table"] == "ashi 13mw") & (gap["building_type"] == "old dwellings: Building types total") &
         gap["region"].isin(["Major cities (total)", "Whole country excluding major cities"])]
gap_within = float((gr["gap"] * gr["sales_total"]).sum() / gr["sales_total"].sum())
gap_nat = float(gap[(gap["source_table"] == "ashi 13mw") & (gap["region"] == "Whole country") &
                    (gap["building_type"] == "old dwellings: Building types total")]["gap"].iloc[0])
rented_share = float(gap[(gap["source_table"] == "ashi 13mw") & (gap["region"] == "Whole country") &
                         (gap["building_type"] == "old dwellings: Building types total")].eval("sales_rented / sales_total").iloc[0])
pp = plots.set_index(["region", "year"])
mr_owner_mean = float(F.wv("main_residence")["total"] / (F.wv("main_residence", "participation_rate_pct")["total"] / 100.0))
ev = [dict(evidence="residual: 1 - N111 / survey dwelling value (2023)", value=SH["s_d"], role="central (the paper's construction)",
           note="market value of household dwellings (151u) minus residential structures at current cost (11zx N111)"),
      dict(evidence="N211 / (N211 + N111), households, 2022", value=float(bsr.set_index("year").loc[2022, "n211_over_n211_plus_n111"]),
           role=f"upper bound, the flow year (band high {F.S_D_BAND[1]:.2f})", note="N211 holds all household land, forest and farmland included"),
      dict(evidence="N211 / (N211 + N111), households, 2023", value=float(bsr.set_index("year").loc[2023, "n211_over_n211_plus_n111"]),
           role="upper bound, the survey year", note=f"N211 can be held only up to s_d = N211 / survey dwellings = {SH['s_d_max_n211_held']:.3f} (2023)"),
      dict(evidence="own vs rented plot price gap, old housing-company dwellings, whole country 2022", value=gap_nat,
           role="lower bound", note=f"rented plots are {100 * rented_share:.0f}% of sales and cluster in high-price cities, which pulls the national gap down"),
      dict(evidence="same, sales-weighted mean of the gaps within 'major cities' and 'rest of country'", value=gap_within,
           role=f"lower bound (band low {F.S_D_BAND[0]:.2f})", note="removes the city/country composition effect; municipal ground rents below market still bias it down"),
      dict(evidence="own vs rented plot gap, new blocks of flats, whole country / Greater Helsinki 2022",
           value=float(gap[(gap["source_table"] == "ashi 12de") & (gap["region"] == "Whole country") &
                           (gap["building_type"] == "new dwellings: Blocks of flats")]["gap"].iloc[0]),
           role="lower bound", note=f"Greater Helsinki {float(gap[(gap['source_table'] == 'ashi 12de') & (gap['region'] == 'Greater Helsinki') & (gap['building_type'] == 'new dwellings: Blocks of flats')]['gap'].iloc[0]):.3f}"),
      dict(evidence="single-family plot, whole country 2022: mean price EUR (25.9/m2 x 2,837 m2)",
           value=float(pp.loc[("Whole country", 2022), "plot_price_mean_eur"]), role="regional spread (not a share)",
           note=f"Greater Helsinki EUR {pp.loc[('Greater Helsinki', 2022), 'plot_price_mean_eur']:,.0f}; municipalities under 20,000 EUR "
                f"{pp.loc[('Under 20 000 inhabitants', 2022), 'plot_price_mean_eur']:,.0f}; mean owner-occupied main residence EUR {mr_owner_mean:,.0f} (151u 2023)"),
      dict(evidence="forest + farmland + business land share (residual from N211, 2023)", value=SH["s_f"], role="central",
           note="band 0.5-1.5: forest at the bare-land taxation value (below market), farmland at purchase prices, business net wealth mostly not land")]
EV = pd.DataFrame(ev)
wcsv(EV, "fi_lvt_land_evidence.csv")
wcsv(gap, "fi_lvt_plot_gap_2022.csv")
wcsv(bsr, "fi_lvt_balance_sheet_ratio.csv")
print("\nstep 1, land-share evidence:\n" + EV[["evidence", "value", "role"]].round(4).to_string(index=False))

# land by decile and quintile, per household and per share
ld = LD.copy()
for c in ["L_main", "L_ore", "L_ftr", "L_ffb", "B1", "B2"]:
    ld[f"{c}_share"] = ld[c] * ld["households"] / float((ld[c] * ld["households"]).sum())
ld["B2_meur"] = ld["B2"] * ld["households"] / 1e6
ld["main_residence_participation"] = F.wv("main_residence", "participation_rate_pct").reindex(DEC) / 100.0
ld["quintile"] = F.decile_to_quintile_key()
wcsv(ld.reset_index(), "fi_lvt_land_by_decile.csv")
lq = pd.DataFrame({f"{b}_per_household": LQ[b] for b in LQ})
for c in CONVS:
    for b in LQ:
        lq[f"{b}_per_share_{c}"] = 12.0 * F.land_per_share_month(M[c], LQ[b])
lq["shares_per_household"] = U.loc[Q, "shares"]
lq["households_hbs"] = HH
wcsv(lq.reset_index().rename(columns={"index": "quintile"}), "fi_lvt_land_by_quintile.csv")

# concentration: the top income decile's / quintile's share of each stock, Finland (151u) beside the US (SCF 2025)
N_D = LD["households"]
conc = []
for comp, lab in [("main_residence", "main residence"), ("housing_wealth", "dwellings (main + other + free-time)"),
                  ("forest_farmland_business", "forest, farmland, business"), ("financial_assets", "financial assets"),
                  ("net_wealth", "net wealth"), ("deposits", "deposits"), ("housing_loans", "housing loans"),
                  ("disposable_income", "disposable income")]:
    t = F.wv(comp).reindex(DEC) * N_D
    conc.append(dict(country="FI", item=lab, top_decile=float(t["d10"] / t.sum()), top_quintile=float(t[["d09", "d10"]].sum() / t.sum()),
                     bottom_half=float(t[DEC[:5]].sum() / t.sum()), source="151u 2023, income deciles"))
for b in ["B1", "B2"]:
    t = LD[b] * N_D
    conc.append(dict(country="FI", item=f"land {b}", top_decile=float(t["d10"] / t.sum()), top_quintile=float(t[["d09", "d10"]].sum() / t.sum()),
                     bottom_half=float(t[DEC[:5]].sum() / t.sum()), source="this unit"))
for c in CONVS:
    x = ACC_V[c]["vatable"] * M[c]["w"]
    conc.append(dict(country="FI", item=f"VAT-able consumption ({c})", top_decile=np.nan, top_quintile=float(x["q5"] / x.sum()),
                     bottom_half=np.nan, source="HBS 2022 quintiles, the bridge's weights"))
usl = F.us_out("us_lvt_land_by_decile.csv").set_index("decile")
for col, lab in [("L1_share", "land L1 (residential)"), ("L2_share", "land L2 (all)"), ("vatable_share", "VAT-able consumption (CE)"),
                 ("scf_houses_share", "home value (SCF)")]:
    conc.append(dict(country="US", item=lab, top_decile=float(usl.loc["d10", col]), top_quintile=float(usl.loc[["d09", "d10"], col].sum()),
                     bottom_half=float(usl.loc[DEC[:5], col].sum()), source="consumption/lvt/out/us_lvt_land_by_decile.csv"))
usw = F.us_wealth_concentration()
for v, lab in [("FIN", "financial assets"), ("NETWORTH", "net wealth"), ("INCOME", "income (pretax)")]:
    conc.append(dict(country="US", item=lab, top_decile=float(usw.loc[v, "top_decile"]), top_quintile=float(usw.loc[v, "top_quintile"]),
                     bottom_half=float(usw.loc[v, "bottom_half"]), source="SCF 2025 summary extract, INCPCTLECAT deciles"))
CONC = pd.DataFrame(conc)
wcsv(CONC, "fi_lvt_concentration.csv")
print("\nconcentration (top income decile / quintile share):\n" + CONC[["country", "item", "top_decile", "top_quintile"]].round(3).to_string(index=False))

# %% step 2: rates - bridge-equivalent phi and full capture, by base, measure and yield year
L_TOT = {b: float((LD[b] * LD["households"]).sum()) / 1e6 for b in ["B1", "B2"]}      # EUR million, survey population, 2022
L_TOT["B3"] = N211_22 + F.balance_sheet("S11", "N211", 2022) + F.balance_sheet("S15", "N211", 2022)   # all private land
HBS_SCALE = float(HH.sum()) / HBS_AGG                                                  # HBS households / survey households
rows = []
meas = [("m1", "10-year yield", lambda y: F.yield_of(y, 0.0, YLD)), ("m2", "10-year yield + 1.5", lambda y: F.yield_of(y, F.YIELD_SPREAD, YLD))]
for base in ["B1", "B2", "B3"]:
    Lb = L_TOT[base] * (HBS_SCALE if base != "B3" else 1.0)        # land held by the HBS population (B3: the balance sheet)
    for year in [2022, 2023, 2024, 2025]:
        for mk, lab, fn in meas:
            r = fn(year)
            rent = r * Lb
            for conv in (CONVS if base != "B3" else ["coherent"]):      # B3 exists only as an aggregate
                div_full = F.PHI_FULL * rent * 1e6 / (SHARES_TOT * 12.0)
                rows.append(dict(base=base, measure=mk, label=lab, yield_year=year, convention=conv, r=r, land_meur=Lb, rent_meur=rent,
                                 phi_bridge=np.nan, dividend_full=div_full, vat_dividend=DIV_V[conv], share_of_vat_dividend=np.nan,
                                 feasible=np.nan))
PHI = pd.DataFrame(rows)
# convention-exact phi and full-capture dividend for B1/B2 (the bridge's own weights); B3 only at the aggregate
for i, r in PHI.iterrows():
    if r["base"] in ("B1", "B2"):
        m = M[r["convention"]]
        mps = F.mean_land_ps(m, LQ[r["base"]])
        tau_b = F.tau_for_dividend(m, LQ[r["base"]], DIV_V[r["convention"]])
        PHI.loc[i, "phi_bridge"] = tau_b / r["r"]
        PHI.loc[i, "dividend_full"] = F.PHI_FULL * r["r"] * mps / 12.0
        PHI.loc[i, "tau_bridge_pct_of_land_value"] = 100.0 * tau_b
    else:
        PHI.loc[i, "phi_bridge"] = VAT_REV_MEUR / r["rent_meur"]
        PHI.loc[i, "tau_bridge_pct_of_land_value"] = 100.0 * VAT_REV_MEUR / r["land_meur"]
PHI["share_of_vat_dividend"] = PHI["dividend_full"] / PHI["vat_dividend"]
PHI["feasible"] = PHI["phi_bridge"] <= F.PHI_FULL
PHI["dwelling_value_loss_bridge"] = [F.dwelling_value_loss(p, SH["s_d"]) for p in PHI["phi_bridge"]]
PHI["dwelling_value_loss_full"] = F.PHI_FULL * SH["s_d"]
PHI["capitalized_land_loss_full_meur"] = F.PHI_FULL * PHI["land_meur"]
# the paper's flow measures (US conventions: 30% / 50% of housing services) and the Finnish land share of housing
# services, on residential land (B1) only: they measure the land rent inside housing
flow_rows = []
for mk, lab, rT in [("m3", "30% of housing services (paper's US measure)", 0.30 * HS_MEUR),
                    ("m4", "50% of housing services (paper's US measure)", 0.50 * HS_MEUR),
                    ("m5", f"housing services x s_d ({SH['s_d']:.3f})", SH["s_d"] * HS_MEUR)]:
    Lb = L_TOT["B1"] * HBS_SCALE
    r = rT / Lb
    for conv in CONVS:
        m = M[conv]
        mps = F.mean_land_ps(m, LQ["B1"])
        tau_b = F.tau_for_dividend(m, LQ["B1"], DIV_V[conv])
        flow_rows.append(dict(base="B1", measure=mk, label=lab, yield_year=2022, convention=conv, r=r, land_meur=Lb, rent_meur=rT,
                              phi_bridge=tau_b / r, dividend_full=F.PHI_FULL * r * mps / 12.0, vat_dividend=DIV_V[conv],
                              tau_bridge_pct_of_land_value=100.0 * tau_b))
FL = pd.DataFrame(flow_rows)
FL["share_of_vat_dividend"] = FL["dividend_full"] / FL["vat_dividend"]
FL["feasible"] = FL["phi_bridge"] <= F.PHI_FULL
FL["dwelling_value_loss_bridge"] = [F.dwelling_value_loss(p, SH["s_d"]) for p in FL["phi_bridge"]]
FL["dwelling_value_loss_full"] = F.PHI_FULL * SH["s_d"]
FL["capitalized_land_loss_full_meur"] = F.PHI_FULL * FL["land_meur"]
PHI = pd.concat([PHI, FL], ignore_index=True)
# the Finnish-law VAT dividend (172.4 post / 178.0 coherent) as the bridge-equivalent target, main base and measure
for conv in CONVS:
    tau_l = F.tau_for_dividend(M[conv], LQ["B2"], DIV_V_LAW[conv])
    PHI.loc[len(PHI)] = dict(base="B2", measure="m1", label="10-year yield; VAT dividend under Finnish law", yield_year=2022,
                             convention=conv, r=Y22, land_meur=L_TOT["B2"] * HBS_SCALE, rent_meur=Y22 * L_TOT["B2"] * HBS_SCALE,
                             phi_bridge=tau_l / Y22, dividend_full=F.PHI_FULL * Y22 * F.mean_land_ps(M[conv], LQ["B2"]) / 12.0,
                             vat_dividend=DIV_V_LAW[conv], tau_bridge_pct_of_land_value=100.0 * tau_l,
                             share_of_vat_dividend=np.nan, feasible=np.nan)
PHI["share_of_vat_dividend"] = PHI["dividend_full"] / PHI["vat_dividend"]
PHI["feasible"] = PHI["phi_bridge"] <= F.PHI_FULL
PHI["dwelling_value_loss_bridge"] = [F.dwelling_value_loss(p, SH["s_d"]) for p in PHI["phi_bridge"]]
wcsv(PHI, "fi_lvt_phi.csv")
main = PHI[(PHI["yield_year"] == 2022) & (PHI["convention"] == "coherent")]
print("\nstep 2, rates (coherent, 2022):\n" + main[["base", "measure", "label", "r", "phi_bridge", "dividend_full", "share_of_vat_dividend",
                                                      "tau_bridge_pct_of_land_value", "dwelling_value_loss_bridge"]].round(4).to_string(index=False))
sens = PHI[(PHI["measure"].isin(["m1", "m2"])) & (PHI["convention"] == "coherent") & (PHI["base"] == "B2")
           & ~PHI["label"].str.contains("law")].pivot_table(index="yield_year", columns="measure", values="share_of_vat_dividend")
print("   full-capture dividend / VAT dividend, B2, by yield year:\n" + sens.round(3).to_string())
# yield timing: the land stock is dated end-2022 and the 2022 yield is an annual mean in a year when yields rose from
# 0.2% to 2.7%; the paper pairs annual means. December 2022 alone, and the range over every yield-based case
mps_c = F.mean_land_ps(M["coherent"], LQ["B2"])
share_dec = F.PHI_FULL * Y22_DEC * mps_c / 12.0 / DIV_V["coherent"]
yc = PHI[(PHI["base"] == "B2") & PHI["measure"].isin(["m1", "m2"]) & (PHI["convention"] == "coherent") & ~PHI["label"].str.contains("law")]
rev("yield_2022_12_pct", 100 * Y22_DEC, "% a year", "Eurostat monthly, December 2022")
rev("full_capture_share_dec2022_yield", share_dec, "share of the VAT dividend", "B2, coherent, phi 0.98 at the December 2022 yield")
rev("full_capture_share_min_yield_cases", float(yc["share_of_vat_dividend"].min()), "share of the VAT dividend", "B2, m1 and m2, 2022-2025 annual yields")
rev("full_capture_share_max_yield_cases", float(yc["share_of_vat_dividend"].max()), "share of the VAT dividend", "B2, m1 and m2, 2022-2025 annual yields")
# the rates table prints the coherent rows; how far the post convention's rows sit from them
dd_ = []
for _, r_ in PHI[(PHI["convention"] == "coherent") & (PHI["base"] != "B3")].iterrows():
    p_ = PHI[(PHI["convention"] == "post") & (PHI["base"] == r_["base"]) & (PHI["measure"] == r_["measure"]) &
             (PHI["yield_year"] == r_["yield_year"]) & (PHI["label"] == r_["label"])]
    if len(p_):
        dd_.append((abs(float(p_["phi_bridge"].iloc[0]) - r_["phi_bridge"]),
                    100 * abs(float(p_["share_of_vat_dividend"].iloc[0]) - r_["share_of_vat_dividend"])))
rev("post_vs_coherent_max_abs_diff_phi", max(d[0] for d in dd_), "phi", "rates table rows, B1 and B2, every measure and yield year")
rev("post_vs_coherent_max_abs_diff_share_pts", max(d[1] for d in dd_), "points of the VAT dividend", "largest on the housing-services rows (m3-m5)")
print(f"   December 2022 yield {100 * Y22_DEC:.2f}%: full capture funds {100 * share_dec:.1f}% of the bridge's dividend; every yield case "
      f"{100 * yc['share_of_vat_dividend'].min():.1f}-{100 * yc['share_of_vat_dividend'].max():.1f}%. Post vs coherent: phi within "
      f"{max(d[0] for d in dd_):.3f}, share within {max(d[1] for d in dd_):.2f} points")

R = {"m1": Y22, "m2": Y22 + F.YIELD_SPREAD / 100.0}


def tau_of(rate, base, conv):
    """Annual charge on land value for a rate concept: 'bridge' (notional: the VAT dividend), 'full_m1', 'full_m2'
    (the 2022 yield, + 1.5), or 'full_y<year>' (full capture at another year's annual yield; the yield-year table)."""
    if rate == "bridge":
        return F.tau_for_dividend(M[conv], LQ[base], DIV_V[conv])
    if rate.startswith("full_y"):
        return F.PHI_FULL * F.yield_of(int(rate[6:]), ylds=YLD)
    if rate.startswith("full_"):
        return F.PHI_FULL * R[rate.split("_")[1]]
    raise ValueError(rate)


# %% step 3: incidence by quintile, inside the deciles, liquidity, MPC grades
RATES = ["bridge", "full_m1", "full_m2"]
acc_rows, ACC_L = [], {}
for conv in CONVS:
    m = M[conv]
    av = ACC_V[conv]
    for q in Q:
        acc_rows.append(dict(convention=conv, instrument="VAT", base="", rate="bridge", quintile=q, base_value=float(av.loc[q, "vatable"]),
                             bill=float(av.loc[q, "tax"]), dividend=float(av.loc[q, "dividend"]), net=float(av.loc[q, "net"]),
                             budget=float(av.loc[q, "budget"]), net_pct_budget=float(av.loc[q, "net_pct_budget"]), tau=B.TAU))
    for base in ["B1", "B2"]:
        for rate in RATES:
            tau = tau_of(rate, base, conv)
            a = F.lvt_accounting(m, LQ[base], tau)
            ACC_L[(conv, base, rate)] = a
            for q in Q:
                acc_rows.append(dict(convention=conv, instrument="LVT", base=base, rate=rate, quintile=q, base_value=float(a.loc[q, "land_value_ps"]),
                                     bill=float(a.loc[q, "bill"]), dividend=float(a.loc[q, "dividend"]), net=float(a.loc[q, "net"]),
                                     budget=float(a.loc[q, "budget"]), net_pct_budget=float(a.loc[q, "net_pct_budget"]), tau=tau))
ACC = pd.DataFrame(acc_rows)
wcsv(ACC, "fi_lvt_accounting_by_quintile.csv")
pv = ACC[(ACC["convention"] == "coherent") & ((ACC["instrument"] == "VAT") | (ACC["base"] == "B2"))].pivot_table(
    index=["instrument", "rate"], columns="quintile", values="net")
print("\nstep 3, net per adult share per month (coherent; LVT on B2):\n" + pv.round(2).to_string())
pv = ACC[(ACC["convention"] == "coherent") & ((ACC["instrument"] == "VAT") | (ACC["base"] == "B2"))].pivot_table(
    index=["instrument", "rate"], columns="quintile", values="net_pct_budget")
print("   % of budget:\n" + pv.round(2).to_string())

# inside the deciles: owners pay, non-owners receive (parametric split from the published quartiles)
P_OWN = F.wv("main_residence", "participation_rate_pct").reindex(DEC) / 100.0
mrq = {k: F.wv("main_residence", k).reindex(DEC) for k in ("p25", "p75")}
SIG_OWN = (np.log(mrq["p75"]) - np.log(mrq["p25"])) / (2.0 * F.norm.ppf(0.75))
KEY = F.decile_to_quintile_key()
S_DEC = {c: pd.Series(M[c]["units"].loc[Q, "shares"].values.repeat(2), index=DEC) for c in CONVS}
HTM = {k: F.htm_by_decile(v) for k, v in F.HTM_DIVISOR.items()}
HTM_T = {k: F.htm_by_tenure(v) for k, v in F.HTM_DIVISOR.items()}
HTM_OWN = {k: F.htm_owners(v) for k, v in F.HTM_DIVISOR.items()}
OC = F.owner_counts()
MB = F.mortgaged_by_decile()
K_OUT = 1.0 - MB["k_mortgaged_value_share"]                   # outright owners' share of the decile's main-residence value


def to_q(x_dec, per_share_conv=None, tau=1.0):
    """Decile per-household amounts -> quintile pair means; optionally x tau / (12 s_q) (euros per share per month)."""
    x = F.pair_quintiles(x_dec)
    if per_share_conv is None:
        return x
    return x * tau / (12.0 * M[per_share_conv]["units"].loc[Q, "shares"])


def lvt_flows(conv, base, rate, htm_key="half_month", defer=None, tau=None):
    """Within-quintile LVT flows (euros per share per month): receipts, payments, net, payers' HtM share, the
    accounting frame, and (with defer='outright_full' / 'outright_cash') the deferral of outright owners' bills on
    main-residence land (paid in full by state lending / cash-balanced dividend). tau overrides the rate's charge."""
    m = M[conv]
    tau = tau_of(rate, base, conv) if tau is None else tau
    mps = F.mean_land_ps(m, LQ[base])
    om = F.owner_model(LD[base], S_DEC[conv], mps, P_OWN, SIG_OWN)
    recv = to_q(om["recv_nonowner"] + om["recv_owner"], conv, tau)
    pay = to_q(om["pay_owner"], conv, tau)
    h = (HTM_OWN[htm_key] * om["pay_owner"]).groupby(KEY).sum() / om["pay_owner"].groupby(KEY).sum()
    acc = F.lvt_accounting(m, LQ[base], tau)
    out = dict(conv=conv, base=base, rate=rate, tau=tau, recv=recv, pay=pay, net=acc["net"].copy(), h=h.reindex(Q), acc=acc, om=om,
               deferred=pd.Series(0.0, index=Q), d_div=0.0)
    if defer:
        dfd = to_q(LD["L_main"] * K_OUT, conv, tau)                       # deferred bill, per share per month
        payer_land = 1.0 - F.norm.cdf((np.log(om["L_star"]) - (np.log(om["L_per_owner"]) - om["sigma"] ** 2 / 2)) / om["sigma"] - om["sigma"])
        fpay = (payer_land * LD["L_main"] * K_OUT).groupby(KEY).sum() / (LD["L_main"] * K_OUT).groupby(KEY).sum()
        d_pay = (dfd * fpay.reindex(Q)).clip(upper=pay)
        out["pay"] = pay - d_pay
        out["recv"] = recv + (dfd - d_pay)
        out["deferred"] = dfd
        out["net"] = acc["net"] + dfd
        if defer == "outright_cash":
            d_div = float((m["w"] * dfd).sum())
            out["d_div"] = d_div
            out["net"] = out["net"] - d_div
            out["recv"] = out["recv"] - d_div          # the cut falls on every share; booked against receipts
    assert np.allclose((out["recv"] - out["pay"]).values, out["net"].values, atol=1e-8), "within-quintile split does not add up"
    return out


def vat_flows(conv, sigma_c=F.SIGMA_C["mid"], htm_key="half_month"):
    """Within-quintile VAT flows: VAT-able consumption per share log-normal around the quintile mean (sigma_c);
    payers are households above the population mean Cbar_v."""
    av = ACC_V[conv]
    t = float(av["Cbar_v"].iloc[0])
    above, below, _ = F.lognormal_split(av["vatable"].values, t, sigma_c)
    recv = pd.Series(B.TAU * below, index=Q)
    pay = pd.Series(B.TAU * above, index=Q)
    h = F.pair_quintiles(HTM[htm_key]["htm_share"])
    out = dict(conv=conv, base="", rate="bridge", tau=B.TAU, recv=recv, pay=pay, net=av["net"].copy(), h=h, acc=av,
               deferred=pd.Series(0.0, index=Q), d_div=0.0)
    assert np.allclose((recv - pay).values, out["net"].values, atol=1e-8)
    return out


GRADES = {"post_mid": ("post", "mid", None), "post_low": ("post", "low", None), "post_high": ("post", "high", None),
          "liq_mid": ("liq", "mid", None), "wealth_mid": ("wealth", "mid", "mid"), "wealth_low": ("wealth", "mid", "low"),
          "wealth_high": ("wealth", "mid", "high")}
GRADE_LABEL = {"post_mid": "the post's schedule (mid), quintile-netted: the post's method",
               "post_low": "low schedule, quintile-netted", "post_high": "high schedule, quintile-netted",
               "liq_mid": "recipients at the schedule; payers 1.0 if hand-to-mouth, else the schedule",
               "wealth_mid": "recipients at the schedule; payers 1.0 if hand-to-mouth, else 0.56 (top quintile) whatever their income",
               "wealth_low": "as wealth_mid, unconstrained payers at 0.25",
               "wealth_high": "as wealth_mid, unconstrained payers at 0.68 (high schedule's top)"}


def dC_of(fl, grade):
    kind, sch, mu = GRADES[grade]
    mpc = SCHED[sch].values
    return F.graded_dC(fl["net"].values, fl["recv"].values, fl["pay"].values, mpc, fl["h"].values, kind,
                       None if mu is None else MPC_U[mu])


# liquidity by decile and the grades' MPCs by quintile
lq_rows = []
for dd in DEC:
    r = dict(decile=dd, households=float(OC.loc[dd, "n_households"]), owners=float(OC.loc[dd, "n_owners"]),
             mortgaged=float(OC.loc[dd, "n_mortgaged"]), outright=float(OC.loc[dd, "n_outright"]))
    for k in F.HTM_DIVISOR:
        r[f"htm_all_{k}"] = float(HTM[k].loc[dd, "htm_share"])
        r[f"htm_owners_{k}"] = float(HTM_OWN[k].loc[dd])
    for c in ["deposits_median_holders", "income_median", "deposit_months_at_median", "liquid_mean", "income_mean", "liquid_months_of_mean_income"]:
        r[c] = float(HTM["half_month"].loc[dd, c])
    lq_rows.append(r)
LIQ = pd.DataFrame(lq_rows)
ht = pd.concat({k: v for k, v in HTM_T.items()}, names=["threshold", "tenure"]).reset_index()
wcsv(LIQ, "fi_lvt_liquidity.csv")
wcsv(ht, "fi_lvt_liquidity_tenure.csv")
print("\nliquidity: hand-to-mouth share (deposits <= half a month's income), all households / owners, by decile:\n" +
      LIQ.set_index("decile")[["htm_all_half_month", "htm_owners_half_month", "deposit_months_at_median", "liquid_months_of_mean_income"]].round(3).T.to_string())

FL_MAIN = {}
for conv in CONVS:
    FL_MAIN[(conv, "VAT", "bridge")] = vat_flows(conv)
    for base in ["B1", "B2"]:
        for rate in RATES:
            FL_MAIN[(conv, f"LVT_{base}", rate)] = lvt_flows(conv, base, rate)
wd_rows = []
for conv in CONVS:
    for base in ["B1", "B2"]:
        om = FL_MAIN[(conv, f"LVT_{base}", "bridge")]["om"]
        tau_b = FL_MAIN[(conv, f"LVT_{base}", "bridge")]["tau"]
        for dd in DEC:
            sdd = float(S_DEC[conv][dd])
            wd_rows.append(dict(convention=conv, base=base, decile=dd, owners_share=float(om.loc[dd, "p_own"]), sigma=float(om.loc[dd, "sigma"]),
                                land_per_household=float(om.loc[dd, "L_hh"]), land_per_owner=float(om.loc[dd, "L_per_owner"]),
                                payer_threshold_land=float(om.loc[dd, "L_star"]), payer_share_of_owners=float(om.loc[dd, "payer_share_of_owners"]),
                                payer_share_of_households=float(om.loc[dd, "payer_share_of_households"]),
                                gross_receipts_eur_share_month_bridge=float((om.loc[dd, "recv_nonowner"] + om.loc[dd, "recv_owner"]) * tau_b / (12 * sdd)),
                                gross_payments_eur_share_month_bridge=float(om.loc[dd, "pay_owner"] * tau_b / (12 * sdd)),
                                net_eur_share_month_bridge=float(om.loc[dd, "net"] * tau_b / (12 * sdd)),
                                owner_htm_share=float(HTM_OWN["half_month"].loc[dd])))
WD = pd.DataFrame(wd_rows)
WD["households"] = WD["decile"].map(OC["n_households"])
wcsv(WD, "fi_lvt_within_decile.csv")
wdm = WD[(WD["convention"] == "coherent") & (WD["base"] == "B2")].set_index("decile")
pay_share_all = float((wdm["payer_share_of_households"] * wdm["households"]).sum() / wdm["households"].sum())
print(f"\ninside the deciles (B2, coherent): {100 * pay_share_all:.1f}% of households pay net (rate-invariant); payer share by decile: "
      + ", ".join(f"{100 * v:.0f}%" for v in wdm["payer_share_of_households"]))
# gross flows on one unit: euros per share x payment shares per household x households = euros a month in the decile
units_hh = S_DEC["coherent"] * wdm["households"]
gp = wdm["gross_payments_eur_share_month_bridge"] * units_hh
gr_ = wdm["gross_receipts_eur_share_month_bridge"] * units_hh
BH_GP = float(gp[DEC[:5]].sum() / gp.sum())
D12_PR = float(gp[DEC[:2]].sum() / gr_[DEC[:2]].sum())
rev("bottom_half_share_of_gross_lvt_payments", BH_GP, "share", "D1-D5, per-share payments x shares per household x households (one unit); the same at any rate")
rev("gross_payments_over_receipts_d1_d2", D12_PR, "ratio", "D1-D2, same unit")
rev("households_paying_net_lvt", pay_share_all, "share", "owner model (renters' land assigned to owners); any rate")
# renters' own land (cottages, other dwellings, forest; 151z), which the owner model hands to the decile's owners: the
# 'renters pay nothing' of the model is this assumption, not a measurement
tv_ = lambda c, k="mean": float(F.wv(c, k, "tenure")["renter_or_other"])
REN_LAND = (SH["s_d"] * (tv_("other_residential_property") + tv_("free_time_residences")) + SH["s_f"] * tv_(F.FFB_ITEM)) * \
    tv_("disposable_income", "households_holding") / 1e6
rev("renters_share_of_household_land", REN_LAND / N211_23, "share", "151z 2023 renters' other dwellings and cottages x s_d plus forest/farmland/business x s_f, "
    "over N211 2023; the owner model assigns it to owners")
rev("renters_share_of_households", 1.0 - float(F.wv("main_residence", "participation_rate_pct")["total"]) / 100.0, "share", "151u 2023: households without a main residence")
print("   share of all gross payments made in D1-D5: %.1f%%; gross payments / gross receipts in D1-D2: %.3f (one unit: euros a month)" % (
    100 * BH_GP, D12_PR))

mg_rows = []
for conv in ["coherent"]:
    for inst in ["VAT", "LVT_B2", "LVT_B1"]:
        fl = FL_MAIN[(conv, inst, "bridge")]
        for g in GRADES:
            kind, sch, mu = GRADES[g]
            for i, q in enumerate(Q):
                mpc = float(SCHED.loc[q, sch])
                pay_mpc = {"post": mpc, "liq": float(fl["h"].iloc[i]) + (1 - float(fl["h"].iloc[i])) * mpc,
                           "wealth": float(fl["h"].iloc[i]) + (1 - float(fl["h"].iloc[i])) * (MPC_U[mu] if mu else np.nan)}[kind]
                mg_rows.append(dict(convention=conv, instrument=inst, grade=g, quintile=q, recipient_mpc=mpc, payer_mpc=pay_mpc,
                                    payer_htm_share=float(fl["h"].iloc[i]), gross_receipts=float(fl["recv"].iloc[i]),
                                    gross_payments=float(fl["pay"].iloc[i]), net=float(fl["net"].iloc[i]), grade_label=GRADE_LABEL[g]))
MG = pd.DataFrame(mg_rows)
wcsv(MG, "fi_lvt_mpc_grades.csv")

# %% step 4: demand - flow impulses for every instrument x convention x rate x grade (+ deferral), category shifts
imp_rows, SHIFT = [], {}
jobs = []
for conv in CONVS:
    jobs.append((conv, "VAT", "", "bridge", None))
    for base in ["B1", "B2"]:
        for rate in RATES:
            jobs.append((conv, "LVT", base, rate, None))
            if base == "B2":
                jobs += [(conv, "LVT", base, rate, "outright_full"), (conv, "LVT", base, rate, "outright_cash")]
for conv, inst, base, rate, defer in tqdm(jobs, desc="flows x grades"):
    m = M[conv]
    fl = FL_MAIN[(conv, "VAT", "bridge")] if inst == "VAT" else (
        FL_MAIN[(conv, f"LVT_{base}", rate)] if defer is None else lvt_flows(conv, base, rate, defer=defer))
    for g in GRADES:
        dC = dC_of(fl, g)
        shock = F.shock_of(m, dC)
        imp = B.impulse(m, shock=shock)
        key = (conv, inst, base, rate, defer or "none", g)
        if defer is None and g in ("post_mid", "wealth_mid", "liq_mid"):
            if g == "post_mid":
                sh = B.shifts_from_transfers(m, fl["net"], mpc=SCHED["mid"].values, mpc_label="mid")
            else:
                sh = B.shifts_from_transfers(m, None, shock=shock, mpc_label="mid")
            SHIFT[key] = sh
        dividend = float(fl["acc"]["dividend"].iloc[0]) - fl["d_div"]
        imp_rows.append(dict(convention=conv, instrument=inst, base=base, rate=rate, defer=defer or "none", grade=g,
                             flow_eur=imp["flow_usd"], flow_pct_consumption=imp["flow_pct_consumption"],
                             bars_chart_eur=imp["bars_chart_usd"], bars_all_eur=imp["bars_all_usd"], dividend=dividend,
                             tau=fl["tau"], deferred_share_of_revenue=float((m["w"] * fl["deferred"]).sum()) / float(fl["acc"]["dividend"].iloc[0]),
                             gross_payments_eur=float((m["w"] * fl["pay"]).sum()), gross_receipts_eur=float((m["w"] * fl["recv"]).sum()),
                             grade_label=GRADE_LABEL[g]))
IMP = pd.DataFrame(imp_rows)
wcsv(IMP, "fi_lvt_impulse.csv")
# the liquidity grade is asymmetric: VAT payers (each quintile's top spenders) get the hand-to-mouth share of ALL its
# households, LVT payers (owners) that of owners, which is lower; at owners' shares the VAT's graded impulse rises
fv_own = dict(FL_MAIN[("coherent", "VAT", "bridge")], h=F.pair_quintiles(HTM_OWN["half_month"]))
VAT_LIQ_OWN = B.impulse(M["coherent"], shock=F.shock_of(M["coherent"], dC_of(fv_own, "liq_mid")))["flow_pct_consumption"]
liq_ = {i: float(IMP[(IMP["convention"] == "coherent") & (IMP["instrument"] == i) & (IMP["base"] == ("B2" if i == "LVT" else "")) &
                     (IMP["rate"] == "bridge") & (IMP["grade"] == "liq_mid") & (IMP["defer"] == "none")]["flow_pct_consumption"].iloc[0]) for i in ("LVT", "VAT")}
rev("vat_flow_liq_grade_owner_htm_shares", VAT_LIQ_OWN, "% of consumption", "VAT payers given owners' hand-to-mouth shares (the LVT payers' grade)")
rev("lvt_vat_ratio_liq_grade", liq_["LVT"] / liq_["VAT"], "ratio", "same revenue, B2, coherent: an upper bound")
rev("lvt_vat_ratio_liq_grade_owner_shares", liq_["LVT"] / VAT_LIQ_OWN, "ratio", "both instruments' payers at owners' hand-to-mouth shares")
print(f"   liquidity grade: VAT {liq_['VAT']:.3f} at all households' hand-to-mouth shares, {VAT_LIQ_OWN:.3f} at owners'; LVT/VAT "
      f"{liq_['LVT'] / liq_['VAT']:.3f} -> {liq_['LVT'] / VAT_LIQ_OWN:.3f}")
sel = IMP[(IMP["defer"] == "none") & ((IMP["instrument"] == "VAT") | (IMP["base"] == "B2"))]
print("\nstep 4, flow impulse, % of consumption (B2 for the LVT):\n" +
      sel.pivot_table(index=["convention", "instrument", "rate"], columns="grade", values="flow_pct_consumption").round(3).to_string())
dsel = IMP[(IMP["base"] == "B2") & (IMP["convention"] == "coherent") & IMP["grade"].isin(["post_mid", "wealth_mid"])]
print("   deferral (coherent, B2):\n" + dsel.pivot_table(index=["rate", "defer"], columns="grade", values="flow_pct_consumption").round(3).to_string()
      + "\n   deferred share of revenue: %.3f" % float(IMP[(IMP["defer"] == "outright_full") & (IMP["base"] == "B2")]["deferred_share_of_revenue"].iloc[0]))

# category shifts: every version on one frame (euros per share per month; the post convention also on the post's
# euro conversion, so its VAT bars are the published Fig 2 bars)
sh_rows = []
for (conv, inst, base, rate, defer, g), sh in SHIFT.items():
    m = M[conv]
    eur = sh["dUSD_mid"]
    eur_post = B.fi_post_eur(m, eur)
    for cat in sh.index:
        sh_rows.append(dict(convention=conv, instrument=inst, base=base, rate=rate, grade=g, category=cat, role=sh.loc[cat, "role"],
                            code=m["code"][cat], Cbar=float(m["Cbar"][cat]), dEUR=float(eur[cat]), dPct=float(sh.loc[cat, "dPct_mid"]),
                            dEUR_post_conversion=float(eur_post[cat]),
                            dEUR_mpc1=float(sh.loc[cat, "dUSD_mpc1"]) if "dUSD_mpc1" in sh else np.nan,
                            dPct_mpc1=float(sh.loc[cat, "dPct_mpc1"]) if "dPct_mpc1" in sh else np.nan))
SHF = pd.DataFrame(sh_rows)
wcsv(SHF, "fi_lvt_demand_shifts.csv")
# the published Fig 2 bar for rent, as a check that the VAT side here is the rebuild's
rent_post = float(SHF[(SHF["convention"] == "post") & (SHF["instrument"] == "VAT") & (SHF["grade"] == "post_mid") &
                      (SHF["category"] == "04.1 Actual rents")]["dEUR_post_conversion"].iloc[0])
print(f"\nVAT rent bar, post convention on the post's euro conversion: EUR {rent_post:.3f} (published 4.92; rebuild 4.93)")


def compare(conv, lvt_key, vat_key, label):
    """LVT bars against the VAT bars on the chart categories: sign agreement, ratio, share of each version's impulse."""
    a = SHF[(SHF["convention"] == conv) & (SHF["instrument"] == "LVT") & (SHF["base"] == lvt_key[0]) & (SHF["rate"] == lvt_key[1]) &
            (SHF["grade"] == lvt_key[2])].set_index("category")
    v = SHF[(SHF["convention"] == conv) & (SHF["instrument"] == "VAT") & (SHF["grade"] == vat_key)].set_index("category")
    chart = M[conv]["chart"]
    d = pd.DataFrame({"vat": v.loc[chart, "dEUR"], "lvt": a.loc[chart, "dEUR"]})
    d["ratio"] = d["lvt"] / d["vat"]
    d["same_sign"] = np.sign(d["lvt"]) == np.sign(d["vat"])
    d["vat_share_of_chart"] = d["vat"] / d["vat"].sum()
    d["lvt_share_of_chart"] = d["lvt"] / d["lvt"].sum()
    # ghost flips: the bar's sign at MPC = 1 (the post's ghost) against its MPC-adjusted sign (post's method only)
    ghost = lvt_key[2] == "post_mid" and vat_key == "post_mid"
    d["vat_ghost_flip"] = (np.sign(v.loc[chart, "dEUR_mpc1"]) != np.sign(v.loc[chart, "dEUR"])) if ghost else np.nan
    d["lvt_ghost_flip"] = (np.sign(a.loc[chart, "dEUR_mpc1"]) != np.sign(a.loc[chart, "dEUR"])) if ghost else np.nan
    d["comparison"] = label
    d["convention"] = conv
    return d


cmp_list = []
for conv in CONVS:
    for base in ["B2", "B1"]:
        for rate in RATES:
            cmp_list.append(compare(conv, (base, rate, "post_mid"), "post_mid", f"LVT {base} {rate} vs VAT, the post's method (mid)"))
        cmp_list.append(compare(conv, (base, "bridge", "wealth_mid"), "wealth_mid", f"LVT {base} bridge vs VAT, unconstrained payers draw on wealth"))
CMP = pd.concat(cmp_list).reset_index().rename(columns={"index": "category"})
wcsv(CMP, "fi_lvt_demand_compare.csv")
c0 = CMP[(CMP["comparison"] == "LVT B2 bridge vs VAT, the post's method (mid)") & (CMP["convention"] == "coherent")].set_index("category")
big = c0.reindex(c0["lvt"].abs().sort_values(ascending=False).index)
print("\nLVT (B2, notional bridge rate) vs VAT bars, coherent, the post's method: %d/%d same sign; ratio median %.2f "
      "[%.2f, %.2f] over bars above EUR 0.05; share of impulse, rent: LVT %.1f%% vs VAT %.1f%%" % (
          int(c0["same_sign"].sum()), len(c0), float(c0.loc[c0["vat"].abs() > 0.05, "ratio"].median()),
          float(c0.loc[c0["vat"].abs() > 0.05, "ratio"].min()), float(c0.loc[c0["vat"].abs() > 0.05, "ratio"].max()),
          100 * c0.loc["04.1 Actual rents", "lvt_share_of_chart"], 100 * c0.loc["04.1 Actual rents", "vat_share_of_chart"]))
print(big.head(12)[["vat", "lvt", "ratio", "vat_share_of_chart", "lvt_share_of_chart"]].round(3).to_string())
flips = c0[~c0["same_sign"]]
print("   bars that flip sign:", ", ".join(f"{k} ({r['vat']:+.3f} -> {r['lvt']:+.3f})" for k, r in flips.iterrows()) or "none")
# ghost flips (MPC = 1 ghost against the MPC-adjusted bar), both conventions, LVT B2 and VAT at the same revenue
GHOST = {}
for conv in CONVS:
    cg = CMP[(CMP["comparison"] == "LVT B2 bridge vs VAT, the post's method (mid)") & (CMP["convention"] == conv)].set_index("category")
    for inst in ("lvt", "vat"):
        GHOST[(conv, inst)] = sorted(cg.index[cg[f"{inst}_ghost_flip"].astype(bool)])
        rev(f"ghost_flips_{conv}_{inst}", len(GHOST[(conv, inst)]), "bars of 37", "charted bars whose MPC=1 ghost and MPC-adjusted bar differ in sign (B2, same revenue)")
VEH_OP = "07.2 Operation of personal transport equipment"
rev("ghost_flip_vehicle_operation_under_both_all_conventions", float(all(VEH_OP in GHOST[(c, i)] for c in CONVS for i in ("lvt", "vat"))), "1 = yes", "")
print("   ghost flips (MPC=1 ghost vs MPC-adjusted bar): " + "; ".join(f"{c} LVT {len(GHOST[(c, 'lvt')])}, VAT {len(GHOST[(c, 'vat')])}" for c in CONVS)
      + f"; vehicle operation flips under both in both conventions: {all(VEH_OP in GHOST[(c, i)] for c in CONVS for i in ('lvt', 'vat'))}")
# rent's share of the flow impulse (the money each version moves) against its share of the charted bars (which add
# the division-parent over-allocation and leave out the off-chart lines, imputed rent among them)
for inst, base in [("LVT", "B2"), ("VAT", "")]:
    ir = IMP[(IMP["convention"] == "coherent") & (IMP["instrument"] == inst) & (IMP["base"] == base) & (IMP["rate"] == "bridge") &
             (IMP["grade"] == "post_mid") & (IMP["defer"] == "none")].iloc[0]
    rent_ = float(c0.loc["04.1 Actual rents", inst.lower()])
    rev(f"rent_share_of_flow_{inst.lower()}", rent_ / float(ir["flow_eur"]), "share", "rent bar / flow impulse (coherent, same revenue, post's method)")
    rev(f"rent_share_of_charted_{inst.lower()}", rent_ / float(ir["bars_chart_eur"]), "share", "rent bar / sum of the 37 charted bars")
print("   rent: %.1f%% of the LVT's flow impulse and %.1f%% of the VAT's (%.1f%% / %.1f%% of the charted bars)" % tuple(
    100 * next(r["value"] for r in REV if r["item"] == k) for k in ("rent_share_of_flow_lvt", "rent_share_of_flow_vat", "rent_share_of_charted_lvt", "rent_share_of_charted_vat")))

# quintile segments of the ten largest movers (Fig 3 analog), LVT and VAT, coherent, the post's method
seg_rows = []
for inst, key in [("LVT_B2", ("coherent", "LVT", "B2", "bridge", "none", "post_mid")), ("VAT", ("coherent", "VAT", "", "bridge", "none", "post_mid"))]:
    m = M["coherent"]
    fl = FL_MAIN[("coherent", inst, "bridge")]
    shock = B.budget_shock(fl["net"], SCHED["mid"].values, m["budget"])
    dec = B.decompose(m, shock)
    top = B.top_movers(SHIFT[key], "dUSD_mid", m["chart"], 10)
    for cat in top:
        for q in Q:
            seg_rows.append(dict(instrument=inst, category=cat, quintile=q, segment_eur=float(dec.loc[cat, q]), net_eur=float(dec.loc[cat].sum())))
SEG = pd.DataFrame(seg_rows)
wcsv(SEG, "fi_lvt_decomposition_top10.csv")
st = SEG.groupby(["instrument", "category"]).apply(lambda d: pd.Series({
    "net": d["segment_eur"].sum(), "gross_in": d.loc[d["segment_eur"] > 0, "segment_eur"].sum(),
    "gross_out": d.loc[d["segment_eur"] < 0, "segment_eur"].sum(), "q5_share_of_out": d.loc[d["quintile"] == "q5", "segment_eur"].sum() /
    d.loc[d["segment_eur"] < 0, "segment_eur"].sum() if (d["segment_eur"] < 0).any() else np.nan}), include_groups=False)
print("\ntop-10 movers, gross flows by quintile (coherent, bridge rate):\n" + st.round(3).to_string())

# tenure-aware baskets (extension): rent with renters, imputed rent / interest / housing-company charges with owners.
# Main: owners' changes spread over the lines they transact (imputed rent and loan interest cannot move at impact);
# sensitivity (dEUR_as_allocated): the Working-model allocation at the owner basket, imputed rent and interest included
P_OWN_Q = F.pair_quintiles(P_OWN)
flags = B.fi_vat_flags()
ten_rows, TEN_OWNER = [], {}


def owner_part(m, tm, dc_o, owner_basket):
    """Owners' contribution to each line (euros per share per month, population mean) for one owner allocation."""
    sh = F.tenure_marginal_shares(tm, owner_basket)["owner"]
    return (sh * (m["w"] * P_OWN_Q.values * pd.Series(np.asarray(dc_o, float), index=m["C"].columns)).values).sum(axis=1)


def ten_append(conv, inst, base, g, m, tm, dc_o, dc_r):
    tot = {ob: F.shifts_tenure_aware(m, tm, dc_o, dc_r, P_OWN_Q.values, ob) for ob in F.OWNER_BASKETS}
    TEN_OWNER[(conv, inst, base, g)] = {ob: owner_part(m, tm, dc_o, ob) for ob in F.OWNER_BASKETS}
    pe = {ob: B.fi_post_eur(m, tot[ob]) for ob in F.OWNER_BASKETS}
    for cat in m["C"].index:
        ten_rows.append(dict(convention=conv, instrument=inst, base=base, rate="bridge", grade=g, category=cat, role=m["prov"].loc[cat, "role"],
                             dEUR=float(tot["transacted"][cat]), dEUR_post_conversion=float(pe["transacted"][cat]),
                             dEUR_as_allocated=float(tot["as_allocated"][cat]), dEUR_as_allocated_post_conversion=float(pe["as_allocated"][cat]),
                             owners_dEUR=float(TEN_OWNER[(conv, inst, base, g)]["transacted"][cat]),
                             owners_dEUR_as_allocated=float(TEN_OWNER[(conv, inst, base, g)]["as_allocated"][cat])))


TM = {}
for conv in CONVS:
    m = M[conv]
    tm = TM[conv] = F.fi_tenure_model(m, P_OWN_Q.values)
    s_q = m["units"].loc[Q, "shares"]
    # LVT: renters receive the dividend; owners carry the owner flows of the within-decile split
    for base in ["B2", "B1"]:
        fl = FL_MAIN[(conv, f"LVT_{base}", "bridge")]
        om, tau = fl["om"], fl["tau"]
        div = float(fl["acc"]["dividend"].iloc[0])
        recv_o = (om["recv_owner"]).groupby(KEY).sum() * tau / 12.0
        pay_o = (om["pay_owner"]).groupby(KEY).sum() * tau / 12.0
        p_sum = om["p_own"].groupby(KEY).sum()
        for g in ["post_mid", "wealth_mid"]:
            kind, sch, mu = GRADES[g]
            mpc = SCHED[sch].reindex(Q)
            mpc_pay = mpc if kind == "post" else fl["h"] + (1 - fl["h"]) * MPC_U[mu]
            dc_o = (mpc * recv_o.reindex(Q) - mpc_pay * pay_o.reindex(Q)) / (p_sum.reindex(Q) * s_q)
            dc_r = mpc * div
            ten_append(conv, "LVT", base, g, m, tm, dc_o.values, dc_r.values)
    # VAT: each tenure's VAT-able consumption on its own basket (renters pay no housing-company charges)
    av = ACC_V[conv]
    ch = m["lines"].loc["maintenance charges of housing companies", Q] * flags["maintenance charges of housing companies"]
    x_r = av["vatable"] - ch
    x_o = av["vatable"] - ch + ch / P_OWN_Q
    cv = float(av["Cbar_v"].iloc[0])
    for g in ["post_mid"]:
        mpc = SCHED["mid"].reindex(Q)
        dc_o = mpc * B.TAU * (cv - x_o)
        dc_r = mpc * B.TAU * (cv - x_r)
        ten_append(conv, "VAT", "", g, m, tm, dc_o.values, dc_r.values)
TEN = pd.DataFrame(ten_rows)
wcsv(TEN, "fi_lvt_tenure_aware.csv")
# how much of owners' change the Working-model allocation books on lines nothing is transacted on
Co_, eo_ = TM["coherent"]["owner"]
own_ms = (Co_.loc[F.UNTRANSACTED] * eo_.loc[F.UNTRANSACTED]).sum() / Co_.sum()
mc_ = M["coherent"]
avg_ms = (mc_["C"].loc[F.UNTRANSACTED] * mc_["eta"].loc[F.UNTRANSACTED]).sum() / mc_["budget"]
ow = TEN_OWNER[("coherent", "LVT", "B2", "wealth_mid")]
rev("owner_marginal_share_untransacted_min", float(own_ms.min()), "share of an owner's marginal euro", "imputed rent + housing-loan interest, owner basket, by quintile")
rev("owner_marginal_share_untransacted_max", float(own_ms.max()), "share of an owner's marginal euro", "")
rev("quintile_marginal_share_untransacted_min", float(avg_ms.min()), "share of the marginal euro", "the post's quintile-average basket")
rev("quintile_marginal_share_untransacted_max", float(avg_ms.max()), "share of the marginal euro", "")
rev("owners_change_lvt_b2_bridge_wealth", float(ow["as_allocated"].sum()), "EUR per share per month", "owners' total change (the same under both allocations)")
rev("owners_change_on_untransacted_as_allocated", float(ow["as_allocated"].loc[F.UNTRANSACTED].sum()), "EUR per share per month", "LVT B2, bridge rate, wealth grade, coherent")
tw_ = TEN[(TEN["convention"] == "coherent") & (TEN["instrument"] == "LVT") & (TEN["base"] == "B2") & (TEN["grade"] == "wealth_mid")].set_index("category")
for col, lab in [("dEUR", "transacted"), ("dEUR_as_allocated", "as_allocated")]:
    rev(f"tenure_aware_charted_total_lvt_b2_wealth_{lab}", float(tw_.loc[mc_["chart"], col].sum()), "EUR per share per month", "the 37 charted bars")
print(f"\ntenure-aware owners: {100 * own_ms.min():.0f}-{100 * own_ms.max():.0f}% of an owner's marginal euro sits on imputed rent and loan interest "
      f"(quintile average {100 * avg_ms.min():.0f}-{100 * avg_ms.max():.0f}%); LVT B2 wealth grade: EUR {-ow['as_allocated'].loc[F.UNTRANSACTED].sum():.2f} of "
      f"owners' EUR {-ow['as_allocated'].sum():.2f} cut; re-spread over transacted lines, the charted total goes "
      f"{tw_.loc[mc_['chart'], 'dEUR_as_allocated'].sum():.2f} -> {tw_.loc[mc_['chart'], 'dEUR'].sum():.2f}")
tt = TEN[(TEN["convention"] == "coherent") & ((TEN["base"] == "B2") | (TEN["instrument"] == "VAT"))].pivot_table(
    index="category", columns=["instrument", "grade"], values="dEUR")
dn = SHF[(SHF["convention"] == "coherent") & ((SHF["base"] == "B2") | (SHF["instrument"] == "VAT")) & (SHF["rate"] == "bridge")
         & (SHF["grade"] == "post_mid")].pivot_table(index="category", columns="instrument", values="dEUR")
show = ["04.1 Actual rents", "04.2 Imputed rentals (off-chart)", "04.6 Interest on housing loans (off-chart)",
        "04.4 Water & misc. dwelling services", "04.3 Maintenance, repair and security of the dwelling", "01.1 Food (at home)",
        "07.1 Purchase of vehicles"]
print("\ntenure-aware baskets (coherent, bridge rate) beside the quintile-netted bars:\n" +
      pd.concat([dn.loc[show].add_prefix("netted_"), tt.loc[show]], axis=1).round(3).to_string())

# %% step 5: macro - two channels kept apart. (i) the price level; (ii) demand: flow, the VAT's levy, the LVT's stock
# (capitalization, collateral, non-occupiers, deferral), the loop
mc = M["coherent"]
step = {k: F.vat_price_step(mc, v)[0] for k, v in F.PASS_THROUGH.items()}
VSHARE = F.vat_price_step(mc, 1.0)[1]
step_post = {k: F.vat_price_step(M["post"], v)[0] for k, v in F.PASS_THROUGH.items()}
print(f"\nstep 5 (i), price level: VAT {100 * step['mid']:.2f}% [{100 * step['low']:.2f}, {100 * step['high']:.2f}] "
      f"(aggregate VAT-able share {VSHARE:.3f}; post convention {100 * step_post['mid']:.2f}%); LVT 0")

# (ii-a) the VAT's levy channel, impact version on the 2023 survey's balance sheets (deflated to 2022)
NW_MEUR = float(F.wv("net_wealth")["total"]) * HBS_AGG / 1e6 / DEFL23
LEVY = {k: v / (1.0 + v) for k, v in step.items()}
LEVY_T = pd.concat([F.vat_levy_impact(NW_MEUR, C_MEUR, LEVY["mid"]).assign(levy_case="mid")] +
                   [F.vat_levy_impact(NW_MEUR, C_MEUR, LEVY[k], lambdas=(0.35, 1.0)).assign(levy_case=k) for k in ("low", "high")])
LEVY_T["net_worth_meur"] = NW_MEUR
wcsv(LEVY_T, "fi_lvt_vat_levy.csv")
lv = LEVY_T[LEVY_T["levy_case"] == "mid"].pivot_table(index="lam", columns="mpw", values="pct_consumption")
print(f"   VAT levy channel (impact; net worth EUR {NW_MEUR / 1e3:,.0f}bn = {NW_MEUR / C_MEUR:.2f} years of HBS consumption, "
      f"{NW_MEUR / NA_C_MEUR:.2f} of NA; levy {100 * LEVY['mid']:.2f}%), % of consumption:\n" + lv.round(3).to_string())

# (ii-b) capitalization at announcement: land value lost and dwelling value lost, by design and rate
DESIGNS = ["immediate", "phasein_5y", "phasein_10y", "phasein_20y", "phasein_30y", "increment"]
PHIS = {"full_m1": F.PHI_FULL, "full_m2": F.PHI_FULL,
        "bridge_m1": float(PHI[(PHI["base"] == "B2") & (PHI["measure"] == "m1") & (PHI["yield_year"] == 2022) &
                               (PHI["convention"] == "coherent") & ~PHI["label"].str.contains("law")]["phi_bridge"].iloc[0]),
        "bridge_m2": float(PHI[(PHI["base"] == "B2") & (PHI["measure"] == "m2") & (PHI["yield_year"] == 2022) &
                               (PHI["convention"] == "coherent") & ~PHI["label"].str.contains("law")]["phi_bridge"].iloc[0])}
cap_rows = []
for rk, phi in PHIS.items():
    for d in DESIGNS:
        lf = F.loss_fraction(phi, d)
        cap_rows.append(dict(rate=rk, phi=phi, design=d, pv_share=F.pv_share(d), land_value_lost=lf,
                             dwelling_value_lost=F.dwelling_value_loss(phi, SH["s_d"], d),
                             land_loss_meur=lf * L_TOT["B2"], charge_beyond_land_rent=phi * F.pv_share(d) > 1.0))
CAP = pd.DataFrame(cap_rows)
wcsv(CAP, "fi_lvt_capitalization.csv")
print("\n(ii-b) capitalization, share of dwelling value lost at announcement:\n" +
      CAP.pivot_table(index="design", columns="rate", values="dwelling_value_lost").reindex(DESIGNS).round(3).to_string())

# (ii-c) collateral at decile level: mortgaged owners' loans against dwelling values (151u/151z), US-shape (central)
# and log-normal (band) within-decile LTVs. The clean concept is the crossers' lost BORROWING CAPACITY (a credit effect
# on top of the bill); their lost equity counts the bill twice (T4: the price fall is the capitalized bill) and is a
# band edge only, as in the US unit after its fix. Variants: only hand-to-mouth crossers respond; crossers respond to
# their lost equity instead of their bill (each crosser counted once).
POP = F.us_shape_population(MB)
HT_N = HTM_T["half_month"]["htm_share"]
H_MORT = (HTM["half_month"]["htm_share"] * HT_N["owner_with_mortgage"] / HT_N["all"]).clip(upper=1.0)   # judgment (151z ratio)
MPC_DEC = pd.Series(SCHED["mid"].reindex(KEY.values).values, index=DEC)       # the schedule's MPC of each decile's quintile
RATE_R = {"full_m1": R["m1"], "full_m2": R["m2"], "bridge_m1": R["m1"], "bridge_m2": R["m2"]}
SUMCOLS = ["lost_capacity_htm_meur", "lost_equity_htm_meur", "crossers_bill_meur", "crossers_bill_response_meur"]
coll_dec, coll_tot = [], []
for rk, phi in PHIS.items():
    for d in (DESIGNS if rk.startswith("full") else ["immediate"]):
        f = F.dwelling_value_loss(phi, SH["s_d"], d)
        cu = F.collateral_us_shape(f, POP, carry=CARRY)
        cu["rate"], cu["design"], cu["method"] = rk, d, "us_shape"
        hm = cu["decile"].map(H_MORT)
        cu["lost_capacity_htm_meur"] = cu["lost_capacity_meur"] * hm
        cu["lost_equity_htm_meur"] = cu["lost_equity_meur"] * hm
        if d == "immediate":                                  # the crossers' own bills (on their main-residence land)
            cu["crossers_bill_meur"] = phi * RATE_R[rk] * SH["s_d"] * cu["crossers_value_meur"]
            cu["crossers_bill_response_meur"] = cu["crossers_bill_meur"] * cu["decile"].map(MPC_DEC)
        else:
            cu["crossers_bill_meur"], cu["crossers_bill_response_meur"] = np.nan, np.nan
        for th in F.LTV_THRESHOLDS:
            dm, tm_ = (cu["threshold"] == th) & (cu["decile"] != "total"), (cu["threshold"] == th) & (cu["decile"] == "total")
            for c in SUMCOLS:
                cu.loc[tm_, c] = cu.loc[dm, c].sum(min_count=1)
        coll_dec.append(cu)
        for sk, sg in F.LTV_SIGMA.items():
            dln, tln = F.collateral_fi(f, sg, carry=CARRY)
            tln["rate"], tln["design"], tln["method"] = rk, d, f"lognormal_sigma_{sk}"
            coll_tot.append(tln)
COLL_DEC = pd.concat(coll_dec, ignore_index=True)
for k, v in F.MPC_COLL.items():
    COLL_DEC[f"dC_lost_capacity_{k}_pct"] = -100.0 * v * COLL_DEC["lost_capacity_meur"] / C_MEUR            # clean
    COLL_DEC[f"dC_lost_equity_{k}_pct"] = -100.0 * v * COLL_DEC["lost_equity_meur"] / C_MEUR                # T4 overlap
    COLL_DEC[f"dC_lost_capacity_htm_{k}_pct"] = -100.0 * v * COLL_DEC["lost_capacity_htm_meur"] / C_MEUR    # hand-to-mouth only
    COLL_DEC[f"dC_stock_instead_of_bill_{k}_pct"] = 100.0 * (COLL_DEC["crossers_bill_response_meur"] - v * COLL_DEC["lost_equity_meur"]) / C_MEUR
wcsv(COLL_DEC, "fi_lvt_collateral.csv")
COLL_LN = pd.concat(coll_tot, ignore_index=True)
for k, v in F.MPC_COLL.items():
    COLL_LN[f"dC_lost_capacity_{k}_pct"] = -100.0 * v * COLL_LN["lost_capacity_meur"] / C_MEUR
    COLL_LN[f"dC_lost_equity_{k}_pct"] = -100.0 * v * COLL_LN["lost_equity_meur"] / C_MEUR
wcsv(COLL_LN, "fi_lvt_collateral_lognormal_totals.csv")
ct = COLL_DEC[(COLL_DEC["method"] == "us_shape") & (COLL_DEC["decile"] == "total")]
print("\n(ii-c) collateral, mortgaged owners (US-shape LTVs inside each decile), totals:\n" +
      ct[["rate", "design", "threshold", "f", "ltv_before", "ltv_after", "n_cross", "above_before", "above_after", "lost_equity_meur",
          "lost_capacity_meur", "dC_lost_capacity_mid_pct", "dC_lost_equity_mid_pct", "dC_lost_capacity_htm_mid_pct"]].round(3).to_string(index=False))
cl = COLL_LN[(COLL_LN["threshold"] == 0.8) & (COLL_LN["design"] == "immediate")]
print("   log-normal band (80%, immediate):\n" + cl[["rate", "method", "n_cross", "lost_capacity_meur", "dC_lost_capacity_mid_pct"]].round(3).to_string(index=False))
# the crosser count is a borrowed shape: the SCF's within-decile LTV spread (US-shape) or a log-normal one
clf = cl[cl["rate"] == "full_m1"].set_index("method")
rev("crossers_80_full_us_shape", float(ct[(ct["rate"] == "full_m1") & (ct["design"] == "immediate") & (ct["threshold"] == 0.8)]["n_cross"].iloc[0]),
    "mortgaged owners", "SCF 2025 within-decile LTV shape rescaled to each Finnish decile")
for k in F.LTV_SIGMA:
    rev(f"crossers_80_full_lognormal_sigma_{k}", float(clf.loc[f"lognormal_sigma_{k}", "n_cross"]), "mortgaged owners", f"log-normal LTVs, sigma {F.LTV_SIGMA[k]}")
# who responds: the hand-to-mouth crossers' part of the lost borrowing capacity (the rest belongs to owners with more than
# half a month's income in deposits, who need not borrow at impact)
ct80 = ct[(ct["rate"] == "full_m1") & (ct["design"] == "immediate") & (ct["threshold"] == 0.8)].iloc[0]
rev("htm_share_of_crossers_lost_capacity", float(ct80["lost_capacity_htm_meur"] / ct80["lost_capacity_meur"]), "share",
    "full capture, US-shape: decile hand-to-mouth shares scaled by 151z's mortgaged-owner ratio")
cd = COLL_DEC[(COLL_DEC["method"] == "us_shape") & (COLL_DEC["rate"] == "full_m1") & (COLL_DEC["design"] == "immediate") &
              (COLL_DEC["threshold"] == 0.8) & (COLL_DEC["decile"] != "total")]
print("   by decile (full capture, 80%):\n" + cd.set_index("decile")[["n_mortgaged", "ltv_before", "ltv_after", "n_cross", "lost_capacity_meur",
                                                                      "lost_equity_meur"]].round(2).T.to_string())

# method check: the log-normal decile method on US decile aggregates against the SCF microdata (the US unit's own
# crossers), and the US-shape population's loan/value quartiles against Finland's published 151z quartiles
uin = F.us_out("us_lvt_inputs.csv").set_index("item")["value"]
uphi = F.us_out("us_lvt_phi.csv")
s_us = float(uin["s_uniform_2025"])
chk_rows = []
for lab, phi in [("US bridge L1 m1", float(uphi[(uphi["base"] == "L1") & (uphi["measure"] == "m1_z1hh_x_gs10") & (uphi["rate"] == "bridge")]["phi"].iloc[0])),
                 ("US full L1", F.PHI_FULL), ("US increment-only, bridge L1", float(uphi[(uphi["base"] == "L1") & (uphi["measure"] == "m1_z1hh_x_gs10") &
                                                                                       (uphi["rate"] == "bridge")]["phi"].iloc[0]) * F.GAMMA / F.DELTA)]:
    f = phi * s_us
    for th in F.LTV_THRESHOLDS:
        for sk, sg in F.LTV_SIGMA.items():
            mi, pa = F.us_collateral_check(f, th, sg)
            chk_rows.append(dict(check="lognormal on US decile aggregates vs SCF microdata", case=lab, f=f, threshold=th, sigma=sg,
                                 micro_n_cross_m=mi["n_cross_m"], param_n_cross_m=pa["n_cross_m"], micro_lost_equity_bn=mi["lost_equity_bn"],
                                 param_lost_equity_bn=pa["lost_equity_bn"], micro_lost_capacity_bn=mi["lost_capacity_bn"],
                                 param_lost_capacity_bn=pa["lost_capacity_bn"]))
CHK = pd.DataFrame(chk_rows)
for v in ["n_cross_m", "lost_equity_bn", "lost_capacity_bn"]:
    CHK[f"param_over_micro_{v}"] = CHK[f"param_{v}"] / CHK[f"micro_{v}"]
qs = dict(loans=(F.weighted_quantiles(POP["M_fi"], POP["w_fi"]), [F.wv("housing_loans", k, "tenure")["owner_with_mortgage"] for k in ("p25", "median", "p75")]),
          values=(F.weighted_quantiles(POP["V_fi"], POP["w_fi"]), [F.wv("main_residence", k, "tenure")["owner_with_mortgage"] for k in ("p25", "median", "p75")]))
for k, (mine, pub) in qs.items():
    for qn, a, b in zip(["p25", "median", "p75"], mine, pub):
        CHK.loc[len(CHK)] = dict(check=f"US-shape population vs 151z mortgaged owners: {k} {qn}", case="Finland", micro_n_cross_m=b, param_n_cross_m=a,
                                 param_over_micro_n_cross_m=a / b)
wcsv(CHK, "fi_lvt_collateral_method_check.csv")
cm = CHK[(CHK["sigma"] == F.LTV_SIGMA["mid"]) & (CHK["threshold"] == 0.8)]
print("\ncollateral method check (log-normal sigma 0.6 on US aggregates / SCF microdata), 80%:\n" +
      cm[["case", "param_over_micro_n_cross_m", "param_over_micro_lost_equity_bn", "param_over_micro_lost_capacity_bn"]].round(3).to_string(index=False))
print("   US-shape quartiles vs 151z (mine / published):\n" + CHK[CHK["case"] == "Finland"][["check", "param_n_cross_m", "micro_n_cross_m"]].round(0).to_string(index=False))

# (ii-d) non-occupying holders: the flow (bill x MPC, already in the impulse) or a wealth effect on the capitalized
# loss (2-5 cents per euro per year), never both; the deferral's residual wealth effect beside it
CAPS = {"L_ore": 1.0 / SH["s_d"], "L_ftr": 1.0 / SH["s_d"], "L_ffb": 1.0 / SH["s_f"]}   # loss capped at the item's whole value
no_rows = []
for conv in ["coherent"]:
    m = M[conv]
    for base in ["B2", "B1"]:
        for rate in RATES:
            fl = FL_MAIN[(conv, f"LVT_{base}", rate)]
            tau = fl["tau"]
            phi = tau / R["m1"] if rate != "full_m2" else F.PHI_FULL
            if rate == "full_m1":
                phi = F.PHI_FULL
            bill_no = to_q(LD[F.NONOCC_COLS[base]].sum(axis=1), conv, tau)                # euros per share per month
            loss = sum(to_q(LD[c] * min(phi, CAPS[c]), conv, 1.0) for c in F.NONOCC_COLS[base])   # capitalized loss per share / 12
            base_imp = float(IMP[(IMP["convention"] == conv) & (IMP["instrument"] == "LVT") & (IMP["base"] == base) & (IMP["rate"] == rate) &
                                 (IMP["defer"] == "none") & (IMP["grade"] == "post_mid")]["flow_eur"].iloc[0])
            add_back = float((m["w"] * SCHED["mid"].values * bill_no).sum())
            r = dict(convention=conv, base=base, rate=rate, phi=phi, flow_version_pct=100 * base_imp / m["budget_bar"],
                     nonocc_bill_meur=float((m["w"] * bill_no).sum()) * SHARES_TOT * 12 / 1e6,
                     nonocc_capitalized_loss_meur=float((m["w"] * loss).sum()) * SHARES_TOT * 12 / 1e6,
                     nonocc_share_of_base=float((LD[F.NONOCC_COLS[base]].sum(axis=1) * LD["households"]).sum() / (LD[base] * LD["households"]).sum()))
            for k, v in F.MPW.items():
                we = float((m["w"] * v * loss).sum())
                r[f"wealth_version_{k}_pct"] = 100 * (base_imp + add_back - we) / m["budget_bar"]
            r["loss_per_euro_of_bill"] = r["nonocc_capitalized_loss_meur"] / r["nonocc_bill_meur"]
            no_rows.append(r)
NO = pd.DataFrame(no_rows)
wcsv(NO, "fi_lvt_nonoccupier.csv")
print("\n(ii-d) non-occupiers, flow vs wealth-effect version of the impulse (% of consumption):\n" +
      NO[["base", "rate", "phi", "nonocc_share_of_base", "loss_per_euro_of_bill", "flow_version_pct", "wealth_version_low_pct",
          "wealth_version_mid_pct", "wealth_version_high_pct"]].round(3).to_string(index=False))

# deferral by outright owners: the deferred share, the impulse change, and their residual wealth effect
df_rows = []
for rate in RATES:
    fl = FL_MAIN[("coherent", "LVT_B2", rate)]
    phi = F.PHI_FULL if rate.startswith("full") else PHIS["bridge_m1"]
    lost = float((LD["L_main"] * K_OUT * min(phi, 1.0 / SH["s_d"]) * LD["households"]).sum()) / 1e6 * HBS_SCALE
    for g in ["post_mid", "wealth_mid"]:
        base_i = IMP[(IMP["convention"] == "coherent") & (IMP["base"] == "B2") & (IMP["rate"] == rate) & (IMP["grade"] == g)].set_index("defer")
        r = dict(rate=rate, grade=g, flow_none=float(base_i.loc["none", "flow_pct_consumption"]),
                 flow_defer_dividend_in_full=float(base_i.loc["outright_full", "flow_pct_consumption"]),
                 flow_defer_cash_balanced=float(base_i.loc["outright_cash", "flow_pct_consumption"]),
                 deferred_share_of_revenue=float(base_i.loc["outright_full", "deferred_share_of_revenue"]),
                 dividend=float(base_i.loc["none", "dividend"]), dividend_cash_balanced=float(base_i.loc["outright_cash", "dividend"]),
                 deferrers_capitalized_loss_meur=lost)
        for k, v in F.MPW.items():
            r[f"deferrers_residual_wealth_effect_{k}_pct"] = -100.0 * v * lost / C_MEUR
        df_rows.append(r)
DF = pd.DataFrame(df_rows)
wcsv(DF, "fi_lvt_deferral.csv")
print("\ndeferral by outright owners (B2, coherent):\n" + DF.round(3).to_string(index=False))

# (ii-e) the loop (T5): the dividend's rent bar raises land rent; a household-land tax takes back the household
# landlords' part; under the VAT the whole increment goes to landlords. The land share of a rent CHANGE is a judgment
# (central: the average land share s_d; band 0.13-0.30); 'one' puts land as the residual claimant on a permanent,
# demand-driven rent rise (ls = 1: structures are reproducible at cost, so the whole rise is land rent), reported
# beside the band, not inside it
ORP_Q = F.pair_quintiles(F.wv("other_residential_property").reindex(DEC) * LD["households"]) * 2.0
key_q = (ORP_Q / ORP_Q.sum()).values
lp_rows = []
mpc_mid = SCHED["mid"].values
for inst, rate in [("LVT_B2", "full_m1"), ("LVT_B2", "full_m2"), ("LVT_B2", "bridge"), ("VAT", "bridge")]:
    fl = FL_MAIN[("coherent", inst, rate)]
    R0 = F.rent_bar(mc, B.budget_shock(fl["net"], mpc_mid, mc["budget"]))
    for lk, ls in [("low", F.LS_RENT_BAND[0]), ("mid", SH["s_d"]), ("high", F.LS_RENT_BAND[1]), ("one", 1.0)]:
        for hk, hl in F.HH_LANDLORD_SHARE.items():
            if inst == "VAT":
                tot, leak, qq, rounds = 0.0, ls * R0, np.nan, None
                phi = 0.0
            else:
                phi = min(F.PHI_FULL, fl["tau"] / R["m1"]) if rate != "full_m2" else F.PHI_FULL
                tot, leak, qq, rounds = F.loop_closed_form(mc, R0, phi, ls, hl, key_q, mpc_mid)
            lp_rows.append(dict(instrument=inst, rate=rate, ls_case=lk, ls=ls, landlord_case=hk, h_landlord=hl, phi=phi, rent_bar_round0=R0,
                                land_rent_increment_round0=ls * R0, extra_dividend_total=tot, leak_to_landlords_total=leak,
                                extra_dividend_pct_of_dividend=100.0 * tot / float(fl["acc"]["dividend"].iloc[0]),
                                land_rent_increment_meur=ls * R0 * SHARES_TOT * 12 / 1e6,
                                capitalized_increment_meur=ls * R0 * SHARES_TOT * 12 / 1e6 / R["m1"], q=qq,
                                multiplier=1.0 / (1.0 - phi * hl * ls * qq) if inst != "VAT" else np.nan))
LOOP = pd.DataFrame(lp_rows)
wcsv(LOOP, "fi_lvt_loop.csv")
l1 = LOOP[(LOOP["instrument"] == "LVT_B2") & (LOOP["rate"] == "full_m1") & (LOOP["ls_case"] == "one") & (LOOP["landlord_case"] == "mid")].iloc[0]
v1 = LOOP[(LOOP["instrument"] == "VAT") & (LOOP["ls_case"] == "one") & (LOOP["landlord_case"] == "mid")].iloc[0]
rev("loop_ls1_multiplier", float(l1["multiplier"]), "ratio", "full capture, B2, household landlords 0.55, land share of a rent change 1")
rev("loop_ls1_extra_dividend_pct", float(l1["extra_dividend_pct_of_dividend"]), "% of the dividend", "same")
rev("vat_leak_to_landlords_ls1_meur", float(v1["land_rent_increment_meur"]), "EUR million a year", "the VAT dividend's rent bar, all of it land rent")
rev("vat_leak_to_landlords_ls1_capitalized_meur", float(v1["capitalized_increment_meur"]), "EUR million", "capitalized at the 2022 yield")
print("\n(ii-e) the loop (ls central = s_d, household landlords' share 0.55):\n" +
      LOOP[(LOOP["ls_case"] == "mid") & (LOOP["landlord_case"] == "mid")][["instrument", "rate", "rent_bar_round0", "land_rent_increment_round0",
                                                                           "extra_dividend_total", "extra_dividend_pct_of_dividend", "leak_to_landlords_total",
                                                                           "land_rent_increment_meur", "capitalized_increment_meur", "q", "multiplier"]].round(4).to_string(index=False))

# %% step 5 (iii): the macro channels side by side (the table behind the macro figure), the headline readings, and the
# post's published numbers
def imp_of(inst, rate, grade, base="B2", conv="coherent", defer="none"):
    x = IMP[(IMP["convention"] == conv) & (IMP["instrument"] == inst) & (IMP["rate"] == (rate if inst == "LVT" else "bridge")) &
            (IMP["grade"] == grade) & (IMP["defer"] == defer) & (IMP["base"] == (base if inst == "LVT" else ""))]
    assert len(x) == 1, (inst, rate, grade, base, conv, defer)
    return float(x["flow_pct_consumption"].iloc[0])


def coll_of(rate, design="immediate", th=0.8, col="dC_lost_capacity_mid_pct", method="us_shape"):
    x = COLL_DEC[(COLL_DEC["method"] == method) & (COLL_DEC["decile"] == "total") & (COLL_DEC["rate"] == rate) &
                 (COLL_DEC["design"] == design) & (COLL_DEC["threshold"] == th)]
    assert len(x) == 1, (rate, design, th, col)
    return float(x[col].iloc[0])


def lev_of(lam, mpw, case="mid"):
    x = LEVY_T[(LEVY_T["lam"] == lam) & (LEVY_T["mpw"] == mpw) & (LEVY_T["levy_case"] == case)]
    return float(x["pct_consumption"].iloc[0])


def nonocc_change(rate, base="B2", k="mid"):
    r = NO[(NO["base"] == base) & (NO["rate"] == rate)].iloc[0]
    return float(r[f"wealth_version_{k}_pct"] - r["flow_version_pct"])


mrow = []


def add(instr, channel, central, low, high, unit="% of consumption", note="", stress=np.nan):
    mrow.append(dict(instrument=instr, channel=channel, central=central, low=min(low, high), high=max(low, high), stress_10c=stress,
                     unit=unit, note=note))


add("VAT", "price level step (80-100% pass-through)", 100 * step["mid"], 100 * step["low"], 100 * step["high"], "% of consumer price level",
    f"15 points x aggregate VAT-able share {VSHARE:.3f} x pass-through")
add("LVT", "price level step", 0.0, 0.0, 0.0, "% of consumer price level", "land in fixed supply, rents set by demand: nothing to pass through")
add("VAT", "flow impulse, post's method (mid; band = high/low schedules)", imp_of("VAT", "", "post_mid"), imp_of("VAT", "", "post_high"),
    imp_of("VAT", "", "post_low"), note="rebuild: 0.422% (coherent), 0.438% (post)")
add("VAT", "flow impulse, payers graded by liquidity", imp_of("VAT", "", "liq_mid"), imp_of("VAT", "", "liq_mid"), imp_of("VAT", "", "liq_mid"),
    note="within-quintile VAT payers (log-normal spending, sigma 0.45), hand-to-mouth payers at 1.0")
add("VAT", "flow impulse, unconstrained payers draw on wealth", imp_of("VAT", "", "wealth_mid"), imp_of("VAT", "", "wealth_high"),
    imp_of("VAT", "", "wealth_low"), note="unconstrained payers at 0.56 (band 0.68 / 0.25)")
add("VAT", "levy channel, lambda = 0.35 (impact; 2-5c per EUR per year)", lev_of(0.35, "mid"), lev_of(0.35, "high"), lev_of(0.35, "low"),
    note=f"-mpw x 0.35 x {100 * LEVY['mid']:.1f}% x survey net worth (EUR {NW_MEUR / 1e3:,.0f}bn, 2022 euros)")
add("VAT", "levy channel, lambda = 1 (impact)", lev_of(1.0, "mid"), lev_of(1.0, "high"), lev_of(1.0, "low"), note="full A-K corner")
VAT_NET = (imp_of("VAT", "", "post_mid") + lev_of(0.35, "mid"), imp_of("VAT", "", "post_high") + lev_of(0.35, "high"),
           imp_of("VAT", "", "post_low") + lev_of(0.35, "low"))
add("VAT", "net demand at impact, lambda = 0.35 (flow + levy)", *VAT_NET, note="this unit's impact version")
add("VAT", "post, published: flow-only path (year 3; band)", 0.419, 0.293, 0.509, note="Fig 10 read-offs P803, P806-P807")
add("VAT", "post, published: central lambda = 0.35 (year 3; band)", 0.04, -0.17, 0.29, note="P878-P880")
add("VAT", "post, published: full A-K lambda = 1 (year 3; band)", -0.65, -0.99, -0.09, note="P881-P883")
for rate, lab in [("full_m1", "full capture, 2022 yield"), ("full_m2", "full capture, yield + 1.5"), ("bridge", "notional bridge rate")]:
    add("LVT", f"flow impulse, post's method ({lab}, B2)", imp_of("LVT", rate, "post_mid"), imp_of("LVT", rate, "post_high"),
        imp_of("LVT", rate, "post_low"), note="band = high/low schedules")
add("LVT", "flow impulse, payers graded by liquidity (full capture, B2)", imp_of("LVT", "full_m1", "liq_mid"), imp_of("LVT", "full_m1", "liq_mid"),
    imp_of("LVT", "full_m1", "liq_mid"), note="owners' hand-to-mouth shares (151u/151z)")
add("LVT", "flow impulse, unconstrained payers draw on wealth (full capture, B2)", imp_of("LVT", "full_m1", "wealth_mid"),
    imp_of("LVT", "full_m1", "wealth_high"), imp_of("LVT", "full_m1", "wealth_low"), note="the verifier's variant: 0.56 (band 0.68 / 0.25)")
add("LVT", "collateral: credit effect on all crossers' lost borrowing capacity (full capture, immediate)", coll_of("full_m1"),
    coll_of("full_m1", col="dC_lost_capacity_lit_high_pct"), coll_of("full_m1", col="dC_lost_capacity_low_pct"),
    note="the clean concept: 4.7c / 6c / 7c (stress 10c); US-shape LTVs inside deciles", stress=coll_of("full_m1", col="dC_lost_capacity_stress_pct"))
add("LVT", "collateral: credit effect, hand-to-mouth crossers only (full capture, immediate)", coll_of("full_m1", col="dC_lost_capacity_htm_mid_pct"),
    coll_of("full_m1", col="dC_lost_capacity_htm_lit_high_pct"), coll_of("full_m1", col="dC_lost_capacity_htm_low_pct"),
    note="deposits at most half a month's income (decile shares, mortgaged-owner ratio from 151z)", stress=coll_of("full_m1", col="dC_lost_capacity_htm_stress_pct"))
add("LVT", "collateral on all crossers' lost equity: includes the T4 overlap (full capture, immediate)", coll_of("full_m1", col="dC_lost_equity_mid_pct"),
    coll_of("full_m1", col="dC_lost_equity_lit_high_pct"), coll_of("full_m1", col="dC_lost_equity_low_pct"),
    note="counts the bill twice (the price fall is the capitalized bill): band edge only", stress=coll_of("full_m1", col="dC_lost_equity_stress_pct"))
lnb = COLL_LN[(COLL_LN["rate"] == "full_m1") & (COLL_LN["design"] == "immediate") & (COLL_LN["threshold"] == 0.8)]
add("LVT", "collateral: credit effect, log-normal LTVs (sigma 0.5-0.8; full capture)",
    float(lnb[lnb["method"] == "lognormal_sigma_mid"]["dC_lost_capacity_mid_pct"].iloc[0]), float(lnb["dC_lost_capacity_mid_pct"].min()),
    float(lnb["dC_lost_capacity_mid_pct"].max()), note="the second method, 6 cents")
add("LVT", "collateral: credit effect under a 10-year phase-in (full capture)", coll_of("full_m1", "phasein_10y"),
    coll_of("full_m1", "phasein_10y", col="dC_lost_capacity_lit_high_pct"), coll_of("full_m1", "phasein_10y", col="dC_lost_capacity_low_pct"))
add("LVT", "collateral: credit effect under increment-only grandfathering (full capture)", coll_of("full_m1", "increment"),
    coll_of("full_m1", "increment", col="dC_lost_capacity_lit_high_pct"), coll_of("full_m1", "increment", col="dC_lost_capacity_low_pct"),
    note="launch revenue then near zero (only rent increments are taxed)")
add("LVT", "non-occupying holders: wealth effect instead of flow (change in impulse, full capture, B2)", nonocc_change("full_m1"),
    nonocc_change("full_m1", k="high"), nonocc_change("full_m1", k="low"),
    note=f"cottages, other dwellings, forest and farmland: 2-5c on the capitalized loss ({float(NO[(NO['base'] == 'B2') & (NO['rate'] == 'full_m1')]['loss_per_euro_of_bill'].iloc[0]):.0f} EUR per EUR of bill)")
dfb = DF[(DF["rate"] == "full_m1") & (DF["grade"] == "post_mid")].iloc[0]
add("LVT", "deferral by outright owners, dividend paid in full (state lends the liens)", float(dfb["flow_defer_dividend_in_full"] - dfb["flow_none"]),
    float(dfb["flow_defer_dividend_in_full"] - dfb["flow_none"]), float(dfb["flow_defer_dividend_in_full"] - dfb["flow_none"]),
    note=f"change in impulse; deferred = {100 * dfb['deferred_share_of_revenue']:.0f}% of revenue")
add("LVT", "deferral by outright owners, cash-balanced dividend", float(dfb["flow_defer_cash_balanced"] - dfb["flow_none"]),
    float(dfb["flow_defer_cash_balanced"] - dfb["flow_none"]), float(dfb["flow_defer_cash_balanced"] - dfb["flow_none"]), note="change in impulse")
add("LVT", "deferral by outright owners: their residual wealth effect (if any)", float(dfb["deferrers_residual_wealth_effect_mid_pct"]),
    float(dfb["deferrers_residual_wealth_effect_high_pct"]), 0.0, note="0 to 5 cents per EUR of capitalized loss; never added to the flow")
lp = LOOP[(LOOP["instrument"] == "LVT_B2") & (LOOP["rate"] == "full_m1") & (LOOP["ls_case"] != "one")]
add("LVT", "the loop: extra dividend (full capture, B2)", float(lp[(lp["ls_case"] == "mid") & (lp["landlord_case"] == "mid")]["extra_dividend_pct_of_dividend"].iloc[0]),
    float(lp["extra_dividend_pct_of_dividend"].min()), float(lp["extra_dividend_pct_of_dividend"].max()), unit="% of the dividend",
    note="land share of a rent change 0.13-0.30, household landlords' share 0.40-0.70")


def readings(rate, base="B2"):
    """The headline readings at impact for one LVT rate, mirroring the US unit's us_lvt_headline.csv:
    (central, low, high, stress_10c) in % of consumption."""
    fm, fh, fl_ = imp_of("LVT", rate, "post_mid", base), imp_of("LVT", rate, "post_high", base), imp_of("LVT", rate, "post_low", base)
    crk = "full_m1" if rate in ("full_m1",) else ("full_m2" if rate == "full_m2" else "bridge_m1")
    c = lambda col: coll_of(crk, col=col)
    out = {
        "flow": (fm, fh, fl_, np.nan, "flow impulse only (post's method)"),
        "clean": (fm + c("dC_lost_capacity_mid_pct"), fh + c("dC_lost_capacity_lit_high_pct"), fl_ + c("dC_lost_capacity_low_pct"),
                  fh + c("dC_lost_capacity_stress_pct"), "flow + credit effect on all crossers' lost borrowing capacity (each crosser counted once)"),
        "t4": (fm + c("dC_lost_equity_mid_pct"), fh + c("dC_lost_equity_lit_high_pct"), fl_ + c("dC_lost_equity_low_pct"),
               fh + c("dC_lost_equity_stress_pct"), "flow + collateral on all crossers' lost equity: includes the T4 overlap (band edge only)"),
        "htm": (fm + c("dC_lost_capacity_htm_mid_pct"), fh + c("dC_lost_capacity_htm_lit_high_pct"), fl_ + c("dC_lost_capacity_htm_low_pct"),
                fh + c("dC_lost_capacity_htm_stress_pct"), "flow + credit effect on hand-to-mouth crossers' lost borrowing capacity"),
        "stock": (fm + c("dC_stock_instead_of_bill_mid_pct"), fh + c("dC_stock_instead_of_bill_lit_high_pct"), fl_ + c("dC_stock_instead_of_bill_low_pct"),
                  np.nan, "crossers' stock response (lost equity) instead of their bill response (each crosser counted once)"),
        "wealth_grade": (imp_of("LVT", rate, "wealth_mid", base) + c("dC_lost_capacity_mid_pct"),
                         imp_of("LVT", rate, "wealth_high", base) + c("dC_lost_capacity_lit_high_pct"),
                         imp_of("LVT", rate, "wealth_low", base) + c("dC_lost_capacity_low_pct"), np.nan,
                         "clean, with unconstrained payers drawing on wealth (MPC 0.56; 0.68 / 0.25)"),
    }
    if rate in ("full_m1", "full_m2", "bridge") and base == "B2":
        nr = "full_m1" if rate == "full_m1" else ("full_m2" if rate == "full_m2" else "bridge")
        out["nonocc_wealth"] = (out["clean"][0] + nonocc_change(nr, base, "mid"), out["clean"][1] + nonocc_change(nr, base, "high"),
                                out["clean"][2] + nonocc_change(nr, base, "low"), np.nan,
                                "clean, with every non-occupier's land on the wealth reading (3.5c; 5c / 2c)")
    return out


hl_rows = []
for rate in ["full_m1", "full_m2", "bridge"]:
    for k, (cen, lo, hi, st, lab) in readings(rate).items():
        hl_rows.append(dict(instrument="LVT", base="B2", rate=rate, reading=k, label=lab, central=cen, low=min(lo, hi), high=max(lo, hi), stress_10c=st))
hl_rows.append(dict(instrument="VAT", base="", rate="bridge", reading="net", label="flow + levy at lambda = 0.35 (2-5c)", central=VAT_NET[0],
                    low=min(VAT_NET[1:]), high=max(VAT_NET[1:]), stress_10c=np.nan))
hl_rows.append(dict(instrument="VAT", base="", rate="bridge", reading="flow", label="flow impulse only (post's method)", central=imp_of("VAT", "", "post_mid"),
                    low=imp_of("VAT", "", "post_high"), high=imp_of("VAT", "", "post_low"), stress_10c=np.nan))
HL = pd.DataFrame(hl_rows)
wcsv(HL, "fi_lvt_headline.csv")
for rate, lab in [("full_m1", "full capture, 2022 yield"), ("full_m2", "full capture, yield + 1.5")]:
    h = HL[(HL["rate"] == rate) & (HL["instrument"] == "LVT")].set_index("reading")
    add("LVT", f"net demand at impact: flow + credit effect ({lab})", float(h.loc["clean", "central"]), float(h.loc["clean", "low"]),
        float(h.loc["clean", "high"]), note="each crosser counted once; low: high schedule + 7c; high: low schedule + 4.7c; stress: high schedule + 10c",
        stress=float(h.loc["clean", "stress_10c"]))
h = HL[(HL["rate"] == "full_m1") & (HL["instrument"] == "LVT")].set_index("reading")
for k, lab in [("t4", "net demand at impact, includes the T4 overlap (full capture)"), ("htm", "net demand at impact, only hand-to-mouth crossers respond (full capture)"),
               ("stock", "net demand at impact, crossers' stock response instead of their bill (full capture)"),
               ("nonocc_wealth", "net demand at impact, every non-occupier on the wealth reading (full capture)"),
               ("wealth_grade", "net demand at impact, unconstrained payers draw on wealth (full capture)")]:
    add("LVT", lab, float(h.loc[k, "central"]), float(h.loc[k, "low"]), float(h.loc[k, "high"]), stress=float(h.loc[k, "stress_10c"]))
hb = HL[(HL["rate"] == "bridge") & (HL["instrument"] == "LVT")].set_index("reading")
add("LVT", "notional bridge rate: flow + credit effect when dwellings lose their whole value (phi 5.2)", float(hb.loc["clean", "central"]),
    float(hb.loc["clean", "low"]), float(hb.loc["clean", "high"]), note="not a land tax: the charge is 5.2 times the land rent; sizes the infeasibility",
    stress=float(hb.loc["clean", "stress_10c"]))


# %% step 5 (iv): full capture at each year's yield. The flow and the non-occupiers' bills scale with r; the
# capitalized losses and the collateral (dwelling values fall phi x s_d whatever r is) do not. So the yield year
# decides how large a capitalized loss is per euro of bill (1/r): 59 at the 2022 yield, 33-35 at the 2023-25 yields
def nonocc_change_tau(tau, phi, base="B2", k="mid", conv="coherent"):
    """Change in impulse (% of consumption) when non-occupiers respond to their capitalized loss (k cents per euro a
    year) instead of their bill (tau x land at the quintile MPC, already in the flow), as nonocc_change() at any tau."""
    m = M[conv]
    bill_no = to_q(LD[F.NONOCC_COLS[base]].sum(axis=1), conv, tau)
    loss = sum(to_q(LD[c] * min(phi, CAPS[c]), conv, 1.0) for c in F.NONOCC_COLS[base])
    add_back = float((m["w"] * SCHED["mid"].values * bill_no).sum())
    return 100.0 * (add_back - float((m["w"] * F.MPW[k] * loss).sum())) / m["budget_bar"], float((m["w"] * loss).sum() / (m["w"] * bill_no).sum())


def readings_at_yield(r, base="B2", conv="coherent"):
    """The full-capture readings at impact (central, low, high, stress_10c) at yield r, plus the funding numbers:
    the flow (post's method), the clean reading, the T4 overlap, hand-to-mouth crossers only, non-occupiers on the
    wealth reading, unconstrained payers on wealth. Collateral columns are the full_m1 rows (independent of r)."""
    m = M[conv]
    tau = F.PHI_FULL * r
    acc = F.lvt_accounting(m, LQ[base], tau)
    fp = lambda dC: B.impulse(m, shock=F.shock_of(m, dC))["flow_pct_consumption"]
    f = {s: fp(SCHED[s].values * acc["net"].values) for s in ("mid", "high", "low")}
    flw = lvt_flows(conv, base, "full_m1", tau=tau)
    fw = {k: fp(F.graded_dC(flw["net"].values, flw["recv"].values, flw["pay"].values, SCHED["mid"].values, flw["h"].values, "wealth", MPC_U[k]))
          for k in ("mid", "high", "low")}
    c = lambda col: coll_of("full_m1", col=col)
    no = {k: nonocc_change_tau(tau, F.PHI_FULL, base, k, conv) for k in F.MPW}
    out = {"flow": (f["mid"], f["high"], f["low"], np.nan),
           "clean": (f["mid"] + c("dC_lost_capacity_mid_pct"), f["high"] + c("dC_lost_capacity_lit_high_pct"), f["low"] + c("dC_lost_capacity_low_pct"),
                     f["high"] + c("dC_lost_capacity_stress_pct")),
           "t4": (f["mid"] + c("dC_lost_equity_mid_pct"), f["high"] + c("dC_lost_equity_lit_high_pct"), f["low"] + c("dC_lost_equity_low_pct"),
                  f["high"] + c("dC_lost_equity_stress_pct")),
           "htm": (f["mid"] + c("dC_lost_capacity_htm_mid_pct"), f["high"] + c("dC_lost_capacity_htm_lit_high_pct"),
                   f["low"] + c("dC_lost_capacity_htm_low_pct"), f["high"] + c("dC_lost_capacity_htm_stress_pct")),
           "wealth_grade": (fw["mid"] + c("dC_lost_capacity_mid_pct"), fw["high"] + c("dC_lost_capacity_lit_high_pct"),
                            fw["low"] + c("dC_lost_capacity_low_pct"), np.nan),
           "nonocc_change": (no["mid"][0], no["high"][0], no["low"][0], np.nan)}
    out["nonocc_wealth"] = (out["clean"][0] + no["mid"][0], out["clean"][1] + no["high"][0], out["clean"][2] + no["low"][0], np.nan)
    div = F.PHI_FULL * r * F.mean_land_ps(m, LQ[base]) / 12.0
    return out, dict(r=r, tau=tau, dividend_full=div, share_of_vat_dividend=div / DIV_V[conv], loss_per_euro_of_nonocc_bill=no["mid"][1])


YY_LABEL = {"wealth_grade": "clean, with unconstrained payers drawing on wealth (MPC 0.56; 0.68 / 0.25)",
            "nonocc_change": "non-occupiers on the wealth reading instead of the flow: change in impulse (3.5c; 5c / 2c)"}
yy_rows = []
for lab, r in [("2022", Y22), ("2022-12", Y22_DEC)] + [(str(y), F.yield_of(y, ylds=YLD)) for y in YEARS[1:]]:
    rd, fu = readings_at_yield(r)
    for k, (cen, lo, hi, st) in rd.items():
        yy_rows.append(dict(yield_label=lab, reading=k, label=YY_LABEL.get(k, HL[(HL["rate"] == "full_m1") & (HL["reading"] == k)]["label"].iloc[0]
                                                               if k in set(HL["reading"]) else k),
                            central=cen, low=min(lo, hi), high=max(lo, hi), stress_10c=st, **fu))
YY = pd.DataFrame(yy_rows)
wcsv(YY, "fi_lvt_yield_years.csv")
yv = lambda lab, k, col="central": float(YY[(YY["yield_label"] == lab) & (YY["reading"] == k)][col].iloc[0])
assert abs(yv("2022", "clean") - float(HL[(HL["rate"] == "full_m1") & (HL["reading"] == "clean")]["central"].iloc[0])) < 1e-12
assert abs(yv("2022", "nonocc_wealth") - float(HL[(HL["rate"] == "full_m1") & (HL["reading"] == "nonocc_wealth")]["central"].iloc[0])) < 1e-12
print("\nstep 5 (iv), full capture at each year's yield (% of consumption, central):\n" +
      YY.pivot_table(index="reading", columns="yield_label", values="central").round(3).to_string() + "\n" +
      YY.drop_duplicates("yield_label").set_index("yield_label")[["r", "dividend_full", "share_of_vat_dividend", "loss_per_euro_of_nonocc_bill"]].round(4).to_string())
for y in YEARS[1:]:
    for k, lab in [("clean", "net demand at impact: flow + credit effect"), ("nonocc_wealth", "net demand at impact, every non-occupier on the wealth reading")]:
        add("LVT", f"{lab} (full capture, {y} yield)", yv(str(y), k), yv(str(y), k, "low"), yv(str(y), k, "high"),
            note=f"yield {100 * F.yield_of(y, ylds=YLD):.2f}%: the flow and the non-occupiers' bills scale with r, the capitalized losses do not",
            stress=yv(str(y), k, "stress_10c"))
MACRO = pd.DataFrame(mrow)
wcsv(MACRO, "fi_lvt_macro_channels.csv")
print("\nstep 5 (iii), macro channels:\n" + MACRO[["instrument", "channel", "central", "low", "high", "stress_10c", "unit"]].round(3).to_string(index=False))

# %% step 6: the US unit beside this one (read only): concentration, the two stock channels, and the gap. The US numbers
# are read from consumption/lvt/out at run time (the US unit was being revised for its T4-overlap fix while this unit
# ran; rerunning this script re-reads them), and the US collateral at Finland's revenue share is recomputed on the SCF
# microdata with the US unit's own crossing logic.
um = F.us_out("us_lvt_macro_channels.csv")
uc = F.us_out("us_lvt_collateral.csv")
uno = F.us_out("us_lvt_nonoccupier.csv").set_index(["scenario", "grade"])
uhl = F.us_out("us_lvt_headline.csv") if (OUT / "us_lvt_headline.csv").exists() else None


def us_ch(*parts, col="central"):
    """The US macro-channel row whose name contains every part (exactly one)."""
    x = um[np.logical_and.reduce([um["channel"].str.contains(p_, regex=False) for p_ in parts])]
    assert len(x) == 1, (parts, list(x["channel"]))
    return float(x[col].iloc[0])


def us_coll(scenario, col, th=0.8, design="immediate", measure="m1_z1hh_x_gs10"):
    x = uc[(uc["scenario"] == scenario) & (uc["design"] == design) & (uc["threshold"] == th) & (uc["measure"] == measure)]
    assert len(x) == 1, (scenario, col)
    return float(x[col].iloc[0])


US_C_BN = float(uin["ce_consumption_bn"])
US_RENT_L1 = float(uphi[(uphi["base"] == "L1") & (uphi["measure"] == "m1_z1hh_x_gs10") & (uphi["rate"] == "bridge")]["rent_bn"].iloc[0])
US_PHI_B = float(uphi[(uphi["base"] == "L1") & (uphi["measure"] == "m1_z1hh_x_gs10") & (uphi["rate"] == "bridge")]["phi"].iloc[0])
US_FLOW_B = us_ch("flow impulse, post's method (bridge, L1)")
US_FLOW_FULL = us_ch("flow impulse, post's method (full, L1)")
US_CR_B = us_coll("LVT_bridge_L1", "dC_lost_capacity_mid_pct")
US_LE_B = us_coll("LVT_bridge_L1", "dC_lost_equity_mid_pct")
US_CR_FULL = us_coll("LVT_full_L1", "dC_lost_capacity_mid_pct")
US_LE_FULL = us_coll("LVT_full_L1", "dC_lost_equity_mid_pct")
us_vat_net = us_ch("net demand at impact, lambda = 0.35 (flow + levy)")
us_vat_flow = us_ch("flow impulse, post's method (mid; band")
us_vat_levy = us_ch("levy channel, lambda = 0.35")
fi_rev_share = float(IMP[(IMP["convention"] == "coherent") & (IMP["instrument"] == "LVT") & (IMP["base"] == "B2") & (IMP["rate"] == "full_m1") &
                         (IMP["grade"] == "post_mid") & (IMP["defer"] == "none")]["dividend"].iloc[0]) * SHARES_TOT * 12 / 1e6 / C_MEUR
phi_us_match = fi_rev_share * US_C_BN / US_RENT_L1                       # US phi that raises Finland's full-capture revenue share
mi_match, _ = F.us_collateral_check(phi_us_match * s_us, 0.8, F.LTV_SIGMA["mid"])
us_cr_match = -100.0 * F.MPC_COLL["mid"] * mi_match["lost_capacity_bn"] / US_C_BN
us_le_match = -100.0 * F.MPC_COLL["mid"] * mi_match["lost_equity_bn"] / US_C_BN
us_flow_match = US_FLOW_B * phi_us_match / US_PHI_B
fi_flow_full = imp_of("LVT", "full_m1", "post_mid")
fi_cr_full, fi_le_full = coll_of("full_m1"), coll_of("full_m1", col="dC_lost_equity_mid_pct")
f_fi_usphi = US_PHI_B * SH["s_d"]                                        # Finland at the US bridge's share of rent
cu_usphi = F.collateral_us_shape(f_fi_usphi, POP, carry=CARRY)
cu_usphi_t = cu_usphi[(cu_usphi["decile"] == "total") & (cu_usphi["threshold"] == 0.8)].iloc[0]
fi_cr_usphi = -100 * F.MPC_COLL["mid"] * float(cu_usphi_t["lost_capacity_meur"]) / C_MEUR
fi_le_usphi = -100 * F.MPC_COLL["mid"] * float(cu_usphi_t["lost_equity_meur"]) / C_MEUR
fi_flow_usphi = fi_flow_full * US_PHI_B / F.PHI_FULL
fi_vat_net = VAT_NET[0]
us_nonocc_full = float(uno.loc[("LVT_full_L1_m1", "dn_mid"), "wealth_version_mid_pct"] - uno.loc[("LVT_full_L1_m1", "dn_mid"), "flow_version_pct"])
PHI_B2 = float(PHI[(PHI["base"] == "B2") & (PHI["measure"] == "m1") & (PHI["yield_year"] == 2022) & (PHI["convention"] == "coherent") &
                   ~PHI["label"].str.contains("law")]["phi_bridge"].iloc[0])
cmp_rows = [
    dict(block="concentration", item="top income decile's share of residential land", US=float(usl.loc["d10", "L1_share"]),
         FI=float(CONC[(CONC["country"] == "FI") & (CONC["item"] == "land B1")]["top_decile"].iloc[0]), note="SCF 2025 L1; 151u 2023 B1"),
    dict(block="concentration", item="top income decile's share of all household land", US=float(usl.loc["d10", "L2_share"]),
         FI=float(CONC[(CONC["country"] == "FI") & (CONC["item"] == "land B2")]["top_decile"].iloc[0]),
         note="definitions differ: US L2 adds noncorporate and corporate land; FI B2 adds forest, farmland and business land"),
    dict(block="concentration", item="top income decile's share of financial assets", US=float(usw.loc["FIN", "top_decile"]),
         FI=float(CONC[(CONC["country"] == "FI") & (CONC["item"] == "financial assets")]["top_decile"].iloc[0]), note=""),
    dict(block="concentration", item="top income decile's share of net wealth", US=float(usw.loc["NETWORTH", "top_decile"]),
         FI=float(CONC[(CONC["country"] == "FI") & (CONC["item"] == "net wealth")]["top_decile"].iloc[0]), note=""),
    dict(block="concentration", item="top income quintile's share of VAT-able consumption", US=float(usl.loc[["d09", "d10"], "vatable_share"].sum()),
         FI=float(CONC[(CONC["country"] == "FI") & (CONC["item"] == "VAT-able consumption (coherent)")]["top_quintile"].iloc[0]), note=""),
    dict(block="land", item="land share of residential value", US=s_us, FI=SH["s_d"], note="US: SCF-calibrated (Z.1 0.46); FI: the residual"),
    dict(block="land", item="household land / consumption (survey budget)", US=float(uin["L_hh"]) / US_C_BN, FI=N211_22 / C_MEUR,
         note="US Z.1 household residual / CE 2024; FI N211 S14 2022 / HBS 2022"),
    dict(block="land", item="rent-to-value r, measure m1", US=float(uphi["r"].iloc[0]), FI=Y22, note="US 10-year Treasury 2024; FI 10-year 2022"),
    dict(block="land", item="land rent / consumption at m1", US=US_RENT_L1 / US_C_BN, FI=Y22 * L_TOT["B2"] * HBS_SCALE / C_MEUR, note=""),
    dict(block="rates", item="phi needed for the bridge's dividend (m1)", US=US_PHI_B, FI=PHI_B2, note="FI above 1: infeasible as a land tax"),
    dict(block="rates", item="full-capture dividend / VAT dividend (m1)", US=float(uphi[(uphi["base"] == "L1") & (uphi["measure"] == "m1_z1hh_x_gs10") &
                                                                                     (uphi["rate"] == "full")]["dividend_vs_vat"].iloc[0]),
         FI=float(PHI[(PHI["base"] == "B2") & (PHI["measure"] == "m1") & (PHI["yield_year"] == 2022) & (PHI["convention"] == "coherent") &
                      ~PHI["label"].str.contains("law")]["share_of_vat_dividend"].iloc[0]), note=""),
    dict(block="VAT, impact (same formulas)", item="flow impulse (post's method)", US=us_vat_flow, FI=imp_of("VAT", "", "post_mid"), note="% of consumption"),
    dict(block="VAT, impact (same formulas)", item="levy channel, lambda 0.35, 3.5c", US=us_vat_levy, FI=lev_of(0.35, "mid"),
         note="same formula on each country's survey net worth"),
    dict(block="VAT, impact (same formulas)", item="net demand at impact (flow + levy)", US=us_vat_net, FI=fi_vat_net, note=""),
    dict(block="VAT, published", item="the post's central path (year 3)", US=-0.69, FI=0.04, note="P663; P878"),
    dict(block="VAT, published", item="the post's full A-K path (year 3)", US=-2.7, FI=-0.65, note="P666; P881"),
]
for blk, flows, crs, les, note in [
        ("LVT, same share of rent (full capture, phi 0.98)", (US_FLOW_FULL, fi_flow_full), (US_CR_FULL, fi_cr_full), (US_LE_FULL, fi_le_full),
         "US L1; FI B2 at the 2022 yield"),
        ("LVT, the US bridge's share of rent (phi 0.848)", (US_FLOW_B, fi_flow_usphi), (US_CR_B, fi_cr_usphi), (US_LE_B, fi_le_usphi),
         "FI flow scaled from full capture; FI collateral recomputed at f = 0.848 x s_d"),
        ("LVT, same revenue as Finland's full capture", (us_flow_match, fi_flow_full), (us_cr_match, fi_cr_full), (us_le_match, fi_le_full),
         f"revenue {100 * fi_rev_share:.2f}% of consumption; US phi {phi_us_match:.3f}, its collateral recomputed on SCF 2025 microdata")]:
    cmp_rows += [dict(block=blk, item="flow impulse", US=flows[0], FI=flows[1], note=note),
                 dict(block=blk, item="collateral: credit effect (6c x crossers' lost borrowing capacity)", US=crs[0], FI=crs[1], note="the clean concept"),
                 dict(block=blk, item="net demand at impact (flow + credit effect)", US=flows[0] + crs[0], FI=flows[1] + crs[1], note="the headline reading"),
                 dict(block=blk, item="net demand at impact, includes the T4 overlap (6c x lost equity)", US=flows[0] + les[0], FI=flows[1] + les[1],
                      note="band edge only")]
cmp_rows += [
    dict(block="LVT, same share of rent (full capture, phi 0.98)", item="non-occupiers on the wealth reading: change in impulse (3.5c)",
         US=us_nonocc_full, FI=nonocc_change("full_m1"), note="US: other residential land; FI: other dwellings, cottages, forest, farmland"),
    dict(block="LVT, same share of rent (full capture, phi 0.98)", item="net demand at impact, non-occupiers on the wealth reading (3.5c)",
         US=US_FLOW_FULL + US_CR_FULL + us_nonocc_full, FI=fi_flow_full + fi_cr_full + nonocc_change("full_m1"), note="clean reading plus the change above"),
    dict(block="LVT, same dividend as the VAT bridge", item="net demand at impact (flow + credit effect)", US=US_FLOW_B + US_CR_B,
         FI=float(hb.loc["clean", "central"]), note=f"FI: a charge {PHI_B2:.1f} times the land rent, dwellings worthless: not a land tax")]
# Both countries on the same year's yield (full capture). The rows above pair the US unit's 2024 Treasury yield (4.21%)
# with Finland's 2022 yield (1.69%), and a capitalized loss is 1/r times its bill (24 against 59). Here: Finland at its
# 2024 yield beside the US unit's own numbers, and the US at its 2022 yield (GS10 annual mean, the US unit's source)
# beside Finland's main numbers. The US rescaling is yield-only, as Finland's is: the flow and the non-occupiers' bill
# response scale with r; the credit effect, the lost equity and the capitalized losses do not.
ufl = uphi[(uphi["base"] == "L1") & (uphi["measure"] == "m1_z1hh_x_gs10") & (uphi["rate"] == "full")].iloc[0]
US_R = {y: F.us_gs10_annual(y) / 100.0 for y in (2022, 2024)}
assert abs(float(ufl["r"]) / US_R[2024] - 1.0) < 1e-9, "the US unit's m1 yield is GS10 2024 (stored at 10 significant digits)"
un_ = uno.loc[("LVT_full_L1_m1", "dn_mid")]
we_us = {k: 100.0 * v * float(un_["nonocc_capitalized_loss_bn"]) / US_C_BN for k, v in F.MPW.items()}
addb_us = float(un_["wealth_version_mid_pct"] - un_["flow_version_pct"]) + we_us["mid"]      # the bill response the wealth reading removes
for k in ("low", "high"):                                       # the decomposition reproduces the US unit's 2c and 5c rows
    assert abs(float(un_["flow_version_pct"]) + addb_us - we_us[k] - float(un_[f"wealth_version_{k}_pct"])) < 1e-9, k


def us_full_at(r):
    """The US unit's full-capture L1 readings (6c, 3.5c) put on yield r: flow and non-occupiers' bill response x r / r_2024."""
    k = r / US_R[2024]
    flow, chg = US_FLOW_FULL * k, addb_us * k - we_us["mid"]
    return dict(flow=flow, credit=US_CR_FULL, clean=flow + US_CR_FULL, t4=flow + US_LE_FULL, nonocc_change=chg, nonocc=flow + US_CR_FULL + chg,
                loss_per_bill=float(un_["nonocc_capitalized_loss_bn"]) / (float(un_["nonocc_bill_bn"]) * k))


def fi_full_at(lab):
    return dict(flow=yv(lab, "flow"), credit=fi_cr_full, clean=yv(lab, "clean"), t4=yv(lab, "t4"), nonocc_change=yv(lab, "nonocc_change"),
                nonocc=yv(lab, "nonocc_wealth"), loss_per_bill=float(YY[YY["yield_label"] == lab]["loss_per_euro_of_nonocc_bill"].iloc[0]))


SAME_YEAR = {}
for y in (2024, 2022):
    us_, fi_ = us_full_at(US_R[y]), fi_full_at(str(y))
    SAME_YEAR[y] = (us_, fi_)
    blk = f"LVT, full capture (phi 0.98), both at their {y} yields (US {100 * US_R[y]:.2f}%, FI {100 * F.yield_of(y, ylds=YLD):.2f}%)"
    nt = "US: the US unit's outputs" if y == 2024 else "US: the US unit's full-capture outputs put on the 2022 GS10 yield here (yield-only)"
    nt += "; FI: the unit's own readings" + ("" if y == 2022 else " at the 2024 yield (yield-only)")
    for key, item in [("flow", "flow impulse"), ("credit", "collateral: credit effect (6c x crossers' lost borrowing capacity)"),
                      ("clean", "net demand at impact (flow + credit effect)"), ("t4", "net demand at impact, includes the T4 overlap (6c x lost equity)"),
                      ("nonocc_change", "non-occupiers on the wealth reading: change in impulse (3.5c)"),
                      ("nonocc", "net demand at impact, non-occupiers on the wealth reading (3.5c)"),
                      ("loss_per_bill", "capitalized loss per unit of non-occupiers' bill (= 1/r)")]:
        cmp_rows.append(dict(block=blk, item=item, US=us_[key], FI=fi_[key], note=nt))
for y in YEARS[1:]:
    cmp_rows.append(dict(block="LVT, full capture (phi 0.98), Finland at each year's yield", item=f"net demand at impact, non-occupiers on the wealth reading (3.5c), FI {y} yield",
                         US=SAME_YEAR[2024][0]["nonocc"], FI=yv(str(y), "nonocc_wealth"), note="US: the US unit's 2024 reading"))
# the US bridge's share of rent (the US headline's scale) with Finland on the same year's (2024) yield
fi_flow_usphi24 = yv("2024", "flow") * US_PHI_B / F.PHI_FULL
blk = f"LVT, the US bridge's share of rent (phi {US_PHI_B:.3f}), both at their 2024 yields"
cmp_rows += [dict(block=blk, item="flow impulse", US=US_FLOW_B, FI=fi_flow_usphi24, note="FI flow scaled from full capture at the 2024 yield"),
             dict(block=blk, item="collateral: credit effect (6c x crossers' lost borrowing capacity)", US=US_CR_B, FI=fi_cr_usphi, note="independent of the yield"),
             dict(block=blk, item="net demand at impact (flow + credit effect)", US=US_FLOW_B + US_CR_B, FI=fi_flow_usphi24 + fi_cr_usphi,
                  note="the US unit's headline beside Finland at the same year's yield")]
us_share_cross = float(uc[(uc["scenario"] == "LVT_full_L1") & (uc["design"] == "immediate") & (uc["threshold"] == 0.8) &
                          (uc["measure"] == "m1_z1hh_x_gs10")]["share_of_mortgaged"].iloc[0])
fi_c80 = COLL_DEC[(COLL_DEC["method"] == "us_shape") & (COLL_DEC["rate"] == "full_m1") & (COLL_DEC["design"] == "immediate") &
                  (COLL_DEC["threshold"] == 0.8) & (COLL_DEC["decile"] == "total")].iloc[0]
cmp_rows += [dict(block="collateral at full capture", item="mortgaged owners crossing 80% LTV, share of the mortgaged", US=us_share_cross,
                  FI=float(fi_c80["n_cross"] / fi_c80["n_mortgaged"]), note="US: us_lvt_collateral.csv; FI: US-shape LTVs inside deciles"),
             dict(block="collateral at full capture", item="dwelling value lost at announcement (phi x land share)", US=F.PHI_FULL * s_us, FI=F.PHI_FULL * SH["s_d"], note="")]
rev("us_over_fi_land_per_consumption", (float(uin["L_hh"]) / US_C_BN) / (N211_22 / C_MEUR), "ratio", "household land / survey consumption, US (Z.1 2024 / CE 2024) over FI (N211 2022 / HBS 2022)")
rev("us_share_of_mortgaged_crossing_80_full", us_share_cross, "share", "US unit, full capture, L1")
rev("fi_share_of_mortgaged_crossing_80_full", float(fi_c80["n_cross"] / fi_c80["n_mortgaged"]), "share", "FI, full capture, US-shape")
rev("us_gs10_2022_pct", 100 * US_R[2022], "% a year", "pinning/cache/GS10.csv annual mean (the US unit's yield source)")
if uhl is not None:
    for _, r in uhl[(uhl["instrument"] == "LVT") & (uhl["base"] == "L1")].iterrows():
        cmp_rows.append(dict(block="US headline readings (us_lvt_headline.csv, bridge L1)", item=r["label"], US=float(r["central"]), FI=np.nan,
                             note=f"[{r['low']:.3f}, {r['high']:.3f}]"))
UC = pd.DataFrame(cmp_rows)
UC["US_minus_FI"] = UC["US"] - UC["FI"]
UC["us_files_read"] = ("us_lvt_macro_channels.csv, us_lvt_collateral.csv, us_lvt_nonoccupier.csv, us_lvt_phi.csv, us_lvt_inputs.csv, "
                       "us_lvt_land_by_decile.csv, us_lvt_headline.csv; pinning/cache/GS10.csv (the 2022 yield)")
wcsv(UC, "fi_lvt_us_compare.csv")
print("\nstep 6, the US beside Finland:\n" + UC[UC["FI"].notna()][["block", "item", "US", "FI", "US_minus_FI"]].round(4).to_string(index=False))

# %% step 7: robustness - land shares, carry, composition, convention, yield year, base, VAT law, liquidity, LTV method
def headline(label, sh=None, carry=None, conv="coherent", composition="12ew", year=2022, base="B2", vat_flags="adopted",
             htm_key="half_month", coll_method="us_shape", note="", r=None):
    sh = SH if sh is None else sh
    carry = CARRY if carry is None else carry
    m = M[conv] if composition == "12ew" else B.build_fi_model(convention=conv, composition=composition)
    av = B.fi_vat_accounting(m, flags=B.fi_vat_flags(vat_flags))
    div = float(av["dividend"].iloc[0])
    ld = F.land_by_decile(sh, carry)
    lq = F.pair_quintiles(ld[base])
    r = F.yield_of(year, ylds=YLD) if r is None else r
    mps = F.mean_land_ps(m, lq)
    tau_b = F.tau_for_dividend(m, lq, div)
    tau_f = F.PHI_FULL * r
    acc_b, acc_f = F.lvt_accounting(m, lq, tau_b), F.lvt_accounting(m, lq, tau_f)
    s_dec = pd.Series(m["units"].loc[Q, "shares"].values.repeat(2), index=DEC)
    om = F.owner_model(ld[base], s_dec, mps, P_OWN, SIG_OWN)
    conv12 = 12.0 * m["units"].loc[Q, "shares"]
    recv = F.pair_quintiles(om["recv_nonowner"] + om["recv_owner"]) * tau_f / conv12
    pay = F.pair_quintiles(om["pay_owner"]) * tau_f / conv12
    h = (HTM_OWN[htm_key] * om["pay_owner"]).groupby(KEY).sum() / om["pay_owner"].groupby(KEY).sum()
    mpc = SCHED["mid"].values
    fl = lambda dC: B.impulse(m, shock=F.shock_of(m, dC))["flow_pct_consumption"]
    flow_b = fl(mpc * acc_b["net"].values)
    flow_f = fl(mpc * acc_f["net"].values)
    flow_fw = fl(F.graded_dC(acc_f["net"].values, recv.values, pay.values, mpc, h.reindex(Q).values, "wealth", MPC_U["mid"]))
    flow_v = fl(mpc * av["net"].values)
    f = F.PHI_FULL * sh["s_d"]
    if coll_method == "us_shape":
        cu = F.collateral_us_shape(f, POP, carry=carry)
        tt = cu[(cu["decile"] == "total") & (cu["threshold"] == 0.8)].iloc[0]
        lc, le = float(tt["lost_capacity_meur"]), float(tt["lost_equity_meur"])
    else:
        _, tln = F.collateral_fi(f, F.LTV_SIGMA[coll_method], carry=carry)
        tt = tln[tln["threshold"] == 0.8].iloc[0]
        lc, le = float(tt["lost_capacity_meur"]), float(tt["lost_equity_meur"])
    coll = -100.0 * F.MPC_COLL["mid"] * lc / C_MEUR
    coll_t4 = -100.0 * F.MPC_COLL["mid"] * le / C_MEUR
    return dict(variant=label, s_d=sh["s_d"], s_f=sh["s_f"], carry=carry, convention=conv, composition=composition, yield_year=year,
                r=r, base=base, vat_dividend=div, phi_bridge=tau_b / r, tau_bridge_pct=100 * tau_b, dividend_full=F.PHI_FULL * r * mps / 12.0,
                share_of_vat_dividend=F.PHI_FULL * r * mps / 12.0 / div, net_q1_bridge=float(acc_b.loc["q1", "net"]),
                net_q5_bridge=float(acc_b.loc["q5", "net"]), net_q5_bridge_pct=float(acc_b.loc["q5", "net_pct_budget"]),
                vat_net_q5=float(av.loc["q5", "net"]), flow_vat=flow_v, flow_lvt_bridge=flow_b, flow_ratio_bridge=flow_b / flow_v,
                flow_lvt_full=flow_f, flow_lvt_full_wealth_grade=flow_fw, dwelling_value_fall_full=f, collateral_credit_full_6c=coll,
                net_full=flow_f + coll, collateral_t4_full_6c=coll_t4, net_full_t4=flow_f + coll_t4, note=note)


def sd_label(v):
    sh = F.land_shares("fix_sd", s_d=v)
    if sh["n211_held"]:
        return f"dwelling land share s_d = {v:.2f} (N211 held; s_f = {sh['s_f']:.2f})"
    return (f"dwelling land share s_d = {v:.2f} (s_f floored at 0: N211 can be held only up to s_d = {sh['s_d_max_n211_held']:.3f}; "
            f"land {100 * (sh['land_over_n211'] - 1):+.1f}% against N211)")


rb = [headline("main: residual land shares, end-2022 carry, coherent, 12ew, 2022 yield, B2")]
rb += [headline(sd_label(v), sh=F.land_shares("fix_sd", s_d=v), note="judgment band: the unit's own evidence (fi_lvt_land_evidence.csv)")
       for v in F.S_D_BAND]
rb += [headline(f"forest/farmland/business land share s_f = {v:.1f} (total departs from N211)", sh=F.land_shares("fixed", s_d=SH["s_d"], s_f=v),
                note="judgment band") for v in F.S_F_BAND]
rb += [headline("carry to mid-2022 (mean of end-2021 and end-2022 N211)", carry=F.carry_factor("mid2022"))]
rb += [headline("post convention (equal consumption units, published VAT side)", conv="post")]
rb += [headline("coherent, 14qa composition (the HBS's own quintiles)", composition="14qa")]
rb += [headline(f"yield year {y}", year=y) for y in (2023, 2024, 2025)]
rb += [headline("base B1: residential land only", base="B1")]
rb += [headline("VAT flags under Finnish law line by line (bridge target 178.0 coherent)", vat_flags="law")]
rb += [headline(f"hand-to-mouth threshold: {k}", htm_key=k) for k in ("half_biweekly", "one_month")]
rb += [headline(f"collateral: log-normal LTVs, sigma {F.LTV_SIGMA[k]}", coll_method=k) for k in ("low", "mid", "high")]
rb += [headline(f"yield: December 2022 alone ({100 * Y22_DEC:.2f}%; the month of the end-2022 land stock)", r=Y22_DEC,
                note="yield timing: the paper pairs annual means")]
ROB = pd.DataFrame(rb)
wcsv(ROB, "fi_lvt_robustness.csv")
print("\nstep 7, robustness:\n" + ROB[["variant", "phi_bridge", "share_of_vat_dividend", "net_q1_bridge", "net_q5_bridge", "flow_lvt_bridge",
                                       "flow_ratio_bridge", "flow_lvt_full", "flow_lvt_full_wealth_grade", "collateral_credit_full_6c", "net_full",
                                       "net_full_t4"]].round(3).to_string(index=False))

# VAT payers inside the quintiles (for the who-pays panel): share of households above the mean VAT-able spending
_, _, vat_pay_share = F.lognormal_split(ACC_V["coherent"]["vatable"].values, float(ACC_V["coherent"]["Cbar_v"].iloc[0]), F.SIGMA_C["mid"])
VAT_PAYERS_Q = pd.Series(vat_pay_share, index=Q)
wcsv(pd.DataFrame({"quintile": Q, "vat_payer_share_lognormal": vat_pay_share,
                   "lvt_payer_share_owner_model": F.pair_quintiles(wdm["payer_share_of_households"]).values}), "fi_lvt_payer_shares.csv")
REVIEW = pd.DataFrame(REV)
assert REVIEW["item"].is_unique
wcsv(REVIEW, "fi_lvt_review.csv")
print("\nthe review's numbers (out/fi_lvt_review.csv):\n" + REVIEW[["item", "value", "unit"]].to_string(index=False))

# %% figures (light mode, PNG at 200 dpi; the rebuild's and the US unit's chrome, the dataviz reference palette in
# fixed slot order, validated with the skill's validator: VAT = blue, LVT on all household land (B2) = orange, LVT on
# residential land (B1) or the tenure-aware variant = aqua; aqua's sub-3:1 contrast is relieved by legends, direct
# labels and the CSV tables in out/)
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, Polygon

SURF, INK, INK2, MUTED, GRID, AXIS = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
C1, C2, C3, C4 = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": AXIS, "axes.labelcolor": INK2,
                     "xtick.color": MUTED, "ytick.color": INK2, "axes.facecolor": SURF, "figure.facecolor": SURF,
                     "savefig.facecolor": SURF})
QQ = np.arange(1, 6)
DD = np.arange(1, 11)


def style_axes(ax, grid_axis="y"):
    for sp in ["top", "right", "left"]:
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color(AXIS)
    ax.grid(axis=grid_axis, color=GRID, linewidth=0.8, linestyle="-")
    ax.set_axisbelow(True)
    ax.tick_params(length=0)


def hbar(ax, yc, v, h, color, r_px=7):
    """Horizontal bar from 0 to v, rounded at the data end, square at the baseline (one polygon, display space)."""
    if v == 0:
        return
    T = ax.transData
    (xb, ylo), (xe, yhi) = T.transform((0, yc - h / 2)), T.transform((v, yc + h / 2))
    sgn = 1.0 if xe >= xb else -1.0
    r = min(r_px, abs(yhi - ylo) / 2.0, abs(xe - xb))
    th = np.linspace(0, np.pi / 2, 10)
    lower = [(xe - sgn * r + sgn * r * np.sin(a), ylo + r - r * np.cos(a)) for a in th]
    upper = [(xe - sgn * r + sgn * r * np.cos(a), yhi - r + r * np.sin(a)) for a in th]
    pts = [(xb, ylo)] + lower + upper + [(xb, yhi)]
    ax.add_patch(Polygon(T.inverted().transform(pts), closed=True, facecolor=color, edgecolor="none", zorder=3))


def vbar(ax, xc, v, w, color, r_px=7):
    """Column from 0 to v, rounded at the data end, square at the baseline (one polygon, display space)."""
    if v == 0:
        return
    T = ax.transData
    (xlo, yb), (xhi, ye) = T.transform((xc - w / 2, 0)), T.transform((xc + w / 2, v))
    sgn = 1.0 if ye >= yb else -1.0
    r = min(r_px, abs(xhi - xlo) / 2.0, abs(ye - yb))
    th = np.linspace(0, np.pi / 2, 10)
    left = [(xlo + r - r * np.cos(a), ye - sgn * r + sgn * r * np.sin(a)) for a in th]
    right = [(xhi - r + r * np.sin(a), ye - sgn * r + sgn * r * np.cos(a)) for a in th]
    pts = [(xlo, yb)] + left + right + [(xhi, yb)]
    ax.add_patch(Polygon(T.inverted().transform(pts), closed=True, facecolor=color, edgecolor="none", zorder=3))


def eur(v, dec=0):
    s = f"{abs(v):,.{dec}f}"
    return f"−€{s}" if v < 0 else f"+€{s}"


def signed(v, fmt="{:.2f}"):
    return ("−" if v < 0 else "+") + fmt.format(abs(v))


# --- Figure 1: what Finnish land rent can fund
fg = PHI[PHI["convention"] == "coherent"].copy()
rowsF = [("All household land, 10-year yield 2022 (1.69%)", fg[(fg.base == "B2") & (fg.measure == "m1") & (fg.yield_year == 2022) & ~fg.label.str.contains("law")]),
         ("All household land, 2022 yield + 1.5 points", fg[(fg.base == "B2") & (fg.measure == "m2") & (fg.yield_year == 2022)]),
         ("All household land, 10-year yield 2023 (3.04%)", fg[(fg.base == "B2") & (fg.measure == "m1") & (fg.yield_year == 2023)]),
         ("All household land, 2023 yield + 1.5 points", fg[(fg.base == "B2") & (fg.measure == "m2") & (fg.yield_year == 2023)]),
         ("Residential land only, 2022 yield", fg[(fg.base == "B1") & (fg.measure == "m1") & (fg.yield_year == 2022)]),
         ("Residential land only, 2022 yield + 1.5", fg[(fg.base == "B1") & (fg.measure == "m2") & (fg.yield_year == 2022)]),
         ("All private land (households, firms, non-profits), 2022 yield", fg[(fg.base == "B3") & (fg.measure == "m1") & (fg.yield_year == 2022)]),
         ("All private land, 2022 yield + 1.5", fg[(fg.base == "B3") & (fg.measure == "m2") & (fg.yield_year == 2022)]),
         ("Residential land, housing services x land share (19.7%)", fg[(fg.measure == "m5")]),
         ("Residential land, 30% of housing services (US measure)", fg[(fg.measure == "m3")]),
         ("Residential land, 50% of housing services (US measure)", fg[(fg.measure == "m4")])]
vals = [float(r["dividend_full"].iloc[0]) for _, r in rowsF]
labs = [l for l, _ in rowsF]
fig = plt.figure(figsize=(14.5, 7.4), dpi=200)
axL = fig.add_axes([0.30, 0.13, 0.40, 0.67])
axR = fig.add_axes([0.775, 0.13, 0.20, 0.67])
n = len(vals)
yy = np.arange(n)[::-1].astype(float)
style_axes(axL, "x")
axL.set_xlim(0, 300)
axL.set_ylim(-0.7, n - 0.3)
fig.canvas.draw()
for v, yc, lab in zip(vals, yy, labs):
    hbar(axL, yc, v, 0.52, C2 if "US measure" not in lab else "#f2a27f")
    axL.text(v + 4, yc, f"€{v:,.0f}  ({100 * v / DIV_V['coherent']:.0f}%)", va="center", fontsize=8, color=INK2)
axL.axvline(DIV_V["coherent"], color=INK, linewidth=1.2, zorder=4)
axL.text(DIV_V["coherent"] + 3, n - 0.45, f"the VAT bridge's dividend, €{DIV_V['coherent']:.0f}", fontsize=8, color=INK, va="bottom")
axL.axvline(DIV_V_LAW["coherent"], color=MUTED, linewidth=1.0, zorder=4)
axL.text(DIV_V_LAW["coherent"] - 3, n - 0.45, f"under Finnish VAT law, €{DIV_V_LAW['coherent']:.0f}", fontsize=7.6, color=MUTED, va="bottom", ha="right")
axL.set_yticks(yy)
axL.set_yticklabels(labs, fontsize=8.4)
axL.set_xlabel("Dividend that full capture (phi = 0.98) funds, € per adult share per month", fontsize=9)
axL.set_title("Full capture of land rent: the dividend it funds (share of the bridge's)", fontsize=10, color=INK, loc="left")
# right: dwelling value lost at announcement, Finland and the US
dv = [("FI full capture", F.PHI_FULL * SH["s_d"]), ("FI bridge revenue, yield + 1.5", F.dwelling_value_loss(PHIS["bridge_m2"], SH["s_d"])),
      ("FI bridge revenue, 2022 yield", F.dwelling_value_loss(PHIS["bridge_m1"], SH["s_d"])), ("US bridge (L1, phi 0.85)", US_PHI_B * s_us),
      ("US full capture (L1)", F.PHI_FULL * s_us)]
yy2 = np.arange(len(dv))[::-1].astype(float)
style_axes(axR, "x")
axR.set_xlim(0, 118)
axR.set_ylim(-0.7, len(dv) - 0.3)
fig.canvas.draw()
for (lab, v), yc in zip(dv, yy2):
    hbar(axR, yc, 100 * v, 0.52, C2 if lab.startswith("FI") else MUTED)
    axR.text(100 * v + 2, yc, f"{100 * v:.0f}%", va="center", fontsize=8, color=INK2)
axR.set_yticks(yy2)
axR.set_yticklabels([l for l, _ in dv], fontsize=8.2)
axR.set_xlabel("Dwelling value lost at announcement, %", fontsize=9)
axR.set_title("What the revenue costs the dwellings", fontsize=10, color=INK, loc="left")
fig.text(0.04, 0.95, "Finnish household land rent cannot fund the bridge's dividend", fontsize=13.5, color=INK, weight="bold")
fig.text(0.04, 0.905, f"Full capture of all household land rent at the 2022 yield funds €{vals[0]:.0f} of the bridge's €{DIV_V['coherent']:.0f}. "
         f"Raising the whole €{VAT_REV_MEUR / 1e3:.1f}bn from land would take {PHIS['bridge_m1']:.1f} times the land rent:\na charge of "
         f"{float(fg[(fg.base == 'B2') & (fg.measure == 'm1') & (fg.yield_year == 2022)]['tau_bridge_pct_of_land_value'].iloc[0]):.1f}% of land value a year, "
         "whose present value is the dwellings' whole value. That is a levy on owners, not a tax on land rent.", fontsize=9, color=INK2, va="top", linespacing=1.35)
fig.text(0.04, 0.025, "Coherent convention (HBS 2022, equal-household weights). Land: wealth survey 2023 calibrated to the household balance sheet (N211, N111), "
         "carried to 2022 with N211. Yields: Eurostat EMU convergence 10-year series.\nLighter bars: the paper's US flow measures applied to Finnish housing services; "
         "they imply land rent of 9-15% of land value a year. Source: out/fi_lvt_phi.csv, fi_lvt_capitalization.csv.", fontsize=7.4, color=MUTED, linespacing=1.35)
fig.savefig(FIG / "fig_fi_funding_gap.png", dpi=200)
plt.close(fig)

# --- Figure 2: who gains and who pays
fig, axs = plt.subplots(2, 2, figsize=(14.5, 10.2), dpi=200)
fig.subplots_adjust(left=0.065, right=0.975, top=0.84, bottom=0.10, wspace=0.22, hspace=0.46)
a_ = ACC[ACC["convention"] == "coherent"]
series = [("VAT bridge (rebuilt, coherent)", a_[a_["instrument"] == "VAT"], C1),
          ("LVT on all household land (B2)", a_[(a_["base"] == "B2")], C2), ("LVT on residential land (B1)", a_[(a_["base"] == "B1")], C3)]
for ax, rate, title in [(axs[0, 0], "bridge", f"Same revenue (notional): every dividend €{DIV_V['coherent']:.0f}"),
                        (axs[0, 1], "full_m1", "What land can fund: full capture at the 2022 yield")]:
    style_axes(ax)
    ax.axhline(0, color=AXIS, linewidth=1.0, zorder=2)
    for lab, d, col in series:
        dd = d if lab.startswith("VAT") else d[d["rate"] == rate]
        y = dd.set_index("quintile").loc[Q, "net"].values
        ax.plot(QQ, y, color=col, linewidth=2, zorder=3, solid_capstyle="round")
        ax.plot(QQ, y, linestyle="none", marker="o", markersize=6.5, markerfacecolor=col, markeredgecolor=SURF, markeredgewidth=2, zorder=4)
        if "B1" not in lab:                       # selective labels: B1's values are in the legend's table (CSV)
            ax.annotate(eur(y[-1]), (5, y[-1]), xytext=(8, 0), textcoords="offset points", va="center", fontsize=8, color=INK2)
            ax.annotate(eur(y[0]), (1, y[0]), xytext=(-8, 0), textcoords="offset points", va="center", ha="right", fontsize=8, color=INK2)
    ax.set_xticks(QQ)
    ax.set_xticklabels([f"Q{i}" for i in QQ])
    ax.set_xlim(0.3, 5.7)
    ax.set_ylabel("Net transfer, € per adult share per month", fontsize=9)
    ax.set_title(title, fontsize=10.5, color=INK, loc="left")
divs = {r: [float(a_[(a_["base"] == b) & (a_["rate"] == r)]["dividend"].iloc[0]) for b in ("B2", "B1")] for r in ("full_m1",)}
axs[0, 1].text(0.0, -0.13, f"dividends: VAT €{DIV_V['coherent']:.0f} (for reference) · LVT B2 €{divs['full_m1'][0]:.0f} · LVT B1 €{divs['full_m1'][1]:.0f}",
               transform=axs[0, 1].transAxes, fontsize=7.6, color=MUTED, va="top")
axs[0, 0].text(0.0, -0.13, f"LVT: a charge of {100 * tau_of('bridge', 'B2', 'coherent'):.1f}% (B2) and {100 * tau_of('bridge', 'B1', 'coherent'):.1f}% (B1) of land value a year, "
               f"{PHIS['bridge_m1']:.1f} and {tau_of('bridge', 'B1', 'coherent') / Y22:.1f} times the land rent",
               transform=axs[0, 0].transAxes, fontsize=7.6, color=MUTED, va="top")
# (c) households that pay net, by quintile / decile
ax = axs[1, 0]
style_axes(ax)
ax.plot(DD, 100 * wdm["payer_share_of_households"].values, color=C2, linewidth=2, zorder=3)
ax.plot(DD, 100 * wdm["payer_share_of_households"].values, linestyle="none", marker="o", markersize=6.5, markerfacecolor=C2, markeredgecolor=SURF,
        markeredgewidth=2, zorder=4)
xq = np.array([1.5, 3.5, 5.5, 7.5, 9.5])
ax.plot(xq, 100 * VAT_PAYERS_Q.values, color=C1, linewidth=2, zorder=3)
ax.plot(xq, 100 * VAT_PAYERS_Q.values, linestyle="none", marker="o", markersize=6.5, markerfacecolor=C1, markeredgecolor=SURF, markeredgewidth=2, zorder=4)
ax.plot(DD, 100 * P_OWN.values, color=MUTED, linewidth=1.4, zorder=2)
ax.annotate("own their home", (10, 100 * P_OWN.values[-1]), xytext=(8, 0), textcoords="offset points", va="center", fontsize=8, color=MUTED)
ax.annotate("pay net, LVT", (10, 100 * wdm["payer_share_of_households"].values[-1]), xytext=(8, -9), textcoords="offset points", va="center", fontsize=8, color=INK2)
ax.annotate("pay net, VAT", (9.5, 100 * VAT_PAYERS_Q.values[-1]), xytext=(8, 0), textcoords="offset points", va="center", fontsize=8, color=INK2)
ax.set_xticks(DD)
ax.set_xticklabels([f"D{i}" for i in DD])
ax.set_xlim(0.5, 11.9)
ax.set_ylim(0, 100)
ax.set_ylabel("Households, % of the decile", fontsize=9)
ax.set_title(f"Who pays net: {100 * pay_share_all:.0f}% of households under the LVT (any rate)", fontsize=10.5, color=INK, loc="left")
ax.text(0.0, -0.11, "LVT: owners' land log-normal inside deciles (main-residence quartiles); renters' land (2.5% of household land) is assigned\n"
        "to owners, so renters pay nothing by assumption. VAT: spending log-normal inside quintiles (sigma 0.45, judgment)",
        transform=ax.transAxes, fontsize=7.6, color=MUTED, va="top", linespacing=1.3)
# (d) payers' liquidity
ax = axs[1, 1]
style_axes(ax)
ax.set_xlim(0.4, 10.6)
ax.set_ylim(0, 45)
fig.canvas.draw()
for i, dd_ in enumerate(DEC):
    for off, v, col in [(-0.17, LIQ.set_index("decile").loc[dd_, "htm_all_half_month"], C1), (0.17, LIQ.set_index("decile").loc[dd_, "htm_owners_half_month"], C2)]:
        vbar(ax, i + 1 + off, 100 * v, 0.30, col)
ax.set_xticks(DD)
ax.set_xticklabels([f"D{i}" for i in DD])
ax.set_ylabel("Hand-to-mouth, %", fontsize=9)
ax.set_title("Payers' liquidity: deposits at most half a month's income", fontsize=10.5, color=INK, loc="left")
ax.legend(handles=[Patch(facecolor=C1, edgecolor="none", label="all households (VAT payers' grade)"),
                   Patch(facecolor=C2, edgecolor="none", label="owners (LVT payers' grade)")], loc="upper right", frameon=False, fontsize=8, labelcolor=INK2)
ax.text(0.0, -0.11, "Deposit quartiles and median disposable income by decile (151u);\nowners scaled by the tenure table's outright/mortgaged mix (151z)",
        transform=ax.transAxes, fontsize=7.6, color=MUTED, va="top", linespacing=1.3)
handles = [Line2D([0], [0], color=c, linewidth=2, marker="o", markersize=6, markeredgecolor=SURF, label=l) for l, _, c in series]
fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.06, 0.905), ncol=3, frameon=False, fontsize=8.4, labelcolor=INK2)
fig.text(0.065, 0.965, "Who gains and who pays in Finland: the VAT bridge and a land-value tax funding a flat dividend", fontsize=13.5, color=INK, weight="bold")
fig.text(0.065, 0.94, "At the same revenue the LVT is about twice as redistributive as the VAT; the land Finland's households own can fund only a fifth of it "
         "at the 2022 yield (a third at the 2023-25 yields).", fontsize=9, color=INK2)
fig.text(0.065, 0.012, "HBS 2022 income quintiles, payment shares adult 1, child 0.3 (coherent convention). Land: wealth survey 2023 deciles paired into quintiles. "
         "Source: out/fi_lvt_accounting_by_quintile.csv, fi_lvt_within_decile.csv, fi_lvt_liquidity.csv.", fontsize=7.4, color=MUTED)
fig.savefig(FIG / "fig_fi_net_by_quintile.png", dpi=200)
plt.close(fig)

# --- Figure 3: demand shifts side by side, the 15 largest charted movers
mc_chart = M["coherent"]["chart"]
vat_b = SHF[(SHF["convention"] == "coherent") & (SHF["instrument"] == "VAT") & (SHF["grade"] == "post_mid")].set_index("category")["dEUR"]
lvt_b = SHF[(SHF["convention"] == "coherent") & (SHF["instrument"] == "LVT") & (SHF["base"] == "B2") & (SHF["rate"] == "bridge") &
            (SHF["grade"] == "post_mid")].set_index("category")["dEUR"]
lvt_t = TEN[(TEN["convention"] == "coherent") & (TEN["instrument"] == "LVT") & (TEN["base"] == "B2") & (TEN["grade"] == "wealth_mid")].set_index("category")["dEUR"]
dsh = pd.DataFrame({"vat": vat_b, "lvt": lvt_b, "lvt_t": lvt_t}).loc[mc_chart]
top = list(dsh.abs().max(axis=1).sort_values(ascending=False).index[:15])
cols = [("vat", "VAT, the post's method", C1), ("lvt", "LVT (B2), the post's method", C2),
        ("lvt_t", "LVT (B2), tenure-aware baskets, unconstrained payers draw on wealth", C3)]
tot = {c: float(dsh[c].sum()) for c, _, _ in cols}
n = len(top)
fig = plt.figure(figsize=(14.5, 9.6), dpi=200)
axL = fig.add_axes([0.285, 0.115, 0.42, 0.705])
axR = fig.add_axes([0.755, 0.115, 0.22, 0.705], sharey=axL)
yy = np.arange(n)[::-1].astype(float)
bh = 0.24
axL.set_xlim(min(dsh.loc[top].min().min(), 0) - 0.6, dsh.loc[top].max().max() + 2.4)
axL.set_ylim(-0.7, n - 0.3)
style_axes(axL, "x")
axL.axvline(0, color=AXIS, linewidth=1.0, zorder=2)
fig.canvas.draw()
for j, (c, lab, col) in enumerate(cols):
    for cat, yc in zip(top, yy):
        hbar(axL, yc + (1 - j) * (bh + 0.03), float(dsh.loc[cat, c]), bh, col)
for cat, yc in zip(top, yy):
    if cat in ("04.1 Actual rents", "04.4 Water & misc. dwelling services", "07.1 Purchase of vehicles"):
        for j, (c, _, _) in enumerate(cols):
            v = float(dsh.loc[cat, c])
            axL.text(max(v, 0) + 0.2, yc + (1 - j) * (bh + 0.03), signed(v), va="center", fontsize=7.4, color=INK2)
axL.set_yticks(yy)
axL.set_yticklabels(top, fontsize=8.4)
axL.set_xlabel("Change in spending at impact, € per adult share per month", fontsize=9)
axL.set_title(f"Euros (same revenue: dividend €{DIV_V['coherent']:.0f}; mid MPC schedule)", fontsize=9.6, color=INK, loc="left")
style_axes(axR, "x")
axR.axvline(0, color=AXIS, linewidth=1.0, zorder=2)
for j, (c, lab, col) in enumerate(cols):
    axR.plot(100 * dsh.loc[top, c].values / tot[c], yy + (1 - j) * (bh + 0.03), linestyle="none", marker="o", markersize=5.6,
             markerfacecolor=col, markeredgecolor=SURF, markeredgewidth=1.4, zorder=4)
axR.tick_params(axis="y", labelleft=False)
axR.set_xlabel("Share of the version's charted total, %", fontsize=9)
axR.set_title("Composition (each version / its own total)", fontsize=9.6, color=INK, loc="left")
fig.text(0.04, 0.955, "Demand shifts: the Finnish LVT is the VAT scaled up, until renters and owners get their own baskets",
         fontsize=13.5, color=INK, weight="bold")
fig.text(0.04, 0.928, f"Charted totals: VAT €{tot['vat']:.2f}, LVT €{tot['lvt']:.2f} (quintile-netted), €{tot['lvt_t']:.2f} (tenure-aware). "
         f"All 37 bars keep their sign; LVT/VAT median ratio {float(c0.loc[c0['vat'].abs() > 0.05, 'ratio'].median()):.2f}.",
         fontsize=9, color=INK2)
fig.legend(handles=[Patch(facecolor=col, edgecolor="none", label=lab) for _, lab, col in cols], loc="upper left",
           bbox_to_anchor=(0.285, 0.905), ncol=3, frameon=False, fontsize=8.2, labelcolor=INK2)
DIVS_RATIO = float(ACC_L[("coherent", "B2", "full_m1")]["dividend"].iloc[0] / DIV_V["coherent"])
TT_AA = float(TEN[(TEN["convention"] == "coherent") & (TEN["instrument"] == "LVT") & (TEN["base"] == "B2") & (TEN["grade"] == "wealth_mid")]
              .set_index("category").loc[mc_chart, "dEUR_as_allocated"].sum())
fig.text(0.04, 0.025, "HBS 2022 quintiles (coherent convention), Working-model elasticities (bridge.py). Tenure-aware: actual rent with renters, housing-company "
         "charges with owners, and owners' changes spread over the lines they transact:\nimputed rent and housing-loan interest cannot move at impact (booked "
         f"there as the Working model allocates them, the tenure-aware charted total would be €{TT_AA:.2f}: dEUR_as_allocated in the CSV). At full capture "
         f"(2022 yield) every LVT bar\nis {100 * DIVS_RATIO:.0f}% of the one shown. Source: out/fi_lvt_demand_shifts.csv, fi_lvt_demand_compare.csv, fi_lvt_tenure_aware.csv.",
         fontsize=7.4, color=MUTED, linespacing=1.35)
fig.savefig(FIG / "fig_fi_demand_shifts.png", dpi=200)
plt.close(fig)

# --- Figure 4: the macro channels
fig = plt.figure(figsize=(14.5, 10.8), dpi=200)
axP = fig.add_axes([0.40, 0.775, 0.56, 0.085])
axD = fig.add_axes([0.40, 0.125, 0.56, 0.575])
pr = MACRO[MACRO["unit"].str.startswith("% of consumer")].reset_index(drop=True)
style_axes(axP, "x")
for k, (lab, col) in enumerate([("VAT", C1), ("LVT", C2)]):
    r = pr[pr["instrument"] == lab].iloc[0]
    yc = 1 - k
    axP.plot([r["low"], r["high"]], [yc, yc], color=col, linewidth=2, solid_capstyle="round", zorder=3)
    axP.plot(r["central"], yc, marker="o", markersize=7, markerfacecolor=col, markeredgecolor=SURF, markeredgewidth=2, zorder=4)
    axP.text(-0.02, yc, f"{lab}: {r['central']:.1f}%" + (f" [{r['low']:.1f}, {r['high']:.1f}]" if r["high"] > 0 else ""),
             transform=axP.get_yaxis_transform(), ha="right", va="center", fontsize=8.6, color=INK2)
axP.set_ylim(-0.6, 1.6)
axP.set_yticks([])
axP.set_xlim(-0.5, 10.5)
axP.set_title("Channel 1: the price level (one-off step, % of the consumer price level)", fontsize=10, color=INK, loc="left")
rows_d = [("VAT", "flow impulse, post's method (mid; band = high/low schedules)", "VAT: flow impulse, post's method"),
          ("VAT", "flow impulse, unconstrained payers draw on wealth", "VAT: flow, unconstrained payers draw on wealth"),
          ("VAT", "levy channel, lambda = 0.35 (impact; 2-5c per EUR per year)", "VAT: levy channel, lambda = 0.35"),
          ("VAT", "levy channel, lambda = 1 (impact)", "VAT: levy channel, lambda = 1 (full A-K)"),
          ("VAT", "net demand at impact, lambda = 0.35 (flow + levy)", "VAT: net at impact, lambda = 0.35"),
          (None, None, None),
          ("LVT", "flow impulse, post's method (full capture, 2022 yield, B2)", "LVT: flow impulse, post's method"),
          ("LVT", "flow impulse, unconstrained payers draw on wealth (full capture, B2)", "LVT: flow, unconstrained payers draw on wealth"),
          ("LVT", "collateral: credit effect on all crossers' lost borrowing capacity (full capture, immediate)", "LVT: collateral, credit effect (clean)"),
          ("LVT", "collateral: credit effect, hand-to-mouth crossers only (full capture, immediate)", "LVT: collateral, hand-to-mouth crossers only"),
          ("LVT", "collateral on all crossers' lost equity: includes the T4 overlap (full capture, immediate)", "LVT: collateral on lost equity (T4 overlap)"),
          ("LVT", "non-occupying holders: wealth effect instead of flow (change in impulse, full capture, B2)", "LVT: cottages, rentals, forest on a wealth effect"),
          ("LVT", "net demand at impact: flow + credit effect (full capture, 2022 yield)", "LVT: net at impact, flow + credit effect"),
          ("LVT", "net demand at impact, only hand-to-mouth crossers respond (full capture)", "LVT: net at impact, hand-to-mouth crossers only"),
          ("LVT", "net demand at impact, includes the T4 overlap (full capture)", "LVT: net at impact, lost equity (T4 overlap)"),
          ("LVT", "net demand at impact, every non-occupier on the wealth reading (full capture)", "LVT: net at impact, non-occupiers on wealth"),
          ("LVT", "net demand at impact: flow + credit effect (full capture, yield + 1.5)", "LVT: net at impact, yield + 1.5"),
          ("LVT", "net demand at impact: flow + credit effect (full capture, 2024 yield)", "LVT: net at impact, 2024 yield (2.85%)"),
          ("LVT", "net demand at impact, every non-occupier on the wealth reading (full capture, 2024 yield)", "LVT: non-occupiers on wealth, 2024 yield")]
pub = {"VAT: flow impulse, post's method": "post, published: flow-only path (year 3; band)",
       "VAT: levy channel, lambda = 1 (full A-K)": "post, published: full A-K lambda = 1 (year 3; band)",
       "VAT: net at impact, lambda = 0.35": "post, published: central lambda = 0.35 (year 3; band)"}
style_axes(axD, "x")
axD.axvline(0, color=AXIS, linewidth=1.0, zorder=2)
yt = len(rows_d)
ylabels, yticks = [], []
for inst, ch, lab in rows_d:
    yt -= 1
    if inst is None:
        continue
    rr = MACRO[(MACRO["instrument"] == inst) & (MACRO["channel"] == ch)]
    assert len(rr) == 1, ch
    r = rr.iloc[0]
    col = C1 if inst == "VAT" else C2
    axD.plot([r["low"], r["high"]], [yt, yt], color=col, linewidth=2, solid_capstyle="round", zorder=3)
    axD.plot(r["central"], yt, marker="o", markersize=7, markerfacecolor=col, markeredgecolor=SURF, markeredgewidth=2, zorder=4)
    axD.text(max(r["high"], r["central"]) + 0.04, yt, signed(r["central"]), va="center", fontsize=7.8, color=INK2)
    yticks.append(yt)
    ylabels.append(lab)
    if lab in pub:
        p = MACRO[MACRO["channel"] == pub[lab]].iloc[0]
        axD.plot([p["low"], p["high"]], [yt - 0.34, yt - 0.34], color=INK, linewidth=1.2, zorder=3)
        axD.plot(p["central"], yt - 0.34, marker="D", markersize=5, markerfacecolor=SURF, markeredgecolor=INK, markeredgewidth=1.1, zorder=5)
axD.set_yticks(yticks)
axD.set_yticklabels(ylabels, fontsize=8.4)
axD.set_ylim(-0.8, len(rows_d) - 0.4)
axD.set_xlabel("Change in consumption demand at impact, % of consumption (HBS 2022)", fontsize=9)
axD.set_title("Channel 2: demand (dot: central; line: band). LVT rows at full capture (phi = 0.98), 2022 yield unless marked", fontsize=10, color=INK,
              loc="left")
fig.legend(handles=[Line2D([0], [0], color=C1, linewidth=2, marker="o", markersize=7, markeredgecolor=SURF, label="VAT bridge (this unit, impact)"),
                    Line2D([0], [0], color=C2, linewidth=2, marker="o", markersize=7, markeredgecolor=SURF, label="LVT, full capture (impact)"),
                    Line2D([0], [0], color=INK, linewidth=1.2, marker="D", markersize=5, markerfacecolor=SURF, markeredgecolor=INK,
                           label="the post's published Finnish path (year 3)")],
           loc="upper left", bbox_to_anchor=(0.40, 0.93), ncol=3, frameon=False, fontsize=8.4, labelcolor=INK2)
fig.text(0.04, 0.965, "Two channels, kept apart: no price step and no lambda; the sign turns on how holders read their land loss", fontsize=13.5, color=INK, weight="bold")
NO_YRS = [yv(str(y), "nonocc_wealth") for y in YEARS[1:]]
LPB = YY.drop_duplicates("yield_label").set_index("yield_label")["loss_per_euro_of_nonocc_bill"]
fig.text(0.04, 0.016, "Impact-period, static: flows at the rebuilt MPC schedules; the levy at 2-5 cents per € of survey net worth; collateral at 4.7-7 cents per € (US "
         "estimates; 10 cents stress, no source, in the CSV) on mortgaged owners crossing 80% LTV\n(US-shape LTVs inside each decile). The yield sets the "
         f"non-occupier reading: a capitalized loss is 1/r times its bill ({LPB['2022']:.0f} at the 2022 yield, {LPB[['2023', '2024', '2025']].min():.0f}-"
         f"{LPB[['2023', '2024', '2025']].max():.0f} at 2023-25), so the reading is {signed(min(NO_YRS))} to {signed(max(NO_YRS))} at the 2023-25 yields.\n"
         "The post's numbers come from its dynamic model and are shown for orientation. "
         f"At the notional bridge rate (phi 5.2) dwellings lose their whole value and flow + credit effect is {signed(float(hb.loc['clean', 'central']), '{:.1f}')}%. "
         "Source: out/fi_lvt_macro_channels.csv, fi_lvt_headline.csv, fi_lvt_yield_years.csv.", fontsize=7.4, color=MUTED, linespacing=1.35)
fig.savefig(FIG / "fig_fi_macro_channels.png", dpi=200)
plt.close(fig)

# --- Figure 5: the US beside Finland
fig = plt.figure(figsize=(14.5, 9.4), dpi=200)
axA = fig.add_axes([0.235, 0.115, 0.25, 0.645])
axB = fig.add_axes([0.70, 0.115, 0.26, 0.645])
ca = [("residential land", "top income decile's share of residential land"), ("all land in the wider base (*)", "top income decile's share of all household land"),
      ("financial assets", "top income decile's share of financial assets"), ("net wealth", "top income decile's share of net wealth"),
      ("VAT-able consumption (top quintile)", "top income quintile's share of VAT-able consumption")]
ucx = UC.set_index("item")
yy = np.arange(len(ca))[::-1].astype(float)
style_axes(axA, "x")
for (lab, it), yc in zip(ca, yy):
    us_, fi_ = 100 * float(ucx.loc[it, "US"]), 100 * float(ucx.loc[it, "FI"])
    axA.plot([fi_, us_], [yc, yc], color=GRID, linewidth=3, zorder=2, solid_capstyle="round")
    axA.plot(us_, yc, marker="o", markersize=8, markerfacecolor=C1, markeredgecolor=SURF, markeredgewidth=2, zorder=4)
    axA.plot(fi_, yc, marker="o", markersize=8, markerfacecolor=C2, markeredgecolor=SURF, markeredgewidth=2, zorder=4)
    axA.text(max(us_, fi_) + 2, yc, f"gap {us_ - fi_:.0f} pts", va="center", fontsize=7.8, color=INK2)
axA.set_yticks(yy)
axA.set_yticklabels([l for l, _ in ca], fontsize=8.4)
axA.set_xlim(0, 85)
axA.set_ylim(-0.7, len(ca) - 0.3)
axA.set_xlabel("Share held by the top income decile, %", fontsize=9)
axA.set_title("Concentration: land is less top-heavy than financial wealth", fontsize=10, color=INK, loc="left")
B24 = [b for b in UC["block"].unique() if b.startswith("LVT, full capture (phi 0.98), both at their 2024 yields")][0]
B22 = [b for b in UC["block"].unique() if b.startswith("LVT, full capture (phi 0.98), both at their 2022 yields")][0]
BUS = [b for b in UC["block"].unique() if b.startswith("LVT, the US bridge's share of rent") and b.endswith("both at their 2024 yields")][0]
CLEAN, T4I, NOI = ("net demand at impact (flow + credit effect)", "net demand at impact, includes the T4 overlap (6c x lost equity)",
                   "net demand at impact, non-occupiers on the wealth reading (3.5c)")
cb = [[("VAT: net at impact (flow + levy, lambda 0.35)", "VAT, impact (same formulas)", "net demand at impact (flow + levy)"),
       ("VAT: the post's published central path", "VAT, published", "the post's central path (year 3)")],
      [("LVT phi 0.98, 2024 yields: flow + credit effect", B24, CLEAN), ("LVT phi 0.98, 2024 yields: lost equity (T4 overlap)", B24, T4I),
       ("LVT phi 0.98, 2024 yields: non-occupiers on wealth", B24, NOI)],
      [("LVT phi 0.98, 2022 yields: flow + credit effect", B22, CLEAN), ("LVT phi 0.98, 2022 yields: lost equity (T4 overlap)", B22, T4I),
       ("LVT phi 0.98, 2022 yields: non-occupiers on wealth", B22, NOI)],
      [("LVT phi 0.85 (US bridge), 2024 yields: flow + credit effect", BUS, CLEAN),
       ("LVT, same revenue (FI 2022 yield): flow + credit effect", "LVT, same revenue as Finland's full capture", CLEAN)]]
UCb = UC.set_index(["block", "item"])
ypos, rows_b, yc = [], [], 0.0
for grp in cb[::-1]:
    for row in grp[::-1]:
        ypos.append(yc)
        rows_b.append(row)
        yc += 1.0
    yc += 0.55                                              # air between groups instead of a rule
style_axes(axB, "x")
axB.axvline(0, color=AXIS, linewidth=1.0, zorder=2)
for (lab, blk, it), yc in zip(rows_b, ypos):
    us_, fi_ = float(UCb.loc[(blk, it), "US"]), float(UCb.loc[(blk, it), "FI"])
    axB.plot([fi_, us_], [yc, yc], color=GRID, linewidth=3, zorder=2, solid_capstyle="round")
    axB.plot(us_, yc, marker="o", markersize=8, markerfacecolor=C1, markeredgecolor=SURF, markeredgewidth=2, zorder=4)
    axB.plot(fi_, yc, marker="o", markersize=8, markerfacecolor=C2, markeredgecolor=SURF, markeredgewidth=2, zorder=4)
    axB.text(max(us_, fi_) + 0.08, yc, f"US {signed(us_)}  FI {signed(fi_)}", va="center", fontsize=7.8, color=INK2)
axB.set_yticks(ypos)
axB.set_yticklabels([l for l, _, _ in rows_b], fontsize=8.4)
axB.set_xlim(-2.0, 1.35)
axB.set_ylim(-0.7, max(ypos) + 0.7)
axB.set_xlabel("Demand at impact, % of consumption", fontsize=9)
axB.set_title("Net demand at impact, % of consumption", fontsize=10, color=INK, loc="left")
fig.legend(handles=[Line2D([0], [0], color=C1, linewidth=0, marker="o", markersize=8, markeredgecolor=SURF, label="United States (US unit)"),
                    Line2D([0], [0], color=C2, linewidth=0, marker="o", markersize=8, markeredgecolor=SURF, label="Finland (this unit)")],
           loc="upper left", bbox_to_anchor=(0.235, 0.845), ncol=2, frameon=False, fontsize=8.6, labelcolor=INK2)
u24, f24 = SAME_YEAR[2024]
u22, f22 = SAME_YEAR[2022]
fig.text(0.04, 0.968, "The US beside Finland: the LVT shrinks the gap, but not because land is less concentrated", fontsize=13.5, color=INK, weight="bold")
fig.text(0.04, 0.942, "The VAT's gap is its levy channel: the post's lambda on net worth, which the US has far more of. An LVT has no levy, and on the clean reading "
         "(collateral as a credit effect) both\ncountries sit near zero when each is on the same year's yield "
         f"(2024: US {signed(u24['clean'])}, FI {signed(f24['clean'])}). The gap reopens if mortgaged crossers respond to their lost equity: it hits "
         f"the US ({signed(u24['t4'])} against {signed(f24['t4'])}),\nwhere land is {100 * s_us:.0f}% of house values against {100 * SH['s_d']:.0f}% "
         f"and {(float(uin['L_hh']) / US_C_BN) / (N211_22 / C_MEUR):.1f} times as much per unit of consumption. Non-occupiers' capitalized losses weigh about the "
         f"same in both on the same year's yield\n(2024: {signed(u24['nonocc'])}, {signed(f24['nonocc'])}; 2022: {signed(u22['nonocc'])}, {signed(f22['nonocc'])}). "
         f"Set Finland's 2022 yield against the US's 2024 one ({signed(f22['nonocc'])} against {signed(u24['nonocc'])}) and they seem to split: a loss is "
         f"1/r times its bill ({f22['loss_per_bill']:.0f} against {u24['loss_per_bill']:.0f}).", fontsize=9, color=INK2, va="top", linespacing=1.35)
fig.text(0.04, 0.022, "US: consumption/lvt/out (SCF 2025, CE 2024, Z.1) at the 2024 Treasury yield (4.21%); its 2022-yield rows put the flow and the non-occupiers' "
         f"bills on GS10 2022 ({100 * US_R[2022]:.2f}%) here, nothing else changed. FI: HBS 2022, wealth survey 2023,\nat its 2022 (1.69%) and 2024 (2.85%) "
         "yields the same way. Both at impact, same formulas: levy 3.5c (2-5c), collateral 6c (4.7-7c) per € per year; bands in out/fi_lvt_us_compare.csv, "
         "fi_lvt_yield_years.csv.\n(*) Definitions differ: the US adds noncorporate and corporate land (attributed to households by equity); Finland adds "
         "households' forest, farmland and business land.", fontsize=7.4, color=MUTED, linespacing=1.35)
fig.savefig(FIG / "fig_fi_us_compare.png", dpi=200)
plt.close(fig)
print("\nfigures written:", ", ".join(p.name for p in sorted(FIG.glob("fig_fi_*.png"))))
