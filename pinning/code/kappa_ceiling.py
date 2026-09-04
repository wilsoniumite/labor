# kappa_ceiling.py — data item two: the ceiling of Proposition 8's coverage ratio.
# kappa(q) = q·T/(N·(g_s + q·h_s)) rises toward T/(N·h_s) and NEVER exceeds it, and the
# paper never checked that ceiling against 1 (audit point iv). In flow terms the ceiling
# is (aggregate site rent) / (N × site-rent bill of one person's floor HOUSING): the r
# cancels in the model; empirically both flows are measured, each on the paper's grid.
# Numerator: the paper's own rT members (feasibility_kappa machinery, imported, FRED live).
# Denominator: floor housing cost per person (HUD FMR, bundle-paired: single↔efficiency/1,
# pc4↔2BR/4; plus the BLS SPM renter threshold's housing portion if reachable) × the
# housing site-share axis {0.30, 0.50} (the paper's flow_ls variants, reused).
# Verdict rule, pre-stated: ceiling band clear of 1 from above → audit iv is a robustness
# note; band straddling or below 1 → the "climbs toward the threshold" sentence of Prop 8
# is wrong as written and the paper takes a correction. 2026-08-09.

import io
import os
import sys

import numpy as np
import pandas as pd
import requests

sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # Windows console: never crash on a glyph

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                                  # pinning/
LINKREPO = ROOT                                               # the kappa machinery lives beside this script
DATA = os.path.join(ROOT, "data")
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

# ---------------- Cell 0: the paper's own rT machinery, imported not re-derived ----------------
# chdir so pull_fred's cache/ lands in pinning/cache exactly as the paper's scripts leave it.
os.chdir(LINKREPO)
sys.path.insert(0, os.path.join(LINKREPO, "code"))
from feasibility_kappa import fetch_all, land_series, GRID_BUNDLE, CPI_BASE_YEAR, PS_ANCHOR_2023

data, ledger = fetch_all()
print("=== FRED validation ledger (paper's own gates) ===")
for c, sid, msg in ledger:
    print(f"{c:15s} {sid:20s} {msg}")
core = ["re_hh", "str_hh_res", "pce_housing", "gs10", "pop", "cpi"]
missing = [c for c in core if data.get(c) is None]
if missing:
    print(f"BLOCKED: {missing} unavailable — stopping rather than approximating.")
    raise SystemExit(1)

land_hh = land_series(data, "z1_hh")
YEAR = int(min(land_hh.index.max(), data["pce_housing"].index.max(),
               data["gs10"].index.max(), data["pop"].index.max()))
print(f"\nceiling year (latest with all members live): {YEAR}")
g10 = float(data["gs10"].loc[YEAR])
N_thousands = float(data["pop"].loc[YEAR])
rT = {  # $B/yr — the paper's four current members (z1_econ ends 2020: excluded, year-mixing refused)
    "z1_hh_gs10":  float(land_hh.loc[YEAR]) * g10 / 100.0,
    "z1_hh_gs10p": float(land_hh.loc[YEAR]) * (g10 + 1.5) / 100.0,
    "flow_ls30":   float(data["pce_housing"].loc[YEAR]) * 0.30,
    "flow_ls50":   float(data["pce_housing"].loc[YEAR]) * 0.50,
}
print("rT members ($B/yr):", {k: round(v) for k, v in rT.items()},
      f"| N = {N_thousands*1e3/1e6:.1f}M")

# ---------------- Cell 1: HUD Fair Market Rents — the floor housing price ----------------
# County-level FY2025 schedule (40th-percentile gross rent of standard-quality units —
# HUD's own "modest housing" standard). National summaries as labeled members:
# population-weighted mean if the file carries a population column, else refused;
# unweighted county median always. Occupancy pairing is the HUD standard read onto the
# paper's bundles: single person ↔ efficiency ÷ 1; family-of-four ↔ two-bedroom ÷ 4.
FMR_URL = "https://www.huduser.gov/portal/datasets/fmr/fmr2025/FY25_FMRs.xlsx"
fp = os.path.join(DATA, "hud_fy25_fmrs.xlsx")
if not os.path.exists(fp):
    r = requests.get(FMR_URL, headers=UA, timeout=120)
    r.raise_for_status()
    assert r.content[:2] == b"PK", "not an xlsx"
    open(fp, "wb").write(r.content)
fmr = pd.read_excel(fp, engine="calamine")  # HUD's file carries malformed XML properties; calamine skips them
fmr.columns = [str(c).strip().lower() for c in fmr.columns]
c_eff = next(c for c in fmr.columns if c in ("fmr_0", "fmr0"))
c_2br = next(c for c in fmr.columns if c in ("fmr_2", "fmr2"))
popcols = [c for c in fmr.columns if "pop" in c]
n_areas = len(fmr)
med_eff, med_2br = float(fmr[c_eff].median()), float(fmr[c_2br].median())
print(f"\nHUD FY25: {n_areas} areas, cols eff='{c_eff}' 2br='{c_2br}' pop={popcols}")
assert n_areas > 3000, "FMR file suspiciously short"
assert 700 <= med_eff <= 2000 and 1000 <= med_2br <= 2500, "FMR medians out of sanity range"
members_fmr = {"fmr_medcty": (med_eff, med_2br)}
if popcols:
    w = pd.to_numeric(fmr[popcols[0]], errors="coerce").fillna(0)
    pw_eff = float(np.average(fmr[c_eff], weights=w))
    pw_2br = float(np.average(fmr[c_2br], weights=w))
    members_fmr["fmr_popwt"] = (pw_eff, pw_2br)
    print(f"FMR members ($/mo): median-county eff {med_eff:.0f} 2br {med_2br:.0f} | "
          f"pop-weighted eff {pw_eff:.0f} 2br {pw_2br:.0f}")
