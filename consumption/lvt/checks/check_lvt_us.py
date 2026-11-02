# check_lvt_us.py - identities behind consumption/lvt's US results, recomputed from the tidy files with plain numpy
# (lvt_us.py is not imported; bridge.py only for the gated CE 2024 model and the rebuild's outputs it must match).
# PASS/FAIL per check; writes out/check_lvt_us.csv; exits 1 on any FAIL.
#
#   A  inputs: Z.1 residuals rebuilt from their components, the yield, PCE housing, the four rent measures
#   B  land by household: SCF totals equal Z.1, decile shares sum to one, the calibration of s
#   C  accounting: revenue = dividend payments, net transfers sum to zero, bills sum to revenue, phi feasible
#   D  the VAT side reproduces the rebuild (nets, Fig 5 bars, impulse, dividend)
#   E  household level: aggregates equal the decile accounting; group shares sum to one
#   F  MPCs: the SCF windfall tabulation against the Fed's FEDS note; the schedules against the rebuild
#   G  macro: price step, levy channel, LTVs and threshold crossers recomputed, capitalization, the loop
#   K  the headline: each crosser counted once (flow + credit effect on lost borrowing capacity), the T4-overlap edge,
#      who responds (hand-to-mouth crossers), corporate land on the wealth reading, the PCE denominator
#
# Tolerances: identities that hold to machine precision in run_lvt_us.py are checked to the CSVs' 10 significant digits
# (about 1e-6 dollars per share-month); recomputations from the SCF file to 1e-6 relative.
#
# Run from the repo root:  venv/bin/python -I consumption/lvt/checks/check_lvt_us.py

# %% setup
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent                    # consumption/lvt/checks
LVT = HERE.parent
THREAD = LVT.parent
REPO = THREAD.parent
sys.path.insert(0, str(THREAD / "rebuild" / "code"))

import numpy as np
import pandas as pd

import bridge as B

OUT = LVT / "out"
TIDY = THREAD / "data" / "tidy"
DEC = [f"d{i:02d}" for i in range(1, 11)]
CPI = 4750.0 / 4625.0
ROWS = []


def check(cid, desc, value, target, tol, kind="abs"):
    value, target = float(value), float(target)
    gap = value - target
    ok = abs(gap) <= tol if kind == "abs" else abs(gap) <= tol * max(abs(target), 1e-12)
    ROWS.append(dict(id=cid, check=desc, value=value, target=target, gap=gap, tolerance=tol, kind=kind, status="PASS" if ok else "FAIL"))
    return ok


def check_true(cid, desc, cond, note=""):
    ROWS.append(dict(id=cid, check=desc, value=float(bool(cond)), target=1.0, gap=0.0 if cond else 1.0, tolerance=0.0, kind="bool",
                     status="PASS" if cond else "FAIL", note=note))


inp = pd.read_csv(OUT / "us_lvt_inputs.csv").set_index("item")["value"]

# %% A: inputs
z = pd.read_csv(TIDY / "z1_land.csv", dtype={"date": str})


def zv(sid, freq, year):
    return float(z[(z["series_id"] == sid) & (z["freq"] == freq) & (z["date"] == str(year))]["value"].iloc[0])


L_hh = zv("LM155035005", "A_mean", 2024) - zv("LM155012665", "A_mean", 2024)
check("A1", "Z.1 household land 2024 = HH+NPO real estate - HH structures (annual means)", L_hh, zv("LAND_HH_PAPER", "A_paper", 2024), 0.01)
check("A2", "household land 2024 = 23,410.7 $bn (task statement)", L_hh, 23410.7, 0.05)
check("A3", "household land used by the run", inp["L_hh"], L_hh, 1e-6)
L_nnb = zv("LM115035005", "A_eop", 2024) - zv("FL115012665", "A_mean", 2024) - zv("FL115013665", "A_eop", 2024)
check("A4", "noncorporate land 2024 = NNB real estate (year-end) - residential (mean) - nonresidential (year-end) structures", inp["L_nnb"], L_nnb, 1e-6)
sh = np.mean([zv("LAND_NFC_PAPERCONV", "A_paper", y) / zv("LM105035005", "A_eop", y) for y in range(2016, 2021)])
check("A5", "NFC land 2024 (assumption): 2016-2020 mean land share of NFC real estate x 2024 NFC real estate", inp["L_nfc"], sh * zv("LM105035005", "A_eop", 2024), 1e-6)
check("A6", "NFC land, structures-proxy low end < main < 2020-share high end", float(inp["L_nfc_structures_proxy"] < inp["L_nfc"] < inp["L_nfc_share_2020"]), 1.0, 0)
g = pd.read_csv(REPO / "pinning" / "cache" / "GS10.csv", parse_dates=["observation_date"])
gs = float(g[g["observation_date"].dt.year == 2024]["GS10"].mean())
check("A7", "GS10 2024 annual mean (12 months)", inp["gs10_2024"], gs, 1e-9)
d10 = pd.read_csv(REPO / "three-taxes" / "cache" / "DGS10.csv", parse_dates=["observation_date"])
d10["v"] = pd.to_numeric(d10["DGS10"], errors="coerce")
check("A8", "GS10 2024 agrees with the daily DGS10 mean", gs, float(d10[d10["observation_date"].dt.year == 2024]["v"].mean()), 0.01)
bea = pd.read_csv(TIDY / "bea_pce_u_long.csv.gz", low_memory=False, usecols=["table", "freq", "series_code", "date", "value"])
ph = float(bea[(bea["table"] == "2.4.5U") & (bea["freq"] == "A") & (bea["series_code"] == "DHSGRC") & (bea["date"].astype(str) == "2024")]["value"].iloc[0]) / 1000
check("A9", "PCE housing services 2024, $bn", inp["pce_housing_2024_bn"], ph, 1e-9)
for k, rT in [("m1", L_hh * gs / 100), ("m2", L_hh * (gs + 1.5) / 100), ("m3", 0.3 * ph), ("m4", 0.5 * ph)]:
    check(f"A10_{k}", f"rent measure {k}: rT", inp[f"rT_{k}"], rT, 1e-6)
    check(f"A11_{k}", f"rent measure {k}: r = rT / household land", inp[f"r_{k}"], rT / L_hh, 1e-9, "rel")

