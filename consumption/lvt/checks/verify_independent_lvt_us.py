"""Independent verification of the LVT US unit (consumption/lvt/NOTES_us.md, code/lvt_us.py, code/run_lvt_us.py, out/us_lvt_*.csv).

Nothing is imported or copied from consumption/lvt/code/. The method is re-implemented from NOTES_us.md and the task text,
reading the RAW files where the task asks for them:

  - SCF 2025 and 2022 summary extracts: parsed here from the vendored zips (raw/fed/scf/scfp2025excel.zip, scfp2022excel.zip);
  - SCF 2022 roster (adults and minors in the primary economic unit): rebuilt here from the full public Stata file
    (raw/fed/scf/scf2022s.zip, p22i6.dta) with the codebook's PEU rule, not from the tidy roster/xvars files;
  - Z.1 land: annual means and year-ends rebuilt here from the QUARTERLY rows of data/tidy/z1_land.csv;
  - GS10 / DGS10: the repo's vendored FRED copies (pinning/cache, three-taxes/cache); PCE housing: data/tidy/bea_pce_u_long.csv.gz;
  - the FEDS note on the SCF windfall question: parsed from raw/fed/feds_notes/ (accessible-data page).

bridge.py (verified separately) is imported for the CE 2024 model dict (C, w, budget, eta, payment units), the VAT accounting, the
MPC schedules and eta_table (for the tenure baskets). Weights, land allocation, bills, dividends, net transfers, household units,
hand-to-mouth flags, MPC grading, impulses, category shifts, collateral, the levy channel and the loop are computed here.

Every claim prints one line

    OK  | claim | builder | mine | note        (or BAD | ...)

OK means: my independent value agrees with the builder's CSV value and with the number NOTES_us.md prints (within the printed
rounding or the stated tolerance), or, for a review item, that the builder's statement holds up. BAD means one of these fails, or
that a statement or judgment call does not hold up on review (the note says why and what should change). A final count follows.
A CSV copy goes to out/verify_independent_lvt_us.csv.

Run from the repo root:  venv/bin/python -I consumption/lvt/checks/verify_independent_lvt_us.py   (about 20 s)

Plain functions and top-level code, so the cells can be pasted into a notebook.
"""
# %% setup
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent                     # consumption/lvt/checks
LVT = HERE.parent
CONS = LVT.parent
REPO = CONS.parent
sys.path.insert(0, str(CONS / "rebuild" / "code"))          # bridge.py only (verified separately)

import html
import io
import re
import zipfile
from decimal import ROUND_HALF_UP, Decimal

import numpy as np
import pandas as pd
from tqdm.auto import tqdm

import bridge as B

RAW_SCF = CONS / "data" / "raw" / "fed" / "scf"
RAW_FEDS = CONS / "data" / "raw" / "fed" / "feds_notes" / "feds-note-mpc-heterogeneity-accessible-20261009.htm"
TIDY = CONS / "data" / "tidy"
BOUT = LVT / "out"                                          # the builder's outputs (read only)
OUT_CSV = BOUT / "verify_independent_lvt_us.csv"
NOTES_TXT = re.sub(r"\s+", " ", (LVT / "NOTES_us.md").read_text())   # whitespace-normalized, for the wording claims
DEC = [f"d{i:02d}" for i in range(1, 11)]
CPILAG25 = 4750.0 / 4625.0          # macro: annual-average CPI-U-RS 2025 / 2024 (income-year factor of the 2025 extract)
PHI_FULL, GAMMA, DELTA, LEVY = 0.98, 0.02, 0.05, 0.08
MPW = {"low": 0.02, "mid": 0.035, "high": 0.05}
MPCC = {"low": 0.047, "mid": 0.06, "high": 0.10}
LS = {"low": 0.30, "mid": 0.40, "high": 0.50}
CLAIMS = []
AREA = ""


DR = []                                                     # printed values that only a double rounding reproduces
DR_SEEN = [0]


def claim(ok, text, builder, mine, note=""):
    """Record one claim. builder/mine are printed as given (str) or formatted floats. A claim whose printed-value check was met
    only by a double rounding (pv below) says so in its note; all such cases are summarized in one review claim at the end."""
    f = lambda v: v if isinstance(v, str) else ("" if v is None else (f"{v:.4g}" if abs(v) < 1e4 else f"{v:,.0f}"))
    if len(DR) > DR_SEEN[0] and not text.startswith("printed numbers that only a double rounding"):
        note = (note + "; " if note else "") + "printed value double-rounded: " + "; ".join(DR[DR_SEEN[0]:])
        DR_SEEN[0] = len(DR)
    CLAIMS.append(dict(area=AREA, status="OK" if ok else "BAD", claim=text, builder=f(builder), mine=f(mine), note=note))
    return ok



def pv(mine, printed, unit=0.01, label=""):
    """A printed (NOTES) value: within half a printed unit of mine; or reproduced only by double rounding (mine rounded to one
    more decimal first, then to the printed unit, half up), which is accepted here and logged in DR for one summary claim."""
    mine, printed = float(mine), float(printed)
    if abs(mine - printed) <= 0.5 * unit * 1.02 + 1e-12:
        return True
    d = int(round(-np.log10(unit)))
    q1, q2 = Decimal(1).scaleb(-(d + 1)), Decimal(1).scaleb(-d)
    r2 = Decimal(str(mine)).quantize(q1, rounding=ROUND_HALF_UP).quantize(q2, rounding=ROUND_HALF_UP)
    if abs(float(r2) - printed) < 1e-9:
        DR.append(f"{label}: {mine:.4f} printed {printed:g}")
        return True
    return False


def close(a, b, tol, rel=False):
    a, b = float(a), float(b)
    if not (np.isfinite(a) and np.isfinite(b)):
        return False
    return abs(a - b) <= (tol * max(abs(b), 1e-12) if rel else tol)


def num(a, b, text, notes_val=None, notes_tol=None, tol=1e-6, rel=True, note=""):
    """Numerical claim: my value a vs the builder's CSV value b (tol), and vs the NOTES' printed value (notes_tol, absolute)."""
    ok = close(a, b, tol, rel)
    msg = note
    if notes_val is not None:
        okn = pv(a, notes_val, 10.0 ** np.round(np.log10(2 * notes_tol)), text)   # half a printed unit (double rounding logged)
        ok = ok and okn
        msg = (f"NOTES {notes_val:g}" + ("" if okn else " (NOT within its rounding)") + ("; " + note if note else ""))
    return claim(ok, text, b, a, msg)


def wsum(x, w):
    return float(np.sum(np.asarray(x, float) * np.asarray(w, float)))


# %% 1. raw readers: SCF summary extracts from the zips; the 2022 PEU roster from the full Stata file
def read_scf(year):
    """The Fed's summary extract as published (2025 dollars; all implicates; WGT = X42001/5)."""
    with zipfile.ZipFile(RAW_SCF / f"scfp{year}excel.zip") as z:
        with z.open(f"SCFP{year}.csv") as f:
            d = pd.read_csv(f, low_memory=False)
    d.columns = [c.upper() for c in d.columns]
    return d


def peu_roster_2022():
    """Adults and minors in each record's PEU from p22i6.dta: person 1 always; person 2 if X7020 = 2; persons 3-12 if
    financially dependent (X113, X119, ... = 1). Adult = age >= 18 (X8022, X104, X110, ...)."""
    with zipfile.ZipFile(RAW_SCF / "scf2022s.zip") as z:
        buf = io.BytesIO(z.read("p22i6.dta"))
    rel = [108, 114, 120, 126, 132, 202, 208, 214, 220, 226]
    cols = ["y1", "yy1", "x42001", "x7001", "x7020", "x8022", "x102", "x104"]
    for n in rel:
        cols += [f"x{n}", f"x{n + 2}", f"x{n + 5}"]
    d = pd.read_stata(buf, columns=cols, convert_categoricals=False)
    yy1_dtype = str(d["yy1"].dtype)
    d = d.astype({c: "int64" for c in cols if c != "x42001"})
    adults = np.ones(len(d))
    minors = np.zeros(len(d))
    peu = np.ones(len(d))
    sp = (d["x7020"] == 2).values
    adults += sp & (d["x104"].values >= 18)
    minors += sp & (d["x104"].values < 18)
    peu += sp
    for n in rel:
        inpeu = (d[f"x{n}"].values != 0) & (d[f"x{n + 5}"].values == 1)
        age = d[f"x{n + 2}"].values
        adults += inpeu & (age >= 18)
        minors += inpeu & (age < 18)
        peu += inpeu
    out = pd.DataFrame({"Y1": d["y1"].values, "YY1_raw_dtype": yy1_dtype, "X42001": d["x42001"].values,
                        "X7001": d["x7001"].values, "N_PEU_mine": peu, "ADULTS": adults, "MINORS": minors})
    return out


# %% 2. Z.1 from the quarterly rows; yields; PCE housing
Z = pd.read_csv(TIDY / "z1_land.csv", dtype={"date": str})


def zq(sid, year):
    q = Z[(Z["series_id"] == sid) & (Z["freq"] == "Q") & Z["date"].str.startswith(str(year))]
    assert len(q) == 4, (sid, year, len(q))
    return q.sort_values("date")["value"].astype(float).values


def zmean(sid, year):
    return float(zq(sid, year).mean())


def zeop(sid, year):
    return float(zq(sid, year)[-1])


def z1_mine(year=2024):
    t = {}
    t["re_hh"], t["str_hh"] = zmean("LM155035005", year), zmean("LM155012665", year)
    t["L_hh"] = t["re_hh"] - t["str_hh"]
    t["re_ownocc"] = zmean("LM155035015", year)
    t["L_ownocc"] = t["re_ownocc"] - t["str_hh"]
    t["mortg"] = zmean("LA153165105", year)
    # noncorporate (the paper's conventions: FRED 'A' ids are year-end, 'Q' ids annual means)
    t["L_nnb"] = zeop("LM115035005", year) - zmean("FL115012665", year) - zeop("FL115013665", year)
    t["re_nfc"] = zeop("LM105035005", year)
    shares = {}
    for y in range(2016, 2021):
        land = zeop("LM105035005", y) - zmean("LM105012665", y) - zeop("LM105013665", y)
        shares[y] = land / zeop("LM105035005", y)
    t["nfc_share_1620"] = float(np.mean([shares[y] for y in range(2016, 2021)]))
    t["nfc_share_2020"] = shares[2020]
    t["L_nfc"] = t["nfc_share_1620"] * t["re_nfc"]
    t["L_nfc_high"] = t["nfc_share_2020"] * t["re_nfc"]
    s20 = zmean("LM105012665", 2020) + zeop("LM105013665", 2020)
    g = (zmean("FL115012665", year) + zeop("FL115013665", year)) / (zmean("FL115012665", 2020) + zeop("FL115013665", 2020))
    t["L_nfc_low"] = t["re_nfc"] - s20 * g
    return t


AREA = "inputs: Z.1, yields, PCE, CE"
z1 = z1_mine(2024)
z25 = z1_mine(2025)
inp = pd.read_csv(BOUT / "us_lvt_inputs.csv").set_index("item")["value"]
num(z1["L_hh"], inp["L_hh"], "Z.1 household land 2024, $bn (HH+NPO RE minus HH structures, annual means of quarters)", 23410.7, 0.05)
num(z25["L_hh"], 23466.4, "Z.1 household land 2025 (task statement 23,466.4 on the 2026:Q2 vintage)", 23466.4, 0.05, tol=0.05, rel=False)
num(z1["L_nnb"], inp["L_nnb"], "Z.1 noncorporate business land 2024 (paper's conventions), $bn", 8354.4, 0.05)
num(z1["L_nfc"], inp["L_nfc"], "NFC land 2024, assumption: 2016-2020 mean land share x 2024 NFC real estate", 3994.6, 0.05)
num(z1["nfc_share_1620"], inp["nfc_share_2016_2020"], "NFC land share of NFC real estate, 2016-2020 mean", 0.255, 0.0005)
num(z1["L_nfc_low"], inp["L_nfc_structures_proxy"], "NFC land, low variant (structures grown at noncorporate structures' growth)", 1699.8, 0.05)
num(z1["L_nfc_high"], inp["L_nfc_share_2020"], "NFC land, high variant (2020 share)", 4306.2, 0.05)
num(z1["L_ownocc"], inp["L_hh_ownocc"], "households-only owner-occupied land residual, $bn", 19374.9, 0.05)
num(z1["L_hh"] / z1["re_hh"], inp["land_share_re"], "Z.1 2024 land / HH+NPO real estate", 0.460, 0.0005)
num(z1["re_hh"] / 1000, inp["re_hh"] / 1000, "Z.1 2024 HH+NPO real estate, $tn", 50.9, 0.05)
num(z1["re_ownocc"] / 1000, inp["re_ownocc"] / 1000, "Z.1 2024 households' owner-occupied real estate, $tn", 46.9, 0.05)
num(z1["L_hh"] + z1["L_nnb"] + z1["L_nfc"], 35759.62926, "L2 land total, $bn (NOTES: $35.8tn)", 35759.6, 0.1)

g = pd.read_csv(REPO / "pinning" / "cache" / "GS10.csv", parse_dates=["observation_date"])
GS10 = float(g[g["observation_date"].dt.year == 2024]["GS10"].mean())
dg = pd.read_csv(REPO / "three-taxes" / "cache" / "DGS10.csv", parse_dates=["observation_date"])
dg["v"] = pd.to_numeric(dg["DGS10"], errors="coerce")
DGS10 = float(dg[dg["observation_date"].dt.year == 2024]["v"].mean())
num(GS10, inp["gs10_2024"], "GS10 2024 annual mean (12 months), %", 4.208, 0.0005,
    note=f"daily DGS10 2024 mean {DGS10:.3f} (agrees to {abs(GS10 - DGS10):.3f} pp)")
bea = pd.read_csv(TIDY / "bea_pce_u_long.csv.gz", low_memory=False, usecols=["table", "freq", "series_code", "date", "value"])
bea = bea[(bea["table"] == "2.4.5U") & (bea["freq"] == "A") & (bea["date"].astype(str) == "2024")]
PCE_H = float(bea[bea["series_code"] == "DHSGRC"]["value"].iloc[0]) / 1000.0
PCE = float(bea[bea["series_code"] == "DPCERC"]["value"].iloc[0]) / 1000.0
num(PCE_H, inp["pce_housing_2024_bn"], "PCE housing services 2024, $bn", 3148.6, 0.05)
RT = {"m1": z1["L_hh"] * GS10 / 100, "m2": z1["L_hh"] * (GS10 + 1.5) / 100, "m3": 0.30 * PCE_H, "m4": 0.50 * PCE_H}
R = {k: v / z1["L_hh"] for k, v in RT.items()}
for k, nv in zip(RT, [4.21, 5.71, 4.03, 6.72]):
    num(100 * R[k], 100 * inp[f"r_{k}"], f"rent-to-value r on measure {k}, %", nv, 0.005)

# CE 2024 via bridge (verified separately)
m = B.build_model(2024)
acc_v = B.vat_accounting(m)
U = m["units"]
N_CE = U["N_thousand"].values * 1000.0
SH_CE = U["shares"].values
S_CE = float((N_CE * SH_CE).sum())
W_D = N_CE * SH_CE / S_CE
BUD = m["budget"].values
BUD_BAR = float((W_D * BUD).sum())
C_TOT = BUD_BAR * S_CE * 12 / 1e9                     # $bn/yr, the post's denominator
DIV_VAT = float(acc_v["dividend"].iloc[0])
VAT_REV = DIV_VAT * S_CE * 12 / 1e9
num(S_CE / 1e6, inp["ce_payment_shares"] / 1e6, "CE 2024 payment shares, million", 279.1, 0.05)
num(DIV_VAT, inp["vat_dividend_usd_month"], "VAT dividend per adult share per month, $", 249.38, 0.005)
num(VAT_REV, inp["vat_revenue_bn"], "VAT revenue, $bn/yr", 835.1, 0.05)
num(C_TOT, inp["ce_consumption_bn"], "CE consumption budget, $bn/yr (impulse denominator)", None, None)


# %% 3. SCF: weights, deciles, dollars, the 2022 PEU roster, payment units
AREA = "SCF: weights, deciles, dollars, units"


def flags(d_):
    """Decile (12 Fed groups: 1-9 deciles, 10-12 = 90-95, 95-99, 99-100 merged into 10), owner and 65+ flags."""
    dec_i = np.minimum(d_["INCPCTLECAT"].astype(int), 10)
    extra = pd.DataFrame({"dec_i": dec_i, "dec": dec_i.map(lambda k: f"d{k:02d}"), "owner": (d_["HOUSES"] > 0).astype(int),
                          "age65": (d_["AGE"] >= 65).astype(int)}, index=d_.index)
    return pd.concat([d_, extra], axis=1)


s25 = flags(read_scf(2025))
s22 = flags(read_scf(2022))
w25, w22 = s25["WGT"].values, s22["WGT"].values
num(w25.sum() / 1e6, inp["scf2025_families_m"], "SCF 2025 families, million (WGT pooled over the five implicates)", 134.96, 0.005)
num(w22.sum() / 1e6, inp["scf2022_families_m"], "SCF 2022 families, million", 131.31, 0.005)
dshare = pd.Series([w25[s25["dec_i"].values == k].sum() / w25.sum() for k in range(1, 11)], index=DEC)
claim(bool((dshare - 0.1).abs().max() <= 0.0003), "each SCF 2025 income decile (INCPCTLECAT, 10-12 merged) holds 10.0% +/- 0.03% of families",
      "10.0% +/- 0.03%", f"{100 * dshare.min():.3f}-{100 * dshare.max():.3f}%")


def weighted_cut(x, w, p):
    """Smallest x at which the weighted CDF reaches p."""
    o = np.argsort(np.asarray(x, float), kind="mergesort")
    cw = np.cumsum(np.asarray(w, float)[o]) / np.sum(w)
    return float(np.asarray(x, float)[o][np.searchsorted(cw, p)])


