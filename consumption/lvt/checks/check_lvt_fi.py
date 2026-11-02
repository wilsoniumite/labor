# check_lvt_fi.py - re-derives the Finnish LVT unit's headline numbers from the tidy files with independent code
# (it reads the tidy CSVs and the vendored yield files directly, and uses bridge.py only for the rebuilt VAT side and
# the category machinery), checks the accounting identities, and checks that the US numbers in the comparison are
# the US unit's current outputs. Writes consumption/lvt/out/check_lvt_fi.csv and prints a summary.
#
# Run from the repo root:  venv/bin/python -I consumption/lvt/checks/check_lvt_fi.py   (after run_lvt_fi.py)

# %% setup
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent                      # consumption/lvt/checks
LVT = HERE.parent
THREAD = LVT.parent
sys.path.insert(0, str(THREAD / "rebuild" / "code"))

import numpy as np
import pandas as pd
from scipy.stats import lognorm, norm

import bridge as B

TIDY, OUT, FIG = THREAD / "data" / "tidy", LVT / "out", LVT / "figures"
RAW = THREAD / "data" / "raw"
DEC = [f"d{i:02d}" for i in range(1, 11)]
Q = ["q1", "q2", "q3", "q4", "q5"]
rows = []


def check(cid, desc, value, ref, tol, kind="identity", note=""):
    # the outputs are stored at 10 significant digits (float_format %.10g): allow that storage rounding on top of tol
    tol = max(tol, 2e-9 * max(1.0, abs(float(ref)), abs(float(value))))
    ok = abs(float(value) - float(ref)) <= tol
    rows.append(dict(check_id=cid, kind=kind, description=desc, value=float(value), reference=float(ref), diff=float(value) - float(ref),
                     tolerance=tol, result="PASS" if ok else "FAIL", note=note))


def info(cid, desc, value, note=""):
    rows.append(dict(check_id=cid, kind="info", description=desc, value=float(value), reference=np.nan, diff=np.nan, tolerance=np.nan,
                     result="INFO", note=note))


out = {n: pd.read_csv(OUT / f"fi_lvt_{n}.csv") for n in ["phi", "accounting_by_quintile", "impulse", "demand_shifts", "collateral", "macro_channels",
                                                         "us_compare", "land_by_decile", "concentration", "liquidity", "within_decile",
                                                         "vat_levy", "loop", "deferral", "tenure_aware", "headline", "inputs", "yields",
                                                         "yield_years", "review", "robustness", "collateral_lognormal_totals", "nonoccupier",
                                                         "land_evidence"]}
for n in ("impulse", "demand_shifts", "tenure_aware", "accounting_by_quintile"):
    out[n]["base"] = out[n]["base"].fillna("")

# %% A. yields: Eurostat annual = mean of Eurostat monthly = mean of ECB monthly (2022-2025)
ja = json.loads((RAW / "eurostat" / "data" / "irt_lt_mcby_a_FI.json").read_text())
jm = json.loads((RAW / "eurostat" / "data" / "irt_lt_mcby_m_FI.json").read_text())
inv = lambda j: {v: k for k, v in j["dimension"]["time"]["category"]["index"].items()}
ya = {inv(ja)[int(k)]: v for k, v in ja["value"].items()}
ym = pd.Series({inv(jm)[int(k)]: v for k, v in jm["value"].items()})
ec = pd.read_csv(RAW / "ecb" / "data" / "IRS_M.FI.L.L40.CI.0000.EUR.N.Z.csv", usecols=["TIME_PERIOD", "OBS_VALUE"])
for y in (2022, 2023, 2024, 2025):
    mm = ym[ym.index.str.startswith(str(y))]
    ee = ec[ec["TIME_PERIOD"].astype(str).str.startswith(str(y))]["OBS_VALUE"]
    check(f"A{y}a", f"Eurostat annual {y} = mean of its 12 monthly values", ya[str(y)], mm.mean(), 0.015, "crosscheck", f"{len(mm)} months")
    check(f"A{y}b", f"ECB monthly mean {y} = Eurostat monthly mean", ee.mean(), mm.mean(), 0.005, "crosscheck", f"{len(ee)} months")
Y22 = ya["2022"] / 100.0
check("A0", "yield used for 2022 (fi_lvt_inputs)", float(out["inputs"].set_index("item").loc["yield_2022", "value"]) / 100.0, Y22, 1e-12)

# %% B. land: calibration to the balance sheet, carry, decile holdings (independent recomputation)
w = pd.read_csv(TIDY / "fi_wealth_2023_deciles.csv")
wv = lambda c, m="mean": w[(w["component"] == c) & (w["measure"] == m)].set_index("decile")["value"].astype(float)
nf = pd.read_csv(TIDY / "fi_nonfin_assets_long.csv")
bs = lambda s, i, y: float(nf[(nf["sector"] == s) & (nf["instrument"] == i) & (nf["year"] == y) & (nf["measure"] == "stock")]["value"].iloc[0])
N = wv("net_wealth", "households_holding").reindex(DEC)
HWd = (wv("main_residence") + wv("other_residential_property") + wv("free_time_residences")).reindex(DEC)
FFBd = wv("forest_farmland_business").reindex(DEC)
HW, FFB = float((HWd * N).sum()) / 1e6, float((FFBd * N).sum()) / 1e6
s_d = 1 - bs("S14", "N111", 2023) / HW
s_f = (bs("S14", "N211", 2023) - s_d * HW) / FFB
carry = bs("S14", "N211", 2022) / bs("S14", "N211", 2023)
inp = out["inputs"].set_index("item")["value"]
check("B1", "s_d (residual: 1 - N111 / survey dwellings, 2023)", float(inp["s_d_residual"]), s_d, 1e-9)
check("B2", "s_f (N211 residual after dwelling land)", float(inp["s_f_residual"]), s_f, 1e-9)
check("B3", "carry 2023 -> 2022 = N211 end-2022 / end-2023", float(inp["carry_2023_to_2022"]), carry, 1e-12)
L2 = (s_d * HWd + s_f * FFBd) * carry
check("B4", "household land 2022 over the survey households = N211 S14 2022 (EUR m)", float((L2 * N).sum()) / 1e6, bs("S14", "N211", 2022), 0.5)
ld = out["land_by_decile"].set_index("decile")
check("B5", "B2 land per household by decile (max abs diff, EUR)", float((ld["B2"] - L2).abs().max()), 0.0, 1e-3, "identity", "values of EUR 10,000-125,000 stored at 10 significant digits")
check("B6", "N211/(N211+N111) 2022 (the upper bound)", bs("S14", "N211", 2022) / (bs("S14", "N211", 2022) + bs("S14", "N111", 2022)), 0.2591, 0.0005,
      "crosscheck", "README_fin: 25.9%")