# %% B: land by household
s = pd.read_csv(TIDY / "scf2025_summary.csv.gz", usecols=["Y1", "WGT", "HOUSES", "ORESRE", "NNRESRE", "BUS", "EQUITY", "MRTHEL",
                                                          "NETWORTH", "INCPCTLECAT", "NINCPCTLECAT", "MPSPEND", "AGE", "LIQ", "STOCKS",
                                                          "BOND", "NMMF", "CCBAL", "INCOME"])
w = s["WGT"].values
for v in ["HOUSES", "ORESRE", "NNRESRE", "BUS", "EQUITY", "MRTHEL", "NETWORTH", "LIQ", "STOCKS", "BOND", "NMMF", "CCBAL", "INCOME"]:
    s[v] = s[v] / CPI
dec = np.minimum(s["INCPCTLECAT"].values, 10)
check("B1", "SCF 2025 families (million)", w.sum() / 1e6, 134.96, 0.01)
for i in range(1, 11):
    check(f"B2_{i}", f"income decile {i} holds a tenth of families (INCPCTLECAT)", w[dec == i].sum() / w.sum(), 0.1, 0.0015)
prop = (w * (s["HOUSES"].clip(lower=0) + s["ORESRE"].clip(lower=0))).sum()
s_cal = L_hh * 1e9 / prop
check("B3", "calibrated land share s (Z.1 household land / SCF HOUSES+ORESRE in 2024 $)", inp["s_uniform_2025"], s_cal, 1e-9)
L1 = s_cal * (s["HOUSES"].clip(lower=0) + s["ORESRE"].clip(lower=0)).values
check("B4", "SCF residential land total = Z.1 household land, $bn", (w * L1).sum() / 1e9, L_hh, 1e-6)
key_nnb = (s["NNRESRE"].clip(lower=0) + s["BUS"].clip(lower=0)).values
key_nfc = s["EQUITY"].clip(lower=0).values
Lnnb = inp["L_nnb"] * 1e9 * key_nnb / (w * key_nnb).sum()
Lnfc = inp["L_nfc"] * 1e9 * key_nfc / (w * key_nfc).sum()
L2 = L1 + Lnnb + Lnfc
check("B5", "SCF L2 total = Z.1 household + noncorporate + NFC (assumed) land, $bn", (w * L2).sum() / 1e9, L_hh + inp["L_nnb"] + inp["L_nfc"], 1e-6)
ld = pd.read_csv(OUT / "us_lvt_land_by_decile.csv").set_index("decile")
sh1 = pd.Series([(w * L1)[dec == i].sum() for i in range(1, 11)], index=DEC) / (w * L1).sum()
sh2 = pd.Series([(w * L2)[dec == i].sum() for i in range(1, 11)], index=DEC) / (w * L2).sum()
check("B6", "L1 decile shares sum to one", sh1.sum(), 1.0, 1e-12)
check("B7", "L2 decile shares sum to one", sh2.sum(), 1.0, 1e-12)
check("B8", "L1 decile shares match out/us_lvt_land_by_decile.csv (max abs gap)", (sh1 - ld["L1_share"]).abs().max(), 0.0, 1e-6)
check("B9", "L2 decile shares match out/us_lvt_land_by_decile.csv (max abs gap)", (sh2 - ld["L2_share"]).abs().max(), 0.0, 1e-6)
check("B10", "VAT-able consumption decile shares sum to one", ld["vatable_share"].sum(), 1.0, 1e-9)
cal = pd.read_csv(OUT / "us_lvt_s_calibration.csv")
zr = float(cal[cal["item"].str.startswith("Z.1 2024 aggregate land")]["value"].iloc[0])
check("B11", "Z.1 aggregate land / real estate ratio (task: ~45%)", zr, L_hh / zv("LM155035005", "A_mean", 2024), 1e-9)

