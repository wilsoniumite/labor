# run_lvt_us.py - question 1, US: an LVT-funded flat dividend through the rebuilt VAT-bridge machinery, beside the
# VAT bridge. Steps 1-7 of the task (the tax, land by household, incidence, MPCs, demand shifts, macro, the loop),
# then the figures. Every output is a CSV in consumption/lvt/out/; the write-up is consumption/lvt/NOTES_us.md and
# the identities are re-checked by consumption/lvt/checks/check_lvt_us.py.
#
# Run from the repo root:  venv/bin/python -I consumption/lvt/code/run_lvt_us.py      (about a minute)
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

import lvt_us as L

B = L.B
OUT, FIG = L.OUT, L.FIG
OUT.mkdir(exist_ok=True)
FIG.mkdir(exist_ok=True)
DEC = L.DEC
pd.set_option("display.width", 230)
pd.set_option("display.max_columns", 40)
warnings.filterwarnings("ignore", category=pd.errors.PerformanceWarning)

# %% inputs: the rebuilt VAT bridge, Z.1, the rent measures, the SCF
m = B.build_model(2024)
acc_v = B.vat_accounting(m)
DIV_VAT = float(acc_v["dividend"].iloc[0])
S_CE = L.total_shares(m)                                  # CE 2024 payment shares (persons-equivalent)
C_TOT_BN = m["budget_bar"] * S_CE * 12.0 / 1e9            # CE consumption budget, $bn/yr (the post's denominator)
PCE_BN = L.pce_total(L.YEAR)
VAT_REV_BN = DIV_VAT * S_CE * 12.0 / 1e9
SCHED = L.post_schedules()
z1 = L.z1_targets()
RM = L.rent_measures(z1)
MEAS = {"m1": "m1_z1hh_x_gs10", "m2": "m2_z1hh_x_gs10p150", "m3": "m3_pce_housing_x_0.30", "m4": "m4_pce_housing_x_0.50"}
R = {k: float(RM.loc[v, "r"]) for k, v in MEAS.items()}

s22_raw = L.add_payment_units(L.load_scf(2022), 2022)
CELLS = L.adult_cells(s22_raw)
s25_raw = L.add_payment_units(L.load_scf(2025), 2025, CELLS)
s25, c25 = L.calibrate_units_to_ce(m, s25_raw)
s22, c22 = L.calibrate_units_to_ce(m, s22_raw)
S25, INFO25 = L.land_holdings(s25, z1)                    # main: SCF 2025, uniform s calibrated to Z.1 2024
S22, INFO22 = L.land_holdings(s22, z1)                    # robustness: SCF 2022 (real 2024 dollars), same Z.1 target
HTM = {b: L.htm_flags(S25, b) for b in L.HTM_DIVISOR}
HTM22 = L.htm_flags(S22, "biweekly")
MEAS_D, MEAS_DH = L.measured_mpc(S25, HTM["biweekly"])
print(f"CE 2024: {S_CE / 1e6:.2f}m payment shares, budget ${m['budget_bar']:.2f}/share/month = ${C_TOT_BN:,.0f}bn/yr "
      f"({100 * C_TOT_BN / PCE_BN:.1f}% of PCE ${PCE_BN:,.0f}bn); VAT dividend ${DIV_VAT:.2f} = revenue ${VAT_REV_BN:,.1f}bn/yr")
print(f"Z.1 2024 ($bn): household land {z1['L_hh']:,.1f} ({100 * z1['land_share_re']:.1f}% of HH real estate), noncorporate "
      f"{z1['L_nnb']:,.1f}, NFC (assumed: {z1['nfc_rule']}) {z1['L_nfc']:,.1f} [{z1['L_nfc_structures_proxy']:,.0f}-{z1['L_nfc_share_2020']:,.0f}]")
print("rent measures:\n" + RM[["label", "rT", "r"]].round(4).to_string())
inputs = [dict(item=k, value=v, source="Z.1 2026:Q2 vintage (consumption/data/tidy/z1_land.csv)")
          for k, v in z1.items() if isinstance(v, (int, float)) and not isinstance(v, bool)]
inputs += [dict(item=f"rT_{k}", value=float(RM.loc[v, "rT"]), source=RM.loc[v, "label"]) for k, v in MEAS.items()]
inputs += [dict(item=f"r_{k}", value=R[k], source="rent-to-value implied by the measure (rT / household land)") for k in MEAS]
inputs += [dict(item="gs10_2024", value=float(RM["gs10"].iloc[0]), source="pinning/cache/GS10.csv, mean of 12 months"),
           dict(item="pce_housing_2024_bn", value=float(RM["pce_housing"].iloc[0]), source="BEA Table 2.4.5U line 153 (DHSGRC), Oct 2026 vintage"),
           dict(item="pce_2024_bn", value=PCE_BN, source="BEA Table 2.4.5U line 1"),
           dict(item="ce_payment_shares", value=S_CE, source="CE 2024 Table 1110: sum of N_d x (adults + 0.3 children)"),
           dict(item="ce_consumption_bn", value=C_TOT_BN, source="bridge budget x payment shares x 12"),
           dict(item="vat_dividend_usd_month", value=DIV_VAT, source="rebuilt VAT accounting"),
           dict(item="vat_revenue_bn", value=VAT_REV_BN, source="dividend x payment shares x 12"),
           dict(item="cpi_2025_to_2024", value=L.CPI_25_TO_24, source="SCF macro CPILAG for 2025 (4750/4625)"),
           dict(item="scf2025_families_m", value=float(s25["WGT"].sum()) / 1e6, source="SCF 2025 summary extract"),
           dict(item="scf2022_families_m", value=float(s22["WGT"].sum()) / 1e6, source="SCF 2022 summary extract"),
           dict(item="s_uniform_2025", value=INFO25["s_uniform"], source="calibrated: Z.1 household land / SCF 2025 HOUSES+ORESRE (2024 $)"),
           dict(item="s_uniform_2022", value=INFO22["s_uniform"], source="calibrated: Z.1 household land / SCF 2022 HOUSES+ORESRE (2024 $)")]
inputs += [dict(item=f"judgment_{k}", value=v, source=s) for k, v, s in [
    ("mpw_low", L.MPW["low"], "post fn 31"), ("mpw_mid", L.MPW["mid"], "midpoint of 2-5c"), ("mpw_high", L.MPW["high"], "post fn 31"),
    ("mpc_coll_low", L.MPC_COLL["low"], "Aladangady 2017"), ("mpc_coll_mid", L.MPC_COLL["mid"], "Mian-Rao-Sufi 2013 5-7c midpoint"),
    ("mpc_coll_high", L.MPC_COLL["high"], "stress, judgment"), ("phi_full", L.PHI_FULL, "design memo 1.1"),
    ("gamma", L.GAMMA, "T4"), ("delta", L.DELTA, "T4"), ("levy_ak", L.LEVY_AK, "post"),
    ("ls_rent_low", L.LS_RENT["low"], "paper's 30% flow measure"), ("ls_rent_mid", L.LS_RENT["mid"], "judgment"),
    ("ls_rent_high", L.LS_RENT["high"], "paper's 50% flow measure")]]
pd.DataFrame(inputs).to_csv(OUT / "us_lvt_inputs.csv", index=False, float_format="%.10g")

# %% step 1: the tax - bridge-equivalent phi for each base x measure, and full capture
rows = []
for base in ["L1", "L2"]:
    Ltot = INFO25[f"{base}_total_bn"]
    for mk, mname in MEAS.items():
        r = R[mk]
        phi_b = VAT_REV_BN / (r * Ltot)
        for rate, phi in [("bridge", phi_b), ("full", L.PHI_FULL)]:
            rev = phi * r * Ltot
            rows.append(dict(base=base, measure=mname, rate=rate, phi=phi, r=r, land_bn=Ltot, rent_bn=r * Ltot,
                             revenue_bn=rev, dividend_usd_month=rev * 1e9 / (S_CE * 12.0),
                             dividend_vs_vat=rev / VAT_REV_BN, feasible=phi <= L.PHI_FULL,
                             loss_frac_immediate=L.loss_fraction(phi, "immediate"),
                             capitalized_loss_bn=L.loss_fraction(phi, "immediate") * Ltot))
PHI = pd.DataFrame(rows)
PHI.to_csv(OUT / "us_lvt_phi.csv", index=False, float_format="%.10g")
pb = PHI[PHI["rate"] == "bridge"].pivot(index="measure", columns="base", values="phi")
pf = PHI[PHI["rate"] == "full"].pivot(index="measure", columns="base", values="dividend_usd_month")
print("\nstep 1, bridge-equivalent phi (dividend $%.2f):\n%s" % (DIV_VAT, pb.round(3).to_string()))
print("   full capture (phi = 0.98) dividend, $/share/month:\n" + pf.round(1).to_string())
assert (PHI.loc[PHI["rate"] == "bridge", "phi"] <= L.PHI_FULL).all()


def phi_of(rate, base, mk, info=INFO25):
    if rate == "full":
        return L.PHI_FULL
    return VAT_REV_BN / (R[mk] * info[f"{base}_total_bn"])


# %% step 2: land by household - calibration of s, the band, the rising-s variant, the decile profile
w25 = S25["WGT"]
s_nominal_2025 = L.z1_targets(2025)["L_hh"] * 1e9 / float((w25 * (S25["HOUSES"] + S25["ORESRE"]) * L.CPI_25_TO_24).sum())
S25r, INFO25r = L.land_holdings(s25, z1, s_rule="rising")
cal = pd.DataFrame([
    dict(item="s, uniform: Z.1 2024 household land / SCF 2025 property value in 2024 dollars (main)", value=INFO25["s_uniform"]),
    dict(item="s, uniform: Z.1 2025 household land / SCF 2025 property value in 2025 dollars", value=s_nominal_2025),
    dict(item="Z.1 2024 aggregate land / household real estate (HH+NPO)", value=z1["land_share_re"]),
    dict(item="Z.1 2024 owner-occupied land (households only) / owner-occupied real estate", value=z1["L_hh_ownocc"] / z1["re_ownocc"]),
    dict(item="s, uniform, SCF 2022 (real 2024 dollars) to Z.1 2024", value=INFO22["s_uniform"]),
    dict(item="SCF 2025 HOUSES + ORESRE, $bn 2024", value=INFO25["scf_property_total_bn"]),
    dict(item="Z.1 2024 HH+NPO real estate, $bn", value=z1["re_hh"]),
    dict(item="Z.1 2024 households' owner-occupied real estate, $bn", value=z1["re_ownocc"]),
    dict(item="SCF 2025 HOUSES, $bn 2024", value=float((w25 * S25["HOUSES"]).sum()) / 1e9),
    dict(item="SCF 2025 ORESRE, $bn 2024", value=float((w25 * S25["ORESRE"]).sum()) / 1e9),
    dict(item="rising s: scale k (raw rule 0.30 + 0.30 F(V) times k)", value=INFO25r["s_rising_scale"]),
    dict(item="rising s: effective range low", value=0.30 * INFO25r["s_rising_scale"]),
    dict(item="rising s: effective range high", value=0.60 * INFO25r["s_rising_scale"]),
    dict(item="land at s = 0.30 (fixed aggregate property value), $bn", value=0.30 * INFO25["scf_property_total_bn"]),
    dict(item="land at s = 0.60 (fixed aggregate property value), $bn", value=0.60 * INFO25["scf_property_total_bn"]),
])
cal.to_csv(OUT / "us_lvt_s_calibration.csv", index=False, float_format="%.10g")
print("\nstep 2, land share s:\n" + cal.round(4).to_string(index=False))