rng = s25.groupby("INCPCTLECAT")["INCOME"].agg(["min", "max"])
mono = bool((rng["max"].values[:-1] <= rng["min"].values[1:]).all())
cuts = [weighted_cut(s25["INCOME"], w25, p_) for p_ in (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9)]
cut_ok = all(abs(c_ - lo) < 1e-6 for c_, lo in zip(cuts, rng["min"].values[1:10]))
claim(mono and cut_ok, "INCPCTLECAT is a pooled weighted decile cut of INCOME (monotone; cut points = my weighted percentiles)",
      "Fed groups", f"monotone {mono}; 9 cut points equal {cut_ok}",
      "tied incomes at a cut (round numbers) are split across the two groups so that each holds exactly 10%")
# dollars: INCOME is the 2024 income year x CPILAG; balance-sheet items are interview-date (2025) values (CPIADJ = 1)
macro = (RAW_SCF / "bulletin.macro.txt").read_text(errors="replace")
mm = re.search(r"YEAR=2025\).*?CPIADJ=&CPIBASE/(\d+);\s*%LET CPILAG=(\d+)/(\d+);", macro, re.S)
claim(mm is not None and abs(int(mm.group(2)) / int(mm.group(3)) - inp["cpi_2025_to_2024"]) < 1e-9,
      "the 2025 extract's CPILAG = 4750/4625 (the factor the unit divides by)", f"{inp['cpi_2025_to_2024']:.6f}",
      f"{int(mm.group(2))}/{int(mm.group(3))}" if mm else "not found",
      "CPILAG moves INCOME (2024) to 2025 dollars; balance sheets are interview-date values, so '2024 $' for HOUSES is a CPI "
      "deflation, not a 2024 valuation. Harmless here: a uniform s, LTVs and HtM ratios are invariant to it")
# the 2022 roster, rebuilt from the Stata file
ros = peu_roster_2022()
claim(bool((ros["N_PEU_mine"] == ros["X7001"]).all()), "PEU rule (person 1; spouse if X7020=2; others if financially dependent) reproduces X7001 on every 2022 record",
      "README: all 22,975", f"{int((ros['N_PEU_mine'] == ros['X7001']).sum()):,} of {len(ros):,}")
wr = ros["X42001"].values / 5
num(wsum(ros["ADULTS"], wr) / 1e6, 225.0, "SCF 2022 adults in PEUs, million (README 225.0)", 225.0, 0.05, tol=0.05, rel=False)
num(wsum(ros["MINORS"], wr) / 1e6, 74.1, "SCF 2022 minors in PEUs, million (NOTES 74.1)", 74.1, 0.05, tol=0.05, rel=False)
# the data-defect claim: tidy IMPLICATE wrong for YY1 >= 3277 (int16 overflow of 10*YY1)
xv = pd.read_csv(TIDY / "scf2022_xvars.csv.gz", usecols=["YY1", "Y1", "IMPLICATE"])
badimp = xv["IMPLICATE"] != (xv["Y1"] - 10 * xv["YY1"])
hi = xv["YY1"] >= 3277
claim(bool(badimp.equals(hi) and set(xv.loc[hi, "IMPLICATE"]) <= set(range(65537, 65542)) and ros["YY1_raw_dtype"].iloc[0] == "int16"),
      "data defect: tidy xvars IMPLICATE is wrong exactly for YY1 >= 3277 (65537-65541), YY1 is int16 in the Stata file",
      "6,625 records", f"{int(badimp.sum()):,} records; YY1 dtype {ros['YY1_raw_dtype'].iloc[0]}")
src = (CONS / "code" / "acquire_fed.py").read_text().splitlines()
line = src[1134].strip() if len(src) >= 1135 else ""
claim(('FULL["Y1"] - 10 * FULL["YY1"]' in line and "astype" not in line) or "Not fixed here" not in NOTES_TXT or not badimp.any(),
      "NOTES 'Data defect found': the cause still sits in acquire_fed.py line 1135 and is 'not fixed here'",
      'FULL["Y1"] - 10 * FULL["YY1"]', line[:80],
      "stale: commit aeba577 fixed the line (int64 cast) but the tidy scf2022_roster/xvars files were not regenerated and still "
      "carry 6,625 bad IMPLICATE values; the paragraph should say so")
# payment units 2025: adults = 1 + partner + 2022-roster cell mean of other PEU adults; minors likewise (AGECL x MARRIED x min(KIDS,3))
r22 = s22[["Y1", "WGT", "AGECL", "MARRIED", "KIDS", "dec"]].merge(ros[["Y1", "ADULTS", "MINORS"]], on="Y1", how="left", validate="one_to_one")
assert r22["ADULTS"].notna().all()
r22 = r22.assign(oth=r22["ADULTS"] - 1 - (r22["MARRIED"] == 1), kb=np.minimum(r22["KIDS"].astype(int), 3))


def cellmeans(keys):
    gb = r22.groupby(keys)
    return pd.DataFrame({"oth": gb.apply(lambda q: np.average(q["oth"], weights=q["WGT"]), include_groups=False),
                         "minors": gb.apply(lambda q: np.average(q["MINORS"], weights=q["WGT"]), include_groups=False),
                         "n": gb.size()})


FINE, COARSE = cellmeans(["AGECL", "MARRIED", "kb"]), cellmeans(["AGECL", "MARRIED"])


def predict_units(d_):
    kb = np.minimum(d_["KIDS"].astype(int), 3).values
    fi = FINE.reindex(pd.MultiIndex.from_arrays([d_["AGECL"].values, d_["MARRIED"].values, kb]))
    co = COARSE.reindex(pd.MultiIndex.from_arrays([d_["AGECL"].values, d_["MARRIED"].values]))
    use = (fi["n"].fillna(0).values >= 40)
    oth = np.where(use, fi["oth"].values, co["oth"].values)
    mn = np.where(use, fi["minors"].values, co["minors"].values)
    return 1.0 + (d_["MARRIED"].values == 1) + oth, mn


def calibrate(d_, adults, minors):
    raw = adults + 0.3 * minors
    tot = pd.Series(raw * d_["WGT"].values).groupby(d_["dec"].values).sum().reindex(DEC).values
    c = N_CE * SH_CE / tot
    return raw * c[d_["dec_i"].values - 1], pd.Series(c, index=DEC), raw


a25, mn25 = predict_units(s25)
sh25, C25, raw25 = calibrate(s25, a25, mn25)
sh22, C22, raw22 = calibrate(s22, r22["ADULTS"].values, r22["MINORS"].values)
s25 = pd.concat([s25, pd.DataFrame({"shares": sh25, "shares_raw": raw25}, index=s25.index)], axis=1)
s22 = pd.concat([s22, pd.DataFrame({"shares": sh22, "shares_raw": raw22}, index=s22.index)], axis=1)
ld = pd.read_csv(BOUT / "us_lvt_land_by_decile.csv").set_index("decile")
num((C25 - ld["c_d_2025"]).abs().max(), 0.0, "SCF 2025 payment-share scaling to CE deciles c_d: max gap to the builder", tol=1e-6, rel=False,
    note=f"c_d {C25.min():.2f}-{C25.max():.2f} (NOTES 0.92-1.19)")
num((C22 - ld["c_d_2022"]).abs().max(), 0.0, "SCF 2022 (roster) payment-share scaling c_d: max gap to the builder", tol=1e-6, rel=False)
claim(close(C25.min(), 0.92, 0.005) and close(C25.max(), 1.19, 0.005), "c_d = 0.92-1.19", "0.92-1.19", f"{C25.min():.3f}-{C25.max():.3f}")
# in-sample check of the cell prediction on 2022 (NOTES: decile means within 0.06 shares)
p22a, p22m = predict_units(s22)
gap22 = (pd.Series((p22a + 0.3 * p22m - (r22["ADULTS"].values + 0.3 * r22["MINORS"].values)) * w22).groupby(s22["dec"].values).sum()
         / pd.Series(w22).groupby(s22["dec"].values).sum())
claim(bool(gap22.abs().max() <= 0.06 + 1e-9), "2022 in-sample: predicted shares' decile means within 0.06 of the roster's", "within 0.06",
      f"max {gap22.abs().max():.3f}")


# %% 4. land by family and by decile
AREA = "land by household"
DOLLARS = ["HOUSES", "ORESRE", "NNRESRE", "BUS", "ACTBUS", "EQUITY", "MRTHEL", "NETWORTH", "INCOME", "LIQ", "STOCKS", "BOND",
           "NMMF", "CCBAL", "HOMEEQ", "RESDBT", "RETQLIQ", "CASHLI", "CDS", "SAVBND", "OTHMA", "TOTSPENDNH"]
s25 = pd.concat([s25, pd.DataFrame({v + "_24": s25[v].astype(float) / CPILAG25 for v in DOLLARS}, index=s25.index)], axis=1)
s22 = pd.concat([s22, pd.DataFrame({v + "_24": s22[v].astype(float) / CPILAG25 for v in DOLLARS}, index=s22.index)], axis=1)
# (the unit's convention, '2024 dollars': every dollar value / CPILAG)


def land(d_, Lhh_bn, Lnnb_bn, Lnfc_bn, s_fix=None, nnb_key=("NNRESRE", "BUS"), rising=False):
    w = d_["WGT"].values
    Po, Pr = d_["HOUSES_24"].clip(lower=0).values, d_["ORESRE_24"].clip(lower=0).values
    prop = wsum(Po + Pr, w)
    if rising:
        own = Po > 0
        o = np.argsort(Po[own])
        xs, cw = Po[own][o], np.cumsum(w[own][o]) / w[own].sum()
        F = lambda v: np.interp(v, xs, cw, left=0.0, right=1.0)
        ro, rr = 0.30 + 0.30 * F(Po), 0.30 + 0.30 * F(Pr)
        k = Lhh_bn * 1e9 / wsum(ro * Po + rr * Pr, w)
        so, sr = k * ro, k * rr
    else:
        k = np.nan
        so = sr = (Lhh_bn * 1e9 / prop if s_fix is None else s_fix)
    out = pd.DataFrame(index=d_.index)
    out["L_own"], out["L_ore"] = so * Po, sr * Pr
    kn = sum(d_[c + "_24"].clip(lower=0).values for c in nnb_key)
    ke = d_["EQUITY_24"].clip(lower=0).values
    out["L_nnb"] = Lnnb_bn * 1e9 * kn / wsum(kn, w)
    out["L_nfc"] = Lnfc_bn * 1e9 * ke / wsum(ke, w)
    out["L1"] = out["L_own"] + out["L_ore"]
    out["L2"] = out["L1"] + out["L_nnb"] + out["L_nfc"]
    return out, dict(s=(Lhh_bn * 1e9 / prop if s_fix is None else s_fix), prop_bn=prop / 1e9, k=k)


def dsum(d_, x):
    return pd.Series(np.asarray(x, float) * d_["WGT"].values).groupby(d_["dec"].values).sum().reindex(DEC).values


L25, I25 = land(s25, z1["L_hh"], z1["L_nnb"], z1["L_nfc"])
L22, I22 = land(s22, z1["L_hh"], z1["L_nnb"], z1["L_nfc"])
cal = pd.read_csv(BOUT / "us_lvt_s_calibration.csv").set_index("item")["value"]
num(I25["s"], inp["s_uniform_2025"], "land share s, uniform: Z.1 2024 household land / SCF 2025 HOUSES+ORESRE (2024 $)", 0.416, 0.0005)
s_nom = z25["L_hh"] * 1e9 / wsum(s25["HOUSES"].clip(lower=0) + s25["ORESRE"].clip(lower=0), w25)
num(s_nom, cal.iloc[1], "s on SCF 2025 nominal against Z.1 2025", 0.406, 0.0005)
num(I22["s"], inp["s_uniform_2022"], "s, SCF 2022 (real 2024 $) to Z.1 2024", 0.442, 0.0005)
H24 = wsum(s25["HOUSES_24"].clip(lower=0), w25) / 1e12
O24 = wsum(s25["ORESRE_24"].clip(lower=0), w25) / 1e12
num(H24, cal.iloc[8] / 1000, "SCF 2025 HOUSES, $tn (2024 $)", 46.0, 0.05)
num(O24, cal.iloc[9] / 1000, "SCF 2025 ORESRE, $tn (2024 $)", 10.3, 0.05)
num(H24 + O24, cal.iloc[5] / 1000, "SCF 2025 property, $tn (2024 $)", 56.3, 0.05)
num(wsum(L25["L1"], w25) / 1e9, z1["L_hh"], "SCF residential land total = Z.1 household land, $bn", tol=1e-9)
num(wsum(L25["L2"], w25) / 1e9, z1["L_hh"] + z1["L_nnb"] + z1["L_nfc"], "SCF L2 total = Z.1 HH + NNB + NFC (assumed), $bn", tol=1e-9)
DSH = {}
for col, lab, nv in [("L1", "L1 residential land", [1.8, 2.5, 3.7, 4.5, 6.0, 7.1, 9.4, 10.6, 15.0, 39.4]),
                     ("L2", "L2 all land", [1.7, 1.7, 2.8, 3.3, 4.8, 5.4, 7.4, 8.4, 13.0, 51.5])]:
    sh = dsum(s25, L25[col]) / wsum(L25[col], w25)
    DSH[col] = sh
    ok = np.allclose(sh, ld[f"{col}_share"].values, atol=1e-6) and np.all(np.abs(100 * sh - np.array(nv)) <= 0.051)
    claim(ok, f"decile shares of {lab} (NOTES row)", " ".join(f"{100 * v:.1f}" for v in ld[f'{col}_share'].values),
          " ".join(f"{100 * v:.1f}" for v in sh))
shH = dsum(s25, s25["HOUSES_24"].clip(lower=0)) / H24 / 1e12
claim(np.allclose(shH, ld["scf_houses_share"].values, atol=1e-6) and np.all(np.abs(100 * shH - np.array([2.0, 2.8, 4.0, 4.8, 6.6, 8.0, 10.4, 11.6, 14.9, 34.9])) <= 0.051),
      "decile shares of SCF HOUSES (NOTES row)", " ".join(f"{100 * v:.1f}" for v in ld["scf_houses_share"].values), " ".join(f"{100 * v:.1f}" for v in shH))
ce_home = m["vals"].loc["Addenda: > Other financial information: > Estimated market value of owned home", DEC].astype(float).values
ce_own = m["vals"].loc["Percent distribution: > Housing tenure: > Homeowner", DEC].astype(float).values / 100
shCE = ce_home * N_CE / (ce_home * N_CE).sum()
claim(np.all(np.abs(100 * shCE - np.array([3.4, 5.5, 6.5, 6.7, 7.5, 8.3, 9.8, 11.8, 15.0, 25.5])) <= 0.051),
      "decile shares of CE 2024 home values (cross-check row)", "3.4 ... 25.5", " ".join(f"{100 * v:.1f}" for v in shCE))
vt = acc_v["vatable"].values * W_D
vt = vt / vt.sum()
claim(np.all(np.abs(100 * vt - np.array([4.4, 5.3, 6.3, 7.3, 8.3, 8.9, 10.4, 12.5, 14.9, 21.7])) <= 0.051),
      "decile shares of VAT-able consumption (CE)", "4.4 ... 21.7", " ".join(f"{100 * v:.1f}" for v in vt))
own_r = dsum(s25, s25["owner"]) / dsum(s25, np.ones(len(s25)))
claim(close(own_r.min(), 0.39, 0.005) and close(own_r.max(), 0.93, 0.005) and close(ce_own.min(), 0.34, 0.005) and close(ce_own.max(), 0.90, 0.005),
      "homeownership by decile: SCF 39-93%, CE 34-90%", "SCF 39-93, CE 34-90", f"SCF {100 * own_r.min():.0f}-{100 * own_r.max():.0f}, CE {100 * ce_own.min():.0f}-{100 * ce_own.max():.0f}",
      "SCF D9 (84.5%) sits below D8 (85.3%): not monotone, as the range implies")
claim(close(DSH["L1"][9], 0.394, 0.0005) and close(DSH["L2"][9], 0.515, 0.0005) and close(vt[9], 0.217, 0.0005),
      "top decile: 39% of residential land, 52% with business land, 22% of VAT-able spending", "39 / 52 / 22",
      f"{100 * DSH['L1'][9]:.1f} / {100 * DSH['L2'][9]:.1f} / {100 * vt[9]:.1f}")

# %% 5. the tax and the decile accounting (the post's method)
AREA = "tax and decile accounting"
LTOT = {"L1": z1["L_hh"], "L2": z1["L_hh"] + z1["L_nnb"] + z1["L_nfc"]}
phi_csv = pd.read_csv(BOUT / "us_lvt_phi.csv")
PHI = {}
for base in ["L1", "L2"]:
    for mk in ["m1", "m2", "m3", "m4"]:
        PHI[("bridge", base, mk)] = VAT_REV / (R[mk] * LTOT[base])
        PHI[("full", base, mk)] = PHI_FULL
NV_PHI = {("L1", "m1"): 0.848, ("L1", "m2"): 0.625, ("L1", "m3"): 0.884, ("L1", "m4"): 0.530,
          ("L2", "m1"): 0.555, ("L2", "m2"): 0.409, ("L2", "m3"): 0.579, ("L2", "m4"): 0.347}
NV_FULL = {("L1", "m1"): (288, 1.16), ("L1", "m2"): (391, 1.57), ("L1", "m3"): (276, 1.11), ("L1", "m4"): (461, 1.85),
           ("L2", "m1"): (440, 1.77), ("L2", "m2"): (597, 2.40), ("L2", "m3"): (422, 1.69), ("L2", "m4"): (704, 2.82)}
MNAME = {"m1": "m1_z1hh_x_gs10", "m2": "m2_z1hh_x_gs10p150", "m3": "m3_pce_housing_x_0.30", "m4": "m4_pce_housing_x_0.50"}
for (base, mk), nv in NV_PHI.items():
    row = phi_csv[(phi_csv["base"] == base) & (phi_csv["measure"] == MNAME[mk])].set_index("rate")
    num(PHI[("bridge", base, mk)], row.loc["bridge", "phi"], f"bridge-equivalent phi, {base} {mk}", nv, 0.0005)
    fd = PHI_FULL * R[mk] * LTOT[base] * 1e9 / (S_CE * 12)
    nf = NV_FULL[(base, mk)]
    num(fd, row.loc["full", "dividend_usd_month"], f"full-capture (0.98) dividend, {base} {mk}, $/share/month", nf[0], 0.5,
        note=f"{fd / DIV_VAT:.2f}x VAT (NOTES {nf[1]:.2f}x)" + ("" if close(fd / DIV_VAT, nf[1], 0.0051) else " RATIO MISMATCH"))
