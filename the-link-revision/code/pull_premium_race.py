# pull_premium_race.py — data item one for "The Link" revision (Prop C2 + queue)
# Style: flat notebook cells. Sources: NBER MORG (primary CPS microdata), Census A-2, NCES 318.10, NY Fed.
# Pulled live 2026-08-09. No substitution: blocked sources are reported, not worked around.

import os, re, glob, requests
import numpy as np
import pandas as pd
from tqdm.auto import tqdm

UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"}
os.makedirs("extract", exist_ok=True)
os.makedirs("out", exist_ok=True)

def weighted_median(vals, wts):
    v = np.asarray(vals, dtype=float); w = np.asarray(wts, dtype=float)
    o = np.argsort(v); v, w = v[o], w[o]
    c = np.cumsum(w)
    return float(v[np.searchsorted(c, 0.5 * c[-1])])

# ---------------- Cell 0: downloads (idempotent; skips files already present) ----------------
os.makedirs("morg", exist_ok=True); os.makedirs("xl", exist_ok=True)
_r = requests.get("https://data.nber.org/morg/annual/", headers=UA, timeout=60)
_listing = sorted(set(re.findall(r"morg\d{2}\.dta", _r.text)))
_missing = [f for f in _listing if not os.path.exists(f"morg/{f}")]
for fn in tqdm(_missing, desc="MORG download (~2 GB total)", ncols=70):
    rr = requests.get(f"https://data.nber.org/morg/annual/{fn}", headers=UA, timeout=600)
    rr.raise_for_status(); open(f"morg/{fn}", "wb").write(rr.content)
for _name, _url in [
    ("xl/taba-2.xlsx", "https://www2.census.gov/programs-surveys/demo/tables/educational-attainment/time-series/cps-historical-time-series/taba-2.xlsx"),
    ("xl/tabn318.10.xlsx", "https://nces.ed.gov/programs/digest/d23/tables/xls/tabn318.10.xlsx"),
]:
    if not os.path.exists(_name):
        rr = requests.get(_url, headers=UA, timeout=120)
        rr.raise_for_status(); open(_name, "wb").write(rr.content)

# ---------------- Cell 1: MORG loop, cached per year ----------------
CACHE = "morg_cache.csv"
done_years = set()
if os.path.exists(CACHE):
    done_years = set(pd.read_csv(CACHE)["year"].unique())

rows = []
files = sorted(glob.glob("morg/morg*.dta"))
for fn in tqdm(files, ncols=70):
    yy = int(re.search(r"morg(\d{2})\.dta", fn).group(1))
    year = 1900 + yy if yy >= 79 else 2000 + yy
    if year in done_years:
        continue
    try:
        if year >= 1992:
            cols = ["age", "sex", "earnwke", "earnwt", "uhourse", "grade92"]
        else:
            cols = ["age", "sex", "earnwke", "earnwt", "uhourse", "gradeat", "gradecp"]
        df = pd.read_stata(fn, columns=cols, convert_categoricals=False)
        df = df[(df.age >= 25) & (df.age <= 64) & (df.earnwke > 0) & (df.earnwt > 0)]
        n_all = len(df)
        df = df[(df.uhourse >= 35) & (df.uhourse <= 99)]
        n_ft = len(df)
        if year >= 1992:
            g = df.grade92
            educg = np.select([g >= 43, (g >= 40) & (g <= 42), g == 39, g < 39],
                              ["BA+", "SC", "HS", "<HS"], default="NA")
        else:
            yrs = df.gradeat - (df.gradecp != 1).astype(int)
            yrs = yrs.clip(lower=0)
            educg = np.select([yrs >= 16, (yrs >= 13) & (yrs <= 15), yrs == 12, yrs < 12],
                              ["BA+", "SC", "HS", "<HS"], default="NA")
        df = df.assign(educg=educg, year=year)
        # per-year extract for later composition work (pass two)
        ex = df[["year", "age", "sex", "educg", "earnwke", "earnwt"]]
        ex.to_parquet(f"extract/morg_{year}.parquet", index=False)
        # aggregates: overall + sex x ageband cells, per educ group
        df["ageband"] = pd.cut(df.age, [24, 34, 44, 54, 64], labels=["25-34", "35-44", "45-54", "55-64"])
        for grp, sub in df.groupby("educg"):
            rows.append(dict(year=year, cell="ALL", educg=grp, n=len(sub),
                             wmed=weighted_median(sub.earnwke, sub.earnwt),
                             wsum=sub.earnwt.sum(), n_all=n_all, n_ft=n_ft))
        for (sx, ab, grp), sub in df.groupby(["sex", "ageband", "educg"], observed=True):
            if len(sub) == 0: continue
            rows.append(dict(year=year, cell=f"{int(sx)}|{ab}", educg=grp, n=len(sub),
                             wmed=weighted_median(sub.earnwke, sub.earnwt),
                             wsum=sub.earnwt.sum(), n_all=n_all, n_ft=n_ft))
    except Exception as e:
        rows.append(dict(year=year, cell="ERROR", educg=str(e)[:120], n=0, wmed=np.nan, wsum=np.nan))