Lq = pd.Series([(L2[DEC[2 * i]] + L2[DEC[2 * i + 1]]) / 2 for i in range(5)], index=Q)

# %% C. the bridge-equivalent rate and full capture, from scratch with equal-household weights (coherent)
m = B.build_fi_model(convention="coherent")
mp = B.build_fi_model(convention="post")
accv = B.fi_vat_accounting(m)
accp = B.fi_vat_accounting(mp)
div_c, div_p = float(accv["dividend"].iloc[0]), float(accp["dividend"].iloc[0])
check("C1", "VAT dividend, post convention (rebuild: 193.01)", div_p, 193.0054, 0.001, "crosscheck")
check("C2", "VAT dividend, coherent convention (rebuild: 198.82)", div_c, 198.8246, 0.001, "crosscheck")
hh = m["units"].loc[Q, "households"].astype(float)
sh = m["units"].loc[Q, "shares"].astype(float)
mean_ps = float((hh * Lq).sum() / (hh * sh).sum())                    # land value per payment share, equal households
tau_b = div_c * 12.0 / mean_ps                                       # monthly dividend x 12 / land value per share
ph = out["phi"]
pr = ph[(ph["base"] == "B2") & (ph["measure"] == "m1") & (ph["yield_year"] == 2022) & (ph["convention"] == "coherent") & ~ph["label"].str.contains("law")].iloc[0]
check("C3", "bridge-equivalent charge on land value (B2, % a year)", float(pr["tau_bridge_pct_of_land_value"]), 100 * tau_b, 1e-6)
check("C4", "bridge-equivalent phi (B2, m1, 2022) = charge / yield", float(pr["phi_bridge"]), tau_b / Y22, 1e-6)
div_full = 0.98 * Y22 * mean_ps / 12.0
check("C5", "full-capture dividend (B2, m1, 2022), EUR/share/month", float(pr["dividend_full"]), div_full, 1e-6)
check("C6", "full-capture dividend / VAT dividend", float(pr["share_of_vat_dividend"]), div_full / div_c, 1e-9)
pr2 = ph[(ph["base"] == "B2") & (ph["measure"] == "m2") & (ph["yield_year"] == 2022) & (ph["convention"] == "coherent")].iloc[0]
check("C7", "full-capture dividend at yield + 1.5 (B2)", float(pr2["dividend_full"]), 0.98 * (Y22 + 0.015) * mean_ps / 12.0, 1e-6)
rev_full = div_full * float((hh * sh).sum()) * 12 / 1e6
check("C8", "full-capture revenue = 0.98 x yield x land held by HBS households (EUR m)", rev_full,
      0.98 * Y22 * float((L2 * N).sum()) / 1e6 * float(hh.sum()) / float(N.sum()), 1.0, "identity",
      "quintile pair means weighted by HBS households against the aggregate scaled by households: 0.03% apart")
for yy in (2023, 2024, 2025):
    r = ph[(ph["base"] == "B2") & (ph["measure"] == "m1") & (ph["yield_year"] == yy) & (ph["convention"] == "coherent")].iloc[0]
    check(f"C9_{yy}", f"full-capture share of the VAT dividend at the {yy} yield", float(r["share_of_vat_dividend"]),
          0.98 * ya[str(yy)] / 100 * mean_ps / 12.0 / div_c, 1e-9)
info("C10", "household land rent can fund the bridge's dividend at full capture (1 = yes) on m1/m2 at 2022-25 yields",
     float((ph[(ph["base"] == "B2") & ph["measure"].isin(["m1", "m2"]) & (ph["convention"] == "coherent")]["share_of_vat_dividend"] >= 1).any()),
     "0: no yield-based case funds it")

# %% D. incidence: balanced budgets, nets, % of budget (both conventions)
acc = out["accounting_by_quintile"]
for conv, mm_ in [("coherent", m), ("post", mp)]:
    for base in ["B1", "B2"]:
        for rate in ["bridge", "full_m1", "full_m2"]:
            a = acc[(acc["convention"] == conv) & (acc["instrument"] == "LVT") & (acc["base"] == base) & (acc["rate"] == rate)].set_index("quintile").loc[Q]
            check(f"D_{conv}_{base}_{rate}_bal", f"sum_q w_q net_q = 0 ({conv}, {base}, {rate})", float((mm_["w"] * a["net"]).sum()), 0.0, 1e-6,
                  "identity", "nets of EUR 10-200 stored at 10 significant digits")
            Lb = ld.groupby("quintile")[base].mean().reindex(Q) if base == "B1" else Lq
            bill = a["tau"].iloc[0] * Lb / (12.0 * mm_["units"].loc[Q, "shares"])
            check(f"D_{conv}_{base}_{rate}_bill", f"bill_q = tau x land per share / 12 (max abs, {conv}, {base}, {rate})",
                  float((a["bill"] - bill).abs().max()), 0.0, 1e-6, "identity", "values stored at 10 significant digits")
a = acc[(acc["convention"] == "coherent") & (acc["base"] == "B2") & (acc["rate"] == "bridge")].set_index("quintile")
check("D1", "LVT bridge net Q1 (coherent, B2), EUR", float(a.loc["q1", "net"]), div_c - tau_b * Lq["q1"] / (12 * sh["q1"]), 1e-8)
check("D2", "LVT bridge net Q5 (coherent, B2), EUR", float(a.loc["q5", "net"]), div_c - tau_b * Lq["q5"] / (12 * sh["q5"]), 1e-8)
check("D3", "LVT bridge net Q5 % of budget", float(a.loc["q5", "net_pct_budget"]), 100 * float(a.loc["q5", "net"]) / float(m["budget"]["q5"]), 1e-9)

# %% E. inside the deciles: the owner model's split, re-derived with scipy's lognorm
wd = out["within_decile"]
x = wd[(wd["convention"] == "coherent") & (wd["base"] == "B2")].set_index("decile").loc[DEC]
p_own = wv("main_residence", "participation_rate_pct").reindex(DEC) / 100
sig = (np.log(wv("main_residence", "p75")) - np.log(wv("main_residence", "p25"))).reindex(DEC) / (2 * norm.ppf(0.75))
Lown = L2 / p_own
Lstar = mean_ps * np.repeat(sh.values, 2)
P = np.array([lognorm(s=sig[d], scale=Lown[d] * np.exp(-sig[d] ** 2 / 2)).sf(Lstar[i]) for i, d in enumerate(DEC)])
check("E1", "payer share of owners by decile (max abs diff, scipy lognorm)", float(np.abs(x["payer_share_of_owners"].values - P).max()), 0.0, 1e-9)
check("E2", "households paying net under the LVT, all deciles", float((x["payer_share_of_households"] * x["households"]).sum() / x["households"].sum()),
      float((p_own.values * P * N.values).sum() / N.sum()), 1e-9)