# %% C: accounting
m = B.build_model(2024)
vals = m["vals"]
N = vals.loc[B.NCU, DEC].astype(float).values * 1000
people = vals.loc[B.PEOPLE, DEC].astype(float).values
kids = vals.loc[B.CHILDREN, DEC].astype(float).values
shares = (people - kids) + 0.3 * kids
S_CE = (N * shares).sum()
wd = N * shares / S_CE
check("C1", "CE 2024 payment shares used by the run", inp["ce_payment_shares"], S_CE, 1e-3)
check("C2", "CE decile weights sum to one", wd.sum(), 1.0, 1e-12)
acc = pd.read_csv(OUT / "us_lvt_accounting_by_decile.csv")
phi = pd.read_csv(OUT / "us_lvt_phi.csv")
VAT_DIV = float(acc[acc["scenario"] == "VAT"]["dividend"].iloc[0])
for _, r in phi.iterrows():
    tag = f"{r['rate']}_{r['base']}_{r['measure'][:2]}"
    check(f"C3_{tag}", f"revenue = phi x r x land ({tag})", r["revenue_bn"], r["phi"] * r["r"] * r["land_bn"], 1e-6, "rel")
    check(f"C4_{tag}", f"revenue = dividend payments: dividend x CE shares x 12 ({tag})", r["dividend_usd_month"] * S_CE * 12 / 1e9, r["revenue_bn"], 1e-9, "rel")
    if r["rate"] == "bridge":
        check(f"C5_{tag}", f"bridge-equivalent dividend = the rebuilt VAT dividend ({tag})", r["dividend_usd_month"], VAT_DIV, 1e-9)
        check_true(f"C6_{tag}", f"bridge-equivalent phi <= 0.98 ({tag}: phi {r['phi']:.3f})", r["phi"] <= 0.98)
for sc, q in acc.groupby("scenario"):
    q = q.set_index("decile").loc[DEC]
    check(f"C7_{sc}", f"net transfers sum to zero over the population, $/share/month ({sc})", float((wd * q["net"].values).sum()), 0.0, 1e-6)
    check(f"C8_{sc}", f"net = dividend - bill in every decile, max gap ({sc})", float(np.abs(q["dividend"] - q["bill"] - q["net"]).max()), 0.0, 1e-6)
    if sc != "VAT":
        rev = float(phi[(phi["rate"] == sc.split("_")[1]) & (phi["base"] == sc.split("_")[2]) & (phi["measure"].str[:2] == sc.split("_")[3])]["revenue_bn"].iloc[0])
        check(f"C9_{sc}", f"bills by decile x CE shares x 12 = revenue ({sc})", float((N * shares * q["bill"].values).sum() * 12 / 1e9), rev, 1e-9, "rel")
# independent recompute of the bridge-rate L1 nets
r1 = inp["r_m1"]
phi1 = float(phi[(phi["rate"] == "bridge") & (phi["base"] == "L1") & (phi["measure"].str.startswith("m1"))]["phi"].iloc[0])
bill = np.array([phi1 * r1 * (w * L1)[dec == i].sum() for i in range(1, 11)]) / (N * shares * 12)
div = (wd * bill).sum()
q = acc[acc["scenario"] == "LVT_bridge_L1_m1"].set_index("decile").loc[DEC]
check("C10", "LVT bridge L1 nets recomputed from the SCF file, max abs gap $", float(np.abs((div - bill) - q["net"].values).max()), 0.0, 1e-6)
check("C11", "LVT bridge L1 dividend recomputed = VAT dividend", div, VAT_DIV, 1e-6)
rob = pd.read_csv(OUT / "us_lvt_robustness.csv")
inf = rob[rob["phi"] > 0.98][["variant", "base", "phi"]]
ROWS.append(dict(id="C12", check="infeasible variants (phi > 0.98: the base cannot fund the bridge's dividend on that measure): "
                 + "; ".join(f"{a} [{b}] phi {c:.3f}" for a, b, c in inf.values), value=len(inf), target=np.nan, gap=np.nan,
                 tolerance=np.nan, kind="info", status="INFO"))

# %% D: the VAT side reproduces the rebuild
reb = pd.read_csv(B.REBUILD / "out" / "us_accounting_by_decile.csv").set_index("decile")
v = acc[acc["scenario"] == "VAT"].set_index("decile").loc[DEC]
check("D1", "VAT nets = rebuild us_accounting_by_decile.csv, max abs gap $", float(np.abs(v["net"].values - reb.loc[DEC, "net_usd_month"].values).max()), 0.0, 1e-4)
check("D2", "VAT dividend = rebuild ($249.38)", VAT_DIV, float(reb["dividend_usd_month"].iloc[0]), 1e-4)
ds = pd.read_csv(OUT / "us_lvt_demand_shifts.csv", index_col=0)
rds = pd.read_csv(B.REBUILD / "out" / "us_demand_shifts.csv", index_col=0)
check("D3", "VAT decile-netted category shifts = rebuild Fig 5 (36 bars), max abs gap $",
      float(np.abs(ds.loc[m["chart"], "VAT|decile_netted"] - rds.loc[m["chart"], "dUSD_mid"]).max()), 0.0, 1e-5)
