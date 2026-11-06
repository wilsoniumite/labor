# panel.py — the us-record data panel (SPEC.md section 8, Phase 1): annual US series, 1950–2025, for the backward
# model. Three groups, as SPEC.md sections 3–5 name them: the four targeted facts, the measured inputs, and the facts the
# fit is judged on without being fitted to them. Every series is either a file already in the repository or a public
# series fetched once into cache/; data/manifest.csv records each file's origin and SHA-256. The measurement equation
# for each column is in docs/measurement.md.
#
# Rules. Annual means over complete calendar years only (the repository's rule for monthly and quarterly series: 12
# months or 4 quarters, else the year is missing). 2025 is therefore missing wherever October 2025 was never published
# (the CPI); nothing is filled, interpolated or extended. A fetch that fails stops the build (her standing rule).
#
# Run from us-record/:  python3 code/panel.py      (writes data/panel.csv and data/manifest.csv)

import datetime as dt
import hashlib
import json
import os
import sys

import numpy as np
import openpyxl
import pandas as pd
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                      # us-record/
REPO = os.path.dirname(ROOT)
CACHE = os.path.join(ROOT, "cache")
DATA = os.path.join(ROOT, "data")
YEARS = list(range(1950, 2026))
BEA_FA1 = "https://apps.bea.gov/national/FixedAssets/Release/XLS/Section1All_xls.xlsx"

sys.path.insert(0, os.path.join(REPO, "pinning", "code"))
import lambda_compute2 as lc  # noqa: E402  the house FRED machinery: fredgraph CSV, cache first, patient retries

lc.CACHE = CACHE
MANIFEST = []                                     # one row per source file


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def record(path, origin, used_for):
    """A manifest row for a source file (repository-relative path)."""
    MANIFEST.append(dict(file=os.path.relpath(path, REPO).replace(os.sep, "/"), sha256=sha256(path), origin=origin,
                         used_for=used_for))


def annual_complete(s):
    """Annual means over complete calendar years: 12 monthly or 4 quarterly observations (an annual series as is),
    else no value."""
    s = s.dropna()
    per_year = s.groupby(s.index.year)
    gap = s.index.to_series().diff().dt.days.median()
    need = 12 if gap < 45 else (4 if gap < 120 else 1)
    return per_year.mean()[per_year.count() == need]


def fred_file(path, sid):
    """A cached FRED CSV (observation_date, sid) as a dated series."""
    df = pd.read_csv(path)
    return pd.Series(pd.to_numeric(df[sid], errors="coerce").values, index=pd.to_datetime(df["observation_date"]))


def fred_repo(rel, sid, used_for):
    """A FRED series already in the repository."""
    path = os.path.join(REPO, rel)
    record(path, f"repository file (FRED {sid})", used_for)
    return annual_complete(fred_file(path, sid))


def fred_fetch(sid, used_for):
    """A FRED series fetched once into cache/ through pinning/code/lambda_compute2.pull_fred."""
    s = lc.pull_fred(sid)
    if s is None:
        raise SystemExit(f"STOP: FRED {sid} could not be fetched or parsed; nothing substituted")
    path = os.path.join(CACHE, f"{sid}.csv")
    record(path, f"fetched {lc.FRED_CSV.format(sid=sid)}", used_for)
    return annual_complete(s)


def bea_fixed_assets():
    """Table 1.1 (current-cost net stock) and 1.3 (current-cost depreciation), line 'Fixed assets', fetched once."""
    path = os.path.join(CACHE, "Section1All_xls.xlsx")
    if not os.path.exists(path):
        r = requests.get(BEA_FA1, timeout=120)
        if r.status_code != 200 or not r.content.startswith(b"PK"):
            raise SystemExit(f"STOP: BEA Fixed Assets section 1 fetch failed ({r.status_code}); nothing substituted")
        with open(path, "wb") as f:
            f.write(r.content)
    record(path, f"fetched {BEA_FA1}", "delta")
    wb = openpyxl.load_workbook(path, read_only=True)

    def line(sheet, code):
        rows = list(wb[sheet].iter_rows(values_only=True))
        hdr = next(r for r in rows if r and r[0] == "Line")
        years = [int(c) for c in hdr[3:] if c is not None]
        row = next(r for r in rows if r and len(r) > 2 and r[2] == code)
        return pd.Series(dict(zip(years, row[3:3 + len(years)])), dtype=float)

    stock, dep = line("FAAt101-A", "k1ttotl1es00"), line("FAAt103-A", "m1ttotl1es00")
    return dep / ((stock.shift(1) + stock) / 2.0)                 # depreciation over the average net stock