check("E3", "receipts - payments = net, every decile (max abs, EUR/share/month)",
      float((x["gross_receipts_eur_share_month_bridge"] - x["gross_payments_eur_share_month_bridge"] - x["net_eur_share_month_bridge"]).abs().max()), 0.0, 1e-6)

# %% F. liquidity: hand-to-mouth shares re-derived
q25, q50, q75 = (wv("deposits", k).reindex(DEC) for k in ("p25", "median", "p75"))
part = wv("deposits", "participation_rate_pct").reindex(DEC) / 100
inc = wv("disposable_income", "median").reindex(DEC)
sd = (np.log(q75) - np.log(q25)) / (2 * norm.ppf(0.75))
h = ((1 - part) + part * lognorm(s=sd.values, scale=q50.values).cdf((inc / 24).values)).values
check("F1", "hand-to-mouth share by decile, deposits <= income/24 (max abs diff)", float(np.abs(out["liquidity"].set_index("decile").loc[DEC, "htm_all_half_month"].values - h).max()),
      0.0, 1e-9)
info("F2", "hand-to-mouth share D1 / D10 (all households)", float(h[0]), f"D10 {h[-1]:.3f}")

# %% G. flows: the post's method, re-derived; bars; signs
imp = out["impulse"]
sched = B.fi_mpc_schedules()["mid"].values
for inst, base, rate in [("VAT", "", "bridge"), ("LVT", "B2", "bridge"), ("LVT", "B2", "full_m1"), ("LVT", "B2", "full_m2"), ("LVT", "B1", "full_m1")]:
    if inst == "VAT":
        net = accv["net"].values
    else:
        net = acc[(acc["convention"] == "coherent") & (acc["instrument"] == "LVT") & (acc["base"] == base) & (acc["rate"] == rate)].set_index("quintile").loc[Q, "net"].values
    flow = 100 * float((m["w"].values * sched * net).sum()) / m["budget_bar"]
    r = imp[(imp["convention"] == "coherent") & (imp["instrument"] == inst) & (imp["base"].fillna("") == base) & (imp["rate"] == rate) &
            (imp["grade"] == "post_mid") & (imp["defer"] == "none")]
    check(f"G_{inst}_{base}_{rate}", f"flow impulse, post's method, % of consumption ({inst} {base} {rate})", float(r["flow_pct_consumption"].iloc[0]), flow, 1e-9)
shf = out["demand_shifts"]
v = shf[(shf["convention"] == "coherent") & (shf["instrument"] == "VAT") & (shf["grade"] == "post_mid")].set_index("category")
l_ = shf[(shf["convention"] == "coherent") & (shf["instrument"] == "LVT") & (shf["base"] == "B2") & (shf["rate"] == "bridge") & (shf["grade"] == "post_mid")].set_index("category")
chart = m["chart"]
check("G1", "charted LVT bars with the VAT bar's sign (of 37)", float((np.sign(v.loc[chart, "dEUR"]) == np.sign(l_.loc[chart, "dEUR"])).sum()), 37, 0)
flow_l = float((m["w"].values * sched * acc[(acc["convention"] == "coherent") & (acc["base"] == "B2") & (acc["rate"] == "bridge")].set_index("quintile").loc[Q, "net"].values).sum())
check("G2", "all LVT bars / flow = the division-parent over-allocation (rebuild: 1.052)", float(l_["dEUR"].sum()) / flow_l, 1.0522, 0.002, "crosscheck")
vp = shf[(shf["convention"] == "post") & (shf["instrument"] == "VAT") & (shf["grade"] == "post_mid")].set_index("category")
check("G3", "VAT rent bar on the post's euro conversion (rebuild 4.928; published 4.92)", float(vp.loc["04.1 Actual rents", "dEUR_post_conversion"]), 4.9276, 0.001,
      "crosscheck")
ten = out["tenure_aware"]
tl = ten[(ten["convention"] == "coherent") & (ten["instrument"] == "LVT") & (ten["base"] == "B2") & (ten["grade"] == "post_mid")]
check("G4", "tenure-aware LVT bars over all categories / flow (Engel, division parents)", float(tl["dEUR"].sum()) / flow_l, 1.05, 0.03, "identity",
      "the tenure baskets keep adding-up to the division-parent factor")
info("G5", "tenure-aware LVT rent bar / quintile-netted rent bar", float(tl.set_index("category").loc["04.1 Actual rents", "dEUR"] / l_.loc["04.1 Actual rents", "dEUR"]))

# %% H. macro: price step, levy, collateral (US-shape population rebuilt here), the headline
vsh = float(accv["Cbar_v"].iloc[0]) / m["budget_bar"]
mac = out["macro_channels"].set_index("channel")
check("H1", "VAT price step, central (0.15 x VAT-able share x 0.9), %", float(mac.loc["price level step (80-100% pass-through)", "central"]), 100 * 0.15 * vsh * 0.9, 1e-9)
nw = float(wv("net_wealth")["total"]) * float(wv("net_wealth", "households_holding")["total"]) / 1e6
nf_ = pd.read_csv(TIDY / "fi_na_hfce_coicop2018_long.csv", dtype={"coicop_code": str})
defl = (nf_[(nf_["transaction"] == "P31DCK") & (nf_["coicop_code"] == "0") & (nf_["year"] == 2023) & (nf_["measure"] == "current_prices")]["value"].iloc[0] /
        nf_[(nf_["transaction"] == "P31DCK") & (nf_["coicop_code"] == "0") & (nf_["year"] == 2023) & (nf_["measure"] == "previous_year_prices")]["value"].iloc[0])
C = m["budget_bar"] * float((hh * sh).sum()) * 12 / 1e6
st = 0.15 * vsh * 0.9
check("H2", "VAT levy channel, lambda 0.35, 3.5c (% of consumption)", float(mac.loc["levy channel, lambda = 0.35 (impact; 2-5c per EUR per year)", "central"]),
      -100 * 0.035 * 0.35 * st / (1 + st) * nw / defl / C, 1e-9)