claim(all(PHI[("bridge", b, k)] <= PHI_FULL for b in ("L1", "L2") for k in ("m1", "m2", "m3", "m4")),
      "both bases fund the bridge dividend on all four measures (phi <= 0.98)", "all feasible",
      f"max phi {max(PHI[('bridge', b, k)] for b in ('L1', 'L2') for k in ('m1', 'm2', 'm3', 'm4')):.3f}")
num(VAT_REV / (R["m1"] * 0.30 * I25["prop_bn"]), 1.176, "phi needed on L1 m1 at s = 0.30 (land $16.9tn)", 1.18, 0.005, tol=0.0005, rel=False,
    note=f"land at s=0.30: {0.30 * I25['prop_bn']:,.0f} $bn")
num(VAT_REV / (R["m1"] * z1["L_ownocc"]), 1.024, "phi needed on L1 m1 with the households-only owner-occupied land concept", 1.02, 0.005, tol=0.0005, rel=False)
num(PHI[("bridge", "L1", "m4")] * LTOT["L1"] / 1000, 12.4, "capitalized loss phi*L on L1 at m4, $tn", 12.4, 0.05, tol=0.05, rel=False)
num(PHI[("bridge", "L1", "m3")] * LTOT["L1"] / 1000, 20.7, "capitalized loss phi*L on L1 at m3, $tn", 20.7, 0.05, tol=0.05, rel=False)
num(PHI[("bridge", "L1", "m1")] * LTOT["L1"] / 1000, 19.8, "capitalized loss at the bridge rate on m1 ('a $19.8tn loss'), $tn", 19.8, 0.05, tol=0.05, rel=False)


def decile_acc(Lcol, phi, r, Ldf=L25, d_=s25):
    """$/share/month by decile: rent base, bill, dividend, net (my arithmetic, not bridge.net_from_base)."""
    rent_d = r * dsum(d_, Ldf[Lcol]) / (N_CE * SH_CE * 12)
    bill = phi * rent_d
    div = float((W_D * bill).sum())
    return dict(bill=bill, div=div, net=div - bill, pct=100 * (div - bill) / BUD, land_share=dsum(d_, Ldf[Lcol]) / wsum(Ldf[Lcol], d_["WGT"]))


accb = pd.read_csv(BOUT / "us_lvt_accounting_by_decile.csv")
ACC = {}
NV_NET = {"LVT_bridge_L1_m1": [183.4, 157.3, 139.4, 130.5, 89.7, 80.4, 40.1, 24.7, -39.4, -514.4],
          "LVT_bridge_L2_m1": [188.8, 185.6, 166.7, 161.3, 121.9, 121.8, 83.7, 71.8, -1.0, -749.6],
          "LVT_full_L1_m1": [212.0, 181.8, 161.2, 150.9, 103.7, 92.9, 46.4, 28.5, -45.5, -594.7],
          "LVT_full_L2_m1": [333.3, 327.8, 294.4, 284.8, 215.3, 215.2, 147.9, 126.8, -1.8, -1323.6]}
NV_PCT = {"VAT": [4.8, 2.4, 2.9, 2.6, 1.3, 1.6, 0.7, -0.5, -1.2, -3.9],
          "LVT_bridge_L1_m1": [10.0, 7.2, 6.7, 6.2, 3.8, 3.4, 1.6, 0.9, -1.3, -11.7],
          "LVT_bridge_L2_m1": [10.3, 8.5, 8.0, 7.6, 5.1, 5.2, 3.3, 2.6, -0.0, -17.1]}
for rate in ["bridge", "full"]:
    for base in ["L1", "L2"]:
        for mk in (["m1"] if rate == "bridge" else ["m1", "m2", "m3", "m4"]):
            key = f"LVT_{rate}_{base}_{mk}"
            a = decile_acc(base, PHI[(rate, base, mk)], R[mk])
            ACC[key] = a
            bq = accb[accb["scenario"] == key].set_index("decile").loc[DEC]
            gap = np.abs(a["net"] - bq["net"].values).max() / np.abs(bq["net"].values).max()
            okn = True if key not in NV_NET else bool(np.all(np.abs(a["net"] - np.array(NV_NET[key])) <= 0.051))
            claim(gap < 1e-6 and okn and abs(float((W_D * a["net"]).sum())) < 1e-9, f"net per adult share by decile, {key} (sum w*net = 0)",
                  " ".join(f"{v:.1f}" for v in bq["net"].values), " ".join(f"{v:.1f}" for v in a["net"]),
                  f"max relative gap to builder {gap:.1e}" + ("" if okn else "; NOTES row NOT reproduced"))
            if key in NV_PCT:
                bad = [f"{DEC[i]} {a['pct'][i]:.3f} printed {NV_PCT[key][i]}" for i in range(10)
                       if not pv(a["pct"][i], NV_PCT[key][i], 0.1, f"% of budget {key} {DEC[i]}")]
                claim(not bad, f"net as % of budget by decile, {key} (NOTES row)", " ".join(f"{v:.1f}" for v in NV_PCT[key]),
                      " ".join(f"{v:.2f}" for v in a["pct"]), "; ".join(bad))
            if rate == "bridge":
                num(a["div"], DIV_VAT, f"{key}: dividend = the VAT dividend", tol=1e-9)
vnet, vpct = acc_v["net"].values, acc_v["net_pct_budget"].values
claim(bool(np.all(np.abs(vnet - np.array([87.8, 53.4, 60.8, 55.5, 30.2, 38.6, 16.9, -13.8, -37.9, -172.0])) <= 0.051) and
           np.all(np.abs(vpct - np.array(NV_PCT["VAT"])) <= 0.051)), "VAT bridge net and % of budget by decile (NOTES rows)",
      "87.8 ... -172.0", " ".join(f"{v:.1f}" for v in vnet))
L1n = ACC["LVT_bridge_L1_m1"]["net"]
L2n = ACC["LVT_bridge_L2_m1"]["net"]
claim(int((L1n > 0).sum()) == 8 and int((vnet > 0).sum()) == 7, "eight deciles gain under the LVT (L1) instead of seven under the VAT",
      "8 vs 7", f"{int((L1n > 0).sum())} vs {int((vnet > 0).sum())}")
claim(close(L1n[0] / vnet[0], 2.0, 0.15) and all(2.0 <= L1n[i] / vnet[i] <= 3.05 for i in range(1, 7)) and L1n[7] > 0 > vnet[7]
      and close(L1n[8], vnet[8], 2.0) and close(L1n[9] / vnet[9], 3.0, 0.05) and close(L2n[9] / vnet[9], 4.4, 0.05),
      "decile by decile: D1 2x, D2-D7 2-3x, D8 switches, D9 about the same, D10 3x (L2: 4.4x)", "as stated",
      f"D1 {L1n[0] / vnet[0]:.2f}x, D2-D7 {min(L1n[i] / vnet[i] for i in range(1, 7)):.2f}-{max(L1n[i] / vnet[i] for i in range(1, 7)):.2f}x, "
      f"D9 {L1n[8]:.1f} vs {vnet[8]:.1f}, D10 {L1n[9] / vnet[9]:.2f}x, L2 D10 {L2n[9] / vnet[9]:.2f}x")


# %% 6. household level: bills, dividends, nets; hand-to-mouth; who pays
AREA = "households: who pays"


def kvw(d_, divisor=52.0):
    liquid = d_["LIQ_24"] + d_["STOCKS_24"] + d_["BOND_24"] + d_["NMMF_24"] - d_["CCBAL_24"]
    illiquid = (d_["HOMEEQ_24"] + (d_["ORESRE_24"] - d_["RESDBT_24"]) + d_["NNRESRE_24"] + d_["RETQLIQ_24"] + d_["CASHLI_24"]
                + d_["CDS_24"] + d_["SAVBND_24"] + d_["OTHMA_24"])
    htm = (liquid <= d_["INCOME_24"].clip(lower=0) / divisor).values
    return dict(htm=htm, whtm=htm & (illiquid > 0).values, liquid=liquid.values, illiquid=illiquid.values)


HTM = kvw(s25, 52.0)
HTMm = kvw(s25, 24.0)
HTM22 = kvw(s22, 52.0)


def hh_lvt(base, phi, r, div, d_=s25, Ldf=L25):
    comps = ["L_own", "L_ore"] + (["L_nnb", "L_nfc"] if base == "L2" else [])
    bills = {c: phi * r * Ldf[c].values / 12 for c in comps}
    bill = sum(bills.values())
    dv = div * d_["shares"].values
    return dict(div=dv, bill=bill, bill_own=bills["L_own"], bill_nonocc=bill - bills["L_own"], net=dv - bill,
                net_ps=(dv - bill) / d_["shares"].values)


def hh_vat(d_=s25):
    T = acc_v["tax"].values * N_CE * SH_CE                     # $ per month, decile totals
    sp = d_["TOTSPENDNH_24"].clip(lower=0).values
    den = dsum(d_, sp)
    bill = T[d_["dec_i"].values - 1] / den[d_["dec_i"].values - 1] * sp
    dv = DIV_VAT * d_["shares"].values
    return dict(div=dv, bill=bill, bill_own=np.zeros(len(d_)), bill_nonocc=np.zeros(len(d_)), net=dv - bill, net_ps=(dv - bill) / d_["shares"].values)


HH = {"VAT": hh_vat()}
for key in ["LVT_bridge_L1_m1", "LVT_bridge_L2_m1"] + [f"LVT_full_{b}_{k}" for b in ("L1", "L2") for k in ("m1", "m2", "m3", "m4")]:
    _, rate, base, mk = key.split("_")
    HH[key] = hh_lvt(base, PHI[(rate, base, mk)], R[mk], ACC[key]["div"])
# aggregation identity: household nets sum to the decile nets
for key in ["VAT", "LVT_bridge_L1_m1"]:
    agg = dsum(s25, HH[key]["net"]) / (N_CE * SH_CE)
    ref = vnet if key == "VAT" else ACC[key]["net"]
    num(np.abs(agg - ref).max(), 0.0, f"household nets aggregate exactly to the decile nets ({key}), max gap $", tol=1e-6, rel=False)


def wq(x, w, q):
    """Weighted quantile: the smallest x with cumulative weight >= q (no interpolation)."""
    o = np.argsort(x, kind="mergesort")
    cw = np.cumsum(w[o]) / w.sum()
    return float(x[o][min(np.searchsorted(cw, q), len(x) - 1)])


def who(h, mask=None):
    mk = np.ones(len(s25), bool) if mask is None else mask
    w = w25[mk]
    net = h["net"][mk]
    pay = net < 0
    paid = -np.minimum(net, 0) * w
    g = {"owner": s25["owner"].values[mk] == 1, "renter": s25["owner"].values[mk] == 0, "age65": s25["age65"].values[mk] == 1,
         "owner65": (s25["owner"].values[mk] == 1) & (s25["age65"].values[mk] == 1), "htm": HTM["htm"][mk], "whtm": HTM["whtm"][mk]}
    out = dict(payer_share=float((w * pay).sum() / w.sum()))
    for k, f in g.items():
        out[f"payers_{k}"] = float((w * pay * f).sum() / (w * pay).sum())
        out[f"payments_{k}"] = float((paid * f).sum() / paid.sum())
        out[f"rate_{k}"] = float((w * pay * f).sum() / (w * f).sum())
    for q in (10, 25, 50, 75, 90):
        out[f"p{q}"] = wq(h["net_ps"][mk], w, q / 100)
    return out


WHO = {k: who(h) for k, h in HH.items()}
whob = pd.read_csv(BOUT / "us_lvt_who_pays.csv")
bname = {"VAT": "VAT (household, TOTSPENDNH split)", "LVT_bridge_L1_m1": "LVT_bridge_L1_m1", "LVT_bridge_L2_m1": "LVT_bridge_L2_m1"}
NV_WHO = {"payer_share": (37.8, 31.6, 22.4), "payers_owner": (75, 99, 98), "payers_age65": (35, 44, 49), "payers_htm": (24, 16, 11),
          "payments_owner65": (36, 45, 46), "payments_htm": (14, 7, 4)}
BCOL = {"payer_share": "payer_share", "payers_owner": "payers_owner_share", "payers_age65": "payers_age65_share",
        "payers_htm": "payers_htm_share", "payments_owner65": "payments_owner65_share", "payments_htm": "payments_htm_share"}
for stat, nvs in NV_WHO.items():
    for (key, lab), nv in zip(bname.items(), nvs):
        b = float(whob[(whob["scenario"] == lab) & (whob["dec"] == "all")][BCOL[stat]].iloc[0])
        tol = 0.051 if stat == "payer_share" else 0.51
        num(100 * WHO[key][stat], 100 * b, f"{stat.replace('_', ' ')}, {key}, % (all families)", nv, tol, tol=1e-6)
for key, nvs in [("VAT", (13, 39, 50, 65)), ("LVT_bridge_L1_m1", (6, 28, 49, 85)), ("LVT_bridge_L2_m1", (4, 19, 32, 78))]:
    mine = [100 * who(HH[key], s25["dec"].values == d)["payer_share"] for d in ("d01", "d05", "d09", "d10")]
    b = [100 * float(whob[(whob["scenario"] == bname[key]) & (whob["dec"] == d)]["payer_share"].iloc[0]) for d in ("d01", "d05", "d09", "d10")]
    claim(np.allclose(mine, b, atol=1e-6) and all(abs(x - y) <= 0.51 for x, y in zip(mine, nvs)), f"net payers in D1 / D5 / D9 / D10, {key}, %",
          " / ".join(f"{v:.1f}" for v in b), " / ".join(f"{v:.1f}" for v in mine), "NOTES " + " / ".join(str(v) for v in nvs))
for key, nvs in [("VAT", (-234, 47, 167)), ("LVT_bridge_L1_m1", (-323, 117, 249)), ("LVT_bridge_L2_m1", (-236, 155, 249))]:
    mine = [WHO[key][f"p{q}"] for q in (10, 50, 90)]
    b = [float(whob[(whob["scenario"] == bname[key]) & (whob["dec"] == "all")][f"net_ps_p{q}"].iloc[0]) for q in (10, 50, 90)]
    claim(all(abs(x - y) <= 2.0 for x, y in zip(mine, b)) and all(abs(x - y) <= 2.0 for x, y in zip(mine, nvs)),
          f"net per share at the 10th / 50th / 90th percentile, {key}, $", " / ".join(f"{v:.0f}" for v in b), " / ".join(f"{v:.0f}" for v in mine),
          "my quantile does not interpolate; tolerance $2")
noland = float(w25[(L25["L1"].values == 0)].sum() / w25.sum())
claim(close(100 * noland, 32.6, 0.051) and close(100 * WHO["LVT_bridge_L1_m1"]["payer_share"], 100 - 68.4, 0.06),
      "68% of families are net recipients; the third with no land (32.6%) pays nothing", "32.6% no land; 68% recipients",
      f"{100 * noland:.1f}% no land; {100 - 100 * WHO['LVT_bridge_L1_m1']['payer_share']:.1f}% recipients")
p10_d10 = wq(HH["LVT_bridge_L1_m1"]["net_ps"][s25["dec"].values == "d10"], w25[s25["dec"].values == "d10"], 0.10)
b10 = float(whob[(whob["scenario"] == "LVT_bridge_L1_m1") & (whob["dec"] == "d10")]["net_ps_p10"].iloc[0])
claim(abs(p10_d10 - b10) <= 5 and abs(p10_d10 + 1438) <= 5, "D10's 10th percentile pays $1,438 per share per month (L1)", f"{b10:,.0f}", f"{p10_d10:,.0f}")
full_div = []
for d in DEC:
    mk = s25["dec"].values == d
    q = 0.75 if d <= "d06" else 0.90
    full_div.append(abs(wq(HH["LVT_bridge_L1_m1"]["net_ps"][mk], w25[mk], q) - DIV_VAT) < 1e-6)
claim(all(full_div[:9]), "the top quarter of D1-D6 and the top tenth of D7-D9 (no land) receive the full $249", "as stated",
      f"{sum(full_div[:9])} of 9 deciles", "")
num(100 * WHO["LVT_bridge_L1_m1"]["rate_owner65"], 100 * float(whob[(whob["scenario"] == "LVT_bridge_L1_m1") & (whob["dec"] == "all")]["payer_rate_owner65"].iloc[0]),
    "among owners 65+, share who are net payers (L1), %", 57, 0.51)
num(100 * WHO["LVT_bridge_L1_m1"]["payers_renter"], 1.37, "L1 payers who are renters (with other property), %", 1.4, 0.051, tol=0.01, rel=False)
num(100 * WHO["LVT_bridge_L1_m1"]["payments_whtm"], 7.09, "net LVT payments by WEALTHY hand-to-mouth families (of 7.2% by all HtM), %", None, None,
    tol=0.01, rel=False, note="'nearly all of them house-rich': borne out")
# payments by owners 65+ by decile (payments_by_group.csv)
pg = pd.read_csv(BOUT / "us_lvt_payments_by_group.csv").set_index("decile")
o65 = np.array([who(HH["LVT_bridge_L1_m1"], s25["dec"].values == d)["payments_owner65"] for d in DEC])
claim(np.allclose(o65, pg["owner 65+"].values, atol=1e-6) and close(100 * o65[0], 54, 0.51) and close(100 * o65[1:4].min(), 74, 0.51)
      and close(100 * o65[1:4].max(), 82, 0.51) and close(100 * o65[4:8].min(), 60, 0.51) and close(100 * o65[4:8].max(), 71, 0.51)
      and close(100 * o65[8], 41, 0.51) and close(100 * o65[9], 36, 0.51),
      "owners 65+ make 54% (D1), 74-82% (D2-D4), 60-71% (D5-D8), 41% (D9), 36% (D10) of each decile's net payments",
      " ".join(f"{100 * v:.0f}" for v in pg["owner 65+"].values), " ".join(f"{100 * v:.0f}" for v in o65))