if rows:
    newc = pd.DataFrame(rows)
    if os.path.exists(CACHE):
        newc = pd.concat([pd.read_csv(CACHE), newc])
    newc.to_csv(CACHE, index=False)

cache = pd.read_csv(CACHE)
errs = cache[cache.cell == "ERROR"]
print("\nMORG years done:", sorted(cache.year.unique())[:3], "...", sorted(cache.year.unique())[-3:],
      f"({cache.year.nunique()} yrs), errors: {len(errs)}")
if len(errs): print(errs[["year", "educg"]].to_string())

# ---------------- Cell 2: premium series ----------------
allc = cache[(cache.cell == "ALL") & (cache.educg.isin(["BA+", "HS"]))]
piv = allc.pivot_table(index="year", columns="educg", values="wmed")
cnt = allc.pivot_table(index="year", columns="educg", values="n")
prem = pd.DataFrame({"med_BA": piv["BA+"], "med_HS": piv["HS"],
                     "n_BA": cnt["BA+"], "n_HS": cnt["HS"]})
prem["ratio_raw"] = prem.med_BA / prem.med_HS
prem["educ_regime"] = np.where(prem.index >= 1992, "grade92", "gradeat")

cells = cache[(cache.cell != "ALL") & (cache.cell != "ERROR") & (cache.educg.isin(["BA+", "HS"]))]
base = cells[cells.year.isin([1989, 1990, 1991])].groupby("cell").wsum.sum()
w_fix = base / base.sum()
adj = {}
for yr, sub in cells.groupby("year"):
    p = sub.pivot_table(index="cell", columns="educg", values="wmed")
    nn = sub.pivot_table(index="cell", columns="educg", values="n")
    ok = p.index[(nn.get("BA+", 0) >= 30) & (nn.get("HS", 0) >= 30)]
    ok = [c for c in ok if c in w_fix.index and np.isfinite(p.loc[c, ["BA+", "HS"]]).all()]
    if not ok: continue
    w = w_fix.loc[ok] / w_fix.loc[ok].sum()
    gap = np.log(p.loc[ok, "BA+"]) - np.log(p.loc[ok, "HS"])
    adj[yr] = float(np.exp((w * gap).sum()))
prem["ratio_fixedwt"] = pd.Series(adj)
prem.to_csv("out/morg_premium_annual.csv")
spot = [1979, 1985, 1991, 1992, 2000, 2010, 2019, 2024]
print("\nPremium spot years:\n", prem.loc[[y for y in spot if y in prem.index],
      ["med_BA", "med_HS", "ratio_raw", "ratio_fixedwt", "n_BA", "n_HS"]].round(3).to_string())

# educ share sanity (BA+ share of FT earners 25-64)
sh = cache[cache.cell == "ALL"].pivot_table(index="year", columns="educg", values="wsum")
sh = (sh.T / sh.sum(axis=1)).T
print("\nBA+ share of FT earners 25-64 (spot):",
      {y: round(float(sh.loc[y, "BA+"]), 3) for y in [1980, 1991, 1992, 2005, 2024] if y in sh.index})