# decile profile of land and property, SCF 2025 vs CE 2024's own estimated market value of owned home
ce_home = m["vals"].loc["Addenda: > Other financial information: > Estimated market value of owned home", DEC].astype(float)
ce_own = m["vals"].loc["Percent distribution: > Housing tenure: > Homeowner", DEC].astype(float) / 100.0
N_ce = m["units"]["N_thousand"] * 1000.0
land_dec = pd.DataFrame({
    "scf_families_m": L.decile_sum(S25, np.ones(len(S25))) / 1e6,
    "scf_owner_rate": L.decile_sum(S25, S25["owner"]) / L.decile_sum(S25, np.ones(len(S25))),
    "ce_owner_rate": ce_own,
    "scf_houses_share": L.decile_sum(S25, S25["HOUSES"]) / float((w25 * S25["HOUSES"]).sum()),
    "ce_home_value_share": ce_home * N_ce / float((ce_home * N_ce).sum()),
    "scf_houses_per_family": L.decile_sum(S25, S25["HOUSES"]) / L.decile_sum(S25, np.ones(len(S25))),
    "ce_home_value_per_cu": ce_home,
    "L_own_share": L.decile_sum(S25, S25["L_own"]) / float((w25 * S25["L_own"]).sum()),
    "L_ore_share": L.decile_sum(S25, S25["L_ore"]) / float((w25 * S25["L_ore"]).sum()),
    "L1_share": L.decile_sum(S25, S25["L1"]) / float((w25 * S25["L1"]).sum()),
    "L_nnb_share": L.decile_sum(S25, S25["L_nnb"]) / float((w25 * S25["L_nnb"]).sum()),
    "L_nfc_share": L.decile_sum(S25, S25["L_nfc"]) / float((w25 * S25["L_nfc"]).sum()),
    "L2_share": L.decile_sum(S25, S25["L2"]) / float((w25 * S25["L2"]).sum()),
    "L1_rising_s_share": L.decile_sum(S25r, S25r["L1"]) / float((w25 * S25r["L1"]).sum()),
    "L1_scf2022_share": L.decile_sum(S22, S22["L1"]) / float((S22["WGT"] * S22["L1"]).sum()),
    "L2_scf2022_share": L.decile_sum(S22, S22["L2"]) / float((S22["WGT"] * S22["L2"]).sum()),
    "vatable_share": acc_v["vatable"] * m["w"] / float((acc_v["vatable"] * m["w"]).sum()),
    "budget_share": m["budget"] * m["w"] / m["budget_bar"],
    "c_d_2025": c25, "c_d_2022": c22, "ce_shares_per_cu": m["units"]["shares"],
    "scf_raw_shares_per_family": L.decile_sum(S25, S25["shares_raw"]) / L.decile_sum(S25, np.ones(len(S25)))})
land_dec.index.name = "decile"
land_dec.to_csv(OUT / "us_lvt_land_by_decile.csv", float_format="%.10g")
print("   decile shares (SCF HOUSES vs CE home value; L1, L2; VAT-able consumption):")
print(land_dec[["scf_houses_share", "ce_home_value_share", "L1_share", "L2_share", "vatable_share", "scf_owner_rate", "ce_owner_rate"]].round(3).T.to_string())

# %% step 3: incidence - decile-netted (the post's method) and household-level
# the income deciles are the Fed's pooled weighted percentile groups (INCPCTLECAT); recomputed here as a check
own_dec = L.weighted_decile(S25["INCOME"].values, S25["WGT"].values)
agree = float((S25["WGT"] * (own_dec == S25["decile"].values)).sum() / S25["WGT"].sum())
print(f"\nstep 3, income deciles: own weighted deciles of INCOME agree with INCPCTLECAT for {100 * agree:.2f}% of families (by weight)")
ACC, HH = {}, {}


def run_tax(rate, base, mk, S=S25, info=INFO25, tag=""):
    phi = phi_of(rate, base, mk, info)
    acc = L.lvt_accounting(m, S, base, phi, R[mk])
    h = L.lvt_household(S, base, phi, R[mk], float(acc["dividend"].iloc[0]))
    return phi, acc, h


for rate in ["bridge", "full"]:
    for base in ["L1", "L2"]:
        for mk in (["m1"] if rate == "bridge" else list(MEAS)):
            phi, acc, h = run_tax(rate, base, mk)
            key = f"LVT_{rate}_{base}_{mk}"
            ACC[key], HH[key] = (phi, acc), h
HV = L.vat_household(m, S25, acc_v)
rows = []
for d in DEC:
    rows.append(dict(scenario="VAT", decile=d, phi=np.nan, dividend=DIV_VAT, bill=acc_v.loc[d, "tax"], net=acc_v.loc[d, "net"],
                     net_pct_budget=acc_v.loc[d, "net_pct_budget"], budget=m["budget"][d], base_share=np.nan))
for key, (phi, acc) in ACC.items():
    for d in DEC:
        rows.append(dict(scenario=key, decile=d, phi=phi, dividend=acc.loc[d, "dividend"], bill=acc.loc[d, "bill"],
                         net=acc.loc[d, "net"], net_pct_budget=acc.loc[d, "net_pct_budget"], budget=acc.loc[d, "budget"],
                         base_share=acc.loc[d, "land_share"]))
inc = pd.DataFrame(rows)
inc.to_csv(OUT / "us_lvt_accounting_by_decile.csv", index=False, float_format="%.10g")
wide = inc.pivot(index="scenario", columns="decile", values="net")[DEC]
print("\nstep 3, net per adult share per month by decile:\n" + wide.round(1).to_string())
assert all(abs(float((m["w"] * a["net"]).sum())) < 1e-9 for _, a in ACC.values())

# household level: who pays, distribution of net per share
WHO = [L.who_pays(S25, HV, HTM["biweekly"], "VAT (household, TOTSPENDNH split)")]
for key in ["LVT_bridge_L1_m1", "LVT_bridge_L2_m1", "LVT_full_L1_m1", "LVT_full_L2_m1"]:
    WHO.append(L.who_pays(S25, HH[key], HTM["biweekly"], key))
who = pd.concat(WHO, ignore_index=True)
who.to_csv(OUT / "us_lvt_who_pays.csv", index=False, float_format="%.10g")
print("   share of families that are net payers, by decile:")
print(who.pivot(index="scenario", columns="dec", values="payer_share")[DEC + ["all"]].round(3).to_string())
wl1 = who[who["scenario"] == "LVT_bridge_L1_m1"].set_index("dec")
print("   LVT bridge L1: payers who are owners / 65+ / HtM / wealthy HtM; payments by owners 65+:")
print(wl1[["payers_owner_share", "payers_age65_share", "payers_htm_share", "payers_whtm_share", "payments_owner65_share",
           "payments_htm_share"]].round(3).T.to_string())

# %% step 4: MPC grades
fe = S25.groupby("NINCPCTLECAT").apply(lambda q: np.average(q["MPSPEND"], weights=q["WGT"]), include_groups=False)
FEDS = pd.Series([28.3, 25.0, 24.9, 23.7, 22.7, 19.4, 20.5, 19.8, 19.2, 22.2, 18.4, 14.0], index=range(1, 13))   # FEDS note Fig 3
grades = pd.DataFrame({"post_mid": SCHED["mid"], "post_low": SCHED["low"], "post_high": SCHED["high"],
                       "post_monotone_diag": SCHED["mono"], "measured_windfall": MEAS_D,
                       "measured_windfall_shape_d1_1": MEAS_D / MEAS_D.iloc[0]})
mdh = MEAS_DH.pivot(index="dec", columns="htm", values="mpc").rename(columns={0: "measured_not_htm", 1: "measured_htm"})
grades = grades.join(mdh)
for b in L.HTM_DIVISOR:
    grades[f"htm_share_{b}"] = L.decile_sum(S25, HTM[b]["htm"]) / L.decile_sum(S25, np.ones(len(S25)))
    grades[f"whtm_share_{b}"] = L.decile_sum(S25, HTM[b]["whtm"]) / L.decile_sum(S25, np.ones(len(S25)))
grades.index.name = "decile"
grades.to_csv(OUT / "us_lvt_mpc_grades.csv", float_format="%.10g")
feds_chk = pd.DataFrame({"scf_public_extract": fe.reindex(FEDS.index), "feds_note_fig3": FEDS})
feds_chk["gap_pp"] = feds_chk["scf_public_extract"] - feds_chk["feds_note_fig3"]
feds_chk.index.name = "NINCPCTLECAT"
feds_chk.to_csv(OUT / "us_lvt_feds_mpc_check.csv", float_format="%.10g")
print("\nstep 4, MPC grades by decile:\n" + grades.round(3).T.to_string())
print(f"   SCF windfall MPC by usual-income group vs the Fed's FEDS note Fig 3: max gap {feds_chk['gap_pp'].abs().max():.2f} pp; "
      f"overall {np.average(S25['MPSPEND'], weights=w25):.2f}% (note: 22.35)")




# %% flow impulse machinery: one function for every grade x deferral
def defer_mask(kind, S=S25, htm=None):
    """Who defers the primary-residence bill: 'own65' owners aged 65+; 'whtm_owners' wealthy hand-to-mouth owners
    (any age). Full take-up of the eligible (judgment; US property-tax deferral take-up is low, and every flow is
    linear in take-up, so a take-up of x moves the result x of the way from 'none')."""
    htm = HTM["biweekly"] if htm is None else htm
    base = kind.replace("_cash", "")
    if base == "none":
        return np.zeros(len(S))
    if base == "own65":
        return ((S["owner"] == 1) & (S["age65"] == 1)).values.astype(float)
    if base == "whtm_owners":
        return ((S["owner"] == 1) & (htm["whtm"] == 1)).values.astype(float)
    raise ValueError(kind)


def cash_flows(h, defer="none", S=S25, htm=None, nonocc=None):
    """Monthly cash net per family. Deferral 'X': the deferred bills accrue as liens and the dividend is still paid
    in full (the state lends the deferred bills: the program is balanced on accrual, not on cash). 'X_cash': the
    dividend is cut to the cash revenue (cash-balanced). nonocc = mpw: the non-occupier bills are removed from the
    cash net and replaced by a wealth effect mpw x capitalized loss (returned as `extra`)."""
    dm = defer_mask(defer, S, htm)
    deferred = h["bill_L_own"].values * dm if "bill_L_own" in h else np.zeros(len(h))
    w = S["WGT"].values
    k = 1.0
    if defer.endswith("_cash") and deferred.any():
        k = 1.0 - float((w * deferred).sum()) / float((w * h["div"].values).sum())
    cash = k * h["div"].values - h["bill"].values + deferred
    extra = np.zeros(len(h))
    if nonocc is not None:
        cash = cash + h["bill_nonocc"].values
        extra = -nonocc * h["loss_nonocc"].values / 12.0
    return cash, extra, k, float((w * deferred).sum())


GRADES_DN = {"dn_mid": SCHED["mid"], "dn_low": SCHED["low"], "dn_high": SCHED["high"], "dn_mono": SCHED["mono"],
             "dn_meas": MEAS_D, "dn_measshape": MEAS_D / MEAS_D.iloc[0]}
GRADES_HH = {"hh_mid": ("mid", "biweekly"), "hh_liq_mid": ("liq_mid", "biweekly"), "hh_liq_low": ("liq_low", "biweekly"),
             "hh_liq_high": ("liq_high", "biweekly"), "hh_liq_mono": ("liq_mono", "biweekly"),
             "hh_liq_mid_monthly": ("liq_mid", "monthly"), "hh_liqsym_mid": ("liqsym_mid", "biweekly"),
             "hh_meas_htm": ("meas_htm", "biweekly")}