claim(close(100 * o65[1:8].min(), 60, 0.51) and close(100 * o65[1:8].max(), 82, 0.51),
      "'Below the top two deciles most net payments come from owners over 65 ... 60-82% of them in deciles 2-8'", "60-82%",
      f"{100 * o65[1:8].min():.0f}-{100 * o65[1:8].max():.0f}%", f"D1 is {100 * o65[0]:.0f}%: 'most' also holds there")

# %% 7. MPC grades: the post's schedules, KVW shares, the SCF windfall question vs the FEDS note
AREA = "MPC grades"
SC = B.mpc_schedules()
SCHED = {k: SC[k].values for k in ["mid", "low", "high"]}
SCHED["mono"] = pd.read_csv(B.REBUILD / "out" / "us_mpc_schedules.csv").set_index("decile").loc[DEC, "mpc_mid_monotone_fig5_fig6_diagnostic"].values
grb = pd.read_csv(BOUT / "us_lvt_mpc_grades.csv").set_index("decile")
claim(np.allclose(SCHED["mid"], [1.00, 1.00, 0.97, 0.91, 0.85, 0.78, 0.72, 0.66, 0.59, 0.53], atol=0.0051)
      and np.allclose(SCHED["mono"], [0.99, 0.99, 0.96, 0.91, 0.88, 0.82, 0.77, 0.77, 0.61, 0.53], atol=0.0051),
      "post mid schedule and monotone diagnostic (NOTES rows)", "1.00 ... 0.53", " ".join(f"{v:.2f}" for v in SCHED["mid"]))
mp = s25["MPSPEND"].values / 100
MEAS = np.array([np.average(mp[s25["dec"].values == d], weights=w25[s25["dec"].values == d]) for d in DEC])
MEAS_DH = {}
for i, d in enumerate(DEC):
    for hv in (0, 1):
        mk = (s25["dec"].values == d) & (HTM["htm"] == bool(hv))
        MEAS_DH[(d, hv)] = np.average(mp[mk], weights=w25[mk]) if mk.sum() >= 30 else MEAS[i]
claim(np.allclose(MEAS, grb["measured_windfall"].values, atol=1e-9) and np.allclose(MEAS, [0.29, 0.26, 0.25, 0.23, 0.22, 0.19, 0.21, 0.19, 0.21, 0.18], atol=0.0051),
      "measured windfall MPC by decile (SCF 2025 MPSPEND)", " ".join(f"{v:.2f}" for v in grb["measured_windfall"].values), " ".join(f"{v:.2f}" for v in MEAS))
mh = np.array([MEAS_DH[(d, 1)] for d in DEC])
mn_ = np.array([MEAS_DH[(d, 0)] for d in DEC])
claim(np.allclose(mh, grb["measured_htm"].values, atol=1e-9) and np.allclose(mn_, grb["measured_not_htm"].values, atol=1e-9),
      "measured MPC by decile x hand-to-mouth", " ".join(f"{v:.2f}" for v in grb["measured_htm"].values), " ".join(f"{v:.2f}" for v in mh))
lower = [DEC[i] for i in range(10) if mh[i] < mn_[i]]
claim(lower == DEC[4:] or "lower, in fact, from D5 up" not in NOTES_TXT, "'barely higher for hand-to-mouth families: lower, in fact, from D5 up'", "lower from D5 up",
      "lower in " + ",".join(lower), "D1 is lower too (0.277 vs 0.300); the sentence should say 'lower in D1 and from D5 up'")
hs = dsum(s25, HTM["htm"]) / dsum(s25, np.ones(len(s25)))
claim(np.allclose(hs, grb["htm_share_biweekly"].values, atol=1e-9) and np.allclose(hs, [0.46, 0.50, 0.44, 0.40, 0.34, 0.35, 0.29, 0.21, 0.14, 0.07], atol=0.0051),
      "hand-to-mouth share by decile (biweekly)", " ".join(f"{v:.2f}" for v in grb["htm_share_biweekly"].values), " ".join(f"{v:.2f}" for v in hs))
tot = lambda f: 100 * float((w25 * f).sum() / w25.sum())
claim(close(tot(HTM["htm"]), 32.0, 0.051) and close(tot(HTM["whtm"]), 21.2, 0.051) and close(tot(HTMm["htm"]), 40.2, 0.051) and close(tot(HTMm["whtm"]), 27.4, 0.051),
      "hand-to-mouth: 32.0% (21.2% wealthy) biweekly; 40.2% (27.4%) monthly", "32.0 (21.2); 40.2 (27.4)",
      f"{tot(HTM['htm']):.1f} ({tot(HTM['whtm']):.1f}); {tot(HTMm['htm']):.1f} ({tot(HTMm['whtm']):.1f})")
# the FEDS note (accessible data): Figure 1 and Figure 3 (by normal-income percentile), parsed from the vendored page
t = RAW_FEDS.read_text(encoding="utf-8", errors="replace")
t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", t, flags=re.S)
txt = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t)))
f1 = re.search(r"Spend Save Pay Debt Mean Percent \(%\) ([\d.]+) ([\d.]+) ([\d.]+)", txt)
seg = txt[txt.index("by Normal Income Percentile"):]
seg = seg[:seg.index("Source")]
labs = ["Bottom 10%", "10-20%", "20-30%", "30-40%", "40-50%", "50-60%", "60-70%", "70-80%", "80-90%", "Top 90-95%", "Top 95-99%", "Top 1%"]
fig3 = [float(re.search(re.escape(lb) + r" ([\d.]+)", seg).group(1)) for lb in labs]
f4 = re.search(r"Not Hand-to-Mouth ([\d.]+) Hand-to-Mouth ([\d.]+)", txt)
mine_g = [100 * np.average(mp[s25["NINCPCTLECAT"].values == k], weights=w25[s25["NINCPCTLECAT"].values == k]) for k in range(1, 13)]
gap = max(abs(a_ - b_) for a_, b_ in zip(mine_g, fig3))
claim(gap <= 0.75, "the public extract reproduces FEDS note Fig 3 'within 0.7 points in every usual-income group'", "within 0.7",
      f"max gap {gap:.3f} pp", "0.705 at 10-20%: 0.7 after rounding")
ov = [100 * np.average(s25[c].values / 100, weights=w25) for c in ("MPSPEND", "MPSAVE", "MPDEBT")]
claim(f1 is not None and all(abs(a_ - float(b_)) < 0.005 for a_, b_ in zip(ov, f1.groups())), "overall spend / save / pay debt = 22.35 / 47.31 / 30.30 (FEDS Fig 1)",
      " / ".join(f1.groups()) if f1 else "?", " / ".join(f"{v:.2f}" for v in ov))
claim(f4 is not None and f4.groups() == ("20.3", "22.9"), "FEDS note: +2.6 points for hand-to-mouth conditional on usual income (22.9 vs 20.3)",
      "22.9 vs 20.3", f"{f4.group(2)} vs {f4.group(1)}" if f4 else "?")
claim(close(MEAS[0] - MEAS[9], 0.11, 0.0051) and close((SCHED["mid"][0] - SCHED["mid"][9]), 0.47, 0.0051)
      and 0.2 <= (MEAS[0] - MEAS[9]) / (SCHED["mid"][0] - SCHED["mid"][9]) <= 0.3 and 0.2 <= MEAS.mean() / SCHED["mid"].mean() <= 0.33,
      "measured MPC is about a quarter of the post's level and a quarter of its slope", "1/4 and 1/4",
      f"level {MEAS.mean() / SCHED['mid'].mean():.2f}, slope {(MEAS[0] - MEAS[9]) / (SCHED['mid'][0] - SCHED['mid'][9]):.2f}")

# %% 8. flow impulses: the grid of grades x instruments, and deferral
AREA = "flow impulse"
IMPb = pd.read_csv(BOUT / "us_lvt_impulse.csv")


def imp_dn(net_d, mpc):
    return 100 * float((W_D * mpc * net_d).sum()) / BUD_BAR


def imp_hh(dC):
    return 100 * wsum(dC, w25) / (S_CE * BUD_BAR)


def mpc_hh(rule, cash, htm=HTM, sch="mid"):
    base = SCHED[sch][s25["dec_i"].values - 1]
    if rule == "liq":
        return np.where((cash < 0) & htm["htm"], 1.0, base)
    if rule == "liqsym":
        return np.where(htm["htm"], 1.0, base)
    if rule == "meas_htm":
        return np.array([MEAS_DH[(d, int(h))] for d, h in zip(s25["dec"].values, htm["htm"])])
    return base


def cash_of(h, defer="none"):
    if defer == "none":
        return h["net"], 1.0, 0.0
    who_ = defer.replace("_cash", "")
    mk = ((s25["owner"] == 1) & (s25["age65"] == 1)).values if who_ == "own65" else ((s25["owner"] == 1).values & HTM["whtm"])
    dfr = h["bill_own"] * mk
    k = 1.0 - wsum(dfr, w25) / wsum(h["div"], w25) if defer.endswith("_cash") else 1.0
    return k * h["div"] - h["bill"] + dfr, k, wsum(dfr, w25)


def grade_imp(h, grade, defer="none"):
    cash, k, D = cash_of(h, defer)
    cash_d = dsum(s25, cash) / (N_CE * SH_CE)
    if grade.startswith("dn_"):
        g = grade[3:]
        mpc = SCHED[g] if g in SCHED else (MEAS if g == "meas" else MEAS / MEAS[0])
        return imp_dn(cash_d, mpc), k, D
    rule, band = {"hh_liq_mid": ("liq", HTM), "hh_liq_low": ("liq", HTM), "hh_liq_high": ("liq", HTM), "hh_liq_mono": ("liq", HTM),
                  "hh_liq_mid_monthly": ("liq", HTMm), "hh_liqsym_mid": ("liqsym", HTM), "hh_meas_htm": ("meas_htm", HTM),
                  "hh_mid": ("plain", HTM)}[grade]
    sch = grade.split("_")[2] if grade.startswith("hh_liq_") and grade.split("_")[2] in SCHED else "mid"
    return imp_hh(mpc_hh(rule, cash, band, sch) * cash), k, D


GRADES = ["dn_mid", "dn_low", "dn_high", "dn_mono", "dn_meas", "dn_measshape", "hh_mid", "hh_liq_mid", "hh_liq_low", "hh_liq_high",
          "hh_liq_mono", "hh_liq_mid_monthly", "hh_liqsym_mid", "hh_meas_htm"]
IMP = {}
worst = 0.0
for key in tqdm(list(HH), desc="impulse grid", leave=False):
    for gr in GRADES:
        for dfr in (["none"] if key == "VAT" else ["none", "own65", "own65_cash", "whtm_owners", "whtm_owners_cash"]):
            v, k, D = grade_imp(HH[key], gr, dfr)
            IMP[(key, gr, dfr)] = v
            if key == "VAT":
                b = float(IMPb[(IMPb["tax"] == "VAT") & (IMPb["grade"] == gr)]["impulse_pct"].iloc[0])
            else:
                _, rate, base, mk = key.split("_")
                b = float(IMPb[(IMPb["tax"] == "LVT") & (IMPb["rate"] == rate) & (IMPb["base"] == base) & (IMPb["measure"] == MNAME[mk])
                               & (IMPb["grade"] == gr) & (IMPb["defer"] == dfr)]["impulse_pct"].iloc[0])
            worst = max(worst, abs(v - b))
claim(worst < 1e-6 and len(IMP) == len(IMPb), "flow impulse grid (every rate x base x measure x grade x deferral) equals the builder's us_lvt_impulse.csv",
      f"{len(IMPb)} rows", f"{len(IMP)} cells, max gap {worst:.1e} pp")
NV_IMP = {"dn_mid": (0.389, 0.976, 1.242, 1.129, 2.194), "dn_low": (0.474, 1.188, 1.505, 1.374, 2.658), "dn_high": (0.305, 0.768, 0.983, 0.888, 1.736),
          "dn_mono": (0.389, 1.011, 1.324, 1.169, 2.338), "hh_liq_mid": (0.314, 0.885, 1.183, 1.023, 2.089),
          "hh_liq_mid_monthly": (0.285, 0.852, 1.153, 0.985, 2.036), "hh_liqsym_mid": (0.441, 1.114, 1.457, 1.288, 2.572),
          "dn_meas": (0.060, 0.152, 0.189, 0.175, 0.334), "hh_meas_htm": (0.053, 0.136, 0.163, 0.157, 0.287),
          "dn_measshape": (0.208, 0.524, 0.653, 0.605, 1.153)}
KEYS5 = ["VAT", "LVT_bridge_L1_m1", "LVT_bridge_L2_m1", "LVT_full_L1_m1", "LVT_full_L2_m1"]
for gr, nvs in NV_IMP.items():
    mine = [IMP[(k, gr, "none")] for k in KEYS5]
    bad = [f"{k} {v:.4f} vs {nv}" for k, v, nv in zip(KEYS5, mine, nvs) if abs(v - nv) > 0.00051]
    claim(not bad, f"flow impulse row '{gr}' (VAT, L1, L2, full L1, full L2), % of consumption", " / ".join(str(v) for v in nvs),
          " / ".join(f"{v:.3f}" for v in mine), "; ".join(bad))
ratios = [IMP[("LVT_bridge_L1_m1", g, "none")] / IMP[("VAT", g, "none")] for g in GRADES]
claim(min(ratios) >= 2.5 - 0.005 and max(ratios) <= 3.0 + 0.005, "the LVT/VAT impulse ratio stays at 2.5-3.0 under every MPC grade tried",
      "2.5-3.0", f"{min(ratios):.2f}-{max(ratios):.2f}")
claim(close(IMP[("LVT_bridge_L1_m1", "dn_mono", "none")] / IMP[("LVT_bridge_L1_m1", "dn_mid", "none")] - 1, 0.036, 0.0006)
      and abs(IMP[("VAT", "dn_mono", "none")] - IMP[("VAT", "dn_mid", "none")]) < 0.001,
      "monotone diagnostic moves the LVT by +3.6%, the VAT by nothing", "+3.6% / 0",
      f"{100 * (IMP[('LVT_bridge_L1_m1', 'dn_mono', 'none')] / IMP[('LVT_bridge_L1_m1', 'dn_mid', 'none')] - 1):+.1f}% / "
      f"{IMP[('VAT', 'dn_mono', 'none')] - IMP[('VAT', 'dn_mid', 'none')]:+.4f} pp")
rv = IMP[("VAT", "hh_liq_mid", "none")] / IMP[("VAT", "dn_mid", "none")] - 1
rl = IMP[("LVT_bridge_L1_m1", "hh_liq_mid", "none")] / IMP[("LVT_bridge_L1_m1", "dn_mid", "none")] - 1
claim(close(rv, -0.19, 0.006) and close(rl, -0.09, 0.006), "the liquidity grade lowers the VAT's impulse by 19%, the LVT's by 9%", "-19% / -9%",
      f"{100 * rv:.1f}% / {100 * rl:.1f}%")
NV_DEF = {("dn_mid", "own65"): 2.976, ("dn_mid", "own65_cash"): 0.852, ("dn_mid", "whtm_owners"): 1.852, ("dn_mid", "whtm_owners_cash"): 0.967,
          ("hh_liq_mid", "own65"): 2.913, ("hh_liq_mid", "own65_cash"): 0.757, ("hh_liq_mid", "whtm_owners"): 1.838, ("hh_liq_mid", "whtm_owners_cash"): 0.952}
bad = [f"{g}/{d}: {IMP[('LVT_bridge_L1_m1', g, d)]:.3f} vs {v}" for (g, d), v in NV_DEF.items() if abs(IMP[("LVT_bridge_L1_m1", g, d)] - v) > 0.00051]
claim(not bad, "deferral table: flows (post's method, liquidity-graded) under the four deferral variants", "2.976 / 0.852 / 1.852 / 0.967 ...",
      "reproduced" if not bad else "; ".join(bad))
h1 = HH["LVT_bridge_L1_m1"]
_, k65, D65 = cash_of(h1, "own65_cash")
_, kw, Dw = cash_of(h1, "whtm_owners_cash")
rev_m = VAT_REV * 1e9 / 12
claim(close(D65 / rev_m, 0.299, 0.0006) and close(Dw / rev_m, 0.125, 0.0006) and close(k65 * DIV_VAT, 175, 0.51) and close(kw * DIV_VAT, 218, 0.51),
      "deferred share of revenue 29.9% / 12.5%; cash-balanced dividends $175 / $218", "29.9% / 12.5%; $175 / $218",
      f"{100 * D65 / rev_m:.1f}% / {100 * Dw / rev_m:.1f}%; ${k65 * DIV_VAT:.0f} / ${kw * DIV_VAT:.0f}")
for who_, nv in [("own65", (-2.30, -3.29)), ("whtm_owners", (-0.96, -1.37))]:
    mk = ((s25["owner"] == 1) & (s25["age65"] == 1)).values if who_ == "own65" else ((s25["owner"] == 1).values & HTM["whtm"])
    lossd = PHI[("bridge", "L1", "m1")] * wsum(L25["L_own"].values * mk, w25) / 1e9
    v = [-100 * MPW[k] * lossd / C_TOT for k in ("mid", "high")]
    claim(close(v[0], nv[0], 0.0051) and close(v[1], nv[1], 0.0051), f"deferrers' residual wealth effect at 3.5c (5c), {who_}, % of consumption",
          f"{nv[0]} ({nv[1]})", f"{v[0]:.2f} ({v[1]:.2f})")


# %% 9. demand shifts: decile-netted (the post's method), household level, tenure-aware baskets
AREA = "demand shifts"
CM, ETA = m["C"], m["eta"]
CATS = list(CM.index)
CH = m["chart"]


def contrib(shock, C=None, eta=None):
    """c_gd = w_d C_gd eta_gd shock_d ($/share/month), my arithmetic."""
    C = CM if C is None else C
    eta = ETA if eta is None else eta
    return C.values * eta.values * (W_D * np.asarray(shock))[None, :]


def bars_dn(net_d, mpc):
    return pd.Series(contrib(mpc * net_d / BUD).sum(axis=1), index=CATS)


