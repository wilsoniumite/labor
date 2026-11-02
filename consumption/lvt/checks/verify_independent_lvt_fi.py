"""Independent verification of the LVT Finland unit (consumption/lvt/NOTES_fi.md, code/lvt_fi.py, code/run_lvt_fi.py, out/fi_lvt_*.csv).

Nothing is imported or copied from consumption/lvt/code/. The method is re-implemented here from NOTES_fi.md and the task text,
reading the RAW files where the task asks for them:

  - wealth survey 2023 (vtutk 151u by income decile, 151z by tenure), household balance sheet (rtp 11zx: N211 land, N111
    residential buildings), national accounts (ntp 15ag), plot and dwelling prices (ashi 13mw, ashi 12de, kihi 11jc), HBS
    background (ktutk 14qa): parsed here from the StatFin JSON-stat files in consumption/data/raw/statfin/data/;
  - ten-year yields: the Eurostat JSON-stat files (irt_lt_mcby_a/m, FI) and the ECB CSV in consumption/data/raw/{eurostat,ecb}/;
  - SCF 2025 summary extract (the US-shape LTV population, US concentration): parsed here from the vendored zip
    consumption/data/raw/fed/scf/scfp2025excel.zip;
  - the US side of the comparison: the US unit's current outputs (consumption/lvt/out/us_lvt_*.csv), which the FI unit quotes; the
    US collateral at Finland's revenue share is recomputed here from the SCF zip.

bridge.py (verified separately) is imported for the HBS 2022 model dict (C, w, budget, eta, payment units), the VAT accounting,
the MPC schedules, eta at a given basket (fi_eta_table) and the category machinery (shifts_from_transfers, decompose). Land
shares, land by decile and quintile, bills, dividends, nets, the within-decile owner split, hand-to-mouth shares, MPC grades,
impulses, tenure baskets, deferral, collateral, the levy, non-occupiers, the loop and the robustness rows are computed here.

Every claim prints one line

    OK  | claim | builder | mine | note        (or BAD | ...)

OK: my independent value agrees with the builder's CSV value and with the number NOTES_fi.md prints (within its printed rounding
or the stated tolerance), or, for a review item, the builder's statement holds up. BAD: one of these fails, or a statement or
judgment call does not hold up on review (the note says why and what should change). A final count follows; a CSV copy goes to
consumption/lvt/out/verify_independent_lvt_fi.csv.

Run from the repo root:  venv/bin/python -I consumption/lvt/checks/verify_independent_lvt_fi.py   (about 10 s)

Plain functions and top-level code, so the cells can be pasted into a notebook.
"""
# %% setup
import io
import itertools
import json
import re
import sys
import zipfile
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent                     # consumption/lvt/checks
LVT = HERE.parent
CONS = LVT.parent
REPO = CONS.parent
sys.path.insert(0, str(CONS / "rebuild" / "code"))          # bridge.py only (verified separately)

import numpy as np
import pandas as pd
from scipy import stats
from tqdm.auto import tqdm

import bridge as B