imp = pd.read_csv(OUT / "us_lvt_impulse.csv")
rimp = pd.read_csv(B.REBUILD / "out" / "us_impulse.csv")
check("D4", "VAT flow impulse (mid) = rebuild, % of consumption", float(imp[(imp["tax"] == "VAT") & (imp["grade"] == "dn_mid")]["impulse_pct"].iloc[0]),
      float(rimp[(rimp["schedule"] == "mid") & (rimp["variant"] == "chosen")]["flow_pct_consumption"].iloc[0]), 1e-5)
for k, gname in [("low", "dn_low"), ("high", "dn_high")]:
    check(f"D5_{k}", f"VAT flow impulse ({k}) = rebuild", float(imp[(imp["tax"] == "VAT") & (imp["grade"] == gname)]["impulse_pct"].iloc[0]),
          float(rimp[(rimp["schedule"] == k) & (rimp["variant"] == "chosen")]["flow_pct_consumption"].iloc[0]), 1e-5)

# %% E: household level
z0 = imp[(imp["tax"] == "LVT") & (imp["defer"] == "none")]
for sc, q in z0.groupby(["rate", "base", "measure"]):
    a = float(q[q["grade"] == "dn_mid"]["impulse_pct"].iloc[0])
    b = float(q[q["grade"] == "hh_mid"]["impulse_pct"].iloc[0])
    check(f"E1_{'_'.join(sc)[:20]}", f"household aggregation = decile accounting at a uniform MPC ({'/'.join(sc)})", b, a, 1e-9)
check("E2", "VAT household level = decile level at a uniform MPC", float(imp[(imp["tax"] == "VAT") & (imp["grade"] == "hh_mid")]["impulse_pct"].iloc[0]),
      float(imp[(imp["tax"] == "VAT") & (imp["grade"] == "dn_mid")]["impulse_pct"].iloc[0]), 1e-9)
pg = pd.read_csv(OUT / "us_lvt_payments_by_group.csv").set_index("decile")
check("E3", "payer groups' shares of each decile's net payments sum to one (max abs gap)", float((pg.sum(axis=1) - 1).abs().max()), 0.0, 1e-9)
who = pd.read_csv(OUT / "us_lvt_who_pays.csv")
check_true("E4", "payer shares lie in [0, 1]", ((who["payer_share"] >= 0) & (who["payer_share"] <= 1)).all())
for sc, q in who[who["dec"] == "all"].groupby("scenario"):
    tot = q[["payers_owner_share", "payers_renter_share"]].sum(axis=1).iloc[0]
    check(f"E5_{sc[:18]}", f"payers are owners or renters, shares sum to one ({sc})", tot, 1.0, 1e-9)
cd = ld["c_d_2025"] * ld["scf_raw_shares_per_family"] * ld["scf_families_m"] * 1e6
check("E6", "calibrated SCF payment shares = CE decile payment shares (max relative gap)", float(np.abs(cd.values / (N * shares) - 1).max()), 0.0, 1e-9)
cmpd = pd.read_csv(OUT / "us_lvt_demand_shifts.csv", index_col=0)
for lab in ["VAT", "LVT_bridge_L1_m1"]:
    hh = float(cmpd[lab + "|household_liq"].sum())
    ten = float(cmpd[lab + "|household_liq_tenure"].sum())
    check(f"E7_{lab}", f"tenure-aware bars add up to the household flow (Engel aggregation at the tenure baskets), {lab}", ten, hh, 0.002, "rel")

# %% F: MPCs
fe = pd.read_csv(OUT / "us_lvt_feds_mpc_check.csv")
mp = {i: np.average(s["MPSPEND"][s["NINCPCTLECAT"] == i], weights=w[s["NINCPCTLECAT"] == i]) for i in range(1, 13)}
for _, r in fe.iterrows():
    check(f"F1_{int(r['NINCPCTLECAT'])}", f"SCF windfall MPC, usual-income group {int(r['NINCPCTLECAT'])}, vs FEDS note Fig 3 (pp)",
          mp[int(r["NINCPCTLECAT"])], r["feds_note_fig3"], 1.0)