# ---------------- Cell 3: Census A-2 (supply: % of 25+ with BA+) ----------------
supply = None
try:
    a2 = pd.read_excel("xl/taba-2.xlsx", header=None)
    col0 = a2[0].apply(lambda v: "" if pd.isna(v) else str(v))
    starts = [i for i, s in col0.items()
              if ("25 Years and Over" in s) and re.search(r"College or [Mm]ore|Bachelor", s)]
    i0 = starts[0]
    recs = {}
    for i in range(i0 + 1, len(a2)):
        s = str(a2.iloc[i, 0])
        if "Completed" in s and "Years" in s:  # next panel header
            break
        m = re.match(r"^\s*((?:19|20)\d{2})", s)
        if m:
            y = int(m.group(1))
            v = pd.to_numeric(a2.iloc[i, 1], errors="coerce")
            if y not in recs and np.isfinite(v):
                recs[y] = float(v)
    supply = pd.Series(recs).sort_index().rename("pct_BAplus_25plus")
    supply.to_csv("out/supply_attainment.csv")
    print("\nCensus %BA+ (25+): ",
          {y: supply[y] for y in [1970, 1990, 2010, 2024] if y in supply.index})
except Exception as e:
    print("CENSUS PARSE FAILED:", e)

# ---------------- Cell 4: NCES 318.10 (BA degrees conferred) ----------------
conf = None
try:
    t = pd.read_excel("xl/tabn318.10.xlsx", header=None)
    recs, proj_cut = {}, None
    for i in range(len(t)):
        s = str(t.iloc[i, 0])
        if re.search(r"[Pp]rojected", " ".join(str(x) for x in t.iloc[i, :3])):
            proj_cut = i
        m = re.match(r"^\s*(\d{4})-(\d{2,4})\s*$", s)
        if m:
            p1, p2 = m.group(1), m.group(2)
            end = int(p2) if len(p2) == 4 else int(p1[:2]) * 100 + int(p2)
            if end < int(p1): end += 100  # 1899-00 style rollover
            v = pd.to_numeric(t.iloc[i, 5], errors="coerce")
            if np.isfinite(v):
                recs[end] = (float(v), i)
    conf = pd.Series({y: v for y, (v, i) in recs.items()
                      if proj_cut is None or i < proj_cut}).sort_index().rename("BA_conferred")
    if proj_cut is None:
        conf = conf[conf.index <= 2022]
        print("(NCES: no 'Projected' marker found; truncated at 2022 by rule)")
    conf.to_csv("out/ba_degrees_conferred.csv")
    print("NCES BA conferred (spot):",
          {y: int(conf[y]) for y in [1970, 2000, 2020] if y in conf.index}, "| last actual:", conf.index.max())
except Exception as e:
    print("NCES PARSE FAILED:", e)

# ---------------- Cell 5: NY Fed underemployment (the queue) ----------------
nyf = None
try:
    u = "https://www.newyorkfed.org/medialibrary/research/interactives/data/college-labor-market/college-labor-underemployment-data.csv"
    r = requests.get(u, headers=UA, timeout=60); r.raise_for_status()
    open("xl/nyfed_underemployment_raw.csv", "wb").write(r.content)
    nyf = pd.read_csv("xl/nyfed_underemployment_raw.csv")
    print("\nNY Fed underemployment columns:", nyf.columns.tolist())
    nyf.to_csv("out/nyfed_underemployment.csv", index=False)
    print(nyf.head(2).to_string(), "\n...\n", nyf.tail(2).to_string())
except Exception as e:
    print("NY FED FETCH/PARSE FAILED:", e)

# companion: unemployment series if it exists at the same pattern
try:
    u2 = "https://www.newyorkfed.org/medialibrary/research/interactives/data/college-labor-market/college-labor-unemployment-data.csv"
    r2 = requests.get(u2, headers=UA, timeout=60)
    if r2.ok and b"," in r2.content[:200]:
        open("out/nyfed_unemployment.csv", "wb").write(r2.content)
        print("(also saved nyfed_unemployment.csv)")