check("H3", "HBS consumption = 39,808 x 2,919,000 (EUR m)", C, 39808 * 2.919, 5.0, "crosscheck", "the published EUR 39,808 is rounded")
# the US-shape population, rebuilt from the SCF and the 151u/151z aggregates
s = pd.read_csv(TIDY / "scf2025_summary.csv.gz", usecols=["WGT", "HOUSES", "MRTHEL", "INCPCTLECAT"])
s = s[(s["HOUSES"] > 0) & (s["MRTHEL"] > 0)].copy()
s["d"] = np.minimum(s["INCPCTLECAT"].astype(int), 10)
t = pd.read_csv(TIDY / "fi_wealth_2023_tenure.csv")
tv = lambda c, mm2="mean": t[(t["component"] == c) & (t["measure"] == mm2)].set_index("tenure")["value"].astype(float)
n_m = wv("housing_loans", "households_holding").reindex(DEC)
n_o = wv("main_residence", "households_holding").reindex(DEC) - n_m
vm, vo = tv("main_residence")["owner_with_mortgage"], tv("main_residence")["outright_owner"]
k = n_m * vm / (n_m * vm + n_o * vo)
Vm = wv("main_residence").reindex(DEC) * N * k
Vm = Vm * (tv("housing_loans", "households_holding")["owner_with_mortgage"] * vm) / Vm.sum()
A = (wv("housing_loans").reindex(DEC) * N) / Vm
Vbar = Vm / n_m
check("H4", "mortgaged owners' aggregate LTV (151z: 106,965 / 222,127)", float((wv("housing_loans").reindex(DEC) * N).sum() / Vm.sum()), 106965 / 222127, 1e-3,
      "crosscheck")
f = 0.98 * s_d
lc_tot, n_cross = 0.0, 0.0
for i, dd in enumerate(DEC):
    g = s[s["d"] == i + 1]
    wgt = g["WGT"].values
    aus = float((g["MRTHEL"] * g["WGT"]).sum() / (g["HOUSES"] * g["WGT"]).sum())
    vus = float(np.average(g["HOUSES"], weights=wgt))
    ltv = g["MRTHEL"].values / g["HOUSES"].values * A[dd] / aus
    V0 = g["HOUSES"].values * Vbar[dd] / vus
    ww = wgt * n_m[dd] / wgt.sum()
    M = ltv * V0
    cr = (ltv <= 0.8) & (ltv / (1 - f) > 0.8)
    lc = np.maximum(0, 0.8 * V0 - M) - np.maximum(0, 0.8 * V0 * (1 - f) - M)
    lc_tot += float((ww * cr * lc).sum())
    n_cross += float((ww * cr).sum())
col = out["collateral"]
ct = col[(col["method"] == "us_shape") & (col["rate"] == "full_m1") & (col["design"] == "immediate") & (col["threshold"] == 0.8) & (col["decile"] == "total")].iloc[0]
check("H5", "mortgaged owners crossing 80% LTV at full capture (US-shape)", float(ct["n_cross"]), n_cross, 1.0)
check("H6", "their lost borrowing capacity (EUR m, carried to 2022)", float(ct["lost_capacity_meur"]), lc_tot / 1e6 * carry, 0.5)
check("H7", "collateral credit effect, 6c (% of consumption)",
      float(mac.loc["collateral: credit effect on all crossers' lost borrowing capacity (full capture, immediate)", "central"]),
      -100 * 0.06 * lc_tot / 1e6 * carry / C, 1e-6)
hl = out["headline"][out["headline"]["instrument"] == "LVT"].set_index(["rate", "reading"]).sort_index()
flow_f = float(imp[(imp["convention"] == "coherent") & (imp["instrument"] == "LVT") & (imp["base"] == "B2") & (imp["rate"] == "full_m1") &
                   (imp["grade"] == "post_mid") & (imp["defer"] == "none")]["flow_pct_consumption"].iloc[0])
check("H8", "net at impact, flow + credit effect (full capture) = flow + collateral", float(hl.loc[("full_m1", "clean"), "central"]),
      flow_f - 100 * 0.06 * lc_tot / 1e6 * carry / C, 1e-6)
info("H9", "net at impact, full capture, clean reading (% of consumption)", float(hl.loc[("full_m1", "clean"), "central"]),
     f"band [{hl.loc[('full_m1', 'clean'), 'low']:.3f}, {hl.loc[('full_m1', 'clean'), 'high']:.3f}]")
info("H10", "net at impact, full capture, T4-overlap reading", float(hl.loc[("full_m1", "t4"), "central"]))
info("H11", "net at impact, full capture, non-occupiers on the wealth reading", float(hl.loc[("full_m1", "nonocc_wealth"), "central"]))
lp = out["loop"]
r = lp[(lp["instrument"] == "LVT_B2") & (lp["rate"] == "full_m1") & (lp["ls_case"] == "mid") & (lp["landlord_case"] == "mid")].iloc[0]
check("H12", "the loop: fixed point = round-0 dividend / (1 - phi h ls q)", float(r["extra_dividend_total"]),
      0.98 * 0.55 * float(r["ls"]) * float(r["rent_bar_round0"]) / (1 - 0.98 * 0.55 * float(r["ls"]) * float(r["q"])), 2e-4, "identity",
      "the iteration's first-round q against the closed form")

# %% I. the US comparison uses the US unit's current outputs
uc = out["us_compare"].set_index(["block", "item"])
um = pd.read_csv(OUT / "us_lvt_macro_channels.csv").set_index("channel")
ucol = pd.read_csv(OUT / "us_lvt_collateral.csv")
uu = lambda sc, c: float(ucol[(ucol["scenario"] == sc) & (ucol["design"] == "immediate") & (ucol["threshold"] == 0.8) &
                              (ucol["measure"] == "m1_z1hh_x_gs10")][c].iloc[0])
check("I1", "US VAT net at impact in the comparison = us_lvt_macro_channels.csv", float(uc.loc[("VAT, impact (same formulas)", "net demand at impact (flow + levy)"), "US"]),
      float(um.loc["net demand at impact, lambda = 0.35 (flow + levy)", "central"]), 1e-12)
check("I2", "US full-capture flow + credit effect = US flow (full, L1) + US credit effect (full, L1)",
      float(uc.loc[("LVT, same share of rent (full capture, phi 0.98)", "net demand at impact (flow + credit effect)"), "US"]),
      float(um.loc["flow impulse, post's method (full, L1)", "central"]) + uu("LVT_full_L1", "dC_lost_capacity_mid_pct"), 1e-12)