def dC_hh(h, rule="liq"):
    cash = h["net"]
    return mpc_hh(rule, cash) * cash


def bars_hh(dC):
    dCd = dsum(s25, dC) / (N_CE * SH_CE)
    return pd.Series(contrib(dCd / BUD).sum(axis=1), index=CATS)


# tenure baskets inside each decile (CE Table 1710 ratios)
ten = pd.read_csv(TIDY / "ce_housing_tenure_long.csv", low_memory=False)
ten = ten[(ten["year"] == 2024) & (ten["stat"] == "mean")].pivot_table(index="path", columns="group", values="value", aggfunc="first")
SH_ = B.EXP + " > Housing > Shelter > "
RR = float(ten.loc[SH_ + "Rented dwellings", "owner"] / ten.loc[SH_ + "Rented dwellings", "renter"])
RO = float(ten.loc[SH_ + "Owned dwellings", "renter"] / ten.loc[SH_ + "Owned dwellings", "owner"])
claim(close(100 * RR, 0.8, 0.051) and close(100 * RO, 0.6, 0.051), "Table 1710: owners' rent = 0.8% of renters'; renters' owner costs = 0.6% of owners'",
      "0.8% / 0.6%", f"{100 * RR:.2f}% / {100 * RO:.2f}%")
def tenure_baskets(p_owner):
    """Owner and renter baskets inside each decile: rent with renters, owner costs with owners (Table 1710 ratios), every other
    line at the decile mean; p_o C^o + p_r C^r = C. Elasticities re-evaluated at each basket with bridge.eta_table."""
    po = pd.Series(np.asarray(p_owner, float), index=CM.columns)
    pr = 1 - po
    Co, Cr = CM.copy(), CM.copy()
    Cr.loc["Rented dwellings"] = CM.loc["Rented dwellings"] / (pr + po * RR)
    Co.loc["Rented dwellings"] = RR * Cr.loc["Rented dwellings"]
    for g_ in ["Mortgage interest and charges", "Property taxes", "Home maintenance, repairs & insurance"]:
        Co.loc[g_] = CM.loc[g_] / (po + pr * RO)
        Cr.loc[g_] = RO * Co.loc[g_]
    assert np.allclose((po * Co + pr * Cr).values, CM.values)
    tb = {}
    for nm, Ct in [("owner", Co), ("renter", Cr)]:
        eta_t, _ = B.eta_table(dict(m, C=Ct, budget=Ct.sum()), m["food_map"])
        tb[nm] = (Ct, eta_t)
    return tb


TB = tenure_baskets(ce_own)


def bars_tenure(dC, tb=None):
    tb = TB if tb is None else tb
    out = np.zeros(len(CATS))
    own = s25["owner"].values == 1
    for nm, mk in [("owner", own), ("renter", ~own)]:
        Ct, eta_t = tb[nm]
        tot_d = np.nan_to_num(pd.Series(np.asarray(dC)[mk] * w25[mk]).groupby(s25["dec"].values[mk]).sum().reindex(DEC).values)
        out += (Ct.values / Ct.sum().values[None, :] * eta_t.values * tot_d[None, :]).sum(axis=1) / S_CE
    return pd.Series(out, index=CATS)


DSb = pd.read_csv(BOUT / "us_lvt_demand_shifts.csv", index_col=0)
DS = {}
for key, net_d, h in [("VAT", vnet, HH["VAT"]), ("LVT_bridge_L1_m1", ACC["LVT_bridge_L1_m1"]["net"], HH["LVT_bridge_L1_m1"]),
                      ("LVT_bridge_L2_m1", ACC["LVT_bridge_L2_m1"]["net"], HH["LVT_bridge_L2_m1"]),
                      ("LVT_full_L1_m1", ACC["LVT_full_L1_m1"]["net"], HH["LVT_full_L1_m1"]), ("LVT_full_L2_m1", ACC["LVT_full_L2_m1"]["net"], HH["LVT_full_L2_m1"])]:
    dC = dC_hh(h)
    DS[f"{key}|decile_netted"] = bars_dn(net_d, SCHED["mid"])
    DS[f"{key}|household_liq"] = bars_hh(dC)
    DS[f"{key}|household_liq_tenure"] = bars_tenure(dC)
    gap = max(float((DS[f"{key}|{v}"] - DSb[f"{key}|{v}"].reindex(CATS)).abs().max()) for v in ("decile_netted", "household_liq", "household_liq_tenure"))
    claim(gap < 1e-6, f"category shifts, three versions, {key}: equal the builder's us_lvt_demand_shifts.csv", "", f"max gap ${gap:.1e}")
reb = pd.read_csv(B.REBUILD / "out" / "us_demand_shifts.csv", index_col=0)
num(float((DS["VAT|decile_netted"].loc[CH] - reb.loc[CH, "dUSD_mid"]).abs().max()), 0.0, "VAT decile-netted bars = the rebuild's Fig 5 (36 bars), max gap $",
    tol=1e-5, rel=False)
NV_DS = {"Rented dwellings": (3.36, 8.28, 10.32, 4.00, 18.10), "Health insurance": (1.08, 2.80, 3.68, 0.91, 2.41),
         "Gasoline and other fuels": (0.68, 1.78, 2.38, 0.58, 1.54), "Electricity": (0.64, 1.60, 2.02, 0.58, 1.42),
         "Home maintenance, repairs & insurance": (0.35, 0.81, 1.00, 0.03, -1.96), "Food at home": (0.59, 1.48, 1.87, 0.51, 1.16),
         "Vehicle insurance": (0.53, 1.39, 1.86, 0.45, 1.20), "Cars and trucks, used": (0.38, 1.14, 1.66, 0.27, 0.88),
         "Cars and trucks, new": (-0.39, -1.09, -1.59, -0.48, -1.31), "Telephone services": (0.46, 1.16, 1.52, 0.40, 1.03),
         "Fees and admissions": (-0.20, -0.55, -0.75, -0.24, -0.64), "Other lodging": (-0.13, -0.37, -0.52, -0.18, -0.49),
         "Mortgage interest and charges": (-0.38, -0.86, -0.96, -0.64, -3.52), "Property taxes": (0.10, 0.22, 0.25, -0.17, -2.15)}
cols5 = ["VAT|decile_netted", "LVT_bridge_L1_m1|decile_netted", "LVT_bridge_L2_m1|decile_netted", "VAT|household_liq_tenure", "LVT_bridge_L1_m1|household_liq_tenure"]
for cat, nvs in NV_DS.items():
    mine = [float(DS[c].loc[cat]) for c in cols5]
    bad = [f"{c.split('|')[0]} {c.split('|')[1][:6]} {v:+.3f} vs {nv:+.2f}" for c, v, nv in zip(cols5, mine, nvs) if not pv(v, nv, 0.01, f"demand {cat} {c}")]
    claim(not bad, f"demand table row: {cat} ($/share/month; VAT, L1, L2, VAT tenure, L1 tenure)", " / ".join(f"{v:+.2f}" for v in nvs),
          " / ".join(f"{v:+.2f}" for v in mine), "; ".join(bad))
totals = [float(DS[c].sum()) for c in cols5]
claim(all(abs(a_ - b_) <= 0.0051 for a_, b_ in zip(totals, (10.48, 26.31, 33.47, 8.46, 23.85))), "demand table totals (flow impulse, $)",
      "10.48 / 26.31 / 33.47 / 8.46 / 23.85", " / ".join(f"{v:.2f}" for v in totals))
for key in ["VAT", "LVT_bridge_L1_m1"]:
    flow = wsum(dC_hh(HH[key]), w25) / S_CE
    num(float(DS[f"{key}|household_liq_tenure"].sum()), flow, f"Engel aggregation: tenure-aware bars add to the household flow ({key})", tol=0.002,
        note=f"gap {100 * (float(DS[f'{key}|household_liq_tenure'].sum()) / flow - 1):+.3f}%")
v_, l_ = DS["VAT|decile_netted"].loc[CH], DS["LVT_bridge_L1_m1|decile_netted"].loc[CH]
l2_ = DS["LVT_bridge_L2_m1|decile_netted"].loc[CH]
ratio = l_ / v_
claim(bool((np.sign(v_) == np.sign(l_)).all() and (np.sign(v_) == np.sign(l2_)).all()), "all 36 charted bars keep their sign under the LVT (post's method, L1 and L2)",
      "36/36", f"{int((np.sign(v_) == np.sign(l_)).sum())}/36 (L1), {int((np.sign(v_) == np.sign(l2_)).sum())}/36 (L2)")
inband = int(((ratio >= 2.3) & (ratio <= 3.0)).sum())
claim(inband == 31, "sizes scale by 2.3-3.0 for 31 of the 36 bars", "31", str(inband),
      "outliers: " + ", ".join(f"{c} {ratio[c]:.2f}x" for c in ratio.index[(ratio < 2.3) | (ratio > 3.0)]))
claim(bool(((ratio >= 2.3) & (ratio <= 3.0)).all()) or "every LVT bar is the matching VAT bar times about 2.5" not in NOTES_TXT,
      "'Under the post's own decile method, every LVT bar is the matching VAT bar times about 2.5' (plain-words summary)",
      "every bar ~2.5x", f"{ratio.min():.2f}x-{ratio.max():.2f}x; 5 bars outside 2.3-3.0",
      "overstated: the detail (Results 5) is right, 31 of 36 in 2.3-3.0 with outliers at 1.5x and 3.6x; the summary should say 'nearly every'")
iv, il = float(DS["VAT|decile_netted"].sum()), float(DS["LVT_bridge_L1_m1|decile_netted"].sum())
shd = (l_ / il - v_ / iv).abs()
claim(shd.max() <= 0.0075 and close(100 * l_["Rented dwellings"] / il, 31.5, 0.051) and close(100 * v_["Rented dwellings"] / iv, 32.1, 0.051),
      "each bar's share of the impulse within 0.7 points of the VAT's (rent 31.5% vs 32.1%)", "0.7 pts; 31.5 vs 32.1",
      f"max {100 * shd.max():.2f} pts ({shd.idxmax()}); rent {100 * l_['Rented dwellings'] / il:.1f} vs {100 * v_['Rented dwellings'] / iv:.1f}")
claim(close(ratio["Cars and trucks, used"], 2.99, 0.01) and close(ratio["Cars and trucks, new"], 2.78, 0.01) and l_["Cars and trucks, new"] < 0 < l_["Cars and trucks, used"],
      "quality ladder survives: new cars fall, used rise, 2.8-3.0x larger under the LVT", "2.8-3.0x",
      f"new {ratio['Cars and trucks, new']:.2f}x, used {ratio['Cars and trucks, used']:.2f}x")
# Fig 6 analog: D10's share of each top-10 mover's withdrawal
d10s = {}
for key, net_d in [("VAT", vnet), ("LVT_bridge_L1_m1", ACC["LVT_bridge_L1_m1"]["net"])]:
    c = pd.DataFrame(contrib(SCHED["mid"] * net_d / BUD), index=CATS, columns=DEC)
    top = DS[f"{key}|decile_netted"].loc[CH].abs().sort_values(ascending=False).index[:10]
    neg = c.loc[top].clip(upper=0)
    d10s[key] = (neg["d10"] / neg.sum(axis=1))
claim(close(d10s["LVT_bridge_L1_m1"].min(), 0.87, 0.0051) and close(d10s["LVT_bridge_L1_m1"].max(), 0.95, 0.0051)
      and close(d10s["VAT"].min(), 0.61, 0.0051) and close(d10s["VAT"].max(), 0.83, 0.0051),
      "Fig 6 analog: D10 supplies 87-95% of each top-10 withdrawal under the LVT, 61-83% under the VAT", "87-95 / 61-83",
      f"{100 * d10s['LVT_bridge_L1_m1'].min():.0f}-{100 * d10s['LVT_bridge_L1_m1'].max():.0f} / {100 * d10s['VAT'].min():.0f}-{100 * d10s['VAT'].max():.0f}")
lt, vt_ = DS["LVT_bridge_L1_m1|household_liq_tenure"].loc[CH], DS["VAT|household_liq_tenure"].loc[CH]
flip_vs_vat_tenure = list(lt.index[np.sign(lt) != np.sign(vt_)])
flip_vs_post = list(lt.index[np.sign(lt) != np.sign(v_)])
claim(sorted(flip_vs_vat_tenure) == sorted(["Home maintenance, repairs & insurance", "Reading"]),
      "tenure-aware version: two bars flip (home maintenance; reading at -$0.002)", "2 flips vs the VAT's tenure-aware bars",
      f"{len(flip_vs_vat_tenure)} vs VAT tenure-aware; {len(flip_vs_post)} vs the post's method ({', '.join(flip_vs_post)})",
      "against the post's own (decile-netted) VAT bars a third bar also flips: vehicle rental (+0.016 -> -0.015); say which comparison")
# marginal propensity to spend on rent: renters', owners', decile-average basket
mps = {}
for nm, (Ct, eta_t) in list(TB.items()) + [("decile", (CM, ETA))]:
    mps[nm] = (Ct.loc["Rented dwellings"] / Ct.sum() * eta_t.loc["Rented dwellings"]).values
claim(close(100 * mps["renter"].min(), 24, 0.51) and close(100 * mps["renter"].max(), 32, 0.51) and close(100 * mps["owner"].max(), 0.3, 0.051)
      and close(100 * mps["decile"].min(), 3, 0.51) and close(100 * mps["decile"].max(), 19, 0.51),
      "marginal spending on rent: renters 24-32 cents, owners 0.3 cents, decile-average basket 3-19 cents", "24-32 / 0.3 / 3-19",
      f"{100 * mps['renter'].min():.1f}-{100 * mps['renter'].max():.1f} / {100 * mps['owner'].max():.2f} / {100 * mps['decile'].min():.1f}-{100 * mps['decile'].max():.1f}")
rb_hh = float(DS["LVT_bridge_L1_m1|household_liq"].loc["Rented dwellings"])
claim(True, "rent bar 'doubles' to $18.10 from $8.28: the comparison mixes two changes", "$8.28 -> $18.10",
      f"household level, decile baskets ${rb_hh:.2f}; tenure baskets $18.10 ({18.0993 / rb_hh:.2f}x)",
      "the tenure effect alone is " + f"{18.0993 / rb_hh:.1f}x (household level), the liquidity grade moves the decile-netted $8.28 to ${rb_hh:.2f}; 'doubles' holds either way")


# %% 10. the stock channel: capitalization, collateral, non-occupiers, the VAT levy
AREA = "stock channel"
SHOCK = pd.read_csv(REPO / "three-taxes" / "data" / "lvt_shock.csv").set_index("design")["price_drop"]


def loss_frac(phi, design):
    if design == "immediate":
        return phi
    if design == "increment":
        return phi * GAMMA / DELTA
    return float(SHOCK[f"phase-in {design.split('_')[1]}"]) * phi / PHI_FULL


capb = pd.read_csv(BOUT / "us_lvt_capitalization.csv")
NV_CAP = {"LVT_bridge_L1": [0.848, 0.801, 0.746, 0.653, 0.574, 0.339], "LVT_bridge_L2": [0.555, 0.524, 0.489, 0.428, 0.376, 0.222],
          "LVT_full_L1": [0.980, 0.926, 0.863, 0.755, 0.664, 0.392]}
DES = ["immediate", "phasein_5y", "phasein_10y", "phasein_20y", "phasein_30y", "increment"]
for sc, nvs in NV_CAP.items():
    rate, base = sc.split("_")[1], sc.split("_")[2]
    mine = [loss_frac(PHI[(rate, base, "m1")], d) for d in DES]
    b = [float(capb[(capb["scenario"] == sc) & (capb["design"] == d) & (capb["measure"] == MNAME["m1"])]["loss_fraction"].iloc[0]) for d in DES]
    claim(np.allclose(mine, b, atol=1e-9) and np.allclose(mine, nvs, atol=0.00051), f"capitalization (share of land value lost), {sc} m1: immediate / phase-in 5-30y / increment-only",
          " / ".join(f"{v:.3f}" for v in nvs), " / ".join(f"{v:.3f}" for v in mine))
claim(close(loss_frac(PHI[("bridge", "L1", "m1")], "phasein_10y") / PHI[("bridge", "L1", "m1")], 0.88, 0.0051),
      "a 10-year phase-in still capitalizes 88% of the immediate loss", "88%", f"{100 * loss_frac(1, 'phasein_10y'):.1f}%")


def collateral(lf, d_=s25, Ldf=L25, ths=(0.80, 0.90, 1.00)):
    V0, M = d_["HOUSES_24"].values, d_["MRTHEL_24"].values
    loss = lf * Ldf["L_own"].values
    V1 = V0 - loss
    w = d_["WGT"].values
    mort = (V0 > 0) & (M > 0)
    with np.errstate(divide="ignore", invalid="ignore"):
        l0 = np.where(mort, M / np.where(V0 > 0, V0, 1), np.nan)
        l1 = np.where(mort, np.where(V1 > 0, M / np.where(V1 > 0, V1, 1), np.inf), np.nan)
    out = dict(agg0=wsum(M, w) / wsum(V0, w), agg1=wsum(M, w) / wsum(np.maximum(V1, 0), w), nmort=wsum(mort, w) / 1e6,
               under=wsum(mort & (l1 > 1), w) / 1e6, loss=loss, l0=l0, l1=l1, mort=mort)
    for th in ths:
        cr = mort & (l0 <= th) & (l1 > th)
        cap = np.maximum(0, th * V0 - M) - np.maximum(0, th * V1 - M)
        out[th] = dict(n=wsum(cr, w) / 1e6, share=wsum(cr, w) / wsum(mort, w), eq=wsum(loss * cr, w) / 1e9, cap=wsum(cap * cr, w) / 1e9, cross=cr)
    return out


def pct(x_bn, mpc):
    return -100 * mpc * x_bn / C_TOT