def theta_v():
    """The machine chain's labour share of a machine's build cost, on calibration (c)'s basis: the equipment + IPP +
    private structures bundle, domestic labour (domp), annual 1997–2023 (paths/results/chains.json); before 1997 the λ
    thread's benchmark points 1967–1992 (narrow machinery set, import-comparable basis, already spliced to 1997 NAICS),
    linked to the bundle's basis by their 1997 ratio. Nothing before 1967 is measured."""
    chains = os.path.join(REPO, "paths", "results", "chains.json")
    century = os.path.join(REPO, "progress_and_prosperity", "lambda", "data", "lambda_us_century.csv")
    family = os.path.join(REPO, "progress_and_prosperity", "lambda", "data", "lambda_us_family_a.csv")
    record(chains, "repository file (paths/code/chains.py)", "theta_V")
    record(century, "repository file (the λ thread's century arc)", "theta_V")
    record(family, "repository file (the λ thread's family A)", "theta_V")
    bundle = json.load(open(chains))["bundles"]["equipment_ipp_structures"]
    annual = pd.Series({int(y): v["theta_domp"] for y, v in bundle.items()})
    narrow97 = pd.read_csv(family).set_index("year").loc[1997, "lam_narrow_tot"]
    bench = pd.read_csv(century).set_index("year")["lam_spliced"].dropna()
    linked = bench * (annual.loc[1997] / narrow97)
    out = pd.concat([linked, annual]).sort_index()
    basis = pd.Series({y: ("bundle domp, chains.json" if y >= 1997 else "century benchmark, narrow tot, linked at 1997")
                       for y in out.index})
    return out, basis


def repo_table(rel, used_for, index="year"):
    path = os.path.join(REPO, rel)
    record(path, "repository file", used_for)
    return pd.read_csv(path).set_index(index)