check("I3", "US bridge flow + credit effect = the US unit's headline (clean, L1)",
      float(uc.loc[("LVT, the US bridge's share of rent (phi 0.848)", "net demand at impact (flow + credit effect)"), "US"]),
      float(um.loc["net demand at impact (flow + collateral; bridge, L1, immediate)", "central"]), 1e-9, "crosscheck",
      "fails if the US unit changes its headline again: rerun run_lvt_fi.py")
uin = pd.read_csv(OUT / "us_lvt_inputs.csv").set_index("item")["value"]
info("I4", "US-Finland gap, VAT at impact (same formulas), points", float(uc.loc[("VAT, impact (same formulas)", "net demand at impact (flow + levy)"), "US_minus_FI"]))
info("I5", "US-Finland gap, LVT at phi 0.98, clean reading, points",
     float(uc.loc[("LVT, same share of rent (full capture, phi 0.98)", "net demand at impact (flow + credit effect)"), "US_minus_FI"]))

# %% J. concentration and figures
cc = out["concentration"]
mr = wv("main_residence").reindex(DEC) * N
check("J1", "top income decile's share of main-residence value", float(cc[(cc["country"] == "FI") & (cc["item"] == "main residence")]["top_decile"].iloc[0]),
      float(mr["d10"] / mr.sum()), 1e-12)
fa = wv("financial_assets").reindex(DEC) * N
check("J2", "top income decile's share of financial assets", float(cc[(cc["country"] == "FI") & (cc["item"] == "financial assets")]["top_decile"].iloc[0]),
      float(fa["d10"] / fa.sum()), 1e-12)
for fn in ["fig_fi_funding_gap", "fig_fi_net_by_quintile", "fig_fi_demand_shifts", "fig_fi_macro_channels", "fig_fi_us_compare"]:
    p = FIG / f"{fn}.png"
    check(f"J_{fn}", f"figure exists: {fn}.png", float(p.exists() and p.stat().st_size > 50000), 1.0, 0)

# %% K. the review's numbers (out/fi_lvt_review.csv, fi_lvt_yield_years.csv, the same-year US rows), re-derived here
rv = out["review"].set_index("item")["value"]
w_c = m["w"]
mid = pd.Series(sched, index=Q)
pairq = lambda x: pd.Series([(float(x[DEC[2 * i]]) + float(x[DEC[2 * i + 1]])) / 2 for i in range(5)], index=Q)
# K1 gross LVT payments on one unit: per-household payments of owner-payers (log-normal partial expectations) x households
L2d = L2.reindex(DEC)
pay_hh, recv_own_hh = {}, {}
for i, d in enumerate(DEC):
    s_ = sig[d]
    X = lognorm(s=s_, scale=Lown[d] * np.exp(-s_ ** 2 / 2))
    Xs = lognorm(s=s_, scale=Lown[d] * np.exp(s_ ** 2 / 2))       # E[X; X > t] = E[X] P(X' > t)
    above = Lown[d] * Xs.sf(Lstar[i])
    pay_hh[d] = p_own[d] * (above - Lstar[i] * X.sf(Lstar[i]))
    recv_own_hh[d] = p_own[d] * (Lstar[i] * (1 - X.sf(Lstar[i])) - (Lown[d] - above))
pay_hh, recv_own_hh = pd.Series(pay_hh), pd.Series(recv_own_hh)
bh = float((pay_hh * N)[DEC[:5]].sum() / (pay_hh * N).sum())
check("K1", "bottom half's share of gross LVT payments, one unit (per-household payments x households)", float(rv["bottom_half_share_of_gross_lvt_payments"]), bh, 1e-9,
      "identity", "the earlier 22.6% weighted per-share payments by households")
recv_hh = (1 - p_own) * pd.Series(Lstar, index=DEC) + recv_own_hh
check("K2", "gross payments / gross receipts in D1-D2 (one unit)", float(rv["gross_payments_over_receipts_d1_d2"]),
      float((pay_hh * N)[DEC[:2]].sum() / (recv_hh * N)[DEC[:2]].sum()), 1e-9)
# K3 ghost flips from the stored bars (MPC = 1 ghost against the MPC-adjusted bar), both conventions
for conv, mm_ in [("coherent", m), ("post", mp)]:
    for inst, base in [("lvt", "B2"), ("vat", "")]:
        x = shf[(shf["convention"] == conv) & (shf["instrument"] == inst.upper()) & (shf["base"] == base) & (shf["rate"] == "bridge") &
                (shf["grade"] == "post_mid")].set_index("category").loc[mm_["chart"]]
        check(f"K3_{conv}_{inst}", f"ghost flips, {conv} convention, {inst.upper()} (charted bars)", float(rv[f"ghost_flips_{conv}_{inst}"]),
              float((np.sign(x["dEUR_mpc1"]) != np.sign(x["dEUR"])).sum()), 0, "identity", "coherent 13 / 17, post 12 / 14")
# K4 the s_d band is the unit's own evidence, rounded: within-region plot gap (low), the flow year's N211/(N211+N111) (high)
ev = out["land_evidence"]
g_w = float(ev[ev["evidence"].str.startswith("same, sales-weighted")]["value"].iloc[0])
ub22 = bs("S14", "N211", 2022) / (bs("S14", "N211", 2022) + bs("S14", "N111", 2022))
check("K4a", "s_d band low = the within-region plot gap, rounded (0.150)", float(inp["judgment_s_d_band_low"]), round(g_w, 2), 1e-12, "crosscheck")
check("K4b", "s_d band high = N211/(N211+N111) in 2022, rounded (0.259)", float(inp["judgment_s_d_band_high"]), round(ub22, 2), 1e-12, "crosscheck")
rb_ = out["robustness"]
r26 = rb_[rb_["variant"].str.startswith("dwelling land share s_d = 0.26")].iloc[0]
check("K4c", "at s_d = 0.26 the N211-held residual s_f would be negative, so s_f = 0 (floored)", float(r26["s_f"]), 0.0, 1e-12, "identity",
      f"residual {(bs('S14', 'N211', 2023) - 0.26 * HW) / FFB:.3f}; N211 can be held up to s_d = {bs('S14', 'N211', 2023) / HW:.4f}")