except Exception:
    pass

# ---------------- Cell 6: figure ----------------
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

npanel = 2 + (nyf is not None)
fig, axes = plt.subplots(npanel, 1, figsize=(9, 3.6 * npanel), sharex=False)
ax = axes[0]
ax.plot(prem.index, prem.ratio_raw, lw=2, label="raw: weighted-median ratio, FT 25–64")
ax.plot(prem.index, prem.ratio_fixedwt, lw=1.5, ls="--", label="fixed-weight (sex×age cells, 1989–91 wts)")
ax.axvline(1992, color="gray", ls=":", lw=1)
ax.text(1992.3, ax.get_ylim()[0] + 0.02, "CPS educ redesign", fontsize=8, color="gray")
ax.set_title("College premium: median usual weekly earnings, BA+ / HS (CPS MORG)")
ax.set_ylabel("ratio"); ax.legend(fontsize=8); ax.grid(alpha=.3)

ax = axes[1]
if supply is not None:
    ax.plot(supply.index, supply.values, lw=2, color="tab:green", label="% of 25+ with BA+ (Census A-2)")
    ax.set_ylabel("% BA+ (25+)")
if conf is not None:
    ax2 = ax.twinx()
    ax2.plot(conf.index, conf.values / 1e6, lw=1.5, color="tab:orange", label="BA degrees conferred (right)")
    ax2.set_ylabel("BA conferred, millions")
ax.set_title("Supply: stock (attainment) and flow (conferrals)")
ax.set_xlim(1960, 2026); ax.grid(alpha=.3); ax.legend(fontsize=8, loc="upper left")

if nyf is not None:
    ax = axes[2]
    dcol = nyf.columns[0]
    d = pd.to_datetime(nyf[dcol], errors="coerce")
    if "NBER" in nyf.columns:
        rec = pd.to_numeric(nyf["NBER"], errors="coerce").fillna(0) > 0
        ax.fill_between(d, 0, 55, where=rec, color="gray", alpha=.15, lw=0)
    for c in nyf.columns[1:]:
        if str(c).upper() == "NBER":
            continue
        v = pd.to_numeric(nyf[c], errors="coerce")
        if v.notna().sum() > 10:
            ax.plot(d, v, lw=1.5, label=str(c))
    ax.set_ylim(0, 55)
    ax.set_title("The queue: underemployment rate (NY Fed)")
    ax.set_ylabel("%"); ax.legend(fontsize=8); ax.grid(alpha=.3)

plt.tight_layout(); plt.savefig("out/premium_race.png", dpi=150)
print("\nFigure written: out/premium_race.png")

# ---------------- Cell 7: consolidate extract + note metrics ----------------
import glob as _g
ex = pd.concat([pd.read_parquet(f) for f in sorted(_g.glob("extract/morg_*.parquet"))], ignore_index=True)
ex.to_parquet("out/morg_extract_1979_2024.parquet", index=False)
print("extract rows:", len(ex), "| size MB:", round(os.path.getsize("out/morg_extract_1979_2024.parquet")/1e6, 1))
print("break check raw 1991->1992: %.3f -> %.3f | fixedwt: %.3f -> %.3f" % (
    prem.ratio_raw[1991], prem.ratio_raw[1992], prem.ratio_fixedwt[1991], prem.ratio_fixedwt[1992]))
print("fixedwt peak:", int(prem.ratio_fixedwt.idxmax()), round(prem.ratio_fixedwt.max(), 3),
      "| 2024:", round(prem.ratio_fixedwt[2024], 3))
print("raw 3yr means 1998-2000 / 2008-2010 / 2022-2024: %.3f / %.3f / %.3f" % (
    prem.ratio_raw.loc[1998:2000].mean(), prem.ratio_raw.loc[2008:2010].mean(), prem.ratio_raw.loc[2022:2024].mean()))