GRADE_LABEL = {"dn_mid": "post mid schedule, decile-netted (the post's method)", "dn_low": "post low schedule, decile-netted",
               "dn_high": "post high schedule, decile-netted", "dn_mono": "monotone diagnostic schedule, decile-netted",
               "dn_meas": "measured windfall MPC by decile (SCF 2025), decile-netted",
               "dn_measshape": "measured windfall shape, scaled to 1.0 at D1, decile-netted",
               "hh_mid": "post mid, household level (equals decile-netted without deferral)",
               "hh_liq_mid": "recipients mid; payers 1.0 if hand-to-mouth (biweekly), else mid",
               "hh_liq_low": "as hh_liq_mid with the low schedule", "hh_liq_high": "as hh_liq_mid with the high schedule",
               "hh_liq_mono": "as hh_liq_mid with the monotone diagnostic schedule",
               "hh_liq_mid_monthly": "as hh_liq_mid, hand-to-mouth on the monthly band",
               "hh_liqsym_mid": "1.0 for every hand-to-mouth family (recipient or payer), else mid",
               "hh_meas_htm": "measured windfall MPC by decile x hand-to-mouth cell"}


def flow_dC(h, grade, defer="none", S=S25, acc_net=None, htm_sets=None, meas_dh=MEAS_DH, nonocc=None):
    """Household dC_i (monthly, per family) under a grade. Decile-netted grades apply mpc_d to the decile's cash net
    (returned as per-share dC_d with dC_i=None); household grades apply mpc_i to each family's cash net."""
    htm_sets = HTM if htm_sets is None else htm_sets
    cash, extra, k, D = cash_flows(h, defer, S, htm_sets["biweekly"], nonocc)
    if grade in GRADES_DN:
        cash_d = L.household_to_decile(m, S, cash)
        dC_d = GRADES_DN[grade].reindex(DEC).values * cash_d + L.household_to_decile(m, S, extra)
        return None, dC_d, k, D
    rule, band = GRADES_HH[grade]
    mpc = L.household_mpc(rule, S, cash, htm_sets[band], SCHED, meas_dh)
    dC = mpc * cash + extra
    return dC, L.household_to_decile(m, S, dC), k, D


def flow_shock(h, grade, defer="none", S=S25, **kw):
    _, dC_d, _, _ = flow_dC(h, grade, defer, S, **kw)
    return (dC_d / m["budget"]).rename("shock")


def residual_wealth(phi, defer, mpw, S=S25):
    """Annual wealth-effect response of deferring owners to their capitalized land loss, % of CE consumption
    (reported beside the flow, never added to it)."""
    loss = L.loss_fraction(phi) * S["L_own"].values * defer_mask(defer, S)
    return -100.0 * mpw * float((S["WGT"] * loss).sum()) / (C_TOT_BN * 1e9)


for key in HH:
    phi = ACC[key][0]
    base = key.split("_")[2]
    HH[key]["loss_nonocc"] = L.loss_fraction(phi) * S25[L.NONOCC_COLS[base]].sum(axis=1).values
# identity: the household-level twin of the decile-netted grade, without deferral, is the decile-netted result
for key in ["LVT_bridge_L1_m1", "LVT_full_L2_m1"]:
    a = flow_shock(HH[key], "dn_mid")
    b = flow_shock(HH[key], "hh_mid")
    assert np.allclose(a.values, b.values, atol=1e-12) and np.allclose(a.values, (SCHED["mid"].values * ACC[key][1]["net"] / m["budget"]).values)
assert np.allclose(flow_shock(HV, "dn_mid").values, B.budget_shock(acc_v["net"], SCHED["mid"].values, m["budget"]).values)

# %% step 6(ii): the flow impulse grid (rate x base x measure x grade x deferral)
DEFERS = ["none", "own65", "own65_cash", "whtm_owners", "whtm_owners_cash"]
rows = []
for grade in list(GRADES_DN) + list(GRADES_HH):
    ii = B.impulse(m, shock=flow_shock(HV, grade))
    rows.append(dict(tax="VAT", rate="", base="", measure="", phi=np.nan, grade=grade, defer="none",
                     impulse_pct=ii["flow_pct_consumption"], impulse_usd=ii["flow_usd"], dividend_scale=1.0,
                     deferred_share_of_revenue=0.0, residual_wealth_pct_mid=0.0, residual_wealth_pct_high=0.0))
for key in tqdm(list(HH), desc="flow impulse grid", leave=False):
    phi, acc = ACC[key]
    _, rate, base, mk = key.split("_")
    rev_month = float(acc["revenue_bn"].iloc[0]) * 1e9 / 12.0
    for grade in list(GRADES_DN) + list(GRADES_HH):
        for defer in DEFERS:
            _, dC_d, k, D = flow_dC(HH[key], grade, defer)
            ii = B.impulse(m, shock=dC_d / m["budget"])
            rows.append(dict(tax="LVT", rate=rate, base=base, measure=MEAS[mk], phi=phi, grade=grade, defer=defer,
                             impulse_pct=ii["flow_pct_consumption"], impulse_usd=ii["flow_usd"], dividend_scale=k,
                             deferred_share_of_revenue=D / rev_month,
                             residual_wealth_pct_mid=residual_wealth(phi, defer, L.MPW["mid"]),
                             residual_wealth_pct_high=residual_wealth(phi, defer, L.MPW["high"])))
IMP = pd.DataFrame(rows)
IMP["grade_label"] = IMP["grade"].map(GRADE_LABEL)
IMP.to_csv(OUT / "us_lvt_impulse.csv", index=False, float_format="%.10g")
v_mid = float(IMP[(IMP["tax"] == "VAT") & (IMP["grade"] == "dn_mid")]["impulse_pct"].iloc[0])
assert abs(v_mid - B.impulse(m, acc_v["net"], SCHED["mid"].values)["flow_pct_consumption"]) < 1e-9
show = IMP[(IMP["defer"] == "none") & ((IMP["tax"] == "VAT") | (IMP["measure"] == MEAS["m1"]))]
piv = show.assign(sc=show["tax"] + " " + show["rate"] + " " + show["base"]).pivot(index="sc", columns="grade", values="impulse_pct")
print("\nstep 6(ii), flow impulse at impact, % of consumption (LVT on measure m1; bridge-rate flows do not depend on the measure):")
print(piv[["dn_mid", "dn_low", "dn_high", "dn_mono", "hh_liq_mid", "hh_liq_low", "hh_liq_high", "hh_liq_mid_monthly",
           "hh_liqsym_mid", "dn_meas", "dn_measshape", "hh_meas_htm"]].round(3).to_string())
dsub = IMP[(IMP["tax"] == "LVT") & (IMP["measure"] == MEAS["m1"]) & IMP["grade"].isin(["dn_mid", "hh_liq_mid"])]
print("   deferral variants (m1); deferred share of revenue; residual wealth effect of deferrers at 3.5c (% of consumption):")
print(dsub.assign(sc=dsub["rate"] + " " + dsub["base"] + " " + dsub["grade"]).pivot(index="sc", columns="defer", values="impulse_pct")[DEFERS].round(3).to_string())
print(dsub[dsub["grade"] == "dn_mid"].assign(sc=lambda d: d["rate"] + " " + d["base"]).pivot(
    index="sc", columns="defer", values="deferred_share_of_revenue")[DEFERS].round(3).to_string())
print(dsub[dsub["grade"] == "dn_mid"].assign(sc=lambda d: d["rate"] + " " + d["base"]).pivot(
    index="sc", columns="defer", values="residual_wealth_pct_mid")[DEFERS].round(3).to_string())

# %% step 5: demand shifts by category - decile-netted (the post's method), household level, and tenure-aware
# baskets (household level, the structural housing lines split by tenure inside each decile; an extension)
TM = L.tenure_model(m, ce_own.values)
CH = m["chart"]


def demand_versions(h, net_d, label):
    """Category $ and % per share per month in three versions for one instrument."""
    out = {}
    dn = B.shifts_from_transfers(m, net_d, mpc=SCHED["mid"].values)
    out[f"{label}|decile_netted"] = dn["dUSD_mpc"]
    out[f"{label}|ghost_mpc1"] = dn["dUSD_mpc1"]
    dC_i, dC_d, _, _ = flow_dC(h, "hh_liq_mid")
    out[f"{label}|household_liq"] = B.shifts_from_transfers(m, None, shock=dC_d / m["budget"])["dUSD_mpc"]
    out[f"{label}|household_liq_tenure"] = L.shifts_tenure_aware(m, S25, dC_i, TM)
    return out


DS = {}
DS.update(demand_versions(HV, acc_v["net"], "VAT"))
for key in ["LVT_bridge_L1_m1", "LVT_bridge_L2_m1", "LVT_full_L1_m1", "LVT_full_L2_m1"]:
    DS.update(demand_versions(HH[key], ACC[key][1]["net"], key))
dsh = pd.DataFrame(DS)
dsh.insert(0, "Cbar", m["Cbar"])
dsh.insert(0, "role", m["prov"]["role"])
for c in [c for c in dsh.columns if "|" in c]:
    dsh[c.replace("|", "|pct|")] = 100.0 * dsh[c] / dsh["Cbar"]
dsh.index.name = "category"
dsh.to_csv(OUT / "us_lvt_demand_shifts.csv", float_format="%.10g")
# identity: the VAT decile-netted column is the rebuild's Fig 5
reb = pd.read_csv(B.REBUILD / "out" / "us_demand_shifts.csv", index_col=0)
assert np.allclose(dsh.loc[CH, "VAT|decile_netted"].values, reb.loc[CH, "dUSD_mid"].values, atol=1e-5)
# Engel aggregation of the tenure-aware version (sum of all bars vs the flow)
for lab in ["VAT", "LVT_bridge_L1_m1"]:
    hh = HV if lab == "VAT" else HH[lab]
    dC_i, dC_d, _, _ = flow_dC(hh, "hh_liq_mid")
    flow_usd = float((m["w"] * dC_d).sum())
    print(f"   {lab}: household flow ${flow_usd:.3f}/share/month; sum of tenure-aware bars ${dsh[lab + '|household_liq_tenure'].sum():.3f}; "
          f"sum of household bars ${dsh[lab + '|household_liq'].sum():.3f}")