check("F2", "SCF windfall MPC overall = FEDS note (22.35)", np.average(s["MPSPEND"], weights=w), 22.35, 0.01)
gr = pd.read_csv(OUT / "us_lvt_mpc_grades.csv").set_index("decile")
md = pd.Series([np.average(s["MPSPEND"][dec == i], weights=w[dec == i]) / 100 for i in range(1, 11)], index=DEC)
check("F3", "measured MPC by income decile recomputed (max abs gap)", float((md - gr["measured_windfall"]).abs().max()), 0.0, 1e-9)
sc = B.mpc_schedules()
check("F4", "post mid schedule = bridge.mpc_schedules (max abs gap)", float(np.abs(gr["post_mid"].values - sc["mid"].values).max()), 0.0, 1e-9)
mono = pd.read_csv(B.REBUILD / "out" / "us_mpc_schedules.csv").set_index("decile")["mpc_mid_monotone_fig5_fig6_diagnostic"]
check("F5", "monotone diagnostic schedule = rebuild CSV (max abs gap)", float((gr["post_monotone_diag"] - mono.loc[DEC]).abs().max()), 0.0, 1e-9)

# %% G: macro
mac = pd.read_csv(OUT / "us_lvt_macro_channels.csv").set_index("channel")
vsh = B.vatable_share_aggregate(m)
check("G1", "VAT price step at 80% pass-through (rebuild: 7.4%)", mac.loc["price level step (80-100% pass-through)", "low"], 100 * 0.15 * vsh * 0.8, 1e-9)
check("G2", "VAT price step at 100% pass-through (rebuild: 9.3%)", mac.loc["price level step (80-100% pass-through)", "high"], 100 * 0.15 * vsh, 1e-9)
check("G3", "LVT price step is zero", mac.loc["price level step", "central"], 0.0, 0)
lev = pd.read_csv(OUT / "us_lvt_vat_levy.csv")
NW = (w * s["NETWORTH"].values).sum()
Ctot = inp["ce_consumption_bn"] * 1e9
for _, r in lev.iterrows():
    check(f"G4_{r['lam']}_{r['mpw']}", f"VAT levy channel recomputed: -mpw x lambda x 8% x net worth (lambda {r['lam']}, {r['mpw']})",
          r["pct_ce_consumption"], -100 * r["mpw_value"] * r["lam"] * 0.08 * NW / Ctot, 1e-9)
ltv = pd.read_csv(OUT / "us_lvt_ltv.csv")
check("G5", "aggregate LTV of SCF owners before (sum MRTHEL / sum HOUSES)", float(ltv["ltv_aggregate_before"].iloc[0]),
      (w * s["MRTHEL"]).sum() / (w * s["HOUSES"]).sum(), 1e-9)
V0 = s["HOUSES"].values
M = s["MRTHEL"].values
loss = phi1 * s_cal * np.clip(V0, 0, None)
V1 = V0 - loss
mort = (V0 > 0) & (M > 0)
with np.errstate(divide="ignore", invalid="ignore"):
    cross = mort & (M / np.where(V0 > 0, V0, 1) <= 0.8) & (M / np.where(V1 > 0, V1, 1e-9) > 0.8)
col = pd.read_csv(OUT / "us_lvt_collateral.csv")
cr = col[(col["scenario"] == "LVT_bridge_L1") & (col["design"] == "immediate") & (col["threshold"] == 0.8) & col["measure"].str.startswith("m1")].iloc[0]
check("G6", "owners crossing 80% LTV (bridge L1 m1, immediate), millions, recomputed", (w * cross).sum() / 1e6, cr["n_cross_m"], 1e-6)
check("G7", "their lost equity, $bn, recomputed", (w * loss * cross).sum() / 1e9, cr["lost_equity_crossers_bn"], 1e-6)
full = ltv[(ltv["scenario"] == "LVT_full_L1") & (ltv["design"] == "immediate") & ltv["measure"].str.startswith("m1")].iloc[0]
check("G8", "aggregate LTV after full capture (memo 7.1: 26% -> 48% on Z.1 aggregates)", full["ltv_aggregate_after"], 0.48, 0.02)
lfl = ltv[ltv["design"] == "land_to_zero"].iloc[0]
z_lfl = zv("LA153165105", "A_mean", 2024) / (zv("LM155035005", "A_mean", 2024) - L_hh)
check("G8b", "memo 7.1 like for like (land price to zero, 2024): Z.1 mortgages / (HH real estate - land), recomputed", lfl["z1_ltv_land_to_zero"], z_lfl, 1e-9)
check("G8c", "memo 7.1 like for like: SCF owners' LTV with the land price at zero, recomputed (sum MRTHEL / sum (HOUSES - s x HOUSES))",
      lfl["ltv_aggregate_after"], (w * M).sum() / (w * np.maximum(V0 - s_cal * np.clip(V0, 0, None), 0)).sum(), 1e-9)