r15 = rb_[rb_["variant"].str.startswith("dwelling land share s_d = 0.15")].iloc[0]
check("K4d", "at s_d = 0.15 the residual s_f holds N211", float(r15["s_f"]), (bs("S14", "N211", 2023) - 0.15 * HW) / FFB, 1e-9)
# K5 the yield-year table: the flow and the non-occupiers' bill response scale with r; the capitalized loss and collateral do not
ld_i = {c: pairq(ld[c]) for c in ["L_ore", "L_ftr", "L_ffb"]}
L_no = ld_i["L_ore"] + ld_i["L_ftr"] + ld_i["L_ffb"]
yy = out["yield_years"]
yv = lambda lab, k, c="central": float(yy[(yy["yield_label"].astype(str) == lab) & (yy["reading"] == k)][c].iloc[0])
coll_mid = float(mac.loc["collateral: credit effect on all crossers' lost borrowing capacity (full capture, immediate)", "central"])
coll_t4 = float(mac.loc["collateral on all crossers' lost equity: includes the T4 overlap (full capture, immediate)", "central"])
for lab, y_ in [("2022", Y22), ("2023", ya["2023"] / 100), ("2024", ya["2024"] / 100), ("2025", ya["2025"] / 100)]:
    tau_y = 0.98 * y_
    net_y = div_full * y_ / Y22 - tau_y * Lq / (12 * sh)                  # the dividend scales with r; bills tau x land per share
    flow_y = 100 * float((w_c * mid * net_y).sum()) / m["budget_bar"]
    add_back = float((w_c * mid * tau_y * L_no / (12 * sh)).sum())
    we = float((w_c * 0.035 * 0.98 * L_no / (12 * sh)).sum())
    chg = 100 * (add_back - we) / m["budget_bar"]
    check(f"K5_{lab}_flow", f"full capture at the {lab} yield: flow impulse (post's method)", yv(lab, "flow"), flow_y, 1e-9)
    check(f"K5_{lab}_nonocc", f"full capture at the {lab} yield: non-occupiers on the wealth reading, net", yv(lab, "nonocc_wealth"), flow_y + coll_mid + chg, 1e-9,
          "identity", "flow + credit effect + (bill response added back - 3.5c x capitalized loss)")
    check(f"K5_{lab}_t4", f"full capture at the {lab} yield: includes the T4 overlap", yv(lab, "t4"), flow_y + coll_t4, 1e-9)
check("K5_2022_main", "yield-year table at 2022 = the headline's non-occupier reading", yv("2022", "nonocc_wealth"), float(hl.loc[("full_m1", "nonocc_wealth"), "central"]), 1e-9)
ydec = float(ym["2022-12"]) / 100
check("K6", "full capture at the December 2022 yield: share of the bridge's dividend", float(rv["full_capture_share_dec2022_yield"]),
      0.98 * ydec * mean_ps / 12 / div_c, 1e-9, "identity", f"yield {100 * ydec:.2f}%")
check("K6b", "funding share range over every yield case (B2, m1 and m2, 2022-25): max", float(rv["full_capture_share_max_yield_cases"]),
      max(0.98 * (ya[str(y)] / 100 + s_) * mean_ps / 12 / div_c for y in (2022, 2023, 2024, 2025) for s_ in (0, 0.015)), 1e-9)
# K7 the US on the same year's yield: GS10 annual means from the vendored FRED copy; the US unit's full-capture outputs rescaled
g10 = pd.read_csv(THREAD.parent / "pinning" / "cache" / "GS10.csv", parse_dates=["observation_date"])
gs = {y: g10[g10["observation_date"].dt.year == y]["GS10"].mean() / 100 for y in (2022, 2024)}
uno = pd.read_csv(OUT / "us_lvt_nonoccupier.csv").set_index(["scenario", "grade"]).loc[("LVT_full_L1_m1", "dn_mid")]
usC = float(uin["ce_consumption_bn"])
we_us = 100 * 0.035 * float(uno["nonocc_capitalized_loss_bn"]) / usC
ab_us = float(uno["wealth_version_mid_pct"] - uno["flow_version_pct"]) + we_us
check("K7a", "US non-occupier decomposition reproduces the US unit's 2c row", float(uno["flow_version_pct"]) + ab_us - 100 * 0.02 * float(uno["nonocc_capitalized_loss_bn"]) / usC,
      float(uno["wealth_version_low_pct"]), 1e-8)
blk22 = [b for b in uc.index.get_level_values(0).unique() if b.startswith("LVT, full capture (phi 0.98), both at their 2022 yields")][0]
blk24 = [b for b in uc.index.get_level_values(0).unique() if b.startswith("LVT, full capture (phi 0.98), both at their 2024 yields")][0]
k22 = gs[2022] / gs[2024]
us_flow_f = float(um.loc["flow impulse, post's method (full, L1)", "central"])
us_cr_f, us_le_f = uu("LVT_full_L1", "dC_lost_capacity_mid_pct"), uu("LVT_full_L1", "dC_lost_equity_mid_pct")
check("K7b", "US at the 2022 yield: non-occupiers on the wealth reading", float(uc.loc[(blk22, "net demand at impact, non-occupiers on the wealth reading (3.5c)"), "US"]),
      us_flow_f * k22 + us_cr_f + ab_us * k22 - we_us, 1e-9, "identity", f"GS10 2022 {100 * gs[2022]:.3f}% / 2024 {100 * gs[2024]:.3f}%")
check("K7c", "US at the 2022 yield: flow + credit effect", float(uc.loc[(blk22, "net demand at impact (flow + credit effect)"), "US"]), us_flow_f * k22 + us_cr_f, 1e-9)
check("K7d", "US at the 2024 yield = the US unit's own non-occupier reading", float(uc.loc[(blk24, "net demand at impact, non-occupiers on the wealth reading (3.5c)"), "US"]),
      us_flow_f + us_cr_f + float(uno["wealth_version_mid_pct"] - uno["flow_version_pct"]), 1e-9)
check("K7e", "FI at the 2024 yield in the comparison = the yield-year table", float(uc.loc[(blk24, "net demand at impact, non-occupiers on the wealth reading (3.5c)"), "FI"]),
      yv("2024", "nonocc_wealth"), 1e-12)
check("K7f", "US at the 2022 yield: includes the T4 overlap", float(uc.loc[(blk22, "net demand at impact, includes the T4 overlap (6c x lost equity)"), "US"]),
      us_flow_f * k22 + us_le_f, 1e-9)