def build():
    os.makedirs(CACHE, exist_ok=True)
    os.makedirs(DATA, exist_ok=True)
    p = pd.DataFrame(index=pd.Index(YEARS, name="year"))

    # ---- the targeted facts (SPEC.md section 4)
    fork = repo_table("pinning/effort/data/fig3_realwage_fork_1950.csv", "wage_goods, wage_shelter")
    p["wage_goods"] = fork["real_wage_durables_1950_100"]
    p["wage_shelter"] = fork["real_wage_shelter_1950_100"]
    lr = repo_table("pinning/effort/archive_v28/expected/LR_Q1_fullchain_factor_content_strong_weak_1950_2025.csv",
                    "labour_share_c")
    p["labour_share_c"] = lr["human_effort_share_headline"]
    weak = lr["evidence_tier"] == "WEAK"                        # the band is the weak (regression) estimate's: it applies
    p["labour_share_c_lo"] = lr["human_effort_weak_lower"].where(weak)   # where the headline is that estimate; the
    p["labour_share_c_hi"] = lr["human_effort_weak_upper"].where(weak)   # STRONG years (1997–2023, annual I-O) carry none
    p["labour_share_c_tier"] = lr["evidence_tier"]
    p["emp_rate"] = fred_repo("paths/cache/EMRATIO.csv", "EMRATIO", "emp_rate") / 100.0

    # ---- the measured inputs (SPEC.md section 3)
    p["adults"] = fred_fetch("CNP16OV", "adults")                 # thousands, civilian noninstitutional, 16+
    p["employed"] = fred_fetch("CE16OV", "employed (the emp_rate identity check)")
    p["aaa"] = fred_repo("paths/cache/AAA.csv", "AAA", "aaa, real_rate") / 100.0
    p["gs10"] = fred_repo("pinning/cache/GS10.csv", "GS10", "gs10, real_rate_gs10") / 100.0
    cpi = fred_repo("paths/cache/CPIAUCNS.csv", "CPIAUCNS", "infl, exp_infl, real_wage_cpi")
    infl = np.log(cpi).diff()
    p["infl"] = infl
    p["exp_infl"] = infl.rolling(5).mean()                        # the five years to t (adaptive)
    p["real_rate"] = p["aaa"] - p["exp_infl"]
    p["real_rate_gs10"] = p["gs10"] - p["exp_infl"]
    p["delta"] = bea_fixed_assets()
    tv, basis = theta_v()
    p["theta_V"], p["theta_V_basis"] = tv, basis

    # ---- the facts the fit is judged on (SPEC.md section 5)
    k = repo_table("pinning/data/kappa_results.csv", "kappa")
    p["kappa_med"], p["kappa_min"], p["kappa_max"] = k["kappa_med"], k["kappa_min"], k["kappa_max"]
    df21 = repo_table("pinning/effort/archive_v28/expected/DF21_FINAL_longrun_labor_origin_financing_1950_2025.csv",
                      "labor_origin_fin")
    p["labor_origin_fin"], p["labor_origin_fin_lo"], p["labor_origin_fin_hi"] = (
        df21["labor_origin_financing_central"], df21["lower"], df21["upper"])
    fw = repo_table("pinning/data/four_way_split.csv", "fin_*")
    for c in ("wage_direct", "wagetax", "ownertax", "borrowed"):
        p[f"fin_{c}"] = fw[f"{c}_med"]
    p["wc_median"] = repo_table("companion/data/wc_grid.csv", "wc_median")["wc_median"]
    p["nfb_labour_share"] = fred_repo("paths/cache/PRS85006173.csv", "PRS85006173", "nfb_labour_share")
    p["prime_emp_rate"] = fred_repo("paths/cache/LNS12300060.csv", "LNS12300060", "prime_emp_rate") / 100.0
    hs = fred_repo("pinning/cache/DHSGRC1A027NBEA.csv", "DHSGRC1A027NBEA", "housing_share_pce")
    pce = fred_repo("pinning/cache/PCECA.csv", "PCECA", "housing_share_pce")
    p["housing_share_pce"] = hs / pce

    # ---- the split (her calls, 2026-11-05): the production and nonsupervisory group (AHETPI's) as a share of private
    # employment, which sets the two types' sizes; and the pay gap, all private employees' average hourly wage over
    # that group's, a check only. Everyone is taken to work that group's weekly hours, so only the gap's change is read.
    pns = fred_fetch("CES0500000006", "pns_share")
    priv = fred_fetch("USPRIV", "pns_share, pay_gap")
    hours = fred_fetch("AWHNONAG", "pay_gap")
    wages = fred_fetch("A132RC1A027NBEA", "pay_gap")             # private wages and salaries, billions, annual
    ahe = fred_repo("pinning/effort/data/raw/AHETPI.csv", "AHETPI", "pay_gap, real_wage_cpi")
    p["pns_share"] = pns / priv
    gap = (wages * 1e9 / (priv * 1e3 * hours * 52.0)) / ahe
    p["pay_gap"] = gap / gap.loc[1964]
    p["ahe_all"] = fred_fetch("CES0500000003", "ahe_all")        # all private employees' hourly earnings, from 2006: the
                                                                  # pay gap's anchor (checks/check_panel.py I8)

    # ---- the basket's utility (her note, 2026-11-05: by most counts it rose until about 1970): the production worker's
    # real hourly earnings over the all-items CPI, AHEMAN (manufacturing) to 1964 and AHETPI after, linked at 1964
    man = fred_repo("pinning/effort/data/raw/AHEMAN.csv", "AHEMAN", "real_wage_cpi")
    spliced = pd.concat([man.loc[:1964], ahe.loc[1965:] * (man.loc[1964] / ahe.loc[1964])])
    real = spliced / cpi
    p["real_wage_cpi"] = 100.0 * real / real.loc[1950]

    # ---- the goods wage read over everything but shelter (the playground of 2026-11-06: the model's one final good as all
    # consumption except shelter, against durables alone): the same linked earnings over the CPI less shelter, 1950 = 100
    exsh = fred_fetch("CUUR0000SA0L2", "wage_exshelter")
    real_ex = spliced / exsh
    p["wage_exshelter"] = 100.0 * real_ex / real_ex.loc[1950]

    # ---- durables apart (her go, 2026-11-06): durables' share of consumer spending on everything but housing (BEA, PCE
    # durable goods over PCE less housing services), and durables' price relative to the other goods in that spending.
    # The other goods' price is chained from the CPI less shelter and the CPI's durables (the durables leg of the fork,
    # CUUR0000SAD), each year's change weighted by the two years' mean durables share: a Tornqvist split of the CPI less
    # shelter into durables and the rest, on spending weights (PCE's, not the CPI's own relative importance).
    dur = fred_fetch("PCDGA", "dur_share")
    p["dur_share"] = dur / (pce - hs)
    r_d = np.log(p["wage_exshelter"] / p["wage_goods"])            # log of durables' price over the CPI less shelter's
    w = p["dur_share"]
    w_bar = (w + w.shift(1)) / 2.0
    r_g = (-(w_bar / (1.0 - w_bar)) * r_d.diff()).fillna(0.0).cumsum()   # log of the other goods' price over it
    p["dur_rel_price"] = np.exp(r_d - r_g)                         # durables' price over the other goods', 1950 = 1
    p.loc[p["wage_goods"].isna() | p["wage_exshelter"].isna(), "dur_rel_price"] = np.nan

    p = p.loc[YEARS]
    p.to_csv(os.path.join(DATA, "panel.csv"))                    # full precision: anchors are checked exactly
    man = pd.DataFrame(MANIFEST).drop_duplicates("file")
    man["built_utc"] = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    man.to_csv(os.path.join(DATA, "manifest.csv"), index=False)
    return p


if __name__ == "__main__":
    panel = build()
    cov = panel.apply(lambda c: f"{c.first_valid_index()}-{c.last_valid_index()} ({c.notna().sum()})")
    print("data/panel.csv:", panel.shape[0], "years,", panel.shape[1], "columns; coverage (first-last, years present):")
    for c, v in cov.items():
        print(f"  {c:22s} {v}")