check("G8d", "memo 7.1 like for like: SCF within about one point of Z.1 (26% -> 48%)", lfl["ltv_aggregate_after"], lfl["z1_ltv_land_to_zero"], 0.015)
cap = pd.read_csv(OUT / "us_lvt_capitalization.csv")
shock = pd.read_csv(REPO / "three-taxes" / "data" / "lvt_shock.csv").set_index("design")["price_drop"]
for _, r in cap[cap["measure"].str.startswith("m1")].iterrows():
    if r["design"] == "immediate":
        tgt = r["phi"]
    elif r["design"] == "increment":                       # one convention: the repo table for every design
        tgt = shock["increment-only (grandfather r0)"] * r["phi"] / 0.98
    else:
        tgt = shock[f"phase-in {r['design'].split('_')[1]}"] * r["phi"] / 0.98
    check(f"G9_{r['scenario']}_{r['design']}", f"capitalized share lost at announcement ({r['scenario']}, {r['design']})", r["loss_fraction"], tgt, 1e-9)
lp = pd.read_csv(OUT / "us_lvt_loop.csv")
for _, r in lp[lp["scenario"].str.startswith("LVT") & lp["closed_form"].notna()].iterrows():
    check(f"G10_{r['scenario']}_{r['ls']}", f"loop: iterated extra dividend = T5 closed form phi*ls*R0/(1-phi*ls*q) ({r['scenario']}, {r['ls']})",
          r["extra_dividend"], r["closed_form"], 1e-4, "rel")
non = pd.read_csv(OUT / "us_lvt_nonoccupier.csv")
for _, r in non.iterrows():
    ph_ = float(phi[(phi["rate"] == r["scenario"].split("_")[1]) & (phi["base"] == r["scenario"].split("_")[2]) & phi["measure"].str.startswith("m1")]["phi"].iloc[0])
    check(f"G11_{r['scenario']}_{r['grade']}", f"non-occupier capitalized loss = phi x non-occupier land ({r['scenario']})",
          r["nonocc_capitalized_loss_bn"] / r["nonocc_bill_bn"], 1.0 / inp["r_m1"], 1e-9, "rel")

# %% K: the headline - each crosser counted once
# The crossers' lost equity is their own-home bills capitalized (bill = r x lost equity at the immediate design), the
# flow already charges those bills at the decile MPC, so the clean reading adds only a credit effect on the lost
# borrowing capacity; the T4-overlap reading (flow + 6c x lost equity) is a band edge. Recomputed here from the SCF file.
mpc_mid = sc["mid"].values[dec - 1]
Ctot_bn = inp["ce_consumption_bn"]
cap = np.maximum(0, 0.8 * V0 - M) - np.maximum(0, 0.8 * V1 - M)
bill_own = phi1 * r1 * s_cal * np.clip(V0, 0, None)                      # $ per year, the immediate-design own-home bill
cap_bn = (w * cap * cross).sum() / 1e9
eq_bn = (w * loss * cross).sum() / 1e9
billx_bn = (w * bill_own * cross).sum() / 1e9
respx_bn = (w * mpc_mid * bill_own * cross).sum() / 1e9
check("K1", "crossers' lost borrowing capacity (80%, bridge L1 m1), $bn, recomputed", cap_bn, cr["lost_capacity_crossers_bn"], 1e-6, "rel")
check("K2", "crossers' own-home bills, $bn/yr, recomputed", billx_bn, cr["crossers_own_bills_bn"], 1e-6, "rel")
check("K3", "T4: crossers' lost equity = their own-home bills / r (the same money)", cr["lost_equity_crossers_bn"] * r1, cr["crossers_own_bills_bn"], 1e-9, "rel")
check("K4", "crossers' bill response inside the flow (mid schedule), $bn/yr, recomputed", respx_bn, cr["crossers_bill_response_mid_bn"], 1e-6, "rel")
liquid = (s["LIQ"] + s["STOCKS"] + s["BOND"] + s["NMMF"] - s["CCBAL"]).values
inc = s["INCOME"].clip(lower=0).values
htm = liquid <= inc / 52.0
liq3 = liquid >= inc / 4.0
check("K5", "hand-to-mouth crossers (KVW biweekly), millions, recomputed", (w * cross * htm).sum() / 1e6, cr["n_cross_htm_m"], 1e-6, "rel")
check("K6", "hand-to-mouth crossers' lost equity, $bn, recomputed", (w * loss * cross * htm).sum() / 1e9, cr["lost_equity_crossers_htm_bn"], 1e-6, "rel")
check("K7", "hand-to-mouth crossers' lost borrowing capacity, $bn, recomputed", (w * cap * cross * htm).sum() / 1e9, cr["lost_capacity_crossers_htm_bn"], 1e-6, "rel")
check("K8", "share of the crossers' lost equity held by families with >= 3 months' income in liquid assets", (w * loss * cross * liq3).sum() / 1e9 / eq_bn,
      cr["liquid3m_share_of_lost_equity"], 1e-6, "rel")
flow = {g: float(imp[(imp["tax"] == "LVT") & (imp["rate"] == "bridge") & (imp["base"] == "L1") & imp["measure"].str.startswith("m1")
                     & (imp["grade"] == g) & (imp["defer"] == "none")]["impulse_pct"].iloc[0]) for g in ["dn_mid", "dn_high", "dn_low", "dn_meas"]}