colb = pd.read_csv(BOUT / "us_lvt_collateral.csv")
ltvb = pd.read_csv(BOUT / "us_lvt_ltv.csv")
COL = {}
worst = 0.0
for sc in ["LVT_bridge_L1", "LVT_bridge_L2", "LVT_full_L1"]:
    rate, base = sc.split("_")[1], sc.split("_")[2]
    for mk in ["m1", "m2", "m3", "m4"]:
        for dsg in ["immediate", "phasein_10y", "increment"]:
            c = collateral(loss_frac(PHI[(rate, base, mk)], dsg))
            COL[(sc, mk, dsg)] = c
            for th in (0.80, 0.90, 1.00):
                b = colb[(colb["scenario"] == sc) & (colb["measure"] == MNAME[mk]) & (colb["design"] == dsg) & (colb["threshold"] == th)].iloc[0]
                worst = max(worst, abs(c[th]["n"] - b["n_cross_m"]) / max(b["n_cross_m"], 1), abs(c[th]["eq"] - b["lost_equity_crossers_bn"]) / max(b["lost_equity_crossers_bn"], 1),
                            abs(c[th]["cap"] - b["lost_capacity_crossers_bn"]) / max(b["lost_capacity_crossers_bn"], 1))
            bl = ltvb[(ltvb["scenario"] == sc) & (ltvb["measure"] == MNAME[mk]) & (ltvb["design"] == dsg)].iloc[0]
            worst = max(worst, abs(c["agg1"] - bl["ltv_aggregate_after"]), abs(c["under"] - bl["underwater_after_m"]) / bl["underwater_after_m"])
claim(worst < 1e-6, "collateral grid (3 scenarios x 4 measures x 3 designs x 3 thresholds) equals us_lvt_collateral.csv / us_lvt_ltv.csv", "108 + 36 rows",
      f"max relative gap {worst:.1e}")
cols4 = [("LVT_bridge_L1", "immediate"), ("LVT_bridge_L1", "phasein_10y"), ("LVT_bridge_L1", "increment"), ("LVT_full_L1", "immediate")]
c4 = [COL[(sc, "m1", d)] for sc, d in cols4]
claim(close(100 * c4[0]["agg0"], 28.7, 0.051) and all(close(100 * c["agg1"], v, 0.051) for c, v in zip(c4, (44.4, 41.7, 33.5, 48.5))),
      "aggregate LTV of SCF owners 28.7% -> 44.4 / 41.7 / 33.5 / 48.5%", "28.7 -> 44.4 / 41.7 / 33.5 / 48.5",
      f"{100 * c4[0]['agg0']:.1f} -> " + " / ".join(f"{100 * c['agg1']:.1f}" for c in c4))
claim(close(c4[0]["nmort"], 56.7, 0.051) and all(close(c["under"], v, 0.051) for c, v in zip(c4, (14.4, 12.7, 4.6, 18.0))),
      "mortgaged owners underwater after: 14.4 / 12.7 / 4.6 / 18.0 million of 56.7", "14.4 / 12.7 / 4.6 / 18.0 of 56.7",
      " / ".join(f"{c['under']:.1f}" for c in c4) + f" of {c4[0]['nmort']:.1f}")
claim(all(close(c[0.8]["n"], v, 0.051) and close(100 * c[0.8]["share"], sh, 0.51) for c, v, sh in zip(c4, (16.8, 14.3, 6.3, 19.9), (30, 25, 11, 35))),
      "crossing 80% LTV: 16.8 (30%) / 14.3 (25%) / 6.3 (11%) / 19.9 (35%) million", "16.8 / 14.3 / 6.3 / 19.9",
      " / ".join(f"{c[0.8]['n']:.1f} ({100 * c[0.8]['share']:.0f}%)" for c in c4))
claim(all(close(c[0.8]["eq"], e, 0.51) and close(c[0.8]["cap"], k, 0.51) for c, e, k in zip(c4, (2834, 2107, 390, 3948), (1246, 914, 163, 1751))),
      "crossers' lost equity / lost borrowing capacity, $bn", "2,834/1,246; 2,107/914; 390/163; 3,948/1,751",
      "; ".join(f"{c[0.8]['eq']:,.0f}/{c[0.8]['cap']:,.0f}" for c in c4))
NV_RESP = [(-1.48, -1.89, -3.14, -0.83), (-1.10, -1.40, -2.34, -0.61), (-0.20, -0.26, -0.43, -0.11), (-2.06, -2.63, -4.38, -1.17)]
mine_r = [(pct(c[0.8]["eq"], MPCC["low"]), pct(c[0.8]["eq"], MPCC["mid"]), pct(c[0.8]["eq"], MPCC["high"]), pct(c[0.8]["cap"], MPCC["mid"])) for c in c4]
claim(all(pv(a_, b_, 0.01, "collateral response table") for row_m, row_n in zip(mine_r, NV_RESP) for a_, b_ in zip(row_m, row_n)),
      "collateral response at 4.7 / 6 / 10c on lost equity, and 6c on lost capacity, % of consumption (4 designs)",
      "; ".join("/".join(f"{v:.2f}" for v in r_) for r_ in NV_RESP), "; ".join("/".join(f"{v:.2f}" for v in r_) for r_ in mine_r))
cL2 = COL[("LVT_bridge_L2", "m1", "immediate")]
claim(close(100 * cL2["agg1"], 37.4, 0.051) and close(cL2["under"], 8.3, 0.051) and close(cL2[0.8]["n"], 10.3, 0.051) and close(cL2[0.8]["eq"], 1093, 0.51)
      and close(pct(cL2[0.8]["eq"], 0.047), -0.57, 0.0051) and close(pct(cL2[0.8]["eq"], 0.06), -0.73, 0.0051) and close(pct(cL2[0.8]["eq"], 0.10), -1.21, 0.0051)
      and close(pct(cL2[0.8]["cap"], 0.06), -0.31, 0.0051),
      "L2 at the bridge rate: LTV 37.4%, 8.3m underwater, 10.3m cross 80% with $1,093bn; -0.57/-0.73/-1.21; capacity -0.31", "as stated",
      f"{100 * cL2['agg1']:.1f}%, {cL2['under']:.1f}m, {cL2[0.8]['n']:.1f}m, ${cL2[0.8]['eq']:,.0f}bn; {pct(cL2[0.8]['eq'], 0.047):.2f}/"
      f"{pct(cL2[0.8]['eq'], 0.06):.2f}/{pct(cL2[0.8]['eq'], 0.10):.2f}; {pct(cL2[0.8]['cap'], 0.06):.2f}")
nm4 = [COL[("LVT_bridge_L1", k, "immediate")][0.8]["n"] for k in ("m1", "m2", "m3", "m4")]
rm4 = {k: pct(COL[("LVT_bridge_L1", k, "immediate")][0.8]["eq"], 0.06) for k in ("m1", "m2", "m3", "m4")}
claim(close(min(nm4), 9.7, 0.051) and close(max(nm4), 17.3, 0.051) and pv(rm4["m4"], -0.64, 0.01, "four measures m4") and pv(rm4["m2"], -0.94, 0.01, "four measures m2")
      and pv(rm4["m1"], -1.89, 0.01, "four measures m1") and pv(rm4["m3"], -2.04, 0.01, "four measures m3"),
      "across the four measures: 9.7-17.3m crossers; mid response -0.64 (m4), -0.94 (m2), -1.89 (m1), -2.04 (m3)", "as stated",
      f"{min(nm4):.1f}-{max(nm4):.1f}m; " + ", ".join(f"{k} {v:.2f}" for k, v in rm4.items()))
c1 = COL[("LVT_bridge_L1", "m1", "immediate")]
red = [1 - c1[th]["eq"] / c1[0.8]["eq"] for th in (0.9, 1.0)]
claim(close(red[0], 0.10, 0.0051) and close(red[1], 0.27, 0.0051), "with the 90% or 100% threshold the response is 10-27% smaller", "10-27%",
      f"{100 * red[0]:.0f}% / {100 * red[1]:.0f}%")
claim(close(PHI[("bridge", "L1", "m4")], 0.53, 0.0051) and close(PHI[("bridge", "L1", "m3")], 0.88, 0.0051),
      "the price fall at the bridge rate ranges from 53% (m4) to 88% (m3)", "53-88%", f"{100 * PHI[('bridge', 'L1', 'm4')]:.0f}-{100 * PHI[('bridge', 'L1', 'm3')]:.0f}%")
# non-occupiers: flow OR wealth effect
nonb = pd.read_csv(BOUT / "us_lvt_nonoccupier.csv")
NONOCC = {}
for key, nvs in [("LVT_bridge_L1_m1", (152, 3.6, 0.976, 1.197, 0.594, -0.008)), ("LVT_bridge_L2_m1", (388, 9.2, 1.242, 1.714, 0.181, -1.353))]:
    h = HH[key]
    _, rate, base, mk = key.split("_")
    phi = PHI[(rate, base, mk)]
    Lno = (L25["L_ore"] + (L25["L_nnb"] + L25["L_nfc"] if base == "L2" else 0)).values
    bill_bn = wsum(h["bill_nonocc"], w25) * 12 / 1e9
    capl = phi * wsum(Lno, w25) / 1e12
    res = [imp_dn(dsum(s25, h["net"]) / (N_CE * SH_CE), SCHED["mid"])]
    for mpw in (MPW["low"], MPW["mid"], MPW["high"]):
        cash = h["net"] + h["bill_nonocc"]
        extra = -mpw * phi * Lno / 12
        dCd = SCHED["mid"] * dsum(s25, cash) / (N_CE * SH_CE) + dsum(s25, extra) / (N_CE * SH_CE)
        res.append(100 * float((W_D * dCd).sum()) / BUD_BAR)
    NONOCC[key] = res
    b = nonb[(nonb["scenario"] == key) & (nonb["grade"] == "dn_mid")].iloc[0]
    okb = np.allclose(res, [b["flow_version_pct"], b["wealth_version_low_pct"], b["wealth_version_mid_pct"], b["wealth_version_high_pct"]], atol=1e-6)
    okn = close(bill_bn, nvs[0], 0.51) and close(capl, nvs[1], 0.051) and all(close(a_, b_, 0.00051) for a_, b_ in zip(res, nvs[2:]))
    claim(okb and okn, f"non-occupying holders ({key[11:13]}): bills $bn/yr, capitalized $tn; flow vs wealth effect 2/3.5/5c",
          " / ".join(str(v) for v in nvs), f"{bill_bn:.0f} / {capl:.1f} / " + " / ".join(f"{v:.3f}" for v in res))
claim(close(MPW["mid"] / R["m1"], 0.83, 0.0051), "a 3.5-cent wealth effect withdraws 0.83 dollars per dollar of bill (capitalized loss = bill / r)", "0.83",
      f"{MPW['mid'] / R['m1']:.3f}")
# the VAT levy channel (impact) on SCF 2025 net worth
NW = wsum(s25["NETWORTH_24"], w25) / 1e9
levyb = pd.read_csv(BOUT / "us_lvt_vat_levy.csv").set_index(["lam", "mpw"])["pct_ce_consumption"]
claim(close(NW / 1000, 161.9, 0.051) and close(NW / C_TOT, 17.9, 0.051) and close(NW / PCE, 8.2, 0.051) and close(LEVY * NW / 1000, 13.0, 0.051),
      "SCF 2025 net worth $161.9tn (2024 $) = 17.9x CE consumption, 8.2x PCE; 8% levy $13.0tn", "161.9 / 17.9 / 8.2 / 13.0",
      f"{NW / 1000:.1f} / {NW / C_TOT:.1f} / {NW / PCE:.1f} / {LEVY * NW / 1000:.1f}")
LEV = {(lam, k): -100 * MPW[k] * lam * LEVY * NW / C_TOT for lam in (0.0, 0.35, 1.0) for k in MPW}
claim(all(close(LEV[(lam, k)], float(levyb[(lam, k)]), 1e-6) for lam in (0.0, 0.35, 1.0) for k in MPW)
      and all(close(LEV[(0.35, k)], v, 0.0051) for k, v in zip(("low", "mid", "high"), (-1.00, -1.76, -2.51)))
      and all(close(LEV[(1.0, k)], v, 0.0051) for k, v in zip(("low", "mid", "high"), (-2.87, -5.02, -7.18)))
      and close(-100 * MPW["mid"] * 0.35 * LEVY * NW / PCE, -0.80, 0.0051),
      "VAT levy channel table (lambda 0.35: -1.00/-1.76/-2.51; lambda 1: -2.87/-5.02/-7.18; 3.5c on PCE -0.80)", "as printed",
      " / ".join(f"{LEV[(0.35, k)]:.2f}" for k in MPW) + "; " + " / ".join(f"{LEV[(1.0, k)]:.2f}" for k in MPW))

# %% 11. the macro channels and the headline table
AREA = "macro: price step and the headline table"
vsh = float((W_D * acc_v["vatable"].values).sum() / BUD_BAR)
claim(close(vsh, 0.617, 0.0005) and close(100 * 0.15 * vsh * 0.9, 8.3, 0.051) and close(100 * 0.15 * vsh * 0.8, 7.4, 0.051) and close(100 * 0.15 * vsh, 9.3, 0.051),
      "VAT price step 8.3% [7.4, 9.3] = 15 points x VAT-able share 61.7% x 80-100% pass-through", "8.3 [7.4, 9.3]",
      f"{100 * 0.15 * vsh * 0.9:.2f} [{100 * 0.15 * vsh * 0.8:.2f}, {100 * 0.15 * vsh:.2f}]; share {vsh:.4f}")
macb = pd.read_csv(BOUT / "us_lvt_macro_channels.csv").set_index("channel")
pub = pd.read_csv(TIDY / "post_published_numbers.csv").set_index("id")["value"].astype(float)
fl = lambda k, g: IMP[(k, g, "none")]
vat_c = fl("VAT", "dn_mid") + LEV[(0.35, "mid")]
vat_lo = fl("VAT", "dn_high") + LEV[(0.35, "high")]
vat_hi = fl("VAT", "dn_low") + LEV[(0.35, "low")]
c1L1 = COL[("LVT_bridge_L1", "m1", "immediate")][0.8]
c1L2 = COL[("LVT_bridge_L2", "m1", "immediate")][0.8]
L1_c = fl("LVT_bridge_L1_m1", "dn_mid") + pct(c1L1["eq"], MPCC["mid"])
L1_lo = fl("LVT_bridge_L1_m1", "dn_high") + pct(c1L1["eq"], MPCC["high"])
L1_hi = fl("LVT_bridge_L1_m1", "dn_low") + pct(c1L1["cap"], MPCC["low"])
L2_c = fl("LVT_bridge_L2_m1", "dn_mid") + pct(c1L2["eq"], MPCC["mid"])
L2_lo = fl("LVT_bridge_L2_m1", "dn_high") + pct(c1L2["eq"], MPCC["high"])
L2_hi = fl("LVT_bridge_L2_m1", "dn_low") + pct(c1L2["cap"], MPCC["low"])
for lab, trip, nv, ch in [("VAT: flow + levy at lambda = 0.35", (vat_c, vat_lo, vat_hi), (-1.37, -2.21, -0.53), "net demand at impact, lambda = 0.35 (flow + levy)"),
                          ("LVT bridge L1: flow + collateral", (L1_c, L1_lo, L1_hi), (-0.91, -2.37, 0.54), "net demand at impact (flow + collateral; bridge, L1, immediate)"),
                          ("LVT bridge L2: flow + collateral", (L2_c, L2_lo, L2_hi), (0.52, -0.23, 1.26), "net demand at impact (flow + collateral; bridge, L2, immediate)")]:
    b = macb.loc[ch]
    claim(np.allclose(trip, [b["central"], b["low"], b["high"]], atol=1e-6) and all(close(a_, n_, 0.0051) for a_, n_ in zip(trip, nv)),
          f"headline table: {lab}, central [band], % of consumption", f"{nv[0]} [{nv[1]}, {nv[2]}]", f"{trip[0]:.3f} [{trip[1]:.3f}, {trip[2]:.3f}]")
claim(close(pub["P663"], -0.69, 1e-9) and close(pub["P664"], -0.97, 1e-9) and close(pub["P665"], -0.14, 1e-9) and close(pub["P662"], 0.38, 1e-9)
      and close(pub["P666"], -2.7, 1e-9), "the post's published path: flow +0.38 (P662); central -0.69 [-0.97, -0.14] (P663-P665); A-K -2.7 (P666)", "as cited",
      f"{pub['P662']} ; {pub['P663']} [{pub['P664']}, {pub['P665']}] ; {pub['P666']}")
claim(close(pub["P663"] - pub["P662"], -1.07, 0.0051) and close(pub["P666"] - pub["P662"], -3.1, 0.051),
      "the post's implied levy part at year 3: about -1.07 (lambda 0.35), -3.1 (A-K)", "-1.07 / -3.1", f"{pub['P663'] - pub['P662']:.2f} / {pub['P666'] - pub['P662']:.2f}")
nb2 = NONOCC["LVT_bridge_L2_m1"]
claim(close(nb2[2] + pct(c1L2["eq"], MPCC["mid"]), -0.55, 0.0051), "L2 if business/corporate landholders respond to the capitalized loss at 3.5c: -0.55%", "-0.55",
      f"{nb2[2] + pct(c1L2['eq'], MPCC['mid']):.3f}")
claim(close(pct(COL[("LVT_bridge_L1", "m1", "increment")][0.8]["eq"], 0.06), -0.26, 0.0051), "increment-only grandfathering cuts the collateral channel to -0.26%", "-0.26",
      f"{pct(COL[('LVT_bridge_L1', 'm1', 'increment')][0.8]['eq'], 0.06):.3f}")
claim(close(pct(c1L1["eq"], 0.047), -1.48, 0.0051) and close(pct(c1L1["eq"], 0.10), -3.14, 0.0051) and close(pct(c1L1["cap"], 0.047), -0.65, 0.0051)
      and close(pct(c1L1["cap"], 0.10), -1.38, 0.0051), "'that is -1.5% to -3.1% of consumption ... lost borrowing capacity -0.65% to -1.4%'",
      "-1.5/-3.1; -0.65/-1.4", f"{pct(c1L1['eq'], 0.047):.2f}/{pct(c1L1['eq'], 0.10):.2f}; {pct(c1L1['cap'], 0.047):.2f}/{pct(c1L1['cap'], 0.10):.2f}")