# category comparison, VAT vs LVT (bridge-equivalent, L1, decile-netted): sign and size, and the decile sources
cmp_rows = []
dec_v = B.decompose(m, B.budget_shock(acc_v["net"], SCHED["mid"].values, m["budget"]))
dec_l = B.decompose(m, B.budget_shock(ACC["LVT_bridge_L1_m1"][1]["net"], SCHED["mid"].values, m["budget"]))
dec_l2 = B.decompose(m, B.budget_shock(ACC["LVT_bridge_L2_m1"][1]["net"], SCHED["mid"].values, m["budget"]))
imp_v = float(dsh.loc[:, "VAT|decile_netted"].sum())
imp_l = float(dsh.loc[:, "LVT_bridge_L1_m1|decile_netted"].sum())
for c in CH:
    v, l1, l2 = dsh.loc[c, "VAT|decile_netted"], dsh.loc[c, "LVT_bridge_L1_m1|decile_netted"], dsh.loc[c, "LVT_bridge_L2_m1|decile_netted"]
    lt = dsh.loc[c, "LVT_bridge_L1_m1|household_liq_tenure"]
    vt = dsh.loc[c, "VAT|household_liq_tenure"]
    cmp_rows.append(dict(category=c, vat=v, lvt_L1=l1, lvt_L2=l2, vat_tenure=vt, lvt_L1_tenure=lt,
                         ratio_L1_vat=l1 / v if abs(v) > 1e-9 else np.nan, same_sign_L1=np.sign(v) == np.sign(l1),
                         same_sign_L2=np.sign(v) == np.sign(l2), same_sign_tenure=np.sign(vt) == np.sign(lt),
                         vat_share_of_impulse=v / imp_v, lvt_share_of_impulse=l1 / imp_l,
                         vat_withdrawal_d8_d10=float(dec_v.loc[c, ["d08", "d09", "d10"]].clip(upper=0).sum()),
                         lvt_withdrawal_d9_d10=float(dec_l.loc[c, ["d09", "d10"]].clip(upper=0).sum()),
                         vat_additions=float(dec_v.loc[c].clip(lower=0).sum()), lvt_additions=float(dec_l.loc[c].clip(lower=0).sum()),
                         vat_ghost=dsh.loc[c, "VAT|ghost_mpc1"], lvt_ghost=dsh.loc[c, "LVT_bridge_L1_m1|ghost_mpc1"]))
CMP = pd.DataFrame(cmp_rows).set_index("category")
CMP["abs_max"] = CMP[["vat", "lvt_L1", "lvt_L2", "lvt_L1_tenure"]].abs().max(axis=1)
CMP = CMP.sort_values("abs_max", ascending=False)
CMP.to_csv(OUT / "us_lvt_demand_compare.csv", float_format="%.10g")
print("\nstep 5, demand shifts ($/share/month), the 15 largest movers across VAT and LVT (bridge-equivalent rate):")
print(CMP.head(15)[["vat", "lvt_L1", "lvt_L2", "vat_tenure", "lvt_L1_tenure", "ratio_L1_vat", "vat_share_of_impulse",
                    "lvt_share_of_impulse"]].round(3).to_string())
# Fig 6 analog: the ten largest movers decomposed by decile, VAT and LVT (bridge, L1 and L2), decile-netted, mid MPC
dec_rows = []
for lab, dmat, col in [("VAT", dec_v, "vat"), ("LVT_bridge_L1_m1", dec_l, "lvt_L1"), ("LVT_bridge_L2_m1", dec_l2, "lvt_L2")]:
    top10 = B.top_movers(dsh.rename(columns={f"{lab}|decile_netted": "x"}), "x", CH, 10)
    for rk, c in enumerate(top10, 1):
        for d in DEC:
            dec_rows.append(dict(scenario=lab, rank=rk, category=c, decile=d, contrib=float(dmat.loc[c, d])))
        dec_rows.append(dict(scenario=lab, rank=rk, category=c, decile="net", contrib=float(dmat.loc[c].sum())))
pd.DataFrame(dec_rows).to_csv(OUT / "us_lvt_decomposition_top10.csv", index=False, float_format="%.10g")
print(f"   sign kept VAT -> LVT L1 on {int(CMP['same_sign_L1'].sum())}/{len(CMP)} charted bars, L2 {int(CMP['same_sign_L2'].sum())}, "
      f"tenure-aware {int(CMP['same_sign_tenure'].sum())}; flips (L1): {list(CMP.index[~CMP['same_sign_L1']])}")

# %% step 6(i)-(ii): the stock channel - capitalization, collateral, non-occupiers, the VAT levy beside it
SHOCK_T = pd.read_csv(L.SHOCK_FILE)
DESIGNS = ["immediate", "phasein_5y", "phasein_10y", "phasein_20y", "phasein_30y", "increment"]
cap_rows = []
for key in ["LVT_bridge_L1_m1", "LVT_bridge_L2_m1", "LVT_full_L1_m1", "LVT_full_L2_m1"]:
    phi = ACC[key][0]
    base = key.split("_")[2]
    for mk in MEAS:
        ph = phi_of(key.split("_")[1], base, mk)
        for dsg in DESIGNS:
            lf = L.loss_fraction(ph, dsg, SHOCK_T)
            cap_rows.append(dict(scenario=key.rsplit("_", 1)[0], measure=MEAS[mk], phi=ph, design=dsg, loss_fraction=lf,
                                 land_loss_bn=lf * INFO25[f"{base}_total_bn"],
                                 owner_occupied_loss_bn=lf * float((w25 * S25["L_own"]).sum()) / 1e9,
                                 nonoccupier_loss_bn=lf * float((w25 * S25[L.NONOCC_COLS[base]].sum(axis=1)).sum()) / 1e9))
CAP = pd.DataFrame(cap_rows).drop_duplicates(["scenario", "measure", "design"])
CAP.to_csv(OUT / "us_lvt_capitalization.csv", index=False, float_format="%.10g")
print("\nstep 6, capitalization at announcement (share of land value lost; m1):")
print(CAP[CAP["measure"] == MEAS["m1"]].pivot(index="scenario", columns="design", values="loss_fraction")[DESIGNS].round(3).to_string())

# collateral: LTVs of mortgaged owners and the threshold crossers
col_rows, LTVS = [], []
for key in ["LVT_bridge_L1", "LVT_bridge_L2", "LVT_full_L1"]:
    for mk in MEAS:
        rate, base = key.split("_")[1], key.split("_")[2]
        ph = phi_of(rate, base, mk)
        for dsg in ["immediate", "phasein_10y", "increment"]:
            lf = L.loss_fraction(ph, dsg, SHOCK_T)
            f, summ, agg = L.collateral(S25, lf)
            LTVS.append(dict(scenario=key, measure=MEAS[mk], phi=ph, design=dsg, loss_fraction=lf, **agg))
            for _, r in summ.iterrows():
                d = r.to_dict()
                for kk, v in L.MPC_COLL.items():
                    d[f"dC_lost_equity_{kk}_pct"] = -100.0 * v * d["lost_equity_crossers_bn"] / C_TOT_BN
                    d[f"dC_lost_capacity_{kk}_pct"] = -100.0 * v * d["lost_capacity_crossers_bn"] / C_TOT_BN
                col_rows.append(dict(scenario=key, measure=MEAS[mk], phi=ph, design=dsg, loss_fraction=lf, **d))
COLL = pd.DataFrame(col_rows)
COLL.to_csv(OUT / "us_lvt_collateral.csv", index=False, float_format="%.10g")
LTV = pd.DataFrame(LTVS)
LTV.to_csv(OUT / "us_lvt_ltv.csv", index=False, float_format="%.10g")
# collateral crossers by decile for the main case (bridge L1 m1, immediate, 80%)
f_main, _, _ = L.collateral(S25, L.loss_fraction(phi_of("bridge", "L1", "m1")))
coll_dec = pd.DataFrame({"crossers_share_of_families": L.decile_sum(S25, f_main["cross_0.80"]) / L.decile_sum(S25, np.ones(len(S25))),
                         "lost_equity_bn": L.decile_sum(S25, f_main["loss"] * f_main["cross_0.80"]) / 1e9})
print(f"   aggregate LTV (SCF owners): {LTV.iloc[0]['ltv_aggregate_before']:.3f} before; after full capture (immediate, m1): "
      f"{LTV[(LTV['scenario'] == 'LVT_full_L1') & (LTV['design'] == 'immediate') & (LTV['measure'] == MEAS['m1'])]['ltv_aggregate_after'].iloc[0]:.3f} "
      f"(memo 7.1 on Z.1 aggregates: 26% -> 48%; Z.1 2024 mortgages / HH real estate {z1['mortg'] / z1['re_hh']:.3f})")
cm = COLL[(COLL["measure"] == MEAS["m1"])]
print("   threshold crossers (millions) and collateral response at 4.7 / 6 / 10 cents, % of consumption (m1):")
print(cm[["scenario", "design", "threshold", "n_cross_m", "share_of_mortgaged", "lost_equity_crossers_bn", "lost_capacity_crossers_bn",
          "dC_lost_equity_low_pct", "dC_lost_equity_mid_pct", "dC_lost_equity_high_pct", "dC_lost_capacity_mid_pct"]].round(3).to_string(index=False))

# non-occupying holders: the flow (bill x MPC) OR a wealth effect on the capitalized loss, never both
no_rows = []
for key in ["LVT_bridge_L1_m1", "LVT_bridge_L2_m1", "LVT_full_L1_m1", "LVT_full_L2_m1"]:
    for grade in ["dn_mid", "hh_liq_mid"]:
        base_imp = B.impulse(m, shock=flow_shock(HH[key], grade))["flow_pct_consumption"]
        rowd = dict(scenario=key, grade=grade, flow_version_pct=base_imp)
        for kk, v in L.MPW.items():
            rowd[f"wealth_version_{kk}_pct"] = B.impulse(m, shock=flow_shock(HH[key], grade, nonocc=v))["flow_pct_consumption"]
        rowd["nonocc_bill_bn"] = float((w25 * HH[key]["bill_nonocc"]).sum()) * 12 / 1e9
        rowd["nonocc_capitalized_loss_bn"] = float((w25 * HH[key]["loss_nonocc"]).sum()) / 1e9
        no_rows.append(rowd)
NONOCC = pd.DataFrame(no_rows)
NONOCC.to_csv(OUT / "us_lvt_nonoccupier.csv", index=False, float_format="%.10g")
print("   non-occupying holders, flow version vs wealth-effect version (2 / 3.5 / 5 cents), impulse % of consumption:")
print(NONOCC.round(3).to_string(index=False))

# the VAT's levy channel, impact version on the same SCF balance sheets
LEVY = L.vat_levy_impact(m, S25)
LEVY["pct_pce"] = 100.0 * LEVY["dC_bn"] / PCE_BN
LEVY.to_csv(OUT / "us_lvt_vat_levy.csv", index=False, float_format="%.10g")
nw_tot = float((w25 * S25["NETWORTH"]).sum()) / 1e9
print(f"   VAT levy channel (impact): SCF 2025 net worth ${nw_tot:,.0f}bn (2024 $) = {nw_tot / C_TOT_BN:.1f}x CE consumption, "
      f"{nw_tot / PCE_BN:.1f}x PCE; 8% levy = ${0.08 * nw_tot:,.0f}bn")
print(LEVY.pivot(index="lam", columns="mpw", values="pct_ce_consumption")[["low", "mid", "high"]].round(3).to_string())

# %% step 7: the loop - the dividend's rent bar raises land rent; the LVT taxes it back, the VAT leaves it to landlords
key_L1 = L.decile_sum(S25, S25["L_ore"]) / float((w25 * S25["L_ore"]).sum())
key_L2 = L.decile_sum(S25, S25["L_ore"] + S25["L_nnb"]) / float((w25 * (S25["L_ore"] + S25["L_nnb"])).sum())
loop_rows, LOOP_ROUNDS = [], []
for key in ["LVT_bridge_L1_m1", "LVT_bridge_L2_m1", "LVT_full_L1_m1", "LVT_full_L2_m1"]:
    phi, acc = ACC[key]
    kshare = key_L1 if "_L1_" in key else key_L2
    shock0 = B.budget_shock(acc["net"], SCHED["mid"].values, m["budget"])
    for lk, ls in L.LS_RENT.items():
        tot, rr, q = L.loop_fixed_point(m, shock0, phi, ls, kshare, SCHED["mid"].values)
        R0 = L.rent_bar(m, shock0)
        closed = phi * ls * R0 / (1.0 - phi * ls * q)
        loop_rows.append(dict(scenario=key, ls=lk, ls_value=ls, phi=phi, rent_bar_round0=R0, rounds=len(rr),
                              extra_dividend=tot, extra_pct_of_dividend=100.0 * tot / float(acc["dividend"].iloc[0]),
                              q_rent_bar_per_dollar=q, closed_form=closed, gross_multiplier_T5=1.0 / (1.0 - phi * ls * q)))
        if lk == "mid":
            LOOP_ROUNDS.append(rr.assign(scenario=key))