pc = lambda x_bn, c: -100.0 * c * x_bn / Ctot_bn
nl1 = mac.loc["net demand at impact (flow + collateral; bridge, L1, immediate)"]
check("K9", "headline L1 central = flow (mid) + 6c x crossers' lost capacity", nl1["central"], flow["dn_mid"] + pc(cap_bn, 0.06), 1e-9)
check("K10", "headline L1 band low = flow (high schedule) + 7c (top of Mian-Rao-Sufi) x lost capacity", nl1["low"], flow["dn_high"] + pc(cap_bn, 0.07), 1e-9)
check("K11", "headline L1 band high = flow (low schedule) + 4.7c (Aladangady) x lost capacity", nl1["high"], flow["dn_low"] + pc(cap_bn, 0.047), 1e-9)
check("K12", "headline L1 at the 10c stress value (labelled, outside the band)", nl1["stress_10c"], flow["dn_high"] + pc(cap_bn, 0.10), 1e-9)
t4 = mac.loc["net demand at impact, includes the T4 overlap (flow + 6c x crossers' lost equity; bridge, L1)"]
check("K13", "T4-overlap edge L1 = flow (mid) + 6c x crossers' lost equity (the earlier central)", t4["central"], flow["dn_mid"] + pc(eq_bn, 0.06), 1e-9)
stk = mac.loc["net demand at impact, crossers' stock response instead of their bill (bridge, L1)"]
check("K14", "never both: T4 edge - stock-instead-of-bill reading = the crossers' bill response counted twice", t4["central"] - stk["central"],
      -100.0 * respx_bn / Ctot_bn, 1e-9)
hm = mac.loc["net demand at impact, only hand-to-mouth crossers respond (bridge, L1)"]
check("K15", "who responds: hand-to-mouth crossers only = flow (mid) + 6c x their lost capacity", hm["central"],
      flow["dn_mid"] + pc((w * cap * cross * htm).sum() / 1e9, 0.06), 1e-9)
ms = mac.loc["net demand at impact, measured windfall MPCs (bridge, L1)"]
check("K16", "measured windfall MPCs: flow (decile means) + 6c x lost capacity", ms["central"], flow["dn_meas"] + pc(cap_bn, 0.06), 1e-9)
# L2: corporate land on the wealth reading (3.5c on the capitalized loss instead of the bill at the decile MPC)
phi2 = float(phi[(phi["rate"] == "bridge") & (phi["base"] == "L2") & phi["measure"].str.startswith("m1")]["phi"].iloc[0])
ps = N * shares
q2 = acc[acc["scenario"] == "LVT_bridge_L2_m1"].set_index("decile").loc[DEC]
nfc_d = np.array([(w * Lnfc)[dec == i].sum() for i in range(1, 11)])
nfc_bill = phi2 * r1 * nfc_d / (ps * 12)
loss2 = phi2 * s_cal * np.clip(V0, 0, None)
V1b = V0 - loss2
with np.errstate(divide="ignore", invalid="ignore"):
    cross2 = mort & (M / np.where(V0 > 0, V0, 1) <= 0.8) & (M / np.where(V1b > 0, V1b, 1e-9) > 0.8)
cap2_bn = (w * cross2 * (np.maximum(0, 0.8 * V0 - M) - np.maximum(0, 0.8 * V1b - M))).sum() / 1e9
bbar = m["budget_bar"]
for kk, mpw in [("mid", 0.035), ("low", 0.02), ("high", 0.05)]:
    dC = sc["mid"].values * (q2["net"].values + nfc_bill) - mpw * phi2 * nfc_d / (ps * 12)
    fw_ = 100 * float((wd * dC).sum()) / bbar
    if kk == "mid":
        fw_mid = fw_
nl2 = mac.loc["net demand at impact (flow + collateral; bridge, L2, immediate)"]
check("K17", "headline L2 central: corporate land on the wealth reading (3.5c) + 6c x L2 crossers' lost capacity", nl2["central"],
      fw_mid + pc(cap2_bn, 0.06), 1e-9)
f2 = float(imp[(imp["tax"] == "LVT") & (imp["rate"] == "bridge") & (imp["base"] == "L2") & imp["measure"].str.startswith("m1")
               & (imp["grade"] == "dn_mid") & (imp["defer"] == "none")]["impulse_pct"].iloc[0])
check("K18", "L2 with corporate land on the flow reading = flow (mid) + 6c x lost capacity",
      mac.loc["net demand at impact, corporate land on the flow reading (bridge, L2)", "central"], f2 + pc(cap2_bn, 0.06), 1e-9)
check("K19", "L2 crossers' lost capacity, $bn, recomputed", cap2_bn,
      col[(col["scenario"] == "LVT_bridge_L2") & (col["design"] == "immediate") & (col["threshold"] == 0.8) & col["measure"].str.startswith("m1")]
      ["lost_capacity_crossers_bn"].iloc[0], 1e-6, "rel")