else:
    print(f"FMR member ($/mo): median-county eff {med_eff:.0f} 2br {med_2br:.0f} "
          "(no population column — pop-weighted member not built)")

# ---------------- Cell 2: BLS SPM renter threshold, housing portion (probe; drop if blocked) ----------------
# The SPM threshold prices the modern floor bundle directly and publishes its housing
# portion; if reachable it adds a member independent of HUD. Probed, never guessed blind.
spm_member = None
spm_note = "not attempted"
for url in [
    "https://www.bls.gov/pir/spm/spm_thresholds_2023.xlsx",
    "https://www.bls.gov/pir/spm/spm_thresholds_2024.xlsx",
]:
    try:
        r = requests.get(url, headers=UA, timeout=60)
        if r.status_code == 200 and r.content[:2] == b"PK":
            t = pd.read_excel(io.BytesIO(r.content), header=None)
            spm_note = f"fetched {url.rsplit('/',1)[1]} — parse below"
            # structure varies; find a renter row and a housing-portion column by label scan
            txt = t.astype(str)
            hit = txt.apply(lambda col: col.str.contains("renter", case=False, na=False)).any().any()
            spm_member = (t, url) if hit else None
            if spm_member is None:
                spm_note += " [no renter row found — DROPPED, structure unknown]"
            break
        spm_note = f"HTTP {r.status_code} at {url.rsplit('/',1)[1]}"
    except requests.RequestException as e:
        spm_note = f"FAIL {type(e).__name__}"
print(f"\nBLS SPM threshold probe: {spm_note}")
if spm_member is not None:
    print("SPM file fetched but structure not pre-registered — recorded for a later pass, "
          "NOT folded into today's grid uninspected.")

# ---------------- Cell 3: the ceiling grid ----------------
# ceiling = rT / (N × annual floor housing cost × site-share). Site-share axis {0.30, 0.50}
# converts gross rent to site rent — the same contested share the paper's flow members use.
SITE_SHARE = [0.30, 0.50]
rows = []
for rt_name, rt_val in rT.items():
    for fmr_name, (eff, br2) in members_fmr.items():
        for pairing, monthly, occ in [("single_eff", None, 1.0), ("pc4_2br", None, 4.0)]:
            monthly = eff if pairing == "single_eff" else br2
            annual_pp = monthly * 12.0 / occ                       # $/person/yr, gross rent
            for ss in SITE_SHARE:
                bill = annual_pp * ss                              # site-rent bill per person
                denom = N_thousands * 1e3 * bill / 1e9             # $B/yr
                rows.append(dict(rt=rt_name, fmr=fmr_name, pairing=pairing, site_share=ss,
                                 floor_rent_pp=annual_pp, ceiling=rt_val / denom))
grid = pd.DataFrame(rows)
med, lo, hi = grid.ceiling.median(), grid.ceiling.min(), grid.ceiling.max()
share_below_1 = (grid.ceiling < 1).mean()
print("\n=== the ceiling, %d, %d members ===" % (YEAR, len(grid)))
print(grid.round(3).to_string(index=False))
print(f"\nceiling median {med:.2f}, band [{lo:.2f}, {hi:.2f}], members below 1: "
      f"{(grid.ceiling < 1).sum()}/{len(grid)} ({share_below_1*100:.0f}%)")

# ---------------- Cell 4: context — today's kappa on the same members, and the bundle tension ----------------
cpi = data["cpi"]
cpi0 = float(cpi.loc[CPI_BASE_YEAR])
print("\ncontext (same year, paper's kappa vs the ceiling):")
for bname, base in GRID_BUNDLE:
    ps = base * float(cpi.loc[YEAR]) / cpi0
    nps = N_thousands * 1e3 * ps / 1e9
    ks = {k: v / nps for k, v in rT.items()}
    print(f"  bundle {bname}: P_s({YEAR}) = ${ps:,.0f}/person/yr | kappa members: "
          + ", ".join(f"{k} {v:.2f}" for k, v in ks.items()))
eff_ann = members_fmr["fmr_medcty"][0] * 12
print(f"\nbundle tension, stated: FY25 median-county efficiency FMR is ${eff_ann:,.0f}/yr GROSS —"
      f" compare the whole Orshansky single-person bundle above. The paper's P_s carries 1963's"
      f" housing weight; a modern floor bundle is housing-heavier, so the paper's kappa is, if"
      f" anything, OVERSTATED at modern housing prices while the ceiling here is bundle-free on"
      f" the goods side. The two objects answer different questions and neither substitutes.")

grid.to_csv(os.path.join(DATA, "kappa_ceiling.csv"), index=False)
print(f"\nwrote data/kappa_ceiling.csv")