# tenure-aware round 0 (the rent bar that sees renters' baskets)
for key in ["LVT_bridge_L1_m1"]:
    phi, acc = ACC[key]
    R0t = float(dsh.loc["Rented dwellings", key + "|household_liq_tenure"])
    loop_rows.append(dict(scenario=key + " (tenure-aware round-0 rent bar)", ls="mid", ls_value=L.LS_RENT["mid"], phi=phi,
                          rent_bar_round0=R0t, rounds=1, extra_dividend=phi * L.LS_RENT["mid"] * R0t,
                          extra_pct_of_dividend=100.0 * phi * L.LS_RENT["mid"] * R0t / float(acc["dividend"].iloc[0]),
                          q_rent_bar_per_dollar=np.nan, closed_form=np.nan, gross_multiplier_T5=np.nan))
# the VAT: the same increment goes to landlords; capitalized at r and allocated to holders of rental land
R0v = L.rent_bar(m, B.budget_shock(acc_v["net"], SCHED["mid"].values, m["budget"]))
for lk, ls in L.LS_RENT.items():
    for mk in MEAS:
        gain_flow = ls * R0v * 12.0 * S_CE / 1e9
        loop_rows.append(dict(scenario="VAT", ls=lk, ls_value=ls, phi=0.0, rent_bar_round0=R0v, rounds=0, extra_dividend=0.0,
                              extra_pct_of_dividend=0.0, landlord_rent_gain_bn=gain_flow, r=R[mk], measure=MEAS[mk],
                              landlord_value_gain_bn=gain_flow / R[mk]))
LOOP = pd.DataFrame(loop_rows)
LOOP.to_csv(OUT / "us_lvt_loop.csv", index=False, float_format="%.10g")
pd.concat(LOOP_ROUNDS).to_csv(OUT / "us_lvt_loop_rounds.csv", index=False, float_format="%.10g")
gain_dec = pd.DataFrame({"rental_land_share_L1_key": key_L1, "rental_land_share_L2_key": key_L2,
                         "vat_landlord_value_gain_bn_L1_key_m1_mid": key_L1 * L.LS_RENT["mid"] * R0v * 12 * S_CE / 1e9 / R["m1"],
                         "vat_landlord_value_gain_bn_L2_key_m1_mid": key_L2 * L.LS_RENT["mid"] * R0v * 12 * S_CE / 1e9 / R["m1"]})
gain_dec.index.name = "decile"
gain_dec.to_csv(OUT / "us_lvt_loop_landlord_gain_by_decile.csv", float_format="%.10g")
print("\nstep 7, the loop:")
print(LOOP[LOOP["scenario"] != "VAT"][["scenario", "ls", "phi", "rent_bar_round0", "extra_dividend", "extra_pct_of_dividend",
                                       "q_rent_bar_per_dollar", "gross_multiplier_T5"]].round(4).to_string(index=False))
vv = LOOP[(LOOP["scenario"] == "VAT")]
print("   VAT: landlord land-rent gain $bn/yr and capitalized value gain $bn by measure (ls mid):")
print(vv[vv["ls"] == "mid"][["measure", "landlord_rent_gain_bn", "r", "landlord_value_gain_bn"]].round(2).to_string(index=False))
print("   who holds it (L1 key, rental land = other residential real estate): " +
      ", ".join(f"{d} {100 * v:.0f}%" for d, v in key_L1.items()))

# %% robustness: the land distribution, the survey year, the land concept, the NFC assumption, the s band
def headline(label, S, info, z1v, rate="bridge", mk="m1", htm_sets=None, note=""):
    """Headline numbers for one land variant: phi, dividend, nets by decile, break-even, payer share, impulses,
    collateral (immediate, 80% threshold, lost equity at the mid response)."""
    htm_sets = HTM if htm_sets is None else htm_sets
    out = []
    for base in ["L1", "L2"]:
        phi = VAT_REV_BN / (R[mk] * info[f"{base}_total_bn"]) if rate == "bridge" else L.PHI_FULL
        acc = L.lvt_accounting(m, S, base, phi, R[mk])
        h = L.lvt_household(S, base, phi, R[mk], float(acc["dividend"].iloc[0]))
        net = acc["net"]
        _, sum_c, _ = L.collateral(S, L.loss_fraction(phi))
        c80 = sum_c[sum_c["threshold"] == 0.80].iloc[0]
        d = dict(variant=label, base=base, rate=rate, measure=MEAS[mk], phi=phi, dividend=float(acc["dividend"].iloc[0]),
                 land_total_bn=info[f"{base}_total_bn"], top_decile_land_share=float(acc["land_share"]["d10"]),
                 deciles_gaining=int((net > 0).sum()), payer_share=float((S["WGT"] * (h["net"] < 0)).sum() / S["WGT"].sum()),
                 impulse_dn_mid=B.impulse(m, net, SCHED["mid"].values)["flow_pct_consumption"],
                 impulse_hh_liq_mid=B.impulse(m, shock=flow_shock(h, "hh_liq_mid", S=S, htm_sets=htm_sets))["flow_pct_consumption"],
                 collateral_cross80_m=float(c80["n_cross_m"]),
                 collateral_mid_pct=-100.0 * L.MPC_COLL["mid"] * float(c80["lost_equity_crossers_bn"]) / C_TOT_BN, note=note)
        d.update({f"net_{dd}": float(net[dd]) for dd in DEC})
        out.append(d)
    return out


rob = []
rob += headline("main: SCF 2025, uniform s calibrated to Z.1 2024", S25, INFO25, z1)
rob += headline("SCF 2022 (real 2024 dollars), uniform s calibrated to Z.1 2024", S22, INFO22, z1,
                htm_sets={"biweekly": HTM22, "monthly": L.htm_flags(S22, "monthly")})
rob += headline("SCF 2025, s rising with home value (0.30-0.60 rule, rescaled to Z.1)", S25r, INFO25r, z1)
for sv in L.S_BAND:
    Sx, Ix = L.land_holdings(s25, z1, s_level=sv)
    rob += headline(f"SCF 2025, uniform s = {sv:.2f} (aggregate property value fixed; land = s x SCF property)", Sx, Ix, z1)
z1o = dict(z1, L_hh=z1["L_hh_ownocc"])
Sx, Ix = L.land_holdings(s25, z1o)
rob += headline("household land = Z.1 households-only owner-occupied residual (19.4tn; NPO structures and land out)", Sx, Ix, z1o)
for rule in ["structures_proxy", "share_2020"]:
    zz = L.z1_targets(nfc_rule=rule)
    Sx, Ix = L.land_holdings(s25, zz)
    rob += [r for r in headline(f"NFC land rule: {rule} ({zz['L_nfc']:,.0f}bn)", Sx, Ix, zz) if r["base"] == "L2"]
Sx, Ix = L.land_holdings(s25, z1, nnb_key=("NNRESRE", "BUS", "ORESRE"))
rob += [r for r in headline("noncorporate land key adds ORESRE (Z.1 books household rental property in NNB)", Sx, Ix, z1) if r["base"] == "L2"]
Sx, Ix = L.land_holdings(s25, z1, nnb_key=("NNRESRE", "ACTBUS"))
rob += [r for r in headline("noncorporate land key: NNRESRE + actively managed businesses only", Sx, Ix, z1) if r["base"] == "L2"]
for rate in ["full"]:
    rob += headline("main, full capture (phi = 0.98)", S25, INFO25, z1, rate=rate)
# CE's own home-value distribution for the owner-occupied land (decile level; SCF for everything else)
for base in ["L1", "L2"]:
    Lown_tot = float((w25 * S25["L_own"]).sum())
    other = L.decile_sum(S25, S25[[c for c in L.BASE_COLS[base] if c != "L_own"]].sum(axis=1))
    land_d = Lown_tot * land_dec["ce_home_value_share"] + other
    phi = VAT_REV_BN / (R["m1"] * float(land_d.sum()) / 1e9)
    rent_ps = B.per_share_monthly(m, R["m1"] * land_d / (m["units"]["N_thousand"] * 1000.0))
    acc = B.net_from_base(rent_ps, m["w"], phi, m["budget"])
    d = dict(variant="CE 2024's own estimated home values by decile for the owner-occupied land (decile-netted only)",
             base=base, rate="bridge", measure=MEAS["m1"], phi=phi, dividend=float(acc["dividend"].iloc[0]),
             land_total_bn=float(land_d.sum()) / 1e9, top_decile_land_share=float(land_d["d10"] / land_d.sum()),
             deciles_gaining=int((acc["net"] > 0).sum()), payer_share=np.nan,
             impulse_dn_mid=B.impulse(m, acc["net"], SCHED["mid"].values)["flow_pct_consumption"], impulse_hh_liq_mid=np.nan,
             collateral_cross80_m=np.nan, collateral_mid_pct=np.nan, note="CE's home-value shares by income decile (Table 1110 addenda)")
    d.update({f"net_{dd}": float(acc["net"][dd]) for dd in DEC})
    rob.append(d)
ROB = pd.DataFrame(rob)
ROB.to_csv(OUT / "us_lvt_robustness.csv", index=False, float_format="%.10g")
print("\nrobustness (bridge-equivalent rate, measure m1 unless noted):")
print(ROB[["variant", "base", "phi", "dividend", "top_decile_land_share", "deciles_gaining", "payer_share", "net_d01", "net_d05",
           "net_d09", "net_d10", "impulse_dn_mid", "impulse_hh_liq_mid", "collateral_mid_pct"]].round(3).to_string(index=False))

# the s band at a fixed aggregate property value, by measure: what moves (phi, full-capture dividend, losses)
band_rows = []
for sv in [L.S_BAND[0], INFO25["s_uniform"], L.S_BAND[1]]:
    Ltot = sv * INFO25["scf_property_total_bn"]
    Sx, Ix = L.land_holdings(s25, z1, s_level=sv)
    for mk in MEAS:
        rT = RM.loc[MEAS[mk], "rT"]
        r = R[mk] if mk in ("m1", "m2") else rT / Ltot                   # yield measures: r fixed; flow measures: rent fixed
        phi_b = VAT_REV_BN / (r * Ltot)
        lf = L.loss_fraction(phi_b)
        _, sc, _ = L.collateral(Sx, lf)
        band_rows.append(dict(s=sv, measure=MEAS[mk], land_bn=Ltot, r=r, phi_bridge=phi_b, feasible=phi_b <= L.PHI_FULL,
                              full_capture_dividend=L.PHI_FULL * r * Ltot * 1e9 / (S_CE * 12),
                              bridge_capitalized_loss_bn=lf * Ltot,
                              bridge_collateral_mid_pct=-100 * L.MPC_COLL["mid"] * float(sc[sc["threshold"] == 0.8]["lost_equity_crossers_bn"].iloc[0]) / C_TOT_BN))
SBAND = pd.DataFrame(band_rows)
SBAND.to_csv(OUT / "us_lvt_s_band.csv", index=False, float_format="%.10g")
print("   s band (aggregate property value fixed):\n" + SBAND.round(3).to_string(index=False))