vat_c = mac.loc["net demand at impact, lambda = 0.35 (flow + levy)", "central"]
check("K20", "VAT net demand at impact unchanged (flow + levy at lambda 0.35, 3.5c)", vat_c,
      float(imp[(imp["tax"] == "VAT") & (imp["grade"] == "dn_mid")]["impulse_pct"].iloc[0]) - 100 * 0.035 * 0.35 * 0.08 * NW / Ctot, 1e-9)
pce = inp["pce_2024_bn"]
dem = mac[mac["unit"] == "% of consumption"]
check("K21", "every demand row as % of PCE = % of CE consumption x CE/PCE (0.455), max abs gap",
      float((dem["central_pct_pce"] - dem["central"] * Ctot_bn / pce).abs().max()), 0.0, 1e-9)
check("K22", "CE consumption / PCE = 0.455", Ctot_bn / pce, 0.455, 0.0005)
hd = pd.read_csv(OUT / "us_lvt_headline.csv")
hq = lambda b, c, rd: hd[(hd["base"].fillna("") == b) & (hd["corporate_land"].fillna("") == c) & (hd["reading"] == rd)].iloc[0]
check("K23", "headline CSV = macro table (L1 clean central)", hq("L1", "not in base", "clean")["central"], nl1["central"], 1e-9)
check("K24", "headline CSV = macro table (L2 clean central, corporate land on the wealth reading)", hq("L2", "wealth", "clean")["central"], nl2["central"], 1e-9)
rb = pd.read_csv(OUT / "us_lvt_robustness.csv")
rb1 = rb[(rb["base"] == "L1") & rb["collateral_capacity_mid_pct"].notna()]
check("K25", "robustness, L1 rows: net (clean) = flow + 6c x lost capacity, max abs gap",
      float((rb1["net_clean_mid_pct"] - rb1["impulse_dn_mid"] - rb1["collateral_capacity_mid_pct"]).abs().max()), 0.0, 1e-9)
lpm = lp[(lp["scenario"] == "LVT_bridge_L1_m1") & (lp["ls"] == "mid")].iloc[0]
lpv = lp[(lp["scenario"] == "VAT") & (lp["ls"] == "mid") & (lp["measure"].astype(str).str.startswith("m1"))].iloc[0]
Lore = s_cal * s["ORESRE"].clip(lower=0).values
key1 = np.array([(w * Lore)[dec == i].sum() for i in range(1, 11)]) / (w * Lore).sum()
hold_mpc = float((key1 * sc["mid"].values).sum())
inc_l = 0.4 * lpm["rent_bar_round0"] * 12 * S_CE / 1e9
check("K27", "loop: the LVT's land-rent increment ($bn/yr) = 0.4 x round-0 rent bar x CE shares x 12", lpm["land_rent_increment_bn"], inc_l, 1e-9, "rel")
check("K28", "loop: the rental-land holders' uncredited receipt at their MPC (rental-land-weighted mid schedule), % of consumption, LVT",
      lpm["uncredited_receipt_pct"], 100 * hold_mpc * inc_l / Ctot_bn, 1e-9)
check("K29", "loop: the same for the VAT's own (smaller) increment", lpv["uncredited_receipt_pct"],
      100 * hold_mpc * 0.4 * lpv["rent_bar_round0"] * 12 * S_CE / 1e9 / Ctot_bn, 1e-9)
check("K30", "loop: the rent bar as a share of rent spending (a rent-price effect on a fixed stock)", lpm["rent_bar_share_of_rent_spending"],
      lpm["rent_bar_round0"] / float(m["Cbar"]["Rented dwellings"]), 1e-9, "rel")
check("K26", "robustness main rows = the headline (L1 and L2 clean centrals), max abs gap",
      max(abs(float(rb[rb["variant"].str.startswith("main: SCF 2025") & (rb["base"] == b_)]["net_clean_mid_pct"].iloc[0]) - v_)
          for b_, v_ in [("L1", nl1["central"]), ("L2", nl2["central"])]), 0.0, 1e-9)

# %% H: deliverables exist
for f in ["us_lvt_net_by_decile.png", "us_lvt_demand_shifts_top15.png", "us_lvt_who_pays.png", "us_lvt_macro_channels.png"]:
    check_true(f"H_{f}", f"figure written: figures/{f}", (LVT / "figures" / f).exists())

# %% summary
res = pd.DataFrame(ROWS)
res.to_csv(OUT / "check_lvt_us.csv", index=False, float_format="%.10g")
n_pass, n_fail = int((res["status"] == "PASS").sum()), int((res["status"] == "FAIL").sum())
print(f"check_lvt_us: {n_pass} PASS, {n_fail} FAIL, {int((res['status'] == 'INFO').sum())} INFO of {len(res)}")
if n_fail:
    print(res[res["status"] == "FAIL"][["id", "check", "value", "target", "gap"]].to_string(index=False))
print(res[res["status"] == "INFO"]["check"].to_string(index=False))
sys.exit(1 if n_fail else 0)