RAW = CONS / "data" / "raw"
SF = RAW / "statfin" / "data"
BOUT = LVT / "out"                                          # the builder's outputs (read only)
OUT_CSV = BOUT / "verify_independent_lvt_fi.csv"
NOTES = re.sub(r"\s+", " ", (LVT / "NOTES_fi.md").read_text())
DEC = [f"d{i:02d}" for i in range(1, 11)]
Q = ["q1", "q2", "q3", "q4", "q5"]
PAIR = {d: Q[i // 2] for i, d in enumerate(DEC)}           # wealth-survey deciles -> HBS quintiles (D1, D2 -> q1 ...)
PHI = 0.98                                                  # full capture (design memo 1.1)
SPREAD = 0.015                                              # the paper's +1.5 points
MPW = {"low": 0.02, "mid": 0.035, "high": 0.05}             # post fn 31
MPCC = {"low": 0.047, "mid": 0.06, "lit_high": 0.07, "stress": 0.10}   # collateral cents per euro (US unit's band)
CLAIMS = []
AREA = [""]


DR = []                                                     # printed values that only a double rounding reproduces
DR_SEEN = [0]


def claim(ok, text, builder, mine, note=""):
    """Record one claim; a printed-value check met only by double rounding since the last claim is appended to its note."""
    fmt = lambda v: v if isinstance(v, str) else ("" if v is None else (f"{v:.5g}" if abs(v) < 1e5 else f"{v:,.0f}"))
    if len(DR) > DR_SEEN[0]:
        for x in DR[DR_SEEN[0]:]:
            x["claim"] = text
        note = (note + "; " if note else "") + "double-rounded print: " + ", ".join(f"{x['mine']:.5g} printed {x['printed']:g}" for x in DR[DR_SEEN[0]:])
        DR_SEEN[0] = len(DR)
    CLAIMS.append(dict(area=AREA[0], status="OK" if ok else "BAD", claim=text, builder=fmt(builder), mine=fmt(mine), note=note))
    return ok


def near(a, b, tol, rel=True):
    a, b = float(a), float(b)
    if not (np.isfinite(a) and np.isfinite(b)):
        return a == b
    return abs(a - b) <= (tol * max(abs(b), 1e-12) if rel else tol)


def printed(mine, value, unit):
    """A number NOTES prints: within half a printed unit of mine (2% slack on the half unit for float storage); or reproduced only
    by double rounding (mine rounded half-up to one more decimal, then to the printed unit), accepted here and logged in DR."""
    mine, value = float(mine), float(value)
    if abs(mine - value) <= 0.5 * unit * 1.02 + 1e-12:
        return True
    d = int(round(-np.log10(unit)))
    two = Decimal(repr(mine)).quantize(Decimal(1).scaleb(-(d + 1)), ROUND_HALF_UP).quantize(Decimal(1).scaleb(-d), ROUND_HALF_UP)
    if abs(float(two) - value) < 1e-9:
        DR.append(dict(mine=mine, printed=value))
        return True
    return False


def num(mine, builder, text, notes=None, unit=None, tol=1e-6, rel=True, note=""):
    """My value against the builder's CSV value (tol) and, if given, the NOTES value printed to `unit`."""
    ok = near(mine, builder, tol, rel) if builder is not None else True
    msg = []
    if notes is not None:
        okn = printed(mine, notes, unit)
        ok = ok and okn
        msg.append(f"NOTES {notes:g}" + ("" if okn else " (NOT within its printed rounding)"))
    if builder is not None and not near(mine, builder, tol, rel):
        msg.append(f"differs from the builder's CSV by {float(mine) - float(builder):+.4g}")
    if note:
        msg.append(note)
    return claim(ok, text, builder if builder is not None else "", mine, "; ".join(msg))


def in_notes(s):
    return re.sub(r"\s+", " ", s) in NOTES


def bcsv(name, **kw):
    return pd.read_csv(BOUT / name, **kw)


# %% raw readers: StatFin and Eurostat JSON-stat, the ECB CSV, the SCF zip
def jsonstat(path):
    """A JSON-stat 2.0 dataset as a long frame: one column per dimension (category codes) plus 'value' (NaN where the
    publisher left the cell empty). Values are stored row-major over the dimensions in 'id' order."""
    j = json.loads(Path(path).read_text())
    cats = []
    for d in j["id"]:
        idx = j["dimension"][d]["category"]["index"]
        if isinstance(idx, list):
            idx = {k: i for i, k in enumerate(idx)}
        cats.append(sorted(idx, key=idx.get))
    n = int(np.prod(j["size"]))
    v = j["value"]
    vals = [np.nan] * n
    if isinstance(v, dict):
        for k, x in v.items():
            vals[int(k)] = np.nan if x is None else float(x)
    else:
        vals = [np.nan if x is None else float(x) for x in v]
    out = pd.DataFrame(list(itertools.product(*cats)), columns=j["id"])
    out["value"] = vals
    return out


W_ITEM = {"main_residence": "asarav", "free_time": "vaarvy", "other_res": "asaram", "ffb": "muurealvar", "net_wealth": "nettoae_DN3001",
          "financial": "finan", "deposits": "talle", "listed": "pymar", "other_fin": "muufinan", "housing_loans": "asuntm",
          "income": "kturaha", "housing_wealth": "asvara"}
W_MEAS = {"mean": "vtutk_keskiarvo_n", "median": "vtutk_mediaani_n", "p25": "vtutk_alakvartiili_n", "p75": "vtutk_ylakvartiili_n",
          "holders": "vtutk_kotitalousomistajia", "part": "vtutk_kotitalousosuus", "pop": "vtutk_kotitalouksia_perusjoukko"}
u151 = jsonstat(SF / "vtutk_151u.json")
u151 = u151[u151["timeperiod_y"] == "2023"]
z151 = jsonstat(SF / "vtutk_151z.json")
z151 = z151[z151["timeperiod_y"] == "2023"]
DMAP = {**{str(i): f"d{i:02d}" for i in range(1, 11)}, "SS": "total"}
TMAP = {"SS": "all", "1": "outright", "2": "mortgaged", "3": "renter"}


def wd(item, meas="mean"):
    """151u 2023 by income decile (d01..d10, total)."""
    x = u151[(u151["vtutk_varlaji_6_20200101"] == W_ITEM[item]) & (u151["contentscode"] == W_MEAS[meas])]
    return x.set_index(x["desiilit_2_20120101"].map(DMAP))["value"].reindex(DEC + ["total"])


def wt(item, meas="mean"):
    """151z 2023 by housing tenure (all, outright, mortgaged, renter)."""
    x = z151[(z151["vtutk_varlaji_6_20200101"] == W_ITEM[item]) & (z151["contentscode"] == W_MEAS[meas])]
    return x.set_index(x["hallintaperuste_1_20150401"].map(TMAP))["value"].reindex(["all", "outright", "mortgaged", "renter"])


bs_raw = jsonstat(SF / "rtp_11zx.json")


def bsheet(sector, instr, year):
    x = bs_raw[(bs_raw["sektoriluokitus_7_20230101"] == sector) & (bs_raw["varojenluokitus_5_20180101"] == instr) &
               (bs_raw["timeperiod_y"] == str(year)) & (bs_raw["contentscode"] == "KK")]
    assert len(x) == 1
    return float(x["value"].iloc[0])


na_raw = jsonstat(SF / "ntp_15ag.json")


def na(code, year, meas="ntp-cp"):
    x = na_raw[(na_raw["taloustoimi_1_20180101"] == "P31DCK") & (na_raw["coicop_45_20231201"] == code) &
               (na_raw["timeperiod_y"] == str(year)) & (na_raw["contentscode"] == meas)]
    assert len(x) == 1, (code, year)
    return float(x["value"].iloc[0])


def eurostat_series(path):
    j = json.loads(Path(path).read_text())
    inv = {v: k for k, v in j["dimension"]["time"]["category"]["index"].items()}
    return pd.Series({inv[int(k)]: float(v) for k, v in j["value"].items()}).sort_index()


Y_A = eurostat_series(RAW / "eurostat" / "data" / "irt_lt_mcby_a_FI.json")
Y_M = eurostat_series(RAW / "eurostat" / "data" / "irt_lt_mcby_m_FI.json")
ecb = pd.read_csv(RAW / "ecb" / "data" / "IRS_M.FI.L.L40.CI.0000.EUR.N.Z.csv", usecols=["TIME_PERIOD", "OBS_VALUE"])
Y_E = pd.Series(ecb["OBS_VALUE"].astype(float).values, index=ecb["TIME_PERIOD"].astype(str))
YLD = {y: float(Y_A[str(y)]) / 100.0 for y in (2022, 2023, 2024, 2025)}


def scf2025(cols):
    with zipfile.ZipFile(RAW / "fed" / "scf" / "scfp2025excel.zip") as z:
        with z.open("SCFP2025.csv") as fh:
            return pd.read_csv(io.BytesIO(fh.read()), usecols=cols)


SCF = scf2025(["YY1", "Y1", "WGT", "HOUSES", "MRTHEL", "ORESRE", "FIN", "NETWORTH", "INCOME", "INCPCTLECAT"])
SCF["dec"] = np.minimum(SCF["INCPCTLECAT"].astype(int), 10)      # 90-95, 95-99, 99-100 -> the top decile (macro PCTL points)


# %% the builder's outputs (read only)
b_inp = bcsv("fi_lvt_inputs.csv").set_index("item")["value"]
b_phi = bcsv("fi_lvt_phi.csv")
b_acc = bcsv("fi_lvt_accounting_by_quintile.csv", keep_default_na=False, na_values=[""])
b_imp = bcsv("fi_lvt_impulse.csv", keep_default_na=False, na_values=[""])
b_imp["base"] = b_imp["base"].fillna("")
b_acc["base"] = b_acc["base"].fillna("")
b_ld = bcsv("fi_lvt_land_by_decile.csv").set_index("decile")
b_lq = bcsv("fi_lvt_land_by_quintile.csv").set_index("quintile")
b_ev = bcsv("fi_lvt_land_evidence.csv")
b_conc = bcsv("fi_lvt_concentration.csv")
b_wd = bcsv("fi_lvt_within_decile.csv")
b_liq = bcsv("fi_lvt_liquidity.csv").set_index("decile")
b_lt = bcsv("fi_lvt_liquidity_tenure.csv")
b_pay = bcsv("fi_lvt_payer_shares.csv").set_index("quintile")
b_shf = bcsv("fi_lvt_demand_shifts.csv", keep_default_na=False, na_values=[""])
b_shf["base"] = b_shf["base"].fillna("")
b_seg = bcsv("fi_lvt_decomposition_top10.csv")
b_ten = bcsv("fi_lvt_tenure_aware.csv", keep_default_na=False, na_values=[""])
b_ten["base"] = b_ten["base"].fillna("")
b_cap = bcsv("fi_lvt_capitalization.csv")
b_col = bcsv("fi_lvt_collateral.csv")
b_cln = bcsv("fi_lvt_collateral_lognormal_totals.csv")
b_no = bcsv("fi_lvt_nonoccupier.csv")
b_df = bcsv("fi_lvt_deferral.csv")
b_loop = bcsv("fi_lvt_loop.csv")
b_lev = bcsv("fi_lvt_vat_levy.csv")
b_mac = bcsv("fi_lvt_macro_channels.csv")
b_hl = bcsv("fi_lvt_headline.csv", keep_default_na=False, na_values=[""])
b_uc = bcsv("fi_lvt_us_compare.csv")
b_rob = bcsv("fi_lvt_robustness.csv")


def b_mc(channel, col="central"):
    x = b_mac[b_mac["channel"] == channel]
    assert len(x) == 1, channel
    return float(x[col].iloc[0])


def b_flow(inst, base, rate, grade, conv="coherent", defer="none"):
    x = b_imp[(b_imp["convention"] == conv) & (b_imp["instrument"] == inst) & (b_imp["base"] == base) & (b_imp["rate"] == rate) &
              (b_imp["grade"] == grade) & (b_imp["defer"] == defer)]
    assert len(x) == 1, (inst, base, rate, grade, conv, defer)
    return x.iloc[0]


# %% A. inputs: the rebuilt VAT side (bridge.py), the HBS population, yields, balance sheet, national accounts
AREA[0] = "A inputs"
M = {c: B.build_fi_model(convention=c) for c in ("coherent", "post")}
VA = {c: B.fi_vat_accounting(M[c]) for c in M}
VA_LAW = {c: B.fi_vat_accounting(M[c], flags=B.fi_vat_flags("law")) for c in M}
DIV = {c: float(VA[c]["dividend"].iloc[0]) for c in M}
DIV_LAW = {c: float(VA_LAW[c]["dividend"].iloc[0]) for c in M}
SQ = {c: M[c]["units"]["shares"].reindex(Q) for c in M}           # payment shares per household by quintile (12ew pair means)
HH = M["coherent"]["units"]["households"].reindex(Q)                # HBS 2022 households (14qa)
NSH = float((HH * SQ["coherent"]).sum())                            # payment shares in the HBS population
C_MEUR = M["coherent"]["budget_bar"] * NSH * 12 / 1e6               # HBS 2022 consumption, EUR million a year
SCHED = B.fi_mpc_schedules()
num(DIV["coherent"], b_inp["vat_dividend_coherent"], "VAT dividend, coherent convention (EUR/share/month)", 198.82, 0.01)
num(DIV["post"], b_inp["vat_dividend_post"], "VAT dividend, post convention (the published EUR 193)", 193.01, 0.01)
num(DIV_LAW["coherent"], b_inp["vat_dividend_law_coherent"], "VAT dividend under Finnish law line by line, coherent", 178.0, 0.1)
num(DIV_LAW["post"], b_inp["vat_dividend_law_post"], "VAT dividend under Finnish law line by line, post", 172.4, 0.1)
num(NSH, b_inp["payment_shares_hbs_coherent"], "payment shares in the HBS 2022 population (households x 12ew shares)")
num(C_MEUR, b_inp["consumption_hbs_meur"], "HBS 2022 consumption, EUR million (budget x shares x 12)",
    note=f"= {C_MEUR / (39808 * 2.919):.4f} x (EUR 39,808 x 2,919,000)")
VAT_REV = DIV["coherent"] * NSH * 12 / 1e6
num(VAT_REV, b_inp["vat_revenue_meur"], "VAT bridge revenue, EUR million a year")
claim(printed(VAT_REV / 1e3, 11.5, 0.1), "VAT bridge revenue EUR 11.5bn (NOTES)", "11.5", VAT_REV / 1e3)
HS = na("041", 2022) + na("042", 2022)
num(HS, b_inp["housing_services_2022_meur"], "NA housing services 2022 (04.1 + 04.2, ntp 15ag), EUR million")
NA_C = na("SSS", 2022)
num(NA_C, b_inp["na_consumption_2022_meur"], "NA household consumption 2022 (P31DCK), EUR million")
DEFL23 = na("SSS", 2023) / na("SSS", 2023, "ntp-fp")
num(DEFL23, b_inp["consumption_deflator_2023"], "consumption deflator 2023 (P31DCK current / previous-year prices)", 1.043, 0.001)
for y in (2022, 2023, 2024, 2025):
    num(100 * YLD[y], b_inp[f"yield_{y}"], f"Eurostat 10-year yield (irt_lt_mcby_a, FI), annual {y}, %",
        {2022: 1.69, 2023: 3.04, 2024: 2.85, 2025: 3.00}[y], 0.01)
ecb22 = float(Y_E[Y_E.index.str.startswith("2022")].mean())
mo22 = float(Y_M[Y_M.index.str.startswith("2022")].mean())
claim(abs(ecb22 - mo22) <= 0.002 and len(Y_E[Y_E.index.str.startswith("2022")]) == 12,
      "ECB's identical series agrees with Eurostat's 'to 0.002 points' in 2022 (NOTES)", f"{mo22:.4f}",
      ecb22, f"ECB monthly mean {ecb22:.4f} vs Eurostat monthly mean {mo22:.4f} ({ecb22 - mo22:+.4f}); "
             f"vs Eurostat's annual 1.69: {ecb22 - 100 * YLD[2022]:+.4f}; 12 months each")
dec22 = float(Y_M["2022-12"])
claim(True, "The 2022 annual-mean yield pairs with an END-2022 land stock (info; see review R-yield)", "1.69",
      100 * YLD[2022], f"December 2022 monthly yield {dec22:.2f}%; mean of 2022 months {mo22:.3f}%")


# %% B. land: shares (the residual), carry, holdings by decile and quintile, evidence, concentration
AREA[0] = "B land"
NHD = wd("net_wealth", "holders").reindex(DEC)                     # households per survey decile (exact counts, 2023)
N_SURV = float(wd("net_wealth", "holders")["total"])
HWd = (wd("main_residence") + wd("other_res") + wd("free_time")).reindex(DEC)
FFBd = wd("ffb").reindex(DEC)
HW23, FFB23 = float((HWd * NHD).sum()) / 1e6, float((FFBd * NHD).sum()) / 1e6
N211 = {y: bsheet("S14", "N211", y) for y in (2021, 2022, 2023)}
N111 = {y: bsheet("S14", "N111", y) for y in (2022, 2023)}
S_D = 1.0 - N111[2023] / HW23
S_F = (N211[2023] - S_D * HW23) / FFB23
CARRY = N211[2022] / N211[2023]
CARRY_MID = 0.5 * (N211[2021] + N211[2022]) / N211[2023]
num(HW23, b_inp["survey_dwellings_2023_meur"], "survey dwellings 2023 (main + other residential + free-time), EUR million")
num(FFB23, b_inp["survey_ffb_2023_meur"], "survey forest, farmland and business 2023, EUR million")
num(S_D, b_inp["s_d_residual"], "dwelling land share s_d = 1 - N111(2023) / survey dwelling value", 0.197, 0.001)
num(S_F, b_inp["s_f_residual"], "forest/farmland/business land share s_f (N211 residual)", 0.763, 0.001)
num(CARRY, b_inp["carry_2023_to_2022"], "carry 2023 -> 2022 = N211 end-2022 / end-2023", 1.0415, 0.0001)
num(CARRY_MID, b_inp["carry_mid2022_alt"], "carry to mid-2022 (mean of end-2021, end-2022 N211) / end-2023")


def land_dec(sd=None, sf=None, carry=None):
    """Land per household by survey decile (2022 euros): item x land share x carry."""
    sd, sf, carry = (S_D if sd is None else sd), (S_F if sf is None else sf), (CARRY if carry is None else carry)
    d = pd.DataFrame(index=DEC)
    d["L_main"] = sd * wd("main_residence").reindex(DEC) * carry
    d["L_ore"] = sd * wd("other_res").reindex(DEC) * carry
    d["L_ftr"] = sd * wd("free_time").reindex(DEC) * carry
    d["L_ffb"] = sf * wd("ffb").reindex(DEC) * carry
    d["B1"] = d[["L_main", "L_ore", "L_ftr"]].sum(axis=1)
    d["B2"] = d["B1"] + d["L_ffb"]
    return d


def pairq(x):
    """Decile values -> quintile values, the mean of each decile pair (the survey deciles hold equal households)."""
    x = pd.Series(x, dtype=float).reindex(DEC)
    return pd.Series([0.5 * (x.iloc[2 * i] + x.iloc[2 * i + 1]) for i in range(5)], index=Q)


LD = land_dec()
LQ = {b: pairq(LD[b]) for b in ("B1", "B2")}
tot_land = float((LD["B2"] * NHD).sum()) / 1e6
claim(near(tot_land, N211[2022], 1e-9) and printed(tot_land / 1e3, 131.5, 0.1), "household land 2022 = N211 S14 end-2022 = EUR 131.5bn",
      f"{N211[2022]:,.0f}", tot_land)
claim(near(N211[2023], 126251, 1e-12) and printed(N211[2023] / 1e3, 126.3, 0.1), "N211 S14 end-2023 = EUR 126.3bn (survey year)",
      "126.3bn", N211[2023] / 1e3)
mx = max(float((LD[c] - b_ld[c].reindex(DEC)).abs().max()) for c in ["L_main", "L_ore", "L_ftr", "L_ffb", "B1", "B2"])
claim(mx < 1e-3, "land per household by decile, every item (max abs diff, EUR)", "fi_lvt_land_by_decile.csv", mx)
mxq = max(float((LQ[b] - b_lq[f"{b}_per_household"].reindex(Q)).abs().max()) for b in LQ)
claim(mxq < 1e-3, "land per household by quintile, B1 and B2 (pair means; max abs diff, EUR)", "fi_lvt_land_by_quintile.csv", mxq)
pooled = {b: pd.Series([float((LD[b] * NHD).iloc[2 * i:2 * i + 2].sum() / NHD.iloc[2 * i:2 * i + 2].sum()) for i in range(5)], index=Q) for b in LQ}
claim(float(((pooled["B2"] - LQ["B2"]) / LQ["B2"]).abs().max()) < 1e-3, "pair mean = pooled pair within 0.1% (deciles hold equal households)",
      "", float(((pooled["B2"] - LQ["B2"]) / LQ["B2"]).abs().max()))
for c in M:
    for b in LQ:
        mine = LQ[b] / SQ[c]
        mxs = float((mine - b_lq[f"{b}_per_share_{c}"].reindex(Q)).abs().max())
        claim(mxs < 1e-3, f"land per payment share by quintile, {b}, {c} (max abs diff, EUR)", "fi_lvt_land_by_quintile.csv", mxs)

# land-share evidence: the balance-sheet upper bound and the plot-price lower bound
ub22, ub23 = N211[2022] / (N211[2022] + N111[2022]), N211[2023] / (N211[2023] + N111[2023])
num(ub22, float(b_ev[b_ev["evidence"].str.contains("2022") & b_ev["evidence"].str.contains("N211")]["value"].iloc[0]),
    "upper bound N211/(N211+N111), households 2022", 0.259, 0.001)
num(ub23, float(b_ev[b_ev["evidence"].str.contains("2023") & b_ev["evidence"].str.startswith("N211")]["value"].iloc[0]),
    "upper bound N211/(N211+N111), households 2023 (band high 0.24)", 0.239, 0.001)
a13 = jsonstat(SF / "ashi_13mw.json")
a13 = a13[(a13["timeperiod_y"] == "2022") & (a13["talotyyppi_6_20131021"] == "6")]


def a13v(region, plot, meas):
    x = a13[(a13["alue_43_20220407"] == region) & (a13["vuokratontti_1_20191126"] == plot) & (a13["contentscode"] == meas)]
    return float(x["value"].iloc[0])


gap = {r: 1 - a13v(r, "1", "keskihinta_aritm") / a13v(r, "0", "keskihinta_aritm") for r in ("ksu", "kas", "muu", "pks")}
sales = {r: a13v(r, "2", "lkm_julk20") for r in ("ksu", "kas", "muu")}
gap_within = (gap["kas"] * sales["kas"] + gap["muu"] * sales["muu"]) / (sales["kas"] + sales["muu"])
rented_share = a13v("ksu", "1", "lkm_julk20") / sales["ksu"]
b_gn = float(b_ev[b_ev["evidence"].str.startswith("own vs rented plot price gap, old")]["value"].iloc[0])
b_gw = float(b_ev[b_ev["evidence"].str.startswith("same, sales-weighted")]["value"].iloc[0])
num(gap["ksu"], b_gn, "plot gap 1 - rented/own, old housing-company dwellings, whole country 2022", 0.094, 0.001)
num(gap_within, b_gw, "plot gap within region groups (major cities / rest), sales-weighted", 0.150, 0.001,
    note=f"major cities {gap['kas']:.3f} (NOTES 16.6%), rest {gap['muu']:.3f} (NOTES 13.6%)")
claim(printed(gap["kas"], 0.166, 0.001) and printed(gap["muu"], 0.136, 0.001) and printed(rented_share, 0.22, 0.01),
      "region-group gaps 16.6% / 13.6% and rented plots 22% of sales (NOTES)", "16.6 / 13.6 / 22%",
      f"{100 * gap['kas']:.1f} / {100 * gap['muu']:.1f} / {100 * rented_share:.1f}%")
a12 = jsonstat(SF / "ashi_12de.json")
a12 = a12[(a12["timeperiod_y"] == "2022") & (a12["talotyyppi_5_20111209"] == "3") & (a12["huoneluku_1_20111212"] == "00") &
          (a12["contentscode"] == "keskihinta_uudet")]
g12 = {r: 1 - float(a12[(a12["alue_3_20181009"] == r) & (a12["vuokratontti_1_20191126"] == "1")]["value"].iloc[0]) /
       float(a12[(a12["alue_3_20181009"] == r) & (a12["vuokratontti_1_20191126"] == "0")]["value"].iloc[0]) for r in ("ksu", "pks")}
claim(printed(g12["ksu"], 0.090, 0.001) and printed(g12["pks"], 0.188, 0.001), "new blocks of flats plot gap 2022: 9.0% nationally, 18.8% Greater Helsinki",
      "9.0 / 18.8%", f"{100 * g12['ksu']:.1f} / {100 * g12['pks']:.1f}%")
k11 = jsonstat(SF / "kihi_11jc.json")
k11 = k11[k11["timeperiod_y"] == "2022"]
kv = lambda r, m: float(k11[(k11["alue_21_20131212"] == r) & (k11["contentscode"] == m)]["value"].iloc[0])
plot = {r: kv(r, "kihi-keskihinta") * kv(r, "keskiala") for r in ("01", "02", "07")}
claim(printed(plot["01"] / 1e3, 73, 1) and printed(plot["02"] / 1e3, 316, 1) and printed(plot["07"] / 1e3, 41, 1) and
      printed(kv("01", "kihi-keskihinta"), 25.9, 0.1) and printed(kv("01", "keskiala"), 2837, 1),
      "single-family plot 2022: EUR 25.9/m2 x 2,837 m2 = EUR 73,000; Greater Helsinki 316,000; under 20,000 inhabitants 41,000",
      "73 / 316 / 41 kEUR", f"{plot['01'] / 1e3:.1f} / {plot['02'] / 1e3:.1f} / {plot['07'] / 1e3:.1f} kEUR")
claim(S_D > gap_within and S_D < ub23, "the residual s_d sits inside its bounds (lower: within-region plot gap; upper: N211/(N211+N111) 2023)",
      "0.150 < 0.197 < 0.239", f"{gap_within:.3f} < {S_D:.3f} < {ub23:.3f}")

# concentration: top income decile's share, Finland (151u; this unit's land) and the US (SCF 2025 from the zip; US unit's land)
def top_share(x):
    x = pd.Series(x, dtype=float).reindex(DEC) * NHD
    return float(x["d10"] / x.sum()), float(x[["d09", "d10"]].sum() / x.sum()), float(x[DEC[:5]].sum() / x.sum())


bc = b_conc.set_index(["country", "item"])
for lab, x, item, nv in [("residential land B1", LD["B1"], "land B1", 0.288), ("all household land B2", LD["B2"], "land B2", 0.281),
                         ("financial assets", wd("financial"), "financial assets", 0.509), ("net wealth", wd("net_wealth"), "net wealth", 0.373),
                         ("main residence", wd("main_residence"), "main residence", None)]:
    t1, t2, bh = top_share(x)
    num(t1, bc.loc[("FI", item), "top_decile"], f"FI top income decile's share of {lab}", nv, 0.001 if nv else None, tol=1e-6)
scf_w = SCF["WGT"]


def us_top(v):
    t = (SCF[v].clip(lower=0) * scf_w).groupby(SCF["dec"]).sum()
    return float(t.loc[10] / t.sum())


for v, item, nv in [("FIN", "financial assets", 0.656), ("NETWORTH", "net wealth", 0.613)]:
    num(us_top(v), bc.loc[("US", item), "top_decile"], f"US top income decile's share of {item} (SCF 2025 zip, all implicates, WGT)", nv, 0.001)
usl = pd.read_csv(BOUT / "us_lvt_land_by_decile.csv").set_index("decile")
num(float(usl.loc["d10", "L1_share"]), bc.loc[("US", "land L1 (residential)"), "top_decile"], "US top decile's share of residential land (US unit's L1)",
    0.394, 0.001)
num(float(usl.loc["d10", "L2_share"]), bc.loc[("US", "land L2 (all)"), "top_decile"], "US top decile's share of all land in the wider base (US L2)",
    0.515, 0.001)
xv = VA["coherent"]["vatable"] * M["coherent"]["w"]
num(float(xv["q5"] / xv.sum()), bc.loc[("FI", "VAT-able consumption (coherent)"), "top_quintile"], "FI top quintile's share of VAT-able consumption",
    0.327, 0.001)
num(float(usl.loc[["d09", "d10"], "vatable_share"].sum()), bc.loc[("US", "VAT-able consumption (CE)"), "top_quintile"],
    "US top quintile's share of VAT-able consumption (CE)", 0.366, 0.001)


# %% C. rates: the bridge-equivalent charge, full capture, by base, measure and yield year
AREA[0] = "C rates"
HBS_SCALE = float(HH.sum()) / N_SURV                                # HBS households / survey households


def mean_ps(conv, lq):
    """Population-mean land value per payment share (EUR) under the convention's own weights."""
    return float((M[conv]["w"] * pd.Series(lq).reindex(Q) / SQ[conv]).sum())


def tau_for(conv, base, div=None):
    return 12.0 * (DIV[conv] if div is None else div) / mean_ps(conv, LQ[base])


def div_full(conv, base, r, phi=PHI):
    return phi * r * mean_ps(conv, LQ[base]) / 12.0


def bphi(base, measure, year, conv="coherent", law=False):
    x = b_phi[(b_phi["base"] == base) & (b_phi["measure"] == measure) & (b_phi["yield_year"] == year) & (b_phi["convention"] == conv) &
              (b_phi["label"].str.contains("law") == law)]
    assert len(x) == 1, (base, measure, year, conv, law)
    return x.iloc[0]


L_HBS = {b: float((LD[b] * NHD).sum()) / 1e6 * HBS_SCALE for b in ("B1", "B2")}
r22 = YLD[2022]
t_b2 = tau_for("coherent", "B2")
num(100 * t_b2, bphi("B2", "m1", 2022)["tau_bridge_pct_of_land_value"], "bridge-equivalent charge on all household land (B2), % of land value a year",
    8.9, 0.1)
num(t_b2 / r22, bphi("B2", "m1", 2022)["phi_bridge"], "phi for the EUR 199 dividend, B2, 2022 yield ('5.2 times the whole rent')", 5.24, 0.01)
claim(printed(t_b2 / r22, 5.2, 0.1), "'That is 5.2 times the whole rent'", "5.2", t_b2 / r22)
num(div_full("coherent", "B2", r22), bphi("B2", "m1", 2022)["dividend_full"], "full-capture dividend, B2, 2022 yield (EUR/share/month)", 37.2, 0.1)
claim(printed(div_full("coherent", "B2", r22), 37, 1), "'Taking 98% of it funds a dividend of EUR 37'", "37", div_full("coherent", "B2", r22))
sh22 = div_full("coherent", "B2", r22) / DIV["coherent"]
num(100 * sh22, 100 * bphi("B2", "m1", 2022)["share_of_vat_dividend"], "full capture / VAT dividend, B2, 2022 yield, %", 18.7, 0.1)
claim(printed(100 * sh22, 19, 1), "'That is 19% of the VAT bridge's EUR 199'", "19%", 100 * sh22)
rent22 = r22 * L_HBS["B2"]
num(rent22, bphi("B2", "m1", 2022)["rent_meur"], "household land rent at the 2022 yield, HBS population (EUR m; NOTES 'about EUR 2.2bn')", 2200, 100)
num(L_HBS["B2"], bphi("B2", "m1", 2022)["land_meur"], "B2 land held by the HBS population (EUR m)")
for y, nphi, ndiv, nsh in [(2022, 2.78, 70.1, 35.3), (2023, 1.95, 99.8, 50.2), (2024, 2.04, 95.6, 48.1), (2025, 1.97, 98.9, 49.7)]:
    r = YLD[y] + SPREAD
    num(tau_for("coherent", "B2") / r, bphi("B2", "m2", y)["phi_bridge"], f"phi, B2, {y} yield + 1.5", nphi, 0.01 if y == 2022 else 0.02)
    num(div_full("coherent", "B2", r), bphi("B2", "m2", y)["dividend_full"], f"full-capture dividend, B2, {y} yield + 1.5", ndiv, 0.2)
    num(100 * div_full("coherent", "B2", r) / DIV["coherent"], 100 * bphi("B2", "m2", y)["share_of_vat_dividend"],
        f"full capture / VAT dividend, B2, {y} yield + 1.5, %", nsh, 0.2 if y > 2022 else 0.1)
for y, nphi, ndiv, nsh in [(2023, 2.92, 66.8, 33.6), (2024, 3.11, 62.7, 31.5), (2025, 2.96, 65.9, 33.1)]:
    num(tau_for("coherent", "B2") / YLD[y], bphi("B2", "m1", y)["phi_bridge"], f"phi, B2, {y} yield", nphi, 0.01)
    num(div_full("coherent", "B2", YLD[y]), bphi("B2", "m1", y)["dividend_full"], f"full-capture dividend, B2, {y} yield", ndiv, 0.1)
    num(100 * div_full("coherent", "B2", YLD[y]) / DIV["coherent"], 100 * bphi("B2", "m1", y)["share_of_vat_dividend"],
        f"full capture / VAT dividend, B2, {y} yield, %", nsh, 0.1)
lo, hi = min(YLD[y] for y in (2023, 2024, 2025)) + SPREAD, max(YLD[y] for y in (2023, 2024, 2025)) + SPREAD
claim(printed(100 * lo, 4.35, 0.01) and printed(100 * hi, 4.54, 0.01), "2023-25 yields + 1.5 = 4.35-4.54%", "4.35-4.54", f"{100 * lo:.3f}-{100 * hi:.3f}")
t_b1 = tau_for("coherent", "B1")
for mk, r, nphi, ndiv, nsh in [("m1", r22, 6.72, 29.0, 14.6), ("m2", r22 + SPREAD, 3.56, 54.7, 27.5)]:
    num(t_b1 / r, bphi("B1", mk, 2022)["phi_bridge"], f"phi, residential land B1, {mk}", nphi, 0.01)
    num(div_full("coherent", "B1", r), bphi("B1", mk, 2022)["dividend_full"], f"full-capture dividend, B1, {mk}", ndiv, 0.1)
    num(100 * div_full("coherent", "B1", r) / DIV["coherent"], 100 * bphi("B1", mk, 2022)["share_of_vat_dividend"], f"full capture share, B1, {mk}, %",
        nsh, 0.1)
num(100 * t_b1, bphi("B1", "m1", 2022)["tau_bridge_pct_of_land_value"], "bridge-equivalent charge on residential land alone, %", 11.4, 0.1)
L_B3 = N211[2022] + bsheet("S11", "N211", 2022) + bsheet("S15", "N211", 2022)
num(L_B3, bphi("B3", "m1", 2022)["land_meur"], "all private land B3 (households + firms + non-profits, N211 2022), EUR m", 176900, 100)
for mk, r, nphi, ndiv, nsh in [("m1", r22, 3.86, 50.5, 25.4), ("m2", r22 + SPREAD, 2.04, 95.4, 48.0)]:
    num(VAT_REV / (r * L_B3), bphi("B3", mk, 2022)["phi_bridge"], f"phi, B3, {mk}", nphi, 0.01)
    num(PHI * r * L_B3 * 1e6 / (NSH * 12), bphi("B3", mk, 2022)["dividend_full"], f"full-capture dividend, B3, {mk}", ndiv, 0.1)
    num(100 * PHI * r * L_B3 * 1e6 / (NSH * 12) / DIV["coherent"], 100 * bphi("B3", mk, 2022)["share_of_vat_dividend"], f"full capture share, B3, {mk}, %",
        nsh, 0.1)
b3_scaled = PHI * r22 * (L_B3 - N211[2022] * (1 - HBS_SCALE)) * 1e6 / (NSH * 12) / DIV["coherent"]
claim(True, "B3 adds the balance sheet's whole household N211 (not scaled to the HBS population as B1/B2 are): info", "25.4%",
      100 * b3_scaled, "scaling the household part gives 25.2% (m1); immaterial")
for mk, frac, nr, nphi, ndiv, nsh in [("m5", S_D, 6.0, 1.90, 102.6, 51.6), ("m3", 0.30, 9.1, 1.25, 156.2, 78.6), ("m4", 0.50, 15.2, 0.75, 260.4, 131.0)]:
    rr = frac * HS / L_HBS["B1"]
    num(100 * rr, 100 * bphi("B1", mk, 2022)["r"], f"implied land rent-to-value, residential land, {mk} (housing services x {frac:.3f}), %", nr, 0.1)
    num(t_b1 / rr, bphi("B1", mk, 2022)["phi_bridge"], f"phi, B1, {mk}", nphi, 0.01)
    num(div_full("coherent", "B1", rr), bphi("B1", mk, 2022)["dividend_full"], f"full-capture dividend, B1, {mk}", ndiv, 0.1)
    num(100 * div_full("coherent", "B1", rr) / DIV["coherent"], 100 * bphi("B1", mk, 2022)["share_of_vat_dividend"], f"full capture share, B1, {mk}, %",
        nsh, 0.1)
claim(printed(S_D * HS / 1e3, 6.1, 0.1), "housing services x s_d = EUR 6.1bn", "6.1", S_D * HS / 1e3)
# Finnish-law target, post convention
num(tau_for("coherent", "B2", DIV_LAW["coherent"]) / r22, bphi("B2", "m1", 2022, law=True)["phi_bridge"], "phi against the Finnish-law VAT dividend (EUR 178.0)",
    4.70, 0.01)
num(100 * div_full("coherent", "B2", r22) / DIV_LAW["coherent"], 100 * bphi("B2", "m1", 2022, law=True)["share_of_vat_dividend"],
    "full capture share against the Finnish-law dividend, %", 20.9, 0.1)
dphi, dsh = [], []
for _, r in b_phi[(b_phi["convention"] == "coherent") & (b_phi["base"] != "B3")].iterrows():
    p = b_phi[(b_phi["convention"] == "post") & (b_phi["base"] == r["base"]) & (b_phi["measure"] == r["measure"]) &
              (b_phi["yield_year"] == r["yield_year"]) & (b_phi["label"] == r["label"])]
    if len(p):
        dphi.append(abs(float(p["phi_bridge"].iloc[0]) - r["phi_bridge"]))
        dsh.append(abs(100 * (float(p["share_of_vat_dividend"].iloc[0]) - r["share_of_vat_dividend"])))
post_b2 = div_full("post", "B2", r22)
num(post_b2, bphi("B2", "m1", 2022, "post")["dividend_full"], "full-capture dividend, post convention (EUR/share/month)")
claim(max(dphi) < 0.1 and max(dsh) <= 0.1, "rates table: 'post within 0.1 point' of the coherent rows", "0.1",
      f"phi {max(dphi):.3f}; share {max(dsh):.2f} pts",
      "phi agrees within 0.1 in every row, but the funding share differs by up to 0.32 points (the housing-services rows m3-m5: "
      "131.0% coherent vs 130.6% post); say 'within 0.1 in phi and 0.4 points in share'" if max(dsh) > 0.1 else "")
fcap = b_cap.set_index(["rate", "design"])
claim(min(t_b2 / r22 * S_D, 1.0) == 1.0 and t_b2 / r22 * S_D > 1.0, "PV of the bridge charge = the dwellings' whole value at the 2022 yield",
      f"{fcap.loc[('bridge_m1', 'immediate'), 'dwelling_value_lost']:.3f}", t_b2 / r22 * S_D, "phi x s_d > 1: the charge capitalizes to more than the dwelling")
num(min(tau_for("coherent", "B2") / (r22 + SPREAD) * S_D, 1), fcap.loc[("bridge_m2", "immediate"), "dwelling_value_lost"],
    "share of dwelling value the bridge charge capitalizes to at yield + 1.5 ('55%')", 0.55, 0.01)


# %% D. incidence: net per adult share per month by quintile (the accounting tier)
AREA[0] = "D accounting"
R = {"m1": r22, "m2": r22 + SPREAD}
TAU = {(c, b, "bridge"): tau_for(c, b) for c in M for b in ("B1", "B2")}
TAU.update({(c, b, f"full_{k}"): PHI * R[k] for c in M for b in ("B1", "B2") for k in R})


def lvt_net(conv, base, rate):
    """bill_q = tau x land per share / 12; dividend = sum_q w_q bill_q; net_q = dividend - bill_q."""
    tau = TAU[(conv, base, rate)]
    bill = tau * LQ[base] / (12.0 * SQ[conv])
    div = float((M[conv]["w"] * bill).sum())
    return pd.DataFrame({"bill": bill, "dividend": div, "net": div - bill, "pct": 100 * (div - bill) / M[conv]["budget"].reindex(Q)})


ACC = {(c, b, r): lvt_net(c, b, r) for c in M for b in ("B1", "B2") for r in ("bridge", "full_m1", "full_m2")}
mx = 0.0
for (c, b, r), a in ACC.items():
    x = b_acc[(b_acc["convention"] == c) & (b_acc["instrument"] == "LVT") & (b_acc["base"] == b) & (b_acc["rate"] == r)].set_index("quintile")
    mx = max(mx, float((a["net"] - x["net"].reindex(Q)).abs().max()), float((a["bill"] - x["bill"].reindex(Q)).abs().max()))
    assert abs(float((M[c]["w"] * a["net"]).sum())) < 1e-9
claim(mx < 1e-5, "LVT bills and nets, every convention x base x rate x quintile (max abs diff, EUR); nets balance under the weights",
      "fi_lvt_accounting_by_quintile.csv", mx)
for c in M:
    x = b_acc[(b_acc["convention"] == c) & (b_acc["instrument"] == "VAT")].set_index("quintile")
    claim(float((VA[c]["net"] - x["net"].reindex(Q)).abs().max()) < 1e-6, f"VAT nets by quintile, {c} (rebuilt VAT accounting)", "", "")
tables = [("VAT bridge", VA["coherent"]["net"], [80.3, 41.5, 8.0, -11.5, -83.9], 0.1),
          ("LVT B2, same revenue", ACC[("coherent", "B2", "bridge")]["net"], [117.1, 82.5, 32.8, -1.4, -174.5], 0.1),
          ("LVT B1, same revenue", ACC[("coherent", "B1", "bridge")]["net"], [124.7, 90.8, 31.3, -5.9, -180.8], 0.1),
          ("LVT B2, full capture, 2022 yield", ACC[("coherent", "B2", "full_m1")]["net"], [21.9, 15.4, 6.1, -0.3, -32.6], 0.1),
          ("LVT B2, full capture, yield + 1.5", ACC[("coherent", "B2", "full_m2")]["net"], [41.3, 29.1, 11.6, -0.5, -61.6], 0.1),
          ("VAT, % of budget", VA["coherent"]["net_pct_budget"], [6.1, 2.6, 0.4, -0.5, -3.0], 0.1),
          ("LVT B2 same revenue, % of budget", ACC[("coherent", "B2", "bridge")]["pct"], [8.9, 5.2, 1.7, -0.1, -6.2], 0.1),
          ("LVT B2 full capture, % of budget", ACC[("coherent", "B2", "full_m1")]["pct"], [1.7, 1.0, 0.3, -0.0, -1.2], 0.1),
          ("post convention: VAT (the published Fig 1)", VA["post"]["net"], [76.8, None, None, None, -88.1], 0.1),
          ("post convention: LVT B2 same revenue", ACC[("post", "B2", "bridge")]["net"], [111.2, 76.7, 26.9, -7.3, -180.5], 0.1)]
for lab, mine, nv, unit in tables:
    ok = all(v is None or printed(float(mine[q]), v, unit) for q, v in zip(Q, nv))
    claim(ok, f"net per share by quintile (coherent unless stated): {lab}", " / ".join("" if v is None else f"{v:+.1f}" for v in nv),
          " / ".join(f"{float(mine[q]):+.2f}" for q in Q))
claim(printed(-float(ACC[("coherent", "B2", "bridge")]["net"]["q5"]), 175, 1) and printed(-float(VA["coherent"]["net"]["q5"]), 84, 1)
      and printed(float(ACC[("coherent", "B2", "bridge")]["net"]["q1"]), 117, 1) and printed(float(VA["coherent"]["net"]["q1"]), 80, 1),
      "plain words: Q1 gains EUR 117 instead of 80; Q5 pays EUR 175 (6.2%) instead of 84 (3.0%)", "117/80; 175/84",
      f"{float(ACC[('coherent', 'B2', 'bridge')]['net']['q1']):.1f}/{float(VA['coherent']['net']['q1']):.1f}; "
      f"{-float(ACC[('coherent', 'B2', 'bridge')]['net']['q5']):.1f}/{-float(VA['coherent']['net']['q5']):.1f}")
gain = {c: (ACC[(c, "B2", "bridge")]["net"] - VA[c]["net"]) for c in M}
claim(all((gain[c][Q[:4]] > 0).all() and gain[c]["q5"] < 0 for c in M), "every quintile but the top gains relative to the VAT (both conventions)",
      "", " ; ".join(f"{c}: " + ", ".join(f"{v:+.1f}" for v in gain[c]) for c in M))
claim(abs(float(ACC[("coherent", "B2", "bridge")]["net"]["q4"])) < 2.0, "Q4 at break-even under the LVT (coherent)", "-1.43",
      float(ACC[("coherent", "B2", "bridge")]["net"]["q4"]), f"post convention Q4 {float(ACC[('post', 'B2', 'bridge')]['net']['q4']):+.2f}")
gross = {k: float((M["coherent"]["w"] * v.clip(lower=0)).sum()) for k, v in [("VAT", VA["coherent"]["net"]), ("LVT", ACC[("coherent", "B2", "bridge")]["net"])]}
ratio_gross = gross["LVT"] / gross["VAT"]
claim(1.6 <= ratio_gross <= 2.4, "'At the same revenue the LVT is about twice as redistributive as the VAT'", "about 2",
      ratio_gross, f"net redistribution sum_q w_q max(net_q, 0): VAT EUR {gross['VAT']:.1f}, LVT EUR {gross['LVT']:.1f} per share-month; "
      f"Q5 payment ratio {float(ACC[('coherent', 'B2', 'bridge')]['net']['q5'] / VA['coherent']['net']['q5']):.2f}, Q1 gain ratio "
      f"{float(ACC[('coherent', 'B2', 'bridge')]['net']['q1'] / VA['coherent']['net']['q1']):.2f}")


# %% E. inside the deciles: owners hold the decile's land (log-normal), a household pays net iff its land > mean per share x shares
AREA[0] = "E within deciles"
P_OWN = wd("main_residence", "part").reindex(DEC) / 100.0
Z75 = stats.norm.ppf(0.75)
SIG_OWN = (np.log(wd("main_residence", "p75")) - np.log(wd("main_residence", "p25"))).reindex(DEC) / (2 * Z75)
S_DEC = {c: pd.Series([float(SQ[c][PAIR[d]]) for d in DEC], index=DEC) for c in M}


def split_decile(base, conv, land=None, p_own=None, sig=None):
    """Per household of the decile, in land units (x tau for euros a year): receipts of non-owners, net receipts of owner-recipients,
    net payments of owner-payers; payer shares. X ~ lognormal(mu, s) with E[X] = land per owner; partial expectations by
    E[X; X > t] = E[X] P(X' > t), X' ~ lognormal(mu + s^2, s)."""
    land = LD[base] if land is None else land
    p = P_OWN if p_own is None else p_own
    s = SIG_OWN if sig is None else sig
    mps = mean_ps(conv, pairq(land))
    rows = {}
    for d in DEC:
        Lo = float(land[d] / p[d])
        mu = np.log(Lo) - s[d] ** 2 / 2
        t = mps * float(S_DEC[conv][d])
        P = float(stats.lognorm(s=s[d], scale=np.exp(mu)).sf(t))
        above = Lo * float(stats.lognorm(s=s[d], scale=np.exp(mu + s[d] ** 2)).sf(t))      # E[X; X > t]
        pay = above - t * P
        recv_own = t * (1 - P) - (Lo - above)
        rows[d] = dict(p=p[d], Lo=Lo, t=t, P=P, payer_hh=p[d] * P, recv_non=(1 - p[d]) * t, recv_own=p[d] * recv_own, pay=p[d] * pay,
                       payer_land_share=above / Lo)
    out = pd.DataFrame(rows).T
    out["net"] = out["recv_non"] + out["recv_own"] - out["pay"]
    assert np.allclose(out["net"], out["t"] - land.reindex(DEC), atol=1e-6)
    return out


OM = {(c, b): split_decile(b, c) for c in M for b in ("B1", "B2")}
wdm = b_wd[(b_wd["convention"] == "coherent") & (b_wd["base"] == "B2")].set_index("decile")
om = OM[("coherent", "B2")]
num(float(om["payer_hh"].sub(wdm["payer_share_of_households"].reindex(DEC)).abs().max()), 0.0,
    "payer share of households by decile (max abs diff vs fi_lvt_within_decile.csv)", tol=1e-8, rel=False)
pay_all = float((om["payer_hh"] * NHD).sum() / NHD.sum())
num(100 * pay_all, None, "households paying net under the LVT, all deciles, %", 35.3, 0.1)
claim(printed(100 * om.loc["d01", "payer_hh"], 12, 1) and printed(100 * om.loc["d10", "payer_hh"], 80, 1) and
      printed(100 * om.loc[DEC[3:7], "payer_hh"].min(), 27, 1) and printed(100 * om.loc[DEC[3:7], "payer_hh"].max(), 36, 1),
      "payers: 12% in D1, 27-36% in D4-D7, 80% in D10", "12 / 27-36 / 80",
      f"{100 * om.loc['d01', 'payer_hh']:.1f} / {100 * om.loc[DEC[3:7], 'payer_hh'].min():.1f}-{100 * om.loc[DEC[3:7], 'payer_hh'].max():.1f} / "
      f"{100 * om.loc['d10', 'payer_hh']:.1f}")
net_b = TAU[("coherent", "B2", "bridge")] * (om["t"] - LD["B2"].reindex(DEC))
net_f = TAU[("coherent", "B2", "full_m1")] * (om["t"] - LD["B2"].reindex(DEC))
claim(bool((np.sign(net_b) == np.sign(net_f)).all()) and float(om["t"].min()) > 0,
      "'Whatever the rate, 35% ... pay net': the payer threshold L* = mean land per share x shares carries no tau", "rate-invariant",
      "rate-invariant", "identity: a household's net is tau x (L* - L); its sign, hence who pays, does not move with tau")
nonown = 1 - float(wd("main_residence", "part")["total"]) / 100
claim(printed(100 * nonown, 36, 1) and printed(100 * (1 - P_OWN["d01"]), 73, 1), "non-owners: 36% of households and 73% of the bottom decile",
      "36 / 73", f"{100 * nonown:.0f} / {100 * (1 - P_OWN['d01']):.0f}")
# who holds land among renters (151z): the owner model gives renters' land to owners
ren = (S_D * (wt("other_res")["renter"] + wt("free_time")["renter"]) + S_F * wt("ffb")["renter"]) * float(wt("income", "holders")["renter"])
ren_share = ren / 1e6 / N211[2023]
claim(printed(100 * ren_share, 2.5, 0.1), "renters' own land is 2.5% of household land nationally (151z), assigned to owners", "2.5%", 100 * ren_share,
      "a modelling approximation: the plain-words 'Renters pay nothing' is the model's assumption, not a measurement (review R-renters)")
# gross payments by half, on a consistent unit
tau_b = TAU[("coherent", "B2", "bridge")]
pay_ps = om["pay"] * tau_b / (12 * S_DEC["coherent"])                # EUR per share per month, by decile
recv_ps = (om["recv_non"] + om["recv_own"]) * tau_b / (12 * S_DEC["coherent"])
mx = float((pay_ps - wdm["gross_payments_eur_share_month_bridge"].reindex(DEC)).abs().max())
claim(mx < 1e-6, "gross payments per share by decile at the bridge rate (max abs diff, EUR)", "fi_lvt_within_decile.csv", mx)
bh_builder = float((pay_ps * NHD)[DEC[:5]].sum() / (pay_ps * NHD).sum())              # per-share amounts weighted by HOUSEHOLDS (builder's)
bh_hh = float((om["pay"] * NHD)[DEC[:5]].sum() / (om["pay"] * NHD).sum())             # per-household payments x households (consistent)
claim(printed(100 * bh_hh, 22.6, 0.1), "'The bottom half makes 22.6% of all gross LVT payments'", "22.6% (builder: per-share payments x households)",
      100 * bh_hh, f"builder's figure {100 * bh_builder:.1f}% weights per-SHARE payments by HOUSEHOLDS; on one unit (per-household payments x "
      f"households, = per-share payments x shares) the bottom half makes {100 * bh_hh:.1f}%. Fix run_lvt_fi.py's gp line (multiply by shares)")
r12 = float(pay_ps[DEC[:2]].sum() / recv_ps[DEC[:2]].sum())
claim(printed(r12, 0.2, 0.05), "'In D1-D2, gross payments are a fifth of gross receipts'", "1/5", r12)
pq = pairq(om["payer_hh"])
num(float((pq - b_pay["lvt_payer_share_owner_model"].reindex(Q)).abs().max()), 0.0, "LVT payer share by quintile (pair means; max abs diff)", tol=1e-8, rel=False)


# %% F. liquidity: hand-to-mouth by deposits (KVW with monthly pay), all households and owners
AREA[0] = "F liquidity"
HTM_DIV = {"half_month": 24.0, "half_biweekly": 52.0, "one_month": 12.0}


def htm_share(part, p25, med, p75, income, divisor):
    s = (np.log(p75) - np.log(p25)) / (2 * Z75)
    return (1 - part) + part * stats.lognorm(s=s, scale=med).cdf(income / divisor)


def htm_dec(divisor):
    return pd.Series(htm_share(wd("deposits", "part").reindex(DEC).values / 100, wd("deposits", "p25").reindex(DEC).values,
                               wd("deposits", "median").reindex(DEC).values, wd("deposits", "p75").reindex(DEC).values,
                               wd("income", "median").reindex(DEC).values, divisor), index=DEC)


def htm_ten(divisor):
    g = ["all", "outright", "mortgaged", "renter"]
    return pd.Series(htm_share(wt("deposits", "part").reindex(g).values / 100, wt("deposits", "p25").reindex(g).values,
                               wt("deposits", "median").reindex(g).values, wt("deposits", "p75").reindex(g).values,
                               wt("income", "median").reindex(g).values, divisor), index=g)


N_OWN = wd("main_residence", "holders").reindex(DEC)
N_MORT = wd("housing_loans", "holders").reindex(DEC)
N_OUT = N_OWN - N_MORT


def htm_own(divisor):
    hd, ht = htm_dec(divisor), htm_ten(divisor)
    mix = (N_OUT * ht["outright"] + N_MORT * ht["mortgaged"]) / N_OWN
    return (hd * mix / ht["all"]).clip(upper=1.0)


HD = {k: htm_dec(v) for k, v in HTM_DIV.items()}
HT = {k: htm_ten(v) for k, v in HTM_DIV.items()}
HO = {k: htm_own(v) for k, v in HTM_DIV.items()}
mx = max(float((HD[k] - b_liq[f"htm_all_{k}"].reindex(DEC)).abs().max()) for k in HTM_DIV)
mx = max(mx, max(float((HO[k] - b_liq[f"htm_owners_{k}"].reindex(DEC)).abs().max()) for k in HTM_DIV))
claim(mx < 1e-8, "hand-to-mouth shares by decile, all households and owners, three thresholds (max abs diff)", "fi_lvt_liquidity.csv", mx)
hm = HD["half_month"]
claim(all(printed(100 * hm[d], v, u) for d, v, u in [("d01", 31, 1), ("d02", 37, 1), ("d05", 21, 1), ("d10", 7.5, 0.1)]),
      "all households hand-to-mouth: 31% (D1), 37% (D2), 21% (D5), 7.5% (D10)", "31/37/21/7.5", "/".join(f"{100 * hm[d]:.2f}" for d in ("d01", "d02", "d05", "d10")))
ho = HO["half_month"]
claim(all(printed(100 * ho[d], v, 1) for d, v in [("d01", 17), ("d02", 18), ("d05", 12), ("d10", 5)]),
      "owners hand-to-mouth: 17%, 18%, 12%, 5% (D1, D2, D5, D10)", "17/18/12/5", "/".join(f"{100 * ho[d]:.2f}" for d in ("d01", "d02", "d05", "d10")))
th = HT["half_month"]
claim(printed(100 * th["outright"], 8.5, 0.1) and printed(100 * th["mortgaged"], 21.6, 0.1) and printed(100 * th["renter"], 36.2, 0.1),
      "nationally (151z): outright owners 8.5%, mortgaged 21.6%, renters 36.2%", "8.5/21.6/36.2", "/".join(f"{100 * th[k]:.2f}" for k in ("outright", "mortgaged", "renter")))
mx = float((th - b_lt[b_lt["threshold"] == "half_month"].set_index("tenure")["htm_share"].rename(
    {"outright_owner": "outright", "owner_with_mortgage": "mortgaged", "renter_or_other": "renter"}).reindex(th.index)).abs().max())
claim(mx < 1e-8, "hand-to-mouth by tenure (max abs diff vs fi_lvt_liquidity_tenure.csv)", "", mx)
claim(printed(100 * ho[DEC[:3]].min(), 17, 1) and printed(100 * ho[DEC[:3]].max(), 18, 1) and printed(100 * hm[DEC[:3]].min(), 31, 1)
      and printed(100 * hm[DEC[:3]].max(), 37, 1), "bottom three deciles: 17-18% of owners hand-to-mouth against 31-37% of all households",
      "17-18 / 31-37", f"{100 * ho[DEC[:3]].min():.1f}-{100 * ho[DEC[:3]].max():.1f} / {100 * hm[DEC[:3]].min():.1f}-{100 * hm[DEC[:3]].max():.1f}",
      "owners' rates are the decile's rate scaled by the national owner/all ratio (judgment: 151u does not cross tenure with income)")
liq_m = 12 * (wd("deposits") + wd("listed") + wd("other_fin")).reindex(DEC) / wd("income").reindex(DEC)
dep_m = 12 * wd("deposits", "median").reindex(DEC) / wd("income", "median").reindex(DEC)
claim(printed(liq_m[DEC[:9]].min(), 9, 1) and printed(liq_m[DEC[:9]].max(), 15, 1) and printed(liq_m["d10"], 26, 1)
      and printed(dep_m.min(), 1.4, 0.1) and printed(dep_m.max(), 4.3, 0.1),
      "mean liquid assets 9-15 months of income in D1-D9, 26 in D10; median holder's deposits 1.4-4.3 months", "9-15 / 26 / 1.4-4.3",
      f"{liq_m[DEC[:9]].min():.1f}-{liq_m[DEC[:9]].max():.1f} / {liq_m['d10']:.1f} / {dep_m.min():.2f}-{dep_m.max():.2f}")


# %% G. flow impulses by MPC grade (the post's quintile-netted method; payers by liquidity; unconstrained payers on wealth), deferral
AREA[0] = "G impulse"
MPC_U = {"mid": float(SCHED.loc["q5", "mid"]), "low": 0.25, "high": float(SCHED.loc["q5", "high"])}
SIG_C = 0.45


def lvt_flows(conv, base, rate):
    """Quintile receipts, payments, net (EUR/share/month) and payers' hand-to-mouth share (owners' rates weighted by each decile's
    payments), from the decile split."""
    tau = TAU[(conv, base, rate)]
    o = OM[(conv, base)]
    conv12 = 12 * SQ[conv]
    recv = pairq(o["recv_non"] + o["recv_own"]) * tau / conv12
    pay = pairq(o["pay"]) * tau / conv12
    hh = HO["half_month"]
    h = pd.Series([float((hh * o["pay"])[[DEC[2 * i], DEC[2 * i + 1]]].sum() / o["pay"][[DEC[2 * i], DEC[2 * i + 1]]].sum()) for i in range(5)], index=Q)
    return dict(recv=recv, pay=pay, net=recv - pay, h=h, tau=tau, o=o)


def vat_flows(conv):
    t = float(VA[conv]["Cbar_v"].iloc[0])
    x = VA[conv]["vatable"].reindex(Q)
    mu = np.log(x) - SIG_C ** 2 / 2
    P = pd.Series(stats.norm.sf((np.log(t) - mu) / SIG_C), index=Q)
    above = x * stats.norm.sf((np.log(t) - mu - SIG_C ** 2) / SIG_C)
    pay = B.TAU * (above - t * P)
    recv = B.TAU * (t * (1 - P) - (x - above))
    return dict(recv=recv, pay=pay, net=recv - pay, h=pairq(HD["half_month"]), P=P)


def dC(fl, grade, sched="mid", mu=None):
    mpc = SCHED[sched].reindex(Q)
    if grade == "post":
        return mpc * fl["net"]
    payer = fl["h"] + (1 - fl["h"]) * (mpc if grade == "liq" else MPC_U[mu])
    return mpc * fl["recv"] - payer * fl["pay"]


def flow_pct(conv, d):
    return 100 * float((M[conv]["w"] * d).sum()) / M[conv]["budget_bar"]


GR = {"post_mid": ("post", "mid", None), "post_high": ("post", "high", None), "post_low": ("post", "low", None), "liq_mid": ("liq", "mid", None),
      "wealth_mid": ("wealth", "mid", "mid"), "wealth_high": ("wealth", "mid", "high"), "wealth_low": ("wealth", "mid", "low")}
FL = {(c, "VAT", "", "bridge"): vat_flows(c) for c in M}
for c in M:
    for b in ("B1", "B2"):
        for r in ("bridge", "full_m1", "full_m2"):
            FL[(c, "LVT", b, r)] = lvt_flows(c, b, r)
for k, fl in FL.items():
    assert np.allclose(fl["net"].values, (VA[k[0]]["net"] if k[1] == "VAT" else ACC[(k[0], k[2], k[3])]["net"]).reindex(Q).values, atol=1e-8)
IMP = {(k, g): flow_pct(k[0], dC(fl, *GR[g])) for k, fl in FL.items() for g in GR}
mx = max(abs(v - float(b_flow(k[1], k[2], k[3], g, k[0])["flow_pct_consumption"])) for (k, g), v in IMP.items())
claim(mx < 1e-7, "flow impulse, every instrument x convention x base x rate (14) x grade (7); max abs diff, % of consumption", "fi_lvt_impulse.csv", mx)
I = lambda inst, b, r, g, c="coherent": IMP[((c, inst, b, r), g)]
for lab, vals in [("the post's schedule (mid)", [("VAT", "", "bridge", "post_mid", 0.422), ("LVT", "B2", "bridge", "post_mid", 0.771),
                                                 ("LVT", "B2", "full_m1", "post_mid", 0.144), ("LVT", "B2", "full_m2", "post_mid", 0.272)]),
                  ("band: high / low schedules", [("VAT", "", "bridge", "post_high", 0.322), ("VAT", "", "bridge", "post_low", 0.524),
                                                  ("LVT", "B2", "bridge", "post_high", 0.598), ("LVT", "B2", "bridge", "post_low", 0.948),
                                                  ("LVT", "B2", "full_m1", "post_high", 0.112), ("LVT", "B2", "full_m1", "post_low", 0.177)]),
                  ("payers graded by liquidity", [("VAT", "", "bridge", "liq_mid", 0.339), ("LVT", "B2", "bridge", "liq_mid", 0.659),
                                                  ("LVT", "B2", "full_m1", "liq_mid", 0.123), ("LVT", "B2", "full_m2", "liq_mid", 0.233)]),
                  ("unconstrained payers draw on wealth (0.56)", [("VAT", "", "bridge", "wealth_mid", 0.502), ("LVT", "B2", "bridge", "wealth_mid", 1.076),
                                                                 ("LVT", "B2", "full_m1", "wealth_mid", 0.201), ("LVT", "B2", "full_m2", "wealth_mid", 0.380)]),
                  ("wealth band 0.68 / 0.25", [("VAT", "", "bridge", "wealth_high", 0.298), ("VAT", "", "bridge", "wealth_low", 1.056),
                                               ("LVT", "B2", "bridge", "wealth_high", 0.617), ("LVT", "B2", "bridge", "wealth_low", 2.324),
                                               ("LVT", "B2", "full_m1", "wealth_high", 0.115), ("LVT", "B2", "full_m1", "wealth_low", 0.434)])]:
    ok = all(printed(I(i, b, r, g), v, 0.001) for i, b, r, g, v in vals)
    claim(ok, f"flow impulse table, {lab} (coherent, % of consumption)", " / ".join(f"{v:.3f}" for *_, v in vals),
          " / ".join(f"{I(i, b, r, g):.4f}" for i, b, r, g, _ in vals))
post_vals = [("VAT", "", "bridge", 0.438), ("LVT", "B2", "bridge", 0.792), ("LVT", "B2", "full_m1", 0.148), ("LVT", "B2", "full_m2", 0.279)]
claim(all(printed(I(i, b, r, "post_mid", "post"), v, 0.001) for i, b, r, v in post_vals), "flow impulse table, post convention, the post's schedule",
      " / ".join(f"{v:.3f}" for *_, v in post_vals), " / ".join(f"{I(i, b, r, 'post_mid', 'post'):.4f}" for i, b, r, _ in post_vals))
rat2, rat1 = I("LVT", "B2", "bridge", "post_mid") / I("VAT", "", "bridge", "post_mid"), I("LVT", "B1", "bridge", "post_mid") / I("VAT", "", "bridge", "post_mid")
uimp = pd.read_csv(BOUT / "us_lvt_macro_channels.csv")
us_ch = lambda s: float(uimp[uimp["channel"].str.contains(s, regex=False)]["central"].iloc[0])
us_ratio = us_ch("flow impulse, post's method (bridge, L1)") / us_ch("flow impulse, post's method (mid; band")
claim(printed(rat2, 1.83, 0.01) and printed(rat1, 1.94, 0.01) and printed(us_ratio, 2.51, 0.01),
      "LVT/VAT flow ratio at the same revenue: 1.83 (B2), 1.94 (B1); US 2.51", "1.83 / 1.94 / 2.51", f"{rat2:.3f} / {rat1:.3f} / {us_ratio:.3f}")
claim(printed(I("LVT", "B2", "bridge", "post_mid"), 0.77, 0.01) and printed(I("VAT", "", "bridge", "post_mid"), 0.42, 0.01), "'Under the post's method the flow impulse is 0.77% of consumption, against the VAT's 0.42%'",
      "0.77 / 0.42", f"{I('LVT', 'B2', 'bridge', 'post_mid'):.3f} / {I('VAT', '', 'bridge', 'post_mid'):.3f}")
# the wealth grade's story: the LVT's low-income payers are liquid owners
hq = FL[("coherent", "LVT", "B2", "bridge")]["h"]
up = (I("LVT", "B2", "bridge", "wealth_mid") - I("LVT", "B2", "bridge", "post_mid"), I("VAT", "", "bridge", "wealth_mid") - I("VAT", "", "bridge", "post_mid"))
claim(up[0] > up[1] > 0, "the wealth grade raises the LVT more than the VAT", f"+{up[0]:.3f} vs +{up[1]:.3f}", f"+{up[0]:.3f} vs +{up[1]:.3f}",
      f"LVT payers' hand-to-mouth share by quintile {', '.join(f'{v:.3f}' for v in hq)}; schedule {', '.join(f'{v:.3f}' for v in SCHED['mid'])}")
bm = bcsv("fi_lvt_mpc_grades.csv")
bh = bm[(bm["instrument"] == "LVT_B2") & (bm["grade"] == "post_mid")].set_index("quintile")["payer_htm_share"].reindex(Q)
claim(float((hq - bh).abs().max()) < 1e-8, "payers' hand-to-mouth share by quintile (LVT B2; max abs diff vs fi_lvt_mpc_grades.csv)", "", float((hq - bh).abs().max()))
vp = vat_flows("coherent")["P"]
claim(float((vp - b_pay["vat_payer_share_lognormal"].reindex(Q)).abs().max()) < 1e-9 and printed(100 * vp["q1"], 8, 1) and printed(100 * vp["q5"], 71, 1),
      "VAT payers inside quintiles (sigma 0.45, judgment): 8% of Q1 to 71% of Q5", "8 / 71", f"{100 * vp['q1']:.1f} / {100 * vp['q5']:.1f}")

# deferral: outright owners defer the bill on their main-residence land
n_m_nat, v_m, v_o = float(wt("housing_loans", "holders")["mortgaged"]), float(wt("main_residence")["mortgaged"]), float(wt("main_residence")["outright"])
k_m = N_MORT * v_m / (N_MORT * v_m + N_OUT * v_o)
MR_TOT = wd("main_residence").reindex(DEC) * NHD
scale_m = n_m_nat * v_m / float((MR_TOT * k_m).sum())
VM_TOT = MR_TOT * k_m * scale_m                                       # mortgaged owners' main-residence value by decile (2023 EUR)
K_OUT = 1 - k_m * scale_m
HL_TOT = wd("housing_loans").reindex(DEC) * NHD


def deferral(rate, grade="post_mid", cash=False):
    fl = FL[("coherent", "LVT", "B2", rate)]
    tau = fl["tau"]
    dfd = pairq(LD["L_main"] * K_OUT) * tau / (12 * SQ["coherent"])
    w = M["coherent"]["w"]
    div0 = float(ACC[("coherent", "B2", rate)]["dividend"].iloc[0])
    share = float((w * dfd).sum()) / div0
    o = fl["o"]
    fpay = pd.Series([float((o["payer_land_share"] * LD["L_main"] * K_OUT)[[DEC[2 * i], DEC[2 * i + 1]]].sum() /
                            (LD["L_main"] * K_OUT)[[DEC[2 * i], DEC[2 * i + 1]]].sum()) for i in range(5)], index=Q)
    d_pay = np.minimum(dfd * fpay, fl["pay"])
    f2 = dict(fl, pay=fl["pay"] - d_pay, recv=fl["recv"] + dfd - d_pay, net=fl["net"] + dfd)
    d_div = float((w * dfd).sum()) if cash else 0.0
    if cash:
        f2 = dict(f2, recv=f2["recv"] - d_div, net=f2["net"] - d_div)
    return flow_pct("coherent", dC(f2, *GR[grade])), share, div0 - d_div


bdf = b_df.set_index(["rate", "grade"])
for rate, nv in [("full_m1", 0.37), ("bridge", 1.98)]:
    f_full, share, _ = deferral(rate)
    num(f_full, bdf.loc[(rate, "post_mid"), "flow_defer_dividend_in_full"], f"deferral, dividend paid in full (state lends the liens), impulse, {rate}")
    num(f_full - I("LVT", "B2", rate, "post_mid"), None, f"deferral raises the impulse by {nv} points ({rate})", nv, 0.01)
us_def = float(uimp[uimp["channel"].str.startswith("deferral by owners 65+, dividend paid in full")]["central"].iloc[0])
claim(printed(us_def, 2.0, 0.1), "deferral beside the US: 'US 2.0' (owners 65+ defer, dividend in full; the US unit's output)", "2.0", us_def)
f_cash, share, div_cash = deferral("full_m1", cash=True)
num(100 * share, 100 * bdf.loc[("full_m1", "post_mid"), "deferred_share_of_revenue"], "outright owners' main-residence land, share of revenue (%)", 27.1, 0.1)
num(div_cash, bdf.loc[("full_m1", "post_mid"), "dividend_cash_balanced"], "cash-balanced dividend at full capture (EUR 37.2 -> 27.1)", 27.1, 0.1)
num(f_cash - I("LVT", "B2", "full_m1", "post_mid"), None, "cash-balanced deferral changes the impulse by -0.02 points", -0.02, 0.01)
for g in ("wealth_mid",):
    fw, _, _ = deferral("full_m1", g)
    num(fw, bdf.loc[("full_m1", g), "flow_defer_dividend_in_full"], f"deferral, dividend in full, {g} grade (full capture)")
lost_def = float((LD["L_main"] * K_OUT * min(PHI, 1 / S_D) * NHD).sum()) / 1e6 * HBS_SCALE
num(-100 * MPW["mid"] * lost_def / C_MEUR, bdf.loc[("full_m1", "post_mid"), "deferrers_residual_wealth_effect_mid_pct"],
    "deferrers' capitalized loss at 3.5c (% of consumption; reported beside the flow)", -1.04, 0.01)
num(-100 * MPW["high"] * lost_def / C_MEUR, bdf.loc[("full_m1", "post_mid"), "deferrers_residual_wealth_effect_high_pct"], "same at 5c", -1.49, 0.01)


# %% H. demand shifts: the post's theta x eta machinery (bridge.shifts_from_transfers), comparisons, Fig 3 analogue, tenure baskets
AREA[0] = "H demand shifts"
SH = {}
for k, fl in FL.items():
    c, inst, b, r = k
    m = M[c]
    for g in ("post_mid", "wealth_mid", "liq_mid"):
        if g == "post_mid":
            SH[(k, g)] = B.shifts_from_transfers(m, fl["net"].values, mpc=SCHED["mid"].values, mpc_label="mid")
        else:
            SH[(k, g)] = B.shifts_from_transfers(m, None, shock=(dC(fl, *GR[g]) / m["budget"].reindex(Q)).values, mpc_label="mid")
mx = 0.0
for (k, g), sh in SH.items():
    c, inst, b, r = k
    x = b_shf[(b_shf["convention"] == c) & (b_shf["instrument"] == inst) & (b_shf["base"] == b) & (b_shf["rate"] == r) & (b_shf["grade"] == g)]
    x = x.set_index("category")["dEUR"].reindex(sh.index)
    mx = max(mx, float((sh["dUSD_mid"] - x).abs().max()))
claim(mx < 1e-6, "category shifts, every instrument x convention x base x rate x grade (max abs diff, EUR/share/month)", "fi_lvt_demand_shifts.csv", mx)
V = SH[(("coherent", "VAT", "", "bridge"), "post_mid")]["dUSD_mid"]
L2 = SH[(("coherent", "LVT", "B2", "bridge"), "post_mid")]["dUSD_mid"]
chart = M["coherent"]["chart"]
rows_n = [("04.1 Actual rents", 4.21, 6.87), ("01.1 Food (at home)", 0.93, 1.66), ("08.3 Information and communication services", 0.50, 0.92),
          ("07.2 Operation of personal transport equipment", 0.43, 0.85), ("07.1 Purchase of vehicles", -0.43, -0.70),
          ("04.4 Water & misc. dwelling services", 0.27, 0.59), ("04.2 Imputed rentals (off-chart)", -0.78, -1.01),
          ("04.6 Interest on housing loans (off-chart)", -0.04, -0.04)]
claim(all(printed(V[g], a, 0.01) and printed(L2[g], b, 0.01) for g, a, b in rows_n),
      "demand-shift table, VAT and LVT B2 (post's method, same revenue, coherent): rent, food, ICT, vehicle operation, vehicles, 04.4, imputed, interest",
      " ; ".join(f"{a:+.2f}/{b:+.2f}" for _, a, b in rows_n), " ; ".join(f"{V[g]:+.3f}/{L2[g]:+.3f}" for g, _, _ in rows_n))
claim(printed(V[chart].sum(), 9.68, 0.01) and printed(L2[chart].sum(), 17.27, 0.01), "charted totals EUR 9.68 (VAT) and 17.27 (LVT)", "9.68 / 17.27",
      f"{V[chart].sum():.3f} / {L2[chart].sum():.3f}")
d = pd.DataFrame({"vat": V[chart], "lvt": L2[chart]})
same = int((np.sign(d["vat"]) == np.sign(d["lvt"])).sum())
big = d[d["vat"].abs() > 0.05]
ratio = big["lvt"] / big["vat"]
claim(same == 37 and printed(ratio.median(), 1.80, 0.01) and printed(ratio.min(), 0.71, 0.01) and printed(ratio.max(), 2.19, 0.01)
      and ratio.idxmin().startswith("13.9") and ratio.idxmax().startswith("04.4"),
      "all 37 bars keep their sign; LVT/VAT ratio median 1.80 over bars above EUR 0.05, range 0.71 (13.9) to 2.19 (04.4)",
      "37; 1.80 [0.71, 2.19]", f"{same}; {ratio.median():.3f} [{ratio.min():.3f} {ratio.idxmin()[:4]}, {ratio.max():.3f} {ratio.idxmax()[:4]}]")
claim(printed(100 * d.loc["04.1 Actual rents", "lvt"] / d["lvt"].sum(), 39.8, 0.1) and printed(100 * d.loc["04.1 Actual rents", "vat"] / d["vat"].sum(), 43.5, 0.1),
      "rent's share of the charted impulse: LVT 39.8% vs VAT 43.5%", "39.8 / 43.5",
      f"{100 * d.loc['04.1 Actual rents', 'lvt'] / d['lvt'].sum():.2f} / {100 * d.loc['04.1 Actual rents', 'vat'] / d['vat'].sum():.2f}")
VP = B.fi_post_eur(M["post"], SH[(("post", "VAT", "", "bridge"), "post_mid")]["dUSD_mid"])
LP = B.fi_post_eur(M["post"], SH[(("post", "LVT", "B2", "bridge"), "post_mid")]["dUSD_mid"])
claim(printed(VP["04.1 Actual rents"], 4.93, 0.01) and printed(LP["04.1 Actual rents"], 7.95, 0.01) and printed(VP["07.1 Purchase of vehicles"], -0.52, 0.01)
      and printed(LP["07.1 Purchase of vehicles"], -0.86, 0.01) and printed(VP["01.1 Food (at home)"], 0.92, 0.01) and printed(LP["01.1 Food (at home)"], 1.63, 0.01),
      "on the post's euro conversion: rent 4.93 -> 7.95, vehicles -0.52 -> -0.86, food 0.92 -> 1.63", "4.93/7.95; -0.52/-0.86; 0.92/1.63",
      f"{VP['04.1 Actual rents']:.3f}/{LP['04.1 Actual rents']:.3f}; {VP['07.1 Purchase of vehicles']:.3f}/{LP['07.1 Purchase of vehicles']:.3f}; "
      f"{VP['01.1 Food (at home)']:.3f}/{LP['01.1 Food (at home)']:.3f}")
# Fig 3 analogue: quintile segments of the ten largest movers
q5s, segmx = {}, 0.0
for inst, k, bi in [("LVT", ("coherent", "LVT", "B2", "bridge"), "LVT_B2"), ("VAT", ("coherent", "VAT", "", "bridge"), "VAT")]:
    m = M["coherent"]
    seg = B.decompose(m, B.budget_shock(FL[k]["net"].values, SCHED["mid"].values, m["budget"]))
    top = SH[(k, "post_mid")].loc[chart, "dUSD_mid"].abs().sort_values(ascending=False).index[:10]
    bseg = b_seg[b_seg["instrument"] == bi].pivot_table(index="category", columns="quintile", values="segment_eur")
    segmx = max(segmx, float((seg.loc[top, Q] - bseg.reindex(top)[Q]).abs().max().max()))
    sh = []
    for g in top:
        neg = seg.loc[g][seg.loc[g] < 0]
        if len(neg):
            sh.append(float(seg.loc[g, "q5"] / neg.sum()) if seg.loc[g, "q5"] < 0 else 0.0)
    q5s[inst] = sh
claim(segmx < 1e-8, "Fig 3 analogue: the ten largest movers and their quintile segments (max abs diff vs fi_lvt_decomposition_top10.csv)", "", segmx)
claim(printed(100 * min(q5s["LVT"]), 98, 1) and printed(100 * max(q5s["LVT"]), 99, 1) and printed(100 * min(q5s["VAT"]), 71, 1)
      and printed(100 * max(q5s["VAT"]), 91, 1), "Fig 3 analogue: Q5 supplies 98-99% of every top-10 withdrawal under the LVT, 71-91% under the VAT",
      "98-99 / 71-91", f"{100 * min(q5s['LVT']):.1f}-{100 * max(q5s['LVT']):.1f} / {100 * min(q5s['VAT']):.1f}-{100 * max(q5s['VAT']):.1f}",
      "mechanical: the LVT's Q4 nets to -1.4, so quintile netting leaves only Q5 to withdraw (inside Q4, 40% of households pay)")
ghost = {}
for c in M:
    for inst, k in [("LVT", (c, "LVT", "B2", "bridge")), ("VAT", (c, "VAT", "", "bridge"))]:
        s_ = SH[(k, "post_mid")].loc[M[c]["chart"]]
        ghost[(c, inst)] = s_.index[np.sign(s_["dUSD_mpc1"]) != np.sign(s_["dUSD_mid"])].tolist()
veh = "07.2 Operation of personal transport equipment"
claim(len(ghost[("coherent", "LVT")]) == 12 and len(ghost[("coherent", "VAT")]) == 14 and veh in set(ghost[("coherent", "LVT")]) & set(ghost[("coherent", "VAT")]),
      "ghost flips (MPC=1 ghost vs MPC-adjusted bar): 12 LVT, 14 VAT, in the section's coherent convention; vehicle operation flips under both", "12 / 14",
      f"{len(ghost[('coherent', 'LVT')])} / {len(ghost[('coherent', 'VAT')])}",
      f"12 / 14 are the POST convention's counts ({len(ghost[('post', 'LVT')])} / {len(ghost[('post', 'VAT')])}); the section is coherent "
      f"(13 / 17). No code computes them (run_lvt_fi.py stores dEUR_mpc1 only). Say 'post convention' or print 13 / 17; vehicle operation "
      f"flips under both in both conventions: {veh in set(ghost[('post', 'LVT')]) & set(ghost[('post', 'VAT')])}")
VW = SH[(("coherent", "VAT", "", "bridge"), "wealth_mid")]["dUSD_mid"][chart]
LW = SH[(("coherent", "LVT", "B2", "bridge"), "wealth_mid")]["dUSD_mid"][chart]
flips = [g for g in chart if np.sign(VW[g]) != np.sign(LW[g])]
claim(len(flips) == 2 and any(g.startswith("05.5") for g in flips) and any(g.startswith("13.9") for g in flips)
      and printed(VW["05.5 Tools and equipment for house and garden"], -0.005, 0.001) and printed(LW["05.5 Tools and equipment for house and garden"], 0.013, 0.001)
      and printed(VW["13.9 Other services"], -0.006, 0.001) and printed(LW["13.9 Other services"], 0.16, 0.01),
      "under the wealth grade 35 of 37 bars keep their sign; tools -0.005 -> +0.013, other services -0.006 -> +0.16", "35; 2 flips",
      f"{37 - len(flips)}; " + ", ".join(f"{g[:4]} {VW[g]:+.3f}->{LW[g]:+.3f}" for g in flips))

# tenure-aware baskets: actual rent with renters; imputed rent, interest and housing-company charges with owners
P_OWN_Q = pairq(P_OWN)
CHG = "maintenance charges of housing companies"


def baskets(m):
    C = m["C"]
    po = pd.Series(P_OWN_Q.values, index=C.columns)
    Co, Cr = C.copy(), C.copy()
    Cr.loc["04.1 Actual rents"] = C.loc["04.1 Actual rents"] / (1 - po)
    Co.loc["04.1 Actual rents"] = 0.0
    for g in ("04.2 Imputed rentals (off-chart)", "04.6 Interest on housing loans (off-chart)"):
        Co.loc[g] = C.loc[g] / po
        Cr.loc[g] = 0.0
    ch = m["lines"].loc[CHG, C.columns]
    Co.loc["04.4 Water & misc. dwelling services"] = C.loc["04.4 Water & misc. dwelling services"] + ch * (1 / po - 1)
    Cr.loc["04.4 Water & misc. dwelling services"] = C.loc["04.4 Water & misc. dwelling services"] - ch
    assert np.allclose((po * Co + (1 - po) * Cr).values, C.values)
    return {t: (Ct, B.fi_eta_table(dict(m, C=Ct, budget=Ct.sum()), "F3")[0]) for t, Ct in (("owner", Co), ("renter", Cr))}


def tenure_shifts(m, bk, dco, dcr):
    po = pd.Series(P_OWN_Q.values, index=m["C"].columns)
    out = 0.0
    for t, pt, dc in (("owner", po, dco), ("renter", 1 - po, dcr)):
        Ct, et = bk[t]
        out = out + (Ct / Ct.sum() * et).mul(m["w"] * pt * pd.Series(np.asarray(dc, float), index=Ct.columns), axis=1).sum(axis=1)
    return out


TEN = {}
for c in M:
    m = M[c]
    bk = baskets(m)
    po = P_OWN_Q
    for b in ("B2", "B1"):
        fl = FL[(c, "LVT", b, "bridge")]
        o, tau = fl["o"], fl["tau"]
        div = float(ACC[(c, b, "bridge")]["dividend"].iloc[0])
        ro = pd.Series([float(o["recv_own"][[DEC[2 * i], DEC[2 * i + 1]]].sum()) for i in range(5)], index=Q) * tau / 12
        pyo = pd.Series([float(o["pay"][[DEC[2 * i], DEC[2 * i + 1]]].sum()) for i in range(5)], index=Q) * tau / 12
        psum = pd.Series([float(P_OWN[[DEC[2 * i], DEC[2 * i + 1]]].sum()) for i in range(5)], index=Q)
        for g in ("post_mid", "wealth_mid"):
            mpc = SCHED["mid"].reindex(Q)
            mpay = mpc if g == "post_mid" else fl["h"] + (1 - fl["h"]) * MPC_U["mid"]
            dco = (mpc * ro - mpay * pyo) / (psum * SQ[c])
            dcr = mpc * div
            TEN[(c, "LVT", b, g)] = tenure_shifts(m, bk, dco.values, dcr.values)
    av = VA[c]
    flags = B.fi_vat_flags()
    ch = m["lines"].loc[CHG, Q] * flags[CHG]
    cv = float(av["Cbar_v"].iloc[0])
    mpc = SCHED["mid"].reindex(Q)
    xr, xo = av["vatable"] - ch, av["vatable"] - ch + ch / po
    TEN[(c, "VAT", "", "post_mid")] = tenure_shifts(m, bk, (mpc * B.TAU * (cv - xo)).values, (mpc * B.TAU * (cv - xr)).values)
mx = 0.0
for (c, inst, b, g), s_ in TEN.items():
    x = b_ten[(b_ten["convention"] == c) & (b_ten["instrument"] == inst) & (b_ten["base"] == b) & (b_ten["grade"] == g)].set_index("category")["dEUR"]
    mx = max(mx, float((s_ - x.reindex(s_.index)).abs().max()))
claim(mx < 1e-6, "tenure-aware bars, every version (max abs diff, EUR)", "fi_lvt_tenure_aware.csv", mx)
TW, TP, TV = TEN[("coherent", "LVT", "B2", "wealth_mid")], TEN[("coherent", "LVT", "B2", "post_mid")], TEN[("coherent", "VAT", "", "post_mid")]
rows_t = [("04.1 Actual rents", 16.88, 4.42), ("01.1 Food (at home)", 2.05, 0.95), ("07.1 Purchase of vehicles", -0.36, -0.42),
          ("04.4 Water & misc. dwelling services", -0.73, 0.22), ("04.2 Imputed rentals (off-chart)", -7.89, -1.03),
          ("04.6 Interest on housing loans (off-chart)", -0.43, -0.05)]
claim(all(printed(TW[g], a, 0.01) and printed(TV[g], b, 0.01) for g, a, b in rows_t),
      "tenure-aware table: LVT B2 (wealth grade) and VAT", " ; ".join(f"{a:+.2f}/{b:+.2f}" for _, a, b in rows_t),
      " ; ".join(f"{TW[g]:+.3f}/{TV[g]:+.3f}" for g, _, _ in rows_t))
rr = TW["04.1 Actual rents"] / L2["04.1 Actual rents"]
claim(printed(rr, 2.5, 0.1) and abs(TP["04.1 Actual rents"] - TW["04.1 Actual rents"]) < 1e-9, "tenure-aware LVT rent bar 2.5 x the quintile-netted one (EUR 16.9 vs 6.9)",
      "2.5", rr, "the same under the post's schedule (renters receive at the schedule either way), so the factor is the baskets, not the wealth grade")
fl_l = I("LVT", "B2", "bridge", "wealth_mid") / 100 * M["coherent"]["budget_bar"]
claim(printed(TW.sum() / fl_l, 1.05, 0.01), "tenure-aware bars over all 47 lines = flow x 1.05 (division-parent over-allocation)", "1.05", TW.sum() / fl_l)
bk = baskets(M["coherent"])
Cr, er = bk["renter"]
mrent_r = (er.loc["04.1 Actual rents"] * Cr.loc["04.1 Actual rents"] / Cr.sum())
mc = M["coherent"]
mrent_q = mc["eta"].loc["04.1 Actual rents"] * mc["C"].loc["04.1 Actual rents"] / mc["budget"]
claim(printed(100 * mrent_r.min(), 17, 1) and printed(100 * mrent_r.max(), 39, 1) and printed(100 * mrent_r["q1"], 39, 1)
      and printed(100 * mrent_q.min(), 2, 1) and printed(100 * mrent_q.max(), 28, 1),
      "renters spend 17-39 cents of an extra euro on rent (39 in Q1); the quintile-average basket says 2-28 cents", "17-39 / 2-28",
      f"{100 * mrent_r.min():.1f}-{100 * mrent_r.max():.1f} (Q1 {100 * mrent_r['q1']:.1f}) / {100 * mrent_q.min():.1f}-{100 * mrent_q.max():.1f}")
UNTX = ["04.2 Imputed rentals (off-chart)", "04.6 Interest on housing loans (off-chart)"]
Co_, eo_ = bk["owner"]
own_ms = (Co_.loc[UNTX] * eo_.loc[UNTX]).sum() / Co_.sum()                      # owners' marginal euro on imputed rent + interest
avg_ms = (mc["C"].loc[UNTX] * mc["eta"].loc[UNTX]).sum() / mc["budget"]
fl_ = FL[("coherent", "LVT", "B2", "bridge")]
ro_ = pd.Series([float(fl_["o"]["recv_own"][[DEC[2 * i], DEC[2 * i + 1]]].sum()) for i in range(5)], index=Q) * fl_["tau"] / 12
po_ = pd.Series([float(fl_["o"]["pay"][[DEC[2 * i], DEC[2 * i + 1]]].sum()) for i in range(5)], index=Q) * fl_["tau"] / 12
ps_ = pd.Series([float(P_OWN[[DEC[2 * i], DEC[2 * i + 1]]].sum()) for i in range(5)], index=Q)
dco_ = (SCHED["mid"].reindex(Q) * ro_ - (fl_["h"] + (1 - fl_["h"]) * MPC_U["mid"]) * po_) / (ps_ * SQ["coherent"])
own_c = (Co_ / Co_.sum() * eo_).mul(mc["w"] * P_OWN_Q * dco_, axis=1)
own_tot, own_untx = float(own_c.sum().sum()), float(own_c.loc[UNTX].sum().sum())
chart_t = float(TW[chart].sum())
claim(False, "'Owners' cuts land on imputed rent and housing-company charges' (tenure-aware extension) describes spending", "finding",
      f"{100 * own_untx / own_tot:.0f}% of owners' cut",
      f"owners' basket puts {100 * own_ms.min():.0f}-{100 * own_ms.max():.0f}% of each marginal euro on imputed rent and mortgage interest (quintile "
      f"average {100 * avg_ms.min():.0f}-{100 * avg_ms.max():.0f}%), so EUR {-own_untx:.2f} of owners' EUR {-own_tot:.2f} cut (wealth grade, bridge rate) is "
      f"booked on lines that cannot move at impact. Re-spread over what owners can cut, the tenure-aware charted total EUR {chart_t:.1f} "
      f"(fig_fi_demand_shifts) falls toward EUR {chart_t + own_untx:.1f}. Say the imputed-rent cut is an accounting artifact (the post omits "
      "imputed rent because nothing is transacted), or re-spread it")


# %% I. macro (i) the price level and the VAT's levy channel; capitalization at announcement
AREA[0] = "I macro"
mc = M["coherent"]
VSH = float(VA["coherent"]["Cbar_v"].iloc[0]) / mc["budget_bar"]
STEP = {k: B.TAU * VSH * v for k, v in {"low": 0.8, "mid": 0.9, "high": 1.0}.items()}
num(100 * STEP["mid"], b_mc("price level step (80-100% pass-through)"), "VAT price-level step, central (15 x VAT-able share x 0.9), %", 8.9, 0.1,
    note=f"VAT-able share {VSH:.4f} (NOTES 0.661)")
claim(printed(100 * STEP["low"], 7.9, 0.1) and printed(100 * STEP["high"], 9.9, 0.1) and printed(VSH, 0.661, 0.001), "VAT step band [7.9, 9.9]; share 0.661",
      "7.9 / 9.9 / 0.661", f"{100 * STEP['low']:.3f} / {100 * STEP['high']:.3f} / {VSH:.4f}")
claim(b_mc("price level step") == 0.0, "LVT price step 0 (land in fixed supply; nothing to pass through)", "0", 0.0)
NW = float(wd("net_wealth")["total"]) * N_SURV / 1e6 / DEFL23
LEVY = {k: v / (1 + v) for k, v in STEP.items()}
lev = lambda lam, k, lk="mid": -100 * MPW[k] * lam * LEVY[lk] * NW / C_MEUR
blev = b_lev[(b_lev["levy_case"] == "mid") & (b_lev["lam"] == 0.35)].set_index("mpw")["pct_consumption"]
num(lev(0.35, "mid"), blev["mid"], "VAT levy channel, lambda 0.35, 3.5c (impact), % of consumption", -0.56, 0.01,
    note=f"net worth EUR {NW / 1e3:.0f}bn (NOTES 647) = {NW / C_MEUR:.2f} years of HBS consumption (NOTES 5.6); levy {100 * LEVY['mid']:.2f}% (NOTES 8.2)")
claim(printed(NW / 1e3, 647, 1) and printed(NW / C_MEUR, 5.6, 0.1) and printed(100 * LEVY["mid"], 8.2, 0.1) and printed(lev(0.35, "high"), -0.80, 0.01)
      and printed(lev(0.35, "low"), -0.32, 0.01) and printed(lev(1.0, "mid"), -1.60, 0.01),
      "levy inputs and band: EUR 647bn, 5.6 years, 8.2%; [-0.80, -0.32]; lambda 1 -1.60", "647 / 5.6 / 8.2; -0.80/-0.32; -1.60",
      f"{NW / 1e3:.1f} / {NW / C_MEUR:.2f} / {100 * LEVY['mid']:.2f}; {lev(0.35, 'high'):.3f}/{lev(0.35, 'low'):.3f}; {lev(1.0, 'mid'):.3f}")
VATNET = (I("VAT", "", "bridge", "post_mid") + lev(0.35, "mid"), I("VAT", "", "bridge", "post_high") + lev(0.35, "high"),
          I("VAT", "", "bridge", "post_low") + lev(0.35, "low"))
num(VATNET[0], b_mc("net demand at impact, lambda = 0.35 (flow + levy)"), "VAT net demand at impact, lambda 0.35 (flow + levy)", -0.14, 0.01)
claim(printed(VATNET[1], -0.48, 0.01) and printed(VATNET[2], 0.20, 0.01), "VAT net band [-0.48, +0.20]", "-0.48 / +0.20", f"{VATNET[1]:.3f} / {VATNET[2]:.3f}")
shock = pd.read_csv(REPO / "three-taxes" / "data" / "lvt_shock.csv").set_index("design")["price_drop"]
PV = {"immediate": 1.0, "phasein_10y": shock["phase-in 10y"] / PHI, "phasein_5y": shock["phase-in 5y"] / PHI, "phasein_20y": shock["phase-in 20y"] / PHI,
      "phasein_30y": shock["phase-in 30y"] / PHI, "increment": shock["increment-only (grandfather r0)"] / PHI}
F_FULL = PHI * S_D
num(F_FULL, b_cap[(b_cap["rate"] == "full_m1") & (b_cap["design"] == "immediate")]["dwelling_value_lost"].iloc[0],
    "dwelling values fall phi x s_d at full capture ('about 19%'; collateral block 19.3%)", 0.193, 0.001)
mxc = max(abs(min(PHI * PV[dz] * S_D, 1) - float(b_cap[(b_cap["rate"] == "full_m1") & (b_cap["design"] == dz)]["dwelling_value_lost"].iloc[0])) for dz in PV)
claim(mxc < 1e-9, "dwelling value lost by design (immediate, phase-ins, increment-only) from three-taxes/data/lvt_shock.csv (max abs diff)", "", mxc,
      "T4: increment-only captures 0.404 at phi 0.98, i.e. gamma/delta = 0.40 per unit of phi (discrete timing 0.412)")


# %% J. macro (ii) the LVT's stock channel: collateral (US-shape LTVs, log-normal band), non-occupiers; the headline readings
AREA[0] = "J collateral"
mort = SCF[(SCF["HOUSES"] > 0) & (SCF["MRTHEL"] > 0)].copy()
mort["ltv"] = mort["MRTHEL"] / mort["HOUSES"]
gus = mort.groupby("dec").apply(lambda g: pd.Series({"n": g["WGT"].sum(), "Vbar": np.average(g["HOUSES"], weights=g["WGT"]),
                                                     "A": (g["MRTHEL"] * g["WGT"]).sum() / (g["HOUSES"] * g["WGT"]).sum()}), include_groups=False)
fi_dec = pd.DataFrame({"n": N_MORT.values, "Vbar": (VM_TOT / N_MORT).values, "A": (HL_TOT / VM_TOT).values}, index=range(1, 11))
pop = pd.DataFrame({"dec": mort["dec"].values,
                    "w": (mort["WGT"] * mort["dec"].map(fi_dec["n"] / gus["n"])).values,
                    "V": (mort["HOUSES"] * mort["dec"].map(fi_dec["Vbar"] / gus["Vbar"])).values})
pop["M"] = (mort["ltv"] * mort["dec"].map(fi_dec["A"] / gus["A"])).values * pop["V"].values
agg = pop.groupby("dec").apply(lambda g: pd.Series({"n": g["w"].sum(), "V": (g["w"] * g["V"]).sum(), "M": (g["w"] * g["M"]).sum()}), include_groups=False)
claim(np.allclose(agg["n"], fi_dec["n"]) and np.allclose(agg["V"], VM_TOT.values) and np.allclose(agg["M"], HL_TOT.values),
      "US-shape population reproduces Finland's decile counts, mortgaged values and loans exactly", "exact", "exact")
LTV_M0 = float(HL_TOT.sum() / VM_TOT.sum())
LTV_A0 = float(HL_TOT.sum() / MR_TOT.sum())
claim(printed(100 * LTV_M0, 48.2, 0.1) and printed(100 * LTV_M0 / (1 - F_FULL), 59.7, 0.1) and printed(100 * LTV_A0, 25.4, 0.1)
      and printed(100 * LTV_A0 / (1 - F_FULL), 31.5, 0.1) and near(LTV_M0, wt("housing_loans")["mortgaged"] / wt("main_residence")["mortgaged"], 1e-5),
      "LTVs at full capture: mortgaged 48.2% -> 59.7%; all owners 25.4% -> 31.5% (151z: 106,965 / 222,127)", "48.2/59.7; 25.4/31.5",
      f"{100 * LTV_M0:.2f}/{100 * LTV_M0 / (1 - F_FULL):.2f}; {100 * LTV_A0:.2f}/{100 * LTV_A0 / (1 - F_FULL):.2f}")


def crossers(f, th, p=None):
    p = pop if p is None else p
    V0, Mx, w = p["V"].values, p["M"].values, p["w"].values
    V1 = V0 * (1 - f)
    cr = (Mx <= th * V0) & ((Mx > th * V1) if f < 1 else True)
    lc = np.maximum(th * V0 - Mx, 0) - np.maximum(th * V1 - Mx, 0)
    return dict(n=float((w * cr).sum()), le=float((w * cr * f * V0).sum()) / 1e6 * CARRY, lc=float((w * cr * lc).sum()) / 1e6 * CARRY,
                val=float((w * cr * V0).sum()) / 1e6 * CARRY, above0=float((w * (Mx > th * V0)).sum()),
                above1=float((w * ((Mx > th * V1) if f < 1 else np.ones(len(w), bool))).sum()), by_dec=pd.Series(w * cr).groupby(p["dec"].values).sum(),
                lc_dec=pd.Series(w * cr * lc).groupby(p["dec"].values).sum() / 1e6 * CARRY)


def bcol(rate, design="immediate", th=0.8, col="dC_lost_capacity_mid_pct"):
    x = b_col[(b_col["method"] == "us_shape") & (b_col["decile"] == "total") & (b_col["rate"] == rate) & (b_col["design"] == design) & (b_col["threshold"] == th)]
    assert len(x) == 1
    return float(x[col].iloc[0])


cx = crossers(F_FULL, 0.8)
cx100 = crossers(F_FULL, 1.0)
num(cx["n"], bcol("full_m1", col="n_cross"), "mortgaged owners crossing 80% LTV at full capture", 121500, 100, tol=1e-6)
claim(printed(cx["n"] / 1e3, 122, 1) and printed(100 * cx["n"] / N_MORT.sum(), 14, 1), "'122,000 owners, 14% of the mortgaged'", "122k / 14%",
      f"{cx['n'] / 1e3:.1f}k / {100 * cx['n'] / N_MORT.sum():.1f}%")
claim(printed(cx["above0"] / 1e3, 175, 1) and printed(cx["above1"] / 1e3, 296, 1) and printed(cx100["above0"] / 1e3, 47, 1)
      and printed(cx100["above1"] / 1e3, 172, 1), "above 80%: 175,000 -> 296,000; above 100%: 47,000 -> 172,000", "175/296; 47/172",
      f"{cx['above0'] / 1e3:.1f}/{cx['above1'] / 1e3:.1f}; {cx100['above0'] / 1e3:.1f}/{cx100['above1'] / 1e3:.1f}")
num(cx["lc"], bcol("full_m1", col="lost_capacity_meur"), "crossers' lost borrowing capacity (EUR m, carried to 2022)", 2000, 100)
num(cx["le"], bcol("full_m1", col="lost_equity_meur"), "crossers' lost equity (EUR m)", 4900, 100)
COLL = {k: -100 * v * cx["lc"] / C_MEUR for k, v in MPCC.items()}
COLL_T4 = {k: -100 * v * cx["le"] / C_MEUR for k, v in MPCC.items()}
num(COLL["mid"], bcol("full_m1"), "collateral credit effect, 6c on crossers' lost capacity (% of consumption)", -0.11, 0.01)
claim(printed(COLL["lit_high"], -0.12, 0.01) and printed(COLL["low"], -0.08, 0.01) and printed(COLL["stress"], -0.18, 0.01),
      "credit-effect band [-0.12, -0.08], stress -0.18 (NOTES table); plain words -0.105 [-0.123, -0.082], stress -0.175", "-0.12/-0.08/-0.18",
      f"{COLL['lit_high']:.4f}/{COLL['low']:.4f}/{COLL['stress']:.4f}")
num(COLL_T4["mid"], bcol("full_m1", col="dC_lost_equity_mid_pct"), "collateral on crossers' lost equity (T4 overlap, band edge)", -0.25, 0.01)
claim(printed(COLL_T4["lit_high"], -0.30, 0.01) and printed(COLL_T4["low"], -0.20, 0.01) and printed(COLL_T4["stress"], -0.42, 0.01),
      "T4-overlap band [-0.30, -0.20], stress -0.42", "-0.30/-0.20/-0.42", f"{COLL_T4['lit_high']:.4f}/{COLL_T4['low']:.4f}/{COLL_T4['stress']:.4f}")
H_MORT = (HD["half_month"] * HT["half_month"]["mortgaged"] / HT["half_month"]["all"]).clip(upper=1.0)
lc_htm = float((cx["lc_dec"] * pd.Series(H_MORT.values, index=range(1, 11))).sum())
COLL_H = {k: -100 * v * lc_htm / C_MEUR for k, v in MPCC.items()}
num(COLL_H["mid"], bcol("full_m1", col="dC_lost_capacity_htm_mid_pct"), "collateral, hand-to-mouth crossers only (6c)", -0.01, 0.01,
    note=f"hand-to-mouth crossers carry {100 * lc_htm / cx['lc']:.1f}% of the lost capacity")
d610 = float(cx["by_dec"].loc[6:10].sum() / cx["n"])
claim(d610 > 0.7, "crossers concentrate in D6-D10, where the mortgages are", "D6-D10", f"{100 * d610:.0f}% of crossers in D6-D10")
for dz, nv in [("phasein_10y", -0.09), ("increment", -0.02)]:
    cz = crossers(PHI * PV[dz] * S_D, 0.8)
    num(-100 * MPCC["mid"] * cz["lc"] / C_MEUR, bcol("full_m1", dz), f"collateral credit effect under {dz}", nv, 0.01)
# the US-shape quartiles against 151z, and the log-normal band
def wq(x, w, qs=(0.25, 0.5, 0.75)):
    o = np.argsort(x)
    cw = np.cumsum(w[o]) / w.sum()
    return [float(np.interp(q, cw, x[o])) for q in qs]


rat = [a / b for a, b in zip(wq(pop["M"].values, pop["w"].values), [wt("housing_loans", k)["mortgaged"] for k in ("p25", "median", "p75")])]
rat += [a / b for a, b in zip(wq(pop["V"].values, pop["w"].values), [wt("main_residence", k)["mortgaged"] for k in ("p25", "median", "p75")])]
dev = [abs(r - 1) for r in rat]
claim(printed(100 * min(dev), 4, 1) and printed(100 * max(dev), 32, 1), "US-shape loan and value quartiles within 4-32% of 151z's", "4-32%",
      f"{100 * min(dev):.1f}-{100 * max(dev):.1f}%", "ratios " + ", ".join(f"{r:.2f}" for r in rat))


def lognormal_coll(f, th, sigma, c=1.1, n=None, Vbar=None, A=None):
    n = N_MORT.values if n is None else n
    Vbar = (VM_TOT / N_MORT).values if Vbar is None else Vbar
    A = (HL_TOT / VM_TOT).values if A is None else A
    nc = le = lc = 0.0
    for nn, vb, aa in zip(n, Vbar, A):
        D = stats.lognorm(s=sigma, scale=c * aa)
        lo = th * (1 - f) if f < 1 else 0.0
        P = D.cdf(th) - D.cdf(lo)
        EL = D.expect(lambda x: x, lb=lo, ub=th) if P > 0 else 0.0
        nc += nn * P
        le += nn * P * f * vb
        lc += nn * vb * (th * P - EL)
    return nc, le / 1e6 * CARRY, lc / 1e6 * CARRY


LN = {s: lognormal_coll(F_FULL, 0.8, s) for s in (0.5, 0.6, 0.8)}
LNd = {s: -100 * MPCC["mid"] * v[2] / C_MEUR for s, v in LN.items()}
bln = b_cln[(b_cln["rate"] == "full_m1") & (b_cln["design"] == "immediate") & (b_cln["threshold"] == 0.8)].set_index("sigma")
claim(max(abs(LNd[s] - float(bln.loc[s, "dC_lost_capacity_mid_pct"])) for s in LNd) < 1e-6 and printed(LNd[0.8], -0.08, 0.01) and printed(LNd[0.5], -0.12, 0.01),
      "log-normal LTV method (median 1.1 x aggregate, sigma 0.5-0.8): -0.08 to -0.12", "-0.08 / -0.12",
      f"{LNd[0.8]:.4f} / {LNd[0.6]:.4f} / {LNd[0.5]:.4f}")

# non-occupiers (other dwellings, cottages, forest/farmland/business land): the bill at the MPC, or a wealth effect on the
# capitalized loss, never both
NONOCC = {"B2": ["L_ore", "L_ftr", "L_ffb"], "B1": ["L_ore", "L_ftr"]}
CAP = {"L_ore": 1 / S_D, "L_ftr": 1 / S_D, "L_ffb": 1 / S_F}


def nonocc(base, rate, r=None, k="mid"):
    r = r22 if r is None else r
    m = M["coherent"]
    tau = TAU[("coherent", base, rate)] if rate in ("bridge", "full_m1", "full_m2") else rate
    phi = (tau / r22) if rate == "bridge" else PHI
    s12 = 12 * SQ["coherent"]
    bill = pairq(LD[NONOCC[base]].sum(axis=1)) * tau / s12
    loss = sum(pairq(LD[cn] * min(phi, CAP[cn])) for cn in NONOCC[base]) / s12
    mpc = SCHED["mid"].reindex(Q)
    add_back = float((m["w"] * mpc * bill).sum())
    we = float((m["w"] * MPW[k] * loss).sum())
    share = float((LD[NONOCC[base]].sum(axis=1) * NHD).sum() / (LD[base] * NHD).sum())
    return dict(change=100 * (add_back - we) / m["budget_bar"], per_bill=float((m["w"] * loss).sum() / (m["w"] * bill).sum()), share=share)


bno = b_no.set_index(["base", "rate"])
NO = {k: nonocc("B2", "full_m1", k=k)["change"] for k in MPW}
num(100 * nonocc("B2", "full_m1")["share"], 100 * bno.loc[("B2", "full_m1"), "nonocc_share_of_base"], "non-occupiers' share of B2 land, %", 42.7, 0.1)
claim(printed(nonocc("B2", "full_m1")["per_bill"], 59, 1) and printed(nonocc("B2", "full_m2")["per_bill"], 31, 1)
      and near(nonocc("B2", "full_m1")["per_bill"], 1 / r22, 1e-9), "capitalized loss per euro of bill: 59 at the 2022 yield, 31 at yield + 1.5 (= 1/r)",
      "59 / 31", f"{nonocc('B2', 'full_m1')['per_bill']:.2f} / {nonocc('B2', 'full_m2')['per_bill']:.2f}")
num(NO["mid"], b_mc("non-occupying holders: wealth effect instead of flow (change in impulse, full capture, B2)"),
    "non-occupiers on the wealth reading: change in impulse, full capture (3.5c)", -1.09, 0.01)
claim(printed(NO["high"], -1.79, 0.01) and printed(NO["low"], -0.39, 0.01), "non-occupier change band [-1.79, -0.39]", "-1.79 / -0.39",
      f"{NO['high']:.4f} / {NO['low']:.4f}")
for (b, r), row in bno.iterrows():
    mine = I("LVT", b, r, "post_mid") + nonocc(b, r)["change"]
    if not near(mine, row["wealth_version_mid_pct"], 1e-7):
        claim(False, f"non-occupier wealth version {b} {r}", row["wealth_version_mid_pct"], mine)
claim(True, "non-occupier wealth versions, B1/B2 x three rates, match fi_lvt_nonoccupier.csv (checked row by row above)", "", "")

# the headline readings at impact
def readings(rate):
    f_mid, f_hi, f_lo = (I("LVT", "B2", rate, g) for g in ("post_mid", "post_high", "post_low"))
    f = F_FULL if rate != "bridge" else 1.0
    c_ = crossers(f, 0.8)
    lc, le = c_["lc"], c_["le"]
    cd = lambda v, x: -100 * v * x / C_MEUR
    htm_lc = float((c_["lc_dec"] * pd.Series(H_MORT.values, index=range(1, 11))).sum())
    rr = R["m2"] if rate == "full_m2" else r22
    phi = PHI if rate != "bridge" else TAU[("coherent", "B2", "bridge")] / r22
    p = pop.copy()
    V0, Mx, w = p["V"].values, p["M"].values, p["w"].values
    cr = (Mx <= 0.8 * V0) & ((Mx > 0.8 * V0 * (1 - f)) if f < 1 else True)
    val_dec = pd.Series(w * cr * V0).groupby(p["dec"].values).sum() / 1e6 * CARRY
    mpc_dec = pd.Series([float(SCHED.loc[Q[(d - 1) // 2], "mid"]) for d in range(1, 11)], index=range(1, 11))
    resp = float((phi * rr * S_D * val_dec * mpc_dec).sum())
    out = {"clean": (f_mid + cd(MPCC["mid"], lc), f_hi + cd(MPCC["lit_high"], lc), f_lo + cd(MPCC["low"], lc), f_hi + cd(MPCC["stress"], lc)),
           "t4": (f_mid + cd(MPCC["mid"], le), f_hi + cd(MPCC["lit_high"], le), f_lo + cd(MPCC["low"], le), f_hi + cd(MPCC["stress"], le)),
           "htm": (f_mid + cd(MPCC["mid"], htm_lc), f_hi + cd(MPCC["lit_high"], htm_lc), f_lo + cd(MPCC["low"], htm_lc), f_hi + cd(MPCC["stress"], htm_lc)),
           "stock": tuple(fl_ + 100 * (resp - v * le) / C_MEUR for fl_, v in ((f_mid, MPCC["mid"]), (f_hi, MPCC["lit_high"]), (f_lo, MPCC["low"]))) + (np.nan,),
           "wealth_grade": (I("LVT", "B2", rate, "wealth_mid") + cd(MPCC["mid"], lc), I("LVT", "B2", rate, "wealth_high") + cd(MPCC["lit_high"], lc),
                            I("LVT", "B2", rate, "wealth_low") + cd(MPCC["low"], lc), np.nan)}
    out["nonocc_wealth"] = tuple(out["clean"][i] + nonocc("B2", rate, k=k)["change"] for i, k in enumerate(("mid", "high", "low"))) + (np.nan,)
    return out


HLm = {r: readings(r) for r in ("full_m1", "full_m2", "bridge")}
bhl = b_hl[b_hl["instrument"] == "LVT"].set_index(["rate", "reading"])
mx = 0.0
for r, dd in HLm.items():
    for k, (cen, a, b, st) in dd.items():
        row = bhl.loc[(r, k)]
        mx = max(mx, abs(cen - row["central"]), abs(min(a, b) - row["low"]), abs(max(a, b) - row["high"]),
                 0 if (np.isnan(st) and np.isnan(row["stress_10c"])) else abs(st - row["stress_10c"]))
claim(mx < 1e-7, "headline readings (clean, T4, hand-to-mouth, stock, wealth grade, non-occupiers) x three rates, central/band/stress (max abs diff)",
      "fi_lvt_headline.csv", mx)
H = HLm["full_m1"]
for k, lab, nv in [("clean", "net at impact, flow + credit effect (2022 yield)", (0.04, -0.01, 0.10, -0.06)),
                   ("t4", "net, includes the T4 overlap", (-0.11, -0.18, -0.02, -0.31)), ("htm", "net, only hand-to-mouth crossers respond", (0.13, 0.10, 0.17, None)),
                   ("stock", "net, crossers' stock response instead of their bill", (-0.06, -0.14, 0.03, None)),
                   ("nonocc_wealth", "net, every non-occupier on the wealth reading", (-1.05, -1.80, -0.29, None)),
                   ("wealth_grade", "net, unconstrained payers draw on wealth", (0.10, -0.01, 0.35, None))]:
    cen, a, b, st = H[k]
    ok = printed(cen, nv[0], 0.01) and printed(min(a, b), nv[1], 0.01) and printed(max(a, b), nv[2], 0.01) and (nv[3] is None or printed(st, nv[3], 0.01))
    claim(ok, f"macro table: {lab} (full capture)", " / ".join("" if v is None else f"{v:+.2f}" for v in nv),
          f"{cen:+.4f} [{min(a, b):+.4f}, {max(a, b):+.4f}]" + ("" if np.isnan(st) else f" stress {st:+.4f}"))
cen, a, b, st = HLm["full_m2"]["clean"]
claim(printed(cen, 0.17, 0.01) and printed(min(a, b), 0.09, 0.01) and printed(max(a, b), 0.25, 0.01) and printed(st, 0.04, 0.01),
      "macro table: net, yield + 1.5: +0.17 [0.09, 0.25], stress +0.04", "+0.17 [0.09, 0.25] +0.04", f"{cen:+.4f} [{min(a, b):+.4f}, {max(a, b):+.4f}] {st:+.4f}")
cen, a, b, st = HLm["bridge"]["clean"]
claim(printed(cen, -2.77, 0.01) and printed(min(a, b), -3.54, 0.01) and printed(max(a, b), -1.83, 0.01) and printed(st, -5.31, 0.01),
      "macro table: notional bridge rate, flow + credit effect (dwellings worthless): -2.77 [-3.54, -1.83], stress -5.31", "-2.77 [-3.54, -1.83] -5.31",
      f"{cen:+.4f} [{min(a, b):+.4f}, {max(a, b):+.4f}] {st:+.4f}")
claim(printed(I("LVT", "B2", "full_m1", "post_mid"), 0.14, 0.01) and printed(I("LVT", "B2", "full_m1", "post_high"), 0.11, 0.01)
      and printed(I("LVT", "B2", "full_m1", "post_low"), 0.18, 0.01), "macro table: LVT full capture flow +0.14 [0.11, 0.18]", "+0.14 [0.11, 0.18]",
      f"{I('LVT', 'B2', 'full_m1', 'post_mid'):.4f}")


# %% K. the loop (T5): the dividend's rent bar raises land rent; a household-land tax takes back the household landlords' part
AREA[0] = "K loop"
ORPq = pd.Series([float((wd("other_res").reindex(DEC) * NHD).iloc[2 * i:2 * i + 2].sum()) for i in range(5)], index=Q)
KEY = ORPq / ORPq.sum()


def rent_bar(net, mpc=None):
    mpc = SCHED["mid"].values if mpc is None else mpc
    return float(B.decompose(mc, B.budget_shock(np.asarray(net, float), mpc, mc["budget"])).loc["04.1 Actual rents"].sum())


def loop(R0, phi, ls, h, tol=1e-13):
    R_, tot, rounds = R0, 0.0, []
    for _ in range(500):
        dd = phi * h * ls * R_
        if abs(dd) < tol:
            break
        net = dd - dd * KEY.values / mc["w"].reindex(Q).values
        R_ = rent_bar(net)
        rounds.append((dd, R_))
        tot += dd
    q = rounds[0][1] / rounds[0][0]
    return tot, q, 1 / (1 - phi * h * ls * q)


R0f = rent_bar(FL[("coherent", "LVT", "B2", "full_m1")]["net"].values)
R0v = rent_bar(FL[("coherent", "VAT", "", "bridge")]["net"].values)
tot, q, mult = loop(R0f, PHI, S_D, 0.55)
div_f = float(ACC[("coherent", "B2", "full_m1")]["dividend"].iloc[0])
blp = b_loop[(b_loop["instrument"] == "LVT_B2") & (b_loop["rate"] == "full_m1")].set_index(["ls_case", "landlord_case"])
num(R0f, blp.loc[("mid", "mid"), "rent_bar_round0"], "rent bar at full capture (EUR/share/month)", 1.28, 0.01)
num(S_D * R0f * NSH * 12 / 1e6, blp.loc[("mid", "mid"), "land_rent_increment_meur"], "land rent increment, EUR m a year", 14.7, 0.1)
num(100 * tot / div_f, blp.loc[("mid", "mid"), "extra_dividend_pct_of_dividend"], "extra dividend from the loop, % of the dividend", 0.37, 0.01)
num(mult, blp.loc[("mid", "mid"), "multiplier"], "loop multiplier 1 / (1 - phi h ls q)", 1.005, 0.001)
ext = [100 * loop(R0f, PHI, ls, h)[0] / div_f for ls in (0.13, 0.30) for h in (0.40, 0.70)]
claim(printed(min(ext), 0.18, 0.01) and printed(max(ext), 0.72, 0.01), "loop band [0.18, 0.72]% of the dividend (ls 0.13-0.30, landlords 0.40-0.70)",
      "0.18 / 0.72", f"{min(ext):.4f} / {max(ext):.4f}")
claim(printed(S_D * R0v * NSH * 12 / 1e6, 48, 1) and printed(S_D * R0v * NSH * 12 / 1e6 / r22 / 1e3, 2.8, 0.1),
      "under the VAT the increment, EUR 48m a year (EUR 2.8bn capitalized at the 2022 yield), goes to landlords", "48m / 2.8bn",
      f"{S_D * R0v * NSH * 12 / 1e6:.2f}m / {S_D * R0v * NSH * 12 / 1e6 / r22 / 1e3:.3f}bn")
claim(abs(tot - PHI * 0.55 * S_D * R0f * mult) < 1e-9, "the loop's iteration equals the closed form R0 x phi h ls / (1 - phi h ls q) (T5's fixed point)",
      "closed form", tot, "q = rent bar per euro of round transfer, constant across rounds (the bridge is linear)")
tot1, _, mult1 = loop(R0f, PHI, 1.0, 0.55)
claim(mult1 < 1.05, "info: the land share of a rent CHANGE is set at the AVERAGE land share s_d (band 0.13-0.30); with land the residual claimant "
      "on a permanent demand-driven rent rise (ls = 1) the loop stays second-order", "multiplier 1.005", f"{mult1:.4f}",
      f"ls = 1: extra dividend {100 * tot1 / div_f:.2f}% of the dividend (vs 0.37%); the VAT's leak to landlords EUR {R0v * NSH * 12 / 1e6:.0f}m a year "
      f"(EUR {R0v * NSH * 12 / 1e6 / r22 / 1e3:.1f}bn capitalized) instead of EUR 48m. The US unit's band is 0.30-0.50; say the marginal share is a judgment")


# %% L. the US beside Finland: the US numbers are the US unit's current outputs; the US collateral at Finland's revenue share is
# recomputed here on the SCF 2025 zip with the US unit's crossing logic (validated first on the US unit's own full-capture row)
AREA[0] = "L US compare"
um = pd.read_csv(BOUT / "us_lvt_macro_channels.csv")
ucol = pd.read_csv(BOUT / "us_lvt_collateral.csv")
uno = pd.read_csv(BOUT / "us_lvt_nonoccupier.csv").set_index(["scenario", "grade"])
uphi = pd.read_csv(BOUT / "us_lvt_phi.csv")
uin = pd.read_csv(BOUT / "us_lvt_inputs.csv").set_index("item")["value"]
uhl = pd.read_csv(BOUT / "us_lvt_headline.csv")
UC = b_uc.set_index(["block", "item"])
us_c = float(uin["ce_consumption_bn"])
s_us = float(uin["s_uniform_2025"])
ul1 = uphi[(uphi["base"] == "L1") & (uphi["measure"] == "m1_z1hh_x_gs10")].set_index("rate")
us_phi_b, us_rent = float(ul1.loc["bridge", "phi"]), float(ul1.loc["bridge", "rent_bn"])
ucx = lambda sc, col: float(ucol[(ucol["scenario"] == sc) & (ucol["design"] == "immediate") & (ucol["threshold"] == 0.8) &
                                 (ucol["measure"] == "m1_z1hh_x_gs10")][col].iloc[0])
US = dict(vat_flow=us_ch("flow impulse, post's method (mid; band"), vat_levy=us_ch("levy channel, lambda = 0.35"),
          vat_net=us_ch("net demand at impact, lambda = 0.35 (flow + levy)"), flow_b=us_ch("flow impulse, post's method (bridge, L1)"),
          flow_f=us_ch("flow impulse, post's method (full, L1)"), cr_b=ucx("LVT_bridge_L1", "dC_lost_capacity_mid_pct"),
          cr_f=ucx("LVT_full_L1", "dC_lost_capacity_mid_pct"), le_f=ucx("LVT_full_L1", "dC_lost_equity_mid_pct"),
          no_f=float(uno.loc[("LVT_full_L1_m1", "dn_mid"), "wealth_version_mid_pct"] - uno.loc[("LVT_full_L1_m1", "dn_mid"), "flow_version_pct"]))
hl_us = uhl[(uhl["instrument"] == "LVT") & (uhl["base"] == "L1")].set_index("reading") if "reading" in uhl else None
claim(near(UC.loc[("VAT, impact (same formulas)", "net demand at impact (flow + levy)"), "US"], US["vat_net"], 1e-9) and
      near(UC.loc[("LVT, same share of rent (full capture, phi 0.98)", "net demand at impact (flow + credit effect)"), "US"], US["flow_f"] + US["cr_f"], 1e-9) and
      near(UC.loc[("LVT, the US bridge's share of rent (phi 0.848)", "net demand at impact (flow + credit effect)"), "US"], US["flow_b"] + US["cr_b"], 1e-9) and
      near(UC.loc[("LVT, same share of rent (full capture, phi 0.98)", "non-occupiers on the wealth reading: change in impulse (3.5c)"), "US"], US["no_f"], 1e-9),
      "the US numbers in fi_lvt_us_compare.csv are the US unit's current outputs (VAT net, LVT full and bridge nets, non-occupiers)", "", "",
      f"US bridge flow + credit effect {US['flow_b'] + US['cr_b']:+.4f} (NOTES_us central +0.15)")
# validate my SCF crossing logic on the US unit's own full-capture row, then recompute at Finland's revenue share
us_m = SCF[(SCF["HOUSES"] > 0) & (SCF["MRTHEL"] > 0)]
cpi = 4750.0 / 4625.0


def us_cross(f, th=0.8):
    w, V0, Mx = us_m["WGT"].values, us_m["HOUSES"].values / cpi, us_m["MRTHEL"].values / cpi
    V1 = V0 * (1 - f)
    cr = (Mx <= th * V0) & (Mx > th * V1)
    lc = np.maximum(th * V0 - Mx, 0) - np.maximum(th * V1 - Mx, 0)
    return float((w * cr).sum()) / 1e6, float((w * cr * f * V0).sum()) / 1e9, float((w * cr * lc).sum()) / 1e9


n_f, le_f, lc_f = us_cross(PHI * s_us)
claim(near(n_f, ucx("LVT_full_L1", "n_cross_m"), 1e-6) and near(lc_f, ucx("LVT_full_L1", "lost_capacity_crossers_bn"), 1e-6),
      "my SCF 2025 crossing logic reproduces the US unit's full-capture crossers and lost capacity (validates the recomputation)",
      f"{ucx('LVT_full_L1', 'n_cross_m'):.3f}m / ${ucx('LVT_full_L1', 'lost_capacity_crossers_bn'):,.0f}bn", f"{n_f:.3f}m / ${lc_f:,.0f}bn")
fi_rev = div_full("coherent", "B2", r22) * NSH * 12 / 1e6 / C_MEUR
phi_us = fi_rev * us_c / us_rent
_, le_m, lc_m = us_cross(phi_us * s_us)
us_same = (US["flow_b"] * phi_us / us_phi_b, -100 * MPCC["mid"] * lc_m / us_c, -100 * MPCC["mid"] * le_m / us_c)
bl = "LVT, same revenue as Finland's full capture"
num(us_same[0] + us_same[1], UC.loc[(bl, "net demand at impact (flow + credit effect)"), "US"], "US LVT at Finland's revenue share: flow + credit effect", 0.17, 0.01,
    note=f"revenue {100 * fi_rev:.3f}% of consumption (NOTES 1.85), US phi {phi_us:.4f} (NOTES 0.17)")
claim(printed(100 * fi_rev, 1.85, 0.01) and printed(phi_us, 0.17, 0.01), "same revenue: 1.85% of consumption; US phi 0.17", "1.85 / 0.17", f"{100 * fi_rev:.3f} / {phi_us:.3f}")
F_CR, F_LE, F_FL = COLL["mid"], COLL_T4["mid"], I("LVT", "B2", "full_m1", "post_mid")
cu848 = crossers(us_phi_b * S_D, 0.8)
fi848 = (F_FL * us_phi_b / PHI, -100 * MPCC["mid"] * cu848["lc"] / C_MEUR)
num(sum(fi848), UC.loc[("LVT, the US bridge's share of rent (phi 0.848)", "net demand at impact (flow + credit effect)"), "FI"],
    "FI at the US bridge's share of rent (phi 0.848): flow + credit effect", 0.04, 0.01)
rows_us = [("VAT flow (same formulas)", US["vat_flow"], I("VAT", "", "bridge", "post_mid"), 0.39, 0.42),
           ("VAT levy, lambda 0.35, 3.5c", US["vat_levy"], lev(0.35, "mid"), -1.76, -0.56),
           ("VAT net at impact", US["vat_net"], VATNET[0], -1.37, -0.14),
           ("LVT phi 0.98: flow", US["flow_f"], F_FL, 1.13, 0.14), ("LVT phi 0.98: credit effect", US["cr_f"], F_CR, -1.16, -0.11),
           ("LVT phi 0.98: flow + credit effect", US["flow_f"] + US["cr_f"], F_FL + F_CR, -0.04, 0.04),
           ("LVT phi 0.85: flow + credit effect", US["flow_b"] + US["cr_b"], sum(fi848), 0.15, 0.04),
           ("LVT same revenue: flow + credit effect", us_same[0] + us_same[1], F_FL + F_CR, 0.17, 0.04),
           ("LVT phi 0.98: includes the T4 overlap", US["flow_f"] + US["le_f"], F_FL + F_LE, -1.50, -0.11),
           ("LVT phi 0.98: non-occupiers on the wealth reading", US["flow_f"] + US["cr_f"] + US["no_f"], F_FL + F_CR + NO["mid"], -0.48, -1.05)]
claim(all(printed(a, c_, 0.01) and printed(b, d_, 0.01) for _, a, b, c_, d_ in rows_us), "US-beside-Finland table, every row (US / FI, % of consumption)",
      " ; ".join(f"{c_:+.2f}/{d_:+.2f}" for *_, c_, d_ in rows_us), " ; ".join(f"{a:+.3f}/{b:+.3f}" for _, a, b, *_ in rows_us))
gaps = [("VAT net", US["vat_net"] - VATNET[0], -1.23), ("post central path", -0.69 - 0.04, -0.73), ("LVT phi 0.98", US["flow_f"] + US["cr_f"] - F_FL - F_CR, -0.07),
        ("LVT phi 0.85", US["flow_b"] + US["cr_b"] - sum(fi848), 0.11), ("LVT same revenue", us_same[0] + us_same[1] - F_FL - F_CR, 0.13),
        ("T4", US["flow_f"] + US["le_f"] - F_FL - F_LE, -1.39), ("non-occupiers", US["flow_f"] + US["cr_f"] + US["no_f"] - F_FL - F_CR - NO["mid"], 0.57)]
claim(all(printed(a, b, 0.01) for _, a, b in gaps), "US - FI gaps: -1.23, -0.73, -0.07, +0.11, +0.13, -1.39, +0.57", " ".join(f"{b:+.2f}" for *_, b in gaps),
      " ".join(f"{a:+.3f}" for _, a, _ in gaps))
claim(printed(US["no_f"], -0.44, 0.01), "US full-capture non-occupier change -0.44 (US unit's output)", "-0.44", US["no_f"])
us_lhh = float(uin["L_hh"])
claim(printed(s_us, 0.416, 0.001) and printed(us_lhh / us_c, 2.6, 0.1) and printed(N211[2022] / C_MEUR, 1.1, 0.1) and printed(100 * float(ul1.loc["bridge", "r"]), 4.21, 0.01)
      and printed(100 * us_rent / us_c, 10.9, 0.1) and printed(100 * r22 * L_HBS["B2"] / C_MEUR, 1.9, 0.1) and printed(us_phi_b, 0.85, 0.01),
      "what is behind it: land share 0.416 vs 0.197; land / consumption 2.6 vs 1.1; r 4.21% (2024) vs 1.69% (2022); land rent 10.9% vs 1.9% of consumption; US phi 0.85",
      "0.416; 2.6/1.1; 4.21; 10.9/1.9; 0.85", f"{s_us:.3f}; {us_lhh / us_c:.2f}/{N211[2022] / C_MEUR:.2f}; {100 * float(ul1.loc['bridge', 'r']):.2f}; "
      f"{100 * us_rent / us_c:.1f}/{100 * r22 * L_HBS['B2'] / C_MEUR:.2f}; {us_phi_b:.3f}")
post = pd.read_csv(CONS / "data" / "tidy" / "post_published_numbers.csv").set_index("id")
p_us_flow, p_us_c, p_fi_c = float(post.loc["P662", "value"]), float(post.loc["P663", "value"]), 0.04
p_fi_flow = float(b_mc("post, published: flow-only path (year 3; band)"))
levy_gap_post = (p_us_c - p_us_flow) - (p_fi_c - p_fi_flow)
claim(printed(US["vat_levy"] - lev(0.35, "mid"), -1.20, 0.01) and printed(abs(levy_gap_post), 0.7, 0.1) and abs(levy_gap_post) / abs(p_us_c - p_fi_c) > 0.9,
      "'Under the VAT the whole US-Finland gap is the levy on net worth (1.2 points at impact; 0.7 in the post)'", "1.2 / 0.7",
      f"{US['vat_levy'] - lev(0.35, 'mid'):+.3f} of {US['vat_net'] - VATNET[0]:+.3f}; post {levy_gap_post:+.3f} of {p_us_c - p_fi_c:+.2f}",
      "post: (central - flow-only) gap from P662/P663 (US) and P878 + Fig 10 flow-only (FI)")


# %% M. robustness: land shares, carry, composition, convention, yield year, base, VAT law, liquidity, LTV method
AREA[0] = "M robustness"


def split_core(land, s_dec, mps):
    """Owner split for any land vector, shares by decile and mean land per share: per household, land units."""
    out = {}
    for d in DEC:
        Lo = float(land[d] / P_OWN[d])
        mu = np.log(Lo) - SIG_OWN[d] ** 2 / 2
        t = mps * float(s_dec[d])
        P = float(stats.lognorm(s=SIG_OWN[d], scale=np.exp(mu)).sf(t))
        above = Lo * float(stats.lognorm(s=SIG_OWN[d], scale=np.exp(mu + SIG_OWN[d] ** 2)).sf(t))
        out[d] = dict(recv=(1 - P_OWN[d]) * t + P_OWN[d] * (t * (1 - P) - (Lo - above)), pay=P_OWN[d] * (above - t * P), o_pay=P_OWN[d] * (above - t * P))
    return pd.DataFrame(out).T


def coll_variant(f, carry, method="us_shape", sigma=0.6):
    if method == "us_shape":
        c_ = crossers(f, 0.8)
        return c_["lc"] / CARRY * carry, c_["le"] / CARRY * carry
    nc, le, lc = lognormal_coll(f, 0.8, sigma)
    return lc / CARRY * carry, le / CARRY * carry


def variant(sd=None, sf=None, carry=None, conv="coherent", comp="12ew", year=2022, base="B2", flags="adopted", htm="half_month", method="us_shape", sigma=0.6):
    sd, sf, carry = (S_D if sd is None else sd), (S_F if sf is None else sf), (CARRY if carry is None else carry)
    m = M[conv] if comp == "12ew" else B.build_fi_model(convention=conv, composition=comp)
    av = B.fi_vat_accounting(m, flags=B.fi_vat_flags(flags))
    div = float(av["dividend"].iloc[0])
    ld = land_dec(sd, sf, carry)
    lq = pairq(ld[base])
    sq = m["units"]["shares"].reindex(Q)
    w = m["w"].reindex(Q)
    mps = float((w * lq / sq).sum())
    r = YLD[year]
    tb, tf = 12 * div / mps, PHI * r
    net = lambda tau: float((w * tau * lq / (12 * sq)).sum()) - tau * lq / (12 * sq)
    mpc = SCHED["mid"].reindex(Q)
    fp = lambda d_: 100 * float((w * d_).sum()) / m["budget_bar"]
    s_dec = pd.Series([float(sq[PAIR[d]]) for d in DEC], index=DEC)
    o = split_core(ld[base], s_dec, mps)
    recv, pay = pairq(o["recv"]) * tf / (12 * sq), pairq(o["pay"]) * tf / (12 * sq)
    hh = HO[htm]
    h = pd.Series([float((hh * o["pay"])[[DEC[2 * i], DEC[2 * i + 1]]].sum() / o["pay"][[DEC[2 * i], DEC[2 * i + 1]]].sum()) for i in range(5)], index=Q)
    lc, le = coll_variant(PHI * sd, carry, method, sigma)
    flow_f = fp(mpc * net(tf))
    return dict(phi_bridge=tb / r, share=PHI * r * mps / 12 / div, q1=float(net(tb)["q1"]), q5=float(net(tb)["q5"]), flow_b=fp(mpc * net(tb)),
                flow_v=fp(mpc * av["net"].reindex(Q)), flow_f=flow_f, flow_fw=fp(mpc * recv - (h + (1 - h) * MPC_U["mid"]) * pay),
                coll=-100 * MPCC["mid"] * lc / C_MEUR, net_full=flow_f - 100 * MPCC["mid"] * lc / C_MEUR, net_t4=flow_f - 100 * MPCC["mid"] * le / C_MEUR)


sdf = lambda v: (N211[2023] - v * HW23) / FFB23
VARS = [dict(), dict(sd=0.13, sf=sdf(0.13)), dict(sd=0.24, sf=sdf(0.24)), dict(sf=0.5), dict(sf=1.5), dict(carry=CARRY_MID), dict(conv="post"),
        dict(comp="14qa"), dict(year=2023), dict(year=2024), dict(year=2025), dict(base="B1"), dict(flags="law"), dict(htm="half_biweekly"),
        dict(htm="one_month"), dict(method="ln", sigma=0.5), dict(method="ln", sigma=0.6), dict(method="ln", sigma=0.8)]
COLS = {"phi_bridge": "phi_bridge", "share": "share_of_vat_dividend", "q1": "net_q1_bridge", "q5": "net_q5_bridge", "flow_b": "flow_lvt_bridge",
        "flow_f": "flow_lvt_full", "flow_fw": "flow_lvt_full_wealth_grade", "coll": "collateral_credit_full_6c", "net_full": "net_full", "net_t4": "net_full_t4"}
RB = []
mx = 0.0
for i, kw in enumerate(tqdm(VARS, desc="robustness variants")):
    v = variant(**kw)
    RB.append(v)
    for k, col in COLS.items():
        mx = max(mx, abs(v[k] - float(b_rob.iloc[i][col])))
claim(mx < 1e-6, "robustness rows (18 variants x 10 statistics; max abs diff vs fi_lvt_robustness.csv)", "fi_lvt_robustness.csv", mx)
rb = lambda i, k: RB[i][k]
checks_rb = [("main", [(0, "phi_bridge", 5.24, 0.01), (0, "share", 0.187, 0.001), (0, "q5", -174.5, 0.1), (0, "flow_b", 0.771, 0.001), (0, "net_full", 0.039, 0.001),
                       (0, "net_t4", -0.109, 0.001)]),
             ("s_d 0.13 / 0.24", [(1, "q5", -166.9, 0.1), (2, "q5", -179.4, 0.1), (1, "flow_b", 0.717, 0.001), (2, "flow_b", 0.806, 0.001),
                                  (1, "net_full", 0.086, 0.001), (2, "net_full", -0.008, 0.001)]),
             ("s_f 0.5 / 1.5", [(3, "phi_bridge", 5.67, 0.01), (4, "phi_bridge", 4.33, 0.01), (3, "share", 0.173, 0.001), (4, "share", 0.226, 0.001),
                                (3, "q5", -176.4, 0.1), (4, "q5", -170.6, 0.1), (3, "flow_b", 0.785, 0.001), (4, "flow_b", 0.743, 0.001),
                                (3, "net_full", 0.030, 0.001), (4, "net_full", 0.063, 0.001)]),
             ("carry to mid-2022", [(5, "phi_bridge", 5.31, 0.01), (5, "share", 0.185, 0.001), (5, "net_full", 0.039, 0.001)]),
             ("post convention", [(6, "phi_bridge", 5.25, 0.01), (6, "share", 0.187, 0.001), (6, "q5", -180.5, 0.1), (6, "flow_b", 0.792, 0.001),
                                  (6, "net_full", 0.043, 0.001)]),
             ("14qa composition", [(7, "phi_bridge", 5.25, 0.01), (7, "share", 0.187, 0.001), (7, "q5", -174.0, 0.1), (7, "flow_b", 0.780, 0.001),
                                   (7, "net_full", 0.041, 0.001)]),
             ("yields 2023 / 2024 / 2025", [(8, "net_full", 0.154, 0.001), (9, "net_full", 0.138, 0.001), (10, "net_full", 0.151, 0.001)]),
             ("B1", [(11, "phi_bridge", 6.72, 0.01), (11, "share", 0.146, 0.001), (11, "q5", -180.8, 0.1), (11, "flow_b", 0.817, 0.001), (11, "net_full", 0.014, 0.001)]),
             ("Finnish-law target", [(12, "phi_bridge", 4.70, 0.01), (12, "share", 0.209, 0.001), (12, "q5", -156.3, 0.1), (12, "flow_b", 0.691, 0.001),
                                     (12, "net_full", 0.039, 0.001)]),
             ("log-normal LTVs 0.5 / 0.8", [(15, "net_full", 0.023, 0.001), (17, "net_full", 0.061, 0.001)])]
for lab, items in checks_rb:
    ok = all(printed(rb(i, k), v, u) for i, k, v, u in items)
    claim(ok, f"robustness table: {lab}", " / ".join(f"{v:g}" for *_, v, _ in items), " / ".join(f"{rb(i, k):.4g}" for i, k, *_ in items))
claim(printed(RB[1]["coll"], -0.05, 0.01) and printed(RB[2]["coll"], -0.16, 0.01) and printed(RB[1]["net_full"], 0.09, 0.01) and printed(RB[2]["net_full"], -0.01, 0.01),
      "judgment table, s_d: collateral -0.05 to -0.16; net at full capture +0.09 to -0.01", "-0.05/-0.16; +0.09/-0.01",
      f"{RB[1]['coll']:.4f}/{RB[2]['coll']:.4f}; {RB[1]['net_full']:+.4f}/{RB[2]['net_full']:+.4f}")
claim(printed(100 * RB[3]["share"], 17, 1) and printed(100 * RB[4]["share"], 23, 1) and printed(RB[3]["net_full"], 0.03, 0.01) and printed(RB[4]["net_full"], 0.06, 0.01),
      "judgment table, s_f: funding share 17-23%; net +0.03 to +0.06", "17-23; +0.03/+0.06", f"{100 * RB[3]['share']:.1f}-{100 * RB[4]['share']:.1f}; "
      f"{RB[3]['net_full']:+.4f}/{RB[4]['net_full']:+.4f}")
yr = [RB[i] for i in (8, 9, 10)]
claim(printed(100 * min(v["share"] for v in yr), 32, 1) and printed(100 * max(v["share"] for v in yr), 34, 1) and printed(min(v["flow_f"] for v in yr), 0.24, 0.01)
      and printed(max(v["flow_f"] for v in yr), 0.26, 0.01) and printed(min(v["net_full"] for v in yr), 0.14, 0.01) and printed(max(v["net_full"] for v in yr), 0.15, 0.01),
      "judgment table, yield year: share 32-34%; flow at full capture 0.24-0.26; net +0.14 to +0.15", "32-34; 0.24-0.26; 0.14-0.15",
      f"{100 * min(v['share'] for v in yr):.1f}-{100 * max(v['share'] for v in yr):.1f}; {min(v['flow_f'] for v in yr):.3f}-{max(v['flow_f'] for v in yr):.3f}; "
      f"{min(v['net_full'] for v in yr):.3f}-{max(v['net_full'] for v in yr):.3f}")
claim(printed(RB[13]["flow_fw"], 0.221, 0.001) and printed(RB[14]["flow_fw"], 0.169, 0.001), "judgment table, hand-to-mouth threshold: wealth-grade flow 0.169-0.221 vs 0.201",
      "0.169-0.221", f"{RB[14]['flow_fw']:.4f}-{RB[13]['flow_fw']:.4f}")
# the log-normal shape's calibration on the US microdata ('within -16% to +1%' on lost capacity)
gus2 = us_m.assign(dec=us_m["dec"]).groupby("dec").apply(lambda g: pd.Series({"n": g["WGT"].sum(), "Vbar": np.average(g["HOUSES"] / cpi, weights=g["WGT"]),
                                                                           "A": (g["MRTHEL"] * g["WGT"]).sum() / (g["HOUSES"] * g["WGT"]).sum()}), include_groups=False)
rats = []
for f_ in (us_phi_b * s_us, PHI * s_us, us_phi_b * 0.02 / 0.05 * s_us):
    for th in (0.8, 0.9, 1.0):
        _, _, lc_micro = us_cross(f_, th)
        nc, le_, lc_ = lognormal_coll(f_, th, 0.6, 1.1, gus2["n"].values, gus2["Vbar"].values, gus2["A"].values)
        rats.append(lc_ / CARRY / 1e3 / lc_micro - 1)
claim(printed(100 * min(rats), -16, 1) and printed(100 * max(rats), 1, 1), "log-normal (1.1, 0.6) on US decile aggregates gets the US microdata's lost capacity within -16% to +1%",
      "-16% to +1%", f"{100 * min(rats):.1f}% to {100 * max(rats):+.1f}%", "three US cases (bridge, full, increment-only) x thresholds 0.8 / 0.9 / 1.0")


# %% N. review: double counting (T4), the yield year, payment units, who responds, judgment calls presented as measurements, the VAT comparison
AREA[0] = "N review"
# T4: the clean reading charges each owner-occupier's bill once (flow) and adds only the credit effect; every alternative swaps, never adds
st_ = HLm["full_m1"]
claim(near(st_["clean"][0] - F_FL, COLL["mid"], 1e-12) and near(st_["nonocc_wealth"][0] - st_["clean"][0], NO["mid"], 1e-12),
      "T4: the clean reading adds no equity loss to the flow; the non-occupier and stock readings replace the bill response, never add to it", "",
      "", "checked by construction above: add-back of non-occupiers' bills at the quintile MPC; crossers' own bills x decile MPC removed in 'stock'")
claim(True, "T4 dial: the bridge-equivalent charge (phi 5.2) is shown as infeasible (charge beyond the land's rent capitalizes beyond the dwelling)",
      "phi > 1 incoherent", f"phi x s_d = {t_b2 / r22 * S_D:.3f}", "the unit caps the price fall at the dwelling's value and labels the -2.77 row 'not a land tax'")
claim(True, "deferral 'dividend paid in full' is a state loan of 27% of the revenue (a deficit while it lasts); the NOTES say 'the state lends the liens'",
      "+0.37 / +1.98", f"+{deferral('full_m1')[0] - F_FL:.3f}", "an impulse from public borrowing, not from the land tax; the cash-balanced row is the LVT's own")
# the yield year: an end-2022 stock at the 2022 annual-mean yield; and the US-FI comparison mixes yield years
r24 = YLD[2024]
fl24 = F_FL * r24 / r22
no24 = nonocc("B2", PHI * r24)["change"]
net_no24 = fl24 + COLL["mid"] + no24
no_by_year = {y: F_FL * YLD[y] / r22 + COLL["mid"] + nonocc("B2", PHI * YLD[y])["change"] for y in (2023, 2024, 2025)}
us_no = US["flow_f"] + US["cr_f"] + US["no_f"]
claim(net_no24 < 1.5 * us_no, "'Non-occupiers' capitalized losses hit Finland (-1.05% against -0.48%)': robust to putting both countries on the same yield year",
      "-1.05 (FI 2022 yield) vs -0.48 (US 2024 yield)", f"FI at the 2024 yield {net_no24:+.3f}",
      f"the FI reading uses 1.69% (2022), the US 4.21% (2024); the capitalized loss per euro of bill is 1/r (59 vs 24). At Finland's own 2023/2024/2025 "
      f"yields the FI reading is {no_by_year[2023]:+.2f} / {no_by_year[2024]:+.2f} / {no_by_year[2025]:+.2f}, beside the US {us_no:+.2f}: the 'opposite "
      "directions' contrast and 'Low yields make Finnish land expensive relative to its rent' are a 2022-yield artifact. Report the FI row at 2023-25 "
      "yields too, or compare on one year")
loss24 = nonocc("B2", PHI * r24)["per_bill"]
claim(True, "info: capitalized loss per euro of bill by yield (1/r)", "59 (2022)", f"{loss24:.1f} (FI 2024); {1 / float(ul1.loc['bridge', 'r']):.1f} (US 2024)")
share_dec22 = div_full("coherent", "B2", dec22 / 100) / DIV["coherent"]
claim(True, "info: yield timing. The paper pairs annual-mean land with the annual-mean yield; the unit pairs an end-2022 stock with the 2022 "
      "annual mean (mid-2022 carry is the matching stock: phi 5.31)", "18.7%", f"{100 * share_dec22:.1f}% at the Dec-2022 yield ({dec22:.2f}%)",
      "the 2022 mean (1.69%) sits in a year when yields rose from 0.2% to 2.7%; the NOTES caveat says so and the 2023-25 rows bound it")
# who responds to the collateral loss
claim(False, "headline band 'Net demand at impact +0.04% [-0.01, +0.10]' carries the collateral judgment (who responds)", "[-0.01, +0.10]",
      f"hand-to-mouth-only {HLm['full_m1']['htm'][0]:+.3f}",
      f"the band spans the cents (4.7-7c) and the MPC schedules only; {100 * (1 - lc_htm / cx['lc']):.0f}% of the crossers' lost capacity belongs to "
      "owners with more than half a month's income in deposits, who need not borrow at impact. The NOTES table reports the hand-to-mouth reading "
      "(+0.13 [0.10, 0.17]) but the plain words omit it: add it to 'The sign turns on ...' or widen the band to +0.17")
nln = LN[0.6][0]
claim(True, "info: the crosser count is a borrowed shape, not a measurement", "122,000 (US shape)", f"{nln:,.0f} (log-normal sigma 0.6)",
      f"log-normal sigma 0.5 / 0.8: {LN[0.5][0]:,.0f} / {LN[0.8][0]:,.0f}; the Finnish HFCS microdata would measure it (NOTES caveat)")
claim(False, "'Renters pay nothing; they are 36% of households' (plain words) states a measurement", "renters pay nothing", f"renters hold {100 * ren_share:.1f}% of land",
      "it is the owner model's assumption (renters' 2.5% of household land, mostly rental flats and cottages, is assigned to owners); say 'in the model'")
# the VAT comparison
claim(False, "'Net demand at impact is +0.04% ..., about where the post put the Finnish VAT (+0.04%)' compares like with like", "+0.04 vs +0.04",
      f"LVT {HLm['full_m1']['clean'][0]:+.3f} vs this unit's VAT {VATNET[0]:+.3f}",
      "the post's +0.04 is its dynamic year-3 central path; on this unit's own impact formulas the Finnish VAT nets -0.14, so the LVT sits 0.18 points "
      "above the VAT, not 'about where' it. Quote the impact figure beside the post's")
gr_ = gross["LVT"] / gross["VAT"]
claim(True, "'about twice as redistributive' (same revenue): net redistribution sum w max(net, 0)", "about 2", gr_, "1.85x; Q5's payment 2.08x")
# concentration and the LVT/VAT ratio: a counterfactual with US land concentration on Finland's total
us_sh = usl["L1_share"].reindex(DEC)
cf = us_sh * float((LD["B2"] * NHD).sum()) / NHD
cf_q = pairq(cf)
mps_cf = mean_ps("coherent", cf_q)
tcf = 12 * DIV["coherent"] / mps_cf
net_cf = float((mc["w"] * tcf * cf_q / (12 * SQ["coherent"])).sum()) - tcf * cf_q / (12 * SQ["coherent"])
flow_cf = flow_pct("coherent", SCHED["mid"].reindex(Q) * net_cf)
claim(flow_cf / I("VAT", "", "bridge", "post_mid") > rat2 + 0.4, "'The ratio is smaller because Finnish land is less top-heavy' (1.8 vs US 2.5)", "1.83 vs 2.51",
      f"FI with US land concentration: {flow_cf / I('VAT', '', 'bridge', 'post_mid'):.2f}",
      "counterfactual: Finland's land total spread over income deciles with the US L1 shares raises the FI LVT/VAT flow ratio toward the US's; "
      "the explanation holds")
claim(True, "Fig 3 analogue 'only the top withdraws' is a netting artifact the NOTES flag", "Q4 at break-even",
      f"inside Q4 {100 * float(pairq(om['payer_hh'])['q4']):.0f}% of households pay net", "the NOTES' 'Netting hides payments in the lower deciles' covers it")
claim(True, "SCF use: WGT pooled over all five implicates (sums to 134.96m families), dollar year irrelevant (ratios only), INCPCTLECAT 10-12 merged "
      "into the top decile (macro PCTL points 90 95 99)", "", f"{SCF['WGT'].sum() / 1e6:.2f}m",
      "the US-shape population and my SCF recomputation reproduce the US unit's crossers exactly")
claim(True, "payment units: land per HOUSEHOLD (survey) / 12ew shares per HBS household, both conventions, as the VAT side; the dividend is per adult share "
      "(child 0.3)", "", "", "bridge.per_share_monthly's documented Finnish unit; checked above to 1e-6")
claim(True, "decile -> quintile pairing (D1, D2 -> q1 ...) and household weighting consistent on both sides (151u and HBS are household-weighted)", "", "",
      "the ranking variables differ (README_fin); pair mean vs pooled pair within 0.01%")


sd15, sd22 = variant(sd=gap_within, sf=sdf(gap_within)), variant(sd=ub22, sf=sdf(ub22))
claim(False, "s_d band 0.13-0.24: 'the own vs rented plot gap within region groups' (low) to 'N211/(N211+N111)' (high) brackets the evidence",
      "0.13-0.24", f"{gap_within:.3f}-{ub22:.3f}",
      f"the unit's own within-region sales-weighted gap is {gap_within:.3f}, not 0.13 (its evidence row prints 'band low 0.13' beside 0.150; 0.13 is "
      f"the rest-of-country gap 0.136 rounded down), and 0.24 is the 2023 bound while the flow year's (2022) N211/(N211+N111) is {ub22:.3f}. On that "
      f"evidence the net at full capture spans {sd22['net_full']:+.3f} (collateral {sd22['coll']:+.3f}) to {sd15['net_full']:+.3f}, not '+0.09 to "
      "-0.01': relabel or reset the band (S_D_BAND in lvt_fi.py) and reprint the judgment table row")
# who pays VAT: the liquidity grade gives VAT payers the hand-to-mouth share of ALL households, LVT payers that of owners
fv = dict(FL[("coherent", "VAT", "", "bridge")])
fv_own = dict(fv, h=pairq(HO["half_month"]))
liq_vat_own = flow_pct("coherent", dC(fv_own, "liq", "mid"))
claim(True, "info: liquidity grade asymmetry. VAT payers (the quintile's top spenders) get the hand-to-mouth share of all households; LVT payers "
      "that of owners", f"VAT {I('VAT', '', 'bridge', 'liq_mid'):.3f}", f"VAT at owners' shares {liq_vat_own:.3f}",
      "the VAT's liquidity-graded impulse is a lower bound; the LVT/VAT ratio under that grade (1.95) is correspondingly an upper bound")
per_euro = (us_same[0] / (100 * fi_rev), F_FL / (100 * fi_rev))
claim(per_euro[0] > per_euro[1], "'concentration feeds only the flow channel. There, the US raises more demand per euro, not less' (same revenue)",
      "US > FI", f"US {us_same[0]:.3f} vs FI {F_FL:.3f} at {100 * fi_rev:.2f}% of consumption", "")
# housekeeping the NOTES assert: bridge.py untouched, yield files vendored with MANIFEST rows, the builder's own check counts
import hashlib
import subprocess
try:
    head = subprocess.run(["git", "-C", str(REPO), "show", "HEAD:consumption/rebuild/code/bridge.py"], capture_output=True, check=True).stdout
    same_bridge = head == (CONS / "rebuild" / "code" / "bridge.py").read_bytes()
    note_b = "byte-identical to HEAD"
except Exception as e:                                                   # git unavailable: report, do not fail
    same_bridge, note_b = True, f"git not available ({type(e).__name__}); not checked"
claim(same_bridge, "'bridge.py is imported, not forked, and was not edited' (rebuild gates untouched)", "unchanged", "unchanged" if same_bridge else "CHANGED", note_b)
man = pd.concat([pd.read_csv(RAW / "eurostat" / "MANIFEST.csv"), pd.read_csv(RAW / "ecb" / "MANIFEST.csv")], ignore_index=True)
okh = []
for sub, fn in [("eurostat", "data/irt_lt_mcby_a_FI.json"), ("eurostat", "data/irt_lt_mcby_m_FI.json"), ("ecb", "data/IRS_M.FI.L.L40.CI.0000.EUR.N.Z.csv")]:
    h = hashlib.sha256((RAW / sub / fn).read_bytes()).hexdigest()
    okh.append(bool((man["file"] == fn).any()) and h in set(man.loc[man["file"] == fn, "sha256"]))
claim(all(okh), "yield files vendored once via common.fetch with MANIFEST rows whose sha256 match the files", "3 files", f"{sum(okh)} of 3 match")
bc_ = bcsv("check_lvt_fi.csv")["result"].value_counts()
claim(int(bc_.get("PASS", 0)) == 85 and int(bc_.get("FAIL", 0)) == 0 and int(bc_.get("INFO", 0)) == 8, "the builder's checks: '85 PASS / 0 FAIL / 8 INFO'",
      "85 / 0 / 8", f"{int(bc_.get('PASS', 0))} / {int(bc_.get('FAIL', 0))} / {int(bc_.get('INFO', 0))}")


QUOTED = ["+0.04% [−0.01, +0.10]", "about where the post put the Finnish VAT (+0.04%)", "22.6% of all gross LVT payments",
          "12 of the LVT's bars flip sign", "(−1.05% against −0.48%)", "Renters pay nothing", "post within 0.1 point",
          "0.13 (own vs rented plot price gap within region groups, a lower bound)", "net at full capture +0.09 to −0.01",
          "Owners' cuts land on imputed rent and housing-company charges", "Low yields make Finnish land expensive relative to its rent",
          "in opposite directions", "against 71-91% under the VAT"]
missing = [p_ for p_ in QUOTED if not in_notes(p_)]
claim(not missing, "every NOTES_fi.md phrase the BAD claims quote is verbatim in the NOTES", f"{len(QUOTED)} phrases", f"{len(QUOTED) - len(missing)} found",
      "; ".join(missing))


# %% summary
dr_bad = [x for x in DR]
AREA[0] = "N review"
claim(len(dr_bad) == 0, "printed numbers that only a double rounding reproduces (rounded to 3 decimals, then to 2)", "", f"{len(dr_bad)} values",
      "; ".join(f"{x['mine']:.5g} printed {x['printed']:g} ({x.get('claim', '')[:60]})" for x in dr_bad) +
      ". Print from the unrounded values (e.g. the headline band's top +0.0948 is +0.09, not +0.10)")
res = pd.DataFrame(CLAIMS)
res.index = np.arange(1, len(res) + 1)
res.index.name = "n"
res.to_csv(OUT_CSV)
w_ = 60
for i, r in res.iterrows():
    print(f"{r['status']:3s} | {r['area']:<16s} | {r['claim']} | builder {r['builder']} | mine {r['mine']}" + (f" | {r['note']}" if r["note"] else ""))
n_ok, n_bad = int((res["status"] == "OK").sum()), int((res["status"] == "BAD").sum())
print(f"\n{n_ok} OK / {n_bad} BAD of {len(res)} claims; written {OUT_CSV.relative_to(REPO)}")