# %% step 6: the macro channels, side by side (the table behind the macro figure)
def imp_of(tax, grade, rate="", base="", mk="m1", defer="none"):
    q = IMP[(IMP["tax"] == tax) & (IMP["grade"] == grade) & (IMP["defer"] == defer)]
    if tax == "LVT":
        q = q[(q["rate"] == rate) & (q["base"] == base) & (q["measure"] == MEAS[mk])]
    return float(q["impulse_pct"].iloc[0])


def coll_of(scenario, design, th=0.80, col="dC_lost_equity_mid_pct", mk="m1"):
    q = COLL[(COLL["scenario"] == scenario) & (COLL["design"] == design) & (COLL["threshold"] == th) & (COLL["measure"] == MEAS[mk])]
    return float(q[col].iloc[0])


vshare = B.vatable_share_aggregate(m)
lev = LEVY.set_index(["lam", "mpw"])["pct_ce_consumption"]
pub = pd.read_csv(B.TIDY / "post_published_numbers.csv").set_index("id")["value"]
mrow = []


def add(instr, channel, central, low, high, unit="% of consumption", note=""):
    mrow.append(dict(instrument=instr, channel=channel, central=central, low=low, high=high, unit=unit, note=note))


add("VAT", "price level step (80-100% pass-through)", 100 * B.TAU * vshare * 0.9, 100 * B.TAU * vshare * 0.8, 100 * B.TAU * vshare,
    unit="% of consumer price level", note=f"15 points x aggregate VAT-able share {vshare:.3f}; post: 7-9% (P497-P498)")
add("LVT", "price level step", 0.0, 0.0, 0.0, unit="% of consumer price level",
    note="land in fixed supply, rents set by demand: nothing to pass through; no indexation plumbing needed")
add("VAT", "flow impulse, post's method (mid; band = high/low schedules)", imp_of("VAT", "dn_mid"), imp_of("VAT", "dn_high"), imp_of("VAT", "dn_low"),
    note="rebuild: 0.389% (Fig 7 central 0.390)")
add("VAT", "flow impulse, household level, payers graded by liquidity", imp_of("VAT", "hh_liq_mid"), imp_of("VAT", "hh_liq_high"), imp_of("VAT", "hh_liq_low"),
    note="VAT bills split within deciles by SCF non-housing spending")
add("VAT", "flow impulse, measured windfall MPCs (SCF 2025)", imp_of("VAT", "dn_meas"), imp_of("VAT", "hh_meas_htm"), imp_of("VAT", "dn_measshape"),
    note="central: decile means; low: decile x HtM cells; high: the measured shape scaled to 1.0 at D1")
add("VAT", "levy channel, lambda = 0.35 (impact; 2-5c per $ per year)", lev[(0.35, "mid")], lev[(0.35, "high")], lev[(0.35, "low")],
    note="-mpw x 0.35 x 8% x SCF 2025 net worth")
add("VAT", "levy channel, lambda = 1 (impact)", lev[(1.0, "mid")], lev[(1.0, "high")], lev[(1.0, "low")], note="full A-K corner")
add("VAT", "net demand at impact, lambda = 0.35 (flow + levy)", imp_of("VAT", "dn_mid") + lev[(0.35, "mid")],
    imp_of("VAT", "dn_high") + lev[(0.35, "high")], imp_of("VAT", "dn_low") + lev[(0.35, "low")], note="this unit's impact version")
add("VAT", "post, published: flow-only path (year 3)", pub["P662"], pub["P662"], pub["P662"], note="P662")
add("VAT", "post, published: central lambda = 0.35 (year 3; band = year 5)", pub["P663"], pub["P664"], pub["P665"], note="P663-P665")
add("VAT", "post, published: full A-K lambda = 1 (year 3; band = year 5)", pub["P666"], pub["P667"], pub["P668"], note="P666-P668")
for rate, base in [("bridge", "L1"), ("bridge", "L2"), ("full", "L1"), ("full", "L2")]:
    add("LVT", f"flow impulse, post's method ({rate}, {base})", imp_of("LVT", "dn_mid", rate, base), imp_of("LVT", "dn_high", rate, base),
        imp_of("LVT", "dn_low", rate, base), note="measure m1 (bridge-rate flows do not depend on the measure)")
add("LVT", "flow impulse, household level, payers graded by liquidity (bridge, L1)", imp_of("LVT", "hh_liq_mid", "bridge", "L1"),
    imp_of("LVT", "hh_liq_high", "bridge", "L1"), imp_of("LVT", "hh_liq_low", "bridge", "L1"))
add("LVT", "flow impulse, measured windfall MPCs (bridge, L1)", imp_of("LVT", "dn_meas", "bridge", "L1"), imp_of("LVT", "hh_meas_htm", "bridge", "L1"),
    imp_of("LVT", "dn_measshape", "bridge", "L1"))
add("LVT", "collateral, owners crossing 80% LTV, lost equity (bridge, L1, immediate)", coll_of("LVT_bridge_L1", "immediate"),
    coll_of("LVT_bridge_L1", "immediate", col="dC_lost_equity_high_pct"), coll_of("LVT_bridge_L1", "immediate", col="dC_lost_equity_low_pct"),
    note="4.7 / 6 / 10 cents per $ (Aladangady 2017; Mian-Rao-Sufi 2013; stress)")
add("LVT", "collateral, lost borrowing capacity only (bridge, L1, immediate)", coll_of("LVT_bridge_L1", "immediate", col="dC_lost_capacity_mid_pct"),
    coll_of("LVT_bridge_L1", "immediate", col="dC_lost_capacity_high_pct"), coll_of("LVT_bridge_L1", "immediate", col="dC_lost_capacity_low_pct"),
    note="the part that is credit, not wealth: the cleanest collateral-only base")
add("LVT", "collateral, full capture (L1, immediate)", coll_of("LVT_full_L1", "immediate"), coll_of("LVT_full_L1", "immediate", col="dC_lost_equity_high_pct"),
    coll_of("LVT_full_L1", "immediate", col="dC_lost_equity_low_pct"))
add("LVT", "collateral under increment-only grandfathering (bridge rate, L1)", coll_of("LVT_bridge_L1", "increment"),
    coll_of("LVT_bridge_L1", "increment", col="dC_lost_equity_high_pct"), coll_of("LVT_bridge_L1", "increment", col="dC_lost_equity_low_pct"),
    note="but the launch revenue is then near zero (only rent increments are taxed)")
nb = NONOCC[(NONOCC["scenario"] == "LVT_bridge_L1_m1") & (NONOCC["grade"] == "dn_mid")].iloc[0]
add("LVT", "non-occupying holders: wealth effect instead of flow (change in impulse, bridge, L1)", nb["wealth_version_mid_pct"] - nb["flow_version_pct"],
    nb["wealth_version_high_pct"] - nb["flow_version_pct"], nb["wealth_version_low_pct"] - nb["flow_version_pct"], note="2 / 3.5 / 5 cents per $")
nb2 = NONOCC[(NONOCC["scenario"] == "LVT_bridge_L2_m1") & (NONOCC["grade"] == "dn_mid")].iloc[0]
add("LVT", "non-occupying holders: wealth effect instead of flow (change in impulse, bridge, L2)", nb2["wealth_version_mid_pct"] - nb2["flow_version_pct"],
    nb2["wealth_version_high_pct"] - nb2["flow_version_pct"], nb2["wealth_version_low_pct"] - nb2["flow_version_pct"])
d65 = IMP[(IMP["tax"] == "LVT") & (IMP["rate"] == "bridge") & (IMP["base"] == "L1") & (IMP["measure"] == MEAS["m1"]) & (IMP["grade"] == "dn_mid")].set_index("defer")
add("LVT", "deferral by owners 65+, dividend paid in full (state lends the liens)", d65.loc["own65", "impulse_pct"] - d65.loc["none", "impulse_pct"],
    d65.loc["own65", "impulse_pct"] - d65.loc["none", "impulse_pct"], d65.loc["own65", "impulse_pct"] - d65.loc["none", "impulse_pct"],
    note=f"change in impulse; deferred = {100 * d65.loc['own65', 'deferred_share_of_revenue']:.0f}% of revenue, a deficit while it lasts")
add("LVT", "deferral by owners 65+, cash-balanced dividend", d65.loc["own65_cash", "impulse_pct"] - d65.loc["none", "impulse_pct"],
    d65.loc["own65_cash", "impulse_pct"] - d65.loc["none", "impulse_pct"], d65.loc["own65_cash", "impulse_pct"] - d65.loc["none", "impulse_pct"],
    note="change in impulse")
add("LVT", "deferral by owners 65+: their residual wealth effect (if any)", residual_wealth(ACC["LVT_bridge_L1_m1"][0], "own65", L.MPW["mid"]),
    residual_wealth(ACC["LVT_bridge_L1_m1"][0], "own65", L.MPW["high"]), 0.0, note="0 to 5 cents per $ of capitalized loss; never added to the flow")
lp = LOOP[(LOOP["scenario"] == "LVT_bridge_L1_m1")].set_index("ls")
add("LVT", "the loop: extra dividend (bridge, L1)", lp.loc["mid", "extra_pct_of_dividend"], lp.loc["low", "extra_pct_of_dividend"],
    lp.loc["high", "extra_pct_of_dividend"], unit="% of the dividend", note="land share of the rent change 0.30-0.50")
# net demand at impact for the LVT: flow + collateral (bridge, L1); band edges pair the extremes
lvt_net_c = imp_of("LVT", "dn_mid", "bridge", "L1") + coll_of("LVT_bridge_L1", "immediate")
lvt_net_lo = imp_of("LVT", "dn_high", "bridge", "L1") + coll_of("LVT_bridge_L1", "immediate", col="dC_lost_equity_high_pct")
lvt_net_hi = imp_of("LVT", "dn_low", "bridge", "L1") + coll_of("LVT_bridge_L1", "immediate", col="dC_lost_capacity_low_pct")
add("LVT", "net demand at impact (flow + collateral; bridge, L1, immediate)", lvt_net_c, lvt_net_lo, lvt_net_hi,
    note="low: high MPC schedule (smallest flow) + 10c on lost equity; high: low schedule + 4.7c on lost capacity")
add("LVT", "collateral, owners crossing 80% LTV, lost equity (bridge, L2, immediate)", coll_of("LVT_bridge_L2", "immediate"),
    coll_of("LVT_bridge_L2", "immediate", col="dC_lost_equity_high_pct"), coll_of("LVT_bridge_L2", "immediate", col="dC_lost_equity_low_pct"),
    note="the broader base lowers the rate on homes (phi 0.555) and with it the price fall")
add("LVT", "net demand at impact (flow + collateral; bridge, L2, immediate)",
    imp_of("LVT", "dn_mid", "bridge", "L2") + coll_of("LVT_bridge_L2", "immediate"),
    imp_of("LVT", "dn_high", "bridge", "L2") + coll_of("LVT_bridge_L2", "immediate", col="dC_lost_equity_high_pct"),
    imp_of("LVT", "dn_low", "bridge", "L2") + coll_of("LVT_bridge_L2", "immediate", col="dC_lost_capacity_low_pct"),
    note="same pairing of extremes as for L1")
MACRO = pd.DataFrame(mrow)
MACRO.to_csv(OUT / "us_lvt_macro_channels.csv", index=False, float_format="%.10g")
print("\nstep 6, macro channels:\n" + MACRO[["instrument", "channel", "central", "low", "high", "unit"]].round(3).to_string(index=False))