# K8 tenure-aware baskets, re-derived for the LVT (B2, bridge, the post's schedule): owners' changes on transacted lines
UNTX = ["04.2 Imputed rentals (off-chart)", "04.6 Interest on housing loans (off-chart)"]
po = pairq(p_own)
Cq = m["C"]
Co, Cr = Cq.copy(), Cq.copy()
Cr.loc["04.1 Actual rents"] = Cq.loc["04.1 Actual rents"] / (1 - po)
Co.loc["04.1 Actual rents"] = 0.0
for g_ in UNTX:
    Co.loc[g_] = Cq.loc[g_] / po
    Cr.loc[g_] = 0.0
chg_ = m["lines"].loc["maintenance charges of housing companies", Q]
Co.loc["04.4 Water & misc. dwelling services"] = Cq.loc["04.4 Water & misc. dwelling services"] + chg_ * (1 / po - 1)
Cr.loc["04.4 Water & misc. dwelling services"] = Cq.loc["04.4 Water & misc. dwelling services"] - chg_
eo = B.fi_eta_table(dict(m, C=Co, budget=Co.sum()), "F3")[0]
er = B.fi_eta_table(dict(m, C=Cr, budget=Cr.sum()), "F3")[0]
so, sr = Co / Co.sum() * eo, Cr / Cr.sum() * er
so_t = so * (so.sum() / (so.sum() - so.loc[UNTX].sum()))
so_t.loc[UNTX] = 0.0
psum = pd.Series([float(p_own[DEC[2 * i]] + p_own[DEC[2 * i + 1]]) for i in range(5)], index=Q)
own_net = pd.Series([float((recv_own_hh - pay_hh)[[DEC[2 * i], DEC[2 * i + 1]]].sum()) for i in range(5)], index=Q) * tau_b / 12
dco = mid * own_net / (psum * sh)
dcr = mid * div_c
ten_c = ten[(ten["convention"] == "coherent") & (ten["instrument"] == "LVT") & (ten["base"] == "B2") & (ten["grade"] == "post_mid")].set_index("category")
for lab, so_ in [("transacted", so_t), ("as_allocated", so)]:
    mine = (so_.mul(w_c * po * dco, axis=1)).sum(axis=1) + (sr.mul(w_c * (1 - po) * dcr, axis=1)).sum(axis=1)
    col_ = "dEUR" if lab == "transacted" else "dEUR_as_allocated"
    check(f"K8_{lab}", f"tenure-aware LVT bars ({lab} owner allocation), every line (max abs diff, EUR)", float((ten_c[col_].reindex(mine.index) - mine).abs().max()), 0.0, 1e-9)
check("K8_total", "re-spreading keeps the total change (all 47 lines)", float(ten_c["dEUR"].sum()), float(ten_c["dEUR_as_allocated"].sum()), 1e-9)
check("K8_untx", "nothing is booked on imputed rent and loan interest under the transacted allocation (LVT and VAT)",
      float(ten[ten["category"].isin(UNTX)]["dEUR"].abs().max()), 0.0, 1e-12)
own_ms = (Co.loc[UNTX] * eo.loc[UNTX]).sum() / Co.sum()
check("K8_ms", "owners' marginal euro on imputed rent and interest: highest quintile share (18-25%)", float(rv["owner_marginal_share_untransacted_max"]),
      float(own_ms.max()), 1e-9, "identity", f"lowest {own_ms.min():.3f}")
# K9 the liquidity grade at owners' hand-to-mouth shares (151u deciles x 151z tenure mix), for the VAT's payers
tt_ = pd.read_csv(TIDY / "fi_wealth_2023_tenure.csv")
tq = lambda c, k: tt_[(tt_["component"] == c) & (tt_["measure"] == k)].set_index("tenure")["value"].astype(float)
dq = {k: tq("deposits", k) for k in ("p25", "median", "p75")}
s_t = (np.log(dq["p75"]) - np.log(dq["p25"])) / (2 * norm.ppf(0.75))
h_t = (1 - tq("deposits", "participation_rate_pct") / 100) + tq("deposits", "participation_rate_pct") / 100 * \
    pd.Series(lognorm(s=s_t.values, scale=dq["median"].values).cdf((tq("disposable_income", "median") / 24).values), index=s_t.index)
n_mo = wv("housing_loans", "households_holding").reindex(DEC)
n_ow = wv("main_residence", "households_holding").reindex(DEC)
mix = ((n_ow - n_mo) * h_t["outright_owner"] + n_mo * h_t["owner_with_mortgage"]) / n_ow
h_own = (pd.Series(h, index=DEC) * mix / h_t["all"]).clip(upper=1.0)
xv = accv["vatable"].reindex(Q)
cv = float(accv["Cbar_v"].iloc[0])
mu_v = np.log(xv) - 0.45 ** 2 / 2
Pv = norm.sf((np.log(cv) - mu_v) / 0.45)
ab_v = xv * norm.sf((np.log(cv) - mu_v - 0.45 ** 2) / 0.45)
pay_v, recv_v = B.TAU * (ab_v - cv * Pv), B.TAU * (cv * (1 - Pv) - (xv - ab_v))
hq = pairq(h_own)
dC_v = mid * recv_v - (hq + (1 - hq) * mid) * pay_v
check("K9", "VAT flow, payers graded by liquidity at owners' hand-to-mouth shares (% of consumption)", float(rv["vat_flow_liq_grade_owner_htm_shares"]),
      100 * float((w_c * dC_v).sum()) / m["budget_bar"], 1e-9, "identity", "0.339 at all households' shares: the LVT/VAT ratio 1.95 is an upper bound")
# K10 the loop with land as the residual claimant on a rent rise (ls = 1), and the VAT's leak at ls = 1
l1 = lp[(lp["instrument"] == "LVT_B2") & (lp["rate"] == "full_m1") & (lp["ls_case"] == "one") & (lp["landlord_case"] == "mid")].iloc[0]
check("K10a", "loop at ls = 1: multiplier 1 / (1 - phi h q)", float(rv["loop_ls1_multiplier"]), 1 / (1 - 0.98 * 0.55 * float(l1["q"])), 1e-12)
check("K10b", "loop at ls = 1: extra dividend = phi h R0 x multiplier, % of the dividend", float(rv["loop_ls1_extra_dividend_pct"]),
      100 * 0.98 * 0.55 * float(l1["rent_bar_round0"]) / (1 - 0.98 * 0.55 * float(l1["q"])) / div_full, 2e-4, "identity", "iteration against the closed form")
v1 = lp[(lp["instrument"] == "VAT") & (lp["ls_case"] == "one") & (lp["landlord_case"] == "mid")].iloc[0]
check("K10c", "VAT's leak to landlords at ls = 1, EUR m a year (rent bar x shares x 12)", float(rv["vat_leak_to_landlords_ls1_meur"]),
      float(v1["rent_bar_round0"]) * float((hh * sh).sum()) * 12 / 1e6, 1e-6)