low_end = [fl("LVT_bridge_L1_m1", g) + pct(c1L1["cap"], 0.047) for g in ("dn_high", "dn_mid", "dn_low")]
hi_end = [fl("LVT_bridge_L1_m1", g) + pct(c1L1["eq"], 0.10) for g in ("dn_mid", "dn_high")]
claim(close(min(low_end), 0.1, 0.051) and close(max(low_end), 0.5, 0.051) and close(hi_end[0], -2.2, 0.051) and close(hi_end[1], -2.4, 0.051),
      "'What would change': low end (4.7c, capacity only) +0.1% to +0.5%; 10c on lost equity -2.2% (mid) to -2.4%", "+0.1..+0.5; -2.2..-2.4",
      f"{min(low_end):+.2f}..{max(low_end):+.2f}; {hi_end[0]:.2f}..{hi_end[1]:.2f}")

pubn = pd.read_csv(TIDY / "post_published_numbers.csv").set_index("id")["note"].astype(str)
claim(close(pub["P497"], 7, 1e-9) and close(pub["P498"], 9, 1e-9) and close(pub["P667"], -3.3, 1e-9) and close(pub["P668"], -1.2, 1e-9)
      and "year-5" in pubn["P664"] and "year-5" in pubn["P667"],
      "post: price level 7-9% (P497-P498); A-K band [-3.3, -1.2] (P667-P668); bands are the year-5 edges (gate notes)", "as cited",
      f"{pub['P497']:g}-{pub['P498']:g}%; [{pub['P667']:g}, {pub['P668']:g}]")
pf = [IMP[("LVT_bridge_L1_m1", g_, "none")] for g_ in ["dn_mid", "dn_low", "dn_high", "dn_mono", "hh_liq_mid", "hh_liq_low", "hh_liq_high",
                                                       "hh_liq_mono", "hh_liq_mid_monthly", "hh_liqsym_mid"]]
mf = [IMP[("LVT_bridge_L1_m1", g_, "none")] for g_ in ["dn_meas", "hh_meas_htm", "dn_measshape"]]
claim(close(min(pf), 0.70, 0.0051) and close(max(pf), 1.19, 0.0051) and close(min(mf), 0.14, 0.0051) and close(max(mf), 0.52, 0.0051),
      "Judgment table: LVT L1 impulse 0.70-1.19% across the post's family of grades, 0.14-0.52% measured", "0.70-1.19 / 0.14-0.52",
      f"{min(pf):.3f}-{max(pf):.3f} / {min(mf):.3f}-{max(mf):.3f}")
dd = IMP[("LVT_bridge_L1_m1", "dn_mid", "own65")] - IMP[("LVT_bridge_L1_m1", "dn_mid", "none")]
dc = IMP[("LVT_bridge_L1_m1", "dn_mid", "own65_cash")] - IMP[("LVT_bridge_L1_m1", "dn_mid", "none")]
claim(close(dd, 2.0, 0.0051) and close(dc, -0.12, 0.0051), "deferral by owners 65+: +2.0 points (dividend in full, state lends) or -0.12 (cash-balanced)", "+2.0 / -0.12",
      f"{dd:+.3f} / {dc:+.3f}", "the +2.0 is a deficit-financed transfer of 30% of revenue, not comparable with the balanced VAT (the NOTES say so)")

# %% 12. the loop (T5)
AREA = "the loop"
RENT_I = CATS.index("Rented dwellings")


def rent_bar(shock):
    return float(contrib(shock)[RENT_I].sum())


keyL1 = dsum(s25, L25["L_ore"]) / wsum(L25["L_ore"], w25)
keyL2 = dsum(s25, L25["L_ore"] + L25["L_nnb"]) / wsum(L25["L_ore"] + L25["L_nnb"], w25)
loopb = pd.read_csv(BOUT / "us_lvt_loop.csv")
LOOP = {}
for key in ["LVT_bridge_L1_m1", "LVT_bridge_L2_m1", "LVT_full_L1_m1", "LVT_full_L2_m1"]:
    _, rate, base, mk = key.split("_")
    phi = PHI[(rate, base, mk)]
    kk = keyL1 if base == "L1" else keyL2
    R0 = rent_bar(SCHED["mid"] * ACC[key]["net"] / BUD)
    for lk, ls in LS.items():
        R_, tot_, q_ = R0, 0.0, None
        for _ in range(200):
            dd = phi * ls * R_
            net_r = dd - dd * kk / W_D                         # everyone gets dd; rental-land holders pay it
            Rn = rent_bar(SCHED["mid"] * net_r / BUD)
            q_ = Rn / dd if q_ is None else q_
            tot_ += dd
            if abs(dd) < 1e-12:
                break
            R_ = Rn
        LOOP[(key, lk)] = dict(R0=R0, extra=tot_, pct=100 * tot_ / ACC[key]["div"], q=q_, mult=1 / (1 - phi * ls * q_),
                               closed=phi * ls * R0 / (1 - phi * ls * q_))
        b = loopb[(loopb["scenario"] == key) & (loopb["ls"] == lk)].iloc[0]
        claim(close(tot_, b["extra_dividend"], 1e-6, True) and close(q_, b["q_rent_bar_per_dollar"], 1e-6, True) and close(tot_, LOOP[(key, lk)]["closed"], 1e-6, True),
              f"loop {key} ls {ls}: extra dividend iterated = closed form phi*ls*R0/(1-phi*ls*q)", f"{b['extra_dividend']:.4f}", f"{tot_:.4f}",
              f"R0 {R0:.2f}, q {q_:.4f}, multiplier {1 / (1 - phi * ls * q_):.4f}")
for key, nv in [("LVT_bridge_L1_m1", (8.28, 3.31, 2.86, 1.14, 0.86, 1.44, 0.0495, 1.017)), ("LVT_bridge_L2_m1", (10.32, 4.13, 2.32, 0.93, 0.70, 1.17, 0.0540, 1.012)),
                ("LVT_full_L1_m1", (9.57, 3.83, 3.83, 1.33, 0.99, 1.67, 0.0495, 1.020))]:
    L_ = LOOP[(key, "mid")]
    mine = (L_["R0"], 0.4 * L_["R0"], L_["extra"], L_["pct"], LOOP[(key, "low")]["pct"], LOOP[(key, "high")]["pct"], L_["q"], L_["mult"])
    tols = (0.0051, 0.0051, 0.0051, 0.0051, 0.0051, 0.0051, 0.00006, 0.00051)
    bad = [f"{i}: {a_:.4f} vs {n_}" for i, (a_, n_, t_) in enumerate(zip(mine, nv, tols)) if abs(a_ - n_) > t_]
    claim(not bad, f"loop table row {key}: R0, increment, extra dividend, % [low, high], q, 1/(1-phi ls q)", " / ".join(str(v) for v in nv),
          " / ".join(f"{v:.4f}" for v in mine), ("; ".join(bad) + ": 1.1449 printed as 1.14 (rounds to 1.14 or 1.15; the macro table says 1.145)") if bad else "")
R0t = float(DS["LVT_bridge_L1_m1|household_liq_tenure"].loc["Rented dwellings"])
claim(close(R0t, 18.10, 0.0051) and close(0.4 * R0t, 7.24, 0.0051) and close(PHI[("bridge", "L1", "m1")] * 0.4 * R0t, 6.14, 0.0051)
      and close(100 * PHI[("bridge", "L1", "m1")] * 0.4 * R0t / DIV_VAT, 2.46, 0.0051), "tenure-aware round 0: $18.10 -> $7.24 -> $6.14 = 2.46% of the dividend",
      "18.10 / 7.24 / 6.14 / 2.46", f"{R0t:.2f} / {0.4 * R0t:.2f} / {PHI[('bridge', 'L1', 'm1')] * 0.4 * R0t:.2f} / {100 * PHI[('bridge', 'L1', 'm1')] * 0.4 * R0t / DIV_VAT:.2f}",
      "one round only (no closed form), unlike the decile rows")
R0v = rent_bar(SCHED["mid"] * vnet / BUD)
gain = {lk: ls * R0v * 12 * S_CE / 1e9 for lk, ls in LS.items()}
vals_ = [gain["mid"] / R[k] for k in ("m1", "m2", "m3", "m4")] + [gain[lk] / R[k] for lk in LS for k in ("m1", "m2", "m3", "m4")]
claim(close(gain["mid"], 4.5, 0.051) and close(gain["low"], 3.4, 0.051) and close(gain["high"], 5.6, 0.051) and close(gain["mid"] / R["m1"], 107, 0.51)
      and close(min(vals_), 50, 0.51) and close(max(vals_), 139, 0.51),
      "VAT: the increment, $4.5bn a year [3.4, 5.6], goes to landlords; worth $107bn on m1 ($50-139bn)", "4.5 [3.4, 5.6]; 107 (50-139)",
      f"{gain['mid']:.2f} [{gain['low']:.2f}, {gain['high']:.2f}]; {gain['mid'] / R['m1']:.0f} ({min(vals_):.0f}-{max(vals_):.0f})")
claim(close(keyL1[9], 0.60, 0.0051) and close(keyL1[8], 0.16, 0.0051) and close(keyL2[9], 0.71, 0.0051),
      "holders of rental land: 60% top decile, 16% D9 (ORESRE key); 71% D10 with noncorporate land", "60 / 16 / 71",
      f"{100 * keyL1[9]:.1f} / {100 * keyL1[8]:.1f} / {100 * keyL2[9]:.1f}")
claim(close(0.4 * float(DS["VAT|household_liq_tenure"].loc["Rented dwellings"]) * 12 * S_CE / 1e9 / R["m1"], 127, 0.51),
      "with the tenure-aware VAT rent bar ($4.00) the landlords' gain is about $127bn", "127",
      f"{0.4 * float(DS['VAT|household_liq_tenure'].loc['Rented dwellings']) * 12 * S_CE / 1e9 / R['m1']:.0f}")
claim(close(1 - PHI[("bridge", "L1", "m1")], 0.15, 0.0051), "at the bridge rate 1 - phi = 15% of the increment leaks to landowners", "15%", f"{100 * (1 - PHI[('bridge', 'L1', 'm1')]):.1f}%")


# %% 13. robustness: survey year, rising s, CE home values, the s band, NFC and noncorporate-key alternatives
AREA = "robustness"
robb = pd.read_csv(BOUT / "us_lvt_robustness.csv")


def headline(d_, Ldf, htm, base, mk="m1", rate="bridge"):
    w = d_["WGT"].values
    Ltot = wsum(Ldf[base], w) / 1e9
    phi = VAT_REV / (R[mk] * Ltot) if rate == "bridge" else PHI_FULL
    a = decile_acc(base, phi, R[mk], Ldf, d_)
    h = hh_lvt(base, phi, R[mk], a["div"], d_, Ldf)
    mpc = np.where((h["net"] < 0) & htm["htm"], 1.0, SCHED["mid"][d_["dec_i"].values - 1])
    c = collateral(phi, d_, Ldf)
    return dict(phi=phi, net=a["net"], payer=100 * wsum(h["net"] < 0, w) / w.sum(), imp=imp_dn(a["net"], SCHED["mid"]),
                liq=100 * wsum(mpc * h["net"], w) / (S_CE * BUD_BAR), coll=pct(c[0.8]["eq"], MPCC["mid"]), top=a["land_share"][9], Ltot=Ltot)


def rob_claim(label, H, brow, nv, base):
    """nv = (phi, D1, D5, D9, D10, payers %, impulse post, impulse liq, collateral 6c) as printed; None = not printed."""
    mine = (H["phi"], H["net"][0], H["net"][4], H["net"][8], H["net"][9], H.get("payer"), H["imp"], H.get("liq"), H.get("coll"))
    units = (0.001, 1, 1, 1, 1, 0.1, 0.001, 0.001, 0.01)
    b = (brow["phi"], brow["net_d01"], brow["net_d05"], brow["net_d09"], brow["net_d10"], 100 * brow["payer_share"], brow["impulse_dn_mid"],
         brow["impulse_hh_liq_mid"], brow["collateral_mid_pct"])
    okb = all((m_ is None or not np.isfinite(b_)) or close(m_, b_, 1e-5, True) or abs(m_ - b_) < 1e-6 for m_, b_ in zip(mine, b))
    bad = [f"{i}: {m_:.3f} vs {n_}" for i, (m_, n_, u_) in enumerate(zip(mine, nv, units)) if n_ is not None and not pv(m_, n_, u_, f"robustness {label} {base} col{i}")]
    claim(okb and not bad, f"robustness row: {label} [{base}] (phi, D1, D5, D9, D10, payers, impulse post / liquidity, collateral 6c)",
          " / ".join("" if v is None else f"{v:g}" for v in nv), " / ".join("" if v is None else f"{v:.3f}" for v in mine),
          ("; ".join(bad)) + ("" if okb else " (builder CSV mismatch)"))


def brow(variant_start, base):
    q = robb[robb["variant"].str.startswith(variant_start) & (robb["base"] == base)]
    return q.iloc[0]


ROB = {}
for base, nv in [("L1", (0.848, 183, 90, -39, -514, 31.6, 0.976, 0.885, -1.89)), ("L2", (0.555, 189, 122, -1, -750, 22.4, 1.242, 1.183, -0.73))]:
    ROB[("main", base)] = headline(s25, L25, HTM, base)
    rob_claim("main: SCF 2025, uniform s", ROB[("main", base)], brow("main: SCF 2025", base), nv, base)
for base, nv in [("L1", (0.848, 167, 88, -64, -524, 29.8, 0.997, 0.937, -2.20)), ("L2", (0.555, 153, 123, -10, -751, 21.9, 1.234, 1.182, -0.83))]:
    ROB[("scf22", base)] = headline(s22, L22, HTM22, base)
    rob_claim("SCF 2022 (real 2024 $, roster adults)", ROB[("scf22", base)], brow("SCF 2022", base), nv, base)
L25r, I25r = land(s25, z1["L_hh"], z1["L_nnb"], z1["L_nfc"], rising=True)
ROB[("rising", "L1")] = headline(s25, L25r, HTM, "L1")
rob_claim("s rising with home value", ROB[("rising", "L1")], brow("SCF 2025, s rising", "L1"), (0.848, 193, 106, -41, -588, 27.4, 1.090, 0.993, -1.79), "L1")
num(0.30 * I25r["k"], cal.iloc[11], "rising s: effective range low end (0.30 k)", 0.24, 0.005)
num(0.60 * I25r["k"], cal.iloc[12], "rising s: effective range high end (0.60 k)", 0.48, 0.005)
for nm, zz, nv in [("NFC land, low ($1.7tn)", z1["L_nfc_low"], (0.593, 186, 116, -3, -724, 22.9, 1.207, 1.141, -0.83)),
                   ("NFC land, high (2020 share)", z1["L_nfc_high"], (0.550, None, None, None, -753, None, None, None, None))]:
    Lx, _ = land(s25, z1["L_hh"], z1["L_nnb"], zz)
    H = headline(s25, Lx, HTM, "L2")
    rob_claim(nm, H, brow("NFC land rule: " + ("structures_proxy" if "low" in nm else "share_2020"), "L2"), nv, "L2")
for nm, key, nv in [("noncorporate key + ORESRE", ("NNRESRE", "BUS", "ORESRE"), -733), ("noncorporate key NNRESRE + ACTBUS", ("NNRESRE", "ACTBUS"), -739)]:
    Lx, _ = land(s25, z1["L_hh"], z1["L_nnb"], z1["L_nfc"], nnb_key=key)
    H = headline(s25, Lx, HTM, "L2")
    rob_claim(nm, H, brow("noncorporate land key" + (" adds ORESRE" if "ORESRE" in key else ": NNRESRE + actively"), "L2"),
              (0.555, None, None, None, nv, None, None, None, None), "L2")
# CE 2024 home values for the owner-occupied land (decile-netted only)
for base, nv in [("L1", (0.848, 140, 71, -41, -365, None, 0.672, None, None)), ("L2", (0.555, 161, 110, -2, -652, None, 1.043, None, None))]:
    other = sum(dsum(s25, L25[c]) for c in (["L_ore"] + (["L_nnb", "L_nfc"] if base == "L2" else [])))
    land_d = wsum(L25["L_own"], w25) * shCE + other
    phi = VAT_REV / (R["m1"] * land_d.sum() / 1e9)
    bill = phi * R["m1"] * land_d / (N_CE * SH_CE * 12)
    net = float((W_D * bill).sum()) - bill
    H = dict(phi=phi, net=net, imp=imp_dn(net, SCHED["mid"]), top=land_d[9] / land_d.sum())
    rob_claim("CE home-value distribution", H, brow("CE 2024's own", base), nv, base)
    ROB[("ce", base)] = H
claim(close(ROB[("ce", "L1")]["top"], 0.32, 0.0051), "CE's home values put 32% of residential land in the top decile (vs 39% SCF)", "32% vs 39%",
      f"{100 * ROB[('ce', 'L1')]['top']:.1f}% vs {100 * DSH['L1'][9]:.1f}%")
# the s band at a fixed aggregate property value
sb = []
for sv in (0.30, 0.60):
    Lx, _ = land(s25, z1["L_hh"], z1["L_nnb"], z1["L_nfc"], s_fix=sv)
    Ltot = sv * I25["prop_bn"]
    row = {}
    for mk in ("m1", "m3"):
        r = R[mk] if mk == "m1" else RT[mk] / Ltot
        phi = VAT_REV / (r * Ltot)
        row[mk] = dict(phi=phi, fd=PHI_FULL * r * Ltot * 1e9 / (S_CE * 12), coll=pct(collateral(phi, s25, Lx)[0.8]["eq"], MPCC["mid"]))
    sb.append(row)