# %% figures (light mode, PNG at 200 dpi; the rebuild's chrome and the dataviz reference palette, slots in fixed order:
# VAT = blue, LVT on base L1 = orange, LVT on base L2 = aqua; validated with the skill's validator, contrast relief by
# legends, direct labels and the CSV tables in out/)
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, Polygon, Rectangle

SURF, INK, INK2, MUTED, GRID, AXIS = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
C1, C2, C3, C4 = "#2a78d6", "#eb6834", "#1baf7a", "#eda100"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": AXIS, "axes.labelcolor": INK2,
                     "xtick.color": MUTED, "ytick.color": INK2, "axes.facecolor": SURF, "figure.facecolor": SURF,
                     "savefig.facecolor": SURF})
DD = np.arange(1, 11)


def style_axes(ax, grid_axis="y"):
    for sp in ["top", "right", "left"]:
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color(AXIS)
    ax.grid(axis=grid_axis, color=GRID, linewidth=0.8, linestyle="-")
    ax.set_axisbelow(True)
    ax.tick_params(length=0)


def money(v):
    return f"−${abs(v):,.0f}" if v < 0 else f"+${v:,.0f}"


# --- Figure 1: net transfer by decile, VAT vs LVT
fig, axs = plt.subplots(1, 3, figsize=(15.5, 5.9), dpi=200, gridspec_kw={"width_ratios": [1, 1, 1.05]})
fig.subplots_adjust(left=0.055, right=0.985, top=0.80, bottom=0.17, wspace=0.28)
panels = [("Bridge-equivalent rate: every dividend $%.0f" % DIV_VAT, "LVT_bridge_L1_m1", "LVT_bridge_L2_m1"),
          ("Full capture (phi = 0.98, measure m1)", "LVT_full_L1_m1", "LVT_full_L2_m1")]
for ax, (title, k1, k2) in zip(axs[:2], panels):
    style_axes(ax)
    ax.axhline(0, color=AXIS, linewidth=1.0, zorder=2)
    series = [("VAT, 15 points", acc_v["net"].values, C1, DIV_VAT),
              (f"LVT on L1 (residential land), phi {ACC[k1][0]:.2f}", ACC[k1][1]["net"].values, C2, float(ACC[k1][1]["dividend"].iloc[0])),
              (f"LVT on L2 (+ business land), phi {ACC[k2][0]:.2f}", ACC[k2][1]["net"].values, C3, float(ACC[k2][1]["dividend"].iloc[0]))]
    for lab, y, col, dv in series:
        ax.plot(DD, y, color=col, linewidth=2, zorder=3, solid_capstyle="round")
        ax.plot(DD, y, linestyle="none", marker="o", markersize=6.5, markerfacecolor=col, markeredgecolor=SURF, markeredgewidth=2, zorder=4)
        ax.annotate(money(y[-1]), (10, y[-1]), xytext=(8, 0), textcoords="offset points", va="center", fontsize=8, color=INK2)
    ax.set_xticks(DD)
    ax.set_xticklabels([f"D{i}" for i in DD])
    ax.set_xlim(0.6, 11.0)
    ax.set_title(title, fontsize=10.5, color=INK, loc="left")
    ax.set_ylabel("Net transfer, $ per adult share per month", fontsize=9)
    divs = "  ·  ".join(f"{n.split(',')[0].split(' (')[0]} dividend ${d:.0f}" for n, _, _, d in series)
    ax.text(0.0, -0.13, divs, transform=ax.transAxes, fontsize=7.6, color=MUTED, va="top")
# panel (c): within-decile spread at the bridge-equivalent rate (household level)
ax = axs[2]
style_axes(ax)
ax.axhline(0, color=AXIS, linewidth=1.0, zorder=2)
for off, lab, col in [(-0.17, "VAT (household, TOTSPENDNH split)", C1), (0.17, "LVT_bridge_L1_m1", C2)]:
    q = who[who["scenario"] == lab].set_index("dec").loc[DEC]
    for i, d in enumerate(DEC):
        x = i + 1 + off
        ax.plot([x, x], [q.loc[d, "net_ps_p10"], q.loc[d, "net_ps_p90"]], color=col, linewidth=2, solid_capstyle="round", zorder=3)
        ax.plot([x, x], [q.loc[d, "net_ps_p25"], q.loc[d, "net_ps_p75"]], color=col, linewidth=5.5, solid_capstyle="butt", zorder=3, alpha=0.55)
        ax.plot(x, q.loc[d, "net_ps_p50"], marker="o", markersize=6, markerfacecolor=col, markeredgecolor=SURF, markeredgewidth=1.6, zorder=4)
ax.set_xticks(DD)
ax.set_xticklabels([f"D{i}" for i in DD])
ax.set_xlim(0.4, 10.6)
ax.set_title("Inside the deciles (bridge rate): households' net per share", fontsize=10.5, color=INK, loc="left")
ax.set_ylabel("$ per adult share per month", fontsize=9)
ax.text(0.0, -0.13, "line: 10th-90th percentile; thick: 25th-75th; dot: median (SCF 2025 families)", transform=ax.transAxes,
        fontsize=7.6, color=MUTED, va="top")
handles = [Line2D([0], [0], color=C1, linewidth=2, marker="o", markersize=6, markeredgecolor=SURF, label="VAT bridge (rebuilt)"),
           Line2D([0], [0], color=C2, linewidth=2, marker="o", markersize=6, markeredgecolor=SURF, label="LVT on L1: land under homes and other residential property"),
           Line2D([0], [0], color=C3, linewidth=2, marker="o", markersize=6, markeredgecolor=SURF, label="LVT on L2: L1 plus noncorporate and corporate land")]
fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.055, 0.905), ncol=3, frameon=False, fontsize=8.4, labelcolor=INK2)
fig.text(0.055, 0.965, "Who gains and who pays: the VAT bridge and a land-value tax funding the same flat dividend",
         fontsize=13.5, color=INK, weight="bold")
fig.text(0.055, 0.03, "CE 2024 pretax-income deciles and payment shares (adult 1, child 0.3); land from SCF 2025 calibrated to the Z.1 2024 land residuals; "
         "rent-to-value r = 10-year Treasury yield (4.21%). Source: consumption/lvt (run_lvt_us.py), out/us_lvt_accounting_by_decile.csv, us_lvt_who_pays.csv.",
         fontsize=7.4, color=MUTED)
fig.savefig(FIG / "us_lvt_net_by_decile.png", dpi=200)
plt.close(fig)


# --- Figure 2: demand shifts side by side, the 15 largest movers
def hbar(ax, yc, v, h, color, r_px=7):
    """Horizontal bar from 0 to v as one polygon: rounded corners at the data end (r_px at 200 dpi), square at the
    baseline. Built in display space and mapped back, so there is no seam where two patches would overlap."""
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


def signed(v, fmt="{:.2f}"):
    return ("−" if v < 0 else "+") + fmt.format(abs(v))


top = list(CMP.head(15).index)
cols = [("VAT|decile_netted", "VAT, post's method", C1), ("LVT_bridge_L1_m1|decile_netted", "LVT L1, post's method", C2),
        ("LVT_bridge_L1_m1|household_liq_tenure", "LVT L1, household level, tenure-aware baskets", C3)]
tot = {c: float(dsh[c].sum()) for c, _, _ in cols}
n = len(top)
fig = plt.figure(figsize=(14.5, 9.6), dpi=200)
axL = fig.add_axes([0.255, 0.10, 0.44, 0.72])
axR = fig.add_axes([0.745, 0.10, 0.23, 0.72], sharey=axL)
yy = np.arange(n)[::-1].astype(float)
bh = 0.24
lo_ = min(dsh.loc[top, [c for c, _, _ in cols]].min().min(), 0) - 0.5
hi_ = dsh.loc[top, [c for c, _, _ in cols]].max().max() + 2.6
axL.set_xlim(lo_, hi_)
axL.set_ylim(-0.7, n - 0.3)
style_axes(axL, "x")
axL.axvline(0, color=AXIS, linewidth=1.0, zorder=2)
fig.canvas.draw()
for j, (c, lab, col) in enumerate(cols):
    for cat, yc in zip(top, yy):
        hbar(axL, yc + (1 - j) * (bh + 0.03), float(dsh.loc[cat, c]), bh, col)
for cat, yc in zip(top, yy):
    v = float(dsh.loc[cat, cols[2][0]])
    if cat in ("Rented dwellings", "Home maintenance, repairs & insurance"):
        axL.text(max(v, 0) + 0.25, yc - (bh + 0.03), signed(v), va="center", fontsize=7.6, color=INK2)
axL.set_yticks(yy)
axL.set_yticklabels(top, fontsize=8.6)
axL.set_xlabel("Change in spending at impact, $ per adult share per month", fontsize=9)
axL.set_title("Dollars (bridge-equivalent rate, mid MPC schedule; household level: payers graded by liquidity)", fontsize=9.6, color=INK, loc="left")
style_axes(axR, "x")
axR.axvline(0, color=AXIS, linewidth=1.0, zorder=2)
for j, (c, lab, col) in enumerate(cols):
    axR.plot(100 * dsh.loc[top, c].values / tot[c], yy + (1 - j) * (bh + 0.03), linestyle="none", marker="o", markersize=5.6,
             markerfacecolor=col, markeredgecolor=SURF, markeredgewidth=1.4, zorder=4)
axR.tick_params(axis="y", labelleft=False)
axR.set_xlabel("Share of the version's total flow impulse, %", fontsize=9)
axR.set_title("Composition (each version / its own total)", fontsize=9.6, color=INK, loc="left")
fig.text(0.255, 0.955, "Demand shifts: under the post's method the LVT is the VAT scaled up; inside the deciles it is not",
         fontsize=13.5, color=INK, weight="bold")
fig.text(0.255, 0.928, f"Totals: VAT ${tot[cols[0][0]]:.2f}, LVT L1 ${tot[cols[1][0]]:.2f} (decile-netted), ${tot[cols[2][0]]:.2f} (household level). "
         "Tenure-aware: rent sits in renters' baskets and owner costs in owners' within each decile.", fontsize=9, color=INK2)
fig.legend(handles=[Patch(facecolor=col, edgecolor="none", label=lab) for _, lab, col in cols], loc="upper left",
           bbox_to_anchor=(0.255, 0.905), ncol=3, frameon=False, fontsize=8.4, labelcolor=INK2)
fig.text(0.255, 0.03, "The 15 largest movers across the three versions. CE 2024 deciles, Working-model elasticities (bridge.py), SCF 2025 households. "
         "Source: out/us_lvt_demand_shifts.csv, us_lvt_demand_compare.csv.", fontsize=7.4, color=MUTED)
fig.savefig(FIG / "us_lvt_demand_shifts_top15.png", dpi=200)
plt.close(fig)

# --- Figure 3: who pays
hL1 = HH["LVT_bridge_L1_m1"]
htm_b = HTM["biweekly"]
grp = np.where(S25["owner"] == 0, "non-owner",
               np.where(S25["age65"] == 1, "owner 65+", np.where(htm_b["htm"] == 1, "owner under 65, hand-to-mouth", "owner under 65, not hand-to-mouth")))