# K11 renters' own land, the crosser shapes, the US-FI collateral contrast, rent's share of the flow
ren = (s_d * (tq("other_residential_property", "mean")["renter_or_other"] + tq("free_time_residences", "mean")["renter_or_other"]) +
       s_f * tq("forest_farmland_business", "mean")["renter_or_other"]) * tq("disposable_income", "households_holding")["renter_or_other"] / 1e6
check("K11a", "renters' own land / N211 2023 (assigned to owners by the owner model)", float(rv["renters_share_of_household_land"]), ren / bs("S14", "N211", 2023), 1e-9)
fdec = 0.98 * s_d
n_ln = 0.0
for i, dd in enumerate(DEC):
    D_ = lognorm(s=0.6, scale=1.1 * A[dd])
    n_ln += n_m[dd] * (D_.cdf(0.8) - D_.cdf(0.8 * (1 - fdec)))
check("K11b", "crossers at full capture, log-normal LTVs (sigma 0.6)", float(rv["crossers_80_full_lognormal_sigma_mid"]), n_ln, 1e-3)
check("K11c", "crossers at full capture, US-shape (H5's recomputation)", float(rv["crossers_80_full_us_shape"]), n_cross, 1.0)
h_mort = (pd.Series(h, index=DEC) * h_t["owner_with_mortgage"] / h_t["all"]).clip(upper=1.0)
lc_dec = {}
for i, dd in enumerate(DEC):                                   # H's US-shape population again, lost capacity by decile
    g = s[s["d"] == i + 1]
    aus = float((g["MRTHEL"] * g["WGT"]).sum() / (g["HOUSES"] * g["WGT"]).sum())
    V0 = g["HOUSES"].values * Vbar[dd] / float(np.average(g["HOUSES"], weights=g["WGT"].values))
    M_ = g["MRTHEL"].values / g["HOUSES"].values * A[dd] / aus * V0
    cr_ = (M_ <= 0.8 * V0) & (M_ > 0.8 * V0 * (1 - f))
    lc_dec[dd] = float((g["WGT"].values * n_m[dd] / g["WGT"].sum() * cr_ * (np.maximum(0, 0.8 * V0 - M_) - np.maximum(0, 0.8 * V0 * (1 - f) - M_))).sum())
lc_dec = pd.Series(lc_dec)
check("K11h", "hand-to-mouth crossers' share of the lost borrowing capacity (full capture)", float(rv["htm_share_of_crossers_lost_capacity"]),
      float((lc_dec * h_mort).sum() / lc_dec.sum()), 1e-9, "identity", "the rest belongs to owners with more than half a month's income in deposits")
ucol_f = ucol[(ucol["scenario"] == "LVT_full_L1") & (ucol["design"] == "immediate") & (ucol["threshold"] == 0.8) & (ucol["measure"] == "m1_z1hh_x_gs10")].iloc[0]
check("K11d", "US share of mortgaged owners crossing 80% at full capture (us_lvt_collateral.csv)", float(rv["us_share_of_mortgaged_crossing_80_full"]),
      float(ucol_f["share_of_mortgaged"]), 1e-12)
check("K11e", "FI share of mortgaged owners crossing 80% at full capture", float(rv["fi_share_of_mortgaged_crossing_80_full"]), n_cross / float(n_m.sum()), 1e-6)
check("K11f", "household land per unit of consumption, US / FI", float(rv["us_over_fi_land_per_consumption"]),
      (float(uin["L_hh"]) / usC) / (bs("S14", "N211", 2022) / C), 1e-9)
for inst, base in [("lvt", "B2"), ("vat", "")]:
    rent_ = float(shf[(shf["convention"] == "coherent") & (shf["instrument"] == inst.upper()) & (shf["base"] == base) & (shf["rate"] == "bridge") &
                      (shf["grade"] == "post_mid") & (shf["category"] == "04.1 Actual rents")]["dEUR"].iloc[0])
    fl_ = float(imp[(imp["convention"] == "coherent") & (imp["instrument"] == inst.upper()) & (imp["base"] == base) & (imp["rate"] == "bridge") &
                    (imp["grade"] == "post_mid") & (imp["defer"] == "none")]["flow_pct_consumption"].iloc[0]) / 100 * m["budget_bar"]
    check(f"K11g_{inst}", f"rent's share of the flow impulse ({inst.upper()}, same revenue)", float(rv[f"rent_share_of_flow_{inst}"]), rent_ / fl_, 1e-9)
# K12 post against coherent in the rates table
dphi = dsh = 0.0
for _, r_ in ph[(ph["convention"] == "coherent") & (ph["base"] != "B3")].iterrows():
    p_ = ph[(ph["convention"] == "post") & (ph["base"] == r_["base"]) & (ph["measure"] == r_["measure"]) & (ph["yield_year"] == r_["yield_year"]) &
            (ph["label"] == r_["label"])]
    if len(p_):
        dphi = max(dphi, abs(float(p_["phi_bridge"].iloc[0]) - r_["phi_bridge"]))
        dsh = max(dsh, 100 * abs(float(p_["share_of_vat_dividend"].iloc[0]) - r_["share_of_vat_dividend"]))
check("K12", "post vs coherent rates table: phi within 0.02 and share within 0.4 points", float(dphi < 0.02 and dsh < 0.4), 1.0, 0, "identity",
      f"phi {dphi:.4f}, share {dsh:.3f} points")
info("K13", "Finnish non-occupier reading at the 2023 / 2024 / 2025 yields (beside the US unit's -0.48 at its 2024 yield)", yv("2024", "nonocc_wealth"),
     f"2023 {yv('2023', 'nonocc_wealth'):+.3f}, 2025 {yv('2025', 'nonocc_wealth'):+.3f}; 2022 {yv('2022', 'nonocc_wealth'):+.3f}")


# %% summary
R = pd.DataFrame(rows)
R.to_csv(OUT / "check_lvt_fi.csv", index=False, float_format="%.10g")
print(R["result"].value_counts().to_string())
bad = R[R["result"] == "FAIL"]
if len(bad):
    print("\nFAILED:\n" + bad[["check_id", "description", "value", "reference", "diff"]].to_string(index=False))
print(f"\n{(R['result'] == 'PASS').sum()} PASS / {(R['result'] == 'FAIL').sum()} FAIL / {(R['result'] == 'INFO').sum()} INFO; wrote out/check_lvt_fi.csv")