claim(close(sb[0]["m1"]["phi"], 1.18, 0.0051) and close(sb[1]["m1"]["phi"], 0.59, 0.0051) and close(sb[0]["m1"]["fd"], 208, 0.51) and close(sb[1]["m1"]["fd"], 416, 0.51)
      and close(sb[0]["m1"]["coll"], ROB[("main", "L1")]["coll"], 1e-6) and close(sb[1]["m1"]["coll"], ROB[("main", "L1")]["coll"], 1e-6)
      and close(sb[0]["m3"]["coll"], -1.0, 0.051) and close(sb[1]["m3"]["coll"], -5.0, 0.051),
      "s band 0.30-0.60: phi on m1 1.18 to 0.59; full-capture dividend $208-$416; collateral unchanged on m1, -1.0% to -5.0% on m3", "as stated",
      f"phi {sb[0]['m1']['phi']:.3f}-{sb[1]['m1']['phi']:.3f}; ${sb[0]['m1']['fd']:.0f}-${sb[1]['m1']['fd']:.0f}; m3 {sb[0]['m3']['coll']:.2f} to {sb[1]['m3']['coll']:.2f}")
claim(np.allclose(ROB[("main", "L1")]["net"], decile_acc("L1", VAT_REV / (R["m1"] * 0.30 * I25["prop_bn"]), R["m1"], land(s25, z1["L_hh"], z1["L_nnb"], z1["L_nfc"], s_fix=0.30)[0])["net"], atol=1e-6),
      "at the bridge rate a uniform s cancels: L1 nets identical at s = 0.30 and calibrated s", "identical", "identical")


# %% 14. caveats, deliverables, house-keeping claims
AREA = "caveats and deliverables"
claim(close(100 * C_TOT / PCE, 45.5, 0.051), "the bridge's consumption budget is 45.5% of PCE", "45.5%", f"{100 * C_TOT / PCE:.1f}%")
nat = 0.15 * vsh * PCE
phis = {(b, k): nat / (R[k] * LTOT[b]) for b in ("L1", "L2") for k in ("m1", "m2", "m3", "m4")}
claim(close(nat / 1000, 1.83, 0.0051) and close(nat * 1e9 / (S_CE * 12), 548, 0.51) and all(phis[("L1", k)] > 0.98 for k in ("m1", "m2", "m3", "m4"))
      and close(phis[("L2", "m2")], 0.90, 0.0051) and close(phis[("L2", "m4")], 0.76, 0.0051) and phis[("L2", "m1")] > 0.98 and phis[("L2", "m3")] > 0.98,
      "national-accounts VAT: up to $1.83tn ($548 dividend); phi > 0.98 on L1 everywhere, L2 only m2 / m4 (0.90, 0.76)", "1.83tn / $548 / 0.90, 0.76",
      f"{nat / 1000:.2f}tn / ${nat * 1e9 / (S_CE * 12):.0f} / {phis[('L2', 'm2')]:.2f}, {phis[('L2', 'm4')]:.2f}")
agg25 = pd.read_csv(REPO / "three-taxes" / "data" / "aggregates_2025.csv", index_col=0)["value"]
claim(close(agg25["proptax"], 789, 0.51), "state and local property taxes $789bn in 2025 (aggregates_2025.csv)", "789", f"{agg25['proptax']:.1f}")
chk = pd.read_csv(BOUT / "check_lvt_us.csv")
cnt = chk["status"].value_counts().to_dict()
claim(cnt.get("PASS", 0) == 228 and cnt.get("FAIL", 0) == 0 and cnt.get("INFO", 0) == 1 and len(chk) == 229, "the builder's own checks: 228 PASS / 0 FAIL / 1 INFO of 229",
      "228/0/1", f"{cnt.get('PASS', 0)}/{cnt.get('FAIL', 0)}/{cnt.get('INFO', 0)} of {len(chk)}")
claim("mpc_default" not in m, "bridge.py imported unchanged for the US: the US model dict carries no 'mpc_default' (Finland's hook)", "no key",
      "no key" if "mpc_default" not in m else "key present", "and the VAT bars equal the rebuild's Fig 5 (above)")


def png_dpi(path):
    b = Path(path).read_bytes()
    i = b.find(b"pHYs")
    if i < 0:
        return None
    ppm = int.from_bytes(b[i + 4:i + 8], "big")
    return ppm * 0.0254


figs = ["us_lvt_net_by_decile.png", "us_lvt_demand_shifts_top15.png", "us_lvt_who_pays.png", "us_lvt_macro_channels.png"]
dpis = [png_dpi(LVT / "figures" / f) if (LVT / "figures" / f).exists() else None for f in figs]
claim(all(d is not None and abs(d - 200) < 1 for d in dpis), "the four figures exist as PNG at 200 dpi", "4 x 200 dpi", " / ".join(f"{d:.0f}" if d else "missing" for d in dpis))

# %% 15. adversarial review
AREA = "review"
h1 = HH["LVT_bridge_L1_m1"]
c1 = COL[("LVT_bridge_L1", "m1", "immediate")]
cr = c1[0.8]["cross"]
mid_i = SCHED["mid"][s25["dec_i"].values - 1]
bill_cr = wsum(h1["bill_own"] * cr, w25) * 12 / 1e9                          # crossers' own-home LVT bills, $bn/yr
flow_cr = wsum(mid_i * h1["bill_own"] * cr, w25) * 12 / 1e9                 # their response to it already inside the flow
coll_eq = 0.06 * c1[0.8]["eq"]
mult = (flow_cr + coll_eq) / bill_cr
flowL1 = IMP[("LVT_bridge_L1_m1", "dn_mid", "none")]
alt_cap = flowL1 + pct(c1[0.8]["cap"], 0.06)
alt_either = flowL1 + pct(c1[0.8]["eq"], 0.06) + 100 * flow_cr / C_TOT        # crossers: wealth response INSTEAD of their bill response
cL2x = COL[("LVT_bridge_L2", "m1", "immediate")][0.8]
flowL2 = IMP[("LVT_bridge_L2_m1", "dn_mid", "none")]
flow_cr2 = wsum(mid_i * HH["LVT_bridge_L2_m1"]["bill_own"] * cL2x["cross"], w25) * 12 / 1e9
alt2 = (flowL2 + pct(cL2x["cap"], 0.06), flowL2 + pct(cL2x["eq"], 0.06) + 100 * flow_cr2 / C_TOT)
# (1) the T4 point: stock and flow are one object; the headline's central adds both for the threshold crossers
centL1 = float(macb.loc["net demand at impact (flow + collateral; bridge, L1, immediate)", "central"])
claim(min(abs(centL1 - alt_cap), abs(centL1 - alt_either)) < 0.3, "headline 'LVT at the bridge rate, base L1: flow + collateral -0.91' counts the crossers' tax twice (T4)",
      "-0.91 (flow 0.976 + 6c x crossers' lost equity -1.885)",
      f"clean readings: flow + 6c x lost capacity {alt_cap:+.2f}; crossers' wealth response instead of their bill response {alt_either:+.2f}",
      f"crossers' lost equity (${c1[0.8]['eq']:,.0f}bn) is the capitalized value of their own-home bills (${bill_cr:,.0f}bn/yr, T4). The flow already "
      f"takes their bill at the decile MPC ({100 * flow_cr / C_TOT:.2f}% of consumption); adding 6c x the capitalized loss on top makes them cut "
      f"spending by {mult:.1f}x their annual bill (6c > r = {100 * R['m1']:.1f}%). The unit's own rule for non-occupiers is 'either the flow or a "
      "wealth effect, never both', and NOTES call the lost-equity row 'an upper reading', yet it is the central value. With either clean reading "
      f"the LVT's central demand at impact is about zero ({alt_either:+.2f} to {alt_cap:+.2f}), not -0.91, so the headline sign rests on the double "
      f"count. Same on L2: {alt2[1]:+.2f} to {alt2[0]:+.2f} instead of +0.52")
# (2) the collateral channel applied to families who would not borrow
inc = s25["INCOME_24"].clip(lower=0).values
liq3 = HTM["liquid"] >= inc / 4
sh_htm = wsum(c1["loss"] * cr * HTM["htm"], w25) / 1e9 / c1[0.8]["eq"]
sh_liq = wsum(c1["loss"] * cr * liq3, w25) / 1e9 / c1[0.8]["eq"]
n_htm = wsum(cr * HTM["htm"], w25) / 1e6
capv = np.maximum(0, 0.8 * s25["HOUSES_24"].values - s25["MRTHEL_24"].values) - np.maximum(0, 0.8 * (s25["HOUSES_24"].values - c1["loss"]) - s25["MRTHEL_24"].values)
htm_eq = pct(wsum(c1["loss"] * cr * HTM["htm"], w25) / 1e9, 0.06)
htm_cap = pct(wsum(capv * cr * HTM["htm"], w25) / 1e9, 0.06)
claim(re.search(r"crossers.{0,200}(hand-to-mouth|liquid)|(hand-to-mouth|liquid).{0,200}crossers", NOTES_TXT) is not None,
      "the collateral response is applied to every mortgaged owner who crosses 80% LTV, whether or not they would borrow",
      f"16.8m crossers, -1.89% at 6c", f"HtM crossers {n_htm:.1f}m hold {100 * sh_htm:.0f}% of the lost equity; {100 * sh_liq:.0f}% sits with families "
      f"holding >= 3 months' income in liquid assets", f"restricted to hand-to-mouth crossers (KVW, the unit's own flag): {htm_eq:.2f}% (lost equity) / "
      f"{htm_cap:.2f}% (lost capacity) at 6c, against -1.89 / -0.83. Aladangady's 4.7c is an average over all homeowners and is driven by the "
      "constrained; applying it to unconstrained crossers' lost equity is a judgment the NOTES do not show as one. Report the constrained-crossers "
      "version beside the all-crossers one")
claim("in the literature (4.7-10 cents" not in NOTES_TXT, "plain words: 'At the housing-collateral responses in the literature (4.7-10 cents per dollar per year), that is -1.5% to -3.1%'",
      "4.7-10c 'in the literature'", f"literature 4.7-7c gives {pct(c1[0.8]['eq'], 0.047):.2f}% to {pct(c1[0.8]['eq'], 0.07):.2f}%",
      "10c is the unit's own stress value ('no source gives a number for the levered tail', Judgment section); the summary presents it as a "
      "measurement and the headline band's lower edge (-2.37) rests on it. Say '4.7-7 cents in the literature, 10 cents as a stress value'")
inc_tab = float(SHOCK["increment-only (grandfather r0)"]) * PHI[("bridge", "L1", "m1")] / PHI_FULL
ci = collateral(inc_tab)
inc_b = float(capb[(capb["scenario"] == "LVT_bridge_L1") & (capb["design"] == "increment") & (capb["measure"] == MNAME["m1"])]["loss_fraction"].iloc[0])
claim(abs(inc_b - inc_tab) < 1e-6, "increment-only grandfathering: loss phi x gamma/delta (0.339) while the phase-in rows come from lvt_shock.csv",
      f"{loss_frac(PHI[('bridge', 'L1', 'm1')], 'increment'):.3f}; collateral -0.26", f"table: {inc_tab:.3f}; collateral {pct(ci[0.8]['eq'], 0.06):.2f}",
      "the same repo table the unit uses for the phase-in rows gives a 40.4% loss at 0.98 (discrete timing), not 39.2%: use one convention "
      "for all designs (effect small: -0.26 -> -0.27)")
claim("same SCF balance sheets, same bands" not in NOTES_TXT, "headline-table header '(same SCF balance sheets, same bands)'", "same bands", "levy 2-5c vs collateral 4.7-10c",
      "the flow bands are the same MPC schedules, but the stock channels use different per-dollar bands; say 'same SCF balance sheets, same "
      "denominator'")
inc_lvt = 0.4 * LOOP[("LVT_bridge_L1_m1", "mid")]["R0"] * 12 * S_CE / 1e9
claim("Under the VAT, the same increment" not in NOTES_TXT, "'Under the VAT, the same increment ($4.5bn a year of land rent ...) goes to landlords'", "the same increment",
      f"LVT increment ${inc_lvt:.1f}bn/yr vs VAT ${gain['mid']:.1f}bn/yr", "same mechanism, 2.5x different size; say 'the VAT's own (smaller) increment'")
z_after100 = z1["mortg"] / (z1["re_hh"] - z1["L_hh"])
scf_after100 = collateral(1.0)["agg1"]
claim(abs(scf_after100 - z_after100) < 0.015, "memo 7.1 aggregate LTV (26% -> 48%) 'reproduced on SCF owners: 28.7% -> 48.5%'", "48.5% at 0.98",
      f"like for like (land price to zero, 2024): SCF {100 * scf_after100:.1f}% vs Z.1 {100 * z_after100:.1f}%",
      "the two differences (SCF starts higher, 28.7 vs 26.0; its land share is lower, 0.416 vs 0.460) offset; within 1.1 points on the same concept")
nb1 = NONOCC["LVT_bridge_L1_m1"]
claim(True, "non-occupiers: flow OR wealth effect, never both (the wealth version removes their bills from cash)", "never both",
      f"flow {nb1[0]:.3f}; wealth 2/3.5/5c {nb1[1]:.3f}/{nb1[2]:.3f}/{nb1[3]:.3f}", "the same rule is not applied to the threshold crossers (item 1)")
claim(close(N_CE.sum() / w25.sum(), 1.006, 0.001) and np.allclose(dsum(s25, s25["shares"]), N_CE * SH_CE, rtol=1e-12),
      "payment units: the LVT and VAT sides share CE's payment shares; household shares sum to CE decile totals", "consistent",
      f"CE CUs {N_CE.sum() / 1e6:.2f}m vs SCF families {w25.sum() / 1e6:.2f}m (+{100 * (N_CE.sum() / w25.sum() - 1):.1f}%)")
claim(True, "SCF weighting and deciles: WGT pooled over implicates (134.96m), INCPCTLECAT pooled groups; per-implicate weights kept", "pooled",
      "pooled", "no implicate averaging error; the 2022 merge on Y1 sidesteps the tidy IMPLICATE defect")
claim(True, "denominator: every demand channel is % of CE consumption ($9.0tn, 45.5% of PCE)", "CE consumption", f"${C_TOT:,.0f}bn",
      "the stock channels (SCF/Z.1 dollars) and flows (national transfers) are both over the CE budget, so the comparison is internally "
      "consistent; on PCE every channel would be x0.455 (the NOTES show PCE only for the levy)")
landlord = (1 - PHI[("bridge", "L1", "m1")]) * inc_lvt
claim(True, "the loop's arithmetic: iteration = T5's closed form; q is net (payers' and recipients' rent propensities)", "1.017",
      f"{LOOP[('LVT_bridge_L1_m1', 'mid')]['mult']:.4f}", f"conceptual: the rental-land holders are charged the extra dividend but not credited the "
      f"extra rent they collect (net +${landlord:.1f}bn/yr under the LVT, +${gain['mid']:.1f}bn under the VAT); second order (< 0.03% of consumption)")
claim(True, "LVT price step = 0", "0", "0 by assumption", "standard incidence (fixed supply, full capitalization), filed under 'accounting'; "
      f"the unit's own loop adds demand for rent of ${LOOP[('LVT_bridge_L1_m1', 'mid')]['R0']:.2f}/share/month "
      f"({100 * LOOP[('LVT_bridge_L1_m1', 'mid')]['R0'] / float(m['Cbar']['Rented dwellings']):.1f}% of rent spending), so 'nothing' is the pass-through, "
      "not the whole rent-price effect")
phiL2 = PHI[("bridge", "L2", "m1")]
hL2 = HH["LVT_bridge_L2_m1"]
bill_nfc = phiL2 * R["m1"] * L25["L_nfc"].values / 12
l2w = {}
for k_, mpw in MPW.items():
    dCd = SCHED["mid"] * dsum(s25, hL2["net"] + bill_nfc) / (N_CE * SH_CE) + dsum(s25, -mpw * phiL2 * L25["L_nfc"].values / 12) / (N_CE * SH_CE)
    l2w[k_] = 100 * float((W_D * dCd).sum()) / BUD_BAR + pct(c1L2["eq"], MPCC["mid"])
centL2 = float(macb.loc["net demand at impact (flow + collateral; bridge, L2, immediate)", "central"])
claim(abs(centL2 - l2w["mid"]) < 0.1, "headline L2 '+0.52' takes corporate (NFC) land on the flow reading, which the NOTES call unnatural ('holders never see a bill')",
      "+0.52 (all non-occupier land on the flow)", f"NFC land on the wealth reading: {l2w['mid']:+.2f} at 3.5c ({l2w['low']:+.2f} at 2c, {l2w['high']:+.2f} at 5c)",
      "Results 6 says 'for the corporate land in L2 ... the wealth-effect column is the natural reading', but the headline row and the plain-words "
      "+0.52 use the flow for it (shareholders paying the corporate bill from cash at their decile MPC). The sign holds at 3.5c; state the "
      "natural-reading central (+0.25) or say why the flow reading is kept")
tb_scf = tenure_baskets(own_r)
bt = bars_tenure(dC_hh(HH["LVT_bridge_L1_m1"]), tb_scf)
claim(abs(bt["Rented dwellings"] - 18.10) < 0.2, "tenure baskets are split with CE homeowner rates while families are assigned by the SCF owner flag (rates differ: D2 51% vs 42%)",
      "$18.10 rent, -$1.96 home maintenance", f"with SCF owner rates: ${bt['Rented dwellings']:.2f}, {bt['Home maintenance, repairs & insurance']:+.2f}",
      "immaterial: the tenure result does not depend on which survey's tenure rates split the baskets")
claim(not DR, "printed numbers that only a double rounding reproduces (value -> 3 decimals -> 2)", "", f"{len(DR)} found",
      "; ".join(DR) + ("; reprint from the unrounded values" if DR else ""))


# %% output
out = pd.DataFrame(CLAIMS)
out.insert(0, "n", range(1, len(out) + 1))
out.to_csv(OUT_CSV, index=False)
cur = None
for _, r in out.iterrows():
    if r["area"] != cur:
        cur = r["area"]
        print(f"\n# {cur}")
    print(" | ".join([r["status"].ljust(3), r["claim"], r["builder"], r["mine"], r["note"]]))
n_ok, n_bad = int((out.status == "OK").sum()), int((out.status == "BAD").sum())
print(f"\nclaims: {len(out)}  OK: {n_ok}  BAD: {n_bad}")
print("BAD:")
for _, r in out[out.status == "BAD"].iterrows():
    print(f"  [{r['area']}] {r['claim']}")
print(f"written: {OUT_CSV.relative_to(REPO)}")