paid = -np.minimum(hL1["net"].values, 0)
GR = ["owner 65+", "owner under 65, hand-to-mouth", "owner under 65, not hand-to-mouth", "non-owner"]
shares = pd.DataFrame({g: L.decile_sum(S25, paid * (grp == g)) for g in GR})
shares = shares.div(shares.sum(axis=1), axis=0)
shares.index.name = "decile"
shares.to_csv(OUT / "us_lvt_payments_by_group.csv", float_format="%.10g")
fig, (a1, a2) = plt.subplots(1, 2, figsize=(14.5, 5.6), dpi=200, gridspec_kw={"width_ratios": [1, 1.15]})
fig.subplots_adjust(left=0.06, right=0.98, top=0.77, bottom=0.20, wspace=0.22)
style_axes(a1)
for lab, col, key in [("VAT (household level)", C1, "VAT (household, TOTSPENDNH split)"), ("LVT on L1", C2, "LVT_bridge_L1_m1"),
                      ("LVT on L2", C3, "LVT_bridge_L2_m1")]:
    q = who[who["scenario"] == key].set_index("dec").loc[DEC, "payer_share"].values * 100
    a1.plot(DD, q, color=col, linewidth=2, zorder=3)
    a1.plot(DD, q, linestyle="none", marker="o", markersize=6.5, markerfacecolor=col, markeredgecolor=SURF, markeredgewidth=2, zorder=4)
    a1.annotate(lab, (10, q[-1]), xytext=(8, 0), textcoords="offset points", va="center", fontsize=8, color=INK2)
a1.set_xticks(DD)
a1.set_xticklabels([f"D{i}" for i in DD])
a1.set_xlim(0.6, 12.2)
a1.set_ylim(0, 100)
a1.set_ylabel("Families that are net payers, %", fontsize=9)
a1.set_title("Net payers by income decile (bridge-equivalent rate)", fontsize=10.5, color=INK, loc="left")
style_axes(a2)
bottom = np.zeros(10)
for g, col in zip(GR, [C1, C2, C3, C4]):
    v = shares[g].values * 100
    for i in range(10):
        if v[i] > 0:
            a2.add_patch(Rectangle((i + 1 - 0.32, bottom[i]), 0.64, v[i], facecolor=col, edgecolor="none", zorder=3))
    bottom += v
cum = shares.cumsum(axis=1).values * 100
for i in range(10):
    for b in cum[i, :-1]:
        if 0.05 < b < 99.95:
            a2.plot([i + 1 - 0.32, i + 1 + 0.32], [b, b], color=SURF, linewidth=0.75, solid_capstyle="butt", zorder=4)
a2.set_xlim(0.4, 10.6)
a2.set_ylim(0, 100)
a2.set_xticks(DD)
a2.set_xticklabels([f"D{i}" for i in DD])
a2.set_ylabel("Share of the decile's net LVT payments, %", fontsize=9)
a2.set_title("Who makes the LVT's net payments (L1, bridge rate)", fontsize=10.5, color=INK, loc="left")
a2.legend(handles=[Patch(facecolor=col, edgecolor="none", label=g) for g, col in zip(GR, [C1, C2, C3, C4])], loc="upper center",
          bbox_to_anchor=(0.5, -0.085), ncol=2, frameon=False, fontsize=8.0, labelcolor=INK2)
fig.text(0.06, 0.955, "The LVT's payers are landowners, and below the top two deciles mostly owners over 65", fontsize=13.5, color=INK, weight="bold")
fig.text(0.06, 0.93, f"Families that are net payers: VAT {100 * who[who['scenario'].str.startswith('VAT')].set_index('dec').loc['all', 'payer_share']:.0f}%, "
         f"LVT L1 {100 * who[who['scenario'] == 'LVT_bridge_L1_m1'].set_index('dec').loc['all', 'payer_share']:.0f}%. "
         f"Owners 65+ make {100 * wl1.loc['all', 'payments_owner65_share']:.0f}% of all LVT L1 net payments.\nHand-to-mouth "
         "(KVW, biweekly band) families make few of them, and almost all of those are wealthy hand-to-mouth owners.", fontsize=9, color=INK2,
         va="top", linespacing=1.35)
fig.text(0.06, 0.025, "SCF 2025 families in CE 2024 payment shares. Source: out/us_lvt_who_pays.csv, us_lvt_payments_by_group.csv.",
         fontsize=7.4, color=MUTED)
fig.savefig(FIG / "us_lvt_who_pays.png", dpi=200)
plt.close(fig)

# --- Figure 4: the macro channels
rows_v = ["flow impulse, post's method (mid; band = high/low schedules)", "flow impulse, household level, payers graded by liquidity",
          "flow impulse, measured windfall MPCs (SCF 2025)", "levy channel, lambda = 0.35 (impact; 2-5c per $ per year)",
          "levy channel, lambda = 1 (impact)", "net demand at impact, lambda = 0.35 (flow + levy)"]
rows_l = ["flow impulse, post's method (bridge, L1)", "flow impulse, post's method (bridge, L2)",
          "flow impulse, household level, payers graded by liquidity (bridge, L1)", "flow impulse, measured windfall MPCs (bridge, L1)",
          "collateral, owners crossing 80% LTV, lost equity (bridge, L1, immediate)", "collateral, lost borrowing capacity only (bridge, L1, immediate)",
          "collateral under increment-only grandfathering (bridge rate, L1)",
          "non-occupying holders: wealth effect instead of flow (change in impulse, bridge, L1)",
          "net demand at impact (flow + collateral; bridge, L1, immediate)",
          "net demand at impact (flow + collateral; bridge, L2, immediate)"]
short = {rows_v[0]: "flow impulse, post's method", rows_v[1]: "flow, household level, liquidity-graded payers",
         rows_v[2]: "flow, measured SCF windfall MPCs", rows_v[3]: "levy channel, lambda = 0.35",
         rows_v[4]: "levy channel, lambda = 1 (full A-K)", rows_v[5]: "net at impact, lambda = 0.35",
         rows_l[0]: "flow impulse, post's method, L1", rows_l[1]: "flow impulse, post's method, L2",
         rows_l[2]: "flow, household level, liquidity-graded, L1", rows_l[3]: "flow, measured SCF windfall MPCs, L1",
         rows_l[4]: "collateral: crossers' lost equity (80% LTV)", rows_l[5]: "collateral: crossers' lost borrowing capacity",
         rows_l[6]: "collateral under increment-only grandfathering", rows_l[7]: "non-occupiers: wealth effect instead of flow",
         rows_l[8]: "net at impact (flow + collateral), L1", rows_l[9]: "net at impact (flow + collateral), L2"}
MI = MACRO.set_index("channel")
fig = plt.figure(figsize=(14.5, 9.4), dpi=200)
axP = fig.add_axes([0.30, 0.775, 0.66, 0.085])
axD = fig.add_axes([0.30, 0.115, 0.66, 0.575])
style_axes(axP, "x")
for yc, (lab, ch, col) in enumerate([("LVT", "price level step", C2), ("VAT", "price level step (80-100% pass-through)", C1)]):
    r = MI.loc[ch]
    axP.plot([r["low"], r["high"]], [yc, yc], color=col, linewidth=2, solid_capstyle="round", zorder=3)
    axP.plot(r["central"], yc, marker="o", markersize=7, markerfacecolor=col, markeredgecolor=SURF, markeredgewidth=2, zorder=4)
    axP.text(-0.012, yc, f"{lab}: {r['central']:.1f}%" + (f" [{r['low']:.1f}, {r['high']:.1f}]" if r["high"] > r["low"] else ""),
             transform=axP.get_yaxis_transform(), ha="right", va="center", fontsize=8.6, color=INK2)
axP.set_ylim(-0.6, 1.6)
axP.set_yticks([])
axP.set_xlim(-0.5, 10)
axP.set_title("Channel 1: the price level (one-off step, % of the consumer price level)", fontsize=10, color=INK, loc="left")
style_axes(axD, "x")
axD.axvline(0, color=AXIS, linewidth=1.0, zorder=2)
labels, ys = [], []
y = 0
for blk, rws, col in [("LVT", rows_l[::-1], C2), ("VAT", rows_v[::-1], C1)]:
    for ch in rws:
        r = MI.loc[ch]
        axD.plot([r["low"], r["high"]], [y, y], color=col, linewidth=2, solid_capstyle="round", zorder=3)
        axD.plot(r["central"], y, marker="o", markersize=7, markerfacecolor=col, markeredgecolor=SURF, markeredgewidth=2, zorder=4)
        axD.annotate(signed(r["central"]), (max(r["high"], r["central"]), y), xytext=(6, 0), textcoords="offset points", va="center",
                     fontsize=7.6, color=INK2)
        labels.append(f"{blk}: {short[ch]}")
        ys.append(y)
        y += 1
    y += 0.6
# the post's published numbers, on the VAT rows they correspond to
pubs = [("post, published: flow-only path (year 3)", rows_v[0]), ("post, published: central lambda = 0.35 (year 3; band = year 5)", rows_v[5])]
for ch, target in pubs:
    r = MI.loc[ch]
    yt = ys[labels.index(f"VAT: {short[target]}")]
    axD.plot([r["low"], r["high"]], [yt - 0.34, yt - 0.34], color=INK, linewidth=1.2, zorder=3)
    axD.plot(r["central"], yt - 0.34, marker="D", markersize=5, markerfacecolor=SURF, markeredgecolor=INK, markeredgewidth=1.1, zorder=5)
r = MI.loc["post, published: full A-K lambda = 1 (year 3; band = year 5)"]
yt = ys[labels.index(f"VAT: {short[rows_v[4]]}")]
axD.plot([r["low"], r["high"]], [yt - 0.34, yt - 0.34], color=INK, linewidth=1.2, zorder=3)
axD.plot(r["central"], yt - 0.34, marker="D", markersize=5, markerfacecolor=SURF, markeredgecolor=INK, markeredgewidth=1.1, zorder=5)
axD.set_yticks(ys)
axD.set_yticklabels(labels, fontsize=8.5)
axD.set_ylim(-0.8, y - 0.2)
axD.set_xlabel("Change in consumption demand at impact, % of consumption (CE 2024 budget)", fontsize=9)
axD.set_title("Channel 2: demand (dot: central; line: band)", fontsize=10, color=INK, loc="left")
fig.legend(handles=[Line2D([0], [0], color=C1, linewidth=2, marker="o", markersize=7, markeredgecolor=SURF, label="VAT bridge (this unit, impact)"),
                    Line2D([0], [0], color=C2, linewidth=2, marker="o", markersize=7, markeredgecolor=SURF, label="LVT, bridge-equivalent rate (impact)"),
                    Line2D([0], [0], color=INK, linewidth=1.2, marker="D", markersize=5, markerfacecolor=SURF, markeredgecolor=INK,
                           label="the post's published path (year 3; band year 5)")],
           loc="upper left", bbox_to_anchor=(0.30, 0.915), ncol=3, frameon=False, fontsize=8.4, labelcolor=INK2)
fig.text(0.04, 0.965, "Two channels, kept apart: the LVT has no price step and no lambda, but it has a collateral channel",
         fontsize=13.0, color=INK, weight="bold")
fig.text(0.30, 0.012, "Impact-period, static: flows at the rebuilt MPC schedules; the levy and collateral channels at 2-5 and 4.7-10 cents per $ per year "
         "on SCF 2025 balance sheets.\nThe post's numbers come from a dynamic ramp-and-rebuild model and are shown for orientation, not as a like-for-like gate. "
         "Source: out/us_lvt_macro_channels.csv.", fontsize=7.4, color=MUTED, linespacing=1.3)
fig.savefig(FIG / "us_lvt_macro_channels.png", dpi=200)
plt.close(fig)
print("\nfigures: us_lvt_net_by_decile.png, us_lvt_demand_shifts_top15.png, us_lvt_who_pays.png, us_lvt_macro_channels.png")
